# 2026-11-07 — OGNI CORSA SALVA SEMPRE LO STATO COMPLETO *(Luca `2026-11-07` `16:01`; I1, I3, I4)*

**Il mandato** *(nella sostanza)*: **e' l'INFRASTRUTTURA delle corse, non il codice di ogni corsa, a salvare SEMPRE lo stato completo a intervalli regolari** *(«completo» = tutto cio' che serve a ripartire AL BIT, anche con le grandezze future: per esempio `A` ed `E` del campo `U(1)`, che vivono in `Campo`, FUORI da `z["st"]`)*. **R1** *(il salvataggio non tocca la corsa)*, **R2** *(salva, riparti, confronta al bit; il DEVE FALLIRE con una grandezza tolta)*, **R3** *(la registrazione)*, **R4** *(il formato)*. **Nucleo intatto; il codice in `csv/`.** **I1 e I3 PRIMA di T1-T5, sequenziali.**

## 1. LE PREMESSE DAL CODICE *(cosa credo prima di guardare, e cosa NON so)*

1. ### **CIO' CHE C'E' GIA'** *(`csv/solitone/corsa_accensione.py`)*: **(i) il file di RIPRESA** `db/accensione_lenta/<nome>.npz` *(tutte le chiavi di `z["st"]`, scritto a fine pezzo)*, **(ii) gli STATI COMPLETI ai tempi di `STATI[nome]`** *(`TM1000`: `2000, 6000, 10000`; `DG1000`: `20000 .. 40000`; `TM3`, `TM3C`; `TBS` e le coppie: ogni `1500`)* **su `E:` col loro `sha` per chiave nel jsonl**, **(iii) `dopo_stato`** *(gli `sha` dopo `100` tick da ogni stato: la prova di ripartenza della corsa, `ripartenza()`)*. ### **Quindi R2 per `z["st"]` esiste gia', per le corse con `STATI`.**
2. ### ⚠ **LO STATO CHE NON STA IN `z["st"]`, OGGI** *(cio' che una ripartenza da `z["st"]` da solo PERDEREBBE)*: **(a) gli ACCUMULATORI DEL BORDO** *(`bor`: `M_ass`, `V_ass`, `E_ass`, `c0`, `X`; la corsa li riprende dalla riga jsonl del pezzo prima, `prec["bordo"]`)*; **(b) `acc`** *(lo stato dell'accensione: `_acc.npz` con `psi` e `mu`)*; **(c) `giro`** *(`DG1000`)* **e `pst`** *(la partenza del moto)*; **(d) il campo `U(1)`** *(`Campo.A`, `Campo.E`: nel prototipo, in memoria)*; **(e) le TABELLE** *(`fase_F3.npz`: COSTANTI, il loro `sha` nella riga)*; **(f) `mot.cs`, `mot.lambda_c`** *(oggi costanti; con `cs` dinamico diventano STATO)*. ### **(a)-(c) la corsa li porta nel jsonl e nei suoi `.npz`: la ripresa al bit funziona OGGI perche' la corsa li conosce uno per uno** -- **e' esattamente cio' che Luca vuole togliere al «codice di ogni corsa».**
3. **Le tabelle costanti** *(e)* **non sono stato:** **si registrano col loro `sha`** *(un controllo, non un salvataggio)*.
4. **Che cosa NON so:** **se ogni pezzo di stato e' un array** *(gli accumulatori del bordo sono `float`: si salvano come array di dimensione `0`)*; **se il registro si puo' rendere OBBLIGATORIO** *(una grandezza non registrata fa fallire R2 -- si', per costruzione: R2 confronta TUTTE le chiavi di `z["st"]` e di ogni oggetto registrato contro la corsa mai interrotta)*.

## 2. PROGETTAZIONE *(le letture e i DEVE fissati PRIMA)*

- ### **IL REGISTRO** *(`csv/solitone/stato_completo.py`, nuovo)*: **`registra(nome, prendi, metti)`**: **`prendi()` -> `{chiave: array}`, `metti({chiave: array})`**; **registrati per costruzione: `z["st"]` *(ogni chiave)*, il bordo *(gli accumulatori)*, `acc`, `giro`, `pst`**; **il campo `U(1)` si registra da `_u1_oggi`** *(I4)*; **le tabelle col loro `sha`** *(un controllo all'apertura)*.
- **IL FORMATO** *(R4)*: **un `.npz` per stato**: **le chiavi `<nome>/<chiave>`**, **e `meta`** *(json: la corsa, il tick, `t`, il commit, l'impronta del palindromo, lo `sha` di ogni chiave, l'elenco dei registrati)*; **su `E:\soliton_simulator\stati\<corsa>\`**; **nel repo l'indice** *(percorso, dimensione, `sha1`)*.
- ### **L'INTERVALLO** *(la proposta di Luca, da motivare)*: **ogni `1000` unita' di tempo** *(`~6667` tick a `s 0.15`)*: **il motivo: la ripresa dopo il riavvio notturno perde al piu' un intervallo** *(`~1.5` ore su `L 162`, `~11` minuti su `L 81`)*, **e il costo di spazio** *(uno stato `L 162` `~9` MB, `L 81` `~2.3` MB: `30` stati a `30000`, `~270` MB e `~70` MB)*. ### ⚠ **Gli `STATI` di oggi** *(ogni `1500` per le coppie)* **NON coincidono con `1000`**: **si tengono tutti e due** *(gli `STATI` sono i tempi delle misure, l'intervallo regolare e' la sicurezza)*.
- **R1:** **la stessa corsa corta** *(`L 81`, `200` tick dopo la rampa, col bordo)* **con e senza salvataggio: gli `sha` di ogni chiave AL BIT.** **R2:** **salvato a `t1`, ripartito dal file, a `t1 + N` contro la corsa mai interrotta: ogni chiave AL BIT**; **R2-F** *(DEVE FALLIRE)*: **un salvataggio senza `phi_h`** *(la fase del vuoto)* **e uno senza gli accumulatori del bordo** *(la ripartenza con `M_ass` da zero: `M + M_ass` non torna)*. **R3:** **il file elenca i registrati e i loro `sha`; una grandezza non registrata fa fallire R2** *(voluto)*.
- ### **ATTIVO DI DEFAULT sulle corse NUOVE** *(un flag nella corsa, acceso)*: ### ⚠ **e' un cambio di `corsa_accensione.py`**: **le corse vecchie al bit** *(il salvataggio e' sola lettura dello stato: R1)*; **le corse gia' fatte non si toccano.** **`D6`, la cassetta.**
- **I3, L'INVENTARIO DEGLI STATI GIA' ESISTENTI** *(dal disco, letto oggi)*: **`E:\soliton_simulator\stati\`: `C35-0`, `C35-pi`, `D0R`, `S162`, `TBS`, `TM1000`** *(`TM1000`: i tick `13333`, `40000`, `66667`, cioe' `t 2000, 6000, 10000`)*; **`E:\soliton_simulator\due_giri\stati\`** *(`DG1000`)*; **i file di ripresa di fine corsa in `db/accensione_lenta/`: `TA1000`, `TA2000`, `TB3`, `TBS`, `TF3`, `TF3C`, `TFI`, `TM1000`, `TP1000`, `TS`, `D0R`, `DG1000`, `S162`, `C35-0`, `C35-pi`**; ### **`TM3` NON ha stati su `E:`** *(non c'e' la cartella)*. **La tabella** *(la corsa, `t`, il bordo si'/no, il vuoto, lo `sha` verificato contro il jsonl)* **nell'indice della libreria**, **con uno script di sola lettura.**

## 3. TODO

1. **Questo task history, un commit.**
2. **`stato_completo.py` e i test R1, R2, R2-F, R3** *(committati prima di girarli; la corsa corta)*; **poi il flag nella corsa, `D6`, la cassetta.**
3. **I3: lo script dell'inventario, il referto.**
4. **I4: `Campo` registrato in `_u1_oggi`; la prova R2 col campo dentro T3.**

## 4. IL CONFLITTO CON GLI ALLUNGAMENTI *(`2026-11-08` `03:25`)*: **IL FLAG DI I1 STA IN UN FILE CHE OGGI NON SI TOCCA -- FERMO SU I1, LA DECISIONE E' DI LUCA**

- ### **Il passo `2` di I1 e' «il flag nella corsa»: un cambio di `csv/solitone/corsa_accensione.py`.** **Quel file e' fra i `61` del percorso della corsa** *(`doc/referti_l2/ripresa_C35-0.txt`)*, **e il par. `5` dice: durante un run nessun file del percorso si modifica.** **Gli allungamenti** *(Luca `00:52`: `C35-0`, `C35-pi`, `S162`, `C50-0` in sequenza, uno dopo l'altro)* **lo tengono fermo per `~3` giorni** *(`C35-0` fino alle `17`-`24` di oggi; poi le altre tre)*.
- **Le strade** *(la scelta e' di Luca)*: **(i1) I1 aspetta la fine degli allungamenti** *(e T1-T5, che Luca vuole DOPO I1, aspettano con lui)*; **(i2) `stato_completo.py` e i suoi test R1, R2, R2-F, R3 si fanno ORA, su una corsa corta che chiama il ciclo del tick direttamente** *(nessun cambio di `corsa_accensione.py`)*, **e solo il flag nella corsa aspetta la fine degli allungamenti**; **(i3) gli allungamenti si fermano fra due corse** *(per esempio dopo `C35-0`)* **per il commit del flag, e ripartono** *(con `R-1` rifatto per la corsa successiva)*. ### **La mia proposta: (i2)** *(il registro si prova subito; nessun file del percorso cambia)*.
- **I3** *(l'inventario degli stati gia' esistenti, sola lettura)* **non dipende da questo.**

## 5. LE DECISIONI DI LUCA DEL `2026-11-08` `03:47` *(chiude il FERMO di `baf31869`)*: **I1 CON (i2) -- IL PROGETTO, PRIMA DEL CODICE**

**Le decisioni:** **(i2)**: **`stato_completo.py` e R1, R2, R2-F, R3 ORA, su una corsa corta che chiama il ciclo del tick direttamente; `corsa_accensione.py` NON si tocca finche' girano gli allungamenti; il flag nella corsa alla fine** *(o fra due corse, se Luca lo chiede)*, **con `R-1` rifatto.** **T1-T5 non aspettano il flag: girano col registro provato; nelle prove col campo `U`, `Campo` si registra (I4).** **I3 se non e' fatto** *(non e' fatto)*.

### 5.1 LE PREMESSE *(dal codice, in aggiunta alla sez. `1`)*

1. **La corsa corta:** **la scena di `TBS`** *(`L 81`, il bordo di `TB3`, il vuoto `c(t) F3`)* **dallo stato completo della libreria `TBS_100000_completo.npz`** *(validato al bit)*, **il ciclo della corsa scritto come in `bilancio_b1`** *(`AC.tick`, poi `BO.assorbi` con `c(t) F3`)* ### **E gli ACCUMULATORI del bordo aggiornati come li aggiorna la corsa** *(`M_ass += dM`, `V_ass += dV`, `E_ass += e_prima - e_dopo` col libro dei conti)*: **sono lo stato che `z["st"]` NON contiene** *(la premessa `2 (a)`)*, **e su cui R2-F (b) deve fallire.**
2. **`N = 100` tick, il salvataggio a meta'** *(dopo `50`)*: **una scelta di protocollo mia, dichiarata** *(`100` = `DOPO_STATO`)*.
3. **Che cosa NON so:** **se `np.savez` di un `float` come array di dimensione `0` lo rida' AL BIT** *(si': `float64` -> `float64`; lo verifica R2)*.

### 5.2 PROGETTAZIONE *(i DEVE, prima dei numeri)*

- ### **`stato_completo.py`, IL REGISTRO** *(R3, R4)*: **`Registro()`**; **`registra(nome, prendi, metti)`** *(`prendi() -> {chiave: array}`, `metti({chiave: array})`; un nome due volte ALZA)*; **`tabella(nome, array)`** *(una costante: solo lo `sha`, controllato al caricamento)*; **`salva(file, meta)`** *(un `.npz`: le chiavi `<nome>/<chiave>` e `meta`, un json con la corsa, il tick, `t`, il commit, l'elenco dei registrati, lo `sha1` di ogni chiave e delle tabelle; scritto in un `tmp` e poi `os.replace`)*; ### **`carica(file)`** *(ALZA se i registrati del file e quelli del registro NON coincidono -- una grandezza registrata ma non salvata, o salvata ma non registrata --, se uno `sha` non torna, se una tabella e' cambiata)*. **Due aiuti:** **`di_z(z)`** *(ogni chiave array di `z["st"]`)* **e `di_dict(d, chiavi)`** *(gli accumulatori: `float` come array di dimensione `0`, liste come array, rimessi col loro tipo)*.
- **I DEVE** *(`csv/solitone/test_stato_completo.py`, la corsa corta)*:
  - **`R1`** *(DEVE PASSARE)*: **`100` tick senza salvataggio e `100` con il salvataggio a `50`: gli `sha` di ogni chiave di `z["st"]` E gli accumulatori del bordo AL BIT** *(il salvataggio e' sola lettura)*;
  - ### **`R2`** *(DEVE PASSARE)*: **lo stato e gli accumulatori SPORCATI** *(`z["st"]` a zero, gli accumulatori a zero)*, **poi `carica` dal file a `50`, poi `50` tick: ogni chiave e ogni accumulatore = la corsa mai interrotta, AL BIT**;
  - **`R2-F`** *(DEVE FALLIRE, due volte)*: **(a) un registro SENZA `phi_h`** *(la fase del vuoto)*: **la ripartenza non torna al bit**; **(b) un registro SENZA gli accumulatori del bordo**: ### **`M + M_ass` a `100` non torna** *(`M_ass` riparte da zero)*;
  - **`R3`** *(DEVE PASSARE)*: **il file elenca i registrati e i loro `sha`**; ### **`carica` in un registro con una grandezza in PIU' ALZA, e con una in MENO ALZA** *(una grandezza non registrata non passa in silenzio)*; **una tabella cambiata ALZA.**
- **I3, L'INVENTARIO** *(`csv/solitone/inventario_stati.py`, sola lettura)*: **per ogni corsa con stati su `E:` e per ogni file di ripresa in `db/accensione_lenta/`: il tick, `t`, il bordo si'/no, il vuoto, e lo `sha` di ogni chiave CONTRO quello registrato nel jsonl** *(per gli stati: `stati[].sha`; per la ripresa: `sha_fine` dell'ultima riga)*. ### ⚠ **Le corse IN VOLO** *(`C35-0`: il file di ripresa si riscrive a ogni pezzo)* **si leggono come sono, e si dice che sono in volo.** **Il DEVE `I3-F`** *(DEVE FALLIRE)*: **uno stato confrontato con lo `sha` di un altro tick.**
- **Che cosa mi fa FERMARE:** **R1 o R2 che falliscono; R2-F o `I3-F` che passano.**

### 5.3 TODO

1. **Questa sezione: commit e push.**
2. **`stato_completo.py`, `test_stato_completo.py`:** l'INVENTARIO; commit; `D6`, la cassetta *(il test dentro la cassetta? NO: la cassetta gira i test dei moduli di oggi; il test nuovo si gira a se', dichiarato)*; commit.
3. `python csv/solitone/test_stato_completo.py > doc/referti_l2/stato_completo.txt`; il referto, la relazione; commit.
4. **I3:** lo script, il referto; commit.
