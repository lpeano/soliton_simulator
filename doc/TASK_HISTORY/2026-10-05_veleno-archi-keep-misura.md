# `VELENO-ARCHI-KEEP`, **passo (1): la misura che conferma la causa**

*Mandato di Luca, 2026-10-05. Il simulatore **`0f060670` non si tocca**.*
**Rientra nell'eccezione al congelamento**: e' un difetto d'**infrastruttura** che
**falserebbe la cura di `TETTO-CAUSALE` passo (2)**.
**Scritto e committato PRIMA di girare** *(par.8)*.

---

## LA STELLA POLARE — **le cinque risposte, PRIMA del lavoro** *(`L-STELLA`)*

*(Questo mandato non le chiede esplicitamente, e questa misura **non cambia la fisica**.
Le scrivo perche' `L-STELLA` copre anche **le due vie di cura** che il referto deve
riportare, e perche' una misura progettata male **afferma** fisica senza scriverla.)*

**① `A14` — conserva energia e carica LOCALMENTE?**
### **NON SI APPLICA, e il perche' e' piu' forte di <<e' una misura>>:** l'oggetto non e'
una legge di fisica, e' ### **una DERIVATA, cioe' una cache.** Una cache non conserva
niente: la sua unica proprieta' e' **essere allineata a cio' che descrive**.
### ⚠ **Ma c'e' un <<ma>> che va scritto ORA:** se una derivata disallineata viene **letta
da una legge**, allora quella legge sta usando **il valore di un altro arco** — e **quello**
e' un problema di `A14`, perche' un bilancio locale calcolato col valore del vicino **non e'
locale**. ### **Il punto `(c)` della misura esiste per sapere se succede OGGI.**

**② A quale dei TRE GRADINI arriva il risultato?**
### **Al gradino `(a)`, e qui in una forma piu' forte del solito:** il confronto e'
`vecchio[flatnonzero(keep)]` contro il reale, ### **un'uguaglianza AL BIT fra due array**,
non una statistica. **Uno scarto e' `0` o non lo e'.**
### ⛔ **NON arriva al `(b)`** *(non tolgo nessuna legge pratica)* ### **ne' al `(c)`**
*(non c'e' un limite noto con cui confrontare un disallineamento di indici)*.

**③ Aggiunge un numero o una legge? Di che tipo?**
### **ZERO numeri, e zero leggi: e' una misura, e la cura NON si scrive** *(decisione di
Luca: la forma la decide lui dopo il referto)*.
### 📌 **E LA DOMANDA MORDE LE DUE VIE che devo riportare, quindi la rispondo ORA, senza
scegliere:** la via `(i)` *(`keep` applicato a tutte le derivate d'arco prima del veleno)*
### **non aggiunge leggi: ne RIPARA una** — e per `9-ter` **toglie un'eccezione**, perche'
oggi le colonne d'arco si riallineano e le derivate d'arco no. La via `(ii)` *(chi legge
`dt_e` dopo la mitosi lo ricalcola da `r`)* ### **aggiunge una SECONDA SCRITTURA della
stessa legge** — ed e' precisamente cio' che il simulatore dichiara di non voler fare,
accanto a `_dt_e_ultimo`: *«una seconda scrittura della stessa legge e' due leggi che
possono divergere»*. ### **Lo scrivo come CONTO delle leggi, non come raccomandazione: la
scelta e' di Luca.**

**④ Tocca `rho`, `c_s` o il SEGNO? In quale verso dell'accoppiamento?**
### **NON tocca nessuno dei tre, e non ha un verso:** un disallineamento di indici non ha
un segno ne' una direzione. ### ⚠ **E la conseguenza va detta invece di saltare la
domanda:** l'errore **non e' sistematico in un verso** — ogni arco legge il valore di
**un arco qualunque**, quindi ### **non si media a zero e non si somma in una direzione: e'
RUMORE STRUTTURATO.** ### **Un errore cosi' e' peggiore di uno con un segno, perche' non
lascia una firma.**

**⑤ Emergente o imposto: sopravvive se si toglie la legge pratica?**
### **LA LEGGE PRATICA SOSPETTA E' IL VELENO STESSO** *(`COMMIT 4`)*, e la domanda si
ribalta in modo utile: ### **il veleno NON crea il difetto — lo NASCONDE.** Senza veleno,
una derivata d'arco restava **CORTA** dopo la nascita, e la lunghezza sbagliata era
### **un segnale che le guardie di lunghezza prendevano** *(il simulatore lo dichiara:
*«la sua legge l'ha riscritta, oppure non c'erano nati per lei»*)*.
### ⛔ **Col veleno la lunghezza e' GIUSTA e i valori sono SPOSTATI: il segnale e' sparito
e il difetto e' rimasto.** ### **E' la forma peggiore di un presidio: uno che rende un
difetto invisibile invece di impedirlo** — ed e' esattamente `A9` letto al rovescio.

---

## 1. RAGIONAMENTO PRELIMINARE — *cosa credo PRIMA di guardare*

### **IL CENSIMENTO DAL REGISTRO, FATTO DALL'AST** *(par.2: mai per riga)*

`REGISTRO_DERIVATE` *(assegnazione a `:1300`)*, **10 voci**:

| ambito | classe | quante | quali |
|---|---|--:|---|
| `nodo` | `avvelena` | **6** | `_chi_core_nodi`, `_chi_core_raggio`, `_chi_core_rho0`, `_fatt_cs_ultimo`, `_chi_geom_nodi`, `_r_corrente` |
| `nodo` | `auto-rinfresco` | **2** | `_g_rampa_prec`, `_xi_rumore` |
| ### `arco` | ### `avvelena` | ### **2** | ### **`_dt_e_ultimo`, `_sin2_vir`** |
| `arco` | `auto-rinfresco` | **0** | — |

### **IL NUMERO CHE VEDO E' `2`**, e coincide con quello del mandato. **Nessuna combinazione
ambito/classe fuori dalle quattro attese.**

### ⛔ **L'IPOTESI E' CONFERMATA DALLA LETTURA DEL CODICE** *(e resta da MISURARE)*

`_avvelena_derivate` *(`:1521`–`:1619`)* fa **una cosa sola** sulle derivate da avvelenare:

```
if len(v) >= bersaglio:  continue          # gia' lunga: non fa niente
quanti = bersaglio - len(v)
_nuovo = np.concatenate([v, np.full(quanti, np.nan)])
```

### **`keep` NON COMPARE MAI in quella funzione.** Appende `NaN` **in coda**, e basta.

E la chiamata e' a **`:1707`**, ### **DOPO** che tutte le regole hanno scritto — compresa
`_rn_div_i` *(`:1743`)*: `net.i = concat(net.i[keep], a, m)`.
### 📌 **E L'ORDINE E' DELIBERATO, lo dice il commento del codice:** *«PERCHE' DOPO E NON
PRIMA: il veleno estende fino a `len(net.phi)` e `len(net.i)`, cioe' alle lunghezze NUOVE —
e quelle le stabiliscono le regole di `phi` e di `i`»*.
### ⛔ **E' proprio questo a far mordere l'omissione di `keep`: il veleno arriva quando gli
archi sono GIA' stati riordinati, e tratta l'array vecchio come se non lo fossero.**

### ⛔ **E I DUE EVENTI DI NASCITA NON SI COMPORTANO ALLO STESSO MODO** *(letto dall'AST)*

| evento | la regola di `i` | toglie archi? |
|---|---|---|
| **`divisione`** *(`:1743`)* | `concat(net.i[keep], a, m)` | ### **SI** |
| **`schwinger`** *(`:2171`)* | `concat(net.i, aa, k)` | ### **NO**: solo coda |

> ### ✅ **QUINDI IL CASO CHE DISCRIMINA LA CAUSA VIENE GRATIS DALLA STESSA CORSA:** negli
> eventi **Schwinger** non si toglie **niente**, quindi ### **le differenze devono essere
> ZERO.** ### **Non serve una scena costruita: la traiettoria del driver contiene
> entrambi i tipi di evento.**

## 2. LE ATTESE, **dichiarate PRIMA** e col conto che le produce

Sia `s = len(sel)` il numero di archi che si dividono in un evento, `m` gli archi prima.

| | l'attesa | il conto |
|---|---|---|
| **①** | archi **tolti** `= s`, **aggiunti** `= 2s`, e `m_nuovo = m + s` | `keep` e' falso su `s` posizioni; `concat` aggiunge `a` e `m`, cioe' `2s` |
| **②** | il veleno appende **esattamente `s`** celle `NaN` | `quanti = bersaglio - len(v) = (m + s) - m = s` |
| ### **③** | ### **il veleno copre solo METÀ degli archi nuovi** | gli archi nuovi sono `2s`, le celle avvelenate `s`. ### **Gli altri `s` ricevono un valore FINITO preso da un arco vecchio** |
| **④** | la **prima posizione diversa** `= min(sel)` | fino al primo arco tolto gli indici coincidono; dal primo tolto in poi tutto scala di uno |
| **⑤** | gli elementi diversi sugli archi conservati `~ sum(keep) - min(sel)` | tutte le posizioni dal primo tolto in poi, salvo coincidenze di valore |
| ### **⑥** | ### negli eventi **Schwinger**: differenze `= 0` | non c'e' `keep`: `concat(net.i, aa, k)` |

### ⚠ **E L'ATTESA ③ E' LA PIU' IMPORTANTE, perche' e' quella che spiega il referto del
### tetto causale:** se il veleno coprisse **tutti** gli archi nuovi, un lettore troverebbe
`NaN` e si fermerebbe. ### **Coprendone METÀ, l'altra metà legge un valore FINITO E
SBAGLIATO — e un valore finito non fa scattare nessun controllo.**
### **E' questo che rende il difetto SILENZIOSO.**

### **I VALORI SOTTO IPOTESI NULLA, scritti ORA** *(presidio di `FATTI_dal_codice.md`)*

**Se l'ipotesi fosse SBAGLIATA** e il veleno riallineasse: **differenze `= 0` in OGNI
evento**, compresi quelli con archi tolti. ### **Quindi <<zero differenze>> non e' un
risultato neutro: SMENTIREBBE l'ipotesi**, e il mandato dice di fermarsi e **non proporre
la cura**.
**Se il confronto fosse mal costruito:** darebbe differenze **anche** negli eventi
Schwinger — ed e' il **caso che discrimina**.

### **COSA NON SO, e non voglio indovinare**

1. **Se `_sin2_vir` e `_dt_e_ultimo` esistano** al momento della prima nascita. Il veleno
   ha un ramo `if v is None: continue` *(contato in `_g_veleno_assenti`)*: ### **se una
   delle due non esiste ancora, per lei il difetto non c'e' ANCORA**, e va distinto da
   *«non c'e'»*.
2. **Quanti eventi Schwinger** ci sono in 150 passi. ### ⚠ **Se fossero ZERO, il caso che
   discrimina NON gira**, e lo direi invece di presentare il controllo come passato.
3. **Se i nodi siano davvero solo AGGIUNTI** *(punto `(d)`)*. La regola di `phi` e'
   `concat(phi, fm)`, che e' solo coda — ma ### **va verificato su TUTTE le colonne di
   nodo, non su una**, e anche a runtime.
4. **Se un lettore VIVO** legga queste due derivate **dopo** `mitosi` nello stesso passo
   *(punto `(c)`)*. ### **Dal referto del tetto causale so che `memoria_hebbiana_moto` e'
   la voce 5 e `mitosi` la 3** — ma `memoria_hebbiana_moto` **oggi NON legge** `dt_e`, e
   `_sin2_vir` la riscrive **intera**. ### **Quindi mi aspetto che il difetto sia LATENTE,
   non attivo — e se mi sbagliassi sarebbe la notizia piu' importante del referto.**

## 3. PROGETTAZIONE DEL RAGIONAMENTO — *i passi, e cosa decide ciascuno*

| | il passo | che cosa DECIDE | che cosa mi FERMA |
|---|---|---|---|
| **1** | scena del **driver**, `nmasse`/`sep` **dall'argv**, seme `11`, **150 passi** | la scena del mandato | `nmasse`/`sep` a mano: e' `H-P3` |
| **2** | patch su una **COPIA**, come per il tetto | il simulatore **non si tocca** | ancora non unica *(`P1-quater`)* |
| **3** | si registra **A OGNI EVENTO** *(non per passo)*, **prima e dopo** `nascita` | granularita' | — |
| **4** | ### `keep` si prende **DAL CONTESTO `c['keep']`**, non si ricostruisce | esattezza | ### **ricostruirlo a mano sarebbe una seconda scrittura della stessa legge** |
| **5** | atteso `= vecchio[np.flatnonzero(keep)]` contro il reale nelle prime `sum(keep)` posizioni | **il difetto** | — |
| **6** | i **lettori** delle due derivate, dall'AST, con la **voce** in cui stanno | se il difetto e' **attivo oggi** | — |
| **7** | le colonne di **nodo**: solo aggiunte? | se il veleno dei nodi e' **corretto** | — |
| **8** | ### **il caso che discrimina**: eventi senza archi tolti | ### **la CAUSA** | ### ⛔ **differenze senza archi tolti: l'ipotesi e' SBAGLIATA, FERMO** |
| **9** | **il controllo positivo**: `concat(vecchio[keep], NaN)` contro l'atteso | il **confronto** | ### ⛔ **se non da' zero, il confronto e' sbagliato: FERMO** |

### **E UN BATTITO PER PASSO, che il mandato chiede e che e' un debito che ho annotato io**

Lo strumento del tetto causale **non stampava niente per passo**, e la richiesta di stato di
Luca ha dovuto **stimare** il passo *(`100`–`115` su `150`)* invece di leggerlo.
### ✅ **Questo strumento stampa un battito per passo, a uscita non bufferizzata.**

## 4. I CRITERI DEL SIGILLO, per i commit successivi

*(La cura **non si scrive** — li fisso ora perche' il mandato chiede che i criteri stiano
nel task history **prima**, non dopo.)*

| | il criterio |
|---|---|
| **braccio `0`** | la patch sul *prima* riproduce il blob di oggi: `0f060670` |
| ### **il caso che DEVE fallire** | ### una copia **senza** `keep` applicato alle derivate: il sigillo **DEVE BOCCIARLA** |
| **l'identita'** | sugli eventi **senza archi tolti** *(Schwinger)*, la cura e' **identica al byte** |
| **la copertura** | dopo la cura, le celle `NaN` sugli archi nuovi sono **`2s`** e non `s` |
| ### **dove stanno le differenze** | ### **solo** nelle due derivate d'arco e **a valle**: se comparissero a monte, la cura ha toccato altro |

### ⚠ **E UN CRITERIO CHE NON POSSO FISSARE, e lo dico:** *«byte-identico sullo stato»*
**non vale** per questa cura. Il `COMMIT 4` lo ha gia' dichiarato per se stesso — *«il passo
della nascita NON e' byte-identico sulle DERIVATE»* — e ### **una cura che riallinea le
derivate le cambia PER DEFINIZIONE.** Il criterio giusto e' **lo stato**, non le derivate.

## 5. TODO DEL NEXT STEP

1. lo **strumento** in `csv/_test_fork/`, con `_presidio.avvia`, la patch su una **copia**,
   il **battito per passo** e il **collaudo** *(coi due controlli su dati sintetici)*;
2. la **voce `VELENO-ARCHI-KEEP`** in `doc/INDICE_ID.tsv` *(aperto, difetto)*, col rimando a
   `VELENO-ORIENTATO` e a `TETTO-CAUSALE-TEMPO-COORDINATO`;
3. la voce d'**inventario** nello stesso commit dello strumento *(par.6 ①)*;
4. **commit PRIMA di girare** *(par.5)*;
5. il **run**, staccato e non bufferizzato, **150 passi**;
6. il **referto**, coi **blob citati**, e in **testa** la risposta al punto `(c)`: ### **se
   un lettore vivo legge queste derivate dopo la nascita nello stesso passo, il difetto e'
   GIA' ATTIVO oggi**;
7. ### **NIENTE CURA.** Le due vie si **riportano**, senza sceglierne una.
