# TRIANGOLI, GRADINO 2: `S3` E LA CAMMINATA SUL TORO TRIANGOLARE, E LA SUA STABILITA' LINEARE (`R2`)

> **Il mandato:** decisione di Luca del `2026-10-21` alle `21:52`; progetto `doc/PROGETTO_TRIANGOLI.md`
> *(`a840e8f7`)*, gradino `1` *(`3008bd13`, `csv/_triangoli.py`)*. ### **Eseguito DOPO la pulizia del
> nucleo** *(arrivata insieme, `5d2d1121`)*: `PRECEDENZA-IN-CODA`, l'ordine registrato nella relazione.
> ### **`eps = 0.5`** *(decisione delle `17:53`)*. ### **`leggi.yaml` intatto: `S3` e' la STESSA legge,
> letta su `6` estremita'.** ### **NESSUNA CURA, nessun'altra legge sui triangoli** *(`R1` e `cs` dopo)*.

**LIVELLO:** `L2`, triangoli. ### **Sulla griglia quadrata TUTTO resta AL BIT.**

## 0. LA STELLA POLARE

1. **`A14`** *(la conservazione locale)*: ### **`S3` e' per nodo** *(`N(rho, Lambda)` del nodo)*, e la
   camminata per estremita' e per arco: ### **raggio `0` anche su `6` vicini.** Non cambia.
2. **Il gradino:** `(a)` ### **il caso che deve fallire** e' l'isotropia `C6` di `gamma(k)` sul quadrato; ###
   **la camminata sola esatta** e' il controllo del metodo; `(b)` ### **`R2` toglie `cs`**; `(c)` ### **non si
   applica** *(nessuna cura)*.
3. **Aggiunge un numero o una legge?** ### **No.** ### **La scelta di scala NON si fa qui:** due bracci
   dichiarati, `SN` e `SE`, e ### **la scelta e' di Luca.**
4. **Tocca `rho`, `c_s` o il segno?** ### **`rho` e `Lambda` per nodo SI'**, ed e' il punto: `SN` li tiene
   uguali al quadrato, `SE` li moltiplica per `6/4`. ### **`cs` e' spento.**
5. **Emergente o imposto?** ### **La geometria e' imposta** *(il grafo)*; ### **`gamma(k)` e' misurato.**

## 1. RAGIONAMENTO PRELIMINARE

- **LETTO DAL CODICE PRIMA DEI NUMERI:**
  - ### **`rho_k = sum_h |psi_h|^2`, `Lambda_k = sum_h |phi_h|^2`** *(`motore.densita_materia`,
    `densita_vuoto`)*: ### **quadratiche.** Quindi `SN` = ### **`psi` E `phi` per `sqrt(4/6)`**, e per
    nodo ### **`rho = 0.4`, `Lambda = 4`, come il quadrato**; `SE` = le ampiezze di `594417f6`
    *(`x = 0.1`, vuoto `1`)*, e per nodo ### **`rho = 0.6`, `Lambda = 6`.**
  - ### ⚠ **`nu_S3 / OMEGA_H` = `(Lambda/(rho+Lambda))^2 / pi`** *(come lo calcola `braccio_proiettato`)*
    ### **dipende SOLO dal rapporto `rho/Lambda`**, che e' `x` in tutti e due i bracci: ### **credo che
    `SN` e `SE` diano ENTRAMBI `0.2631`, per costruzione.** ### **Lo si stampa, non lo si assume.** ###
    **Quindi `nu_S3` NON distingue i due bracci:** `N(rho, Lambda) = rho ln(rho/(rho+Lambda))` ### **e'
    omogenea di grado `1`**, e cio' che cambia fra `SN` e `SE` e' ### **la scala di `N` rispetto alla
    camminata** *(che non ha scala)*.
  - ### **La cella:** l'arco `k = v d + a`, le estremita' `2k` *(sul nodo `v`)* e `2k + 1` *(sul vicino)*:
    `reshape(n, 4d)` e `reshape(n, 2d)` danno ### **la cella dei `d` archi propri del nodo** -- ### **sul
    quadrato `d = 2`, `24` reali, la cella di `_stabilita_lineare.celle`**; sui triangoli `d = 3`, ###
    **`36` reali.** Il nodo e' `i L + j`: ### **`fft2` sugli indici vale com'e'.**
  - ### ⛔ **`_stabilita_lineare.proietta` ha `4 * n` scritto dentro**, e `celle`, `perturba`,
    `uniformita` le `4` estremita': ### **l'estensione sta in un file NUOVO**, `csv/_stabilita_triangoli.py`,
    ### **che importa i due strumenti e generalizza in `d` cella, impulso, Green, proiezione,
    uniformita'.** ### ⚠ **Il mandato dice «`_stabilita_lineare.py` esteso»:** lo lascio ### **al bit**,
    cosi' ### **i suoi referti si rigirano anche a HEAD**; la scelta si dichiara qui e nella relazione.
- **IL VALORE DI RIFERIMENTO DEL QUADRATO** *(letto dal `jsonl` di `594417f6`, prima delle corse)*: ###
  **il `0.407` del mandato e' lo stimatore degli AUTOVALORI** *(`meta_eig`, max `0.4069` a `k = (0, 8)`)*; ###
  **lo stimatore della NORMA** *(`meta_norm`, quello che il mandato chiede)* ### **da' `0.4018`, allo stesso
  `k`.** ### **Il rapporto si fa con lo STESSO stimatore** *(norma con norma)*, ### **e si stampano
  tutti e due.**
- ### **I PUNTI `K` NON SONO SULLA GRIGLIA A LATO `32`:** in `K` le tre fasi `k.a` valgono `±2pi/3`, cioe'
  `m = L/3 = 10.67`. ### **Si dichiarano i `k` della griglia piu' vicini a `K`** *(la distanza stampata)*;
  ### **lato `32` lo fissa il mandato**, e il confronto col quadrato lo vuole.
- **Cosa NON so:** ### **se `S3` gira sui triangoli senza toccare il codice** *(il gradino `1` ha girato
  SOLO la camminata, `S3` saltata)*; ### **se `proietta` generalizzata tiene la base** *(`<= 1e3` ulp)*.

## 2. LA PROGETTAZIONE: I PASSI, E COSA MI FA FERMARE

- **La scena:** il costruttore di `csv/_triangoli.py` *(`scena(griglia, lato, dtau, x)`)*; `SN` riscala
  ### **dopo** la costruzione `psi_h` e `phi_h` per `sqrt(4/6)`.
- **LA MAPPA NELLA ZONA ESAGONALE** *(dichiarata)*: `a1 = (1, 0)`, `a2 = (-1/2, sqrt3/2)` *(le direzioni
  `0` e `120` gradi di `_triangoli.TRIANGOLI`; il terzo spostamento `(1, 1)` e' `a1 + a2`, `60` gradi)*;
  ### **`k = 2pi (m_x b1 + m_y b2) / L`** coi reciproci `a_i . b_j = delta_ij`; ### **il rappresentante e'
  l'immagine `(m_x + p L, m_y + q L)` di `|k|` minimo.** ### **Le etichette:** `centro` *(`k = 0`)*, ### **`M`**
  *(`m` in `{(L/2, 0), (0, L/2), (L/2, L/2)}`)*, ### **`K`** *(i `k` della griglia a distanza minima dai due
  vertici `K` non equivalenti)*, ### **`interno`** il resto.
- **LA ROTAZIONE DI `60` GRADI:** `(m_x, m_y) -> (-m_y, m_x + m_y)`, ### **quella di `_triangoli.ruota60`**
  *(gradino `1`, verificata sulle fasi di `A(k)`)*.
- **`gamma(k)`:** ### **lo stimatore della NORMA, pendenza della seconda meta'** *(`pend["meta_norm"]` di
  `braccio_proiettato`)*, nel tempo proprio. ### **`R2`: `S3` sola, `cs` spento, lato `32`, `dtau 0.125`,
  `x 0.1`, base proiettata, `N dtau = 100`.**

### I CONTROLLI *(copiati dal mandato)*

- ### **DEVONO RIUSCIRE:**
  1. ### **lo strumento esteso, sulla scena QUADRATA del costruttore generale, ridà `R2` di `594417f6`
     AL BIT** *(i `10` campi di `csv/_al_bit_cura_d0.py`)*. ### **Se no: STOP** -- lo strumento esteso
     misura un'altra cosa;
  2. ### **la camminata sola sui triangoli ESATTA:** `gamma = 0` su ogni `k` ### **entro `N * 64` ulp**
     *(`max |ln|lambda(A^N)||`, come `c2_esatto_lungo`)*;
  3. ### **`P1`** *(un tick con le cache azzerate = con le cache, AL BIT)* ### **e `P3`** *(nessuna memoria in
     `mot`: al bit o `<= 64` ulp)*, sui triangoli, ### **`cs` spento** *(`R2`)*;
  4. ### **la base `<= 1e3` ulp** per tutto l'intervallo, `SN` e `SE`;
  5. ### **la linearita' su `SN`:** `max_k |gamma_(1e-7) - gamma_(1e-6)| <= 1e-3 * max_k gamma`;
  6. ### **l'ISOTROPIA `C6` di `gamma(k)` sui triangoli:** `max_k |gamma(k) - gamma(R60 k)|` ### **entro la
     banda di linearita'** *(`1e-3 * max_k gamma`, la stessa del punto `5`)*, `SN` e `SE`.
- ### **DEVE FALLIRE:** ### **l'isotropia `C6` di `gamma(k)` sul QUADRATO** *(lo stesso conto sul `gamma`
  del controllo `1`)*.
- ### **COSA MI FA FERMARE:** il controllo `1` che cade; la camminata sola che cresce; `P1` o `P3`; la base
  oltre `1e3` ulp; ### **`S3` che non gira sui triangoli senza toccare il NUCLEO** *(allora: il minimo, al bit
  sul quadrato, con la suite -- e se il minimo non e' ovvio, STOP)*.

### LE LETTURE, FISSATE QUI *(copiate dal mandato)*, per `SN` e `SE`

- ### **il massimo di `gamma`, dove** *(`centro`, `M`, `K`, `interno`)*, ### **e il rapporto col massimo del
  quadrato, STESSO stimatore** *(norma: `0.4018`, misurato dal controllo `1`)* -- ### **e accanto il `0.407`
  del mandato** *(autovalori)*;
- ### **STABILE** se il massimo `<= 1e-3 * 0.407` *(`4.07e-4`)*;
- ### **LA PREVISIONE DELLA BANDA** *(sez. `j` del progetto)*: ### **tiene se il massimo della banda sta fra
  `0.37` e `0.45`**. ### **La banda sui triangoli:** il massimo di `gamma` ### **escluso `k = 0` e esclusi i
  punti `M` e `K`** *(il bordo si legge a parte)*; ### **sul quadrato era `punto_banda`** *(assi e diagonale,
  escluso l'intorno di `(pi, pi)`)*;
- ### **IL BORDO:** `gamma` ai punti `M` e `K`, ### **accanto a `(pi, 0)` e `(pi, pi)` del quadrato**;
- ### **`nu_S3 / OMEGA_H`** per `SN` e `SE`, accanto a `0.2631` del quadrato.
- ### **Le PREVISIONI del progetto** *(sez. `j`)*: ### **il picco alternato non esiste** *(sui triangoli non
  c'e' un `(pi, pi)`: il grafo non e' bipartito)*; ### **la banda di `R2` resta entro `~10%`, `0.37`-`0.45`**;
  ### **se cambia molto, dipende dalla geometria.**

## 3. TODO

1. Questo task history, ### **committato DA SOLO.**
2. `csv/_stabilita_triangoli.py`: commit; ### **una prova corta di `S3` sui triangoli** *(gira o non gira)*.
3. La corsa, il referto `doc/referti_l2/triangoli_gradino2.txt` e `.jsonl` dal blob committato.
4. La voce `[[GRIGLIA-A-TRIANGOLI]]`, la relazione, ### **UNA domanda: la scelta di scala, `SN` o `SE`, coi
   numeri dei due bracci.**
