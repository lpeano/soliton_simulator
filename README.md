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
| `--verso-chi` | aggancia il frame-dragging al verso chirale stabile | A/B del verso |
| `--olon-part` | include twist coerente e curl nella partizione tangenziale | da usare con viriale/polo |
| `--ls-azim` | ricava il verso tangenziale da radiale × spinore | da usare con `--viriale` |
| `--sync` | aggiorna il ponte fase→metrica dallo snapshot iniziale del passo | test Jacobi/Gauss-Seidel |
| `--kfrange X` | aggiunge il canale di moto lungo le frange | sonda con parametro, non legge dimostrata |
| `--scala B` | coarse-graining: un solitone rappresenta `B` solitoni fini | cambio di scala |
| `--sync-db FILE` | salva o ricarica lo stato versionato | esecuzioni spezzate |

La schermatura è sempre attiva (`SCHERMATURA=True`). `--plam` è mantenuto solo
per compatibilità con vecchi comandi: il suo valore viene ignorato. I valori
`P_LAM` e `LAM_MIN` non controllano più la dinamica.

## 5. Script Windows

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

## 6. Script Linux/macOS

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

## 7. Lettura dei risultati

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

## 8. Run lunghi e ripresa con DB

Per spezzare un batch lungo:

```text
python soliton_simulator.py --batch --nmasse 3 --sep 16 --seed 1 --passi 20000 --ogni 5 --sync-db out_test/db_s1.pkl --db-ogni 100 --csv out_test/cond_s1.csv --diaglog out_test/diag_s1.csv
```

Rilanciando lo stesso comando, il simulatore ricarica lo stato e completa i
passi mancanti. Il DB contiene l'hash del codice: se il codice cambia, il DB
viene rifiutato per evitare di mischiare fisiche diverse. Per ricominciare da
zero usare `--db-cleanup`.

## 9. Cosa non versionare

Il repository conserva codice, script e documentazione. Sono ignorati:

- tutti gli `*.mp4`, `*.avi`, `*.mov` e `*.mkv`;
- CSV, log e file pickle/NumPy generati;
- directory `out_*`, `log/` e `__pycache__/`.

La regola `*.mp4` vale in ogni sottocartella. I risultati importanti vanno
riassunti nella documentazione o conservati fuori dal repository.
