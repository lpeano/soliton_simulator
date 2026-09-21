# -*- coding: utf-8 -*-
"""Scrive/aggiorna il blocco PUNTO DI RIPRESA in cima alla CODA UNICA.

⚠ E' RIGENERABILE: si riscrive per intero ogni volta, fra due marcatori. Cosi' non si accumulano
  versioni vecchie e non serve ricordarsi di cancellare la precedente.
Uso:  python ripresa.py <file_con_il_corpo.md>
"""
import io
import subprocess
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

APRE = "<!-- PUNTO-DI-RIPRESA:INIZIO -->"
CHIUDE = "<!-- PUNTO-DI-RIPRESA:FINE -->"
P = "doc/STATO_RUN.md"

corpo = io.open(sys.argv[1], encoding="utf-8", newline="").read().rstrip("\n")
head = subprocess.run(["git", "rev-parse", "--short", "HEAD"],
                      capture_output=True, text=True).stdout.strip()
import datetime as _dt
corpo = corpo.replace("@@HEAD@@", head).replace("@@ORA@@",
                                                _dt.datetime.now().strftime("%Y-%m-%d %H:%M"))

t = io.open(P, encoding="utf-8", newline="").read()
blocco = APRE + "\n" + corpo + "\n" + CHIUDE
if APRE in t:
    a = t.index(APRE)
    b = t.index(CHIUDE) + len(CHIUDE)
    t = t[:a] + blocco + t[b:]
    dove = "aggiornato"
else:
    t = blocco + "\n\n" + t
    dove = "creato in cima"
io.open(P, "w", encoding="utf-8", newline="\n").write(t)
print("PUNTO DI RIPRESA %s in %s (HEAD %s)" % (dove, P, head))
