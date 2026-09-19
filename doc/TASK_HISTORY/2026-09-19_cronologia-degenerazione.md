# TASK HISTORY — **la cronologia della degenerazione: chi si muove per primo**

**Data** 2026-09-19 · **branch** `fork-su2` · **HEAD** `ebc440b` · **blob** `7c4dec1d` · albero
**pulito** · **45 snapshot**, passi 60-2700, cadenza 60.

> **NESSUN RUN NUOVO** *(salvo la rigiocata del §3, e solo se il §2 la indica)*. **NESSUNA CURA.**
> **Il simulatore non si tocca.** **Questa misura serve a TROVARE dove si rompe, non a confermare
> un'ipotesi** — oggi tre ipotesi pronte sono risultate false, e due erano di Claude web.

---

## 1. DUE SOGLIE **DERIVATE DAL CODICE**, non scelte

**Servono a datare la comparsa della bimodalità, che è essa stessa un evento.**

```python
:2122  r = x / np.sqrt(1.0 + x**2) + 1.0e-6      # satura a 1 per x -> inf
:2123  r_unit = 1.0 / np.sqrt(2.0) + 1.0e-6
:2124  r_normalized = r / r_unit                  # -> TETTO = sqrt(2) = 1.41421356
```

- **il TETTO di `ritmo()` è `√2`** *(e il pavimento è `√2·10⁻⁶`, che è esattamente il
  `1.414213e-06` misurato in `Z46`: conferma che la derivazione è giusta)*;
- **il grado di NASCITA è `2`** *(il figlio nasce al punto medio dell'arco con esattamente due
  archi, verso entrambi i genitori — `CLAUDE.md` §9)*.

> **Quindi «`_deg` p50 = 2» e «`_r_corrente` p75 = √2» NON sono soglie scelte da me: sono i due
> valori che il codice prescrive.** Datare quando vengono raggiunti è datare un evento
> **strutturale**, non superare una soglia arbitraria.

## 2. IL PUNTO DI ATTRAVERSAMENTO — **definito PRIMA di guardare i dati**

Per ogni grandezza `X` con valori `x₁ … x₄₅`:

```
lo = min(x),  hi = max(x)
soglia = sqrt(lo*hi)   se lo > 0      (meta' dell'escursione in scala LOG)
         (lo+hi)/2     altrimenti     (lineare: log non definito)
t50(X)  = il PRIMO passo in cui x >= soglia
```

**La scala logaritmica non è un vezzo:** `omega_s` va da `0` a `10⁵`, `d0` da `1` a `400`. Con una
soglia lineare il `t50` di una grandezza che cresce di cinque ordini cadrebbe **sempre alla fine**,
e l'ordine cronologico sarebbe un artefatto della scala.

## 3. LE QUATTRO LETTURE, **fissate PRIMA, coi numeri**

| # | condizione | conclusione |
|---|---|---|
| **A — EVENTO** | tutti i `t50` entro **2 snapshot (120 passi)** | **è un evento: si DATA e si va a vedere cosa accade lì** → §4 rigiocata |
| **B — UNA PRECEDE** | il `t50` minimo è almeno **3 snapshot (180 passi)** prima del secondo | **quella è la CANDIDATA CAUSA**, riportata col ritardo misurato |
| **C — GRADUALE** | ogni grandezza supera il **10 %** dell'escursione entro i primi 3 snapshot **e** nessun intervallo singolo ne porta più del **30 %** | **NON c'è transizione: il sistema era già così.** Il difetto è nella **FORMA DELLE LEGGI**, non in un evento |
| **D — NESSUNA** | nessuna delle tre | **si riporta così, senza inventarne una quinta** |

> **⚠ `C` è la lettura più scomoda, ed è quella da non scartare.** Se i numeri la indicano, il
> referto dice che **non esiste un punto in cui si rompe** — e che cercare *l'evento* era la
> domanda sbagliata.
> **⚠ `D` esiste perché le altre tre potrebbero non descrivere i dati.** Oggi è già successo tre
> volte che un'ipotesi pronta fosse falsa: la quarta casella è lì per non forzarne una.

## 4. LA RIGIOCATA — **solo se `A`, e solo in quell'intervallo**

`--db-rigioca <prima> <dopo>` con `--db-ogni 5` → **dodici istanti dentro la finestra invece di
due**. Costa ~60 passi; **il costo si MISURA, non si assume**.

**E porta il proprio sigillo:** lo stato finale **deve essere byte-identico** allo snapshot che
esiste già. **Se non lo è, la riproduzione non funziona e si FERMA** *(la ripresa è sigillata 5/5,
ma su 12 frame: qui sarebbe su una finestra diversa)*.

**La rigiocata userebbe `_scena_video_ripresa.py`** — il driver in uso durante il run è stato
ripristinato a `f14ea4bd` e **non ha `--riprendi`**. Va dichiarato nel referto.

## 5. I PRESIDI

- **BIMODALI:** al 2700 `_deg` (p50 `2`, p75 `501`) e `_r_corrente` (p75 al tetto) lo sono.
  **Percentili, MAI una mediana da sola** (A3c). **E si DATA il passo in cui la bimodalità compare.**
- **MEMORIA:** 45 snapshot × ~50 MB decompressi. **Uno alla volta**, solo i numeri trattenuti.
- **UN SEME, UNA SCENA.** `--tau-luce` sigillo **6/7**. Nessuna identificazione, nessun verdetto.

## 6. COSA MI FA FERMARE
- **la rigiocata che non combacia** → la riproduzione non funziona: **STOP e si riporta**;
- **le letture che non si applicano** → **si usa `D`**, non si allarga una delle altre tre;
- **un `t50` che dipende dalla scala** → lo dichiaro invece di sceglierne una comoda: per questo la
  regola log/lineare è scritta **qui**, prima di aver visto un numero.
