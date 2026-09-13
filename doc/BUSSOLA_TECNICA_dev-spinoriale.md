# BUSSOLA TECNICA — soliton_simulator.py (branch dev-spinoriale) — v2
### Dove stanno le cose nel codice, le formule, i flag, i sigilli, il gauge dinamico.
*Documento tecnico completo. Numeri di riga APPROSSIMATIVI (verificare col blob corrente).*
*v2 integra: antipodalità (peso sin χ), olonomia corretta (fattore 1/2), gauge dinamico a strati.*

> Blob certificato di riferimento: `git hash-object soliton_simulator.py` -> **4fc7a794...**
> Se diverso, le righe possono essere shiftate: cercare per nome di funzione/flag.

---

## 1. L'ALGEBRA DELLO SPINORE
- Stato per nodo: `_psi_spinor` forma **(n, 2)** complessa -> `psi=(a,b)`, con `|a|^2+|b|^2=1`.
- **Bloch -> spinore** (`_bloch_a_spinore`, ~riga 955-966):
  `a = cos(th/2)`, `b = sin(th/2)*exp(i*ph)`. Il **th/2** = doppia copertura (spinore torna a 4pi).
- **Spinore -> Bloch** (mappa di Pauli, `_nb_grav`, ~riga 2018-2028):
  `n = psi^dag . sigma . psi = (2Re(conj(a) b), 2Im(conj(a) b), |a|^2-|b|^2)`. **Perde il segno**
  (gauge-inv -> gravita' cieca al segno).
- **Pauli:** sx=[[0,1],[1,0]], sy=[[0,-i],[i,0]], sz=[[1,0],[0,-1]]. Non commutano: sx*sy=i*sz != sy*sx.
- Estrazione (th,ph) dal campo: `th=2*arccos(|a|)`, `ph=angle(b)-angle(a)`.

## 2. LE FORMULE CHIAVE
- **Velocita' luce locale / metrica:** `cs = CS_M/(1 + g*sqrt(I))`, `I=|psi|^2`, **CS_M=2.0, g(GAMMA)=0.05**.
  Attivazione nonlineare: `g*sqrt(I)~1` -> `I~1/g^2=400`. Run reale I~0.05 -> **inattivo** (fattore ~8200).
- **Tempo proprio METRICO** (gravita'): `tau_p = d/cs` (~riga 2610). Usa cs.
- **Tempo proprio OROLOGIO** (de Broglie/EM): `dt_n = DT*r`, `r=ritmo()` (~riga 1620, 2227). **NON usa cs.**
- **Fase orologio (evoluzione spinore)** (~riga 1839-1840):
  `_phc = exp(-0.5j * s_k * omega_clk * _dts)` ; `a1*=_phc ; b1*=_phc` (= U(dt), th/2, scalare/U(1)).
- **Forza di interferenza** (~riga 2207-2208):
  `K_C * Im( conj(a)*(mat(A)@a) + conj(b)*(mat(A)@b) )` = `K_C*Sum_j A_ij*Im<psi_i|psi_j>`.
  **A_ij SCALARE** applicato uguale a `a` e `b` -> **trasporto ABELIANO** (la scoperta chiave: il sistema
  nasce abeliano per STRUTTURA, non per dinamica).
- **Coarse-graining** (`_fattori_coarse(B)`, ~riga 173): `(B^(1/3), B^(-1/2), B^(1/2))` =
  (lambda, gamma, ampiezza). Costruito perche' `gamma*campo` sia INVARIANTE -> B=1 identita', similarita' classica.

## 3. IL LOOP RELAZIONALE (tempo-luce-materia)
`rho=|psi|^2 -> cs -> orologio(w prop cs^2) -> fase(_phc) -> campo emesso -> rho`
- Passo 1 (rho->cs): c'e'. Passo 3-4-5: ci sono. **Passo 2 (cs->orologio): NON c'e'** (orologio usa r, non cs).
- Chiuderlo = **Step 2** (accoppiamento cs<->orologio): in `_phc` fare `omega_clk *= (cs/CS_M)^2`.
  Sigillo: `cs=CS_M -> fattore 1 -> byte-identico`.
- **systasis:** rho=|psi|^2 e' la "systasis" (coerenza d'interferenza) nell'interpretazione — il codice la
  chiama `massa`/`rho`. Ipotesi (da dimostrare): all'uscita del deserto diventa la massa misurata,
  con alpha_G=(m/m_Planck)^2. Vedi SYSTASIS_nota_concettuale.

## 4. IL CHANGE NON-ABELIANO — connessione SU(2) sugli archi (fork)
La topologia del grafo NON cambia. Cambia il CONTENUTO degli archi: da scalare A_ij a matrice U_ij in SU(2)
che MESCOLA a,b durante il trasporto. La non-abelianita' vive nei CICLI (olonomia), che il grafo gia' contiene.

### 4.0 — Costruzione del link (connessione geometrica di Berry)
- `chi = arccos(n_i.n_j)` ; `m_hat = (n_j x n_i)/|n_j x n_i|`
- `U_ij = cos(chi/2)*I - i*sin(chi/2)*(m_hat.sigma) = exp(-i (chi/2) m_hat.sigma)` [2x2, SU(2), U_ji=U_ij^dag auto]
- Sostituzione nella forza (~riga 2207-2208): `Im<psi_i|psi_j> -> w_ij * Im<psi_i| U_ij |psi_j>`
- Attenzione all'ORIENTAMENTO dell'arco (U_ij=U_ji^dag): con gli scalari era irrilevante, ora conta.

### 4.1 — Antipodalita': PESO sin(chi) (NON convenzione d'asse)
Quando i Bloch sono antipodali (chi=pi), l'asse m_hat e' indeterminato. NON scegliere un asse (imporrebbe
un verso all'universo). Invece PESA il contributo d'arco:
- `w_ij = |n_j x n_i| = sin(chi)`
- perpendicolari (chi=90)->w=1 ; allineati (chi=0)->w=0 (innocuo, U->I) ; antipodali (chi=180)->w=0
  (asse indeterminato -> arco NON contribuisce, nessun asse inventato).
- REGOLE: NIENTE soglia netta ("if chi>179"). NIENTE coefficiente tarato (e^{-k(...)}). Solo sin(chi),
  derivato dalla geometria, zero parametri.
- SIGILLO: allineati -> w->0 e U->I insieme (svanisce liscio); antipodali -> w->0 (nessuna direzione spuria).

### 4.2 — Olonomia di plaquette (il test)
- Plaquette = tre nodi mutuamente connessi (triangolo del grafo). Trovarli: vicini comuni di ogni arco.
- `W = Tr(U_ij * U_jk * U_ki)` ; **W = 2*cos(Omega/2)**, con Omega = angolo solido dei Bloch. Il **fattore 1/2
  e' la doppia copertura** (spin-1/2). W=2 -> banale (abeliano). W!=2, non-commutante -> non-abeliano.
- Convenzione di VERSO fissa (verso opposto -> W^{-1}). Vedi PROTOCOLLO_test_olonomia per la scaletta
  completa (globale/picchi/bordo/gradiente radiale W(r)).

### 4.3 — GAUGE DINAMICO a strati (vita propria relazionale, zero manopole)
La connessione 4.0 e' CINEMATICA (schiava dei Bloch). Per darle vita propria, a STRATI — ognuno si
riduce al precedente, catena di sigilli fino allo scalare. Implementare UNO STRATO ALLA VOLTA.

- **STRATO 0** = connessione Berry statica (4.0+4.1). Cinematica. SIGILLO: allineati -> byte-identico scalare.

- **STRATO 1 — orientazione con MEMORIA (rilassamento):**
  `dU_ij/dt = (U_ij^Berry - U_ij)/tau_ij`, con `tau_ij = d_ij/cs` [tempo metrico GIA' esistente, zero manopole].
  IMPLEMENTAZIONE: rilassamento NELL'ALGEBRA di Lie (slerp/geodetica in SU(2)), NON blend lineare di
  matrici (uscirebbe da SU(2)): rilassa il vettore asse.angolo, poi ri-esponenzia.
  Da' MEMORIA/inerzia -> non piu' schiavo. SIGILLO: tau->0 -> U=U^Berry -> byte-identico Strato 0.
  STABILITA': puo' oscillare -> sigillo (norma, no NaN, no runaway).

- **STRATO 2 — forza del link: MEMORIA HEBBIANA SATURATA:**
  Il link ha forza `g_ij` che cresce dove l'interazione e' coerente (Hebb) ma satura per densita'.
  `c_ij = Re<psi_i|psi_j>` (coerenza, misurata SUGLI SPINORI).
  `dg_ij/dt = c_ij * g_ij * (1 - g_ij/G(rho_ij)) / tau_ij` (Hebb logistica: cresce se c>0, satura a G(rho)).
  **TETTO RELAZIONALE — "SORELLE, NON CATENA":** `G(rho) = G0*sqrt(rho)/(1+g*sqrt(rho))` legato alla DENSITA'
  rho con lo STESSO g di cs. NON legare G a cs direttamente: cs e G sono SORELLE della stessa madre rho
  (non figlia dell'altra) -> evita il loop annidato memoria<->cs<->rho<->memoria (instabile).
  Forza completa: `F_i = K_C * Sum_j w_ij * g_ij * Im<psi_i| U_ij |psi_j>`.
  SIGILLO: g_ij=costante (Hebb off) -> Strato 1. STABILITA': Hebb pura diverge; la saturazione G(rho) e' il
  freno EMERGENTE (non manopola). Verificare g_ij <= G(rho) sempre (no runaway).

### 4.4 — Strada alternativa GIA' NEL CODICE: `--kuramoto-su2` (par.46)
Torque ON-SITE: ruota lo spinore intero verso la media SU(2) dei vicini, asse variabile nb x nb_bar
(non commuta). Default off, stato NON verificato. DIVERSO da 4.0 (on-site vs connessione sull'arco).
Da esaminare/confrontare prima di scrivere 4.0 da zero (potrebbe coprire parte del lavoro).

### 4.5 — Presidi trasversali del fork
- **Spinore NON eliminato:** il link (archi) LEGGE gli spinori (nodi): c_ij, U^Berry, rho vengono dai
  nodi. Freccia causale spinore->link (i nodi guidano, gli archi ricordano). Se gli spinori diventassero
  passivi (link li comanda) -> BUG, da rilevare.
- **Zero manopole:** tau=d/cs, G(rho) con g gia' esistenti. Se scegli un numero nuovo, ti sei fermato sul dito.
- **Catena di riduzioni al limite:** Strato 2->(Hebb off)->1->(tau->0)->0->(allineati)->scalare. Ogni anello
  un sigillo byte-identico. Se un anello si rompe, STOP li'.

## 5. FLAG PRINCIPALI (config campagna attuale)
`--batch --nmasse 3 --sep 8 --passi 800 --ogni 100 --campo-spinoriale --spinore-vivo`
`--spinore-corretto --chi-core --calore-scal --deparam-orologio --verlet` + firma del braccio.
- `--campo-spinoriale`: campo emesso dallo spinore (rho_spin, nb, forze = overlap).
- `--orologio-segno` (5.3c): `_phc` firmato con s_k=sign(perc_chi). Richiede `--deparam-orologio` o e' inerte.
- `--tempo-segno` (5.3a/b): verso materia/antimateria. Richiede campo-spinoriale+spinore-corretto.
- `--sync-fase-orologio` (par.43): Kuramoto sul SEGNO (fase globale, nb invariante). Cura del loop-segno.
- `--kuramoto-su2` (par.46): Kuramoto SU(2) NON-ABELIANO (spinore intero). <- rilevante per il fork (4.4).
- `--cs-dinamico`: attiva cs variabile (ma inattivo a bassa densita').
- `--scala B`: coarse-graining (similarita' classica, invariante per costruzione).
- **SCUOTIMENTO DEL VUOTO** (~riga 1884-1885, gated da SYNC_UPDATE and SCUOTIMENTO): rumore complesso
  isotropo indipendente per nodo su a,b, amp=sqrt(Lam)/(1+I2/Lam). Rompe la degenerazione dei Bloch (serve
  al fork, insieme al peso sin chi). Isotropia GIA' verificata (riga ~114). Controllare che sia ATTIVO.

## 6. I DIAGNOSTICI / METRICHE (gauge-robuste vs no)
- **Gauge-robuste (fidati):** `segno_ov_absmedia` (~2/pi=0.637 se frustrato), `spin_overlap_arco`
  (=0.5 se casuale). Base del verdetto (B).
- **Gauge-dipendenti (cautela):** `segno_arco*` (frame-locale, convenzione canon).
- **MORTE/ridondanti (NON usare come arbitro):** `berry_segno*` e `berry_spin*` (telescopano -> cieche
  al segno-orologio). Verificato: berry_segno_media == berry_spin_media.
- **Nuove per il fork:** olonomia W(r) (par.4.2), distribuzione angoli chi tra vicini (rottura degenerazione),
  <n> (isotropia — verso preferito spurio?). Vedi PROTOCOLLO_test_olonomia.
- Presidio carica: per-coppia, append-only, +-1, Schwinger bilanciato.

## 7. I SIGILLI OPERATIVI (rito, in ordine)
1. **b=1 / OFF = IDENTITA' byte-identica** (`max|A-B|=0.000e+00`). Se fallisce -> STOP.
2. **Riduzione al limite:** ogni change nuovo torna al comportamento vecchio nel limite (scalare/allineato/
   tau->0/Hebb-off). Catena completa fino allo scalare.
3. **Purezza pure-read:** i diagnostici non mutano stato ne' RNG (snapshot esteso, byte-id).
4. **Norma |psi|=1**, no NaN/inf. **Stabilita'** (per i loop di feedback e Hebb: no runaway, g<=G(rho)).
5. **Unitarieta' SU(2):** U_ij^dag U_ij=I preservato anche DURANTE l'evoluzione (Strato 1), non solo all'inizio.
6. **Gate ancorato al git-BLOB:** il timbro vale per i byte esatti (un commit puo' "mentire", un blob no).
7. **Verifica dal DISCO, non dal messaggio di commit.**

## 8. PROCESSO (regole Luca)
- Ogni commit = push. Messaggi approfonditi (cosa/perche'/come/numeri/cosa-ricontrollare).
- Commit PRIMA di ogni run (riproducibilita'). Dati+script committati col verdetto.
- STATO_CLAUDE_dev-spinoriale.md aggiornato a ogni commit. ROADMAP + BUSSOLA per l'orientamento.
- Un fronte alla volta sul codice verificato. Separare chi implementa da chi verifica.
- **Divisione economica:** Claude (chat) pensa/scrive il codice; Claude Code applica (o Luca incolla a mano);
  Luca gira sulla sua macchina (gratis); Claude legge gli output committati e verifica (basso costo).

## 9. RISPARMIO (piano personale)
- **Esecuzione sulla TUA macchina** (Python, gratis) — mai run pesanti via agente a pagamento.
- Assistente = pensiero/progettazione/revisione (leggero). Dai TU il contesto (righe, pezzo di ROADMAP),
  non far esplorare il repo all'agente (li' evaporano i crediti).
- Costa la LETTURA dell'output nel contesto, non il calcolo (che e' CPU tua). Tu giri e committi cieco;
  Claude legge una volta e verifica. Sigilli con verdetto secco/exit-code = lettura minima.
- Sessioni brevi e mirate. Un fronte alla volta = disciplina scientifica E economica.

---
*Questa bussola dice DOVE e COME. La BUSSOLA concettuale dice PERCHE' e DOVE-VA. La ROADMAP_fork_SU2
dice IN-CHE-ORDINE. Il PROTOCOLLO_test_olonomia dice COME-MISURARE. SYSTASIS definisce il concetto.
CLAUDE.md dice come si COMPORTA l'esecutore (regole, sigilli, commit) ed e' l'unico file autorevole
per quel ruolo.*
