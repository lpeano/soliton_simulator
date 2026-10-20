# LA PROVA DI RAFFINAMENTO SULL'INSTABILITA' DELLA MATERIA UNIFORME

> **Il mandato:** decisione di Luca del `2026-10-20`, `11:05`-`11:26`. ### **La risposta di
> principio** *(mappa, sotto `L1`)*: ### **la griglia del simulatore e' un campionamento
> grossolano della scala di Planck, e i risultati fisici sono quelli che CONVERGONO raffinando.**
> ### **La regola di scala:** valori per nodo invariati, `dtau` proporzionale al passo della
> griglia, stessa scena fisica. ### **Nessun codice di fisica: una misura.** ### **`LINEARE`,
> `Lambda_c`, ogni lettura «alla Jeans» o di «instabilita' di modulazione», e la misura dello
> stato finale restano FERMI fino all'esito.**

**LIVELLO CORRENTE:** `L2`.

## 0. LA STELLA POLARE

1. **`A14`:** ### **nessuna legge cambia.** Si misura ### **se l'instabilita' della materia
   uniforme converge raffinando**, cioe' se e' della fisica o della griglia.
2. **Il gradino:** `(a)` le barre fra blocchi con la `t` di Student coi gradi veri, il braccio
   `0` ### **al bit** contro `9018188b`; `(b)` ### **`R2` toglie `cs`**; `(c)` ### **non si
   applica.** ### **E `TAGLIA-FINITA`: TRE risoluzioni**, non due.
3. **Aggiunge un numero o una legge?** ### **No.** Le risoluzioni, i `dtau` e il budget sono
   ### **parametri della misura**, e ### **i `dtau` si derivano dalla regola di scala**, non si
   scelgono.
4. **Tocca `rho`, `c_s` o il segno?** ### **Misura** `rho` e `Lambda`, con `cs` acceso *(`R1`)*
   e spento *(`R2`)*.
5. **Emergente o imposto?** ### **E' la domanda:** un fenomeno che segue la griglia ### **e'
   imposto dal campionamento**, non emergente dalla fisica.

## 1. RAGIONAMENTO PRELIMINARE — cosa credo, e cosa NON so

- **Cosa credo:** il modo dominante a `k` circa `pi` con `cs` acceso, e la mancanza di una lunghezza minima, ### **somigliano a un artefatto** *(previsione `A`)*. ### **Ma `I2`** *(`cs` spento)* ### **cresce a `(8,0)`, lambda `3.88`**, che ### **non e' la scala di Nyquist**: li' non ho un'attesa.
- ### ⚠ **COSA NON SO, E CHE PUO' CONFONDERE IL VERDETTO:** ### **`31` e' DISPARI, `62` e `124` sono PARI.**
  - Su un toro di lato pari ### **il modo a scacchiera `k = pi` esiste ESATTAMENTE** *(indice `L/2`)*;
  - ### **su `31` no**: il piu' vicino e' `15/31`, e la scacchiera e' ### **frustrata** dal giro del toro.
  - ### **Quindi un modo a `k = pi` puo' comportarsi diversamente a `62` e `124` per la PARITA', e non per la risoluzione.** ### **Lo dichiaro prima**, e il referto stampa ### **`k` in unita' di `pi`** per ogni risoluzione.
- **Non so il costo** a `124`: lo dichiaro sotto.

## 2. PROGETTAZIONE

**Lo strumento:** `csv/_raffinamento.py`. ### **Riusa** `scena_l2.scena` *(con `lati`)*, `statica_protocollo.chi_allineato`, `_instabilita_vuoto` *(`gamma_del_tratto`, `onda`)*, `_jeans_del_modello` *(`gamma_k`, `t_soglia`)*.

### LE TRE RISOLUZIONI *(`TAGLIA-FINITA`)*

| lato | `dtau` | il passo della griglia `a` *(in unita' di quello a `31`)* | nodi | tick per lo stesso tempo |
|---|---|---|---|---|
| `31` | `0.125` | `1` | `961` | `8000` |
| `62` | `0.0625` | `1/2` | `3844` | `16000` |
| `124` | `0.03125` | `1/4` | `15376` | `32000` |

- ### **STESSA REGIONE FISICA:** `lato * a = 31` sempre.
- ### **LA REGOLA DI SCALA** *(punto `2` del mandato)*: ### **valori per nodo invariati** *(`x 0.1`: `rho_k` e `Lambda_k` come a `31`, `Lambda_c = Lambda_m`, rapporto `1`)*; ### **`dtau` proporzionale ad `a`.**
- **La materia uniforme col solo rumore d'arrotondamento**, costruita come in `29b997da` *(`psi = sqrt(x) chi_allineato`)*.
- ### **IL TEMPO FISICO:** `1000` *(`tick * dtau`)*, come `9018188b`; ### **l'arresto** quando `max|delta rho|` supera il `10%` di `rho_m` *(non tocca il fit, che usa il tratto fino all'`1%`)*.

### I BRACCI

| | `x` | `cs` |
|---|---|---|
| `R1` | `0.1` | ### **acceso**, rapporto `1` |
| `R2` | `0.1` | ### **spento** |

- ### **IL BRACCIO `0`:** a `31` la serie `max|delta rho|` di `R1` e di `R2` ### **deve coincidere AL BIT** con quella di `I1 x 0.1 dtau 0.125` e di `I2 dtau 0.125` in `doc/referti_l2/instabilita_dtau_piccolo.jsonl` *(`9018188b`)*, sui tick percorsi. ### **Se no: STOP.**
  - ⚠ **Qui NON si calcolano i termini di `H` a ogni tick** *(in `9018188b` si')*: ### **il bit-a-bit prova anche che quella osservazione non toccava la dinamica.** Si calcola `G` *(`g_dello_stato`)* come in `29b997da`.
- **`M1`:** l'equilibrio al tick `0`, entro `256` ulp, a ogni risoluzione.
- ### **Se il punto fisso di `cs` non converge, si registra e il braccio si chiude li', senza cure.**

### LA MISURA, per ogni braccio e risoluzione

- ### **la lunghezza d'onda del modo che cresce** *(`onda` alla fine del tratto)*: ### **IN ARCHI e IN UNITA' FISICHE** *(`archi * a`)*, e `k` in unita' di `pi`; per `rho` e per `Lambda`;
- ### **gamma** per tick e ### **nel tempo fisico** *(il tempo proprio: `gamma / (dtau cs_m)`)*;
- ### **la lunghezza minima:** il `lambda` piu' corto *(archi e fisico)* il cui `gamma(k)` supera la soglia di Student; ### **se crescono tutti gli anelli, NON ESISTE.**

### LE DUE PREVISIONI, che si escludono *(scritte prima)*

**Partendo dal `lambda` in archi misurato a `31`** *(in `9018188b`: `R1` `rho` `2.21`, `Lambda` `1.46`; `R2` `3.88`)*:

| | `lambda` in archi a `62` / a `31` | a `124` / a `31` | `lambda` fisico | gamma nel tempo fisico |
|---|---|---|---|---|
| ### **`F` FISICA** | ### **`2`** | ### **`4`** | lo stesso | lo stesso |
| ### **`A` ARTEFATTO** | ### **`1`** | ### **`1`** | si dimezza a ogni raffinamento | *(nessuna previsione)* |

- ### **IL VERDETTO, letto da queste previsioni** *(fissato qui)*: ### **`F` se il rapporto e' sopra la media geometrica delle due previsioni a ENTRAMBE le risoluzioni** *(`sqrt 2 = 1.41` a `62`, `2` a `124`)*; ### **`A` se e' sotto a entrambe**; ### **altrimenti «misto»**, e si riportano i numeri.
- ### **Con tre punti NON si fa un test di significativita'** *(errore `n.21`)*, e ### **lo dichiaro qui.** Le barre di gamma *(Student a `4` gradi, `6.62`)* servono solo a dire ### **se il braccio e' instabile.**
- ### **Si riporta anche** il rapporto di gamma nel tempo fisico *(`F` prevede `1`)*, e la lunghezza minima.

### IL COSTO, dichiarato prima

- ### **A `124` i nodi sono `16` volte e i tick `4` volte quelli a `31`:** `64` volte il lavoro per tick-nodo. A `31` *(`9018188b`)* `I1 x 0.1` costava `28` s fino all'arresto, `I2` `3` s.
- ### **IL BUDGET: `4` ore di orologio per braccio.** ### **Se un braccio lo supera, si riporta dove e' arrivato e ci si FERMA, senza ridurre la prova.**

### ⛔ **COSA MI FA FERMARE:** il braccio `0` che non riproduce `9018188b`; `M1` che cade; il budget superato *(si riporta)*.

## 3. TODO DEL NEXT STEP

1. Questo task history, con la risposta di principio, la regola di scala e l'errore `n.22`: commit e push ### **PRIMA del codice.**
2. `csv/_raffinamento.py` e la voce nell'inventario: ### **un commit a se'.**
3. La corsa dal blob committato e pulito, in background: `python csv/_raffinamento.py > doc/referti_l2/raffinamento.txt`, bracci salvati in `doc/referti_l2/raffinamento.jsonl`.
4. Il referto e la relazione: un commit, `PUSHATO`, e ### **`FERMO`** *(il verdetto e' una lettura delle previsioni; il seguito e' di Luca)*.
