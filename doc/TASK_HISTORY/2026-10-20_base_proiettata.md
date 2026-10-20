# L'INTERVALLO LUNGO CON LA BASE PROIETTATA E GAMMA COME PENDENZA

> **Il mandato:** decisione di Luca del `2026-10-20` alle `18:02`, sulla domanda della relazione
> di `16b5d10f`. ### **Un conto, nessuna cura.** ### **Due cambi di METODO del conto, nessuno di
> fisica:** impronta `2e7f795d2a52fbe7`, `leggi.yaml` intatto. ### **Lo strumento
> `csv/_stabilita_lineare.py` (blob `0610bf5e`) si ESTENDE con un modo nuovo**
> *(`--proiettata`)*; ### **senza argomenti e con `--lungo` rifa' AL BIT `c38367db` e
> `16b5d10f`.** ### **`LINEARE`, `Lambda_c`, le letture «alla Jeans» o di modulazione, lo stato
> finale FERMI; `D4` da rileggere.**

**LIVELLO CORRENTE:** `L2`.

## 0. LA STELLA POLARE

1. **`A14`:** ### **non si applica**, perche' ### **nessuna legge cambia**: cambia il METODO del
   conto *(la base proiettata, gamma come pendenza)*.
2. **Il gradino:** `(a)` ### **la riproduzione di `c38367db` e dei numeri del guardiano con la
   base proiettata**, la proiezione SPENTA che deve riprodurre il difetto di `16b5d10f`, la
   camminata sola esatta, `P3`; `(b)` ### **`R2` toglie `cs`**; `(c)` ### **non si applica.**
3. **Aggiunge un numero o una legge?** ### **Non si applica alla fisica:** le soglie *(`1e3`
   ulp, `5%`, `1e-2`, `1e-3`)* sono ### **parametri del conto, dati dal mandato.**
4. **Tocca `rho`, `c_s` o il segno?** ### **Non si applica:** nessuna legge si tocca.
5. **Emergente o imposto?** ### **Non si applica come domanda su una legge:** il conto dice ###
   **quale famiglia di modi domina** quando il transitorio e' finito, con una base che resta
   uniforme.

## 1. RAGIONAMENTO PRELIMINARE

- ### **Le annotazioni del guardiano** *(in relazione)*: ### **l'errore `n.24`** *(l'intervallo `N dtau 100` proposto senza il conto `eps exp(gamma t) ~ 1e-16 e^40 ~ 1e1`)*; e ### **la sua LETTURA da mettere alla prova:** i quarti di `R1` ### **non sono contaminati dalla base** *(deviazione `~1e-5` relativa)*: a `(pi, pi)` coincidono fra lato `32` e `64` *(`0.549/0.625/0.450/0.605` contro `0.549/0.622/0.447/0.603`)* con rumori diversi, ### **e l'oscillazione dei quarti e' DETERMINISTICA, dello stimatore lungo l'orbita.**
  - ### **LA PREVISIONE DEL GUARDIANO:** ### **con la base proiettata, i quattro quarti di `R1` a `(pi, pi)` ridanno quelli di `16b5d10f` entro `1e-2`.** ### **Se no, la lettura cade e lo si scrive.**
- **LETTO DAL SORGENTE, su `mot`** *(cio' che il passo potrebbe leggere dal passo precedente)*:
  - `tick_con_cs` → `cs_al_centro` ### **riscrive `mot.lambda_c` e calcola la prima ipotesi di `cs` dallo STATO** *(`FP.cs(mot.densita_vuoto(st), ...)`)*, non da `mot.cs`;
  - `mot.giri_omega` e' ### **un contatore** *(scritto, non letto dal passo)*;
  - ### **se il punto fisso di `Omega` in `energia_pesata.applica` parta da una stima del passo precedente, NON l'ho verificato nel sorgente:** ### **lo verifica `P3`.**
- **Cosa credo:** che con la base proiettata `R1` e `R2` diano ### **gli stessi quarti di `16b5d10f` nei primi due**, e che ### **la pendenza** tolga l'oscillazione dello stimatore.

## 2. I DUE CAMBI DI METODO

- ### **A) LA BASE PROIETTATA:** dopo ogni tick della base, ### **ogni campo dello stato di base** *(`psi_h`, `phi_h`, e i campi per nodo `psi`, `rho`, `Lambda`, `h_int`)* ### **si sostituisce con la MEDIA SULLE CELLE**, componente per componente della cella *(per le estremita': la stessa posizione nella cella)*. ### **Lo stato uniforme e' invariante per il passo:** la proiezione toglie il rumore d'arrotondamento, e cambia l'orbita solo agli ulp.
  - ### **Le perturbazioni NON si proiettano:** la differenza `tick(base + eps e_j) - tick(base)` si calcola ### **prima** della proiezione, sulla stessa base di partenza.
  - ### **LA RIGA «UNIFORMITA'»** si misura ### **sulla base DOPO il tick e PRIMA della proiezione** *(dopo la proiezione sarebbe `0` per costruzione, e non direbbe niente)*: ### **e' il rumore che UN tick introduce.**
- ### **B) GAMMA COME PENDENZA:** ogni `4` tick si registrano ### **`ln |lambda_max(M_t)|`** *(con l'accumulatore della rinormalizzazione)* ### **e `ln ||M_t||_F`** *(l'accumulatore da solo: dopo la rinormalizzazione `||M||_F = 1`)*. ### **gamma = la pendenza della retta dei minimi quadrati contro il TEMPO PROPRIO** *(`tick dtau cs_m`)*:
  - ### **sulla SECONDA META'** `[N/2, N]` *(il gamma da riportare)*;
  - ### **sull'ULTIMO QUARTO** `[3N/4, N]` *(il controllo)*;
  - per ### **entrambi gli stimatori**. ### **Restano stampati i quattro quarti alla vecchia, come informazione.**

## 3. LA CONFIGURAZIONE *(come `16b5d10f`)*

- lati `32` *(`dtau 0.125`)* e `64` *(`dtau 0.0625`)*; `x 0.1`, `RAPPORTO 1`; ### **`N dtau 100`**; `R1` e `R2`;
- ### **la linearita'** *(`1e-7` contro `1e-6`)* ### **solo a lato `32`**, ### **sulla pendenza della seconda meta'** *(stimatore autovalore)*, entro `1e-3` del massimo;
- ### **budget `3` h per braccio**, oltre il quale si ferma e lo dichiara;
- ### **il comando:** `python csv/_stabilita_lineare.py --proiettata`.

## 4. I CRITERI, FISSATI QUI *(copiati dal mandato prima dei numeri)*

- ### **BASE VALIDA:** la riga «uniformita'» resta `<= 1e3` ulp ### **per TUTTO l'intervallo, a ogni braccio.** ### **Altrimenti il braccio NON VALE: STOP**, e lo si scrive.
- ### **ASINTOTICO**, per i tre punti *(`(pi, pi)`; ### **la banda**: il massimo della pendenza della SECONDA META' su assi e diagonale, esclusi `k = 0` e l'intorno `0.1 pi` di `(pi, pi)`, come in `16b5d10f` ma scelto sulla seconda meta'; `k = 0`)*: ### **la pendenza sulla seconda meta' e quella sull'ultimo quarto coincidono entro il `5%` del massimo assoluto** *(della pendenza sulla seconda meta')*, ### **E i due stimatori coincidono entro il `5%`** *(dello stesso massimo)* sulla seconda meta'. ### **Altrimenti NON ASINTOTICO.**
- ### **CHI VINCE:** sulla pendenza della seconda meta' *(stimatore autovalore)*, `(pi, pi)` contro la banda; ### **sotto il `5%` del massimo: NON DECIDIBILE.**
- ### **`k = 0`: CRESCITA VERA** se la pendenza sulla seconda meta' e' `> 0.02` ### **E** quella sull'ultimo quarto e' `>= 0.5` volte lei; ### **altrimenti TRANSITORIO**, e la frase «nessuna lunghezza minima» si ritira.
- ### **LA LARGHEZZA DEL PICCO:** come in `16b5d10f`, ### **sulla pendenza della seconda meta'.**
- ### **LA PREVISIONE DEL GUARDIANO:** i quattro quarti alla vecchia di `R1` a `(pi, pi)`, ### **a lato `32` e `64`**, contro quelli di `16b5d10f` *(letti dal `jsonl`)*: ### **entro `1e-2` ciascuno.**

## 5. I CASI DI CONTROLLO

- ### **DEVE RIUSCIRE:**
  - con la base proiettata, ### **i parametri di `c38367db`** *(lato `31`, `N dtau 25`, `R1` e `R2`)*: ### **gli stessi gamma alla vecchia** *(`ln |lambda| / tempo`)* ### **entro `1e-3` del massimo, su ogni `k`**;
  - ### **`R2` a lato `32`, `N dtau 25`:** `0.3754` a `(10, 0)` e seconda meta' `0.5847` a `(16, 16)` ### **entro `1e-3`**;
  - ### **se no: STOP.**
- ### **DEVE FALLIRE: la proiezione SPENTA**, `R2` lato `32`, `N dtau 100`: ### **la riga «uniformita'» supera `1e3` ulp.** ### **Lo fa la funzione `braccio_lungo` di `16b5d10f`, intatta**, e i suoi `L` ### **devono essere AL BIT quelli del `jsonl` di `16b5d10f`** *(cosi' `--lungo` e' provato invariato)*. ### **Se non la supera: STOP**, la proiezione non e' cio' che tiene la base.
- ### **DEVE FALLIRE: la camminata sola esatta**, lato `32`, `N dtau 100`, `<= N * 64` ulp.
- ### **`P3`, NESSUNA MEMORIA IN `mot`:** ### **un tick della base con `mot` appena dopo un tick PERTURBATO, contro un tick con `mot` dopo un tick della base:** `psi_h` e `phi_h` ### **AL BIT, oppure la differenza in ulp stampata e `<= 64` ulp**, con `cs` acceso e spento. ### **Se fallisce: STOP**, la funzione di Green ha una memoria in `mot`.
- ### **E il conto di `c38367db` senza argomenti:** `R2` lato `31` ### **AL BIT** col suo `jsonl` *(come in `16b5d10f`)*.

## 6. TODO

1. Questo task history, ### **committato DA SOLO.**
2. Le annotazioni del guardiano nella relazione: un commit.
3. Lo strumento esteso *(`--proiettata`)* e l'inventario: ### **un commit a se'.**
4. Il conto dal blob committato e pulito, in background: `python csv/_stabilita_lineare.py --proiettata > doc/referti_l2/stabilita_base_proiettata.txt`, con `doc/referti_l2/stabilita_base_proiettata.jsonl`.
5. Il referto e la relazione: un commit, `PUSHATO`, `FERMO`.
