# REFERTO — **La Y non c'è: né nel denso, né nel vuoto, né nella variazione. Il dipolo sì**

**Data:** 2026-09-18 · **Blob `a1ae5090` INVARIATO** — **nessun run nuovo**, i sei `.pkl` esistevano
**Letture fissate PRIMA:** `0f7cea6` · **Sonda:** `_Y_nel_vuoto.py`

> **⚠ IN TESTA:** **`--tau-luce` HA IL SIGILLO FALLITO** (par.0): **ramo NON CERTIFICATO, e ogni
> numero lo eredita.** `--chi-basc` attivo. **UN SEME. NESSUN VERDETTO DI FISICA, NESSUNA
> IDENTIFICAZIONE.**

---

## 0. IL VERDETTO CONTRO LE QUATTRO LETTURE FISSATE PRIMA

| lettura | esito |
|---|---|
| `A_3` alto sul VUOTO ai frame precoci **E** sulla VARIAZIONE → la Y esiste | **NO** |
| **`A_3` al nullo in tutte e tre le varianti → artefatto della colormap** | **✓ È QUESTA** |
| **`A_1` domina anche sul vuoto e sulla variazione → il dipolo è la struttura** | **A METÀ: domina nella VARIAZIONE (`3.37×`), NON nel vuoto** |
| `N_eff` troppo basso → non si legge | **è scattata due volte, ed è dichiarata** |

> **Il rilievo era giusto — `Z50` aveva misurato il posto sbagliato — ma cercando nel posto giusto
> la Y non c'è lo stesso.**
> **`A_3` non supera mai DUE volte il nullo in nessuna delle tre varianti.**
> **`A_1` sì: `3.3×` nel denso, `3.37×` nella variazione finale.**

---

## 1. ① IL VUOTO INTERNO È **ISOTROPO**

```
caso                        nodi   N_eff  | A_1     A_2     A_3     A_6    | NULLO  | A_3/nullo  A_1/nullo
f10   vuoto < 1x mediana     883   883.0  | 0.0125  0.0349  0.0385  0.0243 | 0.0337 |   1.14       0.37
f115  vuoto < 1x mediana     268   268.0  | 0.0472  0.0868  0.0417  0.0406 | 0.0611 |   0.68       0.77
f190  vuoto < 1x mediana     222   222.0  | 0.0649  0.0407  0.0243  0.0506 | 0.0671 |   0.36       0.97
f270  vuoto < 1x mediana     222   222.0  | 0.0461  0.0152  0.0473  0.0770 | 0.0671 |   0.70       0.69
f375  vuoto < 1x mediana     224   224.0  | 0.1154  0.1751  0.0875  0.0362 | 0.0668 |   1.31       1.73
f400  vuoto < 0.1x mediana   113   113.0  | 0.1790  0.1174  0.1611  0.0605 | 0.0941 |   1.71       1.90
```

**`A_3/nullo` sta fra `0.36` e `1.71`: mai due volte il nullo.** **E al frame 10, dove la statistica
è migliore (`883` nodi), vale `1.14`.**

**Il controllo pesato sul DEFICIT concorda ovunque** *(differenze in terza cifra)*: **il risultato non
dipende dalla scelta del peso**, che era la mia riserva scritta prima.

**E l'istogramma del vuoto, al frame 115 — `268` nodi:**

```
tutti i 24 bin fra 0.448 e 1.343, media 1     (nel DENSO il picco arrivava a 3.998)
```

> **Piatto. Nessun braccio, nessun avvallamento a tre.**

## 2. ② LA VARIAZIONE — **la misura che doveva rispondere, e risponde NO**

```
intervallo        nodi  N_eff  | A_1     A_2     A_3     A_6    | NULLO  | A_3/nullo  A_1/nullo
f10 -> 115         215  187.9  | 0.0500  0.0484  0.1213  0.1024 | 0.0730 |   1.66       0.69
f115 -> 190         20    —    (meno di 30: NON SI LEGGE)
f190 -> 270        157   14.9  | 0.3476  0.2252  0.2566  0.2399 | 0.2595 |   0.99       1.34
f270 -> 375        413   43.4  | 0.1007  0.2452  0.2380  0.0171 | 0.1518 |   1.57       0.66
f375 -> 400        733   76.3  | 0.3864  0.3151  0.2196  0.1350 | 0.1145 |   1.92       3.37
```

**`A_3/nullo` non supera `1.92` in nessun intervallo, e nell'intervallo con la statistica migliore
(`f10→115`, `N_eff = 188`) vale `1.66`.**

> **Il campo NON si accende lungo tre bracci.**
> **⚠ E nell'ultimo intervallo `A_1/nullo = 3.37`: si accende lungo UNA direzione.**

*(`f115→190` ha **20 nodi** e `f190→270` ha `N_eff = 14.9`: **lì non si legge, e non l'ho letto.**)*

## 3. ③ L'ANDAMENTO NEL TEMPO — **il vuoto non si struttura mai**

```
frame | DEN A_1  DEN A_3  DEN null  N_eff | VUO A_1  VUO A_3  VUO null  N_eff
10    |   -        -        -         0   | 0.0125   0.0385   0.0337    883
115   |   -        -        -         0   | 0.0472   0.0417   0.0611    268
190   |   -        -        -         0   | 0.0649   0.0243   0.0671    222
270   |   -        -        -         0   | 0.0461   0.0473   0.0671    222
375   |   -        -        -        18   | 0.1154   0.0875   0.0668    224
400   | 0.4001   0.2310   0.1198    69.6  | 0.1328   0.0692   0.0729    188
```

**Il vuoto resta al nullo per tutti e sei gli istanti.** **Non c'è nessun «alto presto e poi cala»:
non c'è mai stato niente da calare.**
**E la regione DENSA non esiste prima del frame 375** *(coerente con `Z49`)*: **quando compare, il
suo modo dominante è `A_1`.**

---

## 4. COSA QUESTO DICE, E COSA NO

**DICE:** **con tre definizioni diverse di «dove cercare» — denso, vuoto, variazione — e con il
nullo accanto a ogni numero, `A_3` non supera mai due volte il nullo.** **La firma a tre bracci non
c'è.** **L'osservazione visiva era un'impressione, e la colormap satura.**

**DICE ANCHE:** **`A_1` è l'unico modo che supera il nullo in modo netto**, e lo fa in **due** delle
tre varianti — `3.3×` nel denso, `3.37×` nella variazione finale. **Il sistema si accende lungo UNA
direzione, non tre.**

**NON DICE:**
- **che nel video non si veda niente.** Dice che **ciò che si vede non ha una firma a tre bracci in
  `rho_spin`**. **Una struttura può essere visibile in `|psi|` proiettato sulla griglia
  (`campo_spaziale`, con il kernel FFT) e non nella distribuzione ANGOLARE dei NODI**: sono due
  oggetti diversi, e **questa misura ha guardato il secondo.**
- **⚠ E questo è un limite VERO della misura, non una scusa:** `A_m` sui nodi pesa **i puntatori**,
  mentre il fotogramma mostra **il campo interpolato fra di essi.** **Per chiudere davvero servirebbe
  `A_m` sulla griglia di `campo_spaziale`, e NON è stato fatto.**
- **NON è un verdetto sulla predizione di Luca**, che riguarda il **CICLO** e si decide col run a due
  masse — **in corso.**

**`Z50` è QUALIFICATA, non corretta:** vale **per la regione densa**, e questo referto ne è il
complemento sul vuoto e sulla variazione. **Le conclusioni concordano.**

## 5. I LIMITI

**Un seme, `--tau-luce` non certificato, sei istanti.** **`N_eff` sotto 30 in due intervalli su
cinque: lì non si legge, ed è stampato.** **E la misura è sui NODI, non sul campo interpolato** —
**il confronto con il fotogramma resta aperto.**
