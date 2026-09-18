# REFERTO — **Non è «metà», non è la chiralità: è il TRANSITORIO DI NASCITA. E `Z43` non ne è un sintomo**

**Data:** 2026-09-18 · **Blob `a1ae5090` INVARIATO** *(nessuna cura, strumentazione inerte)*
1 seme (5), 120 passi · **Task history pushato PRIMA:** `0d9abac` · **Sonda:** `_chi_non_ruota.py`
*(committata prima di girarla)* · **Output:** `csv/_test_fork/_chi_non_ruota.txt`

---

## 0. IL VERDETTO CONTRO LE SEI LETTURE FISSATE PRIMA

| lettura | esito |
|---|---|
| **⑤b** — i nodi fermi hanno tutti lo stesso segno | **NO — MISTO. L'ipotesi CADE**, e cade sui due soli passi che hanno potenza statistica |
| **④** — `ramp ≈ 0` sui fermi | **✓ REGGE** — `ramp` fino a **66 volte** sotto la popolazione |
| **③** — `\|psi\| ≈ 0`, `f = 0` è convenzione di numpy | **✓ REGGE, nella forma più forte: è ZERO ESATTO** |
| **②** — evolve ma `angle` non lo vede | **NO** — `\|Δψ\| = 0.0000e+00`. *Ma non è un'ipotesi concorrente: è lo STESSO fatto di ③* |
| **①** — sempre gli stessi nodi | **NO** — Jaccard ≈ **0**: **non è congelamento, è un TRANSITORIO DI NASCITA** |
| nessuna regge | **non è il caso: ne reggono due, e sono lo stesso fatto a due livelli** |

> **⚠ E DUE PREMESSE DEL MANDATO CADONO PRIMA ANCORA DELLE LETTURE.**

---

## 1. ⚠ «METÀ DEI NODI» NON ESISTE — **misurato, non dedotto**

Il §0 diceva *«in quei passi metà dei nodi ha `f = 0`»*, come **aritmetica** della mediana. **La
frazione VERA:**

```
passi con almeno un nodo a f = 0 : 13 su 124
frazione mediana sui passi degeneri : 0.004357     <- lo 0.4 %, cioe' UNO o DUE nodi su ~450

passo 0     n 80    nodi a f=0 80    frazione 1.000000   <- non esiste un prima
passo 5     n 440   nodi a f=0 414   frazione 0.940909   <- dopo l'iniezione di 360 nodi senza genitore
passo 12    n 442   nodi a f=0 2     frazione 0.004525
passo 16    n 443   nodi a f=0 1     frazione 0.002257
…  (altri 9 passi, sempre 1 o 2 nodi)
```

> **Non c'è nessun regime «a metà».** Ci sono **due passi di NASCITA** (100 % e 94 %) e **undici
> passi con UNO o DUE nodi** su ~450. **Sono due fenomeni diversi, e nessuno dei due è «metà».**

## 2. ⑤a — **l'universo è BILANCIATO, e il bilanciamento NON viene dalla Schwinger**

```
ramo                          chiamate   nodi aggiunti
semina/nuova_massa (:1850)    4          440      <- rng.choice([-1,1]) : 50/50 A CASO
mitosi UGUALE (:3945)         126        19       <- CONSERVA il segno
Schwinger OPPOSTO (:4066)     5          6        <- lo ROVESCIA

frazione +1 : primo 0.4375 (n=80) -> 0.5066 -> 0.5066 -> 0.5054 (n=459)
              min 0.4375   mediana 0.5056   max 0.5078
```

**NON è un universo di sola materia: è bilanciato a metà, entro lo 0.8 %.**
**E il ramo Schwinger GIRA davvero** — 5 volte, 6 nodi — **ma è l'1.3 % della popolazione.**

> **Il bilanciamento viene da `rng.choice([-1, 1])` alla nascita, che fa il 94.6 % dei nodi**, non
> dalla mitosi antichirale, **che ne fa l'1.3 %.** *(Era la correzione scritta nel task history
> PRIMA di misurare: il mandato attribuiva il bilanciamento alla Schwinger.)*

## 3. ⑤b — **MISTO. L'ipotesi materia/antimateria CADE**

```
passo  n fermi  frazione +1   NULLO (popolazione)   scarto
0      80       0.437500      0.437500              +0.000000   <- TAUTOLOGIA: i fermi SONO la popolazione
5      414      0.519324      0.506818              +0.012505
16     1        0.000000      0.505643              -0.505643
18     1        1.000000      0.506757              +0.493243
24     1        1.000000      0.507761              +0.492239
…
```

**⚠ I DUE SOLI PASSI CON POTENZA STATISTICA DICONO NO:**
**passo 0 → scarto `+0.000000` ESATTO** *(e non poteva che esserlo: tutti i nodi sono fermi, quindi
la popolazione dei fermi **è** la popolazione — il nullo ha intercettato la tautologia)*;
**passo 5 → scarto `+0.0125` su 414 nodi**, cioè **nulla**.

**Gli altri undici passi hanno UNO o DUE nodi.** Con `n = 1` la frazione **deve** valere `0` o `1`:
**gli scarti `±0.49` sono aritmetica, non segnale.** E sono **bilanciati**: sui sei passi a `n = 1`,
**tre `+1` e tre `−1`.**

> **Non c'è nessuna chiralità che non ruota. L'indizio numerico era una coincidenza, ed è escluso.**

**⚠ E il canale esiste davvero — l'avevo mancato nel task history e l'ho dichiarato prima di
misurare:** `CALORE_VETTORIALE = True` (`:270`) e `scuoti_vuoto` (`:538-540`) fa
`phivel[:n] += rng.normal(0,1)*ampiezza * perc_chi` **a ogni passo**. **Ma è un SEGNO su un rumore
SIMMETRICO:** la distribuzione marginale di un nodo `+1` e di uno `−1` è **identica**, e può agire
**solo** attraverso le correlazioni. **La misura conferma che sul singolo nodo non agisce.**

*(Verificati e spenti: `OROLOGIO_SEGNO`, `TEMPO_SEGNO`, `CHI_BASC`, `CHI_DA_SPINORE`, `COMPAT_CHI`,
`SPIN_POSITIVI`. Accesi: `CALORE_VETTORIALE`, `CHI_CORE`, `TORS_4PI`.)*

## 4. ③ — **`|psi_spin| = 0` ESATTO. `f = 0` NON È FISICA**

```
                    fermi mediana   fermi MAX     | tutti mediana   tutti p05
passo 12            0.0000e+00      0.0000e+00    | 3.2769e-05      5.9306e-06
passo 69            0.0000e+00      0.0000e+00    | 4.2703e-03      1.7527e-04
passo 117           0.0000e+00      0.0000e+00    | 1.2539e-02      4.7027e-04
```

**In 12 passi su 13 il modulo dello spinore dei nodi fermi è `0.0000e+00` — ESATTAMENTE zero, anche
nel MASSIMO.** *(L'unica eccezione è il passo 32: `1.1e-06`, comunque **600 volte** sotto la mediana
della popolazione.)*

> **`angle(0)` restituisce `0` per convenzione di numpy. Quindi `f = 0` non dice «il tempo è fermo»:
> dice «la fase non è definita».** **Non è una misura: è un valore di ritorno.**

## 5. ④ — **`ramp` fino a 66 volte sotto la popolazione: il collegamento con `Z9` REGGE**

```
passo    eta fermi     ramp fermi     | eta tutti    ramp tutti     rapporto eta
12       0.004967      9.93e-05       | 0.055854     0.001117       11
32       0.027918      5.58e-04       | 0.228605     0.004572       8
117      0.014125      2.83e-04       | 0.931708     0.018634       66
```

**I nodi fermi sono nodi IMMATURI**, e lo scarto **cresce col tempo** (11 → 66): la popolazione
matura, loro **sono appena nati**.

## 6. ① e ② — **non è congelamento: è un TRANSITORIO DI NASCITA**

```
Jaccard fra passi degeneri consecutivi: 0.1227, 0, 0, 0, 0, 0, 0, 0.3333, 0, 0, 0, 0
|delta psi_spin| dei fermi: 0.0000e+00 in 12 passi su 13
```

**Gli indici NON si ripetono.** **Non sono nodi congelati per sempre: sono ogni volta nodi DIVERSI,
appena nati.** E `|Δψ| = 0` **non è un'ipotesi concorrente a ③: è la sua conseguenza** — se
`psi_spin` vale zero adesso e valeva zero prima, la differenza è zero. **Lo stesso fatto.**

---

## 7. LA CATENA, e si chiude tutta

```
nodo APPENA NATO  ->  eta ~ 0  ->  ramp ~ 0  ->  pesi del kernel ~ 0  ->  psi_spin = 0 ESATTO
                  ->  angle(0) = 0  (CONVENZIONE numpy)  ->  f = 0  ->  gauge degenere (Z33)
```

**③ e ④ reggono INSIEME, ed è quello che avevo previsto nel task history:** sono **lo stesso fatto a
due livelli**, non due spiegazioni in competizione.

**E i tre regimi si spiegano tutti con la stessa catena:**
- **passo 0** — non esiste un prima: **tutti** i nodi;
- **passo 5** — `nuova_massa` ha appena iniettato **360 nodi senza genitore**: il **94 %**;
- **gli altri 11 passi** — **uno o due nodi appena nati** dalla mitosi.

---

## 8. ⚠ MA `Z43` NON È UN SINTOMO DI `Z9`, e va detto

La lettura ④ del mandato dice: *«`Z33`/`Z43` sono sintomi di `Z9`»`*. **Per `Z33` è vero. Per `Z43`
NO, e si vede dai numeri già in archivio:**

**`Z43` è l'oscillazione del gauge del `62 %` fra passi. Ma i passi degeneri sono `13 su 124`, e
solo `2` hanno `median(|f|) = 0`.** Il rapporto `med_t/med_{t-1}` misurato in `631ff15` ha
**`p05 0.482` e `p95 2.097`** — **percentili su 123 passi, che 2 valori estremi non possono
spostare** — e **l'11.4 % dei passi sta fuori da `[0.5, 2]`.**

> **Curare `Z9` toglierebbe i 13 passi degeneri, NON l'oscillazione del gauge negli altri 111.**
> **`Z33` risale a `Z9`. `Z43` no: resta una domanda sulla DEFINIZIONE DEL TEMPO.**

*(Limite dichiarato: non ho ricalcolato quei percentili escludendo esplicitamente i passi degeneri.
L'argomento è di robustezza — `p05`/`p95` su 123 valori — non una misura dedicata.)*

## 9. COSA NON HO FATTO

**Nessuna cura, nessun cablaggio, nessuna promozione, nessun cambio di default. Blob `a1ae5090`
invariato.** Non toccati: il gauge, il `+1e-6`, il `max(...,1e-9)`, la regolarizzazione di `Z42`.
**`perc_chi` non dedotto dai nomi: i tre rami sono CONTATI** (A8).

## 10. I LIMITI

Un seme, 120 passi, una scena. **Undici dei tredici passi degeneri hanno 1-2 nodi: su quelli
nessuna statistica è possibile, ed è esattamente ciò che il nullo di ⑤b ha reso visibile.** Il
confronto dei nodi fermi è fatto **nello stesso istante e sulla stessa popolazione** (A3c). **La
frazione `0.4 %` è di questa scena**, e dipende dal tasso di mitosi.
