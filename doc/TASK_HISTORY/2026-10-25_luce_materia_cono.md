# LA LUCE E LA MATERIA ATTORNO A UN CONO *(la parte C2 del mandato delle 20:44)*

> **Il mandato:** di Luca, `2026-10-25`, `20:44`, la parte `C2` *([[PROGETTO-MITOSI]], la sezione `4`, la seconda misura sulla carta; [[LORENTZ-MATERIA-INTERFERENZA]], [[PROGETTO-U1]])*.
> ### **Strumenti in `csv/`, in memoria; nessun file del nucleo.** ### **Lo script `csv/_luce_materia_cono.py`, il referto `doc/referti_l2/luce_materia_cono.{txt,jsonl}`.**

**LIVELLO:** una misura di propagazione su un grafo con un difetto conico.

## 0. LA STELLA POLARE

1. **`A14`:** ### **non si applica.** 2. **Il gradino:** ### **la geometria fatta dal CONTEGGIO** *(un nodo a `5` vicini)* ### **devia la luce e la materia dello stesso angolo?** 3. **Aggiunge un numero o una legge?** ### **No.** 4. **Tocca `rho`, `c_s` o il segno?** ### **No** *(il vuoto non entra)*. 5. **Emergente o imposto?** ### **Il difetto e' imposto; la deviazione e' cio' che si misura.**

## 1. LA SCENA *(fissata qui)*

- ### **IL DISCO A SETTORI:** ### **`n` settori triangolari di lato `R`, il settore `s` coi nodi `(a, b)`, `a, b >= 0`, `a + b <= R`, alla posizione `a e_s + b e_{s+1}`** *(`e_s` la direzione a `60 s` gradi)*; ### **gli archi `(a,b)-(a+1,b)`, `(a,b)-(a,b+1)`, `(a+1,b)-(a,b+1)`; i triangoli `(a,b),(a+1,b),(a,b+1)` e `(a+1,b),(a+1,b+1),(a,b+1)`;** ### **il bordo `b = 0` del settore `s` incollato al bordo `a = 0` del settore `s - 1`** *(ciclicamente)*, ### **il centro comune.** ### **`n = 6`: il disco PIATTO** *(il centro a `6`)*; ### **`n = 5`: il CONO** *(il centro a `5`, il difetto d'angolo `pi/3`)*. ### **`R = 120`.**
- ### **LA CARTA:** ### **ogni elemento** *(nodo, arco, triangolo, estremita')* ### **ha la posizione nel riferimento piatto del SUO settore** *(il settore `s` ai suoi `60 s` gradi)*; ### **sul cono l'unico taglio e' fra il settore `4` e il settore `0`** *(il raggio a `300` gradi del `4` = il raggio a `0` gradi dello `0`)*. ### **I nodi sul taglio prendono la posizione del settore `0`.**
- ### **IL VERSO:** ### **i pacchetti partono a `x0 = -55`, `y = +-b`, verso `+x`** *(attraverso i settori `2, 1, 0` sopra; `3, 4` e poi il taglio sotto)*. ### **Nella carta: il fascio SOPRA non attraversa il taglio** *(la deviazione attesa `0`)*; ### **il fascio SOTTO lo attraversa e gira di `+pi/3`** *(la rotazione del taglio)*: ### **LA CONVERGENZA dei due fasci = `delta_sotto - delta_sopra`, attesa `pi/3` sul cono e `0` sul piatto, a ogni `b`.**

## 2. LE DUE DINAMICHE *(fissate qui)*

- ### **LA LUCE: il campo `F1` di `_u1_prototipo`** *(`A`, `E` per arco; `w = s^2 (l/l*)`, `l/l* = sqrt(3)`; `V = somma B^2/(2 A_p)`, `A_p = sqrt(3)/4`, NON compatto; il tick `spinta(1/2) deriva(1/2) deriva(1/2) spinta(1/2)` di `tick_campo`)*, ### **su un grafo QUALUNQUE: una classe nuova dello script, con le stesse operazioni; le placchette sono i triangoli del disco, orientati in senso antiorario nella carta del settore.** ### **Sul cono ogni arco interno ha due triangoli equilateri, quindi `l/l*` e `A_p` sono quelli di oggi ovunque** *(la stella duale sul cono: nessun cambiamento locale)*. ### **`s = 0.3`** *(stabile: `S_STABILE` del prototipo)*.
- ### **IL PACCHETTO DI LUCE:** ### **`_u1_prototipo.pacchetto_campo` su un toro piatto `256 x 256`** *(`k0` lungo `+x`, `|k0| = 2 pi 41/256 = 1.006`, `W 6`)*, ### **copiato sul disco arco per arco con le coordinate di reticolo della carta** *(l'arco di direzione `-a` prende `-A`, `-E` dell'arco `+a`)*.
- ### **LA MATERIA: il GENERATORE `(I - P_u) + P_-` a `eps 0`, il limite `s -> 0` del tick** *(come in `C1`)*, ### **`psi(t) = exp(-i H t) psi(0)`** *(`scipy.sparse.linalg.expm_multiply`, la matrice sparsa)*. ### ⚠ **PERCHE' NON IL TICK:** ### **un tick di `_triangoli.camminata` su un toro di `25600` nodi costa `0.61` s** *(misurato)*, ### **e un pacchetto a `v ~ 0.07` per attraversare `~110` archi ne vuole `~2000` a `s 0.2`: ore per corsa.** ### **Il generatore e' la stessa fisica a `s -> 0`; lo dichiaro e non lo nascondo.**
- ### **IL PACCHETTO DI MATERIA:** ### **la banda dispersiva ALTA della coppia** *(`mu` in `[1/2, 1]`)*, ### **a `k = K + q`, `q = 0.5` lungo `+x`, `W 8`:** ### **su un toro piatto `256 x 256` la busta `g(r) e^{i k.r} u_k` e poi la PROIEZIONE ESATTA sulla banda** *(la FFT, per ogni `k` il proiettore sull'autovettore di `_u1_terzo.H_gen`)*, ### **copiata sul disco estremita' per estremita'** *(lo slot `a` sul lato di partenza dell'arco di tipo `a`, `3 + a` su quello d'arrivo)*.

## 3. LE MISURE E I CRITERI *(fissati qui, prima dei numeri)*

- ### **IL BARICENTRO:** ### **della densita' d'energia** *(luce: `w E^2/2` al punto medio dell'arco, `B^2/(2A_p)` al baricentro del triangolo)* ### **o di `|psi|^2`** *(materia: alla posizione del nodo dell'estremita')*, ### **nella carta.** ### **LA FINESTRA D'INGRESSO: finche' il `99%` del peso sta nei settori `2, 3`** *(un riferimento continuo)*; ### **LA FINESTRA D'USCITA: quando il `99%` del peso sta nei settori `0, 1`, fino al tempo massimo.** ### **LA DIREZIONE = la retta ai minimi quadrati del baricentro nella finestra** *(la velocita' media)*; ### **`delta = theta_uscita - theta_ingresso`.**
- ### **IL TEMPO MASSIMO, dichiarato:** ### **quando il baricentro arriva a `x = +55` nella carta, o al primo istante in cui il peso a distanza `<= 4` dal bordo del disco supera `1e-6` del totale** *(il secondo e' il presidio del bordo: si riporta)*.
- ### **`b = 24, 32, 40`;** ### **la convergenza in larghezza: la luce anche a `W 9`, la materia anche a `W 11`, a `b 32`.**
- ### **LA TOLLERANZA DEL PIATTO, dalla larghezza:** ### **`|delta| <= 0.1/(|k| W)`** *(un decimo della larghezza angolare del pacchetto: la luce `0.1/(1.006 x 6) = 0.017` rad; la materia `0.1/(0.5 x 8) = 0.025` rad)*.

| | il criterio | il tipo |
|---|---|---|
| `0` | ### **i controlli dello strumento:** ### **il campo su grafo, costruito dal toro, = `_u1_prototipo.Campo` per `20` tick entro `1e-13`;** ### **il generatore sparso = `_massa_nei_difetti.H_diretto` su un toro `6 x 6` entro `1e-15`;** ### **i gradi** *(il centro `5` o `6`, l'interno `6`)*; ### **la carta: ogni arco interno con due triangoli; il pacchetto di materia nella banda entro `1e-10`** | DEVE |
| `1` | ### **sul PIATTO nessuna deviazione: `|delta| <= 0.1/(|k| W)` per i due fasci, la luce e la materia, a ogni `b`** | DEVE |
| `2` | ### **la LUCE sul cono: la convergenza `pi/3` entro il `5%` a ogni `b`** | PUO' FALLIRE |
| `3` | ### **la MATERIA sul cono: la convergenza uguale a quella della luce entro il `5%` a ogni `b`** *(il principio di equivalenza per la geometria del conteggio)* | PUO' FALLIRE |
| `4` | ### **la convergenza dipende da `b` come `1/b`** | ### **DEVE FALLIRE, PER LA CHIAVE GIUSTA: il rapporto convergenza(`b 24`)/convergenza(`b 40`) entro il `10%` da `1`, NON `40/24`** *(la luce e la materia)* |

### **Mi FERMO** ### **se il criterio `0` o `1` fallisce** *(lo strumento non misura la geometria)*.

## 3-bis. ANNOTAZIONE, PRIMA DELLA CORSA *(le prove di costruzione dello script, NON misure)*

- ### **IL TORO DEL PACCHETTO DI LUCE E' `128 x 128`, NON `256`:** ### **`pacchetto_campo` costa (`k` del pacchetto) x (nodi del toro), e a `256` non si chiude in tempi umani;** ### **quindi `N_K0 = 20`, `|k0| = 2 pi 20/128 = 0.982`** *(non `1.006`)*, ### **e la tolleranza del piatto per la luce `0.1/(0.982 x 6) = 0.0170` rad.** ### **La copia sul disco entro `D_COPIA = 50` dalla sorgente** *(oltre, il pacchetto e' sotto `e^-30`)*, ### **lo stesso per la materia.**
- ### **LA FINESTRA D'USCITA vuole anche il baricentro a `x > 0`** *(oltre il centro: il fascio SOPRA e' nei settori `0, 1` gia' prima del centro)*; ### **la finestra finisce quando il baricentro ha percorso `L_USCITA = 40` dentro di essa, o alla guardia del bordo.**
- ### ⚠ **UN NUMERO GIA' VISTO, dichiarato:** ### **la prova di costruzione a piena taglia, la luce sul cono a `b 32`, `W 6`, ha dato `delta` `-0.0041` sopra e `+1.0456` sotto** *(la convergenza `1.0497`)*. ### **Le soglie del §3 erano gia' fissate e NON cambiano.** ### **La materia: il pacchetto copiato ha `<H> = 0.4812` contro `1 - mu(k0) = 0.4827`, varianza `7e-5`** *(nella banda alta: la copia degli slot e' giusta)*; ### **la norma fuori banda sul toro `5e-32`.**
- ### **IL CONTROLLO `0` aggiunto allo script:** ### **la banda della materia** *(il massimo sulle corse della norma fuori banda, `<= 1e-10`)*.

## 4. TODO

1. questo task history, da solo; 2. lo script, committato prima della corsa; 3. la corsa; 4. il referto, la relazione, l'indice.

## 5. IL RISULTATO *(dopo `0a4c2d11`)*

### **IL REFERTO DELLA LUCE E DELLA MATERIA ATTORNO A UN CONO:** `doc/referti_l2/luce_materia_cono.{txt,jsonl}` *(`csv/_luce_materia_cono.py` `sha1-BYTE 3209518c`, al commit `0a4c2d11`)*. ### ⛔ **`6/9`, DUE DEVE FALLITI, ed entrambi sono DIFETTI DEL MIO STRUMENTO, non fisica:** ### **`FERMO` su `C2`; la correzione e' un commit a se'.**

- ### **I CONTROLLI `0` PASSANO:** ### **il campo su grafo = `_u1_prototipo.Campo` al bit per `20` tick; il generatore sparso = `H_diretto` al bit; i dischi** *(il piatto `51091` nodi, `152490` archi, `101400` triangoli; il cono `42576`, `127075`, `84500`)*; ### **il pacchetto di materia nella banda alta a `5e-32`.**
- ### ⭐ **LA LUCE SUL CONO** *(la `PUO' FALLIRE (2)`: PASSA)*: ### **la convergenza dei due fasci `1.04588`, `1.04969`, `1.04257` a `b` `24`, `32`, `40`, contro `pi/3 = 1.04720`** *(entro lo `0.5%`)*; ### **NON dipende da `b`: il rapporto `b 24`/`b 40` e' `1.0032`, non `40/24`** *(la chiave per la luce TIENE; il criterio `4` cade solo perche' manca la materia)*; ### **in larghezza a `b 32`: `1.04969` a `W 6`, `1.04715` a `W 9`** *(si avvicina a `pi/3` allargando il pacchetto: la diffrazione dal vertice)*. ### **Il fascio sopra devia `-0.004`, `-0.004`, `-0.0007`** *(atteso `0`)*.
- ### ⛔ **IL DIFETTO `1`, LA MATERIA:** ### **NESSUNA corsa di materia ha la finestra d'uscita: la guardia del bordo** *(`1e-6` del peso a distanza `<= 4` dal bordo)* ### **scatta dopo `18`-`38` punti** *(`t = 85`-`185`; a `W 11` subito)*. ### **La diagnosi** *(misurata dopo, su una copia in memoria)*: ### **il disco di lato `130` mette la sorgente a `~40` archi dal bordo esagonale** *(la proiezione della sorgente `(-65, 32)` sulla normale del bordo del settore `2` e' `72`, il bordo a `112`: l'avevo stimato male)*; ### **gia' a `t = 0` il `20%` del peso sta entro distanza `40` dal bordo,** ### **e le code del pacchetto lento** *(che deve correre `t ~ 1800`)* ### **superano `1e-6` presto.** ### **La luce, piu' stretta e veloce, ci passa.**
- ### ⛔ **IL DIFETTO `2`, IL FASCIO SOTTO SUL PIATTO:** ### **la finestra d'uscita «`99%` nei settori `0, 1`» e' pensata per il CONO** *(dove il settore `5` non c'e')*: ### **sul piatto il fascio sotto resta nel settore `5`** *(`y < 0`)* ### **e la finestra non si apre mai** *(`0` punti)*. ### **Il fascio sopra sul piatto devia `0.00000`** *(come deve)*.
- ### **LA CORREZIONE, da fare in un commit a se' e non decisa qui:** ### **un disco piu' grande per la materia** *(o la sorgente piu' vicina al centro con `b` piu' piccoli, o una guardia scritta sulla distanza percorsa)*; ### **la finestra d'uscita come «il `99%` in una carta CONTINUA dopo il centro»** *(sul piatto `4, 5, 0, 1`; sul cono `0, 1`)*.
