# Analisi tecnica — Solitone spinoriale (lo spinore emette il campo)

## Il principio

**Visione (Luca, dai 12 anni):** un solitone è un *emettitore di campo gestito da uno
spinore* — la "sfera con l'otto" (SU(2)) che pilota l'emissione del campo. La materia è
l'interferenza NON distruttiva del campo; il tutto vive su un grafo di adiacenza.

**Cosa fa il codice oggi (verificato):** il campo φ (U(1), scalare) è **fondamentale**;
lo spinore è **derivato/parallelo**. Gerarchia: **campo → spinore**.

**L'inversione:** rendere lo **spinore fondamentale**; il campo Ψ **emesso dallo
spinore**. Gerarchia: **spinore → campo**. Il fondamentale diventa SU(2) (non-abeliano
per costruzione), non U(1) (abeliano).

**Perché conta:** il sistema attuale è abeliano perché il *fondamentale* (il campo Ψ,
che tutto usa) è U(1). Se il fondamentale è lo spinore (SU(2)), il non-abeliano è
*incorporato*, non attivato. Le vie fallite testavano meccanismi sopra un campo abeliano;
qui si cambia l'oggetto, non il meccanismo.

---

## Il substrato: il grafo di adiacenza (invariato)

Il grafo di adiacenza resta la struttura portante, ESATTAMENTE come nel sistema attuale:
- **nodi** = solitoni (ora ciascuno con spinore ψ_i invece della sola fase φ_i);
- **archi** = relazioni di vicinanza, pesate w_ij = e^(-r/λ) (il `_mat(w)` esistente);
- **l'interferenza** (Ψ_i = Σ_j w_ij ψ_j) avviene sugli archi;
- **la geometria** (distanze, pozzo, curvatura) emerge dal grafo.

=> il codice del grafo (adiacenza, pesi, mitosi che aggiunge nodi/archi) si PRESERVA
INTATTO. Cambia solo cosa "vive" sui nodi (spinore invece di fase) e cosa si somma sugli
archi (spinori invece di e^{iφ}).

---

## Il punto di rottura - dove tutto si decide

**`calcola_psi()` (riga ~1905, 1 riga chiave):**
```python
F = self._mat(w) @ (amp * np.exp(1j * self.phi))   # <-- Ψ da e^{i·φ} (SCALARE)
self.psi = self.satura(F)
```

Il campo `self.psi` (complesso scalare) è costruito da **e^{i·φ}**, sommato con kernel
`e^{-r/λ}` (in `_mat(w)`), poi saturato. **Da qui nasce tutta la fisica** (Ψ è letto da
~15+ punti: densità |Ψ|², gravità, forze, mitosi, coerenza).

**L'inversione in una riga:** Ψ costruito dallo **spinore** invece che da e^{i·φ}:
```python
# NUOVO (dietro flag): Ψ spinoriale = somma pesata degli spinori con kernel
F_spin = self._mat(w) @ (amp[:,None] * self._psi_spinor)   # (n,2) complesso
self.psi_spin = satura_spinoriale(F_spin)                   # campo a 2 componenti
```

**Il campo passa da scalare (n,) complesso a spinoriale (n,2) complesso.**
Il kernel `_mat(w)` (il grafo di adiacenza pesato) e' lo STESSO - si applica alle 2
componenti invece che allo scalare.

---

## La materia = interferenza NON distruttiva (spinoriale)

Nel sistema scalare: densita' rho = |Psi|^2, grande dove le fasi concordano (costruttiva).
Nel sistema spinoriale: rho = Psi_spin^dag Psi_spin = |a|^2 + |b|^2, MA la costruttiva/
distruttiva ora dipende dall'INTERO spinore:
- spinori identici -> costruttiva (materia);
- antipodali -> distruttiva (vuoto);
- STESSA direzione ma SEGNO opposto (differenza di 2pi) -> DISTRUTTIVA lo stesso;
- ortogonali -> parziale (quadratura).

**Implicazione tecnica chiave:** la materia (interferenza non distruttiva) richiede
accordo di direzione E di segno di doppia-copertura. Il segno di doppia-copertura ENTRA
nella formazione della materia (rho). Quindi lo spin-1/2 e' costitutivo della densita',
non un'etichetta. => la densita' rho e' l'osservabile dove verificare se il segno si
ordina (materia coerente = segni concordi).

---

## Cosa va toccato (mappa dell'intreccio)

### A. Il campo (il cuore del cambio)
| oggi | nuovo |
|---|---|
| `self.psi` : (n,) complesso scalare | `self.psi_spin` : (n,2) complesso spinoriale |
| `F = _mat(w) @ (amp·e^{iφ})` | `F = _mat(w) @ (amp·ψ_spinore)` |
| densita' `|ψ|²` | densita' `ψ†ψ` = |a|²+|b|² (norma spinoriale) |

### B. Le leggi che LEGGONO Ψ - da adattare (fisica preservata, forma riscritta)
1. **Densita' rho = |ψ|²** -> `rho = ψ_spin† ψ_spin` (norma spinoriale). Fisica identica.
2. **Gravita' bifase** (∝ nb·nb) -> nb ora **dal campo spinoriale** direttamente (già è
   ψ†σψ). Si semplifica: nb e' nativo, non derivato.
3. **Forze di fase** (K·cos(Δφ)) -> la "fase relativa" diventa **overlap spinoriale**
   ⟨ψ_i|ψ_j⟩ (contiene sia fase che direzione). Generalizza cos(Δφ).
4. **Coerenza / interferenza** -> overlap spinoriale invece di cos(Δφ). Naturale.
5. **Mitosi / densita' critica** -> soglia su rho = ψ†ψ. Fisica identica.
6. **Twist / chiralita'** -> il segno di doppia-copertura e' **nativo** nello spinore
   (non piu' derivato da φ). Si semplifica.

### C. Cosa si PRESERVA intatto
- Il **grafo di adiacenza** (nodi, archi, pesi `_mat(w)`, mitosi). INVARIATO.
- Il **kernel** `e^{-r/λ}` - la geometria dell'emissione. Invariato.
- La **schermatura** λ(ρ), la **de-parametrizzazione**, il **limite continuo** - leggi
  su ρ, che resta |campo|². Invariate nella fisica.
- La **posizione**, la **struttura del grafo**. Invariate.
- Le **due forze bifase** (materia/geometria) - riscritte con overlap spinoriale, ma
  fisica preservata.

---

## Perche' il non-abeliano DOVREBBE emergere (l'ipotesi da testare)

- Oggi: Ψ = Σ e^{iφ} -> campo **scalare** -> interferenza `cos(Δφ)` -> **abeliana** (le
  fasi commutano).
- Nuovo: Ψ = Σ ψ_spinore -> campo **spinoriale** -> interferenza `⟨ψ_i|ψ_j⟩` -> **NON
  commuta** (gli spinori vivono in SU(2)) -> **non-abeliana per costruzione**.
- Il segno di doppia-copertura (4π) e' **nativo** nel campo (lo spinore lo porta), non
  aggiunto -> l'olonomia ha un verso perche' la geometria SU(2) (di contatto,
  non-integrabile) lo seleziona.

**Se l'ipotesi di Luca e' giusta**, il segno si ordina perche' il campo *e'* spinoriale,
non perche' un meccanismo lo forza. E la materia (interferenza non distruttiva) si forma
solo dove i segni concordano => la densita' stessa seleziona l'ordine del segno.

---

## Disciplina di implementazione (branch nuovo)

1. **Branch dedicato:** `dev-spinoriale`, separato da dev-dof. Il sistema attuale
   (abeliano) resta intatto e certificabile a parte.
2. **Flag master:** `--campo-spinoriale` (default OFF = sistema attuale byte-identico).
   Con OFF, il nuovo codice non si esegue -> non-regressione garantita.
3. **Un pezzo alla volta:**
   - Fase 1: `calcola_psi` spinoriale (campo a 2 componenti sul grafo) + densita' rho=ψ†ψ.
     Sigillo RIDUZIONE-AL-LIMITE: con spinori tutti in fase (ψ=(e^{iφ/2},0)), Ψ_spin deve
     ridursi al caso scalare Ψ=e^{iφ}. Se si riduce, e' l'inversione; se no, e' un altro
     sistema.
   - Fase 2: gravita' + densita' sul nuovo campo. Sigillo: gravita' ∝ nb·nb invariata.
   - Fase 3: forze di fase -> overlap spinoriale. Sigillo: si riduce a cos(Δφ) nel limite.
   - Fase 4: mitosi/twist/chiralita' sul campo nativo; creazione coppie a segno opposto.
4. **Sigilli per ogni fase:** riduzione-al-limite (il nuovo -> il vecchio quando gli
   spinori sono allineati in fase), conservazione, unitarieta', convergenza-dt.
5. **Test finale (l'ipotesi della visione):**
   - overlap spinoriale ⟨ψ_i|ψ_j⟩ sugli archi del grafo;
   - segno di doppia-copertura, berry firmata;
   - la DENSITA' (materia) segue i segni concordi?
   **Il segno si ordina ORA (campo spinoriale, materia = interferenza non distruttiva)
   dove non si ordinava (campo scalare)?** - il test della visione.

## Linea rossa
- Il cambio nasce dal **principio** (il solitone E' uno spinore che emette, visione dai
  12 anni), NON dal desiderio dello spin-1/2. Legittimo.
- Ogni legge nuova deve **ridursi al vecchio** nel limite (spinori allineati -> campo
  scalare). Se non si riduce, e' un sistema arbitrario, non l'inversione.
- Zero parametri nuovi: il campo spinoriale usa lo stesso kernel/grafo, la stessa λ, lo
  stesso K. Cambia l'OGGETTO (scalare->spinore), non le costanti.

## Geometria di contatto (la cornice - vedi FONDAZIONE_SPINORIALE.md)
- La distribuzione di contatto ξ (dove i solitoni interferiscono) = il GRAFO di adiacenza.
- Il campo di Reeb = l'orologio proprio (Legge IX, tempo proprio).
- La NON-INTEGRABILITA' di ξ (dα|ξ ≠ 0) = il non-abeliano = l'olonomia = lo spin-1/2.
- Test geometrico: misurare l'olonomia su cicli chiusi del grafo. Se non-banale (dipende
  dal cammino), la struttura e' di contatto non-integrabile = non-abeliana.

## Portata onesta
- **Non** byte-identico col vecchio (φ e' la radice, Ψ ne dipende, ~15 leggi da adattare).
- **Sì** grafo di adiacenza e kernel preservati intatti; fisica (gravita', forze, mitosi)
  preservata come leggi; overlap generalizza cos.
- **Progetto di settimane**, non ore. Ma fattibile con disciplina (flag, fasi, sigilli
  di riduzione-al-limite).
- **Esito incerto:** potrebbe dare il non-abeliano (visione giusta) o rivelare nuovi
  problemi. Ma testa il SOLITONE VERO, non l'aggregato attuale.

---

## Nota sulla sfumatura SU(2) dell'interferenza (guardiano)

Nel caso scalare due fasi possono essere solo "in accordo" (costruttiva) o "opposte"
(distruttiva) — binario. Nel caso spinoriale ci sono **stati intermedi** (ortogonali)
dove l'interferenza è parziale (quadratura). La materia spinoriale può formarsi in modi
che quella scalare non permetteva — potenzialmente **fisica nuova**, non solo la vecchia
riscritta.

E il legame con la doppia copertura: due spinori che differiscono di un giro (2π) hanno
lo stesso Bloch ma **segno opposto** → interferiscono **distruttivamente** anche se
"puntano nello stesso posto". Quindi il segno di doppia-copertura ENTRA nell'interferenza:
la materia non distruttiva richiede accordo di direzione E di segno. È il punto dove lo
spin ½ entra nella *formazione* della materia — strutturale, non accessorio.
