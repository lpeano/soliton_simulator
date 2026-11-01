# -*- coding: utf-8 -*-
r"""**LA SUITE AL BIT** *(il mandato di Luca delle `16:52` del `2026-11-01`, `S1` e la moneta nel nucleo; il task history `doc/TASK_HISTORY/2026-11-01_s1_e_moneta_nel_nucleo.md`)*:
### **ogni collaudo di `primo_ordine/collauda.COLLAUDI`, uno alla volta; l'uscita senza le righe dei tempi e dei timbri, il suo `sha1` e il codice d'uscita.**
### **Con `--forma S3`** il collaudo gira dopo `materia_vuoto.scegli("S3")`, nello stesso processo *(`runpy`)*: **l'opzione esplicita per riprodurre il vecchio.**

    python csv/_suite_al_bit.py --gira prima                 # il riferimento, sul nucleo di prima
    python csv/_suite_al_bit.py --gira dopo_S3 --forma S3    # dopo, con S3 esplicita
    python csv/_suite_al_bit.py --gira dopo_S1               # dopo, col predefinito
    python csv/_suite_al_bit.py --confronta prima dopo_S3    # collaudo per collaudo, e le righe diverse

### **Le uscite intere** in `db/suite_al_bit/<etichetta>/` *(non si committano: si rifanno col comando)*; **gli `sha1`** in `doc/referti_l2/s1_e_moneta_nel_nucleo/<etichetta>.json`.
"""
import difflib
import hashlib
import json
import os
import re
import subprocess
import sys
import time

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
_PO = os.path.join(RADICE, "primo_ordine")
for _p in (_QUI, _PO):
    if _p not in sys.path:
        sys.path.insert(0, _p)

DIR_JSON = os.path.join(RADICE, "doc", "referti_l2", "s1_e_moneta_nel_nucleo")
DIR_DB = os.path.join(RADICE, "db", "suite_al_bit")
# ### le righe che cambiano senza che cambi la fisica: i tempi e i timbri dei blob (un collaudo il cui file cambia ha un timbro nuovo)
TEMPO = re.compile(r"(\d+(\.\d+)?\s?(s|ms|sec|secondi)\b)|perf_counter|\[TIMBRO\]|SOLITON_DRIVER")
BOOT = ("import sys, os, runpy; sys.path.insert(0, os.path.join(os.getcwd(), 'primo_ordine')); import materia_vuoto as MV; MV.scegli(sys.argv[1]); "
        "sys.argv = sys.argv[2:]; sys.path.insert(0, os.path.dirname(os.path.abspath(sys.argv[0]))); runpy.run_path(sys.argv[0], run_name='__main__')")


def pulita(u):
    tolte = [r for r in u.splitlines() if TEMPO.search(r)]
    resto = [r for r in u.splitlines() if not TEMPO.search(r)]
    return "\n".join(resto) + "\n", len(tolte)


def gira(etichetta, forma):
    import collauda as C
    fj = os.path.join(DIR_JSON, etichetta + ".json")
    assert not os.path.exists(fj), fj
    d = os.path.join(DIR_DB, etichetta)
    os.makedirs(d, exist_ok=True)
    os.makedirs(DIR_JSON, exist_ok=True)
    out = {"etichetta": etichetta, "forma": forma, "collaudi": []}
    print("LA SUITE AL BIT: %s%s; %d collaudi" % (etichetta, (", la forma scelta esplicitamente: %s" % forma) if forma else ", il predefinito", len(C.COLLAUDI)))
    for i, (nome, cmd, dove) in enumerate(C.COLLAUDI):
        pezzi = cmd.split()
        arg = [sys.executable] + (["-c", BOOT, forma] if forma else []) + pezzi
        t0 = time.perf_counter()
        r = subprocess.run(arg, cwd=RADICE, capture_output=True)
        sec = time.perf_counter() - t0
        u = ((r.stdout or b"") + (r.stderr or b"")).decode("utf-8", "replace").replace("\r\n", "\n")
        p, tolte = pulita(u)
        with open(os.path.join(d, "%02d.txt" % i), "w", encoding="utf-8", newline="\n") as f:
            f.write(p)
        out["collaudi"].append({"i": i, "nome": nome, "cmd": cmd, "dove": dove, "rc": r.returncode, "sha1": hashlib.sha1(p.encode("utf-8")).hexdigest(),
                                "righe": p.count("\n"), "tolte": tolte})
        print("  %2d %-40s rc %d  %s  (%d righe, %d tolte; %.0f s)" % (i, nome[:40], r.returncode, out["collaudi"][-1]["sha1"][:10], p.count("\n"), tolte, sec))
        sys.stdout.flush()
    with open(fj, "w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(out, ensure_ascii=False, indent=1) + "\n")
    print("FINE: %d collaudi, %d con rc 0" % (len(out["collaudi"]), sum(c["rc"] == 0 for c in out["collaudi"])))


def confronta(a, b):
    ja = json.load(open(os.path.join(DIR_JSON, a + ".json"), encoding="utf-8"))
    jb = json.load(open(os.path.join(DIR_JSON, b + ".json"), encoding="utf-8"))
    ca = {c["cmd"]: c for c in ja["collaudi"]}
    cb = {c["cmd"]: c for c in jb["collaudi"]}
    print("IL CONFRONTO: %s (%s) contro %s (%s)" % (a, ja["forma"] or "predefinito", b, jb["forma"] or "predefinito"))
    uguali, diversi = 0, []
    for cmd in ca:
        x, y = ca[cmd], cb.get(cmd)
        if y is None:
            diversi.append(cmd)
            print("  ### %s: MANCA in %s" % (x["nome"], b))
            continue
        if x["sha1"] == y["sha1"] and x["rc"] == y["rc"]:
            uguali += 1
            continue
        diversi.append(cmd)
        print("  ### %-40s rc %d -> %d; le righe diverse:" % (x["nome"][:40], x["rc"], y["rc"]))
        ta = open(os.path.join(DIR_DB, a, "%02d.txt" % x["i"]), encoding="utf-8").read().splitlines()
        tb = open(os.path.join(DIR_DB, b, "%02d.txt" % y["i"]), encoding="utf-8").read().splitlines()
        for r in list(difflib.unified_diff(ta, tb, lineterm="", n=0))[2:40]:
            print("      %s" % r[:220])
    print("ESITO: %d collaudi uguali al bit, %d diversi%s" % (uguali, len(diversi), (": " + "; ".join(ca[c]["nome"] for c in diversi if c in ca)) if diversi else ""))
    return 0 if not diversi else 1


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    if "--gira" in argv:
        e = argv[argv.index("--gira") + 1]
        f = argv[argv.index("--forma") + 1] if "--forma" in argv else None
        gira(e, f)
        return 0
    if "--confronta" in argv:
        k = argv.index("--confronta")
        return confronta(argv[k + 1], argv[k + 2])
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
