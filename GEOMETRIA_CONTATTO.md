# Geometria di contatto del modello

Questo documento descrive in modo pedissequo la geometria di contatto
**attualmente implementata** in `soliton_simulator.py`. Per "contatto" si
intende qui la relazione topologica rappresentata da un arco del grafo
`(i, j)`. Non si deve confondere l'arco con una particella, una corda fisica o
una forza autonoma: è il supporto discreto sul quale il codice fa evolvere
peso d'interferenza, fase, torsione e variabili metriche.

La geometria di contatto è quindi composta da due livelli distinti:

1. **topologia di contatto**: quali coppie di nodi sono collegate (`i`, `j`);
2. **geometria metrica dell'arco**: distanza reale `d`, distanza di riposo `d0`
  e velocità metrica `vd`;
3. **mezzo metrico locale**: velocità d'onda `cs_eff` sugli archi, attiva solo
  con `--cs-dinamico`.

La topologia nasce dalle coordinate, mentre la metrica degli archi evolve nel
tempo. Le coordinate sono il supporto computazionale e visuale della geometria
relazionale; non sono, da sole, la materia del modello.

## 1. Nodi e spazio di supporto

Ogni nodo ha una posizione tridimensionale

$$\mathbf x_i\in\mathbb R^3,$$

conservata in `net.pos`. Le posizioni vengono utilizzate per:

- costruire i contatti tramite un `cKDTree`;
- inizializzare le distanze degli archi;
- rilassare il disegno verso la metrica dinamica;
- costruire l'embedding e il rendering.

Il campo d'interferenza, le fasi e le relazioni sugli archi sono le osservabili
fisiche privilegiate del progetto. La posizione è quindi una rappresentazione
geometrica necessaria al calcolo attuale, non un'identificazione automatica tra
"nodo" e "corpo materiale".

## 2. Grafo di contatto

Il grafo è non orientato nella costruzione fisica, anche se il codice conserva
ogni arco mediante due array orientati:

$$E=\{(i_e,j_e)\}_{e=1}^{N_E},$$

rappresentati da `net.i` e `net.j`. Per ogni arco esistono array paralleli:

| Variabile | Significato |
|---|---|
| `i[e]`, `j[e]` | estremi dell'arco |
| `d[e]` | distanza metrica corrente |
| `d0[e]` | distanza di riposo/plastica |
| `vd[e]` | velocità di variazione di `d` |
| `cs_eff[e]` | velocità locale dell'onda metrica, diagnostica |
| `peq[e]` | fondo/equilibrio locale |
| `tw[e]` | torsione accumulata |
| `twp[e]` | torsione di riferimento del passo precedente |

La matrice sparsa `net._S` è simmetrica: per il calcolo del campo ogni arco
contribuisce in entrambe le direzioni, anche se viene memorizzato una sola volta
negli array `i` e `j`.

## 3. Criterio esatto di creazione dei contatti

La routine responsabile è `Rete._allaccia(base)`. Quando vengono aggiunti nodi,
`base` è l'indice del primo nodo nuovo. Il codice costruisce:

- un `cKDTree` su tutte le posizioni `self.pos`;
- un secondo `cKDTree` sulle posizioni dei soli nodi nuovi;
- tutte le coppie nuovo–totale entro un raggio `rc` tramite
  `sparse_distance_matrix`.

Per una coppia candidata il contatto geometrico iniziale è quindi

$$\|\mathbf x_a-\mathbf x_b\|\le r_c.$$

La distanza registrata è

$$d_{ab}=\max\left(\|\mathbf x_a-\mathbf x_b\|,10^{-6}\right),
\qquad d_{0,ab}=d_{ab}.$$

Il termine $10^{-6}$ è una protezione numerica per evitare una distanza nulla;
non è una scala fisica del modello.

### 3.1 Raggio di contatto

Il raggio di connessione dipende dal momento della semina:

- se il grafo non ha ancora archi, `rc = R_CONN() = 3 LAM`;
- se esistono già archi, `rc = 3 median(lambda_nodi())`.

In formula, nel secondo caso:

$$r_c=3\,\mathrm{med}_k(\lambda_k),$$

con `lambda_nodi()` calcolata dallo stato disponibile al momento
 dell'allacciamento.

Questo significa che la schermatura può ridurre il raggio usato per la
creazione di nuovi contatti quando il campo locale è denso. Il raggio non è
però un criterio di aggiornamento continuo della topologia: una volta creato,
un contatto non viene automaticamente cancellato quando le posizioni o le
portate cambiano.

### 3.2 Eliminazione dei duplicati e orientamento di memoria

Dalla matrice delle distanze il codice conserva solo le coppie che soddisfano

$$b<\mathrm{base}\quad\lor\quad a<b,$$

con `a` nodo nuovo e `b` nodo già presente oppure altro nodo nuovo. In questo
modo:

- ogni coppia viene memorizzata una sola volta;
- non vengono create due volte le coppie vecchio–nuovo;
- non viene mantenuto il doppio arco $(i,j)$ e $(j,i)$ negli array principali;
- la matrice di calcolo viene poi resa simmetrica da `_costruisci_struttura()`.

Se `COMPAT_CHI=True`, dopo il filtro geometrico vengono mantenuti soltanto gli
archi con chiralità opposta:

$$\chi_a\ne\chi_b.$$

Con la configurazione corrente `COMPAT_CHI=False`, quindi la chiralità non
impedisce la creazione del contatto. Può comunque entrare nelle dinamiche di
torsione e del settore spinoriale.

## 4. La portata locale e il contatto

La portata locale del nodo è `lambda_nodi()`. Quando la schermatura è attiva,
il codice usa la densità di interferenza

$$\rho_i=|\Psi_i|^2,$$

la densità critica adattiva $N_c$ e la densità critica locale di riferimento

$$\rho_c=\frac{N_c}{(4/3)\pi LAM^3}.$$

Con $u_i=\rho_i/\rho_c$:

$$f(u_i)=\frac{1}{1+\log(1+e^{u_i-1})},$$

$$\lambda_i=\max\left(LAM\,f(u_i),0.15\,LAM\right).$$

Per un arco già esistente la portata è simmetrizzata:

$$\lambda_{ij}=\frac{\lambda_i+\lambda_j}{2}.$$

Questa quantità entra nel peso del campo,

$$w_{ij}\supset e^{-d_{ij}/\lambda_{ij}},$$

e, durante una nuova semina, la mediana delle `lambda_i` determina il raggio
globale di ricerca dei contatti nuovi.

### Punto importante: due usi diversi della portata

Nel modello attuale `lambda_nodi()` ha due effetti distinti:

1. modifica la portata del kernel d'interferenza sugli archi già esistenti;
2. modifica il raggio di ricerca quando vengono aggiunti nuovi nodi.

Non esiste una procedura generale che scandisca a ogni passo tutti i nodi e
ricostruisca $E$ in base alla nuova distanza o alla nuova portata. Pertanto la
schermatura è dinamica per i pesi e per i futuri allacciamenti, ma la topologia
è storica e discreta.

La portata `lambda_ij` e la velocità dell'onda metrica `cs_eff_ij` sono
grandezze distinte: la prima controlla il kernel d'interferenza e la ricerca
di contatti futuri; la seconda controlla la rigidità e la stabilità della
propagazione metrica.

## 5. Inizializzazione della metrica dell'arco

Quando un contatto nasce, il codice imposta:

$$d_{ij}^{(0)}=\|\mathbf x_i-\mathbf x_j\|,$$

$$d_{0,ij}^{(0)}=d_{ij}^{(0)},
\qquad vd_{ij}^{(0)}=0.$$

Ne consegue che un arco appena creato parte senza deformazione:

$$q_{ij}^{(0)}=d_{ij}^{(0)}-d_{0,ij}^{(0)}=0.$$

Anche `peq` e `tw` vengono inizializzati senza un valore dinamico già
accumulato; `peq` parte da `NaN` e viene calibrato al primo aggiornamento,
mentre `tw` e `twp` partono da zero.

## 6. Evoluzione metrica del contatto

La lunghezza reale dell'arco non è più necessariamente la distanza euclidea
tra le coordinate dopo l'inizializzazione. Il codice evolve la deformazione

$$q_{ij}=d_{ij}-d_{0,ij}$$

con un'equazione discreta di tipo onda sul grafo:

$$\ddot q_{ij}=c_s^2\Delta_Gq_{ij}+a_{ij}-\beta_{ij}\dot q_{ij}.$$

Nel ramo canonico (`CS_DINAMICO=False`) $c_s=CS_M=2$. Con `--cs-dinamico`,
la velocità dipende localmente dalla densità del campo. Ponendo

$$u_i=\frac{|\Psi_i|^2}{\max(\operatorname{mediana}(|\Psi|^2),10^{-9})},$$

il codice usa il riferimento locale dei vicini

$$\bar I_i=\frac{(W I)_i}{(W\mathbf 1)_i},
\qquad u_i=\frac{I_i}{\max(\bar I_i,10^{-9})},$$

e il profilo liscio con un floor che emerge dalla saturazione locale:

$$c_{floor,i}=\frac{CS_M}{1+\gamma\sqrt{I_i}},
\qquad
c_{s,i}=c_{floor,i}+(CS_M-c_{floor,i})\frac{1+\tanh(1-u_i)}2.$$

L'arco usa la media armonica, non quella aritmetica:

$$c_{s,ij}=\frac{2c_{s,i}c_{s,j}}{c_{s,i}+c_{s,j}}.$$

La rigidità locale diventa quindi $c_{s,ij}^2\Delta_Gq_{ij}$ e lo smorzamento
locale usa $\beta_{ij}=2\zeta_Mc_{s,ij}/d_{ij}$. Il CFL usa il massimo
attuale $\max_{ij}c_{s,ij}$ per i sottopassi. Il flag è default-off: a
`CS_DINAMICO=False` il percorso storico resta invariato.

Qui:

- $\Delta_G$ è il Laplaciano discreto sugli archi adiacenti;
- $a_{ij}$ è la sorgente di densità o la sorgente hamiltoniana;
- $\beta_{ij}$ è lo smorzamento;
- `vd` rappresenta $\dot d_{ij}$.

La sorgente fenomenologica usa

$$\rho_{ij}=\frac{\rho_i+\rho_j}{2},
\qquad a_{ij}=\alpha_M\frac{\rho_{ij}-P_{eq,ij}}{P_{eq,ij}},$$

salvo il ramo hamiltoniano opzionale. Con lo smorzamento locale di scala:

$$\beta_{ij}=\frac{2\zeta_Mc_{s,ij}}{d_{ij}}$$
nel ramo dinamico, mentre nel ramo storico $c_{s,ij}=CS_M$.

Il codice integra questa dinamica con sottopassi quando sorgente, smorzamento o
velocità lo richiedono. La distanza reale è protetta inferiormente da `0.05`:

$$d_{ij}\leftarrow\max(d_{ij},0.05).$$

Questo è un pavimento numerico/di stabilità per la metrica reale, distinto dal
limite `0.15 LAM` della portata d'interferenza.

## 7. Evoluzione della distanza di riposo

`d0` è una variabile di stato plastica. In modalità locale il tempo di risposta
usa la scala dell'arco e un fattore di elasticità derivato dalla densità:

$$\tau_{p,ij}=\frac{d_{ij}}{c_s}\left[1+100\max\left(\frac{\rho_{ij}}{\rho_{med}}-1,0\right)\right].$$

L'aggiornamento è

$$d_{0,ij}\leftarrow d_{0,ij}+dt_{ij}
\frac{d_{ij}-d_{0,ij}}{\tau_{p,ij}}.$$

Se le costanti temporali locali sono disattivate, viene usata la forma globale

$$d_{0,ij}\leftarrow d_{0,ij}+dt_{ij}
\frac{d_{ij}-d_{0,ij}}{\tau_P}.$$

Dopo l'aggiornamento, `d0` è limitata dal pavimento definito da `_floor_d0()`.
Con `PAV_COM=False` il pavimento è `0.05`; con `PAV_COM=True` è comovente e
proporzionale alla mediana corrente di `d0`.

## 8. Rilassamento delle coordinate

La routine `rilassa_disegno()` non cambia `d` o `d0`: cambia le coordinate
`pos` per farle inseguire la metrica corrente. Per l'arco $e=(i,j)$ definisce

$$\mathbf v_e=\mathbf x_j-\mathbf x_i,
\qquad L_e=\|\mathbf v_e\|,$$

$$\mathbf c_e=\frac{L_e-d_e}{L_e}\,\mathbf v_e\,\frac12.$$

Per ogni nodo il codice accumula i contributi degli archi incidenti, divide per
il grado del nodo e applica il passo limitato

$$\Delta\mathbf x_i=\eta\,
\mathrm{clip}\left(\frac{1}{deg_i}\sum_{e\ni i}\mathbf c_e,-0.5,0.5\right).$$

Dopo ogni chiamata il baricentro cartesiano viene riportato all'origine:

$$\mathbf x_i\leftarrow\mathbf x_i-\frac1N\sum_k\mathbf x_k.$$

Il rilassamento è quindi un embedding della metrica, non un'equazione del moto
dei solitoni. L'opzione `L_CONSERVA`, disattiva per default, tenta inoltre di
rimuovere la rotazione rigida spuriosa introdotta dal rilassamento.

## 9. Modifiche topologiche successive

### 9.1 Mitosi di un arco

Quando la torsione dell'arco supera la soglia probabilistica, `mitosi()` può
sostituire un arco $(a,b)$ con due archi $(a,m)$ e $(m,b)$. Il nuovo nodo ha
posizione

$$\mathbf x_m=\frac{\mathbf x_a+\mathbf x_b}{2}.$$

La distanza reale dei due nuovi archi è inizialmente metà di quella vecchia:

$$d_{am}=d_{mb}=\frac{d_{ab}}2.$$

Di default anche la distanza di riposo è dimezzata:

$$d_{0,am}=d_{0,mb}=\frac{d_{ab}}2.$$

Con `PLAST_MIT>0` viene applicato un offset plastico derivato dalla torsione
sciolta:

$$d_{0,am}=d_{0,mb}=\frac{d_{ab}}2
\left(1+PLAST\_MIT\frac{|tw_{ab}|}{\Phi_{crit}}\right).$$

L'arco padre viene rimosso dall'elenco, quindi la mitosi non aggiunge
semplicemente due archi lasciando il padre: lo sostituisce. I nuovi archi
partono con torsione nulla e con la memoria `twp` coerente con le nuove
 differenze di fase.

La posizione del figlio è un punto medio cartesiano, mentre la sua fase è il
punto medio avvolto della differenza di fase; con `MITOSI_DIR` la fase può essere
spostata verso l'estremo con torsione maggiore. Sono quindi due medie diverse:
una geometrica per `pos`, una relazionale di fase per `phi`.

### 9.2 Creazione di coppia

Nel ramo opzionale di creazione di coppia, un anti-nodo nasce sul punto medio
fra i genitori e viene collegato a entrambi. Le due nuove lunghezze sono
inizializzate a

$$d=d_0=\frac12\|\mathbf x_a-\mathbf x_b\|.$$

L'anti-nodo ha fase opposta di $\pi$ nella copertura usata dal codice e
chiralità opposta a quella del genitore selezionato. Anche questi contatti sono
aggiunti topologicamente e non derivano da una ricerca globale immediata dei
vicini.

## 10. Ordine temporale di un passo

Nel ciclo operativo di batch e video l'ordine generale è:

1. eventuale scuotimento locale del vuoto;
2. aggiornamento di fase, torsione, fondo e metrica (`step()`);
3. mitosi e possibili coppie (`mitosi()`), quindi modifiche topologiche;
4. rilassamento delle coordinate (`rilassa_disegno()`);
5. memoria hebbiana del moto (`memoria_hebbiana_moto()`).

Questo ordine è rilevante: la metrica viene aggiornata prima della mitosi, la
mitosi può cambiare il grafo prima del rilassamento, e il rilassamento usa le
nuove relazioni metriche.

## 11. Cosa significa "contatto" nel modello

Un contatto è dunque contemporaneamente:

- un'appartenenza topologica a $E$;
- una coppia di estremi che contribuisce al campo $\Psi$;
- un supporto per peso, memoria di fase, torsione e fondo;
- un elemento della rete su cui si propaga la deformazione metrica;
- un vincolo usato per l'embedding visuale.

Non significa invece necessariamente:

- che le coordinate siano una particella materiale;
- che la distanza corrente sia sempre quella euclidea;
- che un arco venga cancellato quando supera la portata;
- che ogni nodo entro la portata sia materia coerente;
- che la topologia sia una triangolazione Delaunay o una tassellazione completa.

Il modello corrente è quindi una **rete geometrica dinamica con topologia a
memoria**: i contatti nascono da prossimità coordinate, mentre la metrica e il
campo evolvono sugli archi già presenti.

## 12. Osservabili per verificare la geometria di contatto

Per i test usare soprattutto grandezze relazionali e confrontare più semi:

- `n_archi`: numero totale di contatti;
- `entro`: frazione degli archi con $d\le R\_CONN()`;
- `d_min`, `d_mean`, `d_max`: distribuzione della metrica reale;
- `d0_min`, `d0_mean`, `d0_max`: distribuzione della metrica di riposo;
- `dmin_nodi`: minima distanza euclidea fra posizioni nel `diaglog`;
- `lambda_eff_min/med/max`: portata schermata;
- `cs_eff_min/med/max`: velocità locale dell'onda metrica, presenti solo con
  `--cs-dinamico`;
- `ncrit_adattivo`, `rho_critica`: ancoraggio della schermatura;
- `stress` e `dil`: deformazione e dilatazione metriche;
- `tw_q` e `tw_disp`: torsione in unità di olonomia;
- `Lz_orb_ij` e `dist_ij`: relazioni tra strutture di massa.

La diagnostica passiva `circolazione_topologica()` costruisce cicli fondamentali
dalla sola lista degli archi. La corrente è pesata da densità locale, twist e
allineamento spinoriale:

$$J_{ij}=w_{ij}\,\frac{\rho_i+\rho_j}{2}\,
(\mathbf n_i\cdot\mathbf n_j)\,\frac{tw_{ij}}{\Phi_{crit}}.$$

Le colonne sono `n_cicli_topologici`, `circolazione_topologica_max`,
`circolazione_topologica_media_assoluta` e `circolazione_topologica_media`, più
le componenti non-gradientali gauge-invarianti `olonomia_fase_*` (olonomia di
fase sui cicli) e `berry_spin_*` (fase di Berry come invariante di Bargmann).
Non dipendono da `pos` o dal rendering e non costituiscono ancora una nuova
forza dinamica. Sul sistema reale $\Gamma\simeq0$ (twist curl-free); `berry_spin_*`
è $\equiv0$ con spinore congelato (default) e diventa non-nullo solo con
`--spinore-vivo`, il flag che reinnesta l'evoluzione SU(2) (sotto test A/B).

La condizione `entro` non dimostra che il grafo sia correttamente connesso in
senso fisico: misura solo il rapporto tra la metrica corrente e il raggio
`R_CONN()`. Poiché gli archi hanno memoria, è possibile avere archi oltre la
portata corrente senza che il codice li elimini.

### Core locale e chiralità collettiva

Il flag sperimentale `--chi-core` distingue `perc_chi`, chiralità del singolo
puntatore, dalla chiralità emergente del dominio denso. Il core usa il massimo
locale di $|\Psi|^2$, la soglia critica riferita alla cella nativa e la portata
schermata locale:

$$R_{core}=\lambda_{eff}\max\left(\log(\rho_0/\rho_c),0\right).$$

La chiralità è poi la proiezione pesata da $|\Psi|^2$ di tutti i nodi nella
maschera, senza filtro preventivo su $+1$ o $-1$. Con il flag attivo guida i
canali collettivi spinoriali, il twist dipolare e il frame-dragging; i processi
di nascita ed eredità mantengono la chiralità microscopica. Stabilità del segno
e separazione fisica core/guscio restano da verificare.

## 13. Livello di certezza

**Implementato**: le regole descritte corrispondono alle routine e alle
variabili attuali del programma.

**Da verificare**: che questa geometria produca nel lungo periodo strutture
stabili, contatti sufficientemente risolti e osservabili indipendenti da seed e
artefatti di embedding.

**Aperto**: una derivazione continua o geometrica più fondamentale dalla quale
la topologia di contatto, il raggio $3\,\mathrm{med}(\lambda)$ e la
ricostruzione storica degli archi emergano senza assunzioni ulteriori.
