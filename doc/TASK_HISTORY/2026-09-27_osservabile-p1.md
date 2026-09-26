# `OSSERVABILE-P1` — la distanza fra due masse **lungo il grafo**, pesata con `d`

> **Secondo `SI` dello smistamento** *(`doc/REVISIONE_SI_2026-09-26.md`, sezione `OSSERVABILE-P1`)*.
> **Mandato di Luca, 2026-09-27.** La `PROVA 1` chiede *«due masse si avvicinano?»*, e la distanza
> del sistema **sta sugli archi** (`A13`), **non su `pos`**.
>
> **COMMITTATO PRIMA DEL CODICE** (`CLAUDE.md` par.8).

---

## 1. RAGIONAMENTO PRELIMINARE

### 1.1 ⚠ LA RICOGNIZIONE CHE LUCA HA CHIESTO: **i tre script non esistono**

Il mandato dice *«dimmi se i tre script di analisi che gia' calcolano cammini minimi si possono
riusare»*. **Non ce n'e' nemmeno uno: in tutto il repo non esiste UN cammino minimo.**

**Ricerca sull'INTERO albero** (`STANDARD 9`, e il comando e' questo, senza intervalli di righe):

```
grep -rl <nome> --include=*.py .        (esclusi `/_tmp/`, `_old_sim_*`, `*._sim.py`)
  dijkstra .......... nessun file        floyd_warshall .... nessun file
  shortest_path ..... nessun file        bellman_ford ...... nessun file
  breadth_first ..... nessun file        johnson ........... nessun file
grep -c 'dijkstra|shortest_path' soliton_simulator.py  ->  0
```

**Che cosa c'e' DAVVERO, ed e' un'altra cosa:** **quattro** script costruiscono un grafo sparso e
ne contano le **COMPONENTI CONNESSE**:

| script | che cosa fa col grafo | i pesi |
|---|---|---|
| `csv/_test_fork/_letture_ab.py` | il presidio di `Z65`: numero di componenti, taglia della piu' grande, nodi isolati | **`np.ones`** |
| `csv/_test_fork/_topologia.py` | componenti connesse su un run | **`np.ones`** *(`float32`)* |
| `csv/_test_fork/_topologia_blocchi.py` | le stesse, a blocchi | **`np.ones`** |
| `csv/_test_fork/_pilota_sep.py` | componenti al variare di `--sep` | **`np.ones`** |

> ### **RIUSABILE E' L'IDIOMA, NON LA MISURA.**
> `coo_matrix((pesi, (i, j)), shape=(n, n)).tocsr()` da `net.i` / `net.j` **si riusa** — ed e' lo
> stesso in tutti e quattro, quindi e' la forma di casa. **Ma i loro pesi sono `ones`, cioe' il
> CONTEGGIO DEI SALTI**, e la `PROVA 1` chiede la **lunghezza pesata con `d`**: sono due grandezze
> diverse sullo stesso grafo. **Riusare il loro codice cambiando `ones` in `d` sarebbe corretto e
> minimo**, e non c'e' niente da riusare oltre a quello.
> **`connected_components` mi serve comunque**, per un motivo che non e' cosmetico: **se due masse
> stanno in componenti diverse la distanza e' `inf`**, e uno strumento che restituisse `inf` senza
> dirlo sarebbe illeggibile.

*(`csv/_seal_fork/_passo_zero_scena_ii.py` legge `net.d` ma **non e' un cammino**: somma pesi e
conta. `csv/_test_fork/_chi_comprime_d0.py` usa `len(net.d)` come conteggio archi.)*

### 1.2 Che cosa la scena `(ii)` mi da' gia', verificato dal codice

| dove | che cosa |
|---|---|
| `test["dati"]["coorti"]["massa_0"...]` | **gli indici dei nodi** di ogni regione *(e `"vuoto"` per il resto)* |
| `test["dati"]["scena_ii"]` | `sep`, `r_regione`, `raggio_vuoto`, `R_CONN`, `dentro`, `quota` |
| `net.i`, `net.j`, `net.d` | gli archi e la loro **lunghezza** |

**`conc_nodi` NON e' toccato dalla scena, di proposito** *(le regioni non sono masse seminate)*:
quindi **le masse si trovano dalle `coorti`, non dal lignaggio**.

### 1.3 Il problema che mi aspetto sia il piu' difficile: **che cos'e' «il CENTRO» di una regione**

Luca chiede la distanza **fra i CENTRI**. Ma un centro geometrico si prende da `pos`, **e `pos` e'
proprio cio' che non deve entrare**. La mia scelta, da dichiarare:

- **il centro e' il MEDOIDE DI GRAFO della regione**: il nodo che **minimizza la somma delle
  distanze pesate con `d`** verso gli altri nodi della regione, calcolato **sul sottografo indotto
  dalla regione**. **Nessun `pos`.**
- **e riporto ANCHE la distanza INSIEME-INSIEME** *(il minimo fra un nodo qualunque di `A` e uno
  qualunque di `B`)*, perche' e' la grandezza che non ha bisogno di un centro, e le due rispondono
  a domande diverse: *«quanto distano i cuori»* contro *«quanto distano le superfici»*.
- **il centro da `pos` lo calcolo come DIAGNOSTICO**, per dire **se coincide**: se coincidesse
  sempre, la scelta del medoide sarebbe indifferente; se non coincide, e' un fatto da sapere.

**Cosa NON so:** se il medoide sia **unico**. Con `d` quasi uniformi possono esserci pareggi. **Se
ci sono, lo dico e prendo l'indice minore** — una regola dichiarata, non un caso taciuto.

### 1.4 Una trappola che mi ha gia' morso OGGI, e che rimorderebbe

**`_cli_flag.argv_del_driver` taglia all'ancora `S._applica_flag(a)`, e le tre righe che riempiono
`S._NMASSE_VIDEO` stanno DOPO.** Chi carica la scena in-process senza riempirle **ottiene il `sep`
di MODULO (`3.0`) invece di quello del driver**: misurato **oggi**, `n = 2124` invece di `12 814`,
e ha fatto sbagliare un numero al sigillo `T2`. **Lo strumento deve riempirle, e il collaudo deve
verificare che il `sep` usato sia quello del driver.**

### 1.5 Che cosa mi aspetto dai numeri

- **`L/d >= 1` sempre**, dove `L` e' la distanza lungo il grafo e `d` la distanza euclidea da `pos`:
  un cammino sul grafo non puo' essere piu' corto della linea retta **se gli archi sono corde**.
  **Non e' garantito**, perche' `d` non e' la lunghezza della corda in `pos`: e' una variabile di
  stato. **Quindi `L/d` puo' essere qualunque cosa, e il caso-che-deve-fallire e' proprio questo.**
- i **punti di controllo nel vuoto** dovrebbero dare una distanza **simile** a quella delle masse
  a parita' di distanza iniziale: **e' il braccio di confronto della `PROVA 1`**, e se al passo 0
  fossero diversi il confronto sarebbe viziato dalla partenza.

---

## 2. PROGETTAZIONE DEL RAGIONAMENTO — i criteri, **prima dei numeri**

**Lo strumento e' `csv/_osservabile_p1.py`**, e il sigillo `csv/_seal_fork/_sigillo_osservabile_p1.py`.

| # | criterio *(dettato da Luca)* | come si verifica | che cosa mi fa FERMARE |
|--:|---|---|---|
| **K1** | **collaudo su un grafo SINTETICO a distanza NOTA** *(catena, reticolo)* | **errore `< 1e-12`** contro il valore calcolato a mano | se l'errore e' `> 1e-12` su una catena, il cammino e' sbagliato e **nulla di cio' che segue conta** |
| **K2** | **il caso che DEVE fallire:** la stessa misura **con pesi da `pos`** da' un numero **DIVERSO** sulla scena `(ii)` | `L_d != L_pos`, cioe' **`L_d / L_pos != 1`** | se coincidessero, **non potrei dimostrare che lo strumento usa `d`**: il criterio esiste per rendere visibile la differenza, non per sperarla |
| **K3** | **invarianza:** stessa rete, **due chiamate** → **stesso numero** | uguaglianza **esatta** *(non «entro epsilon»)*: e' un calcolo deterministico su dati immobili | qualunque differenza: c'e' uno stato che cambia sotto la misura, e va trovato **prima** |
| **K4** | i **punti di CONTROLLO nel vuoto**, alla **stessa distanza iniziale**, **lontani dalle masse** | esistono, e la loro distanza sta **entro una tolleranza dichiarata** da quella delle masse; e la loro distanza **da ogni nodo di massa** supera `r_regione` | se non se ne trovano, la `PROVA 1` **non ha braccio di controllo**, e va detto invece di aggirarlo |
| **K5** | **dispersione fra semi, `>= 4` semi** (`P3`) | quattro semi, **un processo per braccio** (`STANDARD 1`), e l'IC95 col `t` di Student giusto per **3** gradi di liberta' *(`t(3) = 3.182`)* | con meno di 4 semi **non si riporta una barra**: `t(0.025,1) = 12.706` la rende inutilizzabile |

### 2.1 Le letture si fissano QUI

- **`K1` e' la porta:** se non passa, gli altri **non si leggono**. La catena: `N` nodi in fila,
  pesi `w_k` → distanza fra gli estremi **`sum(w_k)`**, e fra `a` e `b` **`sum(w_k)` sul tratto**.
  Il reticolo: griglia `m x m` a pesi unitari → distanza **Manhattan**, `|dx| + |dy|`.
- **`K2` si scrive come DISUGUAGLIANZA, non come «sono diversi»:** si riporta **`L_d / L_pos`** col
  suo valore, e il criterio e' **`|L_d/L_pos - 1| > 1e-6`**. *(Un criterio «diversi» sarebbe
  soddisfatto da due `NaN`.)*
- **`K4` porta la sua tolleranza SCRITTA PRIMA: `10 %`** sulla distanza iniziale. **E se non si
  trovano punti entro il `10 %`, il criterio FALLISCE** — non si allarga la tolleranza dopo
  (`P1-sexies`, e la soglia non si calcola dai dati che giudica).
- **`K5` riporta l'IC95, e se contiene lo zero si scrive come LIMITE**, non come «nessun effetto»
  — e **con la risoluzione accanto**.

### 2.2 Che cosa questo task **NON** fa

**Non fa la `PROVA 1`.** Fa **la grandezza** che la `PROVA 1` misurera', e i suoi collaudi.
**Nessun run lungo, nessun passo di dinamica oltre la costruzione della scena.** Si ferma al sigillo.

---

## 3. TODO DEL NEXT STEP

- [ ] `csv/_osservabile_p1.py`: legge **uno snapshot** *(`.pkl`/`.pkl.gz`)* **o una rete viva**;
- [ ] Dijkstra con pesi **`net.d`** dall'idioma dei quattro script, `ones` → `d`;
- [ ] centro = **medoide di grafo** della regione *(pareggi: indice minore, dichiarato)*;
- [ ] distanza **centro-centro** per ogni coppia, **piu'** la distanza **insieme-insieme**;
- [ ] punti di **controllo** nel vuoto: stessa distanza entro il **10 %**, distanza da ogni massa
      **`> r_regione`**;
- [ ] **componenti connesse**: se due masse non comunicano, `inf` **dichiarato**, non stampato;
- [ ] `csv/_seal_fork/_sigillo_osservabile_p1.py`: `K1`-`K5`, **via CLI**, **un processo per
      braccio**, **giro corto prima**;
- [ ] inventario + README + relazione **nello stesso commit**;
- [ ] **STOP.**
