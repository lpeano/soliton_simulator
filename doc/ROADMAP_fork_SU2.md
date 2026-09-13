# ROADMAP FORK SU(2) — cose da fare (con antipodalità)
### Aggiornata con: peso sin(χ), scuotimento del vuoto esistente, sigilli distinti.
*Da eseguire un pezzo alla volta, ogni pezzo un sigillo. NON tutto insieme.*

---

## PREPARAZIONE (a costo zero, prima di toccare il codice)
- **Fork** del branch dev-spinoriale (blob certificato 4fc7a794). Il ramo vecchio resta intatto
  come riferimento/baseline: se il non-abeliano demolisce, ci si torna in un secondo.
- **Decisione già presa:** usare la STESSA algebra spinoriale attuale anche nella parte non-abeliana
  sugli archi (link U_ij), e usare lo SCUOTIMENTO DEL VUOTO GIÀ ESISTENTE (non aggiungerne uno nuovo).

## PEZZO 1 — funzione U_ij(n_i, n_j) [isolata, testabile da sola]
Costruzione del link (trasporto parallelo geodetico, relazionale, zero parametri):
- χ = arccos(n_i · n_j)
- m̂ = (n_j × n_i) / |n_j × n_i|
- U_ij = cos(χ/2)·I − i·sin(χ/2)·(m̂·σ)   [2×2, SU(2), U_ji = U_ij† automatico]
SIGILLI Pezzo 1:
- allineati (χ→0) → U_ij → I  (identità)
- unitaria: U_ij U_ij† = I (conserva |ψ|=1)
- caso antipodale gestito dal PESO (Pezzo 2), NON da una convenzione d'asse arbitraria.

## PEZZO 2 — peso sin(χ) per l'antipodalità [il fix relazionale]
Ogni contributo d'arco alla forza va moltiplicato per:
- w_ij = |n_j × n_i| = sin(χ)
Comportamento: perpendicolari (χ=90°)→w=1 (asse netto); allineati (χ=0)→w=0 (innocuo, U→I);
antipodali (χ=180°)→w=0 (asse indeterminato → arco NON contribuisce, nessun asse inventato).
REGOLE: NIENTE soglia netta (no "if χ>179"). NIENTE coefficiente tarato (no e^{−k(...)}).
Solo la funzione continua sin(χ), derivata dalla geometria, zero parametri.
SIGILLO Pezzo 2 (riduzione al limite): allineati → w→0 e U→I insieme, contributo svanisce liscio;
antipodali → w→0, nessuna direzione entra nella forza. Verificare la continuità (no salti).

## PEZZO 3 — cablaggio nella forza [la sostituzione non-abeliana]
Alla riga ~2207-2208 (forza di interferenza), sostituire:
- Im⟨ψ_i|ψ_j⟩  →  w_ij · Im⟨ψ_i| U_ij |ψ_j⟩
U_ij MESCOLA a,b durante il trasporto (= il pezzo non-abeliano). NON è più separabile in
"trasporto di a" + "trasporto di b".
SIGILLO Pezzo 3: flag OFF / tutti allineati → BYTE-IDENTICO al ramo scalare attuale.
Attenzione all'ORIENTAMENTO dell'arco (U_ij = U_ji†): con gli scalari era irrilevante, ora conta.

## SCUOTIMENTO DEL VUOTO — usare quello ESISTENTE (non aggiungere)
Già nel codice (righe ~1884-1885), gated da SYNC_UPDATE and SCUOTIMENTO:
- a1 += (rng.normal(0,1,n) + i·rng.normal(0,1,n))·amp ; b1 += (idem)
- amp = √Lam/(1+I2/Lam), Lam=lambda_vuoto (globale), I2 per-nodo → forte nel vuoto, debole nella materia.
- RUMORE INDIPENDENTE per nodo (n estrazioni distinte) → rompe la degenerazione senza correlare i vicini.
- ISOTROPIA GIÀ VERIFICATA: "il momento angolare netto NON dipende dal vuoto stocastico" (riga ~114).
DA CONTROLLARE prima (lettura, gratis): che SYNC_UPDATE e SCUOTIMENTO siano ATTIVI nella config del fork.
Se spenti, lo scuotimento non gira e la degenerazione non si rompe.

## DIVISIONE DEI RUOLI (perché servono entrambi)
- SCUOTIMENTO (dinamico, preventivo): rompe la degenerazione GLOBALE (evita il vuoto degenere che non parte).
- PESO sin(χ) (strutturale, continuo): rende innocua ogni degenerazione LOCALE transitoria (no asse spurio).
Si rinforzano: lo scuotimento rende raro il caso degenere, il peso rende innocuo quel poco che resta.
SIGILLI DISTINTI: scuotimento → isotropia (⟨n⟩ nel tempo); peso → riduzione al limite (w→0 liscio).
Testarli UNO ALLA VOLTA, non insieme al primo colpo.

## VERIFICHE DINAMICHE (misure di Luca, poi lettura di Claude)
1. Distribuzione degli angoli χ tra vicini nel tempo:
   - resta SPARSA → il rumore vince, degenerazione rotta, settore non-abeliano vivo;
   - COLLASSA verso 0/π → una forza di allineamento domina il rumore → serve più calcio o meno allineamento
     (bilancio da tarare CON CAUTELA, presidio anti-manopola).
2. Olonomia di plaquette W = Tr(U_ij U_jk U_ki) (vedi PROTOCOLLO_test_olonomia.md):
   - W ≈ 2 ovunque → ancora abeliano (fork non ha portato struttura);
   - W ≠ 2, non-commutante, gobba sul BORDO delle masse → non-abelianità fisica emergente.
3. Isotropia: ⟨n⟩ persistente ≠ 0 → verso preferito spurio (bug di simmetria da cacciare).

## CAVEAT (onestà permanente)
- I link U_ij derivati dai soli Bloch sono "schiavi" della materia (no gradi di libertà propri):
  danno la non-abelianità CINEMATICA, forse non DINAMICA. Se serve vita propria: farli dipendere
  anche da cs e dal segno (che hanno dinamica propria) — DA COSTRUIRE E TESTARE, non è nel piano base.
- Non-abelianità ≠ unificazione ≠ gap 35 ordini di α_G. È un ingrediente necessario, non la meta.
- "In teoria funziona" = struttura coerente; se REALE (olonomia non-banale) e UTILE (media la forza)
  sono domande EMPIRICHE che solo il fork implementato e misurato risponde.

---
*Ordine: Preparazione → Pezzo 1 (+sigillo) → Pezzo 2 (+sigillo) → Pezzo 3 (+sigillo) →
controlla scuotimento attivo → verifiche dinamiche (Luca gira, Claude legge). Un pezzo, un sigillo.*
*Vedi anche: BUSSOLA, BUSSOLA TECNICA, PROTOCOLLO_test_olonomia, CLAUDE.md (regole dell'esecutore).*
