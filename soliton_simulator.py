# NOTA: la repulsione dell'interferenza e' una LEGGE (REPULS_LEGGE, default attivo): scatta
# via conversione dinamica u = riempimento*coerenza rispetto a Ncrit adattivo, senza parametri
# ne' esponenti fissi. La coerenza e' quella col nucleo (allineamento col campo Psi locale).
# Sostituisce la vecchia repulsione a parametro MU_PSI. Reversibile: REPULS_LEGGE=False torna
# al comportamento precedente. Verifica del plateau su run lunghi in corso.
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IL MURATORE DI PLANCK  (v9)  -- sistema dei solitoni relazionali

PRINCIPIO GUIDA: "guarda la luna, non il dito".
I solitoni sono PUNTATORI, non oggetti fisici. Materia, spazio e tempo emergono
dalle loro INTERFERENZE. Le coordinate non esistono nel modello: qui servono
solo al disegno, e vengono RILASSATE verso le distanze relazionali d_ij, cosi'
che sullo schermo si veda la geometria vera e non un fantasma cartesiano.

TUTTE LE LEGGI SONO SEMPRE ATTIVE — nessun interruttore per la fisica:
  * VUOTO RELAZIONALE sempre presente: nessuna scena parte dal nulla
  * fasi al SECOND'ORDINE (inerzia)             -> Leggi IV, V, VII
  * MEMORIA HEBBIANA dei legami, cos(dphi0)     -> Legge VI
  * SATURAZIONE del campo, tetto 1/gamma        -> Leggi XV, XVIII
  * METRICA DINAMICA sugli archi:
        d'' = c_s^2 Lap(d - d0) + a (rho - P_eq)/P_eq - b d'
    le onde viaggiano sulla DEFORMAZIONE (d - d0): a riposo il termine e'
    identicamente nullo, quindi il vuoto non deriva e SOLO la materia muove la
    geometria (corr. materia-deformazione misurata: da +0.34 a +0.79)
  * VUOTO DI SFONDO: P_eq insegue la mediana GLOBALE di rho, non quella locale:
    assorbe la crescita di densita' senza cancellare le anomalie locali
  * MEMORIA PLASTICA della lunghezza di riposo (TAU_P)
  * MITOSI TOPOLOGICA (criterio 2pi): l'arco si sdoppia quando ha accumulato un
    QUANTO DI OLONOMIA, non quando e' teso -- immune alla plasticita'.
    Funziona da RAFFINAMENTO: mentre la metrica si dilata, la struttura discreta
    si suddivide per restare risolta, e i legami tornano entro portata.
    Il neonato prende il PUNTO MEDIO GEODETICO della fase: l'olonomia di ogni
    ciclo che attraversa l'arco resta invariata (Legge III)

RENDERING DELLA MATERIA (v9). Il pannello di sinistra disegna il CAMPO
D'INTERFERENZA nello spazio, Psi(x) = somma_i exp(-|x-p_i|/LAM) e^{i phi_i},
saturato e ricalcolato A OGNI PASSO, sulle coordinate rilassate verso le d_ij.
Non i puntatori: disegnarli significherebbe colorare il dito con la luce della
luna, e la forma sullo schermo sarebbe quella della nuvola, che e' fissa.
Non gli archi: dove l'interferenza si annulla i legami ci sono comunque, quindi
la cancellazione resterebbe invisibile.
LA MATERIA E' CIO' CHE SOPRAVVIVE ALL'ANNULLAMENTO DELLE FASI, e vive nello
spazio FRA i puntatori: due domini in opposizione mostrano due lobi separati da
una cicatrice nera dove la materia e' stata distrutta pur essendoci tutti i
puntatori. Inquadratura monotona e scala di colore ancorata: la dilatazione
dello spazio e la diluizione della materia si vedono, invece di essere
rinormalizzate via a ogni fotogramma.

interattivo:  python soliton_simulator.py
headless:     python soliton_simulator.py --test URTO --out urto.mp4
"""
# ============================================================================
# TASK APERTO (registrato) -- MATERIA STABILE: freno non-locale guscio<-nucleo
# ----------------------------------------------------------------------------
# SCOPERTA STRUTTURALE (misurata): il grumo NON e' omogeneo. Ha
#   - un NUCLEO congelato: alta densita', bassa torsione, poca mitosi
#   - un GUSCIO attivo: bassa densita', alta torsione, dove avviene la mitosi
# E' la struttura di un buco nero (nucleo/singolarita' + guscio/orizzonte).
# La crescita illimitata viene dal GUSCIO che continua a creare materia.
#
# PISTE CHIUSE (ognuna con difetto strutturale misurato):
#   - torsione: satura a 2.5pi
#   - tempo proprio SURROGATO della mitosi (1+torsione/PHI_CRIT): eredita la
#     saturazione della torsione -> non raggiunge mai il tetto 4pi di spegnimento
#   - dilatazione metrica: troppo debole (+69% vs massa x1000)
#   - repulsione di fase MU_PSI: agisce sul PICCO, non sui portatori
#   - antifase delle aggiunte (ANTIFASE_ADD, interruttore presente): NON annichila
#     (sfasare un nodo non lo cancella, resta e la massa cresce) -> muro dell'1%
#   - ritmo vero dell'interferenza: rumoroso, instabile, satura al clip
#
# DIREZIONE APERTA (accoppiamento non-locale, embrionale nel sistema):
#   Esiste gia' un segnale: quando il NUCLEO e' pieno, la mitosi del GUSCIO cala
#   (da 5 a 1) mentre la torsione locale del guscio resta costante, e il tempo
#   proprio del guscio si dilata (1->11). Cioe' il guscio GIA' risponde allo stato
#   del nucleo via tempo proprio, ma TROPPO DEBOLMENTE per fermare la crescita.
#
# SVOLTA (schermatura dolce dell'interferenza -- PRIMA stabilizzazione sana):
#   Le masse crescono per interferenza -> solo una SCHERMATURA dall'interferenza
#   le stabilizza (intuizione di Luca). Meccanismo: lambda_nodi() ora accorcia la
#   portata dell'interferenza dove e' denso, con TRANSIZIONE DOLCE (tanh), non un
#   muro (la vecchia potenza (dl/med)^P_LAM esplodeva). Con P_LAM=1, LAM_MIN=0.3 il
#   grumo per la PRIMA VOLTA si stabilizza a taglia finita (massa si assesta, non
#   cresce senza limite, e lambda resta finita). Il nucleo denso, schermato, smette
#   di sentire la propria interferenza collettiva -> mitosi non alimentata -> stop.
#   Collega spin/ordine: nucleo = cristallizzato (spin allineati, sync forte perche'
#   denso); guscio = liquido (spin frustrati, sync debole perche' rado). Stabilita'
#   = cristallizzazione che si chiude quando la schermatura isola il denso.
#
# DIFETTO DA RISOLVERE (verifica di Luca "P_LAM serve?"):
#   La taglia di equilibrio dipende da DUE parametri liberi P_LAM e LAM_MIN, in modo
#   NON monotono (P_LAM 0.5/1/2 -> taglia 4983/9669/4400; LAM_MIN 0.1/0.3 -> 2369/9669).
#   E' stabilizzazione per TARATURA, non derivata = parametro travestito.
#
# DA FARE:
#   1. ANCORARE scala e profondita' della schermatura a N_critico (non parametri):
#      la scala della transizione = densita' critica, non la mediana generica;
#      LAM_MIN dal rapporto densita'/densita'_critica, non un numero scelto.
#      Obiettivo: taglia di equilibrio DETERMINATA dal sistema (~N_c), non scelta.
#   2. VINCOLO buchi neri: schermatura totale = orizzonte, deve restare possibile
#      (schermatura parziale = materia stabile; totale = buco nero).
#   3. NULL-TEST: gusci a tempo proprio, esponente M(N), olonomia, causalita', semi
#   4. validare su TEMPI LUNGHI (hardware di Luca): taglia stabile e coerente?
#
# NB stato interruttori: P_LAM=0 default (schermatura spenta finche' non ancorata a
#   N_c); lambda_nodi() ora usa la forma DOLCE (tanh) se P_LAM>0, non piu' la potenza
#   che esplodeva. LAM_MIN, COPPIA_DENSITA, ANTIFASE_ADD presenti (esplorativi).
# ============================================================================
import numpy as np

# ============================================================================
# INTERRUTTORE DI REGIME
#   "stocastico"     -> vuoto stocastico ATTIVO. Configurazione VALIDATA e STABILE. DEFAULT.
#                       Il vuoto fa da termostato e da sorgente di asimmetria; la materia
#                       condensa dalle sue fluttuazioni. E' il sistema canonico.
#   "deterministico" -> vuoto SPENTO. Mitosi modulata dal TEMPO PROPRIO LOCALE (WIP).
#                       Impulso iniziale conservativo nella semina, attrito ridotto. Proof of
#                       concept: la materia condensa dal seme iniziale e il termostato da tempo
#                       proprio controlla in parte l'energia, ma lo stress resta alto e manca
#                       l'innesco della prima asimmetria (tau omogeneo all'inizio).
#                       DA RIPRENDERE: seme iniziale di asimmetria strutturale (fase/torsione).
# APERTO: la PRECESSIONE fra due masse persiste in regime deterministico? Se si', il momento
#         angolare netto NON dipende dal vuoto stocastico (risultato forte).
REGIME = "deterministico"     # <-- cambia qui: "stocastico" (stabile) | "deterministico" (default: forma pura + calcio vett)

if REGIME == "deterministico":
    _SCUOTIMENTO_REGIME = False
    _G_PH_REGIME = 3e-3        # attrito basso ma non nullo (1e-4 e 0 divergono)
    _TAU_A_REGIME = 50.0       # alta persistenza memoria spinoriale
    _CALORE_INIT = 0.4         # impulso iniziale conservativo (punto zero)
else:
    _SCUOTIMENTO_REGIME = True
    _G_PH_REGIME = 0.15        # attrito canonico validato
    _TAU_A_REGIME = 2.0        # canonico
    _CALORE_INIT = 0.0         # phivel nasce a zero (canonico)
# ============================================================================
import sys as _sys
# Backend non-interattivo (Agg) SOLO quando si registra un video headless (--test).
# Con altri flag (es. --scala) senza --test si vuole la GUI interattiva, che richiede
# un backend con finestra: non forzare Agg in quel caso.
if "--test" in _sys.argv:
    import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
# distruzione (ciano) <- NERO (nessuna interferenza) -> materia (fuoco)
CMAP_INTERF = LinearSegmentedColormap.from_list("interf", [
    (0.00, "#7ff5ff"), (0.25, "#1170a0"), (0.50, "#000000"),
    (0.72, "#b03060"), (0.88, "#ff8c1a"), (1.00, "#fff5cc")])
from matplotlib.widgets import Button
from matplotlib.animation import FuncAnimation
from scipy import sparse
from scipy.spatial import cKDTree
from scipy.ndimage import gaussian_filter

LAM      = 0.8
LAM_BASE = 0.8   # lunghezza d'onda del solitone fondamentale (~2 lunghezze di Planck)
# COARSE-GRAINING (dettare la scala): un solitone-blocco rappresenta SCALA_B solitoni
# fini. Regole di scala derivate imponendo la conservazione delle tre leggi al continuo
# (Poisson, bilancio gravita'/espansione, precessione), e verificate numericamente:
#   lambda_eff  = lambda_base * SCALA_B^(1/3)   (portata del kernel: il blocco e' piu' largo)
#   massa/solitone = SCALA_B * massa_fine        (ogni blocco pesa SCALA_B fini: preserva Poisson)
#   rho_eq, cs, alpha, PHI_CRIT invarianti       (densita' e proprieta' del mezzo non scalano)
# SCALA_B=1 e' la scala di Planck (solitone fondamentale). Salendo, si copre una
# gerarchia di scale reali: il blocco copre SCALA_B^(1/3) lunghezze d'onda del solitone.
SCALA_B  = 1.0
# BOX eliminato come parametro fisico: il sistema e' relazionale, le coordinate non
# esistono nella fisica (servono solo al disegno, rilassate verso le d_ij). La scala
# di semina deriva da LAMBDA (la scala propria del sistema): i puntatori del vuoto
# nascono a distanza ~lambda l'uno dall'altro. Nessun box scelto a mano.
# TARGET FUTURO (strada B): eliminare anche il seme iniziale, dando al vuoto un
# feedback che stabilizzi la sua densita' a un equilibrio EMERGENTE (misurato: oggi
# la densita' del vuoto non ha un attrattore pulito, dipende dal seme; serve un
# meccanismo di stabilizzazione prima di poter eliminare il seme iniziale).
GAMMA    = 0.05
# scala caratteristica di semina e disegno: derivata da LAMBDA, non un box scelto.
# ~10 lambda copre l'estensione tipica di un addensamento sulla scala del sistema.
def _scala_sistema(): return 10.0 * LAM
# DT: NON e' un passo temporale continuo (da raffinare con dt->0), ma l'avanzamento di UNO
# STATO nella successione discreta degli stati del sistema — un contatore, un tick. Il sistema
# E' una successione di stati discreti; DT ne e' l'incremento. E' la granularita' irriducibile,
# la frequenza di Planck del sistema (i solitoni vivono alla doppia lunghezza di Planck). Sotto
# questo tick non c'e' nulla: e' il riferimento assoluto comune. Le frequenze FONDAMENTALI (che
# DEFINISCONO il tempo proprio, come f_i nel ritmo) si misurano rispetto a DT; le frequenze
# DERIVATE/IMMERSE (processi dentro la materia, come lo spin) si leggono nel tempo proprio locale.
DT       = 0.01
K_C      = 2.0
# SINCRONIZZAZIONE PESATA DAL TEMPO PROPRIO GRAVITAZIONALE (il pozzo). Off di default
# (K_SYNC=0). Idea: due solitoni alla stessa profondita' del pozzo hanno lo stesso tempo
# proprio (dilatazione gravitazionale, come in RG) e si agganciano in fase, come i pendoli
# di Huygens che battono allo stesso ritmo. La coppia sin(phi_j-phi_i) e' pesata dalla
# VICINANZA nel pozzo g(Phi_i-Phi_j): forte dove i tempi propri coincidono (cuore denso e
# uniforme della materia -> nucleo coerente), debole dove il pozzo varia (bordo, vuoto ->
# resta disordinato). Cosi' la coerenza EMERGE dal pozzo, non e' imposta, e sbiadisce con
# la distanza dalla massa. Risolve la materia che non si ordina (guscio azzurro onnipresente).
K_SYNC   = 1.0   # interruttore/scala della LEGGE di sincronizzazione (1 = legge piena, 0 = off).
                 # La forza per nodo NON e' piu' imposta: emerge dalla dispersione locale del
                 # tempo proprio (pozzo dal centro di massa) secondo la soglia di Kuramoto
                 # (costante universale 2/pi). Dove i tempi propri sono simili la sync ordina
                 # (nucleo -> materia coerente), dove dispersi resta libera (vuoto). Poiche' il
                 # pozzo scala col coarse-graining, la legge e' indipendente dalla scala.
SYNC_W   = 1.0   # (riservato)
M_PH     = 1.0
G_PH     = _G_PH_REGIME
def R_CONN(): return 3.0 * LAM   # raggio di connessione: funzione di LAM, cosi' scala
                                 # correttamente col coarse-graining (LAM->LAM*B^(1/3)).
                                 # Era una costante calcolata all'import: restava congelata
                                 # al valore iniziale mentre LAM cambiava, sconnettendo il
                                 # grafo sotto compressione di scala. Ora e' dinamica.
DIFF_RES = 0.0          # DIFFUSIONE DEL RESIDUO. 0 = si diffonde P_eq (come finora):
                        # il punto fisso e' una MISCELA di rho e della media dei vicini,
                        # sicche' P_eq != rho ovunque rho devii dal proprio vicinato, e
                        # quel residuo E' la sorgente che espande il vuoto in eterno.
                        # 1 = si diffonde il RESIDUO (rho - P_eq): a residuo nullo la
                        # diffusione si annulla, dunque P_eq = rho e' punto fisso ESATTO
                        # e il vuoto acquista un equilibrio, mentre il transitorio
                        # continua a essere lisciato.
ALPHA_NAT= 0.0          # SORGENTE IN UNITA' NATURALI. 0 = usa ALPHA_M (costante con
                        # le dimensioni di un'accelerazione, dunque una scala assoluta).
                        # >0: src = ALPHA_NAT*(c_s^2/d_ij)*(rho-P_eq)/P_eq, dove
                        # c_s^2/d_ij E' l'accelerazione caratteristica LOCALE dell'arco.
                        # Con ALPHA_NAT=1 il coefficiente sparisce del tutto: ALPHA_M
                        # e' eliminata in favore di c_s e della lunghezza dell'arco,
                        # entrambe gia' presenti. Nessun riferimento globale.
HAM_SRC  = 0.0          # SORGENTE DELLA METRICA. 0 = fenomenologica, alpha*(rho-P_eq)/P_eq
                        # con il suo parametro ALPHA_M. 1 = forza HAMILTONIANA, ricavata
                        # dal potenziale delle fasi V = -K_C*somma w cos(dphi0)cos(dphi),
                        # che dipende da d attraverso w = exp(-d/lambda):
                        #    F = -dV/d(d_ij) = -K_C*(w/lambda)*cos(dphi0)*cos(dphi)
                        # Non aggiunge parametri: li TOGLIE, perche' ALPHA_M sparisce
                        # e restano K_C e lambda che esistono gia'. L'accoppiamento
                        # metrica-fasi diventa conservativo per costruzione.
                        # Misurato: |F_ham|/|src| = 0,15 nel vuoto ma 1,18-1,30 nella
                        # materia, quindi la sostituzione agisce dove c'e' materia.
ZETA_M   = 0.75         # SMORZAMENTO METRICO ADIMENSIONALE (ATTIVO). 0 = BETA_M costante
                        # (come finora). >0: beta_ij = 2*ZETA_M*c_s/d_ij, cioe' un
                        # multiplo fisso della frequenza LOCALE dell'arco, costruito
                        # con la sola lunghezza di quell'arco: nessun riferimento
                        # globale. Cosi' il rapporto di smorzamento resta ZETA_M
                        # comunque il mezzo si dilati, mentre con beta costante esso
                        # vale beta*d/(2c_s) e cresce con d, spegnendo le onde:
                        # misurato 0,51 a t=50 e 1,10 a t=400.
                        # ATTIVO PER DEFAULT a 0,75: contrasto materia/vuoto x6,0 e
                        # x5,8 su due semi, archi entro portata dal 5,8% al 24,6%,
                        # a parita' di numero di nodi. Sotto 1 il mezzo resta
                        # sottosmorzato per sempre, condizione che serve alle onde.
ZETA_LOC = False        # SMORZAMENTO METRICO LOCALE (legge, non parametro): se True, zeta scende
TAU_LOC  = 1.0          # TEMPO PROPRIO LOCALE ATTIVO. Ogni nodo evolve al proprio ritmo
                        # (0 = un solo DT globale, com'era prima). 1 = ogni nodo avanza col PROPRIO
                        # ritmo, ricavato dalla frequenza di Psi (Legge V) e mai
                        # da quella dei puntatori, che ne inverte il segno.
                        # Se il modello e' invariante per riparametrizzazione, gli
                        # osservabili RELAZIONALI non devono cambiare: e' un test,
                        # non una legge nuova.
SCHERMATURA = False     # LEGGE DI SCHERMATURA (derivata da N_critico, senza parametri liberi):
                        # la portata dell interferenza si accorcia dove rho supera la densita
                        # critica -> la massa densa si scherma e si stabilizza. Default off
                        # finche non validata sui tempi lunghi con i null-test.
LAM_MIN  = 0.3          # SCHERMATURA (con P_LAM>0): frazione minima della portata nel denso.
                        # PARAMETRO da derivare/ancorare a N_c (vedi TASK): con P_LAM insieme
                        # determina la taglia di equilibrio, per ora in modo tarato non derivato.
                        # (lambda -> LAM*LAM_MIN dove massimamente denso). Transizione DOLCE (tanh).
P_LAM    = 0.0          # ESPONENTE DELLA SCALA LOCALE. 0 = lambda fissa (come prima).
                        # >0: lambda_i = LAM * (scala locale / mediana)^P_LAM, poi
                        # simmetrizzata sull arco. Normalizzando sulla MEDIANA il
                        # raffinamento locale viene compensato, mentre la dilatazione
                        # GLOBALE resta sentita: le due cose non vanno confuse.
CS_M, ALPHA_M, BETA_M = 2.0, 0.05, 0.8
TAU_BG   = 5.0          # il vuoto insegue la densita' LOCALE
TAU_DIFF = 1.0          # e diffonde sulla topologia (Legge I: nessuna scorciatoia globale)
TAU_P    = 2.0
TAU_A    = _TAU_A_REGIME
TAU_LOCALI = True      # Punto 2: costanti temporali TAU_P/TAU_BG/TAU_TW come RAPPORTI adimensionali
TAU_USA_D0 = False     # tau_p locale: False=usa d (distanza reale dilatata), True=usa d0 (riposo). --tau-d0 per attivare
CALORE_VETTORIALE = True   # calcio termico: True=vettoriale+chirale DI DEFAULT (innesco precessione: omega_s 3D
                           # eccitato, phivel firmato da perc_chi). False=scalare isotropo. --calore-scal per tornare scalare
                       # rispetto a frequenze locali (invarianza per riparametrizzazione). IN VERIFICA.
                       # False = costanti fisse (comportamento precedente). Reversibile.
TAU_A_LOCALE = True     # vita media spinoriale LOCALE ~|Psi|^2 (decadimento atomico). IN VERIFICA.
                       # False = TAU_A fisso (comportamento precedente). Reversibile.
PHI_CRIT = 2 * np.pi    # QUANTO DI OLONOMIA. Un giro, non due: il sistema e'
                        # abeliano (settore U(1) varieta' invariante esatta, misurato),
                        # quindi il quanto naturale e' 2pi; il 4pi veniva dall'intuizione
                        # spinoriale, risultata assente. A 4pi la mitosi non scattava MAI
                        # e il grafo restava al 100% oltre portata; a 2pi ripara.
TAU_TW   = 20.0
def _tau_tw_locale(net):
    """TAU_TW LOCALE = 2pi/|omega_i - omega_j| (inverso della dispersione di frequenza tra nodi
    adiacenti). La torsione decade tanto piu' in fretta quanto piu' i due nodi sono fuori fase.
    kappa_tw = TAU_TW/(2pi) resta come rapporto O(1). Invariante per riparametrizzazione."""
    import numpy as _np
    i, j = net.i, net.j
    if len(net.phivel) < net.n or len(i) == 0:
        return TAU_TW
    dom = _np.abs(net.phivel[i] - net.phivel[j]) + 1e-3
    # tau_tw = kappa_tw * 2pi/|dw|, con kappa_tw = TAU_TW/(2pi) rapporto O(1)
    return _np.maximum((2*_np.pi) / dom, 1e-3)   # kappa=1: tau_tw = 2pi/|dw_locale|
KICK_TW  = 0.35

# ============================================================================
# LEGGE DELLA DENSITA' CRITICA DI COLLASSO (misurata su griglia lambda x gamma).
# ----------------------------------------------------------------------------
# La transizione da materia strutturata (gusci netti) a collasso omogeneo
# (regime tipo buco nero) avviene quando il numero di puntatori della materia
# supera una soglia critica N_c che dipende dalle costanti del sistema:
#
#       N_c(lambda, gamma) = DENS_CRIT_C * lambda^(-3) * gamma^(DENS_CRIT_B)
#
# NON e' un numero fisso: e' una RELAZIONE. Cambiando lambda o gamma, la soglia
# si aggiorna da se'. L'esponente -3 di lambda e' dimensionale (densita' critica
# di puntatori per volume di coerenza): piu' largo il kernel, meno puntatori
# servono per collassare. E' la struttura dominante, misurata (R^2 alto,
# invariante costante entro il 6% sulla griglia). L'esponente di gamma e' l'effetto
# debole ma reale della saturazione, incluso per completezza (~0.14, misurato).
# La costante C e' il numero critico a lambda=1, gamma=1.
# Fonte: griglia lambda in {0.6,0.8,1.0} x gamma in {0.02,0.035,0.05} x 2 semi.
#
# ============================================================================
# LEGGE DELLA DENSITA' CRITICA — FORMA ADATTIVA ALLE SCALE (crossover di saturazione)
# ----------------------------------------------------------------------------
# La transizione materia->collasso e' governata da una densita' critica N_c. La
# forma GEOMETRICA N_c = C*lambda^-3*gamma^b vale solo dove la saturazione e'
# trascurabile (gamma|F| << 1). La forma ADATTIVA, valida a OGNI scala, e':
#
#     N_c(lambda,gamma,s) = C * lambda^(-3) * (1 + s)^theta,   s = gamma*|F|
#
# derivata imponendo i due limiti asintotici (vedi legge_crossover.md e il capitolo
# omonimo nel documento):
#   - s -> 0 (scale piccole, simulabili):  (1+s)^theta -> 1  =>  N_c ~ C*lambda^-3
#     (recupera ESATTAMENTE la legge geometrica misurata)
#   - s -> inf (materia reale, saturata):  (1+s)^theta -> (gamma|F|)^theta
#     (emerge la dipendenza da gamma: l'inversione dei pesi prevista)
# UN solo parametro nuovo, theta, misurato ~0.14 dai picchi saturi. Notevole: theta
# coincide con l'esponente di gamma della legge geometrica (DENS_CRIT_B), il che
# conferma che quel gamma^0.14 ERA gia' l'affiorare del crossover. theta piccolo =
# crossover DOLCE: lambda resta dominante anche nel saturato, gamma cresce piano.
# Cablare la forma adattiva NON cambia nulla alle scale attuali (li (1+s)^theta~1)
# ma rende la legge corretta a ogni scala. Sempre attiva.
# Cautela: theta e' stima INDIRETTA (dai picchi); da confermare con griglia nel
# regime saturato. Fonte: griglia lambda x gamma + misura del crossover.
DENS_CRIT_C     = 484.0     # numero critico a lambda=1, gamma=1
DENS_CRIT_B     = 0.14      # esponente di gamma nella forma geometrica (= theta, non a caso)
DENS_CRIT_THETA = 0.14      # esponente del crossover (regime saturato), misurato dai picchi
CROSSOVER_K     = 1.0       # calibrazione di s in forma esplicita s~gamma*k*N/R^3 (da affinare)

def massa_critica_collasso(lam=None, gamma=None, s=None):
    """Numero critico di puntatori oltre cui la materia collassa (regime buco nero).
    Forma ADATTIVA alle scale: N_c = C * lambda^-3 * (1 + s)^theta, s = gamma|F|.
    - se s e' None (default), usa s=0: si riduce alla forma geometrica C*lambda^-3*gamma^b,
      esatta alle scale simulabili (gamma|F|<<1).
    - se s e' fornito (da stato_crossover), applica il crossover completo: la legge
      si adatta da se' al regime, geometrico o saturato.
    Valida a OGNI scala per costruzione (interpola i due regimi asintotici)."""
    lm = LAM if lam is None else lam
    ga = GAMMA if gamma is None else gamma
    # RITARATURA per la nuova fisica: con antichiralita' + torsione 3pi i gusci si
    # formano diversamente e la transizione materia->buco nero (omogeneizzazione della
    # coerenza radiale) avviene a densita' PIU' BASSA. MISURATO: la transizione passa
    # da ~622 (classico) a ~500 (nuova fisica), circa -20%. Il coefficiente C scala di
    # conseguenza: 484 -> 389. Applicato solo quando i flag della nuova fisica sono
    # attivi, cosi' la taratura classica resta invariata.
    C = DENS_CRIT_C * (389.0/484.0) if (COMPAT_CHI and TORS_4PI) else DENS_CRIT_C
    geom = C * lm**(-3.0) * ga**(DENS_CRIT_B)   # forma geometrica (limite s->0)
    if s is None or s <= 0:
        return geom
    # forma adattiva: la geometrica moltiplicata per il fattore di crossover
    # normalizzato a 1 quando s->0, cosi' le due forme COINCIDONO a piccola scala
    # e il crossover aggiunge solo la correzione del regime saturato.
    return geom * ((1.0 + s) ** DENS_CRIT_THETA)


def massa_critica_adattiva(net):
    """Densita' critica adattiva calcolata sullo stato CORRENTE della rete: misura
    s=gamma|F| dal campo reale e applica la legge di crossover. Sempre attiva: e' la
    versione che 'sa' a quale scala si trova la materia presente."""
    st = stato_crossover(net)
    return massa_critica_collasso(s=st["gF_med"])


def classifica_topologia(net, centro=None):
    """Classifica un addensamento come MATERIA o BUCO NERO dalla TOPOLOGIA della
    connettivita', non dalla sola densita' (righello vecchio superato dalla nuova fisica).
    MATERIA: nucleo cavo (torsione/dipoli nulli al centro) + guscio di legami crescente
    e diffuso verso l'esterno. BUCO NERO: torto e dipolare fino al centro + connettivita'
    concentrata in anelli piccati. Il discriminante e' il profilo radiale della densita'
    di legami: monotono crescente (materia) vs a picco concentrato (buco nero)."""
    if net.n < 20 or not len(net.i):
        return "vuoto", 0.0
    pos = net.pos[:net.n]
    if centro is None:
        # baricentro dell'interferenza (dove sta davvero la massa), non il centro nominale
        if not hasattr(net, "psi") or len(net.psi) < net.n:
            net.calcola_psi()
        I = np.abs(net.psi[:net.n]) ** 2
        c = (pos * I[:, None]).sum(0) / max(I.sum(), 1e-9)
    else:
        c = np.asarray(centro, float)
    rad = np.linalg.norm(pos - c, axis=1)
    i, j = net.i, net.j
    mask = (i < net.n) & (j < net.n)
    ii, jj = i[mask], j[mask]
    midr = 0.5 * (rad[ii] + rad[jj])
    rmax = max(float(np.quantile(rad, 0.9)), 0.5)
    bins = np.linspace(0, rmax, 6)
    dens = []
    for k in range(len(bins) - 1):
        ma = (midr >= bins[k]) & (midr < bins[k + 1])
        mn = (rad >= bins[k]) & (rad < bins[k + 1])
        dens.append(ma.sum() / max(mn.sum(), 1))
    dens = np.array(dens)
    if dens.max() < 1e-6:
        return "vuoto", 0.0
    # discriminante: quanto e' PIENO il nucleo rispetto al picco. Il buco nero ha il
    # nucleo gia' molto connesso (nucleo/picco alto, oggetto pieno); la materia ha il
    # nucleo piu' rado rispetto al mantello (nucleo/picco basso, oggetto cavo a guscio).
    riemp_nucleo = dens[0] / max(dens.max(), 1e-9)
    if riemp_nucleo < 0.5:
        return "materia", riemp_nucleo         # nucleo cavo -> mantello -> materia
    else:
        return "buco nero", riemp_nucleo       # nucleo pieno -> buco nero


def stato_crossover(net):
    """Riporta gamma*|F| nel cuore (mediano) e di picco: dice se la legge della
    densita' critica e' nel suo dominio di validita' (regime geometrico, mediano<<1)
    o se la materia sta entrando nel regime saturato (picchi o mediano oltre 1)."""
    if net.n == 0 or not len(net.i):
        return {"gF_med": 0.0, "gF_max": 0.0, "regime": "vuoto"}
    w = net._pesi(); F = net._mat(w) @ np.exp(1j * net.phi)
    Fabs = np.abs(F[:net.n])
    gF_med = GAMMA * float(np.median(Fabs))
    gF_max = GAMMA * float(Fabs.max())
    regime = "SATURO" if gF_med > 1 else ("misto" if gF_max > 1 else "geometrico")
    return {"gF_med": gF_med, "gF_max": gF_max, "regime": regime}


def _righe_stato_universo(net):
    """Descrizione del REGIME dell universo, per l evoluzione libera (lo spaziotempo che
    autogenera materia dal caos). Sostituisce la classificazione binaria COLLASSO/materia su
    net.n globale, che era SBAGLIATA: confrontava il conteggio TOTALE dei puntatori (vuoto +
    tutto) con la soglia critica di UN corpo singolo, dando collasso solo perche l universo
    aveva molti nodi in totale, non per una fisica di collasso.
    Qui si misura quanta materia coerente e emersa dal vuoto: la frazione di nodi coerenti
    dice se il sistema e ancora caotico, in formazione, o organizzato. La classificazione
    materia/buco-nero di un SINGOLO corpo (per struttura) resta affidata a classifica_topologia,
    da usare su un addensamento isolato, non sull universo intero."""
    n = net.n
    if n == 0:
        return [("universo: vuoto", 10, "#5d4037", "bold")]
    if not hasattr(net, "psi") or len(net.psi) < n:
        net.calcola_psi()
    I2 = np.abs(net.psi[:n]) ** 2
    soglia = float(np.median(I2)) + lambda_vuoto(net)
    coerenti = int(np.sum(I2 > soglia))
    frazione = coerenti / max(n, 1)
    if frazione < 0.05:
        desc, col = "caos (vuoto che ribolle)", "#e65100"
    elif frazione < 0.20:
        desc, col = "materia in formazione", "#f9a825"
    else:
        desc, col = "materia organizzata", "#2e7d32"
    return [(f"universo: {desc}  ({coerenti}/{n} coerenti)", 10, col, "bold")]


# ============================================================================
# LEGGE DELLO SCUOTIMENTO LOCALE DEL VUOTO (creazione stocastica di materia).
# ----------------------------------------------------------------------------
# Il vuoto non e' fermo: ribolle, e questo scuotimento fa nascere materia in modo
# stocastico. E' un fenomeno DISTINTO dalla creazione di coppia alla Schwinger
# (mitosi/antimitosi), che e' l'analogo di Hawking e lavora dove la curvatura e'
# ALTA (coppie dal vuoto teso). Lo scuotimento, al contrario, e' una LEGGE DI
# LOCALITA' misurata: ribolle dove NON c'e' materia (bassa coerenza) ed e' soppresso
# DENTRO la materia (alta coerenza), che cosi' resta stabile.
#
# La legge, senza parametri arbitrari, lega due grandezze GIA' misurate del sistema:
#   scuotimento(x) = sqrt(Lambda) / (1 + |Psi(x)|^2 / Lambda)
# dove:
#   - Lambda = energia del vuoto. NON e' un numero fisso: e' calcolata DINAMICAMENTE
#     dallo stato del grafo a ogni istante, come densita' di energia d'interferenza
#     del vuoto <|Psi|^2>. Cambia con la scala (misurato: cresce col sistema), quindi
#     la legge si adatta da se' a ogni scala invece di inchiodare un valore.
#   - |Psi|^2 = coerenza locale: quanto un nodo E' materia. Lo stesso Lambda che da'
#     l'ampiezza da' la scala di normalizzazione: un nodo con energia ~Lambda (vuoto)
#     ribolle a piena ampiezza, uno con energia >> Lambda (materia) e' soppresso. La
#     soppressione era prima affidata alla curvatura, proxy debole (proteggeva la
#     materia solo all'81% del vuoto): la coerenza e' il discriminante fisico giusto.
# Nessun numero scelto: ampiezza dall'energia del vuoto (dinamica), modulazione
# dalla geometria locale. Sempre attiva (flag SCUOTIMENTO, default on).
SCUOTIMENTO  = _SCUOTIMENTO_REGIME  # legge dello scuotimento (segue REGIME; True in stocastico)

def lambda_vuoto(net):
    """Energia del vuoto DINAMICA: densita' di energia d'interferenza <|Psi|^2>.
    Non un numero fisso - calcolata dallo stato corrente, si adatta a ogni scala.
    E' l'analogo della costante cosmologica, ma qui e' una grandezza del sistema."""
    if net.n == 0:
        return 0.0
    if not hasattr(net, "psi") or len(net.psi) < net.n:
        net.calcola_psi()
    return float(np.mean(np.abs(net.psi[:net.n])**2))

def scuoti_vuoto(net):
    """Applica la legge dello scuotimento locale del vuoto: inietta agitazione di fase.
    Ampiezza sqrt(Lambda) con Lambda calcolato DINAMICAMENTE dallo stato (energia del vuoto),
    soppressa dalla COERENZA locale |Psi|^2 (non piu' dalla curvatura): il vuoto ribolle dove
    non c'e' materia, la materia (coerenza alta) e' protetta. Genera materia stocasticamente
    dal caos e non la riassorbe. Sempre attiva."""
    if not SCUOTIMENTO or net.n == 0:
        return
    Lam = lambda_vuoto(net)                        # energia del vuoto, dinamica
    if Lam <= 0:
        return
    # SOPPRESSIONE PER COERENZA (non piu' per curvatura). Il vuoto deve ribollire dove NON c'e'
    # materia, ed essere soppresso DENTRO la materia. Il discriminante giusto e' la coerenza
    # locale |Psi|^2 (quanto un nodo E' materia), non la curvatura della metrica: misurato, la
    # curvatura proteggeva la materia solo all'81% del vuoto (protezione debole), e le masse si
    # decoerivano (~70% in 60 passi). La coerenza le protegge (~47% persa) senza spegnere la
    # creazione dal vuoto. Forma NON-PARAMETRICA: lo stesso Lambda che da' l'ampiezza da' la
    # scala di normalizzazione. Un nodo con energia ~Lambda (vuoto) ribolle a piena ampiezza;
    # un nodo con energia >> Lambda (materia) e' fortemente soppresso. Nessun coefficiente libero.
    if not hasattr(net, "psi") or len(net.psi) < net.n:
        net.calcola_psi()
    I2 = np.abs(net.psi[:net.n]) ** 2
    ampiezza = np.sqrt(Lam) / (1.0 + I2 / Lam)     # sqrt(Lam)/(1 + |Psi|^2/Lam): legge pura
    net.phivel[:net.n] += net.rng.normal(0, 1.0, net.n) * ampiezza
    # Nota: l'eccitazione del vuoto sul settore spinoriale (se attivo) e' integrata dentro
    # _passo_spinoriale (parte del ciclo di evoluzione in step), non qui.
# ============================================================================
MU_PSI   = -0.05
REPULS_LEGGE = True      # repulsione EMERGENTE con conversione dinamica (riempimento*coerenza vs Ncrit adattivo): legge, non parametro        # AUTO-INTERAZIONE repulsiva ATTIVA (default B): pressione
                        # interna dall'Hamiltoniana. Espande R90 conservando l'olonomia.          # AUTO-INTERAZIONE DELL'INTERFERENZA (opzione, spenta).
                        # <0 = repulsiva (pressione interna), derivata da d|Psi|^2/dphi.
                        # NON e' una forza scelta: e' il gradiente di |Psi|^2, l'unica
                        # forma coerente. Candidata alla faccia repulsiva del modello.
L_CONSERVA = False      # ERRATA, NON usare (default OFF). Doveva rimuovere la rotazione spuria del
                        # rilassamento, ma AZZERA tutta la rotazione rigida ad ogni passo -> distrugge
                        # la PRECESSIONE FISICA REALE del sistema (momento angolare netto misurato
                        # L_z~-0.9, verso coerente all'84%). Conservare L != annullare la rotazione.
                        # La fisica fondamentale (fasi/mitosi/moto) conserva gia' L da sola. Vedi doc.
ANTIFASE_ADD = False    # LEGGE DI STABILITA' (esplorativa): i nuovi nodi in regione sovra-densa
                        # nascono in ANTIFASE con prob tanh((rho-rho_eq)/rho_c), rho_c da N_critico.
                        # Annichila le AGGIUNTE (non la materia esistente) -> il grumo si stabilizza.
COPPIA_DENSITA = False  # ESPLORATIVO: lega la creazione di coppia anche all anomalia di densita'
                        # (oltre alla torsione), per il feedback anti-accrescimento. Da validare.
COPPIA_MIT = 1.0        # CREAZIONE DI COPPIA alla Schwinger ATTIVA (default B):
                        # antiparticelle nate oltre la torsione critica.        # EMISSIONE DI COPPIA alla mitosi (opzione, spenta di default).
                        # >0: frazione di eventi in cui, oltre al nodo corretto (fase fm,
                        # in serie, che conserva l'olonomia del ciclo), nasce un ANTI-NODO
                        # a fase fm+pi collegato agli stessi genitori. La coppia ha media
                        # di fase fm: l'olonomia GLOBALE e' conservata, ma si creano due
                        # difetti opposti (analogia con la creazione di coppia). Ipotesi:
                        # nodo e anti-nodo si respingono (antifase), generando volume, e
                        # possono annichilare con materia coerente vicina. Da MISURARE:
                        # olonomia, separazione della coppia, effetto sulla densita'.
PLAST_MIT = 0.0         # SPINTA VOLUMETRICA ALLA MITOSI (opzione, spenta di default).
                        # >0: alla nascita di un nodo la lunghezza di riposo d0 dei due
                        # nuovi archi riceve un offset plastico permanente proporzionale
                        # alla torsione sciolta, invece di essere solo meta' dell'arco.
                        # Ipotesi: la suddivisione GENERA spazio invece di comprimerlo.
                        # Il punto medio corretto per la fase (fm) NON e' toccato:
                        # l'olonomia di ciclo resta invariante. Osservabili di controllo:
                        # esponente di scala R(M), conservazione olonomia, sopravvivenza
                        # del collasso oltre la massa critica. Da MISURARE, non imporre.
QMIN_M   = 0.000
MITMAX   = 0            # NESSUN tetto di default: un massimo di falsa fisica falsifica le metriche
KERNEL_ALPHA = 1.0      # KERNEL BILANCIATO DAL TEMPO PROPRIO (tau^alpha) SEMPRE ATTIVO.
                        # alpha=1: il kernel e' pesato LINEARMENTE dal tempo proprio locale
                        # tau=1+|torsione|/PHI_CRIT, senza esponente arbitrario. Il kernel si
                        # rafforza dove il tempo proprio rallenta (nella materia): meccanismo
                        # con cui la materia pesa i legami secondo il tempo proprio (principio
                        # di equivalenza). alpha=0 lo spegne.
COMPAT_CHI = False      # REGOLA DI COMPATIBILITA' DIPOLARE delle antichiralita': se True,
                        # i solitoni si legano SOLO fra chiralita' opposte (filtro assoluto -> tutti
                        # i legami fra opposti, f=1, twist=pi). Ora FALSE di default: col settore
                        # spinoriale attivo servono i legami sia fra opposti sia fra uguali, per i
                        # due generatori SU(2) non commutanti (vera non-abelianita', verificata).
TORS_4PI = True         # TORSIONE A DOPPIA COPERTURA (4pi): se True, la torsione vive sul
                        # dominio doppio [-4pi,4pi] includendo i profili di percorrenza dei
                        # legami dipolari, e la soglia di mitosi diventa 4pi. Prova
                        # sperimentale, default off: non tocca la torsione classica.
MITOSI_DIR = 0.5        # MITOSI DIREZIONALE ATTIVA: il figlio nasce spostato in fase verso il
                        # figlio nasce decentrato verso il gradiente di torsione (frazione
                        # della semi-lunghezza dell'arco). Polarizza la replicazione e fa
                        # traslare il baricentro lungo la geodetica. Sperimentale.
MEM_HEBB  = True        # MEMORIA HEBBIANA DEL MOTO ATTIVA (inerzia plastica). Quando attiva,
                        # l'inerzia e la plasticita' NON sono parametri: derivano dallo stato.
                        # Inerzia = |Psi|^2 del nodo (la massa e' l'inerzia). Plasticita' =
                        # gradiente di torsione locale (la geodetica corregge dove curva).
                        # Il momento si conserva e viene piegato dal campo: legge, non numeri.
                        # le metriche (nasconde la valanga di mitosi, gonfia la torsione).
                        # Attivabile a 60 col pulsante LIMITE o --mitmax N solo come
                        # guardia di MEMORIA quando serve, mai come default.
                        # milioni di nodi (collasso), da studiare in modo dedicato
# MOTO LUNGO LE FRANGE (geodetiche del flusso di fase). Off di default (K_FRANGE=0).
# Ipotesi: il moto vero non e' cadere lungo il gradiente radiale del pozzo, ma SCORRERE
# lungo le frange d'interferenza rotanti (i bordi dei solchi = le geodetiche). Le frange
# hanno un flusso di fase rotazionale netto (misurato ~0.94), quindi il moto lungo di esse
# e' tangenziale e produce orbita e precessione. Il feedback spinge ogni solitone lungo il
# gradiente di fase locale (grad theta pesato da |Psi|^2), la direzione delle frange.
K_FRANGE = 0.0
VIRIALE  = False        # CONVERSIONE VIRIALE (legge): ripartisce la spinta radiale fra
# TERMINE DI HALL / FRAME-DRAGGING come LEGGE, ATTIVO di default. Interruttore on/off (non un
# coefficiente): la forza NON e' tarata, e' il twist locale medio normalizzato da PHI_CRIT
# (grandezza di stato), coefficiente 1. Il twist, da diagnostica passiva, diventa forza: la
# ROTAZIONE TRA GUSCI, dove il twist di un guscio devia la fase del guscio vicino (analogo di
# v x B / Lense-Thirring). E' la componente non conservativa verso la precessione. Verificata
# sana su piu' semi (osservabili di controllo intatte); la precessione orbitale piena attende
# ancora il canale di moto posizionale, ma la legge e' fisica del sistema e resta attiva.
FRAME_DRAG = True
PASSI_PER_FRAME = 6      # passi di motore per frame nell'interattivo: rende visibile l'evoluzione
GRAV_BIFASE = True       # LEGGE gravitazionale bifase unica (sciolta-1, direzione intrinseca,
                         # spinore accoppiato, tetto causale). Attiva di default.
# SETTORE SPINORIALE a 4pi (ATTIVO di default). Ogni nodo porta una SECONDA componente di
# fase che, accoppiata alle antichiralita' (perc_chi, i +-pi gia' nel sistema), trasforma
# come uno spinore sotto 4pi (doppia copertura). Quando SPENTO (SPINORE=False) il sistema e'
# IDENTICO all'U(1) scalare (non-regressione garantita per costruzione).
# NB (aggiornato): l'ACCOPPIAMENTO NON-ABELIANO SU(2) NON e' piu' "da attivare" - E' IMPLEMENTATO
# E ATTIVO. Il metodo _passo_spinoriale (Passo 2+3) e' chiamato a ogni step (sotto if SPINORE):
# i legami fra chiralita' OPPOSTE ruotano il Bloch attorno a sigma_z, quelli fra UGUALI attorno
# a sigma_x; sigma_z e sigma_x NON commutano -> struttura SU(2) genuina, non-abelianita'
# verificata (commutatore dei generatori != 0). Il motore e' conservativo hebbiano (memoria
# omega_s), non un rilassamento. Quindi le simulazioni girano con SU(2) non-abeliana viva.
SPINORE = True          # SETTORE SPINORIALE a 4pi ATTIVO DI DEFAULT. Implementato, FUNZIONANTE
                        # e VALIDATO (motore conservativo hebbiano: lo spinore si accende col
                        # vuoto e resta vivo, all'equatore, senza disturbare l'U(1); non-abelianita'
                        # genuina verificata, commutatore dei generatori != 0). Attivo ovunque come
                        # legge valida del sistema. Richiede COMPAT_CHI=False per i due generatori
                        # SU(2) (impostato di conseguenza). Il costo raddoppia gli archi (e' la
                        # non-abelianita' stessa, non spreco: verificato), ma e' una legge del sistema.
# SEME_INIZIALE: numero di puntatori da cui il sistema PARTE. Non e' piu' una densita'
# del vuoto imposta (BOX+N_VUOTO fissavano insieme una densita' fisica nascosta) - e'
# solo il seme da cui la dinamica evolve, sparpagliato sulla scala del sistema (~lambda).
# STRADA B (futura): eliminare anche questo, con un feedback che porti il vuoto alla sua
# densita' di equilibrio EMERGENTE. Oggi la densita' del vuoto non ha un attrattore
# pulito (misurato: dipende dal seme), quindi il seme iniziale resta, ma onesto: e' un
# punto di partenza, non una densita' target.
SEME_INIZIALE = 900
MAX_NODI = 4000000      # GUARDIA DI MEMORIA, non di fisica: non limita la dinamica,
                        # impedisce solo l'esaurimento della RAM. Va tenuta cosi' alta
                        # da non essere mai raggiunta nelle corse reali; se lo fosse,
                        # la misura e' da rifare con piu' memoria, non da troncare.
EMB_IT   = 3
EMB_ETA  = 0.12


class Rete:
    def __init__(self, seed=42):
        self.rng = np.random.default_rng(seed)
        self.pos = np.zeros((0, 3)); self.phi = np.zeros(0); self.phi0 = np.zeros(0)
        self.phivel = np.zeros(0); self.eta = np.zeros(0)
        self.phi_s = np.zeros(0)             # COMPONENTE SPINORIALE (settore 4pi). Inerte se
                                             # SPINORE=False. Parallela a phi, gestita ovunque phi cambi.
        self.omega_s = np.zeros((0, 3))      # MEMORIA HEBBIANA del momento angolare spinoriale
                                             # (motore conservativo: si conserva, non rilassa).
        # PROFILO DI PERCORRENZA (struttura a nastro delle specifiche originali).
        # Ogni solitone e' una sinusoide che, percorsa lungo il suo profilo, esegue
        # un salto NETTO di 180 gradi (pi) nel punto d'incrocio con l'asse al mediano.
        # Il verso di percorrenza (+1/-1) da' le due ANTICHIRALITA': percorrere l'onda
        # in un verso torce di +pi, nell'altro di -pi. 'perc_chi' e' il verso; 'perc_tw'
        # e' lo stato del mezzo-twist (0 = prima del mediano, pi = dopo il salto).
        # Introdotto DORMIENTE: non accoppiato ancora a Psi ne' alla dinamica, finche'
        # non e' verificato che la struttura non rompe le leggi esistenti.
        self.perc_chi = np.zeros(0, int)     # verso di percorrenza / antichiralita' (+1/-1)
        self.perc_tw  = np.zeros(0)          # stato del salto di pi al mediano (0 o pi)
        self.i = np.zeros(0, int); self.j = np.zeros(0, int)
        self.d = np.zeros(0); self.d0 = np.zeros(0); self.vd = np.zeros(0)
        self.peq = np.zeros(0); self.tw = np.zeros(0); self.twp = np.zeros(0)
        # MEMORIA HEBBIANA DEL MOTO (inerzia plastica). Per ogni nodo, un vettore che
        # ricorda la direzione di moto del baricentro d'interferenza locale. Si rinforza
        # percorrendola (hebbiano: la via percorsa si consolida) e decade se non usata.
        # Non e' una rotaia rigida: la sua PLASTICITA' lascia che le microvariazioni di
        # spinta della mitosi asimmetrica la riorientino ad ogni passo, cosi' il moto
        # segue la geodetica curva invece di andare dritto. mem_mot = direzione*intensita'.
        self.mem_mot = np.zeros((0, 3))       # memoria hebbiana del moto per nodo
        self._psi_bar_prec = None             # baricentro locale al passo precedente
        self.nati = 0; self.negate = 0; self.coppie_nate = 0
        self.ultima_prob_coppia = 0.0
        self.psi = np.zeros(0, complex); self._deg = np.zeros(0)
        self._S = None; self._perm = None; self._psi_prec = None
        # ---- TRACKING DI CONCORRENZA ALLE MASSE ----
        # Ogni massa creata riceve un ID univoco. conc_nodi[k] = lista di [id_massa, peso_nascita,
        # peso_corrente]: quanto il solitone k CONCORRE (contributo al campo di interferenza) a
        # ciascuna massa a cui partecipa. Un solitone puo' concorrere a piu' masse. Il peso e' il
        # contributo fisico |Psi| / |A_ij e^{i phi}| (guarda la luna: contributo all'interferenza,
        # non appartenenza). conc_archi[e] = idem per l'arco.
        self.xi_termo = 0.0   # TERMOSTATO NOSE-HOOVER: attrito adattivo. Sale se l'energia e' sopra
                              # il target (frena), diventa NEGATIVO se sotto (RIFORNISCE). Rende il
                              # regime deterministico auto-sostenuto invece che in esaurimento.
        self._next_mass_id = 0
        self.conc_nodi = []
        self.conc_archi = []
        self.masse_info = {}

    @property
    def n(self): return len(self.phi)

    def _grado(self):
        self._deg = np.maximum(np.bincount(self.i, minlength=self.n) +
                               np.bincount(self.j, minlength=self.n), 1)
        self._costruisci_struttura()

    def _costruisci_struttura(self):
        """struttura CSR simmetrica in cache: la topologia cambia solo alla
        nascita di puntatori o per mitosi, i pesi cambiano a ogni passo."""
        if not len(self.i): self._S = None; return
        ii = np.concatenate([self.i, self.j]); jj = np.concatenate([self.j, self.i])
        S = sparse.coo_matrix((np.arange(len(ii), dtype=float), (ii, jj)),
                              shape=(self.n, self.n)).tocsr()
        self._perm = S.data.astype(np.int64)      # posizione CSR -> indice originale
        S.data = np.zeros(len(ii))
        self._S = S

    def semina(self, n, raggio=None, centro=(0, 0, 0), fase=None, mass_id=None):
        n = max(0, min(n, MAX_NODI - self.n))
        if n == 0: return
        r = _scala_sistema() * 0.5 if raggio is None else raggio
        u = self.rng.normal(size=(n, 3)); u /= np.linalg.norm(u, axis=1, keepdims=True)
        p = np.asarray(centro, float) + u * (r * self.rng.random(n) ** (1 / 3))[:, None]
        if fase is None:
            ph = self.rng.random(n) * 4 * np.pi
        else:
            ph = float(fase) + self.rng.normal(0, 0.05, n)
        base = self.n
        self.pos = np.vstack([self.pos, p])
        self.phi = np.concatenate([self.phi, ph % (4 * np.pi)])
        self.phi0 = np.concatenate([self.phi0, ph % (4 * np.pi)])
        self.phi_s = np.concatenate([self.phi_s, np.zeros(n)])   # spinore: nasce a 0 (inerte se spento)
        # profilo di percorrenza: verso casuale (+1/-1) = le due antichiralita', ~50/50.
        # (assegnato PRIMA di phivel perche' il calcio chirale lo usa)
        chi_nuovi = self.rng.choice([-1, 1], n)
        # impulso iniziale di fase: zero in regime stocastico (canonico), calcio termico di punto
        # zero in regime deterministico (_CALORE_INIT), sostituto del vuoto come energia iniziale.
        if _CALORE_INIT > 0:
            if CALORE_VETTORIALE:
                # CALCIO CHIRALE: la fluttuazione di fase e' FIRMATA dalla chiralita' del solitone.
                # Non si media a zero come il rumore isotropo: crea chiralita' netta locale che
                # frame-drag e mem_mot possono agganciare e trasformare in rotazione orbitale.
                calcio_phi = chi_nuovi * self.rng.normal(_CALORE_INIT, _CALORE_INIT * 0.5, n)
            else:
                calcio_phi = self.rng.normal(0, _CALORE_INIT, n)   # scalare isotropo (canonico)
            self.phivel = np.concatenate([self.phivel, calcio_phi])
        else:
            self.phivel = np.concatenate([self.phivel, np.zeros(n)])
        self.eta = np.concatenate([self.eta, np.zeros(n)])
        self.perc_chi = np.concatenate([self.perc_chi, chi_nuovi])
        self.perc_tw = np.concatenate([self.perc_tw, np.zeros(n)])
        self.mem_mot = np.vstack([self.mem_mot, np.zeros((n, 3))]) if len(self.mem_mot) else np.zeros((n, 3))
        # CALCIO al MOMENTO ANGOLARE SPINORIALE: invece di omega_s=(0,0,0), il punto zero eccita il
        # vettore di rotazione di Bloch, rompendo la degenerazione meridiana (1D -> precessione 3D).
        if CALORE_VETTORIALE and _CALORE_INIT > 0:
            calcio_omega = self.rng.normal(0, _CALORE_INIT, (n, 3))
            self.omega_s = np.vstack([self.omega_s, calcio_omega]) if len(self.omega_s) else calcio_omega
        self.conc_nodi.extend([[] for _ in range(n)])   # TRACKING: liste vuote per i nuovi nodi
        self._allaccia(base)
        if mass_id is not None:
            self.masse_info[mass_id] = dict(centro=tuple(np.asarray(centro, float)),
                                            fase=(None if fase is None else float(fase)),
                                            passo_nascita=getattr(self, "_passo_corrente", 0),
                                            n_nodi_nascita=n)
            self._registra_concorrenza(np.arange(base, self.n), mass_id, centro)

    def nuova_massa(self, n, raggio=None, centro=(0, 0, 0), fase=None):
        """Semina una massa NUOVA con ID univoco di tracking; registra la concorrenza (peso fisico
        dal campo di interferenza) dei solitoni/archi che la creano. Restituisce l'id."""
        mid = self._next_mass_id; self._next_mass_id += 1
        self.semina(n, raggio=raggio, centro=centro, fase=fase, mass_id=mid)
        return mid

    def _registra_concorrenza(self, idx_nodi, mass_id, centro):
        """Registra che idx_nodi (e gli archi fra loro) CONCORRONO a mass_id, peso = contributo al
        campo di interferenza. peso_nascita = peso_corrente all'inizio."""
        idx_nodi = np.asarray(idx_nodi, int)
        if len(idx_nodi) == 0: return
        self.calcola_psi()
        for k in idx_nodi:
            w = float(np.abs(self.psi[k])) if k < len(self.psi) else 0.0
            self._agg_voce(self.conc_nodi, int(k), mass_id, w)
        sel_set = set(idx_nodi.tolist())
        for e in range(len(self.i)):
            if int(self.i[e]) in sel_set and int(self.j[e]) in sel_set:
                wa = float(np.abs(np.exp(1j*self.phi[self.i[e]]) + np.exp(1j*self.phi[self.j[e]]))) / 2.0
                self._agg_voce(self.conc_archi, e, mass_id, wa)

    @staticmethod
    def _agg_voce(lista, idx, mass_id, peso):
        """aggiunge/aggiorna la voce [id, w_nascita, w_corrente] per l'elemento idx."""
        while len(lista) <= idx:
            lista.append([])
        for voce in lista[idx]:
            if voce[0] == mass_id:
                voce[2] = peso; return
        lista[idx].append([mass_id, peso, peso])

    def _riallinea_tracking(self):
        """Auto-riparazione: porta conc_nodi e conc_archi alla dimensione corrente di nodi e archi.
        I nodi/archi senza voce esplicita restano con lista vuota (non concorrono a nessuna massa).
        Rende il tracking ROBUSTO a qualsiasi operazione topologica (mitosi, Schwinger, allaccio)
        senza dover patchare ogni singolo punto che crea nodi/archi."""
        while len(self.conc_nodi) < self.n: self.conc_nodi.append([])
        if len(self.conc_nodi) > self.n: del self.conc_nodi[self.n:]
        na = len(self.i)
        while len(self.conc_archi) < na: self.conc_archi.append([])
        if len(self.conc_archi) > na: del self.conc_archi[na:]

    def aggiorna_pesi_concorrenza(self):
        """Ricalcola il PESO CORRENTE di concorrenza di ogni nodo/arco alle masse, dal campo di
        interferenza attuale (il contributo cambia mentre le fasi evolvono). Il peso di nascita
        resta fisso. Chiamabile a ogni passo o ogni N passi per il tracking dinamico."""
        self._riallinea_tracking()
        if not self.conc_nodi: return
        self.calcola_psi()
        # PROIEZIONE REALE: il peso del nodo e' la sua COERENZA di fase con la sua massa.
        # cos(phi_nodo - phi_massa): +1 in fase (nucleo, proietta pieno), -1 in antifase (guscio,
        # proietta contro). Cosi' rho*peso = contributo reale del nodo alla massa, aggiornato ogni volta.
        acc = {}
        for k in range(min(len(self.conc_nodi), self.n)):
            for voce in self.conc_nodi[k]:
                mid = voce[0]
                a = np.abs(self.psi[k]) if k < len(self.psi) else 0.0
                acc[mid] = acc.get(mid, 0.0+0.0j) + a*np.exp(1j*self.phi[k])
        fase_massa = {mid:(np.angle(z) if abs(z)>1e-9 else 0.0) for mid,z in acc.items()}
        for k in range(min(len(self.conc_nodi), self.n)):
            if not self.conc_nodi[k]: continue
            for voce in self.conc_nodi[k]:
                phim = fase_massa.get(voce[0], 0.0)
                voce[2] = float(np.cos(self.phi[k] - phim))   # coerenza con la massa = proiezione reale
        for e in range(min(len(self.conc_archi), len(self.i))):
            if not self.conc_archi[e]: continue
            wa = float(np.abs(np.exp(1j*self.phi[self.i[e]]) + np.exp(1j*self.phi[self.j[e]]))) / 2.0
            for voce in self.conc_archi[e]: voce[2] = wa

    def tracking_masse(self):
        """Stato del tracking: per ogni massa, nodi e archi concorrenti con pesi di nascita e
        correnti, piu' il peso totale (massa integrata come somma dei contributi)."""
        self._riallinea_tracking()
        out = {}
        for mid, info in self.masse_info.items():
            out[mid] = dict(info=info, nodi=[], archi=[], peso_tot_nascita=0.0, peso_tot_corrente=0.0)
        for k in range(min(len(self.conc_nodi), self.n)):
            for voce in self.conc_nodi[k]:
                mid, wn, wc = voce[0], voce[1], voce[2]   # voce puo' avere 4 campi (schwinger)
                if mid in out:
                    out[mid]["nodi"].append((k, wn, wc))
                    out[mid]["peso_tot_nascita"] += wn; out[mid]["peso_tot_corrente"] += wc
        for e in range(min(len(self.conc_archi), len(self.i))):
            for voce in self.conc_archi[e]:
                mid, wn, wc = voce[0], voce[1], voce[2]   # voce puo' avere 4 campi
                if mid in out: out[mid]["archi"].append((e, wn, wc))
        return out

    def _allaccia(self, base):
        if base >= self.n: return
        T = cKDTree(self.pos); Tn = cKDTree(self.pos[base:])
        rc = R_CONN() if P_LAM == 0.0 or not len(self.i) else \
             3.0 * float(np.median(self.lambda_nodi()))   # i neonati non hanno vicinato
        M = Tn.sparse_distance_matrix(T, rc, output_type="coo_matrix")
        a = M.row + base; b = M.col; dd = M.data
        keep = (b < base) | (a < b)
        a, b, dd = a[keep], b[keep], np.maximum(dd[keep], 1e-6)
        # REGOLA DI COMPATIBILITA' DIPOLARE (le antichiralita' si comportano come
        # bipoli: poli opposti si legano, uguali si respingono). Un solitone si connette
        # a un altro SOLO se le loro chiralita' di percorrenza sono OPPOSTE (+1 con -1).
        # Due mezzi-twist di pi opposti si completano in un giro chiuso. Attiva col flag
        # COMPAT_CHI (default off, per non alterare i risultati esistenti finche' non
        # e' verificata). Versione assoluta come primo passo: legami fra uguali proibiti.
        if COMPAT_CHI and len(a) and len(self.perc_chi) >= self.n:
            opposti = self.perc_chi[a] != self.perc_chi[b]
            a, b, dd = a[opposti], b[opposti], dd[opposti]
        if not len(a): self._grado(); return
        self.i = np.concatenate([self.i, a]); self.j = np.concatenate([self.j, b])
        self.d = np.concatenate([self.d, dd]); self.d0 = np.concatenate([self.d0, dd])
        self.vd = np.concatenate([self.vd, np.zeros(len(dd))])
        self.peq = np.concatenate([self.peq, np.full(len(dd), np.nan)])  # da calibrare
        self.tw = np.concatenate([self.tw, np.zeros(len(dd))])
        self.twp = np.concatenate([self.twp, np.zeros(len(dd))])
        self._grado()

    def lambda_nodi(self):
        """scala d'interazione LOCALE per nodo (SCHERMATURA dell'interferenza).
        Con SCHERMATURA=False e' la costante LAM (comportamento storico).
        Con SCHERMATURA=True la portata dell'interferenza si ACCORCIA dolcemente dove la densita'
        d'interferenza supera la densita' CRITICA: una massa densa si scherma dalla propria
        interferenza collettiva, smette di alimentarsi, si stabilizza. TUTTO DERIVATO DALLO STATO,
        nessun parametro libero:
          - la SCALA della transizione e' la densita' critica rho_c, ancorata a N_critico
            (massa_critica_collasso), non una mediana generica;
          - la PROFONDITA' emerge dal rapporto rho/rho_c stesso: dove rho >> rho_c la portata
            tende a LAM*(rho_c/rho) (schermatura tanto piu' forte quanto piu' si e' sopra soglia),
            dove rho << rho_c resta LAM (interferenza piena). Nessun LAM_MIN scelto.
          - transizione DOLCE (no muro secco), coerente col principio costruttivo del sistema.
        Interpretazione: schermatura PARZIALE (rho di poco sopra rho_c) = materia stabile;
        schermatura che tende a isolare del tutto (rho >> rho_c) = nucleo/orizzonte = buco nero.
        Cosi' il vincolo dei buchi neri e' rispettato: il collasso resta possibile come limite."""
        if (not SCHERMATURA) or (not len(self.i)):
            return np.full(self.n, LAM)
        # densita' d'interferenza per nodo (|Psi|^2). Uso il psi GIA' calcolato (dello step
        # precedente) per evitare ricorsione (calcola_psi -> _pesi -> _lam_archi -> lambda_nodi).
        # Se non disponibile ancora, nessuna schermatura questo giro (parte al giro dopo).
        if not hasattr(self, "psi") or len(self.psi) < self.n:
            return np.full(self.n, LAM)
        rho = np.abs(self.psi[:self.n])**2
        # densita' critica rho_c ancorata a N_critico: la densita' media che un grumo di massa
        # N_critico avrebbe. Derivata dallo stato: massa critica / volume tipico del nucleo.
        Ncrit = massa_critica_collasso()
        # volume di riferimento: quello entro il raggio di correlazione LAM (scala nativa),
        # cosi' rho_c e' una densita' d'interferenza critica, non un numero imposto.
        rho_c = Ncrit / max((4.0/3.0) * np.pi * (LAM**3), 1e-9)
        # rapporto sopra/sotto soglia, schermatura dolce: fattore in (0,1], = 1 sotto soglia,
        # decresce dolcemente come rho_c/rho sopra soglia. Uso una transizione morbida:
        #   f = 1 / (1 + softplus((rho/rho_c) - 1))   -> 1 se rho<rho_c, ~rho_c/rho se rho>>rho_c
        u = rho / rho_c
        softplus = np.log1p(np.exp(np.clip(u - 1.0, -30, 30)))   # dolce, >=0, ~0 sotto soglia
        fattore = 1.0 / (1.0 + softplus)
        return LAM * fattore

    def _lam_archi(self):
        """SIMMETRIZZATA: w_ij deve valere quanto w_ji, altrimenti la matrice
        di accoppiamento perde la simmetria su cui poggiano memoria hebbiana
        e costruzione del campo."""
        if (not SCHERMATURA) and P_LAM == 0.0: return LAM
        li = self.lambda_nodi()
        return np.maximum(0.5 * (li[self.i] + li[self.j]), 1e-6)

    def ritmo(self):
        """Ritmo del TEMPO PROPRIO locale, derivato dalla frequenza d'interferenza.
        Privo di clipping artificiali: dilatazione e compressione del tempo proprio emergono da una
        risposta analitica continua e liscia (bottleneck x/sqrt(1+x^2)), ancorata alla mediana
        globale come gauge. Vicino a x=1 la risposta e' ~lineare; per x->inf satura sub-linearmente;
        per x->0 decade dolcemente verso un pavimento infinitesimo, senza discontinuita'. Nessun
        parametro libero: la scala e' dettata dalla transizione analitica."""
        if TAU_LOC == 0.0: return None
        if self._psi_prec is None or len(self._psi_prec) != self.n:
            self._psi_prec = self.psi.copy() if len(self.psi) == self.n else np.ones(self.n, complex)
            return np.ones(self.n)
        a = np.angle(self.psi) - np.angle(self._psi_prec)
        f = np.abs((a + np.pi) % (2 * np.pi) - np.pi) / DT
        med = max(float(np.median(f)), 1e-9)
        x = f / med
        r = x / np.sqrt(1.0 + x**2) + 1.0e-6           # bottleneck liscio, satura a 1 per x->inf
        r_unit = 1.0 / np.sqrt(2.0) + 1.0e-6           # valore al gauge x=1
        r_normalized = r / r_unit                       # x=1 -> fattore unitario
        return 1.0 + TAU_LOC * (r_normalized - 1.0)

    def _passo_spinoriale(self, i, j, w, dt_n):
        """PASSO 2+3: settore spinoriale non-abeliano con MOTORE CONSERVATIVO hebbiano.
        Ogni nodo e' uno spinore, rappresentato dal vettore di Bloch n_i(phi, phi_s). Il campo
        effettivo B_i viene dai vicini, con rotazione SU(2) il cui asse dipende dalla chiralita'
        del legame (opposti -> sigma_z, uguali -> sigma_x; non commutano -> SU(2) genuino).
        La dinamica NON e' un rilassamento (che collasserebbe lo spinore al polo) ma una
        PRECESSIONE CONSERVATIVA sostenuta dalla MEMORIA HEBBIANA del momento angolare omega_s,
        con la stessa struttura di mem_mot: omega si CONSERVA (non insegue lo zero), corretto
        dal campo (torsione B x n = la geodetica che piega il moto), con INERZIA = |Psi|^2 (la
        materia mantiene il moto) e decadimento hebbiano che stabilizza. Il rumore del vuoto
        eccita lo spinore fuori dal polo; la memoria mantiene la rotazione invece di spegnerla.
        Aggiornamento simultaneo (vettorizzato): la conservazione viene dalla memoria, non
        dall'ordine di aggiornamento, dunque non serve il sequenziale lento. Causale: il campo
        dai vicini usa lo stato RITARDATO (Bloch del passo precedente)."""
        n = self.n
        # estendo omega_s e _nb ai nuovi nodi (nati da mitosi) PRESERVANDO lo stato esistente,
        # invece di reinizializzare tutto (che azzererebbe la memoria accumulata a ogni nascita).
        if len(self.omega_s) < n:
            self.omega_s = np.vstack([self.omega_s, np.zeros((n - len(self.omega_s), 3))])
        elif len(self.omega_s) > n:
            self.omega_s = self.omega_s[:n]
        if not hasattr(self, "_nb") or self._nb is None:
            b0 = self.phi_s if len(self.phi_s) == n else np.zeros(n)
            self._nb = np.stack([np.sin(b0), np.zeros(n), np.cos(b0)], axis=1)
        elif len(self._nb) < n:
            k = n - len(self._nb)
            nuovi = np.tile([0.0, 0.0, 1.0], (k, 1))     # nuovi nodi al polo
            self._nb = np.vstack([self._nb, nuovi])
        elif len(self._nb) > n:
            self._nb = self._nb[:n]
        # ECCITAZIONE DEL VUOTO sullo spinore, integrata nel passo (cosi' e' parte del ciclo di
        # evoluzione fisica, non dipende dal loop di disegno). Il rumore del vuoto perturba il
        # Bloch spingendolo fuori dal polo; la memoria hebbiana poi mantiene la rotazione.
        # STESSA legge dello scuotimento scalare: soppressione per COERENZA |Psi|^2, non per
        # curvatura (le due leggi devono essere identiche - il vuoto e' lo stesso vuoto).
        if SCUOTIMENTO:
            Lam = lambda_vuoto(self)
            if Lam > 0:
                if not hasattr(self, "psi") or len(self.psi) < n:
                    self.calcola_psi()
                I2 = np.abs(self.psi[:n]) ** 2
                amp = np.sqrt(Lam) / (1.0 + I2 / Lam)   # sqrt(Lam)/(1+|Psi|^2/Lam): come lo scalare
                self._nb = self._nb + self.rng.normal(0, 1.0, (n, 3)) * amp[:, None]
                self._nb = self._nb / np.maximum(np.linalg.norm(self._nb, axis=1, keepdims=True), 1e-9)
        nb = self._nb
        # CAUSALITA': campo dai vicini allo stato RITARDATO (Bloch del passo precedente)
        if not hasattr(self, "_nb_prec") or self._nb_prec is None or len(self._nb_prec) != n:
            nb_vic = nb
        else:
            nb_vic = self._nb_prec
        # campo effettivo B_i = somma dei vicini, con segno SU(2) dalla chiralita' del legame.
        # Il segno chirale (opposti/uguali) da' i due generatori non commutanti.
        chi = (self.perc_chi[i] * self.perc_chi[j]).astype(float)  # +1 uguali / -1 opposti
        B = np.zeros((n, 3)); deg = np.zeros(n)
        mask = (i < n) & (j < n)
        ii, jj, wl, cl = i[mask], j[mask], w[mask], chi[mask]
        # i legami opposti contribuiscono col vicino, gli uguali col vicino "riflesso" (asse diverso)
        contrib_j = nb_vic[jj] * wl[:, None]
        contrib_i = nb_vic[ii] * wl[:, None]
        # riflessione per i legami fra uguali (asse sigma_x invece di sigma_z): inverte z
        refl = np.where(cl[:, None] > 0, np.array([1.0, 1.0, -1.0]), np.array([1.0, 1.0, 1.0]))
        np.add.at(B, ii, contrib_j * refl); np.add.at(deg, ii, wl)
        np.add.at(B, jj, contrib_i * refl); np.add.at(deg, jj, wl)
        B = B / np.maximum(deg[:, None], 1e-9)
        # INERZIA = |Psi|^2 (la materia mantiene il moto), come in mem_mot
        if not hasattr(self, "psi") or len(self.psi) < n: self.calcola_psi()
        inerzia = np.maximum(np.abs(self.psi[:n])**2, 1e-6)
        dtn = dt_n if np.isscalar(dt_n) else np.asarray(dt_n)[:n]
        dtn_c = dtn if np.isscalar(dtn) else dtn[:, None]
        # MEMORIA HEBBIANA: omega si conserva + correzione dal campo (torsione B x n) - decadimento
        correzione = np.cross(B, nb)                      # la geodetica che piega il momento
        # VITA MEDIA LOCALE (ispirata al decadimento atomico / regola d'oro di Fermi): TAU_A non e'
        # piu' un numero fisso ma una PROPRIETA' DELLO STATO. Come ogni isotopo ha la sua vita media,
        # ogni nodo ha la sua: stati fortemente legati (|Psi|^2 grande, nucleo coerente) decadono
        # LENTAMENTE (nucleo stabile); stati deboli (|Psi|^2 piccolo, alone) decadono in FRETTA (stato
        # eccitato instabile). TAU_A_locale = TAU_A*|Psi|^2 / densita' mediana (coefficiente calibrato,
        # nessun numero nuovo). IN VERIFICA: stabile, ma il guadagno sul decadimento lungo non e'
        # ancora confermato (manca il confronto lungo TAU_A-fisso vs locale). Reversibile: se
        # TAU_A_LOCALE=False torna al comportamento fisso.
        if TAU_A_LOCALE:
            _dens = np.abs(self.psi[:n])**2
            _dens_rif = max(float(np.median(_dens[_dens > 1e-6])), 1e-6) if np.any(_dens > 1e-6) else 1.0
            _tau = TAU_A * np.maximum(_dens / _dens_rif, 0.05)   # vita media locale, pavimento 0.05
            _tau = _tau[:, None]
        else:
            _tau = TAU_A
        self.omega_s = self.omega_s + dtn_c * (correzione / inerzia[:, None] - self.omega_s / _tau)
        # PRECESSIONE conservativa: ruoto il Bloch attorno a omega (rotazione esatta, unitaria)
        on = np.linalg.norm(self.omega_s, axis=1, keepdims=True)
        ohat = self.omega_s / np.maximum(on, 1e-9)
        ang = on * (dtn_c if not np.isscalar(dtn_c) else dtn_c)
        cA = np.cos(ang); sA = np.sin(ang)
        dot = np.sum(ohat * nb, axis=1, keepdims=True)
        nb_new = nb * cA + np.cross(ohat, nb) * sA + ohat * dot * (1 - cA)
        nb_new = nb_new / np.maximum(np.linalg.norm(nb_new, axis=1, keepdims=True), 1e-9)
        self._nb = nb_new.copy()                          # stato dello spinore (indipendente da phi)
        self._nb_prec = nb_new.copy()                     # memorizzo per il ritardo causale
        # rileggo phi_s (angolo polare) dal Bloch. phi (fase scalare U(1)) resta intatta.
        self.phi_s = np.arccos(np.clip(nb_new[:, 2], -1, 1))            # b = angolo polare [0,pi]

    def spin_locale(self):
        """MISURA dello spin nel TEMPO PROPRIO LOCALE. Lo spin (frequenza di rotazione della
        fase del campo) e' una frequenza DERIVATA/IMMERSA: e' un processo che accade DENTRO la
        materia gia' formata, immersa nel proprio tempo. Va dunque LETTO nel tempo proprio del
        luogo, non nel tick fondamentale DT. Questo la distingue nettamente dalla frequenza
        f_i che DEFINISCE il ritmo (metodo ritmo()): quella e' FONDAMENTALE, sta a monte del
        tempo proprio, e deve usare DT come riferimento comune (senno' la dilatazione non e'
        piu' definibile). Qui invece siamo A VALLE: lo spin e' conseguenza del processo gia'
        immerso, e usare DT lo mescolerebbe con la dilatazione gravitazionale (come misurare
        il decadimento di un muone col nostro orologio invece che col suo). Ritorna la
        frequenza propria per nodo, letta nel tempo proprio locale dt_n = DT * r."""
        n = self.n
        if self._psi_prec is None or len(self._psi_prec) != n:
            return np.zeros(n)
        a = np.angle(self.psi[:n]) - np.angle(self._psi_prec[:n])
        dphi = np.abs((a + np.pi) % (2 * np.pi) - np.pi)
        r = self.ritmo()
        if r is None:
            r = np.ones(n)               # orologio globale: tempo proprio = tick
        r = r[:n]
        # spin = fase accumulata / tempo PROPRIO con cui e' avvenuta (dt_n = DT * r).
        # Toglie la dilatazione: e' la rotazione vera nel tempo del luogo, non nel tick globale.
        return dphi / (DT * np.maximum(r, 0.01))

    def _pesi(self):
        ramp = np.minimum(1.0, self.eta / TAU_A)
        base = np.exp(-self.d / self._lam_archi()) * ramp[self.i] * ramp[self.j]
        if KERNEL_ALPHA != 0.0 and len(self.tw) == len(self.d):
            # KERNEL BILANCIATO DAL TEMPO PROPRIO con HAMILTONIANA RAZIONALE (cutoff UV).
            # tau = |torsione| in unita' del quanto di olonomia (l'energia torsionale locale).
            # Il rinforzo del kernel non e' piu' tau^alpha (che cresce illimitato e fa
            # divergere il sistema quando la torsione fluttua all'estremo), ma la forma
            # razionale exp(alpha*tau/(1+beta*tau)):
            #   - torsione bassa (tau<<1): esponente ~ alpha*tau -> rinforzo lineare, come prima
            #     (regime di attivazione: la materia si struttura, gravita').
            #   - torsione alta (tau->inf): esponente satura a alpha/beta -> il rinforzo NON
            #     diverge, si ferma a exp(alpha/beta) (regime di sovraccarico: cutoff UV, la
            #     cella rifiuta la singolarita'). E' la capienza elastica limite del reticolo.
            # Il rapporto alpha/beta e' il tetto del rinforzo = capienza della cella. Vale 2:
            # le due unita' di torsione/capienza emerse dall'analisi della campana (non un
            # numero esterno). alpha = KERNEL_ALPHA (bilanciamento col tempo proprio), e
            # beta = alpha/2 perche' il tetto sia 2. La transizione fra rinforzo e cutoff e'
            # incorporata nella forma razionale: i regimi emergono da se', senza soglia netta.
            tau = np.abs(self.tw) / PHI_CRIT              # energia torsionale (unita' di quanto)
            alpha = KERNEL_ALPHA
            beta = KERNEL_ALPHA / 2.0                     # cosi' alpha/beta = 2 (capienza cella)
            base = base * np.exp(alpha * tau / (1.0 + beta * tau))
        return base

    def _mat(self, val):
        """riempie la struttura in cache: nessuna ricostruzione, nessuna densa"""
        if self._S is None: self._costruisci_struttura()
        self._S.data = np.concatenate([val, val])[self._perm]
        return self._S

    def calcola_psi(self, w=None):
        if self.n == 0 or not len(self.i):
            self.psi = np.zeros(self.n, complex); return self.psi
        if w is None: w = self._pesi()
        # COARSE-GRAINING: ogni solitone-blocco porta la massa di SCALA_B fini. L'ampiezza
        # scala come sqrt(SCALA_B) cosi' che l'intensita' |Psi|^2 (la massa) scali con
        # SCALA_B, come richiesto per preservare Poisson (la sorgente e' rho=|Psi|^2).
        amp = 1.0 if SCALA_B == 1.0 else np.sqrt(SCALA_B)
        F = self._mat(w) @ (amp * np.exp(1j * self.phi))
        self.psi = self.satura(F)                          # saturazione regolarizzata (Leggi XV/XVIII)
        return self.psi

    def intensita(self): return np.abs(self.psi) ** 2

    @staticmethod
    def satura(f):
        """SATURAZIONE RAZIONALE del campo, coerente con quella dell'interferenza:
        S(f) = f / (1 + GAMMA*|f|). Un solo ingrediente, GAMMA, gia' nel sistema:
        nessun parametro nuovo, ne' di scala ne' di regolarizzazione. Il termine 1e-9
        e' la STESSA regolarizzazione anti-zero gia' usata in tutto il codice (nei
        np.maximum(...,1e-9)), non una manopola: rende |f| liscio all'origine senza
        introdurre valori nuovi. Vettorializzata. Gestisce f reale (mitosi/torsione)
        e complesso (interferenza): np.abs(f) e' il modulo in entrambi i casi."""
        return f / (1.0 + GAMMA * np.sqrt(np.abs(f) ** 2 + 1e-9))

    @staticmethod
    def _w4(a): return (a + 2 * np.pi) % (4 * np.pi) - 2 * np.pi

    @staticmethod
    def _w8(a): return (a + 4 * np.pi) % (8 * np.pi) - 4 * np.pi
    # avvolgimento su ±4pi: permette alla torsione di vivere sul dominio DOPPIO (4pi)
    # invece che su 2pi. Usato dalla torsione a doppia copertura (flag TORS_4PI),
    # motivato dai legami dipolari che uniscono due antichirali (due mezzi-twist).

    def step(self):
        if self.n < 2 or not len(self.i): return
        i, j = self.i, self.j
        r = self.ritmo()                       # None se l'orologio e' globale
        if r is None:
            dt_n = DT; dt_e = DT
        else:
            dt_n = DT * r                      # per nodo
            dt_e = DT * 0.5 * (r[i] + r[j])    # per arco
            self._psi_prec = self.psi.copy()
        w = self._pesi(); self.eta += dt_n
        A = w * np.cos(self.phi0[i] - self.phi0[j])
        z = np.exp(1j * self.phi)
        coppia = K_C * np.imag(np.conj(z) * (self._mat(A) @ z))
        # AUTO-INTERAZIONE DELL'INTERFERENZA (opzione, MU_PSI=0 di default).
        # Termine di energia H_int = -(mu/2) sum_k |Psi_k|^2, derivato -> forza
        # sulle fasi -dH/dphi. Con MU_PSI<0 e' REPULSIVO: l'interferenza alta ALZA
        # l'energia, la materia si oppone alla propria concentrazione (pressione
        # interna). La forma NON e' scelta: e' la derivata di |Psi|^2 rispetto a phi.
        #   Psi = M z (a meno della saturazione); d|Psi|^2/dphi_n coinvolge M^T Psi.
        # REPULSIONE COME LEGGE con CONVERSIONE DINAMICA (nessun parametro, nessun esponente fisso).
        # La vicinanza al collasso di ogni nodo = riempimento * coerenza, TUTTO da stato:
        #  - coerenza locale = |media e^{i phi} sui vicini| (0=scorrelato, 1=in fase) = proiezione reale
        #  - riempimento = (numero efficace di vicini coerenti) / Ncrit ADATTIVO (ricalcolato da stato)
        # u -> 1 quando un addensamento coerente raggiunge il numero critico: li' la repulsione
        # scatta e rifiuta altra concentrazione (il cluster "e' pieno"). Intensita' u(u+2) (forma
        # dalla saturazione del campo). Segno MENO = opposto all'attrazione K_C. Nessun numero messo
        # lì: Ncrit e coerenza sono grandezze di stato, la conversione e' dinamica.
        if REPULS_LEGGE:
            self.calcola_psi()
            MtPsi = self._mat(w) @ self.psi
            dHdphi = 2.0 * np.imag(np.conj(z) * MtPsi)   # direzione: de-concentra l'interferenza
            zc = np.exp(1j * self.phi[:self.n])
            # COERENZA COL NUCLEO (corretta): NON la media vettoriale coi vicini di legame (che il
            # guscio in antifase abbatte, spegnendo la repulsione proprio quando la massa si struttura),
            # ma l'allineamento del nodo con la FASE DEL CAMPO Psi locale - il "battito" della sua
            # massa, dominato dal nucleo costruttivo. Un nodo del nucleo (in fase col campo) resta
            # coerente ~1 anche quando il guscio si forma; il guscio (antifase col campo) da coerenza
            # negativa e NON contribuisce alla repulsione del nucleo. Cosi' la repulsione resta accesa
            # dove la materia si concentra, invece di spegnersi.
            psi_loc = self.psi[:self.n]
            fase_campo = np.angle(psi_loc + 1e-12)       # fase del campo locale = battito della massa
            coerenza = np.cos(self.phi[:self.n] - fase_campo)   # +1 nucleo (in fase), -1 guscio (antifase)
            coerenza = np.clip(coerenza, 0.0, 1.0)       # solo il nucleo costruttivo alimenta la repulsione
            # numero efficace di puntatori coerenti che il nodo sente: ampiezza del campo locale
            # (|Psi| e' gia' l'interferenza dei vicini coerenti) rapportata all'ampiezza per puntatore
            deg = np.maximum(np.bincount(i, minlength=self.n)[:self.n] +
                             np.bincount(j, minlength=self.n)[:self.n], 1)
            somma_vic = np.zeros(self.n, complex)
            np.add.at(somma_vic, i, zc[j]); np.add.at(somma_vic, j, zc[i])
            n_vic_coer = np.abs(somma_vic)               # numero efficace di vicini in fase
            try:
                Ncrit_ad = massa_critica_adattiva(self)
            except Exception:
                Ncrit_ad = massa_critica_collasso()
            riempimento = n_vic_coer / max(Ncrit_ad, 1e-9)
            u = riempimento * coerenza                   # vicinanza al collasso (0..~1), tutto da stato
            fattore = u * (u + 2.0)                       # (1+u)^2 - 1, la legge dalla saturazione
            coppia = coppia - fattore * dHdphi           # MENO = repulsivo, opposto all'attrazione
        elif MU_PSI != 0.0:
            self.calcola_psi()
            MtPsi = self._mat(w) @ self.psi            # M simmetrica: M^T Psi = M Psi
            dHdphi = 2.0 * np.imag(np.conj(z) * MtPsi)  # d(sum|Psi|^2)/dphi_n
            coppia = coppia + MU_PSI * dHdphi           # (vecchia repulsione a parametro, fallback)
        # TERMINE DI HALL / FRAME-DRAGGING come LEGGE (non parametro): il twist, finora solo
        # registrato, chiude il loop e agisce come coppia. La forza NON ha un coefficiente
        # libero: e' il twist locale MEDIO normalizzato dalla scala critica del sistema
        # (tw/PHI_CRIT, la stessa che definisce il tempo proprio), mediato sugli archi del nodo
        # (la torsione che il nodo sente, non la somma che crescerebbe col grado). Emerge nella
        # scala giusta (~0.2 della coppia principale) senza aggiustamenti. E' la forza non
        # conservativa (frame-dragging, v x B con B=twist) che devia trasversalmente il moto.
        if FRAME_DRAG and len(self.tw):
            twn = self.tw / PHI_CRIT                     # twist adimensionale (scala di stato)
            twist_nodo = np.zeros(self.n)
            grado = np.zeros(self.n)
            np.add.at(twist_nodo, i, twn); np.add.at(twist_nodo, j, -twn)  # circolazione orientata
            np.add.at(grado, i, 1.0);      np.add.at(grado, j, 1.0)
            coppia = coppia + twist_nodo[:self.n] / np.maximum(grado[:self.n], 1.0)
        if REGIME == "deterministico":
            # TERMOSTATO NOSE-HOOVER con TEMPERATURA TARGET = LEGGE (dal vuoto di equilibrio P_eq).
            # L'energia cinetica di fase e' <phivel^2>. Il target NON e' un parametro: e' l'energia
            # di punto zero coerente con la densita' di equilibrio del vuoto P_eq = self.d0 (che e'
            # gia' una legge emergente del sistema, insegue la mediana globale di rho). L'attrito xi
            # evolve per riportare l'energia al target: xi>0 frena (energia alta), xi<0 RIFORNISCE
            # (energia bassa) -> il sistema si auto-sostiene invece di spegnersi.
            E_cin = float(np.mean(self.phivel[:self.n]**2)) if self.n > 0 else 0.0
            # TARGET come legge: energia di punto zero del vuoto di equilibrio. P_eq = mediana di d0
            # (densita' di sfondo); l'energia di fase che quel vuoto sostiene scala con P_eq attraverso
            # la relazione di dispersione (v^2, la rigidita' del mezzo). Nessun numero libero: tutto da
            # grandezze gia' nel sistema (d0, la scala di frequenza mediana del ritmo).
            P_eq = float(np.median(self.d0[:self.n])) if self.n > 0 and len(self.d0) >= self.n else 1.0
            T_target = (CS_M ** 2) * P_eq          # energia di punto zero = rigidita' del mezzo (c_s^2) * densita' vuoto (P_eq): leggi/costanti gia' nel sistema, nessun parametro nuovo
            # TERMOSTATO NOSE-HOOVER con TARGET MOBILE STABILE. Il target T_target = c_s^2 * P_eq
            # NON e' costante: P_eq (densita' del vuoto di equilibrio) evolve e cala mentre il
            # sistema si dirada. Un termostato con inerzia FISSA insegue troppo lentamente un target
            # calante: quando E_cin supera T_target, non fa in tempo a frenare -> instabilita' (era
            # la causa dell'artefatto). La soluzione fedele: reagire all'ERRORE RELATIVO (E-T)/T e
            # rendere la reattivita' proporzionale al target corrente, cosi' il termostato mantiene
            # la stessa risposta RELATIVA ovunque vada il bersaglio. Piu' un richiamo che impedisce
            # la deriva di xi. Tutto in unita' del sistema: nessun parametro nuovo.
            Tt = max(T_target, 1e-6)
            err_rel = (E_cin - Tt) / Tt                     # errore RELATIVO al target (adimensionale)
            tau_termo = np.sqrt(max(1.0/Tt, 1e-6))          # tempo di risposta: scala col target (piu' basso il target, piu' reattivo)
            dt_scal = float(np.median(dt_n)) if np.ndim(dt_n) else float(dt_n)
            # dinamica di xi: guida dall'errore relativo + richiamo -xi (anti-deriva). Entrambi col
            # tempo di risposta tau_termo che si adegua al target mobile.
            self.xi_termo += dt_scal * (err_rel - self.xi_termo) / tau_termo
            self.xi_termo = float(np.clip(self.xi_termo, -2.0, 2.0))   # guardia: attrito fisico limitato
            self.phivel += dt_n * (coppia - self.xi_termo * self.phivel) / M_PH
        else:
            self.phivel += dt_n * (coppia - G_PH * self.phivel) / M_PH
        self.phi = (self.phi + dt_n * self.phivel) % (4 * np.pi)
        # SETTORE SPINORIALE NON-ABELIANO (PASSO 2). Attivo solo con SPINORE. Ogni nodo porta
        # un vero SPINORE a due componenti in C^2 (parametrizzato da phi e phi_s). L'accoppiamento
        # fra due nodi e' una ROTAZIONE SU(2) il cui ASSE dipende dalla chiralita' del legame:
        # legami fra opposti ruotano attorno a un asse (sigma_z), fra uguali attorno a un altro
        # (sigma_x). Le matrici di Pauli NON commutano -> struttura non-abeliana SU(2) genuina,
        # da cui puo' emergere lo spettro di spin. Con SPINORE spento il settore e' inerte
        # (non-regressione: si recupera l'U(1) scalare su phi).
        if SPINORE and self.n > 2 and len(self.phi_s) == self.n:
            self._passo_spinoriale(i, j, w, dt_n)
        # SINCRONIZZAZIONE come LEGGE (non parametro): la forza deriva dalla dispersione locale
        # del tempo proprio (il pozzo dal centro di massa), come la soglia critica di Kuramoto,
        # che dipende dalla dispersione delle frequenze proprie. Dove i tempi propri sono simili
        # (nucleo uniforme) la sync e' forte e ordina; dove dispersi (bordo, vuoto) e' debole.
        # Costante universale 2/pi (Kuramoto), non tarata. K_SYNC resta come interruttore/scala
        # globale (1=legge piena); il profilo per nodo emerge dallo stato e scala col pozzo,
        # dunque col coarse-graining: legge indipendente dalla scala.
        if K_SYNC != 0.0 and self.n > 2:
            self.calcola_psi()
            I2 = np.abs(self.psi) ** 2
            cmv = (self.pos[:self.n] * I2[:, None]).sum(0) / max(I2.sum(), 1e-9)
            r_cm = np.linalg.norm(self.pos[:self.n] - cmv, axis=1) + LAM * 0.5
            pozzo = I2.sum() / r_cm                       # tempo proprio: pozzo dal centro
            wI = self._mat(w)
            uno = np.maximum(wI @ np.ones(self.n), 1e-9)
            media_p = wI @ pozzo / uno
            disp = np.sqrt(np.maximum(wI @ (pozzo ** 2) / uno - media_p ** 2, 0.0))
            # Soglia di Kuramoto bilanciata: la forza cresce con la PROFONDITA' del pozzo
            # relativa al suo valore tipico (alta nel nucleo denso, bassa nel vuoto), attenuata
            # dove la dispersione dei tempi propri e' alta (che alza la soglia di sincronizza-
            # zione). La profondita' DOMINA (il nucleo si ordina); il vuoto, poco profondo,
            # resta sotto. Tutto normalizzato dalla scala del pozzo -> adimensionale, indip.
            # dalla scala. Costante universale 2/pi.
            scala = max(pozzo.mean(), 1e-9)
            prof_rel = pozzo / scala                       # profondita' relativa (nucleo >> vuoto)
            attenua = scala / (scala + disp)               # <1 dove la dispersione e' alta
            forza = (2.0 / np.pi) * prof_rel * attenua
            forza = K_SYNC * forza                        # K_SYNC=1 = legge piena
            zc = wI @ np.exp(1j * self.phi)
            media = np.angle(zc)
            self.phi = (self.phi + dt_n * forza * np.sin(media - self.phi)) % (4 * np.pi)
        dph = self._w4(self.phi[i] - self.phi[j])
        if TORS_4PI and len(self.perc_chi) >= self.n:
            # TORSIONE A DOPPIA COPERTURA (4pi): sul legame dipolare, la torsione
            # include il contributo dei profili di percorrenza dei due antichirali
            # che unisce (perc_chi[i], perc_chi[j], di segno opposto per il filtro).
            # Ogni polo aggiunge il suo mezzo-twist di pi: il legame puo' accumulare
            # fino a 4pi invece di 2pi. L'avvolgimento passa da _w4 a _w8 (dominio doppio).
            twist_dip = np.pi * 0.5 * (self.perc_chi[i] - self.perc_chi[j])  # ±pi dai due poli
            _ttw = _tau_tw_locale(self) if TAU_LOCALI else TAU_TW
            self.tw += self._w8(dph + twist_dip - self.twp) - dt_e * self.tw / _ttw
            self.twp = self._w8(dph + twist_dip)
        else:
            _ttw = _tau_tw_locale(self) if TAU_LOCALI else TAU_TW
            self.tw += self._w4(dph - self.twp) - dt_e * self.tw / _ttw
            self.twp = dph
        # --- materia: una sola matrice dei pesi, riusata per Psi e diffusione ---
        Mw = self._mat(w)
        F = Mw @ np.exp(1j * self.phi)
        self.psi = self.satura(F)                          # saturazione regolarizzata (Leggi XV/XVIII)
        I = np.abs(self.psi) ** 2
        rho = 0.5 * (I[i] + I[j])

        # CALIBRAZIONE alla nascita, PRIMA di ogni lettura di peq: un arco appena
        # nato adotta la densita' che vede. Va fatta qui e non dopo, altrimenti
        # i NaN dei nuovi archi entrano nella proiezione e la diffusione li
        # propaga all'intero grafo (accade appena si aggiunge materia al vuoto).
        nuovi = np.isnan(self.peq)
        if nuovi.any(): self.peq[nuovi] = rho[nuovi]

        # --- VUOTO DI SFONDO LOCALE, che DIFFONDE sulla topologia (Legge I) ---
        # nessuna mediana globale: il vuoto conosce solo i propri vicini.
        # archi -> nodi (media topologica)
        den_w = np.maximum(np.bincount(i, w, minlength=self.n) +
                           np.bincount(j, w, minlength=self.n), 1e-12)
        # CHE COSA diffonde: P_eq stesso (livella, e con cio' sposta il punto
        # fisso) oppure il RESIDUO rho-P_eq (a residuo nullo la diffusione si
        # annulla, dunque P_eq = rho resta punto fisso esatto)
        campo = self.peq if DIFF_RES == 0.0 else (rho - self.peq)
        sp = np.bincount(i, campo, minlength=self.n) + \
             np.bincount(j, campo, minlength=self.n)
        cn = (Mw @ (sp / self._deg)) / den_w
        c_arco = 0.5 * (cn[i] + cn[j])
        # per DIFF_RES: r = rho - P_eq deve obbedire a  dr/dt = -r/TAU_BG + Lap(r),
        # e poiche' r = rho - P_eq il laplaciano entra in P_eq col segno MENO
        flusso = (c_arco - self.peq) if DIFF_RES == 0.0 else ((rho - self.peq) - c_arco)
        # il vuoto insegue la densita' locale E si mescola con il vicinato.
        # Nessuna fase privilegiata, nessuna metrica congelata: il sistema vale
        # tutto intero dal primo istante, transitorio compreso.
        if TAU_LOCALI:
            # TAU_BG LOCALE = kappa_BG / r, con r = ritmo del tempo proprio (|frequenza| di fase).
            # Il vuoto insegue la densita' al ritmo del tempo PROPRIO locale, non coordinato.
            r_nodo = np.abs(self.phivel[:self.n]) if len(self.phivel) >= self.n else np.ones(self.n)
            r_arco = 0.5 * (r_nodo[i] + r_nodo[j])
            tau_bg_loc = np.maximum(1.0 / np.maximum(r_arco, 1e-3), 1e-3)   # kappa=1: tau_bg = 1/r_locale
            self.peq += dt_e * ((rho - self.peq) / tau_bg_loc + flusso / TAU_DIFF)
        else:
            self.peq += dt_e * ((rho - self.peq) / TAU_BG + flusso / TAU_DIFF)
        if HAM_SRC == 0.0:
            anom = (rho - self.peq) / np.maximum(self.peq, 1e-9)     # anomalia relativa
            src = (ALPHA_M * anom if ALPHA_NAT == 0.0
                   else ALPHA_NAT * (CS_M ** 2 / np.maximum(self.d, 1e-6)) * anom)
        else:
            # forza dal potenziale delle fasi: coerenza CONTRAE, frustrazione DILATA
            src = -HAM_SRC * K_C * (w / LAM) * np.cos(self.phi0[i] - self.phi0[j]) * np.cos(dph)
        if ZETA_M == 0.0:
            beta = BETA_M
        elif ZETA_LOC:
            # SMORZAMENTO METRICO LOCALE (legge, non parametro): zeta scende dove la densita'
            # d'interferenza rho supera la mediana (nella MATERIA), lasciando vivere la
            # circolazione tangenziale; nel VUOTO (rho ~ mediana) resta ZETA_M pieno (stabilita').
            # Nessun numero nuovo: ZETA_M e rho gia' calcolati, forma 1/(1+x) come nel resto.
            med_rho = max(float(np.median(rho)), 1e-9)
            eccesso = np.maximum(rho / med_rho - 1.0, 0.0)   # 0 nel vuoto, cresce nella materia
            zeta_loc = ZETA_M / (1.0 + eccesso)              # ZETA_M nel vuoto, ->0 nel denso
            beta = 2.0 * zeta_loc * CS_M / np.maximum(self.d, 1e-6)
        else:
            beta = 2.0 * ZETA_M * CS_M / np.maximum(self.d, 1e-6)
        # il sotto-ciclo si infittisce quanto SERVE alla stabilita': nessun tetto
        # arbitrario al numero di sotto-passi, cosi' non tronca la dinamica veloce
        n1 = np.ceil(np.abs(src).max() * DT / (0.05 * CS_M))
        n2 = np.ceil(np.max(beta) * DT / 0.5)
        n3 = np.ceil(np.abs(self.vd).max() * DT / (0.1 * max(np.median(self.d), 0.1)))
        nsub = int(max(1, n1, n2, n3))
        dts = dt_e / nsub
        for _ in range(nsub):
            q = self.d - self.d0
            sm = np.bincount(i, q, minlength=self.n) + np.bincount(j, q, minlength=self.n)
            med = sm / self._deg
            lap = 0.5 * (med[i] + med[j]) - q
            # niente clip a mano: la velocita' resta limitata dalla dinamica
            # (smorzamento + saturazione), col passo infittito quanto basta
            self.vd = self.vd + dts * (CS_M ** 2 * lap + src - beta * self.vd)
            self.d = np.maximum(self.d + dts * self.vd, 0.05)
        if TAU_LOCALI:
            # TAU_P LOCALE = kappa_p * d/c_s (tempo di transito elastico dell'arco). kappa_p = TAU_P
            # come rapporto adimensionale O(1). Invariante per riparametrizzazione: e' un TEMPO fisico
            # dell'arco (quanto ci mette un'onda ad attraversarlo), non un numero di step.
            # FLAG TAU_USA_D0: se True usa d0 (distanza di RIPOSO) invece di d (distanza REALE dilatata).
            #   d  -> il tau cresce con lo spazio gonfiato: lascia dilatare di piu' (d_medio ~2.88)
            #   d0 -> il tau si basa sul riposo: piu' stabile, meno gonfiaggio (d_medio ~1.33)
            if TAU_USA_D0:
                d_arco = 0.5 * (self.d0[self.i] + self.d0[self.j]) if len(self.d0) else self.d0
            else:
                d_arco = 0.5 * (self.d[self.i] + self.d[self.j]) if len(self.d) else self.d
            tau_p_loc = np.maximum(d_arco / max(CS_M, 1e-9), 1e-3)   # kappa=1: tau_p = d_locale/c_s
            self.d0 += dt_e * (self.d - self.d0) / tau_p_loc
        else:
            self.d0 += dt_e * (self.d - self.d0) / TAU_P
        # PAVIMENTO FISICO su d0: la distanza di riposo non puo' scendere sotto la scala
        # minima del sistema (0.05, la stessa di d). Un d0 -> 0 non e' fisico (due nodi
        # non hanno distanza di riposo nulla) e fa divergere lo stress |d-d0|/d0 anche
        # con d sano. Non e' un tetto arbitrario: e' la scala minima gia' presente su d.
        self.d0 = np.maximum(self.d0, 0.05)

    def mitosi(self):
        if self.n >= MAX_NODI or not len(self.tw): return 0
        avv = np.abs(self.tw)
        # soglia della mitosi: 2pi classico, oppure 3pi se la torsione vive sul dominio
        # doppio (TORS_4PI). MISURATO: la torsione a doppia copertura accumula la fase
        # (fino a 2pi) piu' i due mezzi-twist dipolari (±pi) = 3pi come quanto naturale,
        # non 4pi (che sarebbe irraggiungibile). La mitosi e' cosi' guidata dalla
        # struttura a doppia copertura, con soglia al valore che la torsione tocca davvero.
        # SOGLIA CRITICA come LEGGE FISICA EMERGENTE, non il numero 3pi imposto.
        # La torsione a doppia copertura accumula due contributi, entrambi gia' nel
        # sistema: il QUANTO DI OLONOMIA (PHI_CRIT = 2pi, un giro completo di fase) e il
        # MASSIMO TWIST DIPOLARE (i due poli antichirali opposti danno |chi_i - chi_j|=2,
        # cioe' un mezzo-twist di pi: vedi twist_dip = pi*0.5*(chi_i-chi_j)). La soglia
        # critica EMERGE come loro somma: 2pi + pi = 3pi, non perche' scritto 3, ma perche'
        # e' un giro pieno piu' il twist dipolare massimo. Se cambiano gli ingredienti
        # (quanto o struttura dipolare) la soglia si aggiorna da se'. A doppia copertura
        # spenta resta il solo quanto di olonomia PHI_CRIT.
        if TORS_4PI:
            twist_max = np.pi                                 # |chi_i-chi_j|=2 -> pi*0.5*2 = pi
            soglia0 = PHI_CRIT + twist_max                    # = 2pi + pi (emergente), = 3pi
        else:
            soglia0 = PHI_CRIT
        # SOGLIA CRITICA LOCALE, PILOTATA DAL GRADIENTE DI TEMPO PROPRIO.
        # La soglia emergente (2pi+pi) e' il valore MEDIO; localmente si abbassa dove il
        # tempo proprio rallenta di piu' lungo l'arco (gradiente di tempo proprio), cioe'
        # nella direzione della geodetica. Dove la soglia locale e' piu' bassa la mitosi
        # scatta prima -> nasce piu' materia da quel lato -> il baricentro trasla lungo
        # la geodetica (principio di equivalenza: la materia va dove il tempo rallenta).
        # Il tempo proprio locale sull'arco e' tau = 1 + |tw|/PHI_CRIT (gia' nel kernel).
        # La modulazione e' LIMITATA a una frazione (tanh, ampiezza <0.3 della soglia):
        # la soglia non si annulla mai (mitosi che esplode) ne' diverge (mitosi che muore).
        soglia = np.full(len(avv), soglia0, float)
        if TORS_4PI and len(self.i) == len(avv):
            # gradiente di tempo proprio LUNGO l'arco: differenza del tempo proprio nodale
            # fra i due estremi. tau_nodo alto = tempo lento = materia. Dove il gradiente
            # e' forte, la soglia si abbassa (la mitosi e' agevolata verso il tempo lento).
            tau_nodo = np.zeros(self.n)
            aw = np.abs(self.tw)
            np.add.at(tau_nodo, self.i[self.i < self.n], aw[self.i < self.n])
            np.add.at(tau_nodo, self.j[self.j < self.n], aw[self.j < self.n])
            tau_nodo = 1.0 + tau_nodo / np.maximum(self._deg, 1) / PHI_CRIT
            grad_tau = np.abs(tau_nodo[self.i] - tau_nodo[self.j])   # gradiente lungo l'arco
            # modulazione limitata: la soglia scende di al piu' ~30% dove il gradiente e' forte
            soglia = soglia0 * (1.0 - 0.3 * np.tanh(grad_tau))
        # CRITICITA' NON MONOTONA (campana) ancorata ai due valori fisici del sistema:
        # massima alla SOGLIA LOCALE (soglia critica emergente, pilotata dal gradiente di
        # tempo proprio), e si SPEGNE al tetto della doppia copertura 4pi. Tra i due, la
        # mitosi decresce: dove la torsione supera la soglia e va verso il tetto, il
        # sistema RIDUCE la generazione (omeostasi), e a 4pi si azzera del tutto (confine
        # netto per reazione geometrica intrinseca). Il ciclo di vita:
        #   torsione < soglia   -> attivazione (sale): raffinamento dove lo spazio accumula stress
        #   torsione = soglia   -> massimo: strutturazione ottimale della materia
        #   soglia < tw < 4pi   -> riduzione (scende): il dominio si sta saturando
        #   torsione >= 4pi     -> spegnimento: la mitosi si azzera (auto-limitazione)
        # I due estremi (soglia locale, 4pi) sono grandezze fisiche del sistema, non
        # multipli astratti: la campana lavora nel regime che la torsione esplora davvero
        # (l'analisi con massimo a x=1 e spegnimento a x=2 restava inattiva perche' la
        # torsione non raggiunge mai 2 volte la soglia; con 4pi come spegnimento, si').
        TW_TETTO = 4.0 * np.pi                            # tetto della doppia copertura
        # La campana e' CENTRATA sulla soglia locale e STRETTA: quasi zero lontano dalla
        # soglia (cosi' la mitosi non scatta a torsione bassa e non esplode), massima
        # alla soglia, e comunque azzerata al tetto 4pi. Uso l'eccesso relativo rispetto
        # alla soglia come variabile, con la stessa saturazione del sistema per la salita
        # e un fattore di spegnimento (1 - tw/4pi) per la discesa verso il tetto.
        #   - salita: satura(ecc) e' zero sotto soglia, sale sopra (nessuna mitosi a tw bassa)
        #   - discesa: (1 - tw/4pi) porta a zero quando la torsione tende al tetto
        # Prodotto = campana: attivazione sopra soglia, massimo appena sopra, spegnimento
        # verso 4pi. Il ramo sotto-soglia resta soppresso (stabilita'), il ramo sopra-soglia
        # ha il ciclo di vita (raffinamento -> saturazione -> spegnimento omeostatico).
        ecc = avv / np.maximum(soglia, 1e-9) - 1.0        # eccesso oltre la soglia LOCALE
        ecc = np.maximum(ecc, 0.0)                         # zero sotto soglia: niente mitosi
        salita = self.satura(ecc)                         # sale sopra soglia (soppressa sotto)
        discesa = np.clip(1.0 - avv / TW_TETTO, 0.0, 1.0) # -> 0 quando tw -> 4pi (spegnimento)
        # RAMO REPULSIVO regolato dal TEMPO PROPRIO LOCALE. Il tempo proprio finora
        # modulava solo il RITMO; ora decide anche il SEGNO. La mitosi CREA (+) nel regime
        # critico (attorno alla soglia, dove la materia si struttura) e inverte in
        # REPULSIONE (-) avvicinandosi al tetto 4pi (materia super-compressa, tempo proprio
        # estremo). La transizione di segno sta FRA la soglia (crea) e il tetto (respinge):
        # cosi' la creazione avviene attorno alla soglia e la repulsione solo nel
        # sovraccarico verso 4pi. La campana va da +max (a soglia) a -max (a 4pi).
        tau_pp = 1.0 + avv / PHI_CRIT                     # tempo proprio locale (>=1)
        tau_soglia = 1.0 + soglia / PHI_CRIT              # tempo proprio ALLA soglia (locale)
        tau_tetto = 1.0 + TW_TETTO / PHI_CRIT             # tempo proprio al tetto 4pi (=3)
        # transizione di segno a META' fra soglia e tetto: crea da soglia in giu', respinge
        # da meta'-cammino-al-tetto in su. Centrata sul punto medio (soglia+tetto)/2.
        centro = 0.5 * (tau_soglia + tau_tetto)
        segno = -np.tanh(3.0 * (tau_pp - centro))
        tau_locale = 1.0 / tau_pp                          # ritmo (sempre positivo)
        ampiezza = salita * discesa * tau_locale           # campana positiva (0..max)
        resp = ampiezza * segno                            # FIRMATA: + crea, - respinge
        # --- CREAZIONE: dove resp > 0, mitosi probabilistica (come prima) ---
        prob = np.clip(resp, 0.0, 1.0)
        nasce = self.rng.random(len(avv)) < prob
        # --- REPULSIONE: dove resp < 0, il tempo proprio estremo respinge: allarga d0
        # localmente (pressione a corto raggio), invece di creare nodi. E' il confine
        # attivo dei nuclei super-densi: la materia compressa respinge invece di collassare.
        rep = np.clip(-resp, 0.0, 1.0)
        if rep.any() and len(self.d0) == len(avv):
            # spinta repulsiva proporzionale a rep: d0 cresce dove il tempo proprio e' estremo.
            # limitata (2% per passo) e conservativa in media come nella memoria hebbiana.
            spinta = 0.02 * np.median(self.d0) * rep
            self.d0 = self.d0 + spinta - spinta.mean()     # media zero: pressione, non espansione
            self.d0 = np.maximum(self.d0, 0.05)            # PAVIMENTO: la spinta non deve
            #   portare d0 sotto la scala minima, o lo stress |d-d0|/d0 diverge (bug rientrante)
        c = np.where(nasce)[0]
        if not len(c): return 0
        c = c if MITMAX == 0 else c[np.argsort(avv[c])[::-1]][:MITMAX]
        I = self.intensita()
        a, b = self.i[c], self.j[c]
        ok = 0.5 * (I[a] + I[b]) >= QMIN_M * float(np.median(self.peq))
        self.negate += int((~ok).sum()); sel = c[ok]
        if not len(sel): return 0
        a, b = self.i[sel], self.j[sel]; m = self.n + np.arange(len(sel))
        D = self._w4(self.phi[a] - self.phi[b])
        # FASE DEL FIGLIO. Di default la fase media (mitosi isotropa nell'interferenza:
        # il pattern costruttivo si espande simmetrico, il baricentro non trasla).
        # Con MITOSI_DIR la fase del figlio e' spostata verso il genitore a torsione
        # MAGGIORE: il pattern d'interferenza costruttiva si estende lungo il gradiente
        # di torsione, e il baricentro dell'interferenza (=la materia) trasla in quella
        # direzione. L'asimmetria e' nella FASE, dove vive la materia, non nella posizione
        # (che il rilassamento geometrico riporterebbe indietro). Non e' una forza: e'
        # l'orientamento della replicazione lungo il gradiente gia' presente.
        if MITOSI_DIR != 0.0:
            twn = np.zeros(self.n)
            np.add.at(twn, self.i[self.i < self.n], np.abs(self.tw)[self.i < self.n])
            np.add.at(twn, self.j[self.j < self.n], np.abs(self.tw)[self.j < self.n])
            twn = twn / np.maximum(self._deg, 1)
            # bias in [-0.5,0.5]: verso il genitore piu' teso. 0 = punto medio.
            bias = 0.5 * np.tanh(MITOSI_DIR * (twn[a] - twn[b]))
            fm = (self.phi[a] - (0.5 + bias) * D) % (4 * np.pi)
        else:
            fm = (self.phi[a] - 0.5 * D) % (4 * np.pi)
        pos_figlio = 0.5 * (self.pos[a] + self.pos[b])
        # --- LEGGE DI STABILITA' (ANTIFASE DELLE AGGIUNTE, interruttore ANTIFASE_ADD) ---
        # Dove la densita' locale supera l'equilibrio, il NUOVO nodo nasce in ANTIFASE invece
        # che in fase, con probabilita' morbida tanh((rho-rho_eq)/rho_c). Cosi' l'aggiunta NON
        # incrementa l'interferenza collettiva: la materia esistente resta intatta, ma la
        # crescita si ferma. rho_c = densita' a N_critico (scala derivata, NON un parametro):
        # transizione dolce vicino all'equilibrio, satura verso il collasso. La materia e'
        # sfumata -> annichilazione sfumata. NB: opera sulle AGGIUNTE (un nodo), non sul
        # collettivo esistente (che un intervento locale non potrebbe scalfire).
        if ANTIFASE_ADD:
            rho_sel = 0.5 * (I[a] + I[b])                       # densita' d'interferenza sull'arco
            peq_sel = self.peq[sel]
            peq_sel = np.where(np.isnan(peq_sel), rho_sel, peq_sel)
            # rho_c: densita' corrispondente a N_critico. Uso la densita' di equilibrio scalata
            # dal rapporto N_c/N_attuale come proxy della soglia di coerenza, derivata dallo stato.
            rho_c = np.maximum(peq_sel, 1e-6) * max(massa_critica_collasso() / max(self.n, 1), 1e-3)
            s = (rho_sel - peq_sel) / np.maximum(rho_c, 1e-6)
            p_anti = np.where(s > 0, np.tanh(s), 0.0)          # prob antifase, 0 sotto equilibrio
            flip = self.rng.random(len(sel)) < p_anti
            fm = np.where(flip, (fm + 2 * np.pi) % (4 * np.pi), fm)  # +2pi in copertura 4pi = antifase
            self.ultima_frac_antifase = float(flip.mean()) if len(flip) else 0.0
        self.pos = np.vstack([self.pos, pos_figlio])
        self.phi = np.concatenate([self.phi, fm]); self.phi0 = np.concatenate([self.phi0, fm])
        self.phi_s = np.concatenate([self.phi_s, self.phi_s[a]])   # spinore del figlio: eredita dal genitore
        self.phivel = np.concatenate([self.phivel, 0.5 * (self.phivel[a] + self.phivel[b])])
        self.eta = np.concatenate([self.eta, np.zeros(len(sel))])
        # profilo di percorrenza del figlio: eredita la chiralita' del genitore a
        # (dormiente, non ancora accoppiato). Salto a 0.
        self.perc_chi = np.concatenate([self.perc_chi, self.perc_chi[a]])
        self.perc_tw = np.concatenate([self.perc_tw, np.zeros(len(sel))])
        self.mem_mot = np.vstack([self.mem_mot, self.mem_mot[a]]) if len(self.mem_mot) else np.zeros((len(sel), 3))
        # TRACKING: i figli della mitosi ereditano la concorrenza del genitore a (nascono dalla sua
        # divisione, concorrono alle stesse masse). conc_archi viene riallineato sotto (keep+nuovi).
        if self.conc_nodi:
            for kk in a:
                eredita = [v[:] for v in self.conc_nodi[kk]] if kk < len(self.conc_nodi) else []
                self.conc_nodi.append(eredita)
        sciolta = np.abs(self.tw[sel]) / PHI_CRIT
        g = np.concatenate([a, b])
        if REGIME == "deterministico":
            # REGIME DETERMINISTICO (WIP): impulso modulato dal TEMPO PROPRIO LOCALE tau =
            # 1+|tw|/PHI_CRIT. Componente comune diretta da tau (rompe la simmetria attorno alla
            # materia, non si media a zero) + parte chirale antisimmetrica. Saturazione tau/(1+tau)
            # = termostato (auto-freno dove tau alto). Vedi note REGIME in testa al file.
            tau_a = 1.0 + np.abs(self.tw[sel]) / PHI_CRIT
            mod = tau_a / (1.0 + tau_a)
            chi_a = self.perc_chi[a]; chi_b = self.perc_chi[b]
            comune = KICK_TW * sciolta * (mod - 0.5)
            calcio_a = comune + 0.5 * KICK_TW * sciolta * chi_a * mod
            calcio_b = comune - 0.5 * KICK_TW * sciolta * chi_b * mod
            self.phi[a] = (self.phi[a] + calcio_a) % (4 * np.pi)
            self.phi[b] = (self.phi[b] + calcio_b) % (4 * np.pi)
        else:
            # REGIME STOCASTICO (canonico, validato): rinculo di fase casuale. DEFAULT.
            self.phi[g] = (self.phi[g] + self.rng.normal(0, 1, len(g)) *
                           KICK_TW * np.concatenate([sciolta, sciolta])) % (4 * np.pi)
        keep = np.ones(len(self.i), bool); keep[sel] = False
        dh = self.d[sel] / 2
        # lunghezza di riposo dei due nuovi archi. Di default meta' dell'arco (dh):
        # e' questo dimezzamento che produce la compressione degenere, perche' la
        # geometria di equilibrio si accorcia a ogni suddivisione.
        # Con PLAST_MIT>0: offset plastico PERMANENTE proporzionale alla torsione
        # sciolta, cosicche' la suddivisione registri nel mezzo una generazione di
        # struttura metrica invece di un puro infittimento. Modifica lo stato
        # stazionario dell'arco (d0), non un impulso transitorio su vd.
        if PLAST_MIT > 0.0:
            d0h = dh * (1.0 + PLAST_MIT * sciolta)   # sciolta = |tw|/PHI_CRIT >= 1
            d0new = np.concatenate([d0h, d0h])
        else:
            d0new = np.concatenate([dh, dh])
        self.i = np.concatenate([self.i[keep], a, m])
        self.j = np.concatenate([self.j[keep], m, b])
        # TRACKING: riallineo conc_archi. Archi mantenuti (keep) conservano la concorrenza; i nuovi
        # (a-m, m-b) nascono senza concorrenza (ripopolabile da aggiorna_pesi_concorrenza).
        if self.conc_archi:
            keep_idx = np.where(keep)[0]
            self.conc_archi = ([self.conc_archi[e] if e < len(self.conc_archi) else []
                                for e in keep_idx] + [[] for _ in range(2 * len(a))])
        self.d = np.concatenate([self.d[keep], dh, dh])
        self.d0 = np.concatenate([self.d0[keep], d0new])
        self.vd = np.concatenate([self.vd[keep], self.vd[sel], self.vd[sel]])
        self.peq = np.concatenate([self.peq[keep], self.peq[sel], self.peq[sel]])
        zz = np.zeros(len(sel))
        self.tw = np.concatenate([self.tw[keep], zz, zz])
        self.twp = np.concatenate([self.twp[keep], self._w4(self.phi[a] - fm),
                                   self._w4(fm - self.phi[b])])
        self._grado(); self.nati += len(sel)
        # EMISSIONE DI COPPIA: per una frazione degli eventi nasce un anti-nodo a
        # fase fm+pi, collegato ai due genitori a-b. La coppia (nodo fm + anti-nodo
        # fm+pi) ha media fm, quindi conserva l'olonomia globale, ma introduce due
        # difetti opposti. L'anti-nodo e' collocato sul punto medio come il nodo,
        # cosi' i due nascono sovrapposti e la dinamica (antifase -> repulsione) li
        # separa da se'. NON si impone alcuna forza: solo la fase opposta.
        if COPPIA_MIT > 0.0 and self.n < MAX_NODI:
            # CREAZIONE DI COPPIA alla Schwinger: probabilistica secondo l'ECCESSO di
            # torsione oltre il quanto critico. Come nel meccanismo di Schwinger la
            # creazione e' soppressa sotto la soglia (sciolta<=1) e sale esponenzialmente
            # oltre. La torsione gioca il ruolo del campo E, il quanto 2pi quello del
            # campo critico. prob = 1 - exp(-COPPIA_MIT * (sciolta-1)).
            eccesso_torsione = np.maximum(0.0, sciolta - 1.0)
            # --- CORREZIONE ESPLORATIVA (COPPIA_DENSITA): feedback anti-accrescimento ---
            # La torsione SATURA a ~2.5pi, quindi eccesso_torsione satura e la creazione di
            # coppia non pareggia mai la mitosi -> il grumo cresce senza limite. La densita'
            # invece cresce senza saturare. Aggiungo all'eccesso l'ANOMALIA DI DENSITA' locale
            # (rho-peq)/peq sugli archi in mitosi: dove la densita' supera l'equilibrio, piu'
            # antifase distruttiva, che cancella la materia in eccesso. Feedback CONTINUO (prob
            # graduale), nella valuta giusta (crea/distrugge portatori), che si annulla al
            # pareggio (anomalia 0). NON un parametro nuovo: rho e peq sono gia' nello stato.
            # eccesso totale = eccesso_torsione + max(0, anomalia_densita). Interruttore per null-test.
            if COPPIA_DENSITA:
                I = self.intensita()
                rho_sel = 0.5 * (I[a] + I[b])                   # densita' d'interferenza sull'arco
                peq_sel = self.peq[sel]
                peq_sel = np.where(np.isnan(peq_sel), rho_sel, peq_sel)
                anom = np.maximum(0.0, (rho_sel - peq_sel) / np.maximum(peq_sel, 1e-6))
                eccesso_totale = eccesso_torsione + anom
            else:
                eccesso_totale = eccesso_torsione
            prob_coppia = 1.0 - np.exp(-COPPIA_MIT * eccesso_totale)
            self.ultima_prob_coppia = float(prob_coppia.mean()) if len(prob_coppia) else 0.0
            estratto = self.rng.random(len(sel)) < prob_coppia
            if estratto.any():
                pick = np.where(estratto)[0]
                aa, bb = a[pick], b[pick]
                anti = (fm[pick] + 2 * np.pi) % (4 * np.pi)
                nc = len(pick)   # fase opposta (fm+pi)
                k = self.n + np.arange(nc)
                dd = np.maximum(0.5 * np.linalg.norm(self.pos[aa] - self.pos[bb], axis=1), 0.05)
                pmed = float(np.median(self.peq))
                self.pos = np.vstack([self.pos, 0.5 * (self.pos[aa] + self.pos[bb])])
                self.phi = np.concatenate([self.phi, anti])
                self.phi0 = np.concatenate([self.phi0, anti])
                self.phi_s = np.concatenate([self.phi_s, np.zeros(nc)])   # spinore antinodo: 0 (inerte se spento)
                self.phivel = np.concatenate([self.phivel, 0.5 * (self.phivel[aa] + self.phivel[bb])])
                self.eta = np.concatenate([self.eta, np.zeros(nc)])
                # l'antiparticella nasce con chiralita' OPPOSTA al genitore (antichirale).
                # Coerente con la creazione di coppia. Dormiente.
                self.perc_chi = np.concatenate([self.perc_chi, -self.perc_chi[aa]])
                self.perc_tw = np.concatenate([self.perc_tw, np.zeros(nc)])
                self.mem_mot = np.vstack([self.mem_mot, np.zeros((nc, 3))]) if len(self.mem_mot) else np.zeros((nc, 3))
                # TRACKING: l'anti-nodo Schwinger EREDITA la concorrenza del genitore aa. Se aa
                # concorre a una massa (nasce nel campo di una massa), l'anti-nodo vi concorre pure
                # (categoria "creazione di coppie" = accrescimento, non materia nuova). Se aa non
                # concorre a nulla (nasce nel vuoto teso), l'anti-nodo resta senza concorrenza
                # (materia nuova dal vuoto). La distinzione fisica: la Schwinger drena tensione di
                # una massa esistente, tranne quando nasce lontano da ogni massa.
                if self.conc_nodi:
                    for gk in aa:
                        eredita = [v[:] for v in self.conc_nodi[gk]] if gk < len(self.conc_nodi) else []
                        # marco l'origine Schwinger nella voce (4o campo opzionale) per distinguere
                        # la categoria "creazione di coppie" dall'accrescimento per mitosi
                        eredita = [[v[0], v[1], v[2], "schwinger"] if len(v) == 3 else v[:] for v in eredita]
                        self.conc_nodi.append(eredita)
                self.i = np.concatenate([self.i, aa, k])
                self.j = np.concatenate([self.j, k, bb])
                self.d = np.concatenate([self.d, dd, dd])
                self.d0 = np.concatenate([self.d0, dd, dd])
                self.vd = np.concatenate([self.vd, np.zeros(2 * nc)])
                self.peq = np.concatenate([self.peq, np.full(2 * nc, pmed)])
                zz2 = np.zeros(nc)
                self.tw = np.concatenate([self.tw, zz2, zz2])
                self.twp = np.concatenate([self.twp, self._w4(self.phi[aa] - anti),
                                           self._w4(anti - self.phi[bb])])
                self._grado(); self.nati += nc; self.coppie_nate += nc
        return len(sel)

    def campo_spaziale(self, G=72, mezzo=None, M=None):
        """LA SOLA INTERFERENZA, in tutto il volume, ricalcolata a ogni passo.

        |Psi(x)|^2 = somma_i K^2  +  somma_{i!=j} K K cos(dphi)
                      ^ FONDO         ^ INTERFERENZA
        Il primo termine e' presente anche con fasi del tutto casuali: non e'
        materia, e' la somma quadratica dei contributi (nel vuoto vale il 137%
        del totale). Disegnarlo significherebbe spacciare per materia l'alone
        incoerente. Qui viene SOTTRATTO, e resta solo l'interferenza:
          positiva = materia (cio' che sopravvive all'annullamento)
          negativa = distruzione (la cicatrice, visibile invece che assente)
        Rendering volumetrico a emissione-assorbimento, vista rotante."""
        if self.n == 0: return np.zeros((G, G)), 1.0, 0.0
        P = self.pos if M is None else self.pos @ M
        R = mezzo if mezzo else float(np.abs(P).max()) * 1.12 + 1e-6
        h = 2 * R / G
        idx = tuple(np.clip(((P[:, k] + R) / h).astype(int), 0, G - 1) for k in range(3))
        u = (np.arange(G) - G // 2) * h
        if getattr(self, "_r3_G", None) != (G, round(h, 6)):
            X, Y, Z = np.meshgrid(u, u, u, indexing="ij")
            self._r3 = np.sqrt(X**2 + Y**2 + Z**2); self._r3_G = (G, round(h, 6))
            self._ker_cache = {}
        def nuclei(lm):
            k = round(float(lm), 4)
            if k not in self._ker_cache:
                K = np.exp(-self._r3 / max(lm, 1e-6))
                self._ker_cache[k] = (np.fft.fftn(np.fft.ifftshift(K)),
                                      np.fft.fftn(np.fft.ifftshift(K ** 2)))
            return self._ker_cache[k]
        z = np.exp(1j * self.phi)
        if P_LAM == 0.0:
            classi = [(LAM, np.ones(self.n, bool))]
        else:                       # 4 classi di lambda: 4 convoluzioni invece di 1
            li = self.lambda_nodi()
            q = np.quantile(li, [0.25, 0.5, 0.75])
            lab = np.digitize(li, q)
            classi = [(float(np.median(li[lab == k])), lab == k)
                      for k in range(4) if (lab == k).any()]
        F = np.zeros((G, G, G), complex); fondo = np.zeros((G, G, G))
        for lm, m in classi:
            s = np.zeros((G, G, G), complex); n_ = np.zeros((G, G, G))
            im = tuple(a[m] for a in idx)
            np.add.at(s, im, z[m]); np.add.at(n_, im, 1.0)
            kf, k2f = nuclei(lm)
            F += np.fft.ifftn(np.fft.fftn(s) * kf)
            fondo += np.real(np.fft.ifftn(np.fft.fftn(n_) * k2f))
        interf = np.abs(F) ** 2 - fondo                  # SOLO l'interferenza
        s = np.sign(interf) * np.abs(interf) / (1.0 + GAMMA * np.sqrt(np.abs(interf)))
        # --- volumetrico: opacita' dal modulo, colore dal segno ---
        k = 2.5 / max(np.abs(s).max(), 1e-12)
        alpha = 1.0 - np.exp(-k * np.abs(s))
        trasp = np.concatenate([np.ones_like(alpha[:, :, :1]),
                                np.cumprod(1.0 - alpha, axis=2)[:, :, :-1]], axis=2)
        img = (s * trasp).sum(axis=2)                    # con SEGNO
        return img, R, float(np.maximum(interf, 0).sum())   # massa = costruttiva

    def rilassa_disegno(self, it=EMB_IT):
        """le coordinate inseguono le distanze relazionali: la dilatazione si VEDE.
        LEGGE DI SMORZAMENTO: il numero di iterazioni cresce con lo stress della metrica,
        cosi' quando la mitosi corre piu' veloce dell'estensione (stress che diverge) il
        rilassamento si intensifica automaticamente per tenere il passo. Il bilanciamento
        fra creazione e rilassamento e' auto-regolato dallo stato (lo stress stesso),
        indipendentemente da quante volte il chiamante invoca il rilassamento. Non e' un
        tetto: e' un feedback che accelera il rilassamento dove serve."""
        if self.n < 2 or not len(self.i): return
        pos0 = self.pos.copy() if L_CONSERVA else None   # per misurare la rotazione spuria
        for _ in range(it):
            v = self.pos[self.j] - self.pos[self.i]
            L = np.maximum(np.linalg.norm(v, axis=1), 1e-9)
            corr = ((L - self.d) / L)[:, None] * v * 0.5
            acc = np.empty_like(self.pos)      # bincount: ~30x piu' veloce di add.at
            for k in range(3):
                acc[:, k] = (np.bincount(self.i, corr[:, k], minlength=self.n) -
                             np.bincount(self.j, corr[:, k], minlength=self.n))
            acc /= self._deg[:, None]          # MEDIA sui vicini, non somma
            self.pos += EMB_ETA * np.clip(acc, -0.5, 0.5)
        if not np.isfinite(self.pos).all():
            self.pos = np.nan_to_num(self.pos, nan=0.0, posinf=0.0, neginf=0.0)
        self.pos -= self.pos.mean(axis=0)
        if L_CONSERVA and pos0 is not None:
            # CONSERVAZIONE DEL MOMENTO ANGOLARE: il rilassamento fa inseguire le coordinate alla
            # metrica (fisica, si mantiene), ma la media sui vicini introduce una ROTAZIONE RIGIDA
            # spuria (non-centrale) che rompe L. La rimuovo proiettando via la sola rotazione rigida
            # netta dello spostamento, pesata per |Psi|^2 (l'inerzia = materia). NON tocca la
            # deformazione (la metrica che si realizza), solo la rotazione globale parassita.
            self._togli_rotazione_rigida(pos0)

    def _togli_rotazione_rigida(self, pos0):
        """rimuove la rotazione rigida netta introdotta dallo spostamento pos0->pos, pesata per
        l'inerzia |Psi|^2. ITERATIVA: ripete finche' L residuo e' trascurabile (~conservazione
        completa). Conserva il momento angolare senza alterare la deformazione metrica."""
        n = self.n
        if not hasattr(self, "psi") or len(self.psi) < n:
            try: self.calcola_psi()
            except Exception: return
        w = np.abs(self.psi[:n]) ** 2
        if w.sum() < 1e-9: return
        P0 = pos0[:n]
        c = np.average(P0, axis=0, weights=w)      # centro pesato (inerzia), fisso
        r = P0 - c                                  # posizioni rispetto al centro (riferimento)
        I = np.sum(w * (r**2).sum(axis=1)) + 1e-9   # momento d'inerzia (fisso)
        for _ in range(12):                         # itero: la rimozione lineare e' approssimata
            P = self.pos[:n]
            d = P - P0                              # spostamento residuo dal riferimento
            Lz = np.sum(w * (r[:,0]*d[:,1] - r[:,1]*d[:,0]))
            Lx = np.sum(w * (r[:,1]*d[:,2] - r[:,2]*d[:,1]))
            Ly = np.sum(w * (r[:,2]*d[:,0] - r[:,0]*d[:,2]))
            Lnorm = abs(Lz)+abs(Lx)+abs(Ly)
            if Lnorm < 1e-6: break
            oz, ox, oy = Lz/I, Lx/I, Ly/I
            rot = np.empty_like(P)
            rot[:,0] = oy*r[:,2] - oz*r[:,1]
            rot[:,1] = oz*r[:,0] - ox*r[:,2]
            rot[:,2] = ox*r[:,1] - oy*r[:,0]
            self.pos[:n] = P - rot


    def memoria_hebbiana_moto(self):
        """MEMORIA HEBBIANA DELLA DINAMICA — come LEGGE, non parametri.
        Il momento del moto si CONSERVA (inerzia) e viene corretto dal campo (geodetica),
        invece di inseguire una velocita' che il rilassamento azzera. Tutto deriva dallo
        stato del sistema, nessun coefficiente arbitrario:
          - INERZIA = |Psi|^2 del nodo: la massa (interferenza) E' l'inerzia. Piu' materia,
            piu' il moto persiste. Non un numero: la grandezza che gia' esiste.
          - PLASTICITA' = gradiente di torsione locale: dove la geodetica curva (torsione
            che varia), la memoria si lascia correggere; dove il moto e' libero, persiste.
            Le microvariazioni della mitosi asimmetrica sono proprio questo gradiente.
          - CONSERVAZIONE: mem(t+1) = mem(t) + correzione_dal_campo. Il momento si mantiene
            (inerzia hebbiana), la correzione lo piega lungo la geodetica. Cosi' non insegue
            lo zero: genera e protegge il moto, assecondando la curvatura."""
        if not MEM_HEBB or self.n < 2 or not len(self.i):
            return
        n = self.n
        if not hasattr(self, "psi") or len(self.psi) < n:
            self.calcola_psi()
        I = np.abs(self.psi[:n]) ** 2
        Imed = max(float(np.median(I)), 1e-9)
        # uso solo archi i cui due estremi sono nodi validi (< n)
        mask = (self.i < n) & (self.j < n)
        ii, jj = self.i[mask], self.j[mask]
        if len(self.mem_mot) < n:
            self.mem_mot = np.vstack([self.mem_mot, np.zeros((n - len(self.mem_mot), 3))])
        # gradiente di torsione per nodo: la direzione lungo cui la torsione cresce
        # (= la spinta della mitosi asimmetrica = la curvatura della geodetica).
        twabs = np.abs(self.tw)[mask]
        twn = np.zeros(self.n)
        np.add.at(twn, ii, twabs); np.add.at(twn, jj, twabs)
        twn = twn / np.maximum(self._deg, 1)
        v = self.pos[jj] - self.pos[ii]
        L = np.maximum(np.linalg.norm(v, axis=1), 1e-9)
        dirarc = v / L[:, None]
        dtw = (twn[jj] - twn[ii])                          # variazione torsione lungo l'arco
        grad_tw = np.zeros((self.n, 3))                    # gradiente torsione per nodo
        for k in range(3):
            grad_tw[:, k] = (np.bincount(ii, dtw * dirarc[:, k], minlength=self.n) +
                             np.bincount(jj, dtw * dirarc[:, k], minlength=self.n))
        grad_tw /= self._deg[:, None]
        # LEGGE DEL MOMENTO: si conserva, corretto dal gradiente di torsione (geodetica).
        # la plasticita' (quanto il campo corregge) e' |grad_tw| stesso: emerge, non scelta.
        plast = np.tanh(np.linalg.norm(grad_tw, axis=1))[:, None]   # in [0,1), dallo stato
        self.mem_mot[:self.n] = (1.0 - plast) * self.mem_mot[:self.n] + plast * grad_tw
        # INERZIA = |Psi|^2: il momento sposta le d0 in proporzione alla massa del nodo.
        memedge = 0.5 * (self.mem_mot[ii] * (I[ii, None] / Imed) +
                         self.mem_mot[jj] * (I[jj, None] / Imed))
        proj = np.sum(memedge * dirarc, axis=1)
        # CONSERVAZIONE: proj sposta le d0 (traslazione della massa) ma NON deve
        # cambiare la lunghezza totale, altrimenti d0 si gonfia senza limite e le
        # distanze esplodono (feedback divergente sugli archi). Sottraggo la media:
        # cio' che si allunga da un lato si accorcia dall'altro. Il moto SPOSTA la
        # materia, non espande lo spazio. E un tetto per arco impedisce derive locali.
        if len(proj):
            proj = proj - proj.mean()                     # media zero: conserva la lunghezza
            passo_max = 0.01 * float(np.median(self.d0[mask])) if mask.any() else 0.0
            proj = np.clip(proj, -passo_max, passo_max)    # nessuna deriva locale per passo
            self.d0[mask] += proj
            self.d0 = np.maximum(self.d0, 0.05)            # PAVIMENTO: anche il moto non deve
            #   portare d0 sotto la scala minima, o lo stress diverge (stessa causa)
        # LEGGE GRAVITAZIONALE BIFASE (direzione intrinseca). UNA sola legge firmata dalla torsione
        # rispetto al quanto: s = |tw|/PHI_CRIT - 1. Il SEGNO di s E' la direzione (s<0 attrae,
        # s>0 respinge, s=0 equilibrio); il POZZO (somma I/d) da' la scala spaziale; il TWIST
        # firmato ruota il vettore del moto (precessione intrinseca, non attenuazione). Il tetto
        # e' CAUSALE (c*dt, c dalla velocita' del cono = LAM*sqrt(K_C)), non un numero: la
        # stabilita' emerge dalla causalita'. Nessun parametro, ampiezza e direzione dallo stato.
        if GRAV_BIFASE and len(proj):
            s = np.abs(self.tw[mask]) / PHI_CRIT - 1.0    # grandezza FIRMATA: segno = direzione
            phi_g = np.zeros(self.n)                       # pozzo sul grafo (scala spaziale)
            np.add.at(phi_g, ii, I[jj] / L)
            np.add.at(phi_g, jj, I[ii] / L)
            dpozzo = phi_g[jj] - phi_g[ii]
            scala_p = max(float(np.median(np.abs(dpozzo))), 1e-9)
            ampiezza = np.tanh(np.abs(dpozzo) / scala_p)  # scala dal pozzo, in [0,1), dallo stato
            grav = -np.tanh(s) * ampiezza                 # bifase: -s = verso (attrae/respinge), firmato
            # ACCOPPIAMENTO SPIN-ORBITA: il SEGNO viene dallo SPINORE REALE _nb, non dal twist. La
            # proiezione dello spin sulla direzione del pozzo (allineamento spin-gravita') firma
            # l'accoppiamento: spin allineato col pozzo e anti-allineato si accoppiano in verso
            # opposto. Questo e' il segno intrinseco dello spinore reale, non una grandezza imposta.
            # La precessione non e' scritta: emerge da come lo spin (che gia' precede attorno al suo
            # campo) risponde a una geometria modulata dal proprio allineamento.
            if SPINORE and self._nb is not None and len(self._nb) >= self.n:
                # direzione del pozzo nello spazio, per arco: versore da i a j pesato dalla pendenza
                dirp = (self.pos[jj] - self.pos[ii])
                dirp = dirp / np.maximum(np.linalg.norm(dirp, axis=1, keepdims=True), 1e-9)
                # spin dell'arco = media dei Bloch dei due estremi (lo spinore reale)
                spin_arc = 0.5 * (self._nb[ii] + self._nb[jj])
                # PROIEZIONE dello spin reale sulla direzione del pozzo: il segno intrinseco.
                proiez = np.sum(spin_arc * dirp, axis=1) * np.sign(dpozzo)  # allineamento spin-pozzo
                grav = grav * proiez                       # firmato dallo SPINORE REALE (spin-orbita)
            grav = grav - grav.mean()                     # conserva la lunghezza
            c_sistema = LAM * np.sqrt(K_C)                 # velocita' del cono (da LAM, K_C: stato)
            passo_causale = c_sistema * DT                 # TETTO CAUSALE: quanto la causalita' permette
            if VIRIALE:
                # CONVERSIONE VIRIALE (legge, zero parametri): la spinta radiale NON e' additiva
                # (fu il fallimento di K_FRANGE) ma si RIPARTISCE fra cadere e girare. La direzione
                # tangenziale segue la CIRCOLAZIONE ORIENTATA del twist (+tw su i, -tw su j), come
                # FRAME_DRAG: ha curl coerente anche quando tw_mean~0 (il segno grezzo del twist,
                # bilanciato, NON circolava). Pozzo e circolazione normalizzati con lo stesso tanh.
                # theta = atan2(|t_tan|,|r_rad|): cos^2 resta RADIALE (attrazione ridotta), sin^2
                # diventa TANGENZIALE (orbita). cos^2+sin^2=1 -> budget conservato. Dove non c'e'
                # circolazione coerente (circ~0) la conversione tangenziale svanisce da se'.
                twn_a = self.tw[mask] / PHI_CRIT                   # twist adimensionale (come FRAME_DRAG)
                circ_nodo = np.zeros(self.n); grado_c = np.zeros(self.n)
                np.add.at(circ_nodo, ii, twn_a); np.add.at(circ_nodo, jj, -twn_a)  # CIRCOLAZIONE ORIENTATA
                np.add.at(grado_c, ii, 1.0);     np.add.at(grado_c, jj, 1.0)
                circ_nodo = circ_nodo / np.maximum(grado_c, 1.0)
                circ_arc = 0.5 * (circ_nodo[ii] + circ_nodo[jj])  # circolazione orientata per arco (curl)
                r_rad = ampiezza                                  # |pozzo| gia' normalizzato: tanh(|dpozzo|/scala_p)
                t_tan = np.tanh(np.abs(circ_arc))                 # |circolazione orientata| normalizzata, in [0,1)
                H = np.maximum(np.hypot(r_rad, t_tan), 1e-9)      # ipotenusa = budget totale
                cos2 = (r_rad / H) ** 2                            # quota RADIALE (cadere)
                sin2 = (t_tan / H) ** 2                            # quota TANGENZIALE (girare)
                radiale = grav * cos2                              # attrazione ridotta (feedback negativo)
                tangenz = np.abs(grav) * sin2 * np.sign(circ_arc) # verso dalla CIRCOLAZIONE ORIENTATA (coerente)
                spinta = radiale + tangenz
                spinta = spinta - spinta.mean()                   # conserva la lunghezza
                spinta = np.clip(spinta, -passo_causale, passo_causale)
                self.d0[mask] += spinta * float(np.median(self.d0[mask]))
            else:
                grav = np.clip(grav, -passo_causale, passo_causale)
                self.d0[mask] += grav * float(np.median(self.d0[mask]))
            self.d0 = np.maximum(self.d0, 0.05)
        # MOTO LUNGO LE FRANGE: spinta tangenziale lungo il gradiente di fase (le frange
        # rotanti = geodetiche del flusso). Diversamente dal gradiente di torsione (radiale),
        # il flusso di fase e' tangenziale e produce orbita/precessione. Per ogni arco, la
        # differenza di fase pesata dall'intensita' da' il flusso; sposta le d0 lungo di esso.
        if K_FRANGE != 0.0 and len(proj):
            dphi_arc = np.angle(np.exp(1j * (self.phi[jj] - self.phi[ii])))  # flusso di fase
            wI = 0.5 * (I[ii] + I[jj]) / Imed              # peso: intensita' della frangia
            flusso = K_FRANGE * wI * dphi_arc
            flusso = flusso - flusso.mean()                # conserva la lunghezza (come proj)
            flusso = np.clip(flusso, -passo_max, passo_max)
            self.d0[mask] += flusso
            self.d0 = np.maximum(self.d0, 0.05)

    def diagnostica(self):
        I = self.intensita()
        z = np.exp(1j * self.phi)
        w = self._pesi()
        num = np.abs(self._mat(w) @ z)
        den = np.maximum(np.bincount(self.i, w, minlength=self.n) +
                         np.bincount(self.j, w, minlength=self.n), 1e-9)
        return dict(I=I,
                    coer_g=float(abs(z.mean())) if self.n else 0.0,
                    coer_l=float(np.mean(np.clip(num / den, 0, 1))) if self.n else 0.0,
                    picco=float(I.max()) if self.n else 0.0,
                    stress=float(np.median((self.d - self.d0) / np.maximum(self.d0, 1e-9))) if len(self.d) else 0.0,
                    # MEDIANA, non media: lo stress e' |d-d0|/d0 per arco. Pochi archi
                    # patologici (corti a riposo, tesi ora: ~2%) dominano la MEDIA e la
                    # gonfiano a valori enormi, pur essendo outlier. La mediana riflette
                    # lo stress TIPICO del sistema, robusto agli outlier - la fisica vera.
                    dil=float(np.mean(self.d) / max(np.mean(self.d0), 1e-9) - 1) if len(self.d) else 0.0,
                    tw=float(np.abs(self.tw).max()) if len(self.tw) else 0.0,
                    entro=float((self.d <= R_CONN()).mean()) if len(self.d) else 0.0,
                    d_med=float(np.mean(self.d)) if len(self.d) else 0.0)


net = Rete()
net.semina(SEME_INIZIALE)

# ============================================================================
# DEBUG INIT: strumentazione dell'inizializzazione del vuoto. Stampa a console cosa
# sta facendo, timing per fase e metriche calcolate, cosi' si vede DOVE va il tempo
# e cosa produce ogni fase. Attivo/disattivo con la variabile DEBUG_INIT (o la env
# var SOLITON_DEBUG_INIT). Non altera la fisica: solo misura e stampa.
DEBUG_INIT = False

def _dbg_init():
    import time as _t
    _p = lambda *a: (print("[INIT]", *a, flush=True) if DEBUG_INIT else None)
    _p("avvio inizializzazione del vuoto (CICLO COMPLETO = stessa fisica del runtime)")
    _p("leggi attive: SPINORE=%s COMPAT_CHI=%s FRAME_DRAG=%s MEM_HEBB=%s TORS_4PI=%s SCUOTIMENTO=%s"
       % (SPINORE, COMPAT_CHI, FRAME_DRAG, MEM_HEBB, TORS_4PI, SCUOTIMENTO))
    _p("parametri: LAM=%s GAMMA=%s MU_PSI=%s DT=%s SEME_INIZIALE=%s"
       % (LAM, GAMMA, MU_PSI, DT, SEME_INIZIALE))
    _p("nodi iniziali dopo semina: n=%d" % net.n)
    N_PASSI = 300
    t_tot = _t.time()
    # timing per operazione: cosi' si vede DOVE va il tempo nel ciclo completo
    acc = dict(scuoti=0.0, step=0.0, mitosi=0.0, rilassa=0.0, hebb=0.0)
    for k in range(N_PASSI):
        # CICLO COMPLETO identico al runtime (update): stessa fisica, stesse leggi, stesso ordine.
        t0 = _t.time(); scuoti_vuoto(net);           acc["scuoti"]  += _t.time() - t0
        t0 = _t.time(); net.step();                  acc["step"]    += _t.time() - t0
        t0 = _t.time(); net.mitosi();                acc["mitosi"]  += _t.time() - t0
        t0 = _t.time(); net.rilassa_disegno();       acc["rilassa"] += _t.time() - t0
        t0 = _t.time(); net.memoria_hebbiana_moto(); acc["hebb"]    += _t.time() - t0
        if DEBUG_INIT and (k % 20 == 19 or k == 0):
            try:
                d = net.diagnostica()
                sp = 0.0
                if hasattr(net, "_nb") and net._nb is not None and len(net._nb):
                    mm = min(len(net._nb), net.n)
                    sp = float(np.mean(np.arccos(np.clip(net._nb[:mm, 2], -1, 1))))
                el = _t.time() - t_tot
                _p("passo %3d/%d | %.1fs (%.1fms/passo) | nodi=%d archi=%d | olonomia=%.1f "
                   "stress=%.1f%% dilat=%+.1f%% coer_g=%.3f coer_l=%.3f spin=%.2f"
                   % (k + 1, N_PASSI, el, 1000 * el / (k + 1), net.n, len(net.i),
                      d.get("tw", 0), 100 * d.get("stress", 0), 100 * d.get("dil", 0),
                      d.get("coer_g", 0), d.get("coer_l", 0), sp))
            except Exception as e:
                _p("passo %d: errore diagnostica: %s" % (k + 1, e))
    t0 = _t.time(); net.rilassa_disegno(30); t_rilassa_fin = _t.time() - t0
    tot = _t.time() - t_tot
    _p("--- inizializzazione completata in %.1fs ---" % tot)
    _p("ripartizione tempo: scuoti=%.1fs (%.0f%%) step=%.1fs (%.0f%%) mitosi=%.1fs (%.0f%%) "
       "rilassa=%.1fs (%.0f%%) hebb=%.1fs (%.0f%%) | rilassa_finale(30)=%.1fs"
       % (acc["scuoti"], 100 * acc["scuoti"] / max(tot, 1e-9),
          acc["step"], 100 * acc["step"] / max(tot, 1e-9),
          acc["mitosi"], 100 * acc["mitosi"] / max(tot, 1e-9),
          acc["rilassa"], 100 * acc["rilassa"] / max(tot, 1e-9),
          acc["hebb"], 100 * acc["hebb"] / max(tot, 1e-9), t_rilassa_fin))
    _p("stato finale: nodi=%d archi=%d archi/nodo=%.1f" % (net.n, len(net.i), len(net.i) / max(net.n, 1)))

if False:
    _dbg_init()
else:
    # CICLO COMPLETO = stessa fisica del runtime (update): il vuoto nasce con TUTTE le leggi,
    # nello stesso ordine con cui poi evolve. Identico al ramo debug, senza le stampe.
    pass
# ============================================================================

stato = dict(nframe=0, pausa=False, zoom=1.0, R=0.0, vmax=None, massa0=None,
             giri=1.0, durata=600,      # un giro completo sulla durata della scena
             passi_frame=6,             # PASSI di motore per frame: rende l'evoluzione visibile
             denoise=False,             # filtro anti-ribollio nel rendering (switch)
             theta=0.0, elev=0.28,      # angolo ACCUMULATO: si puo' fermare e riprendere
             rot_auto=False, gabbia=True, trascina=None,   # fermi: si ruota a mano
             piazza=None,               # modalita' piazzamento: None | 'materia' | 'buconero'
             passo_semina=100, semina_cont=False, ogni=30,
             bigbang=False, bigbang_drif=None, bigbang_ttmin=18.0, bigbang_ttmax=32.0,
             num_masse=1, raggio_semina=3.0, pozzo_scala=None)


def matrice_vista(theta, phi_v=0.28):
    """rotazione della VISTA: si ruotano i punti, non la griglia (costa nulla)"""
    ct, st = np.cos(theta), np.sin(theta)
    cp, sp = np.cos(phi_v), np.sin(phi_v)
    return (np.array([[ct, 0, st], [0, 1, 0], [-st, 0, ct]]) @
            np.array([[1, 0, 0], [0, cp, -sp], [0, sp, cp]])).T


def angolo_vista():
    """angolo ACCUMULATO: avanza solo se la rotazione automatica e' attiva,
    cosi' si puo' fermare, riprendere e ruotare a mano senza salti"""
    return stato["theta"]


def avanza_vista():
    if stato["rot_auto"]:
        stato["theta"] += 2 * np.pi * stato["giri"] / max(stato["durata"], 1)


def bussola(ax, R, M, scala=0.13):
    """Indicatore d'assi nel MARGINE, non sopra il campo.
    La gabbia a fil di ferro che c'era prima disegnava righe grigie in mezzo
    all'immagine — decorazione confondibile con struttura, per giunta sopra la
    materia. Qui il riferimento di rotazione resta, ma fuori dai dati."""
    from matplotlib.collections import LineCollection
    o = np.array([-R * 1.02, -R * 1.02])
    L = R * scala
    assi = np.eye(3) * L
    seg, col = [], []
    for k, cl in enumerate(("#c0392b", "#27ae60", "#2980b9")):    # x, y, z
        p = (assi[k] @ M)[:2]
        seg.append([tuple(o), tuple(o + p)]); col.append(cl)
    ax.add_collection(LineCollection(seg, colors=col, linewidths=1.2, alpha=0.7, zorder=6))



def _accresci(cx, r, n, fase):
    """versa puntatori coerenti in una regione: la massa si RICOMPONE la',
    e il suo centro migra (Legge XVI). Nessun trasporto, nessuna forza."""
    net.semina(n, raggio=r, centro=(cx, 0.0, 0.0), fase=fase)


test = dict(nome=None, fase=0, timer=0, cap="", dati={})


def _massa(cx, r, n, fase, etichetta=None):
    """crea un dominio coerente e ne REGISTRA la coorte, per poterlo misurare.
    cx puo' essere un numero (coordinata x, centro sull'asse) o una terna/array (x,y,z)."""
    base = net.n
    centro = (float(cx), 0.0, 0.0) if np.isscalar(cx) else tuple(np.asarray(cx, float)[:3])
    net.semina(n, raggio=r, centro=centro, fase=fase)
    if etichetta:
        idx = np.arange(base, net.n)
        test["dati"].setdefault("coorti", {})[etichetta] = idx
        test["dati"].setdefault("E0", {})[etichetta] = None


# --- N MASSE nel video: disposte in cerchio, con lo zoom che segue lo scaling dello spazio ---
_NMASSE_VIDEO = {"n": 4, "sep": 3.0, "size": None}   # riempiti da esegui_headless via --nmasse/--sep/--size

def _n_masse_video(): return int(_NMASSE_VIDEO["n"])
def _sep_video():     return float(_NMASSE_VIDEO["sep"])
def _size_video(k, default):
    """Dimensione (raggio) dell'oggetto k-esimo, da --size s1,s2,... se fornito, altrimenti il
    default della scena. Se --size ha meno valori di k, usa l'ultimo fornito."""
    sizes = _NMASSE_VIDEO.get("size")
    if not sizes:
        return float(default)
    return float(sizes[k]) if k < len(sizes) else float(sizes[-1])

def _semina_fila_radiale():
    """1 massa CENTRALE grande (raggio 3) + 5 masse (raggio 1) in FILA lungo l'asse x, ai centri
    6, 10, 14, 18, 22 (passo R+3 fra le superfici). Sistema tipo 'raggio' radiale."""
    Nc = massa_critica_collasso()
    # massa centrale grande: raggio 3, piu' nodi (scala col volume ~ raggio^3)
    _massa((0.0, 0.0, 0.0), _size_video(0, 3.0), int(Nc * 1.4), 0.0, "centrale")
    # 5 masse raggio 1 in fila lungo x
    for k_fila, cx in enumerate((6.0, 10.0, 14.0, 18.0, 22.0)):
        _massa((cx, 0.0, 0.0), _size_video(k_fila+1, 1.0), int(Nc * 0.4), 0.0, "m_%d" % int(cx))


def _semina_buco_nero():
    """1 massa CENTRALE grande (buco nero) + 10 masse attorno a distanza >=4, in cerchio.
    Le masse esterne non toccano il centro (raggio orbitale 4.5)."""
    npunt = int(massa_critica_collasso() * 0.35)   # masse satellite piu' piccole (performance)
    # buco nero centrale: piu' massiccio per dominare il pozzo
    _massa((0.0, 0.0, 0.0), 0.9, int(massa_critica_collasso()*0.9), 0.0, "buco_nero")
    # 10 masse attorno, a raggio 4.5 (>4 dal centro), in cerchio
    R = 4.5
    for k in range(10):
        ang = 2*np.pi*k/10
        centro = (R*np.cos(ang), R*np.sin(ang), 0.0)
        _massa(centro, _size_video(k+1, 0.6), npunt, 0.0, "sat_%d" % k)


def _semina_n_masse():
    """semina N masse coerenti in cerchio di raggio sep attorno all'origine. Il numero e il raggio
    vengono da --nmasse/--sep. L'inquadratura del rendering si adatta gia' all'estensione dei nodi
    (R = max|pos|), quindi lo zoom SEGUE lo scaling dello spazio senza intervento manuale."""
    nm = _n_masse_video(); sep = _sep_video()
    npunt = int(massa_critica_collasso() * 0.8)
    for k in range(nm):
        ang = 2*np.pi*k/nm
        centro = (sep*np.cos(ang), sep*np.sin(ang), 0.0)
        _massa(centro, _size_video(k, 0.7), npunt, 0.0, "massa_%d" % k)


def _energia(etichetta):
    """energia d'interferenza della coorte, normalizzata al suo valore iniziale"""
    co = test["dati"].get("coorti", {}).get(etichetta)
    if co is None or not len(co) or co.max() >= net.n: return float("nan")
    E = float(net.intensita()[co].sum())
    E0 = test["dati"]["E0"].get(etichetta)
    if E0 is None or E0 == 0:
        test["dati"]["E0"][etichetta] = max(E, 1e-9); return 1.0
    return E / E0



def _crea_masse_casuali(num_m, tipo="materia"):
    """Crea masse casuali non sovrapposte. Il numero di puntatori per massa e'
    fissato DALLA LEGGE della densita' critica, non a mano:
      - tipo 'materia'  -> sotto N_c: materia strutturata a gusci (regime lento-ma-scorre)
      - tipo 'buconero' -> sopra N_c: oltre la soglia, collassa nel regime omogeneo
    N_c = massa_critica_collasso(LAM, GAMMA) e' calcolata dalle costanti correnti."""
    test.clear(); test.update(nome=None, fase=0, timer=0, cap="", dati={})
    rng = net.rng; centri = []
    Nc = massa_critica_collasso()
    if tipo == "buconero":
        n_punt = int(Nc * 1.8)      # ben oltre la soglia -> collasso garantito
    else:
        n_punt = int(Nc * 0.45)     # sotto la soglia -> materia strutturata
    min_d = max(2.5 * stato["raggio_semina"], 4.0)
    for k in range(num_m):
        for _ in range(100):
            u = rng.normal(size=3); u /= np.linalg.norm(u)
            c_pos = u * (_scala_sistema() * 0.35) * (rng.random() ** (1/3))
            if all(np.linalg.norm(c_pos - ce) >= min_d for ce in centri) or not centri:
                centri.append(c_pos); break
        else:
            c_pos = np.array([k*3.0 - num_m*1.5, 0.0, 0.0]); centri.append(c_pos)
        et = ("buconero_" if tipo == "buconero" else "massa_") + str(k+1)
        _massa(c_pos, stato["raggio_semina"], n_punt, 0.0, etichetta=et)  # fase compatibile: le masse devono coesistere, non annichilarsi

TESTS = {
 "VUOTO": [
   dict(cap="VUOTO 1/2 — solo puntatori scorrelati: nessuna materia stabile.\n"
            "Le interferenze fluttuano senza mai addensarsi", dur=110),
   dict(cap="VUOTO 2/2 — il vuoto respira ma NON deriva: con le onde sulla\n"
            "deformazione, a riposo la geometria e' immobile per costruzione", dur=110)],
 "LIBERO": [
   dict(cap=lambda: f"OSSERVAZIONE LIBERA 1/6 — il sistema intero, senza interventi. "
                    f"puntatori {net.n}, archi {len(net.i)}", dur=250),
   dict(cap=lambda: f"2/6 — coerenza globale {net.diagnostica()['coer_g']:.3f}, "
                    f"locale {net.diagnostica()['coer_l']:.3f}; d medio {net.diagnostica()['d_med']:.3f}",
        dur=250),
   dict(cap=lambda: f"3/6 — dilatazione {100*net.diagnostica()['dil']:+.1f}%, "
                    f"stress {100*net.diagnostica()['stress']:+.2f}%: la geometria si assesta?",
        dur=250),
   dict(cap=lambda: f"4/6 — torsione max {net.diagnostica()['tw']:.1f}/{PHI_CRIT:.1f}; "
                    f"mitosi {net.nati}", dur=250),
   dict(cap=lambda: f"5/6 — picco |Psi|² {net.diagnostica()['picco']:.1f}; "
                    f"la materia si organizza in strutture stabili?", dur=250),
   dict(cap=lambda: f"6/6 — bilancio: d medio {net.diagnostica()['d_med']:.3f}, "
                    f"coerenza locale {net.diagnostica()['coer_l']:.3f}, mitosi {net.nati}",
        dur=250)],
 "MASSA": [
   dict(cap="MASSA 1/3 — nasce un dominio COERENTE dentro il vuoto (sotto N_c)",
        al_via=lambda: _massa(0.0, _size_video(0, 1.5), int(massa_critica_collasso()*0.45), 0.0, "massa"), dur=120),
   dict(cap="MASSA 2/3 — la materia si addensa dove le fasi si accordano", dur=140),
   dict(cap=lambda: f"MASSA 3/3 — dilatazione {100*net.diagnostica()['dil']:+.1f}%: "
                    "il pozzo relazionale attorno alla materia", dur=140)],
 "BUCO NERO": [
   dict(cap="BUCO NERO 1/3 — dominio OLTRE la densita' critica N_c",
        al_via=lambda: _massa(0.0, _size_video(0, 1.2), int(massa_critica_collasso()*1.8), 0.0, "buconero"), dur=120),
   dict(cap="BUCO NERO 2/3 — oltre soglia i gusci si omogeneizzano: la materia collassa", dur=140),
   dict(cap=lambda: f"BUCO NERO 3/3 — coerenza uniforme {net.diagnostica()['coer_l']:.3f}: "
                    "il regime omogeneo, i gusci annullati", dur=140)],
 "BIG BANG": [
   dict(cap="BIG BANG 1/4 — evento iniziale denso e CALDO: l'universo si accende",
        al_via=lambda: _big_bang(calore=0.5, punti=1500), dur=60),
   dict(cap=lambda: f"BIG BANG 2/4 — creazione di materia (nodi {net.n}): la mitosi genera",
        dur=140),
   dict(cap=lambda: f"BIG BANG 3/4 — espansione e diluizione: TAU_TW cala, "
                    f"la generazione rallenta (nodi {net.n})", dur=200),
   dict(cap=lambda: f"BIG BANG 4/4 — universo assestato con la materia creata "
                    f"(nodi {net.n}, dil. {100*net.diagnostica()['dil']:+.0f}%)", dur=220)],
 "SISTEMA": [
   dict(cap="1/5 — BUCO NERO massiccio al centro (3x N_c)",
        al_via=lambda: _massa((0.0,0.0,0.0), 1.6, int(massa_critica_collasso()*3.0), 0.0, "buconero"),
        dur=110),
   dict(cap="2/5 — tre MASSE strutturate poste LONTANE, ben separate",
        al_via=lambda: [_massa(p, 0.8, int(massa_critica_collasso()*0.35), f, "massa_%d"%k)
                        for k,(p,f) in enumerate([((5.2,0.6,0.0),0.4),
                                                  ((-3.0,4.4,0.5),1.9),
                                                  ((-2.6,-4.6,-0.6),3.3)])],
        dur=140),
   dict(cap="3/5 — il campo d'interferenza si tende FRA le masse e il centro",
        dur=200),
   dict(cap=lambda: f"4/5 — deformazione del campo: dilatazione {100*net.diagnostica()['dil']:+.1f}%, "
                    f"stress {100*net.diagnostica().get('stress',0):+.1f}%",
        dur=200),
   dict(cap=lambda: f"5/5 — evoluzione lunga: come si deforma il campo fra i corpi "
                    f"(coerenza {net.diagnostica()['coer_l']:.2f})",
        dur=260)],
 "DUE-MASSE": [
   dict(cap="DUE MASSE 1/3 — prima massa coerente (0.8x N_c) a sinistra",
        al_via=lambda: _massa(-_sep_video(), _size_video(0, 0.7), int(massa_critica_collasso()*0.8), 0.0, "massaA"), dur=15),
   dict(cap="DUE MASSE 2/3 — seconda massa (0.8x N_c) a destra, vicina ma non unita",
        al_via=lambda: _massa(_sep_video(), _size_video(1, 0.7), int(massa_critica_collasso()*0.8), 0.0, "massaB"), dur=15),
   dict(cap=lambda: f"DUE MASSE 3/3 — frame-dragging attivo: osservare se la congiungente "
                    f"ruota (precessione) e se i solitoni corrono lungo le geodetiche",
        dur=220)],
 "N-MASSE": [
   dict(cap=lambda: f"N MASSE 1/2 — {_n_masse_video()} masse in cerchio (raggio {_sep_video():.1f}), "
                    f"ben separate; lo zoom segue lo scaling dello spazio",
        al_via=lambda: _semina_n_masse(), dur=120),
   dict(cap=lambda: f"N MASSE 2/2 — evoluzione libera: condensazione fra le masse e guscio esterno; "
                    f"coerenza {net.diagnostica()['coer_l']:.2f}, dilatazione {100*net.diagnostica()['dil']:+.1f}%",
        dur=280)],
 "TERRA-BUCONERO": [
   dict(cap="1/4 — un oggetto COLLASSATO (2.5x N_c): il 'buco nero'",
        al_via=lambda: _massa(-2.2, _size_video(0, 1.5), int(massa_critica_collasso()*2.5), 0.0, "buconero"), dur=110),
   dict(cap="2/4 — una piccola MASSA strutturata (0.12x N_c): la 'Terra', a distanza",
        al_via=lambda: _massa(3.0, _size_video(1, 0.7), int(massa_critica_collasso()*0.12), 0.0, "terra"), dur=130),
   dict(cap="3/4 — i rapporti coi rispettivi N_c sono dalla legge di densita' critica",
        dur=150),
   dict(cap=lambda: f"4/4 — la massa presso l'oggetto collassato "
                    f"(dil. tempo {100*net.diagnostica()['dil']:+.1f}%): rappresentazione qualitativa",
        dur=170)],
 "TERRA-SOLE": [
   dict(cap="TERRA-SOLE 1/4 — un oggetto grande e coerente (il 'Sole'): massa "
            "strutturata sotto N_c, al centro",
        al_via=lambda: _massa(0.0, _size_video(0, 1.6), int(massa_critica_collasso()*0.8), 0.0, "sole"), dur=120),
   dict(cap="TERRA-SOLE 2/4 — un piccolo oggetto (la 'Terra') a distanza orbitale, "
            "nato con una spinta di fase tangenziale",
        al_via=lambda: _massa(4.0, _size_video(1, 0.6), int(massa_critica_collasso()*0.15), 0.0, "terra"), dur=150),
   dict(cap="TERRA-SOLE 3/4 — con il coarse-graining (avvia con --scala) l'orbita "
            "vive a piu' lunghezze d'onda: la gravita' compete con l'espansione",
        dur=170),
   dict(cap=lambda: f"TERRA-SOLE 4/4 — moto della 'Terra' presso il 'Sole' "
                    f"(dil. tempo {100*net.diagnostica()['dil']:+.1f}%): "
                    f"osservare se orbita, cade o si allontana", dur=200)],
 "URTO": [
   dict(cap="URTO 1/4 — una massa coerente si assesta nel vuoto relazionale",
        al_via=lambda: _massa(0.0, _size_video(0, 1.5), 420, 0.0, "massa"), dur=120),
   dict(cap="URTO 2/4 — CARTUCCIA densa in anti-fase accanto alla massa",
        al_via=lambda: (test["dati"].__setitem__("d0", net.diagnostica()["d_med"]),
                        _massa(2.6, _size_video(1, 0.9), 320, np.pi, "cartuccia")), dur=150),
   dict(cap=lambda: f"URTO 3/4 — la geometria si dilata: d medio "
                    f"{net.diagnostica()['d_med']:.2f} (era {test['dati'].get('d0', 0):.2f}).  "
                    f"materia: massa x{_energia('massa'):.2f}  cartuccia x{_energia('cartuccia'):.2f}",
        dur=150),
   dict(cap=lambda: f"URTO 4/4 — esito MISURATO: massa x{_energia('massa'):.2f}, "
                    f"cartuccia x{_energia('cartuccia'):.2f} rispetto all'inizio.  "
                    f"I puntatori restano tutti {net.n}; mitosi {net.nati}", dur=110)],
 "SCONTRO": [
   dict(cap="SCONTRO 1/4 — due masse coerenti nascono lontane, nel vuoto",
        al_via=lambda: (_massa(-3.0, _size_video(0, 1.2), 320, 0.0, "A"),
                        _massa(3.0, _size_video(1, 1.2), 320, 0.0, "B")), dur=120),
   dict(cap="SCONTRO 2/4 — ACCRESCIMENTO fra le due: ciascuna riceve materiale\n"
            "coerente dal lato interno (Legge XVI). Nessuna forza, nessun trasporto",
        al_via=lambda: (_accresci(-1.6, 0.9, 200, 0.0), _accresci(1.6, 0.9, 200, 0.0)),
        dur=140),
   dict(cap="SCONTRO 3/4 — i centri MIGRANO verso l'interno per ricomposizione\n"
            "della coerenza: la materia si sposta senza che i puntatori si muovano",
        al_via=lambda: (_accresci(-0.7, 0.8, 180, 0.0), _accresci(0.7, 0.8, 180, 0.0)),
        dur=140),
   dict(cap=lambda: f"SCONTRO 4/4 — incontro: materia A x{_energia('A'):.2f}, "
                    f"B x{_energia('B'):.2f}; d medio {net.diagnostica()['d_med']:.2f}",
        dur=130)],
 "FILA RADIALE": [
   dict(cap="FILA RADIALE — massa centrale R3 e 5 masse R1 in fila (centri 6,10,14,18,22)",
        al_via=_semina_fila_radiale, dur=200),
   dict(cap="FILA RADIALE — evoluzione libera: le masse cadono, restano, o si espandono?", dur=300),
   dict(cap=lambda: f"FILA RADIALE — d medio {net.diagnostica()['d_med']:.2f}; "
                    "osservare il campo fra centrale e satelliti (la luna) e le posizioni (il dito)", dur=400)],
 "TRE MASSE D3": [
   dict(cap="TRE MASSE — triangolo a distanza 3, tutte le leggi + momento angolare fisico",
        al_via=lambda: (_massa((0.0, 3.0, 0.0), _size_video(0, 0.7), int(massa_critica_collasso()*0.6), 0.0, "A"),
                        _massa((-2.6, -1.5, 0.0), _size_video(1, 0.7), int(massa_critica_collasso()*0.6), 0.0, "B"),
                        _massa((2.6, -1.5, 0.0), _size_video(2, 0.7), int(massa_critica_collasso()*0.6), 0.0, "C")), dur=200),
   dict(cap="TRE MASSE — l'interferenza si accumula nello spazio fra le masse (la luna)", dur=250),
   dict(cap=lambda: f"TRE MASSE — d medio {net.diagnostica()['d_med']:.2f}; "
                    "il campo comune al centro cresce prima che le masse si muovano", dur=300)],
 "BUCO NERO": [
   dict(cap="BUCO NERO — 1 massa centrale e 10 masse attorno a distanza 4.5",
        al_via=_semina_buco_nero, dur=150),
   dict(cap="BUCO NERO — le masse esterne rispondono al pozzo centrale", dur=170),
   dict(cap=lambda: f"BUCO NERO — d medio {net.diagnostica()['d_med']:.2f}; "
                    "momento angolare conservato: evoluzione orbitale attorno al centro", dur=200)],
 "DUE MASSE": [
   dict(cap="DUE MASSE 1/3 — due domini coerenti fra loro, affiancati",
        al_via=lambda: (_massa(-_sep_video(), _size_video(0, 1.2), 320, 0.0, "A"), _massa(_sep_video(), _size_video(1, 1.2), 320, 0.0, "B")), dur=130),
   dict(cap="DUE MASSE 2/3 — le interferenze si cercano nello spazio fra loro", dur=150),
   dict(cap=lambda: f"DUE MASSE 3/3 — d medio {net.diagnostica()['d_med']:.2f}; "
                    f"materia A x{_energia('A'):.2f}, B x{_energia('B'):.2f}: "
                    "si attraggono, o la geometria si limita a dilatarsi?", dur=150)],
 "ANTIFASE": [
   dict(cap="ANTIFASE 1/2 — due domini in OPPOSIZIONE di fase",
        al_via=lambda: (_massa(-_sep_video(), _size_video(0, 1.2), 320, 0.0, "A"), _massa(_sep_video(), _size_video(1, 1.2), 320, np.pi, "B")), dur=140),
   dict(cap=lambda: "ANTIFASE 2/2 — misura: dominio A x%.2f, dominio B x%.2f.\n"
                    "Dove le fasi si oppongono l'interferenza si cancella, "
                    "benche' i puntatori ci siano tutti" % (_energia("A"), _energia("B")), dur=170)],
 "TERRA-BH": [
   dict(cap="TERRA presso BUCO NERO 1/4 — a sinistra materia strutturata (sotto N_c), "
            "a destra un oggetto collassato (oltre N_c). Rapporti dalla legge di densita' critica.",
        al_via=lambda: (_massa(-3.0, _size_video(0, 0.9), int(0.45*massa_critica_collasso()), 0.0, "terra"),
                        _massa(2.2, _size_video(1, 1.6), int(1.8*massa_critica_collasso()), 0.0, "bh")), dur=140),
   dict(cap="TERRA presso BUCO NERO 2/4 — la materia mantiene i suoi gusci; "
            "il collasso si omogeneizza in un blocco coerente", dur=150),
   dict(cap=lambda: f"TERRA presso BUCO NERO 3/4 — pozzo del collassato molto piu' profondo; "
                    f"la materia (x{_energia('terra'):.2f}) sente la geometria del buco nero (x{_energia('bh'):.2f})", dur=150),
   dict(cap=lambda: f"TERRA presso BUCO NERO 4/4 — d medio {net.diagnostica()['d_med']:.2f}; "
                    "la materia strutturata cade nella deformazione del vuoto attorno al collassato", dur=160)],
}


def avvia_test(nome):
    def _f(_=None):
        if test["nome"] == nome: ferma_test(); return
        test.update(nome=nome, fase=0, timer=0, dati={})
        stato["durata"] = sum(f.get("dur", 150) for f in TESTS[nome])
        f0 = TESTS[nome][0]
        if f0.get("al_via"): f0["al_via"]()
        test["cap"] = f0["cap"]() if callable(f0["cap"]) else f0["cap"]
    return _f


def ferma_test(): test.update(nome=None)   # l ultima didascalia resta a schermo


def passo_test():
    if not test["nome"]: return
    test["timer"] += 1
    fs = TESTS[test["nome"]]; f = fs[test["fase"]]
    if f.get("dur") and test["timer"] >= f["dur"]:
        test["fase"] += 1; test["timer"] = 0
        if test["fase"] >= len(fs):
            # lo scenario finisce, la SIMULAZIONE NO: prosegue in evoluzione libera
            test.update(nome=None)
            test["cap"] = (test["cap"].split("\n")[0] + "  —  scenario concluso, "
                           "evoluzione libera in corso")
            return
        f = fs[test["fase"]]
        if f.get("al_via"): f["al_via"]()
    test["cap"] = f["cap"]() if callable(f["cap"]) else f["cap"]


fig = plt.figure(figsize=(17.5, 7.6), facecolor="none")
_y0 = 0.135 if "--test" not in _sys.argv else 0.03      # spazio per i bottoni: interattivo sì, video no
ax  = fig.add_axes([0.205, _y0, 0.34, 0.79 - _y0 + 0.02])
ax3d = fig.add_axes([0.55, _y0, 0.22, 0.79 - _y0 + 0.02], projection='3d')
ax2 = fig.add_axes([0.785, _y0 + 0.13, 0.21, 0.46])
axt = fig.add_axes([0.005, _y0, 0.195, 0.81 - _y0]); axt.axis("off")
axc = fig.add_axes([0.205, 0.90, 0.79, 0.09]); axc.axis("off")


def update(frame):
    if stato["pausa"]: return
    stato["nframe"] += 1
    # BIG BANG IBRIDO: se attivo, TAU_TW si accoppia alla densita' del sistema.
    # Denso/caldo (evento iniziale) -> TAU_TW alto -> la mitosi si accende e genera
    # materia. Diluito (dopo espansione) -> TAU_TW cala -> la generazione si spegne
    # da se'. Cosi' l'evento iniziale accende la creazione, e l'espansione la calma:
    # un ciclo cosmologico auto-consistente. L'idea e' di Luca (il Big Bang che tara
    # la mitosi per la semina). Attivo solo in modalita' bigbang; altrove TAU_TW e'
    # la costante normale.
    if stato.get("bigbang"):
        import soliton_simulator as _self  # per riscrivere la globale TAU_TW
        V = float(net.d0.sum()) if len(net.d0) else 1.0
        dens = net.n / max(V, 1e-9)
        d_rif = stato.get("bigbang_drif", dens) or dens
        dn = np.clip(dens / d_rif, 0.0, 1.0)
        globals()["TAU_TW"] = stato["bigbang_ttmin"] + \
            (stato["bigbang_ttmax"] - stato["bigbang_ttmin"]) * dn
    if stato["semina_cont"] and stato["nframe"] % max(stato["ogni"], 1) == 0:
        net.semina(stato["passo_semina"])       # accrescimento continuo del vuoto
    passo_test()
    # PASSI PER FRAME: piu' passi di motore per ogni frame renderizzato, cosi' l'evoluzione
    # (lenta, DT piccolo) diventa VISIBILE. Non cambia la fisica: fa la stessa identica cosa
    # del runtime, solo che ne condensa PASSI_PER_FRAME in un frame invece di uno. Interruttore
    # regolabile (stato['passi_frame']); il passo_test/scuotimento restano una volta per frame.
    _npf = max(1, int(stato.get("passi_frame", PASSI_PER_FRAME)))
    for _ip in range(_npf):
        scuoti_vuoto(net)      # LEGGE DELLO SCUOTIMENTO LOCALE: il vuoto ribolle e
                               # genera materia stocasticamente ai bordi morbidi. Sempre attiva.
        net.step(); net.mitosi(); net.rilassa_disegno()
        net.memoria_hebbiana_moto()  # MEMORIA HEBBIANA DEL MOTO: inerzia plastica, segue geodetiche
    dg = net.diagnostica()
    ax.clear(); ax3d.clear(); ax2.clear(); axt.clear(); axt.axis("off"); axc.clear(); axc.axis("off")

    # ---------- PANNELLO SINISTRO: LA MATERIA ----------
    # Il campo d'interferenza nello spazio, |Psi(x)|^2, RICALCOLATO a ogni passo.
    # Non i puntatori (sarebbe il dito colorato con la luce della luna) e non gli
    # archi (dove l'interferenza si annulla i legami ci sono comunque): la materia
    # e' cio' che sopravvive all'annullamento delle fasi, e vive FRA i puntatori.
    # Inquadratura MONOTONA e scala di colore ANCORATA ai primi fotogrammi, cosi'
    # dilatazione e diluizione si vedono invece di essere rinormalizzate via.
    # l'inquadratura cresce A SCATTI e non si restringe mai: se cambiasse a
    # ogni fotogramma cambierebbe il passo della griglia, invalidando la cache
    # del kernel 3D (un meshgrid 72^3 e la sua FFT ricalcolati ogni volta).
    # INQUADRATURA ADATTIVA. R deve contenere sia le POSIZIONI dei nodi sia l'estensione del CAMPO
    # (le code del kernel si estendono oltre i nodi di ~alcuni lambda). Quando una massa nasce di
    # colpo a un raggio grande, R deve espandersi SUBITO e con margine sufficiente, altrimenti la
    # massa sfora il pannello per qualche frame (artefatto ai bordi). Uso il percentile 99.5 delle
    # distanze (robusto ai singoli nodi sparati lontano) piu' un cuscinetto per le code del campo.
    if net.n > 0:
        d_nodi = np.linalg.norm(net.pos, axis=1)
        r_nodi = float(np.percentile(d_nodi, 99.5)) if net.n > 4 else float(d_nodi.max())
        coda_campo = 2.0 * LAM * _scala_sistema()   # code del kernel oltre i nodi
        Rn = (r_nodi + coda_campo) * 1.12 + 1e-6
    else:
        Rn = 1e-6
    if Rn > stato["R"]:
        stato["R"] = Rn * 1.15          # espansione immediata alla nascita, margine 15%
    else:
        stato["R"] += (Rn - stato["R"]) * 0.05   # contrazione lenta verso l'estensione reale
    avanza_vista()
    M = matrice_vista(angolo_vista(), stato["elev"])   # stessa vista per i due pannelli
    Rv = stato["R"] / max(stato["zoom"], 1e-3)         # zoom: inquadratura effettiva
    campo, R, massa3d = net.campo_spaziale(mezzo=Rv, M=M)
    # SCALA COLORE ADATTIVA CON MEMORIA. Il contrasto si ritara sul contesto (cosi' la
    # materia si vede bene in ogni dinamica), ma con memoria: la scala SALE subito quando
    # serve piu' gamma (comparsa di un oggetto intenso) e SCENDE lentamente, cosi' non si
    # perde il senso dell'evoluzione (una scala ri-normalizzata a ogni frame cancellerebbe
    # la crescita/diluizione della materia). Percentile 99 invece del massimo: ignora i
    # pochi pixel di picco che schiaccerebbero tutto il resto.
    picco_ctx = float(np.percentile(np.abs(campo), 99)) if campo.size else 1.0
    picco_ctx = max(picco_ctx, 1e-9)
    if stato["nframe"] <= 25:
        stato["vmax"] = max(stato["vmax"] or 0.0, picco_ctx)   # ancoraggio iniziale
    else:
        vprec = stato["vmax"] or picco_ctx
        # sale subito (0.5), scende piano (0.02): adattivo ma con memoria dell'evoluzione
        tasso = 0.5 if picco_ctx > vprec else 0.02
        stato["vmax"] = vprec + tasso * (picco_ctx - vprec)
    vm = max(stato["vmax"] or 1.0, 1e-9)
    q = np.clip(campo.T / vm, -1, 1)
    # gamma di RENDERING adattiva: quando in scena c'e' forte squilibrio di intensita'
    # (oggetto intenso + corpi deboli) l'esponente scende per sollevare i deboli; quando
    # la dinamica e' uniforme risale, per non appiattire. Deriva dal contrasto stesso.
    contrasto = float(np.abs(q).mean()) if q.size else 0.3
    gamma_rend = float(np.clip(0.30 + 0.5 * contrasto, 0.30, 0.60))  # adattivo, dallo stato
    q = np.sign(q) * np.abs(q) ** gamma_rend      # compressione, segno conservato
    # SOLO MATERIA (--solo-materia): nasconde il guscio ciano (interferenza distruttiva, q<0) per
    # rivelare i nuclei di materia accesa (fuoco, q>0) che il guscio avvolge e nasconde. Azzera i
    # valori negativi: il ciano diventa nero (nulla), resta solo la materia costruttiva. Filtro di
    # VISUALIZZAZIONE, non tocca la fisica: mostra i nuclei dentro i gusci.
    if stato.get("solo_materia", False):
        q = np.clip(q, 0, 1)      # taglia il ciano (q<0 -> 0 = nero), tiene solo il fuoco
    # DENOISE (--denoise): attenua il ribollio nel rendering SENZA tagliare la materia. Due filtri
    # dolci: (1) spaziale - ammorbidisce il campo (media coi vicini) togliendo le fluttuazioni fini
    # cella-per-cella (i "quadratini") ma tenendo la struttura; (2) temporale leggero - media col
    # frame precedente cosi' il ribollio effimero si smorza. NON alza la soglia (che taglierebbe la
    # materia lasciando solo frammenti). NON tocca la fisica: filtra solo l'immagine mostrata.
    if stato.get("denoise", False):
        try:
            from scipy.ndimage import gaussian_filter as _gf
            q = _gf(q, 1.2)      # smoothing SPAZIALE: toglie i quadratini, ammorbidisce
        except Exception:
            pass
        qm = stato.get("_q_mem", None)
        if qm is not None and qm.shape == q.shape:
            beta = 0.4           # media temporale LEGGERA (era 0.6, troppo aggressiva)
            q = beta * qm + (1 - beta) * q
        stato["_q_mem"] = q.copy()
    # SFONDO TRASPARENTE fuori dalla scena: converto in RGBA e rendo trasparente dove
    # |q| e' sotto una soglia minima (nessuna interferenza rilevabile = fuori dai dati),
    # tenendo il nero fisico dove l'interferenza e' davvero nulla ma c'e' materia intorno.
    rgba = CMAP_INTERF((q + 1) / 2)               # mappa [-1,1] -> colore
    # TRASPARENZA AL VUOTO: soglia relativa al contrasto della scena (non un numero fisso): dove
    # c'e' materia netta il fondo ribollente si dirada. Solo resa, non tocca la fisica.
    # NB: col denoise NON si alza la soglia (lo smoothing gia' pulisce il ribollio); alzarla
    # lasciava solo quadratini isolati.
    soglia_vuoto = float(np.clip(0.06 + 0.30 * contrasto, 0.06, 0.30))
    alpha = np.clip((np.abs(q) - soglia_vuoto) / max(1.0 - soglia_vuoto, 1e-6), 0.0, 1.0)
    rgba[..., 3] = alpha
    ax.imshow(rgba, origin="lower", extent=[-R, R, -R, R], interpolation="bilinear")
    ax.set_xlim(-R*1.12, R*1.12); ax.set_ylim(-R*1.12, R*1.12)
    ax.set_aspect("equal"); ax.axis("off")
    ax.patch.set_alpha(0.0)                    # sfondo pannello trasparente (non nero)
    if stato["gabbia"]: bussola(ax, R, M)     # nel margine, mai sopra il campo
    ax.set_title("LA SOLA INTERFERENZA (fondo incoerente sottratto)\n"
                 "fuoco = materia   ·   ciano = distruzione   ·   nero = nulla\n"
                 f"(volumetrico · camera {np.degrees(angolo_vista())%360:.0f}°"
                 f"{' auto' if stato['rot_auto'] else ' — trascina per ruotare'})",
                 fontsize=10, color="#333")

    # ---------- PANNELLO DESTRO: I PUNTATORI ----------
    # ---------- POZZO GRAVITAZIONALE (embedding di Flamm sulla materia vera) ----------
    resg = 54
    lim_g = R * 0.95
    gx = np.linspace(-lim_g, lim_g, resg); gy = np.linspace(-lim_g, lim_g, resg)
    GXm, GYm = np.meshgrid(gx, gy, indexing='ij')
    pts2d = np.column_stack([GXm.ravel(), GYm.ravel()])
    n0 = net.n
    if n0 > 0 and len(net.psi) == n0:
        Pn = (net.pos @ M)[:, :2]
        Iv = np.abs(net.psi[:n0]) ** 2
        tree = cKDTree(Pn)
        vic = tree.query_ball_point(pts2d, r=lim_g * 0.5)
        phi_w = np.zeros(pts2d.shape[0])
        for gi in range(pts2d.shape[0]):
            vv = vic[gi]
            if vv:
                dd = np.linalg.norm(Pn[vv] - pts2d[gi], axis=1) + LAM * 0.5
                phi_w[gi] = np.sum(Iv[vv] / dd)
        phi_w = phi_w.reshape(GXm.shape)
        # LISCIATURA: durante la valanga di mitosi con antifase, i singoli anti-nodi
        # rendono il potenziale rugoso (picchi e crateri locali). Lo smoothing mostra
        # la curvatura gravitazionale D'INSIEME (la luna) invece del rumore dei nodi
        # (il dito), cosi' il pozzo resta un imbuto pulito anche a molti nodi.
        phi_w = gaussian_filter(phi_w, sigma=1.6)
        # sottraggo il FONDO (il bordo della scena, dove non c'e' materia concentrata):
        # cosi' il pozzo mostra il CONTRASTO della massa, e non annega quando la
        # valanga di mitosi riempie di puntatori tutto lo spazio uniformemente.
        bordo = np.concatenate([phi_w[0], phi_w[-1], phi_w[:, 0], phi_w[:, -1]])
        phi_w = np.maximum(phi_w - np.median(bordo), 0.0)
        pm = phi_w.max()
        # profondita' ANCORATA a scala assoluta (come vmax dell'interferenza).
        ps = stato.get("pozzo_scala")
        if pm > 0:
            stato["pozzo_scala"] = pm if ps is None else max(pm, 0.97 * ps)
        scala = stato.get("pozzo_scala") or max(pm, 1e-6)
        prof_scala = _scala_sistema() * 0.9
        # POZZI MULTIPLI: il potenziale somma di piu' sorgenti gia' contiene un pozzo
        # per ogni massa; la mappatura sqrt li rende proporzionati alla massa (fedele
        # alla gravita': massa maggiore, pozzo piu' profondo). La griglia piu' fitta
        # (resg alto) garantisce che masse vicine restino pozzi DISTINTI e non si
        # fondano in un'unica conca larga.
        Zdef = -prof_scala * np.sqrt(np.clip(phi_w / scala, 0, 1) + 1e-6) if pm > 0 else np.zeros_like(GXm)
    else:
        Zdef = np.zeros_like(GXm)
    prof = -Zdef; pmx = max(prof.max(), 1e-6)
    from matplotlib import cm as _cm
    col = _cm.magma(0.12 + 0.82 * (prof / pmx))
    ax3d.plot_surface(GXm, GYm, Zdef, facecolors=col, rstride=1, cstride=1,
                      linewidth=0.15, edgecolor="#22103a", antialiased=True, shade=False)
    ax3d.contour(GXm, GYm, Zdef, levels=8, colors="#4a148c", alpha=0.35,
                 linewidths=0.6, offset=Zdef.min() * 1.05, zdir='z')
    ax3d.view_init(elev=26, azim=-60)
    ax3d.set_xlim(-R, R); ax3d.set_ylim(-R, R)
    ax3d.set_zlim(-_scala_sistema() * 0.95, _scala_sistema() * 0.35)
    ax3d.axis("off")
    ax3d.set_title("POZZO GRAVITAZIONALE\n(embedding della metrica · profondità = materia)",
                   fontsize=9, color="#7b1fa2")

    P = net.pos @ M                            # i puntatori ruotano col campo
    # TRASPARENZA AL VUOTO: l'opacita' di ogni puntatore e' proporzionale alla sua intensita'
    # d'interferenza. Le masse (alta intensita', la materia coerente) restano visibili; il vuoto
    # ribollente (bassa intensita') diventa quasi trasparente. Cosi' si vede la materia, non la
    # tempesta di fondo. Non cambia la fisica: e' solo resa. La soglia e' relativa (mediana).
    Ivis = net.intensita()[:net.n]
    Iref = max(float(np.median(Ivis)) * 3.0, 1e-9)     # scala relativa (materia >> vuoto)
    alpha_nodo = np.clip(Ivis / Iref, 0.03, 1.0)       # vuoto ~0.03 (quasi invisibile), masse ~1
    ax2.scatter(P[:net.n, 0], P[:net.n, 1], c=np.cos(net.phi[:net.n]), s=5, cmap="twilight",
                vmin=-1, vmax=1, alpha=alpha_nodo, linewidths=0)
    ax2.set_xlim(-R*1.12, R*1.12); ax2.set_ylim(-R*1.12, R*1.12)
    ax2.set_aspect("equal"); ax2.axis("off")
    ax2.set_title("i puntatori (fase) — il dito", fontsize=9, color="#666")

    # ---------- DIAGNOSTICA ----------
    massa = massa3d      # integrale di |Psi|^2 su TUTTO il volume
    if stato["massa0"] is None and stato["nframe"] > 25: stato["massa0"] = max(massa, 1e-9)
    rel = massa / stato["massa0"] if stato["massa0"] else 1.0
    T = [("MURATORE DI PLANCK", 14, "#111", "bold"),
         ("tutte le leggi sempre attive", 9, "#7b1fa2", "normal"), ("", 8, "#000", "normal"),
         (f"puntatori: {net.n} / {MAX_NODI}", 10, "#111", "normal"),
         (f"archi:     {len(net.i)}", 10, "#111", "normal"), ("", 8, "#000", "normal"),
         ("— MATERIA (dal campo) —", 10, "#111", "bold"),
         (f"massa totale:  {massa:.3g}   (x{rel:.2f})", 10, "#111", "normal"),
         (f"picco proiettato: {campo.max():.3g}", 10, "#111", "normal"),
         (f"coerenza globale: {dg['coer_g']:.3f}", 10, "#111", "normal"),
         (f"coerenza locale:  {dg['coer_l']:.3f}", 10, "#111", "normal"),
         ("", 8, "#000", "normal"), ("— GEOMETRIA VIVA —", 10, "#7b1fa2", "bold"),
         (f"d medio:     {dg['d_med']:.3f}", 10, "#7b1fa2", "normal"),
         (f"dilatazione: {100*dg['dil']:+.1f}%", 10, "#7b1fa2", "normal"),
         (f"stress:      {100*dg['stress']:+.2f}%", 10, "#7b1fa2", "normal"),
         ("", 8, "#000", "normal"), ("— TOPOLOGIA —", 10, "#0277bd", "bold"),
         (f"torsione max: {dg['tw']:.1f} / {(3*np.pi if TORS_4PI else PHI_CRIT):.1f}", 10, "#0277bd", "normal"),
         (f"mitosi: {net.nati}  (negate {net.negate})", 10, "#0277bd", "normal"),
         (f"prob. coppia: {100.0 * net.ultima_prob_coppia:.1f}%", 10, "#c0392b", "bold"),
         (f"antiparticelle: {net.coppie_nate}", 10, "#c0392b", "bold"),
         (f"N_critico (adattivo): {massa_critica_adattiva(net):.0f}", 10, "#5d4037", "bold"),
         (f"raggio nascita: {stato['raggio_semina']:.1f}  masse: {stato['num_masse']}", 9, "#5d4037", "normal"),
         (f"regime: {stato_crossover(net)['regime']} (g|F| med {stato_crossover(net)['gF_med']:.3f})", 9,
          "#00695c" if stato_crossover(net)['regime']=='geometrico' else "#e65100", "normal"),
         *(_righe_stato_universo(net)),
         (f"topologia: {classifica_topologia(net)[0]}", 10, "#5d4037", "bold"),
         (f"legami entro portata: {100*dg['entro']:.0f}%", 10, "#0277bd", "normal")]
    y = 0.97
    for txt, sz, col, wt in T:
        if txt: axt.text(0, y, txt, fontsize=sz, color=col, weight=wt, va="top")
        y -= 0.042 if txt else 0.018
    if stato["piazza"]:
        axc.text(0.5, 0.5, "▶ PIAZZAMENTO %s ATTIVO — clicca sul pannello 3D dove crearlo (raggio %.1f)"
                 % ("MASSA" if stato["piazza"] == "materia" else "BUCO NERO", stato["raggio_semina"]),
                 ha="center", va="center", fontsize=11, color="#b71c1c", weight="bold")
    elif test["cap"]:
        axc.text(0.5, 0.5, test["cap"], ha="center", va="center",
                 fontsize=11, color="#4a148c", weight="bold")


# ----------------------------------------------------- rotazione manuale
def _ruota(dth=0.0, dph=0.0):
    def _f(_=None):
        stato["theta"] += dth
        stato["elev"] = float(np.clip(stato["elev"] + dph, -1.45, 1.45))
    return _f


def _auto(_=None):
    stato["rot_auto"] = not stato["rot_auto"]


def _premi(ev):
    if ev.button == 1 and ev.inaxes in (ax, ax3d, ax2) and ev.xdata is not None:
        if stato["piazza"]:                       # modalita' piazzamento attiva
            _semina_al_click(ev.xdata, ev.ydata, stato["piazza"])
            stato["piazza"] = None                # un click, un oggetto
            return
        stato["trascina"] = (ev.xdata, ev.ydata)


def _muovi(ev):
    """trascinare col mouse su un pannello ruota la vista: orizzontale =
    azimut, verticale = elevazione. I due pannelli restano solidali."""
    t = stato["trascina"]
    if t is None or ev.inaxes not in (ax, ax2) or ev.xdata is None: return
    R = max(stato["R"], 1e-6)
    stato["theta"] -= 3.0 * (ev.xdata - t[0]) / (2 * R)
    stato["elev"] = float(np.clip(stato["elev"] + 3.0 * (ev.ydata - t[1]) / (2 * R), -1.45, 1.45))
    stato["trascina"] = (ev.xdata, ev.ydata)


def _rilascia(_ev):
    stato["trascina"] = None


def _tasto(ev):
    k = ev.key
    if   k == "left":  _ruota(-0.10, 0)()
    elif k == "right": _ruota(+0.10, 0)()
    elif k == "up":    _ruota(0, +0.08)()
    elif k == "down":  _ruota(0, -0.08)()
    elif k == "r":     _auto()
    elif k == " ":     _pausa()
    elif k in ("+", "="): _zoom(1.25)()
    elif k == "-":     _zoom(0.8)()
    elif k == "s":     net.semina(stato["passo_semina"])
    elif k == "c":     stato["semina_cont"] = not stato["semina_cont"]
    elif k == "g":     stato["gabbia"] = not stato["gabbia"]
    elif k in ("f", "F"):    # PIU' VELOCE: piu' passi di motore per frame
        stato["passi_frame"] = min(int(stato.get("passi_frame", PASSI_PER_FRAME)) + 2, 40)
        print("[VELOCITA'] passi per frame:", stato["passi_frame"])
    elif k in ("l", "L"):    # PIU' LENTO: meno passi per frame (fino a 1)
        stato["passi_frame"] = max(int(stato.get("passi_frame", PASSI_PER_FRAME)) - 2, 1)
        print("[VELOCITA'] passi per frame:", stato["passi_frame"])
    elif k in ("d", "D"):    # DENOISE: attenua il ribollio transitorio nel rendering
        stato["denoise"] = not stato.get("denoise", False)
        stato["_q_mem"] = None
        print("[DENOISE]", "ON" if stato["denoise"] else "OFF")


def _btn(x, y, lab, cb, w=0.105, h=0.045):
    b = Button(plt.axes([x, y, w, h]), lab, color="#eceff1", hovercolor="#cfd8dc")
    b.on_clicked(cb); b.label.set_fontsize(8); return b


def _zoom(v):
    def _f(_=None): stato["zoom"] = float(np.clip(stato["zoom"] * v, 0.3, 4))
    return _f


def _pausa(_=None): stato["pausa"] = not stato["pausa"]


def _limite(_=None):
    """Attiva/disattiva il tetto alle nascite. Di default NESSUN tetto (MITMAX=0):
    la fisica e' visibile. Il pulsante lo alza a 60 come guardia di memoria quando
    serve, poi lo rimette a 0. E' una scelta esplicita dell'utente, mai un default
    che falsifica le metriche."""
    global MITMAX
    MITMAX = 60 if MITMAX == 0 else 0
    print("[LIMITE] tetto nascite:", "ATTIVO (60)" if MITMAX else "nessuno (mitosi libera)")


def _crea_massa(_=None):
    """Crea materia STRUTTURATA: puntatori sotto la soglia critica N_c (gusci netti)."""
    _crea_masse_casuali(stato["num_masse"], tipo="materia")
    print("[MASSA] create %d masse sotto N_c=%.0f (materia strutturata)"
          % (stato["num_masse"], massa_critica_collasso()))


def _crea_buconero(_=None):
    """Crea BUCHI NERI: puntatori oltre la soglia critica N_c (collasso omogeneo)."""
    _crea_masse_casuali(stato["num_masse"], tipo="buconero")
    print("[BUCO NERO] creati %d buchi neri oltre N_c=%.0f (collasso)"
          % (stato["num_masse"], massa_critica_collasso()))


def _piazza_materia(_=None):
    """Attiva la modalita' PIAZZAMENTO di materia: il prossimo click sul pannello 3D
    semina una massa in quel punto, col raggio impostato nel box."""
    stato["piazza"] = None if stato["piazza"] == "materia" else "materia"
    print("[PIAZZA MASSA]", "clicca sul pannello 3D dove vuoi la massa"
          if stato["piazza"] else "annullato")


def _piazza_buconero(_=None):
    """Attiva la modalita' PIAZZAMENTO di buco nero."""
    stato["piazza"] = None if stato["piazza"] == "buconero" else "buconero"
    print("[PIAZZA BUCO NERO]", "clicca sul pannello 3D dove vuoi il buco nero"
          if stato["piazza"] else "annullato")


def _semina_al_click(xdata, ydata, tipo):
    """Converte un click sul pannello (coordinate della vista ruotata) in una
    posizione 3D VERA e semina li' l'oggetto. Soluzione A: profondita' sul piano
    di mezzo della scena (z_vista=0), poi si applica la rotazione inversa per
    tornare allo spazio reale. Il raggio e' quello del box 'Raggio'."""
    M = matrice_vista(angolo_vista(), stato["elev"])
    # il click da' (x, y) nel sistema RUOTATO; z (profondita') = 0 (piano di mezzo)
    p_vista = np.array([xdata, ydata, 0.0])
    # M trasforma reale->vista (pos @ M). Per tornare: p_reale = M @ p_vista
    # (M ortogonale: l'inversa e' la trasposta; pos@M significa M.T applicata a colonna)
    p_reale = M @ p_vista
    Nc = massa_critica_collasso()
    n_punt = int(Nc * 1.8) if tipo == "buconero" else int(Nc * 0.45)
    et = ("buconero_" if tipo == "buconero" else "massa_") + str(net.n)
    _massa(p_reale, stato["raggio_semina"], n_punt, 0.0, etichetta=et)  # fase compatibile fra oggetti
    print("[PIAZZATO %s] a (%.1f, %.1f, %.1f) raggio %.1f, %d puntatori"
          % (tipo.upper(), p_reale[0], p_reale[1], p_reale[2],
             stato["raggio_semina"], n_punt))

def _big_bang(_=None, calore=0.5, punti=1500):
    """Innesca il BIG BANG: evento iniziale denso e CALDO (fasi agitate, fuori
    equilibrio), e attiva l'accoppiamento TAU_TW-densita'. L'evento accende la
    mitosi (creazione di materia); l'espansione successiva diluisce e la generazione
    si calma da se'. Idea di Luca: il Big Bang tara la mitosi per la semina."""
    net.semina(punti, raggio=1.2, centro=(0, 0, 0))
    # calore: agitazione termica iniziale delle fasi (fuori equilibrio)
    net.phivel = net.rng.normal(0, calore, net.n)
    V = float(net.d0.sum()) if len(net.d0) else 1.0
    stato["bigbang"] = True
    stato["bigbang_drif"] = net.n / max(V, 1e-9)     # densita' di riferimento (t=0)
    print("[BIG BANG] evento caldo: %d punti, calore %.2f. Mitosi accoppiata alla densita'."
          % (punti, calore))
    print("           l'universo si accende, genera materia, poi si calma espandendo.")

BOTTONI = []
if "--test" not in _sys.argv:       # bottoni in interattivo (con o senza flag); non nel video headless
    x = 0.005
    for nome in TESTS:                       # fila alta: gli scenari
        BOTTONI.append(_btn(x, 0.062, nome, avvia_test(nome), w=0.10)); x += 0.103
    # creazione diretta di masse / buchi neri (dalla legge della densita' critica)
    BOTTONI.append(_btn(0.005, 0.115, "+ MASSA", _crea_massa, w=0.10))
    BOTTONI.append(_btn(0.108, 0.115, "+ BUCO NERO", _crea_buconero, w=0.10))
    # piazzamento col mouse: attiva, poi clicca sul pannello 3D per posizionare
    BOTTONI.append(_btn(0.211, 0.115, "piazza MASSA", _piazza_materia, w=0.10))
    BOTTONI.append(_btn(0.314, 0.115, "piazza B.NERO", _piazza_buconero, w=0.10))
    BOTTONI.append(_btn(0.634, 0.115, "BIG BANG", lambda _=None: _big_bang(), w=0.10))
    # raggio (volume di nascita) e numero masse: BOTTONI +/- invece di caselle di
    # testo, che in matplotlib entrano in conflitto con l'animazione (perdono il
    # focus a ogni frame). I bottoni non hanno questo problema.
    def _ragg(delta):
        def _f(_=None):
            stato["raggio_semina"] = float(np.clip(stato["raggio_semina"] + delta, 0.3, 6.0))
            print("[RAGGIO] =", round(stato["raggio_semina"], 1))
        return _f
    def _nmasse(delta):
        def _f(_=None):
            stato["num_masse"] = int(np.clip(stato["num_masse"] + delta, 1, 12))
            print("[N.MASSE] =", stato["num_masse"])
        return _f
    BOTTONI.append(_btn(0.417, 0.115, "raggio -", _ragg(-0.5), w=0.048))
    BOTTONI.append(_btn(0.468, 0.115, "raggio +", _ragg(+0.5), w=0.048))
    BOTTONI.append(_btn(0.520, 0.115, "masse -", _nmasse(-1), w=0.048))
    BOTTONI.append(_btn(0.571, 0.115, "masse +", _nmasse(+1), w=0.048))
    x = 0.005
    for lab, cb in (("< ruota", _ruota(-0.12, 0)), ("ruota >", _ruota(+0.12, 0)),
                    ("alza", _ruota(0, +0.10)), ("abbassa", _ruota(0, -0.10)),
                    ("auto rot.", _auto), ("zoom +", _zoom(1.25)),
                    ("zoom -", _zoom(0.8)), ("+punt.", lambda _=None: net.semina(stato["passo_semina"])),
                    ("semina cont.", lambda _=None: stato.__setitem__("semina_cont", not stato["semina_cont"])),
                    ("LIMITE", _limite), ("pausa", _pausa)):
        BOTTONI.append(_btn(x, 0.008, lab, cb, w=0.10)); x += 0.103
    for _ev, _cb in (("button_press_event", _premi), ("motion_notify_event", _muovi),
                     ("button_release_event", _rilascia), ("key_press_event", _tasto)):
        fig.canvas.mpl_connect(_ev, _cb)


def _durata(nome): return sum(f.get("dur", 150) for f in TESTS[nome])


def _applica_flag(a):
    """Applica i parametri/flag ai globali. Usata sia in headless sia in interattivo,
    cosi' TUTTI i flag (coarse-graining incluso) valgono in ogni modalita'."""
    global net
    global MAX_NODI, P_LAM, TAU_LOC, ZETA_M, HAM_SRC, ALPHA_NAT, DIFF_RES, PLAST_MIT, ZETA_LOC
    global COPPIA_MIT, MU_PSI, MITMAX, GAMMA, LAM, SCALA_B, TAU_USA_D0, CALORE_VETTORIALE, K_FRANGE, VIRIALE
    if getattr(a, "tau_d0", False):
        TAU_USA_D0 = True
        print("[tau] tau_p locale usa d0 (distanza di riposo) invece di d reale: forma piu' stabile")
    if getattr(a, "calore_vett", False):
        CALORE_VETTORIALE = True
        print("[calore] calcio termico VETTORIALE+chirale attivo: omega_s 3D eccitato, phivel firmato da perc_chi")
    if getattr(a, "calore_scal", False):
        CALORE_VETTORIALE = False
        print("[calore] calcio termico SCALARE isotropo forzato (vettoriale spento per confronto)")
    MAX_NODI = a.maxnodi
    P_LAM = a.plam
    TAU_LOC = a.tauloc
    ZETA_M = a.zeta
    ZETA_LOC = bool(getattr(a, "zeta_loc", False))   # smorzamento locale (legge): default off = non-regressione
    HAM_SRC = a.ham
    ALPHA_NAT = a.alfanat
    DIFF_RES = a.diffres
    PLAST_MIT = a.plastmit
    COPPIA_MIT = a.coppia
    MU_PSI = a.mupsi
    GAMMA = a.gamma
    LAM = a.lam
    MITMAX = a.mitmax
    K_FRANGE = a.kfrange   # canale ORBITALE tangenziale (moto lungo le frange). 0 = spento (non-regressione)
    VIRIALE = bool(getattr(a, "viriale", False))   # conversione viriale (legge): default off = non-regressione
    # COARSE-GRAINING: se richiesta una scala > 1, applico le regole di scala derivate.
    SCALA_B = a.scala
    if SCALA_B != 1.0:
        LAM = a.lam * (SCALA_B ** (1.0 / 3.0))   # lambda_eff = lambda_base * B^(1/3)
        GAMMA = a.gamma / np.sqrt(SCALA_B)        # gamma_eff = gamma/sqrt(B): la saturazione
                                                  # resta invariante in forma (derivato esatto)
        print(f"[scala] coarse-graining B={SCALA_B:.0f}: ogni solitone rappresenta "
              f"{SCALA_B:.0f} fini | lambda_eff={LAM:.3f} | gamma_eff={GAMMA:.4f} | "
              f"R_conn={3.0*LAM:.2f} (scala con lambda). NB: la regione FISICA di semina "
              f"resta la stessa — i blocchi occupano lo spazio dei fini, piu' grossolanamente.")
    # se richiesto un seme/numero nodi diverso, rigenero la rete
    if a.seed is not None or a.nodi != SEME_INIZIALE:
        net = Rete(a.seed if a.seed is not None else 42)
        net.semina(a.nodi)
        for _ in range(300): net.step()
        net.rilassa_disegno(30)


def esegui_headless(a):
    from matplotlib.animation import FFMpegWriter
    global net
    _applica_flag(a)
    # N MASSE nel video: passo numero e raggio allo scenario. Lo zoom seguira' lo scaling perche'
    # l'inquadratura R si adatta all'estensione reale dei nodi (vedi update: R = max|pos|).
    _NMASSE_VIDEO["n"] = max(2, int(getattr(a, "nmasse", 2)))
    _NMASSE_VIDEO["sep"] = float(getattr(a, "sep", 3.0))
    _sz = getattr(a, "size", None)
    if _sz:
        try: _NMASSE_VIDEO["size"] = [float(x) for x in str(_sz).split(",") if x.strip()]
        except Exception: _NMASSE_VIDEO["size"] = None
    else:
        _NMASSE_VIDEO["size"] = None
    stato["denoise"] = bool(getattr(a, "denoise", False))
    stato["solo_materia"] = bool(getattr(a, "solo_materia", False))
    if getattr(a, "passi_per_frame", None):
        stato["passi_frame"] = max(1, int(a.passi_per_frame))
    stato["giri"] = a.giri
    stato["rot_auto"] = (a.giri != 0)     # nei filmati la rotazione resta opzionale
    stato["gabbia"] = bool(a.bussola)
    n = a.frames or _durata(a.test) + 15
    stato["durata"] = n
    # AVVIO DELLO SCENARIO: esegue la prima fase (compresa la sua al_via, che pianta la massa/
    # buco nero). Senza questo, in headless lo scenario non partiva mai e si renderizzava solo
    # l'evoluzione libera del seme. avvia_test restituisce la callback dei bottoni: la si chiama
    # subito per far scattare la prima fase.
    if a.test:
        avvia_test(a.test)()
    w = FFMpegWriter(fps=a.fps, bitrate=4000,
                     metadata=dict(title=f"Muratore di Planck - {a.test}"))
    print(f"[headless] test={a.test} frame={n} fps={a.fps} - tutte le leggi attive")
    with w.saving(fig, a.out, dpi=a.dpi):
        for f in range(n):
            update(f); w.grab_frame()
            if (f + 1) % 25 == 0:
                d = net.diagnostica()
                print(f"   {f+1}/{n} nodi={net.n} archi={len(net.i)} "
                      f"dilataz={100*d['dil']:+.1f}% torsione={d['tw']:.1f} "
                      f"mitosi={net.nati}", flush=True)
    print(f"[headless] scritto {a.out}")


def _cli():
    import argparse
    p = argparse.ArgumentParser(description="Muratore di Planck v9 - headless")
    p.add_argument("--calore-vett", action="store_true", dest="calore_vett",
                   help="calcio termico VETTORIALE+chirale (default ON): eccita omega_s 3D e firma phivel con perc_chi.")
    p.add_argument("--calore-scal", action="store_true", dest="calore_scal",
                   help="forza il calcio termico SCALARE isotropo (spegne il vettoriale, per confronto A/B).")
    p.add_argument("--tau-d0", action="store_true", dest="tau_d0",
                   help="tau_p locale usa d0 (distanza di riposo) invece di d (reale dilatata). "
                        "Piu' stabile, meno gonfiaggio (d_medio ~1.33 vs ~2.88).")
    p.add_argument("--regime", choices=["stocastico", "deterministico"], default=None,
                   help="regime dinamico: 'stocastico' (vuoto attivo, VALIDATO e STABILE) | "
                        "'deterministico' (vuoto spento, mitosi modulata dal tempo proprio locale, "
                        "WIP). Sovrascrive REGIME in testa al file. Vale per headless e interattivo.")
    p.add_argument("--test", choices=sorted(TESTS), default=None,
                   help="scenario headless (registra un video). Se omesso ma con altri "
                        "flag, questi si applicano alla modalita' interattiva")
    p.add_argument("--out", default=None)
    p.add_argument("--frames", type=int, default=0)
    p.add_argument("--fps", type=int, default=20)
    p.add_argument("--dpi", type=int, default=100)
    p.add_argument("--seed", type=int, default=None)
    p.add_argument("--nodi", type=int, default=SEME_INIZIALE, help="puntatori del seme iniziale")
    p.add_argument("--maxnodi", type=int, default=MAX_NODI,
                   help="tetto ai puntatori (la mitosi ne crea: serve margine)")
    p.add_argument("--diffres", type=float, default=DIFF_RES,
                   help="1 = diffonde il residuo: P_eq=rho diventa punto fisso esatto")
    p.add_argument("--alfanat", type=float, default=ALPHA_NAT,
                   help="1 = sorgente in unita' naturali c_s^2/d (elimina ALPHA_M)")
    p.add_argument("--ham", type=float, default=HAM_SRC,
                   help="1 = sorgente metrica hamiltoniana (toglie ALPHA_M), 0 = fenomenologica")
    p.add_argument("--zeta", type=float, default=ZETA_M,
                   help="smorzamento metrico adimensionale (0 = BETA_M costante)")
    p.add_argument("--zeta-loc", action="store_true", dest="zeta_loc",
                   help="SMORZAMENTO LOCALE (legge): zeta scende nella MATERIA (rho>mediana), "
                        "resta pieno nel VUOTO. Lascia vivere la circolazione tangenziale. "
                        "Default off = identico a prima (non-regressione).")
    p.add_argument("--tauloc", type=float, default=TAU_LOC,
                   help="1 = ogni nodo avanza nel proprio tempo proprio, 0 = orologio globale")
    p.add_argument("--plam", type=float, default=P_LAM,
                   help="esponente della scala locale di lambda (0 = lambda fissa)")
    p.add_argument("--plastmit", type=float, default=PLAST_MIT,
                   help="spinta plastica su d0 alla mitosi (0 = spenta, dimezzamento normale)")
    p.add_argument("--coppia", type=float, default=COPPIA_MIT,
                   help="frazione di eventi mitosi che emette un anti-nodo (0 = spenta)")
    p.add_argument("--gamma", type=float, default=GAMMA,
                   help="saturazione: alza per portare il crossover gamma|F|~1 nel regime simulabile")
    p.add_argument("--lam", type=float, default=LAM,
                   help="portata del kernel (lambda). Cambia la geometria di coerenza")
    p.add_argument("--scala", type=float, default=1.0,
                   help="COARSE-GRAINING: fattore di blocco B (1=scala di Planck). "
                        "Ogni solitone rappresenta B fini; imposta lambda_eff=lambda*B^(1/3) "
                        "e massa/solitone=B, preservando le leggi al continuo")
    p.add_argument("--mupsi", type=float, default=MU_PSI,
                   help="auto-interazione dell'interferenza (<0 repulsiva, 0 spenta)")
    p.add_argument("--mitmax", type=int, default=MITMAX,
                   help="tetto nascite per passo (0 = nessun tetto, mitosi libera)")
    p.add_argument("--kfrange", type=float, default=K_FRANGE,
                   help="MOTO LUNGO LE FRANGE (canale orbitale tangenziale): sposta d0 lungo il "
                        "gradiente di fase, dove il flusso e' rotazionale. 0 = spento (default, "
                        "identico a prima). Prova 0.02-0.05 per cercare la precessione orbitale.")
    p.add_argument("--viriale", action="store_true", dest="viriale",
                   help="CONVERSIONE VIRIALE (legge, zero parametri): la spinta radiale si "
                        "ripartisce fra cadere (cos^2) e girare (sin^2) secondo l'angolo fra "
                        "pozzo e flusso di fase. Conservativa (non additiva come kfrange). "
                        "Default off = non-regressione.")
    p.add_argument("--bussola", type=int, default=1,
                   help="1 = indicatore d'assi nel margine, 0 = nessun riferimento")
    p.add_argument("--giri", type=float, default=1.0,
                   help="giri di camera sulla durata della scena (0 = vista fissa)")
    p.add_argument("--batch", action="store_true",
                   help="processo batch: due masse, evoluzione lunga, misura la CONDENSAZIONE "
                        "nel vuoto fra le masse (ordine, densita', nuovo nucleo). Output numerico.")
    p.add_argument("--passi", type=int, default=3000,
                   help="batch: numero totale di passi di evoluzione (default 3000)")
    p.add_argument("--ogni", type=int, default=30,
                   help="batch: ogni quanti passi registrare una misura (default 30)")
    p.add_argument("--sep", type=float, default=2.3,
                   help="batch: raggio del cerchio su cui stanno le masse (default 2.3)")
    p.add_argument("--nmasse", type=int, default=2,
                   help="batch/video: numero di masse, disposte in cerchio di raggio sep (default 2)")
    p.add_argument("--size", type=str, default=None,
                   help="video: dimensioni (raggio) degli oggetti, es. --size 0.7,1.2,0.5 (uno per oggetto; "
                        "se meno dei necessari, l'ultimo vale per i restanti; se assente, default della scena)")
    p.add_argument("--passi-per-frame", "--ppf", type=int, default=None, dest="passi_per_frame",
                   help="video: passi di motore per ogni frame renderizzato (default 6). Alzarlo copre "
                        "piu' evoluzione con meno frame: passi_totali = frames x passi_per_frame.")
    p.add_argument("--solo-materia", dest="solo_materia", action="store_true",
                   help="nasconde il guscio ciano (distruttivo) per vedere i nuclei di materia accesa")
    p.add_argument("--denoise", action="store_true",
                   help="rendering: attenua il ribollio transitorio (filtro temporale + soglia piu' alta), "
                        "cosi' restano visibili le masse persistenti. Non tocca la fisica, solo la resa.")
    p.add_argument("--csv", default="condensazione.csv",
                   help="batch: file CSV di output con i numeri della misura")
    p.add_argument("--diaglog", default=None,
                   help="batch: file CSV di LOG DIAGNOSTICO COMPLETO (tutte le variabili di stato a OGNI step, per catturare l'istante di un artefatto)")
    a = p.parse_args()
    if a.out is None and a.test is not None:
        a.out = f"{a.test.lower().replace(' ', '_')}.mp4"
    return a


def batch_condensazione(a):
    """PROCESSO BATCH: due masse coerenti con precessione, evoluzione lunga. Misura nel tempo la
    CONDENSAZIONE nel vuoto fra le masse: ordine, densita', numero di nodi centrali, e i controlli
    per distinguere la NASCITA di una nuova massa dal semplice accrescimento delle due esistenti.
    Output numerico su stdout e CSV. Pensato per girare a lungo su hardware capace."""
    import time as _t
    try:
        from scipy.spatial import cKDTree
    except Exception:
        cKDTree = None
    _applica_flag(a)
    seed = a.seed if a.seed is not None else SEME_INIZIALE
    passi = int(a.passi); ogni = max(1, int(a.ogni)); sep = float(a.sep)
    _nm = max(2, int(getattr(a, "nmasse", 2)))
    print(f"[batch] condensazione: seed={seed} passi={passi} ogni={ogni} sep={sep} nmasse={_nm}")
    print(f"[batch] leggi attive: GRAV_BIFASE={GRAV_BIFASE} SPIN_ORBITA(via SPINORE)={SPINORE} "
          f"COPPIA_MIT={COPPIA_MIT} lambda={LAM:.3f}")
    Nc = massa_critica_collasso()
    net = Rete(seed); net.semina(80)
    for _ in range(6):
        scuoti_vuoto(net); net.step(); net.mitosi(); net.rilassa_disegno(); net.memoria_hebbiana_moto()
    # N MASSE disposte in cerchio di raggio 'sep' attorno all'origine (equidistanti dal centro,
    # simmetriche: il sistema scala in modo pulito con N). Traccio gli indici di ogni coorte per
    # distinguere la materia NATA dalla materia delle masse iniziali.
    nmasse = max(2, int(getattr(a, "nmasse", 2)))
    coorti = []            # lista di set: gli indici iniziali di ciascuna massa (metodo vecchio)
    centri = []            # i centri delle masse (per baricentro e regione centrale)
    ids_massa = []         # TRACKING: gli ID di massa (metodo nuovo, robusto alla mitosi)
    for k in range(nmasse):
        if nmasse == 2:
            ang = np.pi * k         # 2 masse: agli antipodi sull'asse x (-sep, +sep), come prima
        else:
            ang = 2*np.pi*k/nmasse  # N masse: in cerchio
        cx, cy = sep*np.cos(ang), sep*np.sin(ang)
        base = net.n
        mid = net.nuova_massa(int(Nc*0.6), raggio=_size_video(k, 0.8), centro=(cx, cy, 0.0), fase=0.0)  # TRACKING: ID
        coorti.append(set(range(base, net.n)))
        centri.append((cx, cy))
        ids_massa.append(mid)
    net.aggiorna_pesi_concorrenza()   # fissa i pesi di nascita reali (dopo che il campo esiste)
    idxA0 = coorti[0]; idxB0 = coorti[1]   # compatibilita' con le metriche a due masse
    n_orig = net.n   # nodi che esistono PRIMA dell'evoluzione: tutto cio' che nasce dopo e' >= n_orig

    def _passo(net):
        scuoti_vuoto(net); net.step(); net.mitosi(); net.rilassa_disegno(); net.memoria_hebbiana_moto()

    def _stat(v):
        """statistiche compatte di un array: min, max, media, |max| (per diagnostica)."""
        if v is None or len(v) == 0: return (0.0, 0.0, 0.0, 0.0)
        v = np.asarray(v, float).ravel()
        return (float(np.nanmin(v)), float(np.nanmax(v)), float(np.nanmean(v)), float(np.nanmax(np.abs(v))))

    def _diag_completa(net, step):
        """LOG DIAGNOSTICO COMPLETO: tutte le variabili di stato del sistema a questo step, con le
        loro statistiche. Serve a catturare l'istante in cui una grandezza degenera (artefatto):
        guardando quale colonna esplode PER PRIMA si individua la causa. Ritorna una riga CSV."""
        n = net.n
        net.calcola_psi()
        I2 = np.abs(net.psi[:n])**2
        P = net.pos[:n]; r = np.linalg.norm(P, axis=1)
        tau = net.ritmo()
        # distanza minima fra nodi (se ~0 due nodi coincidono -> kernel esplode)
        dmin = 0.0
        if cKDTree is not None and n > 1:
            try:
                dd, _ = cKDTree(P).query(P, k=2); dmin = float(dd[:, 1].min())
            except Exception: dmin = -1.0
        # torsione, velocita' di fase, densita', tempo proprio, ampiezza
        tw = net.tw if len(net.tw) else np.zeros(1)
        cols = {}
        cols['n'] = n
        cols['I2_min'], cols['I2_max'], cols['I2_mean'], cols['I2_absmax'] = _stat(I2)
        cols['r_min'], cols['r_max'], cols['r_mean'], _ = _stat(r)
        cols['tw_min'], cols['tw_max'], cols['tw_mean'], cols['tw_absmax'] = _stat(tw)
        cols['phi_min'], cols['phi_max'], cols['phi_mean'], _ = _stat(net.phi[:n])
        cols['phivel_min'], cols['phivel_max'], cols['phivel_mean'], cols['phivel_absmax'] = _stat(net.phivel[:n])
        cols['d_min'], cols['d_max'], cols['d_mean'], _ = _stat(net.d[:n] if len(net.d) >= n else net.d)
        cols['d0_min'], cols['d0_max'], cols['d0_mean'], _ = _stat(net.d0[:n] if len(net.d0) >= n else net.d0)
        cols['eta_min'], cols['eta_max'], cols['eta_mean'], _ = _stat(net.eta[:n] if len(net.eta) >= n else net.eta)
        cols['tau_min'], cols['tau_max'], cols['tau_mean'], _ = _stat(tau)
        cols['dmin_nodi'] = dmin
        cols['xi_termo'] = float(getattr(net, 'xi_termo', 0.0))
        cols['n_archi'] = len(net.i)
        # conteggi di degenerazione: quanti valori non-finiti o estremi
        cols['n_naninf'] = int(np.sum(~np.isfinite(I2)) + np.sum(~np.isfinite(net.phivel[:n])))
        cols['n_I2_grandi'] = int(np.sum(I2 > 1.0))     # nodi con |Psi|^2 anomalo
        cols['n_lontani'] = int(np.sum(r > 15.0))       # nodi scagliati lontano
        # MISURE PER-MASSA (massa 0 tracciata): isolano la singola massa dall'espansione GLOBALE
        # del sistema, per rispondere a decadimento/equilibrio/divergenza sulla massa VERA.
        m0_I2pesata = 0.0; m0_raggio = 0.0; m0_N = 0; m0_coer = 0.0; m0_spin = 0.0; m0_spin_disp = 0.0
        m0_vort_pos = 0; m0_vort_neg = 0; m0_carica = 0
        m0_coer_nucleo = 0.0; m0_N_nucleo = 0; m0_raggio_nucleo = 0.0
        m0_Lz = 0.0; m0_Lz_norm = 0.0
        try:
            if getattr(net, 'conc_nodi', None) and getattr(net, 'masse_info', None):
                net.aggiorna_pesi_concorrenza()
                mid0 = sorted(net.masse_info.keys())[0]
                idx_m = []; pesi_m = []
                for k in range(min(len(net.conc_nodi), n)):
                    for voce in net.conc_nodi[k]:
                        if voce[0] == mid0:
                            idx_m.append(k); pesi_m.append(voce[2]); break
                if len(idx_m) >= 2:
                    idx_m = np.array(idx_m); pesi_m = np.array(pesi_m)
                    m0_N = int(len(idx_m))
                    m0_I2pesata = float(np.sum(I2[idx_m] * pesi_m))
                    m0_coer = float(np.mean(pesi_m))          # coerenza MEDIA (tutta la massa: nucleo+alone)
                    # CENTRO pesato per densita' |Psi|^2: sta nel NUCLEO denso, non tirato dall'alone
                    wI = I2[idx_m]
                    if wI.sum() > 1e-9:
                        cm = (P[idx_m] * wI[:, None]).sum(0) / wI.sum()
                    else:
                        cm = P[idx_m].mean(0)
                    dcm = np.linalg.norm(P[idx_m] - cm, axis=1)
                    m0_raggio = float(dcm.mean())            # raggio medio (tutta la massa)
                    # COERENZA DEL NUCLEO (locale): solo i nodi densi vicino al centro, non l'alone.
                    # Distingue "il cuore vive, l'alone diluisce" da "decade anche il nucleo".
                    r_nuc = max(np.percentile(dcm, 25), 1.0)  # quartile interno = nucleo denso
                    nuc = dcm < r_nuc
                    m0_coer_nucleo = float(np.mean(pesi_m[nuc])) if nuc.sum() >= 3 else m0_coer
                    m0_N_nucleo = int(nuc.sum())
                    m0_raggio_nucleo = float(dcm[nuc].mean()) if nuc.sum() >= 3 else 0.0
                    # SPIN COERENTE LOCALE: velocita' di fase media dei solitoni della massa,
                    # pesata dalla coerenza. Se != 0 con verso stabile e bassa dispersione = la massa
                    # precede su se stessa come unico oggetto (spin intrinseco). vphi_disp misura la
                    # coerenza dello spin: bassa = tutti ruotano insieme, alta = scorrelati.
                    # SPIN = ROTAZIONE DELL'ASSE del pattern di interferenza (cio' che si vede
                    # precedere nel video). Calcolo l'asse principale della massa via PCA pesata per
                    # |Psi|^2, e misuro quanto ruota rispetto allo step precedente. La velocita' di
                    # rotazione dell'asse E' la precessione = spin. (Il moto dei nodi dava ~0: era il
                    # dito; l'asse del campo e' la luna.)
                    try:
                        wI = I2[idx_m]
                        cmA = (P[idx_m] * wI[:, None]).sum(0) / max(wI.sum(), 1e-9)
                        rA = (P[idx_m] - cmA)[:, :2]
                        # tensore d'inerzia pesato 2D -> asse principale
                        Ixx = np.sum(wI * rA[:,0]**2); Iyy = np.sum(wI * rA[:,1]**2)
                        Ixy = np.sum(wI * rA[:,0]*rA[:,1])
                        ang_asse = 0.5 * np.arctan2(2*Ixy, Ixx - Iyy)   # orientazione asse (rad)
                        if hasattr(net, '_ang_asse_prec') and net._ang_asse_prec is not None:
                            dang = ang_asse - net._ang_asse_prec
                            dang = (dang + np.pi/2) % np.pi - np.pi/2    # wrap in (-pi/2,pi/2] (asse ha periodo pi)
                            m0_Lz = float(dang)                          # rotazione asse per step = precessione
                            m0_Lz_norm = float(dang)                     # (gia' velocita' angolare per step)
                        net._ang_asse_prec = ang_asse
                    except Exception:
                        pass
                    vphi_m = net.phivel[idx_m]
                    wpos = np.clip(pesi_m, 0.0, None)              # peso solo dai nodi coerenti (nucleo)
                    if wpos.sum() > 1e-9:
                        m0_spin = float(np.sum(vphi_m * wpos) / wpos.sum())   # spin medio pesato
                        m0_spin_disp = float(np.sqrt(np.sum(wpos*(vphi_m - m0_spin)**2)/wpos.sum()))  # dispersione
                    # SPIN TOPOLOGICO: la massa e' una struttura VORTICE-ANTIVORTICE. I vortici
                    # (singolarita' di fase, +-2pi) NON stanno nel nucleo coerente ma nel GUSCIO,
                    # al confine nucleo/vuoto. Quindi li cerco sui nodi entro un raggio dal centro
                    # della massa (nucleo + guscio), non sui soli nodi tracciati (che sono il nucleo).
                    # Plaquette method su Delaunay 2D: carica netta (vortici - antivortici) = spin
                    # topologico della massa, misurato ~+1 quantizzato.
                    try:
                        from scipy.spatial import Delaunay as _Del
                        d_cm = np.linalg.norm(P[:, :2] - cm[:2], axis=1)
                        sel_v = np.where(d_cm < max(4.0*m0_raggio, 3.0))[0]   # nucleo + guscio
                        if len(sel_v) >= 8:
                            P2 = P[sel_v][:, :2]
                            ph = np.angle(net.psi[sel_v])
                            tri = _Del(P2).simplices
                            def _wrap(dd): return (dd + np.pi) % (2*np.pi) - np.pi
                            pa, pb, pc = ph[tri[:,0]], ph[tri[:,1]], ph[tri[:,2]]
                            circ = _wrap(pb-pa) + _wrap(pc-pb) + _wrap(pa-pc)
                            q = np.round(circ/(2*np.pi)).astype(int)
                            m0_vort_pos = int(np.sum(q > 0))
                            m0_vort_neg = int(np.sum(q < 0))
                            m0_carica = int(np.sum(q))     # carica topologica netta = spin della massa
                    except Exception:
                        pass
        except Exception:
            pass
        cols['m0_I2pesata'] = m0_I2pesata
        cols['m0_raggio'] = m0_raggio
        cols['m0_N'] = m0_N
        cols['m0_coer'] = m0_coer
        cols['m0_spin'] = m0_spin        # spin coerente locale (vphi media pesata)
        cols['m0_spin_disp'] = m0_spin_disp   # dispersione dello spin (bassa=coerente)
        cols['m0_vort_pos'] = m0_vort_pos     # numero di vortici (+1)
        cols['m0_vort_neg'] = m0_vort_neg     # numero di antivortici (-1)
        cols['m0_carica'] = m0_carica         # carica topologica netta = SPIN della massa
        cols['m0_coer_nucleo'] = m0_coer_nucleo   # coerenza del solo NUCLEO denso (locale)
        cols['m0_N_nucleo'] = m0_N_nucleo         # solitoni nel nucleo
        cols['m0_raggio_nucleo'] = m0_raggio_nucleo  # raggio del nucleo
        cols['m0_Lz'] = m0_Lz              # rotazione asse pattern per step = PRECESSIONE (spin)
        cols['m0_Lz_norm'] = m0_Lz_norm

        # ============ MULTIMASSA: tutte le masse + interazioni tra coppie ============
        # Estende la misura a OGNI massa (m0, m1, ... qualsiasi tipo e numero) e calcola
        # la coerenza e la precessione TRA le masse (grandezze di interazione).
        try:
            # COORTI seminate: traccia TUTTE le masse messe nella scena (qualsiasi numero/tipo),
            # non i cluster del tracking (che fonde le masse vicine, es. FILA RADIALE 6->2).
            _coorti = None
            try:
                # 'test' e' la globale del modulo; le coorti sono le masse seminate dalla scena
                if isinstance(test, dict) and test.get('dati', {}).get('coorti'):
                    _coorti = test['dati']['coorti']
            except Exception:
                _coorti = None
            if _coorti:
                # uso le coorti: ogni etichetta = una massa, indici dei nodi seminati (entro n)
                info = {}
                for i_lab, (lab, idx0) in enumerate(sorted(_coorti.items())):
                    idxA = np.array([ii for ii in np.asarray(idx0) if ii < n])
                    if len(idxA) >= 2:
                        pesA = np.ones(len(idxA))  # coorti: peso uniforme (non c'e' concorrenza)
                        wI = I2[idxA]
                        cmM = (P[idxA]*wI[:,None]).sum(0)/max(wI.sum(),1e-9)
                        dcm = np.linalg.norm(P[idxA]-cmM, axis=1)
                        r_nuc = max(np.percentile(dcm,25), 1.0); nuc = dcm < r_nuc
                        rA=(P[idxA]-cmM)[:,:2]
                        Ixx=np.sum(wI*rA[:,0]**2); Iyy=np.sum(wI*rA[:,1]**2); Ixy=np.sum(wI*rA[:,0]*rA[:,1])
                        angM=0.5*np.arctan2(2*Ixy, Ixx-Iyy)
                        # coerenza della coorte = |media e^{i phi}| dei suoi nodi (ordine di fase)
                        zc=np.mean(np.exp(1j*net.phi[idxA]))
                        coer_c=float(np.abs(zc))
                        znuc=np.mean(np.exp(1j*net.phi[idxA[nuc]])) if nuc.sum()>=3 else zc
                        info[i_lab]=dict(idx=idxA, pesi=pesA, cm=cmM, ang=angM,
                                         coer=coer_c,
                                         coer_nuc=float(np.abs(znuc)),
                                         N=int(len(idxA)),
                                         spin=float(np.mean(net.phivel[idxA])),
                                         tipo=lab)
                mids = sorted(info.keys())
            elif getattr(net, 'conc_nodi', None) and getattr(net, 'masse_info', None):
                mids = sorted(net.masse_info.keys())
                info = {}
                for i_mid, mid in enumerate(mids):
                    idxL = []; pesL = []
                    for k in range(min(len(net.conc_nodi), n)):
                        for voce in net.conc_nodi[k]:
                            if voce[0] == mid:
                                idxL.append(k); pesL.append(voce[2]); break
                    if len(idxL) >= 2:
                        idxA = np.array(idxL); pesA = np.array(pesL)
                        wI = I2[idxA]
                        cmM = (P[idxA]*wI[:,None]).sum(0)/max(wI.sum(),1e-9)
                        dcm = np.linalg.norm(P[idxA]-cmM, axis=1)
                        r_nuc = max(np.percentile(dcm,25), 1.0); nuc = dcm < r_nuc
                        # angolo asse principale (per la precessione interna)
                        rA=(P[idxA]-cmM)[:,:2]
                        Ixx=np.sum(wI*rA[:,0]**2); Iyy=np.sum(wI*rA[:,1]**2); Ixy=np.sum(wI*rA[:,0]*rA[:,1])
                        angM=0.5*np.arctan2(2*Ixy, Ixx-Iyy)
                        info[mid]=dict(idx=idxA, pesi=pesA, cm=cmM, ang=angM,
                                       coer=float(np.mean(pesA)),
                                       coer_nuc=float(np.mean(pesA[nuc])) if nuc.sum()>=3 else float(np.mean(pesA)),
                                       N=int(len(idxA)),
                                       spin=float(np.sum(net.phivel[idxA]*np.clip(pesA,0,None))/max(np.clip(pesA,0,None).sum(),1e-9)),
                                       tipo=net.masse_info[mid].get('tipo','massa'))
                # colonne PER OGNI massa (mI_*)
                for i_m, mid in enumerate(mids):
                    if mid not in info: continue
                    d=info[mid]
                    cols['m%d_N'%i_m]=d['N']
                    cols['m%d_coer'%i_m]=round(d['coer'],4)
                    cols['m%d_coer_nucleo'%i_m]=round(d['coer_nuc'],4)
                    cols['m%d_spin'%i_m]=round(d['spin'],5)
                    # precessione INTERNA di questa massa (rotazione asse per step)
                    key='_ang_prec_%d'%mid
                    if hasattr(net,key) and getattr(net,key) is not None:
                        dang=d['ang']-getattr(net,key); dang=(dang+np.pi/2)%np.pi-np.pi/2
                        cols['m%d_Lz'%i_m]=round(float(dang),6)
                    else:
                        cols['m%d_Lz'%i_m]=0.0
                    setattr(net,key,d['ang'])
                cols['n_masse']=len(info)
                # ============ INTERAZIONI tra coppie di masse ============
                # coerenza TRA massa a e b = |<e^{i(phi_a-phi_b)}>| sui rispettivi nodi (fasi medie)
                # precessione ORBITALE = rotazione dell'asse congiungente i due baricentri per step
                mm=[mid for mid in mids if mid in info]
                for a in range(len(mm)):
                    for b in range(a+1, len(mm)):
                        ida, idb = info[mm[a]]['idx'], info[mm[b]]['idx']
                        # fase media (coerente) di ciascuna massa
                        za=np.mean(np.exp(1j*net.phi[ida])); zb=np.mean(np.exp(1j*net.phi[idb]))
                        # coerenza tra le due = |media prodotto|; cos della differenza di fase media
                        coer_ab=float(np.abs(za)*np.abs(zb))  # ampiezza congiunta
                        dphi_ab=float(np.angle(za)-np.angle(zb))
                        cos_ab=float(np.cos(dphi_ab))         # +1 in fase, -1 opposizione
                        cols['coer_%d%d'%(a,b)]=round(coer_ab,4)
                        cols['cosphi_%d%d'%(a,b)]=round(cos_ab,4)
                        # precessione orbitale: angolo della congiungente dei baricentri
                        cong=info[mm[b]]['cm'][:2]-info[mm[a]]['cm'][:2]
                        ang_orb=float(np.arctan2(cong[1], cong[0]))
                        keyo='_ang_orb_%d_%d'%(mm[a],mm[b])
                        if hasattr(net,keyo) and getattr(net,keyo) is not None:
                            do=ang_orb-getattr(net,keyo); do=(do+np.pi)%(2*np.pi)-np.pi
                            cols['Lz_orb_%d%d'%(a,b)]=round(float(do),6)  # precessione orbitale per step
                        else:
                            cols['Lz_orb_%d%d'%(a,b)]=0.0
                        setattr(net,keyo,ang_orb)
                        # distanza tra le masse (nell'interferenza: baricentri pesati |Psi|^2)
                        cols['dist_%d%d'%(a,b)]=round(float(np.linalg.norm(cong)),3)
                # ============ GUSCIO E CENTRO COLLETTIVI (test gauge emergente) ============
                # Ipotesi: N masse in configurazione chiusa generano strutture di fase collettive
                # (candidato campo di gauge emergente). Misuriamo DUE regioni:
                #  - CENTRO: dentro la configurazione, verso il baricentro (il pozzo/valle collettiva)
                #  - GUSCIO: anello attorno a ciascuna massa, fuori dai nuclei (la "buccia" di antifase)
                try:
                    if len(mm) >= 2:
                        P = net.pos[:net.n]
                        cms = np.array([info[m]['cm'][:2] for m in mm])
                        bar = cms.mean(axis=0)
                        r_masse = np.mean([np.linalg.norm(info[m]['cm'][:2]-bar) for m in mm])
                        dr = np.linalg.norm(P[:,:2]-bar, axis=1)
                        # distanza dal nucleo di massa piu' vicino
                        dmin_nuc = np.full(net.n, 1e9)
                        for m in mm:
                            cm = info[m]['cm'][:2]
                            dmin_nuc = np.minimum(dmin_nuc, np.linalg.norm(P[:,:2]-cm, axis=1))
                        # fase media dei nuclei (riferimento)
                        fasi_nuc = [np.angle(np.mean(np.exp(1j*net.phi[info[m]['idx']]))) for m in mm]
                        fase_nuc_media = np.angle(np.mean(np.exp(1j*np.array(fasi_nuc))))

                        # --- CENTRO: dentro la configurazione, lontano dai nuclei ---
                        # (la struttura collettiva: pozzo/valle. cosphi<0 = antifase con le masse)
                        centro = (dr < r_masse*0.7) & (dmin_nuc > 1.3)
                        nc = int(centro.sum())
                        cols['centro_N'] = nc
                        if nc > 3:
                            zc = np.mean(np.exp(1j*net.phi[:net.n][centro]))
                            cols['centro_coer'] = round(float(np.abs(zc)),4)
                            cols['centro_cosphi'] = round(float(np.cos(np.angle(zc)-fase_nuc_media)),4)
                        else:
                            cols['centro_coer']=0.0; cols['centro_cosphi']=0.0

                        # --- ANELLO attorno al centro: i nodi tra il pozzo centrale e le masse ---
                        # Qui si misura l'OLONOMIA (circolazione netta di fase lungo un giro attorno
                        # al centro del triangolo = firma di gauge emergente / carica topologica).
                        anello = (dr > r_masse*0.3) & (dr < r_masse*0.85) & (dmin_nuc > 1.3)
                        ng = int(anello.sum())
                        cols['guscio_N'] = ng
                        if ng > 5:
                            phg = net.phi[:net.n][anello]
                            zg = np.mean(np.exp(1j*phg))
                            cols['guscio_coer'] = round(float(np.abs(zg)),4)
                            cols['guscio_cosphi'] = round(float(np.cos(np.angle(zg)-fase_nuc_media)),4)
                            # OLONOMIA: ordino per angolo attorno al baricentro, sommo i salti di fase
                            # lungo il giro chiuso. Netto intero != 0 = carica di gauge topologica.
                            pg = net.pos[:net.n][anello]
                            ang_pos = np.arctan2(pg[:,1]-bar[1], pg[:,0]-bar[0])
                            o = np.argsort(ang_pos)
                            phi_ord = phg[o]
                            salti = np.diff(np.unwrap(np.concatenate([phi_ord, phi_ord[:1]])))
                            cols['guscio_circ'] = round(float(np.sum(salti)/(2*np.pi)),4)
                        else:
                            cols['guscio_coer']=0.0; cols['guscio_cosphi']=0.0; cols['guscio_circ']=0.0
                except Exception:
                    pass
        except Exception as _e:
            pass
        return cols

    # ordine fisso delle colonne del log diagnostico
    _DIAG_COLS = ['step','n','n_archi','I2_min','I2_max','I2_mean','I2_absmax',
                  'r_min','r_max','r_mean','tw_min','tw_max','tw_mean','tw_absmax',
                  'phi_min','phi_max','phi_mean','phivel_min','phivel_max','phivel_mean','phivel_absmax',
                  'd_min','d_max','d_mean','d0_min','d0_max','d0_mean','eta_min','eta_max','eta_mean',
                  'tau_min','tau_max','tau_mean','dmin_nodi','xi_termo','n_naninf','n_I2_grandi','n_lontani',
                  'm0_I2pesata','m0_raggio','m0_N','m0_coer','m0_spin','m0_spin_disp',
                  'm0_vort_pos','m0_vort_neg','m0_carica',
                  'm0_coer_nucleo','m0_N_nucleo','m0_raggio_nucleo','m0_Lz','m0_Lz_norm']

    def _regione_centrale(net, raggio_c=1.5):
        # la regione centrale e' attorno al BARICENTRO del sistema (origine), valida per ogni N
        n = net.n; P = net.pos[:n]
        return np.where(np.linalg.norm(P, axis=1) < raggio_c)[0]

    def _ordine(net, idx):
        n = net.n; P = net.pos[:n]; phi = net.phi[:n]
        idx = idx[idx < n]
        if len(idx) < 4 or cKDTree is None: return None
        tree = cKDTree(P); ol = []
        for i in idx[:400]:
            vic = tree.query_ball_point(P[i], 1.0)
            if len(vic) >= 3: ol.append(abs(np.exp(1j*phi[vic]).mean()))
        return float(np.mean(ol)) if ol else None

    def _gusci_esterni(net, cm, R_masse):
        """Cerca il GUSCIO DI ANTIFASE che avvolge l'insieme dei nuclei: nel sistema il guscio di
        una massa e' un anello di DECOERENZA (annullamento fra domini in antifase), non di materia.
        Quindi a scala superiore il guscio e' un anello a r>R_masse dove la coerenza LOCALE crolla
        (minimo di coerenza) pur essendoci nodi: una superficie di antifase che separa l'oggetto
        dal vuoto. Restituisce (raggio, coerenza_locale_minima, n_nodi, tau) dell'anello di antifase
        piu' netto oltre le masse, o None. Coerenza locale bassa MA con nodi presenti = guscio.
        ADATTIVO: la finestra di ricerca si estende fino al BORDO reale dei nodi (il guscio si
        espande con la massa, non sta a raggio fisso), e il guscio e' identificato come una CADUTA
        netta di coerenza (minimo locale pronunciato rispetto ai vicini), non il minimo assoluto,
        cosi' si distingue un vero anello di antifase dal semplice sfumare del bordo."""
        n = net.n; P = net.pos[:n]
        r = np.linalg.norm(P - cm, axis=1)
        tau = net.ritmo()
        try:
            from scipy.spatial import cKDTree
            tree = cKDTree(P); phi = net.phi[:n]
        except Exception:
            tree = None
        prof = []
        rmax = float(r.max())
        passo_r = 0.5
        rr = R_masse
        # ADATTIVO: scandaglio fino al bordo reale dei nodi (rmax), non R_masse+6 fisso.
        # Cosi' un guscio che si e' espanso lontano viene comunque trovato.
        while rr < rmax:
            sel = np.where((r >= rr) & (r < rr + passo_r))[0]
            if len(sel) >= 4:
                if tree is not None:
                    cl = []
                    for i in sel[:80]:
                        vic = tree.query_ball_point(P[i], 1.0)
                        if len(vic) >= 3: cl.append(abs(np.exp(1j*phi[vic]).mean()))
                    coer_loc = float(np.mean(cl)) if cl else 1.0
                else:
                    coer_loc = 1.0
                tmed = float(tau[sel].mean()) if tau is not None else 0.0
                prof.append((rr + passo_r/2, coer_loc, len(sel), tmed))
            rr += passo_r
        if len(prof) < 3: return None
        arr = np.array([[p[0], p[1], p[2], p[3]] for p in prof])
        # GUSCIO = CADUTA NETTA di coerenza locale: un anello che e' minimo rispetto ai vicini E
        # significativamente sotto la coerenza tipica del profilo (non il semplice sfumare del bordo).
        coer = arr[:, 1]
        soglia = float(np.median(coer)) - 0.5 * float(np.std(coer))   # sotto la tipica meno mezza std
        # cerco minimi locali (piu' bassi dei vicini immediati) sotto la soglia
        candidati = []
        for k in range(1, len(coer) - 1):
            if coer[k] <= coer[k-1] and coer[k] <= coer[k+1] and coer[k] < soglia and arr[k, 2] >= 4:
                # profondita' del minimo: quanto e' sotto la coerenza dei bordi dell'anello
                prof_locale = 0.5*(coer[k-1] + coer[k+1]) - coer[k]
                candidati.append((k, prof_locale))
        if candidati:
            # il guscio piu' NETTO = minimo locale piu' profondo (caduta di antifase piu' marcata)
            ipk = max(candidati, key=lambda c: c[1])[0]
        else:
            # nessun anello netto: ripiego sul minimo assoluto (comportamento precedente)
            ipk = int(np.argmin(coer))
        return (float(arr[ipk, 0]), float(arr[ipk, 1]), int(arr[ipk, 2]), float(arr[ipk, 3]))

    def _classifica_tracking(net, ids_massa):
        """CLASSIFICAZIONE ROBUSTA con il tracking di concorrenza (sostituisce le coorti a indici,
        fragili alla mitosi). Distingue tre categorie di materia contando i nodi per come concorrono
        alle masse:
          - accrescimento (mitosi): nodi che concorrono a una massa registrata, ereditati per mitosi
          - creazione_coppie (Schwinger): nodi Schwinger che concorrono a una massa (voce 'schwinger')
          - materia_nuova: nodi che NON concorrono a nessuna massa (nati dal vuoto/vuoto teso)
        Ritorna un dict coi conteggi e, per ogni massa, il peso corrente totale."""
        net.aggiorna_pesi_concorrenza()
        n_accr = 0; n_schw = 0; n_nuova = 0
        for k in range(min(len(net.conc_nodi), net.n)):
            voci = net.conc_nodi[k]
            if not voci:
                n_nuova += 1
            elif any(len(v) >= 4 and v[3] == "schwinger" for v in voci):
                n_schw += 1
            else:
                n_accr += 1
        tr = net.tracking_masse()
        pesi = {mid: tr[mid]["peso_tot_corrente"] for mid in ids_massa if mid in tr}
        return dict(accrescimento=n_accr, creazione_coppie=n_schw, materia_nuova=n_nuova, pesi_masse=pesi)

    def _picchi_nuovi(net, centri_sem, soglia_rel=0.5, dist_nuovo=1.5):
        """MATERIA ISOLATA CHE SI CREA (guarda la luna non il dito): cerca i picchi del campo di
        interferenza |Psi|^2 su griglia 3D. Un picco = una massa. I picchi LONTANI dai centri
        seminati (oltre dist_nuovo) sono materia NUOVA, nata dal vuoto e staccata. Restituisce
        (n_picchi_totali, n_picchi_nuovi, raggio del picco nuovo piu' esterno)."""
        n = net.n; P = net.pos[:n]
        net.calcola_psi(); I2 = np.abs(net.psi[:n])**2
        est = float(np.abs(P).max()) + 1.0
        G = 24
        grid = np.zeros((G, G, G))
        gi = ((P + est)/(2*est)*(G-1)).astype(int).clip(0, G-1)
        for k in range(n):
            grid[gi[k,0], gi[k,1], gi[k,2]] += I2[k]
        grid = gaussian_filter(grid, 1.0)
        from scipy.ndimage import maximum_filter
        mx = (grid == maximum_filter(grid, 3)) & (grid > grid.max()*soglia_rel)
        picchi = np.argwhere(mx)
        n_tot = len(picchi); n_nuovi = 0; r_nuovo = 0.0
        for pk in picchi:
            pos = pk/(G-1)*2*est - est
            vicino = any(np.linalg.norm(pos[:2] - c[:2]) < dist_nuovo for c in centri_sem)
            if not vicino:
                n_nuovi += 1
                r_nuovo = max(r_nuovo, float(np.linalg.norm(pos[:2])))
        return n_tot, n_nuovi, r_nuovo

    # centri seminati in 2D per il rilevatore di picchi nuovi
    centri_sem = [np.array([cx, cy]) for (cx, cy) in centri]

    # intestazione CSV
    righe = ["passo,n_tot,ord_centrale,dens_centrale,n_centrali,frac_nati_centrali,"
             "dist_masse,dens_picco_centrale,ord_masse,"
             "antiguscio_raggio,antiguscio_coerenza_min,antiguscio_nodi,antiguscio_tau,"
             "picchi_totali,picchi_nuovi,raggio_picco_nuovo"]
    print("\npasso | dens_centr | dist_masse | ANTIGUSCIO(r,c,n) | PICCHI(tot,NUOVI)")
    t0 = _t.time()
    # LOG DIAGNOSTICO COMPLETO: una riga per OGNI step con tutte le variabili di stato.
    # Attivato da --diaglog PERCORSO. Serve a catturare l'istante dell'artefatto (quale grandezza
    # degenera per prima). File separato dal CSV normale.
    diag_path = getattr(a, "diaglog", None)
    diag_f = None
    _diag_header = None   # header dinamico: fissato alla prima riga (include colonne multimassa)
    if diag_path:
        diag_f = open(diag_path, "w")
        print(f"[batch] LOG DIAGNOSTICO COMPLETO attivo -> {diag_path} (una riga per ogni step)")
    for step in range(passi + 1):
        if step > 0:
            _passo(net)
        if diag_f is not None:
            d = _diag_completa(net, step); d['step'] = step
            if _diag_header is None:
                # ordine: colonne fisse note, poi le extra multimassa/interazione in coda
                extra = [k for k in d.keys() if k not in _DIAG_COLS]
                _diag_header = list(_DIAG_COLS) + extra
                diag_f.write(",".join(_diag_header) + "\n")
            diag_f.write(",".join(str(d.get(c, '')) for c in _diag_header) + "\n")
            diag_f.flush()   # flush a ogni step: se il run si blocca, il log fino al blocco e' salvo
        if step % ogni == 0:
            n = net.n
            idxc = _regione_centrale(net)
            net.calcola_psi(); I2 = np.abs(net.psi[:n])**2
            ordc = _ordine(net, idxc)
            densc = float(I2[idxc].mean()) if len(idxc) else 0.0
            picco = float(I2[idxc].max()) if len(idxc) else 0.0
            nati_centrali = [i for i in idxc if i >= n_orig]
            frac_nati = (len(nati_centrali)/len(idxc)) if len(idxc) else 0.0
            P = net.pos[:n]
            # baricentri di TUTTE le coorti (masse) ancora presenti
            baric_masse = []
            for co in coorti:
                ic = np.array([i for i in co if i < n])
                if len(ic) > 2: baric_masse.append(P[ic].mean(0))
            baric_masse = np.array(baric_masse) if baric_masse else np.zeros((0,3))
            # "dist_masse": raggio medio delle masse dal baricentro del sistema (per N generico
            # e' la misura giusta: se le masse restano al loro posto resta ~sep, se collassano cala)
            if len(baric_masse) >= 2:
                cm = baric_masse.mean(0)
                raggi = np.linalg.norm(baric_masse - cm, axis=1)
                distm = float(raggi.mean() * 2)  # diametro medio: confrontabile col caso a 2 masse
                ordm = _ordine(net, np.concatenate([np.array([i for i in co if i < n]) for co in coorti]))
            else:
                cm = np.zeros(3); distm = -1; ordm = None
            # GUSCIO DI ANTIFASE. Due tipi in una configurazione multi-massa:
            #   (collettivo) l'anello che avvolge TUTTO l'insieme, a r>R_masse dal baricentro;
            #   (singolo) il guscio di CIASCUNA massa, attorno al suo centro (a r piccolo dal centro
            #             della massa). Cerco prima il collettivo; se assente, il piu' netto fra i
            #             gusci delle singole masse (scandagliati dal loro centro, catturano il
            #             guscio anche quando e' interno al cerchio delle masse).
            gusc = None
            if len(baric_masse) >= 2:
                R_masse = float(np.linalg.norm(baric_masse - cm, axis=1).max()) + 1.2
                gusc = _gusci_esterni(net, cm, R_masse)   # collettivo
            if gusc is None:
                # ripiego: guscio delle singole masse (dal centro di ognuna, partendo da vicino)
                migliore = None
                for bm in baric_masse:
                    g = _gusci_esterni(net, bm, 0.5)
                    if g is not None and (migliore is None or g[1] < migliore[1]):
                        migliore = g   # il guscio a coerenza piu' bassa (antifase piu' netta)
                gusc = migliore
            gr, gc, gn, gt = (gusc if gusc else ('', '', '', ''))
            # MATERIA ISOLATA CHE SI CREA: picchi di interferenza nuovi (lontani dalle masse seminate)
            p_tot, p_nuovi, r_nuovo = _picchi_nuovi(net, centri_sem)
            # CLASSIFICAZIONE ROBUSTA col tracking (accrescimento / creazione_coppie / materia_nuova)
            cls = _classifica_tracking(net, ids_massa)
            righe.append(f"{step},{n},{ordc if ordc is not None else ''},{densc:.5f},{len(idxc)},"
                         f"{frac_nati:.3f},{distm:.3f},{picco:.5f},{ordm if ordm is not None else ''},"
                         f"{gr if gr=='' else '%.2f'%gr},{gc if gc=='' else '%.5f'%gc},"
                         f"{gn if gn=='' else gn},{gt if gt=='' else '%.3f'%gt},"
                         f"{p_tot},{p_nuovi},{r_nuovo:.2f},"
                         f"{cls['accrescimento']},{cls['creazione_coppie']},{cls['materia_nuova']}")
            gstr = (f"r={gr:.1f} c={gc:.3f} n={gn}" if gusc else "nessuno")
            print(f"  {step:5d} | {densc:9.4f} | {distm:9.3f} | {gstr:22s} | tot={p_tot} NUOVI={p_nuovi}"
                  f" | TRACK accr={cls['accrescimento']} coppie={cls['creazione_coppie']} "
                  f"nuova={cls['materia_nuova']}",
                  flush=True)
    dt = _t.time() - t0
    if diag_f is not None:
        diag_f.close()
        print(f"[batch] log diagnostico completo salvato in {diag_path}")
    with open(a.csv, "w") as f:
        f.write("\n".join(righe) + "\n")
    print(f"\n[batch] completato in {dt:.1f}s, {passi} passi. CSV salvato in {a.csv}")
    print("[batch] LETTURA condensazione: se dens_centrale e n_centrali CRESCONO e frac_nati resta")
    print("        ALTA mentre dist_masse NON crolla -> NUOVA massa dal vuoto (non accrescimento).")
    print("[batch] LETTURA picchi_nuovi: se picchi_nuovi passa da 0 a >=1 a un certo passo, quello e'")
    print("        il momento in cui una MASSA NUOVA si stacca dal vuoto (materia isolata che si crea).")
    print("[batch] LETTURA antiguscio: se compare un anello a coerenza_min BASSA (antifase) e raggio")
    print("        stabile oltre le masse, con nodi presenti -> GUSCIO DI ANTIFASE che avvolge i nuclei")
    print("        = massa di scala superiore (il guscio del sistema e antifase, non materia).")


def _applica_regime(a):
    """Applica il --regime da riga di comando, rivalutando i globali che dipendono dal REGIME
    (SCUOTIMENTO, G_PH, TAU_A, _CALORE_INIT), valutati al caricamento del modulo prima del parsing.
    Vale per headless e interattivo: va chiamata dopo il parsing e prima di evolvere la rete."""
    reg = getattr(a, "regime", None)
    if reg is None:
        return  # nessun override: resta il REGIME impostato in testa al file
    global REGIME, SCUOTIMENTO, G_PH, TAU_A, _CALORE_INIT
    REGIME = reg
    if reg == "deterministico":
        SCUOTIMENTO = False; G_PH = 3e-3; TAU_A = 50.0; _CALORE_INIT = 0.4
    else:
        SCUOTIMENTO = True;  G_PH = 0.15; TAU_A = 2.0;  _CALORE_INIT = 0.0
    print(f"[regime] '{reg}' da riga di comando: SCUOTIMENTO={SCUOTIMENTO} G_PH={G_PH} "
          f"TAU_A={TAU_A} calore_init={_CALORE_INIT}", flush=True)


if __name__ == "__main__":
    if len(_sys.argv) > 1:
        a = _cli()
        _applica_regime(a)   # applica --regime (se dato) prima di ogni ramo: batch/headless/interattivo
        if getattr(a, "batch", None):
            batch_condensazione(a)
        elif a.test is not None:
            # scenario headless: registra un video
            esegui_headless(a)
        else:
            # modalita' INTERATTIVA con i flag applicati (coarse-graining incluso).
            # Tutti i flag valgono qui come in headless; le leggi sono attive di default.
            _applica_flag(a)
            print("[interattivo] flag applicati - tutte le leggi attive. "
                  f"lambda={LAM:.3f} scala_B={SCALA_B:.0f} mu_psi={MU_PSI} "
                  f"coppia={COPPIA_MIT} mitmax={MITMAX}")
            ani = FuncAnimation(fig, update, frames=10_000_000, interval=20, repeat=False)
            plt.show()
    else:
        # interattivo puro, senza flag: le leggi importanti sono comunque attive di default
        ani = FuncAnimation(fig, update, frames=10_000_000, interval=20, repeat=False)
        plt.show()