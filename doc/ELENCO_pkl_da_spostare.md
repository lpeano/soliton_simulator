# I `.pkl` DA SPOSTARE SU `E:` — **l'elenco ANNOTATO, e le domande aperte**

> **§1 del mandato dello spostamento.** **Nessun byte copiato, cancellato o modificato.**
> Prodotto il 2026-09-21 mentre il **ramo D gira** (`PID 19912`): la cartella `csv/_test_fork/_ab_D`
> **non e' stata attraversata**, nemmeno in lettura.
> **`.pkl` TRACCIATI da git: ZERO** — nessun conflitto con `git ls-files`.

---

## 1. IL QUADRO — **e non e' un elenco piatto: sono TRE categorie**

```
                                      cartelle   file        MB
  ARCHIVIO, documentato in INVENTARIO      17     202       5430
  ARCHIVIO, NON documentato                21     100       1755     <-- il gruppo che pesa
  SCRATCH di sigilli, rigenerabile          4       7        144
                                                 ----    -------
  TOTALE                                           309       7328
```

### ⚠ La riga che conta e' la seconda
**1755 MB di `.pkl` NON hanno il comando che li rigenera.** Il par.5-quinquies li chiama
**«un dato che nessuno potra' rifare»**. **Per questi lo spostamento non e' liberare spazio: e'
l'unica forma di conservazione disponibile** — e cancellarli, oggi, sarebbe irreversibile.
**Per i 5430 MB documentati, invece, lo spostamento e' una comodita': il comando c'e'.**

### ⚠ E la terza categoria NON andrebbe spostata affatto
**144 MB sono SCRATCH che un sigillo committato ricrea da solo.** Spostarlo significa
**archiviare per sempre qualcosa che si rifa' in due minuti**, e occupare `E:` con rumore.
**La mia proposta e' cancellarlo, non spostarlo — ma NON l'ho fatto: decide Luca.**

---

## 2. L'ELENCO, cartella per cartella

| cartella | file | MB | in `INVENTARIO` | categoria |
|---|---:|---:|---|---|
| `csv/_test_fork/_g6000` | 45 | 1313.6 | si' | archivio |
| `csv/_test_fork/_ab_A` | 25 | 923.0 | si' | archivio |
| `csv/_test_fork` | 36 | 631.7 | si' | archivio |
| `csv/_seal_fork` | 24 | 428.7 | si' | archivio |
| `csv/_test_fork/_ab_C_solo_chicoop_FERMATO` | 10 | 345.8 | **NO** | archivio |
| `csv/_test_fork/_fin_B` | 11 | 308.3 | **NO** | archivio |
| `csv/_test_fork/_fin_A` | 10 | 272.4 | si' | archivio |
| `csv/_test_fork/_gvideo` | 6 | 271.1 | si' | archivio |
| `csv/_seal_fork/_ab_grav_ampiezza/B` | 9 | 253.5 | si' | archivio |
| `csv/_seal_fork/_ab_coppia_reciproca/B` | 9 | 253.5 | si' | archivio |
| `csv/_seal_fork/_ab_coppia_reciproca/A` | 9 | 252.7 | si' | archivio |
| `csv/_seal_fork/_ab_grav_ampiezza/A` | 9 | 252.7 | si' | archivio |
| `csv/_test_fork/_g2m` | 6 | 193.9 | si' | archivio |
| `csv/_test_fork/_g1200` | 7 | 147.6 | si' | archivio |
| `db/deparam_probe` | 13 | 146.7 | **NO** | archivio |
| `db/tw_spinore` | 6 | 110.0 | **NO** | archivio |
| `csv/_test_fork/_ab_B` | 3 | 104.9 | si' | archivio |
| `db/freetest` | 8 | 96.7 | **NO** | archivio |
| `csv/_seal_53c` | 5 | 85.9 | **NO** | archivio |
| `csv/_test_fork/_pilota6000scena` | 3 | 84.0 | **NO** | archivio |
| `db/fase3_cov` | 6 | 79.2 | **NO** | archivio |
| `db/sync_spinore` | 6 | 71.7 | **NO** | archivio |
| `csv/deparam_bracci` | 6 | 66.8 | **NO** | archivio |
| `csv/_test_53c` | 3 | 53.7 | **NO** | archivio |
| `db/sync_spinore_step2` | 4 | 47.2 | **NO** | archivio |
| `csv/_seal_fork/_sig_drv_B` | 1 | 46.5 | **NO** | scratch |
| `db/deparam_pilota_chi` | 2 | 44.0 | **NO** | archivio |
| `csv/_seal_fork/_sig_flag_driver/run` | 1 | 43.6 | si' | scratch |
| `csv/_seal_fork/_sig_drv_A` | 1 | 43.6 | **NO** | scratch |
| `csv/_test_fork/_costo_sep4/P1` | 1 | 34.7 | si' | archivio |
| `csv/_test_fork/_costo_sep4/P2` | 1 | 34.7 | si' | archivio |
| `csv/_test_fork/_costo_sep4/S1` | 1 | 34.7 | si' | archivio |
| `csv/_test_fork/_pilota_sep_4p0` | 1 | 34.7 | **NO** | archivio |
| `csv/_seal_k2` | 3 | 33.7 | **NO** | archivio |
| `csv/_seal_fase2` | 3 | 33.3 | **NO** | archivio |
| `csv/_seal_chibasc` | 3 | 33.1 | **NO** | archivio |
| `csv/_test_fork/_pilota6000` | 1 | 26.4 | si' | archivio |
| `db/deparam_pilota_sfo` | 2 | 22.8 | **NO** | archivio |
| `db/deparam_pilota` | 2 | 22.8 | **NO** | archivio |
| `csv/deparam_pilota_k2` | 2 | 22.7 | **NO** | archivio |
| `db/deparam_segno` | 1 | 11.6 | **NO** | archivio |
| `csv/_seal_fork/_tmp_coorti` | 4 | 9.9 | **NO** | scratch |

---

## 3. LE DUE DOMANDE APERTE — **e il mandato non le decide**

### ① Le cartelle di lavoro dei sigilli
Il §0 del mandato dice **«SI SPOSTA ogni `.pkl`»** *e* **«NON SI TOCCA: cartelle di lavoro dei
sigilli, restano dove sono»**. Le due frasi si contraddicono su **1156 MB**.
**Proposta:** lo scratch rigenerabile **si cancella**; le due `_ab_*` da ~506 MB **si spostano**,
perche' NON sono in inventario e quindi non si rifanno.

### ② `_ab_C_solo_chicoop_FERMATO` (346 MB)
**Non e' un archivio «vecchio»: e' di stamattina**, ed e' il run del ramo D fermato perche' girava
con la configurazione sbagliata. **Non e' stato ancora letto da nessuno.**
**Domanda:** si sposta come gli altri, o resta su `C:` finche' non si decide se merita un referto?

---

## 4. IL COSTO DEL METODO, detto PRIMA

Il §2 impone **copia -> verifica `sha1` + caricamento -> cancella**, uno alla volta. Su **309 file
e 7.2 GB** significa **decomprimere 7.2 GB di gzip** e fare `pickle.load` su ognuno.
**E' lo stesso carico che il 20/9 ha portato il ramo B da 25 a 84 s/frame.**
**Lo faro' sequenziale e sorvegliato** — `s/frame` di D letto ogni pochi file, e **stop se sale** —
**ma va messo in conto: questa operazione costa tempo al ramo D.** **Il modo per non pagarlo e'
farla a run finito.**

---

## 5. SPAZIO

```
PRIMA       C:  3.8 GB liberi        E:  238 GB liberi (633 MB usati)
PROIEZIONE  C: ~11 GB liberi         E: ~7.9 GB usati
```
