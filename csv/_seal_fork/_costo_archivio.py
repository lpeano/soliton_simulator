# -*- coding: utf-8 -*-
"""COSTO dell'archivio, MISURATO su uno snapshot VERO. Due domande, un solo file aperto.

DOMANDA 1 (serve ADESSO, decide la CORREZIONE di D2)
  Il mandato chiede di controllare il BLOB di TUTTI gli snapshot della serie, e avverte: "puo'
  essere caro se sono molti; se lo e', PROPONI invece di lasciare il controllo incompleto".
  Leggere il blob oggi significa `pickle.load` dell'INTERO snapshot: il blob e' una chiave del
  dizionario, e un dizionario non si legge a meta'. QUINDI IL COSTO DELLA SCANSIONE E' N * t_load.
  Questo script misura `t_load`. NON decide: PORTA IL NUMERO.

DOMANDA 2 (e' V8, anticipato perche' il file e' gia' aperto)
  Quanto comprime `gzip` su questi dati, e quanto costa. Il task history dice "si MISURA, non si
  stima", e il riferimento e' i 26.45 MB non compressi dello snapshot del pilota (24add7d).
  ATTENZIONE: questo NON e' V8 completo. V8 vero deve misurare l'overhead PER PASSO dentro un run,
  cioe' quanto rallenta la simulazione. Qui si misura il costo di UNA scrittura e di UNA lettura,
  su UN file. E' un limite inferiore onesto, non il costo di campagna.

PERCHE' SI MISURANO I LIVELLI DI COMPRESSIONE
  `gzip.open(..., 'wb')` usa `compresslevel=9` DI DEFAULT, che e' il piu' LENTO. L'implementazione
  committata usa proprio quel default. Se 9 costasse troppo, il rimedio non e' rinunciare a gzip:
  e' scegliere un livello -- ma un livello e' UN NUMERO SCELTO (par.3), quindi va MISURATO e
  PROPOSTO a Luca, non deciso qui dentro.

NON TOCCA NULLA: legge uno snapshot esistente in sola lettura, scrive in una cartella TEMPORANEA
che rimuove alla fine, e non importa il simulatore (non serve: `pickle` basta, e cosi' la misura
non dipende dal blob corrente).
ASCII PURO.
"""
import gzip
import os
import pickle
import shutil
import statistics
import sys
import tempfile
import time

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
SNAP = os.path.join(RADICE, "csv", "_test_fork", "_pilota6000", "pilota.pkl")
RIPETIZIONI = 3
LIVELLI = [1, 6, 9]
# le cadenze con cui una serie viene davvero scritta, per tradurre t_load in costo di AVVIO
SERIE_ATTESE = [(6000, 250), (6000, 50), (2400, 10)]


def mediana_tempo(fn, n=RIPETIZIONI):
    t = []
    for _ in range(n):
        t0 = time.perf_counter()
        fn()
        t.append(time.perf_counter() - t0)
    return statistics.median(t), min(t), max(t)


def main():
    if not os.path.exists(SNAP):
        print("SNAPSHOT ASSENTE: %s" % SNAP)
        print("Senza uno snapshot VERO questa misura non si fa: stimare la compressione di")
        print("float64 densi senza guardarli e' esattamente cio' che il task history vieta.")
        return 2

    mb = os.path.getsize(SNAP) / 1e6
    print("snapshot: %s" % os.path.relpath(SNAP, RADICE))
    print("dimensione NON compressa: %.2f MB" % mb)
    print("")

    # --- DOMANDA 1: quanto costa LEGGERE il blob di uno snapshot ------------------------
    def _load():
        with open(SNAP, "rb") as fh:
            return pickle.load(fh)

    t_load, lo, hi = mediana_tempo(_load)
    stato = _load()
    print("LETTURA (pickle.load, non compresso): %.3f s  [min %.3f, max %.3f]" % (t_load, lo, hi))
    print("  chiavi di testa: %s" % list(stato.keys())[:6])
    print("  blob nel file: %r   _db_step: %r"
          % (stato.get("blob"), (stato.get("attrs") or {}).get("_db_step")))
    print("")
    print("COSTO DELLA SCANSIONE COMPLETA = N * t_load  (il blob e' una CHIAVE di un dizionario:")
    print("un dizionario non si legge a meta', quindi oggi non c'e' modo di leggerlo piu' in fretta)")
    for passi, ogni in SERIE_ATTESE:
        n = passi // ogni
        print("   serie %5d passi @ ogni %3d -> %4d snapshot -> %7.1f s di SOLO CONTROLLO all'avvio"
              % (passi, ogni, n, n * t_load))
    print("")

    # --- DOMANDA 2 (V8 parziale): gzip ---------------------------------------------------
    tmp = tempfile.mkdtemp(prefix="costoarch_")
    try:
        dst = os.path.join(tmp, "x.pkl")

        def _dump_piano():
            with open(dst, "wb") as fh:
                pickle.dump(stato, fh, protocol=pickle.HIGHEST_PROTOCOL)

        t_piano, _, _ = mediana_tempo(_dump_piano)
        mb_piano = os.path.getsize(dst) / 1e6
        print("SCRITTURA non compressa: %.3f s  ->  %.2f MB" % (t_piano, mb_piano))
        print("")
        print("%-8s %10s %10s %10s %10s" % ("livello", "scrittura", "dimens.", "rapporto", "lettura"))
        for lv in LIVELLI:
            dgz = os.path.join(tmp, "x_%d.pkl.gz" % lv)

            def _dump_gz():
                with gzip.open(dgz, "wb", compresslevel=lv) as fh:
                    pickle.dump(stato, fh, protocol=pickle.HIGHEST_PROTOCOL)

            t_gz, _, _ = mediana_tempo(_dump_gz, n=1 if lv == 9 else RIPETIZIONI)
            mb_gz = os.path.getsize(dgz) / 1e6

            def _load_gz():
                with gzip.open(dgz, "rb") as fh:
                    return pickle.load(fh)

            t_lgz, _, _ = mediana_tempo(_load_gz, n=1)
            print("%-8d %9.2fs %9.2fMB %9.3fx %9.2fs"
                  % (lv, t_gz, mb_gz, mb_piano / mb_gz if mb_gz else float("nan"), t_lgz))
        print("")
        print("NB: l'implementazione committata usa gzip.open SENZA compresslevel, cioe' il")
        print("DEFAULT 9 -- la riga piu' lenta della tabella.")
        print("NB: lettura a livello 9 misurata UNA volta sola (n=1) per non spendere: e' un")
        print("    numero piu' rumoroso degli altri, e va letto come tale.")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
