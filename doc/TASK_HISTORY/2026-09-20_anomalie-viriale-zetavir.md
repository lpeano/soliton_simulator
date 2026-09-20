# TASK HISTORY — le quattro anomalie di `VIRIALE` e `ZETA_VIR`. Si curano tutte

**Data** 2026-09-20 · **branch** `fork-su2` · **HEAD** `a3ac521` · **blob** `775ceab7`
(sha1 dei BYTE GREZZI, convenzione `_presidio`; blob git `775ceab7` — **qui le due coincidono**,
e non sempre: vedi `CLAUDE.md` §5-quinquies) · albero **pulito** · **nessun processo in esecuzione**.

> **RUN E TEST FERMI. Si cura PRIMA di raccogliere altri dati.**
> **Il lavoro gia' fatto NON si reverte: si somma.** Il driver con `--sep` nominale e la ripresa
> restano, **sigillati `4/4` e `5/5`** (`a3ac521`), e serviranno quando il run ripartira' **su un
> simulatore curato**. **Il run da 10.000 passi NON e' mai partito:** `_g10000` non esiste.

---

## 1. I DUE CHIARIMENTI CHE GOVERNANO TUTTO, e li scrivo prima di ogni altra cosa

**① SI CURANO TUTTE, anche quelle che oggi non scattano mai.** Una guardia che salta in silenzio e
un default non dichiarato sono difetti **PER FORMA, non per frequenza** — `A8`: *un ramo silenzioso
non e' un ramo*. **I contatori servono a MISURARE quanto mordono, MAI a decidere se curare.**
Il precedente e' `Z25`, tenuto **nonostante** l'A/B non mostrasse alcun effetto.

**② LE CORREZIONI VANNO OVUNQUE lo stesso schema compaia.** **L'elenco del mandato e' il punto di
partenza, non il perimetro.**

## 2. LE QUATTRO ANOMALIE — **righe VERIFICATE DAL DISCO**, non ricopiate

```python
# (1) LA SCALA NASCOSTA -- A1
:4425   r_rad = ampiezza                                   NON limitata
:4426-4429   t_tan = np.tanh(...)                          limitata in [0, 1)
:4430   H = np.maximum(np.hypot(r_rad, t_tan), 1e-9)
:4431-4432   cos2 = (r_rad/H)**2 ;  sin2 = (t_tan/H)**2
:4437   radiale = grav * cos2
# (2) LA GUARDIA CHE SALTA IN SILENZIO -- A8, DUE occorrenze
:3678   if ZETA_VIR and self._sin2_vir is not None and len(self._sin2_vir) == len(beta):
:3715   if ZETA_VIR and self._sin2_vir is not None and len(self._sin2_vir) == len(beta_new):
# (3) IL DEFAULT SILENZIOSO
:4434-4435   s2full = np.zeros(len(self.i)) ;  s2full[mask] = sin2
```

**`tanh` satura a `1`: la ripartizione confronta `ampiezza` CONTRO UNO**, e quell'uno **non e'
dichiarato e non e' derivato**. **Se `ampiezza >> 1` allora `sin2 -> 0` e la conversione virale non
avviene mai.** **Gli archi fuori dal `mask` prendono `sin2 = 0`, cioe' FRENO PIENO: una decisione
fisica presa da un `np.zeros`.**

**(4) LO SFASAMENTO:** `_sin2_vir` e' **scritto** in `memoria_hebbiana_moto` e **letto** in `step`;
nel ciclo `step` viene **prima**, quindi `beta` usa il `sin2` del passo **precedente**.
**Probabilmente corretto (`A6` vuole lo stato precedente), ma non e' scritto. Va verificato e
dichiarato.**

## 3. L'ORDINE DEL LAVORO, e cosa decide ogni passo

**§1 LA SCANSIONE PRIMA DI TUTTO** — si cerca **in tutto il simulatore**, dal disco:
- **ogni `len(X) == len(Y)`** che, fallendo, **salta una legge senza contarlo** *(schema ②)*;
- **ogni `np.zeros`/`np.full` usato come DEFAULT FISICO su una maschera parziale** *(schema ③)*;
- **ogni saturazione** (`tanh`, `x/sqrt(1+x^2)`, `clip`) **confrontata con una grandezza NON
  limitata** *(schema ①: la scala implicita e' il punto di saturazione)*;
- **ogni memoria `self._*` scritta in una funzione e letta in un'altra** senza ordine dichiarato
  *(schema ④)*.

**Si riporta l'ELENCO COMPLETO con le righe, e si STOP.** **Se una famiglia ha dieci occorrenze si
curano tutte e dieci, o si dichiara perche' no, caso per caso.**

**Poi, una cura alla volta, ciascuna col suo sigillo:**
1. **I CONTATORI (②③)** — **byte-inerti**, committati e girati **prima**. **Dicono QUANTO mordono,
   non SE curare**, e restano come presidio permanente;
2. **④ LA DICHIARAZIONE** — si verifica l'ordine e si scrive nel docstring. **Zero cambi di
   comportamento;**
3. **① LA SCALA** — si **misura `ampiezza` (percentili) PRIMA**. La scala dev'essere **DERIVATA da
   una grandezza di stato** (`A1`), non presa. **Il precedente vincente e' `cs_floor`:
   `GAMMA = 0.05` → `Lam = mean(I)`, fattore 1300.**
   **⚠ La mediana di `ampiezza` stessa sarebbe `A3`** *(normalizzazione sul proprio insieme)*:
   **se la propongo, lo DICO.** **E «nessuna scala derivabile» e' un esito valido;**
4. **②③ LE CURE** — la guardia **o funziona o DICHIARA, mai il silenzio**; il default fuori dal
   `mask` **giustificato o cambiato, e la scelta DERIVATA;**
5. **LE ALTRE OCCORRENZE** del §1, **con lo stesso criterio.**

## 4. I SIGILLI, per ciascuna cura
- **X0** riferimento **`775ceab7`**, **BYTE GREZZI** (`sha1`), **mai `git hash-object`** (C18);
- **X1 — riduzione al limite, BLOCCANTE:** forzando la scala nuova al valore implicito `1`,
  **BYTE-IDENTICO**. **Forma algebrica binariamente esatta;**
- **X2 — controllo positivo:** coi valori veri **DEVE** differire;
- **X3 — `A8`:** i contatori a **~0 %** dopo la cura, **o dichiarati;**
- **X4 — LA CONVERSIONE AVVIENE:** **`sin2` ai percentili prima e dopo.** **Se era ~0 e resta ~0,
  la cura non ha fatto quello che doveva;**
- **X5 — L'EFFETTO SU `L`:** il momento angolare netto *(il commento di `L_CONSERVA` cita
  `L_z ~ -0.9`, verso coerente all'84 %)*. **Cambia? Di quanto?**
- **X6 — stabilita':** no NaN/runaway, CFL < 1, `|nb| = 1`;
- **X7 — SI RIGIRANO TUTTI i sigilli del giro. Se uno si muove, e' un reperto.**

## 5. COSA MI FA FERMARE
- **la scansione che trova una famiglia numerosa** → **si riporta l'elenco e si aspetta**, invece di
  curare venti punti in un commit solo (§1 del par.1 di `CLAUDE.md`: un interruttore alla volta);
- **`X1` che non e' byte-identico** → **la forma algebrica non e' esatta: si riscrive, non si
  allenta la soglia;**
- **nessuna scala derivabile per ①** → **lo si dichiara**, e la cura di ① **non si fa**;
- **`X4` che resta a zero** → **la cura non ha fatto quello che doveva, e va detto.**

## 6. COSA NON SI TOCCA
**`L_CONSERVA`** — e' altra cosa: rimuove la rotazione spuria del rilassamento, e azzerava la
precessione vera. **Fuori dal mandato.**

## 7. TODO DEL NEXT STEP
1. [fatto] blob/branch dal disco; righe del mandato **verificate**;
2. **la SCANSIONE dei quattro schemi in tutto il simulatore** → **elenco completo con le righe**;
3. **STOP e riporto.**
