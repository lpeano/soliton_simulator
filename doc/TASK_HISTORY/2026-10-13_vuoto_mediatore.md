# LA STRADA `(A)`: **IL VUOTO COME MEDIATORE** — derivazione, senza codice

> **Decisione di Luca, 2026-10-13 11:42:** *«Lo sbilancio di energia di ogni tick **NON e'
> perso**: va nel vuoto locale e ne torna. [...] La variabile che tiene il conto e' il
> **TEMPO PROPRIO del nodo come COPPIA CONIUGATA dell'energia**. [...] In meccanica,
> rendere il tempo una variabile dinamica fa tornare conservata l'energia estesa, e qui va
> fatto **NODO PER NODO**.»*
>
> **E la condizione che separa la fisica dalla contabilita', alla lettera:** *«una
> variabile del vuoto che si limita a CONTARE l'errore rende `E` conservata **per
> costruzione** e NON significa niente. La legge e' fisica **SOLO SE** l'energia assorbita
> **AGISCE INDIETRO** sulla dinamica.»*

> ### ✅ **Questo file si committa PRIMA del codice.** ### ⛔ **E il mandato dice
> <<SENZA CODICE>>: qui non c'e' nessuna misura, solo la derivazione e le previsioni.**

---

## 1. DA DOVE SI PARTE — *il fatto misurato, e la sua forma esatta*

Il bilancio locale, **misurato** in `db328b9` e con la corrente costruita in `0080cf3`:

> **`Delta E_k = (div J)_k + s_k`**

| | il pezzo | che cosa se ne sa, MISURATO |
|---|---|---|
| `J` | la **corrente locale** del pezzo lineare | esiste, **portata `3` archi**, continuita' a `2.9`–`70.4` ulp |
| `s_k` | la **sorgente** per nodo | **`O(1)` in `dtau`** *(rapporti `1.001`, `0.984`, `0.993`)*, e vale **circa la META'** di `Delta E_k` |
| `somma_k s_k` | lo **sbilancio globale** | **non zero**: e' `Delta E` del tick |

### ⭐ **E LA DIAGNOSI DI LUCA DICE CHE COS'E' `s_k`, e lo dice in una riga:** il tick ha
**due generatori con due orologi**. La camminata lineare e' **una mappa fissa** *(orologio:
il contatore dei tick)* e conserva `Re<psi|W psi>` **per identita'**; la saturazione e' **il
flusso di un'hamiltoniana per un tempo `dtau`** *(orologio: il tempo proprio)*.
### ⛔ **Quindi `s_k` E' ESATTAMENTE LA NON-COMMUTAZIONE DEI DUE PEZZI**, nodo per nodo —
non un errore numerico, non un troncamento: ### **e' il termine di Floquet.**

---

## 2. LA DERIVAZIONE — *e il conto che la rende obbligata, non scelta*

### `2.1` ⭐ **LA MECCANICA LO FA GIA', E IL CONTO E' STANDARD**

Per un'hamiltoniana che dipende dal tempo, `dH/dt = dH/dt|parziale`, cioe' **`H` non si
conserva**. La cura classica non e' un rattoppo: si **estende lo spazio delle fasi** con la
coppia **`(t, p_t)`** e si definisce

> **`K = H(q, p, t) + p_t`**

`K` **non dipende dal tempo**, quindi **si conserva**; e l'equazione di Hamilton da'
**`dp_t/dt = - dH/dt|parziale`**, cioe' ### **`p_t` assorbe ESATTAMENTE l'energia che `H`
perde.** ### ⚠ **E `p_t` non e' un contatore: e' il momento coniugato del tempo**, e questo
e' il punto che fa la differenza fra fisica e contabilita'.

### `2.2` **TRASPOSTO NODO PER NODO** — *la coppia coniugata di `F7` e `F8`*

`CARTA-FISICA-SIMULATORE/F7` **cabla il posto**: *«TEMPO PROPRIO LOCALE in OGNI legge che
evolve (`dtau_k = cs_k per dt`), e `cs` locale E' la velocita' locale della luce, la STESSA
grandezza: il POSTO e' cablato, la FORMA e' aperta»*. E
`CARTA-FISICA-SIMULATORE/F8` dice che le memorie entrano **solo come COPPIE CONIUGATE**.

> ### ⭐ **Allora la coppia e' questa, e non e' una scelta mia: e' i due punti della carta
> messi insieme.**
>
> | la variabile | che cos'e' |
> |---|---|
> | **`theta_k`** | il **tempo proprio** del nodo `k` — la variabile che `F7` cabla |
> | **`pi_k`** | il suo **momento coniugato**, che **E' l'energia tenuta nel vuoto del nodo** |

E l'energia estesa, **nodo per nodo**:

> **`E~_k = E_k + pi_k`**,  con  **`Delta pi_k = - s_k`** per tick.

### ✅ **E ALLORA LA CONSERVAZIONE E' ESATTA, E LOCALE:**

> **`Delta E~_k = Delta E_k - s_k = (div J)_k`**

### ⭐ **Cioe' la continuita' dell'energia estesa CHIUDE NODO PER NODO, SENZA SORGENTE, con
la corrente di `0080cf3`** — quella di portata `3` archi, gia' costruita e sigillata. E
sommando su `k`, siccome `somma_k (div J)_k = 0` **telescopia**:

> **`Delta E~ = 0` ESATTAMENTE.**

### `2.3` ⛔ **E QUI MI FERMO A DIRE CHE QUESTO, DA SOLO, E' CONTABILITA'**

### ⛔ **Il paragrafo `2.2` NON E' FISICA, ed e' precisamente cio' che Luca ha scritto:**
avendo **definito** `pi_k` come *«meno lo sbilancio»*, la conservazione di `E~`
### **e' un'identita' algebrica, non una misura.** ### ⚠ **Una misura che la verificasse
tornerebbe a ulp e non direbbe NIENTE**, ed e' il motivo per cui la previsione `P1` qui
sotto e' dichiarata **non informativa**.

### ⭐ **IL CONTENUTO FISICO STA IN DUE POSTI, E SOLO IN DUE:**

1. ### **che `s_k` abbia una FORMA CHIUSA E LOCALE**, invece di essere *«cio' che resta»*;
2. ### **che `pi_k` AGISCA INDIETRO** sulla dinamica.

---

## 3. ⭐ IL PRIMO CONTENUTO: **`s_k` HA UNA FORMA CHIUSA, E UNA PORTATA FINITA**

### ⛔ **Una variabile definita come residuo non e' una legge**, e non e' nemmeno
ovviamente **reversibile**: *«cio' che resta»* dipende da **come ho fatto il conto**.
### ✅ **Ma `s_k` non e' un residuo: e' la differenza di DUE MAPPE ESATTAMENTE NOTE**, e si
scrive:

> **`s_k = E_k(N(dtau/2) W N(dtau/2) psi) - E_k(psi) - (div J)_k`**

### ⭐ **Ogni pezzo e' una funzione chiusa dello stato**, e da qui segue **la portata**:

| | il pezzo | la sua portata |
|---|---|---|
| `E_k(psi)` | `e_h = Re[conj(psi_h) (W psi)_h]` sulle estremita' di `k`, piu' il vuoto del nodo | **`1` arco** *(`W` muove di un arco)* |
| `E_k(tick(psi))` | lo stesso, dopo un tick | **`2` archi** |
| `N` | il flusso di saturazione | **`0` archi** *(dipende solo da `h_k` e `Lambda_k`)* |
| `(div J)_k` | con l'instradamento di `0080cf3` | **`3` archi** → il totale **`4`** |

### ⚠ **QUINDI LA PORTATA DELLA DINAMICA ESTESA LA DECIDE L'INSTRADAMENTO**, e non il
fenomeno: ### ⭐ **`Delta E_k` ha portata INTRINSECA `2`**, ed e' `J` che porta il conto a
`4`. ### ✅ **E la LIBERTA' DI RICIRCOLO che avevo dichiarato ieri — <<la corrente non e'
unica, come nel continuo a meno di un rotore>> — DIVENTA UNA SCELTA CON UN SIGNIFICATO
FISICO: sceglie la PORTATA.**

### ⛔ **E QUI C'E' UNA TENSIONE CON `CARTA-FISICA-SIMULATORE/F10`, e la dichiaro invece di
nasconderla:** `F10` chiede **scala minima UN ARCO** *(`A13`)*. Una dinamica in cui
`pi_k` si aggiorna con un `s_k` di portata `2` *(o `4`)* ### **muove informazione di `2`
archi per tick**, cioe' ### **un cono piu' largo di un arco per tick.**

| | la lettura | che cosa comporta |
|---|---|---|
| `1` | `J` e' **un osservatore** *(una contabilita' di dove e' finita l'energia)*, non un canale | ### ✅ **nessun problema**: il cono resta quello della dinamica |
| `2` | ### ⛔ **ma `pi_k` E' DINAMICO**, e il suo aggiornamento usa `s_k` | ### **allora il cono della teoria E' la portata di `s_k`**, e va dichiarato |

### ⭐ **E LA CURA NON LA DECIDO IO, MA LA RACCOMANDAZIONE E' PRECISA:** si sceglie
l'instradamento **piu' corto** *(portata `1` arco dove possibile)*, cosi' il cono della
dinamica estesa resta ### **un arco per tick**, e la portata `2` di `Delta E_k` si spezza in
**due passi di un arco** -- che e' esattamente cio' che `W` fa.
### ⚠ **E' una DOMANDA**, non una decisione: `[[DOMANDA-PORTATA-DEL-VUOTO-MEDIATORE]]`.

---

## 4. ⭐⭐ IL SECONDO CONTENUTO: **L'EFFETTO DI RITORNO**, e la coppia coniugata lo FORZA

### ✅ **QUESTA E' LA PARTE CHE RISPONDE ALLA CONDIZIONE DI LUCA, e non e' un innesto: viene
dall'equazione di Hamilton della coppia che ho scritto nel `2.2`.**

Se `(theta_k, pi_k)` sono **coniugate** e l'hamiltoniana estesa e'
`K = E(psi, phi; theta) + somma_k f(pi_k)`, allora

> **`d theta_k / dt = dK/d pi_k = f'(pi_k)`**

### ⭐ **Cioe' il RITMO del tempo proprio del nodo e' funzione dell'energia che il nodo ha
nel vuoto.** E `F7` dice `dtau_k = cs_k per dt`, dove `cs_k` **e' la velocita' locale della
luce, la stessa grandezza**. Quindi:

> ### ⭐⭐ **`cs_k = f'(pi_k)`**
>
> ### **La velocita' locale della luce E' la derivata dell'energia del vuoto rispetto
> all'energia che ci ha messo dentro.**

### ⛔ **E QUESTO NON E' UN EFFETTO CHE HO AGGIUNTO PER SODDISFARE LA CONDIZIONE: e'
OBBLIGATO.** ### **Se `pi_k` e' il coniugato di `theta_k`, allora `pi_k` CAMBIA il ritmo di
`theta_k`: non c'e' modo di avere la coppia senza l'effetto.** ### ✅ **La contabilita' e'
proprio il caso `f' = costante`** — e allora `cs_k` non dipende da `pi_k`, la coppia e'
finta, e si ricade in `(C)`.

### ⭐ **E L'EFFETTO SI VEDE SULLA MATERIA, per il verso che `F7` cabla:** `dtau_k` entra in
**ogni legge che evolve**, quindi entra nel **flusso di saturazione** *(che gira per un tempo
`dtau_k/2`)*. ### **Un nodo che ha assorbito energia ha un `dtau_k` diverso, quindi la sua
saturazione gira di piu' o di meno: la materia LO SENTE.**

### ⚠ **E IL SECONDO CANALE CHE IL MANDATO NOMINA — `Lambda_k` — E' PIU' ECONOMICO MA HA UN
OSTACOLO MISURATO, e lo devo dire.**

| | la via | il costo | l'ostacolo |
|---|---|---|---|
| **`A-i`** | `pi_k` e' **una variabile nuova** per nodo, coniugata a `theta_k`; il ritorno e' `cs_k = f'(pi_k)` | **`1` variabile nuova** per nodo *(piu' `theta_k`, che `F7` cabla gia')* | — |
| **`A-ii`** | `pi_k` **non e' nuova**: e' l'ampiezza del vuoto, `pi_k = pi_k(Lambda_k)`; il ritorno e' **automatico**, perche' `E_vuoto = Lambda_k G(h_k/Lambda_k)` dipende da `Lambda_k` | ### ✅ **ZERO variabili nuove** — e `9-ter` preferisce questa | ### ⛔ **MISURATO il 2026-10-12: il flusso di saturazione CONSERVA `h` e `Lambda`** *(`1.9` ulp)*, **ed e' la CAUSA della sua esattezza** — due mezzi fanno l'intero **perche'** conserva i suoi coefficienti. ### **Farlo cambiare `Lambda` ROMPE quell'esattezza.** |

### ⭐ **E C'E' UN FATTO CHE RENDE `A-ii` PIU' BELLA DI QUANTO SEMBRI:** per un campo
complesso `phi = sqrt(n) exp(i alpha)`, la coppia **`(alpha, n)` E' CANONICA**. E il flusso
di saturazione ### **DA' GIA' UNA FASE A `phi`.** ### ⚠ **Quindi in `A-ii` il <<tempo
proprio del nodo>> sarebbe LETTERALMENTE LA FASE DEL SUO VUOTO, e l'energia assorbita la sua
AMPIEZZA** — e la coppia coniugata **esisterebbe gia' nella tabella**, senza aggiungere
niente.

### ⛔ **MA NON LA RACCOMANDO SENZA DIRE L'OSTACOLO**, che e' preciso: oggi il flusso
conserva `|phi|^2`, quindi `n` **non cambia**, quindi `pi_k` **non si muove**.
### **Perche' `A-ii` funzioni, il flusso deve cambiare `|phi|`, e allora la sua esattezza va
RIDIMOSTRATA.** ### **E' una DOMANDA:** `[[DOMANDA-QUALE-COPPIA-CONIUGATA-DEL-VUOTO]]`.

---

## 5. LA COMPATIBILITA' COI VINCOLI — *uno per uno, e dove c'e' un dubbio lo dico*

| | il vincolo | la risposta |
|---|---|---|
| **localita'** *(`F10`)* | `s_k` ha **forma chiusa** e portata **`2`** *(intrinseca)* o `4` *(col `J` di ieri)* | ### ✅ **locale, con portata DICHIARATA** |
| **cono causale** *(`A13`, scala minima un arco)* | la portata `> 1` arco per tick | ### ⛔ **TENSIONE DICHIARATA** *(par. `3`)*: si cura con l'instradamento piu' corto, e la scelta va a Luca |
| **reversibilita' esatta** *(`F10`)* | `s_k` e' una **funzione dello stato**, e il tick e' **esattamente invertibile** *(l'inverso del flusso annulla a `0.7` ulp; `W` e' unitario)* | ### ⚠ **NON LO SO ANCORA:** serve che l'aggiornamento di `pi_k` sia **simmetrico nel tempo**, e con una composizione di Strang ### **va MISURATO** — e' la previsione `P3` |
| **gauge `U(2)` di tutto il passo** *(`F10`)* | `E_k`, `h_k`, `Lambda_k` sono **invarianti di gauge** *(tracce e moduli)*; `s_k` e' una loro differenza; `pi_k` e' uno **scalare di nodo** | ### ✅ **invariante** |
| **la `C`** | sotto `C` *(completa: `psi -> i sigma_y psi*`, `phi -> phi*`, `U -> sigma_y U* sigma_y^-1`)* `E_k` e' **pari** e `s_k` lo e' con lei; `pi_k` e' **pari**; `theta_k` **pari** | ### ⚠ **lo CREDO e non l'ho misurato:** `P6`. ### ⛔ **E attenzione: se `pi_k` fosse DISPARI sarebbe una carica, non un calore** |
| **nessuna costante nuova** *(`F10`)* | la forma `f` **non e' un numero**: e' una **legge**, e `cs_k = f'(pi_k)` la lega a una grandezza che c'e' | ### ✅ **nessuna costante** — ma la **forma di `f` e' una DOMANDA** |
| **niente clip, niente pavimento** *(`F10`, `A11`)* | `cs_k = f'(pi_k)` potrebbe andare a zero o cambiare segno | ### ⛔ **E' IL PERICOLO VERO, e lo dichiaro:** la tentazione sara' **un pavimento su `cs_k`**, e `A11` lo vieta senza un errore trovato. ### **La forma `f` deve rendere `f' > 0` PER COSTRUZIONE**, non per clip |
| **nessun riferimento globale** *(`F10`)* | `pi_k` e' **per nodo**; lo scambio e' **lungo gli archi** *(`VUOTO-LOCALE-DETERMINISTICO`)*; nessuna somma globale entra in una legge | ### ✅ |
| **determinismo e reversibilita' dello scambio** *(`A15.3`, `VUOTO-LOCALE-DETERMINISTICO`)* | `Delta pi_k = -s_k` con `s_k` funzione chiusa dello stato: **deterministico**, e **nessuna temperatura obiettivo** | ### ✅ **e COINCIDE con la forma che Luca aveva gia' deciso** |
| **norme conservate anche attraverso le nascite** *(`F10`)* | `pi_k` di un nodo nuovo | ### ⛔ **NON DERIVATO: e' un POSTO APERTO.** Un nodo che nasce **porta un `pi` nuovo**, e da dove viene e' ### **la decisione `10` (<<il calore paga la nascita>>) riscritta su questa variabile** |

---

## 6. ⭐ LE PREVISIONI E LE SOGLIE — **scritte PRIMA dei numeri**

### ⛔ **E LA PRIMA E' DICHIARATA NON INFORMATIVA, perche' sarebbe disonesto contarla:**

| | la previsione | la soglia | che cosa decide |
|---|---|---|---|
| **`P1`** | `E~ = somma_k (E_k + pi_k)` si conserva **a ulp** | `< 100` ulp | ### ⛔ **NIENTE: e' l'identita' algebrica del par. `2.2`.** ### **La scrivo solo perche' se NON tornasse avrei sbagliato il conto** |
| **`P2`** | `s_k` ha **portata finita**, e la misuro | `<= 4` archi col `J` di ieri; ### ⭐ **`<= 2` con l'instradamento minimo** | se la portata **non si riduce a `2`**, la tensione col cono **non si cura** con l'instradamento, e la domanda cambia |
| **`P3`** | la **reversibilita'**: il passo esteso **inverso annulla** | `< 1000` ulp | ### ⚠ **NON LO SO**, e lo dico: se **non** annulla, `(A)` **viola `F10`** e si va verso `(C)` |
| **`P4`** | ### ⭐⭐ **L'EFFETTO DI RITORNO SI VEDE:** due corse identiche tranne `pi_k(0)` **DIVERGONO** in `psi`, e la divergenza **cresce con `|Delta pi|`** | divergenza relativa `> 1e-3` dopo `200` tick per `|Delta pi| ~ 1` | ### ⛔ **E' IL TEST DELLA CONDIZIONE DI LUCA.** ### **Se NON divergono, `(A)` e' contabilita' e lo scrivo** |
| **`P5`** | il calore **si conduce lungo gli archi**: un `pi` concentrato **si allarga** con un fronte `<=` portata per tick | il fronte **non** supera la portata dichiarata | se lo supera, la **localita'** e' rotta |
| **`P6`** | sotto la `C` **completa**, `pi_k` e' **PARI** | `< 100` ulp | se fosse **dispari**, `pi_k` ### **non e' un calore: e' una carica** — e cambia tutto |

### ⛔ **CHE COSA MI FAREBBE FERMARE**

1. se `P4` **fallisse** — cioe' se cambiare `pi_k(0)` **non cambiasse `psi`** — allora
   ### **la legge e' contabilita'**, e il mandato dice cosa fare: *«se la derivazione
   fallisce, scrivi PERCHE' e proponi a Luca il passaggio a `(C)`: **non passarci da
   solo**»*. ### ✅ **Non ci passo da solo.**
2. se `P3` **fallisse**, `(A)` viola la **reversibilita' esatta** di `F10`: stesso esito.
3. se per far funzionare `f` servisse **un pavimento su `cs_k`**, mi fermo: ### ⛔ **`A11`
   lo vieta senza un errore trovato**, e un `cs` che si azzera e' **un errore di forma,
   non un caso da tappare.**
4. se `P6` dicesse che `pi_k` e' **dispari** sotto `C`, ### **non e' un calore** e la
   derivazione va riscritta — **non aggiustata.**

---

## 7. ⚠ CHE COSA RESTA LIBERO, E VA A LUCA — *una domanda per voce*

| | la domanda | perche' non la decido io |
|---|---|---|
| `1` | **`[[DOMANDA-QUALE-COPPIA-CONIUGATA-DEL-VUOTO]]`** — `A-i` *(`pi` nuova, `cs_k = f'(pi_k)`)* oppure `A-ii` *(`pi` e' l'ampiezza del vuoto, coppia `(fase, |phi|^2)` gia' in tabella)* | `9-ter` preferisce `A-ii` *(zero variabili nuove)*, ### **ma rompe l'esattezza misurata del flusso.** E' un **compromesso fra due criteri**, non un calcolo |
| `2` | **`[[DOMANDA-PORTATA-DEL-VUOTO-MEDIATORE]]`** — quale instradamento, cioe' **quale cono** | la **liberta' di ricircolo** adesso **sceglie la portata della dinamica**: e' fisica, e `A13` e' in gioco |
| `3` | **`[[DOMANDA-LA-FORMA-DI-CS-DAL-VUOTO]]`** — la forma di `f`, cioe' **`cs_k = f'(pi_k)`** | e' il **posto `A1` della carta** *(«la forma di `cs` dal vuoto»)*, **dichiarato aperto**, e `A1` dice *«la legge, non il numero»* |
| `4` | **`[[DOMANDA-IL-PI-DEL-NODO-CHE-NASCE]]`** — il `pi` di un nodo nuovo | e' la **decisione `10`** *(«il calore paga la nascita»)* **riscritta su questa variabile**, e `DOMANDA-QUANTITA-CONSERVATA` dice che quella decisione **aspettava proprio un oggetto su cui scriversi** |

### ⭐ **E NOTO UNA COSA CHE NON MI ASPETTAVO, scrivendo:** `DOMANDA-QUANTITA-CONSERVATA`
diceva *«la decisione `10` e' un bilancio d'energia: senza una quantita' conservata su cui
scriverlo, QUELLA DECISIONE NON HA UN OGGETTO»*. ### ✅ **`E~` E' QUELL'OGGETTO**, se `(A)`
regge. ### ⚠ **Quindi `P4` non decide solo questo pezzo: decide anche se la decisione `10`
ha un oggetto** — e lo scrivo **prima** di misurare, perche' dopo sembrerebbe una lettura
comoda.

---

## 8. LA STELLA POLARE

| | la domanda | la risposta |
|--:|---|---|
| **1** | conserva **localmente**? | ### ⭐ **E' TUTTO IL PEZZO:** `Delta(E_k + pi_k) = (div J)_k`, **senza sorgente**, con la corrente di `0080cf3`. ### ⚠ **Ma la conservazione e' per COSTRUZIONE** *(par. `2.3`)*: cio' che si misura e' **l'effetto di ritorno** |
| **2** | **quale gradino**? | ### ⛔ **NESSUNO ANCORA: questa e' una DERIVAZIONE, senza codice.** Il gradino lo decidera' `P4` |
| **3** | **aggiunge un numero o una legge**? | ### ⚠ **UNA LEGGE** *(lo scambio col vuoto)*, e `9-ter` chiede di contarle: **da `3` a `4`**, e la giustificazione e' che ### **togliere un'eccezione non era possibile** — la non-conservazione non e' un'eccezione, e' **una mancanza**. ### ✅ **E `A-ii` la terrebbe a `3` variabili**, ed e' il motivo per cui la domanda `1` esiste. ### ⛔ **NESSUNA COSTANTE NUOVA** |
| **4** | tocca `rho`, `c_s` o **il SEGNO**? | ### ⭐ **`c_s` SI', ed e' il cuore:** `cs_k = f'(pi_k)`. ### ⚠ **E il SEGNO di `f'` e' il pericolo**: deve essere positivo **per costruzione**, non per clip |
| **5** | **emergente o imposto**? | ### ⭐ **L'EFFETTO DI RITORNO E' EMERGENTE** *(viene dall'equazione di Hamilton della coppia, non da un innesto)*. ### ⚠ **La coppia stessa e' IMPOSTA**, ed e' la decisione di Luca; ### **la FORMA di `f` e' aperta** |

---

## 9. TODO DEL NEXT STEP

1. registrare la **decisione** nell'indice, chiudere
   `[[DOMANDA-E-NON-SI-CONSERVA-A-X-UNO]]` come **decisa da Luca**, e segnare
   `[[D-ENERGIA]]` come **superata**.
2. registrare le **quattro domande** del par. `7`, con la raccomandazione **separata**.
3. la **correzione** del punto `2` del mandato: la `C` **completa** *(che trasforma anche
   `U`)*, e chiudere `[[DOMANDA-TRASPORTO-DEVE-STARE-IN-SU2]]`.
4. ### ⛔ **NIENTE CODICE DI `(A)` finche' le domande `1` e `3` non hanno una risposta:**
   senza la coppia e senza `f` ### **scriverei io la fisica.**
5. se il budget regge, `M1a` sulla **scena grande** *(il riscaldamento di Floquet)*.
