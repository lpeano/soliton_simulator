# REPERTO — `_psi_spin_prec`: **l'orologio spinoriale a 4π è spento nel 95 % dei passi**

**Data:** 2026-09-15 · **Branch:** `fork-su2` · **Blob:** `b298677a` (verificato dal disco)
**FASE A soltanto — nessuna cura. Si aspetta il via libera.**

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

**FERMO in attesa del via libera** (§5 del mandato, e par.1 «un interruttore alla volta»).
La FASE B — `_psi_spin_prec` esteso alla mitosi come le altre sei, `vstack` perché è `n x 2`
complesso — è **scritta ma non applicata**.

⚠ **A differenza della cache `cs`, questa cura CAMBIA LA FISICA per costruzione:** fa ripartire
l'aggiornamento di `signed` dopo ogni mitosi, quindi il ramo ON **non sarà byte-identico**, ed è
**atteso**. S1 (byte-identità) vale solo a `--campo-spinoriale` **OFF**.
