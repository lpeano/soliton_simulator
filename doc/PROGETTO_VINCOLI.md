# PROGETTO «VINCOLI» — la stessa nave, con i vincoli al posto dei campi
(Luca, 22 novembre 2026, 22:07–22:53; il guardiano ha scritto, Luca ha deciso. Carta prima del codice. Il ramo `vincoli` nasce da `lapse-u` e, finché le pote di sez. 6 non si aprono, contiene SOLO carta.)

## 0. Il principio (la stella polare)
I vincoli si applicano, i campi non si impongono. Il lapse N non è un campo con un'equazione: è ciò che si aggiusta perché un vincolo locale sia soddisfatto. Il precedente nel modello è Gauss: U(1) non fu imposto, nacque dal vincolo della carica. La gravità si fa allo stesso modo con l'energia. Va via χ (κ, f, la sorgente); restano, verificati al bit, il cammino, le bande, il solitone, Gauss, lo zero, la mitosi con le cure.

## 1. La sagoma (il metodo)
I vincoli non si leggono da un buco ma dai rapporti fra tutti i buchi: doc/SAGOMA.md, 15 proporzioni misurate, 5 mancanti, la tabella del giudizio (CURA / TOPPA / NULLA). Ogni passo di questo progetto si giudica contro TUTTA la sagoma. Un passo che migliora una riga e ne peggiora un'altra è una toppa e non entra nel nucleo. La sagoma è in prospettiva (2D, favo, tick, reticolo finito): le proporzioni «dell'animale» si distinguono da quelle «della prospettiva» solo cambiando punto di vista (M3).

## 2. I tre pezzi, in ordine
### A. Il lapse come moltiplicatore, sul tick di oggi
N(x) non da χ ma dal vincolo: l'energia (il libro dei conti, con lo zero dichiarato prima: la cima della banda, S2) si conserva localmente attorno a ogni nodo, e N è il valore che lo rende vero. Nessuna costante libera. Prima prova: Eötvös (S4) deve scendere da 0,12–0,14 sotto l'1% senza che nessuno glielo chieda. Si fa sul motore di oggi, a tick, nel nucleo congelato di lapse-u, come forma del lapse (file nuovi), DOPO il torneo [M1631].
### B. La mitosi come chiusura dello spazio
Su un reticolo la simmetria che genera i vincoli si rompe in proporzione alla curvatura per cella (Bahr–Dittrich); il rimedio è raffinare dove la curvatura si concentra. La mitosi fa questo con il grilletto giusto: Θ = π Σ(dτ_i − dτ_j) è la misura di quanto il vincolo del tempo NON chiude lì. Un nodo nasce dove la chiusura fallisce. Due condizioni da misurare (M2, mitosi e gravità nella stessa corsa): (B1) Θ residuo attorno al nato deve SCENDERE, non spostarsi ai vicini; (B2) la sagoma del mattone non deve cambiare quando il reticolo si infittisce (stessa ω, stessa m*, stessa caduta, w riscalata: il test GAMMA di settembre, con un nome nuovo). Limite dichiarato: la mitosi infittisce lo SPAZIO; il vincolo del TEMPO lo chiude il pezzo A (e poi C). Le due idee sono le due metà: la mitosi chiude lo spazio dove il tempo non torna; il lapse chiude il tempo dove lo spazio non basta.
### C. Il motore a strati: i vincoli nelle code
Il tick globale è provvisorio. Il tempo di un nodo è il numero di eventi che lo riguardano; il lapse è una frequenza di ammissione; la mitosi è ciò che accade quando nessun evento è ammissibile.
- C1 La coda: un heap in processo, deterministico (prontezza causale; a pari prontezza l'indice del nodo). NON un broker, NON thread che pescano eventi. La storia degli eventi è un'impronta committabile.
- C2 Gli strati: a ogni giro si aggiornano TUTTI i nodi pronti, per colori (le mezze fasi insieme; Grover per nodo; lo spostamento per arco), dentro ogni colore in parallelo (numba prange). Lo strato non è un tick: un nodo partecipa solo se pronto; il suo tempo proprio è il numero di strati a cui ha partecipato. Caso noto: nel reticolo uniforme tutti pronti a ogni strato = il tick di oggi AL BIT.
- C3 I vincoli come proiettori, non come porte (Luca 22:49): tutti i modi ammissibili esistono e si applicano INSIEME, con i pesi che conservano la norma (è la moneta di Grover; è il cammino quantistico; è Gauss sul reticolo, dove gli stati fisici sono quelli che il vincolo annulla). Un evento = «applica la somma unitaria delle mosse ammissibili». Nessuna scelta, nessuna regola di precedenza, nessun sorteggio.
- C4 Energia conservata = algebra chiusa: proiettare e poi evolvere conserva la norma solo se il vincolo commuta con l'evoluzione (prima classe). Il controllo che può fallire: la norma dopo un passo filtrato dal vincolo = quella di prima, al bit.
- C5 La mitosi come unitarietà che chiede spazio: dove il sottospazio ammissibile di un nodo è vuoto, nessuna evoluzione unitaria continua; la norma ha bisogno di una dimensione in più: nasce un nodo. Lo spazio nasce perché l'energia non può sparire. Verifica sul codice di oggi: la nascita conserva la norma totale al bit? (da controllare in O1–O8, non da supporre).
- C6 La riproducibilità dal primo giorno: sha1 dello stato per strato + log degli eventi; la ripresa da uno stato intermedio ridà la stessa storia al bit (come P8 oggi con k). Il registro e le impronte si riscrivono sul conteggio, non su k.

## 3. Le domande aperte (da chiudere sulla carta prima del codice di C)
- Q1 Il vincolo è LOCALE e DECIDIBILE sulla stella del nodo (il nodo e i suoi sei archi)? Se servisse una somma globale, torna la barriera, cioè il tick. L'energia del libro dei conti si lascia scrivere così?
- Q2 La non linearità come vincolo. «Tutti i modi insieme» è lineare; il legame materia–vuoto (α che satura a +s) non lo è: la somma di due stati ammissibili non evolve come la somma delle evoluzioni. O il mattone si riscrive come stato che soddisfa un vincolo (non come onda che si autoattrae), o la sovrapposizione vale solo dove la materia è rada. Si ricollega al torneo: stiamo cambiando il segno di quel termine ora.
- Q3 Lo stallo: vincoli troppo stretti = nessun nodo ammissibile, lo spazio esplode di nascite; troppo laschi = il tick di oggi. La fascia buona la decide la forma del vincolo: se per restarci servisse tarare, si è tornati a imporre.
- Q4 Quale c: la banda dice 0,566 s, il solitone 0,588 s (S7). Il motore a strati deve ridare le due velocità com'erano.

## 4. Le prove a costo zero (in memoria, L 16, senza toccare niente; si possono fare SUBITO sul ramo vincoli come file nuovi)
- Z1 La confluenza del tick di oggi: i pezzi applicati nodo per nodo in due ordini (indice crescente; decrescente; lotti alternati) contro il tick vettoriale. Previsione: fasi e legame commutano (diagonali); Grover e spostamento no; scarto fra gli ordini ~ s² (70%). Se passa al bit, il motore a strati è una riscrittura del CICLO, non della FISICA.
- Z2 Gauss come proiettore sul tick di oggi: il passo filtrato dal vincolo di Gauss; quanti nodi non passano (vuoto puro: nessuno, 90%; con un mattone: solo il bordo, 60%); la norma conservata (C4); nessuno stallo (80%).
- Z3 La norma alla nascita: nelle 9 nascite registrate, Σρ prima e dopo, al bit (C5).
- Z4 Θ residuo attorno ai nati nelle 9 nascite (B1): scende o si sposta.

## 5. Cosa NON è questo progetto
Non è un'era nuova (Luca, 16:31: «niente era 3»): il mondo è lo stesso, cambia il collegamento col tempo (A), si misura la mitosi come chiusura (B), e si cambia il CICLO del motore (C). Non è un campo unico né un campo a un angolo (quella idea è a verbale altrove, non si fa). Non usa broker, thread liberi, sorteggi, né manopole: ogni costante che comparisse è un allarme.

## 6. Le pote (gates): il codice entra solo quando la porta si apre
- G0 (ora): solo carta e le prove Z1–Z4 in memoria.
- G1: il torneo [M1631] chiuso con la tabella del giudizio; la forma predefinita decisa da Luca. Si apre il pezzo A.
  - **G1 APERTA** (2026-11-23, [M0528]): il torneo chiuso con `doc/referti_l2/TORNEO_FINALE.md` del ramo `lapse-u` (08de784c): nessuna forma cambia il segno della gravita'; FH TOPPA, FT DANNO, (c) DANNO, il fondo la banda piatta; la forma predefinita F0 (decisione di Luca, 23/11). Il pezzo A (il lapse come moltiplicatore: N dal vincolo, non da chi) comincia dalla carta, sul ramo `lapse-u` (file nuovi, fuori dal nucleo).
- G2: A dà Eötvös sotto l'1% su almeno un collegamento, senza peggiorare S2, S3, S5 (CURA, non TOPPA). Si apre C1–C2 (il motore a strati col tick uniforme come caso noto al bit).
- G3: Z1 passata e C2 al bit col tick di oggi. Si apre C3–C5 (i vincoli come proiettori, la mitosi dallo stallo).
- G4: M2 (mitosi e gravità insieme) con B1 e B2. Da qui la sagoma si rilegge da un altro punto di vista (M3).
Se una porta non si apre, si scrive perché, con il numero, e NON si passa alla successiva.

## 7. Le previsioni del guardiano (scritte il 22/11, prima di tutto)
- A: il vincolo di energia locale più semplice dà Eötvös sotto l'1% al 35%; lascia A cos δ com'è al 70%.
- B1 passa (60%); B2 fallisce al primo colpo (65%): i nati portano ancora il favo.
- Z1: scarto ~ s² fra gli ordini (70%). Z2: come scritto. Z3: la norma alla nascita è conservata al bit (55%). Z4: Θ residuo scende (60%).
- C nel suo insieme: il caso noto (tick uniforme al bit) passa (85%); C4 (norma conservata col proiettore di Gauss) passa (75%); con un vincolo di energia scritto per primo, C4 fallisce (60%): l'algebra non si chiude al primo tentativo.
