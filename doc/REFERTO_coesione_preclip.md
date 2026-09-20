# REFERTO — **il clip PROTEGGE, non produce. La cura autorizzata NON puo' passare il suo `Z3`.**

> `§4` del via libera, eseguito **PRIMA** della cura come ordinato. **Nessuna cura applicata:
> mi fermo e riporto, come il mandato prescrive.**
> Simulatore `d06219de -> d163510d` *(solo la traccia pre-clip, byte-inerte)*. Rigiocata `0 -> 120`
> del ramo B, **sigillo interno `138/138`**. Dati: `csv/_test_fork/_coesione_preclip.txt`,
> `_coesione_popolazione.txt`.

---

## 1. LA MISURA — **`coesione_relazionale` e' da 80 a 2 MILIONI di volte il suo tetto**

```
passo      archi    saturi   |c|/t p50   |c|/t p99   |c|/t max | arco 16-481: coes / tetto
10        527522    520906   2.654e+06   9.014e+08   2.029e+12 |   39543.7 / 0.0179543  rap 2.20e+06
40        527646    526461   2.152e+05   7.851e+07   7.391e+10 |   258.485 / 0.156566   rap 1.65e+03
60        527716    526958   1.003e+05   3.172e+07   6.288e+11 |  -4090.29 / 0.231750   rap 1.77e+04
100       527810    521295        6439   5.622e+06   4.484e+10 |  -910.173 / 0.638542   rap 1.43e+03
110       527830    500393        5812   3.532e+06   1.456e+11 |   30.0149 / 0.371541   rap 8.08e+01

SATURI su tutti i campioni: 62 601 833 su 63 322 622 = 98.86 %
```

**Il criterio era fissato PRIMA, e non lascia margine di lettura:**
> *«`|coes| >> tetto` -> il clip PROTEGGE, il difetto e' nel TERMINE; `|coes| ~ tetto` -> e' il clip
> a produrre il movimento, e il tetto e' la cura.»*

**`|coes|/tetto` ha mediana fra `5.8e+03` e `2.7e+06`. IL CLIP PROTEGGE.**

---

## 2. ⚠ LA CONSEGUENZA: **la cura autorizzata fallirebbe `Z3` PER COSTRUZIONE**

`Z3` chiede: *«il clip NON e' piu' saturo; se resta a `1.000`, il difetto e' SPOSTATO, non curato,
e allora si FERMA e si riporta»*.

**Il tetto causale e' da `1.6x` a `56x` PIU' STRETTO di quello attuale.** Con `|coes|` che vale
`1e3`-`1e6` volte il tetto **attuale**, stringerlo **rende la saturazione PIU' certa, non meno.**

> **`Z3` non fallirebbe per un difetto dell'implementazione: fallirebbe perche' la cura non
> affronta la grandezza che sbaglia.** **Eseguirla e poi scoprirlo sarebbe stato spendere un giro
> per confermare cio' che questa misura dice in dieci minuti** — ed e' esattamente per questo che
> il `§4` era messo per primo.

### 2.1 ⚠ Ma una cosa il tetto causale LA FAREBBE, e va detta per non buttarla

**Con `|coes| >> tetto` il clip SATURA sempre, quindi `|delta d0| = tetto` ESATTAMENTE, a ogni passo.**
```
tetto di oggi      tanh(stress)*d0    -> cresce quando d0 cala  -> DIVERGE
tetto causale      c_sistema*DT       = 0.011314 COSTANTE       -> passeggiata LIMITATA
```
> **La cura NON curerebbe il difetto, ma CONTERREBBE la divergenza**: `d0` si muoverebbe di
> `+-0.0113` per passo seguendo il segno di `coes`, invece di poter perdere il `100 %` del proprio
> valore in un passo. **E' CONTENIMENTO, non cura, e chiamarla cura sarebbe falso.**
> **Se applicarla lo stesso, come contenimento dichiarato, e' una decisione di Luca.**

---

## 3. DA DOVE VIENE IL NUMERO — **`1/I_med` AL QUADRATO**

```python
:4950   scala_statale        = (CS_M ** 2) / I_med
:4975   I_arco               = 0.5 * (I_nodi[ii] + I_nodi[jj])      # ARCHI
:4976   I_med                = max(float(np.mean(I_nodi)), 1e-9)    # MEDIA sui NODI
:4964   coesione_relazionale = scala_statale * (...) * filtro * d0**2 * (I_arco / I_med)
```
**`I_med` compare AL QUADRATO al denominatore.** E `I_med = mean(|psi|^2)` e' **piccolissimo**:

| ramo | passo | `mean(I_nodi)` | `I_arco/I_med` | **`I_arco/I_med^2`** |
|---|---|---|---|---|
| **B** | 120 | `2.50e-04` | `0.555` | **`2216`** |
| **B** | 360 | `1.04e-03` | `1.095` | **`1048`** |
| **A** | 120 | `3.04e-04` | `0.359` | **`1183`** |
| **A** | 3000 | **`2.16e-01`** | `6.31` | **`29.2`** |

### 3.1 ⚠ E qui ci sono DUE cose diverse, e non vanno confuse

**(a) L'errore di POPOLAZIONE c'e', ma e' MITE:** `I_arco/I_med` vale `0.36`-`6.3`, **non** le
migliaia. *(Il precedente curato a `:4072` — stessa struttura, `rho_arco` sugli archi contro
`median(I_nodi)` sui nodi — li' il rapporto mediano misurato era **8830**. **Qui no**, e dirlo
diversamente sarebbe trasportare un numero fra due casi.)*

**(b) L'AMPLIFICATORE e' `1/I_med^2`**, cioe' una **NORMALIZZAZIONE SU UNA MEDIA GLOBALE, elevata
al quadrato**. `I_med ~ 2.5e-04` -> `1/I_med^2 ~ 1.6e+07`.
> **E' `A2`** *(«LOCALE PURA: la media globale introduce NON-LOCALITA'»)*, **al quadrato.**

### 3.2 E spiega PERCHE' il ramo A non e' esploso

**`I_med` cresce di TRE ordini** fra il passo 120 e il 3000 di A (`3.0e-04 -> 2.2e-01`), quindi
**`1/I_med^2` CALA di sei**: il fattore passa da `1183` a `29.2`, **quaranta volte piu' debole**.
> **Il termine si auto-attenua man mano che il sistema matura.** **Il ramo B e' stato fermato al
> passo 390, cioe' quando il fattore valeva ancora `~1000`.**
> **⚠ NON dico che sia QUESTA la ragione per cui A e' sopravvissuto e B no** — un seme per ramo, e
> le due traiettorie divergono per mille motivi. **Dico che il fattore c'e', e' misurato, e va di
> tre ordini nella direzione giusta.**

---

## 4. COSA PROPONGO — **e NON lo faccio senza via libera**

La cura vera non e' il tetto: e' **`I_med`**. E ha la stessa forma del precedente gia' curato a
`:4072`:
> **una scala LOCALE al posto di una media globale.** *(Li' fu `_Lam = mean(I)` a sostituire la
> costante `400`; qui servirebbe il movimento OPPOSTO: togliere la media globale.)*

**⚠ MA NON PROPONGO UNA FORMA**, e la ragione e' `A1`: **una scala nuova va DERIVATA**, e qui
**non ho ancora un candidato che non sia scelto.** `I_arco` stesso? Un `I` per-vicinato? **Sono
due direzioni diverse e nessuna delle due l'ho misurata.**

**QUELLO CHE SO DIRE ORA:**
- il tetto causale **contiene** ma non cura;
- il termine e' **`1e3`-`1e6`** volte il proprio limite, quindi **oggi la fisica della coesione non
  gira: gira il suo clip**;
- e **il clip e' l'unico motore di `d0`** su quell'arco (`Z79`: il `96-98 %` del movimento).

> **Cioe': `d0` e' governato da un LIMITE, e il limite e' l'unica cosa che ne decide l'ampiezza.
> Cambiare il limite cambia il comportamento del sistema — ed e' una decisione di FISICA.**

---

## 5. LIMITI

**UN seme, UN ramo, 120 passi.** I percentili sono su `~527 800` archi per campione *(quindi la
statistica per-arco e' solida)*, **ma la scena e' una e il seme uno.**
**E `I_med` di `A` al passo 3000 viene da una traiettoria diversa, non da una controprova.**
