# LA TORSIONE DEL TEMPO PROPRIO, SOLO MISURA *(il mandato unico di Luca `2026-11-17` `18:04`)*

> **Il mandato:** **D-R1, D-R2, D-R3 SOSPESE** *(non annullate; D-R4 resta)*. **Prima di scegliere l'innesco si MISURA il quanto di olonomia nella forma del tempo proprio** [[MITOSI-QUANTO-OLONOMIA]]: per ogni arco `Theta_a(t) = omega * somma sui tick (dtau_i - dtau_j)`, il quanto `|Theta_a| = 2 pi`. **Le prove prima** *(K1 il vuoto F3 puro; K2 il legame con la fase vera; K3 l'integrale fra stati)*, **poi la misura sugli stati di C2 e di C1** *(M1-M6)*, **la sez. `14` della carta della mitosi, FERMO per Luca.** **Nessun file del nucleo; C1 e C2 non si toccano; la misura sugli stati parte DOPO la loro chiusura nel registro.**
> **L'ordine dei lavori** *(L-UN-PROMPT, PRECEDENZA-IN-CODA)*: **il mandato e' arrivato durante B2** *(il commit di `Motore.cresci` sul ramo `mitosi`, che aspettava la suite)*: **B2 si chiude** *(non dipende da D-R1-D-R3: e' infrastruttura, D-R5)*, **poi questo mandato; B3-B7 restano in coda dopo.**

## 1. LE PREMESSE DAL CODICE *(cosa credo; cosa NON so)*

### 1.1 COME `dtau` ENTRA NELLA FASE DEL VUOTO *(letto oggi)*

- **`primo_ordine/flussi_parziali.py`**: **il tempo proprio del nodo e' `dtau_nodo = mot.dtau * cs_k`** *(`dtau_nodo`: con `mot.cs is None` e' `mot.dtau`)*; **`s_nodo = dtau_nodo / dtau_rif`** con **`dtau_rif = 1`** *(l'UNITA': il raccordo `omega dtau_rif = pi` di B-4 da' `omega = pi`)*; **i pezzi di nodo applicano `e^{i pi s_k frazione}`** *(`z_nodo`)*, **quelli d'arco `e^{i pi s_arco frazione}`** con `s_arco` la MEDIA ARMONICA dei due capi *(B-3)*.
- **`csv/solitone/tick_lapse.py`** *(il tick delle corse C1 e C2, attraverso `p6_bracci.tick_GU`)*: **`cs = s N(rho)`** *(`N = 1/(1 + rho/rho_c)`, `rho` la densita' della MATERIA per nodo)*, **dallo stato al CENTRO del palindromo, a punto fisso** *(`cs_al_centro`)*; **`mot.lambda_c = None`**: ### **CAMM-FASE-VUOTO e' SPENTA** *(niente fase in `cs'` sul vuoto)*; **la reazione** *(`Omega_k = s N' [...]`)* **tocca SOLO `psi`.**
- **Gli stati salvati da `controllo_senza_bordo.py`** portano **`cs_prec`** *(il `cs` del punto fisso dell'ultimo tick: `PS.LC.cs_prec()`)*: **il lapse VERO, non ricalcolato.**

### 1.2 LA DEFINIZIONE DEL GUARDIANO, CONTRO IL CODICE

- **La fase che un nodo da' al vuoto per tick e' `pi s_k = pi dtau_nodo_k / dtau_rif`**: **con `mot.dtau = 1`** *(da ASSERIRE nello script)* **e' `pi cs_k`**, e **sul vuoto `cs = s = 0.15`: `3 pi / 20` per tick** *(il numero del mandato: `omega = pi` per unita' di tempo)*. ### **QUINDI LA DEFINIZIONE E' GIUSTA, con `dtau_i` = `dtau_nodo` del codice** *(`mot.dtau * cs_i`)* **e `omega = pi / dtau_rif = pi`: nessun fattore da correggere.** **Lo script la scrive cosi':** `Theta_a = pi * somma_t (dtau_nodo_i(t) - dtau_nodo_j(t))`, `i = ii[a]`, `j = jj[a]`; **il segno e' una convenzione** *(conta `|Theta|`)*.
- ### **CIO' CHE NON SO, e che K2 decide:** **la fase RELATIVA delle due estremita' di un arco NON avanza solo per i pezzi di nodo**: **gli spostamenti e il Grover MESCOLANO le estremita'** *(la fase d'arco e' comune ai due capi, ma lo spostamento porta la fase di un nodo nell'altro)*. **Nel vuoto F3 la fase relativa resta `pi` per costruzione** *(le estremita' opposte)*: **se il mescolamento la tiene legata, l'avanzamento relativo NON e' `pi (cs_i - cs_j)` ma molto meno** *(la torsione si scarica)* -- **e allora la torsione del tempo proprio NON e' l'olonomia del vuoto** *(FERMO, come dice il mandato)*. **Non lo so: lo misura K2.**
- **E UNA COSA DA DIRE PRIMA** *(per K2)*: **oltre `30` nodi la materia e' quasi zero, quindi `cs_i - cs_j` e' piccolissimo** *(`N` dipende da `rho` della materia)*: **il rapporto puo' essere un quoziente di due numeri vicini allo zero.** **Lo script stampa ANCHE la scala** *(`max |pi (cs_i - cs_j)|` sugli archi usati)*; **se quella scala e' sotto l'arrotondamento della fase** *(`1e-12` rad per tick)*, **K2 e' NON LEGGIBILE e lo scrivo, invece di riportare un rapporto.** *(Non cambio la soglia dei `30` nodi: e' del mandato; stampo accanto, dichiarato, lo stesso conto per anelli piu' interni.)*

### 1.3 LE MISURE: COME

- **K1:** il vuoto F3 puro della scena di C2 *(`psi = 0`)*, `cs` dal punto fisso VERO *(`tick_lapse.cs_al_centro`)*: **`Theta` di un tick = `0` al bit su tutti gli archi** *(con `rho = 0`, `N = 1`, `cs = s` esatto: la prova che il punto fisso non introduce differenze)*. **Il caso che deve fallire:** lo stesso con `cs` perturbato di `1e-12` su un nodo: `Theta != 0`.
- **K3:** dallo stato `k 1500` di C2, `250` tick con la corsa senza bordo *(le righe di `controllo_senza_bordo.corsa_senza_bordo`, importate)*, `cs_prec` a ogni tick: **`Theta` accumulata tick per tick contro il trapezio fra `k 1500` e `k 1750`**; **e lo stato di arrivo contro `stato_01750.npz` di C2** *(la ripresa al bit: se non torna, l'accumulo non e' quello della corsa)*.
- **M1-M6:** `cs_prec` dagli stati ogni `250` tick *(`k 0`: `cs` del primo tick, dichiarato)*; il baricentro dal `meta["centro"]` della corsa; gli anelli dal punto medio dell'arco; radiale/tangenziale dall'angolo fra l'arco e il raggio *(radiale se entro `30` gradi dal raggio, tangenziale se oltre `60`: dichiarato ora)*.

## 2. LE PREVISIONI DEL GUARDIANO *(copiate PRIMA delle misure; anche nella carta della mitosi, sez. `14`)*

- **P-T1.** Il ritmo massimo sta fra `10` e `22` nodi dal baricentro: sul bordo della materia, DENTRO il confine dell'energia (`23.81`).
- **P-T2.** Il primo arco arriva a `2 pi` (o ci arriverebbe al ritmo misurato) fra `100` e `10000` tick.
- **P-T3.** Il ritmo e' stabile: all'anello del massimo, ultime `500` contro prime `500` entro il `10%`.
- **P-T4.** Oltre `40` nodi il ritmo e' sotto l'`1%` del massimo.
- **P-T5.** K2: il rapporto fra la fase vera e `omega * dtau` sta entro l'`1%` da `1`.
- ### **LE MIE, accanto:** **P-T1 VERA** *(il gradiente di `N(rho)` e' massimo dove `rho` scende piu' ripido: il bordo della materia, `10`-`15` nodi)*; **P-T2: NON so** *(`pi * 0.15 * |Delta N|`: con `Delta N ~ 1e-2` per arco al bordo, `2 pi` in circa `1300` tick -- dentro la forbice, ma il `Delta N` non l'ho letto)*; **P-T3 VERA** *(il mattone e' quasi stazionario: la massa entro `12.4` cambia poco in C2)*; **P-T4 VERA**; ### **P-T5: credo FALSA o NON LEGGIBILE** *(sez. `1.2`: il mescolamento tiene la fase relativa, e oltre `30` nodi la scala e' minuscola)*.

## 3. TODO DEL NEXT STEP

1. questa carta: commit, push *(dopo la chiusura di B2 sul ramo `mitosi`)*;
2. lo script `doc/referti_l2/torsione_tempo_proprio.py` *(K1, K3, K2, M1-M6 come sottocomandi)*: commit, push; K1 e K3 subito *(`3` processi coi due di C1 e C2)*: commit, push;
3. dopo la chiusura di C2 nel registro: K2, poi M1-M6; il referto `doc/referti_l2/torsione_tempo_proprio.txt` con la figura; commit, push;
4. la carta della mitosi, sez. `14`; D-R1-D-R3 SOSPESE annotate nella sez. `13`; **FERMO per Luca**;
5. **in coda dopo:** il referto di C1 e C2 *(mandato delle `15:22`)*, B3-B7 *(mandato delle `16:38`, la parte infrastruttura)*.

## 4. L'AGGIUNTA DI LUCA DELLE `18:48`: M3-bis *(scritta PRIMA delle misure)*

- **K3** *(`doc/referti_l2/torsione_tempo_proprio_K3.txt`, `191e5733`)*: **il trapezio fra stati ogni `250` tick sbaglia Theta del `96%` della scala** *(il ritmo di un tick NON rappresenta la media)*: ### **M3 sugli stati e' SOSTITUITA da M3-bis.** ### **L'ERRORE `n.189` DEL GUARDIANO:** **la stazionarieta' del lapse data per buona** *(il mandato delle `18:04` misurava Theta col trapezio sugli stati)*. **E la mia parte:** **nella carta (sez. `1.3`) ho scritto la misura sugli stati senza dubitarne; il dubbio l'ha alzato K3, che il mandato aveva messo apposta.**
- **M3-bis:** **i `12` segmenti di C2** *(`k 0-250`, ..., `2750-3000`)* **ripresi dagli stati salvati** *(la ripresa e' AL BIT: K3)*, **Theta accumulata TICK PER TICK in ciascuno, Theta totale = la somma.** **Il controllo:** **lo stato d'arrivo di ogni segmento = lo stato salvato successivo AL BIT** *(il segmento `0-250` parte dallo stato PREPARATO come la corsa)*. **Al piu' `5` processi, `1` filo; una voce del registro per ogni giro** *(`forza` col testo di Luca delle `18:48`)*. **C1 dopo C2, se i processi lo permettono; altrimenti dopo, dichiarato.**
- **CRESCE O OSCILLA** *(per gli archi del massimo)*: **Theta(t) tick per tick su tutta la corsa** *(il ritmo di ogni tick salvato per gli archi entro `45` nodi dal centro: dichiarato ORA)*; **gli archi del massimo = i `20` con `|Theta|` totale piu' grande** *(dichiarato ORA)*; **la retta dei minimi quadrati: la pendenza = il ritmo NETTO, con l'errore standard dai residui; la parte oscillante = l'ampiezza `rms` e massima attorno alla retta.**
- **Le previsioni si leggono cosi':** **P-T2 sul ritmo NETTO massimo** *(`2 pi / pendenza`)*; **P-T1 e P-T4 su `|Theta| / 3000`** *(il ritmo netto medio della corsa)*; **P-T3 sul ritmo netto dei primi due segmenti contro gli ultimi due, all'anello del massimo di `|Theta|`.** **M1, M2, M4, M5, M6 usano Theta di M3-bis, non il ritmo di un tick.**
- **Lo script:** **`doc/referti_l2/torsione_tempo_proprio_v2.py`, una versione NUOVA dichiarata** *(la v1 resta: k1, k3 e k2 vengono da li')*; **K2 resta quella della v1** *(50 tick da `k 3000`)*.
