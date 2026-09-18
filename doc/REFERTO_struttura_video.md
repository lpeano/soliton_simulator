# REFERTO — **Il ciclo c'è, ma non è nel corpo: è nella CODA. E l'anello si sfalda mentre il centro si accende**

**Data:** 2026-09-18 · **Blob `a1ae5090` INVARIATO** — nessuna cura, nessun cablaggio
**Run:** scena video, **400 frame = 2400 passi**, 1h49, `n` **2391 → 8018** · driver **sigillato**
**Previsioni scritte PRIMA:** `515ed53` · **Sonda:** `_struttura_video.py` (`6bb24e5e`)

> **⚠ IN TESTA, NON IN FONDO:**
> **`--tau-luce` HA IL SIGILLO FALLITO** (`doc/SIGILLO_tau_luce_FALLITO.md`, CLAUDE.md par.0):
> **la scena include una legge NON CERTIFICATA e OGNI numero di questo referto lo eredita.**
> **`--chi-basc` attivo. UN SEME, UNA SCENA. NESSUN VERDETTO DI FISICA, NESSUNA IDENTIFICAZIONE.**

---

## 0. LA SCENA È LA STESSA — confermato a quattro cifre

```
              frame 10   115      190      270      375
d MEDIA        0.9275   1.4502   1.6739   1.7537   1.4871      <- misurato
la tabella     0.934    1.454    1.676    1.753    1.483       <- i fotogrammi del video
```

**Combaciano ovunque.** *(E `n` al 270: `5443` contro `5465`; al 375: `7480` contro `7503`.)*

---

## 1. ⚠ IL CICLO ESISTE — **ma è nella CODA, non nel corpo**

```
frame     10        115       190       270       375       400
d MEDIA   0.9275    1.4502    1.6739    1.7537    1.4871    1.4004     <- SALE poi SCENDE
d MEDIANA 0.8626    0.9636    1.0126    1.1191    1.3191    1.3514     <- SALE SEMPRE
d p95     1.9709    4.6983    6.1655    6.3985    3.6234    2.9533     <- SALE poi CROLLA
```

> **La distanza TIPICA non si ricomprime mai: la mediana cresce monotona (`0.86 → 1.35`).**
> **È il `p95` a crollare — da `6.40` a `2.95`, dimezzato in 780 passi — e con lui la MEDIA.**
> **La «ricompressione» è il RIASSORBIMENTO DELLA CODA LUNGA, non una contrazione del corpo.**

**È esattamente la trappola che il §4 del mandato metteva in guardia** *(«se bimodale, non riportare
mediane»)*: **qui media e mediana dicono cose opposte, e solo la coppia descrive il fenomeno.**

**E la dilatazione non inverte soltanto: RIMBALZA** *(dal log, ogni 5 frame)*:

```
frame 370: -7.44 %    375: -2.70 %    380: -4.21 %    385: +2.80 %    400: -1.13 %
```

**La tabella dei fotogrammi si fermava al 375 e non poteva vederlo.**

## 2. ⚠ LA REGIONE INTERNA — **si svuota, poi si riempie, e si ACCENDE di cinque ordini**

```
frame   nodi(r<4)   rho_spin      |psi|        eta med   grado
10        900       3.66e-07     9.97e-05      0.338     127
115       291       6.53e-06     3.19e-04      7.05      157
190       224       3.49e-07     5.99e-05      11.57     143
270       221       5.14e-07     3.20e-03      17.35     121
375       559       4.06e-03     7.41e-02      26.46     127
400       907       5.59e-02     6.66e-01      28.60     109
```

> **Il centro si SVUOTA (900 → 221) e poi si RIEMPIE (221 → 907).**
> **E `rho_spin` passa da `5.1e-07` a `5.6e-02`: CINQUE ORDINI DI GRANDEZZA in 780 passi.**
> **`|psi|` da `3.2e-03` a `0.666`: duecento volte.**

**Il minimo di popolazione (frame 270) coincide col massimo di `d MEDIA` (1.754): il riempimento e la
ricompressione sono lo stesso intervallo.**

## 3. ⚠ E L'ANELLO SI SFALDA — **grado da 496 a 2**

```
frame          10     115    190    270    375    400
grado ANELLO   496    160     87      2      2      2
grado INTERNA  127    157    143    121    127    109
```

> **I nodi dell'anello perdono quasi tutti i legami: `496 → 2`.** **La regione interna li mantiene.**
> **Non è che la struttura «ingloba» le masse: le masse si DISGREGANO e la materia si concentra al
> centro.** *(È una descrizione dei numeri, non un meccanismo: il meccanismo non lo misuro.)*

## 4. ⚠ DI COSA È FATTA — **l'OPPOSTO di `Z48`, e il discriminante lo conferma**

```
frame     eta INTERNA   eta ANELLO    frac NATI interna   frac NATI anello
10        0.338         0.498         0.000               0.000
270       17.35          8.93         0.394               0.606
400       28.60          9.81         0.377               0.764
```

**La regione interna è TRE VOLTE più matura dell'anello** — e **i nodi nuovi stanno più nell'ANELLO
(76 %) che al centro (38 %)**.

**⚠ E il discriminante fissato nelle previsioni — `r` ricavato da `eta += DT·r`:**

```
intervallo      r INTERNA   r ANELLO    r/r_floor (interna)
10 -> 115       1.0793      0.7055      7.6e+05
270 -> 375      1.4096      0.5096      1.0e+06
375 -> 400      1.3920      0.3734      9.8e+05
```

> **`r` della regione interna vale `1.08 → 1.41`, cioè `10⁶` volte il pavimento: NON è ferma.**
> **La previsione diceva: *«se il loro `r` valesse `1.414212e-06`, "materia nuova" sarebbe
> sbagliato»*. NON lo vale. È l'OPPOSTO di `Z46`/`Z48`.**
> **E `r` dell'anello SCENDE (`0.71 → 0.37`): il centro accelera mentre l'anello rallenta.**

## 5. ⚠ `perc_chi` — **la separazione si ottiene SENZA contatori, e dice `chi_basc`**

```
frame       10      115      190      270      375      400
frac +1    0.000   0.0292   0.0369   0.0834   0.1468   0.1645
```

**Alla semina `chi_nuovi = rng.choice([-1,1])` darebbe `~0.50`. Al frame 10 vale `0.000`.**

> **⟹ `chi_basc` ha GIÀ RISCRITTO TUTTI I 2391 NODI entro il frame 10, azzerando il sorteggio di
> nascita.** **La separazione che avevo chiesto si ottiene per DEDUZIONE dai dati, non serve
> strumentare: il contributo della mitosi è invisibile contro il basculamento.**
> **L'antimateria di questa scena viene dal BASCULAMENTO, non dalla generazione.**

*(`0.1645` al frame 400 contro il `18.4 %` letto dai fotogrammi: coerente.)*
**⚠ LIMITE: è una deduzione da due numeri (`0.50` atteso, `0.000` misurato), non un conteggio. Un
conteggio diretto richiederebbe contatori durante il run, e NON è stato fatto.**

## 6. ✅ ASSOLUTO E COMOVENTE **CONCORDANO: la mia riserva cade, e lo dico**

`R_anello` misurato: `7.67 / 7.56 / 7.94 / 8.04 / 7.44 / 7.37` — **varia solo dell'8 %**, quindi le
due letture danno gli stessi numeri *(es. regione interna al frame 400: `907` nodi in assoluto,
`811` in comovente; `rho_spin` `5.59e-02` contro `5.56e-02`)*.

> **La riserva del task history era legittima — par.4 vieta gli intervalli fissi su un sistema che
> dilata — ma QUI non morde, perché l'anello non si è spostato abbastanza. Lo dichiaro invece di
> tenermi il dubbio.**
> **⚠ E vale solo perché `R_anello` è quasi costante: NON è una licenza generale.**

**E `R_anello` fa il ciclo da solo:** `7.56` (115) → **`8.04`** (270) → `7.37` (400). **Sale e
scende.** Così il `R p95` della nube: `8.48 → 9.84 → 9.42`.

## 7. E LA COERENZA GLOBALE **CROLLA** mentre il centro si accende

```
|<nb>| globale:  0.995 -> 0.678 -> 0.484 -> 0.269 -> 0.199 -> 0.190
```

**Cinque volte più bassa alla fine.** *(La `coer_l` locale del log fa l'opposto: sale a `0.669`.
Sono due grandezze diverse — globale contro locale — e vanno citate separate, non mediate.)*

---

## 8. COSA QUESTO **NON** DICE

- **NESSUNA IDENTIFICAZIONE.** Non dico cosa sia. **Riporto i numeri e la forma.**
- **Non misuro il MECCANISMO** per cui l'anello perde i legami e il centro si accende: **descrivo che
  accade, non perché.**
- **La previsione ① era «l'inversione c'è»: confermata. Ma NON avevo previsto che media e mediana
  dicessero cose opposte** — quello è il risultato, e l'ho trovato solo perché il §4 del mandato
  imponeva di non fidarsi delle mediane.
- **Un seme, una scena, `--tau-luce` non certificato**, **5 punti** per il profilo radiale e **5
  frame** di risoluzione per il ciclo.
