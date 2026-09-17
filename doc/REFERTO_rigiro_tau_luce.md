# REFERTO — **rigiro del sigillo `--tau-luce` sul blob attuale.** T4 si ribalta, T1 è scaduto, **e T3 fallisce per una ragione DIVERSA**

**Blob:** `69ee5403` (byte grezzi `ee0c2a60`), HEAD `b6c83c3`. **Nessun codice toccato, nessun flag
acceso.** Unico run autorizzato dal mandato. Output integrale:
`csv/_seal_fork/_sigillo_tau_luce_RIGIRO_2026-09-17.txt`.

---

## 1. I DUE VERDETTI AFFIANCATI

| | **allora** (`7d484580`, 15 set) | **oggi** (`69ee5403`, 17 set) | |
|---|---|---|---|
| **T1** byte-identità a flag OFF | **PASS** | **FAIL** | ⚠ **criterio SCADUTO**, vedi §2 |
| **T2** riduzione al limite | **FAIL** (`n` 1718 vs 1647) | **FAIL** (`n` 1682 vs 1680) | **stessa ragione**, come previsto |
| **T3** pendenza | **FAIL** (OFF −0.1685, ON −0.4265) | **FAIL** (OFF **−1.7311**, ON **−1.2749**) | ⚠ **RAGIONE DIVERSA: il segno si è INVERTITO** |
| **T4** covarianza | **FAIL** (`cs→2cs` dava `1.000000`) | **PASS** (`cs→2cs` dà **`0.500000`**) | ✅ **ribaltato** |
| **T5** stabilità | PASS | PASS | |

**ESITO COMPLESSIVO: ancora FAIL** — ma **nessuno dei tre FAIL è più quello di allora.**

---

## 2. T1 — **il criterio è SCADUTO, e non è una regressione**

```
n_A = 1718   n_B = 1682   ->  NON CONFRONTABILI
```

**T1 confronta il codice attuale, a flag OFF, col file `_old_sim_pre_tauluce.py`.** Verificato dal
disco: quel file è il blob **`f5887254`**, cioè **`f7051c3~1`** — **quindici commit fa.**

> **Le differenze che T1 rileva sono le SETTE CORREZIONI DI LEGGE SIGILLATE** — `cs_floor`
> relazionale, la cura della cache, `d_arco`, la plasticità causale, l'inerzia dimensionale, ecc.
> **T1 sta misurando che la bonifica è avvenuta.**

**NON è una regressione della byte-identità a flag OFF**, ed è importante non leggerlo così. È un
criterio che **confronta con un riferimento che non è più il riferimento giusto**: la sua domanda
(*«l'estrazione di `_tempo_luce_nodo` ha cambiato qualcosa?»*) **ha già avuto risposta allora**, e
oggi la stessa misura risponde a una domanda diversa.

**Non ho riscritto il criterio**, come il mandato ordina: **lo dichiaro scaduto.**

---

## 3. T2 — **FAIL per la stessa ragione, e la marcatura lo aveva previsto**

```
allora :  n_A = 1718   n_B = 1647    (differenza 71)
oggi   :  n_A = 1682   n_B = 1680    (differenza  2)
```

Il monkeypatch colpisce il metodo **condiviso** `_tempo_luce_nodo`, quindi cambia **anche** lo
Strato 1: due meccanismi insieme, traiettoria diversa, nessun confronto. **È un difetto del TEST, e
il rigiro non poteva cambiarlo** — l'avevo scritto nella marcatura (`b6c83c3`) **prima** di girarlo.

**La differenza si è ridotta da 71 a 2 nodi.** *(Non ne traggo nulla: con `N` diverso non c'è
confronto, e leggere «quasi identici» da una differenza piccola sarebbe la stessa trappola dello
zero senza shape.)*

---

## 4. ⚠ T3 — **FAIL per una RAGIONE DIVERSA: l'effetto ha CAMBIATO SEGNO**

| | pendenza OFF | pendenza ON | effetto di `--tau-luce` |
|---|---|---|---|
| **allora** | −0.1685 | −0.4265 | **ON si ALLONTANA da zero di 0.258** |
| **oggi** | **−1.7311 ± 0.0197** | **−1.2749 ± 0.0155** | **ON si AVVICINA a zero di 0.456** |

> **Allora `--tau-luce` rendeva la pendenza più ripida. Oggi la rende più piatta.**
> **Non è "lo stesso FAIL con numeri diversi": è l'effetto che ha cambiato verso.**

E le barre escludono il caso: gli `IC95` sono `[−1.7696, −1.6925]` e `[−1.3052, −1.2445]`, **disgiunti**.

**E c'è dell'altro che va detto insieme:** anche il braccio **OFF** si è spostato, da **−0.1685** a
**−1.7311** — **dieci volte**. Non è `--tau-luce` ad averlo fatto: è la **bonifica**, e in
particolare l'inerzia dimensionale, che entra proprio nella grandezza contro cui la pendenza è
misurata. **Quindi i due esperimenti non misurano la stessa cosa**, e confrontare i quattro numeri
come se fossero commensurabili sarebbe un errore.

**Il mandato fissa la lettura PRIMA, ed è questa:** *«fallisce per una ragione DIVERSA → **è un
reperto nuovo. Riporta e fermati.**»* **È quello che questo referto fa.**

---

## 5. ✅ T4 — **si ribalta, ed era la previsione della marcatura**

```
allora :  cs -> 2cs : 1.000000   (atteso 0.500000)   <- NON SEGUE
oggi   :  cs -> 2cs : 0.500000   (atteso 0.500000)   <- ESATTO
           d  -> 2d : 2.000000   (atteso 2.000000)   <- ESATTO, come allora
```

**Il FAIL di T4 era l'artefatto di un difetto poi CURATO:** `_cs_nodo_prev` veniva scartata a ogni
mitosi (**80 % dei passi con `cs = CS_M`**), e la cura **C7** (commit `43e9a47`) ha portato il
fallback da **71.88 %** a **0.00 %**.

> **`tau = d/cs` segue ORA lo stato da solo, su entrambe le grandezze, in modo esatto: è una LEGGE,
> non un numero travestito.** **Questo il sigillo di allora non poteva dirlo, e ora lo dice.**

**È la conferma diretta della tesi del mandato** — *«un sigillo preso su un sistema cambiato quattordici
volte non è un ostacolo: è una voce da rigirare»* — **su uno dei tre punti. Non su tutti e tre.**

---

## 6. COSA NE È DELL'OSTACOLO A `TAU_A`

**Il quadro è a tre colori, e nessuno dei tre è quello che il mandato si aspettava:**

- **T4 dice che l'ostacolo era in parte un artefatto** — e su quel punto il mandato aveva ragione;
- **T2 dice che una parte dell'ostacolo NON era un artefatto**: è un test scritto male, e lo è
  ancora. **Finché T2 non è riscritto, `--tau-luce` non ha una riduzione al limite** — cioè manca
  proprio il sigillo che dimostra che il flag *sostituisce* una legge invece di *aggiungerne* una;
- **T3 apre un fronte nuovo**: l'effetto ha cambiato segno, e **non so perché**. **Non invento una
  spiegazione** — è il punto in cui, per tre volte in una notte, ne sono state generate tre sbagliate.

> **Quindi: l'ostacolo a `TAU_A` NON cade, ma non regge più per le ragioni di allora.**
> **E resta fermo il punto che il blocco aveva sollevato per primo, che nessun rigiro tocca:**
> **`TAU_A = LAM/cs` non elimina il numero scelto — lo sposta su `LAM`.** Su quello il mandato
> stesso ha accolto il blocco.

---

## 7. E T5, che va letto con cautela

```
allora :  OFF theta 4.662e+04 gradi/passo = 129.5 giri     ON 1.568e+04 = 43.6 giri
oggi   :  OFF theta      64.51 gradi/passo =  0.18 giri     ON      2.02 =  0.01 giri
```

**Riporto i numeri perché sono l'output del sigillo autorizzato, e NON ne traggo un verdetto di
fisica.** Il mandato della bonifica dice che `theta` **si guarda a bonifica finita, contro una
predizione scritta prima** — e quelle predizioni sono committate (`9c9cc43`, `3c82177`). **Questo è
un braccio di sigillo su una scena di test, non una campagna**: leggerlo come «l'aliasing è
risolto» sarebbe esattamente il salto che i mandati vietano.
