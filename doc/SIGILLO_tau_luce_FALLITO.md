# `--tau-luce` — **SIGILLO FALLITO (T2, T3, T4). Ci si ferma.**

> **Scritto per Claude web** (§5-ter). Branch `fork-su2`, 2026-09-15.
> Blob **prima** `f5887254` → **dopo** `7d484580`. **Gate NON ri-timbrato**: i sigilli non passano.
> Il flag è **OFF di default** e **T1 dimostra la byte-identità**, quindi il comportamento di
> default del repo è **invariato**.

```
ESITO: T1=PASS   T2=FAIL   T3=FAIL   T4=FAIL   T5=PASS
SIGILLO COMPLESSIVO: FAIL
```

Per `CLAUDE.md` §2: *«se il sigillo FALLISCE, committa comunque lo stato + il fallimento e
FERMATI: non "aggiustare al volo" dentro lo stesso commit»*. **È quello che questo commit fa.**

---

## T1 — **PASS**, ed è il sigillo che copre di più

```
n_A = 1718   n_B = 1718   ->  CONFRONTABILI
21 campi confrontati, PEGGIOR max|A-B| = 0.000e+00   stato RNG identico
```

Confronto contro il file **prima** della modifica, quindi certifica **due** cose insieme: il flag OFF
è byte-identico, **e** l'estrazione di `_tempo_luce_nodo` da `_bloch_ritardato` **non ha cambiato una
virgola**.

## T2 — **FAIL, ma è un difetto del TEST**, e va detto senza sconti

```
n_A = 1718   n_B = 1647   ->  NON CONFRONTABILI
```

T2 forza `_tempo_luce_nodo` a restituire il `tau` vecchio, con un monkeypatch **sul metodo**. Ma il
metodo è **condiviso**: lo chiama anche `_bloch_ritardato`, e `--fork-su2-mem` è **attivo** nella
configurazione del sigillo.

> Il monkeypatch non ha cambiato **un** interruttore: ha cambiato **anche la ritardazione dello
> Strato 1**. Due meccanismi insieme ⇒ traiettoria diversa ⇒ `N` diverso.

È il rovescio della scelta — giusta — di avere **una sola** formula invece di due copie: un test
naïve che la sostituisce colpisce **entrambi** gli utilizzatori. **La scelta di progetto resta; il
test va riscritto** in modo che discrimini il chiamante.

**E il presidio ha funzionato:** la riga dei conteggi, stampata **per prima**, ha impedito di leggere
uno zero come identità. Con `N` diverso non c'è nulla da confrontare.

## T3 — **FAIL**: l'effetto è reale e grande, ma **la metà di quello predetto**

| | pendenza | SE | r² | n | IC 95 % |
|---|---|---|---|---|---|
| OFF | −0.1685 | 0.0090 | 0.126 | 2417 | [−0.1862, −0.1507] |
| **ON** | **−0.4265** | **0.0091** | 0.464 | 2534 | [−0.4444, −0.4086] |

> **La pendenza si è spostata di 0.258, cioè ~28 sigma: l'effetto è indiscutibilmente reale.**
> **Ma l'attesa era −1.03** (naive) **o −0.69** (stima onesta col transitorio): misurata **−0.43**,
> `z` dalla attesa naive = **66**. **Circa la metà.**

Il criterio chiedeva uno spostamento di almeno 0.3: **0.258 non lo raggiunge**. FAIL.

> **Non ho una spiegazione della metà mancante, e non ne invento una.** È esattamente il punto in cui
> stanotte ho sbagliato tre volte generando scuse. Il numero si riporta; la causa si cerca dopo, con
> un criterio scritto prima.

## T4 — **FAIL a metà, e il perché è un REPERTO che riguarda anche lo Strato 1**

```
d  -> 2d    : tau_nuovo/tau_vecchio = 2.000000   (atteso 2.000000)   <- ESATTO
cs -> 2cs   : tau_nuovo/tau_vecchio = 1.000000   (atteso 0.500000)   <- NON SEGUE
CONTRASTO, legge VECCHIA con d -> 2d: 1.000000   (resta ferma, come dev'essere)
```

**Sulla geometria è una legge, e in modo esatto.** Sul `cs` **no** — e la causa non è il cablaggio
nuovo:

```
  passo |    n  | len(_cs_nodo_prev) | cache usabile (len >= n)?
      6 |  1196 |               1196 | SI
     12 |  1355 |               1322 | NO -> cs = CS_M costante
     30 |  1821 |               1804 | NO -> cs = CS_M costante
  cache usabile in 6 passi su 30 (20%)
```

> `_cs_nodo_prev` è scritta in `step()` con l'`n` di quel momento; **poi `mitosi()` fa crescere `n`**,
> e al passo dopo `len(csp) >= n` è **falso**. La guardia ricade su `cs_nodo = CS_M`.
> **Nell'80 % dei passi il `cs` locale non viene usato affatto.**

**E questo vale ANCHE per lo Strato 1**, che è sigillato 23/23 e usa la stessa funzione: il suo
`tau = d/cs` è in realtà **`d/CS_M`** nella grande maggioranza dei passi. Il ritardo esiste, ma la
sua **dipendenza da `cs`** — cioè la parte che porta la curvatura — **è quasi sempre inerte.**
Non è un difetto introdotto oggi: è **ereditato**, e non era stato notato.

## T5 — **PASS** sulla stabilità, ma con un numero da leggere

```
OFF  |omega| 8.137e+04   theta 4.662e+04 gradi/passo = 129.5 giri
ON   |omega| 2.737e+04   theta 1.568e+04 gradi/passo =  43.6 giri
fattore su theta: 0.3363    (atteso ~0.077)
|nb| max scostamento da 1: 2.220e-16    NaN/inf: 0
```

Nessun NaN, nessun runaway, `|nb| = 1` a `2.2e-16`. **Ma l'ampiezza cala di 3×, non di 13×** —
coerente con T3, e **43.6 giri per passo restano un settore massicciamente aliasato.**
**Non è una cura, e ora c'è anche il numero misurato a dirlo.**

---

## COSA C'È DA FARE, E CHE NON FACCIO ORA

1. **riscrivere T2** perché colpisca solo il rilassamento e non lo Strato 1;
2. **decidere sul reperto `_cs_nodo_prev`**: è una riga che rende quasi inerte la dipendenza da `cs`
   in **due** meccanismi, uno dei quali già sigillato. **È una questione a sé**, e va aperta con il
   suo criterio — non infilata qui;
3. **capire la metà mancante di T3** — con un criterio scritto prima, non con una spiegazione dopo.

**Nessuna di queste va fatta "al volo" dentro questo commit** (§2). Il flag resta **OFF**, il gate
**non ri-timbrato**, e il default del repo **invariato**.
