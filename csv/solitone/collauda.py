# -*- coding: utf-8 -*-
r"""**IL COLLAUDO DELLA CASSETTA DEGLI ATTREZZI DEL SOLITONE** *(il task history `doc/TASK_HISTORY/2026-11-01_cassetta_solitone.md`)*: ### **i test dei tre moduli, coi tempi.**

    python csv/solitone/collauda.py > doc/referti_l2/cassetta_solitone.txt
"""
import os
import sys
import time

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))

import solitone  # noqa: E402,F401  (i percorsi)

OK = [0, 0]
FALLITE = []


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    if not passa:
        FALLITE.append(che)
    print("  %-130s %s   %s" % (che[:130], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return passa


PRIMA_ALLINEAMENTO = "9180fd38"     # ### l'ultimo commit prima dell'allineamento del mandato delle 01:28 (punto 6)
REFERTI_VECCHI = (("eps 0", "csv/_livelli_piatti.py", "doc/referti_l2/livelli_piatti.txt"), ("eps 0.5", "csv/_massimo_di_B.py", "doc/referti_l2/massimo_di_B.txt"),
                  ("A a K", "csv/_coppia_di_B.py", "doc/referti_l2/coppia_di_B.txt"))


# ### ⛔ **D6 RISCRITTO** *(Luca, `S1` nel nucleo, la chiusura)*: il nucleo e' cambiato *(`c7ad2238`, e la chiusura)*, quindi «nessun `.py` fuori
# ### dalla libreria cambiato» non puo' piu' valere, e i referti vecchi si rigirano AL LORO COMMIT. ### **Il controllo diventa: nessun `.py` della
# ### libreria cambiato** da `LIBRERIA_RIFERITA`, l'ultimo commit in cui i `32` test e `D5` hanno dato i numeri al bit col predefinito `S1`.
# ### ⚠ **`collauda.py` si esclude, dichiarato:** e' il collaudo, non la libreria *(e la chiusura lo cambia)*.
# ### **Dall'unita' `e_K`** *(Luca, dopo `6052a2b4`)*: la libreria cambia per mandato *(`protetto.legame_spento`, `protetto.e_K`, `P3`)*, e
# ### `LIBRERIA_RIFERITA` e' il suo commit, `3d5fe03a` *(prima `3fe2f12d`)*.
# ### **Dal solitone vestito** *(Luca `2026-11-02` `01:04`, passo `2`)*: la libreria aggiunge `vuoto.py`, `test_vuoto.py`, `carta_vuoto.py` *(`ae4640ee`)*.
# ### **Dalla carta completata col respiro** *(Luca dopo `25614c34`, punto `3`)*: `respiro.py`, `test_respiro.py`, `carta_respiro.py` *(`2f3e93f8`)*.
LIBRERIA_RIFERITA = "2f3e93f8"


def vecchi():
    """### **D6** *(riscritto)*: **nessun `.py` della libreria cambiato** da `LIBRERIA_RIFERITA` *(escluso questo collaudo)*, niente di non committato
    nella libreria, e nessuno script fuori da `csv/solitone/` importa la libreria. ### **I tre referti vecchi si rigirano al loro commit:** il nucleo e'
    cambiato da `PRIMA_ALLINEAMENTO`, e a `HEAD` non sono piu' garantiti."""
    import subprocess
    print("### D6: LA LIBRERIA E' QUELLA DI %s (escluso collauda.py); i tre referti vecchi (%s) si rigirano al loro commit"
          % (LIBRERIA_RIFERITA, "; ".join("%s: %s -> %s" % r for r in REFERTI_VECCHI)))
    rad = solitone.RADICE
    lib = "csv/solitone/"
    escluso = lib + "collauda.py"
    cambiati = subprocess.check_output(["git", "diff", "--name-only", LIBRERIA_RIFERITA, "HEAD", "--", lib + "*.py"], cwd=rad).decode().split()
    sporchi = subprocess.check_output(["git", "status", "--porcelain", "--", lib + "*.py"], cwd=rad).decode().splitlines()
    cambiati = [f for f in cambiati if f != escluso]
    sporchi = [x for x in sporchi if x.strip() and not x.strip().endswith(escluso)]
    importano = []
    for cart in ("csv", "primo_ordine"):
        for d, _s, ff in os.walk(os.path.join(rad, cart)):
            if os.path.join("csv", "solitone") in d:
                continue
            for f in ff:
                if f.endswith(".py"):
                    with open(os.path.join(d, f), encoding="utf-8", errors="replace") as fh:
                        tt = fh.read()
                    if "import solitone" in tt or "from solitone" in tt:
                        importano.append(os.path.join(d, f))
    esito("DEVE PASSARE: D6 nessun .py della libreria cambiato da %s a HEAD (escluso collauda.py), e niente di non committato" % LIBRERIA_RIFERITA,
          not cambiati and not sporchi, "cambiati %s, non committati %s" % (cambiati or "nessuno", sporchi or "nessuno"))
    esito("DEVE PASSARE: D6 nessuno script fuori da csv/solitone/ importa la libreria", not importano, "%s" % importano)
    fuori = subprocess.check_output(["git", "diff", "--name-only", PRIMA_ALLINEAMENTO, "HEAD", "--", "*.py"], cwd=rad).decode().split()
    print("    i .py fuori dalla libreria cambiati da %s: %d (il nucleo); i tre script vecchi:" % (PRIMA_ALLINEAMENTO, len([f for f in fuori if not f.startswith(lib)])))
    for _chi, scr, ref in REFERTI_VECCHI:
        print("    %s: il blob a %s e a HEAD %s" % (scr, PRIMA_ALLINEAMENTO, "uguali" if scr not in fuori else "### DIVERSI"))


def main():
    import _presidio
    for m in ("__init__", "uscite", "protetto", "misure", "vuoto", "respiro", "test_uscite", "test_protetto", "test_misure", "test_vuoto", "test_respiro"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(__file__)          # ### per ultimo: SOLITON_DRIVER resta quello del collaudo
    from solitone import test_misure, test_protetto, test_respiro, test_uscite, test_vuoto
    print("=" * 150)
    print("LA CASSETTA DEGLI ATTREZZI DEL SOLITONE (Luca 01:22): csv/solitone/ (uscite, protetto, misure); i test ridanno AL BIT i numeri gia' committati")
    print("  LE LETTURE DI LUCA, SCRITTE PRIMA: (t1) ogni modulo rida' al bit i numeri committati; (t2) un modulo non li rida': quale, perche'")
    print("=" * 150)
    tempi = {}
    s0 = time.time()
    test_uscite.gira(esito)
    tempi["uscite"] = time.time() - s0
    s0 = time.time()
    partenze = test_protetto.gira(esito)
    tempi["protetto"] = time.time() - s0
    s0 = time.time()
    test_misure.gira(esito, partenze)
    tempi["misure"] = time.time() - s0
    s0 = time.time()
    test_vuoto.gira(esito)
    tempi["vuoto"] = time.time() - s0
    s0 = time.time()
    test_respiro.gira(esito)
    tempi["respiro"] = time.time() - s0
    vecchi()
    print("-" * 150)
    print("  i tempi: %s" % "; ".join("%s %.0f s" % kv for kv in tempi.items()))
    print("ESITO: %d/%d controlli passano; fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    return 0 if OK[0] == OK[1] else 1


if __name__ == "__main__":
    sys.exit(main())
