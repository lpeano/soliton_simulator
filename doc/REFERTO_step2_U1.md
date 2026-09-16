# REFERTO — LO STEP 2 CONTRO SE STESSO SPENTO: la predizione regge, **ma per meta' delle osservabili il test non aveva potenza**

> **2026-09-16.** Branch `fork-su2`, blob **`a44adc31`** (coincide con `HEAD:soliton_simulator.py`).
> **8 run, 500 passi, 4 semi appaiati per braccio, `--cs-dinamico` acceso.** 8/8 `rc=0` in 53.8 min.
> Driver `csv/_test_fork/_campagna_step2.py` (`eb34245`), contrasto `_contrasto_step2.py`.
> **Predizione e soglia committate PRIMA:** `doc/PREDIZIONE_step2_U1.md` (`b7cb537`).
> Prerequisito: sigillo di purezza dell'osservatore con MISURA U **6/6 PASS**.

---

## 0. IL VERDETTO IN TRE RIGHE

> 1. **Nessuna delle 11 firme di SPIN esclude lo zero. Il CRITERIO DI RETROCESSIONE NON scatta:**
>    lo Step 2 **non organizza lo spin**, che e' esattamente cio' che il suo messaggio dichiara.
> 2. **Nessuna delle 5 osservabili U(1) esclude lo zero.** Il debito contratto con la promozione
>    (*«le conseguenze sul settore U(1) sono da misurare»*) e' **saldato con un risultato negativo**.
> 3. **⚠ MA il «contiene lo zero» NON vale uguale per tutte:** su `chi` la risoluzione e' lo
>    **0.21 %**, su `|<n>|` e' il **129 %** e sulla coerenza di segno il **603 %**. **Dove la barra
>    e' piu' larga del valore, il test non ha misurato niente** — e dirlo e' obbligatorio.

---

## 1. IL DISEGNO, e perche' i semi sono APPAIATI

I due bracci girano sugli **stessi quattro semi**, quindi la differenza si prende **seme per seme**
(`Delta_k = ON_k - OFF_k`) e l'IC95 si costruisce sui **quattro `Delta`**, con `t(0.025,3) = 3.182`.
E' piu' potente del confronto fra medie indipendenti, perche' **il seme fissa la condizione
iniziale**, e i due bracci divergono solo per la variabile in esame.

**Variabile unica:** `--senza-step2` contro il default. `TAU_LUCE=0`, `TW_SPINORE=0`, `CS_DIN=1`,
tutto il resto identico — **verificato dalle colonne dei CSV, non dal nome dei file** (P6).

---

## 2. FIRME DI SPIN — **0 su 11 escludono lo zero**

| osservabile | `Delta` (ON − OFF) | IC95 | esito |
|---|---|---|---|
| chi medio TUTTI | −0.03502 gradi | ±0.1918 | contiene lo zero |
| chi medio MATERIA | −0.03901 | ±0.1748 | contiene lo zero |
| chi medio p90 | −0.09805 | ±0.2785 | contiene lo zero |
| chi std TUTTI | −0.02063 | ±0.09954 | contiene lo zero |
| frazione chi < 10 gradi | −1.924e-04 | ±3.969e-04 | contiene lo zero |
| `|<n>|` TUTTI / MATERIA / p90 | +0.00228 / +0.00019 / +0.0266 | ±0.0224 / ±0.0306 / ±0.0302 | contengono lo zero |
| spin overlap d'arco | +2.458e-04 | ±1.573e-03 | contiene lo zero |
| `|omega_s|` mediana | −1730 | ±5218 | contiene lo zero |
| theta giri/passo | −1.773 | ±8.625 | contiene lo zero |

> ### **IL CRITERIO DI RETROCESSIONE NON SCATTA.**
> Era scritto **al momento della promozione**: *«torna a flag se una firma di SPIN si muove per lo
> Step 2 oltre la dispersione fra semi»*. **Nessuna si muove.** La promozione **regge**, e regge
> **per la ragione giusta**: `_phc` moltiplica `a1` e `b1` per lo **stesso** fattore (`:2212-2213`,
> uniche occorrenze), quindi `nb = psi^dag sigma psi` e' **invariante per fase globale**.
> **Non e' fortuna: e' la proprieta' su cui la promozione poggiava, ed e' stata messa alla prova.**

---

## 3. SETTORE U(1) / EM — **0 su 5 escludono lo zero**

| osservabile | `Delta` | IC95 |
|---|---|---|
| `|Re<canon|psi>|` | +8.479e-04 | ±0.01524 |
| coerenza SEGNO d'arco | +1.625e-03 | ±5.931e-03 |
|  … materia-materia | +4.229e-03 | ±7.531e-03 |
|  … p90 | −2.143e-03 | ±4.718e-03 |
| coerenza VERSO *(nullo ignoto)* | +0.1213 | ±0.1759 |

**Il debito della promozione e' saldato, e la risposta e' negativa:** lo Step 2 **non muove** le
osservabili U(1) misurabili entro la risoluzione di questo test.

---

## 4. ⚠ LA COSA PIU' IMPORTANTE DEL REFERTO: **«contiene lo zero» NON VALE UGUALE PER TUTTE**

Un risultato nullo si legge **solo** insieme alla risoluzione che lo ha prodotto. Altrimenti e'
la versione statistica del `max|A-B| = 0.000e+00` per **mancanza di confronto** (§9).

| osservabile | IC95 | valore ON | **risoluzione** | il nullo dice… |
|---|---|---|---|---|
| chi medio | 0.00335 rad | 1.572 | **0.213 %** | **molto** |
| chi std | 0.00174 rad | 0.6837 | **0.254 %** | **molto** |
| spin overlap | 0.00157 | 0.4997 | **0.315 %** | **molto** |
| `|omega_s|` | 5218 | 7.749e+04 | **6.73 %** | qualcosa |
| n nodi | 366.2 | 3315 | **11 %** | poco |
| `Lam` | 0.00393 | 0.01114 | **35.3 %** | poco |
| **`|<n>|`** | 0.02236 | 0.01735 | **129 %** | **NIENTE** |
| **coerenza segno** | 0.00593 | 9.837e-04 | **603 %** | **NIENTE** |

> **Tradotto in limiti superiori, che e' la forma onesta di un risultato negativo:**
> lo Step 2 **non sposta `chi` di piu' di 0.19 gradi**, ne' lo spin overlap di piu' di 0.0016,
> ne' `|omega_s|` di piu' del 6.7 %. **Su `|<n>|` e sulla coerenza di segno non si sa nulla:**
> la barra e' **piu' larga del valore stesso**, e la colonna «contiene lo zero» li' e' **vuota**,
> non rassicurante.

**Perche' la barra e' cosi' larga proprio li':** sono grandezze il cui valore **e' gia' il nullo**
(`|<n>|` = il Bloch medio di versori casuali, coerenza di segno = 0). **Una quantita' che vale zero
non puo' avere un `Delta` piccolo in percentuale.** Servirebbero **molti piu' semi**, non piu' passi.

---

## 5. UN CONTROLLO CHE VALE, E UNA LACUNA STRUTTURALE

**Il controllo:** `max|fatt_cs - 1|`, `cs_std` e `frazione oltre l'1 %` **non differiscono** fra i
bracci — ed e' **giusto cosi'**, perche' `fatt_cs` e' il fattore `(CS_M/cs)^2` dell'**inerzia**,
cablato come **correzione di difetto** e **non** gated su `STEP2_OROLOGIO`. **I due bracci sono
identici in tutto tranne l'orologio**, e i controlli lo confermano.

> ### ⚠ LA LACUNA: **nessuna colonna misura l'orologio DIRETTAMENTE.**
> Cercate `clk`, `orolog`, `fase`, `phc` fra le 256 colonne: **nessuna**. Questa campagna misura le
> **CONSEGUENZE** dell'orologio su spin e U(1) — mai `omega_clk` stesso. Quindi il nullo su U(1)
> **non dice che l'orologio non e' cambiato**: dice che **cio' che sappiamo misurare non se ne
> accorge**. E l'orologio **e' cambiato**: il `10.8 %` dei nodi ha `|fatt_cs - 1| > 1 %`.
> **La minima cosa che chiuderebbe il punto:** una colonna con la mediana di `|omega_clk|` e la sua
> dispersione. **Una riga di scrittura nell'osservatore, zero fisica.**

---

## 6. COSA QUESTO REFERTO NON DICE

1. **Non dice che lo Step 2 «non faccia nulla».** Dice che **non organizza lo spin** — che e' cio'
   che il suo messaggio dichiara — e che le osservabili U(1) **che abbiamo** non lo vedono.
2. **Non dice nulla a regime.** 500 passi sono **un decimo** della maturazione (`ramp` pieno a
   ~5000). Un non-effetto a 500 passi non e' un non-effetto **mai**.
3. **Non dice nulla sul tempo-luce:** `--tau-luce` e' escluso di proposito (sigillo **fallito**).
4. **Non assolve le altre tredici componenti:** restano senza sigillo e restano spente.
5. **Non chiude `u1_verso_arco_coer`:** il suo nullo **non e' verificato** (`nb_grav` e' una media
   di vicinato, quindi due nodi adiacenti sono correlati **per costruzione**). Resta muta.

---

## 7. E DUE COSE DA CORREGGERE NELL'OSSERVATORE, ora che la campagna e' finita

1. **`u1_segno_ov_nullo` scrive `2/pi = 0.6366`, che e' SBAGLIATO.** `canon` viene da `_nb_grav()`,
   una direzione **diversa** da quella del nodo, quindi il nullo e' `(2/3)*(2/pi) = 0.42441`
   (Monte Carlo: 0.424474). **I CSV gia' scritti portano il valore sbagliato** e non lo
   acquisiranno: va annotato, non riscritto a memoria (§9).
2. **Aggiungere la colonna dell'orologio** (§5), che e' la lacuna vera di questa campagna.

*(Nessuna delle due si poteva fare durante i run: l'osservatore era in uso — §5.)*
