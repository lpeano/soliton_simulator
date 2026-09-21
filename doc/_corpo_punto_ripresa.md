# ⚠⚠ PUNTO DI RIPRESA — **si legge PER PRIMO dopo un riavvio**

> **Aggiornato @@ORA@@ · HEAD `@@HEAD@@` · branch `fork-su2`, tutto committato e pushato.**
> **Il PC si riavvia fra mezzanotte e le due** *(vincolo di Luca, 2026-09-21)*. **Questo blocco e'
> RIGENERATO per intero a ogni aggiornamento**, fra due marcatori HTML: non si accumulano versioni
> e non c'e' niente da cancellare a mano.

## COSA E' FATTO — **e come verificarlo senza fidarsi di questa riga**
| | stato | la prova, sul disco |
|---|---|---|
| **diagnosi dei picchi** | ✅ passo **1126**, arco **`3352-506`**, `peq = -4.85e-04` | `csv/_test_fork/_diag_D/PEQ_DENTRO_001126.txt` · `Z93`, `Z94` |
| **`C1 PEQ_ESATTO`** | ✅ **sigillo `7/7`** | `csv/_seal_fork/_sigillo_peq_esatto_2026-09-21.txt` · `Z95` |
| **`C2 PEQ_NASCITA_LOCALE`** | ✅ **sigillo `6/6`** | `csv/_seal_fork/_sigillo_peq_nascita_2026-09-21.txt` · `Z96` |
| **assioma `A11`** | ✅ scritto, coi sette corollari | `doc/ASSIOMI.md` · `CLAUDE.md` `P1-quinquies` |
| **`C3 SCALA_MIN_PASSO`** | ✅ **sigillo `6/6`** | `csv/_seal_fork/_sigillo_scala_min_passo_2026-09-21.txt` · `Z97` |
| **`C4 COES_CAUSALE`** | ⏳ **IN CORSO — e' il prossimo** | — |
| **`C1-bis ANOM_SIMM`** | ⏸ **dopo `C4`, prima di `C5`** *(deciso da Luca il 21/9)* | derivazione in `csv/_deriva_anom_simm.py` |
| `C5 INVARIANTI` | ⏸ | mandato `C5` |
| **validazione 600 passi** | ⏸ **CHECKPOINT 2: ci si FERMA** | — |

## COME SI RIPARTE — **i comandi esatti, verbatim**

**① VERIFICARE CHE NON SI SIA PERSO NULLA** *(sempre, prima di tutto)*
```
cd C:\\Users\\lpeano\\soliton_simulator
git status --short
git log --oneline -5
python csv/_presidio.py
```

**② RIGIRARE I SIGILLI GIA' PASSATI** *(devono ridare gli stessi numeri: se no, qualcosa e' cambiato)*
```
python csv/_seal_fork/_sigillo_traccia_peq.py
python csv/_seal_fork/_sigillo_peq_esatto.py
python csv/_seal_fork/_sigillo_peq_nascita.py
```

**③ RIFARE LA MISURA DEI TRE NUMERI** *(due minuti: NON integra il passo esplosivo)*
```
python csv/_test_fork/_peq_dentro_1126.py --da=1080 --fino=1126
```

**④ LA VALIDAZIONE, QUANDO SI ARRIVERA' — e va lanciata COSI', con l'archivio a SERIE**
**⚠ Senza `--serie` NON E' RIPRENDIBILE**, e un riavvio la farebbe ricominciare da zero.
```
python csv/_test_fork/_scena_video.py 600 csv/_test_fork/_val600 --sep=4.0 --serie=20 ^
  --csv-progresso=csv/_test_fork/_val600/prog.csv ^
  --chi-basc=on --chi-coop=on --scala-min=on --coes-adim=on
```
**⚠ LE OPZIONI DELLE CURE NON SONO ANCORA CABLATE NEL DRIVER** *(`C1`-`C4` hanno i flag nel
simulatore ma il driver non li inoltra)*: **prima della validazione va fatto, e il sigillo dei flag
del driver lo verifica da solo** — `python csv/_seal_fork/_sigillo_flag_driver.py`.

**⑤ SE LA VALIDAZIONE ERA IN CORSO AL RIAVVIO — si RIPRENDE, non si rilancia**
```
python soliton_simulator.py --db-rigioca <ULTIMO_SNAPSHOT> 600 ...   (stessi flag)
```
**L'ultimo snapshot si legge dal disco:**
```
ls csv/_test_fork/_val600/scena_*.pkl.gz
```
**e `doc/STATO_RUN.md` porta la voce del run col COMANDO VERBATIM** *(par.5-octies)*.

## ⚠ COSA NON SI DEVE FARE AL RIAVVIO
- **NON usare `--db-cleanup`**: **CANCELLA il `.pkl`**. L'archivio del ramo D *(10 snapshot,
  ~370 MB, irriproducibili senza rigirare 1200 passi)* non si tocca.
- **NON rigirare il ramo D vecchio** per confronto: e' **EPOCA 2**, le cure lo hanno cambiato.
- **NON fidarsi di questa tabella:** ogni riga porta il file che la prova. **Si guarda quello.**
