# IL BILANCIO DEI TASSI — l'ordine di spin **nasce** e viene **distrutto**

> **Scritto per Claude web.** Branch `fork-su2`, 2026-09-15. Blob sul disco **`f5887254`**
> (gate in `CLAUDE.md` §0 su `c0803713`: disallineamento voluto, ramo turbo diagnostico).
> **Nessuna modifica alla fisica.** Stato: **FASE A chiusa.** FASE B e C **non ancora fatte**.

---

## 0. LA RIFORMULAZIONE — perché questo lavoro non è «un settimo lato»

Sei misure convergenti dicono che lo spin è *frozen-o-noise*. Ma dal codice emerge un fatto che
**cambia la domanda**: alla mitosi il figlio eredita il padre per **copia esatta**. Quindi

> **ogni nascita crea una coppia perfettamente correlata (chi = 0).**

E la misura dice **chi = 90° ovunque**. Segue che **l'ordine non manca: nasce di continuo e viene
distrutto.** Il problema non è «serve un meccanismo ordinante» — sarebbe la strada che porta a
*imporre* un Kuramoto, già refutata — ma **un bilancio fra due tassi già presenti nel sistema**:

| | chi lo produce |
|---|---|
| **creazione** di correlazione | la mitosi (eredità esatta) |
| **distruzione** | rumore del vuoto + precessione mutua (misurata come **attivamente disordinante**: 60° → 104° a rumore spento) |

Questo documento **misura i due tassi**. Non aggiunge meccanismi.

---

## 1. FASE A — IL FATTO, VERIFICATO

### 1.1 L'eredità è una copia esatta, senza perturbazione

`_eredita_spinore_figli` ([`soliton_simulator.py:1133-1170`](../soliton_simulator.py#L1133-L1170)),
chiamata da `mitosi` a [`:3125`](../soliton_simulator.py#L3125):

| campo ereditato | riga | come |
|---|---|---|
| `_nb` (Bloch) | `:1147` | `vstack([_nb, _nb[src]])` — **esatta** |
| `_nb_prec` | `:1149` | esatta |
| `_nb_ret` (ritardato, Strato 1) | `:1155` | esatta |
| `omega_s` (memoria hebbiana) | `:1157` | esatta |
| `_psi_spinor` (primario complesso) | `:1159-1161` | `.copy()`, con `−` per gli antinodi |
| `_spinor_lift` | `:1164` | idem |
| `_psi_prec` | `:1169` | esatta |

**Nessun jitter, nessuna perturbazione, nessun gating** oltre al flag
(`SPINORE_CORRETTO or CAMPO_SPINORIALE`, entrambi attivi nei run del fork).

> **Conseguenza non ovvia, da tenere:** l'antinodo Schwinger ([`:3242`](../soliton_simulator.py#L3242),
> `segno=-1`) eredita `−ψ`. Ma `nb = ψ†σψ` è **invariante per fase globale**, e `−1 = e^{iπ}` lo è:
> `conj(−a)(−b) = conj(a)b`. **Anche l'antinodo nasce con chi = 0 in Bloch.** «Antichirale» riguarda
> il segno di doppia copertura, **non** la direzione. Il tasso di creazione di coppie correlate
> include quindi *anche* le Schwinger, non solo le mitosi.

### 1.2 Il figlio nasce adiacente — nello spazio **e** nella topologia

- **spazio:** [`:3094`](../soliton_simulator.py#L3094) `pos_figlio = 0.5*(pos[a] + pos[b])`, il punto
  medio dell'arco. Il kernel `e^{−d/λ}` li accoppia **per costruzione**, non per caso.
- **topologia:** [`:3172-3173`](../soliton_simulator.py#L3172-L3173) l'arco del padre viene
  **rimosso** e sostituito da `(a,m)` e `(m,b)`. Il figlio nasce con **esattamente due archi**,
  verso entrambi i genitori.

### 1.3 La parentela **non è registrata**, ma è **ricostruibile in volo**

Nessun array di lignaggio esiste. Gli unici `parent` del file
([`:949-982`](../soliton_simulator.py#L949-L982)) sono lo spanning-tree di
`_base_cicli_topologici`: **topologia di grafo, non genealogia**. `conc_nodi` eredita l'**ID di
massa**, non l'indice del padre.

**Ma un osservatore per passo la ricostruisce**, e il padre `a` — quello da cui si eredita — è
distinguibile da `b`: nell'arco `(a,m)` il padre sta nel lato `i`, il figlio nel lato `j`.
Verificato, non dedotto (`csv/_test_fork/_parentela_bloch.py`):

```
nuovi nodi osservati             : 7
  con ESATTAMENTE 2 genitori     : 7  (100.0%)
  con il padre `a` identificabile: 7  (100.0%)
```

> **Quindi la FASE B può fare la misura VERA** (coppie padre-figlio seguite nel tempo), **non un
> proxy.** Era questo a essere in dubbio.

---

## 2. IL FATTO È CONFERMATO — ma il numero accanto è quello che conta

```
chi PADRE-FIGLIO alla nascita (gradi), n=7:
   media 0.0000  mediana 0.0000  min 0.0000  max 0.0000
   VALORE-NULL (direzioni casuali): 90.000 +- 39.171
```

Correlazione **perfetta ed esatta**, come prevede la copia. Ma nello **stesso passo**:

```
spostamento del PADRE nel passo della nascita (gradi), n=7:
   media 85.6452  mediana 95.8363  min 36.6732  max 108.7353
```

> **Il Bloch di un nodo si sposta di ~90° in UN passo: decorrela da sé stesso in un tick.**

Cioè si colloca già sul valore-null della decorrelazione completa. Se regge sulla statistica,
`tau_dec ≲ 1 passo` e il verdetto della FASE B è **già indicato**: `tau_dec << tau_mit`, sistema
**dominato dalla distruzione**, coerente con `chi = 90` ovunque.

**Ma sette campioni non sono una misura,** ed è esattamente il genere di numero a cui si crede
troppo presto. La FASE B lo rifà sulla scena reale con centinaia di nascite. Finché non è rifatto,
questo è un **indizio**, non un risultato.

---

## 3. IL CANALE DEL RUMORE NON È QUELLO CHE SI PRESUME (pesa sulla FASE C)

Sotto `--spinore-corretto` con `SYNC_UPDATE = False` — cioè **la configurazione di tutti i run del
fork**:

- il rumore a [`:1847`](../soliton_simulator.py#L1847) colpisce `self._nb`…
- …ma il `_nb` **committato** è **derivato** da `_psi_spinor`
  ([`:2066-2069`](../soliton_simulator.py#L2066-L2069), [`:2088`](../soliton_simulator.py#L2088));
- il rumore additivo **diretto** sul Bloch ([`:2060`](../soliton_simulator.py#L2060),
  [`:2085`](../soliton_simulator.py#L2085)) è gated su `SYNC_UPDATE` ed è **spento**.

> Il rumore entra **solo** via `correzione = cross(B, nb)` → `omega_new` → rotazione.
> **È rumore di COPPIA, non di posizione sulla sfera.**

Non è un dettaglio di implementazione: cambia la legge attesa di decorrelazione (diffusione
sull'**angolo di rotazione**, non sulla posizione) e tocca direttamente l'ipotesi della FASE C,
perché `omega_s` **ha già memoria** (`TAU_A`, e `TAU_A_LOCALE` la rende locale). Un canale a cui
«dare memoria» ce l'ha già, e resta comunque disordinato: è un vincolo forte sulla classifica.

---

## 4. LA PRECISAZIONE DA NON PERDERE — la memoria **non ordina**

Un rilassamento `dx/dt = (x_eq − x)/tau` **rallenta** i cambiamenti, non li **orienta**.
La prova è già nel repo: lo **Strato 1 è memoria pura**, ed è passato 23/23 **senza ordinare i
Bloch**. La memoria agisce **sui tassi** — filtro passa-basso sul rumore veloce, vita più lunga
della correlazione ereditata — quindi la domanda giusta per ogni canale è **un confronto di tempi**,
non «aiuta o no».

---

## 5. STATO E PROSSIMO PASSO

| fase | stato |
|---|---|
| **A** — verifica del fatto, adiacenza, parentela ricostruibile | **chiusa** |
| **B** — i due tassi (`tau_dec` vs `tau_mit`) e il verdetto del bilancio | da fare |
| **C** — classifica dei canali col confronto dei tempi | da fare |

**Lettura del verdetto B3, scritta PRIMA di misurare** (così non si adatta al risultato):

| esito | lettura |
|---|---|
| `tau_dec << tau_mit` | l'ordine muore prima che ne nasca altro: dominio della distruzione. **Coerente con chi = 90.** |
| `tau_dec ~ tau_mit` | bilancio in bilico: un piccolo spostamento dei tassi sposterebbe il sistema. **Il caso interessante.** |
| `tau_dec >> tau_mit` | l'ordine dovrebbe accumularsi, e allora `chi = 90` sarebbe **inspiegato**. **Un reperto.** |

**Configurazione proposta per la FASE B:** scena reale `--nmasse 3 --sep 8 --seed 1`, campionamento
a ogni passo per ~300-500 passi dopo il riscaldamento, per avere **centinaia** di nascite invece di
sette. Da confermare, insieme all'eventuale secondo seme.

---

## 6. COSA NON È STATO TOCCATO

`soliton_simulator.py` **non è stato modificato**: `git status` lo dà pulito e il blob sul disco è
`f5887254`, lo stesso di prima di questo lavoro. Nessun flag nuovo, nessuna memoria aggiunta a
nulla, nessuna costante di tempo nuova. `csv/_test_fork/_parentela_bloch.py` legge **solo array di
stato** (`i`, `j`, `_nb`): non chiama `calcola_psi()` né `ritmo()`, che mutano le cache di
continuità lette dalla dinamica, e non consuma `net.rng`.
