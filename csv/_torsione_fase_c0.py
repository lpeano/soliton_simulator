# -*- coding: utf-8 -*-
r"""**LA DEVE `(0)` DELLA TORSIONE IN FASE, CORRETTA DOPO I NUMERI** *([[TORSIONE-DEL-VUOTO]]; la risposta di Luca delle `17:51`)*: ### **«al bit» diventa
«entro `1e-12` relativo»** *(relativo a `2 pi`, il quanto della torsione: dichiarato)*, ### **rivalutata sul jsonl di `csv/_torsione_del_vuoto.py`** *(`0c60cc94`)*;
### **e l'esito della misura in fase: NON LEGGIBILE** *(la guardia `g`)*. ### **Nessuna corsa nuova.**

Gira con:  python csv/_torsione_fase_c0.py > doc/referti_l2/torsione_fase_c0.txt
"""
import io
import json
import math
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
for _p in (_QUI, os.path.join(RADICE, "primo_ordine")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

RIF = os.path.join(RADICE, "doc", "referti_l2", "torsione_del_vuoto.jsonl")
TOLL_REL = 1e-12               # ### la correzione di Luca (`17:51`)
SCALA = 2 * math.pi            # ### relativo al quanto della torsione: dichiarato
GUARDIA = math.pi / 2


def main(argv):
    del argv
    import _presidio
    import _universalita_massa as UM
    _presidio.avvia(__file__)
    print("=" * 130)
    print("LA DEVE (0) DELLA TORSIONE IN FASE, CORRETTA DOPO I NUMERI (Luca, 17:51): ENTRO 1e-12 RELATIVO A 2 pi; E L'ESITO DELLA MISURA IN FASE")
    print("=" * 130)
    blobs = {p: UM.blob(p) for p in ("csv/_torsione_fase_c0.py", "csv/_torsione_del_vuoto.py", "doc/referti_l2/torsione_del_vuoto.jsonl")}
    print("  i blob nel repo: %s" % "; ".join("%s %s" % (k, v["sha1-BYTE"]) for k, v in blobs.items()))
    print("  la configurazione: TOLL_REL %g SCALA 2 pi = %.12f GUARDIA %.6f" % (TOLL_REL, SCALA, GUARDIA))
    print("  ### LA CORREZIONE, DICHIARATA DOPO I NUMERI: la convenzione simmetrica aggiunge operazioni in virgola mobile; 'al bit' non e' il criterio giusto (Luca, 17:51)")
    print("-" * 130)
    righe = [json.loads(l) for l in io.open(RIF, encoding="utf-8")]
    testa = [r for r in righe if r.get("tipo") == "testata"][0]
    print("  il referto rivalutato: csv/_torsione_del_vuoto.py %s" % testa["blobs"]["csv/_torsione_del_vuoto.py"]["sha1-BYTE"])
    vu = [r for r in righe if r.get("tipo") == "vuoto"]
    ok = True
    for r in vu:
        x = r["max_theta"] / SCALA
        ok &= x <= TOLL_REL
        print("  il vuoto uniforme L %d cs %s: max |theta| %.3e = %.3e di 2 pi" % (r["L"], "acceso" if r["cs_acceso"] else "spento", r["max_theta"], x))
    print("  %-110s %s" % ("DEVE PASSARE (0'): il vuoto uniforme senza materia, la torsione entro %g relativo a 2 pi, cs spento e acceso" % TOLL_REL, "PASSA" if ok else "### FALLISCE"))
    print("-" * 130)
    cc = [r for r in righe if r.get("tipo") == "corsa"]
    leggibile = True
    for r in cc:
        leggibile &= r["d_max"] < GUARDIA
        print("  N %g L %d cs spento: l'incremento massimo per tick %.4f; %d archi oltre pi/2" % (r["N"], r["L"], r["d_max"], r["archi_oltre_guardia"]))
    print("### L'ESITO DELLA MISURA IN FASE: %s" % ("LEGGIBILE" if leggibile else "NON LEGGIBILE (gli incrementi a pi: lo srotolamento per tick non regge)"))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
