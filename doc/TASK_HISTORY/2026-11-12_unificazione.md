# 2026-11-12 -- L'UNIFICAZIONE DEI DUE RAMI *(il passo `3` della ROTTA; Luca `10:39`)* [[PIANO-2D-3D]] [[H-NUCLEO-CONGELATO]]

> **La decisione di Luca** *(`2026-11-12` `10:39`)*: **la condizione «dopo la chiusura di S5» e' tolta.**
> - **S5 non ha mai toccato il nucleo** *(tutto nel banco, fuori)*.
> - **La prossima domanda** *(la gravita' G insieme alla `U(1)`)* **vuole i due rami insieme.**
>
> **Il mandato:** **U0** il piano *(questo file)*, **FERMO** per la conferma; **U1** i segnaposto; **U2** la fusione; **U3** il doppio zero; **U4** i controlli; **U5** l'unificazione; **U6** i coefficienti, su carta e misurati.
>
> ### ⚠ **La domanda aperta su G1** *(rifarlo con `h_k` della sola materia, o passare a G2)* **resta in coda:** **questo mandato viene prima.**

## 1. LE PREMESSE DAL CODICE *(U0: cosa credo prima di toccare, e cosa NON so)*

### 1.1 Lo stato *(da `git fetch`, `11:0x`)*

- ### **Il principale e' a `ff0602dd`, il laterale a `986440d6`**:
  - **il mandato dice `9c8dc888` e `f0affd34`;**
  - **dopo sono venuti, sul laterale, la cura 2 di A** *(`986440d6`)* **e, sul principale, la relazione di G1** *(`ff0602dd`)*;
  - **nessuna corsa in atto.**
- **La base comune: `0bebbe94`** *(`2026-11-09` `02:40`)*. **Dopo la base: `113` commit sul principale, `115` sul laterale.**
- ### **La prima fusione e' gia' «sciolta» sul laterale:**
  - **il laterale ha fuso il principale** *(lo stato X, `ebe2f13c`, col revert `de46816d` dentro)*;
  - **poi ha rifatto `git revert de46816d`** *(lo stato Y, `8cfda2f1`)*.
  - **Quindi un `git merge origin/zero-nel-nucleo` sul principale PORTA v2** *(il revert del revert e' un commit del laterale che il principale non ha)*.

### 1.2 I file che differiscono *(`git diff --name-only origin/primo-ordine origin/zero-nel-nucleo`; «chi» = il lato che l'ha cambiato dalla base)*

| la categoria | i file | chi |
|---|---|---|
| **il nucleo** *(`primo_ordine/`)* | **`12`** *(la tabella 1.3)* | **TUTTI dal laterale** |
| **gli strumenti** *(`csv/`, fuori dal nucleo)* | **`4`** in `csv/` *(`_simmetrie_reticolo`, `_triangoli_bassa_energia`, `_triangoli_forza`, `_zero_simmetrico`)* **+ `46`** in `csv/solitone/` | **`csv/`: laterale.** **`csv/solitone/`: `26` laterale, `20` principale** |
| **i documenti** | `CLAUDE.md`, `RELAZIONE_PER_CLAUDE.md`, `doc/MAPPA.md`, `doc/PIANO_2D_3D.md`, `doc/PROGETTO_MITOSI.md`, `doc/REGOLE/par4.md`, `doc/ROTTA.md` | **principale** |
| | `doc/LEGGI_PROVATE.md`, `doc/indice/leggi.jsonl`, `doc/indice/storico_era2.jsonl`, `doc/leggi_era2/CAMM-*.md` *(4)*, `db_era2/stato_0bc547638e.npz.timbro.json` | **laterale** |
| | **`doc/INVENTARIO_strumenti.md`** | ### **TUTTI E DUE: l'unico conflitto atteso** |
| **i task history** | **`11`** | **`10` principale, `1` laterale** *(`2026-11-09_laterale_mb.md`)* |
| **i referti** *(`doc/referti_l2/`)* | **`117`** | **`81` principale, `36` laterale** |

### 1.3 Il nucleo: lo sha dei due lati *(### **`sha1-BYTE`, lo sha1 dei byte grezzi**, NON `git hash-object`)*

| il file | principale `ff0602dd` | laterale `986440d6` |
|---|---|---|
| `primo_ordine/_collauda_motore.py` | `e4526319` | `4d60d2f2` |
| `primo_ordine/_collauda_r60.py` | `2c972bfe` | `1ee3f0eb` |
| `primo_ordine/_mappa.yaml` | `1eb339be` | `f3bb3fdc` |
| `primo_ordine/_misura_hw.py` | `a28e1413` | `98c1d34b` |
| `primo_ordine/_misura_mb2.py` | `266b5600` | `48269077` |
| `primo_ordine/energia_pesata.py` | `cfaff204` | `43bce8ad` |
| `primo_ordine/flussi_parziali.py` | `1461182f` | `d43b1cf8` |
| `primo_ordine/leggi/leggi.yaml` | `809d7fdb` | `1c0eac29` |
| `primo_ordine/termini/camm_grover.py` | `925a9103` | `10b70489` |
| `primo_ordine/termini/camm_grover_vuoto.py` | `60ef8476` | `8f88bc20` |
| `primo_ordine/termini/camm_spostamento.py` | `4123e139` | `d58a753f` |
| `primo_ordine/termini/camm_spostamento_vuoto.py` | `a98c4267` | `a58a55ea` |

**`primo_ordine/tick.py` e gli altri: uguali nei due rami.**

### 1.4 I conflitti attesi, e come si risolvono

- **Il nucleo: nessun conflitto atteso** *(il principale non l'ha toccato: e' congelato)*. **Se ne compare uno: vince il LATERALE.**
- ### **`doc/INVENTARIO_strumenti.md`: si UNISCONO le righe dei due lati** *(niente si perde)*; **per una voce cambiata da tutti e due, la riga del lato che ha il blob del file nel ramo fuso, e una nota.**
- **I documenti cambiati da un lato solo** *(RELAZIONE, MAPPA, ROTTA, CLAUDE, i task history)*: **git li prende senza conflitto.** **Li controllo uno per uno dopo la fusione** *(nessuna riga persa: il conto delle righe contro i due lati)*.
- **I referti: i due insiemi insieme** *(nessun nome in comune fra i file cambiati)*.

### 1.5 Il doppio zero *(lo zero simmetrico in memoria)*

- ### **SUL LATERALE E' GIA' SPENTO** *(dal `2026-11-08`, `7c181cc4`, poi il revert del revert `8cfda2f1`)*:
  - **`csv/_zero_simmetrico.convenzione_simmetrica()` non applica NULLA** *(un `yield` solo, col testo «applicarla ancora darebbe lo zero DUE volte»)*;
  - **`csv/_triangoli_bassa_energia.conv(nome)` e' un'IDENTITA' DICHIARATA:** **`assert nome == "simm"` e `nullcontext()`** *(«lo zero di prima non esiste piu' nel nucleo»)*.
- **Gli usi:**
  - **`BE.conv(DC.ZERO)` in `~100` file di `csv/`** *(fra cui `csv/solitone/corsa_accensione.py`, `5` volte)*: **passano tutti da `BE.conv`, un punto solo;**
  - **`ZS.convenzione_simmetrica()` usata direttamente in `csv/_segno_gravita.py`, `csv/_modi_pi_e_solitoni.py`, `csv/_scomposizione_zero_lambda.py`:** **anche loro ora non applicano niente.**
- **Sul principale le due funzioni AVVOLGONO davvero.**
  - **La fusione porta le versioni del laterale** *(cambiate solo li')*: ### **lo spegnimento ENTRA CON LA FUSIONE, non va scritto.**
  - **U3 diventa una VERIFICA:**
    - **nessun file del ramo fuso applica lo zero in memoria;**
    - ### **DEVE: il tick della corsa = il tick del nucleo** *(il braccio `0` di v2, `csv/solitone/zero_nel_nucleo.py`, gia' `4/4` al bit sul laterale: `Z0-D`, `Z0-R`)*;
    - ### **DEVE FALLIRE: lo zero applicato DUE volte** *(`Z0-F-D`, `Z0-F-R` dello stesso strumento: `4` chiavi diverse)*;
    - **l'energia di uno stato col doppio zero spostata di `2 pi (M + V)` invece di `pi (M + V)`:** **una misura da aggiungere** *(e' la richiesta di Luca; lo strumento di oggi guarda le chiavi della dinamica, non l'energia)*.

### 1.6 Le costanti da convertire *(`E_nuovo = E_vecchio + pi (M + V)`; per unita' di norma `e_K_nuovo = e_K_vecchio + pi`)*

- ### ⚠ **LA CONVERSIONE NON E' AL BIT:** **`-4.7122750003546425 + pi = -1.5706823467648494`, mentre `e_K` misurato con v2 e' `-1.5706823467648499`** *(lo scarto `4.4e-16`, da `python`)*. **Quindi le costanti convertite si confrontano con una tolleranza:** **la proposta `1e-14` relativo** *(`~45` ulp: dichiarata, non tarata su un risultato)*.

| dove | che cosa confronta | vecchio | nuovo | la formula |
|---|---|---|---|---|
| **`csv/solitone/corsa_accensione.py`** *(`corsa`, l'assert della testa)* | `testa["e_K"] == e_K` | `-4.7122750003546425` *(C35-pi; ogni corsa ha il suo)* | `-1.5706823467648499` | **`e_K == testa["e_K"] + pi` entro `1e-14`** |
| **`csv/solitone/corsa_accensione.py`** *(`ripresa`, R-1: «il controllo all'apertura di C35-pi»)* | `campioni` uguali al pezzo registrato | **le energie dei campioni** *(`E`, nel jsonl)* | **`E + pi (M + V)`** | **le chiavi della dinamica al bit; le energie convertite entro `1e-14`** |
| **`csv/solitone/test_protetto.py`** *(la cassetta, P3)* | `e_K == ref["e_K"]` *(BG-F-0.15, il primo pezzo)* | il `e_K` del jsonl | `+ pi` | **come sopra** |
| **`csv/_respiro_congelato.py`, `csv/_respiro_sul_fondo.py`** | `e_K == testa["e_K"]` | | `+ pi` | **come sopra** *(sigilli vecchi: si rigirano al loro commit; li elenco, non li tocco se non sono nella suite)* |

- ### **Cosa NON so:**
  - **se altri referti usati come riferimento portino energie assolute** *(`carta_coppia`, `carta_statiche`, `libreria`, `_u1_carica_e` leggono `e_K` dai jsonl, ma per SCALARE: `N |e_K|`; il cambio di `e_K` cambia la scala, non un confronto)*;
  - ### **se la cassetta oggi passi sul laterale:** **il suo ultimo referto e' `fbccc445`, PRIMA di v2.** **La misuro in U4.**

### 1.7 P3 *(`vieta_cs`)*: **un punto che non torna col ramo `unificazione`**

- **`csv/solitone/ramo.py`:**
  - **il divieto e' acceso solo sul ramo `primo-ordine` e con `doc/NUCLEO_CONGELATO.md` a `CONGELATO`;**
  - **`csv/solitone/p3_ramo.py`** *(P3-D)* **PRETENDE `ramo == "primo-ordine"`.**
- ### **Sul ramo `unificazione` il divieto NON e' attivo, e P3-D FALLIREBBE per il nome del ramo, non per la fisica.**
- **La proposta:**
  - **in U4, su `unificazione`, P3-F e P3-S** *(la decisione pura)*;
  - ### **P3-D in U5, sul `primo-ordine` avanzato in LOCALE, PRIMA del push:** **se fallisce, il puntatore torna indietro** *(`git reset` del solo ramo locale al vecchio hash, il push non avviene)*.
- **Anche il presidio `H-NUCLEO-CONGELATO` guarda il nome del ramo:** **su `unificazione` non blocca** *(cosi' la fusione puo' portare il nucleo)*; **il fast-forward di U5 non e' un commit: il presidio non lo vede.**

## 2. PROGETTAZIONE DEL RAGIONAMENTO *(i passi, cosa decide ciascuno, cosa mi fa FERMARE)*

- **U1:**
  - **due tag annotati** *(`pre-unificazione-principale` a `origin/primo-ordine`, `pre-unificazione-laterale` a `origin/zero-nel-nucleo`)*, **pushati;**
  - **il ramo `unificazione` da `primo-ordine`, pushato.**
- **U2:**
  - **`git merge --no-ff origin/zero-nel-nucleo` su `unificazione`** *(il messaggio coi conflitti e le risoluzioni)*;
  - **`doc/NUCLEO_CONGELATO.md`: il nucleo unificato** *(la tabella 1.3, il lato laterale)* **e la decisione di Luca delle `10:39`;**
  - **lo stato resta `CONGELATO`** *(sul `primo-ordine` di oggi non si committa niente nel nucleo; su `unificazione` il presidio non agisce)*.
  - ### **FERMO se: un conflitto nel nucleo** *(non atteso)*, **o una riga persa nei documenti.**
- **U3** *(la verifica di 1.5)*:
  - **un censimento** *(`git grep`)* **che nessun file applichi lo zero in memoria;**
  - **`zero_nel_nucleo.py`** *(i DEVE e i DEVE FALLIRE di Luca)*;
  - **la misura dell'energia col doppio zero** *(uno script nuovo, il codice committato prima)*.
- **U4** *(uno alla volta; al PRIMO che fallisce: FERMO, `primo-ordine` com'era)*:
  1. **la suite completa** *(`primo_ordine/collauda.py`: `67` collaudi, `~12`-`18` minuti; dentro R60 `1.3 s`, M-B1 `28 s`)*;
  2. **la cassetta con le costanti convertite** *(`csv/solitone/collauda.py`; la durata da misurare)*;
  3. **`zero_nel_nucleo.py`; P3-F e P3-S;**
  4. ### **il controllo all'apertura di C35-pi** *(R-1 di `ripresa`, con le energie convertite)*: **DEVE passare;**
  5. ### **la riproduzione:**
     - **da C35-pi a `60000` e da TBS a `10000`, `1000` tick col nucleo unificato e `1000` tick col codice di `pre-unificazione-principale`** *(un worktree temporaneo su `E:`, cancellato dopo)*;
     - **la rms di `rho` relativa sotto `1e-10`, la norma, la distanza della coppia, l'energia convertita entro `1e-10` relativo;**
     - **se coincidono al bit, lo scrivo;**
  6. **il banco del lapse a `N = 1` = il tick del nucleo unificato al bit** *(S5.1, `s5_banco.py`)*; **il prototipo `U(1)`: i suoi collaudi T1** *(e T4 se breve)*;
  7. ### **DEVE FALLIRE: il confronto della riproduzione SENZA la conversione dell'energia.**
  - **Il referto: `doc/referti_l2/unificazione_controlli.txt`.**
- **U5:**
  - **`primo-ordine` avanza in locale a `unificazione`** *(fast-forward)*; **P3-D;** **poi il push;**
  - **il tag `laterale-archiviato` e la riga in cima alla relazione del laterale;**
  - **la ROTTA** *(il passo `3` chiuso, lo storico)*; **`doc/LEGGI_PROVATE.md`** *(entra con la fusione)*; **la RELAZIONE.**
- **U6:** **le tre forme dei coefficienti** *((k1) `|z| = 1`, (k2) `alpha + beta = 1`, (k3) `I - beta (I - S)`)* **su carta, poi una misura breve ciascuna fuori dal nucleo;** **DEVE FALLIRE una forma sbagliata apposta; FERMO per la scelta di Luca.**

### 2.1 Il piano di ritorno indietro

- **Fino a U5 `primo-ordine` NON si muove:** **tornare indietro = cancellare il ramo `unificazione`** *(i tag restano)*.
- **Dopo U5:** **`primo-ordine` si riporta a `pre-unificazione-principale`** *(un `git reset` del ramo + push forzato: SOLO con la decisione di Luca)*.
- **`zero-nel-nucleo` non si cancella mai** *(il tag `pre-unificazione-laterale`)*.

## 3. TODO DEL NEXT STEP

1. **commit e push di questo piano; FERMO per la conferma di Luca** *(una riga)*, **anche sulle due proposte:**
   - **la tolleranza `1e-14` per le costanti convertite** *(1.6)*;
   - **P3-D in U5 sul `primo-ordine` locale prima del push** *(1.7)*;
2. **dopo la conferma: U1.**

## 4. LA CONFERMA DI LUCA E U1

- ### **U0 CONFERMATO** *(Luca `2026-11-12`, dopo `fca1dd26`)*. **Le sue decisioni:**
  1. **la tolleranza `1e-14` relativa per le costanti convertite** *(l'ultimo bit della conversione, dichiarato)*; **P3-D in U5, sul `primo-ordine` locale prima del push;**
  2. **fino alla fine di U5: NIENTE commit su `zero-nel-nucleo` e nessuna prova; tutto il lavoro sul ramo `unificazione`;**
  3. **i tag sugli ULTIMI commit su origin, verificati con `git fetch`;** **se dopo i tag compare un commit nuovo su `origin/zero-nel-nucleo`: FERMO;**
  4. **il codice di prova per le costanti convertite** *(la cassetta, R-1 di `ripresa`)* **si committa su `unificazione` PRIMA di girare i controlli;**
  5. **U1-U4** *(fermo al primo controllo che fallisce)*, **poi U5 e U6; commit, push e hash dopo ogni fase; niente cicli di attesa;**
  6. **dopo U5 il laterale e' archiviato; si lavora solo sul `primo-ordine` unificato** *(`wt_zero` resta finche' Luca non decide)*.
- ### **U1, FATTO** *(i tag annotati, pushati)*:
  - **`pre-unificazione-principale` -> `fca1dd26`** *(`fca1dd26144835470a8e0f983fc14d6762ceece9`)*;
  - **`pre-unificazione-laterale` -> `986440d6`** *(`986440d6b54533a09e06e35b79568678b702db97`)*;
  - **il ramo `unificazione` da `primo-ordine` a `fca1dd26`, pushato;**
  - **dopo i tag `origin/zero-nel-nucleo` e' ancora a `986440d6`.**

## 5. U2 E U3

- **U2** *(`d9b1f943`)*: **la fusione; un solo conflitto, l'inventario, risolto unendo i due blocchi; ogni altro file = il lato che l'ha cambiato; la suite sull'albero fuso `67` su `67`.**
- ### **U3, IL BRACCIO 0 DI v2: `4/4`** *(dalle `12:10:16` alle `12:11:06`, a `f9784206`; `doc/referti_l2/unificazione_zero_nel_nucleo.txt`)*:
  - **il padre e' il worktree temporaneo `E:\soliton_simulator\wt_pre_unificazione`, a `pre-unificazione-principale`;**
  - **Z0-D e Z0-R: il tick del nucleo unificato = il tick del VECCHIO con l'avvolgimento, AL BIT, `6` chiavi su `6`** *(dopo la rampa e nella rampa)*;
  - **Z0-F-D e Z0-F-R, lo zero DUE volte: `4` chiavi diverse** *(`Lambda`, `phi_h`, `psi_h`, `rho`)*, **come deve.**
  - ### **Il doppio zero e' spento: entrato con la fusione.**
    - **Il censimento:** **`convenzione_simmetrica` non applica niente; `BE.conv` e' un'identita' con l'assert;**
    - **solo `zero_nel_nucleo.doppio_avvolgimento` rimette l'avvolgimento, ed e' lo strumento del DEVE FALLIRE.**
- ### **U3, L'ENERGIA** *(i json dello strumento `energia_doppio_zero.py`, a `f9784206`; i numeri da uno script sui json)*:
  - **lo stato di TBS a `100000`: `M0 995049.6959049285`, `V0 35768.45723562832` UGUALI nei due nuclei;**
  - ### **E0 vecchio `5039901.153070251`, nuovo `8278311.890163623`: il nuovo meno il vecchio `3238410.7370933713` = `pi (M + V)` ESATTO** *(lo scarto `0.000e+00`)*;
  - **`e_K` nuovo meno vecchio meno `pi`: `-4.4e-16`;**
  - **gli sha dello stato dopo `20` tick: UGUALI.**
- ### ⚠ **UNA PREMESSA DEL MANDATO CHE NON REGGE** *(U3, il DEVE FALLIRE sull'energia)*:
  - **«riattivando l'involucro sul nucleo unificato, il controllo dell'energia di uno stato di riferimento deve vedere lo spostamento doppio, `2 pi (M + V)`».**
  - ### **Dal codice:**
    - **l'energia di uno stato si calcola con una formula esplicita, `primo_ordine/energia_pesata.termini_di_h`, ed e' LI' che v2 ha messo lo zero simmetrico** *(`-pi s (N/2 - P)` sul nodo, `- Re incro` sull'arco)*;
    - **l'avvolgimento di prima sostituisce SOLO le funzioni del tick** *(`FP.grover`, `hop_psi`, `hop_phi`)*.
  - ### **Quindi rimettere l'avvolgimento NON puo' spostare l'energia di uno stato:** **sposta la fase della dinamica, ed e' cio' che Z0-F vede.**
  - **Lo spostamento `pi (M + V)` sta nella FORMULA dell'energia, non nel tick.**
  - **Un difetto mio nello strumento:** **`energia_doppio_zero.py --doppio` avvolge tutta la misura, anche la costruzione della scena, e li' le bande col doppio zero si rompono** *(`ValueError` in `_materia_leggera.bande_coppia`)*.
    - **Non lo curo adesso:** **anche curato misurerebbe una cosa che non puo' cambiare.**
  - ### **FERMO: la decisione e' di Luca.** **La proposta:**
    - **il DEVE FALLIRE di U3 e' Z0-F** *(lo zero due volte, visto sulla dinamica, `4` chiavi)*;
    - **il DEVE FALLIRE dell'energia sta in U4** *(il confronto SENZA la conversione deve fallire, ed e' gia' nel piano)*.
- **Due inciampi dell'ambiente, curati:**
  - **git rifiuta il worktree su `E:`** *(«dubious ownership»: il filesystem non registra il proprietario)*, **e il presidio `P-BARRIERA` rifiutava di girare:** **l'eccezione `safe.directory` passata SOLO per variabile d'ambiente** *(`GIT_CONFIG_COUNT`)*, **la configurazione globale non e' toccata;**
  - **`db/accensione_lenta/fase_F3.npz`** *(non tracciato)* **mancava nel worktree:** **copiato, lo sha `4beb01d95a98` uguale nel principale e nel laterale.**
- ### **LA DECISIONE DI LUCA SU U3** *(`2026-11-12`)*: **U3 ACCETTATO.**
  - **Il DEVE FALLIRE sull'energia col doppio zero era sbagliato in partenza:** **ERRORE DEL GUARDIANO `n.139`** *(l'energia e' una formula, l'involucro tocca solo il tick)*.
  - **Il doppio zero e' gia' riconosciuto dalla dinamica** *(le `4` chiavi diverse di Z0-F), **e basta.**
  - **Si procede con U4, fermandosi al primo controllo che fallisce.**

## 6. U4, I CONTROLLI (uno alla volta; FERMO al primo che fallisce)

- **Il codice dei controlli PRIMA** *(`6c97a2e3`)*: `conversione_v2.py`; l'assert della testa e R-1 in `corsa_accensione.py`; P3 in `test_protetto.py`; `riproduzione_unificazione.py`.
- ### **(1) LA SUITE COMPLETA: `67` su `67`** *(dalle `12:30:28` alle `12:43:36`, sull'albero di `6c97a2e3`)*.
- ### **(2) LA CASSETTA: `107/108`, FALLISCE D6** *(dalle `12:47:30` alle `12:48:42`, a `6c97a2e3`; `doc/referti_l2/unificazione_cassetta.txt`)*:
  - ### **P3 PASSA con la conversione:** **`mu`, il residuo, `w_in`, `h` AL BIT; `e_K -1.5706823467648499` = il primo pezzo di BG-F-0.15 + `pi` entro `1e-14`; il controllo positivo** *(il legame acceso, `-0.5706823467648499`)* **resta diverso anche convertito.**
  - ### **FALLISCE D6:** **«nessun `.py` della libreria cambiato da `654292f2` a HEAD»** *(`cambiati ['csv/solitone/__init__.py', 'csv/solitone/b1_profilo.py', 'csv/solitone/b1_raccordo.py', 'csv/solitone/c0_cucitura.py', 'csv/solitone/carta_coppia.py', 'csv/solitone/carta_coppia_ss.py', 'csv/solitone/carta_f1.py', 'csv/solitone/carta_f1_lunga.py', 'csv/solitone/carta_punto_fisso.py', 'csv/solitone/carta_punto_fisso_r.py', 'csv/solitone/confronta_coppia_ra.py', 'csv/solitone/confronta_co ...`)*.
  - ### **D6 NON dipende dalla fusione:** **da `654292f2`** *(`2026-11-08` `19:00`)* **il principale da solo ha cambiato `26` `.py` di `csv/solitone/`, il laterale `32`** *(`git diff --name-only`, escluso `collauda.py`)*; **l'ultimo referto della cassetta e' `fbccc445` dello stesso giorno.** **D6 fallirebbe anche sul principale di prima: la cassetta e' scaduta su tutti e due i rami.**
  - ### **FERMO** *(il mandato: al primo controllo che fallisce)*. **`primo-ordine` e' com'era** *(`fca1dd26`)*.
  - **La proposta, la decisione e' di Luca:** **D6 si riallinea alla libreria del nucleo unificato** *(`LIBRERIA_RIFERITA` = il commit della fusione)*, **un commit a se', con la suite;** **oppure si accetta D6 fallito come scadenza nota e si prosegue con (3).**
- ### **D6 RIALLINEATO** *(Luca `2026-11-12`; `9e32c88d`, la suite `67` su `67`)*: **`LIBRERIA_RIFERITA = 6c97a2e3`** *(il commit su cui la cassetta aveva passato `107/108`)*; **il motivo scritto nel collaudo: la cassetta era scaduta su tutti e due i rami dall'8 novembre, non per la fusione.**
- ### **(2) LA CASSETTA RIFATTA: `108/108`** *(dalle `13:13:51` alle `13:15:01`, a `9e32c88d`; `doc/referti_l2/unificazione_cassetta_bis.txt`)*.
- ### **(3) P3** *(`doc/referti_l2/unificazione_p3.txt`)*:
  - **lo script `p3_ramo.py` su `unificazione` NON arriva a P3-F e P3-S:**
    - **il divieto non e' attivo** *(il ramo non e' `primo-ordine`)*;
    - **quindi P3-D chiama la `energia_pesata.applica` VERA col motore finto del test, che si rompe** *(`'Finto' object has no attribute 'dtau'`)*;
    - **e' cio' che il piano prevedeva** *(1.7: P3-D in U5, sul `primo-ordine` locale prima del push)*;
  - ### **P3-F e P3-S, la decisione pura** *(la funzione committata `ramo.decidi`, chiamata direttamente)*: **come devono:**
    - **`zero-nel-nucleo` CONGELATO: non vieta;**
    - **`primo-ordine` SBLOCCATO: non vieta;**
    - **`primo-ordine` CONGELATO: vieta.**
- ### **(4) R-1 DI C35-pi: INTERROTTO PRIMA DI RIFARE IL PEZZO** *(alle `13:19:16`-`13:19:18`, a `7e8cbdf3`, codice `1`; `doc/referti_l2/unificazione_r1_interrotta.txt`)*:
  - **R-0 PASSA:** **il file di ripresa e' a `200000` e i suoi sha = `sha_fine` dell'ultima riga, al bit.**
  - ### **POI R-1 SI FERMA: «lo stato completo a `196667` non c'e'».**
    - **`ripresa` rifa' sempre l'ULTIMO pezzo, e dopo gli allungamenti l'ultimo pezzo di C35-pi e' `196667 -> 200000`;**
    - **ma gli stati completi sono ogni `10000` tick** *(`0`, ..., `200000`)*.
  - ### **I pezzi che cominciano su uno stato:** **solo quelli fino a `60000 -> 66667`** *(gli allungamenti partono da `66667`, `76667`, ...)*.
  - ### **Il controllo di Luca** *(«il controllo all'apertura di C35-pi, quello che fece fallire la prima fusione»)* **NON e' stato fatto:** **l'assert della testa sta dentro `corsa()`, che non e' partita.**
  - ### **FERMO** *(il mandato: al primo controllo che fallisce)*. **`primo-ordine` e' com'era.**
  - **La proposta, la decisione e' di Luca:**
    - ### **(a)** **`ripresa(nome, t0=...)`: R-1 sul pezzo che comincia a `t0`** *(i jsonl fino al pezzo prima, lo stato a `t0`)*.
      - **Su C35-pi il pezzo `60000 -> 66667`:** **`2739 s` all'originale** *(circa `46` minuti)*; **e' quello su cui la prima fusione non passo'** *(`doc/referti_l2/ripresa_C35-pi_v2_non_passa.txt`)*.
      - **Un commit a se', con la suite, poi R-1.**
    - **(b)** **solo l'apertura** *(l'assert della testa, senza rifare il pezzo)*, **e la riproduzione** *(il controllo (5), `1000` tick da `60000`)* **al posto del pezzo intero.**
- ### **(4) R-1 DI C35-pi SUL PEZZO `60000 -> 66667`** *(Luca `2026-11-12`; dalle `13:44:54` alle `14:38:16`, a `27e9bb7e`, codice `1`; `3181 s`, l'originale `2739 s`; `doc/referti_l2/unificazione_r1_60000.txt`)*:
  - ### **PASSA LA DINAMICA, AL BIT:** **`sha_fine`, D, `D_acc`, `dopo_stato`, `t1`, lo sha1 del file delle mappe.**
  - ### **PASSA IL BORDO CONVERTITO** *(`E_ass` da accumulatore: `1.1e-14`)*.
  - ### **PASSA L'APERTURA A `66667`** *(R-A: `mu` e `w_in` al bit, `e_K -4.7122750003546425 + pi = -1.5706823467648499` entro `1e-14`, lo stato di ripresa = `sha_fine` del pezzo rifatto)*: **il controllo che fece fallire la prima fusione.**
  - ### **NON PASSANO I CAMPIONI CONVERTITI** *(diverse `E` e `per`)*. **La diagnosi, dai jsonl:**
    - **sul toro intero** *(`E.totale`)* **la conversione regge:** **`cin`, `cost`, `tot` entro `1.6e-16`;** **`vuo` a `1.29e-14`, appena SOPRA `1e-14` relativo AL TERMINE** *(`vuo` e' piccolo, `5652`, la differenza di termini molto piu' grandi)*;
    - ### **per REGIONE** *(`vicino`, `lontano`)* **e per settore** *(`per.E_set`)* **NO:**
      - **anche `cin` cambia** *(`3e-4`, di segno opposto nelle due regioni, il totale uguale)*;
      - **le maschere sono le stesse:** **la massa della regione vicina e' al bit in ogni campione;**
    - ### **IL PERCHE'** *(dal codice di `energia_pesata.termini_di_h`)*:
      - **lo zero di v2 sposta un pezzo dell'energia dagli ARCHI ai NODI** *(sul nodo `0.5 nrm - pu`, sull'arco `- Re incro`)*;
      - **sul toro intero i due spostamenti si compensano;**
      - **in una regione gli archi che attraversano il confine NON si compensano;**
      - ### **quindi «`cin` uguale, `cost + pi M`» vale per il TOTALE, non per regione: la mia conversione per regione era SBAGLIATA** *(un errore mio)*, **e quella dei settori di `per` non c'era.**
  - ### **UN ERRORE MIO DI CONTABILITA':** **R-1-V** *(il DEVE FALLIRE senza conversione)* **e' contato fra i falliti, ma va come deve** *(i campioni e il bordo non sono uguali al bit)*: **`corsa_accensione.esito` non ha l'argomento `deve`, e l'ho chiamato come un DEVE PASSARE.**
  - ### **FERMO** *(il mandato: al primo controllo che fallisce)*. **`primo-ordine` e' com'era.**
  - **La proposta, la decisione e' di Luca:**
    1. **per un pezzo registrato col nucleo vecchio, R-1 controlla:**
       - **la dinamica al bit;**
       - **il bordo convertito;**
       - **le energie del TOTALE convertite, con la tolleranza `1e-14` relativa alla SCALA DELL'ENERGIA** *(`|tot|`)* **invece che al termine;**
       - **le energie per regione e per settore NON si confrontano** *(dichiarato: il confine sposta energia fra archi e nodi)*, **ma le loro `M` e `V` al bit;**
    2. **R-1-V col verso giusto** *(`not ...`, come R-1-F)*;
    3. **un commit a se', con la suite;** **e R-1 si rifa'** *(circa `53` minuti)*, **oppure si rilegge dai due jsonl gia' scritti** *(la sabbiera `E:\soliton_simulator\ripresa_R1\C35-pi_20261112_134456`)*.
- ### **LA DECISIONE DI LUCA** *(`14:55`, ripetuta alle `15:08`)*: **la proposta accettata, con la tolleranza `1e-14` relativa a `max(|tot|, pi (M + V))`** *(il pavimento dell'arrotondamento della costante aggiunta, non una taratura)*; **R-1 si RILEGGE dai jsonl gia' scritti.** **Errore del guardiano `n.141`** *(nella MAPPA, accanto ai miei: la conversione per regione, la contabilita' di R-1-V)*.
- **Il codice dei criteri** *(`a393e310`, la suite `67` su `67`)*.
- ### **(4) R-1 RILETTO: `4/4`** *(dalle `15:14:22` alle `15:14:46`, a `a393e310`; `doc/referti_l2/unificazione_r1_60000_riletto.txt`)*:
  - **la dinamica al bit;**
  - **i campioni: il TOTALE convertito entro `2.3e-16` della scala, `M` e `V` per regione e per settore al bit, ogni altra chiave al bit;**
  - **il bordo convertito `1.1e-14`;**
  - **R-1-V e R-1-F falliscono come devono;**
  - ### **l'apertura a `66667` PASSA.**
- **La nota in `doc/LEGGI_PROVATE.md`, sez. `6`:** **fra referti del nucleo vecchio e del nucleo unificato si confrontano solo il totale, `M` e `V`.**
- ### **(5) LA RIPRODUZIONE: `9/9`** *(dalle `15:19:43` alle `15:36:02`, a `01763cf7`; il vecchio nel worktree `E:\soliton_simulator\wt_pre_unificazione`; `doc/referti_l2/unificazione_riproduzione.txt`)*:
  - **C35-pi da `60000` e TBS da `10000`, `1000` tick del ciclo della corsa** *(col bordo)*;
  - ### **`rho` e gli sha di OGNI chiave AL BIT** *(la rms `0.000e+00`)*, **la norma, `V`, la distanza della coppia** *(`37.428755539897566`)* **uguali;**
  - **l'energia convertita entro `1.1e-16`** *(la soglia di Luca `1e-10`)*;
  - **senza conversione `4.1e-01` e `3.9e-01`: il DEVE FALLIRE fallisce come deve.**
