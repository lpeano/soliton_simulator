# TASK HISTORY — **l'estensività è un difetto? `ω` contro il grado, prima e dopo**

**Data:** 2026-09-18 · **Branch** `fork-su2` · **HEAD alla scrittura** `288d995` · **blob** `aa84755b`
**Task:** mettere alla prova la speculazione di Luca su `Z30` — *l'estensività è corretta, perché
l'inerzia la compensa già, e normalizzare anche il feedback la compenserebbe due volte.*
**Luca la dichiara speculazione e chiede di misurare: `ω` contro grado, prima e dopo.**

---

## 1. RAGIONAMENTO PRELIMINARE — *cosa credo prima di guardare*

### La catena del ragionamento di Luca, e dove mi convince

1. **«un nodo non è un punto dello spazio, è un evento di relazione; il grado è quante relazioni
   ha»** — coerente col modello.
2. **«gli archi nascono per prossimità, quindi grado alto = regione densa; il grado è un proxy
   della densità locale»** — **verificabile, e non l'ho mai verificato.** È una premessa, non un
   fatto stabilito: va misurata.
3. **«il grafo è bimodale: non è una distribuzione continua, sono due popolazioni — i neonati
   (grado 2, due archi verso i genitori) e la materia stabilizzata (grado 119)»** — **questo è
   già misurato da me** (`Z27`: 19.85 % a grado 2, 65.57 % a grado ≥ 100) **ed è solido**. E la
   riformulazione che ne trae — *«la domanda è: un neonato deve subire il feedback quanto un nodo
   maturo?»* — **è più precisa della mia**, che parlava di «crescita col grado» come se il grado
   fosse un continuo.
4. **«normalizzare via direbbe che un nodo isolato e uno nel cuore di un solitone rispondono allo
   stesso modo, e sarebbe strano»** — argomento di plausibilità, e lo trovo buono.

### ⚠ E QUI IL PUNTO CHE DEVO SOLLEVARE PRIMA DI MISURARE (P1)

L'argomento che Luca stesso chiama **«più forte»** è:

> *«un nodo nel denso ha `rho/peq` alto, quindi inerzia alta, quindi ruota di meno a parità di
> coppia. L'estensività della coppia è già compensata dall'inerzia. Normalizzare anche il feedback
> la compenserebbe DUE volte.»*

**Ma io ho già misurato, e committato, che il feedback NON passa per l'inerzia**
(`doc/REFERTO_denominatore.md` §1, commit `a15716c`):

```
:3189  if SPINORE_VIVO and SPINORE and SPIN_FEEDBACK:  ->  coppia += _fb
       coppia  ->  delta_phivel = dt_n_s * (coppia - G_PH*phivel) / M_PH      M_PH = 1.0  COSTANTE
l'unica  / inerzia  del file divide `correzione` (3-vettore) in _passo_spinoriale  ->  omega_s
```

**Sono DUE CATENE SEPARATE: il feedback vive nel settore della FASE (`phivel`, massa UNIFORME), non
in quello dello SPIN (`omega_s`, inerzia per nodo).** Vale **anche** per `twist_nodo` (`Z27`), che
finisce nello stesso `coppia`.

**Quindi, se la catena è quella che ho misurato, la «doppia compensazione» NON PUÒ AVVENIRE sul
canale in questione: a valle del feedback non c'è nessuna inerzia da compensare, c'è una costante.**

**Non lo do per scontato, e non lo uso per liquidare l'argomento:**
- **la compensazione potrebbe avvenire INDIRETTAMENTE** — `phivel` → `phi` → `psi` → `rho` →
  `inerzia`: il ciclo esiste, e se è abbastanza rapido l'effetto netto potrebbe assomigliare a una
  compensazione. **Questo non l'ho mai misurato.**
- **e l'argomento di Luca potrebbe essere giusto su un ALTRO punto**: `correzione = B × nb` (il
  punto 1 di `Z24`) **passa davvero per l'inerzia**. Lì la doppia compensazione sarebbe reale — ma
  lì la cura del denominatore **non si applica** (due rotture, `Z27`).

### Cosa NON so, e lo scrivo adesso

- **non so se `grado` correli davvero con la densità** — è la premessa 2, mai verificata;
- **non so se `inerzia` cresca col grado** — è ciò che renderebbe vera la compensazione, e nessuno
  l'ha misurato;
- **non so quale `ω` intenda Luca.** `omega_s` (spin) e `phivel` (fase) sono grandezze diverse in
  catene diverse, e **la risposta cambia a seconda di quale si guarda**. Le misuro **entrambe** e
  dico quale appartiene a quale catena, invece di sceglierne una e chiamarla «ω».
- **e non so se la mia stessa lettura della catena regga** — l'ho misurata una volta sola.
  **La rifaccio come primo passo.**

---

## 2. PROGETTAZIONE DEL RAGIONAMENTO — *i passi, cosa decide ciascuno, cosa mi ferma*

**Passo 0 — RI-VERIFICARE LA CATENA dal sorgente.** *Decide:* se l'argomento della doppia
compensazione si applica al canale in questione. **Se la mia lettura precedente fosse sbagliata,
questo è il primo risultato e va riportato prima di tutto il resto.**

**Passo 1 — LA PREMESSA DI LUCA: `grado` è un proxy della densità?** Correlazione fra grado
topologico e densità locale (`rho_sorgente`, `peq_nodo`) **sulla stessa popolazione, allo stesso
istante** (A3c). *Decide:* se «grado alto = regione densa» è un fatto o un'analogia.
**Nullo da dichiarare prima:** su un grafo costruito per prossimità una correlazione **positiva e
forte** è attesa; il valore informativo è **quanto**, e se regge **su entrambe le mode**.

**Passo 2 — LA COMPENSAZIONE ESISTE? `inerzia` contro grado.** *Decide:* se «l'inerzia compensa
già» ha una base misurata. **Se `inerzia` NON cresce col grado, l'argomento cade a prescindere
dalla catena.**

**Passo 3 — LA MISURA CHE LUCA CHIEDE: `ω` contro grado, PRIMA e DOPO la cura.** Due osservabili,
dichiarate separatamente:
- **`|phivel|` vs grado** — **la catena in cui il feedback ENTRA** (massa uniforme);
- **`|omega_s|` vs grado** — **la catena dell'inerzia**, dove il feedback entra solo indirettamente.

E si riporta **sulle DUE MODE** (`g = 2` contro `g ≥ 100`), **non con un fit**: la distribuzione è
bimodale, e un fit su due popolazioni separate è l'errore che ho già fatto una volta (`Z27`).

**LE LETTURE, FISSATE ADESSO:**
- **`|ω|` PIATTO contro il grado dopo la cura** → l'estensività della coppia **è** compensata a
  valle: **la speculazione di Luca regge**, e `nudo` è giustificato **da una misura**, non solo da
  A1.
- **`|ω|` CRESCE col grado dopo, ed era piatto prima** → la cura ha introdotto un **bias di grado
  nell'osservabile**, non solo nel termine: è un costo reale e va messo accanto al guadagno.
- **`|ω|` cresceva col grado ANCHE PRIMA** → il bias **precede la cura**, e la scelta del
  denominatore non è ciò che lo decide. **Sarebbe il risultato più interessante**, e cambierebbe la
  domanda.

**COSA MI FA FERMARE E RIPORTARE invece di procedere:**
- se il passo 0 contraddice ciò che ho già committato → **si riporta quello, prima di tutto**;
- se `inerzia` e grado sono **scorrelati** → l'argomento della doppia compensazione cade, e **va
  detto a Luca prima di misurare `ω`**, perché cambierebbe la sua domanda;
- se le due mode danno **verdetti opposti** → non si media: **si riportano separate.**

**E una cosa che NON farò:** non deciderò `Z30`. Questa misura **informa** la decisione; la
decisione resta di Luca, e va presa **sui due punti insieme** (`Z25` e `Z27`) come già stabilito.

---

## 3. TODO DEL NEXT STEP

- [x] **passo 0** — ri-verificare la catena del feedback dal sorgente *(se smentisce il committato,
      si riporta per primo)*
- [x] **passo 1** — `grado` vs densità locale: la premessa di Luca è un fatto?
- [x] **passo 2** — `inerzia` vs grado: la compensazione ha una base misurata?
- [x] **passo 3** — `|phivel|` e `|omega_s|` vs grado, **prima e dopo**, **sulle due mode**
- [x] referto + voce `Z30` aggiornata col risultato + relazione (par.5-ter) + **riportare a Luca
      senza decidere**
- [ ] **⚠ NON toccare:** `Z9`, il punto 1 di `Z24` (`refl` = legge nuova), `Z31` (meccanismo
      proposto, non cablato), e **non cambiare `Z25` in questo giro**

---

## 4. ESITO — *cosa il ragionamento preliminare aveva preso, e cosa no*

**PRESO:** il rilievo sulla catena era **giusto e decisivo** — la doppia compensazione non può
avvenire sul canale del feedback, e il passo 0 l'ha confermato. E la scelta di misurare **due**
osservabili invece di una «ω» ha prodotto **due verdetti opposti**: senza quella separazione avrei
riportato una risposta sola, e sbagliata per metà.

**NON PRESO — e questa è la parte che il ragionamento preliminare non aveva:** non avevo previsto
che **la scelta del denominatore non si vedesse a valle**. Avevo fissato tre letture su *«|ω| cresce
o no col grado»*, e la risposta è **«cresce, ma non per via del denominatore»** — la terza lettura,
che avevo chiamato «la più interessante» e che infatti lo è: **cambia la domanda invece di
rispondere a quella posta.**

**E un errore mio che il risultato corregge:** avevo portato a Luca `36.2` contro `16.9` come **la
posta in gioco**. Sono numeri sul **termine**; **a valle valgono 0.8 %.** La scelta andava presentata
dicendo **su cosa** quei numeri si misurano.

## 5. TODO DEL PROSSIMO PASSO *(aggiornato)*

- [ ] **`Z30` è decidibile, e ora con una misura**: il criterio dell'estensività **non discrimina**
      → restano `A1` e §3, che indicano `nudo`. **Decisione di Luca, sui due punti insieme.**
- [ ] **DOMANDA NUOVA, non misurata:** il bias di grado di `phivel` (`×4.9`) è esso stesso un
      difetto? **Da dove viene?** *(candidati: `_coppia_interferenza`, la repulsione, `twist_nodo`)*
- [ ] `Z31`: meccanismo **proposto, non cablato**
- [ ] `Z9`, il punto 1 di `Z24` (`refl` = legge nuova): **non toccati**
