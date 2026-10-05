# LE ESENZIONI DICHIARATE AI PRESIDI — **generato**

*(`csv/_hook_presidi.py --elenca`. Un'esenzione che NON compare qui **fa fallire il
commit**: cosi' non se ne accumulano di invisibili.)*

| file\|presidio | motivo dichiarato |
|---|---|
| `csv/_analisi_lettori_indice.py|H-P5` | non importa il simulatore e non lo fa girare. Legge sorgenti e conta. |
| `csv/_ancore_prima.py|H-P5` | strumento di analisi STATICA. Non importa il simulatore e non lo fa girare: |
| `csv/_archivio_relazioni.py|H-P5` | non importa il simulatore e non lo fa girare. Divide un documento per giorno. |
| `csv/_collaudo_criterio_zero.py|H-P5` | non importa il simulatore e non lo fa girare. E' un collaudo di un CRITERIO |
| `csv/_collaudo_istruzioni.py|H-P5` | non importa il simulatore e non lo fa girare. Collauda una sezione di documentazione. |
| `csv/_collaudo_lista_chiusa.py|H-P5` | non importa il simulatore e non lo fa girare. Collauda un generatore di documenti. |
| `csv/_collisioni_id.py|H-P5` | non importa il simulatore e non lo fa girare. Conta occorrenze in documenti. |
| `csv/_confronto_pds.py|H-P5` | non importa il simulatore e non lo fa girare. Confronta due documenti. |
| `csv/_controlli_riordino.py|H-P5` | non importa il simulatore e non lo fa girare. Conta righe e cerca stringhe. |
| `csv/_indice_id.py|H-P5` | non importa il simulatore e non lo fa girare. Valida un TSV. |
| `csv/_indice_riordino.py|H-P5` | non importa il simulatore e non lo fa girare. Aggiunge righe a un TSV. |
| `csv/_inventario_lettori_id.py|H-P5` | non importa il simulatore e non lo fa girare. Classifica script per contenuto. |
| `csv/_letture_rho_s.py|H-P5` | strumento di analisi STATICA. Non importa il simulatore e non lo fa girare: |
| `csv/_lista_chiusa.py|H-P5` | non importa il simulatore e non lo fa girare. Legge un TSV e scrive un documento. |
| `csv/_osservabile_p1.py|H-P5` | la configurazione si dichiara solo quando si COSTRUISCE una scena (`--scena`), e |
| `csv/_patch_cura2_strutturale.py|H-P5` | non importa il simulatore e non lo fa girare. Riscrive un sorgente per AST. |
| `csv/_patch_d32_nomi.py|H-P5` | non importa il simulatore e non lo fa girare. Rinomina variabili in un sorgente. |
| `csv/_patch_default_scena.py|H-P5` | non importa il simulatore e non lo fa girare. Sostituisce due default nel driver. |
| `csv/_patch_scena_ii.py|H-P5` | non importa il simulatore e non lo fa girare. Sostituisce testo in due sorgenti. |
| `csv/_presidio_commenti_flag.py|H-P8` | legge `HEAD:soliton_simulator.py`, ma **NON come «il codice prima di una |
| `csv/_presidio_commenti_flag.py|H-P5` | strumento di analisi STATICA. Non importa il simulatore e non lo fa girare: legge |
| `csv/_presidio_indice.py|H-P5` | non importa il simulatore e non lo fa girare. E' un presidio su documenti. |
| `csv/_presidio_righe.py|H-P5` | non importa il simulatore e non lo fa girare. Conta le righe di un documento. |
| `csv/_punto_della_situazione.py|H-P5` | non importa il simulatore e non lo fa girare. Legge un TSV e `git log`. |
| `csv/_regole_proposta.py|H-P5` | non importa il simulatore e non lo fa girare. Legge documenti e ne scrive uno. |
| `csv/_rinomina_collisioni.py|H-P5` | non importa il simulatore e non lo fa girare. Rinomina etichette in due documenti. |
| `csv/_rinomina_hook.py|H-P5` | non importa il simulatore e non lo fa girare. Rinomina etichette in sorgenti. |
| `csv/_rinomina_hook.py|H-P8` | la stringa `HEAD:soliton_simulator.py` qui dentro NON e' un'ancora al codice di |
| `csv/_riordino_fatti.py|H-P5` | non importa il simulatore e non lo fa girare. Sposta prosa fra due documenti. |
| `csv/_riordino_sposta.py|H-P5` | non importa il simulatore e non lo fa girare. Sposta prosa fra documenti. |
| `csv/_riordino_storia.py|H-P5` | non importa il simulatore e non lo fa girare. Archivia prosa da un tag di git. |
| `csv/_seal_fork/_sigillo_mem_fase.py|H-P3` | il flag `MEM_FASE` NON HA un'opzione da riga di comando, DI PROPOSITO (README.md par. 9-bis: <<si impostano SUL MODULO da uno script di rigiocata ... non devono poter essere accese per sbaglio da un comando>>), come MEM_MOTO e MEM_MOTO_TUTTO. Quindi impostarlo sul modulo E' IL MODO PRESCRITTO, non un aggiramento del CLI: il sigillo DEVE poter confrontare i due stati del flag nello stesso blob. La SCENA passa TUTTA dal CLI, e la configurazione INTERA si DICHIARA. |
| `csv/_seal_fork/_sigillo_mem_fase.py|H-P8` | le DUE occorrenze di `HEAD` stanno nella DOCSTRING di braccio0(), e dicono ESATTAMENTE IL CONTRARIO di cio' che il presidio teme: spiegano perche' il *prima* NON si prende da HEAD~1 ma dal PADRE DEL COMMIT CHE HA CAMBIATO IL SIMULATORE. Il hook cerca la sottostringa `HEAD` e la trova nella prosa. POTEVO SCRIVERE `@~1`, che in git e' lo stesso e passa il controllo: NON LO FACCIO, sarebbe disarmare un presidio cambiando le parole. E' la SECONDA volta per la stessa ragione (la prima e' _sigillo_veleno_keep.py, 92ecb04). Il braccio 0 VERIFICA il *prima*: se fosse sbagliato, il blob non tornerebbe. |
| `csv/_sposta_standard10.py|H-P5` | non importa il simulatore e non lo fa girare. Sposta prosa fra due documenti. |
| `csv/_test_fork/_mem_hebb_verso.py|H-P3` | la scena passa TUTTA dal CLI (`nmasse` e `sep` da `argv`), e la configurazione INTERA si DICHIARA (`_cli_flag.dichiara_configurazione`). La COPIA PATCHATA serve perche' `ii`, `jj`, `dirarc`, `I`, `Imed` e `proj` vivono SOLO dentro `memoria_hebbiana_moto`: ricostruirli fuori sarebbe una SECONDA scrittura della stessa legge, cioe' le <<due leggi>> che `9-ter` vieta. |
| `csv/_test_fork/_z43_tempo_proprio.py|H-P3` | la scena passa TUTTA dal CLI (`nmasse` e `sep` da `argv`), e la configurazione INTERA si DICHIARA (`_cli_flag.dichiara_configurazione`). La COPIA PATCHATA serve perche' `psi_spin`, `_psi_spin_prec` e `_med_f_prec` vanno letti ESATTAMENTE dove `ritmo()` li legge, e `I`/`w`/`cs_nodo` dove il settore metrico li calcola: ricostruirli fuori sarebbe una SECONDA scrittura delle stesse leggi, cioe' le <<due leggi>> che `9-ter` vieta. |
| `csv/_titoli_brevi.py|H-P5` | non importa il simulatore e non lo fa girare. Accorcia titoli in un TSV. |
| `csv/_vista_smistamento.py|H-P5` | non importa il simulatore e non lo fa girare. Legge due TSV e scrive un documento. |
| `csv/_archivio/_indice_id_importatore.py|H-P5` | non importa il simulatore e non lo fa girare. Genera due indici da documenti. |
| `csv/_archivio/rami_off_cura2.py|H-P5` | e' un ARCHIVIO. Non importa il simulatore, non gira, non scrive referti. |
| `csv/_seal_fork/_c1_col_segno.py|H-P5` | legge JSON gia' scritti e non fa girare il simulatore. La configurazione di quei dati |
| `csv/_seal_fork/_sigillo_veleno_keep.py|H-P8` | il *prima* NON viene da `HEAD`, viene dal PADRE -- `git rev-parse HEAD~1`, |
| `csv/_seal_fork/_sigillo_veleno_keep.py|H-P3` | i due moduli si caricano TUTTI E DUE passando dal `_cli()` del simulatore |
| `csv/_seal_fork/_veleno_keep_patch.py|H-P3` | non importa il simulatore e non lo fa girare. Scrive un file. |
| `csv/_test_fork/_calcio_sotto_scambio.py|H-P3` | la frazione del CONTROLLO si cambia su una COPIA DEL SORGENTE, non |
| `csv/_test_fork/_confronto_blob_misure.py|H-P5` | non importa il simulatore e non lo fa girare. Legge due referti json |
| `csv/_test_fork/_confronto_previsione.py|H-P5` | non costruisce nessuna scena e non carica il simulatore: legge i `json` di un run |
| `csv/_test_fork/_esponenti_figli.py|H-P5` | legge JSON gia' scritti, non fa girare il simulatore. La configurazione di quei dati |
| `csv/_test_fork/_massa_id.py|H-P5` | non costruisce nessuna scena e non carica il simulatore. Il `--collaudo` gira su un |
| `csv/_test_fork/_massa_id_fisso.py|H-P5` | non costruisce nessuna scena e non carica il simulatore. Legge gli `.npz` di un run |
| `csv/_test_fork/_partecipazioni.py|H-P5` | legge le coorti e i `misura.json` di un run che ha gia' dichiarato la propria |
| `csv/_test_fork/_scomposizione_tratti.py|H-P5` | non costruisce nessuna scena e non carica il simulatore. Legge i `misura.json` di un |
| `csv/_test_fork/_tetto_causale_tempo.py|H-P3` | la misura NON configura il modulo a mano -- la scena passa TUTTA dal CLI |
| `csv/_test_fork/_tratti_cammino.py|H-P5` | non costruisce nessuna scena e non carica il simulatore. Il `--collaudo` gira su |
| `csv/_test_fork/_v1_ripetizione.py|H-P5` | confronta due `misura.json` gia' prodotti, ciascuno da un run che ha dichiarato la |
| `csv/_test_fork/_veleno_archi_keep.py|H-P3` | la scena passa TUTTA dal CLI (`nmasse` e `sep` da `argv`). La COPIA PATCHATA |
| `csv/_test_fork/_verifica_flag_accesi.py|H-P5` | non importa il simulatore e non lo fa girare. LEGGE i referti committati e |
| `csv/_test_fork/_video_scena.py|H-P5` | non costruisce nessuna scena e non carica il simulatore: legge i fotogrammi `.npz` |

```
esenzioni dichiarate   58
```
