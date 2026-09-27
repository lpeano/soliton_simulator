# -*- coding: utf-8 -*-
"""Applica le DECISIONI DI LUCA sulle dieci `CENS-*` che la regola aveva lasciato AMBIGUE.

**Mandato, verbatim (risposte a `bf15c0c`):**
  - `CENS-B12` (KERNEL_ALPHA): **NO**. *«BLOCCA LA PROVA 3 (universalita'): misura del principio
    di equivalenza prima della PROVA 3.»* **Correzione del guardiano:** `SI` avrebbe bloccato
    il run base con una misura SOSPESA. -- **era un mio `SI`, ed era sbagliato per quella ragione.**
  - `CENS-A1`: **SI**. Si chiude con la decisione **(e)** sul legame `phi`-spinore.
  - `CENS-B1 B2 B5 B8 B13 B14`: **NO**. Leggi ATTIVE, restano attive *(decisione 3)*,
    nota: *«da misurare dopo il run base»*.
  - `CENS-B3 B4`: **NO**. **La cura e' DICHIARARE che il ramo OFF non esiste.**
  - `CENS-B6`: **NO** *(progetto)*.

**GIRA UNA VOLTA:** si ferma se la decisione e' gia' scritta nella nota.
"""
import io
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
RAD = r"C:\Users\lpeano\soliton_simulator"
TAB, NL = chr(9), chr(10)
MARCA = "DECISIONE DI LUCA del 2026-09-27 (risposte a bf15c0c)"

DOPO_RUN = "da misurare dopo il run base"
DEC = {
    "CENS-B12": ("NO", "", "NON blocca il run base, BLOCCA LA PROVA 3 (universalita'): la misura "
                          "del principio di equivalenza va fatta prima della PROVA 3. Correzione "
                          "del guardiano al mio SI: un SI avrebbe bloccato il run base con una "
                          "misura SOSPESA dalla decisione (1)."),
    "CENS-A1":  ("SI", "la riduzione al limite dello spinore e' la PROPRIETA' su cui poggiano i "
                       "sigilli del fork: se e' falsa, quei sigilli certificano uno stato fuori "
                       "dall'orbita del sistema",
                 "SI. Si chiude con la decisione (e) sul legame phi-spinore."),
    "CENS-B1":  ("NO", "", "legge ATTIVA, resta attiva (decisione 3). " + DOPO_RUN + "."),
    "CENS-B2":  ("NO", "", "legge ATTIVA, resta attiva (decisione 3). " + DOPO_RUN + "."),
    "CENS-B5":  ("NO", "", "legge ATTIVA, resta attiva (decisione 3). " + DOPO_RUN + "."),
    "CENS-B8":  ("NO", "", "legge ATTIVA, resta attiva (decisione 3). " + DOPO_RUN + "."),
    "CENS-B13": ("NO", "", "legge ATTIVA, resta attiva (decisione 3). " + DOPO_RUN + "."),
    "CENS-B14": ("NO", "", "legge ATTIVA, resta attiva (decisione 3). " + DOPO_RUN + "."),
    "CENS-B3":  ("NO", "", "LA CURA E' DICHIARARE CHE IL RAMO OFF NON ESISTE (nessun flag CLI): "
                           "non si misura un ramo che non c'e', si scrive che non c'e'."),
    "CENS-B4":  ("NO", "", "LA CURA E' DICHIARARE CHE IL RAMO OFF NON ESISTE (nessun flag CLI): "
                           "non si misura un ramo che non c'e', si scrive che non c'e'."),
    "CENS-B6":  ("NO", "", "NO: e' PROGETTO (chiede un meccanismo nuovo), non una lacuna di misura."),
}

P = os.path.join(RAD, "doc", "INDICE_ID.tsv")
righe = io.open(P, encoding="utf-8").read().split(NL)
capi = righe[0].split(TAB)
K = {k: i for i, k in enumerate(capi)}
fatte = 0
for n, r in enumerate(righe):
    c = r.split(TAB)
    if len(c) != len(capi) or c[0] not in DEC:
        continue
    if MARCA in c[K["nota"]]:
        print("  gia' deciso:", c[0])
        continue
    val, mot, testo = DEC[c[0]]
    c[K["blocca_run_base"]] = val
    c[K["motivo"]] = mot
    c[K["nota"]] = c[K["nota"]] + " | " + MARCA + ": blocca_run_base = " + val + ". " + testo
    righe[n] = TAB.join(c)
    fatte += 1
    print("  %-10s -> %-3s  %s" % (c[0], val, testo[:72]))
if fatte == 0:
    raise SystemExit("[decisioni] nessuna voce da decidere: MI FERMO")
io.open(P, "w", encoding="utf-8", newline=NL).write(NL.join(righe))
print("")
print("voci decise: %d su %d" % (fatte, len(DEC)))
