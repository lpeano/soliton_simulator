# TASK HISTORY — **`Z33`: la cura dell'ordine/snapshot, e il dubbio che va sciolto PRIMA**

**Data:** 2026-09-18 · **Branch** `fork-su2` · **HEAD alla scrittura** `680d069`
**Blob:** `72acd6aa` (git) / `aa84755b` (byte)
**Task:** il contatore (§6.2), le due vie coi numeri e il quarto caso (§6.3), poi la cura.

---

## 1. RAGIONAMENTO PRELIMINARE — *cosa credo prima di guardare*

### ⚠ Ho letto il ciclo per intero, e **la via (1) del mandato romperebbe A6**

`psi_spin` è assegnato in **UN SOLO punto**: `:2662`, **dentro `calcola_psi()`**, sotto
`if CAMPO_SPINORIALE`. E `ritmo()` gira a `:3093`, **all'inizio di `step()`**, *prima* che
`calcola_psi()` di quel passo venga chiamata.

**Quindi il ciclo normale è:**

```
passo k   : ritmo()  legge  psi_spin (prodotto da calcola_psi del passo k−1)  vs  _psi_spin_prec
            :3101    _psi_spin_prec = psi_spin.copy()        <- snapshot dello stato APPENA LETTO
            ...      calcola_psi()  RICALCOLA psi_spin       <- ora cambia
passo k+1 : ritmo()  legge il psi_spin NUOVO vs lo snapshot del passo k        ✓ CORRETTO
```

> **L'ordine attuale è GIUSTO, e rispetta A6:** il consumo legge uno stato `t−1`.
> **Spostare l'aggiornamento prima del consumo — la via (1) del mandato — farebbe confrontare
> `psi_spin` con SÉ STESSO nello stesso passo.** Sarebbe **il difetto, non la cura.**

**Questa è la prima cosa che va detta, e va detta prima di cablare qualunque cosa.**

### E allora perché degenera? — **perché `calcola_psi()` non ha ricalcolato `psi_spin` in mezzo**

`snap == True` significa che fra lo snapshot del passo `k` e il `ritmo()` del passo `k+1`
**`psi_spin` non è cambiato**. Le vie per cui può accadere, dal sorgente:

- **`calcola_psi()` esce prima** del blocco `CAMPO_SPINORIALE`: `:2640` ritorna se
  `self.n == 0 or not len(self.i)` — **nessun arco, nessun aggiornamento**;
- **le lunghezze non combaciano** e il guard di `:2038` scarta il ramo 4π.

### ⚠ E il dubbio vero: **i quattro casi sono davvero un difetto?**

**Li rileggo uno per uno, con quello che so adesso:**

| passo | cosa succede | **è un difetto?** |
|---|---|---|
| **0** | avvio: `len(_psi_spin_prec) = −1`, **non esiste uno stato precedente** | **NO.** `r = 1` è la risposta giusta: non c'è un «prima» |
| **1** | `psi_spin == _psi_spin_prec`, sistema appena seminato | **forse no**: se il campo non si è mosso, `f = 0` **è vero** |
| **6** | `440/80` dopo `nuova_massa`: guard 4π fallisce → 2π → anche lì corto → **ramo di sicurezza `:2028`** → `r = ones` | **NO: è il ramo di sicurezza che fa il suo mestiere.** I 360 nodi nuovi **non hanno un passato** |
| **7** | snapshot aggiornato, `max\|f\| = 3.55e-13` | **NO: è zero NUMERICO.** Il sistema davvero non si è mosso |

> **Il mio sospetto, e va misurato non assunto: NON C'È UN DIFETTO DA CURARE — c'è un difetto da
> DICHIARARE.** In tutti e quattro i casi **manca un passato con cui confrontarsi**, e il codice fa
> la cosa giusta. **Ciò che manca è che lo dica** (A8: un ramo silenzioso non è un ramo).

### E la via (2) — **estendere lo snapshot — INVENTA uno stato che non esiste**

`_eredita_spinore_figli` estende `_psi_spin_prec` alla **mitosi** (`:1349-1351`, la cura `C11`), ed è
**giustificato**: il figlio nasce dal padre, e **ereditarne la fase è fisica**.

**Ma `nuova_massa` crea nodi SENZA genitore.** Estendere lo snapshot lì significherebbe
**inventare una fase precedente** per nodi che non ne hanno una. **Sarebbe un numero scelto (A1) e
una storia falsa (A7b: uno stato non nasce indefinito — ma non nasce nemmeno con un passato).**

> **Quindi la via (2) risolve il passo 6 solo a prezzo di fabbricare un passato.** **Va detto, e non
> è una preferenza: è A1 + A7b.**

### Cosa NON so

- **non so se il passo 1 sia legittimo**: se `calcola_psi()` ha girato e `psi_spin` non è cambiato,
  `f = 0` è **vero**; se non ha girato, è un buco. **È la misura che decide.**
- **non so quanti punti di crescita esistano davvero** — vanno enumerati dal disco (§1.2 del
  mandato), non dalla memoria;
- **non so se `f` sia CONFRONTABILE fra passi** (§1.4, `K7`): se la fase salta di gauge, `f` è
  rumore anche quando non è zero. **Nessuno l'ha mai misurato su questo oggetto.**

---

## 2. PROGETTAZIONE DEL RAGIONAMENTO

**Passo 1 — IL CONTATORE, per primo e BYTE-INERTE** (§6.2 del mandato). Conta: `psi_spin` e
`_psi_spin_prec` **identici**; `f` **identicamente nullo**; il **guard 4π** che fallisce; il **ramo
di sicurezza `:2028`** che scatta. *Decide:* rende leggibile tutto il resto, **e sarebbe l'unica
cosa che manca se il sospetto di §1 è giusto.**

**Passo 2 — I PUNTI DI CRESCITA, enumerati dal disco.** Dove `n` cresce, e per ciascuno: lo snapshot
è esteso? *Decide:* la portata della via (2).

**Passo 3 — IL QUARTO CASO.** Il passo 7 ha `snap == False` e `max|f| = 3.55e-13`: **è zero numerico
o un residuo?** *Decide:* se è un reperto separato.

**Passo 4 — `K7`, LA CONFRONTABILITÀ.** `f` è continuo fra passi consecutivi, o salta? **È `G6`
applicata a `_psi_spin_prec`, e non l'ha fatto nessuno.** *Decide:* se sotto c'è un secondo difetto.

**LE LETTURE, FISSATE ADESSO:**
- **i quattro casi sono legittimi** *(manca un passato, il codice fa la cosa giusta)* → **la cura è
  il CONTATORE + la DICHIARAZIONE, non l'estensione.** **Si riporta e si chiede via libera.**
- **almeno uno è un buco vero** *(`calcola_psi` doveva girare e non l'ha fatto)* → **si cura quello**,
  e la cura è sull'**ordine delle chiamate**, non sullo snapshot;
- **la via (2) serve** → **allora va detto che inventa un passato**, e **il numero inventato va
  derivato o dichiarato**;
- **`K7` mostra salti di fase** → **secondo difetto sotto, e il primo diventa secondario.**

**COSA MI FA FERMARE:**
- se la via (1) risultasse davvero proposta come cura → **si riporta che romperebbe A6**, prima di
  tutto il resto;
- se l'estensione richiedesse un valore inventato → **si riporta e NON si cabla**: è A1.

**E una cosa che NON farò:** **non tocco il gauge** — la misura ha stabilito che non c'entra.

---

## 3. TODO DEL NEXT STEP

- [ ] **1** — il CONTATORE (A8), byte-inerte → commit **prima** di tutto il resto
- [ ] **2** — i punti di crescita di `n`, enumerati **dal disco**, e chi estende lo snapshot
- [ ] **3** — il QUARTO caso: zero numerico o reperto separato?
- [ ] **4** — `K7`: `f` è confrontabile fra passi consecutivi?
- [ ] **le due vie coi numeri + dichiarare quale cablare e perché** → **STOP e riporta**
- [ ] *(solo con via libera)* previsioni → cura → sigilli `K0-K9` → `Z9` rimisurata
- [ ] **⚠ NON toccare:** il gauge (`median(|f|)`, `max(...,1e-9)`, `+1e-6`)
