# INVENTARIO DEGLI STRUMENTI — quali script producono i numeri di questo programma

> **2026-09-16.** Branch `fork-su2`. Blob del simulatore: **`08784685`**.
> **Perche' esiste:** i numeri di questo repo non escono dal simulatore ma da **undici script**, e
> finora l'unico modo di sapere **quale** script ha prodotto **quale** numero era leggere i commit
> in ordine. Qui c'e' l'elenco, con **il blob di ogni script** — perche' un commit puo' mentire, un
> blob no (§2.6), e **vale per i diagnostici quanto per il simulatore**.
>
> **Si aggiorna quando uno strumento nasce, cambia o viene sigillato**, nello stesso commit (§5-bis).
> **Non e' una cronaca**: se uno script e' qui, e' perche' un numero committato dipende da lui.

---

### `csv/_seal_fork/_sigillo_mem_moto_tutto.py` — **SIGILLO di `MEM_MOTO_TUTTO`** *(`G4-bis`)*

```
python csv/_seal_fork/_sigillo_mem_moto_tutto.py
```
**Cosa misura:** che `MEM_MOTO_TUTTO` sia **byte-inerte acceso** *(`T9`, 120 passi contro
`_val600`)* e che spento spenga **tutti e quattro** i punti della memoria del moto — la
scrittura su `d0` *(`T1`-`T3`)*, l'aggiornamento di `mem_mot` *(`T4`)* e **lo spostamento di
fase su `phi`** *(`T5`)*. **`T6` misura PERCHE' `G4-bis` esiste:** col solo `MEM_MOTO=False`,
`mem_mot` resta viva e `phi` identica al braccio acceso.
**⚠ Il criterio guarda `d0` E `phi` E `mem_mot`:** un criterio sul solo `d0` sarebbe
**cieco sul quarto punto**, e il collaudo `K7` e' il caso che lo dimostra.
**Blob dell'ultimo giro:** *(da riempire dopo il primo giro)* · **simulatore `21e3a3dc`**.
**Opzioni:** `--passi=N` *(default 3)* · `--senza-t9` *(salta la byte-inerzia: la marca
FAIL, non la salta in silenzio)*.

## 0. LA REGOLA CHE QUESTO FILE RENDE VERIFICABILE

> **Un diagnostico che contamina la fisica non misura il sistema: misura se stesso** (§2.3).
> Percio' ogni riga qui sotto porta **il suo sigillo di purezza** — non «e' puro», ma **quale file
> lo dimostra e con che numero**. Dove la colonna dice *«nessuno»*, quel numero **non e'
> certificato puro**, e va detto da chi lo cita.

---

## 1. GLI STRUMENTI IN USO OGGI (2026-09-16)

| script | blob | righe | cosa produce | sigillo di purezza |
|---|---|---|---|---|
| **`csv/_test_fork/_osserva_vuoto.py`** | `54faf42d` | 485 | **il driver della campagna.** Avvolge `Rete.step` e legge gli array **gia' committati**. MISURE A (`chi`), B (`\|<n>\|`), C (`theta`), D (dispersione di `r`), E (autocorrelazione), **F** (le tre pendenze trasversali), **G** (ingredienti FDT) | **`_sigillo_osservatore.py` 6/6 PASS** (2026-09-16, `d7bc21c`): `max\|A-B\| = 0.000e+00`, nodi **3020 = 3020** |
| **`csv/_test_fork/_sigillo_osservatore.py`** | `64b2c894` | 156 | il sigillo qui sopra: O1.0, O1, O2, O3a-c | — *(e' lui il sigillo)* |
| **`csv/_test_fork/_tracing_omega.py`** | `2d12f6e7` | 438 | **`ingredienti(S, net)`**, la ricostruzione della catena di `omega` su **copia profonda** con restore dell'RNG. **MISURA F la RIUSA invece di riscriverla** | sigillo interno `--sigillo`, piu' O1 sopra (che esercita la copia profonda **dentro** un run vero) |
| **`csv/_test_fork/_verdetto_S_R.py`** | `e43b5911` | 397 | **l'analisi di oggi**: conformita' P6, voce **S**, l'INDETERMINATO `chi_p90`, voce **R**, dispersione di `r`, conto **FDT**. Barre **FRA SEMI** con il `t` di Student giusto per i gradi di liberta' | non serve: **legge CSV**, non tocca il simulatore |
| **`csv/_test_fork/_esperimento_spin_feedback.py`** | `35ae8a55` | 165 | l'A/B su **`SPIN_FEEDBACK`** a `TAU_A = 2.0`: `E4` (gate A8 sul feedback), `E1` (stabilita'), `E2` (conteggio nodi contro il `-32 %`), `E3` (`psi`, `d0`, `ramp`). **Tre bracci:** `off` e `on` a `TAU_A = 2.0`, `rif` al default `TAU_A = 50` | — *(e' un esperimento, non un sigillo; `SPIN_FEEDBACK` NON e' sigillato)* |
| **`csv/_test_fork/_esperimento_tau_a.py`** | `52ca4f68` | 151 | l'A/B **`TAU_A = 50` contro `TAU_A = 2.0`** nel deterministico: `S1` stabilita' [bloccante], `S2` la firma di `Z9`. Produce il **`-32 %`** su cui poggia `E2` dell'esperimento qui sopra | — *(esperimento)* |
| **`csv/_seal_fork/_sigillo_strato1.py`** | `06f7e661` | 541 | i sigilli dello **STRATO 1**: S1.0/S1a/S1b, S2, S3, S4, S5, S6, S7, **S8 (nuovo oggi)**, S3b | — *(e' un sigillo)* |

## 2. GLI STRUMENTI CHE HANNO PRODOTTO NUMERI ANCORA CITATI

| script | blob | righe | numero che regge | dove e' citato |
|---|---|---|---|---|
| `csv/_test_fork/_verdetto_4pi.py` | `aec79357` | 157 | **ESITO (A)** dei quattro bracci; gradiente `theta` **96.37 -> 15.08 = 6.39x** | **C14** |
| `csv/_test_fork/_rimisura_t3.py` | `b4a9775b` | 120 | le pendenze T3 sui quattro incroci PRE/POST x OFF/ON | **C8** |
| `csv/_test_fork/_controllo_semi.py` | `1fa8dc56` | 134 | **la dispersione FRA SEMI = 0.030** contro la `SE` interna ~0.010 | **C10**, ed e' il numero che ha fatto ritirare il «16.9 %» |
| `csv/_seal_fork/_sigillo_fix_cache.py` | `5858acf0` | 208 | fallback `_cs_nodo_prev` **71.88 % -> 0.00 %**, **5/5 PASS** | **C7** |
| `csv/_seal_fork/_sigillo_psi_spin_prec.py` | `3834df9d` | 248 | guardia 4pi fallita **95.33 % -> 0.00 %**, **6/6 PASS** | **C11** |
| `csv/_seal_fork/_sigillo_tau_luce.py` | `d11548cd` | 212 | **il sigillo che NON passa** (T2/T3/T4) | voce **A**, `doc/SIGILLO_tau_luce_FALLITO.md` |

---

## 3. ⚠ UN BUCO DI TRACCIABILITA', TROVATO OGGI

> **I `.log` dei run NON SONO NEL REPO, e non si vedono nemmeno come «non tracciati».**

`.gitignore` esclude `*.log` globalmente e ri-include **solo** `log/**/`, non `csv/**/*.log`.
Quindi `csv/_test_fork/_csOFF_s1.log` e compagni sono **invisibili a `git status`**: non appaiono
fra i file non tracciati, quindi nessuno si accorge che mancano.

**Cosa si perde:** la riga **`[osserva-flag] ... (letti DURANTE il run)`**, che e' la
certificazione **piu' diretta** dei flag — letta dai globali vivi **dentro** il ciclo, non da prima
del run. *(E' proprio la distinzione che ha fatto fallire il sigillo O3c il 2026-09-15, commit
`279c3b7`: leggere i flag prima di `_applica_flag` dava `False` su entrambi anche quando il run li
usava.)*

**Cosa NON si perde, e per questo il buco non e' urgente:** dal 2026-09-15 gli stessi flag sono
**colonne del CSV** (`FORK_SU2`, `FORK_SU2_MEM`, `SCUOTIMENTO`, `SYNC_UPDATE`, `KURAMOTO_SU2`,
`STEP2`, `GAMMA_TURBO`, `TAU_LUCE`, `CS_DINAMICO`, e da oggi `SPIN_LARMOR` e `TW_SPINORE`), **piu'
`blob` e `seed`** — ed e' esattamente il **P6**. **Il CSV resta, il log si perde**: la ridondanza e'
gia' dalla parte giusta.

**Decisione presa oggi, e i suoi limiti:** i log della campagna di oggi sono stati aggiunti con
`git add -f`, perche' sono la prova di una misura in corso. **Non ho toccato `.gitignore`**: e' una
regola di progetto, e cambiarla e' una decisione di Luca. **Finche' non e' cambiata, ogni campagna
futura ripetera' il buco a meno che qualcuno si ricordi del `-f`** — cioe' e' una toppa, non una
cura.

---

## 3-bis. LA GUARDIA DI IDENTITA' DEL CODICE (cablata il 2026-09-16, `CLAUDE.md` §5-quinquies)

`_osserva_vuoto.py` confronta il proprio blob calcolato con **`git rev-parse
HEAD:soliton_simulator.py`**, e si comporta in **due modi, entrambi provati**:

| caso | cosa fa | provato? |
|---|---|---|
| blob disco **=** blob HEAD | stampa *«codice COMMITTATO»* e prosegue | **si'** — `08784685` = `08784685` |
| blob disco **!=** blob HEAD | **scrive da solo** `<base>._sim.py`, copia **BINARIA** del file che sta girando, e lo dichiara nel log | **si'** — copia `a435ebb8` = disco `a435ebb8`, **byte-identica** |

**Si confronta col blob a HEAD, non con `git status`:** un file puo' risultare «modificato» per
sole newline e avere lo **stesso** blob, e puo' essere identico a un commit **vecchio** senza
esserlo a HEAD.
**La copia e' scritta in BINARIO** per la stessa ragione per cui lo sono le copie storiche del §4:
una riscrittura testuale cambierebbe le newline, quindi il **blob**, e la copia non sarebbe piu'
*quel* file.

---

## 3-ter. ⚠ QUALE SCRIPT PRODUCE QUALE `theta` — le DUE CONVENZIONI (C19, chiuso il 2026-09-16)

**`theta` non e' un'osservabile sola.** Due script lo calcolano in due tempi diversi, e i numeri
**non sono confrontabili fra loro**:

| script | riga | formula | tempo | dove sta |
|---|---|---|---|---|
| `_rimisura_t3.py` | `:73` | `theta = \|omega\| * DT` | **COORDINATA** | i numeri di **C8**, e **l'attesa `-0.69`** |
| `_osserva_vuoto.py` MISURA C/F | `:400`, `:482` | `theta = \|omega\| * dt_n` | **PROPRIO** | i numeri del **referto S/R/FDT** |

**Dal 2026-09-16 l'osservatore scrive ENTRAMBE, fianco a fianco, nello stesso campione:**
`theta_coord_*`, `theta_prop_*`, e **`r_ratio_*`** — il loro rapporto, che **e' `r`**, il tempo
proprio locale (utile di per se': la FASE 5 agisce proprio li'). In MISURA F ci sono anche
`t3_b_theta_coord`, `t3_b_theta_prop` e **`t3_b_r`**.
**Nessuna delle due e' stata dismessa:** la **giusta** e' `prop` (`CLAUDE.md` §9, *il tic dei
processi locali e' `dt_n = DT*r`*), ma **tutto lo storico e' in `coord`** e serve per rileggerlo.
**`theta_*` senza suffisso resta come LEGACY ed E' `theta_prop`**: sta li' solo perche' gli **8 CSV
gia' committati** e `_verdetto_4pi.py` / `_verdetto_S_R.py` la leggono con quel nome. **Rinominarla
avrebbe reso illeggibili i dati gia' presi**, che e' un prezzo piu' alto del guadagno.
*(Deviazione dichiarata rispetto al mandato, che chiedeva «mai `theta` nudo»: il nome nudo
sopravvive come alias documentato, non come nome da usare.)*

**IL CONTROLLO DI IDENTITA', cablato:** poiche' `theta_prop = theta_coord * r` e il campione e' lo
stesso, deve valere **`pend(prop) - pend(coord) - pend(r) = 0` ESATTAMENTE**. La colonna
`t3_identita` lo verifica: **misurato `4.6e-16`**. Se un giorno non fosse ~`1e-12`, l'errore e' nel
codice, non nella fisica.

**E UNA CORREZIONE ALLA CATENA, che e' venuta fuori scrivendo le due convenzioni.** Da
`|omega|_eq = |F|*sqrt(dt_n*tau/2)` con `dt_n = DT*r`:

```
pend(omega)       = sigma + tau/2 +   r/2
pend(theta_coord) = sigma + tau/2 +   r/2
pend(theta_prop)  = sigma + tau/2 + 3*r/2
```

**La formula usata finora, `sigma + tau/2`, ASSUME `pend(r) = 0` — in ENTRAMBE le convenzioni, e
non era mai stato verificato.** Ora `t3_b_r` lo misura. *(Il **divario** resta pero'
**indipendente dalla convenzione**: `divario_prop - divario_coord = pend(r) - pend(r) = 0`, ed e'
verificato nei dati.)*

---

## 4. COSA *NON* E' UNO STRUMENTO DI MISURA (per non confondersi)

`csv/_seal_fork/_old_sim_pre_*.py` sono **copie storiche del simulatore**, estratte da git
(`_old_sim_pre_strato1.py`, `_pre_step2.py`, `_pre_pezzo3.py`, `_pre_fixcache.py`,
`_pre_psispin.py`, `_pre_tauluce.py`). **Non misurano: sono il termine di paragone** dei sigilli di
byte-identita'. Si estraggono **in binario** (`git show`, non `text=True`), perche' con le newline
universali il file riscritto avrebbe un **blob diverso** e il controllo che lo verifica non
varrebbe piu' nulla.

---

## 5. **QUALE COMANDO PRODUCE QUALE `.pkl`** *(sezione aperta il 2026-09-17)*

> **Perche' questa sezione esiste.** I `.pkl` sono **~36 file, ~18 MB l'uno, oltre 650 MB**: non
> sono nel repo e **non devono esserci** — git non dimentica i binari, e ogni versione resterebbe
> nella storia per sempre. **Ma il sistema e' DETERMINISTICO** (stesso seme, stesso blob, stesso
> risultato: verificato decine di volte dalle byte-identita'), **quindi un `.pkl` non e' un dato
> irripetibile: e' il RISULTATO DI UN COMANDO.**
> **Se il comando non e' scritto, il dato e' perso come riproducibilita' anche se il file c'e'.**
> Regola in `CLAUDE.md`, presidio *«un `.pkl` senza il suo comando non e' un dato»*.

**Tre esiti, e si dichiarano:** **RICOSTRUITO** (comando completo, blob, seme, passi) ·
**PARZIALE** (manca qualcosa: **si scrive cosa**, non si riempie con una supposizione) ·
**NON RICOSTRUIBILE** (**si dice**: e' un reperto, non un imbarazzo).

### L'ESITO DEL RECUPERO RETROATTIVO (2026-09-17)

```
36 .pkl   ->   RICOSTRUITI 21    PARZIALI 14    NON RICOSTRUIBILI 1
```

**La fonte NON e' la memoria**: e' il **blocco di condizioni JSON** che ogni run scrive in testa al
proprio `.cond.csv` (seme, passi, tutti i flag) **piu' la colonna `blob`** del `.vuoto.csv`
dell'osservatore. **Due file diversi, due meta' della stessa prova** — ed e' per questo che il primo
passaggio dava **zero** ricostruiti: cercavo il blob dove non sta.
Ricostruttore: `csv/_test_fork/_ricostruisci_comandi_pkl.py` (**non apre i `.pkl`**, legge solo i CSV).

**I 21 RICOSTRUITI** portano il blob: **`c57800c1`** (baseline 4 bracci) · **`08784685`** (campagna
`cs`, 4+4 semi) · **`a44adc31`** (campagna Step 2, 4+4 semi) · **`827d3bf8`** (`_vuoto_sigON_s1`).

**I 14 PARZIALI mancano TUTTI della stessa cosa: il BLOB del simulatore.** Non e' un caso: sono i
run **anteriori al cablaggio delle colonne P6** nell'osservatore — **e' il «buco di tracciabilita'»
gia' documentato al §3 di questo file**, visto ora dal lato dei dati invece che da quello degli
strumenti. **Si sa COSA e' stato lanciato, non SU QUALE CODICE**, e su questo repo il blob e'
cambiato **14 volte in tre giorni**.

**L'UNICO NON RICOSTRUIBILE: `_stf_seed.pkl`** — **nessun `.cond.csv` corrispondente.** Il file
esiste, ma **come riproducibilita' e' gia' perso**, e saperlo vale piu' che fingere il contrario.

### LA TABELLA

<!-- generato da _ricostruisci_comandi_pkl.py: NON scrivere a mano -->

| `.pkl` | esito | seme | passi | comando |
|---|---|---|---|---|
| `_stf_seed.pkl` | **NON RICOSTRUIBILE** *(nessun .cond.csv corrispondente)* |  |  | `` |
| `_tw_off.pkl` | **PARZIALE** *(manca: BLOB del simulatore)* | 1 | 150 | `python soliton_simulator.py --batch --nmasse 3 --sep 8.0 --lam 0.8 --seed 1 --passi 150 --calore-scal --campo-spinoriale --chi-core --cs-dinamico --deparam-orologio --fork-su2 --fork-su2-mem --spinore-corretto --spinore-vivo --verlet --csv csv/_test_fork/_tw_off.cond.csv --sync-db csv/_test_fork/_tw_off.pkl --db-cleanup` |
| `_tw_on.pkl` | **PARZIALE** *(manca: BLOB del simulatore)* | 1 | 150 | `python soliton_simulator.py --batch --nmasse 3 --sep 8.0 --lam 0.8 --seed 1 --passi 150 --calore-scal --campo-spinoriale --chi-core --cs-dinamico --deparam-orologio --fork-su2 --fork-su2-mem --spinore-corretto --spinore-vivo --tw-spinore --verlet --csv csv/_test_fork/_tw_on.cond.csv --sync-db csv/_test_fork/_tw_on.pkl --db-cleanup` |
| `_vuoto_ab_off_s1.pkl` | **PARZIALE** *(manca: BLOB del simulatore)* | 1 | 300 | `python soliton_simulator.py --batch --nmasse 3 --sep 8.0 --lam 0.8 --seed 1 --passi 300 --calore-scal --campo-spinoriale --chi-core --deparam-orologio --fork-su2 --fork-su2-mem --spinore-corretto --spinore-vivo --verlet --csv csv/_test_fork/_vuoto_ab_off_s1.cond.csv --sync-db csv/_test_fork/_vuoto_ab_off_s1.pkl --db-cleanup` |
| `_vuoto_ab_on_s1.pkl` | **PARZIALE** *(manca: BLOB del simulatore)* | 1 | 300 | `python soliton_simulator.py --batch --nmasse 3 --sep 8.0 --lam 0.8 --seed 1 --passi 300 --calore-scal --campo-spinoriale --chi-core --deparam-orologio --fork-su2 --fork-su2-mem --spinore-corretto --spinore-vivo --verlet --csv csv/_test_fork/_vuoto_ab_on_s1.cond.csv --sync-db csv/_test_fork/_vuoto_ab_on_s1.pkl --db-cleanup` |
| `_vuoto_base_OFF_s1.pkl` | **RICOSTRUITO** | 1 | 500 | `python soliton_simulator.py --batch --nmasse 3 --sep 8.0 --lam 0.8 --seed 1 --passi 500 --calore-scal --campo-spinoriale --chi-core --cs-dinamico --deparam-orologio --fork-su2 --fork-su2-mem --spinore-corretto --spinore-vivo --verlet --csv csv/_test_fork/_vuoto_base_OFF_s1.cond.csv --sync-db csv/_test_fork/_vuoto_base_OFF_s1.pkl --db-cleanup` |
| `_vuoto_base_OFF_s2.pkl` | **RICOSTRUITO** | 2 | 500 | `python soliton_simulator.py --batch --nmasse 3 --sep 8.0 --lam 0.8 --seed 2 --passi 500 --calore-scal --campo-spinoriale --chi-core --cs-dinamico --deparam-orologio --fork-su2 --fork-su2-mem --spinore-corretto --spinore-vivo --verlet --csv csv/_test_fork/_vuoto_base_OFF_s2.cond.csv --sync-db csv/_test_fork/_vuoto_base_OFF_s2.pkl --db-cleanup` |
| `_vuoto_base_ON_s1.pkl` | **RICOSTRUITO** | 1 | 500 | `python soliton_simulator.py --batch --nmasse 3 --sep 8.0 --lam 0.8 --seed 1 --passi 500 --calore-scal --campo-spinoriale --chi-core --cs-dinamico --deparam-orologio --fork-su2 --fork-su2-mem --spinore-corretto --spinore-vivo --tau-luce --verlet --csv csv/_test_fork/_vuoto_base_ON_s1.cond.csv --sync-db csv/_test_fork/_vuoto_base_ON_s1.pkl --db-cleanup` |
| `_vuoto_base_ON_s2.pkl` | **RICOSTRUITO** | 2 | 500 | `python soliton_simulator.py --batch --nmasse 3 --sep 8.0 --lam 0.8 --seed 2 --passi 500 --calore-scal --campo-spinoriale --chi-core --cs-dinamico --deparam-orologio --fork-su2 --fork-su2-mem --spinore-corretto --spinore-vivo --tau-luce --verlet --csv csv/_test_fork/_vuoto_base_ON_s2.cond.csv --sync-db csv/_test_fork/_vuoto_base_ON_s2.pkl --db-cleanup` |
| `_vuoto_csOFF_s1.pkl` | **RICOSTRUITO** | 1 | 500 | `python soliton_simulator.py --batch --nmasse 3 --sep 8.0 --lam 0.8 --seed 1 --passi 500 --calore-scal --campo-spinoriale --chi-core --cs-dinamico --deparam-orologio --fork-su2 --fork-su2-mem --spinore-corretto --spinore-vivo --verlet --csv csv/_test_fork/_vuoto_csOFF_s1.cond.csv --sync-db csv/_test_fork/_vuoto_csOFF_s1.pkl --db-cleanup` |
| `_vuoto_csOFF_s2.pkl` | **RICOSTRUITO** | 2 | 500 | `python soliton_simulator.py --batch --nmasse 3 --sep 8.0 --lam 0.8 --seed 2 --passi 500 --calore-scal --campo-spinoriale --chi-core --cs-dinamico --deparam-orologio --fork-su2 --fork-su2-mem --spinore-corretto --spinore-vivo --verlet --csv csv/_test_fork/_vuoto_csOFF_s2.cond.csv --sync-db csv/_test_fork/_vuoto_csOFF_s2.pkl --db-cleanup` |
| `_vuoto_csOFF_s3.pkl` | **RICOSTRUITO** | 3 | 500 | `python soliton_simulator.py --batch --nmasse 3 --sep 8.0 --lam 0.8 --seed 3 --passi 500 --calore-scal --campo-spinoriale --chi-core --cs-dinamico --deparam-orologio --fork-su2 --fork-su2-mem --spinore-corretto --spinore-vivo --verlet --csv csv/_test_fork/_vuoto_csOFF_s3.cond.csv --sync-db csv/_test_fork/_vuoto_csOFF_s3.pkl --db-cleanup` |
| `_vuoto_csOFF_s4.pkl` | **RICOSTRUITO** | 4 | 500 | `python soliton_simulator.py --batch --nmasse 3 --sep 8.0 --lam 0.8 --seed 4 --passi 500 --calore-scal --campo-spinoriale --chi-core --cs-dinamico --deparam-orologio --fork-su2 --fork-su2-mem --spinore-corretto --spinore-vivo --verlet --csv csv/_test_fork/_vuoto_csOFF_s4.cond.csv --sync-db csv/_test_fork/_vuoto_csOFF_s4.pkl --db-cleanup` |
| `_vuoto_csON_s1.pkl` | **RICOSTRUITO** | 1 | 500 | `python soliton_simulator.py --batch --nmasse 3 --sep 8.0 --lam 0.8 --seed 1 --passi 500 --calore-scal --campo-spinoriale --chi-core --cs-dinamico --deparam-orologio --fork-su2 --fork-su2-mem --spinore-corretto --spinore-vivo --tau-luce --verlet --csv csv/_test_fork/_vuoto_csON_s1.cond.csv --sync-db csv/_test_fork/_vuoto_csON_s1.pkl --db-cleanup` |
| `_vuoto_csON_s2.pkl` | **RICOSTRUITO** | 2 | 500 | `python soliton_simulator.py --batch --nmasse 3 --sep 8.0 --lam 0.8 --seed 2 --passi 500 --calore-scal --campo-spinoriale --chi-core --cs-dinamico --deparam-orologio --fork-su2 --fork-su2-mem --spinore-corretto --spinore-vivo --tau-luce --verlet --csv csv/_test_fork/_vuoto_csON_s2.cond.csv --sync-db csv/_test_fork/_vuoto_csON_s2.pkl --db-cleanup` |
| `_vuoto_csON_s3.pkl` | **RICOSTRUITO** | 3 | 500 | `python soliton_simulator.py --batch --nmasse 3 --sep 8.0 --lam 0.8 --seed 3 --passi 500 --calore-scal --campo-spinoriale --chi-core --cs-dinamico --deparam-orologio --fork-su2 --fork-su2-mem --spinore-corretto --spinore-vivo --tau-luce --verlet --csv csv/_test_fork/_vuoto_csON_s3.cond.csv --sync-db csv/_test_fork/_vuoto_csON_s3.pkl --db-cleanup` |
| `_vuoto_csON_s4.pkl` | **RICOSTRUITO** | 4 | 500 | `python soliton_simulator.py --batch --nmasse 3 --sep 8.0 --lam 0.8 --seed 4 --passi 500 --calore-scal --campo-spinoriale --chi-core --cs-dinamico --deparam-orologio --fork-su2 --fork-su2-mem --spinore-corretto --spinore-vivo --tau-luce --verlet --csv csv/_test_fork/_vuoto_csON_s4.cond.csv --sync-db csv/_test_fork/_vuoto_csON_s4.pkl --db-cleanup` |
| `_vuoto_k300_s2off_s1.pkl` | **PARZIALE** *(manca: BLOB del simulatore)* | 1 | 2000 | `python soliton_simulator.py --batch --nmasse 3 --sep 8.0 --gamma-turbo 300.0 --lam 0.8 --seed 1 --passi 2000 --calore-scal --campo-spinoriale --chi-core --cs-dinamico --deparam-orologio --fork-su2 --fork-su2-mem --spinore-corretto --spinore-vivo --verlet --csv csv/_test_fork/_vuoto_k300_s2off_s1.cond.csv --sync-db csv/_test_fork/_vuoto_k300_s2off_s1.pkl --db-cleanup` |
| `_vuoto_k300_s2on_s1.pkl` | **PARZIALE** *(manca: BLOB del simulatore)* | 1 | 2000 | `python soliton_simulator.py --batch --nmasse 3 --sep 8.0 --gamma-turbo 300.0 --lam 0.8 --seed 1 --passi 2000 --calore-scal --campo-spinoriale --chi-core --cs-dinamico --deparam-orologio --fork-su2 --fork-su2-mem --spinore-corretto --spinore-vivo --step2-orologio --verlet --csv csv/_test_fork/_vuoto_k300_s2on_s1.cond.csv --sync-db csv/_test_fork/_vuoto_k300_s2on_s1.pkl --db-cleanup` |
| `_vuoto_k_frozen_s1.pkl` | **PARZIALE** *(manca: BLOB del simulatore)* | 1 | 300 | `python soliton_simulator.py --batch --nmasse 3 --sep 8.0 --lam 0.8 --seed 1 --passi 300 --calore-scal --campo-spinoriale --chi-core --deparam-orologio --fork-su2 --fork-su2-mem --kuramoto-su2 --spinore-corretto --spinore-vivo --verlet --csv csv/_test_fork/_vuoto_k_frozen_s1.cond.csv --sync-db csv/_test_fork/_vuoto_k_frozen_s1.pkl --db-cleanup` |
| `_vuoto_k_noise_s1.pkl` | **PARZIALE** *(manca: BLOB del simulatore)* | 1 | 300 | `python soliton_simulator.py --batch --nmasse 3 --sep 8.0 --lam 0.8 --seed 1 --passi 300 --calore-scal --campo-spinoriale --chi-core --deparam-orologio --fork-su2 --fork-su2-mem --kuramoto-su2 --spinore-corretto --spinore-vivo --verlet --csv csv/_test_fork/_vuoto_k_noise_s1.cond.csv --sync-db csv/_test_fork/_vuoto_k_noise_s1.pkl --db-cleanup` |
| `_vuoto_pulito1_s1.pkl` | **PARZIALE** *(manca: BLOB del simulatore)* | 1 | 500 | `python soliton_simulator.py --batch --nmasse 3 --sep 8.0 --lam 0.8 --seed 1 --passi 500 --calore-scal --campo-spinoriale --chi-core --deparam-orologio --fork-su2 --fork-su2-mem --spinore-corretto --spinore-vivo --verlet --csv csv/_test_fork/_vuoto_pulito1_s1.cond.csv --sync-db csv/_test_fork/_vuoto_pulito1_s1.pkl --db-cleanup` |
| `_vuoto_pulito2_s2.pkl` | **PARZIALE** *(manca: BLOB del simulatore)* | 2 | 500 | `python soliton_simulator.py --batch --nmasse 3 --sep 8.0 --lam 0.8 --seed 2 --passi 500 --calore-scal --campo-spinoriale --chi-core --deparam-orologio --fork-su2 --fork-su2-mem --spinore-corretto --spinore-vivo --verlet --csv csv/_test_fork/_vuoto_pulito2_s2.cond.csv --sync-db csv/_test_fork/_vuoto_pulito2_s2.pkl --db-cleanup` |
| `_vuoto_s2OFF_s1.pkl` | **RICOSTRUITO** | 1 | 500 | `python soliton_simulator.py --batch --nmasse 3 --sep 8.0 --lam 0.8 --seed 1 --passi 500 --calore-scal --campo-spinoriale --chi-core --cs-dinamico --deparam-orologio --fork-su2 --fork-su2-mem --senza-step2-orologio --spinore-corretto --spinore-vivo --verlet --csv csv/_test_fork/_vuoto_s2OFF_s1.cond.csv --sync-db csv/_test_fork/_vuoto_s2OFF_s1.pkl --db-cleanup` |
| `_vuoto_s2OFF_s2.pkl` | **RICOSTRUITO** | 2 | 500 | `python soliton_simulator.py --batch --nmasse 3 --sep 8.0 --lam 0.8 --seed 2 --passi 500 --calore-scal --campo-spinoriale --chi-core --cs-dinamico --deparam-orologio --fork-su2 --fork-su2-mem --senza-step2-orologio --spinore-corretto --spinore-vivo --verlet --csv csv/_test_fork/_vuoto_s2OFF_s2.cond.csv --sync-db csv/_test_fork/_vuoto_s2OFF_s2.pkl --db-cleanup` |
| `_vuoto_s2OFF_s3.pkl` | **RICOSTRUITO** | 3 | 500 | `python soliton_simulator.py --batch --nmasse 3 --sep 8.0 --lam 0.8 --seed 3 --passi 500 --calore-scal --campo-spinoriale --chi-core --cs-dinamico --deparam-orologio --fork-su2 --fork-su2-mem --senza-step2-orologio --spinore-corretto --spinore-vivo --verlet --csv csv/_test_fork/_vuoto_s2OFF_s3.cond.csv --sync-db csv/_test_fork/_vuoto_s2OFF_s3.pkl --db-cleanup` |
| `_vuoto_s2OFF_s4.pkl` | **RICOSTRUITO** | 4 | 500 | `python soliton_simulator.py --batch --nmasse 3 --sep 8.0 --lam 0.8 --seed 4 --passi 500 --calore-scal --campo-spinoriale --chi-core --cs-dinamico --deparam-orologio --fork-su2 --fork-su2-mem --senza-step2-orologio --spinore-corretto --spinore-vivo --verlet --csv csv/_test_fork/_vuoto_s2OFF_s4.cond.csv --sync-db csv/_test_fork/_vuoto_s2OFF_s4.pkl --db-cleanup` |
| `_vuoto_s2ON_s1.pkl` | **RICOSTRUITO** | 1 | 500 | `python soliton_simulator.py --batch --nmasse 3 --sep 8.0 --lam 0.8 --seed 1 --passi 500 --calore-scal --campo-spinoriale --chi-core --cs-dinamico --deparam-orologio --fork-su2 --fork-su2-mem --spinore-corretto --spinore-vivo --verlet --csv csv/_test_fork/_vuoto_s2ON_s1.cond.csv --sync-db csv/_test_fork/_vuoto_s2ON_s1.pkl --db-cleanup` |
| `_vuoto_s2ON_s2.pkl` | **RICOSTRUITO** | 2 | 500 | `python soliton_simulator.py --batch --nmasse 3 --sep 8.0 --lam 0.8 --seed 2 --passi 500 --calore-scal --campo-spinoriale --chi-core --cs-dinamico --deparam-orologio --fork-su2 --fork-su2-mem --spinore-corretto --spinore-vivo --verlet --csv csv/_test_fork/_vuoto_s2ON_s2.cond.csv --sync-db csv/_test_fork/_vuoto_s2ON_s2.pkl --db-cleanup` |
| `_vuoto_s2ON_s3.pkl` | **RICOSTRUITO** | 3 | 500 | `python soliton_simulator.py --batch --nmasse 3 --sep 8.0 --lam 0.8 --seed 3 --passi 500 --calore-scal --campo-spinoriale --chi-core --cs-dinamico --deparam-orologio --fork-su2 --fork-su2-mem --spinore-corretto --spinore-vivo --verlet --csv csv/_test_fork/_vuoto_s2ON_s3.cond.csv --sync-db csv/_test_fork/_vuoto_s2ON_s3.pkl --db-cleanup` |
| `_vuoto_s2ON_s4.pkl` | **RICOSTRUITO** | 4 | 500 | `python soliton_simulator.py --batch --nmasse 3 --sep 8.0 --lam 0.8 --seed 4 --passi 500 --calore-scal --campo-spinoriale --chi-core --cs-dinamico --deparam-orologio --fork-su2 --fork-su2-mem --spinore-corretto --spinore-vivo --verlet --csv csv/_test_fork/_vuoto_s2ON_s4.cond.csv --sync-db csv/_test_fork/_vuoto_s2ON_s4.pkl --db-cleanup` |
| `_vuoto_sigDET_s1.pkl` | **PARZIALE** *(manca: BLOB del simulatore)* | 1 | 150 | `python soliton_simulator.py --batch --nmasse 3 --sep 8.0 --lam 0.8 --seed 1 --passi 150 --calore-scal --campo-spinoriale --chi-core --cs-dinamico --deparam-orologio --fork-su2 --fork-su2-mem --spinore-corretto --spinore-vivo --verlet --csv csv/_test_fork/_vuoto_sigDET_s1.cond.csv --sync-db csv/_test_fork/_vuoto_sigDET_s1.pkl --db-cleanup` |
| `_vuoto_sigOFF_s1.pkl` | **PARZIALE** *(manca: BLOB del simulatore)* | 1 | 150 | `python soliton_simulator.py --batch --nmasse 3 --sep 8.0 --lam 0.8 --seed 1 --passi 150 --calore-scal --campo-spinoriale --chi-core --cs-dinamico --deparam-orologio --fork-su2 --fork-su2-mem --spinore-corretto --spinore-vivo --verlet --csv csv/_test_fork/_vuoto_sigOFF_s1.cond.csv --sync-db csv/_test_fork/_vuoto_sigOFF_s1.pkl --db-cleanup` |
| `_vuoto_sigON_s1.pkl` | **RICOSTRUITO** | 1 | 150 | `python soliton_simulator.py --batch --nmasse 3 --sep 8.0 --lam 0.8 --seed 1 --passi 150 --calore-scal --campo-spinoriale --chi-core --cs-dinamico --deparam-orologio --fork-su2 --fork-su2-mem --spinore-corretto --spinore-vivo --verlet --csv csv/_test_fork/_vuoto_sigON_s1.cond.csv --sync-db csv/_test_fork/_vuoto_sigON_s1.pkl --db-cleanup` |
| `_vuoto_stf_freeze_s1.pkl` | **PARZIALE** *(manca: BLOB del simulatore)* | 1 | 900 | `python soliton_simulator.py --batch --nmasse 3 --sep 8.0 --lam 0.8 --seed 1 --passi 900 --calore-scal --campo-spinoriale --chi-core --deparam-orologio --fork-su2 --fork-su2-mem --spinore-corretto --spinore-vivo --verlet --csv csv/_test_fork/_vuoto_stf_freeze_s1.cond.csv --sync-db csv/_test_fork/_vuoto_stf_freeze_s1.pkl --db-cleanup` |
| `_vuoto_stf_shake_s1.pkl` | **PARZIALE** *(manca: BLOB del simulatore)* | 1 | 300 | `python soliton_simulator.py --batch --nmasse 3 --sep 8.0 --lam 0.8 --seed 1 --passi 300 --calore-scal --campo-spinoriale --chi-core --deparam-orologio --fork-su2 --fork-su2-mem --spinore-corretto --spinore-vivo --verlet --csv csv/_test_fork/_vuoto_stf_shake_s1.cond.csv --sync-db csv/_test_fork/_vuoto_stf_shake_s1.pkl --db-cleanup` |

---

## 4. I COMANDI ESATTI (2026-09-17) — regola dei `.pkl`: un dato senza il suo comando non e' un dato

**`_esperimento_spin_feedback.py`** — lanciato dalla radice del repo, output su
`csv/_test_fork/_esperimento_spin_feedback.txt`:

```
python csv/_test_fork/_esperimento_spin_feedback.py
```

Il driver lancia **tre** sottoprocessi. Le righe di comando effettive (`SCRATCH` = la cartella
scratchpad di sessione, i `.pkl` sono `--db-cleanup` e **non** vengono committati):

```
python soliton_simulator.py --batch --nmasse 3 --sep 8 --seed 5 --passi 120 --ogni 120   --db-ogni 120 --campo-spinoriale --spinore-vivo --spinore-corretto --chi-core --calore-scal   --deparam-orologio --verlet --fork-su2 --fork-su2-mem --cs-dinamico --tau-a 2.0   --csv $SCRATCH/_sfb_off.csv --sync-db $SCRATCH/_sfb_off.pkl --db-cleanup
            (braccio ON: + `--spin-feedback`, csv/db `_sfb_on`)
            (braccio RIF: SENZA `--tau-a 2.0`, csv/db `_sfb_rif`  <- e' questo che mancava)
```

**`_esperimento_tau_a.py`** (i due bracci di §9.33):

```
python soliton_simulator.py --batch --nmasse 3 --sep 8 --seed 5 --passi 120 --ogni 120   --db-ogni 120 --campo-spinoriale --spinore-vivo --spinore-corretto --chi-core --calore-scal   --deparam-orologio --verlet --fork-su2 --fork-su2-mem --cs-dinamico   --csv $SCRATCH/_exp_tau50.csv --sync-db $SCRATCH/_exp_tau50.pkl --db-cleanup
            (braccio 2.0: + `--tau-a 2.0`, csv/db `_exp_tau02`)
```

> **E il modo di verificare quale `TAU_A` ha girato NON e' rileggere questi comandi**, ma il blocco
> **`# RUN_PARAMS`** in testa a ciascun CSV: `tau_a_over` + `leggi_attive.REGIME`.
> **Il driver dice cosa si INTENDEVA lanciare; il CSV dice cosa E' STATO lanciato.**
> Vedi `doc/REFERTO_driver_gira.md`.

---

## 2026-09-18 — **la campagna a 1200 passi** (`csv/_test_fork/_g1200/`)

**I `.pkl` NON sono committati** (binari, grandi): **il dato È il comando**, e il sistema è
deterministico. Ecco tutto ciò che serve a rifarli.

| cosa | valore |
|---|---|
| **BLOB del simulatore** | **`a1ae5090`** *(`sha1` dei BYTE GREZZI, non `git hash-object`: C18)* |
| **HEAD alla partenza** | `fb87640` |
| **SEME** | quello di default del batch — **letto DAI DATI** nell'intestazione `RUN_PARAMS` di `csv/_test_fork/_g1200/cond.csv` (P6) |
| **passi** | **1200**, in quattro segmenti `120 → 400 → 800 → 1200` |
| **durata misurata** | **127.5 s / 100 passi** sul pilota ⟹ **~26 min** totali (`n` piatto) |
| **script di analisi** | `csv/_test_fork/_struttura_1200.py`, blob **`d3f954e3`** |
| **data** | 2026-09-18 |

**LA RIGA DI COMANDO, VERBATIM** *(ripetuta con `--passi` 120, 400, 800, 1200; il `.pkl` viene
COPIATO in `stato_<P>.pkl` dopo ogni segmento, perché `--db-ogni` riscrive sempre lo stesso file)*:

```
python soliton_simulator.py --batch --nmasse 3 --sep 8 --ogni 10 \
  --csv csv/_test_fork/_g1200/cond.csv --diaglog csv/_test_fork/_g1200/diag.csv \
  --campo-spinoriale --spinore-vivo --spinore-corretto --chi-core \
  --calore-scal --deparam-orologio --verlet --fork-su2 --fork-su2-mem \
  --cs-dinamico --tau-luce --rumore-colorato \
  --pav-com --guscio-morbido --zeta-vir --chi-basc --plast-din --viriale --olon-part \
  --sync-db csv/_test_fork/_g1200/stato.pkl --db-ogni 10 --passi <P>
```

**⚠ DUE AVVERTENZE CHE VANNO CON IL DATO, NON DOPO:**
1. **`--tau-luce` ha il SIGILLO FALLITO** (`doc/SIGILLO_tau_luce_FALLITO.md`, CLAUDE.md par.0): è
   **un ramo esplicitamente NON CERTIFICATO**, ed è la ragione per cui il gate resta a `c0803713`.
2. **`--chi-basc` RISCRIVE `perc_chi` in blocco a ogni passo** (`:3486`): in questo run `perc_chi`
   **non è un'etichetta di lignaggio**, ed è una configurazione **diversa** da quella di `Z45`.

**⚠ E UN LIMITE DEL `.pkl` STESSO, trovato leggendo `salva_stato` (`:2862-2866`):** salva solo
`ndarray/int/float/bool/str`, quindi **`conc_nodi` e `masse_info` — il tracking delle masse — NON ci
sono.** Le coorti vanno ricostruite **dalla posizione**, e l'analisi lo dichiara.

**`--db` NON ESISTE come flag:** è ambiguo con `--db-cleanup`/`--db-ogni`. **Il flag è `--sync-db`.**

---

## 2026-09-18 — **la scena VIDEO a 400 frame** (`csv/_test_fork/_gvideo/`)

| cosa | valore |
|---|---|
| **BLOB del simulatore** | **`a1ae5090`** *(`sha1` dei BYTE GREZZI, non `git hash-object`: C18)* |
| **driver** | `csv/_test_fork/_scena_video.py`, **SIGILLATO** (`_sigillo_driver_video.py`: 14 array, `max\|A-B\| = 0.000e+00`) |
| **frame / passi** | **400 frame = 2400 passi** *(`PASSI_PER_FRAME = 6`)* |
| **durata misurata** | **6535 s (1h49)**, `16.34 s/frame` |
| **`n`** | 2391 → 8018 |
| **snapshot** | `frame_{10,115,190,270,375,400}.pkl` — **il `_db_step` dentro è il FRAME, non il passo** |
| **analisi** | `csv/_test_fork/_struttura_video.py` (`6bb24e5e`) - `csv/_test_fork/_ab_due_tre.py` (`0889bcef`) - **`csv/_test_fork/_z9_coorti.py` (`16acd823`)** |

**IL COMANDO, VERBATIM:**

```
python csv/_test_fork/_scena_video.py 400 csv/_test_fork/_gvideo 10,115,190,270,375
```

*(il driver applica internamente la config: `--test N-MASSE --nmasse 3 --sep 8 --giri 0
--campo-spinoriale --spinore-vivo --spinore-corretto --chi-core --calore-scal --deparam-orologio
--verlet --fork-su2 --fork-su2-mem --cs-dinamico --tau-luce --rumore-colorato --pav-com
--guscio-morbido --zeta-vir --chi-basc --plast-din --viriale --olon-part`, **col percorso ufficiale
`_cli()` → `_applica_regime` → `_applica_flag`**)*

**⚠ `--tau-luce` HA IL SIGILLO FALLITO** (`doc/SIGILLO_tau_luce_FALLITO.md`): **ramo NON
CERTIFICATO**, ed è la ragione per cui il gate resta a `c0803713`. **Ogni numero di questa campagna
lo eredita.** **`--chi-basc` riscrive `perc_chi` a ogni passo.**

**I `.pkl` (48 MB l'uno) NON sono committati: il dato è il comando, e il sistema è deterministico.**

## 2026-09-18 — **il CONTROLLO a DUE masse** (`csv/_test_fork/_g2m/`) — *A/B a variabile singola contro `_gvideo`*

> **⚠ VOCE SCRITTA IN RITARDO, e lo dichiaro:** la regola dice **«nello STESSO commit»** del run che
> produce i `.pkl`. **Questa voce è stata scritta DOPO la chiusura del run**, insieme al referto
> `Z52`. **I dati sono rigenerabili — il comando è qui sotto, verbatim, e il blob non è cambiato — ma
> fra la nascita dei `.pkl` e la loro documentazione c'è stata una finestra in cui non lo erano.**

| cosa | valore |
|---|---|
| **BLOB del simulatore** | **`a1ae5090`** *(`sha1` dei BYTE GREZZI, non `git hash-object`: C18)* — **lo STESSO del braccio a tre masse** |
| **driver** | `csv/_test_fork/_scena_video.py`, **SIGILLATO** (`_sigillo_driver_video.py`) |
| **frame / passi** | **400 frame = 2400 passi** *(`PASSI_PER_FRAME = 6`)* |
| **durata misurata** | **5357.8 s (1h29)**, `13.40 s/frame` |
| **`n`** | 1894 → 5878 *(contro 2391 → 8018 a tre masse)* |
| **snapshot** | `frame_{10,115,190,270,375,400}.pkl` — **il `_db_step` dentro è il FRAME, non il passo** |
| **analisi** | `csv/_test_fork/_ab_due_tre.py` (`0889bcef`) - `csv/_test_fork/_struttura_video.py` (`16773e2f`) - **`csv/_test_fork/_z9_coorti.py` (`16acd823`)** |

**IL COMANDO, VERBATIM:**

```
python csv/_test_fork/_scena_video.py 400 csv/_test_fork/_g2m 10,115,190,270,375 fisica 2
```

*(l'ultimo argomento è `--nmasse 2`: **è l'UNICA differenza** dal comando del braccio a tre masse.
Tutti gli altri flag sono quelli della voce `_gvideo` qui sopra, applicati dallo stesso driver.)*

**HEAD all'avvio:** `8f94cf4` · **avvio** `2026-09-18 19:40:56` · **chiuso** `2026-09-18 21:10:45`

**⚠ `--tau-luce` HA IL SIGILLO FALLITO** (`doc/SIGILLO_tau_luce_FALLITO.md`): **ramo NON
CERTIFICATO**, e **ogni numero di questo run lo eredita** — **esattamente come il braccio a tre
masse**, il che è la ragione per cui l'A/B resta interpretabile: **il difetto è comune ai due bracci.**

**⚠ `--chi-basc` attivo:** `perc_chi` **non è un'etichetta di lignaggio.**

**I `.pkl` NON si committano** (binari). **Il dato è il comando.**

---

## 2026-09-19 — **L'ARCHIVIO A SERIE** (`--db-serie`, `--db-rigioca`, `gzip`)

> **Blob del simulatore sigillato: `7c4dec1d`** *(byte grezzi `5216c891`)*. **Sigillo `12/12`.**
> **`Z54` del registro.** I `.pkl` non si committano: **qui ci sono i comandi che li rigenerano.**

### Gli strumenti

| script | blob | cosa produce | esito |
|---|---|---|---|
| **`csv/_seal_fork/_sigillo_archivio.py`** | `6c039a43` | **il sigillo `V0`-`V9` + `V6b`** dell'archivio. Gira anche **una voce sola**: `python … _sigillo_archivio.py V6` | **`12/12`**, `csv/_seal_fork/_sigillo_archivio_2026-09-19.txt` |
| **`csv/_seal_fork/_prova_D2_rigiocata.py`** | `b6297465` | la **prova del difetto `D2`** e, sullo stesso script, la prova della cura. Rileva la firma di `_db_serie_verifica` e **rovescia le attese** | **`7/7` prima** (`_prova_D2_rigiocata_2026-09-19.txt`, script `a3fad1a4`), **`8/8` dopo** (`_prova_D2_rigiocata_DOPO_2026-09-19.txt`) |
| **`csv/_seal_fork/_costo_archivio.py`** | `4efcc767` | il **costo**: `pickle.load` per snapshot, e `gzip` ai livelli 1/6/9 su uno snapshot **vero** | `csv/_seal_fork/_costo_archivio_2026-09-19.txt` |

### I comandi, verbatim

```
python csv/_seal_fork/_sigillo_archivio.py                    # il sigillo COMPLETO (12/12, ~6 min)
python csv/_seal_fork/_sigillo_archivio.py V6                 # una voce sola -- NON e' un sigillo
python csv/_seal_fork/_prova_D2_rigiocata.py                  # difetto D2 + cura, end-to-end
python csv/_seal_fork/_costo_archivio.py                      # il costo, su _pilota6000/pilota.pkl
```

**Un archivio a serie si produce così** *(il `.pkl` non si committa: questo comando È il dato)*:

```
python soliton_simulator.py --batch --sep 8 --seed 900 --passi 100 --ogni 50 \
    --csv <out>.csv --sync-db <dir>/stato.pkl --db-ogni 25 --db-serie
```
→ `stato_000025.pkl`, `…_000050`, `…_000075`, `…_000100`. **Con `.pkl.gz` lo snapshot è compresso**
*(livello 1)*. **Per INFITTIRE** senza rifare il run, **da 50 a 100 a cadenza 10**:

```
python soliton_simulator.py --batch --sep 8 --seed 900 --passi 100 --ogni 50 \
    --csv <out>.csv --sync-db <dir>/stato.pkl --db-ogni 10 --db-serie --db-rigioca 50 100
```
→ scrive `…_000060/70/80/90`, **salta `…_000100` che già esiste e lo CONTA**. A fine run:
`[db] ARCHIVIO: 4 snapshot scritti, 1 saltati (gia' presenti), 0 FALLITI.`

### I numeri, e quello che NON dicono

```
pickle.load di uno snapshot da 27.73 MB        0.156 s   (0.32 s se .gz)
gzip livello 1    0.82 s   16.08 MB   1.725x       <- CABLATO, per decisione di Luca
gzip livello 6    1.27 s   15.81 MB   1.755x
gzip livello 9    4.42 s   15.77 MB   1.759x       <- il default di gzip.open, mai scelto da nessuno
overhead DENTRO un run (V8):  +0.82 s/snapshot, +5.7 %   al livello 1
                              +2.66 s/snapshot, +16.1 %  al livello 9
```

> **`1.76x` è IL LIMITE DEL DATO, non del formato** *(float64 densi)*. **Per questo la proposta
> ibrida `pickle`+HDF5 è CHIUSA:** comprimerebbe gli stessi byte con gli stessi algoritmi.
> *(HDF5 era già stato scartato per due ragioni indipendenti: perde l'atomicità di `os.replace` e
> non serializza `rng_state`/`conc_nodi`.)*

**⚠ `V8` è misurato su una scena BREVE e NON si estrapola:** `+0.82 s` per snapshot qui contro i
`0.82 s` di una scrittura isolata da 27.73 MB — **coincidono per caso**, perché la rete a 100 passi
è piccola. Su una campagna il costo per snapshot **cresce col numero di nodi**.

---

## Gli strumenti della TOPOLOGIA (2026-09-20) — **quale script produce quale numero**

Tutti e tre leggono **solo** gli snapshot già in archivio: **nessun run, nessun `.pkl` nuovo**.
Simulatore blob `775ceab7`, seme 42, scena video a 3 masse.

| script | blob (byte grezzi) | esito | che numeri produce |
|---|---|---|---|
| `csv/_test_fork/_topologia_neonati.py` | `81b7be15` | `_topologia_neonati.txt` | **P0/P1** su 45 snapshot; le due coorti di grado-2 (`t0 = 600`, `1800`) seguite nel tempo col **controllo** dei grado≥3; il grado contro l'età ai passi 600/1800/2700 |
| `csv/_test_fork/_topologia.py` | `bae1313b` | `_topologia.txt` | istogramma completo dei gradi **con la valle vuota**; clustering **esatto** per quattro gruppi di grado; lunghezze e punti d'appoggio delle catene; la quinta misura (grado alto ⟷ nodi del passo 60) |
| `csv/_test_fork/_topologia_blocchi.py` | `40ab9e31` | `_topologia_blocchi.txt` | componenti del sottografo denso a **tre soglie**, densità interna, **archi diretti fra componenti**, e **la casella che decide**: capi della catena nello stesso pezzo o in due diversi |

> **⚠ `_topologia.py` e `_topologia_blocchi.py` NON sono ridondanti, e la distinzione è il reperto:**
> il primo misura che il **100 %** delle catene ha due punti d'appoggio **distinti**; il secondo che
> lo **0.00 %** ne ha due in **pezzi diversi**. **Sono compatibili, e solo il secondo risponde alla
> domanda del mandato.** Chi cita il primo da solo conclude l'opposto del vero.

**Le due componenti connesse del grafo intero e la densità al passo 6** *(riportate in
`doc/REFERTO_topologia.md` §1-2)* **non vengono da uno script committato**: sono due letture dirette
con `connected_components` sugli snapshot di `_g6000` e `_fin_A`, e **lo dichiaro invece di
attribuirle a uno strumento**. I numeri sono riproducibili da quegli snapshot in poche righe; il
fatto che il grafo abbia **4 componenti a tutti i passi** è comunque **ricalcolato da
`_topologia_blocchi.py`** sul sottografo denso, dove dà le stesse 4 componenti.

---

## Il VIDEO rigenerato dagli snapshot (2026-09-20) — **il `.mp4` non è committabile: ecco il comando**

`*.mp4` è ignorato da `.gitignore:6`, e **la regola non si forza**. Vale allora la stessa politica
dei `.pkl` (§5-quinquies): **il dato è il comando che lo produce**, e il sistema è deterministico —
qui ancora di più, perché **non c'è fisica**: si legge e si disegna.

| voce | valore |
|---|---|
| **comando, verbatim** | `python csv/_test_fork/_video_da_snapshot.py` *(aggiungere `--solo-primo` per il solo primo frame e il costo)* |
| **script** | `csv/_test_fork/_video_da_snapshot.py`, blob dei byte grezzi **`32606239`** |
| **simulatore** | blob **`775ceab7`** *(il disegno)* |
| **stati letti** | i 45 snapshot di `csv/_test_fork/_g6000`, blob **`7c4dec1d`** |
| **seme** | 42 · **scena** N-MASSE, `--nmasse 3 --sep 8` |
| **uscita** | `csv/_test_fork/_video_g6000/` — 45 `frame_%03d.png` + `video_g6000.mp4` (0.8 MB, 20 fps, 2.2 s) |
| **costo misurato** | pre-passata `10.9 s` + **`1.12 s/frame`** → **50 s** in tutto |
| **data** | 2026-09-20 |

**Committati: `frame_001.png` e `frame_045.png`** *(il primo e l'ultimo, cioè il confronto che
conta)*. **Gli altri 43 PNG no** — 8.5 MB che il comando rigenera in 50 secondi.

> **Cosa produce, e cosa NON è:** due pannelli per frame — il **campo** (`campo_spaziale`) e il
> **grafo** coi nodi colorati per **componente connessa**, luminosità dal pozzo `phi_g`
> (`pozzo_grafo`). **È uno strumento di ISPEZIONE: nessun numero che ne esce entra in un referto
> come risultato.** I numeri misurati stanno in `Z65`.
> **I controlli che stampa su ogni frame — 4 componenti, `0` archi fra componenti, `P0` su `0`
> nodi — sono controlli, e il testo diventa ROSSO se il conteggio non è zero.**

---

# RECUPERO DEL 2026-09-20 — **le 97 voci che mancavano**

> **Il conto PRIMA:** `79` strumenti in `csv/_test_fork/` + `45` sigilli in `csv/_seal_fork/`,
> **`27` in inventario** *(19 + 8)* = **il 22 %**. **`97` mancanti.**
> **⚠ E il conto da cui il mandato partiva — `81 / 34 / 47` — NON includeva `_seal_fork/`,**
> cioe' proprio i **sigilli**, che sono la categoria dove l'omissione costa di piu'.

> **IL TRIAGE E' QUELLO DEL par.5-novies, e NON e' burocrazia:** inventariare una sonda come
> un sigillo **gonfia il conto e nasconde i sigilli veri**.

> **⚠ ONESTA' SUL «COMANDO», e va letta prima di fidarsi:** dove lo strumento **non** legge
> `argv`, il comando e' **completo e verificato**. Dove lo legge, e' marcato
> **`+ ARGOMENTI DA VERIFICARE`**: **scrivere un comando inventato sarebbe peggio di non
> scriverlo**, perche' il prossimo lo rigirerebbe sbagliato credendolo giusto.

> **Il `blob` e' lo `sha1` dei BYTE GREZZI** *(mai `git hash-object`: par.5-quinquies)*,
> **al 2026-09-20**, ed e' il blob **del file**, non quello su cui e' stato girato l'ultima
> volta — **quello non e' recuperabile a posteriori, e lo dico invece di inventarlo**.


## SIGILLI (30) — voce COMPLETA

**⚠ LA RI-GIRABILITA' NON E' STATA VERIFICATA UNO PER UNO** *(e' la famiglia di `Z31`:
riferimenti in cartelle temporanee, snapshot cancellati nel `finally`, blob spariti)*.
**Dichiararla senza averla provata sarebbe un timbro falso.** Resta come lavoro aperto.

| strumento | blob (byte) | comando | cosa fa | esito |
|---|---|---|---|---|
| `csv/_seal_fork/_ab_chi_basc.py` | `c40cf1c6` | `python csv/_seal_fork/_ab_chi_basc.py` | (nessun docstring) | `_ab_chi_basc.txt` |
| `csv/_seal_fork/_ab_reciprocita.py` | `655a9f40` | `python csv/_seal_fork/_ab_reciprocita.py` **+ ARGOMENTI DA VERIFICARE** | (nessun docstring) | `_ab_reciprocita.txt` |
| `csv/_seal_fork/_sigillo_N.py` | `1b69f06a` | `python csv/_seal_fork/_sigillo_N.py` | ) | **nessun esito accanto** |
| `csv/_seal_fork/_sigillo_Y5_riscritto.py` | `adab8c60` | `python csv/_seal_fork/_sigillo_Y5_riscritto.py` **+ ARGOMENTI DA VERIFICARE** | (nessun docstring) | `_sigillo_Y5_riscritto.txt` |
| `csv/_seal_fork/_sigillo_anello.py` | `989a6992` | `python csv/_seal_fork/_sigillo_anello.py` | la STESSA legge di `ritmo()`, righe per righe. Se sbaglio, P1 FALLISCE: non passa in silenzio. | `_sigillo_anello.txt` |
| `csv/_seal_fork/_sigillo_calcpsi_T1.py` | `c1137f31` | `python csv/_seal_fork/_sigillo_calcpsi_T1.py` | (nessun docstring) | `_sigillo_calcpsi_T1.txt` |
| `csv/_seal_fork/_sigillo_calcpsi_T2.py` | `c71ab853` | `python csv/_seal_fork/_sigillo_calcpsi_T2.py` | (nessun docstring) | `_sigillo_calcpsi_T2.txt` |
| `csv/_seal_fork/_sigillo_chibasc_driver.py` | `bee78272` | `python csv/_seal_fork/_sigillo_chibasc_driver.py` | I flag come il MODULO li ha DOPO `_applica_flag`, non come il comando li chiedeva. | `_sigillo_chibasc_driver.txt` |
| `csv/_seal_fork/_sigillo_chicoop.py` | `05ff11e3` | `python csv/_seal_fork/_sigillo_chicoop.py` | SIGILLO di `CHI_COOP` nel SIMULATORE: `Z1` byte-identita' a flag spento, `Z1b` il ramo geometria IRRAGGIUNGIBILE, `Z2` le chiamate di `chiralita_core_locale` divise per array, `Z2b` **controllo positivo obbligatorio** (se i due array non differiscono mai il test e' VUOTO -> FAIL), `Z3` `perc_chi` == doppia copertura e `chi_basc` mai su `perc_chi`, `Z4` `len(perc_geom) == n`, `Z5` niente NaN. | `_sigillo_chicoop.txt` |
| `csv/_seal_fork/_sigillo_ramo_D.py` | `f884eff0` | `python csv/_seal_fork/_sigillo_ramo_D.py` | SIGILLO UNICO del RAMO D (le tre modifiche): `Z1` byte-identita' a tutti i flag spenti, `Z2` ogni flag DA SOLO produce un effetto (tre controlli positivi), `Z3` i criteri di `CHI_COOP`, **`Z4a` IL DECISIVO -- il vincolo NON CREA MOVIMENTO: nessun incremento >= 0 toccato e `max(dx_eff-dx) <= 0`, misurato a OGNI scrittura di TUTTO il run**, `Z4b` `min(d) >= LAM` e `min(d0) >= LAM`, `Z4c` stress finito, `Z4d` i casi patologici CONTATI e non tappati, `Z5` `|delta d0| <= passo_causale`, `Z6` niente NaN e lunghezze = `n`. | `_sigillo_ramo_D.txt` |
| `csv/_seal_fork/_sigillo_Z1c.py` | `f885e27e` | `python csv/_seal_fork/_sigillo_Z1c.py` | **`Z1c` [BLOCCANTE] -- la byte-identita' nella CONFIGURAZIONE VERA**: il simulatore di `0f4fc1e` con innestata SOLO la cura del mondo, contro quello di oggi, entrambi con l'**argv del FORK** e i tre flag del ramo D **spenti**. E' l'unico test che ATTRAVERSA la catena `CHI_CORE` e il campo `B` del passo spinoriale a flag spenti -- `Z1` con l'argv nudo non li esercita. Verifica anche che il test non sia VUOTO (contatore delle chiamate a `chiralita_core_locale`). | `_sigillo_Z1c.txt` |
| `csv/_seal_fork/_sigillo_chicoop_driver.py` | `45a93111` | `python csv/_seal_fork/_sigillo_chicoop_driver.py` | SIGILLO di `--chi-coop=on\|off` nel DRIVER: `D1` argv byte-identico a default, `D2` controllo positivo, `D3` il flag giusto letto DAL MODULO, `D4` nient'altro cambiato -- **`CHI_BASC` compreso: la cooperazione non lo spegne**. Isola il DRIVER, non il simulatore. | `_sigillo_chicoop_driver.txt` |
| `csv/_seal_fork/_sigillo_contatori_guardie.py` | `2ffef151` | `python csv/_seal_fork/_sigillo_contatori_guardie.py` | (nessun docstring) | `_sigillo_contatori_guardie.txt` |
| `csv/_seal_fork/_sigillo_coorti.py` | `93aaec70` | `python csv/_seal_fork/_sigillo_coorti.py` | LA RIGA DELLE SHAPE PRIMA DI TUTTO: max/A-B/ = 0 puo' significare NESSUN CONFRONTO. | `_sigillo_coorti.txt` |
| `csv/_seal_fork/_sigillo_correzioni.py` | `7e14d5c0` | `python csv/_seal_fork/_sigillo_correzioni.py` | Ritorna (xi_padre, xi_figlio) e i `xi` dei NEONATI, leggendoli nel momento GIUSTO. | `_sigillo_correzioni.txt` |
| `csv/_seal_fork/_sigillo_cs_floor.py` | `485829e2` | `python csv/_seal_fork/_sigillo_cs_floor.py` | righe ESEGUIBILI che usano GAMMA: niente commenti, niente stringhe di help. | `_sigillo_cs_floor.txt` |
| `csv/_seal_fork/_sigillo_d_arco.py` | `6ba08d61` | `python csv/_seal_fork/_sigillo_d_arco.py` | Occorrenze nel CODICE ESEGUIBILE, non nei commenti. | `_sigillo_d_arco.txt` |
| `csv/_seal_fork/_sigillo_denominatore.py` | `0dee44c5` | `python csv/_seal_fork/_sigillo_denominatore.py` | La forma PRE-CURA, ricostruita esplicitamente: e' il termine di paragone. | `_sigillo_denominatore.txt` |
| `csv/_seal_fork/_sigillo_inerzia.py` | `5f317518` | `python csv/_seal_fork/_sigillo_inerzia.py` | (nessun docstring) | `_sigillo_inerzia.txt` |
| `csv/_seal_fork/_sigillo_passo1_dieci.py` | `4876f063` | `python csv/_seal_fork/_sigillo_passo1_dieci.py` | (nessun docstring) | `_sigillo_passo1_dieci.txt` |
| `csv/_seal_fork/_sigillo_pesi.py` | `a0509686` | `python csv/_seal_fork/_sigillo_pesi.py` | ) | **nessun esito accanto** |
| `csv/_seal_fork/_sigillo_pezzo1.py` | `5071113f` | `python csv/_seal_fork/_sigillo_pezzo1.py` | Bloch di uno spinore (mappa di Pauli), stessa forma di _nb_grav. | **nessun esito accanto** |
| `csv/_seal_fork/_sigillo_pezzo2.py` | `23eb8330` | `python csv/_seal_fork/_sigillo_pezzo2.py` | ) | **nessun esito accanto** |
| `csv/_seal_fork/_sigillo_pezzo3.py` | `f03f67f0` | `python csv/_seal_fork/_sigillo_pezzo3.py` | ) | **nessun esito accanto** |
| `csv/_seal_fork/_sigillo_rep_spinta.py` | `7263607f` | `python csv/_seal_fork/_sigillo_rep_spinta.py` | (nessun docstring) | `_sigillo_rep_spinta.txt` |
| `csv/_seal_fork/_sigillo_rimozione5.py` | `1d67209e` | `python csv/_seal_fork/_sigillo_rimozione5.py` | (nessun docstring) | `_sigillo_rimozione5.txt` |
| `csv/_seal_fork/_sigillo_ripresa_scena.py` | `fe0eb6f2` | `python csv/_seal_fork/_sigillo_ripresa_scena.py` | (nessun docstring) | `_sigillo_ripresa_scena.txt` |
| `csv/_seal_fork/_sigillo_rumore_colorato.py` | `9e7dc7a5` | `python csv/_seal_fork/_sigillo_rumore_colorato.py` | tau_c -> 0 SOLO per la durata del passo spinoriale: fuori, CS_M resta quello vero. | `_sigillo_rumore_colorato.txt` |
| `csv/_seal_fork/_sigillo_scala_p.py` | `a0dae4e9` | `python csv/_seal_fork/_sigillo_scala_p.py` | (nessun docstring) | `_sigillo_scala_p.txt` |
| `csv/_seal_fork/_sigillo_sep_driver.py` | `012f6a49` | `python csv/_seal_fork/_sigillo_sep_driver.py` | (nessun docstring) | `_sigillo_sep_driver.txt` |
| `csv/_seal_fork/_sigillo_step2.py` | `1d12dd2b` | `python csv/_seal_fork/_sigillo_step2.py` | ) | **nessun esito accanto** |
| `csv/_seal_fork/_sigillo_taup_causale.py` | `2506052c` | `python csv/_seal_fork/_sigillo_taup_causale.py` | (nessun docstring) | `_sigillo_taup_causale.txt` |
| `csv/_seal_fork/_sigillo_turbo.py` | `02c7b0e4` | `python csv/_seal_fork/_sigillo_turbo.py` | ) | **nessun esito accanto** |
| `csv/_seal_fork/_sigillo_twist_nodo.py` | `9274ef75` | `python csv/_seal_fork/_sigillo_twist_nodo.py` | (nessun docstring) | `_sigillo_twist_nodo.txt` |

## SONDE con esito committato accanto (61) — UNA riga

**Il risultato ESISTE accanto allo strumento.** Per queste il par.5-novies chiede
**una riga che dica DOVE sta l'esito**, non una voce completa.

| strumento | blob (byte) | comando | cosa fa | esito |
|---|---|---|---|---|
| `csv/_seal_fork/_diagnosi_porte_Y5.py` | `32561762` | `python csv/_seal_fork/_diagnosi_porte_Y5.py` | (nessun docstring) | `_diagnosi_porte_Y5.txt` |
| `csv/_seal_fork/_fdt_scuotimento.py` | `a9bf1dc3` | `python csv/_seal_fork/_fdt_scuotimento.py` | ESATTAMENTE `:2016-2021` (Rodrigues): ruota n ATTORNO a omega. Conserva /n/ e l'angolo n-omega. | **nessun esito accanto** |
| `csv/_seal_fork/_reperto_inerzia.py` | `480d9a34` | `python csv/_seal_fork/_reperto_inerzia.py` | ) | **nessun esito accanto** |
| `csv/_seal_fork/_rigioca_finestre.py` | `d4b32fae` | `python csv/_seal_fork/_rigioca_finestre.py` | (nessun docstring) | `_rigioca_finestre.txt` |
| `csv/_seal_fork/_u7_separazione_scale.py` | `664724c2` | `python csv/_seal_fork/_u7_separazione_scale.py` | (nessun docstring) | `_u7_separazione_scale.txt` |
| `csv/_seal_fork/_verifica_finestra_patch.py` | `56946ffd` | `python csv/_seal_fork/_verifica_finestra_patch.py` **+ ARGOMENTI DA VERIFICARE** | (nessun docstring) | `_verifica_finestra_patch.txt` |
| `csv/_test_fork/_Y_nel_vuoto.py` | `b7ec7f46` | `python csv/_test_fork/_Y_nel_vuoto.py` **+ ARGOMENTI DA VERIFICARE** | (nessun docstring) | **nessun esito accanto** |
| `csv/_test_fork/_Z33_due_vie.py` | `7d1f6717` | `python csv/_test_fork/_Z33_due_vie.py` | (nessun docstring) | `_Z33_due_vie.txt` |
| `csv/_test_fork/_Z36_cucitura.py` | `1f0bf98e` | `python csv/_test_fork/_Z36_cucitura.py` | (nessun docstring) | `_Z36_cucitura.txt` |
| `csv/_test_fork/_analisi7_assiomi.py` | `c356bbc1` | `python csv/_test_fork/_analisi7_assiomi.py` | (nessun docstring) | `_analisi7_assiomi.txt` |
| `csv/_test_fork/_analisi_tw.py` | `a3b092e9` | `python csv/_test_fork/_analisi_tw.py` | (nessun docstring) | `_analisi_tw.txt` |
| `csv/_test_fork/_anello_sfasato.py` | `555b5763` | `python csv/_test_fork/_anello_sfasato.py` | (nessun docstring) | `_anello_sfasato.txt` |
| `csv/_test_fork/_audit_A8.py` | `c7b058f6` | `python csv/_test_fork/_audit_A8.py` | (nessun docstring) | `_audit_A8.txt` |
| `csv/_test_fork/_audit_default.py` | `3ef9ff63` | `python csv/_test_fork/_audit_default.py` | (nessun docstring) | `_audit_default.txt` |
| `csv/_test_fork/_campagna_csfloor.py` | `1c74b90d` | `python csv/_test_fork/_campagna_csfloor.py` | (nessun docstring) | `_campagna_csfloor.txt` |
| `csv/_test_fork/_campagna_step2.py` | `d05a6749` | `python csv/_test_fork/_campagna_step2.py` | (nessun docstring) | `_campagna_step2.txt` |
| `csv/_test_fork/_canali_disordine.py` | `cec06613` | `python csv/_test_fork/_canali_disordine.py` **+ ARGOMENTI DA VERIFICARE** | (nessun docstring) | **nessun esito accanto** |
| `csv/_test_fork/_chi_non_invecchia.py` | `44611f63` | `python csv/_test_fork/_chi_non_invecchia.py` | (nessun docstring) | `_chi_non_invecchia.txt` |
| `csv/_test_fork/_chi_non_ruota.py` | `135ac307` | `python csv/_test_fork/_chi_non_ruota.py` | nodi FERMI contro TUTTI, nello STESSO istante e sulla STESSA popolazione (A3c). | `_chi_non_ruota.txt` |
| `csv/_test_fork/_classifica_guardie.py` | `318d6cd1` | `python csv/_test_fork/_classifica_guardie.py` | il commit che ha INTRODOTTO la riga: `git log -S`, PRIMA riga dell'output. | `_classifica_guardie.txt` |
| `csv/_test_fork/_conta_psi_spin_prec.py` | `7b7fd5fc` | `python csv/_test_fork/_conta_psi_spin_prec.py` | (nessun docstring) | `_conta_psi_spin_prec.txt` |
| `csv/_test_fork/_contrasto_step2.py` | `98f787f3` | `python csv/_test_fork/_contrasto_step2.py` | (nessun docstring) | `_contrasto_step2.txt` |
| `csv/_test_fork/_crescita_omega.py` | `cfb77b43` | `python csv/_test_fork/_crescita_omega.py` **+ ARGOMENTI DA VERIFICARE** | (nessun docstring) | `_crescita_omega.txt` |
| `csv/_test_fork/_cronologia.py` | `2634c749` | `python csv/_test_fork/_cronologia.py` **+ ARGOMENTI DA VERIFICARE** | Il punto di attraversamento, con la regola fissata PRIMA. | `_cronologia.txt` |
| `csv/_test_fork/_diagnosi_peq_nascita.py` | `2adb1c29` | `python csv/_test_fork/_diagnosi_peq_nascita.py` | (nessun docstring) | `_diagnosi_peq_nascita.txt` |
| `csv/_test_fork/_dump_snapshot.py` | `0974b224` | `python csv/_test_fork/_dump_snapshot.py` **+ ARGOMENTI DA VERIFICARE** | Solo dove serve davvero il MODULO (ampiezze, norme): lo dichiara chi lo chiama. | **nessun esito accanto** |
| `csv/_test_fork/_estensivita_grado.py` | `c1f66b33` | `python csv/_test_fork/_estensivita_grado.py` | Le DUE MODE separate: mai un fit, mai una media fra popolazioni distinte. | `_estensivita_grado.txt` |
| `csv/_test_fork/_f_e_median.py` | `cd1ad7e4` | `python csv/_test_fork/_f_e_median.py` | (nessun docstring) | `_f_e_median.txt` |
| `csv/_test_fork/_forma_Y.py` | `180f36c2` | `python csv/_test_fork/_forma_Y.py` **+ ARGOMENTI DA VERIFICARE** | (nessun docstring) | **nessun esito accanto** |
| `csv/_test_fork/_freq_riferimento.py` | `4e3a84a8` | `python csv/_test_fork/_freq_riferimento.py` | la STESSA formula di _tempo_luce_nodo (:3036-3044): media di `d` sugli archi incidenti. | `_freq_riferimento.txt` |
| `csv/_test_fork/_gate_bonifica.py` | `5289eec4` | `python csv/_test_fork/_gate_bonifica.py` | La domanda e' sempre la stessa: e' concentrata su 1, o ha struttura? | `_gate_bonifica.txt` |
| `csv/_test_fork/_gauge_degenere.py` | `b1ca7968` | `python csv/_test_fork/_gauge_degenere.py` | (nessun docstring) | `_gauge_degenere.txt` |
| `csv/_test_fork/_gauge_vuoto.py` | `72c4c39e` | `python csv/_test_fork/_gauge_vuoto.py` | proiezione arco->nodo di `peq`: la STESSA forma gia' usata a :2295-2297. | `_gauge_vuoto.txt` |
| `csv/_test_fork/_lettura_braccio_ON.py` | `f83ec9d1` | `python csv/_test_fork/_lettura_braccio_ON.py` **+ ARGOMENTI DA VERIFICARE** | valore della colonna all'ultimo campione, o al passo chiesto. | `_lettura_braccio_ON.txt` |
| `csv/_test_fork/_letture_ab.py` | `4e14a227` | `python csv/_test_fork/_letture_ab.py` | olonomia FIRMATA, berry, e `coer_l`. IMPORTA IL SIMULATORE: si gira a run FINITI. | **nessun esito accanto** |
| `csv/_test_fork/_maturazione.py` | `b8f5708d` | `python csv/_test_fork/_maturazione.py` **+ ARGOMENTI DA VERIFICARE** | (nessun docstring) | **nessun esito accanto** |
| `csv/_test_fork/_mediana_ritmo.py` | `d8f5c054` | `python csv/_test_fork/_mediana_ritmo.py` | (nessun docstring) | `_mediana_ritmo.txt` |
| `csv/_test_fork/_misura_Z24.py` | `4b4af172` | `python csv/_test_fork/_misura_Z24.py` | /sum/ / max/./ su un array (n,) o (n,3): per i vettori si usa la NORMA della somma. | `_misura_Z24.txt` |
| `csv/_test_fork/_misura_denominatore.py` | `536494fe` | `python csv/_test_fork/_misura_denominatore.py` | (nessun docstring) | `_misura_denominatore.txt` |
| `csv/_test_fork/_misura_tw.py` | `1316b5ca` | `python csv/_test_fork/_misura_tw.py` **+ ARGOMENTI DA VERIFICARE** | (nessun docstring) | `_misura_tw.txt` |
| `csv/_test_fork/_misure_run6000.py` | `718cd94d` | `python csv/_test_fork/_misure_run6000.py` **+ ARGOMENTI DA VERIFICARE** | ramp = min(1, eta/TAU_A). LA LEGGE E' DEL CODICE (:2649), non una definizione mia. | **nessun esito accanto** |
| `csv/_test_fork/_misure_scala_p.py` | `c10f3464` | `python csv/_test_fork/_misure_scala_p.py` | median(tanh(/dpozzo/ / phi_arc)) -- quello che la CURA produrrebbe. | `_misure_scala_p.txt` |
| `csv/_test_fork/_parentela_bloch.py` | `d8174393` | `python csv/_test_fork/_parentela_bloch.py` **+ ARGOMENTI DA VERIFICARE** | Angolo fra due direzioni, in gradi. Nessuna normalizzazione assunta. | **nessun esito accanto** |
| `csv/_test_fork/_passo198.py` | `5267eaf0` | `python csv/_test_fork/_passo198.py` **+ ARGOMENTI DA VERIFICARE** | (nessun docstring) | `_passo198.txt` |
| `csv/_test_fork/_pilota_sep.py` | `631ebf44` | `python csv/_test_fork/_pilota_sep.py` | Il LIGNAGGIO dei nodi nati dopo la semina, e dichiaro come. | **nessun esito accanto** |
| `csv/_test_fork/_retroazione_r.py` | `c27e279a` | `python csv/_test_fork/_retroazione_r.py` | pendenza PARZIALE su x1 tenendo x2 fisso (due regressori + intercetta). | `_retroazione_r.txt` |
| `csv/_test_fork/_rimisura_Z9.py` | `cd2c76b7` | `python csv/_test_fork/_rimisura_Z9.py` **+ ARGOMENTI DA VERIFICARE** | Restituisce la traiettoria di ramp/eta. `scena` costruisce e restituisce la rete. | `_rimisura_Z9.txt` |
| `csv/_test_fork/_scansione_schemi.py` | `27d9e2db` | `python csv/_test_fork/_scansione_schemi.py` | Mappa riga -> nome della funzione che la contiene (la piu' interna). | `_scansione_schemi.txt` |
| `csv/_test_fork/_scelta_denominatore.py` | `4f4ad994` | `python csv/_test_fork/_scelta_denominatore.py` | (nessun docstring) | `_scelta_denominatore.txt` |
| `csv/_test_fork/_scena_video_ripresa.py` | `e68bb8c5` | `python csv/_test_fork/_scena_video_ripresa.py` | (nessun docstring) | **nessun esito accanto** |
| `csv/_test_fork/_scomposizione_L.py` | `580fbb05` | `python csv/_test_fork/_scomposizione_L.py` | (nessun docstring) | `_scomposizione_L.txt` |
| `csv/_test_fork/_semi_spin_feedback.py` | `a18cd12d` | `python csv/_test_fork/_semi_spin_feedback.py` | (nessun docstring) | `_semi_spin_feedback.txt` |
| `csv/_test_fork/_somme.py` | `5ec2372f` | `python csv/_test_fork/_somme.py` | (nessun docstring) | `_somme.txt` |
| `csv/_test_fork/_sonda_2706.py` | `b350f651` | `python csv/_test_fork/_sonda_2706.py` | (nessun docstring) | `_sonda_2706.txt` |
| `csv/_test_fork/_sonda_eta_ramp.py` | `c4ca14ac` | `python csv/_test_fork/_sonda_eta_ramp.py` **+ ARGOMENTI DA VERIFICARE** | Chiamata da step:3018 PRIMA dell'incremento di eta: e' li' che si misura. | `_sonda_eta_ramp.txt` |
| `csv/_test_fork/_tassi_coppie.py` | `9b152fc4` | `python csv/_test_fork/_tassi_coppie.py` **+ ARGOMENTI DA VERIFICARE** | Prima eta' in cui <chi> raggiunge 1-1/e del percorso verso 90 gradi, con interpolazione | **nessun esito accanto** |
| `csv/_test_fork/_tre_cricchetti.py` | `07ececc0` | `python csv/_test_fork/_tre_cricchetti.py` **+ ARGOMENTI DA VERIFICARE** | (nessun docstring) | `_tre_cricchetti.txt` |
| `csv/_test_fork/_verdetto_baseline.py` | `d063f797` | `python csv/_test_fork/_verdetto_baseline.py` | (nessun docstring) | `_verdetto_baseline.txt` |
| `csv/_test_fork/_verifica_inerzia1.py` | `480b6f02` | `python csv/_test_fork/_verifica_inerzia1.py` | (nessun docstring) | `_verifica_inerzia1.txt` |
| `csv/_test_fork/_verifiche_inerzia.py` | `18012f00` | `python csv/_test_fork/_verifiche_inerzia.py` | (nessun docstring) | `_verifiche_inerzia.txt` |
| `csv/_test_fork/_verifiche_ramp.py` | `ba371915` | `python csv/_test_fork/_verifiche_ramp.py` | (nessun docstring) | `_verifiche_ramp.txt` |

## ⚠ STRUMENTI SENZA ESITO REPERIBILE (5)

**⚠ E NESSUNO DI QUESTI E' UN REPERTO — la parola giusta conta, e la prima che avevo usato era
SBAGLIATA.**

Il mandato chiama **REPERTO** *«una misura fatta e mai scritta»*. **Sono andato a cercarli, e non
ce ne sono.**

**DUE MISURE INDIPENDENTI, e la seconda ha corretto la prima:**
- **la veloce** — *«esiste un file di esito accanto allo strumento?»* — dava **17** candidati, poi
  **11 falsi positivi**, quindi **6**;
- **la lenta** — *«lo strumento e' nominato in un messaggio di commit?»* — dice che **16 dei 17 lo
  sono**, e il diciassettesimo (`_verifica_finestra_patch.py`) ha il suo `.txt` accanto.

> **Per il criterio «esito accanto OPPURE nominato in un commit»: ZERO reperti su 17.**
> **Nessun risultato e' andato perduto.**

**Quello che manca a questi `5` e' il FILE DI ESITO accanto allo strumento, non il risultato.**
**E la lezione di metodo e' la piu' utile del giro:** il classificatore veloce sbagliava **quasi
due su tre**, e **se mi fossi fermato alla prima misura avrei scritto nel registro cinque «reperti»
che non esistono** — cioe' avrei creato lavoro fantasma **dentro il documento che serve a togliere
il lavoro fantasma.**

| strumento | blob (byte) | comando | cosa fa | esito |
|---|---|---|---|---|
| `csv/_test_fork/_autocorr_bloch.py` | `5681f628` | `python csv/_test_fork/_autocorr_bloch.py` | (nessun docstring) | **nessun esito accanto** |
| `csv/_test_fork/_conformita_e_verdetto.py` | `8c378f03` | `python csv/_test_fork/_conformita_e_verdetto.py` | (nessun docstring) | **nessun esito accanto** |
| `csv/_test_fork/_pilota_eta.py` | `d5c69ee0` | `python csv/_test_fork/_pilota_eta.py` | (nessun docstring) | **nessun esito accanto** |
| `csv/_test_fork/_pilota_scena6000.py` | `91da82d5` | `python csv/_test_fork/_pilota_scena6000.py` **+ ARGOMENTI DA VERIFICARE** | (nessun docstring) | **nessun esito accanto** |
| `csv/_test_fork/_sonda_rho_zero.py` | `8efca84e` | `python csv/_test_fork/_sonda_rho_zero.py` **+ ARGOMENTI DA VERIFICARE** | (nessun docstring) | **nessun esito accanto** |

## INFRASTRUTTURA (1) — non e' ne' sigillo ne' sonda

**Non produce una misura propria:** e' un modulo che altri sigilli caricano.
Il mio classificatore l'aveva messo fra i reperti: **errore di categoria, corretto a mano**.

| strumento | blob (byte) | comando | cosa fa | esito |
|---|---|---|---|---|
| `csv/_seal_fork/_runner_sim.py` | `368e6caa` | `python csv/_seal_fork/_runner_sim.py` | (nessun docstring) | **nessun esito accanto** |


## Aggiunto il 2026-09-20 -- par.5-novies regola (1): NELLO STESSO COMMIT dello strumento

| strumento | blob (byte) | comando | cosa fa | esito |
|---|---|---|---|---|
| `csv/_test_fork/_fuga_vd.py` | `2035429e` | `python csv/_test_fork/_fuga_vd.py` | serie nel tempo di `|vd|` (p50/p99/p999/max), `n3`, conteggi a cinque soglie, **identita' Jaccard** dei primi 100 archi veloci, e dove stanno (`d/d0`, `perc_chi`, `eta`). SONDA: un `.pkl` alla volta, solo numpy per-arco. | par.2 di `doc/TASK_HISTORY/2026-09-20_fuga-vd-ramoB.md` |

| `csv/_test_fork/_venti_archi.py` | `cee10eb5` | `python csv/_test_fork/_venti_archi.py` | i 20 archi con `|vd|` massimo (indice, nodi, `d`, `d0`, `d/d0`, e per ogni nodo `_deg`/`eta`/`perc_chi`/`|psi|`/`|omega_s|`); la loro INTERSEZIONE fra istanti (per coppia di nodi, non per indice); e la distribuzione di `_deg` separata ORIGINALI/NATI. SONDA. | par.2 di `doc/TASK_HISTORY/2026-09-20_venti-archi-e-nsub.md` |

| `csv/_test_fork/_innesco_cinque.py` | `7e0ec88f` | `python csv/_test_fork/_innesco_cinque.py` | PARTE 1 della caccia all innesco: i cinque nodi persistenti (16, 481, 621, 627, 837) al passo 120 contro il 240 del ramo B, con il RANGO PERCENTILE di ogni campo nella popolazione, e i loro archi (d/d0, |vd|, tau derivato). SOLO LETTURA di due .pkl. | `doc/REFERTO_innesco_cinque.md` |


---

## ⚠ I `.pkl` DEI DUE RUN A/B a `sep = 4.0` — **aggiunti il 2026-09-20, e la voce ERA MANCANTE**

> **`CLAUDE.md` par.5-quinquies: «un `.pkl` senza il suo comando non e' un dato».** La regola chiede
> che la voce sia scritta **NELLO STESSO COMMIT** in cui il `.pkl` nasce.
> **⚠ NON L'HO FATTO: i due run giravano da oltre due ore e questa voce non esisteva.**
> **E' un'omissione mia, non una scelta**, ed e' esattamente la classe di difetto che il par.5-novies
> che ho scritto stamattina dovrebbe impedire — **e che una REGOLA SCRITTA, da sola, non impedisce
> (`A9`).**

**I `.pkl` non si committano** (binari, ~35 MB l'uno; **`16` in A + `3` in B = `673 MB` finora**).
**Ma il sistema e' DETERMINISTICO: il dato E' il comando che lo produce.**

| | |
|---|---|
| **archivi** | ⚠ **SPOSTATI SU `E:` il 2026-09-21** *(archivio freddo, `Z89`)*: `E:\soliton_archivio\csv\_test_fork\_ab_A\scena_??????.pkl.gz`. `_ab_B` e' sotto i 300 MB e **resta su `C:`**: `csv/_test_fork/_ab_B/scena_??????.pkl.gz`. **⚠ IL COMANDO QUI SOTTO NON E' STATO CAMBIATO, di proposito:** e' la riga che RIGENERA l'archivio, e un run scrive su `C:`. Cambiarla la renderebbe sbagliata. **La posizione dell'archivio e il comando che lo produce sono due cose diverse.** |
| **cadenza** | uno ogni **20 frame = 120 passi** di motore (`--serie=20`), numerati **col passo** |
| **SEME** | **`42`** *(letto dal blocco di testa del `prog.csv`, non assunto)* |
| **BLOB del simulatore** | **`edb8f844`** *(sha1 dei BYTE GREZZI — **non** `git hash-object`)* · git-blob `b44f50ce` |
| **BLOB del driver** | **`9aee4fc2`** *(`csv/_test_fork/_scena_video.py`, con `--chi-basc=on\|off`)* — **⚠ SUPERATO il 2026-09-21: il driver e' ora `4d31ddee`**, e **SUPERATO DI NUOVO il 2026-09-24: e' `7ef26b3f`**, con il **referto di configurazione** *(`CONFIGURAZIONE.txt`/`.json` nella cartella del run, e il driver RIFIUTA DI PARTIRE se non riesce a scriverlo)*. **⚠ Da questa data l'argv NON e' piu' identico elemento per elemento a quello dei run precedenti?** NO: l'argv non cambia affatto -- il referto non aggiunge opzioni, LEGGE. Cio' che cambia e' che nella cartella compaiono due file in piu', con `--chi-coop=on\|off` (default `off`). **I due run A/B qui sotto restano riproducibili VERBATIM**: a default l'argv e' identico elemento per elemento, e lo prova `csv/_seal_fork/_sigillo_chicoop_driver.py`, non questa nota. |
| **passi previsti** | **3000** per ramo (500 frame x 6) |
| **data** | avvio **2026-09-20 16:26:50** *(`doc/STATO_RUN.md`, voce `ab_sep4_A_e_B`)* |

**LE DUE RIGHE DI COMANDO, VERBATIM:**
```
ramo A  (chi_basc ACCESO, il default)
python csv/_test_fork/_scena_video.py 500 csv/_test_fork/_ab_A --sep=4.0 --serie=20 --csv-progresso=csv/_test_fork/_ab_A/prog.csv

ramo B  (chi_basc SPENTO)
python csv/_test_fork/_scena_video.py 500 csv/_test_fork/_ab_B --sep=4.0 --serie=20 --csv-progresso=csv/_test_fork/_ab_B/prog.csv --chi-basc=off
```

**⚠ E DUE COSE CHE SERVONO PER RIFARLI DAVVERO, e che il comando da solo non dice:**
- **il `prog.csv` di ciascun ramo PORTA GIA' blob, seme e venti flag nel suo blocco di testa (P6)** —
  quindi **quello** e' il file che certifica il run, non il nome della cartella;
- **`--chi-basc=on` e' il DEFAULT**: il ramo A si ottiene **omettendo** l'opzione. *(Il sigillo
  `_sigillo_chibasc_driver.py` prova che a default il driver e' byte-identico a quello di `bb1d727`:
  `C1`, 142 campi confrontati, 0 diversi.)*

| `csv/_punto_ripresa.py` | `f8ef1f0c` | `python csv/_punto_ripresa.py doc/_corpo_punto_ripresa.md` | RIGENERA per intero il blocco **PUNTO DI RIPRESA** in cima a `doc/STATO_RUN.md`, fra due marcatori HTML, sostituendo `@@HEAD@@` e `@@ORA@@`. Serve al vincolo del riavvio notturno: **il blocco non si accumula e non c'e' niente da cancellare a mano**. | `doc/STATO_RUN.md`, in testa |
| `csv/_deriva_anom_simm.py` | `5215a7e2` | `python csv/_deriva_anom_simm.py` | DERIVA la forma `anom = 2(rho-peq)/(rho+peq)` sui casi limite PRIMA di scriverla, come chiede il mandato: coincidenza con la forma vecchia per anomalie piccole, il caso `peq -> 0`, il caso `0/0`, e i casi con `peq` NEGATIVO misurati da Z94. Genera da codice la tabella che altrimenti si ricopierebbe a mano (P1-ter). | `doc/REFERTO_istanti_scala_min_coes_adim.md` e `csv/_test_fork/_diag_D/DERIVAZIONE_anom_simm.txt` |
| `csv/_test_fork/_peq_dentro_1126.py` | `8eb40fd1` | `python csv/_test_fork/_peq_dentro_1126.py --da=1080 --fino=1126` | **I TRE NUMERI** sull'aggiornamento di `peq` al passo che esplode: **`max(dt_e/tau_bg_loc)`** *(il gemello di `_taup_cfl_max`, che su `d0` esiste da sempre e su `peq` non esisteva)*, **quanti archi finiscono con `peq < 0`**, e **quale dei due termini di `:4206` ce li porta** *(i due esiti calcolati CONTROFATTUALMENTE e a parte)*. Piu' l'arco peggiore col dettaglio completo. **NON integra il passo esplosivo**: `FERMA_DOPO_NSUB`. | `csv/_test_fork/_diag_D/PEQ_DENTRO_001126.txt` |
| `csv/_test_fork/_video_val600.py` | `fe3835cb` | `python csv/_test_fork/_video_val600.py` *(prova rapida: `--prova`)* | **IL VIDEO DEL RUN DI VALIDAZIONE.** Rigioca dalla semina con la configurazione della validazione **byte per byte**, un fotogramma ogni **6** passi *(100 fotogrammi)*, e **VERIFICA al passo 600 che lo stato coincida con `scena_000600.pkl.gz`** -- *se non coincide NON monta il video e lo dice*. Due pannelli: la RETE *(archi per `d/d0`, nodi per regione)* e le MEDIANE nel tempo. **Scala dei colori FISSA** `d/d0 in [0.5, 1.5]` con `1` al centro *(il punto neutro FISICO)*: riscalarla per fotogramma farebbe **sparire un cambiamento vero**. **Ogni fotogramma porta la riga «posizioni = DISEGNO (`Z47`); colori = FISICA».** Esce su `E:\soliton_archivio\`, **non in git**. | `E:\soliton_archivio\video_val600\REFERTO.txt` |
| `csv/_test_fork/_quanto_conta_il_disegno.py` | `84732180` | `python csv/_test_fork/_quanto_conta_il_disegno.py` | **`G1`: QUANTO CONTA IL DISEGNO.** `L_disegno/d` arco per arco *(`L_disegno` calcolata **esattamente come `pozzo_grafo`**, da `pos`)*: distribuzione, **per REGIONE**, **nel tempo**, e la **correlazione con la distanza dal CENTRO del disegno** -- se dipende, **il disegno impone un centro a una legge che non dovrebbe averne**. La soglia e' **`3/sqrt(N)`, il valore sotto ipotesi nulla a 3 sigma, non scelta**, e **il criterio e' COLLAUDATO su due casi a risposta nota** *(`P1-sexies`)*. **SOLA LETTURA.** | `csv/_test_fork/_diag_D/QUANTO_CONTA_IL_DISEGNO.txt` |
| `csv/_test_fork/_somma_per_scrittore_d0.py` | `0c1197b1` | `python csv/_test_fork/_somma_per_scrittore_d0.py --passi=120` | **CHI FA SCAPPARE `d0`.** Somma per scrittore, **SALITE e DISCESE separate** *(un saldo piccolo puo' nascere da due termini enormi che quasi si cancellano: il saldo da solo non distingue)*, piu' per `S09`/`S10` il **rapporto fra il loro saldo e `median(d0)`** e la **pendenza** contro di esso. **NON tocca il simulatore:** SOSTITUISCE `_traccia_d0` con una funzione pure-read allo stesso punto di chiamata. I siti che CONCATENANO portano `n/d`, dichiarato. **SOLA MISURA.** | `csv/_test_fork/_diag_D/SOMMA_PER_SCRITTORE_d0.txt` |
| `csv/_test_fork/_componenti_e_tempo.py` | `15e17d48` | `python csv/_test_fork/_componenti_e_tempo.py` | **`D27` e `D25` SENZA NESSUN RUN.** Le **componenti connesse** del grafo per ogni archivio e ogni snapshot *(union-find, zero dipendenze)*: quante, nodi e archi in ciascuna, la composizione per regione, e **`med d0` / `med d` / `med d/d0` PER COMPONENTE** — cioe' **se la crescita di `d0` e' la stessa in tutte**. E **la domanda di Luca: le tre masse stanno in componenti diverse?** Piu' `D25`: la distribuzione di **`_r_corrente`**, **quanti nodi non integrano** e **quanta parte del tempo proprio totale portano** *(il confronto e' col nodo MEDIANO, non con una soglia scelta)*. **SOLA LETTURA su snapshot: gira mentre un run e' in corso.** Tre collaudi, e il secondo e' quello che DEVE fallire. | `csv/_test_fork/_diag_D/COMPONENTI_E_TEMPO.md` |
| `csv/_test_fork/_g4_prova.py` | **`454b0562`** *(era `b9642633`: aggiunti i modi `--fase-2pi` e `--fase-2pi-corto`)* | `--controllo` *(120 passi)*, poi `--riferimento` e `--spegni` *(600 passi)* | **`G4`: la prova di spegnimento della MEMORIA DEL MOTO, col BILANCIO COMPLETO di `d0`.** Oltre agli scrittori di `Z102`, misura **il FRENO** *(avvolge `_smorza`, e conta solo `d0_passo`: le altre chiamate stanno dentro siti gia' tracciati e si conterebbero due volte)*, **le NASCITE** e **le MORTI** *(fotografia delle CHIAVI `(i,j)` a inizio e fine passo)*. **CRITERIO scritto PRIMA: `Δ(somma d0) = scritture + freno + nascite - morti`, entro `1e-9` relativo alla SCALA dei termini** *(non al `Δ`, che puo' essere ~0 per cancellazione)*. **Se non chiude, la prova non si legge.** Cinque collaudi, **quattro dei quali DEVONO fallire**. **NON tocca simulatore ne' driver.** | `csv/_test_fork/_g4_*/BILANCIO_d0.txt` · `.csv` |
| **`csv/_configurazione.py`** | **`9ef011b2`** | `python csv/_configurazione.py` *(il COLLAUDO; il referto lo scrive il driver, non si invoca a mano)* | **IL REFERTO DI CONFIGURAZIONE DI UN RUN.** Scrive `CONFIGURAZIONE.txt` e `.json` nella cartella del run: **lo stato EFFETTIVO di tutti i flag di modulo, letto DAL MODULO dopo `_applica_flag`**, i due argv **VERBATIM** *(quello del processo e quello passato al simulatore, che NON sono lo stesso)*, `sha1` dei **byte grezzi** di simulatore e driver, seme, `HEAD` e se l'albero e' pulito. **I nomi vengono dall'AST** *(assegnamenti di MODULO con nome MAIUSCOLO: `123` trovati)*, **non da una lista a mano** -- nel driver ce n'era una di `24`. **Il driver RIFIUTA DI PARTIRE se non riesce a scriverlo.** **Collaudo `6/6`, con DUE casi che devono fallire** *(`K3`: letto PRIMA di `_applica_flag` darebbe il DEFAULT; `K5`: una `dest` inesistente deve SOLLEVARE)*, **piu' `K6`, che verifica DALL'AST che nel driver `scrivi()` venga DOPO `_applica_flag`** -- e `K6` ha davvero FALLITO prima che il cablaggio esistesse. | `<cartella del run>/CONFIGURAZIONE.txt` · `.json` |
| **`csv/_test_fork/_ricostruisci_config.py`** | **`0fd8b254`** | `python csv/_test_fork/_ricostruisci_config.py` | **LA RICOSTRUZIONE DELLA CONFIGURAZIONE DEI RUN GIA' FATTI**, tabella **generata** flag × run su **11 campagne** *(`G1`, `G2`, validazione 600, `G3` ×2, `G4` ×3, `G4-bis`, `D34`, `FASE_2PI` corto)*. **Tre fonti, e ogni cella porta la SUA:** l'**argv** dal driver committato a quel commit · il **banner** del log *(stato EFFETTIVO dal modulo, ma sono 24 flag su 123)* · il **default del blob di quel run** *(`git cat-file -p <commit>:soliton_simulator.py`)*, **valido solo se nessuna opzione lo cambia -- e questo si VERIFICA**, ricavando dall'AST di `_applica_flag` l'opzione che scrive quel flag e cercandola nei lanciatori committati. **Il commit di ogni run viene DALLO SNAPSHOT**, non dal log. **Le contraddizioni fra fonti si riportano ENTRAMBE**, e quelle che nessuna opzione spiega sono marcate `*** NON SPIEGATA ***`. **Cio' che non si ricostruisce e' `NON RICOSTRUITO`, col motivo.** **SOLA LETTURA.** | `csv/_test_fork/_RICOSTRUZIONE_config.txt` |
| **`csv/_test_fork/_mappa_4pi.py`** | **`ff17daa3`** *(era `9a53f27b`: grafo corretto, l'orologio viene dallo SPINORE)* | `python csv/_test_fork/_mappa_4pi.py` | **LA MAPPA DEL `4pi`: di CHI e' la doppia copertura, punto per punto.** Quattro classi **`VERA`** *(dello spinore: fisica)* · **`DICHIARATA`** *(il dominio di `phi`: una convenzione)* · **`EREDITATA`** *(chi prende la scala da `phi`)* · **`INVERSA`** *(il finto che pilota il vero)*, con **precedenza dichiarata** `INVERSA > VERA > DICHIARATA > EREDITATA`. **RIUSA `_censimento_fasi.py` (`Z118`)** e **aggiunge una SPAZZATA** per i siti che `Z118` non vede *(cerca i multipli di `pi` come LETTERALI, e `FASE_2PI` li ha riscritti in `self._dphi()`)*. **Contagio da `tw` con chiusura e mutazione IN PLACE** *(`np.add.at`)*, **insensibile al flusso e lo dichiara**. Stato **EFFETTIVO** dal referto di configurazione generato. **Collaudo `7/7`, con DUE casi che devono fallire.** **SOLA LETTURA.** | `csv/_test_fork/_diag_D/MAPPA_4PI.md` |
| **`csv/_test_fork/_sonda_fallback_psispin.py`** | **`8bd48351`** | `python csv/_test_fork/_sonda_fallback_psispin.py` *(`SONDA_PASSI` per cambiare i passi; default 30)* | **QUANTE VOLTE SCATTA IL FALLBACK `:3394`**, l'UNICO punto in cui `phi` entra nella catena dell'orologio. **NON modifica il simulatore:** avvolge `calcola_psi` e valuta la STESSA condizione di `:3393` prima di ogni chiamata. **`P5`: un fallback mai misurato e' un comportamento sconosciuto** — i precedenti sono `_cs_nodo_prev` al `71.88 %` e `_psi_spin_prec` al `95.33 %`, per mesi. **MISURATO: `3` su `441` (`0.68 %`), alle invocazioni `1-2-3`.** | `csv/_test_fork/_sonda_fallback_psispin.txt` |
| **`csv/_test_fork/_f2p_test_E.py`** | **`391eee7a`** | `python csv/_test_fork/_f2p_test_E.py _f2p_corto` *(l'argomento e' la cartella del braccio della cura; senza, usa `_f2p_prova`)* | **I TEST `E1`-`E4` DELLA CURA `FASE_2PI`, coi criteri fissati PRIMA.** `E1` ed `E2` sono di **Luca**; **`E3` ed `E4` sono MIEI, derivati e marcati come tali** *(`Z125`: il §E non esisteva oltre `E1`/`E2`)*. **`E2` e' dichiarato NON MISURABILE** *(l'annichilazione vive solo dentro `ANTIFASE_ADD = False`)*. **Collaudo `6/6`, con TRE casi che devono fallire.** **SOLA LETTURA su snapshot gia' scritti.** | `csv/_test_fork/_f2p_corto_TEST_E.txt` · `_f2p_CONTROLLO_involucro.txt` |
| `csv/_test_fork/_g3_confronto.py` | `6b88ce78` | `python csv/_test_fork/_g3_confronto.py` | **`G3`: la gravita' ACCESA contro la gravita' SPENTA.** SOLA LETTURA su file gia' scritti: `med d0` e `d/d0` snapshot per snapshot, **il rapporto fra snapshot consecutivi** *(che e' il criterio 4)*, e `coer_l`/`dil` dai due `prog.csv`. **NON e' un confronto fra epoche:** stesso blob, stesso seme, stessa scena, stessa configurazione, **l'unica differenza e' il flag**. | `csv/_test_fork/_g3_senza_bifase/CONFRONTO_ON_OFF.md` |
| `csv/_test_fork/_spegni_grav_bifase.py` | `9648906e` | `python csv/_test_fork/_spegni_grav_bifase.py --controllo` *(120 passi, il controllo positivo)* poi `--prova` *(600 passi)* | **`G3`: LA PROVA DI SPEGNIMENTO DELLA GRAVITA' BIFASE.** **NON modifica simulatore ne' driver:** e' un INVOLUCRO che **avvolge `_applica_flag`** per rimettere `GRAV_BIFASE = False` **sul modulo** subito DOPO che il driver ha applicato i suoi flag *(assegnare prima verrebbe sovrascritto in silenzio)*, e poi **esegue il driver com'e'** con `runpy`. **`--controllo` e' OBBLIGATORIO e viene prima:** gira 120 passi **lasciando il flag com'e'** e confronta lo stato con `_val600/scena_000120.pkl.gz` -- **se l'involucro non riproduce la validazione, una differenza misurata sarebbe attribuibile all'involucro invece che al flag, e la prova non si fa.** Installa anche la **traccia SALITE/DISCESE per scrittore di `d0`, la stessa di `Z102`**, in `txt` e `csv` generati da codice. Si legge con `_letture_validazione.py --dir=csv/_test_fork/_g3_senza_bifase`, cioe' **con gli STESSI otto criteri assoluti**. | `csv/_test_fork/_g3_senza_bifase/` · `SOMMA_PER_SCRITTORE_d0.txt` · `.csv` |
| `csv/_seal_fork/_inventario_scrittori.py` | `2c70e4ad` | `python csv/_seal_fork/_inventario_scrittori.py` | **FASE A del registro della fisica: OGNI punto del simulatore che SCRIVE lo stato, trovato dall'AST.** Trova cio' che una `grep` non vede: **assegnamenti AUMENTATI**, **scritture per indice**, **`np.add.at`** *(nessun `=` nella riga)* e le **CONCATENAZIONI** *(che cambiano la LUNGHEZZA: nascite e morti)*. Per ognuno: **funzione, riga e FLAG che lo governa**. **L'esclusione e' VISIBILE:** cio' che non e' nella lista dichiarata compare lo stesso, marcato. **SOLA LETTURA: costruisce l'AST, non importa il simulatore** -- puo' girare mentre un run e' in corso. **Sei collaudi, e il sesto e' quello che DEVE fallire: un cercatore MENOMATO deve PERDERE gli scrittori nascosti.** | `csv/_seal_fork/_inventario/INVENTARIO_SCRITTORI.md` · `.csv` |
| `csv/_seal_fork/_sigillo_mem_moto.py` | `940afcc7` | `python csv/_seal_fork/_sigillo_mem_moto.py` | **SIGILLO di `G4`: `MEM_MOTO` BYTE-INERTE acceso, CHIRURGICO spento.** Scritto sui **cinque pattern standard**. `T0` riproducibilita' · `T1` lo spegnimento spegne · `T2` solo `S08_proj` · `T3` byte-identita' a monte · `T4` `mem_mot` resta aggiornato *(voluto: il flag toglie la SCRITTURA, non la grandezza)* · `T5` gate unico via AST · `T6` il caso che DEVE fallire, `MEM_HEBB=False` sul codice vero · **`T7` LA BYTE-INERZIA: 120 passi attraverso il driver, snapshot contro snapshot con `_val600`, prodotto dal blob PRIMA del flag**. Otto collaudi del criterio, quattro dei quali DEVONO fallire. | `csv/_seal_fork/_sig_mem_moto/REFERTO.txt` |
| `csv/_seal_fork/_sigillo_spegni_grav.py` | `cb506019` | `python csv/_seal_fork/_sigillo_spegni_grav.py` | **SIGILLO di `G3`: `GRAV_BIFASE = False` spegne SOLO `S09`.** Quattro bracci da 3 passi dalla semina, **ciascuno in un PROCESSO SEPARATO** *(in-process il secondo nasceva senza masse: `avvia_test` e' un interruttore a LEVETTA)*, confrontati per **FIRMA** *(sha1 dei byte, piu' stretto di `max|delta|`)*; **i siti che CONCATENANO portano anche la firma della CODA NUOVA e dell'INTERO `d0`**, cosi' stesse lunghezze con contenuto diverso risultano DIVERSE *(`ON`, `ON-bis`, `OFF`, `HEBB`)*. **`T0` RIPRODUCIBILITA'** *(senza, uno zero non significa niente)* · **`T1`** lo spegnimento spegne · **`T2`** gli altri diciannove scrittori di `d0` hanno le **stesse invocazioni** · **`T3`** byte-identita' **a monte** al passo 1 · **`T4`** `mem_mot` identico · **`T5` LA PROVA STRUTTURALE (AST): le ramificazioni che dipendono da `GRAV_BIFASE` sono UNA SOLA**, quindi nessun'altra legge PUO' essere gated su quel nome · **`T6` IL CASO CHE DEVE FALLIRE, sul codice VERO: `MEM_HEBB=False`**, cioe' proprio lo spegnimento che il mandato vieta. **⚠ Dichiara la distinzione sulla COESIONE:** sta **a valle**, quindi i suoi incrementi **cambiano** -- il sigillo afferma che la sua LEGGE non e' toccata, **non** che i suoi numeri siano identici. | `csv/_seal_fork/_sig_spegni_grav/REFERTO.txt` |
| `csv/_test_fork/_dove_spinge_la_gravita.py` | `2e95917b` | `python csv/_test_fork/_dove_spinge_la_gravita.py` | **`G2`: DOVE SPINGE LA GRAVITA'.** Il saldo di `S09` **PER REGIONE** *(vuoto, massa, nato, i due CONFINI)*, **salite e discese separate**, **e il saldo PER ARCO** -- senza il quale la regione con piu' archi sembra sempre la piu' spinta (`A3`, errore di popolazione). Piu' **i 20 archi che ricevono la spinta maggiore**, coi loro **nodi**, `d`, `d0` e `L/d`, e la **concentrazione** *(frazione della spinta positiva nell'`1 %` di archi piu' spinti: il valore sotto **ipotesi nulla** e' `0.01`, non una soglia scelta)*. **NON tocca il simulatore:** sostituisce `_traccia_d0` con una funzione pure-read allo stesso punto di chiamata. **⚠ GUARDIA DEL PREFISSO:** il cumulato per arco assume che la mitosi APPENDA senza riordinare; **e' verificato a ogni passo**, e **se non regge la tabella dei 20 archi NON si stampa**. **Il criterio e' COLLAUDATO su tre casi a risposta nota** *(`P1-sexies`)*, **e il piu' importante e' quello che DEVE fallire: una permutazione degli archi**. **Produce anche la TABELLA DEI 20 ARCHI col `|saldo|` piu' grande in **`csv`** e **`markdown`**, GENERATA da codice (`P1-ter`), con saldo/salite/discese/**passi in cui l'arco esiste**, e le **tre righe di riscontro** *(quanti dei 20 sul confine; quanta parte del saldo di confine fanno; e se il saldo per regione rifatto PER CHIAVE coincide con quello di `Z105`)*. **E LA SATURAZIONE MISURATA:** quanti archi hanno la spinta **incollata al tetto causale**, *per passo* *(frazione sugli scritti e sui vivi)*, *per arco* *(istogramma `0` / `1-10` / `11-60` / `61-119` / `120`)*, *per regione*, e **quanta parte del saldo viene da incrementi saturi**. **La lettura e' fissata NEL FILE prima dei numeri** *(rara `< 1 %` → difetto locale; diffusa `> 10 %` → `A11` corollario 6; in mezzo → si scrive il numero SENZA etichetta)*. **SOLA MISURA.** | `csv/_test_fork/_diag_D/DOVE_SPINGE_LA_GRAVITA.txt` · `G2_20_ARCHI.csv` · `G2_20_ARCHI.md` |
| `csv/_test_fork/_letture_validazione.py` | `50f33c5c` | `python csv/_test_fork/_letture_validazione.py --dir=csv/_test_fork/_val600` | genera DA CODICE la tabella della validazione e l'esito contro gli **otto criteri ASSOLUTI**, che sono scritti NEL FILE e fissati **prima** di vedere i numeri: nessun picco di `nsub`, `peq >= 0`, nessun arco sotto `LAM`, `d0` non scappa, `d/d0` vicino a 1 **in entrambi i versi**, stress finito, invarianti mai scattati, e **quanto il termine di coesione tocca il cono locale**. **Nessun confronto con le epoche precedenti.** | `csv/_test_fork/_val600/LETTURE.txt` |
| `csv/_seal_fork/_sigillo_invarianti.py` | `214ac395` | `python csv/_seal_fork/_sigillo_invarianti.py` | **SIGILLO BLOCCANTE di `C5`.** `I1` invarianti accesi = spenti **byte-identico**, **col COSTO MISURATO** e non stimato; **`I2` CONTROLLO POSITIVO, IL CASO DI OGGI**: il ramo D al passo **1126** senza `PEQ_ESATTO` **deve** far scattare `peq >= 0` **sull'arco `3352-506`** -- *e' la prova che avrebbe preso l'errore di oggi*; **`I3` COMPLETEZZA DAL CODICE**: ogni attributo ARRAY dello snapshot ha la sua riga in `DOMINI`, senno' FALLISCE. **`I4` e `I5` NON sono qui**, e il sigillo lo dichiara. | `csv/_seal_fork/_sigillo_invarianti_2026-09-21.txt` |
| `csv/_seal_fork/_sigillo_anom_simm.py` | `5cf58d3a` | `python csv/_seal_fork/_sigillo_anom_simm.py` | **SIGILLO BLOCCANTE della cura `C1-bis`.** `U1` byte-identita'; `U2` controllo positivo; **`U3` riduzione al limite che misura un NUMERO** *(la differenza relativa e' ESATTAMENTE meta' dell'anomalia, `e/2`)*; **`U4` limitata in `[-2,+2]` E IL LIMITE E' RAGGIUNTO** *(senno' non sarebbe esercitato)*; **`U5` il POLO e' zero in esercizio MA DIMOSTRATO possibile** *(a `peq = -rho` il denominatore e' esattamente 0 e oltre il segno si rovescia: la dipendenza da `C1` e' reale, non prudenziale)*; **`U6` `0/0` succede DAVVERO** *(senno' quella definizione sarebbe codice morto)*. | `csv/_seal_fork/_sigillo_anom_simm_2026-09-21.txt` |
| `csv/_seal_fork/_sigillo_coes_causale.py` | `ff82a982` | `python csv/_seal_fork/_sigillo_coes_causale.py` | **SIGILLO BLOCCANTE della cura `C4`.** `S1` byte-identita' a flag spento; `S2` controllo positivo; **`S3` L'ISTANTE** *(fotografia usata sempre, **e lo scarto dal `d0` di prima > 0**: i due istanti ERANO diversi davvero)*; **`S4` IL CONO E' LOCALE** *(tetto da `_cs_nodo_prev`, minimo locale piu' stretto del globale -- la prova che `A5` era violato -- e riporta in quale VERSO agisce)*; `S5` nessuno spostamento piu' veloce del cono locale. | `csv/_seal_fork/_sigillo_coes_causale_2026-09-21.txt` |
| `csv/_seal_fork/_sigillo_scala_min_passo.py` | `e2b005a9` | `python csv/_seal_fork/_sigillo_scala_min_passo.py` | **SIGILLO BLOCCANTE della cura `C3`.** `R1` byte-identita' a flag spento; `R2` controllo positivo; **`R3` LA COMPOSIZIONE -- il sigillo che oggi NON ESISTE**: spinte opposte a somma NULLA dentro un passo, e `d0` deve restare INTATTO; **col freno per-scrittura lo stesso test DEVE fallire**, e le due meta' insieme sono cio' che lo rende non vuoto; `R4` il vincolo `LAM` tiene; **`R5` la CHIRURGIA attraverso la mitosi e' allineata** *(zero disallineamenti)*; **`R6` `nsub` non moltiplica piu' il bias** *(il freno su `d` gira una volta per passo)*. | `csv/_seal_fork/_sigillo_scala_min_passo_2026-09-21.txt` |
| `csv/_seal_fork/_sigillo_peq_nascita.py` | `05b3f1d9` | `python csv/_seal_fork/_sigillo_peq_nascita.py` | **SIGILLO BLOCCANTE della cura `C2`.** `Q1` byte-identita' a flag spento; `Q2` controllo positivo *(acceso e spento DEVONO differire)*; `Q3` a flag acceso compaiono esattamente `2*nc` `nan` dopo la mitosi e ZERO a flag spento; **`Q4` dopo il passo dopo NON resta nessun `nan` -- il `nan` e' una CONSEGNA, non una perdita**; `Q5` nessun `nan` altrove *(d, d0, vd, psi, tw, phi)*; **`Q6` LA LEGGE E' CAMBIATA: a flag acceso il `peq` calibrato DIFFERISCE dalla mediana globale, a flag spento COINCIDE** -- e' il criterio che conta, gli altri cinque non lo sostituiscono. | `csv/_seal_fork/_sigillo_peq_nascita_2026-09-21.txt` |
| `csv/_seal_fork/_sigillo_peq_esatto.py` | `6b361c93` | `python csv/_seal_fork/_sigillo_peq_esatto.py` | **SIGILLO BLOCCANTE della cura `C1`.** `P1` byte-identita' a flag spento; **`P2` riduzione al limite che misura l'ESPONENTE** *(scarto/x^2 costante = |p-r|/2), non l'ampiezza -- "piccolo" non e' un criterio*; `P3` `peq >= 0` su un run vero col flag acceso, piu' `P3b` che il flag NON sia inerte; `P4` controllo positivo aritmetico *(a `x = 1.5` l'Eulero va negativo e l'esatto no)*; **`P5a` il passo 1126 vero sullo STESSO STATO con la cura accesa solo li'**, e **`P5b` la finestra intera a cura accesa**. | `csv/_seal_fork/_sigillo_peq_esatto_2026-09-21.txt` |
| `csv/_seal_fork/_sigillo_traccia_peq.py` | `57a95f50` | `python csv/_seal_fork/_sigillo_traccia_peq.py` | **SIGILLO BLOCCANTE** dei contatori `TRACCIA_PEQ` e dello stop `FERMA_DOPO_NSUB`. QUATTRO prove: T1 byte-identita' a diagnostici SPENTI contro il simulatore committato; **T2 byte-identita' con TRACCIA_PEQ ACCESO (PURE-READ, par.2.3) -- senza, byte-inerte significherebbe solo spento**; T3 controllo positivo (la sonda ha attraversato archi veri, senno' e' codice morto); T4 lo stop alza davvero e porta i quattro numeri. Configurazione VERA del ramo D, tre flag ACCESI. | `csv/_seal_fork/_sigillo_traccia_peq_2026-09-21.txt` |
| `csv/_test_fork/_arco_innesco.py` | `9c22c0f6` | `python csv/_test_fork/_arco_innesco.py --da=1080 --fino=1126` | misura `n1` e l ARCO con |anom| MASSIMO ALL INGRESSO di `step()` -- dove il codice calcola `nsub` -- invece che DOPO, che e l istante sbagliato e che la rigiocata guarda. Si ferma al superamento della soglia SENZA integrare il passo esplosivo, perche la misura e gia fatta. Stampa anche gli 8 archi di |anom| maggiore e quanti hanno `peq` al pavimento. PURE-READ. | `doc/REFERTO_istanti_scala_min_coes_adim.md` |
| `csv/_test_fork/_rigiocata_1200_1230.py` | `5fc61522` | `python csv/_test_fork/_rigiocata_1200_1230.py --da=1080` | rigioca il ramo D da uno SNAPSHOT (`--da=<passo>`, default 1080) registrando a OGNI passo n1/n2/n3/nsub ricostruiti come il codice (`:4264`, ramo VERLET), i SECONDI del passo, l ARCO con |anom| MASSIMO (i due nodi, la loro origine, rho, peq, anom), l arco candidato 2773-4158 cercato per COPPIA DI NODI, e i cinque nati piu giovani con ramp. Soglia DICHIARATA: si ferma se n1 supera 100, per non integrare l esplosione. IL NOME DEL FILE E STORICO: la finestra giusta e 1080-1200, non 1200-1230. | `doc/REFERTO_rigiocata_ramoD.md` |
| `csv/_peq_mediana_ramoD.py` | `3aef0b51` | `python csv/_peq_mediana_ramoD.py` | legge dagli snapshot del ramo D la MEDIANA e il MINIMO di `peq`, la mediana di `rho`, e calcola quale `anom` e quale `n1` produrrebbe un arco nato da SCHWINGER (che prende `peq = median(peq)`, `:4846`). Serve a decidere il candidato: lo ha REFUTATO. | `doc/REFERTO_istanti_scala_min_coes_adim.md` §②-bis |
| `csv/_estratto_grezzo_D.py` | `265ad8f6` | `python csv/_estratto_grezzo_D.py` | esporta tre snapshot del ramo D (600, 1080, 1200) in `.npz` compressi con TUTTO il necessario per ricostruire src e n1, piu un README che dice come. Serve a far RIFARE I CONTI da fuori invece di fidarsi di una tabella. | ramo `dati-grezzi`, `estratto_grezzo/README.md` |
| `csv/_analisi_ramoD.py` | `864b7d92` | `python csv/_analisi_ramoD.py` | genera DA CODICE le tabelle del ramo D (T1..T5): mediane di d/d0/peq per snapshot, archi sotto LAM, regione degli archi con peq minimo, confronto D contro C. Nasce da P1-ter: una tabella si genera, non si ricopia. | `csv/_test_fork/_diag_D/ANALISI_ramoD.txt` |
| `csv/_estrai_ramoD.py` | `48543e87` | `python csv/_estrai_ramoD.py` | estrae dagli snapshot del ramo D il quadro per passo (n, archi, d, d0, peq, contatori delle guardie) senza interpretarlo. | `csv/_test_fork/_diag_D/` |
| `csv/_sposta_archivi.py` | `df44cf93` | `python csv/_sposta_archivi.py` | sposta le cartelle di `.pkl` sopra i 300 MB sul disco freddo `E:` verificando lo sha1 dei BYTE COMPRESSI, senza mai decomprimere ne caricare. | `doc/SPOSTAMENTO_archivi.tsv` |
| `csv/_test_fork/_rigiocata_0_120.py` | `402e95d6` | `python csv/_test_fork/_rigiocata_0_120.py` | rigioca la SEMINA del ramo B per 120 passi campionando a OGNI PASSO: l arco 16-481 con d e d0 SEPARATI, i cinque nodi con _deg/phivel/tensione, i percentili della popolazione, n3 ricostruito, e la GEOMETRIA alla semina (correlazione _deg contro distanza dal baricentro). Porta un SIGILLO INTERNO BLOCCANTE: al passo 120 lo stato dev essere identico a _ab_B/scena_000120.pkl.gz. | `doc/REFERTO_rigiocata_0_120.md` |

---

## Aggiunti il 2026-09-26 — **la chiusura della cura A e la LISTA CHIUSA**

| strumento | blob (byte) | comando | cosa fa | esito |
|---|---|---|---|---|
| `csv/_collaudo_criterio_zero.py` | `9a675b90` | `python csv/_collaudo_criterio_zero.py` | COLLAUDO di un CRITERIO su rumore puro (`P1-sexies`): la forma con `|x|` del criterio `C1` contro la forma COL SEGNO, 1e5 prove, 4 valori, seme fisso `20260926` | `doc/COLLAUDO_criterio_zero.txt`: con `|x|` passa il **14.11 %**, col SEGNO l'**86.13 %** -> la forma vecchia **NON era soddisfacibile** |
| `csv/_seal_fork/_c1_col_segno.py` | `aeebf3dc` | `python csv/_seal_fork/_c1_col_segno.py` | `C1` nella forma COL SEGNO, **dai json GIA' SCRITTI** del sigillo della cura A: nessun rigiro del simulatore, e le pendenze si ricalcolano con **la stessa funzione `pend` del sigillo** | `csv/_seal_fork/_sig_cura_A/C1_COL_SEGNO.txt`: `(a')` **PASS** (`|media|/SE` `0.9656` lunghi, `1.2640` corti), `(b)` **PASS** -> **cura A `6/6`** |
| `csv/_lista_chiusa.py` | `b27b4a9d` | `python csv/_lista_chiusa.py` | genera `doc/LISTA_CHIUSA.md` da **CINQUE fonti** (`STATO_RUN`, `RAMIFICAZIONI`, `REGISTRO_FISICA`, `INVENTARIO_passo_incompleto`, `CONFIGURAZIONE_misure_2026-09-25`), assegna una famiglia per REGOLA e manda ogni voce in LISTA o in FUORI LISTA **col motivo** | `doc/LISTA_CHIUSA.md`: **624 voci**, `405` in lista, `219` fuori, `48` sezioni dichiarate fuori portata. **Si FERMA** se una delle 15 voci dell'elenco `DEVONO` non compare in lista |
| `csv/_collaudo_lista_chiusa.py` | `0700fd9c` | `python csv/_collaudo_lista_chiusa.py` | COLLAUDO dei DUE rami del presidio di `_lista_chiusa.py`: il generatore vero deve scrivere, una copia con una voce **che non esiste** deve **fermarsi** e **non toccare** il documento | `doc/COLLAUDO_lista_chiusa.txt`: **2/2 PASS** (uscita `3`, sha1 del documento **invariato**) |

**⚠ E DUE COSE DA DIRE SU QUESTE VOCI, perche' l'inventario serve a chi rigira:**
- i due `_collaudo_*` **non sono sigilli di una legge**: collaudano **un CRITERIO** e **un PRESIDIO**. Inventariarli come sigilli gonfierebbe il conto dei sigilli veri *(par.5-novies, il triage)*;
- `_c1_col_segno.py` **non rigira il simulatore**: legge i json del sigillo della cura A. **Se quei json vengono cancellati, lo strumento non e' piu' ri-girabile** — e allora la voce diventa un `Z31`, non un'omissione d'inventario.

---

## Aggiunti il 2026-09-26 — **le COLLISIONI di ID (`PASSO 1` dell'indice)**

| strumento | blob (byte) | comando | cosa fa | esito |
|---|---|---|---|---|
| `csv/_collisioni_id.py` | `343eb8f8` | `python csv/_collisioni_id.py` | MISURA le COLLISIONI di ID: stesso nome, voci diverse. Definizione = l'ID sta nell'etichetta di una riga o apre un'intestazione, **in un registro GLOBALE**; citazione = compare nel testo | `doc/COLLISIONI_ID.txt`: da **60** collisioni apparenti a **15** vere, e **0** dopo la rinomina. **37 righe** riconosciute come RIMANDI e non definizioni |
| `csv/_rinomina_collisioni.py` | `4e3d838e` | `python csv/_rinomina_collisioni.py` | RINOMINA le 23 voci in collisione **nei soli documenti VIVI**, una riga alla volta con l'ancora contata (`P1-quater`), e **collauda nei due versi** | `doc/RINOMINE_ID.txt`: **4/4 PASS** -- `0` collisioni residue, `0` file intoccabili cambiati su **1029**, un'ancora inesistente FA fallire l'assert, `0` file modificati fuori dall'elenco |

**⚠ `_rinomina_collisioni.py` E' IDEMPOTENTE, e non lo era:** `\bA1\b` trova `A1` **dentro** `A1-INERZIA` *(il trattino e' un confine di parola)*, quindi la seconda passata avrebbe scritto `A1-INERZIA-INERZIA`. **Un difetto che si vede solo al secondo giro**, e la guardia e' *«se il nome nuovo c'e' gia', salta»*.

---

## Aggiunti il 2026-09-26 — **l'INDICE DEGLI ID (`PASSO 2`)**

| strumento | blob (byte) | comando | cosa fa | esito |
|---|---|---|---|---|
| `csv/_indice_id.py` | `7127a4e7` | `python csv/_indice_id.py` | GENERA `doc/INDICE_ID.tsv` (id, alias, titolo, fonte, stato, blocca_run_base, tipo) e `doc/INDICE_ID_ESCLUSI.tsv` (le forme che NON sono ID, **col motivo**) da SEI registri, `CLAUDE.md` compreso | `doc/INDICE_ID_referto.txt`: **663** voci, **38** escluse; stato `da-decidere` su **466**, `blocca_run_base` `DA-DECIDERE` su **511** — e non e' pigrizia: **nessun documento lo dichiara** |
| `csv/_presidio_indice.py` | `e1754107` | `python csv/_presidio_indice.py --collaudo` | PRESIDIO: ogni ID che un commit AGGIUNGE a un documento vivo, o cita nel messaggio, esiste nell'indice o fra gli esclusi. Tre esiti: NOTO, ESCLUSO, **AMBIGUO** *(forma nuda definita da due registri)* | `doc/COLLAUDO_presidio_indice.txt`: **5/5 PASS**, e il quinto e' il **HOOK VERO** *(uscita `1`, ID segnalato, documento tornato identico)* |

**⚠ IL PRESIDIO GUARDA SOLO LE RIGHE AGGIUNTE, ed e' una scelta:** guardare i file interi rifiuterebbe **ogni** commit finche' l'indice non e' perfetto, e verrebbe aggirato il primo giorno (`A9`). **Cosi' il debito vecchio resta visibile nell'indice e il debito NUOVO non si crea.**

---

## Aggiunto il 2026-09-26 — **l'inventario che precede il `PASSO 3`**

| strumento | blob (byte) | comando | cosa fa | esito |
|---|---|---|---|---|
| `csv/_inventario_lettori_id.py` | `d1f3819d` | `python csv/_inventario_lettori_id.py` | classifica in QUATTRO classi gli script che nominano un registro: **copia del simulatore** *(reperto)*, **scrittore una volta**, **IMPORTATORE** *(costruisce l'indice: DEVE leggere il Markdown)*, **LETTORE** *(il perimetro del `PASSO 3`)* | `doc/INVENTARIO_lettori_id.txt`: **83** script nominano un registro, ma i LETTORI che aprono davvero un registro sono **10** |

---

## Aggiornati il 2026-09-26 — **il `PASSO 3` ridotto: la vista legge l'INDICE**

| strumento | blob (byte) | comando | cosa fa | esito |
|---|---|---|---|---|
| `csv/_lista_chiusa.py` | `11300066` | `python csv/_lista_chiusa.py` | **RISCRITTO**: era un parser di **cinque** documenti in Markdown, ora e' una **VISTA su `doc/INDICE_ID.tsv`** *(`PASSO 3` ridotto)*. `id`, `stato`, `tipo`, `famiglia` sono **campi**, non inferenze | `doc/LISTA_CHIUSA.md`: **736** voci, `333` in lista, `403` fuori col motivo, **2 voci PERSE dichiarate** *(senza ID: non possono comparire)*. Collaudo `2/2` |
| `csv/_indice_id.py` | `a66133cb` | `python csv/_indice_id.py` | **+ colonna `famiglia`** *(opzione (a) di Luca)*, **+ `doc/SMISTAMENTO_run_base.md`**, e la regola di `blocca_run_base` **corretta**: un chiuso, un non-difetto, una teoria o un criterio-locale **non bloccano mai** | `doc/INDICE_ID_referto.txt`: **736** voci *(da 666)*, `blocca SI` **2** *(da 5)*, controllo di Luca **PASS**; smistamento **103** voci in sette famiglie |
| `csv/_collisioni_id.py` | `d226ee8d` | `python csv/_collisioni_id.py` | stessa forma di ID dell'indice *(stem lungo, enumerazioni, cifre in coda)* | `0` collisioni su **291** ID definiti |
| `csv/_presidio_indice.py` | `16da1629` | `python csv/_presidio_indice.py --collaudo` | stessa forma di ID + **sentinella scelta a RUN TIME** | **5/5 PASS**, hook vero incluso |
| `csv/_collaudo_lista_chiusa.py` | `4dd40e46` | `python csv/_collaudo_lista_chiusa.py` | l'iniezione della copia truccata usa **tre** campi *(l'elenco `DEVONO` porta anche il motivo della copertura)* | **2/2 PASS** |

---

## Aggiornati il 2026-09-26 — **il CONGELAMENTO della lista chiusa**

| strumento | blob (byte) | comando | cosa fa | esito |
|---|---|---|---|---|
| `csv/_indice_id.py` | `ca922928` | `python csv/_indice_id.py` | **+ `TIPO_A_MANO`** *(le voci che erano `altro` e sparivano dallo smistamento)*, **+ le FRASI che dichiarano `chiuso`** *(con la frase in `stato_da`)*, **+ le `DECISIONI` della revisione** *(ogni riga con la prova in una frase)*, **+ l'ORDINE DI LAVORO** e **le CONDIZIONI DI FINE** verificate da script | `doc/INDICE_ID_referto.txt`: `741` voci, `blocca SI` **8** *(esattamente le otto del mandato)*, `DA VERIFICARE` **1** *(`D09`)*; **4 condizioni su 4 PASS** |
| `csv/_lista_chiusa.py` | `1d2dfe33` | `python csv/_lista_chiusa.py` | vista sull'indice; **l'elenco delle voci PERSE e' VUOTO** e il collaudo contiene **tutte** le voci nominate dal mandato | `doc/LISTA_CHIUSA.md`: `741` voci, `352` in lista, `389` fuori, **0 perse** |
| `csv/_presidio_indice.py` | `c379d913` | `python csv/_presidio_indice.py --collaudo` | il controllo vive in **UNO stadio solo** (`commit-msg`): in `pre-commit` il messaggio non esiste ancora | **5/5 PASS**, end-to-end dallo stadio `commit-msg` |

---

## Aggiunto il 2026-09-26 — **l'analisi dei sei LETTORI (punto 5)**

| strumento | blob (byte) | comando | cosa fa | esito |
|---|---|---|---|---|
| `csv/_analisi_lettori_indice.py` | `9c0a577f` | `python csv/_analisi_lettori_indice.py` | misura **dal sorgente** cosa apre ciascuno dei sei lettori, se legge il CODICE, se SCRIVE, e dichiara **quale campo dell'indice gli manca** | `doc/LETTORI_INDICE_analisi.md`: **nessuno dei sei si converte com'e'** — 2 consumatori a cui manca un campo, 2 generatori che leggono il codice e scrivono nel registro, 1 che misura la prosa, 1 fuori perimetro |

---

## Aggiornati il 2026-09-26 — **`LETTORI-INDICE` chiusa: 1 ritirato, 1 convertito, 4 fuori**

| strumento | blob (byte) | comando | cosa fa | esito |
|---|---|---|---|---|
| `csv/_archivio/_triage_difetti.py` | `d84ad423` | — **RITIRATO** | **spostato in archivio il 2026-09-26** *(`STANDARD 10`: lo smistamento dell'indice fa lo stesso lavoro — una cura non aumenta il numero degli strumenti)*. **Non si cancella**: resta come storia, e la tabella che generava in `STATO_RUN` resta valida fino alla prossima rigenerazione | — |
| `csv/_punto_della_situazione.py` | `04167da9` | `python csv/_punto_della_situazione.py` | **CONVERTITO**: legge **soltanto** `doc/INDICE_ID.tsv` *(campo nuovo `avanzamento`)*, e ha un **collaudo nei due versi** — `SCALE-TW` deve comparire, `CONTAGIO` *(nel Markdown, senza ID)* **non deve** | `doc/PUNTO_DELLA_SITUAZIONE.md`: **95** task con marcatore *(da 60)*, `47` difetti; collaudo **5/5** |
| `csv/_confronto_pds.py` | `b49cca16` | `PDS_PRIMA=<file> python csv/_confronto_pds.py` | il confronto **prima/dopo** dell'output, con le differenze in **tre classi** | `doc/LETTORI_INDICE_confronto.md`: **+68 comparse** *(l'indice copre tutti i registri)*, **-30 senza marcatore** *(filtro dichiarato)*, **-3 che non erano ID** *(due erano NOMI DI FILE)* |
| `doc/PUNTO_DELLA_SITUAZIONE_prima_della_conversione.md` | — | — | **il reperto del PRIMA**: l'output del parser salvato **prima** della conversione, committato perche' un confronto senza il termine di paragone non e' verificabile | — |

---

## Aggiunto il 2026-09-26 — **la REVISIONE STORICA degli otto `SI`**

| documento | comando che lo collega | cosa contiene |
|---|---|---|
| `doc/REVISIONE_SI_2026-09-26.md` | `python csv/_indice_id.py` *(scrive la colonna `revisione` e i rimandi nello smistamento)* | per ognuno degli otto `SI` e per le sei voci che **non** bloccano: cio' che e' ✅ **VERIFICATO sul codice** *(file, riga, la frase che la riga contiene)*, cio' che e' 🟨 **di Luca e non ho rifatto**, cio' che e' 🧠 **INFERENZA**. **Blob del documento: `06c18fe9`.** |

---

## Aggiornati il 2026-09-26 — **l'INDICE E' LA FONTE: l'importatore si spegne**

| strumento | blob (byte) | comando | cosa fa | esito |
|---|---|---|---|---|
| `csv/_archivio/_indice_id_importatore.py` | `c796966e` | ⛔ **NON SI RILANCIA** | **l'importatore, SPENTO il 2026-09-26 dopo l'ULTIMA importazione.** Leggeva il Markdown e ricostruiva l'indice: rilanciarlo ora **sovrascriverebbe la fonte con una ricostruzione**, buttando via le decisioni scritte nelle colonne | — |
| `csv/_indice_id.py` | `ee6bc793` | `python csv/_indice_id.py` · `--collaudo` | **VALIDATORE** *(non genera piu' niente)*: schema, vocabolari, ID unici e ben formati, coerenza `stato`/`blocca`, `motivo` dove `blocca = SI`, **nessuna voce persa rispetto al tag** *(con le cancellazioni DICHIARATE)*. **Gira nel `pre-commit`** | `doc/INDICE_ID_validazione.txt`: **6/6 PASS** — l'indice vero passa, quattro guasti diversi vengono RIFIUTATI |
| `csv/_vista_smistamento.py` | `2c0575bf` | `python csv/_vista_smistamento.py` | genera `doc/SMISTAMENTO_run_base.md` **dai DATI**: `doc/INDICE_ID.tsv` + **`doc/ORDINE_SI.tsv`** *(l'ordine di lavoro, estratto dall'AST del vecchio generatore)*. **Nessuna decisione nel codice** | `137` voci, `8` `SI`, `0` da verificare |
| `csv/_collaudo_istruzioni.py` | `9f30af48` | `python csv/_collaudo_istruzioni.py` | **collauda la SEZIONE 11 di `CLAUDE.md`**: la estrae, ne legge colonne/stati/comandi, **costruisce la riga del difetto finto dalle colonne DICHIARATE**, prova i due versi sul hook vero, rigenera le viste coi comandi della sezione, ripristina e verifica per sha1 | `doc/COLLAUDO_istruzioni_indice.txt`: **6/6 PASS — la sezione basta da sola** |
| `doc/ORDINE_SI.tsv` | — | *(dato)* | l'ordine di lavoro degli otto `SI`: `n`, `voce`, `perche_viene_qui`, `stima`. **Era un letterale Python nel generatore: ora e' un DATO** | — |

---

## Aggiunto il 2026-09-26 — **la PROPOSTA di riordino delle regole**

| strumento | blob (byte) | comando | cosa fa | esito |
|---|---|---|---|---|
| `csv/_regole_proposta.py` | `934fb523` | `python csv/_regole_proposta.py` | **inventaria OGNI regola in vigore** *(assiomi, `STANDARD`, i `P` di `CLAUDE.md`, i presidi dei hook, le sezioni di `CLAUDE.md`, le regole di lavoro nuove)*, misura le righe di ogni sezione e documento, e assegna a ciascuna una **destinazione**. **Si FERMA se un id resta senza destinazione** | `doc/REGOLE_proposta.md`: **76 regole, 76 con destinazione, 0 senza**; `CLAUDE.md` `1576 -> ~153`; avvio `2714 -> ~1021`; il posto 2 passa da `16` a `10` con tre fusioni |

## Aggiunto il 2026-09-26 — **l'APPLICAZIONE del riordino delle regole**

*(Il blob e' lo **sha1 dei BYTE GREZZI**, non `git hash-object`: sono due numeri
diversi per lo stesso file.)*

| strumento | blob (byte) | comando | cosa fa | esito |
|---|---|---|---|---|
| `csv/_riordino_fatti.py` | `902f045c` | `python csv/_riordino_fatti.py` · `--verifica` | sposta `par.9` (dal **tag** `regole-pre-riordino`) in `doc/FATTI_dal_codice.md`, **ordinato per FUNZIONE**, con le righe del simulatore **misurate dall'AST**. Lo spostamento e' **verbatim** | **53 punti, 11 funzioni, 0 righe perse** |
| `csv/_riordino_storia.py` | `8ffe675a` | `python csv/_riordino_storia.py` · `--verifica` · `--estrai <sez>` | archivia **verbatim** ogni sezione di `CLAUDE.md` al tag (tranne `par.9`) in `doc/STORIA_REGOLE.md`, con la tabella *dove vive oggi la sua regola* | **23 sezioni, 0 senza destinazione, 0 righe perse** |
| `csv/_riordino_sposta.py` | `f9b41925` | `python csv/_riordino_sposta.py` · `--prova` | porta `par.4` in coda a `doc/REGISTRO_FISICA.md` e `par.6` in `doc/STATO_RUN.md` **dopo l'INDIRIZZO** (mai in coda: la' `csv/_stato_run.py` cerca la voce APERTA). Idempotente | 27 + 28 righe; `STATO_RUN` resta bilanciato **17 `APERTO` / 17 `chiuso`** |
| `csv/_archivio_relazioni.py` | `1df67e2c` | `python csv/_archivio_relazioni.py` · `--verifica` | divide `RELAZIONE_PER_CLAUDE.md` in `doc/relazioni/<giorno>.md`; il file vivo tiene **solo il giorno corrente**. La **regola di taglio e' dichiarata** nel docstring | **20437 righe in ingresso = 20437 in uscita**, 9 giorni |
| `csv/_rinomina_hook.py` | `eb1df579` | `python csv/_rinomina_hook.py` · `--prova` | da' il prefisso **`H-`** ai presidi dei hook (`P3`->`H-P3`, ...) e ai marcatori `ESENTE-Pn`. **Ogni sostituzione e' asserita per se'** (`P1-quater`) | **37 sostituzioni** nei 7 sorgenti + **21 marcatori** in 20 file; collaudo dei presidi **8/8** |
| `csv/_presidio_righe.py` | `7acf5e65` | `python csv/_presidio_righe.py` · `--collaudo` | **`H-RIGHE`**: rifiuta un commit se `CLAUDE.md` supera le **400 righe**. Sta in `commit-msg`, perche' la via d'uscita `[CLAUDE-OLTRE-400: ...]` vive **nel messaggio** | **collaudo 5/5 nei DUE versi**; e ha **rifiutato davvero** il commit 1/6 della serie |
| `csv/_indice_riordino.py` | `f7155270` | `python csv/_indice_riordino.py` · `--prova` | aggiunge a `doc/INDICE_ID.tsv` le voci del riordino (`H-*`, `L-*`, `STANDARD 4/6/8`), **annota** i nomi vecchi col rimando, e dichiara in `INDICE_ID_ESCLUSI.tsv` le forme che **non sono id**. Idempotente | **17 voci nuove, 9 annotate, 6 forme escluse**; validatore **TUTTO A POSTO**, 757 voci |
| `csv/_controlli_riordino.py` | `7fc039ea` | `python csv/_controlli_riordino.py` | i **cinque controlli di fine** del riordino: le 76 regole ritrovate, il tetto del posto 2, le righe di `CLAUDE.md` e quelle **lette all'avvio misurate prima/dopo**, tutti i collaudi, i nomi citati dai hook | vedi `doc/CONTROLLI_riordino.txt` |

## Aggiunto il 2026-09-26 — **`DRIVER-SCENA-II`** *(il primo `SI`)*

| strumento | blob (byte) | comando | cosa fa | esito |
|---|---|---|---|---|
| `csv/_test_fork/_misura0_scena_ii.py` | `2d502a4d` | `python csv/_test_fork/_misura0_scena_ii.py` | **MISURA 0** di `DRIVER-SCENA-II`: `net.n` dopo `_applica_flag` con `--nodi 0`, e che cosa fanno la scena `(ii)` e `N-MASSE`. Passa dall'**argv del driver** catturata dal suo testo | **3/3 come atteso**: `455` nodi con `--nodi 0`, `SystemExit` su entrambe le scene (`csv/_test_fork/_misura0_scena_ii.txt`) |
| `csv/_patch_scena_ii.py` | `3b3bd1d4` | `python csv/_patch_scena_ii.py` · `--prova` | la **cura** di `DRIVER-SCENA-II`: nove sostituzioni, **ognuna asserita per se'** (`P1-quater`), su `soliton_simulator.py` e sul driver. Idempotente | applicata; sintassi verificata dall'AST su entrambi i file |

| `csv/_seal_fork/_sigillo_scena_ii.py` | `2a324202` | `python csv/_seal_fork/_sigillo_scena_ii.py` · `--corto` | **il SIGILLO di `DRIVER-SCENA-II`**, cinque criteri: argv del default invariata *(contro il PADRE del commit di `--scena=`)*, un vuoto solo fatto dalla scena *(+ AST della scena intatto)*, il seme reale *(tre processi, firme `sha1`)*, configurazione intera, e `N-MASSE` che rifiuta ancora | **6/6 PASS** sul simulatore `437632bf` e sul driver `18fb1231` (`csv/_seal_fork/_sig_scena_ii/REFERTO.txt`) |

## Aggiunto il 2026-09-27 — **`OSSERVABILE-P1`** *(il secondo `SI`)*

| strumento | blob (byte) | comando | cosa fa | esito |
|---|---|---|---|---|
| `csv/_osservabile_p1.py` | `77b93d1b` | `python csv/_osservabile_p1.py --scena` · `--snap F` · `--semi 11,12,13,14` · `--collaudo` · `--json F` | **L'OSSERVABILE DELLA `PROVA 1`**: la distanza fra le masse **lungo il grafo, pesi `net.d`** (`A13`, mai `pos`). Centro = **medoide di grafo**; da' anche **insieme-insieme**, i **punti di controllo** nel vuoto e la **dispersione fra semi** (`P3`). `inf` **dichiarato** se le masse sono in componenti diverse | `K1` errore **0.000e+00** su catena, reticolo, componenti staccate e medoide |
| `csv/_seal_fork/_sigillo_osservabile_p1.py` | `8db2c386` | `python csv/_seal_fork/_sigillo_osservabile_p1.py` · `--corto` | il sigillo: `K1` sintetico, **`K2a`/`K2b`** *(cambio solo `d` -> cambia; solo `pos` -> non cambia)*, `K3` invarianza esatta, `K4` controlli entro il 10 %, `K5` **quattro processi** | **6/6 PASS** (`csv/_seal_fork/_sig_osservabile_p1/REFERTO.txt`) |

## Aggiunto il 2026-09-27 — **`INDICE-LEGGERO`**

| strumento | blob (byte) | comando | cosa fa | esito |
|---|---|---|---|---|
| `csv/_titoli_brevi.py` | `05ca3df8` | `python csv/_titoli_brevi.py` · `--prova` | accorcia i `titolo_breve` oltre i **100** caratteri *(la frase intera va in `stato_da`)* e **de-duplica** quelli identici. **Il delta e' asserito col diff:** `id`, `stato`, `blocca` e `famiglia` non cambiano su nessuna riga | **330 accorciati, 275 de-duplicati, 0 violazioni** sulle colonne intoccabili |
| `csv/_indice_id.py` | `48510b17` | `--cerca ID` · `--aperti` · `--blocca SI` · `--famiglia X` · `--dettaglio ID` · `--testo PAROLA` | **il VALIDATORE, e ora anche l'INTERROGAZIONE**: l'indice non si legge intero. `--cerca` e' **uguaglianza esatta**; `--testo` cerca sul **testo completo** e tronca **solo la stampa** | **collaudo 10/10**, coi quattro casi di `INDICE-LEGGERO` nei due versi |

## Aggiunto il 2026-09-27 — **`CURA2-STRUTTURALE`**

| strumento | blob (byte) | comando | cosa fa | esito |
|---|---|---|---|---|
| `csv/_patch_cura2_strutturale.py` | `5400b1bc` | `python csv/_patch_cura2_strutturale.py` · `--prova` | toglie i **quattro** rami `else` di `TEMPO_UNICO_MITOSI` **per AST** *(de-indenta il corpo del ramo acceso di 4 e nient'altro)*, porta la costante a `True` e toglie l'assegnazione da `_applica_flag`. Si ferma se i blocchi non sono 4 o se il file non compila | 4 blocchi trovati, **0 rimasti**, 1 sola assegnazione (la costante) |
| `csv/_seal_fork/_sigillo_cura2_strutturale.py` | `365a08a0` | `python csv/_seal_fork/_sigillo_cura2_strutturale.py` · `--corto` | il sigillo: `C1` byte-identici col flag ACCESO contro il **tag**, 2 semi; `C2` **il caso che DEVE fallire** *(al tag col flag SPENTO i byte cambiano)*; `C3` driver 0 differenze; `C4` la mitosi HA girato. **Avanza con `csv/_passo.py passo_pieno`**, non con le cinque chiamate | **4/4 PASS**: 214 campi, **0 diversi** su 2 semi; `C2` **116 campi diversi** (`csv/_seal_fork/_sig_cura2_strutturale/REFERTO.txt`) |
| `csv/_archivio/rami_off_cura2.py` | — | *(archivio: non si importa e non gira)* | i **quattro** rami `else` **copiati dal sorgente**, con funzione, righe al tag, cosa facevano, perche' sono usciti e il comando per rilanciarli | tag **`pre-cura2-strutturale`**, blob del simulatore al tag **`dd4f5ccf`** |

## Aggiunto il 2026-09-27 — **`POZZO-D`** *(`D02`, il primo `SI` di fisica)*

| strumento | blob (byte) | comando | cosa fa | esito |
|---|---|---|---|---|
| `csv/_seal_fork/_sigillo_pozzo_d.py` | `16c298d3` | `python csv/_seal_fork/_sigillo_pozzo_d.py` · `--corto` | il sigillo di **`POZZO-D`** (`D02`): `W1` byte-identico a flag spento *(contro il PADRE del commit del flag)*, `W2` la spinta cambia **col rapporto `L_pos/L_d`**, `W3` i `d <= 0` **contati**, `W4` **il caso che DEVE fallire** *(solo `pos` mosso: ON non cambia, OFF si')*. Avanza con **`passo_pieno`** | **4/4 PASS**; `W4`: ON **`0.000000e+00`** esatto, OFF **`5.38e+02`** (`csv/_seal_fork/_sig_pozzo_d/REFERTO.txt`) |

## Aggiunto il 2026-09-27 — **il PILOTA della `PROVA 1`**, e la cura `CTRL-RISCELTA`

> **⚠ QUESTA SEZIONE ARRIVA UN COMMIT IN RITARDO, e lo dichiaro invece di lasciarlo passare:**
> `CLAUDE.md` par.6 vuole l'inventario **nello stesso commit** del cambiamento, e gli strumenti
> sono stati committati in `4a7597e`, `2ebbd25` e `8c2997c`. **Un blocco di recupero non sana
> la violazione: la conferma.**

| strumento | blob (byte) | comando | cosa fa | esito |
|---|---|---|---|---|
| `csv/_test_fork/_pilota_prova1.py` | `b5e1c4a5` | `python csv/_test_fork/_pilota_prova1.py` · `--passi N` · `--checkpoint 0,40,80,120` · `--semi 11,12,13,14` · `--solo-referto` · `--collaudo` | **IL PILOTA DELLA `PROVA 1`** *(NON il run base: `5 SI` aperti)*. Lancia **un processo per seme** (`STANDARD 1`) e scrive il referto: `V1` controlli **FISSI**, `V2` l'osservabile `A(t)` con IC95 fra semi, `V5` migrazione, `V6` forma e allungamento, `V3` dove nascono i nodi, `V4` scorciatoie Schwinger. Dichiara la **configurazione intera** (`H-P5`) | **4 semi su 4**, 120 passi; `A(t) < 0` oltre la barra su **2 coppie su 3 a 40 e a 80 passi** |
| `csv/_test_fork/_pilota_prova1_braccio.py` | `f79a6aae` | `python csv/_test_fork/_pilota_prova1_braccio.py --seme 11 --passi 120 --checkpoint 40,80,120` | **un braccio, un seme.** Avanza con **`_passo.passo_pieno`** (`H-P9`), misura ai checkpoint, e **CALIBRA `kappa`** al passo 0 sulla risposta NOTA. Contiene la `Spia` che separa **mitosi** e **Schwinger** *(dagli indici e da `_g_nati_schwinger`)* e conta le **scorciatoie** `2*dd < d` | `kappa = 3` scelto dalla regola scritta prima; contaminazione **prevista `276.1` contro misurata `284.0`** |
| `csv/_test_fork/_confronto_previsione.py` | `231c78b7` | `python csv/_test_fork/_confronto_previsione.py` | **IL CONFRONTO fra la previsione e il pilota**, e i numeri del referto escono da qui (`L-NUMERI`). Stampa ogni previsione **col suo falsificante** e l'esito | **2 previsioni su 3 FALSIFICATE**; referto in `_pilota_prova1/CONFRONTO_previsione.txt` |
| `csv/_osservabile_p1.py` | `7854c7b7` | `--scena` · `--snap F` · `--semi …` · `--collaudo` · **`--collaudo-controlli`** | **AGGIORNATO**: `controlli_fissi()` + `segui_controlli()` — le coppie di controllo si scelgono **una volta al passo 0** e poi **si SEGUONO**. `controlli()` RESTA col suo **marchio**, perche' e' l'evidenza del difetto e il ramo che **deve fallire** | **`K5` 2/2**; `K5b`: su un effetto vero del `-4.475 %` i fissi vedono `+0.0000 %` e la riscelta porta `A` a `+0.025 %` |

**E i `.pkl`: NESSUNO.** Il pilota non scrive snapshot: ogni braccio produce **un `misura.json`** *(`csv/_test_fork/_pilota_prova1/seme_<N>/misura.json`)*, che **e' committabile** e porta seme, passi, `kappa`, blob e configurazione. **Per rigenerarli:** `python csv/_test_fork/_pilota_prova1.py` *(4 semi, 120 passi, ~40 min in parallelo)*.

## Aggiornati il 2026-09-27 — **la VERIFICA DEL GUARDIANO su `8c2997c`**

| strumento | blob (byte) | comando | cosa fa | esito |
|---|---|---|---|---|
| `csv/_test_fork/_scomposizione_tratti.py` | `62a56361` | `python csv/_test_fork/_scomposizione_tratti.py` · `--collaudo` | **`TRATTI`: il calo sta nel VARCO o negli INTERNI?** In unita' **ASSOLUTE** *(`D_centri`, `D_varco`, `D_interni`)*, IC95 fra semi. **Legge i `misura.json` GIA' COMMITTATI: nessun run nuovo.** `D_interni` e' un **INDICATORE** dichiarato, non il tratto interno del cammino | **`T4` 3/3**; **a 80 passi `D_interni` esclude lo zero 3 su 3, `D_varco` lo contiene 3 su 3** |
| `csv/_test_fork/_confronto_previsione.py` | `dcdf6165` | `python csv/_test_fork/_confronto_previsione.py` | **AGGIORNATO** con le tre correzioni del guardiano: *«i NODI del passo 0»* invece di *«le masse»*, il blocco **`(a-ter)`** sulla **divergenza** delle due distanze, `(b)` **da rimisurare** *(estimatore rotto, `ALLUNG-RELATIVO`)*, e i controlli col loro **IC95** piu' la **correlazione appaiata** | il referto rigenerato: `0` allungamenti, `7` non determinate, `2` nulli informativi |

**⚠ E `T4` E' UN CONTROLLO DI ARITMETICA, NON UN COLLAUDO** *(rilievo di Luca, 2026-09-27):
`D_interni = D_centri - D_varco` e' **zero per identita'** se i due si spostano uguale, e nel
`--collaudo` i valori sono costruiti **per aritmetica** -- **non puo' fallire** (`A9`).
**Resta perche' MISURA** quanto effetto inventa la forma **relativa** (`-0.04000` su una
traslazione rigida di `-0.19`): e' la prova di `ALLUNG-RELATIVO`. **Il collaudo VERO e' `T7`,
SUL GRAFO**, coi criteri in `doc/TASK_HISTORY/2026-09-27_tratti.md` par.4. -> `T4-TAUTOLOGICO`.

**⚠ E GLI STATI `.npz` DEL PROSSIMO RUN NON VANNO IN GIT** *(decisione di Luca)*: restano in
locale sotto `csv/_test_fork/_pilota_prova1/stati/` *(gia' in `.gitignore`)*, e qui si
committeranno **percorso**, **`sha1` dei byte grezzi** e il **comando verbatim** che li
rigenera. -> `STATI-LOCALI`.

**E non ci sono `.pkl` ne' dati nuovi:** entrambi leggono i `misura.json` committati in `c4517a9`. **Per rigenerare i referti basta rilanciare i due comandi.**

## Aggiunto il 2026-09-27 — **il VIDEO della scena del pilota** *(`VIDEO-SCENA`)*

> ### 📦 **MA UNA COPIA STA SU GITHUB, NEL RAMO ORFANO `media`** *(richiesta di Luca,
> 2026-09-27: il guardiano legge solo da GitHub)*. **Ramo `media`, aggiornato al commit
> `182e30f`** *(prima `acb235c`)*,
> che contiene **SOLO** `video_scena_seme11.mp4`, i quattro `FOTOGRAMMA_*.png` e un `README.md`
> con gli `sha1`, i commit di `fork-su2` che li hanno prodotti e il comando per rigenerarli.
>
> **⚠ E' UN RAMO ORFANO: NESSUNA STORIA CONDIVISA con `fork-su2`**, verificato
> (`git merge-base --is-ancestor` dice di no). E' stato creato in un **worktree separato**,
> cosi' l'albero di lavoro di `fork-su2` non e' stato toccato: `HEAD` invariato a `8718fb5`,
> `git status` pulito **prima e dopo**.
>
> **NON si fa il merge di `media` in `fork-su2`**, e non e' una formalita': ci rientrerebbero
> i 16 MB di binari che `.gitignore` tiene fuori apposta.

> **⚠ IL VIDEO E I FOTOGRAMMI NON SONO IN GIT** *(`STATI-LOCALI`)*: `8.56 MB` il video,
> `~2 MB` ciascun PNG. **Qui ci sono `sha1`, percorso e comando**, che e' cio' che li rende
> rigenerabili — **il sistema e' deterministico, quindi il dato E' il comando.**

| file | sha1 (byte grezzi) | come si rigenera |
|---|---|---|
| `csv/_test_fork/_pilota_prova1/VIDEO_scena_seme11.mp4` | `bbeee48ddac0a8b4` | `python csv/_test_fork/_video_scena.py --fps 8 --dpi 120` |
| `csv/_test_fork/_pilota_prova1/FOTOGRAMMA_passo000.png` | `b872374abe4f31c0` | `ffmpeg -i VIDEO_scena_seme11.mp4 -vf "select=eq(n\,0)" -vframes 1 FOTOGRAMMA_passo000.png` |
| `csv/_test_fork/_pilota_prova1/FOTOGRAMMA_passo040.png` | `f4495f6baa7d84bc` | `ffmpeg -i VIDEO_scena_seme11.mp4 -vf "select=eq(n\,20)" -vframes 1 FOTOGRAMMA_passo040.png` |
| `csv/_test_fork/_pilota_prova1/FOTOGRAMMA_passo080.png` | `e9ce704aa28c2896` | `ffmpeg -i VIDEO_scena_seme11.mp4 -vf "select=eq(n\,40)" -vframes 1 FOTOGRAMMA_passo080.png` |
| `csv/_test_fork/_pilota_prova1/FOTOGRAMMA_passo120.png` | `c563dd1c332d5fce` | `ffmpeg -i VIDEO_scena_seme11.mp4 -vf "select=eq(n\,60)" -vframes 1 FOTOGRAMMA_passo120.png` |

**E i fotogrammi `.npz` da cui il video nasce** *(61 file, `21.59 MB`, **locali**)*:
`csv/_test_fork/_pilota_prova1/stati/frame_seme11_passo*.npz`, rigenerati da
`python csv/_test_fork/_pilota_prova1.py --salva-stati --ogni 2` *(4 semi, 120 passi, ~48 min)*,
col blob del simulatore **`e203f9a8`** *(byte grezzi)*, semi `11,12,13,14`, checkpoint
`0/40/80/120`, data `2026-09-27`.

| strumento | blob (byte) | comando | cosa fa | esito |
|---|---|---|---|---|
| `csv/_test_fork/_video_scena.py` | `25aedde8` | `--fps 8 --dpi 120` · `--max-frame N` | **il renderer a DUE pannelli**: a sinistra la **vista di sempre** col `vmax` **FISSO**, a destra la **coerenza interna** col riferimento **co-rotante per massa**; contorno delle regioni, diagnostici **per fotogramma**, didascalia `A3-DISEGNO` | **61/61 fotogrammi**, `8.56 MB`, `60.5 s` di rendering |
| `csv/_test_fork/_pilota_prova1_braccio.py` | `6a80d3eb` | `--salva-stati --ogni 2` | salva stati, fotogrammi e coorti, **tutti LOCALI** | `V1` **provato**: `0` campi diversi contro il primo pilota |

---

## `ETC-PASSO` — la cura (a), **FASE 0** *(2026-09-27)*

| strumento | blob (byte) | comando che lo rigira **verbatim** | cosa misura | esito |
|---|---|---|---|---|
| `csv/_test_fork/_etc_letture.py` | `cea93194` | `python csv/_test_fork/_etc_letture.py` | **chi legge stato che una legge precedente dello STESSO passo ha gia' scritto**: censimento **dall'AST**, ricorsivo sulle chiamate a metodi di `Rete`, per le cinque leggi lette da `csv/_passo.py` | **56 letture sporche** su **31 attributi**, in **4 leggi su 5** *(`0/1/20/15/20`)*, sul blob del simulatore **`e203f9a8`** |

**Referto:** `csv/_test_fork/_etc_letture.json` *(committato)*.
**⚠ IL LIMITE E' DICHIARATO NEL DOCSTRING:** analisi **statica e per nome** — alias, `getattr` e
rami mai eseguiti non si vedono. **`56` e' un LIMITE INFERIORE**, e serve a **progettare** la cura,
non a certificarla: chi certifica e' `H-ETC-2`.

## `ETC-PASSO` — la cura (a), **FASE 0-bis** *(2026-09-27)*

| strumento | blob (byte) | comando che lo rigira **verbatim** | cosa misura | esito |
|---|---|---|---|---|
| `csv/_test_fork/_etc_progetto.py` | `92fb2285` | `python csv/_test_fork/_etc_progetto.py` | **le SCRITTURE CONCORRENTI** e quali **non sono variazioni**; l'**inventario dei clip** (`CLIP-INVENTARIO`); **per nodo o per arco**; i **flussi casuali**; le **56 letture** dopo la cura; il **costo** della fotografia | **21/21 attributi concorrenti** · **13 scritture non componibili** · **117 guardie**, di cui **27 tetti fisici** · **24.97 MB** per fotografia |

**Referto:** `csv/_test_fork/_etc_progetto.json` *(blob byte `0c362f32`, committato)*.
**Il `.json` precedente è stato CANCELLATO e rigenerato**, su istruzione di Luca: *«il json vecchio
si rigenera, non si riusa»* — non veniva dal sorgente accanto.
**⚠ IL LIMITE, nel docstring:** analisi **statica e per nome**; per i tetti fisici il conto **27**
è un **limite SUPERIORE** *(tre pavimenti di grado sono guardie la cui divisione sta altrove)*.

| strumento | blob (byte) | comando che lo rigira **verbatim** | cosa misura | esito |
|---|---|---|---|---|
| `csv/_test_fork/_etc_pavimenti.py` | `04a6ec32` | `python csv/_test_fork/_etc_pavimenti.py --passi=3` | **se gli 8 pavimenti del gruppo 1 GIRANO col driver**: copertura di riga (`sys.settrace`) sui siti esatti, più i contatori già cablati, con l'**argv costruito dal driver** e non ricostruito | ### **TUTTI E 8 MORTI**: `:4456` `:5737` `:5782` **0 esecuzioni** su 3 passi; `_g_sm_pav_saltati = 15` = le 15 chiamate tracciate. E il freno di scala minima è **già 1 volta per passo pieno** (`3/3/3`, `nsub = 4`) |

**Referto:** `csv/_test_fork/_etc_pavimenti.json` *(blob byte `7c464c26`, committato)*.
**Condizioni:** scena `(ii)(a)`, seme `11`, `n = 2107`, `m = 70199`, **3 passi**, simulatore
`e203f9a8`. **⚠ LIMITE:** `_g_smp_chirurgie = 0` — **la chirurgia sullo snapshot non è stata
esercitata**, perché in 3 passi nessuna mitosi ha diviso un arco.

| strumento | blob (byte) | comando che lo rigira **verbatim** | cosa misura | esito |
|---|---|---|---|---|
| `csv/_test_fork/_etc_lam_stati.py` | `0b89b496` | `python csv/_test_fork/_etc_lam_stati.py` | **`min(d)` e quanti archi stanno sotto `LAM`** nei **16 stati salvati** del pilota. **Sola lettura, nessun run.** `LAM` si legge **dal sorgente** | ### **`min(d) = 0.800000 = LAM` esatto** in 16/16 stati · **0 archi sotto `LAM`** · il pavimento vecchio (`0.05`) sta **16×** più in basso |

**Referto:** `csv/_test_fork/_etc_lam_stati.json` *(blob byte `0ec8cc57`)*.

| strumento | blob (byte) | comando che lo rigira **verbatim** | cosa misura | esito |
|---|---|---|---|---|
| `csv/_seal_fork/_h_etc_2.py` | `a75ce816` | `python csv/_seal_fork/_h_etc_2.py --passi=1 --seme=11` | **`H-ETC-2`**: permutare l'ordine delle cinque leggi dà lo **stesso stato**? Tre permutazioni che **non spostano `mitosi`**, flussi casuali **per legge** iniettati dall'esterno, tolleranza **derivata** `5·2⁻⁵²` | ### **FALLISCE 3/3** sul blob `e203f9a8` *(è l'esito richiesto)*. Controllo positivo: **`0.000000e+00`** esatto. **Esce `1`** |

**Referto:** `csv/_seal_fork/_h_etc_2.json` *(blob byte `1da33034`)*.
**⚠ Il presidio RILANCIA SE STESSO con `PYTHONHASHSEED=0`** *(`HASHSEED-RIPROD`)*: senza,
**il referto non è riproducibile fra processi**.

| strumento | blob (byte) | comando che lo rigira **verbatim** | cosa misura | esito |
|---|---|---|---|---|
| `csv/_test_fork/_hashseed_prova.py` | `02136001` | `PYTHONHASHSEED=1 python csv/_test_fork/_hashseed_prova.py --out=hs1.npz` · idem con `=2` · `python csv/_test_fork/_hashseed_prova.py --confronta hs1.npz hs2.npz` | **`PYTHONHASHSEED` cambia lo stato del simulatore?** Solo il simulatore: nessun presidio, nessuna iniezione di `rng`, **e lo strumento non contiene `hash()`** | ### **23/23 grandezze IDENTICHE byte per byte** → **`HASHSEED-RIPROD` è un falso allarme**, chiuso come `non-difetto` |

**Referto:** `csv/_test_fork/_hashseed_prova.json`. *(Gli `.npz` sono locali e non committati: il
comando è il dato.)*
**E `csv/_seal_fork/_h_etc_2.py` passa a `708e1b6e`**: il rilancio automatico con
`PYTHONHASHSEED=0` è **rimosso**. L'esito e il referto *(`sha1 1da33034`)* **non cambiano**.

| strumento | blob (byte) | comando che lo rigira **verbatim** | cosa misura | esito |
|---|---|---|---|---|
| `csv/_seal_fork/_h_etc_1.py` | `7851ef01` | `python csv/_seal_fork/_h_etc_1.py` | **`H-ETC-1`**: chiamate a `calcola_psi` **prive di `w`** fra le funzioni raggiungibili dalle cinque leggi. **Collaudo a due facce** con sorgenti sintetici incorporati | ### **FALLISCE, conta 8** sul blob `e203f9a8` *(è l'esito richiesto, e coincide con la FASE 0)*. Collaudo **3/3**. **Esce `1`** |

**Referto:** `csv/_seal_fork/_h_etc_1.json` *(blob byte `a1b36398`)*.

## `(b)1` — l'archiviazione dei pavimenti morti, e il suo sigillo *(2026-09-27)*

| strumento | blob (byte) | comando che lo rigira **verbatim** | cosa misura | esito |
|---|---|---|---|---|
| `csv/_test_fork/_hashseed_prova.py` | `71fa4f9b` | `python csv/_test_fork/_hashseed_prova.py --out=X.npz --seme=11 --passi=3` · `… --confronta A.npz B.npz` | **confronta DUE STATI byte per byte** *(23 grandezze)*. Il dump registra `PYTHONHASHSEED` **e il blob del simulatore** | ### `(b)1`: **23/23 identiche**, `e203f9a8` → `59c23942` |

**Referto del sigillo:** `csv/_seal_fork/_sig_arch_pavimenti.json` *(blob byte `02222028`)*.
**Archivio:** `csv/_archivio/_pavimenti_morti.py` *(blob byte `346fdd15`)* — **non gira**.
**Lo stato PRIMA si rigenera dal tag**, e questo è il comando *(gli `.npz` sono locali: il dato è
il comando)*:

```
git checkout pre-archivio-pavimenti -- soliton_simulator.py
python csv/_test_fork/_hashseed_prova.py --out=PRIMA.npz --seme=11 --passi=3
git checkout HEAD -- soliton_simulator.py
python csv/_test_fork/_hashseed_prova.py --out=DOPO.npz --seme=11 --passi=3
python csv/_test_fork/_hashseed_prova.py --confronta PRIMA.npz DOPO.npz
```

> ### ⚠ **DUE STRUMENTI DIVENTANO REPERTI, e la voce va letta così:**
> **`csv/_test_fork/_etc_pavimenti.py`** *(blob `04a6ec32`)* **NON è più ri-girabile come sigillo**:
> cita `:4453` `:4456` `:5737` `:5782`, **righe che dopo la rimozione non significano più quello**.
> **È un REPERTO**, e il suo referto `_etc_pavimenti.json` **è il dato**. *(Non è un difetto nuovo:
> era una verifica una-volta-sola.)*
> **`csv/_seal_fork/_sigillo_Z1c.py`** nomina `_pav_d0` nel docstring fra le funzioni che **non**
> toccava: **va riletto prima di ri-girarlo.**

| strumento | blob (byte) | comando che lo rigira **verbatim** | cosa misura | esito |
|---|---|---|---|---|
| `csv/_test_fork/_hashseed_prova.py` | `2df2dbc3` | `… --out=X.npz --seme=11 --passi=3 [--extra=--scala-min]` · `… --confronta A.npz B.npz` | ora accetta **`--extra`** *(flag aggiunti a quelli del driver)* e **registra l'ARGV INTERO** nel dump, così un confronto **dichiara** la configurazione invece di assumerla *(`P5`)* | sigillo della **precedenza**: **3 bracci su 3** |

**Referto:** `csv/_seal_fork/_sig_precedenza_scalamin.json` *(blob byte `cf99c93d`)* — i tre bracci
col dettaglio. **I comandi dei tre bracci** *(gli `.npz` sono locali: il dato è il comando)*:

```
# A - col driver: tag contro corretto
git checkout pre-archivio-pavimenti -- soliton_simulator.py
python csv/_test_fork/_hashseed_prova.py --out=PRIMA.npz --seme=11 --passi=3
git checkout HEAD -- soliton_simulator.py
python csv/_test_fork/_hashseed_prova.py --out=A_dopo.npz --seme=11 --passi=3
python csv/_test_fork/_hashseed_prova.py --confronta PRIMA.npz A_dopo.npz

# B - con --scala-min E --scala-min-passo insieme
git checkout pre-archivio-pavimenti -- soliton_simulator.py
python csv/_test_fork/_hashseed_prova.py --out=B_tag.npz --seme=11 --passi=3 --extra=--scala-min
git checkout HEAD -- soliton_simulator.py
python csv/_test_fork/_hashseed_prova.py --out=B_dopo.npz --seme=11 --passi=3 --extra=--scala-min
python csv/_test_fork/_hashseed_prova.py --confronta B_tag.npz B_dopo.npz

# C - IL CONTROLLO CHE DEVE FALLIRE: il blob ROTTO
git checkout 7840039 -- soliton_simulator.py
python csv/_test_fork/_hashseed_prova.py --out=B_rotto.npz --seme=11 --passi=3 --extra=--scala-min
git checkout HEAD -- soliton_simulator.py
python csv/_test_fork/_hashseed_prova.py --confronta B_tag.npz B_rotto.npz     # DEVE dare DIVERSE
```

## `(b)2` — l'archiviazione di `SYNC_UPDATE`, e il suo sigillo *(2026-09-27)*

| referto | blob (byte) | esito |
|---|---|---|
| `csv/_seal_fork/_sig_arch_sync.json` | `6de5a9d2` | ### **5 bracci su 5**, blob `f845d30d` → `7439d5c3` |
| `csv/_archivio/_sync_update.py` *(archivio, non gira)* | `2ed18d5e` | 7 blocchi + 9 ternari |

**I comandi, verbatim** *(gli `.npz` sono locali: il dato è il comando; lo strumento è
`csv/_test_fork/_hashseed_prova.py`, blob `2df2dbc3`)*:

```
# i due stati PRIMA (dal tag)
git checkout pre-archivio-sync -- soliton_simulator.py
python csv/_test_fork/_hashseed_prova.py --out=S_prima_off.npz --seme=11 --passi=3
python csv/_test_fork/_hashseed_prova.py --out=S_prima_on.npz  --seme=11 --passi=3 --extra=--sync
git checkout HEAD -- soliton_simulator.py
# i due stati DOPO
python csv/_test_fork/_hashseed_prova.py --out=S_dopo_off.npz --seme=11 --passi=3
python csv/_test_fork/_hashseed_prova.py --out=S_dopo_on.npz  --seme=11 --passi=3 --extra=--sync
# i cinque bracci
python csv/_test_fork/_hashseed_prova.py --confronta S_prima_off.npz S_dopo_off.npz   # A: IDENTICO
python csv/_test_fork/_hashseed_prova.py --confronta S_prima_on.npz  S_dopo_on.npz    # B: DIVERSO
python csv/_test_fork/_hashseed_prova.py --confronta S_dopo_off.npz  S_dopo_on.npz    # C: IDENTICO
python csv/_test_fork/_hashseed_prova.py --confronta S_prima_off.npz S_prima_on.npz   # D: DIVERSO
python csv/_test_fork/_hashseed_prova.py --confronta S_prima_off.npz S_dopo_on.npz    # E: IDENTICO
```

> ### ⚠ **`B` e `D` sono la STESSA comparazione**: poiché `E` prova `dopo+sync == prima-senza-sync`,
> `B` coincide con `D` — **e infatti danno le stesse 19 grandezze**. **I bracci indipendenti sono
> QUATTRO: `A`, `C`, `D`, `E`.**

| strumento | blob (byte) | comando che lo rigira **verbatim** | cosa misura | esito |
|---|---|---|---|---|
| `csv/_test_fork/_etc_rami_morti.py` | `900d19c0` | `python csv/_test_fork/_etc_rami_morti.py --passi=3` | **i rami MORTI col driver** dentro il perimetro della cura (c). Criterio deciso **dai flag** e non dal campionamento; corroborato con la copertura sulle **righe esclusive** | ### **121 rami, 243 righe**, in **57** funzioni. **0 righe esclusive hanno eseguito** |

**Referto:** `csv/_test_fork/_etc_rami_morti.json`. **Tabella intera:** `doc/RAMI_MORTI_perimetro_c.md`.
**⚠ 61 rami NON sono corroborabili per riga** *(ternari e `if` di una riga: il ramo morto condivide
la riga col vivo)* e sono **dichiarati tali**.

## `(c)1` — il confine del passo, e il suo sigillo *(2026-09-27)*

| referto | blob (byte) | esito |
|---|---|---|
| `csv/_seal_fork/_sig_etc_c1.json` | `2dfeadd6` | ### **byte-identico 23/23** + **contatori `3` e `12`**, blob `7439d5c3` → `b5a713d1` |

**Lo strumento passa a `e6e1f212`**: il dump registra ora gli **otto contatori del confine del
passo** (`_g_smp_aperture`, `_g_smp_gia_aperta`, `_g_smp_chiusure`, `_g_smp_d_chiusure`,
`_g_smp_chirurgie`, `_g_smp_disallineati`, `_g_sm_patol`, `_g_sm_nascite`), così **ogni sigillo
futuro li porta** invece di supporli.

```
git checkout adbaca9~1 -- soliton_simulator.py
python csv/_test_fork/_hashseed_prova.py --out=PRIMA.npz --seme=11 --passi=3
git checkout HEAD -- soliton_simulator.py
python csv/_test_fork/_hashseed_prova.py --out=DOPO.npz --seme=11 --passi=3
python csv/_test_fork/_hashseed_prova.py --confronta PRIMA.npz DOPO.npz
```

> ### ⚠ **Il byte-identico DA SOLO non basta per questo sigillo:** la fotografia serve al freno, e il
> freno chiude **solo se è aperta** — un confine sparito darebbe lo stesso stato. **Sono i contatori
> a distinguere le due cose.**

| strumento | blob (byte) | comando che lo rigira **verbatim** | cosa misura | esito |
|---|---|---|---|---|
| `csv/_test_fork/_etc_schedulatore.py` | `83405bd9` | `python csv/_test_fork/_etc_schedulatore.py` | i **tre inventari** del piano dello schedulatore: il **TIPO** di ogni funzione del passo *(dedotto da cosa scrive)*, **cosa scrive ogni legge** e in che forma, e **tutte le letture di `pos`** nelle leggi fisiche | **57** funzioni: `dinamica` 9, `vincolo` 1, `disegno` 2, `osservatore` 44, **`AMBIGUA` 1** *(`mitosi`)* · **11** letture di `pos` in 5 funzioni |

**Referto:** `csv/_test_fork/_etc_schedulatore.json`. **Piano:** `doc/PIANO_schedulatore_passo.md`.
**⚠ Analisi STATICA e PER NOME**, come la FASE 0: i tipi sono una **proposta da confermare
leggendo**, e le `AMBIGUA` sono quelle che il mandato chiede di segnalare.

## `T1` dello schedulatore, e il suo sigillo *(2026-09-28)*

| referto | blob (byte) | esito |
|---|---|---|
| `csv/_seal_fork/_sig_sched_t1.json` | `48537064` | ### **tre criteri su tre**, blob `e06dcb4e` → `e287a43e` |

**I tre criteri:** ① **byte-identico 23/23** · ② **contatori** `aperture = chiusure = passi = 3`,
`disallineati = 0`, e ### **`gia_aperta` da 4 per passo a ZERO** · ③ **il caso che deve fallire**:
`H-P9` **rifiuta** un chiamante che salta l'esecutore e **accetta** chi lo usa.

```
git checkout acaf86b~1 -- soliton_simulator.py
python csv/_test_fork/_hashseed_prova.py --out=PRIMA.npz --seme=11 --passi=3
git checkout HEAD -- soliton_simulator.py
python csv/_test_fork/_hashseed_prova.py --out=DOPO.npz --seme=11 --passi=3
python csv/_test_fork/_hashseed_prova.py --confronta PRIMA.npz DOPO.npz
```

**Il controllo ③ si rigira** creando due sorgenti sintetici — uno che fa `net.step()` in un ciclo,
uno che chiama `esegui_passo` — e passandoli a `csv/_hook_presidi.py::_avanza_con_step`: **il primo
deve essere rifiutato, il secondo deve passare.** *(I due file sono locali: il dato è il comando.)*

## `T2` dello schedulatore: i **referti rigirati** dopo `L_CONSERVA` *(2026-09-28)*

> **Perché rigirati:** `L_CONSERVA` *(`56552f0`, simulatore `fe00b48a` → `1fc9235f`)* ha **tolto una
> chiamata** e **tolto la catena** che rendeva incoerente un tipo. **I due referti di prima
> descrivevano un blob che non c'è più**, e li si rigira: **un referto scaduto è un numero senza
> provenienza.**

| strumento | blob (byte) | comando che lo rigira **verbatim** | cosa misura | esito |
|---|---|---|---|---|
| `csv/_seal_fork/_sig_sched_tipi.py` | `e60f6f65` | `python csv/_seal_fork/_sig_sched_tipi.py` | il **tipo dichiarato** in `_PASSO_TIPI` è **coerente con ciò che la funzione SCRIVE**, dedotto dall'AST | ### **8 su 8 coerenti**, `non_coerenti = 0`, sul blob `1fc9235f`. **Esce `0`** |
| `csv/_seal_fork/_h_etc_1.py` | `7851ef01` | `python csv/_seal_fork/_h_etc_1.py` | **`H-ETC-1`**: chiamate a `calcola_psi` **prive di `w`** fra le **53** funzioni raggiungibili dalle cinque leggi | ### **conta `7`**, e `ATTESO_OGGI = 7`: era **8** sul blob `e203f9a8`, e la chiamata che è sparita è quella di `_togli_rotazione_rigida` |

**Referti:** `csv/_seal_fork/_sig_sched_tipi.json` *(blob byte `a289bc47`)* ·
`csv/_seal_fork/_h_etc_1.json` *(blob byte `19068acd`)*. **Entrambi dichiarano `blob_sim
1fc9235f`.**

## Il sigillo dei **segni**: una sola legge scrive ogni grandezza-segno *(2026-09-28)*

> ### 📌 **Nasce da una CORREZIONE DEL GUARDIANO**, non da un dubbio mio: nel documento delle regole
> di `T3` avevo scritto che `perc_chi` è **scritta due volte nello stesso passo** e che *«la seconda
> sovrascrive la prima»*. **È falso** — `:5639` e `:5642` sono l'`if` e l'`else` della **stessa
> condizione**. **L'analisi statica vede le scritture e non le condizioni che le escludono.**

| strumento | blob (byte) | comando che lo rigira **verbatim** | cosa misura | esito |
|---|---|---|---|---|
| `csv/_seal_fork/_sig_segni_una_legge.py` | `48fb1141` | `python csv/_seal_fork/_sig_segni_una_legge.py --passi=3` | **copertura di riga a RUNTIME** dei tre siti che scrivono una grandezza-segno, con l'argv del driver sulla scena `(ii)(a)` | ### **un solo sito per grandezza**: `perc_geom` ← `:5639` **3/3**, `perc_chi` ← `:5666` **3/3**, `:5642` **ZERO**. **Esce `0`** |

**Referto:** `csv/_seal_fork/_sig_segni_una_legge.json` *(blob byte `db4e1cdb`)*.
**Flag che decidono:** `CHI_BASC=True CHI_COOP=True CHI_DA_SPINORE=False SPINORE_CORRETTO=True`.
**Scena:** `MASSE-COERENTI`, seme `11`, `n = 2107`, `m = 70199`, **3 passi pieni**.
**Il verdetto viene dalla copertura, non dal conteggio** — ed è per questo che vale: `:5666` gira
**con `CHI_DA_SPINORE` SPENTO**, perché `_chi_da_psi = CHI_DA_SPINORE or CHI_COOP` *(`:5653`)*.

## Le decisioni di Luca sull'indice: **la patch, e non si rilancia** *(2026-09-28)*

| strumento | blob (byte) | comando | cosa fa |
|---|---|---|---|
| `csv/_archivio/_indice_decisioni_6.py` | `2377ec89` | `python csv/_archivio/_indice_decisioni_6.py` | **16 modifiche** a `doc/INDICE_ID.tsv`: le **sei decisioni** di Luca sulle pendenze del checkpoint `bd3baa1`, più la correzione di `SCHED-T2-TIPI` |

**⚠ NON SI RILANCIA:** ogni sostituzione **asserisce il valore vecchio** e ogni aggiunta **fallisce
se il testo c'è già** *(`P1-quater`)*, quindi un secondo giro **esce `1` senza scrivere**. Il
referto è **l'indice stesso**, e la tabella delle 16 modifiche è nel messaggio del commit.

## `T3`, il classificatore della SOVRAPPOSIZIONE *(2026-09-28)*

> ### ⚠ **UNA LACUNA MIA, e la dichiaro: questa voce MANCAVA.** Lo strumento e' nato in `5ac5150` e
> **non ha avuto la sua voce nell'inventario in quel commit**, che e' il par.6 ① di `CLAUDE.md`.
> **E' una regola scritta, non un presidio** (`A9`), e infatti non ha impedito niente. **Recuperata
> qui, col ritardo dichiarato.**

| strumento | blob (byte) | comando che lo rigira **verbatim** | cosa misura | esito |
|---|---|---|---|---|
| `csv/_test_fork/_etc_sovrapposizione.py` | `d0c8e951` | `python csv/_test_fork/_etc_sovrapposizione.py` | la **FORMA di composizione** di ogni scrittura di stato nel perimetro delle cinque leggi: le **cinque forme** di Luca, le **due accettate** *(`6 gruppo`, `7 nascita`)* e **l'esenzione** *(`0 segno`)* | **94** scritture, e ### **le ECCEZIONI sono ZERO**: `1` 22 · `2` 6 · `3` 14 · `4` 6 · `5` 40 · `6` 2 · `7` 1 · `0` 3 |

**Referto:** `csv/_test_fork/_etc_sovrapposizione.json` *(blob byte `d3b5aa68`)*.
**E scrive anche `doc/REGOLE_composizione_T3_tabelle.md`**, cioe' **le tabelle del documento**: non
si ricopiano a mano (`L-NUMERI`), **le genera lui a ogni giro**.
**Blob precedenti:** `9b683cbf` *(14 eccezioni, prima delle decisioni)* → `d0c8e951`.
**⚠ Analisi STATICA:** l'esenzione `0 segno` **regge su una condizione che questo strumento NON puo'
verificare**, e la verifica vive in `csv/_seal_fork/_sig_segni_una_legge.py`, **a runtime**.

| strumento | blob (byte) | comando | cosa fa |
|---|---|---|---|
| `csv/_archivio/_indice_t3_punto7.py` | `ac6ef486` | `python csv/_archivio/_indice_t3_punto7.py` | le **tre voci nuove** di `T3` *(`TORS-SPINTA`, `MAX-NODI-FERMA`, `MITOSI-SOGLIA-GRAD`)* piu' l'**attribuzione** in `MITOSI-NON-DIVISA` |

**⚠ NON SI RILANCIA:** ogni voce **fallisce se l'id esiste** e ogni aggiunta **fallisce se il testo
c'e' gia'**. Il referto e' **l'indice stesso**.

## `MAX-NODI-FERMA`, il sigillo *(2026-09-28)*

| strumento | blob (byte) | comando che lo rigira **verbatim** | cosa misura | esito |
|---|---|---|---|---|
| `csv/_seal_fork/_sig_max_nodi.py` | `8120a2af` | `python csv/_seal_fork/_sig_max_nodi.py` | **quattro bracci**: **(A)** byte-identita' col driver · **(B)** il **caso che deve fallire**, in due sotto-casi *(la semina e lo schedulatore)* · **(C)** il **controllo positivo** sul blob **vecchio** · **(E)** la **FORMA** del controllo in `semina`, **statica** | ### **PASSA.** (A) ### **tutte e 23 le grandezze identiche byte per byte** · (B) **2 su 2** fermano il run · (C) **2 su 2**, il vecchio **non si ferma** · (E) ### **1 chiamata, 0 dentro un ramo** |

**Referto:** `csv/_seal_fork/_sig_max_nodi.json` *(blob byte `3316c0ba`)*.
**Simulatore:** `2feb5ba0`; **il vecchio** e' `1fc9235f`, estratto **in binario** dal **PADRE** del
commit della cura *(`95249c5~1`, cioe' `H-P8`: non si prende <<il codice di prima>> da `HEAD`)*.

**Bracci interni, che il sigillo lancia in SOTTOPROCESSO** *(un `raise` va visto **come esce il
processo**)*:
```
python csv/_seal_fork/_sig_max_nodi.py --corri=<MAX_NODI> [--sim=<percorso>] [--passi=N]
python csv/_seal_fork/_sig_max_nodi.py --sintetico [--sim=<percorso>]
```
**IL BRACCIO `E` E' STATICO E NASCE DA UN FALLIMENTO:** il ramo **senza `--semina-lam`** -- quello
che la prima stesura della cura **lasciava scoperto** -- ### **non e' raggiungibile a runtime sulla
scena dei sigilli**, perche' la scena `MASSE-COERENTI` chiama `semina(-1)`, cioe' **chiede la
saturazione**, e senza `SEMINA_LAM` alza il `SystemExit` che c'era **da prima**. **Provato: il
braccio falliva su ENTRAMBI i blob, cioe' non misurava la cura.** Allora si verifica **la FORMA**:
`_ferma_se_oltre_max_nodi` in `semina` e' ### **UNA chiamata, 0 dentro un ramo, 1 nel corpo** --
quindi copre **entrambi i rami per costruzione**. ⚠ **E' una lettura statica, e lo dico** (`A9`).
**La dump `PRIMA`** *(`csv/_seal_fork/_sig_max_nodi/PRIMA.npz`)* **e' presa col blob `1fc9235f`**, e
questo sigillo **non puo' ricostruirla da se'**: se manca, **si ferma e lo dice**.

> ### ⚠ **IL PRIMO GIRO E' FALLITO, e conta piu' del secondo.** Il braccio `B2` aspettava che una
> **NASCITA** sforasse il tetto: sulla scena `(ii)(a)` seme `11` ci sono ### **40 passi con ZERO
> nascite**, quindi `n` non cresce. ### **Era il braccio a essere mal progettato, non la cura.**
> Il sito dello schedulatore si esercita con un **`net` sintetico** *(basta `.n`, perche' il
> controllo sta **prima** di toccare `net`)*, e il controllo positivo e' **netto**: il nuovo solleva
> **`LimiteNodiSuperato`**, il vecchio **arriva a toccare `net`** e muore di **`AttributeError`**.

**E un fatto misurato sul VECCHIO, piu' forte di quello che credevo:** con `MAX_NODI = 100` il blob
vecchio **costruisce una scena di 2107 nodi e gira 3 passi senza dire niente**. Nel ramo di
saturazione il tetto veniva **sovrascritto** da `n = len(p)`: ### **non troncava nemmeno -- lo stato
finiva a 21 volte la propria guardia, in silenzio.** E' la ragione per cui il controllo nuovo sta
**anche DOPO la geometria**.

**⚠ RESTA DICHIARATO E NON MISURATO:** quanto valga lo **sforo** dentro un passo. **Serve una scena
che cresce**, cioe' un run lungo: e' una misura a se'.

## `T3` pezzo ②, i passi 0-1: **il flash, i suoi siti, il rinculo** *(2026-09-28)*

| strumento | blob (byte) | comando che lo rigira **verbatim** | cosa misura | esito |
|---|---|---|---|---|
| `csv/_test_fork/_flash_passo01.py` | `605fe10b` | `python csv/_test_fork/_flash_passo01.py` | **SOLA LETTURA**: l'AST del simulatore e i **61 fotogrammi LOCALI** del pilota. ① il **salto** di `mean(phi_g)` passo per passo · ② i **siti** con la guardia `len(self.psi) < n` e quali sono **raggiungibili dopo `mitosi`** · ③ **quando morde** il rinculo a indici ripetuti | ### **il flash SMETTE**: solo ai passi `2`, `42`, `58`, `62`, `68`, e dal 70 al 120 il salto e' `1.000` con nascite a ogni fotogramma · **salto al passo 42: `2.631x` su `phi_g`, `1.622x` su `|psi|`** · **siti 7, due dopo `mitosi`** |

**Referto:** `csv/_test_fork/_flash_passo01.json` *(blob byte `b799994e`)*.
**⚠ I FOTOGRAMMI SONO LOCALI** (`STATI-LOCALI`, `.gitignore`): `csv/_test_fork/_pilota_prova1/stati/`,
81 `.npz` prodotti dal run `pilota-prova1-stati` sul blob `e203f9a8`. **Senza quelli lo strumento
lo dice e non misura il passo 0.**
**E NON PERMETTONO DI RIPARTIRE:** mancano `d`, `d0`, `vd`, `peq`, `tw`, `twp`, `psi`, `psi_spin`,
`eta`, `phivel`. ### **Il sigillo del pezzo ② deve RIFARE il run fino al passo 44, su due blob:
~21 s per passo su un seme, cioe' ~30 minuti in tutto.**

## La scena dei sigilli, DICHIARATA — e i sigilli che non hanno mai visto una nascita *(2026-09-28)*

> ### ⚠ **Rilievo del guardiano:** `csv/_test_fork/_hashseed_prova.py` imponeva `sep = 3.0` e
> `nmasse = 2` **a mano**, mentre il dump registrava `_argv` col **`--sep 6.1158`** del driver.
> ### **Il referto dichiarava una configurazione diversa da quella che girava** (`P5`). E la
> conseguenza e' piu' grossa della forma: **tutti i sigilli che dicono «scena `(ii)(a)`, argv del
> driver» sono girati sulla scena PICCOLA** -- `2107` nodi, **zero nascite in 40 passi**.

| strumento | blob (byte) | comando che lo rigira **verbatim** | cosa misura | esito |
|---|---|---|---|---|
| `csv/_test_fork/_hashseed_prova.py` | `fa225a95` | `python csv/_test_fork/_hashseed_prova.py --out=X.npz --seme=11 --passi=3` | *(invariato nel confronto)* e **ORA DICHIARA LA SCENA**: `_scena_nmasse`, `_scena_sep`, `_scena_*_argv`, `_scena_n`, `_scena_m`, `_scena_nota` | la **scena piccola RESTA** *(i dump devono restare confrontabili)*, ma a schermo e nel dump compaiono **le DUE scene**, con l'avviso quando differiscono |
| `csv/_test_fork/_sigilli_senza_nascite.py` | `7401720d` | `python csv/_test_fork/_sigilli_senza_nascite.py` | quali commit hanno toccato **la regione delle nascite**, derivato **da git** | **179** commit sul simulatore, ### **37 nella regione delle nascite**, di cui **13** portano un file di sigillo nel commit |

**Referto:** `csv/_test_fork/_sigilli_senza_nascite.json` *(blob byte `9fc81805`)*; la stampa in
`csv/_seal_fork/_sig_nascita_atomica/_elenco_senza_nascite.txt` *(`dce02307`)*.

> ### ⚠ **IL CRITERIO E' PER TESTO, NON PER RAGGIUNGIBILITA', e lo strumento lo dichiara** (`A9`):
> riconosce la regione dai marcatori `concatenate([self.`, `vstack([self.`, `COPPIA_MIT`,
> `coppie_nate`, `pos_figlio`, `d0new`, `perc_tw`, `_g_nati_`. Un commit puo' comparire per un
> `concatenate` **fuori** dalla mitosi, e uno puo' **mancare**. ### **E' UN ELENCO DA LEGGERE, NON
> UN VERDETTO** -- e il mandato dice *«solo l'elenco, niente da rifare adesso»*.
>
> ### **E che cosa NON vuol dire:** non vuol dire che quei sigilli siano sbagliati. Vuol dire che
> **il loro braccio di byte-identita' NON HA PERCORSO quei rami**, e quindi **non dice niente su di
> essi.**

## `PSI-FLASH`, il sigillo — **cinque bracci su cinque** *(2026-09-28)*

| strumento | blob (byte) | comando che lo rigira **verbatim** | cosa misura | esito |
|---|---|---|---|---|
| `csv/_seal_fork/_sig_nascita_psi.py` | `3e6b00ad` | `python csv/_seal_fork/_sig_nascita_psi.py --passi=46` | **A** byte-identita' nei passi **senza** nascite *(scena piccola)* · **B** `lambda` degli archi al passo di nascita *(scena GRANDE)* · **C** `mean(phi_g)` al passo di nascita · **D** il **caso che deve fallire** sul blob PRE-CURA · **E** i due ripieghi, **distinti** | ### **PASSA 5/5.** A **23 su 23** identiche · B **0** chiamate non ricorsive fuori intervallo · C ### **`1.0524x` la base invece di `2.812x`** · D sul PRE-CURA **8 chiamate a LAM su 13** e pozzo **366.17** · E nessun `SchermaturaSpenta`, e **302 = 302** |

**Referto:** `csv/_seal_fork/_sig_nascita_psi.json` *(blob byte `1ab27a01`)*; la stampa in
`csv/_seal_fork/_sig_nascita_psi/_corsa.txt` *(`bd15e71e`)*.
**Simulatore `407e6c51`; il PRE-CURA e' `05691d41`**, preso da un **`git worktree`** sul **PADRE**
del commit che introduce la cura *(`4efd3ae4`)* -- ### **ancora NON pinnata** (`H-P8`). Il worktree
serve perche' `_hashseed_prova.py` carica il simulatore **dal disco** e non ha un `--sim`:
### **cosi' lo strumento di allora gira sul simulatore di allora**, coerenti fra loro. **E si rimuove
a sigillo chiuso.**

> ### 📌 **Il numero che dice la cura in una riga:** al passo di nascita le chiamate a `LAM` passano
> da ### **8 su 13** a ### **7 su 12**. **La chiamata sparita e' esattamente UNA:** quella che il
> ripiego `len(psi) < n` causava. **E le 7 che restano sono la ricorsione, che e' la definizione.**

**La scena si prende da `a`** *(`nmasse`, `sep` del driver)*, **non scritta a mano**: e' l'errore che
aveva fatto misurare tutto sulla scena piccola.
**⚠ E una soglia SCELTA, dichiarata:** il braccio `C` usa *«entro il 10 %»*. **Serve a distinguere
`1.05` da `2.81`, non a misurare.**

## 🗄 Il banco della scomposizione, **archiviato come superato** *(2026-09-28)*

| file | blob (byte) | che cos'e' |
|---|---|---|
| `csv/_archivio/_flash_scomposizione.py` | `3125acef` | la versione **corretta** *(serie di `mean(phi_g)`, criterio `V5` cablato)* |
| `csv/_archivio/_flash_scomposizione_ROTTO.py` | `868fffea` | quella col **ciclo `O(m^2)`** che ha **bloccato due run** |

**Perche' esce** *(decisione di Luca)*: ### **la domanda a cui rispondeva -- <<quale ingrediente
porta il `2.6`?>> -- e' chiusa: lo porta la schermatura che si spegne.**
**E perche' non ci e' arrivato:** il suo criterio ④ confrontava `psi` calcolato **dentro** `step` con
un ricalcolo su uno stato **gia' cambiato**. ### **Era MAL POSTO, e l'avevo scritto io.**
*(Un banco archiviato senza il perche' e' un reperto muto.)*

## L'elenco dei ripieghi `len(x) < n` -> valore di scorta *(2026-09-28)*

| strumento | blob (byte) | comando che lo rigira **verbatim** | cosa misura | esito |
|---|---|---|---|---|
| `csv/_test_fork/_ripieghi_len_n.py` | `7f32fbbd` | `python csv/_test_fork/_ripieghi_len_n.py --passi=46` | **due passaggi**: ① dall'**AST**, ogni confronto fra un `len(...)` e `n`/`self.n` · ② **a RUNTIME**, quali prendono davvero il **ramo di scorta**, e in quale passo | ① ### **100 confronti in 26 funzioni** · ② al passo di **nascita** ### **NESSUNO**; al passo **dopo** ### **DUE**: `_rho_sorgente` :4384 *(2 su 15)* e `_passo_spinoriale` :3570 *(1)* |

**Referto:** `csv/_test_fork/_ripieghi_len_n.json` *(blob byte `de9c12ed`)*; la stampa in
`csv/_seal_fork/_sig_nascita_psi/_ripieghi.txt`.

> ### 📌 **E l'elenco NON e' un verdetto, che e' il punto:** dei due siti che mordono al passo dopo,
> **uno e' il DIFETTO** *(`_rho_sorgente` da' un'altra densita' a tutta la rete, in silenzio)* e
> ### **l'altro e' LEGITTIMO E DICHIARATO** -- `_xi_rumore` :3570, dove il codice scrive *«questo
> NON e' un fallback: e' il percorso normale della mitosi; `xi` e' l'AMBIENTE, non una proprieta'
> del nodo, quindi il figlio NON lo eredita»*, ed e' **gia' contato**.
> ### **Su 100 confronti della stessa FORMA, quelli che mordono sono 2 e uno e' giusto: la forma non
> basta a giudicare.**

**⚠ La traccia si accende dal passo 41**, e il prezzo e' dichiarato: dei passi prima non si sa
niente. **Con `settrace` su tutto, su 471564 archi, il run NON FINIVA** -- misurato, e fermato.

### ⛔ Il sigillo di `PSI-FLASH`, secondo giro a **72 passi**: **FALLISCE** *(2026-09-28)*

`csv/_seal_fork/_sig_nascita_psi.py` passa a **`1d1e5edf`** *(corsa fino al passo chiesto, e il
**braccio `F`**: il passo dopo **ogni** nascita entro il 5 % dalla base)*. Referto **`acd584a2`**,
stampa `_sig_nascita_psi/_corsa72.txt` *(`f9fd7363`)*.

| | |
|---|---|
| **A B C D** | **PASSANO** |
| ### **E** | ### **FALLISCE -- e il braccio e' MAL POSTO, l'ho scritto io**: confronta somme su **domini diversi** *(i passi senza nascite non sono gli stessi nei due giri)* |
| ### **F** | ### **FALLISCE: `10.48 %` contro il `5 %`.** Ma lo scostamento peggiore va da **`168.70 %`** a **`10.48 %`**, un **fattore 16** |

**⚠ E le due traiettorie DIVERGONO:** il PRE-CURA ha nascite in **12** passi, il curato in **8**, e in
passi diversi. ### **La cura ha cambiato la dinamica -- atteso -- ma allora il confronto per passo,
dopo il 42, non confronta la stessa cosa.**
**⚠ E la base e' una MEDIA GLOBALE su una serie che DERIVA:** uno scostamento da lei misura **anche
la deriva**, non solo il gradino.

### ✅ Il sigillo di `PSI-FLASH`, **terzo giro: sei bracci su sei** *(2026-09-28)*

`csv/_seal_fork/_sig_nascita_psi.py` blob **`dfebef2a`**, referto **`bf50de74`**, stampa
`_sig_nascita_psi/_corsa72c.txt` *(`ab0ecd50`)*. Simulatore **`f7541d03`**, PRE-CURA **`05691d41`**,
scena **GRANDE** fino al **passo 72**.

| braccio | criterio | esito |
|---|---|---|
| **A** | byte-identita' nei passi senza nascite | **23 su 23** |
| **B** | `lambda` al passo di nascita | **0** chiamate non ricorsive fuori intervallo |
| **C** | `mean(phi_g)` al passo di nascita | `1.0505x` la base |
| **D** | il caso che deve fallire | sul PRE-CURA **8 su 13** a `LAM`, pozzo **366.17** |
| ### **E** | ### **PER PASSO, sullo stesso dominio** | **41** passi comuni, ### **ZERO** differenti, `7`-`8` ricorsioni per passo in entrambi. **Totale riportato e non confrontato: 517 / 505** |
| ### **F** | ### **NESSUN SALTO** | oscillazione naturale **`2.1010 %`** al passo 7 *(passi 4-41)*; curato ### **`1.7281 %`**; PRE-CURA ### **`197.2613 %`**, che la supera **94 volte** |

> ### ⚠ **E il metro di `F` era 40 volte troppo largo nella prima stesura:** dentro c'era il
> **transitorio d'avvio** *(`86.66 %` al passo 2)*. `phi_g(0)` e' **zero esatto**, quindi i primi
> salti sono **il campo che nasce**, non oscillazione. ### **La scelta del confine NON e' fragile ed
> e' misurata: da 4 e da 6 il metro e' LO STESSO** su entrambi i giri -- quindi non e' una manopola
> (`A1`). **E non ho chiuso sul PASS ottenuto col metro largo: ho stretto e rigirato.**

**SI RIPORTA, e pesa:** il PRE-CURA ha nascite in **12** passi con **30** nati e `n` finale
**12832**; il curato in **8** passi con **10** nati e `n` finale **12812**.
### ➜ **Le nascite calano di un fattore TRE**, ed e' atteso con un meccanismo preciso: il flash
**gonfiava `psi` di `1.62x`**, e una `psi` gonfiata **fa scattare piu' mitosi**.
### **Quindi parte della mitosi di prima era PRODOTTA DAL CAMPO GONFIATO** -- e ogni conteggio di
nascite misurato prima di questa cura, nei passi con nascite, viene da un campo gonfiato.

---

## La PROVA A GUASTO dei ripieghi *(2026-09-28)*

| strumento | blob (byte) | comando che lo rigira **verbatim** | cosa misura |
|---|---|---|---|
| `csv/_test_fork/_guasto_ripieghi.py` | `3df06c44` | `python csv/_test_fork/_guasto_ripieghi.py --passi=30` | dallo stato al passo **30** della scena **GRANDE**, per **ogni** grandezza per nodo: che cosa fa un passo se la cache e' **CORTA** o **LUNGA** di uno. Quattro esiti: **PROTETTO** *(errore dichiarato)*, **ROTTO RUMOROSO**, **RIPIEGO SILENZIOSO**, **INERTE** |

> ### 📌 **E' COMMITTATO PRIMA DI GIRARE, e quindi qui non ci sono numeri:** il mandato chiede
> **lo strumento prima della misura**, e un esito scritto prima del giro sarebbe una previsione
> travestita da misura. ### **I numeri arrivano nel commit del referto.**

**Perche' esiste:** ### **quattro volte una LETTURA ha sbagliato** su questi stessi siti
*(`full(n,…)` contato come «estende», la condizione fusa chiamata «inizializzazione», `==`/`!=`
messi fuori dal mandato, e il ramo degli `IfExp` invertito)*. **Questa prova non legge: guasta.**

**Tre scelte di misura, dichiarate prima dei numeri:**

| | |
|---|---|
| **`phi` e' ESCLUSA** | `n` **E'** `len(phi)` *(property `:2063`)*: accorciarla non accorcia una cache, ### **cambia `n`** -- e il confronto perderebbe il riferimento |
| **per nodo sui primi `n-1`, per arco INTERI** | un cambiamento su un nodo e' allora **per costruzione** un effetto **su qualcun altro**. *(Tagliare un array per arco a `n-1` guarderebbe `12801` archi su `471564`.)* |
| ### **la riga responsabile si TROVA** | per chi ripiega in silenzio il passo si **rigira col tracciatore** limitato alle funzioni della tabella generata: si registra **quale riga elencata ha ESEGUITO**. ### **Misura, non lettura** |

**Il CONTROLLO e' una condizione di validita', non un braccio:** un passo **due volte da due copie**
di BASE deve essere **byte-identico** *(il generatore e' `net.rng`, dentro la rete, quindi la copia
profonda lo porta con se')*. ### **Se non lo e', lo strumento scrive `vale: false` e si ferma.**

**Il CASO CHE DEVE FALLIRE** *(`P1-sexies`)*: il guasto **CORTO su `psi`** sul blob **PRE-CURA**
*(estratto col padre del commit che introduce `_eredita_psi_figli`, mai un hash fissato a mano)*
deve dare **RIPIEGO SILENZIOSO su TUTTA LA RETE** -- e' il flash di `PSI-FLASH`.
### **Se non lo da', lo strumento esce con `1` e dice che la prova non dimostra niente.**

> ### 📌 **IL CRITERIO E' FISSATO DAL GUARDIANO PRIMA DEI NUMERI:** una grandezza e' **«a posto»**
> solo se **entrambi** i guasti danno **PROTETTO**, **oppure** se danno **INERTE** ed e'
> **DIMOSTRATO** che nessuna legge del passo la legge. ### **«Inerte» da solo NON BASTA**, e lo
> strumento lo stampa accanto al conteggio invece di lasciarlo capire.

> ### ⛔ **Il primo giro (`7582e89c`) e' MORTO nel CONTROLLO, e il difetto era mio.** Il confronto
> sanificava con `nan_to_num` **DOPO** la sottrazione, e il simulatore impone
> **`np.seterr(invalid='raise')`** *(`:8835`, invarianti accesi = default)*.
> ### **`invalid` non scatta su un `nan` che passa: scatta su `inf - inf`** — quindi almeno una
> grandezza per nodo porta un `inf`. **`3df06c44`** sanifica **prima**, sotto `errstate`, conta
> **`NaN` contro `NaN` come UGUALE**, e ### **ELENCA le grandezze non finite** invece di morirci
> sopra. *(Il fallimento e' committato a se': `360e681`.)*

### 🔥 **La prova a guasto, GIRATA** *(2026-09-28)*

| strumento | blob (byte) | comando che lo rigira **verbatim** | cosa misura | esito |
|---|---|---|---|---|
| `csv/_test_fork/_guasto_ripieghi.py` | `682f1ba4` | `python csv/_test_fork/_guasto_ripieghi.py --passi=30` | i due guasti su ogni grandezza **per nodo E per arco** | ### **A POSTO: 0 su 31.** RIPIEGO SILENZIOSO **10** · ROTTO RUMOROSO **8** · INERTE su entrambi **12** · ### **con effetto oltre l'ultimo nodo: 10** |
| `csv/_test_fork/_referto_guasto.py` | `36a44cc8` | `python csv/_test_fork/_referto_guasto.py` | **genera** `doc/RIPIEGHI_guasto.md` dal `json`: nessun numero ricopiato a mano (`L-NUMERI`) | 196 righe |

**Referti:** `csv/_seal_fork/_guasto_ripieghi/_guasto_ripieghi.json` *(`9d935528`)* · la stampa
`_corsa.txt` · la **configurazione intera** `_configurazione.txt` *(**zero differenze su 80**
booleani dal driver)* · il simulatore **PRE-CURA** `_sim_precura.py` *(blob `05691d41`, accanto ai
dati come chiede il par.7)*. Il documento: `doc/RIPIEGHI_guasto.md` *(`e8721758`)*.

| | |
|---|---|
| ### ✅ **il CONTROLLO tiene** | un passo da due copie di BASE e' **byte-identico**, `net.rng` compreso → **la prova vale** |
| ### ✅ **il caso che deve fallire FALLISCE** | `psi` CORTA sul pre-cura: **17** grandezze, **12801** nodi, **471564** archi, scost. **`1.256e+01`**. ### **Lo stesso guasto oggi: `SchermaturaSpenta`** |
| ### ⛔ **le due sole PROTETTE** | `psi` e `rho_spin` — **le due curate stamattina**, e ### **solo dal lato CORTA** |

> ### 📌 **IL MECCANISMO, e non e' una lettura:** `:4462` *(la guardia su `psi_spin`)* ### **ESEGUE
> e non spara**, perche' `calcola_psi` riscrive `psi_spin` a piena lunghezza a `:4421`; e
> `_estendi_psi_spinor` **allunga la coda** a `:2264`, disarmando ogni guardia a valle.
> ### ➜ **Una guardia DENTRO una legge arriva troppo tardi o viene aggirata.**

**⚠ E TRE DIFETTI DELLO STRUMENTO, dichiarati nel referto e che NON toccano gli esiti:** le
etichette del braccio pre-cura sono **sbagliate** *(righe del file pre-cura annotate con la tabella
di oggi)*; *«eseguita»* **non** vuol dire *«ramo di scorta preso»* *(registro la guardia, non il
corpo)*; il filtro per **nome** perde gli **alias locali**. **Invalidano la colonna «riga
responsabile», non il verdetto** — che esce dal confronto dello stato.
**E lo strumento NON chiama `dichiara_configurazione`:** `_configurazione.txt` e' un **riparo**.

### 📒 Il registro delle grandezze *(2026-09-29)*

| strumento | blob (byte) | comando che lo rigira **verbatim** | cosa misura |
|---|---|---|---|
| `csv/_test_fork/_registro_grandezze.py` | `5e501255` | `python csv/_test_fork/_registro_grandezze.py --passi=30` | ① **a runtime**: chi e' **per nodo** *(`len == n`)* e chi **per arco** *(`len == m`)* allo stato BASE — **stessa scena e stesso passo della prova a guasto**, cosi' i due elenchi si confrontano · ② **dall'AST**: **tutte** le scritture `self.X = ...` con funzione ed espressione, e la **regola di nascita PROPOSTA** dai soli siti che **allungano** |

**Genera `doc/REGISTRO_grandezze.md`.** ### **E' una SONDA, non un sigillo:** esce sempre con `0`,
il verdetto lo da' il piano.

> ### 📌 **La regola di nascita si PROPONE, non si assegna a macchina**, ed e' la lezione di
> `_classi_ripieghi.py`: **quattro** volte una regola automatica ha **nascosto** cio' che cercava.
> ### **L'espressione e' SEMPRE riportata** — senza quella tabella la colonna della proposta
> sarebbe una cosa da **credere**. E cio' che non e' evidente resta ### **DA DECIDERE**, che decide
> Luca *(`A1`)*.
> ### **Una grandezza senza NESSUNA scrittura che la allunga a un sito di nascita e' un BUCO, non
> una regola** — ed e' la **causa** del ripiego, non il ripiego.

> ### ⛔ **Il primo blob (`5910fde6`) avrebbe scritto «BUCO» FALSI, e l'ho preso verificando il
> registro PRIMA di pubblicarlo.** Usava una **lista di nomi** *(`semina`/`mitosi`/`_allaccia`)*, e
> l'estensione e' **delegata** a `_eredita_psi_figli` e `_eredita_spinore_figli`, che `mitosi` chiama
> a `:6660` e `:6822`. ### **Sarebbe stata la SESTA volta che una mia regola basata sul NOME nasconde
> cio' che cerca.** `5e501255` usa il **grafo delle chiamate** *(38 funzioni raggiungibili dai siti di
> nascita)*, **stampa la CATENA** di ogni voce, e ### **spezza la colonna per EVENTO**: `semina` ·
> `mitosi (+Schwinger)` · `_allaccia`, perche' ### **la semina crea dal VUOTO e la mitosi divide un
> GENITORE — due regole diverse non sono un'incoerenza, sono due eventi.**

**Referto:** `doc/REGISTRO_grandezze.md` *(blob `cfb59fb8`)* · la stampa
`csv/_seal_fork/_guasto_ripieghi/_registro_corsa.txt`.
**Esito:** per nodo **32** *(= le 31 della prova a guasto **+ `phi`**, il metro)* · per arco **11** ·
### **ambigue ZERO** · con regola di nascita **22 + 9** · ### **senza regola 10 + 2** · **DA
DECIDERE 9 + 5** · *«incoerenti»* **3 + 3**.

### 🔬 L'ordine fra la prima lettura e la prima riscrittura *(2026-09-29)*

| strumento | blob (byte) | comando che lo rigira **verbatim** | cosa misura |
|---|---|---|---|
| `csv/_test_fork/_ordine_letture.py` | `97cb0ea3` | `python csv/_test_fork/_ordine_letture.py --da=40 --fino=72` | in un passo **CON NASCITA**, per ogni grandezza del registro: la **prima LETTURA DI LEGGE** e la **prima RISCRITTURA COMPLETA** *(`len == n`)*, ### **in ordine**. Il confine e' l'istante in cui `phi` viene assegnata **piu' lunga** |

> ### 📌 **Perche' esiste, ed e' la correzione del guardiano al mio piano:** il criterio del
> controllo unico **non e'** *«stato o derivata»*. ### **`psi` E' derivata, e ha avuto bisogno di
> ereditare perche' UNA LEGGE LA LEGGEVA fra la mitosi e il ricalcolo** — ed e' li' che nasceva il
> flash. ### ➜ **Il criterio e' l'ORDINE: letta prima ⇒ serve una regola di nascita; riscritta
> prima ⇒ puo' restare corta.**

**Come:** una **sottoclasse dinamica** intercetta `__getattribute__` e `__setattr__` per le sole
grandezze del registro e registra **ordine** e **funzione chiamante**. ### **Nessun byte del
simulatore cambia**, e la classe si rimette com'era a fine misura.

| | |
|---|---|
| ### **il CONTROLLO e' una condizione di validita'** | lo stesso passo **con** e **senza** sorveglianza deve essere ### **byte-identico**. Se non lo e', `vale: false` e si ferma |
| ### **due specie di LETTURA, e separarle e' obbligatorio** | chi **estende** una cache la **legge** per estenderla *(`concatenate([self.eta, …])`)*: ### **quella non e' una lettura di legge, e' parte della riscrittura.** Si separa dalla **funzione chiamante** — se e' raggiungibile dai siti di nascita e' una lettura di **estensione** |
| `phi`, `i`, `j` | sono i **METRI** *(`n = len(phi)`, `m = len(i)`)*: si sorvegliano *(`phi` E' il confine)* ma ### **non sono voci del registro** |

> ### ⛔ **La prima stesura (`3a35664d`) e' GIRATA e il suo verdetto era NULLO** *(fallimento in
> `249ee3c`)*. **Quattro difetti, tutti dall'aver fissato UN SOLO METRO:**
> ① la riscrittura completa cercata come `len == n` **anche per le grandezze per ARCO**, piene a
> `m`: ### **tutte e nove «mai riscritta» per costruzione** · ② il confine era la riga di `phi`, ma
> `mitosi` estende `pos` **un evento prima** (`:6640`), e `pos` risultava *«letta prima»*,
> ### **un artefatto** · ③ la finestra si chiudeva a **fine passo**, e `_xi_rumore` ripiega **al
> passo seguente** · ④ ogni lettura contava come lettura di **legge**, ### **anche quella di
> `verifica_invarianti`, che `_PASSO_TIPI` dichiara «osservatore: LEGGE SOLTANTO»**.
>
> **`97cb0ea3` cura tutti e quattro:** bersaglio **`n` per i nodi e `m` per gli archi** con la
> classe **fissata prima della nascita** · finestra da ### **quando `mitosi` RITORNA** · finestra
> **estesa al passo seguente** · tipo del lettore ### **preso da `_PASSO_TIPI`**, la tabella del
> simulatore. **E non tiene piu' l'elenco degli eventi** *(1,9 milioni per passo)*: registra **solo
> le PRIME occorrenze**.
> ### ⚠ **E un quinto difetto l'ho preso PRIMA di girare:** il bersaglio era fissato **a fine
> passo**, quindi nel passo di nascita **nessuna riscrittura** sarebbe stata registrata. Ora si
> fissa **dentro `mitosi`**, dove la finestra si apre.

### 🔬 La misura dell'ordine, **GIRATA**, e le regole di nascita *(2026-09-29)*

| strumento | blob (byte) | comando che lo rigira **verbatim** | cosa fa |
|---|---|---|---|
| `csv/_test_fork/_ordine_letture.py` | `97cb0ea3` | `python csv/_test_fork/_ordine_letture.py --da=40 --fino=72` | **misura** l'ordine lettura/riscrittura nella finestra della nascita |
| `csv/_test_fork/_referto_ordine.py` | `b0e89744` | `python csv/_test_fork/_referto_ordine.py` | **genera** `doc/ORDINE_letture.md` dalla misura **e** dalla dichiarazione `doc/REGOLE_nascita.tsv`, ### **verificando ogni ancora PER TESTO** e stampando la riga di oggi |

**Referti:** `csv/_seal_fork/_ordine_letture/_ordine_letture.json` *(`cde9dce2`)* · la stampa
`_corsa.txt` · la dichiarazione `doc/REGOLE_nascita.tsv` *(`c45ca427`, **29 regole**)* · il
documento `doc/ORDINE_letture.md` *(`1dca883f`)*.

| | |
|---|---|
| ### ✅ **il CONTROLLO tiene** | lo stesso passo **con** e **senza** sorveglianza e' ### **byte-identico** su **1 887 282** eventi intercettati |
| la nascita | ### **trovata** al passo **42** *(al 41 nessuna)*: `n = 12803`, `m = 471565`, `mitosi` ritorna all'evento **3 774 496** |
| ### **PIENE a fine mitosi** | ### **30 su 40** — ed **e' esattamente l'insieme che HA una regola di nascita**: ### **la regola si vede nella MISURA, non solo nel codice** |
| **CORTE a fine mitosi** | **10** |
| ### ✅ **BUCHI** | ### **ZERO** |

**Delle 10 corte:** **4** nessuna legge le legge · **4** la legge le trova **gia' piene** · **2**
sono **AUTO-RINFRESCHI** *(`_xi_rumore` e `_g_rampa_prec`: la legge le legge corte e **le riscrive
lei stessa** un evento dopo)*, ### **e per entrambe la dichiarazione ESISTE GIA' NEL CODICE**.

> ### ⛔ **E IL SESTO DIFETTO DI `_ordine_letture.py`, dichiarato:** la sua **stampa** etichetta
> *«LETTA PRIMA»* **24** grandezze, e l'etichetta e' **fuorviante** — la finestra si apre quando
> `mitosi` **ritorna**, e a quell'istante **30 su 40 sono GIA' PIENE**. ### **La domanda vera e'
> «una legge le legge CORTE?», e il dato per rispondere e' nella misura stessa** *(ogni evento
> porta la lunghezza vista)*. ### **Percio' la misura VALE e non si rigira: il referto la legge
> bene.** **La stampa si corregge a parte, ed e' in coda:** il blob che ha girato resta `97cb0ea3`.

> ### ⛔ **Il primo giro del SIGILLO ha smascherato DUE difetti dello strumento, non della cura**
> *(2026-09-29, blob `3df06c44` → `dd327a2a`)*
>
> | | |
> |---|---|
> | ### **① `CacheLunga` non era fra i DICHIARATI** | e' **nata dopo** lo strumento, quindi il lato **LUNGA** risultava ### **«ROTTO RUMOROSO»** mentre era ### **PROTETTO**: **23 grandezze su 23 etichettate male**, e ### **il verdetto del criterio `A` sarebbe stato FALSO** |
> | ### **② le grandezze PER ARCO non venivano guastate affatto** | l'elenco cercava **solo** `len == n`: `d` `d0` `peq` `tw` `twp` `vd` `_rep` ### **non comparivano nella tabella**, e il **criterio `D`** *(controllo positivo sugli archi)* ### **non era coperto da nessuna misura** |
>
> **`dd327a2a`** aggiunge `CacheLunga` ai dichiarati, estende l'elenco a `len == m`, ed **esclude
> `i` e `j`** oltre a `phi`: ### **sono i METRI**, e accorciarli non accorcia una cache — **cambia
> il bersaglio**.
> ### 📌 **E il primo giro NON e' buttato: il numero che conta lo ha dato comunque —
> ### RIPIEGO SILENZIOSO da 10 a ZERO.**

### 🔬 Gli STRUMENTI DI MISURA di `DIVISIONE-AUTOCONSISTENTE` e del CALORE *(2026-10-01)*

**Mandato del guardiano, su priorita' di Luca** *(«qua si gioca veramente la dinamica pulita di
tutto»)*. ### **Committati PRIMA di girare**, come chiede il mandato e il par.5.

| strumento | blob (byte) | comando che lo rigira **verbatim** | cosa misura |
|---|---|---|---|
| `csv/_test_fork/_misure_calore.py` | `a9944b1a` | `python csv/_test_fork/_misure_calore.py --passi=72` | **`DIVISIONE-AUTOCONSISTENTE:M0`** *(esiste un'energia totale: le parti misurabili)* · **`DIVISIONE-AUTOCONSISTENTE:M1`** *(quanta `|tw|` sparisce con le divisioni, come frazione)* · **`DIVISIONE-AUTOCONSISTENTE:M3`** *(il termostato Nose-Hoover: serie, clip, pavimenti, e il fattore di `T_target` con la mediana di TUTTI gli archi)* · **`DIVISIONE-AUTOCONSISTENTE:M4`** *(il bilancio di una divisione, col calcio separato dalla cancellazione)* · **`DIVISIONE-AUTOCONSISTENTE:M6`** *(lo scuotimento come sorgente: energia e torsione immesse, e dove)* |
| `csv/_test_fork/_verso_archi.py` | `7c8b0200` | `python csv/_test_fork/_verso_archi.py --passi=1` | **`DIVISIONE-AUTOCONSISTENTE:M2`** *(il verso dell'arco entra nella fisica? Si invertono `(i,j)` per TUTTI gli archi, `tw` cambia segno, e si confrontano le grandezze PER NODO)*. ### **Vale anche per `GEOM-SENZA-VERSO`** |
| `csv/_test_fork/_pos_contro_d.py` | `edb2e305` | `python csv/_test_fork/_pos_contro_d.py --passi=1` | **`DIVISIONE-AUTOCONSISTENTE:M5`** *(quali leggi leggono `pos` e quali solo `d`: la posizione del figlio e' FISICA o solo DISEGNO?)*, in **due modi** — **statica** dall'AST col grafo delle chiamate, e **a runtime** per intercettazione |
| `csv/_test_fork/_regime_due_sistemi.py` | `211b0b46` | `python csv/_test_fork/_regime_due_sistemi.py --passi=72` | **`REGIME-DUE-SISTEMI`**: di quanto differiscono i **due sistemi** che si chiamano **entrambi** *«regime deterministico»* -- quello **del modulo** *(il sistema di riferimento, `SCUOTIMENTO = True`)* e quello **con `--regime`** *(`SCUOTIMENTO = False`)*. Confronto ### **passo per passo**, grandezze **e contatori**. ### ⚠ **Non decide la cura:** dice solo se la via *«allineare `_applica_regime` al modulo»* ### **butterebbe via un sistema che qualcuno ha misurato** *(il braccio `O2` di `_sigillo_osservatore.py`)* |
| `csv/_test_fork/_carica_e_coppie.py` | `1ce1cac8` | `python csv/_test_fork/_carica_e_coppie.py --seme=11 --passi=72` | **`DIVISIONE-AUTOCONSISTENTE:G1`** *(la carica: la serie di `sum(perc_chi)`, e ### **se il segno dipende da una SCELTA DI GAUGE** — il rappresentante canonico)* · **`:G2`** *(`D35`: con `phi` su `4π` l'antinodo e' **identico** al genitore per il campo?)* · **`:G3`** *(`COPPIA_DENSITA`: `peq` entra nella creazione di coppie?)* · **`:G4`** *(quanti nodi crea un evento, e come cambia la carica totale)* · ### **`:E-base`** *(la LINEA DI BASE dei criteri del par. `(E)` del piano: `K_fase` ed `E_cin` su un run lungo, col volume)*. ⚠ **Si gira TRE volte**: `--seme=11 --passi=72`, `--seme=12 --passi=72`, `--seme=11 --passi=150` |

> ### ⭐ **LA TECNICA DI MISURA NUOVA, e non era prevista: LE VOCI DELLO SCHEDULATORE**
> `_misure_calore.py` mette una **spia** su `_ferma_se_registro_incoerente`, che il **commit 1**
> chiama ### **dopo OGNI voce** *(generalizzazione 2 di Luca)*. ### ➜ **Ogni confine di voce
> diventa un punto di misura**, e la variazione di una grandezza si puo' ### **ATTRIBUIRE ALLA
> VOCE** invece di essere letta a fine passo come un totale indistinto.
> ### **Il presidio del commit 1 e' diventato l'imbragatura di misura di questo lavoro**, e questo
> non era uno scopo: e' un effetto. *(Un presidio che serve anche a misurare costa meno di due.)*

> ### ⛔ **E I NOMI DELLE MISURE STANNO NEL NAMESPACE DELLA VOCE, perche' `M2` E' GIA' PRESO**
> Il mandato le chiama `M0`…`M6`. ### **Ma nell'indice `M1`, `M2`, `M3`, `M4` ESISTONO GIA'**, e
> ### **`M2` e' «LA MITOSI — DUE DIFETTI DA ACCLARARE: ① il figlio nasce nel PUNTO MEDIO»**, cioe'
> ### **lo STESSO argomento.** ### ➜ **La forma nuda avrebbe risolto al difetto sbagliato**, ed e'
> la famiglia della collisione `P3`/`P5` che il prefisso `H-` ha curato.
> ### **Quindi: `DIVISIONE-AUTOCONSISTENTE:M0` … `:M6`.** La forma corta resta **dentro i tre
> file e nei loro `json`**, dove e' **locale** e il par.9 la consente — ### **mai in un documento
> vivo, mai in un messaggio di commit.**
> *(E l'ha trovata `H-INDICE`, rifiutando il commit: non la mia attenzione.)*

> ### ⚠ **CHE COSA QUESTI STRUMENTI NON FANNO, dichiarato prima dei numeri**
> ### **Non chiamano <<energia>> cio' che non lo e'.** `K_fase` e' una cinetica vera *(`M_PH = 1`
> uniforme)*, `K_metr` lo e' **con massa d'arco posta a 1 e DICHIARATA**, e `Q2` e' un ### **proxy
> dichiarato**, non un potenziale — perche' la forza metrica e' `cs^2 (M − I) q`, **non** `−k q`.
> ### **Un bilancio su una grandezza che non si conserva nemmeno in principio non e' un bilancio:
> e' una somma.** Il perche' sta in `DIVISIONE-AUTOCONSISTENTE:M0`.

### 🔬 Il SIGILLO del COMMIT 2 del riordino *(2026-10-01)*

| strumento | blob (byte) | comando che lo rigira **verbatim** | cosa misura |
|---|---|---|---|
| `csv/_seal_fork/_sig_decisione_separata.py` | `06209df4` | `python csv/_seal_fork/_sig_decisione_separata.py --passi=72` | **`A`** *(### **byte-identico fino al 72**, grandezze **e contatori**, contro il blob di prima)* · **`B`** *(### **il caso che deve fallire**: un arco portato **sopra la sua soglia locale** deve entrare nell'insieme che `decidi_divisione` **DICHIARA**)* · **`C`** *(### **MISURA, non prova**: quanto vale la **soglia** dove avvengono le divisioni)* |

> ### ➕ **E PORTA UN PRESIDIO CHE IERI MANCAVA:** controlla che il blob *«di prima»*
> ### **NON contenga l'ancora della cura** — ed e' il difetto `SIM-PRIMA-STANTIO`, trovato oggi
> su un artefatto committato. ### **Da reperto a presidio nello stesso giorno.**

> ### ⚠ **PERCHE' `B` NON MUOVE LA SOGLIA, come il piano chiedeva:** la soglia ### **non ha un
> handle esterno** *(nasce da `PHI_CRIT + π` modulata dal gradiente, e toccare `PHI_CRIT` cambia
> **tutto** il criterio)*. ### **Si porta L'ARCO sopra la SUA soglia locale**, che la decisione
> dichiara nel `perche'`: ### **stesso effetto misurato, nessuna costante di fisica toccata.**

### 🔬 Il SIGILLO del controllo unico *(2026-09-29)*

| strumento | blob (byte) | comando che lo rigira **verbatim** | cosa fa |
|---|---|---|---|
| `csv/_seal_fork/_sig_controllo_unico.py` | `e915cbad` | `python csv/_seal_fork/_sig_controllo_unico.py --passi=72` | i bracci **`B`** *(byte-identico fino al 72 contro il blob PRE-CONTROLLO)*, **`C`** *(il caso che deve fallire: col controllo SPENTO i guasti tornano scoperti)* ed **`E`** *(un run sano CON NASCITE arriva al 72 senza un solo errore del registro)*, piu' il **riepilogo** che cita `A` e `D` dal referto committato di `_guasto_ripieghi.py` |

**I cinque criteri sono di Luca e sono fissati PRIMA del codice** *(piano `f684353f`, par.5)*.

> ### ➕ **BRACCIO `G`, aggiunto col COMMIT 1 del riordino** *(2026-10-01)*: ### **i TRE casi che
> devono fallire** — `pippo` *(per **nodo**)*, `pluto` *(per **arco**)* e ### **la finestra
> `_smp_d0` lasciata aperta.**
> **Perche' il terzo esiste:** la **prova a guasto NON lo raggiunge**, perche' inietta **fra i
> passi** e `_smp_d0` ### **fra i passi non esiste** — vive **solo dentro** il passo.
> ### **Il solo modo di provarla e' questo braccio.**

> ### 📌 **Due scelte di misura, dichiarate prima dei numeri:**
> **①** `B` confronta ### **PASSO PER PASSO**, non solo alla fine — ### **il primo passo in cui
> qualcosa cambia E' l'informazione**, e una somma finale la nasconderebbe *(e' il braccio `E` di
> `PSI-FLASH` che ho sbagliato una volta, sommando su domini diversi)*.
> **②** il blob **PRE-CONTROLLO** non e' un hash scelto a mano: e' ### **il PADRE del commit che
> introduce `_ferma_se_registro_incoerente`**, ricavato da `git log -S`, ed e' estratto con
> **`git cat-file -p` IN BINARIO** *(par.7: **non** `git checkout`, per la trappola CRLF)*.

> ### ⛔ **`H-P8` ha RIFIUTATO la prima stesura, e aveva ragione.** Estraeva il blob pre-controllo
> con `git cat-file -p <introduce>^:...` **fatto a mano**. ### **`_cli_flag.sim_prima_del_flag` fa
> la stessa cosa ancorando al PADRE del commit che introduce l'ancora**, ed e' la funzione che il
> presidio riconosce: ### **meno codice, e un presidio in piu' invece di uno aggirato.**
> *(Il difetto che `H-P8` esiste per impedire e' `ANCORE-1`: **25 sigilli** che prendevano «il
> codice di prima» da `HEAD` e ### **diventavano VUOTI appena la cura era committata**.)*
> **E nello stesso giro ho aggiunto `dichiara_configurazione` (`P5`)** — l'omissione che avevo
> dichiarato per `_guasto_ripieghi.py`, ### **e qui non la ripeto.**

**ESITO, dal referto `_sig_controllo_unico.json`** *(un SOLO run, 2026-10-01, blob del
simulatore `5d29334b`)*: ### **IL SIGILLO PASSA, tutti e SETTE i bracci.**

| braccio | numeri |
|---|---|
| **`A`** | **30 su 30** di STATO a posto, mancano **NESSUNA** |
| **`D`** | **7** per arco, non a posto **NESSUNA** |
| ### **`B`** | **72** passi, ### **0** passi con differenze contro `f7541d03` — ### **179 contatori confrontati** |
| ### **`C`** | protette a controllo **SPENTO**: ### **0** *(chiamate spente contate: 270)* |
| **`E`** | `n` da **12802** a **12812** *(### **10 nati**)*, controlli **648**, assenze contate **42** |
| **`F`** | **30 su 30** viste piene, mai apparse: **NESSUNA** |
| ### **`G`** | `pippo` ### **FERMA con GrandezzaNonDichiarata** · `pluto` ### **FERMA con GrandezzaNonDichiarata** · finestra ### **FERMA con FinestraRestataAperta** |
| **ripiego silenzioso residuo** | ### **NESSUNO** |

> ### ⛔ **E LA VOCE DI PRIMA PORTAVA UN NUMERO STANTIO, che questo run ha scoperto**
> Diceva *«`B`: 72 passi, **0** passi con differenze»* accanto al blob `a13a385c`, ### **che
> CONTIENE la clausola dei `set`** di `_contatori` *(entrata il 2026-09-29 alle 15:07 con
> `bd7c4ae`, mentre `_g_registro_apparse` esisteva dalle 14:28 con `4036ad9`)*. ### **Ma il blob
> PRE-CONTROLLO non puo' avere `_g_registro_apparse`: non ha il registro.** Quindi un run di `B`
> su quel blob del sigillo ### **avrebbe segnalato la differenza, PER COSTRUZIONE** — e dunque
> ### **il numero e il blob di quella voce non venivano dallo stesso run.**
> ### ➜ **`L-NUMERI`: un numero ricopiato non ha provenienza, uno generato ce l'ha.** Questa
> tabella e' **generata dal `json`**, non ricopiata.

> ### ✅ **IL RESIDUO `_sin2_vir` E' CHIUSO, e questa nota era SCADUTA** *(corretta il 2026-10-01)*
> **Diceva:** *«l'unico ripiego silenzioso che resta ... va nel commit delle guardie, separato»*.
> ### **Quel commit c'e' stato** *(`0053aca`: la condizione fusa SEPARATA — `None` legittimo e
> **contato**, lunghezza sbagliata che **spara**)*, e ### **il referto di oggi dice `ripiego
> silenzioso residuo: NESSUNO`.**
> ### ⚠ **E la nota e' rimasta li' a dire il falso fino a che un numero GENERATO non l'ha
> smentita** — che e' la stessa famiglia del commento di `MITOSI_DIR` e di quelli sul REGIME:
> ### **una frase scritta quando era vera, e mai piu' riletta.**

> ### 📌 **BRACCIO `F` aggiunto il 2026-09-29** *(punto 2 di Luca)*: **il RENDICONTO della
> tolleranza.** Elenca le grandezze di **STATO** che **non si sono MAI viste piene**, leggendole
> ### **dalla rete del braccio `E`** — cosi' il rendiconto parla del **run appena fatto** e non di
> un altro. ### **Se anche UNA sola non e' mai apparsa, `F` FALLISCE**: o non esiste in questa
> configurazione *(e va dichiarata DERIVATA col suo motivo misurato)*, o qualcosa non la crea mai
> *(e allora il registro dice il falso)*. ### **In entrambi i casi resterebbe fuori dal controllo in
> silenzio, ed e' il varco che il punto 2 chiude.**

| strumento | blob (byte) | comando | cosa fa |
|---|---|---|---|
| `csv/_test_fork/_gen_potatura.py` | `2b9b584d` | `python csv/_test_fork/_gen_potatura.py` | **genera** `doc/POTATURA_guardie.md` dalla tabella `doc/RIPIEGHI_classi.md`: i **57** rami morti, **12 fusi** e **45 di sola lunghezza**, in **13** funzioni. ### **La lista non e' scritta a mano e i numeri di riga si RIGENERANO** |

> ### 📌 **Il braccio `B` confronta ora ANCHE I CONTATORI** *(decisione di Luca, 2026-09-29)*: ogni
> attributo **intero** *(o tupla di interi, come le `_..._shape`)* che comincia con `_`.
> ### **Un contatore che cambia di UNO e' un difetto, e le 23 grandezze NON lo vedrebbero** — lo
> stato puo' restare identico mentre il **percorso** e' cambiato. **E l'ancora si da' dal CLI**
> *(`--ancora=registro_mai_apparse` da' esattamente il blob **`fc9ef41c`**, verificato)*.

> ### ⛔ **DUE DIFETTI DEL SIGILLO, presi dal suo stesso giro** *(2026-09-29)*
>
> | | |
> |---|---|
> | ### **① il referto di `A`/`D` era accettato SENZA verificare su quale BLOB era stato prodotto** | ### **E' capitato davvero**: il referto della prova a guasto era di **PRIMA** della cura di `_sin2_vir`, e il sigillo riportava un residuo ### **che quella cura aveva gia' chiuso**. ### **Un sigillo che legge un referto STANTIO non e' un sigillo: e' una CITAZIONE.** Ora confronta `blob_sim_sha1_byte` col blob di oggi e ### **si rifiuta di leggerlo** |
> | ### **② il RESIDUO non entrava nel verdetto** | era stampato come **nota**. Ma il criterio di Luca per il pezzo delle guardie e' ### **«zero ripieghi silenziosi, `_sin2_vir` COMPRESA»**: quindi il residuo ### **fa FALLIRE `A`**, non lo commenta |
>
> *(E il messaggio finale diceva «tutti e cinque i bracci» quando erano **sei**: ora il numero si
> conta.)*

| strumento | blob (byte) | comando | cosa misura |
|---|---|---|---|
| `csv/_test_fork/_sonda_buco_tipo.py` | `a114c92f` | `python csv/_test_fork/_sonda_buco_tipo.py` | trasforma in **lista** sei grandezze **tipate** *(forma giusta, nessun `dtype`)* e dice se il controllo le **salta**, le **rompe** o le **protegge** |

**Referti:** `csv/_seal_fork/_sig_tipo_buco/_prima_della_correzione.txt` *(prodotto dalla sonda
`c0d0fe1c`, che asseriva la conclusione)* e `_dopo_la_correzione.txt` *(sonda `a114c92f`, che la
### **DERIVA dai risultati**)*.
**Esito: PRIMA `psi` ed `eta` SALTATE IN SILENZIO, `phi0` e `perc_chi` rotte, `pos` e `_psi_spinor`
gia' protette; DOPO ### SEI SU SEI PROTETTE, zero silenziose e zero rumorose.**

> ### 📌 **E la sonda e' stata CORRETTA nello stesso giro, perche' la sua conclusione era
> ASSERITA:** stampava *«il tipo non viene guardato»*, una frase ### **vera prima della cura e FALSA
> dopo**. Ora ### **il conto si DERIVA dai risultati**. *(Il file `_prima` porta la conclusione
> vecchia, che era accurata quando e' stato prodotto: il blob della sonda e' scritto qui accanto.)*

### 🧪 La sonda del VELENO *(2026-10-01)*

| strumento | blob (byte) | comando | cosa misura |
|---|---|---|---|
| `csv/_test_fork/_sonda_veleno.py` | `20edc5b5` | `python csv/_test_fork/_sonda_veleno.py --passi=3` | la **terza via** per le derivate sporche: ① il **costo** del controllo di finitezza alle dimensioni vere · ② quante derivate sono **intere** *(dove `NaN` non esiste)* · ③ l'interazione con **`np.seterr(invalid='raise')`** · ### **④ il censimento dei non finiti su un run SANO**, che non era nel mandato |

**Referto:** `csv/_seal_fork/_sonda_veleno/_referto.txt`.
**Esito:** controllo di finitezza su 30 voci **`0.002085 s`** contro un passo da **`2.849 s`** ⇒
### **lo `0.073 %`** *(con 9 controlli per passo, lo `0.659 %`)* · derivate **intere: ZERO** *(tutte
e 10 `float64`)* · il `NaN` ### **PROPAGA** in somma, prodotto, confronto, `isfinite` e `sum`, e
solleva **solo** su `astype(int64)` e `inf - inf` · ### **e UNA grandezza di STATO ha GIA' non finiti
su un run sano: `eta`, `inf` su tutti i 12802** — legittimo e dichiarato.

> ### 📌 **La quarta misura RAFFINA la proposta, ed e' per questo che l'ho fatta:** un controllo
> **globale** di finitezza ### **sparerebbe al primo passo**, e il veleno **non si distinguerebbe da
> cio' che e' legittimo. ➜ Il controllo va fatto PER GRANDEZZA, con l'esenzione DICHIARATA** — lo
> stesso schema gia' in piedi per il **tipo**.
> ### ✅ **E il sistema usa GIA' il veleno:** `peq` nasce **`NaN`** a `:3693` *(«da calibrare»)* e a
> `:7165`, e `step` la **calibra**. ### **«Derivata sporca» e «`peq` da calibrare» sono la STESSA
> COSA**, e per `9-ter` questo conta: la generalizzazione 4 ### **da' un nome a cio' che il sistema
> fa gia' in due punti.**
