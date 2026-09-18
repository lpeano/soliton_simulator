# REFERTO — **La premessa di Luca è vera, la compensazione esiste. Ma la scelta del denominatore NON si vede a valle**

**Data:** 2026-09-18 · **Branch** `fork-su2` · **blob** `aa84755b` · **un seme (5), 60 passi, una scena**
**Task history:** `doc/TASK_HISTORY/2026-09-18_estensivita-omega-grado.md` (commit `75a15bc`,
**scritto e pushato PRIMA della misura**) · **Strumento:** `csv/_test_fork/_estensivita_grado.py`

---

## 0. IN TRE RIGHE

1. **«grado alto = regione densa» È UN FATTO**, non un'analogia: `corr(grado, rho) = +0.79`, e fra
   le due mode il rapporto è **637×**.
2. **La compensazione dell'inerzia ESISTE ed è grande — ma vive nel settore dello SPIN**, dove
   l'inerzia c'è davvero: `omega_s` è **~130 volte più piccolo** nel bulk che nei neonati.
3. **⚠ E la scelta del denominatore NON cambia la dipendenza dal grado dell'osservabile a valle:**
   `phivel` fa `×4.891` prima e `×4.853` dopo — **0.8 % di differenza.** **Il bias precede la cura
   e sopravvive alla cura.**

---

## 1. PASSO 0 — la catena, ri-verificata

La lettura committata in `a15716c` **regge**:

```
feedback + twist_nodo  ->  `coppia`  ->  / M_PH = 1.0 (UNIFORME)  ->  phivel     [settore FASE]
correzione = B x nb    ->  / inerzia (PER NODO)                   ->  omega_s    [settore SPIN]
```

**Quindi l'argomento della «doppia compensazione», come formulato, non può applicarsi al canale del
feedback: a valle di quel canale non c'è nessuna inerzia, c'è una costante.**
*(Restava aperta la via indiretta `phivel → phi → psi → rho → inerzia`: il §3 la mette alla prova.)*

## 2. PASSO 1 — **la premessa di Luca regge, e fortemente**

| | `corr(grado, ·)` | mediana a `g=2` | a `g≥100` | rapporto |
|---|---|---|---|---|
| **`rho_sorgente`** (POST) | **+0.7923** | 0.002282 | **1.453** | **636.8×** |
| `rho_sorgente` (PRE) | +0.7881 | 0.001885 | 1.397 | 740.9× |
| `peq_nodo` (POST) | +0.7629 | 0.3402 | 0.6659 | 1.957× |

> **«Gli archi nascono per prossimità, quindi grado alto = regione densa»: confermato.** Non era un
> fatto stabilito nel repo — era una premessa — **e adesso lo è.**

## 3. PASSO 2 — **la compensazione ha una base misurata**

| | `corr(grado, ·)` | `g=2` | `g≥100` | rapporto |
|---|---|---|---|---|
| contrasto `rho/peq` (POST) | +0.1999 | 0.007635 | 2.249 | **294.6×** |
| contrasto `rho/peq` (PRE) | +0.2521 | 0.005096 | 2.287 | 448.8× |

**⚠ E qui la correlazione e il rapporto dicono cose diverse — la correlazione è quella sbagliata.**
`corr = +0.20` sembra debole, ma su una distribuzione **bimodale con code pesanti** Pearson è
dominato dalla varianza *dentro* il bulk. **Il rapporto fra le mode — `295×` — è la statistica
giusta**, ed è la lezione già pagata in `Z27`.

> **Il contrasto `rho/peq` cresce di ~300 volte fra neonati e bulk: l'ingrediente della
> compensazione c'è, ed è enorme.**

*(Rinuncia dichiarata: si riporta il **contrasto**, non l'inerzia piena — il fattore `(d/cs)²` è una
locale di `_passo_spinoriale` e il simulatore non lo espone. Ricostruirlo qui sarebbe una
ri-implementazione, e chiamarlo «inerzia» un fallback silenzioso, P5.)*

## 4. PASSO 3 — **la misura chiesta, e i due settori danno verdetti OPPOSTI**

| osservabile | variante | `g = 2` | `g ≥ 100` | rapporto | `corr(grado)` |
|---|---|---|---|---|---|
| **`phivel`** *(dove il feedback ENTRA)* | PRE (`/grado`) | 1.938 | 9.478 | **4.891** | +0.482 |
| | **POST (`nudo`)** | 1.893 | 9.186 | **4.853** | +0.483 |
| **`omega_s`** *(la catena dell'INERZIA)* | PRE | 56.23 | 0.4284 | **0.00762** | −0.215 |
| | POST | 42.04 | 0.4461 | **0.01061** | −0.144 |

### `omega_s` — **l'argomento di Luca è CONFERMATO, dove l'inerzia c'è**

**`omega_s` DECRESCE col grado di un fattore ~130.** I neonati ruotano ~100 volte più dei nodi
maturi. È **esattamente** ciò che l'argomento prevede: contrasto `rho/peq` **×295** verso il bulk,
inerzia alta, **rotazione minore a parità di coppia**.

> **La compensazione non è una speculazione: è misurata, e il segno è quello giusto.**

### `phivel` — **e qui la terza lettura, quella che avevo chiamato «la più interessante»**

**`4.891` prima, `4.853` dopo: 0.8 % di differenza.**

E il confronto è più forte di quanto sembri, perché **PRE e POST sono i due estremi disponibili**:
il termine passa da **intensivo** (`0.989`) a **estensivo ×36.2** — **un fattore 37 sul termine** —
e l'osservabile a valle **non se ne accorge**.

> **Il bias di grado di `phivel` precede la cura, sopravvive alla cura, e non è il denominatore del
> feedback a produrlo.**

**La spiegazione più semplice, e la dichiaro come tale:** `coppia` contiene altri termini —
`_coppia_interferenza`, la repulsione, `twist_nodo` — e **la struttura in grado di `phivel` è
dominata da quelli**. Il feedback contribuisce troppo poco per spostarla. *(È coerente con l'A/B a
quattro semi, che non aveva mostrato effetto.)*

---

## 5. COSA NE SEGUE PER `Z30` — **e cambia la domanda**

**Avevo portato a Luca una scelta fra `36.2×` e `16.9×` come se fosse la posta in gioco.
Quei numeri sono sul TERMINE. A valle, su `phivel`, la differenza fra i due estremi vale `0.8 %`.**

**Quindi:**
- **il criterio «quale forma è meno estensiva» non discrimina**, perché l'osservabile non lo vede;
- **restano `A1` e §3, ed è quello che Luca aveva già detto: `nudo` non richiede nessuna scelta.**
  Ma ora non è solo un principio: **è una misura che dice che l'alternativa non compra niente**;
- **e `linea` non è "più sicuro": è solo una scelta in più senza un guadagno misurabile.**

**La speculazione di Luca regge, con una precisazione:** la compensazione che invoca è **reale e
misurata**, ma **agisce sul settore dello spin**, non su quello in cui il feedback entra. **Il
feedback non ha bisogno di essere normalizzato — non perché l'inerzia lo compensi, ma perché la sua
forma non arriva all'osservabile.**

## 6. I LIMITI, dichiarati

- **Un seme, 60 passi, una scena.** Orientamento, non statistica.
- **PRE e POST divergono** (traiettorie diverse): i valori **assoluti** non si confrontano fra i due
  giri. **Ciò che si confronta è il RAPPORTO fra le mode DENTRO ciascun giro**, ed è per questo che
  la misura è disegnata così.
- **Non è stato misurato se il bias di `phivel` sia esso stesso un difetto.** So che c'è (`×4.9`) e
  che non viene dal feedback. **Da dove venga, e se vada curato, è una domanda nuova.**
- **`omega_s` a `g=2` vale 42-56 contro 0.43-0.45 nel bulk:** i neonati ruotano in un regime
  totalmente diverso. **Non l'ho interpretato** — è il settore aliasato, e `Z9` resta aperta.
