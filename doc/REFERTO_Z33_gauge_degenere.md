# REFERTO — **`Z33` NON è un difetto del gauge: è un difetto di ORDINE/SNAPSHOT. E il mandato aveva il segno sbagliato**

**Data:** 2026-09-18 · **Blob** `72acd6aa` (git) / `aa84755b` (byte) · un seme (5), 126 passi
**Task history scritto e pushato PRIMA:** `aff0df6` · **Strumento:** `csv/_test_fork/_gauge_degenere.py`
**NESSUNA CURA.** Le tre misure del §2 e lo STOP.

---

## 0. IN QUATTRO RIGHE

1. **Le degeneri sono nel percorso fisico**: `126/126` invocazioni vengono da **`step()`**, nessun
   diagnostico. **La quinta lettura (artefatto della sonda) è esclusa.**
2. **Ma NON sono un difetto del gauge.** `f` non ha *mediana piccola*: è **identicamente nullo**, e
   la causa è **lo snapshot confrontato con sé stesso**. **Il pavimento `1e-9` non c'entra.**
3. **È TRANSITORIO**: passi **0, 1, 6, 7**. **Zero dopo il passo 20.**
4. **⚠ E il mandato aveva il segno sbagliato:** prevedeva `r → ±1` (`x → ∞`). Misurato: **`x = 0`,
   `r → 1.414e-06`** — **il tempo si ferma, non accelera.**

---

## 1. (A) IL CHIAMANTE — **percorso fisico, non diagnostico**

```
TUTTE le invocazioni, per chiamante : step=126
le DEGENERI, per chiamante          : step=4
```

**Nessuna chiamata da `stato_crossover` né dai diagnostici a `:6232`/`:6890`.** Le degeneri
**alimentano `dt_n` e quindi `eta`.** **La lettura «è un artefatto della sonda» è esclusa.**

## 2. (B / 2.1) COSA COLLASSA — **`f` identicamente nullo, non «mediana piccola»**

| passo | n | ramo | frazione `f=0` | `max\|f\|` | `snap ==` | `len ps/psp` |
|---|---|---|---|---|---|---|
| **0** | 80 | 2π | **1.0000** | 0 | **True** | 80 / **−1** |
| **1** | 80 | 4π | **1.0000** | 0 | **True** | 80 / 80 |
| **6** | 440 | 2π | **1.0000** | 0 | **True** | **440 / 80** |
| **7** | 440 | 4π | 0.9818 | **3.55e-13** | False | 440 / 440 |

**`f` IDENTICAMENTE NULLO in 3 casi su 4.** Il quarto (passo 7) ha `max|f| = 3.55e-13`, cioè **zero
numerico**, non valori veri.

> **La terza alternativa della 2.1 — «mediana nulla con valori non nulli» — è ESCLUSA.**
> **E con essa cade l'idea che il difetto sia nella mediana:** non c'è una statistica che collassa,
> **non c'è variazione da misurare.**

### Le due cause, entrambe confermate

**(1) SNAPSHOT CONFRONTATO CON SÉ STESSO — 3 su 4.** `_psi_spin_prec` viene aggiornato a
**`:3099-3101`**, cioè **dopo** `ritmo()`. Quando `psi_spin` non è cambiato dall'ultimo snapshot,
`a = angle(ψ) − angle(ψ) = 0` **per ogni nodo**. `snap == True` in 3 casi su 4.

**(2) LUNGHEZZE DISALLINEATE — il passo 6.** `len(psi_spin) = 440` ma `len(_psi_spin_prec) = 80`:
dopo l'iniezione delle tre masse (`n: 80 → 440`) **lo snapshot non è stato esteso**. Il guard di
`:2038` fallisce → si cade sul **ramo scalare 2π** → e lì anche `_psi_prec` è corto → scatta il
**ramo di sicurezza `:2028-2030`**, che restituisce `np.ones(n)`.

> **È la stessa famiglia di `C11`** (`_psi_spin_prec` non esteso alla mitosi, inerte nel 95.33 % per
> mesi) **e di `C7`** (la cache `_cs_nodo_prev` scartata a ogni mitosi). **Terzo membro.**

## 3. (C / 2.2) QUANDO — **transitorio, senza ambiguità**

```
passi degeneri : [0, 1, 6, 7]
primi 10 passi : 4        dopo il passo 20 : 0
nodi NATI nei degeneri : [0, 0, 0, 0]
```

**Non coincidono con le mitosi** (nati = 0 in tutti e quattro). **Coincidono con le due
discontinuità della popolazione:** l'**avvio** (0, 1) e l'**iniezione delle tre masse** (6, 7, dove
`n` salta `80 → 440`).

> **È il TRANSITORIO, ed è la stessa classe dei neonati con `psi = 0` alla nascita, già catalogata.**

## 4. (D / 2.3) COSA SUCCEDE a `r` — **la dilatazione sparisce, ma verso il BASSO**

| gruppo | quanti | `median(r)` | **`std(r)`** | `p95−p05` | `fraz r>1.4` | `fraz r<1e-5` |
|---|---|---|---|---|---|---|
| **DEGENERI** | 4 | 0.500001 | **0 ESATTO** | **0 ESATTO** | **0.0000** | **0.4909** |
| SANI | 122 | 1 | 0.4146 | 1.268 | 0.0926 | 0.0000 |

**`std(r) = 0` ESATTO nei degeneri: tutti i nodi allo stesso ritmo. La dilatazione temporale è
sparita davvero.** Il sospetto del §1 del mandato **è confermato nell'effetto.**

### ⚠ Ma il segno era sbagliato, e la differenza conta

Il mandato scriveva: *«`med = 1e-9` → `|x|` enorme → `r → ±1` per tutti»*. **Misurato: `fraz r>1.4`
è `0.0000`, e `fraz r<1e-5` è `0.49`.**

**Perché:** se `f` è **identicamente nullo**, allora `x = 0/1e-9 = 0`, quindi `r = 0 + 1e-6` e il
ritorno vale `1 + (1e-6/r_unit − 1) ≈ **1.414e-06**`. **Il collasso è verso il BASSO.**

**I quattro degeneri si dividono in due coppie:**
- **passi 0 e 6** → `r = 1.0` esatto per tutti *(il ramo di sicurezza `:2028`: `np.ones(n)`)*;
- **passi 1 e 7** → `r ≈ 1.414e-06` per tutti *(`f` nullo → `x = 0`)*.

> **Nei passi 1 e 7 `dt_n = DT × 1.4e-06`: IL TEMPO PROPRIO SI FERMA PER TUTTI.** Non è che tutti
> vadano alla stessa velocità normale: **vanno a velocità quasi nulla.**
> *(Lo avevo previsto nel task history, prima di misurare. **Il mandato prevedeva l'opposto.**)*

---

## 5. VERDETTO CONTRO LE CINQUE LETTURE

| lettura | esito |
|---|---|
| transitorio, `r` non degenera → si chiude `Z33` | **NO**: `r` degenera, `std(r) = 0` |
| **transitorio, ma `r` degenera → difetto CONFINATO, cura opzionale** | **✓ È QUESTA** |
| a regime → difetto grave, `Z9` da rimisurare | **NO**: zero eventi dopo il passo 20 |
| `f` mediana nulla per costruzione → A3 in forma nuova | **NO**: `f` è *identicamente* nullo |
| **⊕ non è nel percorso fisico** *(la quinta, aggiunta da me)* | **NO** — ma **la sua seconda metà sì** |

**La quinta lettura diceva anche:** *«se `f` è identicamente nullo e la causa è lo snapshot non
aggiornato → è un difetto di ORDINE, non di gauge, e la cura non c'entra con la mediana.
Cambierebbe tutto il quadro.»* **È esattamente così.**

> **`Z33` non è un difetto del gauge né della mediana. È un difetto di ORDINE/SNAPSHOT**, e va
> spostato fuori dalla famiglia `A3` in cui l'avevo messo.

## 6. E IL §4 DEL MANDATO — **`Z9` non ha bisogno di essere rimisurata, e lo dico con un numero**

I passi degeneri sono **0, 1, 6, 7**, e in **due** di essi (`1` e `7`) `eta` non cresce.
**Su 126 passi sono 2, cioè l'`1.6 %`** — e sono **tutti nel transitorio iniziale**, prima che la
finestra di misura di `Z9` (passi 1/60/120) abbia peso.

> **L'impatto su `Z9` è ≤ ~2 %, cioè dentro il `+2.8 %` già misurato e dentro la differenza fra le
> due scene (`5680` contro `6049`, `+6.5 %`).** **Rimisurare `Z9` non cambierebbe nulla di leggibile,
> e lo dico con un conto invece di ometterlo.**

## 7. SE SI VOLESSE CURARE — **e non è il gauge**

**La cura non tocca né la mediana né il pavimento `1e-9`.** Le due cause sono:
1. **l'ORDINE**: `ritmo()` legge uno snapshot che sarà aggiornato subito dopo. Una guardia che
   **rilevi `psi_spin == _psi_spin_prec` e lo dichiari** (A8: un ramo silenzioso non è un ramo)
   basterebbe a renderlo visibile;
2. **l'ESTENSIONE dello snapshot** dopo una crescita di `n` — **la stessa cura di `C7`/`C11`**, che
   in entrambi i casi era «il figlio eredita dal padre», e qui sarebbe «lo snapshot si estende con
   la popolazione».

**Non le propongo: le riporto.** E **nessuna delle due tocca il gauge**, quindi **non ricade nella
decisione di Luca del §3** — ma **la cura resta opzionale**, perché il difetto è confinato a 4 passi
su 126 nel transitorio.

## 8. I LIMITI

Un seme, 126 passi, una scena. **E i quattro eventi sono legati a DUE discontinuità specifiche**
(l'avvio e l'iniezione delle masse): **una scena con più iniezioni ne avrebbe di più**, e una senza
iniezioni forse solo due. **La frazione `3.2 %` è di questa scena, non del sistema.**
