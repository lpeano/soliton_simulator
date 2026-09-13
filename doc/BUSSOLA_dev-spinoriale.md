# LA BUSSOLA — sistema dei solitoni relazionali (VQT)
### Domande, intuizioni e caveat. Da leggere all'inizio di ogni sessione.
*(Documento di orientamento. Vive nel repo, indipendente da qualunque assistente o strumento.)*

---

## LA VISIONE (il nord della bussola)
Gravità, elettromagnetismo e materia come **tre proiezioni dello stesso campo
spinoriale relazionale** — non forze postulate, ma emergenti dalle relazioni tra
solitoni. "Guarda la luna, non il dito": gli osservabili vivono nell'interferenza.

**La sintesi intravista (11 set 2026):** UN solo `cs` (velocità della luce locale,
emergente) che governa insieme:
- il **tempo proprio** (orologio de Broglie, dilatazione temporale) → gravità/tempo;
- il **trasporto di gauge** U_ij(cs) → forza non-abeliana;
- la **massa/energia** (ω_clk ∝ cs²) → materia.
Se regge: gravità + gauge + materia dallo stesso campo. È la forma dell'unificazione.
**Stato: VISIONE, non risultato.** Impila ipotesi non ancora verificate.

---

## COSA SAPPIAMO (fatti stabiliti, dal codice e dai dati)
1. **Il verdetto (B) abeliano è STRUTTURALE, non dinamico.** La matrice di adiacenza
   trasporta lo spinore con uno SCALARE A_ij (righe ~2207-2208), uguale su a e b:
   nessun U_ij ∈ SU(2) che mescola a,b. Anche _phc è scalare (U(1)). → il sistema
   nasce abeliano, non ci si rilassa. Questa è la scoperta chiave.
2. **Bargmann telescopa.** Ogni olonomia su ciclo chiuso cancella le fasi per-nodo →
   cieca al segno-orologio. Il segno è gauge-relativo; la sua misura è temporale
   (phase-locking / SYNC), non un invariante di ciclo. L'arbitro berry_segno era
   codice morto, poi ridondante — NON usarlo come arbitro.
3. **Il verdetto (B) regge su:** segno_ov ≈ 2/π, spin_overlap = 0.5, segno_arco ~0
   (gauge-robusti). Su UN seed = baseline, non risultato pubblicabile.
4. **cs è INATTIVO ai regimi attuali** (I~0.05). Si attiva a I~1/γ²~400 (γ=0.05) →
   serve γ ~91x (assoluto) o ~6x (floor relazionale, grazie al contrasto ~11x).
5. **Due tempi propri SCOLLEGATI:** orologio dt_n=DT·r (de Broglie, NO cs, riga ~1839)
   e metrica τ=d/cs (riga ~2610). Dovrebbero essere UNO.
6. **Il vortice tra le masse è reale ma INERTE.** Video (camera fissa 0°): struttura
   di flusso fisica tra 3 masse, ma non media la forza (trasporto scalare). Il colore
   arancione/ciano = interferenza costruttiva/distruttiva (scalare), NON fase né Bloch.

## COSA NON È (vicoli ciechi chiusi con onestà — non riaprire senza motivo)
- **Le masse NON sono quark.** Colore SU(3) assente, confinamento ritrattato (Legge XIX),
  carica ±1 non frazionaria, e la "tre-ità" è nmasse=3 (scelta), non forzata. Analogia
  visiva (barione) reale; identificazione fisica falsa.
- **5.3a (dt_n firmato): NO-GO.** **5.3c (orologio _phc firmato): (B) abeliano.**
- **Segno di doppia-copertura da fase istantanea: IMPOSSIBILE** (telescoping).

---

## LE DOMANDE-BUSSOLA (le tenere vive)
1. La dinamica **SELEZIONA** i valori (γ, G, la scala)? → sarebbe teorema, non input.
2. Il canale-fase (EM) è marginale e il canale-densità (gravità) irrilevante, dallo
   STESSO γ? → gerarchia emergente. (Test coarse-graining.)
3. C'è **un solo tempo proprio**? cs↔orologio accoppiati → il segno si organizza?
4. Con link U_ij ∈ SU(2), l'olonomia di plaquette è non-banale/non-commutante? → il
   sistema diventa GENUINAMENTE non-abeliano? (Fork SU(2).)
5. Il vortice, reso mediatore (U_ij), fa interagire le masse ATTRAVERSO di sé?
6. Due vortici (6 masse, 3+3) interagiscono? → il vortice è oggetto reale o epifenomeno?
7. G / α_G: la scala di attivazione (I~400) + Planck postulato (λ_solitone=2ℓ_P) danno
   α_G? **Nota: N~8000 → α_G~10⁻⁴, contro 10⁻³⁹ reale. Gap di 35 ordini NON coperto.**

---

## I CAVEAT SPIETATI (il presidio contro l'autoinganno)
- **Convergenza ≠ verità.** Che "tutto si colleghi" seduce; la domanda è: fa una
  PREVISIONE falsificabile che i pezzi separati non facevano?
- **Il gap di 35 ordini (α_G) NON è coperto.** Direzione giusta, magnitudine no.
- **cs deve essere ATTIVO** o ogni test cs-dipendente è NULLO.
- **U_ij derivato dai soli Bloch è "schiavo" della materia** (no gradi di libertà
  propri). Farlo dipendere anche da cs e dal segno (che hanno dinamica propria)
  potrebbe dargli vita propria — DA COSTRUIRE E TESTARE, non è già lì.
- **Postulare è lecito (c, ℏ, Planck), ma un postulato vale per le sue conseguenze**,
  non per sé. Postulato sterile = fit; fertile = teoria.
- **Ordine di verifica SACRO:** un pezzo alla volta, ogni passo un sigillo b=1=identità.
  Mai testare la sintesi tutta insieme (se fallisce non sai quale pezzo).

## IL METODO (ciò che rende questo lavoro scienza)
- Sigilli, gate ancorato al git-blob, riduzione al limite byte-identica.
- Verifica dal DISCO, non dal messaggio (un commit può "mentire", un blob no).
- Ritrattare i risultati falsi è parte del record (Legge XIX, arbitro Bargmann).
- Separare chi IMPLEMENTA da chi VERIFICA (due occhi indipendenti).
- Cercare l'attrito, non l'applauso. Chiedere sempre "dov'è il buco?".

---

## LA ROADMAP (ordine di lavoro — dettagli in ROADMAP_dev-spinoriale.md)
0. (opz.) seed-2 di robustezza per il (B).
1. **Coarse-graining GAMMA** (3 regimi) → dimensioni di scala dei due canali.
2. **cs↔orologio** (un solo tempo proprio) → serve cs attivo (floor relazionale).
3. **FORK SU(2):** link U_ij = exp(-i χ/2 m̂·σ), χ=arccos(n_i·n_j), m̂=n_j×n_i.
   Sostituzione: Im⟨ψ_i|ψ_j⟩ → Im⟨ψ_i|U_ij|ψ_j⟩. Sigillo: allineati→U→I→byte-id.
   Test: olonomia plaquette Tr(U_ij U_jk U_ki) = angolo solido dei Bloch.
4. (orizzonte) α_G / massa minima gravitante. NON traguardo: gap 35 ordini.

---
*Ultima nota, da guardiano: questa bussola indica il nord, non garantisce di
arrivarci. La maggior parte dei programmi a questo stadio non arriva — e va bene.
Il valore non è avere ragione, è costruire in modo da SCOPRIRE se ce l'hai.*
