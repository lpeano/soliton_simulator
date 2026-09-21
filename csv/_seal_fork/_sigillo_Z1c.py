# -*- coding: utf-8 -*-
"""SIGILLO `Z1c` -- LA BYTE-IDENTITA' NELLA CONFIGURAZIONE VERA. [BLOCCANTE]

⚠ E' IL TEST CHE MANCAVA, ed e' un rilievo di Luca. `Z1` del sigillo del ramo D confronta con
  l'ARGV NUDO: li' nessun flag di fisica gira, quindi **la catena `CHI_CORE` e il campo `B` del
  passo spinoriale NON VENGONO MAI ESERCITATI** -- e sono esattamente i punti che la modifica ha
  toccato (`chiralita_core_locale(sorgente, geom)`, `_sd0`, `_pav_d0`).
  Un test che non attraversa il codice modificato non prova niente su quel codice.

IL CONFRONTO:
    braccio A   il simulatore di PRIMA di `CHI_COOP` (`0f4fc1e`), con innestata SOLTANTO la cura
                del mondo-dopo-i-flag (categoria D, nessun flag: cambia TUTTI i run e quindi va
                messa da entrambe le parti, senno' si misurerebbe LEI invece dei tre flag)
    braccio B   il simulatore di OGGI
  entrambi con l'ARGV COMPLETO DEL FORK e i TRE flag del ramo D **SPENTI**.

CRITERIO: byte-identici su tutti i campi. Una sola divergenza = i tre flag NON sono inerti nella
configurazione vera, e il ramo D va FERMATO.

⚠ L'INNESTO DELLA CURA SUL SIMULATORE VECCHIO E' LA PARTE DELICATA: si applica la STESSA
  sostituzione esatta, e si VERIFICA che l'ancora sia unica. Se non lo fosse, lo script muore
  invece di innestare a caso.
⚠ Il simulatore vecchio si estrae con `git cat-file -p` IN BINARIO, mai con `git checkout`
  (par.5-quinquies, la trappola CRLF).
⚠ QUESTO SIGILLO NON TOCCA `soliton_simulator.py`: lo LEGGE soltanto. Puo' girare mentre il ramo D
  e' in corso.
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
COMMIT_PRIMA = "0f4fc1e"
PASSI = 30
CAMPI = ("d0", "d", "vd", "psi", "phi", "eta", "perc_chi", "tw", "omega_s", "pos")

# la cura del mondo-dopo-i-flag, nella forma ESATTA in cui e' stata cablata
VECCHIO_BLOCCO = (
    "    # se richiesto un seme/numero nodi diverso, rigenero la rete\n"
    "    if a.seed is not None or a.nodi != SEME_INIZIALE:\n"
    "        net = Rete(a.seed if a.seed is not None else 42)\n"
    "        net.semina(a.nodi)\n"
    "        for _ in range(300): net.step()\n"
    "        net.rilassa_disegno(30)\n")
NUOVO_BLOCCO = (
    "    # [INNESTO Z1c] la cura del mondo-dopo-i-flag, identica a quella cablata nel simulatore\n"
    "    # di oggi: serve da ENTRAMBE le parti, senno' si misurerebbe LEI invece dei tre flag.\n"
    "    net = Rete(a.seed if a.seed is not None else 42)\n"
    "    net.semina(a.nodi)\n"
    "    if a.seed is not None or a.nodi != SEME_INIZIALE:\n"
    "        for _ in range(300): net.step()\n"
    "        net.rilassa_disegno(30)\n")

ARGV_FORK = ["soliton_simulator.py", "--test", "N-MASSE", "--nmasse", "3", "--sep", "4.0",
             "--giri", "0", "--campo-spinoriale", "--spinore-vivo", "--spinore-corretto",
             "--chi-core", "--calore-scal", "--deparam-orologio", "--verlet", "--fork-su2",
             "--fork-su2-mem", "--cs-dinamico", "--tau-luce", "--rumore-colorato",
             "--pav-com", "--guscio-morbido", "--zeta-vir", "--chi-basc", "--plast-din",
             "--viriale", "--olon-part"]


# ----------------------------------------------------------------- il lavoratore
if "--lavoro" in sys.argv:
    simp = [x.split("=", 1)[1] for x in sys.argv if x.startswith("--sim=")][0]
    outp = [x.split("=", 1)[1] for x in sys.argv if x.startswith("--out=")][0]
    os.chdir(RADICE)
    sys.argv = list(ARGV_FORK)
    import importlib.util as _iu
    _sp = _iu.spec_from_file_location("_sim_z1c", simp)
    S = _iu.module_from_spec(_sp)
    sys.modules["_sim_z1c"] = S
    _sp.loader.exec_module(S)
    a = S._cli(); S._applica_regime(a); S._applica_flag(a)
    # i TRE flag devono essere SPENTI: si VERIFICA, non si assume
    for nome in ("CHI_COOP", "SCALA_MIN", "COES_ADIM"):
        if getattr(S, nome, False):
            raise SystemExit("[Z1c] %s e' ACCESO: il confronto non avrebbe senso" % nome)
    # e la catena che il test deve ESERCITARE dev'essere viva
    for nome in ("CHI_CORE", "TORS_4PI", "FRAME_DRAG", "CAMPO_SPINORIALE"):
        if not getattr(S, nome, False):
            raise SystemExit("[Z1c] %s e' SPENTO: il test non attraverserebbe il codice toccato"
                             % nome)
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
    # la prova che la catena e' stata ATTRAVERSATA, non solo accesa
    print("TRACCIA ccl=%d n=%d archi=%d"
          % (getattr(net, "_g_ccl_tot", 0), net.n, len(net.i)))
    raise SystemExit(0)


def gira(sim, out):
    pr = subprocess.run([sys.executable, os.path.abspath(__file__), "--lavoro",
                         "--sim=%s" % sim, "--out=%s" % out],
                        cwd=RADICE, capture_output=True, text=True,
                        encoding="utf-8", errors="replace")
    if pr.returncode != 0:
        print(pr.stdout[-1200:]); print(pr.stderr[-2000:])
        raise SystemExit("lavoratore uscito con %d" % pr.returncode)
    return pr.stdout


def main():
    base = os.path.join(RADICE, "csv", "_seal_fork", "_sig_z1c")
    os.makedirs(base, exist_ok=True)

    q = subprocess.run(["git", "cat-file", "-p", "%s:soliton_simulator.py" % COMMIT_PRIMA],
                       cwd=RADICE, capture_output=True)
    if q.returncode != 0:
        raise SystemExit("non riesco a estrarre il simulatore di %s" % COMMIT_PRIMA)
    testo = q.stdout.decode("utf-8")
    n_anc = testo.count(VECCHIO_BLOCCO)
    if n_anc != 1:
        raise SystemExit("[Z1c] l'ancora della cura compare %d volte nel simulatore di %s: "
                         "NON innesto a caso." % (n_anc, COMMIT_PRIMA))
    innestato = testo.replace(VECCHIO_BLOCCO, NUOVO_BLOCCO)
    vecchio = os.path.join(base, "_sim_prima_con_cura.py")
    with open(vecchio, "wb") as f:
        f.write(innestato.encode("utf-8"))

    with open(SIM_ORA, "rb") as f:
        ora = f.read()
    print("Z1c  simulatore PRIMA (%s)          : sha1 GREZZO %s"
          % (COMMIT_PRIMA, hashlib.sha1(q.stdout).hexdigest()[:8]))
    print("Z1c  PRIMA + la sola cura del mondo  : sha1 GREZZO %s"
          % hashlib.sha1(innestato.encode("utf-8")).hexdigest()[:8])
    print("Z1c  simulatore ORA                  : sha1 GREZZO %s"
          % hashlib.sha1(ora).hexdigest()[:8])
    print("Z1c  (byte grezzi, NON `git hash-object`: sono due numeri diversi, C18)")
    print("")

    pA = os.path.join(base, "A_prima_con_cura.npz")
    pB = os.path.join(base, "B_ora.npz")
    print("braccio A   PRIMA + cura, argv del FORK, i tre flag SPENTI")
    oA = gira(vecchio, pA)
    print("braccio B   ORA,          argv del FORK, i tre flag SPENTI")
    oB = gira(SIM_ORA, pB)
    print("")

    A, B = np.load(pA), np.load(pB)
    f = []
    for k in CAMPI:
        if k not in A or k not in B:
            f.append("%s(assente)" % k); continue
        x, y = A[k], B[k]
        if x.shape != y.shape:
            f.append("%s(shape %s vs %s)" % (k, x.shape, y.shape))
        elif not np.array_equal(x, y):
            f.append("%s(max|d|=%.3e)" % (k, float(np.nanmax(np.abs(x - y)))))

    import re
    cclA = re.search(r"TRACCIA ccl=(\d+)", oA)
    cclB = re.search(r"TRACCIA ccl=(\d+)", oB)
    print("     CONTROPROVA che il test ATTRAVERSA il codice toccato:")
    print("       chiamate a `chiralita_core_locale`:  A = %s   B = %s"
          % (cclA.group(1) if cclA else "?", cclB.group(1) if cclB else "?"))
    vuoto = not (cclB and int(cclB.group(1)) > 0)
    if vuoto:
        print("       *** ZERO chiamate: il test NON esercita la catena -> e' VUOTO, FAIL. ***")
    print("")

    ok = (not f) and not vuoto
    print("Z1c  %-6s argv del FORK, tre flag SPENTI: %d campi -> %s"
          % ("PASS" if ok else "FAIL", len(CAMPI),
             "BYTE-IDENTICI" if not f else "DIVERSI: %s" % f[:6]))
    print("")
    if ok:
        print("VERDETTO: i tre flag sono INERTI anche nella CONFIGURAZIONE VERA, dove la catena")
        print("  CHI_CORE e il campo B del passo spinoriale girano davvero. Il ramo D puo'")
        print("  continuare.")
    else:
        print("VERDETTO: *** FERMARE IL RAMO D. *** I tre flag NON sono inerti a spento nella")
        print("  configurazione vera: il run in corso NON misura quello che dichiara.")
    print("")
    print("LIMITI: UN seme, UNA scena, %d passi. Prova la byte-identita' a flag SPENTI, NON che i" % PASSI)
    print("  flag accesi producano una fisica migliore.")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
