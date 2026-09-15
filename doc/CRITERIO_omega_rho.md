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
