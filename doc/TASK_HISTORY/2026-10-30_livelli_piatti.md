# 2026-10-30 — LA REGOLA DEI LIVELLI PIATTI E LA PROVA DI UN SOLITONE CHE LA RISPETTA *(UNA PROVA IN `csv/`, NESSUNA MODIFICA AL NUCLEO; [[PIANO-2D-3D]], [[PROGETTO-MASSA-COLLETTIVA]]; il mandato di Luca delle `09:31`, con l'INTEGRAZIONE delle `09:33`)*

> **LA CODA:** questo mandato viene **dopo** quello delle `09:09`/`09:16`, chiuso in `03142636`. **L'integrazione delle `09:33` arriva prima che questo cominci:** entra qui, nelle premesse e nelle letture, **senza un commit a parte** *(il punto `3` delle `09:33` vale solo se il mandato fosse gia' iniziato)*.
> **LIVELLO:** i pesi del nodo e dell'arco e la saturazione `g` del legame cambiati **IN MEMORIA** in `csv/` *(come in `af1758fd`)*, rimessi all'uscita; Newton, cinque corse brevi, una corsa lunga a pezzi; nessun file del nucleo.
> **I nomi:** `a_n = pi`, `b_a = r pi` i pesi per unita' di tempo *(ATTENZIONE: non la famiglia `mu0 = pi/2` di `_strada_b_r`)*; `g` la saturazione del legame `alpha(x) = g x^2/(1 + x^2)`; `E0 = A(K) = -mu0`; `J = [E0, E0 + U_max]`, `U_max = g`; `F` i livelli piatti; `W` la larghezza della risonanza.

## 1. LE PREMESSE DAL CODICE

### La regola *(del guardiano, da verificare; va in `doc/BANDE_PIATTE.md` PRIMA delle corse)*

Un solitone costruito sul punto `E0` della banda *(oggi `A` a `K`, `E0 = -mu0`, `mu0 = (1/2) sqrt(a_n^2 - a_n b_a + b_a^2)`)* ha una frequenza locale nuda `mu - U(r)` che percorre `J = [E0, E0 + U_max]`, con `U_max` il massimo spostamento del legame *(per `S1` la saturazione `g`, oggi `1`)*, **per QUALUNQUE quantita' di materia**. **Le uscite esponenziali sono quelle i cui prodotti non si propagano** *(le piatte: in `6d941a4d` e `de411167` togliere una piatta sola spegneva il modo anche con la banda `A` disponibile)*. **LA REGOLA:** nessun livello piatto `F` *(`P0 = (b_a - a_n)/2`, `Ppi = -(a_n + b_a)/2`)* e nessuna media di due livelli piatti *(`(F_i + F_j)/2`: `(P0 + Ppi)/2 = -a_n/2`, `P0 + P0`, `Ppi + Ppi`)* deve cadere in `J` allargato di `W`. Le uscite con un prodotto che si propaga danno solo una perdita lenta *(da verificare)*.

**Il controllo sui casi gia' misurati:** `r 1`: la coppia sul bordo di `J` *(decade, `0.15`)*; `r 0.65`: `P0` dentro `J` *(la risonanza di `P0`, `ea8ace8f`)*; `r 1.5247`: la coppia dentro `J` *(il modo lento, la coppia agli anelli `12`-`13`; misurato in `03142636`: tasso `0.0331`, `alpha* 0.60`-`0.64`)*; `r 0.69`: al limite. **E' la stessa cosa delle tre condizioni di `03142636`** *(c1: `F + alpha = mu` cioe' `F = mu - alpha` in `J`; la coppia: `(F_i + F_j)/2 = mu - alpha` in `J`)*, **con in piu' le medie `P0 + P0` e `Ppi + Ppi`** *(che sono i livelli stessi)* **e la larghezza `W`.**

### LA FORMA GENERALE *(l'integrazione delle `09:33`; ### **IPOTESI DEL GUARDIANO DA VERIFICARE, NON LEGGE**)*

Con `omega` la frequenza del solitone, `V(x)` in `[0, V_max]` lo spostamento locale del legame, `F_j` i livelli dei modi a velocita' di gruppo zero *(le piatte)*: **per ogni ordine `n` permesso dal legame, `n (omega - V) != F_j1 + ... + F_jn` per ogni `V` in `[0, V_max]`, con margine `n W`** *(le quasienergie modulo `2 pi/s`; nel limite `s -> 0` senza modulo)*. `n = 1`: una piatta; `n = 2`: la coppia; `n >= 3` solo se il legame ha termini di ordine piu' alto. **Il riferimento:** la condizione di non risonanza dei breather discreti *(MacKay e Aubry, `1994`: `n omega` fuori dallo spettro lineare)*. **Le differenze qui:** (i) il pericolo esponenziale viene solo dai modi fermi *(i modi che si propagano danno una perdita lenta: da verificare)*; (ii) `V` varia lungo il profilo, quindi la condizione vale su un intervallo, non su un valore. **`W` e' empirica** *(`99b679bc`)*; la sua legge *(per esempio con `x alpha'(x)`)* non e' nota.

**Una nota mia, dal codice, sull'ordine `n`:** `alpha(x) = g x^2/(1 + x^2)` **non e' un polinomio**: ha termini di ogni ordine nell'ampiezza. **Ma la stabilita' lineare** *(la crescita esponenziale di un `D` piccolo)* **vede solo `D` e `conj(D)`, cioe' `n = 1` e `n = 2`.** `n >= 3` sarebbe un processo non lineare in `D`, visibile solo vicino alla saturazione. **Lo scrivo come una cosa che NON so verificare con queste corse.**

### Dal codice *(letto in questa sessione)*

- **Il legame:** `_screening_forme_s3._ab("S1", x)` = `(x^2/(1 + x^2), x - arctan x - x^3/(1 + x^2))`; il tick lo prende da `materia_vuoto.pezzi`, che `SF.forma(nome)` sostituisce con `SF.pezzi_di(nome)`. **`g` si applica avvolgendo `SF.pezzi_di`:** `(alpha, beta) -> (g alpha, g beta)`. **Il gemello `beta` scalato dello stesso `g`, dichiarato: col vuoto congelato non agisce sulla materia** *(i pezzi del vuoto sono saltati, `CL.avanza`)*.
- **I pesi:** `flussi_parziali.z_nodo` e `z_arco` avvolti con la frazione per `a_n/pi = 1` e `b_a/pi = r` *(il metodo di `_strada_b_r.pesi`, con un'altra famiglia)*. **A `r 1`, `g 1` i fattori sono `1.0`: il tick deve essere quello di oggi AL BIT** *(DEVE)*.
- **`N` NON cambia la scena** *(una sonda in memoria, nessun file)*: a `N` `3e5`, `1e6`, `3e6` la scena ha `L 81`, `phi0` e le posizioni **identici**; cambia solo la norma dello stato *(e la «larghezza» del continuo, `4.92`, `6.61`, `8.68`, che fissa solo lo stato iniziale)*; lo stato di `dfb5ab7e` riscalato alla norma ruota sotto il tick diversamente del `2.5e-3` *(`3e5`)* e `1.1e-3` *(`3e6`)*: la non linearita'.
- **`W` da `99b679bc`:** spostando la SOMMA delle piatte, il modo si spegne fra `-0.1` e `-0.4` da un lato e fra `+0.4` e `+1.6` dall'altro: **per quanto `0.05`-`0.2` da un lato, `0.2`-`0.8` dall'altro. La larghezza e' ASIMMETRICA**; la regola usa `0.05`-`0.2`. **Lo dichiaro: quale lato corrisponde a «sotto `J`» lo deve dire il segno, e lo script lo stampa.**
- **Un fatto di `03142636`:** i periodi presi dai cambi di segno campionando ogni `3` unita' di tempo sono alias. **Qui il periodo si prende dalle rotazioni per banda** *(campionamento ogni `5` tick, `0.75`)* **se un modo cresce.**

### Sulla carta *(il primo ordine; le previsioni del tick le calcola lo script PRIMA di Newton)*

Con `a_n = pi`, `b_a = r pi`: `mu0 = (pi/2) sqrt(1 - r + r^2)`, `P0 = (r - 1) pi/2`, `Ppi = -(1 + r) pi/2`, `(P0 + Ppi)/2 = -pi/2`.

| | `r`, `g` | `J` | i livelli e le medie | la previsione di Luca |
|---|---|---|---|---|
| **(R)** | `0.6`, `0.5` | `[-1.369, -0.869]` | la coppia `-1.571` **`0.20` sotto**; `P0 -0.628` **`0.24` sopra**; `Ppi -2.513` `1.14` sotto | **nessun modo esponenziale, per ogni `N`** |
| **(X1)** | `1`, `0.5` | `[-1.571, -1.071]` | la coppia `-1.571` **sul bordo** | **decade (la coppia)** |
| **(X2)** | `0.6`, `1` | `[-1.369, -0.369]` | **`P0 -0.628` dentro** | **decade (`P0` da sola)** |

*(I numeri del guardiano: `0.20`, `0.24`, `1.14`; li ho ricontrollati con la formula. **Il margine di (R), `0.20`, sta sul bordo alto di `W`** *(`0.05`-`0.2`)*: **se `W` fosse `0.2`, (R) sarebbe al limite.** Lo scrivo PRIMA.)*

### Cosa NON so

- **se Newton converge** da `dfb5ab7e` a pesi e `g` cosi' lontani *(a `g 0.5` il legame e' la meta')*;
- **se lo stato di (R) resta sotto `L/6 = 13.5`** di larghezza *(a `g` piu' piccolo il legato e' piu' largo)*;
- **quale lato di `W`** vale per la coppia sotto `J`;
- **se `U_max = g`** e' raggiunto: a `N 3e5` il cuore puo' non saturare *(`alpha` del cuore `< g`)*: allora `J` vero e' piu' corto. **Lo script stampa `alpha` del cuore di ogni stato.**

## 1-bis. L'INTEGRAZIONE DELLE `10:06` *(arrivata a mandato iniziato: il task history `68285252` committato, lo script scritto e NON ancora committato; annotata qui con un commit a parte, nessuna corsa in piu')*

1. **Il campionamento:** il periodo vero del modo e' `4.07`-`4.10` *(`03142636`)*; `10.91`, `11.45`, `22.8` e il respiro `11.1` sono compatibili con un alias del campionamento ogni `3` *(**l'errore `n.84` del guardiano**)*. **Qui ogni periodo si misura con le rotazioni per banda, con `D` campionato non piu' rado di `0.75` unita' di tempo, e ogni periodo riportato dice il suo passo.** Lo script: `D` ogni `5` tick *(`0.75`)*; il periodo dai cambi di segno resta stampato come in `03142636`, **ma non entra in nessuna lettura**.
2. **I criteri di forma:** **l'istante al bordo alto della finestra** *(la saturazione: per costruzione l'ULTIMO campione della finestra)* **non entra nei criteri** *(«il modo previsto» di X1 e X2 si legge sui due istanti prima)*. **`Q_S` si confronta con una tolleranza assoluta dichiarata, `1e-6`.** ### **Una cosa da sapere PRIMA:** nei dati di `03142636` `q - 1` della parte piatta PROIETTATA vale `-1.3e-6`..`-6.2e-6` *(l'artefatto del proiettore su `Ppi`, dove tocca `A` in `Gamma`)*, mentre `q(D) - 1` resta sotto `8e-9`: **con `1e-6` sulla parte proiettata, `Q_S` «non tornerebbe» per l'artefatto.** In questo mandato `Q_S` non entra nelle letture; se servira', **il confronto va fatto su `q(D)` o su `q(P0)`** *(`P0` e' isolata)*, **e lo decide Luca.**
3. **`doc/BANDE_PIATTE.md`:** la regola **AGGIORNA la sezione `5`** *(non le si affianca)*: **una taratura sceglie i pesi per un solitone dato; la regola vale per ogni solitone su quel punto della banda, con la legge `U_max <= margine`.** La decisione delle `09:09` *(niente taratura)* resta.
4. **La MAPPA:** la voce del periodo *(`18`, e la `23`)* chiusa come alias; **il respiro della corsa lunga da rimisurare col campionamento fitto**, in lista d'attesa; l'errore `n.84`.

## 2. I CRITERI

| il punto | il criterio *(fissato qui)* |
|---|---|
| `0`, le previsioni | **prima di Newton**, committate: per ogni configurazione, sul tick libero *(`s 0.15`, i generatori ricomposti, `_bande_piatte.ricomposto`)*: `E0 = A(K)`, `J = [E0, E0 + g]`, `P0`, `Ppi`, le tre medie, **la distanza con segno di ciascuno da `J`** *(negativa dentro)*, **il margine minimo**, il confronto con `W` `0.05` e `0.2`; e le stesse al primo ordine. **Se il tick cambia una previsione, vale quella del tick, scritta li'.** **DEVE PASSARE: il tick coi pesi in memoria = il tick ricomposto entro `1e-10`; a `r 1`, `g 1` il tick di uno stato = quello di oggi AL BIT** |
| `1`, Newton | il metodo e il criterio di `26300537` *(`_strada_b_r.cerca`: GMRES precondizionato, `TOLL_RES 1e-9`, `30` passi)*; le partenze: **(R) `N 1e6`, (X1), (X2) da `dfb5ab7e` riscalato**; **(R) `3e5` e `3e6` dallo stato di (R) `1e6` riscalato** *(la continuazione in `N`)*. **Se una ricerca diretta non converge:** una sola tappa, la configurazione di mezzo *(`r` e `g` a meta' strada da `r 1`, `g 1`)*, poi la destinazione; **se ancora no, si corre dallo stato migliore, dichiarato.** Ogni stato committato appena trovato |
| `1`, la scena | `L 81`; **se la larghezza `w` di uno stato supera `L/6 = 13.5`, la sua corsa a `L 120`, dichiarato** |
| `2`, le corse brevi | `300` unita' di tempo *(`2000` tick)* da ogni stato; `|D|/|psi0|` ogni `3` *(`20` tick)*; **la forma: (L) contro (E) come `ea8ace8f`** *(`_strada_b_lati.giudica`; la sua debolezza con l'intercetta negativa dichiarata)*; le pendenze locali; **`D` salvato ogni `5` tick in memoria** *(in `complex64` per l'analisi; dichiarato)*; **se esponenziale: il tasso nella finestra** *(da `10` volte la deriva attesa `residuo/s * tau` a `1e-2`)*, **le bande, gli anelli, le armoniche, le rotazioni per banda** *(`_modo_lento.analizza`)* |
| `3`, la corsa lunga | (R) a `N 1e6`, `20000` tick a pezzi di `2000`, ogni pezzo committato; i punti di `_congelato_lungo.punto` ogni `10` tick; `|D|/|psi0|` e le frazioni di banda di `D` ogni `20`; le finestre di `500` come `ea8ace8f`, contro `26300537` e `lunga_r1.52` |
| le grandezze di ogni (R) | **la massa** *(la curvatura di `A` a `K`)* **e `mu0` contro `r 1`**; `alpha` del cuore; `w` |

## 3. LE LETTURE *(di Luca, scritte prima, senza soglie; con l'integrazione delle `09:33`)*

- **(p1)** le tre (R) senza modo esponenziale e le due (X) col modo previsto *(la coppia per X1, `P0` per X2)*: **la regola e' confermata; la forma generale e' confermata per `n = 1` e `n = 2`.**
- **(p2)** una (R) decade: **la regola e' incompleta** *(quale uscita, dalle bande e dagli anelli)*; **dire quale termine della forma generale manca.**
- **(p3)** una (X) non decade: **la regola e' troppo severa** *(di quanto)*; **dire quale termine della forma generale e' troppo severo.**
- **(p4)** nella corsa lunga (R) il cuore regge, o si svuota lentamente *(la perdita lenta verso una banda che si propaga: dove va `D`)*.
- **Come si legge «il modo previsto»:** per X1, `D` con `P0 + Ppi` maggiore di `A + B`; per X2, `D` con `P0` maggiore di `Ppi + A + B`; agli istanti della finestra.

## 4. LE MOTIVAZIONI

La regola non dipende dal solitone *(`N`, larghezza, nodi)*: si prova su tre `N` e con due controlli che la violano. **La configurazione (R) e' di prova; cambiare il cammino o il legame del nucleo resta una decisione di Luca dopo l'esito.** **E non e' la taratura esclusa alle `09:09`:** li' si sceglievano i pesi per un `S1` dato; qui si prova se una REGOLA che non dipende dal solitone predice chi decade.

## 5. TODO

1. Questo file, committato **DA SOLO**.
2. `doc/BANDE_PIATTE.md`: la sezione della regola e della forma generale, **prima delle corse**.
3. `csv/_livelli_piatti.py` *(`--previsioni`, `--cerca`, `--breve`, `--lunga`, `--referto`)* e la sua riga nell'inventario, committati prima di girare.
4. `--previsioni`: committate prima di Newton.
5. Newton: (R) `1e6`, (X1), (X2), poi (R) `3e5`, `3e6`; ogni stato committato.
6. Le cinque corse brevi; ogni `.json` committato.
7. La corsa lunga di (R) `1e6`, a pezzi.
8. Il referto; `doc/BANDE_PIATTE.md` *(il controllo, l'esito)*; `RELAZIONE`; `MAPPA` *(la riga `d`; l'integrazione delle `09:33`)*; la sezione `6` qui; il checkpoint.

## 5-bis. I CONTROLLI DOPO IL DISCO PIENO *(il mandato di Luca delle `13:40`; scritto PRIMA dei controlli)*

### Le premesse *(cosa credo prima di guardare, e cosa NON so)*

- **Lo spazio:** alle `14:13` su `C:` restano **`6.6G`** *(`df -h`)*. Quello che manca al mandato delle `09:31` scrive pochi file piccoli: gli stati *(`fermo_*.npz`, `1260220` byte l'uno, sovrascritti)*, i pezzi della corsa lunga *(`~49` kB l'uno, `8` ancora)*, lo stato di ripresa *(`1.26` MB, sovrascritto)*, i `.json` delle corse brevi *(`13-21` kB)*. **Credo che basti di tre ordini di grandezza; la stima esce dallo script, non da qui** *(`L-NUMERI`)*. **Il grosso di `db/` e' `db/modo_lento`, `580M`**: le istantanee di `D` del mandato delle `09:09`. **Non lo cancello:** e' una decisione di Luca *(il punto 5 vale «d'ora in poi»)*.
- **git:** `git log origin/primo-ordine..HEAD` e' **vuoto** dopo `git fetch`: **ogni commit locale e' su GitHub**, l'ultimo `6fb0b485` *(`11:25`)*. **Nessun commit dopo le `11:25` e' riuscito**; il solo tentato, il pezzo `02000` della corsa lunga, e' **fermo nel hook dalle `11:36`** *(`git commit` PID `39716` -> `indice.py valida` PID `41012` -> `git cat-file --batch` PID `41948`; tempo di CPU fermo: `0:00:00`, `0:00:13`, `0:00:02` alle `14:13`)*; **`.git/index.lock` NON c'e'**. Il file e' rimasto in stage. **Non e' un commit fallito da rifare: e' un commit mai finito.** Terminare quei processi mi e' stato negato: **non ci riprovo.** Un commit nuovo puo' passare accanto: se il commit fermo un giorno riparte, `HEAD` sara' cambiato e il suo aggiornamento del ramo **fallisce** *(dichiarato: e' cio' che credo di git, non l'ho provato)*.
- **I file scritti dalle `11:19` in poi** *(tutti non committati, salvo i pezzi gia' in `6c385aa2` e `6fb0b485`)*: `lunga_R_1e6_02000.jsonl` *(in stage)*, `breve_X1.json/.txt`, `cerca_R_3e5.json/.txt`, `cerca_X2.json` *(il `.txt` nello scratchpad)*; in `db/livelli_piatti/` *(non si committa: il dato e' il comando)* `fermo_R_3e5.npz`, `fermo_X2.npz`, `lunga_R_1e6.npz` *(la ripresa, a tick `4000`)*. **Cosa NON so:** se uno di questi e' stato scritto troncato a disco pieno. **Gli `.npz` si scrivono su un `_tmp` e poi `os.replace`**, i `.json` con `scrivi_nuovo`: un `.npz` troncato **non si apre**, un `.json` troncato **non si legge**.
- ### ⚠ **LE INDICAZIONI DELLE `13:22` NON LE HO.** Il mandato delle `13:40` le cita *(«la tappa a `2e6` per `R_3e6`, i passi in piu' di `X1`, il criterio aggiunto della forma della crescita»)*, ma **nella conversazione e nel repo non c'e' nessun testo delle `13:22`** *(`grep "13:22"` su `doc/TASK_HISTORY`, `doc/MAPPA.md`, `RELAZIONE_PER_CLAUDE.md`: vuoto)*. **Non le ricostruisco dal titolo:** quanti passi, a che residuo, quale criterio sono decisioni di Luca. **Criterio di chiusura:** il testo delle `13:22`.

### La progettazione *(i passi, cosa decide ciascuno, cosa mi fa FERMARE)*

1. **Uno script di controllo, `csv/_controllo_disco_pieno.py`, committato prima di girare**, che **non scrive niente** su disco *(solo `stdout`, poi il referto)*:
   - **(a) ogni file:** si apre *(`np.load`, `json`)*, la dimensione, lo sha1 dei byte; **per i file committati, lo sha1 coincide col blob a `HEAD`** *(`git cat-file`, in binario)*; **per gli stati, `sha(psi)` = il campo `sha` del `cerca_*.json`**; **per le corse brevi, il loro `sha` = quello dello stato**; **il `.txt` nel repo = la copia nello scratchpad, al byte.**
   - **(b) la corsa lunga AL BIT:** dallo stato di `R_1e6` *(committato in `8e159c2e`)* si rifanno in memoria i tick `1 -> 4000` col ciclo di `lunga()`: **a `2000` lo sha DEVE essere `sha_fine` del pezzo `00000` di `6c385aa2`, e i suoi punti uguali AL BIT; a `4000` lo sha e i punti DEVONO essere quelli del pezzo `02000` sul disco; lo stato di ripresa DEVE avere quello sha e `t 4000`.** *(Controllo positivo: il pezzo `00000` e' committato da prima del disco pieno, quindi DEVE passare; se non passa, lo strumento e' rotto, non il dato.)*
   - **(c) la stima dello spazio** dalle dimensioni misurate in (a), contro lo spazio libero.
2. **Cosa decide:** un file che non passa **si rifa'** *(lo stato col suo `--cerca`, la corsa breve col suo `--breve`, il pezzo dalla ripresa del pezzo prima)* **e non si usa**; un file che passa si committa col suo commit.
3. **Cosa mi fa FERMARE:** (b) che fallisce sul pezzo `00000` *(lo strumento)*; la stima oltre lo spazio libero; un file rotto che non so rifare senza una scelta.
4. **Poi la push; e la ripresa del mandato delle `09:31` SOLO con il testo delle `13:22`.** Il punto 5 delle `13:40` *(le istantanee di `D` solo agli istanti del referto; nessuno stato di prova non usato su disco)* **vale da qui**: `--breve` tiene `D` **in memoria** e nel `.json` scrive solo l'esame; `--cerca` scrive **solo lo stato finale** *(la tappa NON si scrive)*: **gia' cosi' nel codice di `9a1ecdf3`** *(da verificare nello stesso script: nessun file oltre a quelli elencati in (a))*.


### L'ESITO DEI CONTROLLI, PRIMA PROVA *(`4e2bf875`, sha1-BYTE `98459922`; il referto `doc/referti_l2/livelli_piatti/controllo_disco_pieno.txt`; ### **FERMO**)*

- **(a2) gli stati: `5/5` PASSANO.** `fermo_R_1e6`, `R_3e6`, `X1`, `R_3e5`, `X2`: ciascuno `1260220` byte, si apre, `psi (39366, 2) complex128`, `sha(psi)` = il campo `sha` del suo `cerca_*.json`, `mu` uguale. **Nessuno stato rotto.**
- **(a1) i file committati: `5/6`;** il sesto, `breve_R_3e6.txt`, FALLISCE **per la trappola CRLF** *(par.7)*: sul disco `1555` byte con CRLF *(l'output di python su Windows, uguale al byte alla copia nello scratchpad)*, nel blob `1547` con LF; `diff` non trova differenze di testo. **E' il mio controllo che confronta i byte di un `.txt`: il file e' sano.**
- **(a3) le brevi: `1/3`;** FALLISCONO `breve_R_1e6` *(committato in `640f4fa6`, prima del disco pieno)* e `breve_X1` **perche' ho preso come riferimento delle chiavi `breve_R_3e6`, la cui forma «non si giudica» e che percio' ha `19` chiavi invece di `28`** *(mancano `a`, `c`, `finestra`, `finestra_tau`, `gamma`, `scarto_E`, `scarto_L`, `tasso`, `v`)*. **Il fallimento su `R_1e6`, committato prima, e' il controllo positivo che smaschera lo strumento.** `breve_X1` ha le `28` chiavi di `breve_R_1e6`.
- **(a4) i `.txt`: `3/3` PASSANO** *(`breve_X1`, `cerca_R_3e5` uguali al byte allo scratchpad; `cerca_X2` chiuso dalla riga del residuo finale)*.
- ### ⛔ **(b) la corsa lunga rifatta in memoria: NON FINITA.** **`numpy._ArrayMemoryError: Unable to allocate 1.20 MiB`** dentro `flussi_parziali.grover`: **la memoria virtuale del sistema e' esaurita** *(`systeminfo`: in uso `62.250` MB su `63.262`)*, **e il disco e' di nuovo pieno: `256M` liberi** *(`df -h`)*, **contro i `6.6G` delle `14:13`**. **Il mio controllo non scrive su disco; chi abbia consumato `~6` GB in mezz'ora NON lo so** *(i processi piu' grandi: `vmmemWSL` `7.1` GB, `Code.exe`)*. **Quindi il pezzo `02000` e lo stato di ripresa NON sono verificati: non si usano.**
- **(c) lo spazio: non misurato** *(lo script e' morto prima)*; **ma il punto 1 delle `13:40` e' gia' deciso dai fatti: ADESSO NON BASTA.** **FERMO.**
- **La correzione dei due difetti dello strumento** *(i `.txt` confrontati senza i CR; le chiavi delle brevi contro quelle committate di `R_1e6` o `R_3e6`)* **e' pronta e NON applicata:** e' un commit a se', dopo lo spazio.

- **Dopo il FERMO** *(Luca: «ora c'e' spazio»)*: `df -h` `16G` liberi; memoria virtuale disponibile `10.605` MB *(`systeminfo`)*. **Il primo commit di questo esito era rimasto fermo nel hook e l'ho interrotto col `timeout` dopo `900` s: rifatto qui.** Il commit del pezzo `02000` *(PID `39716`)* e' ancora fermo; un `git` in piu' *(PID `45192`)*, probabilmente il figlio del commit interrotto, anche.

## 5-ter. L'ESITO DEI CONTROLLI, RIGIRATI; E IL COMMIT APPESO CHIUSO *(Luca, `15:45`, punti `0` e `1`)*

- **I controlli, rigirati per intero** *(lo script corretto di `5eeb3d5c`, sha1-BYTE `b732959f`; ### **Luca chiedeva «lo script di `4e2bf875`»: quello aveva i due difetti di strumento di `47ad8c8c`, e l'ho corretto PRIMA del suo messaggio; dichiarato)***: **`32/32` PASSANO.** Il controllo positivo *(il pezzo `00000` di `6c385aa2`, rifatto in memoria)* passa AL BIT; **il pezzo `02000` e lo stato di ripresa *(`t 4000`)* coincidono AL BIT con la corsa rifatta**; gli `5` stati, le `3` brevi, i `.txt` sani; lo spazio che serve per finire, per eccesso, `8.52` MB contro `30.72` GB liberi. Il referto: `doc/referti_l2/livelli_piatti/controllo_disco_pieno.txt`.
- **Il commit appeso dalle `11:36`:** terminato `git cat-file --batch` *(PID `41948`)*, con lui sono usciti `indice.py valida` *(`41012`)* e `git commit` *(`39716`)*; terminato anche il `git` rimasto dal mio commit interrotto *(`45192`)*. **`.git/index.lock` non c'e'.** Il ciclo della corsa lunga, che aspettava quel commit, **si e' fermato da se'** *(il commit fallito: `FINE lunga 02000 commit 1`)* **senza girare il pezzo `04000`** *(lo stato di ripresa e' ancora delle `11:28:59`)*. ### ⚠ **Il job in coda dello stato di `R_3e5` e' ripartito da solo appena liberato il lucchetto** *(`15:58`)*: committa `cerca_R_3e5` e poi gira la sua corsa breve. **E' cio' che il punto `5` chiede** *(`R_3e5` passa i controlli)*, **ma non l'ho deciso io a quell'ora: dichiarato.**
- **Il pezzo `02000`** si committa con un commit nuovo, ora che i controlli passano.

## 6-pre. LA RIPRESA DEL MANDATO DELLE `09:31` *(il testo delle `13:22`, mandato alle `15:45`; scritto PRIMA dello script e delle corse)*

### Le premesse dal codice

- **`newton` fa al piu' `SB.MAX_NEWTON = 30` passi** e tiene **lo stato migliore**; il criterio e' `SB.TOLL_RES = 1e-9` sul residuo relativo del tick *(il criterio di `26300537`)*. **Per i passi in piu' di `X1` serve un argomento `passi`** *(nessun default: `30` per le ricerche di prima, `10` per `X1`)*.
- **`scrivi_nuovo` apre in `xb`: un `.json` esistente non si riscrive.** Quindi gli stati e le brevi nuovi hanno **nomi nuovi**: **`R_3e6_t`** *(`R_3e6` per la tappa a `2e6`)* e **`X1_p`** *(`X1` coi passi in piu')*; **le vecchie `cerca_R_3e6`, `breve_R_3e6`, `cerca_X1`, `breve_X1` restano, dichiarate** *(stati non fermi)*.
- **La tappa a `2e6`:** dallo stato di `R_1e6` riscalato a `N 2e6`, Newton coi `30` passi; poi dallo stato della tappa riscalato a `3e6`, Newton coi `30` passi. **La tappa resta in memoria: non si scrive** *(il punto `3` delle `15:45`, e il `5` delle `13:40`)*; nel `.json` di `R_3e6_t` restano **la sua storia dei residui e il suo `mu`**, non lo stato.
- **`X1_p`:** dallo stato migliore di `X1` *(`2.290e-7`, sha `005443ea`)*, Newton con al piu' `10` passi. **Se converge**, la sua breve dallo stato fermo; **la breve di `X1` dallo stato non fermo resta, dichiarata.**
- **Se `R_3e6_t` o `X1_p` NON convergono:** lo stato migliore si scrive e si dichiara, come per gli altri; la breve di `R_3e6_t` gira comunque *(il punto `3` dice «poi la sua corsa breve»)*; quella di `X1_p` **no** *(il punto `4` la lega alla convergenza)*.
- **La corsa lunga:** l'ultimo pezzo che passa AL BIT e' `02000` *(fine a tick `4000`)*: si riparte dallo stato di ripresa, pezzi `04000` .. `18000`, fino a `20000`. **Lo script non si modifica mentre gira:** prima si committa la versione nuova, poi si lancia.
- **La memoria:** alle `14:40` la memoria virtuale si era esaurita. **Al piu' due processi di calcolo insieme** *(la corsa lunga e una ricerca, o una breve)*.

### IL CRITERIO AGGIUNTO DELLA FORMA DELLA CRESCITA *(il punto `6`; scritto PRIMA di leggere i casi)*

**Il difetto del criterio vecchio** *((L) contro (E) nello scarto di `ln|D|`)*: con l'intercetta negativa *(`breve_R_1e6`: `|D| = -1.774e-8 + 3.502e-9 t`)* lo scarto di (L) e' **infinito** e vince (E) **per costruzione**, anche se `|D|` cresce come `v t` *(`v / attesa 1.11`)*.

**Il criterio aggiunto, dalle pendenze locali** `l(t) = d ln|D|/dt` *(le stesse che il referto gia' stampa: `np.gradient` di `ln|D|` sui campioni ogni `3`)*, **sui campioni sotto la saturazione `1e-2`, esclusi il primo e l'ultimo della serie** *(il bordo del gradiente)*:

- **perche':** se `|D| = c + v t`, `l = v/(c + v t)` **tende a `1/t`**; se `|D| ~ e^{gamma t}`, `l` **tende alla costante `gamma`**; se `|D| ~ t^b`, `l = b/t`.
- **il fit:** `l = gamma + b/t`, minimi quadrati in `(1, 1/t)`; `sigma_gamma` dalla covarianza del fit.
- **ESPONENZIALE** se `gamma - 3 sigma_gamma > 0` **e** `gamma t_ultimo > 1` *(la costante supera `1/t` dentro la finestra: e' cio' che rende «sopra una costante» VISIBILE; il `3 sigma` e' quello di `PATTERN_DI_PROVA`)*;
- **altrimenti, una POTENZA `t^b`:** **LINEARE** se `b` arrotondato all'intero e' `1` *(le alternative sono discrete: `t`, `t^2` di un seme quadratico, la costante `t^0` del caso nullo)*; altrimenti **POTENZA `t^<b>`**, dichiarata;
- **meno di `3` campioni:** non si giudica.
- **Il collaudo, PRIMA dei casi** *(`P1-sexies`; stampato nel referto, sulla stessa griglia `t = 3 .. 300` ogni `3`)*: **DEVE dare LINEARE** `|D| = 1e-8 t` e `|D| = -1.774e-8 + 3.502e-9 t` *(i numeri di `breve_R_1e6`: il caso che il criterio vecchio sbaglia)*; **DEVE dare ESPONENZIALE** `|D| = 1e-8 e^{0.06 t}` e `|D| = 1e-8 (t + e^{0.0331 t})` *(il tasso del modo lento, col seme lineare)*; **il caso nullo** `|D| = 1e-8` *(niente cresce)* **DEVE dare POTENZA `t^0`, non LINEARE ne' ESPONENZIALE.**
- **Nel referto, per ogni breve:** la lettura **alla lettera del criterio vecchio** *(stampata accanto, invariata)* e quella del criterio aggiunto. **Le letture `p1`-`p3` usano il criterio aggiunto**; **dove i due danno forme diverse, si dice.** Vale per le brevi gia' fatte *(`R_1e6`, `R_3e6`, `X1`)*, **rilette dal `.json`, non rifatte.**

### La progettazione, e cosa mi fa FERMARE

1. Questo testo, committato **da solo**; poi la MAPPA *(la ripresa, la tappa, i passi di `X1`, il criterio aggiunto, il commit appeso)*.
2. I dati in coda committati: il pezzo `02000`, `breve_X1`, `cerca_X2` *(`R_3e5` col suo job)*.
3. **Lo script nuovo** *(`--cerca R_3e6_t`, `--cerca X1_p`, `newton(..., passi)`, il criterio aggiunto e il collaudo nel referto)* **e la sua riga nell'inventario, committati prima di girare** — **solo quando nessuna corsa dello script vecchio e' in vita** *(la breve di `R_3e5`)*.
4. Le corse: la corsa lunga *(`04000` .. `18000`, ogni pezzo committato)* e, accanto, `R_3e6_t`, poi `X1_p`, poi le brevi *(`X2`, `R_3e6_t`, e `X1_p` se converge)*.
5. Il referto, `BANDE_PIATTE` *(l'esito)*, `RELAZIONE`, `MAPPA` *(la riga `d`, i punti `10:06`)*, la sezione `6` qui.
- **FERMO se:** **il collaudo del criterio aggiunto fallisce** *(si committa il fallimento e ci si ferma: un criterio che sbaglia sui casi noti non legge i casi veri)*; un pezzo della corsa lunga che non riparte AL BIT dal precedente *(l'`assert` di `lunga()`)*; lo spazio o la memoria di nuovo esauriti.

## 6-pre-bis. L'AGGIUNTA DELLE `16:00` *(LA MEMORIA)*, E I SUOI NUMERI; ### **FERMO**

- **Il testo, in breve:** dopo il punto `0`, misurare la memoria virtuale libera e lo spazio; **sotto `15` GB liberi di memoria virtuale, o con processi `python.exe` estranei, FERMARSI** *(Luca decide se riavviare)*; **la corsa lunga si confronta AL BIT solo fino al tick `2000`** *(il pezzo `00000` di `6c385aa2`)*, **il pezzo `02000` e lo stato di ripresa si scartano e si rifanno dal tick `2000`**; **UN SOLO processo di calcolo alla volta**, col controllo a fine corsa che sia terminato; **sotto `4` GB liberi: fermarsi.** ### **Sostituisce, per la corsa lunga e il parallelismo, cio' che avevo scritto in `6-pre`** *(«al piu' due processi»; «si riparte dallo stato di ripresa a `4000`»)*: **vale l'ultima** *(`PRECEDENZA-IN-CODA`)*.
- **Le misure** *(`systeminfo`, `df -h`, `tasklist`)*: alle `16:02` memoria virtuale **disponibile `8.929` MB** *(massima `46.416`, in uso `37.487`)*, `C:` **`29G`** liberi; vivi: **un solo `python.exe`** *(PID `1800`, `127` MB: la corsa breve di `R_3e5`, di questo lavoro, partita da sola dopo il commit del suo stato alle `16:00`)* e i `git.exe` della push di `2924d947`. Alle `16:03:44`, finita la breve: **nessun `python.exe` vivo**, memoria virtuale **disponibile `10.494` MB**. ### **SOTTO I `15` GB: FERMO.** **La dimensione massima e' scesa da `63.262` a `46.416` MB**: il file di paging si e' ristretto *(compatibile con l'ipotesi di Luca)*.
- **La breve di `R_3e5` e' finita prima dell'aggiunta** *(partita alle `16:02`, finita alle `16:03:44`, `88` s)*: si committa. **Stato NON fermo** *(residuo `1.242e-3`)*: `|D|/|psi0|` parte da `2.18e-2`, **nessun campione sotto `1e-2`: la forma non si giudica, con nessuno dei due criteri.**
- **Scartati** *(cancellati dal disco, non committati)*: `doc/referti_l2/livelli_piatti/lunga_R_1e6_02000.jsonl` *(sha1 dei byte `c7d385c4`)* e `db/livelli_piatti/lunga_R_1e6.npz` *(lo stato a `t 4000`)*. **Erano sani AL BIT** *(`5-ter`)*, **ma l'ordine e' di rifarli.** ### ⚠ **Per ripartire dal tick `2000` lo script deve RICOSTRUIRE lo stato a `2000`** *(da `fermo_R_1e6`, `2000` tick in memoria, `sha` = `sha_fine` del pezzo `00000`)*: **`lunga()` oggi, senza stato di ripresa, ripartirebbe da `0` e si fermerebbe sull'`assert` di `scrivi_nuovo`** *(il pezzo `00000` esiste)*. **Va nello script nuovo, prima di girare.**
- **Committati ora, senza calcolo:** `breve_R_3e5`, `breve_X1`, `cerca_X2` *(passati i controlli)*.


### ANNOTAZIONE a `6-pre`, prima di girare il collaudo *(non riscrive: annota)*

- **Il secondo caso del collaudo, come l'ho scritto** *(`|D| = -1.774e-8 + 3.502e-9 t` su `t = 3 .. 300`)*, **e' NEGATIVO per `t < 5.07`**: un modulo negativo non esiste, e `ln` non e' definito. **Errore mio nel caso, non nel criterio.** Il collaudo toglie i campioni con `|D| <= 0` *(resta una retta con intercetta negativa, cioe' `l = 1/(t - 5.07)`)*.
- ### ⚠ **Provandolo nello scratchpad prima di committare** *(solo i `5` casi sintetici, nessun caso vero)* **quel caso da' `potenza t^2`, NON lineare:** vicino allo zero di `|D|` le pendenze locali sono grandi, e il fit `gamma + b/t` le legge come `b ~ 2`. **Gli altri quattro danno cio' che devono.** **Il numero vero esce dal collaudo committato** *(`--collaudo-forma`)*. **Se lo conferma: e' il FERMO scritto in `6-pre` per il criterio** -- ### **la LETTURA della forma aspetta la decisione di Luca; le corse no** *(non usano il criterio)*. **Non correggo il criterio da solo:** sarebbe scegliere il criterio dopo aver visto come sbaglia.
- **Lo script nuovo, il collaudo e questa annotazione vanno nello stesso commit** *(dichiarato: l'annotazione e' prima della corsa, non prima dello script)*.

## 6-pre-ter. IL MANDATO DELLE `16:26` *(«dopo il riavvio»)*: LO STATO DELLA MACCHINA, L'ORDINE NUOVO *(scritto prima del lavoro che resta)*

- **Lo stato della macchina, alle `16:47:58`** *(`systeminfo`, `df -h`, `tasklist`)*: ### ⚠ **il PC NON risulta riavviato** *(«Tempo di avvio sistema: `29/10/2026, 02:35:42`»)*; memoria virtuale **disponibile `14.707` MB** *(massima `46.400`, in uso `31.693`)*, fisica disponibile `13.760` MB; `C:` **`29G`** liberi; **nessun `git.exe` vivo**; **un `python.exe` vivo, PID `46456`, `230` MB: il mio** *(sotto)*.
- **La soglia nuova:** fermarsi sotto **`4` GB** di memoria virtuale disponibile *(non piu' `15`)*; **un solo processo di calcolo alla volta.**
- **L'ordine nuovo** *(`PRECEDENZA-IN-CODA`: vale questo, e sostituisce quello di `6-pre`)*: **(a)** la corsa lunga di `R_1e6`, lo stato a `2000` ricostruito al bit col pezzo `00000`, poi fino a `20000`; **(b)** la breve di `X2` dal suo stato migliore *(`4.8e-5`, dichiarato)*; **(c)** `R_3e6` con la tappa a `N 2e6` *(non scritta)*, poi la breve; **(d)** `R_3e5` per continuazione con la tappa a `N 6e5` *(non scritta)*, poi `3e5`; **se non converge si scrive, e si dice se Newton allarga lo stato fino al bordo del toro** *(la larghezza `w` contro `L/6` e contro `L`, gia' stampata nel referto)*; poi la breve. ### **`X1_p` (i `10` passi in piu' di `X1`) NON e' nell'ultima versione: non si gira.** **Da annotare nel referto, senza lettura nuova:** `X1` decade per la coppia col tasso `0.061` *(a `g 1`, `r 1`: `0.151`)*: **un indizio che la larghezza `W` scali col legame `g`.**
- ### ⚠ **Il mio errore d'ordine, dichiarato:** alle `16:32` avevo gia' lanciato, col driver, l'ordine di `6-pre` *(prima `R_3e6_t`, poi `X1_p`, poi la corsa lunga)*; il mandato delle `16:26` l'ho letto alle `16:47`. **Ho fermato il driver** *(il suo `bash`)*, **ma il `python` della ricerca `R_3e6_t` (PID `46456`) e' rimasto vivo, e terminarlo mi e' stato NEGATO.** **Lo lascio finire:** e' il passo **(c)**, dallo script committato `5e6cc257` *(sha1-BYTE `f53ad849`)*, quindi non e' lavoro sprecato; **ma gira PRIMA di (a), contro l'ordine.** Finche' e' vivo: **nessun'altra corsa** *(una alla volta)* **e nessuna modifica allo script** *(e' importato)*.
- **Lo script per (d)** *(la tappa a `N 6e5` per `R_3e5`: una voce `R_3e5_t` in `RIPRESE`, partenza `R_1e6`)* **si scrive e si committa a ricerca `R_3e6_t` finita**, poi l'ordine: (a), (b), la breve di (c), (d).
