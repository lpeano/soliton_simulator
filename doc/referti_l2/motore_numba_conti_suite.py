# -*- coding: utf-8 -*-
r"""**I CONTI DELLA SUITE A SWITCH ACCESO** *(V4, Luca `2026-11-16` `13:58`)*: legge i `conti_<pid>.json` scritti dallo strumento `sitecustomize.py` *(fuori dal repo)*.

    E:\python\py3132\python.exe doc/referti_l2/motore_numba_conti_suite.py E:\python\numba_suite2 > doc/referti_l2/motore_numba_v4_conti.txt

**Per processo:** se il motore e' ACCESO, se l'accensione e' caduta *(l'errore)*, il secondo passo e il suo modo, le chiamate al ciclo numba, i ripieghi su numpy, i fili.
"""
import glob
import hashlib
import json
import os
import sys


def main(argv):
    d = argv[0]
    f_strum = os.path.join(d, "sitecustomize.py")
    print("=" * 130)
    print("I CONTI DELLA SUITE A SWITCH ACCESO (V4): la cartella %s; lo strumento sitecustomize.py sha1-BYTE %s" % (d, hashlib.sha1(open(f_strum, "rb").read()).hexdigest()[:8]))
    print("=" * 130)
    tutti = []
    for f in sorted(glob.glob(os.path.join(d, "conti_*.json"))):
        with open(f, encoding="utf-8") as h:
            tutti.append(json.load(h))
    accesi = [x for x in tutti if x.get("acceso")]
    errori = [x for x in tutti if x.get("errore")]
    due = [x for x in accesi if x.get("secondo_passo")]
    modi = sorted(set(str(x.get("fma")) for x in due))
    vie = sorted(set(str(x.get("via_fma")) for x in due))
    ch = sum(int(x.get("chiamate", 0)) for x in accesi)
    rip = sum(int(x.get("ripieghi", 0)) for x in accesi)
    print("### i processi %d; ACCESI %d (coi due passi %d; il modo %s; la via della FMA %s); l'accensione caduta %d; le chiamate al ciclo numba %d; i ripieghi su numpy %d"
          % (len(tutti), len(accesi), len(due), modi, vie, len(errori), ch, rip))
    for x in accesi:
        a = x.get("argv") or ["?"]
        print("    ACCESO  %-60s le chiamate %d, i ripieghi %d, i fili %s, il secondo passo %s (%s, %s)" % (os.path.relpath(a[0]) if os.path.isabs(a[0]) else a[0], int(x.get("chiamate", 0)), int(x.get("ripieghi", 0)),
                                                                                                   x.get("fili"), x.get("secondo_passo"), x.get("fma"), x.get("via_fma")))
    for x in errori:
        print("    ### CADUTA  %s: %s" % ((x.get("argv") or ["?"])[0], x.get("errore")))
    print("=" * 130)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
