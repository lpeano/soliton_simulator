# Sistema dei solitoni relazionali

## Intento e ontologia

Questo progetto esplora un modello discreto in cui spazio, materia e tempo non
sono ingredienti primitivi, ma emergono dalle relazioni di fase tra solitoni.
I solitoni sono **puntatori di fase**, non oggetti materiali: ciò che il modello
considera fisico è il campo d'interferenza e la rete di relazioni sugli archi.
Le coordinate servono alla connettività, all'integrazione metrica e al disegno;
non rappresentano da sole la materia.

Il simulatore è uno strumento di ricerca e falsificazione. Una legge presente
nel codice è una legge del modello implementato, non automaticamente una legge
della natura. I risultati vanno distinti tra **dimostrati**, **in verifica** e
**aperti**, secondo la loro ripetibilità sperimentale.

La formalizzazione matematica, con formule e definizioni delle leggi
implementate, è disponibile in [`FISICA.md`](FISICA.md). Questo README resta la
guida operativa del progetto.

La descrizione pedissequa della geometria di contatto, del grafo, della metrica
degli archi e delle modifiche topologiche è in
[`GEOMETRIA_CONTATTO.md`](GEOMETRIA_CONTATTO.md).

Guida operativa e scientifica per `soliton_simulator.py` e per gli script di
esperimento del repository.

## 1. Requisiti

- Python 3.10 o superiore.
- `numpy`, `scipy` e `matplotlib`.
- `ffmpeg` disponibile nel `PATH` se si vogliono generare video MP4.
- Windows: usare i file `.bat` da PowerShell o dal Prompt dei comandi.
- Linux/macOS: usare `RunTutti.bash` con `bash`.

Installazione tipica delle dipendenze Python:

```text
python -m pip install numpy scipy matplotlib
```

Il simulatore non richiede un database esterno. I file `.pkl` usati con
`--sync-db` sono cache di stato locali e non fanno parte dei risultati da
versionare.

## 2. Principio del simulatore

Il modello tratta i solitoni come puntatori di fase. Le grandezze fisiche da
osservare sono le interferenze, il campo `Psi`, le relazioni sugli archi, la
metrica dinamica e le strutture di fase; le coordinate servono soprattutto al
rendering.

La configurazione corrente include, tra le altre, queste leggi:

- campo d'interferenza con saturazione razionale;
- fasi al secondo ordine e inerzia della velocità di fase;
- memoria hebbiana dei legami e del moto;
- tempo proprio locale e kernel pesato dalla torsione;
- torsione e mitosi topologica per quanto di olonomia;
- metrica dinamica sugli archi, deformazione e lunghezza di riposo plastica;
- gravitazione bifase con tetto causale;
- spinore SU(2) non abeliano, attivo di default;
- frame-dragging e, negli esperimenti dedicati, conversione viriale;
- schermatura dell'interferenza attiva e ancorata alla densità critica adattiva
	`N_c`, senza usare `P_LAM` o `LAM_MIN` come manopole fisiche;
- tracking della concorrenza delle masse e diagnostica multimassa.

Per interpretare i risultati vale la disciplina sperimentale: i run brevi
verificano che il codice parta, mentre gli effetti dinamici vanno giudicati su
run lunghi e su più semi casuali. Una correlazione istantanea non dimostra una
causalità ritardata.

## 3. Avvio diretto

### Modalità interattiva

```text
python soliton_simulator.py
```

La finestra mostra il campo d'interferenza, il pozzo gravitazionale e i
puntatori. I tasti principali sono:

- `Spazio`: pausa/ripresa;
- `R`: rotazione automatica della vista;
- frecce: rotazione manuale;
- `+` / `-`: zoom;
- `S`: semina di puntatori;
- `C`: semina continua;
- `F` / `L`: aumenta/riduce i passi per frame;
- `D`: attiva/disattiva il denoise del solo rendering;
- `G`: attiva/disattiva la bussola.

### Batch numerico

```text
python soliton_simulator.py --batch --nmasse 3 --sep 16 --seed 1 --passi 20000 --ogni 5 --csv risultati.csv --diaglog diagnostica.csv
```

Il batch non crea video. Produce:

- un CSV compatto con condensazione, distanza tra masse, gusci e picchi nuovi;
- un `diaglog` dettagliato, una riga per passo, con variabili globali e misure
	per massa/coppia di masse.

Ogni CSV batch e ogni `diaglog` inizia con una riga commentata
`# RUN_PARAMS {...}` in formato JSON compatto. La riga registra la configurazione
del run (seed, masse, separazione, passi, flag fisici come `--sync` e
`--cs-dinamico`, oltre alle costanti effettive), così il report resta interpretabile
anche quando viene separato dal comando o dallo script `.bat` che lo ha prodotto.

Le directory padre indicate in `--csv`, `--diaglog`, `--sync-db` e `--out`
vengono create automaticamente se non esistono.

In PowerShell il comando va lanciato direttamente con `python`. Se si usa
`Start-Process`, tutti gli argomenti del simulatore devono essere passati con
`-ArgumentList`; altrimenti PowerShell può interpretare `--test` o altri flag
come argomenti di `Start-Process`.

### Video headless

```text
python soliton_simulator.py --test N-MASSE --nmasse 3 --sep 16 --seed 1 --giri 0 --ppf 1 --frames 300 --fps 24 --out scena.mp4
```

`--giri 0` blocca la camera: è obbligatorio per distinguere il moto reale dalla
rotazione automatica della vista. `--frames` vale per i video; `--passi` vale
per i batch.

## 4. Flag fisici principali

| Flag | Funzione | Tipo di confronto |
|---|---|---|
| `--calore-vett` | calcio termico vettoriale e chirale, con eccitazione 3D dello spinore | default/esplicito |
| `--calore-scal` | calcio termico scalare isotropo | A/B con vettoriale |
| `--tau-d0` | usa la distanza di riposo per il tempo plastico | A/B con distanza reale |
| `--viriale` | ripartisce la spinta tra componente radiale e tangenziale | legge candidata, zero parametri |
| `--zeta-vir` | riduce il freno nella componente tangenziale della viriale | da usare con `--viriale` |
| `--zeta-loc` | rende lo smorzamento più debole nella materia densa | A/B dello smorzamento |
| `--chi-basc` | organizza la chiralità secondo la torsione locale | A/B della separazione chirale |
| `--polo-maturo` | usa il polo più maturo per dare un verso al twist | da usare con `--chi-basc` |
| `--scala-min` | **DEFAULT OFF, byte-inerte a default.** Nessuna lunghezza sotto `LAM`: **non rimappa il valore, SMORZA LA DISCESA** — un incremento `>= 0` resta intatto **bit per bit**, uno `< 0` e' moltiplicato per `max(0, 1 - LAM/x)` col valore `x` **prima di quella scrittura**. I **sette** pavimenti di `d0` **spariscono**; le nascite partono da `LAM`; per `d` la regola va sull'**incremento del Verlet**. Zero coefficienti. | ramo D |
| `--invarianti=on|off` | **⚠ ACCESI DI DEFAULT** *(l'unico flag delle cure che lo e')*. **Il programma si FERMA al primo passo in cui una grandezza esce dal suo DOMINIO FISICO, e dice DOVE:** grandezza, regola violata, **passo**, **indici** *(arco `i-j` o nodo)*, valori, e la funzione. **Due livelli:** **NUMERICO** *(overflow, divisione per zero, valori non validi)* e **FISICO** *(il registro `DOMINI`, 42 grandezze)*. **L'UNDERFLOW NON ferma niente:** densita' come `1e-81` di un nodo neonato sono **legittime**. **Legge soltanto: su un run sano non cambia un bit** *(sigillo `I1`)*. **`off` serve a RIGIOCARE i run delle epoche 1 e 2**, che violano regole oggi note *(il `peq` negativo al passo 1126)* e che si vogliono riprodurre **com'erano**. |
| `--anom-simm` | **DEFAULT OFF, byte-inerte a default.** **L'anomalia SIMMETRICA, senza pavimento:** `anom = 2(rho-peq)/(rho+peq)`, con **`0/0 := 0` DEFINITO** *(precedente dichiarato: `scala_p`, `Z67`)*. **Toglie `max(peq, 1e-9)`**, che e' un numero **SCELTO** e non esprime nessun vincolo fisico (**`A11`**): con `peq` negativo **ribaltava il segno** e moltiplicava per `3.7e5` (**`Z94`**). Il caso `peq -> 0` con `rho` ordinario passa da `1e+08` a **esattamente `+2`**, e per anomalie piccole le due forme **coincidono** *(la differenza relativa e' meta' dell'anomalia)*. **⚠ RICHIEDE `--peq-esatto`:** con `peq < 0` il denominatore si annulla in `peq = -rho` ed e' un **POLO**, non un limite -- **senza `C1` questa cura sostituisce un pavimento con un polo**, e il codice stampa un **avviso grave**. |
| `--coes-causale` | **DEFAULT OFF, byte-inerte a default.** **La coesione rispetta l'ISTANTE e il CONO LOCALE.** `d0` e `d` si leggono dalla **fotografia di inizio passo** *(prima `richiamo_elastico` leggeva un `d0` gia' spostato da **sette** scritture, sommato a densita' di fine `step`: **due istanti in una `tanh`**)*, e il tetto diventa **`cs_arco*DT`** col `cs` del nodo **piu' lento**, invece di `LAM*sqrt(K_C)*DT`, che e' costruito su **costanti di modulo** e non conosce il cono del luogo (**`A5`**). **Zero parametri:** `_cs_nodo_prev` esiste gia'. **⚠ Il tetto locale NON e' sempre piu' stretto:** dove il cono e' veloce **allarga**. Il punto non e' stringere, e' che il tetto sia quello del **luogo**. |
| `--senza-controllo-registro` | ### **DEFAULT: il controllo e' ACCESO — questo flag lo SPEGNE.** E' l'unico flag del repo il cui default **non** e' *«spento»*, e la ragione va detta: ### **non e' un esperimento, e' la CURA di `RIPIEGHI-ZERO` approvata da Luca**, e un controllo spento di default **non impedisce niente** (`A9`). **Che cosa fa il controllo:** nello schedulatore, all'`apri` *(prima del ciclo)* e **subito dopo la voce `mitosi`**, ogni grandezza di **`REGISTRO_STATO`** *(30 voci)* deve essere lunga **esattamente `n`** *(nodi)* o **`m`** *(archi)*; altrimenti **`CacheCorta`** o **`CacheLunga`**, ### **col nome della grandezza**. Le **10** voci di `REGISTRO_DERIVATE` sono **escluse, col loro motivo MISURATO**. **L'assenza si CONTA** *(`A8`, `_g_registro_assenti`)* **finche' la grandezza non si e' mai vista piena** — poi una sparizione e' un **errore**. ### **A cosa serve il flag:** al **criterio `C`** del sigillo *(`P1-sexies`)*, che chiede di rifare la prova a guasto **col controllo spento** e ritrovare **zero** grandezze protette; senza il flag il sigillo non potrebbe dimostrare di stare misurando il controllo. **Ogni chiamata a controllo spento si CONTA** in `_g_registro_spento`. |
| `--scala-min-passo` | **DEFAULT OFF, byte-inerte a default.** **Il freno della scala minima UNA VOLTA PER PASSO**, sulla **variazione TOTALE** di `d0` e di `d`, dal valore di **inizio passo**. Le **sei** scritture di `d0` e i **`nsub`** sotto-passi di `d` **non frenano piu'**. **Cura il CRICCHETTO di `Z91`:** frenare ogni scrittura separatamente rende il risultato dipendente dall'**ORDINE** delle leggi e, poiche' frena solo le discese, **con spinte opposte di somma nulla non da' zero**. Applicato una volta sola il bias e' **ZERO ESATTO**. **Le nascite restano a `LAM`** *(una concatenazione non e' una discesa)*, e lo **snapshot di inizio passo segue la mitosi** ai quattro siti di ristrutturazione. **Zero coefficienti.** |
| `--peq-nascita-locale` | **DEFAULT OFF, byte-inerte a default.** **Una sola legge di nascita per `peq`, e LOCALE.** Gli archi della creazione di coppia alla **Schwinger** (`:4951`) nascono con `nan` e vengono **calibrati da `step()` sulla `rho` del LORO arco** -- *esattamente come quelli di `_allaccia`* -- invece di prendere **`median(peq)`, la mediana GLOBALE**: una statistica della rete dentro una legge locale (**`A2`**), e quei nodi non hanno alcun rapporto con la mediana. **Zero parametri: il meccanismo esisteva gia'.** **L'eredita' della MITOSI non si tocca** -- un arco che si spezza non *nasce*, **CONTINUA**. |
| `--peq-esatto` | **DEFAULT OFF, byte-inerte a default.** Il rilassamento di `peq` in **forma ESATTA**: `peq <- rho + (peq-rho)*exp(-dt_e/tau_bg)`, piu' lo stesso passo esatto per la diffusione *(splitting di Lie-Trotter, punto fisso `peq+flusso`)*. **E' una COMBINAZIONE CONVESSA, quindi `min(peq,rho) <= peq_new <= max(peq,rho)` per QUALUNQUE passo: `peq` non puo' piu' scavalcare sotto zero.** CURA il difetto misurato in `Z94`: l'Eulero esplicito scavalca per `dt_e/tau_bg > 1` *(misurato `1.2018` al passo 1126 del ramo D)*, `peq` va a `-4.854e-04`, e il pavimento `max(peq,1e-9)` **ribalta il segno** dell'anomalia -> `nsub = 22591`. **Zero coefficienti nuovi:** e' la forma che il par.4 gia' impone ai rilassamenti di primo ordine. **NON toglie il pavimento di `:4215`.** |
| `--coes-adim` | **DEFAULT OFF, byte-inerte a default.** Coesione con **dimensioni giuste e densita' LOCALE**: i tre addendi normalizzati su `I_arco` invece che su `I_med` (media globale, `A2`), e lo spostamento e' `passo_causale * tanh(...) * filtro_portata`, con `|F| <= 1` **per costruzione** invece che per clip. Sostituisce il clip `tanh(stress)*d0`. | ramo D |
| `--chi-coop` | **DEFAULT OFF, byte-inerte a default.** `chi_basc` **non si spegne più** quando lo spinore scrive la carica: scrive la **geometria** in `perc_geom` (letta dalla catena della torsione `CHI_CORE`/`FRAME_DRAG`/`TORS_4PI`), mentre lo **spinore** scrive la **carica** in `perc_chi` (letta dal campo `B` del passo spinoriale, dalla mitosi, da Schwinger e da `TEMPO_SEGNO`). **Richiede `--spinore-corretto`** (`SystemExit`, non un avviso). | ramo C: geometria e carica **cooperano** invece di escludersi |
| `--chi-da-spinore` | **DEFAULT OFF, byte-inerte a default.** `perc_chi` = segno di doppia copertura di `_psi_spinor` dopo il commit, e **`CHI_BASC` viene disattivato nel codice** (`if CHI_BASC and not CHI_DA_SPINORE`). **Richiede `--spinore-corretto`.** ⚠ È l'alternativa **esclusiva** a `--chi-coop`: sostituisce invece di separare. | ramo C **esclusivo**, superato dalla cooperazione |
| `--verso-chi` | aggancia il frame-dragging al verso chirale stabile | A/B del verso |
| `--olon-part` | include twist coerente e curl nella partizione tangenziale | da usare con viriale/polo |
| `--ls-azim` | ricava il verso tangenziale da radiale × spinore | da usare con `--viriale` |
| `--sync` | aggiorna il ponte fase→metrica dallo snapshot iniziale del passo | test Jacobi/Gauss-Seidel |
| `--verlet` | integratore metrico Velocity-Verlet al secondo ordine | confronto A/B, default off |
| `--elast-c C` | coefficiente del nucleo elastico nella dinamica di `d0` | test ridondanza/sensibilita' |
| `--kfrange X` | aggiunge il canale di moto lungo le frange | sonda con parametro, non legge dimostrata |
| `--scala B` | coarse-graining: un solitone rappresenta `B` solitoni fini | cambio di scala |
| `--chi-core` | chiralità emergente del core nei canali collettivi | A/B fisico, default off |
| `--spin-positivi` | registra il sottogruppo `perc_chi=+1` | sola diagnostica |
| `--cs-dinamico` | velocità metrica locale `cs_eff(rho)` con profilo `tanh` e media armonica sugli archi | A/B metrico, default off |
| `--sync-db FILE` | salva o ricarica lo stato versionato | esecuzioni spezzate |
| `--sep=X` *(del DRIVER, default CAMBIATO il 2026-09-26)* | la separazione delle masse. **Default `6.1158` = la scena `(ii)`(a) «STESSO RAGGIO»**; la `(b)` e' `--sep=4.0`, **esplicita**. I numeri vengono da `doc/REGISTRO_FISICA.md`: `(a)` -> `n 12 802`, `471 564` archi, `QUOTA 0.0966`; `(b)` -> `n 4 252`, `148 237` archi, `QUOTA 0.0484`. **NON e' byte-inerte, ed e' il punto:** il default segue cio' che si lancia davvero | era `4.0`, e prima `8` |
| `--nodi N` *(del SIMULATORE, comportamento CAMBIATO il 2026-09-26)* | **`--nodi 0` = NESSUN VUOTO: lo costruisce la SCENA.** Prima `a.nodi` era guardato **solo a flag `--semina-lam` spento**: acceso, il ternario andava in **saturazione** e `--nodi 0` chiedeva zero nodi ottenendone **455** *(misura 0, `M0a`)*. **NON e' byte-inerte per `--nodi 0` con `--semina-lam`** *(era l'unico caso rotto)*; **per ogni altro valore, e per `--nodi 0` a flag spento, il comportamento e' invariato di un bit.** E' **un'eccezione in meno**, non una legge in piu' (`STANDARD 10`): un valore aveva **due** significati. | serve la scena `(ii)` |

### Le opzioni del DRIVER `csv/_test_fork/_scena_video.py` *(nuove il 2026-09-26)*

| opzione | che cosa fa | DEFAULT, e se e' inerte |
|---|---|---|
| `--scena=NOME` | scegle la **scena** del simulatore *(il vocabolario si legge da `S.TESTS`, non si ricopia)*. Prima il driver **FISSAVA `N-MASSE`** in **due** punti, e la scena `(ii)` -- quella del **run base** -- non era raggiungibile da nessun comando | **`MASSE-COERENTI` dal 2026-09-26** *(decisione di Luca)*, **e NON e' byte-inerte:** `N-MASSE` con `--semina-lam` **RIFIUTA DI PARTIRE**, quindi il vecchio default era **un run che si ferma**. `N-MASSE` resta raggiungibile con `--scena=N-MASSE`, e li' rifiutera': e' il presidio delle scene pre-`A13`, non un difetto |
| `--nodi=N` | inoltra `--nodi` al simulatore | **non passato**, cioe' il default del simulatore. **Con `--scena=MASSE-COERENTI` il driver passa `0` e LO STAMPA**, invece di aggiungerlo in silenzio (`A9`); un `--nodi=` esplicito vince |
| `--seme=N` | inoltra `--seed` al simulatore. **Prima `--seed` non era MAI passato: ogni run del driver girava col seme 42**, e senza un seme variabile non esiste una barra fra semi (`P3` ne chiede almeno quattro) | **non passato**, cioe' **42 come prima**. E `SEME_EFFETTIVO` ora si legge da `a.seed`, non dalla firma della classe |

Tutti gli script di lancio includono esplicitamente `--sync`, sia nel ramo
Euleriano sia nelle varianti Velocity-Verlet. La schermatura è sempre attiva
(`SCHERMATURA=True`). `--plam` è mantenuto solo
per compatibilità con vecchi comandi: il suo valore viene ignorato. I valori
`P_LAM` e `LAM_MIN` non controllano più la dinamica.

Con `--sync` il campo materia e la sorgente metrica leggono gli snapshot del
passo precedente; senza flag resta il percorso storico. L'integratore fase e
il sottociclo metrico restano sequenziali in entrambi i casi.

Con `--chi-core` il segno usato nei canali collettivi viene calcolato nel core
locale da $|\Psi|^2$, dalla soglia $\rho_c$ e dalla portata schermata. `perc_chi`
resta la chiralità microscopica di nascita ed eredità. La legge è sperimentale
e va validata con confronto OFF/ON su più semi.

Con `--cs-dinamico` la velocità metrica locale usa la densità rispetto al solo
vicinato topologico. Il floor è emergente dalla saturazione locale
$CS_M/(1+\gamma\sqrt{|\Psi|^2})$, la transizione è liscia con `tanh`, la
velocità sugli archi è la media armonica dei due nodi e il ramo OFF conserva la
fisica storica.

Le campagne da ripetere con la versione corrente devono usare DB/output nuovi:
le cache `--sync-db` sono versionate per hash del codice e non vanno riutilizzate
tra configurazioni fisiche diverse. Vedi `REPORT_SESSIONE_2026-09-04.md` per lo
stato della sessione e il TODO dei test.

## 4-bis. Il referto di configurazione dei run — **nessun run parte senza**

*(decisione di Luca, 2026-09-24)*

Ogni run lanciato attraverso `csv/_test_fork/_scena_video.py` scrive nella **cartella del
run** due file:

| file | contenuto |
|---|---|
| **`CONFIGURAZIONE.txt`** | leggibile: i flag che l'argv ha **cambiato** rispetto al default, poi **tutti** i flag e le costanti di modulo |
| **`CONFIGURAZIONE.json`** | gli stessi dati, per gli strumenti |

**Cosa contiene**, e ogni voce c'e' per un motivo:

- **lo stato EFFETTIVO di tutti i flag di modulo, letto DAL MODULO dopo `_applica_flag`** —
  non il default scritto nel sorgente. **Sono due cose diverse:** `SPINORE_CORRETTO` ha
  default `False` e vale `True` in ogni run del fork, perche' il driver cabla
  `--spinore-corretto`. Chi legge il sorgente conclude il contrario di chi legge il run;
- **i due argv VERBATIM**, che **non sono lo stesso**: quello con cui e' stato invocato il
  processo, e quello passato al simulatore dopo che il driver ha tolto le proprie opzioni;
- **`sha1` dei byte grezzi** di simulatore e driver *(**non** `git hash-object`: trappola
  CRLF)*, il **seme**, `HEAD`, e **se l'albero di git e' pulito**.

**L'elenco dei flag non e' scritto a mano: viene dall'AST** — gli assegnamenti a livello di
modulo con nome maiuscolo, **`123`** al momento in cui scrivo. La lista a mano che il driver
stampava a video ne aveva **`24`**, e una lista a mano invecchia in silenzio.

> **DEFAULT: sempre attivo, e non si spegne.** Il driver **rifiuta di partire** se non riesce
> a scrivere il referto. **Non e' byte-inerte sulla fisica** perche' non tocca la fisica:
> legge il modulo e scrive due file. **Nessun flag**, per la stessa ragione per cui non ce
> l'hanno le correzioni di difetto (par.10): non e' una legge, e' un presidio.

**Il collaudo si gira da solo:** `python csv/_configurazione.py` — **`6/6`**, con due casi che
**devono** fallire e un terzo, `K6`, che verifica **dall'AST** che nel driver la scrittura
venga **dopo** `_applica_flag`. *(Letta prima, la tabella mostrerebbe i default: esattamente
la bugia che il referto esiste per impedire. E `K6` ha davvero fallito finche' il cablaggio
non c'era.)*

## 5. Varianti Velocity-Verlet

Per ogni script di esperimento è disponibile una copia con suffisso `_verlet`.
Le copie non modificano gli script originali: aggiungono `--verlet` ai comandi
e scrivono output distinti, così il confronto con il ramo Euleriano resta
possibile.

| Script originale | Variante Velocity-Verlet |
|---|---|
| `RunTutti.bat` / `RunTutti.bash` | `RunTutti_verlet.bat` / `RunTutti_verlet.bash` |
| `run_catena.bat` | `run_catena_verlet.bat` |
| `run_guscio.bat` | `run_guscio_verlet.bat` |
| `run_kfrange.bat` | `run_kfrange_verlet.bat` |
| `run_ordine_spin.bat` | `run_ordine_spin_verlet.bat` |
| `run_polo_maturo.bat` | `run_polo_maturo_verlet.bat` |
| `run_precessine.bat` | `run_precessine_verlet.bat` |
| `run_test_aperti.bat` | `run_test_aperti_verlet.bat` |
| `run_verso_chi.bat` | `run_verso_chi_verlet.bat` |
| `run_viriale.bat` | `run_viriale_verlet.bat` |
| `run_zetaloc.bat` | `run_zetaloc_verlet.bat` |

`run_differenza_verlet.bat` esegue un A/B diretto sullo stesso scenario:
un ramo senza flag (Eulero) e uno con `--verlet`. Le varianti sono esperimenti
numerici: eventuali riduzioni di oscillazione o miglioramenti di precessione
vanno misurati nei `diaglog`, su run lunghi e più semi.

Per isolare i due canali aggiuntivi della precessione sono disponibili anche
due script a **un solo run** ciascuno (seed 1, `sep=10`, 700 passi):

- `test_precessione_verso_chi.bat`: aggiunge solo `--verso-chi`;
- `test_precessione_ls_azim.bat`: aggiunge solo `--ls-azim`.

Producono dati distinti in `out_elast/` e log distinti in `log/`; non avviano
sei processi per test.

## 5.1 Test del nucleo elastico

Tre script dedicati usano `--verlet` e studiano il coefficiente storico
`ELAST_C=100` nella dinamica plastica di `d0`:

- `test_ridondanza.bat`: confronto `ELAST_C=100` contro `ELAST_C=0` su tre semi;
	ora configurato a 300 passi come test preliminare rapido;
- `test_elastico_300.bat`: copia separata per il test rapido a 300 passi, con
  output e DB dedicati; non modifica `test_ridondanza.bat`;
- `test_elastico_300_sep10.bat`: stesso test a 300 passi con `sep=10`;
- `test_elastico_700_sep10.bat`: variante a 700 passi con `sep=10`, output e
	DB distinti dal test da 300 passi;
- `test_sensibilita.bat`: scansione `ELAST_C=30/100/300` su due semi;
- `test_scala.bat`: confronto tra 3 e 6 masse a `ELAST_C=100`.

Gli output finiscono in `out_elast/` e i log in `log/`. Il coefficiente è una
sonda di test, non una legge derivata: il run breve da 300 passi mostra la
formazione ma non chiude il verdetto; quello lungo va basato su `m0_coer`,
`m0_coer_nucleo`, `m0_Lz`, `Lz_orb` e sulle metriche normalizzate.

I tre test usano la stessa catena completa su entrambi i rami/configurazioni:
`--verlet --sync --viriale --zeta-vir --pav-com --chi-basc --polo-maturo
--olon-part --calore-vett`. Cambia solo `--elast-c` nel test di ridondanza;
negli altri test cambia esclusivamente il valore scansionato o la scala del
numero di masse. `--sync-db` è infrastruttura: ogni seme e condizione ha un DB
separato per poter riprendere i run senza modificare la fisica.

## 6. Script Windows

Tutti i `.bat` vanno lanciati dalla cartella del progetto:

```text
run_nome.bat
```

Gli script aprono spesso più processi con `START`; al termine, i risultati
numerici si trovano nelle directory indicate dallo script. Gli MP4, CSV, log,
DB e cache sono ignorati da Git.

### `RunTutti.bat`

Avvia il riferimento generale per 2 e 3 masse. Confronta il caso standard con
le varianti scalare e `tau-d0` quando le righe A/B sono abilitate. Produce CSV,
diaglog, log e video di riferimento.

Leggi osservate: interferenza, saturazione, tempo proprio, torsione, mitosi,
metrica dinamica, schermatura `N_c`, spinore e diagnostica multimassa.

### `run_test_aperti.bat`

Avvia la configurazione combinata dei test aperti su tre semi:
`--sync --viriale --zeta-vir --pav-com --chi-basc`. Usa `--sync-db` e salva
periodicamente per permettere la ripresa.

Leggi osservate: aggiornamento sincrono, conversione viriale, freno anisotropo,
pavimento comovente, basculamento chirale, precessione `Lz_orb`, scala
comovente, guscio e olonomia.

### `run_catena.bat`

Esegue la catena progressiva `chi-basc → viriale → polo-maturo → olon-part`.
Serve a isolare quale ingrediente produce un verso coerente e se `Lz_orb`
accumula precessione. Le righe delle condizioni intermedie sono predisposte
per essere riattivate; il run configurato usa tre masse, `--sync` e calcio
vettoriale.

Leggi osservate: chiralità, twist dipolare, olonomia, partizione radiale/
tangenziale e precessione orbitale.

### `run_guscio.bat`

Testa se le chiralità `chi=-1` si dispongono nel guscio esterno rispetto alle
`chi=+1`. Usa tre semi e `--pav-com`; genera anche un video a camera fissa.

Colonne principali: `rchi_pos`, `rchi_neg`, `rchi_ratio` e `frac_chi_neg`.
Un valore `rchi_ratio > 1` è un segnale della separazione ipotizzata, non una
dimostrazione automatica.

### `run_kfrange.bat`

Confronta `--kfrange 0` con `--kfrange 0.03` su tre semi e due video. Isola il
canale di moto lungo le frange.

Misura primaria: `Lz_orb` nella finestra pre-collasso. Il valore `0.03` è una
sonda parametrica: l'eventuale risultato va indicato come **in verifica con
parametro libero**.

### `run_ordine_spin.bat`

Testa se lo spinore si ordina per domini dopo `--chi-basc`, usando tre masse e
un run lungo.

Leggi osservate: angolo medio dello spinore, dispersione dello spin, struttura
dei domini e possibile verso azimutale. L'accoppiamento SU(2) è già attivo nel
motore; questo script misura il suo eventuale ordine macroscopico.

### `run_polo_maturo.bat`

Confronta `--chi-basc` con `--chi-basc --polo-maturo`. Verifica se scegliere il
polo con torsione maggiore rompe il bilanciamento dei twist e rende coerente
il verso di `Lz_orb`.

### `run_precessine.bat`

Confronta tre condizioni: base, `--viriale`, `--viriale --zeta-vir`, tutte con
`--pav-com`. Il criterio non è solo visivo: si controllano `Lz_orb`, `rcom_*`,
`s2_medio` e il raggio finale prima del collasso.

### `run_verso_chi.bat`

Confronta il frame-dragging standard con `--verso-chi`, mantenendo
`--chi-basc`. Cerca un verso chirale stabile e un eventuale accumulo di
precessione orbitale.

### `run_viriale.bat`

Confronta la dinamica standard con `--viriale`, lasciando spento `K_FRANGE` in
entrambi i rami. Verifica se la conversione conservativa radiale/tangenziale
arresta il collasso a un raggio finito.

### `run_zetaloc.bat`

Confronta smorzamento fisso e `--zeta-loc`, lasciando spento `K_FRANGE`. Misura
se il rilascio del freno nella materia permette alla circolazione di
sopravvivere e se cambia `Lz_orb`.

## 7. Script Linux/macOS

### `RunTutti.bash`

È l'equivalente Unix del run generale. Esegue in parallelo batch e video per 2
e 3 masse, confrontando:

- calcio vettoriale contro scalare (`--calore-scal`);
- tempo plastico su `d` contro `d0` (`--tau-d0`);
- camera fissa nei video (`--giri 0`).

Avvio:

```text
bash RunTutti.bash
```

## 8. Lettura dei risultati

`test_circolazione_topologica.bat` produce inoltre le colonne passive
`n_cicli_topologici`, `corrente_arco_max`, `gradiente_rho_arco_media_assoluta`,
`circolazione_topologica_max`, `circolazione_topologica_rms` e
`circolazione_topologica_media`. Sono misure sul grafo e non dipendono
dall'embedding; non costituiscono ancora una forza dinamica.

### CSV compatto

Il CSV del batch riassume condensazione e interazione. Le colonne utili
includono distanza tra baricentri, densità centrale, ordine, guscio, picchi
nuovi e tracking di accrescimento/coppie.

### `diaglog`

Il `diaglog` è il registro principale per i test scientifici. Oltre a torsione,
fase, velocità, densità e metrica contiene:

- `ncrit_adattivo`, `rho_critica`;
- `lambda_eff_min`, `lambda_eff_med`, `lambda_eff_max`;
- `lambda_eff_ratio_med`, `rho_su_rhoc_max`;
- quantità per massa `m0_*`, `m1_*`, ...;
- interazioni `coer_01`, `cosphi_01`, `Lz_orb_01`, `dist_01`;
- misure di guscio, centro, olonomia e scala comovente.

Per la schermatura, il nucleo dovrebbe mostrare portata ridotta e un rapporto
`rho_su_rhoc_max` elevato, mentre le regioni sotto soglia dovrebbero restare
vicine a `LAM`. Questo è un criterio di lettura: la stabilità va verificata su
run lunghi e più semi.

## 9. Run lunghi e ripresa con DB

Per spezzare un batch lungo:

```text
python soliton_simulator.py --batch --nmasse 3 --sep 16 --seed 1 --passi 20000 --ogni 5 --sync-db out_test/db_s1.pkl --db-ogni 100 --csv out_test/cond_s1.csv --diaglog out_test/diag_s1.csv
```

Rilanciando lo stesso comando, il simulatore ricarica lo stato e completa i
passi mancanti. Il DB contiene l'hash del codice: se il codice cambia, il DB
viene rifiutato per evitare di mischiare fisiche diverse. Per ricominciare da
zero usare `--db-cleanup`.

## 9-bis. Costanti di modulo SENZA flag da riga di comando

Alcune leggi si accendono e si spengono da una **costante di modulo**, non da un'opzione: si
impostano **sul modulo** da uno script di rigiocata. E' voluto — non devono poter essere accese
per sbaglio da un comando.

| costante | default | cosa fa | byte-inerte al default? |
|---|:-:|---|---|
| `GRAV_BIFASE` | `True` | la legge gravitazionale bifase: il sito `S09_spinta_med` che scrive `d0` | — (e' il comportamento storico) |
| `MEM_MOTO` | `True` | **la scrittura della memoria del moto su `d0`**, cioe' il sito `S08_proj`. Spenta, `proj` resta calcolato *(il ramo della gravita' ne usa `len(proj)`)*, `mem_mot` resta aggiornato e il pavimento `P3` continua a girare: si toglie **solo** il contributo a `d0` | **si', MISURATO**: `206` campi identici e `0` diversi contro `_val600`, prodotto dal blob PRIMA del flag *(sigillo `T7`)* |
| ### **`MEM_FASE`** | ### **`False`** | ### **la scrittura della memoria del moto su `phi`**, cioe' il **trascinamento di fase** in `memoria_hebbiana_moto`. Acceso riproduce il comportamento storico; ### **spento (il DEFAULT) il sito NON scrive `phi`.** `mem_mot`, `proiezione_trasversale` e `shift_fase_dinamico` restano **calcolati**, e il taglio `pi/4` resta applicato: si toglie **solo** il contributo a `phi`. ### ⚠ **Toglie ANCHE il `% _dphi()`**, non solo la somma | ### ⛔ **NO, E IL DEFAULT NON E' IL COMPORTAMENTO STORICO:** spento ### **la fisica CAMBIA.** E' la fisica **decisa** *(Luca, 2026-10-04)*. **Acceso** e' byte-identico a `e2940b3c` *(sigillo `csv/_seal_fork/_sigillo_mem_fase.py`)* |
| `TRACCIA_D0` | `False` | i diciannove punti di traccia degli scrittori di `d0` | si' |

### ⛔ **E UNA COSA NUOVA IN QUESTO PARAGRAFO, dal 2026-10-05: `MEM_FASE` E' IL PRIMO
### FLAG IL CUI DEFAULT CAMBIA LA FISICA.**
Tutti gli altri qui nascono **OFF e inerti**, oppure **ON** *(il comportamento
storico)*. ### **`MEM_FASE` nasce OFF E TOGLIE UNA LEGGE**, perche' quella legge era
### **un artefatto dell'ordine dell'array** *(misurato: scartava il **`97.3%`** dei
contributi, rapporto dei moduli scartati/applicati **`36.2`**;
`doc/REFERTO_mem_hebb_verso_2026-10-05.md`)*.
### 📌 **LA CONSEGUENZA:** da quel commit, ### **ogni sigillo e ogni rigiocata che
ri-esegue il simulatore da' numeri diversi dai suoi referti** -- e non e' un difetto:
### **i referti sono legati al loro BLOB** *(par.6)*.

**⚠ `MEM_HEBB = False` NON e' il modo di spegnere la memoria del moto:** spegne l'**intera**
funzione, gravita' e coesione comprese. **Misurato: toglie cinque siti oltre la gravita'**
(`S08_proj`, `P3_dopo_proj`, `S12_coesione`, `P6`, `P7`).

## 10. Cosa non versionare

Il repository conserva codice, script e documentazione. Sono ignorati:

- tutti gli `*.mp4`, `*.avi`, `*.mov` e `*.mkv`;
- file CSV e log generati, salvo i risultati ELAST_C esplicitamente conservati;
- file pickle/NumPy generati;
- directory `out_*`, `log/` e `__pycache__/`.

La regola `*.mp4` vale in ogni sottocartella. I CSV di `out_elast/` e i log
`log/elast*.log` sono conservati per documentare i test ELAST_C; i DB `.pkl`
restano cache locali e non vengono versionati.

## ✅ PRIMA DI LAVORARE: I PRESIDI (un comando, una volta per clone)

```
git config core.hooksPath .githooks
```

Gli hook stanno in **`.githooks/`**, **tracciata da git** (`.git/hooks/` non viaggia col
repo). Rifiutano un commit che:

* tocca un referto **senza** toccare `RELAZIONE_PER_CLAUDE.md` (`P1-bis`);
* cambia una **legge** senza la sua **scheda** in `doc/REGISTRO_FISICA.md` (`REG-R`);
* aggiunge un **sigillo** che configura il modulo **a mano** invece di passare dal CLI (`P3`);
* scrive un **referto** senza dichiarare la **configurazione intera** (`P5`);
* prende **«il codice di prima» da `HEAD`** (`P8`), che diventa vuoto appena la cura e'
  committata.

Ogni rifiuto dice **cosa fare**, e l'eccezione si dichiara nel file
(`ESENTE-<Pn>: <motivo>`, col cancelletto) **piu'** una voce in
`doc/ESENZIONI_presidi.md` (`python csv/_hook_presidi.py --elenca`).
**Finche' il comando non e' dato i presidi non impediscono niente, e
`python csv/_hook_presidi.py` lo dice** (`A9`).

---

## ⚠ `--pav-com` È **INERTE** dal 2026-09-27 *(passo (b)1 di `ETC-PASSO`)*

| | |
|---|---|
| **cosa faceva** | rendeva **comovente** il pavimento di `d0` — `f·median(d0)` invece del muro assoluto `0.05` |
| **default** | `False`, **e da oggi il default non conta più**: il flag non fa niente in nessuno dei due stati |
| **byte-inerte a default spento?** | ### **è inerte in ENTRAMBI gli stati**, acceso o spento |
| **perché** | il pavimento che governava — `_floor_d0` e `_pav_d0` — **è stato ARCHIVIATO** in `csv/_archivio/_pavimenti_morti.py` *(tag `pre-archivio-pavimenti`)*, perché **col driver non eseguiva mai**: `_g_sm_pav_saltati = 15` su 15 chiamate, e la riga del pavimento **0 esecuzioni** su 3 passi *(copertura di riga con `settrace`)* |
| **non è stato TOLTO** | decisione 3 di Luca: **si conserva tutto**. Il driver lo passa ancora, e all'avvio **stampa che è inerte** invece di annunciare una legge che non applica |

> ### **E la garanzia sulle lunghezze NON se ne va con lui: è `LAM`**
> *(`--scala-min-passo`, `--semina-lam`, `--mitosi-2lam`, `_nasce`)*, **che non si tocca**.
> Misurato sui 16 stati del pilota: **`min(d) = 0.800000 = LAM` esattamente**, in ogni stato e ogni
> checkpoint, **0 archi sotto `LAM`**. Il pavimento vecchio, `0.05`, stava **16 volte più in basso**
> del minimo osservato: **non avrebbe potuto mordere nemmeno se fosse stato vivo.**
>
> **⚠ E cosa cambia davvero, dichiarato:** con **entrambi** `--scala-min` e `--scala-min-passo`
> **spenti** — una configurazione che **il driver non usa** — prima `d0` aveva un pavimento e ora
> **non l'ha più**. Non è una regressione nascosta: **è il senso dell'archiviazione**, e quel
> comportamento si ritrova nel tag e in `csv/_archivio/_pavimenti_morti.py`.

---

## ⚠ `--sync` è un **NO-OP ACCETTATO** dal 2026-09-27 *(passo (b)2 di `ETC-PASSO`)*

| | |
|---|---|
| **cosa prometteva** | l'**aggiornamento sincrono** (Jacobi invece di Gauss-Seidel): tutte le leggi leggono la fase dallo **snapshot di inizio passo** |
| **default** | `False`, **e da oggi non conta più**: il flag **non fa niente in nessuno dei due stati** |
| **byte-inerte?** | ### **sì, in entrambi gli stati** |
| **il flag resta accettato** | `--sync` **non fallisce**, e all'avvio **dichiara di non fare niente**. Decisione 3: **si conserva tutto** |
| **perché** | ### **il suo raggio era UNA legge su cinque.** Misurato nella FASE 0: **7** usi in `_passo_spinoriale`, **6** in `step`, e ### **ZERO** in `scuoti_vuoto`, `mitosi`, `rilassa_disegno`, `memoria_hebbiana_moto`. **Tutte e 56** le letture miste `t`/`t+1` misurate stavano **fuori** da quel raggio |
| **dove è finito** | `csv/_archivio/_sync_update.py`, tag **`pre-archivio-sync`** |
| **chi lo sostituisce** | la cura **`ETC-PASSO`**, che rende sincrono il **passo intero** |

> ### ⚠ **E cosa cambia davvero, dichiarato:** chi passava `--sync` **prima otteneva un
> comportamento diverso** — misurato: **19 grandezze su 23** differivano fra `--sync` acceso e
> spento. **Da oggi `--sync` non cambia più niente**, quindi **i run vecchi fatti con `--sync` non
> si confrontano con quelli nuovi senza dirlo.** Il comportamento di prima si ritrova nel tag.
>
> **Due flag con `SYNC` nel nome, due cose diverse:** `--sync-spinore` (`SYNC_SPINORE`) **non è
> toccato** e continua a funzionare.

---

## ⚠ `L_CONSERVA` è un **NO-OP ACCETTATO** dal 2026-09-28

| | |
|---|---|
| **cosa faceva** | rimuoveva la **rotazione rigida netta** introdotta dal rilassamento del disegno, pesata per `|Psi|²` |
| **default** | `False`, e **non ha nemmeno un flag CLI**: per accenderlo si **modificava il sorgente** |
| **byte-inerte?** | ### **sì, in entrambi gli stati** |
| **perché** | ### **il codice stesso lo marcava «ERRATA, NON usare»**: *«AZZERA tutta la rotazione rigida a ogni passo → distrugge la PRECESSIONE FISICA REALE»* *(`L_z ≈ −0.9`, verso coerente all'84 %)*. **Conservare `L` ≠ annullare la rotazione** |
| **e la ragione che l'ha fatto uscire adesso** | ### faceva **dichiarare il falso al TIPO** di `rilassa_disegno`: la catena `rilassa_disegno → _togli_rotazione_rigida → calcola_psi` le faceva scrivere `psi`, mentre il tipo `disegno` dice *«scrive solo `pos`»*. **Archiviandolo il tipo è vero per costruzione** |
| **dove è finito** | `csv/_archivio/_l_conserva.py`, tag **`pre-archivio-lconserva`** |
| **non è stato TOLTO** | decisione 3, e **lo dichiara all'avvio** insieme agli altri flag inerti accesi |

> ### ⚠ **E il ramo AGIVA, misurato PRIMA di toglierlo:** con `L_CONSERVA` acceso contro spento,
> ### **17 grandezze su 23 differivano.** **Non è una pulizia: è una decisione.**

## L'avviso `[flag-inerti]`

All'avvio, **se un flag inerte è ACCESO**, il simulatore lo dice e **nomina l'archivio**:
`L_CONSERVA` · `PAV_COM` · `SYNC_UPDATE`.
### **Un flag che non fa niente e che qualcuno accende è un'aspettativa tradita, non un dettaglio.**

**⚠ Il limite, dichiarato:** l'avviso legge le costanti **al momento della configurazione**. Chi le
imposta **dopo** *(per esempio uno strumento che le inietta a runtime, come `--flag=` di
`csv/_test_fork/_hashseed_prova.py`)* **non lo fa scattare** — e in quel caso è chi lancia che sa cosa
sta facendo.

## ⚠ `--maxnodi` **FERMA IL RUN** dal 2026-09-28 *(`MAX-NODI-FERMA`, primo pezzo di codice di `T3`)*

| | |
|---|---|
| **cosa fa** | e' la **GUARDIA DI MEMORIA** sul numero di puntatori: `MAX_NODI` |
| **DEFAULT** | ### **`4000000`** *(quattro milioni)*, **invariato** |
| **byte-inerte a default?** | ### **SI, ed e' sigillato:** `csv/_seal_fork/_sig_max_nodi.py`, **23 grandezze su 23 identiche** |

### **CHE COSA E' CAMBIATO:** prima, quando il numero di nodi arrivava al tetto, **tre siti
cambiavano la fisica in silenzio** e il run continuava:

| sito | che cosa faceva |
|---|---|
| `mitosi` | restituiva **ZERO NASCITE** -- e dai dati sembrava che la fisica avesse deciso cosi' |
| `semina` | **troncava** al numero che ci stava: si chiedevano `n` nodi, ne nascevano meno |
| canale di **Schwinger** | si **spegneva** |

### ➜ **Ora il run SI FERMA**, con `LimiteNodiSuperato` e un messaggio che dice **dove**, **quanti
nodi**, **quanti richiesti** e **di quanto** si e' superato il tetto.

> ### 📌 **E il commento della costante lo diceva GIA':** *«se lo fosse, la misura e' da rifare con
> piu' memoria, **non da troncare**»*. **L'intenzione era scritta e il codice faceva l'opposto** --
> la forma esatta che `A8` esiste per impedire.

**SE MORDE, CHE FARE:** si **rialza `--maxnodi`** e si rifa' la misura. ### **Non si tronca.**

**⚠ E non e' un tetto fisico** (`A11`): non protegge da un errore di fisica, protegge la RAM.
**In futuro va ELIMINATO** *(decisione di Luca, 2026-09-28)*.

## 🆕 `PSI-FLASH` **curato** dal 2026-09-28: la schermatura non si spegne più alla nascita

| | |
|---|---|
| **cosa c'era** | al passo di una nascita `mitosi` faceva crescere `n`, quindi `len(psi) < n`, quindi `lambda_nodi` restituiva `LAM` **per tutta la rete**: ### **la schermatura si spegneva in silenzio** |
| **quanto valeva** | `λ` da `~0.60` a **`0.80`**, `exp(-d/λ)` da `0.0655` a `0.1223`, ### **`\|psi\|` su di `1.62×` per TUTTI** *(non per il nato)*, e il pozzo da `130` a **`366`** |
| **la cura** | `mitosi` **ESTENDE** `psi` *(media dei genitori)* e `psi_spin` *(da `a`)* ai nati, ai **due** canali *(mitosi e Schwinger)*. Così ### **`len(psi) == n` sempre** |
| **e il presidio** | `len(psi) < n` in `lambda_nodi` ### **solleva `SchermaturaSpenta` e FERMA il run.** Se scatta, una strada nuova fa crescere `n` senza estendere `psi` — e **prima cambiava la fisica in silenzio** |
| **NESSUN FLAG NUOVO** | ### **non c'è niente da accendere: è una cura strutturale.** `SCHERMATURA` e `LAM` restano come erano |

### ⚠ **Che cosa NON è cambiato, e va detto:** il ripiego della **ricorsione** in `lambda_nodi`
*(`_calcolo_schermatura`)* ### **RESTA**, perché non è un difetto: è la **definizione** — *la massa
critica si calcola sul **nucleo nudo**, perché la soglia che accende la schermatura non può dipendere
dalla schermatura stessa*. **Ora è contata** *(`_g_scherm_ricorsione`)*: **sette per passo**.

> ### 📌 **E il `2.6×` sul pozzo non era fisica:** era l'assenza della schermatura. **Ogni numero
> misurato in un passo CON nascite, prima di questa cura, viene da un campo gonfiato di `~1.6×`.**


---

## 🆕 `Z43` CURA (2) dal 2026-10-05: **il tempo proprio viene da `cs`**, e **DUE flag diventano INERTI**

**LA LEGGE NUOVA:** `r = cs_nodo(t-1) / CS_M` *(esponente `p = 1`, <<orologio a luce>>)*.
**Prima** `r` veniva dalla **frequenza d'interferenza della fase**, normalizzata sulla
**mediana globale** di `|f|`. *(Decisione di Luca; scheda in `doc/REGISTRO_FISICA.md` ⑤;
ramo archiviato in `csv/_archivio/_rami_off_z43_cura2.py`, tag `pre-z43-cura2-r-da-cs`.)*

### ⚠ **`--tauloc` CAMBIA SIGNIFICATO, e il default NON cambia**

| | |
|---|---|
| **cosa faceva** | era **l'AMPIEZZA** della dilatazione: `r = 1 + TAU_LOC*(r_norm - 1)` |
| **cosa fa da oggi** | e' **solo un INTERRUTTORE**: `TAU_LOC == 0.0` → orologio **globale** *(`r = None`)*; qualunque altro valore → la legge `cs/CS_M`, **che non lo legge** |
| **default** | `1.0`, **invariato**, e il driver lo passa cosi' |
| **byte-inerte a default?** | ### **SI', ed e' misurato dall'ARITMETICA:** a `TAU_LOC = 1.0` la forma vecchia era `1 + 1.0*(x - 1) = x` — ### **un PASSANTE.** Quindi la cura **non toglie un'ampiezza in uso**: toglie **una manopola che valeva `1`** *(`A1`)* |
| **⚠ e che cosa cambia DAVVERO** | con `--tauloc` **diverso da `0` e da `1`** — una configurazione che **il driver non usa** — prima il valore **scalava** la dilatazione e ora ### **non fa piu' niente.** Non e' una regressione nascosta: e' il senso della cura, e si ritrova nel tag |

### ⚠ **`--ritmo-wrap-2pi` e `--tempo-proprio-orientato` sono INERTI dal 2026-10-05**

| | |
|---|---|
| **cosa facevano** | `--ritmo-wrap-2pi`: la cura **`D34`**, il wrapping su `2pi` *(invece di `4pi`)* della differenza di `np.angle` dentro `ritmo()`. `--tempo-proprio-orientato`: teneva il **SEGNO** di `f` invece del modulo |
| **default** | `False` entrambi; **il driver accende `--ritmo-wrap-2pi`** e non accende l'altro. **Da oggi il default non conta piu'**: non fanno niente in nessuno dei due stati |
| **byte-inerte a default spento?** | ### **sono inerti in ENTRAMBI gli stati**, acceso o spento |
| **perche'** | ### **agivano SOLO sulla fase dentro `ritmo()`**, e `r` **non legge piu' la fase**: non c'e' piu' niente da avvolgere ne' da orientare. Censito: fuori da `ritmo()` restavano **solo** la `global`, l'assegnazione dal CLI e *(per `--tempo-proprio-orientato`)* un `print` d'avviso |
| **non sono stati TOLTI** | ### **toglierli sarebbe ESTENDERE LA CURA DA SOLI** *(par.2)*. Restano **accettati dal CLI**, e la loro sorte e' **una decisione di Luca** |

> ### ⚠ **E `D34` ERA UNA CURA SIGILLATA** *(`csv/_seal_fork/_sigillo_ritmo_wrap.py`, 4/4,
> piu' la prova a 600 passi `Z123`)*. ### **La sua misura resta vera** — diceva che un wrap su
> `4pi` applicato a una differenza di `np.angle` *(periodo `2pi`)* e' **l'identita'**, con
> `max|w4(a) - a| = 0.000e+00` su 100 001 punti. ### **Ma la legge che curava non c'e' piu':
> non e' il sigillo a essere sbagliato, e' il suo OGGETTO a essere uscito.**

> ### 📌 **E un terzo sigillo diventa STORICO:** `csv/_seal_fork/_sigillo_anello.py`
> **asserisce che `step()` PROMUOVA il gauge `_med_f_prec`.** Da questa cura **FALLISCE a
> `HEAD`, e DEVE.** ### **Si rigira AL SUO COMMIT**, come il par.6 prescrive — **un sigillo
> non si giudica su un codice che non ha sigillato.**
