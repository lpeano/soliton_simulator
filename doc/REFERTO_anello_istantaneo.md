# REFERTO — **L'anello istantaneo è rotto. `10/10`. E il metro resta ballerino**

**Data:** 2026-09-18 · **Blob** `f8f46683` → **`a1ae5090`** *(sha1 dei BYTE GREZZI, non
`git hash-object`: C18)* · 1 seme (5), 120 passi
**Task history pushato PRIMA:** `fd198ba` · **Previsioni pushate PRIMA della cura:** `631ff15`
**Cura:** `c6630fc` · **FAIL committato:** `c818208` · **Correzione:** `24…` · **Sigillo 10/10:** `b98c5d1`

---

## 0. IL VERDETTO

1. **Il difetto era ESATTO, non approssimato:** `max|median(x) − 1| = **0.000e+00**` su **122 passi**.
   **A3 non era «quasi» violato: lo era a macchina.**
2. **È rotto:** dopo la cura `median(x)` ha `p05 0.326`, `mediana 0.976`, `p95 2.997`,
   **`max|med−1| = 12.49`**.
3. **`P1` è una BYTE-IDENTITÀ VERA** — `444` nodi **contro** `444`, **7 array su 7 con shape uguali**,
   `max|A-B| = 0.000e+00`. **Non è «nessun confronto»: la riga delle shape lo dimostra.**
4. **⚠ E `Z33` non è sparita: si sarebbe ROVESCIATA** — l'avevo previsto, e **la cura si porta dietro
   il presidio che lo impedisce**, che ha sparato **2 volte su 2**.
5. **⚠ Il metro resta BALLERINO**, ed è un **fronte nuovo**: l'anello è rotto, ma la dispersione del
   `62 %` di `median(|f|)` **ora passa dentro `r`** invece di essere divisa via.

---

## 1. IL DIFETTO, e quanto era esatto

```python
med = max(float(np.median(np.abs(f))), 1e-9)     # calcolato DA f
x   = f / med                                     # e usato SU f
```

**A6** — `f` e `r` si determinavano a vicenda **dentro** il passo. **A3** — `median(x) = 1` per
identità. **Due assiomi nella stessa riga.**

```
PRIMA  max|median(x) - 1| = 0.000e+00   su 122 passi (esclusi i 2 degeneri di Z33)
DOPO   p05 0.325981   mediana 0.975909   p95 2.996750   max|med-1| = 12.493
```

> **Non era «circa un punto fisso»: era ESATTO A MACCHINA.** Ed è la ragione per cui `P4`
> (l'ex-presidio *«una grandezza normalizzata sulla propria mediana non può muoversi»*) **si
> applicava a `ritmo()` alla lettera.**

## 2. LA CURA — **il riferimento non cambia, cambia QUANDO lo si legge**

`median(|f|)` resta il gauge. **Nessun gauge nuovo, nessun numero tarato, nessun flag** *(categoria
D del par.10: un bug curato non ha un interruttore)*.

### 2.1 ⚠ Il presidio che regge tutto: **`ritmo()` NON scrive lo snapshot**

**Verificato dal disco, e nessuno l'aveva nominato:** `ritmo()` ha **TRE call-site**, e **due sono
diagnostici**:

```
:3124   r   = self.ritmo()     <- LA FISICA, dentro step()
:6263   tau = net.ritmo()      <- _diag_completa   (DIAGNOSTICO)
:6921   tau = net.ritmo()      <- DIAGNOSTICO
```

**Se lo snapshot avanzasse dentro `ritmo()`, ogni chiamata diagnostica farebbe avanzare lo stato
fisico** — par.2.3 violato, e **sarebbe il QUINTO difetto di questa famiglia.**

| chi | cosa fa |
|---|---|
| `ritmo()` | **LEGGE** `_med_f_prec` *(mai lo scrive)* e **REGISTRA** `_med_f_ultimo` |
| `step()` (`:3129-3131`) | **PROMUOVE** `_med_f_prec = _med_f_ultimo`, accanto a `_psi_prec` e `_psi_spin_prec` |

> **La contaminazione da diagnostico è chiusa PER COSTRUZIONE, non per attenzione:** un diagnostico
> può sovrascrivere `_med_f_ultimo`, ma **`step()` chiama `ritmo()` PRIMA di promuovere** — quindi il
> valore promosso è **sempre** quello della chiamata fisica.

### 2.2 ⚠ E il mandato citava `Z33` col segno rovesciato

Il §2 diceva *«`Z33` è nata così: `_psi_spin_prec` aggiornato DOPO il consumo»*. **`680d069` ha
misurato il contrario:** promuovere **dopo** il consumo **è ciò che fa valere A6**; promuoverlo
prima confronterebbe lo stato con sé stesso, **`f = 0` sempre**.
**Quindi il pattern di `:3129-3131` è quello da SEGUIRE, ed è quello che ho seguito.**

### 2.3 Uno SCALARE, non l'array — **A8b chiusa per costruzione**

`med` **non ha lunghezza**: l'estensione a `mitosi`/`semina`/`nuova_massa` **non serve**.
**È il presidio più forte disponibile**, ed è esattamente ciò che è mancato a `_cs_nodo_prev`
(fallback **71.88 %**) e `_psi_spin_prec` (**95.33 %**).
**A3c/A8b quarto livello:** `med_prec` e `f` sono **entrambi `Δangle/DT`, cioè `[1/T]`** —
**confrontabili**, non solo presenti.

### 2.4 Il primo passo — convenzione **riusata**, non inventata

`_med_f_prec` assente → **`np.ones(n)`**, la stessa convenzione già presente in `ritmo()` a
`:2021-2026` quando manca `_psi_prec` *(«non esiste un prima» = «nessuna dilatazione»)*, **e si
conta**. **⚠ Il fallback NON è `median(|f|)` corrente: sarebbe il difetto stesso, al passo 1.**

### 2.5 ⚠ Il presidio che la MISURA ha imposto: **non si promuove un `med` sul pavimento**

`1e-9` **non è una misura: è la protezione da divisione per zero.** Promuoverlo renderebbe **la
regolarizzazione il gauge del passo dopo** — *«alle scale simulabili la regolarizzazione diventa il
parametro fisico»* (par.9).

**Quanto sarebbe costato, misurato PRIMA:** il rapporto `med_t/med_{t-1}` ha **`max = 4.81e+07`**, ed
è **esattamente il passo che segue un gauge degenere**. **Senza questo ramo `Z33` non sarebbe sparita:
si sarebbe ROVESCIATA**, da *«tutti sul pavimento»* a *«tutti in saturazione `r ≈ √2`»*.
**Misurato dopo: `med sul pavimento 2`, `med NON promosso 2`. Ha sparato 2 volte su 2.**

---

## 3. IL SIGILLO — `10/10`

| | esito | il numero |
|---|---|---|
| **P0** | PASS | vecchio `f8f46683` (atteso), nuovo `a1ae5090` |
| **P1** *(bloccante)* | **PASS** | **`n: 444 contro 444`**, 7 array su 7 **shape uguali**, `max|A-B| = 0.000e+00` |
| **P2** | PASS | `n: 444 contro 459`, 7 shape divergenti: **coi valori veri il sistema cambia** |
| **P3** | **PASS** | `max|median(x)−1| = 12.493` — **il punto fisso esatto è sciolto** |
| **P4** | PASS | `ritmo()` scrive `_med_f_prec`: **False** · `step()` promuove: **True** |
| **P5** | PASS | 126 chiamate · assente **2** (1.59 %) · identico **0** · non promosso **2** |
| **P6** | PASS | `med` sul pavimento **2**, non promosso **2** — **intercettati tutti** |
| **P7** | PASS | tetto **1.4142130** contro `1.41419`: **non si è spostato**. ⚠ **pavimento: `1.41421e-06` contro `1.293e-04` — ORA SI TOCCA** |
| **P8** | PASS | `TAU_A = 50`; `ramp` **0.0002 / 0.00981 / 0.01962** — **riportato, NON confrontato** |
| **P9** | PASS | no NaN/inf, `r > 0`, `||nb|−1| < 1e-6` |

**⚠ `P1` valida anche il wrapper:** se avessi ricostruito `f` male nel sigillo, **P1 sarebbe
fallito.** Il `0.000e+00` con shape uguali **prova entrambe le cose insieme.**

### 3.1 ⚠ E il sigillo è FALLITO al primo giro, per un difetto MIO — committato prima di aggiustare

**`c818208`: P0, P1, P2 FAIL.** Il sigillo estraeva il blob di riferimento con
`git cat-file -p HEAD:soliton_simulator.py` — **ma `HEAD` era già il commit della cura**:
**ho confrontato il codice curato con sé stesso.**

> **E `P2` dava `max|A-B| = 0.000e+00` con SHAPE UGUALI — la trappola già catalogata, col segno
> ROVESCIATO:** là lo zero era **mancanza di confronto**, qui era **identità perfetta per la ragione
> sbagliata.** **La riga delle shape, stampata per prima, l'ha reso leggibile in un colpo d'occhio:
> `n: 459 contro 459`.**

**È un difetto di STRUTTURA, non una svista:** un riferimento ancorato a `HEAD` **si sposta col
lavoro**. È la stessa ragione per cui **il gate è ancorato al BLOB e non al commit** (par.2.6).
**Corretto in un commit dedicato, dopo aver committato il fallimento** (par.5).

---

## 4. ⚠ IL FRONTE NUOVO — **il metro resta ballerino**

L'avevo scritto **prima di misurare** (task history `fd198ba`, §1.6) e **prima di cablare**
(previsione 5, `631ff15`):

```
median(|f|) : oscilla del 62 % fra passi (std/med 0.6234)
median(x) dopo la cura : p05 0.326   mediana 0.976   p95 2.997
```

> **L'anello è rotto — A6 e A3 sono a posto — ma la dispersione del gauge NON viene più divisa via:
> PASSA DENTRO `r`.** Il nodo tipico non è più inchiodato a `x = 1`, **e questo è il punto della
> cura**; ma ora **oscilla di un fattore ~9 fra il 5° e il 95° percentile.**

**E si vede nel codominio:** il **pavimento assoluto `1.414e-06` ORA SI TOCCA** (prima: `min 1.293e-04`).
**Il tetto non si è spostato** — `r_unit` e la forma sono intatti — **ma la popolazione arriva ai
bordi.**

**Non è un'obiezione alla cura** *(A6 non è negoziabile, e un punto fisso esatto è peggio di un metro
mobile)* **ma è un fatto nuovo, e va deciso:** *un gauge che oscilla del 62 % fra passi è il metro
che vogliamo?* **È la stessa domanda di `Z36`, spostata di un livello.**

## 5. COSA NON HO FATTO

Non ho cambiato il riferimento, non ho introdotto sotto-passi, non ho salvato un array, **non ho
toccato** il `+1e-6`, il `max(...,1e-9)`, `x/sqrt(1+x²)`, `TAU_LOC`, `r_unit`. **Nessun flag**
(categoria D). **`P8` non confronta** i propri numeri con `0.0002/0.0102/0.0212`: quelli sono di
un'**altra scena** (A3c).

## 6. I LIMITI

Un seme, 120 passi, una scena. **`P8` non dimostra né miglioramento né peggioramento su `Z9`:** la
previsione 6 diceva di aspettarsi uno scarto **dentro la dispersione fra semi (~3 %)**, quindi **non
interpretabile su un seme** — servirebbero **≥ 4 semi** (P3/C10). **Il presidio del pavimento è stato
esercitato 2 volte in questa scena**: poche, e il numero è **di questa scena**.
