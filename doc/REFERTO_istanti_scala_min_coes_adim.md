# REFERTO — **DA QUALE ISTANTE leggono `SCALA_MIN` e `COES_ADIM`**

> **Mandato del 2026-09-21 §②.** **SOLA LETTURA del codice, nessuna modifica, nessuna cura.**
> Simulatore **`4954fe5b`** *(sha1 dei BYTE GREZZI; il `git hash-object` dello stesso file e'
> `26fa354d`, ed e' quello che `prog.csv` scrive — par.5-quinquies, due convenzioni diverse)*.
> **Le righe sono verificate dal DISCO**, non ricordate.

---

## RISPOSTA IN UNA RIGA

**Nessuno dei due legge lo stato di INIZIO PASSO.** `SCALA_MIN` legge, a ogni scrittura, **il valore
lasciato dalla scrittura precedente dello stesso passo**; `COES_ADIM` legge **una MISCELA**: la parte
di densita' e' di fine `step`, ma il suo richiamo elastico legge `d0` **gia' spostato sette volte**
nello stesso passo. **Il risultato dipende dall'ORDINE in cui le leggi vengono chiamate**, e lo si
dimostra algebricamente qui sotto, non per analogia.

---

## ① `SCALA_MIN` — **l'istante e' «adesso», a ogni scrittura**

### 1.1 Il freno legge `self.d0` / `self.d` AL MOMENTO DELLA CHIAMATA

```python
def _sd0(self, dx, mask=None):                                   # :3295
    if not SCALA_MIN:
        return dx
    return self._smorza(self.d0 if mask is None else self.d0[mask], dx, 'd0')   # :3299
```
**`self.d0` e' letto dentro la chiamata**, quindi e' il valore **corrente**, non una copia presa
all'inizio del passo. **Non esiste nel file alcuno snapshot di inizio passo di `d0`**: l'unico
`self.d0.copy()` e' `_tr_pre`, che e' **diagnostico** e gira solo con `TRACCIA_D0` (`:4419`, `:5309`,
e altri sette siti).

Il fattore di frenata e' **`fatt = max(0, 1 - LAM/prima)`** (`:3257`), con `prima` = quel valore
corrente. **Quindi il freno e' PIU' FORTE dove `d0` e' PIU' VICINO a `LAM`**, e **quanto vicino sia
dipende da quante scritture lo hanno gia' mosso in quel passo.**

### 1.2 QUANTI scrittori, e in che ordine

**Nove siti `_sd0` nel file; SEI girano davvero per passo — MISURATO, non contato a occhio.**
Dal contatore `_g_sm_d0` negli snapshot del ramo D: `6476` al passo 1080 e `7196` al 1200, cioe'
**`720/120 = 6.000` esatte per passo**, costante su tutto il run.

| ordine | riga | funzione | cosa scrive |
|---:|---|---|---|
| 1 | `:4420` | `step` | rilassamento viscoso `dt_e*(d-d0)/tau_p_loc` |
| 2 | `:4431` | `step` | diffusione di guscio (`GUSCIO_MORBIDO`) |
| — | `:4435` | `step` | ramo alternativo di 1 (`else` di `TAU_LOCALI`): **non gira** |
| 3 | `:4615` | `mitosi` | spinta (`Locale pura`) |
| 4 | `:5048` | `memoria_hebbiana_moto` | proiezione sul pozzo |
| 5 | `:5195` | `memoria_hebbiana_moto` | **S09 — spinta `* median(d0)`** |
| 6 | `:5201` | `memoria_hebbiana_moto` | **S10 — gravita' `* median(d0)`** |
| 7 | `:5224` | `memoria_hebbiana_moto` | flusso |
| 8 | `:5312` | `memoria_hebbiana_moto` | **coesione, ramo `COES_ADIM`** |
| — | `:5314` | `memoria_hebbiana_moto` | coesione, ramo vecchio (esclusivo col precedente) |

*(La somma a sei significa che due o tre di questi sono a maschera vuota o gated in questa
configurazione. **Il numero misurato e' 6.000/passo, e vale piu' del conteggio delle righe.**)*

**Ognuno dei sei legge `self.d0` come l'ha lasciato il precedente.**

### 1.3 ⚠ LA DIMOSTRAZIONE CHE L'ORDINE CONTA, e che il freno per-scrittura E' UN CRICCHETTO

Siano due incrementi dello stesso passo, **uno in su e uno in giu', di somma NULLA**:
`a > 0`, `b < 0`, `a + b = 0`, a partire da `x > LAM`.

| come si applica | risultato |
|---|---|
| **UNA VOLTA, sulla variazione TOTALE** | `dx = a+b = 0` -> non e' una discesa -> **`x` intatto. Bias ZERO.** |
| separatamente, **prima la salita** | `x + a + b*(1 - LAM/(x+a))` = **`x + LAM*|b|/(x+a)`** |
| separatamente, **prima la discesa** | `x + b*(1-LAM/x) + a` = **`x + LAM*|b|/x`** |

**Tre risultati diversi per la stessa fisica.** I due separati sono **entrambi maggiori di `x`**, e
**diversi fra loro**: il freno per-scrittura **dipende dall'ordine** e **produce un bias VERSO L'ALTO
anche quando la variazione netta del passo e' esattamente zero.**

**Il bias per passo, in forma chiusa:**
```
bias  ~=  LAM * SOMMA( |dx| sulle sole DISCESE ) / d0
```
**E il caso peggiore e' `d0 ~ LAM`, dove il bias vale l'INTERA discesa: a `d0 = 0.83` con
`LAM = 0.8` il fattore `fatt` vale `0.036`, cioe' il 96 % di ogni discesa viene ANNULLATO mentre
ogni salita passa intatta.** *(E `0.83` e' esattamente il valore a cui `d0` resta inchiodato nei
rami SENZA i flag — `T5`.)*

### 1.4 ⚠ E IL CRICCHETTO NON VIOLA IL SIGILLO: vive nella COMPOSIZIONE

I contatori di `_smorza`, letti dagli snapshot del ramo D **su disco**, sono **tutti a posto**:

| contatore | passo 120 | 600 | 960 | 1080 | 1200 | criterio |
|---|---:|---:|---:|---:|---:|---|
| `_g_sm_viol_id` | 0 | 0 | 0 | 0 | 0 | deve essere 0 ✔ |
| `_g_sm_max_giu` | `-0` | `-0` | `-0` | `-0` | `-0` | deve essere `<= 0` ✔ |
| `_g_sm_viol_giu` | 0 | 0 | 0 | 0 | 0 | deve essere 0 ✔ |
| `_g_sm_patol` | 0 | 0 | 0 | 0 | 0 | — |

> **`_g_sm_max_giu = -0` dice che una SINGOLA scrittura non spinge MAI verso l'alto.**
> **Il bias non e' in una scrittura: e' nella SOMMA di sei scritture frenate una per una.**
> Ecco perche' il sigillo `11/11` passa e il cricchetto esiste lo stesso: **il sigillo verifica la
> proprieta' per-scrittura, che e' vera; nessun criterio guarda la COMPOSIZIONE.** *(`A9`: un
> presidio verifica cio' che guarda, non cio' che si spera.)*

### 1.5 `d` — **il freno gira UNA VOLTA PER SOTTO-PASSO, e `nsub` moltiplica il bias**

```python
nsub = int(max(4, n1, n2, n3))          # :4267 -- calcolato UNA VOLTA, PRIMA del ciclo
...
for _ in range(nsub):                   # :4277
    ...
    d_new = (self.d + self._smorza(self.d, dts * vd_half, 'd') if SCALA_MIN    # :4288
             else np.maximum(self.d + dts * vd_half, 0.05))
    ...
    self.d = d_new                      # :4331
```
`self.d` e' **aggiornato in fondo a ogni sotto-passo**, quindi il freno del sotto-passo successivo
legge **il valore del sotto-passo precedente**: stesso schema di `d0`, **`nsub` volte invece di
sei**.

**MISURATO dal contatore `_g_sm_d`, che conta esattamente una chiamata per sotto-passo:**

| intervallo | `_g_sm_d` | **per passo = `nsub` medio** |
|---|---:|---:|
| 120 -> 600 | `+1920` | **4.00** *(il pavimento `max(4, ...)`)* |
| 600 -> 960 | `+1440` | **4.00** |
| 960 -> 1080 | `+480` | **4.00** |
| **1080 -> 1200** | **`+23613`** | **196.8** |

> **⚠ QUESTO E' IL PICCO, ED E' LETTO DA DATI GIA' SU DISCO, senza rigiocare nulla.**
> **Per 1080 passi `nsub` e' stato INCHIODATO a 4. Nei 120 passi fra 1080 e 1200 vale 197 in
> media — un fattore 49 — e poi il run PROSEGUE.** E' la conferma indipendente che l'esplosione e'
> **dentro** quella finestra e che **si e' riassorbita**: se fosse rimasta, `nsub` non sarebbe potuto
> tornare a un valore che consente di scrivere lo snapshot 1200 in 34 minuti.
> *(`_g_sm_discese` fa lo stesso salto: da `2.28e6` a `5.09e7` per passo, fattore 22.)*

**CONSEGUENZA DI LETTURA, e la marco come DERIVATA e NON MISURATA PER SITO:** poiche' il bias del
§1.3 si paga **a ogni frenata**, e le frenate su `d` sono **`nsub` per passo**, **un'esplosione di
`nsub` moltiplica il bias verso l'alto su `d` per lo stesso fattore**. Al picco il freno e' stato
applicato **22 591 volte in un solo passo** (`Z90`) invece di 4. **Non e' dimostrato che questo
chiuda un anello di retroazione** — servirebbe la somma per scrittore, che e' il prossimo strumento —
**ma e' un canale per cui un raffinamento puramente NUMERICO del passo cambia la FISICA**, e un
integratore che non converge al raffinare il passo e' un difetto per definizione.

---

## ② `COES_ADIM` — **istanti MISTI, e un tetto GLOBALE**

### 2.1 Da dove legge, riga per riga

`memoria_hebbiana_moto` (`:4994`) gira **dopo** `step()`, `mitosi()` e `rilassa_disegno()`.
Dentro il blocco della coesione:

| ingresso | riga | **istante** |
|---|---|---|
| `I_nodi = |psi|^2` | `:5232` | **fine `step` (+ mitosi)**: `psi` non e' toccato in questa funzione |
| `grad_I_relativo` | `:5235` | idem, diviso per `self.d[mask]` |
| `lap_arco` | `:5242` | idem |
| `I_arco` | `:5244` | idem |
| `filtro_portata = 1 - tanh(d/LAM)` | `:5248` | **`self.d` di fine `step`** |
| **`richiamo_elastico = -(d0-LAM)/LAM`** | `:5259` | ⚠ **`self.d0` GIA' SPOSTATO da SETTE scritture** *(le tre di `step`, quella di `mitosi`, e le tre di questa stessa funzione a `:5048`, `:5195`, `:5201`, `:5224`)* |

```python
_F_adim = np.tanh(_forza_adim + richiamo_elastico) * filtro_portata     # :5291
```
**Nella stessa `tanh` convivono due istanti diversi:** `_forza_adim` e' costruito su densita' di
**fine `step`**, `richiamo_elastico` su un `d0` di **meta' `memoria_hebbiana_moto`**. **La risposta
alla domanda del mandato e' SI': legge valori misti.**

### 2.2 Il tetto e' GLOBALE — e la risposta su `A5` e' «SI' IN PRINCIPIO, NO IN QUESTO RUN»

```python
_passo_causale = LAM * np.sqrt(K_C) * DT      # :5292
_delta_coes = _passo_causale * _F_adim        # :5293
```
`LAM = 0.8` e `K_C = 2.0` sono **costanti di modulo**: il tetto **non ha nulla di locale**.
`c_sistema = LAM*sqrt(K_C) = 1.1314` (`:5135`, stessa espressione), contro `CS_M = 2.0`.

**La velocita' locale `cs` NON e' costante** — misurata altrove *(`doc/REFERTO_gauge_vuoto.md` §1,
**un seme, 120 passi, altra scena**: `cs/CS_M` mediana `0.8265`, `p05` `0.528`, **min `0.283`**)* —
quindi il cono locale piu' lento vale `~0.566`, e **il tetto globale `1.1314` ne permette il
DOPPIO.** **Strutturalmente il tetto viola `A5`: non conosce il cono del luogo in cui scrive.**

**MA NON E' STATO ESERCITATO IN QUESTO RUN, e va detto:**

| grandezza | valore |
|---|---|
| `_g_coes_tetto` | `0.0113137` = `c_sistema * DT` |
| **`_g_coes_max`** | **`0.00269725`** — *identico in tutti e cinque gli snapshot, dal 120 al 1200* |
| `_g_coes_satura` (`|F_adim| > 0.99`) | **0** su `6.3e8` archi-scrittura |

Lo spostamento massimo mai usato corrisponde a una velocita' di **`0.2697`**, cioe' **il 24 % del
tetto** e **il 48 % del cono locale piu' lento**. **Il difetto del tetto e' REALE ma DORMIENTE**:
va corretto perche' e' sbagliato, non perche' abbia prodotto questo.

**E `_g_coes_satura = 0` chiude una domanda aperta:** la forma adimensionale **non satura mai**, a
differenza di `tanh(stress)*d0` che `Z79` aveva misurato saturo. **`COES_ADIM` fa cio' che dichiara.**

### 2.3 ⚠ COSA CAMBIA DAVVERO `COES_ADIM`, ed e' il contrappeso

Il ramo vecchio (`:5314`) e' `np.clip(coesione_relazionale, -tasso_dinamico, +tasso_dinamico)` con
`tasso_dinamico = tanh(|d-d0|/d0) * d0` (`:5265`): **un tetto che CRESCE con `d0`**.
Il ramo nuovo (`:5312`) ha tetto `LAM*sqrt(K_C)*DT = 0.0113`, **COSTANTE**.

A `d0 = 30` e `d = 21` (ramo D, passo 1200) il vecchio tetto vale `tanh(0.3)*30 = 8.7`:
**770 volte il nuovo.** E il termine che quel tetto lascia passare e' **negativo** — il richiamo
elastico `-(30-0.8)/0.8 = -36.5` domina — cioe' **tira `d0` GIU'**.

> **Letto cosi', `COES_ADIM` non «aggiunge una spinta»: TOGLIE UN FRENO che cresceva insieme alla
> fuga.** E' esattamente la forma dell'ipotesi di Luca — *il cricchetto di `SCALA_MIN` diventa
> decisivo solo quando manca il contrappeso* — **con la differenza che qui e' letta dal codice
> invece che congetturata.**
>
> **⚠ E NON E' UNA CONCLUSIONE MISURATA.** Entrambi i rami sono moltiplicati per
> **`filtro_portata = 1 - tanh(d/LAM)`**, che a `d = 21` vale `~1e-23`: **a grande `d` i due rami
> sono ENTRAMBI spenti**, e la differenza vive **solo sugli archi corti**. **Quanto pesi quella
> differenza NON e' misurato**, e serve la somma per scrittore per dirlo. Scriverlo come causa
> sarebbe la congettura travestita da riscontro che `Z90` ha gia' preso una volta.

---

## ③ LA CURA CANDIDATA — **DERIVATA, NON APPLICATA**

Il mandato la propone e **la derivazione la conferma**:

> **frenare `d0` UNA VOLTA PER PASSO, sulla VARIAZIONE TOTALE, a partire dal valore di INIZIO PASSO.**

**Perche' funziona, e non e' un'opinione:** nella tabella del §1.3 la prima riga da' **bias ZERO
esatto** quando la variazione netta e' nulla, e **non contiene l'ordine**. Le salite e le discese
dello stesso passo **si compensano PRIMA del freno**, che e' cio' che la causalita' richiede: il
vincolo e' *«nessuna lunghezza sotto `LAM`»*, ed e' una proprieta' dello **stato a fine passo**, non
di ciascuna delle sei scritture intermedie — **nessuna delle quali e' uno stato fisico.**

**Per `d` la stessa cura significa frenare a fine `step`, non dentro il ciclo dei sotto-passi**, e
questo toglie anche la dipendenza da `nsub` del §1.5: **il raffinamento del passo torna a essere
numerico.**

**⚠ NON APPLICATA, come da mandato.** E prima di applicarla servono, dichiarati qui:
1. **la somma per scrittore** *(rigiocate tracciate di D, S e K con `TRACCIA_D0`)*, separata fra
   **SALITE** e **DISCESE**, piu' `SOMMA(dx_eff - dx)` per passo: e' il numero che dice **quanto**
   vale il bias, non solo che esiste;
2. **un sigillo sulla COMPOSIZIONE**, non solo sulla singola scrittura — oggi non esiste;
3. **la riduzione al limite:** a variazione netta negativa il nuovo freno deve dare lo stesso
   risultato del vecchio applicato una volta sola.

---

## ④ COSA QUESTO REFERTO **NON** DICE

- **NON dice che `SCALA_MIN` sia sbagliato.** Fa esattamente cio' che dichiara, per-scrittura, e i
  quattro contatori lo provano su `3.5e4` chiamate. **Il difetto e' nel PUNTO DI APPLICAZIONE.**
- **NON dice che il cricchetto spieghi la fuga di `d0`.** `§1` del mandato precedente aveva gia'
  chiuso che **nessuno dei due flag da solo fa scappare `d0`**; questo referto dice **per quale
  meccanismo** l'interazione potrebbe farlo, **non che lo faccia.**
- **NON e' una misura del bias.** Tutto il §1.3 e' **algebra esatta**; tutto il §1.5 sotto la
  tabella e' **derivazione**. Gli unici NUMERI MISURATI sono i contatori, e vengono da snapshot
  **gia' su disco**.
- **NON tocca il codice.** Nessuna modifica, nessuna cura, come da mandato.
