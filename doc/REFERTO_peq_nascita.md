# REFERTO — **la verifica preliminare di ① FALLISCE, e il reperto va riletto**

**Blob al momento della verifica:** `241eefb` (byte grezzi `7775ac45`). **Nessun cablaggio di ① o ②.**
Il mandato ordina la verifica **prima** del cablaggio (§6.1) e dice: *«Se non è raggiungibile né per
snapshot, **FERMATI e riporta: non inventare una via**»*. È quello che segue.

> **NOTA SUL BLOB.** Il mandato cita **`87450f78`** / HEAD `f405327`. Quel blob è reale ed **era**
> HEAD a `f405327`, ma da allora sono stati committati ②③⑤ (`3ca7731`), i registri (`ed26d14`) e lo
> STATO (`b16c792`). **Le righe citate sono shiftate**: `:1862 → :1867`, `:3548 → :3598`,
> `:3626 → :3680`. Cercate per **nome**, come impone §0 di CLAUDE.md, non per numero.

---

## 1. LA VERIFICA PRELIMINARE — `psi` è raggiungibile, **ma è IDENTICAMENTE ZERO**

`_allaccia` non riceve `I` né `psi`, ma `self.psi` **esiste** ed ha la lunghezza giusta
(`len(psi) = 120 = n`). **Sembrerebbe quindi cablabile senza snapshot. Non lo è:**

```
DOPO la costruzione della scena:  len(psi) = 120   n = 120
  psi tutti zero?  True      max|psi| = 0

IL VALORE CHE ① SCRIVEREBBE  ->  0.5*(I[a]+I[b]) :
  min 0    mediana 0    max 0
  quanti <= 1e-30, cioe' DEGENERI LO STESSO:  4555 su 4555   (100.00 %)
```

**`psi` non è "non raggiungibile": non è ancora stato calcolato.** Nasce `np.zeros(0, complex)`
(`:1027`) e viene popolato **solo dentro `step()`** (`calcola_psi`, `:2401-2408`). Al momento in cui
gli archi nascono, **la densità non esiste come grandezza fisica.**

> **Conseguenza diretta: ① scriverebbe `0` al posto di `NaN`, e `0 <= 1e-30`.
> Il contatore `_taup_peq_degenere` resterebbe IDENTICO, e W1 fallirebbe per costruzione.**
> **Non è un dettaglio implementativo: ① sarebbe INERTE rispetto al problema che dichiara di
> risolvere.**

**E uno snapshot non aiuta**, perché non c'è nulla da fotografare: non esiste un istante precedente
in cui `psi` valga qualcosa. L'unica via sarebbe **ricalcolarlo** con `calcola_psi()` — che il
mandato **vieta esplicitamente** (§5), e a ragione: quella funzione **scrive** `self.psi`
(precedente `lambda_vuoto`). **Non invento una via: mi fermo e riporto, come ordinato.**

---

## 2. IL REPERTO VA RILETTO — **non è una finestra sempre popolata: sono DUE PASSI**

Il mandato legge il contatore così: *«in un sistema che genera archi in continuazione quella
finestra è sempre popolata»*. **Ho cablato un secondo contatore per deciderlo invece di
argomentarlo** — quanti **passi distinti** hanno almeno un `peq` degenere:

```
RUN REALE, 60 passi:
  _taup_peq_degenere  (archi-passo cumulativi) :  207520
  _taup_peq_deg_passi (PASSI DISTINTI)         :       2      <----
  _taup_causale_scatti / su_degenere           :  249017 / 207520
```

**Due passi su sessanta.** I 207520 archi-passo non sono una finestra permanente: sono
**~103 760 archi × 2 passi**, cioè **il transitorio di accensione moltiplicato per il numero di
archi**. Un contatore cumulativo, da solo, **non distingue «difetto sempre presente» da «transitorio
moltiplicato»** — e senza il secondo contatore si sceglie la diagnosi che si ha in mente.

**La sequenza esatta, misurata passo per passo:**

| momento | `peq` |
|---|---|
| dopo la costruzione della scena | **NaN su 14009 archi (100 %)** |
| dopo il **passo 1** | `psi` è **ancora tutto zero** → `peq = rho = 0` **ESATTO** su 14009 |
| dopo il **passo 2** | `peq` min `1.13e-17` — **zero degeneri** |
| da lì in poi | **zero degeneri, sempre** |

**Ed è coerente con ciò che era già stato misurato:** `peq` degenere **0.0000 %** nei dati maturi e
**2.49 %** nel run giovane. Il 2.49 % non era «una finestra»: era **2/60 passi** diluiti nel
cumulativo.

---

## 3. IL RIBALTAMENTO — **il `NaN` non è il difetto: è l'unica cosa onesta in quel punto**

Il mandato lo marca come *«IL PROBLEMA»* e scrive: *«`NaN` dice "non lo so" — ma si sa: un arco
appena nato sta in un posto che esiste già, coi suoi due nodi e la loro densità»*.

**Alla costruzione della scena quel posto NON esiste ancora.** I nodi ci sono come **posizioni**, ma
la loro densità è **zero per costruzione**, perché `psi` non è stato calcolato. Il `NaN` non sta
nascondendo un valore noto: sta dicendo, correttamente, che **la grandezza non è ancora definita** —
e la delega a `:3137` è precisamente il meccanismo che la definisce appena esiste.

**Il difetto, se c'è, è a valle e di natura diversa:** al passo 1 **l'intero campo è identicamente
zero**, quindi ogni grandezza derivata lo è. Il vincolo causale che scatta lì **non sta mascherando
un difetto numerico: sta attraversando un sistema che non è ancora partito.**

**Questo non assolve tutto.** Restano veri due punti del mandato, e sono indipendenti da quanto
sopra:

- **② `pmed = median(self.peq)` nello Schwinger (`:3680`) viola A2** — è una statistica dell'intero
  sistema su un percorso fisico (Legge I, `:265`). **Questo è un difetto vero, e non ha nulla a che
  fare col transitorio**: lo Schwinger gira a sistema avviato, dove `peq` è sano e **i due nodi
  dell'arco hanno una densità vera**. **② È CABLABILE.**
- **③ `:3598` resta il riferimento di stile**: eredita dall'arco padre, locale, immediato.

---

## 4. COSA NON HO FATTO, E PERCHÉ

**Non ho cablato ① — verifica preliminare fallita**, come il mandato ordina.

**Non ho cablato ② da sola**, e questa è una scelta che dichiaro invece di prenderla in silenzio:
il mandato (§6.3) le cabla **insieme**, con **W1 come sigillo decisivo**, e W1 **non può passare**
finché il transitorio esiste. Cablare ② da sola significherebbe **cambiare il comportamento senza
il sigillo che il mandato ha scelto per autorizzarlo**, e presentare un W1 fallito come se fosse il
verdetto su ②, che invece con W1 non c'entra nulla. **② è pronta e la ragione che la sostiene è
intatta: serve una riga del mandato che la sganci da ①.**

**L'unica modifica al codice in questo commit è un CONTATORE** (`_taup_peq_deg_passi`,
`_taup_peq_deg_ultimo`): non tocca nessuna legge, e serviva a decidere il reperto invece di
interpretarlo. **A1/A2/A5 non sono coinvolti: non è una legge.**

---

## 5. COSA DECIDERE — e non lo decido io

1. **Il transitorio di accensione va trattato?** Al passo 1 **tutto** il campo è zero, non solo
   `peq`. Se è un difetto, **non è un difetto di `peq`**: è che il primo passo integra su un campo
   che non esiste. Una via sarebbe **calcolare `psi` una volta alla costruzione della scena**, prima
   del primo `step` — **ma è un cambio del percorso di inizializzazione**, non una bonifica, e va
   deciso.
2. **② si cabla da sola?** È sana, indipendente, e il suo sigillo naturale **non è W1** (è: nessuna
   occorrenza di `median(self.peq)` sul percorso di nascita, più il limite `pmed → nodi dell'arco`).
3. **Oppure ① si ridefinisce**: non `0.5*(I[a]+I[b])` — che è zero — ma una grandezza che **esiste**
   alla nascita. **L'unica che esiste è geometrica** (`d`, `pos`), e usarla per inizializzare una
   **densità** richiederebbe un fattore di conversione, cioè **un numero scelto: A1.**
