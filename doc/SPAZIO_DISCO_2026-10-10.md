# 💾 **LO SPAZIO SU DISCO — che cosa occupa, e che cosa LASCIANO i collaudi**

> ### ⛔ **CONGELATO** *(la forma dichiarata il `2026-10-10`: `csv/_forma_referti.py`)*: questo e- un ### **REPERTO**, cioe- ### **che cosa si e- misurato A UN ISTANTE** — ### **la CI NON lo rigenera**, e il presidio verifica ### **il suo BLOB**. ### ⭐ **E QUI E- L-UNICA FORMA ONESTA:** lo spazio libero ### **cambia da un minuto all-altro**, e un `VIVO` fallirebbe ### **un minuto dopo averlo scritto.**

*(**Generata** da `csv/_spazio_disco.py`. Le quattro domande di Luca del 2026-10-10.)*

> ## ⛔ **LA RISPOSTA IN UNA RIGA: `C:` E- PIENA AL `99.3%`, e il repo NON E- LA CAUSA.**
> Il repo pesa ### **9.3 GB** e il `%TEMP%` ### **1.5 GB**: insieme ### **10.8 GB su 472 occupati**, cioe- ### **il 2.3% di cio- che riempie il disco.**

## `1` I DISCHI

| disco | nome | totale | libero | usato | uso |
|---|---|---|---|---|---|
| **`C:`** | Windows | 475.1 GB | ### **3.17 GB** | 471.9 GB | ### **99.3%** |
| **`E:`** | Intenso | 238.5 GB | ### **232.39 GB** | 6.1 GB | ### **2.5%** |

## `2` CHE COSA OCCUPA DENTRO IL REPO

**Il repo in tutto: `9.3` GB, `6068` file.**

| | MB | che cos-e- |
|---|---|---|
| **`csv/`** | ### **5184** | gli output dei run dell-era `1` |
| **`.git/`** | ### **3653** | la storia |
| **`db/`** | ### **653** | i database dei run |
| **`doc/`** | ### **21** | i documenti |
| **`db_era2/`** | ### **0** | il database dell-era `2` |
| **`primo_ordine/`** | ### **0** | il codice dell-era `2` |
| **`proto_primo_ordine/`** | ### **4** | il banco del prototipo |

### ⭐ **E LA RISPOSTA STA NELLE ESTENSIONE, non nelle cartelle:** dentro `csv/` il peso e- ### **tutto in tre formati di uscita.**

| estensione in `csv/` | MB |
|---|---|
| `.gz` | 2903 |
| `.pkl` | 1182 |
| `.npz` | 641 |
| `.csv` | 170 |
| `.py` | 115 |
| `.pyc` | 73 |
| `.json` | 58 |
| `.png` | 16 |

**I `.pkl` in tutto il repo: `104` file, `1835` MB — e ### **`0` sono TRACCIATI in git**.** ### ✅ **E- cio- che `CLAUDE.md` par. `6` pretende** *(<<i `.pkl` non si committano: il dato E- il comando che lo produce>>)*: sono ### **rigenerabili**, e cancellarli ### **non perde niente che il repo non sappia rifare.**

**E gli altri due formati, con lo stesso stato:** `.gz` ### **`87` file, `2903` MB**; `.npz` ### **`120` file, `641` MB**.

### LE `15` CARTELLE PIU- GROSSE *(fino al terzo livello)*

| | cartella | MB |
|---|---|---|
| `1` | `csv/` | 5184 |
| `2` | `.git/` | 3653 |
| `3` | `csv/_test_fork/` | 3575 |
| `4` | `csv/_seal_fork/` | 1106 |
| `5` | `db/` | 653 |
| `6` | `csv/_test_fork/_ab_D/` | 351 |
| `7` | `csv/_test_fork/_fin_A/` | 272 |
| `8` | `csv/_test_fork/_gvideo/` | 271 |
| `9` | `csv/_test_fork/_g2m/` | 194 |
| `10` | `csv/_test_fork/_d34_ritmo_wrap/` | 174 |
| `11` | `csv/_test_fork/_g4_riferimento/` | 174 |
| `12` | `csv/_test_fork/_val600/` | 174 |
| `13` | `csv/_test_fork/_g4bis_senza_blocco/` | 174 |
| `14` | `csv/_test_fork/_g4_senza_memmoto/` | 174 |
| `15` | `csv/_test_fork/_run_K/` | 173 |

### I `10` FILE PIU- GROSSI

| | file | MB |
|---|---|---|
| `1` | `.git/objects/pack/loose-66e69bc987d83681b22236fa26d38d596c4e8f35.pack` | 2878.6 |
| `2` | `.git/objects/pack/loose-58a2f6d75a23e0af4335f5de54c3ee6efbce69fa.pack` | 570.9 |
| `3` | `csv/_seal_fork/_c1_semina/driver/frame_20.pkl` | 53.3 |
| `4` | `csv/_test_fork/_gvideo/frame_400.pkl` | 46.7 |
| `5` | `csv/_seal_fork/_sig_drv_B/frame_12.pkl` | 46.5 |
| `6` | `csv/_test_fork/_gvideo/frame_375.pkl` | 46.4 |
| `7` | `csv/_test_fork/_gvideo/frame_270.pkl` | 45.3 |
| `8` | `csv/_test_fork/_gvideo/frame_190.pkl` | 44.7 |
| `9` | `csv/_test_fork/_gvideo/frame_115.pkl` | 44.3 |
| `10` | `csv/_seal_fork/_sig_flag_driver/run/frame_1.pkl` | 43.6 |

## `3` CHE COSA LASCIANO I COLLAUDI NEL `%TEMP%`

**`C:\Users\lpeano\AppData\Local\Temp`, `1492` MB in tutto.**

| prefisso | cartelle | MB | file | di cui `read-only` | dalla | alla | chi lo crea |
|---|---|---|---|---|---|---|---|
| `stage_*` | ### **0** | 0 | 0 | ### **0** | - | - | `csv/_stage.py` `controlla()`: la copia dell-INDICE da validare |
| `repo_*` | ### **24** | 0 | 120 | ### **120** | 2026-10-10 12:40 | 2026-10-10 16:37 | `csv/_stage.py` `collaudo()`: il repo USA-E-GETTA del collaudo |
| `st_*` | ### **0** | 0 | 0 | ### **0** | - | - | `csv/_stage.py` `collaudo()`: la copia dello stage del repo usa-e-getta |
| `sol_*` | ### **0** | 0 | 0 | ### **0** | - | - | i CLONI della verifica (`clone.sh`): li creo io a mano, non un collaudo |
| `tmp*` | ### **61** | 97 | 124 | ### **0** | 2026-10-05 23:40 | 2026-10-06 18:20 | `tempfile.mkdtemp()` SENZA prefisso: non si puo- attribuire a un chiamante |

> ### ⛔ **E LE `repo_*` SONO UN DIFETTO MIO, NON UN RESIDUO INNOCENTE.**
> `csv/_stage.py` le cancella in un `finally` con `shutil.rmtree(dove, ignore_errors=True)` — ### **e su Windows non ci riesce**, perche- `git` scrive i suoi oggetti ### **in sola lettura** *(`-r--r--r--`)* e `rmtree` non li tocca. ### ⚠ **`ignore_errors=True` SILENZIA il fallimento**, quindi ### **ogni giro del collaudo ne lascia una e nessuno lo dice** — e il numero di cartelle e- ### **il numero di volte che il collaudo e- girato.**

## `4` IL COMANDO CHE HA FALLITO, E IL MESSAGGIO

**Il comando:** `python csv/_stage.py --collaudo`, lanciato da `python primo_ordine/collauda.py` *(che lo chiama con `subprocess.run([sys.executable, "csv/_stage.py", "--collaudo"], cwd=RADICE, capture_output=True)`)*, su un clone pulito di `65983ee`.

**Le righe della suite, copiate dalla sua uscita:**

```
i controlli sullo STAGE e non sul disco solo-CI        58.69  ### FALLISCE (codice 1)
i controlli sullo STAGE e non sul disco solo-CI         6.69  ### FALLISCE (codice 1)
   i controlli sullo STAGE e non sul disco `csv/_stage.py --collaudo` -> codice 1
```

**E rigirato a mano col disco pieno, dice QUALI bracci cadono:**

```
  ### e il modo RAPIDO passa (e- quello del `pre-commit`)       ### FALLISCE
  sul disco: i controlli del contenuto passano SULLO STAGE      ### FALLISCE
  ### il collaudo ha MATERIA: le due liste non sono vuote       PASSA
  ### il caso SANO: tutto committato, il controllo PASSA        PASSA
  ### (a) DEVE scattare: `b` in stage e `a` SOLO SUL DISCO      PASSA
  ### e SUL DISCO lo stesso caso PASSA                         PASSA
  ### (b) entrambi in stage: il controllo PASSA                 PASSA
  IL COLLAUDO DELLO STAGE: 5 su 7   ### CI SONO BUCHI
```

### ⭐ **E I DUE BRACCI CHE CADONO SONO ESATTAMENTE I DUE CHE ESPORTANO L-INDICE DEL REPO VERO** *(`~290` MB per copia)*, mentre ### **i quattro in sandbox passano** *(il repo usa-e-getta e- di `1` MB)*. ### **Non e- una coincidenza: e- la firma dello spazio che manca.**

> ### ⛔ **IL MESSAGGIO DI `git` NON SI VEDE DA NESSUNA PARTE, E QUESTO E- IL SECONDO DIFETTO.**
> `esporta()` lo restituisce *(`### git checkout-index e- fallito: <stderr>`)*, ma ### **il braccio del collaudo stampa solo la nota e BUTTA la lista degli errori**, e `collauda.py` ### **butta l-uscita del figlio** *(`capture_output=True`, e il contenuto non viene letto)*. ### ⚠ **Quindi un rosso d-AMBIENTE e un rosso da DIFETTO sono indistinguibili**, ed e- per questo che la diagnosi e- costata ### **tre corse da tre minuti.**

**L-unico messaggio del sistema che ho catturato alla lettera** e- quello di `tail` nello stesso istante, e dice la causa: ### **`tail: write error: No space left on device`.**

### ⛔ **E QUELLO DI `git` NON LO RICOSTRUISCO A MEMORIA:** per averlo alla lettera bisogna ### **rifare il caso con il disco pieno**, e il mandato dice ### **di non toccare niente e aspettare.**

