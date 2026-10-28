# 2026-10-28 — IL SOLITONE CON LA SUA BUCA: LA RAMPA DEL VUOTO *([[MAPPA-DEL-LAVORO]], [[VUOTO-SUL-FONDO]], [[LIBRO-DEI-CONTI]], [[PROGETTO-MASSA-COLLETTIVA]]; il mandato di Luca delle `22:59` del `2026-10-27`)*

> ### **LIVELLO: misure in memoria; nessun file del nucleo;** ### **`B-4`, `B-5` e l'impronta `2e7f795d2a52fbe7` intatte.**
> ### **La rampa del vuoto e' uno STRUMENTO DI PREPARAZIONE DELLO STATO, dichiarato in memoria, NON una legge.**

## 0. IL MANDATO DELLE `22:59`, PER INTERO *(nel repo non c'era: `80644d93` ne registro' solo l'arrivo)*

```
LIVELLO: misure in memoria; nessun file del nucleo; B-4, B-5 e l'impronta 2e7f795d2a52fbe7 intatte.
La rampa del vuoto e' uno strumento di preparazione dello stato, dichiarato in memoria, NON una legge.

DECISIONE DI LUCA (2026-10-27 22:59): si promuove dalla lista in attesa "il solitone con la sua buca".

PERCHE (dal guardiano, da 76eecbf5): dal vuoto del fondo il vuoto PRENDE energia dalla materia
(+2.3e3 - +2.5e3), ma il solitone vive solo 1.6-1.9 volte di piu'; col vuoto congelato e' stabile su
qualunque vuoto. Lo stato di partenza viene dal risolutore col vuoto uniforme e fermo: sul fondo non
e' l'equilibrio comune di materia e vuoto.

PARTE 1, LA RAMPA: si parte dallo stato di 76eecbf5 col vuoto congelato (stabile); i pezzi del vuoto
(CAMM-GROVER-VUOTO, CAMM-SPOSTAMENTO-VUOTO, CAMM-FASE-VUOTO) e la rotazione gemella del legame sul
vuoto si accendono lentamente: l'angolo di ciascuno per r(t), da 0 a 1 in un tempo fisico T_r con una
forma liscia dichiarata PRIMA (per esempio sin^2), poi il tick intero. Le scene: il vuoto del fondo
(F0 di 76eecbf5) e, per confronto, il vuoto uniforme; S1, lo zero simmetrico, cs spento, s 0.075,
N 1e6 L 81 e una seconda taglia. T_r = 25, 100, 400 in tempo fisico; dopo la rampa almeno tempo
fisico 800 col tick intero. Le misure col libro dei conti (strada A): larghezza e picco nel tempo; la
vita dalla fine della rampa; Lambda per estremita' al centro e sul bordo (la buca) nel tempo;
l'energia per pezzo e per regione; il dare e avere sul confine; M e V.

PREVISIONI (scritte PRIMA): DEVE PASSARE: M e V entro 1e-10; con r = 0 per sempre lo stato resta
quello del congelato. PUO' FALLIRE (circa 50%): col vuoto del fondo e la rampa piu' lenta il solitone
resta entro il 20% della larghezza per 800 di tempo fisico dopo la rampa, alle due taglie. PUO'
FALLIRE: la vita cresce con T_r. LETTURA: la buca alla fine della rampa (profondita', larghezza) e se
si stabilizza; l'uniforme contro il fondo.

PARTE 2, SE LA RAMPA NON BASTA (solo descritta, non eseguita senza decisione): il risolutore
autoconsistente (la materia stazionaria su un Lambda(x) dato, il vuoto stazionario nel fondo col
potenziale del legame, l'iterazione fino al punto fisso): che cosa servirebbe e il costo stimato.

PARTE 3 (solo se la parte 1 trova un oggetto stabile): la scomposizione di 0fb93b8c sull'oggetto con
la sua buca, allo zero simmetrico, con in piu' l'energia della buca (l'energia del vuoto rispetto al
fondo indisturbato): quanta parte della massa e' la buca?

FORMA: il task history prima; lo script committato prima della corsa (senza CRLF); il referto (txt +
jsonl, timbro sha1-BYTE); la RELAZIONE; l'indice; la riga della MAPPA nello stesso commit; FILE
CAMBIATI esatto; le corse lunghe a pezzi (il riavvio notturno della macchina di Luca).
```

## 1. RAGIONAMENTO PRELIMINARE

### **CHE COSA HO LETTO DAL CODICE PRIMA DI SCRIVERE** *(per nome di funzione, non per riga)*

- ### **I pezzi del vuoto e i loro angoli** *(`flussi_parziali.grover`, `hop_phi`, `z_nodo`, `z_arco`)*: ### **l'angolo e' `theta = pi * s_nodo * frazione`** *(e `s_arco` per lo spostamento)*, ### **lineare nella frazione:** ### **«l'angolo per `r`» e' la frazione per `r`.**
- ### ⚠ **`_frazione_valida` VIETA la frazione `0`** *(`0 < frazione <= 1`)*: ### **a `r = 0` il pezzo si SALTA.** ### **Non e' un pavimento** *(`A11`)*: ### **a `theta = 0` il Grover parziale e' `P_u + (I - P_u) = I` e lo spostamento `alpha I + beta S` ha `beta = 0`:** ### **saltare e' il valore che il pezzo PRENDE a `r = 0`.**
- ### **`CAMM-FASE-VUOTO`** *(`motore._fase_vuoto`)*: ### **con `cs` spento** *(`mot.cs is None`)* ### **non fa niente, al bit:** ### **la rampa lo scala per completezza, ma non cambia nulla.**
- ### **La rotazione gemella del legame sul vuoto** *(`materia_vuoto.applica`)*: ### **la fase `beta` su `phi` sta NELLO STESSO PEZZO della fase `alpha` su `psi`, con la stessa frazione.** ### **Per scalare solo `beta`, lo script ha la sua copia di quelle righe** *(in memoria)*: ### **`alpha` per la frazione intera, `beta` per la frazione per `r`.**
- ### ⛔ **QUINDI LO SCRIPT HA UN SECONDO PERCORSO DEL TICK** *(il difetto per cui `tick.py` esiste)*: ### **lo si accetta SOLO come strumento di preparazione, e con un controllo positivo:** ### **a `r = 1` il tick con la rampa deve dare lo stato di `tick.percorri_tick` AL BIT.**

### **CHE COSA CREDO PRIMA DI GUARDARE**

- ### **Che la rampa lenta aiuti, ma non basti:** ### **il risolutore da' una materia in equilibrio col vuoto UNIFORME e FERMO;** ### **accendere il vuoto lentamente lascia al vuoto il tempo di scavare la buca, ma la materia non e' preparata per il vuoto che si muove.** ### **La mia stima per la PUO' FALLIRE `(p1)`: meno del `50%` del mandato, circa `35%`.**
- ### **Che la vita cresca con `T_r`** *(la `(p2)`)*: ### **circa `60%`.**
- ### **Che il vuoto uniforme si comporti peggio del fondo** *(come in `76eecbf5`: li' il vuoto cedeva energia alla materia)*.

### **CHE COSA NON SO**

- ### ⚠ **SE `r = 0` DA' AL BIT IL «CONGELATO» DI `76eecbf5`:** ### **quel congelato rimette `phi` a `phi0` ALLA FINE di ogni tick, ma DENTRO il tick i pezzi del vuoto girano** *(e la fase `beta`, che dipende da `rho`, rompe la stazionarieta' del flusso dentro il tick)*. ### **A `r = 0` invece `phi` non si muove mai.** ### **I due «congelati» sono la stessa fisica nel limite, ma non per forza gli stessi bit.**
- ### **Se la buca si stabilizza, e con che profondita'.**
- ### **Se alla taglia piccola** *(`N 1e5`)* ### **il congelato sia stabile a `s 0.075`:** ### **a `s 0.3` NON lo era** *(`solitone_vuoto_congelato.txt`: vita `1080` a `L 48`)*.

## 2. PROGETTAZIONE DEL RAGIONAMENTO

### **LE SCELTE, DICHIARATE PRIMA DEI NUMERI**

| | la scelta | il perche' |
|---|---|---|
| 1 | ### **la forma: `r(t) = sin^2(pi t / (2 T_r))` per `t <= T_r`, poi `1`** | ### **l'esempio del mandato;** ### **derivata nulla ai due capi** |
| 2 | ### **`r` per tick: il valore al CENTRO del tick** *(`t = (n + 1/2) s`)*, ### **uguale per tutti i pezzi del tick** | ### **il palindromo resta un palindromo dentro ogni tick** |
| 3 | ### **la seconda taglia: `N 1e5`, `L 48`** | ### **la coppia di `solitone_vuoto_congelato.txt`** *(«le due taglie», `N 1e6` e `N 1e5`)* |
| 4 | ### **i tick: `T_r / s` di rampa, poi `800 / s`** *(`s 0.075`: `333`, `1333`, `5333` piu' `10667`)* | ### **il mandato** |
| 5 | ### **la vita dalla fine della rampa:** ### **il primo controllo dopo la rampa in cui la larghezza esce del `20%` da quella iniziale o la frazione entro `3 w0` scende sotto `0.8`** | ### **il criterio di `_solitoni_triangoli`** *(`TOLL_LARGH`, `FRAZ_MIN`, `RAGGIO_FRAZ`)* ### **gia' usato in `76eecbf5`;** ### **anche una rottura DURANTE la rampa si registra** |
| 6 | ### **la buca:** ### **`Lambda` per estremita' = `Lambda_k / grado_k`;** ### **media al CENTRO** *(`r <= w_in/2`)*, ### **sul BORDO** *(`w_in < r <= 2 w_in`)*, ### **LONTANO** *(`r > 2 w_in`)*; ### **la profondita' `1 - centro/lontano`;** ### **la larghezza: la radice del secondo momento radiale del deficit `(lontano - Lambda_k/grado_k)` sul disco `2 w_in`** | ### **le regioni di `76eecbf5`** *(`R_VICINO 2`)*; ### **il centro a mezza larghezza** |
| 7 | ### **il picco: il massimo di `rho_k`** | -- |
| 8 | ### **i conti ogni `3` di tempo fisico, la strada `A` a ogni tick sul disco `2 w_in`** | ### **come `76eecbf5`** |

### **I CONTROLLI, NELL'ORDINE**

1. ### **`(k0)` DEVE: il tick con la rampa a `r = 1` = `tick.percorri_tick` AL BIT** *(`20` tick, dal fondo, alle due taglie)* -- ### **il controllo positivo del secondo percorso.**
2. ### **`(k1)` DEVE: il congelato di `76eecbf5` ridato AL BIT** *(la serie delle larghezze di `F0 congelato` nel jsonl, `N 1e6`)*.
3. ### **`(d1)` DEVE: `M` e `V` entro `1e-10` in ogni corsa.**
4. ### **`(d2)` DEVE: con `r = 0` per sempre lo stato resta quello del congelato:** ### **`(i)` `phi` uguale a `phi0` AL BIT per tutta la corsa;** ### **`(ii)` la corsa NON si rompe** *(il criterio della riga `5`, sull'orizzonte del congelato, `600` di tempo fisico)* ### **SE il congelato non si rompe;** ### **`(iii)` la distanza massima dalla larghezza del congelato si riporta come LETTURA** *(e' la domanda della sezione `1`)*.
5. ### **`(p1)` PUO' FALLIRE: col fondo e `T_r 400`, la larghezza entro il `20%` di quella iniziale per tutti gli `800` dopo la rampa, alle due taglie.**
6. ### **`(p2)` PUO' FALLIRE: la vita dalla fine della rampa NON decresce con `T_r`, e a `400` e' maggiore che a `25`** *(«oltre l'orizzonte» conta piu' di qualunque numero; due «oltre» contano uguali)*, ### **col fondo, alle due taglie.**

### **LE LETTURE** *(non criteri)*: ### **la buca alla fine della rampa e alla fine della corsa** *(profondita', larghezza)*, ### **se si stabilizza;** ### **l'uniforme contro il fondo;** ### **l'energia per pezzo e per regione; il dare e avere sul disco `2 w_in`.**

### **COSA MI FAREBBE FERMARE**

- ### **`(k0)` o `(k1)` falliti: lo strumento non e' quello che dice di essere;** ### **non si corre il resto.**
- ### **una DEVE fallita: si committa lo stato e il fallimento, e FERMO.**

### **LE CORSE A PEZZI** *(il riavvio notturno)*: ### **una corsa per invocazione** *(`--corsa <taglia> <scena> <T_r>`)*, ### **ognuna appende la sua riga al jsonl;** ### **`--referto` scrive il txt dalle righe.** ### **Il costo stimato:** ### **circa `94000` tick per taglia;** ### **a `L 81` circa `2` ore, a `L 48` meno di una.**

## 3. TODO DEL NEXT STEP

1. ### **questo task history, da solo, committato e pushato;**
2. ### **lo script `csv/_solitone_con_la_buca.py`** *(LF, `_presidio.avvia`)*, ### **una prova breve a `L 48`;** ### **lo script committato prima della corsa, con l'inventario;**
3. ### **le corse a pezzi; il referto; la RELAZIONE, l'indice, la MAPPA nello stesso commit;**
4. ### **la parte `2` descritta nel referto; la parte `3` solo se la parte `1` trova un oggetto stabile.**
