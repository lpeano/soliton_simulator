# PREDIZIONE — cosa fa lo STEP 2 al settore U(1)

> **Scritta PRIMA di lanciare la campagna.** 2026-09-16, branch `fork-su2`, blob `a44adc31`
> (byte grezzi verificati, 0 CRLF, coincide con `HEAD:soliton_simulator.py`).
> **Prerequisito bloccante gia' soddisfatto:** sigillo di purezza dell'osservatore **6/6 PASS**
> sulla versione con MISURA U (`csv/_test_fork/_sigillo_osservatore_postU.txt`), con `O1` che
> confronta **2849 nodi contro 2849** — il confronto **esiste**.

---

## 0. PERCHE' QUESTA CAMPAGNA ESISTE — un debito che ho contratto io stesso stamattina

Promuovendo `STEP2_OROLOGIO` ho scritto, nel registro:

> *«COSA QUESTA PROMOZIONE NON DICE: non dice che lo Step 2 **migliori** alcuna osservabile. Dice
> che la sua **assenza e' un difetto**. Le sue conseguenze misurabili sul settore U(1) sono ancora
> **da misurare**.»*

**Questa e' quella misura.** E c'e' un secondo motivo, verificato dai dati e non dedotto:

```
_vuoto_base_OFF_s1   passo 500   STEP2=0  TAU_LUCE=0  CS_DIN=1
_vuoto_base_OFF_s2   passo 500   STEP2=0  TAU_LUCE=0  CS_DIN=1
_vuoto_base_ON_s1    passo 500   STEP2=0  TAU_LUCE=1  CS_DIN=1
_vuoto_base_ON_s2    passo 500   STEP2=0  TAU_LUCE=1  CS_DIN=1
colonne u1_* nei dati di baseline: NESSUNA
```

> **Tutta la baseline committata ha `STEP2 = 0`.** Cioe' e' stata presa su quella che, **per nostra
> stessa decisione di oggi**, e' una fisica **amputata** rispetto al default. E non contiene nessuna
> osservabile del settore che lo Step 2 tocca. **Non e' un riferimento del sistema di default.**

---

## 1. IL DISEGNO — a variabile singola, e si puo' fare solo ora

| | |
|---|---|
| **variabile unica** | `--senza-step2` **contro** il default (Step 2 ON) |
| **semi** | **4 per braccio** — P3: con 2 semi `t(0.025,1) = 12.706`, l'IC95 e' inutilizzabile; con 4, `t(3) = 3.182` |
| **passi** | **500**, gli stessi della baseline esistente, per poterle confrontare |
| **fisso** | `--cs-dinamico` (§4, **ci va sempre**), `--fork-su2`, `--fork-su2-mem`, `--campo-spinoriale`, `--spinore-vivo`, `--spinore-corretto`, `--chi-core`, `--calore-scal`, `--deparam-orologio`, `--verlet` |
| **ESCLUSO** | **`--tau-luce`**: il suo sigillo e' **FALLITO** (voce **A** del registro). Non si mette un ramo non certificato dentro la misura che ne certifica un altro |
| **ESCLUSO** | **`--rumore-colorato`** (`N2` FAIL), **`--tw-spinore`** (voce **W**, spento per decisione), e i restanti dodici senza sigillo |

**E' l'unico test a variabile singola oggi disponibile:** con TW spento e gli altri tredici senza
sigillo, **lo Step 2 e' l'unica legge nuova accesa**, quindi un cambiamento sarebbe **attribuibile**.

---

## 2. LA PREDIZIONE, con la ragione e il falsificatore

> ### **Predico che NESSUNA firma di SPIN si muova oltre la dispersione fra semi.**
> ### **E che le osservabili U(1) o restino ai loro valori-null, o si muovano poco.**

**Perche', ed e' un fatto gia' nel repo, non una speranza:** `_phc` e' una **fase globale**.
Moltiplica `a1` e `b1` per lo **stesso** fattore (`:2212-2213`, **uniche occorrenze nel file**),
e `nb = ψ†σψ` e' **invariante per fase globale** — misurato **`3.3e-16`**. Il messaggio stesso dello
Step 2 lo dichiara: *«agisce sulla FASE (U(1)), NON sul Bloch: non organizza lo spin, e non deve.»*

**I VALORI SOTTO IPOTESI NULLA, fissati ORA** (§9: prima di leggere una statistica, chiedersi quanto
varrebbe se non ci fosse niente):

| osservabile | valore se non c'e' niente |
|---|---|
| `u1_segno_ov_absmedia` | **2/π = 0.6366** (media di `\|cos\|` uniforme) |
| `u1_segno_arco_coer` | **0** (+1 concorde, −1 alternato) |
| `u1_segno_arco_coer_materia` | **0** |
| `u1_spin_overlap_arco` | **0.5** |
| `u1_verso_arco_coer` | **0** |
| `chi` | **90.000 ± 39.171** gradi |
| `\|<n>\|` | **0.9213 ± 0.3888** |

**LA SOGLIA, scritta prima e non prorogabile** (§9: *«il criterio si scrive prima, con una soglia
numerica, e non si proroga»*): un contrasto ON−OFF conta **solo** se il suo **IC95 fra semi**
(4 semi, `t(3) = 3.182`) **esclude lo zero**. **Mai la `SE` interna al run**, che su questo sistema
e' ~3 volte troppo piccola (P3, C10).

### ⚠ IL FALSIFICATORE — e qui la predizione ha un prezzo, non e' gratis

> **Se una firma di SPIN si muovesse oltre quella barra, NON sarebbe una buona notizia: sarebbe il
> CRITERIO DI RETROCESSIONE dello Step 2 a scattare**, quello che ho scritto stamattina **al momento
> della promozione**:
>
> *«Torna a flag se un riscontro committato mostra che `_phc` NON e' una fase globale — cioe' se una
> firma di SPIN si muovesse per lo Step 2 oltre la dispersione fra semi.»*
>
> **In quel caso lo Step 2 RETROCEDE, e la promozione di stamattina si rivela sbagliata.**
> Lo scrivo qui perche' la predizione **possa costarmi**: una predizione che non puo' perdere non e'
> una predizione.

---

## 3. COSA QUESTA CAMPAGNA NON POTRA' DIRE, in nessun caso

1. **Nulla sul tempo-luce.** `--tau-luce` e' escluso di proposito: il confronto con la baseline
   esistente vale **solo** contro i suoi bracci `TAU_LUCE=0`.
2. **Nulla a regime.** A 500 passi il sistema ha vissuto **un decimo** della propria maturazione
   (`ramp` pieno a ~5000 passi, `doc/REFERTO_scomposizione_L.md`). Un **non-effetto** a 500 passi
   non e' un non-effetto **mai**.
3. **Nulla che assolva le altre tredici componenti.** Restano senza sigillo, e restano spente.
4. **Nulla sul perche' la crescita di `L_tot` stia nella CODA** e non nel nodo tipico: e' il fatto
   nuovo e non spiegato del referto precedente, e questa campagna non lo tocca.
