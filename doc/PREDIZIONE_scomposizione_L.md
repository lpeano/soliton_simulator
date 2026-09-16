# PREDIZIONE — da dove viene la crescita di `L_tot`?

> **Scritta PRIMA di calcolare la scomposizione.** 2026-09-16, blob **`c57800c1`** (byte grezzi
> verificati, 0 CRLF). Branch `fork-su2`. **Nessun run nuovo, nessuna modifica alla fisica.**

---

## 0. ⚠ PRIMA DI TUTTO: LA SCOMPOSIZIONE COME E' POSTA **NON E' CALCOLABILE** DAI DATI COMMITTATI

Il mandato chiede `A` e `B` **sui soli intervalli senza nascite** (`n` invariato fra due campioni).
**Verificato dai dati: quegli intervalli NON ESISTONO.**

```
base_OFF_s1   n per campione: 80, 1883, 2759, 3072, 3253, 3364, 3453, 3534, 3606, 3675, 3790
base_OFF_s2   n per campione: 80, 1853, 2131, 2299, 2417, 2486, 2513, 2567, 2637, 2717, 2800
base_ON_s1    n per campione: 80, 1912, 2644, 3002, 3149, 3275, 3392, 3475, 3574, 3664, 3773
base_ON_s2    n per campione: 80, 1916, 2243, 2442, 2545, 2641, 2735, 2801, 2860, 2929, 3054

intervalli SENZA nascite fra campioni consecutivi: 0 su 10, in TUTTI E QUATTRO i run.
```

**Perche':** il CSV campiona **ogni 50 passi**, e in 50 passi nascono sempre nodi. I passi
birth-free **esistono** — sono 87-152 per run, ed e' da li' che viene il numero `dL/L senza
nascite` del referto — **ma sono contati DENTRO il run**, in `serie_L`, e **solo il loro aggregato**
finisce nel CSV. **La serie per-passo non e' persistita.**

> **Quindi: o si fa un run nuovo (che il mandato vieta), o si risponde alla stessa domanda con i
> dati che ci sono. Faccio la seconda, e dichiaro cosa cambia.**

**COSA SI PUO' FARE CON I DATI COMMITTATI, e risponde alla STESSA domanda:**
sui **11 campioni** di ogni run ci sono `L_tot`, `n`, **`fdt_inerzia_mediana`** (l'inerzia mediana,
fattore `cs^-2` incluso) e **`fdt_om_mediana`** (`|omega|` mediano). Quindi si puo' scomporre la
crescita **dell'intensita' per nodo**:

```
L_tot ~ n * <I * |omega|>        =>     d log(L/n)  =  d log(I)  +  d log(|omega|)   ( + termine misto )
                                          \_ TERMINE A _/   \_ TERMINE B _/
```

**E' la stessa domanda — «cresce l'inerzia o cresce omega?» — a risoluzione di CAMPIONE invece che
di PASSO, e senza il filtro birth-free.** **Cosa perdo, detto ora:** non posso separare
l'effetto delle nascite da quello della crescita intensiva **all'interno** di un intervallo. **Cosa
NON perdo:** il rapporto `A/B`, che e' la cosa che le due letture del mandato distinguono.

**E il controllo §3.2 del mandato — `L_tot/n` e la mediana di `I*|omega|` — e' calcolabile
ESATTAMENTE**, senza approssimazioni: e' la separazione fra **AGGREGAZIONE** e
**INTENSIFICAZIONE**, e non richiede intervalli birth-free.

---

## 1. LE TRE LETTURE, fissate ORA

| esito | lettura |
|---|---|
| **DOMINA B** (`I * Delta\|omega\|`) | **e' `omega` che cresce**: qualcosa **pompa momento angolare** in modo continuo. La direzione successiva sarebbe **cercare la sorgente** |
| **DOMINA A** (`\|omega\| * Delta I`) | **e' l'INERZIA che cresce**: il campo **si sta accendendo**. **`L_tot` non sarebbe una violazione, ma un sistema che non ha finito di accendersi**, e la domanda diventa *«`L_tot` si conserva A REGIME?»* |
| **A ~ B** | terzo caso: si riporta e ci si ferma |

**NON si sceglie la lettura prima del numero.** Le due portano in direzioni opposte — una a cercare
una sorgente, l'altra ad aspettare il regime.

---

## 2. LA MIA PREDIZIONE, con la ragione e il falsificatore

> ### **Predico che DOMINI A: l'inerzia.**

**Perche', e sono fatti gia' nel repo:**
1. **`Lam` cresce di NOVE ORDINI in 150 passi**: `7.45e-14` al passo 1 -> `1.32e-4` al passo 150
   (`doc/INERZIA_massa_o_frazione.md:83`, *«il campo si sta accendendo, non e' a regime»*).
   **⚠ E qui correggo il mandato:** quel numero **non** sta in **C4** (che e' `inerzia = T^2`) ne'
   in **C5** (che e' `d/cs e' piatto`). **Il fatto e' vero, la citazione no.**
2. **E continua dopo:** nella baseline `Lam` vale **`7.68e-3` al passo 500**, cioe' **~58 volte**
   il valore di 150 passi. **L'accensione non era finita a 150 e non e' finita a 500.**
3. **`ramp = min(1, eta/TAU_A)`** (`:2321`) raggiunge il pieno solo a **`eta = TAU_A = 50`**, cioe'
   **~5000 passi**: a 500 passi il sistema ha vissuto **un decimo** della propria maturazione.
4. **L'inerzia mediana ha appena lasciato il pavimento:** `2.29e-6` contro il floor `1e-6`. Fino a
   poco fa era **incollata al floor** (§9: il pavimento attivo sul 99.7 % dei nodi), quindi ogni
   suo aumento e' **crescita vera**, non rumore.

**IL FALSIFICATORE, esplicito:** se `d log(|omega|)` fosse **confrontabile o maggiore** di
`d log(I)`, la mia predizione cade, e con essa l'idea che `L_tot` sia solo transitorio.
**In quel caso la crescita e' una SORGENTE, e va cercata** — e il primo sospettato sarebbe il
**taglio spettrale**, che ho cablato oggi con la predizione esplicita *«`theta` non scende, e se si
muove SALE»*. *(Nota: nella baseline il flag e' **OFF**, quindi non puo' essere lui. Ma se `omega`
crescesse **anche** col flag spento, sarebbe un fatto indipendente da quel cablaggio.)*

---

## 3. E COSA QUESTO CALCOLO NON POTRA' DIRE, in nessun caso

- **nulla sui passi birth-free in particolare**: la separazione `con/senza nascite` del referto
  resta un fatto misurato, ma la sua **scomposizione** richiede la serie per-passo, che **non e'
  nei dati**. Se dopo questo calcolo servisse ancora, **si dira' che serve un run**, non si
  fingera' di averlo fatto;
- **nulla su «violazione della conservazione»** se domina A: **un sistema che si accende non e' un
  sistema che viola.** La conservazione si giudica **a regime**, e il regime non c'e';
- **nulla sul turbo**, che resta **non lanciato** finche' questo non e' chiuso.

---

## 4. LA MINIMA COSA CHE CHIUDEREBBE DAVVERO LA DOMANDA (non fatta, dichiarata)

Persistere `serie_L` **per passo** (passo, `n`, `L_tot`, `sum(I)`, `sum(|omega|)`) in un CSV a
parte. E' **una riga di scrittura** nell'osservatore, **zero fisica**, e renderebbe la
scomposizione `A`/`B` **esatta e ristretta agli intervalli birth-free** al prossimo run —
**senza lanciarne uno apposta**.
