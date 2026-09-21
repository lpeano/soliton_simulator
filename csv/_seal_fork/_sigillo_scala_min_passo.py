# -*- coding: utf-8 -*-
"""SIGILLO DELLA CURA `C3 -- SCALA_MIN_PASSO`. [BLOCCANTE]

⚠ `R3` E' IL SIGILLO CHE OGGI NON ESISTE: **LA COMPOSIZIONE.**
  Tutti i criteri di `SCALA_MIN` guardano la SINGOLA scrittura, e su quella il codice e' corretto
  *(`_g_sm_max_giu = -0` su tutti gli snapshot del ramo D)*. **Il cricchetto vive nella SOMMA di
  sei scritture frenate una per una, e nessun criterio guardava la somma** (`A9`).
  `R3` inietta **spinte opposte di somma NULLA** e chiede che `d0` torni **identico**.
  **E il contrasto lo rende non vuoto:** con il freno per-scrittura lo stesso test **DEVE fallire**.
  Un criterio che passa in entrambi i regimi non distingue niente.

LE PROVE:
  `R1`  flag SPENTO -> **byte-identico** al simulatore di prima della cura;
  `R2`  **CONTROLLO POSITIVO**: ACCESO e SPENTO devono differire;
  `R3`  **COMPOSIZIONE** -- somma nulla dentro un passo: con `C3` `d0` e' **INTATTO**, col freno
        per-scrittura **NO**. *(Le due meta' insieme, o il test non prova niente.)*
  `R4`  **il VINCOLO TIENE**: con `C3` nessuna lunghezza scende sotto `LAM`;
  `R5`  **LA CHIRURGIA E' ALLINEATA**: aperture == chiusure, e **zero** disallineamenti attraverso
        la mitosi -- che e' la parte delicata della cura;
  `R6`  **`nsub` NON MOLTIPLICA PIU' IL BIAS**: il freno su `d` gira **una volta per passo**,
        qualunque sia `nsub`.
ASCII PURO.
"""
import hashlib
import os
import subprocess
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
SIM_ORA = os.path.join(RADICE, "soliton_simulator.py")
COMMIT_PRIMA = "2a0e908"
BLOB_PRIMA = "d30bb0b9"
PASSI = 24
CAMPI = ("d0", "d", "vd", "psi", "phi", "eta", "peq", "perc_chi", "perc_geom",
         "tw", "omega_s", "pos")

ARGV = ["soliton_simulator.py", "--test", "N-MASSE", "--nmasse", "3", "--sep", "4.0",
        "--giri", "0", "--campo-spinoriale", "--spinore-vivo", "--spinore-corretto",
        "--chi-core", "--calore-scal", "--deparam-orologio", "--verlet", "--fork-su2",
        "--fork-su2-mem", "--cs-dinamico", "--tau-luce", "--rumore-colorato",
        "--pav-com", "--guscio-morbido", "--zeta-vir", "--chi-basc", "--chi-coop",
        "--coes-adim", "--plast-din", "--viriale", "--olon-part"]


if "--lavoro" in sys.argv:
    simp = [x.split("=", 1)[1] for x in sys.argv if x.startswith("--sim=")][0]
    outp = [x.split("=", 1)[1] for x in sys.argv if x.startswith("--out=")][0]
    modo = [x.split("=", 1)[1] for x in sys.argv if x.startswith("--modo=")][0]
    os.chdir(RADICE)
    extra = {"spento": [], "passo": ["--scala-min-passo"], "scrittura": ["--scala-min"]}[modo]
    sys.argv = list(ARGV) + extra
    import importlib.util as _iu
    _sp = _iu.spec_from_file_location("_sim_c3", simp)
    S = _iu.module_from_spec(_sp)
    sys.modules["_sim_c3"] = S
    _sp.loader.exec_module(S)
    a = S._cli(); S._applica_regime(a); S._applica_flag(a)
    S._NMASSE_VIDEO["n"] = 3; S._NMASSE_VIDEO["sep"] = 4.0; S._NMASSE_VIDEO["size"] = None
    S.avvia_test("N-MASSE")()
    net = S.net
    S.stato["nframe"] = 0
    for _f in range(PASSI // int(S.PASSI_PER_FRAME)):
        S.passo_test()
        for _ in range(int(S.PASSI_PER_FRAME)):
            S.scuoti_vuoto(net); net.step(); net.mitosi()
            net.rilassa_disegno(); net.memoria_hebbiana_moto()
    np.savez(outp, **{k: np.asarray(getattr(net, k)) for k in CAMPI if hasattr(net, k)})

    # --- R3: LA COMPOSIZIONE, sul CODICE VERO (non su un modello del codice)
    # Si aprono le stesse porte che apre il passo, si iniettano DUE spinte opposte di somma
    # ESATTAMENTE nulla attraverso `_sd0`, e si chiude. Con `C3` il freno vede `dx = 0` -- che
    # non e' una discesa -- e il valore resta intatto. Col freno per-scrittura ogni meta' viene
    # frenata da sola, e la somma NON torna.
    # ⚠ il braccio A gira sul simulatore di PRIMA della cura, che i tre metodi non li ha: li' non
    #   si inietta niente e il bias resta `nan`, cosi' non lo si confonde con uno ZERO MISURATO.
    #   (`nan` != 0.0, quindi un criterio scritto male fallisce invece di passare di nascosto.)
    # ⚠ I CONTATORI SI LEGGONO **PRIMA** DELL'INIEZIONE: l'iniezione stessa apre e chiude il freno,
    #   e li' gonfierebbe di 1. *(E' successo: `25` aperture su `24` passi, e il FAIL era MIO.)*
    cont = dict(ap=getattr(net, "_g_smp_aperture", 0), ch=getattr(net, "_g_smp_chiusure", 0),
                chir=getattr(net, "_g_smp_chirurgie", 0),
                dis=getattr(net, "_g_smp_disallineati", 0),
                dch=getattr(net, "_g_smp_d_chiusure", 0),
                pas=getattr(net, "_g_smp_passanti", 0),
                nsub=getattr(net, "_g_smp_d_nsub", 0))
    d0_prima = np.array(net.d0, dtype=float, copy=True)
    # ⚠ IL RESIDUO DI ARROTONDAMENTO SI **MISURA**, NON SI SCEGLIE UNA SOGLIA.
    #   `(x + s) - s` non torna `x` in virgola mobile, e quel residuo e' INEVITABILE: e' il
    #   metro con cui si giudica il bias della cura. Nessun numero inventato (`A11`, corollario 1).
    spinta = 0.10 * np.maximum(d0_prima, 1e-12)
    _puro = (d0_prima + spinta) - spinta
    arrot = float(np.max(np.abs(_puro - d0_prima)))
    if hasattr(net, "_smp_apri"):
        net._smp_apri()
        net.d0 = net.d0 + net._sd0(+spinta)
        net.d0 = net.d0 + net._sd0(-spinta)
        net._smp_chiudi()
        scarto = float(np.max(np.abs(np.asarray(net.d0, dtype=float) - d0_prima)))
        rel = scarto / max(float(np.median(d0_prima)), 1e-12)
    else:
        scarto = rel = float("nan")

    print("C3 modo=%s passi=%d aperture=%d chiusure=%d chirurgie=%d disall=%d dchius=%d "
          "passanti=%d mind=%.6f mind0=%.6f LAM=%.4f bias=%.6e biasrel=%.6e nsubmax=%d "
          "arrot=%.6e"
          % (modo, PASSI, cont["ap"], cont["ch"], cont["chir"], cont["dis"], cont["dch"],
             cont["pas"], float(np.min(net.d)), float(np.min(d0_prima)), S.LAM, scarto, rel,
             cont["nsub"], arrot))
    raise SystemExit(0)


def gira(*extra):
    pr = subprocess.run([sys.executable, os.path.abspath(__file__)] + list(extra),
                        cwd=RADICE, capture_output=True, text=True,
                        encoding="utf-8", errors="replace")
    if pr.returncode != 0:
        print(pr.stdout[-1500:]); print(pr.stderr[-2500:])
        raise SystemExit("lavoratore uscito con %d" % pr.returncode)
    return pr.stdout


def leggi(out):
    import re
    m = re.search(r"C3 modo=(\S+) passi=(\d+) aperture=(\d+) chiusure=(\d+) chirurgie=(\d+) "
                  r"disall=(\d+) dchius=(\d+) passanti=(\d+) mind=(\S+) mind0=(\S+) LAM=(\S+) "
                  r"bias=(\S+) biasrel=(\S+) nsubmax=(\d+) arrot=(\S+)", out)
    if not m:
        raise SystemExit("output non riconosciuto:\n%s" % out[-900:])
    return dict(modo=m.group(1), passi=int(m.group(2)), ap=int(m.group(3)), ch=int(m.group(4)),
                chir=int(m.group(5)), dis=int(m.group(6)), dch=int(m.group(7)),
                pas=int(m.group(8)), mind=float(m.group(9)), mind0=float(m.group(10)),
                lam=float(m.group(11)), bias=float(m.group(12)), biasrel=float(m.group(13)),
                nsub=int(m.group(14)), arrot=float(m.group(15)))


def main():
    base = os.path.join(RADICE, "csv", "_seal_fork", "_sig_scala_min_passo")
    os.makedirs(base, exist_ok=True)
    esiti = []

    q = subprocess.run(["git", "cat-file", "-p", "%s:soliton_simulator.py" % COMMIT_PRIMA],
                       cwd=RADICE, capture_output=True)
    if q.returncode != 0:
        raise SystemExit("non riesco a estrarre il simulatore di %s" % COMMIT_PRIMA)
    bp = hashlib.sha1(q.stdout).hexdigest()[:8]
    if bp != BLOB_PRIMA:
        raise SystemExit("[R1] blob di %s = %s, atteso %s" % (COMMIT_PRIMA, bp, BLOB_PRIMA))
    prima = os.path.join(base, "_sim_prima.py")
    with open(prima, "wb") as fh:
        fh.write(q.stdout)
    print("sim PRIMA (%s): sha1 GREZZO %s" % (COMMIT_PRIMA, bp))
    print("sim SUL DISCO      : sha1 GREZZO %s\n"
          % hashlib.sha1(open(SIM_ORA, "rb").read()).hexdigest()[:8])

    pA = os.path.join(base, "A_prima.npz")
    pB = os.path.join(base, "B_spento.npz")
    pC = os.path.join(base, "C_passo.npz")
    pD = os.path.join(base, "D_scrittura.npz")
    print("braccio A (prima della cura)...")
    gira("--lavoro", "--sim=%s" % prima, "--out=%s" % pA, "--modo=spento")
    print("braccio B (disco, tutto SPENTO)...")
    oB = gira("--lavoro", "--sim=%s" % SIM_ORA, "--out=%s" % pB, "--modo=spento")
    print("braccio C (disco, SCALA_MIN_PASSO)...")
    oC = gira("--lavoro", "--sim=%s" % SIM_ORA, "--out=%s" % pC, "--modo=passo")
    print("braccio D (disco, SCALA_MIN per-scrittura)...")
    oD = gira("--lavoro", "--sim=%s" % SIM_ORA, "--out=%s" % pD, "--modo=scrittura")
    print("")
    B_, C_, D_ = leggi(oB), leggi(oC), leggi(oD)

    A, B, C = np.load(pA), np.load(pB), np.load(pC)
    f1 = [k for k in CAMPI if k in A and k in B
          and (A[k].shape != B[k].shape or not np.array_equal(A[k], B[k]))]
    com = sum(1 for k in CAMPI if k in A and k in B)
    esiti.append(("R1", (not f1) and com >= 10,
                  "flag SPENTO = prima della cura: %d campi -> %s"
                  % (com, "BYTE-IDENTICI" if not f1 else "DIVERSI: %s" % f1[:5])))

    dif = [k for k in CAMPI if k in B and k in C
           and (B[k].shape != C[k].shape or not np.array_equal(B[k], C[k]))]
    esiti.append(("R2", len(dif) > 0,
                  "CONTROLLO POSITIVO: ACCESO vs SPENTO differiscono su %d campi%s"
                  % (len(dif), "" if dif else "   *** IL FLAG E' INERTE ***")))

    # R3 -- e le DUE meta' insieme, o non prova niente
    # ⚠ IL METRO E' L'ARROTONDAMENTO MISURATO, non una soglia scelta (`A11`, corollario 1).
    #   `(x + s) - s` non torna `x` in virgola mobile: quel residuo e' INEVITABILE, e il bias
    #   della cura non puo' essere piu' piccolo di lui. La prima versione chiedeva `== 0.0`
    #   ESATTO e falliva su `4.441e-16`, che sono DUE ulp: **il FAIL era del criterio.**
    ok3 = (C_["bias"] <= C_["arrot"] and D_["bias"] > 1000.0 * max(D_["arrot"], 1e-300))
    esiti.append(("R3", ok3,
                  "COMPOSIZIONE (spinte opposte a somma NULLA dentro un passo): C3 -> bias = "
                  "%.3e contro un arrotondamento INEVITABILE di %.3e (dev'essere <=); freno "
                  "per-scrittura -> bias = %.3e, cioe' %.4f%% della mediana di `d0` e %.0f "
                  "VOLTE l'arrotondamento (DEVE essere enormemente sopra, senno' il test non "
                  "distingue)"
                  % (C_["bias"], C_["arrot"], D_["bias"], 100.0 * D_["biasrel"],
                     D_["bias"] / max(D_["arrot"], 1e-300))))

    esiti.append(("R4", C_["mind"] >= C_["lam"] - 1e-12,
                  "IL VINCOLO TIENE: con C3 min(d) = %.6f contro LAM = %.4f"
                  % (C_["mind"], C_["lam"])))

    ok5 = (C_["ap"] == C_["ch"] == C_["passi"] and C_["dis"] == 0 and C_["chir"] > 0)
    esiti.append(("R5", ok5,
                  "LA CHIRURGIA E' ALLINEATA: %d aperture, %d chiusure su %d passi, %d chirurgie "
                  "attraverso la mitosi, %d disallineamenti (deve essere 0)"
                  % (C_["ap"], C_["ch"], C_["passi"], C_["chir"], C_["dis"])))

    ok6 = (C_["dch"] == C_["passi"] and C_["nsub"] >= 4)
    esiti.append(("R6", ok6,
                  "`nsub` NON MOLTIPLICA PIU' IL BIAS: il freno su `d` gira %d volte in %d passi "
                  "(una per passo), col `nsub` massimo osservato = %d. Prima girava `nsub` volte."
                  % (C_["dch"], C_["passi"], C_["nsub"])))

    print("-" * 100)
    for nome, ok, testo in esiti:
        print("%-4s %-4s %s" % (nome, "PASS" if ok else "FAIL", testo))
    print("-" * 100)
    n_ok = sum(1 for _, ok, _ in esiti if ok)
    print("SIGILLO SCALA_MIN_PASSO: %d/%d" % (n_ok, len(esiti)))
    print("")
    if n_ok == len(esiti):
        print("VERDETTO: il CRICCHETTO e' curato. Con spinte a somma nulla `d0` resta INTATTO, il")
        print("  vincolo `LAM` tiene, la chirurgia attraverso la mitosi e' allineata, e `nsub` non")
        print("  moltiplica piu' il bias.")
    else:
        print("VERDETTO: *** BLOCCANTE: la cura C3 non si accende. ***")
    print("")
    print("LIMITI: UN seme, UNA scena, %d passi. `R3` inietta spinte COSTRUITE (10%% di `d0`), non" % PASSI)
    print("  le spinte vere delle sei leggi: prova che l'OPERATORE compone bene, non che nel run")
    print("  vero le spinte si compensino.")
    return 0 if n_ok == len(esiti) else 1


if __name__ == "__main__":
    sys.exit(main())
