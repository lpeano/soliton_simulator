# TASK HISTORY — **una direzione non è una forza: rimoltiplicare per `rho_spin`**

**Data** 2026-09-19 · **branch** `fork-su2` · **HEAD** `d22ac56` · **blob** `1a5e0796` · albero
**pulito**.

> **⚠ ORDINE REALE, dichiarato:** le due letture del §1 **venivano dal mandato**, quindi erano
> fissate prima **per costruzione**. **Ma la verifica (lettura del codice) è avvenuta PRIMA che
> scrivessi questo documento**, e lo dico invece di ricostruire un ordine che non c'è stato. *(È
> la seconda volta oggi: vale la pena notarlo.)*

---

## 1. LA VERIFICA — **l'ampiezza è ASSENTE dal numeratore. Via libera.**

**La domanda era: `rho_spin` è già altrove nella catena che porta a `omega_s`?**

### I consumatori di `_nb_grav()` sono DUE, e sono diversi

```
:2453   _tq = np.cross(self._nb_grav(), nb)              <- IL TERMINE DI COPPIA
:4383   _nbg = self._nb_grav()
:4384   prod_interno = np.sum(_nbg[ii] * _nbg[jj], axis=1)   <- un COSENO fra versori
```

> **Il secondo è un PRODOTTO INTERNO fra versori, cioè un coseno d'angolo: lì la normalizzazione è
> CORRETTA E VOLUTA.** **Togliere la divisione dentro `_nb_grav()` romperebbe quel punto.**
> **Conferma la scelta del mandato: si rimoltiplica DOPO, al solo `:2453`.**

### La catena del numeratore NON contiene l'ampiezza

```python
correzione = np.cross(B, nb) + np.cross(_nb_grav(), nb)

B      = somma(nb_vic * w) / somma(w)          con w = _pesi()
_pesi(): base = exp(-d/_lam_archi()) * ramp[i] * ramp[j]   [* il fattore di torsione]
```

**`_pesi()` contiene `d`, `ramp`, `tw`. NON contiene `rho_spin` né `|psi|`.** E `nb_vic`, `nb`,
`_nb_grav()` sono **tutti versori**. **Il numeratore è adimensionale rispetto all'ampiezza.**

### E l'ampiezza c'è, ma al DENOMINATORE

```python
:2393  _rho_s = self._rho_sorgente()          # = rho_spin  (CAMPO_SPINORIALE ON)
       _contrasto = rho_s / peq_nodo
:2417  inerzia = np.maximum(_contrasto * _T2, 1e-6)
       omega = correzione / inerzia
```

> **`rho_spin` compare UNA SOLA VOLTA, e sta sotto.** **Quindi più il campo è debole, più `omega`
> è grande** — l'opposto di una forza.
> **LETTURA 2: l'ampiezza è assente dal numeratore. VIA LIBERA AL §2.**

### ⚠ E una conseguenza che il conto mostra, e va scritta PRIMA

**Per i nodi il cui contrasto NON è al pavimento**, rimoltiplicare dà:

```
omega = (corr * rho) / ((rho/peq) * T2)  =  corr * peq / T2        <- rho SI SEMPLIFICA
```

**Per i nodi AL PAVIMENTO** *(come il 2393: `_contrasto*_T2 = 5.7e-10 << 1e-6`)* **non si
semplifica**, e resta `corr * rho / 1e-6`.

> **Quindi la modifica NON è uniforme: è quasi inerte sui nodi normali e mordente su quelli al
> pavimento.** **È esattamente il comportamento che si vorrebbe** — ma va **misurato**, non dato
> per buono, ed è la ragione per cui l'A/B guarda **i percentili** e non solo il massimo.

## 2. LA MODIFICA — una riga, zero numeri nuovi

```python
_tq = np.cross(self._nb_grav(), nb)
if GRAV_AMPIEZZA:
    _tq = _tq * self._rho_sorgente()[:, None]     # l'ampiezza che _nb_grav() divide via
correzione = correzione + _tq
```

**Flag `GRAV_AMPIEZZA`, OFF di default, byte-identico a spento**, come `COPPIA_RECIPROCA`.
**Si usa `_rho_sorgente()`**, non `rho_spin` diretto: è **lo stesso metodo** che alimenta
`_contrasto`, quindi numeratore e denominatore parlano della **stessa grandezza**. *(Zero numeri
nuovi, zero definizioni nuove.)*

### Cosa NON si fa
**NESSUN tetto, NESSUN clamp, NESSUNA saturazione** su `omega_s`. **Il precedente è `ritmo()`:
forma liscia e saturante, e al passo 60 `r` p25/p50/p75 erano TUTTI a `√2` — la popolazione si è
incollata al tetto.** *Una saturazione non impedisce di arrivare al limite: impedisce solo di
superarlo.*
**NON si tocca** il pavimento `1e-6`, `A7b`, il peso zero alla nascita, `_nb_grav()` stessa, il
termine `B`.

## 3. L'A/B, e il conto atteso

```
ramo A: flag SPENTO   192 -> 240    DEVE combaciare con l'archivio (sigillo di inerzia)
ramo B: flag ACCESO   192 -> 240    stesso override, SIMMETRICO
```

**L'aritmetica della modifica sul nodo 2393** *(non è una previsione: è il conto)*:

```
prima:  0.3809 / 1e-6              = 3.8e+05
dopo:   0.3809 * 5.7e-10 / 1e-6    = 2.2e-04          NOVE ORDINI
```

> **Se il misurato non lo riproduce, c'è altro nella catena** — e allora è quello il reperto.

**Si confronta:** `omega_s` *(percentili e max)* · **nodi con `omega > 1e2`** *(ramo A precedente:
`12`)* · `_inerzia_al_pavimento` · **il nodo 2393** · **`omega·d/cs`: quanti nodi restano sopra 1**,
cioè **oltre il limite causale**.

## 4. IL FALSIFICATORE, dall'esperienza di un'ora fa

**La reciprocità era corretta, derivata, misurata — e l'A/B ha dato nodi eccitati da `12` a `30`.**

> **Se anche questa peggiora, si riporta come NEGATIVO e NON si cabla**, per quanto la fisica sia
> giusta. **Una legge corretta che peggiora il sistema resta un risultato negativo.**

## 5. COSA MI FA FERMARE
- **il ramo A che non combacia** → la modifica non è inerte a flag spento: **STOP**;
- **`omega·d/cs` che resta sopra 1 per la maggioranza** → la cura non ha riportato il sistema nel
  cono causale, **e va detto anche se `omega` scende**;
- **la tentazione di leggere i numeri del ramo B come fisica** → è **mezzo run con override del
  blob**.
