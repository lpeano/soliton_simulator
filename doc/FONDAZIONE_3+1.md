# FONDAZIONE 3+1 — il tempo proprio come QUARTA dimensione (spaziotempo relazionale)

## branch: dev-spinoriale — proposta (da testare, con presidi anti-trucco)

## Intuizione di Luca Peano; formalizzazione con il guardiano scientifico

---

## 0. CONTESTO E MOTIVAZIONE

Stato misurato (pilota pulito, calore isotropo, segno casuale):

- `segno_arco_coer` oscilla ~0 (segno frustrato, NON ordinato);
- `m0_Lz` ~0 (nessuna rotazione fisica);
- `spin_overlap_arco` ~0.76 (correlazione di DIREZIONE, non del segno);
- il sistema si comporta come U(1) (abeliano) nella dinamica, benche' lo spinore
sia C^2 (struttura SU(2)) nell'oggetto.

Reperto chiave (dimostrato): lo spinore HA la struttura SU(2) (2 componenti complesse,
sfera di Bloch S^2), MA la dinamica non attiva il segno di doppia-copertura (la fase
relativa delle due componenti). Il segno, da misura istantanea, e' impossibile da estrarre
pulito (teorema: le 3 proprieta' - limite +1, stabile, vede antimateria - sono mutuamente
esclusive); da perc_chi e' casuale; da cos(tw/2) e' la parita' del winding (non antimateria).

CONGETTURA (Luca): il segno non si ordina perche' e' un'ETICHETTA ASTRATTA in un sistema 3D
con tempo esterno. Se il tempo proprio diventa una DIMENSIONE (3D -> 3+1), il segno diventa
la POSIZIONE lungo la quarta coordinata (verso del tempo), quindi GEOMETRICO, non arbitrario.
E lo split materia/antimateria emerge dalla metrica, non da un decreto.

### 0.1 — DIAGNOSI 5.3a e BERSAGLIO GIUSTO (l'orologio INTERNO _phc)

Il pilota MOD 5.3a (`--tempo-segno`) ha firmato `dt_n` = il tempo proprio ESTERNO (il passo)
-> NO-GO (segno_arco_coer ~0, spin_overlap ~0.5, m0_Lz ~0). Bersaglio SBAGLIATO: firmare il
tempo esterno non pilota il segno di doppia-copertura.

BERSAGLIO GIUSTO: l'OROLOGIO de Broglie INTERNO, gia' isolato nel codice come
`_phc = np.exp(-0.5j * omega_clk * _dts)`. Il commento del codice lo dichiara: "pilota il SEGNO
non la DIREZIONE, vincola SOLO il segno di doppia-copertura". E' il termine che porta il verso
del tempo INTERNO (fase de Broglie), non il tempo esterno. La CONGETTURA di Luca in prospettiva
3+1: il verso sta nell'orologio interno; il segno diventa la POSIZIONE lungo la quarta coordinata,
geometrico. **La MOD 5.3c (`--orologio-segno`, firma di `_phc`) e' il PRIMO passo operativo verso il 3+1.**

---

## 1. LA STRUTTURA GEOMETRICA: da R^3 a R^{3,1}

### 1.1 Stato attuale (3D + tempo esterno)

- posizione: x_k in R^3 (pos, 3 coordinate);
- tempo: parametro ESTERNO t (il passo della simulazione), uguale per tutti;
- tempo proprio: fattore di DILATAZIONE tau_k = 1 + |tw_k|/PHI_CRIT (scalare, non coordinata);
- spinore: psi_k in C^2 (SU(2)), sfera di Bloch S^2 (interno).

### 1.2 Proposta (3+1, spaziotempo relazionale)

Ogni nodo acquista una QUARTA coordinata: il tempo proprio locale accumulato, FIRMATO.

X_k = (x_k^1, x_k^2, x_k^3, T_k)  in R^{3,1}

dove T_k e' il tempo proprio accumulato del nodo k, con VERSO dal segno:
dT_k/dt = s_k * tau_k^{-1}    (materia s_k=+1 -> T avanti; antimateria s_k=-1 -> T indietro)
con tau_k la dilatazione (dalla torsione), s_k il segno di doppia-copertura.

Metrica (Minkowski relazionale, locale):
ds^2 = -c_s^2 dT^2 + dx^2       (segnatura -+++, c_s = velocita' del segnale LOCALE)

dove c_s = c_s(x) e' la velocita' locale (--cs-dinamico), governata dalla densita'/metrica.
=> curvatura, c_s e tempo proprio sono la STESSA metrica (chiude l'intuizione precedente).

### 1.3 Feynman-Stuckelberg GEOMETRICO

L'antiparticella e' la particella sul foglio-tempo OPPOSTO: materia su T crescente,
antimateria su T decrescente. Non un'etichetta (+/-) astratta, ma la DIREZIONE lungo T.
Il segno di doppia-copertura = orientazione lungo la quarta coordinata.

---

## 2. LO SPLIT IMPLICITO (materia/antimateria) — EMERGENTE, non imposto

### 2.1 Il meccanismo (dalla metrica, non da un termine di soppressione)

L'interazione fra due nodi passa per la SINCRONIZZAZIONE dei tempi propri (legge sync,
K_SYNC): "dove i tempi propri sono simili, la sync ordina" (codice, riga 202). E il tempo
dell'arco e' dt_e = 0.5*(r_i + r_j) (media dei tempi propri, riga 2189).

Con tempo proprio FIRMATO (r_k = s_k * |r_k|):

- arco materia-materia (s_i=s_j=+1): dt_e = 0.5*(|r_i|+|r_j|) > 0 -> interagiscono NORMALMENTE;
- arco antimateria-antimateria (s_i=s_j=-1): dt_e = -0.5*(|r_i|+|r_j|) < 0 -> interagiscono
(entrambi indietro, sincroni fra loro);
- arco materia-antimateria (s_i=+1, s_j=-1): dt_e = 0.5*(|r_i|-|r_j|) ~ 0 -> ARCO CONGELATO
-> interazione QUASI IMPOSSIBILE.

CONSEGUENZA: lo split materia/antimateria e' IMPLICITO. Non si impone "materia interagisce
poco con antimateria" (che sarebbe un trucco): EMERGE perche' i tempi propri di verso opposto
danno dt_e ~ 0, e la sync ordina solo fra tempi simili. La causalita' relativistica separa i
due settori PER COSTRUZIONE.

### 2.2 Perche' questo e' fisica e NON trucco

- TRUCCO (respinto): aggiungere un termine di soppressione |accoppiamento(s_i, s_j)| che
penalizza s_i != s_j. Questo FORZA l'ordine del segno (i settori si separano perche' l'hai
imposto) -> il segno "si ordina" per decreto, non per dinamica.
- FISICA (proposta): lo split e' una CONSEGUENZA di dt_e = media dei tempi propri firmati.
Non aggiungi soppressione; usi la struttura esistente (dt_e) con il tempo firmato. Nel
limite tutta-materia (s_k=+1) tutto interagisce normalmente (byte-identico al 3D vecchio).

### 2.3 Il feedback potenzialmente VIRTUOSO (la speranza, da misurare)

Segno -> verso del tempo (T) -> split (dt_e~0 fra opposti) -> materia interagisce solo con
materia -> il segno di un nodo si RINFORZA con i vicini dello stesso segno (sync fra tempi
simili) -> segno piu' STABILE. Questo potrebbe risolvere il problema del segno oscillante:
non lo stabilizzi a mano, lo stabilizza la separazione geometrica. DA MISURARE (potrebbe
NON accadere: il segno potrebbe restare frustrato anche cosi').

### 2.4 — AGGANCIO SELETTIVO in 3+1 (la gravita' NON si separa)

PROBLEMA (osservazione guardiano): dt_e firmato con dt_e~0 congela l'arco materia-antimateria.
Ma dt_e governa ANCHE la geometria legittima (peq riga 2454, distanze d0 riga 2548). Congelare
dt_e congelerebbe anche la GRAVITA' fra materia e antimateria - il che e' SBAGLIATO: in fisica
materia e antimateria interagiscono gravitazionalmente (stessa massa), solo la loro dinamica di
spin/segno e' separata.

SOLUZIONE (aggancio selettivo, come 5.3a esteso a 3+1):
- dt_e FIRMATO (s_i|r_i| + s_j|r_j|) -> governa la DINAMICA del SEGNO / la sincronizzazione:
  qui dt_e~0 fra opposti separa i settori (lo split);
- |dt_e| MAGNITUDINE -> governa la GEOMETRIA (peq, distanze, gravita'): qui NON si congela,
  materia e antimateria restano accoppiate gravitazionalmente.
CONSEGUENZA: lo split e' nel SEGNO/tempo (dinamica interna), NON nella gravita'. Materia e
antimateria si separano nell'evoluzione dello spin, ma si vedono gravitazionalmente - come
in fisica. Il presidio '|dt_e| per la geometria' e' obbligatorio.

---

## 3. (rivista) COSTO O(N): localita' temporale TOPOLOGICA

PROBLEMA (osservazione guardiano): se |T_i - T_j| NON entra nella CREAZIONE degli archi, allora
dt_e~0 rende gli archi materia-antimateria INERTI (esistono ma non fanno nulla), ma NON li
elimina. Il NUMERO di archi resta lo stesso -> il costo NON si riduce (calcoli archi inerti,
spreco). O(N) NON e' garantito.

SOLUZIONE: la localita' temporale deve essere TOPOLOGICA, non solo dinamica:
- |T_i - T_j| entra nella CREAZIONE/esistenza degli archi: nodi con tempi propri molto diversi
  (|T_i - T_j| > soglia_T) NON creano un arco (non sono causalmente vicini in 3+1);
- cosi' il numero di archi resta O(N) (solo vicini nello spazio E nel tempo).
Se |T| governa solo la DINAMICA (arco inerte ma esistente), il costo resta O(N^2 archi
potenziali) - proibitivo. La localita' TOPOLOGICA e' il sigillo cruciale del costo.
soglia_T = una scala di sistema (es. legata a c_s * dt tipico), NON un parametro nuovo tarato.

Promemoria (costo relazionale, non griglia): il sistema e' RELAZIONALE (nodi con coordinate),
non su GRIGLIA. Aggiungere una coordinata T per nodo e' costo LINEARE (+1 colonna), NON N^4
(che sarebbe il costo di una griglia N^3 -> N^4). Il rischio O(N^2) non viene dalla dimensione
ma dagli ARCHI: solo la localita' topologica in T lo scongiura.

---

## 4. RIDUZIONE AL LIMITE E SIGILLI (anti-trucco)

Il 3+1 e' un CAMBIO FISICO deliberato (come Feynman-Stuckelberg), ma deve ridursi al 3D
vecchio nel limite corretto:

- LIMITE tutta-materia (s_k = +1 per ogni k): T_k tutti crescenti, dt_e = media positiva
normale, nessun arco congelato -> il sistema 3+1 diventa il 3D vecchio ESATTAMENTE
(byte-identico off, o con --spaziotempo off).
- Solo con antimateria (s_k = -1) presente: lo split emerge, la quarta dimensione si attiva.

SIGILLI:

1. OFF byte-identico (flag --spaziotempo off -> nessun cambio).
2. Riduzione al limite (tutta-materia -> 3D vecchio, esatto).
3. Localita' temporale TOPOLOGICA (GATE COSTO): archi ~ O(N) perche' |T_i-T_j| > soglia_T ->
   NESSUN arco (non solo arco inerte/dinamica). Verificare che il numero di archi resti O(N),
   NON O(N^2).
4. Causalita' relativistica (nessun loop: T decrescente dell'antimateria NON legge il futuro
globale; l'ordine di aggiornamento resta ETC t-1).
5. Conservazione (Sigma s_k somma-zero sulle coppie; l'energia/olonomia 4D conservata).
6. c_s dinamico coerente (c_s -> dt_e -> cono causale; verificare che c_s governi dt_e).
7. GRAVITA' INTATTA: la geometria (peq, distanze) usa |dt_e| MAGNITUDINE, NON si congela fra
   materia e antimateria. Verificare che l'attrazione gravitazionale materia-antimateria
   PERSISTA (lo split e' nel segno/tempo, non nella gravita').
8. INVECCHIAMENTO (GATE FISICA, ALPHA 2023): eta >= 0 per ENTRAMBI i settori. Materia e
   antimateria invecchiano in AVANTI (l'anti-idrogeno cade in giu' e invecchia); solo
   l'orologio INTERNO (spinore/fase) inverte. eta usa |dt_n| (magnitudine), mai il firmato.

### DICHIARAZIONE ONESTA (nel commit e nel doc)

Il verso opposto del tempo INTERNO dell'antimateria e' un POSTULATO di modellazione
(Feynman-Stuckelberg), NON un dato emergente. Il codice conferma: senza --tempo-segno, dt_n e'
magnitudine (tutto avanti). Il 3+1 ASSUME il verso (5.3a), non lo scopre. La scoperta, se c'e',
sara' nelle CONSEGUENZE non postulate: il segno si ordina? emerge rotazione? Il postulato e'
lecito (FS e' interpretazione standard; ALPHA 2023 vincola: gravita'/invecchiamento NON invertono).

---

## 5. LA DOMANDA (il verdetto che il 3+1 deve dare)

Con il tempo proprio come quarta dimensione (firmato dal segno) + c_s dinamico + split
emergente:
(a) il segno si ORDINA (segno_arco_coer sale e RESTA, vs oscillare ~0)? Il feedback
geometrico (split -> segno piu' stabile) funziona, o il segno resta frustrato?
(b) emerge una ROTAZIONE (m0_Lz != 0) dalla struttura 4D?
(c) il sistema diventa non-abeliano nella DINAMICA (segno attivo), o resta U(1) anche in 3+1?

ONESTA': il 3+1 e' la forma piu' FISICA del sistema (spaziotempo, split geometrico, segno
come coordinata). MA il pattern finora e' abeliano a ogni livello. Il 3+1 potrebbe:

- ATTIVARE il segno (il feedback geometrico lo stabilizza) -> non-abeliano emergente;
- oppure RESTARE abeliano (il segno frustrato anche in 4D) -> teorema di assenza definitivo,
su un sistema ora COMPLETO (spaziotempo). In entrambi i casi, e' il test piu' informativo:
a sistema 3+1 completo, se resta 0.5, l'abelianita' e' DEFINITIVA a ogni livello geometrico.

### 5.1 PRESIDIO CRITICO: distinguere ORDINE da SEPARAZIONE (obbligatorio)

`segno_arco_coer` sul sistema INTERO puo' salire per DUE motivi OPPOSTI:
- (A) ORDINE VERO: dentro il settore materia, il segno si ordina (i +1 coerenti fra loro);
- (B) SEPARAZIONE ILLUSORIA: gli archi materia-antimateria (che davano -1) sono CONGELATI, quindi
  `segno_arco` sale solo perche' hai TOLTO gli archi discordi, NON perche' il segno si e' ordinato.

PER DISTINGUERE, misura `segno_arco_coer` DENTRO UN SOLO SETTORE (solo archi materia-materia,
escludendo gli archi congelati/discordi):
- se sale ANCHE dentro il solo settore materia -> (A) ORDINE VERO (non-abeliano emergente, scoperta);
- se dentro il solo settore materia resta ~0 -> (B) SEPARAZIONE (il 3+1 separa i settori ma NON
  ordina il segno: nessuna scoperta, solo la geometria dello split che postuli).
SENZA questa misura, un `segno_arco` che sale sul sistema intero e' AMBIGUO e non va interpretato
come ordine.

---

## 6. RIASSUNTO MATEMATICO

- Spazio delle configurazioni: da R^3 x S^2(spin) x U(1)(fase) a R^{3,1} x S^2 x U(1).
- Quarta coordinata: T_k con dT_k/dt = s_k / tau_k (tempo proprio firmato dal segno).
- Metrica: ds^2 = -c_s(x)^2 dT^2 + dx^2 (Minkowski locale, c_s dinamico).
- Split materia/antimateria: implicito via dt_e = 0.5(s_i|r_i| + s_j|r_j|) ~ 0 fra segni opposti.
  AGGANCIO SELETTIVO: il segno/dinamica usa dt_e FIRMATO (split); la geometria/gravita' usa
  |dt_e| MAGNITUDINE (materia e antimateria restano accoppiate gravitazionalmente).
- Feynman-Stuckelberg: geometrico (antiparticella = foglio-tempo opposto).
- Costo: O(N) (relazionale, non griglia), garantito dalla localita' temporale TOPOLOGICA
  (|T_i-T_j| > soglia_T -> nessun arco), non solo dinamica.
- Presidio: riduzione al limite (tutta-materia -> 3D vecchio esatto).
- PRIMO PASSO OPERATIVO: la MOD 5.3c (`--orologio-segno`, firma dell'orologio interno `_phc`
  con `s_k` = sign(perc_chi) delle coppie) e' l'implementazione operativa iniziale verso il 3+1:
  firma SOLO il verso del segno di doppia-copertura (materia exp-, antimateria exp+), omega_clk
  invariata (S3b: solo verso, non velocita'); geometria/gravita'/eta restano magnitudine.
