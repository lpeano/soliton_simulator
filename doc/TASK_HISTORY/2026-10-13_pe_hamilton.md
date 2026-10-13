# `(P-e)` — **LA RISERVA DELLA VERIFICA ESTERNA SU `(A)`: il conto, e `(A)` NON REGGE**

> **La riserva, che il mandato mi fa aggiungere al piano:** *«nella derivazione di
> `1bfde50` lo sbilancio entra nel vuoto **PER DEFINIZIONE** (`Delta pi_k = -s_k`). Perche'
> sia meccanica e non contabilita' con un effetto di ritorno, `Delta pi_k` deve **uscire
> dalle equazioni di Hamilton** (`-dK/dtheta_k`), non essere imposto. Il test `P4` mostra
> che l'effetto esiste, **non che la struttura sia coerente**.»*

> ### ⛔ **SENZA CODICE: e' un conto a carta.** ### **E l'esito e' NEGATIVO, quindi va a
> Luca col ripiego `(C)` — non ci passo da solo.**

---

## 1. IL CONTO, in sei righe

La derivazione di `1bfde50` aveva posto, con `(theta_k, pi_k)` **coniugate**:

> **`K = E(psi, phi; theta) + somma_k f(pi_k)`**

Le **due** equazioni di Hamilton sono:

| | l'equazione | che cosa ne avevo fatto |
|---|---|---|
| `1` | **`d theta_k / dt = dK / d pi_k = f'(pi_k)`** | ### ✅ **USATA:** da qui `cs_k = f'(pi_k)` |
| `2` | **`d pi_k / dt = - dK / d theta_k = - dE / d theta_k`** | ### ⛔ **SALTATA:** avevo messo `Delta pi_k = -s_k` **a mano** |

### ⭐ **Quindi la coerenza chiede una cosa sola, e si scrive:**

> **`dE / d theta_k = s_k / dt`**

---

## 2. ⛔⛔ E LA RISPOSTA E' **ZERO**: `E` NON DIPENDE DA `theta_k`

> **`E = Re<psi|W psi> + somma_k Lambda_k G(h_k / Lambda_k)`**

### ⛔ **Guardo i suoi argomenti, uno per uno, e `theta_k` NON C'E':**

| | il termine | da che cosa dipende | contiene `theta_k`? |
|---|---|---|---|
| `1` | `Re<psi\|W psi>` | **`psi`** e la geometria *(`n`, `U`)* | ### ⛔ **no** |
| `2` | `Lambda_k = somma \|phi_h\|^2` | il **MODULO** di `phi` | ### ⛔ **no** |
| `3` | `h_k = somma s . n` | **`psi`** e i versori | ### ⛔ **no** |

### ⭐ **`E` E' UNA FUNZIONE DELLO STATO `(psi, phi)` E DELLA GEOMETRIA, E NIENT'ALTRO.**
### ⛔ **Quindi `dE / d theta_k = 0`, e l'equazione `2` da':**

> ### ⛔⛔ **`d pi_k / dt = 0`** — ### **`pi_k` NON CAMBIA AFFATTO.**

### ⛔ **E questo CONTRADDICE `Delta pi_k = -s_k`, che avevo imposto.**
### ✅ **La verifica esterna aveva ragione, e la conclusione e' netta: `(A)` COSI' COM'E'
NON E' MECCANICA.** E' **contabilita' con un effetto di ritorno** — e il mio `P4` non lo
avrebbe mai visto.

### ⭐ **E NOTO PERCHE' `P4` NON BASTAVA, perche' e' la lezione del pezzo:** `P4` *(due corse
con `pi_k(0)` diverso divergono)* ### **passerebbe anche con `pi` imposto a mano**, perche'
basta che `cs_k` **dipenda** da `pi_k`. ### ⛔ **`P4` testava il CANALE DI RITORNO, non la
COERENZA DELLA STRUTTURA** — ed e' esattamente la distinzione che il mandato fa.

---

## 3. ⚠ E `A-ii` NON SALVA NIENTE — *l'ho controllato, perche' ci speravo*

In `A-ii` la coppia coniugata sarebbe **`(alpha_k, n_k)`**, cioe' **la fase e il modulo
quadrato del vuoto**, che e' una coppia canonica **vera**. ### ⭐ **Allora `pi_k` sarebbe
`n_k` e il <<tempo proprio>> sarebbe `alpha_k`.** La seconda equazione diventa
`d n_k / dt = - dE / d alpha_k`.

### ⛔ **E ANCHE QUI FA ZERO:** `E` dipende da `phi` **solo attraverso `Lambda_k`**, che e'
**una somma di MODULI** — ### **la FASE di `phi` non entra in `E` da nessuna parte.**

> ### ⛔ **Quindi il fallimento e' lo STESSO in `A-i` e in `A-ii`, e non e' un dettaglio
> della realizzazione: e' STRUTTURALE.** ### **`E` non ha un partner coniugato per `pi_k`,
> in nessuna delle due letture.**

---

## 4. ⭐ PERCHE' IL TRUCCO NON SI APPLICA — *la diagnosi, e non e' un dettaglio tecnico*

### ⭐ **Il trucco dello spazio delle fasi esteso cura UN tipo di non conservazione:** quella
di un'hamiltoniana che **dipende esplicitamente dal tempo**. La' `dH/dt = dH/dt|parziale`,
e `p_t` assorbe **proprio quella derivata parziale**.

### ⛔ **MA LA NOSTRA NON CONSERVAZIONE E' DI UN ALTRO TIPO, e il nome ce l'ha:** `s_k` e'
**la non-commutazione di `W` e `N`** — e la diagnosi che Luca ha accettato lo dice:
### **due generatori con due orologi.** ### ⚠ **E `W` non e' <<un'hamiltoniana che dipende
dal tempo>>: non e' un flusso AFFATTO.** E' **una mappa fissa**, un cammino a tempo
discreto *(e lo avevo misurato: `4` pezzi su `7` non dipendono da `dtau`)*.

> ### ⛔ **Quindi il problema non e' che `E` perde energia PER VIA DEL TEMPO: e' che LA
> MAPPA COMPOSTA NON HA UN'HAMILTONIANA.** ### **E lo spazio delle fasi esteso non crea
> un'hamiltoniana che non c'e'.**

---

## 5. ⭐ QUAL'E' L'OGGETTO GIUSTO, SECONDO ME — *e `DOMANDA-QUANTITA-CONSERVATA` lo aveva gia' nominato*

Per una mappa **periodica** *(e il tick lo e': si ripete identico)* l'oggetto conservato
**esattamente** non e' `E`: e' la **QUASI-ENERGIA**, cioe' il generatore della mappa di un
periodo —

> **`U_tick = exp(-i H_eff T)`** , e ### **`H_eff` e' conservata PER COSTRUZIONE.**

### ⭐ **E NON LO STO INVENTANDO ADESSO:** `[[DOMANDA-QUANTITA-CONSERVATA]]` dice, con
queste parole, *«Per la LINEARE: la QUASI-ENERGIA. Per la NON LINEARE: DA PROVARE.»*
### ✅ **Era gia' scritto, e il conto di oggi dice PERCHE' era la risposta giusta.**

### ⛔ **E IL PROBLEMA DELLA QUASI-ENERGIA E' LA LOCALITA', non l'esistenza:** `H_eff` e' il
**logaritmo** di `U_tick`, e un logaritmo di operatore ### **non ha una portata finita in
generale.** ### ⚠ **E questo riapre un dubbio che la scheda di `D-ENERGIA` diceva chiuso:**
la' c'era scritto *«NIENTE LOGARITMO DELL'OPERATORE, quindi NESSUNA AMBIGUITA' DI RAMO»*,
### **e quel vantaggio si perde se la grandezza giusta e' proprio il logaritmo.**

### ⛔ **E C'E' UN FATTO MISURATO CHE RENDE LA COSA PIU' DELICATA, non meno:** `a67b68f` ha
misurato che ### **le bande vanno alla PARITA'**, cioe' il sistema **termalizza** nel grado
di liberta' delle bande. ### ⚠ **Per i sistemi di Floquet, termalizzazione e localita' della
quasi-energia sono in tensione**: un sistema che termalizza **non ha** una quasi-energia
locale conservata su tempi lunghi. ### **Quindi la misura di `a67b68f` e' un indizio CONTRO
la localita' di `H_eff`**, non a favore.

---

## 6. ⛔ CHE COSA SERVIREBBE PER SALVARE `(A)`, e perche' e' una DECISIONE

### ⭐ **La riparazione e' UNA, e si scrive in una riga:** perche' l'equazione `2` dia
qualcosa, ### **`E` deve dipendere ESPLICITAMENTE da `theta_k`** *(o dalla fase del vuoto,
in `A-ii`)*.

### ⛔ **E questo vuol dire AGGIUNGERE UN TERMINE A `E`**, cioe' ### **una legge nuova** — e
`9-ter` chiede di contarle: ### **da `3` a `4`, e questa volta la giustificazione NON c'e'
ancora**, perche' il termine andrebbe **scelto** per far tornare l'equazione.
### ⚠ **E un termine scelto per far tornare un'equazione e' esattamente cio' che
`SCARTATA-SAKHAROV-C-ESPLICITA` critica**, nella sua forma: *«un termine aggiunto per
ottenere un risultato e' il contrario di una legge derivata»*.

> ### ⛔ **QUINDI MI FERMO, E LO PORTO A LUCA**, come il mandato dice: *«se la derivazione
> fallisce, scrivi PERCHE' e proponi a Luca il passaggio a `(C)`: non passarci da solo»*.
> ### ✅ **Scrivo il perche', e NON ci passo da solo.**

---

## 7. LE TRE VIE, E LA MIA RACCOMANDAZIONE SEPARATA

| | la via | che cosa costa | che cosa salva |
|---|---|---|---|
| `i` | **aggiungere a `E` un termine che dipende da `theta_k`** | ### ⛔ **una legge nuova, SCELTA e non derivata** | `(A)` diventa meccanica |
| `ii` | **la QUASI-ENERGIA** come grandezza conservata | ### ⛔ **la LOCALITA' non e' garantita** *(e' un logaritmo di operatore)*, e `a67b68f` e' un **indizio contro** | la conservazione e' **esatta per costruzione** |
| `iii` | ### **il ripiego `(C)`**: si rinuncia a un'energia conservata, e si tengono **le grandezze protette da simmetrie** *(la norma, l'eventuale carica)* | ### ⛔ **la decisione `10` va riscritta** su quelle | ### ✅ **non si aggiunge NIENTE**, e la direzione resta pulita |

### ⭐ **LA MIA RACCOMANDAZIONE, SEPARATA DALLA DECISIONE: `(iii)`**, e per **tre** ragioni.

1. ### ⛔ **`(i)` aggiunge una legge SCELTA per far tornare un conto**, che e' il tipo di
   mossa che questo repo rifiuta altrove — e **la rifiuterei anch'io se la proponesse un
   altro.**
2. ### ⚠ **`(ii)` non e' esclusa, ma oggi NON E' VERIFICABILE:** la localita' di `H_eff` si
   deciderebbe con una misura **che non ho fatto**, e il solo dato che ho *(la
   termalizzazione delle bande)* ### **va nella direzione sbagliata.**
3. ### ✅ **`(iii)` E' GIA' SCRITTO come criterio di riapertura** in
   `[[DOMANDA-QUANTITA-CONSERVATA]]`, e ### **la strada `(3)` non ha bisogno di un'energia
   conservata**: ha bisogno di una **carica** *(globale)* e di un **segno locale** — e
   **quelli sono protetti da simmetrie, non da un'hamiltoniana.**

### ⚠ **E DICO CHE COSA MI FAREBBE CAMBIARE IDEA, perche' una raccomandazione senza questo
e' una preferenza:** se `H_eff` avesse una **portata finita misurata** su una scena di
prova, ### **`(ii)` diventerebbe la via migliore di tutte** — e sarebbe **una misura**, non
un argomento.

---

## 8. LA STELLA POLARE

| | la domanda | la risposta |
|--:|---|---|
| **1** | conserva **localmente**? | ### ⛔ **NO, e questo pezzo lo DIMOSTRA invece di misurarlo:** `Delta pi_k = -s_k` **non segue** dalle equazioni di Hamilton, quindi la conservazione locale di `E~` era **un'identita' imposta.** ### **`A14` chiede di dichiarare la violazione: dichiarata** |
| **2** | **quale gradino**? | ### **NESSUNO: un conto a carta, e il suo esito e' NEGATIVO** |
| **3** | **aggiunge un numero o una legge**? | ### ✅ **Nessuno: non propongo niente.** ### ⛔ **E il risultato TOGLIE una strada dal tavolo** — `(A)` com'era scritta |
| **4** | tocca `rho`, `c_s` o **il SEGNO**? | ### ⚠ **`c_s` resta nel conto** *(`cs_k = f'(pi_k)` vale ancora: era l'equazione `1`)*, ### **ma non c'e' piu' niente che muova `pi_k`** |
| **5** | **emergente o imposto**? | ### ⛔ **IMPOSTO, ed e' il difetto:** `Delta pi_k = -s_k` era **messo a mano**, e il conto di oggi lo mostra |

---

## 9. TODO

1. registrare **`[[DOMANDA-A-NON-E-MECCANICA]]`** con le tre vie e la raccomandazione
   separata.
2. ### ⛔ **ANNOTARE il task history di `1bfde50`** *(non riscriverlo)*: la derivazione
   usava **una sola** equazione di Hamilton.
3. ### ⚠ **E le previsioni `P1`..`P6` di quel file RESTANO SCRITTE, ma `P4` va marcata:**
   ### **non era il test della coerenza, e lo dico.**
