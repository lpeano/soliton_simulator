# `SCALE-TW` — **che cos'è `tw`, e da dove vengono le sue cinque scale**

> **Mandato di Luca, 2026-09-25. SOLA LETTURA, nessuna riga di codice.**
> **STOP: sceglie Luca.** Questo documento non decide niente: legge il codice, misura, e mette
> sul tavolo due letture alternative con le loro leggi candidate.

**Le righe sono del blob `e76fa872`** *(sha1 dei byte grezzi)*. **Cercare per NOME, non per riga**
*(par.0)*: durante questa lettura le righe si sono già spostate una volta — il sito della soglia di
densità era citato `:5749` nella voce `S-MIT1` di stamattina e ora è `:5781`.

---

## (a) CHE COS'È `tw` NEL CODICE — **un accumulatore con perdita, con l'incremento di una fase**

**Il solo aggiornamento per passo** *(`:5081`, ramo `TORS_4PI`; `:5085` il ramo a `2π`)*:

```python
_ttw = _tau_tw_locale(self) if TAU_LOCALI else TAU_TW
self.tw += self._w8(dph + twist_dip - self.twp) - dt_e * self.tw / _ttw
self.twp = self._w8(dph + twist_dip)
```

| pezzo | che cos'è |
|---|---|
| `dph` | `_wphi(phi_i − phi_j)`, la **differenza di fase AVVOLTA** sul periodo di `phi` |
| `twist_dip` | `π·0.5·(χ_i − χ_j)`, il **twist dipolare**: `±π` al massimo, `0` fra uguali |
| `_w8(… − twp)` | l'**INCREMENTO**, avvolto su `±4π` |
| `− dt_e·tw/_ttw` | la **PERDITA**: rilassamento del primo ordine verso zero |
| `self.tw` | **NON è avvolto.** È un accumulatore libero |

> ### ❗ LA CONTRADDIZIONE È QUI, E IL CODICE LA DICHIARA DA SÉ.
> Il docstring di **`_wphi`** avverte: *«⚠ **NON si usa per la TORSIONE: `tw` è un ACCUMULO e non
> ha periodo** (vedi `_w8`)»*.
> Ma **l'incremento passa per `_w8`**, che è un **avvolgimento**, cioè l'operazione propria di una
> **fase**; e la soglia della mitosi è chiamata, nel commento di `mitosi`, **«QUANTO DI OLONOMIA»**
> — che è il linguaggio di un **invariante topologico**.
> **Un invariante topologico non perde.** `− dt_e·tw/_ttw` **è una perdita.**

### DA DOVE VIENE `_ttw`: **DERIVATO, con due regolarizzazioni e un commento che non torna**

`TAU_LOCALI = True` *(`:409`)*, quindi **il ramo vivo è `_tau_tw_locale`** *(`:428`)*:

```python
dom = np.abs(net.phivel[i] - net.phivel[j]) + 1e-3
return np.maximum((2*np.pi) / dom, 1e-3)     # kappa=1: tau_tw = 2pi/|dw_locale|
```

- **È DERIVATO:** `_ttw = 2π/|Δω|` è *«un giro diviso la dispersione di frequenza locale»* — un
  tempo costruito da grandezze già nel sistema. **Nessun numero scelto nella forma.**
- **⚠ MA `TAU_TW = 20.0` *(`:427`)* NON ENTRA:** il codice usa `kappa = 1`. Il docstring dice
  *«`kappa_tw = TAU_TW/(2π)` resta come rapporto `O(1)`»*, e `20/(2π) = 3.183`, **non `1`**.
  **Docstring e codice dicono due cose diverse**, ed è la famiglia dei commenti scaduti (par.9).
  `TAU_TW` sopravvive **solo** come fallback quando `phivel` non è allineato o non ci sono archi.
- **DUE REGOLARIZZAZIONI, da classificare con `A11`:** `+1e-3` sul denominatore e
  `max(…, 1e-3)` sul risultato. **Proteggono da `|Δω| → 0`**, cioè da due nodi in fase — che **non
  è un errore, è un caso fisico**: due nodi coerenti avrebbero `_ttw → ∞`, cioè **nessuna perdita**.
  **Il pavimento `1e-3` sostituisce «memoria infinita» con «memoria di `1e-3`», che è
  l'OPPOSTO.** → **da acclarare, e non l'ho misurato: non so quante volte morde.**

---

## (c) LE CINQUE SCALE — **DERIVATA o SCELTA, con la riga**

| # | scala | valore | riga | **derivata o scelta** |
|--:|---|---|---|---|
| 1 | **`PHI_CRIT`** | `2π` | **`:422`** | **DERIVATA… e giustificata a posteriori nello stesso commento** — vedi sotto |
| 2 | **soglia della mitosi** | `3π` | **`:5504-5506`** | **DERIVATA da una MASSIMO**, e il codice la chiama *«derivazione a posteriori»* — vedi sotto |
| 3 | **inversione di segno** | `3.5π` | **`:5637`** | **DERIVATA, e NON indipendente**: è il punto medio fra soglia e tetto, `centro = (τ_soglia+τ_tetto)/2` |
| 4 | **tetto** `TW_TETTO` | `4π` | **`:5626`** | **DERIVATA** dal ricoprimento doppio… **ma di una variabile che non è limitata a `4π`** |
| 5 | **dominio dell'incremento** | `±4π` | **`_w8`** | **DERIVATA**: `(a+4π) % 8π − 4π` è l'avvolgimento sul doppio ricoprimento |

### ① `PHI_CRIT = 2π` — la derivazione c'è, **ma il commento cita l'ESITO come ragione**

```
PHI_CRIT = 2 * np.pi    # QUANTO DI OLONOMIA. Un giro, non due: il sistema e'
                        # abeliano (settore U(1) varieta' invariante esatta, misurato),
                        # quindi il quanto naturale e' 2pi; il 4pi veniva dall'intuizione
                        # spinoriale, risultata assente. A 4pi la mitosi non scattava MAI
                        # e il grafo restava al 100% oltre portata; a 2pi ripara.
```

**La prima metà è una derivazione** *(settore `U(1)` varietà invariante, misurato → il quanto è
`2π`)*. **La seconda metà è la taratura**: *«a `4π` la mitosi non scattava MAI … a `2π` ripara»*.

> ### ⚠ **È IL VALORE SCELTO PERCHÉ IL MECCANISMO FUNZIONASSE, scritto nel commento stesso.**
> Non dico che la derivazione sia falsa: dico che **le due ragioni sono intrecciate**, e che finché
> lo sono **non si può sapere quale delle due stia tenendo il numero in piedi.**

### ② soglia `= PHI_CRIT + π = 3π` — **il codice la chiama «derivazione a posteriori»**

```python
if TORS_4PI and not FASE_2PI:
    twist_max = np.pi                # |chi_i-chi_j|=2 -> pi*0.5*2 = pi
    soglia0 = PHI_CRIT + twist_max   # = 2pi + pi (emergente), = 3pi
```

La derivazione dichiarata: *«un giro pieno PIÙ il twist dipolare massimo»*.
**È vera come ALGEBRA** — `twist_dip = π·0.5·(χ_i−χ_j)` e `|χ_i−χ_j| ≤ 2` dà `|twist_dip| ≤ π`.

> ### ❗ MA SOMMARE UN MASSIMO A UN QUANTO NON È UNA LEGGE DI CONSERVAZIONE.
> Il quanto `2π` è **il valore a cui una cosa si chiude**; `π` è **il valore più grande che un'altra
> cosa può assumere**. **Non sono commensurabili**: la somma dice *«il caso peggiore»*, non
> *«la condizione di chiusura»*.
> **E il codice lo sa:** il commento `[FASE_2PI]` a `:5500-5502` dice, di sé stesso:
> *«il `2pi + pi` cade, e con esso la sua **derivazione a posteriori**. È il punto PIÙ INCERTO
> della cura»*.

### ③ `3.5π` non è una scala nuova

`centro = 0.5·(τ_soglia + τ_tetto)` in spazio `τ`; riportato su `tw` dà
`(centro−1)·PHI_CRIT = 1.75·PHI_CRIT = 3.5π`. **Se cambiano ① o ②, cambia da sé.** Nessun numero.

### ④ `TW_TETTO = 4π` — **il tetto di una variabile che non ha tetto**

`discesa = clip(1 − |tw|/TW_TETTO, 0, 1)` *(`:5640`)* porta la mitosi a **zero** a `|tw| = 4π`.
**Ma `tw` NON è avvolto**: nulla nel codice impedisce `|tw| > 4π`. Il `4π` è quindi
**un tetto DELLA LEGGE, non della variabile** — e va detto così, perché *«tetto della doppia
copertura»* suggerisce un vincolo che non c'è.

### LE COSTANTI DELLA CAMPANA — **due scelte, una derivata**

| costante | riga | dove | **derivata o scelta** |
|---|---|---|---|
| **`3.0`** in `segno = −tanh(3.0·(τ_pp − centro))` | **`:5638`** | pendenza dell'inversione | **SCELTA.** Il commento spiega **il centro**, non la pendenza |
| **`0.3`** in `soglia = soglia0·(1 − 0.3·tanh(grad_τ))` | **`:5595`** | modulazione locale | **SCELTA**, e dichiarata tale: *«modulazione limitata: la soglia scende di al più ~30 %»* |
| `satura(ecc)` | `satura` | salita sopra soglia | **DERIVATA**: `f/(1+GAMMA·|f|)`, un solo ingrediente e già nel sistema |
| `discesa` lineare in `|tw|/TW_TETTO` | `:5640` | spegnimento al tetto | **FORMA SCELTA** (una rampa lineare); il *punto* dove si annulla è ④ |
| `KICK_TW = 0.35` | `:439` | rinculo di fase alla mitosi | **SCELTA** |

### ⚠ E UNA COSA CHE CORREGGE QUELLO CHE HO REGISTRATO STAMATTINA

**`QMIN_M = 0.000`** *(`:782`)*, e il sito è `0.5·(I_a+I_b) >= QMIN_M · median(peq)` *(`:5781`)*.

> ### **CON `QMIN_M = 0` LA CONDIZIONE È `>= 0`: SEMPRE VERA.**
> La voce **`S-MIT1`** che ho registrato stamattina descrive **una forma reale** — una legge locale
> decisa da una statistica globale — **ma OGGI QUEL SITO È INERTE**, e il `median(peq) = 0.0` con
> `negate = 0` misurati nel sigillo `U2` **erano la conferma e non l'avevo letta così**.
> **La voce resta** *(la forma è un difetto latente: basta `QMIN_M > 0` per accenderla)*, **ma la
> frase «con la scena (ii) la mediana la decide il vuoto» non è oggi operante.** Va corretta.

---

## (d) LA DOMANDA DI LUCA: **`tw` è una FASE o un ACCUMULO?**

**Oggi il codice fa entrambe le cose a metà**, e non è un'impressione: si può elencare **quale
pezzo appartiene a quale lettura.**

| pezzo del codice | coerente con **FASE** | coerente con **ACCUMULO** |
|---|---|---|
| incremento avvolto `_w8(…)` | **sì** — l'incremento di una fase è avvolto | no: un accumulo somma l'incremento vero |
| `tw` **non** avvolto | no: una fase vive sul suo periodo | **sì** |
| perdita `− dt_e·tw/_ttw` | **no**: un invariante topologico **non perde** | **sì** — un'energia si dissipa |
| soglia chiamata *«quanto di olonomia»* | **sì** | no: una soglia energetica non è un quanto di giro |
| soglia `= quanto + massimo` | no: si sommano due cose incommensurabili | no: non viene da un bilancio |
| tetto `4π` con spegnimento | **sì**, se `4π` è il periodo | no |
| `τ_pp = 1 + |tw|/PHI_CRIT` come **tempo proprio** | no | **sì** — `tw` è un'energia che dilata il tempo |
| `_ttw = 2π/|Δω|` | **sì**, è un tempo di sfasamento | **sì**, è un tempo di rilassamento |

> ### **IL CONTO È 4 A 4, E NON PER CASO: sono DUE LEGGI SOVRAPPOSTE, non una legge imprecisa.**

**E c'è una conseguenza che decide, senza bisogno di misure:** se `tw` fosse una fase, **il valore
`tw = 2π` e il valore `tw = 0` sarebbero LO STESSO STATO**. Non lo sono: `τ_pp = 1 + |tw|/PHI_CRIT`
vale `1` nel secondo caso e `2` nel primo, e `discesa` vale `1` contro `0.5`.
**Quindi il codice, DI FATTO, tratta `tw` come un ACCUMULO** — mentre il **nome** della soglia
(*«quanto di olonomia»*) e **l'avvolgimento dell'incremento** dicono fase.

---

## (e) LE DUE LEGGI CANDIDATE — **una per lettura, nessun numero nuovo**

### LETTURA A — `tw` È UNA FASE (avvolgimento topologico)

**La legge:** `tw` **vive su `±4π`** e **non perde**.

```
tw  <-  _w8( tw + _w8(D(dph + twist_dip)) )        # avvolto, NESSUNA perdita
soglia = PHI_CRIT                                  # UN quanto di ricoprimento, non 2pi+pi
```

**Cosa cambia nel codice:** ① `tw` si avvolge; ② **cade il termine `− dt_e·tw/_ttw`**, e con esso
`_ttw`, `TAU_TW`, `_tau_tw_locale` e **i suoi due pavimenti `1e-3`**; ③ **cade `soglia0 = 2π+π`**:
la soglia è **il quanto**; ④ `TW_TETTO` diventa **il periodo**, cioè `discesa` non è più una rampa
scelta ma **la distanza dal punto di identificazione**; ⑤ **cade `τ_pp = 1 + |tw|/PHI_CRIT`**,
perché una fase non è un'energia — **e questo tocca la mitosi, il gradiente di soglia e il tempo
proprio d'arco: è il costo vero di questa lettura.**

**Il legame con `CURA 3`:** è **la stessa domanda**. `CURA 3` è dove vive il **doppio
ricoprimento**; se `tw` è un avvolgimento, **il suo periodo deve essere quello del ricoprimento**,
e `TORS_4PI` smette di essere un flag e diventa **la definizione della variabile**.

**A FAVORE:** la soglia diventa **un quanto**, cioè un numero che **non si può tarare**.
**CONTRO:** perde il tempo proprio d'arco, che **oggi è usato da cinque siti**.

### LETTURA B — `tw` È UN ACCUMULO (energia di torsione)

**La legge:** la soglia viene da un **bilancio**, non da una somma di scale.

```
la mitosi avviene quando l'energia di torsione dell'arco PAGA il costo di creare un nodo:
        E_tors(arco)  >=  E_nodo
con E_tors ed E_nodo presi dalla STESSA hamiltoniana che governa il resto del passo.
```

**Cosa cambia nel codice:** ① `soglia0` **non è più una scala di `tw`**: è la `tw` che soddisfa
`E_tors(tw) = E_nodo`, e **cambia col luogo** senza bisogno del `0.3·tanh` *(che cade)*;
② il termine di perdita **resta** ed è legittimo — **ma `_ttw` va derivato come tempo di
dissipazione di QUELL'energia**, non come `2π/|Δω|` *(che è un tempo di sfasamento: un'altra cosa)*;
③ `_w8` sull'incremento **è un difetto** in questa lettura: un'energia non ha periodo, e avvolgere
l'incremento **butta via l'energia sopra `4π`**; ④ il `3.0` del `tanh` **cade**: la transizione
creazione/repulsione viene dal **segno del bilancio**, non da una sigmoide centrata a mano.

**A FAVORE:** tutto il resto del file è energetico *(`τ_pp` come tempo proprio, la dissipazione, il
viriale)*, quindi **è la lettura che costa meno al codice esistente**.
**CONTRO:** **non ho l'hamiltoniana scritta da nessuna parte del repo**, e `E_nodo` andrebbe
**derivata**. **Senza quella, la lettura B è un programma, non una legge** — e va detto.

### ⚠ CIÒ CHE NON SO, E CHE NON PROVO A COPRIRE

**Non so quale delle due sia giusta**, e **nessuna delle due la decide una misura di `|tw|`**: la
misura del punto (b) dice **se la soglia di oggi è raggiungibile**, non **quale legge sia vera**.
**È `A8`/`E` di `COMPONENTI_PROMOSSE`: si misura per PROMUOVERE, si DIMOSTRA per ESCLUDERE.**

### I CRITERI DI PROVA, SCRITTI ORA — **prima di sapere quale strada si prende**

| | criterio | quale lettura boccia |
|---|---|---|
| **`TW-1`** | **flag OFF = byte-identico**, firma dei byte, un processo per braccio | nessuna: è il presidio |
| **`TW-2`** | **`tw = 0` e `tw = periodo` danno LO STESSO passo**, byte per byte | **boccia A** se falliscono, perché in A sono lo stesso stato |
| **`TW-3`** | **con l'incremento a media nulla, `sum(tw)` è CONSERVATA** *(nessuna perdita)* | **boccia A** se non lo è |
| **`TW-4`** | la soglia **non dipende da `PHI_CRIT` moltiplicato per un numero**: la si cambia di `×2` e la mitosi **scala come il bilancio prevede** | **boccia B** se la soglia resta dov'era |
| **`TW-5`** | **caso che DEVE fallire** *(`P1-sexies`)*: con `E_nodo` messa a zero la mitosi **deve scattare su OGNI arco** | **boccia B** se non scatta: vuol dire che la soglia non viene dal bilancio |
| **`TW-6`** | **frazione di archi che raggiungono la soglia `> 0` su 4 semi** *(non su uno)* | nessuna: è la condizione perché la mitosi esista |

**`TW-2` e `TW-3` sono i due che decidono**, e **nessuno dei due ha bisogno di nuova fisica: sono
due prove sul codice di oggi.**

---

## ❗ (b) LA MISURA — **`|tw|` SI FERMA A `π`, E LA SOGLIA È `3π`**

*(`csv/_test_fork/_scale_tw.py`, referto in `csv/_test_fork/_scale_tw/`, scena `(ii)` `(b)`,
seme `11`, `20` passi — **UN SEME: non è una barra d'errore**)*

**La stima era scritta nella docstring PRIMA di girare** *(par.5-septies)*: `tw` è un **cammino
aleatorio smorzato**, `|tw|_eq ≈ σ·sqrt(_ttw/(2·dt_e))` — la stessa forma di `omega_eq` del par.9,
lì misurata a `×1.03`. **E il criterio era fissato prima:** *se il tipico sta sotto `3π` di più di
un fattore `2`, la mitosi scatta solo sulla coda.*

```
passo   |tw| / pi                            _ttw                 frazione |tw| >= 3 pi
  0     p50 0.0000  p95 0.0000  max 0.0000   p50 13.757  p05 5.369      0.000000
  1     p50 0.9919  p95 2.5891  max 2.9999   p50 13.753  p05 5.367      0.000000
  2     p50 0.9913  p95 2.5848  max 2.9982   p50 10.056  p05 4.014      0.000000
  5     p50 0.9933  p95 2.5758  max 2.9959   p50  7.254  p05 2.901      0.000000
 10     p50 0.9939  p95 2.5176  max 2.9651   p50  3.391  p05 1.337      0.000000
 20     p50 0.9933  p95 2.3434  max 2.8991   p50  1.818  p05 0.690      0.000000
```

### ❌❌❌ RITIRATO IL 2026-09-25: **LA SOGLIA È RAGGIUNTA. LA MISURA QUI SOTTO GIRAVA SU UN CICLO INCOMPLETO**

**`net.step()` NON È UN PASSO:** il passo è `scuoti_vuoto → step → mitosi → rilassa_disegno →
memoria_hebbiana_moto`. **Questa misura chiamava solo `step()`**, quindi **senza scuotimento del
vuoto** *(che è ciò che alimenta `tw`)* **e senza mitosi** *(che non poteva scattare perché non
veniva chiamata)*.

**RIFATTA col passo PIENO, campo MATURO, 4 SEMI, 300 passi**
*(`csv/_test_fork/_scale_tw2.py`)*:

```
passo 300:  |tw| p50 = 0.7600 pi    max = 3.6554 pi +- 0.0870    la soglia e' 3.000 pi
            frazione NELLA FINESTRA = 8.154e-04      (circa 1 arco su 1230)
            NODI NATI DA MITOSI = 48.0 +- 2.4        eventi = 41.2
```

> ### ✅ **LA MITOSI NON È MORTA.** L'affermazione corretta è: **la soglia è raggiungibile da
> ### circa un arco su `1230`, e la mitosi produce `~0.16` nodi per passo su `~4300`.**
> **Né morta né sana: RARA.**
>
> **Cosa RESTA della lettura qui sotto:** `|tw|` **tipico** è sotto la soglia di un fattore `3.9`,
> quindi **la mitosi scatta SOLO SULLA CODA** — e ora la coda ha un numero. E **`_ttw` cala**
> *(`13.8 → 1.67`)*, che era misurato bene.
> **Cosa CADE:** *«mai raggiunta»*, *«frazione `0.000000`»*, *«spenta di un fattore `3`»*.

### ⚙ IL BLOCCO STORICO, che si legge per sapere COM'ERA e COSA L'HA TOLTO

> ### ⛔ **LA SOGLIA `3π` NON È MAI RAGGIUNTA DA NESSUN ARCO, IN NESSUNO DEI 20 PASSI.**
> `max|tw| = 2.8991 π`; la frazione `>= 3π` è **`0.000000`** sempre.
> **Il tipico sta sotto la soglia di un fattore `3.020`** — **sopra** il `2` del criterio.

### ❗ E IL VALORE A CUI SI FERMA DICE **QUALE PEZZO DELLA SOGLIA NON SI ACCUMULA**

**`|tw|` mediano vale `0.9933 π`, cioè `π` entro lo `0.7 %`.** E `π` qui non è un numero
qualunque: **è esattamente `twist_dip` massimo**, `π·0.5·|χ_i − χ_j|` con `|χ_i − χ_j| = 2`.

> ### **`tw` ACCUMULA IL TWIST DIPOLARE E BASTA. IL QUANTO `2π` NON VIENE MAI ACCUMULATO.**
> La soglia è `2π + π` = *«un giro pieno PIÙ il twist dipolare massimo»*.
> **Misurato: si arriva al secondo addendo e MAI al primo.**
> **La mitosi, in questo regime, è SPENTA — e di un fattore `3`, non di un margine.**

### ⚠ NON È UN TRANSITORIO CHE SI RISOLVE ASPETTANDO: **il margine PEGGIORA**

- **`|tw|` non cresce** fra il passo `1` e il `20`: `p50` fermo a `0.993 π`, e il **`p95` CALA**
  *(`2.589 → 2.343`)*;
- **`_ttw` CALA di un fattore `7.6`** *(`13.76 → 1.82`)*: `|Δω|` **cresce**, quindi
  `λ = dt_e/_ttw` cresce e `|tw|_eq ∝ sqrt(_ttw)` **scende**;
- **è il presidio del par.9 al contrario** *(«un'ipotesi che rigenera la propria scusa»)*: qui
  **non c'è nessun «aspetta ancora» da invocare**, perché la grandezza che fissa il livello
  **sta calando**.

**⚠ UN SEME, UNA SCENA, 20 PASSI**, e il tempo di equilibrio è `_ttw/dt_e ≈ 196` passi: il valore
va citato **col passo** *(par.9)*. **La DIREZIONE non è in dubbio**, perché `_ttw` decresce in
tutti i punti misurati.

### COSA QUESTA MISURA **NON** DICE

**Non dice quale delle due letture di (d) sia giusta.** Dice che **la soglia di oggi non è
raggiungibile**: *un numero tarato per far scattare la mitosi non la fa scattare più* nel regime
`A13`. *(`E` di `COMPONENTI_PROMOSSE`: si misura per PROMUOVERE, si DIMOSTRA per ESCLUDERE.)*

### ❗ E SI LEGA A `PHI_CRIT`: **la storia si sta ripetendo col segno opposto**

Il commento di `PHI_CRIT` *(`:422`)* dice: *«a `4π` la mitosi non scattava MAI … a `2π` ripara»*.
**Oggi la mitosi non scatta di nuovo** — non perché il quanto sia `4π`, ma perché **`tw` non
arriva più nemmeno a `2π`**.

> **Se si «riparasse» abbassando la soglia, si rifarebbe esattamente ciò che Luca ha appena
> chiamato «tarato a posteriori». È il motivo per cui il punto (e) propone DUE LEGGI e non un
> numero.**
