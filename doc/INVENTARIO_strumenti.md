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

*(La tabella segue nei commit successivi, a blocchi, una campagna alla volta.)*

