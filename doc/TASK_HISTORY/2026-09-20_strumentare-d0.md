# 2026-09-20 — **STRUMENTARE `d0`: chi lo scrive, quanto, e su QUALE arco**

Mandato: strumentare **tutti** gli scrittori di `d0` + i pavimenti, sigillo **bloccante**, poi
rigiocare `0 -> 120` sul ramo B. **Nessuna cura in questo giro.**
**I due run sono FINITI** *(A ai 3000 alle 20:20, B fermato al 390)*: **la macchina e' libera e il
simulatore si puo' toccare.** Simulatore all'avvio `edb8f844` / git-blob `b44f50ce`. HEAD `77a174c`.

---

## 1. RAGIONAMENTO PRELIMINARE

### 1.1 ⚠ LA MIA ENUMERAZIONE ERA SBAGLIATA, e la correggo PRIMA di costruirci sopra

Avevo scritto *«`d0` ha DIECI scrittori»* (`Z78`, `77a174c`). **Rileggendo dal disco sono DODICI**,
piu' **sette** pavimenti:

```
SCRITTORI (12):  :2083  :4067  :4076  :4078  :4254  :4379  :4466  :4669  :4812  :4816  :4835  :4877
PAVIMENTI  (7):  :4080  :4255  :4670  :4817  :4836  :4878  :4917
```
**I due che mi erano sfuggiti:**
- **`:4078`** — `self.d0 += dt_e*(self.d - self.d0)/TAU_P`, **il ramo `else`** del rilassamento
  *(costante `TAU_P` invece di `tau_p_loc`)*. **L'avevo saltato perche' guardavo il ramo `if`;**
- **`:4812` e `:4816`** sono **DUE** scritture *(`spinta*median` e `grav*median`)*, e le avevo
  contate come una.

> **E' la stessa classe di errore che il mandato mi dice di non commettere** *(«NON assumere che la
> lista dei dieci sia completa»)*: **l'ho commessa nel referto precedente, e la quarta lettura del
> par.3 esiste proprio per questo.** **Lo strumento contera' DICIANNOVE punti, non dieci.**

### 1.2 ⚠ `_floor_d0` E' COMOVENTE — **e questo lo rende un candidato di prima fila**

```python
def _floor_d0(self):
    if not PAV_COM or not len(self.d0):
        return 0.05
    f = 0.05 / LAM_BASE                  # rapporto di nascita, adimensionale
    return f * float(np.median(self.d0))
```
**Il pavimento NON e' una costante: e' `f * median(d0)`.** **E' legato alla MEDIANA della stessa
grandezza che limita.**

> **E' la famiglia dei PUNTI FISSI gia' trovata quattro volte** *(`scala_p`, `median(|f|)` in
> `ritmo()`, `_dens_rif` in `_tau`, `u_nodo`)*, **e il mandato la nomina per prima.**
> **Se `median(d0)` scende, il pavimento scende con lei: un arco puo' restare "sopra il pavimento"
> mentre entrambi affondano.** **Un pavimento che insegue non ferma una discesa: la accompagna.**

### 1.3 Cosa NON so

- **non so se un pavimento morda sull'arco `16-481`.** Al passo 120 `d0 = 0.2425` e la mediana di
  `d0` vale `0.8021`: se `f ~ 0.05` il pavimento starebbe a `~0.04`, **sotto**. **Ma `f = 0.05/LAM_BASE`
  e `LAM_BASE` non l'ho letto:** va letto, non stimato;
- **non so quale dei dodici scrittori domini.** E' la domanda;
- **non so se la lista sia ORA completa.** L'ho gia' sbagliata una volta: la quarta lettura del
  par.3 del mandato resta viva, e se i numeri non chiudono **lo dico**.

### 1.4 Cosa mi aspetto (**non si riscrive se sbagliato**)

- **mi aspetto che il colpevole sia `:4877`** *(`coesione_relazionale`, in `memoria_hebbiana_moto`)*,
  perche' e' l'unico con un `clip` su un `tasso_dinamico` che scala con `d0` stesso;
- **mi aspetto che i pavimenti NON mordano** sull'arco osservato, perche' `0.2425` e' dieci volte
  il pavimento stimato;
- **mi aspetto piu' scrittori attivi insieme**, quindi la seconda lettura *(«competizione»)* piu'
  della prima *(«un colpevole»)*.

---

## 2. PROGETTAZIONE

### 2.1 La forma della strumentazione — **e perche' un contatore globale NON basta**

Il mandato lo dice: *«un contatore per scrittore dice QUANTE VOLTE, non SU QUALE ARCO»*.

**Sotto `TRACCIA_D0` (`False` di default), a ogni sito:**
```python
if TRACCIA_D0: _p = self.d0.copy()
<la scrittura esistente, INVARIATA>
if TRACCIA_D0: self._traccia_d0("nome_sito", _p)
```
**`_traccia_d0` registra, per gli archi TRACCIATI:**
- **il `d0` PRIMA e DOPO** *(non il delta soltanto: la coppia, cosi' un `max()` si distingue da una
  somma)*;
- **per i PAVIMENTI: quanti archi sono stati TAGLIATI** *(`d0_prima < pavimento`)* **e il valore del
  pavimento**. **Un pavimento non e' uno scrittore che spinge: e' un limite che taglia**, e il
  numero che lo dice e' *quanti ha tagliato*, non *quanto ha aggiunto*.

### 2.2 Quali archi si tracciano — **dichiarato, e in due livelli**

```
DETTAGLIO PIENO   l'arco 16-481, da solo: prima/dopo a ogni sito, a ogni passo
RIASSUNTO         tutti gli archi dei cinque nodi (~3100): per sito, quanti toccati,
                  SOMMA ALGEBRICA del delta, e max |delta|
GLOBALE           per sito: quante volte e' girato (costa nulla)
```
**La somma ALGEBRICA e non il conteggio**, perche' *«il conteggio da solo non dice chi spinge in
giu'»* — e' il criterio che avevo scritto io in `Z78`.

### 2.3 Il costo, stimato PRIMA
`19` siti x una `copy()` di un array da `528k` float64 = **4 MB per copia**, `19` copie per passo
= **76 MB/passo** di traffico di memoria. **A `~4.3 s/passo` e' trascurabile in tempo**, ma
**solo col flag ACCESO**. **A flag spento non si copia niente: e' un `if` su una globale.**

### 2.4 IL SIGILLO — i quattro criteri, e due sono bloccanti
```
Z0  riferimento: blob corrente, sha1 dei BYTE GREZZI (mai `git hash-object`, C18)
Z1  [BLOCCANTE] TRACCIA_D0 = False -> byte-identico al blob PRIMA. Una divergenza = STOP
Z2  controllo positivo: a True la traccia produce numeri NON banali (non tutti zero)
Z3  [BLOCCANTE] la rigiocata resta fedele: il sigillo interno che passo' 138/138 DEVE ripassare
```
**⚠ `Z3` e' il criterio che il mandato aggiunge e che non avrei messo:** se la strumentazione
cambia il PERCORSO *(una `copy()` in piu' non cambia la fisica, ma una riga messa nel posto
sbagliato si')*, **la rigiocata non riprodurrebbe piu' il ramo B e i numeri non varrebbero.**

### 2.5 LE LETTURE, fissate qui (sono quelle del mandato)
```
UN solo scrittore fa gli otto salti      -> e' il colpevole, e la cura e' li'
piu' scrittori si alternano              -> COMPETIZIONE, si descrive, non si sceglie
i salti coincidono con un PAVIMENTO      -> d0 non e' spinto giu': e' TAGLIATO. Cura diversa
nessuno dei 19 spiega il profilo         -> SI DICE: l'enumerazione ha mancato qualcosa
```

### 2.6 Cosa mi FERMA
- **`Z1` che fallisce** -> la strumentazione tocca la fisica: **STOP**, e si riporta;
- **`Z3` che fallisce** -> il percorso e' cambiato: **si corregge, non si giustifica**;
- **`LAM_BASE` non leggibile** -> il pavimento non e' calcolabile e va detto.

---

## 3. TODO
1. [ ] leggere `LAM_BASE` e calcolare il pavimento effettivo
2. [ ] la strumentazione dei **19** punti, **committata PRIMA del sigillo**
3. [ ] **Z0-Z3** -> **se `Z1` o `Z3` falliscono, STOP**
4. [ ] il replay `0 -> 120` col flag ACCESO -> **la tabella: chi scrive, quanto, chi taglia**
5. [ ] la voce nel registro -> **CHECKPOINT. Nessuna cura senza via libera.**
