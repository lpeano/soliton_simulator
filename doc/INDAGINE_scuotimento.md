# INDAGINE — lo SCUOTIMENTO del vuoto: cos'e', dove vive, perche' e' gated da `SYNC_UPDATE`

> Sola lettura. Nessuna modifica a `soliton_simulator.py`. Blob indagato: **2277e9a0**
> (branch `fork-su2`, STRATO 1). Data: 2026-09-14.
> Scopo: capire, non cambiare. Le opzioni finali sono nominali; la decisione e' di Luca.

---

## 0. CORREZIONE PRELIMINARE — il mio Passo 0 era SBAGLIATO

Nel report del Passo 0 avevo concluso: *"lo scuotimento dei Bloch non gira nella config del
fork"*. **E' falso.** Avevo cercato il pattern `SYNC_UPDATE and SCUOTIMENTO`, trovato tre
occorrenze tutte nel ramo sincrono, e concluso dall'assenza. **Non avevo cercato il ramo
complementare**, che esiste ed e' a riga 1796:

```python
if SCUOTIMENTO and not SYNC_UPDATE:          # :1796
    ...
    self._nb = self._nb + self.rng.normal(0, 1.0, (n, 3)) * amp[:, None]    # :1803
```

**Lo scuotimento dei Bloch GIRA nella config certificata del fork.** Il gate non e' una
congiunzione che spegne: e' un **dispatch** fra due implementazioni della stessa legge, una per
ciascuno schema di aggiornamento. Errore di metodo, non di lettura: ho concluso da un `grep` di
un solo pattern invece di mappare tutte le sorgenti stocastiche (§0 di CLAUDE.md — *verifica dal
codice*, e verificalo **tutto**).

Quanto segue e' la mappa fatta come andava fatta.

---

## 1. LA MAPPA — tutte le perturbazioni stocastiche

Ogni `rng.normal` del file, con cosa perturba e chi lo gatta:

| riga | perturba | gate | gira nella config del fork? |
|---|---|---|---|
| [:537] `calcio = rng.normal * ampiezza` in `scuoti_vuoto` | `phivel` (**fase**), via stress metrico `d-d0` | `SCUOTIMENTO` ([:500]) | ✅ si |
| [:1803] `self._nb += rng.normal(0,1,(n,3)) * amp` | **BLOCH** (direzioni) | `SCUOTIMENTO and not SYNC_UPDATE` ([:1796]) | ✅ **si** |
| [:2005-2006] `a1,b1 += (normal + i·normal) * amp` | **SPINORE PRIMARIO** `_psi_spinor` | `SYNC_UPDATE and SCUOTIMENTO` ([:1999]) | ❌ no |
| [:2030] `nb_new += rng.normal(0,1,(n,3)) * amp` | Bloch, ramo NON-primario | `SYNC_UPDATE and SCUOTIMENTO` ([:2022]) | ❌ no (doppio: serve anche `not SPINORE_CORRETTO`) |
| [:1515] [:1520] [:1536] [:1538] [:1549] | inizializzazione (semina/calore iniziale) | `_CALORE_INIT` | una tantum, non e' scuotimento |
| [:3090] | `phi` alla mitosi | — | evento, non scuotimento |
| [:3808] [:4584] | utility / init `phivel` | — | — |

### I DUE oggetti distinti — conferma e correzione

La distinzione dello STATO e' **confermata a meta'**:

- ✅ **`scuoti_vuoto()`** ([:496]) e' un oggetto a se': gira **sempre** nel loop batch
  ([:5211] e [:5235], `scuoti_vuoto(net); net.step(); ...`), agisce sulla **fase** (`phivel`) via
  stress metrico `d-d0`, e **non tocca le direzioni di Bloch**. Corretto.
- ❌ **NON e' vero** che lo scuotimento dei Bloch viva solo nel ramo sincrono. Vive in **entrambi**,
  con due implementazioni diverse (righe 1803 e 2005/2030).

Le due leggi usano la **stessa ampiezza** — dichiarato nel commento a [:1794]: *"STESSA legge
dello scuotimento scalare: soppressione per COERENZA |Psi|^2, non per curvatura (le due leggi
devono essere identiche — il vuoto e' lo stesso vuoto)"*.

---

## 2. PERCHE' E' GATED DA `SYNC_UPDATE` — verdetto: **STRUTTURALE, e documentato**

### 2.1 La ragione e' scritta nel codice

Non e' "dov'e' capitato di scriverlo". Le due occorrenze sincrone portano la motivazione esplicita:

- [:2000] — *"eccitazione del vuoto sul PRIMARIO complesso (t->t+1): **perturba psi, non il B
  letto**"*
- [:2023] — *"**Il rumore e' un aggiornamento t -> t+1: non puo' contaminare il campo B letto
  dalla snapshot.** Usa comunque la stessa psi_t."*

E il ramo asincrono porta la sua, a [:1791]: *"ECCITAZIONE DEL VUOTO sullo spinore, integrata nel
passo (cosi' e' parte del ciclo di evoluzione fisica, non dipende dal loop di disegno)."*

**La logica e' coerente e ha senso fisico.** Nel ramo sincrono (Jacobi) tutte le leggi leggono una
snapshot immutabile di `t` ([:1782-1784], commento esplicito): iniettare rumore *prima* della
lettura contaminerebbe il campo `B` che i vicini leggono, rompendo la causalita' evaluate-then-commit.
Quindi li' il rumore va messo **al commit**, sull'oggetto che si sta committando (`a1,b1`).
Nel ramo asincrono non c'e' snapshot da proteggere, quindi il rumore si applica **a monte**, su
`self._nb`, ed entra naturalmente nel passo.

**Verdetto: il `SYNC_UPDATE and` / `and not SYNC_UPDATE` e' STRUTTURALE e motivato.** Non e' un
accidente da ripulire: e' la stessa legge scritta due volte perche' i due integratori richiedono
punti d'iniezione diversi.

### 2.2 Ma i due punti d'iniezione NON sono equivalenti

Questa e' la conseguenza che conta per il fork. Catena causale nella config certificata
(`--campo-spinoriale --spinore-vivo --spinore-corretto --deparam-orologio --verlet`, **senza**
`--sync`):

1. [:1803] il rumore perturba `self._nb`;
2. [:1805] `nb = self._nb` (lo shakerato);
3. [:1851] `correzione = np.cross(B, nb)` → entra in **`omega_new`** (il torque);
4. `omega_tot = omega_new` — nota: sotto `--deparam-orologio` il termine `omega_clk * nb` **non
   c'e'** ([:1926-1928]: *"PURA FASE: l'orologio NON entra nell'asse di rotazione"*), quindi
   l'unica via e' il torque;
5. [:1945-1948] lo spinore `a0,b0 = _psi_spinor` (stato `t-1`, **non** shakerato) ruota di
   `theta = |omega_tot| * dt`;
6. [:2034] **`self._nb = nb_new.copy()`** — il Bloch shakerato viene **sovrascritto** dalla
   proiezione del nuovo primario.

**Quindi:** nel ramo asincrono il rumore raggiunge `_psi_spinor` — che e' l'oggetto da cui il fork
costruisce la connessione — ma **solo attraverso il torque**, con ampiezza **O(amp · |B| · dt)**.
Nel ramo sincrono colpirebbe `a1,b1` **direttamente**, **O(amp)**. E lo shake su `self._nb` **non
si accumula**: viene riscritto a ogni passo.

Non e' "acceso contro spento": e' **diretto contro mediato, e soppresso da |B|·dt**.

---

## 3. COMPORTAMENTO — ampiezza misurata (pure-read, stato reale)

`amp = sqrt(Lam) / (1 + I2/Lam)`, con `Lam = lambda_vuoto(net) = <|Psi|^2>` ([:~490]).
Misurato sullo stato a 150 passi del run con memoria (`csv/_seal_fork/_s1_mem.pkl`, 3073 nodi):

**`Lam = 1.688e-04`, `sqrt(Lam) = 1.299e-02`**

| regione | `I2 = \|Psi\|^2` | `amp` | calcio angolare sul Bloch, per passo |
|---|---|---|---|
| VUOTO (I2 ≤ p10) | 2.88e-09 | **1.2993e-02** | ~2.25e-02 rad = **1.29 gradi** |
| tipico (p45–p55) | 2.62e-07 | 1.2974e-02 | ~1.29 gradi |
| MATERIA (I2 ≥ p90) | 7.73e-04 | 2.3292e-03 | ~0.23 gradi |
| PICCO (I2 ≥ p99) | 1.30e-03 | **1.4928e-03** | ~2.59e-03 rad = **0.148 gradi** |

**Rapporto vuoto/picco = 8.70.** La legge "forte nel vuoto, debole nella materia" e' **verificata
numericamente**, non solo asserita. Nota: la soppressione e' modesta (un fattore ~9, non ordini di
grandezza) perche' nel sistema attuale `I2` supera `Lam` solo di ~un ordine anche ai picchi.

### 3.2 Isotropia — **ASSERITA, NON DIMOSTRATA**

`doc/ROADMAP_fork_SU2.md` riga 46 dice: *"ISOTROPIA GIÀ VERIFICATA: «il momento angolare netto NON
dipende dal vuoto stocastico» (riga ~114)"*. **La citazione non regge.** Le righe 113-114 di
`soliton_simulator.py` sono:

```
# APERTO: la PRECESSIONE fra due masse persiste in regime deterministico? Se si', il momento
#         angolare netto NON dipende dal vuoto stocastico (risultato forte).
```

E' marcato **`# APERTO:`** ed e' un **condizionale** (*"Se si', ... risultato forte"*): una
**domanda aperta con la sua conseguenza ipotetica**, non una misura. Il documento l'ha letta come
un risultato acquisito. E la ROADMAP stessa, venti righe piu' sotto (riga 54), la elenca fra i
**sigilli ancora da fare**: *"SIGILLI DISTINTI: scuotimento → isotropia (⟨n⟩ nel tempo)"*.

Quel che si puo' dire **a priori** dal codice: il rumore e' `normal(0,1)` **indipendente per
componente e per nodo**, moltiplicato per uno scalare `amp` che dipende solo da `I2` — quindi la
sua distribuzione **e' isotropa per costruzione**, e la normalizzazione successiva e' una proiezione
radiale che non privilegia direzioni. Ma **isotropia dell'iniezione ≠ isotropia dell'esito**: la
dinamica a valle (torque chirale, `perc_chi`, memoria hebbiana) potrebbe rettificare rumore isotropo
in una direzione preferita. **Solo un run con `⟨n⟩(t)` lo dice.** Mai fatto.

---

## 4. DE-ACCOPPIABILITA' — analisi, non piano

La domanda "e se il gate diventasse il solo `SCUOTIMENTO`?" e' in parte **superata dai fatti**: la
legge **gia' gira** in entrambi gli schemi. Non c'e' nulla da de-accoppiare per "accendere il
vuoto": e' acceso.

Quel che **non** esiste nel ramo asincrono e' il **rumore diretto sul primario** `_psi_spinor`
(l'equivalente di [:2005]). Se un giorno lo si volesse, ecco gli ostacoli reali letti dal codice:

| ostacolo | esito della verifica |
|---|---|
| serve `psi_snapshot` / `psi_t` (esistono solo nel ramo sincrono)? | **No.** [:2003] usa `psi_snapshot` se c'e', **altrimenti `zeros`**; e il ramo asincrono [:1798-1801] usa `self.psi`, chiamando `calcola_psi()` se manca. Nessuna dipendenza bloccante. |
| romperebbe la byte-identita' del ramo OFF? | **No, se resta gated da `SCUOTIMENTO`** — ma attenzione: `SCUOTIMENTO` e' **True di default** (vedi §5), quindi *non* e' un flag OFF: sarebbe un cambio della baseline, non un'aggiunta spenta. Servirebbe un flag NUOVO, OFF. |
| cambierebbe lo stream di `rng`? | **Si.** Due estrazioni complesse in piu' per nodo per passo ([:2005-2006] ne fa 4·n). Qualunque run successivo non sarebbe confrontabile bit-a-bit con quelli precedenti — il che e' normale per un flag nuovo, ma va sigillato (OFF byte-identico). |

---

## 5. LA TRAPPOLA `--regime` — esito NETTO (e un'opportunita')

| riga | contesto | effetto su `SCUOTIMENTO` |
|---|---|---|
| [:117-121] blocco di modulo, `REGIME == "deterministico"` | eseguito **sempre** all'import | `_SCUOTIMENTO_REGIME = **True**` → [:484] `SCUOTIMENTO = True` |
| [:6246] `_applica_regime`, `reg == "deterministico"` | eseguito **solo se** `--regime` e' passato | `SCUOTIMENTO = **False**` |

**Esito netto:**

| riga di comando | `SCUOTIMENTO` |
|---|---|
| *(nessun `--regime`)* — la config certificata dei bracci | **True** ✅ |
| `--regime deterministico` | **False** ❌ |
| `--regime stocastico` | True |
| `--scuotimento` ([:4650]) | forza True |

Cioe': **passare `--regime deterministico` "per essere espliciti" spegne il vuoto in silenzio**,
pur nominando lo stesso regime che e' gia' il default. E' un conflitto reale fra le due righe.

**L'opportunita', pero':** confrontando [:119-121] con [:6246], `--regime deterministico` fissa
`G_PH=3e-3`, `TAU_A=50.0`, `_CALORE_INIT=0.4` — **identici** ai valori di modulo ([:119-121],
[:207], [:267]). **L'unica differenza e' `SCUOTIMENTO: True → False`.**

→ **`--regime deterministico` e', di fatto, un interruttore A/B dello scuotimento a costo ZERO di
codice.** Non serve toccare il `.py` per girare un braccio senza vuoto.
*(Da ri-verificare con un sigillo prima di usarlo come tale: e' un effetto collaterale di un
conflitto, non un'API dichiarata. Ma il codice dice questo.)*

---

## 6. I FATTI DA CHIARIRE (§4 del mandato)

**6.1 — Lo scuotimento dei Bloch E' girato nei bracci certificati.** La mia affermazione contraria
(Passo 0) era sbagliata: girava il ramo [:1803]. Quindi le campagne 5.3a/5.3b/5.3c e i sigilli
dello Strato 0/1 **avevano il vuoto acceso**, nella forma asincrona (mediata dal torque). Va
corretto anche l'inverso: **non** si puo' dire che quei risultati siano "senza vuoto".

**6.2 — L'isotropia non e' mai stata misurata.** Vedi §3.2. E' asserita da un documento che cita un
commento marcato `APERTO`. E' un sigillo che la ROADMAP stessa elenca e che nessuno ha girato.

**6.3 — Per il fork, la domanda vera non e' "il vuoto e' acceso?" ma "scuote abbastanza?".** Il
calcio e' ~1.3 gradi/passo sul Bloch nel vuoto, ma arriva a `_psi_spinor` solo via
`O(amp·|B|·dt)`. Se sia sufficiente a rompere la degenerazione delle direzioni **e' una misura**
(distribuzione degli angoli `chi` fra vicini nel tempo: sparsa = rotta, collassata su 0/π = no),
e quella misura non e' stata fatta.

---

## 7. OPZIONI (nominali — la decisione e' di Luca)

**(a) PASSO 1 cosi' com'e' (nessun codice nuovo).**
Il prerequisito della ROADMAP **e' soddisfatto**: lo scuotimento gira. Si registra che agisce in
forma **mediata** (via torque, `O(amp·|B|·dt)`) e non diretta. Zero rischio, zero codice.
*Costo:* se la degenerazione non si rompe, non si sapra' se e' colpa dell'ampiezza o della fisica —
a meno di aggiungere al run la misura della distribuzione di `chi` (diagnostico pure-read), che
risponde proprio a questo.

**(b) RUMORE DIRETTO SUL PRIMARIO nel ramo asincrono** (flag nuovo, OFF, col suo sigillo:
byte-identita' OFF, isotropia `⟨n⟩`, stabilita').
Nessun ostacolo tecnico bloccante (§4). *Costo:* un pezzo di lavoro prima del run, e cambia lo
stream `rng` quindi rompe la confrontabilita' bit-a-bit coi run precedenti (normale, ma da sigillare).
*Nota:* **non** e' "de-accoppiare dall'integratore" — quello non serve piu'; e' **aggiungere** il
canale diretto dove oggi c'e' solo quello mediato.

**(c) DUE BRACCI `--sync` OFF/ON — NON E' PULITO.**
`SYNC_UPDATE` ha **13 call-site** oltre alla definizione ([:1785], [:1805], [:1873], [:1999],
[:2022], [:2517], [:2539], [:2651], [:2747], [:2802], [:4774]) e l'help lo dichiara:
*"Jacobi invece di Gauss-Seidel"*. Accenderlo cambia **l'integratore** E **quale implementazione
dello scuotimento gira**: due meccanismi in un interruttore → **viola il §1** di CLAUDE.md, e
qualunque differenza fra i bracci sarebbe inattribuibile.

**(c-bis) DUE BRACCI SULLO SCUOTIMENTO, a costo zero** — l'alternativa pulita a (c):
default (vuoto ON) contro `--regime deterministico` (vuoto OFF), che per §5 differiscono **solo**
per `SCUOTIMENTO`. Una variabile, un interruttore, nessun codice nuovo. Da confermare con un
sigillo che quei due comandi differiscano davvero solo per quel flag.

---

## 8. COSA QUESTA INDAGINE NON DICE

Non dice se lo scuotimento **basti** a rompere la degenerazione dei Bloch (§6.3: e' una misura da
fare). Non dice se il sistema sia **isotropo** (§3.2: mai misurato). Non dice quale opzione
scegliere. E non e' un run: tutti i numeri del §3 vengono da **uno stato a 150 passi, un solo
seme** — servono a dare l'ordine di grandezza di `amp`, non a concludere alcunche' sulla fisica
(§2.7: niente conclusioni sotto ~2000 passi, mai su un seme solo).
