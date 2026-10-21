# `D0`: LA BANDA DI `S3` E' UNA RISONANZA FRA LA CAMMINATA E IL RITMO DI `S3`?

> **Il mandato:** decisione di Luca del `2026-10-21` alle `09:22`, la prima domanda di `c82b51dd`.
> ### **Una DIAGNOSI: nessuna cura, nessun codice di fisica.** Impronta `2e7f795d2a52fbe7` e
> `leggi.yaml` intatti. ### **`csv/_stabilita_lineare.py` (blob `3e054285`) si ESTENDE con
> `--risonanza`; i modi esistenti AL BIT.**

**LIVELLO CORRENTE:** `L2`.

## 0. LA STELLA POLARE

1. **`A14`:** ### **non si applica**: nessuna legge cambia, si misura la dispersione della camminata
   e la crescita di `S3`.
2. **Il gradino:** `(a)` ### **il caso permutato** *(deve fallire)* e ### **la riproduzione di
   `594417f6`** *(deve riuscire)*; `(b)` e `(c)` ### **non si applicano**: e' una diagnosi, non un
   risultato da far reggere a una legge tolta.
3. **Aggiunge un numero o una legge?** ### **No.** La tolleranza `1` passo di `k` ### **e' del
   mandato.**
4. **Tocca `rho`, `c_s` o il segno?** ### **Non si applica:** `cs` e' spento *(`R2`)*.
5. **Emergente o imposto?** ### **Non si applica:** si cerca ### **il meccanismo** della banda.

## 1. RAGIONAMENTO PRELIMINARE

- **Le grandezze, dichiarate prima:**
  - ### **`omega_a(k)`, la dispersione della camminata:** la camminata sola *(senza
    `CAMM-MATERIA-VUOTO`, `cs` spento)* e' ### **LINEARE IN SENSO COMPLESSO**, quindi la sua mappa
    di un tick su una cella e' ### **una matrice `12 x 12` complessa `A(k)`** *(`8` componenti di
    `psi` sulle `4` estremita', `4` di `phi`)*, calcolata ### **esatta** *(impulsi di ampiezza `1`
    su una base nulla, come `braccio_c2_esatto`)*. ### **I suoi autovalori sono
    `exp(-i omega_a(k) dtau)`, `a = 1..12`.** ### **Le `24` fasi reali del mandato sono
    `{omega_a(k)}` piu' `{-omega_a(-k)}`** *(la rappresentazione reale di una mappa complessa)*: ###
    **le condizioni si scrivono con le `12` complesse**, che non perdono niente.
    - ### **LA CONVENZIONE DEI RAMI:** `omega` nell'intervallo `(-pi/dtau, pi/dtau]`, ### **in
      ordine crescente a ogni `k`** *(le fasi ordinate sono continue in `k`)*; ### **psi e phi non
      si mescolano nella camminata sola**, quindi i rami sono ### **`8` della materia e `4` del
      vuoto**, e lo strumento li separa.
    - ### **Le condizioni valgono modulo `2 pi / dtau`** *(Floquet: un passo discreto)*: il
      residuo si riporta in `(-pi/dtau, pi/dtau]`.
  - ### **`Omega_p`, la POMPA:** lo stato uniforme e' ### **una combinazione di autovettori di
    `A(0)` della MATERIA**; si decompone la cella del tick `0` e ### **si tengono le fasi con peso
    `> 1e-6` della norma.** ### **La precessione dell'elicita'** *(`69094682`)* ### **e' la
    differenza fra due di queste.**
  - ### **`nu = nu_S3(x) = Lambda^2 / (rho + Lambda)^2`** *(`c38367db`)*, ### **dalla stessa corsa**
    *(`rho_m`, `Lambda_m` per nodo)*. ### **Stesse unita' di `omega`:** fase per unita' di tempo
    *(a `cs` spento `dtau_nodo = dtau`)*.
- ### **UNA COSA CHE NON METTO, e il perche':** la rotazione uniforme di `S3`, `alpha dtau` su `psi`
  e `beta dtau` su `phi`, ### **sposta la pompa E le bande laterali della stessa quantita'**, e ###
  **nelle condizioni si cancella** *(e' una fase comune)*. ### **Cio' che resta e' l'accoppiamento,
  cioe' `nu`.**

## 2. LA LISTA CHIUSA DELLE CONDIZIONI *(scritta PRIMA dei numeri; nessuna si aggiunge dopo)*

| | la condizione | il perche' |
|---|---|---|
| `K1` | ### **`omega_a(k) - omega_b(k) = +- nu`**, `a != b` | ### **interbanda allo stesso `k`:** `S3` accoppia due rami *(anche materia-vuoto: `alpha` e `beta` leggono `rho` e `Lambda`)* col suo ritmo |
| `K2` | ### **`omega_a(k) - omega_b(k) = +- 2 nu`** | il multiplo di `K1` |
| `K3` | ### **`omega_a(k) + omega_b(-k) - Omega_p - Omega_q = +- nu`** | ### **le bande laterali di un'instabilita' di modulazione:** due quanti della pompa diventano la coppia `k`, `-k`, spostata dal ritmo non lineare |
| `K4` | ### **`omega_a(k) + omega_b(-k) - Omega_p - Omega_q = +- 2 nu`** | il multiplo di `K3` |
| `K5` | ### **`omega_a(k) + omega_b(-k) - Omega_p - Omega_q = 0`** | ### **l'accordo di fase senza spostamento** -- ### **non dipende da `nu`**, quindi ### **non puo' seguire un massimo che si sposta** *(`F4` del documento delle cure)*: ### **e' un controllo dentro la lista** |
| `K6` | ### **`omega_a(k) - omega_b(k) = +- (Omega_p - Omega_q)`** | ### **la precessione della pompa come modulazione periodica** *(`69094682`)*. ### ⚠ **Il perche' e' DEBOLE:** `S3` legge solo `rho` e `Lambda`, che sullo stato uniforme ### **non oscillano** con la precessione *(l'elicita' si rovescia, `rho` no)*. La metto perche' il mandato la nomina. |

- **`a`, `b`** su tutti i `12` rami; **`p`, `q`** su tutte le coppie della pompa *(anche `p = q`)*.

## 3. IL CRITERIO *(fissato dal mandato, con la lettura dichiarata)*

- ### **Il `k` del massimo di `gamma`**, lungo `(m, 0)` e lungo `(m, m)`, `m = 1..16` *(`k = 0` escluso:
  e' un transitorio, `594417f6`)*.
- ### **Il `k` di risonanza di una condizione:** su ogni retta, ### **gli `m` dove il residuo di una
  combinazione cambia segno** fra `m` e `m + 1` *(senza attraversare il salto di `2 pi / dtau`: si
  conta solo se `|r(m)| + |r(m+1)| < pi/dtau`)*, con l'incrocio interpolato. ### **La distanza** e'
  la piu' piccola fra il massimo e gli incroci, ### **in passi di `k`** *(`pi / 16` a lato `32`)*.
- ### **UNA CONDIZIONE TIENE** se, ### **a TUTTI E TRE gli `x`** e ### **su ENTRAMBE le rette**, la
  distanza e' `<= 1`. ### **Una sola che tiene: `D0` TIENE. Nessuna: `D0` CADE. Piu' d'una: NON
  DECIDIBILE**, con le distanze stampate.
- ### ⚠ **LA LARGHEZZA, dichiarata:** con `12` rami e tutte le coppie, ### **una condizione puo'
  avere incroci dappertutto** e tenere per caso. ### **E' per questo che c'e' il caso permutato.**
- ### **DEVE FALLIRE:** ogni condizione che tiene, ### **col `nu` PERMUTATO fra gli `x`** *(le due
  permutazioni cicliche: il `nu` di `x 1` a `x 0.01`, quello di `0.01` a `0.1`, quello di `0.1` a `1`;
  e l'altra)*, ### **NON deve tenere.** ### **Se tiene anche permutata: il criterio e' troppo largo →
  STOP.** *(`K5` non dipende da `nu`: se tenesse, terrebbe anche permutata, e ### **sarebbe STOP**.)*
- ### **DEVE RIUSCIRE:** `R2` a `x 0.1` ### **ridà le pendenze di `594417f6`** *(`0.407` a `~0.5 pi`)*
  ### **entro `1e-3`**, su tutti i `k`, per i due stimatori.
- ### **E i modi esistenti AL BIT:** senza argomenti *(`c38367db`, `R2` lato `31`)* e `--lungo`
  *(`16b5d10f`, `R2` lato `32`)*.

## 4. LE MISURE

- **a)** ### **la dispersione `omega_a(k)`** a lato `32`, `dtau 0.125`, per ogni `k`; stampata lungo
  `(m, 0)` e `(m, m)`, per ramo.
- **b)** ### **`gamma(k)` di `R2`** con la base proiettata, `N dtau 100`, lato `32`, ### **a `x` in
  `{0.01, 0.1, 1}`**: ### **la pendenza della seconda meta', stimatore della NORMA** *(`594417f6` l'ha
  mostrato stabile)*; `nu` dalla stessa corsa. ### **Costo:** `~130` s per `x` *(`594417f6`)*.
- **Il grafico:** ### **opzionale, e non lo faccio** in questo giro *(il referto stampa le curve)*.

## 5. TODO

1. Questo task history, ### **committato DA SOLO.**
2. `--risonanza` in `csv/_stabilita_lineare.py` e l'inventario: ### **un commit a se'.**
3. La corsa dal blob committato: `python csv/_stabilita_lineare.py --risonanza > doc/referti_l2/d0_risonanza.txt`, con `.jsonl`.
4. Il referto, la relazione, ### **e nel documento delle cure la correzione per `C1`** *(conta `f(k)^2 >= 0`; il «segno rovesciato» non vale per `C1`)*: un commit.
