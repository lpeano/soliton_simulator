# -*- coding: utf-8 -*-
"""SIGILLO DELLA CURA `C1 -- PEQ_ESATTO`. [BLOCCANTE]

CINQUE PROVE:
  `P1`  flag SPENTO -> **byte-identico** al simulatore di prima della cura;
  `P2`  **riduzione al limite**: per `dt/tau -> 0` lo scarto dall'Eulero va come `(dt/tau)^2`.
        **Non si misura che sia "piccolo": si misura l'ESPONENTE**, perche' "piccolo" non e' un
        criterio e l'esponente si'.
  `P3`  su un run vero col flag ACCESO, **`peq >= 0` su ogni arco a ogni passo**;
  `P4`  **CONTROLLO POSITIVO**: con `x = dt/tau > soglia` costruito a mano, **l'Eulero va NEGATIVO
        e la forma esatta NO**. Senza questa prova `P1`-`P3` passerebbero anche su codice morto;
  `P5`  **IL PASSO VERO**: al passo `1126` del ramo D, **sullo STESSO STATO**, la cura accesa
        **NON produce il picco**. E' la verifica della previsione scritta in `Z94`
        *(`+4.112e-03` invece di `-4.854e-04`)*, chiesta esplicitamente da Luca.

⚠ `P5` HA DUE FORME, e servono ENTRAMBE:
  `P5a`  si rigioca `1080 -> 1125` **a cura SPENTA** *(traiettoria IDENTICA, byte per byte)* e si
         accende la cura **SOLO per il passo 1126**: cosi' i due `nsub` sono calcolati **sullo
         STESSO STATO** e il confronto e' pulito;
  `P5b`  si rigioca tutta la finestra **a cura ACCESA**: qui la traiettoria diverge -- ed e'
         giusto che diverga -- e si guarda che **nessun picco compaia** e che `peq >= 0` sempre.
  **`P5a` isola la cura, `P5b` dice che non ne nasce un altro poco piu' in la'. Nessuna delle due
  sostituisce l'altra.**
ASCII PURO.
"""
import hashlib
import io
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
COMMIT_PRIMA = "bbeb9f3"
BLOB_PRIMA = "3b9e75bf"          # sha1 dei BYTE GREZZI, non `git hash-object`
PASSI = 30
CAMPI = ("d0", "d", "vd", "psi", "phi", "eta", "peq", "perc_chi", "perc_geom",
         "tw", "omega_s", "pos")
SNAP = os.path.join(RADICE, "csv", "_test_fork", "_ab_D", "scena_001080.pkl.gz")
SIG_TPEQ = os.path.join(RADICE, "csv", "_seal_fork", "_sigillo_traccia_peq_2026-09-21.txt")

ARGV_D = ["soliton_simulator.py", "--test", "N-MASSE", "--nmasse", "3", "--sep", "4.0",
          "--giri", "0", "--campo-spinoriale", "--spinore-vivo", "--spinore-corretto",
          "--chi-core", "--calore-scal", "--deparam-orologio", "--verlet", "--fork-su2",
          "--fork-su2-mem", "--cs-dinamico", "--tau-luce", "--rumore-colorato",
          "--pav-com", "--guscio-morbido", "--zeta-vir", "--chi-basc", "--chi-coop",
          "--scala-min", "--coes-adim", "--plast-din", "--viriale", "--olon-part"]


def sblocca(net, snap):
    """Override DICHIARATO della guardia del blob, CONDIZIONATO al sigillo di `TRACCIA_PEQ`."""
    import gzip
    import pickle
    if "SIGILLO TRACCIA_PEQ: 4/4" not in io.open(SIG_TPEQ, encoding="utf-8",
                                                 errors="replace").read():
        raise SystemExit("[P5] il sigillo di TRACCIA_PEQ non dice 4/4: NON sblocco")
    with gzip.open(snap, "rb") as fh:
        b = pickle.load(fh).get("blob")
    orig = type(net)._versione_codice

    def finto(self):
        v = orig(self)
        v["blob"] = b
        return v
    type(net)._versione_codice = finto
    return orig


# ----------------------------------------------------------------- i lavoratori
if "--lavoro" in sys.argv:
    simp = [x.split("=", 1)[1] for x in sys.argv if x.startswith("--sim=")][0]
    outp = [x.split("=", 1)[1] for x in sys.argv if x.startswith("--out=")][0]
    cura = "--cura" in sys.argv
    os.chdir(RADICE)
    sys.argv = list(ARGV_D) + (["--peq-esatto"] if cura else [])
    import importlib.util as _iu
    _sp = _iu.spec_from_file_location("_sim_c1", simp)
    S = _iu.module_from_spec(_sp)
    sys.modules["_sim_c1"] = S
    _sp.loader.exec_module(S)
    a = S._cli(); S._applica_regime(a); S._applica_flag(a)
    if cura and not getattr(S, "PEQ_ESATTO", False):
        raise SystemExit("[sigillo] --peq-esatto non ha acceso PEQ_ESATTO")
    if (not cura) and getattr(S, "PEQ_ESATTO", False):
        raise SystemExit("[sigillo] PEQ_ESATTO ACCESO nel braccio che lo vuole spento")
    S._NMASSE_VIDEO["n"] = 3; S._NMASSE_VIDEO["sep"] = 4.0; S._NMASSE_VIDEO["size"] = None
    S.avvia_test("N-MASSE")()
    net = S.net
    S.stato["nframe"] = 0
    peq_min = float("inf")
    for _f in range(PASSI // int(S.PASSI_PER_FRAME)):
        S.passo_test()
        for _ in range(int(S.PASSI_PER_FRAME)):
            S.scuoti_vuoto(net); net.step(); net.mitosi()
            net.rilassa_disegno(); net.memoria_hebbiana_moto()
            peq_min = min(peq_min, float(np.min(net.peq)) if len(net.peq) else peq_min)
    np.savez(outp, **{k: np.asarray(getattr(net, k)) for k in CAMPI if hasattr(net, k)})
    print("RUN peqmin=%.6e usi=%d salvati=%d neg=%d bersneg=%d"
          % (peq_min, getattr(net, "_g_peqx_usi", 0), getattr(net, "_g_peqx_salvati", 0),
             getattr(net, "_g_peqx_neg", 0), getattr(net, "_g_peqx_bers_neg", 0)))
    raise SystemExit(0)


if "--p5" in sys.argv:
    # P5a: stesso stato, la cura accesa SOLO al passo 1126. P5b: cura accesa da subito.
    modo = [x.split("=", 1)[1] for x in sys.argv if x.startswith("--modo=")][0]
    os.chdir(RADICE)
    # ⚠ il simulatore vive nella RADICE, non in `csv/_seal_fork/`: senza questa riga
    #   l'`import` muore, e con lo stderr non catturato il sigillo diceva "nessuno stop"
    #   invece di "non parte". Un FAIL che nasconde la sua causa e' peggio di un FAIL.
    sys.path.insert(0, RADICE)
    sys.argv = list(ARGV_D) + (["--peq-esatto"] if modo == "b" else [])
    import soliton_simulator as S
    a = S._cli(); S._applica_regime(a); S._applica_flag(a)
    net = S.net
    orig = sblocca(net, SNAP)
    try:
        if not net.carica_stato(SNAP):
            raise SystemExit("[P5] carica_stato ha rifiutato")
    finally:
        type(net)._versione_codice = orig
    PPF = int(S.PASSI_PER_FRAME)
    peq_min = float("inf")
    for k in range(1, 47):
        passo = 1080 + k
        if (k - 1) % PPF == 0:
            S.passo_test()
        S.scuoti_vuoto(net)
        if passo == 1126:
            if modo == "a":
                S.PEQ_ESATTO = True          # ⚠ SOLO da qui: lo STATO e' quello di prima
            S.FERMA_DOPO_NSUB = True
        try:
            net.step()
        except S.StopDopoNsub as e:
            d = net._g_nsub_stop
            print("P5%s STOP passo=%d nsub=%d n1=%.0f n3=%.0f peqmin=%.6e salvati=%d"
                  % (modo, passo, d["nsub"], d["n1"], d["n3"], peq_min,
                     getattr(net, "_g_peqx_salvati", 0)))
            raise SystemExit(0)
        if len(net.peq):
            peq_min = min(peq_min, float(np.min(net.peq)))
        net.mitosi(); net.rilassa_disegno(); net.memoria_hebbiana_moto()
    print("P5%s NESSUNO STOP" % modo)
    raise SystemExit(1)


def gira(*extra, **kw):
    pr = subprocess.run([sys.executable, os.path.abspath(__file__)] + list(extra),
                        cwd=RADICE, capture_output=True, text=True,
                        encoding="utf-8", errors="replace")
    if pr.returncode != 0 and not kw.get("tollera"):
        print(pr.stdout[-1500:]); print(pr.stderr[-2500:])
        raise SystemExit("lavoratore uscito con %d" % pr.returncode)
    # ⚠ SI RESTITUISCE ANCHE LO STDERR: senza, un lavoratore che MUORE produce un FAIL che
    #   dice "nessuno stop" invece della causa vera. E' successo, e mi ha fatto cercare nel
    #   posto sbagliato.
    if pr.returncode == 0:
        return pr.stdout
    return pr.stdout + os.linesep + "[stderr]" + os.linesep + pr.stderr


def main():
    base = os.path.join(RADICE, "csv", "_seal_fork", "_sig_peq_esatto")
    os.makedirs(base, exist_ok=True)
    esiti = []

    # ---- P1
    q = subprocess.run(["git", "cat-file", "-p", "%s:soliton_simulator.py" % COMMIT_PRIMA],
                       cwd=RADICE, capture_output=True)
    if q.returncode != 0:
        raise SystemExit("non riesco a estrarre il simulatore di %s" % COMMIT_PRIMA)
    bp = hashlib.sha1(q.stdout).hexdigest()[:8]
    if bp != BLOB_PRIMA:
        raise SystemExit("[P1] blob di %s = %s, atteso %s: termine di paragone SBAGLIATO"
                         % (COMMIT_PRIMA, bp, BLOB_PRIMA))
    prima = os.path.join(base, "_sim_prima.py")
    with open(prima, "wb") as fh:
        fh.write(q.stdout)
    print("sim PRIMA (%s): sha1 GREZZO %s" % (COMMIT_PRIMA, bp))
    print("sim SUL DISCO      : sha1 GREZZO %s\n"
          % hashlib.sha1(open(SIM_ORA, "rb").read()).hexdigest()[:8])

    pA = os.path.join(base, "A_prima.npz")
    pB = os.path.join(base, "B_spento.npz")
    pC = os.path.join(base, "C_acceso.npz")
    print("P1  braccio A (prima della cura) e B (disco, flag SPENTO)...")
    gira("--lavoro", "--sim=%s" % prima, "--out=%s" % pA)
    gira("--lavoro", "--sim=%s" % SIM_ORA, "--out=%s" % pB)
    A, B = np.load(pA), np.load(pB)
    f1 = [k for k in CAMPI if k in A and k in B
          and (A[k].shape != B[k].shape or not np.array_equal(A[k], B[k]))]
    com = sum(1 for k in CAMPI if k in A and k in B)
    esiti.append(("P1", (not f1) and com >= 10,
                  "flag SPENTO = prima della cura: %d campi -> %s"
                  % (com, "BYTE-IDENTICI" if not f1 else "DIVERSI: %s" % f1[:5])))

    # ---- P2  riduzione al limite: l'ESPONENTE, non l'ampiezza
    p0, r0 = 1.0, 0.25
    righe = []
    for x in (1e-1, 1e-2, 1e-3, 1e-4):
        eul = p0 + x * (r0 - p0)
        exa = r0 + (p0 - r0) * np.exp(-x)
        righe.append((x, abs(exa - eul), abs(exa - eul) / x ** 2))
    # se lo scarto e' O(x^2), `scarto/x^2` e' COSTANTE e vale |p-r|/2
    atteso = abs(p0 - r0) / 2.0
    rapporti = [z for _, _, z in righe]
    ok2 = max(abs(z / atteso - 1.0) for z in rapporti) < 0.06
    esiti.append(("P2", ok2,
                  "riduzione al limite: scarto/x^2 = %s  (atteso |p-r|/2 = %.4f) -> l'ESPONENTE e' 2"
                  % (["%.5f" % z for z in rapporti], atteso)))

    # ---- P4  controllo positivo, aritmetico ed esplicito
    p1v, r1v, xv = 1.0, 0.0, 1.5
    eul = p1v + xv * (r1v - p1v)
    exa = r1v + (p1v - r1v) * np.exp(-xv)
    ok4 = eul < 0.0 <= exa
    esiti.append(("P4", ok4,
                  "CONTROLLO POSITIVO x=%.1f: Eulero -> %+.4f (%s), esatto -> %+.4f (%s)"
                  % (xv, eul, "NEGATIVO" if eul < 0 else "positivo",
                     exa, "positivo" if exa >= 0 else "NEGATIVO")))

    # ---- P3  run vero col flag acceso
    print("P3  braccio C (disco, flag ACCESO)...")
    oC = gira("--lavoro", "--sim=%s" % SIM_ORA, "--out=%s" % pC, "--cura")
    import re
    m = re.search(r"RUN peqmin=(\S+) usi=(\d+) salvati=(\d+) neg=(\d+) bersneg=(\d+)", oC)
    peqmin = float(m.group(1)) if m else 1.0
    usi = int(m.group(2)) if m else 0
    neg = int(m.group(4)) if m else -1
    bneg = int(m.group(5)) if m else -1
    ok3 = peqmin >= 0.0 and usi > 0 and neg == 0
    esiti.append(("P3", ok3,
                  "run col flag ACCESO: min(peq) = %.6e, usi = %d, peq<0 = %d, bersaglio<0 = %d"
                  % (peqmin, usi, neg, bneg)))
    # e il braccio ACCESO DEVE differire da quello spento: senno' il flag e' inerte
    C = np.load(pC)
    diff = [k for k in CAMPI if k in B and k in C
            and (B[k].shape != C[k].shape or not np.array_equal(B[k], C[k]))]
    esiti.append(("P3b", len(diff) > 0,
                  "CONTROLLO POSITIVO sul flag: ACCESO vs SPENTO differiscono su %d campi%s"
                  % (len(diff), "" if diff else "   *** IL FLAG E' INERTE: codice morto ***")))

    # ---- P5  il passo vero
    print("P5a stesso stato, cura accesa SOLO al passo 1126...")
    o5a = gira("--p5", "--modo=a", tollera=True)
    print("P5b finestra intera a cura ACCESA...")
    o5b = gira("--p5", "--modo=b", tollera=True)
    for modo, out in (("a", o5a), ("b", o5b)):
        mm = re.search(r"P5%s STOP passo=(\d+) nsub=(\d+) n1=(\S+) n3=(\S+) peqmin=(\S+) "
                       r"salvati=(\d+)" % modo, out)
        if not mm:
            # ⚠ la CAUSA, non solo il fatto: un FAIL che non dice perche' fa cercare nel posto
            #   sbagliato -- e' successo, ed e' costato un giro.
            _coda = out.strip()[-600:].replace(os.linesep, os.linesep + "      ")
            esiti.append(("P5%s" % modo, False,
                          "nessuno stop -- ECCO PERCHE':" + os.linesep + "      " + _coda))
            continue
        nsub = int(mm.group(2)); pmin = float(mm.group(5)); salv = int(mm.group(6))
        ok = nsub < 100 and pmin >= 0.0
        esiti.append(("P5%s" % modo, ok,
                      "passo %s: nsub = %d (era 22591), min(peq) = %.4e, salvati dall'Eulero = %d"
                      % (mm.group(1), nsub, pmin, salv)))

    print("\n" + "-" * 90)
    for nome, ok, testo in esiti:
        print("%-5s %-4s %s" % (nome, "PASS" if ok else "FAIL", testo))
    print("-" * 90)
    n_ok = sum(1 for _, ok, _ in esiti if ok)
    print("SIGILLO PEQ_ESATTO: %d/%d" % (n_ok, len(esiti)))
    print("")
    if n_ok == len(esiti):
        print("VERDETTO: la cura C1 e' INERTE a flag spento, si riduce all'Eulero come O(x^2),")
        print("  tiene `peq >= 0`, NON e' codice morto, e SUL PASSO VERO il picco NON SI FORMA.")
    else:
        print("VERDETTO: *** BLOCCANTE: la cura C1 non si accende. ***")
    print("")
    print("LIMITI: UN seme, UNA scena. P3 gira %d passi; P5 una sola finestra del ramo D." % PASSI)
    print("  Prova che la cura fa cio' che dichiara, NON che la fisica risultante sia migliore.")
    return 0 if n_ok == len(esiti) else 1


if __name__ == "__main__":
    sys.exit(main())
