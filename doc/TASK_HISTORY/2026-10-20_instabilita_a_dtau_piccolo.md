# L'INSTABILITA' DELLA MATERIA UNIFORME, RIFATTA A `dtau 0.125`

> **Il mandato:** decisione di Luca del `2026-10-20` alle `10:27`, sullo STOP di `69094682`.
> **Il verdetto della scala del salto e' `P2`**, letto dalle previsioni numeriche fissate prima
> *(task history `2026-10-20_controllo_passo_materia_uniforme.md`, sez.`2-ter`)*: ### **il salto
> di `H` sulla materia uniforme e' un errore ordinario del passo, nel termine della moneta, che
> va come `dtau^2`.** ### **Nessun codice di fisica: una misura.** ### **`LINEARE`, `Lambda_c` e
> ogni lettura «alla Jeans» restano FERMI fino all'esito.**

**LIVELLO CORRENTE:** `L2`.

## 0. LA STELLA POLARE

1. **`A14`:** ### **nessuna legge cambia.** Si misura a quale `dtau` il passo conserva `H` sulla
   materia uniforme entro la banda `B`, ### **e se l'instabilita' resta li'.** Le serie
   dell'energia separate dicono ### **dove va l'energia** mentre la perturbazione cresce.
2. **Il gradino:** `(a)` le barre fra blocchi con la `t` di Student coi gradi veri, ### **la
   riproduzione al bit di `D3` di `29b997da`** come controllo dello strumento, due `dtau`;
   `(b)` ### **`C2` toglie `S3`**, `I2` toglie `cs`; `(c)` ### **non si applica.**
3. **Aggiunge un numero o una legge?** ### **No.** `dtau 0.125` ### **si DERIVA dalla misura**
   *(sotto)*; la durata e la soglia di arresto sono ### **parametri della misura**, dichiarati qui.
4. **Tocca `rho`, `c_s` o il segno?** ### **Misura** come `rho` e `Lambda` uniformi reagiscono al
   rumore, con `cs` acceso *(`I1`)* e spento *(`I2`, `C2`)*: ### **i due versi insieme.**
5. **Emergente o imposto?** ### **E' la domanda di `C2`:** se senza `S3` non cresce, la crescita
   ### **nasce dall'accoppiamento materia-vuoto**, e non dalla camminata.

## 1. RAGIONAMENTO PRELIMINARE — cosa credo, e cosa NON so

- ### **IL `dtau`: `0.125`**, perche' li' ### **l'escursione relativa di `H` sulla materia uniforme e' l'`1.0%`** *(`19.747 / 1937.18`, `scala_salto.txt`, `x 0.1`)*, ### **sotto la banda `B = 3.1%`**; a `0.25` e' il `4.2%` *(`81.984 / 1937.18`)*, ### **sopra.** Gli stessi bracci a `dtau 0.25` si riportano ### **accanto, per confronto.**
  - ⚠ **la banda e' letta a `x 0.1`**: a `x 0.01` e `x 1` l'escursione relativa ### **non l'ho misurata** *(lo strumento la stampa)*.
- **Cosa credo:** `D3` di `29b997da` aveva gia' dato ### **gamma in tempo proprio uguale a `dtau 0.5` e `0.25`** *(`0.469` contro `0.468`)*: ### **mi aspetto che l'instabilita' resti a `0.125`.** Il salto della moneta e' ### **uniforme** *(a `k = 0`)*, e l'instabilita' cresce ### **a `k` circa `pi`**: non vedo un legame diretto.
- **Cosa NON so:**
  - ### **se la camminata da sola** *(`C2`)* **cresce**;
  - se l'energia di materia e di vuoto ### **si compensano** mentre il modo cresce;
  - quanti giri costa il punto fisso di `cs` a `dtau 0.125`, e se converge.

## 2. PROGETTAZIONE

**Lo strumento:** `csv/_instabilita_dtau_piccolo.py`. ### **Riusa** `_jeans_del_modello` *(`scena`, `gamma_k`, `t_soglia`)*, `_instabilita_vuoto` *(`gamma_del_tratto`, `onda`)*, e `_scala_salto.termini` *(i termini di `H`, gia' verificati al bit)*.

### I BRACCI *(materia uniforme, SOLO rumore d'arrotondamento, rapporto `Lambda_c / Lambda_m = 1`)*

| | il braccio | `cs` | che cosa salta | `x` |
|---|---|---|---|---|
| `C2` | ### **la sola camminata** | spento | ### **`CAMM-MATERIA-VUOTO`** | `0.1` |
| `I1` | l'instabilita' di `29b997da` | ### **acceso** | niente | ### **`0.01`, `0.1`, `1`** |
| `I2` | lo stesso | ### **spento** | niente | `0.1` |

- ### **Ciascuno a `dtau 0.125` e a `dtau 0.25`**: `10` bracci.
- ### **LA DURATA: lo stesso tempo totale di `29b997da`**, `tick * dtau = 1000` *(`8000` tick a `0.125`, `4000` a `0.25`)*.
  - ### **L'ARRESTO ANTICIPATO, dichiarato qui:** il braccio si ferma ### **quando `max|delta rho|` supera il `10%` di `rho_m`**. Il fit usa ### **solo il tratto fino all'`1%`** *(`IV.SOGLIA_PICCOLA`)*, quindi ### **l'arresto non lo tocca**, e risparmia la parte non lineare. ### **Non e' un parametro fisico.**
  - ### **Se il punto fisso di `cs` non converge, il braccio si chiude li'** *(tick, `Lambda` min)*, senza cure.

### `P0` — LE PROVE *(se una cade: STOP)*

- ### **`P0a`, il controllo dello strumento:** `I1` a `x 0.1`, `dtau 0.25` ### **e' `D3` di `29b997da`**. ### **La sua serie `max|delta rho|` deve coincidere AL BIT** con quella del `jsonl` *(`D3 dtau 0.25`)*, sui tick che il braccio percorre.
- **`P0b`, i termini:** a ogni tick, `per_nodo` e `per_arco` ricostruiti da `_scala_salto.termini` ### **coincidono al bit** con `termini_di_h`.
- **`M1`** *(come in `29b997da`)*: la variazione di `rho` e `Lambda` nel ### **primo tick** entro `256` ulp della scala.

### LE MISURE, per ogni braccio

- ### **gamma** di `rho` e di `Lambda`, ### **in tick e in tempo proprio** *(`gamma / (dtau cs_m)`, `cs_m = 1` a `cs` spento)*;
- ### **il modo dominante** *(`k`, lunghezza d'onda)*, e ### **`k = pi` o no**;
- ### **la lunghezza minima:** il `lambda` piu' corto il cui `gamma(k)` supera la soglia; ### **se crescono tutti gli anelli, NON ESISTE**;
- ### **la deriva di `G` nella SOLA fase esponenziale** *(fino a `max|delta rho| = 1%` di `rho_m`)*, come rapporto con `max|delta rho| / rho_m`;
- ### **LE SERIE DELL'ENERGIA SEPARATE, a ogni tick** *(richiesta di Luca)*:
  - ### **MATERIA** = i termini di `psi`: nodo `psi` + arco `psi` *(norma e incrocio)*;
  - ### **VUOTO** = i termini di `phi`: nodo `phi` + arco `phi` *(norma e incrocio)*;
  - ### **SCAMBIO** = la moneta `eps h` + `N`;
  - accanto a `G` *(`g_dello_stato`)*. ### ⚠ **Con `cs` acceso `G` e' PESATA, e le tre parti NO:** la loro somma e' `H` non pesata, ### **e non deve coincidere con `G`.**
  - ### **SE LE PARTI SI COMPENSANO:** alla fine della fase esponenziale si riporta `|D_mat + D_vuoto + D_scambio| / (|D_mat| + |D_vuoto| + |D_scambio|)` *(le variazioni da tick `0`)*: ### **`0` = compensazione esatta, `1` = nessuna.** ### **Si riporta il numero, senza soglia.**
- **`gamma` contro `x`** *(`I1`)*: i rapporti e la pendenza in `log x`.

### LE SOGLIE

- ### **«instabile» se `gamma >= t_(99.73%, 4) * barra`** *(`5` blocchi, `4` gradi: `6.62`)*, come in `29b997da`.
- ### **Il confronto fra i due `dtau` in tempo proprio:** la barra combinata `sqrt(b1^2 + b2^2)` e la stessa soglia *(conservativa: i gradi di Welch sono almeno `4`)*.
- ### **DOVE I PUNTI SONO TROPPO POCHI PER UN TEST, LO DICHIARO QUI:** ### **`gamma` contro `x` ha `3` punti**: ### **nessun test**, si leggono i numeri *(i rapporti e la pendenza)*.

### LA LETTURA, fissata qui

- ### **`C2` SE CRESCE: il difetto e' nella camminata. SE NON CRESCE: l'instabilita' nasce dall'accoppiamento `S3`**, e si riporta su quale modo cresce in `I2`.
- ### **`I1`/`I2` a `0.125` contro `0.25`:** gamma in tempo proprio coincide entro la soglia, oppure no. ### **Nessuna lettura oltre questa:** ne' «alla Jeans», ne' una legge che stabilizzi.

### ⛔ **COSA MI FA FERMARE:** `P0a`, `P0b` o `M1` che cadono.

## 3. TODO DEL NEXT STEP

1. Questo task history *(con la relazione, l'annotazione del verdetto `P2` e la domanda nella mappa sotto `L1`, nello stesso commit)*: commit e push ### **PRIMA del codice**.
2. `csv/_instabilita_dtau_piccolo.py` e la sua voce nell'inventario: ### **un commit a se'.**
3. La corsa dal blob committato e pulito, in background: `python csv/_instabilita_dtau_piccolo.py > doc/referti_l2/instabilita_dtau_piccolo.txt`, coi bracci salvati in `doc/referti_l2/instabilita_dtau_piccolo.jsonl` mentre corrono.
4. Il referto e la relazione: un commit, `PUSHATO`, e ### **`FERMO`** *(le letture sono di Luca)*.
