# REFERTO — **Nessuna delle due vie cura `Z33`. La cura è il CONTATORE. E `K7` apre un difetto più grande**

**Data:** 2026-09-18 · **Blob** `94b6cc29` (byte, coi contatori) · un seme (5), 126 passi
**Task history scritto e pushato PRIMA:** `f0c6…` (`2026-09-18_Z33-cura-snapshot.md`)
**Strumento:** `csv/_test_fork/_Z33_due_vie.py` · **NESSUNA CURA CABLATA**

---

## 0. IL VERDETTO, in quattro righe

1. **La via (1) è il difetto, non la cura** — l'ordine attuale **rispetta già A6**, e spostare
   l'aggiornamento farebbe confrontare `psi_spin` **con sé stesso**.
2. **La via (2) non cura il caso che dovrebbe curare**: all'iniezione i nodi nuovi sono l'**81.8 %**,
   quindi dargli `f = 0` **lascia la mediana a zero lo stesso**. E per farlo altrimenti bisognerebbe
   **inventare un passato** (A1 + A7b).
3. **La cura è il CONTATORE**, ed è **già dentro e byte-inerte** (`800fb24`).
4. **⚠ E `K7` apre un difetto più grande: `f` NON è cucito.** Salta del **64.7 %** del proprio valore
   fra passi consecutivi, contro il **3.2 %** di `imag(ov)` del feedback. **Venti volte peggio.**

---

## 1. VIA (1) — **verificata dal sorgente, e sarebbe il difetto**

```
:2693   self.psi_spin = ...          <- UNICO punto di assegnazione
:2649   ...dentro calcola_psi()
:3124   r = self.ritmo()             <- consuma, all'INIZIO di step()
:3132   self._psi_spin_prec = ...    <- lo snapshot si aggiorna DOPO
```

Il consumo a `:3124` legge un `psi_spin` prodotto **dal passo precedente** (l'ultimo `calcola_psi`)
e lo confronta con lo snapshot preso **alla fine di quel passo**.

> **L'ordine attuale rispetta A6.** Spostare l'aggiornamento prima del consumo confronterebbe
> `psi_spin` **con sé stesso**: `f = 0` **per costruzione, sempre**.
> **La via (1) del mandato è il difetto, non la cura.**

## 2. VIA (2) — **non cura, e inventerebbe un passato**

```
:1812   semina()                  -- NON estende _psi_spin_prec   (voce H, verificato)
:1351   _eredita_spinore_figli    -- LO ESTENDE, ma solo per la MITOSI (cura C11)
all'iniezione:  n 80 -> 440   NODI NUOVI 360 = 81.8 % della popolazione
```

**I nodi di `nuova_massa` non hanno un genitore.** `_eredita_spinore_figli` estende lo snapshot alla
mitosi ed è **giustificato** — il figlio nasce dal padre, ereditarne la fase **è fisica**. Ma qui non
c'è un padre da cui ereditare.

**Le due sole scelte, e nessuna funziona:**
- **estendere col valore corrente** *(l'unica che non inventa un moto)* → quei nodi hanno `f = 0`
  **esatto**, e sono l'**81.8 %**: **la mediana resta zero. Il difetto non si cura.**
- **estendere con qualcos'altro** → **si inventa una fase precedente**: **A1** (un numero scelto) e
  **A7b** (una storia che non c'è).

> **La via (2) risolve il passo dell'iniezione solo a prezzo di fabbricare un passato — e nemmeno
> quello, perché col valore corrente il conto dice che non basta.**

## 3. I CONTATORI A8 — **già dentro, byte-inerti, e correggono una mia ricostruzione**

```
_ritmo_chiamate = 126    _ritmo_sicurezza = 2  (shape 80/440)    _ritmo_guard4pi_ko = 0
_ritmo_snap_identico = 1   _ritmo_f_tutto_nullo = 1   _ritmo_f_mediana_nulla = 1
_ritmo_med_sul_pavimento = 2
-> passi con tempo proprio DEGENERE: 4 su 126 = 3.17 %
```

**⚠ `_ritmo_guard4pi_ko = 0`: il guard 4π non fallisce MAI.** Nel referto precedente avevo scritto
che al passo 6 *«il guard di `:2038` fallisce, si cade sul ramo 2π»*. **Non è così:** il ramo di
sicurezza `:2028` viene **prima**, e quando `_psi_prec` è corto si esce di lì **senza mai
raggiungere** il guard 4π. **La mia sonda ricostruiva i rami nell'ordine sbagliato; il contatore,
che sta nel codice vero, è autoritativo.**

**E il quarto caso non era «escluso»:** `_ritmo_f_mediana_nulla = 1` dice che **esiste** un caso con
mediana nulla e valori non nulli — sono `3.5e-13`, rumore numerico, **ma il contatore li distingue,
ed è il suo mestiere.**

**Byte-inerzia verificata** contro il blob `aa84755b` estratto in binario: `psi`, `phivel`, `eta`,
`d`, `d0`, `omega_s`, `_nb` → **`max|A−B| = 0.000e+00` su tutti, shape identiche** (443 = 443).

## 4. ⚠ `K7` — **`f` NON è cucito, e questo rende il primo difetto secondario**

| grandezza | `\|Δ\|/\|·\|` | cambi di segno |
|---|---|---|
| **`f = \|signed\|`** *(quella che il codice USA)* | **0.647** | — |
| `signed` *(col segno)* | 0.933 | **0.342** *(nullo: 0.50)* |
| **confronto — `imag(ov)` del feedback (`G6`)** | **0.032** | **0.0035** |

**`f` salta del `64.7 %` del proprio valore fra passi consecutivi. `imag(ov)` saltava del `3.2 %`.
Venti volte peggio.**

E `signed` cambia segno nel **34.2 %** dei nodi fra passi consecutivi, contro un nullo di `0.50`:
**parzialmente cucito, ma molto più vicino al rumore che alla cucitura.**

> **Il tempo proprio è costruito su una grandezza che non è cucita.** `Z33` — 4 passi su 126 in cui
> `f` è nullo — **è un caso particolare di un problema che c'è in TUTTI i passi.**

**Due precisazioni che impediscono di sovrainterpretare:**
- **il codice prende `|signed|`**, quindi i cambi di segno **sono già scartati**: il `0.933` del
  segnato è **gonfiato da quelli**, e il numero che conta è **`0.647`**;
- **ma proprio per questo, `--tempo-proprio-orientato` alimenterebbe una grandezza NON cucita.**
  **È un avviso per quel flag**, non per il default.

## 5. COSA RACCOMANDO — **e la decisione è di Luca**

**Non cablo né la (1) né la (2).** La (1) è il difetto; la (2) non cura e inventerebbe.

**La cura di `Z33` è il contatore**, ed è **già dentro**: da oggi la degenerazione **si dichiara
invece di essere invisibile** — che è ciò che mancava, e l'unica cosa che i tre casi della famiglia
(`_cs_nodo_prev` 71.88 %, `_psi_spin_prec` 95.33 %, questo) **non avevano**.

**E i quattro casi sono legittimi**, uno per uno: al passo 0 **non esiste un prima**; al passo
dell'iniezione i 360 nodi nuovi **non hanno un passato**; negli altri due il campo **davvero non si è
mosso**. **Il codice fa la cosa giusta. Mancava solo che lo dicesse.**

**Quello che va deciso è `K7`:** un tempo proprio che salta del **65 %** per passo è un fronte
nuovo, **più grande di `Z33`**, e non è in nessuna voce.

## 6. IL §4 DEL MANDATO — **`Z9` non serve rimisurarla, e il conto non cambia**

`eta` non cresce in **2 passi su 126 = 1.6 %**, tutti nel transitorio. **Impatto ≤ ~2 %**, dentro il
`+2.8 %` già misurato. **Confermato dal giro precedente, e i contatori non lo spostano.**

## 7. I LIMITI

Un seme, 126 passi, una scena. **E `K7` confronta nodo per nodo sui primi `min(len)` indici**: i
nuovi si appendono in coda, quindi gli indici bassi restano gli stessi nodi — **è
un'approssimazione, ed è dichiarata nell'output.** La frazione `81.8 %` è **di questa scena**: con
masse più piccole sarebbe minore, e la via (2) potrebbe funzionare meglio — **ma resterebbe
l'invenzione del passato.**
