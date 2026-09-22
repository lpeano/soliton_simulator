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
| **BLOB del driver** | **`9aee4fc2`** *(`csv/_test_fork/_scena_video.py`, con `--chi-basc=on\|off`)* — **⚠ SUPERATO il 2026-09-21: il driver e' ora `4d31ddee`**, con `--chi-coop=on\|off` (default `off`). **I due run A/B qui sotto restano riproducibili VERBATIM**: a default l'argv e' identico elemento per elemento, e lo prova `csv/_seal_fork/_sigillo_chicoop_driver.py`, non questa nota. |
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
| `csv/_test_fork/_g4_prova.py` | `b9642633` | `--controllo` *(120 passi)*, poi `--riferimento` e `--spegni` *(600 passi)* | **`G4`: la prova di spegnimento della MEMORIA DEL MOTO, col BILANCIO COMPLETO di `d0`.** Oltre agli scrittori di `Z102`, misura **il FRENO** *(avvolge `_smorza`, e conta solo `d0_passo`: le altre chiamate stanno dentro siti gia' tracciati e si conterebbero due volte)*, **le NASCITE** e **le MORTI** *(fotografia delle CHIAVI `(i,j)` a inizio e fine passo)*. **CRITERIO scritto PRIMA: `Δ(somma d0) = scritture + freno + nascite - morti`, entro `1e-9` relativo alla SCALA dei termini** *(non al `Δ`, che puo' essere ~0 per cancellazione)*. **Se non chiude, la prova non si legge.** Cinque collaudi, **quattro dei quali DEVONO fallire**. **NON tocca simulatore ne' driver.** | `csv/_test_fork/_g4_*/BILANCIO_d0.txt` · `.csv` |
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
