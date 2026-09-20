# REFERTO — **i cinque erano GIA' diversi al passo 120, e lo stiramento PRECEDE la velocita'**

> PARTE ① del mandato dell'innesco. **Sola lettura di due `.pkl`**, nessuna CPU rubata ai run.
> Strumento `csv/_test_fork/_innesco_cinque.py` (`7e0ec88f`, `d810871`), committato prima di girarlo.
> Dati grezzi: `csv/_test_fork/_innesco_cinque.txt`. Ramo **B**, passi **120** e **240**.
> **«Diverso» e' misurato col RANGO PERCENTILE nella popolazione, non asserito.**

---

## 1. LA RISPOSTA ALLA DOMANDA BINARIA: **ERANO GIA' ANOMALI**

Il mandato chiedeva: *«al passo 120 quei cinque erano GIA' DIVERSI, o erano normali?»*

**Su undici campi misurati, DUE erano gia' al vertice della popolazione al passo 120:**

| campo | `16` | `481` | `621` | `627` | `837` | verdetto |
|---|---|---|---|---|---|---|
| **`_deg`** | p98.5 | **p99.7** | p98.7 | **p99.8** | p98.7 | **GIA' ANOMALO** |
| **`phivel`** | **p99.3** | **p99.8** | p97.2 | **p99.6** | p98.3 | **GIA' ANOMALO** |
| `\|psi\|` | p82.0 | p84.0 | p81.1 | p80.5 | p79.9 | alto, non estremo |
| `phi_s` | p75.2 | p66.4 | p57.5 | p65.1 | p56.4 | normale |
| `\|omega_s\|` | p67.1 | p67.7 | p62.5 | p65.9 | p67.4 | **normale** |
| `\|mem_mot\|` | p49.3 | p59.7 | p67.8 | p61.8 | p80.3 | **normale** |
| `eta` | p86.3 | p73.5 | p43.9 | p48.2 | p58.6 | **normale** |
| `rho_spin` | p57.8 | p67.5 | p55.7 | p52.0 | p50.7 | **normale AL 120** |

**E `_deg` non si muove di un'unita' fra i due passi** (`605, 643, 610, 650, 610`): **non e' una
proprieta' che il sistema ha sviluppato, e' una proprieta' che quei nodi avevano GIA'.**

### 1.1 Un campo che invece DIVENTA anomalo, e dice la direzione

```
rho_spin    passo 120:  p57.8  p67.5  p55.7  p52.0  p50.7      <- normale
            passo 240:  p97.2  p99.0  p86.4  p81.2  p97.3      <- anomalo
```
**`rho_spin` e' una CONSEGUENZA, non una causa**: al 120 e' al `p50`-`p67`.

### 1.2 ⚠ E `perc_chi` NON e' il discriminante
`481` vale `-1`, gli altri quattro `+1`. **Il nucleo e' chiralmente MISTO**, coerente con `Z74`
*(i nodi veloci hanno le proporzioni della popolazione)*.

---

## 2. ⚠ IL REPERTO PRINCIPALE — **lo STIRAMENTO era gia' li', la VELOCITA' no**

| passo 120 | popolazione | i cinque *(mediana dei loro archi)* |
|---|---|---|
| **`d/d0`** | p50 **1.025** | **1.44 – 1.76** |
| `\|vd\|` | p50 `0.192`, **max `2.923`** | p50 `0.31`-`0.54`, **max `1.46`-`1.68`** |

> **I loro archi erano gia' tesi del `44`-`76 %` mentre l'arco tipico stava all'`2.5 %`.**
> **Ma la loro VELOCITA' non era anomala affatto: il massimo dei loro archi (`1.68`) sta SOTTO il
> massimo della popolazione (`2.92`).**

**E l'arco che diventera' il peggiore del sistema era GIA' il piu' teso fra i cinque:**
```
arco 16-481     passo 120:   d/d0 = 8.113    |vd| =  0.7297      <- teso, LENTO
                passo 240:   d/d0 = 10.9     |vd| = 79.15        <- il peggiore del sistema
```
**`d/d0` cresce di `1.34x`. `|vd|` cresce di `108x`.**

> **L'ORDINE CAUSALE SI LEGGE: prima la TENSIONE, poi la velocita'.**
> **Non e' una velocita' che stira un arco: e' un arco teso che, quando la molla lo richiama,
> genera la velocita'.** **E' coerente col meccanismo gia' scritto in `Z74`** *(sovraelongazione),
> **e ne fissa il verso.**

### 2.1 E una cosa che nessuna delle letture prevedeva: **da MOLTI POCO tesi a POCHI MOLTISSIMO**

```
d/d0 mediana degli archi dei cinque:   passo 120: 1.44-1.76     passo 240: 1.05-1.14
d/d0 MASSIMO degli archi dei cinque:   passo 120:  10.8-31.3    passo 240:  6.9-68.0
```
**La mediana SCENDE verso il riposo mentre il massimo SALE.**
> **Fra il 120 e il 240 la tensione si e' CONCENTRATA: molti archi mediamente tesi si sono
> rilassati, e pochi sono esplosi.** **E' lo stesso profilo del `p99` che scende mentre il massimo
> sale (`Z74`), ma qui misurato sulla GEOMETRIA invece che sulla velocita'.**

---

## 3. ⚠ COSA QUESTO CAMBIA PER LA PARTE ② — **e va letto prima di lanciarla**

Il mandato prevedeva due esiti: *«erano gia' anomali -> l'innesco e' VISIBILE»* oppure *«erano
normali -> serve la PARTE ②»*. **L'esito e' il primo, ma con una conseguenza che va detta:**

> **Se al passo 120 la tensione E' GIA' LI' (`d/d0 = 8.1` sull'arco `16-481`), allora la rigiocata
> `120 -> 240` NON mostrerebbe l'ORIGINE: mostrerebbe l'ESCALATION.**
> **L'origine sta PRIMA del 120.**

E' esattamente la clausola che il mandato stesso aveva previsto — *«significa che la causa sta piu'
indietro del 120»* — **solo che si sa gia' adesso, senza spendere la rigiocata per scoprirlo.**

**Quindi la PARTE ② ha DUE forme possibili, e non e' la stessa spesa:**

| | cosa mostrerebbe | costo |
|---|---|---|
| **rigiocata `120 -> 240`** | **come** la tensione si concentra e quando `\|vd\|` si stacca | 120 passi |
| **rigiocata `0 -> 120`** | **perche'** quei legami si sono tesi la prima volta — **la domanda del mandato** | 120 passi, **dalla semina** |

**La seconda e' quella che risponde a *«PERCHE' QUEI LEGAMI SI SIANO TESI LA PRIMA VOLTA»*.**
**La prima risponde a una domanda diversa, e piu' piccola.**

---

## 4. IL COSTO DELLA PARTE ②, dichiarato PRIMA — **e la raccomandazione**

**Misura di riferimento, dal `prog.csv` del ramo B nell'epoca giusta** *(frame 20-30, cioe' i passi
120-180, prima che io rubassi CPU)*: **`23.4` - `25.1 s/frame`, cioe' `~4.1 s/passo`.**

```
120 passi x ~4.1 s        = ~500 s  = ~8 min   se girasse DA SOLA
con DUE run vivi          = ~15-20 min         (contesa misurata: x1.33 a due processi, e qui sarebbero TRE)
```

**⚠ E IL COSTO VERO NON E' IL MIO TEMPO: E' QUELLO CHE RUBA AI RUN.** E' misurato, ed e' mio:
**il ramo B passo' da `25` a `84 s/frame` mentre giravo scipy e `git log -S`.** **Il ramo B e' ora a
`121 s/frame`: un terzo processo lo peggiorerebbe ancora.**

**RACCOMANDAZIONE, e la decisione resta di Luca:**
> **aspettare che il ramo A chiuda** *(frame 290/500, `29 s/frame` -> **~1.7 h**)*, **poi rigiocare
> `0 -> 120` con la macchina meno carica.**
> **Motivo: la PARTE ① ha gia' risposto alla domanda binaria, quindi la rigiocata non e' piu'
> urgente — e la forma che serve (`0 -> 120`) e' diversa da quella che il mandato aveva previsto.**

---

## 5. COSA QUESTO REFERTO **NON** DICE

- **NON dice PERCHE' quei cinque avessero grado `~620` e `phivel` al `p99`** alla semina. **E' la
  domanda aperta**, ed e' quella che la rigiocata `0 -> 120` potrebbe chiudere;
- **NON dice che il grado alto CAUSI la tensione.** Sono **correlati** al passo 120; **la causalita'
  richiede la rigiocata**, e con **un seme** non si attribuisce comunque;
- **NON decide l'A/B di `chi_basc`**, e **non si estende al blocco del passo 2700**;
- **`rho`, `inerzia`, `tau` per NODO non sono nello snapshot** *(verificato elencando gli attributi)*
  — **dichiarati non misurabili invece che stimati.** `tau` stampato e' **per arco** e **derivato**
  come `d/cs`: un oggetto diverso.
