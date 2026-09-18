# TASK HISTORY — **la mediana in `ritmo()`: normalizzazione o GAUGE del tempo?**

**Data:** 2026-09-18 · **Branch** `fork-su2` · **HEAD alla scrittura** `4b976e2`
**Blob:** `72acd6aa` (git) / `aa84755b` (byte) · **Nessun cablaggio in questo giro.**
**Task:** le quattro misure del §2 del mandato, per decidere **se `Z9` sia curabile da `ritmo()`**.

---

## 1. RAGIONAMENTO PRELIMINARE — *cosa credo prima di guardare*

### Il punto del mandato è giusto, ed è più forte di come l'avevo scritto io

Avevo riportato che `median(dt_n) = DT` **blocca il meccanismo al primo ordine**. Il mandato ne trae
la conseguenza che non avevo tratto: **se `r` è il tempo proprio, e la sua mediana è pinnata, allora
il nodo tipico ha `r` fisso qualunque cosa faccia il sistema.** Non «poco sensibile»: **insensibile
per identità**. E da `r` discendono `dt_n`, `dt_e`, `eta`, la maturazione, il rilassamento plastico,
`_rep`, il termostato.

**È già in registro come `C12`**, dal 17 settembre, in *«solo analisi, non cablare»*. **Non è una
scoperta: è una voce vecchia che adesso ha una conseguenza misurata.**

### ⚠ E la domanda 2.2 è quella che decide — **e non so la risposta**

> **normalizzazione** *(rendo `x` adimensionale)* → si cura, come `Lam` ha sostituito `GAMMA`;
> **definizione di unità** *(«`r = 1` per il nodo tipico **è** la convenzione con cui il tempo
> proprio è misurato»)* → **è il GAUGE, e toglierlo cambia l'unità di misura di tutto il sistema.**

**Non ho un'opinione formata, e lo dichiaro invece di sceglierne una e cercarne conferma.**
Ciò che mi fa **propendere per il gauge**, e va messo alla prova:
- **il nome stesso**: `r_unit = r(x=1)`, e il commento dice *«valore al gauge x=1»*. **Il codice
  usa la parola «gauge».** Non è una prova — un commento può essere stale — **ma è un indizio da
  verificare, non da ignorare**;
- **`TAU_LOC = 1.0`** e il ritorno è `1 + TAU_LOC*(r/r_unit − 1)`: la forma è **«1 più uno
  scostamento»**, cioè **una deviazione da un riferimento**, non un rapporto puro. Una
  normalizzazione dimensionale non avrebbe bisogno del `1 +`.

Ciò che mi fa **propendere per la normalizzazione**:
- `f` ha dimensione `1/T` (è `Δangolo/DT`), quindi **`x = f/med` è adimensionale**: la divisione
  **serve** a rendere `x` un numero puro prima di `x/√(1+x²)`. **Questo è un argomento
  dimensionale, non un'analogia.**

**Le due cose possono essere entrambe vere:** la mediana può essere **contemporaneamente** ciò che
rende `x` adimensionale **e** ciò che fissa il gauge. **Se è così, la domanda 2.2 è mal posta come
alternativa secca**, e la risposta corretta è: *«è una normalizzazione che si è portata dietro un
gauge»*. **Lo dico prima, così non sembra una scappatoia trovata dopo.**

### Cosa NON so

- **non so se esista una scala di stato locale alternativa** con la dimensione di `f`. `Lam` è
  un'energia, `cs` una velocità, `d/cs` un tempo. **`1/(d/cs) = cs/d` avrebbe la dimensione giusta**
  — ma è un candidato, non una derivazione, e va guardato dal codice;
- **non so quali leggi diano per scontato `median(r) = 1`** — è la 2.3, e va enumerata dal sorgente;
- **non so se `median(|f|)` evolva** — è la 2.4, e cambierebbe la gravità del difetto.

---

## 2. PROGETTAZIONE DEL RAGIONAMENTO — *i passi, cosa decide ciascuno, cosa mi ferma*

**2.1 — Che cos'è `f`.** Dal sorgente: da dove viene `signed`, che dimensione ha, se è per nodo,
che distribuzione. *Decide:* se il candidato sostitutivo debba avere dimensione `1/T`.

**2.2 — Normalizzazione o gauge?** Tre prove **indipendenti**, perché una sola sarebbe un'analogia:
- **(a) dimensionale** — `f` ha unità? Se sì, la divisione è **necessaria** per l'adimensionalità;
- **(b) strutturale** — la forma `1 + TAU_LOC*(r/r_unit − 1)` è una **deviazione da un
  riferimento**? E `TAU_LOC` cosa spegne quando vale 0?
- **(c) di consumo** — chi usa `r`, lo usa come **rapporto** o come **valore assoluto**? *Se tutti i
  consumatori lo usano come rapporto fra nodi, il gauge è irrilevante e il difetto è reale. Se
  qualcuno usa il valore assoluto, quel qualcuno dipende dal gauge.*

*Decide:* se `Z9` sia curabile da qui. **È la domanda del giro.**

**2.3 — Chi dipende da `median(r) = r(1)`.** Enumerare i consumatori di `ritmo()` e di `dt_n` dal
sorgente, e per ciascuno dire **se darebbe per scontato che il nodo tipico abbia `r` fisso**.
*Decide:* il costo della cura, se si facesse.

**2.4 — `median(|f|)` evolve nel tempo?** Misurato su un run breve. *Decide:* la **gravità**: se la
scala su cui si normalizza cresce coi passi, il difetto è **parziale**.

**LE LETTURE, FISSATE ADESSO** *(le tre del mandato, più una quarta che aggiungo)*:
- **normalizzazione + esiste una scala di stato** → **si cura**, famiglia `cs_floor`;
- **è il GAUGE (A4)** → **`Z9` non si cura da qui.** Si dice, si chiude la strada, si registra che
  `Z9` richiede un'altra via. **È un esito valido.**
- **`median(|f|)` evolve** → **difetto parziale**: si riporta di quanto e si rivaluta;
- **⊕ è ENTRAMBE** *(normalizzazione dimensionale che porta con sé un gauge)* → **allora la cura non
  è «togliere la mediana» ma «sostituirla con un'altra scala dimensionalmente valida»**, e il gauge
  cambia con essa. **Va detto quale gauge si sta scegliendo**, invece di far finta che non ce ne sia
  uno.

**COSA MI FA FERMARE:**
- se `f` risultasse **già adimensionale** → la divisione non serve all'adimensionalità, e la 2.2 si
  risolve subito verso «gauge»;
- se qualche consumatore usasse `r` in **valore assoluto** in una soglia → **toglierlo romperebbe
  quella soglia**, e va riportato **prima** di qualunque proposta;
- se non trovassi **nessun** candidato dimensionalmente valido → **si dice**, e la cura non si
  propone.

**E una cosa che NON farò:** **non cablo niente.** Il mandato lo vieta senza via libera esplicita, e
due cablaggi sono già stati fermati da una verifica preliminare — **entrambe le volte a ragione**.

---

## 3. TODO DEL NEXT STEP

- [x] **2.1** — cos'è `f`: origine, dimensione, per-nodo, distribuzione
- [x] **2.2** — normalizzazione o gauge? **tre prove indipendenti** (dimensionale, strutturale, di
      consumo)
- [x] **2.3** — chi dipende da `median(r) = r(1)`: enumerare i consumatori dal sorgente
- [x] **2.4** — `median(|f|)` evolve nel tempo?
- [x] **STOP e riporta** col verdetto contro le **quattro** letture
- [ ] **⚠ NON toccare:** `ramp`, `TAU_A`, il `+1e-6` di `ritmo()`. **Nessun cablaggio.**

---

## 4. ESITO — *cosa il ragionamento preliminare aveva preso, e cosa no*

**PRESO, ed è stato il contributo principale:** **la quarta lettura.** Avevo scritto, prima di
misurare, che *«le due cose possono essere entrambe vere, e allora la 2.2 è mal posta come
alternativa secca»*. **È esattamente così**, e averlo dichiarato prima ha evitato che sembrasse una
scappatoia trovata dopo.

**PRESO anche:** l'argomento dimensionale (`f` ha unità `1/T` → la divisione **serve**), e il ramo
`TEMPO_SEGNO` senza mediana, trovato leggendo la funzione invece di fermarsi alla riga citata.

**NON PRESO — ed è un errore di configurazione, il secondo di questa classe:** la sonda ha misurato
il **ramo scalare 2π**, `126/126`, perché non avevo acceso `CAMPO_SPINORIALE`. **Le campagne usano
il 4π.** Stessa classe di `--cs-dinamico` spento. **E cambiava i numeri**: gli zeri passano da
`11.1 %` a `3.2 %`, e la scala di `f` da `3.04` a `0.0280` — **un fattore 100**.
**Nel task history avevo elencato cosa non sapevo, ma non avevo messo «con quale configurazione
misuro»** — e quella è la domanda che viene prima di tutte.

**NON PREVISTO AFFATTO:** il **gauge degenere 1 passo su 31**. Non lo cercavo, non è in nessuna voce
del registro, ed è **indipendente dall'ancoraggio** che era l'oggetto del giro.

## 5. TODO DEL PROSSIMO PASSO

- [ ] **decisione di Luca:** `Z9` non si cura da `ritmo()` senza scegliere un **gauge nuovo** (A4).
      **Confermare la chiusura di quella strada**, o aprire la decisione sul gauge.
- [ ] **`Z34` da aprire?** il **gauge degenere** (`median(|f|) = 0` nel 3.2 % dei passi, `r` binario,
      pavimento `1e-9` che diventa il parametro fisico) — **difetto nuovo, mai registrato**
- [ ] **presidio da considerare:** ogni sonda dovrebbe **stampare la configurazione** come fa
      `_rimisura_Z9.py` dal passo 0. **Due errori di questa classe in due giri.**
- [ ] **⚠ NON toccare:** `ramp`, `TAU_A`, il `+1e-6`, `Z31`, il punto 1 di `Z24`
