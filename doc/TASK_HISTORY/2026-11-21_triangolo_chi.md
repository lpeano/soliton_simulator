# IL PIANO DEL TRIANGOLO: LE TRE SFASATE SUL VUOTO CON `chi` E LA MITOSI *(il mandato di Luca `2026-11-21` `23:23`; il ramo `lapse-u`)* [[PROGETTO-MITOSI]]

## 0. IL MANDATO *(in breve; il testo intero nel messaggio di Luca, copiato nella relazione del ramo principale)*

- **Luca:** la mitosi sull'oggetto preferito, **le «tre sfasate sul vuoto»** *(tre solitoni sfasati di `120` gradi, la materia che circola)*, **con `chi`**; **il controllo e' il gemello RUOTATO** *(t120r, `+15` gradi, del `15/11`)*, perche' l'impronta del reticolo non sia scambiata per fisica *(nel ramo MITOSI le `9` nascite sono cadute su due assi del reticolo)*. **Il tronco** *(`chi` e `Theta` fino al primo scatto)* non usa la regola: **puo' partire prima delle cure**; **i rami con le nascite** dipendono dalle cure *(O1, O2, O8)* e da un NUOVO via di Luca. Il triangolo «in fase» viene dopo *(dichiarato)*.
- **Luca:** opzione (a): i due tronchi ai primi posti liberi, mai oltre `5` processi *(attese comprese)*, nessuna corsa fermata; **niente bordo sorbente.** **Del guardiano:** i parametri di `chi` come nel mattone *(`kappa` il NUMERO, D3; `c2 0.25`, `m2 1e-4`; `c0 = kappa m0`, `m0` dallo stato di partenza del triangolo)*; gli stati ogni `250`; il tronco esce al primo scatto con lo stato PRIMA della regola.
- **Il mandato delle `23:30`** *(successivo)*: **i tronchi del triangolo usano `chi_tick_v2`** *(l'inerzia `f`)* **e partono solo dopo V1-V5.**
- **TODO:** P0 *(la compatibilita')*, P1 *(questa carta)*, P2 *(la prova breve per scena)*, P3 *(i tronchi in coda)*, P4 *(le misure in corsa a `k 3000` e ogni `5000`)*.
- **PREVISIONI DEL GUARDIANO:** **P-T1** *(nessuno dei `20` archi piu' maturi nella regione centrale, `80%`)*; **P-T2** *(i primi archi a maturare nei gusci esterni dei tre solitoni, non nei corridoi, `60%`)*; **P-T3** *(nel t120 i `20` piu' maturi entro `10` gradi da un asse; nel t120r ruotano col triangolo di `+15` entro `5` -- se fisica -- invece di restare sugli assi -- se impronta; `55%` che seguano il triangolo)*; **P-T4** *(la circolazione della materia c'e' ancora con `chi` a `k 3000`, lo stesso segno del `15/11`, `75%`)*; **P-T5** *(il primo scatto prima che nel mattone `chi`, `50%`, debole)*.
- **FERMO** dopo P3 e il primo giro di P4; i tronchi continuano.

## 1. LA SCENA E I PARAMETRI *(dal codice; i valori dalla sonda P0)*

- **La scena** *(`triangolo_chi.prepara`: le righe di `mattone_triangolo.corsa` al tick `0`, coi ganci di `triangolo_120` e `triangolo_ruotato`)*: la scena di S162 *(il toro di lato `162`)*, il vuoto fresco, **tre francobolli del mattone di `L 162`** *(`L162_MGU_03000`)* ai vertici equilateri di lato `39` *(t120)* o ruotati di `+15` gradi *(t120r: solo le posizioni)*, `psi_h` per `exp(i 0, 120, 240 gradi)`, la materia per SOMMA, il vuoto per PRODOTTO; **il campo `porto.campi`** *(`A = 0`, `E` da Gauss; `s_a = s`)*; **`g_e = 0`** *(Luca: niente bordo sorbente; il `15/11` aveva il bordo da `R_A 60`: dichiarato, e' una decisione di Luca, non un cambio mio)*.
- **`chi`:** `chi_tick_v2` *(`f`, `kappa` il NUMERO)*; `m0` = la media di `u = s Q - e0 rho` sullo stato di partenza del triangolo; `chi` al profilo statico, `pi = 0`, `Theta = 0`.
- **Il tronco:** dopo ogni tick lo scatto *(`|theta_a| >= 2 pi`)*: lo stato prima della regola, `scatto.json`, l'uscita `10`; gli stati ogni `250` *(per il film leggero e le misure)*; le tappe ogni ora; il limite `k 200000`.
- **Il costo** *(Q-P1)*: il tick con `chi` sulla scena del triangolo misurato su `50` tick *(`triangolo_chi.py costo`)*: **il numero nella sez. `3`.**

## 2. LE MISURE IN CORSA *(P4; le definizioni fissate PRIMA dei numeri)*

- **Quando:** a `k 3000` e poi ogni `5000`, sola lettura sugli stati salvati, al piu' `1` processo breve.
- **(a) la mappa del ritmo:** `|d Theta / dt|` per arco = `|Theta(k2) - Theta(k1)| / (k2 - k1)` fra due stati consecutivi *(`250` tick)*; **i `20` archi con `|Theta|` piu' alto**, ciascuno **classificato** dal punto medio dell'arco nel disegno *(misura, A17)*, coi centri della materia dei tre solitoni *(i baricentri di `rho` nei tre settori di `120` gradi attorno al baricentro del triangolo)*: **regione centrale** = entro l'INRAGGIO del triangolo *(`lato / (2 sqrt 3)`)* dal baricentro; **corridoio** = fuori dalla centrale, entro `6` archi dal SEGMENTO fra due centri, con la proiezione dentro il segmento; **guscio esterno** = il resto entro `25` archi da un centro; **altrove** = il resto. **L'angolo** dal baricentro del triangolo e **la distanza dall'asse del reticolo piu' vicino** *(il metodo di M3)*.
- **(b) la proiezione del primo scatto** *(il METODO, scritto prima del numero)*: da due stati a distanza `D` *(`250` e `2500` tick)*: per arco la velocita' lineare di `|Theta|`, il tick in cui arriva a `2 pi`; **il minimo** sugli archi; **l'incertezza** = la differenza fra le proiezioni con `D = 250` e `D = 2500`.
- **(c) la circolazione della materia:** le misure del `15/11` *(`triangoli_magnetico`, `girandola`)*, sugli stati salvati: **c'e' ancora con `chi`, e col segno di allora?**
- **IL CASO NOTO di (a)** *(DEVE, prima)*: sul mattone con `chi` a parita' di `k` *(lo stato della corsa del mattone, la fisica vecchia: il metodo e' lo stesso)*, la stessa misura ridà i `20` archi piu' maturi **nel guscio** *(`r` fra `17` e `20` dal centro)*.
- **Il referto** `doc/referti_l2/triangolo_chi_misure.txt`, aggiornato a ogni giro.

## 3. I NUMERI DI P0 E P1 *(dopo le misure: la sez. si aggiunge coi referti)*

- **P0** *(triangolo_chi_v2.py compat, a980c640; doc/referti_l2/triangolo_chi_v2_compat.txt)*: le due scene sono compatibili. **t120:** i vertici `[74, 68]`, `[113, 68]`, `[113, 107]`, i lati `39.0000`; `m0` `+1.412935154856e+01`, `c0` `+3.5732340997e-03`. **t120r:** i vertici `[74, 62]`, `[119, 74]`, `[107, 107]`, **i lati `40.3609`** *(non `39`: i vertici ruotati cadono sui nodi del reticolo; la costruzione e' quella del `15/11`, `triangolo_ruotato`, non mia; DICHIARATO: il gemello e' un triangolo piu' grande del `3.5%`)*; `m0` `+1.422893814310e+01`, `c0` `+3.5984189934e-03`. In tutte e due: il vuoto senza materia prima dell'incollatura, le tre masse dei francobolli uguali, `s_a` uniforme `0.15`, `g_e = 0`.
- **P1, il costo** *(triangolo_chi_v2.py costo; doc/referti_l2/triangolo_chi_v2_costo.txt)*: 50 tick col passo v2: **t120 `0.854` s per tick, t120r `0.740`**; la prima misura del t120 *(triangolo_chi.py, 178b033b)* dava `0.615`: **lo stesso conto, un carico della macchina diverso** *(5 processi)*; la stima per `k 20000`: fra `3.4` e `4.7` ore per scena.

## 4. IL GEMELLO RUOTATO ESATTO t120r28 *(la decisione di Luca delle `02:22` e la correzione delle `02:31`, l'errore n.210 del guardiano; scritta PRIMA del codice)*

### 4.0 LA DECISIONE *(copiata)*

- **Il t120r di `+15` gradi ha i lati `40.36`** *(44df0996)*: differisce dal t120 per orientamento E distanza; **come controllo dell'impronta del reticolo non va bene. Resta nel repo, dichiarato.**
- **Il gemello nuovo t120r28:** un triangolo equilatero di lato ESATTAMENTE `39` sui nodi del reticolo, ruotato di `27.8` gradi. **Nelle coordinate `(m1, m2)` del codice** *(la base a `120` gradi, la norma `a^2 - ab + b^2`; la correzione delle `02:31`)*: `V1 = V0 + (45, 21)`, `V2 = V0 + (24, 45)`, `V0` il vertice di partenza del t120; poi la traslazione che porta il baricentro su quello del t120 *(al nodo piu' vicino, dichiarato)*. Le fasi `0, 120, 240` come il t120, nello stesso verso di giro.
- **Prima del lancio:** la compatibilita' e il costo, **i tre lati stampati con la norma del codice, tutti `39.0000`**; **DEVE FALLIRE: coi vettori sbagliati `(24, 21)` e `(-21, 45)` i lati non sono `39`**; la prova breve al bit [M2357-T2]. **Il lanciatore dei tronchi usa t120 e t120r28.**

### 4.1 LE PREMESSE DAL CODICE *(prima dei numeri)*

- **La base:** `_solitoni_triangoli.A1 = (1, 0)`, `A2 = (-1/2, sqrt 3 / 2)`; `|m1 A1 + m2 A2|^2 = m1^2 - m1 m2 + m2^2`. `mattone.distanza` usa questa norma *(con l'immagine piu' vicina sul toro)*. **Il t120:** `[74, 68]`, `[113, 68]`, `[113, 107]` *(i lati `(39, 0)`, `(0, 39)`, `(39, 39)`, tutti `1521` in questa norma)*.
- **I nodi BUONI:** `triangolo_120.vertici` sceglie il vertice fra i nodi con `(n - centro del francobollo) % 3 == 0` *(il francobollo si incolla solo li')*. **`(45, 21)` e `(24, 45)` sono multipli di `3`**: i vertici nuovi sono buoni se `V0` lo e' *(il t120 lo e')* e **se la traslazione del baricentro e' un multiplo di `3` in tutte e due le coordinate**. Se non lo e': **FERMO** *(non scelgo io un altro nodo)*.
- **A mano, prima dello script** *(il numero vero lo stampa lo script)*: il baricentro dei vertici `(74, 68)`, `(119, 89)`, `(98, 113)` e' `(97, 90)`, quello del t120 `(100, 81)`: la traslazione `(3, -9)`, **multipla di `3`, ed esatta** *(nessun arrotondamento)*: i vertici `(77, 59)`, `(122, 80)`, `(101, 104)`. **Il verso di giro:** il prodotto vettoriale cartesiano di `(V1 - V0, V2 - V0)` positivo come nel t120 *(antiorario)*; **l'angolo** di `V1 - V0` dall'asse `A1` circa `27.8` gradi, `32.2` dall'asse a `60`.
- ### ⚠ **IL CASO CHE DEVE FALLIRE, A MANO, NON DA' I NUMERI DELLA CORREZIONE:** con la norma del codice `(24, 21)` da' `513` *(il lato `22.65`)* e `(-21, 45)` da' `3411` *(`58.40`)*, non `21.6` e `52.0`. **Il criterio resta quello della correzione** *(i lati coi vettori sbagliati NON sono `39`)*; **lo scarto dei numeri lo dico a Luca**, e lo stampa lo script.

### 4.2 IL CODICE *(`doc/referti_l2/triangolo_chi_v3.py`, nuovo)*

- **La v2 riga per riga, salvo:** le scene `t120` e `t120r28` *(il t120r di `+15` resta nella v2, non qui)*; **`--quale` scelto** per `compat`, `costo`, `prova` *(il t120 e' gia' passato con la v2, 50845283: si rifa' solo il t120r28)*; in `compat` per il t120r28 **i lati, il baricentro, la traslazione, il verso, l'angolo, e il caso coi vettori sbagliati**.
- **Il lanciatore dei tronchi:** un `triangolo_lancia_v3.sh` nuovo, coi tronchi t120 e t120r28; il vecchio non si usa.
