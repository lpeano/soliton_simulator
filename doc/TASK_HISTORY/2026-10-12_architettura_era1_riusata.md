# IL CENSIMENTO DELL'ARCHITETTURA DELL'ERA `1` — **gli SCHEMI, non le leggi**

> ### ⛔ **QUESTO FILE SI COMMITTA *PRIMA* DEL CODICE DEL SIMULATORE** *(par.8, e il
> mandato lo ripete: «il censimento nella task history, PRIMA del codice»)*.

**Mandato:** `[[BASTA-PROTOTIPI]]` passo `4`, voce `[[ARCHITETTURA-ERA1-RIUSATA]]`, piu'
l'**aggiunta sulla rappresentazione del grafo** del `2026-10-12`.

> ### ⭐ **E OGNI RIGA E' LETTA DAL CODICE, NON DAI COMMENTI** *(par.2)*: sotto, ogni
> schema porta il **nome della funzione** che l'ho trovato a fare, perche' i numeri di riga
> **sono shiftati**.

### ⚠ **E LA STELLA POLARE NON SI APPLICA A QUESTO FILE:** `L-STELLA` chiede le cinque
risposte **a ogni commit che cambia la FISICA**, e questo censimento **non cambia nessuna
legge** — censisce **schemi di architettura**. ### **Si applichera' al commit che porta
`F1`..`F10` in tabella.**

---

## 1. RAGIONAMENTO PRELIMINARE — *che cosa mi aspetto, e che cosa NON so*

### ⭐ **CHE COSA MI ASPETTAVO, E DOVE MI SONO SBAGLIATO**

Mi aspettavo di dover **inventare** la struttura compatta dei vicini per l'era `2`. ### ⛔
**L'ERA `1` LA HA GIA', ED E' UNA `CSR`:** `_costruisci_struttura` costruisce una
`coo_matrix` e la converte in `tocsr()`, tiene in cache `_perm` *(posizione `CSR` →
indice originale)*, e la sua docstring dice il criterio: *«la topologia cambia solo alla
nascita di puntatori o per mitosi, i pesi cambiano a ogni passo»*.

### **Quindi il lavoro non e' inventare: e' ADATTARE.** E la cosa da adattare e' il
passaggio da **nodi** a **ESTREMITA' D'ARCO**, che e' dove vive lo stato della camminata.

### **CHE COSA NON SO**

1. **se la `CSR` di `scipy` convenga anche per la camminata**, o se bastino i due array
   `indptr`/`indici` fatti a mano: la `CSR` di `scipy` porta con se' una matrice sparsa che
   nella camminata **non serve** *(non c'e' nessun prodotto matrice-vettore: c'e' una
   permutazione)*;
2. **quale strategia di crescita costi meno** fra capacita' preallocata col raddoppio e
   ricostruzione a evento — e **non lo decido a occhio**: e' una misura;
3. **quanto pesa davvero una scena ben fatta**: la soglia del vincolo `(d)` va fissata su
   un numero misurato, non su un'aspettativa.

---

## 2. IL CENSIMENTO — **dove sta, che problema risolveva, `primo_ordine` lo ha, come si adatta**

### ⭐ **`A` LA RAPPRESENTAZIONE DEGLI ARCHI** *(aggiunta `(a)`)*

| | |
|---|---|
| **dove sta** | `self.i`, `self.j` — **due vettori di indici** paralleli, un elemento per arco. I gradi: `_grado()` fa `np.bincount(self.i) + np.bincount(self.j)`. Le somme sui vicini: **`np.add.at`**, usato **`34` volte** nel file *(e `np.bincount` **`32`**)* |
| **che problema risolveva** | ### **nessuna lista di liste nel percorso caldo**: tutto e' un array, e una somma sui vicini e' **una sola chiamata vettoriale** invece di un ciclo Python per nodo |
| **la crescita** | alla nascita, dal **punto unico di scrittura**: `net.i = concatenate([net.i[keep], a, m])` e il compagno su `j` — l'arco diviso **sparisce** e nascono i due nuovi |
| **`primo_ordine` lo ha?** | ### ✅ **SI', GIA':** `passo.py` lavora su `(ii, jj)` *(`mezzo_implicito`, `passo_globale`, `passo_locale`, `strati`)*, `grafo.py` **valida** `(ii, jj, n)` a ogni passo e **una violazione FERMA**, e `_genera.py` emette `np.add.at` per le somme sui vicini |
| **come si adatta** | lo stato della camminata sta sulle **ESTREMITA'**, non sui nodi: servono **due array derivati**, `nodo[h]` *(il nodo di ogni estremita')* e `partner[h]` *(l'altra estremita' dello stesso arco)*, entrambi **ricavati da `(ii, jj)`** e **non memorizzati come verita' indipendente** — cosi' non possono divergere |

### ⛔ **`B` LA STRUTTURA DEI VICINI** *(aggiunta `(b)`)*

| | |
|---|---|
| **dove sta** | `_costruisci_struttura()`: `coo_matrix(...).tocsr()`, con `_perm` in cache. ### **E' una `CSR` SIMMETRICA**, cioe' esattamente *«un unico array di indici piu' gli offset per nodo»* |
| **che problema risolveva** | la topologia cambia **solo alla nascita**, i pesi **a ogni passo**: separare le due cose permette di **costruire la struttura una volta** e riempirne i dati a ogni tick |
| **il banco invece** | ### ⛔ **TIENE TUPLE DI TUPLE:** `scena.py` fa `vicini = [[] for _ in range(n)]` e poi `tuple(tuple(x) for x in vicini)` — cioe' **`n` oggetti Python piu' uno per arco**. ### **E' il difetto che la diagnosi ha misurato** |
| **`primo_ordine` lo ha?** | ### ⚠ **NO:** `grep` su `indptr`, `csr`, `bincount` in `primo_ordine/*.py` trova **solo** l'`np.add.at` del generatore. ### **La struttura compatta dei vicini va PORTATA** |
| **come si adatta** | due array: **`offset[n+1]`** e **`vicini_piatti[2m]`**, piu' i due derivati `nodo[h]` e `partner[h]`. ### **Nessuna matrice sparsa**, perche' nella camminata non c'e' un prodotto matrice-vettore: lo spostamento e' **una PERMUTAZIONE** *(`psi'[partner[h]] = U[h] psi[h]`)*, e una permutazione vuole **un array di indici**, non una `CSR` |
| ### 📌 **la strategia di crescita** | **capacita' preallocata con RADDOPPIO**, e il motivo e' un conto: la ricostruzione a evento costa `O(m)` **a ogni nascita**, quindi `O(m²)` su una corsa che cresce; il raddoppio costa `O(m)` **ammortizzato su tutta la corsa**. ### ⛔ **E la crescita passa dal PUNTO UNICO DI SCRITTURA**, come nell'era `1` |
| ### ⚠ **e il prezzo del raddoppio, dichiarato** | tiene **fino al doppio** della memoria utile. ### **Va dentro il vincolo `(d)`**, non accanto |

### ⛔ **`C` IL KD-TREE NON ENTRA NELLA FISICA** *(aggiunta `(c)`)*

| | |
|---|---|
| **dove sta nell'era `1`** | `from scipy.spatial import cKDTree` in testa, e **sei usi**: `_allaccia` *(due alberi su `self.pos`, collega entro `3 ×` la mediana di `lambda_nodi`)*, una **verifica contro tutti i nodi**, e **quattro** nel disegno e nelle analisi |
| **che problema risolveva** | trovare i vicini **per POSIZIONE** |
| **perche' NON serve nell'era `2`** | ### **i vicini sono quelli del GRAFO** *(decisione `9`, `[[DOMANDA-D9-GEOMETRIA]]`)*, e la regola di nascita usa **solo il grafo** *(i vicini comuni dei genitori, `[[SPAZIO-CHE-NASCE]]` `A3(a)`)* |
| **dove resta ammesso** | ### **solo** nella costruzione delle **scene di CONTROLLO** *(`scene3d.py`, `pesi4.py`)* e nell'### **osservatore del disegno `3D`** |
| ### 📌 **il collaudo** | un braccio verifica **SUL SORGENTE** che il codice della fisica **non importi strutture spaziali** — e si guarda il **CODICE** e non la prosa *(e' lo stesso errore che mi ha fatto fallire due bracci il `2026-10-11`)* |

### ⭐ **`D` LA FOTOGRAFIA DELL'ISTANTE `t−1`**

| | |
|---|---|
| **dove sta** | `_smp_apri()`, `_smp_chirurgia(keep, nuovi)`, `_smp_chiudi()` |
| **che problema risolveva** | **lettura CAUSALE**: una legge deve leggere lo stato di `t−1`, non quello che una legge sorella ha gia' cambiato. E la fotografia e' **SOVRASCRITTA**, quindi la memoria e' **COSTANTE** |
| ### ⭐ **e due cose che il codice fa e che vanno copiate** | `1` **E' IDEMPOTENTE**, e la docstring dice perche': la chiamano **tutte e cinque** le leggi in testa, e **la prima che gira apre** — *«l'idempotenza mette il confine DENTRO la cosa che deve rispettarlo, e lo rende indipendente dall'ORDINE»*. `2` **CONTA** quante volte l'ha trovata gia' aperta *(`_g_smp_gia_aperta`, `A8`)*, cosi' il numero e' **leggibile invece che supposto** |
| ### 📌 **e `_smp_chirurgia` e' il pezzo che serve alla MITOSI** | la fotografia **segue** la nascita: `keep` per gli archi che restano, `nuovi` per quelli che nascono |
| **come si adatta** | nella camminata diventa il ### **DOPPIO CONTENITORE** per `psi` e `phi`, **scambiato a ogni tick**: i pezzi del passo scrivono **DENTRO** contenitori esistenti *(in-place, `out=`)*, e gli array di lavoro del **punto medio implicito** si preparano ### **UNA VOLTA PER SCENA** |
| ### ⚠ **e qui c'e' il legame con la diagnosi** | la diagnosi ha misurato temporanei pari a ### **`61` volte lo stato per chiamata** nel punto medio implicito. ### **Sono RILASCIATI**, quindi non erano la causa dei gigabyte — ma con i buffer preallocati ### **non nascerebbero affatto** |

### ⭐ **`E` IL PUNTO UNICO DI SCRITTURA**

| | |
|---|---|
| **dove sta** | `nascita(net, evento, c)`, e la sua docstring e' una **regola**: *«IL PUNTO UNICO: scrive le grandezze della nascita, in ordine DICHIARATO»*, con `c` il **contesto** e il vincolo che le regole **non leggano `self.n`** |
| **che problema risolveva** | prima erano **TRE** i posti che scrivevano, piu' una crescita per **mutazione** *(`.append`, che l'AST non vede)*. ### **Ora e' UNO** |
| ### ⛔ **e il presidio che lo tiene** | *«una grandezza del registro che non compare nella tabella dell'evento **FERMA IL RUN**: non e' un avviso, e' un `RuntimeError`»* |
| **come si adatta** | ### **serve alla mitosi dell'era `2`**: la nascita del nodo e' **un evento unico**, e l'### **immersione isometrica** *(norme conservate attraverso la nascita)* si verifica **in quel punto** e in nessun altro |

### ⚠ **`F` LE CACHE CROSS-PASSO, E LA REGOLA `A8b`**

| | |
|---|---|
| **dove sta** | due siti commentati `A8b`, e il piu' chiaro dice: *«e' un difetto di LUNGHEZZA (`A8b`: cache cross-passo letta con una lunghezza diversa)»* |
| **che problema risolveva** | ### **niente: era il DIFETTO.** Una cache riempita al passo `t` e letta al passo `t+1` **quando il grafo e' cresciuto** ha la lunghezza **sbagliata**, e il sistema **cadeva nei ripieghi** — misurato nell'### **`80%` dei passi** su una cache |
| ### ⛔ **la lezione, ed e' la piu' importante per l'era `2`** | ### **ogni cache cross-passo porta la TAGLIA a cui e' stata riempita**, e chi la legge **confronta** — altrimenti il difetto **non si vede**, si **degrada in silenzio** |
| **come si adatta** | nel simulatore il grafo ### **CRESCE PER MITOSI**, quindi questo non e' un caso di bordo: e' ### **il caso normale** |

### ⭐ **`G` I CONTATORI DEI RIPIEGHI** *(`A8`)*

| | |
|---|---|
| **dove sta** | i campi `_g_*` *(per esempio `_g_smp_gia_aperta`, `_g_compat_chi_tot`, `_g_compat_chi_spento`)* |
| ### ⭐ **che problema risolveva, e vale per l'era `2`** | *«e' un presidio contro un'ACCENSIONE SILENZIOSA: il giorno in cui qualcuno accende `COMPAT_CHI`, il numero cambia»* — e accanto c'e' la misura: ### **ramo SPENTO `12` volte su `12`** |
| **come si adatta** | ### **ogni POSTO DICHIARATO di `A1`..`A5` vuole il suo contatore**: cosi' *«il posto e' al comportamento attuale»* e' un **numero** e non una **promessa** |

### ⚠ **`H` CHECKPOINT, RIPRESA, SALVATAGGIO DURANTE LA CORSA**

| | |
|---|---|
| **dove sta** | ### ⛔ **NON C'E' NELL'ERA `1`:** `grep` su `checkpoint`, `ripresa`, `riprendi` in `soliton_simulator.py` trova ### **ZERO** definizioni |
| ### ⭐ **e lo schema viene dal BANCO, non dall'era `1`** | l'ho scritto il `2026-10-11` **dopo averci perso `2.8` ore**: il `json` si scriveva **solo alla fine**, il run e' caduto e ### **ha perso tutto**. Adesso si scrive ### **dopo ogni scena** |
| **come si adatta** | nel simulatore: le **grandezze osservate** su disco **durante** la corsa, e lo **stato per la ripresa** a **intervalli DICHIARATI** — ### ⛔ **mai lo stato a ogni tick** *(`[[MEMORIA-PER-TICK]]` `D2(c)`)* |

### ⭐ **`I` LO SCHEDULATORE E IL TEMPO PROPRIO LOCALE**

| | |
|---|---|
| **dove sta nell'era `2`** | ### ✅ **GIA' PORTATO**, e con un presidio: `P-ES1` dice *«un solo esecutore»*, e il collaudo lo verifica — l'esecutore e' `primo_ordine/passo.py` |
| **che problema risolveva nell'era `1`** | il tempo proprio locale e' `tau = 1 + |tw|/PHI_CRIT`, **nel kernel** |
| **come si adatta** | ### **il POSTO e' cablato, la FORMA e' aperta** *(`A1` della carta: `cs = 1` come il `v3`)*, e ogni legge che evolve prende `dtau_k = cs_k · dt` |

### ⭐ **`L` IL DISEGNO `3D` COME OSSERVATORE**

| | |
|---|---|
| **dove sta** | quattro dei sei usi di `cKDTree` **sono li'**, piu' `self.pos` |
| **come si adatta** | ### **le posizioni servono SOLO a guardare**, si ricostruiscono **dal seme**, e la scena ### **non le contiene** — e un braccio del banco lo verifica **sul sorgente** |

---

## 3. IL VINCOLO `(d)`, E LA SOGLIA SI FISSA QUI

> ### ⛔ **LA MEMORIA DELLA SCENA DEVE ESSERE PROPORZIONALE AGLI ARCHI E DELLO STESSO
> ### ORDINE DELLO STATO.**

| | la soglia, fissata PRIMA | come si misura |
|---|---|---|
| `m1` | la memoria della **scena** sta ### **entro `4` volte lo stato** *(`2 m × 2 ×  16` byte)* | la privata del processo **dopo** la costruzione, meno quella **prima**, su **due taglie** |
| `m2` | e il rapporto fra due taglie e' ### **stabile entro il `20%`** | cioe' **proporzionale agli archi**, non di piu' |
| `m3` | la memoria **per tick** e' ### **piatta** *(pendenza compatibile con `0` a `3 sigma`)* | la misura che la diagnosi usa gia' |
| `m4` | e tutte e tre si ### **TIMBRANO con la corsa**, accanto al costo per tick | `[[MEMORIA-PER-TICK]]` `D2(a)` |

### ⚠ **PERCHE' `4` E NON `1`:** il **raddoppio** della capacita' tiene fino al **doppio**
della memoria utile, e `offset` piu' `vicini_piatti` piu' i due derivati `nodo` e `partner`
sono ### **quattro array di interi** contro **due array di complessi** dello stato. ### ⛔
**E il `4` e' un TETTO di progetto, non una legge fisica:** se la misura dira' meno, il
tetto **scende**.

### ⛔ **E IL NUMERO DA BATTERE E' MISURATO:** il banco sta a ### **`104` volte lo stato**
*(`441` MB in piu' per la scena a `n = 26000`, con lo stato a `4.254` MB)*. ### **La
soglia `m1` chiede `26` volte meglio.**

---

## 4. TODO DEL NEXT STEP

| | il passo | cosa decide |
|---|---|---|
| `1` | committare e pushare **questo file** | l'ordine verificabile da git |
| `2` | la **sezione nuova** in `doc/REFERTO_legame.md` *(il resto invariato)*, col blob riaggiornato nei REPERTI | il passo `2` del mandato |
| `3` | la derivazione di `[[SPAZIO-CHE-NASCE]]` *(solo task history)* | il punto `(a)` dell'ordine |
| `4` | gli **array compatti** dei vicini in `primo_ordine`, col raddoppio e il punto unico di scrittura | il punto `B` del censimento |
| `5` | il **doppio contenitore** e i buffer del punto medio implicito | il punto `D` |
| `6` | i **collaudi**: `m1`..`m4`, e il braccio **sul sorgente** che la fisica non importi strutture spaziali | il vincolo |

### ⛔ **E LA COSA CHE NON FARO': PORTARE UNA LEGGE IN TABELLA PRIMA DELLA DERIVAZIONE.**
L'ordine del mandato e' `(a)` derivazione, `(b)` simulatore, e ### **il censimento sta
dentro `(b)`** — non lo scavalca.
