# MATURAZIONE e ALIASING — **RAPPORTO INTERMEDIO, RUN IN VOLO**

> **Scritto per Claude web** (regola `CLAUDE.md` §5-ter: a ogni riscontro, una relazione, subito).
> Branch `fork-su2`, 2026-09-15. Blob sul disco **`f5887254`**. **Nessuna modifica alla fisica.**
>
> ## ✔ RUN CONCLUSO — 2000 passi, exit 0
> **VERDETTO: ESITO (C).** L'aliasing è **strutturale, non transitorio**. Il dettaglio è nel §5-ter
> in fondo; i §§1-5 restano come furono scritti **durante** il run, perché la sequenza in cui i
> riscontri sono arrivati è essa stessa parte del risultato.

---

## 1. IL SIGILLO, PRIMA DELLA MISURA — PASS

`csv/_test_fork/_maturazione.py`, due run identici con e senza osservatore:

```
n senza osservatore = 1718   n con osservatore = 1718   ->  CONFRONTABILI
20 campi su 20 (pos phi phi0 phivel eta d d0 vd peq tw twp i j perc_chi perc_tw
                _nb _nb_ret _psi_spinor omega_s psi)   ->  max|A-B| = 0.000e+00
stato RNG                                               ->  identico
SIGILLO: PASS
```

## 2. I FLAG, CONFERMATI **IN-RUN** (lezione del falso O3c)

```
GAMMA_TURBO = 1        (NESSUN turbo)          STEP2_OROLOGIO = False
FORK_SU2 = True        FORK_SU2_MEM = True     CS_DINAMICO = True
TAU_A = 50   DT = 0.01  ->  maturazione piena a 5000 passi
```
Comportamento **naturale**, non forzato, come richiesto. Scena: 3 masse, `sep 8`, seme 1.

---

## 3. PRIMA METÀ DELLA PREDIZIONE: **CONFERMATA**

La predizione (`doc/PREDIZIONE_maturazione.md` §2) diceva che `theta` non sarebbe sceso subito,
perché l'inerzia è **bloccata sul pavimento `1e-6`**, e che la mediana della densità avrebbe
attraversato quel pavimento **«poco dopo il passo 150-300»**.

| passo | `ramp` med | `rho` med | % sotto il pavimento |
|---|---|---|---|
| 25 | 0.0039 | 1.5e-8 | **100 %** |
| 150 | 0.0201 | 2.6e-7 | 66.6 % |
| 225 | 0.0305 | 8.2e-7 | 53.3 % |
| **250** | 0.0349 | **1.12e-6** ← attraversa | 47.6 % |
| 350 | 0.0527 | 2.99e-6 | 27.4 % |
| 425 | 0.0657 | **5.07e-6** | **14.7 %** |

> **L'attraversamento è al passo ~245-250, dentro la finestra dichiarata prima del run.**
> `ramp` cresce lineare come previsto; `rho` è salita di **~5 ordini** e ora è **5× sopra** il
> pavimento, che è passato dal vincolare il 100 % dei nodi al 14.7 %.

## 4. SECONDA METÀ: **NON CONFERMATA (ancora)** — ed è il riscontro che conta

| passo | `rho` med | `theta` med (gradi/passo) | % aliasata |
|---|---|---|---|
| 250 | 1.12e-6 | 4.706e4 | 100 % |
| 275 | 1.53e-6 | 4.693e4 | 100 % |
| 350 | 2.99e-6 | 4.553e4 | 100 % |
| 400 | 4.18e-6 | 4.631e4 | 100 % |
| 425 | 5.07e-6 | **4.681e4** | **100 %** |

> **`rho` è cresciuta 4.5× oltre il pavimento, e `theta` NON è sceso: è piatto a ~4.6e4, e oscilla.**
> Se `theta` seguisse `1/inerzia` come la predizione §1 assume, sarebbe già a **~1.0e4**.
> **La frazione aliasata è ancora 100 %.**

### 4.1 Cosa ho sbagliato nella predizione — dichiarato

La catena del §1 (`omega ∝ ramp⁻⁴`) tratta `omega` **come se fosse istantaneamente uguale a
`coppia/inerzia`**. **Non lo è.** `omega_s` è una **memoria** con rilassamento (riga 1918), e il suo
tempo caratteristico è stato **già misurato**: `tau/DT ≈ 250 passi`
(`doc/ANALISI_gilbert_fdt.md` §3).

> **La predizione ha omesso il ritardo.** `theta` non può seguire `1/inerzia` istantaneamente:
> la insegue con **un ritardo di ~`tau` = 250 passi**. Dal ginocchio (passo 250) a ora (425) è
> passato **meno di un tempo di rilassamento**: siamo *dentro* il transitorio, non dopo.

**Quindi il dato attuale non falsifica ancora la predizione — ma non la conferma neppure**, e la
predizione com'era scritta era **incompleta**. Lo scrivo adesso, non a posteriori.

### 4.2 La previsione corretta, scritta ORA (prima di vederla)

> Se `theta` insegue `1/rho` con ritardo `tau ≈ 250` passi, **la discesa deve diventare visibile a
> partire dal passo ~500-600**, e da lì seguire `theta ∝ n⁻⁴`.
> **Se al passo 800 `theta` è ancora a 4.6e4, la lettura `omega ∝ 1/inerzia` è sbagliata**, non solo
> ritardata — e sarebbe l'esito **(C)**.

---

## 5. UNA PROIEZIONE SCOMODA, DA DIRE ORA

Con `rho ∝ ramp⁴ ∝ n⁴` e `theta ∝ 1/rho`, dal punto attuale (`theta = 4.68e4` al passo 425) la
soglia di aliasing (30 gradi/passo) verrebbe attraversata a

```
n = 425 · (4.68e4 / 30)^(1/4) ≈ 425 · 6.27 ≈ 2660 passi
```

> **Oltre i 2000 passi del run in corso.** E al passo 2000 `ramp` mediano sarà solo **~0.31**:
> **non ci sarà alcuna popolazione "matura" (`ramp > 0.9`)**, quindi la **seconda misura** prevista
> dal mandato (`chi` nella zona matura) **non sarà eseguibile su questo run**.

Due strade, **decisione di Luca**, che riporto ora invece che fra due ore:
1. **prolungare** a ~3000 passi (costo: altre ~2-3 h oltre le attuali);
2. **fermarsi a 2000** e riportare la **pendenza** misurata di `theta(n)`, dichiarando
   l'attraversamento come **estrapolazione** e non come misura.

---

## 5-bis. ⚑ AGGIORNAMENTO AL PASSO 1200 — **IL CRITERIO DI FALSIFICAZIONE È SCATTATO**

Avevo scritto, **prima di vederlo** (§4.2): *«se al passo 800 `theta` è ancora a 4.6e4, la lettura
`omega ∝ 1/inerzia` è sbagliata, non solo ritardata — esito (C)»*. **È così.**

| passo | `rho` med | `theta` misurato | `theta` atteso se ∝ 1/`rho` | scarto |
|---|---|---|---|---|
| 425 | 5.07e-6 | 4.681e4 | (riferimento) | — |
| **800** | 2.95e-5 | **4.815e4** | 8045 | **×6.0** |
| 1100 | 6.82e-5 | 4.724e4 | 3480 | **×13.6** |

### La pendenza — la domanda vera, e la sua risposta

Regressione su **14 campioni**, **solo dopo il rilascio del pavimento** (passi 425-1200):

```
d(log theta)/d(log n)    = -0.020        ATTESA dalla lettura:  -4
d(log theta)/d(log rho)  = -0.006        ATTESA dalla lettura:  -1
leva:  n x2.82    rho x16.9    theta x0.977
```

> **Entrambe le pendenze sono ZERO.** Con `rho` cresciuta di **quasi 17 volte**, `theta` è variato
> del **−2 %**. Non è un ritardo: è **assenza di dipendenza**.

> ### VERDETTO INDICATO: **ESITO (C)** — l'aliasing è **STRUTTURALE, non transitorio**.
> La maturazione **funziona** (`ramp` lineare, `rho` +5 ordini, pavimento rilasciato dal 100 % al
> 3.2 %) **ma non tocca `theta`.** E lo si sa **al passo 1200, non a 20 000** — che era lo scopo di
> misurare la pendenza invece di aspettare la soglia.

### Il meccanismo candidato — **ipotesi, non ancora misurata in questo run**

Riga **1913**:
```python
_tau = TAU_A * np.maximum(_dens / _dens_rif, 0.05)
_dens_rif = median(_dens[_dens > 1e-6])
```

- **Prima** della maturazione quasi tutti i nodi hanno `dens < 1e-6`, quindi `dens/dens_rif` è
  minuscolo e **scatta il pavimento `0.05`**: `tau = TAU_A·0.05 = 2.5`, cioè **`tau/DT = 250` passi**
  — il valore già misurato in `doc/ANALISI_gilbert_fdt.md` §3.
- **Dopo**, con quasi tutti i nodi sopra `1e-6`, per il nodo mediano `dens/dens_rif ≈ 1`, quindi
  `tau = TAU_A = 50`, cioè **`tau/DT = 5000` passi**.

> **La memoria si è allungata di ~20× ESATTAMENTE mentre il sistema maturava.** La maturazione
> abbassa il bersaglio (`|F| ∝ 1/inerzia`) **e insieme allunga l'inseguimento** (`tau ∝ rho`), e
> sull'orizzonte del run vince l'inseguimento.
>
> Con `omega_eq = |F|·√(dt·tau/2)`, se `|F| ∝ 1/rho` **e** `tau ∝ rho`, allora
> **`omega_eq ∝ rho^(−1/2)`**, non `rho^(−1)` — e anche quella discesa arriverebbe su **5000 passi**.

**È un'ipotesi, e va marcata come tale:** `_maturazione.py` **non stampa `tau`**, quindi in questo
run non l'ho misurata. Si verifica a costo quasi nullo aggiungendo la colonna, **dopo**, senza
toccare la fisica.

---

## 5-ter. ⚑ VERDETTO FINALE — **ESITO (C)**, run concluso a 2000 passi

```
theta mediano:   0.01433 -> 3.243e+04 gradi/passo
frazione aliasata (theta > 30 gradi/passo):   6.7% -> 100.0%
ramp mediano:    0.0002 -> 0.2585        rho mediano: 1.76e-11 -> 5.5e-4
-> theta NON e' sceso sotto soglia: esito (C), aliasing STRUTTURALE.
```

**La frazione aliasata è 100 % a OGNI campione, compreso l'ultimo.** Non c'è stato nessun momento,
in 2000 passi, in cui anche un solo nodo sia uscito dall'aliasing.

### 5-ter.1 `theta` scende — ma di un fattore sbagliato di due ordini

Onestà: `theta` **non è piatto fino in fondo**. Ha un picco a **4.978e4** (passo 600) e poi cala a
**3.243e4** (passo 2000): **−35 %**. Ma la domanda non era «cala?», era «**cala come previsto?**».

| finestra | leva su `rho` | `d(log θ)/d(log ρ)` | atteso |
|---|---|---|---|
| tutto post-pavimento (22 campioni) | **×309** | **−0.061** | −1, o −0.5 nella lettura raffinata |
| prima metà (425-1200) | ×36.7 | −0.006 | idem |
| ultima parte (1300-2000) | ×8.7 | −0.131 | idem |

E il confronto diretto, dal picco di `theta` alla fine, con `rho` cresciuta **×43.3**:

| | `theta` |
|---|---|
| se `theta ∝ 1/rho` (lettura originale) | **1149** |
| se `theta ∝ rho^(−1/2)` (lettura raffinata) | **7564** |
| **MISURATO** | **3.243e4** |

> **28× sopra la previsione originale, 4.3× sopra la raffinata.** La pendenza misurata su `rho`,
> **−0.061 con una leva di ×309**, cade nella banda **−0.2…+0.2** del criterio.
> **Il criterio temporale posto da Luca è soddisfatto: la lettura è sbagliata, non ritardata.**

### 5-ter.2 Il limite dichiarato prima si è avverato

`ramp` mediano a 2000 passi: **0.2585** — esattamente la proiezione (~0.31) fatta al passo 425.
**Nessuna popolazione matura**: la colonna `ramp > 0.5` compare solo agli ultimi due campioni.
La **seconda misura** prevista dal mandato (`chi` nella zona matura) **non era eseguibile**, come
avevo detto in anticipo.

### 5-ter.3 E un indizio trasversale che punta **dalla parte sbagliata**

Agli ultimi due campioni, alla **stessa istantanea**:

| | `theta` mediano |
|---|---|
| nodi **giovani** (`ramp < 0.1`) | 3.485e4 |
| nodi **maturi** (`ramp > 0.5`) | **4.088e4** |

> **I nodi maturi ruotano PIÙ VELOCEMENTE dei giovani.** Se `omega = coppia/inerzia` e l'inerzia
> cresce con la maturità, dovrebbe essere il contrario.
>
> **È un confronto a un solo istante, quindi il ritardo non può spiegarlo.** Ma è grezzo (due sole
> classi, campione piccolo sui maturi), quindi lo riporto come **indizio**, non come misura: il test
> vero è la **regressione trasversale** del `doc/CRITERIO_omega_rho.md` §4.1, in corso.

---

## 6. COSTO, MISURATO

425 passi in **9.0 minuti** = ~1.3 s/passo a `N ≈ 4100`. `N` cresce di ~10 nodi/passo e il costo con
lui (`chiralita_core_locale` è un ciclo Python su tutti i nodi). Stima per i 2000 passi: **2-3 ore**.

## 7. COSA NON È STATO TOCCATO

`soliton_simulator.py` **non modificato**: blob `f5887254`, `git status` pulito. Nessun cablaggio,
nessun tetto su `omega`, nessun sottopasso, **`TAU_A` e il regime intatti** — sono la scala di
maturazione che si sta misurando.
