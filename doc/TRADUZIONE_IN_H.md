# LA TRADUZIONE DELLE LEGGI DEL SIMULATORE IN TERMINI DI `H`

> ### ⛔ **QUESTO DOCUMENTO NON CAMBIA NIENTE NEL SIMULATORE** *(resta `b8c21049`)*, e ### **non decide la forma di `H`:** ### **propone**, e marca ogni proposta ### **candidata** o ### **aperta**. ### **La forma di `H` e la regola di crescita sono DECISIONI DI LUCA.**
>
> *I numeri escono da quattro uscite, e nessuno e' ricopiato a mano* *(`L-NUMERI`)*: `_censimento_leggi` · `_prova_integrabilita` · `_crescita_conti` · `proto_primo_ordine/uscite/diagnosi_v2`. Criteri e previsioni: `doc/TASK_HISTORY/2026-10-08_traduzione-in-H.md`, committato ### **prima** *(`c6c1112`, col criterio del «no» in `2f47b75`)*.

# 📌 `⓿` **LA CONFIGURAZIONE DELLE MISURE** *(`P5`: non i flag toccati, TUTTI)*

### ⛔ **Questo documento non fa girare niente: riporta le misure di tre strumenti**, e la configurazione e' ### **quella che LORO hanno dichiarato**, non una che io ridico:

| | |
|---|---|
| booleani di modulo confrontati con l'argv ### **del DRIVER** | ### **`82`** |
| l'esito | ### **nessuna differenza. ZERO su 82.** |
| la scena | `12802` nodi, `471564` archi, `DT = 0.01`, snapshot di `3` passi ### **pieni** *(`_passo.passo_pieno`, non `net.step()`)* |
| dove sta la dichiarazione per intero | `csv/_test_fork/_prova_integrabilita/integrabilita.txt` e `csv/_test_fork/_crescita_conti/crescita.txt` |

> ### ⚠ **E IL GENERATORE DI QUESTO DOCUMENTO E' ESENTE DA `H-P5`, dichiarato:** non importa il simulatore. ### **Chiamare `dichiara_configurazione` qui vorrebbe dire caricare il simulatore in un generatore di testo, e la dichiarazione sarebbe di un modulo appena importato — NON della scena che ha misurato.** L'esenzione e' in `doc/ESENZIONI_presidi.md`.

---

# ⭐ `①` **IL METODO -- e perche' il «NO» ADESSO SI DIMOSTRA**

Il metodo ovvio *(scrivere `E` e verificare `F = −∂E/∂x`)* ### **dimostra il sì ma non il no:** non trovare `E` prova solo che ### **non l'ho trovata**. Il rilievo e' di Luca, e ha prodotto un banco che decide ### **senza indovinare `E`**:

| | il test | che cosa decide |
|---|---|---|
| ### **`(A)`** | la legge ### **legge** la variabile che scrive? | ### ⛔ **se NO, non e' il gradiente di nessuna `E(x)`**: lo spazio d'ingresso non e' quello d'uscita. ### **E il `(B)` va SALTATO**, perche' darebbe `J = 0`, che e' simmetrica — ### **un FALSO-ZERO** |
| ### **`(B)`** | `\|\|J − Jᵀ\|\| / \|\|J\|\|` contro il ### **pavimento CALCOLATO** | ### **simmetrica ⇒ `E` ESISTE** *(localmente, in quelle variabili)*; ### **asimmetrica ⇒ un «no» DIMOSTRATO** |

### ✔ **E IL BANCO E' SANO -- tre controlli, e il terzo e' quello che conta:**

| controllo | numero | esito |
|---|--:|---|
| la coppia ### **SCALARE** *(gradiente noto)* deve essere ### **simmetrica** | `5.178e-12` contro un pavimento di `4.936e-09` | ### ✔ **PASSA** |
| la coppia del ### **DRIVER** deve risultare ### **non traducibile** | `0.000e+00` perturbando `φ` | ### ✔ **PASSA** *(per il `(A)`)* |
| ### ⭐ una coppia ### **SINTETICA** col prefattore di nodo deve risultare ### **asimmetrica** | `1.463e-02` | ### ✔ **PASSA** |

> ### ⭐ **IL TERZO CONTROLLO E' QUELLO CHE VALE, e non era nel mandato:** ### **un banco che approva tutto e un banco che funziona danno lo STESSO referto sul controllo positivo.** Serviva una legge che ### **DEVE** risultare asimmetrica, e l'ho costruita: ### **non e' una legge del simulatore**, e sta dichiarata come controllo.

### ⚠ **E TRE LIMITI, dichiarati PRIMA di usare il banco:**

| | |
|---|---|
| il «sì» e' ### **LOCALE** | e' la condizione di ### **Poincaré**: `J` simmetrica ⇒ la forma e' chiusa ⇒ `E` esiste ### **in un intorno dello stato misurato**, non globalmente |
| il «sì» e' ### **SUL CAMPIONE** | `40` nodi *(`3` di base col loro vicinato)*. ### ⚠ **Un «asimmetrica» invece e' un no SUL TUTTO**, perche' una `J` simmetrica ha ### **tutte** le sottomatrici principali simmetriche |
| vale ### **nelle variabili scelte** | una legge asimmetrica in `φ` puo' essere il gradiente di qualcosa ### **in variabili diverse** — ed e' il caso della coppia del driver, che la forma `U(2)` riscrive in `ψ`. ### **La tavola lo dice invece di nasconderlo** |

# ⭐ `②` **IL CENSIMENTO -- e il difetto che ha preso DI SE STESSO**

| | |
|---|--:|
| scritture di stato trovate, ### **per FORMA** | ### **`419`** su `339` nomi |
| funzioni raggiunte dalle ### **`10` radici dichiarate** | `68` |
| flag cambiati dall'argv ### **DEL DRIVER** | `32` |

> ### ⛔ **IL MANDATO DICEVA «`step()` E LE FUNZIONI CHE CHIAMA», E NON BASTA:** il grafo chiuso dal ### **solo `step`** raggiunge `44` funzioni e ### **NON contiene `mitosi`, Schwinger, `scuoti_vuoto` ne' la memoria hebbiana** — quelle le chiama ### **il DRIVER**. ### ➜ **Con la sola radice `step` avrei perso TUTTA la classe CRESCITA**, cioe' esattamente la classe su cui il mandato chiede il conto.

> ### ⚠ **E CIO' CHE IL METODO NON VEDE, dichiarato:** le scritture per ### **mutazione** *(un `dict` aggiornato dentro una funzione a cui l'oggetto e' passato)* — e' il falso positivo gia' preso su `conc_nodi`. ### **Per quelle il censimento e' per DIFETTO.**

# ⛔ `③` **LA TAVOLA -- legge per legge, con la classe e il perche'**

### ⚠ **LA CLASSIFICAZIONE E' UN GIUDIZIO MIO, e lo dichiaro:** i numeri che la sostengono vengono dalle uscite, il giudizio no.

| la legge | ancora *(nome, MAI una riga)* | variabile | ### **classe** |
|---|---|---|---|
| la coppia d'interferenza, ramo SCALARE | `_coppia_interferenza (ramo OFF)` | `phi` | ### **TRADUCIBILE** |
| il legame elastico delle lunghezze | `step, blocco di `vd` (VERLET)` | `d` | ### **TRADUCIBILE** |
| la repulsione | `REPULS_LEGGE, `_rep`` | `d` | ### **TRADUCIBILE** |
| il rilassamento della torsione | `step, blocco `tau_tw`` | `tw` | ### **CON UNA MEMORIA** |
| il rilassamento della lunghezza di riposo | `step, `tau_p_loc`` | `d0` | ### **CON UNA MEMORIA** |
| il rilassamento della pressione di equilibrio | `step, `tau_bg_loc`, TAU_DIFF` | `peq` | ### **CON UNA MEMORIA** |
| la precessione dello spinore e l'orologio | `_passo_spinoriale, `omega_s`` | `omega_s` | ### **CON UNA MEMORIA** |
| la memoria hebbiana del moto | `memoria_hebbiana_moto, `mem_mot`` | `mem_mot` | ### **CON UNA MEMORIA** |
| la dinamica dei pesi e delle distanze | ``w`, `d`, `d0` nello step` | `w, d, d0` | ### **CON UNA MEMORIA** |
| la mitosi | `mitosi, decidi_divisione` | `tutta la struttura` | ### **CRESCITA DELLO SPAZIO** |
| la creazione di coppia (Schwinger) | `mitosi, evento `schwinger`` | `tutta la struttura` | ### **CRESCITA DELLO SPAZIO** |
| la creazione degli archi | `_allaccia` | `i, j, d, d0, peq, tw, vd` | ### **CRESCITA DELLO SPAZIO** |
| la scomparsa degli archi | `le potature nello step` | `i, j` | ### **CRESCITA DELLO SPAZIO -- ma A ROVESCIO** |
| la sincronizzazione | `K_SYNC` | `phi` | ### **NON TRADUCIBILE -- DIMOSTRATO** |
| la coppia d'interferenza del DRIVER | `_coppia_interferenza (CAMPO_SPINORIALE)` | `phi` | ### **NON TRADUCIBILE IN phi -- DIMOSTRATO** |
| il termostato | `xi_termo, REGIME` | `phivel` | ### **NON TRADUCIBILE** |
| lo scuotimento del vuoto | `scuoti_vuoto` | `phivel` | ### **NON TRADUCIBILE** |
| il freno `_smorza` | `_smorza (D31)` | `d0` | ### **NON TRADUCIBILE -- FRECCIA** |
| lo smorzamento anisotropo | `ZETA_VIR, `beta*vd`` | `vd` | ### **NON TRADUCIBILE -- DISSIPAZIONE** |
| la massa critica | `massa_critica_adattiva, massa_critica_collasso` | `la soglia` | ### **NON TRADUCIBILE -- e' una SOGLIA** |
| i contatori `_g_*`, `_taup_*`, `_sfb_*` | `i prefissi diagnostici` | `-` | ### **DIAGNOSTICA** |

### **IL CONTO PER CLASSE** *(e `9-ter` chiede che si CONTI)*:

| classe | quante | previsto | scarto |
|---|--:|--:|--:|
| ### **TRADUCIBILE** | ### **3** | `7` *(`PT-2`)* | ### **-4** |
| ### **TRADUCIBILE CON UNA MEMORIA** | ### **6** | `6` *(`PT-3`)* | ### **=** |
| ### **CRESCITA DELLO SPAZIO** | ### **4** | `4` *(`PT-4`)* | ### **=** |
| ### **NON TRADUCIBILE** | ### **7** | `5` *(`PT-5`)* | ### **+2** |
| ### **DIAGNOSTICA** | ### **1** | `3` *(`PT-6`)* | ### **-2** |
| ### **IN TUTTO** | ### **21** | `24`..`32` *(`PT-1`)* | ### **SOTTO IL MINIMO** |

> ### ⛔ **`PT-1` E' MANCATA, E DAL BASSO: `21` contro un minimo di `24`.** Il motivo non e' che le leggi sono meno: e' che ### **le ho RAGGRUPPATE piu' grosso di quanto avessi previsto.** Il censimento trova `419` ### **scritture**; la tavola ha `21` ### **righe**, perche' *«il rilassamento di `d0`»* e' una riga e ### **dieci** scritture. ### ➜ **La previsione contava una cosa e la tavola conta un'altra, e la differenza e' MIA, non del sistema.** ### **Lo scrivo invece di spezzare le righe fino a far quadrare il numero.**

> ### ⭐ **`PT-9` LA VINCE, E DI PIU' DI QUANTO AVESSI SCRITTO:** dicevo che il test avrebbe spostato ### **almeno `2`** leggi fuori da TRADUCIBILE. ### ➜ **Ne ha spostate `4`**, e `TRADUCIBILE` passa da `7` previste a ### **`3`**. ### **Le quattro:** la ### **sincronizzazione** *(dimostrata non integrabile)*, la ### **coppia del driver** *(non legge `φ`)*, il ### **freno `_smorza`** *(a senso unico, instradata dal punto `(3)`)* e la ### **massa critica** *(non e' una forza: e' un criterio)*.

> ### ⚠ **E `DIAGNOSTICA` E' `1` RIGA, NON `3`, e non e' un errore di conto:** la riga copre ### **`231` nomi** riconosciuti per forma. ### **`PT-6` contava le LEGGI, la tavola conta le RIGHE**, e le due cose non sono la stessa — lo dico invece di far quadrare il numero.

### ⛔ **E IL CENSIMENTO PUO' AVER PERSO LEGGI: DUE BUCHI SONO CONFERMATI, NON IPOTETICI**

*(Punto `3` della correzione di Luca. ### **Non lo rifaccio adesso: lo scrivo come LIMITE**, coi numeri che il censimento stesso stampa.)*

| il buco | ### **confermato?** | il controllo che lo escluderebbe |
|---|---|---|
| ### **RADICI MANCANTI** | ### ⚠ **non escluso.** Le radici sono `10`, e le ho ### **scelte io**: una legge che ### **solo il driver** chiama e che non sia fra quelle `10` e' ### **invisibile** | chiudere il grafo ### **dal TESTO DEL DRIVER** invece che da una lista mia: radici = ### **tutto cio' che il driver chiama**, letto dall'AST del driver. ### **E' fattibile, e non l'ho fatto** |
| ### ⛔ **SCRITTURE PER MUTAZIONE** | ### ⛔ **CONFERMATO, e dal censimento stesso:** `conc_nodi` e' fra le ### **`7`** variabili *«censite ma MAI scritte dalle radici»* — ma `conc_nodi` ### **viene scritta**, per mutazione in `_agg_voce`. ### **Il buco non e' un'ipotesi: ha un nome** | un controllo ### **A RUNTIME**, non dall'AST: fotografare ### **tutti** gli attributi di stato prima e dopo ogni legge e pretendere che ### **ogni differenza sia attribuita a una scrittura censita**. ### **Nessun metodo statico lo puo' fare** |
| ### ⛔ **`setattr` CON NOME CALCOLATO** | ### ⛔ **CONFERMATO: `5` scritture** hanno come bersaglio `<calcolato>` — il censimento ### **le VEDE ma non sa QUALE variabile toccano** *(`_avvelena_derivate`, `_nasce`, `_riallinea_derivate`, `_smorza`)* | lo stesso controllo a runtime: ### **e' il solo che leghi una scrittura al suo bersaglio** quando il nome e' una stringa calcolata |
| ### **ALIAS LOCALI** | ### **non escluso, e non ha un nome:** `v = self.phi; v[...] = ...` sfugge al criterio `self.X`, e l'AST ### **non lo segue** | ### **o il controllo a runtime, o un'analisi di ALIAS** — che e' molto piu' di una visita dell'albero |

> ### ⚠ **E LE ALTRE `6` <<censite ma mai scritte>> NON sono buchi, e la differenza conta:** `dt_e` `dt_n` `tau` `lambda_nodi` `_tempo_luce_nodo` `_fattore_tempo_arco` sono ### **DERIVATE** — ricalcolate ogni passo dalla loro legge, e per questo il censimento le vede come non scritte dalle radici. ### **`conc_nodi` e' l'unica delle `7` che sia davvero un buco**, e l'ho distinta invece di contarle tutte come difetti.

> ### ⛔ **MA LA CAUSA PRINCIPALE DI `21` CONTRO `24..32` NON E' NESSUNO DI QUESTI BUCHI: SONO IO.** Il censimento trova ### **`419` SCRITTURE**; la tavola ha ### **`21` RIGHE**, perche' *«il rilassamento di `d0`»* e' ### **una** riga e ### **dieci** scritture. ### ➜ **Il raggruppamento e' MIO, e i buchi -- se contano -- contano SOPRA questo.**

> ### 📌 **E UNA FORMA CHE HO CERCATO E CHE NON HA TROVATO NIENTE, perche' si sappia:** `np.add.at(self.X, ...)` -- ### **`0` occorrenze** nelle `68` funzioni raggiunte. ### **Non aggiunge e non toglie: lo dico perche' un criterio che non scatta MAI non e' una garanzia, e' solo un criterio che non scatta.**

### ⛔ **E IL TERMINE DI ENERGIA, O IL MOTIVO PER CUI NON C'E', UNA PER UNA:**

| la legge | ### **`E_x` o il vincolo** | esito della verifica |
|---|---|---|
| ### **la coppia d'interferenza, ramo SCALARE** | E = -K_C * somma_archi A_ij cos(phi_i - phi_j);  i dpsi/dt = dE/dpsi* | SIMMETRICA al banco, e il gradiente coincide a 1.49e-15 (D2-BIS) |
| ### **il legame elastico delle lunghezze** | E = (1/2) somma_archi k_ij (d_ij - d0_ij)^2, con d0 CONGELATA nel termine | NON MISURATA in questo giro: la forza non e' isolabile senza riscrivere il passo |
| ### **la repulsione** | E = somma_archi V_rep(d_ij), con V_rep decrescente;  la forza e' -dV/dd | NON MISURATA: `_rep` INSEGUE un bersaglio, quindi il termine vale a `_rep` FERMA |
| ### **il rilassamento della torsione** | ### NESSUN E_x, e la versione precedente di questo documento SBAGLIAVA: scrivere <<il rilassamento e' la discesa di E_tw>> dichiara un FLUSSO DI GRADIENTE, che DISSIPA. Serve un CONIUGATO -- candidato: tw come FASE DI UN LEGAME U(1), col suo campo elettrico d'arco | la legge dipende da una VELOCITA' (\|Delta omega\|): instradata dal punto (3) |
| ### **il rilassamento della lunghezza di riposo** | ### NESSUN E_x: `d0 += dt*(d - d0)/tau_p` e' un FLUSSO DI GRADIENTE, cioe' dissipazione. Serve un CONIUGATO -- candidato: un impulso proprio `p_d0`, e allora `d0` OSCILLA attorno a `d` invece di raggiungerla | 10 scritture da 4 funzioni: NON e' una legge sola, e il test va fatto sul SISTEMA |
| ### **il rilassamento della pressione di equilibrio** | ### NESSUN E_x: l'inseguimento e la DIFFUSIONE sono entrambi flussi di gradiente. Il laplaciano e' simmetrico, ma la DIFFUSIONE DISSIPA. Serve un CONIUGATO -- candidato: un impulso `p_peq`, e allora la diffusione diventa un'ONDA | la diffusione usa TAU_DIFF = 1.0 NUDO: una MANOPOLA, e A1 la vieta |
| ### **la precessione dello spinore e l'orologio** | ### ⭐ L'UNICA CHE HA GIA' UN CONIUGATO: `omega_s` E' una velocita' angolare, quindi e' il MOMENTO coniugato della fase dell'orologio, e `E_om = (1/2) somma I_k omega_s^2` con `I = (d/cs)^2` e' ENERGIA CINETICA VERA. ### **Non le serve un coniugato: le va TOLTO lo smorzamento `-omega_src/tau`** | il tau e' DERIVATO (`--tau-luce`, esempio di A15.2) -- ma e' il tau di un OBLIO, non una frequenza |
| ### **la memoria hebbiana del moto** | nessun E_x scritto: la legge e' una MEDIA MOBILE, e una media mobile NON e' una discesa -- VINCE L'ULTIMO invece di bilanciare | A14 n.4 + MEM-HEBB-VERSO: la forma va CAMBIATA, non tradotta |
| ### **la dinamica dei pesi e delle distanze** | e' il punto A16.3: w e U devono essere gradi di liberta' DENTRO H. Nel prototipo sono FISSI, ed e' una violazione DICHIARATA | APERTO: la forma del termine di memoria d'arco NON e' scritta |
| ### **la mitosi** | NON e' un termine di H: e' l'unica legge che CAMBIA H. Vincoli: (1) Sigma rho conservata; (2) il Delta H pagato dal vuoto LOCALE | la tavola delle regole NON ha una classe <<il genitore cede>>: Sigma rho CRESCE |
| ### **la creazione di coppia (Schwinger)** | come sopra, piu' il vincolo di CARICA: l'antinodo nasce a fase opposta, e quello si conserva | e' il ramo che conserva N(+1) - N(-1): la carica nasce OPPOSTA |
| ### **la creazione degli archi** | un arco nuovo e' un termine NUOVO in H: il suo contributo va pagato | `peq` nasce `nan` e lo step la CALIBRA: una nascita con un marcatore, non con un valore |
| ### **la scomparsa degli archi** | NON c'e' forma: A14.2 dice che la CRESCITA e' l'unica freccia ammessa, quindi un arco che muore e' GIA' una violazione | e' un difetto, non una legge da tradurre: va nell'elenco di Luca |
| ### **la sincronizzazione** | NESSUNA. Il banco misura un'asimmetria di `1.0641` contro un pavimento di `1.438e-10` | un <<no>> DIMOSTRATO: nove ordini sopra il pavimento, identico ai tre passi h. ### ⭐ E LUCA HA DECISO: SI TOGLIE, perche' DEVE EMERGERE (decisione `3`, PRESA, e la scheda e' in `doc/REGISTRO_FISICA.md`) |
| ### **la coppia d'interferenza del DRIVER** | NESSUNA in phi: la legge NON LEGGE phi (0.000e+00). La forma U(2) la riscrive in psi, ma a 1.054 di scarto, cioe' il 105 % -- per il criterio del <<no>> NON e' una traduzione, e' UNA LEGGE NUOVA | test (A): spazio d'ingresso (lo spinore) diverso dallo spazio d'uscita (phi) |
| ### **il termostato** | NESSUNA: scrive `phivel` DALL'ESTERNO, ed e' GLOBALE (A2). Deve diventare scambio col vuoto LOCALE (A15.3) | A14 n.1. E il numero: senza bagno le nascite crollano da 164 a 0 |
| ### **lo scuotimento del vuoto** | NESSUNA: e' un forzante stocastico. Deve diventare scambio col vuoto LOCALE (A15.3) | A14 n.1, insieme al termostato |
| ### **il freno `_smorza`** | NESSUNA: e' un `clip` DA UN LATO, quindi a senso unico | instradata dal punto (3) del criterio del <<no>>: il test NON si fa, darebbe un FALSO-ZERO |
| ### **lo smorzamento anisotropo** | NESSUNA: dissipa. Deve diventare scambio col vuoto LOCALE (A15.3) | A14 n.2, gia' dichiarato |
| ### **la massa critica** | non e' una forza: e' un CRITERIO. In H non entra; entra nella REGOLA DI CRESCITA | U1 dice che `massacriticacollasso` ha 21 usi DENTRO le leggi: voce BLOCCANTE |
| ### **i contatori `_g_*`, `_taup_*`, `_sfb_*`** | nessuna: non muovono lo stato | `231` nomi riconosciuti per FORMA. ⚠ IL CRITERIO E' DI FORMA: ogni nome va verificato col <<nessun lettore>>, e questo giro NON lo fa |

# ⛔ `④` **I DUE «NO» DIMOSTRATI -- e si riconciliano con misure di prima**

| | il numero | la lettura |
|---|--:|---|
| ### **la SINCRONIZZAZIONE** | asimmetria ### **`1.0641`** contro un pavimento di `1.438e-10` | ### ⛔ **nove ordini sopra**, e ### **identica ai tre passi `h`** — non e' un artefatto. ### **Nessuna `E(φ)` esiste di cui `K_SYNC` sia il gradiente** |
| ### **la COPPIA DEL DRIVER** | `0.000e+00` | ### ⛔ **non legge `φ` AFFATTO**: scrive una coppia su `φ` leggendo ### **lo spinore**. Spazio d'ingresso ≠ spazio d'uscita |

> ### ⭐ **E LA SINCRONIZZAZIONE SI RICONCILIA CON `D2-TER`:** là la sync toglieva il ### **`93.44 %`** della crescita di `H` a `A` fissa ### **senza costare coerenza** *(`AUC400` `0.9394` → `0.9333`)*, e l'avevo scritto *«pompava senza ordinare»*. ### ➜ **È esattamente il comportamento di una forza NON CONSERVATIVA.** Quella misura era ### **il sintomo**; questa e' ### **la causa**, e le due non si scelgono: si spiegano a vicenda.

> ### ⛔ **E LA FORMA `U(2)` NON SALVA LA COPPIA DEL DRIVER:** sta a ### **`1.054`** di scarto, cioe' il ### **`105 %`**, ### **dieci volte sopra** la soglia del `10 %` che il criterio del «no» fissa. ### ➜ **Non e' una traduzione: e' UNA LEGGE NUOVA**, e va ### **nell'elenco delle decisioni di Luca**, non nella `H` candidata. ### ⚠ **Senza quella soglia l'avrei messa in `H`**, chiamando «traduzione» un cambio di fisica del `105 %`.

# ⭐ `⑤` **I TERMINI CANDIDATI, E QUALI SONO GIA' HAMILTONIANI**

> ### ⛔ **CORREZIONE, e il rilievo e' di Luca: la versione precedente di questa sezione scriveva le MEMORIE COME DISSIPAZIONE, e le chiamava «termini di `H`».** Scrivere `(1/2)tw²/τ` con *«il rilassamento e' la discesa di `E`»* descrive un ### **FLUSSO DI GRADIENTE**:

```
flusso di gradiente:   x' = -dE/dx     =>   dE/dt = -|dE/dx|^2  <=  0
dinamica hamiltoniana: x' = +dH/dp,  p' = -dH/dx   =>   dH/dt = 0
```

### ➜ **Il primo DECRESCE SEMPRE: e' dissipazione, ed e' la forma «insegue e dimentica» che `A16.3` NON ammette come legge.** In una `H` un grado lento ### **non scende: ha un CONIUGATO** *(un impulso, o la fase di una variabile d'arco)* e ### **scambia energia in modo reversibile**. ### ⛔ **E l'oblio non si scrive: deve EMERGERE dallo scambio col vuoto** *(`A15.3`)*.

## `⑤.1` ### ✔ **GIA' HAMILTONIANO** — *genera dinamica, non discesa*

```
H_fase  =  - K_C * somma_archi A_ij cos(phi_i - phi_j)
```

| | |
|---|---|
| ### **il coniugato c'e' GIA'** | con `i dψ/dt = ∂H/∂ψ*`, la coppia coniugata e' ### **`(φ, ρ)`**: la fase e la densita'. ### **Non serve aggiungere niente** |
| ### **e il banco lo conferma** | asimmetria ### **`5.178e-12`** contro un pavimento di `4.936e-09`: ### **simmetrica**, cioe' una `E` esiste — e qui ### **e' anche scritta** |

> ### ⭐ **E UNA DISTINZIONE CHE SERVE, perche' senza di essa il `⑤.3` sembra una contraddizione:** la ### **STESSA** `E = −K_C Σ A cos(φ_i − φ_j)` da' ### **due leggi diverse**, e ### **una conserva e l'altra dissipa.**

```
Kuramoto  (gradiente):   phi'_i = -dE/dphi_i        ->  dE/dt <= 0   DISSIPA
primo ordine (A16):      i dpsi/dt = dH/dpsi*       ->  dH/dt  = 0   CONSERVA
                         cioe'  phi'_k = +dH/drho_k ,  rho'_k = -dH/dphi_k
```

### ➜ **Non conta QUALE energia: conta A QUALE EQUAZIONE la si dia.** La coppia scalare e' hamiltoniana perche' `φ` e `ρ` sono ### **coniugati**; lo stesso `E` messo in una discesa ### **dissipa**. ### ⛔ **Per questo «scrivere la `E` della sincronizzazione» non l'avrebbe salvata** — e' il motivo `(ii)` della decisione `3`.

## `⑤.2` ### ⚠ **POTENZIALI VERI, CHE ASPETTANO IL CONIUGATO DELLA GEOMETRIA**

```
V_geom  =  (1/2) somma_archi k_ij (d_ij - d0_ij)^2        <- il legame elastico
         + somma_archi V_rep(d_ij)                        <- la repulsione
```

### ⭐ **Questi sono `V(d)` per davvero** — funzioni della sola configurazione, non inseguimenti. ### ⛔ **Ma `d` non ha un impulso DENTRO `H`:** oggi si muove con `vd` *(Verlet)*, e l'energia cinetica delle lunghezze ### **non e' in `H`**. ### ➜ **E' la DECISIONE `9`.**

## `⑤.3` ### ⛔ **FLUSSI DI GRADIENTE — «memorie da riscrivere col loro coniugato», NON termini di `H`**

```
OGGI (dissipativo):            tw'  = -tw/tau_tw
                               d0'  = +(d - d0)/tau_p
                               peq' = +(rho - peq)/tau_bg + laplaciano(peq)/TAU_DIFF
```

### ⛔ **Nessuno dei tre e' un termine di `H`: sono TRE LEGGI DI DISSIPAZIONE**, e finche' restano in questa forma ### **non entrano nella `H` candidata.**

### 📌 **I CONIUGATI, PROPOSTI COME CANDIDATI E NON COME DECISIONE:**

| memoria | ### **il coniugato candidato** | la forma | ### **che cosa diventa `τ`** |
|---|---|---|---|
| ### **`tw`** *(d'arco)* | ### ⭐ **`tw` come FASE DI UN LEGAME `U(1)`**, col suo ### **campo elettrico d'arco** `E_ij` come momento coniugato | `H_tw = (1/2)Σ_archi E_ij² − K_B Σ_placchette cos(Σ_arco tw)` — ### **energia elettrica + energia di PLACCHETTA** | ### **una FREQUENZA:** `ω_tw = |Δω_locale|` al posto di `τ_tw = 2π/|Δω|`. ### **Lo stesso numero, letto al contrario:** oggi e' un tempo di OBLIO, lì e' il ritmo di un'OSCILLAZIONE |
| ### **`d0`** *(d'arco)* | un ### **impulso proprio** `p_d0`, con una massa d'arco | `H_d0 = Σ p_d0²/(2 m_arco) + (1/2)Σ k(d − d0)²` | ### **una frequenza:** `ω = sqrt(k/m_arco)`, e `d0` ### **OSCILLA attorno a `d`** invece di raggiungerla |
| ### **`peq`** *(di nodo)* | un ### **impulso proprio** `p_peq` | `H_peq = Σ p_peq²/(2 m_p) + (1/2)Σ(ρ − peq)²/χ + (1/2)Σ_archi(peq_i − peq_j)²/χ_d` | ### **una VELOCITA':** la diffusione diventa un'### **ONDA**, e `TAU_DIFF` diventa `c_p² = 1/(m_p·χ_d)` — ### **una velocita' del suono, non un tempo di oblio** |
| ### ⭐ **`omega_s`** *(di nodo)* | ### **NESSUNO: ce l'ha GIA'** | `omega_s` ### **E' una velocita' angolare**, cioe' il momento coniugato della fase dell'orologio, e `(1/2)Σ I_k omega_s²` con `I = (d/cs)²` e' ### **energia cinetica VERA** | ### **niente `τ`:** le va ### **TOLTO** lo smorzamento `−omega_src/τ`, non dato un coniugato |

> ### ⭐ **LA COSA CHE QUESTA CORREZIONE FA EMERGERE, e non e' un dettaglio:** il coniugato naturale di `tw` ### **E' L'ELETTROMAGNETISMO.** `tw` e' un angolo ### **per arco**; un angolo per arco col suo momento coniugato e un termine di placchetta ### **E' una teoria di gauge `U(1)` sul reticolo** — `tw` diventa il ### **potenziale vettore**, il suo coniugato il ### **campo elettrico**, la placchetta il ### **campo magnetico**. ### ➜ **E' esattamente la direzione del principio guida** *(«dallo spinore discende l'interazione con la luce»)*, e ci si arriva ### **dall'obbligo di dare un coniugato a una memoria**, non per innesto.
> ### ⛔ **Resta un'IPOTESI da dimostrare, e la marco tale:** che quella sia LA forma non e' misurato.

## `⑤.4` ### ⛔ **E L'OBLIO, ADESSO, NON HA PIU' CASA**

### **Con i coniugati, `tw`, `d0` e `peq` OSCILLANO: non dimenticano piu'.** ### ➜ **Quindi l'oblio deve venire da FUORI, cioe' dallo scambio col vuoto** *(`A15.3`)* — ### **ed e' lo STESSO posto da cui deve venire l'energia della nascita** *(`S5`, `⑦`)*. ### ⚠ **Non e' una coincidenza: sono la stessa decisione aperta, vista da due lati.**

## `⑤.5` ### ⛔ **CHE COSA NON C'E', E SI VEDE**

| | ### **che cosa NON c'e', e si vede** |
|---|---|
| ### ⛔ **la sincronizzazione** | ### **NON c'e', ed e' dimostrato** che non possa esserci |
| ### ⛔ **la coppia del driver** | ### **NON c'e'**: la `H` candidata ha la coppia ### **SCALARE**. ### **Questa è la prima decisione di Luca** |
| ### ⛔ **termostato e scuotimento** | ### **NON ci sono**: vanno diventati scambio col ### **vuoto LOCALE** *(`A15.3`)*, e quella forma ### **non e' scritta** |
| ### ⛔ **la memoria hebbiana** | ### **NON c'e'**: una ### **media mobile non e' una discesa** *(vince l'ultimo)*. La forma va ### **cambiata**, non tradotta |
| ### ⚠ **`TAU_DIFF = 1.0`** | e' una ### **MANOPOLA NUDA** dentro un termine candidato: ### **`A1` la vieta**, e finche' resta tale quel termine ### **non e' ammissibile** |
| ### ⚠ **`w` e `U` dinamici** | ### **`A16.3`**: devono essere gradi di liberta' DENTRO `H`. ### **La forma del termine di memoria d'arco NON e' scritta** — e per `A16.3` vale lo stesso vincolo del `⑤.3`: ### **servono CONIUGATI, non rilassamenti** |
| ### ⛔ **l'ENERGIA CINETICA delle lunghezze** | ### **NON c'e'**, e la geometria ### **si muove comunque** *(Verlet, `vd`)*: ### **e' la DECISIONE `9`** |

# ⭐ `⑥` **LA REGOLA DI CRESCITA -- a parte, perche' NON e' un termine di `H`**

## `⑥.1` **LA FORMA DELLA REGOLA**

> ### ⭐ **E' l'unica legge che CAMBIA `H`**, quindi non puo' starci dentro. ### **Si scrive accanto.**

```
QUANDO:  una grandezza della materia supera una soglia che e' UNA LEGGE, non un numero
         (A1, A15.2) -- oggi la soglia e' massa_critica_adattiva, e U1 dice che
         `massacriticacollasso` ha 21 usi DENTRO le leggi: voce BLOCCANTE
COME:    psi_p -> psi_p / sqrt(2)   sul genitore E sul nato, stessa fase, stessa
         direzione di Bloch                                     [CANDIDATA, S4]
CHI PAGA: il Delta H va ceduto o ricevuto dal VUOTO LOCALE      [APERTO, S5]
```

### ⛔ **LA REGOLA DI OGGI NON CONSERVA, E LA TAVOLA DEL SIMULATORE LO DICE.** Le `67` regole di nascita si leggono dalla tavola `_nascita_regola`, e fra le sue `26` classi ### **non ce n'e' NESSUNA che si chiami «il genitore cede»**:

| | |
|---|---|
| il nato prende la ### **media dei genitori** per | `phi` `phi0` `phivel` `pos` `psi` |
| ### ⛔ **e nessuno togli niente al genitore** | ### **`Σρ` CRESCE a ogni nascita** — e' la violazione ### **`6`** di `A14`, e qui e' ### **letta dalla tavola**, non dedotta |

### **IL CONTO SULLO SNAPSHOT** *(la `ρ` vera della scena, dopo `3` passi pieni; il nodo piu' denso ha `ρ = 2.9121e+01`, lo `0.0886 %` di `Σρ`)*:

| se quel nodo divide | `Σρ` | `Σρ²` |
|---|--:|--:|
| ### **la regola di OGGI** | ### **`+0.0886 %`** *(non conserva)* | `+0.2062 %` |
| ### **la regola CANDIDATA** `ψ → ψ/√2` | ### **`0.000e+00`** *(conserva AL BIT)* | ### **`-0.1031 %`** *(il `ρ²` del nodo si DIMEZZA)* |

## `⑥.2` ### ⭐ **CHI PAGA LA NASCITA — LA PROPOSTA DI LUCA** *(2026-10-08, CANDIDATA per `S5`)*

> ### ⭐ **LA FRASE:** *«chi paga la nascita e' ### **il calore che si scarica sul vuoto locale**»*.

### **LETTA COL BILANCIO DELLA SONDA** *(`N = 400`, `g = -5`, braccio `NON-NORM`, seme `11`)*:

| il passo | il numero |
|---|--:|
| la ### **CONCENTRAZIONE libera** energia: `H`(esteso) → `H`(un nodo) | `-18533.8` → `-400000.0` |
| ### **energia liberata** | ### **`381466.2`** |
| in una dinamica conservativa *(`A16`)* ### **non sparisce** | diventa ### **agitazione del campo intorno**, cioe' ### **CALORE NEL VUOTO LOCALE** *(`A15.3`, reversibile)* |
| la ### **NASCITA costa** | ### **`+199600.0`** *(la prima divisione)* |
| e lo ### **PRELEVA da quel calore** | il costo e' il ### **`52.32 %`** di cio' che la concentrazione ha liberato |

### ➜ **IL FRENO SI PAGA DA SOLO: la concentrazione produce il calore che finanzia lo spazio nuovo, SENZA BAGNO ESTERNO.**

### ⚠ **E DUE COSE CHE IL CONTO DICE E CHE LA FRASE NON DICEVA ANCORA.**

**`(i)` IL MARGINE E' ZERO PER COSTRUZIONE — ed e' la forza E il limite.** In una dinamica conservativa l'energia per ### **disfare** il collasso e' ### **esattamente** quella che il collasso ha liberato: `381466.2` contro `381466.2`, ### **margine `0`**. ### ✔ **La forza: non serve nessun bagno esterno, il conto si chiude da solo.** ### ⛔ **Il limite: «basta» e «basta esattamente» sono la stessa cosa**, quindi il fatto che il conto torni ### **NON e' una prova che il processo avvenga** — e' la condizione minima perche' ### **non sia vietato.** ### ➜ **Quello che decide e' DOVE VA IL CALORE**, cioe' il punto `(ii)` qui sotto.

**`(ii)` ⭐ E IL FRENO SI FERMA DA SOLO, A UN NUMERO CHE NON HO SCELTO.** Il costo di una divisione va come `N²`, quindi ### **ogni livello della cascata costa un quarto del precedente**: `2^k · [(|g|/4)(N/2^k)² − w(N/2^k)] = (|g|/4)N²/2^k − wN`. Si somma e si guarda quando il calore finisce:

| livello | nodi | norma per nodo | costo del livello | cumulato | ### **calore residuo** |
|--:|--:|--:|--:|--:|--:|
| `0` | `1` | `400.0` | `199600.0` | `199600.0` | `181866.2` |
| `1` | `2` | `200.0` | `99600.0` | `299200.0` | `82266.2` |
| `2` | `4` | `100.0` | `49600.0` | `348800.0` | `32666.2` |
| `3` | `8` | `50.0` | `24600.0` | `373400.0` | `8066.2` |
| `4` | `16` | `25.0` | `12100.0` | `385500.0` | ### **`-4033.8`** |

### ➜ **IL CALORE SI ESAURISCE AL LIVELLO `4`: il sistema si ferma a `16` NODI.** ### ⭐ **Non frammenta all'infinito, e la scala d'arresto ESCE DAL BILANCIO — non e' una manopola** *(`A1`)*.

> ### ⭐ **E UN'IDENTITA' CHE VALE LA PENA DI DIRE:** la serie intera dei costi, ignorando l'hopping, fa `(|g|/2)N² = 400000.0`; l'energia liberata dal collasso fa `381466.2`. ### **I due termini `N²` SI CANCELLANO**, e la differenza — ### **`18533.8`** — e' esattamente `|H`(esteso)`|`, cioe' ### **i termini di HOPPING**. ### ➜ **Quindi non sono le grandezze dominanti a decidere se la nascita si paga: LO DECIDONO I TERMINI SOTTODOMINANTI** — ed e' il motivo per cui la decisione `2` *(l'interferenza normalizzata o no)* ### **pesa su questa**.

### ⭐ **LA CONSEGUENZA CANDIDATA SULLA SOGLIA** *(`A1`, `A15.2`)*

> ### **La soglia di nascita NON e' un numero ne' una massa critica a parte: e' IL BILANCIO STESSO.** Un nodo si divide quando ### **il calore disponibile nel suo vuoto locale ≥ `ΔH` della divisione.**

| | |
|---|---|
| ### ✔ **perche' questo soddisfa `A1`** | ### **non c'e' nessun numero da tarare:** `ΔH` si calcola da `H`, e il calore si misura dal campo. ### **E' una LEGGE, non una soglia** |
| ### ⭐ **e il segno del controretroazione e' QUELLO GIUSTO** | la nascita ### **diluisce** → la concentrazione ### **cala** → si produce ### **meno** calore → le nascite ### **rallentano**. ### **E' retroazione NEGATIVA, cioe' un REGOLATORE** — ed e' esattamente cio' che un freno deve essere. ### ⚠ **Lettura candidata, non misurata** |

### **CHE COSA SOSTITUIREBBE:**

| | |
|---|---|
| `massa_critica_adattiva` | ### **sparisce**: la soglia non e' una massa |
| `massa_critica_collasso` e i suoi ### **`21` usi DENTRO le leggi** | ### ⛔ **sparisce, ed e' la voce BLOCCANTE `U1`.** ### ➜ **La proposta di Luca non e' solo una forma piu' pulita: CHIUDE una voce che blocca i run base** |
| la soglia della mitosi come ### **numero** | diventa ### **il confronto fra due energie**, entrambe calcolate |

### ⛔ **E CHE COSA RESTA DA DEFINIRE — due cose, e non le invento:**

| | che cosa manca | ### **il candidato** |
|---|---|---|
| ### **`(i)`** | che cos'e' il ### **«vuoto locale» come grandezza CONTABILE** | la ### **parte del campo intorno alla massa che non e' nella massa**, cioe' le ### **oscillazioni irradiate** — ### ✔ **NON una variabile aggiunta:** si legge da `ψ` come `H` ristretta all'intorno ### **meno** l'energia del profilo stazionario lì. ### ⚠ **Questa sottrazione non e' scritta**, ed e' il pezzo che manca |
| ### **`(ii)`** | l'### **estensione di «locale»** | ### **i vicini diretti**, oppure ### ⭐ **una scala legata alla massa** — candidato: la ### **lunghezza di guarigione** `ξ = 1/√(|g|ρ)`, che e' ### **DERIVATA e non scelta** *(`A1`)*, ed e' la scala su cui il solitone stesso si forma. ### ⛔ **Fra le due c'e' una differenza MISURABILE**, e non e' misurata |

> ### ⚠ **E IL LEGAME CON IL `⑤.4`, che e' la cosa che mi ha sorpreso:** con i coniugati le memorie ### **oscillano invece di dimenticare**, quindi l'oblio deve venire ### **dallo stesso vuoto locale**. ### ➜ **La proposta di Luca non finanzia solo la NASCITA: finanzia anche L'OBLIO**, e le due cose diventano ### **lo stesso conto.** ### ⛔ **Che il conto basti per DUE uscite invece di una NON e' verificato**, e il margine — come dice il `(i)` — e' ### **zero**.

# ⛔ `⑦` **`PT-7`: LA NASCITA FRENA IL COLLASSO? -- LA VINCE A META', E LA META' CHE PERDE E' QUELLA CHE CONTA**

La previsione, scritta ### **prima** *(`c6c1112`)*: *«la divisione impedisce il collasso, perche' conserva `Σρ` ma dimezza il contributo `ρ²` del nodo che divide»*. Il conto, sulla `H` della sonda:

```
H(un nodo)   = (g/2) N^2
H(due figli) = -2 w (N/2) + (g/2) * 2 * (N/2)^2  =  -w N + (g/4) N^2
Delta H      = -(g/4) N^2 - w N  =  (|g|/4) N^2 - w N
```

| `N` | `g` | `w` | `H` un nodo | `H` due figli | ### **`ΔH`** |
|--:|--:|--:|--:|--:|--:|
| `400` | `-5.0` | `1.0000` | `-400000.0` | `-200400.0` | ### **`+199600.0`** |
| `400` | `-5.0` | `5.6494` | `-400000.0` | `-202259.8` | ### **`+197740.2`** |
| `400` | `-10.0` | `1.0000` | `-800000.0` | `-400400.0` | ### **`+399600.0`** |
| `400` | `-10.0` | `5.6494` | `-800000.0` | `-402259.8` | ### **`+397740.2`** |

| | |
|---|---|
| ### ✔ **la META' CHE VINCE** | ### **la diluizione c'e', ed e' ESATTA:** `Σρ` si conserva al bit e il contributo `ρ²` del nodo ### **si dimezza** — cioe' la divisione toglie ### **esattamente** cio' che il collasso guadagna |
| ### ⛔ **la META' CHE PERDE** | ### **la divisione ALZA `H`**, quindi ### **NON avviene da sola:** `ΔH = +199600.0` per `N = 400`, `g = -5.0`. ### **Va PAGATA** |
| ### ⛔ ### ➜ **la conclusione** | ### **LA NASCITA E' UN FRENO SOLO SE QUALCUNO PAGA**, e chi paga e' il ### **VUOTO LOCALE** — che e' il punto ### **`S5`**, e ### **`S5` e' APERTO**. ### ⚠ **Non e' una conferma dell'ipotesi del guardiano: e' la dimostrazione che quell'ipotesi DIPENDE INTERAMENTE DAL PUNTO APERTO** |

> ### ⭐ **E LA PROPOSTA DI LUCA RISPONDE ESATTAMENTE A QUESTO** *(`⑥.2`)*: il `ΔH` lo paga ### **il calore che la concentrazione stessa ha liberato** — `381466.2` disponibili contro `199600.0` richiesti dalla prima divisione, cioe' il ### **`52.32 %`**. ### ⛔ **Ma il margine complessivo e' ZERO per costruzione**, e la cascata ### **si ferma al livello `4`**: `16` nodi.

> ### ⭐ **E IL NUMERO CHE LEGA QUESTO AL SIMULATORE:** senza bagno le nascite crollano da ### **`164`** *(`B-SCAL`, col bagno)* a ### **`0`** *(`B-SCAL-TS`, senza)*. ### ➜ **Nel simulatore di oggi chi paga la nascita E' IL BAGNO GLOBALE**, ed e' misurato. ### **La domanda di `S5` non e' accademica: e' la domanda su che cosa sostituisca quel bagno.**

# ⭐ `⑧` **IL CONFRONTO CON LA SONDA DEL PROTOTIPO, termine per termine**

| nella sonda | nel simulatore | la lettura |
|---|---|---|
| ### **l'hopping** `-w ⟨ψ_i|U|ψ_j⟩` | la ### **coppia d'interferenza** con `A = w·cos(φ⁰_i − φ⁰_j)` | ### ⚠ **il kernel del simulatore ha `φ⁰` CONGELATA** *(`PHI0-CONGELATA`)*: la sonda non ha niente di congelato, e in questo e' ### **meno** difettosa |
| ### **la COESIONE** `(g/2)|ψ|⁴` | ### ⛔ **NON esiste un `|ψ|⁴`.** La coesione viene dalla ### **coppia stessa** *(una `A` positiva lega le fasi)* piu' il ### **legame elastico** | ### ➜ **la sonda ha messo in un termine di sito cio' che nel simulatore e' un termine d'ARCO** |
| ### ⛔ **il FRENO** | la ### **repulsione** `V_rep(d)`, la ### **massa critica**, e ### **la nascita dello spazio** | ### ⛔ **LA SONDA NON HA NESSUNO DEI TRE**, ed e' per questo che collassa |
| ### **il grafo** | ### **dinamico**: nodi e archi nascono | ### ⛔ **nella sonda e' FISSO**: un'### **impalcatura del test**, dichiarata violazione provvisoria di `A16.3` |
| la ### **memoria** | `tw`, `d0`, `peq`, `omega_s`, `mem_mot` | ### ⛔ **la sonda non ha NESSUNA memoria**: `w` e `U` sono fissi |

> ### ⭐ **E IL NUMERO DEL MARE `v2` SI LEGGE ADESSO:** con la sonda, a norma fissa, lo stato piu' basso e' il ### **collasso su un nodo** per ogni `g < 0` *(a `g = -5`: `-400000.0` contro `-18533.8`)*. ### ➜ **Non e' un fatto sul modello di Luca: e' un fatto su una `H` CHE NON HA IL FRENO.** Il simulatore ne ha ### **tre**, e la tavola li nomina.

# ⛔ `⑨` **L'ELENCO DELLE DECISIONI DI LUCA** — *una per riga, con le alternative e che cosa cambierebbe*

### ⭐ **TRE SONO PRESE** *(decisioni di Luca del 2026-10-08)*: la ### **`1`** *(il freno e' la `(c)`: entrambi)*, la ### **`3`** *(la sincronizzazione si toglie)*, la ### **`10`** *(il calore paga la nascita)*. ### **Le altre dieci sono APERTE**, e le schede delle prese stanno in `doc/REGISTRO_FISICA.md`.

| # | la decisione | le alternative | che cosa cambia |
|--:|---|---|---|
| `1` | ### ✔ ⭐ **IL FRENO DELLA COESIONE E' LA `(c)` — DECISIONE DI LUCA, PRESA** *(2026-10-08)* | ### **ENTRAMBI**, e non per prudenza | ### **FRENO VERO:** la ### **nascita dello spazio**, pagata dal calore *(decisione `10`)*. ### **FRENO A CORTO RAGGIO:** la ### **PRESSIONE DI DEGENERAZIONE** — *«che in natura esiste»* — come ### **BARRIERA PER NODO dentro `H`**. ### ⭐ **PERCHE' ENTRAMBI, ed e' coerenza non gusto:** se il freno fosse solo «capacita' + nascite», quando il calore si esaurisce *(livello `4`)* ### **le nascite si fermano e NON RESTA NESSUN FRENO.** Con la barriera: la degenerazione ### **tiene sempre**, la nascita ### **alleggerisce quando il calore la paga**, e se il calore non basta la materia ### **resta compressa al limite senza collassare**. ### **Scheda:** `freno-della-coesione`. ### **Dettagli:** `⑧` |
| `2` | ### **l'interferenza NORMALIZZATA sul grado, o no** | `w_ij` ### **come oggi**; oppure `w_ij/√(s_i s_j)` | il `PR` del Perron a `g = 0` passa da ### **`24.6`** a ### **`348.2`** su `400`: ### **la geometria da sola concentra, e la normalizzazione glielo toglie quasi tutto.** ### ⚠ **E tocca `A3`** *(`s_k` e' del proprio intorno — ma e' una SOMMA, non una statistica di posizione: `s̃_k` passa da `0.3856` a `0.1160` di deviazione, media `0.98`, ### **non `1`**)* |
| `3` | ### ✔ ⭐ **LA SINCRONIZZAZIONE SI TOGLIE — DECISIONE DI LUCA, PRESA** *(2026-10-08)* | ### **non ci sono piu' alternative: e' DECISA.** La scheda sta in `doc/REGISTRO_FISICA.md` *(`sincronizzazione-si-toglie`)* | ### **I TRE MOTIVI:** `(i)` ### **nessuna `E(φ)` esiste** *(asimmetria `1.0641` contro `1.438e-10`)*; `(ii)` ### **anche un Kuramoto SIMMETRICO e' un flusso di gradiente**, cioe' dissipativo — la forma che `A16.3` non ammette; `(iii)` toglierla ### **non costa coerenza** *(`AUC400` `0.9394` → `0.9333`)* e toglie il ### **`93.44 %`** del pompaggio. ### ➜ **DEVE EMERGERE:** al primo ordine uno stato stazionario ha `dφ_k/dt = μ` ### **per ogni `k`**, e il sistema ci arriva cedendo l'eccesso al vuoto locale — ### **lo stesso calore della `10`**. ### ⛔ **CRITERIO DA MISURARE, non da assumere:** la dispersione di `dφ/dt` dentro la massa deve ### **calare**, col calore contabilizzato. ### **Se non succede, la decisione si RIAPRE.** ### ⚠ **E lo stesso calore serve alla `1` e alla `10`: UN SERBATOIO, TRE USI** |
| `4` | ### **`A` da `φ⁰` o dalla MEMORIA VIVA dei legami** | `φ⁰` ### **congelata** *(oggi)*; oppure una memoria d'arco che ### **evolve** | ### ⛔ **`φ⁰` congelata viola `A15.1`** *(non dimentica niente)* ed e' `PHI0-CONGELATA`. Con la memoria viva `A` diventa un grado di liberta' ### **dentro `H`** *(`A16.3`)*, e la `H` candidata acquista un termine |
| `5` | ### **il campo scalare a `φ/2`** | `cos(φ_i − φ_j)` ### **(oggi)**; oppure `cos((φ_i − φ_j)/2)` ### **(la direzione candidata di Luca)** | ### **cambia la periodicita'**: `φ/2` e' la doppia copertura `4π`, cioe' ### **lo spinore**. ### ⚠ **E il ramo scalare di oggi usa `cos(φ_i − φ_j)`**, non `/2`: era un test sul ### **principio**, non sulla forma |
| `6` | ### **che cosa diventano TERMOSTATO e SCUOTIMENTO** | restare forzanti ### **globali** *(oggi, e viola `A2` e `A14.1`)*; oppure ### **scambio col vuoto LOCALE** *(`A15.3`)* | ### ⛔ **e non e' indolore: senza bagno le nascite crollano da `164` a `0`.** Togliere il bagno ### **senza** mettere il vuoto locale ### **spegne la crescita** |
| `7` | ### **la forma della DIVISIONE alla nascita, e la soglia come LEGGE** | `ψ → ψ/√2` ### **(candidata)**; oppure un'altra ripartizione | ### ✔ **`ψ/√2` conserva `Σρ` al bit e dimezza il `ρ²` del nodo** — ma ### **alza `H` di `+199600.0`**, quindi serve `S5`. ### ⛔ **E la soglia di oggi NON e' una legge:** `U1` e' ### **bloccante** |
| `8` | ### **DA DOVE VIENE L'ENERGIA DELLO SPAZIO NUOVO** *(`S5`)* | il ### **bagno globale** *(oggi, misurato)*; oppure un termine di ### **vuoto LOCALE** da scrivere | ### ⛔ **E' LA DECISIONE DA CUI DIPENDONO LE ALTRE:** senza di essa la nascita non puo' essere il freno, e la `1` si riduce a `(a)`. ### ⭐ **E LA PROPOSTA DI LUCA LE DA' UNA RISPOSTA CANDIDATA:** il calore della concentrazione stessa — ### **vedi la `10`** |
| `9` | ### ⭐ **LA GEOMETRIA AL SECONDO ORDINE** — `d` si muove con una velocita' propria *(Verlet, `vd`)*, ma ### **`A16.2` dice che ogni stato evolve al PRIMO ordine sotto `H`** | ### **`(a)`** la geometria e' ### **hamiltoniana in `(d, p_d)`**, cioe' ### **del primo ordine NELLO SPAZIO DELLE FASI**, con l'energia cinetica delle lunghezze ### **DENTRO `H`**; ### **`(b)`** la geometria diventa ### **anch'essa uno stato del tipo di `ψ`** | ### **vedi la tabella qui sotto** |
| `10` | ### ✔ ⭐ **IL CALORE PAGA LA NASCITA — DECISIONE DI LUCA, PRESA** *(2026-10-08; era ### **candidata** in `b6cba2f`)* | ### **non ci sono piu' alternative:** la soglia ### **E' IL BILANCIO** *(il nodo divide quando il calore del suo vuoto locale ≥ `ΔH`)*. ### **Scheda:** `chi-paga-la-nascita` | ### ⭐ **sparisce `massa_critica_collasso` e i suoi `21` usi dentro le leggi: CHIUDE la voce bloccante `U1`**, e la soglia diventa una ### **LEGGE** *(`A1`)*. ### ⛔ **E RESTA APERTO, scritto come aperto:** che cos'e' il ### **vuoto locale come grandezza contabile** e la sua ### **estensione**, ### **entrambi in forma RELAZIONALE** *(`A17`)*. ### ⛔ **CRITERIO CHE LA RIAPRE:** se il calore ### **non resta disponibile vicino alla massa** *(si disperde prima di poter pagare)*, si riapre |
| `11` | ### **la forma `U(2)` della coppia** | tenerla; oppure no | ### ⛔ **NON e' una traduzione: e' UNA LEGGE NUOVA** — `1.054` di scarto, il `105 %`, dieci volte sopra la soglia del `10 %`. ### **Va decisa come fisica nuova, non adottata come riscrittura** |
| `12` | ### **la SCOMPARSA degli archi** | tenerla; oppure vietarla | ### ⛔ **`A14.2` dice che la CRESCITA e' l'unica freccia ammessa**, quindi un arco che muore e' ### **già una violazione**. ### **Non e' una legge da tradurre: e' un difetto da decidere** |
| `13` | ### ⛔ **I CONIUGATI DELLE MEMORIE** *(`⑤.3`)* | `tw` come ### **fase di un legame `U(1)`** *(e allora arriva l'elettromagnetismo)*; `d0` e `peq` con un ### **impulso proprio**; oppure una forma diversa | ### **`τ` smette di essere un tempo di OBLIO e diventa una FREQUENZA**, e le memorie ### **oscillano invece di dimenticare**. ### ⛔ **E allora l'oblio deve venire dal vuoto — cioe' dalle decisioni `8` e `10`** |

### ⭐ **LA DECISIONE `9` PER ESTESO -- che cosa cambia nel codice, e che cosa diventa `beta·vd`**

| | ### **`(a)` hamiltoniana in `(d, p_d)`** | ### **`(b)` la geometria diventa uno stato come `ψ`** |
|---|---|---|
| ### **la lettura** | la geometria resta ### **sua**, ma col suo impulso: `H += Σ_archi p_d²/(2 m_arco)`, e `d' = ∂H/∂p_d`, `p_d' = −∂H/∂d`. ### ✔ **`A16` la AMMETTE**, perche' *«primo ordine»* vale ### **nello spazio delle fasi** — a patto che ### **il termine cinetico sia IN `H` e non aggiunto da fuori** | ### **la geometria SPARISCE come variabile indipendente:** `d` si ### **LEGGE** da un'ampiezza d'arco complessa, come `φ` si legge da `ψ`. ### **Un solo tipo di stato, una sola legge** |
| ### **che cosa cambia nel codice** | `vd` ### **diventa `p_d/m_arco`**, e `m_arco` ### **va DERIVATA, non scelta** *(`A1`)* — candidata: `m_arco = (d/cs)²`, la stessa inerzia che l'orologio usa gia'. ### ⚠ **Verlet e' GIA' simplettico, quindi l'integratore non e' il problema:** il problema e' che ### **l'energia cinetica non e' in `H`** e che `beta·vd` scrive ### **da fuori** | `d`, `vd`, `d0` ### **spariscono come variabili**; restano le ampiezze d'arco. ### ⛔ **E' una riscrittura PIU' GROSSA di `A16`:** `A16` riscrive i nodi, questa riscriverebbe ### **anche gli archi** |
| ### ⛔ **e `beta·vd`?** | ### **non ha piu' posto come e' scritto:** uno smorzamento sull'impulso e' ### **dissipazione** *(`A14` n.2, gia' dichiarata)*. ### ➜ **Diventa un TERMINE DI ACCOPPIAMENTO fra `p_d` e un grado del vuoto** *(`A15.3`)*, e l'anisotropia *(`ZETA_VIR`: dissipa radiale, libera tangenziale)* diventa ### **l'anisotropia di quel accoppiamento** | ### **SPARISCE**, e non per scelta: ### **senza una velocita' indipendente non c'e' niente da smorzare.** ### ⚠ **E cio' che `beta·vd` faceva — togliere energia al radiale — dovra' essere fatto da `H`, o non essere fatto** |

> ### ⚠ **E LA DIFFERENZA FRA LE DUE NON E' DI ELEGANZA:** la `(a)` ### **tiene due tipi di stato** *(i nodi `ψ`, gli archi `(d, p_d)`)*; la `(b)` ### **ne tiene uno**. ### ➜ **Per `9-ter` la `(b)` e' la variante con MENO LEGGI** — ma ### **non a parita' di effetto misurato**, perche' nessuna delle due e' stata misurata. ### ⛔ **Quindi `9-ter` NON decide qui**, e lo dico invece di usarlo come argomento.

---

# ⛔ **CHE COSA QUESTO DOCUMENTO NON DICE**

| | |
|---|---|
| la ### **forma di `H`** | ### ⛔ **non la decide.** La `H` del `⑤` e' ### **candidata**, e ha ### **due buchi dichiarati** *(`TAU_DIFF` nuda, `w`/`U` fissi)* |
| che le ### **traducibili** siano verificate | ### ⛔ **NO:** ### **una sola** lo e' *(la coppia scalare)*. Le altre dicono ### **perche' non lo sono**, e il motivo e' sempre lo stesso: ### **la forza non e' isolabile senza riscrivere il passo** |
| che la nascita ### **frenerebbe** | ### ⛔ **non lo dice:** dice che ### **diluisce esattamente** e che ### **costa**, quindi dipende da `S5`, ### **che e' aperto** |
| che i ### **contatori** siano davvero diagnostici | ### ⚠ **il criterio e' di FORMA** *(prefissi e code)*, e ### **puo' sbagliare**: ogni nome va verificato col ### **«nessun lettore»**, e questo giro ### **non lo fa** |
| le ### **scale e i semi** | ### **uno snapshot, una scena, `3` passi.** ### **`P3` non e' soddisfatta**, e il documento non pretende il contrario |
