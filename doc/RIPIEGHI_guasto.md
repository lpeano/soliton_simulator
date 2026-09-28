# 🔥 **LA PROVA A GUASTO DEI RIPIEGHI: il COMPORTAMENTO, non la lettura**

> ### **Generato da** `csv/_test_fork/_referto_guasto.py` dal referto
> `csv/_seal_fork/_guasto_ripieghi/_guasto_ripieghi.json`. **Non si modifica a mano:** si
> rigira lo strumento. *(`L-NUMERI`: ogni numero esce da uno script.)*

| | |
|---|---|
| strumento | `csv/_test_fork/_guasto_ripieghi.py` |
| simulatore | blob sha1-byte **`f7541d03`** |
| scena | `nmasse 3`, `sep 6.1158` → ### **`n = 12802`, archi `471564`** dopo **30** passi |
| errori **dichiarati** riconosciuti | `CacheCorta`, `SchermaturaSpenta`, `LimiteNodiSuperato`, `ComposizioneNonValida` |
| ### **il CONTROLLO** | ### **TIENE**: un passo da due copie di BASE e' **byte-identico**, `net.rng` compreso → ### **la prova VALE** |
| grandezze per nodo, **trovate in automatico** | ### **31** |
| sospette *(per arco con `len == n` per caso)* | **NESSUNA** — `n = 12802` e archi `= 471564` non possono coincidere |

**LA CONFIGURAZIONE INTERA** (`P5`) sta in `csv/_seal_fork/_guasto_ripieghi/_configurazione.txt`: ### **zero differenze su 80 booleani** rispetto alla configurazione del driver.
### ⚠ **E non la produce lo strumento, ed e' una mia omissione:** `_guasto_ripieghi.py` **non chiama** `_cli_flag.dichiara_configurazione`. Quel file e' un **riparo**, ricavato dallo **stesso** percorso *(stesso driver, stesso `--seme=11`, nessun passo avanzato)*. **La cura e' mettere la chiamata dentro lo strumento.**

## ⚖ Il verdetto sul criterio del guardiano, **fissato prima dei numeri**

> **«a posto» solo se ENTRAMBI i guasti danno PROTETTO, oppure se danno INERTE ed e'
> DIMOSTRATO che nessuna legge del passo la legge.»**

| esito | quante | quali |
|---|---|---|
| ### ⛔ **A POSTO** | ### **0 su 31** | ### **NESSUNA** |
| ### **RIPIEGO SILENZIOSO** | **10** | `_cs_nodo_prev` · `_nb_prec` · `_nb_ret` · `_psi_prec` · `_psi_spin_prec` · `_psi_spinor` · `_spinor_lift` · `mem_mot` · `phi_s` · `psi_spin` |
| **ROTTO RUMOROSO** *(eccezione non dichiarata)* | **8** | `_deg` · `eta` · `perc_chi` · `perc_geom` · `phi0` · `phivel` · `pos` · `psi` |
| **INERTE su entrambi** *(e NON vuol dire protetto)* | **12** | `_chi_core_nodi` · `_chi_core_raggio` · `_chi_core_rho0` · `_chi_geom_nodi` · `_fatt_cs_ultimo` · `_g_rampa_prec` · `_nb` · `_r_corrente` · `_xi_rumore` · `conc_nodi` · `omega_s` · `perc_tw` |
| ### **con effetto OLTRE l'ultimo nodo** | ### **10** | **tutte quelle che ripiegano** |

### ➜ **ZERO grandezze su 31 sono «a posto».** E le sole due che sollevano un errore
**dichiarato** sono `psi` e `rho_spin` — ### **esattamente le due curate stamattina**, e ### **solo dal
lato CORTA**:

| | CORTA | LUNGA |
|---|---|---|
| `psi` | **PROTETTO** `SchermaturaSpenta` | ROTTO `ValueError` soliton_simulator.py:3467 |
| `rho_spin` | **PROTETTO** `CacheCorta` | INERTE |

> ### 📌 **LA CURA FUNZIONA, E FUNZIONA SOLO DOVE L'HO MESSA — e solo su CORTA.**
> `_ferma_se_cache_corta` comincia con `if quanta >= n: return`: ### **una cache PIU'
> LUNGA passa in silenzio.** E' il lato che i tre confronti `len(x) > n` guardavano, e che
> ho lasciato scoperto. ### **Non e' una congettura: `psi` LUNGA da' un `ValueError` di
> broadcast, non un errore dichiarato.**

## La tabella, grandezza per grandezza

**`nodi` e `archi` sono QUANTI cambiano** rispetto al controllo, **sui primi `n-1` nodi**
*(cioe' escludendo il nodo che ho guastato io)* e su **tutti** gli archi.
### **`12801` nodi vuol dire OGNI nodo tranne quello guastato: e' TUTTA LA RETE.**

| grandezza | CORTA | LUNGA | gr. | nodi | archi | scost. max | come la leggeva la tabella |
|---|---|---|---|---|---|---|---|
| `_chi_core_nodi` | INERTE | INERTE |  |  |  |  | ### **mai nominata, con nessun nome** |
| `_chi_core_raggio` | INERTE | INERTE |  |  |  |  | ### **mai nominata, con nessun nome** |
| `_chi_core_rho0` | INERTE | INERTE |  |  |  |  | ### **mai nominata, con nessun nome** |
| `_chi_geom_nodi` | INERTE | INERTE |  |  |  |  | ### **mai nominata, con nessun nome** |
| `_cs_nodo_prev` | ### **RIPIEGO SILENZIOSO** | INERTE | 15 | 12801 | 471564 | `8.04e-02` | **(d)**×5 *(come `_csn`, `_csp2`, `_csp_in`, `csn`, `csp`)* |
| `_deg` | ROTTO `ValueError` soliton_simulator.py:5890 | ROTTO `ValueError` soliton_simulator.py:5890 |  |  |  |  | **(d)**×1 |
| `_fatt_cs_ultimo` | INERTE | INERTE |  |  |  |  | ### **mai nominata, con nessun nome** |
| `_g_rampa_prec` | INERTE | INERTE |  |  |  |  | ### **mai nominata, con nessun nome** |
| `_nb` | INERTE | INERTE |  |  |  |  | **(b)**×1 **(c)**×4 **(d)**×5 **(x)**×1 |
| `_nb_prec` | ### **RIPIEGO SILENZIOSO** | ### **RIPIEGO SILENZIOSO** | 6 | 12801 |  | `8.09e-02` | **(d)**×1 |
| `_nb_ret` | ### **RIPIEGO SILENZIOSO** | ### **RIPIEGO SILENZIOSO** | 9 | 12801 | 471564 | `2.20e-03` | **(d)**×1 *(come `nbr`)* |
| `_psi_prec` | ### **RIPIEGO SILENZIOSO** | ### **RIPIEGO SILENZIOSO** | 15 | 12801 | 471564 | `1.26e+01` | **(d)**×1 |
| `_psi_spin_prec` | ### **RIPIEGO SILENZIOSO** | ### **RIPIEGO SILENZIOSO** | 15 | 12801 | 471564 | `1.13e-01` | **(c)**×2 **(d)**×2 *(come `_psp`)* |
| `_psi_spinor` | ### **RIPIEGO SILENZIOSO** | INERTE | 17 | 12801 | 471564 | `4.75e+03` | **(b)**×1 **(c)**×2 **(d)**×5 **(e)**×1 **(x)**×1 *(come `_ps`, `_psp`, `cur`)* |
| `_r_corrente` | INERTE | INERTE |  |  |  |  | **(d)**×2 *(come `r`, `r_loc`)* |
| `_spinor_lift` | ### **RIPIEGO SILENZIOSO** | INERTE | 9 | 12801 | 471564 | `1.55e-02` | **(c)**×4 **(d)**×1 |
| `_xi_rumore` | INERTE | INERTE |  |  |  |  | **(b)**×1 *(come `_xi`)* |
| `conc_nodi` | INERTE | INERTE |  |  |  |  | **(c)**×1 **(x)**×1 |
| `eta` | ROTTO `ValueError` soliton_simulator.py:4278 | ROTTO `ValueError` soliton_simulator.py:4278 |  |  |  |  | **(c)**×1 |
| `mem_mot` | ### **RIPIEGO SILENZIOSO** | INERTE | 2 | 12611 | 471564 | `2.21e-02` | **(b)**×1 |
| `omega_s` | INERTE | INERTE |  |  |  |  | **(b)**×1 **(x)**×1 |
| `perc_chi` | ROTTO `IndexError` soliton_simulator.py:3688 | INERTE |  |  |  |  | **(c)**×7 **(d)**×11 |
| `perc_geom` | ROTTO `IndexError` soliton_simulator.py:5721 | INERTE |  |  |  |  | ### **mai nominata, con nessun nome** |
| `perc_tw` | INERTE | INERTE |  |  |  |  | ### **mai nominata, con nessun nome** |
| `phi0` | ROTTO `IndexError` soliton_simulator.py:5600 | INERTE |  |  |  |  | ### **mai nominata, con nessun nome** |
| `phi_s` | ### **RIPIEGO SILENZIOSO** | ### **RIPIEGO SILENZIOSO** | 6 | 12801 |  | `4.15e-02` | **(d)**×4 |
| `phivel` | ROTTO `ValueError` soliton_simulator.py:839 | ROTTO `ValueError` soliton_simulator.py:5777 |  |  |  |  | **(c)**×1 **(d)**×1 |
| `pos` | ROTTO `ValueError` soliton_simulator.py:5790 | ROTTO `ValueError` soliton_simulator.py:6933 |  |  |  |  | ### **mai nominata, con nessun nome** |
| `psi` | **PROTETTO** `SchermaturaSpenta` | ROTTO `ValueError` soliton_simulator.py:3467 |  |  |  |  | **(b)**×1 **(c)**×4 **(d)**×12 **(e)**×1 **(x)**×1 *(come `cur`)* |
| `psi_spin` | ### **RIPIEGO SILENZIOSO** | ### **RIPIEGO SILENZIOSO** | 15 | 12801 | 471564 | `1.13e-01` | **(d)**×3 **(e)**×2 *(come `_ps`)* |
| `rho_spin` | **PROTETTO** `CacheCorta` | INERTE |  |  |  |  | **(e)**×1 |

## ✅ **Il caso che deve fallire FALLISCE COME DEVE**

| | |
|---|---|
| il guasto | `psi` **CORTA** sul blob **PRE-CURA** *(il padre del commit che introduce `_eredita_psi_figli`)* |
| esito | ### **RIPIEGO SILENZIOSO** |
| quanto | **17** grandezze · ### **12801 nodi** · **471564 archi** · scostamento max ### **`1.256e+01`** |
| ### **lo stesso guasto OGGI** | **PROTETTO** `SchermaturaSpenta` |

### ➜ **La prova RIPRODUCE il flash e mostra che la cura l'ha chiuso.** Lo stesso guasto,
sulla stessa scena, sullo stesso passo: **prima** cambiava **tutta la rete in silenzio**,
**oggi** alza `SchermaturaSpenta`. ### **Non e' una lettura: e' lo stesso esperimento due
volte.**

## ⛔ Tre difetti del MIO strumento, e **nessuno tocca gli esiti**

Gli esiti escono dal **confronto dello stato**, non dal tracciatore.
### **Quello che segue invalida la colonna «riga responsabile», non il verdetto.**

| | |
|---|---|
| ### **① le etichette del braccio PRE-CURA sono SBAGLIATE** | i numeri di riga vengono dal file **pre-cura**, annotati con la tabella di **oggi**. ### **I numeri di riga SHIFTANO fra due blob** — e' la regola del par.2 che ho scritto io e poi violato. **Verificato:** pre-cura `:3391` e' `if med == _med_corrente:`, `:3465` e' `if _xi is None or len(_xi) < n:`, `:5754` e' `F = Mw @ np.exp(1j * self.phi)` — ### **nessuna delle tre e' un confronto su `psi`** |
| ### **② «eseguita» NON vuol dire «ramo di scorta PRESO»** | registro la riga della **GUARDIA**, non quella del **CORPO**: un `if` si esegue in **entrambi** i casi. Dove compare **anche** una riga di corpo *(`:3465` dentro `ritmo`, per `_psi_prec`)* la prova c'e'; **altrove no** |
| ### **③ il filtro per NOME perde gli ALIAS LOCALI** | `_cs_nodo_prev` si legge in `_csp_in = getattr(self, "_cs_nodo_prev", None)`, quindi la tabella chiama quella cache **`_csp_in`** e il mio filtro non la riconosce. ### **Ecco perche' 4 delle 10 che ripiegano non hanno una riga responsabile: non e' che il sito manchi dalla tabella — e' che il nome non combacia** |

> ### 📌 **E' LA QUINTA VOLTA, E SEMPRE LA STESSA FORMA.** Dopo `(b)` che contava `full(n,…)` come «estende», `(a)` che chiamava «inizializzazione» una condizione fusa, `==`/`!=` messi «fuori dal mandato» e il ramo degli `IfExp` invertito: ### **una regola che parte dal NOME o dalla SINTASSI e non da CHE COSA SCATTA.** La prova a guasto e' immune *(guasta e guarda)*; ### **il pezzo che ci ho attaccato sopra per attribuire la colpa NO.**

**Che cosa la renderebbe una prova:** registrare la riga del **corpo** del ramo, **oppure** confrontare i **contatori** `_g_*` fra il giro di controllo e il giro guastato — che sono ### **gia' li', per `A8`**, nei siti che li hanno *(`_cs_in_fallback`, `_ritmo_sicurezza`, `_sfb_lift_corto`…)*. E dove il contatore **non c'e'**, ### **la sua assenza e' essa stessa un difetto `A8`.**

## ⚙ **IL MECCANISMO, misurato: perche' la cura PER GUARDIE non tiene**

Tre casi, e ### **tutti e tre si leggono dai numeri, non dal codice**.

### ① `psi_spin`: la guardia c'e', ### **ESEGUE, e non spara**

| | |
|---|---|
| la guardia | `:4462` in `_nb_grav` — `_ferma_se_cache_corta("psi_spin", len(_ps), n, ...)`, ed e' **la cura di stamattina**, classe **(e)** |
| il tracciatore | ### **`:4462` ESEGUE** |
| e nonostante questo | ### **RIPIEGO SILENZIOSO** — 15 grandezze, **12801 nodi**, 471564 archi, scost. `1.13e-01` |

### ➜ **Se la guardia esegue e NON solleva, quando la legge `psi_spin` e' GIA' LUNGA `n`.** E l'unica scrittura a piena lunghezza e' **`:4421` in `calcola_psi`** *(`self.psi_spin = _Fs / (1.0 + GAMMA * _norm)[:, None]`)*.
### ⚠ **La guardia sta A VALLE della riscrittura: non protegge NIENTE.** Il danno e' gia' avvenuto a monte, in chi ha letto la `psi_spin` corta prima di `calcola_psi`.

### ② `_psi_spinor`: la coda si allunga, e la guardia a valle trova un array giusto

| | |
|---|---|
| il tracciatore | ### **`:2262` ESEGUE** *(`elif len(cur) < n:` in `_estendi_psi_spinor`)* e ### **`:2265` NO** — quindi il ramo preso e' **l'estensione** `:2264` `self._psi_spinor = np.vstack([cur, manca])` |
| esito | ### **RIPIEGO SILENZIOSO** — 17 grandezze, **12801 nodi**, 471564 archi, ### **scost. `4.75e+03`**, il piu' grande del giro |

### ➜ **Un estensore a monte DISARMA ogni guardia a valle**: la cache arriva lunga `n`,
con **una riga inventata** al posto di quella vera.

### ③ `mem_mot`: e' classe **(b)**, *«estensione dei soli nuovi»*, e ### **NON e' sicura**

| | |
|---|---|
| il sito | `:7009` `if len(self.mem_mot) < n:` → `vstack([mem_mot, zeros((n-len, 3))])`. ### **E' una estensione VERA della coda**, non un `full(n, ...)` |
| la mia tabella | **(b)**, cioe' *«i primi `len(x)` restano»* — e **restano davvero** |
| ### **la misura** | ### **RIPIEGO SILENZIOSO**: 2 grandezze e ### **12611 nodi su 12801** cambiano, scost. `2.21e-02` |

### ➜ **Perche' (b) non basta:** l'elemento inventato e' `zeros(1, 3)`, e appartiene a un nodo ### **CHE ESISTEVA GIA'** e che aveva una memoria vera. ### **(b) e' sicura per i nodi APPENA NATI, non per una cache che e' corta per QUALUNQUE ALTRA RAGIONE** — e i due casi ### **hanno la STESSA FORMA**, quindi nessuna regola sintattica li distingue.

> ### 📌 **E QUESTO E' L'ARGOMENTO PER LA SUA FORMA DI CURA.** Tre guasti su tre mostrano che una guardia **dentro** una legge arriva **troppo tardi** o **troppo presto**: a valle di una riscrittura non vede niente, a monte di un estensore viene aggirata. ### **Un CONTROLLO UNICO nello schedulatore, PRIMA che le leggi girino, non ha questo problema** — ed e' esattamente quello che il guardiano ha proposto.

## 🔀 L'incrocio con `doc/RIPIEGHI_incrocio.md`: **conferma o smentisce?**

| | |
|---|---|
| ### **conferma la SUA lettura** | il suo verdetto era *«sostituzione VIVA, deve diventare errore»*. ### **La prova lo dimostra col comportamento: 10 grandezze cambiano TUTTA LA RETE in silenzio, e ZERO su 31 sono «a posto».** |
| ### **conferma la sua proposta di CURA** | la sua era **un solo controllo dello schedulatore** invece di quaranta `raise` sparsi. ### **La prova la corrobora: le due sole protette sono le due che ho curato a mano, e una delle due lo e' solo da un lato.** Curare sito per sito ha lasciato **29 grandezze su 31** scoperte |
| ### **smentisce una MIA premessa** | avevo trattato il mandato come «i 101 confronti». ### **La prova misura le GRANDEZZE, e sono 31 — quindici non stanno nelle 23 del sigillo.** Un elenco di confronti non e' un elenco di grandezze |
| aggiunge un lato che **nessuna** delle due letture aveva | ### **il lato LUNGA.** La cura di stamattina protegge solo il CORTO: `if quanta >= n: return` |

### I tre *«da guardare a mano»* del suo gruppo 7

| sito | che cosa dice la PROVA A GUASTO |
|---|---|
| `:2153` `_aggiorna_lift_spinoriale` *(`self._nb`)* | ### **la riga non e' MAI stata ESEGUITA** in un passo: e' assente da tutte e 10 le tracce. E il guasto su `_nb` da' ### **INERTE su entrambi**. ➜ ### **DORMIENTE in questa configurazione** — d'accordo con la sua lettura *(«blocco saltato»)*, e in piu': **il blocco non ci arriva nemmeno** |
| `:5750` `step` *(`self.d0`)* | ### **la prova NON PUO' provarlo, e lo dico:** `d0` e' **per ARCO**, quindi non e' fra le 31 grandezze per nodo. ### **Ma la misura conferma la sua lettura per un'altra via:** archi `471564` contro `n = 12802`, quindi `len(d0) >= n` e' **sempre vero** e ### **il ramo di scorta non scatta mai** |
| `:5859` `step` *(`_chi_geom_nodi`, perche' `CHI_COOP` e' **ON**)* | ### **la riga ESEGUE**, e il guasto da' ### **INERTE su entrambi**. ➜ **ha ragione lui: e' un RICALCOLO**, e la prova aggiunge che il ricalcolo riproduce la cache ### **ESATTAMENTE** a questo passo. ### ⚠ **«Inerte» NON vuol dire «a posto»: la grandezza E' LETTA**, quindi per il criterio del guardiano **non passa** |

## ✅ **E la correzione di una cosa che avevo detto senza saperla**

In `360e681` ho scritto che almeno una grandezza porta un `inf` e che ### **non sapevo
quale**. Ora lo strumento lo elenca:

| grandezza | `inf` | `nan` | su quanti |
|---|---|---|---|
| `eta` | ### **12802** | 0 | 12802 |

### ➜ **`eta` e' `inf` su TUTTI i nodi, ed e' LEGITTIMO E GIA' DICHIARATO:** la tabella
dei domini dice *«`eta`: `nonneg_inf` — non negativa, e **`+inf` per il vuoto DATO**»*
(`:241-242`). Un nodo del vuoto seminato **non ha un tempo di accensione**, e
`ramp = min(1, eta/tau)` da' `1`. ### **Quindi il primo giro non e' morto su un difetto
della fisica: e' morto sul mio confronto.** *(Nel commit del fallimento avevo detto
«probabilmente una sentinella»: era un'ipotesi, e va sostituita da questo fatto.)*

---

## 🛑 Che cosa NON dice questa prova

| | |
|---|---|
| **«INERTE» non e' un'assoluzione** | vuol dire che **in QUESTO passo, in QUESTA configurazione** nessuna legge l'ha letta. ### **Sono 12 grandezze, e per dirle «a posto» serve DIMOSTRARE che nessuna legge le legge** |
| **un passo, non una traiettoria** | il guasto e' iniettato al passo **30** e si guarda **un** passo. Un ripiego che morde solo **dopo** una nascita qui non compare — e le nascite cominciano al **42** |
| ### **niente e' curato** | questa e' una **misura**, non una cura. ### **Non ho toccato un byte di fisica**, e sulla forma della cura decide Luca |

