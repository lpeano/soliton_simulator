# `L2` — PRIMO PEZZO: **la scena di riferimento e la misura del VERSO**

> **Decisioni di Luca del 2026-10-15** *(`16:50` e `17:27`)*. Ultimo commit verificato dal
> guardiano: `939a895`.
>
> ### ⛔ **E SI SCRIVE PRIMA DEL CODICE** *(§8)*: il commit di questo file e' **antenato**
> di quelli del lavoro.

---

## 1. RAGIONAMENTO PRELIMINARE — *cosa credo prima di guardare*

### ⭐⭐ **LA DERIVAZIONE CHE REGGE TUTTO, fatta a mano e da verificare col codice**

La saturazione e' `N = Lambda · G(h/Lambda)` con `G(x) = x - arctan x` e `x = h/Lambda`.
`motore.py::_saturazione` prende da `saturazione.pezzi(h, lam)` due numeri, `al` e `be`, e
li usa cosi': **`al`** e' la **velocita' angolare** della rotazione di `psi`, **`be`** e' la
**velocita' di fase** di `phi`. ### **Allora `al` e `be` devono essere le due derivate di
`N`**, e il conto lo conferma:

```
al = dN/dh      = G'(x)              = x^2/(1+x^2)          <- saturazione.Gp
be = dN/dLambda = G(x) - x G'(x)     = x/(1+x^2) - arctan x  <- saturazione.b
```

*(il secondo si semplifica cosi': `x - x^3/(1+x^2) = x(1+x^2-x^2)/(1+x^2) = x/(1+x^2)`)*.

### ✅ **Quindi `beta = dN/dLambda` NON e' una scelta: e' cio' che la stessa `H` produce**,
ed e' il punto della **strada `A` DERIVATA** che Luca registra: ### **nessuna legge nuova.**

### ⭐ **E IL SEGNO SI LEGGE DALLA FORMULA:** per `x` piccolo
`be ~ (x - x^3) - (x - x^3/3) = -(2/3) x^3`, ### **cioe' NEGATIVO** — e il mandato lo dice.
### ⛔ **Ma <<`beta < 0`>> NON E' ANCORA <<`Lambda` scende dove c'e' materia>>:** `beta` da'
**una FASE** a `phi`, e cio' che muove `|phi|^2` e' **la camminata del vuoto**, che converte
**differenze di fase** in **spostamento**. ### **Quel passaggio NON lo so fare a mano, e non
devo: e' esattamente cio' che il punto 2 misura.**

### ⛔⛔ **CIO' CHE NON SO, E CHE MI ASPETTO MI SORPRENDA: `h` SI ANNULLA SE LA MATERIA NON
HA UNA DIREZIONE**

Con `n` **GEOMETRICI**, `h_k = somma_{h in k} psi_h^dagger (sigma.n_h) psi_h`. E
### **la fase di `psi_h` NON conta** *(`psi^dagger A psi` e' invariante per fase)*, quindi
se `psi_h = a_h · chi` con **lo stesso spinore `chi`** su tutte le estremita' del nodo:

```
h_k = somma_h |a_h|^2 · chi^dagger (sigma.n_h) chi
```

### ⛔ **e su un toro le direzioni uscenti di un nodo SOMMANO A ZERO** *(`+x, -x, +y, -y`)*,
quindi ### **con `|a_h|` uguale su tutte le estremita' si ha `h_k = 0` ESATTAMENTE.**

> ### ⚠⚠ **CIOE': un grumo <<isotropo>>, definito sul NODO e con un solo spinore, NON
> SATURA** — `x = 0`, `al = be = 0`, e ### **la materia non tocca il vuoto per niente.**

### ✅ **E LA VIA D'USCITA NON E' UN TRUCCO: E' `sigma.p`.** Se lo spinore di ogni estremita'
e' **allineato con la sua direzione** *(l'autovettore `+1` di `sigma.n_h`)*, allora
`chi_h^dagger (sigma.n_h) chi_h = +1` per **ogni** estremita', e

```
h_k = somma_h |psi_h|^2  =  la densita' di materia del nodo
```

### ⭐ **Quindi `x = h/Lambda` diventa ESATTAMENTE il rapporto materia/vuoto**, che e' la
grandezza che la scansione del punto 2 vuole. ### 📌 **E questa e' UNA SCELTA DI SCENA, non
una legge: la DICHIARO** — il grumo di riferimento ha **elicita' `+1`**, cioe' **spin
allineato col moto.**

### ⚠ **E lo scrivo PRIMA di misurare perche' e' una previsione che puo' cadere:** se anche
col grumo allineato `h` restasse `~0`, ### **la scena di riferimento non sarebbe costruibile
cosi'**, e andrei a riportarlo invece di cambiare scena di nascosto.

### ⭐ **E IL VUOTO UNIFORME E' STAZIONARIO — e lo so derivare**

Con `phi` **uniforme** e `psi = 0`: `h = 0` ⟹ `al = be = 0` ⟹ **la saturazione non fa
niente**. E i due pezzi del vuoto: ### **il Grover** `P_u + e^{i theta}(I - P_u)` lascia il
vettore uniforme **fermo** *(e' l'autovettore di `P_u`)*; ### **il hop** `alpha I + beta S`
su due estremita' uguali da' `(alpha + beta) phi = phi`, perche' `alpha + beta = 1`.
### ⚠ **MA <<`alpha + beta = 1`>> E' ESATTO IN MATEMATICA E NON IN VIRGOLA MOBILE:**
`(1+z)/2` e `(1-z)/2` **arrotondano**, quindi mi aspetto una deriva di **qualche ulp per
tick**, cioe' **centinaia di ulp su `200` tick**. ### **E' quello il numero che riporto, non
uno zero.**

---

## 2. PROGETTAZIONE — *i passi, cosa decide ciascuno, cosa mi FERMA*

| | il passo | **che cosa decide** | **cosa mi FERMA** |
|---|---|---|---|
| `1` | **`primo_ordine/scena_l2.py`**: `n` GEOMETRICI, `U = I`, toro di taglia **dichiarata**, `phi` **uniforme**, e il grumo a **elicita' `+1`** | la scena di riferimento di `L2` | — |
| `2` | **la STAZIONARIETA' del vuoto** senza materia: `Lambda_k` invariante **all'ulp** per `>= 200` tick | se la scena si puo' usare | ### ⛔ **se non e' stazionario: RIPORTO E MI FERMO.** ### **Non scelgo un altro vuoto senza dirlo** |
| `3` | **`h` del grumo**: e' `!= 0` con l'elicita' `+1`, ed e' `= 0` col grumo isotropo | se la materia tocca il vuoto **per niente** | `h = 0` anche con l'elicita' → la scena non e' costruibile cosi' |
| `4` | **`beta = dN/dLambda` verificato COL CODICE** *(non solo a mano)* | se la strada `A` e' davvero **derivata** | `beta != dN/dLambda` → la derivazione e' sbagliata, e **tutto il resto cade** |
| `5` | **la misura DIFFERENZIALE** `dLambda_k = Lambda_k(materia) - Lambda_k(vuoto)`, sui nodi del grumo e sugli **anelli**, su **finestre** di tick, a `dtau = 1` e `0.5`, con `x` **piccolo** e `~1` | **il VERSO** | ### ⛔ **`dLambda > 0` → STOP e riporto.** ### **Nessuna legge per raddrizzarlo** |
| `6` | **IL CASO CHE DEVE FALLIRE**: `beta` col **segno rovesciato**, **solo dentro lo script** | se la misura **vede il meccanismo** | ### ⛔ **se non rovescia il segno di `dLambda`, NESSUN VERDETTO VALE** |
| `7` | **la scansione in `x`**: per `x` piccolo l'effetto deve essere **minuscolo** *(`beta ~ -(2/3)x^3`)* | se la misura **scala come la derivazione dice** | una scala che non torna → la misura guarda **un'altra cosa** |
| `8` | **la robustezza**: `n` casuali, `phi` a fasi casuali | se il verso **dipende dalla scena** | il verso che **cambia** → lo riporto, non lo scelgo |
| `9` | **il vuoto TOTALE** `somma |phi|^2` conservato all'ulp, e **dove va** il vuoto spostato | se la materia **sposta** o **distrugge** | — |

### ⛔ **LE DUE COSE CHE NON FACCIO**
1. **non tocco il motore** per il caso che deve fallire: il segno di `beta` si rovescia
   **dentro lo script**, sostituendo la funzione di `saturazione` **a runtime**;
2. **non accoppio `cs` a `Lambda`**: a `L2` ### **`cs` resta UNIFORME** e si misura **solo la
   risposta del vuoto.** ### **Come `cs` dipenda da `Lambda` e' la PROSSIMA decisione di
   Luca.**

---

## 3. LA STELLA POLARE — **cinque risposte, PRIMA del codice**

| | la risposta |
|---|---|
| **1. `A14`, conserva localmente?** | ### ⭐ **E' LA DOMANDA DEL PUNTO 9, e la misuro:** `somma |phi|^2` **globale** deve restare all'ulp, e ### **se resta, la materia SPOSTA il vuoto e non lo distrugge** — che e' la conseguenza di principio che Luca registra. ### ⚠ **Localmente invece `Lambda_k` CAMBIA, ed e' il punto:** e' proprio quel cambiamento che si va a misurare. |
| **2. a quale GRADINO arriva?** | **`(a)`**, e per la stazionarieta' e per `beta = dN/dLambda` **all'ulp**. ### ⛔ **NON `(c)`:** nessun limite noto — e in particolare ### **non affermo che questa sia gravita'**, solo che il verso e' quello della fase `1`. |
| **3. aggiunge un numero o una legge?** | ### ✅ **NESSUNA LEGGE E NESSUN PARAMETRO.** La strada `A` e' **derivata**: `beta` e' `dN/dLambda` dell'unica `H`, e il codice che la usa ### **esiste da prima** *(`_saturazione`)*. ### ⚠ **E i numeri della scena** *(taglia del toro, modulo del vuoto, ampiezza e raggio del grumo)* ### **sono UNA SCENA, non una legge**: si dichiarano e si fanno variare, e la scansione in `x` e' li' per questo. |
| **4. tocca `rho`, `c_s` o il SEGNO?** | ### **Tocca `Lambda`, e quindi `cs` INDIRETTAMENTE — ma solo nel VERSO <<materia → vuoto>>.** ### ⛔ **`cs` NON e' accoppiato a `Lambda` in questo pezzo**, e il verso contrario *(vuoto → materia)* e' `L2` piu' avanti. ### **Nessun EM.** |
| **5. emergente o imposto?** | ### ⭐⭐ **E' IL CUORE: il verso DEVE EMERGERE.** `beta < 0` e' un conto; ### **che `Lambda` SCENDA dove c'e' materia e' una CONSEGUENZA DELLA DINAMICA** *(la fase diventa spostamento attraverso la camminata del vuoto)*, e ### **nessuna riga la impone.** ### ⛔ **E se la misura dara' il verso opposto, lo riporto e mi fermo:** il mandato lo dice, e ### **una legge per raddrizzare il segno sarebbe esattamente la cosa vietata.** |

---

## 4. TODO DEL NEXT STEP

1. `primo_ordine/scena_l2.py` — il costruttore, `anelli()`, e i versori geometrici
   *(che diventano UNA sola definizione: `_misura_theta_n.py` li importera' da qui)*.
2. `primo_ordine/_misura_verso_l2.py` — stazionarieta', `h` del grumo, `beta` verificato,
   la misura differenziale, **il caso che deve fallire**, la scansione in `x`, la robustezza,
   il vuoto totale.
3. I referti in **`doc/referti_l2/`**, **dal codice gia' committato**.
4. `RIPRESA` e mappa: `L2` aperto, primo pezzo fatto *(o perche' no)*, **il verso misurato**.
   Poi **STOP**: la forma di `cs(Lambda)` e' la prossima decisione di Luca.
