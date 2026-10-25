# LA CURVATURA, PARTE 0-BIS: LE DUE MISURE CHE MANCANO PRIMA DI LEGGERE IL RAPPORTO DELLE DUE c (la strada A1, in memoria)

> **Il mandato:** di Luca, `2026-10-25` *(«facciamo le misure», `16:58`; [[PROGETTO-CURVATURA]], [[LORENTZ-MATERIA-INTERFERENZA]])*. ### **NESSUN file del nucleo; `B-4` e l'impronta `2e7f795d2a52fbe7` intatte.** ### **Lo script `csv/_curvatura_0bis.py`** *(importa `csv/_curvatura_prototipo.py`, `_u1_terzo`, `_u1_prototipo`)*, ### **il referto `doc/referti_l2/curvatura_0bis.{txt,jsonl}`.**
> ### ⚠ **L'ORDINE, riportato:** ### **il mandato chiede queste misure PRIMA della parte `1`, ma quando e' arrivato la parte `1` era gia' corsa e committata** *(`31ee70cc`, FERMO sulla chiave di `(c)`)*: ### **la parte `1` NON si tocca; questo mandato si esegue ORA, PRIMA del mandato «colmare le mancanze del censimento» arrivato prima di lui** *(perche' e' il completamento della parte `0`; l'ordine si registra: [[PRECEDENZA-IN-CODA]])*.
> ### **LA CORREZIONE CHIESTA:** ### **la frase «a `r 0.5` il rapporto e' `1.11`: oltre la luce» di `b0edae62` NON E' MISURATA** *(la luce in `A1` viene dalla carta; `v_b` non e' una velocita' che un pacchetto raggiunge)*: ### **si annota nel task history della curvatura e nella relazione.**

**LIVELLO:** misure in memoria.

## 0. LA STELLA POLARE

1. **`A14`:** ### **non si applica** *(nessuna legge cambia)*. 2. **Il gradino:** ### **`(c)` limiti noti:** ### **`c = 1` e `v_max/s = 0.598467` a `r = 1`.** 3. **Aggiunge un numero o una legge?** ### **No.** 4. **Tocca `rho`, `c_s` o il segno?** ### **Misura come `c_s` entra nelle velocita'.** 5. **Emergente o imposto?** ### **Non si applica.**

## 1. LE SCELTE DI METODO *(fissate qui, prima dei numeri)*

- ### **`M1`, LA LUCE IN `A1`:** ### **una regione a `cs` uniforme:** ### **`s = 0.05` per tick ovunque, `s_rif = s/r`** *(quindi `l = 1/r` per arco, `A_p = (sqrt3/4)/r^2`)*, ### **`CampoA1` col tempo del campo `F1` dalla `s_arco` VERA.** ### **ENTRAMBI i metodi:** ### **`(i)` la DISPERSIONE: i blocchi del tick del campo** *(`_u1_prototipo.blocchi_campo` con `CampoA1`)*, ### **`v_g` a `|k| = 1e-3` in `12` direzioni;** ### **`(ii)` un PACCHETTO** *(`_u1_prototipo.corsa_pacchetto`)* ### **contro la sua velocita' prevista dallo spettro.**
- ### **LE UNITA':** ### **«archi per tempo proprio»** *(la velocita' per tick divisa per `s`)* ### **e «lunghezza propria per tempo proprio»** *(per `l = 1/r`)*; ### **IL RAPPORTO con la materia si fa nella STESSA unita'** *(archi per tempo proprio per tutte e due: il fattore `l` si semplifica)*.
- ### **COURANT IN `A1`:** ### **`omega^2 = s^2 (l/l*)/A_p lambda ~ s^2 r^2 lambda`, quindi `s r sqrt24 <= 2`: `s <= 0.40825/r`;** ### **al `r` massimo `2`: `s <= 0.2041`;** ### **`s 0.05` vale a ogni `r`.** ### **E si MISURA:** ### **`max|lambda|` fuori dalla gauge sulla griglia `48 x 48` a ogni `r`.**
- ### **`M2`, LA VELOCITA' MASSIMA VERA DELLA MATERIA:** ### **il generatore `H_r`, la banda della coppia a `K` seguita per CONTINUITA' su tutta la zona** *(dal `K`, per sovrapposizione col vicino gia' assegnato: NON l'ordinamento)*; ### **`|grad mu|` da Hellmann-Feynman** *(`dH_r = r dH_gen`)*; ### **le griglie `48`, `96`, `192`** *(la convergenza, la regola della parte `B` del censimento)*. ### **E accanto il massimo su TUTTE le bande** *(il `v_max` di `_triangoli_forza`, la griglia `48`)*. ### **La conferma con gli spettri completi** *(`A1`, `s 0.01`, `r` `0.5`, `1`, `2`: `_triangoli_forza.v_max`, tutte le bande)*. ### **Il pacchetto in dinamica a `r 0.5`: NON si fa** *(dichiarato: costoso e opzionale)*.
- ### **`M3`, IL RAPPORTO:** ### **`v_max/c_luce` e `v_b/c_luce`** *(`v_b/s = pi sqrt(r)/4`, `b0edae62`)* ### **nella stessa unita'.**

## 2. I CRITERI *(del mandato, le previsioni del guardiano)*

| | il criterio | il tipo |
|---|---|---|
| `1` | a `r = 1`: `c_luce = 1` arco per tempo proprio entro `1e-3`; `v_max/s = 0.598467` entro `1e-4` *(la banda di `K` seguita, griglia `48`)*; `x(1) = 1/4` | DEVE |
| `2` | `c_luce(r) = r` archi per tempo proprio entro `1e-3` a ogni `r` | PUO' FALLIRE |
| `3` | `v_max/s` contro le stime del guardiano *(`0.3821`, `0.5298`, `0.6623`, `0.7642` a `r` `0.5`, `0.8`, `1.25`, `2`)* entro `3e-3` | PUO' FALLIRE |
| `4` | `v_max/c_luce < 1` a ogni `r` | PUO' FALLIRE |
| `5` | `v_max/c_luce` costante in `r` | ### **DEVE FALLIRE, per la chiave giusta:** ### **la variazione fra `r 0.5` e `r 2` `> 1.5` volte** |
| servizio | Courant a ogni `r`: stabile a `s 0.05` | servizio |

### **Mi FERMO se** ### **una DEVE fallisce.**

## 3. TODO

1. questo task history, da solo; 2. lo script, prima dei numeri; 3. la corsa; 4. il referto, la relazione, le annotazioni della frase «oltre la luce».

## 4. ANNOTAZIONI DOPO LA PROVA A VUOTO *(ridotta, nello scratchpad: `r` `0.5`, `1`, `2`; la griglia `48`; PRIMA di committare lo script)*

### ⛔ **NON SI RISCRIVE, SI ANNOTA:** ### **i criteri della sezione `2` NON cambiano.**

1. ### ⛔ **LA DEVE `1` FALLIRA' sul valore di riferimento:** ### **il generatore a `r 1`, griglia `48`, da' `v_max/s = 0.598622` contro `0.598467` entro `1e-4`** *(lo scarto `1.6e-4`)*. ### **La mia ipotesi:** ### **`0.598467` viene da `_triangoli_forza.v_max`, che sui gruppi DEGENERI** *(a `eps 0` ogni banda del tick e' doppia per lo spin)* ### **prende il massimo su `61` direzioni in `[0, pi]`:** ### **la scansione sottostima fino a `1 - cos(1.5 gradi) = 3.4e-4`.** ### **LA DIAGNOSI aggiunta** *(una LETTURA, non un criterio)*: ### **il generatore con la STESSA scansione su `61` direzioni.** ### **Nella corsa vera la DEVE `1` fallira', il referto lo dira', e MI FERMO.**
2. ### **Le altre letture della prova a vuoto** *(non il referto)*: ### **la luce in `A1` va a `r` archi per tempo proprio entro `4e-8`** *(cioe' `1` lunghezza propria per tempo proprio)*; ### **`v_max/c` `0.764`, `0.599`, `0.382` a `r` `0.5`, `1`, `2`.**

## 5. IL RISULTATO *(dopo `52eba072`; con l'aggiunta del guardiano arrivata DOPO la corsa: la correzione `1` e `M4` qui, `M1-BIS` NON eseguita)*

### **IL REFERTO DELLA PARTE 0-BIS:** `doc/referti_l2/curvatura_0bis.{txt,jsonl}` *(`csv/_curvatura_0bis.py` `sha1-BYTE f5386aab` al commit `52eba072`; il task history `8288068d`)*. ### **`5/6`; UNA DEVE FALLITA, sul VALORE DI RIFERIMENTO** *(come la prova a vuoto aveva previsto)*. ### ⛔ **FERMO.**

### **`M1`, LA LUCE IN `A1`** *(una regione uniforme, `s 0.05`, `s_rif = s/r`)*: ### **`c` dalla dispersione `0.500000`, `0.800000`, `1.000000`, `1.250000`, `2.000000` archi per tempo proprio a `r` `0.5`, `0.8`, `1`, `1.25`, `2`** *(lo scarto dalla carta `4.1e-8`)*, ### **cioe' `1.000000` lunghezza propria per tempo proprio a ogni `r`;** ### **isotropa entro `7.9e-8`** *(le `12` direzioni, il `k` piccolo)*; ### **il pacchetto `0.48606`, `0.77740`, `0.97161`, `1.21440`, `1.94365` contro la previsione dallo spettro** *(`1e-4`-`4e-4`)*; ### **stabile a `s 0.05` per ogni `r`** *(Courant sulla carta `s <= 0.40825/r`)*.
- ### **LE UNITA'** *(la correzione `1` dell'aggiunta, errore del guardiano `n.65`)*: ### **la previsione della carta e' `c = r s` archi per TICK = `r` archi per TEMPO PROPRIO = `1` lunghezza propria per tempo proprio:** ### **le tre tornano.** ### **E con l'esponente di `31ee70cc`** *(`d ln v/d ln cs = 2.0245` nel gradiente, archi per tick)*: ### **archi per tick `= r s = s^2/s_rif`, l'esponente `2`: coerente** *(lo scarto `0.0245` e' del gradiente, non dell'unita')*.

### **`M2`, LA VELOCITA' MASSIMA VERA DELLA MATERIA** *(il generatore, la banda di `K` seguita per continuita')*:

| `r` | `0.5` | `0.8` | `1` | `1.25` | `2` |
|---|---|---|---|---|---|
| griglia `48` | `0.381810` | `0.529394` | `0.598622` | `0.661742` | `0.763619` |
| griglia `96` | `0.381986` | `0.529670` | `0.599163` | `0.662087` | `0.763971` |
| griglia `192` | `0.382093` | `0.529828` | `0.599237` | `0.662285` | `0.764186` |
| gli spettri completi *(`s 0.01`, tutte le bande, `48`)* | `0.381716` | -- | `0.598483` | -- | `0.763457` |

- ### ⛔ **LA DEVE `1` FALLISCE:** ### **`v_max/s = 0.598622` contro `0.598467` entro `1e-4`** *(`c = 1.000000` e `x(1) = 0.2500000002` passano)*. ### **LA DIAGNOSI** *(una lettura)*: ### **il generatore con la scansione su `61` direzioni, come `_triangoli_forza.v_max` sui gruppi degeneri, da' `0.598467`: il valore «noto» e' SOTTOSTIMATO dalla scansione** *(il difetto [[V-MAX-DIREZIONI]])*. ### **E la griglia `48` NON e' convergiuta** *(`0.598622` -> `0.599237` a `192`)*: ### **la regola della convergenza raffinando** *(il censimento, la parte `B`)*.
- ### **Le stime del guardiano** *(PUO' FALLIRE entro `3e-3`)*: ### **PASSANO** *(`0.3818`/`0.3821`, `0.5294`/`0.5298`, `0.6617`/`0.6623`, `0.7636`/`0.7642`)*.

### **`M3`, IL RAPPORTO nella stessa unita'** *(archi per tempo proprio)*: ### **`v_max/c` `0.7636`, `0.6617`, `0.5986`, `0.5294`, `0.3818`** *(PUO' FALLIRE `< 1` a ogni `r`: PASSA)*; ### **`v_b/c` `1.1107`, `0.8781`, `0.7854`, `0.7025`, `0.5554`;** ### **la variazione di `v_max/c` fra `r 0.5` e `r 2`: `2.000`** *(DEVE FALLIRE per la chiave giusta: PASSA)*.

### ⛔ **LA CORREZIONE CHIESTA DAL MANDATO:** ### **la frase di `b0edae62` «a `r 0.5` il rapporto e' `1.11`: oltre la luce» NON ERA MISURATA:** ### **`1.11` e' `v_b/c`, e `v_b` e' la `c` asintotica della dispersione massiva che nessun pacchetto raggiunge;** ### **con la velocita' massima vera, `v_max/c < 1` a ogni `r` misurato: NESSUN superamento della luce in `A1`.**

### **`M4`, `gamma` RISPETTO ALLA MATERIA DI `A1`** *(una RILETTURA dei numeri di `31ee70cc`, fatta a mano, non uno script)*: ### **`R1` nello script e' `2 pi eta/Lu`, la caduta della materia di OGGI; con `A1` la materia cade `1.50` volte** *(la parte `(d)`)*: ### **dalla velocita' della luce: `1 + gamma = 2.0245/1.50 = 1.350`, `gamma ~ 0.35`;** ### **dalla deflessione: `kappa/(1.5 R1)` `0.977`, `0.987`, `0.987` a `W` `12`, `16`, `24`, `gamma ~ 0`** *(con Ehrenfest che spiega l'`83%`)*. ### ⛔ **QUINDI la frase «`gamma` da Shapiro `1.02`» di `31ee70cc` era contro la materia di oggi, non contro quella di `A1`.**

### ⛔ **FERMO: la DEVE `1` e' fallita** *(sul valore di riferimento: [[V-MAX-DIREZIONI]])*. ### **NON ESEGUITA:** ### **la misura `M1-BIS` dell'aggiunta** *(la luce in due direzioni, l'ipotesi di anisotropia del guardiano)*: ### **resta in coda, dopo la decisione di Luca.** ### **LE DOMANDE A LUCA:** ### **`(1)` il valore di riferimento di `v_max/s`: `0.598622`** *(il gradiente vero, griglia `48`)* ### **o il valore convergente in griglia** *(`~0.5992`)*? ### **`(2)` si esegue `M1-BIS`?** ### **Le domande di `31ee70cc` restano aperte** *(non toccate)*.
