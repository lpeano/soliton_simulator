# REFERTO — **R6 blocca: `_pesi()` legge la cache 16 volte per passo, 9 prima e 7 dopo.** A6 sarebbe violato in modo permanente

**Blob:** `69ee5403` (byte grezzi `ee0c2a60`), HEAD `f349654`. **Nessun codice toccato.**

Il mandato §2.5/R6: *«**Se legge come `_passo_spinoriale` (3.03 %), è un REPERTO: significa che il
fallback dipende da QUANDO nel passo si legge. Riporta e FERMATI prima di cablare.**»*
**Legge 7.82 %, diverso da entrambi — e la ragione è peggiore di quella temuta.**

---

## 1. IL REPERTO — **`_pesi()` è chiamata SEDICI volte per passo, a cavallo della scrittura della cache**

```
passo    _pesi() PRIMA della scrittura di _cs_nodo_prev    DOPO
  0              12                                          7      (+ 19 con cache assente)
  1               9                                          7
  2               9                                          7
  3               9                                          7
  4               9                                          7
  5               9                                          7
TOTALE su 10 passi: 93 PRIMA, 70 DOPO
```

> **Dentro lo STESSO passo, `_pesi()` gira 16 volte: 9 PRIMA che `_cs_nodo_prev` sia aggiornata
> (`:3213`) e 7 DOPO.**
> **Se il `ramp` usasse `_tempo_luce_nodo`, 9 chiamate userebbero il `cs` del passo PRECEDENTE
> (A6 ✓) e 7 quello CORRENTE (A6 ✗).**
> **Non è il transitorio: è 9/7 a OGNI passo, in modo permanente. Sarebbe una violazione di A6 su
> 7 chiamate su 16 — il 44 %.**

**E il valore della maturazione dipenderebbe da QUALE delle sedici chiamate la calcola**, cioè da un
dettaglio di implementazione, **non dalla fisica.**

### Il terzo lettore, contro i due già misurati

```
_cs_nodo_prev  letta da _tempo_luce_nodo   :  0.0000 %   (0 su 62)
_cs_nodo_prev  letta da _passo_spinoriale  :  3.0303 %   (2 su 66)
_cs_nodo_prev  letta da _pesi()            :  7.8189 %   (19 su 243)   <- QUESTO
```

**Tre lettori della stessa cache, tre frazioni diverse.** I 19 fallback di `_pesi()` sono **tutti al
passo 0** (cache inesistente, `len = -1`), quindi la frazione alta viene dal **numero di chiamate**,
non da un comportamento peggiore. **Ma è proprio questo il punto di A8b:** la frazione di un
fallback **non è una proprietà della cache, è una proprietà del consumatore** — e finché ogni
consumatore non è contato **separatamente**, quel numero non significa niente.

---

## 2. LE ALTRE QUATTRO VERIFICHE — **passano, e la diagnosi di Z9 regge**

**2.1 — `_tempo_luce_nodo` è chiamabile e non ricorsivo.** Restituisce **per NODO** (`shape n`),
**non chiama `_pesi()`** → nessuna ricorsione. Nessun ricalcolo richiesto.

**2.2 — nodi isolati: ZERO.**
```
nodi isolati (grado 0) : 0  su 87120 nodi-chiamata
d_nodo  min 1.4799   mediana 1.6338
```
> **`LAM` non entrerebbe MAI nella maturazione** per la via dei nodi isolati. Il divieto del
> mandato §6 (*«non usare `LAM`»*) **è rispettato di fatto**: la scala è `d_nodo`, media degli archi
> incidenti, e il ramo `d_nodo[grado <= 0] = LAM` **non scatta mai** in questo scenario.
> *(Resta un ramo da contare, per A8: oggi non lo è.)*

**E l'ordine di grandezza conferma la diagnosi:** `d_nodo ~ 1.63`, `cs ~ 2.0` → tempo-luce **~0.82**
contro `TAU_A = 50`. Con `eta` che cresce di ~0.009 per passo, `ramp = 1` arriverebbe **entro un
centinaio di passi** — **dentro la durata dei run**, che è esattamente ciò che Z9 chiede.

**2.3 — A6:** è il punto che il §1 blocca. `eta` è aggiornata a `:2958`, la cache a `:3213`, `d` a
`:3318`; **ma `_pesi()` non ha una riga fissa** — la chiama `calcola_psi()`, da più punti, **16
volte per passo**.

**2.4 — `TAU_A` non compare altrove.** Rienumerato sul blob attuale: i tre punti noti
(`:2226`, `:2229`, `:2429`), la definizione (`:120`/`:125`/`:267`) e `--regime` (`:6950`/`:6952`).
**Nessun punto nuovo.**

---

## 3. COSA LO SBLOCCHEREBBE — **e non lo cablo**

**Uno SNAPSHOT del tempo-luce per nodo, calcolato UNA VOLTA per passo**, all'inizio di `step()`, e
letto da tutte e sedici le chiamate:

- **risolve A6** — un solo istante, quello precedente, per tutte le chiamate;
- **risolve la dipendenza dall'ordine** — il valore non dipende più da *quale* chiamata;
- **e riduce il costo**: oggi significherebbe 16 valutazioni per passo invece di una.

**MA è uno snapshot nuovo, e A8b impone il prezzo che questo repo ha già pagato due volte**
(`_cs_nodo_prev` **71.88 %**, `_psi_spin_prec` **95.33 %**): **va esteso a TUTTI e cinque i punti di
crescita** (`:1855`, `:3305`, `:3422`, `:3482`, `:3560`) **e contato**. Il mandato lo dice
esplicitamente: *«Due volte è bastato.»*

**Aggiungere stato persistente al simulatore per una correzione non ancora autorizzata sarebbe
cablarla a metà** — e lo stato sopravviverebbe alla decisione di non farla. **È la stessa ragione per
cui non ho aggiunto `_cs_arco_ultimo` per ⑥.**

---

## 4. COSA RESTA STABILITO

- **Z9 è reale e la diagnosi del mandato è giusta:** il tempo-luce del nodo (~0.82) porterebbe la
  maturità **dentro la durata dei run**, contro i ~5526 passi di oggi.
- **La separazione delle due leggi è la cura giusta**, e `_tau` non verrebbe toccato.
- **`LAM` non entra**, verificato: zero nodi isolati.
- **Il blocco non è sulla LEGGE: è sul PUNTO in cui verrebbe valutata.**

**Serve una decisione su una riga sola:** *si aggiunge uno snapshot per-passo del tempo-luce nodale,
con estensione ai cinque punti di crescita e contatore?* **Se sì, la correzione è realizzabile e i
sigilli R0-R11 sono scrivibili. Se no, il `ramp` non può leggere `cs` senza violare A6 su 7
chiamate su 16.**
