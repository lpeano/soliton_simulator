# PROTOCOLLO — TEST DI OLONOMIA NON-ABELIANA
### Da eseguire QUANDO l'infrastruttura del fork SU(2) sarà implementata.
*Branch: fork di dev-spinoriale. Documento di progettazione: il test è disegnato PRIMA,
si esegue DOPO. Serve pure-read (misura, non muta la fisica).*

---

## 0. PRECONDIZIONE
Il test ha senso SOLO dopo che i link U_ij ∈ SU(2) sono nel codice E hanno passato il
sigillo di riduzione al limite (allineati → U_ij → I → byte-identico al ramo scalare).
Se la riduzione al limite non passa, FERMARSI: il test misurerebbe un bug, non la fisica.

## 1. COSA MISURA
L'olonomia di plaquette W = Tr(U_ij · U_jk · U_ki) su un triangolo chiuso (i,j,k).
- W ≈ 2 (traccia dell'identità in SU(2)) → trasporto banale → ABELIANO.
- W ≠ 2, e cicli diversi NON commutano → connessione NON-ABELIANA genuina.
Fisicamente: W = angolo solido sotteso dalle direzioni di Bloch n_i, n_j, n_k sulla sfera.
Bloch complanari → W banale; non complanari → W ≠ 2.

## 2. COME SI TROVANO LE PLAQUETTE (non si scelgono: le trova la topologia)
Una plaquette = tre nodi mutuamente connessi (i-j, j-k, k-i TUTTI presenti nel grafo).
Algoritmo: per ogni arco i-j, i vicini COMUNI di i e j chiudono i triangoli (intersezione
delle liste di adiacenza). Il grafo (nodo connesso ai vicini geometrici) è ricco di triangoli.
- CONVENZIONE DI VERSO FISSA (es. ordine crescente di indice): il verso opposto dà W^{-1}.
  Fissarla PRIMA. Documentarla.
- Campione rappresentativo (non serve enumerare tutti i triangoli ridondanti).

## 3. LA SCALETTA (quattro livelli, in ordine)
1. **W GLOBALE** — media su tutti i triangoli campionati. BASELINE (atteso ~banale: il vuoto domina).
2. **W NEI PICCHI** — triangoli con densità alta: peso ρ_ijk = (|ψ_i|²+|ψ_j|²+|ψ_k|²)/3
   sopra una soglia. SOGLIA FISSATA PRIMA di guardare W (anti bias di selezione).
3. **W SUL BORDO** — triangoli dove il gradiente di densità |∇ρ| è grande.
4. **GRADIENTE RADIALE W(r)** ← la misura decisiva.
   - Definire il centro della massa = massimo locale di ρ. Definire r = distanza (geodetica
     sul grafo o metrica) dal centro. DEFINIRE centro e r PRIMA, non aggiustare dopo.
   - Tracciare W in funzione di r: dal centro (r=0) verso il bordo (r=R) verso il vuoto (r≫R).

## 4. LA PREVISIONE FALSIFICABILE (la firma da cercare)
W(r) deve avere una GOBBA a raggio intermedio:
- **CENTRO (r≈0): W basso** — massa coerente → Bloch allineati → χ≈0 → U≈I → olonomia banale.
- **BORDO (r≈R): W MASSIMO** — i Bloch cambiano direzione (dentro→fuori) → χ grande →
  il gradiente di direzione È la curvatura → olonomia massima.
- **VUOTO (r≫R): W basso e rumoroso** — Bloch deboli e casuali.
→ FIRMA della non-abelianità fisica = PICCO di W(r) sul bordo, con centro e vuoto bassi.
Una gobba al posto giusto è difficile da falsare per caso (a differenza di un singolo numero grande).

## 5. I VERDETTI
- **W(r) piatto ~2 ovunque** → connessione ABELIANA anche col fork → il change non ha portato
  la struttura sperata (o i link sono degeneri). Risultato onesto: la non-abelianità non emerge.
- **W(r) con gobba sul bordo, centro/vuoto bassi, RIPRODUCIBILE su più masse** → NON-ABELIANITÀ
  FISICA emergente, concentrata dove la fisica la mette. Il fork ha funzionato.
- **W grande MA solo nel vuoto / non riproducibile / dipende dalla soglia** → ARTEFATTO. Non fidarsi.

## 6. I PRESIDI (anti-autoinganno)
1. Riduzione al limite passata PRIMA (§0).
2. Soglie e definizioni (centro, r, soglia densità) fissate PRIMA di guardare W.
3. Il VUOTO è il controllo: la coda a r≫R deve essere piatta e bassa. Se W è alto ovunque,
   il "segnale" è un artefatto globale, non una struttura.
4. MEDIA SU PIÙ MASSE (le 3, o le 6 del test a 3+3): riproducibile = struttura; una sola = rumore.
5. Verso delle plaquette coerente (W coniugato se inverti).
6. Pure-read: la misura non muta stato/RNG (snapshot, byte-identico dopo la misura).
7. NON dedurre il verdetto nel codice: l'analizzatore STAMPA W(r) e le distribuzioni; il verdetto
   lo legge Luca sul dato.

## 7. IL LEGAME COL PROGRAMMA (perché questo test conta)
- Se la gobba c'è: hai una connessione non-abeliana REALE, concentrata sui bordi delle masse.
- Come la gobba SCALA con densità/dimensione della massa = il coarse-graining / l'amplificatore
  di loop visto in coordinate SPAZIALI. Lega il fork al dubbio sull'RG nascosto nel loop.
- Poi la domanda successiva: il vortice non-abeliano MEDIA la forza? (le masse interagiscono
  attraverso di esso?) → test a 3 masse, e poi a 6 (3+3): due vortici interagiscono?

## 8. NOTA DI SCALA (onestà permanente)
Anche una gobba pulita NON dimostra l'unificazione né copre il gap di 35 ordini in α_G.
Dimostra che il sistema è genuinamente non-abeliano — un ingrediente necessario, non la meta.
Un pezzo alla volta.

---
*Vedi anche: BUSSOLA (perché/dove-va), BUSSOLA TECNICA (dove-sta/come), ROADMAP (in-che-ordine).*
