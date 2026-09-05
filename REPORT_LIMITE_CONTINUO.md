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
