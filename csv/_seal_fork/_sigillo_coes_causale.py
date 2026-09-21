# -*- coding: utf-8 -*-
"""SIGILLO DELLA CURA `C4 -- COES_CAUSALE`. [BLOCCANTE]

LE PROVE:
  `S1`  flag SPENTO -> **byte-identico** al simulatore di prima della cura;
  `S2`  **CONTROLLO POSITIVO**: ACCESO e SPENTO devono differire;
  `S3`  **L'ISTANTE**: la fotografia di inizio passo e' usata **sempre** *(zero fallback)*, **e lo
        scarto dal `d0` che si leggeva prima e' > 0** -- cioe' **i due istanti ERANO diversi
        davvero**. *(Senza questa seconda meta' il test passerebbe anche se il difetto non ci fosse
        mai stato.)*
  `S4`  **IL CONO E' LOCALE**: il tetto viene da `_cs_nodo_prev` **sempre** *(zero fallback)*, e il
        **minimo locale e' PIU' STRETTO del tetto globale** -- che e' la prova che `A5` era violato;
  `S5`  **NESSUNO SPOSTAMENTO PIU' VELOCE DEL CONO LOCALE**: zero violazioni, col rapporto massimo
        `|delta| / (cs_arco*DT)` riportato.

⚠ `S4` RIPORTA ANCHE IN QUALE VERSO IL TETTO AGISCE, e non e' un dettaglio: il tetto locale **non e'
  sempre piu' stretto**. Dove il cono e' veloce **allarga**. **Il punto non e' stringere: e' che il
  tetto sia quello del LUOGO.** Un sigillo che pretendesse *«stringe sempre»* misurerebbe la
  prudenza, non la causalita'.
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
COMMIT_PRIMA = "4f39828"
BLOB_PRIMA = "716d43b9"
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
    cura = "--cura" in sys.argv
    os.chdir(RADICE)
    sys.argv = list(ARGV) + (["--coes-causale"] if cura else [])
    import importlib.util as _iu
    _sp = _iu.spec_from_file_location("_sim_c4", simp)
    S = _iu.module_from_spec(_sp)
    sys.modules["_sim_c4"] = S
    _sp.loader.exec_module(S)
    a = S._cli(); S._applica_regime(a); S._applica_flag(a)
    if cura != bool(getattr(S, "COES_CAUSALE", False)):
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
    print("C4 tot=%d usi=%d salti=%d scartod0=%.6e | ttot=%d tusi=%d tsalti=%d stringe=%d "
          "allarga=%d archi=%d tmin=%.6e tglob=%.6e viol=%d rapmax=%.6e"
          % (g("_g_cc_tot"), g("_g_cc_usi"), g("_g_cc_salti"), g("_g_cc_scarto_d0", -1.0),
             g("_g_cct_tot"), g("_g_cct_usi"), g("_g_cct_salti"), g("_g_cct_stringe"),
             g("_g_cct_allarga"), g("_g_cct_archi"), g("_g_cct_min", -1.0),
             S.LAM * (S.K_C ** 0.5) * S.DT, g("_g_cct_viol", -1), g("_g_cct_rapmax", -1.0)))
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
    m = re.search(r"C4 tot=(\d+) usi=(\d+) salti=(\d+) scartod0=(\S+) \| ttot=(\d+) tusi=(\d+) "
                  r"tsalti=(\d+) stringe=(\d+) allarga=(\d+) archi=(\d+) tmin=(\S+) tglob=(\S+) "
                  r"viol=(-?\d+) rapmax=(\S+)", out)
    if not m:
        raise SystemExit("output non riconosciuto:\n%s" % out[-900:])
    k = ["tot", "usi", "salti", "scarto", "ttot", "tusi", "tsalti", "stringe", "allarga",
         "archi", "tmin", "tglob", "viol", "rapmax"]
    v = [int(m.group(1)), int(m.group(2)), int(m.group(3)), float(m.group(4)),
         int(m.group(5)), int(m.group(6)), int(m.group(7)), int(m.group(8)),
         int(m.group(9)), int(m.group(10)), float(m.group(11)), float(m.group(12)),
         int(m.group(13)), float(m.group(14))]
    return dict(zip(k, v))


def main():
    base = os.path.join(RADICE, "csv", "_seal_fork", "_sig_coes_causale")
    os.makedirs(base, exist_ok=True)
    esiti = []

    q = subprocess.run(["git", "cat-file", "-p", "%s:soliton_simulator.py" % COMMIT_PRIMA],
                       cwd=RADICE, capture_output=True)
    if q.returncode != 0:
        raise SystemExit("non riesco a estrarre il simulatore di %s" % COMMIT_PRIMA)
    bp = hashlib.sha1(q.stdout).hexdigest()[:8]
    if bp != BLOB_PRIMA:
        raise SystemExit("[S1] blob di %s = %s, atteso %s" % (COMMIT_PRIMA, bp, BLOB_PRIMA))
    prima = os.path.join(base, "_sim_prima.py")
    with open(prima, "wb") as fh:
        fh.write(q.stdout)
    print("sim PRIMA (%s): sha1 GREZZO %s" % (COMMIT_PRIMA, bp))
    print("sim SUL DISCO      : sha1 GREZZO %s\n"
          % hashlib.sha1(open(SIM_ORA, "rb").read()).hexdigest()[:8])

    pA = os.path.join(base, "A_prima.npz")
    pB = os.path.join(base, "B_spento.npz")
    pC = os.path.join(base, "C_acceso.npz")
    print("braccio A (prima della cura)...")
    gira("--lavoro", "--sim=%s" % prima, "--out=%s" % pA)
    print("braccio B (disco, SPENTO)...")
    gira("--lavoro", "--sim=%s" % SIM_ORA, "--out=%s" % pB)
    print("braccio C (disco, ACCESO)...")
    oC = gira("--lavoro", "--sim=%s" % SIM_ORA, "--out=%s" % pC, "--cura")
    print("")
    C_ = leggi(oC)

    A, B, C = np.load(pA), np.load(pB), np.load(pC)
    f1 = [k for k in CAMPI if k in A and k in B
          and (A[k].shape != B[k].shape or not np.array_equal(A[k], B[k]))]
    com = sum(1 for k in CAMPI if k in A and k in B)
    esiti.append(("S1", (not f1) and com >= 10,
                  "flag SPENTO = prima della cura: %d campi -> %s"
                  % (com, "BYTE-IDENTICI" if not f1 else "DIVERSI: %s" % f1[:5])))

    dif = [k for k in CAMPI if k in B and k in C
           and (B[k].shape != C[k].shape or not np.array_equal(B[k], C[k]))]
    esiti.append(("S2", len(dif) > 0,
                  "CONTROLLO POSITIVO: ACCESO vs SPENTO differiscono su %d campi%s"
                  % (len(dif), "" if dif else "   *** IL FLAG E' INERTE ***")))

    ok3 = (C_["usi"] == C_["tot"] and C_["tot"] > 0 and C_["salti"] == 0
           and C_["scarto"] > 0.0)
    esiti.append(("S3", ok3,
                  "L'ISTANTE: fotografia usata %d volte su %d, %d fallback. E LO SCARTO dal `d0` "
                  "che si leggeva prima vale %.4e -- cioe' i due istanti ERANO diversi davvero "
                  "(se fosse 0, il difetto non ci sarebbe mai stato e il test non proverebbe nulla)"
                  % (C_["usi"], C_["tot"], C_["salti"], C_["scarto"])))

    ok4 = (C_["tusi"] == C_["ttot"] and C_["ttot"] > 0 and C_["tsalti"] == 0
           and C_["tmin"] < C_["tglob"])
    esiti.append(("S4", ok4,
                  "IL CONO E' LOCALE: tetto da `_cs_nodo_prev` %d volte su %d, %d fallback; tetto "
                  "minimo locale %.4e contro il globale %.4e (%.2f volte). STRINGE su %d "
                  "archi-scrittura e ALLARGA su %d, su %d -- e non e' un difetto: il tetto dev'essere "
                  "quello del LUOGO, non il piu' prudente"
                  % (C_["tusi"], C_["ttot"], C_["tsalti"], C_["tmin"], C_["tglob"],
                     C_["tmin"] / max(C_["tglob"], 1e-300), C_["stringe"], C_["allarga"],
                     C_["archi"])))

    esiti.append(("S5", C_["viol"] == 0 and C_["rapmax"] <= 1.0,
                  "NESSUNO SPOSTAMENTO PIU' VELOCE DEL CONO LOCALE: %d violazioni, rapporto massimo "
                  "|delta|/(cs_arco*DT) = %.6f" % (C_["viol"], C_["rapmax"])))

    print("-" * 104)
    for nome, ok, testo in esiti:
        print("%-4s %-4s %s" % (nome, "PASS" if ok else "FAIL", testo))
    print("-" * 104)
    n_ok = sum(1 for _, ok, _ in esiti if ok)
    print("SIGILLO COES_CAUSALE: %d/%d" % (n_ok, len(esiti)))
    print("")
    if n_ok == len(esiti):
        print("VERDETTO: la coesione legge un solo ISTANTE e rispetta il CONO DEL LUOGO.")
    else:
        print("VERDETTO: *** BLOCCANTE: la cura C4 non si accende. ***")
    print("")
    print("LIMITI: UN seme, UNA scena, %d passi. `I_nodi`, `I_arco` e `lap_arco` restano di FINE" % PASSI)
    print("  `step`, DICHIARATO: `psi` e' quella che `step()` ha appena committato, quindi le tre")
    print("  sono gia' coerenti fra loro. L'unico ingresso fuori istante era `d0`.")
    return 0 if n_ok == len(esiti) else 1


if __name__ == "__main__":
    sys.exit(main())
