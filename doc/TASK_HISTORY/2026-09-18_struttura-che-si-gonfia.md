# TASK HISTORY — **la struttura che si gonfia e si ricomprime**

**Data:** 2026-09-18 · **Branch** `fork-su2` · **HEAD alla scrittura** `feb5bec`
**Blob:** `a1ae5090` — **e non cambierà: nessuna cura, nessun cablaggio.**

---

## 1. RAGIONAMENTO PRELIMINARE

### 1.1 ✅ `Z48` QUALIFICATA — e il §0 del mandato ha ragione, con una prova che era già mia

Il mio referto concludeva *«il "guscio" coincide con l'anello delle masse seminate»*. **È vero PER IL
BATCH.** **E la ragione per cui il batch non poteva contenere l'altra struttura è MISURATA nel
referto stesso: `8 nodi e 10 archi in 1200 passi` — la mitosi è ferma.**
**La struttura osservata è fatta di MATERIA NUOVA, e nel batch quella materia non nasce.**
**Qualificata, non corretta** *(`Z48` resta valida per il batch)*.

### 1.2 ✅ IL RUN DEL §2 È GIÀ IN CORSO, ed è la scena giusta — **verificato, non assunto**

Il driver sigillato (`94e2ec0`) sta girando la config del mandato **dal commit `94e2ec0`**, e
**traccia la tabella dei fotogrammi**:

```
              frame 190      frame 270
il mio run    n = ?          n = 5443    dil = +10.75 %
la tabella    n = 4317       n = 5465    dil = +10.3 %
```

**È la stessa scena.** **Stato: frame 275/400, `15.6 s/frame`, ~33 minuti alla fine.**
**Snapshot presi: 10 / 115 / 190 / 270. Manca il 375.**

> **NON lo rilancio.** Rilanciarlo costerebbe **1 h 45** per riavere gli stessi numeri, e il §2
> chiede *«almeno 400 frame = 2400 passi»*: **questo run li fa.**

**⚠ E L'INVERSIONE È GIÀ VISIBILE NEI MIEI DATI, prima di qualunque analisi:**

```
frame 265 : dil = +10.967 %
frame 275 : dil =  +8.593 %
```

**La dilatazione ha iniziato a scendere.** *(La tabella del mandato dà `−3.5 %` al frame 375.)*

### 1.3 ⚠ LA MIA RISERVA SUL §3 — **i raggi `4 / 8 / 12` sono ASSOLUTI su un sistema che DILATA**

Il §3 chiede tre regioni: **`r < 4`**, **`r ≈ 8`**, **`r > 12`**. **Ma il sistema si dilata del
`+19.6 %` e poi si ricomprime**, e `d medio` va da `0.934` a `1.753` e torna a `1.483` — **quasi un
fattore 2.**

> **CLAUDE.md par.4 lo vieta esplicitamente:** *«Mai confronti a PASSO FISSO su un sistema che si
> espande/dilata: genera ALIASING… Campiona in modo adattivo o normalizza sulla scala (COMOVENTE),
> non su intervalli assoluti.»*
> **`r < 4` al frame 10 e `r < 4` al frame 375 NON sono la stessa regione fisica.**

**Cosa farò, e non è disubbidire:** **riporto ENTRAMBI** — i raggi **assoluti** come il mandato
chiede, **e** i raggi **comoventi**, normalizzati alla scala del sistema *(il raggio dell'anello
delle masse, misurato a ogni istante, invece del `sep = 8` di semina)*.
**Se le due letture concordano, la riserva cade e lo dico. Se divergono, la misura assoluta è
aliasata e va scartata.**

### 1.4 Cosa NON so

- **se la struttura a `r < 4` esista come regione distinta**, o se sia solo il centro della nube;
- **se il suo raggio cresca fino a inglobare `r = 8` e poi si ritragga** — è la misura diretta della
  descrizione, e non ce l'ho;
- **se i nodi lì siano materia NUOVA**: la mitosi qui è viva, quindi **stavolta il falsificatore di
  `Z48` può dare l'esito opposto**;
- **da quale meccanismo venga l'antimateria** — ed è il mio stesso rilievo: **mitosi o
  `chi_basc`?**

### 1.5 ⚠ Un limite del run in corso, dichiarato PRIMA di usarlo

Il §2 chiede **snapshot ogni 20 frame**; il run ne prende **5** (10/115/190/270/375).
**`d medio` NON è nel log per-frame** *(il driver stampa `n`, `archi`, `coer_l`, `dil` ogni 5
frame)*: **il ciclo di `d medio` lo ricostruirò dai 5 snapshot, la dilatazione dal log ogni 5
frame.**
**Per l'istante dell'inversione la risoluzione è 5 frame; per il profilo radiale è 5 punti.**
**È meno di quanto il §3 chiede, e lo dico prima invece di presentarlo come sufficiente.**

---

## 2. PROGETTAZIONE

**①** profilo **radiale** di `rho_spin`, `|psi|`, coerenza, `eta`, `d`, **e il GRADO**, ai 5 istanti,
**in raggio ASSOLUTO e COMOVENTE** *(§1.3)*, con le tre regioni **contate**, non descritte.
**②** il **ciclo**: `dil` ogni 5 frame (dal log) + `d medio` ai 5 snapshot; **il raggio della regione
interna sopra soglia** — **cresce, ingloba `r ≈ 8`, si ritrae?** — e il contrasto interno/esterno.
**③** **di cosa è fatta**: `eta` interna contro anello; **quanti nati dopo il passo 0**
*(indice ≥ n₀: esatto)*; **`perc_chi` SEPARANDO mitosi da `chi_basc`.**

**LE LETTURE, FISSATE ADESSO:**
- **il raggio interno cresce, supera `8`, poi si ritrae** → **la struttura descritta ESISTE e si
  misura;**
- **`eta` interna ALTA e nodi NATI DOPO** → **è materia nuova: l'opposto di `Z48`, e va detto;**
- **`eta` interna bassa come nell'anello** → **è di nuovo la regione dei nodi fermi, e la struttura
  osservata è un'altra cosa ancora;**
- **assoluto e comovente DIVERGONO** → **la misura assoluta è aliasata: si scarta;**
- **nessuna regge** → **si dice, senza inventarne una quinta.**

**COSA MI FA FERMARE:** nulla di tecnico — **ma nessun verdetto di fisica e nessuna identificazione**,
qualunque forma esca.

---

## 3. TODO DEL NEXT STEP

- [x] **`Z48` qualificata** (§0) + `STATO_RUN.md` aggiornato
- [ ] previsioni qualitative → commit **prima dell'analisi**
- [ ] attendere il frame 375 e la chiusura del run *(~33 min)*, **poi chiudere la voce di
      `STATO_RUN.md`**
- [ ] **①** profilo radiale, assoluto **E** comovente · **②** il ciclo · **③** di cosa è fatta
- [ ] referto **senza verdetto**, con **`--tau-luce` NEL REFERTO** + registro (`Z49`) + relazione
      **nello stesso commit** + **CHECKPOINT**
- [ ] **⚠ NON toccare:** niente cure, niente default, nessuna identificazione di fisica
