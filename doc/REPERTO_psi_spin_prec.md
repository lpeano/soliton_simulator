# REPERTO — `_psi_spin_prec`: **l'orologio spinoriale a 4π è spento nel 95 % dei passi**

**Data:** 2026-09-15 · **Branch:** `fork-su2` · **Blob:** `b298677a` → **`08784685`** (curato)
**FASE A (§1-6) e FASE B (§7-8) — cura applicata col via libera, sigillo 6/6 PASS.**
**⚠ Leggi il §8: `S4` ha misurato la cosa sbagliata, e il numero non lo diceva.**

---

## 1. LE TRE VERIFICHE PER STRINGA — **tornano tutte e tre**

| verifica | esito |
|---|---|
| `len(_ps) == self.n and len(_psp) == self.n` | **riga 1829**, uguaglianza **esatta** (`==`), non `>=` |
| `self._psi_spin_prec = self.psi_spin.copy()` | **riga 2647**, a fine passo, con l'`n` di **quel** passo |
| `_psi_spin_prec.*[src]` / `vstack.*_psi_spin_prec` | **zero occorrenze** — **non e' esteso alla mitosi** |

È l'ultimo della sua famiglia a non esserlo: `_nb`, `_nb_prec`, `_nb_ret`, `omega_s`, `_psi_spinor`,
`_psi_prec` sono tutti estesi, e `_cs_nodo_prev` lo è da oggi.

---

## 2. IL NUMERO (150 passi, seme 1, scena 3 masse, `--campo-spinoriale` ON)

`csv/_test_fork/_conta_psi_spin_prec.py` → `csv/_test_fork/_conta_psi_spin_prec.txt`

| esito di ogni chiamata a `ritmo()` | conteggio | % |
|---|---|---|
| **guardia 4π FALLISCE** → ricade sul ritmo **SCALARE a 2π** | **143 / 150** | **95.33 %** |
| guardia 4π passa (ritmo spinoriale attivo) | 6 / 150 | 4.00 % |
| `return` anticipato su `_psi_prec` (`r = 1` ovunque) | 1 / 150 | 0.67 % |

**E la condizione che fallisce è UNA SOLA, in 143 casi su 143:**

```
solo len(psi_spin) != n        :   0
solo len(_psi_spin_prec) != n  : 143     <-- tutti qui
entrambe                       :   0
uno dei due ASSENTE (None)     :   0
```

**`psi_spin` è sempre della lunghezza giusta** (lo ricalcola `calcola_psi` dentro il passo). È
**solo** lo snapshot cross-passo a restare indietro — **la firma esatta del pattern**.

```
passo |     n | len psi_spin | len _psi_spin_prec | esito
    2 |  1196 |         1196 |               1196 | 4pi          <- prima della prima mitosi
    3 |  1196 |         1196 |               1196 | 4pi
   10 |  1258 |         1258 |               1231 | SCALARE 2pi
   30 |  1746 |         1746 |               1728 | SCALARE 2pi
   60 |  2369 |         2369 |               2343 | SCALARE 2pi
  150 |  3420 |         3420 |               3413 | SCALARE 2pi
```

Il 4π gira **solo ai passi 2 e 3**, prima che la mitosi cominci. **Da lì in poi, mai più.**

**Lettura fissata PRIMA: `> 10 %` ⇒ stesso bug della cache `cs`, la cura è giustificata.**
Misurato **95.33 %**: non è un caso limite, è il regime.

---

## 3. DUE CORREZIONI AL MANDATO, dalla misura

**3.1 — «il tempo proprio del settore 4π resta fermo»: NO, ricade sul 2π.**
Il mandato dice che se la guardia scarta *«`signed` non viene aggiornato, e il tempo proprio del
settore 4π resta fermo»*. **Non è quello che succede.** `signed` **è già stato calcolato** poche
righe sopra, nella versione **scalare a 2π** (righe 1822-1823); la guardia decide solo se
**sovrascriverlo** con la versione a 4π. Quando fallisce, `r` e `dt_n` **esistono e sono aggiornati** —
con l'orologio **storico**, non con quello spinoriale.

**La conseguenza vera è più netta di quella temuta, non meno:** non è un orologio fermo, è che
**la FASE 5 — l'orologio di doppia copertura — è di fatto INERTE in ogni run `--campo-spinoriale`
mai girato.** Il flag è acceso, il codice c'è, e il ramo non viene preso.

**3.2 — c'è un TERZO esito, che il mandato non nomina.**
Prima della guardia 4π, `ritmo()` ne ha un'altra su `_psi_prec` con **`return` anticipato**
(`return np.ones(self.n)`): se scatta, `r = 1` ovunque e il 4π **non viene nemmeno raggiunto**.
Contarli insieme avrebbe detto «la guardia fallisce» per due situazioni fisicamente diverse. Contati
a parte: **0.67 %**, un solo passo (il primo dopo `nuova_massa`, `_psi_prec` a 80 contro `n = 1196`).
Marginale — ma andava separato **prima** di guardare i dati, non dopo.

---

## 4. PUREZZA — più forte di quella chiesta

Il mandato chiedeva di strumentare la guardia con un contatore **nel sorgente**. Non è stato
necessario e sarebbe stato più invasivo: lo script **avvolge `Rete.ritmo`** in un wrapper che valuta
le **stesse** condizioni in sola lettura e poi delega all'originale.
**`soliton_simulator.py` non è stato toccato: blob invariato `b298677a`.** Zero RNG consumato, zero
stato mutato. Il contatore in produzione si cabla se e quando servirà.

---

## 5. COSA **NON** DICO

**Non dico che questo spiega il residuo di T3, la «metà mancante», o qualunque risultato
precedente.** Il mandato lo vieta prima di S4, e lo vieterei comunque: è **esattamente** l'errore
appena pagato con la cache `cs`, dove un difetto reale al 71.88 % ha prodotto un effetto fisico
**non dimostrabile** su tre semi (`doc/FIX_cache_cs.md` §7, fronte **P**).

**Un difetto grande non implica un effetto grande.** Il numero qui sopra dice quanto spesso un ramo
viene preso, **non** quanto cambia la fisica quando lo si prende. Quello lo direbbe **S4**, e S4 non
è stato eseguito.

---

## 6. STATO

*(Paragrafo storico: qui la FASE A si è fermata in attesa del via libera, arrivato poi. La FASE B è
nel §7.)* La cura: `_psi_spin_prec` esteso alla mitosi come le altre sei, `vstack` perché è `n x 2`
complesso.

⚠ **A differenza della cache `cs`, questa cura CAMBIA LA FISICA per costruzione:** fa ripartire
l'aggiornamento di `signed` dopo ogni mitosi, quindi il ramo ON **non sarà byte-identico**, ed è
**atteso**. S1 (byte-identità) vale solo a `--campo-spinoriale` **OFF**.

---

## 7. FASE B — LA CURA, **sigillo 6/6 PASS**

Via libera ricevuta. `_psi_spin_prec` esteso alla mitosi in `_eredita_spinore_figli`: **settima voce
della stessa convenzione**, `np.vstack` perché è `n × 2` **complesso**. Zero parametri.
Non toccati: la guardia, la scrittura a fine passo, `signed`, `r`, `dt_n`.
Blob: **`b298677a` → `08784685`**. Sigillo: `csv/_seal_fork/_sigillo_psi_spin_prec.txt`.

| | esito | numeri |
|---|---|---|
| **S1** byte-identità a `--campo-spinoriale` OFF | **PASS** | `n_A = n_B = 2501` (**confrontabili**), 21 campi, `max\|A-B\| = 0.000e+00`, RNG identico |
| **S1b** con ON devono DIFFERIRE (aggiunto da me) | **PASS** | `n` **2392** contro **2200** |
| **S2** il contatore | **PASS** | **88.33 % → 0.00 %** (53/60 → 0/60); *tutti* i fallimenti erano `len != n` |
| **S3** `len(_psi_spin_prec) == n` | **PASS** | passi disallineati **54/60 → 0/60** |
| **S4** di quanto cambia `r` | *quantificazione* | vedi sotto — **la misura era mal posta** |
| **S5** stabilità | **PASS** | `\|nb\|-1 = 2.2e-16`, NaN/inf **0**, `r` finito e positivo |

*(88.33 % qui contro 95.33 % in FASE A: run più corto, 60 passi contro 150 — più peso ai primi passi,
quando la mitosi non ha ancora cominciato. Stesso regime.)*

---

## 8. ⚠ S4 HA MISURATO LA COSA SBAGLIATA — e non lo dice il numero, lo dice il codice

```
PRIMA   r: mediana 1.000000 +- 0.011330   dev.std fra nodi 0.442149   n 2392
DOPO    r: mediana 0.999999 +- 0.011374   dev.std fra nodi 0.425661   n 2200
scarto sulla mediana: -0.000001 +- 0.016054   ->  z = 0.00
```

**Quel `z = 0.00` non significa "la cura non cambia `r`". Significa che la mediana di `r` NON PUÒ
CAMBIARE.** Dalla coda di `ritmo()`:

```python
f   = np.abs(signed)
med = max(float(np.median(np.abs(f))), 1e-9)
x   = f / med                       #  il nodo MEDIANO ha x = 1, sempre
r   = x/np.sqrt(1+x**2) + 1e-6      #  x = 1  ->  r = 1/sqrt(2) + 1e-6
r_normalized = r / (1/np.sqrt(2) + 1e-6)     #  = 1 ESATTAMENTE
return 1.0 + TAU_LOC * (r_normalized - 1.0)  #  = 1.0 ESATTAMENTE
```

**`r` è normalizzato sulla PROPRIA mediana**, e la trasformazione è monotona in `f`: quindi
**`median(r) = 1.0` identicamente, con qualunque orologio.** Cambiare da 2π a 4π cambia `f` nodo per
nodo, ma **la mediana resta inchiodata a 1 per costruzione**. Confrontare le due mediane è come
confrontare due termometri dopo averli entrambi azzerati sulla loro stessa lettura mediana.

> **È IL SECONDO CASO DELLO STESSO TRABOCCHETTO STRUTTURALE.** Il primo è già in `CLAUDE.md` §9:
> `_tau = TAU_A * max(_dens/_dens_rif, 0.05)` con `_dens_rif = median(_dens)` → `tau_mediano ≈ TAU_A`
> **sempre**. Stessa forma: **una grandezza normalizzata sulla propria mediana ha un punto fisso
> auto-normalizzante, e su quel punto NON si misura nulla.**

**L'unico numero informativo di S4 è la DISPERSIONE:**

| | PRIMA (2π) | DOPO (4π) | rapporto |
|---|---|---|---|
| dev.std di `r` fra nodi | **0.442149** | **0.425661** | **0.9627** (−3.7 %) |
| `r` minimo | 0.001139 | **0.000020** | ×0.018 |
| `r` massimo | 1.414209 | 1.347323 | 0.953 |

**E non basta a concludere.** È **un seme**, e per **C10** (`doc/RAMIFICAZIONI.md`) il valore sotto
ipotesi nulla di un confronto fra due run caotici **non è zero** e qui **non è stato misurato**: due
run che divergono fino a `N = 2392` contro `2200` hanno una dispersione di `r` diversa **anche senza
cambiare l'orologio**. **Il numero si riporta, non si interpreta.**

**Quindi: l'attesa «r potrebbe cambiare in modo significativo» NON è confermata da questa misura —
e non è nemmeno smentita. S4, così com'è costruito, non può rispondere.** Rifarlo richiede o un
osservabile che non passi dalla normalizzazione (per esempio `signed` grezzo, oggi non esposto), o
il confronto su più semi.

**E non dico che questo chiuda T3.** Non è stato misurato qui.
