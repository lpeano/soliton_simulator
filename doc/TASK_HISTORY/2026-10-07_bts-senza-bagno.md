# `B-TS` — **SENZA TERMOSTATO E SENZA SCUOTIMENTO: resta solo la dinamica interna** *(2026-10-07 sera, mandato di Luca)*

> ### ⛔ **SOLO DIAGNOSI. Nessun file del simulatore si tocca**, resta ### **`b8c21049`**, e
> i due interventi stanno ### **nello strumento**, con gli stessi controlli di `B-T` e `B-S`.

> ### 📌 **Committato e pushato PRIMA della modifica allo strumento e PRIMA della corsa.**

---

## 0. ✔ **IL FATTO, VERIFICATO DAI JSON DI `H3`** *(non ripreso dal mandato)*

### `(a)` in ### **`B-S`** il vuoto resta fresco e ### **le masse si scaldano DI PIÙ**

| passo | `std(phivel)` VUOTO | ### **MASSE** | masse/vuoto |
|--:|--:|--:|--:|
| `50` | `0.5392` | `0.7421` | `1.376` |
| `150` | `1.3292` | ### **`2.8992`** | ### **`2.181`** |
| `230` | `2.0788` | ### **`4.1939`** | `2.017` |
| `500` | `3.1879` | `6.3423` | `1.989` |

### ➜ **Le masse si scaldano anche DA DENTRO, e circa il DOPPIO del vuoto.** ✔

### `(b)` nel ### **controllo**, nei nodi delle masse, la ### **COPPIA scalda quanto lo scuotimento**

Somma fra il passo `50` e il `150` *(l'intervallo è ### **dichiarato**, perché cambia la
terza cifra)*:

| | somma `50..150` | somma `51..150` |
|---|--:|--:|
| `scuoti` | `+3.6540` | `+3.5999` |
| ### **`coppia`** | ### **`+3.8471`** | ### **`+3.8280`** |
| `termostato` | ### **`−5.7509`** | `−5.7502` |

### ➜ **La coppia scalda QUANTO lo scuotimento, e il termostato frena più di entrambi messi
insieme.** ✔ *(il mandato dice `3.82 / 3.63 / −5.68`: combacia entro l'intervallo di somma)*

---

## 1. ⭐ **E DUE NUMERI IN PIÙ, CHE HO CERCATO PRIMA DI PREVEDERE**

### ⛔ **`(c)` IN `B-S` IL RISCALDAMENTO DELLE MASSE È DOMINATO DAL TERMOSTATO, NON DALLA COPPIA**

Somma `1..230` nelle ### **masse**:

| braccio | `scuoti` | `termostato` | `coppia` | dominante |
|---|--:|--:|--:|---|
| `base` | `+9.705` | `−10.994` | `+5.619` | `termostato` *(`41.6 %`, e ### **FRENA**)* |
| `B-T` | `+11.236` | `−2.200` | `+4.984` | `scuoti` *(`60.8 %`)* |
| ### **`B-S`** | `+0.000` | ### **`+11.635`** | `+5.678` | ### **`termostato` *(`66.7 %`, e QUI POMPA)*** |

### ➜ **In `B-S` il termostato POMPA** *(il vuoto resta freddo, `E_cin` sta sotto
l'obiettivo, quindi `xi < 0`)*, **e il `66.7 %` del calore delle masse viene da lui.**
### ⭐ **Quindi `B-TS` toglie alle masse la loro SORGENTE PRINCIPALE in `B-S`** — e questo è
esattamente ciò che il braccio deve separare.

### ⭐ **`(d)` MA LA COPPIA È CONCENTRATA NELLE MASSE, ED È STABILE FRA I BRACCI**

| braccio | `coppia` nelle ### **MASSE** | nel VUOTO | ### **rapporto** |
|---|--:|--:|--:|
| `base` | `+5.619` | `+0.604` | ### **`9.31`** |
| `B-T` | `+4.984` | `+3.295` | `1.51` |
| `B-S` | `+5.678` | `+1.216` | `4.67` |

### ⛔ **Nelle masse la coppia vale `5.0–5.7` in TUTTI e tre i bracci**, cioè
### **non dipende dal bagno**: è una ### **sorgente interna AUTONOMA.**
### ➜ **E nel controllo agisce `9.31 ×` più nelle masse che nel vuoto.**

> ### ⭐ **È IL NUMERO CHE DECIDE LA MIA PREVISIONE**, e l'ho cercato ### **prima** di
> scriverla.

---

## 2. ⛔ **I CRITERI, FISSATI ADESSO** *(mandato di Luca)*

| esito | condizione |
|---|---|
| ### **`LA CAUSA È IL BAGNO GLOBALE`** | in `B-TS` l'AUC al `400` è ### **`>= 0.85`** ### **E** la coerenza di fase delle masse al `230` è ### **`>= 0.6`** |
| ### **`LA CAUSA È DENTRO LE MASSE (H2)`** | l'AUC al `400` è ### **`< 0.6`** ### **E** il bilancio delle masse mostra che è la ### **COPPIA** a far crescere `<phivel²>` |
| fra i due | ### **si riporta la curva e il termine dominante nelle masse** |
| ### **sempre** | se l'energia totale ### **resta finita, cresce o cala**: senza sorgenti né freni, la sua evoluzione dice se la dinamica interna ### **conserva, scalda o dissipa** |

### ⚠ **IL RISCHIO, DICHIARATO** *(dal mandato)*: senza freno la corsa può ### **divergere o
congelarsi.** ### **Se succede la fermo e lo riporto** — lo strumento ha già le guardie
*(`phivel` non finiti e massimo assoluto a ogni passo, con arresto e scrittura del json)*.

---

## 3. ⭐ **LE PREVISIONI, PRIMA DELLA CORSA**

### ⛔ **`PTS-1`: scatterà `LA CAUSA È DENTRO LE MASSE (H2)` — AUC al `400` `< 0.6`.**

### **Il perché, col numero `(d)`:** in `B-TS` l'unica sorgente rimasta è la ### **coppia**,
che agisce ### **`9.31 ×` più nelle masse che nel vuoto.** ### ➜ **Le masse si scaldano, il
vuoto resta quasi fermo** → `c_k` di MATERIA ### **scende**, quella del VUOTO ### **tiene o
sale** → ### **il contrasto si chiude da entrambi i lati**, come già visto in `B-S`
*(`c_k` VUOTO `0.4557` al `150` contro `0.2430` del controllo)*.

### ⭐ **`PTS-2`: il termine dominante nelle masse sarà la `coppia`.** Nelle altre tre corse
vale `5.0–5.7` ### **indipendentemente dal bagno**, e in `B-TS` è ### **l'unico rimasto.**

### ⚠ **`PTS-3`: l'energia totale CRESCE, ma `~10 ×` meno del controllo.**
Il conto: la coppia dà `+5.6` nelle masse e `+0.6` nel vuoto su `230` passi, e le masse sono
il ### **`9.66 %`** dei nodi, quindi il globale cresce di circa
`0.0966·5.6 + 0.9034·0.6 ≈ 1.08`, da `0.156` a ### **`~1.2`** — contro
### **`13.57`** del controllo al `230`. ### ➜ **`~11 ×` più freddo.**

### ⚠ **`PTS-4`: la coerenza di fase delle masse al `230` sarà `< 0.3`**, quindi
### **il criterio del bagno NON scatterà** *(chiede `>= 0.6`)*. In `B-S` era `0.0604` con
`std = 4.19`; in `B-TS` la `std` dovrebbe essere `~2.4` *(`√(0.17 + 5.6)`)*, cioè il
### **`57 %`** — meglio, ma non abbastanza.

### ✔ **`PTS-5`: NON divergerà entro `500` passi.** `B-S` ci è arrivato senza divergere, e
`B-TS` ha ### **una sorgente IN MENO** di `B-S` *(il termostato, che lì POMPAVA)*.
### ⚠ **E non si congelerà**, perché la coppia resta e vale `5.0–5.7` in tutti i bracci.

> ### ⛔ **E SE `PTS-1` SI SBAGLIASSE — cioè se l'AUC tenesse — sarebbe il risultato più
> importante della giornata:** vorrebbe dire che ### **le masse sopravvivono quando si toglie
> il bagno**, e che la cura sta ### **nel bagno globale**, non dentro le masse.

---

## 4. ⭐ **LA STELLA POLARE** *(`L-STELLA`)*

| | |
|---|---|
| `A14` | ### **NON SI APPLICA:** nessun termine di nessuna legge è aggiunto, tolto o cambiato nel simulatore. I due interventi spengono ### **dall'esterno**, per vedere |
| `ROBUSTEZZA-FISICA` | ### **NON SI APPLICA.** ### ⚠ **Ma il gradino di robustezza della MISURA è dichiarato:** `B-TS` eredita da `B-T` il fatto di ### **NON essere un azzeramento** del termostato |
| numeri o leggi aggiunti | ### **ZERO** |
| verso EM-curvatura | ### **NON SI APPLICA** |
| ### **emergente o imposto** | ### ⛔ **IMPOSTO:** è un'### **amputazione doppia**, non un modello. Serve a ### **separare due cause**, non a proporre una cura — ### **e la cura è decisione di Luca** |

---

## 5. TODO

- [ ] **(a)** questo task history, ### **committato PRIMA**;
- [ ] **(b)** il braccio `B-TS` in `csv/_test_fork/_termo_h3.py`, con il collaudo — e
      ### **il diff dichiarato**, perché cambia il blob dello strumento che ha prodotto gli
      altri tre bracci;
- [ ] **(c)** la corsa, `500` passi;
- [ ] **(d)** il referto, con `B-TS` accanto agli altri;
- [ ] **(e)** poi ### **FERMO. Se il criterio indica `H2`, NON comincio la cura.**
