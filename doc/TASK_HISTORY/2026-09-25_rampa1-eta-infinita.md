# `RAMPA-1` — IL VUOTO DATO HA ETÀ INFINITA (strada (3), decisione di Luca)

*(committato **PRIMA** del codice, par.5-septies. La decisione e i criteri sono di Luca; qui c'è
ciò che ho verificato prima di scrivere, e cosa mi fermerebbe.)*

## ① RAGIONAMENTO PRELIMINARE — *cosa so prima di toccare una riga*

**IL DIFETTO, misurato:** `ramp = min(1, eta/_tempo_rampa())` è un rapporto fra **due quantità
che si muovono entrambe**. La cura 4 scriveva `eta = _tempo_rampa()` alla semina, che dà
`ramp = 1` **esatto in quell'istante**; un passo dopo, in configurazione del driver, il
denominatore è cresciuto **×1.196** contro **×1.011** del numeratore e la rampa è caduta a
`0.846` (mediana), con `_g_rampa_cali = 4198` e solo **54 nodi su 4252** ancora a `1`.

**LA DECISIONE DI LUCA — strada (3):** i nodi della semina iniziale (`maturi=True`) ricevono
**`eta = +inf`**. Allora `ramp = min(1, inf/tr) = 1` **per sempre, qualunque `cs`**.

> **Perché è la strada giusta e non un trucco:** *«maturo»* non è un valore di `eta`, è una
> **proprietà**: il vuoto **c'era già**. `+inf` è l'unico modo di dirlo **senza un numero e
> senza un array**: non è una soglia grande, è *«nessun tempo di accensione»*.
> **E TOGLIE codice invece di aggiungerlo** (`STANDARD 10`): sparisce la chiamata a
> `_tempo_rampa()` alla semina **e le sue due diramazioni** (array / scalare).

**COSA NON SO, e lo verifico PRIMA:** `+inf` non è un numero grande, è un **valore speciale**.
Ogni **riduzione** su `eta` (`mean`, `sum`, `std`) diventa `inf`; `inf/inf = nan`.

## ② LA VERIFICA, FATTA PRIMA — `csv/_letture_eta.py`, per AST

```
occorrenze di `eta` nel simulatore   17   (11 letture, 6 scritture)
righe attese dal guardiano           [3419, 3684, 4976]     tutte TROVATE
trovate e NON attese                 [1605, 2720, 2723, 2747, 2752, 6022, 6178, 9332]
```

**IL GUARDIANO AVEVA RAGIONE SULLA FISICA:** `:3419` *(il torque pesato)* e `:3684` *(`_pesi`)*
sono **le uniche due letture che USANO `eta` in una legge**, e `:4976` l'unico incremento. Le
altre otto sono **l'inizializzazione** (`:1605`), la **crescita degli array** alla mitosi e allo
Schwinger (`:2720`, `:2723`, `:6022`, `:6178`), **la scrittura della cura 4** (`:2747`, `:2752`
— il sito da cambiare) e **una STATISTICA DIAGNOSTICA** (`:9332`).

**⚠ E `:9332` È UNA RIDUZIONE che il mio euristico NON ha classificato** *(cerca `mean(`,
`sum(`… e lì c'è `_stat(`)*: `cols['eta_min'], cols['eta_max'], cols['eta_mean'] = _stat(net.eta)`.
**Con `eta = inf` quella colonna del CSV diventa `inf`** — e un CSV è il dato (`P6`), non un log.
**Va adattata e dichiarata**, non lasciata stampare `inf`.
*(Il limite del mio strumento — «la riduzione si cerca sulla stessa riga» — si è manifestato
subito, ed è per questo che era dichiarato prima di leggerlo.)*

**NEGLI STRUMENTI:** `287` occorrenze, `14` con una riduzione sulla stessa riga. **Non rompono
la fisica: rompono i REFERTI**, e un referto che stampa `inf` è un verdetto vacuo.

## ③ PROGETTAZIONE — cosa cambio, e cosa DECIDE ciascun passo

| passo | cosa | **cosa decide** |
|---|---|---|
| **1** | `:2743-2752` → `self.eta[_a:_b] = np.inf`, via le due diramazioni | che la maturità sia **irreversibile per costruzione**, non per un valore |
| **2** | `:9332` → statistiche sui soli `eta` **finiti**, più una colonna `eta_inf` col **conto** degli infiniti | che il CSV resti **un dato** invece di una colonna di `inf` |
| **3** | il sigillo `CURA 4` prende un braccio **`lungo`**: 120 passi **dal CLI**, e misura `ramp` sui nodi della semina **a ogni passo** | i criteri di Luca |

**I CRITERI, come Luca li ha dati** *(e si scrivono qui, prima dei numeri)*:
`A2` dal CLI → **`ramp == 1` su tutti i nodi della semina a OGNI passo per 120 passi**;
**`_g_rampa_cali` sui soli nodi della semina == 0**; **un nato da mitosi parte da `0`**;
**flag spento byte-identico**.

**I cali si contano NEL SIGILLO, non nel simulatore:** `_g_rampa_cali` è **globale** e i nati in
dinamica **devono** salire da `0`, quindi un contatore globale non risponde alla domanda.
**Aggiungere un contatore per-sottoinsieme sarebbe una legge in più** (`STANDARD 10`): il sigillo
ha già gli indici della semina, e se li tiene.

**COSA MI FERMEREBBE:** se `A1` (flag spento byte-identico) cade → **STOP**, la cura non è
inerte a flag spento; se una riduzione su `eta` che non ho visto stampa `inf` in un referto → si
**dichiara** in quel referto invece di correggerlo di nascosto.

## ④ TODO DEL NEXT STEP

- [ ] la cura (2 siti) + il sigillo con il braccio `lungo`, rigirato **dal CLI**
- [ ] **`RAMPA-2` in coda** *(richiesta di Luca)*: al passo 0 `_cs_nodo_prev` **non esiste** e il
      tempo-luce usa `cs = CS_M` **ovunque**. Elencare **per AST** quali altre leggi usano il
      tempo-luce o `cs` al passo 1 — **stessa famiglia di `B1`** (*«il passo 1 senza tempo
      proprio»*)
- [ ] poi `P3`/`P5` anticipati dai presidi, e le cinque rimisure in configurazione del driver
