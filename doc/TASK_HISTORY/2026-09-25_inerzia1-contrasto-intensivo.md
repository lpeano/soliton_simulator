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
