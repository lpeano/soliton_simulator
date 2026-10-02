> ## ⚠ DAL TAG `epoca-2`: **SISTEMA D**
> **Nuova carica (dallo spinore), scala minima `LAM` su `d` e `d0`, coesione adimensionale e causale** — piu' la **cura del mondo-dopo-i-flag**, che cambia ogni run.
> **Ogni numero misurato PRIMA appartiene all'EPOCA 1 e NON si confronta con l'epoca 2.**
> `EPOCA 2 = blob del simulatore del tag (`4954fe5b`, byte grezzi) + configurazione con `CHI_COOP`, `SCALA_MIN`, `COES_ADIM` ACCESI`. **Un run a flag spenti su quel blob e' ancora EPOCA 1**, e non e' un'opinione: lo provano `Z1` e `Z1c`, byte-identici.

> ### ⚠ CORREZIONE DEL 2026-09-21 — **la frase qui sopra e' IMPRECISA, e la lascio leggibile**
> **Cio' che avevo scritto:** *«un run a flag spenti su quel blob e' ancora EPOCA 1, lo provano `Z1`
> e `Z1c`».* **VALE SOLO CON L'ARGV NUDO.**
> **Perche' e' sbagliata:** `Z1c` confronta contro **«PRIMA + la cura del mondo»**, non contro
> **«PRIMA»** — la cura e' innestata su ENTRAMBI i bracci di proposito, senno' il sigillo misurerebbe
> LEI invece dei tre flag. **Quindi `Z1c` NON dice nulla sull'equivalenza con l'epoca 1.** A dirlo e'
> `Z1b`, che misura la differenza: **`n` 2569 -> 2580, archi 527 308 -> 526 202.** La cura e'
> **categoria D** e fa finalmente agire gli **otto** flag sul vuoto.
>
> **LA CLASSIFICAZIONE CORRETTA, in quattro righe:**
> ```
> EPOCA 1       blob PRECEDENTE al tag, qualunque configurazione
>
> EPOCA 1       blob del tag, argv NUDO, tre flag spenti
>               -> byte-identico, lo prova Z1
>
> EPOCA 1-bis   blob del tag, argv del FORK, tre flag spenti
>               -> NON e' epoca 1: e' epoca 1 CON LA CURA DEL MONDO.
>                  Il vuoto nasce coi flag del run invece che coi default. Lo misura Z1b.
>
> EPOCA 2       blob del tag + CHI_COOP, SCALA_MIN, COES_ADIM ACCESI
> ```
>
> **⚠ LA CONSEGUENZA PRATICA, ed e' operativa:** **i run del FORK di epoca 1 NON si riproducono sul
> blob nuovo, nemmeno a flag spenti** — **e NON E' UN DIFETTO.** Chi vuole rigirarli deve usare il
> **blob PRECEDENTE** (`git cat-file -p <commit>:soliton_simulator.py`, scritto in BINARIO).
>
> **Il tag NON si sposta e NON si riscrive:** un tag pubblicato che cambia sotto i piedi e' peggio
> dell'imprecisione. La correzione vive qui e in una `git notes` sul commit del tag.

---

## L'ARCHIVIO PER GIORNO - **il file vivo tiene SOLO 2026-10-02**

> **Regola di Luca, 2026-09-26.** A 20436 righe questo file non lo leggeva nessuno per intero, **quindi il suo scopo era gia' perso**. I giorni chiusi stanno in `doc/relazioni/`, uno per giorno, e `git log` resta l'indice.
> *(Diviso da `csv/_archivio_relazioni.py`, che dichiara la regola di taglio.)*

| giorno | righe | file |
|---|--:|---|
| `2026-09-14` | 134 | [`doc/relazioni/2026-09-14.md`](doc/relazioni/2026-09-14.md) |
| `2026-09-15` | 1310 | [`doc/relazioni/2026-09-15.md`](doc/relazioni/2026-09-15.md) |
| `2026-09-16` | 5551 | [`doc/relazioni/2026-09-16.md`](doc/relazioni/2026-09-16.md) |
| `2026-09-19` | 555 | [`doc/relazioni/2026-09-19.md`](doc/relazioni/2026-09-19.md) |
| `2026-09-20` | 1444 | [`doc/relazioni/2026-09-20.md`](doc/relazioni/2026-09-20.md) |
| `2026-09-21` | 5371 | [`doc/relazioni/2026-09-21.md`](doc/relazioni/2026-09-21.md) |
| `2026-09-24` | 1360 | [`doc/relazioni/2026-09-24.md`](doc/relazioni/2026-09-24.md) |
| `2026-09-25` | 3094 | [`doc/relazioni/2026-09-25.md`](doc/relazioni/2026-09-25.md) |
| `2026-09-26` | 2214 | [`doc/relazioni/2026-09-26.md`](doc/relazioni/2026-09-26.md) |
| `2026-09-27` | 2787 | [`doc/relazioni/2026-09-27.md`](doc/relazioni/2026-09-27.md) |
| `2026-09-28` | 1707 | [`doc/relazioni/2026-09-28.md`](doc/relazioni/2026-09-28.md) |
| `2026-09-29` | 1122 | [`doc/relazioni/2026-09-29.md`](doc/relazioni/2026-09-29.md) |
| `2026-10-01` | 1519 | [`doc/relazioni/2026-10-01.md`](doc/relazioni/2026-10-01.md) |

---

# 📁 **PASSO 1: LA RELAZIONE E' ARCHIVIATA PER GIORNO, e lo strumento aveva DUE difetti** *(2026-10-02)*

> ### **Luca, la violazione del par.4 piu' vecchia della coda e' chiusa: il file vivo tiene SOLO oggi.**

**Nessuna riga del simulatore:** blob **`3ddc56d9`** prima e dopo *(sha1 dei byte grezzi)*.

## ✅ **LO STATO, verificato PRIMA di toccare qualunque cosa**

| | |
|---|---|
| `HEAD` | **`e4993ab`**, e coincide con `origin/fork-su2`: ### **atteso, e torna** |
| blob del simulatore sul **disco** | ### **`3ddc56d9`** *(sha1 byte grezzi)* — ### **atteso, e torna** |
| e il disco coincide col **committato** | `git hash-object` da' **`00c6437a`** = `git rev-parse HEAD:soliton_simulator.py`: ### **par.7 stato 1**, il caso normale |

### ⚠ **E le due convenzioni di hash danno due numeri DIVERSI dello stesso file** *(par.2)*: `3ddc56d9` e' il sha1 dei **byte grezzi** *(quello dei presidi e dei referti)*, `00c6437a` e' `git hash-object` *(che applica il filtro `clean`)*. **Sono lo stesso file.**

## 📊 **I NUMERI DELL'ARCHIVIO** *(generati dallo strumento, non ricopiati)*

| | |
|---|---|
| file vivo | da ### **9407 a 61 righe** |
| giorni staccati | **5**: `2026-09-26` *(2214)* · `2026-09-27` *(2787)* · `2026-09-28` *(1707)* · `2026-09-29` *(1122)* · `2026-10-01` *(1519)* |
| gli **8 giorni** dal `2026-09-14` al `2026-09-25` | ### **NON riscritti** — non sono fra i giorni riconosciuti, e lo strumento dice *«SCRITTI 5 file»* |
| conservazione delle righe | ### **9408 in ingresso = 9408 in uscita** *(preambolo 38 + indice scartato 21 + i 5 giorni)* |

### ✅ **E UN CONTROLLO INDIPENDENTE, perche' il conto dello strumento prova solo se stesso**
Ho confrontato il **multiset delle righe non vuote** fra il file a `HEAD` e *(file vivo + i 5 file d'archivio senza le loro 4 righe d'intestazione)*: **7026 contro 7032**, e le **sette** differenze sono ### **esattamente le righe dell'indice rigenerato** *(l'intestazione col giorno nuovo, le 5 righe di tabella nuove, il segnaposto di oggi)*, piu' **una persa** che e' l'intestazione dell'indice col giorno vecchio.
### ➜ **Nessuna riga di CONTENUTO e' persa o cambiata.** *(`L-NUMERI`: il conto dello strumento e la verifica vengono da due conti diversi.)*

## ⛔ **DIFETTO 1 DELLO STRUMENTO: l'indice dell'archivio finiva DENTRO un giorno**

L'intestazione che lo strumento genera e' `## L'ARCHIVIO PER GIORNO - **il file vivo tiene SOLO 2026-09-26**`, e ### **CONTIENE UNA DATA.** La regola di taglio taglia su *«ogni intestazione che contiene una data»*: quindi ### **l'indice di COME SI LEGGE la relazione veniva archiviato come se fosse un fatto del 2026-09-26.**
### ➜ **Cura:** il blocco si **scarta prima del taglio** e si **rigenera**; e se i blocchi non sono esattamente **UNO** lo strumento ### **si ferma senza toccare niente** (`A9`).
### ⚠ **E la regola nuova e' basata sul TESTO, lo dichiaro:** vale perche' quel testo lo scrive **questa stessa funzione**. Il presidio contro la fragilita' non e' la mia attenzione: e' che **un numero di blocchi diverso da 1 FERMA il giro.**

## ⛔ **DIFETTO 2, e l'ho trovato GUARDANDO IL MIO OUTPUT prima di committarlo**

Il primo giro ha prodotto ### **due `---` di fila.** Causa: il blocco dell'indice viveva **fra** un `---` del preambolo e un `---` suo; da quando lo scarto, il `---` del preambolo **resta nel preambolo** e `testa_viva` ne aggiunge un altro.
### ➜ **Non e' cosmetico: lo strumento cosi' NON era IDEMPOTENTE** — a ogni rilancio il file avrebbe guadagnato una riga che nessuno ha deciso.
### ✅ **Curato in un commit a se'** *(par.5: la correzione non si infila nel commit dell'output)*, e il giro vero e' stato **rifatto dal blob di `HEAD` ripristinato in BINARIO** *(par.7: **non** `git checkout`)*.

## ⚠ **E IL TERZO, che era GIA' nello strumento e che la cura ha dovuto prendere**

`testa_viva` costruiva la tabella dai **soli giorni presenti nel file vivo**: ### **le 8 righe dei giorni dal `2026-09-14` al `2026-09-25` sarebbero SPARITE.** Ora i loro conteggi si **ricopiano dalla tabella vecchia**, e ### **non si ricalcolano dai file**: quei file hanno **4 righe d'intestazione d'archivio** in testa, quindi un conteggio rifatto darebbe un numero **diverso** da quello che il giorno aveva — cioe' ### **un numero inventato** (`L-NUMERI`).

## 📖 **CHE COSA HO LETTO, e che cosa NON ho letto per intero — lo dico invece di lasciarlo supporre**

| | |
|---|---|
| **per intero** | `2026-10-01` *(1519 righe)* e `2026-09-29` *(1122)* |
| **in larga parte** | `2026-09-28` e `2026-09-27` |
| ### **NON per intero** | ### **`2026-09-26`**: ne ho letto **le intestazioni e le righe di conclusione** *(`#`, `✅`, `⛔`, `⚠`, `📌`, `🎯`, `➜`)*, non il corpo |
| **i documenti, per intero** | `doc/PIANO_riordino_mitosi.md` · `doc/MITOSI_storia.md` · `doc/PIANO_divisione_e_calore.md` · `doc/REGOLE_nascita.tsv` · la **visione** e la **stella polare** in `doc/REGISTRO_FISICA.md` · le **11 voci** dell'indice chieste · la coda di `doc/INVENTARIO_strumenti.md` |

### ➜ **Perche' lo dichiaro:** il `2026-09-26` e' il giorno dell'**indice** e della **lista chiusa**, e le sue conclusioni vivono in `CLAUDE.md` par.9, nell'indice e nell'inventario — ### **che ho letto.** Ma *«l'ho letto»* vale solo se dico **che cosa**, ed e' la lezione di `dir_laterale` del 2026-10-01: ### **una verifica dichiarata su cio' che non si e' guardato e' peggio di una non fatta.**

---

