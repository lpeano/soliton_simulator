<!-- PUNTO-DI-RIPRESA:INIZIO -->
# ⚠⚠ PUNTO DI RIPRESA — **si legge PER PRIMO dopo un riavvio**

> **Aggiornato 2026-09-21 20:34 · HEAD `3fcc148` · branch `fork-su2`, tutto committato e pushato.**
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
| **`C5 INVARIANTI`** | ⏳ **IN CORSO -- e' il prossimo** | mandato `C5` |
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
<!-- PUNTO-DI-RIPRESA:FINE -->

> ## ⚠ DAL TAG `epoca-2`: **SISTEMA D**
> **Nuova carica (dallo spinore), scala minima `LAM` su `d` e `d0`, coesione adimensionale e causale** — piu' la **cura del mondo-dopo-i-flag**, che cambia ogni run.
> **Ogni numero misurato PRIMA appartiene all'EPOCA 1 e NON si confronta con l'epoca 2.**
> `EPOCA 2 = blob del simulatore del tag (`4954fe5b`, byte grezzi) + configurazione con `CHI_COOP`, `SCALA_MIN`, `COES_ADIM` ACCESI`. **Un run a flag spenti su quel blob e' ancora EPOCA 1**, e non e' un'opinione: lo provano `Z1` e `Z1c`, byte-identici.

> ### ⚠ CORREZIONE DEL 2026-09-21 — **la frase qui sopra e' IMPRECISA, e la lascio leggibile**
> **Cio' che avevo scritto:** *«un run a flag spenti su quel blob e' ancora EPOCA 1, lo provano `Z1`
> e `Z1c`».* **VALE SOLO CON L'ARGV NUDO.**
> **Perche' e' sbagliata:** `Z1c` confronta contro **«PRIMA + la cura del mondo»**, non contro
> **«PRIMA»** — la cura e' innestata su ENTRAMBI i bracci di proposito, senno' il sigillo misurerebbe
> LEI invece dei tre flag. **Quindi `Z1c` NON dice nulla sull'equivalenza con l'epoca 1.** A dirlo e'
> `Z1b`, che misura la differenza: **`n` 2569 -> 2580, archi 527 308 -> 526 202.** La cura e'
> **categoria D** e fa finalmente agire gli **otto** flag sul vuoto.
>
> **LA CLASSIFICAZIONE CORRETTA, in quattro righe:**
> ```
> EPOCA 1       blob PRECEDENTE al tag, qualunque configurazione
>
> EPOCA 1       blob del tag, argv NUDO, tre flag spenti
>               -> byte-identico, lo prova Z1
>
> EPOCA 1-bis   blob del tag, argv del FORK, tre flag spenti
>               -> NON e' epoca 1: e' epoca 1 CON LA CURA DEL MONDO.
>                  Il vuoto nasce coi flag del run invece che coi default. Lo misura Z1b.
>
> EPOCA 2       blob del tag + CHI_COOP, SCALA_MIN, COES_ADIM ACCESI
> ```
>
> **⚠ LA CONSEGUENZA PRATICA, ed e' operativa:** **i run del FORK di epoca 1 NON si riproducono sul
> blob nuovo, nemmeno a flag spenti** — **e NON E' UN DIFETTO.** Chi vuole rigirarli deve usare il
> **blob PRECEDENTE** (`git cat-file -p <commit>:soliton_simulator.py`, scritto in BINARIO).
>
> **Il tag NON si sposta e NON si riscrive:** un tag pubblicato che cambia sotto i piedi e' peggio
> dell'imprecisione. La correzione vive qui e in una `git notes` sul commit del tag.



---

## ⓪ LE CANCELLAZIONI DEL 2026-09-21 — **l'elenco completo, prima di spostare qualunque cosa**

**Criterio applicato:** nessun file tracciato da git; scratch ricreato dagli script stessi.
**Verificato DOPO:** `git status` non segnala **nessun** file tracciato mancante.

### Dentro il repository — **611 MB**, scratch di sigilli
| cartella | MB | chi la ricrea | verdetto salvato? |
|---|---|---|---|
| `csv/_seal_fork/_sig_sep` | 180 | `_sigillo_sep_driver.py` | `_sigillo_sep_driver.txt` |
| `csv/_seal_fork/_sig_chibasc` | 167 | `_sigillo_chibasc_driver.py` | `_sigillo_chibasc_driver.txt` |
| `csv/_seal_fork/_sig_ramo_D` | 131 | `_sigillo_ramo_D.py` | `_sigillo_ramo_D_2026-09-21_*.txt` |
| `csv/_seal_fork/_sig_chicoop` | 50 | `_sigillo_chicoop.py` | ⚠ **NESSUNO** — vedi sotto |
| `csv/_seal_fork/_sig_traccia_d0` | 50 | `_sigillo_traccia_d0.py` | ⚠ **NESSUNO** — vedi sotto |
| `csv/_seal_fork/_sig_z1c` | 34 | `_sigillo_Z1c.py` | `_sigillo_Z1c_2026-09-21.txt` |

**Piu' due copie del driver, MAI tracciate e rigenerate a ogni giro del sigillo:**
`csv/_test_fork/_driver_prima_chibasc.py` · `csv/_test_fork/_driver_prima_sep.py`.

### ⚠ UN ERRORE, e il file e' stato RIPRISTINATO
`csv/_seal_fork/_sig_traccia_d0/` conteneva **`_sim_prima.py`, che ERA TRACCIATO** — ed e' una
**copia del simulatore**, cioe' esattamente cio' che il par.5-quinquies impone di conservare.
**Ripristinato** con `git cat-file -p HEAD:` scritto in **binario** *(mai `git checkout`: trappola
CRLF)*, `sha1` byte grezzi **`01146a16`**.
**Perche' e' sfuggito:** il mio censimento contava i file tracciati **solo** per le cartelle sopra
i 40 MB della tabella; per gli scratch dei sigilli mi sono fidato della **regola generale**
*(«sono usa-e-getta»)* invece di ricontrollare cartella per cartella. **La regola era giusta per
sei cartelle su sette.**

### ⚠ DUE SIGILLI SENZA OUTPUT COMMITTATO, ed e' un debito aperto
`_sigillo_chicoop` (**8/8**) e `_sigillo_traccia_d0` (**4/4**): il par.5 dice *«committa gli output
col verdetto»* e **non l'ho fatto** — i numeri vivono solo nei messaggi di commit. **Lo scratch non
li conteneva** (sono `.npz`, non stdout), quindi cancellarlo non ha perso nulla: **i due sigilli
vanno RIGIRATI e i loro output committati.**

### Fuori dal repository — **1.2 GB**
| percorso | MB | cosa era |
|---|---|---|
| `%TEMP%/claude/c--Users-lpeano-soliton-simulator/b8f19b37-.../` | 1100 | scratchpad di una **sessione morta**, file piu' recente del **2026-09-19** |
| `%TEMP%/claude/bash-edit-diff` | 106 | cache temporanea dell'editor |

**Verificato prima di cancellare:** l'unico processo `python` vivo era il ramo D — **nessuna
sessione parallela**.

### ⚠ E IL CONSUMATORE VERO NON ERA NESSUNO DI QUESTI
Il disco continuava a scendere anche dopo le pulizie. **E' il PAGEFILE**, cresciuto da **18.7 a
19.7 GB** sotto i run pesanti. **E' gestito da Windows e non lo tocco**, ma spiega i cali che
attribuivo al repo.

### Cosa NON e' stato cancellato, e perche'
| cartella | MB | motivo |
|---|---|---|
| `_ab_grav_ampiezza` · `_ab_coppia_reciproca` | 506 + 506 | **NON in `INVENTARIO`**: senza il comando documentato sono **gia' irrecuperabili**. Cancellarle perderebbe cio' che nessuno puo' rifare |
| `_g6000` | 1314 | in inventario, rigenerabile — ma **ore di CPU** |
| `_ab_A` · `_ab_B` | 923 + 105 | i dati dell'A/B di `chi_basc`, dietro `Z73`-`Z77` |
| `_ab_C_solo_chicoop_FERMATO` | 346 | l'archivio del primo lancio di D, **conservato** |

---


---

## 🗃 TABELLA DI CORRISPONDENZA — **gli archivi `.pkl` spostati su `E:` il 2026-09-21**

> **I documenti STORICI non sono stati riscritti** — referti, task history, voci del registro
> continuano a citare i percorsi `C:`, **ed e' corretto cosi'**: un referto del 19 settembre
> riscritto con un percorso del 21 diventa un documento che non e' mai esistito.
> **Questa tabella e' il ponte.** Radice nuova: **`E:\soliton_archivio\`**, con la **stessa
> struttura di cartelle** del repository.
> **Verifica:** `sha1` dei byte del file **compresso**, originale contro copia, **187 file su 187**.
> Il registro riga-per-riga, con ogni `sha1`, e' in **`doc/SPOSTAMENTO_archivi.tsv`**.

| percorso VECCHIO (citato nei documenti storici) | percorso NUOVO | file | MB |
|---|---|---:|---:|
| `csv/_test_fork/_g6000/` | `E:\soliton_archivio\csv\_test_fork\_g6000\` | 45 | 1313.6 |
| `csv/_test_fork/_ab_A/` | `E:\soliton_archivio\csv\_test_fork\_ab_A\` | 25 | 923.0 |
| `csv/_test_fork/` | `E:\soliton_archivio\csv\_test_fork\` | 36 | 631.7 |
| `csv/_seal_fork/` | `E:\soliton_archivio\csv\_seal_fork\` | 24 | 428.7 |
| `csv/_test_fork/_ab_C_solo_chicoop_FERMATO/` | `E:\soliton_archivio\csv\_test_fork\_ab_C_solo_chicoop_FERMATO\` | 10 | 345.8 |
| `csv/_test_fork/_fin_B/` | `E:\soliton_archivio\csv\_test_fork\_fin_B\` | 11 | 308.3 |
| `csv/_seal_fork/_ab_grav_ampiezza/B/` | `E:\soliton_archivio\csv\_seal_fork\_ab_grav_ampiezza\B\` | 9 | 253.5 |
| `csv/_seal_fork/_ab_coppia_reciproca/B/` | `E:\soliton_archivio\csv\_seal_fork\_ab_coppia_reciproca\B\` | 9 | 253.5 |
| `csv/_seal_fork/_ab_coppia_reciproca/A/` | `E:\soliton_archivio\csv\_seal_fork\_ab_coppia_reciproca\A\` | 9 | 252.7 |
| `csv/_seal_fork/_ab_grav_ampiezza/A/` | `E:\soliton_archivio\csv\_seal_fork\_ab_grav_ampiezza\A\` | 9 | 252.7 |

**⚠ E il COMANDO che rigenera un archivio NON e' stato cambiato da nessuna parte.**
La **posizione** di un archivio e il **comando** che lo produce sono due cose diverse:
un run scrive su `C:`, e solo dopo l'archivio viene spostato. Cambiare i comandi in
`INVENTARIO_strumenti.md` li renderebbe **sbagliati**.

---
# ⚠ LA CODA UNICA — **l'ordine del lavoro, e l'UNICA fonte dell'ordine**

> **Decisione di Luca, 2026-09-21.** **Se un mandato sembra contraddire questa coda, VINCE LA CODA
> e lo si SEGNALA a Luca.** Ogni voce si spunta quando e' fatta.

| # | voce | mandato | stato |
|---|---|---|---|
| 1-5 | `CHI_COOP` · `SCALA_MIN`+`COES_ADIM` · sigillo `11/11`+`Z1c` · lancio ramo D · tag `epoca-2` | perentorio, EPOCA | ✅ **FATTE** *(il ramo D **fermato al 1230**: non e' una divergenza, sono **picchi transitori** — `Z90` corretta)* |
| **4-bis** | **DIAGNOSI DEI PICCHI DI `n1`** — i tre numeri che mancano | GLOBALE §1 | ▶ **passo `1126`, arco `3352-506`, `peq = -4.85e-04` NEGATIVO gia' misurati** (`Z93`, `Z94`). **Restano: `max(dt_e/tau_bg_loc)`, QUANTI archi con `peq < 0`, QUALE termine di `:4206` li porta sotto** |
| **C1** | **CURA ① `PEQ_ESATTO`** — rilassamento in forma esatta esponenziale, `peq` non scavalca mai | GLOBALE §2① | ⏸ |
| **C2** | **CURA ② `PEQ_NASCITA_LOCALE`** — Schwinger (`:4846`) prende `rho` del SUO arco, non la mediana globale | GLOBALE §2② | ⏸ *(`A2`, `A10`)* |
| **C3** | **CURA ③ `SCALA_MIN_PASSO`** — il freno UNA VOLTA per passo, sulla variazione TOTALE, dal valore di INIZIO passo | GLOBALE §2③ | ⏸ **col SIGILLO NUOVO sulla COMPOSIZIONE**, che oggi non esiste (`A9`) |
| **C4** | **CURA ④ `COES_CAUSALE`** — ingressi di INIZIO passo e tetto dal cono LOCALE dell'arco | GLOBALE §2④ | ⏸ *(`A5`)* |
| **V** | **VALIDAZIONE BREVE** — tre modifiche + quattro cure, 600 passi, `sep = 4.0`, stesso seme | GLOBALE §3 | ⏸ **⚠ CHECKPOINT 2: QUI CI SI FERMA E SI ASPETTA LUCA** |
| **8-bis** | **ARCHIVIO A ROTAZIONE** — si scrive su `C:`, ogni snapshot completo va su `E:` con `sha1` dei byte compressi, sigilli `R1`-`R5` | archivio | 🔒 **dopo il via libera del CHECKPOINT 2** |
| **E3** | **EPOCA 3 + NUOVO RAMO D COMPLETO** — tag `epoca-3`, 3000 passi, `M1`/`M4` leggere durante il run | GLOBALE §4 | 🔒 **dopo il via libera.** **NESSUN confronto con le epoche precedenti** |
| 6 | strumento cosmologico `M1`-`M4`, **sul nuovo D** | COSMOLOGICO | ⏸ |
| 7 | **`Z47` PARTE ①** — ricognizione di `pos` nella fisica *(sola lettura)* | `MANDATO_Z47_coda` | ⏸ |
| 8 | `M2`/`M3` cosmologici *(pesanti)* | COSMOLOGICO | ⏸ |
| 9 | **CHECKPOINT FINALE a Luca** | — | ⏸ |
| 10 | `Z47` PARTE ② — lo stacco | `MANDATO_Z47_coda` | 🔒 **NON parte senza il via libera di Luca** |

> **⚠ PERCHE' IL COSMOLOGICO E' IN FONDO:** **le misure cosmologiche su un run che esplode NON
> misurano la cosmologia.** `M1`-`M4` chiedono se l'espansione sia senza centro e localmente
> trasparente; un run che attraversa picchi di `nsub` a `22591`, con `peq` fuori dal dominio fisico,
> **non e' il sistema di cui si vuole sapere questo.** **Prima si cura, poi si misura.**

> **⚠ REGISTRATI E NON CURATI IN QUESTO GIRO** *(GLOBALE §6, restano nel SOSPESO)*: **`n3`
> normalizzato su `median(d)`** · **la spinta `S09` moltiplicata per `median(d0)`** · **`Z47`** ·
> **la carica che non produce forze.**


> **⚠ Se una voce si blocca, le successive ASPETTANO: non si passa avanti.**
>
> **⚠⚠ SEGNALAZIONE A LUCA, come la coda stessa impone — IL MANDATO DEL 2026-09-21 CONTRADDICE QUESTA CODA, E LA CODA DICE DI SEGNALARLO.**
> **La coda** mette il **CHECKPOINT** alla voce **9**, cioe' **dopo** il cosmologico `M1`-`M4` (6), `Z47` parte ① (7), `M2`/`M3` (8) e l'archivio a rotazione (8-bis).
> **Il mandato** dice *«ORDINE: 1 lancia la rigiocata, 2 la lettura, 3 commit e push, 4 FERMATI: checkpoint a Luca»* — cioe' **checkpoint SUBITO, saltando 6, 7, 8 e 8-bis**.
> **Cosa ho fatto:** ho eseguito il mandato *(la diagnosi e' la voce **4-bis**, e la voce 4 era la prima non spuntata, quindi la diagnosi del suo esito sta al posto giusto)*, **e mi fermo al checkpoint senza toccare 6, 7, 8 e 8-bis**.
> **✅ RISOLTA il 2026-09-21: Luca ha RIORDINATO la coda lui**, ed e' l'ordine scritto qui sopra. La segnalazione resta leggibile perche' mostra che il meccanismo ha funzionato: **la coda ha vinto sul mandato, e' stato segnalato, e l'ordine l'ha deciso Luca.**

---

## SOSPESO

- **`Z47`, RICOGNIZIONE in coda:** parte dopo il lancio del ramo D (vedi `MANDATO_Z47_coda`), voce
  `7` della coda unica. **Sola lettura, nessuna CPU al run.**

---

# STATO DEI RUN — registro append-only

**Scritto AUTOMATICAMENTE da `csv/_stato_run.py`.** Il commit NON è
automatico (vedi la dichiarazione nel modulo): ma **il file esiste sempre**,
quindi dopo un riavvio lo stato si legge **dal disco**, non dalla memoria.

**Una voce `APERTO` senza `chiuso` = quel run è morto senza dirlo.**


## APERTO batch-1200 (campagna struttura)

- **avvio** `2026-09-18 17:42:46` · **blob** `a1ae5090` · **HEAD** `53b9443`
- **comando**
  ```
  python soliton_simulator.py --batch --nmasse 3 --sep 8 --passi 1200 --ogni 10 --csv csv/_test_fork/_g1200/cond.csv --diaglog csv/_test_fork/_g1200/diag.csv --campo-spinoriale --spinore-vivo --spinore-corretto --chi-core --calore-scal --deparam-orologio --verlet --fork-su2 --fork-su2-mem --cs-dinamico --tau-luce --rumore-colorato --pav-com --guscio-morbido --zeta-vir --chi-basc --plast-din --viriale --olon-part --sync-db csv/_test_fork/_g1200/stato.pkl --db-ogni 10 --db-cleanup
  ```
- **note** voce RICOSTRUITA dai dati sul disco: il registro non esisteva quando il run e' partito.
- *2026-09-18 17:42:46* — seed 900, letto da run.log. Una sola invocazione, 0 righe `[db] stato CARICATO`.
- *2026-09-18 17:42:46* — snapshot presi ai passi VERI 120 / 130 / 470 / 800 / 840 / 1200 (i primi tre mislabellati dal watcher e RINOMINATI col loro `_db_step`).

**chiuso 2026-09-18 17:42:46 — FINITO** Ultima riga di `diag.csv`: **passo 1200**, 21662 righe, `n = 1204`. **Dati COMPLETI.** Analisi fatta: `doc/REFERTO_chi_non_invecchia.md` (`Z46`/`Z9`). ⚠ **MANCA il referto dei QUATTRO BLOCCHI** del mandato «struttura a 1200» (maturazione / guscio / fasi / contrasto): la sonda `csv/_test_fork/_struttura_1200.py` e' COMMITTATA (`35a5786`) ma **NON E' MAI STATA GIRATA**.

## APERTO scena-video TENTATIVO 1

- **avvio** `2026-09-18 17:42:46` · **blob** `a1ae5090` · **HEAD** `53b9443`
- **comando**
  ```
  python csv/_test_fork/_scena_video.py 400 csv/_test_fork/_gvideo 10,115,190,270,375
  ```
- **note** voce RICOSTRUITA: il commit `b84702b` dice «RUN FERMATO» ma NON diceva a che punto.

**chiuso 2026-09-18 17:42:47 — FERMATO** Fermato al **frame ~50 su 400** *(`n` 2391 -> 2576, `14.1 s/frame`)*. **Motivo:** l'equivalenza del driver col `update()` del video era **DEDOTTA, non verificata**. **I dati parziali sono stati CANCELLATI** perche' su una traiettoria non certificata: **non servono.** Il sigillo `_sigillo_driver_video.py` ha poi dato **PASS** (14 array, `max|A-B| = 0.000e+00`, shape uguali).

## APERTO scena-video TENTATIVO 2 (in corso)

- **avvio** `2026-09-18 17:42:47` · **blob** `a1ae5090` · **HEAD** `53b9443`
- **comando**
  ```
  python csv/_test_fork/_scena_video.py 400 csv/_test_fork/_gvideo 10,115,190,270,375 > csv/_test_fork/_gvideo_run.log 2>&1
  ```
- **note** Rilanciato DOPO il PASS del sigillo del driver (`94e2ec0`).
- *2026-09-18 17:42:47* — **IN CORSO** al momento della scrittura: frame **170 su 400**, `n` 2391 -> 4120, `15.6 s/frame`. Snapshot gia' presi: **frame 10, frame 115**. Prossimi: 190 / 270 / 375.
- *2026-09-18 17:42:47* — ⚠ La scena include **`--tau-luce`, il cui SIGILLO E' FALLITO** (CLAUDE.md par.0): **ramo NON CERTIFICATO**, e ogni numero che ne esce lo eredita. E **`--chi-basc` riscrive `perc_chi` a ogni passo**: non e' un'etichetta di lignaggio.
- *2026-09-18 17:42:47* — ⚠ `PASSI_PER_FRAME = 6`: **400 frame = 2400 PASSI**. La tabella dei fotogrammi va RIMAPPATA (**frame 375 = passo 2250**), o i confronti con `Z46` (1200 passi) sbagliano di 2.
- *2026-09-18 17:46:16* — ✅ **IL REFERTO MANCANTE C'E'**: `doc/REFERTO_struttura_1200.md` (`Z48`). Letti gli istanti 120/800/1200; **130/470/840 NON letti** (la sonda cerca per NOME). La voce del batch e' CHIUSA e completa.
- *2026-09-18 18:10:22* — **frame 275/400** (`n` 2391 -> 5520, `15.6 s/frame`, ~33 min alla fine). Snapshot presi: **10, 115, 190, 270**. Manca **375**. ⚠ **L'INVERSIONE DELLA DILATAZIONE E' GIA' VISIBILE NEI MIEI DATI: `dil` da `+10.97 %` (frame 265) a `+8.59 %` (frame 275).** E al frame 270 `n = 5443` contro `5465` della tabella dei fotogrammi, `dil +10.75 %` contro `+10.3 %`: **e' la stessa scena.**
- *2026-09-18 18:42:13* — **frame 385/400**, `n = 7694`, `16.2 s/frame`. **TUTTI E CINQUE gli snapshot presi** (10/115/190/270/**375**). ⚠ **LA DILATAZIONE HA INVERTITO E STA OSCILLANDO:** `dil` = `-7.439 %` (370), `-2.704 %` (375), `-4.214 %` (380), `+2.797 %` (385). **Non e' solo «si ricomprime»: RIMBALZA.** `coer_l` continua a salire: `0.622 -> 0.631`. Al frame 375 `n = 7480` contro `7503` della tabella dei fotogrammi: **stessa scena.**

**chiuso 2026-09-18 18:47:44 — FINITO** **400 frame = 2400 passi in 6535 s (1h49)**, `16.34 s/frame`, **`n` da 2391 a 8018**. **SEI snapshot** (10/115/190/270/375/**400**). Stato finale: `coer_l = 0.669`, `dil = -1.13 %`. ⚠ **La dilatazione INVERTE e poi RIMBALZA**: `-7.44 %` (370) -> `-2.70 %` (375) -> `-4.21 %` (380) -> `+2.80 %` (385) -> `-1.13 %` (400). **La tabella dei fotogrammi si fermava al 375 e non poteva vederlo.** Dati in `csv/_test_fork/_gvideo/`; i `.pkl` NON si committano (48 MB l'uno).
- *2026-09-18 18:50:21* — ✅ **ANALISI FATTA**: `doc/REFERTO_struttura_video.md` (`Z49`). Sei istanti letti (frame 10/115/190/270/375/400 = passi 60/690/1140/1620/2250/2400).

## APERTO due-masse CONTROLLO (A/B su --nmasse)

- **avvio** `2026-09-18 19:40:56` · **blob** `a1ae5090` · **HEAD** `8f94cf4`
- **comando**
  ```
  python csv/_test_fork/_scena_video.py 400 csv/_test_fork/_g2m 10,115,190,270,375 fisica 2
  ```
- **note** A/B A VARIABILE SINGOLA contro `Z49`: cambia SOLO `--nmasse` (3 -> 2). **La PREDIZIONE DI LUCA e' committata PRIMA, in `a4fbe42`.**
- *2026-09-18 19:40:57* — pilota MISURATO: `n = 1894` alla semina, **`13.68 s/frame`** -> ~**1h35** per 400 frame. ⚠ **Il primo falsificatore scatta in parte: attendevo `n ~ 1594` (2/3 di 2391), misurato `1894` = il 79 %.** La semina per massa **NON e' lineare nel numero di masse**: le due scene differiscono anche per POPOLAZIONE, in modo non proporzionale. **Va nel referto.**

**chiuso 2026-09-18 21:10:45 — FINITO** **400 frame = 2400 passi in 5357.8 s (1h29)**, `13.40 s/frame`, **`n` da 1894 a 5878**. **SEI snapshot** (10/115/190/270/375/400) in `csv/_test_fork/_g2m/`. I `.pkl` NON si committano. **Confronto col run a TRE masse (`Z49`): `n` finale `5878` contro `8018`.**

## APERTO pilota-6000 (BLOCCANTE, prima del run lungo)

- **avvio** `2026-09-19 09:49:38` · **blob** `b9e07c73` · **HEAD** `d7b3a33`
- **comando**
  ```
  python soliton_simulator.py --batch --nmasse 3 --sep 8 --passi 300 --ogni 50 --db-ogni 300 --seed 900 --campo-spinoriale --spinore-vivo --spinore-corretto --chi-core --calore-scal --deparam-orologio --verlet --fork-su2 --fork-su2-mem --cs-dinamico --tau-luce --rumore-colorato --pav-com --guscio-morbido --zeta-vir --chi-basc --plast-din --viriale --olon-part --sync-db csv/_test_fork/_pilota6000/pilota.pkl --csv csv/_test_fork/_pilota6000/pilota.csv
  ```
- **note** PILOTA BLOCCANTE del mandato par.1: il batch matura entro 6000 passi, o `r` e' al pavimento come dice `Z46`? Seme 900, lo STESSO di `Z46`, cosi' il confronto e' sulla stessa scena (A3c).

**chiuso 2026-09-19 09:49:38 — FINITO** **300 passi in 371 s = `123.7 s/100`** (il batch a 1200 dava `127.5`: REGGE). `.pkl` **26.45 MB**. **VERDETTO: il batch NON MATURA. `93.0 %` dei nodi e' al pavimento con `r/r_floor = 1.0000`, e il loro tasso da' `1.5 MILIONI` di passi per `ramp = 1`.** **IL RUN A 6000 SUL BATCH NON SI LANCIA.**

## APERTO run-6000 SCENA VIDEO (l'archivio a serie)

- **avvio** `2026-09-19 14:38:00` · **blob** `7c4dec1d` *(SIGILLATO 12/12)* · **HEAD** `406d31f`
- **seme effettivo** `42` — **letto da `Rete.__init__`, NON 900**: `SEME_INIZIALE = 900` e' il
  NUMERO DI NODI seminati (`:4532`), e solo nel `--batch` lo stesso 900 e' riusato come seme
  (`:6407`). Scrivere «seed 900» qui sarebbe falso.
- **comando**
  ```
  python csv/_test_fork/_scena_video.py 1000 csv/_test_fork/_g6000 --serie=10 --csv-progresso=csv/_test_fork/_g6000/prog.csv
  ```
  → **1000 frame x 6 = 6000 passi**, snapshot **ogni 10 frame = 60 passi** → **100 snapshot**
  `scena_%06d.pkl.gz` (compressi a livello 1).
- **cadenza DERIVATA dal pilota**, non scelta: budget dichiarato **5.0 GB** prima di vedere i
  numeri; peso stimato **2.95-3.02 GB**; la cadenza 30 passi darebbe ~6 GB (oltre).
- **previsioni committate PRIMA**: `doc/PREVISIONI_run6000_scena.md`.
- **note** `--tau-luce` e' nel comando: sigillo **6/7**, `T3` e' un risultato dichiarato. Ogni
  numero di questo run lo eredita. `--chi-basc` riscrive `perc_chi`: non e' lignaggio.
- **attesa** ~**7.5 h** col modello lineare, **che SOTTOSTIMA** (il costo per frame cresce con `n`).
- **Z9-a all'avvio**: `passi(ramp=1) = 5098` sui mobili, contro i 6000 del run — **margine 18 %**,
  e `r` si e' mosso del **+149 % in 120 passi**: e' un'istantanea, non una previsione.

### ⚠ DA FARE A RUN FINITO — **la patch della ripresa, e la verifica che la precede**

> **✅ ASSORBITA il 2026-09-20 nella sezione «IL SOSPESO — LA LISTA UNICA» (voce `C`), e CHIUSA:**
> la ripresa **è** sul driver vero. Il testo resta per la cronaca, non come cosa da fare.

> **A RUN FINITO: portare la patch della ripresa sul driver vero** (`csv/_test_fork/_scena_video.py`,
> da **`f14ea4bd`** a **`7a02c5c3`**, la versione **sigillata 5/5** in
> `csv/_seal_fork/_sigillo_ripresa_scena.txt`). **NON prima che il run sia chiuso.**
>
> *(La patch era già stata applicata il 2026-09-19 alle ~15:55 **mentre il run girava**, e
> **ripristinata** alle 15:57:52 — commit `228eb07`. Non c'è stato danno, ed è **misurato**:
> `23f783e`, `3/3`, ripartendo dal passo 1800 si riottiene identico lo snapshot 1860 scritto
> durante quella finestra. **Ma «stavolta è andata bene» non è «era sicuro».**)*

> **PRIMA di applicare la patch, verificare DAL CODICE — non assumere — che gli snapshot di QUESTO
> run restino caricabili dopo che il driver è cambiato.**
>
> **Il ragionamento dice di sì:** `carica_stato` verifica il blob di **`soliton_simulator.py`**, non
> quello del driver, e il simulatore è **intatto** (`7c4dec1d` per tutta la sequenza).
> **Ma va CONFERMATO:** cercare dove viene usato il **blob del driver** (`f14ea4bd` → `7a02c5c3`) e
> se **BLOCCA** qualcosa.
>
> **Se esiste un controllo che include il driver e rifiuta:** il discriminante va riportato al blob
> del **SIMULATORE**, perché è quello che definisce la **FISICA** — e **solo perché** il sigillo del
> driver esteso ha dato **PASS** (`14 array, max|A-B| = 0.000e+00`). **Senza quel sigillo, NON si
> accetta.**
>
> **E la prova finale, dopo la patch:** ricaricare uno snapshot **di questo run** e riprendere.
> **Deve funzionare.**

**chiuso 2026-09-19 19:05 — FERMATO DA LUCA, dopo 2h30 di stallo.** **`450` frame su 1000 =
`2700` passi su 6000**, in `7013 s` di progresso utile più **~2h30 in cui il processo era VIVO e
non avanzava** (`15 817 s` di CPU totali, `99.6 %` su **un solo core**, nessuna scrittura dopo le
`16:35:05`).

**L'ARCHIVIO È INTATTO E COMPLETO fino al passo 2700**, verificato dopo l'arresto:
**45 snapshot su 45** si aprono, il `_db_step` **nel file** coincide con quello **nel nome**, serie
**contigua** da 60 a 2700 a cadenza 60, **nessun buco**, **nessun `.tmp`** lasciato a metà
*(`os.replace` è atomico: o il file c'è completo, o non c'è)*. **1.3 GB**, blob `7c4dec1d` ovunque.

**Il blocco NON è spiegato.** Escluso misurando: memoria *(287 MB usati, 11.5 GB liberi)*, disco
*(17 GB)*, CFL *(`_taup_cfl_max` fermo a `0.5657`, zero clamp)*, `MAX_NODI` *(9511 su 4 000 000)*,
`NaN`/`inf` *(zero su tutti gli array)*. → `doc/REFERTO_blocco_run6000.md`, dati grezzi in
`csv/_test_fork/_dump_2700.txt`.

**COSA RESTA FATTIBILE, e non è poco:** le misure del §3 del mandato — `Z9-b`, `ramp` per coorte,
`p95/p05`, le conseguenze, il ciclo — **si fanno su questi 45 snapshot senza rigirare niente**.
L'analizzatore è pronto: `csv/_test_fork/_misure_run6000.py`.

**E la ripresa è sigillata `5/5`:** si può ripartire dal passo 2700 — **ma prima va capito perché
si è fermato**, altrimenti si riparte verso lo stesso muro.

---

## CHECKPOINT 2026-09-20 — **chiusa la topologia (`Z65`). Il simulatore non è stato toccato.**

**HEAD `3a02819` · blob `775ceab7` · albero pulito · nessun processo in esecuzione.**

**Fatto oggi, tutto sui 45 snapshot già in archivio, senza rigirare niente:** le somme (`Z63`), `f`
e `median(|f|)` (`Z64`), e **la topologia (`Z65`)** — quattro componenti connesse che in 2700 passi
non si scambiano **nemmeno un arco**, i due picchi del grado che sono **la semina** (tre grafi
**completi** da 497 nodi al passo 6) e non una forma emersa, e il **grado 2 permanente** (84 % dopo
2100 passi). → `doc/REFERTO_topologia.md`.

**Un presidio che prima era un'assunzione, ora misurato:** `eta[k]` non diminuisce in **nessuna**
delle 44 transizioni → **gli indici dei nodi sono stabili**, e ogni misura di coorte fatta finora
poggiava su quello senza averlo verificato.

### Cosa resta da fare quando il run è definitivamente chiuso

> **✅ ASSORBITA il 2026-09-20 in «IL SOSPESO — LA LISTA UNICA»:** il punto 1 è **CHIUSO**
> (voce `C`), il punto 2 puntava al **bersaglio sbagliato** (voce `B10`), il punto 3 è la voce
> `B9`. Il testo resta per la cronaca.

1. **riapplicare la patch di ripresa** a `csv/_test_fork/_scena_video.py` (`f14ea4bd` → `7a02c5c3`),
   **dopo** aver verificato dal codice che gli snapshot dell'archivio restano caricabili col blob
   del driver cambiato; poi rigirare il sigillo del driver e **provare davvero** un ricarico +
   ripresa da uno snapshot reale;
2. **togliere `--override-blob`** dal driver: è un presidio **deliberatamente indebolito**,
   accettabile solo finché gli esperimenti su `COPPIA_RECIPROCA` / `GRAV_AMPIEZZA` sono aperti;
3. **i fronti aperti che nessuna misura di oggi ha chiuso:** perché il run si sia fermato al 2700;
   perché la catena `f → x → r` non riproduca `r` dal passo 24 (`Z64`, famiglia `Z19`); perché 1455
   nodi stiano a `10⁻¹³` nel ramo A e qualunque perturbazione della coppia li accenda (`Z63`); se
   il profilo identico delle due cure sia **divergenza caotica** — servirebbe un terzo braccio con
   perturbazione nulla, o un secondo seme.

---

## 2026-09-20 — **L'ORDINE DEL LAVORO, deciso da Luca: ① → ② → ③**

**HEAD `e403e15` · simulatore `f81c4fe1`** *(sha1 byte grezzi; blob git `af8a96f1`)* · albero
pulito · **nessun run in esecuzione.**

```
①  LE GUARDIE DI PRECONDIZIONE          <- in corso
②  IL PANNELLO FEDELE                   <- dopo ①
③  IL RUN LUNGO a sep = 4.0             <- PER ULTIMO
```

**Nessun run parte finché ① e ② non sono chiusi.**

### Cosa è già pronto per ③, e resta sigillato

- **il driver** `csv/_test_fork/_scena_video.py`: `--sep=X` nominale *(sigillo `4/4`)* e la
  **ripresa** `--riprendi` *(sigillo `5/5` sul driver VERO)*;
- **il pilota a `sep = 4.0`**: archi massa-massa **0**, archi massa-vuoto **97 447** stabili
  *(−0.15 % in 300 passi)*, **una componente**, **196 nodi `MISTO`**;
- **la cadenza proposta**: `--serie=20` *(= `--db-ogni 120` passi)* → **83 snapshot, 3.0-4.5 GB**
  su **15 GB liberi** *(disco al 97 %)*;
- **il costo misurato**: `2.922 s/passo` → **8.1 ore come LIMITE INFERIORE** per 10.000 passi.

### ⚠ E una regola che sarebbe servita due giorni fa

> **Prima di interpretare QUALUNQUE struttura vista in un pannello, verificare che ci siano ARCHI
> in quella regione.**

**Il caso reale:** nel run a `sep = 8` il pannello del campo mostrava interferenza **fra le masse**,
e le masse stavano in **quattro componenti connesse con ZERO archi fra loro** *(`Z65`)*. Il
pannello non mentiva — `campo_spaziale` somma su **tutti i nodi**, non sugli archi — **ma la
lettura sì.** Il tool del video (`csv/_test_fork/_video_da_snapshot.py`) stampa il conteggio degli
archi fra componenti **su ogni frame**, proprio per questo.

---

## 2026-09-20 (sera) — **L'ORDINE SI ALLUNGA: ① → ② → ③ → ④**

```
①  LE GUARDIE                      CHIUSO   Z67 (5/5) · Z68 (3/3) · Z69 (3/4 + 1 atteso)
②  IL PANNELLO FEDELE              prossimo
③  LE METRICHE DEL SETTORE CHIRALE + un giro breve a sep = 4.0
④  IL RUN LUNGO a sep = 4.0        per ultimo
```

**Le metriche vanno PRIMA del run: otto ore senza i dati che servono sarebbero da rifare.**

### ⚠ E l'`83 %` a `-1` del passo 2700 NON VALE — ma non per la ragione che sembrava

**Non è (solo) che il grafo fosse in quattro componenti scollegate.** È che **`perc_chi` non è un
lignaggio**: con `CHI_BASC = 1` *(ed era `1` nel run)* la riga `:3765` **riscrive l'intero array a
ogni passo** da `twn > PHI_CRIT`.

> **Quell'`83 %` è la frazione di nodi che NON hanno completato un giro di olonomia.**
> **È un dato sulla TORSIONE, letto come se fosse un dato sulla CHIRALITÀ.**

**E l'eredità chirale della mitosi (`:4294`) e la coppia opposta di Schwinger (`:4415`) sono
appese DOPO `chi_basc` nel ciclo, quindi sopravvivono ESATTAMENTE ZERO passi completi.**
*(Dettaglio e righe in `doc/TASK_HISTORY/2026-09-20_metriche-settore-chirale.md`.)*

### La voce TODO del ② — il pannello fedele

> **✅ ASSORBITA il 2026-09-20 in «IL SOSPESO — LA LISTA UNICA», voce `A5`.**
> Il testo resta: contiene i VINCOLI, che la lista non ripete.

**Il problema, misurato:** `campo_spaziale` somma su **tutti i nodi** con la FFT; `calcola_psi`
solo **sugli archi**. Nel run a `sep = 8` il pannello mostrava interferenza **fra masse in quattro
componenti con zero archi fra loro**.
**Cosa fare:** **un pannello IN PIÙ** che **interpola `psi`** sulla stessa griglia. **Entrambi
restano** — `campo_spaziale` dà **continuità**, l'interpolazione dà **fedeltà**, il grafo dà la
**topologia**.
**Vincoli:** non si tocca `campo_spaziale` né la FFT · **il blob del simulatore NON cambia: è
rendering** · **l'interpolazione LEGGE `psi`, non lo RICALCOLA** *(precedente `lambda_vuoto`)* · i
buchi si **dichiarano** · uno smoothing, se serve, ha la scala **derivata** · **si misura il costo.**

---

# IL SOSPESO — **LA LISTA UNICA** (censita il 2026-09-20, verificata DAL DISCO)

> **Questa è LA lista.** Le tre liste parziali che esistevano prima — *«DA FARE A RUN FINITO»*,
> *«Cosa resta da fare quando il run è definitivamente chiuso»*, *«La voce TODO del ② — il pannello
> fedele»* — **sono ASSORBITE qui** e portano un rimando. **Non se ne apre una quarta.**

**⚠ COME È STATA FATTA, perché cambia quanto ci si può fidare:** l'elenco di partenza veniva dalla
conversazione. **Ogni voce è stata verificata dal disco**, e la verifica ha prodotto **tre
correzioni all'elenco di partenza e due miei errori** *(§ «Cosa la verifica ha cambiato»)*.

### La legenda della validità — **il presidio contro le tre ritrattazioni di oggi**

```
VALE SEMPRE            un difetto di codice, una legge, un fatto letto dal sorgente
VALE PER QUELLA SCENA  un numero misurato su sep = 8 / quattro componenti / una finestra
DA RIVERIFICARE        la premessa sotto è cambiata (scena nuova, blob nuovo, cura applicata)
```
**Il discriminante è una domanda sola:** *«se rigirassi questo su un'altra scena, il numero
cambierebbe?»* Se sì → `VALE PER QUELLA SCENA`. Se la domanda non ha senso perché non c'è un numero
(è una lettura del codice) → `VALE SEMPRE`.

---

## A — LASCIATE A METÀ OGGI (2026-09-20)

| # | la voce | dove sta | a che punto è | cosa manca | chi decide | validità |
|---|---|---|---|---|---|---|
| **A1** | **la catena a TRE VIE di `step`** — `if CHI_CORE… / elif VERSO_CHI… / elif not(…)` | **`:3623` · `:3626` · `:3632`** *(⚠ era citata `:3517`-`:3526`: **slittata di 106 righe**, ritrovata per CONTENUTO)*; `doc/REFERTO_classifica_18_guardie.md` righe 25-27, 90-91 | **né applicata né scartata.** Verificato: **nessun contatore** sulla catena, mentre la gemella `:2366` ne ha quattro | **la FORMA**: tre contatori `_salti` (uno per ramo) **oppure** uno con tre conteggi «quale ramo». Io avevo già dichiarato di preferire **nessuno dei due** *(un contatore per ramo su una scelta a tre vie non misura un fallimento, misura una selezione)* — e l'avevo dichiarata come **mia deviazione dal mandato** | **LUCA** | `VALE SEMPRE` |
| **A2** | **l'anello `A6` di `Z70`** — periodo 2, via `chiralita_core_locale`/`CHI_CORE` | `doc/RAMIFICAZIONI.md` `Z70` | **registrato, NON curato.** `A6` nella sua *lettera* non è violato (ogni gamba legge lo snapshot d'inizio passo), ma `perc_chi` è **schiava** di `tw` | la cura è **un giro a sé** e non è stata fatta | **LUCA** *(è una cura, non una misura)* | `VALE SEMPRE` |
| **A3** | **`Z71` — la carica chirale non si conserva** | `doc/RAMIFICAZIONI.md` `Z71` | **APERTA.** I due punti di scrittura sono verificati dal codice: **`:4294`** eredita UGUALE *(rompe)*, **`:4415`** antinodo OPPOSTO *(conserva)* | **una decisione di FISICA**: *la carica chirale deve conservarsi?* Se sì `:4294` è un difetto; se no, è il meccanismo. **Non si cura senza quella decisione** | **LUCA** | `VALE SEMPRE` |
| **A4** | **le METRICHE DEL SETTORE CHIRALE** | **`doc/TASK_HISTORY/2026-09-20_metriche-settore-chirale.md`** *(⚠ il documento **ESISTE**: vedi i miei errori, §E)* | **punto 1 del TODO fatto** *(il §1 verificato dal codice)*; **punti 2-5 aperti** | il pannello fedele **viene prima** *(è `A5`)*, poi le metriche byte-inerti, il sigillo, la voce nel registro | **io** | **`DA RIVERIFICARE`** — la metrica ④ era *«flip di `chi_basc`»* e **non è misurabile così**; ma **nel ramo B del run in corso `chi_basc` è SPENTO, quindi `perc_chi` È una carica** e la metrica torna misurabile nella forma «confronto di `perc_chi` prima/dopo» |
| **A5** | **il PANNELLO FEDELE** *(interpolazione di `psi` accanto a `campo_spaziale`)* | la **ex-LISTA 3** di questo file | **non iniziato** | un pannello **in più**, che **legge** `psi` e non lo ricalcola; i buchi dichiarati; il costo misurato. Il blob del simulatore **non cambia: è rendering** | **io** | `VALE SEMPRE` |
| **A6** | **`perc_chi` FA DUE LAVORI CON REGOLE OPPOSTE: `chi_basc` lo tratta da CHIRALITA', `TEMPO_SEGNO` da CARICA** — e finche' condividono un array **nessuno dei due puo' essere fatto bene** | `:3558` *(`TEMPO_SEGNO` legge `perc_chi` e ne ricava il VERSO DEL TEMPO)* · `:3765` *(`chi_basc` lo RISCRIVE a ogni passo dalla torsione)* · `:4294` / `:4466` *(le nascite)* · `Z70` `Z71` `Z73` | **REGISTRATA il 2026-09-20, NON iniziata.** **Nasce da un RAGIONAMENTO, non da una misura**, e va letta come tale | **LA PROPOSTA — da decidere, NON eseguita:** separare in **due grandezze**: una **CARICA** nuova, **scritta SOLO alla nascita e mai ricalcolata**, **opposta nelle coppie di Schwinger** (`:4466`), **letta da `TEMPO_SEGNO`**; e **`perc_chi` lasciata libera di essere GEOMETRIA**. *(Il nome della carica nuova NON lo invento: e' una scelta di progetto.)* **⚠ E LA FISICA DISTINGUE DAVVERO LE DUE COSE: la chiralita' NON si conserva** *(una particella con massa la cambia viaggiando)*, **una carica si' — sempre.** **Il NOME e' quello della prima, l'USO di `TEMPO_SEGNO` e' quello della seconda.** **⚠ PERCHE' LA DECISIONE CAMBIA RISPETTO A PRIMA:** la separazione in due array era gia' stata valutata e **SCARTATA**, con la ragione che la seconda grandezza sarebbe rimasta **SENZA LETTORI** — cioe' `A8`, un ramo silenzioso. **Un lettore ora c'e': `TEMPO_SEGNO` (`:3558`).** **⚠⚠ MA VERIFICATO DAL DISCO, E VA DETTO: `TEMPO_SEGNO = False` di default (`:858`), e il driver dei due run A/B NON lo passa — quindi nei run era SPENTO.** **Il lettore esiste nel CODICE ed e' INERTE nei fatti: la ragione dello scarto e' decaduta a META', non del tutto.** **COSA SISTEMEREBBE:** **`Z71`** *(la carica non si conserva: `:4294` eredita UGUALE e rompe, `:4415` OPPOSTA e conserva)* **diventerebbe una domanda DECIDIBILE invece che ambigua**; l'ambiguita' **`A10`** *(un solo significato per grandezza)*; e la domanda **«ogni nascita deve essere una COPPIA?»**, che e' `Z71` in un'altra forma — **se `perc_chi` e' una carica la coppia e' obbligata, se e' un'etichetta no.** **⚠ E COSA NON SISTEMEREBBE, verificato e non assunto: NON tocca il problema di `d0`.** La **coesione relazionale** (`:4877`), che nella traccia risulta **dominante e in giu'** (`-3.68e+03` su 120 passi), lavora su **geometria pura** — `cos2 = (r_rad/H)^2`, `radiale = grav*cos2` — **e `memoria_hebbiana_moto` (righe `4694-5016`) contiene ZERO occorrenze di `perc_chi`.** **I due problemi sono INDIPENDENTI e si curano separatamente**, e lo scrivo perche' domani non vengano legati per comodita' | **LUCA** — **e' una decisione di FISICA, non di codice** | 🟩`VALE SEMPRE` |

---

## B — APERTE DA PRIMA

| # | la voce | dove sta | a che punto è | cosa manca | chi decide | validità |
|---|---|---|---|---|---|---|
| **B1** | **`Z47` — `pos` nella fisica: l'ultimo SFONDO** | `doc/RAMIFICAZIONI.md` `Z47`, `doc/ASSIOMI.md` | **NON INIZIATO**, e il registro lo qualifica già *«progetto di lungo periodo»* | **il costo DECIDE**: non è una modifica, è la **riscrittura di QUATTRO settori** | **LUCA** | `VALE SEMPRE` |
| **B2** | **`Z31` — i sigilli non ri-girabili** | `Z31`, citata in **17 file** | **rifatta TRE volte**, l'ultima ieri | il recupero sistematico → **è il §2.2 del mandato di oggi**, in corso | **io** | `VALE SEMPRE` |
| **B3** | **i rami di `memoria_hebbiana_moto`** | `soliton_simulator.py:4616-4918` | **mai guardati** | ⚠ **sono `25`, non `23`** *(contati dal codice: `if`/`elif`/`else`/`try`/`except` nel corpo della funzione, 303 righe)*. Quanti siano su un **percorso fisico** non è misurato | **io** | `VALE SEMPRE` |
| **B4** | **i `np.zeros`** | tutto il simulatore | **mai guardati** | ⚠ **sono `116`, non `~10`**. Il numero utile non è questo: serve **restringere al percorso fisico**, e quel conto **non esiste ancora** | **io** | `VALE SEMPRE` |
| **B5** | **`theta` / l'aliasing del settore di spin** | `CLAUDE.md` §9, registro `C14`, fronte `A` | **aperto e noto**: `theta` ~ 39-129 giri/passo | `C14` chiude solo con `theta` sotto il tetto `2π·cs/λ`. **È il collo di bottiglia del programma** | **LUCA** *(è la voce `A`)* | `VALE SEMPRE` |
| **B6** | **le due cure OFF: `COPPIA_RECIPROCA` e `GRAV_AMPIEZZA`** | `:739` e `:732` *(entrambe `= False`)*, `doc/REFERTO_somme.md`, due task history del 19/9 | **A/B NEGATIVI** — ma fatti su **QUATTRO COMPONENTI SCOLLEGATE** | **rifare gli A/B sulla scena connessa `sep = 4.0`** | **io** | **`DA RIVERIFICARE`** |
| **B7** | **i reperti DA RIMISURARE sulla scena nuova** | `Z43`, `Z46`, `Z48`-`Z52`, `coer_g` | **misurati su `sep = 8`** | rimisura sulla scena connessa. **Marcatura già presente su 4 su 7**: `Z48`/`Z50`/`Z51` portano «QUALIFICATA», `Z49` dice «scena VIDEO»; **`Z46` non porta NESSUNA marcatura** | **io** | **`VALE PER QUELLA SCENA`** |
| **B8** | **⚠ IL BLOCCO DEL RUN A 6000 AL PASSO 2700** | **`doc/REFERTO_blocco_run6000.md`** *(131 righe)*, `csv/_test_fork/_dump_2700.txt` | ⚠ **NON «mai diagnosticato»: PARZIALMENTE diagnosticato.** **Sei** ipotesi **escluse misurandole** *(memoria, disco, CFL, `MAX_NODI`, `NaN`, contatori)*; la degenerazione documentata *(`d0` max `43 → 395`, `1227` archi sopra `10×p50`)*; lo **stato al 2700 CATTURATO** (45 snapshot + dump di 113 chiavi). **Ciò che NON fu catturato è lo STACK** | **la causa resta ③ «non lo so»**, dichiarata come tale nel referto | **io** | `VALE PER QUELLA SCENA` *(i numeri)* + `VALE SEMPRE` *(le esclusioni)* |
| **B9** | **`Z63` / `Z64`** — i 1455 nodi a `10⁻¹³`; la catena `f → x → r` che non riproduce `r` | registro, **ex-LISTA 2 punto 3** | aperti | vedi le rispettive voci | **io** | `VALE PER QUELLA SCENA` |
| **B10** | **⚠ `--override-blob` e la COPIA del driver** | `csv/_test_fork/_scena_video_ripresa.py` *(`e68bb8c5`, 17466 byte)* e `csv/_seal_fork/_ab_reciprocita.py` | ⚠ **DUE fatti nuovi.** ① **`--override-blob` NON è nel driver vero** *(`0` occorrenze in `_scena_video.py`)*: la ex-LISTA 2 punto 2 **puntava al bersaglio sbagliato**. ② **la COPIA `_scena_video_ripresa.py` ESISTE ANCORA ed è tracciata da git**, mentre il docstring del driver vero dice *«la copia è stata rimossa»* | **un docstring STALE** *(la classe di difetto che `CLAUDE.md` §0 chiama per nome)*, e **un secondo driver nel repo che porta un presidio deliberatamente indebolito** | **io** *(il docstring)* · **LUCA** *(se la copia va tolta)* | `VALE SEMPRE` |

---

## C — CHIUSE DALLA VERIFICA DI OGGI *(tolte dalla lista, e si dice perché)*

| la voce | era | ora | la prova |
|---|---|---|---|
| **ex-LISTA 1** e **ex-LISTA 2 punto 1** — *«riapplicare la patch della ripresa al driver vero»* | **DA FARE A RUN FINITO** | **✅ CHIUSA** | la ripresa **è** nel driver vero *(`10` occorrenze di `--riprendi`/`RIPRENDI` in `_scena_video.py`)*, e il driver attuale `9aee4fc2` la contiene |
| **ex-LISTA 2 punto 2** — *«togliere `--override-blob` dal driver»* | DA FARE | **✅ CHIUSA PER IL DRIVER VERO** *(0 occorrenze)* — **ma resta aperta altrove: → `B10`** | `grep` sul disco |

---

## D — IL CONTO

```
voci sospese CENSITE          15      (5 lasciate a meta' oggi + 10 aperte da prima)
  di cui DECIDE LUCA           5      A1, A2, A3, B1, B5   (+ meta' di B10)
  di cui decido io            10
voci CHIUSE dalla verifica     2      le due ex-liste sulla patch della ripresa
```

**E il registro, misurato nello stesso giro** *(`doc/RAMIFICAZIONI.md`)*:
```
righe-voce                   138
  con un segnale ESPLICITO di apertura      24
  con un segnale ESPLICITO di chiusura      22
  con ENTRAMBI (ambigue)                    19
  MUTE (nessuno dei due)                    73      <- il 53 %
```
> **⚠ Le `73` mute non sono «73 voci aperte»: sono voci il cui stato NON SI LEGGE senza leggerle
> tutte.** È la misura, non il verdetto — e dice che **il registro non è interrogabile
> meccanicamente**.

---

## E — COSA LA VERIFICA HA CAMBIATO, **inclusi due errori miei**

**Tre correzioni all'elenco di partenza:**
1. **il blocco al 2700 NON è «mai diagnosticato»** — c'è un referto di 131 righe con sei ipotesi
   escluse **per misura**. Quello che manca è **lo stack**, non la diagnosi *(→ `B8`)*;
2. **i rami di `memoria_hebbiana_moto` sono `25`, non `23`**, e i `np.zeros` sono **`116`, non
   `~10`** — contati dal codice *(→ `B3`, `B4`)*;
3. **`--override-blob` non è nel driver vero**: il punto della ex-lista puntava al bersaglio
   sbagliato, e il bersaglio giusto è una **copia del driver che doveva essere stata rimossa**
   *(→ `B10`)*.

**Due errori MIEI, dichiarati:**
- ho riportato *«metriche chirali: 0 file»* e *«23 rami: 0 file»*. **Falso in entrambi i casi:** il
  mio `grep` usava `-e "a|b"` **senza `-E`**, quindi l'alternanza era cercata come testo letterale.
  **`doc/TASK_HISTORY/2026-09-20_metriche-settore-chirale.md` ESISTE** *(→ `A4`)*;
- le righe `:3517`-`:3526` che avevo citato **erano slittate di 106 righe** — è il §0 di
  `CLAUDE.md` *(«cerca per NOME, non per riga»)* applicato contro me stesso *(→ `A1`)*.

---

## F — UN PRESIDIO CHE ORA ESISTE DAVVERO: `py-spy`

`doc/REFERTO_blocco_run6000.md` §5 diceva: *«quello che servirebbe è banale e non ce l'ho:
`py-spy dump` legge lo stack di un processo vivo dall'esterno, senza toccarlo. Non è installato.»*

> **Installato oggi (`0.4.2`) ed ESERCITATO su un run VIVO**, non su un test:
> ```
> py-spy dump --pid 9264      (ramo A, mentre gira)
>   chiralita_core_locale (soliton_simulator.py:1556)
>   step (soliton_simulator.py:3624)
>   <module> (_scena_video.py:231)
> ```
> **`A9`: un presidio provato quando NON serve è un presidio; uno scritto e mai esercitato è una
> nota.** La volta scorsa il processo fu ucciso senza catturare lo stack, **e non si saprà mai**.

**PID dei due run in corso: ramo A `9264`, ramo B `30996`.**
**Se uno si pianta — soglia: più di ~1500 s senza uno snapshot nuovo — `py-spy dump` PRIMA di
qualunque altra cosa, e NON si uccide.**

---

## APERTO ab_sep4_A_e_B

- **avvio** `2026-09-20 16:26:43` · **blob** `b44f50ce` · **HEAD** `0f12645`
- **comando**
  ```
  ramo A (chi_basc ON, il default):
  python csv/_test_fork/_scena_video.py 500 csv/_test_fork/_ab_A --sep=4.0 --serie=20 --csv-progresso=csv/_test_fork/_ab_A/prog.csv
ramo B (chi_basc OFF):
  python csv/_test_fork/_scena_video.py 500 csv/_test_fork/_ab_B --sep=4.0 --serie=20 --csv-progresso=csv/_test_fork/_ab_B/prog.csv --chi-basc=off
  ```
- **note** A/B COMPLETO di chi_basc a sep=4.0, i DUE rami IN PARALLELO, 500 frame = 3000 passi ciascuno, uno snapshot ogni 20 frame = 120 passi = 25 per ramo. UNA sola voce per DUE processi perche' sono UN esperimento: un interruttore solo, tutto il resto identico. Geometria verificata alla semina: componenti = 1, archi massa-vuoto = 97590, massa-massa = 0. Disco: 14 GB liberi, stima 1.95 GB. CPU: 6 fisici, parallelo misurato 26.03 s/frame per ramo, stima 3.8-4.5 h. Driver 9aee4fc2, sigillo --chi-basc= 5/5.
- *2026-09-20 19:16:19* — RAMO B FERMATO alle 19:15:26 per decisione di Luca, al frame 65 di 500 (passo 390 di 3000). NON e chiuso l intero esperimento: il ramo A continua, quindi la voce resta APERTA e si chiudera quando A finisce. ARCHIVIO PARZIALE DI B INTATTO E VERIFICATO: 3 snapshot (120, 240, 360), nessun .tmp orfano, tutti caricabili, blob b44f50ce, e il passo nei DATI coincide col nome. MOTIVO: proiezione oltre 33 ore e in peggioramento. CATTURA FINALE PRIMA DELLO STOP, ed e il reperto piu importante dello stop stesso: nsub era passato da 206 a 15594, e IL VINCOLO VINCENTE ERA CAMBIATO -- n3 (|vd|) fermo a 205, ma n1 (la SORGENTE) esploso a 15594. Seconda fase della divergenza, che si sarebbe persa uccidendo senza catturare. File: csv/_test_fork/_diag_B/stack_FINALE_1915.txt

**chiuso 2026-09-20 20:21:06 — FINITO** ESITO ASIMMETRICO, e sono due esiti diversi non uno. RAMO A (chi_basc ACCESO): ARRIVATO INTATTO ai 3000 passi alle 20:20 circa. 500 frame, 28.014 s/frame medio, n da 2391 a 18000, archi 546792, coer_l finale 0.7324, dil +126.96 per cento. 25 snapshot su 25 scritti, 0 saltati, 0 FALLITI, 0.97 GB. Il costo per frame e cresciuto da 27.457 a 28.015, cioe del 2 per cento su 3000 passi: PIATTO. nsub restava 4, il pavimento. RAMO B (chi_basc SPENTO): FERMATO da Luca alle 19:15 al frame 65 di 500, passo 390 di 3000, con nsub a 15594 e proiezione oltre 73 ore. 3 snapshot intatti e verificati. LIMITE DA TENERE: UN SEME PER RAMO, quindi la differenza NON e attribuibile a chi_basc -- il nullo di un confronto fra bracci e la dispersione FRA SEMI, che questo esperimento non misura. Referti: REFERTO_ramoB_sottopassi_CFL, REFERTO_fuga_vd_ramoB, REFERTO_venti_archi_e_nsub, REFERTO_innesco_cinque, REFERTO_rigiocata_0_120. Voci: Z74 Z75 Z76 Z77, piu Z73 corretta in loco due volte.

## APERTO ramo_D_epoca2

- **avvio** `2026-09-21 10:15:20` · **blob** `26fa354d` (git) / `4954fe5b` (byte grezzi) · **HEAD** `ccf3aba`
- ⚠ **NOTA SUL BLOB, e vale per TUTTE le voci precedenti di questo file:** fino a oggi `_stato_run._blob_byte()` calcolava il blob **GIT** dichiarando di calcolare i **byte grezzi**. **Diceva l'opposto di cio' che faceva.** Nessun dato e' perso — un blob git si recupera con `git cat-file` — ma **l'etichetta era falsa**, e mandava chi verifica a cercare un oggetto nella convenzione sbagliata. **Corretto: ora si stampano ENTRAMBE.** Le voci storiche vanno lette come **blob GIT**.
- **comando**
  ```
  python csv/_test_fork/_scena_video.py 500 csv/_test_fork/_ab_D --sep=4.0 --serie=20 --csv-progresso=csv/_test_fork/_ab_D/prog.csv --chi-coop=on --scala-min=on --coes-adim=on
  ```
- **note** RAMO D -- EPOCA 2. Le TRE modifiche accese insieme (CHI_COOP, SCALA_MIN, COES_ADIM) piu' la cura del mondo-dopo-i-flag (categoria D, nessun flag). 500 frame = 3000 passi, uno snapshot ogni 20 frame = 120 passi = 25 snapshot. Sigillo 11/11 (d69e5bae sul simulatore 4954fe5b). PRESIDI PRIMA DEL LANCIO: componenti connesse = 1; min(d) = min(d0) = 0.800000000 = LAM, archi sotto LAM 0 e 0; mediana d/d0 = 1.000000 (nasce NON teso); n = 2391, archi = 525973; processi python vivi 0. DISCO: 5.9 GB liberi su 476, 99 per cento pieno -- il ramo A produsse 0.97 GB in 25 snapshot quindi D ci sta, MA IL MARGINE E' STRETTO. ⚠ NESSUN CONFRONTO CON A, B o C: sono epoca 1, e le letture di D vanno contro criteri ASSOLUTI. ⚠ E con tre interruttori accesi insieme nessun esito e' attribuibile a nessuno dei tre: i confronti legittimi verranno DOPO e DENTRO il sistema nuovo.
- *2026-09-21 11:29:33* — ⚠ FERMATO alle 11:05 al frame 205 di 500 (passo 1230) -- CONFIGURAZIONE SBAGLIATA, non una scelta: il driver NON inoltrava --scala-min e --coes-adim al simulatore. Letto DAL MODULO: CHI_COOP True ma SCALA_MIN False e COES_ADIM False. Le opzioni erano PARSATE e IGNORATE, in silenzio. py-spy dump catturato PRIMA dello stop (csv/_test_fork/_diag_D/stack_STOP_config_sbagliata.txt). Archivio parziale INTATTO e verificato: 10 snapshot (120..1200), tutti caricabili, 0 .tmp orfani.

**chiuso 2026-09-21 11:29:33 — FERMATO** NON E' IL RAMO D: e' un run con CHI_COOP acceso e SCALA_MIN/COES_ADIM spenti, su blob di epoca 2 -- cioe' la COOPERAZIONE da sola. I dati parziali NON si buttano (10 snapshot leggibili, 120..1200 passi) ma NON rispondono alla domanda del mandato perentorio, che chiede le TRE modifiche insieme. CAUSA: la patch al driver usava str.replace con un solo assert GLOBALE, soddisfatto dalle ALTRE sostituzioni; la terza non ha attaccato in silenzio. Nessun sigillo poteva prenderlo: quelli esistenti costruiscono sys.argv da soli e NON passano dal driver. Presidio nuovo: csv/_seal_fork/_sigillo_flag_driver.py. IL RAMO D VA RILANCIATO DA ZERO dopo che il sigillo passa.

## APERTO ramo_D_epoca2_bis

- **avvio** `2026-09-21 11:32:04` · **blob** `26fa354d (git) / 4954fe5b (byte grezzi)` · **HEAD** `ec41deb`
- **comando**
  ```
  python csv/_test_fork/_scena_video.py 500 csv/_test_fork/_ab_D --sep=4.0 --serie=20 --csv-progresso=csv/_test_fork/_ab_D/prog.csv --chi-coop=on --scala-min=on --coes-adim=on
  ```
- **note** RAMO D, SECONDO LANCIO -- il primo (10:15-11:05) girava con SCALA_MIN e COES_ADIM SPENTI perche' il driver non li inoltrava: difetto trovato, riparato, e coperto dal presidio nuovo csv/_seal_fork/_sigillo_flag_driver.py (3/3: ogni opzione arriva al MODULO in entrambi i versi, e l'elenco delle opzioni e' SCOPERTO dal sorgente invece che scritto a mano). Il driver e' ora 5544f3b9 -> riparato. L'archivio del primo lancio e' conservato in csv/_test_fork/_ab_C_solo_chicoop_FERMATO (10 snapshot, 120..1200, tutti leggibili): NON e' il ramo D, e' la COOPERAZIONE da sola su blob di epoca 2. Questa volta il primo controllo dopo l'avvio e' il blocco FLAG ATTIVI letto DAL MODULO.
- *2026-09-21 12:57:51* — ⚠ DIVERGENZA: nsub = 22591 contro il pavimento 4, catturato con py-spy dump --locals sul PID 19912 (PROCESSO NON UCCISO). Il vincolo vincente e' n1 = 22591 (la SORGENTE), mentre n3 = 3 e n2 = 1: NON e' |vd| a esplodere. Stessa firma del ramo B, ma li' chi_basc era SPENTO e qui e' ACCESO con le tre modifiche attive. Il processo calcola (8.4 s CPU su 12 s reali): e' LENTO, non morto. Ultimo dato pulito: frame 185 a 20.537 s/frame; ultimo snapshot su disco: passo 1080 (9 file). A questo nsub i 315 frame restanti sono GIORNI. Referto: doc/REFERTO_nsub_ramoD.md, voce Z90.

**chiuso 2026-09-21 13:14:20 — FERMATO** Fermato al frame 205 di 500 (passo 1230) dopo py-spy dump. nsub = 22591 con n1 = 22591 (la SORGENTE), n2 = 1, n3 = 3: a quel ritmo i 295 frame restanti erano GIORNI. ARCHIVIO INTATTO: 10 snapshot (120..1200), tutti apribili, zero .tmp orfani, ed e arrivato anche il 1200 che al momento della diagnosi mancava. I DATI SERVONO e sono gia analizzati: csv/_analisi_ramoD.py, output in csv/_test_fork/_diag_D/ANALISI_ramoD_2026-09-21.txt. RISULTATO PRINCIPALE: i due flag hanno INVERTITO il regime rispetto al solo CHI_COOP -- da TENSIONE con d0 inchiodato a 0.83 e 55909 archi sotto LAM, a COMPRESSIONE con d0 a 30 e ZERO archi sotto LAM. E peq CROLLA di 14 ordini (1.38e-14 al passo 1200) subito prima dell esplosione di n1.

## APERTO run_S_solo_scalamin

- **avvio** `2026-09-21 13:25:11` · **blob** `26fa354d (git) / 4954fe5b (byte grezzi)` · **HEAD** `5ab29e6`
- **comando**
  ```
  python csv/_test_fork/_scena_video.py 50 csv/_test_fork/_run_S --sep=4.0 --serie=10 --csv-progresso=csv/_test_fork/_run_S/prog.csv --chi-coop=on --scala-min=on --coes-adim=off
  ```
- **note** §1 del mandato: CHI DEI DUE fa scappare d0. RUN S = SOLO SCALA_MIN (COES_ADIM SPENTO), 50 frame = 300 passi. TRACCIA_D0 va acceso a mano nel driver? NO: si accende dal simulatore, e il driver non lo passa -- verificato, quindi questo run misura d0 SENZA la traccia per scrittore. LETTURE FISSATE PRIMA: se d0 scappa solo in S -> e' il CRICCHETTO di SCALA_MIN; solo in K -> e' il contrappeso perso di COES_ADIM; in entrambi -> tutte e due; in nessuno -> e' l'INTERAZIONE. Uno alla volta, MAI in parallelo.

**chiuso 2026-09-21 14:31:19 — FINITO** 50 frame = 300 passi, 17.340 s/frame, 5 snapshot su 5, 0 falliti, 0.18 GB. RISULTATO: d0 NON SCAPPA con SCALA_MIN da solo -- med d0 resta 0.89, 0.81, 0.80, 0.80, 0.81 mentre med d cresce da 1.02 a 2.03 e d/d0 sale a 2.48 (TENSIONE). E ZERO archi sotto LAM a ogni snapshot, contro i 55909 del ramo C senza i due flag: SCALA_MIN fa il suo mestiere SENZA far scappare d0. Il cricchetto DA SOLO non spiega la fuga del ramo D.

## APERTO run_K_solo_coesadim

- **avvio** `2026-09-21 14:31:36` · **blob** `26fa354d (git) / 4954fe5b (byte grezzi)` · **HEAD** `6981a0f`
- **comando**
  ```
  python csv/_test_fork/_scena_video.py 50 csv/_test_fork/_run_K --sep=4.0 --serie=10 --csv-progresso=csv/_test_fork/_run_K/prog.csv --chi-coop=on --scala-min=off --coes-adim=on
  ```
- **note** §1 del mandato, SECONDO run: K = SOLO COES_ADIM (SCALA_MIN SPENTO), 300 passi. Il run S ha gia' ESCLUSO il cricchetto da solo: con SCALA_MIN acceso e COES_ADIM spento, med d0 resta ~0.80 piatto. LETTURA FISSATA PRIMA: se d0 scappa in K -> e' il CONTRAPPESO PERSO di COES_ADIM; se non scappa nemmeno in K -> e' l'INTERAZIONE fra i due, e va detto cosi'. Uno alla volta.

**chiuso 2026-09-21 15:20:16 — FINITO** 50 frame = 300 passi, 20.711 s/frame, 5 snapshot su 5, 0 falliti, 0.18 GB. RISULTATO: d0 in K CRESCE ma piano -- da 0.9728 a 1.3124, cioe' x1.35 su 300 passi -- mentre in S resta piatto (x0.91) e in D scappa (x15 su 1080 passi, e gia' a 2.02 al passo 120 quando K e' a 0.997). NESSUNO DEI DUE FLAG DA SOLO RIPRODUCE LA FUGA: e' l'INTERAZIONE, ed e' la terza possibilita' fissata PRIMA. E K ha d/d0 ~1.2, il piu' vicino alla trasparenza fra tutte le configurazioni, ma con 71114 archi sotto LAM perche' SCALA_MIN e' spento.
