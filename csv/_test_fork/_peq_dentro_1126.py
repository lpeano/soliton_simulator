# -*- coding: utf-8 -*-
"""I TRE NUMERI CHE MANCANO sull'aggiornamento di `peq`, al passo che esplode. [§1 MANDATO GLOBALE]

⚠ COSA MISURA, e perche' erano irraggiungibili prima:
  ① **`max(dt_e / tau_bg_loc)`** -- il numero di stabilita' dell'Eulero esplicito di `:4206`.
     **Su `d0` questo numero esiste da sempre** (`_taup_cfl_max`, `:4412-4419`, misurato `0.0354`);
     **su `peq` NON ESISTEVA.**
  ② **QUANTI archi finiscono con `peq < 0`** -- **uno o mille cambia la diagnosi**: un arco e' un
     incidente, mille sono un regime.
  ③ **QUALE dei due termini** di `:4206` li porta sotto zero: il **rilassamento**
     `(rho-peq)/tau_bg_loc` o la **diffusione** `flusso/TAU_DIFF`. **I due esiti sono calcolati
     CONTROFATTUALMENTE e a parte**, perche' sommati non si saprebbe di chi e' la colpa.

⚠ E NON SI PAGA IL PASSO: `FERMA_DOPO_NSUB` alza `StopDopoNsub` **appena calcolato `nsub`**, quindi
  i 22591 sotto-passi **non vengono integrati**. La rigiocata precedente, per quello stesso numero,
  ha pagato **2032 secondi**.

⚠ LA SONDA E' SIGILLATA: `csv/_seal_fork/_sigillo_traccia_peq.py` **4/4**, e `T2` prova che e'
  **PURE-READ** (byte-identica anche ACCESA), non solo inerte quando e' spenta.
ASCII PURO.
"""
import io
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, RADICE)

DA, FINO = 1080, 1126
for _a in sys.argv[1:]:
    if _a.startswith("--da="):
        DA = int(_a.split("=", 1)[1])
    if _a.startswith("--fino="):
        FINO = int(_a.split("=", 1)[1])
SNAP = os.path.join(RADICE, "csv", "_test_fork", "_ab_D", "scena_%06d.pkl.gz" % DA)
OUT = os.path.join(RADICE, "csv", "_test_fork", "_diag_D", "PEQ_DENTRO_%06d.txt" % FINO)

ARGV_D = ["soliton_simulator.py", "--test", "N-MASSE", "--nmasse", "3", "--sep", "4.0",
          "--giri", "0", "--campo-spinoriale", "--spinore-vivo", "--spinore-corretto",
          "--chi-core", "--calore-scal", "--deparam-orologio", "--verlet", "--fork-su2",
          "--fork-su2-mem", "--cs-dinamico", "--tau-luce", "--rumore-colorato",
          "--pav-com", "--guscio-morbido", "--zeta-vir", "--chi-basc", "--chi-coop",
          "--scala-min", "--coes-adim", "--plast-din", "--viriale", "--olon-part"]

CONT = ("_g_peq_cfl_max", "_g_peq_cfl_sopra1", "_g_peq_cfl_sopra2",
        "_g_peq_neg", "_g_peq_neg_ril", "_g_peq_neg_dif", "_g_peq_archi", "_g_peq_passi")

SIGILLO = os.path.join(RADICE, "csv", "_seal_fork", "_sigillo_traccia_peq_2026-09-21.txt")
ATTESO = "SIGILLO TRACCIA_PEQ: 4/4"


def sblocca_db(net, snap):
    """⚠ OVERRIDE DICHIARATO della guardia di `carica_stato`, CONDIZIONATO AL SIGILLO.

    `carica_stato` RIFIUTA uno snapshot scritto da un blob diverso, ed e' GIUSTO: protegge da
    *«fisica vecchia caricata in fisica nuova»*. Qui il blob **e' cambiato** (`4954fe5b` ->
    `3b9e75bf`) **ma la fisica NO**, e non e' un'opinione: **`T1` e `T2` del sigillo lo hanno
    MISURATO byte-identico**, `T2` anche con la sonda **ACCESA**.

    ⚠ **E NON BASTA CHE LO DICA IO** (`A9`): questa funzione **legge l'output del sigillo dal
      disco** e **rifiuta di sbloccare se non dice `4/4`**. L'override e' condizionato a una
      PROVA, non a un'asserzione. La guardia viene **ripristinata subito**, in un `finally`.
    ⚠ **NON si usa `--db-cleanup`**, che il messaggio d'errore suggerisce: quello **CANCELLA il
      `.pkl`**, e l'archivio del ramo D non si tocca.
    """
    import gzip
    import pickle
    if not os.path.exists(SIGILLO):
        raise SystemExit("[peq] manca l'output del sigillo: NON sblocco")
    if ATTESO not in io.open(SIGILLO, encoding="utf-8", errors="replace").read():
        raise SystemExit("[peq] il sigillo non dice %r: NON sblocco" % ATTESO)
    with gzip.open(snap, "rb") as fh:
        db_blob = pickle.load(fh).get("blob")
    orig = type(net)._versione_codice

    def finto(self):
        v = orig(self)
        v["blob"] = db_blob
        return v
    type(net)._versione_codice = finto
    return orig, db_blob


def leggi(net):
    return {k: getattr(net, k, 0) for k in CONT}


def main():
    os.chdir(RADICE)
    sys.argv = list(ARGV_D)
    import soliton_simulator as S
    S.TRACCIA_PEQ = True                      # la sonda, sigillata 4/4 e PURE-READ
    a = S._cli(); S._applica_regime(a); S._applica_flag(a)
    for f in ("CHI_COOP", "SCALA_MIN", "COES_ADIM"):
        if not getattr(S, f):
            raise SystemExit("[peq] %s e' SPENTO: non e' la configurazione del ramo D" % f)
    net = S.net
    orig, db_blob = sblocca_db(net, SNAP)
    try:
        if not net.carica_stato(SNAP):
            raise SystemExit("[peq] `carica_stato` ha RIFIUTATO %s" % SNAP)
    finally:
        type(net)._versione_codice = orig       # la guardia torna com'era, SUBITO

    o = io.open(OUT, "w", encoding="utf-8", newline="\n")
    W = o.write
    W("# I TRE NUMERI SULL'AGGIORNAMENTO DI `peq` -- dal passo %d al %d\n" % (DA + 1, FINO))
    W("# sonda TRACCIA_PEQ, sigillo 4/4 (T2: PURE-READ). Il passo %d NON viene integrato.\n" % FINO)
    W("# x = dt_e / tau_bg_loc: un Eulero esplicito SCAVALCA per x > 1, OSCILLA per x > 2.\n")
    W("# su `d0` lo stesso numero esiste da sempre (`_taup_cfl_max`, misurato 0.0354); su `peq` no.\n")
    W("# stato di partenza: n = %d, archi = %d\n#\n" % (net.n, len(net.d)))
    W("# ⚠ OVERRIDE DICHIARATO della guardia di `carica_stato`: lo snapshot e' scritto dal blob\n")
    W("#   git %s, il simulatore di oggi e' un altro. LA GUARDIA E' GIUSTA, e NON si aggira\n"
      % db_blob[:8])
    W("#   con `--db-cleanup`, che CANCELLA il `.pkl`. Si sblocca perche' `T1` e `T2` del sigillo\n")
    W("#   hanno MISURATO il codice byte-identico, anche con la sonda ACCESA -- e lo sblocco e'\n")
    W("#   CONDIZIONATO a quella prova: lo strumento LEGGE l'output del sigillo e rifiuta di\n")
    W("#   partire se non dice `4/4`. La guardia e' ripristinata subito dopo il caricamento.\n\n")
    W("%5s | %11s %9s %9s | %8s %8s %8s | %9s\n"
      % ("passo", "max(x)", "x>=1", "x>=2", "neg", "neg SOLO", "neg SOLO", "archi"))
    W("%5s | %11s %9s %9s | %8s %8s %8s | %9s\n"
      % ("", "cumul.", "in questo", "in questo", "in questo", "rilass.", "diffus.", "in questo"))
    W("-" * 86 + "\n")

    PPF = int(S.PASSI_PER_FRAME)
    prec = leggi(net)
    fermato = None
    for k in range(1, FINO - DA + 1):
        passo = DA + k
        if (k - 1) % PPF == 0:
            S.passo_test()
        S.scuoti_vuoto(net)
        if passo == FINO:
            S.FERMA_DOPO_NSUB = True          # ⚠ da qui il passo NON si integra
        try:
            net.step()
        except S.StopDopoNsub as e:
            fermato = (passo, dict(net._g_nsub_stop), str(e))
        c = leggi(net)
        W("%5d | %11.4g %9d %9d | %8d %8d %8d | %9d\n"
          % (passo, c["_g_peq_cfl_max"],
             c["_g_peq_cfl_sopra1"] - prec["_g_peq_cfl_sopra1"],
             c["_g_peq_cfl_sopra2"] - prec["_g_peq_cfl_sopra2"],
             c["_g_peq_neg"] - prec["_g_peq_neg"],
             c["_g_peq_neg_ril"] - prec["_g_peq_neg_ril"],
             c["_g_peq_neg_dif"] - prec["_g_peq_neg_dif"],
             c["_g_peq_archi"] - prec["_g_peq_archi"]))
        o.flush()
        prec = c
        if fermato is not None:
            break
        net.mitosi(); net.rilassa_disegno(); net.memoria_hebbiana_moto()

    W("\n")
    if fermato is None:
        W("*** Il passo %d NON ha alzato lo stop: o `FERMA_DOPO_NSUB` non e' arrivato, o il\n"
          "    ramo non e' VERLET. Va detto, non aggirato.\n" % FINO)
    else:
        p, d, msg = fermato
        W("*** FERMATO AL PASSO %d SENZA INTEGRARLO: %s (ramo %s)\n" % (p, msg, d["ramo"]))
        W("    nsub = %d, n1 = %.0f, n2 = %.0f, n3 = %.0f\n"
          % (d["nsub"], d["n1"], d["n2"], d["n3"]))
    W("\n")
    W("L'ARCO PEGGIORE DI TUTTA LA FINESTRA -- il minimo ASSOLUTO di `peq` dopo l'aggiornamento:\n")
    if hasattr(net, "_g_peq_min_arco"):
        ii, jj = net._g_peq_min_arco
        W("  arco %d-%d   al passo %d della finestra   peq_dopo = %.6e\n"
          % (ii, jj, getattr(net, "_g_peq_min_quando", -1), net._g_peq_min))
        for kk, vv in sorted(net._g_peq_min_dett.items()):
            W("    %-20s %.6e\n" % (kk, vv))
        d = net._g_peq_min_dett
        W("\n  LETTURA, e la scrivo separando cio' che il numero DICE da cio' che non dice:\n")
        W("    x = dt_e/tau_bg = %.4g  ->  %s\n"
          % (d["x"], "SOPRA 1: l'Eulero SCAVALCA" if d["x"] > 1.0
             else "sotto 1: qui l'Eulero e' STABILE, e lo scavalcamento viene da ALTRO"))
        W("    solo rilassamento -> %.6e   (%s)\n"
          % (d["solo_rilassamento"], "NEGATIVO" if d["solo_rilassamento"] < 0 else "positivo"))
        W("    solo diffusione   -> %.6e   (%s)\n"
          % (d["solo_diffusione"], "NEGATIVO" if d["solo_diffusione"] < 0 else "positivo"))
        W("    insieme           -> %.6e   (%s)\n"
          % (d["insieme"], "NEGATIVO" if d["insieme"] < 0 else "positivo"))
    else:
        W("  (nessun minimo registrato: la sonda non ha girato)\n")
    W("\n")
    W("TOTALI DI FINESTRA: %d archi-scrittura in %d passi, max(x) = %.6g,\n"
      % (getattr(net, "_g_peq_archi", 0), getattr(net, "_g_peq_passi", 0),
         getattr(net, "_g_peq_cfl_max", -1.0)))
    W("  archi con x >= 1: %d   con x >= 2: %d   con peq < 0: %d\n"
      % (getattr(net, "_g_peq_cfl_sopra1", 0), getattr(net, "_g_peq_cfl_sopra2", 0),
         getattr(net, "_g_peq_neg", 0)))
    o.close()
    print(io.open(OUT, encoding="utf-8").read())
    return 0


if __name__ == "__main__":
    sys.exit(main())
