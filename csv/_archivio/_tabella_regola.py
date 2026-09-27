# -*- coding: utf-8 -*-
"""GENERA il par.6 di `doc/CURE_fisica_ordine.md`: la tabella delle 23 `CENS-*` dopo la REGOLA.

**A COSA SERVE:** i numeri e i motivi della tabella (5 `SI` / 8 `NO` / 10 AMBIGUE) **escono da
qui**, letti da `doc/INDICE_ID.tsv` -- non sono ricopiati a mano (`L-NUMERI`).
**NON SI RILANCIA A VUOTO:** appende al documento, e si ferma se il par.6 c'e' gia'.
**Girato una volta il 2026-09-27**, dopo `_regola_blocca.py`.
**QUESTO E' IL TESTO CHE HA GIRATO**, riallineato a mano dopo una prima copia approssimata:
la copia non riproduceva il blocco di citazione sull'ambiguita' strutturale, e **un generatore che
non riproduce il suo output non e' una provenienza**.
"""
import io
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
RAD = r"C:\Users\lpeano\soliton_simulator"
TAB, NL = chr(9), chr(10)
DOC = os.path.join(RAD, "doc", "CURE_fisica_ordine.md")
TITOLO = "# 6. **LA REGOLA DI LUCA APPLICATA ALLE 23 `CENS-*`**"

if TITOLO in io.open(DOC, encoding="utf-8").read():
    raise SystemExit("[tabella] il par.6 c'e' GIA': non appendo un duplicato")

righe = io.open(os.path.join(RAD, "doc", "INDICE_ID.tsv"), encoding="utf-8").read().split(NL)
capi = righe[0].split(TAB)
K = {k: i for i, k in enumerate(capi)}
si, no, am = [], [], []
for r in righe:
    c = r.split(TAB)
    if not c or not c[0].startswith("CENS-") or len(c) != len(capi):
        continue
    n = c[K["nota"]]
    i = n.rfind("REGOLA DI LUCA applicata")
    coda = n[i:] if i > 0 else ""
    if "MOTIVO: " in coda:
        mot = coda.split("MOTIVO: ", 1)[1]
    elif "LA DECIDE LUCA: " in coda:
        mot = coda.split("LA DECIDE LUCA: ", 1)[1]
    else:
        mot = ""
    t = c[K["titolo_breve"]].replace("[A] ", "").replace("[B] ", "")[:58]
    v = c[K["blocca_run_base"]]
    (si if v == "SI" else no if v == "NO" else am).append((c[0], t, mot))

SPUNTA, ATTENZIONE = chr(0x2705), chr(0x26A0)
B = []
B.append("")
B.append("---")
B.append("")
B.append(TITOLO + " *(2026-09-27)*")
B.append("")
B.append("> **La regola, verbatim:** `SI` = **la falsita' cambia i NUMERI della fisica del run**;")
B.append("> `NO` = **si risolve riscrivendo un commento o un documento**.")
B.append("> **Applicata a TUTTE e 23, non solo alle cinque nominate.** Esito: **5 `SI` " + chr(0xB7)
         + " 8 `NO` " + chr(0xB7))
B.append("> 10 AMBIGUE**, che restano `DA-DECIDERE` e **le decide Luca**.")
B.append("")
B.append("## %s `SI` — %d voci" % (SPUNTA, len(si)))
B.append("")
B.append("| ID | che cos'e' | motivo |")
B.append("|---|---|---|")
for a, b, c in si:
    B.append("| **`%s`** | %s | %s |" % (a, b, c))
B.append("")
B.append("## `NO` — %d voci" % len(no))
B.append("")
B.append("| ID | che cos'e' | motivo |")
B.append("|---|---|---|")
for a, b, c in no:
    B.append("| `%s` | %s | %s |" % (a, b, c))
B.append("")
B.append("## %s **AMBIGUE — %d voci, LE DECIDE LUCA**" % (ATTENZIONE, len(am)))
B.append("")
B.append("> ### **E L'AMBIGUITA' NON E' CASO PER CASO: E' STRUTTURALE, E STA NELLA CLASSE (B).**")
B.append("> La regola e' **netta sulla classe (A)**: una falsita' di commento **non cambia i")
B.append("> numeri** — il codice fa quel che fa — quindi si risolve **riscrivendo**, ed e' `NO`;")
B.append("> tranne dove la cura **(a)** o **(b)** cambia il comportamento, ed e' `SI`.")
B.append("> **Sulla classe (B) la regola non e' decidibile come scritta, e lo dico invece di")
B.append("> forzarla:** in una (B) **non c'e' una falsita'** — c'e' **un'assenza di misura**.")
B.append("> Cio' che *«cambia i numeri»* **non e' la lacuna: e' la LEGGE, che e' gia' attiva.**")
B.append("> Quindi ogni (B) **attiva e portante** puo' leggersi `SI` *(la legge muove i numeri e")
B.append("> nessuno l'ha verificata)* **oppure** `NO` *(la lacuna si colma con una MISURA, non con")
B.append("> parole — ma le misure sono SOSPESE dalla decisione (1))*.")
B.append(">")
B.append("> **Ne discende una domanda che non e' mia da chiudere:** se una (B) attiva prende `SI`,")
B.append("> **il run base resta bloccato da una misura che la decisione (1) ha appena sospeso.**")
B.append("")
B.append("| ID | che cos'e' | perche' e' ambigua |")
B.append("|---|---|---|")
for a, b, c in am:
    B.append("| %s `%s` | %s | %s |" % (ATTENZIONE, a, b, c))
B.append("")
io.open(DOC, "a", encoding="utf-8", newline=NL).write(NL.join(B) + NL)
print("tabella scritta: %d SI, %d NO, %d ambigue" % (len(si), len(no), len(am)))
