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
