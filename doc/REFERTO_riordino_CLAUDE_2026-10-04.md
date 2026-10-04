# REFERTO — **`CLAUDE.md` diventa l'indice delle regole** *(2026-10-04)*

**Mandato:** decisione di Luca del 2026-10-04 — *«CLAUDE.md diventa l'INDICE delle regole,
con i dettagli fuori, in una struttura che NON puo' creare loop»*.
**Task history** *(committato PRIMA, par.8)*:
`doc/TASK_HISTORY/2026-10-04_claude-md-indice-delle-regole.md`, in `f32f235`.
**Base di confronto:** `da79cc1` — `CLAUDE.md` a **391** righe, **NOVE** sotto il tetto
di `H-RIGHE`.

## IL VERDETTO IN UNA RIGA

> ### ✅ **391 → 281 righe (`-110`, il 28% in meno), 12 file di dettaglio, i DUE CONTROLLI
> ### PASSANO, e nessuna regola persa: `titoli 15/15`, `punti 11/11`, `dichiarate 17 → 18`.**

### ⚠ **E L'OBIETTIVO DI LUCA ERA «CIRCA 250»: 281 E' SOPRA.** Non ho tagliato per arrivare
al numero, e il perche' sta nel par.5 di questo referto.

## 1. CHE COSA DICE OGGI LA STRUTTURA

| | |
|---|---|
| **livello 1** | **`CLAUDE.md`** — **solo le regole**, una riga o un punto ciascuna, col **tetto a 400** |
| **livello 2** | **`doc/REGOLE/par<N>.md`** — il **perche'**, i casi, le trappole: **12 file, 745 righe** |
| **gli archi** | **12** in giu' *(un rimando per paragrafo)*, **12** in su *(tutti nell'intestazione)*, ### **ZERO fra due file di dettaglio** |

> ### 📌 **UN SOLO SALTO, SEMPRE.** Da `CLAUDE.md` si arriva al dettaglio in **un** passo,
> e dal dettaglio **non si parte**: ogni file di secondo livello apre con la frase *«non
> contiene regole … non rimanda ad altri file di `doc/REGOLE/`»*, e ### **il controllo `(b)`
> lo VERIFICA invece di crederlo.**

## 2. I NUMERI *(generati da `csv/_numeri_riordino_regole.py`, non ricopiati — `L-NUMERI`)*

```
============================================================================================
  I NUMERI DEL RIORDINO DI CLAUDE.md
============================================================================================

--- LA CURVA, commit per commit -----------------------------------------------------------
  commit     che cosa e' uscito         righe    delta
  da79cc1    PRIMA del riordino           391         
  61b8e5f    lo strumento                 391       +0
  885d9a5    par.12                       368      -23
  dc08221    par.0 + par.4                340      -28
  d1df098    par.6 + par.7                326      -14
  829b4a5    par.9 + par.9-ter            309      -17
  b5e5e99    par.2,3,5,8,11               281      -28
  HEAD       (il commit di oggi)          281       +0
  (disco)    oggi                         281       +0

  TOTALE: 391 -> 281 righe, -110 (28% in meno). Tetto 400, obiettivo ~250.

--- PARAGRAFO PER PARAGRAFO ---------------------------------------------------------------
  paragrafo                                   prima   dopo   delta
  (intestazione)                                 14     12      -2
  0. CHE COSA SI LEGGE ALL'AVVIO                 39     28     -11
  1. IL BERSAGLIO DEL PROGETTO                   15     13      -2
  2. RUOLO E POSTURA                             17     15      -2
  3. LA REGOLA D'ORO                             19     16      -3
  4. TUTTO CIO' CHE SI DICE A LUCA VA ANCHE      40     21     -19
  5. POLITICHE DI COMMIT                         19     18      -1
  6. LE TRE COSE CHE SI AGGIORNANO **NELLO S     35     23     -12
  7. IL CODICE DI UNA MISURA DEV'ESSERE RECU     27     21      -6
  8. IL TASK HISTORY                             20     16      -4
  9. L'INDICE DEI DIFETTI                        30     22      -8
  9-ter. UNA CURA NON AUMENTA IL NUMERO DELL     32     17     -15
  10. IL PRINCIPIO GUIDA                         14     12      -2
  11. LE REGOLE DI LAVORO                        17     18      +1
  12. I PRESIDI AUTOMATICI                       54     30     -24
  (somma dei risparmi)                                        -110

--- I FILE DI DETTAGLIO -------------------------------------------------------------------
  par0.md          71 righe
  par2.md          36 righe
  par3.md          43 righe
  par4.md          63 righe
  par5.md          47 righe
  par6.md          91 righe
  par7.md          61 righe
  par8.md          30 righe
  par9.md          90 righe
  par11.md         81 righe
  par12.md         83 righe
  par9ter.md       49 righe
  TOTALE          745 righe in 12 file
  media 62.1, il piu' lungo 91, il piu' corto 30

--- IL BILANCIO: dove sono andate le righe ------------------------------------------------
  righe uscite da CLAUDE.md                     110
  righe nei file di dettaglio                   745
  rapporto (dettaglio / uscite)                6.77x
  ### il dettaglio e' PIU' LUNGO di cio' che e' uscito: non e' una perdita,
      e' il testo che in CLAUDE.md era COMPRESSO e qui e' scritto per esteso.

--- CHE COSA NON HO CONDENSATO ------------------------------------------------------------
  1. IL BERSAGLIO DEL PROGETTO   13 righe   CONTENUTO (il BERSAGLIO del progetto), non dettaglio
  10. IL PRINCIPIO GUIDA         12 righe   CONTENUTO (la frase che lo GUIDA), non dettaglio
  ### Condensarli vorrebbe dire ACCORCIARE UNA CITAZIONE DI LUCA.

============================================================================================
```

### 📌 **IL NUMERO CHE SPIEGA IL LAVORO E' `6.77x`.** Sono uscite **110** righe da
`CLAUDE.md`, e nei file di dettaglio ce ne sono **745**. ### **Non e' gonfiatura e non e'
invenzione:** quelle righe in `CLAUDE.md` erano **compresse** — una subordinata dentro una
cella di tabella, un *«(vedi il caso …)»* fra parentesi — e nel secondo livello sono
**scritte per esteso**, col caso che le ha generate e la data.
### **Il primo livello ha perso 110 righe di TESTO e ZERO regole; il secondo ne ha guadagnate
745 di SPIEGAZIONE.**

## 3. I DUE CONTROLLI, come Luca li ha chiesti

```
====================================================================================================
LA STRUTTURA DELLE REGOLE -- i due controlli
====================================================================================================
  CLAUDE.md: 281 righe (tetto 400, obiettivo ~250)

----------------------------------------------------------------------------------------------------
(a) CONSERVAZIONE DELLE REGOLE, contro il blob committato da79cc1
    titoli       prima  15   dopo  15
    dichiarate   prima  17   dopo  18
    punti        prima  11   dopo  11
    ### PASSA: nessuna regola persa.
    regole AGGIUNTE (lecito, e si dichiara):
      dichiarate   L-PATCH

----------------------------------------------------------------------------------------------------
(b) NESSUN LOOP -- il grafo dei rimandi
    file in doc/REGOLE: 12
    archi CLAUDE.md -> dettaglio: 12
    archi dettaglio -> CLAUDE.md: 12 (lecito solo nell'intestazione)
    ### PASSA: albero di PROFONDITA' 1, nessuna catena e nessun ciclo.

====================================================================================================
### I DUE CONTROLLI PASSANO.
====================================================================================================
```

### ⛔ **E IL CONTROLLO `(a)` HA UNA DEFINIZIONE, altrimenti non sarebbe un controllo.** Una
*«regola»* e' una delle tre cose che una **macchina** sa contare:

| | |
|---|---|
| **un titolo** | `#` o `##` *(**mai** `###`: in questo file e' **enfasi**, non struttura)* |
| **una riga di tabella** | l'**id fra backtick** nella **prima cella** |
| **un punto numerato** | il **numero** + l'**etichetta in grassetto** che lo apre |

**Il collaudo:** `python csv/_struttura_regole.py --collaudo` — **5 casi iniettati**, fra cui
una copia **con una regola tolta**, che ### **viene SCOPERTA COL NOME**.

## 4. CHE COSA IL CONTROLLO MI HA IMPEDITO DI FARE *(il punto del presidio)*

> ### ⛔ **HO RISCRITTO UNA CITAZIONE DI LUCA, E IL CONTROLLO MI HA PRESO.** Condensando il
> par.9-ter avevo reso il criterio *«a parità di effetto si preferisce togliere
> un'eccezione»* in una forma mia. ### **Il testo fra le virgolette e' di Luca, del
> 2026-09-25: non e' materiale da condensare.** Ripristinato **verbatim**.

**E tre difetti dello strumento, trovati mentre lo usavo** *(piu' uno nel generatore dei
numeri, trovato oggi: una stringa di formato con un `%2d` non sostituito — corretto prima
di questo referto, perche' **un numero stampato male non ha provenienza**)*:

| | che cosa sbagliava | perche' conta |
|---|---|---|
| **①** | **mancava `_presidio.avvia`** | e' morto al **primo giro utile** su un `UnicodeEncodeError`. ### **OTTAVA volta** *(par.7)* |
| **②** | contava `###` come **titolo** | **falso allarme** che avrebbe **fermato il riordino** senza che una regola fosse persa |
| **③** | una **MENZIONE** di un file valeva come **rimando** | avrebbe dichiarato archi che non esistono |
| **④** | la chiave di un punto era la **prosa** | due parole riscritte e il punto risultava *«perso»* |

## 5. LE RIGHE CHE NON HO TOLTO, e perche'

**`281` contro l'obiettivo `~250`: le ultime `31` righe le vedo, e NON le ho tagliate.**

1. **par.1** *(13 righe)* e **par.10** *(12)* sono **CONTENUTO**, non dettaglio di una regola:
   il **bersaglio** del progetto e la frase che lo **guida**. Condensarli vuol dire
   **accorciare una citazione di Luca** — ### **esattamente cio' che il controllo mi ha
   appena impedito di fare.**
2. **par.0** *(28 righe)* e' **due tabelle di percorsi**: ogni riga e' un file che si apre, e
   togliere una riga vuol dire **togliere un file dalla lista di avvio**.
   ### **Non e' compressione, e' una decisione di contenuto.**
3. **par.12** *(30 righe)* e' **la tabella degli undici presidi**, una riga per hook, piu' le
   due vie d'uscita. ### **Un presidio non elencato e' un presidio che nessuno sa di avere.**

> ### 📌 **COSI' LA DECISIONE RESTA DI LUCA, col numero sul tavolo:** per scendere a `250`
> bisogna **togliere una regola o accorciare una citazione**, e ### **nessuna delle due e'
> una decisione che prendo io** *(`L-DOPO-STOP`)*.

## 6. COME SI CRESCE DOPO *(la regola, ed e' SCRITTA, non un presidio)*

**Una regola nuova va in `CLAUDE.md`, nel paragrafo che la ospita** — una riga o un punto.
**Il suo perche', il caso che l'ha generata e le trappole vanno in `doc/REGOLE/par<N>.md`.**
### ⛔ **MAI un terzo livello, e MAI un rimando fra due file di dettaglio.**

### ✅ **E LO STRUMENTO SI RIGIRA A OGNI MODIFICA DI `CLAUDE.md`:** e' il presidio contro il
loop **nel tempo**, non solo durante il riordino.

### ⚠ **MA OGGI NON E' CABLATO** (`A9`): `python csv/_struttura_regole.py` si lancia **a
mano**. Il hook `H-RIGHE` guarda **la lunghezza**, non **la struttura** — ### **un terzo
livello aggiunto domani passerebbe il commit.** *(Candidato a presidio; la decisione e' di
Luca.)*

## 7. UNA MIA OMISSIONE, sanata in questo commit

### ⛔ **`csv/_struttura_regole.py` NON ERA NELL'INVENTARIO.** Il par.6 ① chiede la voce
**nello stesso commit** del file, e il commit dello strumento (`61b8e5f`) non l'ha scritta.
### **E' una regola SCRITTA e non un presidio** *(`A9`, e il par.6 lo dichiara da se')*:
nessun hook l'ha fermata. **Sanata qui, con DUE voci** — lo strumento e il generatore dei
numeri.

## 8. IL DIFETTO DI QUESTO STESSO REFERTO, trovato dopo averlo committato

> ### ⛔ **LA PRIMA VERSIONE DI QUESTO REFERTO (`accb897`) DICEVA `392 → 282`.
> ### I NUMERI VERI SONO `391 → 281`: ogni conteggio di righe era di UNO troppo alto.**

**LA CAUSA, letta dal codice:** i miei due strumenti contavano `testo.count(NL) + 1`.
`H-RIGHE` — ### **il presidio che IMPONE il tetto** — conta in
`csv/_presidio_righe.conta` i **fine-riga**, come `wc -l`: su un file che **termina** con
un fine-riga le due formule differiscono di **uno**.

### 📌 **E IL SEGNALE C'ERA, SCRITTO NEL MANDATO.** Luca aveva scritto
*«CLAUDE.md e' a 391 righe su 400»*; io ho scritto **392** in sei messaggi e in cinque
commit **senza fermarmi sulla differenza**. ### **Un numero che non coincide con quello di
chi te l'ha dato non e' un arrotondamento: e' un conteggio diverso, e va trovato.**

**LA CURA, e non e' una seconda formula corretta:** i due strumenti ora
**`import _presidio_righe`** e chiamano `conta()`. ### ✅ **Il conteggio ha UNA SOLA
definizione nel repo, quindi non puo' piu' divergere da chi impone il tetto.**

### ⚠ **CHE COSA NON CAMBIA, e lo dico perche' e' la meta' onesta della correzione:**
il **delta `-110`** e il **28%** sono gli stessi *(l'errore era identico sui due estremi e
si cancella)*, i **confronti paragrafo per paragrafo** erano gia' giusti *(sono differenze
fra indici di riga, non conteggi di file)*, e ### **nessun verdetto si ribalta** — i due
controlli passavano e passano. ### **Era sbagliato il numero assoluto, non la misura.**

---

## GLI OTTO COMMIT DEL RIORDINO

| commit | che cosa |
|---|---|
| `f32f235` | il **task history**, **prima** del lavoro *(par.8)* |
| `61b8e5f` | **lo strumento**, committato **prima** di girare *(par.5)* |
| `885d9a5` | **par.12** esce *(54 → 30)*, piu' i **tre difetti** dello strumento |
| `dc08221` | **par.0 + par.4** escono *(79 → 49)* |
| `d1df098` | **par.6 + par.7** escono — e il controllo **mi ha bocciato**, con ragione |
| `829b4a5` | **par.9 + par.9-ter** escono — e il controllo **mi ha preso** mentre riscrivevo Luca |
| `b5e5e99` | **par.2, 3, 5, 8, 11** escono, e `L-PATCH` prende **una riga sua** |
| `accb897` | **il referto**, le due voci d'inventario, la relazione |
| *questo* | la **CORREZIONE** dei conteggi: `392 → 282` era `391 → 281` |

### ✅ **L'ORDINE E' VERIFICABILE DA GIT, non asserito da me**, e l'ho verificato con
`git merge-base --is-ancestor`: `f32f235` *(il task history)* e' **antenato di tutti e
sette**, e `61b8e5f` *(lo strumento)* e' antenato di **ognuno dei cinque commit del
riordino che toccano `CLAUDE.md`**.

### ⚠ **E UNA FORMA PIU' FORTE DI QUELLA FRASE SAREBBE FALSA, quindi non la scrivo:**
`61b8e5f` **non** e' antenato di *ogni* commit che tocca `CLAUDE.md` — `b0f7361`
*(`H-NON-TRACCIATI`)* lo tocca e **viene prima**. ### **La verifica l'ha trovato, e la frase
si restringe al perimetro vero invece di arrotondare.**
