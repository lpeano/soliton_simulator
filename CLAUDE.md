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
- Blob di riferimento certificato: `git hash-object soliton_simulator.py` -> **4fc7a794...**.
  Se diverso, le righe possono essere shiftate: cerca per NOME di funzione/flag, non per riga.

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
- **STRATO 1 — orientazione con memoria (rilassamento):** `dU/dt=(U^Berry-U)/tau`, tau=d/cs, primo
  ordine (vedi par.4). Riduce a Strato 0 per tau->0.
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
- Ancora elastica verso LAM (riga ~3234): e' a CORTO raggio (filtro_portata=1-tanh(d/LAM)), fissa la
  scala LOCALE (materia legata), NON blocca l'espansione a grande scala.
