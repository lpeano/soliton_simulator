# STATO DEI RUN — registro append-only

**Scritto AUTOMATICAMENTE da `csv/_stato_run.py`.** Il commit NON è
automatico (vedi la dichiarazione nel modulo): ma **il file esiste sempre**,
quindi dopo un riavvio lo stato si legge **dal disco**, non dalla memoria.

**Una voce `APERTO` senza `chiuso` = quel run è morto senza dirlo.**


## APERTO batch-1200 (campagna struttura)

- **avvio** `2026-09-18 17:42:46` · **blob** `a1ae5090` · **HEAD** `53b9443`
- **comando**
  ```
  python soliton_simulator.py --batch --nmasse 3 --sep 8 --passi 1200 --ogni 10 --csv csv/_test_fork/_g1200/cond.csv --diaglog csv/_test_fork/_g1200/diag.csv --campo-spinoriale --spinore-vivo --spinore-corretto --chi-core --calore-scal --deparam-orologio --verlet --fork-su2 --fork-su2-mem --cs-dinamico --tau-luce --rumore-colorato --pav-com --guscio-morbido --zeta-vir --chi-basc --plast-din --viriale --olon-part --sync-db csv/_test_fork/_g1200/stato.pkl --db-ogni 10 --db-cleanup
  ```
- **note** voce RICOSTRUITA dai dati sul disco: il registro non esisteva quando il run e' partito.
- *2026-09-18 17:42:46* — seed 900, letto da run.log. Una sola invocazione, 0 righe `[db] stato CARICATO`.
- *2026-09-18 17:42:46* — snapshot presi ai passi VERI 120 / 130 / 470 / 800 / 840 / 1200 (i primi tre mislabellati dal watcher e RINOMINATI col loro `_db_step`).

**chiuso 2026-09-18 17:42:46 — FINITO** Ultima riga di `diag.csv`: **passo 1200**, 21662 righe, `n = 1204`. **Dati COMPLETI.** Analisi fatta: `doc/REFERTO_chi_non_invecchia.md` (`Z46`/`Z9`). ⚠ **MANCA il referto dei QUATTRO BLOCCHI** del mandato «struttura a 1200» (maturazione / guscio / fasi / contrasto): la sonda `csv/_test_fork/_struttura_1200.py` e' COMMITTATA (`35a5786`) ma **NON E' MAI STATA GIRATA**.

## APERTO scena-video TENTATIVO 1

- **avvio** `2026-09-18 17:42:46` · **blob** `a1ae5090` · **HEAD** `53b9443`
- **comando**
  ```
  python csv/_test_fork/_scena_video.py 400 csv/_test_fork/_gvideo 10,115,190,270,375
  ```
- **note** voce RICOSTRUITA: il commit `b84702b` dice «RUN FERMATO» ma NON diceva a che punto.

**chiuso 2026-09-18 17:42:47 — FERMATO** Fermato al **frame ~50 su 400** *(`n` 2391 -> 2576, `14.1 s/frame`)*. **Motivo:** l'equivalenza del driver col `update()` del video era **DEDOTTA, non verificata**. **I dati parziali sono stati CANCELLATI** perche' su una traiettoria non certificata: **non servono.** Il sigillo `_sigillo_driver_video.py` ha poi dato **PASS** (14 array, `max|A-B| = 0.000e+00`, shape uguali).

## APERTO scena-video TENTATIVO 2 (in corso)

- **avvio** `2026-09-18 17:42:47` · **blob** `a1ae5090` · **HEAD** `53b9443`
- **comando**
  ```
  python csv/_test_fork/_scena_video.py 400 csv/_test_fork/_gvideo 10,115,190,270,375 > csv/_test_fork/_gvideo_run.log 2>&1
  ```
- **note** Rilanciato DOPO il PASS del sigillo del driver (`94e2ec0`).
- *2026-09-18 17:42:47* — **IN CORSO** al momento della scrittura: frame **170 su 400**, `n` 2391 -> 4120, `15.6 s/frame`. Snapshot gia' presi: **frame 10, frame 115**. Prossimi: 190 / 270 / 375.
- *2026-09-18 17:42:47* — ⚠ La scena include **`--tau-luce`, il cui SIGILLO E' FALLITO** (CLAUDE.md par.0): **ramo NON CERTIFICATO**, e ogni numero che ne esce lo eredita. E **`--chi-basc` riscrive `perc_chi` a ogni passo**: non e' un'etichetta di lignaggio.
- *2026-09-18 17:42:47* — ⚠ `PASSI_PER_FRAME = 6`: **400 frame = 2400 PASSI**. La tabella dei fotogrammi va RIMAPPATA (**frame 375 = passo 2250**), o i confronti con `Z46` (1200 passi) sbagliano di 2.
- *2026-09-18 17:46:16* — ✅ **IL REFERTO MANCANTE C'E'**: `doc/REFERTO_struttura_1200.md` (`Z48`). Letti gli istanti 120/800/1200; **130/470/840 NON letti** (la sonda cerca per NOME). La voce del batch e' CHIUSA e completa.
- *2026-09-18 18:10:22* — **frame 275/400** (`n` 2391 -> 5520, `15.6 s/frame`, ~33 min alla fine). Snapshot presi: **10, 115, 190, 270**. Manca **375**. ⚠ **L'INVERSIONE DELLA DILATAZIONE E' GIA' VISIBILE NEI MIEI DATI: `dil` da `+10.97 %` (frame 265) a `+8.59 %` (frame 275).** E al frame 270 `n = 5443` contro `5465` della tabella dei fotogrammi, `dil +10.75 %` contro `+10.3 %`: **e' la stessa scena.**
- *2026-09-18 18:42:13* — **frame 385/400**, `n = 7694`, `16.2 s/frame`. **TUTTI E CINQUE gli snapshot presi** (10/115/190/270/**375**). ⚠ **LA DILATAZIONE HA INVERTITO E STA OSCILLANDO:** `dil` = `-7.439 %` (370), `-2.704 %` (375), `-4.214 %` (380), `+2.797 %` (385). **Non e' solo «si ricomprime»: RIMBALZA.** `coer_l` continua a salire: `0.622 -> 0.631`. Al frame 375 `n = 7480` contro `7503` della tabella dei fotogrammi: **stessa scena.**

**chiuso 2026-09-18 18:47:44 — FINITO** **400 frame = 2400 passi in 6535 s (1h49)**, `16.34 s/frame`, **`n` da 2391 a 8018**. **SEI snapshot** (10/115/190/270/375/**400**). Stato finale: `coer_l = 0.669`, `dil = -1.13 %`. ⚠ **La dilatazione INVERTE e poi RIMBALZA**: `-7.44 %` (370) -> `-2.70 %` (375) -> `-4.21 %` (380) -> `+2.80 %` (385) -> `-1.13 %` (400). **La tabella dei fotogrammi si fermava al 375 e non poteva vederlo.** Dati in `csv/_test_fork/_gvideo/`; i `.pkl` NON si committano (48 MB l'uno).
- *2026-09-18 18:50:21* — ✅ **ANALISI FATTA**: `doc/REFERTO_struttura_video.md` (`Z49`). Sei istanti letti (frame 10/115/190/270/375/400 = passi 60/690/1140/1620/2250/2400).

## APERTO due-masse CONTROLLO (A/B su --nmasse)

- **avvio** `2026-09-18 19:40:56` · **blob** `a1ae5090` · **HEAD** `8f94cf4`
- **comando**
  ```
  python csv/_test_fork/_scena_video.py 400 csv/_test_fork/_g2m 10,115,190,270,375 fisica 2
  ```
- **note** A/B A VARIABILE SINGOLA contro `Z49`: cambia SOLO `--nmasse` (3 -> 2). **La PREDIZIONE DI LUCA e' committata PRIMA, in `a4fbe42`.**
- *2026-09-18 19:40:57* — pilota MISURATO: `n = 1894` alla semina, **`13.68 s/frame`** -> ~**1h35** per 400 frame. ⚠ **Il primo falsificatore scatta in parte: attendevo `n ~ 1594` (2/3 di 2391), misurato `1894` = il 79 %.** La semina per massa **NON e' lineare nel numero di masse**: le due scene differiscono anche per POPOLAZIONE, in modo non proporzionale. **Va nel referto.**

**chiuso 2026-09-18 21:10:45 — FINITO** **400 frame = 2400 passi in 5357.8 s (1h29)**, `13.40 s/frame`, **`n` da 1894 a 5878**. **SEI snapshot** (10/115/190/270/375/400) in `csv/_test_fork/_g2m/`. I `.pkl` NON si committano. **Confronto col run a TRE masse (`Z49`): `n` finale `5878` contro `8018`.**

## APERTO pilota-6000 (BLOCCANTE, prima del run lungo)

- **avvio** `2026-09-19 09:49:38` · **blob** `b9e07c73` · **HEAD** `d7b3a33`
- **comando**
  ```
  python soliton_simulator.py --batch --nmasse 3 --sep 8 --passi 300 --ogni 50 --db-ogni 300 --seed 900 --campo-spinoriale --spinore-vivo --spinore-corretto --chi-core --calore-scal --deparam-orologio --verlet --fork-su2 --fork-su2-mem --cs-dinamico --tau-luce --rumore-colorato --pav-com --guscio-morbido --zeta-vir --chi-basc --plast-din --viriale --olon-part --sync-db csv/_test_fork/_pilota6000/pilota.pkl --csv csv/_test_fork/_pilota6000/pilota.csv
  ```
- **note** PILOTA BLOCCANTE del mandato par.1: il batch matura entro 6000 passi, o `r` e' al pavimento come dice `Z46`? Seme 900, lo STESSO di `Z46`, cosi' il confronto e' sulla stessa scena (A3c).

**chiuso 2026-09-19 09:49:38 — FINITO** **300 passi in 371 s = `123.7 s/100`** (il batch a 1200 dava `127.5`: REGGE). `.pkl` **26.45 MB**. **VERDETTO: il batch NON MATURA. `93.0 %` dei nodi e' al pavimento con `r/r_floor = 1.0000`, e il loro tasso da' `1.5 MILIONI` di passi per `ramp = 1`.** **IL RUN A 6000 SUL BATCH NON SI LANCIA.**

## APERTO run-6000 SCENA VIDEO (l'archivio a serie)

- **avvio** `2026-09-19 14:38:00` · **blob** `7c4dec1d` *(SIGILLATO 12/12)* · **HEAD** `406d31f`
- **seme effettivo** `42` — **letto da `Rete.__init__`, NON 900**: `SEME_INIZIALE = 900` e' il
  NUMERO DI NODI seminati (`:4532`), e solo nel `--batch` lo stesso 900 e' riusato come seme
  (`:6407`). Scrivere «seed 900» qui sarebbe falso.
- **comando**
  ```
  python csv/_test_fork/_scena_video.py 1000 csv/_test_fork/_g6000 --serie=10 --csv-progresso=csv/_test_fork/_g6000/prog.csv
  ```
  → **1000 frame x 6 = 6000 passi**, snapshot **ogni 10 frame = 60 passi** → **100 snapshot**
  `scena_%06d.pkl.gz` (compressi a livello 1).
- **cadenza DERIVATA dal pilota**, non scelta: budget dichiarato **5.0 GB** prima di vedere i
  numeri; peso stimato **2.95-3.02 GB**; la cadenza 30 passi darebbe ~6 GB (oltre).
- **previsioni committate PRIMA**: `doc/PREVISIONI_run6000_scena.md`.
- **note** `--tau-luce` e' nel comando: sigillo **6/7**, `T3` e' un risultato dichiarato. Ogni
  numero di questo run lo eredita. `--chi-basc` riscrive `perc_chi`: non e' lignaggio.
- **attesa** ~**7.5 h** col modello lineare, **che SOTTOSTIMA** (il costo per frame cresce con `n`).
- **Z9-a all'avvio**: `passi(ramp=1) = 5098` sui mobili, contro i 6000 del run — **margine 18 %**,
  e `r` si e' mosso del **+149 % in 120 passi**: e' un'istantanea, non una previsione.

### ⚠ DA FARE A RUN FINITO — **la patch della ripresa, e la verifica che la precede**

> **✅ ASSORBITA il 2026-09-20 nella sezione «IL SOSPESO — LA LISTA UNICA» (voce `C`), e CHIUSA:**
> la ripresa **è** sul driver vero. Il testo resta per la cronaca, non come cosa da fare.

> **A RUN FINITO: portare la patch della ripresa sul driver vero** (`csv/_test_fork/_scena_video.py`,
> da **`f14ea4bd`** a **`7a02c5c3`**, la versione **sigillata 5/5** in
> `csv/_seal_fork/_sigillo_ripresa_scena.txt`). **NON prima che il run sia chiuso.**
>
> *(La patch era già stata applicata il 2026-09-19 alle ~15:55 **mentre il run girava**, e
> **ripristinata** alle 15:57:52 — commit `228eb07`. Non c'è stato danno, ed è **misurato**:
> `23f783e`, `3/3`, ripartendo dal passo 1800 si riottiene identico lo snapshot 1860 scritto
> durante quella finestra. **Ma «stavolta è andata bene» non è «era sicuro».**)*

> **PRIMA di applicare la patch, verificare DAL CODICE — non assumere — che gli snapshot di QUESTO
> run restino caricabili dopo che il driver è cambiato.**
>
> **Il ragionamento dice di sì:** `carica_stato` verifica il blob di **`soliton_simulator.py`**, non
> quello del driver, e il simulatore è **intatto** (`7c4dec1d` per tutta la sequenza).
> **Ma va CONFERMATO:** cercare dove viene usato il **blob del driver** (`f14ea4bd` → `7a02c5c3`) e
> se **BLOCCA** qualcosa.
>
> **Se esiste un controllo che include il driver e rifiuta:** il discriminante va riportato al blob
> del **SIMULATORE**, perché è quello che definisce la **FISICA** — e **solo perché** il sigillo del
> driver esteso ha dato **PASS** (`14 array, max|A-B| = 0.000e+00`). **Senza quel sigillo, NON si
> accetta.**
>
> **E la prova finale, dopo la patch:** ricaricare uno snapshot **di questo run** e riprendere.
> **Deve funzionare.**

**chiuso 2026-09-19 19:05 — FERMATO DA LUCA, dopo 2h30 di stallo.** **`450` frame su 1000 =
`2700` passi su 6000**, in `7013 s` di progresso utile più **~2h30 in cui il processo era VIVO e
non avanzava** (`15 817 s` di CPU totali, `99.6 %` su **un solo core**, nessuna scrittura dopo le
`16:35:05`).

**L'ARCHIVIO È INTATTO E COMPLETO fino al passo 2700**, verificato dopo l'arresto:
**45 snapshot su 45** si aprono, il `_db_step` **nel file** coincide con quello **nel nome**, serie
**contigua** da 60 a 2700 a cadenza 60, **nessun buco**, **nessun `.tmp`** lasciato a metà
*(`os.replace` è atomico: o il file c'è completo, o non c'è)*. **1.3 GB**, blob `7c4dec1d` ovunque.

**Il blocco NON è spiegato.** Escluso misurando: memoria *(287 MB usati, 11.5 GB liberi)*, disco
*(17 GB)*, CFL *(`_taup_cfl_max` fermo a `0.5657`, zero clamp)*, `MAX_NODI` *(9511 su 4 000 000)*,
`NaN`/`inf` *(zero su tutti gli array)*. → `doc/REFERTO_blocco_run6000.md`, dati grezzi in
`csv/_test_fork/_dump_2700.txt`.

**COSA RESTA FATTIBILE, e non è poco:** le misure del §3 del mandato — `Z9-b`, `ramp` per coorte,
`p95/p05`, le conseguenze, il ciclo — **si fanno su questi 45 snapshot senza rigirare niente**.
L'analizzatore è pronto: `csv/_test_fork/_misure_run6000.py`.

**E la ripresa è sigillata `5/5`:** si può ripartire dal passo 2700 — **ma prima va capito perché
si è fermato**, altrimenti si riparte verso lo stesso muro.

---

## CHECKPOINT 2026-09-20 — **chiusa la topologia (`Z65`). Il simulatore non è stato toccato.**

**HEAD `3a02819` · blob `775ceab7` · albero pulito · nessun processo in esecuzione.**

**Fatto oggi, tutto sui 45 snapshot già in archivio, senza rigirare niente:** le somme (`Z63`), `f`
e `median(|f|)` (`Z64`), e **la topologia (`Z65`)** — quattro componenti connesse che in 2700 passi
non si scambiano **nemmeno un arco**, i due picchi del grado che sono **la semina** (tre grafi
**completi** da 497 nodi al passo 6) e non una forma emersa, e il **grado 2 permanente** (84 % dopo
2100 passi). → `doc/REFERTO_topologia.md`.

**Un presidio che prima era un'assunzione, ora misurato:** `eta[k]` non diminuisce in **nessuna**
delle 44 transizioni → **gli indici dei nodi sono stabili**, e ogni misura di coorte fatta finora
poggiava su quello senza averlo verificato.

### Cosa resta da fare quando il run è definitivamente chiuso

> **✅ ASSORBITA il 2026-09-20 in «IL SOSPESO — LA LISTA UNICA»:** il punto 1 è **CHIUSO**
> (voce `C`), il punto 2 puntava al **bersaglio sbagliato** (voce `B10`), il punto 3 è la voce
> `B9`. Il testo resta per la cronaca.

1. **riapplicare la patch di ripresa** a `csv/_test_fork/_scena_video.py` (`f14ea4bd` → `7a02c5c3`),
   **dopo** aver verificato dal codice che gli snapshot dell'archivio restano caricabili col blob
   del driver cambiato; poi rigirare il sigillo del driver e **provare davvero** un ricarico +
   ripresa da uno snapshot reale;
2. **togliere `--override-blob`** dal driver: è un presidio **deliberatamente indebolito**,
   accettabile solo finché gli esperimenti su `COPPIA_RECIPROCA` / `GRAV_AMPIEZZA` sono aperti;
3. **i fronti aperti che nessuna misura di oggi ha chiuso:** perché il run si sia fermato al 2700;
   perché la catena `f → x → r` non riproduca `r` dal passo 24 (`Z64`, famiglia `Z19`); perché 1455
   nodi stiano a `10⁻¹³` nel ramo A e qualunque perturbazione della coppia li accenda (`Z63`); se
   il profilo identico delle due cure sia **divergenza caotica** — servirebbe un terzo braccio con
   perturbazione nulla, o un secondo seme.

---

## 2026-09-20 — **L'ORDINE DEL LAVORO, deciso da Luca: ① → ② → ③**

**HEAD `e403e15` · simulatore `f81c4fe1`** *(sha1 byte grezzi; blob git `af8a96f1`)* · albero
pulito · **nessun run in esecuzione.**

```
①  LE GUARDIE DI PRECONDIZIONE          <- in corso
②  IL PANNELLO FEDELE                   <- dopo ①
③  IL RUN LUNGO a sep = 4.0             <- PER ULTIMO
```

**Nessun run parte finché ① e ② non sono chiusi.**

### Cosa è già pronto per ③, e resta sigillato

- **il driver** `csv/_test_fork/_scena_video.py`: `--sep=X` nominale *(sigillo `4/4`)* e la
  **ripresa** `--riprendi` *(sigillo `5/5` sul driver VERO)*;
- **il pilota a `sep = 4.0`**: archi massa-massa **0**, archi massa-vuoto **97 447** stabili
  *(−0.15 % in 300 passi)*, **una componente**, **196 nodi `MISTO`**;
- **la cadenza proposta**: `--serie=20` *(= `--db-ogni 120` passi)* → **83 snapshot, 3.0-4.5 GB**
  su **15 GB liberi** *(disco al 97 %)*;
- **il costo misurato**: `2.922 s/passo` → **8.1 ore come LIMITE INFERIORE** per 10.000 passi.

### ⚠ E una regola che sarebbe servita due giorni fa

> **Prima di interpretare QUALUNQUE struttura vista in un pannello, verificare che ci siano ARCHI
> in quella regione.**

**Il caso reale:** nel run a `sep = 8` il pannello del campo mostrava interferenza **fra le masse**,
e le masse stavano in **quattro componenti connesse con ZERO archi fra loro** *(`Z65`)*. Il
pannello non mentiva — `campo_spaziale` somma su **tutti i nodi**, non sugli archi — **ma la
lettura sì.** Il tool del video (`csv/_test_fork/_video_da_snapshot.py`) stampa il conteggio degli
archi fra componenti **su ogni frame**, proprio per questo.

---

## 2026-09-20 (sera) — **L'ORDINE SI ALLUNGA: ① → ② → ③ → ④**

```
①  LE GUARDIE                      CHIUSO   Z67 (5/5) · Z68 (3/3) · Z69 (3/4 + 1 atteso)
②  IL PANNELLO FEDELE              prossimo
③  LE METRICHE DEL SETTORE CHIRALE + un giro breve a sep = 4.0
④  IL RUN LUNGO a sep = 4.0        per ultimo
```

**Le metriche vanno PRIMA del run: otto ore senza i dati che servono sarebbero da rifare.**

### ⚠ E l'`83 %` a `-1` del passo 2700 NON VALE — ma non per la ragione che sembrava

**Non è (solo) che il grafo fosse in quattro componenti scollegate.** È che **`perc_chi` non è un
lignaggio**: con `CHI_BASC = 1` *(ed era `1` nel run)* la riga `:3765` **riscrive l'intero array a
ogni passo** da `twn > PHI_CRIT`.

> **Quell'`83 %` è la frazione di nodi che NON hanno completato un giro di olonomia.**
> **È un dato sulla TORSIONE, letto come se fosse un dato sulla CHIRALITÀ.**

**E l'eredità chirale della mitosi (`:4294`) e la coppia opposta di Schwinger (`:4415`) sono
appese DOPO `chi_basc` nel ciclo, quindi sopravvivono ESATTAMENTE ZERO passi completi.**
*(Dettaglio e righe in `doc/TASK_HISTORY/2026-09-20_metriche-settore-chirale.md`.)*

### La voce TODO del ② — il pannello fedele

> **✅ ASSORBITA il 2026-09-20 in «IL SOSPESO — LA LISTA UNICA», voce `A5`.**
> Il testo resta: contiene i VINCOLI, che la lista non ripete.

**Il problema, misurato:** `campo_spaziale` somma su **tutti i nodi** con la FFT; `calcola_psi`
solo **sugli archi**. Nel run a `sep = 8` il pannello mostrava interferenza **fra masse in quattro
componenti con zero archi fra loro**.
**Cosa fare:** **un pannello IN PIÙ** che **interpola `psi`** sulla stessa griglia. **Entrambi
restano** — `campo_spaziale` dà **continuità**, l'interpolazione dà **fedeltà**, il grafo dà la
**topologia**.
**Vincoli:** non si tocca `campo_spaziale` né la FFT · **il blob del simulatore NON cambia: è
rendering** · **l'interpolazione LEGGE `psi`, non lo RICALCOLA** *(precedente `lambda_vuoto`)* · i
buchi si **dichiarano** · uno smoothing, se serve, ha la scala **derivata** · **si misura il costo.**

---

# IL SOSPESO — **LA LISTA UNICA** (censita il 2026-09-20, verificata DAL DISCO)

> **Questa è LA lista.** Le tre liste parziali che esistevano prima — *«DA FARE A RUN FINITO»*,
> *«Cosa resta da fare quando il run è definitivamente chiuso»*, *«La voce TODO del ② — il pannello
> fedele»* — **sono ASSORBITE qui** e portano un rimando. **Non se ne apre una quarta.**

**⚠ COME È STATA FATTA, perché cambia quanto ci si può fidare:** l'elenco di partenza veniva dalla
conversazione. **Ogni voce è stata verificata dal disco**, e la verifica ha prodotto **tre
correzioni all'elenco di partenza e due miei errori** *(§ «Cosa la verifica ha cambiato»)*.

### La legenda della validità — **il presidio contro le tre ritrattazioni di oggi**

```
VALE SEMPRE            un difetto di codice, una legge, un fatto letto dal sorgente
VALE PER QUELLA SCENA  un numero misurato su sep = 8 / quattro componenti / una finestra
DA RIVERIFICARE        la premessa sotto è cambiata (scena nuova, blob nuovo, cura applicata)
```
**Il discriminante è una domanda sola:** *«se rigirassi questo su un'altra scena, il numero
cambierebbe?»* Se sì → `VALE PER QUELLA SCENA`. Se la domanda non ha senso perché non c'è un numero
(è una lettura del codice) → `VALE SEMPRE`.

---

## A — LASCIATE A METÀ OGGI (2026-09-20)

| # | la voce | dove sta | a che punto è | cosa manca | chi decide | validità |
|---|---|---|---|---|---|---|
| **A1** | **la catena a TRE VIE di `step`** — `if CHI_CORE… / elif VERSO_CHI… / elif not(…)` | **`:3623` · `:3626` · `:3632`** *(⚠ era citata `:3517`-`:3526`: **slittata di 106 righe**, ritrovata per CONTENUTO)*; `doc/REFERTO_classifica_18_guardie.md` righe 25-27, 90-91 | **né applicata né scartata.** Verificato: **nessun contatore** sulla catena, mentre la gemella `:2366` ne ha quattro | **la FORMA**: tre contatori `_salti` (uno per ramo) **oppure** uno con tre conteggi «quale ramo». Io avevo già dichiarato di preferire **nessuno dei due** *(un contatore per ramo su una scelta a tre vie non misura un fallimento, misura una selezione)* — e l'avevo dichiarata come **mia deviazione dal mandato** | **LUCA** | `VALE SEMPRE` |
| **A2** | **l'anello `A6` di `Z70`** — periodo 2, via `chiralita_core_locale`/`CHI_CORE` | `doc/RAMIFICAZIONI.md` `Z70` | **registrato, NON curato.** `A6` nella sua *lettera* non è violato (ogni gamba legge lo snapshot d'inizio passo), ma `perc_chi` è **schiava** di `tw` | la cura è **un giro a sé** e non è stata fatta | **LUCA** *(è una cura, non una misura)* | `VALE SEMPRE` |
| **A3** | **`Z71` — la carica chirale non si conserva** | `doc/RAMIFICAZIONI.md` `Z71` | **APERTA.** I due punti di scrittura sono verificati dal codice: **`:4294`** eredita UGUALE *(rompe)*, **`:4415`** antinodo OPPOSTO *(conserva)* | **una decisione di FISICA**: *la carica chirale deve conservarsi?* Se sì `:4294` è un difetto; se no, è il meccanismo. **Non si cura senza quella decisione** | **LUCA** | `VALE SEMPRE` |
| **A4** | **le METRICHE DEL SETTORE CHIRALE** | **`doc/TASK_HISTORY/2026-09-20_metriche-settore-chirale.md`** *(⚠ il documento **ESISTE**: vedi i miei errori, §E)* | **punto 1 del TODO fatto** *(il §1 verificato dal codice)*; **punti 2-5 aperti** | il pannello fedele **viene prima** *(è `A5`)*, poi le metriche byte-inerti, il sigillo, la voce nel registro | **io** | **`DA RIVERIFICARE`** — la metrica ④ era *«flip di `chi_basc`»* e **non è misurabile così**; ma **nel ramo B del run in corso `chi_basc` è SPENTO, quindi `perc_chi` È una carica** e la metrica torna misurabile nella forma «confronto di `perc_chi` prima/dopo» |
| **A5** | **il PANNELLO FEDELE** *(interpolazione di `psi` accanto a `campo_spaziale`)* | la **ex-LISTA 3** di questo file | **non iniziato** | un pannello **in più**, che **legge** `psi` e non lo ricalcola; i buchi dichiarati; il costo misurato. Il blob del simulatore **non cambia: è rendering** | **io** | `VALE SEMPRE` |
| **A6** | **`perc_chi` FA DUE LAVORI CON REGOLE OPPOSTE: `chi_basc` lo tratta da CHIRALITA', `TEMPO_SEGNO` da CARICA** — e finche' condividono un array **nessuno dei due puo' essere fatto bene** | `:3558` *(`TEMPO_SEGNO` legge `perc_chi` e ne ricava il VERSO DEL TEMPO)* · `:3765` *(`chi_basc` lo RISCRIVE a ogni passo dalla torsione)* · `:4294` / `:4466` *(le nascite)* · `Z70` `Z71` `Z73` | **REGISTRATA il 2026-09-20, NON iniziata.** **Nasce da un RAGIONAMENTO, non da una misura**, e va letta come tale | **LA PROPOSTA — da decidere, NON eseguita:** separare in **due grandezze**: una **CARICA** nuova, **scritta SOLO alla nascita e mai ricalcolata**, **opposta nelle coppie di Schwinger** (`:4466`), **letta da `TEMPO_SEGNO`**; e **`perc_chi` lasciata libera di essere GEOMETRIA**. *(Il nome della carica nuova NON lo invento: e' una scelta di progetto.)* **⚠ E LA FISICA DISTINGUE DAVVERO LE DUE COSE: la chiralita' NON si conserva** *(una particella con massa la cambia viaggiando)*, **una carica si' — sempre.** **Il NOME e' quello della prima, l'USO di `TEMPO_SEGNO` e' quello della seconda.** **⚠ PERCHE' LA DECISIONE CAMBIA RISPETTO A PRIMA:** la separazione in due array era gia' stata valutata e **SCARTATA**, con la ragione che la seconda grandezza sarebbe rimasta **SENZA LETTORI** — cioe' `A8`, un ramo silenzioso. **Un lettore ora c'e': `TEMPO_SEGNO` (`:3558`).** **⚠⚠ MA VERIFICATO DAL DISCO, E VA DETTO: `TEMPO_SEGNO = False` di default (`:858`), e il driver dei due run A/B NON lo passa — quindi nei run era SPENTO.** **Il lettore esiste nel CODICE ed e' INERTE nei fatti: la ragione dello scarto e' decaduta a META', non del tutto.** **COSA SISTEMEREBBE:** **`Z71`** *(la carica non si conserva: `:4294` eredita UGUALE e rompe, `:4415` OPPOSTA e conserva)* **diventerebbe una domanda DECIDIBILE invece che ambigua**; l'ambiguita' **`A10`** *(un solo significato per grandezza)*; e la domanda **«ogni nascita deve essere una COPPIA?»**, che e' `Z71` in un'altra forma — **se `perc_chi` e' una carica la coppia e' obbligata, se e' un'etichetta no.** **⚠ E COSA NON SISTEMEREBBE, verificato e non assunto: NON tocca il problema di `d0`.** La **coesione relazionale** (`:4877`), che nella traccia risulta **dominante e in giu'** (`-3.68e+03` su 120 passi), lavora su **geometria pura** — `cos2 = (r_rad/H)^2`, `radiale = grav*cos2` — **e `memoria_hebbiana_moto` (righe `4694-5016`) contiene ZERO occorrenze di `perc_chi`.** **I due problemi sono INDIPENDENTI e si curano separatamente**, e lo scrivo perche' domani non vengano legati per comodita' | **LUCA** — **e' una decisione di FISICA, non di codice** | 🟩`VALE SEMPRE` |

---

## B — APERTE DA PRIMA

| # | la voce | dove sta | a che punto è | cosa manca | chi decide | validità |
|---|---|---|---|---|---|---|
| **B1** | **`Z47` — `pos` nella fisica: l'ultimo SFONDO** | `doc/RAMIFICAZIONI.md` `Z47`, `doc/ASSIOMI.md` | **NON INIZIATO**, e il registro lo qualifica già *«progetto di lungo periodo»* | **il costo DECIDE**: non è una modifica, è la **riscrittura di QUATTRO settori** | **LUCA** | `VALE SEMPRE` |
| **B2** | **`Z31` — i sigilli non ri-girabili** | `Z31`, citata in **17 file** | **rifatta TRE volte**, l'ultima ieri | il recupero sistematico → **è il §2.2 del mandato di oggi**, in corso | **io** | `VALE SEMPRE` |
| **B3** | **i rami di `memoria_hebbiana_moto`** | `soliton_simulator.py:4616-4918` | **mai guardati** | ⚠ **sono `25`, non `23`** *(contati dal codice: `if`/`elif`/`else`/`try`/`except` nel corpo della funzione, 303 righe)*. Quanti siano su un **percorso fisico** non è misurato | **io** | `VALE SEMPRE` |
| **B4** | **i `np.zeros`** | tutto il simulatore | **mai guardati** | ⚠ **sono `116`, non `~10`**. Il numero utile non è questo: serve **restringere al percorso fisico**, e quel conto **non esiste ancora** | **io** | `VALE SEMPRE` |
| **B5** | **`theta` / l'aliasing del settore di spin** | `CLAUDE.md` §9, registro `C14`, fronte `A` | **aperto e noto**: `theta` ~ 39-129 giri/passo | `C14` chiude solo con `theta` sotto il tetto `2π·cs/λ`. **È il collo di bottiglia del programma** | **LUCA** *(è la voce `A`)* | `VALE SEMPRE` |
| **B6** | **le due cure OFF: `COPPIA_RECIPROCA` e `GRAV_AMPIEZZA`** | `:739` e `:732` *(entrambe `= False`)*, `doc/REFERTO_somme.md`, due task history del 19/9 | **A/B NEGATIVI** — ma fatti su **QUATTRO COMPONENTI SCOLLEGATE** | **rifare gli A/B sulla scena connessa `sep = 4.0`** | **io** | **`DA RIVERIFICARE`** |
| **B7** | **i reperti DA RIMISURARE sulla scena nuova** | `Z43`, `Z46`, `Z48`-`Z52`, `coer_g` | **misurati su `sep = 8`** | rimisura sulla scena connessa. **Marcatura già presente su 4 su 7**: `Z48`/`Z50`/`Z51` portano «QUALIFICATA», `Z49` dice «scena VIDEO»; **`Z46` non porta NESSUNA marcatura** | **io** | **`VALE PER QUELLA SCENA`** |
| **B8** | **⚠ IL BLOCCO DEL RUN A 6000 AL PASSO 2700** | **`doc/REFERTO_blocco_run6000.md`** *(131 righe)*, `csv/_test_fork/_dump_2700.txt` | ⚠ **NON «mai diagnosticato»: PARZIALMENTE diagnosticato.** **Sei** ipotesi **escluse misurandole** *(memoria, disco, CFL, `MAX_NODI`, `NaN`, contatori)*; la degenerazione documentata *(`d0` max `43 → 395`, `1227` archi sopra `10×p50`)*; lo **stato al 2700 CATTURATO** (45 snapshot + dump di 113 chiavi). **Ciò che NON fu catturato è lo STACK** | **la causa resta ③ «non lo so»**, dichiarata come tale nel referto | **io** | `VALE PER QUELLA SCENA` *(i numeri)* + `VALE SEMPRE` *(le esclusioni)* |
| **B9** | **`Z63` / `Z64`** — i 1455 nodi a `10⁻¹³`; la catena `f → x → r` che non riproduce `r` | registro, **ex-LISTA 2 punto 3** | aperti | vedi le rispettive voci | **io** | `VALE PER QUELLA SCENA` |
| **B10** | **⚠ `--override-blob` e la COPIA del driver** | `csv/_test_fork/_scena_video_ripresa.py` *(`e68bb8c5`, 17466 byte)* e `csv/_seal_fork/_ab_reciprocita.py` | ⚠ **DUE fatti nuovi.** ① **`--override-blob` NON è nel driver vero** *(`0` occorrenze in `_scena_video.py`)*: la ex-LISTA 2 punto 2 **puntava al bersaglio sbagliato**. ② **la COPIA `_scena_video_ripresa.py` ESISTE ANCORA ed è tracciata da git**, mentre il docstring del driver vero dice *«la copia è stata rimossa»* | **un docstring STALE** *(la classe di difetto che `CLAUDE.md` §0 chiama per nome)*, e **un secondo driver nel repo che porta un presidio deliberatamente indebolito** | **io** *(il docstring)* · **LUCA** *(se la copia va tolta)* | `VALE SEMPRE` |

---

## C — CHIUSE DALLA VERIFICA DI OGGI *(tolte dalla lista, e si dice perché)*

| la voce | era | ora | la prova |
|---|---|---|---|
| **ex-LISTA 1** e **ex-LISTA 2 punto 1** — *«riapplicare la patch della ripresa al driver vero»* | **DA FARE A RUN FINITO** | **✅ CHIUSA** | la ripresa **è** nel driver vero *(`10` occorrenze di `--riprendi`/`RIPRENDI` in `_scena_video.py`)*, e il driver attuale `9aee4fc2` la contiene |
| **ex-LISTA 2 punto 2** — *«togliere `--override-blob` dal driver»* | DA FARE | **✅ CHIUSA PER IL DRIVER VERO** *(0 occorrenze)* — **ma resta aperta altrove: → `B10`** | `grep` sul disco |

---

## D — IL CONTO

```
voci sospese CENSITE          15      (5 lasciate a meta' oggi + 10 aperte da prima)
  di cui DECIDE LUCA           5      A1, A2, A3, B1, B5   (+ meta' di B10)
  di cui decido io            10
voci CHIUSE dalla verifica     2      le due ex-liste sulla patch della ripresa
```

**E il registro, misurato nello stesso giro** *(`doc/RAMIFICAZIONI.md`)*:
```
righe-voce                   138
  con un segnale ESPLICITO di apertura      24
  con un segnale ESPLICITO di chiusura      22
  con ENTRAMBI (ambigue)                    19
  MUTE (nessuno dei due)                    73      <- il 53 %
```
> **⚠ Le `73` mute non sono «73 voci aperte»: sono voci il cui stato NON SI LEGGE senza leggerle
> tutte.** È la misura, non il verdetto — e dice che **il registro non è interrogabile
> meccanicamente**.

---

## E — COSA LA VERIFICA HA CAMBIATO, **inclusi due errori miei**

**Tre correzioni all'elenco di partenza:**
1. **il blocco al 2700 NON è «mai diagnosticato»** — c'è un referto di 131 righe con sei ipotesi
   escluse **per misura**. Quello che manca è **lo stack**, non la diagnosi *(→ `B8`)*;
2. **i rami di `memoria_hebbiana_moto` sono `25`, non `23`**, e i `np.zeros` sono **`116`, non
   `~10`** — contati dal codice *(→ `B3`, `B4`)*;
3. **`--override-blob` non è nel driver vero**: il punto della ex-lista puntava al bersaglio
   sbagliato, e il bersaglio giusto è una **copia del driver che doveva essere stata rimossa**
   *(→ `B10`)*.

**Due errori MIEI, dichiarati:**
- ho riportato *«metriche chirali: 0 file»* e *«23 rami: 0 file»*. **Falso in entrambi i casi:** il
  mio `grep` usava `-e "a|b"` **senza `-E`**, quindi l'alternanza era cercata come testo letterale.
  **`doc/TASK_HISTORY/2026-09-20_metriche-settore-chirale.md` ESISTE** *(→ `A4`)*;
- le righe `:3517`-`:3526` che avevo citato **erano slittate di 106 righe** — è il §0 di
  `CLAUDE.md` *(«cerca per NOME, non per riga»)* applicato contro me stesso *(→ `A1`)*.

---

## F — UN PRESIDIO CHE ORA ESISTE DAVVERO: `py-spy`

`doc/REFERTO_blocco_run6000.md` §5 diceva: *«quello che servirebbe è banale e non ce l'ho:
`py-spy dump` legge lo stack di un processo vivo dall'esterno, senza toccarlo. Non è installato.»*

> **Installato oggi (`0.4.2`) ed ESERCITATO su un run VIVO**, non su un test:
> ```
> py-spy dump --pid 9264      (ramo A, mentre gira)
>   chiralita_core_locale (soliton_simulator.py:1556)
>   step (soliton_simulator.py:3624)
>   <module> (_scena_video.py:231)
> ```
> **`A9`: un presidio provato quando NON serve è un presidio; uno scritto e mai esercitato è una
> nota.** La volta scorsa il processo fu ucciso senza catturare lo stack, **e non si saprà mai**.

**PID dei due run in corso: ramo A `9264`, ramo B `30996`.**
**Se uno si pianta — soglia: più di ~1500 s senza uno snapshot nuovo — `py-spy dump` PRIMA di
qualunque altra cosa, e NON si uccide.**

---

## APERTO ab_sep4_A_e_B

- **avvio** `2026-09-20 16:26:43` · **blob** `b44f50ce` · **HEAD** `0f12645`
- **comando**
  ```
  ramo A (chi_basc ON, il default):
  python csv/_test_fork/_scena_video.py 500 csv/_test_fork/_ab_A --sep=4.0 --serie=20 --csv-progresso=csv/_test_fork/_ab_A/prog.csv
ramo B (chi_basc OFF):
  python csv/_test_fork/_scena_video.py 500 csv/_test_fork/_ab_B --sep=4.0 --serie=20 --csv-progresso=csv/_test_fork/_ab_B/prog.csv --chi-basc=off
  ```
- **note** A/B COMPLETO di chi_basc a sep=4.0, i DUE rami IN PARALLELO, 500 frame = 3000 passi ciascuno, uno snapshot ogni 20 frame = 120 passi = 25 per ramo. UNA sola voce per DUE processi perche' sono UN esperimento: un interruttore solo, tutto il resto identico. Geometria verificata alla semina: componenti = 1, archi massa-vuoto = 97590, massa-massa = 0. Disco: 14 GB liberi, stima 1.95 GB. CPU: 6 fisici, parallelo misurato 26.03 s/frame per ramo, stima 3.8-4.5 h. Driver 9aee4fc2, sigillo --chi-basc= 5/5.
- *2026-09-20 19:16:19* — RAMO B FERMATO alle 19:15:26 per decisione di Luca, al frame 65 di 500 (passo 390 di 3000). NON e chiuso l intero esperimento: il ramo A continua, quindi la voce resta APERTA e si chiudera quando A finisce. ARCHIVIO PARZIALE DI B INTATTO E VERIFICATO: 3 snapshot (120, 240, 360), nessun .tmp orfano, tutti caricabili, blob b44f50ce, e il passo nei DATI coincide col nome. MOTIVO: proiezione oltre 33 ore e in peggioramento. CATTURA FINALE PRIMA DELLO STOP, ed e il reperto piu importante dello stop stesso: nsub era passato da 206 a 15594, e IL VINCOLO VINCENTE ERA CAMBIATO -- n3 (|vd|) fermo a 205, ma n1 (la SORGENTE) esploso a 15594. Seconda fase della divergenza, che si sarebbe persa uccidendo senza catturare. File: csv/_test_fork/_diag_B/stack_FINALE_1915.txt

**chiuso 2026-09-20 20:21:06 — FINITO** ESITO ASIMMETRICO, e sono due esiti diversi non uno. RAMO A (chi_basc ACCESO): ARRIVATO INTATTO ai 3000 passi alle 20:20 circa. 500 frame, 28.014 s/frame medio, n da 2391 a 18000, archi 546792, coer_l finale 0.7324, dil +126.96 per cento. 25 snapshot su 25 scritti, 0 saltati, 0 FALLITI, 0.97 GB. Il costo per frame e cresciuto da 27.457 a 28.015, cioe del 2 per cento su 3000 passi: PIATTO. nsub restava 4, il pavimento. RAMO B (chi_basc SPENTO): FERMATO da Luca alle 19:15 al frame 65 di 500, passo 390 di 3000, con nsub a 15594 e proiezione oltre 73 ore. 3 snapshot intatti e verificati. LIMITE DA TENERE: UN SEME PER RAMO, quindi la differenza NON e attribuibile a chi_basc -- il nullo di un confronto fra bracci e la dispersione FRA SEMI, che questo esperimento non misura. Referti: REFERTO_ramoB_sottopassi_CFL, REFERTO_fuga_vd_ramoB, REFERTO_venti_archi_e_nsub, REFERTO_innesco_cinque, REFERTO_rigiocata_0_120. Voci: Z74 Z75 Z76 Z77, piu Z73 corretta in loco due volte.
