# L'ANALISI DI STABILITA' LINEARE ESATTA DELLO STATO DI MATERIA UNIFORME

> **Il mandato:** decisione di Luca del `2026-10-20` alle `12:32`, sul verdetto `A` della prova
> di raffinamento *(`83edbaa7`)*. ### **Prima di qualunque cura, il conto.** ### **Nessun codice
> di fisica: un conto, che non cambia il modello.** ### **`LINEARE`, `Lambda_c`, le letture «alla
> Jeans» o di modulazione, e lo stato finale restano FERMI.**

**LIVELLO CORRENTE:** `L2`.

**IL FATTO** *(`83edbaa7`)*: il modo che cresce resta ### **FISSO IN ARCHI** raffinando *(`R1`: la scacchiera esatta `(pi, pi)` sulle griglie pari; `R2`: circa `0.52 pi`)*, mentre ### **gamma nel tempo fisico resta lo stesso** *(`R1` `0.450`, `0.434`, `0.437`; `R2` `0.371`, `0.355`, `0.343`)*. **La lettura del guardiano, scritta come tale:** l'instabilita' insegue la griglia, quindi non e' fisica per la regola di Luca; ma il ritmo costante dice che nell'automa iperfine ### **si presenterebbe alla scala di Planck con lo stesso ritmo**: un difetto della legge `S3` alla scala piu' corta. ### **Ipotesi, non provata:** come nelle equazioni di Schroedinger discrete con non linearita' locale forte, tutta la banda e' instabile e il massimo cade alla scala della griglia.

## 0. LA STELLA POLARE

1. **`A14`:** ### **nessuna legge cambia.** Il conto dice ### **quale termine genera la crescita**,
   e la camminata sola ### **deve conservare la norma di ogni modo** *(il caso che deve fallire)*.
2. **Il gradino:** `(a)` il conto ### **riproduce le misure** *(il caso che deve riuscire)*, con
   la linearita' verificata a due ampiezze; `(b)` ### **la scomposizione toglie `cs` e
   `CAMM-FASE-VUOTO`**; `(c)` ### **il limite noto e' il caso lineare** *(autovalori di modulo
   `1`)*.
3. **Aggiunge un numero o una legge?** ### **No.** Le ampiezze, l'intervallo e le bande sono
   ### **parametri del conto**, dichiarati qui.
4. **Tocca `rho`, `c_s` o il segno?** ### **Misura** come `S3` e `cs` accoppiano le
   perturbazioni di `rho` e `Lambda`, ### **nei due versi.**
5. **Emergente o imposto?** ### **E' la domanda:** quale legge produce la crescita, e se la
   produce ### **a ogni `k`.**

## 1. RAGIONAMENTO PRELIMINARE

- **LETTO DAL SORGENTE, prima di scrivere il conto:**
  - ### **lo stato dinamico e' `psi_h` e `phi_h`** *(le estremita')*; `rho`, `Lambda`, `h_int`, `psi` sono ### **cache per nodo**. ### **Se il passo ne dipendesse, sarebbero memoria**, e il conto lineare dovrebbe includerle: ### **lo strumento lo verifica** *(`P1` sotto)*;
  - ### **`S3`** *(`materia_vuoto.applica`)* ruota la fase di `psi` di `alpha(rho, Lambda) dtau_nodo frazione` e quella di `phi` di `beta(rho, Lambda) dtau_nodo frazione`, con `alpha = ln(rho/(rho+Lambda)) + Lambda/(rho+Lambda)`, `beta = -rho/(rho+Lambda)`: ### **l'unica non linearita' della camminata a `cs` spento** *(`CAMM-FASE-VUOTO` e' l'identita' a `cs` spento)*;
  - ### **la cella:** il nodo `v` con i suoi `2` archi `(v, asse)`, arco `k = 2v + asse`, estremita' `2k` e `2k+1` *(`corrente.toro`, `scena_l2.versori_geometrici`)*: ### **`4` estremita', `12` complessi, `24` reali.** Il nodo `v` sta a `(v // L, v % L)`.
- **Cosa credo:** che la crescita venga da `S3` *(`C2` di `9018188b` non cresce senza)* e che ### **sia larga in `k`** *(nessuna lunghezza minima)*.
- **Cosa NON so:** se il massimo di gamma cade a `(pi, pi)` per una ragione semplice, e ### **se lo stato uniforme e' un'orbita periodica** a `dtau 0.125` *(la precessione dell'elicita' a `0.5` aveva periodo `2` tick; a `0.125` non lo so)*.

## 2. PROGETTAZIONE

**Lo strumento:** `csv/_stabilita_lineare.py`.

### IL METODO, dichiarato prima

- ### **La mappa tangente NUMERICA, per FUNZIONE DI GREEN di un tick:** lo stato uniforme e' invariante per traslazione, quindi ### **il tick linearizzato e' una CONVOLUZIONE** sulle celle. ### **Per ognuna delle `24` coordinate reali della cella `0`**, si perturba lo stato di base di `eps_j` e si fa ### **UN tick**; la risposta `(tick(base + eps e_j) - tick(base)) / eps_j` su tutte le celle e' ### **la colonna `j` della funzione di Green.** ### **La sua trasformata di Fourier da' le matrici `24 x 24` complesse `R_t(k)` per TUTTI i `k` insieme.**
  - ### ⚠ **E `k` e `-k` NON si mescolano in questo modo:** nelle variabili REALI la mappa e' una convoluzione reale, ### **diagonale in `k`**, con `R(-k) = conj(R(k))`. L'accoppiamento `k`/`-k` che il mandato nomina ### **e' gia' dentro**: e' la parte antilineare della mappa complessa, ### **che nelle variabili reali e' lineare.**
  - ### **Differenze in avanti**, perche' a `124` le centrali raddoppierebbero un costo gia' di ore. ### **La linearita' si verifica con due ampiezze** *(sotto)*.
  - **L'ampiezza:** `eps_j = eps_rel * scala`, con la scala ### **il modulo massimo del campo** *(`psi_h` o `phi_h`)* nello stato di base; ### **`eps_rel = 1e-7`**, e la seconda ampiezza ### **`1e-6`**.
- ### **L'ORBITA:** lo stato uniforme ### **NON e' un punto fisso** del passo, e' un'orbita *(la precessione dell'elicita', `69094682`)*. ### **Si linearizza LUNGO l'orbita:** a ogni tick la base avanza di un tick, e la funzione di Green si ricalcola sulla base di quel tick.
  - ### **L'INTERVALLO: `N` tick con `N dtau = 25`** *(`200` a `dtau 0.125`, `400` a `0.0625`, `800` a `0.03125`, `100` a `0.25`)*;
  - ### **la monodromia `M(k) = R_N(k) ... R_1(k)`**, e ### **`gamma(k) = ln |autovalore massimo| / (N dtau cs_m)`**: il tempo proprio, ### **la stessa normalizzazione dei referti** *(`cs_m = 1` a `cs` spento)*;
  - **informazione, non criterio:** lo stesso gamma su `N/2`.
- ### **L'invarianza per traslazione della base** si stampa a ogni corsa *(la deviazione massima fra celle, in ulp)*.

### `P` — LE PROVE DEL METODO *(se una cade: STOP)*

- **`P1`, nessuna memoria nelle cache:** un tick dallo stato di base con le cache *(`rho`, `Lambda`, `h_int`, `psi`)* ### **azzerate** da' `psi_h` e `phi_h` ### **AL BIT** come con le cache intatte, con `cs` acceso e spento.
- **`P2`, LA LINEARITA':** a lato `31`, `dtau 0.125`, `R1` e `R2`: ### **`max_k |gamma_(1e-7)(k) - gamma_(1e-6)(k)| <= 1e-3 * max_k gamma`.** *(La banda `1e-3` e' una tolleranza del conto, dichiarata qui.)*

### IL CASO CHE DEVE FALLIRE: LA CAMMINATA SOLA *(`C2`: senza `CAMM-MATERIA-VUOTO`, `cs` spento)*

- ### **Il passo senza `S3` e' LINEARE**, quindi la sua funzione di Green ### **si calcola esatta** *(impulso di ampiezza `1` su una base NULLA, nessuna differenza)*: ### **ogni autovalore deve avere `|ln |lambda|| <= N * 64 ulp`, per ogni `k`.**
- **Informazione:** lo stesso con le differenze sulla base uniforme, ### **cioe' il pavimento del metodo** *(cio' che il metodo da' dove la crescita e' zero)*.

### IL CASO CHE DEVE RIUSCIRE *(lato `31`, `dtau 0.125`, `x 0.1`)*

- ### **`max_k gamma(k)` riproduce gamma misurato** in `9018188b`/`83edbaa7` *(letto dal `jsonl`, non ricopiato)*: ### **`R1` `0.450`, `R2` `0.371`**, ### **entro `t * barra`** *(la `t` di Student a `4` gradi, `6.62`: la banda al `99.73%` usata in tutti i referti di oggi)*; si stampa anche la distanza in barre semplici.
- ### **E il `k` del massimo cade dove cadono i modi misurati:** ### **i `k` misurati** *(`R1`: `(14, 0)` per `rho` e `(15, 15)` per `Lambda`; `R2`: `(8, 0)`, letti dal `jsonl`)* ### **hanno `gamma(k) >= max gamma - t * barra`**, cioe' stanno ### **fra i modi di crescita massima entro la banda.**

### LA SCOMPOSIZIONE, a lato `31`

| | che cosa | `cs` | salta |
|---|---|---|---|
| `(a)` | ### **`S3` sola** *(e' `R2`)* | spento | niente |
| `(b)` | con `cs` *(e' `R1`)* | acceso | niente |
| `(c)` | ### **senza `CAMM-FASE-VUOTO`** | acceso | `CAMM-FASE-VUOTO` |

- ### **`x` in `{0.01, 0.1, 1}`** per `(a)` e `(b)`: il massimo di gamma, e ### **il `k` dove cade**;
- ### **il numero di Courant:** `dtau` in `{0.25, 0.125, 0.0625}` a griglia fissa, per `(a)` e `(b)`;
- ### **IL RAPPORTO DEI RITMI, dichiarato qui:** il ritmo della non linearita' di `S3` e' ### **`nu_S3 = rho d(alpha)/d(rho) = Lambda^2 / (rho + Lambda)^2`** *(la variazione della frequenza di `psi` per variazione relativa di `rho`; per unita' di `dtau_nodo`)*; il ritmo del salto fra nodi e' ### **`OMEGA_H = pi`** *(il coefficiente dei generatori di Grover e di hop, per unita' di `dtau`)*. ### **Si riporta `nu_S3 / OMEGA_H`** per ogni `x`, ### **e se il `k` del massimo si sposta con lui.**

### L'INVARIANZA DI RAFFINAMENTO, controllo di coerenza

- **`(a)` e `(b)` a lato `62`** *(`dtau 0.0625`, `N 400`)* e **`124`** *(`dtau 0.03125`, `N 800`)*, con la regola di scala di Luca.
- ### **`max_k gamma` riproduce gamma misurato in `83edbaa7`** a quella risoluzione, ### **entro `t * barra`** *(letto dal `jsonl`)*.
- ### **E la curva `gamma(k)` in funzione di `k` IN ARCHI**: ### **sui `k` comuni alle tre griglie** *(i `k` di `31`)*, si riporta ### **la differenza massima** fra le curve. ### **Nessuna soglia sulla curva:** ### **non saprei derivarla**, e lo dichiaro.
- ### **IL COSTO:** a `124`, `25` tick per passo dell'orbita *(`24` perturbati e la base)* per `800` passi: ### **circa `1.4` ore per braccio** a `0.25` s per tick *(la prova breve di `14a0b02b`)*. ### **Budget `4` ore per braccio: oltre, si riporta e ci si FERMA.**

### ⛔ **NESSUNA CURA.** Se il conto suggerisce un tipo di cura *(un termine che renda «cari» i modi corti, come il termine di Wilson che da' massa ai doppioni; una `S3` che legga la densita' mediata sui vicini)*, ### **lo si scrive come DOMANDA PER LUCA, coi numeri. Ogni cura tocca una legge.**

### ⛔ **COSA MI FA FERMARE:** `P1`, `P2`, il caso che deve fallire o quello che deve riuscire che cadono; il budget superato.

## 3. TODO DEL NEXT STEP

1. Questo task history e ### **l'osservazione nella mappa sotto `L2`** *(il verdetto `A` e il ritmo invariante; `D4` da rileggere)*: commit e push ### **PRIMA del codice.**
2. `csv/_stabilita_lineare.py` e la voce nell'inventario: ### **un commit a se'.**
3. Il conto dal blob committato e pulito, in background: `python csv/_stabilita_lineare.py > doc/referti_l2/stabilita_lineare.txt`, con `gamma(k)` per ogni braccio in `doc/referti_l2/stabilita_lineare.jsonl`.
4. Il referto e la relazione: un commit, `PUSHATO`, `FERMO`.
