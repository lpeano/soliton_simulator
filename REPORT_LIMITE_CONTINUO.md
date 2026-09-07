# Report matematico — limite continuo e problema del core

**Data:** 2026-09-04  
**Oggetto:** valutazione del limite continuo della dinamica discreta e della legge `rho0/rho_c` per la chiralita' del core.

## Sintesi esecutiva

Il codice attuale definisce una dinamica discreta su un grafo geometrico con memoria, crescita topologica, saturazione e tick temporale. Non e' ancora una discretizzazione convergente di una teoria continua nel senso standard `h -> 0`.

Il problema principale per il core e' strutturale:

- `rho0` e' ricavata dal massimo di `|Psi|^2` su nodo + primo intorno topologico;
- `Psi` e' una somma discreta non normalizzata dal volume o dalla misura nodale;
- `rho_c` e' costruita da un conteggio `N_c` diviso per un volume, ma con convenzioni diverse tra schermatura e core;
- `N_c` dipende da `gF_med`, una mediana globale;
- il grafo conserva archi storici oltre la portata corrente;
- il Laplaciano metrico non contiene una normalizzazione esplicita `h^-2`;
- la mitosi cambia la misura discreta senza una legge di conservazione esplicita.

Conclusione: il fatto che `rho0` resti molto sotto `rho_c` puo' essere fisico nel regime attuale, ma non e' ancora interpretabile come densita' continua assoluta. Prima bisogna fissare una normalizzazione coerente del campo e della soglia.

---

## 1. Oggetti implementati

Per nodo:

$$
\mathbf x_i,\qquad z_i=e^{i\phi_i},\qquad v_i=\texttt{phivel}_i,
\qquad \chi_i=\texttt{perc\_chi}_i.
$$

Per arco:

$$
 d_e,\ d_{0,e},\ \dot d_e,\ P_{eq,e},\ tw_e.
$$

Il campo nodale effettivo e':

$$
F_i=\sum_{j\sim i}w_{ij}e^{i\phi_j},
\qquad
\Psi_i=\frac{F_i}{1+\gamma\sqrt{|F_i|^2+\varepsilon}},
\qquad
\rho_i=|\Psi_i|^2.
$$

Il rendering spaziale usa invece un operatore diverso, basato su kernel nelle coordinate e sottrazione del fondo. Quindi il campo usato dalla dinamica e il campo mostrato nel video non sono la stessa osservabile matematica.

---

## 2. Test del limite continuo `h -> 0`

Se `h` e' la spaziatura nodale media in un volume fisso, in tre dimensioni:

$$
N\sim h^{-3}.
$$

Con portata `lambda` fissa, il numero di vicini cresce come:

$$
N_{vic}\sim \lambda^3h^{-3}.
$$

Il campo attuale non contiene un fattore di quadratura `h^3`:

$$
F_i=\sum_jw_{ij}z_j,
$$

mentre una discretizzazione di un integrale dovrebbe assomigliare a:

$$
F(\mathbf x_i)\simeq h^3\sum_jK(\mathbf x_i,\mathbf x_j)z_j.
$$

Per fasi coerenti, quindi, `|F_i|` cresce come `h^-3`; per fasi casuali cresce tipicamente come `h^-3/2`. La saturazione porta allora a:

$$
|\Psi_i|\to\gamma^{-1},
\qquad
\rho_i\to\gamma^{-2}.
$$

Pertanto aumentare la risoluzione non produce automaticamente la stessa teoria a risoluzione piu' fine: senza misura nodale o normalizzazione locale, cambia il regime della saturazione.

### Correzione necessaria prima di parlare di limite continuo

Va scelta una convenzione unica, per esempio:

$$
F_i^{(h)}=\sum_j\mu_j^{(h)}K_{ij}z_j,
\qquad \mu_j^{(h)}\sim h^3,
$$

oppure una normalizzazione locale:

$$
F_i^{(norm)}=\frac{\sum_jw_{ij}z_j}{\sum_jw_{ij}}.
$$

Le due scelte non sono equivalenti fisicamente e devono essere testate A/B. Non va introdotta una normalizzazione solo per far raggiungere la soglia.

---

## 3. `rho0` nel codice

`chiralita_core_locale()` costruisce per ogni nodo:

$$
G_k=\{k\}\cup\{\text{vicini}(k)\},
$$

poi:

$$
\rho_{0,k}=\max_{l\in G_k}|\Psi_l|^2.
$$

Questa non e' una densita' centrale continua. E' un massimo su un primo intorno topologico.

Conseguenze:

1. **Dipendenza dalla storia:** il grafo conserva archi anche quando la distanza supera la portata corrente.
2. **Bias da grado:** un nodo con piu' vicini ha piu' probabilita' di produrre un massimo alto anche a distribuzione invariata.
3. **Non regolarita':** il nodo che realizza il massimo puo' cambiare bruscamente.
4. **Core limitato al primo intorno:** il raggio calcolato puo' crescere senza che il dominio misurato cresca davvero.

Per una definizione continua servirebbe una misura integrale/kernelizzata su una regione, non solo `max` sul primo intorno:

$$
\rho_0(\mathbf x)=\max_{\mathbf y\in B(\mathbf x,R)}\rho(\mathbf y)
$$

con una discretizzazione controllata del volume, oppure una densita' smussata dichiarata come osservabile distinta.

---

## 4. `rho_c`: incoerenza di convenzione

La soglia adattiva e':

$$
N_c=C\lambda^{-3}\gamma^b(1+s)^\theta,
\qquad s=\gamma|F|.
$$

Nella schermatura/diagnostica viene usato un volume costruito con `LAM` corrente:

$$
\rho_c^{(sch)}=\frac{N_c}{(4/3)\pi\,LAM^3}.
$$

Nel calcolo del core viene usato `LAM_BASE`:

$$
\rho_c^{(core)}=\frac{N_c}{(4/3)\pi\,LAM_{base}^3}.
$$

A `B>1`, con `LAM=LAM_base B^(1/3)`, queste soglie differiscono di un fattore `B` a parita' di `N_c`:

$$
\rho_c^{(core)}=B\,\rho_c^{(sch)}.
$$

Questo non e' necessariamente sbagliato, ma rappresenta due densita' diverse. Il rapporto `rho0/rho_c` e' interpretabile solo dopo aver dichiarato se `rho0` e':

- densita' per cella fondamentale;
- densita' per volume efficace;
- intensita' discreta non dimensionale.

**Regola:** numeratore e denominatore del logaritmo devono essere nella stessa convenzione.

---

## 5. Raggio del core

Il codice usa:

$$
R_{core,k}=\lambda_{eff,k}\max\left(\log\frac{\rho_{0,k}}{\rho_c},0\right).
$$

La forma e' motivata formalmente dall'inversione di un profilo esponenziale:

$$
\rho(r)=\rho_0e^{-r/\lambda}.
$$

Ma nel codice non e' dimostrato che:

- il profilo della densita' sia esponenziale;
- `rho0` sia il valore centrale dello stesso profilo;
- `lambda_eff` sia costante nel core;
- la soglia sia della stessa densita'.

La formula e' quindi una legge costitutiva plausibile, **in verifica**, non una conseguenza gia' dimostrata del kernel.

Inoltre la maschera reale e':

$$
core_k=G_k\cap B(\mathbf c_k,R_{core,k}),
$$

non l'intera sfera. Questo produce falsi core piccoli o core saturati al primo intorno.

---

## 6. Non-localita' introdotta dalla soglia

`massa_critica_adattiva()` usa `gF_med`, mediana globale di `gamma|F|`. Quindi:

$$
\rho_c=\rho_c[\text{stato dell'intera rete}].
$$

Se la soglia decide un evento locale, questo introduce un canale non locale. E' accettabile solo se `rho_c` e' dichiarata proprieta' globale del mezzo; altrimenti `s` deve essere calcolato con un intorno locale/kernelizzato.

Le statistiche globali possono restare diagnostiche. Non devono entrare di nascosto nella decisione locale.

---

## 7. Metrica e limite continuo

La metrica evolve una deformazione d'arco `q=d-d0` tramite uno smoothing sul grafo. Un Laplaciano continuo richiede, schematicamente:

$$
\Delta q\sim\frac{q_{i+1}-2q_i+q_{i-1}}{h^2}.
$$

L'operatore attuale e' una media sui vicini senza fattore esplicito `h^-2`. Su un grafo geometrico random, il limite dipende da:

- misura nodale;
- densita' dei punti;
- raggio del kernel;
- normalizzazione del grado;
- scala del Laplaciano.

Senza queste quantita', `--verlet` migliora l'integrazione dell'operatore discreto corrente, ma non dimostra convergenza verso una PDE continua.

---

## 8. Mitosi

La mitosi cambia la topologia, crea nodi e sostituisce archi. La probabilita' per passo non e' esplicitamente proporzionale a `DT`; se si manda `DT->0` mantenendo la stessa probabilita', il tasso di eventi scala come:

$$
rate\sim p/DT.
$$

Per un limite continuo servirebbe una legge di intensita' per unita' di tempo e una conservazione della massa del campo, ad esempio una regola equivalente a:

$$
M_{figlio,1}+M_{figlio,2}=M_{padre}.
$$

Oggi il figlio eredita stato e fase ma il peso di campo non e' una quadratura conservativa dimostrata.

---

## 9. Settore spinoriale e rumore

Con `--spinore-vivo`, il Bloch evolve tramite campo dei vicini e rotazione di Rodrigues. Il rumore viene aggiunto con ampiezza finita per tick, non con scala `sqrt(DT)` tipica di un moto browniano:

$$
\mathbf n_{t+dt}=\mathbf n_t+\mathbf b\,dt+\sigma\,d\mathbf W_t,
\qquad d\mathbf W_t\sim\sqrt{dt}.
$$

Quindi il limite stocastico continuo non e' ancora definito. Anche il termine `1/rho` puo' amplificare fortemente il moto nel vuoto.

---

## 10. Coarse-graining

L'attuale `--scala B` applica:

$$
\lambda_{eff}=\lambda_{base}B^{1/3},
\qquad
\gamma_{eff}=\gamma B^{-1/2},
\qquad
A_{solitone}=B^{1/2}.
$$

E' una famiglia di modelli efficaci, non un coarse-graining ottenuto dalla media di una stessa traiettoria fine. Cambiano rete, grado, cicli, tempi relativi e soglie. Non e' ancora dimostrato che conservi invarianti o olonomie.

A `B=1` i fattori espliciti sono identita', ma la convergenza tra `B>1` e `B=1` resta aperta.

---

## 11. Collegamento con il video ciano

Il rendering distruttivo e il moto posizionale sono parzialmente separati:

$$
\text{fase/interferenza}\to\Psi,tw,d,d_0\to\text{rilassamento delle coordinate},
$$

ma non c'e' ancora una dinamica completa del baricentro:

$$
\text{campo}\to\text{forza traslazionale}\to\ddot{\mathbf x}_{CM}.
$$

Quindi un campo ciano crescente con masse quasi immobili e' compatibile con il codice attuale. E' un comportamento interessante, ma non basta da solo a dimostrare un nuovo disaccoppiamento fisico.

---

## 12. Classificazione delle affermazioni

### Dimostrato dal codice

- `rho_i=|Psi_i|^2` e' una somma discreta saturata.
- `rho0` e' un massimo su nodo + primo intorno topologico.
- `rho_c_core` usa `LAM_BASE^3`.
- la schermatura usa `LAM^3`.
- `N_c` usa una mediana globale `gF_med`.
- il grafo mantiene archi storici.
- il Laplaciano metrico non ha normalizzazione esplicita `h^-2`.
- la mitosi non e' scalata esplicitamente con `DT`.
- il default ha spinore congelato; `--spinore-vivo` riattiva la dinamica.
- rendering e campo nodale sono osservabili diverse.

### In verifica

- il raggio logaritmico rappresenta il core fisico;
- la maschera locale separa core e guscio;
- la soglia con `LAM_BASE` e' la convenzione corretta a `B>1`;
- la chiralita' core-aware e' stabile rispetto a seed e grado;
- `CHI_CORE` migliora un verso della massa;
- il coarse-graining conserva gli invarianti;
- l'ordine spinoriale e la Berry sopravvivono ai tempi lunghi.

### Aperto

- limite continuo ben posto;
- misura nodale/volume fisica;
- conservazione della massa durante la mitosi;
- limite stocastico del settore spinoriale;
- derivazione dei coefficienti critici e dei pavimenti;
- canale di moto traslazionale del baricentro.

---

## 13. Piano di verifica consigliato

1. **Test di normalizzazione:** confrontare campo non normalizzato, campo normalizzato per grado e campo con misura nodale; mantenere separata la dinamica.
2. **Test di soglia:** registrare contemporaneamente `rho0`, `rho_c_core`, `rho_c_sch`, `gF_med`, grado e numero di vicini.
3. **Test del core:** sostituire il primo intorno con una regione kernelizzata e confrontare stabilita' di `R_core` e `chi_core`.
4. **Test locale/globale:** sostituire `gF_med` con `gF_locale` solo in un ramo sperimentale e misurare l'impatto.
5. **Test di raffinamento:** ripetere a risoluzioni/scale equivalenti con volume e densita' fisica controllati.
6. **Test di dinamica:** misurare baricentri, `d`, `d0`, `tw`, energia e massa ciano nello stesso run.
7. **Solo dopo:** usare `chi_core` come feedback fisico definitivo.

La regola di governance resta: una modifica alla volta, default invariato, almeno 2000 passi e 2–3 semi prima di promuovere una legge.

---

## 14. ADDENDUM 2026-09-07 — il criterio giusto è il COARSE-GRAINING (RG), non `h→0`

**Verificato che il report resta consistente col codice al 2026-09-07** (campo `satura`, `rho0=max`, `R_core=λ·log(rho0/rho_c)`, `gF_med` globale, Laplaciano senza `h⁻²`, archi storici, convenzione `LAM` vs `LAM_BASE`: tutti invariati). Unica aggiunta non riflessa: **`--cs-dinamico`** (2026-09-05) rende `cs²` un CAMPO LOCALE → la §7 diventa una PDE a **coefficiente variabile** `cs²(x)·Δq` (estende, non contraddice).

### 14.1 Correzione di criterio (obiezione di Luca, ACCOLTA)
I solitoni hanno lunghezza d'onda **2ℓ_P** (LAM): è la **granularità FONDAMENTALE** di Planck, non un artefatto di reticolo. Quindi **`h→0` è il test SBAGLIATO** (sotto Planck non c'è geometria). Il continuo del sistema emerge per **COARSE-GRAINING a grande scala** (molti solitoni aggregati), come in idrodinamica/termodinamica e in gravità emergente (causal sets, LQG). Il criterio giusto è: **le osservabili macroscopiche sono INVARIANTI sotto coarse-graining** (gruppo di rinormalizzazione), cioè descrivere lo stesso sistema con blocchi di `B` o `2B` solitoni dà le stesse grandezze macroscopiche.

### 14.2 L'onere si SPOSTA, non si elimina (guardiano)
Cambiare criterio non cancella la prova: **va dimostrata l'invarianza sotto coarse-graining (RG)**. E alcuni problemi del report **sopravvivono anche col criterio giusto**, perché rompono proprio l'invarianza di coarse-graining:
- **Ψ non normalizzata per il grado** (`deg`): raggruppare solitoni cambierebbe Ψ in modo scala-dipendente → rompe l'invarianza RG. [APERTO]
- **Mediana globale `gF_med`** in `N_c`: canale non-locale → nessun analogo continuo locale → rompe l'invarianza di scala locale. [APERTO]
- **Conservazione della misura alla mitosi**: se la mitosi non conserva una misura, il coarse-graining non è consistente. [APERTO — il più duro, non chiudibile analiticamente]

### 14.3 Classificazione ANALITICA di scaling a N→∞ (dallo scaling, senza girare)
Criterio: **intensiva/adimensionale (rapporto, media normalizzata) → converge; estensiva (somma su N) → diverge; con media/mediana globale → non-locale.**

- **CLASSE 1 — CONVERGONO** (limite continuo ben definito): `spin_axis_R`, `m0_spin_axis_R`, `m0_omega_axis_R` (medie di versori ∈[0,1]); `u=ρ/ρ_c`; `λ` schermatura `=f(ρ/ρ_c)`; `tw/Φ_crit`; frazioni/coerenze per dominio. Il diaglog covariante è **analiticamente corretto**.
- **CLASSE 2 — DIVERGONO per ESTENSIVITÀ** (→ NORMALIZZARE per N/I/V, non de-parametrizzare): `m0_Lz`/`Lz_orb` (÷ I), `N`/`N_nucleo`/massa (÷ V), energia totale (÷ N).
- **CLASSE 3 — NON convergono per PARAMETRO** (scala assoluta → DE-PARAMETRIZZARE con rapporti di stato): **GAMMA=0.05** (Ψ, cs_floor, dens_crit — il più centrale, in 3 osservabili), DENS_CRIT_C, ELAST_C, K_C, KICK_TW, MU_PSI, TAU_BG/TAU_P/TAU_DIFF.
- **CLASSE 4 — NON-LOCALI** (→ LOCALIZZARE con media di vicinato `wI`): `N_c` via `gF_med`, eventuali `pozzo.mean()` residui.
- **UNITÀ (non parametri, non toccare):** LAM=2ℓ_P, DT, Φ_crit=2π.

### 14.4 La connessione (INTUIZIONE di Luca, criterio non ancora dimostrato)
**"Non parametri, ma leggi" ≡ criterio del limite continuo**, per le Classi 3-4: de-parametrizzare = sostituire una scala assoluta con un rapporto di stato = rendere adimensionale/invariante di scala = far convergere a N→∞. Un parametro fisso è una scala assoluta che rompe l'invarianza di scala. NON copre le Classi 1-2 (la 1 converge per natura; la 2 diverge per estensività → si normalizza). **Etichetta: CRITERIO/mappa, non risultato — è analitico sullo scaling.**

### 14.5 Limite onesto dell'analitica
L'analitica dà lo **SCALING** (converge sì/no, come va con N), **non il VALORE del limite né la velocità di convergenza** (non-linearità: saturazione, mitosi, accoppiamenti → numerici). E soprattutto **non chiude l'indipendenza dal MODO di crescere N** (la mitosi conserva la misura?) → serve il numerico o un'analisi profonda della mitosi. La mappa è chiara; il territorio va percorso.

### 14.6 TODO (pian piano — vedi Checkpoint)
1. De-parametrizzare **GAMMA** per primo (Classe 3, centrale in 3 osservabili) con un rapporto di stato — un flag reversibile, byte-identico off, A/B.
2. Localizzare **`gF_med`** (Classe 4) con media di vicinato `wI` (come già fatto per il sync) — ramo sperimentale.
3. Normalizzare le estensive (Classe 2): `Lz/I`, `N/V` — nel diaglog (covariante), non nella dinamica.
4. Test di **invarianza sotto coarse-graining** (RG): stesso sistema a `B` vs `2B`, osservabili macroscopiche coincidono?
5. Aggiungere la normalizzazione di Ψ per il grado come ramo A/B (romperebbe la byte-identità: solo esplorativo).
6. Il punto duro: misura conservata dalla mitosi (analitico + numerico).
