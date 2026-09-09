# Ontologia del sistema dei solitoni relazionali spinoriali

*Branch: `dev-spinoriale`. Documento di ontologia — definisce le ENTITÀ del sistema
(cosa esiste), le loro CATEGORIE (fondamentale / emergente / relazionale) e le RELAZIONI
fra loro. Complementare a `doc/FONDAZIONE_SPINORIALE.md` (fisica e leggi) e
`doc/REFACTORING_SPINORIALE.md` (piano tecnico).*

---

## 1. Il principio ontologico

La domanda ontologica è: **cosa esiste veramente, e cosa è conseguenza?**

Nel sistema spinoriale la risposta è netta e ribalta il sistema precedente:

- **Esiste fondamentalmente:** lo **spinore** (la sfera-otto, SU(2)) e le **relazioni**
  fra solitoni (il grafo di adiacenza).
- **Emerge (è conseguenza):** il campo, la materia, la direzione, il segno, le forze, la
  gravità, il tempo, la geometria, lo spin ½.

Nulla di fisico vive nei solitoni singoli come "cosa": il solitone è un **puntatore
spinoriale** che emette. La fisica vive nell'**interferenza** del campo emesso, sul
grafo. È il principio "guarda la luna, non il dito" portato sull'oggetto giusto: il dito
è la posizione del solitone; la luna è il campo spinoriale che genera.

---

## 2. Le entità fondamentali (ciò che è dato)

| Entità | Simbolo | Natura | Descrizione |
|---|---|---|---|
| **Solitone** | i | puntatore | un nodo del grafo; non ha sostanza propria, è un emettitore |
| **Spinore** | ψ_i | SU(2), \|ψ\|=1 | lo stato interno fondamentale (la sfera-otto). Due componenti complesse (a, b) |
| **Posizione** | p_i | relazionale | dove il solitone sta nel grafo (non in uno spazio di sfondo) |
| **Grafo di adiacenza** | (nodi, archi) | relazionale | il substrato: nodi = solitoni, archi = vicinanze pesate |
| **Peso d'arco** | w_ij = e^(−r_ij/λ) | relazione | forza della relazione fra i e j (il kernel di emissione) |

**Categoria:** questi sono i mattoni. Lo spinore è l'unico "contenuto"; tutto il resto è
relazione (grafo) o parametro di stato (posizione). Le costanti (λ, γ, K, 4π) sono
riferimenti di stato, non entità.

---

## 3. Le entità emergenti (ciò che è conseguenza)

| Entità | Definizione | Da cosa emerge | Legge |
|---|---|---|---|
| **Campo** | Ψ_i = Σ_j w_ij ψ_j | interferenza degli spinori sugli archi | I |
| **Densità / Materia** | ρ_i = Ψ_i† Ψ_i | interferenza NON distruttiva del campo | II |
| **Direzione di Bloch** | n_i = ψ_i† σ ψ_i | proiezione dello spinore sulla sfera | (nativa) |
| **Segno di doppia-copertura** | ± (foglio dell'otto) | fase SU(2) accumulata (olonomia) | VIII |
| **Overlap** | ⟨ψ_i\|ψ_j⟩ | relazione fra spinori adiacenti | IV |
| **Forza (materia)** | F = K·Re⟨ψ_i\|ψ_j⟩·(w/λ) | overlap + peso d'arco | V |
| **Gravità (geometria)** | g ∝ ⟨n_i·n_j⟩ | allineamento di Bloch + pozzo | VII |
| **Tempo proprio** | τ_i = 1 + \|torsione\|/(4π) | torsione locale (massa) | IX |
| **Olonomia / spin ½** | segno su ciclo chiuso del grafo | non-integrabilità di contatto | (geom.) |

**Categoria:** tutte queste sono **derivate** dallo spinore e dal grafo. Nessuna è un
mattone; ciascuna è una lettura o una conseguenza. In particolare la **materia (ρ)** non
è una sostanza ma un **pattern d'interferenza**; lo **spin ½** non è un'etichetta ma
l'**olonomia** della geometria di contatto.

---

## 4. Le relazioni ontologiche (come le entità si generano)

```
                 EMISSIONE                    INTERFERENZA (archi)
  Spinore ψ_i  ───────────▶  campo emesso  ──────────────────────▶  Campo Ψ_i
     │                          (w_ij ψ_j)                              │
     │ proiezione (ψ†σψ)                                                │ norma (Ψ†Ψ)
     ▼                                                                  ▼
  Direzione n_i                                                     Densità ρ_i
     │                                                              (= MATERIA:
     │ allineamento ⟨n_i·n_j⟩                                        interferenza
     ▼                                                               non distruttiva)
  GRAVITÀ (geometria)                                                   │
                                                                        │ soglia
                                                                        ▼
                                                                   MITOSI / coppie
```

- **Emissione** (spinore → campo): il solitone emette il suo spinore, attenuato dal peso
  d'arco. È la relazione generativa primaria (Legge I).
- **Interferenza** (sugli archi): i campi si sommano; dove concordano (direzione E segno)
  → materia; dove si oppongono → vuoto (Legge II). È la relazione che crea la sostanza.
- **Proiezione** (spinore → Bloch): la direzione n è una lettura dello spinore, non un
  grado di libertà indipendente.
- **Overlap** (spinore ↔ spinore): la relazione fra vicini che genera le forze (Legge IV/V).

---

## 5. Le tre categorie ontologiche

1. **Fondamentale (sostanza):** solo lo **spinore SU(2)**. È l'unico oggetto con contenuto
   proprio. La sua natura non-abeliana (doppia copertura, 4π) è data, non attivata.

2. **Relazionale (struttura):** il **grafo di adiacenza** e i **pesi d'arco**. Non è una
   sostanza ma la rete di relazioni. Realizza la **distribuzione di contatto ξ**: lo
   "spazio" dove i solitoni interferiscono.

3. **Emergente (fenomeno):** tutto il resto — campo, materia, direzione, segno, forze,
   gravità, tempo, geometria, spin ½. Sono **pattern** dell'interferenza spinoriale sul
   grafo, non cose in sé.

---

## 6. L'ontologia della geometria di contatto

La geometria di contatto dà la cornice ontologica del "quando" e del "dove":

- **Campo di Reeb R** = il **tempo** (l'orologio di de Broglie): la direzione lungo cui lo
  spinore avanza la sua fase a ritmo costante. È il "quando".
- **Distribuzione ξ = grafo di adiacenza** = lo **spazio** (dove i solitoni interferiscono):
  il piano trasverso al tempo. È il "dove".
- **Forma di contatto α** = il legame fra i due (il ritmo dell'otto legato al moto sulla
  sfera): α = dφ_otto − p·dq.
- **Non-integrabilità (dα\|ξ ≠ 0)** = il **non-abeliano** = l'olonomia = lo **spin ½**.

Ontologicamente: lo spin ½ **non è una proprietà aggiunta** a un oggetto, ma la
**non-integrabilità** della struttura di contatto — una proprietà geometrica della
relazione fra tempo (Reeb) e spazio (grafo). Esiste perché la geometria non si chiude in
un giro: l'otto.

---

## 7. Il contrasto con l'ontologia precedente (sistema scalare)

| | Sistema scalare (precedente) | Sistema spinoriale (nuovo) |
|---|---|---|
| **Fondamentale** | fase φ (U(1), scalare) | spinore ψ (SU(2)) |
| **Campo** | Ψ = Σ e^{iφ} (scalare) | Ψ = Σ ψ (spinoriale, n×2) |
| **Spinore** | derivato / parallelo | **fondamentale** |
| **Segno di doppia-copertura** | derivato da φ, meccanismo | **nativo** nello spinore |
| **Non-abeliano** | attivato da un meccanismo | **incorporato** per costruzione |
| **Materia** | \|Ψ\|², accordo di fase | ρ = Ψ†Ψ, accordo di direzione E segno |
| **Spin ½** | etichetta su gradi aggiunti | olonomia nativa della contatto-geometria |

**La differenza ontologica cruciale:** nel vecchio sistema l'abeliano era la *natura* del
fondamentale (U(1)); nel nuovo, il non-abeliano è la *natura* del fondamentale (SU(2)). Le
vie fallite (documentate su `dev-dof`) testavano meccanismi non-abeliani sopra un
fondamentale abeliano — un innesto. Qui il fondamentale stesso è non-abeliano — non c'è
innesto, c'è l'oggetto vero.

---

## 8. L'ipotesi ontologica da verificare

**Se lo spinore è l'oggetto fondamentale** (non la fase), allora il segno di
doppia-copertura si ordina **perché è la natura della materia** (interferenza non
distruttiva = accordo di direzione E segno), non perché un meccanismo lo forza. La
materia stessa (ρ) **seleziona** i segni concordi: dove i segni discordano, il campo si
cancella (niente materia). Lo spin ½ diventa **costitutivo dell'esistere della materia**.

Questo è il test della visione, sul branch `dev-spinoriale`: la densità (materia) segue i
segni concordi? Se sì, l'ontologia è giusta — lo spin ½ è nativo, non aggiunto.
