# IL TORNEO DELLE FORME DELLA NON LINEARITA', NEL NUCLEO *(il mandato di Luca [M1631], la decisione delle `16:31`: «niente era 3; si lavora qui, toccando il core in questo modo»; scritta PRIMA del codice)* [[PROGETTO-MITOSI]]

> **Le regole:** il nucleo si tocca SOLO cosi': le forme nuove entrano in `primo_ordine/leggi/leggi.yaml` come OPZIONI della legge CAMM-MATERIA-VUOTO *(come S1/S3)*, il modulo generato si rigenera, `alpha`/`beta`/`pezzi` di `primo_ordine/materia_vuoto.py` leggono la forma; **F0 (= S1) resta la PREDEFINITA**; la procedura di sblocco di `doc/NUCLEO_CONGELATO.md` alla lettera; il diff del nucleo contro `42638304` SOLO in `_mappa.yaml`, `motore_numba.py`, `leggi.yaml`, `termini/camm_materia_vuoto.py`, `materia_vuoto.py`; `collauda.py` a F0 AL BIT. **L'era 3 e la voce 5-ERA3 NON si scrivono.** Il resto in file nuovi; POST-HOC dichiarati; `coda_m1446` il solo lanciatore, le corse a priorita' `0`.

## 0. I PEZZI GIA' FATTI *(citati, non rifatti)*

- **1c [M1446-L2]**, le K di V2 e V3 dai quattro zeri col controllo di V2: **fatto sotto [M1446-L]** *(`doc/referti_l2/legge_zeri.py`, 4649c65b; il referto `doc/referti_l2/legge_zeri.txt`, 6d620b9d)*: fisso `1.10` = NATURA *(K -3.1 ... -3.2)*, `0` e locale = CONTRARIO; il controllo di V2 passa *(3.2e-06)*; l'ambiguita' del vuoto locale NON sciolta.
- **1a [M1446-S2]**: il codice `doc/referti_l2/spettro_gap_v3.py` *(4446bac9)*, in corsa; **1b [M1446-E2]**: `doc/referti_l2/emc2_v3.py`, dopo 1a.

## 1. LE FORME IN GARA *(S1; il generatore `N(rho, Lambda)`, `x = rho/Lambda`, `alpha = dN/drho` a `Lambda` fissa, `beta = dN/dLambda` a `rho` fissa: psi e phi accordati come S1)*

| la forma | `N/Lambda` | `alpha = dN/drho` | `beta = dN/dLambda` |
|---|---|---|---|
| **F0** *(= S1, oggi)* | `x - arctan x` | `x^2/(1 + x^2)` | `x - arctan x - x^3/(1 + x^2)` |
| **Flambda** | `lambda (x - arctan x)` | `lambda x^2/(1 + x^2)` | `lambda (x - arctan x - x^3/(1 + x^2))` |
| **FH** *(Luca 16:28)* | `x - 2 arctan x` | `(x^2 - 1)/(x^2 + 1)` | `x - 2 arctan x - x (x^2 - 1)/(x^2 + 1)` |
| **FT** | `ln cosh(x - 1) - ln cosh 1` | `tanh(x - 1)` | `ln cosh(x - 1) - ln cosh 1 - x tanh(x - 1)` |

- `lambda in {+0.5, +0.25, 0, -0.25, -0.5, -1}`; **`lambda = +1` e' F0 AL BIT** *(DEVE; `lambda * expr` con `lambda = 1.0` e' esatto in virgola mobile)*. **I nomi nella tabella:** `S1` *(F0)*, `S3`, `L+0.5`, `L+0.25`, `L0`, `L-0.25`, `L-0.5`, `L-1`, `FH`, `FT`.
- **I limiti a `Lambda = 0`** *(come S1: «il LIMITE, non un pavimento»)*: Flambda `lambda` volte quelli di S1; **FH** `alpha -> 1`, `beta -> -pi` *(`x - 2 arctan x - x(x^2-1)/(x^2+1) -> -2 (pi/2) = -pi`)*, `N -> rho`; **FT** `alpha -> 1`, `beta`: `ln cosh(x - 1) - x tanh(x - 1) -> -1 - ln 2 ... - ln cosh 1` *(il limite di `ln cosh(y) - (y + 1) tanh(y)` per `y -> inf` e' `-ln 2 - 1`)*: `beta -> -1 - ln 2 - ln cosh 1`, `N -> rho - Lambda(...)` -> `rho`. **Da controllare nel codice coi casi noti** *(`a rho = 0 nulla`: `alpha(0) = 0` per F0, Flambda; **FH `alpha(0) = -1`, FT `alpha(0) = tanh(-1)`**: ### ⚠ **a `rho = 0` la fase su psi e' `e^{+i dtau f}` (FH) o `e^{-i tanh(-1) dtau f}` (FT), ma psi = 0: «a rho = 0 nulla» vale perche' psi = 0, e `beta(0) = 0` per tutte** *(`N(0)/Lambda = 0` e `x alpha(x) -> 0`)*: **il vuoto da solo AL BIT, da provare**.

## 2. S1-bis: lambda = -1 COME IL CAMMINO CONIUGATO *(da provare, 1d)*

- **L'affermazione** *(del guardiano)*: `lambda = -1` e', a meno della coniugazione dello stato, **il cammino libero CONIUGATO** *(`theta -> -theta` nel Grover e nello spostamento, `a -> -a` nella moneta; nella convenzione simmetrica `P <-> I - P`)* **con la non linearita' di oggi**: l'inversione temporale del cammino libero rispetto all'interazione.
- **La prova** *(1d, in memoria, `L 16`, ogni `k`)*: **la matrice del tick intero linearizzato a `rho` fissata** con `N_{-1}`, contro **il complesso coniugato** della matrice con `N` *(F0)* e `theta`, `a` rovesciati: **entro `1e-12`**. ### ⚠ **Prima di scriverla devo trovare nel nucleo dove stanno `theta` e `a`** *(i pezzi del palindromo: `camm_grover`, `camm_spostamento`, la moneta)* **e se si possono rovesciare in memoria senza toccare file** *(un contesto come `forma_esplicita`)*: **lo scrivo nella sez. 6 quando l'ho letto, prima del codice.** **DEVE PASSARE prima delle corse di Flambda.**

## 3. S2: LA SEMINA

- **`alpha > 0` nel cuore** *(F0, `lambda > 0`, e FH, FT a `rho > Lambda`)*: **alla CIMA, come oggi** *(lo stampo `L162_MGU_03000`)*.
- **`alpha < 0` nel cuore** *(`lambda < 0`)*: **al FONDO** *(il `k` del minimo da 1a; se degenere, tutti i `k` come casi)*: **la stessa forma di partenza, la portante spostata** *(`psi -> psi e^{i k_fondo . x}` e la componente del fondo: la definizione esatta dopo 1a, nella sez. 6)*.
- **`lambda = 0`:** tutte e due.
- **Il caso noto:** la semina al fondo con F0 **NON deve reggere** *(se regge, detto per primo)*.

## 4. S4: DUE DOMANDE SEPARATE

- **(D1) il segno della gravita':** la massa *(il calcio, `m*_sol`)*, l'orologio *(Nm/Np in V2 e V3)*, la caduta *(V2 e V3)*.
- **(D2) la dipendenza dalla fase:** la coppia a `d 35` in fase e in antifase *(`Delta a` col segno, il Pound-Rebka, l'alone di phi a `r 30-40`)*.

## 5. LA PROCEDURA DEL NUCLEO, E UNA DOMANDA A LUCA *(prima del passo 3)*

- **La procedura di `doc/NUCLEO_CONGELATO.md`** *(«Come si sblocca»)*: «Solo con una decisione SCRITTA di Luca: questo file passa a `stato: SBLOCCATO` con una riga `decisione_di_luca: <data, ora, il testo o il riferimento>`»; **il presidio `H-NUCLEO-CONGELATO`** *(`csv/_nucleo_congelato.py`)* **agisce SOLO sul ramo `primo-ordine`**; **dopo**, si ricongela *(come la riunione di numba: sbloccato per il commit, ricongelato nel commit dopo le suite)*.
- ### ⚠ **LA DOMANDA:** **su quale ramo va il nucleo?** **Tutto il lavoro di oggi** *(il tick con `chi`, la caduta, gli orologi, la coda)* **sta sul ramo `lapse-u`** *(`C:\Users\lpeano\wt_lapse_u`)*: **le corse del torneo leggono il nucleo di QUEL worktree.** **Se le forme vanno sul `primo-ordine`** *(dove il presidio e la procedura valgono)*, **il `lapse-u` non le vede senza un merge** *(che senza mandato non faccio: R-NAVI)*. **Se vanno sul `lapse-u`**, il presidio non agisce *(guarda il nome del ramo)*, e «la procedura alla lettera» vuol dire scrivere `SBLOCCATO` con la riga di Luca nel `NUCLEO_CONGELATO.md` del `lapse-u`, poi ricongelare. **E in ogni caso il nucleo di `wt_lapse_u` non si tocca finche' le corse della coda lo usano** *(le cadute di Eotvos e la corsia F, fino alle `~18:20`: par. 5 di CLAUDE.md)*. **FERMO prima del passo 3 finche' Luca non sceglie.**

## 6. LE DEFINIZIONI CHE DIPENDONO DA 1a E DAL CODICE *(si aggiungono qui PRIMA del codice che le usa)*

*(vuota: il k del fondo da 1a; theta e a nel nucleo per 1d)*

## 7. I CRITERI, L'ALBERO E LE PREVISIONI *(copiati dal mandato)*

- **K1** casi noti: 1d entro `1e-12`; `collauda.py` e la ripresa a F0 al bit; `lambda = 1` al bit *(sha1 a `100` tick)*; a `rho = 0` nulla *(il vuoto da solo al bit)*; la semina al fondo con F0 NON regge *(se regge, dirlo per primo)*; 1a ridà `d2E/dk2 -0.059` e `v_max 0.588 s` entro l'`1%`.
- **K-T** tenuta: `w` a `k 3000` entro `+-30%` di `w` a `k 500`; nessuna frammentazione *(un solo massimo connesso sopra il `10%` del picco)*.
- **K-D1** per forma e per collegamento *(V2, V3)*: «NATURA» = orologio che rallenta dove `N` cala *(`(q - 1)/(N - 1) > 0`)* E caduta VERSO `N` basso. **LA FORMA GIUSTA** e' quella che da' NATURA in almeno un collegamento con `m*_sol > 0` e `K_i/K_th` entro il `20%`.
- **K-D2** per forma: il segno di `Delta a` in fase e in antifase: «UNIVERSALE» *(attrazione in tutte e due)*, «ROVESCIATA» *(in fase respinge, in antifase attrae)*, «COME OGGI».
- **K-buco:** nessun `lambda` con `|lambda| < 0.25` regge; se uno regge, dirlo per primo.
- **K-Dirac:** «VALE» se il fit rifatto regge entro il `5%` su `|k| < 0.3` con lo stesso `c` sui due rami, per almeno un gap attorno alla materia.
- **L'ALBERO:** **(i)** Flambda a `lambda < 0` regge con `m* > 0` e da' NATURA in V2 o V3: la cura e' IL SEGNO; la forma candidata `lambda = -1` *(o il `lambda < 0` piu' stabile)*; FH/FT per D2. **(ii)** nessuna forma con `alpha < 0` nel cuore regge: il fondo non ospita solitoni con questa semina; i passi dentro l'era 2 si propongono a Luca, non si fanno. **(iii)** regge con `m* > 0` ma NON da' NATURA: la legge `a = -grad omega/m*` cade al fondo, o il collegamento al lapse va rifatto per `m* > 0`; FERMO con la tabella. **(iv)** FH o FT: D2 ROVESCIATA o UNIVERSALE con D1 come oggi: fase e segno problemi SEPARATI.
- **LE PREVISIONI DEL GUARDIANO:** **P1** K1 passa `85%`; 1d passa `85%`. **P2** il buco c'e' `80%`; `|lambda|` minimo dalla cima `0.25-0.5` `50%`, dal fondo piu' grande `55%`. **P3** `lambda = -1` regge `55%`; se regge: `m*_sol > 0` `85%`, `omega` fra `-0.65` e `-0.60` `65%`; V2 NATURA `70%`; V3 il contrario di oggi `70%`; `K_i/K_th` entro il `20%` `75%`. **P4** FH regge `70%`, piu' compatta `65%`, `m*_sol < 0` `75%`, caduta V2 VIA `75%`, coppia in fase ROVESCIATA `55%`, alone di phi cambia segno `50%`; FT come FH `70%`. **P5** 1a: K1-S passa con la griglia fine `70%`; K-Dirac NON VALE `65%`. 1c: fisso `1.10` = natura, `0` e locale = contrario `85%` *(### vera: 6d620b9d)*. **P6** l'albero finisce in (i) `45%`, (ii) `30%`, (iii) `15%`; (iv) in aggiunta `55%`.

## 8. LA TABELLA DEL TORNEO *(vuota)*

| la forma | regge | omega | dove sta | m*_sol | orologio V2 | orologio V3 | caduta V2 | caduta V3 | coppia in fase | Pound-Rebka | antifase | K_i/K_th |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F0 | si' *(oggi)* | `0.6264` | il gap sopra | `-19.26` | `+0.999` | `-0.761` | VIA | VERSO | *(oggi: in G+U attrae)* | piu' veloce | respinge | `0.996` |
| L+0.5 ... L-1, FH, FT | | | | | | | | | | | | |
