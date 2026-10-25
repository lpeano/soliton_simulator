# IL PROGETTO DELLA MITOSI NELL'ERA 2 *(sulla carta: nessun codice, nessuna decisione)*

> **Il mandato:** di Luca, `2026-10-25`, `17:53` *([[PROGETTO-MITOSI]], [[D-BILANCIO-NASCITA]], `DOMANDA-MITOSI-LE-FORME`, [[PROGETTO-CURVATURA]], [[PROGETTO-U1]])*; ### **il task history `doc/TASK_HISTORY/2026-10-25_progetto_mitosi.md`** *(`3758d51b`)*.
> ### ⭐ **L'ORIENTAMENTO DI LUCA sul bilancio, da sviluppare per PRIMO** *(NON una legge decisa)*: ### **«l'energia della nascita di un nodo va scambiata col vuoto».**
> ### **Le citazioni del codice sono di `soliton_simulator.py` al blob `b8c21049`** *(sha1-BYTE)*, ### **lette per nome e controllate sul file; quelle dei referti con la riga.** ### **Ogni `[RACCOMANDAZIONE]` manca di proposito: questo documento descrive le forme, NON sceglie.**

## 1. L'ERA 1, COM'ERA *(dal codice e dai referti)*

| | il codice | che cosa e' stato MISURATO | che cosa e' rimasto ipotesi |
|---|---|---|---|
| **la decisione** | `Rete.decidi_divisione` *(`8337`)*; ### **la grandezza: `|tw|`, la torsione dell'arco** *(`8385`)*; `Rete.mitosi` *(`8711`)* esegue | `doc/MITOSI_storia.md` `L77-189`: ### **gli archi divisi hanno `|tw|` `6.98`-`8.35`** *(`1.11`-`1.33` giri)*; ### **una «campana» a `|tw| = 3.79` era un artefatto** *(corretto due volte il `2026-10-01`; la spiegazione in `db89b37`)* | -- |
| **`PHI_CRIT = 2 pi`** | riga `567`: ### **«Un giro, non due: il sistema e' abeliano ... A 4pi la mitosi non scattava MAI e il grafo restava al 100% oltre portata; a 2pi ripara»** | il «non scattava mai» a `4 pi` | ### **perche' `2 pi` sia il quanto giusto** *(«il 4pi veniva dall'intuizione spinoriale, risultata assente»)* |
| **la soglia `3 pi`** | ### **`soglia0 = PHI_CRIT + pi`** *(`8403`-`8405`: «`2pi + pi` (emergente), `= 3pi`», col twist dipolare)* ### **quando `TORS_4PI` e' acceso e `FASE_2PI` no** *(i default)* | ### **`cb178412`: il `pi` dipolare e' assente nel `98%` degli archi**; ### **`D36` (`Z127`): con `phi` su `2 pi` gli archi oltre la soglia vanno da `7047` a `0`** *(`MITOSI_storia.md` `L194-203`)* | ### **se la soglia debba essere adimensionale** *(aperto)* |
| **`TORS_4PI`** | riga `3135`: ### **`True`; il commento dice «default off; la soglia diventa 4pi» ed e' DOPPIAMENTE SCADUTO** | -- | -- |
| **la soglia locale dal gradiente di tempo proprio** | ### **TOLTA il `2026-10-06`** *(decisione di Luca, `8418`-`8428`: `soglia = np.full(...)` a `8417`)*; ### **il commento di `8408`-`8416` la descrive ancora: SCADUTO** | ### **`REFERTO_mitosi_soglia_grad_2026-10-06.md`: senza la modulazione `0.3` le nascite crollano** *(`Ap0/Ap = 0.001641`, `Bp0/Bp = 0.111`: «PORTANTE», «non corretta»)*; ### **la spinta leggeva la grandezza SBAGLIATA** *(Spearman `0.012`-`0.068` col gradiente nudo, `0.870`-`0.915` con `|r_i phivel_i - r_j phivel_j|`)*; ### **`..._zero_dove_2026-10-06.md`: a `1000` passi `R = 0.1616`, «INTERMEDIA»** | ### **mescolare le riduzioni FA CRESCERE le nascite** *(`_perm_`, `_fisso_`: «anti-informativa», `3` semi)* |
| **il tempo proprio e `KERNEL_ALPHA`** | ### **il kernel usa `tau = |tw|/PHI_CRIT` SENZA l'`1`** *(`6251`-`6254`: `exp(alpha tau/(1 + beta tau))`, `beta = alpha/2`)*; ### **`1 + |tw|/PHI_CRIT` compare nel calcio della mitosi** *(`8824`-`8825`)* ### **e nella posizione della campana** *(`8492`-`8501`: «NON E' UN TEMPO PROPRIO ... una POSIZIONE»)* | -- | ### **il legame col principio di equivalenza** *(il commento a `3124`)* |
| **il punto medio e l'olonomia** | ### **`fm = (phi[a] - FRAZ_NASCITA D) % _dphi()`** *(`8782`, il punto medio GEODETICO della fase, su `4 pi`)*; ### **la posizione `pos_figlio` a meta'** *(`8786`)*; ### **i figli `twp = [_wphi(phi[a]-fm), _wphi(fm-phi[b])]`** *(`2261`-`2263`)* | ### **l'invarianza dell'olonomia NON e' esatta:** ### **i genitori prendono un calcio di fase** *(`8824`-`8831`)* ### **dopo `fm` e prima di `twp`** *(`DIVISIONE-AUTOCONSISTENTE`, `8812`-`8815`)* | -- |
| **`PLAST_MIT`, `PLAST_DIN`** | ### **`0.0` e `False`** *(`3107`, `3117`)*; ### **il `d0` dei figli = `d/2`** *(`8874`)*, ### **con `PLAST_DIN` piu' `tanh(max((|tw|/PHI_CRIT - 1) |d - d0|/d0, 0))`** *(`8861`-`8869`)* | ### **nessuna misura nei referti** *(solo `PIANO_riordino_mitosi.md` `L23` e `LETTURA_accensione_e_torsione.md` `L288`)* | ### **«la suddivisione GENERA spazio»** |
| **`MITOSI_2LAM` e `_nasce`** | ### **`MITOSI_2LAM` INERTE dal commit `6b`** *(`469`; il cancello `d >= 2 LAM` e' INCONDIZIONATO, `8653`-`8699`)*; ### **`_nasce` alza ogni pezzo a `LAM`** *(`6930`)* ### **e conta la «LUNGHEZZA FABBRICATA»** | ### **«`_nasce` ... FABBRICA lunghezza (misurato: `_sm_lund_mitosi` vale `0.8 LAM` per evento)»** *(`483`-`485`)*: ### **due meta' `d/2` diventavano `2 LAM`** *(`MITOSI_storia.md` `L239-240`)* | ### **se il flag agisca davvero** *(`_g_m2l_negati`: «non misurato», `PIANO` `L166`)* |
| **`COPPIA_MIT`** *(Schwinger)* | ### **`1.0`: ATTIVA** *(`3097`; il commento dice anche «spenta di default»: SCADUTO)*; ### **l'antinodo nasce a `fm + _dphi()/2`** *(`8945`-`8992`)* | ### **`Z45`: `6` nodi su `19`** *(`1.3%`)*; ### **`Z119`: l'antiparticella prende `+2 pi` mentre il commento dice `+pi`** *(identica nel campo, `D35`)* | -- |
| **`COPPIA_DENSITA`** | ### **`False`** *(`3095`)*; ### **il difetto `PEQ-SEL-STANTIO`** *(`8964`-`8968`)* | -- | -- |
| **il nucleo congelato e il guscio attivo** | ### **l'intestazione** *(`58`-`61`)*: ### **«un NUCLEO congelato ... poca mitosi; un GUSCIO attivo ... dove avviene la mitosi»** | ### ⚠ **I REFERTI DICONO ALTRO:** ### **`RAMIFICAZIONI` `Z46`: il `93%` dei nodi fermi sono le MASSE seminate** *(il guscio a `r 8`)*, ### **i mobili stanno al CENTRO;** ### **`REFERTO_struttura_1200.md`: la mitosi «FERMA», `8` nodi in `1200` passi;** ### **`..._zero_dove_`: «la rete cresce dove c'e' rete», nessuna classe sovrarappresentata** | ### **il profilo nucleo/guscio come struttura fisica** |

## 2. L'ERA 2, COM'E'

- ### **`primo_ordine/crescita.py`: `11` righe, solo l'intestazione** *(«una regola di crescita deve dichiarare il suo bilancio d'energia»)*: ### **nessun codice.**
- ### **`primo_ordine/motore.py`, `cresci`** *(riga `280`)*: ### **un'incidenza nuova, la permutazione dello stato, le estremita' nuove dai loro `iniziali`** *(senza un valore di comodo)*; ### **al piu' una crescita per tick; la usano solo i collaudi, a crescita vuota** *(il commento a `330` dice «a zero»: SCADUTO)*. ### **NESSUNA regola di mitosi.**
- ### **LE VOCI DELL'INDICE:** ### **[[D-BILANCIO-NASCITA]]** *(`2026-10-12`: i genitori pagano con la tensione, il vuoto col suo termine; BLOCCATA «dopo le forme della mitosi», il censimento)*; ### **`DOMANDA-MITOSI-LE-FORME`** *(lo spareggio, `phi`, il ramo della radice, la connessione)*; ### **`DEC-NASCITA-PSI`** *(`psi = 0` vietato: `A16.4` vuole la norma totale conservata)*; ### **`DOMANDA-FUSIONE`, `DOMANDA-LA-MITOSI-CREA-VUOTO`, `DOMANDA-IL-PI-DEL-NODO-CHE-NASCE`.**
- ### **IL NODO `D7` DELL'ALBERO** *(`DEC-D7-DIVISIONE`)*: ### **la nota: «DECISIONE DI LUCA, 2026-10-10 (da CANDIDATA a PRESA). Alla nascita `psi -> psi/sqrt(2)` per il padre E per il figlio, CON LA STESSA FASE»** *(conserva la somma di `rho`, dimezza quella di `rho^2`)* ### ⚠ **ma il campo `presa` e' `False`** *(contrasto `9`)*.
- ### **LA DECISIONE `(A)` DEL `2026-10-08`** *(`doc/REGISTRO_FISICA.md`)*: ### **«chi paga la nascita e' il calore che si scarica sul vuoto locale»** *(dell'era `1`, coi numeri del bilancio: la cascata si ferma da sola a `16` nodi)*.
- ### **IL CENSIMENTO** *(`doc/CENSIMENTO_DECISIONI.md`)*: ### **la mancanza `4` («chi paga la nascita»): bloccata da `DEC-NASCITA-PSI`, le forme della mitosi, `D7`.**

## 3. LE FORME DA SCEGLIERE *(le opzioni, il costo, che cosa rompe, come si misura: NESSUNA scelta)*

### 3(a) QUALE OLONOMIA fa scattare la nascita

| l'opzione | che cosa e' | il costo | che cosa rompe | come si misura |
|---|---|---|---|---|
| `(a1)` ### **il FLUSSO del campo `U(1)` attraverso una placchetta** *(`e B_p`)* | invariante di gauge, locale; ### **il quanto `2 pi` ha senso SOLO se il campo e' COMPATTO** *(una decisione APERTA di Luca, [[PROGETTO-U1]])*: ### **un giro del flusso e' un MONOPOLO che attraversa la placchetta** | il campo dinamico nel nucleo *(oggi solo in memoria)* | ### **nel non compatto `B` non ha giri** | il conto dei giri per placchetta e la loro distribuzione |
| `(a2)` la fase di `A` su un ARCO | `e A_a` | -- | ### **NON e' invariante di gauge: un arco non ha olonomia, un ciclo si'** | -- *(scartata dalla forma)* |
| `(a3)` ### **la TORSIONE DEL VUOTO sull'arco:** `arg(phi_jj^* phi_ii)` | ### **il vuoto e' NEUTRO** *(nessuna `U`, `flussi_parziali.hop_phi`)*, ### **quindi la fase relativa fra due nodi e' invariante:** ### **e' l'equivalente piu' vicino di `tw` dell'era `1`** *(la fase relativa fra i nodi)* | ### **un contatore dei giri** *(la fase srotolata nel tempo: uno stato in piu' per arco)* | ### **`A16`** *(una memoria, da permettere)* | la torsione accumulata per arco e la sua soglia |
| `(a4)` la fase della camminata | la fase di `psi` sull'arco | -- | ### **non invariante di gauge** *(come `(a2)`)*, ### **salvo un anello di Wilson** | -- |
| `(a5)` il FLUSSO di norma sull'arco *(`J` integrato)* | non un'olonomia: un conteggio di carica | -- | non e' un quanto | -- |

### 3(b) LA FORMA SUI TRIANGOLI

| l'opzione | i gradi | il costo | come si misura |
|---|---|---|---|
| ### **`(b1)` lo SDOPPIAMENTO di un arco** *(il nodo nuovo collegato ai due capi e ai due vertici opposti)* | ### **il nuovo `4`, i due opposti da `6` a `7`, i capi restano `6`** *(la somma di `6 - grado`: `+2 - 1 - 1 = 0`, Eulero invariato)* | ### **due difetti di segno opposto a ogni nascita:** ### **la curvatura per costruzione** | la distribuzione dei gradi; ### **la massa nei difetti** *(sezione `4`)* |
| `(b2)` la DIVISIONE di un nodo *(un nodo in due, un arco nuovo fra loro)* | i gradi ridistribuiti fra i due | la scelta della ridistribuzione *(uno spareggio)* | idem |
| `(b3)` un TRIANGOLO in tre *(un nodo al baricentro)* | ### **il nuovo `3`, i tre vertici `7`** | un difetto `3` molto forte | idem |
| ### **la regola INVERSA** *(la morte)* | il collasso di un arco *(l'inverso di `(b1)`)* | ### ⚠ **`A14.2` dice che la crescita e' l'UNICA freccia ammessa** *(`DOMANDA-FUSIONE`)*: ### **la morte come coppia della nascita e' una tensione con l'assioma** | ### **la reversibilita': nascita poi morte = lo stato di partenza** |
| **in 3D sulla FCC** | ### **la FCC non e' simpliciale** *(ottaedri e tetraedri)*: ### **lo sdoppiamento di un arco vuole un complesso di tetraedri** | ### **una triangolazione della FCC** *(ogni ottaedro in quattro tetraedri: una SCELTA di diagonale)* | i difetti di grado `12 +- k` |

### 3(c) IL BILANCIO, CON L'ORIENTAMENTO DI LUCA PER PRIMO

- ### **CHE COSA VUOL DIRE NELL'ERA 2 «l'energia della nascita scambiata col vuoto»:** ### **il vuoto e' la camminata di Grover scalare `phi`** *(`CAMM-GROVER-VUOTO`, `CAMM-SPOSTAMENTO-VUOTO`)*, ### **la sua norma `V` si conserva ESATTA** *(il nodo `DEC-QC-CONSERVATA` dell'albero, presa il `2026-10-16`)*, ### **e la materia lo sente col legame `CAMM-MATERIA-VUOTO`** *(`materia_vuoto.py`, nel tempo `dtau_nodo`)*. ### **L'energia che si conserva al secondo ordine e' `H_tot`** *(`energia.py`)*: ### **la parte del vuoto e' il suo generatore** *(`<I - P_u>`, `<P_->` su `phi`)* ### **piu' `N = rho ln(rho/(rho + Lambda))`.**
- ### **IL VINCOLO DURO:** ### **la probabilita' totale si conserva:** ### **lo stato del nodo che nasce viene da un'IMMERSIONE ISOMETRICA dello stato vecchio nello spazio piu' grande** *(una mappa `W` con `W^dagger W = I`)*, ### **non da un'aggiunta.** ### **La regola di `D7`** *(`psi -> psi/sqrt(2)` per il padre e il figlio, la stessa fase)* ### **e' una tale immersione** *(conserva la somma di `rho`)*; ### **lo stesso per `phi`.**
- ### **DOVE SI PRENDE E DOVE SI RENDE L'ENERGIA:** ### **l'immersione cambia `H_tot` di un `Delta E` che non e' zero in generale** *(i gradi cambiano, il Grover `2/d` cambia)*; ### **l'orientamento di Luca: il VUOTO rende `-Delta E`** ### **con una rotazione UNITARIA delle sue ampiezze sul nodo nuovo e sui vicini** *(che non cambia `V`)*, ### **scelta per annullare `Delta E_tot`.** ### **COME SI MISURA che il conto torna:** ### **`|Delta H_tot|` per nascita all'arrotondamento; `M` e `V` al bit; la corrente d'energia** *(`corrente.py`)* ### **che chiude il bilancio LOCALE attorno al nodo nato.**
- ### **LA REVERSIBILITA':** ### **la morte e' `W^dagger` con la rotazione inversa del vuoto;** ### ⚠ **ma `W^dagger` e' esatta solo sugli stati nell'immagine di `W`:** ### **dopo qualche tick lo stato esce dall'immagine, e la morte di un nodo qualunque PERDE informazione** *(una proiezione: irreversibile)*. ### **La via esatta: una DILATAZIONE unitaria** *(lo stato del nodo nato porta con se' cio' che serve a disfarlo: un grado di liberta' del vuoto come registro)*: ### **una memoria, e quindi `A16`.**
- ### **LE ALTRE OPZIONI:** ### **`(c2)` paga il campo `U(1)`** *(l'energia delle placchette: naturale se la nascita scatta sul flusso, `(a1)`)*; ### **`(c3)` paga la materia stessa** *(la tensione dei genitori: [[D-BILANCIO-NASCITA]])*; ### **`(c4)` non paga nessuno** *(l'energia cresce: viola `A14`, scartata dalla forma)*.

### 3(d) IL PROFILO CHE LA GRAVITA' CHIEDE

- ### **PER `gamma = 1`:** ### **le lunghezze proprie crescono di `|Phi|`** *(`g_ij = (1 + 2|Phi|) delta_ij` a campo debole)*: ### **in 2D l'AREA propria di `2|Phi|`** *(in 3D il volume di `3|Phi|`)*: ### **la frazione di nodi in piu' attesa attorno a una massa e' `~2|Phi|` per unita' d'area.**
- ### **QUANTI NODI SERVONO** *(sulla carta)*: ### **con `Phi = -G M/R`, un anello di raggio `R` ha `~2 pi R` nodi, e i nodi in piu' sono `~2|Phi| 2 pi R = 4 pi G M`, INDIPENDENTI da `R`** *(in 2D)*: ### **perche' il profilo sia liscio e non a gradini serve `4 pi G M >> 1` in unita' del reticolo** *(una massa grande, o un reticolo fine)*; ### **a campo debole fisico** *(`|Phi| ~ 1e-6`)* ### **servono `>> 1e6` nodi per anello.**
- ### **CONTRO L'ERA 1:** ### **il profilo chiesto e' «piu' nodi DOVE `|Phi|` e' grande»;** ### **l'era `1` misurava «la rete cresce dove c'e' rete»** *(nessuna classe sovrarappresentata)* ### **e un centro mobile con le masse ferme:** ### **NON e' lo stesso profilo.**

### 3(e) L'OROLOGIO

- ### **L'ERA 1:** ### **`1 + |tw|/2 pi` come posizione della campana e come calcio** *(non come tempo del kernel, che usa `|tw|/2 pi`)*: ### **la torsione faceva insieme il tempo e lo spazio.**
- ### **L'ERA 2:** ### **`cs = Lambda/(Lambda + Lambda_c)`** *(`flussi_parziali.cs`)* ### **e `dtau_nodo = dtau cs`.** ### ⚠ **LA MITOSI TOCCA `cs` DIRETTAMENTE, attraverso il GRADO:** ### **`Lambda_k = somma |phi_h|^2` sulle estremita' del nodo, e le estremita' sono quante il grado:** ### **un nodo a `4` e uno a `7` con lo stesso vuoto per estremita' hanno `Lambda` diversi, quindi `cs` diversi** *(e' gia' misurato: `DOMANDA-QUALE-FORMA-FISSA-CS`, «`Lambda_k = grado_k lambda_0`, correlazione col grado `1.0000`»)*.
- ### **SEPARARE IL TEMPO DALLO SPAZIO** *(la caduta newtoniana da `cs`; la deflessione doppia dal numero dei nodi)* ### **vuole che `cs` NON veda il grado:** ### **`Lambda` per estremita'** *(`Lambda_k/grado_k`)* ### **o un'immersione che conservi `Lambda_k` del nodo:** ### **una scelta da fare PRIMA del codice.**

## 4. IL LEGAME CON LA CURVATURA

### **LA MITOSI COME STRADA `D` di [[PROGETTO-CURVATURA]]:** ### **accanto ad `A1`** *(la lunghezza sugli archi: la massa per meta' dall'arco, la caduta `x1.50`, `31ee70cc`)*, ### **alla parte `2` sulla carta** *(la famiglia `alpha, beta`: una soluzione solo per `r <= 1`, `5aec4725`)* ### **e ad `A2`/`(C)`.** ### **Il vantaggio sulla carta: OGNI ARCO resta quello di oggi, quindi la massa nell'interno della griglia non e' toccata;** ### **la curvatura sta nei DIFETTI** *(i nodi a `4` e a `7`)*.

### **LE DUE MISURE SULLA CARTA CHE LA DOVREBBERO PRECEDERE** *(solo descritte, non eseguite)*:
1. ### **LA MASSA E `x` SU UN NODO A `4` E A `7` VICINI:** ### **il Grover cambia col grado** *(`2/d`)*: ### **la coppia a `K` attraversa un difetto con un'altra massa?** ### **lo spettro locale del generatore col difetto** *(un toro grande con un difetto, gli stati legati al difetto e lo spostamento dei livelli)*.
2. ### **LA LUCE ATTORNO A UN DIFETTO:** ### **un difetto di grado `d` e' un CONO col difetto d'angolo `2 pi (6 - d)/6`:** ### **la luce di `CampoA1`** *(o di `F1`)* ### **devia di un angolo previsto dalla geometria** *(il fascio dei referti della curvatura)*.

## 5. LE DIPENDENZE

1. ### **la scena a triangoli nel nucleo: FATTA** *(`36040a07`, la parte `A` del censimento)* ### **prima di ogni codice della mitosi;**
2. ### **la decisione sul campo COMPATTO** *(se la nascita scatta sul flusso, `3(a1)`)*;
3. ### **`S1` contro `S4`** *(il legame `CAMM-MATERIA-VUOTO` entra nel bilancio `3(c)`)*;
4. ### **la scelta di `Lambda` per estremita' o per nodo** *(`3(e)`)*;
5. ### **`A16` e `A14.2`** *(la memoria della dilatazione; la morte come coppia)*.

## 6. I CONTRASTI *(riportati, NON corretti)*

1. ### **`MAPPA_DIPENDENZE.md` `L140`-`143`: «il quanto 2 pi fa scattare la mitosi»;** ### **il codice e `CODA_2026-10-09.md` `736`-`740`: la soglia in vigore e' `3 pi`.**
2. ### **`TORS_4PI`** *(`3135`)*: ### **il commento «default off, la soglia diventa 4pi»; il valore `True`, la soglia `3 pi`.**
3. ### **`MITOSI_storia.md` `L227`: `MITOSI_2LAM` «False di default»;** ### **`PIANO_riordino_mitosi.md` `L23`: acceso dal driver; dal `6b` e' una legge incondizionata.**
4. ### **`COPPIA_MIT`** *(`3097`)*: ### **il commento «ATTIVA» e «spenta di default» insieme; «`fm + pi`» contro il `+2 pi` del codice** *(`Z119`)*.
5. ### **`CODA`: il tetto `4 pi` «MAI raggiunto»; `..._zero_dove_` `L155`-`161`: `364` archi oltre `4 pi` a `1000` passi** *(un seme)*.
6. ### **`..._soglia_grad_`** *(`150` passi)*: ### **senza il `0.3` le nascite quasi spariscono; `..._zero_dove_`** *(`1000` passi)*: ### **`R = 0.16`, non annientate.**
7. ### **il criterio di `6b` poggiava su una premessa falsa** *(`PIANO` `L166`)*: ### **che `MITOSI_2LAM` agisca non e' misurato.**
8. ### **IL MANDATO e l'intestazione dell'era `1`** *(«la mitosi nel guscio, poca nel nucleo»)* ### **contro i referti** *(`Z46`: le masse ferme sono il guscio, il centro e' mobile; `..._zero_dove_`: «la rete cresce dove c'e' rete»)*.
9. ### **`DEC-D7-DIVISIONE`: `presa: False`, e la nota dice «da CANDIDATA a PRESA».** ### ⚠ *(ANNOTATO il `2026-10-25`, dopo la conferma di Luca delle `20:44`: NON e' un errore dell'albero. La stessa nota, piu' sotto, dice che `D7` dipende da `DEC-FC-COESIONE`, non presa, e che `P-ALB` rifiuta; l'avevo scritto senza leggere quella riga. Provato di nuovo: [[DOMANDA-D7-DIPENDE-DA-FC]].)*
10. ### **IL MANDATO:** ### **«il tempo proprio `tau = 1 + |torsione|/PHI_CRIT` e `KERNEL_ALPHA`»: il kernel usa `|tw|/PHI_CRIT` SENZA l'`1`** *(`6251`)*; ### **«la soglia locale pilotata dal gradiente di tempo proprio»: TOLTA il `2026-10-06`** *(`8417`-`8428`)*.
11. ### **due commenti scaduti dell'era `2`:** ### **`motore.cresci`** *(«a zero» a `330`, il codice scrive `iniziali`)*.
