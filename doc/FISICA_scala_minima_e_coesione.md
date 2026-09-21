# FISICA -- **la scala minima `LAM`, e la coesione adimensionale**

> **La legge, la derivazione e il perche'** (par.5-novies §3). Flag `--scala-min` e `--coes-adim`,
> **OFF di default**, byte-inerti. Simulatore **`43972024`**.

---

## 1. `SCALA_MIN` -- **`LAM` e' la scala minima, e si fa rispettare senza creare movimento**

### Il problema
`LAM` e' la lunghezza d'onda del solitone fondamentale: **sotto, un solitone non esiste.** Il
vincolo era **gia' dichiarato nel file**, ma affidato a un **pavimento comovente** `f*median(d0)`
-- **che scende insieme a cio' che dovrebbe trattenere.** Misurato: il sistema vive fra il **26 %**
e il **55 %** sotto `LAM`.

### La legge
A **ogni scrittura**, con `x` il valore **prima di quella scrittura**:
```
incremento >= 0  ->  INTATTO, bit per bit
incremento <  0  ->  moltiplicato per max(0, 1 - LAM/x)
```

### ⚠ Perche' NON una rimappatura del valore -- **e questa e' la parte che conta**
Una mappa `L(x)` che porta ogni lunghezza sopra `LAM` sembra la strada ovvia. **Due candidate
naturali -- `LAM + x*exp(-LAM/x)` e `sqrt(x^2 + LAM^2)` -- soddisfano ogni criterio di forma**
(monotone, lisce, asintotiche a `LAM`, identita' a grande scala, zero coefficienti) **e sono
entrambe SBAGLIATE**, per una ragione che non sta nella curva:

> **NON SONO IDEMPOTENTI: `L(x) > x` anche per `x >> LAM`** (a `3*LAM`: **+4.98 %**).
> **E un pavimento viene applicato OGNI VOLTA -- sette volte per passo, per tremila passi.**
> Ne uscirebbe un'**espansione fabbricata dal vincolo stesso**, cioe' **proprio la grandezza che si
> vuole misurare.**

**Il criterio mancante non e' sulla forma, e' sull'operatore: `L(L(x)) == L(x)`.**
Lo smorzamento della discesa lo soddisfa **banalmente**, perche' **quando non si scende non tocca
niente**.

### Le quattro proprieta', dimostrate
1. **identita' esatta** per `dx >= 0` -- misurato `max|dx_eff - dx| = 0.0`, **zero esatto**;
2. **nessuna inflazione** -- il vincolo non aumenta mai una lunghezza;
3. **approccio asintotico**: `nuovo - LAM = (x - LAM) * (1 + dx/x)`, quindi la **distanza** da `LAM`
   si moltiplica per un fattore positivo: **`nuovo > LAM` sempre** e `LAM` **non si tocca mai**.
   *(Invariante verificato a `2.2e-15`; 200 dimezzamenti da `x = 5` convergono a `LAM` restando
   sopra.)*
4. **zero coefficienti** -- c'e' solo `LAM`.

### Tre cose dichiarate
- il **`max(0, .)`** e' un **obbligo di segno**, non una scelta: sotto `LAM` il fattore sarebbe
  negativo e **una discesa diventerebbe una salita**. A zero, una lunghezza gia' sotto **si
  congela**, non si teletrasporta;
- il caso **`dx <= -x`** *(la scrittura grezza porterebbe la lunghezza a zero o sotto)* **rompe la
  (3)** ed e' **CONTATO, non tappato**: nessun pavimento scelto, `_g_sm_patol` lo conta;
- **le nascite sono concatenazioni**, non discese: il troncone parte **da `LAM`**.

---

## 2. `COES_ADIM` -- **le dimensioni, e la densita' locale**

### Il problema
```
coesione = (CS_M^2 / I_med) * (forza_campo + richiamo) * filtro_portata * d0^2 * (I_arco / I_med)
forza_campo = -( dI/d  -  tanh(dI/I_med) * lap_arco )
```
**`dI/d` ha dimensioni `[I]/[L]` e `lap_arco` ha `[I]`: si SOMMANO due cose diverse.** E **`I_med`,
una MEDIA GLOBALE (`A2`), compare AL QUADRATO** al denominatore.

### La legge
```
F_adim = tanh( -( dI/I_arco - tanh(|dI/I_arco|) * lap_arco/I_arco ) + richiamo ) * filtro_portata
d0 += passo_causale * F_adim          passo_causale = LAM * sqrt(K_C) * DT
```
- i tre addendi sono **adimensionali con la densita' LOCALE dell'arco**;
- **`I_med` sparisce da entrambe le posizioni** -- e con essa una media globale;
- **`|F_adim| <= 1` PER COSTRUZIONE**, non per clip. **Per questo sostituisce
  `tanh(stress)*d0`**, che `Z79` ha misurato **saturo**.

### Le scelte dichiarate
- **`d0^2` si toglie**: col passo causale davanti lo spostamento **e' gia' una lunghezza**; per
  `d0^2` sarebbe una lunghezza **al cubo**;
- **`filtro_portata` si tiene**: adimensionale, in `[0,1]`, non rompe il limite, e la sua ragione
  e' **fisica** (corto raggio), non dimensionale. Tolto, la coesione agirebbe a qualunque distanza;
- **`I_arco` nel vuoto: NESSUN pavimento.** Dove e' esattamente zero il rapporto e' `0/0` e **si
  definisce ZERO** *(precedente dichiarato: `scala_p`, `Z67`)*; dove e' minuscolo ma non nullo il
  rapporto e' enorme **ma il `tanh` lo limita a 1**. **La limitatezza e' STRUTTURALE, non messa a
  mano** -- ed e' il motivo per cui questa forma non ha bisogno del numero che la vecchia avrebbe
  richiesto.

### ⚠ Cosa resta aperto
**`passo_causale * tanh(...)` fissa la MAGNITUDINE dello spostamento al passo causale.** Il tetto
causale e' un **limite** giusto -- niente puo' muoversi piu' in fretta del cono -- **ma usarlo come
SCALA della forza e' una scelta, non una derivazione.** **Dichiarato, non coperto.**
