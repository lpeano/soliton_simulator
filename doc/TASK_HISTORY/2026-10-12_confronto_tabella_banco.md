# IL CONFRONTO COMPLETO FRA LA TABELLA DELLE LEGGI E IL BANCO CONGELATO

> **Mandato di Luca, 2026-10-12, parte `2`:** *«E' il TERZO disallineamento della stessa
> famiglia. Non devono piu' venire fuori uno alla volta mentre si scrive il motore. Si fa
> un CONFRONTO COMPLETO, PRIMA di scrivere il flusso di saturazione e prima del criterio
> di passaggio del pezzo `6`.»*

> ### ✅ **E IL RITO E' RISPETTATO: questo file si committa PRIMA del confronto**, cosi'
> l'ordine e' **verificabile da git**.

---

## 1. RAGIONAMENTO PRELIMINARE — *che cosa credo, e che cosa ho GIA' visto*

### ⚠ **PRIMA L'ONESTA': parte l'ho gia' guardata.** Scrivendo il motore ho letto
`camminata.py`, `camminata2.py`, `camminata3.py`, `vuoto3.py`, `saturazione3.py`. ### **Non
posso fingere di non saperlo**, quindi divido: cio' che **so gia'** e cio' che **non ho
ancora guardato** — ed e' quest'ultimo che il confronto deve scoprire.

### 📌 **CHE COSA SO GIA', e lo scrivo come previsione VERIFICABILE**

| | la mia previsione | perche' |
|---|---|---|
| le **cinque variabili** | `psi_h`, `phi_h`, `Lambda`, `h_int` **COINCIDONO**; `psi` *(nodo)* **NON ha un corrispondente nel banco** | il banco tiene `st["psi"]` **sulle estremita'** *(`(2m,2)`)*, e un `psi` di nodo **non esiste la'**: e' la variabile delle tre leggi di **prova** dell'era `2` |
| i **sei pezzi nell'ordine** | **COINCIDONO tutti e sei** | `camminata3.passo3` fa `flusso(mezzo)` → `_lineare` → `flusso(mezzo)`, e `_lineare` fa `passo2` *(moneta → Grover → spostamento)* sullo spinore e `grover_scalare` → `spostamento_scalare` sul vuoto. ### **La tabella dichiara esattamente quella sequenza, con `0.5 + 0.5` sulla saturazione** |
| le **condizioni iniziali** | ### ⛔ **MANCANTI: la tabella non ha un posto dove dichiararle** | il banco ha `LAMBDA0 = 1.0`, `vuoto_fondo` *(modulo uniforme, **fasi dal seme `seme + 777`**)* e `stato_casuale` *(normalizzato, seme)*. ### **Il generato fa `np.zeros`**, e uno stato a zero **non e' una condizione iniziale: e' l'assenza di una** |

### ⛔ **CHE COSA NON HO ANCORA GUARDATO, e lo dico PRIMA**

1. ### **quali operatori del banco le MISURE REGISTRATE usano DAVVERO.** Ho letto i
   moduli `v2` e `v3`; **del `v4` *(`vuoto4`, `pesi4`, `frazione4`, `cslocale4`)* non so
   quali funzioni entrino nelle letture che hanno prodotto i referti.** ### **E' il
   verso `(a)` del mandato**, quello che trova le **RIGHE MANCANTI**.
2. **se `camminata.moneta_banda`** *(`exp(-i dtau sigma_z)`, *«e' la massa»*)* sia usata
   nelle misure registrate. ### **Se si', e' una RIGA MANCANTE** — non c'e' nessuna legge
   in tabella che la realizzi.
3. **a che cosa corrisponda `CAMM-FORMA-D`**, che in tabella porta `posto: A4` e
   `voce_decisione: DOMANDA-QUALE-SEGNO` e **NON sta nell'ordine**. ### Il banco ha
   `saturazione3.flusso_su_rho` e `flusso_v2` come **CONTROLLI CHE DEVONO ROMPERE `C`**:
   se `CAMM-FORMA-D` e' uno di quelli, **la tabella sta dichiarando un controllo come
   legge**, e questo e' **un CONFLITTO**.
4. **il fattore `r`**: il banco calcola `dtau = r * dt`, e il motore prende **`dtau` per
   nodo** direttamente. ### **E' coerente**, ma **`r` e' una grandezza che la tabella non
   nomina**: va detto **dove e' finita**.
5. **le simmetrie e le conservazioni dichiarate**: ogni legge in tabella porta
   `simmetrie: [U1-FASE-GLOBALE]`, e **la `C` non e' fra loro** -- ma `camminata3.coniuga3`
   **esiste** e il banco la misura. ### **Dove sta `C` nella tabella?**

---

## 2. PROGETTAZIONE DEL RAGIONAMENTO — *i passi, e cosa mi FERMEREBBE*

| | il passo | che cosa decide | ### **cosa mi FERMEREBBE** |
|---|---|---|---|
| `1` | **censire gli operatori del banco USATI nelle misure registrate**, dai `_letture*.py` e dai `_referto*.py` — **dal codice, via AST** | il perimetro del verso `(a)` | ### se un modulo del banco **non fosse raggiungibile** da nessuna lettura: allora **non e' <<usato nelle misure>>**, e va detto |
| `2` | **il confronto delle VARIABILI**, meccanico: `dtype`, forma, dove-vive, costruiti **girando le funzioni del banco** su una scena piccola | se i tipi dichiarati **sono quelli** | ### un `dtype` che non coincide ⟹ **ERRORE DI TRASCRIZIONE**, e si corregge la tabella |
| `3` | **il confronto delle LEGGI**: funzione, forma *(segni, fattori, convenzione di `sigma`, verso del trasporto, `ii`/`jj`)*, chi la usa, posizione e frazione, azione di `C` | il cuore | ### una **forma** diversa ⟹ **CONFLITTO**, e va a Luca |
| `4` | **i due versi**: `(a)` operatore del banco senza legge ⟹ **MANCANTE**; `(b)` legge senza banco ⟹ **NUOVA** *(col punto della carta)* o **ORFANA** | che non resti niente fuori | — |
| `5` | **il collaudo ESEGUIBILE**, coi suoi casi che **DEVONO fallire** | che il confronto **non sia ripetibile a mano** | ### un caso che **non fallisce** ⟹ il collaudo **non impedisce niente** |

### ⭐ **LE LETTURE FISSATE QUI, PRIMA DEI NUMERI**

* **ogni riga** ha **un solo** esito fra: `COINCIDE` · `ERRORE DI TRASCRIZIONE` ·
  `CONFLITTO` · `MANCANTE` · `NUOVA` · `ORFANA`.
* ### ⛔ **ERRORE DI TRASCRIZIONE** = banco e carta d'accordo, tabella no ⟹ **si corregge
  la tabella**, dichiarandolo **riga per riga**.
* ### ⛔ **CONFLITTO** = carta e banco non d'accordo, **oppure la scelta tocca la forma di
  una legge** ⟹ **NON si corregge**: va in `DA_DECIDERE_LUCA.md`, **una domanda per
  riga**, con le prove e **la raccomandazione separata dalla decisione**.
* ### ⛔ **ORFANA** ⟹ **si segnala e NON si toglie.**
* ### ⚠ **E le prove si citano PER NOME DI FUNZIONE**, non per riga: `[[P-RIF]]` me le ha
  gia' rifiutate scritte a riga, ed e' il par.`2` — **i numeri di riga sono di blob vecchi
  e sono shiftati.**

---

## 2-bis. LA RIGA CHE MI ERA ARRIVATA TRONCATA, E CAMBIA IL PRODOTTO

> ### ✅ **Luca l'ha ridetta per intero** *(e nel frattempo l'avevo segnalata in
> `doc/CODA_2026-10-12.md` invece di inventarla)*:
>
> *«Il presidio deve **impedire** che una variabile nuova entri in tabella senza la sua
> riga di confronto, oppure senza la dichiarazione **NUOVA** con il punto della carta
> che la decide.»*

### ⛔ **E CAMBIA LA NATURA DEL PRODOTTO: non un collaudo, UN IMPEDIMENTO AL
COMMIT.** Un collaudo dice *<<e' sbagliato>>* a chi lo fa girare; un presidio del
`pre-commit` ### **rifiuta il commit**. ### **Era la differenza che non potevo
indovinare**, ed e' il motivo per cui non l'ho inventata.

| | |
|---|---|
| **dove va** | `csv/_presidi_era2.py`, accanto a `P-E1`..`P-E9`: il `pre-commit` li chiama **tutti insieme** con `--pre-commit`, e un errore **rifiuta** |
| **che cosa rifiuta** | una variabile di `leggi.yaml` che **non ha la sua riga** in `doc/CONFRONTO_tabella_banco.md` *(con uno dei quattro esiti)* **e** non e' dichiarata **NUOVA DELL'ERA `2`** col **punto `F`/`A` della carta** |
| ### ⭐ **perche' il punto della carta e non una frase** | *<<nuova>>* senza il punto che la decide e' ### **una variabile che nessuno ha deciso**: il punto della carta e' **il campo** che lo dice, e `[[DECISIONE-VUOLE-UN-CAMPO]]` lo pretende |
| ### ⛔ **il suo caso che DEVE fallire** | si aggiunge **una variabile finta** alla tabella *(in memoria, non sul disco)* e il presidio **deve rifiutare**. ### **Un presidio che non si prova sul caso cattivo e' una tenda** |
| ### ⚠ **e il verso opposto** | con la riga **presente** il presidio **deve TACERE** -- altrimenti rifiuterebbe sempre, e **lo spegnerebbero il primo giorno** |

---

## 3. LA STELLA POLARE

> ### ⚠ **SI APPLICA, perche' il confronto PUO' cambiare la tabella delle leggi** *(gli
> `ERRORE DI TRASCRIZIONE` si correggono)*. ### **Le cinque risposte vanno scritte nel
> commit che cambia la tabella**, non in questo — qui la tabella **non si tocca**: questo
> commit porta **il task history e nient'altro**.

---

## 4. TODO DEL NEXT STEP

1. ### ⭐ **il censimento degli operatori del banco usati nelle misure**, via AST sui
   `_letture*.py` e `_referto*.py`.
2. **il collaudo eseguibile** `primo_ordine/_collauda_confronto.py`, dichiarato in
   `collauda.py`, coi casi che **devono fallire** *(per esempio **`phi` dichiarato reale
   contro il banco complesso** — il caso che il mandato nomina)*.
3. **`doc/CONFRONTO_tabella_banco.md`**, coi **conteggi per esito in testa**.
4. **le domande dei `CONFLITTO`** in `DA_DECIDERE_LUCA.md`, una per riga.
5. ### ⚠ **E la riga troncata del mandato** — *«Il presidio deve imp»* — **resta da
   ridire**: sta in `doc/CODA_2026-10-12.md`.
