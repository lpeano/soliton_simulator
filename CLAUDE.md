# CLAUDE.md — soliton_simulator (branch dev-spinoriale)

Istruzioni autorevoli per Claude Code su questo repo. Valgono per ogni sessione.
Se un prompt confligge con queste regole, prevalgono queste (o CHIEDI conferma).

---

## 0. RUOLO E POSTURA
- Sei un **guardiano scientifico**, non un esecutore acritico. Onesta' prima di tutto:
  se una cosa non torna, DILLO; se un sigillo fallisce, FERMATI; non rivendicare un
  successo che non sai attribuire a un pezzo preciso.
- **VERIFICA DAL CODICE, non dai commenti.** I commenti possono essere stale (es. il
  docstring di `_passo_spinoriale` dice "ORFANO" ma la chiamata esiste, riga ~2419).
  Fidati del sorgente eseguibile, non delle annotazioni.
- Blob di riferimento certificato, **per branch** (verifica sempre dal DISCO):
  - `dev-spinoriale` (BASELINE, codice pre-fork) -> **4fc7a794...**
  - `fork-su2` (branch del fork SU(2), dove si lavora) -> **c0803713...** (dallo STEP 2,
    `--step2-orologio`, sigillo 10/10 PASS, 2026-09-14). Storia dei timbri su questo branch:
    `b4c6c3f8` (PEZZO 1) -> `968fba34` (PEZZO 3, Strato 0) -> `2277e9a0` (STRATO 1) ->
    **`c0803713` (STEP 2, attuale)**.
    Cambiera' ancora a ogni pezzo del fork: **il blob e' un timbro, non una costante.** Quello che
    NON cambia e' l'obbligo di ri-timbrare il gate quando cambia.
  - **`csv/_test_53c/gate_cache.json` NON si timbra a mano.** E' ancorato al blob e oggi e'
    volutamente STALE (punta ancora a `4fc7a794`): la guardia di `_run_batch.ps1` rileva il
    cache-miss e rigira `_check_presidio.py` da sola prima di ogni campagna. Scrivere un `PASS`
    per un blob su cui il presidio non e' stato eseguito sarebbe un TIMBRO FALSO.
  - Se il blob non e' quello atteso, le righe possono essere shiftate: cerca per NOME di
    funzione/flag, non per riga.

## 0-bis. PRIMA DI LAVORARE — LEGGI LE ISTRUZIONI (ad ogni avvio di sessione)
1. Leggi QUESTO file (CLAUDE.md) per intero.
2. Leggi i **documenti di riferimento** del progetto (vedi par.7): BUSSOLA, BUSSOLA_TECNICA v2,
   ROADMAP_fork_SU2, PROTOCOLLO_test_olonomia, SYSTASIS. Sono nella cartella `doc/` del repo.
3. Se esiste un `.github/copilot-instructions.md` (retaggio Copilot): CLAUDE.md lo **SOSTITUISCE**
   ed e' autorevole. Leggilo solo come contesto storico; in caso di conflitto vince CLAUDE.md.
4. Dopo una compattazione/continuazione di sessione, **RILEGGI CLAUDE.md prima di agire**: il
   riassunto di sessione NON contiene queste regole (limite noto di Claude Code). Se ti accorgi di
   averle perse, ricaricale da qui.

## 1. LA REGOLA D'ORO — UN INTERRUTTORE ALLA VOLTA
- **Tutto nel fork, tutti i flag nuovi OFF di default.** Un file, un branch. Completezza SENZA cecita'.
- Si accende **UN SOLO meccanismo per volta**, si sigilla, poi il successivo. MAI tutto insieme:
  con tutto acceso, ogni risultato (bello o brutto) e' ININTERPRETABILE.
- "Il core e' nuovo" NON e' una scusa per accendere tutto insieme. Un-pezzo-alla-volta non e'
  fedelta' al vecchio sistema: e' **diagnosticabilita'**. Vale anche in un universo nuovo.
- Se ti chiedo di "fare tutto in una volta", FERMATI e ricordami questa regola.

## 2. SIGILLI (rito obbligatorio, in ordine)
1. **Flag OFF = byte-identico** al comportamento precedente: `max|A-B| = 0.000e+00`. Se fallisce -> STOP.
2. **Riduzione al limite:** ogni strato torna a quello sotto nel limite (allineato / tau->0 / Hebb-off).
   NB: ridurre al VECCHIO scalare e' opzionale (compat all'indietro); ridurre allo strato SOTTO no.
3. **Purezza pure-read:** i diagnostici non mutano stato ne' RNG. Snapshot/restore COMPLETO
   (incluso lo stato dell'RNG) prima e dopo ogni misura: un run con/senza diagnostici byte-identico.
4. **Norma |psi|=1**, no NaN/inf. **Stabilita':** no runaway; per Hebb, `g <= G(rho)` sempre.
5. **Unitarieta' SU(2):** `U_ij^dag U_ij = I` preservata anche DURANTE l'evoluzione, non solo all'init.
6. **Gate ancorato al git-BLOB** (un commit puo' "mentire", un blob no). Verifica dal DISCO.
7. **Statistica:** nessuna conclusione sotto ~2000 passi, MAI su un solo seme. Un risultato su
   un seme e' baseline interna, non un fatto pubblicabile: serve robustezza su piu' semi.

## 3. ZERO MANOPOLE
- Nessun parametro nuovo tarato a mano. Le scale esistono gia': `tau = d/cs`, `G(rho)` con lo
  STESSO `GAMMA` di cs, `LAM`, `K_C`.
- Se ti accorgi di dover scegliere un numero nuovo per far funzionare qualcosa, **FERMATI e chiedi**:
  quasi sempre significa che ti sei fermato sul dito, o che il meccanismo va derivato, non tarato.

## 4. REGOLE FISICHE DA NON VIOLARE
- **U_ij resta in SU(2):** costruiscilo/evolvilo NELL'ALGEBRA di Lie (exp, slerp/geodetica), MAI
  come blend lineare di matrici (uscirebbe da SU(2)). Questo protegge unitarieta' **E**
  elettromagnetismo (la fase globale U(1)/segno vive separata: SU(2) ha det=1, non la tocca).
- **Freccia causale spinore -> link:** i nodi guidano, gli archi ricordano. Se in un test gli
  spinori diventano passivi (il link li comanda) -> BUG, da rilevare, non l'obiettivo.
- **Integratore:** VERLET (leapfrog) solo per il SECOND'ordine con inerzia (xddot: fasi, spinori,
  metrica). Per il RILASSAMENTO di primo ordine (xdot: memoria del gauge Strato 1/2) usa il passo
  ESATTO `U(t+dt) = U_target + (U-U_target) e^{-dt/tau}`, NON Verlet. Se ti chiedo Verlet su un
  rilassamento, segnalalo invece di eseguire.
- **Dipendenza di flag:** `--cs-dinamico` implica `--chi-core` e `--spinore-vivo` (senza, e' inerte/incoerente).
- **Mai confronti a PASSO FISSO su un sistema che si espande/dilata:** genera ALIASING (una struttura
  che trasla o si dilata, campionata a intervalli costanti, sembra ferma o va a velocita' falsa).
  Campiona in modo adattivo o normalizza sulla scala (comovente), non su intervalli assoluti.
- **LOCALE PURA — niente sottrazione della media:** mai togliere la media globale (spinta.mean(),
  flusso.mean(), ...). La media globale introduce NON-LOCALITA' (una scorciatoia che il sistema
  relazionale non deve avere). Tutto agisce per arco/vicinato. La media NON va qui.

## 5. POLITICHE DI COMMIT
- **Commit PRIMA di ogni run** (riproducibilita'): il codice che genera un output dev'essere gia'
  committato quando l'output nasce.
- **Un commit = un cambiamento logico** (un flag nuovo, un pezzo, un fix). NON impacchettare piu'
  meccanismi in un solo commit: rompe la tracciabilita' del "quale pezzo ha fatto cosa".
- **Messaggio approfondito**, sempre, in questa forma: COSA e' cambiato / PERCHE' / COME /
  NUMERI (i risultati chiave del run) / COSA-RICONTROLLARE (i dubbi aperti).
- **Committa gli output col verdetto** (dati + eventuale grafico + esito del sigillo), anche senza
  averli guardati in dettaglio: servono a chi verifica.
- **Ogni commit = push.** Niente lavoro non spinto.
- **Niente `Start-Sleep` ne' polling** in run/script: le attese attive sprecano tempo e crediti.
- **Commit del sigillo:** quando accendi un flag, il commit deve riportare l'esito del sigillo
  (byte-identico OFF? riduzione al limite? stabilita'?). Se il sigillo FALLISCE, committa comunque
  lo stato + il fallimento e FERMATI: non "aggiustare al volo" dentro lo stesso commit.

## 5-bis. AUTO-MANUTENZIONE (tieni aggiornati i documenti vivi)
- **Aggiorna CLAUDE.md** quando cambia un FATTO stabile: un nuovo flag, un blob nuovo certificato,
  un fatto verificato dal codice, una regola nuova. CLAUDE.md deve restare vero. NON aggiornarlo per
  cose effimere (lo stato del task del giorno va nel file di STATO, non qui).
- **Aggiorna il file di STATO** (`STATO_CLAUDE_dev-spinoriale.md` o equivalente) a OGNI commit:
  dove siamo, quale strato, cosa manca, quale sigillo e' passato.
- Quando aggiorni CLAUDE.md o lo STATO, e' un commit dedicato con messaggio che dice cosa e' cambiato
  nelle regole/stato e perche'. Le regole si versionano come il codice.
- Se un fatto in par.9 si rivela superato dal codice, CORREGGILO qui (non lasciare un fatto stale:
  e' esattamente l'errore del docstring "ORFANO").

## 5-quater. IL REGISTRO DEI FRONTI APERTI (regola di Luca, 2026-09-15)
- **Lo stato dei fronti aperti sta in `doc/RAMIFICAZIONI.md`**, ed e' uno **STATO, non una cronaca**
  (la cronaca vive nei documenti di `doc/` e in `CLAUDECONNECT.md`).
- **Si aggiorna nello STESSO commit del riscontro che lo cambia** (par.5-bis): un registro aggiornato
  "dopo" e' un registro falso.
- **Le chiuse per DIMOSTRAZIONE e le chiuse per MISURA non si mescolano mai.** Le prime sono
  definitive; le seconde portano **sempre** la condizione che le renderebbe da rifare — e oggi
  quattro di esse sono misurate su un **settore ALIASATO** (~112 giri/passo), quindi **da rifare**.
- **Ogni voce ha un criterio di chiusura.** Una voce senza criterio non e' un fronte, e' un
  desiderio: va in una sezione a parte.
- **Un numero entra nel registro solo se e' gia' nel repo.** Il registro non e' il posto dove i
  numeri nascono.

## 5-ter. RELAZIONE A CLAUDE WEB — A OGNI RISCONTRO (regola di Luca, 2026-09-15)
- **A ogni riscontro di QUALSIASI tipo** — una misura, un'analisi, una simulazione, una lettura del
  codice, un sigillo che passa o che fallisce, una premessa che cade, un errore mio — **scrivi una
  RELAZIONE per Claude web con quello che hai VISTO, e committala e pushala.**
- **Subito, non a fine giornata.** Il riscontro si relaziona **nel momento in cui c'e'**, prima di
  passare al pezzo successivo. **Un riscontro non relazionato e' un riscontro perso:** chi legge il
  repo da fuori non ha la conversazione, ha solo i file.
- **Si scrive QUELLO CHE SI E' VISTO**, non quello che si spera: i NUMERI, con accanto il
  **valore-null / il riferimento** (par.9), e la provenienza (quanti semi, quanti passi, quale scena).
- **Valgono come riscontro anche, e soprattutto:** i risultati **negativi**, le ipotesi **refutate**,
  le premesse di un mandato che **non reggono al codice**, i **propri errori** e le **correzioni a
  fatti gia' scritti**. Non si relaziona solo quando funziona.
- **Dove:** un documento dedicato in `doc/` quando il riscontro e' un pezzo di lavoro, **PIU'** un
  paragrafo in `RELAZIONE_PER_CLAUDE.md`, cosi' chi legge solo quella e' comunque allineato.
- Vale **in aggiunta** a par.5 (politiche di commit) e par.5-bis (documenti vivi), non al loro posto:
  un riscontro che cambia un FATTO STABILE va **anche** in par.9, e lo stato **anche** nel file di STATO.

## 6. STATO E ORDINE DEL LAVORO
Ordine: **prima il FORK (non-abeliano), poi il resto.** GAMMA / Step 2 (cs<->orologio) / verifica
EM<->curvatura sono A VALLE: non toccarli finche' il fork non gira (a densita' reali cs e' MORTO,
I~0.05 vs soglia ~400 -> tutti i test cs-dipendenti oggi sono NULLI).

Il fork si costruisce a strati (ognuno un flag OFF, ognuno si riduce a quello sotto):
- **STRATO 0 — connessione Berry statica (arc-connection): IL PRIMO MATTONE.**
  `U_ij = exp(-i (chi/2) m_hat . sigma)`, `chi=arccos(n_i.n_j)`, `m_hat=(n_j x n_i)/|n_j x n_i|`.
  Peso antipodalita': `w_ij = |n_j x n_i| = sin(chi)` (NIENTE soglia netta, NIENTE coeff. tarato).
  Sostituzione nella forza (`_coppia_interferenza`, righe 2207-2208): `Im<psi_i|psi_j> -> w_ij * Im<psi_i| U_ij |psi_j>`.
  Flag OFF (es. `FORK_SU2=False`). Sigillo: OFF -> byte-identico scalare; ON+allineati -> scalare.
- **STRATO 1 — connessione con MEMORIA (ritardazione): FATTO** (2026-09-14, flag `FORK_SU2_MEM`
  / `--fork-su2-mem`, OFF di default; sigillo `csv/_seal_fork/_sigillo_strato1.py`, **23/23 PASS**).
  Realizzato come **ritardazione dei BLOCH**, non come memoria della matrice: `_bloch_ritardato()`
  rilassa il versore `n_ret` verso quello corrente con **slerp geodetico** e
  `alpha = 1 - exp(-dt_n/tau)`, `tau = d_nodo/cs_nodo`. Si rilassa il Bloch e NON U/N perche' un
  blend lineare di matrici uscirebbe da SU(2) (par.4). Il trasporto resta sugli spinori CORRENTI.
  **E' il pezzo che ACCENDE il fork:** rompe il teorema di inerzia dello Strato 0 (vedi par.9).
  Riduce a Strato 0 per tau->0 (esatto, 0.000e+00) e a riposo (5.3e-15).
- **STRATO 2 — memoria hebbiana saturata (relazionale):** `dg/dt=c_ij*g*(1-g/G(rho))/tau`, tetto
  `G(rho)` legato alla DENSITA' col GAMMA di cs ("sorelle non catena": G da rho, NON da cs diretto).
  Riduce a Strato 1 per g=cost.

**FATTO STABILITO (non ri-derivare male):** il trasporto attuale e' SCALARE (righe 2207-2208, stessa A
applicata ad a e b) -> il sistema e' abeliano per STRUTTURA -> l'olonomia e' banale (W=2) qualunque
cosa facciano gli spinori on-site. **La dinamica sugli ARCHI (arc-connection) e' il pezzo mancante:
senza, non c'e' olonomia.** L'evoluzione on-site esistente (`SPINORE_VIVO`, `KURAMOTO_SU2`) e'
COMPLEMENTARE (fornisce stati di nodo variati da trasportare), non sostitutiva.

## 7. DOCUMENTI DI RIFERIMENTO (cartella `doc/` del repo)
`doc/BUSSOLA_dev-spinoriale.md` (perche'/dove-va) · `doc/BUSSOLA_TECNICA_dev-spinoriale.md` v2
(dove/come, formule, flag, sigilli) · `doc/ROADMAP_fork_SU2.md` (in-che-ordine) ·
`doc/PROTOCOLLO_test_olonomia.md` (come misurare W(r)) · `doc/SYSTASIS_nota_concettuale.md`
(il concetto). Leggili PRIMA di lavorare sul fork (vedi par.0-bis).
NB: `ROADMAP_dev-spinoriale.md` (radice) e' la roadmap GAMMA/Step 2, A VALLE del fork (par.6).

## 8. PRINCIPIO GUIDA (per capire il "perche'")
"Lo spinore E' il tempo proprio della massa; da esso discendono l'interazione con la luce, con la
metrica, e l'aggregazione di spazio-tempo-materia." Ogni "-> nasce" e' un'IPOTESI da dimostrare
(derivazione, non innesto), non una rivendicazione. Verbo onesto: "dovrebbe emergere", non "genera".

## 9. FATTI VERIFICATI DAL CODICE (per non rifare errori gia' fatti)
- Trasporto forza = SCALARE: `_coppia_interferenza`, **righe 2207-2208**
  (`np.conj(_a)*(mat(A)@_a) + np.conj(_b)*(mat(A)@_b)`, stessa A su a e b) -> abeliano per
  struttura. VERIFICATO dal sorgente
  sul blob 4fc7a794 il 2026-09-13. **La riga 2196 citata in passato era il DOCSTRING, non il codice**
  (la funzione inizia a 2192, il docstring occupa 2193-2200): errore da par.0, corretto.
- cs = CS_M/(1+GAMMA*sqrt(I)) (riga 2187, `cs_floor`): vive SOLO nel settore metrica/gravita', MAI
  nell'orologio/EM. VERIFICATO dal sorgente il 2026-09-13.
- Orologio/EM (`_phc`, `omega_clk`, `ritmo()`, `dt_n=DT*r`): NON usa cs. Due tempi propri scollegati
  (metrico tau_p=d/cs vs orologio dt_n=DT*r). L'accoppiamento cs<->orologio e' lo Step 2 (non fatto).
- `_passo_spinoriale`: NON orfano (docstring stale), cablato dietro `SPINORE_VIVO` (OFF). E' ON-SITE
  (precessione dello spinore del nodo con memoria hebbiana + inerzia |Psi|^2), NON arc-connection.
- `PLAST_MIT=0` in TUTTI i test committati: la "compressione" osservata e' il regime di default
  (dimezzamento d0=d/2, "compressione degenere"), NON la generazione di spazio (mai girata).
- **`FORK_SU2_MEM` / `--fork-su2-mem` (STRATO 1, 2026-09-14):** la connessione `N_ij` si costruisce
  dai Bloch RITARDATI `self._nb_ret` invece che da quelli correnti. Metodo `_bloch_ritardato()`;
  stato per-nodo `_nb_ret` (ereditato dalla mitosi in `_eredita_spinore_figli`), cache
  `_cs_nodo_prev` e `_r_corrente` **scritte solo col flag ON** (da cui dipende la byte-identita'
  di S1: se un giorno servissero a ramo spento, il sigillo S1 va rifatto). Richiede `--fork-su2`;
  da solo viene IGNORATO con avviso. VERIFICATO dal sorgente sul blob 2277e9a0.
- **IL TIC DEI PROCESSI LOCALI E' `dt_n = DT*r`, NON `DT`** (fatto generale, non solo del fork).
  `DT` nudo e' il tempo di COORDINATA: usarlo dentro un rilassamento locale cancella la dipendenza
  dall'orologio del luogo, cioe' impone la foliazione sincrona globale = **un frame preferito, un
  "etere"**. Tutta la fisica del file integra gia' in `dt_n`/`dt_e` (phivel, tw); `DT` nudo vive
  solo nel conteggio dei sottopassi CFL. Preso una volta nello Strato 1 (bug dell'istruzione, non
  dell'esecuzione) e corretto. **Presidio permanente: il sigillo S7** (`_sigillo_strato1.py`), che
  misura `alpha` su nodi con ritmi diversi: con `dt_n` il rapporto r=2/r=1 vale 1.9753, col `DT`
  varrebbe esattamente 1.000. S1..S6 passavano IDENTICI col bug: senza S7 era invisibile.
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
- **BILANCIO DEI TASSI (misurato, 2 semi, 4163 coppie, 2026-09-15):** `tau_dec` (decorrelazione di
  una coppia padre-figlio) = **0.63 passi** su ENTRAMBI i semi; `tau_mit` locale = 187 / 210 passi
  -> rapporto **295 / 335**. **Dominio della distruzione.** Il confondente geometrico e' ESCLUSO,
  non stimato: all'eta' 1, con chi gia' a 89.7, la distanza e' INVARIATA (0.540 contro 0.539) e
  l'arco diretto e' vivo al **100%**. Decorrelano da ADIACENTI e CONNESSI.
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
- **`_tau` DELLA MEMORIA SPINORIALE E' ANCORATO A `TAU_A` PER IL NODO MEDIANO, PER COSTRUZIONE**
  (riga 1913, verificato 2026-09-15). `_tau = TAU_A * max(_dens/_dens_rif, 0.05)` con
  `_dens_rif = median(_dens[_dens > 1e-6])`: poiche' il riferimento e' la **MEDIANA**, per il nodo
  mediano `_dens/_dens_rif ~ 1` **sempre, a qualunque livello di maturazione**. Quindi
  `tau_mediano ~ TAU_A` (= 50, cioe' **5000 passi**) e **non scende mai**. Non e' un transitorio che
  si esaurisce: e' un **punto fisso auto-normalizzante**. Conseguenza operativa: **far maturare il
  sistema non puo', per costruzione, accorciare la memoria del nodo tipico** — quindi "aspettare"
  non e' una strategia valida per uscire da un problema che dipende da quella memoria.
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
- **PRESIDIO — `r^2` BASSO NON SIGNIFICA PENDENZA INCERTA** (2026-09-15). `SE_b = |b/r|*sqrt((1-r^2)/(n-2))`:
  il fattore dominante e' **`sqrt(n)`**, non `r`. Stessa pendenza e stesso `r = 0.32`: `SE` vale
  **0.108** con 20 punti, **0.0097** con 2195. Quindi una pendenza con `r^2 = 0.10` su 2195 nodi e'
  determinata a **+-0.01**. `r^2` basso dice che la relazione **spiega poca varianza**, non che la
  pendenza sia fragile. **Serve sempre `SE`, non `r`, per decidere se uno scarto e' significativo.**
- **`d/cs` E' PIATTO CONTRO L'INERZIA: pendenza +0.097** (`r = +0.351`, 2195 nodi; 2026-09-15,
  `doc/TAU_tempo_luce.md`). Quindi sostituire `tau = TAU_A*max(dens/dens_rif, 0.05)` (riga 1913) con
  il **tempo-luce `d/cs`** (lo stesso `tau` gia' cablato nello Strato 1) **romperebbe la
  cancellazione**: `theta` passerebbe da **-0.152** a fra **-0.69** (stima onesta, col residuo) e
  **-1.03** (stima naive). **MA L'AMPIEZZA NON RISOLVE:** `tau/DT` da **6500** a **66.5** passi, e
  poiche' `|omega|_eq ∝ sqrt(tau)` il fattore e' **0.101**: da **126.7 a 12.8 GIRI per passo**.
  **Un ordine di grandezza nella direzione giusta, e il settore resta ALIASATO. Non e' una cura.**
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
- Ancora elastica verso LAM (riga ~3234): e' a CORTO raggio (filtro_portata=1-tanh(d/LAM)), fissa la
  scala LOCALE (materia legata), NON blocca l'espansione a grande scala.
