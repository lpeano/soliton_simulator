# Fisica implementata del sistema dei solitoni relazionali

Questo documento ricostruisce la fisica **implementata** in `soliton_simulator.py`.
Non è una derivazione da un'azione fondamentale e non dimostra che il modello descriva
la natura: distingue le equazioni del programma dalle interpretazioni e dalle ipotesi
ancora da verificare numericamente.

## 1. Oggetti fondamentali

Il sistema è un grafo dinamico non orientato

$$G(t)=(V(t),E(t)), \qquad V=\{1,\ldots,N(t)\}.$$

Ogni vertice è un puntatore di fase, non una particella con proprietà materiali
proprie. Il nodo $i$ porta:

- fase scalare $\phi_i$ e velocità di fase $v_i$ (`phivel`);
- fase iniziale $\phi_{0i}$, usata nella memoria del legame;
- chiralità discreta $\chi_i\in\{-1,+1\}$ (`perc_chi`);
- stato spinoriale e vettore di Bloch $\mathbf n_i$;
- coordinate $\mathbf x_i$, usate per connettività, embedding e disegno.

Il puntatore elementare è

$$z_i=e^{\mathrm{i}\phi_i}, \qquad |z_i|=1.$$

La grandezza fisica primaria del modello non è la posizione di un puntatore, ma il
campo d'interferenza prodotto dalle relazioni fra puntatori.

## 2. Campo e materia

A ogni arco $e=(i,j)$ sono associate distanza metrica $d_{ij}$, portata locale
$\lambda_{ij}$ e peso $w_{ij}$. Il campo discreto è

$$F_i=\sum_{j:(i,j)\in E}w_{ij}z_j, \qquad \Psi_i=S(F_i),$$

con saturazione razionale

$$S(F)=\frac{F}{1+\gamma\sqrt{|F|^2+\varepsilon}},
\qquad \rho_i=|\Psi_i|^2.$$

$\rho_i$ è la densità/coerenza locale usata dal programma come proxy della materia.
Il rendering volumetrico sottrae il fondo incoerente e mostra separatamente interferenza
costruttiva e distruttiva.

## 3. Pesi, torsione e tempo proprio

Il peso degli archi è

$$w_{ij}=e^{-d_{ij}/\lambda_{ij}}r_ir_j
\exp\left(\frac{\alpha\tau_{ij}}{1+\beta\tau_{ij}}\right),$$

con

$$r_i=\min\left(1,\frac{\eta_i}{\tau_A}\right),
\qquad \tau_{ij}=\frac{|tw_{ij}|}{\Phi_{crit}}.$$

Il rinforzo razionale impedisce che il peso diverga con la torsione. La memoria
$\eta_i$ cresce con il tempo proprio e viene limitata dalla scala temporale dello
stato.

Il ritmo locale è ricavato dalla variazione della fase del campo:

$$f_i=\frac{|\Delta\arg\Psi_i|}{DT}, \qquad x_i=\frac{f_i}{\mathrm{med}(f)},$$

$$r_i^{(\tau)}=1+\tau_{loc}\left(
\frac{x_i/\sqrt{1+x_i^2}}{1/\sqrt 2}-1\right),
\qquad dt_i=DT\,r_i^{(\tau)}.$$

Il passo di un arco è la media dei passi locali ai suoi estremi.

Nella sincronizzazione pesata sul taglio, il profilo del pozzo non viene
normalizzato con una media dell'intero sistema. Se $W$ è la matrice dei pesi e
$\mathbf 1$ il vettore unitario, il riferimento locale è

$$\bar p_i=\frac{(W\,\mathbf p)_i}{(W\,\mathbf 1)_i},
\qquad p_i^{rel}=\frac{p_i}{\bar p_i}.$$

Analogamente, la scala del taglio usa l'RMS dei soli vicini:

$$s_i^{loc}=\sqrt{\frac{(W\,\mathbf s^2)_i}{(W\,\mathbf 1)_i}},
\qquad K_i^{shear}=1+\frac{s_i}{s_i^{loc}}.$$

Queste normalizzazioni sono topologicamente locali; non usano `pozzo.mean()` o
`disp_shear.mean()` sull'intero array.

## 4. Dinamica delle fasi

Definendo

$$A_{ij}=w_{ij}\cos(\phi_{0i}-\phi_{0j}),$$

il termine di fase è

$$T_i^{fase}=K_C\,\mathrm{Im}\left[z_i^*(M(A)z)_i\right].$$

L'integrazione discreta è

$$v_i^{n+1}=v_i^n+\frac{dt_i}{M_{ph}}
\left(T_i-\Gamma_i v_i^n\right),$$

$$\phi_i^{n+1}=\phi_i^n+dt_i v_i^{n+1}+\Delta\phi_i^{sync}
\pmod{4\pi}.$$

Il codice usa snapshot di inizio passo per rendere coerenti peso, fase e torsione.
Con `SYNC_UPDATE=True` (flag `--sync`) anche il campo materia viene valutato
sulla fase dello snapshot e la sorgente metrica usa il `P_eq` dello snapshot.
Questo chiude le due riletture cross-sistema principali; l'integratore
`phivel -> phi` e il sottociclo metrico `d/vd/d0` restano sequenziali per
costruzione. `--sync` è quindi un ETC esteso, non una transazione atomica di
ogni variabile dell'intero programma.
Nel regime deterministico il termine dissipativo è sostituito da un termostato:

$$E_{\mathrm{cin}}=\langle v^2\rangle, \qquad T_{*}=c_s^2P_{eq},
\qquad e=\frac{E_{\mathrm{cin}}-T_{*}}{T_{*}},$$

$$\xi^{n+1}=\xi^n+\frac{dt}{\tau_{*}}(e-\xi^n),
\qquad v^{n+1}=v^n+\frac{dt}{M_{ph}}(T-\xi v).$$

## 5. Repulsione emergente

La repulsione principale non usa `MU_PSI` come manopola. Il gradiente della densità
rispetto alle fasi è

$$D_i=2\,\mathrm{Im}\left[z_i^*(M(w)\Psi)_i\right].$$

La vicinanza locale al collasso è

$$u_i=q_i c_i,$$

dove $q_i$ è il numero efficace di vicini coerenti diviso per $N_c$, mentre

$$c_i=\max\left(0,\cos(\phi_i-\arg\Psi_i)\right)$$

è l'allineamento del nodo con il campo. Il fattore applicato alla coppia è

$$R_i=u_i(u_i+2), \qquad T_i\leftarrow T_i-R_iD_i.$$

Il meccanismo agisce soprattutto sul nucleo costruttivo; la componente in antifase non
alimenta direttamente la repulsione del nucleo.

## 6. Schermatura e densità critica

La soglia critica adattiva è

$$N_{c}(\lambda,\gamma,s)=C\lambda^{-3}\gamma^b(1+s)^\theta,
\qquad s=\gamma|F|,$$

con coefficienti e crossover definiti nel codice. Alla scala nativa:

$$\rho_{c}=\frac{N_{c}}{(4/3)\pi LAM^3}.$$

La schermatura è attiva di default. Con $u=\rho/\rho_c$ il fattore continuo è

$$f(u)=\frac{1}{1+\log(1+e^{u-1})},$$

quindi

$$\lambda_i=\max\left(LAM\,f(u_i),\;0.15\,LAM\right),
\qquad \lambda_{ij}=\frac{\lambda_i+\lambda_j}{2}.$$

Il limite $0.15\,LAM$ è il limite geometrico attualmente codificato. `P_LAM` e
`LAM_MIN` non controllano più la dinamica della schermatura.

## 7. Torsione, olonomia e mitosi

La differenza di fase sull'arco è avvolta e combinata con il contributo dipolare

$$\Delta\phi_{\mathrm{dip},ij}=\frac{\pi}{2}(\chi_i-\chi_j).$$

In doppia copertura:

$$tw_{ij}^{n+1}=tw_{ij}^{n}+
\mathrm{wrap}_{8\pi}(\Delta\phi_{ij}+\Delta\phi_{\mathrm{dip},ij}-tw_{ij}^{\mathrm{prec}})
-\frac{dt_{ij}}{\tau_{tw,ij}}tw_{ij}^{n}.$$

Il quanto di olonomia è

$$\Phi_{crit}=2\pi.$$

Con `TORS_4PI=True`, la soglia media della mitosi è costruita come

$$\Phi_{mit}=\Phi_{crit}+\pi=3\pi,$$

cioè un giro completo più il massimo twist dipolare. La soglia viene modulata dal
gradiente locale del tempo proprio. La probabilità di nascita è una campana sopra
soglia che si spegne verso $4\pi$; schematicamente:

$$p_{\mathrm{mit}}=\mathrm{clip}\left[
S\left(\max\left(0,\frac{|tw|}{\Phi_{soglia}}-1\right)\right)
\left(1-\frac{|tw|}{4\pi}\right)\frac{1}{1+|tw|/\Phi_{crit}},0,1\right].$$

La mitosi divide l'arco in due e colloca il figlio nel punto medio della fase
geodetica. È una raffinazione topologica, non un trasporto ordinario. Gli anti-nodi
di Schwinger sono un canale aggiuntivo, opzionale, a fase opposta.

## 8. Metrica dinamica

La deformazione dell'arco è $q_{ij}=d_{ij}-d_{0,ij}$. Il codice integra

$$\ddot q_{ij}=c_s^2\Delta_Gq_{ij}+a_{ij}-\beta_{ij}\dot q_{ij},$$

con sorgente fenomenologica

$$a_{ij}=\alpha_M\frac{\rho_{ij}-P_{eq,ij}}{P_{eq,ij}},
\qquad \rho_{ij}=\frac{\rho_i+\rho_j}{2},$$

oppure sorgente hamiltoniana

$$a^H_{ij}=-K_C\frac{w_{ij}}{LAM}
\cos(\phi_{0i}-\phi_{0j})\cos(\Delta\phi_{ij}).$$

Per lo smorzamento locale di scala:

$$\beta_{ij}=\frac{2\zeta_M c_s}{d_{ij}}.$$

La lunghezza di riposo evolve plasticamente:

$$\dot d_{0,ij}=\frac{d_{ij}-d_{0,ij}}{\tau_{p,ij}}.$$

Quando sono attive le scale temporali locali, il codice usa il nucleo elastico

$$\tau_{p,ij}=\frac{d_{ij}}{c_s}\left[1+ELAST\_C\,
\max\left(\frac{\rho_{ij}}{\rho_{med}}-1,0\right)\right],$$

con `ELAST_C=100` come valore storico predefinito. Il flag `--elast-c` è una
sonda reversibile: `ELAST_C=0` disattiva il rinforzo, mentre `30/100/300`
permettono il test di sensibilità. La ridondanza rispetto al rinforzo di shear
e l'invarianza di scala sono ancora da verificare.

La deformazione $d-d_0$, non la distanza assoluta, è la sorgente delle onde metriche.

### Integratore metrico sperimentale

Il ramo canonico usa Eulero esplicito. Con `--verlet` il sottociclo metrico
usa invece un predictor-corrector Velocity-Verlet: calcola l'accelerazione a
$t$, aggiorna la velocità a metà passo, calcola la nuova distanza e richiude la
velocità con l'accelerazione a $t+\Delta t$. Il ramo mantiene la sorgente dello
stesso passo e ricalcola lo smorzamento locale sulla nuova distanza.

Il flag è intenzionalmente **off di default** per garantire la non regressione.
La maggiore accuratezza del secondo ordine e l'eventuale riduzione delle
oscillazioni devono essere verificate con un confronto A/B su più semi; non sono
conseguenze dimostrate dalla sola implementazione.

## 9. Vuoto e fondo

L'energia dinamica del vuoto è

$$\Lambda_{vuoto}=\langle|\Psi|^2\rangle.$$

Lo scuotimento locale usa lo stress degli archi $\sigma_i$ e viene soppresso dalla
coerenza:

$$A_i=\sqrt{\sigma_i}\frac{\sqrt{\Lambda_{\mathrm{vuoto}}}}
 {1+\rho_i/\Lambda_{\mathrm{vuoto}}},
\qquad \Delta v_i\propto\mathcal N(0,1)A_i\chi_i.$$

Il fondo $P_{eq}$ insegue la densità e viene diffuso sulla topologia degli archi. Nel
regime stocastico lo scuotimento eccita il vuoto; nel deterministico può essere spento.

## 10. Settore spinoriale SU(2)

Il nodo spinoriale è rappresentato da un vettore di Bloch unitario

$$\mathbf n_i=(\sin b_i\cos a_i,\sin b_i\sin a_i,\cos b_i),
\qquad |\mathbf n_i|=1.$$

Il campo $\mathbf B_i$ è la media pesata dei vicini ritardati. I legami fra chiralità
uguali riflettono la componente $z$; quelli fra chiralità opposte non la riflettono.
Questa è l'implementazione discreta di due generatori effettivi non commutanti,
associati schematicamente a $\sigma_x$ e $\sigma_z$.

La memoria spinoriale evolve come

$$\boldsymbol\omega_i^{n+1}=\boldsymbol\omega_i^n+dt_i
\left(\frac{\mathbf B_i\times\mathbf n_i}{\rho_i}
-\frac{\boldsymbol\omega_i^n}{\tau_{A,i}}\right).$$

Poi il Bloch viene ruotato attorno a $\boldsymbol\omega_i$ con angolo
$\vartheta_i=|\boldsymbol\omega_i|dt_i$ mediante la formula di Rodrigues. Questa
evoluzione è però **orfana dal commit d2c76f3** (2026-09-02): la chiamata a
`_passo_spinoriale` fu persa come collaterale del refactor a snapshot/commit-atomico
ETC. Nel percorso di default lo spinore resta quindi **congelato** all'inizializzazione
planare ($\mathbf n_i=(\sin b_i,0,\cos b_i)$, coplanari), letto ma mai ruotato. Il flag
`--spinore-vivo` (default off) **reinnesta** l'evoluzione nell'ordine ETC (legge lo
snapshot $t$, prima del commit atomico delle fasi). È sotto test A/B, non ancora
promosso a default; ordine macroscopico, precessione e curvatura non-abeliana su
spinore vivo sono osservabili **da validare**. Ogni misura di fase di Berry precedente
al reinnesto è ~0 per spinore congelato, non per natura abeliana del sistema.

### Circolazione topologica spin-dipendente

La diagnostica passiva `circolazione_topologica()` costruisce una base di cicli
fondamentali direttamente dagli archi `net.i` e `net.j`, senza usare coordinate
o embedding. La corrente dell'arco è

$$J_{ij}=w_{ij}\,\frac{\rho_i+\rho_j}{2}\,
(\mathbf n_i\cdot\mathbf n_j)\,\frac{tw_{ij}}{\Phi_{crit}}.$$

Per un ciclo $C$ la circolazione è

$$\Gamma_C=\sum_{e\in C}\sigma_{C,e}J_e,$$

dove $\sigma_{C,e}$ tiene conto del verso dell'arco nel ciclo. Il diagnostico
registra numero di cicli, massimo, media assoluta e media firmata di
$\Gamma_C$. La misura è passiva: non modifica fasi, metrica o coordinate.

**Risultato misurato (dimostrato).** Sul sistema reale $\Gamma_C\simeq0$ (zero
numerico, $\sim10^{-15}$): il twist d'equilibrio è essenzialmente un gradiente di
fase, dunque curl-free. La "rotazione" vista in `m0_Lz` (asse PCA, dipendente
dall'embedding) è artefatto delle coordinate, non corrente circolante reale.

**Componenti non-gradientali (decomposizione di Hodge).** Accanto a $\Gamma_C$ il
diagnostico misura due grandezze gauge-invarianti che catturano ciò che il gradiente
non ha: l'**olonomia di fase** $\oint_C\mathrm{d}\phi$ (somma di $\phi_i-\phi_j$
attorno al ciclo, componente armonica/vortici) e la **fase di Berry spinoriale**,
calcolata come invariante di Bargmann–Pancharatnam

$$\gamma_C=-\arg\prod_{k}\langle\psi_k|\psi_{k+1}\rangle,$$

prodotto ciclico degli overlap fra spinori attorno al ciclo. Essendo ciclico è
indipendente dal vertice di partenza e dalle fasi arbitrarie dei singoli spinori
(gauge-invariante; verificato invariante per rinumerazione degli archi, rotazione
globale $SO(3)$ dei Bloch ed embedding). Le colonne sono `olonomia_fase_*` e
`berry_spin_*`. Con spinore congelato (default) $\gamma_C\equiv0$ per costruzione
(Bloch coplanari); diventa misurabile solo con `--spinore-vivo`.

## 11. Gravitazione, frame-dragging e viriale

Il twist orientato produce una coppia locale schematizzabile come

$$T_i^{\mathrm{drag}}=\left\langle\frac{tw_{ij}}{\Phi_{\mathrm{crit}}}\right\rangle_j.$$

Con `--viriale`, la risposta viene ripartita:

$$g_r=g\cos^2\vartheta, \qquad g_t=|g|\sin^2\vartheta.$$

L'angolo deriva da grandezze dello stato, come pozzo, curl e twist coerente. Con
`--zeta-vir` lo stesso fattore riduce il solo smorzamento radiale. `--kfrange` è
invece un canale sperimentale parametrico e non una legge derivata.

### Chiralità emergente del core (`--chi-core`)

La chiralità microscopica `perc_chi` resta assegnata alla nascita ed ereditata
dai figli. Con `--chi-core` il codice calcola invece una chiralità collettiva
locale senza selezionare a priori il segno. Per ogni nodo, con
$I_k=|\Psi_k|^2$, usa il massimo del nodo e dei suoi vicini come $\rho_0$ e la
soglia

$$\rho_c=\frac{N_c(\lambda,\gamma,s)}{(4/3)\pi\lambda_{base}^3}.$$

Il raggio sopra soglia è

$$R_{core,k}=\lambda_{eff,k}\max\left(\log\frac{\rho_{0,k}}{\rho_c},0\right).$$

La chiralità del core è la proiezione pesata da $|\Psi|^2$ di tutti i nodi
nella maschera locale. Quando attivo, `CHI_CORE` guida i canali collettivi
spinoriali, il twist dipolare e il frame-dragging; nascita, scuotimento,
mitosi ed eredità mantengono `perc_chi`. La legge è implementata ma **in
verifica**: stabilità del segno e interpretazione topologica del guscio non
sono dimostrate.

## 12. Osservabili e livello di evidenza

| Osservabile | Definizione | Uso |
|---|---|---|
| $\rho_i$ | $|\Psi_i|^2$ | densità/coerenza locale |
| `coer_g` | $|N^{-1}\sum_i e^{i\phi_i}|$ | ordine globale |
| `coer_l` | coerenza locale col campo pesato | ordine relazionale |
| `tw_q` | $\langle|tw|\rangle/(2\pi)$ | quanti di olonomia |
| `ncrit_adattivo` | $N_c$ dal crossover corrente | soglia critica |
| `lambda_eff_*` | statistiche di $\lambda_i$ | contrasto nucleo/guscio |
| `dist_ij` | distanza fra baricentri | separazione di strutture |
| `Lz_orb_ij` | variazione dell'angolo della congiungente | precessione candidata |
| `rchi_ratio` | $r_{\chi=-1}/r_{\chi=+1}$ | test del guscio chirale |

**Dimostrato** significa misurato in modo robusto e ripetibile nelle condizioni
indicate. **In verifica** significa che il segnale esiste ma dipende da durata,
seed o regime. **Aperto** significa che la previsione non è ancora stata testata.
Una formula implementata è una legge del programma, non automaticamente una legge
fisica del mondo.
