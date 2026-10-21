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

## 4-bis. ANNOTAZIONE DEL `2026-10-21`, `10:00`, PRIMA DEL CODICE: `D0` RIFATTO COL RILEVATORE CORRETTO *(decisione di Luca sullo STOP di `ac9d0d7d`; si annota, non si riscrive)*

- **a) ERRORE `n.28` DEL GUARDIANO:** ### **il caso permutato e' un test VUOTO per le condizioni che non dipendono da `nu`** *(`K5`, `K6`)*: ### **non possono fallire per costruzione.** Il permutato ha funzionato ### **per caso**, facendo emergere la degenerazione *(`C.5`)*.
- **b) IL RILEVATORE NUOVO, fissato qui:**
  - ### **DEGENERAZIONE:** una combinazione con residuo ### **IDENTICAMENTE nullo** -- `|r(m)| <= 64` ulp della sua scala ### **su TUTTI gli `m` di un asse** *(la scala: il massimo, sugli `m`, della somma dei valori assoluti dei suoi termini)* -- ### **si esclude, e si stampa come tale** *(quali rami e quali fasi della pompa, e perche' doppi)*;
  - ### **L'INCROCIO:** dove il residuo ### **cambia segno davvero** fra `m` e `m + 1` *(`r(m) r(m+1) < 0`, senza il salto di `2 pi / dtau`)*, ### **oppure vale zero in un `m` isolato** *(la combinazione non e' degenere)*;
  - ### **SPECIFICITA', per OGNI condizione e OGNI asse:** la frazione degli `m = 1..16` che stanno ### **entro `1` passo da un suo incrocio.** ### **Se supera il `20%`, la condizione e' NON INFORMATIVA su quell'asse, e non puo' «tenere».**
  - ### **Il caso permutato resta il caso che deve fallire SOLO per `K1`-`K4`** *(dipendono da `nu`)*; ### **per `K5` e `K6` il caso che deve fallire e' la specificita'.**
- **c) LA LISTA RESTA QUELLA CHIUSA** *(`K1`-`K6`)*, e ### **il criterio delle `09:22` resta com'e':** tutti e tre gli `x`, entrambi gli assi, entro `1` passo. ### ⚠ **Il guardiano segnala, senza cambiare il criterio:** sulla diagonale a `x 0.01` il massimo e' `(pi, pi)`, ### **cioe' l'altra famiglia** *(il picco)*: ### **e' per questo che `K3` cade li'** *(`1.17`)*. ### **Cambiare il criterio ora, dopo i numeri, sarebbe adattarlo ai dati: NON si fa.** ### **La lettura di `K3` «solo sulla banda» resta INFORMAZIONE.**
- **d) I CASI SINTETICI DEL RILEVATORE:**
  - ### **DEVE RIUSCIRE:** una combinazione costruita a mano col residuo `r(m) = m - 8` *(un incrocio vero a `m = 8`)*: ### **il rilevatore lo trova a distanza `0`** dal massimo a `m = 8, e con specificita' `<= 20%`** *(`3` `m` su `16`, il `18.75%`)*;
  - ### **DEVE FALLIRE:** due rami sintetici IDENTICI *(residuo nullo ovunque)*: ### **DEGENERAZIONE, non incrocio.**
- **e) LE MISURE AL BIT con `ac9d0d7d`:** `omega_a(k)` ### **al bit**, `gamma(k)` ### **entro `1e-12`**, lette dal suo `jsonl` prima di scrivere il nuovo.
- **f) INFORMAZIONE POST HOC, non verdetto** *(formulata DOPO i numeri di `ac9d0d7d`, e dichiarata tale)*: ### **la velocita' di gruppo** `d omega_a / dk` dei rami gia' misurati lungo `(m, 0)`, e dove ha il massimo.
- **Il referto nuovo:** `doc/referti_l2/d0_risonanza_bis.txt` e `.jsonl`; ### **quello di `ac9d0d7d` resta valido al suo commit.**

## 4-ter. ANNOTAZIONE DEL `2026-10-21`, `10:29`, PRIMA DEL CODICE: `D0` A LATO `64` E `128` *(decisione di Luca dopo `c8dbdd83`; si annota)*

- ### **LE TAGLIE**, dalla regola di scala di Luca: ### **lato `64` a `dtau 0.0625`, lato `128` a `dtau 0.03125`**; `N dtau 100`; `x` `0.01`, `0.1`, `1`; ### **`R2` con la base proiettata**; ### **lo stimatore della NORMA, pendenza della seconda meta'** *(come `c8dbdd83`)*.
- ### **LA LISTA CHIUSA `K1`-`K6` E IL RILEVATORE DI `acdfe5e7` INVARIATI:** degenerazioni a `64` ulp; specificita' con soglia `20%`; il permutato solo per `K1`-`K4`; ### **il criterio delle `09:22`**: tutti e tre gli `x`, entrambi gli assi, ### **entro `1` passo di `k` DI QUELLA TAGLIA** *(`pi / 32` a `64`, `pi / 64` a `128`; il massimo su `m = 1..lato/2`)*.
- ### **IL VERDETTO FRA LE TAGLIE, fissato qui:** una condizione ### **TIENE se tiene a `64` E a `128`.** ### **Se tiene a una sola taglia: NON DECIDIBILE.** ### **Se piu' condizioni tengono a entrambe: NON DECIDIBILE**, con le distanze.
- ### **IL CONFRONTO DI CONTROLLO:** lato `32` *(`c8dbdd83`)* ### **riletto dal suo `jsonl`, non rifatto.**
- ### **L'INFORMAZIONE POST HOC sulla velocita' di gruppo, a ogni taglia:** il massimo di `|v_g|` ### **dei rami dispersivi** *(quelli con `|v_g|` massimo `> 0.1`)* in unita' di `pi`, ### **accanto al massimo della banda.** ### **Resta INFORMAZIONE.**
- ### **IL BUDGET: `3` h per braccio**; se uno lo supera, si ferma e lo dichiara.
- ### **I CONTROLLI:**
  - ### **DEVE RIUSCIRE:** il caso sintetico *(un incrocio a `m = lato/4`)* a ogni taglia, ### **con la specificita' attesa** `3 / (lato/2)`: ### **`9.4%` a `64`, `4.7%` a `128`**; ### **`R2` a `x 0.1` a lato `64` coerente con `594417f6`** *(la banda `0.406`; il suo `jsonl` ha `R2 lato 64`)* ### **entro `1e-3`**;
  - ### **DEVE FALLIRE:** due rami sintetici identici: ### **DEGENERAZIONE**;
  - i modi di prima AL BIT *(`c38367db`, `16b5d10f`)*.
- ### **IL COMANDO:** `python csv/_stabilita_lineare.py --risonanza --lato 64 --dtau 0.0625` *(e `128`, `0.03125`)*; ### **senza `--lato` resta il lato `32` di `c8dbdd83`.** Il verdetto fra le taglie: `python csv/_stabilita_lineare.py --verdetto-taglie`.
- ### **I REFERTI:** `doc/referti_l2/d0_risonanza_64.txt` e `.jsonl` ### **subito**, con la frase «verdetto fra le taglie: in attesa di `128`»; poi `d0_risonanza_128.txt` e `.jsonl`; poi `d0_verdetto.txt`.

## 5. TODO

1. Questo task history, ### **committato DA SOLO.**
2. `--risonanza` in `csv/_stabilita_lineare.py` e l'inventario: ### **un commit a se'.**
3. La corsa dal blob committato: `python csv/_stabilita_lineare.py --risonanza > doc/referti_l2/d0_risonanza.txt`, con `.jsonl`.
4. Il referto, la relazione, ### **e nel documento delle cure la correzione per `C1`** *(conta `f(k)^2 >= 0`; il «segno rovesciato» non vale per `C1`)*: un commit.
