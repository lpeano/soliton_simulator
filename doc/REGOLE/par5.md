# dettaglio di `CLAUDE.md` par.5 — **politiche di commit**

*(Questo file **non contiene regole**: spiega regole che stanno in `CLAUDE.md`, citate col loro numero o id. Non rimanda ad altri file di `doc/REGOLE/`.)*

## PERCHE' *«COMMIT PRIMA DI OGNI RUN»*

Il codice che genera un output dev'essere **gia' committato quando l'output nasce**.
### **Altrimenti il referto cita un blob che nel repo non esiste** — e' il caso
`_sonda_scherm`: una sonda girata **fuori dal repo**, il referto committato e **lo
strumento no**.

## PERCHE' *«UN COMMIT = UN CAMBIAMENTO LOGICO»*

Impacchettare piu' meccanismi insieme **rompe la tracciabilita' del «quale pezzo ha fatto
cosa»** — ed e' esattamente la domanda che si fa quando un sigillo fallisce tre settimane
dopo.

## IL MESSAGGIO: cinque sezioni

**COSA e' cambiato / PERCHE' / COME / NUMERI / COSA-RICONTROLLARE.**
### **E la lista dei file si GENERA da `git diff --cached --name-only`, non si ricorda:**
la regola era scritta da **due recidive** prima di diventare il presidio `H-FILE`.

## SE IL SIGILLO FALLISCE

Si committa **lo stato + il fallimento** e **si ferma**. ### \u26d4 **Non si «aggiusta al
volo» dentro lo stesso commit: la correzione e' UN COMMIT A SE'.** Altrimenti il referto
del fallimento e la sua cura diventano indistinguibili, e **nessuno sa piu' che cosa
fallisse.**

## DURANTE UN RUN, NESSUN FILE DEL PERCORSO IN USO SI MODIFICA

**Non solo il simulatore:** il **driver** e **ogni script che il processo ha importato**.
Se serve modificarne uno, si lavora su una **COPIA** e si porta la modifica sul file vero
**a run chiuso**.

### **E il caso tipico e' il sigillo che invoca la patch come sottoprocesso:** durante quel
run **la patch e' un file del percorso in uso**, anche se il sigillo non la importa.

## NIENTE ATTESE ATTIVE

Niente `Start-Sleep` ne' polling in run o script: **sprecano tempo e crediti**.

### \u26a0 **E per attendere un processo STACCATO su Windows, `kill -0` di Git Bash NON
SERVE:** lavora sui PID di **MSYS**, non su quelli di **Windows** — due namespace diversi.
### **Il 2026-10-04 ha dichiarato «terminato» un sigillo che era VIVO all'ultimo braccio.**
Si usa `tasklist`, e la terminazione si verifica con **due** letture indipendenti.
