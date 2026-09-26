# 🧭 **VALUTAZIONE DELLA PROPOSTA DI LUCA: UN REGISTRO STRUTTURATO** *(2026-09-26)*

> **PROPOSTA DI LUCA, DA VALUTARE, NON DA ESEGUIRE.** *«Il difetto è il FORMATO, non il parser: sono
> tabelle scritte per essere lette.»* **Nessuna migrazione è cominciata. Decide Luca.**

**PARERE IN UNA RIGA: la proposta è GIUSTA, e la ragione è più forte di quella scritta nel mandato.**

---

## 1. È meglio del parser attuale? **Sì, e il perché non è «il parser è fragile»**

Il parser di oggi deve **inferire dalla prosa tre cose che sono DECISIONI**:

```
① che cosa è UNA VOCE          -> l'ho inferito dalla contiguità delle righe:  6 righe su 43
② qual è il suo STATO          -> l'ho inferito dalle parole:  `VALE SEMPRE` = chiusa E aperta
③ a quale FAMIGLIA appartiene   -> l'ho inferito da parole chiave:  111 voci senza famiglia,
                                   e `CLI-1` finito in `A` perché la sua riga dice «SEMINA»
```

> ### **Tutti e tre i difetti di oggi sono fallimenti di INFERENZA, non errori di codice.** Un campo
> ### dichiarato non si può inferire male: **si può solo sbagliare a scriverlo, e allora si vede nel
> ### diff.**

**È la stessa mossa del par.9** *(«un criterio si scrive DA UNA MISURA, non dal proprio modello
mentale del codice»)*, applicata al registro: **lo stato si DICHIARA, non si indovina.**
E risponde ad `A9` meglio di qualunque nota: su un file con schema, **il presidio può IMPEDIRE**;
su prosa libera, **non è stato trovato nessun presidio attivo** — è scritto nel par.9 di `CLAUDE.md`
dal 2026-09-19, misurato: *«il 75 % delle voci dei registri non porta il blob del codice che le ha
prodotte»*, e **nessun controllo lo impedisce**.

### Il formato: **preferisco UN FILE PER DIFETTO a un `difetti.yaml` unico**

| | pro | contro |
|---|---|---|
| **`difetti.yaml` unico** *(la proposta)* | una fonte, un `safe_load`, viste banali; leggibile tutto insieme | **il diff è illeggibile** quando cambiano tre voci su 300; due modifiche concorrenti **collidono nello stesso file**; *«nessuna voce si cancella»* si verifica **parsando**, non da git |
| **un file per voce** *(`doc/difetti/D31.yaml`)* — **la mia proposta** | **git dà una storia PER DIFETTO**, che è esattamente ciò che questo repo cita sempre *(la prova è un commit)*; **una cancellazione è `git diff --diff-filter=D`**, cioè un fatto di git e non di un parser; niente collisioni | ~300 file piccoli; le viste devono fare un `glob` *(tre righe)* |
| **JSON** | `json` è nella stdlib, parsing severo per costruzione | **niente commenti**, testo multilinea scomodo, e per un file scritto a mano è il peggiore dei tre sul diff |
| **Markdown «macchina-primo»** *(colonne fisse, vocabolario chiuso, niente blocchi di codice dentro)* | zero migrazione di formato | **non toglie l'inferenza** e non ha schema: la regola dipende dal ricordarsene, ed è già stata rotta. **`A9`: lo scarto.** |

**`PyYAML 6.0.3` c'è già** *(verificato: `import yaml` funziona)*, quindi `yaml.safe_load` — il
loader stretto che Luca chiede — **non aggiunge una dipendenza da installare**.

**Forma che consiglio:** `doc/difetti/<ID>.yaml`, campi **come li ha elencati Luca**, più **tre**
che l'esperienza di oggi rende necessari:

```yaml
id: D31                 # univoco, MAI riusato
titolo: ...
famiglia: F             # A-G
stato: aperto           # aperto | cura-derivata | chiuso | non-difetto | teoria | dopo-run-base
                        #   + da-decidere  <- IL CAMPO CHE SERVE ALLA MIGRAZIONE (vedi §2/R2)
fonte: soliton_simulator.py:3607        # file:riga, oppure un commit
prova: Z113             # e il BLOB con cui è stata fatta
cura: ...
dipende_da: [D33]
dimensione: M
alias: [D-31]           # ① le citazioni storiche scritte diversamente
stato_da: "STATO_RUN.md:618 -- `APERTO`"   # ② LA FRASE da cui ho letto lo stato, verbatim
nota: ...
```

**① `alias` e ② `stato_da` non sono ornamenti: sono i due controlli della migrazione**, e il §2 dice
perché. Il terzo è **`da-decidere`** come stato legittimo: **una migrazione che non può dire «non lo
so» produce trecento indovinelli**.

---

## 2. I rischi della migrazione, e come li controllerei

| | rischio | come lo controllo |
|---|---|---|
| **R1** | **una voce si PERDE** *(sta nella prosa e non arriva nel registro)* | ① lo **sweep degli ID** che propone Luca; ② **il parser di oggi resta e fa da SECONDO LETTORE INDIPENDENTE**: si fa il `diff` fra le sue 624 voci e il registro, e **ogni voce che lui vede e il registro no è una perdita**; ③ i **conteggi per fonte**, vecchio contro nuovo, stampati; ④ le **15 voci nominate da Luca** restano il collaudo che **impedisce** |
| **R2** | **lo STATO viene scelto male** su una voce ambigua *(è già accaduto: `VALE SEMPRE`)* | il campo **`stato_da`** con **la frase verbatim** da cui l'ho letto: uno stato sbagliato diventa **verificabile riga per riga** invece che invisibile. E ogni voce che non so decidere va a **`stato: da-decidere`** — **mai un'ipotesi travestita da dato**. Luca approva UNA volta l'elenco dei `da-decidere` |
| **R3** | **DUE VERITÀ**: registro e tabelle vecchie che divergono | l'intestazione *«fa fede `doc/difetti/`»* **è necessaria e non basta** (`A9`). Le tabelle vecchie vanno **RIGENERATE** dal registro dentro marcatori *(`<!-- GENERATO:difetti:INIZIO -->`, come i `<!-- INDIRIZZO:FINE -->` che `STATO_RUN` ha già)*, e **il hook rifiuta un commit che modifica a mano ciò che sta dentro i marcatori**: così la divergenza è **impossibile per costruzione**, non vietata per iscritto |
| **R4** | **COLLISIONE DI ID fra registri diversi** | **misurato oggi, e non è teorico:** `A3` è **due voci diverse** — in `RAMIFICAZIONI` è *«FDT del solo scuotimento», chiusa per dimostrazione*; in `STATO_RUN` è *«il disegno esce dalla dinamica», aperta*. Idem `B5`, `M1`, `M2`, `C21`. **Gli ID vanno NAMESPACED** (`RAM:A3` / `CODA:A3`) e lo sweep, quando una citazione risolve a **due** voci, **deve dirlo** invece di scegliere |
| **R5** | **lo sweep è ESSO STESSO un parser su prosa** | va detto: **converte ignoti in contati, non li elimina.** Misurato adesso su **217 file `.md`**: `D` **45**, `Z` **137**, `S` **23**, `C` **28**, `B` **11**, `A` **13**, `E` **4**, `M` **5**, **nomi MAIUSCOLI col trattino 170** → **436 ID distinti**. E i nomi col trattino sono **rumorosi**: nei 40 più citati, **circa metà non sono voci** (`BYTE-INERTE`, `NON-ABELIANO`, `ON-OFF`, `NO-OP`, `PURE-READ`, `PRE-FORK`, `COLLO-DI`, `NATO-NATO`…). **L'elenco `ESCLUSI` sarà di ~80-90 voci**, e ciascuna va decisa a mano una volta |
| **R6** | **la migrazione non produce fisica** *(e il bersaglio sono le tre prove)* | è il rischio vero. **Non lo mitigo con una migrazione parziale**: migrare solo i difetti `Dxx` ricrea **R3**. Lo mitigo **ordinando**: prima le voci **con un ID** *(sono quelle che i presidi possono controllare)*, poi le voci **con un nome**, e **le viste per ultime** — con ogni passo **committato e usabile da solo** |

---

## 3. Quanto costa — **una STIMA, e dico quali numeri sono misurati**

**MISURATI oggi:** `624` righe estratte dalle cinque fonti · `405` senza marchio di chiusura ·
`38` difetti `Dxx` in tabella · `436` ID distinti citati in `217` file `.md` · `170` nomi col
trattino di cui **~metà rumore**.

**STIMATO** *(non misurato, e la parte a mano è quella che non so comprimere)*:

```
voci vere nel registro            ~250-320    (i 624 contengono criteri, previsioni, doppioni)
di cui con un ID                  ~150-180
elenco ESCLUSI dello sweep         ~80-90     decisioni una tantum, quasi tutte «non è un ID»

schema + importatore + sweep + i due collaudi      ~2-3 h   (macchina: riuso ciò che c'è)
le viste (LISTA_CHIUSA + i blocchi in STATO_RUN)     ~1 h
il presidio nel hook + collaudo nei due rami         ~1 h
LA REVISIONE A MANO di stato/famiglia/dipendenze    ~3-5 h   <- IL COSTO VERO, non comprimibile
                                                    -------
                                                     ~7-10 h di mio lavoro, in 6-8 passi
                                                     + UNA approvazione di Luca sui `da-decidere`
```

> ### **La parte che non si può automatizzare onestamente è la revisione a mano**, e va detto prima:
> ### se la comprimessi, produrrei trecento campi «plausibili» — cioè **il difetto di oggi
> ### moltiplicato per trecento.**

---

## 4. Che cosa resta a metà del lavoro attuale? **Niente — e si RIUSA, non si butta**

**Il generatore NON è a metà:** è finito, collaudato **`2/2`** *(scrive quando deve, **si ferma e non
tocca il documento** quando una voce manca: `668f7538 → 668f7538`)*, e committato in `f4bc082`.

| pezzo | destino |
|---|---|
| **la lettura delle cinque fonti** *(sezioni, righe non contigue, celle)* | **DIVENTA L'IMPORTATORE della migrazione**: è già il primo passo, e invece del Markdown emette le voci del registro |
| **il collaudo `_collaudo_lista_chiusa.py`** | **resta identico**: collauda una **vista**, e le viste restano |
| **le 15 voci di Luca come criterio bloccante** | **resta**, ed è il controllo `R1`-④ della migrazione |
| **il parser intero, dopo la migrazione** | **resta come SECONDO LETTORE INDIPENDENTE** *(`R1`-②)*: due strade che concordano valgono più di una. Poi, a migrazione chiusa, **scade a strumento di controllo** |
| **`REG_FAM`, le famiglie per parola chiave** | **MUORE, e deve morire**: è il pezzo più debole *(`111` senza famiglia, `CLI-1` → `A`)*. Sopravvive solo per **PROPORRE** una famiglia da rivedere a mano durante la migrazione |
| **lo sweep degli ID** | **NON esiste ancora**: è l'unico pezzo nuovo di macchina, e il §2/`R5` dice quanto pesa |

---

## ⛔ CRITERIO DI CHIUSURA DI QUESTA VOCE *(par.5-quater: una voce senza criterio è un desiderio)*

**La decide Luca**, e la decisione è **una** di queste tre:

```
(a) SÌ, un file per voce (doc/difetti/<ID>.yaml)  -> si migra, nell'ordine del §2/R6
(b) SÌ, ma un difetti.yaml unico                  -> si migra, e R3 costa di più (diff)
(c) NO / non ora                                  -> il parser resta, e resta anche il suo limite,
                                                     che è dichiarato in testa a LISTA_CHIUSA.md
```

**Finché Luca non decide, non si tocca niente:** nessun file `.yaml`, nessuna intestazione *«fa
fede»*, nessun hook nuovo.
