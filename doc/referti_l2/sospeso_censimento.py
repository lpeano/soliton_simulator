# -*- coding: utf-8 -*-
r"""**IL CENSIMENTO PER LA PARTE `7` DI `doc/SOSPESO_2026-11-17_FILO_DELLA_RICERCA.md`** *(Luca `2026-11-17`: «dal repo, non a memoria»)*. **SOLA LETTURA:** nessuna voce, nessun ramo, nessun file cambiato.

    E:\python\py3132\python.exe doc/referti_l2/sospeso_censimento.py > doc/referti_l2/sospeso_censimento.txt

- **(7.3) L'INDICE** *(`doc/indice/voci.jsonl`)*: il conto per classe e stato; **l'elenco delle `APERTA` e `AGENDA` delle classi `DECISIONE`, `FRONTE`, `MISURA`, `DIFETTO`** *(l'id e il titolo)*.
- **(7.5) I RAMI SU ORIGIN** *(dopo un `git fetch`, fatto a mano prima)*: l'ultimo commit e la data; **se e' antenato di `origin/primo-ordine`** *(`git merge-base --is-ancestor`)*; i tag che puntano all'ultimo commit.
- **(7.6) LE CORSE E I LUCCHETTI:** le voci APERTE di ogni `doc/REGISTRO_CORSE.md` di ogni worktree *(la stessa regola di `_registro_corse.aperte`: un `APERTO` senza un `CHIUSO` dopo)*; i file di tappe NON chiusi in `E:\soliton_simulator\registro_tappe`; `index.lock` in ogni cartella git dei worktree; `commit.lock` accanto a `committa2.py` *(lo scratchpad, passato con `--lucchetto`)*.
"""
import argparse
import collections
import json
import os
import subprocess
import sys

QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(os.path.dirname(QUI))
CLASSI = ("DECISIONE", "FRONTE", "MISURA", "DIFETTO")
TAPPE = os.path.join("E:" + os.sep, "soliton_simulator", "registro_tappe")


def git(*a, cwd=RADICE):
    r = subprocess.run(["git"] + list(a), cwd=cwd, capture_output=True, text=True, encoding="utf-8")
    return r.returncode, r.stdout.strip()


def indice():
    V = [json.loads(l) for l in open(os.path.join(RADICE, "doc", "indice", "voci.jsonl"), encoding="utf-8") if l.strip()]
    c = collections.Counter((v["classe"], v["stato"]) for v in V)
    cl = sorted({k[0] for k in c})
    st = sorted({k[1] for k in c})
    print("=" * 130)
    print("(7.3) L'INDICE: %d voci (doc/indice/voci.jsonl); il conto per classe e stato" % len(V))
    print("    %-16s" % "classe" + "".join("%16s" % s for s in st) + "%10s" % "in tutto")
    for x in cl:
        print("    %-16s" % x + "".join("%16d" % c[(x, s)] for s in st) + "%10d" % sum(c[(x, s)] for s in st))
    print("    %-16s" % "IN TUTTO" + "".join("%16d" % sum(c[(x, s)] for x in cl) for s in st) + "%10d" % len(V))
    for x in CLASSI:
        for s in ("APERTA", "AGENDA"):
            L = sorted((v for v in V if v["classe"] == x and v["stato"] == s), key=lambda v: v["id"])
            print("-" * 130)
            print("### %s, %s: %d" % (x, s, len(L)))
            for v in L:
                print("    %-48s %s" % (v["id"], v["titolo"]))


def rami():
    print("=" * 130)
    _, out = git("for-each-ref", "--format=%(refname:short)", "refs/remotes/origin")
    R = [r for r in out.splitlines() if r != "origin/HEAD" and r != "origin"]
    print("(7.5) I RAMI SU ORIGIN: %d (l'ultimo commit; dentro origin/primo-ordine = antenato; i tag che puntano all'ultimo commit)" % len(R))
    print("    %-26s %-9s %-26s %-22s %s" % ("il ramo", "commit", "la data", "dentro primo-ordine", "i tag sull'ultimo commit"))
    for r in R:
        _, h = git("rev-parse", "--short=8", r)
        _, d = git("log", "-1", "--format=%ci", r)
        rc, _ = git("merge-base", "--is-ancestor", r, "origin/primo-ordine")
        _, tg = git("tag", "--points-at", r)
        print("    %-26s %-9s %-26s %-22s %s" % (r, h, d, "SI'" if rc == 0 else "NO", ", ".join(tg.split()) or "-"))
        if rc != 0:
            _, n = git("rev-list", "--count", "origin/primo-ordine.." + r)
            _, s = git("log", "-1", "--format=%s", r)
            print("        %s commit non in primo-ordine; l'ultimo: %s" % (n, s[:150]))


def aperte(f):
    ap = {}
    for l in open(f, encoding="utf-8", errors="replace"):
        if not l.startswith("- {"):
            continue
        try:
            e = json.loads(l[2:])
        except ValueError:
            continue
        if e.get("ev") == "APERTO":
            ap[e["nome"]] = e.get("ora")
        elif e.get("ev") == "CHIUSO":
            ap.pop(e.get("nome"), None)
    return ap


def corse(lucchetto):
    print("=" * 130)
    print("(7.6) LE CORSE E I LUCCHETTI")
    _, out = git("worktree", "list", "--porcelain")
    W = [l[9:] for l in out.splitlines() if l.startswith("worktree ")]
    for w in W:
        f = os.path.join(w, "doc", "REGISTRO_CORSE.md")
        if os.path.exists(f):
            ap = aperte(f)
            print("    il registro di %-44s le voci APERTE: %d %s" % (w, len(ap), ap if ap else ""))
        else:
            print("    il registro di %-44s (nessun doc/REGISTRO_CORSE.md)" % w)
        _, gd = git("rev-parse", "--git-dir", cwd=w)
        gd = gd if os.path.isabs(gd) else os.path.join(w, gd)
        print("        index.lock in %s: %s" % (gd, "### PRESENTE" if os.path.exists(os.path.join(gd, "index.lock")) else "nessuno"))
    if os.path.isdir(TAPPE):
        aperti = [x for x in os.listdir(TAPPE) if x.endswith(".txt") and ".chiuso." not in x]
        print("    i file di tappe NON chiusi in %s: %d %s" % (TAPPE, len(aperti), aperti if aperti else ""))
    else:
        print("    %s: non c'e'" % TAPPE)
    lk = os.path.join(lucchetto, "commit.lock")
    print("    commit.lock (%s): %s" % (lk, "### PRESENTE" if os.path.exists(lk) else "nessuno"))
    print("=" * 130)


def main():
    sys.path.insert(0, os.path.join(RADICE, "csv"))
    import _presidio
    _presidio.avvia(__file__)
    ap = argparse.ArgumentParser()
    ap.add_argument("--lucchetto", required=True, help="la cartella di committa2.py")
    x = ap.parse_args()
    indice()
    rami()
    corse(x.lucchetto)
    return 0


if __name__ == "__main__":
    sys.exit(main())
