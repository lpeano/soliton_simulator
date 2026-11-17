# LE MISURE DEL GUARDIANO NEL REPO, LE CONSIDERAZIONI, LA PROVA CP, LE DECISIONI DELLA MITOSI *(il mandato unico di Luca `2026-11-17` `11:33`)*

> **Il mandato:** **(A)** le misure del guardiano dalle mappe del triangolo, rifatte nel repo *(Q-A1)*, le fonti nel documento SOSPESO, le correzioni n.`183`, n.`184`, e le considerazioni del `2026-11-16` *(B4)* scritte da me sui numeri di A; **(B)** la prova CP *(e CPT)*; **(C)** le decisioni di Luca D-M1..D-M4 nell'albero e nella carta, il ramo `mitosi`, la carta delle regole aperte coi numeri di `divisione_vuoto.txt` rigirati; **FERMO** su D-M3 e su FC. **Nessun file del nucleo; nessuna corsa lunga; nessun merge.**

## 1. LE PREMESSE DAL CODICE *(cosa credo; cosa NON so)*

- **Le mappe** *(lette oggi)*: `doc/referti_l2/mattone/triangolo_t120_mappe.npz` *(i tick `0`-`2000` ogni `20`)*, `legati_t120_mappe_02000.npz` *(`2000`-`5960` ogni `60`)*, `legati_t120_mappe_06000.npz` *(`6000`-`12000` ogni `60`)*; chiavi `rho`, `dphi`, `E` per nodo *(float32)*, `centri` `(k, 3, 2)` **in coordinate di INDICE** `(m1, m2)`, `m1`, `m2`, `x`, `y`, `L`. **`dphi` per nodo** *(`csv/solitone/legati.py`, `misura`)*: `sqrt(somma sulle 6 estremita' di |phi_h - phi0|^2)`, `phi0 = c(t) phi_v`.
- ### **TRE COSE CHE NON TORNANO COL TESTO DEL MANDATO, scritte prima:**
  1. **«rispetto a k 3000» e «ogni 500 tick»:** **nelle mappe da `2000` i fotogrammi sono a `2000 + 60 j`**: **`3000`, `2500`, `3500`, ... NON ci sono.** **Prendo il fotogramma piu' VICINO e stampo il suo tick** *(`2960` o `3020`; `2480`/`2540` ...)*. **Il guardiano ha misurato sulle stesse mappe, quindi ha fatto per forza la stessa cosa o un'altra: non lo so.**
  2. **«una finestra di 11 nodi attorno al centro»:** **la leggo come i nodi entro `5.5` nodi di distanza dal centro** *(un disco di diametro `11`)*; **non so se il guardiano intendeva un quadrato `11 x 11` negli indici.** **Dichiarato; i numeri possono differire per questo.**
  3. **In 2D l'«inversione delle direzioni» `x -> -x`** *(parte B)* **e' una ROTAZIONE di `180` gradi, NON una parita'**: **la parita' in 2D e' uno SPECCHIO** *(che C2 dello specchio, `6faa1a3d`, ha gia' provato da solo)*. **Provo ENTRAMBE come P:** l'inversione attorno a un nodo **e** lo specchio di `specchio_carta.py`.
- **LA PROVA CP, dal codice** *(`csv/solitone/mattone.py`, `Campi.tick`; `doc/referti_l2/mattone/specchio_carta.py`, `mappa_nodi`, `mappa_archi`)*: **la mappa dei nodi per una matrice `M` del reticolo** *(lo specchio o `-I`)*, **le estremita' con l'arco rovesciato**, **`A` col segno del verso**; **lo spinore per una matrice `T`**.
- ### **CPT, E PERCHE' SI PROVA SENZA IL TICK INVERSO:** **un operatore ANTIUNITARIO `Theta` che rovescia il tempo soddisfa `Theta U Theta^-1 = U^-1`, cioe' `U(Theta(U(x))) = Theta(x)`**: **si prova con i soli tick in AVANTI** *(`tick^N(Theta(tick^N(x)))` contro `Theta(x)`)*. **Il tick e' un PALINDROMO** *(`composizione.ORDINE`, `7 + 7` pezzi)*: **se ogni pezzo e' rovesciato da `Theta`, lo e' il tick.** **NON so** se il bordo assorbente *(dissipativo)* e il punto fisso del lapse lo permettono: **il bordo e' lontano** *(il confronto entro `40` nodi)*. ### **E il diagnostico di C2 lo suggerisce:** **il coniugio da solo commuta coi pezzi `exp(-i tau H)` solo se H e' dispari; altrimenti li ROVESCIA** *(la lettura della carta del `09:49`, sez. `4`)*.
- **I SEGNI DI A ED E** *(scritti prima)*: **sotto C entrambi cambiano segno; sotto il rovesciamento del tempo `A` cambia segno ed `E` no** *(classicamente: B dispari, E pari)*. **Quindi i segni di `A` ed `E` si provano SEPARATI** *(`4` combinazioni)*, non legati come in C2.
- **`divisione_vuoto.txt`** *(C3)*: **porta il timbro «`_divisione_vuoto.py` MODIFICATO rispetto a HEAD»** *(il blob dei byte `aa0384b6`, il blob git di HEAD di allora `4ffe9808`)*: **«dal suo commit» = il commit che ha committato il referto**; **lo cerco con `git log`** e **lo rigiro dai byte di quel commit** *(`git cat-file`, par. `7`)*; **se il sorgente di quel commit non da' gli stessi numeri, lo scrivo.**

## 2. PROGETTAZIONE DEL RAGIONAMENTO

### 2.1 A -- le misure *(lo script `doc/referti_l2/triangolo_t120_misure_guardiano.py`, sola lettura delle mappe)*

- **Il baricentro** = la media dei tre centri a `k 0` *(il fotogramma `0`)*, **fisso** per tutti i fotogrammi; `theta = atan2(y, x)` dello scarto `toro.scarti` dal baricentro.
- **A1:** la m=3 di `rho` negli anelli `12-17`, `17-22`, `22-27`, `27-32`: **la rotazione = `-unwrap(arg S)/3`** *(`S = somma rho e^{-3 i theta}`)*, **rispetto al fotogramma piu' vicino a `k 3000`**, ogni fotogramma fra `2500` e `6000`; **l'ampiezza `|S| / somma rho`.** **Il caso noto prima** *(Q-A4)*: **una densita' `cos(3 (theta - alpha))` ruotata di `alpha` = `+10` gradi da' `+10`** *(lo stesso controllo di `segni_vortice.py`, punto 3)*.
- **A2:** le culle *(la definizione del mandato)*; **la distanza culla-centro, lo sfasamento in angolo attorno al baricentro, il raggio medio dei centri e delle culle; e la PENDENZA dello sfasamento nel tempo** *(«senza accumularsi»: la pendenza in gradi per `1000` tick)*.
- **A3:** la m=3 di `dphi` negli anelli `30-45` e `12-28`, ampiezza e orientamento, ai fotogrammi piu' vicini ai multipli di `500`.
- **A4:** la m=6 di `rho` nell'anello `12-32`, accanto alla m=3, agli stessi fotogrammi.
- **A5:** l'orientamento del triangolo dei centri *(`-unwrap(arg somma_j e^{-3 i theta_j})/3`, attorno al loro baricentro)* **e i centri fotogramma per fotogramma fra `9000` e `9500`** *(il salto `9120`-`9360`)*.
- **GLI ATTESI DEL GUARDIANO** *(scritti nel mandato, qui copiati PRIMA dei numeri)*: A1 `27-32` sempre avanti di `+1`/`+2` gradi, `17-22` e `22-27` indietro fino a circa `-23` e `-5` a `k 5000`; A2 `0.1`-`2` nodi, `+-5` gradi, senza accumularsi; A3 il guscio da circa `0.44` a `0.21`, l'orientamento circa fermo.
- **Cosa mi FERMEREBBE:** il caso noto che non passa.

### 2.2 B -- la prova CP e CPT *(lo script `doc/referti_l2/simmetria_CP.py`)*

- **I candidati** *(quanti e quali, PRIMA)*: **la mappa spaziale `P`** in `{l'inversione attorno a un nodo (M = -I), lo specchio a 30 gradi (M di specchio_carta.py)}`; **lo spinore `T`** in `{I, sigma_x, sigma_y, sigma_z}` per l'inversione, e in `{I, sigma_x, sigma_y, sigma_z, sigma.l, sigma.l_perp}` per lo specchio; **sempre il coniugio**; **`phi`** in `{phi, -phi, conj, -conj}`; **i segni `(sA, sE)`** in `{+1, -1}^2`. **In tutto `(4 + 6) x 4 x 4 = 160` candidati.** **Il centro della mappa:** il nodo piu' vicino al baricentro della materia del mattone.
- **CP:** `Theta(tick(x))` contro `tick(Theta(x))`. **CPT:** `tick(Theta(tick(x)))` contro `Theta(x)` *(gli stessi `160` operatori antiunitari)*. **E, per completezza, il «T» senza mappa spaziale** *(`P = identita'`, `4 x 4 x 4 = 64` candidati: il coniugio come rovesciamento del tempo, la lettura del diagnostico)*.
- **Q-A4 prima:** **ogni operatore due volte = l'identita'** *(a meno della fase globale di `sigma_y`)*; **un pacchetto con un gradiente di fase verso `+x`**: **sotto P la corrente di fase `J_x` cambia segno; sotto C anche; sotto CP NON cambia** *(il caso che deve fallire: `J_x` sotto CP che cambia segno)*; **il controllo positivo: l'identita' (senza coniugio, senza mappa) da' `0`.**
- **La prova:** dal mattone `L162_MGU_03000` e da uno stato a caso *(come C2)*; **`1` tick per tutti; `10` tick per i due migliori di ogni famiglia** *(CP: `tick^10` contro; CPT: `tick^10 Theta tick^10` contro `Theta`)*; entro `40` nodi e sul toro.
- ### **LA PREVISIONE DEL GUARDIANO** *(scritta prima)*: **CP commuta col tick sotto `1e-12` dopo `10` tick entro `40` nodi.** **Se cade: CPT; se cade anche quella: chi rompe** *(pezzo per pezzo, come `7782ef70`)*. ### **LA MIA, accanto:** **dal diagnostico di C2** *(Grover e lo spostamento rompono C: il coniugio li ROVESCIA)*, **mi aspetto che CP CADA** *(P e' unitaria: non cambia il verso del tempo che il coniugio ha rovesciato)* **e che la famiglia che puo' passare sia quella che ROVESCIA il tick** *(CPT, o il «T» senza mappa)* -- **ma i pezzi NON LINEARI** *(`CAMM-MATERIA-VUOTO`, `fase_a`, la reazione: fasi pari in `rho`)* **sono rovesciati dal coniugio solo se il tick li applica come `exp(-i tau N)` con `N` reale: non lo so per la reazione** *(il punto medio implicito)*.
- **FC** *(B5)*: **PRESA** come «la coesione e' G+U, simmetrica per CP» se CP passa; «per CPT» se passa solo quella *(scritto)*; **se nessuna, aperta e FERMO.**

### 2.3 C -- le decisioni e il ramo

- **D-M1..D-M4 nelle note di D7 e D9 e nella carta della mitosi** *(nessun `presa` cambiato: D7 dipende ancora da FC)*.
- **Il ramo `mitosi`** da `primo-ordine`: **un WORKTREE su C:** *(`C:/Users/lpeano/wt_mitosi`, come `wt_zero`)*, **creato e pushato vuoto**; **nessun file del nucleo cambiato in questo mandato.**
- **C3:** `divisione_vuoto.txt` rigirato dal suo commit; la carta delle regole aperte *(una sezione nuova della carta della mitosi)*; **la proposta per D-M3 coi numeri; FERMO.**

## 3. TODO DEL NEXT STEP

1. questa carta; commit;
2. A: lo script *(commit)*, la corsa, il referto, il SOSPESO, n.`183`/`184`, le considerazioni *(commit)*;
3. B: lo script *(commit)*, la corsa *(una «breve»)*, il referto, FC *(commit)*;
4. C: l'albero e la carta; il ramo; `divisione_vuoto` rigirato; la carta delle regole aperte *(commit)*;
5. **FERMO** su D-M3 e FC.
