# I FATTI VERIFICATI DAL CODICE - **ordinati per FUNZIONE del simulatore**

> **Non sono regole: sono cio' che il codice FA oggi.** Erano `par.9` di `CLAUDE.md`, e da li' vengono **verbatim**.
> **Si legge QUANDO SERVE, non all'avvio** - e la regola in `CLAUDE.md` e' *«prima di toccare una funzione, leggi i suoi fatti qui»*.
>
> *(Generato da `csv/_riordino_fatti.py`. Le righe del simulatore sono **misurate dall'AST**, non ricopiate: quelle dentro i fatti sono di blob vecchi e vanno lette come storiche.)*

| funzione | riga di oggi | quanti fatti |
|---|--:|--:|
| `rapporto_guardie` | `soliton_simulator.py:606` | 1 |
| `_eredita_spinore_figli` | `soliton_simulator.py:1933` | 1 |
| `ritmo` | `soliton_simulator.py:2983` | 3 |
| `_passo_spinoriale` | `soliton_simulator.py:3100` | 13 |
| `salva_stato` | `soliton_simulator.py:4617` | 3 |
| `_cs_nodo` | `soliton_simulator.py:4734` | 2 |
| `_bloch_ritardato` | `soliton_simulator.py:4789` | 2 |
| `_tempo_luce_nodo` | `soliton_simulator.py:4947` | 3 |
| `_coppia_interferenza` | `soliton_simulator.py:5019` | 1 |
| `mitosi` | `soliton_simulator.py:5871` | 2 |
| `memoria_hebbiana_moto` | `soliton_simulator.py:6547` | 3 |

---

## LE RIGHE CITATE NEI FATTI SONO DI BLOB VECCHI

> Si cerca **per NOME di funzione o di flag, mai per riga**. La tabella qui sotto e' storica e si legge per sapere **a quale blob** un numero si riferiva.

- **LE RIGHE CITATE QUI SOTTO SONO SHIFTATE: il blob e' cambiato** (2026-09-15). Il cablaggio di
  `TAU_LUCE` e il fix della cache hanno spostato tutto cio' che sta dopo la riga ~810. Vale il par.0
  (*cerca per NOME di funzione/flag, non per riga*), ma poiche' le righe **sono** citate ovunque,
  ecco la conversione, **generata confrontando i TRE blob riga per riga** (`git cat-file`), non per aritmetica: un `-` significa che la stringa non esiste in quel blob. **RIGENERATA il 2026-09-15 dopo che tre righe, calcolate a mano per differenza, erano sbagliate.** I numeri storici **non sono stati
  riscritti** nelle voci: li' dicono a quale blob si riferivano, ed e' un'informazione, non un errore.

  | punto | `f5887254` | `b298677a` | **ORA (`08784685`)** |
  |---|---|---|---|
  | commento stale "si conserva, non rilassa" | 868 | 901 | **901** |
  | commento stale "omega si CONSERVA" | 1803 | 1852 | **1864** |
  | rumore sul Bloch (`amp[:, None]`) | 1847 | 1896 | **1908** |
  | `nb_vic = self._nb_prec` | 1856 | 1905 | **1917** |
  | `inerzia = np.maximum(_rho_sorgente(), 1e-6)` | 1891 | 1940 | **1952** |
  | `correzione = np.cross(B, nb)` | 1895 | 1944 | **1956** |
  | `correzione += cross(_nb_grav(), nb)` | 1901 | 1950 | **1962** |
  | `_tau = TAU_A * max(_dens/_dens_rif, 0.05)` | 1913 | 1967 | **1979** |
  | **il rilassamento** `- omega_src/_tau` | 1918 | 1972 | **1984** |
  | `calcio_omega` dentro `semina()` | 1593 | 1642 | **1654** |
  | **la guardia 4pi** `len(_ps) == self.n` | 1780 | 1829 | **1841** |
  | scrittura di `_psi_spin_prec` | 2555 | 2647 | **2659** |
  | guardia `len(csp) >= n` in `_tempo_luce_nodo` | 2435 | 2565 | **2577** |
  | scrittura della cache `_cs_nodo_prev` | 2826 | 2918 | **2930** |
  | trasporto SCALARE `mat(A)@_a` | 2531 | 2623 | **2635** |
  | `cs_floor` | 2382 | 2436 | **2448** |
  | `def _eredita_spinore_figli` | 1133 | 1170 | **1170** |
  | mitosi -> `_eredita_spinore_figli(a)` | 3125 | 3217 | **3229** |
  | Schwinger -> `_eredita_spinore_figli(aa, -1)` | 3242 | 3334 | **3346** |

---

## `rapporto_guardie`

*(oggi a `soliton_simulator.py:606` - **misurato dall'AST**. i contatori delle guardie: quante volte un ramo e' stato saltato.)*

- **ESISTONO I CONTATORI DELLE GUARDIE, e si leggono con `rapporto_guardie(net)`** (2026-09-20,
  `Z68`/`Z69`). **Sono BYTE-INERTI** *(verificato: 7 campi identici contro il blob precedente)* e
  coprono **quindici siti**. **Ogni sito ha QUATTRO numeri, non uno:** invocazioni, salti, **la
  FORMA al fallimento** *(le due lunghezze; `-1` significa memoria ASSENTE, non lunghezza 0)* e
  **QUANDO** — l'indice dell'ULTIMA invocazione saltata. **Il `quando` non e' un lusso:** `20 %` di
  salti **confinati alle prime 11 invocazioni su 55** e `20 %` **sparsi su tutto il run** danno lo
  **stesso conteggio** e sono due diagnosi opposte (`A8`).
  **⚠ E I CONTATORI DELLE `(b)` SI CHIAMANO `_spento`, NON `_salti`:** misurano un ramo che non gira
  **per scelta** (flag o costante a zero), non una legge saltata. Mescolarli produrrebbe una
  «frazione di fallimento» che e' una **frequenza di selezione**.

---

## `_eredita_spinore_figli`

*(oggi a `soliton_simulator.py:1933` - **misurato dall'AST**. che cosa il figlio eredita dal padre alla nascita.)*

- **EREDITA' ALLA MITOSI = COPIA ESATTA (verificato dal codice, 2026-09-15, blob f5887254).**
  `_eredita_spinore_figli` (righe ~1133-1170) copia dal padre `src` SENZA perturbazione: `_nb`,
  `_nb_prec`, `_nb_ret`, `omega_s`, `_psi_spinor`, `_spinor_lift`, `_psi_prec`. Il figlio nasce al
  PUNTO MEDIO dell'arco (riga ~3094) con ESATTAMENTE due archi, verso entrambi i genitori (righe
  ~3172-3173). **Conseguenza: ogni nascita crea una coppia con chi = 0** (misurato 0.0000 esatto).
  **La parentela NON e' registrata** (gli unici `parent` del file, righe ~949-982, sono lo
  spanning-tree dei cicli, non genealogia) **ma e' RICOSTRUIBILE in volo**: il padre `a` sta nel
  lato `i` dell'arco `(a, m)`. Misurato 100% su 7/7 e poi su 4163 coppie.
  NB: l'antinodo Schwinger (riga ~3242) eredita `-psi`, ma `nb = psi^dag sigma psi` e' INVARIANTE
  per fase globale: **anche l'antinodo nasce con chi = 0 in Bloch**. "Antichirale" riguarda il segno
  di doppia copertura, NON la direzione.

---

## `ritmo`

*(oggi a `soliton_simulator.py:2983` - **misurato dall'AST**. l'orologio: `r`, `dt_n = DT*r`, e la doppia copertura a 4pi.)*

- Orologio/EM (`_phc`, `omega_clk`, `ritmo()`, `dt_n=DT*r`): NON usa cs. Due tempi propri scollegati
  (metrico tau_p=d/cs vs orologio dt_n=DT*r). L'accoppiamento cs<->orologio e' lo Step 2 (non fatto).
- **IL TIC DEI PROCESSI LOCALI E' `dt_n = DT*r`, NON `DT`** (fatto generale, non solo del fork).
  `DT` nudo e' il tempo di COORDINATA: usarlo dentro un rilassamento locale cancella la dipendenza
  dall'orologio del luogo, cioe' impone la foliazione sincrona globale = **un frame preferito, un
  "etere"**. Tutta la fisica del file integra gia' in `dt_n`/`dt_e` (phivel, tw); `DT` nudo vive
  solo nel conteggio dei sottopassi CFL. Preso una volta nello Strato 1 (bug dell'istruzione, non
  dell'esecuzione) e corretto. **Presidio permanente: il sigillo S7** (`_sigillo_strato1.py`), che
  misura `alpha` su nodi con ritmi diversi: con `dt_n` il rapporto r=2/r=1 vale 1.9753, col `DT`
  varrebbe esattamente 1.000. S1..S6 passavano IDENTICI col bug: senza S7 era invisibile.
- **`_psi_spin_prec` NON ERA ESTESO ALLA MITOSI → LA FASE 5 (OROLOGIO A 4pi) E' STATA INERTE IN OGNI
  RUN MAI GIRATO — CURATO il 2026-09-15** (commit `cc98ac0`, `doc/REPERTO_psi_spin_prec.md`, sigillo
  `csv/_seal_fork/_sigillo_psi_spin_prec.py` **6/6 PASS**). La guardia di `ritmo()` e' un'uguaglianza
  **ESATTA** (`len(_ps) == n and len(_psp) == n`), quindi bastava **un** nodo di mitosi per farla
  scartare. **MISURATO: 95.33%** delle chiamate (143/150), e la condizione che falliva era
  `len(_psi_spin_prec) != n` in **143 casi su 143** — `psi_spin`, ricostruito da `calcola_psi`
  **dentro** il passo, era sempre lungo `n`. Il 4pi girava **solo ai passi 2 e 3**, prima della prima
  mitosi. Dopo la cura: **0.00%**.
  **ATTENZIONE ALLA FORMULAZIONE, perche' quella sbagliata circola gia':** **NON** e' vero che *"la
  fisica ha integrato con un tempo proprio stale"*. `signed` era **gia' calcolato** nella versione
  **SCALARE a 2pi** poche righe sopra; la guardia decide solo se **sovrascriverlo** col 4pi. `r` era
  **ricalcolato a ogni passo ed era valido** (`len(_psi_prec) == n` in 149 chiamate su 150). La
  frase vera e': **la fisica ha integrato con l'orologio SCALARE STORICO, e la doppia copertura non
  e' mai entrata in funzione.** Le misure **non sono corrotte**: sono misure di un **modello diverso
  da quello che il flag dichiarava**. *"Integrate male"* implicherebbe errore numerico; *"orologio
  diverso da quello dichiarato"* implica modello diverso, **e solo la seconda e' vera.**
  **Conseguenza:** tutte le misure fino al blob `08784685` portano il marchio *"prese col ritmo
  scalare a 2pi; da riverificare col settore 4pi in funzione"* — **T3 e i suoi quattro bracci
  inclusi** (`doc/RAMIFICAZIONI.md`, secondo marchio in testa).

---

## `_passo_spinoriale`

*(oggi a `soliton_simulator.py:3100` - **misurato dall'AST**. il passo dello spinore di nodo: `omega_s`, la coppia, l'inerzia, il rilassamento, l'orologio de Broglie.)*

- `_passo_spinoriale`: NON orfano (docstring stale), cablato dietro `SPINORE_VIVO` (OFF). E' ON-SITE
  (precessione dello spinore del nodo con memoria hebbiana + inerzia |Psi|^2), NON arc-connection.
- **SOTTO `--spinore-corretto` IL RUMORE NON TOCCA IL BLOCH DIRETTAMENTE** (verificato dal codice,
  2026-09-15). Il ramo additivo sul Bloch/spinore (righe ~2060, ~2085) e' gated su `SYNC_UPDATE`,
  che e' SPENTO in tutti i run del fork; il `_nb` committato e' DERIVATO da `_psi_spinor` (righe
  ~2066-2069, ~2088). Il rumore entra SOLO via `correzione = cross(B, nb)` -> `omega_new`: e'
  **rumore di COPPIA, non di posizione sulla sfera**.
- **IL SETTORE DI SPIN NON E' RISOLTO NEL TEMPO DAL PASSO DT** (misurato 2026-09-15,
  `doc/BILANCIO_ordine_spin.md`; UN seme, UNA scena, passo 60: da riconfermare). `omega_s` letto
  direttamente dal simulatore da `theta = |omega_s|*dt_n` mediana **2.4e4 GRADI per passo = ~67 giri
  interi**, 99.3% dei nodi oltre il giro. Non c'e' clamp su `theta` (righe ~2033-2037).
  CAUSA: `inerzia = np.maximum(_rho_sorgente(), 1e-6)` (riga 1891) con densita' mediana **1.21e-07**
  -> il pavimento e' attivo sul **99.7%** dei nodi, e `omega = coppia/inerzia` ~ 6e4 mentre la coppia
  e' ORDINARIA (0.06). **Il pavimento 1e-6 NON e' la causa: la MITIGA** (senza, omega sarebbe otto
  volte maggiore). **E' LA STESSA RADICE di "a densita' reali cs e' MORTO" (par.6), con segno
  opposto:** la densita' minuscola CONGELA la metrica e FA ESPLODERE lo spin.
  CONSEGUENZA DI LETTURA: le misure negative sul settore di spin restano valide, ma NON dicono "non
  esiste una fisica ordinante": dicono "in questo regime numerico nessun ordine sopravvive a un tick".
- **ATTENZIONE, DUE COMMENTI STALE SU `omega_s`** (verificato 2026-09-15): le righe **868**
  (*"motore conservativo: si conserva, non rilassa"*) e **1803** (*"omega si CONSERVA, non insegue
  lo zero"*) dicono il FALSO. L'UNICO aggiornamento per passo e' la riga **1918**, che contiene
  **`- omega_src/_tau`**: e' un rilassamento del primo ordine, con
  `tau = TAU_A * max(rho/rho_rif, 0.05)`. **La dissipazione su `omega_s` ESISTE.** Chi legge solo i
  commenti costruisce una diagnosi sbagliata (e' successo: vedi `doc/ANALISI_gilbert_fdt.md` par.1).
  NB anche: il calcio termico `calcio_omega` (righe 1592-1594) e' DENTRO `semina()`, quindi e' il
  punto zero ALLA NASCITA del nodo, **non** una sorgente di rumore per passo.
- **PIU' MEMORIA SU `omega_s` = PIU' ROTAZIONE, non piu' ordine** (riga 1918; misurato 2026-09-15).
  **CORRETTO il 2026-09-15** — la versione precedente di questo punto diceva
  `omega_eq = tau * coppia/inerzia` (proporzionale a `tau`): e' il punto fisso DETERMINISTICO, che
  varrebbe se la direzione della coppia fosse coerente. **Non lo e'.** La traiettoria misurata
  (`csv/_test_fork/_crescita_omega.py`, 150 passi, 15 punti) dice che `|omega_s|` cresce come
  **`sqrt(n)`** (`omega/sqrt(n)` costante entro il **4.6%**, mentre `omega/n` varia di 3.5x): e' un
  **RANDOM WALK SMORZATO**, e il suo equilibrio e'
  **`omega_eq = |F| * sqrt(dt_n * tau / 2)`, cioe' proporzionale a `sqrt(tau)`, non a `tau`**.
  Misurato: previsto 7.06e4, osservato 7.27e4 al passo 150 (scarto x1.03), con la decelerazione
  visibile (x1.138 da n=100 a n=150 contro x1.225 del puro sqrt(n)).
  **LA CONCLUSIONE RESTA:** omega cresce con la memoria (come `sqrt(tau)`), la memoria vive sulla
  VELOCITA' ANGOLARE e conserva la ROTAZIONE, non la DIREZIONE, e il plateau vale comunque
  **112 giri per passo**. **L'ipotesi "dare memoria combatte il disordine" e' REFUTATA.**
  **E LA DISSIPAZIONE NON MANCA: c'e', e' efficace, e un plateau finito lo produce gia'.** Il
  problema e' DOVE sta quel plateau, e dipende dall'INGRESSO (coppia/inerzia), non dall'uscita.
  **L'ipotesi "dare memoria combatte il disordine" e' REFUTATA su questo canale.**
  NB: `--regime` NON serve a testare TAU_A: cambia TAU_A INSIEME a G_PH, _CALORE_INIT e SCUOTIMENTO
  (quattro interruttori insieme, contro par.1).
- **IL COEFFICIENTE DI GILBERT DAL FDT SI DERIVA (zero parametri) ED E' ~1e4 VOLTE TROPPO LENTO**
  (`doc/ANALISI_gilbert_fdt.md`, 2026-09-15). Dal rumore sul Bloch (riga 1847, `amp`):
  `D = 2*amp^2/dt`; imponendo che l'equilibrio di Langevin `<th^2> = D/(2 lambda)` coincida con
  quello di Boltzmann `<th^2> = 2kT/|B|` si ottiene `lambda = amp^2*|B|/(2*dt*kT)`. Con l'unica
  temperatura parameter-free del sistema (`kT = Lam`, l'energia del vuoto, da cui il rumore stesso
  e' costruito) **`Lam` SI CANCELLA**: `lambda = |B|/(2*dt)` = 3.47/tempo, cioe' un tempo di
  allineamento di **28.8 passi** — contro un rimescolamento misurato di **0.0030 passi**.
  **Il FDT non licenzia uno smorzamento sufficiente**, e metterne uno piu' grande significherebbe
  SCEGLIERLO (contro par.3) e mettere dissipazione senza fluttuazione: lo stesso errore, ribaltato.
  Controllo: l'equipartizione con `I=1e-6` darebbe `kT = 800` contro `Lam = 4.4e-5` (rapporto ~2e7)
  -> **non e' equilibrio termico ma equilibrio DINAMICO pilotato**, ed e' la ragione strutturale per
  cui il FDT non puo' fissare il coefficiente: accoppia una dissipazione a una FLUTTUAZIONE, e qui
  il termine dominante non e' una fluttuazione.
- **IL TEMPO DI DISSIPAZIONE E' FISSATO DA UN PAVIMENTO, non dalla densita'** (misurato 2026-09-15).
  Nella seconda meta' di un run `tau/DT` vale esattamente **250** = `TAU_A*0.05/DT`, cioe' il
  pavimento di `max(rho/rho_rif, 0.05)` (riga 1913). Stessa famiglia del pavimento `1e-6`
  sull'inerzia: alle scale simulabili **la regolarizzazione diventa il parametro fisico**.
- **⚠ CORRETTA il 2026-09-17 — `_tau` NON HA IL PUNTO FISSO CHE QUESTA VOCE GLI ATTRIBUIVA.**
  **La versione precedente diceva:** *«poiche' il riferimento e' la MEDIANA, per il nodo mediano
  `_dens/_dens_rif ~ 1` sempre... e' un punto fisso auto-normalizzante... far maturare il sistema
  non puo', PER COSTRUZIONE, accorciare la memoria del nodo tipico»*.
  **MISURATO** (`csv/_test_fork/_analisi7_assiomi.txt`, 4 semi, 300 passi, blob `a44adc31`):
  `tau_mediano/TAU_A` vale **0.3698 / 0.0629 / 0.8024 / 0.7475** — un **fattore 13 fra semi**,
  non 1.
  **PERCHE', ed e' scritto nella voce stessa che lo negava:** `_dens_rif = median(_dens[_dens >
  1e-6])` e' la mediana di un **SOTTOINSIEME** (il **78-88 %** dei nodi), non dell'insieme.
  Numeratore e denominatore vivono su **popolazioni diverse**, ed e' esattamente la condizione che
  il punto fisso di **C12** richiede e che qui **manca**. *(La stessa distinzione che
  `doc/ASSIOMI.md` A3 chiama «errore di popolazione» — qui col segno opposto: **salva** la legge
  invece di romperla, e la salva **per caso**.)*
  **CONTROPROVA, che e' cio' che rende la correzione conclusiva:** ricalcolando con la mediana su
  **tutti** i nodi, il rapporto vale **`1.000000` ESATTO su 4 semi su 4**. Il filtro e' l'**unica**
  cosa che separa i due casi.
  **COSA RESTA VERO:** il punto fisso **esatto** non c'e', ma il rapporto resta confinato entro un
  fattore ~16: l'ancoraggio e' **attenuato, non abolito**.
  **COSA NON E' PIU' SOSTENUTO:** la conseguenza operativa *«far maturare il sistema non puo', PER
  COSTRUZIONE, accorciare la memoria del nodo tipico»*. **Non e' dimostrato il contrario** — non e'
  stato misurato a tempi diversi — ma **la DIMOSTRAZIONE su cui poggiava non regge.**
  **E IL PAVIMENTO `0.05` NON E' «QUASI TUTTI I NODI»:** misurato **19.58 %** in media (8.8-45.3 %)
  a 300 passi. Il **250 = TAU_A*0.05/DT** citato altrove in questo paragrafo riguarda la **seconda
  meta'** di un run: e' un'altra misura, e **non si trasporta a questa senza dirlo.**
  **LEZIONE DI METODO, ed e' la ragione per cui la voce sbagliata e' sopravvissuta due giorni:**
  la voce **citava il filtro** `[_dens > 1e-6]` e **concludeva comunque** per il punto fisso.
  L'argomento algebrico era stato scritto **guardando la forma** `x/median(x)` e **non l'espressione
  effettiva**. E' P1 applicato al proprio testo: **un'identita' algebrica va verificata sul codice
  che gira, non sulla sua forma ricordata.**
- **`correzione` HA DUE TERMINI, NON UNO** (righe **1895-1901**, verificato 2026-09-15):
  `correzione = cross(B, nb)`, e **se `CAMPO_SPINORIALE`** (ATTIVO in tutti i run del fork)
  `correzione += cross(_nb_grav(), nb)` — il torque verso il Bloch del **campo emesso spinoriale**.
  **Chi ricostruisce la catena di `omega` fuori dal simulatore e ne dimentica uno calcola meta'
  coppia** (successo il 2026-09-15: il residuo non spiegato valeva ~2.8 volte il deterministico).
  NB per la ricostruzione: `B` e' costruito da `nb_vic = self._nb_prec` (riga 1854), cioe' il Bloch
  **committato**, mentre il `nb` del prodotto vettore e' quello **DOPO** il rumore di riga 1847.
- **VERDETTO DEL TRACING DI `omega` (2026-09-15, `doc/TRACING_omega.md`): ESITO (I), NESSUN BUG.**
  La formula d'ingresso e' **giusta**: `coppia/inerzia` ha pendenza trasversale **-1.056** con
  `r = -0.981` su 2781 nodi — esattamente il `-1` che la legge richiede, e viene **tutto** dalla
  divisione per l'inerzia (la coppia da sola e' **piatta**, -0.056). Ma `theta` ha **-0.113**:
  **l'esponente si perde A VALLE**, nel rilassamento, attraverso `sqrt(tau)`.
  Esclusi per misura: (II-a) `|B|` **decresce** (-0.534), non cresce; (II-b) l'angolo `(B,nb)` e'
  **piatto** (-0.006, `r = -0.025`, mediana 59.4 gradi); (IV) `R_stoc = 0.041`, **sotto** l'errore
  atteso della ricostruzione (0.097) -> il rumore e' **marginale**, non guida `omega`.
  E il termine dissipativo **non domina**: rapporto coppia/dissipativo **= 188.9**.
- **LA CATENA `pendenza(theta) = pendenza(sigma) + pendenza(tau)/2` CHIUDE, ma solo A TEMPI LUNGHI**
  (2026-09-15, `doc/BARRE_ERRORE_pendenze.md`). Lo scarto fra attesa e misurata **CALA di due ordini
  col tempo**: **0.979** al passo 50 -> **0.010** al passo 400 (pendenza su `log(passo)`: **-0.412**).
  **E' un TRANSITORIO, non un termine mancante:** `tau ~ 4425-6500 passi` mentre i run ne hanno
  300-400, quindi il sistema ha vissuto **meno di un decimo** di un tempo di rilassamento, e la
  formula vale **all'EQUILIBRIO**.
  **DOPPIA CORREZIONE, entrambe mie, entrambe dello stesso giorno:** prima avevo scritto che la
  catena chiudeva (scarto 0.037); poi che NON chiudeva (0.338) **attribuendolo ai 20 nodi**; en-
  trambe le letture erano parziali. **A parita' di passo le due strade di misura di `tau` CONCORDANO**
  (passo 300: diretta +1.176 su 2195 contro indiretta +1.178, scarto **0.002**; passo 400: +1.812 su
  20 contro +1.867 su 2781, scarto **0.055**). **La differenza e' il PASSO, non il campione.**
- **⚠ `STEP2_OROLOGIO` E' ON DI DEFAULT dal 2026-09-16 (prima promozione eseguita, par.10).**
  **CONSEGUENZA OPERATIVA CHE VALE PER OGNI SCRIPT: l'ASSENZA di `--step2-orologio` NON significa
  piu' OFF, significa ON.** Il braccio OFF si ottiene **solo** con **`--senza-step2-orologio`**
  (nell'osservatore: **`--senza-step2`**), ed e' un **DIAGNOSTICO, non fisica alternativa**.
  `--step2-orologio` resta accettato come **NO-OP dichiarato** (stampa un avviso), per non rompere
  comandi e script gia' scritti.
  **PERCHE' E' UN PRESIDIO E NON UNA NOTA:** il sigillo `_sigillo_step2.py` prendeva il braccio OFF
  **per omissione del flag**. Se non fosse stato adeguato nello stesso commit, **`S2` avrebbe
  confrontato ON contro ON** e sarebbe **PASSATO SEMPRE** — un falso PASS esattamente della classe
  gia' catalogata qui (*«`max|A-B| = 0.000e+00` puo' significare "nessun confronto"»*), **e stavolta
  con le shape UGUALI**, quindi invisibile anche alla guardia delle shape. Adeguati nello stesso
  commit: `csv/_seal_fork/_sigillo_step2.py` e `csv/_test_fork/_osserva_vuoto.py`.
  **REGOLA GENERALE CHE NE DISCENDE: quando si ribalta un default, si cercano nello stesso commit
  TUTTI i punti che ottenevano il vecchio comportamento per OMISSIONE.** Un default ribaltato non
  rompe niente rumorosamente: **converte i rami di controllo in duplicati del ramo di prova.**

- **`TW_SPINORE` RESTA SPENTO PER DECISIONE DI LUCA (2026-09-16), E IL SUO COMMENTO E' FALSO.**
  Il commento (`:705-709`, `:2146-2148`) dice che la torsione *«pilota il Bloch di `tw/2`»*, cioe' un
  **ANGOLO**. **Il codice (`:2149-2154`) somma `tw/(4 pi)` a `omega_new`, che e' una VELOCITA'
  ANGOLARE** (`theta = |omega|*dt`, `:2210` e `:2296`): l'angolo effettivo e' **1.564e-03 rad/passo**
  contro i **9.827e-01** dichiarati, **fattore 628.3 = 2 pi / DT** — *un'unita' di misura mancante,
  non un'approssimazione*. E il termine finisce in **`self.omega_s`** (`:2313`), la **memoria
  persistente**, mentre il commento di `SYNC_SPINORE` (`:724`, `:2157-2160`) dice, **dello stesso
  blocco**, che metterci un torque *«darebbe accumulo/divergenza»*. **Unico fra i termini del blocco,
  `_otw` NON e' diviso per l'inerzia.**
  **CHI VOLESSE RIACCENDERLO LEGGA PRIMA `doc/REFERTO_tw_spinore.md`**: accenderlo **non** aggiunge
  la legge che il commento descrive. *(Stessa classe di `VERSO_CHI`, muto sotto `CHI_CORE`: un flag
  che non fa cio' che dichiara e' peggio di un flag assente.)*
  **E NON E' ARCHIVIATO COME «TRASCURABILE»:** il peso in **ampiezza** e' **0.054 %**, ma la domanda
  e' **DIREZIONALE** — l'asse TW e' **fisso e persistente**, `omega` e' un **random walk**. L'argomento
  di ampiezza su una domanda di correlazione **e' l'errore gia' fatto su `cs` allo 0.023 %**, e vale
  **anche al contrario**. **Resta il fronte `W` del registro.**
  **NESSUN SIGILLO E' STATO SCRITTO, di proposito:** il suo criterio naturale verrebbe **dalla
  descrizione invece che dal codice**, e sarebbe il **quarto** criterio stale in due giorni.


---

## `salva_stato`

*(oggi a `soliton_simulator.py:4617` - **misurato dall'AST**. lo snapshot su disco, e l'archivio a serie.)*

- **`conc_nodi`/`conc_archi`/`masse_info` NON FINIVANO NELLO SNAPSHOT — CURATO il 2026-09-18**
  (blob `a1ae5090` -> **`b9e07c73`**, `doc/REFERTO_coorti_snapshot.md`, sigillo
  `csv/_seal_fork/_sigillo_coorti.py` **9/9 PASS**). Il filtro di `salva_stato` (`:2865-2866`) accetta
  `ndarray`/scalari/`str`; **`conc_nodi` e `conc_archi` sono `list` e `masse_info` e' un `dict`: non
  matchavano, e venivano SCARTATI IN SILENZIO** — mentre la docstring della funzione dichiara
  *«salva TUTTE le grandezze di stato ... cosi' non ne dimentica nessuna»*. **Dopo un salva/ricarica
  il lignaggio delle coorti ripartiva VUOTO.** **Cura: si aggiungono ESPLICITAMENTE dopo il ciclo su
  `__dict__`; IL FILTRO NON SI ALLARGA** (allargarlo farebbe entrare le cache derivate `_S`, `_perm`,
  `_ker_cache`, **che `carica_stato` INVALIDA apposta**). **CATEGORIA D del par.10: nessun flag.**
  **⚠ E LA META' DEL MANDATO CHE NON SERVIVA:** l'**eredita' alla mitosi c'era GIA'** (`:3951-3954`,
  copia profonda dal genitore `a`; ramo Schwinger `:4076-4082`; `conc_archi` riallineato
  `:3997-4001`). **`:1858` — l'`extend` con liste vuote — e' in `semina()`, NON in `mitosi()`, ed e'
  CORRETTO li'.** **Misurato sui DUE bracci: frazione di nodi con coorte non vuota `0.8238` contro
  `0.8238`, identica** *(e' l'`82.4 %`, **non** il «~100 %» atteso: il complemento sono i nodi
  **seminati**, che per costruzione non hanno lignaggio)*.
  **⚠ COSA QUESTO NON DA': gli snapshot GIA' SCRITTI non acquisiscono le coorti retroattivamente.**
  I sei `.pkl` di `_gvideo` e i sei di `_g2m` vengono dal blob `a1ae5090`: **per averle servirebbe
  rigirare le scene.** **E il costo a `n = 8000` NON E' MISURATO:** `S5` da' **`+25.6 %`** sul `.pkl`
  a `n = 454`, e **il tempo non si legge** (due esecuzioni: `x1.0051` e **`x0.9245`**, cioe' il nuovo
  *piu' veloce* del vecchio — **rumore di sistema su 60 passi**).
- **ARCHIVIO A SERIE — `--db-serie` e `--db-rigioca` (2026-09-19, sigillo 12/12 sul blob `7c4dec1d`).**
  `--db-serie` NUMERA gli snapshot (`<stem>_000250.pkl`) invece di sovrascriverli; `--db-rigioca DA A`
  ricarica lo snapshot `DA` e rigioca fino ad `A` **INFITTENDO** l'archivio, **senza sovrascrivere**
  cio' che esiste (salta e conta). Con path `.gz` lo snapshot e' compresso a **livello 1**.
  **Entrambi OFF di default. NON sono fisica** (`doc/COMPONENTI_PROMOSSE.md` **G**): sono
  **infrastruttura di persistenza**, e il par.10 non si applica perche' il par.10 governa **leggi**.
  **`V1`/`V2`: 97 campi byte-identici** contro il codice pre-archivio e fra ON e OFF.
  **⚠ IL DISCRIMINANTE PER RIFIUTARE UNA SERIE E' IL BLOB, NON LA CADENZA**, e il perche' e' un
  errore gia' fatto: il primo criterio pretendeva la **contiguita'** dei passi e **rifiutava proprio
  il caso d'uso di `--db-rigioca`** (infittire = cadenza piu' piccola = serie non contigua).
  **Cadenze diverse nella stessa serie sono LEGITTIME: e' il senso dell'archivio.**
- **`gzip` SU QUESTI DATI COMPRIME `1.76x` E BASTA, ed e' IL LIMITE DEL DATO** (float64 densi;
  misurato su uno snapshot vero da 27.73 MB, `csv/_seal_fork/_costo_archivio_2026-09-19.txt`).
  Il livello **9** — che e' il **default di `gzip.open`**, mai scelto da nessuno — costa **4.42 s**
  per snapshot contro **0.82 s** del livello 1, per il **2 %** di spazio in piu'. **Cablato il
  livello 1** (decisione di Luca). **E questo numero CHIUDE la proposta ibrida `pickle`+HDF5:**
  HDF5 comprimerebbe gli stessi byte con gli stessi algoritmi.

---

## `_cs_nodo`

*(oggi a `soliton_simulator.py:4734` - **misurato dall'AST**. la velocita' delle onde metriche per nodo (`cs_floor`).)*

- cs = CS_M/(1+GAMMA*sqrt(I)) (riga 2187, `cs_floor`): vive SOLO nel settore metrica/gravita', MAI
  nell'orologio/EM. VERIFICATO dal sorgente il 2026-09-13.
- **⚠ SUPERATA il 2026-09-18 — `cs` E' VIVO: `cs_std/cs = 17.6 %`, non `0.0086-0.24 %`.**
  **MISURATO** (`doc/REFERTO_gauge_vuoto.md` par.1, `csv/_test_fork/_gauge_vuoto.py`, blob
  `f8f46683`, 1 seme, 120 passi, ramo 4pi): `cs/CS_M` ha **mediana 0.8265**, `p05` **0.528**, **min
  0.283**; **`cs_std/cs` per passo vale 17.6 %** (min 16.6 %, max 19.4 %), e la frazione con
  `cs/CS_M > 0.99` e' solo il **6.3 %**.
  **La voce qui sotto dice, come fatto stabile, «sempre sotto l'1 %»: e' superata di un fattore
  ~2000 rispetto allo 0.0086 % e ~73 rispetto allo 0.24 %, ed e' SOPRA la soglia dell'1 % di
  DICIASSETTE volte.** La voce resta scritta perche' dice **com'era** e **a quale blob**: e' un'
  informazione, non un errore (stessa convenzione dei marchi storici dello Strato 1).
  **PERCHE', dal codice e non da una congettura:** la cura di `cs_floor` del 2026-09-16 (categoria D,
  nessun flag) ha sostituito la scala **ASSOLUTA** `1/GAMMA^2 = 400` con la scala **RELAZIONALE**
  `_Lam = mean(I)` (`:2914`, `:2921`). Con `400`, `I ~ 1e-7` dava `sqrt(I/400) ~ 1e-5` e **`cs` era
  inchiodato a `CS_M`**; con `mean(I)` il rapporto `I/mean(I)` e' **O(1) per costruzione, a
  QUALUNQUE densita'**.
  > **`cs` non e' vivo perche' il sistema e' maturato: e' vivo perche' la SCALA e' diventata
  > relazionale.** **Una correzione di difetto senza flag ha riaperto un fronte che il registro dava
  > per chiuso «alle densita' simulabili».**
  **⚠ E COSA QUESTO NON DICE:** **non** dice che `tau = d/cs` sia **fisicamente distinguibile** da
  `tau ∝ d` nei run veri — quello richiede il **confronto**, non la dispersione. Dice che **la
  premessa che lo escludeva e' caduta**. **Il giudizio «il braccio ON non testa il tempo-luce» VA
  RIFATTO**, e con esso la parte del fronte **A** che vi si appoggiava. **-> `Z39` del registro.**
  **LIMITE: un seme, 120 passi, una scena** — e il presidio sull'istante (poco sotto) vale anche qui:
  quel rapporto **cresce col tempo**, quindi va citato **con il passo a cui e' misurato.**

---

## `_bloch_ritardato`

*(oggi a `soliton_simulator.py:4789` - **misurato dall'AST**. lo STRATO 1: il Bloch ritardato, `alpha = 1-exp(-dt_n/tau)`.)*

- **`FORK_SU2_MEM` / `--fork-su2-mem` (STRATO 1, 2026-09-14):** la connessione `N_ij` si costruisce
  dai Bloch RITARDATI `self._nb_ret` invece che da quelli correnti. Metodo `_bloch_ritardato()`;
  stato per-nodo `_nb_ret` (ereditato dalla mitosi in `_eredita_spinore_figli`), cache
  `_cs_nodo_prev` e `_r_corrente` **scritte solo col flag ON** (da cui dipende la byte-identita'
  di S1: se un giorno servissero a ramo spento, il sigillo S1 va rifatto). Richiede `--fork-su2`;
  da solo viene IGNORATO con avviso. VERIFICATO dal sorgente sul blob 2277e9a0.
  **✅ MARCHIO TOLTO IL 2026-09-16 — `tau` SEGUE `cs`, MISURATO. Il sigillo e' ora 25/27 PASS + 2
  FAIL ATTESI** (`csv/_seal_fork/_sigillo_strato1_risigillo_2026-09-16.txt`, blob `08784685`,
  **con `--cs-dinamico`**). Il marchio qui sotto e' **storico**: si legge per sapere **com'era** e
  **cosa lo ha tolto**, non come stato attuale.
  **COSA LO HA TOLTO: il SIGILLO 8, scritto apposta perche' rilanciare il sigillo com'era NON
  SAREBBE BASTATO.** Nei test in-process `_cs_nodo_prev` era `None` o `np.full(nodi, cs)`, cioe'
  **COSTANTE**: un `cs` costante non esercita `tau = d/cs`, lo rende indistinguibile da `tau ∝ d`.
  S8 da' a quattro nodi **`cs = 1, 2, 4, 8`** con **tutto il resto identico** (stessa `d`, `r = 1`
  su tutti — l'**opposto esatto** di S7, che varia `r` e tiene `cs` fisso):
  * **S8** `alpha = 1-exp(-dt_n*cs/d)` per nodo -> `max|alpha_mis - alpha_atteso| = 2.550e-15`;
  * **S8b** rapporto `cs=8 / cs=1` = **7.660686976** misurato = atteso — **se `cs` fosse ignorato
    varrebbe ESATTAMENTE 1.000000000**, come il `r=2/r=1` col bug del `DT` nudo;
  * **S8c** `|rapporto - 1| = 6.661`; **S8d** controprova con `cs` COSTANTE -> `alpha` uguale per
    tutti (`3.816e-16`), cosi' S8 non puo' passare per un artefatto dello slerp.
  **I DUE FAIL SONO S1a/S1b, PREVISTI E COMMITTATI PRIMA** (`doc/PREDIZIONE_risigillo_strato1.md`,
  commit `2853b36`): fra il blob di riferimento `968fba34` e `08784685` c'e' **C11**, che **non e'
  gated su `FORK_SU2_MEM`** — nel codice nuovo l'orologio a 4pi e' attivo, nel vecchio era inerte
  al 95.33 %. Due orologi -> due `r` -> due `dt_n` -> traiettorie diverse -> `N` diverso (**3096
  contro 3020, 32 array su 32 con shape diversa**). **Il `max|A-B| = 0.000e+00` stampato accanto a
  quei FAIL e' MANCANZA DI CONFRONTO, non identita'.** **NON e' una regressione: e' una cura che ha
  fatto il suo mestiere.** **E il sigillo si cita cosi': «25/27 PASS + 2 FAIL ATTESI», MAI «23/23».**
  **⚠ E COSA S8 *NON* DICE:** che `tau = d/cs` sia **fisicamente** distinguibile da `tau ∝ d` nei
  run veri. **Non lo e'** (C13: `cs_std/cs` fra **0.0086 %** e **0.24 %**, sempre sotto l'1 %).
  **S8 prova che la LEGGE e' cablata e viva; C13 dice che alle densita' simulabili quella legge ha
  poco da dire.** Due affermazioni diverse, nessuna sostituisce l'altra.
  **Sullo stesso ri-sigillo e' emerso un difetto grosso: vedi la voce «IL SIGILLO SI SCHIANTAVA».**

  **⚠ MARCHIO STORICO (2026-09-15, rilievo di Luca, verificato dal disco) — TOLTO il 2026-09-16,
  vedi sopra: il sigillo 23/23 dello STRATO 1 NON AVEVA MAI ESERCITATO LA DIPENDENZA DA `cs`.** L'argv di `_sigillo_strato1.py` (righe 380-386)
  **non contiene `--cs-dinamico`**, quindi `cs = CS_M` costante e `_cs_nodo_prev` non veniva scritta:
  il ritardo girava su **`tau = d/CS_M`**. E vale **due volte**: quel sigillo e' del blob `2277e9a0`,
  **precedente alla cura della cache**, quindi anche col flag acceso la cache sarebbe stata
  **scartata a ogni mitosi**.
  **COSA RESTA VALIDO:** il **meccanismo** del ritardo (slerp geodetico, `alpha = 1-exp(-dt_n/tau)`)
  e **S7**, che misura il rapporto `r=2 / r=1 = 1.9753` — quel rapporto dipende da **`r`**, non da
  `cs`, quindi il presidio sul tempo proprio **tiene**.
  **COSA NON E' MAI STATO TESTATO:** che `tau` **segua `cs`**. Ed e' proprio la ragione per cui
  `tau = d/cs` sarebbe piu' principiato di `tau ∝ rho`. **Finora nessuno l'ha vista funzionare.**
- **IL SIGILLO DELLO STRATO 1 SI SCHIANTAVA DA UN GIORNO, E NESSUNO SE N'ERA ACCORTO PERCHE'
  NESSUNO LO AVEVA RIGIRATO** (2026-09-16, `csv/_seal_fork/_sigillo_strato1_CRASH_2026-09-16.txt`).
  `_bloch_ritardato` calcolava `tau = d/cs` **inline**; dal commit `f7051c3` (cablaggio di
  `--tau-luce`) la legge e' stata **estratta** nel metodo condiviso `_tempo_luce_nodo`, che
  `_bloch_ritardato` ora **chiama**. `FintaRete` — il guscio in-process del sigillo — espone i
  metodi del simulatore **UNO PER UNO**, quindi da quel momento gli mancava il metodo:
  `AttributeError` a S2, e **S2, S3, S5, S6, S7, S8 e S3b non giravano affatto**.
  **NON FALLIVA: SI SCHIANTAVA** — la modalita' piu' facile da non notare.
  **CONSEGUENZA PIU' FORTE DEL MARCHIO:** dal blob `f7051c3` in poi il «23/23» non era nemmeno
  **RIPRODUCIBILE**. **Un sigillo che non viene rigirato non protegge nulla.**
  **FRAGILITA' DI STRUTTURA, non caso singolo:** poiche' `FintaRete` elenca i metodi a mano,
  **qualunque estrazione futura** di un metodo dentro `_bloch_ritardato` o `_coppia_interferenza`
  rompera' il sigillo **allo stesso modo e in silenzio**. **Gli altri sigilli in-process non sono
  stati controllati per lo stesso difetto** (2026-09-16).

---

## `_tempo_luce_nodo`

*(oggi a `soliton_simulator.py:4947` - **misurato dall'AST**. `tau = d/cs`, e la cache `_cs_nodo_prev` da cui dipende.)*

- **`d/cs` E' PIATTO CONTRO L'INERZIA: pendenza +0.097** (`r = +0.351`, 2195 nodi; 2026-09-15,
  `doc/TAU_tempo_luce.md`). Quindi sostituire `tau = TAU_A*max(dens/dens_rif, 0.05)` (riga 1913) con
  il **tempo-luce `d/cs`** (lo stesso `tau` gia' cablato nello Strato 1) **romperebbe la
  cancellazione**: `theta` passerebbe da **-0.152** a fra **-0.69** (stima onesta, col residuo) e
  **-1.03** (stima naive). **MA L'AMPIEZZA NON RISOLVE:** `tau/DT` da **6500** a **66.5** passi, e
  poiche' `|omega|_eq ∝ sqrt(tau)` il fattore e' **0.101**: da **126.7 a 12.8 GIRI per passo**.
  **Un ordine di grandezza nella direzione giusta, e il settore resta ALIASATO. Non e' una cura.**
- **LA CACHE `_cs_nodo_prev` VENIVA SCARTATA A OGNI MITOSI — CURATO il 2026-09-15** (commit
  `43e9a47`, `doc/FIX_cache_cs.md`, sigillo `csv/_seal_fork/_sigillo_fix_cache.py` **5/5 PASS**).
  La cache e' scritta a fine passo con l'`n` di quel passo (riga ~2918); la **mitosi aggiunge nodi**,
  quindi al passo dopo la guardia `len(csp) >= n` falliva e `_tempo_luce_nodo` cadeva su
  `cs_nodo = CS_M`. Ne risentivano **due** chiamanti: `_bloch_ritardato` (**lo STRATO 1**, gia'
  sigillato 23/23) e il rilassamento sotto `--tau-luce`. Cura: il figlio **eredita `cs` dal padre**
  in `_eredita_spinore_figli`, **sesta voce della stessa convenzione** di `_nb`/`_nb_prec`/`_nb_ret`/
  `omega_s`/`_psi_spinor`/`_psi_prec` — zero parametri. Misurato: fallback **71.88% -> 0.00%**,
  passi con cache inusabile **24/30 -> 0/30**.
  **MA ATTENZIONE A COSA QUESTO NON DICE.** L'effetto FISICO della cura **non e' dimostrato**:
  su **3 semi** (`doc/FIX_cache_cs.md` par.7) `Delta` vale **-0.0445 / +0.0367 / -0.0635** — **segno
  NON concorde** — con `media -0.0238`, `SE 0.0307`, `t = -0.77`, e **`IC95 = [-0.156, +0.108]` che
  contiene lo ZERO *e* il `-0.120` dell'ipotesi "~meta'"**. **Tre semi non decidono: l'esperimento
  non ha potenza.** E' il fronte **P** di `doc/RAMIFICAZIONI.md`.
  **CORREZIONE DI UNA VOCE CHE AVEVO SCRITTO IO STESSO OGGI:** qui c'era scritto *"il difetto
  contribuiva il 16.9% del divario, `z = 3.16`"*, misurato su **UN** seme. **RITIRATO:** quel `z` usava
  la `SE` **interna a un singolo run** (~0.010) mentre la dispersione **fra semi, a codice invariato**,
  vale **0.030**. Era dispersione di run.
  **IL MIO ERRORE, da non rifare:** avevo argomentato che `cs` riparato varia solo dello **0.023%**
  (`min 1.99954`, `max 2.0`, `CS_M = 2`) e che quindi **non poteva** spostare la pendenza. **Avevo
  confrontato l'AMPIEZZA di una variazione con l'ampiezza di una pendenza.** Una pendenza trasversale
  non misura **quanto** una grandezza varia, misura **quanto la sua variazione e' CORRELATA** con
  l'ascissa: un fattore che cambia dello 0.02% ma **sistematicamente nella stessa direzione** lungo
  l'asse dell'inerzia **sposta la pendenza**; uno che cambia del 50% a caso non la sposta.
  **Argomento di AMPIEZZA su una domanda di CORRELAZIONE: e' l'errore, e si ripete facile.**
  Resta vero che `d` era vivo nel **100%** dei passi e che quasi tutto l'effetto della FASE 2 sta in
  `d` — i **6/7** di divario ancora aperto lo confermano — ma *"non puo' muoverla affatto"* era falso.
  **La cura resta giusta anche per una ragione indipendente:** `cs` e' quasi-costante **oggi**
  (par.6); il giorno in cui sara' vivo, una cache scartata a ogni mitosi sarebbe un difetto
  **grande**, e lo sarebbe **in silenzio**.
  NB — **la terza via di crescita dei nodi resta scoperta:** `semina()` (riga ~1600) **non** passa da
  `_eredita_spinore_figli`. In batch e' inerte (`semina_cont=False` di default, si accende **solo**
  dalla GUI, righe ~4610 e ~4753), quindi non tocca nessuna misura committata; registrata in
  `doc/RAMIFICAZIONI.md` sotto la voce **H** (percorso GUI).
- **IL TEMPO-LUCE `tau = d/cs` NON E' TESTABILE ALLE DENSITA' SIMULABILI — MISURATO, non dedotto**
  (2026-09-15, rilievo di Luca). Con `--cs-dinamico` **acceso** e la cache **riparata**:
  `cs ∈ [1.99893, 2.0]`, `cs_std = 1.72e-4`, cioe' **`cs_std/cs = 0.0086 %`** — **116 volte sotto**
  la soglia dell'1% sotto la quale `d/cs` e' indistinguibile da `d`. E dentro `tau`, `cs` pesa
  **0.00629 %** della dispersione (**1 parte su 15 898**).
  **CONSEGUENZA, e va detta cosi':** `cs` non e' quasi-costante *per caso*, e' **MORTO PER DENSITA'**
  (par.6, `I ~ 0.05` contro soglia `~400`). Quindi **`tau = d/cs` E' `tau ∝ d`**, e tutto il ramo di
  lavoro su `--tau-luce` e' — **in questo regime** — un ramo su **`tau ∝ d`**:
  **distanza contro densita'**, non tempo-luce contro densita'.
  **E' un confronto sensato e informativo, ma NON e' quello che il nome del flag dice.**
  **TRE COSE CHE NE DISCENDONO, da non rileggere male fra un mese:**
  * il braccio ON **non testa il tempo-luce**;
  * la giustificazione principale della sostituzione (`inerzia = T^2 = (d/cs)^2`, la causalita') vive
    sul **`cs` locale**: resta vera **in linea di principio**, **non e' esercitata** in questo regime;
  * il fix della cache `_cs_nodo_prev` era **giusto** (un bug e' un bug) ma **in questo regime muove
    lo 0.009%**: **non poteva spiegare nulla** — ed e' il motivo strutturale per cui il «16.9%» e
    l'«11.0%» sono caduti, al di la' della barra d'errore sbagliata.
  **QUANDO SARA' TESTABILE:** solo con **`cs` VIVO** — alta densita', oppure il **turbo su GAMMA**,
  che pero' e' un **esperimento** (`doc/COMPONENTI_PROMOSSE.md` C1), non fisica.
  **Cio' che NON dipende da `cs` e resta il valore vero dei quattro bracci: il GRADIENTE DI
  RISOLUZIONE**, `theta` da **~129** a **~39** giri/passo.

---

## `_coppia_interferenza`

*(oggi a `soliton_simulator.py:5019` - **misurato dall'AST**. la forza fra due nodi: e' qui che il trasporto e' SCALARE, quindi abeliano per struttura.)*

- Trasporto forza = SCALARE: `_coppia_interferenza`, **righe 2207-2208**
  (`np.conj(_a)*(mat(A)@_a) + np.conj(_b)*(mat(A)@_b)`, stessa A su a e b) -> abeliano per
  struttura. VERIFICATO dal sorgente
  sul blob 4fc7a794 il 2026-09-13. **La riga 2196 citata in passato era il DOCSTRING, non il codice**
  (la funzione inizia a 2192, il docstring occupa 2193-2200): errore da par.0, corretto.

---

## `mitosi`

*(oggi a `soliton_simulator.py:5871` - **misurato dall'AST**. la nascita di un nodo nuovo.)*

- `PLAST_MIT=0` in TUTTI i test committati: la "compressione" osservata e' il regime di default
  (dimezzamento d0=d/2, "compressione degenere"), NON la generazione di spazio (mai girata).
- **BILANCIO DEI TASSI (misurato, 2 semi, 4163 coppie, 2026-09-15):** `tau_dec` (decorrelazione di
  una coppia padre-figlio) = **0.63 passi** su ENTRAMBI i semi; `tau_mit` locale = 187 / 210 passi
  -> rapporto **295 / 335**. **Dominio della distruzione.** Il confondente geometrico e' ESCLUSO,
  non stimato: all'eta' 1, con chi gia' a 89.7, la distanza e' INVARIATA (0.540 contro 0.539) e
  l'arco diretto e' vivo al **100%**. Decorrelano da ADIACENTI e CONNESSI.

---

## `memoria_hebbiana_moto`

*(oggi a `soliton_simulator.py:6547` - **misurato dall'AST**. la memoria del moto: `scala_p`, `MEM_MOTO`, il filtro di portata.)*

- **`scala_p` E' CURATA (2026-09-20, `Z67`, sigillo 5/5, categoria D: nessun flag).** La scala di
  `ampiezza` in `memoria_hebbiana_moto` **non e' piu' `median(|dpozzo|)`** — che era **`A3`** e
  inchiodava **`median(ampiezza) = tanh(1) = 0.761594` PER COSTRUZIONE** *(misurato su 14 istanti
  su 14, scarto `2.3e-11`)*. **Ora e' il POZZO LOCALE `0.5*(phi_g[ii]+phi_g[jj])`**: un gradiente
  relativo, adimensionale e locale. **NESSUN PAVIMENTO, e non per fiducia: il rapporto e' `<= 2`
  PER COSTRUZIONE** *(`phi_g >= 0` -> `|phi_g[j]-phi_g[i]| <= 2*phi_arc`; max misurato `2` esatto)*.
  **`0/0` e' definito ZERO, dichiarato.** **CONSEGUENZA MISURATA: `sin2` non e' piu' saturo
  (`p95` da `1.000000` a `0.980561`) e il moltiplicatore di `beta` passa da `0.9928` a `0.8029`:
  `ZETA_VIR` era acceso e NON FRENAVA QUASI NULLA.**
  **⚠ `SCALA_P_MEDIANA` e' una costante DIAGNOSTICA senza flag da riga di comando**, di proposito:
  serve solo alla riduzione al limite del sigillo, e non deve poter essere accesa da un comando.
- **`MEM_MOTO` (2026-09-22, costante di modulo, `True` di default, NESSUN flag CLI).** Recinta
  **una sola riga**: `self.d0[mask] += self._sd0(proj, mask)`, cioe' il sito **`S08_proj`**.
  **Spenta, `proj` resta CALCOLATO** *(il ramo `if GRAV_BIFASE and len(proj)` ne usa la
  lunghezza)*, **`mem_mot` resta AGGIORNATO** *(e chi la legge altrove, come la proiezione
  trasversale di `:6016`, non se ne accorge)*, e **il pavimento `P3_dopo_proj` continua a
  girare**. **Si toglie SOLO il contributo a `d0`**, che e' cio' che una prova di spegnimento
  deve misurare.
  **⚠ NON si usa `MEM_HEBB = False` al suo posto:** spegne l'**intera** funzione. **MISURATO**
  dal sigillo di `G3` (`T6`): toglie **cinque** siti oltre la gravita' — `S08_proj`,
  `P3_dopo_proj`, `S12_coesione`, `P6_dopo_coesione`, `P7_dopo_4917`.
  **Perche' senza flag CLI:** si imposta **sul modulo** dalla rigiocata, come `GRAV_BIFASE` in
  `G3`, **cosi' il driver non cambia** — e una legge di questo peso non deve poter essere
  spenta per sbaglio da un comando.
- Ancora elastica verso LAM (riga ~3234): e' a CORTO raggio (filtro_portata=1-tanh(d/LAM)), fissa la
  scala LOCALE (materia legata), NON blocca l'espansione a grande scala.


---

## I PRESIDI DI LETTURA nati da questi fatti

> **Non sono fatti sul codice: sono modo di leggere una misura.** Stanno qui perche' sono nati **da** questi fatti; la regola che li copre vive al **posto 2** (`doc/PATTERN_DI_PROVA.md`) o fra gli **assiomi**.

- **PRESIDIO PERMANENTE — PRIMA DI LEGGERE UNA STATISTICA RIASSUNTIVA, CHIEDITI CHE VALORE
  AVREBBE SE NON CI FOSSE NIENTE** (il valore sotto ipotesi nulla). Costa due righe e ferma gli
  autoinganni piu' comuni. Casi reali gia' presi su questo repo:
  * `N = 3164 -> 3209` a 150 passi sembrava un effetto del fork: era rumore a 1e-16 amplificato dal
    caos (2026-09-13). Sotto ipotesi nulla, due run che divergono a 1e-16 danno ESATTAMENTE quello.
  * `max|A-B| = 0.000e+00` sembrava identita': era mancanza di confronto, 3209 nodi contro 3073
    (2026-09-14). Sotto ipotesi nulla di "nessun array confrontabile", il massimo di un insieme
    vuoto e' 0.
  * `spin_overlap = 0.5000` e `chi ~ 90 +- 39 gradi` NON sono numeri qualunque: sono **esattamente**
    i valori di direzioni di Bloch CASUALI (`<|<psi_i|psi_j>|^2> = (1+<cos chi>)/2 = 0.5`;
    `sin(chi)/2` ha media 90.000 e std 39.171 gradi). Chi li vede deve riconoscerli.
- **PRESIDIO — QUANDO SI APRE UNA DOMANDA NUOVA, RI-INTERROGA LE MISURE VECCHIE.** Una misura letta
  correttamente per la domanda di allora puo' essere DECISIVA per una domanda posta mesi dopo, e
  nessuno torna a chiedergliela. Caso reale: `spin_ovl = 0.5 (direzione random)` fu misurato e letto
  BENE a 800 passi (verdetto (B) abeliano = disordinato, `STATO:513`); ma diceva gia' che il fork
  SU(2) avrebbe cercato struttura su un substrato senza struttura, e quella conseguenza e' stata
  tratta solo il 2026-09-14. Non tutte le risposte arrivano da run nuovi.
- **PRESIDIO — UN PATTERN CHE SPIEGA TUTTO VA VERIFICATO CONTRO LA FONTE PRIMA DI SCRIVERLO.**
  Nel primo audit (2026-09-14) l'esecutore ha costruito un reperto inesistente ("il segnale era nei
  dati e nessuno l'ha visto") cercando un terzo episodio che completasse uno schema: bastava leggere
  `STATO:513` per intero per vedere che il segnale era stato visto e annotato. **L'entusiasmo per uno
  schema elegante e' una fonte di errore quanto la disattenzione.**
- **TRAPPOLA DI LETTURA (2026-09-14): `max|A-B| = 0.000e+00` puo' significare "nessun confronto".**
  Se due run divergono al punto di cambiare il NUMERO DI NODI, nessun array ha piu' la stessa
  shape, il confronto non ha nulla da confrontare e lo zero e' MANCANZA DI CONFRONTO, non
  identita'. (Misurato: Strato 0 = 3209 nodi, Strato 1 = 3073, 32 shape su 32 divergenti.)
  E' il gemello speculare del falso positivo del 2026-09-13. **Guardare SEMPRE prima la riga delle
  shape / del conteggio nodi.**
- **PRESIDIO — UN'IPOTESI CHE RIGENERA LA PROPRIA SCUSA NON E' UN'IPOTESI** (rilievo di Luca,
  2026-09-15, `doc/CRITERIO_omega_rho.md`). Se ogni volta che l'effetto atteso non si vede la
  spiegazione diventa "il ritardo e' piu' lungo di quanto credessi", e la grandezza che fissa quel
  ritardo **cresce insieme** a quella che si sta misurando, allora **aspettare non chiudera' MAI la
  questione**: il bersaglio si sposta a ogni misura. E' la forma classica della congettura
  **non falsificabile**, e si riconosce dalla FORMA dell'argomento, non dal suo contenuto.
  CASO REALE, preso su questo repo: "theta non scende perche' l'inerzia e' al pavimento" -> il
  pavimento si rilascia e theta non scende -> "perche' insegue con tau=250" -> passano 775 passi e
  theta non scende -> "perche' ora tau e' 5000". Tre scuse, ognuna generata dal fallimento della
  precedente, e `tau ∝ rho` con `rho` crescente: l'attesa **non converge per costruzione**.
  **PRESIDIO OPERATIVO:** quando una spiegazione e' temporale (un ritardo), il test che la decide
  **non deve contenere il tempo**. Si misura la relazione **TRASVERSALE**, a un solo istante, fra
  individui che in quel momento hanno valori diversi della variabile: se la relazione non c'e'
  **allo stesso istante**, nessun ritardo puo' spiegarla. E il criterio si scrive **prima**, con una
  soglia numerica, e **non si proroga**: se scatta, l'ipotesi si **RITIRA**, non si raffina.
- **PRESIDIO — `r^2` BASSO NON SIGNIFICA PENDENZA INCERTA** (2026-09-15). `SE_b = |b/r|*sqrt((1-r^2)/(n-2))`:
  il fattore dominante e' **`sqrt(n)`**, non `r`. Stessa pendenza e stesso `r = 0.32`: `SE` vale
  **0.108** con 20 punti, **0.0097** con 2195. Quindi una pendenza con `r^2 = 0.10` su 2195 nodi e'
  determinata a **+-0.01**. `r^2` basso dice che la relazione **spiega poca varianza**, non che la
  pendenza sia fragile. **Serve sempre `SE`, non `r`, per decidere se uno scarto e' significativo.**
- **PRESIDIO — UNA FORMULA PREDITTIVA SI VALIDA SUL CASO NOTO *PRIMA* DI USARLA PER ESTRAPOLARE**
  (2026-09-15). La relazione `theta = sigma + tau/2` sembrava confermata (scarto 0.037) finche' non
  si e' rifatta la misura di `tau` su un campione serio: **scarto 0.338**. Se avessi estrapolato
  senza ri-verificare, avrei predetto `-1.03` invece di `-0.69`.
  **NB (corretto il 2026-09-15 stesso):** avevo aggiunto qui il corollario *"una pendenza su 20
  nodi non e' una pendenza"*, citando `+1.812` contro `+1.176` come prova. **Quella prova NON era
  valida:** i due numeri sono a **passi diversi** (400 e 300), e a parita' di passo le due strade
  concordano entro 0.055. Il corollario resta una **buona prudenza** (un campione ridotto ha `SE`
  piu' grande, e infatti 20 nodi danno `SE = 0.108` contro 0.0097), ma **non era la causa di quel
  caso**, e citarlo come tale era un errore.
- **PRESIDIO — UN CRITERIO DI SIGILLO SI SCRIVE DA UNA MISURA, NON DAL PROPRIO MODELLO MENTALE
  DEL CODICE** (2026-09-16, dopo **tre** casi nello stesso giorno). Prima di fissare la soglia o
  la coppia di grandezze che un sigillo confronta, **si misura cosa fa davvero il codice** nel
  punto in cui il criterio guarda. Costa meno della spiegazione che si darebbe senza.
  **I TRE CASI, e la forma e' sempre la stessa:**
  * **`N3b`** — *«il ramo di fallback scatta <= 1 volta»* **in assoluto**: ma l'estensione su
    `semina()`/`nuova_massa()` e' **legittima** (voce **H**), quindi il criterio avrebbe prodotto
    un **FAIL su un comportamento corretto**;
  * **`M1b`/`M3`** — misurati **nel momento sbagliato**: subito dopo `mitosi()`, dove i figli
    **non hanno ancora** un `xi` e l'array e' **legittimamente corto**, perche' l'estensione
    avviene dentro `_passo_spinoriale`, cioe' all'inizio del passo **dopo**;
  * **`M3c`** — confrontato con la **coppia sbagliata**: la crescita attraverso `step()`, che e'
    **zero per costruzione** (i nodi nascono in `mitosi()`), contro i nodi nati. Stampava
    **«nodi nati 0»**, e un numero **impossibile** e' il modo in cui un criterio sbagliato si
    denuncia da solo.
  **UN CRITERIO SCADUTO CHE PRODUCE UN FAIL FALSO COSTA PIU' DI UN SIGILLO MANCANTE**, perche' si
  porta dietro **una diagnosi**: chi legge il FAIL cerca il difetto nel codice, e il difetto non
  c'e'. **E la soglia si deriva dal VALORE SOTTO IPOTESI NULLA, non si sceglie:** `|corr| < 0.15`
  era inventato; il nullo della correlazione campionaria di variabili indipendenti e'
  `sigma ~ 1/sqrt(3N)`, che su 110 coppie da' `3 sigma = 0.165`.
- **PRESIDIO — OGNI RAMO `else` / FALLBACK / `getattr(..., default)` SU UN PERCORSO FISICO VA
  STRUMENTATO CON UN CONTATORE: quante volte e' scattato?** Un fallback mai misurato e' un
  comportamento **sconosciuto**, e uno che scatta il 72% delle volte **non e' un fallback, e' il
  comportamento principale.** E' il gemello del presidio del "valore sotto ipotesi nulla": li'
  *"quanto varrebbe se non ci fosse niente?"*, qui *"quante volte questo ramo e' davvero quello che
  gira?"*. CASO REALE che ha generato la regola (2026-09-15): il ramo `else` di `_tempo_luce_nodo`
  scattava nel **71.88%** delle chiamate (23 su 32, cache inusabile in **24 passi su 30**) senza che
  nessun sigillo se ne accorgesse — perche' il ramo **non e' un errore**: e' il fallback legittimo
  per `--cs-dinamico` OFF e per il primo passo. Niente NaN, niente runaway, nessuna byte-identita'
  violata. **Un difetto silenzioso non si trova guardando se il codice sbaglia: si trova contando
  quale strada prende.**
- **PRESIDIO — SU QUESTO SISTEMA CAOTICO LA BARRA D'ERRORE DI UNA PENDENZA E' ~3 VOLTE LA `SE`
  INTERNA AL RUN** (misurato 2026-09-15, `csv/_test_fork/_controllo_semi.txt`). La stessa pendenza
  trasversale, **a codice INVARIATO**, cambia da seme a seme di **0.0302** (e 0.0286 sull'altro
  ramo), mentre la `SE` di campionamento **dentro** un singolo run vale **~0.010**. Quindi:
  **la `SE` interna e' la barra giusta per parlare di QUEL run, non del SISTEMA.** Per confrontare
  due run (due flag, due versioni del codice) il **valore sotto ipotesi nulla NON e' zero**: e' 0.03,
  e va misurato con piu' semi, non dedotto.
  CASO REALE che ha generato la regola: `Delta = -0.0445 +- 0.0141`, `z = 3.16` su **un** seme
  sembrava un effetto a 3 sigma. Su tre semi il **segno non e' nemmeno concorde**
  (-0.0445 / **+0.0367** / -0.0635), `t = -0.77`. **Un'ora di lavoro e tre documenti da correggere.**
  **CONSEGUENZA DA VERIFICARE, non ancora fatta:** tutte le pendenze committate in questo programma
  portano una `SE` interna, cioe' **una barra ~3 volte troppo piccola**. Le conclusioni gia' tratte
  sembrano reggere perche' gli effetti sono grandi (il **-1.056** del tracing, il **+0.097** di `d/cs`
  contro `-1`, il contrasto ON-OFF **-0.32** = 11 volte la dispersione), ma **vanno ricontrollate una
  per una contro 0.03, non contro 0.01.**
- **PRESIDIO — UNA GRANDEZZA NORMALIZZATA SULLA PROPRIA MEDIANA HA UN PUNTO FISSO: SU QUELLO NON SI
  MISURA NULLA.** Se `x = f / median(f)` e la mappa `x -> y` e' **monotona**, allora `median(y)` vale
  **una costante ESATTA**, sempre, qualunque cosa faccia `f`. Confrontare due configurazioni su
  quella mediana e' **come confrontare due termometri dopo averli azzerati ciascuno sulla propria
  lettura mediana**: si ottiene zero per costruzione, e lo zero non dice niente.
  **DUE CASI REALI, entrambi su questo repo:**
  * `_tau = TAU_A * max(_dens/_dens_rif, 0.05)` con `_dens_rif = median(_dens)` → `tau_mediano ~
    TAU_A` **sempre**, a qualunque maturazione (voce sotto);
  * `ritmo()`: `x = f/median(|f|)`, `r_normalized = r/r_unit` con `r_unit` = il valore a `x = 1`
    → **`median(r) = 1.0 ESATTAMENTE`**, con qualunque orologio. Il sigillo `S4` della cura di
    `_psi_spin_prec` confrontava proprio le due mediane e ha dato `z = 0.00`: **non "nessun
    effetto", ma "nessuna misura"**. L'unico numero informativo era la **dispersione**
    (`0.4421 -> 0.4257`, -3.7%, **un seme**, nullo non misurato → vedi il presidio su C10).
  **REGOLA: prima di confrontare una statistica riassuntiva fra due rami, controlla se il codice la
  ancora a se stessa.** E' il gemello del presidio del valore sotto ipotesi nulla: li' *"quanto
  varrebbe se non ci fosse niente?"*, qui *"questa grandezza puo' anche solo in linea di principio
  cambiare?"*.
- **PRESIDIO — UN DATO DEVE PORTARSI DIETRO LE PROPRIE CONDIZIONI. UN FILE CHE SI DISTINGUE DAGLI
  ALTRI SOLO PER IL NOME NON E' UN DATO: E' UN RICORDO.** Ogni CSV di misura deve portare, in ogni
  riga o in un blocco di testa: **il BLOB**, **il SEME**, e **TUTTI i flag che distinguono quel run
  dagli altri bracci dello stesso esperimento** — non solo quelli che si pensava contassero.
  **Non basta scriverli nel log:** il log si perde, il CSV resta.
  CASO REALE (2026-09-15, rilievo di Luca): il braccio OFF della prima misura del settore spinoriale
  ha 136 colonne e **sette** colonne di flag corrette (`FORK_SU2=1`, `FORK_SU2_MEM=1`,
  `KURAMOTO_SU2=0`, `STEP2=0`, `GAMMA_TURBO=1.0`, `SCUOTIMENTO=1`, `SYNC_UPDATE=0`) — **ma NON ha
  `TAU_LUCE`**, che e' l'**unica** variabile che distingue i due bracci di quell'esperimento, **ne'
  `CS_DINAMICO`**, ne' il blob, ne' il seme. I due bracci erano distinguibili **solo dal nome del
  file**. Il run **non era sbagliato** (il flag era davvero OFF, come doveva); era **non
  certificabile dai dati**.
  **E la diagnosi è stata fatta dal DISCO, non dalla memoria:** i CSV sono stati scritti alle
  `19:18:46`, la colonna e' stata aggiunta al codice alle `19:23:32` — **cinque minuti dopo**.
  *(Chi avesse "ricordato" che la colonna c'era avrebbe certificato un file che non la contiene.)*
  **COROLLARIO OPERATIVO:** quando si aggiunge una colonna di certificazione, **i dati gia' scritti
  non la acquisiscono**. O si rilancia, o si annota **esplicitamente nel documento** che la colonna
  manca e **da dove si deduce lo stato** — e un'annotazione dichiarata vale, una ricostruzione a
  memoria no. *(Nel caso reale: `CS_DINAMICO` off e' deducibile da `cs_std = nan` su tutti gli 11
  campioni, perche' la cache `_cs_nodo_prev` non viene scritta a flag spento. Deducibile, non
  scritto.)*
- **PRESIDIO — DUE SEMI SODDISFANO IL MINIMO DEL par.2.7 MA NON PERMETTONO DI STIMARE UNA BARRA
  FRA SEMI.** Con 2 semi la deviazione standard ha **UN grado di liberta'**, e `t(0.025, 1) = 12.706`:
  l'IC95 diventa ~**12.7 volte** la `SE` della media, cioe' praticamente inutilizzabile.
  CASO REALE (2026-09-15, `doc/REFERTO_4bracci_4pi.md`): `chi` materia e' **sotto 90 su entrambi i
  semi OFF** (89.778, 89.876) e **sopra 90 su entrambi i semi ON** (90.048, 90.084) — segno concorde,
  `z ~ 3.5` se preso ingenuamente. **Ma l'IC95 con 1 gdl e' largo 1.2 gradi e contiene lo zero.**
  **Il segno concorde su 2 semi non e' una prova: e' un'ipotesi da rifare con 4.** Con 4 semi
  `t(3) = 3.18`, quattro volte piu' stretto. **Per una barra FRA SEMI servono >= 4 semi.**
- **PRESIDIO — UNA SOGLIA SU UNA GRANDEZZA DI UN SISTEMA CHE CRESCE VA DICHIARATA CON L'ISTANTE IN
  CUI SI MISURA**, altrimenti si finisce per citare la piu' comoda. CASO REALE (2026-09-15):
  `cs_std/cs` — il rapporto che decide se `tau = d/cs` e' distinguibile da `tau ∝ d` — vale
  **0.0086%** al passo 50 (n~80), **0.096%** al passo 300, **0.19-0.24%** al passo 500:
  **venti volte in 450 passi.** Avevo registrato il primo valore come se fosse una proprieta' del
  sistema; era un'istantanea su 80 nodi appena seminati. Il margine sotto la soglia dell'1% e'
  passato da **116x** a **~4x**. La conclusione regge, **la sua forza no** — e poiche' la traiettoria
  e' **monotona crescente**, il regime **cambia con la maturazione**: il tempo-luce non e' «non
  testabile mai», e' «non testabile a 500 passi».
- **PRESIDIO — SI MISURA PER PROMUOVERE, SI DIMOSTRA PER ESCLUDERE** (audit di lettura chiesto da
  Luca, 2026-09-16, `doc/COMPONENTI_PROMOSSE.md` sezione **E**). Una misura dice *«questa legge
  produce un effetto»*; **non dice se ha senso.** `SPIN_LARMOR` produceva un effetto ed era
  **sbagliata**; il fattore `cs^-2` non ne produce quasi ed e' **necessario**.
  **CONSEGUENZA OPERATIVA: escludere una legge perche' «non produce effetto» NON E' UN ARGOMENTO.**
  Si deve dire **QUALE PROPRIETA' ROMPE** — antisimmetria su arco orientato, localita' (§4),
  zero-manopole (§3), un'identita' misurata — **e citarne il punto nel codice.**
  **E per questo le esclusioni per DIMOSTRAZIONE non si riaprono con una misura:** tornano in gioco
  solo se cade la dimostrazione, cioe' se quella proprieta' non e' piu' richiesta o se il codice
  cambia. E' la stessa distinzione che §5-quater impone gia' al registro dei fronti.
  **IL CODICE DI UNA LEGGE ESCLUSA NON SI CANCELLA MAI:** resta spento, ed e' **l'evidenza che
  spiega perche' esiste il suo sostituto** (`TW_SPINORE` esiste **perche'** `SPIN_LARMOR` fallisce:
  cancellare il secondo farebbe perdere il **perche'** del primo).

- **PRESIDIO — UN RISULTATO NULLO SI LEGGE SOLO INSIEME ALLA RISOLUZIONE CHE LO HA PRODOTTO**
  (2026-09-16, `doc/REFERTO_step2_U1.md`). *«L'IC95 contiene lo zero»* **non e' un risultato**
  finche' non si dice **quale effetto quel test AVREBBE potuto vedere**. E' la versione statistica
  del `max|A-B| = 0.000e+00` per **mancanza di confronto**: in entrambi i casi uno zero viene letto
  come informazione mentre e' **assenza di informazione**.
  **CASO REALE, nella STESSA tabella:** contrasto Step 2 ON/OFF, 4 semi appaiati — su `chi` la
  risoluzione e' lo **0.213 %** (il nullo dice **molto**: `chi` non si sposta di piu' di 0.19 gradi),
  su **`|<n>|` e' il 129 %** e sulla **coerenza di segno il 603 %** (il nullo dice **NIENTE**: la
  barra e' **piu' larga del valore**). **Ventidue righe tutte «contiene lo zero», e non significano
  la stessa cosa.**
  **REGOLA OPERATIVA: un risultato negativo si scrive come LIMITE SUPERIORE** — *«X non si sposta di
  piu' di Y»* — **non come «X non cambia».** E se il limite superiore e' piu' grande della grandezza
  stessa, si scrive **«non misurato»**, non «nessun effetto».
  **E la cura non e' sempre piu' passi:** dove la grandezza **vale gia' il suo nullo** (un Bloch
  medio di versori casuali, una coerenza che vale 0) la barra percentuale **non puo'** essere
  piccola. Li' servono **piu' SEMI**.

- **PRESIDIO — DURANTE UN RUN, NESSUN FILE DEL PERCORSO IN USO SI MODIFICA: non solo il simulatore,
  ma anche il DRIVER e ogni script che il processo ha importato** (regola di Luca, 2026-09-19).
  **Il mandato del 19/9 diceva «NON toccare il simulatore finche' il run non e' finito»: il DRIVER
  era in uso e NON era coperto**, e la patch della ripresa gli e' stata applicata **mentre il run a
  6000 passi girava** (poi ripristinata, `228eb07`). **E' rispettare la LETTERA superando
  l'INTENZIONE**, ed e' il modo in cui un vincolo scritto bene viene aggirato in buona fede.
  **LA PROVA DICE CHE STAVOLTA NON C'E' STATO DANNO, NON CHE FOSSE SICURO** (`23f783e`, **3/3**:
  ripartendo dal passo 1800 si riottiene **identico** lo snapshot 1860, scritto durante la finestra
  della patch; 113 campi confrontati, 0 diversi, e il controllo positivo ne trova 84 diversi contro
  un altro istante, quindi lo zero significa *identico* e non *criterio cieco*).
  **PERCHE' E' ANDATA BENE, e perche' non basta:** Python compila il sorgente **una sola volta**,
  all'avvio, e non lo rilegge; il `.pyc` del driver era del giorno prima e **nessuno lo importa**
  (viene solo eseguito come `__main__`); gli snapshot sono scritti **dall'immagine in memoria**.
  **MA SE QUEL DRIVER LEGGESSE UNA CONFIGURAZIONE A RUNTIME, O FACESSE UN RELOAD, LA STESSA MOSSA
  AVREBBE ROTTO UN RUN DA SETTE ORE E MEZZA** — e non ci sarebbe stato modo di accorgersene se non
  dai numeri, alla fine.
  **REGOLA OPERATIVA: finche' un run e' in corso, il file sul disco deve restare quello che lo ha
  lanciato.** Il punto **non** e' se il processo se ne accorge: e' che per tutta la durata del run
  il repo direbbe una cosa diversa da quella che sta girando. Se serve modificare uno strumento in
  uso, si lavora su una **COPIA** e si porta la modifica sul file vero **a run chiuso**.

---

## FATTI CHE NON RIGUARDANO IL SIMULATORE

- **IL 75 % DELLE VOCI DEI REGISTRI NON PORTA IL BLOB DEL CODICE CHE LE HA PRODOTTE — MISURATO**
  (2026-09-19, `csv/_blob_nelle_voci.py`, output `csv/_blob_nelle_voci_2026-09-19.txt`):
  **151 voci, 38 col blob (25 %), e 69 citano NUMERI DI MISURA senza blob.**
  `RAMIFICAZIONI` 36/119, `COMPONENTI_PROMOSSE` **0/23**, `INVENTARIO` 2/9.
  **Non e' un presidio: e' una MISURA** — non impedisce niente e **non verifica che il blob citato
  sia quello GIUSTO**, solo che ce ne sia uno. **Un presidio ATTIVO su prosa libera NON e' stato
  trovato**, e va detto invece di scrivere l'ennesima nota: ogni riga di prosa contiene numeri
  (date, percentuali, numeri di riga), e un controllo che segnala tutto non lo legge nessuno.


---

