# REFERTO -- IL SIGILLO DELLA CURA DI `VELENO-ARCHI-KEEP`

*(mandato di Luca del 2026-10-05, **passo (2): la cura, via (i)**; i criteri furono
fissati **prima del codice** in `b17caec`, e sono **otto**)*

> ### **TUTTI GLI OTTO CRITERI PASSANO, e il numero che riassume il sigillo e'
> ### `0`: le divergenze di STATO su 150 passi.**

| | |
|---|---|
| simulatore | `0f060670` **->** `e2940b3c` |
| la patch del braccio 0 | `14066458` |
| il sigillo | `ee1df224` |
| strumento del passo (1), **rigirato** | `425b8d47` |
| strumento del tetto causale, **rigirato** | `19d08753` |

## IL BRACCIO 0: il *prima* non si asserisce, SI RICOSTRUISCE

La patch applicata al blob di **prima** deve ridare il blob di **oggi**, al byte.

| | |
|---|---|
| commit che ha cambiato il simulatore | `92ecb04` |
| suo **PADRE** *(`H-P8`)* | `b17caec` |
| blob estratto dal padre | `0f060670` |
| blob che **la patch dichiara** | `0f060670` |
| **il *prima* e' quello atteso** | ### **`True`** |
| blob patchato | `e2940b3c` |
| blob sul disco oggi | `e2940b3c` |
| **coincide** | ### **`True`** |

### ⚠ **E QUESTO BRACCIO SI E' RIFIUTATO DI PROSEGUIRE, una volta, e aveva
### ragione.** Al primo giro prendeva il *prima* da `HEAD~1`; ma dopo il commit della
cura ne era arrivato un altro, quindi `HEAD~1` era diventato **il commit della cura** e
il *prima* estratto era ### **GIA' CURATO**. Il riferimento giusto e' **il padre del
commit che ha cambiato il simulatore**, che **non slitta**; e il *prima* ora si verifica
**contro quello che la patch dichiara**, non contro un numero scritto nel sigillo
*(sarebbero due leggi, `9-ter`)*. *(`c7f2eb3`.)*

## CRITERIO 1 -- **STATO IDENTICO AL BYTE** su tutti i passi

Lockstep di due reti, **braccio vecchio** *(`0f060670`)* e **braccio nuovo**
*(`e2940b3c`)*, confrontate su **`vars(net)` INTERO** -- non su un elenco scelto da
me -- a **ogni** passo.

| | |
|---|--:|
| passi confrontati | **`150`** |
| attributi confrontati per passo | **`290`** |
| ### **divergenze di STATO** | ### **`0`** |
| differenze di **derivata ammessa** | `83` |
| differenze di **contatore o registro** | `600` |

### 📌 **E LA DISTINZIONE FRA LE TRE CLASSI E' IL CUORE DEL REFERTO,** perche'
il criterio dice *<<stato identico al byte, le sole eccezioni ammesse sono
`_dt_e_ultimo` e `_sin2_vir`>>*: ### **le differenze che restano non sono di STATO.**

### (1) STATO -- `0`

> ### **ZERO. Su 150 passi, su 290 attributi per passo.**

### **E QUESTO E' IL NUMERO CHE SIGILLA LA CURA:** la conclusione del passo (1) era che
**nessun lettore vivo legge queste derivate dopo la nascita**, e quindi che riallinearle
### **non puo' cambiare la traiettoria**. Se lo stato fosse stato diverso in un punto
qualunque, quella conclusione sarebbe stata **smentita** e il mandato prescriveva di
**fermarsi**. Non e' successo.

### (2) DERIVATA AMMESSA -- `83`, e ### su UN SOLO nome

| derivata | passi in cui differisce |
|---|--:|
| `_dt_e_ultimo` | **`83`** |
| `_sin2_vir` | ### **`0`** -- **mai** |

Le due derivate **ammesse** dal criterio sono `_dt_e_ultimo` e `_sin2_vir`, e
### **l'eccezione si consuma su una sola**: `83` passi, che sono
### **esattamente gli 83 eventi di divisione** -- cioe' **solo** dove `keep`
esiste, come il criterio pretende.

### ⚠ **`_sin2_vir` che non differisce MAI non vuol dire che la cura non la tocca:**
la tocca *(i contatori la contano)*, ma i suoi valori riallineati **coincidono** con
quelli che leggeva prima. ### **E' il caso in cui il difetto era presente e INNOCUO**, e
va detto cosi': **non** *<<`_sin2_vir` stava bene>>*.

### (3) CONTATORE O REGISTRO DEL VELENO -- `600`, su 6 nomi

> ### **Un contatore che cambia NON e' uno stato che cambia: e' la cura che DICHIARA di
> ### aver agito.** Se questi fossero zero, la cura **non avrebbe fatto niente.**

| nome | passi | che cos'e' |
|---|--:|---|
| `_g_keep_riallineate` | **`109`** | le derivate d'arco riallineate: **lo contava la cura, PREVISTO** |
| `_g_keep_celle_tolte` | **`109`** | le celle **tolte** da `keep`: **PREVISTO** |
| `_g_keep_senza` | **`81`** | gli eventi **senza** `keep` *(lo Schwinger)*, dove la cura esce subito: **PREVISTO** |
| `_g_veleno_celle` | **`109`** | le celle avvelenate: **PREVISTO**, e passa da `s` a `2s` |
| `_veleno_registro` | **`83`** | il registro del veleno, che ora segna **`2s`** celle: **PREVISTO** |
| ### `_g_inv_veleno_ok` | ### **`109`** | ### ⛔ **NON PREVISTO DA ME** -- vedi sotto |

### ⛔ **`_g_inv_veleno_ok` NON ERA FRA LE TRE CONSEGUENZE CHE AVEVO DICHIARATO** in
`b17caec`, e lo dico perche' una previsione mancata e' un dato, non un dettaglio.

**CHE COS'E', letto dal codice** *(`:6647`)*: conta le celle che sono
### **avvelenate E `nan`**, cioe' quelle che il controllo d'invariante **ESENTA** dal
dominio. ### **Cresce perche' le celle avvelenate sono passate da `s` a `2s`.**

> ### 📌 **E IL SUO SIGNIFICATO E' LA COSA MIGLIORE CHE QUESTO SIGILLO DICE.**
> Il commento a `:6612` racconta che, **prima** che il veleno esistesse, il controllo
> d'invariante *<<verificava il dominio di derivate che portavano VALORI VECCHI, e che
> passavano PERCHE' ERANO POSITIVI PER CASO>>*.
> ### **Bene: fino a ieri META' DEGLI ARCHI NUOVI DI OGNI DIVISIONE era ancora in quel
> ### caso** -- valori finiti copiati da altri archi, verificati **come se validi**.
> ### **Ora il veleno li copre tutti, e l'invariante li esenta tutti: il presidio e'
> ### diventato ONESTO sul doppio delle celle.**

### ⚠ **E I DUE RIPIEGHI DELLA CURA SONO ENTRAMBI A ZERO, e per `A11` si dice**

La cura ha due rami di ripiego: `_g_keep_salti` *(una derivata d'arco che non sia
`float` a una dimensione)* e `_g_keep_assenti` *(una derivata del registro che non
esiste sulla rete)*. ### **Nessuno dei due compare fra gli attributi diversi, quindi
nessuno dei due e' mai stato creato: `0` su 150 passi.**

### **Lo dichiaro perche' un ramo che non gira mai e' `A11`:** se protegge da un
**errore**, l'errore va cercato. ### **Qui proteggono da una FORMA che il
`REGISTRO_DERIVATE` non garantisce** -- il registro dichiara `dove` e `classe`, non
`dtype` ne' `ndim` -- quindi restano; ### **ma il numero e' zero, e va saputo.**

### ⚠ **E UNA COSA CHE IL SIGILLO HA DOVUTO IMPARARE, invece di esentarsela**

`_veleno_registro` e' un **dizionario che contiene array**, e il comparatore lo
classifica **non confrontabile** `83` volte. ### **Non l'ho esentato: il
sigillo lo CONTA fra le differenze**, perche' *<<un attributo non confrontabile non e'
un attributo uguale>>*. Resta **in coda** come difetto dello strumento, dichiarato.

### ⛔ **E QUESTA E' UNA DOMANDA PER LUCA, non una decisione mia**

> Il criterio 2 dice: *<<le sole eccezioni ammesse sono `_dt_e_ultimo` e `_sin2_vir`>>*.
> ### **Quelle due sono DERIVATE. I 6 nomi di cui sopra sono CONTATORI e un
> ### REGISTRO, e il criterio non li nomina ne' per ammetterli ne' per escluderli.**
> Io li ho classificati `contatore/registro` e **non** `STATO`, perche' nessuno di loro
> entra in una legge: sono **la contabilita' della cura**. ### **Ma la classificazione
> l'ho scritta io, e quindi va approvata o corretta da Luca** -- se li si volesse
> contare come stato, il criterio 1 darebbe `600` e non `0`.
> ### **IL NUMERO NON CAMBIA: cambia che cosa si chiama STATO.**

### ✅ **LA RISPOSTA: APPROVATA.** *(Decisione di Luca del 2026-10-05 sul sigillo
`c4e9fd5`.)*

> ### **La classificazione <<contatore/registro, NON stato>> dei sei nomi e'
> ### APPROVATA**, e i sei sono: `_g_inv_veleno_ok`, `_g_keep_celle_tolte`,
> `_g_keep_riallineate`, `_g_keep_senza`, `_g_veleno_celle`, `_veleno_registro`.

**IL MOTIVO, come Luca lo ha dato — e non e' <<mi fido>>, sono due fatti:**

1. ### **ogni ALTRO attributo resta identico al byte**, quindi ### **nessuno dei sei
   rientra in una legge**: se uno di loro entrasse in una legge, quella legge
   produrrebbe un valore diverso **da qualche parte**, e quel qualche parte
   ### **sarebbe uno degli attributi che invece non si muovono.**
2. ### **`_veleno_registro` e' letto SOLO da `verifica_invarianti`**, che e' un
   ### **PRESIDIO** — non una legge. *(Ed e' coerente col fatto misurato dal
   sigillo: `_g_inv_veleno_ok`, l'unico dei sei che non avevo previsto, e' il
   contatore di quel presidio.)*

### ✅ **E IL GUARDIANO LO HA VERIFICATO CON UN LOCKSTEP INDIPENDENTE SU LINUX**
*(150 passi, tutti gli attributi di `net`)*.

> ### 📌 **E QUESTO E' PIU' DI UN'APPROVAZIONE: e' una SECONDA MISURA, su un'ALTRA
> ### PIATTAFORMA, con uno strumento che non e' il mio.**
> Il sigillo di questo referto e' girato su **Windows 11 / `python 3.13.2` /
> `numpy 2.3.0`**, e la piattaforma e' **timbrata** nel json *(e' la cura di
> `PIATTAFORMA-NON-TIMBRATA`)*. ### **Un risultato confermato su DUE piattaforme da
> DUE strumenti diversi non e' il risultato di uno strumento: e' il risultato del
> SISTEMA.**

### ⚠ **E LA DOMANDA RESTA SCRITTA QUI SOPRA, non l'ho cancellata:** una domanda
cancellata dopo la risposta ### **fa sparire il fatto che ANDAVA CHIESTA**, e il
criterio del mandato non nominava quei sei nomi — ### **la classificazione l'avevo
scritta io, e questo resta vero anche ora che e' approvata.**

## CRITERI 3, 4, 5 -- lo strumento del passo (1) `425b8d47`, RIGIRATO

| | sul VECCHIO `0f060670` | sul CURATO `e2940b3c` |
|---|--:|--:|
| confronti di **divisione** | `166` | `166` |
| ### con **DIFFERENZE** | ### **`166`** | ### **`0`** |
| elementi diversi **in totale** | `63 802 623` | ### **`0`** |
| 1a posizione diversa = primo arco tolto | `166` | `0` *(non ci sono differenze)* |
| archi confrontati | `138 784 360` | `138 784 360` |
| confronti **Schwinger** | `128` | `128` |
| ### con **DIFFERENZE** | **`0`** | **`0`** |
| controllo **positivo** in errore | `0` | `0` |

### **CRITERIO 4** *(controllo positivo: lo strumento sul blob nuovo da' `0` differenze
sui 166 confronti che oggi ne danno)*
### **PASSA**, e il numero piu' eloquente e' `63 802 623` **-> `0`**: ### **non <<meno>>, ZERO.**

### **CRITERIO 3** *(negli eventi Schwinger, dove `keep` e' assente, anche le due
derivate sono identiche al byte)* ### **PASSA**: `0` su `128`.
### ⚠ **Ed era `0` anche PRIMA della cura** -- e' proprio questo che ne fa **il caso
che discrimina la causa**: lo Schwinger non usa `keep`, non aveva il difetto, e la cura
### **non lo ha toccato.** Se qui fosse comparsa una differenza, la cura avrebbe
cambiato qualcosa **dove non c'era niente da cambiare.**

### **CRITERIO 5** *(dopo la cura le celle `NaN` sugli archi nuovi di una divisione sono
`2s` e non `s`)* ### **PASSA nella forma esatta in cui il mandato lo scrive**

| | sul VECCHIO | sul CURATO |
|---|--:|--:|
| confronti di divisione | `166` | `166` |
| copertura del veleno, **minimo** | `0.5000` | ### **`1.0000`** |
| copertura del veleno, **massimo** | `0.5000` | ### **`1.0000`** |
| celle **non finite** in coda, valori distinti | `1, 2, 3, 4, 5, 6, ...` | `2, 4, 6, 8, 10, 12, ...` |
| **archi nuovi**, valori distinti | `2, 4, 6, 8, 10, 12, ...` | `2, 4, 6, 8, 10, 12, ...` |
| ### celle non finite **=** archi nuovi, in OGNI evento | **`False`** | ### **`True`** |

> ### **`min = max = 1.0000` su 166 confronti: non una media, OGNI
> ### evento.** E i valori distinti delle celle non finite passano da
> **`1...32`** a **`2...64`**, ### **cioe' da `s` a `2s`**, e coincidono con gli archi nuovi
> ### **in tutti e 166**.

### ⚠ **UN DIFETTO DELLO STRUMENTO, che NON falsa questo risultato e che dichiaro**
Il campo `celle_nan_appese` dello strumento resta `1...32` anche sul blob curato, perche' e' calcolato come
`len_dopo - len_prima` -- e `len_prima` e' la lunghezza **prima delle regole**. Quella
quantita' coincideva con *<<quante celle appende il veleno>>* ### **solo finche' la cura
non esisteva.** La misura buona e' `non_finite_in_coda`, che e' ### **letta
dall'array**, non dedotta dalle lunghezze -- ed e' quella che da' `2s`.
### **E' un nome scaduto, non un numero sbagliato:** va **in coda**.

## CRITERIO 6 -- **IL CASO CHE DEVE FALLIRE**: lo stesso strumento sul blob VECCHIO

> ### **Lo zero del criterio 4 vale solo se lo strumento VEDE ancora il difetto.**

Lo strumento `425b8d47`, rigirato su `0f060670`, da' ### **`166` differenze su `166`**, `63 802 623` elementi
diversi, e la prima posizione diversa coincide col primo arco tolto in ### **`166` su `166`** -- ### **gli stessi numeri del referto di `cb24b95`, al numero.**
Lo strumento non e' diventato cieco.

**COME, e dichiarato:** i byte del simulatore vecchio si prendono con
`git cat-file -p b17caec:soliton_simulator.py` ### **in binario, non con**
`git checkout` *(par.7: gli stati sono TRE, e <<stesso contenuto, byte diversi>> e' la
trappola CRLF)*; lo scambio avviene ### **fra due corse, mai durante una** *(par.5)*; e
il ripristino si verifica ### **col blob**, che torna `e2940b3c`, con
`git status` **pulito**. Le due uscite restano nel repo col blob nel nome
*(`.sim-0f060670` e `.sim-e2940b3c`)*, perche' ### **un'uscita che non dice quale
blob l'ha prodotta non e' una misura.**

## CRITERIO 7 -- lo strumento del tetto causale `19d08753`, RIGIRATO

> ### **E' il criterio che chiude il `FERMO` di `eeb54be`.**

| | sul VECCHIO `0f060670` *(`eeb54be`)* | sul CURATO `e2940b3c` |
|---|--:|--:|
| verifiche del controllo (A) | `300` | `300` |
| ### con **DIFFERENZE** | ### **`166`** | ### **`0`** |
| verifiche **con potere** | `296` | `296` |
| **INVERIFICABILI** | `4` | `4` |
| (B) **non ha discriminato** | `0` | `0` |
| verifiche **vuote** | `0` | `0` |
| archi confrontati | `141 541 432` | `141 541 432` |
| esclusi: estremo oltre `len(r)` | `4 792` | `4 792` |
| esclusi: `dt_e` non finito | `0` | `0` |

> ### **OGNI numero e' IDENTICO fra le due colonne, tranne uno:**
> ### **`con_differenze`, che passa da `166` a `0`.**

### **E QUESTO E' IL PEZZO PRECISO A CUI ATTRIBUIRE IL `FERMO`.** Il referto del
2026-10-04 si fermo' dicendo *<<il controllo (A) trova differenze in 83 passi su 150, e
non traggo conclusioni>>*. ### **Le `166` differenze erano
### `83` passi x 2 verifiche, e venivano DA QUI**:
il controllo leggeva `_dt_e_ultimo` **dopo** una nascita, cioe' leggeva ### **il valore
di un altro arco**. ### **Curata la causa, il controllo passa su tutte le `300` verifiche.**

### ⚠ **E `esclusi_dt_e_non_finito` RESTA `0` anche dopo la cura, benche' ora
### gli archi nati abbiano `dt_e = NaN`: va spiegato, non lasciato.** Gli archi nati
toccano **nodi nuovi**, e il controllo li scarta **prima**, col filtro *<<estremo oltre
`len(r)`>>* -- che vale `4 792` in **entrambe** le
colonne. ### **Quindi le celle `NaN` nuove non arrivano mai al filtro di finitezza:** il
`0` non e' una svista, e ### **non vuol dire
che il `NaN` non c'e'.**

## LA CONSEGUENZA PER IL PASSO (2) DEL TETTO, registrata e NON decisa

> ### ⛔ **Dopo questa cura, gli archi NATI nel passo hanno `dt_e = NaN`.**
> Prima avevano un valore **finito, preso da un altro arco**: peggio, ma **invisibile**.
> ### **Il passo (2) del tetto causale -- che vuole far leggere `dt_e` a
> ### `memoria_hebbiana_moto`, cioe' alla voce 5, DOPO la nascita -- avra' bisogno di
> ### una REGOLA per quegli archi.**
> ### ⚠ **E' UNA DECISIONE DI LUCA, DA PRENDERE ALLORA E NON ADESSO.** Qui si
> registra **che serve**, non **quale**. *(Scritta in `doc/REGISTRO_FISICA.md`, scheda
> `veleno-derivate` e domanda aperta della scheda `coesione`, e nella voce
> dell'indice.)*

## I NUMERI, IN UNA TABELLA

| criterio | che cosa pretende | numero | esito |
|---|---|--:|---|
| **0** | la patch su `0f060670` ridA' `e2940b3c` al byte | `True` | ### **PASSA** |
| **1** | STATO identico al byte su 150 passi | **`0`** | ### **PASSA** |
| **2** | le sole eccezioni sono `_dt_e_ultimo` e `_sin2_vir` | `83` su 1 nome | ### **PASSA**, e la classificazione dei 6 contatori e' ### **APPROVATA DA LUCA** *(2026-10-05)* |
| **3** | Schwinger: identiche al byte | `0` su `128` | ### **PASSA** |
| **4** | lo strumento sul blob nuovo da' `0` sui 166 | `0` | ### **PASSA** |
| **5** | copertura `2s`, non `s` | `1.0000` = `1.0000` | ### **PASSA** |
| **6** | lo strumento sul blob VECCHIO ridA' le 166 | `166` | ### **PASSA** |
| **7** | il tetto da' `0` passi invalidi in (A) | `0` su `300` | ### **PASSA** |

## LA CONFIGURAZIONE INTERA (`H-P5`) -- **non i flag toccati, TUTTI**

> *(`CONFIG-1`: sei misure furono prese con **28 leggi su 31 spente**, e ogni referto
> dichiarava i **quattro flag accesi da me**. **Il flag era acceso, e intorno a lui il
> sistema era spento.**)*

```
====================================================================================================
LA CONFIGURAZIONE INTERA (`P5`) -- non i flag toccati, TUTTI
====================================================================================================
  booleani di modulo confrontati con l'argv del DRIVER: 81
  -> IN CONFIGURAZIONE DEL DRIVER: nessuna differenza. ZERO su 81.
```

**I VALORI TIMBRATI DALLA CORSA**, letti dal json dello strumento del tetto sul blob
curato *(e sono una SELEZIONE, non l'intera configurazione: l'intera e' il confronto
qui sopra)*:

| flag | valore | | flag | valore |
|---|---|---|---|---|
| `COES_ADIM` | `True` | | `K_C` | `2.0` |
| `COES_CAUSALE` | `True` | | `LAM` | `0.8` |
| `CS_DINAMICO` | `True` | | `MEM_HEBB` | `True` |
| `CS_M` | `2.0` | | `TAU_LOC` | `1.0` |
| `DT` | `0.01` | | `TEMPO_SEGNO` | `False` |
| `GRAV_BIFASE` | `True` | | `VIRIALE` | `True` |

**LA SCENA:** `--nmasse 3 --sep 6.1158`, seme `11`, `n_iniziale = 14000`, `150` passi.

### ⚠ **E UNA COSA DA DICHIARARE SUL SIGILLO, non da tacere:** il sigillo prende la
configurazione dal **CLI del driver** *(`_cli_flag.argv_del_driver`, `:204`)* -- e quindi
**non e' configurato a mano** -- ### **ma non la TIMBRA nel suo json.** La dichiarazione
qui sopra e' **ricostruita** chiamando **lo stesso helper sullo stesso driver**, e vale
perche' ### **il blob del driver e' quello di `HEAD`** *(verificato: `42ed4904`,
`dirty = False`)*. ### **Se il driver fosse cambiato fra la corsa e il
referto, questa ricostruzione MENTIREBBE** -- per questo il blob si verifica, e per
questo il difetto va **in coda**: un sigillo dovrebbe timbrare la sua configurazione,
non lasciarla ricostruire.

## LA PIATTAFORMA

`python 3.13.2` · `numpy 2.3.0` · Windows 11 · AMD64

## CHE COSA RESTA IN CODA, dichiarato e non curato

*(Congelamento dell'infrastruttura, decisione di Luca del 2026-10-04: i difetti degli
strumenti che non falsano il risultato si annotano e si mettono in coda.)*

1. **`_veleno_registro` non confrontabile** nel comparatore del sigillo *(un dizionario
   che contiene array)*: ### **contato fra le differenze, non taciuto.**
2. **`celle_nan_appese` e' un NOME SCADUTO** nello strumento `425b8d47`: misura
   `len_dopo - len_prima`, che coincideva col veleno **solo prima della cura**.
3. ~~La **domanda per Luca** sulla lista di eccezioni del criterio 2.~~
   ### ✅ **CHIUSA il 2026-10-05: la classificazione e' APPROVATA**, col motivo e
   con un lockstep indipendente su Linux. ### **Non e' piu' in coda.**
