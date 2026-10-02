# 📜 **LA STORIA DEL PROBLEMA: la MITOSI e la nascita di nodi e archi**

> ### **Passo 1 del riordino** *(`par.8`: il ragionamento si scrive **prima**)*. **Nessun codice di
> fisica in questo giro.** Blob del simulatore al momento della scrittura: **`62d67675`**.

**Perche' esiste questo documento:** il riordino della mitosi non e' una ristrutturazione a mente
fresca. ### **E' l'ultimo atto di una storia lunga**, e quasi tutto cio' che oggi sembra arbitrario
e' stato messo li' da una cura precedente, per una ragione che allora era buona.
### **Riordinare senza quella storia vorrebbe dire rimettere i difetti che sono stati appena
curati.**

---

## 0. **Che cos'e', in numeri MISURATI**

| | |
|---|---|
| la funzione | `mitosi`, ### **`:6680`-`:7228` = 549 righe** *(e contiene **anche** il canale di Schwinger: non e' una funzione a se')* |
| attributi scritti dentro | ### **56 distinti, 79 scritture** |
| di cui **allungano** *(`concatenate`/`vstack`)* | ### **19 distinti, 38 scritture** |
| mutati **in posto** *(`.append`)* | **1**: `conc_nodi`, **2 volte** |
| grandezze del **registro** scritte **qui** | ### **16 su 30** |
| grandezze del registro scritte **ALTROVE** | ### **13** — in `_eredita_psi_figli` e `_eredita_spinore_figli` — **piu'** `conc_nodi` per mutazione |

### ➜ **E' questo il numero che giustifica il riordino:** la nascita di un nodo tocca **30**
grandezze dichiarate, e oggi ### **le scrive in TRE posti diversi** — dentro `mitosi`, dentro due
funzioni di servizio, e una per mutazione in posto. *(Misurato dall'AST sul blob `62d67675`.)*

---

## 1. **LA STORIA, in ordine: ogni intervento, e cosa ha rotto**

### 🧬 **La famiglia piu' lunga: «una cache non estesa alla mitosi»** — e sono **SETTE**

| quando | che cosa | hash / ID |
|---|---|---|
| **2026-09-06** | `spinore-corretto`: **eredita' coerente delle cache spinoriali dopo mitosi/Schwinger** *(«regola D, niente reset spurio di `_psi_prec`»)*. ### **E' il primo intervento sull'eredita' alla nascita** | `5769a12` |
| *(epoca 1)* | ### **`C7`**: `_cs_nodo_prev` **veniva scartata a ogni mitosi** | `C7` → cura `COMPONENTI:D1` |
| *(epoca 1)* | ### **`C11`**: `_psi_spin_prec` **non era esteso alla mitosi**, e la guardia esatta ### **fu inerte nel 95.33 % delle chiamate PER MESI** | `C11` → cura `COMPONENTI:D2` *(«settima voce della stessa convenzione»)* |
| **2026-09-28** | ### **`PSI-FLASH`**: la mitosi **non estendeva `psi`**, quindi `len(psi) < n` e ### **la schermatura si spegneva PER TUTTA LA RETE** — `lambda` da `0.60` a `0.80`, `\|psi\|` **+62 %**, pozzo **130 → 366** | `4efd3ae` |
| **2026-09-28** | il **gradino al passo dopo**: `rho_spin` si eredita, e i **due ripieghi** di `_rho_sorgente`/`_nb_grav` ### **sollevano** invece di sostituire | `57a3f08` |

> ### 📌 **LA LETTURA, e vale piu' dei singoli difetti:** la stessa famiglia e' stata curata
> ### **UNA CACHE ALLA VOLTA, per settimane** — `_cs_nodo_prev`, `_psi_spin_prec`, `_psi_spinor`,
> `_psi_prec`, `psi`, `rho_spin`, `psi_spin` — ### **e ogni cura era giusta e NON bastava**, perche'
> il difetto non era nella cache: era ### **nel fatto che la nascita non avesse un posto solo.**
> **Il `CONTROLLO UNICO` ha chiuso la famiglia per STRUTTURA** *(`RIPIEGHI-ZERO`, chiusa il
> 2026-09-29)*, ### **ma il riordino e' quello che toglie la CAUSA.**

### ⚙ **Le cure di LEGGE sulla mitosi**

| quando | che cosa | che cosa ha ROTTO | hash / ID |
|---|---|---|---|
| **2026-09-16** | ### **`_xi_rumore` NON SI EREDITA**: `xi` e' **l'ambiente**, non una proprieta' del nodo — *«categoria D, nessun flag»* | niente | `f9bde1e` |
| **2026-09-24** | **`CURA 2`**: **un solo orologio** dentro `mitosi()`, **flag spento** | il flag nasce **inerte**: i rami `else` restano | `c04d2b0` |
| **2026-09-25** | **`CURA 5` / `MITOSI_2LAM`**: ### **`A13` alla nascita — un arco si divide SOLO se `d >= 2 LAM`**. **Flag OFF** | ### **il flag era MORTO** *(non arrivava al modulo)*, scoperto due giri dopo | `127cc11`, poi `03abe62` |
| **2026-09-25** | *(difetto di PATCH, non di fisica)* | ### **avevo separato `MITOSI_2LAM` dal SUO commento** — e `H-P7` esiste per questo | `762ca15` |
| **2026-09-27** | **`CURA2-STRUTTURALE`**: i **quattro** rami `else` **escono dal sorgente** — *«il flag e' una LEGGE, non un interruttore»* | i rami a flag spento vanno **archiviati copiati**, non cancellati | `3e265d2`, ID `CURA2-STRUTTURALE`, `RAMI-OFF-CURA2` |

### 📒 **E poi la struttura, in questa sessione**

| quando | che cosa | hash |
|---|---|---|
| **2026-09-29** | ### **`REGOLE_nascita.tsv`: 32 regole di nascita DICHIARATE**, ognuna verificata **per ancora cercata nel testo** *(non per riga: le righe shiftano)* | `5512799` |
| **2026-09-29** | la **misura dell'ordine**: nella finestra della nascita, ### **BUCHI ZERO** — chi e' letto corto e chi no, e perche' | `bd9262f` |
| **2026-09-29** | il ### **CONTROLLO UNICO** dello schedulatore, e le **tre generalizzazioni** *(forma · dopo ogni voce · tipo)* | `c047850` … `ee7df74` |
| **2026-09-29** | ### **`RIPIEGHI-ZERO` CHIUSA**: sigillo su sei bracci, ripiego silenzioso **ZERO** | `98810aa` |

---

## 2. **LE TOPPE ANCORA PRESENTI NEL PERCORSO DELLA NASCITA**

**Classe:** **assioma** *(una legge, non un numero)* · **toppa** *(un rimedio locale a un sintomo)* ·
**numero derivato** *(viene da grandezze del sistema)* · **dichiarato** *(scritto e consapevole)* ·
**esplorativo** *(acceso per prova, non per decisione)*.

### ⛔ **① La SOGLIA della divisione: `3π`** — `:6708`

> ### ⛔ **CORREZIONE DEL 2026-10-01: LA DIVISIONE NON SCATTA «SOPRA `3π`».**
> *(Rilievo del guardiano, e `DIVISIONE-AUTOCONSISTENTE:M1` lo mostra con un numero.)*
>
> **Questa sezione descrive la soglia come NETTA — un valore sopra il quale si divide.** Il codice
> non fa cosi': la creazione passa per una ### **PROBABILITA' A CAMPANA**:
> ```
> pos_soglia = 1 + soglia/PHI_CRIT ;  pos_tetto = 1 + TW_TETTO/PHI_CRIT
> centro     = 0.5*(pos_soglia + pos_tetto)
> segno      = -tanh(3.0 * (pos_torsione - centro))        # :7068
> ```
> ### **Il segno e' POSITIVO (crea) per tutto cio' che sta SOTTO il `centro`**, e va da `+max`
> alla soglia a `−max` al tetto `4π`.
>
> ### ✅ **E LA MISURA LO CONFERMA:** fra gli **otto** archi divisi in 72 passi ce n'e' uno con
> ### **`|tw| = 3.79`**, cioe' ### **mezzo giro SOTTO `2π`** e **molto** sotto `3π`.
> *(In posizione: `1 + 3.79/6.283 = 1.603` contro un `centro = 2.75`, quindi
> `segno = −tanh(3·(1.603 − 2.75)) = +0.998`, ### **quasi il massimo della campana**.)*
> ### ➜ **Un gradino a `3π` non l'avrebbe mai diviso.**
>
> ### ⚠ **E UNA COSA CHE NON AFFERMO:** che cosa **seleziona** gli archi non e' questo segno da
> solo — se lo fosse si dividerebbe molto di piu'. ### **Il cancello completo e' una lettura a
> se'**, e non la faccio qui per non sostituire una descrizione sbagliata con un'altra.
>
> ### ➕ **E IL `3.0` DENTRO LA `tanh` E' UN NUMERO SCELTO A MANO:** entra nell'elenco del
> **criterio 2** di `doc/PIANO_divisione_e_calore.md` *(`A1`: la legge, non il numero)*.

> ### ⛔⛔ **CORREZIONE DEL 2026-10-01 (stesso giorno): IL `3.79` NON ESISTE, E LA CORREZIONE QUI
> ### SOPRA E' SBAGLIATA. Si ANNOTA e non si riscrive** *(par.8)*.
>
> ### **L'errore e' MIO, e ha generato il rilievo del guardiano:** nel referto di
> `DIVISIONE-AUTOCONSISTENTE:M1` avevo diviso `d_S_tw` per ### **`d_m`** *(gli archi nuovi)*
> invece che per ### **il NUMERO DI DIVISIONI**. Ma i due eventi non hanno la stessa impronta:
>
> | evento | `d_n` | `d_m` |
> |---|---|---|
> | una **divisione** | `+1` | `+1` *(uno rimosso, due aggiunti)* |
> | uno **Schwinger** | `+1` | ### **`+2`** |
>
> ### ➜ **L'evento del passo 70 era `d_n +3, d_m +4`, cioe' DUE DIVISIONI piu' UNO SCHWINGER**, e
> il `|tw|` per arco diviso e' ### **`15.1458 / 2 = 7.57`**, non `/4 = 3.79`.
>
> ### ✅ **I NUMERI VERI, ricalcolati separando gli eventi** *(`div = 2·d_n − d_m`)*:
>
> | | `|tw|` | in **avvolgimenti** |
> |---|---|---|
> | minimo | ### **6.9793** | ### **1.111** |
> | mediano | **7.5568** | **1.203** |
> | massimo | **8.3466** | **1.328** |
>
> ### 🔎 **E ADESSO IL CONTO TORNA, ED E' UNA SPIEGAZIONE DIVERSA DALLA CAMPANA**
> La soglia ### **modulata** vale `3π·(1 − 0.3·tanh(grad))`, cioe' sta fra ### **`6.5973`** e
> `9.4248` — ### **fra `1.05` e `1.50` avvolgimenti.** ### **TUTTI gli archi divisi stanno DENTRO
> quella banda** *(il minimo e' `6.98 ≥ 6.60`)*.
>
> ### ⛔ **E SOTTO LA SOGLIA LOCALE NIENTE PUO' DIVIDERSI, MAI:** `ecc = max(avv/soglia − 1, 0)` e'
> ### **clippato a zero**, `satura(0) = 0` ### **esattamente**, quindi `ampiezza = 0`, `resp = 0`,
> `prob = 1 − exp(0) = 0` e ### **`nasce` e' FALSO per costruzione.** ### **La campana
> `−tanh(3·(pos − centro))` non ammette archi sotto soglia: decide soltanto CREA contro RESPINGE
> SOPRA la soglia.**
>
> ### ➜ **LA FRASE GIUSTA, che sostituisce entrambe le precedenti:**
> ### **la soglia NON e' il `3π` nominale — e' `3π·(1 − 0.3·tanh(grad))`, e le divisioni avvengono
> ### nella PARTE BASSA di quella banda** *(da `1.11` a `1.33` avvolgimenti, contro un nominale di
> `1.50`)*. ### **Quindi «sopra `3π`» e' sbagliato, ma non perche' ci sia una campana: perche' il
> `3π` e' il TETTO della banda, non la soglia.**
>
> ### ⚠ **E IL `0.3` DELLA MODULAZIONE E' IL NUMERO CHE CONTA DAVVERO**, non il `3.0` della `tanh`:
> e' lui a decidere ### **quanto in basso** puo' scendere la soglia, cioe' ### **la larghezza della
> banda in cui la materia nasce.** ### **Entrambi restano nell'elenco del criterio 2**, ma
> ### **il `0.3` e' quello con l'effetto fisico misurato.**
>
> ### 📌 **E LA LEZIONE E' LA PIU' SCOMODA DELLA GIORNATA:** il guardiano ha costruito un rilievo
> ### **su un numero che avevo derivato male**, e io ### **l'ho scritto in DUE documenti come
> fatto, senza rifare il conto.** ### **Un numero generato da uno script non e' al sicuro se la
> FORMULA dentro lo script e' sbagliata**, e `L-NUMERI` non protegge da questo: ### **protegge
> dalla trascrizione, non dalla derivazione.**

> ### ✅✅ **ANNOTAZIONE DEL 2026-10-01 (punto 3 del guardiano): LA MODULAZIONE AGISCE, E LA
> ### SPIEGAZIONE DI `db89b37` REGGE. Era la mia «correzione» di `0487c20` a essere SBAGLIATA.**
>
> **Misurato DENTRO la decisione** *(`csv/_test_fork/_soglia_alla_divisione.py`, blob `e37a7d59`;
> fallback dell'orologio uniforme ### **scattato 0 volte**)*:
>
> | | |
> |---|---|
> | la soglia **minima** sulla rete | da ### **`6.9136`** a `9.4248` ➜ ### **la modulazione del `0.3` AGISCE** |
> | gli archi divisi | `|tw|` da `6.98` a `8.35`, ### **ognuno APPENA SOPRA la sua soglia locale** *(da `6.96` a `8.19`)*; ### **nessuno sotto** |
> | `Δ sum|tw|` della voce `mitosi` | ### **esattamente `−sum|tw|` dei divisi**, scarto `~1e-10` |
>
> ### ⛔ **PERCHE' IL MIO BRACCIO `C` AVEVA VISTO `3π` ESATTO SU TUTTI GLI ARCHI, con la riga:**
> ```
> _r_nodo_mitosi():  r = getattr(self, "_r_corrente", None)
>                    if r is None or len(r) < n: return np.ones(n)   # OROLOGIO UNIFORME
> ```
> Il braccio `C` chiamava `decidi_divisione()` ### **FUORI dal passo**, dopo il 72° — e
> ### **il passo 72 ha partorito**, quindi `n = 12812` mentre `_r_corrente`, scritta da `step`
> **prima** della mitosi, era lunga `12811`. ### **`len(r) < n` ➜ fallback ➜ `grad = 0` ➜
> `soglia = 3π` esatto.**
> ### ⚠ **E `_r_corrente` sta in `REGISTRO_DERIVATE` PROPRIO PERCHE' la sua lunghezza non e' un
> invariante:** ### **il registro me lo diceva, e l'ho ignorato.** Stessa famiglia di `_smp_d0` —
> ### **una grandezza valida SOLO DENTRO il passo** — che il presidio `3-bis` mi aveva fatto
> trovare **il giorno prima.**
>
> ### 🛑 **E LA STORIA DELLA «CAMPANA» NASCEVA DAL `3.79`, CHE ERA UN ARTEFATTO** *(punto 5)*
> La «campana che ammette archi sotto soglia» ### **non esiste**: ### **sotto la soglia locale la
> probabilita' e' ZERO PER COSTRUZIONE** *(`ecc = max(avv/soglia − 1, 0)` clippato, e
> `satura(0) = 0` esatto)*. La `tanh` del `segno` decide ### **CREA contro RESPINGE, sopra la
> soglia** — e nient'altro.
> ### ➜ **La lettura del guardiano era sbagliata quanto il numero su cui l'avevo costruita**, e
> ### **il numero era mio.** ### **La frase giusta e' quella di `db89b37`: la soglia e'
> `3π·(1 − 0.3·tanh(grad))`, e le divisioni avvengono nella PARTE BASSA della banda.**



```
if TORS_4PI and not FASE_2PI:
    twist_max = np.pi          # |chi_i - chi_j| = 2 -> pi*0.5*2 = pi
    soglia0 = PHI_CRIT + twist_max        # = 2pi + pi (emergente), = 3pi
```

| | |
|---|---|
| **classe** | ### **numero DERIVATO su una CONVENZIONE** — e il codice stesso dice che e' *«il punto PIU' INCERTO della cura»* |
| il difetto | ### **`D36`, ACCLARATO PER MISURA (`Z127`)**: la soglia e' in **unita' assolute** di `tw`, ma ### **la scala di `tw` dipende dal DOMINIO di `phi`**. Portando `phi` su `2π`, `\|tw\|` **si dimezza** e la soglia scende di un terzo: ### **gli archi sopra soglia passano da 7047 a ZERO** e la generazione di materia **si ferma** |
| ### **la domanda aperta** | ### **la soglia si puo' scrivere ADIMENSIONALE** — un rapporto a `PHI_CRIT` — cosi' che **non dipenda dalla convenzione**? Senza questo, *«una soglia in unita' assolute di una grandezza la cui scala e' fissata da una convenzione ### non e' una legge fisica: e' una manopola travestita»* |

### ⛔ **② Il `0.3` della modulazione** — `:6761`

```
soglia = soglia0 * (1.0 - 0.3 * np.tanh(grad_modula))
```

| | |
|---|---|
| **classe** | ### **TOPPA, numero NON derivato** *(`A1`)*. Il commento dice *«la soglia scende di al piu' ~30 % dove il gradiente e' forte»* — ### **il `30 %` e' SCELTO** |
| ### ⚠ **e il commento accanto lo sa** | due righe sopra avverte che una modulazione che **satura** *«diventerebbe un RISCALAMENTO COSTANTE della soglia, cioe' un PARAMETRO NASCOSTO (`A1`)»*. ### **La difesa e' scritta; il coefficiente no.** |
| ### **la domanda aperta** | ### **da dove viene il `0.3`?** C'e' una grandezza del sistema da cui **derivarlo**, o la modulazione va **tolta** finche' non c'e'? |

### ⛔ **③ Il figlio nel PUNTO MEDIO** — `:6985`, e lo Schwinger idem

```
pos_figlio = 0.5 * (self.pos[a] + self.pos[b])
```

| | |
|---|---|
| **classe** | ### **TOPPA**, ed e' **`M2` ①** |
| il difetto | il figlio nasce a ### **`d/2` da ciascun genitore**, quindi ### **SOTTO `LAM` se `d < 2·LAM`** — e allora ### **viola `A13`** *(«sotto `LAM` non esiste niente»)*. **`U2`: «la mitosi mette figli SOTTO la scala di Planck»** |
| la cura | ### **esiste e si chiama `MITOSI_2LAM`** *(`CURA 5`, `127cc11`)* — ### **ed e' `False` di DEFAULT** |
| ### **la domanda aperta** | ### **il riordino ACCENDE `MITOSI_2LAM`, o resta una cura separata?** *(E' una **decisione di fisica**: cambia il numero delle nascite.)* |

### ⛔ **④ Le metà portate a `LAM` FABBRICANO lunghezza** — `:7088`, `:7090`

```
dh = self._nasce(dh, 'mitosi', 2, 0)      # [SCALA_MIN] i tronconi d/2 della mitosi
```

| | |
|---|---|
| **classe** | ### **TOPPA costruita su un ASSIOMA**: `LAM` e' `A13`, ma l'**effetto** non e' dichiarato |
| il difetto | ### **`M2` ②**: due archi da `d/2` diventano ### **due archi da `LAM`**, cioe' ### **`2·LAM` al posto di `d`**. *«E' un SECONDO MOTORE del gonfiamento, distinto dal freno di `D31`»* |
| ### **la domanda aperta** | ### **quando `d < 2·LAM`, la divisione si RIFIUTA o si fabbrica lunghezza?** Oggi si fabbrica. ### **Non si possono avere entrambe: `A13` e la conservazione della lunghezza** — e la scelta va **dichiarata** |

### ⛔ **⑤ I due pavimenti della criticità** — `:7000`

```
rho_c = np.maximum(peq_sel, 1e-6) * max(massa_critica_collasso() / max(self.n, 1), 1e-3)
```

| | |
|---|---|
| **classe** | ### **TOPPA, DUE numeri scelti** *(`1e-6`, `1e-3`)* **piu'** una grandezza **globale** dentro una legge **locale** |
| il difetto | **`A11`**: *prima di scrivere un pavimento, cerca l'errore da cui protegge*. E ### **`U1`: `massa_critica_collasso` ha 21 usi DENTRO le leggi** — **`A2`** vieta le medie globali in una legge locale |
| ### **la domanda aperta** | ### **i due pavimenti proteggono da QUALE errore?** E la **massa critica** e' una proprieta' del **sistema** o dell'**arco**? |

### ⛔ **⑥ La RIALLOCAZIONE silenziosa di `_rep`** — `:6881`-`:6884`

```
if len(self._rep) != len(rep):
    self._rep_realloc = ... + 1
    self._rep = np.zeros(len(rep))
```

| | |
|---|---|
| **classe** | ### **TOPPA CONTATA** — `A8` e' rispettato *(c'e' il contatore)*, ma ### **la memoria viene BUTTATA in silenzio** |
| ### ⚠ **e il controllo unico NON la vede** | sta ### **DENTRO `mitosi`**, cioe' nella **sola finestra** che il controllo non puo' guardare *(il limite dichiarato: il controllo guarda **i confini delle voci**, non ogni riga)* |
| ### **la domanda aperta** | ### **dopo il riordino questo ramo puo' ancora scattare?** Se no, va **tolto**; se si', ### **perche' una memoria per arco si perde alla nascita?** |

### ⛔ **⑦ Lo Schwinger prende la lunghezza dal DISEGNO** — `SCHW-CORTI`

| | |
|---|---|
| **classe** | ### **TOPPA**, residuo di **`A3-DISEGNO`** |
| la misura | `dd = 0.5·‖pos_aa − pos_bb‖`: la lunghezza nasce **da `pos`**, non da `d`. ### **MISURATO: al passo 120 il 39.06 % delle coppie ha `2·dd < d`**, cioe' ### **aggiunge una SCORCIATOIA al grafo** *(mediano `1.0131`, minimo `0.6256`; ~48 scorciatoie su ~650 nascite)* |
| ### ⚠ **e la mitosi NO** | per la **divisione** l'arco `(a,b)` e' **SOSTITUITO** da `(a,m)`,`(m,b)` lunghi `d/2`: il cammino e' lungo **quanto prima**. ### **Lo Schwinger non sostituisce: AGGIUNGE** |
| ### **la domanda aperta** | ### **`dd` deve nascere da `d` invece che da `pos`?** *(La voce ha gia' il suo criterio di chiusura, ed e' **sospesa** per priorita'.)* |

### ⛔ **⑧ `MITOSI_DIR` dichiara ATTIVO cio' che e' SPENTO** — `:1516`

| | |
|---|---|
| **classe** | ### **DICHIARAZIONE FALSA** *(non e' una toppa di fisica: e' un commento che mente)* — **`CENS-A4`** |
| il fatto | il commento dice ### **«MITOSI DIREZIONALE ATTIVA»** e il valore e' ### **`0.0`**. Il ramo a `:6975`-`:6981` *(`bias = 0.5·tanh(MITOSI_DIR·(twn[a]−twn[b]))`)* ### **non gira mai** |
| ### **la domanda aperta** | ### **il bias direzionale entra nel riordino, o si ARCHIVIA?** Un ramo che non gira **e un commento che dice il contrario** sono **due** difetti, non uno |

### ⛔ **⑨ `MITMAX`: il tetto alle nascite** — `:6945`, `:1500`

| | |
|---|---|
| **classe** | ### **DICHIARATO, inerte di default** *(`MITMAX = 0`)*, e il commento e' onesto: *«un massimo di falsa fisica falsifica le metriche»* |
| ### **la domanda aperta** | ### **nel riordino il tetto resta un PARAMETRO o diventa un ERRORE**, come `MAX_NODI` *(che dal 2026-09-28 **ferma il run** invece di troncare in silenzio)? |

### ⛔ **⑩ `conc_nodi` e la riparazione che TRONCA** — `:7083`-`:7085`, e `_riallinea_tracking`

| | |
|---|---|
| **classe** | ### **TOPPA DICHIARATA** *(il docstring dice di esistere «senza dover patchare ogni singolo punto che crea nodi/archi»)* — ### **l'esatto opposto del disegno del registro** |
| il fatto | e' l'### **unico posto del sistema dove una cache viene ACCORCIATA di proposito** *(`del self.conc_nodi[self.n:]`)*, e vive in **diagnostica**. ### **Ed e' l'unica grandezza del registro che cresce per MUTAZIONE IN POSTO**, invisibile all'AST e alla sorveglianza |
| ### **la domanda aperta** | ### **il tracking entra nel registro** *(e allora la riparazione si toglie)*, **o resta fuori** *(e allora la troncatura va motivata)*? |

### ⛔ **⑪ `mitosi()` su una rete senza campo** — `FRAG1`

| | |
|---|---|
| **classe** | ### **TOPPA ASSENTE**: non c'e' un rimedio, c'e' un **`IndexError`** |
| il fatto | `I = self._rho_sorgente()` e' **vuoto** e la funzione ### **va in `IndexError` invece di DICHIARARLO** |
| ### **la domanda aperta** | ### **diventa un errore DICHIARATO** *(come `CacheCorta`, `LimiteNodiSuperato`)*, **o la precondizione sale allo schedulatore**? |

### ⛔ **⑫ La rampa del nato** — `REGISTRO_FISICA:A3`

| | |
|---|---|
| **classe** | ### **DICHIARATO, `da-decidere`** |
| il fatto | *«un nodo nato da mitosi parte da `ramp = 0` e arriva a `1` nel suo tempo-luce»* |
| ### **la domanda aperta** | ### **e' una regola di nascita** *(e allora va nel registro)* **o un transitorio** *(e allora va misurato)*? |

### ✅ **E DUE cose che NON sono toppe, e vanno protette dal riordino**

| | |
|---|---|
| ### **`_xi_rumore` non si eredita** | *«`xi` e' l'AMBIENTE, non una proprieta' del nodo»* — ### **e' una REGOLA DI NASCITA** *(«estrazione nuova»)*, **dichiarata**, e la misura dell'ordine l'ha **confermata** |
| ### **la mitosi SOSTITUISCE l'arco** | `(a,b)` → `(a,m)`,`(m,b)`: ### **la mitosi NON accorcia il grafo**, ed e' il ritiro del 2026-09-26 che ### **resta giusto** |

---

## 3. **CHE COSA LA STORIA INSEGNA, e il riordino deve rispettarlo**

| | |
|---|---|
| **1** | ### **Una cura giusta su una cache non chiude la famiglia.** Sette cache, sette cure, tutte corrette — e il difetto tornava, perche' ### **la causa era la mancanza di un posto solo** |
| **2** | ### **Un flag nuovo nasce MORTO se non lo si verifica.** `MITOSI_2LAM` e `--semina-matura` sono stati **inerti** coi loro sigilli che **passavano** |
| **3** | ### **Una patch puo' separare un flag dal suo commento**, e `H-P7` esiste perche' e' **successo** |
| **4** | ### **Un numero scelto si nasconde accanto alla difesa contro i numeri scelti:** il `0.3` sta **due righe sotto** un commento che spiega perche' i parametri nascosti sono vietati |
| ### **5** | ### **La soglia e la scala non si possono cambiare una per volta** *(`D36`)*: il riordino che tocca la decisione ### **tocca per forza anche le unita'** |

---

## 4. 🛑 **I CONFINI: che cosa NON entra nel riordino**

| voce | dove sta nella sequenza |
|---|---|
| **`perc_geom` del nato `= −1`** | ### **DECISA**, commit e sigillo **separati**. Si inserisce ### **DOPO** il riordino della struttura e ### **PRIMA** della potatura: tocca una **regola di nascita**, quindi il registro deve essere gia' l'unico posto che la scrive |
| **`GEOM-SENZA-VERSO`** | **dopo** il riordino. ### **E il suo primo passo e' una DECISIONE DI LUCA** *(la trasformazione di specchio)*, non mia |
| **`P-EQ-MEDIANA-ARCHI`** | **dopo** il riordino: e' in `step`, non nella nascita |
| **`POTATURA-GUARDIE`** | ### **dopo** il riordino **per decisione di Luca**, perche' il riordino **tocchera' molte di quelle 57 righe** |

### ⚠ **E DUE confini che NON tengono, e lo dico invece di assorbirli**

| | |
|---|---|
| ### **`M2` / `U2` / `MITOSI_2LAM`** | ### **NON si possono separare dalla STRUTTURA.** La parte **(b)** del piano deve dire come nascono `pos`, `d`, `d0` — e ### **`pos_figlio` nel punto medio E la fabbricazione di lunghezza SONO quella parte.** Non e' una voce accanto al riordino: **e' il riordino.** ➜ **Decide Luca se accendere `MITOSI_2LAM` dentro o tenerlo fuori, ma la DOMANDA sta dentro** |
| ### **`D36` / la soglia `3π`** | ### **NON si separa dalla DECISIONE.** La parte **(a)** chiede *«la soglia e cosa legge»*: ### **la soglia E' `D36`**, ed e' **acclarata per misura**. ➜ **Il piano puo' lasciare la soglia INVARIATA e dichiararlo** *(byte-identico)*, ### **ma non puo' descrivere la decisione senza nominarla** |

---

## 5. **La CODA, nello stato di oggi**

| voce | stato |
|---|---|
| `RIPIEGHI-ZERO` | ### **CHIUSA** *(`98810aa`)*, generalizzazioni **1-2-3 sigillate** |
| `POTATURA-GUARDIE` · `P-EQ-MEDIANA-ARCHI` · `GEOM-SENZA-VERSO` · `perc_geom` del nato | **in coda**, nell'ordine del par.4 |
| generalizzazione **4** *(derivate sporche)* e **3-bis** *(registro dichiarato)* | ### **DENTRO il piano** del riordino |
| generalizzazione **5** *(matrice di configurazioni)* | **in coda con `T5`** |
| ### ✅ **`RELAZIONE_PER_CLAUDE.md` tiene piu' giorni — CHIUSA il 2026-10-02** | ~~**violazione in corso** del par.4, dichiarata: l'ultimo giorno chiuso in `doc/relazioni/` e' il **2026-09-25**. **E' la voce piu' vecchia della coda**~~ ### ✅ **ARCHIVIATA il 2026-10-02** *(`871101d`)*: cinque giorni staccati *(`2026-09-26` 2214 · `09-27` 2787 · `09-28` 1707 · `09-29` 1122 · `10-01` 1519 righe)*, file vivo da ### **9407 a 61 righe**, e la conservazione delle righe ### **9408 = 9408** piu' una verifica INDIPENDENTE sul multiset delle righe |
