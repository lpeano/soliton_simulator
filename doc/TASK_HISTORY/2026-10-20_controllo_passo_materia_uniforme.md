# DUE CONTROLLI DEL PASSO SULLA MATERIA UNIFORME, PRIMA DI QUALUNQUE INTERPRETAZIONE

> **Il mandato:** decisione di Luca del `2026-10-20` alle `09:12`, sull'instabilita' della
> materia uniforme di `29b997da`. ### **Nessun codice di fisica: una misura.**
> ### **`LINEARE`, la scelta di `Lambda_c` e ogni interpretazione «alla Jeans» restano FERME
> fino all'esito.**

**LIVELLO CORRENTE:** `L2`.

**IL FATTO, come l'ha letto il guardiano** nelle serie di `doc/referti_l2/jeans_del_modello.jsonl`:
- il modo dominante e' `(15, 15)` su `31x31`, cioe' `k` circa `pi` in entrambe le direzioni: ### **la scacchiera, il modo del doppione**;
- non c'e' lunghezza minima: crescono tutti gli anelli;
- gamma cresce di `2.8` volte da `x 0.01` a `x 1`, e ### **non come la radice di `rho`**;
- con `cs` ACCESO, `G` cambia gia' fra i primi campioni *(`-968.6`, `-989.4`, `-1009.6`)* mentre lo stato e' uniforme a `1e-16`;
- con `cs` SPENTO, `G` OSCILLA di periodo `2` *(`-1937.2`, `-2321.6`, `-1937.2`)*, e ### **a `cs` spento `G` e' l'energia `H`, che dovrebbe conservarsi.**

## 0. LA STELLA POLARE

1. **`A14`:** ### **E' la domanda di `C1`.** Nessuna legge cambia; si misura ### **se il passo
   conserva `H` sulla materia uniforme**. Se non la conserva, e' ### **un difetto del passo**,
   non una violazione dichiarata.
2. **Il gradino:** `(a)` e' il livello di `C1`: un tick per volta, contro una banda gia'
   misurata, con un caso che deve riuscire *(la scena di `M-B2`)*. `(b)` e' `C2`: ### **si
   toglie `S3`** *(`CAMM-MATERIA-VUOTO`)* e si guarda se la crescita resta. `(c)` ### **non si
   applica:** nessun confronto con un limite noto.
3. **Aggiunge un numero o una legge?** ### **No.** I `20` tick di `C1` e i `2000` di `C2` sono
   ### **parametri della misura**. La banda e la soglia di Student ### **escono da misure e
   strumenti gia' committati.**
4. **Tocca `rho`, `c_s` o il segno?** ### **No:** `cs` e' SPENTO in entrambi i controlli. ### **E
   proprio per questo** dicono se la crescita ha bisogno di `cs`, del passo o di `S3`.
5. **Emergente o imposto?** ### **E' la domanda di `C2`:** se la crescita resta senza `S3`,
   ### **non e' l'accoppiamento a produrla**, e il sospetto cade sulla camminata.

## 1. RAGIONAMENTO PRELIMINARE — cosa credo prima di guardare, e cosa NON so

- **LA CADENZA DI `29b997da`, dichiarata prima** *(letta dal sorgente, `csv/_jeans_del_modello.py`, funzione `braccio`, chiusura `foto`)*:
  - ### **`G` si campionava UNA volta per tick INTERO**, con `EP.g_dello_stato`, dopo ogni `TK.tick` *(cs spento)* o `TK.tick_con_cs`;
  - il primo campione e' al tick `0`, ### **prima del primo tick**;
  - ### **nessun campione a meta' tick.**
  - ### **Quindi il periodo `2` della serie NON e' un aliasing di un campionamento a mezzo tick:** sono tre tick interi consecutivi.
- **A `cs` spento `CAMM-FASE-VUOTO` e' l'identita'** *(`energia_pesata.applica` torna lo stato se `mot.cs` e' `None`)*, e `g_dello_stato` ### **e' `H_tot`**, a meno dell'ordine della somma. ### **Lo verifico, non lo assumo:** la seconda fonte e' `_misura_mb2.h_tot`.
- **Cosa credo:** un'oscillazione del `20%` di `H` a tick intero, sulla materia uniforme, ### **non e' compatibile con un passo di Strang che conserva `H` al secondo ordine.** Pero' `dtau 0.5` mette i pezzi a `theta = pi/2`, ### **lontano dal regime asintotico** *(`M-B2` lo dice)*.
- **Cosa NON so:**
  - se lo stato uniforme e' un punto fisso del passo **senza** `S3`;
  - se `h_tot` vede su questa scena ### **lo stesso `H` che vede `g_dello_stato`**;
  - ### **se la banda di `C1` di strada `(d)`, misurata su un'altra scena, e' quella giusta per questa:** e' il criterio di Luca, e lo applico com'e'. ### **Il caso che deve riuscire** *(la scena di `M-B2`)* **dice se la banda e' troppo stretta.**

## 2. PROGETTAZIONE — i passi, cosa decide ciascuno, e cosa mi fa FERMARE

**Lo strumento:** `csv/_controllo_passo.py`. ### **Riusa** `_jeans_del_modello.scena`, `t_soglia`, `gamma_k`, e `_instabilita_vuoto.gamma_del_tratto` e `onda`. **Seconda fonte di `H`:** `_misura_mb2.h_tot`. ### **Il mezzo tick:** una COPIA dello stato avanzata con `TK.percorri_tick(copia, mot, par, (), None, TK.meta_del_palindromo())`, cioe' ### **il centro del palindromo**, nello stesso modo in cui lo raggiunge `cs_al_centro`.

### `P0` — LE PROVE DELLO STRUMENTO *(se una cade: STOP)*

- **`P0a`, il rivelatore del periodo `2`** *(il caso che DEVE scattare e quello che NON deve)*:
  - una serie sintetica `H0 (1 + 3 B (-1)^t)` ### **deve** dare «periodo `2`»;
  - una serie costante con rumore `1e-3 B` ### **non** deve.
- **`P0b`, LA BANDA `B`:** si rifa' il braccio `k = 1` di `C1` di strada `(d)` *(`_misura_strada_d.corsa(0.5, 16, True, "centro", 1)`)*.
  - L'escursione ### **deve coincidere** con quella del referto `doc/referti_l2/c1_tetto_omega.txt` *(riga `k = 1`, letta dal file)* **alle `7` cifre stampate**.
  - ### **`B` = escursione / `|G(0)|`** della stessa scena e dello stesso stato *(la pre-corsa di `_misura_hw`, `cs` acceso, `Lambda_c` = la media)*.
- **`P0c`, LA RIPRODUZIONE DI `29b997da`:** i `21` campioni di `G` ai tick interi di `C1` ### **devono essere BIT-IDENTICI** ai primi `21` della serie `G` del braccio `D2 cs SPENTO` nel `jsonl`. ### **Questo prova che la cadenza dichiarata sopra e' quella vera.**

### `C1` — `G` E `H` A `CS` SPENTO, TICK PER TICK

- **La scena:** quella di `D2` *(`x 0.1`, rapporto `1`, `dtau 0.5`, nessuna perturbazione, `cs` spento)*. ### **`20` tick.**
- **I campioni:**
  - a ogni tick intero `t = 0..20`: `G` *(`g_dello_stato`)* e `H` *(`h_tot`, da zero)*;
  - a ogni meta' tick `t + 1/2`, `t = 0..19`: gli stessi, ### **sulla copia al centro del palindromo.**
- **La seconda fonte:** `|G - H|` ### **entro `4096` ulp** *(`_misura_hw.ULP_SECONDA_FONTE`)* della somma dei valori assoluti dei termini *(i tetti di `termini_di_h`)*, ### **a ogni campione.** Se cade: STOP *(le due funzioni non misurano la stessa cosa)*.
- ### **IL CRITERIO, fissato qui:**
  - **(i) CONSERVA:** `max_t |H(t) - H(0)| / |H(0)|` sui tick interi `t = 1..20` e' `<= B`.
  - **(ii) PERIODO `2`:** per ogni `t = 0..18`, `dH_t = H(t+1) - H(t)` e `dH_(t+1)` hanno ### **segno opposto**, e `|dH_t| > B |H(0)|`.
- **Il caso che DEVE RIUSCIRE:** ### **la scena di `M-B2`** *(`DV.scena(MB2.NN, MB2.SEME, 0.5, ...)`, il suo stato di partenza, `cs` spento)*, ### **lo stesso strumento, `20` tick:** deve dare **(i) si'** e **(ii) no**. ### **Se non riesce, lo strumento o la banda sono sbagliati: STOP**, e nessun verdetto su `C1`.
- **IL VERDETTO DI `C1`:** se **(ii)**, oppure se **(i)** cade, ### **il passo NON conserva `H` sulla materia uniforme**: e' ### **un difetto del passo, indipendente da `cs`**, e ### **si FERMA TUTTO**: `C2` non gira.

### `C2` — LA MATERIA SENZA `CAMM-MATERIA-VUOTO` *(senza `S3`)*, `cs` spento

- **La scena di `D2`**, `2000` tick, ### **`TK.percorri_tick(st, mot, par, ("CAMM-MATERIA-VUOTO",), None, len(CM.ORDINE))`**. Resta la camminata lineare e unitaria.
- **Il braccio `0`** *(controllo positivo, deve riuscire)*: ### **lo stesso ciclo con `salta = ()`**.
  - Deve riprodurre `D2` di `29b997da` ### **al bit**: `m_rho`, `m_lam` e `G` uguali al `jsonl`.
  - ### **Se non riesce: STOP.**
- **Si riportano, come in `29b997da`:**
  - `gamma` di `rho` e di `Lambda` *(in tick e in tempo proprio)*;
  - il modo dominante *(`onda`)*, ### **`k = pi` o no**;
  - gli anelli sopra la soglia;
  - `max|delta rho| / rho_m` alla fine.
- ### **«CRESCE» se `gamma >= t_(99.73%, 4) * barra`** *(la soglia di `29b997da`, `6.62`)*.
  - ### ⚠ **Se `max|delta rho|` e' ZERO ESATTO in qualche tick del tratto**, `log` non esiste: si scrive ### **«zero esatto: lo stato uniforme e' un punto fisso al bit»**, che e' ### **«non cresce»**.
- **LA LETTURA, fissata qui** *(e' quella di Luca)*:
  - ### **SE CRESCE: il difetto e' nella camminata.**
  - ### **SE NON CRESCE: l'instabilita' nasce dall'accoppiamento `S3` materia-vuoto**, e si riporta ### **su quale modo** *(quello del braccio `0`: `k = pi` o no)*.

### ⛔ **COSA MI FA FERMARE:** una prova di `P0` che cade; la seconda fonte che non coincide; il caso di `M-B2` che non riesce; `C1` che cade *(e allora `C2` non gira)*; il braccio `0` di `C2` che non riproduce `D2` al bit.

### ⛔ **NESSUNA INTERPRETAZIONE FISICA**: ne' «alla Jeans», ne' una legge che stabilizzi. ### **`LINEARE` e `Lambda_c` FERMI.**

## 3. TODO DEL NEXT STEP

1. Questo task history, l'**errore `n.19`** nella relazione, e ### **l'OSSERVAZIONE nella mappa** *(la lunghezza dell'era `1`, la scala della griglia)*: commit e push ### **PRIMA del codice**.
2. `csv/_controllo_passo.py`, con la voce in `doc/INVENTARIO_strumenti.md`: ### **un commit a se'.**
3. La corsa dal blob committato e pulito: `python csv/_controllo_passo.py > doc/referti_l2/controllo_passo.txt`.
4. Il referto e la relazione: un commit, poi `PUSHATO` e, se un criterio cade, `FERMO`.
