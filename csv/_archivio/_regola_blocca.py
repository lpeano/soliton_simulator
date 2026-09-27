# -*- coding: utf-8 -*-
"""Applica la REGOLA di Luca alle 23 voci `CENS-*`, e SEGNALA le ambigue.

**LA REGOLA, verbatim:**
  `SI` = la falsita' cambia i NUMERI della fisica del run
         *(di fatto: quelle chiuse da (a) e da (b), cioe' `CENS-A6`, `CENS-A7`, `CENS-B7`,
         `CENS-A2`; piu' `KERNEL_ALPHA`, che rivendica il principio di equivalenza = prova 3)*
  `NO` = si risolve riscrivendo un commento o un documento

**COME L'HO APPLICATA, e dove si rompe.** La regola e' NETTA sulla classe (A): una FALSITA' di
commento **non cambia i numeri** -- il codice fa quel che fa -- quindi si risolve **riscrivendo**,
ed e' `NO`; tranne dove la cura (a)/(b) **cambia il comportamento**, ed e' `SI`.
**Sulla classe (B) la regola NON E' DECIDIBILE COME SCRITTA**, e lo dico invece di forzarla: in una
(B) **non c'e' una falsita'** -- c'e' **un'assenza di misura**. Cio' che *«cambia i numeri»* non e'
la lacuna: e' **la legge**, che e' gia' attiva. Quindi per ogni (B) **attiva e portante** la regola
puo' rispondere sia `SI` *(la legge muove i numeri e nessuno l'ha verificata)* sia `NO` *(la
lacuna si colma con una MISURA, non con parole -- ma le misure sono SOSPESE)*.
**Decisione presa qui:** `NO` dove la voce **non e' attiva** *(non puo' cambiare i numeri)* o e'
**di processo**; `SI` per le cinque nominate da Luca; **AMBIGUA per tutte le altre (B) attive**,
che restano `DA-DECIDERE` e **le decide lui**.
"""
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
RAD = r"C:\Users\lpeano\soliton_simulator"
TAB, NL = chr(9), chr(10)

# le cinque nominate da Luca
SI_NOMINATE = {
    "CENS-A6": "chiusa da (a): la cura rende l'aggiornamento SINCRONO, e cio' cambia i numeri",
    "CENS-A7": "chiusa da (a): imporre `w` a ogni `calcola_psi` cambia quale `psi` legge la fisica",
    "CENS-B7": "chiusa da (a): `--sync` e' la cura (a) stessa, e cambia i numeri",
    "CENS-A2": "chiusa da (b): rendere `4 pi` strutturale puo' spostare la soglia di mitosi",
    "CENS-B12": "rivendica il PRINCIPIO DI EQUIVALENZA = la prova (3) del bersaglio, ed e' sempre attivo",
}
# quelle che si risolvono con parole, o che non sono attive (non possono muovere i numeri)
NO_MOTIVI = {
    "CENS-A3": "il ramo gira UGUALE prima e dopo: la falsita' e' nel commento, e si riscrive",
    "CENS-A4": "il ramo e' MORTO (`MITOSI_DIR = 0.0`): un commento falso su codice che non gira",
    "CENS-A5": "due commenti che si contraddicono: nessuno dei due esegue niente",
    "CENS-B9": "NON attiva nel driver: non puo' cambiare i numeri di questo run",
    "CENS-B10": "NON attiva nel driver: non puo' cambiare i numeri di questo run",
    "CENS-B11": "NON attiva (`PLAST_DIN` e' il sostituto): la promessa e' rimasta senza esecutore",
    "CENS-B15": "e' un CONDIZIONALE scritto in un commento: si risolve riscrivendolo",
    "CENS-B16": "e' di PROCESSO (inventario e README), non di fisica: nessun numero lo tocca",
}
# le ambigue, con il PERCHE' l'ambiguita' esiste
AMBIGUE = {
    "CENS-A1": "la RIDUZIONE AL LIMITE dello spinore. Riscrivere il commento NON cambia i numeri, "
               "ma cio' che il commento dichiara e' la PROPRIETA' su cui poggiano i sigilli di "
               "riduzione al limite del fork: se e' falsa, quei sigilli certificano uno stato "
               "fuori dall'orbita del sistema. E' documentaria nella forma e portante nella "
               "sostanza",
    "CENS-B1": "`SPINORE_VIVO` e' ATTIVO e muove i numeri, ma la lacuna e' una MISURA mancante "
               "(il rigiro dei sigilli), non una falsita'. E le misure sono SOSPESE",
    "CENS-B2": "`SPIN_FEEDBACK` attivo; la FORMA e' misurata (12/12), l'EFFETTO no. La voce e' "
               "gia' dichiarata AMBIGUA nel censimento stesso",
    "CENS-B3": "`TAU_A_LOCALE` attivo e SENZA flag CLI: non esiste il ramo OFF, quindi il criterio "
               "non e' nemmeno VERIFICABILE. Non si risolve con parole ne' con una misura possibile",
    "CENS-B4": "`TAU_LOCALI` attivo e senza flag CLI, stessa forma di `CENS-B3`",
    "CENS-B5": "`SCHERMATURA` attiva; *da validare su TEMPI LUNGHI* e' una MISURA lunga, oggi sospesa",
    "CENS-B6": "`REGIME` deterministico attivo; *DA RIPRENDERE* chiede un meccanismo NUOVO "
               "(seme di asimmetria), che non e' ne' parole ne' misura: e' progetto",
    "CENS-B8": "`VERLET`: il ramo detto SPERIMENTALE E' il percorso vivo. Riscrivere il commento "
               "e' parole, ma la deriva d'energia del ramo Eulero non e' MAI stata misurata",
    "CENS-B13": "il PAVIMENTO dell'inerzia: e' un limite ATTIVO che muove i numeri (`A11`), e i "
                "contatori sono cablati ma mai letti. Leggerli e' una misura, oggi sospesa",
    "CENS-B14": "l'osservabile e' gia' CALCOLATA e mai letta: leggerla e' una misura, oggi sospesa",
}

P = os.path.join(RAD, "doc", "INDICE_ID.tsv")
righe = io.open(P, encoding="utf-8").read().split(NL)
capi = righe[0].split(TAB)
K = {k: i for i, k in enumerate(capi)}
tab = []
for n, r in enumerate(righe):
    c = r.split(TAB)
    if not c or not c[0].startswith("CENS-") or len(c) != len(capi):
        continue
    idx = c[0]
    if idx in SI_NOMINATE:
        val, mot, amb = "SI", SI_NOMINATE[idx], ""
    elif idx in NO_MOTIVI:
        val, mot, amb = "NO", NO_MOTIVI[idx], ""
    elif idx in AMBIGUE:
        val, mot, amb = "DA-DECIDERE", "", AMBIGUE[idx]
    else:
        raise SystemExit("[regola] %s non classificata: MI FERMO invece di indovinare" % idx)
    c[K["blocca_run_base"]] = val
    if val == "SI":
        c[K["motivo"]] = mot
    elif val == "NO":
        c[K["motivo"]] = ""
    else:
        c[K["motivo"]] = ""
    agg = (" | REGOLA DI LUCA applicata il 2026-09-27: blocca_run_base = %s. %s"
           % (val, ("MOTIVO: " + mot) if mot else ("⚠ AMBIGUA, LA DECIDE LUCA: " + amb)))
    if "REGOLA DI LUCA applicata" not in c[K["nota"]]:
        c[K["nota"]] = c[K["nota"]] + agg
    righe[n] = TAB.join(c)
    tab.append((idx, val, mot or amb))

io.open(P, "w", encoding="utf-8", newline=NL).write(NL.join(righe))
print("classificate: %d   SI %d   NO %d   AMBIGUE %d"
      % (len(tab), sum(1 for x in tab if x[1] == "SI"),
         sum(1 for x in tab if x[1] == "NO"),
         sum(1 for x in tab if x[1] == "DA-DECIDERE")))
for t in tab:
    print("  %-10s %-12s %s" % (t[0], t[1], t[2][:88]))
