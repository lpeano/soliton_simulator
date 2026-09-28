# `T2c` — **la mitosi NON si spezza per TIPO restando byte-identica** *(2026-09-28)*

> **Mandato:** *«due voci nel registro al posto di "mitosi": una STRUTTURALE (decide dove nascere,
> crea nodi e archi, divide gli archi) e una di STATO (inizializza i nati). […] STESSO ORDINE delle
> operazioni di oggi: deve essere byte-identico.»*
>
> ### 🛑 **LE DUE RICHIESTE SONO INCOMPATIBILI, e l'ho misurato.** Nessun codice scritto.
> **Blob del simulatore `1fc9235f`, prima e dopo.**

---

# 1. LA MISURA: **non c'è nessuna cucitura**

`mitosi()` ha **105 istruzioni di primo livello**, righe `6057-6588` *(**532 righe**)*. Di queste,
**26** scrivono stato o struttura. **In quest'ordine:**

```
STRUT STRUT STATO STRUT STATO STRUT STATO STATO STATO STATO STATO
STRUT STATO STATO STRUT STRUT STRUT STATO STATO STATO STATO STRUT
STATO STATO STRUT MISTA
```

| | |
|---|---|
| ultimo blocco **`STATO`** | posizione **23** |
| primo blocco **`STRUT`** | posizione **0** |
| ### cucitura *«stato poi struttura»* | ### **NO** |
| ### cucitura *«struttura poi stato»* | ### **NO** |

### **Struttura e stato si ALTERNANO, e l'ultimo blocco scrive ENTRAMBI.**

**Alcuni esempi dall'ordine reale:** `:6252` `_rep` *(struttura)* → `:6295` `d0` *(stato)* →
`:6334` `negate` *(struttura)* → `:6380-6398` sette blocchi di **stato dei nodi nati** →
`:6446-6450` `i`, `j`, `conc_archi` *(**la struttura degli archi**)* → `:6459-6472` `d`, `d0`, `vd`,
`peq`, `tw`, `twp` *(**lo stato per arco**)* → `:6481` **MISTA**.

> ### 📌 **Il punto che decide:** ### **lo stato dei nodi NATI è scritto PRIMA della struttura degli
> archi** *(`:6380` viene prima di `:6446`)*, e **lo stato per ARCO è scritto DOPO**.
> **Quindi «prima la struttura, poi lo stato» NON è l'ordine di oggi, e nemmeno il suo contrario.**
> ### **Spezzare per tipo richiede di RIORDINARE, e riordinare cambia la fisica.**

**⚠ E c'è una cosa peggiore dell'alternanza:** l'istruzione `:6481` è ### **MISTA** — un solo blocco
che scrive **`d`, `d0`, `eta`, `mem_mot`, `peq`, `perc_chi`, `perc_geom`** *(stato)* **e** `_rep`,
`coppie_nate`, `i`, `j`, `nati`, `perc_tw` *(struttura)*. **Non è alternanza: è intreccio dentro la
stessa istruzione.**

---

# 2. LA DIVISIONE CHE **SAREBBE** BYTE-IDENTICA: per **CANALE**, non per tipo

Il blocco `:6481` è ### **la creazione di coppia alla Schwinger**, guardata da
`if COPPIA_MIT > 0.0 and self.n < MAX_NODI:`, ed è ### **la PENULTIMA istruzione** — dopo di lei
c'è solo `return len(sel)`.

| | |
|---|---|
| dimensione | righe `6481-6587`, **107 righe** su 532 |
| variabili locali che legge dal corpo di `mitosi` | ### **CINQUE: `a`, `b`, `fm`, `sciolta`, `sel`** |
| variabili proprie | 21 |

### **Un blocco finale, autonomo, con cinque valori di contesto: si stacca senza riordinare niente.**

> **E il nome è già nel tuo piano:** *«LEGGI STRUTTURALI (mitosi, Schwinger)»*. ### **Sono due
> CANALI DI NASCITA, e il registro può nominarli separatamente restando byte-identico.**

**⚠ Ma va detto che cosa NON risolve:** ### **entrambe restano `AMBIGUA`.** La mitosi per divisione
scrive struttura **e** stato; la Schwinger pure *(è il blocco `MISTA`)*. **Spezzare per canale
raddoppia il numero delle voci ambigue invece di togliere l'ambiguità** — e per `9-ter` **il conto
delle leggi non deve crescere senza motivo.**

---

# 3. LE STRADE, e la decisione è di Luca

| | strada | byte-identico? | che cosa dà |
|---|---|---|---|
| **(a)** | **la mitosi resta UNA voce, `AMBIGUA`**, e la si spezza **in `T3`**, quando le variazioni si separano dalle scritture e il riordino è **il lavoro previsto** | ### **sì** *(niente cambia)* | ### **niente adesso**, ma **l'ambiguità resta dichiarata e visibile**, e `T3` la scioglie dove il riordino è legittimo |
| **(b)** | **si spezza per CANALE**: `mitosi` + `schwinger` | ### **sì** | due voci al posto di una, **entrambe `AMBIGUA`**: il registro è più fine ma **l'ambiguità raddoppia** |
| **(c)** | **si spezza per TIPO adesso**, riordinando | ### **NO** | l'ordine cambia, e con lui la fisica: **è `T3` sotto un altro nome**, senza la fotografia e senza le variazioni che lo rendono corretto |

## ➜ **La mia raccomandazione è (a)**, e per una ragione precisa

> **`T2` esiste per dichiarare i tipi *senza cambiare comportamento*.** L'ambiguità della mitosi
> ### **non è un difetto della dichiarazione: è un FATTO del codice**, e il tipo `AMBIGUA` lo dice
> correttamente. **Spezzarla per canale la nasconderebbe meglio senza risolverla** *(due `AMBIGUA`
> invece di una)*; spezzarla per tipo **richiede il riordino**, che è precisamente ciò che `T3` fa
> **con la fotografia e le variazioni** — cioè con gli strumenti che rendono il riordino **corretto
> invece che azzardato**.
>
> ### **In (a) non si perde niente:** la voce resta `AMBIGUA` nel registro, la verifica statica dei
> tipi **continua a passare 8/8** *(l'`AMBIGUA` è coerente: scrive davvero entrambi)*, e il lavoro
> si fa **una volta sola**, in `T3`, invece di due volte.

**Se scegli (b)**, il lavoro è chiaro e piccolo: estrarre il blocco finale in un metodo che riceve
i **cinque** valori di contesto, aggiungere la voce al registro e alla composizione **subito dopo
`mitosi`**, e il sigillo byte-identico come da mandato. ### **Lo dico perché è fattibile, non perché
lo consigli.**

---

# 4. Il resto del mandato, e cosa resta valido

| chiesto | stato |
|---|---|
| verifica statica dei tipi **9/9** | ### **oggi è 8/8 e passa.** Diventa 9 solo con la strada **(b)** |
| il caso che deve fallire *(le due voci invertite → rifiutate)* | ### **pronto per (b)**: la validazione già impone la **coda fissa**, e basterà aggiungere la regola *«la struttura viene DOPO le dinamiche»* — che **oggi non esiste** perché non c'è una voce strutturale separata |
| il sigillo sulla scena del pilota fino al passo 60, con `_g_smp_chirurgie > 0` | ### **non girato**: senza codice da sigillare non c'è niente da confrontare. **Resta il criterio**, e vale per (b) e per `T3` |
| `H-ETC-2` permuta solo fra dinamiche, struttura **dopo** | ### **da cablare nella validazione**, e ha senso **solo** quando esiste una voce strutturale distinta |

---

## LE VOCI D'INDICE CHE QUESTO DOCUMENTO TOCCA

`SCHED-PASSO` · `SCHED-T2-TIPI` · `ETC-PASSO` · `A1` · `A9`
