# -*- coding: utf-8 -*-
"""SIGILLO DEI CONTATORI `TRACCIA_PEQ` e dello stop `FERMA_DOPO_NSUB`. [BLOCCANTE]

§1 del MANDATO GLOBALE del 2026-09-21: *«contatori BYTE-INERTI sul modello di `_taup_cfl_max`,
sotto flag. Sigillo di byte-identita' a flag spento, BLOCCANTE.»*

⚠ QUATTRO PROVE, E LA SECONDA E' QUELLA CHE UN SIGILLO DI BYTE-IDENTITA' DI SOLITO NON FA:
  `T1`  a diagnostici SPENTI il simulatore e' byte-identico a quello committato -> il default
        non e' stato toccato;
  `T2`  **a `TRACCIA_PEQ` ACCESO e' ANCORA byte-identico** -> la sonda e' **PURE-READ** (par.2.3),
        non solo inerte quando e' spenta. **Senza `T2`, "byte-inerte" significherebbe soltanto
        "spento", che e' una tautologia;**
  `T3`  CONTROLLO POSITIVO: coi diagnostici accesi i contatori ESISTONO e hanno attraversato
        archi veri. **Senza, `T1` e `T2` passerebbero anche su codice morto;**
  `T4`  `FERMA_DOPO_NSUB` alza davvero `StopDopoNsub` e porta i quattro numeri.

⚠ Il simulatore committato si estrae con `git cat-file -p` IN BINARIO, mai con `git checkout`
  (par.5-quinquies, la trappola CRLF).
⚠ LA CONFIGURAZIONE E' QUELLA VERA DEL RAMO D, coi TRE flag ACCESI: un sigillo che gira sull'argv
  nudo non attraverserebbe il codice toccato (lezione di `Z1c`).
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
# ⚠ IL TERMINE DI PARAGONE E' IL COMMIT *PRIMA* DELLA PATCH, NON `HEAD`.
#   Col codice gia' committato, `HEAD` E' il file sul disco: `T1` passerebbe per TAUTOLOGIA
#   -- la stessa classe del falso PASS gia' catalogata (*«max|A-B| = 0 puo' significare
#   nessun confronto»*, par.9). Il blob atteso si VERIFICA, non si assume.
COMMIT_PRIMA = "f94cd42"
BLOB_PRIMA = "4954fe5b"      # sha1 dei BYTE GREZZI, non `git hash-object`
PASSI = 30
CAMPI = ("d0", "d", "vd", "psi", "phi", "eta", "peq", "perc_chi", "perc_geom",
         "tw", "omega_s", "pos")

ARGV_D = ["soliton_simulator.py", "--test", "N-MASSE", "--nmasse", "3", "--sep", "4.0",
          "--giri", "0", "--campo-spinoriale", "--spinore-vivo", "--spinore-corretto",
          "--chi-core", "--calore-scal", "--deparam-orologio", "--verlet", "--fork-su2",
          "--fork-su2-mem", "--cs-dinamico", "--tau-luce", "--rumore-colorato",
          "--pav-com", "--guscio-morbido", "--zeta-vir", "--chi-basc", "--chi-coop",
          "--scala-min", "--coes-adim", "--plast-din", "--viriale", "--olon-part"]


# ----------------------------------------------------------------- il lavoratore
if "--lavoro" in sys.argv:
    simp = [x.split("=", 1)[1] for x in sys.argv if x.startswith("--sim=")][0]
    outp = [x.split("=", 1)[1] for x in sys.argv if x.startswith("--out=")][0]
    sonda = "--sonda" in sys.argv
    os.chdir(RADICE)
    sys.argv = list(ARGV_D)
    import importlib.util as _iu
    _sp = _iu.spec_from_file_location("_sim_tpeq", simp)
    S = _iu.module_from_spec(_sp)
    sys.modules["_sim_tpeq"] = S
    _sp.loader.exec_module(S)
    if sonda:
        if not hasattr(S, "TRACCIA_PEQ"):
            raise SystemExit("[sigillo] questo simulatore non ha TRACCIA_PEQ")
        S.TRACCIA_PEQ = True
    a = S._cli(); S._applica_regime(a); S._applica_flag(a)
    for nome in ("CHI_COOP", "SCALA_MIN", "COES_ADIM", "CHI_CORE", "TAU_LOCALI"):
        if not getattr(S, nome, False):
            raise SystemExit("[sigillo] %s e' SPENTO: non e' la configurazione del ramo D" % nome)
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
    print("CONTATORI archi=%d passi=%d cflmax=%.6g neg=%d"
          % (getattr(net, "_g_peq_archi", 0), getattr(net, "_g_peq_passi", 0),
             getattr(net, "_g_peq_cfl_max", -1.0), getattr(net, "_g_peq_neg", -1)))
    raise SystemExit(0)


def gira(sim, out, sonda=False):
    cmd = [sys.executable, os.path.abspath(__file__), "--lavoro",
           "--sim=%s" % sim, "--out=%s" % out]
    if sonda:
        cmd.append("--sonda")
    pr = subprocess.run(cmd, cwd=RADICE, capture_output=True, text=True,
                        encoding="utf-8", errors="replace")
    if pr.returncode != 0:
        print(pr.stdout[-1500:]); print(pr.stderr[-2500:])
        raise SystemExit("lavoratore uscito con %d" % pr.returncode)
    return pr.stdout


def confronta(pa, pb):
    A, B = np.load(pa), np.load(pb)
    f = []
    for k in CAMPI:
        if (k in A) != (k in B):
            f.append("%s(presente da una parte sola)" % k); continue
        if k not in A:
            continue
        x, y = A[k], B[k]
        if x.shape != y.shape:
            f.append("%s(shape %s vs %s)" % (k, x.shape, y.shape))
        elif not np.array_equal(x, y):
            f.append("%s(max|d|=%.3e)" % (k, float(np.nanmax(np.abs(x - y)))))
    # ⚠ la guardia del par.9: uno ZERO su un confronto VUOTO non e' identita'
    comuni = sum(1 for k in CAMPI if k in A and k in B)
    return f, comuni


def main():
    base = os.path.join(RADICE, "csv", "_seal_fork", "_sig_traccia_peq")
    os.makedirs(base, exist_ok=True)

    q = subprocess.run(["git", "cat-file", "-p",
                        "%s:soliton_simulator.py" % COMMIT_PRIMA],
                       cwd=RADICE, capture_output=True)
    if q.returncode != 0:
        raise SystemExit("non riesco a estrarre il simulatore di %s" % COMMIT_PRIMA)
    _bp = hashlib.sha1(q.stdout).hexdigest()[:8]
    if _bp != BLOB_PRIMA:
        raise SystemExit("[sigillo] il blob di %s e' %s, atteso %s: il termine di paragone"
                         " NON e' quello dichiarato." % (COMMIT_PRIMA, _bp, BLOB_PRIMA))
    prima = os.path.join(base, "_sim_committato.py")
    with open(prima, "wb") as fh:
        fh.write(q.stdout)
    with open(SIM_ORA, "rb") as fh:
        ora = fh.read()
    print("sim PRIMA (%s)   : sha1 GREZZO %s" % (COMMIT_PRIMA, _bp))
    print("sim SUL DISCO         : sha1 GREZZO %s" % hashlib.sha1(ora).hexdigest()[:8])
    print("(byte grezzi, NON `git hash-object`: sono due numeri diversi, C18)\n")

    pA = os.path.join(base, "A_committato.npz")
    pB = os.path.join(base, "B_disco_spento.npz")
    pC = os.path.join(base, "C_disco_sonda.npz")
    print("braccio A   simulatore di PRIMA della patch, argv del ramo D")
    gira(prima, pA)
    print("braccio B   simulatore SUL DISCO,  diagnostici SPENTI")
    gira(SIM_ORA, pB)
    print("braccio C   simulatore SUL DISCO,  TRACCIA_PEQ ACCESO")
    oC = gira(SIM_ORA, pC, sonda=True)
    print("")

    esiti = []

    f1, c1 = confronta(pA, pB)
    ok1 = (not f1) and c1 >= 10
    esiti.append(("T1", ok1,
                  "diagnostici SPENTI = PRIMA della patch: %d campi -> %s"
                  % (c1, "BYTE-IDENTICI" if not f1 else "DIVERSI: %s" % f1[:5])))

    f2, c2 = confronta(pA, pC)
    ok2 = (not f2) and c2 >= 10
    esiti.append(("T2", ok2,
                  "TRACCIA_PEQ ACCESO = PRIMA della patch: %d campi -> %s  [PURE-READ]"
                  % (c2, "BYTE-IDENTICI" if not f2 else "DIVERSI: %s" % f2[:5])))

    import re
    m = re.search(r"CONTATORI archi=(\d+) passi=(\d+) cflmax=(\S+) neg=(-?\d+)", oC)
    archi = int(m.group(1)) if m else 0
    passi = int(m.group(2)) if m else 0
    ok3 = archi > 0 and passi > 0
    esiti.append(("T3", ok3,
                  "CONTROLLO POSITIVO: la sonda ha attraversato %d archi in %d passi%s"
                  % (archi, passi, "" if ok3 else "   *** ZERO: il test e' VUOTO ***")))

    # T4: lo stop alza davvero, e porta i numeri
    prova = os.path.join(base, "_prova_stop.py")
    with open(prova, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(
            "import os, sys\n"
            "os.chdir(%r)\n"
            "sys.path.insert(0, %r)\n"
            "sys.argv = %r\n"
            "import soliton_simulator as S\n"
            "S.FERMA_DOPO_NSUB = True\n"
            "a = S._cli(); S._applica_regime(a); S._applica_flag(a)\n"
            "S._NMASSE_VIDEO['n'] = 3; S._NMASSE_VIDEO['sep'] = 4.0\n"
            "S._NMASSE_VIDEO['size'] = None\n"
            "S.avvia_test('N-MASSE')()\n"
            "try:\n"
            "    S.net.step()\n"
            "except S.StopDopoNsub as e:\n"
            "    d = S.net._g_nsub_stop\n"
            "    print('STOP ok nsub=%%d n1=%%.0f ramo=%%s msg=%%s'\n"
            "          %% (d['nsub'], d['n1'], d['ramo'], e))\n"
            "    raise SystemExit(0)\n"
            "print('STOP NON ALZATO')\n"
            "raise SystemExit(1)\n" % (RADICE, RADICE, ARGV_D))
    pr = subprocess.run([sys.executable, prova], cwd=RADICE, capture_output=True,
                        text=True, encoding="utf-8", errors="replace")
    riga = [l for l in pr.stdout.splitlines() if l.startswith("STOP")]
    ok4 = pr.returncode == 0 and riga and riga[0].startswith("STOP ok")
    esiti.append(("T4", ok4, "FERMA_DOPO_NSUB alza e porta i numeri: %s"
                  % (riga[0] if riga else "NESSUNO STOP (rc=%d)" % pr.returncode)))

    print("-" * 78)
    for nome, ok, testo in esiti:
        print("%-4s %-4s %s" % (nome, "PASS" if ok else "FAIL", testo))
    print("-" * 78)
    n_ok = sum(1 for _, ok, _ in esiti if ok)
    print("SIGILLO TRACCIA_PEQ: %d/%d" % (n_ok, len(esiti)))
    print("")
    if n_ok == len(esiti):
        print("VERDETTO: i contatori sono BYTE-INERTI *e* PURE-READ, e NON sono codice morto.")
        print("  Si puo' misurare.")
    else:
        print("VERDETTO: *** BLOCCANTE. Non si misura con una sonda che non e' provata. ***")
    print("")
    print("LIMITI: UN seme, UNA scena, %d passi. Prova la byte-identita' e la purezza," % PASSI)
    print("  NON che i numeri che la sonda produce siano interpretati bene.")
    return 0 if n_ok == len(esiti) else 1


if __name__ == "__main__":
    sys.exit(main())
