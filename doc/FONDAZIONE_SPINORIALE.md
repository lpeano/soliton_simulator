# Il sistema dei solitoni relazionali spinoriali
## Descrizione fisica e leggi matematiche

*Documento fondativo del nuovo sistema — l'oggetto fondamentale è lo spinore che emette
il campo (visione del "solitone sfera-otto"). La materia emerge dall'interferenza non
distruttiva del campo spinoriale; il tutto vive su un grafo di adiacenza relazionale.*

---

## PARTE I — L'idea fisica

### 1. Cos'è un solitone

Un solitone è un **emettitore di campo pilotato da uno spinore**. Non è una fase scalare
che oscilla: è un oggetto geometrico — la "sfera con l'otto" — che vive nello spazio
degli spinori SU(2), e la cui rotazione *genera* il campo che si propaga nello spazio.

Ogni solitone porta:
- una **posizione** p nello spazio relazionale (dove sta nel grafo);
- uno **spinore** ψ (due componenti complesse, |ψ|=1) — la sfera-otto, il suo stato
  interno fondamentale;
- da ψ derivano tutte le sue proprietà osservabili: la direzione (dove punta), il segno
  di doppia-copertura (l'otto), e il campo che emette.

**Differenza cruciale dal sistema scalare precedente:** prima il campo era una fase φ
(un numero) e lo spinore era un'aggiunta; ora **lo spinore è fondamentale e il campo è
ciò che esso emette**. Il non-abeliano (SU(2)) non è attivato da un meccanismo — è la
natura stessa dell'oggetto.

### 2. Il substrato relazionale: il grafo di adiacenza

Il sistema **non ha uno spazio di sfondo**. I solitoni non vivono in una griglia data:
vivono nelle loro **relazioni**. Tutto è gestito da un **grafo di adiacenza**:
- **nodi** = i solitoni, ciascuno col suo spinore ψ_i;
- **archi** = le relazioni di vicinanza fra solitoni, pesate dal kernel di emissione
  w_ij = e^(−r_ij/λ);
- **la geometria emerge dal grafo** — le distanze, la curvatura, il pozzo gravitazionale
  sono proprietà relazionali, non di sfondo;
- **l'interferenza avviene sugli archi** — i solitoni si "parlano" solo con i vicini nel
  grafo.

*Il grafo di adiacenza è la struttura portante: lo spazio-tempo stesso emerge dalle
relazioni fra nodi, non è un contenitore preesistente.*

### 3. Perché SU(2) e la doppia copertura

Lo spinore vive su SU(2), il gruppo delle rotazioni "a doppia copertura": deve girare
**due volte** (4π) per tornare esattamente a sé stesso. Girando una sola volta (2π),
torna alla stessa direzione ma con il **segno opposto** — questa è "l'otto" della
visione: il percorso che si chiude solo dopo due giri.

Il segno di doppia-copertura (±) è quindi una proprietà **geometrica nativa** dello
spinore, non un'etichetta aggiunta. È dove vive lo spin ½.

---

## PARTE II — Le leggi matematiche

*Costanti del sistema (riferimenti di stato): portata base λ = 0.8 = 2 lunghezze di
Planck; saturazione γ = 0.05; accoppiamento K = 2.0; quanto di rotazione = 4π (doppia
copertura).*

### Legge I — Il campo emesso (il cuore del sistema)

Ogni solitone emette il suo spinore nel grafo, attenuato con la distanza. Il campo in un
nodo è la **somma degli spinori** dei solitoni adiacenti, ciascuno pesato dalla vicinanza:

> **Ψ_i = Σ_j  w_ij · ψ_j,   con  w_ij = e^(−|p_i − p_j| / λ)**

dove:
- Ψ_i è ora un **campo spinoriale** (due componenti complesse) nel nodo i, non un numero;
- w_ij è il **peso dell'arco** — quanto forte è la relazione fra i e j (portata λ);
- la somma è sui **vicini nel grafo di adiacenza** (j adiacente a i).

*Il campo in un nodo è la sovrapposizione delle "voci spinoriali" dei solitoni vicini.
Dove le voci concordano, il campo è forte e coerente; dove sono in disaccordo, si
cancellano.*

### Legge II — La materia dall'interferenza NON distruttiva

La materia è dove il campo spinoriale si somma **costruttivamente** (interferenza non
distruttiva); il vuoto è dove si **cancella** (distruttiva). La densità di materia è la
norma del campo:

> **ρ_i = Ψ_i† Ψ_i = |a_i|² + |b_i|²**

**Nel caso spinoriale, "non distruttiva" è più ricco che nel caso scalare.** Due spinori
possono essere:
- **identici** → si sommano pieni → **costruttiva → materia**;
- **antipodali** (opposti sulla sfera di Bloch) → si cancellano → **distruttiva → vuoto**;
- **stessa direzione ma SEGNO opposto** (differiscono di 2π sull'otto) → **si cancellano
  lo stesso** → distruttiva;
- **ortogonali** (a 90° sulla sfera) → interferenza **parziale** (quadratura).

**Conseguenza fondamentale — lo spin ½ struttura la materia:** perché l'interferenza sia
non distruttiva (materia), i solitoni devono concordare **in direzione E in segno di
doppia-copertura**. Il segno non è un'etichetta passiva: **entra nella formazione stessa
della materia**. Due solitoni che puntano nello stesso posto ma con segno opposto NON
fanno materia — si cancellano. È qui che lo spin ½ diventa costitutivo del mondo, non
solo una proprietà accessoria.

### Legge III — La saturazione (il campo non esplode)

Il campo grezzo viene saturato, così l'intensità resta finita anche dove molti solitoni
si sommano:

> **Ψ_saturato = Ψ_grezzo / (1 + γ · |Ψ_grezzo|)**

Satura al valore ±1/γ = ±20. È la stessa legge del sistema scalare, applicata alla norma
dello spinore.

### Legge IV — L'interferenza relazionale (la forza fra solitoni)

Due solitoni adiacenti si "sentono" attraverso l'**overlap dei loro spinori** — la
generalizzazione non-abeliana del coseno della differenza di fase:

> **overlap(i, j) = ⟨ψ_i | ψ_j⟩ = a_i* a_j + b_i* b_j**

Numero complesso che contiene **sia** l'allineamento di direzione **sia** la relazione di
segno:
- spinori identici → overlap = 1 (accordo pieno, attrazione);
- opposti → overlap = 0 (ortogonali);
- il segno/fase dell'overlap porta l'informazione di doppia-copertura.

*Nel limite in cui gli spinori sono semplici fasi (b = 0), l'overlap si riduce a
e^(i(φ_j − φ_i)), la cui parte reale è cos(Δφ) — la vecchia legge. La nuova generalizza
la vecchia.*

### Legge V — L'attrazione/repulsione (la prima forza: materia)

La forza fra due solitoni adiacenti deriva dall'overlap spinoriale e dal peso dell'arco:

> **F(i, j) = K · Re⟨ψ_i | ψ_j⟩ · (w_ij / λ)**

- overlap positivo (spinori in accordo) → **attrazione**;
- overlap negativo (antifase) → **repulsione**.

*La materia si lega dove gli spinori sono in accordo, come il legame chimico si forma fra
funzioni d'onda in fase.*

### Legge VI — La schermatura (la portata dipende dalla densità)

La portata effettiva del campo si accorcia dove la densità è alta:

> **λ_eff(i) = λ / (1 + softplus(u_i − 1)),   con u_i = ρ_i / ρ_critica**

Nel vuoto (u→0) la portata è massima (~0.61); nel nucleo denso si accorcia fino a un
pavimento. È la stessa legge, con ρ = norma spinoriale.

### Legge VII — La gravità bifase (la seconda forza: geometria)

La gravità nasce dall'allineamento degli spinori vicini e dalla torsione, e agisce sulle
**distanze** del grafo (la geometria), non sulla materia:

> **g(i, j) = −tanh(s_ij) · tanh(|∇pozzo|) · ⟨n_i · n_j⟩ · segno(∇pozzo)**

dove:
- n_i = ψ_i† σ ψ_i è la **direzione di Bloch** dello spinore (dove punta sulla sfera);
- ⟨n_i · n_j⟩ è l'allineamento delle direzioni — **la gravità è modulata dallo spin**;
- s_ij misura la torsione relativa al quanto di doppia-copertura;
- ∇pozzo è il gradiente del pozzo di densità nel grafo (dove "cadere").

*La materia coerente crea un pozzo; gli spinori allineati sentono la gravità piena; gli
spinori ortogonali la sentono spenta. Spin e gravità sono accoppiati alla radice.*

### Legge VIII — L'evoluzione dello spinore (come ruota la sfera-otto)

Ogni spinore ruota per effetto del campo che lo circonda, con una rotazione SU(2):

> **ψ_i(t+dt) = exp(−(i/2) Ω_i · σ dt) · ψ_i(t)**

dove:
- σ = (σ_x, σ_y, σ_z) sono le matrici di Pauli (i generatori di SU(2));
- Ω_i è la velocità angolare: memoria del moto (inerzia) + campo locale (torsione dei
  vicini nel grafo) + orologio proprio (massa/de Broglie);
- exp(−(i/2)Ω·σ dt) è la rotazione a doppia-copertura: dopo 4π riporta lo spinore a sé,
  dopo 2π gli dà il segno opposto.

*Questa è "la sfera che ruota". L'olonomia — il segno accumulato lungo un cammino chiuso
nel grafo — è la fase di Berry, ed è nativa: emerge dalla non-commutatività delle
rotazioni SU(2), non da un meccanismo aggiunto.*

### Legge IX — Il tempo proprio (l'orologio del solitone)

Ogni solitone ha il suo ritmo, che rallenta dove la torsione (la "massa") è alta:

> **τ_i = 1 + |torsione_i| / (quanto di olonomia)**

È il tempo proprio locale — la dilatazione temporale emergente. Più un solitone è
"massiccio", più lento è il suo orologio.

### Legge X — La creazione di coppie (materia e antimateria)

Dal campo possono nascere coppie solitone-antisolitone, con spinori a **segno opposto di
doppia-copertura**, nate nello stesso nodo del grafo e con olonomia globale conservata:

> **ψ_antisolitone = (segno di doppia-copertura opposto di ψ_solitone)**
> **conservazione: olonomia(coppia) = 0** (i due segni si bilanciano)

*Materia e antimateria hanno lo stesso spin (modulo) ma segno di doppia-copertura opposto
— come elettrone e positrone. Nascendo con segno opposto, un solitone e il suo antisolitone
interferiscono DISTRUTTIVAMENTE (Legge II): non fanno materia insieme finché non si
separano nel grafo.*

---

## PARTE III — La geometria di contatto

### Perché la geometria di contatto

La visione — lo spinore che *emette* un campo, con un ritmo proprio (l'orologio) e una
propagazione — ha la struttura naturale della **geometria di contatto**: la geometria dei
sistemi che evolvono con un "tempo" privilegiato e una struttura di fase. È il linguaggio
dei sistemi dinamici con un orologio (Hamilton-Jacobi, termodinamica, onde).

### 1. La struttura di contatto

Lo spazio degli stati del solitone non è solo la sfera (dove punta lo spinore): è la
sfera **più la fase di doppia-copertura** (l'otto) **più il tempo proprio** (l'orologio).
Questo spazio (dimensione dispari: le due coordinate della sfera + la fase) porta una
**forma di contatto**:

> **α = dφ_otto − p · dq**

dove:
- φ_otto è la coordinata sull'otto (il segno di doppia-copertura, la fase di Berry);
- q sono le coordinate sulla sfera (dove punta lo spinore);
- p sono i momenti coniugati (la velocità di rotazione);
- α è la **1-forma di contatto**: lega il ritmo dell'otto (dφ) al moto sulla sfera (p·dq).

*La forma di contatto lega il "tic" dell'orologio interno (l'avanzamento sull'otto) al
movimento della direzione dello spinore — un orologio che batte mentre la sfera ruota.*

### 2. Il campo di Reeb (il flusso del tempo proprio)

Ogni struttura di contatto ha un **campo di Reeb** R — la direzione lungo cui il tempo
proprio scorre uniformemente:

> **α(R) = 1,   dα(R, ·) = 0**

Il campo di Reeb è **l'orologio di de Broglie del solitone**: la direzione lungo cui lo
spinore avanza la sua fase di doppia-copertura a ritmo costante. La Legge IX (il tempo
proprio τ) è il flusso di Reeb.

*Un solitone fermo ruota sull'otto al ritmo della sua massa (de Broglie); il campo di
Reeb è questa rotazione — "come batte l'otto".*

### 3. La distribuzione di contatto = il grafo di adiacenza

La forma α definisce un **piano** in ogni punto (il suo nucleo, ker α): la
**distribuzione di contatto** ξ. È dove avviene l'interferenza fra solitoni — il piano
trasverso al flusso del tempo, dove gli spinori si sovrappongono (Legge IV).

> **ξ = ker α = {vettori v : α(v) = 0}**

**La realizzazione discreta di ξ è il grafo di adiacenza.** Gli archi del grafo — dove i
solitoni si parlano, interferiscono, si legano — sono la distribuzione di contatto vista
sul reticolo relazionale. Il campo di Reeb è il tempo (come scorre l'orologio); il grafo
di adiacenza è lo spazio (dove i solitoni interferiscono). La geometria di contatto
separa il "quando" (Reeb) dal "dove" (il grafo).

### 4. La non-integrabilità = il non-abeliano

La proprietà chiave della geometria di contatto è la **non-integrabilità**: la
distribuzione ξ **non** si chiude in superfici (dα|ξ ≠ 0). Questo è precisamente il
**non-abeliano**:

> **dα|ξ ≠ 0   ⟺   le rotazioni non commutano   ⟺   olonomia non banale**

*Questa è la ragione geometrica profonda per cui il solitone spinoriale è non-abeliano:
la sua struttura di contatto è non-integrabile. Percorrere un cammino chiuso nel grafo
(nella distribuzione ξ) accumula olonomia (la fase di Berry, il segno di doppia-copertura)
— esattamente perché ξ non è integrabile. L'otto che non si chiude in un giro è la firma
della non-integrabilità di contatto.*

### 5. Il legame con la doppia copertura

L'otto e la non-integrabilità di contatto sono la stessa cosa vista da due lati:
- **algebra:** lo spinore torna a sé dopo 4π (SU(2), doppia copertura);
- **geometria di contatto:** un cammino chiuso in ξ (nel grafo) accumula olonomia
  (non-integrabilità);
- **fisica:** lo spin ½ — il segno che cambia sotto rotazione di 2π.

Tre descrizioni di un unico fatto: **la sfera con l'otto è una varietà di contatto
non-integrabile, e lo spin ½ è la sua olonomia.**

---

## Sintesi

Il solitone spinoriale è un **emettitore di campo** (Legge I) la cui sorgente è uno
**spinore SU(2)** (la sfera-otto), che vive su un **grafo di adiacenza relazionale**
(nodi = solitoni, archi = relazioni pesate). Il campo emesso è spinoriale, quindi
l'interferenza (Legge IV) è non-abeliana per costruzione, e la **materia emerge
dall'interferenza non distruttiva** (Legge II) — che richiede accordo di direzione E di
segno di doppia-copertura, rendendo lo spin ½ **costitutivo della materia**.

Le forze (attrazione, gravità) e il tempo proprio derivano dal campo e dagli spinori,
preservando la fisica del sistema precedente ma sulla base giusta.

La **geometria di contatto** dà la cornice: la forma α lega il ritmo dell'otto al moto
sulla sfera; il campo di Reeb è l'orologio di de Broglie; la distribuzione ξ — realizzata
dal grafo di adiacenza — è dove i solitoni interferiscono; e la **non-integrabilità** di
ξ è la ragione geometrica del non-abeliano — l'olonomia, la fase di Berry, lo spin ½.

**L'ipotesi centrale da testare:** se il campo è spinoriale (l'oggetto giusto) e la
materia è l'interferenza non distruttiva sul grafo, il segno di doppia-copertura si ordina
perché la geometria di contatto non-integrabile lo seleziona — non perché un meccanismo
lo forza. È il test della visione: il solitone è la sfera con l'otto, la materia è la sua
interferenza costruttiva, e lo spin ½ è la sua olonomia nativa.

---

# AGGIORNAMENTO (post-verdetto Fase 3): il PRINCIPIO DI NON-ABELIANITA' TOTALE

## Il principio (il cuore, emerso dal verdetto Fase 3)

Lo spin-1/2 (il segno di doppia-copertura, l'olonomia) puo' ordinarsi SOLO se TUTTO il
sistema e' non-abeliano in modo COERENTE. Un sistema MISTO — dove l'emissione e' spinoriale
(SU(2), Fasi 1-3) ma l'EVOLUZIONE e' scalare (U(1)) — NON puo' ordinare il segno: la parte
abeliana lo "tira indietro" (l'ordine resta un repulsore, come nel sistema scalare, §48).

Verifica: l'evoluzione dello spinore (ω_new) usa `|self.psi|²` (campo SCALARE) per
l'inerzia -> il LOOP E' APERTO. Il verdetto Fase 3 negativo e' su un sistema misto, NON
sulla visione completa.

## La regola unica

Ovunque una legge legga una FASE (φ) o una DIREZIONE sola (nb), deve leggere lo SPINORE
PIENO (ψ) o l'OVERLAP ⟨ψ_i|ψ_j⟩. Fase = commuta (abeliano); spinore = non commuta (SU(2),
porta il segno). Applicata a OGNI componente (emissione, densita', forze, EVOLUZIONE,
memoria, coppie, mitosi, tempo proprio) -> non-abeliano coerente per costruzione.

PRESIDIO: riduzione-al-limite (spinori in fase -> la legge non-abeliana torna la vecchia).
La struttura e' il CASO LIMITE; il non-abeliano la generalizzazione. Nulla si perde.

## Stato delle leggi (non-abeliano / da fare)

- Legge I (campo emesso): NON-ABELIANO OK (Fase 1)
- Legge II (materia, interferenza non distruttiva): NON-ABELIANO OK (Fase 2) — il segno
  e' COSTITUTIVO della materia (accordo di direzione E segno)
- Legge III (saturazione): NON-ABELIANO OK
- Legge IV/V (interferenza/forze, overlap): NON-ABELIANO OK (Fase 3)
- Legge VI (schermatura, ρ=ψ†ψ): NON-ABELIANO OK
- Legge VII (gravita' bifase, nb nativo): NON-ABELIANO OK — accoppiata allo spin a due
  livelli (sorgente ρ_spin + modulazione nb·nb)
- Legge VIII (EVOLUZIONE dello spinore): DA RENDERE NON-ABELIANO (Fase 4) — lo spinore va
  ruotato dall'OVERLAP spinoriale (non da ω_new abeliano); inerzia = ρ_spin. E' la
  chiusura del loop.
- Legge IX (tempo proprio = campo di Reeb): DA FARE (Fase 5) — l'orologio batte sull'OTTO
  (4π, non 2π), IDENTIFICATO con la rotazione dello spinore (non un rotatore separato).
- Legge X (creazione coppie): DA RENDERE NON-ABELIANO (Fase 5) — la separazione segue
  l'overlap negativo, non la fase.

## Ipotesi da testare (Fase 4+)

A LOOP CHIUSO (evoluzione non-abeliana), la materia (interferenza non distruttiva) rende
l'ordine del segno un ATTRATTORE, e lo spin-1/2 emerge — dove nel sistema misto (loop
aperto) restava abeliano. ONESTA': dopo molti negativi la probabilita' e' bassa; se anche
a loop chiuso e' abeliano, e' un teorema di assenza definitivo; se si sblocca, era la
coerenza non-abeliana totale il pezzo mancante. La geometria di contatto (non-integrabile)
resta la ragione geometrica per cui il non-abeliano, se coerente, dovrebbe dare l'olonomia.
