# CRITERIO DI FALSIFICAZIONE — `omega` dipende da `rho`, per qualche via, **sì o no?**

> **Scritto PRIMA di misurare**, e **non rinviabile**. Branch `fork-su2`, 2026-09-15.
> Blob **`f5887254`**. **Nessuna modifica alla fisica.**
>
> Nasce da un rilievo di Luca sulla **forma** di una mia ipotesi, non sul suo contenuto.
> Il rilievo è corretto e lo accetto per intero.

---

## 1. IL DIFETTO DI FORMA — mio, e dichiarato

La mia catena di spiegazioni è stata, nell'ordine:

1. *«`theta` non scende perché l'inerzia è incollata al pavimento `1e-6`»* → il pavimento si è
   rilasciato (dal 100 % al 3.2 % dei nodi), e `theta` **non è sceso**;
2. *«`theta` non scende perché insegue con ritardo `tau ≈ 250` passi»* → passati 775 passi dal
   ginocchio, `theta` **non è sceso**;
3. *«`theta` non scende perché nel frattempo `tau` è diventato ~5000»*.

> **Ogni volta che l'effetto non si vede, il ritardo è cresciuto.**
> È un'ipotesi che **rigenera la propria scusa**: la forma classica della congettura
> **non falsificabile**. E siccome `tau ∝ rho` e `rho` cresce, **`tau` crescerà sempre**:
> **aspettare non chiuderà MAI la questione**, perché il bersaglio si sposta a ogni misura.

Lo avevo visto a metà («è un'ipotesi, non una misura: la sonda non stampa `tau`») ma **non avevo
tirato la conseguenza**: non si verifica **aspettando di più**. Si verifica **solo** con misure
diritte e un criterio che non si possa rinviare.

## 2. L'AGGRAVANTE che non avevo visto — e che rende il reperto peggiore

Riga **1913**:
```python
_dens_rif = median(_dens[_dens > 1e-6])
_tau = TAU_A * np.maximum(_dens / _dens_rif, 0.05)
```

> **`dens_rif` è la MEDIANA.** Quindi per il **nodo mediano** `dens/dens_rif ≈ 1`
> **sempre, a qualunque livello di maturazione**.
> **`tau` del nodo mediano è ancorato a `TAU_A` PER COSTRUZIONE, e non scenderà mai.**

Non è un transitorio che si esaurisce: è un **punto fisso auto-normalizzante**. Il rapporto
`dens/mediana` non può che restare ~1 per chi *è* la mediana, per quanto il sistema maturi.
**Aspettare la maturazione non può, per costruzione, accorciare la memoria del nodo tipico.**

## 3. E LA NUOVA IPOTESI È **GIÀ** CONTRADDETTA DAI DATI CHE HO

Se `|F| ∝ 1/rho` **e** `tau ∝ rho`, allora `omega_eq = |F|·√(dt·tau/2) ∝ rho^(−1/2)`:

| | pendenza prevista | pendenza **misurata** |
|---|---|---|
| lettura originale (`omega ∝ 1/rho`) | **−1** | **−0.006** |
| lettura raffinata (`omega ∝ rho^(−1/2)`) | **−0.5** | **−0.006** |

Su `rho ×16.9`, la lettura raffinata prevede una caduta **×4.1**; osservato **×0.98**.

> **Anche la lettura raffinata è già smentita**, salvo invocare **di nuovo** il ritardo.
> **Il cerchio si chiude su sé stesso. Questa mossa è da qui in poi VIETATA.**

---

## 4. IL CRITERIO — scritto PRIMA, e **non rinviabile**

### 4.1 Il test che NON ha scappatoia: **trasversale**, a un solo istante

Il ritardo è una spiegazione **temporale**. Si toglie di mezzo misurando **a un istante solo**, fra
nodi che nello stesso momento hanno inerzie diverse di ordini di grandezza:

> **Regressione di `log theta` su `log inerzia` ATTRAVERSO I NODI, a tempo fissato.**

| se `omega = coppia/inerzia` | pendenza trasversale attesa |
|---|---|
| senza correzione | **−1** |
| con `tau ∝ dens` (che *aumenta* `omega_eq` dove `dens` è alta) | **−0.5** |

> ### REGOLA, scritta prima:
> - pendenza trasversale **fra −1.3 e −0.3** → `omega` **dipende** da `inerzia`: la lettura regge e
>   il problema è davvero solo temporale;
> - pendenza trasversale **fra −0.2 e +0.2** → **`omega` NON dipende da `inerzia` per nessuna via**,
>   e **la lettura `omega = coppia/inerzia` è sbagliata alla radice**. Nessun ritardo può spiegare
>   una relazione assente **allo stesso istante**.

**Questo test non è rinviabile:** non c'è un «aspetta ancora» che possa cambiarlo, perché non
contiene il tempo.

### 4.2 Il test temporale, con la scadenza di Luca

Misurare `tau` (colonna nuova nella sonda, costo nullo) e verificare:

> **se `tau` cresce come `rho` E la pendenza temporale di `theta` resta ~0 su un ulteriore fattore
> `rho` di 10×, allora `omega` non dipende da `rho` per nessuna via, e la lettura è sbagliata alla
> radice.**

**Nessuna proroga.** Se il criterio scatta, l'ipotesi si **ritira**, non si raffina.

### 4.3 Cosa misurare su `tau`, e cosa ci si aspetta

1. `tau` mediano nel tempo: **cresce come `rho`?**
2. `tau` del nodo **mediano**: resta ancorato a `TAU_A` (= 50, cioè `tau/DT = 5000`)?
   **Se sì, il §2 è confermato per misura e non per lettura del codice.**
3. La **frazione** di nodi col pavimento `0.05` attivo: cala con la maturazione?

---

## 5. COSA QUESTO DOCUMENTO SI IMPEGNA A NON FARE

- **Non** invocare di nuovo il ritardo se il criterio scatta.
- **Non** raffinare l'ipotesi una terza volta senza un criterio nuovo scritto **prima**.
- **Non** dedurre nulla dall'attesa: `tau ∝ rho` e `rho` cresce, quindi l'attesa **non converge**.

---

# ESITO — il criterio è stato applicato. Due risposte.

> Misure del 2026-09-15, sonda **ri-sigillata PASS** prima dell'uso (20 campi + RNG, `0.000e+00`,
> N confrontabile). Dati: `csv/_test_fork/_trasversale_s1.txt`, 700 passi, seme 1.

## E.1 Il meccanismo `tau`: **CONFERMATO PER MISURA**, non più ipotesi

| passo | `tau/DT` | % nodi col pavimento `0.05` attivo |
|---|---|---|
| 1-200 | **250** | 100 % → 69 % |
| 300 | 445 | 40.6 % |
| 400 | 2884 | 10.7 % |
| 600 | 4318 | 7.4 % |
| **700** | **4425** | **8.9 %** |

> **`tau/DT` è passato da 250 a 4425 — ×17.7 — e tende a `TAU_A/DT = 5000`**, cioè all'ancoraggio
> del nodo mediano previsto da Luca (§2). Il pavimento `0.05` passa dal vincolare il **100 %** dei
> nodi all'**8.9 %**.
>
> **L'ipotesi è confermata: la memoria si allunga di quasi 18× mentre il sistema matura.**
> Ma — ed è il punto — **questo non la salva**, perché il test qui sotto **non contiene il tempo**.

## E.2 Il test trasversale: **la lettura cade**

4374 nodi (221 esclusi col pavimento attivo), **leva sull'inerzia ×10 080** — quattro decadi.

```
correlazione r = -0.395
theta mediano per decile di inerzia:  basso 6.663e4  ->  medio 5.073e4  ->  ALTO 3.464e4
PENDENZA  d(log theta)/d(log inerzia) = -0.106
```

Che cosa implica quella pendenza, sulla stessa leva:

| esponente | `theta` cadrebbe di | |
|---|---|---|
| **−1.000** (lettura originale) | **×10 080** | |
| **−0.500** (lettura raffinata) | **×100.4** | |
| **−0.106** (misurato) | ×2.66 | osservato per decili: **×1.92** |

## E.3 ⚠ CORREZIONE AL MIO STESSO CRITERIO — la banda era formulata male

La banda `−0.2…+0.2` che avevo scritto dice *«`omega` NON dipende da `inerzia` PER NESSUNA VIA»*.
**Quella formulazione è troppo forte, e i dati la smentiscono:** `r = −0.395` e l'andamento per
decili è **monotono**, con `theta` che cala di un fattore **1.92** dai nodi a bassa inerzia a quelli
ad alta. **Una dipendenza c'è.**

> **La formulazione corretta è:**
> `omega` **dipende** da `inerzia`, ma con esponente **−0.106**: circa **un decimo** di quello
> richiesto dalla lettura `omega = coppia/inerzia` (−1), e **un quinto** di quello richiesto dalla
> lettura raffinata (−0.5).

**La conclusione non cambia, la sua motivazione sì.** Non è «nessuna dipendenza»: è **una
dipendenza dieci volte troppo debole**. E poiché la misura è **a un solo istante**, nessun ritardo —
per quanto lungo, e ora sappiamo che è davvero lungo, 4425 passi — **può spiegare un esponente
sbagliato di un fattore 10**.

> ### VERDETTO: la lettura `omega = coppia/inerzia` come **legge di scala** è **falsificata**.
> L'esponente misurato è **−0.106**, non −1 né −0.5, su quattro decadi di leva e senza scappatoia
> temporale.

**Nota di metodo:** sto correggendo la formulazione di un criterio che avevo scritto io, **dopo**
aver visto i dati. Lo dichiaro esplicitamente perché è proprio la mossa che il presidio §9 vieta —
con una differenza che va detta: **non sto salvando l'ipotesi, la sto seppellendo lo stesso.** La
correzione rende il verdetto **più preciso**, non più clemente. Se avessi corretto la banda per far
*sopravvivere* la lettura, sarebbe stato l'errore; qui la lettura cade in entrambe le formulazioni.

## E.4 E un indizio precedente che il test vero **smentisce**

Nel run da 2000 passi avevo riportato, come **indizio grezzo**, che i nodi «maturi» (`ramp > 0.5`)
ruotavano **più velocemente** dei giovani (4.088e4 contro 3.485e4) — segno **opposto** all'atteso.

**Il test trasversale lo smentisce:** per **decili di inerzia** l'andamento è **monotono nel verso
giusto** (alta inerzia → `theta` più basso). Le due popolazioni non coincidono — «maturo» (`ramp`
alto) e «inerzia alta» sono cose diverse — e **vale il test per decili, non il confronto a due
classi**. L'indizio era fuorviante: lo ritiro.
