# REFERTO — **A/B su `--nmasse`: il ciclo c'è anche a DUE masse. Ma si spezza in due fenomeni**

**Data:** 2026-09-18 · **Blob `a1ae5090`** · **Predizione di Luca committata PRIMA del run:** `a4fbe42`
**Sonda:** `_ab_due_tre.py` (committata **prima** di girarla, `7f81634`) · **Output:** `csv/_test_fork/_ab_due_tre.txt`

> **⚠ IN TESTA:** **`--tau-luce` HA IL SIGILLO FALLITO** (par.0): **entrambi** i bracci girano su un
> ramo **NON CERTIFICATO**, e ogni numero lo eredita. **`--chi-basc` attivo in entrambi.**
> **UN SEME PER BRACCIO.** **NESSUN VERDETTO DI FISICA, NESSUNA IDENTIFICAZIONE.**
> **⚠ E un limite di PROGETTO, non di esecuzione:** è un A/B su **`--nmasse`**, **non su «tre corpi»**.
> Numero di masse, **popolazione** e geometria della semina cambiano **insieme**: **le cause non sono
> separate.**

---

## 0. ⚠ IL VERDETTO — **LA PREDIZIONE DI LUCA, NELLA SUA FORMA FORTE, È SBAGLIATA**

> **«Con DUE masse questa dinamica NON ci sarà più. Sarà completamente differente.»**

**Non è così, e si scrive che non è così.** **Il ciclo c'è anche a due masse**, e la **fase di
svuotamento** è **quantitativamente la stessa**.

**Ma la lettura ② secca — «ciclo uguale, quindi è solo un oscillatore di rilassamento» — non scatta
nemmeno lei.** Scatta **la terza**, quella che era stata tenuta aperta:

| lettura fissata in `a4fbe42` | esito |
|---|---|
| ① ciclo **assente** o forma **completamente diversa** → la predizione REGGE | **NO** |
| ② ciclo **uguale** → oscillatore di rilassamento, predizione **SBAGLIATA** | **solo sulla DISCESA** |
| ③ **ciclo con forma o periodo diversi** → né l'una né l'altra, si riporta come tale | **✓ È QUESTA** |

> **IL CICLO SI SEPARA IN DUE FENOMENI, e non erano stati distinti prima:**
> **① LO SVUOTAMENTO è del SISTEMA** — identico a due e a tre masse;
> **② IL RIEMPIMENTO E L'ACCENSIONE dipendono dal NUMERO DI MASSE** — e la differenza è grande.

---

## 1. LA CURVA CHE DECIDE — `nodi(regione interna)`

**Era la curva nominata nella predizione**, e la regione è quella dichiarata prima:
**`r < R_anello(t)/2`** con `R_anello(t)` **misurato**, **più** la lettura assoluta `r < 4`.

```
ASSOLUTA  (r < 4)        f10    f115   f190   f270   f375   f400  | min/f10  f400/min
TRE  (Z49)               900    291    224    221    559    907   | 0.2456   4.1041
DUE  (ctrl)              901    323    242    245    414    559   | 0.2686   2.3099

COMOVENTE (r < R_an/2)   f10    f115   f190   f270   f375   f400  | min/f10  f400/min
TRE  (Z49)               883    268    222    222    497    811   | 0.2514   3.6532
DUE  (ctrl)              867    242    191    216    274    332   | 0.2203   1.7382
```

> **LA DISCESA È LA STESSA: `min/f10` vale `0.246` e `0.269` (assoluta), `0.251` e `0.220`
> (comovente).** **Quattro numeri, due bracci, stesso valore entro il 20 %.**
> **Il minimo cade allo STESSO istante nella lettura comovente: `f190` in entrambi.**
> **La risalita c'è in tutte e quattro le letture**, ma il recupero vale `3.65` contro `1.74`.

### 1.1 ⚠ IL FALSIFICATORE 2 **SCATTA**, ed era stato fissato prima

```
R_anello   TRE  7.672 7.557 7.944 8.039 7.445 7.371   escursione =  9.1 %
           DUE  7.432 6.731 7.126 7.495 6.549 6.239   escursione = 20.1 %
```

**La previsione diceva: *«se `R_anello` con due masse variasse molto più dell'8 %, la lettura
assoluta è aliasata e si scarta»*.** **Varia il `20.1 %`, due volte e mezzo la soglia.**
**Quindi la lettura che vale è la COMOVENTE** — ed è **la meno generosa** delle due
(`1.74` invece di `2.31`). **Non ho scelto la più comoda.**

### 1.2 ⚠ E LA LETTURA CHE DECIDE DAVVERO — **dichiarata POST-HOC, non era fissata prima**

**Fra il minimo e la fine, `n` cresce di quasi il doppio in ENTRAMBI i bracci.** Quindi un conteggio
che raddoppia può voler dire **«la regione si riempie»** oppure **«il sistema cresce e la regione lo
segue»**. **Il rapporto fra i due tassi separa i due casi.**

```
braccio      f_min   int_min  int_f400  n_min   n_f400  | recupero / crescita
TRE  (Z49)    190      222      811     4307     8018   |      1.9624
DUE  (ctrl)   190      191      332     3350     5878   |      0.9906
```

> **A TRE masse la regione interna si riempie DUE VOLTE più in fretta del sistema.**
> **A DUE masse cresce ESATTAMENTE come il sistema: `0.9906`.**
> **Cioè: in senso relativo, a due masse NON si riempie affatto. Ciò che la lettura in conteggio
> nudo mostra come «risalita» è la crescita della popolazione, non un riempimento.**

**⚠ E va pesata per quello che è:** **questa normalizzazione l'ho aggiunta DOPO aver visto i numeri.**
La lettura fissata prima è il **conteggio nudo**, e quella **dà una U in entrambi i bracci.**
**Chi legge deve poter dare peso diverso alle due cose, e per questo sono riportate entrambe.**

---

## 2. L'ACCENSIONE — il **falsificatore 3**, e non scatta alla lettera

**Era scritto:** *«se il ciclo ci fosse ma con `rho_spin` che NON si accende, allora "ciclo" e
"accensione" sono due fenomeni separabili — e sarebbe più informativo di entrambe le letture del §1»*.

```
rho_spin med (interna COMOVENTE)
             f10         f115        f190        f270        f375        f400       | escursione
TRE  (Z49)   3.7728e-07  6.5691e-06  3.4709e-07  5.0703e-07  4.0612e-03  5.5564e-02 | x1.601e+05
DUE  (ctrl)  4.4894e-07  3.3742e-04  7.5504e-05  1.0729e-06  2.6102e-04  2.4743e-03 | x5512
   -> RAPPORTO TRE/DUE all'ultimo istante: x22.46

|psi| med    9.9998e-05  3.2389e-04  5.8846e-05  3.2026e-03  7.5722e-02  6.7782e-01 | x1.152e+04   (TRE)
             1.1506e-04  2.6294e-03  1.0196e-03  1.2889e-04  2.2785e-02  4.6735e-02 | x406.2       (DUE)
   -> RAPPORTO TRE/DUE all'ultimo istante: x14.5
```

> **`rho_spin` SI ACCENDE anche a due masse — `x5512` sull'arco del run. Il falsificatore 3, come era
> scritto, NON scatta.**
> **Ma l'accensione finale è `22.46` volte più debole, e `|psi|` `14.5` volte.**

**E la FORMA dell'accensione è diversa, ed è la cosa che il rapporto finale non mostra:**
- **a TRE masse** `rho_spin` resta **piatta e bassa** (`3.8e-07 → 5.1e-07`) per quattro istanti su
  sei, e poi **esplode** fra `f270` e `f400` (`x1.1e+05` in 130 frame): **un evento TARDIVO e BRUSCO**;
- **a DUE masse** si accende **PRESTO** (`3.37e-04` al `f115`, cioè **51 volte** il valore a tre masse
  nello stesso istante), poi **SI SPEGNE** (`1.07e-06` al `f270`, un fattore `315` in giù), e **poi
  risale**, più debole.

> **La separabilità che il falsificatore 3 anticipava c'è — ma lungo una cucitura diversa da quella
> prevista.** **Non è «ciclo sì, accensione no»: è «svuotamento uguale, riempimento e accensione
> dipendenti dal numero di masse».**

---

## 3. DOVE I DUE BRACCI SONO **INDISTINGUIBILI** — e conta quanto il resto

```
                   TRE (f10 -> f400)         DUE (f10 -> f400)
d MEDIANO          0.8626 -> 1.3514  x1.57   0.8955 -> 1.2664  x1.41
coer |<nb>|        0.9953 -> 0.1900          0.9935 -> 0.1754
frac +1 (perc_chi) 0.0000 -> 0.1645          0.0011 -> 0.1851
r INTERNA          1.078  -> 1.392           1.058  -> 1.310
r int / r_floor    ~7.6e5 -> ~9.8e5          ~7.5e5 -> ~9.3e5
```

**`d` mediano cresce in modo monotono in ENTRAMBI: nessuna «ricompressione» nella mediana** — coerente
con `Z49`, dove il ciclo era **nella coda**, non nella mediana.
**La decoerenza del Bloch è la stessa curva.** **`perc_chi` è persino leggermente più alto a due masse.**

**E il discriminante di `Z46` NON scatta in nessuno dei due bracci:** `r/r_floor ~ 10⁶`, non `1.0000`.
**La regione interna non è ferma, né a due né a tre masse.**

### 3.1 ⚠ MA UNA COSA DI `Z49` **NON SI RIPRODUCE**: l'anello che rallenta

```
r ANELLO   TRE   0.7090  0.7831  0.7219  0.5233  0.3877   <- SCENDE, monotono dopo il primo
           DUE   0.8196  0.9823  0.8928  0.6206  1.0035   <- NON scende: finisce SOPRA il valore iniziale
```

> **`Z49` aveva scritto: *«il centro accelera mentre l'anello rallenta»*.**
> **Il centro accelera in entrambi. L'anello rallenta SOLO a tre masse.**
> **A due masse l'anello finisce a `1.0035`, cioè più veloce di come era partito.**

**E la nube gonfia e si ricomprime in entrambi**, ma a due masse è **più grande** e il picco è **più
tardi**: `R p95` va `8.48 → 9.84 (f190) → 9.42` a tre masse, `8.49 → 10.64 (f270) → 10.30` a due.

---

## 4. IL FALSIFICATORE 1 — **già scattato prima del run, e resta**

```
n0 TRE = 2391   n0 DUE = 1895   atteso proporzionale 2/3 = 1594   MISURATO = 79.3 %
```

**La semina per massa NON è lineare nel numero di masse.** **Le due scene differiscono anche per
POPOLAZIONE, in modo non proporzionale**, ed era registrato nel ledger durante il pilota.
**È esattamente la ragione per cui il limite di progetto in testa non è una formalità:
`--nmasse` cambia tre cose insieme.**

---

## 5. COSA QUESTO DICE, E COSA NO

**DICE:**
- **la predizione di Luca nella sua forma forte è SBAGLIATA**: la dinamica **c'è** anche a due masse,
  e la **discesa** è la stessa entro il 20 % su quattro letture;
- **ma il ciclo NON è un solo fenomeno**: **lo svuotamento è del sistema**, **il riempimento e
  l'accensione dipendono dal numero di masse** — `recupero/crescita` **`1.96` contro `0.99`**,
  accensione finale **`x22.46`**;
- **e una conclusione di `Z49` non si trasporta**: **l'anello che rallenta è un fatto a tre masse.**

**NON DICE:**
- **che sia l'interazione a tre corpi.** **Non è separata** da popolazione e geometria: **tre cause,
  un interruttore.** Per separarle servirebbe un braccio a **due masse con la popolazione di tre**,
  e **non è stato fatto.**
- **che il meccanismo nominato nella lettura ② sia quello.** `lambda_nodi` che accorcia la portata
  dove la densità cresce **è un candidato NOMINATO, non MISURATO**: questo A/B **non lo tocca.**
- **niente sulla barra d'errore.** **Un seme per braccio.** Su questo sistema caotico la dispersione
  **fra semi** è nota per essere grande (par.9, C10). **`x22.46` e `1.96 contro 0.99` sono rapporti
  grandi, ma NON hanno una barra**, e con un seme **non possono averla.**
  **Per renderli un fatto servono ≥ 4 semi per braccio** (par.9, P3).

## 6. I LIMITI, tutti insieme

**Un seme per braccio · `--tau-luce` col SIGILLO FALLITO su ENTRAMBI · `--chi-basc` attivo ·
sei istanti · A/B su `--nmasse` e non su «tre corpi» · la normalizzazione del §1.2 è POST-HOC ·
la lettura assoluta è ALIASATA a due masse (`R_anello` varia il `20.1 %`) e si usa la comovente ·
NESSUNA IDENTIFICAZIONE DI FISICA.**
