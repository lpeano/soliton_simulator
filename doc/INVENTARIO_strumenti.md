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
| **analisi** | `csv/_test_fork/_struttura_video.py` (`6bb24e5e`) |

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
| **analisi** | `csv/_test_fork/_ab_due_tre.py` (`0889bcef`) e `csv/_test_fork/_struttura_video.py` (`16773e2f`) |

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
