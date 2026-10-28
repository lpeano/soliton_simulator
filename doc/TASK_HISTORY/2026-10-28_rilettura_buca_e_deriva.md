# 2026-10-28 — LA RILETTURA DELLA BUCA CONTRO IL CONGELATO, E LA DERIVA DEL CONGELATO *([[VUOTO-SUL-FONDO]], [[LIBRO-DEI-CONTI]], [[PROGETTO-MASSA-COLLETTIVA]], [[DOMANDA-GOBBA-SEGNO-GRAVITA]]; la risposta di Luca delle `14:27` a `58791831`)*

> ### **LIVELLO: una rilettura dei dati di `bd87c0d5` senza corse nuove** *(parte `1`)*; ### **corse BREVI in memoria** *(parte `2`)*; ### **nessun file del nucleo;** ### **il referto di `58791831` resta com'e'.**

## 0. LA RISPOSTA DELLE `14:27`, PER INTERO

```
RISPOSTA DI LUCA (2026-10-28 14:27) A 58791831 (IL SOLITONE CON LA SUA BUCA), sulla raccomandazione del guardiano

1. LA RILETTURA, SENZA CORSE NUOVE (sui dati di bd87c0d5): la vita e lo scarto di ogni corsa misurati RISPETTO AL
   CONGELATO allo stesso tempo fisico (la larghezza della corsa diviso quella del congelato, non diviso la larghezza
   iniziale), dalla fine della rampa; e il confronto tanh contro sin^2 A DURATA UGUALE dove i dati lo permettono
   (dichiaralo). Correzione dichiarata DOPO i numeri: il referto di 58791831 resta com'e'. La domanda: il vuoto vivo
   peggiora le cose rispetto al vuoto fermo, e di quanto? La vita dipende ancora da T_r?
2. LA DERIVA DEL CONGELATO (+17% in 600 a s 0.075, la taglia grande): misura, sulla carta e con corse brevi, da dove
   viene: lo stato del risolutore d'inviluppo non e' lo stazionario del passo discreto a s 0.075? (la rotazione al
   centro contro quella prevista; il profilo dopo 100 tick contro quello iniziale; la stessa misura a s 0.3, dove in
   74f99039 il congelato reggeva). E proponi (senza farlo) come ottenere uno stato davvero fermo del passo discreto col
   vuoto congelato (per esempio un rilassamento sul passo stesso), col costo.
3. La parte 2 del mandato (il risolutore autoconsistente) resta descritta e NON si fa finche' 1 e 2 non hanno risposto.
4. Nella MAPPA: la gobba confermata alla taglia grande (il centro 1.43-2.02 contro 0.98-0.99, col fondo) nella riga 12
   della lista in attesa, come misura; la riga 4 (il solitone con la sua buca): "la rampa non ha dato un oggetto
   stabile; la lettura in corso".
```

## 1. RAGIONAMENTO PRELIMINARE

### **CHE COSA HO LETTO PRIMA DI SCRIVERE** *(per nome di funzione)*

- ### **I dati:** ### **il congelato c'e' solo col FONDO, e solo fino al tick `8000`** *(tempo fisico `600`)*; ### **le corse della rampa vanno oltre** *(fino a `20491`)*. ### **Le serie sono campionate ogni `40` tick, piu' `t_rampa` e `T_MAX`.**
- ### ⚠ **QUINDI LA RILETTURA HA UN LIMITE CHE DICHIARO PRIMA:** ### **il rapporto col congelato esiste solo per `t <= 8000` e sui tick comuni;** ### **la tanh a `T_r 400` finisce la rampa a `9824`: per lei, DOPO la rampa, il rapporto NON ESISTE** *(senza corse nuove)*.
- ### **Il congelato per il vuoto UNIFORME non c'e'.** ### **Dal codice** *(`materia_vuoto.applica`: `alpha` dipende da `rho` e `Lambda`; gli altri pezzi della materia non toccano `phi`)*: ### **col vuoto congelato `psi` vede `phi` solo attraverso `Lambda = sum |phi|^2` per nodo,** ### **e `Lambda` e' `6` su ogni nodo in tutte e due le scene** *(`nan_e_leg.txt`, il minimo; il massimo lo misuro)*. ### **Se e' vero, il congelato del fondo vale anche per l'uniforme: lo CONTROLLO al bit** *(`(c0)` della parte `2`)* ### **prima di usarlo.**
- ### **La rotazione** *(`_solitone_vuoto_congelato.corsa`)*: ### **`-angle(a1/a0)` per tick, `a = <Q, psi(nodo centrale)>`.** ### **In `74f99039`, `s 0.3`, zero simmetrico: congelato `-0.159588`, senza legame** *(lo zero di oggi)* ### **`-1.401070` contro congelato `-1.102066`: la differenza `+0.299` e `mu` del risolutore `+0.29831`.**

### **CHE COSA CREDO PRIMA DI GUARDARE**

- ### **Parte `1`:** ### **contro il congelato la rampa lenta peggiora MENO di quanto diceva il referto, ma peggiora:** ### **circa `60%` che la vita relativa dipenda ancora da `T_r`.**
- ### **Parte `2`:** ### **che lo stato del risolutore NON sia lo stazionario del passo a `s 0.075`** *(l'inviluppo e' un limite continuo; a `s` piccolo il passo e' piu' fine ma il solitone e' piu' largo in archi e la correzione reticolare diversa)*: ### **circa `65%`.** ### **E che a `s 0.3` la deriva ci sia anche** *(il referto di `74f99039`: `6.630 -> 7.344` in `2000` tick, `+10.8%`, che io avevo letto come «reggeva»)*.

### **CHE COSA NON SO**

- ### **La rotazione prevista per lo zero simmetrico:** ### **la regola «la rotazione della materia senza legame piu' `mu`» viene dallo zero di oggi;** ### **la misuro sul toro con un'onda piana a `K`, non la assumo.**
- ### **Se un'onda piana a `K` uniforme sia autostato del passo al bit:** ### **lo controllo** *(la sovrapposizione deve restare `1`)*.

## 2. PROGETTAZIONE DEL RAGIONAMENTO

### **PARTE `1`: `csv/_rilettura_buca.py`** *(legge i jsonl, nessuna corsa)*

| | la scelta | il perche' |
|---|---|---|
| 1 | ### **il rapporto `w(t) / w_cong(t)`, sui tick comuni con `t >= t_rampa` e `t <= 8000`** | ### **il mandato;** ### **il limite dei dati** |
| 2 | ### **la vita relativa: il primo tick comune dopo la rampa con `|w/w_cong - 1| > 0.2` o frazione `< 0.8`;** ### **«oltre `t`» se non si rompe fino all'ultimo tick comune;** ### **«non misurabile» senza tick comuni** | ### **le stesse soglie di `_solitoni_triangoli`;** ### **la frazione resta ASSOLUTA** *(il congelato la tiene sopra `0.99`)* |
| 3 | ### **lo scarto massimo relativo dopo la rampa, e quello DURANTE la rampa** *(lettura)* | ### **la domanda «di quanto»** |
| 4 | ### **l'uniforme contro il congelato del fondo SOLO se `(c0)` passa al bit;** ### **altrimenti «senza riferimento»** | ### **sezione `1`** |
| 5 | ### **la durata uguale:** ### **la durata della rampa** *(da `t = 0` al tick con `r = 1`)* ### **e il tempo di salita `10%`-`90%`, calcolati dalle due funzioni dello script;** ### **se nessuna coppia coincide, LO DICO, e riporto le coppie piu' vicine per tempo di salita, come «non uguali»** | ### **il mandato: «dove i dati lo permettono»** |

### **PARTE `2`: `csv/_deriva_congelato.py`** *(corse brevi; `N 1e6`; lo zero simmetrico; `S1`; `cs` spento)*

1. ### **`(c0)` DEVE: col vuoto congelato `psi` dopo `20` tick e' lo stesso AL BIT col fondo e con l'uniforme** *(`s 0.075`)*; ### **e `Lambda` per nodo uguale al bit nelle due scene.**
2. ### **`(c1)` DEVE: la larghezza del congelato a `100` tick ridata AL BIT dalla serie di `grande_fondo_congelato`** *(il tick `80` e il `120` della serie sono a passo `40`: confronto i tick `40`, `80`)*.
3. ### **Le misure, a `s 0.075` e a `s 0.3`** *(il risolutore a quel `s`; la scena del toro come `prepara`, `L` dalla larghezza)*, ### **`100` tick col vuoto congelato:**
   - ### **la rotazione per tick al centro** *(media e deviazione)*; ### **la rotazione per tick nodo per nodo, la sua dispersione pesata con `rho` entro `w`:** ### **uno stazionario ruota TUTTO INSIEME;**
   - ### **la rotazione PREVISTA:** ### **quella dell'onda piana a `K`** *(`Q e^{2 pi i (m1+m2)/3}`, uniforme, gli stessi pezzi del congelato ma senza il legame)* ### **piu' `mu` del risolutore** *(la regola di `74f99039`, dichiarata qui)*; ### **e la sovrapposizione dell'onda piana con se stessa dopo `20` tick** *(deve restare `1`: se no, non e' autostato e la previsione non vale)*;
   - ### **il profilo:** ### **`|rho(100) - rho(0)| / |rho(0)|`** *(norma `2`)*, ### **la larghezza a `100` contro quella iniziale;** ### **la fedelta' `|<psi(0), psi(100)>| / N`** *(`1` per uno stazionario)*.
4. ### **LA PROPOSTA** *(non eseguita)*: ### **un rilassamento sul passo stesso, col costo dai tempi MISURATI di un tick alle due `s`.**

### **COSA MI FAREBBE FERMARE**

- ### **`(c0)` fallito:** ### **la rilettura dell'uniforme resta «senza riferimento»** *(non mi ferma la parte `1` del fondo)*.
- ### **`(c1)` fallito:** ### **lo stato della parte `2` non e' quello delle corse: FERMO.**

## 3. TODO DEL NEXT STEP

1. ### **questo task history, committato e pushato da solo;**
2. ### **i due script e le voci d'inventario, committati prima di girarli;**
3. ### **le corse brevi; i due referti; la RELAZIONE; la MAPPA** *(la riga `12` come misura; la riga `4`: «la rampa non ha dato un oggetto stabile; la lettura in corso»)*.


## 2-bis. ANNOTAZIONI *(il task history non si riscrive: si annota)*

### **`(a)` IL RILIEVO DI LUCA DOPO LE `14:27`** *(arrivato mentre la misura della deriva girava; in coda dietro di essa, `L-UN-PROMPT`)*, ### **alla lettera:**

```
DISTINGUI DUE CAUSE (lettura del guardiano): (a) lo stato di partenza non e' l'esatto stazionario del passo discreto e
PERDE CODE (la larghezza e' un secondo momento: poche code lontane la gonfiano): allora la frazione entro la larghezza
iniziale resta sopra 0.95, la crescita rallenta fino a fermarsi, e cala con s piu' piccolo; (b) il solitone S1 e'
INSTABILE PER NATURA in 2D (S1 "sopra-critica in 2D", DOSSIER_S1_S4): allora cambia il cuore, la crescita non si ferma
o accelera, e non dipende da s. Riporta, per il congelato alla taglia grande: la frazione entro la larghezza iniziale e
il picco nel tempo, la forma della crescita (rallenta o accelera), e lo stesso a s 0.3 (74f99039) per il confronto.
```

- ### ⚠ **I DATI NON BASTANO:** ### **i jsonl hanno la frazione entro `3 w0`, non entro la larghezza iniziale;** ### **a `s 0.3`** *(`solitone_vuoto_congelato.jsonl`)* ### **la serie ha la larghezza e la frazione entro `3 w0` ogni `20` tick, non il picco.** ### **Servono due corse congelate:** ### **`8000` tick a `s 0.075`, `2000` a `s 0.3`** *(tempo fisico `600` tutte e due)*: ### **`csv/_code_o_cuore.py`.**
- ### ⚠ **UN RILIEVO SUL CRITERIO, PRIMA DEI NUMERI:** ### **in 2D la frazione entro il raggio quadratico medio PARTE sotto `1`** *(per una gaussiana `1 - 1/e = 0.63`)*: ### **«sopra `0.95`» assoluto non vale nemmeno a `t = 0`.** ### **Riporto la frazione entro `w_in` ASSOLUTA e RELATIVA al suo valore iniziale;** ### **leggo la soglia `0.95` sulla RELATIVA, e lo dichiaro qui.**
- ### **LE GRANDEZZE, FISSATE ORA:** ### **ogni `3` di tempo fisico** *(`40` tick a `s 0.075`, `10` a `s 0.3`)*: ### **la larghezza, la frazione entro `w_in` e entro `3 w0`, il picco di `rho`;** ### **la forma della crescita: la pendenza media di `w/w_in` nel tempo fisico nei quattro quarti `[0,150]`, `[150,300]`, `[300,450]`, `[450,600]`;** ### **«rallenta» se le quattro pendenze DECRESCONO, «accelera» se crescono, altrimenti «non monotona».**
- ### **I CONTROLLI:** ### **`(k1)` a `s 0.075` le larghezze ai tick comuni = `grande_fondo_congelato` AL BIT;** ### **`(k2)` a `s 0.3` le larghezze ogni `20` tick = la corsa `simm L 81 congelato` di `74f99039` AL BIT** *(li' il vuoto uniforme: vale se `(c0)` passa)*.
- ### **CHE COSA CREDO:** ### **dai dati gia' visti** *(il picco a `s 0.075` scende da `5062` a `4257` in `600`; a `s 0.3` la larghezza sale del `2%` nei primi `20` tick, e a `L 120` finisce piu' larga che a `L 81`)*: ### **piu' la `(a)`, circa `60%`:** ### **il salto iniziale e la dipendenza dalla scatola sono da code;** ### **il picco che cala e' un indizio per la `(b)`.**


### **`(b)` DOPO LE MISURE** *(i referti `rilettura_buca.txt`, `code_o_cuore.txt`, `deriva_congelato.txt`; gli script di `fcfa13de`)*

- ### ⛔ **`(c0)` FALLISCE:** ### **`Lambda` per nodo e' uguale al bit col fondo e con l'uniforme, ma `psi` dopo `20` tick NO.** ### **La mia lettura del codice della sezione `1` era SBAGLIATA:** ### **col vuoto congelato `psi` sente le FASI di `phi`, non solo `Lambda`.** ### **Quindi, come scritto prima:** ### **l'uniforme resta «senza riferimento» nella rilettura;** ### **e `(k2)`** *(il confronto con `74f99039`, che aveva il vuoto uniforme)* ### **NON era applicabile:** ### **FALLISCE, scarto massimo `0.147`;** ### **i dati di partenza coincidono** *(`w0` `6.6003`, `w_in` `6.6297`, la larghezza al tick `20` `6.7685`)*.
- ### ⛔ **LO SCRIPT DELLA DERIVA SI E' FERMATO** *(un mio errore)*: ### **costruisco l'onda piana DENTRO `BE.conv("simm")`, e li' `coppia_K` trova i gruppi `[2, 4, 2]`;** ### **la correzione e' un commit a se':** ### **lo stato si costruisce fuori dal contesto.** ### **Non l'ho corretta subito perche' `_code_o_cuore.py`, che girava, importa `_deriva_congelato.py`.**
- ### **`(k1)` PASSA al bit** *(`201` tick comuni)*: ### **lo stato e' quello delle corse.**
- ### **PARTE `1`, LA RILETTURA** *(il fondo; i tick comuni fino a `8000`)*: ### **alla grande la vita relativa decresce ancora con `T_r`:** ### **tanh `2746`, `1584`, non misurabile; `sin^2` `2867`, `2507`, `27`** *(a `400` gia' oltre alla fine della rampa, `1.2375`)*; ### **all'ultimo tick comune la larghezza e' `1.14`-`1.16` quella del congelato.** ### **Alla piccola nessuna rottura relativa** *(scarto massimo `<= 0.136`)*. ### **Nessuna coppia tanh/`sin^2` a durata o salita uguale.** ### **La mia stima `60%` sulla dipendenza da `T_r`: tiene.**
- ### **CODE O CUORE:** ### **`s 0.075`: la frazione entro `w_in` relativa scende a `0.871`, il picco a `0.841`, la crescita non monotona** *(veloce, lenta, poi riaccelera)*; ### **`s 0.3`: `0.949`, `0.922`, non monotona;** ### **a `600` di tempo fisico `1.173` contro `1.092`.** ### **Nessuna delle due letture regge pulita:** ### **la `(a)` vuole il cuore fermo e la deriva piu' piccola a `s` piccolo, e non e' cosi';** ### **la `(b)` vuole la deriva indipendente da `s`, e non e' cosi'.** ### **Un indizio:** ### **il salto del `2%` al tick `20` e il ritorno al `40` stanno allo stesso TICK alle due `s`, non allo stesso tempo fisico:** ### **un effetto del passo discreto.** ### **La mia stima `60%` per la `(a)`: non confermata.**


### **`(c)` LA DERIVA, DOPO LA CORREZIONE** *(`35ca68b1`, lo script `sha1-BYTE 0c424cfa`; `deriva_congelato.txt` riscritto)*

- ### **`(c1)` PASSA al bit; `(c0)` fallisce ancora, com'era.**
- ### **LA ROTAZIONE:** ### **a `s 0.075` al centro `-0.043033`, prevista `-0.043030`, scarto `-3.0e-06`; la dispersione fra i nodi entro `w_in` `4.2e-07`;** ### **a `s 0.3` `-0.159614` contro `-0.159672`, scarto `+5.8e-05`, dispersione `2.2e-05`.** ### **L'onda piana a `K` e' autostato del passo** *(sovrapposizione `1.000000000000` dopo `20` tick)*: ### **la previsione vale.**
- ### **IL PROFILO** *(allo stesso tempo fisico `7.5`)*: ### **`|rho - rho0|/|rho0|` `4.2e-03` a `s 0.075`, `4.7e-03` a `s 0.3`; la fedelta' `0.9981` e `0.9979`.**
- ### **LA LETTURA:** ### **lo stato del risolutore ruota TUTTO INSIEME alla frequenza prevista, a `s 0.075` meglio che a `s 0.3`:** ### **e' vicinissimo allo stazionario del passo.** ### **La mia stima** *(`65%` che NON lo fosse)* ### **non e' confermata.** ### **La deriva lunga** *(`+17%` contro `+9%` in `600`, piu' grande a `s` piccolo)* ### **non viene da un errore di partenza grossolano;** ### **resta da capire da dove** *(un residuo del `0.2%` di fedelta' che non si smorza, o un'instabilita' lenta: le due letture di Luca restano aperte)*.
- ### **LA PROPOSTA** *(non eseguita)*: ### **un FILTRO sul passo stesso:** ### **`psi <- normalizza( somma_{t<T} e^{i theta t} U^t psi )`, con `theta` la rotazione misurata e `T = 2 pi / mu`** *(`85` tick a `s 0.075`, `22` a `s 0.3`)*; ### **il passo `U` dipende da `psi`** *(il legame)*: ### **si ripete fino a un punto fisso.** ### **Il costo di un giro, dai tempi misurati: circa `5` s a `s 0.075`, `1` s a `s 0.3`;** ### **il numero dei giri non e' noto prima di provare.** ### ⚠ **La tolleranza d'arresto sarebbe un numero da SCEGLIERE** *(`A1`)*: ### **la decide Luca, o si deriva.** ### **La prova: poi `600` di tempo fisico congelati** *(circa `8` minuti a `s 0.075`)*.


### **`(d)` LA CORREZIONE DELLA SEZIONE `1`** *(Luca `15:49`, punto `3`; il task history non si riscrive: si annota)*

- ### ⛔ **LA FRASE DELLA SEZIONE `1` E' SBAGLIATA:** ### **«col vuoto congelato `psi` vede `phi` solo attraverso `Lambda = sum |phi|^2` per nodo».** ### **Vero che il solo ponte e' `materia_vuoto.applica`, che legge `Lambda`;** ### **ma lo legge AL MOMENTO DELLA CHIAMATA:** ### **in posizione `13` del passo, DOPO che il Grover e il salto del vuoto** *(posizioni `5`-`8`)* ### **hanno fatto interferire le fasi di `phi`.** ### **Il congelato rimette `phi` solo a fine tick.** ### **Quindi `psi` sente le FASI del vuoto attraverso `Lambda` a meta' tick.** ### **Il meccanismo, con file e righe:** `doc/TASK_HISTORY/2026-10-28_congelato_lungo_e_fasi_del_vuoto.md`, *sezione `1`*.
