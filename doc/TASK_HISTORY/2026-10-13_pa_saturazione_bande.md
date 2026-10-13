# `(P-a)` — **UNA SATURAZIONE CHE NON MESCOLA LE BANDE: la derivazione**

> **Il mandato:** *«Deriva quali forme del flusso conservano `N+ - N-` (cioe' commutano con
> il proiettore di banda) restando **locali, esatte e `C`-simmetriche**. Se nessuna forma
> locale lo fa, dichiaralo: e' un ostacolo vero alla strada `(3)`.»*

> ### ⛔ **SENZA CODICE**, come il mandato chiede. ### **E le previsioni erano scritte in
> `doc/TASK_HISTORY/2026-10-13_domini_separati.md`, committato in `3b26977` — prima di
> questa.**

---

## 1. LA CONDIZIONE ESATTA, in quattro righe di conto

Un flusso hamiltoniano `d psi / d tau = -i A psi` con `A` hermitiano *(anche dipendente
dallo stato)*. Allora

> `d/d tau <psi|P+|psi> = <-iA psi|P+ psi> + <psi|P+ (-iA psi)>`
> `                     = i <psi| A P+ |psi> - i <psi| P+ A |psi>`
> ### **`= i <psi| [A, P+] |psi>`**

### ✅ **Quindi `N+` si conserva per OGNI stato se e solo se `[A, P+] = 0`.**

### ⭐ **E `[A, P+] = 0` vuol dire una cosa precisa:** siccome `P+ + P- + P0 = I`,
### **`A` deve essere DIAGONALE A BLOCCHI rispetto alle bande:**
`A = P+ A P+ + P- A P- + P0 A P0`.

### ⚠ **Nota che NON serve `[A, W] = 0`:** quella e' **sufficiente** *(se `A` commuta con
`W` commuta con ogni funzione di `W`)*, ### **non necessaria** — `A` puo' mescolare
**dentro** una banda.

---

## 2. ⭐ LA FAMIGLIA CHE FUNZIONA ESISTE, ED E' COSTRUTTIVA — *e non me l'aspettavo*

### ⛔ **Nel piano avevo previsto che NESSUNA forma locale funzionasse.** ### ⚠ **La
previsione era sbagliata, e la famiglia si scrive:**

> ### ⭐ **`A = somma_j ( c_j W^j + coniugato(c_j) W^{-j} )`**, con `c_j` **scalari** e la
> somma **FINITA**.

| | la proprieta' | perche' vale |
|---|---|---|
| ✅ **hermitiana** | `W` e' unitaria, quindi `W^{-j} = (W^j)^dagger`: la somma e' `X + X^dagger` |
| ✅ **commuta con `W`** | e' un polinomio in `W` e `W^{-1}` ⟹ ### **commuta con ogni funzione di `W`, quindi con `P+`** |
| ✅ **LOCALE, con portata FINITA** | `W` ha **portata `1` arco** *(moneta sull'estremita', Grover sul nodo, spostamento di un arco)*, quindi `W^j` ha portata `j`: ### **la portata e' il GRADO**, e si dichiara |
| ✅ **`C`-simmetrica** | sotto `C`, `W(U) -> W(C U)` *(misurato: `0.000e+00`)*, quindi `g(W)` va in `g(W(C U))`: ### **covariante, non rotta** |
| ✅ **esatta** | `exp(-i A tau)` e' **una funzione di `W`**: non c'e' niente da approssimare |

### ⭐ **E CHE COSA FA QUESTA FAMIGLIA, concretamente:** `exp(-iA tau)` ruota **le fasi
dentro ciascuna banda** e ### **non sposta NIENTE fra le bande.** ### ✅ **E' esattamente
cio' che `(P-a)` chiede.**

---

## 3. ⛔⛔ MA L'OSTACOLO E' VERO, E LA SUA FORMA E' PRECISA — **non e' la localita': e' il GLOBALE**

### `3.1` IL FATTO CHE BLOCCA

### ⛔ **La famiglia del par. `2` e' LINEARE in `psi`.** I `c_j` sono **scalari**, non
dipendono dal nodo. ### **E una saturazione DEVE essere non lineare: e' il suo scopo** —
`N = Lambda G(h/Lambda)` esiste **per limitare un'ampiezza**, e una legge lineare
### **non limita niente.**

### `3.2` ⭐ E SE SI RENDONO I COEFFICIENTI DIPENDENTI DALLO STATO?

Due casi, e **si escludono a vicenda**:

| | `c_j` dipende da | commuta con `P+`? | `F10` lo ammette? |
|---|---|---|---|
| `a` | uno **scalare GLOBALE** dello stato *(per esempio `<psi\|W^j\|psi>`)* | ### ✅ **SI':** i `c_j` restano **numeri**, quindi `A` resta **un polinomio in `W`** | ### ⛔ **NO: `F10` vieta i RIFERIMENTI GLOBALI** |
| `b` | grandezze **DI NODO** *(`h_k`, `Lambda_k`)* | ### ⛔ **NO:** `A = somma_k a_k (...)` **non e' piu' un polinomio in `W`**, e i suoi elementi fuori banda non si annullano | ### ✅ **si'** |

> ### ⛔⛔ **ECCO L'OSTACOLO, nella sua forma esatta:**
>
> ### **La conservazione delle bande chiede che il generatore sia una FUNZIONE DI `W` con
> COEFFICIENTI GLOBALI. I coefficienti DI NODO la rompono. E `CARTA-FISICA-SIMULATORE/F10`
> VIETA i riferimenti globali.**

### ⭐ **E DETTO IN UN'ALTRA FORMA, che e' quella che porto a Luca:**

> ### ⛔ **NON SI POSSONO AVERE INSIEME, TUTTE E CINQUE: locale · esatta · `C`-simmetrica ·
> CONSERVA LE BANDE · NON LINEARE.**
>
> ### **Togliendo la NON LINEARITA' si ottiene la famiglia del par. `2`** *(che esiste e
> funziona)*. ### **Tenendola, servono coefficienti globali, che `F10` vieta.**

### `3.3` ⚠ LA PORTATA DELL'ARGOMENTO, dichiarata

### ✅ **La parte COSTRUTTIVA** *(par. `2`)* **e' una dimostrazione**: la famiglia e'
esibita e le cinque proprieta' si verificano una per una.

### ⚠ **La parte NEGATIVA del caso `b` e' un argomento GENERICO, e lo dico:** su una scena
**traslazionalmente invariante** si vede in modo pulito — `W` e' diagonale a blocchi in
<<momento>>, i suoi autovettori **ruotano con il momento**, e un generatore **diagonale sui
nodi e non costante** ha elementi fuori diagonale che ### **collegano momenti diversi, e
quindi bande diverse.** ### ⛔ **Su una scena qualunque NON ho una dimostrazione: ho un
argomento di genericita'** — e ### **<<generico>> non e' <<sempre>>.**
### ⚠ **Se qualcuno esibisse un controesempio, cadrebbe questo paragrafo e NON il par. `2`.**

---

## 4. ⭐ E L'OSTACOLO **NON BLOCCA LA STRADA `(3)`** — *le due vie d'uscita erano scritte prima*

### `4.1` LA VIA `②` E' LA PIU' FORTE, E CAMBIA LA DOMANDA

### ⛔ **Il parametro d'ordine NON DEVE essere `N+ - N-`.** Nel piano avevo gia' trovato
*(scrivendolo, e prima di questa derivazione)* che:

1. i proiettori di banda **presuppongono `W` FISSA**, e con la **`U` dinamica** *(gia'
   decisa)* ### **`N+` non e' nemmeno ben definita lungo l'evoluzione**;
2. esiste una densita' **`C`-dispari e LOCALE**:
   ### **`q_h = Im[ coniugato(psi_h) (W psi)_h ]`**.

> ### ⭐ **Allora `(P-a)` chiedeva la cosa sbagliata.** La strada `(3)` non ha bisogno che
> **le bande** si conservino: ha bisogno che ### **il segno locale `q` si ORDINI invece di
> spegnersi.** ### **E `q` non e' una popolazione di banda: e' una densita'.**

### ⚠ **E questo NON e' un modo di aggirare l'ostacolo: e' un cambio di oggetto, e va
dichiarato come tale.** ### ⛔ **Resta vero che `N+ - N-` non si conserva**, e resta vero
che ### **con la `C` esatta e all'equilibrio la parita' e' l'esito** — cio' che cambia e'
### **che <<equilibrio>> non e' garantito se c'e' un ordinamento.**

### `4.2` LA VIA `①`: IL RAPPORTO FRA DUE RITMI

### ⭐ **Allora la domanda diventa quantitativa:** il **ritmo del mescolamento** *(che la
saturazione produce, misurato: un fattore `623` in `~1000` tick)* contro il **ritmo
dell'ordinamento** *(che il termine di `(P-b)` produce)*.
### ✅ **Se l'ordinamento vince, i domini si formano NONOSTANTE il mescolamento.**
### ⛔ **E questo si MISURA, non si deriva:** e' `(P-d)`.

### ⚠ **E ha una conseguenza sull'ORDINE del piano**, che non cambio da solo: ### **`(P-d)`
verrebbe prima di una conclusione su `(P-a)`.** Il piano lo aveva gia' previsto, al par. `7`.

---

## 5. ⭐ UN RISULTATO CHE NON CERCAVO — *e che mi sembra il piu' utile dei tre*

### ⭐ **La famiglia del par. `2` E' UNA LEGGE DISPONIBILE, anche se non risolve `(P-a)`.**
`A = somma_j (c_j W^j + c.c.)` e' ### **locale, esatta, `C`-simmetrica, conserva le bande,
conserva la norma**, e la sua **portata e' il grado** — ### **si dichiara, non si scopre.**

### ⚠ **E con `c_j` reali e `j = 1` si riduce a `A = c (W + W^dagger)`, cioe' alla PARTE
HERMITIANA di `W`:** ### **e' la cosa piu' semplice della famiglia**, ha portata `1` arco,
e ### **la sua energia e' PROPRIO `Re<psi|W psi>`** — il primo termine dell'energia
promossa.

> ### ⛔ **NON LA PROPONGO COME SATURAZIONE** *(e' lineare: non satura)*, e non la propongo
> come niente. ### ✅ **La registro perche' e' un FATTO sulla struttura:** se un giorno
> servira' un pezzo **che non mescola le bande**, ### **la famiglia e' questa, e si sa
> perche'.**

---

## 6. CHE COSA VA A LUCA — *una domanda, con la raccomandazione separata*

**`[[DOMANDA-BANDE-O-SEGNO-LOCALE]]`** — *la registro, e la metto in*
`DA_DECIDERE_LUCA.md`.

| | |
|---|---|
| **la domanda** | il parametro d'ordine della strada `(3)` e' **`N+ - N-`** *(le popolazioni di banda)* oppure **`q_h`** *(il segno locale)*? E se e' `q_h`, si accetta che `(P-a)` **resti un ostacolo dichiarato** e che la questione diventi **il rapporto fra due ritmi**, da misurare in `(P-d)`? |
| ### ⭐ **la mia raccomandazione** | ### **`q_h`**, e per **tre** ragioni — e nessuna e' <<cosi' l'ostacolo sparisce>> |
| `1` | `N+` **non e' definita** con `W` dinamica, che e' **gia' decisa**: un parametro d'ordine che **cessa di esistere** quando una decisione presa entra in vigore ### **non e' un parametro d'ordine** |
| `2` | `q_h` e' **locale** *(un prodotto per estremita')*, mentre `N+` costa `O((4m)^3)` ed e' **globale**: e `F10` vieta i riferimenti globali ### **nelle leggi**, quindi un ordine costruito su `N+` **non potrebbe entrare in una legge** |
| `3` | la `C`-disparita' di `q` ### **la derivo** dalla misura di `9c46a68`, non la assumo |
| ### ⚠ **e che cosa NON so** | se `q_h` sia **dispari sotto `C` ESTREMITA' PER ESTREMITA'**: ### **la disparita' che ho derivato e' GLOBALE.** E' la previsione `b2` del piano, e ### **va misurata prima di costruirci sopra** |

---

## 7. LA STELLA POLARE

| | la domanda | la risposta |
|--:|---|---|
| **1** | conserva **localmente**? | ### ⚠ **La famiglia del par. `2` conserva le bande ESATTAMENTE, ma sono grandezze GLOBALI.** ### **Il pezzo non promuove niente, quindi `A14` non e' in gioco qui** |
| **2** | **quale gradino**? | ### **NESSUNO: e' una derivazione, senza codice e senza misura** |
| **3** | **aggiunge un numero o una legge**? | ### ✅ **Nessuno dei due: non propongo nessuna legge.** ### ⛔ **E il risultato NEGATIVO ne TOGLIE una dal tavolo:** <<una saturazione non lineare che conserva le bande>> ### **non esiste sotto `F10`**, quindi non va cercata |
| **4** | tocca `rho`, `c_s` o **il SEGNO**? | ### ⭐ **Il SEGNO: tutto il pezzo e' su che cosa sia il segno** — una popolazione di banda o una densita' locale |
| **5** | **emergente o imposto**? | ### ⭐ **L'ostacolo e' EMERGENTE: viene da `F10` piu' la struttura spettrale di `W`**, non da una scelta. ### **E la famiglia del par. `2` e' DERIVATA, non inventata** |

---

## 8. TODO DEL NEXT STEP

1. ### ⛔ **ASPETTA LUCA su `[[DOMANDA-BANDE-O-SEGNO-LOCALE]]`:** se il parametro d'ordine
   e' `q_h`, ### **tutto `(P-b)` si scrive su `q`**; se e' `N+ - N-`, ### **`(P-a)` e' un
   ostacolo che blocca.**
2. e **intanto**, cio' che **non dipende** da quella risposta: ### ⭐ **`(P-e)`**, il conto
   `dE/d theta_k` contro `s_k/dt` — ### **e' un conto a carta e non dipende da niente.**
