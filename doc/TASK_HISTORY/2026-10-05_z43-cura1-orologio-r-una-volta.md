# `Z43` PARTE A — **CURA (1): `r` VA UNA VOLTA SOLA, NELLA FREQUENZA NO**

*(mandato di Luca del 2026-10-05, `Z43` / LE DUE CURE DEL TEMPO PROPRIO. **Scritto PRIMA
del codice**, e committato prima: cosi' l'ordine e' **verificabile da git** — par.8.)*

> ### ⛔ **E LA `PARTE B` PARTE SOLO SE IL SIGILLO DI QUESTA PASSA: altrimenti `FERMO`.**
> *(Parola del mandato, non mia.)*

## LA DECISIONE DI LUCA, registrata e NON reinterpretata

> **(1)** *«L'orologio di Compton conta `r` DUE volte: `omega_clk = coerenza * r_node *
> (cs/CS_M)^2` (`:5926`, `:5970`) e poi la fase avanza di `omega_clk * dt_n`, con
> `dt_n = DT*r` (`:5971`). ### **Un orologio avanza di frequenza PROPRIA per tempo
> PROPRIO: `r` va UNA volta sola, in `dt_n`. SI TOGLIE `r_node` dalla frequenza.»***

**IL MOTIVO, ed e' MISURATO:** il `BRACCIO A` del referto `66a798d` ha tolto **proprio
quel fattore**, e l'altalena e' **crollata** — `abs(f)` da `5.283` a **`1.034`**, `C0` da
`7.185` a **`1.031`**.

### 📌 **E LE RIGHE DEL MANDATO SONO DI UN BLOB PRECEDENTE, come sempre:** `:5926` e
`:5970` erano di `e2940b3c`; su `1feb9b0a` *(la cura di `MEM_FASE`, `7a03063`)* sono
### **`:5961` e `:6005`**, e `_phc` e' a ### **`:6006`**. ### **Verificate dall'AST, non
dedotte da un delta.**

## ⛔ IL CENSIMENTO — **e il mandato diceva di FERMARMI se trovavo altri siti**

> *«Censisci dall'AST TUTTI i siti in cui `r` (o `r_node`, `dt_n/DT`) moltiplica una
> FREQUENZA che viene poi moltiplicata per `dt_n` ... Se trovi siti oltre a questi due,
> FERMATI e riporta: non estendere la cura da solo.»*

### ✅ **I SITI SONO ESATTAMENTE DUE. NON MI FERMO.**

| | riga | che cos'e' | gira oggi? |
|---|--:|---|---|
| **1** | `:5961` | `omega_clk = (_num / max(_den, 1e-12)) * r_node` — il ramo **`DEPARAM_OROLOGIO`** | ### ✅ **SI'** |
| **2** | `:5966` | `omega_clk = (rho / max(rho_c, 1e-12)) * r_node` — il ramo **legacy** | ### ⛔ **NO** *(`DEPARAM_OROLOGIO = True`)* |

**COME L'HO CERCATO:** dall'AST, **ogni `BinOp` di moltiplicazione** che contenga il nome
`r_node` fra i suoi `Name`. ### **Due, e nessun altro.** Piu' le **tre** assegnazioni a
`omega_clk` *(`:5961`, `:5966`, `:6005`)* e **ogni** moltiplicazione per `_dts`/`dtn`.

### ⚠ **E UN TERZO CANDIDATO C'ERA, e l'ho ESCLUSO guardandolo invece di assumerlo**

`:6038` — `_thk = norm(_Om) * _dts` — ### **moltiplica per `_dts`**, quindi era un
sospetto. ### **Ma `_Om` viene da `forza_sync * _amp * (_crx/_sink)`** *(`:6037`)*, e
### **NON contiene `r_node`**: e' il **torque di Kuramoto** di `SYNC_FASE_OROLOGIO`, che e'
`False`. ### **Non e' un terzo sito.**
### **Lo scrivo perche' un candidato escluso senza dirlo e' un candidato non cercato.**

### 📌 **E IL DOPPIO CONTEGGIO C'E' IN ENTRAMBI I RAMI, per vie DIVERSE**

| | la catena |
|---|---|
| ramo **`DEPARAM`** *(gira)* | `omega_clk = coerenza * r_node` -> `_phc = exp(-0.5j*_sk*omega_clk*_dts)` *(`:6006`)*, e `_dts = dtn = DT*r` -> ### **`r^2`** |
| ramo **legacy** *(non gira)* | `omega_clk = rho/rho_c * r_node` -> `omega_tot += omega_clk*nb` *(`:5967`)* -> `theta = norm(omega_tot)*_dts` *(`:5976`)* -> ### **`r^2`** |

### ✅ **E NEL RAMO CHE GIRA `theta` NON HA IL DOPPIO CONTEGGIO:** li' `omega_tot` e'
`omega_new (+ omega_sync)`, che ### **non contiene `r_node`** — l'orologio e' applicato
**come fase globale**, non come rotazione. ### **Quindi la cura tocca `_phc` nel ramo che
gira e `theta` nel legacy, e sono LO STESSO ERRORE in due forme.**

### ⛔ **IL RAMO LEGACY SI CURA, e il mandato lo dice:** *«Applica la stessa correzione al
ramo legacy (e' la stessa legge), dichiarandolo.»*
### ⚠ **E VA DICHIARATO CHE NESSUN SIGILLO PUO' MISURARLO GIRANDO:** `DEPARAM_OROLOGIO` e'
`True`, quindi quel ramo ### **non viene eseguito.** ### **La sua cura e' verificabile solo
dall'AST e dalla lettura — non da un numero.** ### **Lo scrivo ORA, perche' detto dopo
sembrerebbe una scusa.**

## LA VOCE NUOVA: **`CS-LAMBDA-GLOBALE`** — verificata dall'AST, **e da NON curare ora**

> **Decisione di Luca:** *si registra, ### **si cura DOPO.***

### ✅ **IL FATTO DEL GUARDIANO TORNA, e l'AST lo dice con un numero: UNA sola riduzione
### globale in `_cs_nodo`**

`_cs_nodo` *(`:7107-7160`)* contiene **esattamente una** riduzione su tutta la rete:

```
:7151   _Lam = float(np.mean(_I))        # _I = max(I[:n], 0.0)  ->  MEDIA SU TUTTI I NODI
```

| | |
|---|---|
| la **transizione** | `u_nodo = I / media dei VICINI` *(`W_loc @ I / W_loc @ 1`)* — ### ✅ **LOCALE** |
| il **pavimento** | `_scala = max(_Lam, 1e-30)/GAMMA_TURBO^2`; `cs_floor = CS_M/(1 + sqrt(_I)*sqrt(1/_scala))` — ### ⛔ **porta `_Lam`, che e' GLOBALE** |

### ⛔ **QUINDI `cs` PORTA UN RIFERIMENTO GLOBALE, e con la decisione (2) lo porterebbe
### ANCHE `r`.** E lo stesso termine tocca **gia' oggi** il **tetto causale**, il
**tempo-luce** e l'**orologio**.

### 📌 **LA STORIA, e il mandato chiede di citarla: e' uno SCHEMA RICORRENTE, non un
### incidente**

`48d5ce2`, del **2026-09-16** — *«`cs_floor` RELAZIONALE cablato come CORREZIONE DI
DIFETTO (categoria D, NESSUN FLAG). Sigillo 16/16 PASS, R1 byte-identico»* — tolse la
**densita' critica ASSOLUTA** *(`GAMMA = 0.05`, cioe' `400`)* e la sostitui' con **`Lam`,
l'energia del vuoto che il sistema CALCOLA da se'**.

> ### ⛔ **TOLSE UN NUMERO A MANO E INTRODUSSE UN RIFERIMENTO GLOBALE.**
> ### **E' LO STESSO SCAMBIO fatto per il gauge di `r`** *(la mediana globale di `|f|`)*.
> ### **Due volte la stessa mossa, e nessuna delle due era sbagliata da sola: entrambe
> ### togliavano una COSTANTE ARBITRARIA, che e' il difetto peggiore.**
> ### 📌 **Ma il prezzo e' lo stesso ogni volta, e ora si vede: una legge LOCALE che legge
> ### una MEDIA GLOBALE non e' piu' locale.**

**LA CURA NATURALE**, e il mandato la nomina: ### **un vuoto LOCALE per nodo** — la
proposta di Luca del **2026-10-02** *(`VUOTO-LOCALE-DETERMINISTICO`)*, che
### ⚠ **richiede prima un'energia definita** *(`ENERGIA-NON-DEFINITA`)*.
**Collegata a:** `INVARIANZA-LOCALE-CS`, `Z43`, `VUOTO-LOCALE-DETERMINISTICO`.

## LA STELLA POLARE — **le cinque risposte, PRIMA del codice** *(`L-STELLA`)*

### **1. `A14`: conserva energia e carica LOCALMENTE?**

### **LA CARICA: non si applica** — la cura tocca una **frequenza d'orologio**, non
`perc_chi`.
### ⚠ **L'ENERGIA: non e' rispondibile**, ed e' un fatto del repo
*(`ENERGIA-NON-DEFINITA`)*. Non dico <<conserva>>.

> ### 📌 **MA UNA COSA LA CURA LA GUADAGNA, ED E' DIMENSIONALE:** oggi la fase avanza di
> `coerenza * (cs/CS_M)^2 * DT * r^2`, cioe' ### **`r` al quadrato in una grandezza che
> deve essere <<frequenza x tempo>>.** ### **Una frequenza PROPRIA non contiene il ritmo
> del proprio tempo: contenerlo e' contare lo stesso fattore due volte.**
> ### **Questa non e' una preferenza estetica: e' un'ANALISI DIMENSIONALE**, ed e' il
> motivo scritto nella decisione di Luca.

### **2. A quale dei TRE GRADINI arriva il risultato?**

| gradino | risposta |
|---|---|
| **(a)** robusto al rumore numerico | ### ✅ **SI', e nella forma piu' forte:** il criterio 1 pretende ### **identita' AL BYTE ai passi 1 e 2**, dove `r = 1` **esatto per costruzione** |
| **(b)** regge togliendo la legge pratica | ### ⚠ **LA LEGGE PRATICA QUI E' IL TETTO DI `r`** *(`1.414212977`)*, e il referto `66a798d` l'ha misurato: morde in **mediana** sullo `0.000078` ma ### **fino al `0.384` in qualche passo.** ### **Quindi nei passi dell'altalena cio' che si osserva e' il tetto** — e la cura **toglie l'altalena**, quindi ### **dovrebbe TOGLIERE anche quella saturazione.** Il sigillo lo misura |
| **(c)** coincide con un limite noto | ### ✅ **SI', e il `BRACCIO A` di `66a798d` E' quel limite:** aveva tolto lo **stesso** fattore su una **copia**, e aveva dato `1.034`. ### **Il criterio dell'altalena pretende `<= 1.2`, cioe' COERENZA con una misura gia' fatta** |

### **3. Aggiunge un numero o una legge?**

### **NESSUN NUMERO: ZERO.** E ### **NESSUNA LEGGE: ne TOGLIE un fattore.**

**IL CONTO** *(`9-ter`)*: le leggi restano **le stesse**; una di loro ### **perde un
fattore moltiplicativo.** ### ✅ **E PER `9-ter` QUESTO E' IL CASO MIGLIORE: non e' una
cura che aggiunge, e' una che TOGLIE** — e toglie ### **un'eccezione alla regola
<<frequenza propria x tempo proprio>>**, che il resto del simulatore rispetta.

### **4. Tocca `rho`, `c_s` o il SEGNO?**

### ⛔ **IL SEGNO: NO, e va detto perche' e' facile sbagliarsi.** Il fattore tolto e'
`r_node`, che e' ### **`dtn/DT`, cioe' NON NEGATIVO** *(`r` sta in `[1.414e-06,
1.414212977]`)*. ### **Togliere un fattore positivo NON cambia il segno di `omega_clk`.**

### ⚠ **`rho` e `c_s`: INDIRETTAMENTE.** La fase dello spinore cambia -> `psi_spin` cambia
-> `|psi|^2` e `rho_spin` cambiano -> `cs` cambia, ### **dal passo dopo.** ### **E' la
ragione per cui il criterio dice <<dal passo 3 lo stato DEVE divergere>>.**

### **5. Emergente o imposto: il fenomeno sopravvive se si toglie la legge pratica?**

> ### ⛔ **IL <<FENOMENO>> QUI E' L'ALTALENA, e la risposta e' GIA' MISURATA:** il
> `BRACCIO A` di `66a798d` ha mostrato che ### **togliendo questo fattore l'altalena
> SPARISCE** *(`5.283` -> `1.034`)*.
> ### **Quindi l'altalena era IMPOSTA dal doppio conteggio, non emergente.**

### ⚠ **E LA PARTE ONESTA:** il `BRACCIO A` era una **copia** e toglieva il fattore
**solo** nel ramo `DEPARAM`. ### **Questa cura lo toglie anche nel legacy**, e
### **cambia il blob del simulatore vero.** ### **Il sigillo deve ri-misurare l'altalena
sul simulatore VERO, e il mandato lo pretende** — *«L'ALTALENA SPARISCE nel simulatore
vero»*.

## I SEI CRITERI DEL SIGILLO — **fissati e committati PRIMA del codice**

| | che cosa pretende | e se fallisce |
|---|---|---|
| **`0`** | **braccio 0**: *prima* + la patch committata = **il blob nuovo** | ### **FERMO** |
| **`1`** | ### **IDENTITA' AL BYTE nei passi 1 e 2** *(lockstep su TUTTI gli attributi di `net`, scena del driver, seme 11)*: li' `r = 1` **esatto per costruzione**, quindi togliere `r_node` ### **non cambia niente** | ### ⛔ **la patch tocca altro: FERMO** |
| **`2`** | ### **CASO CHE DEVE FALLIRE: dal passo 3 lo stato DEVE divergere** | ### ⛔ **la cura non agisce: FERMO** |
| **`3`** | **`STEP2` intatto**: `omega_clk / coerenza = (cs_prec/CS_M)^2` ### **al bit**, su ogni nodo e ogni passo | ### **FERMO** |
| **`4`** | ### **L'ALTALENA SPARISCE nel simulatore vero**, `150` passi: rapporto dispari/pari della mediana di `abs(f)` **e** di `C0` ### **`<= 1.2`** *(il braccio A aveva dato `1.03`)*. Si misura con lo **strumento di `Z43`** *(`7b71aa48`)*, rigirato sul blob nuovo | ### **FERMO** |
| **`5`** | la corsa arriva a **`150` passi** ### **senza `FERMO` di invarianti**; e si riporta che cosa cambia **a valle** *(`n`, archi, divisioni, Schwinger)*, ### **senza giudicarlo** | ### **FERMO** |

### ⛔ **IL CRITERIO `1` E IL CRITERIO `2` SONO LE DUE META' DELLO STESSO CONTROLLO**, e lo
scrivo ora perche' e' facile perderne una: ### **ai passi 1-2 l'identita' DEVE tenere** *(li'
`r = 1`, quindi la cura e' un no-op aritmetico)*; ### **dal passo 3 la divergenza DEVE
arrivare** *(li' `r != 1`, quindi il fattore tolto conta)*.
### **Se l'identita' non tiene, la patch tocca altro. Se la divergenza non arriva, la cura
non agisce.**

### ⚠ **E IL CRITERIO `3` HA UNA FINEZZA:** `omega_clk / coerenza` ha senso **solo nel ramo
`DEPARAM`** *(nel legacy `omega_clk = rho/rho_c * r_node`, e il divisore sarebbe
`rho/rho_c`)*. ### **Il sigillo lo misura dove il ramo gira, e dichiara che il legacy non
e' misurabile girando.**

## L'ORDINE DEI COMMIT

1. ### **questo task history** + la **voce nuova `CS-LAMBDA-GLOBALE`** + le **tre decisioni**
   registrate in `Z43` e in `COMPONENTI:A1`/`COMPONENTI:B9` — pushati **PRIMA** *(par.8)*;
2. **il codice e lo strumento del sigillo**, col `REGISTRO_FISICA` e l'**inventario**;
3. **la corsa e il referto**, ### **coi blob citati.**

## TODO DEL NEXT STEP — **operativo**

1. **commit di questo task history**, della voce nuova e delle tre decisioni;
2. la **cura**: togliere `r_node` da `:5961` **e** da `:5966`, ### **e nient'altro**;
3. la **patch del braccio 0**, ### **estratta dal sorgente curato**;
4. lo **strumento del sigillo** coi **sei criteri**;
5. la **corsa**, piu' lo **strumento di `Z43`** *(`7b71aa48`)* rigirato sul blob nuovo per
   il criterio `4`;
6. il **referto**, con **che cosa cambia a valle** *(`n`, archi, divisioni, Schwinger)*
   ### **riportato e non giudicato**;
7. **relazione** e **voci d'indice** nello stesso giro *(par.4)*.

### ⛔ **CIO' CHE NON SI FA:** ### **la decisione (2)** *(`r = cs/CS_M`)*, che e' la
`PARTE B` e parte ### **solo se questo sigillo passa**; ### **l'unificazione delle
densita'** *(la decisione (3) la rinvia esplicitamente)*; e ### **la cura di
`CS-LAMBDA-GLOBALE`**, che si registra e ### **si cura dopo.**
