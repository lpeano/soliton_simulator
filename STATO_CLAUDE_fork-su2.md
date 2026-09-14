# STATO PER CLAUDE — branch `fork-su2`

> File di continuità locale al branch, aggiornato a OGNI commit/push (regola Luca 2026-09-11).
> Serve a Claude per riprendere lo stato senza rileggere tutta la storia. Lingua: italiano.
> La doc canonica di tracing vive su `main`; questo è lo stato operativo del branch di sviluppo.

## BRANCH — il fork vive QUI (regola Luca 2026-09-13)
- **`fork-su2`**, creato da `dev-spinoriale` al commit **`c9fcc1e`** (blob `soliton_simulator.py`
  = **4fc7a794**, invariato al momento della biforcazione). Tracciato su `origin/fork-su2`.
- **Tutte le modifiche al `.py` per il fork SU(2) si fanno QUI, non su `dev-spinoriale`**, che
  resta la BASELINE intatta: se il non-abeliano demolisce, ci si torna in un secondo
  (`doc/ROADMAP_fork_SU2.md`, sezione PREPARAZIONE).
- Questo file e' il rename di `STATO_CLAUDE_dev-spinoriale.md` (un solo file di stato per branch,
  il nome dice quale). **ATTENZIONE AL MERGE:** se un giorno `fork-su2` rientra in
  `dev-spinoriale`, il rename cancellerebbe lo stato di quel branch — va risolto a mano,
  consapevolmente, non lasciato fare a git.
- **Il blob 4fc7a794 CESSA di essere il riferimento su questo branch** appena il PEZZO 1 tocca il
  `.py`. La precondizione "blob == 4fc7a794" scritta in `ROADMAP_dev-spinoriale.md` e nel
  gate-cache vale ancora per `dev-spinoriale`, NON per `fork-su2`: qui il gate va **ri-timbrato
  sul nuovo blob** (altrimenti il guard di `csv/_test_53c/_run_batch.ps1` blocca ogni campagna).

## Ultimo aggiornamento
- Data: **2026-09-14**
- Ultimo commit: **STRATO 1 — connessione con MEMORIA (`--fork-su2-mem`), sigillo 23/23 PASS**,
  + ri-timbro del gate in CLAUDE.md par.0.
- Branch: **`fork-su2`**, allineato con `origin/fork-su2`.
- Blob `soliton_simulator.py` = **2277e9a0** (verificato dal disco). Su `dev-spinoriale`: 4fc7a794.
  Storia dei timbri del branch: `b4c6c3f8` (PEZZO 1) -> `968fba34` (PEZZO 3) -> `2277e9a0` (STRATO 1).
- **GATE RI-TIMBRATO** in CLAUDE.md par.0 (era la condizione posta da Luca al PEZZO 3: "si
  ri-timbra quando i run cambiano davvero". Oggi cambiano). `csv/_test_53c/gate_cache.json` resta
  volutamente STALE su `4fc7a794`: la guardia di `_run_batch.ps1` rigira `_check_presidio.py` da
  sola al primo cache-miss. **Non si scrive un PASS a mano per un blob non verificato.**

## ⚑ STRATO 1 — FATTO, SIGILLO 23/23 PASS (2026-09-14). IL FORK NON E' PIU' INERTE.
**Questo e' il pezzo che accende il fork.** Lo Strato 0 era inerte per TEOREMA (vedi sotto): la
connessione costruita dagli stessi stati che trasporta, nello stesso istante, e' l'identita'
sull'overlap. La cura e' la **CAUSALITA'**, non una taratura: la connessione nasce dai Bloch a
`t-tau`, `tau = d/cs` (tempo-luce d'arco, zero parametri nuovi).

**Cablaggio** (flag `FORK_SU2_MEM` / `--fork-su2-mem`, OFF di default, richiede `--fork-su2`):
- `Rete._bloch_ritardato()`: rilassa il versore `_nb_ret` verso il corrente con **slerp geodetico**,
  `alpha = 1 - exp(-dt_n/tau)`. Si rilassa il **BLOCH**, non la matrice U/N (un blend lineare di
  matrici uscirebbe da SU(2), par.4). **Diverso da come era pianificato** in
  `doc/ROADMAP_fork_SU2.md` (`dU/dt=(U^Berry-U)/tau`, memoria della MATRICE): stesso effetto
  fisico, ma resta dentro SU(2) per costruzione invece che per correzione.
- stato per-nodo `_nb_ret`, **ereditato dalla mitosi** in `_eredita_spinore_figli` (senza, la
  memoria si azzererebbe a ogni nascita: misurato, con l'eredita' 2 reset su 34 chiamate).
- cache `_cs_nodo_prev` e `_r_corrente` **scritte solo col flag ON**: la byte-identita' di S1
  dipende da quel gating.
- in `_coppia_interferenza` il cablaggio e' **una riga**: `_nb_conn = _nb` (Strato 0) oppure
  `self._bloch_ritardato(...)` (Strato 1). Il TRASPORTO resta sugli spinori CORRENTI.

**FIX DI UN FRAME PREFERITO (il punto piu' importante della giornata).** La prima stesura usava
`alpha = 1 - exp(-DT/tau)`, col tic di COORDINATA globale. Ma `tau = d/cs` e' tempo PROPRIO:
rilassarlo con `DT` cancella la dipendenza dall'orologio locale, cioe' impone a un processo locale
la foliazione sincrona globale — **un frame preferito, un "etere"**, l'opposto di un sistema
relazionale. Ora `alpha = 1 - exp(-dt_n/tau)` con `dt_n = DT*r` (`self._r_corrente` esposto da
`step()`). **La radice l'ha vista LUCA**, non l'agent: il prompt di partenza diceva `dt = DT` e
nessuno dei sigilli S1..S6 l'avrebbe presa. Dell'agent e' **S7**, il presidio che impedisce il
rientro del bug.

**SIGILLI (csv/_seal_fork/_sigillo_strato1.py, output _sigillo_strato1_OUT.txt): 23/23 PASS**

| sigillo | misura |
|---|---|
| S1.0 riferimento = blob certificato PEZZO 3 | `968fba34` (commit FISSO `af003c2`, mai HEAD) |
| S1a fork ON + MEM OFF vs pre-Strato 1 | **0.000e+00** (assolve il plumbing in `step()`) |
| S1b baseline fork OFF vs pre-Strato 1 | **0.000e+00** |
| S2 tau->0 -> Strato 0 | **0.000e+00** (e `n_ret == n_cur`, 0.000e+00) |
| S3.0 controprova: Strato 0 e' inerte | 4.441e-15 |
| **S3 LA FORZA CAMBIA** | **9.931e+00 = 74.47% di \|coppia\|** |
| **S3b ... nel CICLO DINAMICO REALE** | mediana **0.170**, max **0.717** su 36 passi |
| S3b2 memoria non resettata dalla mitosi | 2 reset su 34 chiamate |
| S4 `\|n_ret\|=1` / `\|psi\|=1` / NaN / runaway | 2.220e-16 su 3073 nodi / 3.331e-16 / nessuno / max\|x\|=9.37 |
| S5 azione-reazione (ramo MEM) | sum = +6.439e-15 (max\|c\| = 9.312e+00) |
| S6 a riposo MEM == scalare | 5.329e-15 dopo 200 tic |
| **S7 il tic e' il TEMPO PROPRIO** | rapporto r=2/r=1 = **1.975309912** (col bug DT: **1.000000000**) |

**S7 in dettaglio — e' il sigillo che mancava.** Esercita il METODO VERO (`_bloch_ritardato`
chiamato, `alpha` RICAVATO dall'avanzamento geodetico di `n_ret`, non ricalcolato inline):

| r | alpha atteso (dt_n) | alpha misurato | alpha col BUG (DT) |
|---|---|---|---|
| 0.5 | 0.012422199506 | 0.012422199506 | 0.024690087972 |
| 1.0 | 0.024690087972 | 0.024690087972 | 0.024690087972 |
| 2.0 | 0.048770575499 | 0.048770575499 | 0.024690087972 |
| 4.0 | 0.095162581964 | 0.095162581964 | 0.024690087972 |

`max|alpha_mis - atteso| = 2.550e-15`. **S1..S6 passavano IDENTICI anche col bug**: senza S7 il
frame preferito sarebbe rimasto invisibile.

**⚠ TRAPPOLA DI LETTURA PRESA E CORRETTA OGGI (gemello del falso positivo del 2026-09-13).** Il
confronto fra i due run a 150 passi stampava `max|A-B| = 0.000e+00` e sembrava dire "il fork non
fa nulla". **Non lo diceva:** i due run finiscono con **3209 nodi (Strato 0) contro 3073 (Strato
1)**, quindi tutte e **32 le shape su 32** divergono, nessun array era confrontabile e lo zero era
**MANCANZA DI CONFRONTO, non identita'**. Lo script ora stampa PRIMA la riga delle shape.
Regola: **guardare sempre il conteggio nodi prima di leggere uno zero.**

**COSA QUESTO NON DICE (par.8, verbo onesto).** S3/S3b dicono che la forza CAMBIA, **non che sia
FISICA**. Rompere il teorema era garantito per costruzione. Olonomia `W(r)` non banale, stabilita'
su orizzonti lunghi, verso corretto per la gravita': li dice un **RUN**, e non sotto ~2000 passi
ne' su un solo seme (par.2.7). **Non dire "il fork funziona": dire "il fork non e' piu' inerte".**
Inoltre l'effetto e' proporzionale a quanto i Bloch cambiano ENTRO `tau` (a riposo S6 misura
5e-15), e `cs` e' quasi-costante alle densita' attuali -> `tau ~ d/CS_M`: il ritardo c'e', ma la
sua VARIAZIONE spaziale (la curvatura) e' debole finche' `cs` non e' vivo.

## ⚠⚠ REPERTO 2026-09-14 — I BLOCH NON HANNO DINAMICA PROPRIA. Il fork trasporta rumore.

**Test A/B a variabile singola** (`--regime deterministico` cambia SOLO `SCUOTIMENTO`, sigillato
O2), 300 passi, seme 1, osservatore sigillato pure-read (O1: `0.000e+00`). Entrambi i bracci con
`FORK_SU2=True FORK_SU2_MEM=True` verificato **dentro** il ciclo.

| | BRACCIO ON (scuotimento) | BRACCIO OFF (`--regime deterministico`) |
|---|---|---|
| chi materia | 90.04 +- 39.17 gradi | **0.00 +- 0.00** |
| chi vuoto | 90.06 +- 39.06 gradi | **0.00 +- 0.00** |
| chi p90 (densi) | 89.86 +- 39.11 gradi | **0.00 +- 0.00** |
| frazione chi < 10 gradi | 0.0076 | **1.0000** |
| \|<n>\| | 0.007 – 0.025 (~1/sqrt(N)) | **1.000000 esatto** |
| direzione <n> | casuale, cambia | **(0, 0, +1) esatto, immobile** |
| \|n_ret\| - 1 | 2.22e-16 | **0.00e+00 esatto** |

*(atteso per direzioni casuali indipendenti: 90.000 / 39.171 gradi, fr<10 = 0.0076)*

### IL VERDETTO — non e' nessuna delle due ipotesi previste

Non "lo scuotimento copriva la struttura", non "la dinamica non organizza". E' la terza:
**senza scuotimento i Bloch NON SI MUOVONO AFFATTO.** `|<n>| = 1.000000` su `(0,0,+1)` dal passo 1
al passo 300, mentre N cresce 80 -> 3567. Quello e' **esattamente la condizione iniziale**
(`soliton_simulator.py:1778`, *"nuovi nodi al polo"* = `[0,0,1]`). Non e' un collasso verso
l'allineamento: e' che **il sistema parte sul punto fisso e non se ne muove mai**.

**Perche' e' un punto fisso esatto:** se tutti gli `nb` sono uguali, il campo `B` dei vicini e'
parallelo a `nb`, quindi `cross(B, nb) = 0`, quindi `omega_new = 0`, quindi nessuna rotazione. E i
nodi nuovi nascono al polo, cioe' gia' dentro il punto fisso.

**ATTRIBUZIONE: 100% lo scuotimento.** La dinamica deterministica non contribuisce **nulla** alla
direzione dei Bloch — ne' ordine ne' disordine. Il campo di Bloch e' **puro rumore di vuoto**.

### ERA DOCUMENTATO NEL CODICE, e nessuno l'aveva collegato al fork

`soliton_simulator.py` lo dice in **quattro punti** (`:761`, `:1982`, `:4718`, `:5067`), a proposito
di `KURAMOTO_SU2`:
> *"nb **SI muove** (gravita' fisica, voluto: convergenza-dt, **non 6.7e-16**)"*

Cioe': **senza** `--kuramoto-su2`, `nb` si muove di ~6.7e-16 — arrotondamento, non fisica. E la
config certificata del fork **non ha mai avuto `--kuramoto-su2`**. Coerente con il resto del
disegno: `--deparam-orologio` e' esplicitamente costruito perche' l'orologio **non inclini** `nb`
(*"PURA FASE: l'orologio NON entra nell'asse di rotazione ... non tocca la gravita'"*), e
`--sync-fase-orologio` perche' *"nb [resti] invariante"*. Piu' meccanismi sono **nb-invarianti per
progetto**, e l'unico che muove `nb` non era acceso.

E' il secondo caso del presidio nuovo di `CLAUDE.md` par.9 (*"quando si apre una domanda nuova,
ri-interroga le misure vecchie"*): qui la risposta era nei **commenti del codice**, non in un run.

### CONSEGUENZA PER IL FORK (dura, e da non addolcire)

La connessione `N_ij` e' costruita dalle direzioni di Bloch. In questo sistema quelle direzioni
sono, nei due soli regimi possibili:
- **con scuotimento:** indistinguibili dal rumore bianco, **ovunque**, materia compresa;
- **senza scuotimento:** una costante, **zero informazione**.

In nessuno dei due c'e' struttura spaziale. E il W(r) del `PROTOCOLLO` non puo' discriminare in
nessuno dei due: con chi uniforme e' piatto per costruzione; con chi = 0 vale `W = 2` esatto
(`U = I` ovunque), cioe' abeliano banale. **La gobba sul bordo non e' misurabile su questo
substrato.**

Il cerchio con il teorema di inerzia: la connessione e' **uno specchio della materia**; i Bloch
della materia sono **rumore**; lo specchio riflette rumore. Lo Strato 1 ha rotto l'inerzia (23/23
PASS, dimostrato) — ma ha reso la connessione sensibile a un **passato anch'esso casuale**.

### COSA QUESTO NON DICE
300 passi, **un seme**, due bracci (par.2.7): ATTRIBUISCE la causa, non conclude sulla fisica. Non
dice che il fork sia sbagliato: dice che **il substrato su cui gira non ha struttura di Bloch in
QUESTA configurazione**. Esiste un flag documentato che muove `nb` per fisica (`--kuramoto-su2`);
accenderlo e' un meccanismo nuovo (par.1) e **una decisione di Luca**, non dell'esecutore.
Stabilita' perfetta su entrambi i bracci: nessun NaN, `|psi|-1` ~ 4e-16, `max|x|` ~ 9.4, niente runaway.

## PROSSIMA AZIONE (dopo lo STRATO 1)
1. **Run di fisica, non piu' sigilli tecnici**: >= 2000 passi, **piu' semi** (par.2.7), con e senza
   `--fork-su2-mem`. Prima domanda: **olonomia W(r)** secondo `doc/PROTOCOLLO_test_olonomia.md`
   (W != 2, non-commutante, gobba sul BORDO delle masse = non-abelianita' fisica emergente).
2. Controllare che `SYNC_UPDATE` e `SCUOTIMENTO` siano ATTIVI nella config del fork (lettura,
   gratis): senza, la degenerazione dei Bloch non si rompe.
3. Distribuzione degli angoli `chi` fra vicini nel tempo (sparsa = settore non-abeliano vivo;
   collassata su 0/pi = una forza di allineamento domina il rumore). Isotropia `<n>`.
4. **STRATO 2** (memoria hebbiana saturata) solo DOPO che lo Strato 1 ha un verdetto di fisica.
   Un pezzo, un sigillo, un flag OFF.
5. Prima della prossima campagna la guardia di `_run_batch.ps1` rigirera' `_check_presidio.py` sul
   blob nuovo: se FALLISSE, e' un problema da affrontare li', **non da mascherare timbrando la cache**.

## REGOLE E DOCUMENTI (aggiornamento 2026-09-13)
- **CLAUDE.md v2** e' l'istruzione autorevole (sostituisce `.github/copilot-instructions.md`, che resta
  solo come contesto storico). Novita' rispetto alla v1: par.0-bis (leggi le istruzioni a ogni avvio +
  rilettura dopo compattazione), par.5 politiche di commit (un commit = un cambiamento logico, forma del
  messaggio, commit anche del sigillo FALLITO poi STOP, niente `Start-Sleep`/polling), par.5-bis
  auto-manutenzione (CLAUDE.md per i fatti stabili, STATO a ogni commit, commit dedicato per le regole).
  Promosse in par.2/4 tre regole prima solo in copilot-instructions: snapshot/restore COMPLETO incluso RNG
  per la purezza pure-read; `--cs-dinamico` implica `--chi-core` e `--spinore-vivo`; mai confronti a passo
  fisso su sistema che si espande (aliasing).
- **Documenti di riferimento ora NEL REPO**, cartella `doc/` (prima esistevano solo nel Progetto/chat,
  assenti da tutti i branch e dalla storia git -> il par.0-bis non era eseguibile):
  `BUSSOLA_dev-spinoriale.md`, `BUSSOLA_TECNICA_dev-spinoriale.md` (v2), `ROADMAP_fork_SU2.md`,
  `PROTOCOLLO_test_olonomia.md`, `SYSTASIS_nota_concettuale.md`.
- **CONFLITTO D'ORDINE: RISOLTO (Luca, 2026-09-13) -> FORK-FIRST.** Vale CLAUDE.md par.6: si parte dal
  fork non-abeliano; GAMMA / Step 1A / Step 2 (cs<->orologio) / Step 3 (alpha_G) sono **A VALLE**
  (a densita' reali cs e' MORTO, I~0.05 vs soglia ~400 -> ogni test cs-dipendente oggi e' NULLO).
  Allineati di conseguenza: `ROADMAP_dev-spinoriale.md` (radice) marcata **SUPERATA** (rimandata, NON
  ritrattata: la matematica resta valida e si riprende dopo il fork) e la sua "PROSSIMA AZIONE"
  marcata SOSPESA; `doc/BUSSOLA_dev-spinoriale.md` riga 86, puntatore corretto a
  `doc/ROADMAP_fork_SU2.md` + nota che la sua lista 0-4 e' l'ordine STORICO, non di esecuzione.
- **ROADMAP VIVA = `doc/ROADMAP_fork_SU2.md`** (Preparazione -> PEZZO 1 -> PEZZO 2 -> PEZZO 3, un pezzo
  un sigillo). Il test di verifica e' `doc/PROTOCOLLO_test_olonomia.md`, da eseguire DOPO il sigillo di
  riduzione al limite (se non passa, misurerebbe un bug, non la fisica).
- **§9 RIVERIFICATO DA LUCA sul repo (blob 4fc7a794): sano tranne la riga gia' corretta.** Confermati
  dal disco: forza 2207-2208 ✓, cs 2187 ✓, omega_clk/`_phc`/dt_n NON usano cs ✓, chiamata
  `_passo_spinoriale` 2419 dietro SPINORE_VIVO ✓, ancora elastica 3234-3237 con filtro
  `1-tanh(d/LAM)` a 3224 ✓. L'unico sbaglio era 2196 (docstring citato come codice), gia' fixato.
- **COORDINAMENTO (regola Luca 2026-09-13): la CLAUDE.md AUTOREVOLE e' quella NEL REPO.** Le copie
  fuori dal repo sono indietro sul fix 2207-2208 e **NON vanno ripushate** (rimetterebbero l'errore).
  Le modifiche a CLAUDE.md le applica Claude Code nel repo; Luca fornisce il testo esatto.

## PEZZO 1 — FATTO, SIGILLO PASS (2026-09-13)
- **Aggiunta `Rete._link_su2(nb_i, nb_j)`** (staticmethod, subito dopo `_bloch_a_spinore`):
  `chi=arccos(n_i.n_j)`, `m_hat=(n_j x n_i)/|n_j x n_i|`, `U=exp(-i (chi/2) m_hat.sigma)`.
  Ritorna **(U, w)** con `w=|n_j x n_i|=sin(chi)` (il PESO del PEZZO 2, gia' calcolato qui perche'
  e' lo stesso prodotto vettore: non e' anticipare il PEZZO 2, il cablaggio resta al PEZZO 3).
- **Blob: 4fc7a794 -> `b4c6c3f8`** (su `fork-su2`; su `dev-spinoriale` resta 4fc7a794).
- **SIGILLO 1 (OFF = byte-identico): PASS per COSTRUZIONE, verificato strutturalmente.**
  `grep _link_su2` da UN SOLO risultato: la definizione. **Nessun call-site** -> la funzione non
  puo' alterare l'esecuzione. Diff = **50 righe inserite, 0 rimosse, 0 modificate**. Questa e' una
  prova LOGICA (piu' forte di un run A/B, che campiona una sola traiettoria); se si vuole anche la
  prova empirica, il run A/B contro `git show cebaee3:soliton_simulator.py` resta da fare.
- **SIGILLO PEZZO 1: 17/17 PASS** — `csv/_seal_fork/_sigillo_pezzo1.py` (pure-read, exit 0/1):
  S1 allineati -> U=I **esatto** (max|U-I|=0.000e+00) e w=0 ; S2 unitarieta' 5.6e-16 ;
  S3 det U=1 4.5e-16 (e' SU(2), non U(2): la fase U(1)/EM resta separata) ; S4 U_ji=U_ij^dag
  **esatto** ; S5 trasporto |<psi_i|U_ij|psi_j>|=1 (5.6e-16 su 20000 archi) ; S5b Bloch
  trasportato = n_i (1.9e-14) ; S6 antipodali: no NaN, w=0, U unitaria, contributo pesato **0** ;
  S7 w=sin(chi) esatto (1.1e-16), continuo, nessuna soglia ; S8 pure-read (RNG non consumato,
  input non mutati) ; S9 **[U1,U2] = 1.0e+00 != 0** = la non-commutativita' c'e' davvero.
- **FATTO GEOMETRICO DA NON DIMENTICARE (verificato, S5b):** con `m_hat = (n_j x n_i)` la matrice
  `U_ij` trasporta **n_j -> n_i** (NON n_i -> n_j: l'intuizione inganna). E' esattamente il verso
  che serve a `Im<psi_i| U_ij |psi_j>`: porta psi_j fino al sito i, poi confronta con psi_i.
  La formula della BUSSOLA e l'uso nella forza sono coerenti. Invertendo l'asse si otterrebbe
  U^dag e la forza cambierebbe segno: **l'orientamento dell'arco ora CONTA** (con gli scalari no).

## DECISIONI DI LUCA (2026-09-13, dopo verifica indipendente del PEZZO 1)
Luca ha verificato il PEZZO 1 dal DISCO, non dal resoconto: branch, blob, assenza di call-site, e
ha **rigirato lui stesso il sigillo (17/17 PASS, exit 0)**. Confermato anche che `dev-spinoriale`
e' intatto (4fc7a794). Due decisioni operative:
- **GATE — si ri-timbra al PEZZO 3, NON prima.** Il gate esiste per garantire "questo RISULTATO
  viene da questo CODICE esatto". PEZZO 1 e 2 sono funzioni ISOLATE senza call-site: non cambiano
  nessuna dinamica, quindi **nessuna campagna e' necessaria** e i sigilli isolati bastano. Il gate
  stale (ancorato a 4fc7a794) e' **inerte finche' non si girano campagne**. Diventa rilevante al
  PEZZO 3, quando `U_ij` entra nella forza e i run cambiano davvero: li' si ri-timbra sul blob del
  fork, e cosi' a ogni pezzo successivo che tocca la DINAMICA.
- **DOC — non si biforcano.** I documenti in `doc/` descrivono il PROGRAMMA (design, formule,
  roadmap), non un blob: restano unici e branch-agnostici. La verita' per-branch del blob vive in
  **CLAUDE.md par.0 e solo li'** (fonte unica). Cura minima applicata: in
  `doc/BUSSOLA_TECNICA_dev-spinoriale.md` la riga del blob dichiara che e' il riferimento della
  BASELINE e rimanda a CLAUDE.md par.0 per il per-branch. Una riga, non una copia: duplicare
  sarebbe la trappola dei due documenti che divergono in silenzio.

## PEZZO 2 — FATTO, SIGILLO 11/11 PASS + 1 REPERTO PER IL PEZZO 3 (2026-09-13)
- **Il peso come IMPLEMENTAZIONE era gia' dentro `_link_su2`** (w = sin(chi), stesso prodotto
  vettore di m_hat). Il PEZZO 2 quindi non aggiunge codice: **blob INVARIATO b4c6c3f8**, nessuna
  riga di `.py` toccata. Quello che mancava era il sigillo della GRANDEZZA che finira' nella forza,
  non dei suoi fattori presi separatamente:
  `contrib_ij = w_ij * Im<psi_i| U_ij |psi_j>`   (oggi, scalare: `Im<psi_i|psi_j>`).
- **SIGILLO PEZZO 2: 11/11 PASS** — `csv/_seal_fork/_sigillo_pezzo2.py` (pure-read, exit 0/1):
  P1 **antisimmetria i<->j = azione-reazione** (5.6e-16: la coppia non crea momento dal nulla) ;
  P2/P2b contributo = 0 ai due estremi (0.000e+00 / -2.3e-18) ; P3 continuo (salto 3.3e-06) ;
  P3b **liscio ai bordi**, max|dc/dchi| = 0.208 (una soglia netta darebbe un picco: non c'e') ;
  P4/P4b contributo IDENTICAMENTE 0 su antipodali e allineati ; P6 nessun verso preferito
  (media -4.3e-03 dentro 3 sigma = 8.7e-03) ; P7 |contributo| <= 1, il peso non amplifica.

### ⚠ REPERTO — il sigillo previsto per il PEZZO 3 NON puo' passare come e' formulato
La ROADMAP chiede al PEZZO 3: *"flag OFF / tutti allineati -> BYTE-IDENTICO al ramo scalare"*.
Le due meta' non sono equivalenti, e la seconda e' **FALSA in generale** (misurato, P5):
- *flag OFF -> byte-identico*: **VERO** per costruzione (il ramo nuovo non viene eseguito).
- *tutti allineati -> byte-identico*: **FALSO.** Con chi=0 il peso vale w=0 -> contributo nuovo
  **zero**; ma lo scalare di oggi `Im<psi_i|psi_j>` **non e' zero** se i due spinori hanno FASI
  diverse. Misura: max|Im<psi_i|psi_j>| = **9.954e-01**, media |.| = 4.199e-01 su Bloch allineati.
  Le due espressioni coincidono **solo** se gli spinori sono i rappresentanti canonici dei
  rispettivi Bloch (P5b: 2.8e-17), che nel codice **NON e' il caso**: `_nb_grav` (riga ~2024)
  costruisce i Bloch dal campo EMESSO `psi_spin`, mentre cio' che viene trasportato in
  `_coppia_interferenza` (riga ~2203) e' `_psi_spinor`. **Due oggetti distinti**: i Bloch possono
  essere allineati mentre le fasi no.
- **CONSEGUENZA FISICA (la parte che conta):** il peso sin(chi) **SPEGNE gli archi a Bloch
  allineati**, cioe' proprio quelli che oggi portano il contributo di FASE — il settore
  U(1)/orologio, il canale EM. Non e' un bug del peso: e' cio' che il peso fa per costruzione,
  ed e' coerente con "antipodali e allineati non contribuiscono". Ma la ROADMAP lo chiama
  "innocuo" (par.4.1 della BUSSOLA TECNICA: *allineati -> w=0, innocuo*), e innocuo lo e' **solo**
  nel caso canonico. Nel sistema reale toglie un canale che oggi esiste.
- **NESSUNA SCELTA PRESA.** Lo script MISURA, non decide. Serve Luca prima del PEZZO 3.

## DIAGNOSI DEL REPERTO — il peso, non un bivio (Luca + misura, 2026-09-13)
Luca ha verificato il reperto dal disco (righe shiftate di +50 dal PEZZO 1: `_nb_grav` a **2068**,
`_coppia_interferenza` a **2242**, `psi_spin` a **2051**) e ha rigirato il sigillo: 11/11, P5=0.995.
Poi ha sciolto il nodo, e la sua lettura e' piu' profonda della mia:
- **Il reperto NON e' un bivio "perdere l'EM o tenerlo": e' un BUG del peso.** `sin(chi)`
  **SOVRA-CORREGGE**. Traccia l'indeterminatezza dell'asse `m_hat`, che si annulla a ENTRAMBI gli
  estremi, ma quell'indeterminatezza e' **dannosa solo a chi=pi**:
  - **chi=0:** `U = cos(0) I - sin(0)(m.sigma) = I` **qualunque sia m_hat** -> asse indeterminato
    ma INNOCUO, perche' `sin(chi/2)=0` uccide gia' il termine dell'asse. Non serve spegnere.
  - **chi=pi:** `U = -i (m.sigma)` e `sin(chi/2)=1` NON uccide il termine -> U dipende davvero da
    un asse indeterminato. **Dannoso.** Qui serve spegnere.
- **Conseguenza: il sigillo "allineati -> scalare" NON era sbagliato.** E' un controllo giusto (a
  chi=0, U=I, quindi `Im<psi_i|U|psi_j>` = lo scalare) e stava **diagnosticando il peso**. Aggiusti
  il peso -> il sigillo passa -> EM preservato -> antipodalita' gestita. Tutto si riconcilia.
- **Luca ha respinto la mia strada (a)** ("accettare e riformulare il sigillo"): la riformulazione
  e' corretta in se' (CLAUDE.md par.2.2) ma **non va usata per coprire una perdita di fisica**.
  Il sigillo che segnala un problema vero non si silenzia. Registrato: non prendere (a).

### MISURA DEI CANDIDATI — `csv/_seal_fork/_sigillo_pesi.py` (pure-read, blob invariato)
| peso | chi=0 | chi=90 | chi=180 | riduce allo scalare | cura l'antipodale |
|---|---|---|---|---|---|
| `sin(chi)` ATTUALE | 0.000 | 1.000 | 0.000 | **NO (err 9.99e-01)** | si' |
| `cos(chi/2)` da N | 1.000 | 0.707 | 0.000 | **SI' (2.22e-16)** | si' |
| `cos^2(chi/2)` | 1.000 | 0.500 | 0.000 | si' (2.22e-16) | si' (piu' forte) |
| nessun peso | 1.000 | 1.000 | 1.000 | si' | **NO (dispersione 1.62 costante)** |

- **RISULTATO CHIAVE: `cos(chi/2)` NON e' una scelta, e' cio' che resta quando NON si normalizza.**
  Il trasporto parallelo non normalizzato `N = (1+n_i.n_j) I + i (n_i x n_j).sigma` vale
  **esattamente `2 cos(chi/2) U`** (verificato **2.741e-14** su 200000 archi). Quindi il peso e'
  `|N|/2`: **derivato, zero manopole** (par.3 rispettato). In piu' `N` e' polinomiale nei Bloch:
  niente `arccos`, niente asse da normalizzare, niente floor 1e-30, nessun caso degenere a mano.
- **Il test dell'antipodale va fatto sulla DIREZIONE, non sull'angolo** (prima versione del test
  sbagliata, corretta): si perturba n_j attorno all'antipodale in 360 direzioni azimutali e si
  misura la DISPERSIONE del contributo. Senza peso resta **1.62 costante** anche per eps->1e-6
  (contributo indeterminato = dannoso); con `sin(chi)` e `cos(chi/2)` svanisce linearmente; con
  `cos^2(chi/2)` quadraticamente.
- **CAVEAT:** tutti questi pesi sono GLOBALI. L'ammorbidimento STRETTO vicino a pi che Luca
  preferirebbe in linea di principio richiederebbe una larghezza = **un numero nuovo = manopola**
  (par.3). `cos(chi/2)` evita la manopola proprio perche' non e' scelto: emerge.
- **NESSUNA DECISIONE PRESA.** Il peso si tocca solo su delibera di Luca.

## DELIBERA SUL PESO + RIFATTORIZZAZIONE SU N — FATTO (2026-09-13)
- **DELIBERA: il peso e' `cos(chi/2)`, non `sin(chi)`.** La ragione e' FISICA, non estetica
  (argomento di Luca, misurato in `csv/_seal_fork/_sigillo_N.py`):
  - **`cos(chi/2) = |<n_i|n_j>|` = OVERLAP QUANTISTICO dei due spin** (F1: 1.122e-14). Non e' un
    artefatto del non-normalizzare: e' **quanto i due spin si sovrappongono**, cioe' l'accoppia-
    mento fisico fra due solitoni. Questo scioglie la tensione sull'"ammorbidimento stretto":
    trattavamo il peso come un REGOLARIZZATORE (che vorrebbe essere stretto), ma e' un
    **ACCOPPIAMENTO**, e un accoppiamento e' **globale per natura**. "Globale ma non scelto" non e'
    un compromesso: e' corretto. L'antipodale si cura come CONSEGUENZA (overlap -> 0), non come scopo.
  - **Contro `cos^2(chi/2)`: quella e' la PROBABILITA' di Born** (F2: 9.548e-15). La forza e'
    `Im<psi_i|N|psi_j>`, una **AMPIEZZA**: si pesa con un'ampiezza, non con una probabilita'.
    `cos^2` conterebbe due volte. Contro `sin(chi)`: spegne chi=0, perde l'EM. Contro
    l'ammorbidimento stretto: una larghezza = un numero nuovo = manopola (par.3).
- **SIGILLO N: 19/19 PASS.** I tre presidi di Luca: (1) nella forza si usa **N/2**, che ad allineati
  vale I -> `Im<psi_i|N/2|psi_j>` = scalare entro **4.441e-16** (con `sin(chi)` dava 9.992e-01:
  **il reperto del PEZZO 2 e' CHIUSO**); (2) **N nella forza, U = N/sqrt(det N) nell'olonomia** — la
  fase dell'olonomia e' identica con N o U (9.149e-13), il peso fattorizza come scalare positivo
  sul ciclo; (3) l'algebra NON dimostra la correttezza dinamica (vedi PRESIDIO APERTO in fondo).

### RIFATTORIZZAZIONE — `_link_su2` ora poggia sul polinomiale N. **Blob: b4c6c3f8 -> `cf24cd28`**
- **`_link_su2_N(ni,nj)` (NUOVA)** = `N = (1+n_i.n_j) I + i (n_i x n_j).sigma`. **Primitiva della
  FORZA.** Polinomiale: **niente arccos, niente asse da normalizzare, niente floor, nessun caso
  degenere**. Ad antipodali N=0 da solo (dot=-1, cross=0).
- **`_link_su2(ni,nj)` (RISCRITTA)** ritorna `(U, w)` con `U = N/sqrt(det N)` e `w = sqrt(det N)/2
  = cos(chi/2)`. **Per l'OLONOMIA** (pure-read), dove serve la rotazione pura. **La radice vive solo
  qui, mai nella forza.** Resta UN caso degenere, e solo in questo ramo: ad antipodali esatti U e'
  indefinita (0/0) perche' nessuna rotazione porta n_j su -n_j -> `U := I`, con w=0 che spegne
  l'arco. La forza, passando da N, non eredita ne' il caso speciale ne' la soglia.
- Diff: 68 inserite / 41 rimosse. `py_compile` OK. **Ancora NESSUN call-site nella dinamica**
  (`grep _link_su2` -> solo le 2 definizioni + 1 uso interno) -> **sigillo "OFF = byte-identico"
  regge sempre per costruzione**: il fork non e' ancora cablato.
- **SIGILLI DOPO LA RIFATTORIZZAZIONE: N 19/19, PEZZO 1 17/17, PEZZO 2 11/11, tutti exit 0.**

### ⚠ SIGILLI STORICI AGGIORNATI — dichiarato, non silenziato
Cambiando il peso, 5 asserzioni dei sigilli PEZZO 1/2 sono passate a FAIL. **Codificavano la
specifica VECCHIA**, cioe' il bug: sono state riscritte con un commento che dice cosa pretendevano
prima, cosa pretendono ora e perche'. **Non e' "aggiustare il test per farlo passare": la
specifica e' cambiata per delibera motivata, e la pretesa vecchia era sbagliata.**
- `S1b`: "allineati -> w = 0" **-> "allineati -> w = 1"** (overlap massimo, EM preservato).
- `S7`: "w = sin(chi)" **-> "w = cos(chi/2)"**.
- `P2`, `P4b`: "allineati -> contributo = 0" **-> "contributo = scalare"**. Se tornassero a
  pretendere 0, starebbero ri-chiedendo il bug EM.
- `P4`: soglia da `== 0.0` a `< 1e-15`. Motivo NUMERICO, non di specifica: con versori normalizzati
  in floating point il dot ad antipodali vale -1 +- 1e-16, quindi det N ~ 1e-32 e w ~ 1e-16.

## ⚠ PRESIDIO APERTO — cosa NON e' dimostrato
L'algebra chiude tre problemi e **solo** quelli: **numerico** (niente arccos/floor/casi speciali),
**EM** (riduzione allo scalare esatta a chi=0), **antipodale** (indeterminatezza spenta). **NON**
dimostra che `cos(chi/2)` sia **DINAMICAMENTE** corretto. Il peso sotto-pesa gli archi a chi grande
(0.707 a 90 gradi, 0.500 a 120). C'e' un argomento buono che sia giusto — `N|psi_j>` e' la
proiezione naturale del trasportato, e spin disallineati interferiscono davvero meno — **ma e' un
ARGOMENTO, non una MISURA.** Olonomia W(r) sensata, stabilita', comportamento EM: lo dice un RUN.
**Elegante non significa dinamicamente corretto.**

## PEZZO 3 — CABLATO, MA IL SIGILLO S2b FALLISCE: IL FORK E' INERTE (2026-09-13)
**Blob: cf24cd28 -> `968fba34`.** Flag `--fork-su2` (OFF di default), `_mat2` per le due direzioni
dell'arco, e la sostituzione in `_coppia_interferenza`:
`Im<psi_i|psi_j>` -> `Im<psi_i| N_ij/2 |psi_j>`, con i Bloch presi da `_psi_spinor`.

### SIGILLI: 5 PASS, 1 FAIL — e il FAIL e' quello che conta
| sigillo | esito | misura |
|---|---|---|
| S1 flag OFF = byte-identico (2 run veri, 150 passi, seed 1) | **PASS** | **max\|A-B\| = 0.000e+00** su 32 array |
| S2 allineati: ON == ramo scalare (riduzione al limite) | **PASS** | max\|ON-OFF\| = 0.000e+00 |
| S5 azione-reazione, somma coppia ~ 0 (ramo OFF) | PASS | sum = +1.066e-14 (max\|c\| = 13.3) |
| S5 azione-reazione, somma coppia ~ 0 (ramo ON) | PASS | sum = +2.554e-15 (max\|c\| = 13.3) |
| **S2b Bloch generici: ON deve differire dallo scalare** | **FAIL** | **max\|ON-OFF\| = 4.441e-15** |

### ⚠ REPERTO — non e' un bug del cablaggio, e' un TEOREMA
Evidenza: `csv/_seal_fork/_reperto_inerzia.py`. Se i Bloch da cui si costruisce la connessione sono
i Bloch **DEGLI STESSI spinori che vengono trasportati**, allora

        <psi_i| N_ij |psi_j>  ==  2 <psi_i|psi_j>      (misurato: 1.570e-15 su 200000 coppie)

quindi **N/2 agisce come l'IDENTITA' sull'overlap e la forza non cambia di un bit.**
Dimostrazione, due righe: `(n_i.sigma)(n_j.sigma) = (n_i.n_j) I + i (n_i x n_j).sigma`, quindi
`N = I + (n_i.sigma)(n_j.sigma)`; ma `n_i` e' il Bloch di `psi_i`, quindi `|psi_i>` e' autovettore
di `(n_i.sigma)` con autovalore +1, e lo stesso per j. I due termini danno lo stesso overlap.

**Significato:** la connessione di Berry costruita dagli stessi stati che trasporta e' BANALE
SULLA FORZA — trasporta `psi_j` esattamente su `psi_i`, quindi l'overlap non puo' cambiare. E' la
forma FORTE del caveat gia' scritto in `doc/ROADMAP_fork_SU2.md` ("i link derivati dai soli Bloch
sono schiavi della materia, no gradi di liberta' propri"): **non sono solo schiavi, sono INERTI.**

**Distinzione da tenere ferma:** questo riguarda la **FORZA**. L'**OLONOMIA** di plaquette resta
non banale (due U con assi diversi non commutano, PEZZO 1 S9 = 1.000e+00). Quindi il fork puo'
ancora produrre un **diagnostico** non abeliano. Ma un diagnostico non e' dinamica: se la forza
non cambia, **il fork non fa nulla al sistema**.

**CONTROPROVA (misurata):** se i Bloch vengono da un campo DIVERSO dagli spinori trasportati, il
trasporto agisce eccome (9.940e-01). Nel codice quei due oggetti esistono gia': `_nb_grav` prende
i Bloch dal campo EMESSO `psi_spin`, mentre `_coppia_interferenza` trasporta `_psi_spinor`.

### ⚠⚠ CHIARIMENTO CRITICO — il run a 150 passi mostrava N diverso: E' RUMORE, NON FISICA
Confrontando i due run da 150 passi si vedeva **N = 3164 (OFF) contro 3209 (ON), +1.4%**. Sembra
che il fork faccia qualcosa. **NON lo fa.** Misurato rifacendo i confronti in modo pulito:

| orizzonte | esito |
|---|---|
| 2 passi, ramo ON **eseguito 305 volte** (verificato con spia su stderr) | ramo attivo, non saltato |
| 3 passi, ON vs OFF | **file .pkl BYTE-IDENTICI** |
| 40 passi, ON vs OFF | **max\|OFF-ON\| = 2.220e-16**, N identico (1889 = 1889) |
| 150 passi, ON vs OFF | N 3164 vs 3209 |

Lettura: il ramo ON **viene eseguito**, ma per il teorema produce lo stesso risultato; l'unica
differenza e' il **percorso di calcolo** (4 matvec invece di 2), che cambia l'ordine delle somme e
quindi l'ultimo bit. A 40 passi la differenza e' ancora **2.2e-16** (arrotondamento puro). Su
orizzonti lunghi il sistema e' caotico e quel rumore a 1e-16 si amplifica fino a cambiare le
mitosi, quindi N. **La differenza di N a 150 passi e' rumore di arrotondamento amplificato, non
un effetto fisico del fork.**

**PRESIDIO — il falso positivo che ho quasi preso:** guardare solo N a 150 passi avrebbe fatto
concludere "il fork fa qualcosa" (+1.4%, sembra un effetto). E' esattamente l'autoinganno contro
cui i documenti mettono in guardia. Il modo per non cascarci: **misurare la divergenza a orizzonte
CORTO**, dove l'arrotondamento non ha ancora avuto tempo di amplificarsi. Se a 40 passi vale
1e-16, non c'e' fisica dentro, qualunque cosa si veda dopo.

## ⚠ DECISIONE APERTA (di Luca, non mia) — da CHE COSA si costruisce la connessione?
Cambiare la sorgente dei Bloch (da `_psi_spinor` a `psi_spin`) farebbe agire il fork. **Ma
sceglierlo PERCHE' fa muovere il risultato sarebbe tarare un meccanismo per ottenere un effetto:
l'opposto del par.3.** La domanda giusta e' FISICA: la connessione di gauge su un arco, in questo
sistema, da che cosa deve essere costruita, e perche'? Possibilita' viste, nessuna deliberata:
1. **Dal campo emesso `psi_spin`** (i due oggetti esistono gia' e sono distinti). Da giustificare:
   perche' il gauge dovrebbe vivere sul campo emesso e non sullo stato primario?
2. **Dallo STRATO 1** (`doc/ROADMAP_fork_SU2.md`): dare al link una MEMORIA propria
   (`dU/dt = (U^Berry - U)/tau`). Con memoria, U NON e' piu' istantaneamente la Berry degli stati
   correnti, quindi il teorema di inerzia si rompe **da solo, per costruzione**. Questa e' la via
   che il piano gia' prevedeva: forse lo Strato 0 e' inerte **by design** e il fork inizia a vivere
   solo allo Strato 1.
3. Accettare che lo Strato 0 sia solo un'infrastruttura diagnostica (olonomia) e non dinamica.
**Finche' non c'e' una risposta DERIVATA, il cablaggio resta inerte e il flag resta OFF.**

## PROSSIMA AZIONE — decisione di Luca sul punto qui sopra
- Il gate NON e' stato ri-timbrato: con il fork inerte non cambia nessun run, e la decisione di
  Luca era "si ri-timbra al PEZZO 3 quando i run cambiano davvero". **Oggi non cambiano.**
- **S3/S4/S6 ora girati** (dai run gia' su disco piu' due run corti nuovi): **S3 norma |psi|=1
  (2.220e-16 su 3209 nodi) PASS ; S4a nessun NaN/inf PASS ; S6 (ON deve differire da OFF) FAIL**,
  come previsto dall'algebra. Bilancio finale del PEZZO 3: **6 PASS, 2 FAIL (S2b e S6)**, e i due
  FAIL sono la stessa cosa: il fork non cambia la fisica.
- **BUG CORRETTO in `_sigillo_pezzo3.py`:** il codice pre-cablaggio veniva estratto da `HEAD`.
  Appena il cablaggio e' stato committato, `HEAD` ha smesso di essere il pre-cablaggio, quindi il
  sigillo avrebbe confrontato il nuovo codice **con se stesso** e sarebbe passato sempre. Ora il
  riferimento e' il commit FISSO `4d7ca25`. Da ricordare: **un sigillo ancorato a HEAD si
  auto-assolve** appena il lavoro viene committato.
1. **PEZZO 3:** in `_coppia_interferenza` (righe ~2242 sul blob precedente, da ri-cercare per NOME
   sul blob `cf24cd28`), dietro flag OFF: `Im<psi_i|psi_j>` -> `Im<psi_i| N_ij/2 |psi_j>`.
   Attenzione all'ORIENTAMENTO: `N_ij` trasporta n_j -> n_i, il verso giusto per quella forma.
   Da decidere: da DOVE arrivano i Bloch dentro `_coppia_interferenza` (`_nb_grav` usa `psi_spin`).
2. **Sigilli del PEZZO 3:** flag OFF -> byte-identico (ora va verificato per davvero, non piu' per
   costruzione: ci sara' un call-site); allineati -> scalare (ora PASSA esatto); norma; stabilita'.
3. **QUI si ri-timbra il gate** sul blob del fork (decisione di Luca: al PEZZO 3, non prima).
4. Poi: `SYNC_UPDATE`/`SCUOTIMENTO` attivi? Poi olonomia W(r) (`doc/PROTOCOLLO_test_olonomia.md`).
5. Deprioritizzato (Luca): il run sulla divergenza `psi_spin` vs `_psi_spinor`. Non e' piu'
   decision-critical, perche' `cos(chi/2)` preserva chi=0 a qualunque divergenza.
1. **Delibera sul peso** (`sin(chi)` -> `cos(chi/2)` o altro). Finche' non arriva, il PEZZO 3 resta
   fermo: cablare con il peso sbagliato significherebbe cablare una perdita di fisica.
2. **Run di misura (di Luca): quanto divergono davvero `psi_spin` e `_psi_spinor`?** Da' la SCALA
   dell'effetto. Non cambia il fix di principio, ma dice se l'effetto e' grande o marginale.
3. Poi PEZZO 3 (cablaggio in `_coppia_interferenza`, righe ~2242), e **li'** si ri-timbra il gate.
4. Poi controllo che `SYNC_UPDATE`/`SCUOTIMENTO` siano attivi, poi olonomia W(r).
Ordine operativo in `doc/ROADMAP_fork_SU2.md`, un pezzo un sigillo, flag OFF di default:
1. ~~PEZZO 1~~ **FATTO** (sigillo 17/17 PASS, vedi sezione sopra).
2. **PEZZO 2** — peso `w_ij=|n_j x n_i|=sin(chi)`. Niente soglia netta, niente coefficiente tarato.
3. **PEZZO 3** — cablaggio nella forza, **righe 2207-2208** (`_coppia_interferenza`):
   `Im<psi_i|psi_j> -> w_ij * Im<psi_i|U_ij|psi_j>`. Attenzione all'ORIENTAMENTO (`U_ij=U_ji^dag`):
   con gli scalari era irrilevante, ora conta. Sigillo: flag OFF / allineati -> BYTE-IDENTICO.
4. Poi (lettura, gratis): controllare che `SYNC_UPDATE` e `SCUOTIMENTO` siano ATTIVI nella config del
   fork, altrimenti la degenerazione dei Bloch non si rompe.
5. Poi le verifiche dinamiche (Luca gira, Claude legge): distribuzione degli angoli chi, olonomia
   W(r) secondo `doc/PROTOCOLLO_test_olonomia.md`, isotropia `<n>`.

## ROADMAP A VALLE (GAMMA / cs<->orologio) — ⚠ RIMANDATA dopo il fork (2026-09-13)
> Vedi `ROADMAP_dev-spinoriale.md` (marcata SUPERATA) + `/memories/repo/roadmap_todo.md`.
> **Non e' il lavoro corrente**: la prossima azione e' il fork Strato 0 (sezione sopra). Questa
> sezione resta come RECORD del piano e della sua matematica: valida, solo rimandata.

Obiettivo: EM e gravita' come 2 proiezioni dello STESSO campo spinoriale, con la giusta gerarchia.
- Canali gauge-invarianti = MODULO |psi|^2 (gravita') vs FASE/segno (EM). MAI Re/Im per-arco
  (2 proiezioni di 1 solo grado, gauge-dipendenti; Im = motore forza, non carica). Bargmann e' CIECO
  al segno (telescoping) -> misura EM = phase-locking TEMPORALE (SYNC/Kuramoto).
- STEP 0 SALTATO (Luca): seed-1 (B) = BASELINE INTERNA, non risultato robusto. seed-2/3 = TODO
  rimandato (solo se il (B) andra' presentato come stabilito).
- STEP 1A [SOSPESO, non piu' la prossima azione] (pure-read, NON tocca .py): scrivere `_run_3gamma.ps1` +
  `_analizza_3gamma.py`, coarse-graining a blocchi di b, fittare d in gamma_eff(b)~b^d nei due canali
  (modulo; fase via SYNC). Verdetto: FASE d~0 + DENSITA' d<0 = gerarchia emersa. Sigillo b=1=identita' byte-id.
- STEP 1B (flag `--gamma-nudo`/`--gamma-relazionale`), STEP 2 (accoppiamento cs<->orologio:
  omega_clk*(cs/CS_M)^2, solo magnitudine; segno invariato; sigillo cs=CS_M byte-id + stabilita'),
  STEP 3 (esplorativo alpha_G, magnitudine NON torna ~35 ordini). Tutto SCRITTO, NON eseguito.
- Regola: CHECKPOINT a Luca tra ogni step. Precondizione ripresa: blob == 4fc7a794.

## VERDETTO SEED 1 (completo, 3 bracci a 800 passi) — (B) abeliano su tutti
| Braccio | N | solo-materia (2a met) | spin_ovl | segno_ov | verdetto |
|---|---|---|---|---|---|
| b1_base | 4713 | -0.00024 | 0.5000 | 0.638 | (B) abeliano |
| b2_orolseg (5.3c) | 4933 | +0.00011 | 0.5000 | 0.631 | (B) abeliano |
| b3_orolseg_cs (5.3c+cs) | 4697 | +0.00028 | 0.5000 | 0.637 | (B) abeliano |
- Solo-materia decade sempre 0.65->~0. cs-dinamico NON aggiunge ordine (b3 ~ b1/b2).
- Misure gauge-robuste concordi: spin_ovl=0.5000, segno_ov~2/pi ovunque.
- PUNTO 3 (asimmetria settori): la firma AGISCE ma non ordina. frac_chi_neg: b1=0.4997,
  b2 (5.3c)=0.5122 (verso antimateria), b3 (5.3c+cs)=0.4917 (verso opposto). N diverge (b2 4933).
- CAUTELA: 1 solo seed. Non consolidato -> servono seed 2 e 3 (gate-cache -> cache-hit istantaneo).
- berry_segno IGNORATO (cieco: olonomia Bargmann chiusa telescopa la fase per-nodo del segno).

## Cosa è stato fatto (in ordine)
1. **MOD 5.3c `--orologio-segno`** (commit `77c83e5`): firma il VERSO dell'orologio de Broglie INTERNO
   `_phc = exp(-0.5j * s_k * omega_clk * dt)` con `s_k = sign(perc_chi)` STABILE (materia exp−, antimateria exp+).
   Vive nel ramo `--deparam-orologio`. Richiede `--campo-spinoriale --spinore-corretto`.
   SIGILLI GATE PASS: OFF byte-identico (max|A−B|=0 su 32 array), riduzione-al-limite esatto, |ψ|=1, stabilità.
2. **Reperto**: sotto `--campo-spinoriale` la firma NON è inerte — il segno per-nodo cambia l'interferenza del
   campo emesso `mat(w)@_psi_spinor` → rho_spin → N diverge (3228→3273) = canale non-abeliano VOLUTO (Fase 3).
3. **Presidio carica per-coppia** (commit `c45a81b`): la firma è APPEND-ONLY su perc_chi (0/120 riscritture),
   Schwinger antinodo = −perc_chi[genitore], quantizzazione ±1. Σperc_chi drifta solo per lignaggio (mitosi).
4. **FIX presidio critico** (commit `109744a`): `segno_arco_coer_materia` NON più tautologico — settore materia
   selezionato con `perc_chi>0` (etichetta stabile), misura coerenza di `_sgn` (doppia-copertura). + `n_arco_materia`.
   Baseline: 0.65 → ~0 (metrica discrimina). Statistica: 54206 archi materia-materia.
5. **FIX PUREZZA DIAGLOG** (commit `109744a`): bug pre-esistente — sotto `--campo-spinoriale` il diaglog
   contaminava (N 3228 vs 3299). Cause: cache `psi_spin,rho_spin,_psi_spin_prec` + stato RNG non nello
   snapshot/restore. Estesi `_snap_fisica` (diaglog) e `_snap_cond` (condensazione). VERIFICATO byte-identico
   con/senza `--diaglog` (max|A−B|=0) nel config NON-verlet.
6. **Regole comportamentali** (commit `2f8fa61` + copilot-instructions): (a) diaglog/trace SOLO-LETTURA, mai
   toccare la fisica, verifica byte-identico obbligatoria; (b) ogni commit → push, messaggi approfonditi,
   commit/push prima di ogni run; (c) `--verlet` default nei test.

## Campagna 5.3c — CHIUSA come baseline (non e' il lavoro corrente)
> La prossima azione e' il **fork Strato 0** (sezione "PROSSIMA AZIONE" sopra). Quanto segue e' il
> record della campagna e i suoi TODO, che restano aperti ma RIMANDATI.

- **SEED 1 COMPLETO** (vedi verdetto sopra): (B) abeliano su b1/b2/b3.
- **TODO RIMANDATO: seed 2 e 3.** Servono solo se il (B) andra' presentato come risultato STABILITO
  (oggi e' BASELINE INTERNA, 1 seed). Comando: `powershell -File csv/_test_53c/_run_batch.ps1 -seed 2`
  poi `-seed 3` (gate-cache -> cache-hit istantaneo se il blob e' invariato). Commit/push PRIMA di ogni
  run. Attenzione OOM se video attivo. NB: il fork cambiera' il blob -> gate da ri-timbrare.
- Poi: verdetto consolidato a 3 seed + punto 3 (asimmetria) + effetto cs.
- **Verdetto** (arbitro = `segno_arco_coer_materia` SOLO-MATERIA): (A) sale/resta = ordine vero;
  (B) ~0 = separazione/abeliano. Guardare SOLO-MATERIA, non il totale. Analisi: `csv/_test_53c/_analizza_bracci.py`.

## Config base dei bracci (identico al pilota 5.3a + firme + verlet + deparam)
`--batch --nmasse 3 --sep 8 --passi 800 --ogni 100 --campo-spinoriale --spinore-vivo --spinore-corretto
--chi-core --calore-scal --deparam-orologio --verlet` + `--seed S` + firma del braccio.

## Presidi di Luca ancora aperti
- Ri-confermare 5.3a pulito dopo il fix (nel launcher, run `r53a_tsegno_s1`).
- Monitorare braccio 3 (`--cs-dinamico`) per instabilità; STOP se cs non governa il cono causale.

## ARBITRO GAUGE-INVARIANTE — OLONOMIA DI BARGMANN (Luca 2026-09-11)
- Domanda di Luca "la correlazione e' calcolata bene?" -> scoperto che `segno_arco_coer` e' GAUGE-DIPENDENTE
  (segni relativi a canon(nb_k), frame locali diversi per nodo; correlazione su arco APERTO e' gauge-dipendente).
- Verdetto (B) regge per TRIANGOLAZIONE con misure gauge-INVARIANTI: spin_overlap=0.5 (direzione random),
  segno_ov_absmedia~2/pi=0.637 (fase doppia-copertura uniformemente random).
- CURA DEFINITIVA aggiunta (pure-read, in circolazione_topologica + diaglog): OLONOMIA DI BARGMANN di
  _psi_spinor su cicli chiusi = arg(prod <psi_k|psi_{k+1}>). Gauge-invariante per costruzione. La berry su nb
  e' cieca-al-segno (§38-bis); questa usa il PRIMARIO -> sonda DIRETTAMENTE il segno-orologio. Colonne:
  berry_spinor_media (FIRMATA = l'arbitro: ~0=frustrato blindato, !=0=ordine), _media_assoluta, _rms, _max.
- RE-RUN NECESSARIO per popolare berry_spinor. IN ATTESA: Luca genera un VIDEO (python 27104, config 5.3c+cs)
  -> no contention. Al via, rilanciare i batch (gate-cache auto-verifica il nuovo blob + purezza col nuovo pure-read).

## GATE-CACHE (Luca 2026-09-11) — rigore + velocità
- I gate NON sono più solo script a mano: `csv/_test_53c/_run_batch.ps1` ha un GUARD che legge `gate_cache.json`
  ancorato al **git BLOB** di `soliton_simulator.py` (byte attuali, cattura anche modifiche non committate).
- Cache-hit (blob invariato + PASS) → parti istantaneo. Cache-miss/stale → `_gate.ps1` rigira il presidio UNA
  volta e timbra la cache; se FAIL → STOP (non lancia i bracci). Qualsiasi modifica al .py invalida la cache.
- Gate vivo = `_check_presidio.py` (purezza byte-id + baseline discrimina + non-tautologico, exit 0/1).
  Sigilli firma (OFF byte-id, riduzione-al-limite, norma) = analitici + verificati al sigillo 77c83e5.
- Uso: `powershell -File csv/_test_53c/_run_batch.ps1 -seed N` (auto-gate su cache-miss).

## Futuro concordato (non ora)
- Refactor diaglog→messaging: produttore emette snapshot immutabile; consumer applica REGOLE PURE
  disaccoppiate da `net`, fa i conti pesanti a parte. Purezza per costruzione.
