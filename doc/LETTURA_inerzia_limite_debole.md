# `INERZIA-1` — **da dove viene l'inerzia, perché cede a `k = 2`, e quale forma resta regolare**

> **Mandato di Luca, 2026-09-25: SOLA LETTURA.** *«Da dove vengono `_contrasto` e `_T2` (`:3226` e
> dintorni), perché crollano a `k = 2` e non a `k = 4`, e quale forma DERIVATA resta regolare nel
> limite di accoppiamento debole senza numeri nuovi (`STANDARD 10`: contare le leggi prima e
> dopo). Criteri scritti prima: `|omega|` a `k = 2` dello stesso ordine di `k = 77`; flag spento
> byte-identico.»*
>
> **Nessuna cura. Decide Luca.**

---

## 1. DA DOVE VIENE L'INERZIA — la catena completa, dal codice

```python
_T        = self._tempo_luce_nodo(i, j)          # d_nodo / cs_nodo
_T2       = _T * _T                              # T^2: LA DIMENSIONE dell'inerzia
_peq_nodo = MEDIA di `peq` sugli archi del nodo   # bincount(peq) / bincount(1)
_rho_s    = self._rho_sorgente()
_contrasto = _rho_s / _peq_nodo                  # un NUMERO PURO
inerzia   = max(_contrasto * _T2, 1e-6)
```

E `d_nodo` a sua volta:

```python
grado  = bincount(i) + bincount(j)
somma  = bincount(i, weights=d) + bincount(j, weights=d)
d_nodo = somma / max(grado, 1)                   # LA MEDIA delle `d` del nodo
d_nodo[grado <= 0] = LAM                         # NODO ISOLATO -> `LAM`
```

### LA DERIVAZIONE È SCRITTA, ED È BUONA — va detto prima della critica

Il commento a `:3226`-`:3235` porta **tre punti indipendenti**, non una taratura:

- **la dimensione:** da `omega = coppia/inerzia` con `omega ~ 1/T` segue che **l'inerzia è un
  TEMPO AL QUADRATO**; `coppia = cross(B, nb)` è versore × versore, **adimensionale**;
- **l'esponente `cs^-2`**, che `(d/cs)²` contiene già *(e per questo `_fatt_cs` è stato TOLTO
  dall'inerzia: lasciarlo darebbe `cs^-4`)*;
- **`A6`**, il teorema: l'inerzia si valuta sullo stato **del passo precedente**, non di questo —
  *«in meccanica la massa si valuta a `t`, non a `t+dt`»*.

**E la forma precedente era peggiore, misurato:** `max(rho_sorgente·(CS_M/cs)², 1e-6)` aveva **il
pavimento attivo sul `100.00 %` dei nodi a ogni passo** — *«`inerzia` non era "quasi sempre al
pavimento", ERA il pavimento»*.

> **Quindi `INERZIA-1` non dice «la legge è sbagliata»: dice che una legge derivata e migliore
> della precedente CEDE IN UN LIMITE che nessuno aveva provato.**

---

## 2. PERCHÉ CEDE A `k = 2` E NON A `k = 4`

### I NUMERI MISURATI, riordinati per fattore

```
k      COPPIA     inerzia    _contrasto   _T2 (ricavato)   coppia/inerzia   |omega|
77     0.3329     2.727      3.4056       0.8007           0.1262           0.7232
20     0.3284     0.7775     2.2691       0.3426           0.4123           0.7260
 8     0.2923     0.1940     0.8824       0.2199           1.3749           0.7335
 4     0.2909     0.2467     1.3122       0.1880           1.8668           0.7211
 2     0.7958     0.04420    0.2594       0.1704           192.0            2.9683
```

### ❗ PRIMA COSA, E NON ERA NEL MANDATO: **l'inerzia NON È MONOTONA in `k`**

**`k = 8` ha inerzia `0.194`, MINORE di `k = 4` che ha `0.247`.** E `_contrasto` fa lo stesso salto
al contrario: `0.882` a `k = 8` contro `1.312` a `k = 4`.

> **Una grandezza non monotona in `k` non ha un «limite» in senso proprio: ha una DISPERSIONE.**
> Con **un solo nodo per seme** questo può essere rumore del singolo caso — **e va detto invece di
> leggere i cinque punti come una curva.**

### ❗ SECONDA COSA, ED È UN LIMITE DELLA MIA MISURA: **parte del crollo di `_T2` È IL MIO TAGLIO**

`d_nodo` è **la MEDIA delle `d` degli archi del nodo**, e **io ho tolto i più LUNGHI per primi**
*(scelta dichiarata nello strumento)*. **Quindi `d_nodo` cala per costruzione**, e con essa
`_T2 ∝ d_nodo²`.

```
_T2 da k = 77 a k = 2:   ×0.213      cioe' d_nodo ×0.46
```

> ### ⚠ **SE AVESSI TOLTO I PIÙ CORTI, `d_nodo` SAREBBE SALITO e `_T2` con lui.**
> **Il contributo di `_T2` al crollo non è una proprietà della legge: è una proprietà del mio
> taglio.** Lo dico perché altrimenti il referto attribuisce alla legge un effetto che ho messo io.
> **→ la misura va rifatta anche col taglio opposto, e va in coda.**

### ✅ TERZA COSA, E QUESTA SÌ È DELLA LEGGE: **`_contrasto` crolla di `×0.076`, e non per il taglio**

`_contrasto = _rho_s / _peq_nodo`, e **`_peq_nodo` è la MEDIA di `peq` sugli archi del nodo**.

- `_rho_s` è la densità sorgente, che viene dal **campo**, che viene dai **pesi**, che vengono
  dagli **archi**: togliere archi **abbassa `_rho_s`**;
- `_peq_nodo` è una media su **pochi valori**, quindi **non cala allo stesso modo**: è rumorosa.

> ### **IL RAPPORTO DI DUE GRANDEZZE CHE DIPENDONO DAL VICINATO IN MODO DIVERSO NON HA UN LIMITE.**
> **È la ragione strutturale**, e non dipende da quali archi si toglie: `_rho_s` è **estensiva nel
> vicinato** *(somma di contributi)*, `_peq_nodo` è **intensiva** *(una media)*. **Dividere
> un'estensiva per un'intensiva dà una grandezza che scala col numero di vicini** — cioè
> **esattamente ciò che non deve fare un fattore adimensionale.**

### E PERCHÉ `|omega|` RESTA PIATTO FINO A `k = 4`

```python
omega_new = omega_src + dtn_c * (correzione/inerzia - omega_src/_tau)
```

**`omega` ha MEMORIA**: un salto in `coppia/inerzia` entra moltiplicato per `dt` e si accumula
lentamente, e il termine `-omega/_tau` lo riporta indietro.
**A `k = 4` il rapporto vale `1.87`; a `k = 2` vale `192`, cioè `×103`.** **Lì l'ingresso vince
sulla memoria**, e `|omega|` salta.

> **Quindi il «cedimento a `k = 2`» non è una soglia della legge dell'inerzia: è il punto in cui
> il suo errore supera il rilassamento.** La legge peggiora **gradualmente** *(`0.126 → 0.41 →
> 1.37 → 1.87 → 192`)*; è `omega` che **lo mostra di colpo**.

---

## 3. ✅ E LA LEGGE HA GIÀ UN LIMITE REGOLARE — **a `k = 0`, non a `k = 2`**

```python
d_nodo[grado <= 0] = LAM        # NODO ISOLATO: nessun arco da cui leggere la scala
```

> ### ❗ **PER IL NODO ISOLATO LA LEGGE È GIÀ REGOLARE: `d_nodo = LAM`, la scala che esiste.**
> **Quindi la legge è regolare a `k = 0` e a `k` grande, e CEDE IN MEZZO.**
> **Non è un limite mancante: è un limite scritto per il caso estremo e non per quelli vicini.**

---

## 4. LE FORME CANDIDATE — con il **conteggio delle leggi**, `STANDARD 10`

**Oggi:** `inerzia = max(_contrasto · _T2, 1e-6)` — **due fattori** *(`_contrasto`, `_T2`)* **più
un pavimento**.

### CANDIDATA A — **`inerzia = _T2` e basta** *(togliere `_contrasto`)*

```
leggi PRIMA: 2 fattori + pavimento          leggi DOPO: 1 fattore + pavimento      -> UNA IN MENO
```

**A FAVORE:** `_T2` **porta già tutta la dimensione** *(è il punto della derivazione: l'inerzia è
un tempo al quadrato)*; `_contrasto` è **il fattore adimensionale che non ha un limite**; e
`STANDARD 10` è soddisfatto **togliendo**, non aggiungendo.
**Effetto stimato dai numeri di oggi:** `coppia/inerzia` passerebbe da `×1521` a **`×11`** fra
`k = 77` e `k = 2` — **un miglioramento di `138` volte, non la regolarità.**
**CONTRO:** **quel residuo `×11` è il crollo di `_T2`, che è in parte IL MIO TAGLIO** *(punto 2)*.
**Senza la misura col taglio opposto non si sa quanto resti.**
**E si perde una cosa:** `_contrasto` è ciò che fa dipendere l'inerzia dalla **densità locale** —
togliendolo, **un nodo in una regione densa e uno nel vuoto avrebbero la stessa inerzia a parità
di `d`**. **Va deciso se quello è un guadagno o una perdita, e non lo decido io.**

### CANDIDATA B — **`d_nodo` con lo stesso trattamento del nodo isolato**

`d_nodo = somma/grado`, e per `grado = 0` vale **`LAM`**. **La candidata è estendere quella stessa
regola:** `d_nodo = max(somma/grado, LAM)`.

```
leggi PRIMA: 2 fattori + 1 pavimento        leggi DOPO: 2 fattori + 1 pavimento    -> PARI
```

**A FAVORE:** **non è un numero nuovo** — `LAM` è già il valore che la legge usa per il caso
estremo, e questa è **la stessa scelta estesa ai casi vicini**. **È coerente con `A13`**: sotto
`LAM` non esiste una distanza, quindi **una MEDIA di distanze non può stare sotto `LAM`**.
**CONTRO:** **`A11`.** Un `max` che *«protegge da un errore»* è vietato; questo protegge da
*«`d_nodo` sotto `LAM`»*, **che `A13` dichiara impossibile** — quindi **è un vincolo fisico
dichiarato, non un cerotto**. **Ma la distinzione va argomentata, non asserita**, e in questo caso
`d_nodo` **non scende sotto `LAM`** nei dati di oggi *(le `d` sono `>= LAM`, quindi la loro media
lo è)*: **quindi la candidata B NON risolve il crollo misurato.** *(È una guardia giusta e
inefficace: va detto.)*

### CANDIDATA C — **rendere `_contrasto` INTENSIVO su ENTRAMBI i lati**

Il difetto strutturale è: `_rho_s` **estensiva**, `_peq_nodo` **intensiva**. La candidata è
**usare la stessa riduzione per entrambi** — cioè `_rho_s` **per arco**, mediata come `peq`.

```
leggi PRIMA: 2 fattori                      leggi DOPO: 2 fattori                  -> PARI
                                            ma il rapporto diventa adimensionale
                                            **e invariante nel numero di vicini**
```

**⚠ E LA FORMULAZIONE VA CORRETTA, letta dal codice:** `_rho_sorgente()` **è già PER NODO**
*(`|psi[k]|²`, oppure `rho_spin` con `CAMPO_SPINORIALE`)*. **Non serve «una versione per arco».**
**Ma resta ESTENSIVA NEL VICINATO, e la ragione è nel codice:** `psi = _mat(w) @ (amp·exp(iφ))` è
**una SOMMA PESATA sui vicini**, quindi `|psi|²` **cresce col numero di vicini**. `_peq_nodo`
invece è **esplicitamente una MEDIA** *(`bincount(peq)/bincount(1)`)*.

**Quindi la candidata `C`, detta giusta:** **normalizzare `_rho_s` come `_peq_nodo` già lo è** —
cioè **per vicino**, non in assoluto.

**A FAVORE:** **è la correzione del difetto NOMINATO**, non un rimedio ai suoi effetti: un
rapporto fra due grandezze **ridotte allo stesso modo** non scala col grado. E **non introduce
numeri**: la riduzione che serve è **quella che il codice usa già dall'altro lato**.
**CONTRO:** **cambierebbe l'inerzia su TUTTI i nodi**, non solo su quelli a `k` piccolo: **è la
candidata con l'effetto più largo, e quindi quella che richiede il sigillo più severo.**
**E ne cambierebbe anche la SCALA** *(dividere per il grado sposta l'inerzia di un fattore `~77`
sui nodi tipici)*: **il pavimento `1e-6` andrebbe riverificato**, perché nella forma precedente
era attivo sul `100 %`.

---

## 5. I CRITERI, come Luca li ha scritti — **e uno va precisato**

| | criterio | nota |
|---|---|---|
| **`I1`** | **flag spento byte-identico**, firma dei byte, un processo per braccio | par.2.1 |
| **`I2`** | **`\|omega\|` a `k = 2` dello STESSO ORDINE di `k = 77`** | il criterio di Luca |

> ### ⚠ **`I2` VA PRECISATO, E LA RAGIONE È NEI DATI DI OGGI:** `|omega|` a `k = 77` vale
> ### `0.7232` e a `k = 4` vale `0.7211` — **già dello stesso ordine**. Quindi un criterio su
> ### `|omega|` **sarebbe soddisfatto anche da una legge che peggiora di `×15`** *(il rapporto
> ### `coppia/inerzia` da `0.126` a `1.87`)*, **perché la memoria di `omega` lo nasconde.**
>
> **Il criterio va messo su `coppia/inerzia`, non su `|omega|`:** è l'INGRESSO, e non ha memoria.
> **`I2-bis`: `coppia/inerzia` a `k = 2` dello stesso ordine di `k = 77`.**
> *(E `|omega|` resta, come controllo che l'effetto arrivi davvero alla dinamica.)*

**E un terzo criterio, che i dati di oggi rendono necessario:**

> **`I3` — LA MISURA SI RIFÀ CON IL TAGLIO OPPOSTO** *(togliere i più CORTI)*. Senza,
> il contributo di `_T2` al crollo **non è separabile dal taglio**, e qualunque cura verrebbe
> giudicata su un effetto che è in parte mio. **→ è in coda, e viene PRIMA della cura.**

---

## ⛔ STOP — decide Luca

**Il difetto è dimostrato** *(`coppia/inerzia` `×1521`)*. **La ragione strutturale è nominata**
*(un'estensiva divisa per un'intensiva)*. **Tre candidate, e nessuna scritta.**
**E due cose che vanno fatte PRIMA di scegliere:** la misura col **taglio opposto** *(`I3`)* e la
lettura di **se `_rho_sorgente()` abbia una forma per arco** *(candidata `C`)*.
