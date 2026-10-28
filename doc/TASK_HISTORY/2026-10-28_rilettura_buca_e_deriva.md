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
