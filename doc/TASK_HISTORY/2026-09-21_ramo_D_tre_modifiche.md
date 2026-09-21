# TASK HISTORY — **RAMO D: le tre modifiche insieme** (2026-09-21)

> **Scritto e committato PRIMA del codice** (par.5-septies). Mandato perentorio: tre modifiche, tre
> flag separati, `False` di default, **un** run. **Le derivazioni non sono un checkpoint: si
> scrivono qui e si procede.**
> Partenza: simulatore **`54623593`** *(con `CHI_COOP` gia' dentro e sigillato)*, driver `0f0a5f0b`.

---

## 0. STATO ALL'INIZIO — **niente da fermare**

**Punto ① del mandato eseguito: zero processi `python` vivi** *(`Get-CimInstance Win32_Process`)*,
e l'ultima voce di `doc/STATO_RUN.md` e' **chiusa** (`FINITO`, ramo A ai 3000 passi).
**Nessuna cattura `py-spy` da fare, nessun archivio parziale a rischio.**

**E MODIFICA ① E' GIA' FATTA E SIGILLATA** *(mandato precedente, `0f4fc1e` + `7b4cafa`)*:
`_sigillo_chicoop.py` **8/8**, tutti i bloccanti compresi — `Z1` byte-identico, `Z1b` il ramo
geometria **irraggiungibile** a flag spento, `Z2` le chiamate divise `30`/`30`, `Z2b` controllo
positivo (i due array differiscono in `30` passi su `30`, fino a `2535` nodi, e le due cache
portano contenuti diversi in `29`), `Z3` `chi_basc` scrive `perc_geom` `30` volte e `perc_chi`
**`0`**, `Z4` `len(perc_geom) == n` sempre, `Z5` nessun `NaN`.

### ⚠ UNA DEVIAZIONE DAL MANDATO, DICHIARATA
Il mandato dice *«la cache `_chi_core_nodi` e' solo di geometria»*. **Ho fatto l'opposto per NOME:**
`_chi_geom_nodi` e' la cache della geometria, `_chi_core_nodi` resta quella della carica.
**La fisica e' identica** — `TORS_4PI` riceve la geometria in entrambi i casi — **e la ragione della
scelta e' che cosi' il ramo a flag spento non cambia una riga** *(byte-identita' `Z1` piu' pulita)*
**e la colonna diagnostica `chi_core_media` conserva il significato che aveva.**

---

## 1. RAGIONAMENTO PRELIMINARE — *cosa credo prima di guardare*

- **il sistema vive fra il 26 % e il 55 % sotto `LAM`**: `SCALA_MIN` sposta **fino a meta' degli
  archi**. E' voluto, e vuol dire che **il ramo D non e' il ramo A con tre ritocchi: e' un altro
  sistema**;
- **`COES_ADIM` sostituisce il clip `tanh(stress)*d0`**, che `Z79` ha misurato **saturo**: il
  tetto diventa **causale** invece che proporzionale a se' stesso;
- **non so se D arriva ai 3000 passi.** E' la domanda, non una previsione;
- **non so attribuire nessun esito a nessuna delle tre.** Tre interruttori insieme: e' contro par.1,
  ed e' una decisione esplicita di Luca. **Per questo i flag restano SEPARATI**, e i confronti
  legittimi verranno dopo, **dentro** il sistema nuovo (D contro D con un flag spento), **mai
  contro A o B**.

---

## 2. DERIVAZIONE DI `SCALA_MIN` — **la forma, e perche' l'altra cade**

**IL VINCOLO:** una mappa `L : (0, inf) -> (LAM, inf)` che sia **monotona**, **liscia** *(niente
gradino: `max(x, LAM)` ha un angolo nella derivata)*, che valga **`L(x) -> x` per `x >> LAM`** e
**`L(x) -> LAM+` per `x -> 0`**, **costruita con `LAM` soltanto**.

### ⚠ IL CANDIDATO `tanh` CADE, e il criterio del mandato e' esattamente quello che lo uccide
`L(x) = LAM * (1 + tanh(x / LAM))`:
- `x -> 0` da' `L -> LAM` ✓;
- **`x -> inf` da' `L -> 2*LAM`.** **SATURA ANCHE IN ALTO.**

> **Conseguenza sullo stress:** `d0` verrebbe **tappato a `2*LAM`** mentre `d` continua a essere
> spinto da `acc`, quindi `stress = |d - d0| / d0 >= (d - 2 LAM) / (2 LAM)` **CRESCE SENZA LIMITE
> con `d`.** **Il mandato chiede la forma in cui lo stress resta FINITO: questa e' la forma in cui
> DIVERGE.** **Respinta per misura del proprio criterio, non per gusto.**

### LA FORMA SCELTA — **compressione dell'avvicinamento**
```
L(x) = LAM + x * exp(-LAM / x)            (x > 0;  L(0) := LAM)
```
- **`x -> 0+`**: `exp(-LAM/x) -> 0` piu' in fretta di qualunque potenza, quindi **`L -> LAM+`, e non
  lo tocca mai** ✓;
- **`x >> LAM`**: `L = LAM + x(1 - LAM/x + LAM^2/2x^2 - ...) = x + LAM^2/(2x) + O(x^-2)`, cioe'
  **`L -> x`** con errore **relativo `LAM^2/(2x^2)`** ✓ — **e' l'identita' a grande scala, non un
  tetto**;
- **monotona**: `dL/dx = exp(-LAM/x) * (1 + LAM/x) > 0` ovunque ✓;
- **zero coefficienti**: c'e' solo `LAM` ✓ (par.3);
- **stress finito**: `d0 > LAM` e `d > LAM` **per costruzione**, quindi
  **`stress = |d - d0| / d0 < |d - d0| / LAM`**, finito finche' `d` e' finito ✓.

**⚠ E DICHIARO CIO' CHE LA DERIVAZIONE *NON* FISSA:** i criteri sopra sono soddisfatti **anche** da
`L(x) = sqrt(x^2 + LAM^2)`, che ha **le stesse asintotiche** *(errore `LAM^2/2x^2`, identico)*.
**La scelta fra le due NON e' forzata dai criteri.** Ho preso la prima perche' la distorsione e'
minore dove il sistema vive davvero *(a `x = LAM`: `1.368 LAM` contro `1.414 LAM`; a `x = 3 LAM`:
`+3.6 %` contro `+5.4 %`)* **e perche' `exp(-LAM/x)` e' una soppressione a CORTO RAGGIO con l'unica
scala del sistema, lo stesso carattere di `filtro_portata = 1 - tanh(d/LAM)` gia' cablato.**
**Se questa forma si comportasse male, l'alternativa e' quella, e non serve cercarne altre.**

### ⚠ E CIO' CHE LA FORMA COSTA, scritto PRIMA di vederlo
**Non esiste un pavimento liscio che non gonfi anche il corpo della distribuzione.** A `x = 3 LAM`
la lunghezza sale del **3.6 %**; a `x = 0.3 LAM` sale da `0.3 LAM` a **`1.011 LAM`**, cioe'
**3.4 volte**. **Il mandato lo mette in conto** *(«sposta fino a meta' degli archi. E' voluto»)*,
**e va letto come una RIFONDAZIONE delle lunghezze, non come una correzione.**

### DOVE SI APPLICA — **una sola legge per TUTTE le lunghezze**
| sito | oggi | con `SCALA_MIN` |
|---|---|---|
| i **sette** pavimenti di `d0` | `_floor_d0()` = `f * median(d0)`, comovente | `L(d0)` |
| `d` nel mezzo passo Verlet | `max(d + dts*vd_half, 0.05)` | `L(d + dts*vd_half)` |
| `d` nel passo di Eulero | `max(d + dts*vd, 0.05)` | `L(d + dts*vd)` |
| **i tronconi `d/2` alla mitosi** | `max(0.5*|dpos|, 0.05)` | `L(0.5*|dpos|)` |

> **DICHIARATO, come il mandato chiede: alla mitosi NON c'e' nessuna regola di arresto nuova.**
> **I tronconi passano per la STESSA `L`, perche' una lunghezza e' una lunghezza.**

---

## 3. DERIVAZIONE DI `COES_ADIM` — **le dimensioni, e cosa resta aperto**

### Cosa c'e' oggi, e perche' non torna
```
coesione = (CS_M^2 / I_med) * (forza_campo + richiamo) * filtro_portata * d0^2 * (I_arco / I_med)
forza_campo = -( dI/d  -  tanh(dI/I_med) * lap_arco )
```
**`dI/d` ha dimensioni `[I]/[L]`, `lap_arco` ha `[I]`: si SOMMANO due cose diverse.** E `I_med`
compare **al quadrato** al denominatore, ed e' una **media globale** *(`A2`)*.

### La forma nuova
```
F_adim = tanh( -( dI/I_arco - tanh(dI/I_arco) * lap_arco/I_arco ) + richiamo ) * filtro_portata
d0 += passo_causale * F_adim          passo_causale = LAM * sqrt(K_C) * DT
```
- **i tre addendi sono adimensionali con la densita' LOCALE**: `dI/I_arco`, `lap_arco/I_arco`,
  e `richiamo = -(d0 - LAM)/LAM` che lo era gia' ✓;
- **`I_med` sparisce da ENTRAMBE le posizioni** ✓ — e con essa **una media globale** (`A2`);
- **`|F_adim| <= 1` PER COSTRUZIONE**: `|tanh| <= 1` e `filtro_portata = 1 - tanh(d/LAM) in (0,1)`.
  **Non e' un clip: e' la forma.** **E per questo `COES_ADIM` SOSTITUISCE il clip
  `tanh(stress)*d0`**, che `Z79` ha misurato **saturo**;
- **il fattore davanti e' lo SPOSTAMENTO CAUSALE**, lo stesso `passo_causale = c_sistema * DT` dei
  due siti fratelli *(`:5047` la spinta, `:5054` la gravita')*. **Ricalcolato in loco** e non preso
  dalla variabile di `:4990`, che sta **dentro un `if`**: usarla sarebbe stato dipendere da un ramo.

### Le due scelte su `d0^2` e `filtro_portata`, DICHIARATE
- **`d0^2` SI TOGLIE.** Con un **passo causale** davanti, lo spostamento **e' gia' una lunghezza**:
  moltiplicare per `d0^2` lo renderebbe una lunghezza **al cubo**. **Non ha una ragione
  dimensionale, e non ne aveva una prima.**
- **`filtro_portata` SI TIENE.** E' **adimensionale** e vive in `[0, 1]`, quindi **non rompe
  `|F_adim| <= 1`**; e la sua ragione **non e' dimensionale ma fisica**: dice che la coesione e' a
  **corto raggio**, sulla stessa variabile `d/LAM` di tutto il resto. **Tolto, la coesione
  agirebbe a qualunque distanza.**

### ⚠ `I_arco` NEL VUOTO — **nessun pavimento, e la ragione non e' la fiducia**
- dove `I_arco` e' **esattamente** zero, i rapporti sono `0/0` e si **definiscono ZERO**, come e'
  gia' stato fatto e dichiarato per `scala_p` in **`Z67`**. **Precedente di questo repo, zero
  parametri;**
- dove `I_arco` e' **minuscolo ma non nullo** *(il caso vero: `I ~ 1e-7`)*, il rapporto puo' essere
  enorme — **e non serve un pavimento, perche' il `tanh` lo limita a `1`.**
  **La limitatezza e' STRUTTURALE, non messa a mano.** **E' esattamente il motivo per cui la forma
  nuova non ha bisogno del numero che la vecchia avrebbe richiesto.**

### ⚠ COSA RESTA APERTO, e lo dichiaro invece di coprirlo
**`tanh` di una quantita' adimensionale e' lecito; ma `passo_causale * tanh(...)` fissa la
MAGNITUDINE dello spostamento al passo causale, non a una forza.** **Non ho una derivazione che
dica perche' la coesione debba muovere `d0` di ESATTAMENTE un passo causale quando `F_adim`
satura.** **Il mandato lo prevede** *(«usa la forma senza, e DICHIARA che le dimensioni restano
aperte in quel punto»)*: **il tetto causale e' un LIMITE giusto — niente puo' muoversi piu' in
fretta del cono — ma usarlo come SCALA della forza e' una scelta, non una derivazione.**

---

## 4. COSA MI FA FERMARE — fissato ORA

- **`Z1`** byte-identita' a **tutti e tre** i flag spenti *(simulatore e driver)* → STOP;
- **`Z2`** un flag che **non cambia niente** e' codice morto → STOP;
- **`Z3`** i criteri di `CHI_COOP` *(gia' passati 8/8, si rigirano insieme)* → STOP;
- **`Z4`** `min(d0) >= LAM` e `min(d) >= LAM`, **e lo stress massimo FINITO** → STOP;
- **`Z5`** `|delta d0|` da quel sito **sempre `<= passo_causale`** → STOP;
- **`Z6`** tutti accesi: nessun `NaN`, nessun `inf`, tutte le lunghezze pari a `n` → STOP;
- **`Z7`** il sigillo interno della rigiocata.

**⚠ E UN CONTROLLO POSITIVO PER OGNUNO**: `Z2` chiede **tre** effetti, uno per flag, **da soli**.
Un sigillo di sola byte-identita' passerebbe anche su codice morto (par.10.2).

---

## 5. TODO

- [x] fermare tutto, pulito — **niente girava**
- [x] `CHI_COOP` (modifica ①), sigillato **8/8**
- [ ] `SCALA_MIN`: `L(x)`, i sette pavimenti di `d0`, i due di `d`, i tronconi della mitosi
- [ ] `COES_ADIM`: la forma nuova accanto alla vecchia, sotto flag
- [ ] driver `--scala-min`, `--coes-adim` (con `--chi-coop` gia' fatto), tutti `off`
- [ ] INVENTARIO / README / FISICA nello stesso commit
- [ ] **commit PRIMA dei sigilli**
- [ ] `Z0`-`Z7`
- [ ] ramo D: `sep = 4.0`, 3000 passi, archivio `_ab_D`, componenti = 1, disco riportato prima
- [ ] letture **contro i criteri ASSOLUTI**, **nessun confronto con A/B/C**
