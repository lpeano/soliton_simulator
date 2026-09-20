# REFERTO — **i 18 azionabili classificati. E c'è una `(c)`: cinque guardie proteggono da un difetto già curato**

**Blob `f81c4fe1`** *(sha1 byte grezzi; git `af8a96f1`)* · tabella prodotta da
`csv/_test_fork/_classifica_guardie.py` (`09c6116`), **poi letta sito per sito dal disco** ·
criteri fissati in `doc/TASK_HISTORY/2026-09-20_precondizione-e-pannello.md` (`4e122c3`).
**NESSUN CODICE TOCCATO. Simulatore invariato.**

---

## 1. LA TABELLA

| riga | funzione | la guardia | origine | ragione trovata | | al fallimento |
|---|---|---|---|---|---|---|
| **`:1343`** | `_estendi_psi_spinor` | `elif len(cur) > n` | `5769a12` | **è TRONCAMENTO** | **falso positivo** | tronca: è `ESTENSIONE` |
| **`:2104`** | `ritmo` | `len(_ps) != n or len(_psp) != n` | `800fb24` | **`Z33`: già contata** | **già curata** | `_ritmo_guard4pi_ko` + `_shape` |
| **`:2113`** | `ritmo` | la stessa, ramo positivo | `4ea6f0c` | **contata a `:2104`** | **già curata** | il contatore è 9 righe sopra |
| **`:2402`** | `_passo_spinoriale` | `len(_peq_a) != len(self.i)` | `4f2a6b7` | **`Y5`: PORTA A misurata INERTE** | **già curata** | `_porta_A` + `_ultima` + `_shape` |
| **`:4084`** | `mitosi` | `len(_dte) != len(rep)` | `3ca7731` | **`P5` dichiarato nel codice** | **già curata** | `_rep_dte_fallback`, cade su `DT` |
| **`:574`** | `scuoti_vuoto` | `len(perc_chi) == n` | `3fb5143` | — | **(c)** | il calcio non è firmato dalla chiralità |
| **`:2285`** | `_passo_spinoriale` | `len(perc_chi) >= n` | `2bd7ec8` | — | **(c)** | `chi_nodi` = `perc_chi` grezzo |
| **`:3390`** | `step` | `len(perc_chi) >= n` | `0639ba2` | — | **(c)** | `dt_n_s = dt_n` |
| **`:3623`** | `step` | `len(phi_s) == n` | `2dd0756` | — | **(c)** | **tutto `_passo_spinoriale` non gira** |
| **`:3669`** | `step` | `len(perc_chi) >= n` | `5769a12` | — | **(c)** | `perc_chi` non riscritto dallo spinore |
| **`:2021`** | `_allaccia` | `COMPAT_CHI and len(perc_chi) >= n` | `670310f` | **il commento dichiara `default off … finché non è verificata`** | **(b)** | nessun filtro dipolare |
| **`:3517`** | `step` | `CHI_CORE and len(perc_chi) >= n` | `2bd7ec8` | **catena `if/elif/elif` con `else` esplicito a `:3526`** | **(b)** | passa al ramo successivo |
| **`:3520`** | `step` | `VERSO_CHI and len(perc_chi) >= n` | `2bd7ec8` | **idem**; `VERSO_CHI = False` | **(b)** | passa al ramo successivo |
| **`:3526`** | `step` | `not (CHI_CORE and len(perc_chi) >= n)` | `2bd7ec8` | **È l'`else` esplicito della catena** | **(b)** | `twn = _tw_t / PHI_CRIT` |
| **`:4661`** | `memoria_hebbiana_moto` | `K_FRANGE != 0.0 and len(proj)` | `670310f` | **`K_FRANGE = 0.0`: ramo morto per COSTANTE** | **(b)** | il flusso di frangia non gira |
| **`:2279`** | `_passo_spinoriale` | `len(_nb_prec) != n` | `c2175ee` | — | **(a)** | **`nb_vic = nb`: il Bloch CORRENTE al posto del RITARDATO** |
| **`:3353`** | `step` | `len(psi_spin) == n` | `4ea6f0c` | — | **(a)** | **`_psi_spin_prec` NON avanza** |
| **`:4586`** | `memoria_hebbiana_moto` | `SPINORE and len(_nb) >= n` | `670310f` | — | **(a)** | `grav` non proiettata sul campo spinoriale |

```
falso positivo / già curate   5
(c) ragione SCADUTA           5
(b) ragione VALIDA            5
(a) nessuna ragione           3
                             18
```

---

## 2. ⚠ IL REPERTO — **le cinque `(c)` proteggono da qualcosa che non può più accadere**

**Tutte e cinque testano `len(perc_chi)` o `len(phi_s)` contro `n`. E TUTTE E TRE le vie di crescita
dei nodi li estendono — verificato dal disco:**

```
perc_chi :  semina()  :1900      mitosi  :4181      Schwinger  :4302
phi_s    :  semina()  :1882      mitosi  :4176      Schwinger  :4297
```

> **Non esiste un percorso che aggiunga un nodo senza estendere questi due array.**
> **Quelle guardie non possono fallire — e infatti la misura del `PASSO 1` sulle loro sorelle dà
> `0` salti su `145`, `34` e `12` invocazioni.**

**E la più grave è `:3623`:** se fallisse, **l'intero `_passo_spinoriale` non girerebbe** — il cuore
del settore spinoriale, con `SPINORE_VIVO = 1` nel run. **Una guardia muta su un interruttore di
quella portata è esattamente `C11` un'altra volta**, se non fosse che **non può scattare**.

**Cosa NON concludo:** che si possano togliere. **Una guardia che oggi non può fallire protegge
comunque da una REGRESSIONE futura** *(se domani si aggiungesse una quarta via di crescita)*.
**La cura giusta è il contatore + la ragione scritta — «questa guardia è ridondante OGGI perché le
tre vie estendono l'array» — non la rimozione.**

## 3. LE TRE `(a)`, e una è seria

**`:2279` è la peggiore, e non per frequenza ma per COSA fa il fallback.** Due righe sopra il codice
dichiara *«CAUSALITÀ: campo dai vicini allo stato RITARDATO (Bloch del passo precedente)»*, e il
fallback usa **`nb_vic = nb`, cioè il Bloch CORRENTE**. **Se scattasse, la causalità che il commento
dichiara sarebbe rotta in silenzio.**

**`:3353` è la causa di cui `ritmo()` conta già il sintomo:** se non avanza, `_psi_spin_prec` resta
quello vecchio e `ritmo()` registra `_ritmo_snap_identico`. **Il sintomo è contato, la causa no.**

**`:4586`:** `grav` non viene proiettata sul campo spinoriale → la gravità bifase cambia forma.

**⚠ E per `:2279` e `:4586` la verifica di ridondanza NON si chiude come per le `(c)`:** `_nb` e
`_nb_prec` sono estesi da `_eredita_spinore_figli` *(mitosi e Schwinger)*, **ma `semina()` NON passa
da lì** — è la **voce `H`** di `RAMIFICAZIONI.md`. **Quindi quelle due guardie possono ancora
scattare, e il contatore serve davvero.**

## 4. COSA PROPONGO, e mi fermo qui

1. **PASSO 1 — contatori byte-inerti su 8 siti** *(le 3 `(a)` + le 5 `(c)`)*, col nome, le
   invocazioni, la forma e il **QUANDO**. **Le 5 `(c)` si contano proprio per DIMOSTRARE che non
   scattano** — è la differenza fra «credo sia ridondante» e «misurato `0` su `N`»;
2. **le 5 `(b)` si REGISTRANO** col perché, **senza toccarle** *(il mandato dice contatore anche per
   loro: lo farei solo su `:2021` e `:4661`, dove il ramo è inerte per flag/costante, e NON sulla
   catena `:3517-:3526`, che ha già l'`else` esplicito e dove un contatore per ramo sarebbe tre
   contatori su una scelta a tre vie — lo dico perché è una mia deviazione dal mandato)*;
3. **le 4 già curate e il falso positivo si REGISTRANO e basta;**
4. **le 7 `VACUITA'` si registrano come tali** — nessuna decisione da prendere su un insieme vuoto.

**Poi il PASSO 2, poi il pannello, poi il run.**
