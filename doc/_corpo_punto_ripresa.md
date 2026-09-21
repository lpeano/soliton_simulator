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
| **`C4 COES_CAUSALE`** | ✅ **sigillo `5/5`** | `csv/_seal_fork/_sigillo_coes_causale_2026-09-21.txt` · `Z98` |
| **`C1-bis ANOM_SIMM`** | ✅ **sigillo `6/6`** | `csv/_seal_fork/_sigillo_anom_simm_2026-09-21.txt` · `Z99` |
| **`C5 INVARIANTI`** | ✅ **sigillo `3/3`** | `csv/_seal_fork/_sigillo_invarianti_2026-09-21.txt` · `Z100` |
| **il DRIVER inoltra le cure** | ✅ **sigillo dei flag `3/3`**, 9 opzioni su 9 in entrambi i versi | `csv/_seal_fork/_sigillo_flag_driver.py` |
| **strumento delle LETTURE** | ✅ criteri fissati PRIMA, tabella generata da codice | `csv/_test_fork/_letture_validazione.py` |
| **validazione 600 passi** | ✅ **FINITA**: 6 criteri su 8 REGGONO. `nsub` max = **4**, `peq >= 0`, zero sotto `LAM`, zero violazioni. **NON reggono `d0` (esponenziale, x1.232 per snapshot) e `d/d0` (0.69-0.84 = COMPRESSIONE)** | `csv/_test_fork/_val600/LETTURE.txt` · `Z101` |
| **CHECKPOINT 2** | ⚠ **RAGGIUNTO: si aspetta LUCA. IL RUN LUNGO NON SI LANCIA** | — |
| **il prossimo giro** | ⏸ **la fuga di `d0`: `S09`/`S10`** *(auto-amplificanti, mai misurati PER SITO)* | `Z101`, e il mandato globale §6 li aveva esclusi da questo giro |

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

**④ LA VALIDAZIONE — il comando ESATTO, e il driver ORA inoltra le cure** *(sigillo `3/3`)*
**⚠ Senza `--serie` NON E' RIPRENDIBILE**, e un riavvio la farebbe ricominciare da zero.
```
python csv/_test_fork/_scena_video.py 100 csv/_test_fork/_val600 --sep=4.0 --serie=20 --chi-basc=on --chi-coop=on --scala-min=off --coes-adim=on --peq-esatto=on --peq-nascita-locale=on --scala-min-passo=on --coes-causale=on --anom-simm=on --invarianti=on --csv-progresso=csv/_test_fork/_val600/prog.csv
```
**`100` frame x `6` passi = `600` passi.** **`--scala-min=off` perche' `SCALA_MIN_PASSO` lo
SOSTITUISCE** *(precedenza dichiarata: col nuovo acceso, il freno per-scrittura diventa passante)*.
**Le letture si generano poi con:**
```
python csv/_test_fork/_letture_validazione.py --dir=csv/_test_fork/_val600
```

**⑤ SE LA VALIDAZIONE ERA IN CORSO AL RIAVVIO — si RIPRENDE, non si rilancia**
**⚠ IL DRIVER HA `--riprendi`, ED E' LA VIA GIUSTA: stesso comando del punto ④ PIU' `--riprendi`.**
Senza quel flag, una cartella non vuota viene **RIFIUTATA** *(ed e' giusto: la ripresa e' una
scelta esplicita, mai un ripiego automatico)*.
```
python csv/_test_fork/_scena_video.py 100 csv/_test_fork/_val600 --sep=4.0 --serie=20 --riprendi --chi-basc=on --chi-coop=on --scala-min=off --coes-adim=on --peq-esatto=on --peq-nascita-locale=on --scala-min-passo=on --coes-causale=on --anom-simm=on --invarianti=on --csv-progresso=csv/_test_fork/_val600/prog.csv
```
**Per vedere a che punto era:**
```
ls csv/_test_fork/_val600/scena_*.pkl.gz
tail -5 csv/_test_fork/_val600/prog.csv
tail -3 csv/_test_fork/_val600/log.txt
```

**⑤-bis LA VIA ALTERNATIVA, dal simulatore invece che dal driver**
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
