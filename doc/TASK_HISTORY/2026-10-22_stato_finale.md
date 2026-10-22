# LO STATO FINALE: DOVE VA LA MATERIA UNIFORME DOPO L'INSTABILITA'

> **Il mandato:** decisione di Luca del `2026-10-22` alle `02:22`: ### **la voce «stato finale», FERMA fino a oggi, si
> apre come MISURA**; eseguito ### **dopo le due misure su `S3`** *(`642dee6f`, `07083f09`)*. ### **La dinamica
> COMPLETA, non linearizzata.** ### **`leggi.yaml` e l'impronta intatti, nessuna cura**; ### **commit separati per
> braccio** *(il riavvio notturno di Luca)*.

**LIVELLO:** `L2`, una misura della dinamica completa.

## 0. LA STELLA POLARE

1. **`A14`:** ### **si MISURA** *(la norma e `G`)*, non si cambia.
2. **Il gradino:** `(a)` ### **due semi**: un risultato che cambia col seme non e' robusto; `(b)` ### **`R2` toglie
   `cs`**; `(c)` ### **non si applica.**
3. **Aggiunge un numero o una legge?** ### **No.** Il rumore `1e-10` e' ### **il seme della misura**, non fisica.
4. **Tocca `rho`, `c_s` o il segno?** ### **Si osserva `rho`**; `cs` acceso solo in `R1`.
5. **Emergente o imposto?** ### **E' la domanda stessa** *(sotto)*.

### ❓ **LA DOMANDA** *(del mandato)*: ### **«l'instabilita' e' la strada verso un equilibrio dinamico (la materia che si
raggruppa), o un difetto che degenera alla scala del reticolo?»**

## 1. RAGIONAMENTO PRELIMINARE

- ### **CHE COSA CREDO PRIMA:** ### **la banda lineare sta a `~4` archi, FISSA IN ARCHI al raffinamento**
  *(`83edbaa7`)*: ### **se i grumi nascono dalla banda e restano della sua taglia, a lato `64` saranno ancora `~4` archi**
  -- ### **cioe' ARTEFATTO DEL RETICOLO** *(la lettura `(a)`)*. ### **Credo `(a)`**, ### **con una riserva:** la dinamica
  non lineare puo' far crescere i grumi *(coarsening)* fino a una taglia che non dipende dalla banda -- ### **e allora
  la prova la decide la taglia finale, non la banda.**
- ### **Sul reticolo:** ### **credo che la fascia RETICOLO NON passi il `50%`** *(sui triangoli il bordo e' quieto:
  `R2` `M` `0.127`; sul quadrato `(pi, pi)` e' `0.355` contro `0.402` della banda)*; ### **ma a `x` piccolo il picco
  alternato supera la banda** *(`07083f09`)*, ### **e qui `x = 0.1`.**
- **Cosa NON so:** ### **se la dinamica completa di `R1` regge fino alla fine** *(il punto fisso di `cs` e quello di
  `Omega` su uno stato NON uniforme)*; ### **quanto deriva `G`** su `250` unita' di tempo proprio.

## 2. LA PROGETTAZIONE *(fissata prima dei numeri)*

- ### **I BRACCI, e che cosa e' «un braccio» per i commit:** ### **un braccio = (legge, geometria)**: `R2Q`, `R1Q`,
  `R2T`, `R1T`. ### **Ognuno con le DUE TAGLIE e i DUE SEMI** *(la prova che decide vuole le due taglie insieme)*, ###
  **un referto e un commit per braccio**: `doc/referti_l2/stato_finale_<braccio>.txt` e `.jsonl`; ### **la sintesi**
  in `doc/referti_l2/stato_finale.txt` e `.jsonl`, generata dai quattro `jsonl`.
- ### **LA SCENA:** il costruttore di `csv/_triangoli.py` *(`_stabilita_triangoli.scena`)*: ### **quadrato `Q`**,
  ### **triangoli `SN`** *(la densita' per nodo del quadrato: la regola di scala di Luca; `SN` e `SE` coincidono, `bb0ef057`)*;
  ### **`x 0.1`**, vuoto `1`; ### **`R1`: `Lambda_c = 1 * Lambda` medio** *(come `594417f6`)*, `cs` acceso a ogni tick
  *(`tick.tick_con_cs`)*. ### **Le taglie:** lato `32` `dtau 0.125`, lato `64` `dtau 0.0625`.
- ### **IL SEME:** ### **rumore complesso gaussiano** su ogni componente di `psi_h` e di `phi_h`, ### **ampiezza relativa
  `1e-10`** *(deviazione `1e-10 * max|campo|` per parte reale e immaginaria, `/sqrt2`)*, ### **semi `1` e `2`**
  *(`numpy.random.default_rng`)*.
- ### **IL TEMPO:** ### **il tempo proprio** `tau = somma dtau * <cs>` *(`cs = 1` in `R2`; in `R1` il `cs` medio del
  CENTRO di ogni tick)*; ### **fine a `tau = 250`** *(`>= 4 t_sat`, `t_sat ~ ln(1e10)/0.4 ~ 58`)*.
- ### **LE OSSERVABILI, a ogni unita' di `tau`:**
  - ### **conservazione:** `sum |psi|^2` e `sum |phi|^2` *(separate: la camminata e `S3` le conservano ciascuna)*, e
    ### **`G`** *(`energia_pesata.g_dello_stato`)*: lo scarto relativo dall'inizio;
  - ### **lo spettro di `rho - <rho>`:** `|FFT2|^2` sui nodi `(i, j)`; ### **la coordinata nella zona** `r(k) = max_M
    (k . m_hat)/|M|` *(sul quadrato `max(|k_x|, |k_y|)/pi`; sui triangoli l'esagono di `_stabilita_triangoli.zona`)*; ###
    **ONDE LUNGHE `|k| < 0.25 pi`, RETICOLO `r >= 0.75`, BANDA il resto**, come frazioni della potenza delle
    fluttuazioni;
  - ### **i grumi:** `max rho / <rho>`; ### **i massimi locali** *(un nodo con `rho` maggiore di TUTTI i vicini, dagli
    archi)*; ### **la dimensione media `L_g = sqrt(n / n_massimi)` IN ARCHI**; e come informazione ### **la lunghezza
    spettrale `2 pi / <|k|>_potenza`**;
  - ### **i contatori:** `mot.avvisi_omega`, ### **il cono** `max(dtau_nodo)/dtau_rif` dopo ogni tick.

### LE LETTURE, FISSATE QUI *(copiate dal mandato)*, sull'ULTIMO TERZO *(`tau` da `2T/3` a `T`)*

- ### **SATURA** se lo spettro *(le tre frazioni)* e le grandezze dei grumi *(`max rho/<rho>`, `n_massimi`, `L_g`)*
  ### **cambiano meno del `10%`** fra la prima e la seconda meta' dell'ultimo terzo *(le medie)*; ### **altrimenti NON
  SATURA** *(in crescita o in deriva)*.
- ### **DEGENERA** se ### **la fascia RETICOLO porta piu' del `50%`** della potenza delle fluttuazioni *(media
  sull'ultimo terzo)*, ### **o se la corsa si ferma** *(punto fisso, cono, `NaN`)*.
- ### **LA PROVA CHE DECIDE, fra lato `32` e lato `64`** *(per braccio, la media sui due semi)*, ### **sul rapporto `L_g(64)
  / L_g(32)`**: ### **`(a)` FISSA IN ARCHI** *(entro `20%` di `1`)* ### **-> ARTEFATTO DEL RETICOLO**; ### **`(b)` FISSA IN
  UNITA' FISICHE** *(entro `20%` di `2`)* ### **-> FISICA**; ### **`(c)` NE' L'UNA NE' L'ALTRA -> NON DECIDIBILE**, coi
  numeri.
- ### **CONSERVAZIONE:** ### **`G` entro il suo errore di secondo ordine, o scritto quanto deriva** -- ### **non conosco un
  errore di secondo ordine per QUESTA scena** *(quello di `C1` e' di un'altra)*: ### **si scrive la deriva**, e ### **il
  rapporto fra le due taglie** *(dove `dtau` si dimezza: il secondo ordine lo vorrebbe `~4`, ma le due taglie NON sono
  lo stesso sistema discretizzato: e' informazione)*.
- ### **Le istantanee `png`:** ### **NON le faccio** *(il mandato dice «se utile»)*: ### **lo spettro e i grumi nel
  `jsonl` bastano per le letture**, e un `png` non e' rigirabile da un comando senza la libreria di disegno.

## 3. TODO

1. Questo task history, ### **committato DA SOLO.**
2. `csv/_stato_finale.py`: commit; ### **poi un braccio alla volta**, `--braccio R2Q`, `R1Q`, `R2T`, `R1T`: ### **corsa,
   referto, commit, push** per ognuno.
3. `--sintesi`: il referto `stato_finale.txt` e `.jsonl`; la relazione: le letture per braccio e ### **che cosa dicono
   sulla domanda.** ### **NESSUNA CURA; `LINEARE` e' di Luca.**
