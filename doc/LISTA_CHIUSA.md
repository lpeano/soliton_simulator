# 📋 **LA LISTA CHIUSA — BOZZA PER L'APPROVAZIONE DI LUCA**

*(Mandato globale `0c42925`, parte 1. **Generata** da `csv/_lista_chiusa.py` leggendo la tabella
dei difetti acclarati di `doc/STATO_RUN.md`: **nessuna riga e' ricopiata a mano** (`P1-ter`).)*

> ## ⚠ **NON E' ANCORA UNA LISTA CHIUSA: E' UNA PROPOSTA.**
> **Diventa la linea d'arrivo solo quando Luca la APPROVA.** Finche' non lo e', **non vale il
> vincolo che vieta le indagini nuove**, e non si comincia a spuntarla.

**COSA E' GENERATO E COSA E' MIO GIUDIZIO, perche' la differenza conta:**

| | |
|---|---|
| **generato dal file** | l'`ID`, la riga del difetto, la prova, il campo `cura`, lo stato |
| **giudizio MIO, da correggere** | **la FAMIGLIA** di ciascun difetto e la **dimensione**: stanno in `FAMIGLIA_DI` dentro lo script, **una riga per ID**, cosi' si cambiano in un posto solo |

```
difetti acclarati in tabella       38
APERTI o con CURA DERIVATA         24   <- LA LISTA
gia' CURATI / non-difetti          14   <- fuori, ma restano in tabella (non si cancellano)
voci di coda non-difetto           13   <- strumenti, domande, misure da rifare
```

---

## LE SETTE FAMIGLIE

| | famiglia | cosa raccoglie |
|---|---|---|
| **A** | **INERZIA E AVVIO** | l'inerzia spinoriale, il contrasto, la rampa, cio' che decide come nasce un nodo |
| **B** | **TEMPO UNICO** | un solo orologio: `dt_n`/`dt_e` contro `DT` nudo, e le medie d'arco |
| **C** | **DOPPIA COPERTURA E CREAZIONE** | la fase su `2pi`/`4pi`, la mitosi, Schwinger, cio' che eredita |
| **D** | **SOGLIE TARATE E SOTTO PLANCK** | `A11`: ogni clip, pavimento o tetto che non esprima un vincolo dichiarato, e ogni soglia in unita' assolute invece che in frazione del dominio |
| **E** | **DISEGNO E STATISTICHE GLOBALI** | `A2`/`A5`: mediane e medie globali dentro una legge locale, e il disegno che entra nella fisica |
| **F** | **FRENO E CONTRAZIONE** | `SCALA_MIN`, il freno a senso unico, la coesione, cio' che tiene o comprime le distanze |
| **G** | **ARRETRATO DEGLI STRUMENTI** | presidi, ancore, reperti, ripresa: **non e' fisica**, ed e' cio' che rende il resto verificabile |

> **L'ORDINE FRA LE FAMIGLIE E' UNA PROPOSTA, e ha una ragione:** **`A`** prima perche' l'inerzia
> entra in **ogni** passo di **ogni** nodo, e una misura fatta con l'inerzia sbagliata va rifatta;
> **`G`** per ultima **no**: va **in parallelo**, perche' e' cio' che rende verificabile tutto il
> resto e **non produce numeri di fisica**. **Le altre cinque le ordina Luca.**

---

## FAMIGLIA **A** — INERZIA E AVVIO   *(1 difetto, 5 voci di coda)*

| ID | il difetto | stato | cura proposta | prova |
|---|---|---|---|---|
| **D29** | **CINQUE NODI DI VUOTO sono i piu' connessi dell'intero sistema**: il vuoto ha degli HUB, e non dovrebbe averne | `APERTO` | — | `Z77` |

**Voci di coda che NON sono difetti acclarati** *(strumenti, domande, misure da rifare)*:

| voce | dal | cosa |
|---|---|---|
| **RAMPA-2** | 2026-09-25 | `_cs_nodo_prev` non e' inizializzata: la cache parte assente e il primo passo cade sul fallback |
| **RAMPA-2/c** | 2026-09-25 | la candidata di Luca: inizializzare valutando **la stessa legge** sullo stato iniziale |
| **OMEGA-ETA** | 2026-09-26 | il rapporto `|omega|` figlio/maturo **sale con l'eta'** (`1.05 -> 1.86` fra eta' 2 e 14): **da seguire nel run base, NON una cura** *(Luca)* |
| **COPPIA-RAMP** | 2026-09-26 | la coppia **non porta `ramp`** (`^0.15`, `^0.04`) mentre il peso d'arco porta `ramp_i*ramp_j`: **domanda aperta, non cura** |
| **INERZIA-1(C)** | 2026-09-25 | la cura per **conteggio** e' giusta e insufficiente; superata dalla **CURA A** (`rho_s/W^2`), che resta da **sigillare a 4 semi anche su `C2`** |

---

## FAMIGLIA **B** — TEMPO UNICO   *(3 difetti, 0 voci di coda)*

| ID | il difetto | stato | cura proposta | prova |
|---|---|---|---|---|
| **D04** | **`_smp_chiudi()` RISCRIVE tutto `d0` a fine passo e NON ha nessun `_traccia_d0` attorno: e' una scrittura invisibile alla traccia** | `APERTO` | **un sito di traccia** *(o il bilancio come presidio)* | lettura del sorgente `:3677`, commit `0989b78` · e' il buco che in `Z107` lasciava il bilancio aperto |
| **D12** | **`1755 MB` di `.pkl` non hanno il comando che li rigenera** *(par.5-quinquies: «un dato che nessuno potra' rifare»)* | `APERTO` | — | `Z89` |
| **D21** | `_floor_d0` e' SOSPESA, e **i due rami violano assiomi DIVERSI**: la scelta non e' stata fatta | `APERTO` | — | `Z4` |

---

## FAMIGLIA **C** — DOPPIA COPERTURA E CREAZIONE   *(4 difetti, 0 voci di coda)*

| ID | il difetto | stato | cura proposta | prova |
|---|---|---|---|---|
| **D09** | **`chi_basc` BLOCCA la mitosi e DIMEZZA l'olonomia netta: fa l'OPPOSTO del suo scopo dichiarato** | `APERTO` | — | `Z73` |
| **D10** | **`nsub` governa il costo dell'intero sistema ed e' INVISIBILE: nessun contatore, nessuna colonna** | `APERTO` | — | `Z75` |
| **D11** | **`d` scende DIECI VOLTE sotto `LAM` mentre `SCALA_MIN` e' acceso, e la causa NON e' trovata** | `APERTO` | — | `Z87` |
| **D35** | **L'antiparticella di Schwinger nasce con `+2π` (`:5443`) e nel campo `F = Σ exp(iφ)` E' IDENTICA alla particella, non opposta. Il commento dice `+π`** | `APERTO` | **DIPENDE DA §`B1`** *(che cosa e' `φ`)*: **non si corregge prima della decisione di Luca… | `Z119`: letto dal sorgente · **il ramo E' ATTIVO**, `COPPIA_MIT = 1.0`, e `S07_schwinger` scatta `90`-`172` v… |

---

## FAMIGLIA **D** — SOGLIE TARATE E SOTTO PLANCK   *(6 difetti, 0 voci di coda)*

| ID | il difetto | stato | cura proposta | prova |
|---|---|---|---|---|
| **D03** | **La memoria del moto prende le direzioni da `pos`, normalizza su `Imed` GLOBALE, e ha un tetto `0.01*median(d0)`** | `CURA DERIVATA` | **`MEM_ARCO`** | `Z104` `f80503c`, letto da `:5631-5648` · `A1` + `A2` + `A11` cor.2 e 7 · **`Z112` MISURA il tetto: SATURO ne… |
| **D06** | **`_fatt_cs_ultimo` e' SCRITTO e MAI LETTO** *(quarto caso della stessa famiglia)* | `APERTO` | — | `Z7`, letto dal codice |
| **D07** | **`TAU_A` e' UN SOLO numero per DUE leggi fisiche distinte** | `APERTO` | — | `Z10`, `Z9-bis` |
| **D13** | **I sigilli storici non sono stati rigirati sul blob corrente** | `APERTO` | — | `Z11` |
| **D15** | **`A7`: la carica chirale NON si conserva** | `APERTO` | — | `Z71`, letto dal codice |
| **D20** | La correzione (1) su `inerzia` NON e' stata cablata, e **il gate che la autorizzava aveva misurato UN'ALTRA GRANDEZZA** | `APERTO` | — | `Z1` |

---

## FAMIGLIA **E** — DISEGNO E STATISTICHE GLOBALI   *(5 difetti, 0 voci di coda)*

| ID | il difetto | stato | cura proposta | prova |
|---|---|---|---|---|
| **D01** | **`S09` clippa al passo causale — quindi e' gia' una LUNGHEZZA — e poi moltiplica per `median(d0)`: statistica GLOBALE e lunghezza AL QUADRATO** | `APERTO` | **`SPINTA_LOCALE`** | `G2` `fedda6c`: **`85.05 %`** degli archi-passo saturi, **`99.69 %`** del saldo da incrementi saturi · `Z81`,… |
| **D02** | **`pozzo_grafo` calcola `L` da `self.pos` — IL DISEGNO — mentre il suo docstring dichiara «la distanza REALE»** | `APERTO` | **`POZZO_D`** | `G1` `3c03223`, `Z103`: mediana `L/d` `0.98`→`1.22`, **un arco su quattro oltre il doppio** al passo 600, e *… |
| **D05** | **I residui di `C5`: `I4` scatola nera, `I5` underflow per riga, modalita' fine** | `APERTO` | — | il mandato `C5` e la coda |
| **D08** | **Il terzo ramo di `calcola_psi` (`elif` sotto `REPULS_LEGGE`) e' DICHIARATO, non corretto** | `APERTO` | — | `Z14`, letto dal codice |
| **D23** | **La cucitura dello snapshot FALLISCE su entrambi i fronti**, e si DIMOSTRA perche'. **NON CABLATA** | `APERTO` | — | `Z37` |

---

## FAMIGLIA **F** — FRENO E CONTRAZIONE   *(5 difetti, 0 voci di coda)*

| ID | il difetto | stato | cura proposta | prova |
|---|---|---|---|---|
| **D38** | **`_nasce` (`:3850`) e' gated su `SCALA_MIN or SCALA_MIN_PASSO`: la legge «nessun arco sotto `LAM`» e' VERIFICATA sempre (`E4-LAM`) ma FATTA RISPETTARE ALLA NASCITA da un'OPZIONE** | `APERTO` | **`D-b` di Luca: CURA DELLA SEMINA** -- non deve NASCERE un arco sotto `LAM`; `_nasce` **… | `C1` (2026-09-24, `csv/_seal_fork/_prova_nasce_identita.py`, passo ZERO, un processo per braccio): **identita… |
| **D24** | **`A2` e' VIOLATO da `Lam = mean(I)`** -- una media GLOBALE dentro una legge locale -- **e la violazione e' la ragione per cui il pezzo funziona** | `APERTO` | — | `Z40` |
| **D30** | **`_massa` chiama `semina` SENZA `mass_id` (`:6209`), quindi `masse_info` non viene MAI popolato e `_registra_concorrenza` non parte: negli snapshot di epoca 3 `masse_info` e' VUOTO e `conc_nodi` e' … | `APERTO` | — | lettura del sorgente `:6209` + misurato su `_val600/scena_000120` |
| **D31** | **Il freno di `SCALA_MIN` (`_smp_chiudi`) E' IL MOTORE della crescita di `d0`: vale il `117.41 %` del `Δ`, mentre gli scrittori fisici tirano GIU' per il `-17.43 %`** | `APERTO` | **il freno simmetrico** *(`A11` cor.4)*, **da derivare al `CHK3`** · la **scheda ①** del … | `Z108`: bilancio che **CHIUDE** a `1.138e-13` su **600 passi**, blob `ab685eac` · **promosso da `S02`** · **`… |
| **D32** | **I TEMPI PROPRI DICHIARATI SONO TRE, E SONO TRE GRANDEZZE DIVERSE: `r`, `tau_pp` e `d/cs`.** `corr(r, tau_pp)` fra `-0.25` e `+0.26`, **segno non concorde**; `corr(r, d/cs)` **positiva ovunque** ma … | `APERTO` | **dire QUALE delle due e' il tempo proprio**, nella scheda del registro | `Z110`: 20 snapshot, 4 archivi delle cure, strumento blob `20bd4b3e` · **dal sorgente:** `TEMPO_SEGNO = False… |

---

## FAMIGLIA **G** — ARRETRATO DEGLI STRUMENTI   *(0 difetti, 8 voci di coda)*

**Voci di coda che NON sono difetti acclarati** *(strumenti, domande, misure da rifare)*:

| voce | dal | cosa |
|---|---|---|
| **RIPRESA-ARGV** | 2026-09-26 | la ripresa si fida del BLOB, e il blob non certifica l'ARGV: un json con la configurazione sbagliata verrebbe RIPRESO |
| **REPERTI-IMMUTABILI** | 2026-09-26 | un file archiviato con un sigillo e citato da un referto non deve poter cambiare in silenzio (caso reale: `e062fdb`) |
| **P1BIS-DELTA** | 2026-09-25 | il hook di `P1-bis` verifica la PRESENZA di `RELAZIONE_PER_CLAUDE.md` fra i file staged, non il suo DELTA (caso `009d49a`) |
| **ANCORE-1** | 2026-09-25 | **43 sigilli** prendono «il codice di prima» da `HEAD` invece che dal PADRE del commit che ha introdotto il flag (`P8`) |
| **CONFIG-1** | 2026-09-25 | le misure (b)-(e) da rifare in configurazione del driver; (a) fatta |
| **CLI-1** | 2026-09-25 | i sigilli delle cure 4 e 5 da rifare **attraverso il CLI**, non impostando il modulo |
| **PRESIDI-RESTO** | 2026-09-25 | `P1`, `P2`, `P4`, `P6` non scritti, piu' l'**arretrato** dei file che non soddisfano `P3`/`P5`/`P7` |
| **P9** | 2026-09-25 | la copia diagnostica si genera al run e il **diff** deve essere verificato: oggi i due blob si stampano, **il diff non lo controlla nessuno** — `P9` e' META' fatto |

---

## ⚠ **I SOSPETTI RESTANO SEPARATI**

Nella coda unica di `doc/STATO_RUN.md` i **sospetti** (`Sxx`) hanno la loro sezione e **non
entrano qui**: un sospetto si **promuove** con la prova (`PROMOSSO: Sxx -> Dyy`) e **solo allora**
puo' entrare in una famiglia. **Metterli nella lista la renderebbe non finibile**, che e'
esattamente cio' che la chiusura deve impedire.

## LE QUATTRO STRADE PER UN DIFETTO NUOVO *(mandato, parte 2)*

```
1. BLOCCA la voce in corso        -> si ferma e si dice
2. INVALIDA la voce in corso      -> la voce torna aperta, la misura non si pubblica
3. STESSA RADICE di una voce      -> entra in QUELLA famiglia, con la conferma di Luca
4. altrimenti                     -> doc/LISTA_DOPO.md, e NON SI TOCCA
```

> **E IL VINCOLO CHE CAMBIA IL MIO COMPORTAMENTO:** finche' la lista e' attiva **non si aprono
> indagini nuove** — inventari, controlli a tappeto, sonde esplorative — **se non servono a una
> voce**. *(Nel solo 2026-09-25 ne avevo aperte cinque: audit di `eta`, audit di `rho_s`,
> `ANCORE-1`, la tabella delle configurazioni, `P7`. Sono state utili, e da ora ciascuna ha
> bisogno di una voce a cui servire.)*

## LA LINEA D'ARRIVO *(mandato, parte 4)*

```
lista VUOTA  ->  BASE: scena (ii)(a), configurazione del driver con TUTTE le cure,
                 4 semi, 600 passi, passo pieno, P5 attivo, referto elencato
             ->  tag  base-epoca-4
             ->  PROVA 1 sulla base, criteri scritti PRIMA
                 (la prima delle tre prove di doc/IPOTESI_gravita_a_spinta.md:
                  IL BERSAGLIO DEL PROGETTO)
```

**E ogni giorno, in `doc/STATO_RUN.md`:** quante **chiuse**, **aperte**, **nuove**, e in quale
strada. **La lista deve ACCORCIARSI: se in un giorno cresce, lo si scrive IN TESTA.**

---

## COSA QUESTA BOZZA *NON* DICE

- **non dice che i difetti aperti siano 24 e non uno di piu'**: dice che **24 righe della tabella
  portano lo stato `APERTO` o `CURA DERIVATA`**. Un difetto che esiste e **non e' in tabella**
  non lo vede nessuno, e la tabella stessa e' stata **ricostruita dai file, non da memoria**.
- **non dice che le famiglie siano le giuste**: sono le sette proposte dal guardiano nel mandato,
  e il mandato dice **di correggerle se i dati dicono altro, dichiarandolo**.
- **non contiene la DIMENSIONE di ciascuna voce**, che il mandato chiede: stimarla richiede di
  leggere il codice di ognuna, ed e' **lavoro, non generazione**. **Manca, e lo dico** invece di
  riempire una colonna con numeri inventati.
- **non e' ordinata per DIPENDENZE dentro la famiglia**: l'ordine e' quello della tabella
  *(decrescente per ID)*. Le dipendenze fra difetti **non sono registrate in un campo**, quindi
  ricavarle sarebbe un giudizio mio riga per riga. **Secondo punto che manca.**
