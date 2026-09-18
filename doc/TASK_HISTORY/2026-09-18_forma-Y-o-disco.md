# TASK HISTORY — **la forma della regione densa: Y o disco?**

**Data:** 2026-09-18 · **Branch** `fork-su2` · **HEAD alla scrittura** `2b0a19f`
**Blob:** `a1ae5090` — **e non cambierà.** **Nessuna cura, nessun run nuovo per la parte a tre masse.**

---

## 1. RAGIONAMENTO PRELIMINARE

### 1.1 Perché questa misura può rispondere **prima** del run a due masse

**La Y non è una forma: è una TOPOLOGIA.** Tre bracci con un punto triplo **non possono esistere fra
due masse** *(un segmento non ha giunzioni)*, mentre **un disco esiste uguale.**

> **Se la regione interna è un disco, la predizione di Luca perde il suo meccanismo ancora prima di
> essere testata — ed è meglio saperlo adesso.**
> **E i dati ci sono già:** i sei `.pkl` del run a tre masse (`10/115/190/270/375/400`).

### 1.2 ⚠ LA SOGLIA SU `rho_spin` VA DERIVATA, NON SCELTA (A1)

**Scelta, dichiarata:** **`rho_spin > mean(rho_spin)`** — cioè **sopra il livello di vuoto della
STESSA grandezza**. È l'analogo esatto di `lambda_vuoto = mean(|psi|²)` che il codice usa già come
energia del vuoto (`:486-494`), applicato a `rho_spin` invece che a `I`.

**⚠ Perché NON uso `lambda_vuoto` stesso:** `lambda_vuoto` è la media di **`|psi|²`**, e `rho_spin`
è **`psi_spin†psi_spin`** — **due grandezze diverse su due campi diversi.** Confrontarle sarebbe un
**errore di popolazione** (A3c). **La soglia deve venire dalla stessa grandezza che seleziona.**

**⚠ E la riserva su A3, dichiarata:** `mean(rho_spin)` **è** una statistica della propria
popolazione. **Qui è una SOGLIA DI SELEZIONE, non la normalizzazione di una legge dinamica** — il
divieto di A3 riguarda le leggi. **Ma per non fidarmi di una soglia sola, riporterò i risultati a
`1×` e a `10×` la media: se la forma cambia con la soglia, la forma non è un fatto.**

### 1.3 ⚠ IL VALORE SOTTO IPOTESI NULLA DI `A_m`, e senza non si legge niente

`A_m = |Σ_k rho_k · e^{i·m·θ_k}| / Σ_k rho_k`.
**Per `N` punti CASUALI e pesi uguali, `A_m` NON vale 0: vale `~1/√N`.**

> **Su `N = 200` nodi il nullo è `0.071`. Un `A_3 = 0.1` non significherebbe NIENTE.**
> **Riporterò `A_1`, `A_2`, `A_3`, `A_6` INSIEME AL LORO NULLO `1/√N_eff`**, con
> `N_eff = (Σrho)²/Σrho²` *(il numero efficace di nodi coi pesi, non il conteggio)*.
> **Senza il nullo, l'istogramma è un disegno.**

### 1.4 ⚠ LA TRAPPOLA CHE IL MANDATO NOMINA, e come la chiudo

**`A_3` grande potrebbe venire dalle TRE MASSE stesse, non da una Y interna.**
**Riporto DUE valori sempre:** `A_3` **con** l'anello e `A_3` **sulla sola regione interna**
(`r < R_anello(t)/2`, con `R_anello` **misurato**). **Se la Y c'è solo col primo, è l'artefatto
delle masse seminate.**

### 1.5 Cosa NON so, e cosa NON mi aspetto

**Non ho una predizione mia sulla forma.** *(L'osservazione è di Luca ed è **visiva**: questo
mandato serve a metterla alla prova, non a confermarla.)*

**⚠ E una cosa che dichiaro prima perché non diventi una scoperta a posteriori:** la Y a 120° è la
soluzione di **Fermat-Steiner** per tre punti e compare in sistemi molto diversi. **Se esce, NON è
una spiegazione: è una forma.** **Il nome non è il meccanismo, e non nominerò niente.**

**E il controllo ③ del mandato — autovalori del tensore d'inerzia — NON discrimina da solo:** un
disco dà `λ1 ≈ λ2`, **ma anche una Y simmetrica**. **Lo riporto come controllo, dichiarandolo tale.**

---

## 2. PROGETTAZIONE

**Sui sei `.pkl` a TRE masse già esistenti** *(nessun run nuovo)*, e poi **sugli stessi istanti del
run a due masse** quando ci sarà.

**Passo 0 — planarità:** verificare che `|z|` sia trascurabile rispetto a `r`, **altrimenti la
proiezione sul piano è essa stessa un'assunzione.**
**Passo ① — istogramma angolare** dei nodi densi, **contrasto `(max−min)/media`**, **e la sua
evoluzione nel tempo.**
**Passo ② — `A_1, A_2, A_3, A_6` col NULLO `1/√N_eff`**, **dentro e fuori l'anello.**
**Passo ③ — controllo geometrico:** raggio di girazione contro disco equivalente, e gli autovalori
del tensore 2D **— dichiarato come controllo.**

**LE LETTURE, FISSATE ADESSO** *(le quattro del mandato)*:
- **tre picchi, `A_3` ben sopra il nullo, e la Y NELLA REGIONE INTERNA** → **struttura topologica: a
  due masse non può esistere, e la predizione di Luca ha un MECCANISMO;**
- **istogramma piatto, `A_3` al livello del nullo** → **è un DISCO: l'osservazione visiva non regge,
  e si scrive che l'impressione era sbagliata;**
- **`A_3` grande SOLO includendo l'anello** → **è l'artefatto delle tre masse seminate**, non una
  struttura nuova;
- **tre picchi che si formano e POI si dissolvono** → **è un TRANSITORIO, e va detto QUANDO.**
- **⚠ E una mia:** **se la forma cambia al cambiare della soglia** (`1×` contro `10×` la media),
  **la forma non è un fatto e va dichiarato tale.**

**COSA MI FA FERMARE:** nulla di tecnico. **Nessuna identificazione, qualunque forma esca.**

---

## 3. TODO DEL NEXT STEP

- [ ] **§1 sui `.pkl` a TRE masse** *(non costa un run)* → **riporta**
- [ ] le stesse misure sul run a DUE masse **quando c'è** → **il confronto**
- [ ] referto + registro + relazione **nello stesso commit** + **CHECKPOINT**
- [ ] **⚠ NON toccare:** niente cure, niente soglie scelte, nessuna identificazione
