# LA DERIVA E LA FRECCIA DEL VUOTO: `F3` E L'IBRIDO *(Luca `2026-11-03` `08:29`)*

> **Il mandato:** `TF3` = `TP1000` col vuoto `F3` *(fasi `(0, 0, pi)` per `(A2, A1, A1+A2)`, la freccia per nodo nulla)*; **solo se `TF3` si muove meno
> di `TP1000` o in modo diverso**, `TFI` *(l'ibrido `theta = pi/2`)*. La partenza: lo stesso solitone di `TP1000`. Le misure a blocchi di `1000` accanto a `TP1000`.
> **Le letture, di Luca, scritte prima:** (a1) su `F3` non si muove, sull'ibrido in mezzo: la causa e' la freccia, con una forza che cresce con la lunghezza;
> (a2) si muove come su `F0`: la freccia non c'entra; (a3) si muove in un'altra direzione; (a4) `F3` non regge il solitone come `F0` *(gia' prima di `9000`)*; (a5) altro.
> **La condizione:** (f5) commuta. ### **E' soddisfatta:** `95fa6cbe`, lo scarto `0` per ogni rotazione e per lo specchio.
> **La coda** *(`[[PRECEDENZA-IN-CODA]]`, decisione di Luca)*: questo **subito dopo la freccia di `F0`, PRIMA di `TL120`**.

## 1. LE PREMESSE DAL CODICE *(cosa credo, e cosa NON so)*

- **La lunghezza della freccia:** Luca scrive `2` per `F0`; il referto `95fa6cbe` misura **`4`**, con la mia definizione *(la somma sulle DUE estremita'
  del nodo per direzione: `2 sum c_d e_d`)*. **E' solo il fattore `2` della definizione:** i rapporti sono gli stessi *(l'ibrido `(0, 0, theta)`: `4 |cos(theta/2)|`,
  cioe' `2 sqrt2` a `pi/2`)*. Lo dichiaro e non cambio la definizione.
- ### **LA PARTENZA DIPENDE DAL VUOTO, nel codice:** `_vuoto_vivo_B.partenza` costruisce `B` a `Gamma` con `CB.coppia(z, phi0)` *(la coppia di Bloch SUL vuoto `phi0`)*
  e `mu` di Rayleigh col tick sul vuoto. **Luca chiede lo stato iniziale IDENTICO:** quindi ### **`psi` iniziale si costruisce su `F0` esattamente come `TP1000`, POI il
  vuoto si sostituisce con `F3`.** **Dichiaro anche quanto cambierebbe:** nel primo pezzo calcolo la partenza costruita su `F3` *(lo stesso `V.partenza`, col vuoto `F3`)*,
  e ne registro la sovrapposizione con quella di `TP1000` e il suo `mu`. **Non la uso.**
- **Che cosa resta uguale a `t = 0`:** `|phi|` e' lo stesso per `F0` e `F3` *(cambia solo la fase di una direzione)*, quindi `Lambda` e' lo stesso nodo per nodo;
  l'energia del vuoto e' la stessa per costruzione *(`95fa6cbe`)*. **Prevedo:** il primo campione di `TF3` ha `rho`, `Lambda`, il cuore, `w`, l'alone **al bit** di `TP1000`.
  **Cosa NON so:** se il libro dei conti al primo campione e' al bit *(dipende da come `conti_per_nodo` somma i termini con le fasi)*.
- **Che cosa cambia:** il tick del vuoto. `|tick(F0) - F0| / |F0| = 0.467` *(`95fa6cbe`)*: **non so** se `F0` e `F3` evolvono «allo stesso modo a meno delle fasi»;
  se la materia sentisse il vuoto SOLO attraverso `Lambda` e l'evoluzione di `|phi|` fosse la stessa, `TF3` darebbe la stessa `rho` di `TP1000` — **e la misura lo dice.**
  ### **Il controllo che PUO' fallire:** `TF3` deve DIFFERIRE da `TP1000` dopo il primo pezzo *(lo `sha_fine`)*; se fosse uguale, il vuoto non e' stato sostituito.
- **Le bande `D`** *(`righe_D`)* si calcolano sul vuoto della corsa *(`F3`)*, e `mu` resta quello della partenza *(`F0`)*: **`D` non e' fra le misure di Luca**, lo dichiaro.
- **La freccia del vuoto nel tempo:** una funzione nuova della libreria, `vuoto.freccia` *(la definizione di `95fa6cbe`)*, con i suoi test; in `TF3` ogni campione registra
  la freccia media sui nodi e quanto varia fra i nodi. **Per `TP1000`** *(che non la registra)* **la leggo dagli stati completi di `TM1000`** *(a `2000`, `6000`, `10000`, al bit
  di `TP1000`)* e da quelli di `DG1000`.
- **I dati:** come `TP1000`, i `jsonl` in `doc/referti_l2/accensione_lenta/` *(`~17` MB per `TP1000`)*. **Il tempo:** `11` pezzi da `~545` s, `~1.7` ore per corsa.
- **`TFI`** *(fasi `(0, 0, pi/2)`, il numero e' di Luca)*: la scrivo ora nella tabella delle corse; **la giro solo se la condizione di Luca si verifica**, e la condizione
  la leggo dal referto di `TF3` con il criterio della sez. `2`.

## 2. PROGETTAZIONE DEL RAGIONAMENTO

1. **Questo task history, da solo.** Commit.
2. **Il codice:**
   - `vuoto.py`: `freccia(inc, L, phi)` *(il vettore complesso per nodo)* e `freccia_media(...)`; `test_vuoto.py`: `V5` *(`F0`: `4` a `60` gradi su ogni nodo)*, `V5-N`
     *(`F3`: nulla)*, `V5-F` *(`F0` ruotato di `60` gradi ha la stessa freccia di `F0`: DEVE FALLIRE)*;
   - `corsa_accensione.py`: `CORSE["TF3"]`, `CORSE["TFI"]`, `VUOTI = {"TF3": (0, 0, pi), "TFI": (0, 0, pi/2)}` *(`F3` letto da `_solitone_dal_fondo.FASI`, non riscritto)*;
     il vuoto sostituito con `fondo_con_fasi` dopo la partenza; la partenza su `F3` registrata; la freccia in ogni campione.
   - L'inventario, il README se serve. **Commit.** Poi **`D6`** e la cassetta.
3. **`TF3`**, un pezzo alla volta *(il driver col semaforo)*.
4. **La carta** `csv/solitone/carta_freccia.py` *(scritta mentre `TF3` gira: un file nuovo, che la corsa non importa)*, committata prima di girarla.
5. Il referto, la relazione, l'esito qui, la MAPPA. **Commit.** Poi, **solo se la condizione**, `TFI` e la carta rigirata.

**La carta, i DEVE:**

| | che cosa | il tipo |
|---|---|---|
| `T0` | il vuoto di `TF3` a `t = 0` e' `fondo_con_fasi(F3)` AL BIT *(lo `sha` registrato, ricalcolato)* | DEVE PASSARE |
| `T1` | il primo campione di `TF3` uguale a quello di `TP1000` *(il cuore, `w`, l'alone, `M`, `V`)* AL BIT | DEVE PASSARE |
| `T1-F` | lo `sha_fine` del primo pezzo di `TF3` uguale a quello di `TP1000` | DEVE FALLIRE |
| `A3` | `M` e `V` *(`accensione.a3`)* | DEVE PASSARE |
| `A4` | il libro col `par` della corsa | DEVE PASSARE |

**Le misure, a blocchi di `1000`, accanto a `TP1000`:** lo spostamento dal centro periodico *(srotolato)*, la velocita', la direzione *(l'angolo, e il coseno con `A1`, `A2`,
`A1+A2`)*, il tempo a cui parte il moto *(il logaritmo dello spostamento a tratti, `carta_deriva.logaritmo`)*, il cuore, `w`, l'alone, la freccia del vuoto.

### **LA CONDIZIONE DI `TFI`, scritta prima** *(la traduzione MIA di «si muove meno o in modo diverso», dichiarata)*:
- **«meno»:** lo spostamento a `16000` di `TF3` sotto **meta'** di quello di `TP1000` *(`68.45` nodi)*;
- **«in modo diverso»:** la direzione dello spostamento totale a piu' di **`30` gradi** da quella di `TP1000` *(`-173.1` gradi)*, o il tempo di partenza del moto fuori da `9000 +- 2000`.
- **Se nessuna delle tre:** `TFI` non si gira, e lo scrivo. **Se Luca intende altro, corregge.**

### Che cosa mi farebbe FERMARE

- `T0`, `T1`, `A3`, `A4` che falliscono, o `T1-F` che passa;
- un pezzo che si ferma per un errore;
- la cassetta non tutta verde dopo `D6`.

## 3. TODO DEL NEXT STEP

- [ ] commit di questo file *(e la coda nella relazione)*;
- [ ] il codice, i test, l'inventario; commit; `D6`; la cassetta;
- [ ] `TF3` *(~`1.7` ore)*; intanto la carta, committata prima di girarla;
- [ ] il referto, le letture accanto ai fatti *(decide Luca)*; `TFI` solo se la condizione; poi `TL120`.

## 4. ESITO *(2026-11-03, dopo `TF3`; il referto `doc/referti_l2/deriva_e_freccia.txt`)*

- **`T0`, `T1`, `A3`, `A4` passano; `T1-F` fallisce come deve. `TM` FALLISCE** *(la mia definizione ridà `12000` su `TP1000`)*: **FERMO**, le domande a Luca nella relazione.
- **Le premesse, annotate** *(non riscritte)*:
  - «la partenza dipende dal vuoto»: **nel codice si'; nel risultato no**, alle cifre stampate *(la sovrapposizione `1.0`, lo stesso `mu`)*;
  - «cosa NON so: se il libro al primo campione e' al bit»: **lo e'** *(`T1` passa)*;
  - **la freccia di `F3` NON resta nulla sotto il solitone** *(il modulo per nodo fino a `2.29`)*, e **quella di `F0` perde la media** *(circa `0` gia' a `6000`)*: non l'avevo previsto;
  - **la condizione di `TFI`:** il «meno» e' vero *(`7.557` contro `34.23`)*; il tempo del moto non conta *(`TM` fallito)*.
- **TODO:** la decisione di Luca su `TM` e su `TFI`; poi `TL120`.

## 5. LE DECISIONI DI LUCA DOPO `fe409582`, E IL PIANO DI `TFI`

- **`TM` si abbandona come numero:** il moto non ha un inizio netto. **Il fallimento resta scritto** *(`fe409582`)*. Il confronto fra le corse si fa con lo spostamento, la velocita' a blocchi e la pendenza di `ln s`.
- **La lettura di `TF3`: la (a1).** Su `F3` il solitone vaga *(`7.6` nodi, `1.76` per `1000`, la direzione che cambia a ogni blocco)*; su `F0` deriva *(`68.5` nodi, `17.1` per `1000`, lungo `-A1`)*; il cuore, `w`, l'alone quasi uguali: **la (a4) esclusa**. **La deriva su `F0` la causa la freccia del vuoto di fondo.** **Il fatto in piu':** sotto il solitone la freccia tende a `~2` in tutte e due le corse, ma solo con la freccia uniforme di fondo il solitone corre.
- **`TFI` si fa** *(la condizione «meno» e' vera)*, **stesso protocollo di `TF3`.**

### Le premesse *(cosa credo, e cosa NON so)*
- **La lunghezza della freccia di fondo, dalla misura** *(`vuoto.freccia` sul fondo a `t = 0`, con la mia definizione)*: `F0` `4`, l'ibrido `2 sqrt2 = 2.83`, `F3` `0` *(`V5`, `V5-I`, `V5-N`)*. **La carta la RICALCOLA dal vuoto di ciascuna corsa**, non la ricopia.
- **Cosa NON so:** come cresce la deriva con la freccia. **Tre punti non decidono una forma** *(lineare, soglia, quadratica)*: **la carta scrive la tabella, non adatta una curva.**

### Il piano
1. Questa sezione, la relazione, la MAPPA *(la (a1))*: un commit.
2. **La carta** *(`carta_freccia.py`)*: `TM`, `META_V`, `T_MOTO_TP`, `TFI_TEMPO` e la colonna del tempo del moto **tolti**; **una tabella nuova: per ogni corsa la lunghezza della freccia di fondo a `t = 0` contro lo spostamento a `16000`, la velocita' massima a blocchi e la pendenza di `ln s` sulle due rette lunghe**; la condizione di `TFI` scritta come fatto storico *(il «meno» e la direzione)*. La pendenza delle rette lunghe la ritorna `carta_deriva.logaritmo` **senza cambiare la stampa** *(il referto di `TP1000` deve restare uguale nelle righe che gia' c'erano)*. Commit; `D6`; la cassetta.
3. **`TFI`**, un pezzo alla volta *(il driver col semaforo)*; poi la carta, il referto, la relazione, l'esito, la MAPPA.

### I DEVE della carta, dopo
`T0`, `T1`, `T1-F` *(deve fallire)*, `A3`, `A4`, **per `TF3` e per `TFI`**. **In piu', un controllo che puo' fallire:** `FR0` la lunghezza della freccia di fondo ricalcolata dal vuoto della corsa uguale a quella dei test *(`4`, `2 sqrt2`, `0`, entro `1e-12`)*.

### Che cosa mi farebbe FERMARE
Un DEVE fallito; un pezzo di `TFI` che si ferma per un errore; la cassetta non tutta verde; le righe del referto di `TF3` e `TP1000` che cambiano con la carta nuova *(diverse da `fe409582` dove non devono)*.

### TODO
- [ ] commit di questa sezione con la MAPPA e la relazione;
- [ ] la carta; commit; `D6`; la cassetta;
- [ ] `TFI` (~`1.7` ore); la carta; il referto; poi `TL120`.
