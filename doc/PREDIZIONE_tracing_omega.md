# CRITERIO DI LETTURA del tracing di `omega` — **scritto PRIMA di misurare**

> Branch `fork-su2`, 2026-09-15. Blob **`f5887254`**. **Nessuna modifica alla fisica.**
> Nessun run in volo quando questo è scritto. Il commit che contiene questo file **precede** quello
> dei dati.

---

## 1. PERCHÉ SERVE UN CRITERIO SCRITTO PRIMA

Si tracciano **nove grandezze** su venti nodi per centinaia di passi. **Con nove grandezze si trova
sempre qualcosa**, e quel qualcosa non è un risultato: è il rumore che assume la forma che gli si
chiede. Quindi la diagnosi deve cadere da un **confronto di due pendenze**, fissato adesso.

E una correzione di formulazione, che accetto: non è vero che *«qualcosa domina `omega` e nessuno sa
cosa»*. In ~6000 righe deterministiche **ogni termine è enumerabile**. La frase giusta è:

> **c'è un termine che domina `omega` e non l'abbiamo ancora cercato — ed è trovabile.**

Il precedente indica dove guardare: **tre volte** in due giorni un commento diceva una cosa e il
codice ne faceva un'altra (riga 2196; «`omega_s` conservativo» mentre rilassa; «il calcio alimenta
ogni passo» mentre è alla nascita). **Non si stana ragionando: si stana misurando ogni termine
separatamente.**

## 2. IL FATTO DA SPIEGARE

```
d(log theta)/d(log inerzia) = -0.106      richiesto da omega = coppia/inerzia:  -1
```
misurato **trasversalmente** (a un solo istante, 4374 nodi, leva ×10 080), quindi **nessun ritardo
può spiegarlo**. La domanda è: **dove, nella catena, l'esponente −1 si perde?**

---

## 3. IL CRITERIO — quattro esiti, decisi dalle pendenze

La grandezza-cerniera è **`|correzione| / inerzia`**, cioè l'ingresso del termine di coppia prima
che il rilassamento e il passo lo tocchino.

| esito | firma (pendenze trasversali su `log inerzia`) | dove è il colpevole |
|---|---|---|
| **(I)** | `\|correzione\|/inerzia` ≈ **−1** **ma** `theta` ≈ **−0.106** | **A VALLE** del rapporto: il rilassamento `omega_src/tau`, il fattore `dtn_c`, o il commit. **La formula d'ingresso è giusta, qualcosa dopo la annulla.** |
| **(II)** | `\|correzione\|/inerzia` ha **già** ≈ **−0.106** | **A MONTE**, dentro `correzione`. Si discrimina ancora: |
| **(II-a)** | `\|B\|` cresce con l'inerzia, pendenza ≈ **+0.9** | **il campo dai vicini scala come l'inerzia**, e il rapporto è quasi costante **per costruzione** |
| **(II-b)** | `\|B\|` piatto (≈ 0) **ma** l'angolo `(B, nb)` si **chiude** al crescere dell'inerzia | **è GEOMETRIA, non ampiezza**: nei nodi densi `B` e `nb` sono quasi allineati e `\|cross\| = \|B\|·sin(angolo)` crolla per allineamento |
| **(III)** | nessuna delle due | **reperto nuovo: si riportano i numeri e si FERMA.** Non si forza in una casella. |

> **La diagnosi è (I), (II-a), (II-b) o (III), e la decide il confronto delle pendenze, non
> l'impressione.**

**Soglie dichiarate ora**, per non aggiustarle dopo:
- «≈ −1» significa **pendenza ≤ −0.6**;
- «≈ −0.106» significa **pendenza in [−0.35, +0.15]**;
- «`|B|` cresce» significa **pendenza ≥ +0.5**; «`|B|` piatto» significa **|pendenza| ≤ 0.25**;
- «l'angolo si chiude» significa **pendenza dell'angolo (in gradi) ≤ −0.15**.

## 4. UNA SETTIMA GRANDEZZA CHE PUÒ RIBALTARE TUTTO

Oltre alla coppia c'è il **termine dissipativo**. La riga 1918 è
`omega_new = omega_src + dt·(correzione/inerzia − omega_src/tau)`: se **`|omega_src|/tau` domina
`|correzione|/inerzia`**, allora `omega` **non è governato dalla coppia affatto**, e l'esponente
della coppia è irrilevante per costruzione.

> Si riporta il **rapporto `(|correzione|/inerzia) / (|omega_src|/tau)`**.
> **Se è ≪ 1, il termine di coppia è marginale** e questo, da solo, spiega perché la sua pendenza non
> si trasmette a `theta`. **Sarebbe un esito (I) di forma particolarmente semplice.**

---

## 5. COSA IL TRACER RICOSTRUISCE ESATTAMENTE, E COSA NO — dichiarato prima

Il tracer **non può** entrare dentro `_passo_spinoriale`: ricostruisce i termini dagli array di
stato, su una **copia profonda** della rete (così anche le funzioni del simulatore che mutano cache
restano confinate lì).

| termine | ricostruzione |
|---|---|
| `inerzia`, `omega_src`, `eta`, `tau`, `psi` | **letti direttamente**: esatti |
| **`B`** | **ESATTO**: il codice costruisce `B` da `nb_vic = self._nb_prec` (riga 1854), cioè il Bloch **committato**, non quello rumoroso |
| **`correzione = cross(B, nb)`** | **APPROSSIMATO**: il codice usa `nb` **dopo** il rumore di riga 1847, che consuma `net.rng` e **non è riproducibile** senza perturbare il run |

**L'approssimazione, quantificata:** l'errore relativo su `correzione` è dell'ordine di
`|delta_nb| / sin(angolo)`, con `|delta_nb| ≈ amp·√2`. **Va riportato `amp` accanto all'angolo**: se
l'angolo è grande (decine di gradi) l'effetto è piccolo; **se l'angolo è piccolo, l'approssimazione
è FRAGILE proprio nel caso (II-b), e allora il verdetto (II-b) va dichiarato incerto.**
Questo limite è scritto **prima** di vedere i numeri, apposta.

## 6. DISCIPLINA

1. **~20 nodi, FISSI** per tutto il run (5 per quartile di `inerzia`, scelti al primo campione).
   I nodi non vengono **mai rimossi** dal simulatore (la mitosi solo **appende**), quindi gli indici
   restano validi: **si segue il padre**, e il figlio è un indice nuovo che **non** entra nel trace.
2. **Tutte le grandezze allo stesso istante**: gli ingressi si leggono **prima** del passo (sono
   `omega_src` e ciò che lo alimenta), l'uscita **dopo** (`omega_new`). Mai mescolare pre e post.
3. **PURE-READ con sigillo di byte-identità PRIMA dell'uso**, `0.000e+00` **e stesso N**.
4. **Niente medie globali** nel trace. Le **pendenze** invece sono regressioni **fra nodi singoli**,
   non medie: si calcolano su **tutti** i nodi, che è dove hanno potere statistico.
5. Run **corto** (300-500 passi): serve la **catena**, non la maturazione.

## 7. COSA QUESTO LAVORO NON FA

Non propone correzioni. **Prima si trova il termine, poi decide Luca.**

---

# AGGIUNTA AL CRITERIO — **ESITO (IV)**, scritto PRIMA dei dati

> Aggiunta posta da Luca, 2026-09-15. **Il tracer era in corso ed è stato FERMATO** per scriverla:
> i suoi dati sarebbero nati sotto un criterio incompleto, e una spiegazione aggiunta **dopo** averli
> visti è esattamente ciò che il §1 di questo stesso documento vieta.
> **Un criterio protegge solo dalle ipotesi che contiene.**

## IV.1 L'ipotesi

Il criterio come scritto copre tre colpevoli **deterministici** — a valle (I), ampiezza (II-a),
geometria (II-b) — più il reperto nuovo (III). **Manca il caso in cui `omega` non è governato da
NESSUN termine deterministico.**

> **(IV)** L'incremento di `omega` per passo non viene né dalla coppia (`correzione/inerzia`) né dal
> rilassamento (`omega_src/tau`), ma dal **RUMORE**.

Se fosse così:
- il rumore **non sa nulla dell'inerzia**, quindi **qualunque pendenza deterministica è irrilevante
  per costruzione**, e una pendenza debole come **−0.106** **non richiede nessun bug** per essere
  spiegata;
- un incremento stocastico indipendente per passo produce un **random walk**, cioè
  `omega ∝ √n` — **che è esattamente ciò che è già stato misurato**: `omega/√n` costante entro il
  **4.6 %** su 15 punti (`doc/ANALISI_gilbert_fdt.md` §2).

> **È l'unico esito che spiega INSIEME la pendenza −0.106 E il random walk.**
> Gli altri tre spiegano la pendenza e lasciano il random walk **senza causa**.

## IV.2 La firma da misurare

Si scompone l'incremento **effettivo** nelle sue due parti, **per nodo e per passo**, e come
**vettori** (non moduli: la direzione serve al controllo di IV.4):

```
Delta_vec = omega_new - omega_src                                  <- MISURATO
det_vec   = dt_n * ( correzione/inerzia - omega_src/tau )          <- quello che la riga 1918 prescrive
stoc_vec  = Delta_vec - det_vec                                    <- tutto il resto
R_stoc    = |stoc_vec| / |det_vec|
```

`stoc_vec` cattura il rumore **anche se entra a monte** (dentro `B` o `nb`): è per definizione la
parte di incremento che la formula, **valutata sugli ingressi tracciati**, non spiega.

## IV.3 LA LETTURA, fissata adesso

| `R_stoc` (mediana) | verdetto |
|---|---|
| **≥ 3** | **ESITO (IV): è il RUMORE che guida `omega`.** Le pendenze deterministiche sono irrilevanti; la −0.106 non è un bug ma **l'impronta di una dinamica stocastica**. |
| **0.3 … 3** | regime **MISTO**: nessuno dei due domina. **Si riporta come tale e non si sceglie.** |
| **≤ 0.3** | il rumore è marginale: **(IV) è ESCLUSO**, e la diagnosi resta fra (I), (II-a), (II-b), (III). |

## IV.4 IL CONTROLLO INTERNO — `R_stoc` alto potrebbe essere un MIO errore

`stoc_vec` è *«ciò che la mia ricostruzione non spiega»*. Un `R_stoc` alto ha **due** cause possibili:
**(a)** rumore genuino; **(b)** un errore sistematico nella mia ricostruzione. Vanno separate, e si
separano dalla **direzione**:

> Si riporta anche **`cos(stoc_vec, det_vec)`**, la coseno-similarità mediana fra le due parti.
> - **≈ 0** → le due parti sono **scorrelate in direzione**: coerente con **rumore isotropo**;
> - **≈ ±1** → `stoc_vec` è **allineato** (o antiallineato) a `det_vec`: è un **errore sistematico
>   della ricostruzione**, non rumore. **In quel caso (IV) NON si dichiara.**

E una **stima a priori** dell'errore di ricostruzione, per confronto: l'unica approssimazione nota è
`nb` rumoroso nel prodotto vettore (§5), che produce un errore relativo su `correzione` di ordine
`amp·√2 / sin(angolo)`. **Va riportato quel numero accanto a `R_stoc`:** se `R_stoc` lo supera di
molto, l'approssimazione **non può** spiegarlo.

## IV.5 PRESIDIO DI PUREZZA — non consumare l'RNG

Per ricostruire la parte deterministica serve `dt_n = DT·r`, cioè `ritmo()` — che **muta**
`_psi_prec`. Si chiama **sulla copia profonda**, e **prima** di `calcola_psi` (che sovrascriverebbe
`psi`, cambiando ciò che `ritmo()` legge). Inoltre si fa **snapshot/restore completo dello stato
dell'RNG** della rete vera attorno alla misura (§2.3), e **il sigillo lo verifica**.

> **Il generatore in sé non è in discussione.** È PCG64 con periodo 2^128, e le misure di questo
> repo concordano col caso ideale a quattro cifre (`chi = 90.000` contro il nullo 90.000, dispersione
> 39.2 contro 39.171): **un RNG difettoso non lo darebbe.** L'unico rischio è che il tracer
> **consumi** la sequenza, e quello si sigilla.
