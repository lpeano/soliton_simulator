# TASK HISTORY — **la scena del VIDEO, con lo stato salvato**

**Data:** 2026-09-18 · **Branch** `fork-su2` · **HEAD alla scrittura** `567a330`
**Blob:** `a1ae5090` — **e non cambierà: nessuna cura, nessun cablaggio.**

---

## 1. RAGIONAMENTO PRELIMINARE — *verificato dal disco*

### 1.1 ⚠ `--sync-db` NEL RAMO VIDEO **CARICA E BASTA: non salva mai**

```python
:5836   _db_v = getattr(a, "sync_db", None)
:5837   if _db_v and _os_v.path.exists(_db_v):
:5839       net.carica_stato(_db_v)      # <- SOLO LETTURA
        # ... e in TUTTO `esegui_headless` non c'e' NESSUNA chiamata a `salva_stato`
```

Il commento del codice lo dice da sé: *«se `--sync-db` e il file esiste, **CARICA** lo stato … e
renderizza **IN AVANTI** da lì»*.

> **Il comando del §1 del mandato NON produrrebbe nessun `.pkl`.** Il mandato chiedeva di dirlo e
> **proporre la via senza forzare: la via è un driver che riproduce la scena col PERCORSO UFFICIALE
> del programma** — `_cli()` → `_applica_regime` → `_applica_flag` → `avvia_test("N-MASSE")` — **e
> il ciclo per frame COPIATO da `update()`, senza il rendering.** *(Il rendering non è fisica.)*

### 1.2 ⚠ `PASSI_PER_FRAME = 6`: **la scena è 2400 passi, non 400**

`:686` `PASSI_PER_FRAME = 6`, e `update()` (`:5097-5100`) fa **sei** `step()` per frame.
**La scena `N-MASSE` dura `dur=120 + dur=280` = 400 FRAME = `2400` passi di motore.**
**Il conto della durata va fatto sui frame, e ogni frame costa sei passi.**

### 1.3 ✅ LA DURATA, MISURATA su un pilota di 15 frame

```
scena avviata: n = 2391   (N_c*0.8 per massa, N_c = 621, tre masse)
frame  1  n=2391  archi=429498  coer_l=0.639  dil= +7.88%   [16.97 s/frame]
frame 15  n=2391  archi=429498  coer_l=0.515  dil=+20.40%   [16.57 s/frame medio]
```

**`n = 2391` alla semina coincide ESATTAMENTE col frame 10 della tabella del mandato**, e
`coer_l`/`dil` sono nello stesso intorno: **è la scena giusta.**

**La stima, e la dichiaro con la sua incertezza:**
- a `n = 2391` (429 498 archi): **16.6 s/frame** ⟹ 400 frame = **1 h 50 min** *se `n` non crescesse*;
- **ma `n` arriva a `7503`** (tabella del mandato). A grado medio costante (~359) gli archi
  triplicherebbero ⟹ **~50 s/frame a fine corsa**;
- **stima onesta: 3-4 ore**, con l'avvertenza che **il costo cresce coi nodi e una estrapolazione
  lineare SOTTOSTIMA.**

> **Non è «oltre il ragionevole» per un job in background, e non è un lancio alla cieca: il numero è
> misurato. Ma è lungo, e lo dichiaro PRIMA.**

### 1.4 ⚠ UNA DIFFERENZA DI CONFIGURAZIONE CHE NESSUNO HA NOMINATO: `CALORE_VETTORIALE = False`

Letto dal modulo **dopo** `_applica_flag`, con i flag del mandato:

```
CALORE_VETTORIALE    False        <- perche' il comando ha `--calore-scal`
```

**Nel giro di `Z45` questo era l'unico canale vivo fra `perc_chi` e la dinamica**
(`scuoti_vuoto` firma il calcio con `perc_chi`). **Qui è SPENTO.**
**E `--chi-basc` è ACCESO**, quindi `perc_chi` **non è un'etichetta di lignaggio ma una variabile
della torsione.**

> **Due differenze opposte rispetto a `Z45`: il canale è spento, e l'etichetta è dinamica.**
> **La misura ④ va letta con queste due condizioni, non con quelle di `Z45`.**

### 1.5 Cosa mi aspetto, e cosa NON so

**Non so** se il `93 %` si ripeta. **Le due scene differiscono in TRE cose**, non una: masse a
`N_c·0.8` invece di `N_c·0.6`, **mitosi attiva** (5112 contro 4), e `CALORE_VETTORIALE` spento.

**⚠ E c'è un conto che posso già fare**, come nel giro scorso: **se anche qui i fermi fossero al
pavimento, `eta` crescerebbe di `DT·r_floor` = `1.414e-08` per passo.** **È il discriminante, ed è
lo stesso che ha funzionato su `Z46`.**

---

## 2. PROGETTAZIONE

**Il run:** il driver, **400 frame**, snapshot ai frame **10 / 115 / 190 / 270 / 375** *(gli stessi
della tabella del mandato)*. **Nessun rendering.** **`.pkl` documentato in `INVENTARIO`.**

**①** frazione con `x = 0`, **Jaccard** fra istanti, **e il RAGGIO mediano dei fermi** — `~8` (le
masse), `~0` (il centro), o distribuito (il guscio).
**②** `eta` dei fermi contro la popolazione, **quanti sono NATI dopo il frame 0** *(indice ≥ n₀:
esatto)*, e la frazione di neonati sul totale.
**③** profilo **radiale** di `rho_spin`, `|psi|`, coerenza locale **ed `eta`** — **e la domanda che
decide: il guscio coincide coi nodi a `eta` bassa?**
**④** `perc_chi`: distribuzione nel tempo, **i rami di mitosi CONTATI** (A8), il segno dei fermi e
quello del guscio.

**⚠ IL PRESIDIO DEL §3 CHE APPLICO PER PRIMO:** se la distribuzione di `x` è **bimodale** come in
`Z46` *(`0` contro `10⁸`)*, **NON riporto mediane: riporto le due popolazioni separate.** Una
mediana fra due popolazioni distinte **non descrive nessuna delle due** (A3c).

**LE LETTURE, FISSATE ADESSO:**
- **raggio dei fermi ~8** → come nel batch: **sono le masse**;
- **raggio ~0** → **sono il centro**: l'opposto del batch, e va detto;
- **raggio distribuito / coincidente col guscio** → **i fermi SONO il guscio**;
- **Jaccard < 1** → **è un flusso**, e allora il tasso di mitosi conta;
- **`eta` del guscio bassa** → **il guscio è il FRONTE DI NASCITA, non una parete**, e **la lettura
  del video va corretta.**

**COSA MI FA FERMARE:** se il run diverge o supera nettamente la stima. **In ogni caso nessuna cura,
nessun verdetto di fisica, nessuna identificazione.**

---

## 3. TODO DEL NEXT STEP

- [ ] previsioni qualitative → **commit PRIMA del run**
- [ ] il run: 400 frame, snapshot a 10/115/190/270/375, `.pkl` in `INVENTARIO`
- [ ] **①** chi non ruota: frazione, Jaccard, **raggio**
- [ ] **②** età anagrafica e neonati
- [ ] **③** profilo radiale — **il guscio coincide coi nodi giovani?**
- [ ] **④** `perc_chi`, coi rami di mitosi **contati**
- [ ] referto **senza verdetto** + registro *(`Z46` QUALIFICATA «vale per il batch», non corretta)*
      + relazione + **CHECKPOINT**
- [ ] **⚠ NON toccare:** niente cure, niente default, nessuna identificazione di fisica
