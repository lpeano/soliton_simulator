# PREVISIONI — **il run a 6000 passi sulla scena video**

**Scritte e committate PRIMA del run** *(mandato ②)*. **Data:** 2026-09-19 · **Blob** `7c4dec1d`
*(sigillato 12/12)* · **seme effettivo `42`** · scena `N-MASSE`, 3 masse, `sep 8`, **un seme**.

> **Perché esistono:** una previsione scritta dopo non è una previsione. **E servono a essere
> SMENTITE:** sul giro precedente due mie previsioni su `ramp` sono cadute (`Z9`, `f3895aa`), ed è
> stato il pezzo più utile di quel lavoro.
> **Distinguo due generi, perché non valgono uguale:** ciò che **DERIVA dal codice** *(e allora
> sbagliarmi significa che ho letto male il sorgente)* e ciò che è una **SCOMMESSA sul
> comportamento** *(e allora sbagliarmi è informazione)*.

---

## 1. `Z9-b` — **il criterio che può davvero fallire**

**Stato a 2400 passi:** `median(ramp[i]·ramp[j])` sugli archi interni alla coorte originale =
**`0.074950`**, frazione di archi maturi **`0.000000` esatto**.

**DERIVATO dal codice** *(non è una scommessa)*: `ramp = min(1, eta/TAU_A)` e
`d(eta)/d(passo) = DT·r`, quindi **`passi(ramp = 1) = 5000/r`**. Col `r` mediano dei mobili
misurato dal pilota (`0.9808`) fa **`5098` passi**, e **6000 > 5098**.

| # | previsione | come si smentisce |
|---|---|---|
| **P1** | **`Z9-b` cresce di almeno un ordine di grandezza**: da `0.075` a **`> 0.5`** | resta sotto `0.5` |
| **P2** | **la crescita NON è lineare nel passo: SATURA**, perché `ramp` è troncato a 1 | cresce ~lineare fino alla fine |
| **P3** | **NON scommetto che arrivi esattamente a `1`**, cioè che `Z9` si chiuda in questo run | arriva a `1`: allora `Z9` si chiude |

> **⚠ E `P3` non è prudenza: è il numero del pilota.** `r` si è mosso del **`+148.82 %` in 120
> passi**, quindi `5098` è **un'istantanea, non una previsione**. Il margine è del **18 %**.
> **Se `r` scendesse verso il pavimento come nel batch di `Z46`, `Z9-b` smetterebbe di crescere e
> il criterio resterebbe aperto PER SEMPRE — ed è esattamente ciò che `Z9` dice che può accadere.**

## 2. `ramp` per coorte — **dove mi aspetto di essere smentito**

**Stato a 2400 passi:** coorte originale `fr(ramp > 0.5) = 0.3768`; **`fr(ramp > 0.9) = ZERO
ovunque, in ogni coorte, a ogni istante**.

| # | previsione | come si smentisce |
|---|---|---|
| **P4** | **`fr(ramp > 0.9)` diventa `> 0` per la coorte originale.** È il fatto nuovo che questo run può produrre | resta **zero**: sarebbe un risultato forte, e direbbe che qualcosa impedisce la saturazione |
| **P5** | **`fr(ramp > 0.5)` della coorte originale supera `0.8`** | resta sotto |
| **P6** | **il divario coorte-originale / popolazione RESTA** *(era `2.67x`)*, perché i neonati nascono con `eta = 0` di continuo | il divario si chiude |

## 3. `p95/p05` di `ramp[i]·ramp[j]` — **prevedo una NON-MONOTONIA**

**Stato:** `2.31` al frame 10 → **`8.56`** al frame 400. **Cresceva.**

> **P7 — PREVEDO CHE SI INVERTA: cresce ancora e poi CALA verso `1`.**
> **La ragione è strutturale, non un'intuizione:** `ramp = min(1, ·)` ha **un tetto**. Finché i
> nodi sono lontani dalla saturazione la dispersione può allargarsi; **quando i vecchi arrivano a
> `1` il numeratore si blocca e il rapporto DEVE comprimersi.**
> **Si smentisce** se cresce monotonamente fino a 6000 passi — e allora la saturazione non sta
> arrivando, il che **contraddirebbe `P1`** *(le due previsioni sono legate: non possono essere
> entrambe sbagliate nella stessa direzione)*.

**E `Z9` chiede di distinguere:** *«il kernel acerbo non riscala i pesi: li RIPESA»*.
**P8 — se `p95/p05` torna verso `1`, allora il ripesaggio è un TRANSITORIO di immaturità; se resta
alto, è una proprietà del regime.** **Questa è la domanda vera, e non ho una previsione: è ciò che
il run deve dire.**

## 4. Le CONSEGUENZE (`base`, `psi`, `rho_spin`, `cs`) — **NON HO UNA PREVISIONE, e lo dichiaro**

Il registro dice che **non sono mai state misurate** a maturazione. **Non ho un fatto stabilito su
cui appoggiarmi, e inventare un'aspettativa qui sarebbe P1 applicato male** — associazione spacciata
per conclusione.

**L'unica cosa che mi sento di scrivere, e viene da una misura altrui:**

> **P9 — `cs` resta VIVO** (`cs_std/cs` dell'ordine del **`10 %`**, non dello `0.01 %`), perché
> **`Z39` lo ha già misurato al `17.6 %`** e ha fatto cadere il fatto opposto di `CLAUDE.md`.
> Si smentisce se `cs_std/cs` torna sotto l'`1 %`.

## 5. Il CICLO oltre `Z49`

**Stato:** `nodi(regione interna)` `900 → 221 → 907` in 2400 passi; dilatazione che **rimbalza**
(`-7.44 → -2.70 → -4.21 → +2.80 → -1.13 %`). **`Z49` si fermava lì.**

| # | previsione | come si smentisce |
|---|---|---|
| **P10** | **c'è almeno un SECONDO minimo** di `nodi(interni)` entro 6000 passi | non c'è: era un transitorio, non un ciclo |
| **P11** | **il ciclo NON è periodico a periodo fisso**: il secondo periodo è **più lungo** del primo, perché il sistema si dilata | periodo costante entro il 10 % |

> **⚠ Unità COMOVENTI** *(mandato ⑤)*: il confronto si fa su `R_anello(t)` **misurato**, non su
> raggi assoluti. **Un sistema che si espande, campionato a raggio fisso, produce ALIASING** —
> è `CLAUDE.md` par.4.

---

## 6. Cosa NON prevedo, e non proverò a dire

- **nessuna identificazione**: niente *bounce*, *oscillone*, *protone*, *confinamento*. **I numeri
  e la forma** *(mandato ③)*;
- **nessun verdetto di fisica da UN SEME e UNA SCENA**;
- **l'antimateria, se comparirà, viene dal BASCULAMENTO** (`--chi-basc` riscrive `perc_chi` entro
  il frame 10, `frac +1 = 0.000`), **non dalla generazione**. Non è una previsione: è un presidio
  di lettura, e va scritto anche se non serve;
- **`--tau-luce` è nel comando e il suo sigillo è 6/7** *(`T3` è un risultato dichiarato, `T4`/`T5`
  dicono che la legge è sana)*. **Ogni numero di questo run lo eredita, e va detto in testa al
  referto.**
