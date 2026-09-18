# REFERTO — **La mediana in `ritmo()` è ENTRAMBE: normalizzazione dimensionale *e* gauge del tempo. `Z9` non si cura da qui**

**Data:** 2026-09-18 · **Blob** `72acd6aa` (git) / `aa84755b` (byte) · un seme (5), 120 passi
**Task history scritto e pushato PRIMA:** `bb058c0` · **Strumento:** `csv/_test_fork/_mediana_ritmo.py`
**NESSUN CABLAGGIO.** Le quattro misure del §2, e lo STOP che il mandato ordina.

---

## 0. IL VERDETTO, in tre righe

1. **È ENTRAMBE** — la quarta lettura, quella che avevo aggiunto al mandato: la mediana rende `x`
   adimensionale **e** fissa l'unità del tempo locale. **Non è un'alternativa secca.**
2. **I consumatori usano `r` in VALORE ASSOLUTO**, quindi **cambiare la scala riscala tutti i tempi
   propri del sistema**: è **A4**, e **`Z9` non si cura da qui** senza scegliere un gauge nuovo.
3. **⚠ E c'è un difetto che nessuno aveva visto, indipendente dall'ancoraggio: `median(|f|) = 0`
   ESATTO in 4 invocazioni su 126 (3.2 %), anche a `n = 451`.** Lì `med` cade sul pavimento `1e-9`
   e **`r` diventa binario**: `√2` per i nodi non nulli, `1.414e-06` per gli altri.

---

## 1. (2.1) CHE COS'È `f`

`signed = Δangolo / DT` → **dimensione `1/T`** (una frequenza), **per nodo**. Due rami:

| ramo | sorgente | wrapping | `median(|f|)` mediana |
|---|---|---|---|
| **scalare 2π** | `angle(psi) − angle(_psi_prec)` | 2π | **3.04** |
| **spinoriale 4π** *(le campagne usano questo)* | `angle(psi_spin[:,0]) − …` | 4π | **0.0280** |

**La scala di `f` differisce di ~100× fra i due rami.**

> **⚠ E il primo giro della sonda aveva misurato il ramo SBAGLIATO: `CAMPO_SPINORIALE = False`,
> `126/126` invocazioni sul ramo scalare — una configurazione che nessuno gira.** Stessa classe di
> `doc/REPERTO_cs_dinamico_spento.md`: *«una misura senza quel flag non misura il sistema che si
> crede di misurare»*. **Rifatta sul ramo vero**, e i numeri qui sotto sono quelli.

## 2. (2.2) NORMALIZZAZIONE O GAUGE? — **tre prove indipendenti, e danno due risposte diverse**

**(a) DIMENSIONALE → normalizzazione.** `f` ha dimensione `1/T`, quindi `x = f/med` **richiede** la
divisione per essere un numero puro prima di `x/√(1+x²)`. **La divisione serve, e non è
eliminabile:** qualunque sostituto deve avere dimensione `1/T`.

**(b) STRUTTURALE → gauge.** Il ritorno è `1 + TAU_LOC·(r/r_unit − 1)`: **una deviazione da un
riferimento**, non un rapporto puro — il `1 +` non servirebbe a una normalizzazione dimensionale.
E il **docstring dice testualmente** *«ancorata alla mediana globale come **gauge**»* (`:2013`).
*(Un commento può essere stale: vale come indizio, non come prova — ed è per questo che ci sono
altre due prove.)*

**(c) DI CONSUMO → il gauge CONTA.** `r` non è mai usato come rapporto fra nodi:

```
dt_n = DT · r            (per nodo)      dt_e = DT · 0.5·(r[i] + r[j])    (per arco)
eta += dt_n              alpha = 1 − exp(−dt_n/tau)      delta_phivel = dt_n_s · (…)
```

**Sono tutti usi in VALORE ASSOLUTO**, e **nessuna soglia usa `r` direttamente** (verificato, grep
vuoto). **`alpha = 1 − exp(−dt_n/tau)` confronta `dt_n` con `tau = d/cs`: quel rapporto è fisico e
dipende dal gauge.**

> **RISPOSTA: è ENTRAMBE.** La mediana fa **contemporaneamente** due lavori — rende `x`
> adimensionale **e** fissa l'unità del tempo locale. **La domanda 2.2, come alternativa secca, era
> mal posta** — e l'avevo dichiarato **prima** di misurare, nel task history.

## 3. (2.3) CHI DIPENDE DA `median(r) = r(1)`

`dt_n` e `dt_e` alimentano: **`eta`** (la maturazione, cioè `Z9` stessa), **`alpha`** dello Strato 1
(`_bloch_ritardato`), **`delta_phivel`**, **`_rep`**, il **termostato** (`dt_scal = median(dt_n)`).

> **Cambiare `r_unit` riscala TUTTI i tempi propri locali del sistema.** Non è una correzione
> locale: è un cambio di unità di misura. **È A4 — ciò che definisce la struttura causale si giudica
> a parte.**

## 4. (2.4) `median(|f|)` EVOLVE? — **sul ramo vero, NO**

| | ramo **4π** *(campagne)* | ramo 2π |
|---|---|---|
| `median(|f|)` per **quarti** | **0.0254 → 0.0201 → 0.0228 → 0.0358** | 16.20 → 5.71 → 2.04 → 1.93 |
| variazione sui quarti | **×1.4 — quasi PIATTA** | ×8.4 |
| escursione min↔max (istantanea) | 2.06 ordini | 2.19 ordini |

**Sul ramo che le campagne usano, la scala di normalizzazione NON evolve: varia di `1.4×` in 120
passi.** È il caso che avevo scritto come peggiore: **«una costante mascherata da statistica»**.

*(L'escursione di 2.06 ordini è fra il minimo e il massimo **istantanei**, non un trend: è
dispersione fra passi, non evoluzione.)*

> **La terza lettura del mandato — «`median(|f|)` evolve → difetto parziale» — NON si applica al
> ramo vero.** Si applicava al ramo scalare, che nessuno gira.

## 5. ⚠ IL REPERTO CHE NON ERA NELLA LISTA — **il gauge è DEGENERE 1 passo su 31**

```
invocazioni con median(|f|) ESATTAMENTE ZERO : 4 su 126  (3.2 %)      [ramo 4π]
                                              14 su 126 (11.1 %)     [ramo 2π]
```

**Accade anche a `n = 451`**, cioè **più della metà dei nodi ha variazione di fase esattamente nulla
in quel passo.** Quando succede:

- `med = max(median(|f|), 1e-9)` → **cade sul pavimento `1e-9`**;
- `x = f/1e-9` → **esplode** per i nodi non nulli, `r` **satura a `√2`**;
- per i nodi con `f = 0`, `r = 1.414e-06`.

> **In quei passi `r` non è un tempo proprio graduato: è BINARIO.** E il pavimento `1e-9`, messo
> come protezione, **diventa il parametro fisico** — la stessa famiglia del pavimento `1e-6`
> sull'inerzia e del `0.05` su `_tau`.

**Questo è un difetto INDIPENDENTE dall'ancoraggio**, non l'avevo cercato, e **non è in nessuna voce
del registro.**

## 6. E CIÒ CHE RESTA LIBERO — **lo spread è grande, ma non cresce**

```
median(r) = 1.000000000        (pinnata per identità, C12)
dispersione p95−p05 : mediana 1.267    per quarti  1.216 → 1.267 → 1.260 → 1.302
IQR                 : mediana 0.684
```

**Su una mediana che vale `1.0`, una dispersione di `1.27` significa che `r` spazia su un intervallo
largo quanto il suo stesso valore centrale.** **La fisica del tempo proprio differenziale esiste ed
è grande** — ma **è PIATTA**: non cresce in 120 passi.

**Quindi: è il CENTRO a essere fisso, non la fisica.** L'ancoraggio toglie la possibilità che il
*nodo tipico* acceleri o rallenti **rispetto a sé stesso**, non la differenza **fra** nodi.

---

## 7. VERDETTO CONTRO LE QUATTRO LETTURE FISSATE PRIMA

| lettura | esito |
|---|---|
| normalizzazione + esiste scala di stato → **si cura** | **parziale**: è anche normalizzazione, e la scala sostitutiva deve avere dimensione `1/T` |
| **è il GAUGE (A4) → `Z9` non si cura da qui** | **SÌ**, per `2.2(c)` + `2.3`: i consumatori usano il valore assoluto |
| `median(|f|)` evolve → difetto parziale | **NO sul ramo vero** (×1.4 in 120 passi) |
| **⊕ è ENTRAMBE** *(la quarta, che avevo aggiunto)* | **È QUESTA** |

> **`Z9` NON si cura togliendo la mediana da `ritmo()`.** Toglierla senza sostituirla rompe
> l'adimensionalità; sostituirla **cambia il gauge del tempo**, cioè l'unità di misura di `eta`,
> `alpha`, `delta_phivel`, `_rep` e del termostato. **È A4, e va deciso come tale — non come una
> bonifica.**

**E se si volesse farlo lo stesso, il vincolo è preciso:** serve una scala **locale, derivata,
di dimensione `1/T`**. Un candidato **esiste già nel sistema** — **`cs/d`**, l'inverso del tempo-luce
del nodo, che è locale e derivato — **ma è un candidato, non una derivazione**, e sceglierlo
**significa scegliere un gauge nuovo**. **Non lo propongo: lo riporto.**

*(E la prova che l'architettura ammette un `r` senza mediana c'è già: il ramo `TEMPO_SEGNO` a
`:2027` ritorna `1 + (twn/deg)/PHI_CRIT` — **locale, normalizzato da una costante derivata, zero
statistiche dell'insieme**. Non è un rimpiazzo drop-in — è una **legge diversa** — ma è il pattern
di `cs_floor`/`Lam`.)*

## 8. I LIMITI

Un seme, 120 passi, una scena. **E il primo giro ha misurato il ramo sbagliato**: i numeri del ramo
2π restano in `csv/_test_fork/_mediana_ritmo_ramo2pi.txt` perché **il confronto fra i due rami è
esso stesso informativo** — ma **i numeri da citare sono quelli del 4π.**
