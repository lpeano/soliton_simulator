# `INERZIA-1` — CURA (C) **LOCALE**: il contrasto diventa «per vicino» (decisione di Luca)

*(committato **PRIMA** del codice, par.5-septies. La decisione, la località e i criteri sono di
Luca; qui c'è ciò che ho verificato prima di scrivere, e cosa mi fermerebbe.)*

## ① RAGIONAMENTO PRELIMINARE — *cosa è già misurato, e cosa la cura deve togliere*

**IL DIFETTO, misurato oggi in configurazione del driver** *(`CONFIG-1/a`, 2 semi × 2 versi del
taglio, 20 bersagli per seme)*: `inerzia = _contrasto · T2` con `_contrasto = rho_s/peq_nodo`, e
le pendenze su `log k` dicono

```
COPPIA       -0.19 … -0.30      INTENSIVA  (non cresce col numero di vicini)
_contrasto   +1.06 … +2.47      ESTENSIVO
T2           -0.15 … +0.44      fa cio' che la geometria impone
```

> ### **Due fattori della stessa equazione scalano in verso OPPOSTO nel numero di vicini.**
> Conseguenza misurata: da `k = 77` a `k = 2` l'inerzia crolla `×2e-4 … ×4.6e-3`, il rapporto
> sale `×427 … ×1.5e4`, e **`|omega|` arriva a `×176`** — il difetto **arriva alla dinamica**.

**LA CAUSA È DI STRUTTURA, non numerica:** `rho_s` è una **SOMMA pesata sui vicini**
(`psi = _mat(w) @ …`), `_peq_nodo` è **esplicitamente una MEDIA** (`_sp/_cn`). Un rapporto
somma/media **scala col grado per costruzione**.

**LA CURA DI LUCA, e perché è (C) *LOCALE*:** dentro `_contrasto` — **e solo lì** — `rho_s` si
normalizza **per vicino**, col **medesimo `_cn`** che `_peq_nodo` usa già come denominatore.
**`rho_s` non cambia altrove: la cura tocca l'INERZIA, non IL CAMPO.**
**`STANDARD 10`: nessuna legge nuova** — si **toglie** l'incoerenza fra numeratore e denominatore,
e **nessuna grandezza nuova** entra, perché `_cn` c'è già tre righe sopra.

## ② LA VERIFICA, FATTA PRIMA — `csv/_letture_rho_s.py`, per AST **e stringhe**

```
occorrenze totali                      16
  letture                              14        scritture   2
  di cui trovate come STRINGA           4        <- la famiglia che l'audit di `eta` mancava
letture DENTRO `_passo_spinoriale`      7
letture FUORI                           7
```

**LE 7 LETTURE «FUORI», una per una** — sono le leggi che la cura **non deve toccare**:

| dove | come legge |
|---|---|
| `:246` tabella degli invarianti | **STRINGA** `'rho_spin': ('nonneg', …)` |
| `lambda_nodi:2921` | `self._rho_sorgente()` |
| `_rho_sorgente:3859` | `getattr(self, "rho_spin")` — **la definizione stessa** |
| `mitosi:5992` | `self._rho_sorgente()` — la soglia di densità della mitosi |
| `mitosi:6173` | `self._rho_sorgente()` — la densità della coppia Schwinger |
| `batch_condensazione:10223`, `:10281` | **STRINGA**, dentro i dizionari di snapshot |

> ### ✅ **LA CURA È LOCALE PER COSTRUZIONE, e si vede da questa tabella:** tutte e sette
> ### passano da **`rho_spin`** o dal **valore restituito da `_rho_sorgente()`**, e la cura non
> ### tocca né l'uno né l'altro — normalizza **la variabile locale che entra in `_contrasto`**.
> **E la prova non è questo ragionamento: è la byte-identità a flag spento** (`A1` del sigillo).

**⚠ E `:246` È IL CASO CHE MI HA GIÀ MORSO STAMATTINA:** è la **tabella degli invarianti**, che
legge le grandezze **come stringhe**. Se avessi normalizzato `rho_spin` **invece** della variabile
locale, l'invariante avrebbe controllato il valore normalizzato — e l'audit di `eta`, che le
stringhe non le cercava, **non me l'avrebbe detto**.

## ③ PROGETTAZIONE — cosa cambio e cosa decide ciascun passo

| passo | cosa | **cosa decide** |
|---|---|---|
| **1** | flag `CONTRASTO_INTENSIVO`, **OFF di default**, `--contrasto-intensivo`, assegnato in `_applica_flag` **con `global`** | che il flag **sia vivo dal CLI** — la trappola che ha reso morti `--semina-matura` e `--mitosi-2lam` |
| **2** | in `_contrasto`: `_rho_s / max(_cn, 1)` invece di `_rho_s`, **stesso `_cn` di `_peq_nodo`** | che la cura sia **locale** e **senza grandezze nuove** |
| **3** | contatori `A8` del sito: quante volte gira, e il caso `_cn` assente | che il ramo non sia un **fallback non misurato** (`P5`) |
| **4** | sigillo nuovo, **dal CLI** (`P3`), `P5`, 2 semi, 20 bersagli, **due versi** | i criteri di Luca |

**I CRITERI, COME LUCA LI HA DATI** *(si scrivono qui, prima dei numeri)*:
1. **pendenze su `log k` di COPPIA e INERZIA uguali entro l'errore fra semi** *(oggi `-0.2`
   contro `+1.5/+2.4`)*;
2. **`|omega|` a `k = 2` dello stesso ordine di `k = 77`** *(oggi `×150-176`)*;
3. **flag spento byte-identico al codice PRECEDENTE** — **non `HEAD`** (`P8`:
   `sim_prima_del_flag`);
4. **caso che DEVE fallire: il braccio spento**, generato **togliendo il flag dall'argv**;
5. **pavimento `1e-6`: quante volte morde con la cura** *(oggi `0/20`)*;
6. **scala dell'inerzia su TUTTI i nodi prima/dopo** — mediana, `p5`, `p95`.

**COSA MI FAREBBE FERMARE:**
- se `A1` (flag spento byte-identico) **cade** → **STOP**: la cura **non è locale**, e il
  referto lo dice invece di essere aggiustato;
- se il criterio 1 passa ma il **2** no → la coerenza delle pendenze **non basta**, e va detto:
  significa che l'incoerenza non era l'unica causa di `|omega|`;
- se il pavimento **comincia a mordere** → la cura abbassa l'inerzia in assoluto, non solo la sua
  pendenza, e **`A11` chiede di guardare l'errore che il pavimento nasconde**.

## ④ TODO DEL NEXT STEP

- [ ] la cura (1 flag, 1 riga di legge, i contatori) + il sigillo coi sei criteri, **dal CLI**
- [ ] referto + relazione + voce di coda, **nello stesso commit** del riscontro
- [ ] **`STANDARD 10` verificato, non asserito:** contare le leggi prima/dopo nel sito
- [ ] poi **`CONFIG-1` b) chi comprime `d0`** (ordine di Luca)


---

# ② **LA VARIANTE PESATA** — criteri fissati PRIMA di misurare *(decisione di Luca, 2026-09-25)*

> **`rho_s` si normalizza sulla SOMMA DEI PESI del nodo** *(quella di `_mat(w)`)*, **non sul
> conteggio.** Stesso flag. **Nessun numero nuovo.**
> *(La versione per conteggio **non è nel driver** e **resta nel registro come tentativo
> misurato**: toglieva esattamente `−1.0000` di pendenza e non bastava.)*

**DOVE VIVE, e perché non serve niente di nuovo:** `w` è **già un parametro** di
`_passo_spinoriale` (`def _passo_spinoriale(self, i, j, w, dt_n, …)`), ed è **lo stesso `w`** che
`calcola_psi` passa a `_mat(w)` per costruire `psi_spin`. La somma per nodo è
`np.bincount(i, w) + np.bincount(j, w)`, cioè **la somma di riga di `_mat(w)`** — la grandezza che
il campo del nodo usa già.

## ⚠ **UN'OSSERVAZIONE DI STRUTTURA CHE INDEBOLISCE LA MIA STESSA PREVISIONE, e la scrivo PRIMA**

Leggendo `calcola_psi`:

```
psi_spin = (_mat(w) @ (amp * _psi_spinor)) / (1 + GAMMA*|…|)
rho_spin = Re( conj(psi_spin) . psi_spin )          <- IL MODULO QUADRO
```

> ### **`rho_s` non è una somma pesata: è il QUADRATO di una somma pesata.**
> Se `psi_spin ∼ W` *(la somma dei pesi)*, allora **`rho_s ∼ W²`**.

**Conseguenza, e va detta ORA perché dopo sembrerebbe una scusa:** dividere per `W` **una volta**
toglie **una** potenza di `W` — esattamente come dividere per il conteggio toglieva una potenza di
`k`. **Se la dipendenza è quadratica, la variante pesata potrebbe NON portare il residuo sotto
`0.7`**, e la forma coerente sarebbe **`rho_s / W²`**.

**NON la anticipo e non la implemento:** Luca ha deciso `W`, e **la misura dirà se basta**. Ma il
mio `C1''` — *«la differenza scende sotto `0.7` nel taglio corti»* — **ha ora una ragione
strutturale per fallire**, e se fallisce **non sarà una sorpresa: sarà questa**.
*(La differenza fra le due letture è misurabile: se `rho_s ∼ W²`, la variante `W` deve togliere
**una** potenza e lasciare un residuo ≈ a quello di oggi meno uno; se `rho_s ∼ W`, deve azzerarlo.
**Il numero distingue le due ipotesi**, ed è per questo che la misura vale anche se `C1''` cade.)*

## I CRITERI, **come Luca li ha fissati**, prima dei numeri

| | criterio | nota |
|---|---|---|
| **`C1'`** | pendenza su `log k` del **CONTRASTO** uguale a quella della **COPPIA** entro lo spread fra semi, **in tutti e 4 i bracci** | **`T2` ESCLUSO**, e il perché è dichiarato qui sotto |
| **`C1''`** | **la mia previsione falsificabile**: differenza di pendenza **inerzia−coppia < 0.7** nel taglio **«corti»** | **se non passa, la diagnosi «residuo dai pesi» è sbagliata e LO SI SCRIVE** |
| **`C2`** | `|omega|(k=2)/|omega|(k=77)` **< 3** in tutti i bracci | **il `3` è una SCELTA** per *«stesso ordine»*, **dichiarata** |
| **`C3`** | flag spento **byte-identico al padre del commit del flag** (`P8`) | |
| **`C4`** | **CORRETTO da Luca**: braccio spento generato **togliendo l'opzione**, e su di esso **`C1'` NON passa**. **Nessuna soglia propria.** | vedi sotto |
| **`C5`** | il pavimento `1e-6` | quante volte morde |
| **`C6`** | scala dell'inerzia su **tutti** i nodi | mediana, `p5`, `p95` |

### **PERCHÉ `T2` È ESCLUSO DA `C1'`** *(dichiarazione richiesta da Luca)*

`T2 = (d_nodo/cs_nodo)²` **dipende da `k` in questa misura per la GEOMETRIA DEL TAGLIO, non per
estensività**: togliere i **lunghi** accorcia `d_nodo` *(pendenza `+0.44`)*, togliere i **corti**
lo allunga *(`−0.15`)*. **È l'ascissa che cambia la geometria, non la legge che scala col grado.**
Quindi mettere `T2` dentro il criterio misurerebbe **il taglio**, non l'incoerenza.
**`C1'` guarda `_contrasto` contro `COPPIA`**, che sono i due termini che *devono* avere la stessa
estensività. *(E `C1''` resta sull'**inerzia** intera, perché è lì che il difetto arriva a `omega`:
i due criteri guardano due cose diverse, ed è voluto.)*

### **`C4` È STATO CORRETTO, E NON È UN ALLENTAMENTO** *(decisione di Luca)*

```
VECCHIA FORMA (mia, 2026-09-25, sigillo 3/6):
    il braccio spento e' generato togliendo l'opzione
    E  min(|Δpend| OFF) > max(|Δpend| ON) * 3.0        <- UNA SOGLIA PROPRIA

FORMA CORRETTA (Luca):
    il braccio spento e' generato togliendo l'opzione
    E  su di esso `C1'` NON passa                      <- NESSUNA soglia propria
```

**PERCHÉ la vecchia era sbagliata:** quel `* 3.0` **duplicava `C1`** con una soglia più stretta, e
infatti `C4` è fallito **per la stessa ragione di `C1`** — `max(ON) = 1.64` contro
`min(OFF) = 1.71`, rapporto `1.04`. **Un criterio che fallisce per il fallimento di un altro non
sta misurando niente di suo: sta contando due volte lo stesso fatto.**
**E la correzione la fa Luca, non io, e non dopo aver visto i numeri di una misura nuova:** la
vecchia forma è scritta qui sopra perché **un criterio corretto senza che si veda quello di prima
è un criterio senza provenienza.**


---

# ③ ❗ **ESTENSIVO O RITARDATO?** — l'ipotesi di Luca, e i criteri **prima** di misurare

> **`_contrasto = rho_s / _peq_nodo`, e `peq` è una MEMORIA che rilassa verso `rho`.**
> **All'equilibrio i due seguono lo STESSO vicinato, e il loro rapporto potrebbe essere GIÀ
> intensivo.** Allora il `+1.06 … +2.47` che ho misurato non sarebbe estensività: sarebbe **il
> ritardo di `peq` dietro a `rho`**.

**E DUE FATTI LA SOSTENGONO — entrambi verificati dal codice, non supposti:**

1. **nella prova di limite gli archi si tagliano DI COLPO.** `rho_s` si ricostruisce **nello stesso
   passo** *(`psi_spin = _mat(w) @ …`)*; `peq` no: rilassa con `exp(-dt_e/tau_bg)`.
   **Il mio taglio è un GRADINO, e ho misurato la risposta un passo dopo.**
2. **i figli della mitosi EREDITANO `peq` dall'arco del genitore — ESATTAMENTE**, e la riga è
   `:6226`:
   ```
   self.peq = np.concatenate([self.peq[keep], self.peq[sel], self.peq[sel]])
   ```
   **Il `peq` di un arco nato ha il valore di un arco di un nodo da ~77 vicini; il suo `rho` viene
   da 2.** *(Ed è la stessa famiglia di `C7`/`C11`: un'eredità che copia uno stato **di un altro
   vicinato**.)*

## ⚠ **`TAU_BG = 5.0` NON È IL TEMPO VERO, e questo cambia come si scrive il criterio**

Dal codice: con **`TAU_LOCALI = True`** *(default)* il rilassamento usa
**`tau_bg_loc = max(1/max(r_arco, 1e-3), 1e-3)`** — **un tempo LOCALE**, non la costante `5.0`.
`TAU_BG` entra solo nel ramo `TAU_LOCALI` spento (`:5522`).

> ### **Quindi `N` non si SCEGLIE: si DERIVA dalla misura.** Il numero di passi per un tempo di
> ### rilassamento è **`tau_bg_loc / dt_e`**, e **va letto dalla rete che gira**, per arco.
> **Il sigillo stampa la mediana di `tau_bg_loc/dt_e` e usa `N = 3 ×` quel numero**, dichiarandolo.
> *(Scegliere `N = 300` perché «sembra abbastanza» sarebbe un numero tarato — par.3 — e in questo
> repo un `tau` stimato invece che letto ha già prodotto la voce «un'ipotesi che rigenera la
> propria scusa».)*

## I CRITERI DI `(a)` e `(b)`, scritti ORA

| | criterio | **cosa decide** |
|---|---|---|
| **`R1`** | *(a)* dopo `N = 3 tau_bg` dal taglio, **a flag SPENTO**, la pendenza su `log k` di **`_contrasto`** torna entro lo spread fra semi da quella della **COPPIA** | **se SÌ: era un RITARDO**, e la normalizzazione è la cura sbagliata |
| **`R2`** | *(a)* il **residuo** `\|pend(contrasto) − pend(coppia)\|` **cala monotonamente** fra `1`, `N/3`, `N` passi dal taglio | distingue un **transitorio** da un **offset costante**: un ritardo DEVE decadere |
| **`R3`** | *(b)* per i figli della mitosi, `rho`, `peq` e `_contrasto` **dalla nascita**: il contrasto **rientra** verso il valore dei nodi maturi entro `N` passi | **se SÌ: l'eredità di `peq` è il difetto**, e la cura è **`peq` alla nascita** |
| **`R4`** | *(b)* **il nullo**: gli stessi tre valori sui nodi **NON nati** nello stesso intervallo | senza, un «rientro» potrebbe essere solo la deriva di tutto il sistema |

**COSA MI FAREBBE CAMBIARE IDEA, e lo scrivo perché è la mia diagnosi a essere in gioco:**
se `R1` e `R3` passano, **la mia lettura «il residuo viene dai pesi» è sbagliata** — non
incompleta: **sbagliata**, perché avrei attribuito a una legge un artefatto del mio protocollo di
misura *(un gradino su una memoria)*. **E lo scriverò così.**

**COSA RESTEREBBE VERO ANCHE ALLORA:** che `rho_s` **è** una somma pesata e `_peq_nodo` **è** una
media — l'asimmetria di struttura è nel codice. Ma **un'asimmetria di struttura non è un difetto
se le due grandezze, all'equilibrio, vivono sullo stesso vicinato**: sarebbe una scrittura
ridondante, non una legge sbagliata. **La differenza fra le due letture la fa `R1`, non il
ragionamento.**

**⚠ E UNA COSA CHE NON SI PUÒ CHIUDERE COSÌ:** `|omega|` a `k = 2` faceva **×176**. Se è un
transitorio di `peq`, **quel transitorio è comunque ciò che il sistema vive ogni volta che nasce un
nodo** — e i nodi nascono continuamente. **«È un ritardo» non significa «è innocuo»**: significa
che la cura va messa **alla nascita**, non nella legge dell'inerzia.


---

# ④ ❗ **`R3 bis` — UN'INCOERENZA DI ESPONENTI DELLA RAMPA** *(lettura di Luca, verificata dal codice)*

> **Per un figlio della mitosi:** la **COPPIA** è moltiplicata per `ramp` **una volta**, mentre
> **`rho_s`** viene da archi pesati `ramp_i·ramp_j` **ed è un modulo QUADRO** → **`~ramp²`**; con
> **`peq` ereditato dal genitore** *(che non scala con `ramp`)*, **`_contrasto ~ ramp²`** e quindi
> **`omega ~ coppia/inerzia ~ 1/ramp`**.
> **PREVISIONE: sui figli, `|omega| · ramp` ≈ COSTANTE durante la maturazione**, e `|omega|` che
> **cala** mentre `ramp → 1`.

**NESSUNA MISURA NUOVA: si verifica coi dati di `R3`.** *(Conseguenza operativa: `R3` deve
raccogliere **anche `ramp` e `|omega|`** per ciascun figlio, oltre a `rho`, `peq` e `_contrasto`.
Lo scrivo qui perché `R3` non è ancora implementato, e senza queste due colonne `R3 bis` non
sarebbe verificabile.)*

## LA VERIFICA DAL CODICE — **entrambi gli esponenti, riga per riga**

| dove | riga | cosa dice |
|---|---|---|
| **il peso d'arco** | `:3850` | `base = exp(-d/lam) * ramp[self.i] * ramp[self.j]` → **il peso porta `ramp_i·ramp_j`** |
| **`rho_s`** | `calcola_psi` | `psi_spin = _mat(w) @ (amp*_psp)`, poi `rho_spin = Re(conj(psi_spin)·psi_spin)` → **MODULO QUADRO** di una somma pesata → **`~ramp²`** |
| **la coppia, 1° termine** | `:3241-3251` | `B` costruito con `w[mask]` **e poi `B = B / max(deg, 1e-9)`** → porta `ramp_i` **una volta** |
| **la coppia, 2° termine** | `:3526`, `:3554` | `_tq = cross(_nb_grav(), nb)` *(una DIREZIONE, normalizzata: senza `ramp`)*, poi `_tq = _tq * ramp[:n]` → **`ramp` una volta, esplicito** |
| **`peq` del figlio** | `:6226` | `peq[sel]` ereditato **esattamente**: **non scala con `ramp`** |

> ### ✅ **LA DERIVAZIONE REGGE: coppia `~ramp¹`, `_contrasto ~ramp²`, quindi `omega ~ 1/ramp`.**
> Ed è **pulita** perché **tutti e due** i termini della coppia portano `ramp` **una volta sola**:
> il primo attraverso i pesi dentro `B`, il secondo scritto a mano a `:3554`.

## 🎯 **E UN DETTAGLIO CHE RAFFORZA TUTTO IL QUADRO: `B = B / max(deg, 1e-9)`**

**`B` è già una MEDIA sui vicini** *(diviso il grado)*, e `rho_s` **no**.

> **Ecco perché la coppia ha misurato `-0.19 … -0.30`, cioè INTENSIVA:** non è un caso né una
> fortuna, **è scritto nel codice a `:3251`**. **Il campo del nodo (`B`) è normalizzato sul
> vicinato; il campo emesso (`rho_s`) non lo è.** L'asimmetria che ho chiamato «somma contro
> media» ha quindi **una controprova interna**: nello stesso file, **lo stesso tipo di grandezza è
> normalizzato in un posto e non nell'altro.**

## SE `R3 bis` REGGE, COSA CAMBIA — e non è la stessa cura

```
estensivita'        -> si normalizza rho_s (tocca TUTTI i nodi, ~1/77)
ritardo di peq      -> si cura peq ALLA NASCITA dei nuovi archi
esponenti di ramp   -> si cura L'ESPONENTE: la coppia e l'inerzia devono portare
                       LA STESSA potenza di `ramp`, e il difetto e' sui SOLI nodi
                       che stanno maturando -- cioe' i nati in dinamica
```

> **Le tre letture non sono varianti della stessa cura: sono tre difetti diversi**, e **due di
> esse ritirerebbero la variante pesata** *(che tocca tutti i nodi, per sempre)*.
> **`R1`, `R3` e `R3 bis` si escludono a vicenda nei numeri**, ed è il motivo per cui vanno
> misurati **insieme** e non uno alla volta.

**COSA DISTINGUE `R3 bis` DA `R3`, perché sui figli agiscono entrambi:** `R3` dice *«il contrasto
rientra quando `peq` si rilassa»* — un rientro **guidato dal tempo di `peq`**; `R3 bis` dice
*«`|omega|·ramp` è costante»* — un rientro **guidato da `ramp`**. **Hanno due scale di tempo
diverse** *(`tau_bg` contro il tempo-luce della rampa)*, quindi **il dato li separa**:
se il prodotto `|omega|·ramp` è piatto **mentre** `peq` è ancora lontano dall'equilibrio, è
`R3 bis`; se `|omega|` rientra **solo quando `peq` arriva**, è `R3`. **Se sono piatti entrambi,
sono due difetti sovrapposti** — e va scritto così, non scelto.
