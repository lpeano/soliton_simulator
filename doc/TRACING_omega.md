# TRACING di `omega` — **il controllo ha stanato un termine mancante, ed era MIO**

> **Scritto per Claude web** (regola §5-ter). Branch `fork-su2`, 2026-09-15. Blob **`f5887254`**.
> **Nessuna modifica alla fisica.** Criterio scritto e committato **prima** dei dati
> (`075a09f`, + esito (IV) in `457abe4`).
> **Stato: run corretto IN VOLO.** I numeri qui sotto vengono dal run **INCOMPLETO**, conservato
> come evidenza in `csv/_test_fork/_tracing_omega_INCOMPLETO.txt`.

---

## 1. IL RISCONTRO IN UNA RIGA

> **Il controllo di direzione che avevo aggiunto al criterio ha fatto esattamente il suo lavoro:
> ha stanato un termine mancante. Il termine mancava nella MIA ricostruzione, non nel simulatore.**

`correzione` ha **due** termini, righe **1895-1901**, e io ne avevo ricostruito **uno**:

```python
correzione = np.cross(B, nb)
if CAMPO_SPINORIALE:                                   # <-- ATTIVO nei run del fork
    correzione = correzione + np.cross(self._nb_grav(), nb)
```

Il secondo è il torque verso il Bloch del **campo emesso spinoriale**. Nei run del fork
`--campo-spinoriale` è **acceso**, quindi quel termine **c'è sempre** — e la mia catena lo ignorava.

## 2. COME È STATO STANATO — il controllo, non l'occhio

Nel criterio (§IV.4, scritto **prima**) avevo messo un controllo interno sulla **direzione** del
residuo, perché un `R_stoc` alto ha due cause possibili: rumore genuino, **oppure un mio errore**.

> `cos(stoc_vec, det_vec)` ≈ **0** → residuo isotropo, coerente con **rumore**;
> ≈ **±1** → residuo **allineato** al deterministico → **errore sistematico della ricostruzione**,
> e in quel caso **(IV) NON si dichiara**.

**Misurato: `cos = +0.643`**, ben oltre la soglia di veto `0.5`, e **stabile** su tutti gli otto
campioni (`+0.348, +0.349, +0.566, +0.403, +0.452, +0.451, +0.407, +0.643`).

Un residuo **allineato e persistente** non è rumore: è un **pezzo di formula che manca**.
E l'ampiezza torna: con `R_stoc ≈ 2.8` e `cos ≈ 0.64`, il deterministico vero è circa
`1 + R·cos ≈ 2.8×` quello che ricostruivo — cioè **mancava un termine dello stesso ordine del primo**.

> **Senza quel controllo avrei dichiarato l'ESITO (IV)** — «è il rumore che guida `omega`» —
> con `R_stoc` fra 13 e 2.8 a sostenerlo. **Sarebbe stato un falso positivo**, e sarebbe stato
> attribuito al rumore un effetto che è una riga di codice.

## 3. I NUMERI DEL RUN INCOMPLETO — da rifare, ma non da buttare

Quello che segue è **calcolato con mezza coppia**. Lo riporto perché documenta come il difetto si è
manifestato, **non** come misura della fisica.

| pendenza su `log inerzia` (passo 400, 2781 nodi) | valore | r |
|---|---|---|
| `\|B\|` | −0.534 | −0.858 |
| **angolo (B,nb)** | **−0.006** | **−0.025** |
| `\|correzione\|` (incompleta) | −0.538 | −0.820 |
| `coppia/inerzia` (incompleta) | −1.538 | −0.971 |
| `\|om_src\|/tau` | −1.980 | −0.935 |
| `theta` | **−0.113** | −0.353 |

```
rapporto mediano (coppia/inerzia) / (|om_src|/tau) = 73.88
angolo (B,nb) mediano = 59.38 gradi     amp (rumore su nb) mediana = 0.06887
R_stoc mediana = 2.785     cos(stoc,det) = +0.643     errore atteso ricostruzione = 0.099
```

**Tre cose che questi numeri dicono comunque, e che il termine mancante non cambia:**

1. **Il termine dissipativo NON domina.** Il rapporto coppia/dissipazione è **73.88**: l'ipotesi
   «`omega` è governato dal rilassamento» (§4 del criterio) è **esclusa**, non rinviata.
2. **L'angolo `(B, nb)` è PIATTO** — pendenza `−0.006`, `r = −0.025`, mediana **59.4°**. Non c'è
   nessun allineamento crescente con la densità: **l'esito (II-b) è escluso**, e lo è in modo
   robusto, perché l'angolo non dipende dal termine che mancava (`B` è ricostruito **esatto**).
3. **`|B|` DECRESCE** con l'inerzia (−0.534), non cresce: **(II-a) è escluso**.
4. Il `theta` misurato qui, **−0.113**, coincide con il **−0.106** misurato indipendentemente dal
   test trasversale di ieri: **le due misure si confermano a vicenda.**

## 4. COSA RESTA DA STABILIRE

Il verdetto stampato dal run incompleto era **(I)** — colpevole a valle. **Non lo dichiaro**: era
calcolato con `coppia/inerzia` dimezzata, e il secondo termine può cambiarne la pendenza. Il run
corretto è in volo, con il tracer **ri-sigillato PASS** dopo la modifica e **prima** dell'uso.

## 5. COSA NON È STATO TOCCATO

`soliton_simulator.py` **non è stato modificato**: blob `f5887254`, `git status` pulito. L'errore era
**nella mia ricostruzione**, non nel simulatore, e la correzione è avvenuta **solo nel tracer**.
