# -*- coding: utf-8 -*-
r"""**IL FILM PARZIALE: LE NASCITE E I LORO ANELLI** *(Luca `2026-11-21` `20:35`, il film parziale; solo lettura)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/mitosi_film_anelli.py --base <cartella con MITOSI/> --out doc/referti_l2/mitosi_film_parziale

**Legge, non tocca:** l'ultimo `nascite_<k>.json` di `<base>/MITOSI` *(i bilanci di `mitosi_rami.Rami.nasci`: `r` = il raggio del nodo nato dal centro delle misure, `passi` = la sua distanza in passi dalla sorgente)*. **Scrive** `<out>/anelli.json`: il numero delle nascite e per ognuna `tick`, `n`, `r`, **l'anello `round(r)`**, i passi; e lo stampa, col conteggio per anello.
"""
import argparse
import glob
import json
import os
import sys
from collections import Counter


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True)
    ap.add_argument("--out", required=True)
    x = ap.parse_args(argv)
    fs = sorted(glob.glob(os.path.join(x.base, "MITOSI", "nascite_*.json")))
    assert fs, "nessun nascite_<k>.json in %s" % os.path.join(x.base, "MITOSI")
    with open(fs[-1], encoding="utf-8") as fh:
        B = json.load(fh)
    righe = [{"tick": b["k"], "n": b["nodi"]["n"], "r": b["r"], "anello": int(round(b["r"])), "passi": b["passi"]} for b in B]
    conta = Counter(r["anello"] for r in righe)
    os.makedirs(x.out, exist_ok=True)
    with open(os.path.join(x.out, "anelli.json"), "w", encoding="utf-8") as fh:
        json.dump({"da": os.path.basename(fs[-1]), "nascite": len(righe), "per_anello": {str(a): c for a, c in sorted(conta.items())}, "righe": righe}, fh, indent=0)
    print("### dal file %s: %d nascite" % (os.path.basename(fs[-1]), len(righe)))
    for r in righe:
        print("    k %d  n %d  r %.3f  l'anello %d  %d passi" % (r["tick"], r["n"], r["r"], r["anello"], r["passi"]))
    print("### per anello: %s" % ", ".join("%d: %d" % (a, c) for a, c in sorted(conta.items())))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
