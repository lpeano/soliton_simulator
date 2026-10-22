# DUE MISURE SU `S3`, NESSUNA FISICA NUOVA: `(1)` `S-E`, IL MODO CHE CRESCE SUI RAMI; `(2)` LA MATERIA DILUITA

> **Il mandato:** decisione di Luca del `2026-10-22` alle `02:11`, dopo `3d009495` *(`doc/S3_RIPENSATA.md`)*.
> ### **MISURE: `leggi.yaml` e l'impronta `2e7f795d2a52fbe7` intatti, nessuna cura.** ### **Le due misure in
> COMMIT SEPARATI** *(il riavvio notturno: se la seconda si interrompe, la prima resta)*.

**LIVELLO:** `L2`, misure.

## 0. LA STELLA POLARE

1. **`A14`:** ### **non si applica** *(nessuna legge cambia)*.
2. **Il gradino:** ### **non si applica** *(misure di diagnosi)*; ### **ogni misura ha il suo controllo che ripete la
   cosa giusta** *(sotto)*.
3. **Aggiunge un numero o una legge?** ### **No.** Gli `x` diluiti sono ### **scene**, non parametri della legge.
4. **Tocca `rho`, `c_s` o il segno?** ### **La misura `2` cambia `rho` della SCENA** *(`x`)*; ### **`cs` spento.**
5. **Emergente o imposto?** ### **Misurato.**

## 1. RAGIONAMENTO PRELIMINARE

### 1.1 LA LETTURA DEL GUARDIANO *(copiata dal mandato, da verificare, NON assunta)*

> con `N = rho ln(rho/(rho + Lambda))`, `alpha = dN/drho = ln(rho/(rho+Lambda)) + Lambda/(rho+Lambda)`, e
> `rho dalpha/drho = Lambda^2/(rho+Lambda)^2 = nu_S3` *(la grandezza che lo strumento stampa)*. ### **Per `rho -> 0`
> vale `1`: per il logaritmo, l'accoppiamento efficace NON va a zero con la materia.** ### **Previsione: la banda
> resta `O(0.4)` anche con pochissima materia.** ### E' compatibile con la lettura «a rami» *(`S3_RIPENSATA`,
> `3.2`)*, non la sostituisce.

- ### **CHE COSA NE PENSO PRIMA:** ### **il conto torna** *(`d alpha/d rho = Lambda^2 / (rho (rho+Lambda)^2)`)*, e ###
  **i dati gia' committati lo sostengono**: `x 0.01` ha `nu_S3 0.980` e `gamma` `0.3946` *(`d0_risonanza_bis`)*. ###
  **Credo che a `x 1e-3` e `1e-4` la banda resti `~0.39`-`0.40`** *(`nu_S3` `0.998` e `0.9998`)*: ### **DILUITA
  INSTABILE.**
- ### ⛔ **UNA CONSEGUENZA PER LA MIA SEZ. `3.2`, scritta prima dei numeri:** ### **la prova `2`** *(«`nu` piccolo
  davvero: la lettura vuole `gamma -> 0` linearmente in `nu`»)* ### **NON si fa diluendo:** con questa `S3`
  ### **`nu_S3 = 1/(1+x)^2`**, quindi ### **`x -> 0` manda `nu` a `1`, non a `0`**; ### **`nu -> 0` vuol dire `x >> 1`
  *(tanta materia)*. ### **La misura `2` verifica la lettura del guardiano, non la mia prova `2`.** ### **E la mia
  prova `2` come scritta in `3.2` diceva «`x >> 1`, `nu_S3 -> 0`»: giusta nella formula, ma ### **la misura di oggi
  non la tocca.**

### 1.2 LA MISURA `1`, `S-E`: CHE COSA SI MISURA, PRECISATO PRIMA DEI NUMERI

- ### **IL MODO CHE CRESCE:** ### **l'autovettore di modulo massimo di `M(k)`** *(la monodromia della base
  proiettata dopo `N` tick)* ### **al `k` della banda** *(l'argmax di `gamma` con lo stimatore della norma)*.
- ### **I RAMI DELLA CAMMINATA SOLA:** ### **gli autovettori di `A(k)`** *(`_triangoli.matrice_tick`: la camminata
  sola, ESATTA, nella cella complessa `6d`)*. ### ⚠ **La cella di `M` e' REALE** *(`12d` reali: `re` poi `im`)*, perche'
  `S3` accoppia `delta psi` e `delta psi*`; ### **nel Fourier dei campi reali** ### **`u = (Re + i Im)/sqrt2` e' la
  PARTICELLA a `k`** *(evolve con `A(k)`)* ### **e `w = (Re - i Im)/sqrt2` la BUCA** *(evolve con `conj(A(-k))`)*. ###
  **Quindi i rami sono `2 * 6d`** *(`24` sul quadrato, `36` sui triangoli)*, ### **particelle e buche**, e il peso
  di un ramo e' ### **`|<e_b, v>|^2`** sull'autovettore `v` normalizzato *(`A(k)` unitaria: base ortonormale)*.
- ### **IL SEGNO «FOCALIZZANTE»** *(la parola di `3.2`, resa esatta qui)*: con l'autovalore `lambda = e^{-i omega
  dtau}` e la non linearita' ### **`g = segno di d alpha/d rho = +`** *(`nu_S3 > 0`: l'energia di `psi` CRESCE con
  `rho`)*, ### **un ramo e' FOCALIZZANTE per il modo a `k` se `g * D_b(k) < 0`**, ### **`D_b(k) = [omega_b(k) +
  omega_b(-k)]/2 - omega_0`**, ### **lo scarto in frequenza della coppia di bande laterali dal fondo** *(`omega_0`:
  il ramo di `A(0)` che porta lo stato uniforme di `psi`, il piu' sovrapposto)*. ### **E' il criterio del modello
  minimo** *(`Omega^2 = D (D + 2 g)`: cresce se `g D < 0`)*, ramo per ramo. ### **Accanto, come INFORMAZIONE:** la
  curvatura locale `omega_b''` lungo un asse della griglia *(i rami appaiati per sovrapposizione a `k +- 1`)*.

### LE LETTURE DELLA MISURA `1` *(copiate dalla sez. `3.2` di `doc/S3_RIPENSATA.md`, PRIMA dei numeri)*

> **CHE COSA LA SMENTIREBBE** *(tre prove)*:
> 1. **la risoluzione per rami del modo che cresce** *(l'autovettore di `M(k)` alla banda proiettato sui rami della
>    camminata sola)*: **se la banda cresce su un ramo dove la curvatura ha il segno NON focalizzante**, la lettura
>    cade;
> 2. **`nu` piccolo davvero** *(`x >> 1`, `nu_S3 -> 0`)*: la lettura vuole `gamma -> 0` linearmente in `nu` sotto una
>    soglia; se `gamma` resta `~0.3` anche a `nu_S3 ~ 0.01`, la banda non viene dall'autofase di `psi`;
> 3. **una camminata coi rami tutti della stessa curvatura vicino alla banda**: la lettura vuole la banda spenta; se
>    resta, cade.

- ### **Oggi si fa la `1`.** ### **LA LETTURA `3.2` CADE** se ### **il ramo-particella di peso massimo** *(con la sua
  buca)* ### **ha `g * D_b > 0`** *(NON focalizzante)*, ### **sul quadrato O sui triangoli.** ### **TIENE** se e'
  focalizzante su tutti e due. ### **NON DECIDE** se il peso e' sparso *(il ramo di peso massimo sotto il `50%`
  della parte-particella)* -- ### **e lo si scrive.**
- ### **IL CONTROLLO CHE RIPETE LA COSA GIUSTA:** ### **`gamma` della corsa uguale AL BIT a quello committato**
  *(`R2` lato `32`: `594417f6` sul quadrato; `bb0ef057` sui triangoli, braccio `SE` = `x 0.1` per estremita')*; ###
  **`A(k)` unitaria** *(`|lambda| = 1` entro `1e-12`)*; ### **la decomposizione completa** *(la somma dei pesi `= 1`
  entro `1e-10`)*.

### 1.3 LA MISURA `2`, LA MATERIA DILUITA *(copiata dal mandato)*

- `R2` sul QUADRATO, lato `32`, `dtau 0.125`, base proiettata, `N dtau 100`, la norma, la seconda meta', a ### **`x =
  1e-3` e `1e-4`**; ### **`x` `1e-2`, `0.1`, `1` riletti da `d0_risonanza_bis`**, non rifatti.
- ### **I CONTROLLI:** ### **DEVE RIUSCIRE:** `nu_S3` stampato ### **coincide con `rho d alpha/d rho` per differenze
  finite DALLA funzione `materia_vuoto.alpha` del codice**, entro `1e-8` relativo, a ogni `x`; ### **se no: la lettura
  del guardiano e' sbagliata, e lo si scrive.** ### **La linearita'** `1e-7` contro `1e-6` a `x 1e-4`; ### **la base**
  `<= 1e3` ulp; ### **la camminata sola esatta.**
- ### **LE LETTURE, sul massimo della banda** *(`m` fra `h/4` e `3h/4` lungo `(m, 0)`, `h = 16`: `m` da `4` a `12`)*:
  ### **DILUITA INSTABILE** se `gamma(1e-4) >= 0.5 * gamma(0.1)` *(`0.402`)*; ### **SI SPEGNE** se `<= 0.1 *
  gamma(0.1)`; ### **altrimenti INTERMEDIO**, coi numeri. ### **La tabella `x`, `nu_S3`, `gamma` della banda, dove.**

## 2. COSA MI FA FERMARE

### **Il controllo che ripete la cosa giusta che cade** *(`gamma` non al bit)*; ### **`A(k)` non unitaria**; ### **i pesi
che non sommano a `1`**; ### **`nu_S3` contro le differenze finite oltre `1e-8`** *(non e' uno STOP: si scrive)*.

## 3. TODO

1. Questo task history, ### **committato DA SOLO.**
2. `csv/_s3_rami.py`: commit, corsa, referto `doc/referti_l2/s3_rami.txt` e `.jsonl`, relazione, ### **commit e push.**
3. `csv/_s3_diluita.py`: commit, corsa, referto `doc/referti_l2/s3_diluita.txt` e `.jsonl`, relazione con le due
   letture insieme, ### **commit e push.** ### **`LINEARE` e `Lambda_c` FERMI.**
