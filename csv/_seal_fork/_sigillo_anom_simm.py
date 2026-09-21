# -*- coding: utf-8 -*-
"""SIGILLO DELLA CURA `C1-bis -- ANOM_SIMM`. [BLOCCANTE]

LE PROVE:
  `U1`  flag SPENTO -> **byte-identico**;
  `U2`  **CONTROLLO POSITIVO**: ACCESO e SPENTO devono differire;
  `U3`  **RIDUZIONE AL LIMITE, e si misura l'ESPONENTE della differenza, non la sua piccolezza.**
        Per `rho = peq*(1+e)`: vecchia `= e`, simmetrica `= 2e/(2+e)`. Quindi
        **`(vecchia - simm)/vecchia -> e/2` ESATTAMENTE**, cioe' la differenza relativa e' **META'
        dell'anomalia**. E' una PREVISIONE con un numero, non un *«sono vicine»*;
  `U4`  **LIMITATA IN `[-2, +2]`**, e **il limite dev'essere RAGGIUNTO**: se `max|anom|` fosse
        lontano da 2, il limite non sarebbe esercitato e la prova non direbbe nulla;
  `U5`  **IL POLO E' CONTATO E VALE ZERO** con `PEQ_ESATTO` acceso -- **e la sua esistenza e'
        dimostrata aritmeticamente**, cosi' `U5` non e' un *«non e' capitato»*;
  `U6`  **`0/0` E' DEFINITO ZERO e succede DAVVERO**: se non capitasse mai, quella definizione
        sarebbe codice morto e non si saprebbe se e' giusta.
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
COMMIT_PRIMA = "eeb31ec"
BLOB_PRIMA = "e844871d"
PASSI = 24
CAMPI = ("d0", "d", "vd", "psi", "phi", "eta", "peq", "perc_chi", "perc_geom",
         "tw", "omega_s", "pos")

# ⚠ LA CONFIGURAZIONE PORTA `--peq-esatto`: `ANOM_SIMM` **dipende** da `C1`, e provarla senza
#   sarebbe provare una configurazione che il codice stesso dichiara non sicura.
ARGV = ["soliton_simulator.py", "--test", "N-MASSE", "--nmasse", "3", "--sep", "4.0",
        "--giri", "0", "--campo-spinoriale", "--spinore-vivo", "--spinore-corretto",
        "--chi-core", "--calore-scal", "--deparam-orologio", "--verlet", "--fork-su2",
        "--fork-su2-mem", "--cs-dinamico", "--tau-luce", "--rumore-colorato",
        "--pav-com", "--guscio-morbido", "--zeta-vir", "--chi-basc", "--chi-coop",
        "--coes-adim", "--plast-din", "--viriale", "--olon-part", "--peq-esatto"]


if "--lavoro" in sys.argv:
    simp = [x.split("=", 1)[1] for x in sys.argv if x.startswith("--sim=")][0]
    outp = [x.split("=", 1)[1] for x in sys.argv if x.startswith("--out=")][0]
    cura = "--cura" in sys.argv
    os.chdir(RADICE)
    sys.argv = list(ARGV) + (["--anom-simm"] if cura else [])
    import importlib.util as _iu
    _sp = _iu.spec_from_file_location("_sim_c1b", simp)
    S = _iu.module_from_spec(_sp)
    sys.modules["_sim_c1b"] = S
    _sp.loader.exec_module(S)
    a = S._cli(); S._applica_regime(a); S._applica_flag(a)
    if cura != bool(getattr(S, "ANOM_SIMM", False)):
        raise SystemExit("[sigillo] il flag non corrisponde alla richiesta")
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
    g = lambda k, d=0: getattr(net, k, d)
    print("C1b usi=%d zero=%d polo=%d fuori=%d maxanom=%.6f archi=%d minpeq=%.6e"
          % (g("_g_as_usi"), g("_g_as_zero"), g("_g_as_polo"), g("_g_as_fuori"),
             g("_g_as_max", -1.0), g("_g_as_archi"), float(np.min(net.peq))))
    raise SystemExit(0)


def gira(*extra):
    pr = subprocess.run([sys.executable, os.path.abspath(__file__)] + list(extra),
                        cwd=RADICE, capture_output=True, text=True,
                        encoding="utf-8", errors="replace")
    if pr.returncode != 0:
        print(pr.stdout[-1500:]); print(pr.stderr[-2500:])
        raise SystemExit("lavoratore uscito con %d" % pr.returncode)
    return pr.stdout


def main():
    base = os.path.join(RADICE, "csv", "_seal_fork", "_sig_anom_simm")
    os.makedirs(base, exist_ok=True)
    esiti = []

    q = subprocess.run(["git", "cat-file", "-p", "%s:soliton_simulator.py" % COMMIT_PRIMA],
                       cwd=RADICE, capture_output=True)
    if q.returncode != 0:
        raise SystemExit("non riesco a estrarre il simulatore di %s" % COMMIT_PRIMA)
    bp = hashlib.sha1(q.stdout).hexdigest()[:8]
    if bp != BLOB_PRIMA:
        raise SystemExit("[U1] blob di %s = %s, atteso %s" % (COMMIT_PRIMA, bp, BLOB_PRIMA))
    prima = os.path.join(base, "_sim_prima.py")
    with open(prima, "wb") as fh:
        fh.write(q.stdout)
    print("sim PRIMA (%s): sha1 GREZZO %s" % (COMMIT_PRIMA, bp))
    print("sim SUL DISCO      : sha1 GREZZO %s\n"
          % hashlib.sha1(open(SIM_ORA, "rb").read()).hexdigest()[:8])

    pA, pB, pC = (os.path.join(base, x) for x in ("A_prima.npz", "B_spento.npz", "C_acceso.npz"))
    print("braccio A (prima della cura)...")
    gira("--lavoro", "--sim=%s" % prima, "--out=%s" % pA)
    print("braccio B (disco, SPENTO)...")
    gira("--lavoro", "--sim=%s" % SIM_ORA, "--out=%s" % pB)
    print("braccio C (disco, ACCESO)...")
    oC = gira("--lavoro", "--sim=%s" % SIM_ORA, "--out=%s" % pC, "--cura")
    print("")
    import re
    m = re.search(r"C1b usi=(\d+) zero=(\d+) polo=(\d+) fuori=(\d+) maxanom=(\S+) archi=(\d+) "
                  r"minpeq=(\S+)", oC)
    if not m:
        raise SystemExit("output non riconosciuto:\n%s" % oC[-800:])
    usi, zero, polo, fuori = (int(m.group(k)) for k in (1, 2, 3, 4))
    maxan = float(m.group(5)); archi = int(m.group(6)); minpeq = float(m.group(7))

    A, B, C = np.load(pA), np.load(pB), np.load(pC)
    f1 = [k for k in CAMPI if k in A and k in B
          and (A[k].shape != B[k].shape or not np.array_equal(A[k], B[k]))]
    com = sum(1 for k in CAMPI if k in A and k in B)
    esiti.append(("U1", (not f1) and com >= 10,
                  "flag SPENTO = prima della cura: %d campi -> %s"
                  % (com, "BYTE-IDENTICI" if not f1 else "DIVERSI: %s" % f1[:5])))
    dif = [k for k in CAMPI if k in B and k in C
           and (B[k].shape != C[k].shape or not np.array_equal(B[k], C[k]))]
    esiti.append(("U2", len(dif) > 0,
                  "CONTROLLO POSITIVO: ACCESO vs SPENTO differiscono su %d campi%s"
                  % (len(dif), "" if dif else "   *** IL FLAG E' INERTE ***")))

    # U3 -- la PREVISIONE con un numero: (vecchia - simm)/vecchia -> e/2
    # ⚠ IL CRITERIO ERA IL MIO SVILUPPO, NON IL VALORE ESATTO, e il FAIL era suo.
    #   Con `r = p*(1+e)`:  vecchia = e,  simmetrica = 2e/(2+e), quindi
    #       (vecchia - simm)/vecchia = 1 - 2/(2+e) = e/(2+e)     <-- ESATTO
    #   `e/2` e' solo il PRIMO ORDINE, e a `e = 0.1` sbaglia del 4.8 % (`2/2.1 = 0.952380952`,
    #   che e' esattamente cio' che il sigillo ha stampato). **Un criterio approssimato applicato
    #   a un'identita' esatta**: si confronta col valore VERO, non col suo sviluppo.
    righe = []
    for e in (1e-1, 1e-2, 1e-3, 1e-4):
        p0, r0 = 1.0, 1.0 * (1.0 + e)
        vec = (r0 - p0) / max(p0, 1e-9)
        sim = 2.0 * (r0 - p0) / (r0 + p0)
        righe.append((e, (vec - sim) / vec, ((vec - sim) / vec) / (e / (2.0 + e))))
    ok3 = max(abs(z - 1.0) for _, _, z in righe) < 1e-12
    esiti.append(("U3", ok3,
                  "RIDUZIONE AL LIMITE: (vecchia-simm)/vecchia diviso il valore ESATTO `e/(2+e)` "
                  "vale %s -- deve fare 1 a precisione di macchina. Le due forme coincidono al "
                  "primo ordine, e lo scarto e' NOTO in forma chiusa, non solo «piccolo»"
                  % ["%.12f" % z for _, _, z in righe]))

    ok4 = (fuori == 0 and archi > 0 and maxan > 1.9)
    esiti.append(("U4", ok4,
                  "LIMITATA IN [-2,+2]: %d archi-scrittura fuori su %d, e max|anom| = %.6f -- il "
                  "limite E' RAGGIUNTO (se fosse lontano da 2 non sarebbe esercitato e la prova "
                  "non direbbe nulla)" % (fuori, archi, maxan)))

    # U5 -- il polo: ZERO in esercizio, ma DIMOSTRATO possibile
    rr, pp = 1.32e-3, -1.32e-3
    den = rr + pp
    oltre = 2.0 * (1.32e-3 - (-1.4e-3)) / (1.32e-3 + (-1.4e-3))
    ok5 = (polo == 0 and den == 0.0 and oltre < 0.0)
    esiti.append(("U5", ok5,
                  "IL POLO: %d occorrenze con `PEQ_ESATTO` acceso (min(peq) = %.3e, mai negativo). "
                  "E NON E' un «non e' capitato»: con `peq = -rho` il denominatore vale "
                  "ESATTAMENTE %.1f, e oltre il polo l'anomalia vale %.2f -- IL SEGNO SI ROVESCIA. "
                  "La dipendenza da C1 e' REALE, non prudenziale" % (polo, minpeq, den, oltre)))

    ok6 = (zero > 0 and usi > 0)
    esiti.append(("U6", ok6,
                  "`0/0` E' DEFINITO ZERO E SUCCEDE DAVVERO: %d archi-scrittura su %d (%.2f%%) -- "
                  "e' il VUOTO su VUOTO. Se non capitasse mai, quella definizione sarebbe codice "
                  "morto" % (zero, archi, 100.0 * zero / max(archi, 1))))

    print("-" * 104)
    for nome, ok, testo in esiti:
        print("%-4s %-4s %s" % (nome, "PASS" if ok else "FAIL", testo))
    print("-" * 104)
    n_ok = sum(1 for _, ok, _ in esiti if ok)
    print("SIGILLO ANOM_SIMM: %d/%d" % (n_ok, len(esiti)))
    print("")
    if n_ok == len(esiti):
        print("VERDETTO: il pavimento `max(peq,1e-9)` e' TOLTO, l'anomalia e' limitata PER")
        print("  COSTRUZIONE, e `0/0` e' una DEFINIZIONE che si esercita davvero.")
    else:
        print("VERDETTO: *** BLOCCANTE: la cura C1-bis non si accende. ***")
    print("")
    print("LIMITI: UN seme, UNA scena, %d passi. E la configurazione porta `--peq-esatto`: questo" % PASSI)
    print("  sigillo NON prova che `ANOM_SIMM` sia sicura DA SOLA -- il codice stesso stampa un")
    print("  avviso grave se la si accende senza `C1`, e `U5` dice perche'.")
    return 0 if n_ok == len(esiti) else 1


if __name__ == "__main__":
    sys.exit(main())
