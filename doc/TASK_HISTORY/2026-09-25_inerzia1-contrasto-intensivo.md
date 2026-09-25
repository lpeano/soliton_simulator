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
