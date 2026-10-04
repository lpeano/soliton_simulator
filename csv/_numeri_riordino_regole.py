# -*- coding: utf-8 -*-
"""I NUMERI del riordino di CLAUDE.md: li genera, non li ricopia (L-NUMERI).

Confronta il blob di CLAUDE.md a ogni commit del riordino col blob di oggi,
paragrafo per paragrafo, e misura i file di dettaglio nati.
"""
import io
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _presidio
import _presidio_righe

_presidio.avvia(__file__)

NL = chr(10)
RADICE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRIMA = "da79cc1"
TAPPE = [
    ("da79cc1", "PRIMA del riordino"),
    ("61b8e5f", "lo strumento"),
    ("885d9a5", "par.12"),
    ("dc08221", "par.0 + par.4"),
    ("d1df098", "par.6 + par.7"),
    ("829b4a5", "par.9 + par.9-ter"),
    ("b5e5e99", "par.2,3,5,8,11"),
    ("HEAD", "(il commit di oggi)"),
]


def git(*a):
    return subprocess.run(["git", "-C", RADICE] + list(a), capture_output=True).stdout


def paragrafi(testo):
    """-> [(titolo, righe)] piu' ('(intestazione)', righe)."""
    r = testo.split(NL)
    tagli = [(i, l) for i, l in enumerate(r) if re.match(r"^## ", l)]
    out = [("(intestazione)", tagli[0][0])] if tagli else []
    for k, (i, l) in enumerate(tagli):
        fine = tagli[k + 1][0] if k + 1 < len(tagli) else len(r)
        nome = re.sub(r"^## ", "", l)
        nome = re.split(r"[ ]+[-\u2014]|[ ]*\*\(|:", nome)[0].strip()
        out.append((nome, fine - i))
    return out


print("=" * 92)
print("  I NUMERI DEL RIORDINO DI CLAUDE.md")
print("=" * 92)

print(NL + "--- LA CURVA, commit per commit " + "-" * 59)
print("  %-9s  %-24s  %6s  %7s" % ("commit", "che cosa e' uscito", "righe", "delta"))
prec = None
for h, et in TAPPE:
    t = git("show", h + ":CLAUDE.md").decode("utf-8", "replace")
    n = _presidio_righe.conta(t)
    d = "" if prec is None else "%+d" % (n - prec)
    print("  %-9s  %-24s  %6d  %7s" % (h, et, n, d))
    prec = n
oggi = io.open(os.path.join(RADICE, "CLAUDE.md"), encoding="utf-8").read()
n_oggi = _presidio_righe.conta(oggi)
print("  %-9s  %-24s  %6d  %7s" % ("(disco)", "oggi", n_oggi, "%+d" % (n_oggi - prec)))

t0 = git("show", PRIMA + ":CLAUDE.md").decode("utf-8", "replace")
n0 = _presidio_righe.conta(t0)
print(NL + "  TOTALE: %d -> %d righe, %+d (%.0f%% in meno). Tetto 400, obiettivo ~250."
      % (n0, n_oggi, n_oggi - n0, 100.0 * (n0 - n_oggi) / n0))

print(NL + "--- PARAGRAFO PER PARAGRAFO " + "-" * 63)
a = dict(paragrafi(t0))
b = paragrafi(oggi)
print("  %-42s %6s %6s %7s" % ("paragrafo", "prima", "dopo", "delta"))
sp = 0
for nome, n in b:
    p = a.get(nome)
    if p is None:
        print("  %-42s %6s %6d %7s" % (nome[:42], "-", n, "NUOVO"))
        continue
    sp += p - n
    print("  %-42s %6d %6d %7s" % (nome[:42], p, n, "%+d" % (n - p)))
print("  %-42s %6s %6s %7d" % ("(somma dei risparmi)", "", "", -sp))

print(NL + "--- I FILE DI DETTAGLIO " + "-" * 67)
d = os.path.join(RADICE, "doc", "REGOLE")
righe = {}
for f in sorted(os.listdir(d)):
    if not f.endswith(".md"):
        continue
    righe[f] = _presidio_righe.conta(io.open(os.path.join(d, f), encoding="utf-8").read())
for f in sorted(righe, key=lambda x: (len(x), x)):
    print("  %-14s %4d righe" % (f, righe[f]))
print("  %-14s %4d righe in %d file" % ("TOTALE", sum(righe.values()), len(righe)))
print("  media %.1f, il piu' lungo %d, il piu' corto %d"
      % (float(sum(righe.values())) / len(righe), max(righe.values()), min(righe.values())))

print(NL + "--- IL BILANCIO: dove sono andate le righe " + "-" * 48)
print("  righe uscite da CLAUDE.md                  %6d" % (n0 - n_oggi))
print("  righe nei file di dettaglio                %6d" % sum(righe.values()))
print("  rapporto (dettaglio / uscite)              %6.2fx" % (
    float(sum(righe.values())) / max(1, n0 - n_oggi)))
print("  ### il dettaglio e' PIU' LUNGO di cio' che e' uscito: non e' una perdita,")
print("      e' il testo che in CLAUDE.md era COMPRESSO e qui e' scritto per esteso.")

print(NL + "--- CHE COSA NON HO CONDENSATO " + "-" * 60)
d_oggi = dict(b)
for nome, perche in [("1. IL BERSAGLIO DEL PROGETTO", "il BERSAGLIO del progetto"),
                     ("10. IL PRINCIPIO GUIDA", "la frase che lo GUIDA")]:
    print("  %-30s %2d righe   CONTENUTO (%s), non dettaglio"
          % (nome[:30], d_oggi.get(nome, -1), perche))
print("  ### Condensarli vorrebbe dire ACCORCIARE UNA CITAZIONE DI LUCA.")
print()
print("=" * 92)
