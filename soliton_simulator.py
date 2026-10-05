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
#   portata dell'interferenza dove e' denso, con una TRANSIZIONE DOLCE, non un
#   muro: la portata e' determinata dal rapporto u = rho/rho_c. Il
#   ⚠⚠ CORREZIONE DEL 2026-10-03, rilievo del guardiano: QUI C'ERA SCRITTO <<(tanh)>>,
#      E IL CODICE NON USA tanh. Usa `fattore = 1 / (1 + softplus(u - 1))`, con
#      `softplus = log1p(exp(clip(u-1, -30, 30)))` (:5003-5004).
#      ### E LA DIFFERENZA NON E' UNA SFUMATURA, ed e' misurata:
#        softplus: fattore -> 1/u per u grande, cioe' NON SATURA e la portata -> 0;
#        tanh:     fattore -> 0.5 per u grande, cioe' SATURA a metA' portata.
#      ### E A u = 0 `1/(1+tanh(u-1))` darebbe 4.19, cioe' ALLUNGHEREBBE la portata:
#        quindi la frase vecchia non era imprecisa, ### DESCRIVEVA UNA LEGGE DIVERSA
#        da quella scritta.
#      ### E LA SCELTA softplus NON E' MOTIVATA DA NESSUNA PARTE: voce
#        `SCHERMATURA-LEGGE-REVISIONE`.
#      ### E UN FATTO MISURATO CHE NESSUNO AVEVA SCRITTO: a u -> 0 il fattore e'
#        0.761463, cioe' la portata e' TAGLIATA DEL 23.85% ANCHE DOVE LA DENSITA'
#        E' NULLA -- la schermatura NON RESTITUISCE MAI `LAM`. E il `lambda` MAX
#        misurato nel run del driver e' 0.609170 = `LAM * 0.761463` ESATTAMENTE:
#        ### nessun nodo sta nel regime <<non schermato>>.
#   grumo puo' stabilizzarsi a taglia finita (massa si assesta, non cresce senza
#   limite, e lambda resta finita). Il nucleo denso, schermato, smette
#   di sentire la propria interferenza collettiva -> mitosi non alimentata -> stop.
#   Collega spin/ordine: nucleo = cristallizzato (spin allineati, sync forte perche'
#   denso); guscio = liquido (spin frustrati, sync debole perche' rado). Stabilita'
#   = cristallizzazione che si chiude quando la schermatura isola il denso.
#
# IMPLEMENTATO: scala e profondita' della schermatura sono ancorate a N_critico;
#   il limite inferiore e' geometrico (15% di LAM), non una manopola di taratura.
#   Il vincolo buchi neri resta: schermatura totale = orizzonte deve restare possibile
#      (schermatura parziale = materia stabile; totale = buco nero).
#   Da validare su TEMPI LUNGHI (hardware di Luca): taglia stabile e coerente?
#
# NB: la schermatura e' ora sempre ancorata a N_c. P_LAM e LAM_MIN non sono piu'
#   parametri fisici; COPPIA_DENSITA e ANTIFASE_ADD restano esplorativi indipendenti.
# ============================================================================
import numpy as np

# ============================================================================
# INTERRUTTORE DI REGIME
#
# ⚠⚠ CHE COSA GIRA, E DA QUANDO -- e i commenti di prima dicevano IL CONTRARIO
#   ### GIRA IL DETERMINISTICO, E GIRA DAL 2026-08-28 (commit `670310f`). Tutto: ogni test, ogni
#       sigillo, ogni misura di questo repo.
#   ### LO STOCASTICO NON LO GIRA NESSUNO, E NESSUN SIGILLO LO COPRE. Non e' un'opinione: nessuno
#       script di `csv/_test_fork/` ne' di `csv/_seal_fork/` lo seleziona -- lo nominano SOLO le
#       copie vecchie del simulatore (`_old_sim_pre_*.py`), che sono reperti, non strumenti.
#   ### E DUE STRUMENTI PASSANO `--regime`, ma per passare "deterministico": `_osserva_vuoto.py`
#       e `_sigillo_osservatore.py`. ⚠ E NON E' RIDONDANTE, ED E' LA TRAPPOLA `--regime`:
#       passare il flag CAMBIA `SCUOTIMENTO` (vedi `_applica_regime`), perche' qui sotto il ramo
#       di modulo mette `_SCUOTIMENTO_REGIME = True` in ENTRAMBI i casi, mentre `_applica_regime`
#       lo mette `False` per il deterministico. ### LO STESSO NOME DI REGIME DA' DUE SISTEMI
#       DIVERSI, a seconda che il flag sia passato o no.
#   [COMMIT 0-bis del riordino, 2026-10-01: questo commit corregge SOLO COMMENTI ed e'
#    BYTE-INERTE. NON decide niente sul regime: DICHIARA come stanno le cose.]
#
#   "deterministico" -> ### IL REGIME IN USO, E L'UNICO SIGILLATO. Vuoto SPENTO (al netto della
#                       trappola qui sopra). Mitosi modulata dal TEMPO PROPRIO LOCALE. Impulso
#                       iniziale conservativo nella semina, attrito ridotto.
#                       ⚠ IL COMMENTO DI PRIMA LO CHIAMAVA <<WIP / proof of concept>>: era FALSO
#                         quando l'ho letto, perche' e' il sistema su cui gira TUTTO. Cio' che
#                         resta vero del vecchio testo e' il LIMITE FISICO, e lo tengo: lo stress
#                         resta alto e MANCA L'INNESCO DELLA PRIMA ASIMMETRIA (tau omogeneo
#                         all'inizio). DA RIPRENDERE: seme iniziale di asimmetria strutturale
#                         (fase/torsione).
#   "stocastico"     -> vuoto stocastico ATTIVO: il vuoto fa da termostato e da sorgente di
#                       asimmetria, e la materia condensa dalle sue fluttuazioni.
#                       ⚠ IL COMMENTO DI PRIMA LO CHIAMAVA <<DEFAULT>> e <<il sistema canonico>>:
#                         ### FALSO SU ENTRAMBI. Non e' il default (il default e' la riga qui
#                         sotto) e ### NON E' COPERTO DA NESSUN SIGILLO. <<VALIDATA e STABILE>>
#                         si riferisce all'EPOCA 1, prima del fork SU(2): per l'epoca 2 non
#                         esiste una misura che lo dica.
# APERTO: la PRECESSIONE fra due masse persiste in regime deterministico? Se si', il momento
#         angolare netto NON dipende dal vuoto stocastico (risultato forte).
REGIME = "deterministico"     # <-- `REGIME` E' QUESTO, ED E' CIO' CHE GIRA. L'altro valore di `REGIME` e' "stocastico", che NESSUN SIGILLO COPRE.

if REGIME == "deterministico":
    _SCUOTIMENTO_REGIME = True  
    _G_PH_REGIME = 3e-3        # attrito basso ma non nullo (1e-4 e 0 divergono)
    _TAU_A_REGIME = 50.0       # alta persistenza memoria spinoriale
    _CALORE_INIT = 0.4         # impulso iniziale conservativo (punto zero)
else:
    _SCUOTIMENTO_REGIME = True
    _G_PH_REGIME = 0.15        # ⚠ <<canonico validato>> VALE PER L'EPOCA 1: questo ramo NON gira
    _TAU_A_REGIME = 2.0        # idem: valore dell'epoca 1, in un ramo che NON gira
    _CALORE_INIT = 0.0         # phivel nasce a zero (epoca 1; ramo che NON gira)
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

# [TRACCIA_D0, 2026-09-20] STRUMENTAZIONE DEI DICIANNOVE PUNTI CHE TOCCANO `d0`. OFF di default.
# ⚠ PERCHE' ESISTE: `d0` e' scritto in DODICI punti e limitato da SETTE pavimenti, e NESSUNO era
#   contato. La domanda «chi fa gli otto salti sull'arco 16-481» non ha risposta senza questo.
# ⚠ E PERCHE' UN CONTATORE GLOBALE NON BASTA: direbbe QUANTE VOLTE, non SU QUALE ARCO. Qui si
#   registra il `d0` PRIMA e DOPO ogni sito per un insieme di archi DICHIARATO, piu' la somma
#   ALGEBRICA del delta -- il conteggio da solo non dice chi spinge IN GIU'.
# ⚠ I PAVIMENTI ERANO SITI A PIENO TITOLO, e il `pavimento=` di `_traccia_d0` ne registrava
#   il VALORE. DAL 2026-09-27 QUEI PAVIMENTI SONO ARCHIVIATI (`_floor_d0` e `_pav_d0`, in
#   `csv/_archivio/_pavimenti_morti.py`): `pavimento=` resta nella firma -- e' `None` per
#   difetto -- ma nessun chiamante lo passa piu'.
TRACCIA_D0 = False
# [TRACCIA_VD, 2026-09-21] I TRE TERMINI DI `acc` SEPARATI, COL SEGNO. OFF di default.
# ⚠ PERCHE': imporre `d0 >= LAM` limita lo stress a `d_max/LAM - 1`, e nel ramo B al passo 360
#   vale ancora `185` perche' `d_max = 149`. La cura ferma il DENOMINATORE; il NUMERATORE cresce.
#   La domanda «chi spinge `d`» non era mai stata posta.
# ⚠ SI REGISTRANO I TRE TERMINI SEPARATI E NON LA LORO SOMMA: la somma e' `acc`, che si vedrebbe
#   gia' da `vd`. La domanda e' la RIPARTIZIONE.
TRACCIA_VD = False
# --- [§1 MANDATO GLOBALE 2026-09-21] DIAGNOSTICI SU `peq`. NESSUN FLAG DA RIGA DI COMANDO,
#     di proposito: sono sonde, non fisica, e non devono poter essere accese da un comando.
#     Si impostano direttamente sul modulo, come `TRACCIA_D0` (`_rigiocata_0_120.py:79`).
#     BYTE-INERTI a `False`: aggiungono solo due `if` che non toccano stato ne' RNG.
TRACCIA_PEQ = False       # contatori sull'aggiornamento di `peq` (`:4204-4208`)
FERMA_DOPO_NSUB = False   # alza `StopDopoNsub` appena calcolato `nsub`, per NON integrare
                          # un passo esplosivo: il numero si vuole, i 22591 sotto-passi no.


class DominioViolato(Exception):
    """[C5] Una grandezza di stato e' uscita dal suo DOMINIO FISICO.

    Porta **tutto quello che serve per rigiocarla**: la grandezza, la regola violata, il passo,
    **gli indici** *(arco `i-j` o nodo)*, i **valori**, e la funzione in cui il controllo e'
    scattato. **Un errore rumoroso vale piu' di uno silenzioso.**
    """

    def __init__(self, quale, regola, passo, indici, valori, dove, extra=None):
        self.quale, self.regola, self.passo = quale, regola, passo
        self.indici, self.valori, self.dove = indici, valori, dove
        self.extra = extra or {}
        _idx = ', '.join(str(x) for x in list(indici)[:8])
        _val = ', '.join('%.6e' % v for v in list(valori)[:8])
        super().__init__(
            "[INVARIANTE] `%s` VIOLA `%s` al passo %s, in `%s`.\n"
            "  quanti: %d\n  indici (primi 8): %s\n  valori (primi 8): %s\n  %s"
            % (quale, regola, passo, dove, len(indici), _idx, _val,
               ' '.join('%s=%s' % kv for kv in sorted(self.extra.items()))))


# ============================================================================================
# [C5] IL REGISTRO UNICO DEI DOMINI -- una riga per OGNI grandezza di stato.
#
# ⚠ I CONFINI SONO IL DOMINIO FISICO, NON SOGLIE SCELTE (`A11`, corollario 1).
# ⚠ ANCHE «nessun vincolo, solo FINITO» E' SCRITTO: una grandezza senza regola dichiarata
#   sarebbe una grandezza di cui nessuno ha pensato il dominio.
# ⚠ LA COMPLETEZZA SI VERIFICA DAL CODICE, NON DALLA MEMORIA: il sigillo `I3` confronta questo
#   registro con gli attributi ARRAY dello SNAPSHOT. **Chi aggiunge una grandezza di stato e'
#   OBBLIGATO a dichiararne il dominio, o il sigillo fallisce.**
#
# Forme:  'finito'      nessun NaN, nessun inf
#         'pos'         > 0        'nonneg'   >= 0
#         'segno'       in {-1, +1}
#         'lam'         >= LAM con la scala minima accesa, altrimenti > 0
#         'indice'      intero in [0, n)
#         'fase'        in [0, 4*pi)
#         'unita'       vettore/spinore di norma 1
DOMINI = {
    # --- per ARCO
    'd':        ('lam',    'la lunghezza VERA di un arco'),
    'd0':       ('lam',    'la lunghezza di RIPOSO di un arco'),
    'vd':       ('finito', 'velocita di `d`: nessun vincolo di segno, e non deve esserci'),
    # ⚠ `peq` HA UN'ECCEZIONE DICHIARATA, ed e' un INVARIANTE PIU' FORTE, non piu' debole:
    #   con `PEQ_NASCITA_LOCALE` gli archi di Schwinger nascono `nan` e vengono CALIBRATI
    #   all'inizio del passo dopo. Fra la `mitosi()` e quella calibrazione il `nan` e'
    #   LEGITTIMO -- ma **SOLO sugli archi che `C2` ha marcato**. Un `nan` ALTROVE, o un `nan`
    #   che SOPRAVVIVE a un passo, e' una VIOLAZIONE.
    #   **Trovato dall'invariante stesso al PRIMO passo in cui e' stato acceso:** e' il
    #   mestiere di `C5`, e la risposta giusta non e' allargare la regola ma PRECISARLA.
    'peq':      ('peq',    'la pressione di equilibrio: >= 0, e `nan` SOLO sugli archi marcati'),
    'tw':       ('finito', 'torsione d arco: puo essere di entrambi i segni'),
    'twp':      ('finito', 'torsione precedente'),
    '_rep':     ('finito', 'memoria di repulsione d arco'),
    '_sin2_vir':('finito', 'sin^2 della viriale: in [0,1] per costruzione, si verifica FINITO'),
    '_dt_e_ultimo': ('pos', 'il passo di tempo efficace d arco: un tempo e POSITIVO'),
    'i':        ('indice', 'indice di NODO del lato i di ogni arco'),
    'j':        ('indice', 'indice di NODO del lato j di ogni arco'),
    # --- per NODO
    'psi':      ('finito', 'campo di materia complesso'),
    'phi':      ('fase',   'fase, a doppia copertura: il dominio E [0, 4pi)'),
    'phi0':     ('fase',   'fase di riferimento'),
    'phi_s':    ('finito', 'fase spinoriale: nessun vincolo dichiarato oltre la finitezza'),
    'phivel':   ('finito', 'velocita di fase: entrambi i segni'),
    # [`RAMPA-1`, 2026-09-25] `nonneg_inf` E NON `nonneg`: il vuoto DATO ha `eta = +inf`,
    #   cioe' NESSUN TEMPO DI ACCENSIONE. `+inf` e' NEL DOMINIO di un'eta'; `nan` e `-inf` no.
    'eta':      ('nonneg_inf', 'eta di un nodo: non negativa, e +inf per il vuoto DATO'),
    'pos':      ('finito', 'posizione di DISEGNO: nessun vincolo fisico'),
    'perc_chi': ('segno',  'la CARICA: segno di doppia copertura, in {-1,+1}'),
    'perc_geom':('segno',  'la GEOMETRIA: il giro e compiuto o no, in {-1,+1}'),
    'perc_tw':  ('finito', 'percentuale di torsione'),
    'rho_spin': ('nonneg', 'densita spinoriale: una DENSITA non e negativa'),
    'omega_s':  ('finito', 'velocita angolare spinoriale: entrambi i segni'),
    'mem_mot':  ('finito', 'memoria di moto'),
    '_deg':     ('nonneg', 'grado di un nodo: un CONTEGGIO non e negativo'),
    # [D37, 2026-09-24] LA DERIVAZIONE, spostata qui dalla MIA voce DUPLICATA che stava
    #   150 righe sopra. `cs` NON PUO' ESSERE ZERO, ed e' DERIVATO dal codice, non
    #   misurato: `cs_floor = CS_M/(1 + sqrt(I)*sqrt(1/scala))` ha denominatore >= 1
    #   quindi > 0; `min(cs_floor, CS_M)` lo tiene in (0, CS_M]; e
    #   `transizione = 0.5*(1 + tanh(1 - u))` sta in (0, 1) STRETTO, quindi il ritorno
    #   `cs_floor + (CS_M - cs_floor)*transizione` e' >= cs_floor > 0.
    #   CONSEGUENZA per `CURA 2`: `tau_arco = d/cs_arco` si scrive SENZA clamp, e se mai
    #   fosse zero e' il livello NUMERICO (`np.seterr(divide='raise')`) a fermarsi con
    #   la riga -- non un `np.maximum` che nasconde il caso.
    # ⚠ E QUESTA VOCE ESISTEVA GIA': la mia era un DUPLICATO, e in un letterale di dict
    #   vince l'ULTIMA, quindi la mia era CODICE MORTO. L'ho aggiunta perche' avevo
    #   cercato in una finestra di 28 righe invece che nel file intero (`P1`, `D37`).
    '_cs_nodo_prev': ('pos', 'velocita delle onde metriche: una VELOCITA e positiva'),
    '_r_corrente':   ('pos', 'ritmo dell orologio locale: un RITMO e positivo'),
    '_fatt_cs_ultimo': ('pos', 'fattore di cs: positivo per costruzione'),
    '_psi_prec':  ('finito', 'psi del passo precedente'),
    '_psi_spinor':('unita',  'lo spinore primario: |psi| = 1'),
    '_psi_spin_prec': ('finito', 'spinore del passo precedente'),
    'psi_spin':   ('finito', 'spinore ricostruito nel passo'),
    '_spinor_lift': ('finito', 'sollevamento spinoriale'),
    '_nb':      ('unita',  'versore di Bloch: |n| = 1'),
    '_nb_prec': ('unita',  'versore di Bloch committato'),
    '_nb_ret':  ('unita',  'versore di Bloch RITARDATO'),
    '_xi_rumore': ('finito', 'rumore colorato'),
    '_chi_core_nodi':   ('finito', 'chiralita del core locale'),
    '_chi_geom_nodi':   ('finito', 'chiralita GEOMETRICA, cache separata (CHI_COOP)'),
    '_chi_core_rho0':   ('finito', 'densita di riferimento del core'),
    '_chi_core_raggio': ('nonneg', 'raggio del core: un RAGGIO non e negativo'),
    '_perm':    ('finito', 'permutazione di cache: non e fisica, si verifica finita'),
}


class StopDopoNsub(Exception):
    """DIAGNOSTICO: interrompe `step()` subito dopo il calcolo di `nsub`.

    Alzata SOLO se `FERMA_DOPO_NSUB`. Porta i quattro numeri (`nsub`, `n1`, `n2`, `n3`) sia nel
    messaggio sia in `self._g_nsub_stop`, perche' chi la cattura non debba parsare una stringa.
    """

TRACCIA_D0_COPPIE = ((16, 481),)          # dettaglio PIENO: le coppie di nodi seguite una per una
TRACCIA_D0_NODI = (16, 481, 621, 627, 837)  # riassunto: tutti gli archi di questi nodi
# COARSE-GRAINING (dettare la scala): un solitone-blocco rappresenta SCALA_B solitoni
# fini. Regole di scala derivate imponendo la conservazione delle tre leggi al continuo
# (Poisson, bilancio gravita'/espansione, precessione), e verificate numericamente:
#   lambda_eff  = lambda_base * SCALA_B^(1/3)   (portata del kernel: il blocco e' piu' largo)
#   massa/solitone = SCALA_B * massa_fine        (ogni blocco pesa SCALA_B fini: preserva Poisson)
#   rho_eq, cs, alpha, PHI_CRIT invarianti       (densita' e proprieta' del mezzo non scalano)
# SCALA_B=1 e' la scala di Planck (solitone fondamentale). Salendo, si copre una
# gerarchia di scale reali: il blocco copre SCALA_B^(1/3) lunghezze d'onda del solitone.
SCALA_B  = 1.0
SCALA_AMP = 1.0  # fattore di ampiezza del campo: sqrt(SCALA_B), identita' a B=1
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


def _fattori_coarse(B):
    """Restituisce i soli fattori di scala della descrizione efficace.

    B=1 e' per costruzione l'identita': nessun parametro della fisica nativa viene
    modificato. Il coarse-graining non introduce una nuova legge dinamica.
    """
    B = float(B)
    if not np.isfinite(B) or B < 1.0:
        raise ValueError("SCALA_B deve essere finito e maggiore o uguale a 1")
    return B ** (1.0 / 3.0), B ** -0.5, B ** 0.5
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
SCHERMATURA = True      # LEGGE INTRINSECA: portata ancorata alla densita' critica adattiva.
                        # Si attiva automaticamente sopra rho_c, senza manopole di taratura.
P_LAM    = 1.0          # Indicatore storico mantenuto per compatibilita'; non e' piu' un esponente.
CS_M, ALPHA_M, BETA_M = 2.0, 0.05, 0.8
CS_DINAMICO = False       # velocita' locale delle onde metriche, A/B default off
VISTA_RETE = False        # rendering alternativo: solo rete, default = vista campo attuale
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
MITOSI_2LAM = False     # ⛔⛔ `MITOSI_2LAM` E' INERTE DAL COMMIT `6b` (2026-10-04): il
                        # da Luca.
                        # OFF di default: un interruttore alla volta (par.1).
                        #
                        # LA LEGGE: **un arco si divide SOLO se `d_arco >= 2 LAM`.**
                        #
                        # E NON E' UNA LEGGE NUOVA -- e' `A13` *(«sotto `LAM` non esiste niente:
                        # ne' archi ne' distanze fra nodi»)* applicato al sito che non lo
                        # applicava. Il figlio nasce a `d/2` dai genitori, e **la distanza del
                        # sistema e' quella LUNGO GLI ARCHI, non su `pos`** (correzione di Luca,
                        # 2026-09-25): quindi `A13` alla nascita **E'** `d/2 >= LAM`, cioe'
                        # `d_arco >= 2 LAM`. **Nessun numero nuovo.**
                        #
                        # STANDARD 10, IL CONTO DELLE LEGGI -- e va nella direzione giusta:
                        #   PRIMA  la mitosi divide senza guardare `d`; `_nasce` INTERVIENE sui
                        #          figli e FABBRICA lunghezza (misurato: `_sm_lund_mitosi` vale
                        #          `0.8 LAM` per evento nel caso a risposta nota);
                        #   DOPO   la mitosi guarda `d >= 2 LAM`; `_nasce` NON HA PIU' NIENTE DA
                        #          FARE su quel sito.
                        # **Le leggi non aumentano: si TOGLIE l'eccezione per cui la mitosi era il
                        # solo sito capace di creare una distanza sotto la scala di Planck, con un
                        # presidio che la riparava dopo.**
                        #
                        # MISURATO PRIMA DELLA CURA (`7086031`, 279 eventi, 2 semi, 300 passi):
                        #   il **77.23 %** delle divisioni e' GIA' conforme, il **22.77 %** no.
                        #   E la mitosi **non divide a caso**: `0.2277` contro `0.2998` di archi
                        #   corti nel grafo, cioe' **evita un po'** gli archi corti.
                        #
                        # ⚠ LO SCHWINGER **NON E' TOCCATO** (decisione di Luca): la `d` dei suoi
                        #   archi nuovi viene da `0.5*|pos[aa]-pos[bb]|`, cioe' **dal DISEGNO**, ed
                        #   e' la voce `A3`. Toccarlo qui vorrebbe dire curare `A3` di nascosto.

# ============================================================================================
# [`INERZIA-1(C)`, DECISIONE DI LUCA 2026-09-25] **IL CONTRASTO DIVENTA «PER VICINO».**
# --------------------------------------------------------------------------------------------
# `inerzia = _contrasto * T2` con `_contrasto = rho_s / peq_nodo`, e i due fattori scalano nel
# numero di vicini **IN VERSO OPPOSTO**. **MISURATO** in configurazione del driver
# (`CONFIG-1/a`, 2 semi x 2 versi del taglio, 20 bersagli per seme), pendenze su `log k`:
#     COPPIA       -0.19 ... -0.30      INTENSIVA (non cresce col numero di vicini)
#     _contrasto   +1.06 ... +2.47      ESTENSIVO
#     T2           -0.15 ... +0.44      fa cio' che la geometria impone
# Conseguenza: da `k = 77` a `k = 2` l'inerzia crolla `x2e-4 ... x4.6e-3`, il rapporto sale
# `x427 ... x1.5e4`, e **`|omega|` arriva a `x176`**: il difetto ARRIVA ALLA DINAMICA.
# **LA CAUSA E' DI STRUTTURA:** `rho_s` e' una **SOMMA pesata sui vicini**, `_peq_nodo` e'
# **esplicitamente una MEDIA**. Un rapporto somma/media **scala col grado per costruzione**.
# ✅ **LA CURA E' LOCALE, e la localita' e' il punto:** `rho_s` si normalizza **per vicino**
#   **DENTRO `_contrasto` e SOLO LI'**. **`rho_s` NON cambia altrove: la cura tocca
#   L'INERZIA, non IL CAMPO.** Le **7 letture di `rho_s` fuori da `_passo_spinoriale`** sono
#   elencate in `doc/LETTURE_rho_s.md` e passano tutte da `rho_spin` o da `_rho_sorgente()`:
#   **nessuna vede la normalizzazione**, e lo prova la byte-identita' a flag spento (`C3` del
#   sigillo: 121 campi, 0 diversi, 2 semi).
# ⚠ **PRIMO TENTATIVO (per CONTEGGIO dei vicini): MISURATO E INSUFFICIENTE** -- sigillo
#   `3/6`. Toglieva **esattamente `-1.0000` di pendenza** in tutti e 4 i bracci (a quattro
#   cifre), ma il residuo restava **`+0.49`** togliendo i lunghi e **`+1.34`** togliendo i
#   corti. **Il residuo viene DAI PESI:** `rho_s` e' una somma PESATA `Σ w_ij`, e dividere
#   per il NUMERO di vicini non e' dividere per il PESO TOTALE. **Resta nel registro come
#   tentativo misurato** (decisione di Luca).
# ✅ **`STANDARD 10`: NESSUNA LEGGE NUOVA E NESSUNA GRANDEZZA NUOVA** -- si TOGLIE
#   l'incoerenza fra numeratore e denominatore, e il peso dei vicini lo costruisce gia'
#   `_mat(w)`.
CONTRASTO_INTENSIVO = False   # [`INERZIA-1(C)`, 2026-09-25] `CONTRASTO_INTENSIVO`: IL
                        #   CONTRASTO DELL'INERZIA
                        #   E' «PER VICINO». Decisione di Luca. OFF di default, e FUORI dal
                        #   driver finche' il sigillo non passa. La legge, la derivazione e i
                        #   numeri stanno nella scheda `inerzia-spinoriale` di
                        #   `doc/REGISTRO_FISICA.md`.
SEMINA_MATURA = False   # [CURA 4, 2026-09-25] L'ACCENSIONE DEL CAMPO. Decisione di Luca.
                        # OFF di default: un interruttore alla volta (par.1).
                        #
                        # IL DIFETTO CURATO, misurato: `_pesi` moltiplica per
                        # `ramp = min(1, eta/TAU_A)` e **OGNI** nodo nasce con `eta = 0` --
                        # `semina`, `mitosi` e lo Schwinger scrivono LO STESSO ZERO. Quindi
                        # **l'universo parte SENZA CAMPO** (somma dei pesi = 0 ESATTO al passo
                        # zero) e ci mette `TAU_A/DT = 5000` passi ad accendersi. E poiche'
                        # `ramp` entra come `ramp[i]*ramp[j]`, **il peso d'arco va come
                        # `ramp^2`**: al passo 120 vale `5.76e-04` del maturo, UNA PARTE SU 1736.
                        # TUTTI i giri corti fatti finora hanno girato in quel regime.
                        #
                        # LA CURA, in due meta':
                        #  (1) i nodi della SEMINA INIZIALE nascono MATURI -- sono il vuoto che
                        #      GIA' ESISTE, non nodi appena creati;
                        #  (2) la rampa resta SOLO per i nodi nati in dinamica (mitosi,
                        #      Schwinger, semina in volo), col tempo = `_tempo_luce_nodo`
                        #      invece di `TAU_A`.
                        #
                        # E COSI' I DUE RUOLI DI `TAU_A` SI SEPARANO. Oggi `TAU_A` e' insieme
                        # la VITA MEDIA della memoria spinoriale (`:3334`, ed e' per QUELLO che
                        # il 50 fu scelto -- "alta persistenza memoria spinoriale") e il TEMPO
                        # DI ACCENSIONE di una sorgente (`_pesi`). Nessuna ragione, scritta da
                        # nessuna parte, perche' coincidano. Col flag ON `TAU_A` resta SOLO il
                        # primo.
TAU_A_LOCALE = True     # vita media spinoriale LOCALE ~|Psi|^2 (decadimento atomico). IN VERIFICA.
                       # False = TAU_A fisso (comportamento precedente). Reversibile.
SCALA_P_MEDIANA = False  # DIAGNOSTICO, NON FISICA ALTERNATIVA. Ripristina la vecchia scala di
                         # `ampiezza` (la MEDIANA GLOBALE di |dpozzo|) al solo scopo della
                         # RIDUZIONE AL LIMITE del sigillo `Y1`. NON ha un flag da riga di
                         # comando, di proposito: non deve poter essere acceso per sbaglio da un
                         # comando. Il sigillo lo accende IN PROCESSO e lo rispegne.
PHI_CRIT = 2 * np.pi    # QUANTO DI OLONOMIA. Un giro, non due: il sistema e'
                        # abeliano (settore U(1) varieta' invariante esatta, misurato),
                        # quindi il quanto naturale e' 2pi; il 4pi veniva dall'intuizione
                        # spinoriale, risultata assente. A 4pi la mitosi non scattava MAI
                        # e il grafo restava al 100% oltre portata; a 2pi ripara.
# ### LA FRAZIONE DELLA NASCITA, DICHIARATA UNA VOLTA SOLA (`COMMIT 6a`, decisione di
#   Luca del 2026-10-03). ### IL NOME E' `FRAZ_NASCITA` E NON `T_NASCITA`, per decisione
#   di Luca: e' una ### **FRAZIONE dell'arco**, un numero puro in `[0,1]` misurato dal
#   genitore `a`/`aa` -- e nel simulatore ### **`t` e `dt` sono TEMPI** (`dt_e`, il tempo
#   proprio dell'arco). ### Chiamarla `t` avrebbe messo una lunghezza adimensionale nello
#   stesso alfabeto dei tempi.
#   Luca del 2026-10-03). ### Il figlio sta a `FRAZ_NASCITA * d` dal genitore `a` e a
#   `(1 - FRAZ_NASCITA) * d` da `b`, ### **e lo STESSO valore vale per DOVE nasce (`pos`), per
#   QUANTO sono lunghi i suoi archi (`d`, `d0`, `dd`) e per la sua FASE (`fm`).**
#   ### ⛔ **NON E' UN FLAG, ed e' una scelta:** un flag renderebbe la frazione
#   ### **un'opzione**, e dove nasce un figlio non e' un'opzione -- e' la legge. E' il
#   difetto `E4-LAM`, gia' pagato una volta.
#   ### 📌 **PRIMA ERANO SEI FORMULE INDIPENDENTI che per caso dicevano tutte
#   *<<meta'>>***, in tre funzioni diverse: `mitosi` (la preparazione e il ramo Schwinger)
#   e la regola `_rn_sch_pos`. Con `0.5` ### **non cambia un bit**; cambia ### **dove
#   vive**, e da li' una decisione di fisica potra' cambiarla ### **in un posto solo.**
#   ### ⚠ **E le EREDITA' DI STATO NON la leggono** (decisione di Luca): `psi` e
#   `phivel` restano ### **medie**, la famiglia dello spinore resta una ### **copia**, e
#   `rho_sel` del cancello resta com'e'. Si decidono nella ### **LEGGE** di
#   `DIVISIONE-AUTOCONSISTENTE`, che viene ### **dopo la definizione dell'energia** perche'
#   deve rispettare `A14`.
FRAZ_NASCITA = 0.5

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


def rapporto_guardie(net):
    """[A8, 2026-09-20] I CONTATORI DELLE GUARDIE SILENZIOSE, in forma leggibile.

    Esiste perche' `V2` chiede che i contatori SI LEGGANO a fine run, e perche' metterli in un
    `print` dentro il simulatore avrebbe richiesto di toccare anche il driver -- che e' sigillato.
    E' PURA LETTURA: non tocca nulla.

    Per ogni sito: invocazioni, salti, frazione, la FORMA al fallimento e QUANDO (l'indice
    dell'ultima invocazione saltata). `shape[0] == -1` significa memoria ASSENTE, non lunghezza 0.
    """
    siti = ("kernel_alpha", "tempo_luce", "zeta_vir_a", "zeta_vir_b", "tors4pi",
            # [2026-09-20] i DIECI del secondo giro: cinque (c), tre (a), due (b).
            "calore_chi", "chicore_passo", "temposegno", "spinore_vivo", "chi_da_spinore",
            "nb_prec", "snap_psispin", "nb_grav_proiez")
    # il GRUPPO C non e' una guardia ma un DEFAULT: ha contatori diversi, e si riporta a parte
    fuori = {}
    for k in siti:
        tot = int(getattr(net, "_g_%s_tot" % k, 0))
        sal = int(getattr(net, "_g_%s_salti" % k, 0))
        fuori[k] = dict(tot=tot, salti=sal,
                        frazione=(sal / tot if tot else float("nan")),
                        shape=getattr(net, "_g_%s_shape" % k, None),
                        quando=getattr(net, "_g_%s_quando" % k, None))
    # ⚠ le DUE (b) hanno un contatore DIVERSO -- `_spento`, non `_salti` -- perche' misurano un
    # ramo che non gira per SCELTA (flag/costante off), non una legge saltata. Mescolarle con le
    # altre produrrebbe una "frazione di fallimento" che e' una frequenza di selezione: il numero
    # che si porta dietro una diagnosi falsa.
    for _k in ("compat_chi", "k_frange"):
        _t = int(getattr(net, "_g_%s_tot" % _k, 0))
        _sp = int(getattr(net, "_g_%s_spento" % _k, 0))
        fuori[_k + "_SPENTO"] = dict(tot=_t, salti=_sp,
                                     frazione=(_sp / _t if _t else float("nan")),
                                     shape=None, quando=None)
    fuori["s2full_default"] = dict(
        tot=int(getattr(net, "_g_s2full_tot", 0)),
        salti=int(getattr(net, "_g_s2full_conmask", 0)),
        frazione=(int(getattr(net, "_g_s2full_conmask", 0))
                  / max(int(getattr(net, "_g_s2full_tot", 0)), 1)),
        shape=(int(getattr(net, "_g_s2full_fuori", 0)),
               int(getattr(net, "_g_s2full_fuori_max", 0))),
        quando=getattr(net, "_g_s2full_quando", None))
    return fuori


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
# ⚠ IL COMMENTO DI PRIMA DICEVA <<segue REGIME; True in stocastico>>, E NON SEGUE IL REGIME:
#   il ramo di modulo mette `_SCUOTIMENTO_REGIME = True` in ENTRAMBI i casi, quindi qui vale
#   SEMPRE True, qualunque sia `REGIME`. ### A seguire il regime e' `_applica_regime`, che gira
#   SOLO se `--regime` e' passato da riga di comando e mette `False` per il deterministico.
#   ### E' LA TRAPPOLA `--regime`, dichiarata nell'intestazione di REGIME.
SCUOTIMENTO  = _SCUOTIMENTO_REGIME  # `SCUOTIMENTO` vale SEMPRE True da qui; solo `--regime` lo cambia

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
    """Applica lo scuotimento del vuoto guidato dallo stress metrico locale (senza numeri fissi).
    L'intensità emerge dallo scostamento fra la distanza reale (d) e la distanza di riposo (d0)
    degli archi connessi al nodo, pesata dalla soppressione della coerenza locale |Psi|^2."""
    if not SCUOTIMENTO or net.n == 0 or not len(net.i):
        return
    
    # 1. Calcola l'energia del vuoto dinamica (scala di riferimento)
    Lam = lambda_vuoto(net)
    if Lam <= 0:
        return

    if not hasattr(net, "psi") or len(net.psi) < net.n:
        net.calcola_psi()
        
    I2 = np.abs(net.psi[:net.n]) ** 2

    # 2. Deriva lo stress locale dagli archi (senza parametri arbitrari)
    # Stress dell'arco = |d - d0| / d0
    stress_archi = np.abs(net.d - net.d0) / np.maximum(net.d0, 1e-6)
    
    # Mappa lo stress dagli archi ai nodi (media sui vicini di ciascun nodo)
    stress_nodo = np.zeros(net.n)
    grado_nodo = np.zeros(net.n)
    i, j = net.i, net.j
    mask = (i < net.n) & (j < net.n)
    
    np.add.at(stress_nodo, i[mask], stress_archi[mask])
    np.add.at(stress_nodo, j[mask], stress_archi[mask])
    np.add.at(grado_nodo, i[mask], 1.0)
    np.add.at(grado_nodo, j[mask], 1.0)
    
    stress_nodo = stress_nodo / np.maximum(grado_nodo, 1.0)

    # 3. Intensità non-parametrica: radice dello stress locale modulata dalla coerenza
    # - Dove lo spazio è teso/frustrato, lo scuotimento sale.
    # - Dove c'è materia coerente (|Psi|^2 alto), viene soppresso dalla formula pura (1 + I2/Lam).
    intensita_stress = np.sqrt(stress_nodo + 1e-9)
    ampiezza = intensita_stress * (np.sqrt(Lam) / (1.0 + I2 / Lam))

    # Inietta l'agitazione vettoriale di fase firmata dalla chiralità
    calcio = net.rng.normal(0.0, 1.0, net.n) * ampiezza
    # [A8, 2026-09-20] (c) RAGIONE SCADUTA -- si conta per DIMOSTRARLO, non per fiducia.
    # `perc_chi` e' estesa da TUTTE E TRE le vie di crescita di `n` (semina :1900, mitosi :4181,
    # Schwinger :4302), e `n` e' `len(self.phi)`, che cresce SOLO li'. Quindi questa guardia non
    # PUO' fallire. Il contatore serve a provarlo con un numero, e a farlo scattare il giorno in
    # cui qualcuno aggiungesse una quarta via di crescita.
    # NB: il salto si conta solo col FLAG ACCESO (la classe di `N3b`).
        # ✅ MISURATO (sigillo `3/4 + 1 atteso`, 2d018e7): **0 salti su 12 invocazioni**, e in `W3`
    # NON si fa scattare NEMMENO corrompendo `perc_chi`. CLASSE: **(c) FORTE** -- la guardia non e'
    # RAGGIUNGIBILE, e il contatore resta solo come sentinella di regressione.
    net._g_calore_chi_tot = getattr(net, "_g_calore_chi_tot", 0) + 1
    if CALORE_VETTORIALE and not (hasattr(net, "perc_chi") and len(net.perc_chi) == net.n):
        net._g_calore_chi_salti = getattr(net, "_g_calore_chi_salti", 0) + 1
        net._g_calore_chi_shape = (len(getattr(net, "perc_chi", [])), net.n)
        net._g_calore_chi_quando = net._g_calore_chi_tot
    if CALORE_VETTORIALE and hasattr(net, "perc_chi") and len(net.perc_chi) == net.n:
        calcio = calcio * net.perc_chi  # Firma antichirale (rompe simmetria speculare); SCALARE se --calore-scal
        
    net.phivel[:net.n] += calcio

# ==========================================================================
# [T1, 2026-09-28] LO SCHEDULATORE DEL PASSO: la COMPOSIZIONE e' una LISTA ESPLICITA,
#   e c'e' UN SOLO ESECUTORE.
# ==========================================================================
#   Decisione di Luca: lo schedulatore POSSIEDE il passo. Le regole del passo (sincronia,
#   scala minima, 4 pi, ordine) non sono piu' intenzioni dentro le leggi controllate a
#   posteriori dai presidi: sono l'ARCHITETTURA.
#
#   CHE COSA FA T1, E CHE COSA NON FA: T1 e' SOLO lo scheletro. L'ordine e le fasi
#   diventano ESPLICITI e passano per un punto solo; LA FISICA NON CAMBIA, e il sigillo di
#   T1 e' BYTE-IDENTICO. Fotografia, variazioni e vincoli-una-volta sono T3.
#
#   APERTURA E CHIUSURA SONO FISSE, in testa e in coda. Prima l'apertura era dentro
#   ognuna delle cinque leggi (idempotente, cura `(c)1`) e la chiusura in fondo a
#   `memoria_hebbiana_moto`: DUE CONFINI CHE DIPENDEVANO DA CHI GIRAVA. Ora dipendono
#   dallo SCHEDULATORE, e l'idempotenza di `(c)1` non serve piu' -- il compositore SA di
#   essere il primo. `(c)1` era il primo abbozzo di questo confine, e il tag
#   `pre-schedulatore-t1` conserva il suo stato.
#
#   ⚠ `verifica_invarianti` era chiamata DENTRO `memoria_hebbiana_moto` con
#   `dove='memoria_hebbiana_moto'`, e ora la chiama lo schedulatore con
#   `dove='esegui_passo'`: cambia LA STRINGA che finisce nel referto di un'eccezione, non
#   lo stato. E l'ORDINE relativo `chiudi -> verifica_invarianti` E' PRESERVATO, che e'
#   cio' che rende T1 byte-identico: il controllo guarda `d0` GIA' frenata, come prima.

PASSO_COMPOSIZIONE = ('apri', 'scuoti_vuoto', 'step', 'mitosi',
                      'rilassa_disegno', 'memoria_hebbiana_moto', 'chiudi',
                      'verifica_invarianti')
# le fasi che NON sono leggi: le esegue lo schedulatore, e non hanno un metodo omonimo
_PASSO_FASI = {'apri': '_smp_apri', 'chiudi': '_smp_chiudi'}
# le leggi che sono FUNZIONI DI MODULO e non metodi (prendono `net`)
_PASSO_MODULO = ('scuoti_vuoto',)


# IL REGISTRO delle voci ammesse nella composizione. **E' la prima forma del registro di
#   `T2`**: oggi elenca i NOMI, e `T2` gli aggiungera' il TIPO di ogni legge.
#   ⚠ Una voce non nel registro NON si esegue: si SOLLEVA. Un `getattr` su un nome
#     sbagliato darebbe `AttributeError` a meta' passo, cioe' **dopo** che alcune leggi hanno
#     gia' scritto -- e uno stato mezzo avanzato non e' uno stato che qualcuno ha dichiarato.
_PASSO_REGISTRO = frozenset(('apri', 'chiudi', 'verifica_invarianti',
                            'scuoti_vuoto', 'step', 'mitosi', 'rilassa_disegno',
                            'memoria_hebbiana_moto'))
# la CODA OBBLIGATORIA, in quest'ordine: il commit del passo, poi il controllo.
_PASSO_CODA = ('chiudi', 'verifica_invarianti')


# I TIPI DELLE VOCI DEL PASSO (`T2b`, 2026-09-28). **DICHIARATI, non ancora FATTI
#   RISPETTARE:** in `T2b` nessun comportamento cambia, e il sigillo e' byte-identico. Sara'
#   `T3` a dare a ogni tipo il suo CONTRATTO (la dinamica riceve la fotografia e restituisce
#   variazioni, il vincolo corregge la somma una volta, ecc.).
#
#   I TIPI vengono dall'analisi del 2026-09-27 (`csv/_test_fork/_etc_schedulatore.py`), che li
#   deduce da CIO' CHE OGNI FUNZIONE SCRIVE -- non da come si chiama.
#
#   ⚠⚠ **`fase` NON E' UNO DEI CINQUE TIPI DI LUCA, E L'HO AGGIUNTO IO.** I cinque sono
#   `dinamica`, `vincolo`, `strutturale`, `osservatore`, `disegno`, e sono i tipi delle
#   **LEGGI**. Ma `apri` **non e' una legge**: e' la FOTOGRAFIA, cioe' una fase dello
#   schedulatore, e **non scrive nessuno stato fisico** -- scrive solo lo snapshot
#   (`_smp_d0`, `_smp_d`). Chiamarla `osservatore` sarebbe falso (scrive), `vincolo` sarebbe
#   falso (non corregge niente), `dinamica` sarebbe il peggiore dei tre (non fa fisica).
#   **Lo dichiaro come mio invece di forzarlo in una casella che non gli appartiene**, e la
#   decisione se tenerlo e' di Luca.
#   *(`chiudi` invece E' un `vincolo` vero -- applica il freno di scala minima una volta sulla
#   variazione totale -- e l'analisi lo classificava gia' cosi'.)*
#
#   ⚠ **`mitosi` resta `AMBIGUA`**: scrive **struttura E stato** (30 scritture di stato).
#   `T2c` la spezza in una voce STRUTTURALE e una di STATO, e finche' non e' spezzata il tipo
#   dice la verita' invece di scegliere una delle due meta'.
_PASSO_TIPI = {
    'apri':                  'fase',          # la FOTOGRAFIA: scrive solo lo snapshot
    'scuoti_vuoto':          'dinamica',      # scrive `phivel` e nient'altro
    'step':                  'dinamica',      # 26 scritture di stato
    'mitosi':                'AMBIGUA',       # struttura E stato: T2c la spezza
    'rilassa_disegno':       'disegno',       # scrive `pos`, ZERO stato fisico
    'memoria_hebbiana_moto': 'dinamica',      # 10 scritture di stato
    'chiudi':                'vincolo',       # il freno, UNA volta sul totale (`C3`)
    'verifica_invarianti':   'osservatore',   # LEGGE SOLTANTO
}
# la FUNZIONE che sta dietro ogni voce, per chi vuole verificare il tipo sul codice
_PASSO_FUNZIONE = dict(_PASSO_FASI)
for _k in _PASSO_REGISTRO:
    _PASSO_FUNZIONE.setdefault(_k, _k)

class ComposizioneNonValida(ValueError):
    """La composizione del passo viola la struttura della transazione."""


class LimiteNodiSuperato(RuntimeError):
    """**`MAX_NODI` e' una GUARDIA DI MEMORIA, non di fisica: quando morde, il run SI FERMA.**

    *(`MAX-NODI-FERMA`, cura del 2026-09-28. Prima di questa cura i tre siti che la leggevano
    CAMBIAVANO LA FISICA IN SILENZIO -- la mitosi restituiva zero nascite, la semina si
    troncava, il canale di Schwinger si spegneva -- e il run continuava come se la fisica
    avesse deciso cosi'.* ### **Era la forma esatta che `A8` esiste per impedire**, *e il
    commento della costante lo diceva gia': <<la misura e' da rifare con piu' memoria, NON da
    troncare>>. L'intenzione era scritta e il codice faceva l'opposto.)*
    """


class SchermaturaSpenta(RuntimeError):
    """**La SCHERMATURA si e' spenta per tutta la rete, e il run SI FERMA.**

    *(`PSI-FLASH`, cura del 2026-09-28.)* `lambda_nodi` aveva un ripiego silenzioso:
    `if len(self.psi) < self.n: return np.full(self.n, LAM)`. ### **Al passo di nascita `mitosi`
    fa crescere `n`, quindi `len(psi) < n`, quindi la schermatura si spegneva PER TUTTA LA RETE**
    -- `lambda` da `~0.60` a `0.80`, `exp(-d/lambda)` da `0.0655` a `0.1223`, e `|psi|` su di
    `1.62x` **per TUTTI, non per il nato**.

    ### **Il `2.6x` sul pozzo non era fisica: era l'ASSENZA della schermatura.**
    *(Causa trovata dal guardiano, Luca, 2026-09-28; verificata da
    `csv/_test_fork/_lambda_al_flash.py`.)*

    **Chi la vede, che fare:** `psi` deve essere ESTESA a ogni nascita
    *(`_eredita_psi_figli`)*. **Se questo errore scatta, una strada nuova fa crescere `n` senza
    estendere `psi`** -- e ### **prima di questa cura quella strada cambiava la fisica in
    silenzio.**
    """


class CacheCorta(RuntimeError):
    """**Una CACHE e' piu' corta di `n`, e il ramo di scorta darebbe UN'ALTRA GRANDEZZA.**

    *(`PSI-FLASH`, seconda cura del 2026-09-28.)* La forma e' quella di `SchermaturaSpenta`,
    e i siti sono due:

    | sito | il valore di scorta, e perche' non va |
    |---|---|
    | `_rho_sorgente` | restituiva **`|psi|^2`** invece di **`rho_spin`**: ### **un'ALTRA
      DENSITA' per tutta la rete**, e la densita' entra in `lambda_nodi`, quindi nella
      schermatura, quindi nel campo |
    | `_nb_grav` | restituiva **`self._nb`** invece del Bloch NATIVO del campo emesso:
      ### **un'ALTRA DIREZIONE**, e la direzione entra nella gravita' |

    ### **Il gradino del +11 % al passo DOPO la nascita era questo**, e il flash grande lo
    copriva: due difetti di segno opposto. *(Causa trovata dal guardiano, Luca.)*

    **Chi la vede, che fare:** la cache va ESTESA alla nascita (`_eredita_psi_figli`).
    ⚠ **E NON si "ripara" allungandola qui:** allungarla a valle e' proprio il ripiego che
    questa eccezione esiste per rendere impossibile.
    """


class CacheLunga(RuntimeError):
    """**Una CACHE e' piu' LUNGA del suo bersaglio, e nessuno se ne accorgeva.**

    *(`RIPIEGHI-ZERO`, cura del 2026-09-29, decisione di Luca.)*

    ### Perche' esiste, ed e' MISURATO
    `_ferma_se_cache_corta` comincia con **`if quanta >= n: return`**: ### **il lato LUNGA era
    SCOPERTO.** La **prova a guasto** del 2026-09-28 lo ha mostrato col **comportamento** --
    `psi` allungata di uno da' un ### **`ValueError` di broadcast**, non un errore dichiarato.
    E i tre confronti `len(x) > n` *(`:2265` `:3578` `:3587`)* **non possono scattare**, perche'
    ### **nessuna legge toglie nodi**: `n` E' `len(phi)`, e le cinque scritture di `phi` sono
    tutte inizializzazione / `concatenate` / modulo.

    ### -> **Quindi una cache PIU' LUNGA non e' un caso da gestire: e' un ERRORE**, e vuol dire
    che qualcuno l'ha estesa **due volte**.

    **Chi la vede, che fare:** cercare **il secondo** estensore. ### **NON si tronca:** troncare
    sarebbe il ripiego che questa eccezione esiste per rendere impossibile.
    """


class FormaSbagliata(RuntimeError):
    """**Il PRIMO asse e' giusto e uno degli ALTRI no.**

    *(`RIPIEGHI-ZERO`, generalizzazione del 2026-09-29 decisa da Luca.)*

    ### Perche' esiste: il controllo guardava UN SOLO ASSE, e lo dichiaravo come limite
    `len` e' **il primo asse**. Ma ### **dieci grandezze del registro hanno DUE assi** -- `pos`
    `_nb` `_nb_prec` `_nb_ret` `mem_mot` `omega_s` sono `(n, 3)`, `_psi_spinor` `_psi_spin_prec`
    `_spinor_lift` `psi_spin` sono `(n, 2)` -- e ### **un secondo asse sbagliato PASSAVA.**

    ### -> **Ora il registro dichiara la FORMA e il controllo la verifica TUTTA.**
    Un `(n, 2)` dove ci vuole `(n, 3)` non e' ne' corto ne' lungo: e' ### **un'altra grandezza**,
    e merita il suo nome.
    """


class FinestraRestataAperta(RuntimeError):
    """**Una grandezza che vive SOLO DENTRO il passo e' ancora li' quando il passo e' chiuso.**

    *(`RIPIEGHI-ZERO`, **commit 1** del riordino, 2026-10-01.)*

    ### Perche' esiste: IL PRESIDIO `3-bis` HA TROVATO UN BUCO VERO AL SUO PRIMO GIRO
    `_smp_d0` e `_smp_d` sono **per arco**, `float64`, e ### **il registro NON LE DICHIARAVA.**
    Il motivo e' preciso e va detto: ### **il registro era stato costruito MISURANDO `vars(net)`
    alla FINE di un passo** *(`csv/_test_fork/_registro_grandezze.py`, fine del passo 30)*, e
    queste due ### **a fine passo NON ESISTONO** -- le azzera `_smp_chiudi`. ### **Una misura
    presa a un solo istante non puo' vedere cio' che vive fra due istanti.**
    ### -> **E' esattamente il buco che il controllo DOPO OGNI VOCE esisteva per trovare.**

    ### LA FINESTRA, MISURATA voce per voce (scena piccola, seme 11, 3 passi, 27 controlli)
    | dove | `_smp_d0` e `_smp_d` |
    |---|---|
    | `prima delle leggi` | ### **NON ESISTONO** |
    | da `apri` a `memoria_hebbiana_moto` *(sei voci)* | ### **lunghe `m` = 70199** |
    | dopo `chiudi`, dopo `verifica_invarianti` | ### **NON ESISTONO** |
    **Zero casi ambigui, zero disallineamenti, e le due SEMPRE INSIEME.**

    ### Allora NON sono DERIVATE, e nemmeno di STATO: sono UNA TERZA COSA, e si DICHIARA
    **Di STATO no:** una grandezza di stato ha una **regola di nascita** e la sua lunghezza e' un
    **invariante ai due punti** -- queste a quei punti ### **devono NON esserci.**
    **Derivate no:** per il criterio di Luca *(letta fra la nascita e la sua riscrittura)* ###
    **sono LETTE dentro la finestra** -- le scrive `_smp_apri`, le allinea `_smp_chirurgia`, le
    legge e le chiude `_smp_chiudi`. ### **Chiamarle derivate sarebbe FALSO**, e la terza colonna
    del registro delle derivate chiede un **motivo misurato** che qui non esiste.
    ### -> **Si dichiarano per cio' che SONO: una finestra, con la voce che l'APRE e quella che
    la CHIUDE.** E il controllo diventa piu' forte, non piu' debole:
    ### **fuori dalla finestra la grandezza DEVE NON ESSERCI.**

    ### E QUESTO E' IL DIFETTO CHE IL CODICE STESSO TEMEVA, ora IMPEDITO
    `_smp_chiudi` lo scrive da se': *<<la fotografia si CHIUDE sempre, senno' resterebbe aperta
    e ### il passo dopo leggerebbe quella del passo prima>>*. ### **Era un timore scritto in un
    commento; ora e' un presidio** (`A9`: un presidio che non impedisce non e' un presidio).

    ### ⚠ E LA FINESTRA PUO' NON APRIRSI, legittimamente: SI CONTA (`A8`)
    `_smp_apri` fotografa **solo se** `SCALA_MIN_PASSO or COES_CAUSALE`. A flag spenti la finestra
    ### **non si apre mai**, e non e' un difetto. ### **Quindi <<dentro la finestra e assente>> si
    CONTA** (`_g_finestra_chiusa_dentro`) **invece di fermare**: cosi' *<<la finestra non si e'
    aperta>>* e' ### **leggibile invece che supposto**, e il sigillo lo confronta come gli altri
    contatori. ### **Il verso duro e' l'altro, e quello FERMA: presente FUORI dalla finestra.**
    """


class GrandezzaNonDichiarata(RuntimeError):
    """**La rete HA una grandezza per nodo o per arco che il REGISTRO non dichiara.**

    *(`RIPIEGHI-ZERO`, generalizzazione **3-bis**, 2026-10-01 — **commit 1** del riordino.)*

    ### Perche' esiste: toglie il TERZO limite che avevo scritto nella scheda
    Il registro e' stato costruito ### **MISURANDO** una scena e una configurazione *(`nmasse 3`,
    `sep 6.1158`, seme `11`, zero differenze su 80 booleani dal driver)*. ### **Con altri flag una
    grandezza nuova poteva comparire e restare FUORI dal controllo in silenzio, per sempre.**

    ### -> **Ora il controllo non parte da un elenco: PARTE DA CIO' CHE LA RETE HA.**
    Scorre `vars(net)`, prende cio' che e' **array o lista** col **primo asse** `== n` oppure `== m`,
    e ### **se il nome non e' nel registro FERMA IL RUN, nominandolo.**

    ### ⚠ **E LA REGOLA NON PARTE DAL NOME NE' DALLA SINTASSI, ed e' deliberato**
    In questa sessione ### **SEI volte** una mia regola basata sul **nome** o sulla **sintassi** ha
    nascosto cio' che cercava: `full(n,…)` contato come *«estende»* · la condizione fusa chiamata
    *«inizializzazione»* · `==`/`!=` messi *«fuori dal mandato»* *(sette siti)* · il ramo degli
    `IfExp` **invertito** *(una «famiglia» inesistente)* · il filtro per **nome** che perde gli
    **alias locali** · una lista di **nomi** al posto del **grafo** *(falsi «buchi»)*.
    ### **La forma dell'errore e' sempre la stessa: una regola che parte dal NOME o dalla SINTASSI
    invece che da CIO' CHE FA.** ### -> **Qui una grandezza si qualifica PER LA SUA FORMA**, che e'
    un **fatto misurato a runtime**: nessun nome, nessuna sintassi, nessun alias.

    ### ⚠ **IL LIMITE CHE RESTA, dichiarato**
    Una grandezza con `len` **diverso** da `n` e da `m` ### **non viene vista** *(per esempio una per
    faccia o per ciclo)*: ### **il presidio copre i DUE METRI che il registro conosce, non tutti i
    metri possibili.** E se `n == m` i due metri sono **indistinguibili** — oggi `12802` contro
    `471564`, e lo strumento del registro **lo controlla e lo dichiara**.

    **Chi la vede, che fare:** ### **o la grandezza entra nel registro** *(con forma, tipo e, se e'
    di STATO, la sua regola di nascita)*, ### **o si dichiara DERIVATA col suo motivo MISURATO.**
    ### **Mai togliere il nome dal controllo in silenzio.**
    """


class TipoSbagliato(RuntimeError):
    """**La forma e' giusta e il TIPO no.**

    *(`RIPIEGHI-ZERO`, generalizzazione 3 del 2026-09-29, decisione di Luca.)*

    > ### **Un COMPLESSO diventato REALE perde META' DELL'INFORMAZIONE senza cambiare forma.**

    E le sei grandezze `complex128` del registro -- `psi` `_psi_prec` `_psi_spinor`
    `_psi_spin_prec` `_spinor_lift` `psi_spin` -- sono ### **esattamente quelle su cui e' nato il
    flash di `PSI-FLASH`**: la fase vive nella parte immaginaria, e un `np.real` di troppo la
    butterebbe via ### **senza che ne' la LUNGHEZZA ne' la FORMA se ne accorgano.**

    ### -> **E' il QUARTO nome per il QUARTO difetto distinto** -- corta, lunga, forma, tipo -- e
    **non** una legge in piu': ### **la legge e' UNA, `_ferma_se_registro_incoerente`.**

    ### ⚠ **LA RISERVA, dichiarata: i tre `int64` dipendono dalla PIATTAFORMA.**
    `_deg` `perc_chi` `perc_geom` sono `int64` **su questa macchina**, ma la larghezza dell'intero
    predefinito di numpy **cambia fra piattaforme**. ### **Se questo errore scatta su uno di quei
    tre, la cosa da aggiornare e' IL REGISTRO, non il codice** -- e il messaggio lo dice.
    """


def _ferma_se_cache_corta(nome, quanta, n, dove, scorta):
    """**UN SOLO controllo per le cache corte**, come `_ferma_se_oltre_max_nodi`."""
    if quanta >= n:
        return
    _nl = chr(10)
    raise CacheCorta(_nl.join([
        "[CACHE CORTA] IL RUN SI FERMA (`PSI-FLASH`, `A9`).",
        "  cache ..... %s" % nome,
        "  len ....... %d" % quanta,
        "  n ......... %d   (mancano %d valori)" % (n, n - quanta),
        "  dove ...... %s" % dove,
        "  il ramo di scorta avrebbe dato: %s" % scorta,
        "  PERCHE': quel valore di scorta e' UN'ALTRA GRANDEZZA, e la darebbe a TUTTA LA",
        "  RETE in silenzio. CHE FARE: la cache va ESTESA alla nascita",
        "  (`_eredita_psi_figli`), NON allungata qui."]))


# ============================================================================
#  IL REGISTRO DELLE GRANDEZZE, e IL CONTROLLO UNICO DELLO SCHEDULATORE
#  (`RIPIEGHI-ZERO`, 2026-09-29 -- decisione di Luca, piano approvato)
# ============================================================================
#  NON E' UNA LISTA SCRITTA A MANO: e' l'esito di DUE MISURE committate.
#    (1) `csv/_test_fork/_registro_grandezze.py` ha trovato IN AUTOMATICO chi e' per nodo
#        (`len == n`) e chi per arco (`len == m`): 32 + 11, e ZERO ambigue.
#    (2) `csv/_test_fork/_ordine_letture.py` ha misurato, in un passo CON NASCITA, chi e' GIA'
#        PIENO quando `mitosi` ritorna: 30 su 40. Le altre 10 sono corte, e per ognuna si e'
#        misurato SE UNA LEGGE LE LEGGE CORTE. Risposta: BUCHI ZERO.
#  E IL CRITERIO E' DI LUCA, e NON e' "stato o derivata": e' "LETTA fra la nascita e la sua
#    riscrittura". `psi` E' derivata, e ha avuto bisogno di una regola di nascita perche' una
#    legge la leggeva nell intervallo -- ed e' li' che nasceva il flash di `PSI-FLASH`.

# I METRI: non sono voci del registro, sono il RIFERIMENTO. `n` E' `len(phi)` (property) e
#   `m` E' `len(i)`: controllarli contro se stessi non vorrebbe dire niente.
REGISTRO_METRI = (("phi", "nodo"), ("i", "arco"), ("j", "arco"))

# LE GRANDEZZE DI STATO, con la loro FORMA ATTESA (generalizzazione di Luca, 2026-09-29).
#   ("n",) = un asse lungo `n`; ("n", 3) = `n x 3`; ("m",) = un asse lungo `m`.
#   IL TERZO CAMPO E' IL TIPO (generalizzazione 3 di Luca): un COMPLESSO diventato REALE perde
#   META' DELL'INFORMAZIONE SENZA CAMBIARE FORMA, e le sei `complex128` qui sono esattamente quelle
#   su cui e' nato il flash. `None` = ESENTE, e c'e' UNA sola esenzione: `conc_nodi`, che e' una
#   LISTA e il cui `float64` misurato e' un ARTEFATTO di `np.asarray` su liste vuote.
#   ⚠ RISERVA DICHIARATA: i tre `int64` (`_deg`, `perc_chi`, `perc_geom`) hanno una larghezza che
#     DIPENDE DALLA PIATTAFORMA. Se il controllo scatta su uno di quei tre, si aggiorna IL REGISTRO,
#     non il codice -- e il messaggio lo dice.
#   IL CONTROLLO VERIFICA TUTTI GLI ASSI, non solo il primo: dieci grandezze qui hanno DUE assi, e
#   prima un secondo asse sbagliato PASSAVA (era il limite che avevo dichiarato nella scheda).
#   ⚠ LE FORME SONO MISURATE, non scritte a mano: vengono dalla colonna `forma` di
#     `doc/REGISTRO_grandezze.md`, che `csv/_test_fork/_registro_grandezze.py` genera dal runtime.
#   ⚠ `conc_nodi` e' una LISTA DI LISTE e il suo secondo asse vale 0 e CAMBIA (le voci si
#     aggiungono): si dichiara SOLO il primo asse, perche' dichiarare `0` sarebbe dichiarare il
#     falso.
REGISTRO_STATO = (
    ("_cs_nodo_prev", ("n",), "float64"),
    ("_deg", ("n",), "int64"),
    ("_nb", ("n", 3,), "float64"),
    ("_nb_prec", ("n", 3,), "float64"),
    ("_nb_ret", ("n", 3,), "float64"),
    ("_psi_prec", ("n",), "complex128"),
    ("_psi_spin_prec", ("n", 2,), "complex128"),
    ("_psi_spinor", ("n", 2,), "complex128"),
    ("_spinor_lift", ("n", 2,), "complex128"),
    ("conc_nodi", ("n",), None),   # ESENTE: e' una LISTA, non ha un dtype
    ("eta", ("n",), "float64"),
    ("mem_mot", ("n", 3,), "float64"),
    ("omega_s", ("n", 3,), "float64"),
    ("perc_chi", ("n",), "int64"),
    ("perc_geom", ("n",), "int64"),
    ("perc_tw", ("n",), "float64"),
    ("phi0", ("n",), "float64"),
    ("phi_s", ("n",), "float64"),
    ("phivel", ("n",), "float64"),
    ("pos", ("n", 3,), "float64"),
    ("psi", ("n",), "complex128"),
    ("psi_spin", ("n", 2,), "complex128"),
    ("rho_spin", ("n",), "float64"),
    ("_rep", ("m",), "float64"),
    ("d", ("m",), "float64"),
    ("d0", ("m",), "float64"),
    ("peq", ("m",), "float64"),
    ("tw", ("m",), "float64"),
    ("twp", ("m",), "float64"),
    ("vd", ("m",), "float64"),
)

# LE DERIVATE: ricalcolate a piena lunghezza dalla loro legge, quindi fra due ricalcoli la loro
#   lunghezza NON E' UN INVARIANTE. NON si controllano ai due punti, e il MOTIVO di ognuna e'
#   MISURATO, non supposto: e' la terza colonna.
# LE CLASSI DI NASCITA DI UNA DERIVATA, e sono DUE (`COMMIT 4` del riordino, 2026-10-03).
#   ⚠ ESISTONO PERCHE' UNA MISURA LE HA RICHIESTE, non per simmetria: il veleno `NaN`
#     ESTENDE la derivata alla lunghezza nuova, e `csv/_test_fork/_copertura_derivate.py`
#     ha misurato che **DUE** derivate usano il DISALLINEAMENTO DI LUNGHEZZA come
#     SEGNALE per ripulirsi -- quindi estenderle **distrugge il meccanismo che il
#     registro dichiara**, in due modi opposti:
#       `_xi_rumore`    `:5031`  `if _xi is None or len(_xi) < n:`  -> estendere la rende
#         FALSA, quindi **l'estrazione fresca NON avviene** e i nodi nuovi prendono `NaN`.
#         E il commento dichiara che quello e' **IL PERCORSO NORMALE della mitosi**.
#       `_g_rampa_prec` `:5704`  `if ... len(_prec) == len(ramp):` -> estendere la rende
#         VERA, quindi `ramp < _prec` confronta con `NaN`, da' **False in silenzio**, e il
#         ramo che conta `_g_rampa_prec_disallineata` **smette di scattare**.
#   ### DECISIONE DI LUCA, 2026-10-03: VIA A -- si avvelena ogni derivata TRANNE quelle
#     dichiarate `auto-rinfresco`. ### E' LA FORMA GIA' APPROVATA per le esenzioni di
#     `eta` (`nonneg_inf`: `+inf` per il vuoto) e di `peq` (`nan` da calibrare), quindi
#     per `9-ter` **non e' una legge in piu': e' il TERZO caso della STESSA esenzione.**
#   ### E IL REGISTRO LE DICHIARAVA GIA' COSI', A PAROLE: questa colonna non aggiunge una
#     convenzione, la rende **LEGGIBILE DA UNA MACCHINA** -- e `_avvelena_derivate` la
#     legge DA QUI. ### NESSUN ELENCO A MANO nel codice del veleno.
NASCITA_DERIVATA = ("avvelena", "auto-rinfresco")

# (nome, dove, CLASSE DI NASCITA, motivo MISURATO)
REGISTRO_DERIVATE = (
    ("_chi_core_nodi", "nodo", "avvelena",
     "nessuna legge la legge nella finestra della nascita"),
    ("_chi_core_raggio", "nodo", "avvelena",
     "nessuna legge la legge nella finestra della nascita"),
    ("_chi_core_rho0", "nodo", "avvelena",
     "nessuna legge la legge nella finestra della nascita"),
    ("_fatt_cs_ultimo", "nodo", "avvelena",
     "nessuna legge la legge -- e coincide col commento del codice, "
     "che la dichiara DIAGNOSTICA e senza lettori (Z7)"),
    ("_chi_geom_nodi", "nodo", "avvelena",
     "la legge la trova GIA RISCRITTA (chiralita_core_locale)"),
    ("_r_corrente", "nodo", "avvelena", "la legge la trova GIA RISCRITTA (step)"),
    ("_g_rampa_prec", "nodo", "auto-rinfresco",
     "AUTO-RINFRESCO: `_pesi` la legge corta e la riscrive LEI STESSA "
     "un evento dopo, e il disallineamento e GIA CONTATO "
     "(`_g_rampa_prec_disallineata`). ### ESENTE DAL VELENO: il disallineamento di "
     "lunghezza E IL SUO SEGNALE, e estenderla lo distruggerebbe -- MISURATO, "
     "csv/_test_fork/_copertura_derivate/ (99 letture sporche su tre scene)"),
    ("_xi_rumore", "nodo", "auto-rinfresco",
     "AUTO-RINFRESCO, ed E LA REGOLA DI NASCITA: `xi` e l AMBIENTE, non "
     "una proprieta del nodo, quindi il figlio NON lo eredita -- e il "
     "codice lo dichiara al sito di lettura. ### ESENTE DAL VELENO: la guardia "
     "`len(_xi) < n` al :5031 E IL SUO SEGNALE, e il commento dichiara che quello e "
     "IL PERCORSO NORMALE della mitosi -- estenderla farebbe nascere i nodi nuovi con "
     "NaN invece di un campione fresco (99 letture sporche misurate). "
     "### ⚠ MA OGGI NON E L ESENZIONE A PROTEGGERLA, ED E UNA MEZZA VERITA CHE "
     "CORREGGO: `_xi_rumore` ha shape (12802, 3), cioe DUE ASSI, quindi il ramo "
     "`multiasse` di `_avvelena_derivate` la salterebbe COMUNQUE -- e il braccio `B` "
     "del sigillo l ha MISURATO, perche togliendole l esenzione NON CAMBIAVA NIENTE e "
     "il contatore `_g_veleno_multiasse` e comparso. L esenzione resta GIUSTA come "
     "DICHIARAZIONE D INTENTO (morderebbe se un domani diventasse 1-D), ma dire che e "
     "lei a proteggerla OGGI era falso. E per questo il braccio `B` e ancorato a "
     "`_g_rampa_prec`, che e (12802,) 1-D e quindi DAVVERO avvelenabile"),
    ("_dt_e_ultimo", "arco", "avvelena", "la legge la trova GIA RISCRITTA (step)"),
    ("_sin2_vir", "arco", "avvelena",
     "la legge la trova GIA RISCRITTA (memoria_hebbiana_moto), che la riscrive INTERA "
     "(`s2full = np.zeros(len(self.i))`, :8724) nello STESSO passo, dopo `mitosi`. "
     "### QUINDI IL VELENO E INERTE QUI, e lo si dichiara: le 6 guardie di lunghezza del "
     "`step` (:7506-7508, :7608-7611) NON sono ripieghi ma un PRESIDIO CHE SOLLEVA "
     "(`_ferma_registro(CacheCorta/CacheLunga)`), e il veleno le trova la lunghezza GIA "
     "giusta -- come oggi, perche la riscrittura avviene prima del prossimo `step`"),
)
_fuori_vocabolario = [v[0] for v in REGISTRO_DERIVATE if v[2] not in NASCITA_DERIVATA]
if _fuori_vocabolario:
    raise RuntimeError(
        "classe di nascita non dichiarata per %s: le classi sono %s. "
        "Una derivata senza classe non si puo' ne' avvelenare ne' esentare, e il "
        "silenzio NON e' una terza possibilita'."
        % (", ".join(_fuori_vocabolario), ", ".join(NASCITA_DERIVATA)))
del _fuori_vocabolario

# LE GRANDEZZE A FINESTRA: ESISTONO SOLO DENTRO IL PASSO (commit 1 del riordino, 2026-10-01).
#   (nome, forma, tipo, voce che APRE, voce che CHIUDE, motivo MISURATO)
#   ⚠ NON SONO una quarta classe di FISICA: sono la QUARTA TABELLA DI UNA DICHIARAZIONE. La legge
#     resta UNA (`_ferma_se_registro_incoerente`), e la cascata forma->tipo e' in UN POSTO SOLO
#     (`_controlla_forma_e_tipo`): due copie sarebbero due leggi, ed e' `9-ter`.
#   ⚠ QUESTE DUE LE HA TROVATE IL PRESIDIO `3-bis`, non io: il registro era stato costruito
#     MISURANDO `vars(net)` alla FINE di un passo, e a fine passo queste NON ESISTONO.
REGISTRO_FINESTRA = (
    ("_smp_d0", ("m",), "float64", "apri", "chiudi",
     "la fotografia di `d0` a inizio passo pieno (`SCALA_MIN_PASSO` C3 + `COES_CAUSALE` C4): la "
     "scrive `_smp_apri`, la riallinea `_smp_chirurgia` quando la mitosi cambia gli archi, la "
     "legge e la azzera `_smp_chiudi`. MISURATA aperta da `apri` a `memoria_hebbiana_moto`."),
    ("_smp_d", ("m",), "float64", "apri", "chiudi",
     "la fotografia di `d` dello stesso istante, e viaggia SEMPRE con `_smp_d0`: misurate "
     "insieme in tutti e 27 i controlli, mai una senza l altra."),
)

# ACCESO DI DEFAULT, e la ragione va detta: NON E' UN ESPERIMENTO, E' UNA CURA APPROVATA. Un
#   controllo spento di default non impedisce niente (`A9`). Il flag `--senza-controllo-registro`
#   esiste PER IL SIGILLO: il criterio `C` chiede che, col controllo SPENTO, la prova a guasto
#   torni a dare ZERO grandezze protette -- senno' il sigillo non sta misurando il controllo.
CONTROLLO_REGISTRO = True

# TUTTI i nomi che il registro dichiara, nelle sue QUATTRO tabelle. ### Si costruisce DAL
#   REGISTRO, non si riscrive a mano: una voce aggiunta a una delle quattro entra qui PER
#   COSTRUZIONE -- ed e' la ragione per cui la tabella nuova non ha richiesto di toccare `3-bis`.
REGISTRO_NOMI = frozenset([x[0] for x in REGISTRO_STATO]
                          + [x[0] for x in REGISTRO_DERIVATE]
                          + [x[0] for x in REGISTRO_METRI]
                          + [x[0] for x in REGISTRO_FINESTRA])


# =============================================================================
# ### LA NASCITA COME EVENTO UNICO  --  `COMMIT 3` del riordino (2026-10-02)
# =============================================================================
#
# ### TUTTE le grandezze del registro scritte in UN SOLO punto, con UNA regola
# ### DICHIARATA per ciascuna. Niente scritture sparse, niente sistemazioni a valle.
#
# E' il par.(c) di `doc/PIANO_riordino_mitosi.md`. Prima di questo commit i posti
# che scrivevano le grandezze della nascita erano TRE -- `mitosi`, i due
# `_eredita_*`, piu' la crescita per MUTAZIONE di `conc_nodi` (`.append`, che l'AST
# non vede). Ora il posto e' UNO: `nascita()`, guidata da `REGOLE_NASCITA`.
#
# ### E' UNA RIORGANIZZAZIONE, NON UNA CURA: byte-identica, zero bit.
#
# -----------------------------------------------------------------------------
# ### IL CONTRATTO DELL'ORDINE, MISURATO PRIMA DI SCRIVERE QUESTO BLOCCO
# -----------------------------------------------------------------------------
# `csv/_test_fork/_ordine_registro.py` (referto in `csv/_test_fork/_ordine_registro/`)
# ha misurato, sul blob `3d78cfd2`, se le scritture si possono PERMUTARE fra loro --
# che e' una domanda DIVERSA da quella dello STOP 4 (se si possono rendere CONTIGUE).
# ### QUATTRO vincoli genuini, e l'ordine del registro e' un ordine TOPOLOGICO VALIDO
# ### (0 violazioni):
#
#   1. `phi` DEVE stare prima di `twp` -- `twp` legge `phi[a,b]` DOPO il calcio, che
#      e' una scrittura INDICIZZATA sui genitori e quindi NON una pura estensione.
#      RISPETTATO: `phi` sta in `REGISTRO_METRI`, cioe' prima di tutto `REGISTRO_STATO`.
#   2. `peq` DEVE stare prima di `_peqn_idx` -- che legge `peq` INTERA. `_peqn_idx`
#      non sta in NESSUN registro, quindi e' DICHIARATO qui subito dopo `peq`.
#   3. `n0` VA NEL CONTESTO, calcolato nella PREPARAZIONE: le regole NON leggono
#      `self.n`. Motivo: `self.n` e' una `@property` su `len(self.phi)` (`:2651`),
#      quindi `n0 = self.n - k` dipendeva dall'estensione di `phi` -- quattro
#      LOCALI INTERPOSTE, misurate.
#   4. SEI CHIAMATE CON EFFETTO (`_smp_chirurgia`, `_traccia_d0`, `_grado`, tre per
#      evento) NON sono regole di nascita: si collocano a mano e si DICHIARANO con
#      `_nascita_collocata`.
#
# ### E DUE CASI SONO STATI SCARTATI COME INERTI, ed e' importante quanto trovarli:
# `chi_a`/`chi_b` leggono `perc_chi` GIA' estesa, ma la leggono sui GENITORI
# (indici `< n0`) e una pura estensione non tocca i primi `n0` elementi.
# -----------------------------------------------------------------------------

EVENTI_DI_NASCITA = ("semina", "divisione", "schwinger", "allaccio")
# ### I QUATTRO EVENTI SONO APPROVATI DA LUCA (2026-10-01, registrato nel piano).
#   ### MA SOLO DUE SONO CONVERTITI dal commit 3: `divisione` e `schwinger`, che
#   sono i due eventi di `mitosi` -- gli unici due da cui i `_eredita_*` erano
#   chiamati. `semina` e `allaccio` restano nelle loro funzioni e NON hanno ancora
#   una tabella: `nascita()` si RIFIUTA di girare per loro, invece di far finta.
EVENTI_CONVERTITI = ("divisione", "schwinger")


def _ordine_di_nascita():
    """L'ORDINE in cui la nascita scrive, e si DERIVA dai registri.

    L'ordine del REGISTRO -- `METRI`, poi `STATO`, poi `FINESTRA` -- con DUE
    grandezze COLLOCATE da un vincolo dichiarato:

    | | il vincolo | perche' |
    |---|---|---|
    | **2** | `_peqn_idx` subito **dopo `peq`** | l'indice segue la grandezza che indicizza |
    | **4** | `perc_geom` **dopo `tw`** | ### **la sua DERIVAZIONE LEGGE `tw`** |

    ### IL VINCOLO 4, E PERCHE' NON E' UN RIORDINO DI COMODO (`COMMIT 5`, 2026-10-03):
    `perc_geom` si DERIVA dalla sua definizione -- la media di `|tw|` sugli archi del
    nodo contro `PHI_CRIT`, la stessa di `chi_basc`. Nell'ordine del registro
    `perc_geom` cadeva **PRIMA di `tw`** (posto 17 contro 31), cioe' ### **prima che i
    nuovi archi avessero una torsione**: una derivazione scritta la' avrebbe letto lo
    stato VECCHIO e avrebbe dato `-1` ### **per il motivo sbagliato** -- la costante
    `-1` travestita da derivazione. ### E' una DIPENDENZA DI LETTURA, non una manopola.

    ### Si DERIVA e non si scrive a mano, cosi' una voce nuova nel registro fa scattare
    il presidio invece di passare inosservata.
    """
    fuori = []
    visto_pgeom = False
    for blocco in (REGISTRO_METRI, REGISTRO_STATO, REGISTRO_FINESTRA):
        for voce in blocco:
            if voce[0] == "perc_geom":
                # ### VINCOLO 4: `perc_geom` si colloca DOPO `tw`, non qui.
                visto_pgeom = True
                continue
            fuori.append(voce[0])
            if voce[0] == "peq":
                fuori.append("_peqn_idx")   # vincolo 2: DOPO `peq`
            if voce[0] == "tw":
                fuori.append("perc_geom")   # vincolo 4: la DERIVAZIONE legge `tw`
    # ### I DUE PRESIDI DEL VINCOLO 4, e non sono decorativi: senza di loro un cambio
    #   nei registri romperebbe il vincolo IN SILENZIO, e la derivazione leggerebbe un
    #   `tw` che non c'e' ancora -- cioe' tornerebbe a essere la costante `-1`
    #   travestita. `A9`: un vincolo SCRITTO non e' un presidio.
    if not visto_pgeom:
        raise RuntimeError(
            "`perc_geom` NON sta nei registri, ma il vincolo 4 la colloca dopo `tw`: "
            "l'ordine di nascita conterrebbe una grandezza che il registro non "
            "dichiara. Il vincolo 4 va rifatto insieme al registro.")
    if "perc_geom" not in fuori:
        raise RuntimeError(
            "`tw` NON sta nei registri, quindi il vincolo 4 non ha dove collocare "
            "`perc_geom`, e la grandezza SPARIREBBE dall'ordine di nascita -- cioe' il "
            "presidio del punto unico la segnalerebbe come non dichiarata. Il vincolo 4 "
            "va rifatto insieme al registro.")
    return tuple(fuori)


ORDINE_DI_NASCITA = _ordine_di_nascita()
REGOLE_NASCITA = {}


def _nascita_regola(evento, grandezza, classe, ancora, derivazione):
    """Dichiara LA REGOLA di nascita di una grandezza per un evento."""
    def _registra_regola(f):
        chiave = (evento, grandezza)
        if chiave in REGOLE_NASCITA:
            raise RuntimeError(
                "regola di nascita DOPPIA per `%s` all'evento `%s`" % (grandezza, evento))
        REGOLE_NASCITA[chiave] = {"classe": classe, "regola": f, "ancora": ancora,
                                  "derivazione": derivazione}
        return f
    return _registra_regola


def _nascita_collocata(evento, grandezza, chi, perche):
    """La grandezza e' scritta da una CHIAMATA CON EFFETTO, collocata a mano.

    ### NON e' una regola, e dirlo e' il punto: `_grado()` e `_smp_chirurgia()`
    scrivono, ma non sono *<<la regola di nascita di una grandezza>>*. Questa voce
    esiste perche' il presidio non si accontenti del silenzio.
    """
    REGOLE_NASCITA[(evento, grandezza)] = {"classe": "collocata", "regola": None,
                                           "ancora": chi, "derivazione": perche}


def _nascita_non_si_tocca(evento, grandezza, perche):
    """L'evento NON scrive questa grandezza, ed e' DICHIARATO."""
    REGOLE_NASCITA[(evento, grandezza)] = {"classe": "non si tocca", "regola": None,
                                           "ancora": "(nessuna)", "derivazione": perche}


def _riallinea_derivate_arco(net, evento, c):
    """### `keep` SI APPLICA ANCHE ALLE DERIVATE D ARCO, e non solo alle colonne.

    *(`VELENO-ARCHI-KEEP`, cura del 2026-10-05. **VIA (i), DECISIONE DI LUCA**: la
    nascita applica `keep` a TUTTE le derivate d arco PRIMA del veleno. La via (ii)
    -- far ricalcolare `dt_e` a chi lo legge -- e' SCARTATA: curava **un lettore
    solo**, lasciava `_sin2_vir` col difetto, e aggiungeva **una seconda scrittura**
    della legge di `dt_e`.)*

    ### IL DIFETTO CHE CURA, MISURATO (passo (1), `doc/REFERTO_veleno_archi_keep_2026-10-05.md`)
    La nascita ricostruisce le colonne d arco con `concat(x[keep], ...)`: **toglie**
    archi e ne **aggiunge** in coda. `_avvelena_derivate` allungava **solo in coda**
    con `NaN`, e ### **non applicava `keep`**. Quindi dal primo arco tolto in poi
    ### **ogni arco leggeva il valore di UN ALTRO arco** -- un valore **FINITO**, che
    il veleno non segnala.

    ### IL CONTO, e il numero misurato
    Con `s` archi divisi: tolti `s`, aggiunti `2s`, quindi il veleno appendeva
    `(m+s) - m = s` celle su `2s` archi nuovi -- ### **copertura `0.5000`, misurata
    `min = max` su 166 confronti.** Negli eventi **Schwinger**, che non hanno `keep`,
    la copertura era ### **`1.0000`** -- e l unica differenza fra i due casi era `keep`.
    ### ➜ Dopo questa cura `len(v) = sum(keep) = m - s`, quindi il veleno appende
    `(m+s) - (m-s) = 2s` celle: ### **copertura `1.0000` in ENTRAMBI i casi.**
    ### **La cura non aggiunge un comportamento: estende al caso che gli sfuggiva
    quello che il veleno faceva GIA' nell altro.**

    ### PERCHE' QUI E NON DENTRO IL VELENO
    Il veleno sta **dopo le regole** perche' deve conoscere le lunghezze NUOVE, e il
    suo commento lo dichiara. ### **Il riallineamento invece vuole la lunghezza
    VECCHIA**, che e' `len(keep)`: sono due istanti diversi, e metterli nella stessa
    funzione vorrebbe dire darle due bersagli. ### **Restano due funzioni, in fila.**

    ### NESSUN FLAG, ED E' LA STESSA SCELTA DEL VELENO
    *<<Il veleno agisce sempre>>*: un flag renderebbe un **presidio** un **opzione**,
    ed e' il difetto che `E4-LAM` ha curato. ### **Questa e' la riparazione di un
    difetto, non un esperimento: agisce sempre.**

    ### E SE LA LUNGHEZZA NON TORNA, NON SI INDOVINA
    Una derivata d arco **deve** avere la lunghezza degli archi di **PRIMA** della
    nascita, cioe' `len(keep)`. ### **Se non l ha, si ferma il run con
    `_ferma_registro`** -- le stesse eccezioni delle guardie esistenti.
    ### **Allungare o troncare qui sarebbe IL RIPIEGO che quel controllo esiste per
    impedire** (`RIPIEGHI-ZERO`, `A9`).
    """
    keep = None if c is None else c.get("keep")
    if keep is None:
        # ### L EVENTO NON TOGLIE ARCHI (e' lo Schwinger: `concat(net.i, aa, k)`).
        #   Niente da riallineare, e il veleno gia' copriva tutto: misurato `1.0000`.
        net._g_keep_senza = getattr(net, "_g_keep_senza", 0) + 1
        return
    keep = np.asarray(keep)
    if keep.dtype != bool:
        keep = keep.astype(bool)
    tenuti = np.flatnonzero(keep)
    for nome, dove, classe, _motivo in REGISTRO_DERIVATE:
        if dove != "arco" or classe != "avvelena":
            continue
        v = getattr(net, nome, None)
        if v is None:
            # ### non esiste ANCORA: per lei il difetto non c e' ancora, e si conta.
            net._g_keep_assenti = getattr(net, "_g_keep_assenti", 0) + 1
            continue
        v = np.asarray(v)
        if v.ndim != 1 or v.dtype.kind != "f":
            # ### LE STESSE DUE GUARDIE DEL VELENO, e per la stessa ragione: non si
            #   riallinea cio' che il veleno non sa avvelenare. Se una diventasse
            #   multiasse o intera, questo contatore salirebbe invece di far passare
            #   la cosa in silenzio (`A8`).
            net._g_keep_salti = getattr(net, "_g_keep_salti", 0) + 1
            continue
        if len(v) != len(keep):
            # ### NON SI INDOVINA: `_ferma_registro`, come le guardie esistenti.
            _ferma_registro(CacheCorta if len(v) < len(keep) else CacheLunga,
                             "CORTA" if len(v) < len(keep) else "LUNGA",
                             # ### `_scrivi_forma` ITERA l argomento: gli si passa la
                             #   FORMA, non l array -- altrimenti il messaggio
                             #   stamperebbe i VALORI. Una guardia che stampa
                             #   spazzatura e una guardia a meta.
                             nome, (len(keep),), v.shape,
                             "_riallinea_derivate_arco, evento `%s`" % evento)
        setattr(net, nome, v[tenuti])
        net._g_keep_riallineate = getattr(net, "_g_keep_riallineate", 0) + 1
        net._g_keep_celle_tolte = (getattr(net, "_g_keep_celle_tolte", 0)
                                   + int(len(v) - len(tenuti)))


def _avvelena_derivate(net):
    """### IL VELENO: le derivate dei nodi/archi NUOVI si riempiono di `NaN`.

    *(`COMMIT 4` del riordino, 2026-10-03. Terza via del par.(d), **approvata da Luca il
    2026-10-01** nella forma raffinata, e la **VIA A** scelta il 2026-10-03.)*

    ### PERCHE' IL VELENO E NON UNA MARCA LETTA A OGNI ACCESSO
    Intercettare **la lettura** costa: la sorveglianza ha misurato **1 887 282 accessi
    per passo**. Il veleno invece non costa niente a chi legge: ### **una lettura sporca
    PROPAGA il `NaN` nello stato, e il controllo lo prende al confine successivo** -- e
    un controllo di finitezza su tutte e 30 le voci di stato costa `0.002085 s`, cioe'
    lo ### **0.073 %** di un passo.

    ### E NON E UNA CONVENZIONE NUOVA: IL SISTEMA LO FA GIA' IN DUE PUNTI
    `peq` nasce `nan` in `_allaccia` *(`# da calibrare`)* e nello Schwinger con
    `PEQ_NASCITA_LOCALE`, e `step` la ### **CALIBRA**. ### *<<derivata sporca>>* e
    *<<`peq` da calibrare>>* sono ### **LA STESSA COSA**, e per `9-ter` questo conta: il
    commit 4 ### **da' un NOME a cio' che il sistema fa gia'.**

    ### L'ESENZIONE LA DICHIARA IL REGISTRO, NON QUESTO CODICE
    ### **NESSUN ELENCO A MANO QUI.** Si legge `REGISTRO_DERIVATE[...][2]`, e le voci
    `auto-rinfresco` si saltano. Il perche' di ciascuna e' nella sua riga di registro,
    col numero misurato. ### **Un elenco scritto qui sarebbe una seconda fonte, e
    divergerebbe.**

    ### E NON HA UN FLAG, ED E UNA SCELTA
    Un flag renderebbe il presidio ### **un'opzione** -- ed e' esattamente il difetto che
    `E4-LAM` ha curato *(<<il controllo era legge, chi la faceva rispettare era
    un'opzione>>)* e che `_nasce` dichiara di aver tolto *(<<IL GATE E' TOLTO: il
    presidio agisce SEMPRE>>)*. ### **Il veleno agisce sempre.**

    ### ⚠ E IL PREZZO E DICHIARATO E ACCETTATO (decisione di Luca): il passo della
    nascita ### **NON e' byte-identico sulle DERIVATE**, perche' una derivata che prima
    restava CORTA ora e' lunga e piena di `NaN`. ### **Il sigillo del commit 4 confronta
    al byte lo STATO, non le derivate** -- e' il solo criterio del piano che si
    restringe, ed e' una ### **DECISIONE**, non un allentamento.
    """
    n, m = len(net.phi), len(net.i)
    for nome, dove, classe, _motivo in REGISTRO_DERIVATE:
        if classe == "auto-rinfresco":
            # ### ESENTE, E LO DICE IL REGISTRO: il disallineamento di lunghezza E' il
            #   segnale con cui quella grandezza si ripulisce, e estenderla lo
            #   DISTRUGGEREBBE. Misurato: csv/_test_fork/_copertura_derivate/.
            net._g_veleno_esenti = getattr(net, "_g_veleno_esenti", 0) + 1
            continue
        v = getattr(net, nome, None)
        if v is None:
            net._g_veleno_assenti = getattr(net, "_g_veleno_assenti", 0) + 1
            continue
        v = np.asarray(v)
        bersaglio = n if dove == "nodo" else m
        if v.ndim != 1:
            # ### NON SI AVVELENA CIO' CHE NON SI SA AVVELENARE, e si CONTA: un array a
            #   piu' assi vorrebbe una riga di `NaN`, non un elemento. Oggi nessuna delle
            #   dieci e' cosi' (tutte 1-D), e se una lo diventasse questo contatore
            #   salirebbe invece di far passare la cosa in silenzio.
            net._g_veleno_multiasse = getattr(net, "_g_veleno_multiasse", 0) + 1
            continue
        if v.dtype.kind != "f":
            # ### E NON SI AVVELENA UN INTERO: `NaN` non esiste fra gli interi, e
            #   concatenarlo FORZEREBBE un cambio di dtype -- che il controllo unico
            #   prenderebbe come un difetto, giustamente. MISURATO: tutte e dieci le
            #   derivate sono `float64`, quindi questo ramo ha ZERO casi oggi.
            net._g_veleno_non_float = getattr(net, "_g_veleno_non_float", 0) + 1
            continue
        if len(v) >= bersaglio:
            # gia' lunga: la sua legge l'ha riscritta, oppure non c'erano nati per lei.
            net._g_veleno_gia_lunga = getattr(net, "_g_veleno_gia_lunga", 0) + 1
            continue
        quanti = bersaglio - len(v)
        # ### IL REGISTRO DEL VELENO: le CELLE avvelenate e L'IDENTITA' dell'array.
        #   (via (a) di `VELENO-DOMINI`, decisione di Luca del 2026-10-03.)
        #   Serve a `verifica_invarianti`, che senza di lui controllava il dominio di
        #   NOVE derivate come se fossero STATO -- e col veleno le faceva violare il
        #   dominio ### PER COSTRUZIONE (il run cadeva al passo 42 su `_dt_e_ultimo`).
        #
        #   ### SI TIENE IL RIFERIMENTO, NON `id()`, ED E' PIU' FORTE: un `id` si puo'
        #   RIUSARE dopo che l'oggetto e' stato liberato, e allora un registro scaduto
        #   sembrerebbe VIVO. Tenendo il riferimento l'oggetto non puo' essere liberato,
        #   quindi `is` e' ESATTO. ### Il prezzo e' UNA copia stantia per derivata, e
        #   vive al massimo fino al prossimo `verifica_invarianti`, che la cancella.
        #
        #   ### E LA CODA PRECEDENTE SI UNISCE, se e' ancora VIVA: in un passo con
        #   DUE nascite (divisione e Schwinger) il veleno gira due volte, e dopo la
        #   seconda le celle avvelenate sono l'UNIONE -- perche' `concatenate`
        #   conserva la testa, quindi i `nan` della prima sono ancora li'.
        _vreg = getattr(net, "_veleno_registro", None)
        if _vreg is None:
            _vreg = {}
            net._veleno_registro = _vreg
        _prec = _vreg.get(nome)
        _inizio = len(v)
        if _prec is not None and _prec["arr"] is v:
            _inizio = min(int(_prec["inizio"]), len(v))
        _nuovo = np.concatenate([v, np.full(quanti, np.nan)])
        setattr(net, nome, _nuovo)
        _vreg[nome] = {"arr": _nuovo, "inizio": int(_inizio), "fine": int(bersaglio)}
        net._g_veleno_voci = getattr(net, "_g_veleno_voci", 0) + 1
        net._g_veleno_celle = getattr(net, "_g_veleno_celle", 0) + int(quanti)


def _derivazione_perc_geom(net, c):
    """### LA DERIVAZIONE DI `perc_geom` PER I NATI, DALLA SUA DEFINIZIONE.

    ### `+1` se la media di `|tw|` sugli archi del nodo supera `PHI_CRIT`, altrimenti
    `-1`. ### E' la STESSA definizione di `chi_basc`, non una regola parallela:
    `chi_basc` la riapplica a TUTTA la rete al passo dopo, e ### **se il nato nascesse
    con un valore che la definizione non da', il sistema si contraddirebbe per un
    passo** -- e quel passo il frame-drag lo LEGGE.

    ### PERCHE' UNA DERIVAZIONE E NON LA COSTANTE `-1` *(decisione di Luca, 2026-09-29)*:
    oggi il nato ha archi con `tw = 0`, quindi la derivazione ### **da' `-1` sempre** --
    e scrivere `-1` darebbe lo STESSO numero. ### Ma `DIVISIONE-AUTOCONSISTENTE`, se
    decidera' che i figli nascono con una torsione, ### **cambierebbe la risposta**: una
    costante resterebbe `-1` e sarebbe ### **sbagliata in silenzio**, una derivazione
    segue. ### E i contatori `_g_pgeom_der_m1`/`_p1` esistono per questo: dicono
    ### **quante volte la derivazione ha davvero DECISO**, invece di far credere a una
    costante che ha deciso.

    ### LE DUE DIFFERENZE DA `chi_basc`, DICHIARATE e non nascoste:

    | | `chi_basc` | qui, alla nascita |
    |---|---|---|
    | il grado | `self._deg` | ### **RICALCOLATO da `i`/`j`** -- `_grado()` e' `collocata` e gira **DOPO** `nascita()`, quindi dentro la nascita `_deg` e' **STANTIO** |
    | la torsione | `_tw_t`, uno ### **SNAPSHOT** preso prima nel passo | ### **`net.tw`** -- alla nascita non esiste nessuno snapshot |

    ### E NON LEGGE `self.n` *(vincolo 3 del contratto)*: il numero dei nodi del DOPO si
    ricava da `c["n0"] + c["quante"]`.
    """
    n0 = int(c["n0"])
    quante = int(c["quante"])
    n = n0 + quante
    if quante <= 0 or n <= 0 or not len(net.i):
        return np.zeros(0, dtype=net.perc_geom.dtype)
    # il GRADO, come lo calcola `_grado()` -- che qui non e' ancora girato
    deg = np.maximum(np.bincount(net.i, minlength=n) +
                     np.bincount(net.j, minlength=n), 1)[:n]
    twabs = np.abs(net.tw)
    twn = np.zeros(n)
    np.add.at(twn, net.i, twabs)
    np.add.at(twn, net.j, twabs)
    twn = twn / deg
    nuovi = np.where(twn[n0:n] > PHI_CRIT, 1, -1).astype(net.perc_geom.dtype)
    net._g_pgeom_der_m1 = getattr(net, "_g_pgeom_der_m1", 0) + int(np.sum(nuovi < 0))
    net._g_pgeom_der_p1 = getattr(net, "_g_pgeom_der_p1", 0) + int(np.sum(nuovi > 0))
    return nuovi


def nascita(net, evento, c):
    """### IL PUNTO UNICO: scrive le grandezze della nascita, in ordine DICHIARATO.

    `c` e' il CONTESTO: tutto cio' che le regole leggono oltre a `net.<grandezza>`
    -- i genitori, i figli, `n0`, i valori preparati. ### Le regole NON leggono
    `self.n` (vincolo 3 del contratto): ricevono `c["n0"]`.

    ### IL PRESIDIO: una grandezza del registro che non compare nella tabella
    ### dell'evento FERMA IL RUN. Non e' un avviso: e' un `RuntimeError`.
    """
    if evento not in EVENTI_DI_NASCITA:
        raise RuntimeError("evento di nascita sconosciuto: `%s`. I quattro approvati "
                           "sono %s" % (evento, ", ".join(EVENTI_DI_NASCITA)))
    if evento not in EVENTI_CONVERTITI:
        raise RuntimeError(
            "l'evento `%s` NON e' ancora convertito al punto unico: la sua nascita vive "
            "nella sua funzione, e questa tabella non la descrive. I convertiti sono %s."
            % (evento, ", ".join(EVENTI_CONVERTITI)))
    for nome in ORDINE_DI_NASCITA:
        voce = REGOLE_NASCITA.get((evento, nome))
        if voce is None:
            raise RuntimeError(
                "regola di nascita non dichiarata per `%s` all'evento `%s`. "
                "Ogni grandezza del registro vuole una riga nella tabella: una REGOLA, "
                "oppure `collocata` (la scrive una chiamata con effetto), oppure "
                "`non si tocca`. Il silenzio NON e' una terza possibilita'."
                % (nome, evento))
        if voce["regola"] is not None:
            voce["regola"](net, c)
    # ### IL VELENO, e sta QUI perche' QUI e' il punto unico della nascita
    #   (`COMMIT 4`). Dopo che tutte le regole hanno scritto, le derivate dei
    #   nodi/archi NUOVI si riempiono di `NaN` -- tranne quelle che il REGISTRO
    #   dichiara `auto-rinfresco`.
    #   ### PERCHE' DOPO E NON PRIMA: il veleno estende fino a `len(net.phi)` e
    #   `len(net.i)`, cioe' alle lunghezze NUOVE -- e quelle le stabiliscono le
    #   regole di `phi` e di `i`. Prima del blocco non esisterebbero ancora.
    #   ### E PER EVENTO, non per passo: ogni chiamata a `nascita` aggiunge nodi o
    #   archi, quindi ogni chiamata avvelena cio' che ha appena allungato.
    # ### [VELENO-ARCHI-KEEP, cura del 2026-10-05, VIA (i), DECISIONE DI LUCA]
    #   `keep` SI APPLICA ANCHE ALLE DERIVATE D ARCO, e PRIMA del veleno.
    #   ### PERCHE PRIMA: il veleno allunga fino alla lunghezza NUOVA; il
    #   riallineamento vuole quella VECCHIA (`len(keep)`). Sono due istanti, e
    #   l ordine fra loro E la cura: riallinea, POI avvelena il resto.
    #   ### IL DIFETTO MISURATO (passo (1)): senza questo, dal primo arco tolto
    #   in poi ogni arco leggeva il valore di UN ALTRO arco -- un valore FINITO,
    #   che il veleno non segnala -- e la copertura del veleno era `0.5000` nelle
    #   divisioni contro `1.0000` negli Schwinger, con `keep` come UNICA
    #   differenza. Misurato `min = max` su 166 confronti.
    _riallinea_derivate_arco(net, evento, c)
    _avvelena_derivate(net)
    # ### E QUI NON C'E' UN CONTATORE DELLE NASCITE, ED E' UNA SCELTA.
    #   La prima stesura ne aveva uno (`_g_nascite`). L'ho tolto per due ragioni:
    #   ### ① il criterio del commit 3 e' BYTE-IDENTICO, e un contatore nuovo
    #     obbligherebbe il sigillo a DICHIARARE UN'ECCEZIONE -- e un criterio con
    #     un'eccezione e' piu' debole di uno senza. Luca l'ha detto per l'ordine
    #     delle estrazioni, e vale qui: ### **non si allenta il criterio.**
    #   ### ② `9-ter`: una cura non aumenta il numero delle grandezze. Gli eventi
    #     di nascita SONO GIA' CONTATI, e per RAMO, da `_g_nati_mitosi_ev` e
    #     `_g_nati_schwinger_ev` -- che e' il conto che serve, perche' i due rami
    #     fanno cose diverse alla carica. Un totale non distingue le due cose.


# -----------------------------------------------------------------------------
# ### LE REGOLE, evento per evento, NELL'ORDINE DEL REGISTRO
# -----------------------------------------------------------------------------
# Ogni regola e' l'ESPRESSIONE DI PRIMA, verbatim: il commit 3 sposta, non cura.
# Dove una condizione c'era, c'e'; dove un contatore si alzava, si alza.
# -----------------------------------------------------------------------------

# --- `phi`, `i`, `j`: i METRI ------------------------------------------------

@_nascita_regola("divisione", "phi", "media (fase media dei genitori)",
                 "self.phi = np.concatenate([self.phi, fm])",
                 "`fm` e' il punto medio di fase fra i genitori, calcolato nella "
                 "preparazione (con `MITOSI_DIR` spostato verso il genitore piu' teso, "
                 "e con `ANTIFASE_ADD` eventualmente ribaltato di mezzo giro)")
def _rn_div_phi(net, c):
    net.phi = np.concatenate([net.phi, c["fm"]])


@_nascita_regola("divisione", "i", "topologia: l'arco si spezza in due",
                 "self.i = np.concatenate([self.i[keep], a, m])",
                 "l'arco `a-b` sparisce (`keep`) e nascono `a-m` e `m-b`: `i` prende "
                 "`a` e `m`, `j` prende `m` e `b`. ORDINE ESSENZIALE: e' una "
                 "concatenazione, e l'ordine DECIDE la topologia")
def _rn_div_i(net, c):
    net.i = np.concatenate([net.i[c["keep"]], c["a"], c["m"]])


@_nascita_regola("divisione", "j", "topologia: l'arco si spezza in due",
                 "self.j = np.concatenate([self.j[keep], m, b])",
                 "il compagno di `i`: insieme danno `a-m` e `m-b`")
def _rn_div_j(net, c):
    net.j = np.concatenate([net.j[c["keep"]], c["m"], c["b"]])


# --- le cache per NODO, assorbite da `_eredita_spinore_figli` ----------------
# ### QUESTA FUNZIONE SPARISCE, e le sue 12 grandezze entrano qui. E' nata dalle
#   cure di `C7`/`C11`: senza di lei, dopo ogni mitosi `len(cache) != n` e il
#   sistema cadeva nei ripieghi -- MISURATO nell'80% dei passi per `_cs_nodo_prev`
#   e nel 95.33% delle chiamate per `_psi_spin_prec`. Il riordino non la butta:
#   la ASSORBE, e la storia resta scritta qui.

@_nascita_regola("divisione", "_cs_nodo_prev", "eredita dal genitore `a`",
                 "self._cs_nodo_prev = np.concatenate([_csp, np.asarray(_csp, float)[src]])",
                 "STA PRIMA della guardia sugli spinori DI PROPOSITO: questa cache vive "
                 "sotto `CS_DINAMICO and (FORK_SU2_MEM or STEP2_OROLOGIO)`, NON sotto "
                 "`--spinore-corretto`. Senza, `len(_cs_nodo_prev) < n` e `tau = d/cs` "
                 "calcolava `d/CS_M`: MISURATO nell'80% dei passi. "
                 "NB: concatena `_csp` INTERO, non `_csp[:n0]` -- convenzione diversa da "
                 "quella di `psi`, e si conserva tale")
def _rn_div_cs_nodo_prev(net, c):
    if not c["eredita_vale"]:
        return
    _csp_er = getattr(net, "_cs_nodo_prev", None)
    if _csp_er is not None and len(_csp_er) >= c["n0"]:
        net._cs_nodo_prev = np.concatenate([_csp_er, np.asarray(_csp_er, float)[c["src"]]])


_nascita_collocata("divisione", "_deg", "self._grado()",
                   "la scrive `_grado()`, collocata DOPO il blocco perche' LEGGE `i`, `j` "
                   "e `len(phi)`: e' una DERIVATA della topologia, non una regola di "
                   "nascita. Insieme a `_deg` invalida `_cicli_topologici` e richiama "
                   "`_costruisci_struttura`")


@_nascita_regola("divisione", "_nb", "eredita dal genitore `a`",
                 "self._nb = np.vstack([self._nb, self._nb[src]])",
                 "il Bloch del figlio e' quello del padre. ### E IL SUO ESITO E' UNA "
                 "CONDIZIONE PER `_nb_prec`: oggi `_nb_prec` e' estesa solo DENTRO il ramo "
                 "di `_nb`, ed e' una dipendenza di CONTROLLO, non di dato -- quindi non la "
                 "vedrebbe nessun grafo sui dati. Si conserva passando l'esito nel contesto")
def _rn_div_nb(net, c):
    c["_nb_esteso"] = False
    if not (c["eredita_vale"] and c["spinore_vale"]):
        return
    if hasattr(net, "_nb") and net._nb is not None and len(net._nb) >= c["n0"]:
        net._nb = np.vstack([net._nb, net._nb[c["src"]]])
        c["_nb_esteso"] = True


@_nascita_regola("divisione", "_nb_prec", "eredita dal genitore `a`",
                 "self._nb_prec = np.vstack([self._nb_prec, self._nb_prec[src]])",
                 "### SOLO SE `_nb` E' STATA ESTESA: e' il nido di oggi, conservato")
def _rn_div_nb_prec(net, c):
    if not c.get("_nb_esteso"):
        return
    if (hasattr(net, "_nb_prec") and net._nb_prec is not None
            and len(net._nb_prec) >= c["n0"]):
        net._nb_prec = np.vstack([net._nb_prec, net._nb_prec[c["src"]]])


@_nascita_regola("divisione", "_nb_ret", "eredita dal genitore `a`",
                 "self._nb_ret = np.vstack([_nbr_er, _nbr_er[src]])",
                 "[FORK SU(2) STRATO 1] il Bloch RITARDATO e' memoria di NODO: il figlio "
                 "eredita il passato del padre. Senza, al passo dopo `len(_nb_ret) != n` e "
                 "la memoria veniva RESETTATA a ogni mitosi")
def _rn_div_nb_ret(net, c):
    if not (c["eredita_vale"] and c["spinore_vale"]):
        return
    _nbr_er = getattr(net, "_nb_ret", None)
    if _nbr_er is not None and len(_nbr_er) >= c["n0"]:
        net._nb_ret = np.vstack([_nbr_er, _nbr_er[c["src"]]])


@_nascita_regola("divisione", "_psi_prec", "eredita dal genitore `a`",
                 "self._psi_prec = np.concatenate([self._psi_prec, self._psi_prec[src]])",
                 "evita il reset spurio GLOBALE in `ritmo()` su `len != n`")
def _rn_div_psi_prec(net, c):
    if not (c["eredita_vale"] and c["spinore_vale"]):
        return
    if net._psi_prec is not None and len(net._psi_prec) >= c["n0"]:
        net._psi_prec = np.concatenate([net._psi_prec, net._psi_prec[c["src"]]])


@_nascita_regola("divisione", "_psi_spin_prec", "eredita dal genitore `a`",
                 "self._psi_spin_prec = np.vstack([_pspr, np.asarray(_pspr)[src]])",
                 "SNAPSHOT DEL RITMO SPINORIALE (4pi). Senza, `len(_psi_spin_prec) != n` e "
                 "la guardia ESATTA di `ritmo()` scartava il ramo a 4pi: MISURATO nel "
                 "95.33% delle chiamate, e la FASE 5 era INERTE in ogni run "
                 "`--campo-spinoriale`. E' `n x 2` COMPLESSO, quindi `vstack`")
def _rn_div_psi_spin_prec(net, c):
    if not (c["eredita_vale"] and c["spinore_vale"]):
        return
    _pspr = getattr(net, "_psi_spin_prec", None)
    if _pspr is not None and len(_pspr) >= c["n0"]:
        net._psi_spin_prec = np.vstack([_pspr, np.asarray(_pspr)[c["src"]]])


@_nascita_regola("divisione", "_psi_spinor", "eredita col SEGNO (regola D)",
                 "self._psi_spinor = np.vstack([self._psi_spinor, er])",
                 "eredita lo spinore COMPLESSO col segno, non un Bloch ri-derivato. "
                 "`segno = +1` per la mitosi; `-1` per l'antinodo (doppia copertura opposta)")
def _rn_div_psi_spinor(net, c):
    if not (c["eredita_vale"] and c["spinore_vale"]):
        return
    if len(net._psi_spinor) >= c["n0"]:
        er = net._psi_spinor[c["src"]].copy()
        if c["segno"] < 0:
            er = -er
        net._psi_spinor = np.vstack([net._psi_spinor, er])


@_nascita_regola("divisione", "_spinor_lift", "eredita col SEGNO (regola D)",
                 "self._spinor_lift = np.vstack([self._spinor_lift, el])",
                 "il sollevamento, con la stessa convenzione di segno di `_psi_spinor`")
def _rn_div_spinor_lift(net, c):
    if not (c["eredita_vale"] and c["spinore_vale"]):
        return
    if len(net._spinor_lift) >= c["n0"]:
        el = net._spinor_lift[c["src"]].copy()
        if c["segno"] < 0:
            el = -el
        net._spinor_lift = np.vstack([net._spinor_lift, el])


@_nascita_regola("divisione", "conc_nodi", "eredita la concorrenza del genitore `a`",
                 "self.conc_nodi.append(eredita)",
                 "### QUESTA REGOLA CURA LA CRESCITA PER MUTAZIONE: prima `conc_nodi` era "
                 "l'UNICA grandezza del registro che cresceva con `.append`, cioe' "
                 "INVISIBILE all'AST e alla sorveglianza. Ora e' una SCRITTURA VERA. "
                 "### E IL `len` CRESCENTE SI CONSERVA: `.append` dentro il ciclo faceva "
                 "crescere `len(self.conc_nodi)` a ogni giro, quindi un `kk` scartato "
                 "all'inizio poteva passare il test piu' tardi. Si costruisce la lista "
                 "nuova e si appende A QUELLA, non alla vecchia: stesso comportamento, "
                 "anche nel caso limite")
def _rn_div_conc_nodi(net, c):
    if not net.conc_nodi:
        return
    nuovo = list(net.conc_nodi)
    for kk in c["a"]:
        eredita = [v[:] for v in nuovo[kk]] if kk < len(nuovo) else []
        nuovo.append(eredita)
    net.conc_nodi = nuovo


@_nascita_regola("divisione", "eta", "zero",
                 "self.eta = np.concatenate([self.eta, np.zeros(len(sel))])",
                 "il figlio nasce senza `eta`")
def _rn_div_eta(net, c):
    net.eta = np.concatenate([net.eta, np.zeros(c["quante"])])


@_nascita_regola("divisione", "mem_mot", "eredita dal genitore `a`",
                 "self.mem_mot = np.vstack([self.mem_mot, self.mem_mot[a]]) if len(...) "
                 "else np.zeros((len(sel), 3))",
                 "la memoria di moto del padre; se la memoria non c'e' ancora, zeri")
def _rn_div_mem_mot(net, c):
    net.mem_mot = (np.vstack([net.mem_mot, net.mem_mot[c["a"]]])
                   if len(net.mem_mot) else np.zeros((c["quante"], 3)))


@_nascita_regola("divisione", "omega_s", "eredita dal genitore `a`",
                 "self.omega_s = np.vstack([self.omega_s, self.omega_s[src]])",
                 "il ritmo spinoriale del padre")
def _rn_div_omega_s(net, c):
    if not (c["eredita_vale"] and c["spinore_vale"]):
        return
    if len(net.omega_s) >= c["n0"]:
        net.omega_s = np.vstack([net.omega_s, net.omega_s[c["src"]]])


@_nascita_regola("divisione", "perc_chi", "eredita la chiralita' del genitore `a`",
                 "self.perc_chi = np.concatenate([self.perc_chi, self.perc_chi[a]])",
                 "[CHI_COOP via 2 di 3] profilo dormiente, non ancora accoppiato. "
                 "### E QUESTO RAMO SPOSTA `N(+1) - N(-1)` DI `+segno(perc_chi[a])` PER "
                 "FIGLIO: aggiunge un nodo dello STESSO segno del genitore. L'altro ramo "
                 "(Schwinger) lo sposta nel verso OPPOSTO, e ### ⚠ I DUE SI CANCELLANO "
                 "SOLO SUGLI ARCHI DOVE SCATTANO ENTRAMBI: la conservazione e' DELLA "
                 "COPPIA, non della somma dei due rami. ### MISURATO: 9 contro 1 in 72 "
                 "passi, cioe' +8. ### Per questo i nati si contano DUE volte e non una: "
                 "un totale non direbbe da dove viene la carica.")
def _rn_div_perc_chi(net, c):
    net.perc_chi = np.concatenate([net.perc_chi, net.perc_chi[c["a"]]])


@_nascita_regola("divisione", "perc_geom", "DERIVATA dalla definizione (non eredita)",
                 "self.perc_geom = np.concatenate([self.perc_geom, "
                 "_derivazione_perc_geom(self, c)])",
                 "[COMMIT 5, decisione di Luca del 2026-09-29] ### NON SI EREDITA PIU': la "
                 "geometria e' *<<il giro e' compiuto o no>>*, e questo si LEGGE dagli archi "
                 "del nodo -- la media di `|tw|` contro `PHI_CRIT`, la STESSA definizione di "
                 "`chi_basc`. Un valore EREDITATO poteva CONTRADDIRE la definizione, e per un "
                 "passo il frame-drag lo leggeva. ### Il nato ha archi con `tw = 0`, quindi "
                 "OGGI la derivazione da' `-1`; scritta come DERIVAZIONE e non come costante "
                 "resta giusta quando `DIVISIONE-AUTOCONSISTENTE` dara' ai figli una torsione")
def _rn_div_perc_geom(net, c):
    net.perc_geom = np.concatenate([net.perc_geom, _derivazione_perc_geom(net, c)])


@_nascita_regola("divisione", "perc_tw", "zero",
                 "self.perc_tw = np.concatenate([self.perc_tw, np.zeros(len(sel))])",
                 "salto a 0: il profilo di torsione percorso riparte")
def _rn_div_perc_tw(net, c):
    net.perc_tw = np.concatenate([net.perc_tw, np.zeros(c["quante"])])


@_nascita_regola("divisione", "phi0", "media (come `phi`)",
                 "self.phi0 = np.concatenate([self.phi0, fm])",
                 "la fase di riferimento nasce DOVE nasce la fase: lo stesso `fm`")
def _rn_div_phi0(net, c):
    net.phi0 = np.concatenate([net.phi0, c["fm"]])


@_nascita_regola("divisione", "phi_s", "eredita dal genitore `a`",
                 "self.phi_s = np.concatenate([self.phi_s, self.phi_s[a]])",
                 "lo spinore di fase del padre -- ed e' il COMPAGNO di `psi_spin`, che "
                 "eredita per la stessa ragione")
def _rn_div_phi_s(net, c):
    net.phi_s = np.concatenate([net.phi_s, net.phi_s[c["a"]]])


@_nascita_regola("divisione", "phivel", "media dei genitori",
                 "self.phivel = np.concatenate([self.phivel, 0.5 * (self.phivel[a] + "
                 "self.phivel[b])])",
                 "la velocita' di fase media. SOMMA DI DUE ADDENDI: in IEEE-754 "
                 "l'addizione e' COMMUTATIVA, quindi l'ordine dei due genitori NON cambia "
                 "un bit (misurato). Da TRE addendi non lo sarebbe")
def _rn_div_phivel(net, c):
    net.phivel = np.concatenate([net.phivel, 0.5 * (net.phivel[c["a"]] + net.phivel[c["b"]])])


@_nascita_regola("divisione", "pos", "media dei genitori (punto medio)",
                 "self.pos = np.vstack([self.pos, pos_figlio])",
                 "il figlio nasce sul punto medio geometrico; l'asimmetria della mitosi "
                 "diretta vive nella FASE, non nella posizione")
def _rn_div_pos(net, c):
    net.pos = np.vstack([net.pos, c["pos_figlio"]])


# --- `psi`, `psi_spin`, `rho_spin`: assorbite da `_eredita_psi_figli` --------
# ### LE DUE REGOLE NON SONO UGUALI, E NON PER CASO (decisione di Luca, 2026-09-28):
#   `psi` fa la MEDIA perche' il suo compagno `phi` fa la media (`fm`); `psi_spin`
#   EREDITA perche' il suo compagno `phi_s` eredita. Dare a ciascuno la regola del
#   PROPRIO compagno e' l'unica scelta che non aggiunge una convenzione (`9-ter`).

@_nascita_regola("divisione", "psi", "media dei genitori (come `phi`)",
                 "self.psi = np.concatenate([cur[:n0], 0.5 * (cur[a] + cur[b])])",
                 "e la somma e' COMPLESSA: due genitori in antifase danno un figlio con "
                 "`|psi| ~ 0`. E' interferenza distruttiva, cioe' FISICA, non un errore. "
                 "SI CONTA e non si assume (`A8`): se la cache non e' allineata a `n0` non "
                 "si puo' ereditare, e quel salto e' cio' che faceva spegnere la "
                 "schermatura per TUTTA la rete (`PSI-FLASH`)")
def _rn_div_psi(net, c):
    if not c["eredita_vale"]:
        return
    net._g_eredpsi_tot = getattr(net, "_g_eredpsi_tot", 0) + 1
    cur = getattr(net, "psi", None)
    if cur is not None and len(cur) >= c["n0"]:
        net.psi = np.concatenate([cur[:c["n0"]], 0.5 * (cur[c["src_a"]] + cur[c["src_b"]])])
    else:
        net._g_eredpsi_salti = getattr(net, "_g_eredpsi_salti", 0) + 1
        net._g_eredpsi_shape = (len(cur) if cur is not None else -1, c["n0"])


@_nascita_regola("divisione", "psi_spin", "eredita da `a` (come `phi_s`)",
                 "self.psi_spin = np.concatenate([cs[:n0], cs[a]])",
                 "eredita, non media: il compagno `phi_s` eredita")
def _rn_div_psi_spin(net, c):
    if not c["eredita_vale"]:
        return
    cs = getattr(net, "psi_spin", None)
    if cs is not None and len(cs) >= c["n0"]:
        net.psi_spin = np.concatenate([cs[:c["n0"]], cs[c["src_a"]]])
    else:
        net._g_eredpsis_salti = getattr(net, "_g_eredpsis_salti", 0) + 1


@_nascita_regola("divisione", "rho_spin", "eredita da `a` (come `psi_spin`)",
                 "self.rho_spin = np.concatenate([np.asarray(rs)[:n0], np.asarray(rs)[a]])",
                 "[PSI-FLASH] `rho_spin` COME `psi_spin`, e NON e' un'aggiunta ovvia: senza, "
                 "`_rho_sorgente` prendeva il suo ripiego AL PASSO DOPO la nascita e "
                 "restituiva `|psi|^2` invece di `rho_spin` PER TUTTA LA RETE -- il GRADINO "
                 "del +11%. Sono la stessa grandezza vista in due modi, "
                 "`rho_spin = psi_spin^dag psi_spin`")
def _rn_div_rho_spin(net, c):
    if not c["eredita_vale"]:
        return
    rs = getattr(net, "rho_spin", None)
    if rs is not None and len(rs) >= c["n0"]:
        net.rho_spin = np.concatenate([np.asarray(rs)[:c["n0"]],
                                       np.asarray(rs)[c["src_a"]]])
    else:
        net._g_eredrho_salti = getattr(net, "_g_eredrho_salti", 0) + 1


# --- le grandezze per ARCO ---------------------------------------------------

@_nascita_regola("divisione", "_rep", "eredita dall'arco che si spezza",
                 "self._rep = np.concatenate([self._rep[keep], self._rep[sel], "
                 "self._rep[sel]])",
                 "`_rep` e' per ARCO e segue la STESSA struttura degli altri array per "
                 "arco: NON si eredita da `src` come gli stati per NODO. I due archi figli "
                 "ereditano la memoria dell'arco da cui nascono, che e' cio' che "
                 "`[sel], [sel]` fa")
def _rn_div_rep(net, c):
    net._rep = np.concatenate([net._rep[c["keep"]], net._rep[c["sel"]], net._rep[c["sel"]]])


@_nascita_regola("divisione", "d", "meta' dell'arco (due tronconi)",
                 "self.d = np.concatenate([self.d[keep], dh])  # `dh` e' GIA' i due "
                 "blocchi",
                 "`dh` e' ora i DUE BLOCCHI (`t*d[sel]` per `a`-`m` e `(1-t)*d[sel]` per "
                 "`m`-`b`), passati per `_nasce('mitosi', 1, 0, meta=len(dh_a))`: `md = 1` "
                 "e non 2 perche' ogni voce e' ora UN arco vero, e `meta` fa calcolare "
                 "`_fab` PER META' cosi' `_sm_lun` resta identico al bit. Nella preparazione: "
                 "e' il dimezzamento che produce la compressione degenere, perche' la "
                 "geometria di equilibrio si accorcia a ogni suddivisione")
def _rn_div_d(net, c):
    # ### UNA VOLTA SOLA: `dh` e' GIA' l'array dei due blocchi (`a`-`m` e `m`-`b`). Con
    #   `dh, dh` darebbe ### **4n archi**.
    net.d = np.concatenate([net.d[c["keep"]], c["dh"]])


@_nascita_regola("divisione", "d0", "meta' dell'arco, con offset plastico",
                 "self.d0 = np.concatenate([self.d0[keep], d0new])",
                 "con `PLAST_DIN` l'offset e' emergente (stress metrico per eccesso di "
                 "torsione, saturato); con `PLAST_MIT > 0` e' proporzionale a `sciolta`; "
                 "altrimenti e' `dh` nudo. `d0new` e' GIA' i DUE BLOCCHI (dai due mezzi "
                 "`dh_a` e `dh_b`, nello stesso ordine), cioe' i due "
                 "figli, e passa per `_nasce('mitosi', 0, 1)`. "
                 "### ⚠ E IL NOME `sciolta` PRESUPPONE UNA COSA NON MISURATA: `sciolta` "
                 "e' solo `|tw|/PHI_CRIT`, cioe' LA TORSIONE DELL'ARCO IN UNITA' DEL "
                 "QUANTO -- e <<sciolta>> suggerisce che sia stata LIBERATA e spesa da "
                 "qualche parte. ### NON LO E': vedi la regola di `tw` e "
                 "`DIVISIONE-AUTOCONSISTENTE:M1`. ### Il nome NON si cambia qui (sarebbe "
                 "una riga di logica in un commit di soli commenti): e' IN CODA.")
def _rn_div_d0(net, c):
    net.d0 = np.concatenate([net.d0[c["keep"]], c["d0new"]])


@_nascita_regola("divisione", "peq", "eredita dall'arco che si spezza",
                 "self.peq = np.concatenate([self.peq[keep], self.peq[sel], self.peq[sel]])",
                 "### L'EREDITA' DELLA MITOSI NON SI TOCCA, e il perche' e' una frase di "
                 "`PEQ_NASCITA_LOCALE`: *un arco che si spezza non NASCE, CONTINUA*. Per "
                 "questo qui non c'e' `nan` e nello Schwinger si'")
def _rn_div_peq(net, c):
    net.peq = np.concatenate([net.peq[c["keep"]], net.peq[c["sel"]], net.peq[c["sel"]]])


_nascita_non_si_tocca("divisione", "_peqn_idx",
                      "la marca degli archi nati con `peq = nan` esiste SOLO per lo "
                      "Schwinger: la mitosi non ne crea (eredita `peq`, non lo lascia da "
                      "calibrare). DICHIARATO, non omesso")


@_nascita_regola("divisione", "tw", "zero",
                 "self.tw = np.concatenate([self.tw[keep], zz, zz])",
                 "i due tronconi nascono con `tw = 0`: la torsione dell'arco SPARISCE. "
                 "### IL CALCIO LA USA COME MISURA MA NON LA CONSERVA: `|tw|` decide "
                 "QUANTO colpire i genitori, e l'avvolgimento NON viene trasferito -- "
                 "MISURATO: `DIVISIONE-AUTOCONSISTENTE:M1`, ~1.2 giri persi per arco "
                 "diviso, SENZA BILANCIO. Se debba conservarsi e' "
                 "`DIVISIONE-AUTOCONSISTENTE`, APERTA. "
                 "### ⛔ E LA FRASE DI PRIMA ERA FALSA, e la lascio scritta perche' un "
                 "errore non si cancella (par.8): diceva che la torsione era <<SCIOLTA "
                 "dalla divisione, ed e' cio' che il calcio ha SPESO>>, cioe' DAVA PER "
                 "RISOLTA una domanda aperta. Rilievo del guardiano, 2026-10-03.")
def _rn_div_tw(net, c):
    zz = np.zeros(c["quante"])
    net.tw = np.concatenate([net.tw[c["keep"]], zz, zz])


@_nascita_regola("divisione", "twp", "differenza di fase genitore-figlio",
                 "self.twp = np.concatenate([self.twp[keep], self._wphi(self.phi[a] - fm), "
                 "self._wphi(fm - self.phi[b])])",
                 "### VINCOLO 1 DEL CONTRATTO: legge `phi[a]`/`phi[b]` DOPO il calcio, che "
                 "e' una scrittura INDICIZZATA sui genitori -- quindi `phi` deve stare "
                 "PRIMA, e nell'ordine del registro ci sta (`METRI` precede `STATO`)")
def _rn_div_twp(net, c):
    net.twp = np.concatenate([net.twp[c["keep"]],
                              net._wphi(net.phi[c["a"]] - c["fm"]),
                              net._wphi(c["fm"] - net.phi[c["b"]])])


@_nascita_regola("divisione", "vd", "eredita dall'arco che si spezza",
                 "self.vd = np.concatenate([self.vd[keep], self.vd[sel], self.vd[sel]])",
                 "la velocita' metrica dell'arco si eredita come `_rep` e `peq`")
def _rn_div_vd(net, c):
    net.vd = np.concatenate([net.vd[c["keep"]], net.vd[c["sel"]], net.vd[c["sel"]]])


for _nome_smp in ("_smp_d0", "_smp_d"):
    _nascita_collocata("divisione", _nome_smp, "self._smp_chirurgia(keep=keep, nuovi=d0new)",
                       "[SCALA_MIN_PASSO C3 / COES_CAUSALE C4] la fotografia di inizio passo "
                       "subisce LE STESSE operazioni di `d0`, altrimenti un confronto "
                       "`fine - inizio` per posizione confronterebbe ARCHI DIVERSI. NON e' "
                       "una regola di nascita: e' una CHIRURGIA sullo snapshot, e si colloca "
                       "nella preparazione perche' legge solo `keep` e `d0new`")

# =============================================================================
# ### EVENTO `schwinger`: la creazione di coppia
# =============================================================================
# L'anti-nodo nasce a fase `fm + pi`, collegato ai due genitori `aa`-`bb`. La
# coppia (nodo `fm` + antinodo `fm+pi`) ha media `fm`, quindi CONSERVA l'olonomia
# globale, ma introduce due difetti opposti.
# ### E QUESTO E' IL RAMO CHE CONSERVA `N(+1) - N(-1)`: la carica nasce OPPOSTA.
# =============================================================================


@_nascita_regola("schwinger", "phi", "antifase del figlio di mitosi",
                 "self.phi = np.concatenate([self.phi, anti])",
                 "[FASE_2PI, D35] L'ANTIFASE E' META' DEL DOMINIO: `+pi` su 2pi, `+2pi` su "
                 "4pi. Con `phi` su 4pi il `+2pi` NON e' un'antifase -- il campo legge "
                 "`exp(i phi)` e l'antiparticella sarebbe IDENTICA alla particella")
def _rn_sch_phi(net, c):
    net.phi = np.concatenate([net.phi, c["anti"]])


@_nascita_regola("schwinger", "i", "topologia: due archi nuovi verso i genitori",
                 "self.i = np.concatenate([self.i, aa, k])",
                 "l'antinodo si allaccia a ENTRAMBI i genitori: `aa-k` e `k-bb`. Nessun "
                 "arco sparisce (non c'e' `keep`): la coppia AGGIUNGE")
def _rn_sch_i(net, c):
    net.i = np.concatenate([net.i, c["aa"], c["k"]])


@_nascita_regola("schwinger", "j", "topologia: due archi nuovi verso i genitori",
                 "self.j = np.concatenate([self.j, k, bb])",
                 "il compagno di `i`")
def _rn_sch_j(net, c):
    net.j = np.concatenate([net.j, c["k"], c["bb"]])


@_nascita_regola("schwinger", "_cs_nodo_prev", "eredita dal genitore `aa`",
                 "self._cs_nodo_prev = np.concatenate([_csp, np.asarray(_csp, float)[src]])",
                 "la stessa regola della divisione, col genitore `aa`: fuori dalla guardia "
                 "sugli spinori, per la stessa ragione")
def _rn_sch_cs_nodo_prev(net, c):
    _rn_div_cs_nodo_prev(net, c)


_nascita_collocata("schwinger", "_deg", "self._grado()",
                   "come nella divisione: una DERIVATA della topologia, collocata dopo il "
                   "blocco perche' legge `i`, `j` e `len(phi)`")


@_nascita_regola("schwinger", "_nb", "eredita dal genitore `aa`",
                 "self._nb = np.vstack([self._nb, self._nb[src]])",
                 "e il suo esito resta la condizione di `_nb_prec`, come nella divisione")
def _rn_sch_nb(net, c):
    _rn_div_nb(net, c)


@_nascita_regola("schwinger", "_nb_prec", "eredita dal genitore `aa`",
                 "self._nb_prec = np.vstack([self._nb_prec, self._nb_prec[src]])",
                 "SOLO SE `_nb` e' stata estesa")
def _rn_sch_nb_prec(net, c):
    _rn_div_nb_prec(net, c)


@_nascita_regola("schwinger", "_nb_ret", "eredita dal genitore `aa`",
                 "self._nb_ret = np.vstack([_nbr_er, _nbr_er[src]])",
                 "il Bloch ritardato del genitore")
def _rn_sch_nb_ret(net, c):
    _rn_div_nb_ret(net, c)


@_nascita_regola("schwinger", "_psi_prec", "eredita dal genitore `aa`",
                 "self._psi_prec = np.concatenate([self._psi_prec, self._psi_prec[src]])",
                 "evita il reset spurio globale in `ritmo()`")
def _rn_sch_psi_prec(net, c):
    _rn_div_psi_prec(net, c)


@_nascita_regola("schwinger", "_psi_spin_prec", "eredita dal genitore `aa`",
                 "self._psi_spin_prec = np.vstack([_pspr, np.asarray(_pspr)[src]])",
                 "lo snapshot del ritmo spinoriale a 4pi")
def _rn_sch_psi_spin_prec(net, c):
    _rn_div_psi_spin_prec(net, c)


@_nascita_regola("schwinger", "_psi_spinor", "eredita INVERTITA (antichirale)",
                 "er = self._psi_spinor[src].copy(); er = -er",
                 "### `segno = -1`: doppia copertura OPPOSTA, coerente con "
                 "`perc_chi = -perc_chi[genitore]`. E' la regola `eredita INVERTITA` del "
                 "piano, e l'unica dove il segno conta")
def _rn_sch_psi_spinor(net, c):
    _rn_div_psi_spinor(net, c)


@_nascita_regola("schwinger", "_spinor_lift", "eredita INVERTITA (antichirale)",
                 "el = self._spinor_lift[src].copy(); el = -el",
                 "la stessa convenzione di segno di `_psi_spinor`")
def _rn_sch_spinor_lift(net, c):
    _rn_div_spinor_lift(net, c)


@_nascita_regola("schwinger", "conc_nodi",
                 "eredita la concorrenza di `aa`, MARCATA `schwinger`",
                 "eredita = [[v[0], v[1], v[2], \"schwinger\"] if len(v) == 3 else v[:] "
                 "for v in eredita]",
                 "se `aa` concorre a una massa, l'antinodo vi concorre pure (categoria "
                 "*creazione di coppie* = accrescimento); se `aa` non concorre a nulla, "
                 "l'antinodo resta senza concorrenza (materia nuova dal vuoto teso). "
                 "### ⚠ E LA FRASE DI PRIMA AFFERMAVA UN TRASFERIMENTO CHE NESSUNO HA "
                 "MISURATO: diceva che <<la Schwinger DRENA tensione di una massa "
                 "esistente>>. ### QUESTA REGOLA NON DRENA NIENTE: copia la lista di "
                 "concorrenza del genitore e le aggiunge una MARCA `schwinger`. Che la "
                 "creazione di coppia dreni la tensione della massa e' una LETTURA "
                 "FISICA PLAUSIBILE, non una misura -- e il bilancio della torsione alla "
                 "nascita e' `DIVISIONE-AUTOCONSISTENTE`, APERTA. Rilievo del guardiano, "
                 "2026-10-03. "
                 "### E qui pure la mutazione diventa SCRITTURA, col `len` crescente "
                 "conservato")
def _rn_sch_conc_nodi(net, c):
    if not net.conc_nodi:
        return
    nuovo = list(net.conc_nodi)
    for gk in c["aa"]:
        eredita = [v[:] for v in nuovo[gk]] if gk < len(nuovo) else []
        eredita = [[v[0], v[1], v[2], "schwinger"] if len(v) == 3 else v[:] for v in eredita]
        nuovo.append(eredita)
    net.conc_nodi = nuovo


@_nascita_regola("schwinger", "eta", "zero",
                 "self.eta = np.concatenate([self.eta, np.zeros(nc)])",
                 "l'antinodo nasce senza `eta`")
def _rn_sch_eta(net, c):
    net.eta = np.concatenate([net.eta, np.zeros(c["nc"])])


@_nascita_regola("schwinger", "mem_mot", "zero",
                 "self.mem_mot = np.vstack([self.mem_mot, np.zeros((nc, 3))]) if len(...) "
                 "else np.zeros((nc, 3))",
                 "### E QUI LA REGOLA E' DIVERSA DALLA MITOSI, ed e' dichiarata: il figlio "
                 "della divisione EREDITA la memoria di moto del padre, l'antinodo nasce "
                 "con memoria NULLA -- non continua un moto, comincia")
def _rn_sch_mem_mot(net, c):
    net.mem_mot = (np.vstack([net.mem_mot, np.zeros((c["nc"], 3))])
                   if len(net.mem_mot) else np.zeros((c["nc"], 3)))


@_nascita_regola("schwinger", "omega_s", "eredita dal genitore `aa`",
                 "self.omega_s = np.vstack([self.omega_s, self.omega_s[src]])",
                 "il ritmo spinoriale del genitore")
def _rn_sch_omega_s(net, c):
    _rn_div_omega_s(net, c)


@_nascita_regola("schwinger", "perc_chi", "eredita INVERTITA (la CARICA si coniuga)",
                 "self.perc_chi = np.concatenate([self.perc_chi, -self.perc_chi[aa]])",
                 "### l'antiparticella nasce con chiralita' OPPOSTA al genitore: "
                 "`-perc_chi[aa]`. ### QUINDI QUESTO SINGOLO NODO SPOSTA `N(+1) - N(-1)` "
                 "DI `-segno(perc_chi[aa])`, non di zero. "
                 "### ⚠ LA CONSERVAZIONE E' DELLA COPPIA, NON DEL RAMO, E LA COPPIA NON "
                 "SI FORMA SEMPRE: la mitosi aggiunge un figlio dello STESSO segno, lo "
                 "Schwinger un antinodo OPPOSTO, e i due si cancellano SOLO sugli archi "
                 "dove scattano ENTRAMBI -- e lo Schwinger scatta su un SOTTOINSIEME "
                 "(`pick`). "
                 "### E I CONTATORI DEL REPO LO DICONO: 72 passi, seme 11 -> "
                 "`_g_nati_mitosi = 9` contro `_g_nati_schwinger = 1`, cioe' "
                 "`N(+1) - N(-1)` si e' spostato di +8 in quel run "
                 "(`csv/_test_fork/_sonda_commit3/_sonda_commit3.json`, `nati_dopo`). "
                 "### ⛔ E LA FRASE DI PRIMA DICEVA <<E' IL RAMO CHE CONSERVA, la coppia "
                 "e' NEUTRA e `N(+1) - N(-1)` NON cambia>>: era VERA DELLA COPPIA e FALSA "
                 "DEL RAMO, e i due contatori esistono proprio per distinguerle. Rilievo "
                 "del guardiano, 2026-10-03.")
def _rn_sch_perc_chi(net, c):
    net.perc_chi = np.concatenate([net.perc_chi, -net.perc_chi[c["aa"]]])


@_nascita_regola("schwinger", "perc_geom", "DERIVATA dalla definizione (non eredita)",
                 "self.perc_geom = np.concatenate([self.perc_geom, "
                 "_derivazione_perc_geom(self, c)])",
                 "[COMMIT 5, decisione di Luca del 2026-09-29] ### LA SCELTA VECCHIA ERA "
                 "DICHIARATA E NON OVVIA -- la CARICA nasce opposta (e' antimateria), la "
                 "GEOMETRIA copiata tale e quale -- e la decisione di Luca la SUPERA ALLA "
                 "RADICE: la geometria non si EREDITA affatto, ne' diritta ne' coniugata, "
                 "perche' si LEGGE dagli archi del nodo (media di `|tw|` contro `PHI_CRIT`, "
                 "la definizione di `chi_basc`). ### Cosi' la domanda *<<si coniuga o no?>>* "
                 "non si pone: non e' una carica, e' una MISURA sugli archi")
def _rn_sch_perc_geom(net, c):
    net.perc_geom = np.concatenate([net.perc_geom, _derivazione_perc_geom(net, c)])


@_nascita_regola("schwinger", "perc_tw", "zero",
                 "self.perc_tw = np.concatenate([self.perc_tw, np.zeros(nc)])",
                 "salto a 0")
def _rn_sch_perc_tw(net, c):
    net.perc_tw = np.concatenate([net.perc_tw, np.zeros(c["nc"])])


@_nascita_regola("schwinger", "phi0", "antifase (come `phi`)",
                 "self.phi0 = np.concatenate([self.phi0, anti])",
                 "la fase di riferimento nasce dove nasce la fase")
def _rn_sch_phi0(net, c):
    net.phi0 = np.concatenate([net.phi0, c["anti"]])


@_nascita_regola("schwinger", "phi_s", "zero",
                 "self.phi_s = np.concatenate([self.phi_s, np.zeros(nc)])",
                 "### E QUI PURE LA REGOLA E' DIVERSA DALLA MITOSI: il figlio della "
                 "divisione EREDITA `phi_s` dal padre, l'antinodo nasce a ZERO -- inerte se "
                 "lo spinore di fase e' spento")
def _rn_sch_phi_s(net, c):
    net.phi_s = np.concatenate([net.phi_s, np.zeros(c["nc"])])


@_nascita_regola("schwinger", "phivel", "media dei genitori",
                 "self.phivel = np.concatenate([self.phivel, 0.5 * (self.phivel[aa] + "
                 "self.phivel[bb])])",
                 "come nella divisione: due addendi, e in IEEE-754 l'addizione di DUE "
                 "addendi e' commutativa al bit")
def _rn_sch_phivel(net, c):
    net.phivel = np.concatenate([net.phivel,
                                 0.5 * (net.phivel[c["aa"]] + net.phivel[c["bb"]])])


@_nascita_regola("schwinger", "pos", "media dei genitori (punto medio)",
                 "self.pos = np.vstack([self.pos, (1-FRAZ_NASCITA) * self.pos[aa] + "
                 "FRAZ_NASCITA * self.pos[bb]])",
                 "l'anti-nodo e' collocato sul punto medio COME il nodo, cosi' i due "
                 "nascono SOVRAPPOSTI e la dinamica (antifase -> repulsione) li separa da "
                 "se'. ### NON si impone alcuna forza: solo la fase opposta")
def _rn_sch_pos(net, c):
    # ### LA FORMA CONVESSA, come nella divisione.
    net.pos = np.vstack([net.pos,
                         (1.0 - FRAZ_NASCITA) * net.pos[c["aa"]] + FRAZ_NASCITA * net.pos[c["bb"]]])


@_nascita_regola("schwinger", "psi", "media dei genitori (come `phi`)",
                 "self.psi = np.concatenate([cur[:n0], 0.5 * (cur[a] + cur[b])])",
                 "[PSI-FLASH] lo STESSO per il canale di Schwinger: i genitori sono "
                 "`aa`/`bb`. ### E IL SEGNO NON SI TOCCA: `psi` e' un campo COMPLESSO, e "
                 "l'antinodo nasce a fase `anti = fm + pi`, cioe' il segno e' GIA' nella "
                 "sua fase")
def _rn_sch_psi(net, c):
    _rn_div_psi(net, c)


@_nascita_regola("schwinger", "psi_spin", "eredita da `aa` (come `phi_s`... che qui e' zero)",
                 "self.psi_spin = np.concatenate([cs[:n0], cs[a]])",
                 "la regola e' la stessa della divisione, e NON segue `phi_s` in questo "
                 "evento: `phi_s` dell'antinodo e' zero, `psi_spin` eredita. ### E' una "
                 "ASIMMETRIA DI OGGI, dichiarata qui invece che nascosta -- il commit 3 "
                 "SPOSTA, non cura")
def _rn_sch_psi_spin(net, c):
    _rn_div_psi_spin(net, c)


@_nascita_regola("schwinger", "rho_spin", "eredita da `aa` (come `psi_spin`)",
                 "self.rho_spin = np.concatenate([np.asarray(rs)[:n0], np.asarray(rs)[a]])",
                 "coerente con `psi_spin`: sono la stessa grandezza vista in due modi")
def _rn_sch_rho_spin(net, c):
    _rn_div_rho_spin(net, c)


@_nascita_regola("schwinger", "_rep", "zero (archi NUOVI)",
                 "self._rep = np.concatenate([self._rep, np.zeros(2 * nc)])",
                 "### E QUI LA REGOLA E' DIVERSA DALLA MITOSI: i due tronconi della "
                 "divisione EREDITANO la memoria dell'arco che si spezza (`[sel], [sel]`); "
                 "gli archi della coppia NASCONO, e nascono senza memoria")
def _rn_sch_rep(net, c):
    net._rep = np.concatenate([net._rep, np.zeros(2 * c["nc"])])


@_nascita_regola("schwinger", "d", "meta' della distanza fra i genitori",
                 "self.d = np.concatenate([self.d, dd])  # `dd` e' GIA' i due blocchi",
                 "`dd` e' ora i DUE BLOCCHI: `max(t*L, 0.05)` per `aa`-`k` e "
                 "`max((1-t)*L, 0.05)` per `k`-`bb`, con `L = norm(pos[aa]-pos[bb])`, per "
                 "`_nasce('schwinger', "
                 "2, 2)`. ### E la lunghezza viene da `pos`, non da `d`: e' la voce `A3` "
                 "della coda. `norm(..., axis=1)` somma TRE componenti in ordine FISSO, "
                 "quindi non dipende dall'ordine")
def _rn_sch_d(net, c):
    # ### UNA VOLTA SOLA: `dd` e' GIA' i due blocchi (`aa`-`k` e `k`-`bb`).
    net.d = np.concatenate([net.d, c["dd"]])


@_nascita_regola("schwinger", "d0", "meta' della distanza fra i genitori",
                 "self.d0 = np.concatenate([self.d0, dd])  # `dd` e' GIA' i due blocchi",
                 "### LO STESSO `dd` di `d`: e' il QUARTO SITO di `_nasce`, `x2` su "
                 "ENTRAMBE le grandezze -- l'arco della coppia nasce A RIPOSO, cioe' "
                 "`d == d0`, e quindi senza stress")
def _rn_sch_d0(net, c):
    # ### UNA VOLTA SOLA, come `_rn_sch_d`.
    net.d0 = np.concatenate([net.d0, c["dd"]])


@_nascita_regola("schwinger", "peq", "`nan` = da calibrare sul PROPRIO arco",
                 "self.peq = np.concatenate([self.peq, np.full(2 * nc, pmed)])",
                 "[PEQ_NASCITA_LOCALE, C2] `nan` significa *da calibrare sulla `rho` del "
                 "PROPRIO arco*, ed e' la STESSA convenzione di `_allaccia`: `step` lo fa "
                 "all'inizio del passo dopo, e da' `anom = 0` ESATTO alla nascita. ### Il "
                 "ramo storico prendeva `median(self.peq)`, una statistica GLOBALE dentro "
                 "una legge locale (`A2`)")
def _rn_sch_peq(net, c):
    net.peq = np.concatenate([net.peq, np.full(2 * c["nc"], c["pmed"])])


@_nascita_regola("schwinger", "_peqn_idx", "la marca degli archi nati con `nan`",
                 "self._peqn_idx = np.arange(len(self.peq) - 2 * nc, len(self.peq))",
                 "### VINCOLO 2 DEL CONTRATTO: gli indici si riferiscono all'array FINALE, "
                 "quindi questa regola DEVE girare DOPO `peq` -- ed e' per questo che "
                 "`_peqn_idx`, che in nessun registro sta, e' DICHIARATO subito dopo `peq` "
                 "in `ORDINE_DI_NASCITA`. Serve a distinguere QUESTI `nan` da quelli di "
                 "`_allaccia`, che la SEMINA scrive su TUTTI gli archi al primo passo")
def _rn_sch_peqn_idx(net, c):
    if PEQ_NASCITA_LOCALE:
        net._peqn_idx = np.arange(len(net.peq) - 2 * c["nc"], len(net.peq))


@_nascita_regola("schwinger", "tw", "zero",
                 "self.tw = np.concatenate([self.tw, zz2, zz2])",
                 "gli archi della coppia nascono senza torsione")
def _rn_sch_tw(net, c):
    zz2 = np.zeros(c["nc"])
    net.tw = np.concatenate([net.tw, zz2, zz2])


@_nascita_regola("schwinger", "twp", "differenza di fase genitore-antinodo",
                 "self.twp = np.concatenate([self.twp, self._wphi(self.phi[aa] - anti), "
                 "self._wphi(anti - self.phi[bb])])",
                 "legge `phi[aa]`/`phi[bb]`, che sono GENITORI: l'estensione di `phi` non "
                 "li tocca, quindi qui l'arco e' INERTE (misurato). Ma l'ordine resta "
                 "quello del registro, che e' lo stesso di prima")
def _rn_sch_twp(net, c):
    net.twp = np.concatenate([net.twp,
                              net._wphi(net.phi[c["aa"]] - c["anti"]),
                              net._wphi(c["anti"] - net.phi[c["bb"]])])


@_nascita_regola("schwinger", "vd", "zero (archi NUOVI)",
                 "self.vd = np.concatenate([self.vd, np.zeros(2 * nc)])",
                 "come `_rep`: nascono fermi, non continuano un moto")
def _rn_sch_vd(net, c):
    net.vd = np.concatenate([net.vd, np.zeros(2 * c["nc"])])


for _nome_smp in ("_smp_d0", "_smp_d"):
    _nascita_collocata("schwinger", _nome_smp,
                       "self._smp_chirurgia(nuovi=dd)  # `dd` e' GIA' i due blocchi",
                       "[SCALA_MIN_PASSO C3] lo snapshot segue anche lo Schwinger, e qui "
                       "SENZA `keep`: la coppia aggiunge archi e non ne toglie")
del _nome_smp


def _nascita_collaudo_della_tabella():
    """### IL PRESIDIO, A SECCO: ogni evento convertito copre TUTTO l'ordine.

    Gira all'import, cosi' una grandezza che manca ferma il processo ### PRIMA che
    un run cominci, invece di farlo cadere a meta'.
    """
    for evento in EVENTI_CONVERTITI:
        mancanti = [n for n in ORDINE_DI_NASCITA if (evento, n) not in REGOLE_NASCITA]
        if mancanti:
            raise RuntimeError(
                "regola di nascita non dichiarata per `%s` all'evento `%s` (e altre %d). "
                "La tabella `REGOLE_NASCITA` deve coprire TUTTO `ORDINE_DI_NASCITA`."
                % (mancanti[0], evento, len(mancanti) - 1))


_nascita_collaudo_della_tabella()


def _forma_di(v):
    """La forma **vera** di una grandezza: `shape` per un array, `(len,)` per una lista."""
    if v is None:
        return None
    f = getattr(v, "shape", None)
    if f is not None:
        return tuple(int(x) for x in f)
    try:
        return (int(len(v)),)
    except Exception:
        return None


def _scrivi_forma(f):
    return "NON ESISTE" if f is None else ("x".join(str(x) for x in f) or "()")


def _ferma_registro(eccezione, come, nome, attesa, vera, dove,
                    atteso_tipo=None, tipo_vero=None):
    """Il messaggio, **in un posto solo**: due copie sarebbero due leggi (`9-ter`)."""
    _nl = chr(10)
    raise eccezione(_nl.join([
        "[REGISTRO %s] IL RUN SI FERMA (`RIPIEGHI-ZERO`, `A9`)." % come,
        "  grandezza . %s" % nome,
        "  forma ..... %s" % _scrivi_forma(vera),
        "  attesa .... %s" % _scrivi_forma(attesa),
        "  tipo ...... %s" % ("(non guardato)" if tipo_vero is None else tipo_vero),
        "  atteso .... %s" % ("(non dichiarato)" if atteso_tipo is None else atteso_tipo),
        "  dove ...... %s" % dove,
        "  PERCHE: il registro dichiara questa grandezza di STATO, cioe con una REGOLA DI",
        "  NASCITA. Se la sua lunghezza non e esattamente il bersaglio, una legge la leggera",
        "  e prendera un valore CHE NESSUNO HA DICHIARATO.",
        "  E SE IL DIFETTO E IL TIPO: un COMPLESSO diventato REALE perde META DELL",
        "  INFORMAZIONE senza cambiare forma, e le sei complex128 del registro sono quelle su cui",
        "  e nato il flash. ⚠ MA per i tre int64 (_deg, perc_chi, perc_geom) la larghezza DIPENDE",
        "  DALLA PIATTAFORMA: se scatta su uno di quei tre, SI AGGIORNA IL REGISTRO, non il codice.",
        "  CHE FARE: cercare CHI l ha estesa, o NON l ha estesa, alla nascita. NON si allunga",
        "  e NON si tronca qui: sarebbe il ripiego che questo controllo esiste per impedire.",
        "  E se in questa configurazione la grandezza NON ESISTE mai, va dichiarata DERIVATA",
        "  nel registro CON IL SUO MOTIVO MISURATO -- non tolta dal controllo in silenzio."]))


def registro_mai_apparse(net):
    """**Le grandezze di STATO del registro che NON si sono MAI viste piene.**

    ### Perche' esiste: CHIUDE IL VARCO della tolleranza *(punto 2 di Luca, 2026-09-29)*
    L'assenza e' tollerata **per grandezza, fino alla sua prima apparizione** -- ed e' necessario,
    perche' `_nb_ret` e' il **Bloch RITARDATO** e al primo passo **non esiste un passato**.
    ### **Ma una tolleranza senza un rendiconto e' un VARCO:** una grandezza che non appare MAI
    resterebbe **fuori dal controllo per sempre, in silenzio**.

    ### -> **Quindi a fine run, e IN OGNI SIGILLO, si ELENCA cio' che non e' mai apparso.**
    Se la lista non e' vuota, ### **non e' una curiosita': e' un ESITO** -- o la grandezza non
    esiste in questa configurazione *(e va dichiarata **DERIVATA** col suo motivo misurato)*, o
    qualcosa non la crea mai *(e allora il registro dice il falso)*.
    """
    apparse = getattr(net, "_g_registro_apparse", None) or set()
    return sorted(nome for nome, _forma, _tipo in REGISTRO_STATO if nome not in apparse)


def _controlla_forma_e_tipo(nome, attesa, v, vera, tipo, dove):
    """**La cascata forma -> tipo, IN UN POSTO SOLO** *(`9-ter`: due copie sarebbero due leggi)*.

    La chiamano **due** cicli -- le grandezze di **STATO** e quelle **A FINESTRA** -- e il motivo
    per cui e' una funzione e non un blocco ripetuto e' che ### **la seconda tabella non deve
    aggiungere una legge**: aggiunge una **dichiarazione**.

    ### L'ORDINE NON E' DECORATIVO: prima la FORMA, e il TIPO solo se la forma e' giusta
    Se la forma e' sbagliata ### **il difetto e' quello**, e due errori insieme non aiutano chi
    legge.

    ### ⚠ IL BUCO DEL TIPO, CURATO IL 2026-09-29 (rilievo del guardiano)
    Prima la condizione era `if suo is not None and str(suo) != tipo`, e quel `is not None` era
    ### **UNA SECONDA ESENZIONE IMPLICITA** -- mentre il registro ne dichiara **UNA SOLA**
    (`conc_nodi`). E' la stessa famiglia dei ripieghi chiusi da `RIPIEGHI-ZERO`: ### **una
    condizione di ESISTENZA che copre un difetto.**
    **MISURATO PRIMA DELLA CURA:** una grandezza tipata trasformata in **LISTA** con la forma
    giusta veniva ### **SALTATA IN SILENZIO** -- `psi` *(una delle sei complesse)* ed `eta`. Le
    grandezze a **due** assi erano gia' prese da `FormaSbagliata`, perche' una lista perde il
    secondo asse: ### **il buco viveva SOLO su quelle a un asse.**
    """
    if vera != attesa:
        if vera[0] < attesa[0]:
            _ferma_registro(CacheCorta, "CORTA", nome, attesa, vera, dove)
        if vera[0] > attesa[0]:
            _ferma_registro(CacheLunga, "LUNGA", nome, attesa, vera, dove)
        # ### IL PRIMO ASSE E' GIUSTO E UN ALTRO NO: non e' ne' corta ne' lunga, e' UN ALTRA
        #   GRANDEZZA. E' il limite <<un solo asse>> che avevo dichiarato, e che ora non c e piu.
        _ferma_registro(FormaSbagliata, "FORMA", nome, attesa, vera, dove)
    if tipo is None:
        return
    suo = getattr(v, "dtype", None)
    if suo is None:
        _ferma_registro(TipoSbagliato, "TIPO", nome, attesa, vera, dove, atteso_tipo=tipo,
                        tipo_vero="(nessun dtype: %s)" % type(v).__name__)
    if str(suo) != tipo:
        _ferma_registro(TipoSbagliato, "TIPO", nome, attesa, vera, dove, atteso_tipo=tipo,
                        tipo_vero=str(suo))


def _finestra_aperta(voce, apre, chiude, comp):
    """**La finestra e' APERTA da `apre` (compresa) a `chiude` (esclusa)** -- nella composizione
    IN USO, non in quella canonica.

    ### Perche' si DERIVA dalla composizione invece di elencare le voci
    `H-ETC-2` **permuta** l'ordine delle voci, e un elenco scritto a mano
    *(<<aperta dopo `step`, dopo `mitosi`, ...>>)* ### **direbbe il falso appena l'ordine cambia.**
    Due cose rendono la derivazione sicura, e sono **imposte da `valida_composizione`**:
    `apri` e' **sempre la prima** voce, e la **coda** e' sempre `('chiudi', 'verifica_invarianti')`
    -- ### **quindi `chiudi` esiste SEMPRE e viene SEMPRE dopo `apri`.**

    `voce is None` e' ### **la PRECONDIZIONE**: il passo non e' ancora cominciato, e la finestra
    del passo PRECEDENTE deve essere ### **gia' chiusa.** *(E' il caso che `_smp_chiudi` teme nel
    suo commento: <<il passo dopo leggerebbe quella del passo prima>>.)*
    """
    if voce is None:
        return False
    c = list(comp) if comp else list(PASSO_COMPOSIZIONE)
    if apre not in c or chiude not in c or voce not in c:
        return False
    return c.index(apre) <= c.index(voce) < c.index(chiude)


def _ferma_se_registro_incoerente(net, dove, voce=None, comp=None):
    """**UN SOLO controllo, nello schedulatore, invece di quaranta `raise` sparsi.**

    ### Perche' UNICO, ed e' MISURATO (prova a guasto del 2026-09-28)
    Una guardia **dentro** una legge arriva **troppo tardi**, o viene **aggirata**:

    | | |
    |---|---|
    | `:4462`, la guardia su `psi_spin` | **ESEGUE e non spara**, perche' `calcola_psi` ha gia'
      riscritto `psi_spin` a piena lunghezza: ### **sta A VALLE della riscrittura** |
    | `_estendi_psi_spinor` | **allunga la coda** con una riga **inventata**, quindi ogni guardia
      a valle trova un array **giusto**: ### **un estensore a monte la DISARMA** |

    ### -> **Curare sito per sito aveva lasciato 29 grandezze su 31 scoperte.**

    **I due punti** sono quelli decisi da Luca: l'`apri` *(precondizione, prima del ciclo)* e
    **subito dopo `mitosi`**, che e' **il solo posto del passo in cui `n` cresce**.

    ### ASSENTE non e' DI LUNGHEZZA SBAGLIATA
    E' la distinzione che Luca ha imposto in `lambda_nodi`: prima che il **primo passo** sia
    finito una cache pigra puo' non esistere, e ### **si CONTA** (`A8`); ### **dopo, l'assenza
    e' un ERRORE** -- senno' diventa un ripiego silenzioso nuovo.

    ### E <<ASSENTE>> COMPRENDE <<ESISTE MA E' VUOTA>>, ed e' MISURATO
    La prima stesura guardava solo `is None`, e ### **si e' fermata all `apri` del PRIMO passo**
    su `_psi_spinor`: `Rete.__init__` crea diverse cache come **`np.zeros(0)`**, quindi non sono
    `None` e non sono <<di lunghezza sbagliata>> -- sono ### **non ancora inizializzate**.
    *(E' il <<non so>> n.3 del piano, in una forma che non avevo previsto: l ho visto girando,
    non leggendo.)*

    ### E LA TOLLERANZA E' PER GRANDEZZA, non <<prima del primo passo>>: MISURATO
    La regola di Luca diceva *<<assenza tollerata SOLO prima del primo passo completato>>*, e
    ### **ferma un run sano all apri del passo 2** su **`_nb_ret`**. La misura, sulla scena
    piccola a seme 11, dice quando ognuna diventa piena per la prima volta:

    | dall apri del passo | quante |
    |---|---|
    | **0** *(subito dopo la semina)* | **18** |
    | **1** | **11** |
    | ### **2** | ### **1: `_nb_ret`** |
    | mai, in 12 passi | **0** |

    ### **E la ragione di `_nb_ret` e' FISICA, non pigrizia: e' il Bloch RITARDATO** (`FORK_SU2_MEM`,
    `n(t-tau)`), ### **e al primo passo NON ESISTE UN PASSATO.**

    ### -> **Allora la tolleranza e' PER GRANDEZZA, fino alla sua PRIMA APPARIZIONE**, e non
    contiene alcun numero scelto (`A1`): l assenza **si CONTA** finche' la grandezza non si e'
    ancora mai vista piena; ### **dopo, se SPARISCE, e un ERRORE** -- ed e' il caso che la regola
    di Luca vuole impedire. *(La forma <<tollera fino al passo 2>> sarebbe stata una MANOPOLA.)*
    """
    if not CONTROLLO_REGISTRO:
        net._g_registro_spento = getattr(net, "_g_registro_spento", 0) + 1
        return
    n = int(net.n)
    m = int(len(net.i))
    apparse = net.__dict__.setdefault("_g_registro_apparse", set())
    for nome, forma, tipo in REGISTRO_STATO:
        # LA FORMA ATTESA, con il primo asse risolto: ("n", 3) -> (n, 3).
        attesa = ((n if forma[0] == "n" else m),) + tuple(forma[1:])
        v = getattr(net, nome, None)
        vera = _forma_di(v)
        # <<ASSENTE>> = non esiste OPPURE esiste VUOTA (`np.zeros(0)` di `Rete.__init__`).
        if (vera is None or vera[0] <= 0) and attesa[0] > 0:
            if nome not in apparse:
                net._g_registro_assenti = getattr(net, "_g_registro_assenti", 0) + 1
                continue
            # ### GIA VISTA PIENA E ORA NON C E PIU: e' una SPARIZIONE, ed e' un difetto.
            _ferma_registro(CacheCorta, "SPARITA", nome, attesa, vera, dove)
        if vera == attesa:
            _controlla_forma_e_tipo(nome, attesa, v, vera, tipo, dove)
            apparse.add(nome)
            continue
        _controlla_forma_e_tipo(nome, attesa, v, vera, tipo, dove)
    # ### LE GRANDEZZE A FINESTRA: fuori dalla finestra DEVONO NON ESSERCI (commit 1, 2026-10-01).
    #   ⚠ IL VERSO DURO E' QUESTO, ed e' il difetto che `_smp_chiudi` TEME nel suo commento:
    #     <<la fotografia si CHIUDE sempre, senno' resterebbe aperta e il passo dopo leggerebbe
    #     quella del passo prima>>. Era un timore in un commento; ora e' un presidio (`A9`).
    #   ⚠ IL VERSO MOLLE SI CONTA E NON FERMA (`A8`): `_smp_apri` fotografa SOLO se
    #     `SCALA_MIN_PASSO or COES_CAUSALE`, quindi a flag spenti la finestra NON SI APRE MAI e
    #     non e' un difetto -- ma <<non si e' aperta>> deve essere LEGGIBILE, non supposto.
    for nome, forma, tipo, apre, chiude, _perche in REGISTRO_FINESTRA:
        attesa = ((n if forma[0] == "n" else m),) + tuple(forma[1:])
        v = getattr(net, nome, None)
        vera = _forma_di(v)
        dentro = _finestra_aperta(voce, apre, chiude, comp)
        if vera is None or vera[0] <= 0:
            if dentro:
                net._g_finestra_chiusa_dentro = getattr(net, "_g_finestra_chiusa_dentro", 0) + 1
            continue
        if not dentro:
            _nl = chr(10)
            raise FinestraRestataAperta(_nl.join([
                "[REGISTRO FINESTRA APERTA] IL RUN SI FERMA (`RIPIEGHI-ZERO`).",
                "  grandezza . %s" % nome,
                "  forma ..... %s" % _scrivi_forma(vera),
                "  la apre ... la voce `%s`" % apre,
                "  la chiude . la voce `%s`" % chiude,
                "  dove ...... %s" % dove,
                "  PERCHE: questa grandezza vive SOLO DENTRO il passo, e qui il passo e FUORI",
                "  dalla sua finestra -- quindi NON DOVREBBE ESISTERE. Se esiste, la finestra",
                "  non si e chiusa, e LA LEGGE DEL PASSO DOPO LEGGEREBBE LA FOTOGRAFIA DEL",
                "  PASSO PRIMA: un valore vecchio preso per nuovo, che e il ripiego silenzioso",
                "  che `RIPIEGHI-ZERO` esiste per impedire.",
                "  CHE FARE: cercare CHI non ha chiuso -- il ritorno anticipato di una legge e",
                "  il primo sospetto. NON si azzera qui: azzerare sarebbe il ripiego.",
                "  MOTIVO DICHIARATO NEL REGISTRO: %s" % _perche]))
        _controlla_forma_e_tipo(nome, attesa, v, vera, tipo, dove)
    # ### 3-bis: LE GRANDEZZE NON DICHIARATE. Non si parte da un elenco: si parte da CIO' CHE LA
    #   RETE HA, cosi' la regola vale CON QUALUNQUE FLAG. E il criterio e' LA FORMA, non il nome.
    for nome, v in list(vars(net).items()):
        if nome in REGISTRO_NOMI:
            continue
        if not isinstance(v, (np.ndarray, list)):
            continue
        f = _forma_di(v)
        if f is None or not f:
            continue
        if f[0] != n and f[0] != m:
            continue
        # ⚠ `n == m` renderebbe i due metri indistinguibili: si dice QUALE si e' riconosciuto, e
        #   se coincidono si dice ANCHE QUESTO invece di sceglierne uno.
        _quale = ("n E m (INDISTINGUIBILI: n == m == %d)" % n if n == m
                  else ("n = %d" % n if f[0] == n else "m = %d" % m))
        _nl = chr(10)
        raise GrandezzaNonDichiarata(_nl.join([
            "[REGISTRO NON DICHIARATA] IL RUN SI FERMA (`RIPIEGHI-ZERO` 3-bis).",
            "  grandezza . %s" % nome,
            "  forma ..... %s" % _scrivi_forma(f),
            "  primo asse  %s" % _quale,
            "  tipo ...... %s" % str(getattr(v, "dtype", type(v).__name__)),
            "  dove ...... %s" % dove,
            "  PERCHE: la rete HA una grandezza per nodo o per arco che IL REGISTRO NON DICHIARA.",
            "  Il controllo non parte da un elenco: parte da CIO CHE LA RETE HA, cosi vale con",
            "  QUALUNQUE FLAG -- e un flag che crea una grandezza nuova la fa COMPARIRE qui.",
            "  CHE FARE: o la grandezza ENTRA NEL REGISTRO (forma, tipo, e se e di STATO la sua",
            "  regola di nascita), o si DICHIARA DERIVATA CON IL SUO MOTIVO MISURATO.",
            "  MAI togliere il nome dal controllo in silenzio."]))
    net._g_registro_controlli = getattr(net, "_g_registro_controlli", 0) + 1


def _ferma_se_oltre_max_nodi(n_attuale, quanti, dove):
    """**UN SOLO controllo per `MAX_NODI`, e non tronca MAI.**

    E' **una** funzione e non tre `raise` copiati, perche' tre copie sarebbero **tre leggi**
    e `9-ter` dice di non moltiplicarle: *a parita' di effetto si preferisce togliere
    un'eccezione*.

    `dove` non e' decorativo: **dice QUALE dei quattro punti ha fermato il run**, e senza di
    esso l'errore non si distingue da un altro.
    """
    if n_attuale + quanti <= MAX_NODI:
        return
    raise LimiteNodiSuperato(
        "[MAX_NODI] IL RUN SI FERMA, e non si tronca (`MAX-NODI-FERMA`, `A8`).\n"
        "  dove ...... %s\n"
        "  nodi ora .. %d\n"
        "  richiesti . %d  ->  totale %d\n"
        "  MAX_NODI .. %d  (superato di %d)\n"
        "  CHE FARE: la misura si RIFA' CON PIU' MEMORIA (`--maxnodi`), NON si tronca.\n"
        "  Troncare cambierebbe la FISICA in silenzio: meno nascite, meno semina, il canale\n"
        "  di Schwinger spento -- e nessuno lo saprebbe dai dati."
        % (dove, n_attuale, quanti, n_attuale + quanti, MAX_NODI,
           n_attuale + quanti - MAX_NODI))


def valida_composizione(comp):
    """**Il passo e' una TRANSAZIONE: la sua struttura non e' negoziabile.**

    Le quattro regole, e ognuna dice **che cosa romperebbe**:

    1. **`apri` e' il PRIMO.** Se non lo fosse, una legge girerebbe **prima** che la
       fotografia esista, e leggerebbe uno stato di cui nessuno ha preso nota.
    2. **`chiudi` e `verifica_invarianti` sono gli ULTIMI, in quest'ordine.** Se `chiudi`
       stesse in mezzo, il freno di scala minima girerebbe su una variazione PARZIALE
       e le leggi dopo scriverebbero **fuori transazione**. Se il controllo venisse
       prima del commit, guarderebbe `d0` **non ancora frenata** -- ed e' esattamente il
       timore dichiarato in `(c)1`, che `T1` ha evitato tenendoli **insieme**.
    3. **Ogni nome sta nel registro.** Un nome fuori registro solleverebbe a meta' passo.
    4. **Nessun duplicato.** Una legge due volte nello stesso passo e' due volte la stessa
       variazione: non e' una composizione, e' un errore di scrittura.

    ⚠ **SOLLEVA, non avvisa.** Una composizione non valida non e' una
    configurazione insolita da segnalare: e' un passo che non e' un passo. E questo **non e'
    un presidio di `git`** -- e' un controllo **a runtime**, che vive nel codice e che nessun
    commit puo' aggirare.
    """
    comp = tuple(comp)
    # ⚠ OGNI VOCE DEL REGISTRO DEVE AVERE UN TIPO (`T2b`): se il registro e i tipi
    #   divergono, la composizione sarebbe validata su un registro che il resto del
    #   codice non conosce. E' un controllo sul CODICE, non sull'ingresso, e quindi
    #   sta qui una volta sola invece che in un presidio di `git`.
    _senza = sorted(_PASSO_REGISTRO - set(_PASSO_TIPI))
    if _senza:
        raise ComposizioneNonValida(
            'voci del registro SENZA TIPO: %s -- `_PASSO_TIPI` e `_PASSO_REGISTRO` '
            'sono divergenti' % _senza)
    if not comp:
        raise ComposizioneNonValida('la composizione del passo e\' VUOTA')
    fuori = [x for x in comp if x not in _PASSO_REGISTRO]
    if fuori:
        raise ComposizioneNonValida(
            'voci NON nel registro: %s -- il registro e\' %s'
            % (fuori, sorted(_PASSO_REGISTRO)))
    doppie = sorted({x for x in comp if comp.count(x) > 1})
    if doppie:
        raise ComposizioneNonValida(
            'voci DUPLICATE: %s -- una legge due volte nello stesso passo e\' due '
            'volte la stessa variazione' % doppie)
    if comp[0] != 'apri':
        raise ComposizioneNonValida(
            'la composizione NON comincia con `apri` ma con `%s`: una legge girerebbe '
            'prima che la fotografia esista' % comp[0])
    if comp[-len(_PASSO_CODA):] != _PASSO_CODA:
        raise ComposizioneNonValida(
            'la CODA deve essere %s e invece e\' %s: se `chiudi` non e\' penultimo il '
            'freno gira su una variazione PARZIALE, e se il controllo precede il commit '
            'guarda `d0` non ancora frenata'
            % (list(_PASSO_CODA), list(comp[-len(_PASSO_CODA):])))
    return comp

def esegui_passo(net, composizione=None):
    """L'UNICO modo di avanzare di un passo. Esegue `PASSO_COMPOSIZIONE` in ordine.

    `composizione` serve agli INNESTI (`T5`) e al presidio `H-ETC-2`, che permuta
    l'ordine: di default e' la composizione standard, e chi la cambia LO DICHIARA
    (contatore `_g_passi_composizione_altra`).

    ⚠ NON CONTIENE FISICA. Se un giorno ci finisse un `if` su un flag, la composizione
    smetterebbe di essere un DATO e tornerebbe a essere codice.
    """
    # ⚠ SI VALIDA PRIMA DI ESEGUIRE, e prima di toccare `net`: una composizione rotta
    #   deve fallire **con il passo ancora da cominciare**, non a meta'.
    comp = valida_composizione(PASSO_COMPOSIZIONE if composizione is None
                             else composizione)
    # [MAX-NODI-FERMA, 2026-09-28] IL CONTROLLO DELLO SCHEDULATORE, e sta all'INIZIO perche' e'
    #   una PRECONDIZIONE: <<questo passo si puo' fare>>. Un passo che non si puo' fare NON
    #   COMINCIA. Alla fine sarebbe una constatazione, e lo stato sarebbe gia' oltre il limite.
    #   ⚠ IL LIMITE, DICHIARATO E **NON MISURATO**: `mitosi` crea nodi DENTRO il passo, quindi un
    #   passo che sfora FINISCE e l'errore arriva al passo DOPO. **QUANTO** sia lo sforo massimo
    #   NON LO SO, e non e' misurato: sulla scena dei sigilli `(ii)(a)` (n = 2107, seme 11)
    #   MISURATI 40 PASSI CON ZERO NASCITE, quindi `n` non cresce e lo sforo non si osserva. Per
    #   misurarlo serve una scena CHE CRESCE, cioe' un run lungo -- ed e' una misura a se'.
    #   *(Il commento precedente diceva <<dichiarato e MISURATO ... riportato dal sigillo>>: era
    #   FALSO quando l'ho scritto, e questa e' la correzione. Vedi `MAX-NODI-FERMA`.)*
    _ferma_se_oltre_max_nodi(net.n, 0, 'schedulatore: inizio del passo')
    # [RIPIEGHI-ZERO, 2026-09-29] LA PRECONDIZIONE, e sta QUI e non dentro `_smp_apri` per una
    #   ragione precisa: una precondizione NON DEVE MUOVERSI CON UNA VOCE. `H-ETC-2` PERMUTA la
    #   composizione, e un controllo dentro la fase `apri` si sposterebbe con lei -- mentre <<il
    #   passo comincia con le forme giuste>> vale in QUALUNQUE ordine.
    _ferma_se_registro_incoerente(net, 'schedulatore: prima delle leggi')
    for _nome in comp:
        if _nome in _PASSO_FASI:
            getattr(net, _PASSO_FASI[_nome])()
        elif _nome in _PASSO_MODULO:
            globals()[_nome](net)
        elif _nome == 'verifica_invarianti':
            net.verifica_invarianti(dove='esegui_passo')
        else:
            getattr(net, _nome)()
        # [RIPIEGHI-ZERO, generalizzazione 2 del 2026-09-29, decisione di Luca]
        #   IL CONTROLLO DOPO **OGNI** VOCE, non piu' solo dopo `mitosi`.
        #   ⚠ PERCHE': con due soli punti restava un limite che avevo DICHIARATO -- `calcola_psi`
        #     riscrive `psi_spin` e `_estendi_psi_spinor` allunga `_psi_spinor` **a META' PASSO**,
        #     e una grandezza che andasse fuori forma FRA i due punti NON VENIVA VISTA.
        #   ⚠ E COSTA POCO, ed e' la ragione per cui si puo' fare: ~30 confronti di forma per voce.
        #   ### E TOGLIE UN `if` SUL NOME DI UNA VOCE: lo schedulatore non cabla piu' `'mitosi'`,
        #     quindi la composizione resta un DATO anche piu' di prima.
        #   ⚠ `voce` e `comp` NON sono decorativi e NON si ricavano dalla stringa `dove`: la
        #     finestra si DERIVA dalla composizione IN USO, e un controllo che leggesse il NOME
        #     dentro una frase sarebbe una regola che parte dalla SINTASSI -- l errore che in
        #     questa sessione ho fatto SEI volte. Qui la voce passa come DATO.
        _ferma_se_registro_incoerente(net, 'schedulatore: dopo la voce `%s`' % _nome,
                                      voce=_nome, comp=comp)
    net._g_passi_eseguiti = getattr(net, '_g_passi_eseguiti', 0) + 1
    if comp != tuple(PASSO_COMPOSIZIONE):
        net._g_passi_composizione_altra = getattr(net, '_g_passi_composizione_altra', 0) + 1
    return net

# ============================================================================
MU_PSI   = -0.05
REPULS_LEGGE = True      # repulsione EMERGENTE con conversione dinamica (riempimento*coerenza vs Ncrit adattivo): legge, non parametro        # AUTO-INTERAZIONE repulsiva ATTIVA (default B): pressione
                        # interna dall'Hamiltoniana. Espande R90 conservando l'olonomia.          # AUTO-INTERAZIONE DELL'INTERFERENZA (opzione, spenta).
                        # <0 = repulsiva (pressione interna), derivata da d|Psi|^2/dphi.
                        # NON e' una forza scelta: e' il gradiente di |Psi|^2, l'unica
                        # forma coerente. Candidata alla faccia repulsiva del modello.
L_CONSERVA = False      # ⚠⚠ NO-OP ACCETTATO DAL 2026-09-28: il suo ramo e' ARCHIVIATO.
                        # Era marcato <<ERRATA, NON usare>>: doveva rimuovere la rotazione spuria del
                        # rilassamento, ma AZZERAVA tutta la rotazione rigida a ogni passo -> distruggeva
                        # la PRECESSIONE FISICA REALE (L_z~-0.9, verso coerente all'84%). Conservare L
                        # != annullare la rotazione, e la fisica fondamentale conserva gia' L da sola.
                        # `_togli_rotazione_rigida` e il ramo che lo chiamava sono in
                        # `csv/_archivio/_l_conserva.py` (tag `pre-archivio-lconserva`).
                        # ⚠ IL RAMO AGIVA: 17 grandezze su 23 differivano ad accenderlo -- non e' una
                        # pulizia, e' una decisione (Luca, strada (b)).
                        # ⚠ E FACEVA DICHIARARE IL FALSO AL TIPO di `rilassa_disegno`: la catena
                        # `rilassa_disegno -> _togli_rotazione_rigida -> calcola_psi` le faceva scrivere
                        # `psi`, mentre il tipo `disegno` dice <<scrive solo pos>>. Ora e' vero per
                        # COSTRUZIONE. NON E' STATO TOLTO (decisione 3) e si DICHIARA all'avvio.
                        # NB: non ha nemmeno un flag CLI -- per accenderlo si modifica il sorgente.
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
PLAST_DIN = False       # PLASTICITA' METRICA DINAMICA (legge, non parametro). Se True sostituisce
                        # PLAST_MIT statico: l'offset plastico sul d0 dei nuovi archi emerge dallo
                        # stress metrico dell'arco |d-d0|/d0 e dall'ECCESSO di torsione
                        # (|tw|/PHI_CRIT - 1), saturato via tanh e non-negativo. Genera volume solo
                        # dove il reticolo e' sotto forte tensione. Locale (grandezze dell'arco),
                        # nessuna coordinata, nessun parametro libero. Default off = non-regressione.
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
MITOSI_DIR = 0.0        # ⚠ VALE ZERO, QUINDI IL RAMO NON GIRA MAI -- e il commento diceva
                        # l'opposto: <<MITOSI DIREZIONALE ATTIVA>>. E' `CENS-A4`, e sono DUE
                        # difetti e non uno: un ramo morto, E un commento che dice il contrario.
                        # [COMMIT 0 del riordino della mitosi, 2026-10-01, decisione di Luca:
                        #  `MITOSI_DIR` SI ARCHIVIA. Questo commit corregge SOLO il commento,
                        #  ed e' BYTE-INERTE: il valore non si tocca, il ramo resta dov'e'.]
                        #
                        # L'IDEA che il ramo esprimeva: il figlio nasce DECENTRATO verso il
                        # gradiente di torsione, cioe' verso l'estremo piu' avvolto, e cosi' la
                        # replicazione si polarizza e il baricentro trasla lungo la geodetica.
                        # ### L'IDEA E' GIUSTA E NON SI BUTTA: e' il PRIMO TENTATIVO della voce
                        #     `FRAZIONE-DIVISIONE` (aperta il 2026-10-01), dove la posizione del
                        #     figlio diventa `t = f(stato_a, stato_b)` con `f(a,b) = 1 - f(b,a)`.
                        # ### LA FORMA NO, e per questo si archivia: a :6981 il ramo fa
                        #     `bias = 0.5 * np.tanh(MITOSI_DIR * (twn[a] - twn[b]))`, cioe' TRE
                        #     NUMERI A MANO -- il coefficiente `MITOSI_DIR`, la `tanh` scelta, e
                        #     lo `0.5` davanti. `A1` dice la legge, non il numero.
                        # IL SEGUITO STA IN doc/PIANO_riordino_mitosi.md (voce FRAZIONE-DIVISIONE):
                        # il primo passo NON e' scegliere `t`, e' MISURARE se la posizione del
                        # figlio sia FISICA o solo DISEGNO -- quali leggi leggono `pos` e quali
                        # solo `d`.
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
PAV_COM  = False        # ⚠⚠ `PAV_COM` E' INERTE DAL 2026-09-27: il default non conta piu'.
# Rendeva COMOVENTE il pavimento di `d0` (`f*median(d0)` invece del muro assoluto `0.05`), ma
# quel pavimento -- `_floor_d0` e `_pav_d0` -- E' STATO ARCHIVIATO in
# `csv/_archivio/_pavimenti_morti.py` (tag `pre-archivio-pavimenti`), perche' col driver non
# eseguiva mai: `_g_sm_pav_saltati = 15` su 15 chiamate, e la riga del pavimento 0 esecuzioni.
# `PAV_COM` NON E' STATO TOLTO (decisione 3 di Luca: si conserva tutto) e il driver lo
# passa ancora, ma DA OGGI NON FA NIENTE. La garanzia sulle lunghezze e' `LAM`.
LS_AZIM = False         # L·S VETTORIALE (legge): se True, il verso tangenziale della
# viriale viene dalla componente azimutale di (radiale x spinore _nb), non da circ_arc oscillante.
# Il gradiente radiale incrociato con l'asse dello spinore (che non batte) da' un verso azimutale
# STABILE = precessione. L'asse e' lo spinore (stato), non un parametro. Default off.
OLON_PART = False       # OLONOMIA NELLA PARTIZIONE (legge): se True, la quota tangenziale
# della viriale combina il curl |circ_arc| E il twist coerente accumulato |twn_a| (hypot), cosi'
# il verso coerente (polo maturo) comanda QUANTO radiale diventa tangenziale e il freno, non solo
# la direzione. Chiude il buco: coerenza -> curl basso -> poca conversione. Default off.
POLO_MATURO = False     # POLO MATURO (legge, strategia 3): al twist_dip partecipa la
# chiralita' del POLO che matura (nodo con torsione locale maggiore), non la differenza dei due
# poli. Rompe il bilanciamento dei +-pi (olonomia netta acquista verso). Mantiene SU(2). Default off.
VERSO_CHI = False       # AGGANCIO AL VERSO STABILE (legge): se True, FRAME_DRAG e'
# pilotato dalla circolazione del solo twist_dip CHIRALE (segno fisso, gradiente vecchio/nuovo)
# invece che dal tw pieno (dominato da dph oscillante -> il verso si inverte). Aggancia l'orbita
# al verso che NON batte. Default off = comportamento attuale (FRAME_DRAG su tw pieno).
SYNC_UPDATE = False     # ⚠⚠ `SYNC_UPDATE` E' UN NO-OP ACCETTATO DAL 2026-09-27.
# Prometteva l'aggiornamento sincrono (Jacobi invece di Gauss-Seidel), MA IL SUO RAGGIO ERA UNA
# LEGGE SU CINQUE: misurato nella FASE 0 di `ETC-PASSO`, 7 usi in `_passo_spinoriale`, 6 in `step`,
# e ZERO in `scuoti_vuoto`, `mitosi`, `rilassa_disegno`, `memoria_hebbiana_moto`. Tutte e 56 le
# letture miste t/t+1 misurate stavano FUORI dal suo raggio.
# I suoi rami sono ARCHIVIATI in `csv/_archivio/_sync_update.py` (tag `pre-archivio-sync`), e la
# sincronia del passo INTERO la fa la cura `ETC-PASSO`.
# IL FLAG NON E' STATO TOLTO (decisione 3 di Luca: si conserva tutto): `--sync` si accetta, non
# fallisce, e DICHIARA a voce di non fare niente. Il default non conta piu': e' inerte in entrambi
# gli stati.
ZETA_VIR = False        # FRENO ANISOTROPO (legge, zero parametri): se True, lo smorzamento
# metrico beta viene moltiplicato per cos2 (la quota RADIALE della viriale): pieno sul moto
# radiale (cos2=1), scende a zero sul tangenziale (sin2=1). Non toglie il freno ovunque nella
# materia (come zeta-loc, cieco alla direzione), ma SOLO lungo il verso in cui la viriale
# converte in tangenziale. Freno anisotropo = valvola: dissipa il radiale, lascia vivere la
# rotazione -> puo' SELEZIONARE un verso (dissipa tutto tranne il tangenziale) invece che solo
# preservarlo. Usa la stessa sin2/cos2 che la viriale gia' calcola (geometrico, zero parametri).
# Senza --viriale, sin2=0 ovunque -> beta invariato (nessun effetto). Default off = non-regressione.
VERLET = False          # INTEGRATORE METRICO SPERIMENTALE: se True, il sottociclo d/vd usa
# Velocity-Verlet al secondo ordine invece di Eulero esplicito. Default off per mantenere
# invariato il comportamento canonico; attivare con --verlet per il confronto A/B.
ELAST_C = 100.0         # COEFFICIENTE DEL NUCLEO ELASTICO: default storico, esposto solo per
# esperimenti di ridondanza/sensibilita'. ELAST_C=0 disattiva il rinforzo elastico di d0.
# >>> INUTILIZZATO dal 2026-09-17 (bonifica della plasticita'). NON E' STATO CANCELLATO DI
# PROPOSITO: e' EVIDENZA. Il suo unico uso era `fattore_elasticita` in `step` (riga ~3244 del blob
# 827d3bf8), sostituito dalla forma viscoelastica causale `max(t_luce, t_luce*rho_arco/peq)`.
# Restava un NUMERO SCELTO ("default storico", A1) dentro un rapporto fra popolazioni diverse (A3):
# con ELAST_C = 100 il fattore aveva mediana ~8.8e5, cioe' la plasticita' era CONGELATA.
# Il codice di una legge esclusa non si cancella mai (CLAUDE.md par.9): resta qui a spiegare
# PERCHE' esiste il suo sostituto. Vedi doc/COMPONENTI_PROMOSSE.md e doc/REFERTO_gate_bonifica.md.
GUSCIO_MORBIDO = False   # DIFFUSIONE DI SUPERFICIE delle d0 (legge, zero parametri): se True, aggiunge
# al rilassamento plastico un termine diffusivo D*lap(d0) con D = c_locale * spaziatura d'arco. Il
# laplaciano e' ~0 nel nucleo uniforme e grande al bordo ripido -> smussa SOLO il guscio (tensione
# superficiale), non tocca la rigidita' del core. Clamp causale (CFL). Default off = non-regressione.
GRAV_AMPIEZZA = False   # L'AMPIEZZA NELLA CORREZIONE GRAVITAZIONALE (2026-09-19). OFF = byte-identico.
                        # Se True, `cross(_nb_grav(), nb)` viene moltiplicato per `_rho_sorgente()`,
                        # l'ampiezza che `_nb_grav()` divide via. UNA DIREZIONE NON E' UNA FORZA:
                        # |_nb_grav| = 1.000000 ovunque, e l'ampiezza del campo NON entra nel
                        # numeratore -- mentre `rho_spin` sta al DENOMINATORE dentro l'inerzia.
                        # Verificato dal disco: `_pesi()` non contiene rho, e gli altri fattori
                        # sono tutti versori. Nessun numero nuovo, nessun tetto, nessun clamp.
COPPIA_RECIPROCA = False  # RECIPROCITA' DELLA COPPIA SPINORIALE (2026-09-19). OFF = byte-identico.
                        # Se True, il torque `cross(_nb_grav(), nb)` viene pesato per `ramp[k]`,
                        # LO STESSO peso che il nodo ha come SORGENTE. Cura un'ASIMMETRIA MISURATA:
                        # un neonato ha peso ESATTAMENTE zero negli archi (A7b) ma riceve una coppia
                        # di 0.3809, cioe' 4.9 VOLTE la mediana dei maturi, perche' `_nb_grav()`
                        # divide per `rho_spin` ed e' un VERSORE: l'ampiezza del campo non entra.
                        # Nessun numero nuovo, nessuna soglia: e' `ramp`, gia' la legge del peso.
CHI_BASC = False        # BASCULAMENTO CHIRALE (legge, zero parametri): se True, la chiralita'
# di ogni nodo NON resta piu' fissa dalla nascita, ma vira secondo la TORSIONE LOCALE rispetto
# al QUANTO DI OLONOMIA (PHI_CRIT = 2pi): chi=+1 dove la torsione ha COMPLETATO il giro (materia
# matura), chi=-1 dove non l'ha completato (spazio/vuoto). La soglia non e' scelta: e' il quanto
# stesso del sistema. Scopo: rompere la simmetria dei quanti +-pi (twist_dip), che con chiralita'
# casuali 50/50 si bilanciano e azzerano l'olonomia netta -> nessun verso -> nessuna precessione.
# Organizzando le chiralita' sulla torsione, i +-pi si sbilanciano dove la torsione lo impone e
# l'olonomia netta acquista un verso. Default off = identico a prima (non-regressione).
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
MEM_MOTO = True          # LA MEMORIA DEL MOTO scrive su `d0` (il sito `S08_proj`). ATTIVA di
                         # default: spegnerla e' una PROVA DI SPEGNIMENTO, non fisica alternativa.
                         # ⚠ SPEGNE SOLO LA SCRITTURA SU `d0`. `mem_mot` continua ad aggiornarsi
                         #   e resta disponibile a chi la legge altrove (la proiezione
                         #   trasversale di `:6016`): cosi' si isola IL CONTRIBUTO A `d0` invece
                         #   di spegnere una grandezza di stato.
                         # ⚠ NON si usa `MEM_HEBB = False` al suo posto: quello spegne l'INTERA
                         #   funzione -- gravita' e coesione comprese. MISURATO: toglie CINQUE
                         #   siti oltre la gravita' (sigillo di G3, `T6`).
                         # Non ha un flag da riga di comando, di proposito: si imposta SUL MODULO
                         # dalla rigiocata, come `GRAV_BIFASE` in G3, cosi' il driver non cambia.
MEM_MOTO_TUTTO = True    # [G4-bis, 2026-09-22] SPEGNE L'INTERO BLOCCO DELLA MEMORIA DEL MOTO,
                         # SPOSTAMENTO DI FASE COMPRESO. `MEM_MOTO` recinta la sola scrittura su
                         # `d0`; questo recinta i QUATTRO punti in cui la memoria del moto vive:
                         #   (1) `:5655`  l'AGGIORNAMENTO  mem_mot = (1-plast)*mem_mot + plast*grad_tw
                         #   (2) `:5657`  `memedge`, e con esso `proj`
                         #   (3) `:5670`  il sito `S08_proj` (la scrittura su `d0`)
                         #   (4) `:6033`  la PROIEZIONE TRASVERSALE -> `shift_fase_dinamico` -> `phi`
                         # (4) e' L'EFFETTO INDIRETTO che `MEM_MOTO` lascia vivo, ed e' la ragione
                         # per cui questo flag esiste: spento `MEM_MOTO`, `mem_mot` continua ad
                         # aggiornarsi e `:6033` continua a leggerla.
                         # ⚠ SPENTO, `mem_mot` RESTA IDENTICAMENTE ZERO per tutto il run: nasce a
                         #   zero (`:1507`), la mitosi copia dal padre (`:5288`) e semina/Schwinger
                         #   aggiungono zeri. Non e' una grandezza "congelata a un valore": e'
                         #   una grandezza che non si accende mai.
                         # ⚠ `proj` SPENTO E' ZERO **MA CONSERVA LA SUA LUNGHEZZA**: `len(proj)` e'
                         #   il gate del ramo `GRAV_BIFASE` subito sotto. Azzerare la lunghezza
                         #   spegnerebbe ANCHE la gravita' -- che e' esattamente cio' che questa
                         #   prova NON deve fare.
                         # ⚠ COSA NON TOCCA, di proposito: i pavimenti `P3` e `P7`, la gravita'
                         #   bifase, la coesione, e `_smp_chiudi`. Non sono memoria del moto.
                         # Come `MEM_MOTO`: nessun flag da riga di comando, si imposta SUL MODULO.
MEM_FASE = False         # `MEM_FASE` [MEM-HEBB-VERSO, cura (2), decisione di Luca del
                         # 2026-10-04] recinta LA SCRITTURA DELLA MEMORIA DEL MOTO SU `phi`
                         # (il sito del TRASCINAMENTO DI FASE, qui sotto nella stessa
                         # funzione). `MEM_FASE` e' il nome, e questo commento lo NOMINA
                         # perche' `H-P7` lo pretende: un commento che non nomina il suo
                         # flag resta MUTO se una patch si inserisce fra i due.
                         # ⛔ IL DEFAULT E' `False`, E NON E' UN FLAG BYTE-INERTE: spento,
                         #   LA FISICA CAMBIA. E' la fisica DECISA -- il sito NON scrive piu'
                         #   `phi`. Acceso riproduce il comportamento storico, BYTE-IDENTICO.
                         #   E' il CONTRARIO del caso normale di questo repo, dove un flag
                         #   nuovo nasce OFF **e inerte**: qui OFF toglie una legge.
                         # IL PERCHE', MISURATO (`doc/REFERTO_mem_hebb_verso_2026-10-05.md`,
                         #   commit `2717308`): il sito SCARTAVA IL 97.3% dei contributi che
                         #   calcolava -- `phi[ii] = ...` con `ii` CHE CONTIENE RIPETIZIONI, e
                         #   in numpy l'indicizzazione fancy IN SCRITTURA fa VINCERE L'ULTIMO.
                         #   Rapporto dei moduli scartati/applicati: 36.2. Un nodo e' primo
                         #   estremo di fino a 90 archi, e 89 contributi su 90 sparivano IN
                         #   SILENZIO. ⛔ QUALE sopravvivesse dipendeva dall'ORDINE DELL'ARRAY:
                         #   non e' una legge, e' un artefatto dell'ordine.
                         # ⚠ SPEGNE SOLO LA SCRITTURA SU `phi`. `mem_mot` continua ad
                         #   aggiornarsi, `proiezione_trasversale` e `shift_fase_dinamico`
                         #   restano CALCOLATI, e il taglio `pi/4` resta applicato a
                         #   `shift_fase_dinamico`: si toglie SOLO il contributo a `phi`,
                         #   com'e' per `MEM_MOTO` sul contributo a `d0`.
                         # ⚠ E TOGLIE ANCHE IL `% self._dphi()` su `phi[ii]`, non solo la
                         #   somma: il commento di `:9516` dichiara che `(phi + 0) % (4 pi)`
                         #   e' un NO-OP **solo se `phi` sta gia' nel dominio**.
                         # ⛔ GLI ALTRI DUE DIFETTI DEL SITO NON SONO CURATI QUI, e spegnere
                         #   NON E' CURARE: <<solo l'estremo `ii` riceve>> resta in
                         #   `MEM-HEBB-VERSO`, e `dir_laterale = (-y, x, 0)` -- che privilegia
                         #   l'asse `z` del LABORATORIO mentre i nodi stanno in 3D -- e' la
                         #   voce `FASE-TRASCINAMENTO-3D`, che RESTA APERTA: la legge in 3D
                         #   NON si scrive ora (decisione di Luca).
                         # Come `MEM_MOTO` e `MEM_MOTO_TUTTO`: nessun flag da riga di comando,
                         # si imposta SUL MODULO. E' la TERZA volta della stessa forma.
# SETTORE SPINORIALE a 4pi. Ogni nodo porta una SECONDA componente di fase che, accoppiata
# alle antichiralita' (perc_chi, i +-pi gia' nel sistema), trasforma come uno spinore sotto
# 4pi (doppia copertura). Quando SPENTO (SPINORE=False) il sistema e' IDENTICO all'U(1)
# scalare (non-regressione garantita per costruzione).
# STATO REALE (verificato 2026-09-03, git-archeologia): l'EVOLUZIONE SU(2) E' CONGELATA. Il
# metodo _passo_spinoriale (Passo 2+3) e' ORFANO: la sua chiamata e' stata rimossa come
# collaterale del refactor a snapshot/commit-atomico ETC nel commit d2c76f3 (2026-09-02) e non
# e' mai stata reinnestata nel percorso vivo. Nel percorso batch/video _nb viene solo
# INIZIALIZZATO planare ([sin b, 0, cos b], tutti y=0 -> coplanari) e LETTO (proiezione grav,
# LS_AZIM), mai ruotato. Conseguenza: la fase di Berry / curvatura non-abeliana misurata dal
# 2026-09-02 e' ~0 per SPINORE CONGELATO, NON per natura abeliana del sistema. La riattivazione
# richiede il reinnesto corretto nell'ordine ETC (dietro flag, non scommento meccanico).
SPINORE = True          # Flag del settore spinoriale a 4pi. NB: l'EVOLUZIONE e' orfana (vedi
                        # sopra) - _nb resta all'init planare. Richiede COMPAT_CHI=False per i due
                        # generatori SU(2). Il costo raddoppia gli archi (la non-abelianita' stessa).
SPINORE_VIVO = True     # REINNESTO dell'evoluzione SU(2) nell'ordine ETC: _passo_spinoriale viene
                        # chiamato dentro step() PRIMA del commit atomico delle fasi, cosi' legge lo
                        # snapshot t (self.phi non ancora committata). Il braccio OFF e'
                        # --senza-spinore-vivo. Con False lo spinore e' CONGELATO.
                        # ⚠ ON DI DEFAULT dal 2026-09-18, E IL PERCHE' NON E' UNA PROMOZIONE SUA:
                        # e' il PREREQUISITO di SPIN_FEEDBACK. Il ramo del feedback e'
                        #     if SPINORE_VIVO and SPINORE and SPIN_FEEDBACK
                        # quindi con SPINORE_VIVO=False accendere SPIN_FEEDBACK lo lascerebbe
                        # ACCESO MA INERTE -- e inerte IN SILENZIO, perche' il metodo non verrebbe
                        # nemmeno chiamato e nemmeno i contatori A8 (che stanno DENTRO quel blocco)
                        # scatterebbero. E' la famiglia «cablato ma muto» (VERSO_CHI, _passo_spinoriale
                        # «ORFANO», spin_locale, TW_SPINORE, la FASE 5 inerte al 95.33 % per mesi),
                        # intercettata PRIMA che accadesse dall'audit csv/_test_fork/_audit_default.py.
                        # ⚠⚠ E VA DETTO CHIARO: `SPINORE_VIVO = True` NON E' MAI STATO VALIDATO
                        # COME DEFAULT. Tutte le campagne lo passavano DA FUORI (--spinore-vivo), quindi
                        # la configurazione era la stessa, ma NESSUN SIGILLO e' mai stato girato con
                        # questo valore come DEFAULT DI MODULO. E' un cambio NON CERTIFICATO finche' il
                        # rigiro completo non e' chiuso.
                        # Reversibile: --senza-spinore-vivo. Richiede rimisura di Berry.
SPIN_LARMOR = False     # CAMPO TRASVERSO GEOMETRICO sullo spinore (legge, zero parametri). Se True,
                        # al campo effettivo B si somma B_geo = <|tw|/PHI_CRIT * (n_i x n_j)>, termine
                        # non-abeliano perpendicolare a n che sostiene la precessione di Larmor senza
                        # auto-spegnersi quando gli spin si ordinano. Richiede --spinore-vivo. Default off.
TW_SPINORE = False      # AGGANCIO DOPPIA COPERTURA: la torsione a 4pi (tw) pilota il Bloch di tw/2
                        # (spin-1/2, geometrico) attorno all'asse sigma FISSO dalla chiralita' del legame
                        # (sigma_x uguali, sigma_z opposti). Asse persistente (non svanisce all'allineamento,
                        # il difetto di SPIN_LARMOR). Zero parametri (tw/PHI_CRIT gia' nel sistema, 1/2 = spin-1/2).
                        # Richiede --spinore-vivo. Default off = non-regressione.
SPINORE_CORRETTO = False # MASTER: gestione corretta dello spinore. Accende (1) OROLOGIO PROPRIO di de
                        # Broglie [omega_proprio = (rho/rho_c)*r_medio lungo l'asse di Bloch PROPRIO nb_t,
                        # pura fase, non deviazione dell'asse] e (2) SPINORE PRIMARIO complesso _psi_spinor
                        # (n x 2) in SU(2): psi(t+dt)=U psi_t, U=exp(-i/2 omega.sigma dt), Bloch=psi^dag sigma psi
                        # DERIVATO. Evaluate-then-commit rigoroso (snapshot t-1, commit atomico, |psi|=1).
                        # Richiede --spinore-vivo. Default off = byte-identico. NON aggancia perc_chi (flag 3
                        # separato) ne' toglie |.| dal ritmo (flag 4 separato): quelli chiudono loop/cambiano leggi.
CHI_DA_SPINORE = False  # FLAG 3 (separato, NON nel master): perc_chi = segno di doppia-copertura di _psi_spinor
                        # DOPO il commit di psi, e CHI_BASC disattivato. RICHIEDE --spinore-corretto (sennò loop).
SCALA_MIN = False       # NESSUNA LUNGHEZZA SOTTO `LAM` (2026-09-21). `LAM` e' la scala minima
                        # del sistema: sotto, un solitone non esiste -- vincolo GIA' dichiarato
                        # nel file e affidato a un pavimento COMOVENTE (`f*median(d0)`) che
                        # SCENDE INSIEME a cio' che dovrebbe trattenere.
                        #
                        # ⚠ NON SI RIMAPPA IL VALORE: SI SMORZA LA DISCESA.
                        #   incremento >= 0  ->  INTATTO, bit per bit
                        #   incremento <  0  ->  moltiplicato per max(0, 1 - LAM/x),
                        #                        con `x` il valore PRIMA di QUELLA scrittura
                        #
                        # ⚠ PERCHE' NON UNA RIMAPPATURA, ed e' il difetto che ha ucciso la
                        #   prima forma proposta: `LAM + x*exp(-LAM/x)` e `sqrt(x^2+LAM^2)`
                        #   soddisfano tutti i criteri di forma MA NON SONO IDEMPOTENTI --
                        #   danno `L(x) > x` anche per `x >> LAM` (a `3*LAM`: +4.98%). I
                        #   pavimenti girano SETTE volte per passo: ogni lunghezza sarebbe
                        #   stata gonfiata sette volte a passo per tremila passi, cioe'
                        #   un'ESPANSIONE ARTIFICIALE FABBRICATA DAL VINCOLO -- e l'espansione
                        #   e' la grandezza che il run deve misurare. Lo smorzamento non ha
                        #   quel difetto perche' NON TOCCA NULLA quando la lunghezza non scende.
                        #
                        # LE PROPRIETA', dimostrate e non asserite:
                        #  (1) IDENTITA' ESATTA per ogni incremento >= 0: non un bit cambia;
                        #  (2) NESSUNA INFLAZIONE: il vincolo non aumenta MAI una lunghezza,
                        #      quindi non puo' produrre espansione da solo;
                        #  (3) APPROCCIO ASINTOTICO. Con `x > LAM` e `dx < 0`:
                        #        nuovo - LAM = (x - LAM) * (1 + dx/x)
                        #      la DISTANZA da `LAM` si MOLTIPLICA per `(1 + dx/x)`, positivo
                        #      finche' `x + dx > 0`: `nuovo > LAM` SEMPRE, avvicinamento
                        #      GEOMETRICO, `LAM` mai toccato;
                        #  (4) ZERO COEFFICIENTI: c'e' solo `LAM`.
                        #
                        # ⚠ IL `max(0, .)` NON E' UNA SCELTA, E' UN OBBLIGO DI SEGNO: per
                        #   `x < LAM` il fattore `1 - LAM/x` e' NEGATIVO e trasformerebbe una
                        #   discesa in una SALITA. A zero, una lunghezza gia' sotto `LAM` NON
                        #   SCENDE PIU': si congela, non si teletrasporta.
                        # ⚠ IL CASO PATOLOGICO E' CONTATO, NON TAPPATO: se `dx <= -x` la (3)
                        #   non vale. NIENTE pavimento scelto: `_g_sm_patol` lo CONTA e `Z4`
                        #   lo legge. Se non scatta mai, l'invariante tiene; se scatta, e' un
                        #   riscontro.
                        # ⚠ I SETTE PAVIMENTI VECCHI SPARISCONO a flag acceso: la discesa e'
                        #   gia' smorzata alla scrittura, e due leggi sovrapposte darebbero un
                        #   pavimento comovente che continua a mordere.
                        # ⚠ LE NASCITE sono CONCATENAZIONI, non discese: il troncone sotto
                        #   `LAM` si porta A `LAM` ALLA NASCITA, e da li' vale lo smorzamento.
                        # ⚠ PER `d` la regola va sull'INCREMENTO del Verlet, non sul valore
                        #   finale: `dts*vd_half` e `dts*vd`, non `d + dts*vd`.
                        # OFF = byte-identico.
COES_ADIM = False       # LA COESIONE CON DIMENSIONI GIUSTE E DENSITA' LOCALE (2026-09-21).
                        # OGGI: `dI/d` ha dimensioni [I]/[L] e `lap_arco` ha [I], E SI SOMMANO;
                        # e `I_med` (MEDIA GLOBALE, A2) compare AL QUADRATO al denominatore.
                        # NUOVA:  F_adim = tanh( -(dI/I_arco - tanh(|dI/I_arco|)*lap/I_arco)
                        #                        + richiamo ) * filtro_portata
                        #         d0 += passo_causale * F_adim,  passo_causale = LAM*sqrt(K_C)*DT
                        # `|F_adim| <= 1` PER COSTRUZIONE, non per clip: |tanh|<=1 e
                        # filtro_portata in (0,1). Per questo SOSTITUISCE il clip
                        # `tanh(stress)*d0`, che `Z79` ha misurato SATURO.
                        # `d0^2` SI TOGLIE: col passo causale davanti lo spostamento e' GIA'
                        #   una lunghezza; per `d0^2` sarebbe una lunghezza al CUBO.
                        # `filtro_portata` SI TIENE: adimensionale, in [0,1], non rompe il
                        #   limite, e la sua ragione e' FISICA (corto raggio), non dimensionale.
                        # `I_arco` NEL VUOTO, NESSUN PAVIMENTO: `0/0 := 0` come dichiarato per
                        #   `scala_p` in `Z67`; e dove `I_arco` e' minuscolo ma non nullo il
                        #   rapporto e' enorme MA IL `tanh` LO LIMITA A 1 -- la limitatezza e'
                        #   STRUTTURALE, non messa a mano.
                        # ⚠ RESTA APERTO, dichiarato: `passo_causale*tanh(...)` fissa la
                        #   MAGNITUDINE al passo causale. Il tetto causale e' un LIMITE giusto,
                        #   ma usarlo come SCALA della forza e' una scelta, non una derivazione.
                        # OFF = byte-identico.
PEQ_ESATTO = False      # IL RILASSAMENTO DI `peq` IN FORMA ESATTA (2026-09-21, cura C1).
                        # DIFETTO CURATO: `peq += dt_e*(rho-peq)/tau_bg + ...` e' un EULERO
                        #   ESPLICITO. Per `x = dt_e/tau_bg > 1` SCAVALCA il bersaglio, e con
                        #   `rho < peq` lo scavalca SOTTO ZERO. MISURATO (`Z94`): al passo 1126
                        #   del ramo D, `x = 1.2018` porta `peq` da `1.060e-02` a `-4.854e-04`,
                        #   e il pavimento `max(peq,1e-9)` di `:4215` RIBALTA IL SEGNO
                        #   dell'anomalia moltiplicandola per `3.7e5`: `nsub = 22591`.
                        # LA FORMA, DERIVATA e non scelta: da `dpeq/dt = (rho-peq)/tau` con
                        #   `rho` e `tau` costanti SUL PASSO -- l'ipotesi che l'Eulero gia' fa --
                        #   la soluzione e' ESATTA:  peq <- rho + (peq-rho)*exp(-dt/tau).
                        # POSITIVITA' DIMOSTRATA, non sperata: posto `a = exp(-dt/tau)` in
                        #   `(0,1]`, si ha `peq_new = a*peq + (1-a)*rho`, una COMBINAZIONE
                        #   CONVESSA, quindi `min(peq,rho) <= peq_new <= max(peq,rho)` per
                        #   QUALUNQUE `dt`. Con `peq>=0` e `rho = 0.5*(I_i+I_j) >= 0` sempre,
                        #   `peq_new >= 0` SEMPRE, SENZA PAVIMENTI.
                        # LA DIFFUSIONE si tratta con uno SPLITTING DI LIE-TROTTER: i due
                        #   rilassamenti si applicano IN SEQUENZA, ciascuno in forma esatta.
                        #   Il PUNTO FISSO del termine di diffusione e' `peq + flusso` in
                        #   ENTRAMBI i rami di `DIFF_RES` (verificato algebricamente), quindi
                        #   non serve nessuna grandezza nuova.
                        #   ⚠ L'ordine di accuratezza resta 1, come l'Eulero di oggi: NON
                        #   peggiora nulla, e non introduce numeri.
                        #   ⚠ LA POSITIVITA' DEL SECONDO PASSO richiede `peq+flusso >= 0`:
                        #   con `DIFF_RES == 0` (il caso di TUTTI i run) il bersaglio e'
                        #   `c_arco`, una MEDIA PESATA dei `peq` dei vicini, quindi `>= 0`.
                        #   Con `DIFF_RES != 0` il bersaglio e' `rho - c_arco` e PUO' essere
                        #   negativo: li' la dimostrazione NON vale, ed e' CONTATO.
                        # ⚠ COSA QUESTA CURA *NON* FA: non toglie il pavimento `max(peq,1e-9)`
                        #   di `:4215`. Con `peq>=0` garantito quel pavimento non regolarizza
                        #   piu' un SEGNO ma solo lo zero, e toglierlo richiede la forma
                        #   simmetrica, che e' UN'ALTRA cura e ha IL SUO POLO.
                        # OFF = byte-identico.
INVARIANTI = True       # GLI INVARIANTI: il programma si FERMA quando una grandezza esce dal
                        # suo dominio, e dice DOVE (2026-09-21, C5, decisione di Luca).
                        # ⚠ ACCESO DI DEFAULT. **Legge soltanto: su un run sano non cambia un
                        #   bit.** Si spegne con `--invarianti=off`, che serve a RIGIOCARE i run
                        #   dell'epoca 1 e 2, i quali violano regole oggi note *(il `peq`
                        #   negativo al passo 1126)* e che si vogliono riprodurre COM'ERANO.
                        # PERCHE' DUE LIVELLI, e il primo da solo NON BASTA:
                        #   l'esplosione del 2026-09-21 **NON era un overflow** -- `1.8e6` e' un
                        #   numero normale per il computer. Un controllo sui soli errori
                        #   NUMERICI non l'avrebbe vista. **L'avrebbe vista una regola FISICA:
                        #   `peq` non puo' essere negativo.**
ANOM_SIMM = False       # L'ANOMALIA SIMMETRICA, SENZA PAVIMENTO (2026-09-21, C1-bis).
                        # FORMA:  anom = 2*(rho - peq) / (rho + peq),  e `0/0 := 0`.
                        # DIFETTO CURATO: `(rho-peq)/max(peq, 1e-9)` usa un PAVIMENTO SCELTO
                        #   (`A11`, corollario 1) che non esprime nessun vincolo fisico: sta li'
                        #   per non dividere per zero. E `Z94` ha misurato cosa costa: con
                        #   `peq` negativo RIBALTA IL SEGNO e moltiplica per `3.7e5`.
                        # PERCHE' LA FORMA SIMMETRICA E' MEGLIO, derivato PRIMA di scriverla
                        #   (`csv/_deriva_anom_simm.py`):
                        #   * coincide con la vecchia per anomalie PICCOLE (`0.25` contro
                        #     `0.2222`): e' la riduzione al limite;
                        #   * il caso che oggi ESPLODE -- `peq -> 0` con `rho` ordinario --
                        #     passa da `1e+08` a ESATTAMENTE `+2`. **Li' il pavimento diventa
                        #     INUTILE, ed e' il punto della cura.**
                        #   * e' limitata in `[-2, +2]` **SE E SOLO SE** `rho >= 0` E `peq >= 0`.
                        # ⚠ DIPENDE DA `C1`, E NON E' UN DETTAGLIO: con `peq < 0` il
                        #   denominatore `rho+peq` SI ANNULLA in `peq = -rho` -- **e' un POLO,
                        #   non un limite** -- e oltre il polo il SEGNO SI ROVESCIA. Senza
                        #   `PEQ_ESATTO` questa cura SOSTITUISCE UN PAVIMENTO CON UN POLO.
                        #   Il caso e' CONTATO (`_g_as_polo`), non assunto impossibile.
                        # ⚠ `0/0 := 0` E' UNA DEFINIZIONE, NON UNA REGOLARIZZAZIONE: non c'e'
                        #   nessun numero da scegliere, e il valore e' quello giusto -- **dove
                        #   non c'e' densita' non c'e' anomalia**. Precedente dichiarato nello
                        #   stesso file: `scala_p`, `Z67`.
                        # OFF = byte-identico.
COES_CAUSALE = False    # LA COESIONE CHE RISPETTA L'ISTANTE E IL CONO LOCALE (2026-09-21, C4).
                        # DUE DIFETTI CURATI, entrambi misurati in `Z92`:
                        #   (a) ISTANTI MISTI: nella stessa `tanh` convivono `_forza_adim`,
                        #       costruito su densita' di FINE `step`, e `richiamo_elastico`,
                        #       che legge un `d0` GIA' SPOSTATO DA SETTE SCRITTURE dello
                        #       stesso passo. Due istanti in una somma.
                        #   (b) TETTO GLOBALE: `LAM*sqrt(K_C)*DT` e' costruito su COSTANTI DI
                        #       MODULO. `c_sistema = 1.1314` non conosce il cono del luogo in
                        #       cui scrive, e il cono locale misurato scende fino a `0.566`:
                        #       li' il tetto globale ne permette il DOPPIO (`A5`).
                        # LA CURA:
                        #   (a) `d0` e `d` si leggono dalla FOTOGRAFIA DI INIZIO PASSO, la
                        #       stessa di `C3` -- una sola macchina, due utenti;
                        #   (b) il tetto diventa `cs_arco * DT`, con `cs_arco` il piu' LENTO
                        #       dei due nodi: la scelta CONSERVATIVA, e non e' un parametro
                        #       perche' `_cs_nodo_prev` esiste gia'.
                        # ⚠ COSA QUESTA CURA *NON* FA, e va detto: `I_nodi`, `I_arco` e
                        #   `lap_arco` restano di FINE `step`. NON e' una svista: `psi` e' la
                        #   stessa che `step()` ha appena committato, quindi **quelle tre sono
                        #   gia' coerenti fra loro**; l'unico ingresso fuori istante era `d0`.
                        #   Portare anche `psi` a inizio passo richiederebbe una fotografia PER
                        #   NODO con la sua chirurgia, ed e' un'altra cura.
                        # ⚠ E IL TETTO LOCALE NON E' SEMPRE PIU' STRETTO: col cono mediano
                        #   (`cs ~ 1.65`) e' piu' LARGO di `c_sistema = 1.1314`. Il punto non e'
                        #   stringere: e' che il tetto DEVE essere quello del LUOGO. Dove il
                        #   cono e' lento stringe, dove e' veloce allarga -- ed e' causalita',
                        #   non prudenza. **Si CONTA in quale verso agisce.**
                        # OFF = byte-identico.
SCALA_MIN_PASSO = False # IL FRENO UNA VOLTA PER PASSO, SULLA VARIAZIONE TOTALE (2026-09-21, C3).
                        # DIFETTO CURATO (`Z91`): `SCALA_MIN` frena OGNI SCRITTURA guardando il
                        #   valore lasciato dalla precedente NELLO STESSO PASSO -- sei scritture
                        #   su `d0` e `nsub` su `d`. Quindi il risultato DIPENDE DALL'ORDINE
                        #   delle leggi, e poiche' frena solo le DISCESE produce un CRICCHETTO:
                        #   con `a > 0`, `b < 0`, `a+b = 0` il risultato NON e' zero.
                        # LA FORMA, gia' DIMOSTRATA nel referto: applicato UNA VOLTA SOLA sulla
                        #   variazione TOTALE, `dx = a+b = 0` non e' una discesa, quindi il
                        #   valore e' INTATTO e il bias e' ZERO ESATTO. E non contiene l'ordine.
                        # COSA CAMBIA, in concreto:
                        #   * `_sd0` diventa PASSANTE: le sei scritture di `d0` non frenano;
                        #   * dentro i sotto-passi del Verlet `d` non frena e non ha pavimento;
                        #   * a FINE PASSO si applica `_smorza` UNA VOLTA su `fine - inizio`.
                        # ⚠ LA MITOSI CAMBIA IL NUMERO DI ARCHI, quindi lo SNAPSHOT DI INIZIO
                        #   PASSO subisce LE STESSE operazioni di `d0`/`d` ai quattro siti di
                        #   ristrutturazione, e gli archi NATI nel passo entrano con il PROPRIO
                        #   valore di nascita: la loro variazione e' zero e non vengono frenati.
                        #   **E' la parte delicata, ed e' cablata invece che assunta.**
                        # ⚠ LE NASCITE restano a `LAM` (`_nasce`): una concatenazione non e' una
                        #   discesa, e il punto di partenza non e' un freno.
                        # OFF = byte-identico.
PEQ_NASCITA_LOCALE = False  # UNA SOLA LEGGE DI NASCITA PER `peq`, E LOCALE (2026-09-21, C2).
                        # DIFETTO CURATO: `peq` nasce in TRE MODI INCOERENTI.
                        #   (a) `_allaccia` scrive `nan` e `step` (`:4189`) lo CALIBRA sulla
                        #       `rho` DELL'ARCO STESSO -> `anom = 0` ESATTO alla nascita;
                        #   (b) la mitosi lo EREDITA dall'arco che si divide -- ed e' giusto:
                        #       un arco che si spezza in due NON e' una nascita, e' una
                        #       CONTINUAZIONE, e i due tronconi hanno la storia del padre;
                        #   (c) Schwinger scrive `median(self.peq)`, LA MEDIANA GLOBALE.
                        # (c) VIOLA `A2`: una statistica GLOBALE entra in una legge locale, e
                        #   quei nodi NON hanno alcun rapporto con la mediana della rete.
                        # LA CURA NON INVENTA NIENTE: usa il meccanismo GIA' ESISTENTE di (a).
                        #   Schwinger scrive `nan`, e `:4189` lo calibra sulla `rho` del suo
                        #   arco, ESATTAMENTE come `_allaccia`. UNA sola legge di nascita.
                        # ⚠ VERIFICATO CHE E' SICURO, non assunto: fra la `mitosi()` e la
                        #   calibrazione di `:4189` girano `rilassa_disegno`,
                        #   `memoria_hebbiana_moto` e `scuoti_vuoto`, e NESSUNA delle tre
                        #   legge `peq` -- controllato dal sorgente, zero occorrenze.
                        # ⚠ E (b) NON SI TOCCA: l'eredita' della mitosi e' COERENTE, perche'
                        #   non e' una nascita. Cambiarla sarebbe curare cio' che non e' rotto.
                        # OFF = byte-identico.
CHI_COOP = False        # COOPERAZIONE (decisione di Luca, 2026-09-21): chi_basc NON si spegne; scrive la
                        # GEOMETRIA in `perc_geom` (il giro e' compiuto o no, dalla torsione) mentre lo
                        # SPINORE scrive la CARICA in `perc_chi` (segno di doppia copertura). I due fanno
                        # lavori DIVERSI e devono COOPERARE, non escludersi: spegnere chi_basc per
                        # accendere lo spinore toglierebbe la geometria INSIEME alla carica, e un
                        # confronto con due variabili cambiate insieme non si legge.
                        # LETTORI: catena della torsione (CHI_CORE/FRAME_DRAG/TORS_4PI) -> perc_geom;
                        # campo B del passo spinoriale, mitosi, Schwinger, TEMPO_SEGNO -> perc_chi.
                        # RICHIEDE --spinore-corretto (stesso SystemExit di CHI_DA_SPINORE).
                        # OFF = byte-identico: i rami nuovi sono IRRAGGIUNGIBILI, non solo inerti.
TEMPO_PROPRIO_ORIENTATO = False # FLAG 4 (separato, profondo): toglie |.| da f in ritmo() -> r con SEGNO
                        # (tempo proprio orientato). Cambia una legge di base; default off.
FASE_2PI = False        # [B1, 2026-09-22] CURA: `phi` e' una FASE ORDINARIA su [0, 2pi).
                        # DECISIONE DI LUCA, presa DOPO la verifica `Z120`: nessuna riga della
                        # FISICA distingue `phi` da `phi + 2pi`, fuori dalla torsione e
                        # dall'antifase. 31 candidati letti uno per uno.
                        # IL FATTO CHE LA REGGE: in 31 righe su 31 il campo legge `phi` da
                        # `exp`/`cos`/`sin` (Z118), e li' `exp(i(phi+2pi)) = exp(i phi)`: la
                        # doppia copertura e' INVISIBILE. E' un conto, non un'interpretazione.
                        # LA DOPPIA COPERTURA RESTA dove e' gia' vera: nel SEGNO esplicito
                        # (`_spinor_lift`, `s_k = sign(perc_chi)`) e nei MEZZI ANGOLI
                        # (`exp(-0.5i ...)`). UN SOLO PONTE (A10).
                        # ⚠ UNA DELLE QUATTRO GAMBE E' CADUTA, e va detto: il docstring di
                        #   `_passo_spinoriale` dice che `phi` e' l'AZIMUT del Bloch. MISURATO
                        #   FALSO (Z121: R <= 0.18 contro un criterio di 0.90). L'argomento
                        #   caduto NON argomenta per 4pi: dice solo che `phi` non e' cio' che
                        #   il commento dichiarava. -> `S08`, aperto.
                        # COSA TOCCA: (a) il DOMINIO, `% (4pi)` -> `% (2pi)`, via `_dphi()`;
                        #   (b) le DIFFERENZE di fase, `_w4` -> `_w2`, via `_wphi()`;
                        #   (c) l'ANTIFASE, `+2pi` -> `+pi`, come META' del dominio;
                        #   (d) la SOGLIA della mitosi, `2pi + pi` -> `2pi`.
                        # ⚠ COSA NON TOCCA, ed e' un confine scelto: la TORSIONE ACCUMULATA
                        #   (`tw`, `twp`, `_w8` a :4651-4655). `tw` e' un ACCUMULO: non ha
                        #   periodo, e il suo dominio appartiene a `SCALE-TW`. Toccarlo qui
                        #   mescolerebbe due decisioni.
                        # ⚠ SPENTA DI DEFAULT. Il passaggio a `True` e' una decisione di Luca
                        #   dopo i QUATTRO TEST del paragrafo E. Se un test fallisce, la
                        #   lettura CADE e si scrive.
                        # Schede: `doc/REGISTRO_FISICA.md`, LA FASE `phi` E IL SUO DOMINIO,
                        #   e LA MITOSI E SCHWINGER.
SEMINA_LAM = False      # [CURA DELLA SEMINA, 2026-09-24] `A13`: **`LAM` E' LA SCALA DI
                        # PLANCK DEL SISTEMA**, e sotto `LAM` non esiste niente -- ne' archi
                        # ne' DISTANZE FRA NODI, **nemmeno alla semina**.
                        # IL DIFETTO (`D38`, misurato): al passo ZERO il **99.96 %** dei nodi
                        # ha il primo vicino **sotto `LAM`**, con mediana **`0.135*LAM`**: il
                        # sistema nasce **~7.4 volte piu' fitto della propria scala di
                        # Planck**. Da li' il **42.47 %** degli archi nasce sotto `LAM`, e
                        # `_nasce` li tronca -- cioe' **SCOLLEGA `d` da `pos`** (`D02` fatto a
                        # mano).
                        # LA CURA: ogni nodo nuovo a distanza **`>= LAM` da QUALUNQUE nodo
                        # gia' presente** -- stessa massa, altre masse, **VUOTO DI FONDO** --
                        # con semina casuale e **SCARTO** (`RSA`). Nessun nodo di seconda
                        # classe: il vuoto passa da `semina()` come tutto il resto (`:6392`).
                        # ZERO NUMERI NUOVI: `LAM` e' l'assioma, e l'`RSA` non ha parametri.
                        # Scheda 12 `nascita-archi`. Default SPENTO.
                        # ⚠ NON e' `NASCITA_LAM`, che e' RITIRATA: filtrare gli ARCHI lascia i
                        #   NODI sotto `LAM`, cioe' toglie il sintomo e lascia la violazione.
POZZO_D = False             # [D02, 2026-09-27] NEL POZZO DEL GRAFO `L` VIENE DA `self.d`.
                        # IL DIFETTO: `pozzo_grafo` calcola `L` da `self.pos` (il DISEGNO) e
                        # il risultato entra nella SPINTA `S09` -- mentre il suo stesso
                        # docstring dichiara «diviso per la DISTANZA REALE DELL'ARCO».
                        # La distanza reale dell'arco e' `self.d`: `pos` e' il disegno, e
                        # non deve entrare nella gravita'. LA REGOLA E' `A3-DISEGNO`,
                        # NON `A13` -- che e' «`LAM` e' la scala di Planck del sistema».
                        # (Correzione di Luca, 2026-09-27: avevo citato `A13`, e l'avevo
                        # PROPAGATA dalla revisione. Un'etichetta sbagliata manda chi
                        # legge a cercare la regola nel posto sbagliato.)
                        # ⚠ TOCCA SOLO `pozzo_grafo`: le altre due letture di `pos` in
                        # `memoria_hebbiana_moto` (`:6590`, `:6978`) sono DIREZIONI, non
                        # lunghezze, e sono `D03` -- un altro fronte. Un flag che le
                        # cambiasse insieme misurerebbe due cose (par.1).
                        # A flag acceso `L = self.d[mask]`, e il PAVIMENTO `1e-9` NON SERVE
                        # PIU': con `SEMINA_LAM` si ha `d >= LAM` alla semina, e dal `6b` ANCHE alla divisione — ### **senza condizione sul flag**. ⚠ MA E'
                        # UNA MISURA, NON UN'INVARIANTE DEL CODICE (`D11`), quindi i casi
                        # `d <= 0` si CONTANO (`A8`) invece di assumerli impossibili
                        # (`A11`): `_pozzo_d_nonpos`, creato SOLO nel ramo acceso, cosi' la
                        # byte-identita' a flag spento resta vera. Default SPENTO.
TEMPO_UNICO_MITOSI = True   # [CURA 2 -> STRUTTURALE, 2026-09-27: decisione di Luca]
                        # ⚠ NON E' PIU' UN FLAG: E' UNA LEGGE. I quattro rami `else`
                        # sono USCITI dal simulatore, e l'assegnazione da `_applica_flag`
                        # e' stata TOLTA: nessun percorso puo' piu' spegnerla.
                        # RESTA un booleano di MODULO di proposito: cosi' continua a
                        # comparire nella dichiarazione della configurazione (`H-P5` la
                        # enumera con `vars(S)`), e cancellarla la farebbe SPARIRE dal
                        # referto proprio mentre diventa obbligatoria.
                        # IL BRACCIO OFF VIVE AL TAG `pre-cura2-strutturale`, non in un
                        # flag: per questo NON c'e' un `--senza-tempo-unico-mitosi`.
                        # I rami: `csv/_archivio/rami_off_cura2.py`.
                        # [CURA 2, 2026-09-24] UN SOLO OROLOGIO DENTRO `mitosi()`.
                        # IL DIFETTO: `tau_pp = 1 + |tw|/PHI_CRIT` si chiama "tempo proprio
                        # locale" ma e' una MISURA DI TORSIONE, e la mitosi la usa in DUE modi
                        # incompatibili -- come TEMPO (il ritmo `1/tau_pp`, la costante di
                        # rilassamento di `_rep`) e come POSIZIONE sull'asse di `tw` (la soglia,
                        # il centro, l'inversione `segno`). Gli usi-TEMPO passano all'OROLOGIO
                        # `dt_e` che il sistema gia' definisce (`:4369`); gli usi-TORSIONE
                        # restano com'erano, perche' li' intenzione e implementazione COINCIDONO.
                        # E `tau_nodo` (`:5206-5210`) e' IDENTICO al ramo `TEMPO_SEGNO` di
                        # `ritmo()`, CHE NON GIRA (`Z130`): la mitosi usa come "tempo proprio"
                        # la definizione di tempo che il resto del sistema ha SCARTATO.
                        # Scheda 9 `tempo-nella-mitosi`. Default SPENTO.
RITMO_WRAP_2PI = False  # [D34, 2026-09-22] CURA: il ramo SPINORIALE di `ritmo()` avvolge sul
                        # periodo GIUSTO. `np.angle` ha periodo `2pi`, quindi
                        #     a = angle(psi_spin) - angle(psi_spin_prec)   sta in (-2pi, 2pi]
                        # e `((a + 2pi) % 4pi - 2pi)` su quell'intervallo E' L'IDENTITA':
                        # NON AVVOLGE NIENTE. Dimostrato: max|w4(a) - a| = 0.000e+00 su 100 001
                        # punti (Z117). Ogni attraversamento del taglio a +-pi registra una
                        # frequenza spuria di ~2pi/DT.
                        # ⚠ IL CODICE CONTIENE IL PROPRIO CONTROESEMPIO: il ramo SCALARE otto
                        #   righe sopra (`:2565`) usa GIA' `((a + pi) % 2pi - pi)`. Stessa
                        #   grandezza, due periodi, stessa funzione. E il commento di `:2566`
                        #   dichiara l'equivalenza "nel limite |dphi| < pi", che e' ESATTAMENTE
                        #   la condizione in cui il taglio non si attraversa.
                        # ⚠ SPENTO DI DEFAULT, e il default NON si cambia qui: e' una decisione
                        #   di Luca, dopo che ha letto la prova a 600 passi (voce `E3`).
                        # ⚠ TOCCA SOLO IL RAMO SPINORIALE. Il ramo scalare e' gia' giusto, e
                        #   `TEMPO_SEGNO` (che non gira) non passa di qui.
                        # Scheda: `doc/REGISTRO_FISICA.md`, IL TEMPO PROPRIO.
SYNC_SPINORE = False    # KURAMOTO SU(2) SUGLI SPINORI (sotto-flag): tira ogni spinore verso l'allineamento
                        # con la media di vicinato via torque omega_sync = forza*(nb x nb_media), nb_media
                        # = (wI @ nb_t)/uno. forza = la STESSA del Kuramoto-phi (K_SYNC, 2/pi, prof_rel,
                        # rinforzo_shear). Torque ISTANTANEO -> entra in omega_tot (rotazione), NON in omega_s
                        # (memoria: darebbe accumulo/divergenza). Zero parametri nuovi. Richiede il settore
                        # spinore vivo e K_SYNC!=0 (forza dal blocco Kuramoto-phi). Default off = byte-identico.
DEPARAM_OROLOGIO = False # DE-PARAMETRIZZAZIONE RELAZIONALE DELL'OROLOGIO de Broglie: omega_clk non piu' da
                        # |Psi|^2 ESTENSIVA / rho_c GLOBALE (misurato ~95% connettivita', deg 2->379), ma
                        # dalla COERENZA D'ARCO intensiva sum_j w_ij cos(phi_i-phi_j) / sum_j w_ij (media pesata
                        # sugli archi incidenti, indipendente dal grado, in [-1,1]); tetto naturale = 1 (nessun
                        # rho_c globale, niente normalizzazione per volume). Relazionale sulla rete, non per volume.
                        # Tocca SOLO l'orologio spinoriale, NON la Psi-sorgente di gravita'. Richiede
                        # --spinore-corretto. Zero parametri. Default off = byte-identico.
SYNC_FASE_OROLOGIO = False # KURAMOTO SUL SEGNO DI DOPPIA-COPERTURA (la via genuina all'ordinamento del segno,
                        # §43): torque RELAZIONALE O(dt^1) che tira la fase di doppia-copertura alpha_k =
                        # arg<canon(nb_k)|psi_k> verso la media di vicinato. eta = dt*forza*sin(media_alpha-alpha),
                        # applicato come FASE GLOBALE e^{i eta} su psi -> lascia nb=psi^dag sigma psi INVARIANTE
                        # (gravita' intatta), agisce SOLO sul segno (non su phi U(1)). forza/wI/uno = gli stessi del
                        # Kuramoto-phi (K_SYNC, prof_rel, rinforzo_shear) -> zero parametri. Primo ordine in dt
                        # (NON O(dt^2) come il motore-unico artefatto: qui il termine dipende dalla DIFFERENZA
                        # sin(media-alpha), relazionale). Richiede --spinore-corretto. Default off = byte-identico.
CAMPO_SPINORIALE = False # [FASE 1 dev-spinoriale] campo EMESSO dallo spinore (Psi spinoriale n x 2) calcolato IN
                        # PARALLELO in calcola_psi (self.psi_spin, self.rho_spin), non ancora agganciato a
                        # gravita'/forze/mitosi (fasi 2-4). Riduzione-al-limite: con _psi_spinor=(e^{i phi},0) la
                        # componente 0 == campo scalare. Default off = byte-identico.
TEMPO_SEGNO = False      # MOD 5.3a+5.3b (dev-spinoriale): tempo proprio DEPURATO. 5.3a VERSO (Feynman-Stuckelberg):
                        # s_k = 1+(perc_chi-1)*m_coer, m_coer = coerenza col campo locale (materia/antimateria COERENTE
                        # inverte il verso, il VUOTO incoerente va avanti). 5.3b MAGNITUDINE: ritmo() = 1+|tw_nodo|/PHI_CRIT
                        # (torsione esplicita, il de Broglie del campo emesso e' stato bocciato da S3b). Firma solo
                        # l'evoluzione interna (spinore+fase U(1)); eta/geometria restano magnitudine. Da stato t-1 (causale).
                        # Richiede --campo-spinoriale + --spinore-corretto. Default off = byte-identico.
OROLOGIO_SEGNO = False    # MOD 5.3c (dev-spinoriale): firma il VERSO dell'orologio de Broglie INTERNO _phc col
                        # segno di doppia-copertura STABILE s_k=sign(perc_chi) (lignaggio, non l'istantaneo che
                        # oscilla): materia exp(-), antimateria exp(+), tempi SPECULARI. |omega_clk| INVARIATA (S3b:
                        # solo verso, non velocita'). Fase globale -> nb invariante (gravita'/direzione intatte);
                        # eta/geometria = magnitudine. Vive nel ramo --deparam-orologio (orologio pura-fase).
                        # Richiede --campo-spinoriale + --spinore-corretto. Default off = byte-identico.
KURAMOTO_SU2 = False     # KURAMOTO SU(2) NON-ABELIANO (§46): ruota lo SPINORE INTERO verso la media SU(2) dei
                        # vicini psi_bar=(wI@psi)/|.| con rotazione geodetica attorno all'asse VARIABILE nb x nb_bar
                        # (non commuta -> non-abeliano genuino). Verso+segno ruotano INSIEME; il segno emerge per
                        # OLONOMIA (fase geometrica, asse variabile), non targettizzato. nb SI muove (gravita' fisica,
                        # voluto: convergenza-dt, non 6.7e-16). Torque O(dt^1), forza/wI dal Kuramoto-phi, zero param.
                        # Differenza da --sync-spinore: quello media i Bloch (fase-invariante) senza de-param; qui la
                        # media SU(2) e' modulata dalla coerenza di segno (accoppia segno/verso). Richiede --spinore-corretto.
FORK_SU2 = False        # [FORK SU(2) - STRATO 0] ARC-CONNECTION non-abeliana nella FORZA. Sostituisce il
                        # trasporto SCALARE (stessa A applicata ad a e b -> abeliano per STRUTTURA) con il
                        # trasporto parallelo di Berry NON normalizzato N_ij = (1+n_i.n_j) I + i(n_i x n_j).sigma,
                        # che MESCOLA a,b:  Im<psi_i|psi_j> -> Im<psi_i| N_ij/2 |psi_j>.
                        # N/2 = cos(chi/2) U_ij, quindi porta con se' il peso cos(chi/2) = |<n_i|n_j>| = OVERLAP
                        # DI SPIN (accoppiamento fisico, non manopola: e' cio' che resta non normalizzando).
                        # Ad allineati N/2 = I -> riduzione ESATTA al ramo scalare (canale di fase/EM preservato);
                        # ad antipodali N = 0 -> arco spento senza inventare assi. Zero parametri nuovi.
                        # Richiede --campo-spinoriale (il trasporto agisce su _psi_spinor). Default off = byte-identico.
FORK_SU2_MEM = False    # [FORK SU(2) - STRATO 1] CONNESSIONE CON MEMORIA: N_ij nasce dai Bloch RITARDATI
                        # n(t-tau) invece che da quelli dell'ISTANTE. tau = d/cs (tempo-luce d'arco):
                        # nessun numero nuovo, d e cs esistono gia'.
                        # PERCHE': lo Strato 0 e' INERTE per TEOREMA, non per bug. Se i Bloch che
                        # costruiscono la connessione sono quelli DEGLI STESSI stati trasportati e allo
                        # STESSO istante, |psi_i> e' autovettore di (n_i.sigma) con autovalore +1, quindi
                        # <psi_i|N_ij|psi_j> = 2<psi_i|psi_j> ESATTO (misurato 1.57e-15 su 200000 coppie,
                        # csv/_seal_fork/_reperto_inerzia.py) e la forza non cambia di un bit.
                        # LA CURA E' LA CAUSALITA', non una taratura: una mappa costruita ORA, dagli stati
                        # di ORA, non puo' muovere gli stati di ORA. Col ritardo psi(t) NON e' piu'
                        # autovettore di n(t-tau).sigma -> il teorema non si applica -> la forza cambia.
                        # COME: rilassamento del VERSORE di Bloch (non della matrice: un blend lineare di
                        # matrici uscirebbe da SU(2), par.4), slerp GEODETICO sulla sfera con
                        # alpha = 1 - exp(-dt/tau) = passo ESATTO di dn/dt = (n_cur - n_ret)/tau. PRIMO
                        # ORDINE, quindi esponenziale esatto e MAI Verlet (par.4). Il TRASPORTO resta
                        # sugli spinori CORRENTI: cambia solo DA QUANDO viene la connessione.
                        # A RIPOSO n_ret = n_cur -> inerte -> si riduce allo Strato 0 (e quindi allo
                        # scalare): da fermo la memoria non inventa forza. Per tau->0, alpha->1, idem.
                        # Richiede --fork-su2 (da solo verrebbe IGNORATO con avviso). Default off = byte-identico.
STEP2_OROLOGIO = True   # [PROMOSSO A FISICA DI DEFAULT il 2026-09-16, par.10 - decisione di Luca]
                        # AGGANCIO OROLOGIO <-> METRICA: omega_clk *= (cs/CS_M)^2.
                        # I TRE CRITERI DEL par.10, col riscontro di ciascuno:
                        #  (1) DERIVATA, non tarata: orologio di Compton `omega = m c^2/hbar`
                        #      con `c -> cs`, quindi `omega ∝ cs^2` e' NECESSARIA. Zero
                        #      parametri, zero floor, zero coefficienti. Misurato:
                        #      `omega_eff/omega_base = (cs/CS_M)^2` a 3.469e-18 (S3), e a
                        #      cs = CS_M il fattore vale 1.000000000000000 ESATTO (S3c).
                        #  (2) SIGILLATA CON CONTROLLO POSITIVO: S3.0 verifica che il test
                        #      VEDA (39/40 nodi con |f(1)-f(0)| > 1e-13) - senza, un sigillo
                        #      passerebbe anche su codice morto. E S2 e' la riduzione al
                        #      limite sul blob ATTUALE: ON (cs=CS_M) vs OFF byte-identico,
                        #      0.000e+00 con nodi 2924 = 2924 (il confronto ESISTE).
                        #      Sigillo: 9/10 + 1 FAIL ATTESO (S1, contro un blob di quattro
                        #      cambiamenti fa: mancanza di confronto, non identita').
                        #  (3) LA SUA ASSENZA E' UN DIFETTO, NON UN'ALTERNATIVA (Luca):
                        #      «un sistema in cui l'EM non risponde alla metrica e' un
                        #      sistema SBAGLIATO, non diverso». La fase U(1) EVOLVE gia'
                        #      senza Step 2: cio' che manca e' che RISPONDA alla curvatura,
                        #      ed e' proprio l'accoppiamento che in fisica c'e' sempre.
                        # CONSISTENZA TROVATA, non costruita: lo stesso esponente `cs^2`
                        # e' derivato INDIPENDENTEMENTE per l'inerzia (`inerzia ∝ cs^-2`,
                        # doc/INERZIA_tempo_quadro.md). Due strade, stesso esponente.
                        # RETROCESSIONE (scritta ORA, par.10): torna a flag se un riscontro
                        # COMMITTATO mostra che `_phc` NON e' una fase globale - cioe' se una
                        # firma di SPIN si muovesse per lo Step 2 oltre la dispersione fra
                        # semi. Oggi `_phc` moltiplica `a1` e `b1` per lo STESSO fattore
                        # (righe 2212-2213, uniche occorrenze) e il Bloch e' invariante (3.3e-16).
                        # DIAGNOSTICO per spegnerlo: `--senza-step2-orologio`.
                        # E' l'OROLOGIO DI COMPTON, omega = m c^2 / hbar: la frequenza propria di una
                        # massa va come c^2, e nel modello c e' cs. Quindi omega ∝ cs^2 non e' una
                        # manopola, e' fisica NECESSARIA e derivata: zero parametri nuovi, nessun
                        # floor, nessun coefficiente. A cs = CS_M il fattore vale ESATTAMENTE 1, quindi
                        # la riduzione al limite e' esatta per COSTRUZIONE e non per taratura.
                        # PERCHE' SERVE: la metrica legge solo |psi|^2 (cs = _cs_nodo) e l'orologio NON
                        # legge cs -> i due tempi propri (metrico tau_p = d/cs e orologio dt_n = DT*r)
                        # sono SCOLLEGATI. Questo e' l'unico aggancio lecito fra i due.
                        # DOVE AGISCE: su omega_clk, che entra in _phc come FASE GLOBALE per nodo. Il
                        # Bloch nb = psi^dag sigma psi e' INVARIANTE per fase globale (verificato:
                        # 3.3e-16), quindi lo Step 2 vive nel canale U(1)/orologio e NON PUO' muovere
                        # la direzione SU(2). Cambia pero' le fasi RELATIVE fra nodi, che entrano in
                        # Im<psi_i|psi_j>: la forza cambia e la traiettoria diverge (caos), ma non
                        # perche' abbia toccato lo spin.
                        # cs viene dal passo PRECEDENTE (self._cs_nodo_prev): l'orologio gira a :2691,
                        # il settore metrico a :2762. E' un ritardo di un passo, coerente col fatto che
                        # tutto il resto legge snapshot t-1. Senza cache -> CS_M -> fattore 1.
                        # Richiede --campo-spinoriale + --deparam-orologio (e' li' che _phc vive).
                        # Default off = byte-identico.
TAU_LUCE = False        # [FASE 2] IL RILASSAMENTO DI `omega_s` USA IL TEMPO-LUCE `d/cs` invece
                        # della densita'. Sostituisce SOLO la riga ~1913
                        # (`_tau = TAU_A*max(dens/dens_rif, 0.05)`) con `_tau = d_nodo/cs_nodo`,
                        # cioe' con `_tempo_luce_nodo()` - lo STESSO `tau` gia' cablato nello
                        # Strato 1. Default False = byte-identico.
                        # PERCHE', su TRE piani e non uno:
                        # 1. COERENZA DIMENSIONALE. `inerzia = |Psi|^2 = T^2 = (d/cs)^2`
                        #    (doc/INERZIA_tempo_quadro.md): il tempo che COSTRUISCE l'inerzia e
                        #    quello che la RILASSA devono essere LO STESSO. Oggi ce ne sono DUE
                        #    DIVERSI nella stessa equazione (riga 1918): `(d/cs)^2` al denominatore
                        #    della coppia e la DENSITA' nel termine dissipativo.
                        # 2. PRINCIPIO. `d/cs` e' il tempo-luce: un sistema NON PUO' RICORDARE PIU'
                        #    A LUNGO DI QUANTO IMPIEGHI A SAPERE DI SE'. E' esattamente la ragione
                        #    per cui `tau = d/cs` e' gia' nello Strato 1.
                        # 3. MISURA. `d/cs` e' PIATTO contro l'inerzia: pendenza +0.097 +- 0.0055
                        #    (IC95 [+0.086, +0.108], n=2195), contro +1.176 +- 0.019 della riga
                        #    attuale. Un `tau` piatto NON PUO' CANCELLARE il -1 della coppia, e la
                        #    cancellazione che produce l'esponente -0.11 si rompe
                        #    (doc/TAU_tempo_luce.md, doc/BARRE_ERRORE_pendenze.md).
                        # E LA RIGA CHE SOSTITUISCE E' SOSPETTA DUE VOLTE: non ha un principio che
                        # la imponga (scritta come ipotesi in assenza di parametri) E NON FA QUELLO
                        # CHE DICHIARA (scritta proporzionale a dens, misurata rho^1.81, perche'
                        # `dens_rif` e' la MEDIANA e il rapporto si auto-normalizza -> per il nodo
                        # mediano `tau` resta ancorato a TAU_A a qualunque densita').
                        # ZERO MANOPOLE: nessun coefficiente, nessun floor nuovo. `d`, `cs` e `LAM`
                        # esistono gia', e le guardie anti-zero sono quelle EREDITATE dallo Strato 1.
                        # ATTENZIONE A COSA NON FA: `|omega|_eq` va come `sqrt(tau)`, e `tau` passa
                        # da ~44 unita' di tempo a ~0.25, quindi il fattore e' ~1/13: da ~112 a ~9
                        # GIRI per passo. UN ORDINE DI GRANDEZZA NELLA DIREZIONE GIUSTA, **NON** la
                        # soluzione dell'aliasing. Non va venduto come cura.
                        # NON tocca la riga 1918 ne' la FORMA del termine dissipativo: se
                        # `-omega/tau` debba essere un allineamento LLG e' questione SEPARATA e
                        # aperta (par.1, un interruttore alla volta).
RUMORE_COLORATO = False # [2026-09-16] TAGLIO SPETTRALE DEL RUMORE DEL VUOTO. Il calcio termico
                        # (riga ~1908) e' `rng.normal` INDIPENDENTE a ogni passo, cioe' rumore
                        # BIANCO: banda infinita, energia iniettata a TUTTE le frequenze, incluse
                        # quelle che il passo non puo' risolvere, che aliasano per costruzione.
                        # IN NATURA NON ESISTE: ogni rumore fisico ha uno spettro con un taglio
                        # (e' la catastrofe ultravioletta in versione discreta).
                        # LA LEGGE: processo di Ornstein-Uhlenbeck sul rumore stesso,
                        #     xi(t) = xi(t-dt_n)*exp(-dt_n/tau_c) + sqrt(1-exp(-2 dt_n/tau_c))*g
                        # con `tau_c = LAM/CS_M` = IL TEMPO-LUCE DEL SOLITONE. DERIVATO, non
                        # scelto: LAM e CS_M sono gia' nel sistema. ZERO coefficienti nuovi.
                        # `amp` NON SI TOCCA.
                        # ATTENZIONE A COSA FA E COSA NON FA - misurato e scritto PRIMA, in
                        # doc/PREDIZIONE_taglio_spettrale.md:
                        #  * la ricorsione PRESERVA LA VARIANZA (b^2/(1-a^2) = 1.000000 analitico,
                        #    0.997330 simulato): cambia SOLO la struttura temporale del rumore,
                        #    NON la sua ampiezza. Il calcio per passo resta della stessa taglia,
                        #    ma i calci successivi sono CORRELATI su tau_c (= 40 passi).
                        #  * QUINDI NON ABBASSA `theta`, e se lo muove lo fa SALIRE (<=5%): una
                        #    forzante correlata fa crescere omega stocastico come n invece che
                        #    sqrt(n). Chi si aspetta un calo ha in mente un oggetto diverso (banda
                        #    limitata a densita' spettrale COSTANTE), che richiederebbe di
                        #    moltiplicare per sqrt(2*dt/tau_c), cioe' di toccare `amp`: manopola.
                        #  * e il canale su cui agisce e' gia' misurato MARGINALE: il rumore vale
                        #    R_stoc = 0.041 dell'incremento di omega, contro un errore atteso di
                        #    0.097 (doc/TRACING_omega.md). E muove il Bloch fra lo 0.02% e lo
                        #    0.22% (il resto lo muove omega).
                        # SI CABLA PERCHE' IL RUMORE BIANCO E' FISICAMENTE SBAGLIATO, non perche'
                        # si aspetti che risolva l'aliasing. Aspettarsi che NON cambi i numeri e'
                        # parte della predizione, non una scusa dopo.
                        # IL `dt` E' `dt_n = DT*r`, NON `DT`: il rumore e' un processo LOCALE del
                        # nodo, e DT nudo imporrebbe la foliazione sincrona globale, cioe' un
                        # frame preferito (par.9). E' l'errore gia' preso nello Strato 1, che
                        # S1..S6 passavano IDENTICI e solo S7 ha stanato.
                        # STATO: `_xi_rumore`, per nodo, ereditato alla mitosi con la STESSA
                        # convenzione di _nb/_nb_prec/_nb_ret/omega_s/_psi_spinor/_psi_prec/
                        # _cs_nodo_prev/_psi_spin_prec. Inizializzato da N(0,1), cioe' DALLA
                        # DISTRIBUZIONE STAZIONARIA: zero transitorio, zero parametri.
                        # NB: agisce solo sul percorso VIVO (`not SYNC_UPDATE`). Sotto
                        # SYNC_UPDATE il flag e' INERTE, e lo dichiara a voce.
GAMMA_TURBO = 1.0       # [DIAGNOSTICO, NON PERCORSO CERTIFICATO] amplificatore della SENSIBILITA'
                        # DI cs ALLA DENSITA'. Dentro `_cs_nodo` si usa GAMMA*GAMMA_TURBO al posto
                        # di GAMMA; OVUNQUE ALTROVE GAMMA resta ORIGINALE. Default 1.0 = nessun
                        # effetto = byte-identico.
                        # PERCHE' ESISTE: alle densita' attuali cs e' MORTO (I~0.05 contro la soglia
                        # ~1/GAMMA^2 ~ 400), quindi cs ~ CS_M costante e ogni test cs-dipendente e'
                        # nullo. Il turbo abbassa la soglia cosi' che cs si svegli a densita'
                        # RAGGIUNGIBILI. Non aggiunge fisica: accelera un meccanismo che ESISTE
                        # (cs = cs(rho)) e che e' spento SOLO dalla scala.
                        # PERCHE' RISTRETTO: GAMMA e' UN parametro fisico CONDIVISO fra cs (:2354),
                        # la saturazione scalare `satura()` e la saturazione del campo SPINORIALE
                        # (psi_spin = _Fs/(1+GAMMA*norm)). Turboarlo globalmente cambierebbe la
                        # DINAMICA DEL CAMPO, non la sensibilita' di cs, e il risultato sarebbe
                        # INATTRIBUIBILE (il braccio di controllo Step2 ON/OFF non lo isolerebbe:
                        # entrambi avrebbero il campo alterato allo stesso modo).
                        # ONESTA' (da tenere nella lettura): restringendo si ROMPE DI PROPOSITO la
                        # condivisione di GAMMA. Quindi il turbo ristretto e' un ISOLAMENTO
                        # DIAGNOSTICO, **non** il regime reale ad alta densita' — dove, con GAMMA
                        # condiviso, cambierebbero ENTRAMBI. Un esito positivo va letto come
                        # "il gradiente di cs, IN ISOLAMENTO, retroagisce sullo spin": un
                        # CONDIZIONALE, non un'affermazione sul regime reale.
                        # NB: `:5318` (diaglog) RE-IMPLEMENTA cs inline e NON chiama `_cs_nodo`:
                        # sotto turbo quella colonna riporta il cs NON turboato. Non usarla.
                        # Richiede --cs-dinamico (senza, cs = CS_M costante e K non morde).
SPIN_FEEDBACK = True    # FEEDBACK LOCALE SPINORE->ARCHI: usa l'overlap complesso dei lift sugli archi
                        # come flusso di fase antisimmetrico. Il braccio OFF e' --senza-spin-feedback.
                        # ⚠ ON DI DEFAULT dal 2026-09-18, PER DECISIONE DI LUCA E SU BASI DI FORMA,
                        # NON perche' una misura lo abbia mostrato migliore. La distinzione va tenuta:
                        # l'A/B a QUATTRO SEMI (`doc/REFERTO_semi_spin_feedback.md`) NON ha mostrato
                        # effetto -- delta nodi media -6.25, SD fra semi 37.84, IC95 +-60.2, e il
                        # segno NON era concorde (+31 / 0 / +3 / -59).
                        # LE BASI DI FORMA, quelle si' misurate:
                        #   - il cricchetto e' CURATO: antisimmetria da 1.112 a 6.5e-16, QUINDICI
                        #     ordini, con due conferme indipendenti (|sum(ceduto)+sum(ricevuto)| =
                        #     0.000e+00; imag<i|j>+imag<j|i> = 2.2e-16);
                        #   - G6: LA FASE E' CUCITA -- `imag(ov)` e' CONTINUO fra passi consecutivi
                        #     (cambi di segno 0.0035 contro un NULLO di 0.50): e' una CORRENTE
                        #     orientata vera, non rumore di gauge. Nessuno l'aveva mai verificato;
                        #   - il sigillo esiste: 12/12 (`csv/_seal_fork/_sigillo_denominatore.txt`).
                        # E LA RAGIONE FISICA: un settore che evolve e da' il tempo ma non retroagisce
                        # sulla geometria e' un motore acceso con la trasmissione staccata -- ed e'
                        # l'unica trasmissione staccata senza una ragione sostanziale (TW_SPINORE ha
                        # un difetto MISURATO; CHI_DA_SPINORE spegnerebbe CHI_BASC, che e' sana).
                        # ⚠⚠ PREREQUISITO, E NON E' AUTOMATICO: richiede SPINORE_VIVO **e** SPINORE.
                        # `SPINORE_VIVO` e' False di default, quindi in un run che non passa
                        # --spinore-vivo questo flag e' ACCESO MA INERTE. Non in silenzio: l'avviso
                        # e' a `_applica_flag` (cerca "[spin-feedback]").
                        # REGOLA DI CONDOTTA (Luca, 2026-09-18): se un problema emerge col feedback
                        # attivo, NON si spegne il feedback -- si isola, si misura, si corregge la
                        # causa. Spegnerlo sarebbe curare il sintomo nascondendo la fisica.
                        # CRITERIO DI RETROCESSIONE (par.10, scritto ORA e non dopo): torna a OFF di
                        # default solo con un riscontro COMMITTATO che mostri un difetto DEL TERMINE
                        # -- non con un run che va male, e non per ripensamento.
SPIN_POSITIVI = False   # MISURA DELLO SPINORE DI GRUPPO POSITIVO: seleziona perc_chi=+1 solo nella
                        # diagnostica per-massa. Non modifica la dinamica dei solitoni.
CHI_CORE = False        # CHIRALITA' DEL CORE LOCALE: il segno emerge da tutti i nodi sopra
                        # soglia del core; default off per A/B, nessun segno selezionato a priori.
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
                        # [MAX-NODI-FERMA, 2026-09-28] E ORA IL CODICE FA CIO' CHE QUESTO
                        # COMMENTO DICEVA GIA': quando `MAX_NODI` morde, il run SI FERMA con
                        # `LimiteNodiSuperato`. Prima troncava e continuava -- tre siti che
                        # cambiavano la FISICA in silenzio (`A8`). Si cambia con `--maxnodi`,
                        # e il controllo e' UNO: `_ferma_se_oltre_max_nodi`.
                        # ⚠ NON E' UN TETTO FISICO (`A11`): non protegge da un errore di
                        # fisica, protegge la RAM -- e in futuro VA ELIMINATO.
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
        # LIFT COMPLESSO del Bloch: non aggiunge gradi di liberta'. Conserva la scelta di fase
        # del rappresentante spinoriale fra due passi; senza questo trasporto il Bloch perde il
        # segno psi <-> -psi. Viene attivato solo da SPINORE_VIVO.
        self._spinor_lift = np.zeros((0, 2), complex)
        # SPINORE PRIMARIO COMPLESSO (--spinore-corretto): n x 2 in SU(2). Quando attivo e' la
        # variabile FISICA primaria (orologio proprio de Broglie + precessione), e il Bloch _nb
        # ne e' la PROIEZIONE (nb = psi^dag sigma psi). Vuoto = inattivo (path storico: _nb primario).
        self._psi_spinor = np.zeros((0, 2), complex)
        # [FORK SU(2) - STRATO 1] BLOCH RITARDATO per nodo, n(t-tau): il PASSATO da cui nasce la
        # connessione quando FORK_SU2_MEM e' attivo. None = non ancora nato (al primo passo viene
        # inizializzato al Bloch corrente: non c'e' ancora passato, quindi nessun effetto).
        self._nb_ret = None
        # cs del passo PRECEDENTE, cachato per tau = d/cs: la coppia gira PRIMA del settore metrico,
        # quindi il cs del passo corrente non esiste ancora quando serve. E' un RITARDO: va bene.
        self._cs_nodo_prev = None
        # contatori del FALLBACK cs = CS_M in _tempo_luce_nodo (diagnostici, mai letti dalla fisica).
        self._cs_chiamate = 0
        self._cs_fallback = 0
        self._cs_fallback_ultimo = None
        # [CURA DELL'ANELLO ISTANTANEO, 2026-09-18] il gauge di `ritmo()` del passo PRECEDENTE (uno
        # SCALARE: niente lunghezza, niente estensione alla mitosi, A8b chiusa per costruzione).
        # Nasce DICHIARATO a None, non implicito (A7b: uno stato non nasce indefinito); `_med_f_ultimo`
        # e' il registro che `ritmo()` scrive e che SOLO `step()` promuove.
        self._med_f_prec = None
        self._med_f_ultimo = None
        # ritmo del tempo proprio locale del passo corrente (None = orologio globale), esposto da
        # step() perche' il rilassamento della memoria si misuri in dt_n = DT*r e non nel tic globale.
        self._r_corrente = None
        # PROFILO DI PERCORRENZA (struttura a nastro delle specifiche originali).
        # Ogni solitone e' una sinusoide che, percorsa lungo il suo profilo, esegue
        # un salto NETTO di 180 gradi (pi) nel punto d'incrocio con l'asse al mediano.
        # Il verso di percorrenza (+1/-1) da' le due ANTICHIRALITA': percorrere l'onda
        # in un verso torce di +pi, nell'altro di -pi. 'perc_chi' e' il verso; 'perc_tw'
        # e' lo stato del mezzo-twist (0 = prima del mediano, pi = dopo il salto).
        # Introdotto DORMIENTE: non accoppiato ancora a Psi ne' alla dinamica, finche'
        # non e' verificato che la struttura non rompe le leggi esistenti.
        self.perc_chi = np.zeros(0, int)     # verso di percorrenza / antichiralita' (+1/-1) = CARICA
        # [CHI_COOP] LA GEOMETRIA, separata dalla carica: "il giro e' compiuto o no", scritta da
        # `chi_basc` dalla torsione locale. A flag spento NESSUNO la legge (byte-inerte), ma viene
        # ESTESA sempre dalle tre vie di crescita, cosi' `len(perc_geom) == n` e' un'INVARIANTE e non
        # una speranza (Z4). Finisce nello snapshot da se': `salva_stato` accetta gli ndarray di
        # __dict__ -- verificato dal disco, non assunto.
        self.perc_geom = np.zeros(0, int)    # [CHI_COOP] geometria: giro compiuto o no (+1/-1)
        self.perc_tw  = np.zeros(0)          # stato del salto di pi al mediano (0 o pi)
        self.i = np.zeros(0, int); self.j = np.zeros(0, int)
        self.d = np.zeros(0); self.d0 = np.zeros(0); self.vd = np.zeros(0)
        self.peq = np.zeros(0); self.tw = np.zeros(0); self.twp = np.zeros(0)
        # [(3) BONIFICA 2026-09-17] MEMORIA DELLA REPULSIONE, per ARCO. Vedi `mitosi()`.
        # Nasce a 0: un arco appena creato non ha storia repulsiva. (NB: NON e' il pattern di
        # `peq`, che nasce NaN perche' va CALIBRATO sul campo; qui lo zero e' il valore giusto,
        # non un segnaposto.)
        self._rep = np.zeros(0)
        self._sin2_vir = None                 # memoria per-arco della quota tangenziale della viriale (freno anisotropo)
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
        self._cicli_topologici = None
        self._costruisci_struttura()

    def _base_cicli_topologici(self, massimo=256):
        """Costruisce una base di cicli fondamentali usando SOLO la topologia.
        Non legge pos, d, embedding o coordinate: ogni ciclo e' una sequenza di
        (indice_arco, verso). La cache viene invalidata da _grado() quando cambia
        la topologia. Il limite serve solo a mantenere la diagnostica leggera."""
        if getattr(self, "_cicli_topologici", None) is not None:
            return self._cicli_topologici
        n = self.n
        archi = [(e, int(a), int(b)) for e, (a, b) in enumerate(zip(self.i, self.j))
             if a < n and b < n and a != b]
        adiacenza = [[] for _ in range(n)]
        for e, (_, a, b) in enumerate(archi):
            adiacenza[a].append((b, e)); adiacenza[b].append((a, e))
        visitato = np.zeros(n, bool); parent = np.full(n, -1, int)
        parent_e = np.full(n, -1, int); profondita = np.zeros(n, int)
        alberi = set()
        for radice in range(n):
            if visitato[radice]: continue
            visitato[radice] = True; pila = [radice]
            while pila:
                u = pila.pop()
                for v, e in adiacenza[u]:
                    if not visitato[v]:
                        visitato[v] = True; parent[v] = u; parent_e[v] = e
                        profondita[v] = profondita[u] + 1; alberi.add(e); pila.append(v)
        def verso(e, u, v):
            _, a, b = archi[e]
            return 1 if (a == u and b == v) else -1
        cicli = []
        for e, (_, u, v) in enumerate(archi):
            if e in alberi: continue
            pu = []; x = u
            while x >= 0:
                pu.append(x); x = parent[x]
            pv = []; x = v
            while x >= 0:
                pv.append(x); x = parent[x]
            comuni = set(pu); lca = next((x for x in pv if x in comuni), None)
            if lca is None: continue
            ciclo = [(archi[e][0], 1)]  # chiusura v -> u: orientamento i -> j
            x = u
            while x != lca and x >= 0:
                y, pe = parent[x], parent_e[x]
                ciclo.append((archi[pe][0], verso(pe, x, y))); x = y
            ramo = []; x = v
            while x != lca and x >= 0:
                y, pe = parent[x], parent_e[x]
                ramo.append((archi[pe][0], verso(pe, y, x))); x = y
            ciclo.extend(reversed(ramo))
            if len(ciclo) > 2:
                cicli.append(ciclo)
                if len(cicli) >= massimo: break
        self._cicli_topologici = cicli
        return cicli

    def _vertici_ciclo(self, ciclo):
        """Ricostruisce la sequenza ORDINATA dei nodi di un ciclo fondamentale
        (che e' un ciclo semplice: ogni nodo ha grado 2 al suo interno) a partire
        dalla lista di archi (indice, verso). Serve alle misure che vivono sui
        nodi in ordine ciclico (fase di Berry spinoriale). Nessuna coordinata."""
        archi = [(int(self.i[e]), int(self.j[e])) for e, _ in ciclo]
        adj = {}
        for a, b in archi:
            adj.setdefault(a, []).append(b); adj.setdefault(b, []).append(a)
        if any(len(v) != 2 for v in adj.values()):
            return None  # non e' un ciclo semplice: la fase di Berry non e' definita
        start = archi[0][0]; seq = [start]; prev = None; cur = start
        for _ in range(len(archi)):
            n0, n1 = adj[cur]
            nxt = n0 if n0 != prev else n1
            prev, cur = cur, nxt; seq.append(cur)
        return seq[:-1] if seq[-1] == start else None

    def _aggiorna_lift_spinoriale(self, nb_precedente=None):
        """Ricava e trasporta il lift complesso del vettore di Bloch.

        Il rappresentante canonico viene corretto con la fase dell'overlap col passo precedente,
        cosi' l'overlap consecutivo e' reale positivo. Questo conserva il lift lungo la storia
        senza introdurre una dinamica indipendente: il Bloch resta la variabile fisica.
        Non definisce da solo una cucitura spaziale Möbiusiana; rende pero' misurabile il segno
        globale del lift quando una traiettoria compie un giro di 2pi.
        """
        if not hasattr(self, "_nb") or self._nb is None or len(self._nb) < self.n:
            return
        nb = np.asarray(self._nb[:self.n], float)
        th = np.arccos(np.clip(nb[:, 2], -1.0, 1.0))
        ph = np.arctan2(nb[:, 1], nb[:, 0])
        candidato = np.stack([np.cos(th / 2.0), np.sin(th / 2.0) * np.exp(1j * ph)], axis=1)
        precedente = self._spinor_lift
        if nb_precedente is not None and len(precedente) == 0:
            precedente = np.asarray(nb_precedente)
        n_comuni = min(len(precedente), self.n)
        if n_comuni:
            overlap = np.sum(np.conj(precedente[:n_comuni]) * candidato[:n_comuni], axis=1)
            fase = np.ones(n_comuni, complex)
            validi = np.abs(overlap) > 1e-12
            fase[validi] = np.exp(-1j * np.angle(overlap[validi]))
            candidato[:n_comuni] = candidato[:n_comuni] * fase[:, None]
        self._spinor_lift = candidato

    @staticmethod
    def _bloch_a_spinore(nb):
        """Rappresentante canonico complesso di un vettore di Bloch: a=cos(th/2), b=sin(th/2)e^{i ph}."""
        nb = np.asarray(nb, float).reshape(-1, 3)
        th = np.arccos(np.clip(nb[:, 2], -1.0, 1.0))
        ph = np.arctan2(nb[:, 1], nb[:, 0])
        return np.stack([np.cos(th / 2.0), np.sin(th / 2.0) * np.exp(1j * ph)], axis=1)

    @staticmethod
    def _link_su2_N(nb_i, nb_j):
        """[FORK SU(2) - PEZZO 1/2, rifattorizzato] Trasporto parallelo NON normalizzato sull'arco
        i->j. E' la PRIMITIVA usata dalla FORZA:

            N_ij = (1 + n_i.n_j) I + i (n_i x n_j).sigma

        POLINOMIALE nei Bloch: niente arccos, niente asse da normalizzare, niente floor, nessun
        caso degenere da trattare a mano. A chi=pi il prodotto scalare vale -1 e il vettoriale 0,
        quindi N = 0 da solo: l'arco si spegne senza che nessuno inventi una direzione.

        Identita' (sigillata, csv/_seal_fork/_sigillo_N.py):  N_ij = 2 cos(chi/2) U_ij
        dove U_ij e' la connessione di Berry unitaria. Quindi N porta con se' un PESO:

            |N|/2 = cos(chi/2) = |<n_i|n_j>|   = OVERLAP DI SPIN dei due solitoni

        Il peso NON e' scelto: e' cio' che resta quando non si normalizza, ed e' l'accoppiamento
        fisico fra i due spin. Vale 1 ad allineati (canale di fase / EM PRESERVATO, riduzione
        esatta allo scalare), 0.707 a 90 gradi, 0 ad antipodali. ZERO MANOPOLE (par.3).
        NB: e' l'overlap-AMPIEZZA. La forza e' Im<psi_i|N|psi_j>, cioe' un'ampiezza: va pesata con
        un'ampiezza. L'overlap-PROBABILITA' cos^2(chi/2) (regola di Born) conterebbe due volte.

        USO NELLA FORZA:  Im<psi_i|psi_j>  ->  Im<psi_i| N_ij/2 |psi_j>
        Il /2 e' la normalizzazione che rende N/2 = I ad allineati (riduzione allo scalare ESATTA).

        N_ji = N_ij^dag ESATTAMENTE (polinomiale, nessun arrotondamento): l'azione-reazione e'
        esatta. Attenzione all'ORIENTAMENTO: con gli scalari era irrilevante, ora CONTA.
        VERSO: N_ij trasporta n_j -> n_i, il verso giusto per Im<psi_i| N_ij |psi_j>.

        PURE-READ: non legge ne' scrive stato dell'oggetto, non consuma `net.rng`."""
        ni = np.asarray(nb_i, float).reshape(-1, 3)
        nj = np.asarray(nb_j, float).reshape(-1, 3)
        d = np.sum(ni * nj, axis=1)
        c = np.cross(ni, nj)
        N = np.empty((len(ni), 2, 2), dtype=complex)
        N[:, 0, 0] = (1.0 + d) + 1j * c[:, 2]
        N[:, 0, 1] = 1j * c[:, 0] + c[:, 1]
        N[:, 1, 0] = 1j * c[:, 0] - c[:, 1]
        N[:, 1, 1] = (1.0 + d) - 1j * c[:, 2]
        return N

    @staticmethod
    def _link_su2(nb_i, nb_j):
        """[FORK SU(2)] Connessione di Berry UNITARIA U_ij e peso w, ricavati da `_link_su2_N`.

            U_ij = N_ij / sqrt(det N_ij) = exp(-i (chi/2) m_hat.sigma)   [SU(2), det=1]
            w    = sqrt(det N_ij)/2     = cos(chi/2) = |<n_i|n_j>|       [overlap di spin]

        DESTINAZIONE D'USO — "due oggetti, due usi" (presidio di Luca):
          * la FORZA usa `_link_su2_N` (N/2): polinomiale, nessuna radice, nessun caso degenere;
          * l'OLONOMIA di plaquette (diagnostico PURE-READ) usa U, che richiede la rotazione pura
            perche' Tr(U_ij U_jk U_ki) sia l'invariante atteso. La radice quadrata vive SOLO qui.
        Su un ciclo chiuso il peso fattorizza come scalare POSITIVO, quindi la FASE dell'olonomia
        e' la stessa con N o con U: cambia solo l'ampiezza (sigillato, P2c).

        CASO DEGENERE (l'unico rimasto, e vive SOLO in questo ramo): ad antipodali esatti N=0 e
        det N=0, quindi U = 0/0 e' indefinita — non esiste una rotazione che porti n_j su -n_j.
        Li' si pone U := I (unitaria) e w = 0, cosi' il peso spegne comunque l'arco. La forza non
        passa da qui, quindi non eredita ne' il caso speciale ne' la soglia.

        STORIA (non ripetere l'errore): fino al 2026-09-13 questa funzione costruiva U via arccos +
        asse normalizzato e restituiva w = sin(chi). Quel peso SOVRA-CORREGGEVA: si annullava anche
        ad allineati, dove l'indeterminatezza dell'asse e' INNOCUA (sin(chi/2)=0 uccide gia' il
        termine dell'asse, U=I qualunque sia m_hat), e cosi' spegneva il canale di fase (EM).
        Misure e delibera: csv/_seal_fork/_sigillo_pezzo2.py, _sigillo_pesi.py, _sigillo_N.py.

        PURE-READ: non legge ne' scrive stato dell'oggetto, non consuma `net.rng`."""
        N = Rete._link_su2_N(nb_i, nb_j)
        detN = np.real(N[:, 0, 0] * N[:, 1, 1] - N[:, 0, 1] * N[:, 1, 0])
        rad = np.sqrt(np.maximum(detN, 0.0))
        w = rad / 2.0                              # = cos(chi/2) = |<n_i|n_j>|
        U = N / np.maximum(rad, 1e-30)[:, None, None]
        degenere = rad <= 0.0                      # antipodali esatti: U indefinita -> I, w gia' 0
        if np.any(degenere):
            U[degenere] = np.eye(2, dtype=complex)
        return U, w

    def _estendi_psi_spinor(self, n, nb_rif):
        """Garantisce len(_psi_spinor)==n SENZA reset spurio (regola D). I nuovi indici (non gia'
        ereditati dalla mitosi) si inizializzano dal Bloch corrente nb_rif (init da Bloch attuale)."""
        cur = getattr(self, "_psi_spinor", None)
        if cur is None or len(cur) == 0:
            self._psi_spinor = self._bloch_a_spinore(nb_rif[:n])
        elif len(cur) < n:
            manca = self._bloch_a_spinore(nb_rif[len(cur):n])
            self._psi_spinor = np.vstack([cur, manca])
        elif len(cur) > n:
            self._psi_spinor = cur[:n]

    # =====================================================================
    # ### QUI STAVANO `_eredita_psi_figli` E `_eredita_spinore_figli`.
    # ### SONO ASSORBITE DAL PUNTO UNICO DI NASCITA (`COMMIT 3`, 2026-10-02).
    # =====================================================================
    # Le loro **13 grandezze** sono ora righe di `REGOLE_NASCITA`, in testa al file:
    #   `_cs_nodo_prev` `_nb` `_nb_prec` `_nb_ret` `_psi_prec` `_psi_spin_prec`
    #   `_psi_spinor` `_spinor_lift` `omega_s` `psi` `psi_spin` `rho_spin`
    #
    # ### IL RIORDINO NON LE BUTTA: le ASSORBE -- e la ragione per cui esistevano
    #   *(le cure `C7`/`C11`/`PSI-FLASH`)* vive nella `derivazione` di ciascuna
    #   regola, che e' il posto dove chi legge quella grandezza la trova.
    #
    # ⚠ **E DUE COSE NON OVVIE SONO CONSERVATE LI', non perse:**
    #   ① `_nb_prec` era estesa **SOLO DENTRO il ramo di `_nb`** -- una dipendenza
    #     di **CONTROLLO**, non di dato, che nessun grafo sui dati vedrebbe. Ora
    #     passa per `c["_nb_esteso"]`;
    #   ② `_cs_nodo_prev` concatena `_csp` **INTERO**, non `_csp[:n0]` come fa `psi`:
    #     due convenzioni diverse nella stessa funzione, e si conservano tali.
    #
    # ### E `n0` NON SI CALCOLA PIU' QUI: arriva da `c["n0"]`, catturato nella
    #   PREPARAZIONE. Prima era `n0 = self.n - k`, cioe' una lettura di `self.n`
    #   -- una `@property` su `len(self.phi)` -- **A META' DELLA NASCITA**:
    #   misurato da `csv/_test_fork/_ordine_registro.py` come vincolo 3 del
    #   contratto dell'ordine.
    #
    # 📌 Alcuni commenti e docstring altrove nel file le nominano ancora, e li'
    #   la citazione e' **storica**: descrivono da quale cura una regola nasce.
    #   Il loro posto di oggi e' `REGOLE_NASCITA`.
    # =====================================================================
        # [CORREZIONE DI DIFETTO, 2026-09-16 - decisione di Luca] `_xi_rumore` **NON SI EREDITA**,
        # e qui non c'e' nessun codice apposta: il figlio riceve un `xi` FRESCO dal ramo di
        # estensione di `_passo_spinoriale`, che estrae dalla distribuzione stazionaria.
        # PERCHE' L'EREDITA' ERA SBAGLIATA, e l'analogia che avevo usato era MIA ed era falsa:
        # `_nb`, `_nb_prec`, `_nb_ret`, `omega_s`, `_psi_spinor`, `_psi_prec`, `_cs_nodo_prev`,
        # `_psi_spin_prec` sono **PROPRIETA' DEL NODO**: e' giusto che il figlio le erediti.
        # `xi` NO: e' un campione dell'AMBIENTE che spintona il nodo, un processo ESTERNO.
        # Due nodi distinti NON ricevono lo stesso identico spintone. Ereditandolo, padre e figlio
        # avevano rumore CORRELATO AL 100 % per ~40 passi (tau_c = LAM/CS_M) - una correlazione
        # SPURIA fra oggetti che devono essere indipendenti, e per giunta proprio nella grandezza
        # che serve a DECORRELARE.
        # Nessun feedback sul padre: il rumore non e' una quantita' che si ripartisce.

    def olonomia_lift_ciclo(self, ciclo):
        """Misura il prodotto ciclico degli overlap del lift complesso trasportato."""
        if len(self._spinor_lift) < self.n:
            return 1.0 + 0.0j
        seq = self._vertici_ciclo(ciclo)
        if seq is None or len(seq) < 3:
            return 1.0 + 0.0j
        s = self._spinor_lift[seq]
        overlap = np.sum(np.conj(s) * np.roll(s, -1, axis=0), axis=1)
        return complex(np.prod(overlap))

    def _feedback_spinoriale_archi(self, i, j, w):
        """Trasforma l'overlap spinoriale locale in uno SCAMBIO antisimmetrico SULL'ARCO.

        La parte immaginaria dell'overlap normalizzato e' un flusso orientato sull'arco;
        il modulo pesa la coerenza. Cio' che `i` cede, `j` riceve: ESATTAMENTE, senza
        denominatori in mezzo. E' una legge sperimentale separata, default off.

        ⚠ IL DOCSTRING PRECEDENTE DICEVA DUE COSE, ED ERANO SMENTITE DALLA MISURA (2026-09-17,
        `doc/REFERTO_denominatore.md`, `csv/_test_fork/_scelta_denominatore.txt`):
          - «coppia ANTISIMMETRICA ai nodi» -> **era FALSO**: `|sum(out)|/max|out|` valeva
            **mediana 1.112, MAX 8.441**, quando l'errore macchina e' ~1e-16. Il termine
            INIETTAVA coppia netta nel sistema;
          - «la divisione per il grado pesato non introduce una manopola» -> **era VERO, ed era
            ESATTAMENTE LA RAGIONE per cui la prima frase era falsa**: `out[i] -= f/grado[i]` e
            `out[j] += f/grado[j]` hanno DENOMINATORI DIVERSI, quindi la somma vale
            `f*(1/g_j - 1/g_i)`, zero solo se i gradi coincidono. Su un grafo di grado
            disomogeneo -- cioe' questo -- non coincidono mai.
        Il verso dell'iniezione dipendeva dalla DISOMOGENEITA' DEI GRADI, cioe' da una proprieta'
        della TOPOLOGIA, non della fisica dello spin: il cricchetto che A7 esclude.

        PERCHE' NESSUN DENOMINATORE, e non uno simmetrico (scelta del 2026-09-17, misurata):
          - `w` e' ESCLUSO: `flusso = w*imag(ov)`, dividere per `w` lo CANCELLA;
          - `(g_i+g_j)/2` e `g_i+g_j-2w` ripristinano l'antisimmetria ESATTAMENTE quanto il non
            averne (tutti e tre a ~1e-16): il criterio di correttezza NON discrimina;
          - restano A1 e par.3: **nessun denominatore ha ZERO SCELTE**, gli altri sono una
            scelta fra forme equivalenti.

        ⚠⚠ CORREZIONE DEL 2026-09-18, E CAMBIA UNA RAGIONE DI QUESTA SCELTA. Qui era scritto che
        la domanda «|out| cresce col grado?» NON AVEVA RISOLUZIONE, perche' «il ~77 % dei nodi ha
        grado 2». **ERA UN ERRORE DI POPOLAZIONE (A3), fatto sul mio stesso conteggio:** il 1018
        era su **5410** nodi-istanza e l'avevo diviso per 1318, la somma delle SOLE colonne
        stampate (gradi 2..9). La distribuzione vera e' **BIMODALE**: grado 2 = **19.85 %**,
        grado >= 100 = **65.57 %**, mediana **119**. La misura aveva eccome risoluzione.
        **RIFATTA SUL RANGE GIUSTO** (`doc/REFERTO_Z24.md`), `|out|` a `g=2` contro `g>=100`:
            attuale (pre-cura)  0.0489 -> 0.0483   rapporto 0.989   pendenza -0.003  INTENSIVA
            nudo   (cablata)    0.0017 -> 0.0613   rapporto 36.2    pendenza +0.878  ESTENSIVA
            media               0.0023 -> 0.0441   rapporto 18.9    pendenza +0.719  ESTENSIVA
            linea               0.0014 -> 0.0231   rapporto 16.9    pendenza +0.691  ESTENSIVA
        **Il vecchio `/grado` rendeva `out` INTENSIVA davvero, e nessuna cura lo fa.**
        **CONSERVAZIONE E INTENSIVITA' SONO IN CONFLITTO DIRETTO, per ragione algebrica:**
        `sum(out) = 0` richiede un denominatore SIMMETRICO SULL'ARCO; l'indipendenza dal grado
        richiede il denominatore DEL NODO CHE RICEVE. **Non possono valere insieme.** Il vecchio
        codice sceglieva la seconda ROMPENDO la prima, e non lo diceva.
        **La cura resta giusta su cio' che ripara** — un cricchetto e' una violazione di A7, non
        una scelta di modello — **ma il suo costo NON era «non misurabile»: e' misurato, ed e'
        grande** (ai neonati `|out|` scende di un fattore 29).
          - E l'ampiezza NON esplode: misurato `|out|` mediano **0.0400 -> 0.0223**,
            `max|out|` **0.816 -> 0.590**. E' PIU' PICCOLO di prima.

        ⚠ COSA QUESTA CURA **NON** FA: `out[k]` resta una SOMMA su un numero di termini che
        cresce col grado. Se questo sia un difetto **non e' stato misurabile** (vedi sopra):
        e' un fronte APERTO, non una cosa risolta.
        ⚠ E LO STESSO SCHEMA E' IN ALMENO TRE ALTRI PUNTI -- `:2082` (`B`), `:2294` (`_otw`),
        `:3154` (twist) -- **non toccati e non misurati**: fronte separato.
        """
        out = np.zeros(self.n)
        self._spin_feedback_last = 0.0
        # [A8 - ESPERIMENTO SPIN_FEEDBACK, 2026-09-17] SOLO CONTATORI, nessuna logica toccata.
        # Le DUE guardie qui sotto escono restituendo ZERO: se scattassero, il feedback sarebbe
        # INERTE IN SILENZIO e l'esperimento sarebbe nullo senza che nulla lo segnali. La seconda
        # (`len(_spinor_lift) < n`) e' la stessa famiglia di `_psi_spin_prec`, che fu inerte nel
        # 95.33 % delle chiamate per mesi.
        self._sfb_chiamate = getattr(self, "_sfb_chiamate", 0) + 1
        if not SPIN_FEEDBACK:
            self._sfb_off = getattr(self, "_sfb_off", 0) + 1
            return out
        if len(self._spinor_lift) < self.n:
            self._sfb_lift_corto = getattr(self, "_sfb_lift_corto", 0) + 1
            self._sfb_lift_shape = (len(self._spinor_lift), self.n)
            return out
        mask = (i < self.n) & (j < self.n)
        if not mask.any():
            self._sfb_mask_vuota = getattr(self, "_sfb_mask_vuota", 0) + 1
            return out
        self._sfb_applicato = getattr(self, "_sfb_applicato", 0) + 1
        ii, jj, ww = i[mask], j[mask], w[mask]
        ov = np.sum(np.conj(self._spinor_lift[ii]) * self._spinor_lift[jj], axis=1)
        flusso = ww * np.imag(ov)
        # [CURA DEL DENOMINATORE, 2026-09-17] LO SCAMBIO SULL'ARCO E' ESATTO: cio' che `i` cede e'
        # cio' che `j` riceve, senza nulla in mezzo. `imag(<psi_i|psi_j>) = -imag(<psi_j|psi_i>)`
        # e' antisimmetrico PER COSTRUZIONE: la legge era giusta, era la divisione ad averla rotta.
        # Il calcolo di `grado` e' stato RIMOSSO perche' diventerebbe codice morto (la famiglia di
        # `spin_locale`), non perche' fosse sbagliato calcolarlo.
        np.add.at(out, ii, -flusso)
        np.add.at(out, jj, flusso)
        self._spin_feedback_last = float(np.mean(np.abs(flusso))) if len(flusso) else 0.0
        return out

    def chiralita_core_locale(self, sorgente=None, geom=False):
        """Calcola la chiralità emergente del core locale per ogni nodo.

        [CHI_COOP, 2026-09-21] LA FONTE ERA UNICA PER DUE PADRONI. Questa funzione e' chiamata
        sia dalla CATENA DELLA TORSIONE (FRAME_DRAG, e la cache letta da TORS_4PI) sia dal CAMPO
        `B` del passo spinoriale: dirottarla su `perc_geom` avrebbe portato sulla geometria ANCHE
        il campo dello spinore, che invece dev'essere generato dalle CARICHE. Percio' l'array
        arriva come ARGOMENTO.
          `sorgente is None` -> `self.perc_chi`  (LEGACY: byte-identico, il caso di CHI_COOP off)
          `geom=False`       -> scrive `_chi_core_nodi` + i tre diagnostici   (LEGACY)
          `geom=True`        -> scrive `_chi_geom_nodi`, e SOLO quella        (solo con CHI_COOP)
        LA CACHE LA SCRIVE IL RAMO CHE LA POSSIEDE, ed e' il punto delicato: l'ordine dentro
        `step()` e' FRAME_DRAG -> `_passo_spinoriale` -> TORS_4PI, quindi TORS_4PI legge la cache
        scritta PER ULTIMA, cioe' quella del passo spinoriale. Con una cache sola riceverebbe la
        CARICA in silenzio: nessun errore, nessun NaN, solo l'array sbagliato.
        I TRE DIAGNOSTICI (`_chi_core_rho0`, `_chi_core_rhoc`, `_chi_core_raggio`) NON dipendono
        da `chi`: sono calcolati da `I2` e da `lam_loc`. Verificato dal codice, non assunto --
        percio' il ramo `geom` non li riscrive, e il loro valore non cambia."""
        self._g_ccl_tot = getattr(self, "_g_ccl_tot", 0) + 1
        if geom:
            self._g_ccl_geom = getattr(self, "_g_ccl_geom", 0) + 1
        else:
            self._g_ccl_chi = getattr(self, "_g_ccl_chi", 0) + 1
        if self.n == 0 or not len(self.i):
            return np.zeros(self.n)
        if not hasattr(self, "psi") or len(self.psi) < self.n:
            self.calcola_psi()
        I2 = np.abs(self.psi[:self.n]) ** 2
        chi = (self.perc_chi if sorgente is None else sorgente)[:self.n].astype(float)
        vicini = [[] for _ in range(self.n)]
        for a, b in zip(self.i, self.j):
            a, b = int(a), int(b)
            if a < self.n and b < self.n:
                vicini[a].append(b); vicini[b].append(a)
        try:
            rho_c = float(massa_critica_adattiva(self)) / ((4.0 / 3.0) * np.pi * LAM_BASE**3)
        except Exception:
            rho_c = float(massa_critica_collasso()) / ((4.0 / 3.0) * np.pi * LAM_BASE**3)
        lam_loc = self.lambda_nodi()
        chi_core = chi.copy(); r_core = np.zeros(self.n); rho0 = I2.copy()
        for k in range(self.n):
            gruppo = np.asarray([k] + vicini[k], dtype=int)
            intensita = I2[gruppo]
            rho0[k] = float(np.max(intensita)) if len(intensita) else 0.0
            rapporto = rho0[k] / max(rho_c, 1e-12)
            r = float(lam_loc[k]) * np.log(rapporto) if rapporto > 1.0 else 0.0
            r_core[k] = r
            if r <= 0.0:
                continue
            centro = np.average(self.pos[gruppo], axis=0, weights=np.maximum(intensita, 1e-12))
            dentro = np.linalg.norm(self.pos[gruppo] - centro, axis=1) <= r
            wloc = intensita[dentro]
            if np.sum(wloc) > 1e-12:
                chi_core[k] = float(np.sum(wloc * chi[gruppo[dentro]]) / np.sum(wloc))
        if geom:
            # [CHI_COOP] LA CACHE DELLA GEOMETRIA, separata: la legge solo TORS_4PI.
            self._chi_geom_nodi = chi_core
        else:
            self._chi_core_nodi = chi_core
            self._chi_core_rho0 = rho0
            self._chi_core_rhoc = rho_c
            self._chi_core_raggio = r_core
        return chi_core

    def misura_spin_picco_massa(self, idx_massa, pesi=None):
        """Misura spin e chiralita' nel dominio locale del picco costruttivo.

        Il picco e' il nodo della massa con intensita' |Psi|^2 massima. Il dominio
        e' il picco piu' i suoi vicini topologici che appartengono alla stessa massa;
        non usa coordinate, raggio o soglie libere. Le medie sono pesate da |Psi|^2
        e, se disponibili, dai pesi di concorrenza della massa.
        """
        vuoto = dict(picco=-1, n_dominio=0, chi=0.0, spin=0.0,
                     spin_x=0.0, spin_y=0.0, spin_z=0.0,
                     spinor_alpha_re=0.0, spinor_alpha_im=0.0,
                     spinor_beta_re=0.0, spinor_beta_im=0.0,
                     coerenza=0.0, verso_x=0.0, verso_y=0.0, verso_z=0.0)
        idx = np.asarray(idx_massa, dtype=int)
        idx = idx[(idx >= 0) & (idx < self.n)]
        if len(idx) == 0:
            return vuoto
        if not hasattr(self, "psi") or len(self.psi) < self.n:
            self.calcola_psi()
        if not hasattr(self, "_nb") or len(self._nb) < self.n:
            mancanti = self.n - len(getattr(self, "_nb", []))
            nuovi = np.tile([0.0, 0.0, 1.0], (mancanti, 1))
            self._nb = np.vstack([self._nb, nuovi]) if hasattr(self, "_nb") else nuovi
        if len(self._spinor_lift) < self.n:
            self._aggiorna_lift_spinoriale()
        I2 = np.abs(self.psi[:self.n]) ** 2
        campo_formato = float(np.sum(I2[idx])) > 1e-12
        I2_misura = I2 if campo_formato else np.ones(self.n)
        if pesi is None:
            pesi = np.ones(len(idx))
        pesi = np.asarray(pesi, float)
        if len(pesi) != len(idx):
            pesi = np.ones(len(idx))
        peso_nodo = {int(k): max(float(p), 0.0) for k, p in zip(idx, pesi)}
        if not any(p > 0.0 for p in peso_nodo.values()):
            # Il tracking puo' essere negativo durante il transitorio (antifase). In
            # quel caso non eliminiamo il picco: usiamo il dominio della massa con
            # peso topologico unitario, lasciando |Psi|^2 come peso fisico principale.
            peso_nodo = {int(k): 1.0 for k in idx}
        picco = int(idx[np.argmax(I2_misura[idx])])
        dominio = {picco}
        for a, b in zip(self.i, self.j):
            a, b = int(a), int(b)
            if a == picco and b in peso_nodo:
                dominio.add(b)
            elif b == picco and a in peso_nodo:
                dominio.add(a)
        dominio = np.array(sorted(dominio), dtype=int)
        w = I2_misura[dominio] * np.array([peso_nodo[k] for k in dominio])
        den = float(np.sum(w))
        if den <= 1e-12:
            return vuoto
        chi = self.perc_chi[dominio].astype(float) if len(self.perc_chi) >= self.n else np.zeros(len(dominio))
        nb = self._nb[dominio] if hasattr(self, "_nb") and len(self._nb) >= self.n else np.zeros((len(dominio), 3))
        spin_vec = np.sum(w[:, None] * nb, axis=0) / den
        spin_mod = float(np.linalg.norm(spin_vec))
        # Usa il lift complesso gia' trasportato temporalmente; ricostruire qui il
        # rappresentante canonico dal Bloch perderebbe la fase relativa accumulata.
        if len(self._spinor_lift) < self.n and hasattr(self, "_nb") and len(self._nb) >= self.n:
            self._aggiorna_lift_spinoriale()
        spinori = (self._spinor_lift[dominio]
                   if len(self._spinor_lift) >= self.n
                   else np.zeros((len(dominio), 2), complex))
        spinore = np.sum(w[:, None] * spinori, axis=0)
        norma = float(np.linalg.norm(spinore))
        if norma > 1e-12:
            spinore /= norma
        verso = spin_vec / max(spin_mod, 1e-12)
        return dict(picco=picco, n_dominio=int(len(dominio)),
                    chi=float(np.sum(w * chi) / den), spin=spin_mod,
                    spin_x=float(spin_vec[0]), spin_y=float(spin_vec[1]), spin_z=float(spin_vec[2]),
                    spinor_alpha_re=float(spinore[0].real), spinor_alpha_im=float(spinore[0].imag),
                    spinor_beta_re=float(spinore[1].real), spinor_beta_im=float(spinore[1].imag),
                    coerenza=(float(den / max(np.sum(I2[dominio]), 1e-12))
                              if campo_formato else 0.0),
                    verso_x=float(verso[0]), verso_y=float(verso[1]), verso_z=float(verso[2]))

    def misura_spin_picco_per_chiralita(self, idx_massa, pesi=None):
        """Confronta S+ e S- nello stesso dominio locale del picco costruttivo.

        Il dominio viene scelto una sola volta dalla massa completa; la divisione
        per chiralita' e' quindi una misura simmetrica, non una selezione del picco.
        Restituisce anche Q = <chi*n>, correlazione vettoriale spin-chiralita'.
        """
        base = self.misura_spin_picco_massa(idx_massa, pesi)
        vuoto = dict(spin_plus=0.0, spin_minus=0.0, contrasto=0.0,
                     q_x=0.0, q_y=0.0, q_z=0.0, q_modulo=0.0,
                     n_plus=0, n_minus=0)
        if base['picco'] < 0:
            return dict(base, **vuoto)
        idx = np.asarray(idx_massa, dtype=int)
        idx = idx[(idx >= 0) & (idx < self.n)]
        if pesi is None or len(np.asarray(pesi)) != len(idx):
            pesi = np.ones(len(idx))
        pesi = np.asarray(pesi, float)
        if not any(p > 0.0 for p in pesi):
            pesi = np.ones(len(idx))
        I2 = np.abs(self.psi[:self.n]) ** 2
        # Ricostruisce esattamente il dominio: stesso picco e vicini appartenenti alla massa.
        picco = base['picco']; ammessi = set(idx.tolist()); dominio = {picco}
        for a, b in zip(self.i, self.j):
            a, b = int(a), int(b)
            if a == picco and b in ammessi: dominio.add(b)
            elif b == picco and a in ammessi: dominio.add(a)
        dominio = np.array(sorted(dominio), dtype=int)
        pmap = {int(k): max(float(p), 0.0) for k, p in zip(idx, pesi)}
        w = I2[dominio] * np.array([pmap.get(int(k), 0.0) for k in dominio])
        if w.sum() <= 1e-12:
            w = I2[dominio]
        chi = self.perc_chi[dominio].astype(float)
        nb = self._nb[dominio]
        plus = chi > 0; minus = chi < 0
        def modulo(mask):
            den = float(w[mask].sum())
            return float(np.linalg.norm(np.sum(w[mask, None] * nb[mask], axis=0) / den)) if den > 1e-12 else 0.0
        sp, sm = modulo(plus), modulo(minus)
        q = np.sum(w[:, None] * chi[:, None] * nb, axis=0) / max(float(w.sum()), 1e-12)
        contrasto = (sp - sm) / max(sp + sm, 1e-12)
        return dict(base, spin_plus=sp, spin_minus=sm, contrasto=float(contrasto),
                    q_x=float(q[0]), q_y=float(q[1]), q_z=float(q[2]),
                    q_modulo=float(np.linalg.norm(q)), n_plus=int(plus.sum()), n_minus=int(minus.sum()))

    def misura_spin_picco_positivi(self, idx_massa, pesi=None):
        """Controtest empirico: misura lo stesso dominio usando solo perc_chi=+1.

        La selezione e' diagnostica, non una legge dinamica: serve a verificare
        se i generatori positivi possiedono da soli spin e verso piu' coerenti.
        """
        idx = np.asarray(idx_massa, dtype=int)
        if len(self.perc_chi) < self.n:
            return self.misura_spin_picco_massa(idx, pesi)
        mask = self.perc_chi[idx] > 0
        idx_pos = idx[mask]
        if not len(idx_pos):
            return dict(picco=-1, n_dominio=0, chi=0.0, spin=0.0,
                        spin_x=0.0, spin_y=0.0, spin_z=0.0,
                        spinor_alpha_re=0.0, spinor_alpha_im=0.0,
                        spinor_beta_re=0.0, spinor_beta_im=0.0,
                        coerenza=0.0, verso_x=0.0, verso_y=0.0, verso_z=0.0)
        pesi_pos = None if pesi is None else np.asarray(pesi)[mask]
        return self.misura_spin_picco_massa(idx_pos, pesi_pos)

    def indici_massa_vivi(self, mass_id, fallback=None):
        """Restituisce gli indici vivi di una massa e i relativi pesi correnti.

        Il tracking di concorrenza segue anche i figli creati dalla mitosi. Il
        fallback e' usato solo quando la massa non ha ancora voci di tracking.
        """
        indici = []; pesi = []
        for k in range(min(len(self.conc_nodi), self.n)):
            for voce in self.conc_nodi[k]:
                if voce[0] == mass_id:
                    indici.append(k); pesi.append(float(voce[2]) if len(voce) > 2 else 1.0)
                    break
        if indici:
            return np.asarray(indici, dtype=int), np.asarray(pesi, dtype=float)
        if fallback is None:
            return np.zeros(0, dtype=int), np.zeros(0, dtype=float)
        idx = np.asarray(sorted(k for k in fallback if 0 <= k < self.n), dtype=int)
        return idx, np.ones(len(idx), dtype=float)

    def circolazione_topologica(self):
        """Diagnostica della corrente circolante sui cicli del grafo.
        E' deliberatamente passiva: non modifica alcuno stato dinamico.
        La corrente d'arco usa densita' locale, twist orientato e allineamento
        spinoriale; nessuna coordinata o media globale entra nel calcolo.
        La densita' media dell'arco fornisce l'ampiezza energetica locale, mentre
        il twist orientato fornisce la 1-forma che puo' avere circolazione non nulla.
        Oltre alla circolazione della corrente (gradientale, curl-free -> ~0),
        misura le DUE componenti non-gradientali che la decomposizione di Hodge
        ammette: l'OLONOMIA di fase (somma di w4(phi_i-phi_j) sul ciclo: !=0 se
        c'e' un vortice/difetto topologico, componente armonica) e la fase di
        BERRY spinoriale (invariante di Bargmann: prodotto ciclico degli overlap
        tra spinori sul ciclo; curvatura non-abeliana SU(2), gauge-invariante)."""
        vuoto = {"n_cicli": 0, "circolazione_max": 0.0,
                 "circolazione_media_assoluta": 0.0, "circolazione_rms": 0.0,
                 "corrente_arco_max": 0.0, "gradiente_rho_arco_media_assoluta": 0.0,
                 "olonomia_max": 0.0, "olonomia_media_assoluta": 0.0,
                 # le due chiavi NUOVE anche nel ramo VUOTO: un chiamante che le legge non deve
                 # trovarle assenti solo perche' non ci sono cicli. Un `KeyError` in un diagnostico
                 # e' un ramo silenzioso che si scopre al peggior momento.
                 # ⚠ `circolazione_media` MANCAVA nel ramo vuoto mentre quello pieno la
                 # restituisce: un chiamante che la legge prendeva `KeyError` solo quando non ci
                 # sono cicli -- cioe' nel caso raro, che e' il peggiore in cui scoprirlo.
                 # Stessa cosa per i TRE ARRAY GREZZI, che il ramo pieno restituisce e questo no.
                 "olonomia_media": 0.0, "circolazione_media": 0.0,
                 "circolazione": np.zeros(0), "olonomia": np.zeros(0), "berry_spin": np.zeros(0),
                 "olonomia_rms": 0.0, "berry_spin_max": 0.0,
                 "berry_spin_media_assoluta": 0.0, "berry_spin_rms": 0.0,
                 "berry_spin_media": 0.0, "spin_cluster_modulo": 0.0,
                 "spin_cluster_omega": 0.0, "spin_neel_modulo": 0.0,
                 "spin_neel_omega": 0.0,
                 "berry_segno_media": 0.0, "berry_segno_media_assoluta": 0.0,
                 "berry_segno_rms": 0.0, "n_cicli_segno": 0}
        if self.n < 3 or not len(self.i):
            return vuoto
        if not hasattr(self, "psi") or len(self.psi) < self.n:
            self.calcola_psi()
        cicli = self._base_cicli_topologici()
        if not cicli:
            return vuoto
        w = self._pesi(); rho = np.abs(self.psi[:self.n]) ** 2
        spin = np.ones(len(self.i))
        ha_spin = SPINORE and hasattr(self, "_nb") and self._nb is not None and len(self._nb) >= self.n
        if ha_spin:
            spin = np.sum(self._nb[self.i] * self._nb[self.j], axis=1)
        rho_arco = 0.5 * (rho[self.i] + rho[self.j])
        gradiente_rho = rho[self.j] - rho[self.i]
        corrente = w * rho_arco * spin * self.tw / max(PHI_CRIT, 1e-9)
        dph = self._wphi(self.phi[self.i] - self.phi[self.j])   # 1-forma di fase, orientata i->j
        valori = np.array([sum(segno * corrente[e] for e, segno in ciclo)
                           for ciclo in cicli], float)
        olonomia = np.array([sum(segno * dph[e] for e, segno in ciclo)
                             for ciclo in cicli], float)
        berry = []
        if ha_spin:
            nb = self._nb
            # spinori di spin-1/2 dai vettori di Bloch; la fase geometrica e' l'INVARIANTE DI
            # BARGMANN (prodotto ciclico degli overlap <s_k|s_{k+1}>): ciclico -> indipendente dal
            # vertice di partenza, le fasi arbitrarie dei singoli spinori si cancellano. Gauge-invariante
            # (a differenza del solid angle a ventaglio, che dipende dall'apice = dall'orientazione arco).
            th = np.arccos(np.clip(nb[:, 2], -1.0, 1.0))
            ph = np.arctan2(nb[:, 1], nb[:, 0])
            spq = np.stack([np.cos(th / 2.0), np.sin(th / 2.0) * np.exp(1j * ph)], axis=1)
            for ciclo in cicli:
                seq = self._vertici_ciclo(ciclo)
                if seq is None or len(seq) < 3:
                    continue
                s = spq[seq]
                ov = np.sum(np.conj(s) * np.roll(s, -1, axis=0), axis=1)  # <s_k|s_{k+1}> ciclico
                P = np.prod(ov)
                if abs(P) > 1e-12:
                    berry.append(float(np.angle(P)))
        berry = np.array(berry, float) if berry else np.zeros(0)
        # OLONOMIA DI BARGMANN DEL PRIMARIO _psi_spinor (gauge-invariante DEL SEGNO-orologio): arg del
        # prodotto ciclico degli overlap <psi_k|psi_{k+1}> sul ciclo CHIUSO. A differenza della berry su nb
        # (ricostruisce lo spinore dal Bloch -> CIECA al segno-orologio, §38-bis), questa usa il PRIMARIO
        # complesso _psi_spinor -> sonda DIRETTAMENTE se il segno di doppia-copertura si accumula coerente
        # (olonomia netta !=0 = ordine) o si cancella (~0 = frustrato). Invariante di gauge per costruzione:
        # le fasi locali dei singoli spinori si cancellano nel prodotto ciclico chiuso (nessun frame locale).
        berry_sp = []
        _psp = getattr(self, "_psi_spinor", None)
        if _psp is not None and len(_psp) >= self.n:
            for ciclo in cicli:
                seq = self._vertici_ciclo(ciclo)
                if seq is None or len(seq) < 3:
                    continue
                sp = _psp[seq]
                ovp = np.sum(np.conj(sp) * np.roll(sp, -1, axis=0), axis=1)   # <psi_k|psi_{k+1}> ciclico
                Pp = np.prod(ovp)
                if abs(Pp) > 1e-12:
                    berry_sp.append(float(np.angle(Pp)))
        berry_sp = np.array(berry_sp, float) if berry_sp else np.zeros(0)
        # PARAMETRO D'ORDINE SPINORIALE (embedding-indipendente): S_M = |media dei vettori di Bloch|,
        # in [0,1]. S_M~1 = spin allineati/precessione collettiva; S_M~0 = frustrati/sparsi. omega_S =
        # angolo spazzato dalla direzione media Shat fra due campioni consecutivi (precessione dello
        # spin collettivo). Entrambi invarianti per rotazione globale SO(3) (gauge statico dei Bloch).
        S_M = 0.0; omega_S = 0.0
        if ha_spin:
            somma = np.sum(self._nb[:self.n], axis=0)
            norm = float(np.linalg.norm(somma))
            S_M = norm / self.n
            if norm > 1e-9:
                shat = somma / norm
                if getattr(self, "_shat_prec", None) is not None:
                    omega_S = float(np.arccos(np.clip(float(np.dot(shat, self._shat_prec)), -1.0, 1.0)))
                self._shat_prec = shat
        # PARAMETRO D'ORDINE STAGGERED (vettore di Neel): N = |media di chi_i * n_i|. Alto quando gli
        # spin sono ordinati in modo ALTERNATO per chiralita' (antiferromagnetico), anche se S_M~0.
        # omega_N = precessione del vettore di Neel. Embedding-indipendente, gauge-invariante SO(3).
        N_stag = 0.0; omega_N = 0.0
        if ha_spin and len(self.perc_chi) >= self.n:
            chi_n = self.perc_chi[:self.n].astype(float)[:, None] * self._nb[:self.n]
            somN = np.sum(chi_n, axis=0)
            normN = float(np.linalg.norm(somN))
            N_stag = normN / self.n
            if normN > 1e-9:
                nhat = somN / normN
                if getattr(self, "_nhat_prec", None) is not None:
                    omega_N = float(np.arccos(np.clip(float(np.dot(nhat, self._nhat_prec)), -1.0, 1.0)))
                self._nhat_prec = nhat
        return {"n_cicli": int(len(valori)),
                "circolazione_max": float(np.max(np.abs(valori))),
                "circolazione_media_assoluta": float(np.mean(np.abs(valori))),
                "circolazione_rms": float(np.sqrt(np.mean(valori ** 2))),
                "corrente_arco_max": float(np.max(np.abs(corrente))) if len(corrente) else 0.0,
                "gradiente_rho_arco_media_assoluta": float(np.mean(np.abs(gradiente_rho))) if len(gradiente_rho) else 0.0,
                "olonomia_max": float(np.max(np.abs(olonomia))) if len(olonomia) else 0.0,
                "olonomia_media_assoluta": float(np.mean(np.abs(olonomia))) if len(olonomia) else 0.0,
                # [2026-09-20] LA MEDIA COL SEGNO, accanto a quelle assolute e non al loro posto.
                # Le assolute non possono dire se l'olonomia si SOMMA (ordine, verso netto) o si
                # CANCELLA (frustrazione): `olonomia_rms` vale lo stesso in entrambi i casi. Il
                # commento di questa funzione parla gia' di "olonomia netta != 0 = ordine", ma quel
                # numero NON era esposto. Aggiunto, non sostituito: sono due domande diverse.
                # ⚠ SOLO `olonomia_media`: `circolazione_media` ESISTE GIA' in fondo a questo
                # stesso dict (era sfuggita). Averla aggiunta qui avrebbe creato una CHIAVE
                # DUPLICATA nello stesso letterale: Python tiene l'ULTIMA, quindi la mia sarebbe
                # stata codice morto -- e nessun errore lo avrebbe segnalato.
                "olonomia_media": float(np.mean(olonomia)) if len(olonomia) else 0.0,
                "olonomia_rms": float(np.sqrt(np.mean(olonomia ** 2))) if len(olonomia) else 0.0,
                "berry_spin_max": float(np.max(np.abs(berry))) if len(berry) else 0.0,
                "berry_spin_media_assoluta": float(np.mean(np.abs(berry))) if len(berry) else 0.0,
                "berry_spin_rms": float(np.sqrt(np.mean(berry ** 2))) if len(berry) else 0.0,
                "berry_spin_media": float(np.mean(berry)) if len(berry) else 0.0,
                "spin_cluster_modulo": S_M,
                "spin_cluster_omega": omega_S,
                "spin_neel_modulo": N_stag,
                "spin_neel_omega": omega_N,
                # OLONOMIA DI BARGMANN del SEGNO-orologio (_psi_spinor), gauge-invariante: firmata = ORDER
                # PARAMETER (~0 frustrato, !=0 ordine); assoluta = struttura locale; conta i cicli usati.
                "berry_segno_media": float(np.mean(berry_sp)) if len(berry_sp) else 0.0,
                "berry_segno_media_assoluta": float(np.mean(np.abs(berry_sp))) if len(berry_sp) else 0.0,
                "berry_segno_rms": float(np.sqrt(np.mean(berry_sp ** 2))) if len(berry_sp) else 0.0,
                "n_cicli_segno": int(len(berry_sp)),
                "circolazione_media": float(np.mean(valori)),
                "circolazione": valori, "olonomia": olonomia, "berry_spin": berry}

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

    @staticmethod
    def _celle_vive(o, lati, nodi, c, r, T):
        """Classifica le celle. Torna `(vive_o, vive_lati, libere, morte, abbandonate)`.

        Una cella e' un cubo `[o, o+lato)`, **e ogni cella ha il SUO lato**: le libere restano
        grandi, solo le parziali si spezzano. Tre esiti:
          * **MORTA**   -- tutta FUORI dalla palla, **oppure** COPERTA da un nodo;
          * **LIBERA rispetto al nodo piu' vicino al CENTRO** -- tutta dentro la palla, e il
                           nodo piu' vicino al centro della cella dista `>= LAM` dal suo punto
                           piu' vicino. **⚠ NON e' «ogni suo punto e' accettabile»**, e la
                           differenza e' un rilievo di Luca: il test guarda **un solo nodo**,
                           e **un ALTRO nodo puo' stare entro `LAM` da un angolo**. La
                           correttezza regge perche' **ogni proposta e' verificata contro
                           TUTTI i nodi** prima di essere accettata -- ma l'etichetta va
                           scritta per quello che il test fa, non per quello che si spera;
          * **DA DIVIDERE** -- in parte coperta o a cavallo del bordo.

        **La suddivisione si ferma a `lato < LAM * eps_macchina`** *(Luca)*: sotto, due
        posizioni sono **lo stesso `float`**. Le celle abbandonate li' si **CONTANO** (`A8`).

        **⚠ IL TEST GUARDA UN SOLO NODO -- il piu' vicino al CENTRO della cella -- e questo
        ha DUE conseguenze, non una:**
          * una cella coperta dall'**UNIONE** di piu' nodi non e' riconosciuta e **si
            suddivide**: costa lavoro, non correttezza;
          * una cella detta **LIBERA** puo' avere **un altro nodo entro `LAM` da un angolo**:
            quindi «LIBERA» **non garantisce che ogni suo punto vada bene.**
        **La correttezza non dipende da questo test:** dipende dal fatto che **ogni proposta e'
        verificata contro TUTTI i nodi** (`cKDTree`) prima di essere accettata. Il test delle
        celle serve a sapere **DOVE proporre** e **QUANDO fermarsi**, non a garantire i punti.
        *(Rilievo di Luca, 2026-09-24: l'etichetta prometteva piu' di quanto il test verifichi.)*
        """
        if not len(o):
            v = o[:0]
            return v, lati[:0], v, lati[:0], 0, 0
        mezzo = o + 0.5 * lati[:, None]
        dc = np.abs(mezzo - c)
        vicino_c = np.linalg.norm(np.maximum(dc - 0.5 * lati[:, None], 0.0), axis=1)
        lontano_c = np.linalg.norm(dc + 0.5 * lati[:, None], axis=1)
        fuori = vicino_c > r
        dentro = lontano_c <= r
        if T is not None:
            q = nodi[T.query(mezzo, k=1)[1]]
            vic = np.clip(q, o, o + lati[:, None])
            dmin = np.linalg.norm(q - vic, axis=1)
            sp = np.maximum(np.abs(q - o), np.abs(q - (o + lati[:, None])))
            coperta = np.linalg.norm(sp, axis=1) <= LAM
            libera_nodi = dmin >= LAM
        else:
            coperta = np.zeros(len(o), bool)
            libera_nodi = np.ones(len(o), bool)
        morta = fuori | coperta
        libera = (~morta) & dentro & libera_nodi
        dividi = (~morta) & (~libera)
        troppo_piccole = dividi & (lati < LAM * float(np.finfo(float).eps))
        dividi = dividi & (~troppo_piccole)
        # ⚠ LE LIBERE TORNANO COL LORO LATO: senza, il peso `lato^3` del sorteggio sarebbe
        #   sbagliato proprio per le celle grandi, cioe' dove sta quasi tutto il volume libero.
        return (o[dividi], lati[dividi], o[libera], lati[libera],
                int(morta.sum()), int(troppo_piccole.sum()))

    def _semina_lam(self, n, r, centro):
        """[SEMINA_LAM] `n` punti nella palla di raggio `r`, a distanza **>= LAM** l'uno
        dall'altro **e da OGNI nodo gia' presente**. `RSA` con **SATURAZIONE ESATTA**.

        **L'ARRESTO SI DERIVA DA `LAM`** *(decisione di Luca, 2026-09-24)* -- metodo di
        **Zhang & Torquato (2013)**: celle di lato `LAM/sqrt(3)` *(diagonale `LAM`, quindi al
        piu' un nodo per cella)*, si tengono quelle con spazio libero, si suddividono le
        parziali, si propone solo nelle vive, **e si finisce quando non ne resta NESSUNA**.
        **Il rifiuto scatta SOLO se `n` supera la saturazione vera**, quindi **non dipende da
        `n` e non puo' essere FALSO** -- i due difetti del criterio a lotti.

        **UN NUMERO SOLO: `LAM`.** Il lato ne discende per geometria; la risoluzione ultima e'
        `eps` del calcolatore.

        ⚠⚠ **LE PROPOSTE SONO UNIFORMI NEL VOLUME LIBERO, e non e' un dettaglio.**
        La prima stesura proponeva **UN PUNTO PER CELLA**: le celle piccole *(suddivise, cioe'
        gli interstizi)* ricevevano **lo stesso peso** di quelle grandi, quindi **le proposte
        non erano uniformi nel volume libero**. E l'`RSA` e' *esattamente* «uniforme nella
        regione, condizionato all'accettazione», cioe' **uniforme nel volume LIBERO**: un peso
        sbagliato fa un'ALTRA statistica, non l'`RSA`. Ora la cella si sorteggia con peso
        `lato^3`.

        ❌ **E QUI C'ERA SCRITTA UNA DIAGNOSI SBAGLIATA, MIA** *(corretta il 2026-09-24 su
           rilievo di Luca)*. Dicevo: *«il risultato era un impacchettamento piu' DENSO
           dell'RSA, frazione 0.536 contro 0.384, e l'ha preso C3»*. **Falso:**
           * `0.536` era la frazione **GLOBALE**, e il mandato di Luca aveva **gia' dichiarato
             che `C3` si misura NELLA SFERA INTERNA** -- la globale e' alta perche' le sfere di
             raggio `LAM/2` **sporgono** oltre `r` e il denominatore non le contiene;
           * **la prova che la diagnosi era sbagliata: dopo la «correzione» la globale e'
             SALITA** (`0.536` -> `0.568` a `r = 2.0`). Se fosse stata il difetto, la cura
             l'avrebbe abbassata.
           * **`C3`, misurato come va misurato, PASSA:** `0.3826 +- 0.0016` a `r = 10`.
           **Il cambiamento resta giusto; il motivo che avevo scritto no.**
           *(Se commento e storia divergono, il commento mente: par.5-bis.)*
        """
        c = np.asarray(centro, float)
        # [SCENA (ii), 2026-09-25] `n < 0` = **FINO A SATURAZIONE**, senza un bersaglio.
        #   Non e' una manopola nuova (par.3): l'arresto era GIA' derivato da `LAM`, e questo
        #   modo si limita a NON imporre un `n`. Serve perche' la scena `(ii)` chiede
        #   **il vuoto che ci sta**, e la capienza **dipende dal seme** -- misurato
        #   `12807/12783/12812/12790` su quattro semi. Chiedere la MEDIA fa RIFIUTARE i semi
        #   sotto media, ed e' esattamente l'errore che Luca ha preso il 2026-09-25.
        # IL TETTO DELL'ARRAY E' GEOMETRICO, non scelto: al piu' UN nodo per cella di
        #   diagonale `LAM`, quindi al piu' quante celle stanno nel cubo che contiene la palla.
        _sat = bool(n < 0)
        if _sat:
            n = int(np.ceil((2.0 * r / (LAM / np.sqrt(3.0))) ** 3)) + 1
        acc = np.empty((n, 3), float)
        k = 0
        self._sl_abbandonate = getattr(self, "_sl_abbandonate", 0)
        self._sl_giri = getattr(self, "_sl_giri", 0)
        lato0 = LAM / np.sqrt(3.0)
        m = int(np.ceil(2.0 * r / lato0))
        g = np.arange(m, dtype=float) * lato0
        o = (np.stack(np.meshgrid(g, g, g, indexing="ij"), axis=-1).reshape(-1, 3) + (c - r))
        lati = np.full(len(o), lato0)
        while k < n:
            nodi = (np.vstack([np.asarray(self.pos, float), acc[:k]]) if k
                    else np.asarray(self.pos, float))
            T = cKDTree(nodi) if len(nodi) else None
            o_div, lati_div, o_lib, lati_lib, _morte, _abb =                 self._celle_vive(o, lati, nodi, c, r, T)
            self._sl_abbandonate += _abb
            # le LIBERE restano GRANDI: non si spezzano, e il loro volume pesa per intero
            o = np.vstack([o_div, o_lib]) if len(o_lib) else o_div
            lati = (np.concatenate([lati_div, lati_lib]) if len(lati_lib) else lati_div)
            if not len(o):
                break                                     # SATURAZIONE: nessuna cella viva
            self._sl_giri += 1
            # PROPOSTE UNIFORMI NEL VOLUME: la cella si sorteggia con peso `lato^3`.
            # Il numero di proposte e' il numero di celle: non e' un parametro, e' quante ce
            # ne sono.
            vol = lati ** 3
            idx = self.rng.choice(len(o), size=len(o), p=vol / vol.sum())
            p = o[idx] + lati[idx][:, None] * self.rng.random((len(idx), 3))
            p = p[np.linalg.norm(p - c, axis=1) <= r]
            if T is not None and len(p):
                p = p[T.query(p, k=1)[0] >= LAM]
            for q in p:
                if k and np.min(np.sum((acc[:k] - q) ** 2, axis=1)) < LAM * LAM:
                    continue
                acc[k] = q
                k += 1
                if k == n:
                    break
            if k == n:
                break
            # si spezzano SOLO le celle da dividere (le prime `len(o_div)`)
            nd = len(o_div)
            if nd:
                off = 0.5 * np.array([[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 1],
                                      [1, 0, 0], [1, 0, 1], [1, 1, 0], [1, 1, 1]], float)
                nuovi = (o[:nd][:, None, :] + lati[:nd][:, None, None] * off).reshape(-1, 3)
                nuovi_lati = np.repeat(lati[:nd] * 0.5, 8)
                o = np.vstack([nuovi, o[nd:]])
                lati = np.concatenate([nuovi_lati, lati[nd:]])
        if _sat:
            # SATURAZIONE: non c'e' un bersaglio, quindi non c'e' rifiuto. Il tetto geometrico
            # non deve MAI essere toccato: se lo fosse, l'array e' stato il vincolo invece
            # della geometria, e va detto (`A9`) invece di passare in silenzio.
            if k >= n:
                raise SystemExit(
                    "[semina-lam] IL TETTO GEOMETRICO E' STATO RAGGIUNTO (%d): l'array e' stato\n"
                    "  il vincolo invece della geometria. NON riduco in silenzio (`A9`)." % n)
            self._sl_saturazione = int(k)
            return acc[:k]
        if k < n:
            frazione = k * (LAM / 2.0) ** 3 / max(r ** 3, 1e-300)
            raise SystemExit(
                "[semina-lam] RIFIUTO DI SEMINARE: non ci stanno %d nodi a distanza >= LAM\n"
                "  chiesti      n = %d\n"
                "  raggio       r = %.6f   (= %.3f LAM)\n"
                "  LAM            = %.6f   -- `A13`: e' la SCALA DI PLANCK del sistema\n"
                "  collocati      = %d   <- **LA SATURAZIONE VERA**: non resta NESSUNA cella\n"
                "                           in cui un altro nodo possa stare\n"
                "  frazione       = %.4f  (sfere di raggio LAM/2 sul volume della palla;\n"
                "                          il valore noto dell'RSA in 3D e' 0.384, e va\n"
                "                          letto NELLA SFERA INTERNA, non qui: il bordo\n"
                "                          abbassa questa)\n"
                "  nodi gia' presenti = %d   giri = %d   celle abbandonate per risoluzione = %d\n"
                "\n"
                "  NON RIDUCO n IN SILENZIO (`A9`): una massa piu' piccola di quella chiesta\n"
                "  renderebbe ogni misura successiva una misura di un'altra taglia.\n"
                "  LA SCENA CALCOLA IL RAGGIO DA n: o cresce il raggio, o cala n.\n"
                "\n"
                "  L'ARRESTO E' DERIVATO DA LAM (Zhang-Torquato 2013): celle di lato\n"
                "  LAM/sqrt(3), si finisce quando non resta nessuna cella viva. **Quindi\n"
                "  questo rifiuto NON dipende da n e NON puo' essere falso** -- al contrario\n"
                "  del criterio a lotti, che aveva entrambi i difetti (rilievo di Luca).\n"
                "  ** Se `celle abbandonate` > 0 la saturazione NON e' esatta: la suddivisione\n"
                "     ha toccato la risoluzione di `float64` (LAM * eps).**\n"
                % (n, n, r, r / LAM, LAM, k, frazione, len(self.pos),
                   self._sl_giri, self._sl_abbandonate))
        return acc

    def semina(self, n, raggio=None, centro=(0, 0, 0), fase=None, mass_id=None,
               maturi=None):
        # [SCENA (ii)] `n < 0` = **FINO A SATURAZIONE**. Richiede `SEMINA_LAM`: senza una
        # distanza minima la saturazione NON ESISTE, e ridurre a un numero qualsiasi sarebbe
        # una riduzione silenziosa (`A9`). Si DICE, non si aggiusta.
        _sat = bool(n < 0)
        if _sat and not SEMINA_LAM:
            raise SystemExit(
                "[semina] `n < 0` (saturazione) RICHIEDE `SEMINA_LAM`: senza distanza minima\n"
                "  la saturazione non esiste. Per il braccio di controllo di `P-GONFIA` si passa\n"
                "  il numero MISURATO dal braccio acceso, non un numero qualunque (`A9`).")
        # [MAX-NODI-FERMA, 2026-09-28] NON SI TRONCA PIU'. Era:
        #     n = (MAX_NODI - self.n) if _sat else max(0, min(n, MAX_NODI - self.n))
        #   Il `min` tagliava la semina IN SILENZIO: si chiedevano `n` nodi, ne nascevano meno,
        #   e dai dati non si vedeva. Ora si FERMA. Byte-inerte finche' la guardia non morde,
        #   cioe' sempre nelle corse reali (`MAX_NODI` = 4e6 contro i ~12800 nodi del pilota).
        #   ⚠ IL RAMO `_sat` RESTA COM'ERA, e non e' una dimenticanza: in saturazione
        #   IL NUMERO LO DECIDE LA GEOMETRIA (`n = len(p)` qui sotto), e il valore calcolato qui
        #   con `MAX_NODI` **NON VIENE USATO** -- serve SOLO alla scorciatoia `if n == 0: return`,
        #   che e' comportamento dichiarato (`semina(0)` ritorna subito).
        #   **PRIMA DI QUESTA CURA la saturazione NON era controllata da `MAX_NODI`**: lo ha
        #   rilevato il guardiano (Luca, 2026-09-28) sul punto 2 dei miei <<non so>>, e la sua
        #   prescrizione e' **UN SOLO controllo, DOPO `n = len(p)`, sul NUMERO VERO, PER ENTRAMBI
        #   I RAMI**. ### **ORA LO E'**, e il controllo unico sta dopo l'`if`/`else`.
        #   *(Il commento precedente diceva <<quindi OGGI la saturazione NON e' controllata>>:
        #   era vero della versione VECCHIA e falso di questa. Correzione chiesta dal guardiano.)*
        n = (MAX_NODI - self.n) if _sat else max(0, n)
        if n == 0: return
        r = _scala_sistema() * 0.5 if raggio is None else raggio
        if SEMINA_LAM:
            p = self._semina_lam(-1 if _sat else n, r, centro)
            n = len(p)                 # in saturazione il numero lo decide la GEOMETRIA
            if n == 0: return
        else:
            u = self.rng.normal(size=(n, 3)); u /= np.linalg.norm(u, axis=1, keepdims=True)
            p = np.asarray(centro, float) + u * (r * self.rng.random(n) ** (1 / 3))[:, None]
        # [MAX-NODI-FERMA, prescrizione del guardiano del 2026-09-28] UN SOLO CONTROLLO, QUI, SUL
        #   NUMERO VERO, PER ENTRAMBI I RAMI. `n` e' ora il numero di punti che ESISTONO in `p`:
        #   nel ramo `SEMINA_LAM` perche' l'ha deciso la GEOMETRIA (`n = len(p)`), nell'altro
        #   perche' `p` ha esattamente `n` righe. Prima il controllo era DUE: uno prima, sul
        #   numero CHIESTO, e uno dentro il solo ramo `SEMINA_LAM`. Due controlli sono due leggi
        #   (`9-ter`), e quello dentro il ramo LASCIAVA SCOPERTO l'altro ramo.
        #   ⚠ E LA CONSEGUENZA, DICHIARATA: controllando DOPO, i punti `p` sono GIA' ALLOCATI
        #   quando il run si ferma. Sono `n x 3` float, e non sono la memoria che `MAX_NODI`
        #   protegge davvero (quella e' lo STATO DEL GRAFO, archi compresi, che non e' ancora
        #   stato toccato) -- ma e' un'allocazione che prima, col troncamento, non avveniva.
        _ferma_se_oltre_max_nodi(self.n, n, 'semina: numero VERO, dopo la geometria')
        if fase is None:
            ph = self.rng.random(n) * 4 * np.pi
        else:
            ph = float(fase) + self.rng.normal(0, 0.05, n)
        base = self.n
        self.pos = np.vstack([self.pos, p])
        self.phi = np.concatenate([self.phi, ph % self._dphi()])
        self.phi0 = np.concatenate([self.phi0, ph % self._dphi()])
        self.phi_s = np.concatenate([self.phi_s, np.zeros(n)])   # spinore: nasce a 0 (inerte se spento)
        # profilo di percorrenza: verso casuale (+1/-1) = le due antichiralita', ~50/50.
        # (assegnato PRIMA di phivel perche' il calcio chirale lo usa)
        chi_nuovi = self.rng.choice([-1, 1], n)
        # impulso iniziale di fase: zero in regime stocastico (ramo che NON gira), calcio termico
        # di punto zero in regime DETERMINISTICO (_CALORE_INIT), che e' il regime in uso: qui il
        # calcio sostituisce il vuoto come energia iniziale.
        if _CALORE_INIT > 0:
            if CALORE_VETTORIALE:
                # CALCIO CHIRALE: la fluttuazione di fase e' FIRMATA dalla chiralita' del solitone.
                # Non si media a zero come il rumore isotropo: crea chiralita' netta locale che
                # frame-drag e mem_mot possono agganciare e trasformare in rotazione orbitale.
                calcio_phi = chi_nuovi * self.rng.normal(_CALORE_INIT, _CALORE_INIT * 0.5, n)
            else:
                calcio_phi = self.rng.normal(0, _CALORE_INIT, n)   # scalare isotropo (epoca 1)
            self.phivel = np.concatenate([self.phivel, calcio_phi])
        else:
            self.phivel = np.concatenate([self.phivel, np.zeros(n)])
        # [CURA 4] L'ETA' DEI NODI NUOVI. `eta` E' IL MARCATORE, e non serve un array nuovo:
        #   nato in dinamica -> `eta = 0`; nato come vuoto DATO -> `eta` tale che `ramp = 1`.
        #   `eta` esiste gia', e' GIA' estesa a ogni sito di nascita ed e' GIA' nello snapshot:
        #   **usarla come marcatore evita di creare il settimo array da estendere a mano**, che
        #   e' la famiglia di difetti di `_cs_nodo_prev` e `_psi_spin_prec`.
        #
        # LA DISTINZIONE "INIZIALE" / "IN VOLO", dichiarata (il codice non l'aveva):
        #   `maturi=True/False`  -> lo dice il CHIAMANTE, esplicitamente;
        #   `maturi=None`        -> DEFAULT: matura **se la rete era VUOTA**, cioe' se questa
        #                           semina **E'** l'universo.
        #   ⚠ `n == 0` NON E' UNA SOGLIA: e' un fatto topologico -- prima non c'era niente.
        #     Un criterio temporale ("prima del passo 1") sarebbe un numero nuovo (par.3/A11).
        #   ⚠ E IL LIMITE: una scena che seminasse DUE volte su rete non vuota avrebbe la
        #     seconda trattata come "in volo". Per questo il parametro ESPLICITO esiste: chi
        #     vuole due semine iniziali passa `maturi=True` e lo DICHIARA nella scena.
        _mat = (base == 0) if maturi is None else bool(maturi)
        if SEMINA_MATURA and _mat:
            # `eta` = il tempo di rampa DI QUEI NODI -> `ramp = min(1, eta/tempo) = 1` ESATTO.
            # Si legge DOPO `_allaccia` (sotto), perche' il tempo-luce ha bisogno degli archi.
            self.eta = np.concatenate([self.eta, np.zeros(n)])
            self._cura4_maturi = (int(base), int(base + n))
        else:
            self.eta = np.concatenate([self.eta, np.zeros(n)])
            self._cura4_maturi = None
        self.perc_chi = np.concatenate([self.perc_chi, chi_nuovi])
        # [CHI_COOP] VIA 1 di 3 (semina). Alla nascita la geometria COPIA la carica: nel ramo A al
        # passo 0 sono la stessa cosa, e `chi_basc` la riscrive al passo dopo comunque.
        self.perc_geom = np.concatenate([self.perc_geom, chi_nuovi])
        self.perc_tw = np.concatenate([self.perc_tw, np.zeros(n)])
        self.mem_mot = np.vstack([self.mem_mot, np.zeros((n, 3))]) if len(self.mem_mot) else np.zeros((n, 3))
        # CALCIO al MOMENTO ANGOLARE SPINORIALE: invece di omega_s=(0,0,0), il punto zero eccita il
        # vettore di rotazione di Bloch, rompendo la degenerazione meridiana (1D -> precessione 3D).
        if CALORE_VETTORIALE and _CALORE_INIT > 0:
            calcio_omega = self.rng.normal(0, _CALORE_INIT, (n, 3))
            self.omega_s = np.vstack([self.omega_s, calcio_omega]) if len(self.omega_s) else calcio_omega
        self.conc_nodi.extend([[] for _ in range(n)])   # TRACKING: liste vuote per i nuovi nodi
        self._allaccia(base)
        # [CURA 4] LA MATURITA' SI SCRIVE **QUI**, DOPO `_allaccia`, e non prima: il tempo di
        #   rampa e' `_tempo_luce_nodo`, che ha bisogno degli ARCHI per costruire `d_nodo`.
        #   Prima dell'allaccio il nodo non ha archi, e il tempo-luce non esiste ancora.
        # ========================================================================================
        # [`RAMPA-1`, strada (3), DECISIONE DI LUCA 2026-09-25] **IL VUOTO DATO HA ETA' INFINITA.**
        # ----------------------------------------------------------------------------------------
        # ❌ **COM'ERA E PERCHE' NON BASTAVA:** `eta = _tempo_rampa()` da' `ramp = 1` **esatto
        #   IN QUELL'ISTANTE**, e `ramp` e' un rapporto fra **due quantita' che si muovono
        #   entrambe**. **MISURATO** in configurazione del driver (`RAMPA-1`): fra il passo 0 e
        #   il passo 1 `eta` cresce **x1.011** e `_tempo_rampa` **x1.196** -- il denominatore
        #   corre **18 volte** piu' del numeratore -- e `ramp` cade a `0.846` di mediana, con
        #   **solo 54 nodi su 4252** ancora a `1` e `_g_rampa_cali = 4198`.
        #   **CAUSA:** al passo 0 la cache `_cs_nodo_prev` **non esiste**, quindi il tempo-luce
        #   si calcola con `cs = CS_M`; al passo 1 il `cs` vero e' `p50 1.672` su `CS_M = 2`
        #   (`cs_std/cs = 19.07 %`). **La maturita' era assegnata con un `cs` che il nodo non ha.**
        # ✅ **ORA: `eta = +inf`.** `ramp = min(1, inf/tr) = 1` **per sempre, qualunque `cs`**.
        #   **«Maturo» non e' un VALORE di `eta`: e' una PROPRIETA'** -- il vuoto **c'era gia'**.
        #   `+inf` e' l'unico modo di dirlo **senza un numero e senza un array**: non e' una
        #   soglia grande, e' **«nessun tempo di accensione»**.
        # ✅ **E TOGLIE CODICE INVECE DI AGGIUNGERLO** (`STANDARD 10`): via la chiamata a
        #   `_tempo_rampa()` **e le sue DUE diramazioni** (array / scalare), che esistevano solo
        #   per ricopiare il denominatore nel numeratore.
        # ⚠ **I NATI IN DINAMICA NON SONO TOCCATI:** nascono con `eta = 0` (`:2720`, `:2723`,
        #   `:6022`, `:6178`) e salgono con la rampa del tempo-luce. **La maturita' e' del VUOTO
        #   DATO, non una proprieta' che si eredita.**
        # ⚠ **`+inf` E' UN VALORE SPECIALE, e le sue letture sono VERIFICATE PER AST**
        #   (`csv/_letture_eta.py`, `doc/LETTURE_eta.md`): le uniche due letture di `eta` in una
        #   legge sono `:3419` e `:3684`, **nessuna delle due e' una riduzione**. L'unica
        #   riduzione e' **diagnostica** (`_stat` delle colonne `eta_*`), adattata nello stesso
        #   commit.
        if SEMINA_MATURA and getattr(self, "_cura4_maturi", None) is not None:
            _a, _b = self._cura4_maturi
            self.eta[_a:_b] = np.inf
            self._g_cura4_maturati = getattr(self, "_g_cura4_maturati", 0) + int(_b - _a)
            self._cura4_maturi = None
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
        rc = R_CONN() if not len(self.i) else \
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
        # [A8, 2026-09-20] (b) RAGIONE DICHIARATA E VALIDA: il commento qui sopra dice
        # `default off, per non alterare i risultati esistenti finche' non e' verificata`.
        # ⚠ IL CONTATORE MISURA UN'ALTRA COSA, e il nome lo dice: `_spento`, non `_salti`.
        # Conta quante volte il ramo NON gira perche' il FLAG e' spento -- oggi il 100 % per
        # costruzione. Non e' una frazione di fallimento, ed e' un presidio contro
        # un'ACCENSIONE SILENZIOSA: il giorno in cui qualcuno accende COMPAT_CHI, il numero cambia.
                # ✅ MISURATO: ramo SPENTO 12 volte su 12 (frazione 1.000). CLASSE: **(b)**, e il contatore
        # e' un presidio contro un'accensione silenziosa, non una frazione di fallimento.
        self._g_compat_chi_tot = getattr(self, "_g_compat_chi_tot", 0) + 1
        if not COMPAT_CHI:
            self._g_compat_chi_spento = getattr(self, "_g_compat_chi_spento", 0) + 1
        if COMPAT_CHI and len(a) and len(self.perc_chi) >= self.n:
            opposti = self.perc_chi[a] != self.perc_chi[b]
            a, b, dd = a[opposti], b[opposti], dd[opposti]
        if not len(a): self._grado(); return
        self.i = np.concatenate([self.i, a]); self.j = np.concatenate([self.j, b])
        if TRACCIA_D0: _tr_pre = self.d0.copy()
        # `md=1, md0=1`: UNA chiamata vale per `d` E per `d0` (entrambi concatenano `dd`).
        dd = self._nasce(dd, 'semina', 1, 1)   # [SCALA_MIN] il troncone parte da LAM
        self._smp_chirurgia(nuovi=dd)   # [C3] `_allaccia` (semina): archi nuovi in coda
        self.d = np.concatenate([self.d, dd]); self.d0 = np.concatenate([self.d0, dd])
        if TRACCIA_D0: self._traccia_d0('S01_archi_nuovi', _tr_pre)
        self.vd = np.concatenate([self.vd, np.zeros(len(dd))])
        self.peq = np.concatenate([self.peq, np.full(len(dd), np.nan)])  # da calibrare
        self._rep = np.concatenate([self._rep, np.zeros(len(dd))])       # [(3)] nessuna storia
        self.tw = np.concatenate([self.tw, np.zeros(len(dd))])
        self.twp = np.concatenate([self.twp, np.zeros(len(dd))])
        self._grado()

    def lambda_nodi(self):
        """SCHERMATURA NON-PARAMETRICA ANCORATA A N_CRITICO."""
        if (not SCHERMATURA) or (not len(self.i)):
            return np.full(self.n, LAM)
        # [PSI-FLASH, 2026-09-28] LE DUE CONDIZIONI ERANO IN UN `or`, E SONO COSE DIVERSE. Era:
        #     if not hasattr(self, "psi") or len(self.psi) < self.n: return np.full(self.n, LAM)
        #   ⚠ `not hasattr` e' L'INIZIALIZZAZIONE: al passo 1 `psi` non esiste ancora, e usare
        #   `LAM` e' l'unica cosa possibile. **RESTA.** Misurato: scatta 1 volta in 44 passi.
        #   ⚠⚠ `len(psi) < n` era IL DIFETTO: al passo di nascita `mitosi` fa crescere `n`, quindi
        #   la schermatura SI SPEGNEVA PER TUTTA LA RETE -- `lambda` da ~0.60 a 0.80, e `|psi|` su
        #   di 1.62x per TUTTI, non per il nato. **ORA FERMA IL RUN.** Misurato: scattava 1 volta
        #   in 44 passi, ed era il passo della nascita.
        # ⚠ CORREZIONE DI UNA MIA LETTURA SBAGLIATA, 2026-09-28: avevo scritto che il caso
        #   dell'INIZIALIZZAZIONE e' `not hasattr(self, "psi")`. **E' FALSO:** `Rete.__init__` fa
        #   `self.psi = np.zeros(0, complex)`, quindi l'attributo ESISTE SEMPRE e
        #   ### l'inizializzazione e' `len(psi) == 0`. La mia sonda contava le due condizioni
        #   insieme, e ho attribuito alla prima l'occorrenza del passo 1 che era della seconda.
        #   **Con lo split sbagliato l'errore scattava alla COSTRUZIONE DELLA SCENA.**
        if (not hasattr(self, "psi")) or len(self.psi) == 0:
            self._g_scherm_init = getattr(self, "_g_scherm_init", 0) + 1
            return np.full(self.n, LAM)
        if len(self.psi) < self.n:
            raise SchermaturaSpenta(
                "[SCHERMATURA] IL RUN SI FERMA (`PSI-FLASH`, `A9`).\n"
                "  len(psi) .. %d\n"
                "  n ......... %d   (mancano %d valori)\n"
                "  PERCHE': con `psi` piu' corta di `n`, `lambda_nodi` restituiva `LAM` per TUTTA\n"
                "  la rete, cioe' SPEGNEVA LA SCHERMATURA, e il campo saliva di ~1.62x per tutti.\n"
                "  CHE FARE: `psi` va ESTESA a ogni nascita (`_eredita_psi_figli`). Se questo\n"
                "  errore scatta, una strada nuova fa crescere `n` senza estendere `psi` -- e\n"
                "  prima di questa cura quella strada cambiava la fisica IN SILENZIO."
                % (len(self.psi), self.n, self.n - len(self.psi)))
        rho = self._rho_sorgente()   # [FASE 2] |psi|^2 (off) o rho_spin = norma del campo emesso (CAMPO_SPINORIALE on)
        # massa_critica_adattiva usa i pesi correnti e quindi richiama lambda_nodi.
        # Nel ramo ricorsivo si usa LAM: il crossover resta dinamico senza loop infinito.
        if getattr(self, "_calcolo_schermatura", False):
            # [PSI-FLASH, 2026-09-28] QUESTO RIPIEGO RESTA, E NON E' UN DIFETTO: e' la DEFINIZIONE
            #   di come si calcola la massa critica -- **sul NUCLEO NUDO**, `lambda = LAM`, perche'
            #   ### la soglia che ACCENDE la schermatura non puo' dipendere dalla schermatura
            #   stessa. *(Decisione di Luca, 2026-09-28; scheda `schermatura-nucleo-nudo`.)*
            #   ⚠ QUELLO CHE MANCAVA ERA IL NUMERO, e ora c'e' (`A8`): MISURATO 308 volte su 44
            #   passi, cioe' SETTE PER PASSO, contro le 2 del ripiego di `len(psi)`. Su 530
            #   chiamate di `_lam_archi`, 310 restituiscono `LAM`: il 58.5 %.
            #   ⚠⚠ E UNA COSA DA FARE ALTROVE, non qui: `massa_critica_adattiva` si RICALCOLA a
            #   ogni richiesta, su stati DIVERSI dentro lo stesso passo -- e' una LETTURA MISTA.
            #   Va calcolata UNA volta nella fase `apri`, sulla fotografia. Voce `MCRIT-RICALCOLO`.
            self._g_scherm_ricorsione = getattr(self, "_g_scherm_ricorsione", 0) + 1
            return np.full(self.n, LAM)
        self._calcolo_schermatura = True
        try:
            Ncrit = massa_critica_adattiva(self)
        finally:
            self._calcolo_schermatura = False
        rho_c = Ncrit / max((4.0 / 3.0) * np.pi * (LAM**3), 1e-9)
        u = rho / max(rho_c, 1e-9)
        softplus = np.log1p(np.exp(np.clip(u - 1.0, -30, 30)))
        fattore = 1.0 / (1.0 + softplus)
        portata_minima = LAM * 0.15
        return np.maximum(LAM * fattore, portata_minima)

    def _lam_archi(self):
        """SIMMETRIZZATA: w_ij deve valere quanto w_ji, altrimenti la matrice
        di accoppiamento perde la simmetria su cui poggiano memoria hebbiana
        e costruzione del campo."""
        if not SCHERMATURA:
            return LAM
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
        if TEMPO_SEGNO and len(getattr(self, "tw", [])):
            # MOD 5.3b: magnitudine del tempo proprio = dilatazione torsionale ESPLICITA 1+|tw_nodo|/PHI_CRIT
            # (il de Broglie del campo emesso e' scorrelato dalla dilatazione: bocciato da S3b). tw_nodo =
            # media di |tw| sugli archi incidenti (stessa forma del kernel mitosi). Lenta e stabile (RI-TEST 2).
            aw = np.abs(self.tw); ii, jj = self.i, self.j
            twn = np.zeros(self.n); deg = np.zeros(self.n)
            mi = ii < self.n; mj = jj < self.n
            np.add.at(twn, ii[mi], aw[mi]); np.add.at(twn, jj[mj], aw[mj])
            np.add.at(deg, ii[mi], 1.0);    np.add.at(deg, jj[mj], 1.0)
            return 1.0 + (twn / np.maximum(deg, 1.0)) / max(PHI_CRIT, 1e-9)
        # [A8 - Z33, 2026-09-18] SOLO CONTATORI, nessuna logica toccata. Questo ramo restituisce
        # `r = 1` per TUTTI: la dilatazione temporale sparisce in quel passo. E' legittimo -- non
        # esiste uno stato precedente con cui confrontarsi -- ma finora non lo diceva NESSUNO.
        self._ritmo_chiamate = getattr(self, "_ritmo_chiamate", 0) + 1
        if self._psi_prec is None or len(self._psi_prec) != self.n:
            self._ritmo_sicurezza = getattr(self, "_ritmo_sicurezza", 0) + 1
            self._ritmo_sicurezza_shape = (
                -1 if self._psi_prec is None else len(self._psi_prec), self.n)
            self._psi_prec = self.psi.copy() if len(self.psi) == self.n else np.ones(self.n, complex)
            return np.ones(self.n)
        a = np.angle(self.psi) - np.angle(self._psi_prec)
        signed = ((a + np.pi) % (2 * np.pi) - np.pi) / DT
        # [FASE 5] TEMPO PROPRIO dal CAMPO SPINORIALE (batte sull'OTTO, 4pi) invece del campo scalare.
        # COERENZA (magnitudine): nel limite psi_spin[:,0]=self.psi e |dphi|<pi -> ritmo IDENTICO. Il segno
        # non entra nel ritmo (magnitudine); il legame orologio-segno vive nel de Broglie SU(2) (gia' 4pi,
        # TW_SPINORE = tw/4pi). Snapshot t-1 (Jacobi): psi_spin del passo precedente, _psi_spin_prec aggiornato in step.
        _ps = getattr(self, "psi_spin", None); _psp = getattr(self, "_psi_spin_prec", None)
        # [A8 - Z33] il guard 4pi: se fallisce si cade sul ramo SCALARE 2pi, e nessuno lo dice.
        # E' la stessa guardia che fu inerte nel 95.33 % delle chiamate PER MESI (C11).
        if CAMPO_SPINORIALE:
            if _ps is None or _psp is None or len(_ps) != self.n or len(_psp) != self.n:
                self._ritmo_guard4pi_ko = getattr(self, "_ritmo_guard4pi_ko", 0) + 1
                self._ritmo_guard4pi_shape = (-1 if _ps is None else len(_ps),
                                              -1 if _psp is None else len(_psp), self.n)
            elif _ps is _psp or np.array_equal(_ps, _psp):
                # LO SNAPSHOT E' LO STESSO OGGETTO (o identico): `f` sara' ZERO per ogni nodo.
                # Non e' un errore -- significa che `psi_spin` non e' cambiato dall'ultimo snapshot --
                # ma senza questo contatore la degenerazione e' INVISIBILE.
                self._ritmo_snap_identico = getattr(self, "_ritmo_snap_identico", 0) + 1
        if CAMPO_SPINORIALE and _ps is not None and _psp is not None and len(_ps) == self.n and len(_psp) == self.n:
            a = np.angle(_ps[:, 0]) - np.angle(_psp[:, 0])
            if RITMO_WRAP_2PI:
                # [D34, 2026-09-22] IL PERIODO GIUSTO. `np.angle` ha periodo `2pi`, quindi `a`
                # sta in (-2pi, 2pi] e una differenza di OSSERVABILI si avvolge su `2pi`.
                # E' LA STESSA FORMA del ramo scalare otto righe sopra.
                signed = ((a + np.pi) % (2 * np.pi) - np.pi) / DT
            else:
                signed = ((a + 2 * np.pi) % (4 * np.pi) - 2 * np.pi) / DT   # wrapping su 4pi (l'otto)
        # FLAG 4 (--tempo-proprio-orientato): f mantiene il SEGNO (tempo proprio orientato);
        # off = modulo, byte-identico al comportamento storico. La scala gauge resta positiva.
        f = signed if TEMPO_PROPRIO_ORIENTATO else np.abs(signed)
        # [A8 - Z33] LA FIRMA DEL DIFETTO: `f` identicamente nullo -> `x = 0` -> `r ~ 1.414e-06`,
        # cioe' IL TEMPO PROPRIO SI FERMA PER TUTTI in quel passo. E il caso piu' debole:
        # `median(|f|) = 0` con qualche `f` non nullo -> `med` cade sul PAVIMENTO e quelli ESPLODONO.
        # Sono due regimi OPPOSTI e si contano separatamente.
        _fa = np.abs(f)
        if _fa.size:
            if float(np.max(_fa)) == 0.0:
                self._ritmo_f_tutto_nullo = getattr(self, "_ritmo_f_tutto_nullo", 0) + 1
            elif float(np.median(_fa)) <= 0.0:
                self._ritmo_f_mediana_nulla = getattr(self, "_ritmo_f_mediana_nulla", 0) + 1
            if float(np.median(_fa)) <= 1e-9:
                self._ritmo_med_sul_pavimento = getattr(self, "_ritmo_med_sul_pavimento", 0) + 1
        # [CURA DELL'ANELLO ISTANTANEO, 2026-09-18 - categoria D del par.10: NESSUN FLAG]
        # IL DIFETTO: `med` era `median(|f|)` DELLO STESSO ISTANTE, e veniva usato SU `f`. Due
        # assiomi nella stessa riga: A6 (nessuna funzione istantanea di X agisce dinamicamente su X:
        # `f` e `r` si determinavano a vicenda DENTRO il passo) e A3 (`median(x) = 1` per IDENTITA').
        # MISURATO PRIMA DELLA CURA (`csv/_test_fork/_anello_sfasato.txt`, blob f8f46683):
        #   `max|median(x) - 1| = 0.000e+00` su 122 passi -- il punto fisso non era "circa": era
        #   ESATTO A MACCHINA. Col `med` sfasato di uno diventa 2.1097 / 0.9108 / 1.1727.
        # LA CURA: si legge il `med` del passo PRECEDENTE. Il RIFERIMENTO non cambia (resta
        # `median(|f|)`): cambia QUANDO lo si legge. Nessun gauge nuovo, nessun numero tarato.
        #
        # PERCHE' `ritmo()` NON SCRIVE `_med_f_prec`, ed e' il presidio che regge tutto: questo
        # metodo ha TRE call-site, e DUE SONO DIAGNOSTICI (`:3124` la fisica, `_diag_completa` e il
        # terzo). Se lo snapshot avanzasse qui, ogni chiamata diagnostica farebbe avanzare lo stato
        # fisico -- par.2.3 (purezza pure-read) violato, e sarebbe il QUINTO difetto di questa
        # famiglia. Quindi: qui si LEGGE e si REGISTRA; **`step()` PROMUOVE**, a `:3129-3131`,
        # accanto a `_psi_prec` e `_psi_spin_prec`, che sono gli altri due snapshot consumati da qui.
        # La contaminazione da diagnostico e' chiusa PER COSTRUZIONE: `step()` chiama `ritmo()`
        # PRIMA di promuovere, quindi il valore promosso e' sempre quello della chiamata FISICA.
        #
        # PERCHE' UNO SCALARE E NON L'ARRAY `f`: uno scalare NON HA LUNGHEZZA, quindi l'intera
        # classe A8b (cache cross-passo da estendere a ogni punto di crescita: mitosi, `semina`,
        # `nuova_massa`) SPARISCE PER COSTRUZIONE. E' il presidio piu' forte disponibile, ed e' la
        # ragione per cui `_cs_nodo_prev` e `_psi_spin_prec` hanno fatto difetto e questo non puo'.
        # A3c/A8b (quarto livello): `med_prec` e `f` sono ENTRAMBI `Delta_angle/DT`, cioe' `[1/T]` -
        # confrontabili, non solo presenti.
        _med_corrente = max(float(np.median(np.abs(f))), 1e-9)
        self._med_f_ultimo = _med_corrente             # REGISTRO, non snapshot: lo promuove step()
        _medp = getattr(self, "_med_f_prec", None)
        if _medp is None:
            # NON ESISTE UN PRIMA. Si riusa la convenzione gia' presente in questo stesso metodo
            # (`:2021-2026`, `_psi_prec` assente -> `np.ones`), NON se ne inventa una nuova: "nessun
            # passato" significa "nessuna dilatazione", e si CONTA (A8).
            # ⚠ E il fallback NON e' `median(|f|)` corrente: sarebbe il difetto stesso, al passo 1.
            self._ritmo_med_assente = getattr(self, "_ritmo_med_assente", 0) + 1
            return np.ones(self.n)
        med = float(_medp)
        if med == _med_corrente:
            # il gauge non si e' mosso fra i due passi: legittimo, ma invisibile senza contatore
            # (e' la forma che `Z33` prende qui).
            self._ritmo_med_identico = getattr(self, "_ritmo_med_identico", 0) + 1
        x = f / med
        r = x / np.sqrt(1.0 + x**2) + 1.0e-6           # bottleneck liscio, satura a 1 per x->inf
        r_unit = 1.0 / np.sqrt(2.0) + 1.0e-6           # valore al gauge x=1
        r_normalized = r / r_unit                       # x=1 -> fattore unitario
        return 1.0 + TAU_LOC * (r_normalized - 1.0)

    def _passo_spinoriale(self, i, j, w, dt_n, psi_snapshot=None,
                          forza_sync=None, wI_sync=None, uno_sync=None):
        """ORFANO dal 2026-09-02 (commit d2c76f3): la chiamata e' stata persa nel refactor ETC e
        non e' piu' invocata nel percorso vivo. Riattivabile solo reinnestandolo nell'ordine ETC.
        PASSO 2+3: settore spinoriale non-abeliano con MOTORE CONSERVATIVO hebbiano.
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
        # Nel ramo sincrono il settore spinoriale legge una snapshot immutabile
        # dello stato t. Le copie vengono usate solo a destra dell'equazione;
        # le assegnazioni a _nb/omega_s sono il commit verso t+1.
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
                _g = self.rng.normal(0, 1.0, (n, 3))
                if RUMORE_COLORATO:
                    # TAGLIO SPETTRALE: il calcio non e' piu' indipendente fra un passo e l'altro,
                    # ma correlato su `tau_c = LAM/CS_M` (il tempo-luce del solitone, DERIVATO).
                    # `dt_n`, non `DT`: processo LOCALE, altrimenti frame preferito (par.9).
                    _tauc = LAM / max(CS_M, 1e-12)
                    _dtl = dt_n if np.isscalar(dt_n) else np.asarray(dt_n, float)[:n]
                    # VALORE ASSOLUTO, e non e' pignoleria: `_passo_spinoriale` riceve `dt_n_s`,
                    # che sotto `--tempo-segno` (MOD 5.3a, Feynman-Stuckelberg) puo' essere
                    # NEGATIVO per l'antimateria. Con `dt_n < 0` verrebbe `a > 1` e la ricorsione
                    # DIVERGEREBBE IN SILENZIO. Il tempo di correlazione e' una durata, quindi
                    # dipende dal MODULO del tic, non dal suo verso. Nessun numero nuovo.
                    _a = np.exp(-np.abs(_dtl) / _tauc)
                    _b = np.sqrt(np.maximum(1.0 - _a * _a, 0.0))
                    _xi = getattr(self, "_xi_rumore", None)
                    self._xi_chiamate = getattr(self, "_xi_chiamate", 0) + 1
                    if _xi is None or len(_xi) < n:
                        # ESTRAZIONE FRESCA DALLA DISTRIBUZIONE STAZIONARIA (N(0,1)) PER I NODI
                        # NUOVI. Zero transitorio, zero parametri: partire da zero darebbe un
                        # primo calcio attenuato di b = sqrt(1-a^2), cioe' un artefatto.
                        # [2026-09-16] QUESTO NON E' UN FALLBACK: E' IL PERCORSO NORMALE della
                        # mitosi. `xi` e' l'AMBIENTE, non una proprieta' del nodo, quindi il
                        # figlio NON lo eredita (vedi `_eredita_spinore_figli`). I nodi ESISTENTI
                        # conservano il proprio `xi` - il `vstack` tiene la testa intatta - e solo
                        # i NUOVI ricevono un campione fresco, perche' un nodo appena nato non ha
                        # un passato del rumore che lo ha spintonato.
                        self._xi_esteso = getattr(self, "_xi_esteso", 0) + 1
                        self._xi_nuovi = (getattr(self, "_xi_nuovi", 0)
                                          + max(n - (0 if _xi is None else len(_xi)), 0))
                        _base = np.asarray(_xi, float) if _xi is not None else np.zeros((0, 3))
                        _manca = n - len(_base)
                        _xi = (np.vstack([_base, self.rng.normal(0, 1.0, (_manca, 3))])
                               if _manca > 0 else _base[:n])
                    else:
                        _xi = np.asarray(_xi, float)[:n]
                    _ac = _a if np.isscalar(_a) else _a[:, None]
                    _bc = _b if np.isscalar(_b) else _b[:, None]
                    _xi = _xi * _ac + _bc * _g
                    self._xi_rumore = _xi
                    _calcio = _xi
                else:
                    _calcio = _g
                self._nb = self._nb + _calcio * amp[:, None]
                self._nb = self._nb / np.maximum(np.linalg.norm(self._nb, axis=1, keepdims=True), 1e-9)
        nb = self._nb
        # CAUSALITA': campo dai vicini allo stato RITARDATO (Bloch del passo precedente)
        self._g_nb_prec_tot = getattr(self, "_g_nb_prec_tot", 0) + 1
        if not hasattr(self, "_nb_prec") or self._nb_prec is None or len(self._nb_prec) != n:
            # [A8, 2026-09-20] (a) NESSUNA RAGIONE DICHIARATA, e il fallback NON e' innocuo.
            # Due righe sopra il codice dichiara `CAUSALITA': campo dai vicini allo stato
            # RITARDATO (Bloch del passo precedente)`, e qui si usa `nb`, cioe' il Bloch
            # CORRENTE: quando questo ramo gira, la causalita' dichiarata NON vale.
            # MISURATO che NON e' un difetto di lunghezza: `_nb_prec` e' scritto a :2712 DENTRO
            # `_passo_spinoriale`, quindi alla PRIMA chiamata non esiste ancora. E' lo STESSO
            # transitorio di avvio di `zeta_vir` (Z68), e la stessa causa: l'ORDINE.
            # ✅ MISURATO (sigillo `3/4 + 1 atteso`, 2d018e7): **1 salto su 12**, `shape (-1, 2391)`
            # cioe' `_nb_prec is None`, e `quando = 1` -- SOLO la prima invocazione. CLASSE: **(a)**,
            # ed e' l'UNICA dei dieci che scatta davvero in un run. Transitorio d'avvio, stessa
            # causa di `Z68`: l'ORDINE.
            self._g_nb_prec_salti = getattr(self, "_g_nb_prec_salti", 0) + 1
            self._g_nb_prec_shape = (-1 if getattr(self, "_nb_prec", None) is None
                                     else len(self._nb_prec), n)
            self._g_nb_prec_quando = getattr(self, "_g_nb_prec_tot", 0)
            nb_vic = nb
        else:
            nb_vic = self._nb_prec
        # campo effettivo B_i = somma dei vicini, con segno SU(2) dalla chiralita' del legame.
        # Il segno chirale (opposti/uguali) da' i due generatori non commutanti.
        # [A8, 2026-09-20] (c) RAGIONE SCADUTA: `perc_chi` e' estesa da tutte e tre le vie di
        # crescita di `n`, quindi `len(perc_chi) >= n` non puo' essere falso. Si conta per
        # DIMOSTRARLO. L'`else` qui c'e' gia' ed e' esplicito: manca solo il numero.
                # ✅ MISURATO: **0 salti su 12**, ma in `W3` SCATTA corrompendo `perc_chi`. CLASSE:
        # **(c) DEBOLE** -- la guardia E' raggiungibile da uno stato malformato, anche se nessun
        # percorso del codice lo produce oggi. Qui il contatore ha valore OPERATIVO, non solo di
        # sentinella: e' protetta da un'INVARIANTE che tre funzioni mantengono, non dalla forma.
        self._g_chicore_passo_tot = getattr(self, "_g_chicore_passo_tot", 0) + 1
        if CHI_CORE and len(self.perc_chi) >= n:
            chi_nodi = self.chiralita_core_locale()
        else:
            if CHI_CORE:
                self._g_chicore_passo_salti = getattr(self, "_g_chicore_passo_salti", 0) + 1
                self._g_chicore_passo_shape = (len(self.perc_chi), n)
                self._g_chicore_passo_quando = self._g_chicore_passo_tot
            chi_nodi = self.perc_chi[:n].astype(float)
        chi = (chi_nodi[i] * chi_nodi[j]).astype(float)  # +1 uguali / -1 opposti
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
        if SPIN_LARMOR:
            # Campo trasverso GEOMETRICO STAGGERED (non-abeliano): chiralita' del legame (+-1) *
            # torsione * (n_i x n_j). Il fattore staggered cl=chi_i*chi_j alterna il verso della
            # coppia coi domini chirali -> struttura antiferromagnetica/onda di spin che NON si
            # auto-spegne con l'ordine ferromagnetico (a differenza della media dei vicini).
            # Perpendicolare a n, asse dalla torsione e dalla chiralita' (stato), zero parametri.
            twL = np.abs(self.tw[mask]) / max(PHI_CRIT, 1e-9)
            stag = cl * twL
            cross_ij = np.cross(nb_vic[ii], nb_vic[jj])
            Bg = np.zeros((n, 3)); degg = np.zeros(n)
            np.add.at(Bg, ii,  cross_ij * (wl * stag)[:, None]); np.add.at(degg, ii, wl)
            np.add.at(Bg, jj, -cross_ij * (wl * stag)[:, None]); np.add.at(degg, jj, wl)
            Bg = Bg / np.maximum(degg[:, None], 1e-9)
            B = B + Bg
        # INERZIA = |Psi|^2 (la materia mantiene il moto), come in mem_mot
        if not hasattr(self, "psi") or len(self.psi) < n: self.calcola_psi()
        # [CORREZIONE DI DIFETTO, 2026-09-16 - decisione di Luca] IL FATTORE `cs^-2` NELL'INERZIA.
        # DERIVAZIONE, non taratura (doc/INERZIA_tempo_quadro.md, esito (b)):
        #   `correzione` e' ADIMENSIONALE e `omega` e' `1/T`, quindi `correzione/inerzia` deve
        #   dare `1/T^2`  =>  **`inerzia` E' UN TEMPO AL QUADRATO**. Il tempo proprio del nodo e'
        #   `lunghezza/velocita' = d/cs`, quindi `inerzia ∝ (d/cs)^2 ∝ cs^-2`.
        #   L'ESPONENTE E' DERIVATO (non scelto), IL VERSO E' CONFERMATO (Compton con c -> cs: nel
        #   pozzo l'orologio rallenta, redshift), ed e' LO STESSO ESPONENTE dello Step 2
        #   (`omega_clk *= (cs/CS_M)^2`), derivato PRIMA e INDIPENDENTEMENTE: consistenza TROVATA,
        #   non costruita.
        # FORMA: si moltiplica per `(CS_M/cs_nodo)^2`, che e' ADIMENSIONALE e vale ESATTAMENTE 1
        # dove `cs = CS_M` -> riduzione al limite ESATTA (sigillo M2). Nessun coefficiente nuovo,
        # nessun floor nuovo: il floor resta `1e-6` e si applica al RISULTATO, cioe' alla grandezza
        # per cui si divide davvero.
        # PERCHE' E' UNA CORREZIONE DI CONSERVAZIONE E NON UN'AGGIUNTA: alla mitosi il figlio
        # riceve un'inerzia NUOVA e il padre non ne perde, quindi `L_tot = sum(I*omega)` CRESCE a
        # ogni divisione. `omega` e' intensiva (un corpo rigido che si spezza mantiene `omega` in
        # ogni frammento): e' l'INERZIA che deve ripartirsi. Con `inerzia ∝ cs^-2`, quando nasce un
        # figlio la densita' locale sale, `cs` locale cala, e l'inerzia di PADRE E FIGLIO aumenta
        # insieme: un feedback MEDIATO DAL CAMPO, che e' il modo in cui la fisica lo fa, e che non
        # richiede di sottrarre nulla al padre (impossibile: `|psi|^2` e' ricalcolata dalle fasi,
        # non e' una variabile di stato).
        # ⚠ ATTESA QUANTITATIVA, scritta PRIMA: `cs_std/cs_medio` sta fra 0.0086 % e 0.24 % in
        # questo regime (C13), quindi IL FATTORE SARA' QUASI 1 OVUNQUE e l'effetto OGGI sara'
        # MINUSCOLO. Si fa perche' senza la legge e' SBAGLIATA, non per un effetto misurabile a
        # questa densita'. Diventera' rilevante dove `cs` si sveglia davvero.
        # NB - GEMELLO DA TENERE ALLINEATO: la stessa lettura di `_cs_nodo_prev` (cache + fallback
        # a CS_M) sta in `_tempo_luce_nodo`. Sono due punti, non uno: se un giorno la legge di `cs`
        # cambia, vanno cambiati ENTRAMBI. Non l'ho estratta in un metodo di proposito: oggi tre
        # sigilli si sono rotti proprio perche' un metodo estratto non era nei gusci in-process.
        _csp_in = getattr(self, "_cs_nodo_prev", None)
        self._cs_in_chiamate = getattr(self, "_cs_in_chiamate", 0) + 1
        if _csp_in is not None and len(_csp_in) >= n:
            _cs_in = np.maximum(np.asarray(_csp_in, float)[:n], 1e-12)
        else:
            self._cs_in_fallback = getattr(self, "_cs_in_fallback", 0) + 1   # P5: si CONTA
            _cs_in = np.full(n, CS_M)
        # ⚠ `_fatt_cs` NON entra piu' nell'inerzia: la forma nuova contiene gia' `cs^-2` dentro
        # `(d/cs)^2`, e lasciarlo darebbe `cs^-4`. Resta come DIAGNOSTICO, e va detto che non ha
        # lettori: una sola occorrenza nel file, ed e' questa scrittura (voce Z7 del registro,
        # quarto caso dopo _passo_spinoriale/VERSO_CHI/spin_locale).
        _fatt_cs = (CS_M / _cs_in) ** 2                    # adimensionale, == 1 dove cs == CS_M
        self._fatt_cs_ultimo = _fatt_cs                    # DIAGNOSTICO: nessun lettore (Z7)

        # ================= INERZIA DIMENSIONALE (par.10 categoria D: NESSUN FLAG) =================
        # Era:  inerzia = max(rho_sorgente * (CS_M/cs)^2, 1e-6)
        # IL DIFETTO ERA DIMENSIONALE, non una taratura. `coppia = cross(B, nb)` e' versore x
        # versore, quindi ADIMENSIONALE e di ordine 1; `|psi|^2` grezzo e' ~1e-7. Sette ordini, e
        # nessuna dimensione che li leghi. Ma da `omega = coppia/inerzia` con `omega ~ 1/T` segue
        # che **l'inerzia E' UN TEMPO AL QUADRATO** (doc/INERZIA_tempo_quadro.md, confermato su tre
        # punti: dimensione, esponente cs^-2, verso). MISURATO su questo codice: il pavimento 1e-6
        # era attivo sul **100.00 %** dei nodi a ogni passo -- `inerzia` non era "quasi sempre al
        # pavimento", ERA il pavimento -- mentre `_fatt_cs` saliva fino a 6.43 senza servire a
        # nulla. Rapporto T^2/inerzia misurato: **1.03e+06**.
        #
        # ASSIOMA A6 (TEOREMA, residuo 1.57e-15) -- LA RAGIONE PRIMARIA, e non e' numerica:
        # `omega_new = omega_src + dtn_c * (correzione/inerzia - omega_src/_tau)`. Se `inerzia`
        # fosse calcolata dallo stato DI QUESTO PASSO, sarebbe una funzione istantanea di cio' che
        # sta per essere modificato: **uno specchio, non una resistenza**. In meccanica la massa si
        # valuta a `t`, non a `t+dt`.
        # ⚠ E QUI A6 E' SODDISFATTO PER COSTRUZIONE, non da uno snapshot aggiunto: questo blocco
        # gira a riga ~3062, mentre `peq` e' aggiornato a ~3147/3165, `d` a ~3243 e `_cs_nodo_prev`
        # e' scritto a ~3138. **Tutte le grandezze lette qui sono gia' quelle del passo precedente.**
        # (Verificato dal DISCO, non dedotto: csv/_test_fork/_verifiche_inerzia.txt.)
        #
        # ASSIOMI: A6 (primaria) - A1 (zero parametri: rho, peq, d, cs sono tutti di stato)
        #          A2 (`peq` e' lo sfondo DIFFUSO LOCALE, Legge I :265; nessuna statistica globale)
        #          A3 (dopo la proiezione arco->nodo numeratore e denominatore vivono entrambi
        #              sui NODI: stessa popolazione) - A5 (`d/cs` e' il tempo causale)
        #          A4 (nessun DT nudo introdotto) - A8 (il fallback sotto e' CONTATO).
        # Sigillo: csv/_seal_fork/_sigillo_inerzia.py  (Y0-Y10)
        _T = self._tempo_luce_nodo(i, j)                   # d_nodo/cs_nodo, UNICO punto della legge
        _T2 = _T * _T                                      # = T^2, la dimensione dell'inerzia

        # proiezione arco->nodo di `peq`: media sugli archi INCIDENTI -- la stessa forma gia' usata
        # per `den_w` (~:3151), e la grandezza su cui GATE A e' stato misurato.
        _peq_a = np.asarray(self.peq, float)
        # [A8 - DIAGNOSI DELLE DUE PORTE, 2026-09-17] SOLO CONTATORI, nessuna logica toccata.
        # Il fallback dello sfondo ha DUE porte, che portano a diagnosi OPPOSTE:
        #   PORTA A  len(self.peq) != len(self.i)  -> `peq` e topologia sono di due momenti
        #            diversi. E' un difetto di LUNGHEZZA (A8b: cache cross-passo letta con una
        #            topologia che nel frattempo e' cambiata).
        #   PORTA B  le lunghezze combaciano, ma `peq` e' NaN o <= 0 -> letto PRIMA della sua
        #            calibrazione (~:3263). E' un difetto di VALORE.
        # Un TOTALE non distingue le due, ed e' esattamente il numero che non serve.
        self._por_invoc = getattr(self, "_por_invoc", 0) + 1
        if len(_peq_a) != len(self.i):
            self._porta_A = getattr(self, "_porta_A", 0) + 1
            self._porta_A_ultima = self._por_invoc
            self._porta_A_shape = (len(_peq_a), len(self.i))
        else:
            _nan = int(np.sum(~np.isfinite(_peq_a)))
            _nonpos = int(np.sum(np.isfinite(_peq_a) & (_peq_a <= 0)))
            if _nan or _nonpos:
                self._porta_B = getattr(self, "_porta_B", 0) + 1
                self._porta_B_ultima = self._por_invoc
                self._porta_B_nan = getattr(self, "_porta_B_nan", 0) + _nan
                self._porta_B_nonpos = getattr(self, "_porta_B_nonpos", 0) + _nonpos
        _ok_a = np.isfinite(_peq_a) & (_peq_a > 0) if len(_peq_a) == len(self.i) else np.zeros(len(self.i), bool)
        if _ok_a.any():
            _sp = (np.bincount(self.i[_ok_a], _peq_a[_ok_a], minlength=n) +
                   np.bincount(self.j[_ok_a], _peq_a[_ok_a], minlength=n))
            _cn = (np.bincount(self.i[_ok_a], minlength=n) +
                   np.bincount(self.j[_ok_a], minlength=n))
            _peq_nodo = np.where(_cn[:n] > 0, _sp[:n] / np.maximum(_cn[:n], 1), 0.0)
        else:
            _peq_nodo = np.zeros(n)

        # IL FALLBACK DEL PRIMO PASSO, con la convenzione GIA' USATA SOPRA per `_cs_nodo_prev`:
        # quando lo stato precedente non e' utilizzabile si prende il valore che rende il fattore
        # NEUTRO -- li' `CS_M` (cioe' _fatt_cs = 1), qui **contrasto = 1**.
        # NON E' UNA CONVENZIONE NUOVA, ed e' importante: il codice sostituisce gia' `peq` con
        # `rho` quando `peq` e' NaN, in DUE punti (~:3544 e ~:3657,
        # `np.where(np.isnan(peq_sel), rho_sel, peq_sel)`), e `rho/rho = 1`. Il neutro **e'** il
        # limite di quella sostituzione, non un numero scelto (A1).
        # PERCHE' SERVE: ai passi 0 e 1 `peq` non e' MAI stato calibrato (la calibrazione sta a
        # ~:3147, DOPO questo punto) e vale NaN, poi 0 -- su TUTTI i nodi, misurato. Senza questo
        # ramo `rho/peq = 0/0 = NaN` finirebbe in `self.omega_s`, **la memoria persistente**, e
        # `np.maximum(NaN, 1e-6)` **e' NaN**: il pavimento non protegge.
        # A8: si CONTA, e la previsione scritta prima dice che deve scattare solo nel transitorio.
        _rho_s = self._rho_sorgente()
        _ok_n = (np.isfinite(_peq_nodo) & (_peq_nodo > 0) &
                 np.isfinite(_rho_s) & (_rho_s > 0))
        self._inerzia_sfondo_chiamate = getattr(self, "_inerzia_sfondo_chiamate", 0) + int(n)
        self._inerzia_invocazioni = getattr(self, "_inerzia_invocazioni", 0) + 1
        if not bool(np.all(_ok_n)):
            # [A8 - LA TERZA SEPARAZIONE, 2026-09-17] QUALE delle due condizioni di `_ok_n` cade?
            # La diagnosi delle due porte ha escluso sia la LUNGHEZZA (porta A: 0) sia il VALORE di
            # `peq` (porta B: solo nel transitorio, ultima invocazione 8 su 66). Resta `rho_s`.
            # Senza questo contatore la causa si dedurrebbe invece di misurarla.
            _ko_peq = int(np.sum(~(np.isfinite(_peq_nodo) & (_peq_nodo > 0))))
            _ko_rho = int(np.sum(~(np.isfinite(_rho_s) & (_rho_s > 0))))
            self._sfondo_ko_peq = getattr(self, "_sfondo_ko_peq", 0) + _ko_peq
            self._sfondo_ko_rho = getattr(self, "_sfondo_ko_rho", 0) + _ko_rho
            self._sfondo_ko_ultima_rho = self._por_invoc if _ko_rho else getattr(self, "_sfondo_ko_ultima_rho", 0)
            self._sfondo_ko_ultima_peq = self._por_invoc if _ko_peq else getattr(self, "_sfondo_ko_ultima_peq", 0)
            # [A8] i NODI che cadono nel fallback PUR AVENDO archi (grado > 0): distingue
            # "nessun arco valido da cui leggere lo sfondo" da "archi validi ma somma nulla".
            _grado_n = (np.bincount(self.i, minlength=n)[:n] +
                        np.bincount(self.j, minlength=n)[:n]) if len(self.i) else np.zeros(n)
            _con_archi = int(np.sum((~_ok_n) & (_grado_n > 0)))
            self._sfondo_ko_con_archi = getattr(self, "_sfondo_ko_con_archi", 0) + _con_archi
            self._sfondo_ko_senza_archi = (getattr(self, "_sfondo_ko_senza_archi", 0)
                                           + int((~_ok_n).sum()) - _con_archi)
            self._inerzia_sfondo_fallback = getattr(self, "_inerzia_sfondo_fallback", 0) + int((~_ok_n).sum())
            self._inerzia_sfondo_passi = getattr(self, "_inerzia_sfondo_passi", 0) + 1
            # A8: non basta QUANTE volte scatta, serve QUANDO. Un fallback confinato alle prime
            # invocazioni e' un transitorio; uno sparso e' il comportamento principale, e i due
            # casi danno lo stesso conteggio. (Criterio scritto da questa distinzione, par.9.)
            self._inerzia_sfondo_ultima = self._inerzia_invocazioni
        # ====================================================================================
        # [`INERZIA-1(C)`, decisione di Luca 2026-09-25] IL NUMERATORE DIVENTA «PER VICINO»
        # ------------------------------------------------------------------------------------
        #   `_peq_nodo` E' GIA' UNA MEDIA (`_sp/_cn`, tre righe sopra). Qui il numeratore usa
        #   **LO STESSO `_cn`**, cosi' numeratore e denominatore sono **entrambi per vicino** e
        #   il rapporto **non scala col grado**.
        #   ⚠ **`_cn` conta gli archi VALIDI** (`peq` finito e positivo), non tutti: e' il
        #   medesimo insieme su cui `_peq_nodo` fa la media. **Usare un conteggio diverso
        #   sarebbe l'errore di POPOLAZIONE di `A3`** -- numeratore e denominatore su insiemi
        #   diversi -- cioe' esattamente il difetto che questa cura sta togliendo.
        #   ⚠ **`_cn = None`** (nessun arco valido) **NON si aggira con un `1`:** in quel caso
        #   `_ok_n` e' falso e `_contrasto` vale **1** per la convenzione del primo passo. Il
        #   ramo e' CONTATO, non assunto impossibile (`P5`).
        # ✅ [VARIANTE PESATA, decisione di Luca 2026-09-25] **SI NORMALIZZA SULLA SOMMA DEI
        #   PESI, NON SUL CONTEGGIO.** `w` e' **gia' un parametro di questa funzione**, ed e' lo
        #   STESSO `w` che `calcola_psi` passa a `_mat(w)` per costruire `psi_spin`: la somma per
        #   nodo e' **la somma di riga di `_mat(w)`**. **Nessuna grandezza nuova.**
        #   ⚠ **IL PRIMO TENTATIVO (per CONTEGGIO) E' MISURATO E INSUFFICIENTE**, sigillo `3/6`:
        #     toglieva **esattamente `-1.0000`** di pendenza in 4 bracci su 4, e restava un
        #     residuo **`+0.49`** (via i lunghi) e **`+1.34`** (via i corti). **Resta nel
        #     registro come tentativo misurato**, non nel codice.
        #   ⚠ **E UNA COSA DA SAPERE PRIMA DI LEGGERE I NUMERI:** `rho_spin` e' il **MODULO
        #     QUADRO** di `psi_spin`, che a sua volta e' una somma pesata -> **`rho_s ~ W^2`**.
        #     Dividere per `W` **una volta** toglie **una** potenza: se la dipendenza e'
        #     quadratica il residuo **non si azzera**, e la forma coerente sarebbe `W^2`.
        #     **E' scritto nel task history PRIMA della misura**, perche' dopo sembrerebbe una
        #     scusa. Il numero distingue le due ipotesi.
        _rho_c = _rho_s
        if CONTRASTO_INTENSIVO:
            self._g_ci_tot = getattr(self, '_g_ci_tot', 0) + 1
            _wn = None
            if w is not None and len(np.asarray(w)) == len(self.i):
                _wa = np.asarray(w, float)
                _wn = (np.bincount(self.i, _wa, minlength=n)[:n]
                       + np.bincount(self.j, _wa, minlength=n)[:n])
            if _wn is None:
                # nessun peso d'arco utilizzabile AFFATTO (lunghezze incoerenti): qui il ramo e'
                #   davvero globale, perche' manca l'ARRAY, non un valore.
                self._g_ci_senza_array = getattr(self, '_g_ci_senza_array', 0) + 1
                self._g_ci_senza_array_quando = int(self._g_ci_tot)
                self._g_ci_senza_array_forma = (int(len(np.asarray(w))) if w is not None else -1,
                                               int(len(self.i)))
            else:
                # ❌❌ **DIFETTO MIO, RILEVATO DA LUCA il 2026-09-25 (P6): IL RIPIEGO ERA GLOBALE
                #   SU UNA CONDIZIONE LOCALE.** La forma di prima era
                #   `if ... or np.any(_wn <= 0.0):` -> **UN SOLO nodo con somma dei pesi zero
                #   spegneva la cura per TUTTO IL SISTEMA in quel passo.**
                #   **E non era un caso raro: era IL CASO.** I figli della mitosi nascono con
                #   `ramp = 0`, quindi i loro archi hanno `w = 0` e la loro somma e' `0`:
                #   **ogni nascita spegneva la cura per l'intera rete** -- e i figli sono
                #   **esattamente cio' che la cura doveva sistemare.**
                #   ✅ **ORA IL RIPIEGO E' PER NODO** (`np.where`), e i contatori sono **per
                #   NODO**, non per invocazione: *quanti nodi senza peso* e *quanti di questi
                #   NATI IN DINAMICA*. **Un ripiego globale su una condizione locale e' un
                #   verdetto vacuo mascherato**, e sarebbe passato per un `PASS`.
                _ok_w = np.isfinite(_wn) & (_wn > 0.0)
                # ✅ [CURA A, DECISIONE DI LUCA 2026-09-26] **`W` AL QUADRATO, non `W`.**
                #   **MISURATO sui figli della mitosi** (`csv/_test_fork/_scomposizione_figli.py`,
                #   2 semi, `K1` PASS su 4300 campioni): `rho ~ ramp^2.74` e `W ~ ramp^1.37`,
                #   quindi **`rho ~ W^2.00`** — `2.00` esatto, `R2` `0.95`-`0.96`. `rho_s` e' il
                #   **modulo quadro** di una somma pesata, e dividere per `W` **una volta**
                #   toglieva **una** potenza: la variante `/W` dimezzava il divario di pendenza
                #   (`1.25 -> 0.62`, `2.78 -> 1.44`) **senza chiuderlo**.
                #   E la scomposizione lo conferma dall'altro lato: il termine `W^2` (`T2`) e' il
                #   **`107`-`114 %`** del divario dei figli, mentre il `peq` EREDITATO (`T3`) e'
                #   **`-3` a `-6 %`**, cioe' va nella direzione OPPOSTA.
                #   ❌ **CORREZIONE DEL 2026-09-26 (rilievo di Luca) — ERRORE DI UNITA' MIO.**
                #   **Cio' che avevo scritto:** *«l'asimmetria sui figli e' `0` contro `2.8` e `W^2`
                #   ne toglie `2`: **resta `0.8`**. Questa cura non chiude quello.»*
                #   **SBAGLIATO: ho sottratto 2 potenze di `W` da 2.8 potenze di `ramp`** — due basi
                #   diverse. **Il conto giusto:** `W ~ ramp^1.37`, quindi `W^2 ~ ramp^2.74`, e
                #   `inerzia/W^2 ~ ramp^(2.80-2.74) = ramp^0.06`; la coppia va come `ramp^0.10`,
                #   quindi il residuo e' **`0.06 - 0.10 = -0.04`, cioe' ZERO entro il rumore.**
                #   **E IL DATO LO CONFERMAVA GIA':** `exp(T1+T3)` e' **piatto** su eta' `2..14`
                #   (`x1.00`-`x1.08`) mentre `ramp` cresce `x5.20`. Con `0.8` potenze residue
                #   varierebbe di **`x3.74`**; con `0.06`, di `x1.10`. **La piattezza esclude `0.8`
                #   di un fattore quattro, e stava nel referto che avevo scritto io.**
                #   ⇒ **`W^2` non e' una correzione parziale: chiude l'esponente.** La frase
                #   «questa cura non chiude quello» era **troppo PESSIMISTA**, non troppo ottimista.
                #   *(Quello che resta davvero fuori: la coppia non porta `ramp`, e **questo non e'
                #   un difetto dell'inerzia** — e' una domanda sul termine `_tq*ramp`.)*
                #   ⚠ E IL RISCHIO VERO: dividere DUE volte abbassa l'inerzia due volte, quindi
                #   **il pavimento `1e-6` e' il criterio da guardare** (`C5`). Con `/W` non mordeva
                #   (min `0.0655`, quattro ordini sopra).
                _rho_c = np.where(_ok_w, _rho_s / np.where(_ok_w, _wn * _wn, 1.0), _rho_s)
                _senza = int(np.sum(~_ok_w))
                self._g_ci_nodi_senza_peso = getattr(self, '_g_ci_nodi_senza_peso', 0) + _senza
                self._g_ci_nodi_tot = getattr(self, '_g_ci_nodi_tot', 0) + int(n)
                if _senza:
                    self._g_ci_senza_peso_quando = int(self._g_ci_tot)
                    # **QUANTI DI QUESTI SONO NATI IN DINAMICA:** i nodi del vuoto DATO hanno
                    #   `eta = +inf` (`RAMPA-1`), i nati in dinamica un `eta` FINITO. ⚠ Il
                    #   discriminante esiste **solo con `SEMINA_MATURA` acceso**: senza, `eta` e'
                    #   finito per tutti e il contatore vale `-1`, **dichiarato invece che finto**.
                    _et = np.asarray(getattr(self, 'eta', []), float)
                    if SEMINA_MATURA and _et.size >= n:
                        _nati = int(np.sum(~_ok_w & np.isfinite(_et[:n])))
                    else:
                        _nati = -1
                    self._g_ci_senza_peso_nati = (getattr(self, '_g_ci_senza_peso_nati', 0)
                                                  + _nati) if _nati >= 0 else -1
                _wv = _wn[_ok_w]
                if _wv.size:
                    self._g_ci_w_p50 = float(np.median(_wv))
                    self._g_ci_w_min = float(_wv.min())
                    self._g_ci_w_max = float(_wv.max())
                self._g_ci_nodi = int(n)
        _contrasto = np.where(_ok_n, _rho_c / np.where(_ok_n, _peq_nodo, 1.0), 1.0)
        inerzia = np.maximum(_contrasto * _T2, 1e-6)       # il pavimento RESTA: deve diventare inerte
        self._inerzia_al_pavimento = getattr(self, "_inerzia_al_pavimento", 0) + int(np.sum(_contrasto * _T2 <= 1e-6))
        self._inerzia_tot = getattr(self, "_inerzia_tot", 0) + int(n)
        dtn = dt_n if np.isscalar(dt_n) else np.asarray(dt_n)[:n]
        dtn_c = dtn if np.isscalar(dtn) else dtn[:, None]
        # MEMORIA HEBBIANA: omega si conserva + correzione dal campo (torsione B x n) - decadimento
        correzione = np.cross(B, nb)                      # la geodetica che piega il momento (canale chirale B_geo)
        if CAMPO_SPINORIALE:
            # [FASE 4] ARRICCHIMENTO non-abeliano: AGGIUNGO il torque verso il Bloch del CAMPO EMESSO
            # spinoriale (porta il segno relativo dei vicini via interferenza). Identita': cross(nb_campo, nb)
            # = cross(nb_campo - nb, nb) (perche' cross(nb,nb)=0) -> ZERO nel limite (nb_campo=nb=polo) ->
            # riduzione esatta. Mantiene i generatori chirali di B; nessun parametro (peso 1.0); snapshot t-1.
            # [RECIPROCITA', 2026-09-19 -- flag OFF di default, byte-identico a spento]
            # ⚠ IL DIFETTO CHE CURA, MISURATO (doc/REFERTO_verifica_reciprocita.md):
            #   `A7b` dice che un nodo appena nato NON PESA. NON dice cosa RICEVE.
            #   Il TERMINE 1, cross(B, nb), e' gia' reciproco DA SOLO: B = somma(nb*w)/somma(w), e
            #   per un neonato i pesi sono ESATTAMENTE zero -> deg = 0 -> B = 0.
            #   Il TERMINE 2 no: `_nb_grav()` divide per `rho_spin`, quindi e' un VERSORE
            #   (|_nb_grav| = 1.000000 a p05, p50 e p95) e l'ampiezza del campo NON entra.
            #   MISURATO sul nodo 2393 (neonato, peso [0. 0.], rho 5.7e-10): coppia = 0.3809,
            #   cioe' 4.9 VOLTE la mediana dei nodi maturi. Non riceve "come gli altri": riceve
            #   CINQUE VOLTE -- e piu' il nodo e' debole, piu' il versore e' "puro".
            # LA FORMA: si MOLTIPLICA per il peso che gia' esiste. NIENTE `if`, NIENTE soglie:
            #   un `if ramp < X` introdurrebbe un numero scelto (A1) e una DISCONTINUITA'.
            #   `ramp` cresce con `eta`, quindi il neonato entra GRADUALMENTE come sorgente E come
            #   ricevente: non e' escluso, e' PESATO.
            # E' `ramp[k]`, NODALE, perche' la coppia e' nodale: cross(B, nb) e cross(nbg, nb) sono
            #   (n,3) per NODO e non hanno indici d'arco. Deciso DAL CODICE, non scelto.
            # NON si toccano: il pavimento 1e-6, `A7b`, il peso zero alla nascita, il termine 1.
            _tq = np.cross(self._nb_grav(), nb)
            if GRAV_AMPIEZZA:
                # [GRAV_AMPIEZZA, 2026-09-19 -- flag OFF di default, byte-identico a spento]
                # UNA DIREZIONE NON E' UNA FORZA. `_nb_grav()` divide per `rho_spin` (la norma di
                # Bloch E' rho_spin per identita'), quindi e' un VERSORE: |_nb_grav| = 1.000000 a
                # p05, p50 e p95. Il suo docstring lo dice -- "DIREZIONE di Bloch per la gravita'"
                # -- ed e' nato per dare un VERSO: qualcuno ha assunto che l'ampiezza arrivasse da
                # un'altra parte. VERIFICATO DAL DISCO (ee80c7d) che non arriva:
                #   `_pesi()` contiene d, ramp, tw -- NON rho_spin; nb_vic/nb/_nb_grav sono tutti
                #   VERSORI; e `rho_spin` compare UNA SOLA VOLTA nella catena, AL DENOMINATORE
                #   (`_contrasto = rho_s/peq_nodo`, `inerzia = max(_contrasto*_T2, 1e-6)`).
                #   Quindi piu' il campo e' debole, piu' `omega` e' grande: l'opposto di una forza.
                # SI RIMOLTIPLICA QUI E NON DENTRO `_nb_grav()`: l'altro consumatore (:4384) la usa
                # per un PRODOTTO INTERNO fra versori, cioe' un COSENO, dove la normalizzazione e'
                # corretta e voluta. Togliere la divisione la' romperebbe quel punto.
                # `_rho_sorgente()` e NON `rho_spin` diretto: e' LO STESSO metodo che alimenta
                # `_contrasto`, quindi numeratore e denominatore parlano della STESSA grandezza.
                # NESSUN numero nuovo, NESSUN tetto, NESSUN clamp, NESSUNA saturazione.
                _tq = _tq * self._rho_sorgente()[:, None]
            if COPPIA_RECIPROCA:
                # la STESSA riga di `_pesi()` (:2649): nessun numero nuovo
                # [CURA 4] DEVE seguire `_pesi`: il commento sopra dice "la STESSA riga di
                #   `_pesi()`", e se una delle due usasse `TAU_A` e l'altra il tempo-luce
                #   sarebbero DUE leggi che possono divergere -- esattamente la ragione per cui
                #   `_tempo_luce_nodo` fu ESTRATTO in un metodo solo. `_tempo_rampa()` restituisce
                #   `TAU_A` a flag spento, quindi questa riga e' BYTE-IDENTICA a prima.
                _trq = self._tempo_rampa()
                _trq = np.asarray(_trq, float)[:n] if np.ndim(_trq) else _trq
                _tq = _tq * np.minimum(1.0, self.eta[:n] / _trq)[:, None]
            correzione = correzione + _tq
        # VITA MEDIA LOCALE (ispirata al decadimento atomico / regola d'oro di Fermi): TAU_A non e'
        # piu' un numero fisso ma una PROPRIETA' DELLO STATO. Come ogni isotopo ha la sua vita media,
        # ogni nodo ha la sua: stati fortemente legati (|Psi|^2 grande, nucleo coerente) decadono
        # LENTAMENTE (nucleo stabile); stati deboli (|Psi|^2 piccolo, alone) decadono in FRETTA (stato
        # eccitato instabile). TAU_A_locale = TAU_A*|Psi|^2 / densita' mediana (coefficiente calibrato,
        # nessun numero nuovo). IN VERIFICA: stabile, ma il guadagno sul decadimento lungo non e'
        # ancora confermato (manca il confronto lungo TAU_A-fisso vs locale). Reversibile: se
        # TAU_A_LOCALE=False torna al comportamento fisso.
        if TAU_LUCE:
            # [FASE 2] TEMPO-LUCE: il rilassamento usa la STESSA scala temporale che costruisce
            # l'inerzia, `d/cs`. Nessun coefficiente, nessun floor nuovo: e' `_tempo_luce_nodo()`,
            # l'unico posto in cui la legge e' scritta, gia' usato dallo Strato 1.
            _tau = self._tempo_luce_nodo(i, j)[:, None]
        elif TAU_A_LOCALE:
            _dens = np.abs(self.psi[:n])**2
            _dens_rif = max(float(np.median(_dens[_dens > 1e-6])), 1e-6) if np.any(_dens > 1e-6) else 1.0
            _tau = TAU_A * np.maximum(_dens / _dens_rif, 0.05)   # vita media locale, pavimento 0.05
            _tau = _tau[:, None]
        else:
            _tau = TAU_A
        omega_src = self.omega_s
        omega_new = omega_src + dtn_c * (correzione / inerzia[:, None] - omega_src / _tau)
        if TW_SPINORE:
            # DOPPIA COPERTURA: la torsione a 4pi (tw) pilota il Bloch. Angolo = tw/2 (spin-1/2,
            # geometrico, NON una manopola) attorno all'asse sigma FISSO dalla chiralita' del legame
            # (sigma_x uguali, sigma_z opposti) -> asse persistente, non svanisce all'allineamento
            # (il difetto che spense SPIN_LARMOR). Il segno di tw da' il verso. Nessun parametro nuovo.
            _twh = self.tw[mask] / (2.0 * max(PHI_CRIT, 1e-9))
            _axis = np.where(cl[:, None] > 0, np.array([1.0, 0.0, 0.0]), np.array([0.0, 0.0, 1.0]))
            _otw = np.zeros((n, 3)); _degt = np.zeros(n)
            np.add.at(_otw, ii, _axis * _twh[:, None]); np.add.at(_degt, ii, 1.0)
            np.add.at(_otw, jj, _axis * _twh[:, None]); np.add.at(_degt, jj, 1.0)
            omega_new = omega_new + _otw / np.maximum(_degt[:, None], 1.0)
        # KURAMOTO SU(2) (--sync-spinore): torque di ALLINEAMENTO verso la media di vicinato degli
        # spinori. nb_media dallo snapshot t-1 (nb), forza = la STESSA del Kuramoto-phi. E' un torque
        # ISTANTANEO: entra nella rotazione (omega_sync, sotto), MAI in omega_s (memoria: darebbe
        # accumulo/divergenza). |nb_media| non normalizzato = coerenza locale (debole nel guscio frustrato).
        omega_sync = None
        if SYNC_SPINORE and forza_sync is not None and wI_sync is not None and uno_sync is not None:
            nb_media = (wI_sync @ nb) / uno_sync[:, None]
            omega_sync = np.asarray(forza_sync[:n])[:, None] * np.cross(nb, nb_media)
        # PRECESSIONE conservativa: ruoto il Bloch attorno a omega (rotazione esatta, unitaria)
        psi_sp_new = None
        if SPINORE_CORRETTO:
            # === OROLOGIO PROPRIO de Broglie + SPINORE PRIMARIO COMPLESSO (evaluate-then-commit) ===
            # L'asse dell'orologio e' l'asse di Bloch PROPRIO nb (pura FASE attorno a se', non
            # deviazione dell'asse): l'orologio di de Broglie e' un avanzamento e^{-i omega tau/2},
            # invisibile al Bloch, che pilota il SEGNO di doppia-copertura del primario. rho=|Psi|^2
            # (materia, snapshot t), rho_c=massa critica adattiva (legge di stato), r=ritmo proprio
            # RIUSATO (dt_n=DT*r, nessuna nuova chiamata a ritmo() -> nessuna mutazione di _psi_prec,
            # regola C). Nessun coefficiente libero.
            r_node = (np.asarray(dtn) / DT if not np.isscalar(dtn) else np.full(n, dtn / DT))
            if psi_snapshot is not None and len(psi_snapshot) >= n:
                rho = np.abs(psi_snapshot[:n]) ** 2
            elif len(self.psi) >= n:
                rho = np.abs(self.psi[:n]) ** 2
            else:
                rho = np.zeros(n)
            try:
                rho_c = float(massa_critica_adattiva(self))
            except Exception:
                rho_c = float(massa_critica_collasso())
            if DEPARAM_OROLOGIO:
                # DE-PARAM RELAZIONALE + PURA FASE: freq guidata dalla COERENZA D'ARCO intensiva (media
                # pesata di cos(phi_i-phi_j) sugli archi incidenti, indipendente dal grado), NON dalla
                # densita' estensiva / rho_c globale (~95% connettivita'). Tetto naturale 1: nessun rho_c,
                # niente volume. self.phi qui e' lo snapshot t (commit fasi non ancora avvenuto -> ETC).
                _m = (i < n) & (j < n)
                _ii, _jj, _wc = i[_m], j[_m], w[_m]
                _cij = np.cos(self.phi[_ii] - self.phi[_jj])
                _num = np.zeros(n); _den = np.zeros(n)
                np.add.at(_num, _ii, _wc * _cij); np.add.at(_num, _jj, _wc * _cij)
                np.add.at(_den, _ii, _wc);        np.add.at(_den, _jj, _wc)
                omega_clk = (_num / np.maximum(_den, 1e-12)) * r_node   # coerenza d'arco [-1,1] * ritmo proprio
                # PURA FASE: l'orologio NON entra nell'asse di rotazione (non inclina nb -> non tocca la
                # gravita' grav*=nb.nb); e' applicato SOTTO come fase globale e^{-i omega_clk dt/2}.
                omega_tot = omega_new if omega_sync is None else (omega_new + omega_sync)
            else:
                omega_clk = (rho / max(rho_c, 1e-12)) * r_node          # legacy: densita' estensiva / rho_c globale
                omega_tot = omega_new + omega_clk[:, None] * nb         # lungo l'asse PROPRIO (nb unitario)
                if omega_sync is not None:
                    omega_tot = omega_tot + omega_sync                  # torque di allineamento SU(2) (istantaneo)
            # spinore primario: init da Bloch corrente se assente/nuovo (la mitosi eredita il complesso;
            # qui e' solo fallback/primo-init). Legge lo snapshot t-1 di _psi_spinor.
            self._estendi_psi_spinor(n, nb)
            psi_sp_t = self._psi_spinor
            _dts = (np.asarray(dtn) if not np.isscalar(dtn) else np.full(n, dtn))
            _on = np.linalg.norm(omega_tot, axis=1)
            theta = _on * _dts                                       # angolo di rotazione SU(2)
            nhat = omega_tot / np.maximum(_on[:, None], 1e-12)
            c = np.cos(theta / 2.0); s = np.sin(theta / 2.0)
            nx, ny, nz = nhat[:, 0], nhat[:, 1], nhat[:, 2]
            a0 = psi_sp_t[:, 0]; b0 = psi_sp_t[:, 1]
            # U = exp(-i/2 omega.sigma dt) applicato allo spinore t-1
            a1 = (c - 1j * s * nz) * a0 + (-1j * s * (nx - 1j * ny)) * b0
            b1 = (-1j * s * (nx + 1j * ny)) * a0 + (c + 1j * s * nz) * b0
            if DEPARAM_OROLOGIO:
                # OROLOGIO PURA FASE de Broglie: fase globale e^{-i omega_clk dt/2} sullo spinore. Lascia
                # nb = psi^dag sigma psi INVARIANTE (una fase globale non cambia nb -> gravita' grav*=nb.nb
                # intatta); vincola SOLO il segno di doppia-copertura (arg<canon(nb)|psi>). E' la de Broglie
                # 'pura': avanzamento invisibile al Bloch, pilota il SEGNO non la DIREZIONE.
                # MOD 5.3c (--orologio-segno): VERSO firmato dal segno di doppia-copertura STABILE
                # s_k=sign(perc_chi) (lignaggio, non l'istantaneo che oscilla): materia exp(-), antimateria
                # exp(+), tempi SPECULARI (|omega_clk| invariata). OFF: s_k=1.0 -> byte-identico. Tutta-materia
                # (s_k=+1) -> esatto. Fase globale: tocca SOLO il segno, non nb/gravita'/eta.
                _sk = (np.where(np.asarray(self.perc_chi[:n]) >= 0.0, 1.0, -1.0)
                       if (OROLOGIO_SEGNO and hasattr(self, "perc_chi") and len(self.perc_chi) >= n) else 1.0)
                if STEP2_OROLOGIO:
                    # [STEP 2] OROLOGIO DI COMPTON: omega ∝ cs^2. `cs` dal passo PRECEDENTE, perche'
                    # il settore metrico gira DOPO questo punto; assente -> CS_M -> fattore 1 esatto.
                    # NIENTE floor, NIENTE coefficiente: solo (cs/CS_M)^2 (par.3, zero manopole).
                    # Tocca la MAGNITUDINE, mai il segno: _sk resta quello che e'.
                    _csp2 = getattr(self, "_cs_nodo_prev", None)
                    if _csp2 is not None and len(_csp2) >= n:
                        _csn2 = np.maximum(np.asarray(_csp2, float)[:n], 0.0)
                    else:
                        _csn2 = np.full(n, CS_M)
                    omega_clk = omega_clk * (_csn2 / CS_M) ** 2
                _phc = np.exp(-0.5j * _sk * omega_clk * _dts)
                a1 = a1 * _phc; b1 = b1 * _phc
            if SYNC_FASE_OROLOGIO and forza_sync is not None and wI_sync is not None and uno_sync is not None:
                # KURAMOTO SUL SEGNO DI DOPPIA-COPERTURA (sync-fase-orologio, §43): ordina il foglio +- in modo
                # RELAZIONALE. alpha_k = arg<canon(nb_k)|psi_k> (fase di doppia-copertura, snapshot t-1); torque
                # O(dt^1) verso la media di vicinato: eta = dt*forza*sin(media_alpha-alpha). Fase GLOBALE e^{i eta}
                # su psi -> nb = psi^dag sigma psi INVARIANTE (gravita' intatta), agisce SOLO sul segno. forza/wI/uno
                # = gli stessi del Kuramoto-phi (zero parametri). ETC: alpha e la media dei vicini dallo snapshot
                # t-1 (psi_sp_t, nb), applicati simultaneamente -> il segno di k influenza j solo a t+1.
                _canon_s = self._bloch_a_spinore(nb[:n])
                _ov_s = np.sum(np.conj(_canon_s) * psi_sp_t, axis=1)         # e^{i alpha}, snapshot t-1
                _za = _ov_s / np.maximum(np.abs(_ov_s), 1e-12)               # fasore unitario del segno
                _Za = (wI_sync @ _za) / uno_sync                             # media di vicinato pesata (snapshot t-1)
                _eta = np.asarray(forza_sync[:n]) * np.sin(np.angle(_Za) - np.angle(_za)) * _dts  # O(dt^1)
                _phs = np.exp(1j * _eta)
                a1 = a1 * _phs; b1 = b1 * _phs
            if KURAMOTO_SU2 and forza_sync is not None and wI_sync is not None:
                # KURAMOTO SU(2) NON-ABELIANO (§46): ruota lo SPINORE INTERO verso la media SU(2) dei vicini,
                # rotazione geodetica attorno all'asse VARIABILE nb x nb_bar (non commuta -> non-abeliano genuino).
                # psi_bar = media SU(2) dei vicini (snapshot t-1) rinormalizzata; nb_bar = suo Bloch (modulato dalla
                # coerenza di segno: se i segni disaccordano Sum w psi si cancella -> torque debole = accoppia segno/verso).
                # Il torque allinea il VERSO (nb->nb_bar); il SEGNO segue per OLONOMIA (fase geometrica, asse variabile).
                # O(dt^1). nb SI muove (gravita' fisica, voluto). forza/wI = Kuramoto-phi, zero param.
                _pb = wI_sync @ psi_sp_t                                    # somma pesata dei vicini (n,2), snapshot t-1
                _pb = _pb / np.maximum(np.linalg.norm(_pb, axis=1, keepdims=True), 1e-12)   # media SU(2) rinormalizzata
                _ab = _pb[:, 0]; _bbo = _pb[:, 1]
                _nb_bar = np.stack([2.0*np.real(np.conj(_ab)*_bbo), 2.0*np.imag(np.conj(_ab)*_bbo),
                                    np.abs(_ab)**2 - np.abs(_bbo)**2], axis=1)
                _crx = np.cross(nb[:n], _nb_bar)                            # nb x nb_bar (asse, snapshot t-1)
                _sink = np.linalg.norm(_crx, axis=1)
                _amp = np.arcsin(np.clip(_sink, 0.0, 1.0))                  # angolo geodetico verso nb_bar
                _Om = (np.asarray(forza_sync[:n]) * _amp)[:, None] * (_crx / np.maximum(_sink[:, None], 1e-12))
                _thk = np.linalg.norm(_Om, axis=1) * _dts                   # angolo di rotazione O(dt^1)
                _uk = _Om / np.maximum(np.linalg.norm(_Om, axis=1, keepdims=True), 1e-12)
                _ck = np.cos(_thk/2.0); _sk = np.sin(_thk/2.0)
                _kx, _ky, _kz = _uk[:, 0], _uk[:, 1], _uk[:, 2]
                _na1 = (_ck - 1j*_sk*_kz)*a1 + (-1j*_sk*(_kx - 1j*_ky))*b1
                _nb1 = (-1j*_sk*(_kx + 1j*_ky))*a1 + (_ck + 1j*_sk*_kz)*b1
                a1, b1 = _na1, _nb1
            nrm = np.maximum(np.sqrt(np.abs(a1) ** 2 + np.abs(b1) ** 2), 1e-12)  # |psi|=1 ATOMICO
            a1 = a1 / nrm; b1 = b1 / nrm
            psi_sp_new = np.stack([a1, b1], axis=1)
            # Bloch DERIVATO dal primario: nb = psi^dag sigma psi
            nb_new = np.stack([2.0 * np.real(np.conj(a1) * b1),
                               2.0 * np.imag(np.conj(a1) * b1),
                               np.abs(a1) ** 2 - np.abs(b1) ** 2], axis=1)
        else:
            omega_rot = omega_new if omega_sync is None else (omega_new + omega_sync)  # sync nella rotazione, non in memoria
            on = np.linalg.norm(omega_rot, axis=1, keepdims=True)
            ohat = omega_rot / np.maximum(on, 1e-9)
            ang = on * (dtn_c if not np.isscalar(dtn_c) else dtn_c)
            cA = np.cos(ang); sA = np.sin(ang)
            dot = np.sum(ohat * nb, axis=1, keepdims=True)
            nb_new = nb * cA + np.cross(ohat, nb) * sA + ohat * dot * (1 - cA)
        nb_new = nb_new / np.maximum(np.linalg.norm(nb_new, axis=1, keepdims=True), 1e-9)
        # --- COMMIT ATOMICO del settore spinoriale ---
        self.omega_s = omega_new.copy()
        self._nb = nb_new.copy()                          # Bloch (derivato dal primario se SPINORE_CORRETTO)
        self._nb_prec = nb_new.copy()                     # memorizzo per il ritardo causale
        if SPINORE_CORRETTO:
            self._psi_spinor = psi_sp_new                 # primario complesso: segno di doppia-copertura robusto
            self._spinor_lift = psi_sp_new.copy()         # il lift E' il primario (niente ri-derivazione da nb)
        else:
            self._aggiorna_lift_spinoriale()
        # rileggo phi_s (angolo polare) dal Bloch. phi (fase scalare U(1)) resta intatta.
        self.phi_s = np.arccos(np.clip(nb_new[:, 2], -1, 1))            # b = angolo polare [0,pi]

    # --- `spin_locale()` RIMOSSA il 2026-09-17 (correzione (5) della bonifica): CODICE MORTO. ---
    # NON era una legge esclusa, era una MISURA MAI CABLATA: nessun chiamante nel file vivo ne'
    # negli otto backup storici (GATE C, doc/REFERTO_gate_bonifica.md, commit 31922ff). Conteneva
    # un clamp `np.maximum(r, 0.01)` che il mandato della bonifica riteneva responsabile di
    # tagliare il tempo proprio: GATE C ha mostrato che la conseguenza temuta era FALSA, perche'
    # `dt_n` si costruisce in `step()` senza alcun clamp. Il tempo proprio non e' mai stato tagliato.
    # TERZO CASO DELLA STESSA FAMIGLIA: `_passo_spinoriale` con docstring "ORFANO" ma VIVO;
    # `VERSO_CHI` cablato ma MUTO; `spin_locale` definita e MAI CHIAMATA. Lo stato di vita del
    # codice non e' leggibile dal codice.
    # DOVE RECUPERARLA: blob `87450f7` (e ogni blob precedente), metodo `spin_locale`. La sua parte
    # di valore - la DOTTRINA sul perche' una frequenza DERIVATA si legge nel tempo proprio del
    # luogo e non nel tick globale, mentre la frequenza che DEFINISCE il ritmo deve usare `DT` - e'
    # trascritta in doc/COMPONENTI_PROMOSSE.md, sezione F. Cfr. CLAUDE.md par.9: il perche' non si
    # perde, ed e' quella la ragione della regola.
    # Sigillo: csv/_seal_fork/_sigillo_rimozione5.py  (byte-identita' ASSOLUTA, shape comprese)

    def _tempo_rampa(self):
        """[CURA 4] IL TEMPO DI ACCENSIONE di un nodo come sorgente di campo, PER NODO.

        A flag SPENTO e' `TAU_A`, cioe' esattamente il comportamento di prima.
        A flag ACCESO e' **`_tempo_luce_nodo`**, `tau = d_nodo/cs_nodo`: **la STESSA legge
        gia' cablata nello STRATO 1**, non una legge nuova, e **per NODO** -- la forma che
        `ramp` richiede *(shape misurata `= n`)*.

        MISURATO nella scena `(ii)` `(b)`: `p50 = 0.8978`, cioe' **`89.8` passi** contro i
        **`5000`** di `TAU_A`, con `p05 86.6` / `p95 92.2` -- **stretto a +-3 %**, quindi
        **non introduce una dispersione nuova**.

        ⚠ **NON E' MONOTONO, E VA DETTO:** `_tempo_luce_nodo` dipende da `d` e da `cs`, quindi
        **cambia a ogni passo**. Se gli archi di un nodo si allungano, il suo tempo di rampa
        cresce e `ramp` **puo' SCENDERE**. **E' voluto**: e' una legge locale che segue lo stato
        locale, come `_ttw = 2pi/|dw|`.
        **L'ALTERNATIVA -- congelare il tempo-luce alla nascita -- RICHIEDEREBBE UN ARRAY DI
        STATO NUOVO PER NODO**, con la sua estensione alla mitosi, allo Schwinger e allo
        snapshot: **esattamente la famiglia di difetti `_cs_nodo_prev` (71.88 %) e
        `_psi_spin_prec` (95.33 %)**. **Non si fa**, e la non-monotonia si MISURA invece di
        essere nascosta (contatore qui sotto).

        A8: il ramo senza archi e' DICHIARATO e CONTATO. Senza archi `_tempo_luce_nodo` non ha
        da cosa costruire `d_nodo`, e si cade su `TAU_A`: non e' un errore, e' il primo istante.
        """
        if not SEMINA_MATURA:
            return TAU_A
        self._g_rampa_tot = getattr(self, "_g_rampa_tot", 0) + 1
        if not len(self.i):
            self._g_rampa_senza_archi = getattr(self, "_g_rampa_senza_archi", 0) + 1
            self._g_rampa_quando = self._g_rampa_tot
            return TAU_A
        tl = np.asarray(self._tempo_luce_nodo(self.i, self.j), float)
        if tl.size != self.n:
            # A8/A9: la forma non combacia -> si dichiara, si conta, e si cade su `TAU_A`.
            self._g_rampa_forma = getattr(self, "_g_rampa_forma", 0) + 1
            self._g_rampa_shape = (int(tl.size), int(self.n))
            self._g_rampa_quando = self._g_rampa_tot
            return TAU_A
        return tl

    def _pesi(self):
        # [CURA 4] il DENOMINATORE della rampa: `TAU_A` a flag spento, il tempo-luce a flag
        # acceso. La riga sotto e' IDENTICA a prima quando `_tempo_rampa()` restituisce `TAU_A`.
        _tr = self._tempo_rampa()
        ramp = np.minimum(1.0, self.eta / _tr)
        if SEMINA_MATURA:
            # A8: la NON-MONOTONIA dichiarata sopra si MISURA.
            # ❌ `_g_rampa_sotto1` NON MISURA CIO' CHE SERVE, e Luca l'ha rilevato: conta quanti
            #   nodi hanno `ramp < 1`, **che include un nodo GIOVANE non ancora arrivato a 1**.
            #   **Un CALO e' un'altra cosa**, e va misurato come tale: quante volte `ramp` di un
            #   nodo DIMINUISCE, e DI QUANTO.
            #   `_g_rampa_sotto1` resta, perche' e' comunque il denominatore utile.
            self._g_rampa_sotto1 = getattr(self, "_g_rampa_sotto1", 0) + int(np.sum(ramp < 1.0))
            self._g_rampa_nodi = getattr(self, "_g_rampa_nodi", 0) + int(ramp.size)
            # `_g_rampa_prec` e' un array DIAGNOSTICO, e lo dichiaro come tale: il suo
            #   disallineamento SI CONTA e si riparte, invece di essere esteso a mano a ogni sito
            #   di nascita. **NON e' la famiglia di `_cs_nodo_prev`**, che stava su un percorso
            #   FISICO: qui se il confronto salta si perde una MISURA, non una legge.
            _prec = getattr(self, "_g_rampa_prec", None)
            if _prec is not None and len(_prec) == len(ramp):
                _cal = ramp < _prec
                _nc = int(_cal.sum())
                if _nc:
                    _dd = _prec[_cal] - ramp[_cal]
                    self._g_rampa_cali = getattr(self, "_g_rampa_cali", 0) + _nc
                    self._g_rampa_calo_somma = (getattr(self, "_g_rampa_calo_somma", 0.0)
                                                + float(_dd.sum()))
                    self._g_rampa_calo_max = max(getattr(self, "_g_rampa_calo_max", 0.0),
                                                 float(_dd.max()))
                    self._g_rampa_calo_quando = self._g_rampa_tot
            elif _prec is not None:
                self._g_rampa_prec_disallineata = (
                    getattr(self, "_g_rampa_prec_disallineata", 0) + 1)
                self._g_rampa_prec_shape = (len(_prec), len(ramp))
            self._g_rampa_prec = np.array(ramp, dtype=float, copy=True)
        base = np.exp(-self.d / self._lam_archi()) * ramp[self.i] * ramp[self.j]
        # [A8, 2026-09-20] CONTABILITA' DELLA GUARDIA -- byte-inerte: si CONTA, non si cambia.
        # Un ramo che salta in silenzio e' un comportamento SCONOSCIUTO (A8), e questa forma ha
        # gia' prodotto due volte mesi di dati sbagliati: `_cs_nodo_prev` (71.88 %) e
        # `_psi_spin_prec` (95.33 %). Si registrano QUATTRO cose, non una: le invocazioni, i
        # salti, LA FORMA al fallimento (le due lunghezze) e QUANDO -- l'indice dell'ultima
        # invocazione saltata. Il conteggio da solo non distingue un TRANSITORIO delle prime
        # chiamate da un comportamento PRINCIPALE sparso su tutto il run: danno lo stesso numero.
        # NB: il salto si registra SOLO col flag ACCESO. A flag spento la legge NON DEVE girare,
        # e contarlo come fallimento sarebbe un falso positivo -- la classe di `N3b` (par.9).
        self._g_kernel_alpha_tot = getattr(self, "_g_kernel_alpha_tot", 0) + 1
        # [A8/A9, 2026-09-20] IL RAMO ALTERNATIVO, DICHIARATO. Se le lunghezze non combaciano il
        # kernel NON viene rinforzato dal tempo proprio: `base` resta quello esponenziale puro,
        # che e' la forma da cui il rinforzo parte. NON e' un errore, ed e' il comportamento
        # giusto -- ma finora era SILENZIOSO, e un ramo silenzioso non e' un ramo (A8).
        # MISURATO: 0 salti su 145 invocazioni (sigillo 3/3, 4edfab2). Si dichiara lo stesso:
        # e' un difetto di FORMA, non di frequenza -- precedente Z25, tenuto benche' l'A/B non
        # mostrasse alcun effetto.
        # ⚠ PERCHE' UN `if` NEGATO E NON UN `else`: il corpo del ramo buono e' lungo ~40 righe,
        # e un `else` finirebbe lontanissimo dalla condizione. Qui il ramo alternativo sta
        # ACCANTO alla guardia, dove si legge. E' la stessa cosa, scritta dove si vede.
        if KERNEL_ALPHA != 0.0 and len(self.tw) != len(self.d):
            self._g_kernel_alpha_salti = getattr(self, "_g_kernel_alpha_salti", 0) + 1
            self._g_kernel_alpha_shape = (len(self.tw), len(self.d))
            self._g_kernel_alpha_quando = self._g_kernel_alpha_tot
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

    def _mat2(self, val_dir, val_rev):
        """Come `_mat`, ma con valori DIVERSI nelle due direzioni dell'arco.

        `_mat` mette lo stesso `val` sia in M[i,j] sia in M[j,i]: corretto per una quantita'
        simmetrica (lo scalare A_ij). NON basta per il trasporto di gauge, dove l'orientamento
        conta: M[i,j] porta una componente di N_ij, M[j,i] la corrispondente di N_ji = N_ij^dag.
        Passare `val` due volte darebbe una matrice NON hermitiana e romperebbe l'azione-reazione.

        ATTENZIONE: `self._S` e' UNA struttura in cache riusata a ogni chiamata. Il risultato va
        CONSUMATO (matvec) prima della chiamata successiva, altrimenti i dati vengono sovrascritti.
        """
        if self._S is None: self._costruisci_struttura()
        self._S.data = np.concatenate([val_dir, val_rev])[self._perm]
        return self._S

    def calcola_psi(self, w=None):
        # [A8 - TEMPO 1, 2026-09-17] SOLO STRUMENTAZIONE, nessuna legge toccata.
        # Il ramo `w is None` RICALCOLA i pesi. Ma `step()` li calcola GIA' una volta sola
        # (riga ~2958), e il commento DUE RIGHE SOTTO prescrive l'opposto di cio' che accade:
        #   "Non ricalcolare psi in punti diversi del passo: quello introdurrebbe letture miste
        #    t/t+1."
        # L'architettura giusta c'e' gia' (il parametro `w` esiste), ma ~19 chiamanti non lo
        # passano. Un intento SCRITTO e non fatto rispettare dal codice e' esattamente cio' che
        # A8 esiste per intercettare: prima di correggere, SI CONTA - e si conta CHI.
        self._calcpsi_chiamate = getattr(self, "_calcpsi_chiamate", 0) + 1
        if w is None:
            self._calcpsi_w_none = getattr(self, "_calcpsi_w_none", 0) + 1
            try:
                _chi = _sys._getframe(1).f_code.co_name
                _rig = _sys._getframe(1).f_lineno
            except Exception:
                _chi, _rig = "?", -1
            _d = getattr(self, "_calcpsi_origini", None)
            if _d is None:
                _d = {}; self._calcpsi_origini = _d
            _k = "%s:%d" % (_chi, _rig)
            _d[_k] = _d.get(_k, 0) + 1
        if self.n == 0 or not len(self.i):
            self.psi = np.zeros(self.n, complex); return self.psi
        if w is None: w = self._pesi()
        # COARSE-GRAINING: ogni solitone-blocco porta la massa di SCALA_B fini. L'ampiezza
        # scala come sqrt(SCALA_B) cosi' che l'intensita' |Psi|^2 (la massa) scali con
        # SCALA_B, come richiesto per preservare Poisson (la sorgente e' rho=|Psi|^2).
        amp = SCALA_AMP
        F = self._mat(w) @ (amp * np.exp(1j * self.phi))
        self.psi = self.satura(F)                          # saturazione regolarizzata (Leggi XV/XVIII)
        if CAMPO_SPINORIALE:
            # [FASE 1] CAMPO EMESSO DALLO SPINORE (Legge I), calcolato IN PARALLELO: non ancora agganciato a
            # gravita'/forze/mitosi (self.psi scalare resta la sorgente in Fase 1). CAUSALITA' S1 (Jacobi):
            # legge lo SNAPSHOT _psi_spinor (stato committato), tutti i nodi simultanei (sparse @ dense),
            # nessuna dipendenza dall'ordine. Riduzione-al-limite S3: con _psi_spinor=(e^{i phi},0) -> comp 0 == self.psi.
            _n = self.n
            _psp = getattr(self, "_psi_spinor", None)
            if _psp is None or len(_psp) < _n:
                _psp = np.zeros((_n, 2), complex); _psp[:, 0] = np.exp(1j * self.phi[:_n])  # fallback: fase pura asse 0
            else:
                _psp = np.asarray(_psp)[:_n]
            _Fs = self._mat(w) @ (amp * _psp)                                  # (n,2): STESSO kernel del grafo
            _norm = np.sqrt(np.sum(np.abs(_Fs) ** 2, axis=1) + 1e-9)           # norma dello spinore-campo
            self.psi_spin = _Fs / (1.0 + GAMMA * _norm)[:, None]               # saturazione sulla NORMA (non ruota lo spinore)
            self.rho_spin = np.real(np.sum(np.conj(self.psi_spin) * self.psi_spin, axis=1))  # rho = psi^dag psi
        return self.psi

    def intensita(self): return np.abs(self.psi) ** 2

    def _rho_sorgente(self):
        """[FASE 2 dev-spinoriale] densita' SORGENTE della fisica: |psi|^2 scalare (CAMPO_SPINORIALE off)
        oppure rho_spin = psi_spin^dag psi_spin (ON), la norma del campo EMESSO dallo spinore. Nel limite
        (spinori in fase) rho_spin == |psi|^2 (riduzione esatta)."""
        n = self.n
        if CAMPO_SPINORIALE:
            _rs = getattr(self, "rho_spin", None)
            # [PSI-FLASH, 2026-09-28] IL RIPIEGO ERA SILENZIOSO. Era:
            #     if _rs is not None and len(_rs) >= n: return ...[:n]
            #     return np.abs(self.psi[:n]) ** 2          <- per TUTTA la rete
            #   Con `CAMPO_SPINORIALE` ACCESO la densita' sorgente E' `rho_spin`: cadere su
            #   `|psi|^2` non e' un ripiego, e' UN'ALTRA GRANDEZZA. MISURATO: scattava 2
            #   volte su 15 al passo DOPO la nascita (len 12802, n 12803), e quello era il
            #   GRADINO del +11 % sul pozzo.
            #   ⚠ `_rs is None` RESTA legittimo: il campo non e' ancora stato calcolato.
            if _rs is not None:
                _ferma_se_cache_corta("rho_spin", len(_rs), n, "_rho_sorgente",
                                      "abs(psi)**2, cioe' UN'ALTRA DENSITA'")
                return np.asarray(_rs)[:n]
        return np.abs(self.psi[:n]) ** 2

    def _nb_grav(self):
        """[FASE 2 dev-spinoriale] direzione di Bloch per la GRAVITA': self._nb (off) oppure NATIVA dal campo
        EMESSO psi_spin (ON): nb = psi_spin^dag sigma psi_spin / (psi_spin^dag psi_spin). Il campo emesso porta
        la direzione. Nel limite (spinori in fase asse 0) nb -> [0,0,1] == Bloch del vecchio (riduzione esatta)."""
        n = self.n
        if CAMPO_SPINORIALE:
            _ps = getattr(self, "psi_spin", None)
            # [PSI-FLASH, 2026-09-28] LO STESSO SCHEMA, LO STESSO TRATTAMENTO (decisione di
            #   Luca): il ramo di scorta dava `self._nb` invece del Bloch NATIVO del campo
            #   emesso -- UN'ALTRA DIREZIONE, e la direzione entra nella GRAVITA'.
            #   ⚠ MISURATO: su questa scena NON SCATTA MAI nella finestra della nascita,
            #   quindi questa riga e' BYTE-INERTE qui. **Lo dico prima di misurarlo**: il
            #   sigillo non puo' dimostrare che serve, solo che non rompe.
            if _ps is not None:
                _ferma_se_cache_corta("psi_spin", len(_ps), n, "_nb_grav",
                                      "self._nb, cioe' UN'ALTRA DIREZIONE di Bloch")
            if _ps is not None and len(_ps) >= n:
                _ps = np.asarray(_ps)[:n]
                _a = _ps[:, 0]; _b = _ps[:, 1]
                _nbn = np.stack([2.0 * np.real(np.conj(_a) * _b), 2.0 * np.imag(np.conj(_a) * _b),
                                 np.abs(_a) ** 2 - np.abs(_b) ** 2], axis=1)
                # norma di Bloch |psi^dag sigma psi| = psi^dag psi = rho_spin (identita'). Normalizzo per rho_spin
                # con floor MINUSCOLO (solo anti 0/0): dove il campo e' ~0 (vuoto) la direzione e' indefinita -> [0,0,1].
                _rs = np.abs(_a) ** 2 + np.abs(_b) ** 2
                _nbn = _nbn / np.maximum(_rs, 1e-30)[:, None]
                _def = _rs <= 1e-20
                if _def.any():
                    _nbn[_def] = np.array([0.0, 0.0, 1.0])
                return _nbn
        return self._nb

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
    def _dphi():
        """[FASE_2PI] IL DOMINIO DI `phi`: `2pi` con la cura, `4pi` senza.

        Un solo posto da cui tutti i `% (...)` su `phi` prendono il periodo, cosi' non si
        possono sfasare fra loro -- il difetto che `D34` ha mostrato costare caro.
        """
        return (2.0 * np.pi) if FASE_2PI else (4.0 * np.pi)

    @staticmethod
    def _wphi(a):
        """[FASE_2PI] L'avvolgimento di una DIFFERENZA DI FASE, sul periodo di `phi`.

        ⚠ NON si usa per la TORSIONE: `tw` e' un ACCUMULO e non ha periodo (vedi `_w8`).
        """
        if FASE_2PI:
            return (a + np.pi) % (2 * np.pi) - np.pi
        return (a + 2 * np.pi) % (4 * np.pi) - 2 * np.pi

    @staticmethod
    def _w4(a): return (a + 2 * np.pi) % (4 * np.pi) - 2 * np.pi

    @staticmethod
    def _w8(a): return (a + 4 * np.pi) % (8 * np.pi) - 4 * np.pi
    # avvolgimento su ±4pi: permette alla torsione di vivere sul dominio DOPPIO (4pi)
    # invece che su 2pi. Usato dalla torsione a doppia copertura (flag TORS_4PI),
    # motivato dai legami dipolari che uniscono due antichirali (due mezzi-twist).

    def _traccia_d0(self, sito, prima, pavimento=None):
        """Registra il contributo di UN sito a `d0`. PURE-READ sulla fisica: scrive solo la traccia.

        ⚠ TRE LIVELLI, dichiarati: (a) DETTAGLIO PIENO sulle coppie di `TRACCIA_D0_COPPIE`, con il
        valore PRIMA e DOPO -- la coppia, non il delta, cosi' un `max()` si distingue da una somma;
        (b) RIASSUNTO sugli archi dei nodi di `TRACCIA_D0_NODI`: quanti toccati, SOMMA ALGEBRICA
        del delta, max |delta|; (c) GLOBALE: quante volte il sito e' girato.
        ⚠ I siti che CONCATENANO (`:2083`, mitosi, Schwinger) cambiano la LUNGHEZZA di `d0`: li'
        il delta elemento-per-elemento non esiste e si registra il cambio di lunghezza, dichiarato.
        """
        import numpy as _np
        reg = getattr(self, "_traccia_d0_log", None)
        if reg is None:
            reg = self._traccia_d0_log = []
        dopo = self.d0
        passo = int(getattr(self, "_passo_corrente", -1))
        voce = {"passo": passo, "sito": sito, "n": self.n, "archi": len(dopo),
                "len_prima": len(prima), "pavimento": (float(pavimento)
                                                       if pavimento is not None else None)}
        ii, jj = self.i, self.j
        # (a) DETTAGLIO PIENO -- l'arco si cerca per COPPIA DI NODI, mai per indice (gli archi si
        #     aggiungono, la posizione non e' stabile)
        for (a, b) in TRACCIA_D0_COPPIE:
            k = _np.flatnonzero(((ii == a) & (jj == b)) | ((ii == b) & (jj == a)))
            if not len(k):
                voce["%d-%d" % (a, b)] = None
                continue
            k = int(k[0])
            pr = float(prima[k]) if k < len(prima) and len(prima) == len(dopo) else float("nan")
            voce["%d-%d" % (a, b)] = (pr, float(dopo[k]), float(self.d[k]))
        # (b)+(c) RIASSUNTO e GLOBALE
        if len(prima) == len(dopo):
            sel = _np.isin(ii, TRACCIA_D0_NODI) | _np.isin(jj, TRACCIA_D0_NODI)
            dl = dopo[sel] - prima[sel]
            nz = dl != 0.0
            voce["tocc"] = int(nz.sum()); voce["somma"] = float(dl.sum())
            voce["maxass"] = float(_np.abs(dl).max()) if len(dl) else 0.0
            if pavimento is not None:
                voce["tagliati_glob"] = int((prima < pavimento).sum())
                voce["tagliati_tracc"] = int((prima[sel] < pavimento).sum())
        else:
            voce["tocc"] = -1; voce["somma"] = float("nan"); voce["maxass"] = float("nan")
            voce["nota"] = "lunghezza cambiata: %d -> %d" % (len(prima), len(dopo))
        reg.append(voce)
        self._g_traccia_d0 = getattr(self, "_g_traccia_d0", {})
        self._g_traccia_d0[sito] = self._g_traccia_d0.get(sito, 0) + 1

    def _traccia_vd(self, t_lap, t_src, t_beta, beta, cs_arco):
        """I TRE termini di `acc` SEPARATI, col SEGNO. PURE-READ: scrive solo la traccia.

        `acc = cs_arco^2*lap + src - beta*vd`, e qui arrivano i tre gia' calcolati: NON si
        ricalcola niente, si LEGGE. Byte-inerte (gira sotto `TRACCIA_VD`).
        ⚠ Si registrano i tre SEPARATI e non la somma: la somma e' `acc`, che si vedrebbe gia'
        da `vd`. La domanda e' la RIPARTIZIONE.
        """
        import numpy as _np
        reg = getattr(self, "_traccia_vd_log", None)
        if reg is None:
            reg = self._traccia_vd_log = []
        ii, jj = self.i, self.j
        d, d0, vd = self.d, self.d0, self.vd
        m = min(len(ii), len(jj), len(d), len(d0), len(vd), len(_np.atleast_1d(t_lap)))
        sel = _np.isin(ii[:m], TRACCIA_D0_NODI) | _np.isin(jj[:m], TRACCIA_D0_NODI)
        def _a(x):
            x = _np.atleast_1d(_np.asarray(x, float))
            return x[:m] if x.size >= m else _np.full(m, float(x.ravel()[0]))
        L, S, B = _a(t_lap), _a(t_src), _a(t_beta)
        voce = {"passo": int(getattr(self, "_passo_corrente", -1)), "archi": m,
                "lap_p50": float(_np.median(L[sel])) if sel.any() else float("nan"),
                "src_p50": float(_np.median(S[sel])) if sel.any() else float("nan"),
                "bet_p50": float(_np.median(B[sel])) if sel.any() else float("nan"),
                "lap_max": float(_np.abs(L[sel]).max()) if sel.any() else float("nan"),
                "src_max": float(_np.abs(S[sel]).max()) if sel.any() else float("nan"),
                "bet_max": float(_np.abs(B[sel]).max()) if sel.any() else float("nan")}
        # DETTAGLIO: l'arco cercato per COPPIA DI NODI, mai per indice
        for (a, b) in TRACCIA_D0_COPPIE:
            k = _np.flatnonzero(((ii[:m] == a) & (jj[:m] == b)) | ((ii[:m] == b) & (jj[:m] == a)))
            if not len(k):
                voce["%d-%d" % (a, b)] = None
                continue
            k = int(k[0])
            voce["%d-%d" % (a, b)] = (float(L[k]), float(S[k]), float(B[k]),
                                      float(d[k]), float(d0[k]), float(vd[k]),
                                      float(_a(beta)[k]), float(_a(cs_arco)[k]))
        reg.append(voce)
        self._g_traccia_vd = getattr(self, "_g_traccia_vd", 0) + 1

    def _traccia_coesione(self, coes, tetto, mask):
        """Il valore di `coesione_relazionale` PRIMA del clip, e il tetto che lo taglia.

        ⚠ LA DOMANDA A CUI RISPONDE: il clip PROTEGGE o PRODUCE?
          `|coes| >> tetto`  -> il termine e' enorme e il clip lo sta contenendo: stringere il
                                tetto NON basta, il difetto e' nel termine;
          `|coes| ~ tetto`   -> e' il clip a produrre il movimento, e il tetto e' la cura giusta.
        PURE-READ sulla fisica: scrive solo la traccia. Byte-inerte (gira sotto `TRACCIA_D0`).
        """
        import numpy as _np
        reg = getattr(self, "_traccia_coes_log", None)
        if reg is None:
            reg = self._traccia_coes_log = []
        ii, jj = self.i[mask], self.j[mask]
        ac = _np.abs(_np.asarray(coes, float))
        at = _np.abs(_np.asarray(tetto, float))
        rap = ac / _np.maximum(at, 1e-300)
        voce = {"passo": int(getattr(self, "_passo_corrente", -1)),
                "n_archi": int(ac.size),
                "sat": int((ac >= at).sum()),          # quanti SATURANO il clip
                "rap_p50": float(_np.median(rap)) if ac.size else float("nan"),
                "rap_p99": float(_np.percentile(rap, 99)) if ac.size else float("nan"),
                "rap_max": float(rap.max()) if ac.size else float("nan")}
        # e l'arco seguito, per COPPIA DI NODI (mai per indice: gli archi si aggiungono)
        for (a, b) in TRACCIA_D0_COPPIE:
            k = _np.flatnonzero(((ii == a) & (jj == b)) | ((ii == b) & (jj == a)))
            voce["%d-%d" % (a, b)] = (None if not len(k)
                                      else (float(_np.asarray(coes, float)[k[0]]),
                                            float(_np.asarray(tetto, float)[k[0]])))
        reg.append(voce)

    def _smorza(self, prima, dx, quale):
        """SCALA MINIMA: ritorna l'incremento EFFETTIVO, smorzando solo la DISCESA.

        `dx >= 0` -> INTATTO (identita' esatta). `dx < 0` -> `dx * max(0, 1 - LAM/prima)`.
        Invariante: `nuovo - LAM = (prima - LAM) * (1 + dx/prima)`."""
        prima = np.asarray(prima, dtype=float)
        dx = np.asarray(dx, dtype=float)
        scende = dx < 0.0
        pos = prima > 0.0
        base = np.where(pos, prima, 1.0)          # il fittizio NON entra nel risultato
        fatt = np.where(pos, np.maximum(0.0, 1.0 - LAM / base), 0.0)
        self._g_sm_tot = getattr(self, '_g_sm_tot', 0) + 1
        setattr(self, '_g_sm_' + quale, getattr(self, '_g_sm_' + quale, 0) + 1)
        self._g_sm_discese = getattr(self, '_g_sm_discese', 0) + int(np.sum(scende))
        # il patologico: la scrittura GREZZA avrebbe portato la lunghezza a <= 0
        self._g_sm_patol = (getattr(self, '_g_sm_patol', 0)
                            + int(np.sum(scende & ((prima + dx) <= 0.0))))
        eff = np.where(scende, dx * fatt, dx)
        # ⚠ I NUMERI CHE DIMOSTRANO CHE IL VINCOLO NON CREA MOVIMENTO, misurati a OGNI scrittura
        # di TUTTO il run e non al solo primo passo. Byte-inerti: solo contatori.
        #
        # ⚠ IL CRITERIO E' STATO CORRETTO IL 2026-09-21, ED ERA MIO L'ERRORE (`Z86`). La prima
        #   versione chiedeva `max(eff - dx) <= 0`, che e' FALSO PER COSTRUZIONE: per `dx < 0`
        #   si ha `eff = dx*f` con `f in [0,1]`, quindi `eff >= dx` e la differenza arriva fino
        #   a `|dx|`. ATTENUARE UNA DISCESA RENDE L'INCREMENTO MENO NEGATIVO: quel numero non
        #   poteva essere <= 0, e il sigillo era matematicamente impossibile da passare.
        #
        # LA PROPRIETA' VERA e' che il nuovo valore stia SEMPRE in `[x + dx, x]`:
        #   `_g_sm_viol_id`  quante volte un incremento >= 0 e' stato toccato -> DEVE essere 0
        #                    (una lunghezza che non scende non cambia DI UN BIT);
        #   `_g_sm_max_giu`  il massimo di `eff` sulle sole DISCESE -> DEVE restare <= 0
        #                    (il vincolo non spinge mai verso l'ALTO: niente inflazione);
        #   `_g_sm_viol_giu` quante volte `eff < dx` -> DEVE essere 0 (il vincolo non puo'
        #                    APPROFONDIRE una discesa).
        # ⚠ NON E' UN ALLARGAMENTO: il vecchio guardava la DIFFERENZA `eff - dx`, il nuovo
        #   guarda il SEGNO di `eff` -- un punto che il vecchio non guardava affatto.
        _e = np.atleast_1d(eff); _d = np.atleast_1d(dx); _s = np.atleast_1d(scende)
        if len(_d) or len(_e):
            self._g_sm_viol_id = (getattr(self, '_g_sm_viol_id', 0)
                                  + int(np.sum((~_s) & (_e != _d))))
            if np.any(_s):
                self._g_sm_max_giu = max(getattr(self, '_g_sm_max_giu', -np.inf),
                                         float(np.max(_e[np.broadcast_to(_s, _e.shape)])))
            self._g_sm_viol_giu = (getattr(self, '_g_sm_viol_giu', 0)
                                   + int(np.sum(_s & (_e < _d))))
        return eff

    def verifica_invarianti(self, dove='fine passo', passo=None):
        """[C5] Ogni grandezza di stato dentro il suo DOMINIO. Alza `DominioViolato`.

        **Legge soltanto.** Operazioni vettoriali su tutto lo stato: il costo e' piccolo e va
        MISURATO, non stimato -- il sigillo `I1` lo fa.

        ⚠ SI FERMA AL PRIMO DOMINIO VIOLATO, e riporta **gli indici**: senza quelli si saprebbe
          *che* e' successo ma non *dove*, e la rigiocata non avrebbe un bersaglio.
        """
        if not INVARIANTI:
            return 0
        self._g_inv_giri = getattr(self, '_g_inv_giri', 0) + 1
        passo = self._g_inv_giri if passo is None else passo
        n = self.n
        # [E4-LAM] `_lam_attivo` E' STATO TOLTO: era l'unico uso, e serviva a CONDIZIONARE
        # la legge `d >= LAM`. Lasciarlo qui inutilizzato sarebbe codice morto.
        controllate = 0
        for quale, (forma, _perche) in DOMINI.items():
            v = getattr(self, quale, None)
            if v is None:
                continue
            v = np.asarray(v)
            if v.size == 0:
                continue
            controllate += 1
            # --- il livello FISICO
            if forma == 'peq':
                vf = v.astype(float, copy=False)
                _nan = ~np.isfinite(vf)
                _amm = np.zeros(len(vf), dtype=bool)
                _marca = getattr(self, '_peqn_idx', None)
                if PEQ_NASCITA_LOCALE and _marca is not None and len(_marca):
                    _m = np.asarray(_marca)
                    _amm[_m[_m < len(vf)]] = True
                self._g_inv_peq_nan_ok = (getattr(self, '_g_inv_peq_nan_ok', 0)
                                          + int(np.sum(_nan & _amm)))
                cattivo = (_nan & ~_amm) | (np.isfinite(vf) & (vf < 0.0))
                regola = ('>= 0, e `nan` SOLO sugli archi marcati da PEQ_NASCITA_LOCALE '
                          '(ammessi ora: %d)' % int(np.sum(_amm)))
            elif forma == 'indice':
                cattivo = (v < 0) | (v >= n)
                regola = '0 <= x < n (n = %d)' % n
            elif np.iscomplexobj(v):
                cattivo = ~np.isfinite(v.real) | ~np.isfinite(v.imag)
                regola = 'finito (complesso)'
            else:
                vf = v.astype(float, copy=False)
                fin = np.isfinite(vf)
                if forma == 'finito':
                    cattivo = ~fin; regola = 'finito'
                elif forma == 'pos':
                    cattivo = ~fin | (vf <= 0.0); regola = '> 0'
                elif forma == 'nonneg':
                    cattivo = ~fin | (vf < 0.0); regola = '>= 0'
                elif forma == 'nonneg_inf':
                    # [`RAMPA-1`, 2026-09-25] **`+inf` E' NEL DOMINIO, `nan` E `-inf` NO.**
                    #   Serve a `eta`: il vuoto DATO ha `eta = +inf` perche' **non ha un tempo
                    #   di accensione** -- non e' un numero grande, e' l'assenza di una scala.
                    #   ⚠ **NON si allarga `nonneg`**, che copre `rho_spin`, `_deg`, il raggio
                    #   del core e altre otto grandezze: per loro un `inf` **resta un difetto**.
                    #   Una forma nuova per UNA grandezza costa meno di un controllo indebolito
                    #   per dodici (`A9`: un presidio che ammette tutto non impedisce niente).
                    #   ❌ **E QUESTO INVARIANTE HA FERMATO LA CURA AL PRIMO GIRO**, con
                    #   `eta VIOLA >= 0 ... valori inf, quanti 4252 su 4252`: **ha funzionato.**
                    #   L'audit per AST (`csv/_letture_eta.py`) **non poteva vederlo**, perche'
                    #   qui `eta` e' una **CHIAVE DI TABELLA**, cioe' una STRINGA, non un
                    #   attributo: **un audit su chi LEGGE una grandezza deve cercare anche le
                    #   stringhe, in un codice guidato da tabelle.**
                    cattivo = np.isnan(vf) | (vf < 0.0)
                    regola = '>= 0, con +inf AMMESSO (vuoto dato: nessun tempo di accensione)'
                elif forma == 'segno':
                    cattivo = ~np.isin(v, (-1, 1)); regola = 'in {-1, +1}'
                elif forma == 'fase':
                    cattivo = ~fin | (vf < 0.0) | (vf >= 4.0 * np.pi)
                    regola = 'in [0, 4*pi)'
                elif forma == 'lam':
                    # [E4-LAM, decisione di Luca 2026-09-24] SI VERIFICA SEMPRE, NON PIU'
                    # SOTTO FLAG. *** «La lunghezza degli archi non puo' scendere sotto la
                    # lunghezza tipica del sistema» E' UNA LEGGE, non una garanzia che
                    # dipende da un flag. *** Prima il controllo era `if _lam_attivo`, cioe'
                    # `SCALA_MIN or SCALA_MIN_PASSO`, e a flag spenti DEGRADAVA a `> 0`:
                    # una legge verificata solo quando un flag e' acceso non e' una legge,
                    # e' un'opzione (A9: un presidio che non impedisce non e' un presidio).
                    # ⚠ la tolleranza e' l'ARROTONDAMENTO di `LAM`, non un numero scelto
                    cattivo = ~fin | (vf < LAM * (1.0 - 1e-12))
                    regola = '>= LAM (= %.6f) -- LEGGE, non opzione' % LAM
                elif forma == 'unita':
                    nrm = np.sqrt(np.sum(np.abs(v) ** 2, axis=-1)) if v.ndim > 1 \
                        else np.abs(v)
                    cattivo = ~np.isfinite(nrm) | (np.abs(nrm - 1.0) > 1e-6)
                    regola = '|x| = 1 (tolleranza 1e-6)'
                else:
                    cattivo = ~fin; regola = 'finito'
            cattivo = np.asarray(cattivo)
            # ### IL VELENO: ESENZIONE PER CELLA, ANCORATA AL REGISTRO DEL VELENO.
            #   (`COMMIT 4`, via (a), decisione di Luca del 2026-10-03.)
            #
            #   ### E' IL TERZO CASO DELLA STESSA ESENZIONE, e i primi due stanno qui
            #   sopra -- per questo NON e' una legge in piu' (`9-ter`):
            #     `eta` -> `nonneg_inf`: esenzione sull'INTERO DOMINIO (`+inf` legittimo)
            #     `peq` -> `_peqn_idx`:  esenzione ### PER CELLA, ancorata a una MARCA
            #     ### le derivate AVVELENATE -> `_veleno_registro`: esenzione PER CELLA,
            #       ancorata al VELENO. ### La terza volta che si usa la stessa forma.
            #
            #   ### E NESSUN ELENCO A MANO: il registro del veleno lo scrive
            #   `_avvelena_derivate` leggendo la CLASSE DI NASCITA da `REGISTRO_DERIVATE`.
            #
            #   ### E LA CADUTA CHE L'HA RICHIESTA DICE UNA COSA IN PIU', da non perdere:
            #   PRIMA del veleno, dopo ogni nascita, questo stesso controllo verificava il
            #   dominio di derivate che portavano ### VALORI VECCHI (copiati o lasciati), e
            #   che passavano ### PERCHE' ERANO POSITIVI PER CASO. ### Il controllo sulle
            #   derivate dopo una nascita verificava valori NON VALIDI -- e nessuno lo
            #   sapeva finche' il veleno non ha messo `nan` dove c'era un numero vecchio.
            _vel = (getattr(self, '_veleno_registro', None) or {}).get(quale)
            if _vel is not None:
                if _vel['arr'] is not getattr(self, quale, None):
                    # ### SCADUTO: la legge ha RISCRITTO la derivata, quindi il veleno
                    #   non c'e' piu' e il dominio si applica PIENO, come prima.
                    #   ⚠ IL LIMITE, DICHIARATO: una modifica ### IN POSTO conserverebbe
                    #     l'identita' dell'oggetto, quindi il registro sembrerebbe VIVO
                    #     mentre la derivata e' stata ricalcolata -- e le celle
                    #     avvelenate, ora riempite di numeri veri, verrebbero NOMINATE
                    #     come difetto. ### MISURATO: ZERO modifiche in posto sulle dieci
                    #     derivate, e il rilevatore ha il suo CONTROLLO POSITIVO cablato
                    #     (`csv/_test_fork/_copertura_derivate/`; il blob del referto e'
                    #     citato dal braccio `D` del sigillo del veleno).
                    del self._veleno_registro[quale]
                    self._g_inv_veleno_scaduti = (getattr(self, '_g_inv_veleno_scaduti', 0)
                                                  + 1)
                elif cattivo.ndim == 1 and v.dtype.kind == 'f':
                    _i0 = int(_vel['inizio'])
                    _i1 = min(int(_vel['fine']), len(cattivo))
                    _mv = np.zeros(len(cattivo), dtype=bool)
                    if _i1 > _i0:
                        _mv[_i0:_i1] = True
                    _nanv = ~np.isfinite(np.asarray(v, dtype=float))
                    # ### STRETTO NEI DUE VERSI, e il secondo verso e' il punto: nelle
                    #   celle avvelenate il valore ### DEVE essere `nan`. Un NUMERO li'
                    #   vuol dire che qualcuno ha scritto ### UNA CELLA senza riscrivere
                    #   la derivata, e quello e' un ### DIFETTO DA NOMINARE -- non
                    #   un'esenzione. Un'esenzione che ammettesse anche i numeri sarebbe
                    #   `A9`: un presidio che ammette tutto non impedisce niente.
                    cattivo = np.where(_mv, ~_nanv, cattivo)
                    self._g_inv_veleno_ok = (getattr(self, '_g_inv_veleno_ok', 0)
                                             + int(np.sum(_mv & _nanv)))
                    regola = (regola + ' | e nelle %d celle AVVELENATE il valore DEVE '
                              'essere `nan` (esenzione PER CELLA ancorata al veleno: un '
                              'NUMERO li\' significa una cella scritta SENZA riscrivere '
                              'la derivata)' % int(np.sum(_mv)))
            if cattivo.ndim > 1:
                cattivo = np.any(cattivo, axis=tuple(range(1, cattivo.ndim)))
            if not np.any(cattivo):
                continue
            idx = np.where(cattivo)[0]
            vals = np.asarray(v)[idx]
            if vals.ndim > 1:
                vals = vals.reshape(len(idx), -1)[:, 0]
            extra = dict(quanti=int(len(idx)), su=int(len(cattivo)))
            # ⚠ se e' una grandezza per ARCO, si riportano anche i due NODI: un indice d'arco
            #   da solo non dice DOVE, perche' gli archi si riordinano a ogni mitosi.
            if len(cattivo) == len(self.d) and len(self.i) == len(self.d):
                k0 = int(idx[0])
                extra['arco'] = '%d-%d' % (int(self.i[k0]), int(self.j[k0]))
            self._g_inv_violati = getattr(self, '_g_inv_violati', 0) + 1
            raise DominioViolato(quale, regola, passo, idx,
                                 np.abs(vals).astype(float), dove, extra)
        self._g_inv_controllate = controllate
        return controllate

    def _smp_apri(self):
        """[SCALA_MIN_PASSO] Fotografa `d0` e `d` a INIZIO PASSO PIENO: da qui si misura la
        variazione TOTALE, una volta sola.

        ⚠ **E' IDEMPOTENTE, dalla cura `(c)1` del 2026-09-27:** la chiamano **tutte e
        cinque le leggi** del passo, in testa, e **la PRIMA che gira apre**. Le altre quattro
        escono subito.

        **Perche' cosi' e non nel chiamante:** i chiamanti delle cinque leggi sono **SEI**
        (`update()`, il benchmark, due costruttori di scena, `csv/_test_fork/_scena_video.py`,
        e `csv/_passo.py` che li legge per AST), e **una divergenza fra due di loro sarebbe
        invisibile**. L'idempotenza mette il confine **dentro** la cosa che deve rispettarlo,
        e lo rende **indipendente dall'ORDINE** -- che e' cio' che `H-ETC-2` permuta.
        """
        # APERTURA GIA' FATTA in questo passo: non si rifotografa, e si CONTA (`A8`), cosi'
        #   <<quante leggi hanno trovato la fotografia gia' aperta>> e' leggibile invece che
        #   supposto. Con le cinque leggi canoniche il contatore sale di 4 per passo.
        if getattr(self, '_smp_d0', None) is not None:
            self._g_smp_gia_aperta = getattr(self, '_g_smp_gia_aperta', 0) + 1
            return
        # [C4] la stessa fotografia serve alla coesione causale: UNA macchina, DUE utenti.
        if SCALA_MIN_PASSO or COES_CAUSALE:
            self._smp_d0 = np.array(self.d0, dtype=float, copy=True)
            self._smp_d = np.array(self.d, dtype=float, copy=True)
            self._g_smp_aperture = getattr(self, '_g_smp_aperture', 0) + 1

    def _smp_chirurgia(self, keep=None, nuovi=None):
        """[SCALA_MIN_PASSO] Lo snapshot subisce LE STESSE operazioni di `d0`.

        ⚠ E' LA PARTE DELICATA DELLA CURA, e va cablata invece che assunta: la `mitosi()`
        CAMBIA IL NUMERO DI ARCHI *(ne toglie con `[keep]`, ne aggiunge in coda)*, quindi un
        confronto `fine - inizio` fatto per posizione confronterebbe **archi diversi**.
        Gli archi NATI nel passo entrano con il **proprio valore di nascita**: la loro
        variazione e' ZERO e non vengono frenati -- e' giusto, perche' una nascita non e' una
        discesa."""
        if (not (SCALA_MIN_PASSO or COES_CAUSALE)
                or getattr(self, '_smp_d0', None) is None):
            return
        for _nome in ('_smp_d0', '_smp_d'):
            v = getattr(self, _nome, None)
            if v is None:
                continue
            if keep is not None:
                v = v[keep]
            if nuovi is not None and len(nuovi):
                v = np.concatenate([v, np.asarray(nuovi, dtype=float)])
            setattr(self, _nome, v)
        self._g_smp_chirurgie = getattr(self, '_g_smp_chirurgie', 0) + 1

    def _smp_chiudi(self):
        """[SCALA_MIN_PASSO] IL FRENO, UNA VOLTA SOLA, sulla variazione TOTALE del passo.

        `d0 <- inizio + _smorza(inizio, fine - inizio)`. Con spinte opposte di somma nulla
        `dx = 0`, che NON e' una discesa: il valore resta **intatto**, e il bias e' **zero
        esatto**. Non contiene l'ordine delle leggi."""
        v = getattr(self, '_smp_d0', None)
        # ⚠ la fotografia si CHIUDE sempre (anche se serve solo a `C4`), senno' resterebbe
        #   aperta e il passo dopo leggerebbe quella del passo prima. Ma si FRENA solo con `C3`.
        if v is None:
            return
        self._smp_d0 = None
        self._smp_d = None
        if not SCALA_MIN_PASSO:
            return
        if len(v) != len(self.d0):
            # NON si frena a caso su lunghezze diverse: si CONTA e si lascia stare.
            self._g_smp_disallineati = getattr(self, '_g_smp_disallineati', 0) + 1
            self._g_smp_shape = (len(v), len(self.d0))
            return
        dx = np.asarray(self.d0, dtype=float) - v
        self.d0 = v + self._smorza(v, dx, 'd0_passo')
        self._g_smp_chiusure = getattr(self, '_g_smp_chiusure', 0) + 1
        self._g_smp_discese = (getattr(self, '_g_smp_discese', 0) + int(np.sum(dx < 0.0)))
        self._g_smp_salite = (getattr(self, '_g_smp_salite', 0) + int(np.sum(dx > 0.0)))
        self._g_smp_nulli = (getattr(self, '_g_smp_nulli', 0) + int(np.sum(dx == 0.0)))

    def _sd0(self, dx, mask=None):
        """L'incremento effettivo su `d0`. A flag spento e' l'incremento stesso."""
        # [SCALA_MIN_PASSO, C3] PASSANTE: la singola scrittura NON si frena. Il freno si
        # applica UNA VOLTA a fine passo, sulla variazione TOTALE -- e' l'intero punto della
        # cura, perche' frenare scrittura per scrittura fa dipendere il risultato dall'ORDINE.
        if SCALA_MIN_PASSO:
            self._g_smp_passanti = getattr(self, '_g_smp_passanti', 0) + 1
            return dx
        if not SCALA_MIN:
            return dx
        return self._smorza(self.d0 if mask is None else self.d0[mask], dx, 'd0')

    def _nasce(self, v, dove="?", md=1, md0=1, meta=None):
        """NASCITA (concatenazione): il troncone sotto `LAM` si porta A `LAM`. Da li' in poi
        vale lo smorzamento. Non e' una regola di arresto nuova: e' il punto di partenza."""
        # [C3] anche con `SCALA_MIN_PASSO`: una NASCITA e' una concatenazione, non una discesa,
        # e il punto di partenza non e' un freno.
        # ⚠⚠ [`D38`, 2026-09-24] **IL GATE E' TOLTO: il presidio agisce SEMPRE.**
        #   Era `if not (SCALA_MIN or SCALA_MIN_PASSO): return v`, e **coi default del SORGENTE
        #   la legge `d >= LAM` era VIOLATA AL PASSO ZERO su 223 380 archi**. E' lo stesso
        #   schema che `E4-LAM` ha tolto al CONTROLLO e che era rimasto all'ESECUZIONE:
        #   **il controllo era legge, chi la faceva rispettare era un'opzione.**
        #   **NON E' UNA CURA, E' UN PRESIDIO** (decisione di Luca): con `SEMINA_LAM` acceso
        #   **non deve scattare mai**, e `_g_sm_nascite` e' la sua misura -- se sale, un arco
        #   e' nato sotto `LAM` **da un'altra strada** (la MITOSI: voce `M2` della coda).
        self._g_sm_nascite = getattr(self, '_g_sm_nascite', 0) + 1
        # [A8, `U2`, 2026-09-25] ⚠ `_g_sm_nascite` CONTA LE INVOCAZIONI, NON I TRONCAMENTI.
        #   Luca l'ha chiesto per sapere "quante volte `_nasce` ha troncato un figlio della
        #   mitosi", e **quel numero non c'era**: una chiamata che non tronca nulla lo fa
        #   salire ugualmente. Contatori byte-inerti (si somma, non si cambia):
        #     `_sm_vis<q>_<sito>`  quanti archi sono passati da qui (il denominatore)
        #     `_sm_tr<q>_<sito>`   quanti ARCHI sono stati portati a `LAM`
        #     `_sm_lun<q>_<sito>`  **LA LUNGHEZZA FABBRICATA**: `sum(LAM - v)` sui troncati,
        #                          cioe' il contributo DIRETTO di `_nasce` al gonfiamento,
        #                          **nelle stesse unita' del bilancio di quella grandezza**.
        #
        # ❌❌ **CORREZIONE DI LUCA, 2026-09-25 -- PRIMA C'ERA UN CONTATORE SOLO, E MESCOLAVA
        #   `d` CON `d0`.** Tre difetti in uno:
        #     ① `_sm_lunghezza` sommava contributi di `d` e di `d0` nello stesso numero,
        #        quindi **NON era "nelle unita' del bilancio di `d0`"** -- che era l'unica
        #        ragione per cui l'avevo scritto;
        #     ② il sito `dh` della mitosi era **SOTTOCONTATO DI 2**: `dh` ha `len(sel)` voci,
        #        ma finisce in `concatenate([d[keep], dh, dh])`, cioe' **DUE archi veri per voce**;
        #     ③ `_sm_visti` contava le VOCI, non gli ARCHI, con lo stesso errore.
        #
        #   **`dove` e' il SITO; `md`/`md0` dicono QUANTI ARCHI VERI di `d` e di `d0` diventa
        #   ogni voce di `v` in quel sito.** I quattro siti, letti dal codice:
        #     | sito                        | `md` | `md0` | perche'                             |
        #     | `semina`    (`_allaccia`)   |  1   |   1   | UNA chiamata vale per `d` E per `d0` |
        #     | `mitosi`    (`dh`)          |  2   |   0   | `concatenate([d[keep], dh, dh])`     |
        #     | `mitosi`    (`d0new`)       |  0   |   1   | `d0new` e' GIA' i due figli           |
        #     | `schwinger` (`dd`)          |  2   |   2   | `[d, dd, dd]` **e** `[d0, dd, dd]`   |
        #   **Lo Schwinger e' un QUARTO sito, `x2` su ENTRAMBE le grandezze**: non era fra i tre
        #   che il rilievo elencava, e va detto perche' cambia il conto.
        #
        # > **Solo `_sm_lund0_*` entra nel confronto con la crescita di `d0` in `P-GONFIA`.**
        _v = np.asarray(v, dtype=float)
        _sotto = _v < LAM
        _ntr = int(_sotto.sum())
        if meta is None:
            _fab = float(np.sum(LAM - _v[_sotto])) if _ntr else 0.0
        else:
            # ### `_fab` PER META', e non e' un'eleganza: `np.sum` su `2n` elementi
            #   ### **NON e' identica al bit** a `2 * np.sum` su `n` -- MISURATO, 4043
            #   differenze su 14000 *(`csv/_test_fork/_somma_meta/`)*. La somma calcolata
            #   ### **per meta' e poi sommata** a `t = 0.5` e' `s + s`, e ### **`s + s ==
            #   2*s` e' ESATTO** perche' il raddoppio e' uno scalamento per una potenza di
            #   due. ### ➜ **Cosi' il contatore `_sm_lun` resta identico al bit quando
            #   una chiamata con `md = 2` su `n` voci diventa una con `md = 1` su `2n`.**
            #   ### ⚠ `meta` e' il numero di voci della PRIMA meta'.
            _a = _v[:meta]
            _b = _v[meta:]
            _sa = _a < LAM
            _sb = _b < LAM
            _fab = ((float(np.sum(LAM - _a[_sa])) if _sa.any() else 0.0)
                    + (float(np.sum(LAM - _b[_sb])) if _sb.any() else 0.0))
        for _q, _m in (("d", md), ("d0", md0)):
            if not _m:
                continue
            _b = "_sm_%s%s_%s"
            for _pre, _val, _zero in (("lun", _m * _fab, 0.0),
                                      ("tr", _m * _ntr, 0),
                                      ("vis", _m * int(_v.size), 0)):
                _k = _b % (_pre, _q, dove)
                setattr(self, _k, getattr(self, _k, _zero) + _val)
        return np.maximum(v, LAM)

    def _peq_esatto(self, rho, flusso, dt_e, tau_bg):
        """[PEQ_ESATTO] Il rilassamento di `peq` in forma ESATTA, in due passi di Lie-Trotter.

        ① verso `rho` con `tau_bg`:   `peq <- rho + (peq-rho)*exp(-dt_e/tau_bg)`
        ② verso il punto fisso della diffusione, che e' **`peq + flusso`** in ENTRAMBI i rami
           di `DIFF_RES`:             `peq <- b + (peq-b)*exp(-dt_e/TAU_DIFF)`,  `b = peq+flusso`

        Ciascun passo e' una COMBINAZIONE CONVESSA fra il valore e il suo bersaglio, quindi
        **non puo' uscire dall'intervallo fra i due, per QUALUNQUE `dt`**. Con bersagli `>= 0`
        il risultato e' `>= 0` **senza pavimenti**.
        """
        peq = np.asarray(self.peq, dtype=float)
        dte = np.asarray(dt_e, dtype=float)
        a1 = np.exp(-dte / np.asarray(tau_bg, dtype=float))
        p1 = rho + (peq - rho) * a1
        bers = peq + flusso
        a2 = np.exp(-dte / TAU_DIFF)
        p2 = bers + (p1 - bers) * a2
        # CONTATORI (solo a flag ACCESO: non toccano il ramo spento).
        # `_g_peqx_salvati` e' il CONTROLLO POSITIVO CABLATO: quante volte l'Eulero sarebbe
        # andato sotto zero e la forma esatta NO. Se restasse 0 su un run che esplode, la cura
        # sarebbe inerte -- e si vedrebbe dal numero, non da un ragionamento.
        self._g_peqx_usi = getattr(self, '_g_peqx_usi', 0) + 1
        if len(peq):
            eul = peq + dte * ((rho - peq) / np.asarray(tau_bg, dtype=float)
                               + flusso / TAU_DIFF)
            self._g_peqx_salvati = (getattr(self, '_g_peqx_salvati', 0)
                                    + int(np.sum((eul < 0.0) & (p2 >= 0.0))))
            self._g_peqx_neg = getattr(self, '_g_peqx_neg', 0) + int(np.sum(p2 < 0.0))
            # il bersaglio della diffusione NEGATIVO e' l'unico caso in cui la dimostrazione
            # non vale (`DIFF_RES != 0`): si CONTA invece di assumere che non capiti.
            self._g_peqx_bers_neg = (getattr(self, '_g_peqx_bers_neg', 0)
                                     + int(np.sum(bers < 0.0)))
            self._g_peqx_min = min(getattr(self, '_g_peqx_min', float('inf')), float(p2.min()))
        return p2

    def _traccia_peq(self, rho, flusso, dt_e, tau_bg, i, j):
        """[TRACCIA_PEQ] I TRE NUMERI CHE MANCANO sull'aggiornamento di `peq` (`:4206`).

        PURE-READ: calcola e registra, non modifica `self.peq` ne' lo stato ne' l'RNG.

        Il numero di stabilita' e' `x = dt_e / tau_bg`: **un Eulero esplicito SCAVALCA il
        bersaglio per `x > 1` e OSCILLA DIVERGENDO per `x > 2`**. E' lo stesso criterio gia'
        cablato su `d0` con `_taup_cfl_max` (`:4412-4419`), e su `peq` non c'era.

        I TRE ESITI SONO CONTROFATTUALI E CALCOLATI A PARTE -- ed e' il punto: sommati non si
        saprebbe QUALE termine porta sotto zero.
        """
        peq = np.asarray(self.peq, dtype=float)
        if not len(peq):
            return
        dte = np.broadcast_to(np.asarray(dt_e, dtype=float), peq.shape)
        tb = np.broadcast_to(np.asarray(tau_bg, dtype=float), peq.shape)
        x = dte / tb
        self._g_peq_cfl_max = max(getattr(self, '_g_peq_cfl_max', 0.0), float(x.max()))
        self._g_peq_cfl_sopra1 = (getattr(self, '_g_peq_cfl_sopra1', 0)
                                  + int(np.sum(x >= 1.0)))
        self._g_peq_cfl_sopra2 = (getattr(self, '_g_peq_cfl_sopra2', 0)
                                  + int(np.sum(x >= 2.0)))
        solo_ril = peq + dte * (rho - peq) / tb
        solo_dif = peq + dte * (flusso / TAU_DIFF)
        insieme = peq + dte * ((rho - peq) / tb + flusso / TAU_DIFF)
        self._g_peq_neg = getattr(self, '_g_peq_neg', 0) + int(np.sum(insieme < 0.0))
        self._g_peq_neg_ril = (getattr(self, '_g_peq_neg_ril', 0)
                               + int(np.sum(solo_ril < 0.0)))
        self._g_peq_neg_dif = (getattr(self, '_g_peq_neg_dif', 0)
                               + int(np.sum(solo_dif < 0.0)))
        self._g_peq_archi = getattr(self, '_g_peq_archi', 0) + int(len(peq))
        self._g_peq_passi = getattr(self, '_g_peq_passi', 0) + 1
        # l'ARCO PEGGIORE: si tiene il minimo ASSOLUTO di tutto il run, col suo dettaglio.
        k = int(np.argmin(insieme))
        if float(insieme[k]) < getattr(self, '_g_peq_min', float('inf')):
            self._g_peq_min = float(insieme[k])
            self._g_peq_min_arco = (int(i[k]), int(j[k]))
            self._g_peq_min_quando = self._g_peq_passi
            self._g_peq_min_dett = dict(
                peq_prima=float(peq[k]), rho=float(rho[k]), flusso=float(flusso[k]),
                dt_e=float(dte[k]), tau_bg=float(tb[k]), x=float(x[k]),
                solo_rilassamento=float(solo_ril[k]), solo_diffusione=float(solo_dif[k]),
                insieme=float(insieme[k]))

    def _versione_codice(self):
        """IDENTITA' DI VERSIONE del codice in esecuzione, per il versionamento del DB.
        - `blob` = git blob hash dei BYTE ATTUALI del file (`git hash-object`): e' l'IDENTITA' di
          accetta/rifiuta. E' un hash di CONTENUTO (non richiede commit), stabile e uguale al blob
          committato quando il working tree e' pulito. Il branch NON entra nella chiave: stesso
          codice su branch diversi = stessa fisica.
        - `committed_blob`/`commit`/`branch` = METADATI (per rintracciare/worktree; branch diverso
          -> solo avviso). `dirty` = i byte attuali differiscono dal blob committato.
        - `content_hash` = sha256 dei byte: FALLBACK quando git non e' disponibile o per i DB legacy.
        Ritorna un dict. Cache per-processo (il file non cambia durante il run)."""
        cache = getattr(self, '_ver_codice_cache', None)
        if cache is not None:
            return cache
        import hashlib, sys, os, subprocess
        _file = os.path.abspath(sys.modules[type(self).__module__].__file__)
        content_hash = hashlib.sha256(open(_file, 'rb').read()).hexdigest()[:16]
        _dir = os.path.dirname(_file) or "."
        def _git(*args):
            try:
                r = subprocess.run(("git",) + args, cwd=_dir, capture_output=True,
                                   text=True, timeout=5)
                return r.stdout.strip() if r.returncode == 0 else None
            except Exception:
                return None
        blob = _git("hash-object", _file)          # blob dei byte ATTUALI (non serve commit)
        top = _git("rev-parse", "--show-toplevel")
        committed_blob = None
        if top:
            rel = os.path.relpath(_file, top).replace(os.sep, "/")
            committed_blob = _git("rev-parse", f"HEAD:{rel}")
        commit = _git("rev-parse", "HEAD")
        branch = _git("rev-parse", "--abbrev-ref", "HEAD")
        dirty = (blob is None) or (committed_blob is None) or (blob != committed_blob)
        cache = {'blob': blob, 'committed_blob': committed_blob, 'commit': commit,
                 'branch': branch, 'dirty': dirty, 'content_hash': content_hash}
        self._ver_codice_cache = cache
        return cache

    def salva_stato(self, path):
        """DB VERSIONATO + IDEMPOTENTE. Salva TUTTE le grandezze di stato (generico: scorre
        __dict__, cosi' non ne dimentica nessuna - requisito dell'idempotenza), PIU' lo stato
        dell'RNG (senno' la mitosi riparte con casuali diverse) e l'IDENTITA' di versione del codice
        (git blob dei byte attuali + metadati commit/branch/dirty). Al ricarico il blob viene
        verificato e RIFIUTATO se diverso: il DB non puo' iniettare uno stato vecchio in una
        fisica cambiata. `code_hash` (sha256) resta scritto per retro-compatibilita' col fallback."""
        import pickle, os, gzip
        ver = self._versione_codice()
        stato = {'code_hash': ver['content_hash'],   # LEGACY/fallback (retro-compat DB vecchi + no-git)
                 'content_hash': ver['content_hash'],
                 'blob': ver['blob'], 'committed_blob': ver['committed_blob'],
                 'commit': ver['commit'], 'branch': ver['branch'], 'dirty': ver['dirty'],
                 'rng_state': self.rng.bit_generator.state,
                 'attrs': {}}
        for k, v in self.__dict__.items():
            if k == 'rng':
                continue
            if isinstance(v, (np.ndarray, int, float, bool, np.integer, np.floating, str)):
                stato['attrs'][k] = v
        # [CORREZIONE DI DIFETTO, 2026-09-18 - categoria D del par.10: NESSUN FLAG]
        # IL DIFETTO: il filtro qui sopra accetta ndarray/scalari/str. `conc_nodi` e `conc_archi`
        # sono LIST e `masse_info` e' un DICT: non matchano nessuno di quei tipi e vengono SCARTATI
        # IN SILENZIO. La docstring dice "salva TUTTE le grandezze di stato ... cosi' non ne
        # dimentica nessuna": per queste tre NON e' vero. Conseguenza misurabile: dopo un
        # salva/ricarica il lignaggio delle coorti RIPARTE VUOTO, e ogni misura di appartenenza
        # fatta su uno snapshot ricaricato guarda un sistema SENZA storia.
        # LA CURA: si aggiungono ESPLICITAMENTE, e NON si allarga il filtro - allargarlo farebbe
        # entrare anche altro (cache derivate, `_S`, kernel), e quello che entra va SAPUTO.
        # PERCHE' NON TOCCA LA FISICA: sono strutture di MISURA PURA. Enumerati dal disco tutti i
        # lettori - `indici_massa_vivi`, `aggiorna_pesi_concorrenza`, `tracking_masse`,
        # `_registra_concorrenza`, `_ripara_tracking` - NESSUNO e' chiamato da `step()`, `mitosi()`
        # o `scuoti_vuoto()`. E `salva_stato` non e' sul percorso di integrazione.
        # NB: l'eredita' alla mitosi c'era GIA' (:3951-3954, e il ramo Schwinger :4076-4082):
        # mancava SOLO la persistenza.
        for _k_track in ('conc_nodi', 'conc_archi', 'masse_info'):
            _v_track = getattr(self, _k_track, None)
            if _v_track is not None:
                stato['attrs'][_k_track] = _v_track
        tmp = path + '.tmp'
        # [ARCHIVIO, 2026-09-19] COMPRESSIONE PER ESTENSIONE. Il CONTENUTO non cambia di un byte:
        # cambia solo il TRASPORTO. `os.replace` resta, quindi l'ATOMICITA' e' INTATTA, e restano
        # intatti `rng_state`, le tre strutture di tracking di Z53 e la verifica del blob.
        # HDF5 e' stato SCARTATO: perderebbe l'atomicita' e non serializza `rng_state`/`conc_nodi`.
        #
        # ⚠ E IL `with` NON E' UN ABBELLIMENTO, E' UNA CORREZIONE NECESSARIA: la forma precedente
        # (`open(tmp,'wb')` passato direttamente a `pickle.dump`) NON CHIUDEVA MAI IL FILE, si
        # affidava al refcount di CPython. Con un file normale funziona -- il buffer viene scaricato
        # alla distruzione. Con `gzip` NO: un `GzipFile` non chiuso puo' lasciare il TRAILER
        # INCOMPLETO e il file ILLEGGIBILE. Senza il `with`, la compressione produrrebbe archivi
        # rotti in modo silenzioso, che e' il difetto peggiore possibile qui.
        # [ARCHIVIO, 2026-09-19] LIVELLO 1, PER DECISIONE DI LUCA E SU NUMERI MISURATI.
        # `gzip.open` usa `compresslevel=9` DI DEFAULT, e quel 9 non lo aveva scelto nessuno.
        # MISURATO su uno snapshot vero di 27.73 MB (csv/_seal_fork/_costo_archivio_2026-09-19.txt):
        #     nessuna compressione  0.129 s   27.73 MB   1.000x
        #     livello 1             0.82  s   16.08 MB   1.725x
        #     livello 9             4.42  s   15.77 MB   1.759x
        # Il livello 9 costa 5.4 VOLTE il livello 1 per il 2 % di spazio in piu', ed e' 34 volte
        # piu' lento dello scrivere non compresso. "Indefendibile" (Luca, 2026-09-19).
        # E IL NUMERO CHIUDE ANCHE LA PROPOSTA IBRIDA pickle+HDF5: 1.76x su float64 densi e' IL
        # LIMITE DEL DATO, non del formato, quindi HDF5 con compressione non farebbe molto meglio.
        # NB: il default resta NON COMPRESSO -- gzip si attiva solo se il path finisce in `.gz`.
        _apri = gzip.open if str(path).endswith('.gz') else open
        _kw = {'compresslevel': 1} if str(path).endswith('.gz') else {}
        with _apri(tmp, 'wb', **_kw) as _fh:
            pickle.dump(stato, _fh, protocol=pickle.HIGHEST_PROTOCOL)
        os.replace(tmp, path)   # scrittura atomica: o il DB e' completo o non c'e'
        return ver['blob'] or ver['content_hash']

    def carica_stato(self, path):
        """Ricarica lo stato dal DB. VERIFICA l'IDENTITA' di versione: RIFIUTA se il codice e'
        cambiato (protezione fisica-vecchia/fisica-nuova). Chiave di rifiuto = git BLOB dei byte
        (branch/commit sono solo metadati: branch diverso -> avviso, non rifiuto). Fallback su
        sha256 del contenuto se git non e' disponibile o per i DB legacy. Ripristina anche l'RNG."""
        import pickle, os, gzip
        if not os.path.exists(path):
            return False
        # [ARCHIVIO, 2026-09-19] SI ACCETTANO ENTRAMBI I FORMATI. Senza questo i `.pkl` gia' scritti
        # diventerebbero illeggibili al primo run compresso -- e' il sigillo V7.
        _apri = gzip.open if str(path).endswith('.gz') else open
        with _apri(path, 'rb') as _fh:
            stato = pickle.load(_fh)
        ver = self._versione_codice()
        db_blob = stato.get('blob')
        if db_blob is not None and ver['blob'] is not None:
            # NUOVO schema: identita' = git blob dei byte del file.
            if db_blob != ver['blob']:
                raise RuntimeError(
                    f"DB RIFIUTATO: codice diverso (blob DB={db_blob} vs ora={ver['blob']}). "
                    f"DB da commit={stato.get('commit')} branch={stato.get('branch')}; "
                    f"ora commit={ver['commit']} branch={ver['branch']}. La fisica e' cambiata. "
                    f"Esegui la versione giusta (git worktree/checkout del commit del DB) o usa --db-cleanup.")
            if stato.get('branch') and ver['branch'] and stato.get('branch') != ver['branch']:
                print(f"[db] AVVISO: branch diverso (DB={stato.get('branch')} vs ora={ver['branch']}), "
                      f"ma codice IDENTICO (stesso blob) -> accetto.")
            if ver['dirty'] or stato.get('dirty'):
                print("[db] AVVISO: working tree SPORCO (codice non committato): identita' sui byte attuali.")
        else:
            # LEGACY (solo code_hash) o git non disponibile: fallback su sha256 del contenuto.
            db_hash = stato.get('content_hash', stato.get('code_hash'))
            if db_hash != ver['content_hash']:
                raise RuntimeError(
                    f"DB RIFIUTATO: versione codice diversa (DB={db_hash} vs ora={ver['content_hash']}) "
                    f"[fallback sha256: DB legacy o git non disponibile]. Usa --db-cleanup per ripartire pulito.")
            if db_blob is None:
                print("[db] AVVISO: DB legacy (solo sha256): accettato per contenuto identico.")
        for k, v in stato['attrs'].items():
            setattr(self, k, v)
        self.rng.bit_generator.state = stato['rng_state']
        # INVALIDA le cache derivate (matrice sparsa _S, permutazione, kernel): non sono ndarray,
        # quindi non erano nel salvataggio; vanno ricostruite dalla topologia caricata (i/j/n).
        # Senza questo, _mat() userebbe la struttura vecchia -> mismatch (lo stana l'idempotenza).
        self._S = None
        if hasattr(self, '_perm'): self._perm = None
        if hasattr(self, '_ker_cache'): self._ker_cache = {}
        return True

    def _cs_nodo(self, I, w):
        """Campo della velocita' metrica locale per nodo (ramo cs-dinamico). Unica fonte della
        legge cs_eff(rho): normalizzazione strettamente locale (vicini topologici) e floor
        emergente dalla saturazione razionale del campo, senza costanti minime arbitrarie."""
        n = self.n
        W_loc = self._mat(w)
        media_vicini = (W_loc @ I[:n]) / np.maximum(W_loc @ np.ones(n), 1e-9)
        u_nodo = I[:n] / np.maximum(media_vicini, 1e-9)
        # [CORREZIONE DI DIFETTO, 2026-09-16 - categoria D del par.10: NESSUN FLAG]
        # IL DIFETTO: la docstring qui sopra dichiara "senza costanti minime arbitrarie", ma la
        # forma precedente era `CS_M / (1 + GAMMA*sqrt(I))` con GAMMA = 0.05 (:166), che FISSA una
        # densita' critica ASSOLUTA: `GAMMA*sqrt(I) = 1` per `I = 1/GAMMA^2 = 400`. Quel 400 e'
        # esattamente la costante arbitraria che la docstring nega (par.3), ed e' una SCALA ASSOLUTA
        # in un modello RELAZIONALE, che per premessa non ne ha.
        # LA CURA: la scala diventa `Lam`, l'ENERGIA DEL VUOTO, che il sistema CALCOLA da se'.
        # `I/Lam` e' gia' il rapporto di densita' adimensionale del modello, con un significato
        # fisico: sotto `Lam` sei vuoto, sopra sei materia. Il codice lo usa gia' cosi' in due
        # punti (`amp = sqrt(Lam)/(1 + I2/Lam)`, :534 e :1986). Zero coefficienti nuovi.
        #
        # PERCHE' `np.mean(_I)` E NON `lambda_vuoto(self)`, che sarebbe lo stesso numero:
        #   (a) `lambda_vuoto` contiene `calcola_psi()`, che SCRIVE `self.psi`: sarebbe una
        #       mutazione di stato dentro una funzione di sola lettura, chiamata dentro `step`;
        #   (b) `_cs_nodo` e' chiamata DUE volte, e a :2943 riceve lo SNAPSHOT `psi_t`, mentre
        #       `lambda_vuoto(self)` leggerebbe `self.psi` -> scala e numeratore da DUE STATI
        #       DIVERSI. Con `np.mean(_I)` la scala viene SEMPRE dagli stessi dati del numeratore.
        #
        # PERCHE' LA FORMA E' `sqrt(_I) * sqrt(1.0/_scala)` E NON `sqrt(_I/_scala)`:
        #   sono matematicamente uguali ma NON bit-identiche. Con `_scala = 400.0` esatto:
        #       sqrt(I/scala)            -> max|d| = 3.469e-18, 4601 elementi diversi
        #       sqrt(I)/sqrt(scala)      -> max|d| = 3.469e-18, 4477 elementi diversi
        #       sqrt(I)*sqrt(1.0/scala)  -> max|d| = 0.000e+00, ZERO elementi diversi
        #   perche' `np.sqrt(1.0/400.0) == 0.05` ESATTAMENTE. Solo questa forma rende il sigillo
        #   R1 (riduzione al limite: Lam = 400 -> la vecchia legge) una BYTE-IDENTITA' vera invece
        #   di un criterio impossibile da soddisfare per un ulp. Misurato, non dedotto.
        #   NB: `1.0/GAMMA**2` vale 399.99999999999994, NON 400 (0.05 non e' binario-esatto):
        #   il sigillo deve forzare il LETTERALE 400.0.
        #
        # [TURBO DIAGNOSTICO] UNICO punto in cui la scala e' amplificata. Default GAMMA_TURBO = 1.0
        # -> `_scala = _Lam / 1.0` -> byte-identico alla forma senza turbo (x/1.0 == x esatto).
        # Per K > 1 la scala SCENDE, quindi `cs_floor` SCENDE: comportamento invariato.
        # Ogni ALTRO uso di GAMMA nel file resta ORIGINALE: in particolare `satura()` e la
        # saturazione del campo spinoriale NON sono toccate (sigillo T2). GAMMA sparisce da QUI e
        # SOLO da qui.
        _I = np.maximum(I[:n], 0.0)
        _Lam = float(np.mean(_I)) if n > 0 else 0.0     # == lambda_vuoto(self) sugli stessi dati
        # il clamp 1e-30 e' PROTEZIONE DI DIVISIONE, non un parametro: scatta solo a sistema vuoto
        # (Lam = 0), dove qualunque valore darebbe cs_floor = CS_M. Contato (par.9, P5).
        if not (_Lam > 1e-30):
            self._cs_lam_degenere = getattr(self, "_cs_lam_degenere", 0) + 1
        _scala = max(_Lam, 1e-30) / (GAMMA_TURBO * GAMMA_TURBO)
        cs_floor = CS_M / (1.0 + np.sqrt(_I) * np.sqrt(1.0 / _scala))
        cs_floor = np.minimum(cs_floor, CS_M)
        transizione = 0.5 * (1.0 + np.tanh(1.0 - u_nodo))
        return cs_floor + (CS_M - cs_floor) * transizione

    def _bloch_ritardato(self, nb_cur, ii, jj):
        """[FORK SU(2) - STRATO 1] Aggiorna e restituisce il BLOCH RITARDATO n(t-tau) per nodo.

        E' l'unico pezzo dello Strato 1: la connessione dello Strato 0 e' identica, cambia solo da
        QUANDO vengono i Bloch che la costruiscono. Il trasporto agisce sugli spinori CORRENTI.

        LEGGE (primo ordine, quindi passo ESATTO e MAI Verlet, par.4):
            dn_ret/dt = (n_cur - n_ret) / tau          tau = d/cs (tempo-luce d'arco)
            alpha = 1 - exp(-dt_n/tau)                 dt_n = DT*r = TEMPO PROPRIO del nodo
        Il tic e' quello LOCALE, non il DT di coordinata: tau e' tempo proprio, e usare DT
        cancellerebbe la dipendenza dall'orologio del luogo (frame preferito). Sigillo S7.
        e il passo si esegue come SLERP GEODETICO sulla sfera, non come blend lineare: n_ret deve
        restare un VERSORE (|n| = 1). Si rilassa il BLOCH, NON la matrice U/N: un blend lineare di
        matrici uscirebbe da SU(2) (par.4). La fase resta sullo stato corrente; qui vive solo la
        direzione.

        LIMITI (li verifica il sigillo S2/S6):
          * tau -> 0  => alpha -> 1 => n_ret = n_cur  => si riduce ESATTAMENTE allo Strato 0;
          * sistema a RIPOSO (Bloch fermi) => n_ret resta = n_cur => inerte => scalare.
        Cioe': la memoria "morde" solo dove la configurazione evolve entro il tempo-luce tau.

        LOCALE PURA (par.4): d_nodo e' la media degli archi INCIDENTI al nodo, cs e' per nodo.
        Nessuna media globale, nessun parametro nuovo (d, cs, DT, LAM esistono gia').

        NON e' pure-read: aggiorna `self._nb_ret` (e' lo stato della memoria). Non consuma `net.rng`.
        Chiamata UNA volta per passo, dall'unico call-site di `_coppia_interferenza`."""
        n = self.n
        nb_cur = np.asarray(nb_cur, float)[:n]
        nbr = getattr(self, "_nb_ret", None)
        if nbr is None or len(nbr) != n:
            # Primo passo (o conteggio nodi cambiato fuori dalla mitosi): non c'e' ANCORA un passato.
            # Ritardato := corrente -> nessun effetto. E' corretto: la causalita' non inventa memoria.
            self._nb_ret = nb_cur.copy()
            return self._nb_ret
        nbr = np.asarray(nbr, float)

        # --- tau = d/cs, per nodo -----------------------------------------------------------
        tau = self._tempo_luce_nodo(ii, jj)
        # Il tic con cui si rilassa e' il TEMPO PROPRIO del nodo, dt_n = DT*r, non DT. tau = d/cs e'
        # tempo proprio: rilassarlo col tempo di COORDINATA mescolerebbe due frame e cancellerebbe la
        # dipendenza dall'orologio locale, cioe' imporrebbe una foliazione globale sincrona a un
        # processo locale. Tutto il resto della fisica integra gia' in dt_n/dt_e (phivel, tw): DT nudo
        # vive solo nel conteggio dei sottopassi CFL. Un nodo con r piccolo (tempo dilatato) ricorda
        # piu' a lungo, ed e' esattamente quello che deve fare.
        r_loc = getattr(self, "_r_corrente", None)
        if r_loc is None or len(r_loc) < n:
            dt_n = np.full(n, DT)           # orologio globale (TAU_LOC = 0): r == 1 -> dt_n = DT
        else:
            dt_n = DT * np.asarray(r_loc, float)[:n]
        alpha = 1.0 - np.exp(-dt_n / tau)   # rilassamento ESATTO, non un eulero esplicito

        # --- passo geodetico sulla sfera (slerp) --------------------------------------------
        dot = np.clip(np.sum(nbr * nb_cur, axis=1), -1.0, 1.0)
        Om = np.arccos(dot)
        sinOm = np.sin(Om)
        # Due degenerazioni NUMERICHE (non fisiche, non soglie tarate): assi coincidenti (Om~0, lo
        # slerp e' 0/0) e assi antipodali (Om~pi, sin(Om)~0: NON esiste una geodetica unica). In
        # entrambe si usa l'interpolazione lineare, poi si normalizza.
        lineare = (Om < 1e-6) | (sinOm < 1e-12)
        a = alpha[:, None]
        lin = (1.0 - a) * nbr + a * nb_cur
        sl = (nbr * np.sin((1.0 - alpha) * Om)[:, None] +
              nb_cur * np.sin(alpha * Om)[:, None]) / np.maximum(sinOm, 1e-30)[:, None]
        out = np.where(lineare[:, None], lin, sl)
        nor = np.linalg.norm(out, axis=1)
        morto = nor <= 1e-12                # antipodali esatti a meta' strada: l'interpolazione si
        if np.any(morto):                   # annulla. Nessuna direzione da inventare: resta il presente.
            out[morto] = nb_cur[morto]
            nor[morto] = 1.0
        out = out / np.maximum(nor, 1e-30)[:, None]
        # LIMITE tau->0 preso ALLA LETTERA: alpha = 1 significa "nessuna memoria", il ritardato E' il
        # corrente. Senza questa riga la ri-normalizzazione qui sopra sporcherebbe l'ultimo bit e la
        # riduzione allo Strato 0 sarebbe 1e-16 invece che 0.000e+00 (sigillo S2).
        pieno = alpha >= 1.0
        if np.any(pieno):
            out[pieno] = nb_cur[pieno]
        self._nb_ret = out
        return out

    @staticmethod
    def _cs_arco_da_nodo(cs_nodo, ii, jj):
        """MEDIA ARMONICA del `cs` sui due estremi: il COLLO DI BOTTIGLIA CAUSALE d'arco.

        **UNICO punto del file in cui questa relazione e' scritta.** Estratta da `step()`
        (`:4791`) il 2026-09-24 **senza cambiarne una virgola**, perche' `mitosi()` ne ha
        bisogno per `tau_arco = d/cs_arco` (`CURA 2`) e **duplicarla avrebbe significato avere
        due leggi che possono divergere** -- lo stesso argomento del docstring di
        `_tempo_luce_nodo`.

        PERCHE' ARMONICA E NON ARITMETICA: e' un COLLO DI BOTTIGLIA. Il commento originale di
        `step()` lo diceva gia', ed e' la ragione per cui il sistema ha DUE medie d'arco con
        domini diversi: **aritmetica per il TEMPO** (`dt_e`), **armonica per la VELOCITA'**.
        Non se ne inventa una terza.
        """
        return (2.0 * cs_nodo[ii] * cs_nodo[jj] /
                np.maximum(cs_nodo[ii] + cs_nodo[jj], 1e-12))

    def _r_nodo_mitosi(self):
        """L'OROLOGIO per NODO, per il gradiente di tempo della mitosi. Guardia CONTATA (`A8`).

        Il fallback e' `1` = "nessuna dilatazione", **la stessa convenzione che `ritmo()` usa
        quando non c'e' un passato** (`np.ones`): non una convenzione nuova.
        `_r_corrente` e' un array PER NODO attraversato da un punto di crescita, cioe' la
        classe `A8b` di `_cs_nodo_prev` (71.88 %) e `_psi_spin_prec` (95.33 %): si contano
        QUATTRO cose, non una -- invocazioni, salti, la FORMA al fallimento, e QUANDO.
        """
        n = self.n
        self._tum_r_tot = getattr(self, "_tum_r_tot", 0) + 1
        r = getattr(self, "_r_corrente", None)
        if r is None or len(r) < n:
            self._tum_r_salti = getattr(self, "_tum_r_salti", 0) + 1
            self._tum_r_forma = (-1 if r is None else len(r), n)
            self._tum_r_quando = self._tum_r_tot
            return np.ones(n)
        return np.asarray(r, dtype=float)[:n]

    def _fattore_tempo_arco(self, n_archi):
        """`dt_e/DT` per ARCO: il fattore di tempo proprio, **LETTO e non ricalcolato**.

        `dt_e = DT*0.5*(r_i+r_j)` e' **IL** tempo d'arco del sistema (`:4369`), e `step()` lo
        lascia in `_dt_e_ultimo`. Ricalcolarlo qui sarebbe **una seconda formula per lo stesso
        tempo**, cioe' due leggi. Fallback `1` = nessuna dilatazione, CONTATO.
        """
        self._tum_t_tot = getattr(self, "_tum_t_tot", 0) + 1
        dte = getattr(self, "_dt_e_ultimo", None)
        a = None if dte is None else np.asarray(dte, dtype=float)
        if a is None or a.ndim == 0 or len(a) != n_archi:
            self._tum_t_salti = getattr(self, "_tum_t_salti", 0) + 1
            self._tum_t_forma = (-1 if a is None else (0 if a.ndim == 0 else len(a)), n_archi)
            self._tum_t_quando = self._tum_t_tot
            return np.ones(n_archi)
        return a / DT

    def _tau_arco_causale(self, n_archi):
        """Il RITARDO CAUSALE d'arco: `tau = d / cs_arco`, e **ha le unita' di un TEMPO**.

        `[LAM] / [LAM/DT] = [DT]`. E' la stessa legge `tau = d/cs` che `FORK_SU2_MEM` usa per
        il ritardo dei Bloch, **al livello dell'ARCO** invece che del nodo -- e li' `d` e
        `cs_arco` sono DIRETTAMENTE disponibili, senza la media sul grado che la versione
        nodale deve fare.

        ** NESSUN CLAMP, ed e' una decisione di Luca**: `d >= LAM` e' una LEGGE (invariante
        `C5`, verificato SEMPRE da `E4-LAM`) e `cs > 0` e' DERIVATO (`cs_floor > 0`,
        `transizione in (0,1)` stretto). Se mai uno dei due fosse zero, e' il livello NUMERICO
        (`np.seterr(divide='raise')`) a fermarsi **con la riga esatta**: `A11` dice di
        sostituire il limite col RILEVAMENTO dell'errore, non di nasconderlo.
        """
        self._tum_cs_tot = getattr(self, "_tum_cs_tot", 0) + 1
        csn = getattr(self, "_cs_nodo_prev", None)
        if csn is None or len(csn) < self.n:
            self._tum_cs_salti = getattr(self, "_tum_cs_salti", 0) + 1
            self._tum_cs_forma = (-1 if csn is None else len(csn), self.n)
            self._tum_cs_quando = self._tum_cs_tot
            cs_arco = np.full(n_archi, CS_M, dtype=float)   # la convenzione di `:4795`
        else:
            cs_arco = self._cs_arco_da_nodo(np.asarray(csn, dtype=float), self.i, self.j)
        return np.asarray(self.d, dtype=float)[:n_archi] / cs_arco

    def _tempo_luce_nodo(self, ii, jj):
        """TEMPO-LUCE per nodo: `tau = d_nodo / cs_nodo`. **E' una LEGGE, non un numero.**

        UNICO punto del file in cui questa relazione e' scritta. La usano DUE meccanismi, per la
        STESSA ragione causale:
          * lo **STRATO 1** (`_bloch_ritardato`): la connessione nasce dai Bloch a `t - tau`;
          * il **rilassamento di `omega_s`** sotto `TAU_LUCE` (riga ~1913).
        Estratta da `_bloch_ritardato` il 2026-09-15 **senza cambiarne una virgola**: era gia'
        cablata li', e duplicarla avrebbe significato avere due leggi che possono divergere. Il
        sigillo T1 (flag OFF byte-identico) dimostra che l'estrazione non ha alterato nulla.

        PERCHE' E' UNA LEGGE E NON UN NUMERO: `d_nodo/cs_nodo` **cambia con lo stato**. Se la
        geometria si dilata, `tau` la segue; se `cs` cala nel pozzo, `tau` cresce. Un numero resta
        fermo mentre l'universo cambia; una legge no. E' il senso forte del par.3 (zero manopole):
        non "scegli bene il numero", ma **non scrivere numeri, scrivi relazioni**.

        ZERO COSTANTI DI AGGIUSTAMENTO: il coefficiente e' **1**, l'unico che non si tara. Un
        `K*d/cs` con `K` scelto sarebbe un numero travestito da legge.

        I DUE GUARDIE NON SONO MANOPOLE, SONO EREDITATE da questo stesso blocco:
          * nodo isolato (nessun arco da cui leggere la scala) -> `d_nodo = LAM`, la scala che
            esiste gia' nel sistema;
          * `1e-12` / `1e-30` sono le regolarizzazioni anti-zero gia' presenti, non soglie nuove.

        PURE-READ SULLA FISICA: non consuma `net.rng` e non scrive nessuna grandezza che la fisica
        rilegga. Scrive SOLO i tre accumulatori diagnostici `_cs_chiamate` / `_cs_fallback` /
        `_cs_fallback_ultimo` (contatore del ramo else, 2026-09-15): un fallback non misurato e' un
        comportamento sconosciuto, e questo ne scattava nell'80% dei passi.
        """
        n = self.n
        dd = self.d
        # [A8, 2026-09-20] CONTABILITA' DELLA GUARDIA -- byte-inerte: si CONTA, non si cambia.
        # Un ramo che salta in silenzio e' un comportamento SCONOSCIUTO (A8), e questa forma ha
        # gia' prodotto due volte mesi di dati sbagliati: `_cs_nodo_prev` (71.88 %) e
        # `_psi_spin_prec` (95.33 %). Si registrano QUATTRO cose, non una: le invocazioni, i
        # salti, LA FORMA al fallimento (le due lunghezze) e QUANDO -- l'indice dell'ultima
        # invocazione saltata. Il conteggio da solo non distingue un TRANSITORIO delle prime
        # chiamate da un comportamento PRINCIPALE sparso su tutto il run: danno lo stesso numero.
        # QUI IL FALLBACK C'E' GIA', esplicito e derivato (`np.full(n, LAM)`): manca solo il
        # CONTEGGIO. Mezza cura, si completa -- non si cambia il comportamento.
        self._g_tempo_luce_tot = getattr(self, "_g_tempo_luce_tot", 0) + 1
        if len(ii) and len(dd) == len(ii):
            grado = (np.bincount(ii, minlength=n) + np.bincount(jj, minlength=n)).astype(float)
            somma = (np.bincount(ii, weights=dd, minlength=n) +
                     np.bincount(jj, weights=dd, minlength=n))
            d_nodo = somma / np.maximum(grado, 1.0)
            d_nodo[grado <= 0] = LAM        # nodo isolato: nessun arco da cui leggere la scala
        else:
            d_nodo = np.full(n, LAM)        # fallback: LAM e' la scala gia' esistente (par.3)
            # [A8, 2026-09-20] IL FALLBACK C'ERA GIA', esplicito e derivato: mancava il CONTEGGIO.
            # Mezza cura completata -- il comportamento non cambia di un bit.
            # MISURATO: 0 salti su 34 invocazioni (sigillo 3/3, 4edfab2).
            self._g_tempo_luce_salti = getattr(self, "_g_tempo_luce_salti", 0) + 1
            self._g_tempo_luce_shape = (len(ii), len(dd))
            self._g_tempo_luce_quando = self._g_tempo_luce_tot
        d_nodo = np.maximum(d_nodo, 1e-12)
        csp = getattr(self, "_cs_nodo_prev", None)
        # CONTATORE DEL FALLBACK (diagnostico, non fisico): quante volte questo ramo else e' davvero
        # quello che gira? Un fallback mai misurato e' un comportamento sconosciuto. Non consuma RNG,
        # non tocca nessuna grandezza letta dalla fisica: sono soli tre accumulatori.
        self._cs_chiamate = getattr(self, "_cs_chiamate", 0) + 1
        if csp is not None and len(csp) >= n:
            cs_nodo = np.maximum(np.asarray(csp, float)[:n], 1e-12)   # cs di UN PASSO FA (e' un ritardo)
        else:
            self._cs_fallback = getattr(self, "_cs_fallback", 0) + 1
            self._cs_fallback_ultimo = (int(n), int(len(csp)) if csp is not None else -1)
            # --cs-dinamico OFF (o primo passo): cs e' costante = CS_M. Alle densita' attuali cs e'
            # comunque quasi-costante (I~0.05 contro soglia ~400), quindi tau ~ d/CS_M: il RITARDO
            # esiste, ma la sua VARIAZIONE spaziale (la curvatura) e' debole finche' cs non e' vivo.
            cs_nodo = np.full(n, CS_M)
        return np.maximum(d_nodo / cs_nodo, 1e-30)

    def _coppia_interferenza(self, A, z):
        """[FASE 3] Coppia di fase sugli archi. Ramo OFF: interferenza SCALARE
        K_C*Im(conj(z) (mat(A)@z)) con z=e^{i phi} (identica al canonico). Ramo CAMPO_SPINORIALE:
        OVERLAP SPINORIALE <psi_i|psi_j> = conj(a_i)a_j + conj(b_i)b_j; la somma pesata sugli archi
        e' sum_j A_ij <psi_i|psi_j> = conj(a)(mat(A)@a) + conj(b)(mat(A)@b). Generalizzazione ESATTA:
        nel limite spinore in fase (b=0, a=e^{i phi}) il termine b sparisce e a=z -> coppia identica
        alla scalare. Legge lo SNAPSHOT _psi_spinor di inizio passo (causalita' Jacobi: _passo_spinoriale
        lo aggiorna DOPO). Nessun parametro nuovo: stesso K_C, stesso kernel A. Se lo spinore non c'e'
        (feature off) ricade sul ramo scalare."""
        n = self.n
        if CAMPO_SPINORIALE:
            _ps = getattr(self, '_psi_spinor', None)
            if _ps is not None and len(_ps) >= n:
                _ps = np.asarray(_ps)[:n]
                _a = _ps[:, 0]; _b = _ps[:, 1]
                if FORK_SU2 and len(self.i):
                    # [FORK SU(2) - STRATO 0, PEZZO 3] Trasporto NON-ABELIANO sugli archi.
                    # Lo scalare A_ij resta (e' il kernel: peso d'arco * cos(dphi0)); cambia CHE COSA
                    # viene trasportato: non piu' a e b separatamente con lo stesso numero, ma lo
                    # SPINORE INTERO attraverso la matrice N_ij/2 in SU(2), che MESCOLA a,b.
                    #   sum_j A_ij (N_ij/2) psi_j  ->  4 matvec: le componenti (00,01,10,11) di N.
                    # I Bloch vengono da _psi_spinor, cioe' dagli STESSI stati che vengono
                    # trasportati: cosi' N_ij e' la connessione di Berry DI quegli stati, e la
                    # freccia causale resta spinore -> link (i nodi guidano, gli archi ricordano).
                    _ii = self.i; _jj = self.j
                    _nb = np.stack([2.0 * np.real(np.conj(_a) * _b),
                                    2.0 * np.imag(np.conj(_a) * _b),
                                    np.abs(_a) ** 2 - np.abs(_b) ** 2], axis=1)
                    _nb = _nb / np.maximum(np.linalg.norm(_nb, axis=1), 1e-30)[:, None]
                    # [STRATO 0] la connessione nasce dall'ISTANTE -> INERTE per teorema (vedi
                    # FORK_SU2_MEM). [STRATO 1] nasce dal PASSATO n(t-tau) -> il teorema non si
                    # applica. Cambia SOLO la sorgente della connessione: il trasporto qui sotto
                    # resta sugli spinori CORRENTI _a,_b, e la freccia causale resta spinore -> link.
                    _nb_conn = _nb
                    if FORK_SU2_MEM:
                        _nb_conn = self._bloch_ritardato(_nb, _ii, _jj)
                    # N_ij trasporta n_j -> n_i: il verso giusto per Im<psi_i| N_ij |psi_j>.
                    _N = self._link_su2_N(_nb_conn[_ii], _nb_conn[_jj]) * 0.5   # il /2: N/2 = I ad allineati
                    _N00 = A * _N[:, 0, 0]; _N01 = A * _N[:, 0, 1]
                    _N10 = A * _N[:, 1, 0]; _N11 = A * _N[:, 1, 1]
                    # direzione opposta = N_ji = N_ij^dag (hermitiana: conserva l'azione-reazione)
                    _c00 = self._mat2(_N00, np.conj(_N00)) @ _a
                    _c01 = self._mat2(_N01, np.conj(_N10)) @ _b
                    _c10 = self._mat2(_N10, np.conj(_N01)) @ _a
                    _c11 = self._mat2(_N11, np.conj(_N11)) @ _b
                    return K_C * np.imag(np.conj(_a) * (_c00 + _c01)
                                         + np.conj(_b) * (_c10 + _c11))
                return K_C * np.imag(np.conj(_a) * (self._mat(A) @ _a)
                                     + np.conj(_b) * (self._mat(A) @ _b))
        return K_C * np.imag(np.conj(z) * (self._mat(A) @ z))

    def step(self):
        if self.n < 2 or not len(self.i): return
        i, j = self.i, self.j
        
        # --- EVALUATE-THEN-COMMIT: Snapshot rigoroso di inizio passo (tempo t) ---
        # Congeliamo lo stato iniziale affinché tutti i calcoli leggano i campi sincronizzati,
        # eliminando il bias sequenziale senza perdere lo stile dei commenti originali.
        _phi_t = self.phi.copy()
        _tw_t = self.tw.copy()
        _phivel_t = self.phivel.copy()

        r = self.ritmo()                       # None se l'orologio e' globale
        if r is None:
            dt_n = DT; dt_e = DT
        else:
            dt_n = DT * r                      # per nodo
            dt_e = DT * 0.5 * (r[i] + r[j])    # per arco
            self._psi_prec = self.psi.copy()
            # [A8, 2026-09-20] (a) NESSUNA RAGIONE DICHIARATA, ed e' LA CAUSA di un sintomo
            # gia' contato: se questo ramo non gira, `_psi_spin_prec` NON avanza e `ritmo()`
            # registra `_ritmo_snap_identico` (Z33). Il sintomo era contato, la causa no.
                        # ✅ MISURATO: **0 salti su 12**, ma in `W3` SCATTA. CLASSE: **(a)** confermata -- la
            # guardia e' raggiungibile, e questa e' la CAUSA di cui `ritmo()` conta il SINTOMO.
            self._g_snap_psispin_tot = getattr(self, "_g_snap_psispin_tot", 0) + 1
            if CAMPO_SPINORIALE and not (hasattr(self, "psi_spin")
                                         and len(getattr(self, "psi_spin", [])) == self.n):
                self._g_snap_psispin_salti = getattr(self, "_g_snap_psispin_salti", 0) + 1
                self._g_snap_psispin_shape = (len(getattr(self, "psi_spin", [])), self.n)
                self._g_snap_psispin_quando = self._g_snap_psispin_tot
            if CAMPO_SPINORIALE and hasattr(self, "psi_spin") and len(getattr(self, "psi_spin", [])) == self.n:
                self._psi_spin_prec = self.psi_spin.copy()   # [FASE 5] snapshot per il ritmo spinoriale (4pi)
            # [CURA DELL'ANELLO ISTANTANEO, 2026-09-18] LA PROMOZIONE del gauge di `ritmo()`, QUI e
            # non dentro `ritmo()`: questo e' l'UNICO call-site FISICO (gli altri due sono
            # diagnostici), quindi solo qui lo snapshot deve avanzare. Sta accanto a `_psi_prec` e
            # `_psi_spin_prec` perche' e' la stessa cosa: uno snapshot CONSUMATO da `ritmo()`, e si
            # promuove DOPO il consumo -- che e' cio' che fa valere A6 (misurato in `680d069`:
            # promuoverlo PRIMA confronterebbe lo stato con se' stesso, `f = 0` per costruzione).
            # ⚠ NON SI PROMUOVE UN `med` CHE STA SUL PAVIMENTO `1e-9`: quel valore non e' una
            # misura, e' la protezione da divisione per zero. Promuoverlo renderebbe la
            # REGOLARIZZAZIONE il gauge del passo dopo -- e la misura dice quanto costerebbe: il
            # rapporto `med_t/med_(t-1)` ha `max = 4.81e+07`, ed e' ESATTAMENTE il passo che segue
            # un gauge degenere (`Z33`). Senza questo ramo la degenerazione non sparirebbe: si
            # ROVESCEREBBE, da "tutti sul pavimento" a "tutti in saturazione". Contato (A8).
            _mu = getattr(self, "_med_f_ultimo", None)
            if _mu is not None:
                if _mu > 1e-9:
                    self._med_f_prec = _mu
                else:
                    self._ritmo_med_non_promosso = getattr(self, "_ritmo_med_non_promosso", 0) + 1
        # [(3) BONIFICA 2026-09-17] `dt_e` e' il tempo proprio dell'ARCO, e serve a `mitosi()`, che
        # non lo riceve fra gli argomenti. Si porta su `self` invece di RICOSTRUIRLO li': una
        # seconda scrittura della stessa legge e' due leggi che possono divergere (e' la ragione
        # per cui `_tempo_luce_nodo` e' un metodo solo). A4: e' tempo PROPRIO, non il tick DT.
        # Scritto in ENTRAMBI i rami dell'orologio, quindi mai stale e mai assente.
        self._dt_e_ultimo = dt_e
        if FORK_SU2_MEM:
            # [FORK SU(2) - STRATO 1] il rilassamento della memoria vive nel TEMPO PROPRIO del nodo
            # (dt_n = DT*r), non nel tic di COORDINATA globale DT: tau = d/cs e' tempo proprio, e
            # mescolare i due frame infilerebbe la foliazione sincrona globale dentro un processo
            # locale (un frame preferito, un "etere"). `r = None` = orologio globale, cioe' r == 1.
            # Scritto solo col flag ON, cosi' la baseline resta byte-identica.
            self._r_corrente = r
        # MOD 5.3a (--tempo-segno): VERSO del tempo dalla MATERIA/ANTIMATERIA COERENTE (Feynman-Stuckelberg).
        # s_k = 1+(perc_chi-1)*m_coer, m_coer = coerenza col campo locale (materia coerente inverte col segno;
        # vuoto incoerente -> +1 avanti). Da stato committato t-1 (perc_chi, phi, Psi). Firma solo #3-6.
        dt_n_s = dt_n
        # [A8, 2026-09-20] (c) RAGIONE SCADUTA sulla parte `len(perc_chi) >= n` (le tre vie la
        # estendono). Il default e' gia' esplicito: `dt_n_s = dt_n` una riga sopra.
                # ✅ MISURATO: **0 salti su 12**, ma in `W3` SCATTA corrompendo `perc_chi`. CLASSE:
        # **(c) DEBOLE** -- raggiungibile da uno stato malformato.
        self._g_temposegno_tot = getattr(self, "_g_temposegno_tot", 0) + 1
        if TEMPO_SEGNO and not (not np.isscalar(dt_n) and len(self.perc_chi) >= self.n
                                and len(self.psi) >= self.n):
            self._g_temposegno_salti = getattr(self, "_g_temposegno_salti", 0) + 1
            self._g_temposegno_shape = (len(self.perc_chi), len(self.psi), self.n)
            self._g_temposegno_quando = self._g_temposegno_tot
        if TEMPO_SEGNO and not np.isscalar(dt_n) and len(self.perc_chi) >= self.n and len(self.psi) >= self.n:
            _mcoer = np.clip(np.cos(self.phi[:self.n] - np.angle(self.psi[:self.n] + 1e-12)), 0.0, 1.0)
            _pc = np.sign(self.perc_chi[:self.n]).astype(float); _pc[_pc == 0] = 1.0
            dt_n_s = (1.0 + (_pc - 1.0) * _mcoer) * dt_n
        w = self._pesi(); self.eta += dt_n
        # In modalita' sincrona tutte le leggi del passo leggono un unico campo
        # calcolato dalla snapshot t. Non ricalcolare psi in punti diversi del
        # passo: quello introdurrebbe letture miste t/t+1.
        A = w * np.cos(self.phi0[i] - self.phi0[j])
        z = np.exp(1j * _phi_t)  # <-- USA LO SNAPSHOT t
        coppia = self._coppia_interferenza(A, z)  # [FASE 3] scalare (off) o overlap spinoriale (on)
        
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
        # li': Ncrit e coerenza sono grandezze di stato, la conversione e' dinamica.
        if REPULS_LEGGE:
            # [Z13 - TEMPO 2, 2026-09-17] `w` PASSATO, non ricalcolato (categoria D: nessun flag).
            # Era `self.calcola_psi()`, che ricalcolava i pesi al proprio interno mentre la riga
            # SOTTO usa `self._mat(w)`, il `w` di questo passo: DUE INSIEMI DI PESI DIVERSI
            # MOLTIPLICATI INSIEME. E' la "lettura mista t/t+1" che il commento a ~:2959 vieta,
            # e stava una riga sopra la sua stessa cura. Il parametro esisteva gia'.
            # ASSIOMA A8: il ramo `w is None` era un fallback silenzioso, preso nel 100 % delle
            # chiamate (misurato: _calcpsi_w_none = 134/134) senza che nulla lo segnalasse.
            psi_forces = self.calcola_psi(w)
            MtPsi = self._mat(w) @ psi_forces
            dHdphi = 2.0 * np.imag(np.conj(z) * MtPsi)   # direzione: de-concentra l'interferenza
            zc = np.exp(1j * _phi_t[:self.n])  # <-- USA SNAPSHOT
            # COERENZA COL NUCLEO (corretta): NON la media vettoriale coi vicini di legame (che il
            # guscio in antifase abbatte, spegnendo la repulsione proprio quando la massa si struttura),
            # ma l'allineamento del nodo con la FASE DEL CAMPO Psi locale - il "battito" della sua
            # massa, dominato dal nucleo costruttivo. Un nodo del nucleo (in fase col campo) resta
            # coerente ~1 anche quando il guscio si forma; il guscio (antifase col campo) da coerenza
            # negativa e NON contribuisce alla repulsione del nucleo. Cosi' la repulsione resta accesa
            # dove la materia si concentra, invece di spegnersi.
            psi_loc = psi_forces[:self.n]
            fase_campo = np.angle(psi_loc + 1e-12)       # fase del campo locale = battito della massa
            coerenza = np.cos(_phi_t[:self.n] - fase_campo)   # +1 nucleo (in fase), -1 guscio (antifase)  # <-- USA SNAPSHOT
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
            # ⚠ [Z13] QUESTO RAMO HA LO STESSO DIFETTO DI ~:3006 (letture miste t/t+1: `calcola_psi`
            # ricalcola i pesi, la riga sotto usa `self._mat(w)`) ED E' STATO LASCIATO COM'E',
            # DELIBERATAMENTE. Non e' codice morto: e' il comportamento ALTERNATIVO di un flag, ed
            # e' escluso da `REPULS_LEGGE = True` (default). Non essendo eseguito, NESSUN SIGILLO
            # PUO' VERIFICARNE LA CORREZIONE: cablarlo darebbe una verifica di FORMA spacciata per
            # una di COMPORTAMENTO (la classe di `VERSO_CHI`, cablato ma muto).
            # ⚠ SE QUALCUNO SPEGNE `REPULS_LEGGE`, IL DIFETTO DELLE LETTURE MISTE TORNA. Chi lo
            # spegne deve saperlo: e' scritto qui e nella voce Z13 del registro.
            # REGOLA GENERALE: un ramo sotto flag non si corregge e non si cancella -- SI DICHIARA,
            # perche' il difetto e' LATENTE, non assente.
            psi_forces = self.calcola_psi()
            MtPsi = self._mat(w) @ psi_forces            # M simmetrica: M^T Psi = M Psi
            dHdphi = 2.0 * np.imag(np.conj(z) * MtPsi)  # d(sum|Psi|^2)/dphi_n
            coppia = coppia + MU_PSI * dHdphi           # (vecchia repulsione a parametro, fallback)

        # FEEDBACK SPINORE -> ARCHI: deve entrare prima dell'integrazione di delta_phivel.
        if SPINORE_VIVO and SPINORE and SPIN_FEEDBACK:
            _fb = self._feedback_spinoriale_archi(i, j, w)
            # [A8/E4] l'AMPIEZZA del contributo rispetto alla coppia che modifica: se fosse
            # trascurabile, l'esperimento sarebbe NULLO -- e va detto, non dedotto dal fatto
            # che "qualcosa e' cambiato".
            _cm = float(np.median(np.abs(coppia))) if np.size(coppia) else 0.0
            _fm = float(np.median(np.abs(_fb))) if np.size(_fb) else 0.0
            # A3c: il rapporto va riportato in forma CONFRONTABILE. Due MASSIMI presi in passi
            # DIVERSI non hanno quoziente, e stamparli accanto a un rapporto massimo invita a
            # dividerli: si accumula quindi la SOMMA dei rapporti per-passo e il loro CONTEGGIO,
            # cosi' il referto puo' dare il rapporto MEDIO -- stesso statistico, stessa popolazione.
            _r = (_fm / _cm) if _cm > 0 else 0.0
            self._sfb_amp_coppia = max(getattr(self, "_sfb_amp_coppia", 0.0), _cm)
            self._sfb_amp_fb = max(getattr(self, "_sfb_amp_fb", 0.0), _fm)
            self._sfb_rapporto_max = max(getattr(self, "_sfb_rapporto_max", 0.0), _r)
            self._sfb_rapporto_som = getattr(self, "_sfb_rapporto_som", 0.0) + _r
            self._sfb_rapporto_n = getattr(self, "_sfb_rapporto_n", 0) + 1
            coppia += _fb
            
        # TERMINE DI HALL / FRAME-DRAGGING come LEGGE (non parametro): il twist, finora solo
        # registrato, chiude il loop e agisce come coppia. La forza NON ha un coefficiente
        # libero: e' il twist locale normalizzato dalla scala critica del sistema
        # (tw/PHI_CRIT, la stessa che definisce il tempo proprio). E' la forza non
        # conservativa (frame-dragging, v x B con B=twist) che devia trasversalmente il moto.
        #
        # ⚠ IL COMMENTO PRECEDENTE DICEVA DUE COSE CHE LA MISURA HA SMENTITO (2026-09-18,
        # `doc/REFERTO_Z24.md`, voce Z27):
        #   - «mediato sugli archi del nodo (la torsione che il nodo SENTE, non la somma che
        #     crescerebbe col grado)» -> quella media era `/ grado[k]`, col grado DEL NODO CHE
        #     RICEVE, ed e' esattamente cio' che ROMPEVA l'antisimmetria. L'accumulo `+twn` a `i`
        #     e `-twn` a `j` E' uno scambio esatto: misurato `|sum|/max|.| = 0.000e+00` SENZA la
        #     divisione, contro **mediana 6.756, MAX 8.483** CON. La divisione era l'INTERA causa.
        #   - «emerge nella scala giusta (~0.2 della coppia principale) senza aggiustamenti»
        #     -> quella scala veniva PROPRIO dalla divisione, cioe' era un aggiustamento, solo
        #     non dichiarato. Il rapporto REALE dopo la cura e' misurato dal sigillo, non asserito.
        # `coppia` finisce in `delta_phivel / M_PH` con `M_PH = 1.0` UNIFORME: qui `sum = 0` non e'
        # una verifica di forma, E' la conservazione di `sum(phivel)`.
        # ⚠ E LA CURA NON RENDE IL TERMINE INTENSIVO: `sum(out) = 0` richiede un denominatore
        # SIMMETRICO SULL'ARCO, l'indipendenza dal grado richiede quello DEL NODO CHE RICEVE, e le
        # due cose NON possono valere insieme (compromesso algebrico, Z27). Si e' scelto `nudo`
        # perche' e' l'unica forma esatta che non richiede NESSUNA scelta (A1, par.3).
        if FRAME_DRAG and len(_tw_t):
            if CHI_CORE and len(self.perc_chi) >= self.n:
                # [CHI_COOP] LA TORSIONE LEGGE LA GEOMETRIA. Le guardie di lunghezza restano su
                # `perc_chi` di proposito: i due array hanno la stessa lunghezza per costruzione
                # (le tre vie di crescita estendono entrambi) e `Z4` lo VERIFICA invece di assumerlo.
                chi_core = (self.chiralita_core_locale(self.perc_geom, geom=True)
                            if CHI_COOP else self.chiralita_core_locale())
                twn = (np.pi * 0.5 * (chi_core[i] - chi_core[j])) / PHI_CRIT
            elif VERSO_CHI and len(self.perc_chi) >= self.n:
                # AGGANCIO AL VERSO STABILE: FRAME_DRAG pilotato dalla circolazione del solo
                # twist_dip CHIRALE (segno fisso, gradiente vecchio/nuovo), NON dal tw pieno che
                # e' dominato da dph=phi[i]-phi[j] (oscilla col battito delle fasi -> inverte il
                # verso). Le chiralita' non battono come le fasi: il verso non si inverte.
                # [CHI_COOP] VERSO_CHI e' il fallback della TORSIONE: segue la geometria.
                _pc_vc = self.perc_geom if CHI_COOP else self.perc_chi
                twn = (np.pi * 0.5 * (_pc_vc[i] - _pc_vc[j])) / PHI_CRIT
            elif not (CHI_CORE and len(self.perc_chi) >= self.n):
                twn = _tw_t / PHI_CRIT                 # twist adimensionale (scala di stato)  # <-- USA SNAPSHOT
            twist_nodo = np.zeros(self.n)
            np.add.at(twist_nodo, i, twn); np.add.at(twist_nodo, j, -twn)  # circolazione orientata
            # [CURA Z27, 2026-09-18] tolta `/ grado[k]`: rompeva l'antisimmetria dello scambio.
            # Il calcolo di `grado` e' stato RIMOSSO perche' diventerebbe codice morto.
            coppia = coppia + twist_nodo[:self.n]
        
        if REGIME == "deterministico":
            # TERMOSTATO NOSE-HOOVER con TEMPERATURA TARGET = LEGGE (dal vuoto di equilibrio P_eq).
            # L'energia cinetica di fase e' <phivel^2>. Il target NON e' un parametro: e' l'energia
            # di punto zero coerente con la densita' di equilibrio del vuoto P_eq = self.d0 (che e'
            # gia' una legge emergente del sistema, insegue la mediana globale di rho). L'attrito xi
            # evolve per riportare l'energia al target: xi>0 frena (energia alta), xi<0 RIFORNISCE
            # (energia bassa) -> il sistema si auto-sostiene invece di spegnersi.
            E_cin = float(np.mean(_phivel_t[:self.n]**2)) if self.n > 0 else 0.0  # <-- USA SNAPSHOT
            # TARGET come legge: energia di punto zero del vuoto di equilibrio. P_eq = mediana di d0
            # (densita' di sfondo); l'energia di fase che quel vuoto sostiene scala con P_eq attraverso
            # la relazione di dispersione (v^2, la rigidita' del mezzo). Nessun numero libero: tutto da
            # grandezze gia' nel sistema (d0, la scala di frequenza mediana del ritmo).
            # [RIPIEGHI-ZERO, 2026-09-29] IL CONFRONTO ERA FRA DUE METRI DIVERSI, e Luca l ha
            #   rilevato: `d0` e' PER ARCO e veniva confrontata con `self.n`, che conta i
            #   NODI. `471564 >= 12802` e' sempre vero, quindi il ramo di scorta NON SCATTA
            #   MAI -- ed era un ripiego solo in apparenza. Ora il confronto e' archi contro
            #   archi, e resta sempre vero: LA CORREZIONE E' BYTE-INERTE.
            # ⚠ E RESTA UN SOSPETTO A SE', REGISTRATO COME `P-EQ-MEDIANA-ARCHI` E NON CURATO
            #   QUI: la FETTA `self.d0[:self.n]` prende la mediana dei PRIMI `n` ARCHI su `m`
            #   (12802 su 471564), cioe' un SOTTOINSIEME ARBITRARIO ordinato per creazione.
            #   Correggerlo CAMBIA IL VALORE di `P_eq`, quindi e' un cambio di fisica: vuole
            #   il suo commit e il suo sigillo.
            # [RIPIEGHI-ZERO, 2026-09-29] LA GUARDIA SULLA LUNGHEZZA E' TOLTA: il CONTROLLO
            #   UNICO garantisce `len(d0) == m` ai due punti del passo, quindi `len(d0) >= len(i)`
            #   era una condizione SEMPRE VERA -- una guardia che non guarda niente (`A9`).
            #   ⚠ `self.n > 0` RESTA, e non e' la stessa cosa: su una rete VUOTA la mediana di un
            #     array vuoto da' `nan`, e con `np.seterr(invalid='raise')` (:8835) SOLLEVA.
            #   ⚠ E LA FETTA NON E' TOCCATA: `self.d0[:self.n]` prende i PRIMI `n` ARCHI su `m`, ed
            #     e' il sospetto `P-EQ-MEDIANA-ARCHI`, IN CODA. Correggerla CAMBIA IL VALORE.
            P_eq = float(np.median(self.d0[:self.n])) if self.n > 0 else 1.0
            # RIGIDITA' DEL MEZZO: con cs-dinamico il mezzo NON e' omogeneo. Il target (grandezza
            # globale, gauge del vuoto) usa la rigidita' rappresentativa = mediana del campo cs locale.
            if CS_DINAMICO:
                _psi_ct = (self.psi if len(self.psi) >= self.n else None)
                cs_rappr = (float(np.median(self._cs_nodo(np.abs(_psi_ct[:self.n]) ** 2, w)))
                            if _psi_ct is not None else CS_M)
            else:
                cs_rappr = CS_M
            T_target = (cs_rappr ** 2) * P_eq          # rigidita' del mezzo (c_s^2, locale se cs-dinamico) * densita' vuoto (P_eq)
            
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
            delta_phivel = dt_n_s * (coppia - self.xi_termo * _phivel_t) / M_PH  # <-- USA SNAPSHOT; dt_n_s = verso firmato (5.3a)
        else:
            delta_phivel = dt_n_s * (coppia - G_PH * _phivel_t) / M_PH           # <-- USA SNAPSHOT; dt_n_s = verso firmato (5.3a)

        # SINCRONIZZAZIONE PESATA SUL TAGLIO ROTAZIONALE (Legge corretta di Kuramoto)
        delta_sync_phi = np.zeros(self.n)
        _forza_sync = _wI_sync = _uno_sync = None   # ingredienti del Kuramoto per il torque SU(2) (--sync-spinore)
        if K_SYNC != 0.0 and self.n > 2:
            # [Z13 - TEMPO 2] `w` PASSATO: stessa ragione di ~:3006, e `w` e' usato poche righe
            # sotto (`wI = self._mat(w)`). Topologia verificata INVARIATA fra il calcolo di `w` e
            # questo punto: 100 % su 40 chiamate (csv/_test_fork, verifica preliminare 1).
            psi_sync = self.calcola_psi(w)
            I2 = np.abs(psi_sync) ** 2
            cmv = (self.pos[:self.n] * I2[:, None]).sum(0) / max(I2.sum(), 1e-9)
            r_cm = np.linalg.norm(self.pos[:self.n] - cmv, axis=1) + LAM * 0.5
            pozzo = I2.sum() / r_cm                       # tempo proprio: pozzo dal centro
            
            wI = self._mat(w)
            uno = np.maximum(wI @ np.ones(self.n), 1e-9)
            media_p = wI @ pozzo / uno
            
            # --- CORRETTO: dispersione e taglio basati su phivel (shear feedback) ---
            pv = self.phivel[:self.n] if len(self.phivel) >= self.n else np.zeros(self.n)
            media_pv = wI @ pv / uno
            disp_shear = np.sqrt(np.maximum(wI @ (pv ** 2) / uno - media_pv ** 2, 0.0))
            
            # NORMALIZZAZIONE LOCALE: il riferimento del pozzo e' la media pesata
            # dei soli vicini topologici (media_p), non pozzo.mean() sull'intero
            # universo. Cosi' la sync confronta ogni nodo con il proprio intorno.
            prof_rel = pozzo / np.maximum(media_p, 1e-9)  # profondita' relativa locale

            # Anche il rinforzo del taglio usa una scala di vicinato: RMS della
            # dispersione dei vicini pesata da wI. Nessuna media globale entra nella
            # legge locale; il valore 1 e' solo il termine di fondo del rinforzo.
            scala_shear_locale = np.sqrt(np.maximum(wI @ (disp_shear ** 2) / uno, 0.0))
            rinforzo_shear = 1.0 + (disp_shear /
                                    np.maximum(scala_shear_locale, 1e-9))
            
            forza = (2.0 / np.pi) * prof_rel * rinforzo_shear
            forza = K_SYNC * forza                        # K_SYNC=1 = legge piena
            if SYNC_SPINORE or SYNC_FASE_OROLOGIO or KURAMOTO_SU2:
                _forza_sync, _wI_sync, _uno_sync = forza, wI, uno   # riuso per il torque SU(2)/segno, snapshot t-1

            zc_sync = wI @ np.exp(1j * _phi_t)            # USA LO SNAPSHOT t
            media = np.angle(zc_sync)
            delta_sync_phi = dt_n_s * forza * np.sin(media - _phi_t)  # <-- USA SNAPSHOT; dt_n_s firmato (5.3a)

        # REINNESTO ETC DEL SETTORE SPINORIALE: evolve _nb leggendo lo snapshot t (self.phi non e'
        # ancora stata committata, quindi calcola_psi() usa _phi_t). Deve stare PRIMA del commit
        # atomico per non leggere le fasi t+1 (sfasamento che l'ETC deve evitare).
        # [A8, 2026-09-20] (c) RAGIONE SCADUTA, E QUESTA E' LA PIU' GRAVE DELLE CINQUE: se
        # fallisse, l'INTERO `_passo_spinoriale` non girerebbe -- il cuore del settore spinoriale,
        # con SPINORE_VIVO acceso nel run. Sarebbe `C11` un'altra volta.
        # NON PUO' FALLIRE: `phi_s` e' esteso da semina (:1882), mitosi (:4176) e Schwinger
        # (:4297), e la RIASSEGNAZIONE di :2719 gli da' lunghezza `n` ESATTA, perche' `nb_new`
        # deriva da `self._nb` che `_passo_spinoriale` normalizza a `n` incondizionatamente.
        # Si conta per DIMOSTRARLO con un numero invece che con un ragionamento.
                # ✅ MISURATO: **0 salti su 12**, ma in `W3` SCATTA corrompendo `phi_s`. CLASSE:
        # **(c) DEBOLE**, ed e' la piu' importante delle deboli: se scattasse davvero, l'INTERO
        # `_passo_spinoriale` non girerebbe. E' protetta da un'invariante, non dalla forma.
        self._g_spinore_vivo_tot = getattr(self, "_g_spinore_vivo_tot", 0) + 1
        if SPINORE_VIVO and SPINORE and self.n > 2 and len(self.phi_s) != self.n:
            self._g_spinore_vivo_salti = getattr(self, "_g_spinore_vivo_salti", 0) + 1
            self._g_spinore_vivo_shape = (len(self.phi_s), self.n)
            self._g_spinore_vivo_quando = self._g_spinore_vivo_tot
        if SPINORE_VIVO and SPINORE and self.n > 2 and len(self.phi_s) == self.n:
            self._passo_spinoriale(i, j, w, dt_n_s, psi_snapshot=None,
                                   forza_sync=_forza_sync, wI_sync=_wI_sync, uno_sync=_uno_sync)

        # --- COMMIT ATOMICO DELLE FASI (Unico punto di scrittura sincrono) ---
        self.phivel = _phivel_t + delta_phivel
        self.phi = (_phi_t + (dt_n_s * self.phivel) + delta_sync_phi) % self._dphi()  # dt_n_s = verso firmato (5.3a)

        # Calcolo della differenza di fase sull'arco basato rigorosamente sullo stato al tempo t
        dph = self._wphi(_phi_t[i] - _phi_t[j])
        if TORS_4PI and len(self.perc_chi) >= self.n:
            # [CHI_COOP] TORS_4PI E' TORSIONE: legge la cache della GEOMETRIA, non quella della
            # carica. Senza la cache separata riceverebbe `_chi_core_nodi`, che con la cooperazione
            # e' scritta dal PASSO SPINORIALE (l'ultimo chiamante nell'ordine di `step()`): avrebbe
            # ricevuto la CARICA in silenzio -- nessun errore, solo l'array sbagliato.
            _cache_tors = '_chi_geom_nodi' if CHI_COOP else '_chi_core_nodi'
            chi_torsione = (getattr(self, _cache_tors) if CHI_CORE and
                            len(getattr(self, _cache_tors, [])) == self.n
                            else ((self.chiralita_core_locale(self.perc_geom, geom=True)
                                   if CHI_COOP else self.chiralita_core_locale()) if CHI_CORE else
                                  (self.perc_geom if CHI_COOP
                                   else self.perc_chi)[:self.n].astype(float)))
            if POLO_MATURO:
                _twabs = np.abs(self.tw)
                _twn = np.zeros(self.n)
                np.add.at(_twn, i, _twabs); np.add.at(_twn, j, _twabs)
                _twn = _twn / np.maximum(self._deg[:self.n] if len(self._deg) >= self.n else 1.0, 1.0)
                _chi_mat = np.where(_twn[i] >= _twn[j], chi_torsione[i], chi_torsione[j])
                twist_dip = np.pi * 0.5 * _chi_mat            # un solo polo (maturo), segno coerente
            else:
                twist_dip = np.pi * 0.5 * (chi_torsione[i] - chi_torsione[j])  # chiralità core o nodale
            _ttw = _tau_tw_locale(self) if TAU_LOCALI else TAU_TW
            self.tw += self._w8(dph + twist_dip - self.twp) - dt_e * self.tw / _ttw
            self.twp = self._w8(dph + twist_dip)
        else:
            _ttw = _tau_tw_locale(self) if TAU_LOCALI else TAU_TW
            self.tw += self._w4(dph - self.twp) - dt_e * self.tw / _ttw
            self.twp = dph
            
        # --- BASCULAMENTO CHIRALE ---
        # [CHI_COOP] `chi_basc` NON SI SPEGNE PIU' quando lo spinore scrive la carica: continua a
        # girare e scrive la GEOMETRIA. I contatori qui sotto sono il criterio di `Z3`: con la
        # cooperazione `chi_basc` non deve toccare `perc_chi` NEMMENO UNA VOLTA.
        if CHI_BASC and (CHI_COOP or not CHI_DA_SPINORE) and len(self.perc_chi) >= self.n and len(self.tw):
            _tw_src = _tw_t  
            twabs = np.abs(_tw_src)
            twn = np.zeros(self.n)
            np.add.at(twn, i, twabs); np.add.at(twn, j, twabs)
            twn = twn / np.maximum(self._deg, 1)          
            soglia = PHI_CRIT   # soglia = QUANTO di olonomia (2pi), locale: +1 solo dove il giro e' completato. NON la mediana globale (imponeva 50/50)
            if CHI_COOP:
                self._g_chibasc_su_geom = getattr(self, "_g_chibasc_su_geom", 0) + 1
                self.perc_geom[:self.n] = np.where(twn > soglia, 1, -1).astype(self.perc_geom.dtype)
            else:
                self._g_chibasc_su_chi = getattr(self, "_g_chibasc_su_chi", 0) + 1
                self.perc_chi[:self.n] = np.where(twn > soglia, 1, -1).astype(self.perc_chi.dtype)

        # --- FLAG 3 (--chi-da-spinore): perc_chi dal SEGNO di doppia-copertura del primario, DOPO
        # il commit di _psi_spinor (regola A/B: mai durante). Confronto col rappresentante canonico
        # del Bloch corrente: +1 = allineato, -1 = ha accumulato il segno -1 di un giro 2pi. CHI_BASC
        # e' gia' disattivato sopra. Richiede --spinore-corretto (garantito in _applica_flag).
        # [A8, 2026-09-20] (c) RAGIONE SCADUTA sulla parte `len(perc_chi) >= n`.
                # ✅ MISURATO: **0 salti su 12**, e in `W3` NON si fa scattare nemmeno corrompendo
        # `perc_chi`. CLASSE: **(c) FORTE** -- non raggiungibile.
        # [CHI_COOP] lo scrittore della CARICA e' lo stesso di FLAG 3: sotto cooperazione gira
        # INSIEME a `chi_basc` invece che al suo posto.
        _chi_da_psi = CHI_DA_SPINORE or CHI_COOP
        self._g_chi_da_spinore_tot = getattr(self, "_g_chi_da_spinore_tot", 0) + 1
        if _chi_da_psi and SPINORE_CORRETTO and not (
                len(self.perc_chi) >= self.n
                and len(getattr(self, "_psi_spinor", [])) >= self.n):
            self._g_chi_da_spinore_salti = getattr(self, "_g_chi_da_spinore_salti", 0) + 1
            self._g_chi_da_spinore_shape = (len(self.perc_chi),
                                            len(getattr(self, "_psi_spinor", [])), self.n)
            self._g_chi_da_spinore_quando = self._g_chi_da_spinore_tot
        if (_chi_da_psi and SPINORE_CORRETTO and len(self.perc_chi) >= self.n
                and len(getattr(self, "_psi_spinor", [])) >= self.n):
            _canon = self._bloch_a_spinore(self._nb[:self.n])
            _ov = np.sum(np.conj(_canon) * self._psi_spinor[:self.n], axis=1)
            self.perc_chi[:self.n] = np.where(np.real(_ov) >= 0.0, 1, -1).astype(self.perc_chi.dtype)
            
        # --- materia: una sola matrice dei pesi, riusata per Psi e diffusione ---
        Mw = self._mat(w)
        # Con --sync la materia viene valutata sullo snapshot t, nello stesso istante
        # delle coppie di fase e del ponte fase->torsione. Senza flag resta il percorso
        # storico: la materia legge la fase appena committata.
        F = Mw @ np.exp(1j * self.phi)
        self.psi = self.satura(F)
        I = np.abs(self.psi) ** 2
        rho = 0.5 * (I[i] + I[j])

        # Velocita' locale delle onde metriche: nel ramo storico cs_arco=CS_M.
        # Nel ramo dinamico la normalizzazione di densita' e' strettamente locale
        # (vicini topologici), mentre il pavimento emerge dalla stessa saturazione
        # razionale del campo: non viene introdotto un numero minimo arbitrario.
        if CS_DINAMICO:
            cs_nodo = self._cs_nodo(I, w)
            if FORK_SU2_MEM or STEP2_OROLOGIO:
                # [FORK SU(2) - STRATO 1] cache per tau = d/cs. La coppia gira PRIMA di questo punto,
                # quindi al passo dopo leggera' il cs di UN PASSO FA: e' un ritardo dentro un
                # meccanismo di ritardo, coerente e innocuo. Scritta solo col flag ON (byte-identita').
                self._cs_nodo_prev = cs_nodo.copy()
            # Collo di bottiglia causale: media armonica, non media aritmetica.
            # [CURA 2] ESTRATTA in `_cs_arco_da_nodo`: la STESSA espressione, un solo posto.
            cs_arco = self._cs_arco_da_nodo(cs_nodo, i, j)
            cs_max_corrente = float(np.max(cs_arco)) if len(cs_arco) else CS_M
        else:
            cs_arco = np.full(len(i), CS_M, dtype=float)
            cs_max_corrente = CS_M

        nuovi = np.isnan(self.peq)
        if nuevos := nuovi.any(): self.peq[nuovi] = rho[nuovi]
        # [PEQ_NASCITA_LOCALE, C2] IL CONTATORE STA QUI, E NON ALTROVE, PERCHE' QUESTO E' L'ISTANTE
        # in cui la legge di nascita si applica. Dopo, il rilassamento di `:4206` muove tutto e la
        # domanda «ha preso la `rho` del PROPRIO arco?» non e' piu' osservabile dall'esterno.
        # ⚠ `_g_peqn_cal` da solo sarebbe TAUTOLOGICO (`peq[nuovi] = rho[nuovi]` e' la riga stessa).
        #   Il numero che CONTA e' `_g_peqn_vs_med`: quanti di quei valori sono DIVERSI dalla
        #   mediana globale, cioe' quante volte la legge locale ha dato un risultato che la legge
        #   globale NON avrebbe dato. Se fossero zero, la cura sarebbe indistinguibile.
        # ⚠ SI CONTANO SOLO GLI ARCHI CHE `C2` HA MARCATO, non tutti i `nan`.
        #   `_allaccia` scrive `nan` pure lei, e **la SEMINA la chiama**: al primo passo di una
        #   scena TUTTI gli archi sono `nan` e vengono calibrati. Contarli insieme dava
        #   `526059` invece di `88`. *(Avevo letto giusto che `_allaccia` e' chiamata solo da
        #   `semina()`, e concluso male che fosse inerte in batch: inerte e' la semina CONTINUA,
        #   non quella INIZIALE.)*
        _idx_n = getattr(self, '_peqn_idx', None)
        if PEQ_NASCITA_LOCALE and nuevos and _idx_n is not None and len(_idx_n):
            _idx_n = _idx_n[_idx_n < len(self.peq)]
            _sel_n = _idx_n[nuovi[_idx_n]]
            if len(_sel_n):
                _vec = np.asarray(self.peq, dtype=float)
                _altri = np.ones(len(_vec), dtype=bool)
                _altri[_sel_n] = False
                _med_g = float(np.median(_vec[_altri])) if np.any(_altri) else 0.0
                _assegn = np.asarray(rho, dtype=float)[_sel_n]
                self._g_peqn_cal = getattr(self, '_g_peqn_cal', 0) + int(len(_sel_n))
                self._g_peqn_vs_med = (getattr(self, '_g_peqn_vs_med', 0)
                                       + int(np.sum(_assegn != _med_g)))
                self._g_peqn_uguali_rho = (getattr(self, '_g_peqn_uguali_rho', 0)
                                           + int(np.sum(_vec[_sel_n] == _assegn)))
                if _med_g > 0:
                    self._g_peqn_scarto_max = max(
                        getattr(self, '_g_peqn_scarto_max', 0.0),
                        float(np.max(np.abs(_assegn - _med_g) / _med_g)))
            self._peqn_idx = None      # consumata: vale per UNA calibrazione sola

        # --- VUOTO DI SFONDO LOCALE, che DIFFONDE sulla topologia (Legge I) ---
        den_w = np.maximum(np.bincount(i, w, minlength=self.n) +
                           np.bincount(j, w, minlength=self.n), 1e-12)
        campo = self.peq if DIFF_RES == 0.0 else (rho - self.peq)
        sp = np.bincount(i, campo, minlength=self.n) + \
             np.bincount(j, campo, minlength=self.n)
        cn = (Mw @ (sp / self._deg)) / den_w
        c_arco = 0.5 * (cn[i] + cn[j])
        flusso = (c_arco - self.peq) if DIFF_RES == 0.0 else ((rho - self.peq) - c_arco)
        
        if TAU_LOCALI:
            _pv_src = _phivel_t  
            r_nodo = np.abs(_pv_src[:self.n]) if len(_pv_src) >= self.n else np.ones(self.n)
            r_arco = 0.5 * (r_nodo[i] + r_nodo[j])
            tau_bg_loc = np.maximum(1.0 / np.maximum(r_arco, 1e-3), 1e-3)   
            if TRACCIA_PEQ: self._traccia_peq(rho, flusso, dt_e, tau_bg_loc, i, j)
            if PEQ_ESATTO:
                self.peq = self._peq_esatto(rho, flusso, dt_e, tau_bg_loc)
            else:
                self.peq += dt_e * ((rho - self.peq) / tau_bg_loc + flusso / TAU_DIFF)
        else:
            if TRACCIA_PEQ: self._traccia_peq(rho, flusso, dt_e, TAU_BG, i, j)
            if PEQ_ESATTO:
                self.peq = self._peq_esatto(rho, flusso, dt_e, TAU_BG)
            else:
                self.peq += dt_e * ((rho - self.peq) / TAU_BG + flusso / TAU_DIFF)
            
        if HAM_SRC == 0.0:
            # Gli archi nuovi non hanno ancora un peq storico: per loro il valore appena
            # inizializzato è il dato di t. Gli altri usano esclusivamente lo snapshot.
            _peq_src = self.peq
            if ANOM_SIMM:
                # [C1-bis] LA FORMA SIMMETRICA. Il denominatore e' `rho + peq`, che con
                #   `rho >= 0` e `peq >= 0` e' `>= 0` e si annulla SOLO quando sono ENTRAMBI
                #   nulli -- e li' `0/0 := 0` e' la DEFINIZIONE giusta, non una toppa.
                _den_s = rho + _peq_src
                anom = np.where(_den_s > 0.0, 2.0 * (rho - _peq_src)
                                / np.where(_den_s > 0.0, _den_s, 1.0), 0.0)
                # ⚠ I DUE CASI SI CONTANO SEPARATI, perche' sono cose DIVERSE:
                #   `_g_as_zero` e' `0/0`, cioe' vuoto su vuoto -- LEGITTIMO;
                #   `_g_as_polo` e' `rho + peq < 0`, che richiede `peq < 0` -- IL POLO, e
                #   puo' capitare SOLO senza `PEQ_ESATTO`. Sommarli nasconderebbe il secondo.
                self._g_as_usi = getattr(self, '_g_as_usi', 0) + 1
                self._g_as_zero = (getattr(self, '_g_as_zero', 0)
                                   + int(np.sum(_den_s == 0.0)))
                self._g_as_polo = (getattr(self, '_g_as_polo', 0)
                                   + int(np.sum(_den_s < 0.0)))
                self._g_as_archi = getattr(self, '_g_as_archi', 0) + int(len(anom))
                if len(anom):
                    self._g_as_max = max(getattr(self, '_g_as_max', 0.0),
                                         float(np.max(np.abs(anom))))
                self._g_as_fuori = (getattr(self, '_g_as_fuori', 0)
                                    + int(np.sum(np.abs(anom) > 2.0 + 1e-12)))
            else:
                anom = (rho - _peq_src) / np.maximum(_peq_src, 1e-9)
            # cs-dinamico: la sorgente in unita' naturali usa la c LOCALE dell'arco.
            cs2_src = (cs_arco ** 2 if CS_DINAMICO else CS_M ** 2)
            src = (ALPHA_M * anom if ALPHA_NAT == 0.0
                   else ALPHA_NAT * (cs2_src / np.maximum(self.d, 1e-6)) * anom)
        else:
            src = -HAM_SRC * K_C * (w / LAM) * np.cos(self.phi0[i] - self.phi0[j]) * np.cos(dph)
            
        if ZETA_M == 0.0:
            beta = BETA_M
        elif ZETA_LOC:
            med_rho = max(float(np.median(rho)), 1e-9)
            eccesso = np.maximum(rho / med_rho - 1.0, 0.0)   
            zeta_loc = ZETA_M / (1.0 + eccesso)              
            beta = 2.0 * zeta_loc * (cs_arco if CS_DINAMICO else CS_M) / np.maximum(self.d, 1e-6)
        else:
            beta = 2.0 * ZETA_M * (cs_arco if CS_DINAMICO else CS_M) / np.maximum(self.d, 1e-6)
            
        # [A8, 2026-09-20] CONTABILITA' DELLA GUARDIA -- byte-inerte: si CONTA, non si cambia.
        # Un ramo che salta in silenzio e' un comportamento SCONOSCIUTO (A8), e questa forma ha
        # gia' prodotto due volte mesi di dati sbagliati: `_cs_nodo_prev` (71.88 %) e
        # `_psi_spin_prec` (95.33 %). Si registrano QUATTRO cose, non una: le invocazioni, i
        # salti, LA FORMA al fallimento (le due lunghezze) e QUANDO -- l'indice dell'ultima
        # invocazione saltata. Il conteggio da solo non distingue un TRANSITORIO delle prime
        # chiamate da un comportamento PRINCIPALE sparso su tutto il run: danno lo stesso numero.
        # `shape` vale -1 al primo posto quando `_sin2_vir` e' None: le DUE cause di fallimento
        # (memoria assente / lunghezza diversa) sono cose diverse e vanno distinte, non sommate.
        self._g_zeta_vir_a_tot = getattr(self, "_g_zeta_vir_a_tot", 0) + 1
        # [RIPIEGHI-ZERO, 2026-09-29] LA CONDIZIONE FUSA E' SEPARATA, come in `lambda_nodi`.
        #   Il commento qui sotto lo diceva gia': <<le DUE cause (memoria assente / lunghezza
        #   diversa) sono cose diverse e vanno distinte, non sommate>> -- e le distingueva NEL
        #   CONTATORE ma NON NEL COMPORTAMENTO: entrambe portavano a <<nessun freno>>.
        #   MISURATO dalla prova a guasto: accorciare `_sin2_vir` faceva sparire il freno
        #   anisotropo PER TUTTA LA RETE, in silenzio -- l'ultimo ripiego silenzioso del sistema.
        #   ORA: `None` resta LEGITTIMO e contato (A1: al primo giro non esiste, e inventare un
        #   valore iniziale sarebbe un numero scelto); LUNGHEZZA SBAGLIATA SOLLEVA.
        if ZETA_VIR and self._sin2_vir is not None and len(self._sin2_vir) != len(beta):
            _ferma_registro(CacheCorta if len(self._sin2_vir) < len(beta) else CacheLunga,
                            "CORTA" if len(self._sin2_vir) < len(beta) else "LUNGA",
                            "_sin2_vir", (len(beta),), _forma_di(self._sin2_vir),
                            "step: freno anisotropo (zeta-vir, ramo A)")
        if ZETA_VIR and self._sin2_vir is not None:
            beta = beta * (1.0 - self._sin2_vir)
        elif ZETA_VIR:
            # [A8/A9, 2026-09-20] IL RAMO CHE PRIMA TACEVA, ORA DICHIARA -- e NON cambia un bit.
            # MISURATO (sigillo 3/3, commit 4edfab2): questo ramo scatta 1 volta su 12 qui e 11 su
            # 55 nel gemello Verlet, e `shape[0] = -1` dice PERCHE': `_sin2_vir` e' None, NON di
            # lunghezza sbagliata. E i salti sono i PRIMI, consecutivi -- dimostrato: 11 indici
            # distinti, tutti >= 1, il massimo vale 11, quindi sono esattamente {1..11}.
            # LA CAUSA E' L'ORDINE, non la lunghezza: `_sin2_vir` lo scrive `memoria_hebbiana_moto`,
            # che nel ciclo gira DOPO `step`. Al primo giro non esiste ancora.
            # PERCHE' NON SI INIZIALIZZA `_sin2_vir`: `0` significa freno PIENO, `1` freno NULLO, e
            # qualunque valore in mezzo e' un NUMERO SCELTO (A1). Non c'e' niente da cui derivarlo:
            # al primo giro `sin2` non esiste PERCHE' NON E' ANCORA STATO CALCOLATO. Inventare un
            # valore iniziale farebbe credere che la legge abbia girato quando non poteva.
            # QUINDI: al primo giro NON C'E' FRENO ANISOTROPO, ed e' corretto che sia cosi'.
            self._g_zeta_vir_a_salti = getattr(self, "_g_zeta_vir_a_salti", 0) + 1
            self._g_zeta_vir_a_shape = (-1 if self._sin2_vir is None else len(self._sin2_vir),
                                        len(beta))
            self._g_zeta_vir_a_quando = self._g_zeta_vir_a_tot
            
        if VERLET:
            n1 = np.ceil(np.abs(src).max() * DT / (0.02 * cs_max_corrente))
            n2 = np.ceil(np.max(beta) * DT / 0.2)
            n3 = np.ceil(np.abs(self.vd).max() * DT / (0.05 * max(np.median(self.d), 0.1) * cs_max_corrente / CS_M))
            nsub = int(max(4, n1, n2, n3))
            if FERMA_DOPO_NSUB:
                self._g_nsub_stop = dict(nsub=int(nsub), n1=float(n1), n2=float(n2),
                                         n3=float(n3), ramo='VERLET')
                raise StopDopoNsub('nsub=%d n1=%.0f n2=%.0f n3=%.0f'
                                   % (nsub, n1, n2, n3))
        else:
            n1 = np.ceil(np.abs(src).max() * DT / (0.05 * cs_max_corrente))
            n2 = np.ceil(np.max(beta) * DT / 0.5)
            n3 = np.ceil(np.abs(self.vd).max() * DT / (0.1 * max(np.median(self.d), 0.1) * cs_max_corrente / CS_M))
            nsub = int(max(1, n1, n2, n3))
            if FERMA_DOPO_NSUB:
                self._g_nsub_stop = dict(nsub=int(nsub), n1=float(n1), n2=float(n2),
                                         n3=float(n3), ramo='EULERO')
                raise StopDopoNsub('nsub=%d n1=%.0f n2=%.0f n3=%.0f'
                                   % (nsub, n1, n2, n3))
        dts = dt_e / nsub
        # [SCALA_MIN_PASSO, C3] la fotografia di `d` PRIMA del ciclo dei sotto-passi.
        # `d` non viene ristrutturato dentro `step()`, quindi qui la lunghezza e' costante e
        # non serve nessuna chirurgia: basta una copia.
        _smp_d_ini = (np.array(self.d, dtype=float, copy=True) if SCALA_MIN_PASSO else None)

        if VERLET:
            # --- VELOCITY-VERLET METRICO (2 ordine) ---
            # src resta valutata al tempo t; beta viene ricalcolata alla configurazione nuova.
            for _ in range(nsub):
                q = self.d - self.d0
                sm = np.bincount(i, q, minlength=self.n) + np.bincount(j, q, minlength=self.n)
                med = sm / self._deg
                lap = 0.5 * (med[i] + med[j]) - q
                acc_t = cs_arco ** 2 * lap + src - beta * self.vd
                if TRACCIA_VD:
                    self._traccia_vd(cs_arco ** 2 * lap, src, -beta * self.vd, beta, cs_arco)
                vd_half = self.vd + 0.5 * dts * acc_t
                # [SCALA_MIN] la regola va sull'INCREMENTO del Verlet, non sul valore finale.
                # [SCALA_MIN_PASSO, C3] dentro il sotto-passo NON si frena e NON c'e' pavimento:
                #   il freno e' UNO SOLO, dopo il ciclo, sulla variazione TOTALE. Cosi'
                #   `nsub` non moltiplica piu' il bias.
                # [(b)1, 2026-09-27] IL PAVIMENTO `0.05` E' ARCHIVIATO in
                #   `csv/_archivio/_pavimenti_morti.py`: era il ramo `else`, e col driver NON
                #   girava mai (0 esecuzioni su 3 passi, copertura di riga con settrace).
                #   LA GARANZIA RESTA `LAM`, che non si tocca. E i rami scendono da TRE a DUE:
                #   il freno di `SCALA_MIN`, e l'aggiornamento nudo che `SCALA_MIN_PASSO`
                #   frena UNA VOLTA a fine passo (`C3`).
                # ⚠ LA PRECEDENZA E' `SCALA_MIN_PASSO` SOPRA `SCALA_MIN`, e va scritta
                #   ESPLICITA: quando c'era il ramo del pavimento questa era la prima
                #   condizione di una catena `if/elif/else`, e collassarla in `if SCALA_MIN`
                #   la ROVESCIA -- con ENTRAMBI i flag accesi si frenerebbe DUE VOLTE, per
                #   scrittura E a fine passo, mentre deve vincere il freno PER PASSO (`C3`).
                #   (Correzione di Luca su `7840039`: l'avevo rovesciata togliendo il pavimento.)
                if SCALA_MIN and not SCALA_MIN_PASSO:
                    d_new = self.d + self._smorza(self.d, dts * vd_half, 'd')
                else:
                    d_new = self.d + dts * vd_half

                q_new = d_new - self.d0
                sm_new = np.bincount(i, q_new, minlength=self.n) + np.bincount(j, q_new, minlength=self.n)
                med_new = sm_new / self._deg
                lap_new = 0.5 * (med_new[i] + med_new[j]) - q_new
                if ZETA_M == 0.0:
                    beta_new = BETA_M
                elif ZETA_LOC:
                    beta_new = 2.0 * zeta_loc * (cs_arco if CS_DINAMICO else CS_M) / np.maximum(d_new, 1e-6)
                else:
                    beta_new = 2.0 * ZETA_M * (cs_arco if CS_DINAMICO else CS_M) / np.maximum(d_new, 1e-6)
                # [A8, 2026-09-20] LA STESSA GUARDIA, DUPLICATA NEL RAMO VERLET. Introdotta il
                # 2026-09-03 da `7946c46` copiandola dal ramo di sopra, senza dichiararne la
                # ragione. Ha il SUO contatore, non quello di sopra: sapere QUALE dei due salta
                # e' il punto, e un contatore condiviso lo nasconderebbe.
                self._g_zeta_vir_b_tot = getattr(self, "_g_zeta_vir_b_tot", 0) + 1
                # [RIPIEGHI-ZERO, 2026-09-29] LA STESSA SEPARAZIONE nel gemello Verlet: stessa
                #   causa, stessa scelta. `None` legittimo e contato, LUNGHEZZA SBAGLIATA SOLLEVA.
                if (ZETA_VIR and self._sin2_vir is not None
                        and len(self._sin2_vir) != len(beta_new)):
                    _ferma_registro(CacheCorta if len(self._sin2_vir) < len(beta_new)
                                    else CacheLunga,
                                    "CORTA" if len(self._sin2_vir) < len(beta_new) else "LUNGA",
                                    "_sin2_vir", (len(beta_new),), _forma_di(self._sin2_vir),
                                    "step: freno anisotropo (zeta-vir, ramo B, gemello Verlet)")
                if ZETA_VIR and self._sin2_vir is not None:
                    beta_new = beta_new * (1.0 - self._sin2_vir)
                elif ZETA_VIR:
                    # [A8/A9, 2026-09-20] LO STESSO RAMO, nel gemello Verlet: stessa causa (ORDINE,
                    # non lunghezza) e stessa scelta (nessun valore iniziale inventato, A1).
                    # Qui scatta 11 volte su 55 perche' il ramo gira a SOTTOPASSI CFL: ~4.6 per
                    # passo. La frazione e' piu' alta, il transitorio e' lo stesso.
                    self._g_zeta_vir_b_salti = getattr(self, "_g_zeta_vir_b_salti", 0) + 1
                    self._g_zeta_vir_b_shape = (-1 if self._sin2_vir is None
                                                else len(self._sin2_vir), len(beta_new))
                    self._g_zeta_vir_b_quando = self._g_zeta_vir_b_tot
                acc_next = cs_arco ** 2 * lap_new + src - beta_new * vd_half
                self.vd = vd_half + 0.5 * dts * acc_next
                self.d = d_new
                beta = beta_new
        else:
            # --- EULERO ESPLICITO (ramo canonico, invariato) ---
            for _ in range(nsub):
                q = self.d - self.d0
                sm = np.bincount(i, q, minlength=self.n) + np.bincount(j, q, minlength=self.n)
                med = sm / self._deg
                lap = 0.5 * (med[i] + med[j]) - q
                self.vd = self.vd + dts * (cs_arco ** 2 * lap + src - beta * self.vd)
                # [(b)1, 2026-09-27] IDEM: il pavimento `0.05` e' archiviato. Questo ramo
                #   era DOPPIAMENTE morto col driver, che passa `--verlet`: Eulero non gira.
                # ⚠ STESSA PRECEDENZA ESPLICITA del ramo Verlet, e per la stessa ragione.
                if SCALA_MIN and not SCALA_MIN_PASSO:
                    self.d = self.d + self._smorza(self.d, dts * self.vd, 'd')
                else:
                    self.d = self.d + dts * self.vd
            
        # [SCALA_MIN_PASSO, C3] IL FRENO SU `d`, UNA VOLTA SOLA, dopo TUTTI i sotto-passi.
        #   Prima girava `nsub` volte -- 22591 in un solo passo al picco del ramo D -- e ogni
        #   applicazione aggiungeva il suo bias. Qui `nsub` non moltiplica piu' niente.
        if SCALA_MIN_PASSO and _smp_d_ini is not None and len(_smp_d_ini) == len(self.d):
            _dxd = np.asarray(self.d, dtype=float) - _smp_d_ini
            self.d = _smp_d_ini + self._smorza(_smp_d_ini, _dxd, 'd_passo')
            self._g_smp_d_chiusure = getattr(self, '_g_smp_d_chiusure', 0) + 1
            self._g_smp_d_nsub = max(getattr(self, '_g_smp_d_nsub', 0), int(nsub))
        if TAU_LOCALI:
            # CORREZIONE DI DIFETTO (par.10, categoria D: nessun flag). ERRORE DI TIPO, non di legge.
            # Era:  d_arco = 0.5 * (self.d[self.i] + self.d[self.j])
            # `d` e `d0` sono PER ARCO (estesi con `dd`, lunghezze d'arco, riga ~1853), mentre
            # `self.i`/`self.j` sono indici di NODO: si indicizzava un array per-arco con indici di
            # nodo. Shape giusta (len(i) = n_archi), VALORI sbagliati: leggeva solo i primi `n`
            # elementi (98.34 % degli archi mai letto) e produceva una grandezza ANTICORRELATA
            # (r = -0.349) con la lunghezza vera dell'arco che pretendeva di rappresentare.
            # `d` E' GIA' la lunghezza dell'arco: nessuna media serve.
            # ASSIOMA A3, forma "popolazione": un rapporto ha senso solo se numeratore e
            # denominatore vivono sulla STESSA popolazione. Zero parametri coinvolti.
            # Il codice SA distinguere: a riga ~2350 usa `self.d` NUDO accanto a `ramp[self.i]`
            # per nodo, nella stessa espressione. Qui non lo faceva.
            # Sigillo: csv/_seal_fork/_sigillo_d_arco.py
            if TAU_USA_D0:
                d_arco = self.d0
            else:
                d_arco = self.d

            # A8 (2026-09-17): questo ramo ha un FALLBACK PERICOLOSO -- `np.ones(self.n)`, cioe'
            # densita' 1 al posto di |psi|^2, che vale ~1e-6. Se scattasse, `rho_arco` salirebbe di
            # sei ordini e `t_visco` con lui. Non era contato: ora lo e'.
            _I_ok = hasattr(self, "psi") and len(self.psi) >= self.n
            if not _I_ok:
                self._taup_Inodi_fallback = getattr(self, "_taup_Inodi_fallback", 0) + 1
            self._taup_Inodi_chiamate = getattr(self, "_taup_Inodi_chiamate", 0) + 1
            I_nodi = np.abs(self.psi[:self.n])**2 if _I_ok else np.ones(self.n)
            rho_arco = 0.5 * (I_nodi[self.i] + I_nodi[self.j])

            # PLASTICITA' VISCOELASTICA CAUSALE (par.10, categoria D: nessun flag).
            # Era:  fattore_elasticita = 1.0 + ELAST_C * max(rho_arco/median(I_nodi) - 1, 0)
            #       tau_p_loc          = (d_arco / cs) * fattore_elasticita
            # TRE DIFETTI IN UNA RIGA, tutti misurati (doc/REFERTO_gate_bonifica.md):
            #  - ELAST_C = 100 e' un numero SCELTO ("default storico"): A1 violato;
            #  - median(I_nodi) e' una statistica GLOBALE su un percorso fisico: A2 violato
            #    (Legge I, :265);
            #  - ed e' un ERRORE DI POPOLAZIONE (A3): rho_arco vive sugli ARCHI, median(I_nodi)
            #    sui NODI. Su coda pesante l'arco tipico sta MOLTO sopra la mediana nodale
            #    (rapporto mediano misurato: 8830), quindi il fattore aveva mediana ~8.8e5:
            #    la plasticita' non era "spenta a meta'", era CONGELATA quasi ovunque.
            # LA FORMA NUOVA dice una cosa fisica: il rilassamento plastico e' IL PIU' LENTO fra
            # il tempo-luce dell'arco e il suo tempo viscoelastico. Nel denso il mezzo si comporta
            # da solido (ricorda la forma), nel rarefatto da fluido (la dimentica).
            # `peq` e' il vuoto di sfondo LOCALE, per ARCO (A2 soddisfatto), e vive sulla STESSA
            # popolazione di rho_arco (A3 soddisfatto). Zero parametri: d, cs, rho, peq sono tutti
            # di stato (A1).
            # IL `max` NON E' UN PAVIMENTO TARATO (A1/A3b): sotto t_luce la forma di riposo
            # inseguirebbe la forma attuale PIU' IN FRETTA di quanto un segnale attraversi l'arco,
            # cioe' violerebbe A5. Non e' un valore scelto fra molti: e' l'unico possibile, perche'
            # oltre c'e' una violazione. E' la legge che dichiara il proprio dominio.
            # Sigillo: csv/_seal_fork/_sigillo_taup_causale.py  (V2-V5)
            cs_taup = (cs_arco if CS_DINAMICO else CS_M)
            # A8: il clamp 1e-9 su cs e' un ramo silenzioso. CONTATO.
            self._taup_cs_clamp = getattr(self, "_taup_cs_clamp", 0) + int(np.sum(np.asarray(cs_taup) < 1e-9))
            self._taup_cs_clamp_tot = getattr(self, "_taup_cs_clamp_tot", 0) + int(np.size(cs_taup))
            t_luce = d_arco / np.maximum(cs_taup, 1e-9)                       # tempo-luce dell'arco
            _peq_ok = np.isfinite(self.peq) & (self.peq > 1e-30)
            if not bool(np.all(_peq_ok)):
                # P5: ogni protezione su un percorso fisico va CONTATA, non solo messa.
                self._taup_peq_degenere = getattr(self, "_taup_peq_degenere", 0) + int((~_peq_ok).sum())
                # ...e in QUANTI PASSI DISTINTI scatta. Il contatore cumulativo da solo non
                # distingue "un difetto sempre presente" da "un transitorio di accensione
                # moltiplicato per il numero di archi": sono diagnosi opposte, e senza questo
                # secondo contatore si sceglie quella che si ha in mente. (2026-09-17)
                self._taup_peq_deg_passi = getattr(self, "_taup_peq_deg_passi", 0) + 1
                self._taup_peq_deg_ultimo = getattr(self, "_passo_corrente", -1)
            _peq = np.where(_peq_ok, self.peq, 1e-30)
            t_visco = t_luce * (rho_arco / _peq)                              # tempo viscoelastico
            tau_p_loc = np.maximum(t_luce, t_visco)                           # IL PIU' LENTO DEI DUE
            # quante volte e' il VINCOLO CAUSALE a decidere, e non la viscoelasticita' (A3b: un
            # limite che scatta quasi sempre non e' un limite, e' il comportamento principale).
            _scatta = t_visco < t_luce
            self._taup_causale_scatti = getattr(self, "_taup_causale_scatti", 0) + int(_scatta.sum())
            self._taup_causale_tot = getattr(self, "_taup_causale_tot", 0) + int(len(tau_p_loc))
            # E l'INTERSEZIONE: quanti degli scatti causali stanno su archi dove `peq` era gia'
            # degenere. Se coincidessero, il vincolo causale non starebbe descrivendo il vuoto
            # profondo, starebbe descrivendo il punto in cui `peq` smette di essere definito --
            # due cose diverse, che si distinguono solo contandole (P5).
            self._taup_causale_su_degenere = (getattr(self, "_taup_causale_su_degenere", 0)
                                              + int((_scatta & ~_peq_ok).sum()))
            # PRESIDIO DI STABILITA', permanente: il rilassamento d0 += dt_e*(d-d0)/tau_p e' un
            # Eulero esplicito, e DIVERGE OSCILLANDO se dt_e/tau_p >= 1. Prima della bonifica il
            # massimo misurato valeva 34629 sullo 0.11 % degli archi (csv/_seal_fork/
            # _u7_separazione_scale.txt). Non basta che non produca NaN: va GUARDATO.
            if len(tau_p_loc):
                _cfl = float(np.max(dt_e / tau_p_loc)) if np.ndim(dt_e) else float(dt_e / tau_p_loc.min())
                self._taup_cfl_max = max(getattr(self, "_taup_cfl_max", 0.0), _cfl)
            if TRACCIA_D0: _tr_pre = self.d0.copy()
            self.d0 += self._sd0(dt_e * (self.d - self.d0) / tau_p_loc)
            if TRACCIA_D0: self._traccia_d0('S02_rilass_visco', _tr_pre)
            if GUSCIO_MORBIDO:
                # DIFFUSIONE DI SUPERFICIE: lap(d0) ~0 nel nucleo uniforme, grande al bordo ripido ->
                # smussa SOLO il guscio. D = c_locale * spaziatura (lunghezza^2/tempo), nessun coeff.
                # nuovo; clamp causale CFL: |delta d0| <= cs*dt_e (cammino delle onde in un passo).
                _sm0 = np.bincount(self.i, self.d0, minlength=self.n) + np.bincount(self.j, self.d0, minlength=self.n)
                _med0 = _sm0 / np.maximum(self._deg, 1)
                _lap_d0 = 0.5 * (_med0[self.i] + _med0[self.j]) - self.d0
                _cfl = cs_taup * dt_e
                if TRACCIA_D0: _tr_pre = self.d0.copy()
                self.d0 += self._sd0(np.clip(dt_e * cs_taup * d_arco * _lap_d0, -_cfl, _cfl))
                if TRACCIA_D0: self._traccia_d0('S03_diff_guscio', _tr_pre)
        else:
            if TRACCIA_D0: _tr_pre = self.d0.copy()
            self.d0 += self._sd0(dt_e * (self.d - self.d0) / TAU_P)
            if TRACCIA_D0: self._traccia_d0('S04_rilass_TAU_P', _tr_pre)
            
        if TRACCIA_D0: _tr_pre = self.d0.copy()
        if TRACCIA_D0: self._traccia_d0('P1_dopo_rilass', _tr_pre)
        
    def decidi_divisione(self):
        """**CHI DECIDE quali archi si dividono — SEPARATO da chi esegue.**

        *(`COMMIT 2` del riordino della mitosi, 2026-10-01. ### **BYTE-IDENTICO: zero bit.**)*

        ### Perche' esiste: `mitosi` intrecciava decisione ed esecuzione per ~280 righe
        ### **E percio' <<chi decide>> non si poteva nemmeno LEGGERE.** Ora la decisione e' una
        funzione che si legge dall'inizio alla fine, e l'esecuzione un'altra.

        ### ⛔ **E NON <<LEGGE E NON SCRIVE NIENTE>>, come il piano prometteva: lo DICHIARO.**
        Il piano *(`doc/PIANO_riordino_mitosi.md`, parte (a))* diceva
        *«`decidi_divisione(net)` ### legge e NON SCRIVE NIENTE»*. ### **Non e' realizzabile senza
        cambiare la fisica**, e queste sono le tre scritture che restano **dentro** — ciascuna col
        suo motivo:

        | la scrittura | perche' NON puo' uscire |
        |---|---|
        | ### **l'estrazione casuale** `self.rng.random(len(avv))` | il generatore ### **avanza**: spostarla cambia ### **l'ORDINE delle estrazioni**, e il run non sarebbe piu' byte-identico. *(E' esattamente cio' che il **commit 3** deve dichiarare.)* |
        | ### **`self._rep`** *(la memoria di repulsione)* | e' una grandezza ### **di STATO col suo rilassamento esatto** `_rep + (rep − _rep)·exp(−dt/tau)`: ### **e' la MEMORIA della decisione**, non un effetto dell'esecuzione |
        | ### **i contatori** *(`_tum_*`, `_rep_*`, `_g_m2l_*`, `negate`)* | contano ### **cio' che la decisione ha fatto** (`A8`). Spostarli li farebbe contare un'altra cosa |

        ### ➜ **Quindi la promessa onesta non e' «non scrive»: e' «NON TOCCA LA FISICA DEI NODI E
        ### DEGLI ARCHI».** Non crea, non distrugge, non muove `phi`, `d`, `d0`, `pos`, `tw`.
        ### **Dichiararla pura sarebbe stato FALSO**, e un sigillo su una promessa falsa non prova
        niente.

        ### Che cosa restituisce
        `(sel, perche)` — ### **`sel`** sono gli indici degli archi che si dividono;
        ### **`perche`** e' il *«perche'»* chiesto dal piano, e ### **l'esecuzione ne usa UNA
        chiave, `I`** *(la densita' sorgente)*: ### **misurato, non supposto** — lo strumento di
        patch ha **verificato** che l'esecuzione non legge nessun altro locale della decisione.
        Le altre chiavi ci sono ### **per essere LETTE** *(il criterio, non il suo esito)*, e il
        loro essere inutilizzate e' ### **dichiarato qui invece di essere scoperto dopo.**

        ### ⛔ **Soglia e `0.3` INVARIATI**, come decide il piano: la soglia ### **E' `D36`**, e
        toccarla ### **cambia la fisica** *(acclarato per misura: con `phi` su `2π` gli archi sopra
        soglia passano da **7047 a ZERO**)*. ### **Questo commit non la tocca.**
        """
        # [MAX-NODI-FERMA, 2026-09-28] `self.n >= MAX_NODI` TOLTO da questa guardia. Era:
        #     if self.n >= MAX_NODI or not len(self.tw): return 0
        #   `return 0` significa ZERO NASCITE, e il run continuava come se la fisica avesse
        #   deciso di non far nascere niente: la guardia di MEMORIA diventava una LEGGE. Ora
        #   ferma lo schedulatore. `not len(self.tw)` RESTA: quella e' una rete senza archi,
        #   cioe' <<non c'e' niente da dividere>>, e non ha nulla a che vedere con la memoria.
        # ⚠ IL `perche'` SI RESTITUISCE ANCHE QUANDO NON NASCE NIENTE, ed e' il punto del
        #   commit: una decisione LEGGIBILE deve essere leggibile SOPRATTUTTO quando dice NO.
        #   Qui non c'e' ancora niente da dire: la rete non ha archi.
        if not len(self.tw): return None, {}
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
        # [FASE_2PI] Con `phi` su 2pi un arco porta una differenza fino a `pi`, e il
        # quanto che fa dividere l'arco e' `2pi`: il `2pi + pi` cade, e con esso la sua
        # derivazione a posteriori. E' il punto PIU' INCERTO della cura, e lo decide `E1`.
        if TORS_4PI and not FASE_2PI:
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
        # [A8, 2026-09-20] CONTABILITA' DELLA GUARDIA -- byte-inerte: si CONTA, non si cambia.
        # Un ramo che salta in silenzio e' un comportamento SCONOSCIUTO (A8), e questa forma ha
        # gia' prodotto due volte mesi di dati sbagliati: `_cs_nodo_prev` (71.88 %) e
        # `_psi_spin_prec` (95.33 %). Si registrano QUATTRO cose, non una: le invocazioni, i
        # salti, LA FORMA al fallimento (le due lunghezze) e QUANDO -- l'indice dell'ultima
        # invocazione saltata. Il conteggio da solo non distingue un TRANSITORIO delle prime
        # chiamate da un comportamento PRINCIPALE sparso su tutto il run: danno lo stesso numero.
        self._g_tors4pi_tot = getattr(self, "_g_tors4pi_tot", 0) + 1
        # [A8/A9, 2026-09-20] IL RAMO ALTERNATIVO, DICHIARATO. Se le lunghezze non combaciano la
        # soglia di mitosi NON viene modulata dal gradiente di tempo proprio: resta `soglia0`
        # su tutti gli archi, cioe' la soglia non modulata. NON e' un errore -- ma era silenzioso.
        # MISURATO: 0 salti su 12 invocazioni (sigillo 3/3, 4edfab2). Si dichiara lo stesso.
        # ⚠ `if` negato e non `else` per la stessa ragione di `_pesi`: il corpo del ramo buono e'
        # lungo, e il ramo alternativo va scritto ACCANTO alla guardia, dove si legge.
        if TORS_4PI and len(self.i) != len(avv):
            self._g_tors4pi_salti = getattr(self, "_g_tors4pi_salti", 0) + 1
            self._g_tors4pi_shape = (len(self.i), len(avv))
            self._g_tors4pi_quando = self._g_tors4pi_tot
        if TORS_4PI and len(self.i) == len(avv):
            # gradiente di tempo proprio LUNGO l'arco: differenza del tempo proprio nodale
            # fra i due estremi. tau_nodo alto = tempo lento = materia. Dove il gradiente
            # e' forte, la soglia si abbassa (la mitosi e' agevolata verso il tempo lento).
            # [CURA 2 STRUTTURALE, 2026-09-27] IL RAMO `if TEMPO_UNICO_MITOSI:` E' STATO TOLTO: la legge e' SEMPRE questa.
            #   Il ramo `else` e' ARCHIVIATO in `csv/_archivio/rami_off_cura2.py` e si rilancia dal tag `pre-cura2-strutturale`.
            # [CURA 2] IL GRADIENTE DI TEMPO SI PRENDE DALL'OROLOGIO, non da `|tw|`.
            # Il commento qui sopra dice "gradiente di TEMPO PROPRIO", ma `tau_nodo` e'
            # `1 + mean(|tw|)/PHI_CRIT`, cioe' ESATTAMENTE la formula del ramo
            # `TEMPO_SEGNO` di `ritmo()` -- CHE NON GIRA (`TEMPO_SEGNO = False` in 9 run
            # su 11, `Z130`). Intenzione TEMPO, implementazione TORSIONE.
            # SI PRENDE `r` E NON `1/r`, e la ragione e' un conto, non una preferenza:
            #   r    in [1.4142e-6, 1.4142]  -> tanh(grad) <= 0.8884 -> la soglia MODULA
            #   1/r  in [0.707, 707107]      -> tanh(grad) -> 1 ESATTO -> la modulazione
            #                                   diventerebbe un RISCALAMENTO COSTANTE
            #                                   della soglia, cioe' un PARAMETRO NASCOSTO
            #                                   (`A1`), e `A11` cor.6 dice che un limite
            #                                   che satura e' un allarme.
            _rn = self._r_nodo_mitosi()
            # `grad_modula` qui e' il gradiente di `r`: IL TEMPO PROPRIO VERO.
            grad_modula = np.abs(_rn[self.i] - _rn[self.j])
            # modulazione limitata: la soglia scende di al piu' ~30% dove il gradiente e' forte
            soglia = soglia0 * (1.0 - 0.3 * np.tanh(grad_modula))
        # CRITICITA' NON MONOTONA (campana) ancorata ai due valori fisici del sistema:
        # massima alla SOGLIA LOCALE (soglia critica emergente, pilotata da `grad_modula`: il gradiente di
        # `r` a flag acceso, della torsione a flag spento -- `D32`), e si SPEGNE al tetto 4pi. Tra i due, la
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
        # [D32, 2026-09-27] NON E' UN TEMPO PROPRIO: e' una POSIZIONE sull'asse della
        #   torsione, un numero puro `1 + avv/PHI_CRIT`. Il tempo proprio del sistema e'
        #   `r` (e `dt_e` sull'arco); `d/cs` e' il TEMPO-LUCE, un'altra grandezza.
        #   Decisione di Luca, 2026-09-27. Il nome vecchio era `tau_pp`.
        pos_soglia = 1.0 + soglia / PHI_CRIT              # la stessa POSIZIONE, alla soglia
        pos_tetto = 1.0 + TW_TETTO / PHI_CRIT             # la stessa POSIZIONE, al tetto 4pi
        # transizione di segno a META' fra soglia e tetto: crea da soglia in giu', respinge
        # da meta'-cammino-al-tetto in su. Centrata sul punto medio (soglia+tetto)/2.
        centro = 0.5 * (pos_soglia + pos_tetto)
        pos_torsione = 1.0 + avv / PHI_CRIT
        segno = -np.tanh(3.0 * (pos_torsione - centro))
        # [CURA 2] LA CAMPANA SI LEGGE DUE VOLTE, E CIASCUNA LETTURA HA LE SUE UNITA'.
        #   `rep` e' il BERSAGLIO di un rilassamento, cioe' un EQUILIBRIO: **non puo'
        #   dipendere dalla DURATA del passo**, senno' la stessa condizione fisica darebbe un
        #   equilibrio diverso a seconda di quanto batte l'orologio locale.
        #   `prob` e' una probabilita' NEL PASSO, cioe' un CONTEGGIO: **DEVE dipenderne**.
        #   Quindi il fattore di tempo entra UNA volta sola, e solo nel secondo.
        # [CURA 2 STRUTTURALE, 2026-09-27] IL RAMO `if TEMPO_UNICO_MITOSI:` E' STATO TOLTO: la legge e' SEMPRE questa.
        #   Il ramo `else` e' ARCHIVIATO in `csv/_archivio/rami_off_cura2.py` e si rilancia dal tag `pre-cura2-strutturale`.
        _ft = self._fattore_tempo_arco(len(avv))       # dt_e/DT: il tempo d'arco, LETTO
        ampiezza_int = salita * discesa                # INTENSITA': numero puro, SENZA tempo
        ampiezza = ampiezza_int * _ft                  # EVENTI ATTESI nel passo proprio
        resp_int = ampiezza_int * segno                # -> il BERSAGLIO `rep`
        resp = ampiezza * segno                            # FIRMATA: + crea, - respinge
        # --- CREAZIONE: dove resp > 0, mitosi probabilistica (come prima) ---
        # [A8] QUANTE VOLTE IL CLIP AVREBBE MORSO. Byte-inerte: si CONTA, non si cambia --
        # e gira ANCHE a flag spento, cosi' il "prima" del confronto arriva dal giro di
        # byte-inerzia del sigillo, senza un run in piu'.
        self._tum_clip_prob_tot = getattr(self, "_tum_clip_prob_tot", 0) + int(np.size(resp))
        self._tum_clip_prob = (getattr(self, "_tum_clip_prob", 0)
                               + int(np.sum(np.asarray(resp) > 1.0)))
        # [A8, richiesta di Luca 2026-09-24] IL CLIP HA DUE LATI, E FINORA NE CONTAVO UNO SOLO.
        # `np.clip(resp, 0, 1)` taglia in ALTO (contato sopra: ZERO su 63'148'047) **e in BASSO**.
        # Il lato basso morde ogni volta che `resp <= 0`, cioe' su TUTTO il regime repulsivo, e
        # dire "il clip non morde" senza questo numero sarebbe FALSO.
        # NB: la forma di Poisson `1 - exp(-max(resp, 0))` conserva il taglio in basso -- e' il
        # taglio in ALTO che sparisce. Questo contatore dice quanto grande sia il pezzo di
        # dominio su cui le due forme COINCIDONO ESATTAMENTE (entrambe danno 0).
        self._tum_clip0_prob = (getattr(self, "_tum_clip0_prob", 0)
                                + int(np.sum(np.asarray(resp) <= 0.0)))
        # [CURA 2 STRUTTURALE, 2026-09-27] IL RAMO `if TEMPO_UNICO_MITOSI:` E' STATO TOLTO: la legge e' SEMPRE questa.
        #   Il ramo `else` e' ARCHIVIATO in `csv/_archivio/rami_off_cura2.py` e si rilancia dal tag `pre-cura2-strutturale`.
        # LA FORMA DI POISSON: `resp` e' il NUMERO ATTESO di eventi nel passo proprio, e
        # la probabilita' di ALMENO UNO e' `1 - e^-lambda`. Sta in [0, 1) PER COSTRUZIONE:
        # il clip non ha piu' niente da tagliare (`A11`). Per lambda piccolo coincide con
        # la forma vecchia: l'errore relativo e' lambda/2.
        prob = 1.0 - np.exp(-np.maximum(resp, 0.0))
        nasce = self.rng.random(len(avv)) < prob
        # --- REPULSIONE: dove resp < 0, il tempo proprio estremo respinge: allarga d0
        # localmente (pressione a corto raggio), invece di creare nodi. E' il confine
        # attivo dei nuclei super-densi: la materia compressa respinge invece di collassare.
        # [CURA 2] il BERSAGLIO usa `resp_int`, cioe' la campana SENZA il fattore di tempo.
        # ⚠ IL CLIP RESTA, e la sua sostituzione con `tanh` e' una DECISIONE DI LUCA dopo una
        #   MISURA: `satura(f) -> 1/GAMMA = 20`, quindi il clip a 1 E' RAGGIUNGIBILE. Le due
        #   forme coincidono DOVE IL CLIP NON MORDE, e il contatore qui sotto dice quanto.
        _resp_rep = resp if resp_int is None else resp_int
        self._tum_clip_rep_tot = getattr(self, "_tum_clip_rep_tot", 0) + int(np.size(_resp_rep))
        self._tum_clip_rep = (getattr(self, "_tum_clip_rep", 0)
                              + int(np.sum(-np.asarray(_resp_rep) > 1.0)))
        rep = np.clip(-_resp_rep, 0.0, 1.0)

        # ---- CORREZIONE (3) del 2026-09-17: MEMORIA DELLA REPULSIONE (par.10 categoria D) ----
        # ASSIOMA A7: "una grandezza senza stato non puo' conservare nulla". `rep` era ISTANTANEO e
        # `d0 += spinta` e' IRREVERSIBILE: un processo che AGGIUNGE senza TOGLIERE e senza memoria
        # e' un CRICCHETTO, e il rumore vi si integra in crescita monotona. Non c'era modo di
        # tornare indietro, nemmeno quando la condizione che aveva prodotto la spinta spariva.
        # LA CURA: `_rep` diventa uno STATO PER ARCO che rilassa verso il `rep` istantaneo con
        # tempo d'arco `dt_e` -- NON `pos_torsione`, che non e' un tempo (`D32`).
        # ASSIOMA A5, livello 1 (rilassamento esponenziale): lecito perche' `dt_e` e' un tempo
        # locale dello stesso arco. ZERO PARAMETRI: `dt_e` esiste gia'.
        # Il contributo ORA PUO' ANCHE DECRESCERE: il cricchetto e' chiuso.
        # NB su cosa questo NON fa: `d0` resta cumulativa. Chiudere il cricchetto significa che
        # l'INGRESSO puo' calare, non che d0 possa tornare indietro da sola. La previsione scritta
        # prima del cablaggio (doc/PREVISIONI_qualitative.md par.5) dice esattamente questo.
        # A8: il `getattr(..., DT)` cade sul tick di COORDINATA se lo snapshot non esiste --
        # esattamente il difetto che par.9 chiama "DT nudo dentro un processo locale". CONTATO.
        if not hasattr(self, "_dt_e_ultimo"):
            self._rep_dte_assente = getattr(self, "_rep_dte_assente", 0) + 1
        _dte = getattr(self, "_dt_e_ultimo", DT)
        if np.ndim(_dte) and len(np.asarray(_dte)) != len(rep):
            # P5: allineamento mancante -> si conta e si cade sul tick di coordinata.
            self._rep_dte_fallback = getattr(self, "_rep_dte_fallback", 0) + 1
            _dte = DT
        if len(self._rep) != len(rep):
            # P5: se lo stato non e' allineato agli archi, si riparte da zero e SI CONTA.
            self._rep_realloc = getattr(self, "_rep_realloc", 0) + 1
            self._rep = np.zeros(len(rep))
        # A8: il clamp 1e-12 su `pos_torsione` e' un ramo silenzioso. CONTATO.
        # ⚠ IL NOME DEL CONTATORE NON SI RINOMINA: e' un REPERTO, sta nei `json` gia'
        #   scritti (`CLAUDE.md` par.9). E a flag ACCESO conta un clamp che NON GIRA:
        #   vive nel ramo `else`. In coda come `D32-CONTATORE`, non qui.
        self._rep_taupp_clamp = getattr(self, "_rep_taupp_clamp", 0) + int(np.sum(np.asarray(pos_torsione) < 1e-12))
        self._rep_taupp_tot = getattr(self, "_rep_taupp_tot", 0) + int(np.size(pos_torsione))
        # [CURA 2 STRUTTURALE, 2026-09-27] IL RAMO `if TEMPO_UNICO_MITOSI:` E' STATO TOLTO: la legge e' SEMPRE questa.
        #   Il ramo `else` e' ARCHIVIATO in `csv/_archivio/rami_off_cura2.py` e si rilancia dal tag `pre-cura2-strutturale`.
        # [CURA 2 + S12] TRE difetti nella riga vecchia, e il commento ne dichiarava due:
        #   (1) LA DILATAZIONE ERA CONTATA DUE VOLTE: `_dte` E' GIA' `DT*0.5*(r_i+r_j)`,
        #       e dividere ANCHE per `pos_torsione` la conta di nuovo;
        #   (2) `pos_torsione` NON E' UNA DURATA: e' un numero puro (`D32`). Una costante di tempo deve
        #       avere le unita' di un tempo -- e `tau_arco = d/cs_arco` le ha: [DT];
        #   (3) L'INTEGRATORE ERA UN EULERO ESPLICITO, mentre il commento dichiara
        #       "`A5` livello 1, rilassamento ESPONENZIALE" e par.4 impone la forma ESATTA.
        # La forma esatta e' una COMBINAZIONE CONVESSA: `_rep` resta fra `rep` e il suo
        # valore precedente PER QUALUNQUE PASSO, quindi il difetto che l'Eulero aveva su
        # `peq` (`dt/tau = 1.2018`, scavalcava sotto zero) NON PUO' RIPRESENTARSI.
        _tau_a = self._tau_arco_causale(len(rep))
        _rap = np.asarray(_dte, dtype=float) / _tau_a
        # [A8] quante volte l'Eulero AVREBBE scavalcato (`dt/tau > 1`): misura quanto
        # serviva `S12`. Byte-inerte: si conta e basta.
        self._tum_eulero_gt1 = (getattr(self, "_tum_eulero_gt1", 0)
                                + int(np.sum(_rap > 1.0)))
        self._tum_eulero_tot = getattr(self, "_tum_eulero_tot", 0) + int(np.size(_rap))
        self._rep = rep + (self._rep - rep) * np.exp(-_rap)
        _rep_mem = self._rep
        # quanto la memoria si discosta dall'istantaneo: se fosse ~0 la cura sarebbe inerte.
        if len(rep):
            self._rep_scarto_max = max(getattr(self, "_rep_scarto_max", 0.0),
                                       float(np.max(np.abs(_rep_mem - rep))))

        # P5 (mandato (3)): questa guardia e' un FALLBACK NON CONTATO. Quando fallisce, l'INTERO
        # blocco repulsivo non gira affatto - e un ramo mai misurato e' un comportamento
        # sconosciuto. Si conta PRIMA di appoggiarci sopra qualsiasi cosa.
        self._rep_guardia_tot = getattr(self, "_rep_guardia_tot", 0) + 1
        if len(self.d0) != len(avv):
            self._rep_guardia_salti = getattr(self, "_rep_guardia_salti", 0) + 1
            self._rep_guardia_shape = (len(self.d0), len(avv))
        if _rep_mem.any() and len(self.d0) == len(avv):
            # CORREZIONE (2) del 2026-09-17 (par.10 categoria D: nessun flag).
            # Era:  spinta = 0.02 * np.median(self.d0) * rep
            # `median(self.d0)` e' una STATISTICA GLOBALE dentro un termine che si dichiara
            # "Locale pura" nella riga sotto: A2 violato (Legge I, :265), e A3 - normalizzare
            # sulla mediana del proprio insieme fissa il centro a 1 per identita'.
            # CONSEGUENZA CONCRETA: ogni arco riceveva LA STESSA lunghezza di spinta,
            # indipendentemente dalla propria scala. Ora la spinta e' proporzionale alla scala
            # LOCALE dell'arco: un arco corto ne riceve poca, uno lungo molta.
            # ⚠ A1 RESTA VIOLATO, E VA DETTO: il `0.02` e' un numero SCELTO ("limitata (2% per
            # passo)"), non derivato. Questa correzione toglie A2 e A3, NON A1. Registrato fra i
            # fronti aperti invece di essere risolto in silenzio con un numero diverso.
            spinta = 0.02 * self.d0 * _rep_mem
            if TRACCIA_D0: _tr_pre = self.d0.copy()
            self.d0 = self.d0 + self._sd0(spinta)          # Locale pura
            if TRACCIA_D0: self._traccia_d0('S05_spinta_locale', _tr_pre)
            if TRACCIA_D0: _tr_pre = self.d0.copy()
            #   portare d0 sotto la scala minima, o lo stress |d-d0|/d0 diverge (bug rientrante)
            if TRACCIA_D0: self._traccia_d0('P2_dopo_spinta', _tr_pre)
        c = np.where(nasce)[0]
        if not len(c):
            # nessun candidato: il criterio C'E' TUTTO, e si consegna.
            return None, {"avv": avv, "soglia": soglia, "prob": prob, "nasce": nasce,
                          "resp": resp, "segno": segno}
        c = c if MITMAX == 0 else c[np.argsort(avv[c])[::-1]][:MITMAX]
        I = self._rho_sorgente()   # [FASE 5] soglia mitosi su densita' SPINORIALE (rho_spin ON / |psi|^2 OFF); limite identico
        a, b = self.i[c], self.j[c]
        ok = 0.5 * (I[a] + I[b]) >= QMIN_M * float(np.median(self.peq))
        # [CURA 5] `A13` ALLA NASCITA: un arco si divide SOLO se `d_arco >= 2 LAM`.
        #   Il figlio nasce a `d/2` dai genitori, quindi `d/2 >= LAM` <=> `d >= 2 LAM`.
        #   LA CONDIZIONE VA **QUI**, accanto alla soglia di densita': e' lo STESSO punto dove il
        #   codice decide «questo candidato si divide o no». **NON in `nasce`** (la' si decide una
        #   PROBABILITA', e `A13` non e' una probabilita'), **NON in `_nasce`** (la' si RIPARA, e
        #   la cura e' proprio togliere la riparazione).
        self._g_m2l_tot = getattr(self, "_g_m2l_tot", 0) + int(np.size(c))
        # ### IL CANCELLO E' INCONDIZIONATO DAL COMMIT `6b`: `A13` ALLA NASCITA E' LEGGE.
        #   ### **Non c'e' piu' un `if MITOSI_2LAM`**: il comportamento <<senza il flag>>
        #   e' ### **uscito dal sorgente** e sta in `csv/_archivio/_rami_off_cura2.py`,
        #   e il flag resta ### **INERTE come `PAV_COM`** (decisione 3 di Luca: si
        #   conserva tutto), dichiarato fra i `[flag-inerti]`.
        #   ### ⛔ **E IL CONTO DELLE LEGGI VA IN DIMINUZIONE** (`9-ter`): prima c'erano
        #   ### **DUE comportamenti** (col flag e senza), ora ce n'e' ### **UNO**.
        #   ### ✅ **E TOGLIE UNA VIOLAZIONE DI `A14`:** senza il cancello gli archi
        #   sotto `LAM` nascono comunque e ### **`_nasce` li ALZA** -- cioe' modifica una
        #   lunghezza DOPO averla creata, che e' una ### **proiezione** e viola `A14`
        #   ### **per costruzione, qualunque sia il valore.** ### **Un cancello non
        #   modifica lo stato: RIFIUTA un evento.** Non e' un taglio, e' un
        #   ### **NON-ACCADIMENTO**.
        #   ### ⚠ **E NON LA TOGLIE DOVE NON GUARDA:** lo Schwinger continua a produrre
        #   archi sotto `LAM` -- e' `SCHW-SOTTO-LAM`, registrata e NON curata qui.
        if len(c):
            _dc = np.asarray(self.d, float)[c]
            # ### I DUE TRONCONI, ENTRAMBI: il figlio nasce a `FRAZ_NASCITA * d` da
            #   `a` e a `(1 - FRAZ_NASCITA) * d` da `b`, quindi ### **servono DUE
            #   disuguaglianze e non una.** A `t = 0.5` coincidono, e la congiunzione
            #   si riduce a `0.5*d >= LAM` -- che e' `d >= 2*LAM` ### **al bit**,
            #   perche' moltiplicare per `0.5` e per `2.0` e' ### **esatto in
            #   IEEE-754** (potenze di due: la mantissa non cambia). ### **Per questo
            #   il braccio `A` del sigillo e' IDENTICO AL BYTE con il flag acceso.**
            _sx = FRAZ_NASCITA * _dc >= LAM
            _dx = (1.0 - FRAZ_NASCITA) * _dc >= LAM
            _conforme = _sx & _dx
            # ### I RIFIUTI SEPARATI PER CANCELLO, e serve: `negate` li MESCOLA, quindi
            #   un rifiuto per densita' e uno per `LAM` erano ### **indistinguibili**.
            #   ### **Tre contatori, e la somma dei tre e' il totale dei rifiutati.**
            _no_dens = ~ok
            _no_lam = ~_conforme
            self._g_m2l_rif_solo_dens = getattr(self, "_g_m2l_rif_solo_dens", 0) + int(np.sum(_no_dens & ~_no_lam))
            self._g_m2l_rif_solo_lam = getattr(self, "_g_m2l_rif_solo_lam", 0) + int(np.sum(~_no_dens & _no_lam))
            self._g_m2l_rif_entrambi = getattr(self, "_g_m2l_rif_entrambi", 0) + int(np.sum(_no_dens & _no_lam))
            # ### `|tw|` DEGLI ARCHI RIFIUTATI PER `LAM`: una DIAGNOSTICA per il `6c`,
            #   non una legge. ### Si tiene la LISTA e non la somma, perche' il mandato
            #   chiede la ### **MEDIANA** -- e una mediana non si ricostruisce da una
            #   somma. ### ⚠ Cresce, ma i rifiuti sono pochi (2 per scena nella misura
            #   del guardiano), e ### **non entra in nessun calcolo di fisica.**
            if np.any(_no_lam):
                _tws = np.abs(np.asarray(self.tw, float)[c][_no_lam])
                self._g_m2l_tw_rif = (getattr(self, "_g_m2l_tw_rif", []) + [float(x) for x in _tws])
            self._g_m2l_negati = getattr(self, "_g_m2l_negati", 0) + int(np.sum(~_conforme))
            self._g_m2l_dmin = min(getattr(self, "_g_m2l_dmin", float("inf")),
                                   float(_dc.min()) if _dc.size else float("inf"))
            ok = ok & _conforme
        self.negate += int((~ok).sum()); sel = c[ok]
        if not len(sel):
            # candidati c'erano, ma nessuno ammesso: si consegna ANCHE il filtro.
            return None, {"avv": avv, "soglia": soglia, "prob": prob, "nasce": nasce,
                          "resp": resp, "segno": segno, "I": I, "candidati": c,
                          "ammessi": ok}
        # ### IL <<PERCHE'>> CHIESTO DAL PIANO. `I` e' l'unica chiave che l'esecuzione legge
        #   (verificato dallo strumento di patch); le altre ci sono PER ESSERE LETTE.
        return sel, {"I": I, "avv": avv, "soglia": soglia, "prob": prob, "nasce": nasce,
                     "resp": resp, "segno": segno, "candidati": c, "ammessi": ok}

    def mitosi(self):
        """**CHI ESEGUE la divisione** — la decisione sta in `decidi_divisione`.

        *(`COMMIT 3` del riordino, 2026-10-02: ### **LA NASCITA COME EVENTO UNICO.**
        Byte-identico, zero bit.)*

        ### Le quattro fasi, e l'ordine fra loro e' il punto
        | | |
        |---|---|
        | **1 PREPARAZIONE** | si calcola **tutto** cio' che serve: i genitori, `fm`, `keep`, `dh`, `d0new`. ### **Nessuna scrittura della nascita** |
        | **2 IL CALCIO** | ai **genitori**, cioe' a nodi che ### **esistono gia'**: non e' una nascita |
        | ### **3 LA NASCITA** | ### **`nascita(self, evento, c)`** — e **quello e' l'unico posto** che scrive le grandezze del registro |
        | **4 I CONTATORI** | i nati, i derivati (`_grado`), gli allineamenti — ### **dopo**, e dichiarati |

        ### ⚠ **PRIMA ERANO TRE I POSTI CHE SCRIVEVANO**: `mitosi`, i due `_eredita_*`,
        piu' la crescita per **MUTAZIONE** di `conc_nodi` *(`.append`, che l'AST non vede)*.
        ### **Ora e' UNO.** I due `_eredita_*` sono **ASSORBITI** — il riordino non li butta,
        e la ragione per cui esistevano *(le cure `C7`/`C11`/`PSI-FLASH`)* vive nelle
        `derivazione` delle loro regole.

        ### 📌 **E L'ORDINE DELLE SCRITTURE E' L'ORDINE DEL REGISTRO, MISURATO**
        `csv/_test_fork/_ordine_registro.py`: ### **4 vincoli genuini, 0 violazioni.**
        `phi` prima di `twp` · `peq` prima di `_peqn_idx` · `n0` nel **contesto** ·
        le **6 chiamate con effetto** collocate a mano. *(Vedi il blocco di
        `REGOLE_NASCITA` in testa al file.)*
        """
        sel, perche = self.decidi_divisione()
        if sel is None:
            return 0
        # =====================================================================
        # ### 1. PREPARAZIONE -- nessuna scrittura della nascita, qui.
        # =====================================================================
        # [PEQ-MEDIANA-ISTANTE, 2026-10-02, decisione di Luca -- via (b) passo 2]
        #   `_g_peqn_mediana` e' il DIAGNOSTICO <<cio' che si EVITA>>: la mediana GLOBALE
        #   di `peq` che `PEQ_NASCITA_LOCALE` esiste per NON usare.
        #   ### L'ISTANTE E' DICHIARATO: LO STATO DA CUI LA NASCITA DEL PASSO PARTE.
        #   Non e' una scelta di comodo, ed e' l'unico istante NON AMBIGUO: <<dopo la
        #   nascita completa>> dipenderebbe da QUALI RAMI sono scattati dentro `mitosi`
        #   (Schwinger si'/no, quanti archi), quindi due passi darebbero mediane prese su
        #   stati diversi PER RAGIONI DIVERSE.
        #   ### IL COSTO, MISURATO e non stimato: `np.median` su 471564 float costa
        #   `0.0053 s`, cioe' lo `0.187 %` di un passo da `2.849 s`. Il gate e' CHEAP
        #   (due booleani e una lunghezza), quindi la mediana si paga solo nei passi in
        #   cui una divisione c'e' davvero.
        _peqn_med_pre = (float(np.median(self.peq))
                         if (COPPIA_MIT > 0.0 and PEQ_NASCITA_LOCALE and len(sel))
                         else float("nan"))
        # ### L'UNICA chiave che l'esecuzione legge, e il patch l'ha VERIFICATO.
        I = perche["I"]
        a, b = self.i[sel], self.j[sel]; m = self.n + np.arange(len(sel))
        D = self._wphi(self.phi[a] - self.phi[b])
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
            # ### IL `bias` E' UNO SCOSTAMENTO *SOPRA* `FRAZ_NASCITA`, e il suo `0.5` di
            #   AMPIEZZA (la riga qui sopra) ### **NON si tocca**: sono due `0.5` con
            #   ### **due ruoli diversi** sulla stessa legge, e distinguerli e' il punto.
            fm = (self.phi[a] - (FRAZ_NASCITA + bias) * D) % self._dphi()
        else:
            fm = (self.phi[a] - FRAZ_NASCITA * D) % self._dphi()
        # ### LA FORMA CONVESSA, E NON LA LERP: `(1-t)*x + t*y` e' ### **identica al bit** a
        #   `0.5*(x+y)` a `t = 0.5` *(0 differenze su 2 000 000)*, mentre `x + t*(y-x)`
        #   ### **NO** *(576 135 su 2 000 000)*. ### Misurato prima di scrivere.
        pos_figlio = (1.0 - FRAZ_NASCITA) * self.pos[a] + FRAZ_NASCITA * self.pos[b]
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
            # [FASE_2PI] L'ANTIFASE E' META' DEL DOMINIO: `+pi` su 2pi, `+2pi` su 4pi.
            _mezzo = self._dphi() / 2.0
            fm = np.where(flip, (fm + _mezzo) % self._dphi(), fm)
            self.ultima_frac_antifase = float(flip.mean()) if len(flip) else 0.0
        # =====================================================================
        # ### 2. IL CALCIO AI GENITORI -- e NON e' una nascita.
        # =====================================================================
        # ⚠ STA PRIMA DELLA NASCITA, e l'ordine conta: `twp` (vincolo 1 del contratto)
        #   legge `phi[a]`/`phi[b]` GIA' CALCIATI, mentre `fm` qui sopra li ha letti
        #   PRIMA. Due istanti dello stesso passo, e il commit 3 li PRESERVA: la
        #   domanda di fisica e' registrata su `DIVISIONE-AUTOCONSISTENTE`.
        sciolta = np.abs(self.tw[sel]) / PHI_CRIT
        g = np.concatenate([a, b])
        if REGIME == "deterministico":
            # ### REGIME DETERMINISTICO -- IL RAMO CHE GIRA (il commento diceva <<WIP>>, e lo
            # diceva del ramo su cui girano TUTTI i sigilli). Impulso modulato dal TEMPO PROPRIO LOCALE tau =
            # 1+|tw|/PHI_CRIT. Componente comune diretta da tau (rompe la simmetria attorno alla
            # materia, non si media a zero) + parte chirale antisimmetrica. Saturazione tau/(1+tau)
            # = termostato (auto-freno dove tau alto). Vedi note REGIME in testa al file.
            tau_a = 1.0 + np.abs(self.tw[sel]) / PHI_CRIT
            mod = tau_a / (1.0 + tau_a)
            chi_a = self.perc_chi[a]; chi_b = self.perc_chi[b]
            comune = KICK_TW * sciolta * (mod - 0.5)
            calcio_a = comune + 0.5 * KICK_TW * sciolta * chi_a * mod
            calcio_b = comune - 0.5 * KICK_TW * sciolta * chi_b * mod
            self.phi[a] = (self.phi[a] + calcio_a) % self._dphi()
            self.phi[b] = (self.phi[b] + calcio_b) % self._dphi()
        else:
            # ### REGIME STOCASTICO -- RAMO CHE NON GIRA MAI, e il commento diceva l'opposto:
            # <<canonico, validato ... DEFAULT>>. ### E' FALSO SU TUTTI E TRE I PUNTI: il default
            # e' "deterministico" (dal 2026-08-28), nessuno strumento seleziona lo stocastico, e
            # ### NESSUN SIGILLO COPRE QUESTO RAMO. <<validato>> si riferisce all'EPOCA 1.
            # ⚠ E QUI IL CONFRONTO CON IL RAMO SOPRA DICE UNA COSA DI FISICA: il deterministico
            #   ha un'autointerazione (la torsione dell'arco decide la forza del calcio, la
            #   chiralita' il verso), questo ha un RINCULO CASUALE. Vedi
            #   `DIVISIONE-AUTOCONSISTENTE`.
            # rinculo di fase casuale:
            self.phi[g] = (self.phi[g] + self.rng.normal(0, 1, len(g)) *
                           KICK_TW * np.concatenate([sciolta, sciolta])) % self._dphi()
        # =====================================================================
        # ### 1-bis. PREPARAZIONE degli archi: `keep`, `dh`, `d0new`.
        # =====================================================================
        keep = np.ones(len(self.i), bool); keep[sel] = False
        # ### `dh` SI SDOPPIA, e l'ordine e' quello di `i = [keep, a, m]`: ### **il
        #   PRIMO blocco e' `a`-`m` e vale `t * d`**, il secondo e' `m`-`b` e vale
        #   `(1-t) * d`. ### A `t = 0.5` i due blocchi sono IDENTICI, ed e' per questo che
        #   oggi una sola `dh` bastava per entrambi.
        dh_a = FRAZ_NASCITA * self.d[sel]
        dh_b = (1.0 - FRAZ_NASCITA) * self.d[sel]
        # lunghezza di riposo dei due nuovi archi. Di default meta' dell'arco (dh):
        # e' questo dimezzamento che produce la compressione degenere, perche' la
        # geometria di equilibrio si accorcia a ogni suddivisione.
        # Con PLAST_MIT>0: offset plastico PERMANENTE proporzionale alla torsione
        # sciolta, cosicche' la suddivisione registri nel mezzo una generazione di
        # struttura metrica invece di un puro infittimento. Modifica lo stato
        # stazionario dell'arco (d0), non un impulso transitorio su vd.
        if PLAST_DIN:
            # Plasticita' emergente: stress metrico dell'arco * eccesso di torsione, saturato.
            stress_arco = np.abs(self.d[sel] - self.d0[sel]) / np.maximum(self.d0[sel], 1e-6)
            sciolta_ecc = np.abs(self.tw[sel]) / PHI_CRIT - 1.0
            fattore_plastico = np.tanh(np.maximum(sciolta_ecc * stress_arco, 0.0))
            # ### `d0new` DERIVA DAI DUE MEZZI, con lo STESSO ordine, e resta calcolato
            #   dai valori ### **PRIMA** della chiamata a `_nasce` su `dh` -- come oggi.
            d0new = np.concatenate([dh_a * (1.0 + fattore_plastico),
                                    dh_b * (1.0 + fattore_plastico)])
        elif PLAST_MIT > 0.0:
            d0new = np.concatenate([dh_a * (1.0 + PLAST_MIT * sciolta),
                                    dh_b * (1.0 + PLAST_MIT * sciolta)])
        else:
            d0new = np.concatenate([dh_a, dh_b])
        # ### `md=1, md0=0` E NON `2, 0`: `dh` e' ora GIA' l'array dei due blocchi, quindi
        #   ogni voce e' ### **un arco vero** e non due. ### ⛔ **E la chiamata resta UNA,
        #   di proposito:** `_g_sm_nascite` conta le INVOCAZIONI, e spezzarla in due lo
        #   farebbe salire di 2 invece di 1. ### `meta` dice dove finisce il primo blocco,
        #   cosi' `_fab` si calcola PER META' e `_sm_lun` resta identico al bit.
        dh = np.concatenate([dh_a, dh_b])
        dh = self._nasce(dh, 'mitosi', 1, 0, meta=len(dh_a))   # [SCALA_MIN] i due tronconi
        # `md=0, md0=1`: `d0new` e' GIA' `concatenate([d0h, d0h])`, cioe' i due figli.
        d0new = self._nasce(d0new, 'mitosi', 0, 1)
        # ### CHIAMATA CON EFFETTO 1 di 3, DICHIARATA (`_nascita_collocata`): la chirurgia
        #   sullo snapshot. Legge SOLO `keep` e `d0new`, non `d`/`d0`, quindi la sua
        #   posizione rispetto al blocco e' libera -- e sta qui, nella preparazione,
        #   perche' non e' una regola di nascita.
        if TRACCIA_D0: _tr_pre = self.d0.copy()
        self._smp_chirurgia(keep=keep, nuovi=d0new)   # [C3] lo snapshot segue la mitosi
        # =====================================================================
        # ### 3. LA NASCITA -- IL PUNTO UNICO, evento `divisione`.
        # =====================================================================
        # ⚠ `n0` STA NEL CONTESTO ed e' il vincolo 3 del contratto: prima i due
        #   `_eredita_*` calcolavano `n0 = self.n - k` DOPO che `phi` era cresciuto,
        #   cioe' leggevano una `@property` su `len(self.phi)` A META' DELLA NASCITA.
        #   Qui `n0` e' catturato PRIMA, nella preparazione, e le regole non leggono
        #   `self.n`: stesso valore, dipendenza TOLTA.
        c = {"sel": sel, "a": a, "b": b, "m": m, "keep": keep,
             "fm": fm, "pos_figlio": pos_figlio, "dh": dh, "d0new": d0new,
             "quante": len(sel), "n0": self.n,
             # i genitori nella forma che i due `_eredita_*` usavano: `np.asarray(.., int)`
             "src": np.asarray(a, int), "src_a": np.asarray(a, int),
             "src_b": np.asarray(b, int), "segno": 1,
             # le due guardie d'ingresso dei `_eredita_*`: `k == 0` e `n0 <= 0`
             "eredita_vale": bool(len(sel) and self.n > 0),
             "spinore_vale": bool(SPINORE_CORRETTO or CAMPO_SPINORIALE)}
        nascita(self, "divisione", c)
        # ### CHIAMATA CON EFFETTO 2 di 3: la traccia di `d0`, che confronta il
        #   PRIMA (catturato nella preparazione) col DOPO. Sta SUBITO dopo il
        #   blocco, che e' il punto piu' vicino a dove stava -- dentro il blocco
        #   non puo' stare, perche' il blocco e' il PUNTO UNICO. `TRACCIA_D0`
        #   e' SPENTO in ogni run e in ogni sigillo: misurato, non assunto.
        if TRACCIA_D0: self._traccia_d0('S06_mitosi', _tr_pre)
        # =====================================================================
        # ### 4. I CONTATORI E I DERIVATI -- dopo, e dichiarati.
        # =====================================================================
        # [A8/A7, 2026-09-20] I NATI PER RAMO, byte-inerti. QUESTO ramo eredita la chiralita'
        # UGUALE al genitore, quindi AGGIUNGE un nodo del suo stesso segno e ROMPE la
        # conservazione di `N(+1) - N(-1)`. L'altro ramo (Schwinger, antinodo) nasce OPPOSTO e la
        # conserva. Un contatore TOTALE dei nati non distingue le due cose, ed e' esattamente il
        # numero che non serve: per sapere da dove viene la carica servono DUE conteggi.
        self._g_nati_mitosi = getattr(self, "_g_nati_mitosi", 0) + int(len(a))
        self._g_nati_mitosi_ev = getattr(self, "_g_nati_mitosi_ev", 0) + 1
        # TRACKING: riallineo conc_archi. Archi mantenuti (keep) conservano la concorrenza; i nuovi
        # (a-m, m-b) nascono senza concorrenza (ripopolabile da aggiorna_pesi_concorrenza).
        # ⚠ NON e' nel registro, quindi NON e' una regola di nascita: e' un riallineamento
        #   per ARCO, dichiarato qui.
        if self.conc_archi:
            keep_idx = np.where(keep)[0]
            self.conc_archi = ([self.conc_archi[e] if e < len(self.conc_archi) else []
                                for e in keep_idx] + [[] for _ in range(2 * len(a))])
        # ### CHIAMATA CON EFFETTO 3 di 3: `_grado()` scrive `_deg` ed e' una DERIVATA
        #   della topologia -- legge `i`, `j` e `len(phi)`, quindi DOPO il blocco.
        self._grado(); self.nati += len(sel)
        # EMISSIONE DI COPPIA: per una frazione degli eventi nasce un anti-nodo a
        # fase fm+pi, collegato ai due genitori a-b. La coppia (nodo fm + anti-nodo
        # fm+pi) ha media fm, quindi conserva l'olonomia globale, ma introduce due
        # difetti opposti. L'anti-nodo e' collocato sul punto medio come il nodo,
        # cosi' i due nascono sovrapposti e la dinamica (antifase -> repulsione) li
        # separa da se'. NON si impone alcuna forza: solo la fase opposta.
        # [MAX-NODI-FERMA, 2026-09-28] `and self.n < MAX_NODI` TOLTO. Era:
        #     if COPPIA_MIT > 0.0 and self.n < MAX_NODI:
        #   Spegneva il CANALE DI SCHWINGER in silenzio: l'emissione di coppia sparisce e dai
        #   dati sembra che la fisica non la produca. Ora ferma lo schedulatore.
        if COPPIA_MIT > 0.0:
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
                I = self._rho_sorgente()   # [FASE 5] densita' coppia su campo SPINORIALE (rho_spin ON / |psi|^2 OFF); limite identico
                rho_sel = 0.5 * (I[a] + I[b])                   # densita' d'interferenza sull'arco
                # ⚠ `PEQ-SEL-STANTIO`: questa lettura arriva DOPO che la nascita ha
                #   riscritto `peq` con `[keep], [sel], [sel]`, quindi `sel` indicizza
                #   ARCHI DIVERSI. ### IL DIFETTO E' REGISTRATO E NON CURATO QUI: il
                #   commit 3 preserva il comportamento dei rami, anche di quelli spenti,
                #   e `COPPIA_DENSITA` e' spento (`:1714`).
                peq_sel = self.peq[sel]
                peq_sel = np.where(np.isnan(peq_sel), rho_sel, peq_sel)
                anom = np.maximum(0.0, (rho_sel - peq_sel) / np.maximum(peq_sel, 1e-6))
                eccesso_totale = eccesso_torsione + anom
            else:
                eccesso_totale = eccesso_torsione
            prob_coppia = 1.0 - np.exp(-COPPIA_MIT * eccesso_totale)
            # ⚠ `.mean()` su float DIPENDE DALL'ORDINE da 3 elementi in su (misurato,
            #   IEEE-754: l'addizione e' commutativa ma NON associativa). Nella finestra
            #   misurata `len(sel)` sta in {1, 2}, quindi oggi e' INERTE con margine 1 --
            #   e il commit 3 non cambia l'ordine degli archi di `sel`.
            self.ultima_prob_coppia = float(prob_coppia.mean()) if len(prob_coppia) else 0.0
            estratto = self.rng.random(len(sel)) < prob_coppia
            if estratto.any():
                # =============================================================
                # ### 1-ter. PREPARAZIONE dell'evento `schwinger`.
                # =============================================================
                pick = np.where(estratto)[0]
                aa, bb = a[pick], b[pick]
                # [FASE_2PI, D35] L'ANTIFASE E' META' DEL DOMINIO. Con `phi` su 4pi il
                # `+2pi` NON e' un'antifase: il campo legge `exp(i phi)` e
                # `exp(i(phi+2pi)) = exp(i phi)`, cioe' l'antiparticella e' IDENTICA
                # alla particella. Con `phi` su 2pi diventa `+pi`, che lo e' davvero.
                anti = (fm[pick] + self._dphi() / 2.0) % self._dphi()
                nc = len(pick)   # fase opposta (fm+pi)
                k = self.n + np.arange(nc)
                # ### `md=1, md0=1` E NON `2, 2`: `dd` e' ora GIA' i due blocchi, quindi
                #   `concatenate([d, dd])` E `concatenate([d0, dd])` -- e `meta` fa
                #   calcolare `_fab` PER META'.
                # ⚠ QUARTO SITO, non nei tre del rilievo: e' `x2` su ENTRAMBE le grandezze.
                # ⚠ E la lunghezza viene da `pos`, non da `d`: e' la voce `A3` della coda.
                # ### `dd` SI SDOPPIA, e l'ordine e' quello di `i = [.., aa, k]`: il
                #   PRIMO blocco e' `aa`-`k` e vale `max(t*L, 0.05)`, il secondo e' `k`-`bb`
                #   e vale `max((1-t)*L, 0.05)`. ### ⚠ **Il pavimento `0.05` resta
                #   com'e': e' un `A11` e NON e' del `6a`.**
                #   ### ⚠ **E LA LUNGHEZZA VIENE DA `pos`, NON DA `d`** -- nella
                #   divisione viene da `d`. ### **E' `SCHW-CORTI`, e il `6a` la DICHIARA
                #   senza cambiarla.**
                _L_sch = np.linalg.norm(self.pos[aa] - self.pos[bb], axis=1)
                _dd_a = np.maximum(FRAZ_NASCITA * _L_sch, 0.05)
                _dd_b = np.maximum((1.0 - FRAZ_NASCITA) * _L_sch, 0.05)
                dd = self._nasce(np.concatenate([_dd_a, _dd_b]),
                                 'schwinger', 1, 1, meta=len(_dd_a))
                # [PEQ_NASCITA_LOCALE, C2] `nan` = «da calibrare sulla `rho` del PROPRIO
                # arco», ed e' la STESSA convenzione di `_allaccia`: `:4189` lo fa
                # all'inizio del passo dopo, e da' `anom = 0` ESATTO alla nascita.
                # Il ramo storico prende `median(self.peq)`, una statistica GLOBALE (`A2`).
                pmed = np.nan if PEQ_NASCITA_LOCALE else float(np.median(self.peq))
                if PEQ_NASCITA_LOCALE:
                    self._g_peqn_archi = getattr(self, '_g_peqn_archi', 0) + int(2 * nc)
                    self._g_peqn_ev = getattr(self, '_g_peqn_ev', 0) + 1
                    # [PEQ-MEDIANA-ISTANTE] ### NON `np.median(self.peq)` QUI: il valore
                    #   e' quello CATTURATO IN TESTA a `mitosi`, sullo stato da cui la
                    #   nascita parte.
                    self._g_peqn_mediana = _peqn_med_pre   # cio' che si EVITA (PRE-nascita)
                # ### CHIAMATA CON EFFETTO, DICHIARATA: lo snapshot segue anche lo
                #   Schwinger, e qui SENZA `keep` (la coppia aggiunge archi, non ne toglie).
                if TRACCIA_D0: _tr_pre = self.d0.copy()
                # ### UNA VOLTA SOLA: `dd` e' GIA' i due blocchi. Con
                #   `concatenate([dd, dd])` lo snapshot crescerebbe del DOPPIO, e il
                #   presidio `RIPIEGHI-ZERO` ferma il run -- lo ha fatto davvero.
                self._smp_chirurgia(nuovi=dd)   # [C3] Schwinger
                # =============================================================
                # ### 3-bis. LA NASCITA -- IL PUNTO UNICO, evento `schwinger`.
                # =============================================================
                c2 = {"aa": aa, "bb": bb, "k": k, "nc": nc, "anti": anti,
                      "dd": dd, "pmed": pmed, "quante": nc, "n0": self.n,
                      "src": np.asarray(aa, int), "src_a": np.asarray(aa, int),
                      "src_b": np.asarray(bb, int), "segno": -1,
                      "eredita_vale": bool(nc and self.n > 0),
                      "spinore_vale": bool(SPINORE_CORRETTO or CAMPO_SPINORIALE)}
                nascita(self, "schwinger", c2)
                # =============================================================
                # ### 4-bis. I CONTATORI E I DERIVATI dello Schwinger.
                # =============================================================
                # [A8/A7, 2026-09-20] L'ALTRO RAMO: l'antinodo nasce OPPOSTO al genitore, quindi la
                # coppia e' NEUTRA e `N(+1) - N(-1)` NON cambia -- come le coppie nel vuoto
                # quantistico. E' il ramo che CONSERVA.
                self._g_nati_schwinger = getattr(self, "_g_nati_schwinger", 0) + int(nc)
                self._g_nati_schwinger_ev = getattr(self, "_g_nati_schwinger_ev", 0) + 1
                if TRACCIA_D0: self._traccia_d0('S07_schwinger', _tr_pre)
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
        if not SCHERMATURA:
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
        # [2026-09-28] IL RAMO DI `L_CONSERVA` E' ARCHIVIATO (csv/_archivio/_l_conserva.py).
        #   Era marcato <<ERRATA, NON usare>> dal codice stesso, e la catena
        #   `rilassa_disegno -> _togli_rotazione_rigida -> calcola_psi` faceva scrivere `psi`
        #   a una legge di tipo `disegno`: il tipo dichiarava il FALSO. Ora e' vero per
        #   COSTRUZIONE. ⚠ E il ramo AGIVA: 17 grandezze su 23 differivano ad accenderlo.

    def pozzo_grafo(self, intensita=None):
        """Pozzo fisico locale del grafo, condiviso da dinamica e visualizzazione.

        Il pozzo non usa la geometria del rendering: ogni nodo riceve il contributo
        di intensita' dei vicini diviso per la distanza reale dell'arco. Restituisce
        anche la maschera degli archi validi e la pendenza del pozzo su ciascun arco,
        cosi' la figura puo' mostrare esattamente la grandezza che guida GRAV_BIFASE.
        """
        n = self.n
        phi_g = np.zeros(n, dtype=float)
        mask = (self.i < n) & (self.j < n)
        ii, jj = self.i[mask], self.j[mask]
        if not len(ii):
            return phi_g, mask, np.zeros(0, dtype=float)
        I = (np.abs(self.psi[:n]) ** 2 if intensita is None and len(self.psi) >= n
             else np.asarray(intensita, dtype=float)[:n])
        if POZZO_D:
            # [D02] LA LUNGHEZZA E' `self.d`, NON `pos`: e' la distanza REALE dell'arco
            #   (`A3-DISEGNO`, NON `A13`), cioe' quella che il docstring di questa funzione
            #   dichiara GIA'.
            #   NESSUN PAVIMENTO: `d >= LAM` con `SEMINA_LAM`, e alla divisione ### **SEMPRE dal commit `6b`** (non piu' <<con `MITOSI_2LAM`>>: il flag e' INERTE). E poiche' e'
            #   una MISURA e non un'invariante, i `d <= 0` si CONTANO (`A8`) -- il
            #   contatore nasce QUI, cosi' a flag spento lo snapshot non cambia.
            L = self.d[mask]
            self._pozzo_d_nonpos = (getattr(self, '_pozzo_d_nonpos', 0)
                                    + int(np.sum(L <= 0.0)))
            self._pozzo_d_tot = getattr(self, '_pozzo_d_tot', 0) + int(np.size(L))
        else:
            v = self.pos[jj] - self.pos[ii]
            L = np.maximum(np.linalg.norm(v, axis=1), 1e-9)
        np.add.at(phi_g, ii, I[jj] / L)
        np.add.at(phi_g, jj, I[ii] / L)
        return phi_g, mask, phi_g[jj] - phi_g[ii]

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
            # [SCALA_MIN_PASSO, C3] ANCHE SUL RITORNO ANTICIPATO il freno va chiuso: senno' lo
            # snapshot resterebbe aperto e il passo DOPO confronterebbe `d0` con quello del passo
            # PRIMA -- una variazione di DUE passi frenata come se fosse di uno.
            # [T1] LA CHIUSURA NON STA PIU' QUI: la fa lo SCHEDULATORE, in coda alla
            #   composizione. Era il difetto che il commento qui sopra descriveva -- un
            #   confine che dipendeva da CHI girava e da QUALE uscita prendeva.
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
        if MEM_MOTO_TUTTO:
            self.mem_mot[:self.n] = (1.0 - plast) * self.mem_mot[:self.n] + plast * grad_tw
            # INERZIA = |Psi|^2: il momento sposta le d0 in proporzione alla massa del nodo.
            memedge = 0.5 * (self.mem_mot[ii] * (I[ii, None] / Imed) +
                             self.mem_mot[jj] * (I[jj, None] / Imed))
            proj = np.sum(memedge * dirarc, axis=1)
        else:
            # [MEM_MOTO_TUTTO, G4-bis 2026-09-22] PUNTI (1) e (2) SPENTI: `mem_mot` non si
            # aggiorna mai e resta ZERO, quindi `memedge` non ha nulla da calcolare.
            # ⚠ `proj` E' ZERO MA CONSERVA LA LUNGHEZZA: `len(proj)` e' il gate del ramo
            #   `GRAV_BIFASE` qui sotto. Un array vuoto spegnerebbe anche la gravita'.
            proj = np.zeros(len(ii))
        
        if len(proj):
            # --- LOCALE PURA: rimossa la sottrazione di proj.mean() ---
            passo_max = 0.01 * float(np.median(self.d0[mask])) if mask.any() else 0.0
            proj = np.clip(proj, -passo_max, passo_max)
            # [MEM_MOTO, 2026-09-22] LA SOLA SCRITTURA DELLA MEMORIA DEL MOTO SU `d0`.
            # Spegnere il flag toglie QUESTA RIGA e basta: `proj` resta calcolato (il ramo della
            # gravita' qui sotto ne usa `len(proj)`), `mem_mot` resta aggiornato, il pavimento
            # `P3` continua a girare. Cosi' si isola IL CONTRIBUTO A `d0`, che e' cio' che la
            # prova di spegnimento deve misurare.
            # [MEM_MOTO_TUTTO] PUNTO (3): lo stesso sito, recintato anche dal flag di `G4-bis`.
            # Non basta che `proj` sia zero: `_sd0` passa dal freno, e una scrittura di zeri
            # NON e' garantita essere un non-evento. Il sito si spegne, non si annacqua.
            if MEM_MOTO and MEM_MOTO_TUTTO:
                if TRACCIA_D0: _tr_pre = self.d0.copy()
                self.d0[mask] += self._sd0(proj, mask)
                if TRACCIA_D0: self._traccia_d0('S08_proj', _tr_pre)
            if TRACCIA_D0: _tr_pre = self.d0.copy()
            if TRACCIA_D0: self._traccia_d0('P3_dopo_proj', _tr_pre)
            
        if GRAV_BIFASE and len(proj):
            s = np.abs(self.tw[mask]) / PHI_CRIT - 1.0    # grandezza FIRMATA: segno = direzione
            phi_g, _, dpozzo = self.pozzo_grafo(I)
            # Guardia: durante una variazione topologica puo' esistere un passo
            # senza differenze di pozzo valide. np.median([]) genera un warning
            # e poi un errore NumPy (median usa mean internamente).
            # [CORREZIONE DI DIFETTO, 2026-09-20 -- par.10 categoria D: nessun flag di scenario]
            #
            # IL DIFETTO, ed era A3: la scala era `median(|dpozzo|)`, cioe' LA MEDIANA DI CIO' CHE
            # SI STA NORMALIZZANDO. Conseguenza ESATTA, non congetturata:
            #     median(ampiezza) = tanh(1) = 0.761594   PER COSTRUZIONE, sempre.
            # MISURATO su 14 istanti su 14, scarto massimo 2.343e-11 -- il nodo mediano ha SEMPRE
            # quel valore, qualunque cosa faccia il sistema. E' il quarto caso della stessa
            # famiglia su questo repo (`median(|f|)` in `ritmo()`, `_dens_rif` in `_tau`,
            # `u_nodo`), ed e' il presidio P4/C12: una grandezza normalizzata sulla propria
            # mediana NON PUO' MUOVERSI, e su quella non si misura nulla.
            # E l'asimmetria era il punto: `r_rad` autonormalizzato, `t_tan` normalizzato su
            # PHI_CRIT, cioe' una costante DICHIARATA. La ripartizione virale confrontava una
            # grandezza che si muove col sistema contro una che non lo fa.
            #
            # LA CURA: la scala e' il POZZO LOCALE. Quanto e' RIPIDO il pozzo dove sei, rispetto a
            # quanto e' PROFONDO -- un GRADIENTE RELATIVO, adimensionale per costruzione e LOCALE.
            # E' la stessa forma di `u_nodo = I / media_dei_vicini`, che `Z5` ha mostrato
            # soddisfare A2. Il denominatore d'arco e' `0.5*(phi_g[ii] + phi_g[jj])`: NON una
            # scelta libera, ma la stessa media d'arco che questa funzione usa gia' per `circ_arc`.
            #
            # ⚠ NESSUN PAVIMENTO, E NON PERCHE' SI SPERI CHE BASTI: il rapporto e' LIMITATO A 2 PER
            # COSTRUZIONE. `phi_g >= 0` per definizione (somma di `I[k]/L` con `I = |psi|^2 >= 0`),
            # quindi |phi_g[j] - phi_g[i]| <= phi_g[i] + phi_g[j] = 2*phi_arc. MISURATO: max = 2
            # esatto, p99 = 1.898, zero valori non finiti su 527452 archi. Il numeratore si annulla
            # almeno tanto in fretta quanto il denominatore, quindi A1 non viene violata.
            # L'unico caso residuo e' `phi_arc == 0` ESATTO, che implica `dpozzo == 0` ESATTO:
            # 0/0 vale ZERO, ed e' una DEFINIZIONE dichiarata, non una scala.
            #
            # FORMA ALGEBRICA: la divisione e' scritta con `np.divide(..., out=, where=)` perche'
            # con denominatore tutto positivo essa e' BINARIAMENTE IDENTICA a `ad / den`. E' cio'
            # che rende esatta la riduzione al limite di `Y1` (lezione R1: la forma conta).
            _ad = np.abs(dpozzo)
            if SCALA_P_MEDIANA:
                # DIAGNOSTICO: la scala VECCHIA, per la riduzione al limite. Non e' fisica.
                _den = np.full(len(dpozzo), (max(float(np.median(_ad)), 1e-9)
                                             if len(dpozzo) else 1e-9))
            else:
                _den = 0.5 * (phi_g[ii] + phi_g[jj])       # il POZZO LOCALE dell'arco
            _rap = np.zeros(len(dpozzo))
            np.divide(_ad, _den, out=_rap, where=(_den > 0.0))   # 0/0 := 0, dichiarato
            ampiezza = np.tanh(_rap)                       # in [0,1), dalla RIPIDEZZA RELATIVA
            # [DIAGNOSTICO, 2026-09-20] TRE SCALARI, byte-inerti: servono ai sigilli `Y3` e `Y4`,
            # che devono misurare `median(ampiezza)` e `sin2` SUL PERCORSO VERO. Ricalcolarli
            # fuori sarebbe una REPLICA, e una replica puo' divergere dal codice che gira -- e'
            # esattamente il difetto che questo repo ha gia' preso quattro volte coi commenti
            # stale. Non sono stato fisico: non entrano in nessuna legge.
            self._diag_amp_med = float(np.median(ampiezza)) if len(ampiezza) else float("nan")
            if SPINORE:
                if not hasattr(self, "_nb") or self._nb is None or len(self._nb) < self.n:
                    b0 = self.phi_s if len(self.phi_s) == self.n else np.zeros(self.n)
                    self._nb = np.stack([np.sin(b0), np.zeros(self.n), np.cos(b0)], axis=1)
            grav = -np.tanh(s) * ampiezza                 # bifase: -s = verso (attrae/respinge), firmato
            # [A8, 2026-09-20] (a) NESSUNA RAGIONE DICHIARATA: se questo ramo non gira, `grav`
            # NON viene proiettata sul campo spinoriale e la gravita' bifase cambia forma.
            # NON E' INDIPENDENTE da :3623: `_nb` e' rinormalizzato a `n` da `_passo_spinoriale`
            # (:2204-:2209), che gira PRIMA nel ciclo -- quindi questo puo' fallire solo se
            # `_passo_spinoriale` NON ha girato, cioe' se e' scattata la guardia :3623.
                        # ✅ MISURATO: **0 salti su 12**, e in `W3` NON si fa scattare. CLASSE: **(c) FORTE**,
            # ⚠ RICLASSIFICATA da `(a)` -- la predizione e' in `849dd25` (ANTENATO del run) e
            # l'approvazione di Luca in `dd6953b`. La riparazione di `_nb` quattro righe sopra gira
            # sotto lo STESSO flag `SPINORE`: questa guardia non e' raggiungibile.
            self._g_nb_grav_proiez_tot = getattr(self, "_g_nb_grav_proiez_tot", 0) + 1
            if SPINORE and not (self._nb is not None and len(self._nb) >= self.n):
                self._g_nb_grav_proiez_salti = getattr(self, "_g_nb_grav_proiez_salti", 0) + 1
                self._g_nb_grav_proiez_shape = (-1 if self._nb is None else len(self._nb), self.n)
                self._g_nb_grav_proiez_quando = self._g_nb_grav_proiez_tot
            if SPINORE and self._nb is not None and len(self._nb) >= self.n:
                _nbg = self._nb_grav()                     # [FASE 2] _nb (off) o direzione NATIVA dal campo emesso (on)
                prod_interno = np.sum(_nbg[ii] * _nbg[jj], axis=1)
                proiez = prod_interno * np.sign(dpozzo)
                grav = grav * proiez
            
            # --- LOCALE PURA: rimossa la sottrazione di grav.mean() ---
            # grav resta intatto, senza compensazioni globali

            c_sistema = LAM * np.sqrt(K_C)                 # velocita' del cono (da LAM, K_C: stato)
            passo_causale = c_sistema * DT                 # TETTO CAUSALE
            if VIRIALE:
                twn_a = self.tw[mask] / PHI_CRIT
                circ_nodo = np.zeros(self.n); grado_c = np.zeros(self.n)
                np.add.at(circ_nodo, ii, twn_a); np.add.at(circ_nodo, jj, -twn_a)
                np.add.at(grado_c, ii, 1.0);     np.add.at(grado_c, jj, 1.0)
                circ_nodo = circ_nodo / np.maximum(grado_c, 1.0)
                circ_arc = 0.5 * (circ_nodo[ii] + circ_nodo[jj])
                r_rad = ampiezza
                if OLON_PART:
                    t_tan = np.tanh(np.hypot(np.abs(circ_arc), np.abs(twn_a)))
                else:
                    t_tan = np.tanh(np.abs(circ_arc))
                H = np.maximum(np.hypot(r_rad, t_tan), 1e-9)
                cos2 = (r_rad / H) ** 2
                sin2 = (t_tan / H) ** 2
                self._diag_sin2_med = float(np.median(sin2)) if len(sin2) else float("nan")
                self._diag_sin2_p95 = (float(np.percentile(sin2, 95)) if len(sin2)
                                       else float("nan"))
                if ZETA_VIR:
                    # [A8, 2026-09-20] IL DEFAULT FUORI DAL `mask` E' UNA DECISIONE FISICA, e va
                    # dichiarata e CONTATA invece di restare in un'allocazione.
                    # `sin2 = 0` significa `beta * (1 - 0) = beta`, cioe' FRENO PIENO: gli archi
                    # fuori dal `mask` vengono frenati SENZA la correzione anisotropa.
                    # PERCHE' E' GIUSTO COSI', e non e' un ripiego: il `mask` e' `(i < n) & (j < n)`
                    # -- gli archi esclusi sono quelli che puntano a nodi che NON ESISTONO, per cui
                    # `sin2` non e' calcolabile. Frenarli come se non avessero conversione virale e'
                    # il comportamento CONSERVATIVO, e l'alternativa (`1`, freno nullo) darebbe a un
                    # arco non calcolabile il trattamento piu' favorevole.
                    # SI CONTA quanti restano fuori: se fossero molti, questo default smetterebbe
                    # di essere una formalita' e diventerebbe una legge, da DERIVARE.
                    s2full = np.zeros(len(self.i))
                    s2full[mask] = sin2
                    self._sin2_vir = s2full
                    self._g_s2full_tot = getattr(self, "_g_s2full_tot", 0) + 1
                    _fuori = int(len(self.i) - int(np.count_nonzero(mask)))
                    self._g_s2full_fuori = _fuori
                    self._g_s2full_fuori_max = max(int(getattr(self, "_g_s2full_fuori_max", 0)),
                                                   _fuori)
                    if _fuori:
                        self._g_s2full_conmask = getattr(self, "_g_s2full_conmask", 0) + 1
                        self._g_s2full_quando = self._g_s2full_tot
                radiale = grav * cos2
                if LS_AZIM and self._nb is not None and len(self._nb) >= self.n:
                    _cen = self.pos[:self.n].mean(0)
                    _rmid = 0.5 * (self.pos[ii] + self.pos[jj]) - _cen
                    _rhat = _rmid / np.maximum(np.linalg.norm(_rmid, axis=1, keepdims=True), 1e-9)
                    _spin = 0.5 * (self._nb[ii] + self._nb[jj])
                    _azim = np.cross(_rhat, _spin)[:, 2]
                    tangenz = np.abs(grav) * sin2 * np.sign(_azim)
                else:
                    tangenz = np.abs(grav) * sin2 * np.sign(circ_arc)
                spinta = radiale + tangenz
                
                # --- LOCALE PURA: rimossa la sottrazione di spinta.mean() ---
                
                passo_causale = c_sistema * DT
                spinta = np.clip(spinta, -passo_causale, passo_causale)
                if TRACCIA_D0: _tr_pre = self.d0.copy()
                self.d0[mask] += self._sd0(spinta * float(np.median(self.d0[mask])), mask)
                if TRACCIA_D0: self._traccia_d0('S09_spinta_med', _tr_pre)
            else:
                # --- LOCALE PURA ---
                grav = np.clip(grav, -passo_causale, passo_causale)
                if TRACCIA_D0: _tr_pre = self.d0.copy()
                self.d0[mask] += self._sd0(grav * float(np.median(self.d0[mask])), mask)
                if TRACCIA_D0: self._traccia_d0('S10_grav_med', _tr_pre)
            if TRACCIA_D0: _tr_pre = self.d0.copy()
            if TRACCIA_D0: self._traccia_d0('P4_dopo_grav', _tr_pre)
            
        # [A8, 2026-09-20] (b) RAGIONE VALIDA: `K_FRANGE = 0.0`, quindi il ramo e' morto per
        # COSTANTE, non per condizione. Come per COMPAT_CHI il contatore si chiama `_spento` e non
        # `_salti`: misura un ramo che non gira per scelta, ed e' un presidio contro
        # un'accensione silenziosa.
                # ✅ MISURATO: ramo SPENTO 12 volte su 12. CLASSE: **(b)** -- morto per COSTANTE.
        self._g_k_frange_tot = getattr(self, "_g_k_frange_tot", 0) + 1
        if K_FRANGE == 0.0:
            self._g_k_frange_spento = getattr(self, "_g_k_frange_spento", 0) + 1
        if K_FRANGE != 0.0 and len(proj):
            dphi_arc = np.angle(np.exp(1j * (self.phi[jj] - self.phi[ii])))
            wI = 0.5 * (I[ii] + I[jj]) / Imed
            flusso = K_FRANGE * wI * dphi_arc
            
            # --- LOCALE PURA: rimossa la sottrazione di flusso.mean() ---
            
            flusso = np.clip(flusso, -passo_max, passo_max)
            if TRACCIA_D0: _tr_pre = self.d0.copy()
            self.d0[mask] += self._sd0(flusso, mask)
            if TRACCIA_D0: self._traccia_d0('S11_flusso', _tr_pre)
            if TRACCIA_D0: _tr_pre = self.d0.copy()
            if TRACCIA_D0: self._traccia_d0('P5_dopo_flusso', _tr_pre)
            
        # --- COESIONE RELAZIONALE CON ANCORA ELASTICA VERSO LA SCALA NATIVA (LAM) ---
        if len(mask) and mask.any():
            I_nodi = np.abs(self.psi[:n]) ** 2
            d_archi = np.maximum(self.d[mask], 1e-6)
            
            grad_I_relativo = (I_nodi[jj[mask]] - I_nodi[ii[mask]]) / d_archi
            
            lap_I = np.zeros(self.n)
            deg_loc = np.maximum(self._deg[:n], 1)
            np.add.at(lap_I, ii, I_nodi[jj] - I_nodi[ii])
            np.add.at(lap_I, jj, I_nodi[ii] - I_nodi[jj])
            lap_I = lap_I / deg_loc
            lap_arco = 0.5 * (lap_I[ii[mask]] + lap_I[jj[mask]])
            
            I_arco = 0.5 * (I_nodi[ii[mask]] + I_nodi[jj[mask]])
            I_med = max(float(np.mean(I_nodi)), 1e-9)
            
            # [COES_CAUSALE, C4] `d` e `d0` dall'ISTANTE DI INIZIO PASSO. Il fallback e'
            #   CONTATO, non silenzioso: se la fotografia manca o ha la lunghezza sbagliata si
            #   usa il valore corrente e si REGISTRA, invece di far finta di niente (`P5`).
            _cc_d, _cc_d0 = self.d, self.d0
            if COES_CAUSALE:
                _f_d = getattr(self, '_smp_d', None)
                _f_d0 = getattr(self, '_smp_d0', None)
                self._g_cc_tot = getattr(self, '_g_cc_tot', 0) + 1
                if (_f_d is not None and _f_d0 is not None
                        and len(_f_d) == len(self.d) and len(_f_d0) == len(self.d0)):
                    _cc_d, _cc_d0 = _f_d, _f_d0
                    self._g_cc_usi = getattr(self, '_g_cc_usi', 0) + 1
                    self._g_cc_scarto_d0 = max(
                        getattr(self, '_g_cc_scarto_d0', 0.0),
                        float(np.max(np.abs(np.asarray(self.d0, dtype=float) - _f_d0))))
                else:
                    self._g_cc_salti = getattr(self, '_g_cc_salti', 0) + 1
                    self._g_cc_shape = (-1 if _f_d0 is None else len(_f_d0), len(self.d0))
            rapporto_portata = _cc_d[mask] / LAM
            filtro_portata = 1.0 - np.tanh(rapporto_portata)
            
            scala_statale = (CS_M ** 2) / I_med
            
            delta_relativo_arco = np.abs(I_nodi[jj[mask]] - I_nodi[ii[mask]]) / I_med
            peso_dinamico_shear = np.tanh(delta_relativo_arco)
            
            # 1. Dinamica di campo (gradiente e curvatura trasversale)
            forza_campo = -(grad_I_relativo - peso_dinamico_shear * lap_arco)
            
            # 2. Ancora elastica verso la scala nativa LAM (potenziale armonico di richiamo)
            # Penalizza lo scostamento di d0 dalla lunghezza d'onda fondamentale LAM
            # [C4] il richiamo elastico e' l'ingresso che stava FUORI ISTANTE: leggeva un
            #   `d0` gia' spostato da SETTE scritture dello stesso passo.
            scostamento_scala = (_cc_d0[mask] - LAM) / LAM
            richiamo_elastico = -scostamento_scala
            
            # Composizione della coesione totale con il bilancio elastico
            coesione_relazionale = scala_statale * (forza_campo + richiamo_elastico) * filtro_portata * (self.d0[mask] ** 2) * (I_arco / I_med)
            
            stress_metrico = np.abs(self.d[mask] - self.d0[mask]) / np.maximum(self.d0[mask], 1e-6)
            tasso_dinamico = np.tanh(stress_metrico) * self.d0[mask]

            # --- [COES_ADIM] LA FORMA ADIMENSIONALE, ACCANTO ALLA VECCHIA ---------------
            # I tre addendi diventano adimensionali con la densita' LOCALE dell'arco, e
            # `I_med` sparisce da ENTRAMBE le posizioni (era una MEDIA GLOBALE, A2).
            # `|F_adim| <= 1` PER COSTRUZIONE: |tanh| <= 1 e filtro_portata in (0,1). NON e'
            # un clip -- ed e' per questo che questa forma SOSTITUISCE `tanh(stress)*d0`,
            # che `Z79` ha misurato SATURO.
            if COES_ADIM:
                _dI = I_nodi[jj[mask]] - I_nodi[ii[mask]]
                # NESSUN PAVIMENTO su `I_arco`: dove e' ESATTAMENTE zero il rapporto e' `0/0`
                # e si definisce ZERO (precedente dichiarato: `scala_p`, `Z67`); dove e'
                # minuscolo ma non nullo il rapporto e' enorme MA IL `tanh` LO LIMITA A 1.
                # La limitatezza e' STRUTTURALE, non messa a mano.
                _ok = I_arco > 0.0
                _ia = np.where(_ok, I_arco, 1.0)
                _grad_adim = np.where(_ok, _dI / _ia, 0.0)
                _lap_adim = np.where(_ok, lap_arco / _ia, 0.0)
                _peso_adim = np.tanh(np.abs(_grad_adim))
                _forza_adim = -(_grad_adim - _peso_adim * _lap_adim)
                # `richiamo_elastico` era GIA' adimensionale: -(d0-LAM)/LAM. Invariato.
                _F_adim = np.tanh(_forza_adim + richiamo_elastico) * filtro_portata
                # IL TETTO CAUSALE, ricalcolato in loco e NON preso dalla variabile di sopra,
                # che sta dentro un `if`: usarla sarebbe dipendere da un ramo. Stessa
                # espressione dei due siti fratelli (la spinta e la gravita').
                # [COES_CAUSALE, C4] IL TETTO DAL CONO LOCALE DELL'ARCO.
                #   `LAM*sqrt(K_C)*DT` e' costruito su COSTANTI DI MODULO: `c_sistema = 1.1314`
                #   non conosce il cono del luogo in cui scrive, e il cono locale misurato
                #   scende fino a `0.566` -- li' il tetto globale ne permette il DOPPIO (`A5`).
                #   Si prende il `cs` del nodo PIU' LENTO dei due: la scelta CONSERVATIVA.
                #   ⚠ NON e' sempre piu' stretto: col cono mediano e' piu' LARGO. Il punto non
                #   e' stringere, e' che il tetto sia quello del LUOGO -- e si CONTA in quale
                #   verso agisce, invece di sperare che stringa.
                if COES_CAUSALE:
                    _csn = getattr(self, '_cs_nodo_prev', None)
                    self._g_cct_tot = getattr(self, '_g_cct_tot', 0) + 1
                    if _csn is not None and len(_csn) >= self.n:
                        _csa = np.minimum(np.asarray(_csn, dtype=float)[ii[mask]],
                                          np.asarray(_csn, dtype=float)[jj[mask]])
                        self._g_cct_usi = getattr(self, '_g_cct_usi', 0) + 1
                    else:
                        # fallback DICHIARATO e CONTATO: senza `--cs-dinamico` la cache non
                        # esiste, e il cono e' quello nominale.
                        _csa = np.full(int(np.sum(mask)), float(CS_M))
                        self._g_cct_salti = getattr(self, '_g_cct_salti', 0) + 1
                    _passo_causale = _csa * DT
                    _glob = LAM * np.sqrt(K_C) * DT
                    self._g_cct_stringe = (getattr(self, '_g_cct_stringe', 0)
                                           + int(np.sum(_passo_causale < _glob)))
                    self._g_cct_allarga = (getattr(self, '_g_cct_allarga', 0)
                                           + int(np.sum(_passo_causale > _glob)))
                    self._g_cct_archi = (getattr(self, '_g_cct_archi', 0)
                                         + int(len(_passo_causale)))
                    self._g_cct_min = min(getattr(self, '_g_cct_min', float('inf')),
                                          float(np.min(_passo_causale)))
                else:
                    _passo_causale = LAM * np.sqrt(K_C) * DT
                _delta_coes = _passo_causale * _F_adim
                if COES_CAUSALE:
                    # [C4] IL CRITERIO, contato invece che sperato: nessuno spostamento piu'
                    #   veloce del cono LOCALE. `|F_adim| <= 1` per costruzione, quindi la
                    #   violazione dovrebbe essere IMPOSSIBILE -- e proprio per questo va
                    #   CONTATA: un invariante che nessuno misura non e' un invariante (`A9`).
                    self._g_cct_viol = (getattr(self, '_g_cct_viol', 0)
                                        + int(np.sum(np.abs(_delta_coes)
                                                     > _passo_causale * (1.0 + 1e-12))))
                    _rap = np.abs(_delta_coes) / np.maximum(_passo_causale, 1e-300)
                    self._g_cct_rapmax = max(getattr(self, '_g_cct_rapmax', 0.0),
                                             float(np.max(_rap)) if len(_rap) else 0.0)
                self._g_coes_adim_usi = getattr(self, '_g_coes_adim_usi', 0) + 1
                self._g_coes_tetto = float(np.min(_passo_causale)) \
                    if np.ndim(_passo_causale) else float(_passo_causale)
                self._g_coes_max = max(getattr(self, '_g_coes_max', 0.0),
                                       float(np.max(np.abs(_delta_coes)))
                                       if len(_delta_coes) else 0.0)
                self._g_coes_satura = (getattr(self, '_g_coes_satura', 0)
                                       + int(np.sum(np.abs(_F_adim) > 0.99)))
                self._g_coes_archi = getattr(self, '_g_coes_archi', 0) + int(len(_F_adim))
            # ---------------------------------------------------------------------------
            
            # [2026-09-20] LA MISURA CHE MANCAVA: `coesione_relazionale` PRIMA del clip.
            # ⚠ Senza questo numero non si sa se il clip stia PROTEGGENDO da un termine enorme
            # (e allora stringerlo non basta: il difetto e' nel TERMINE) oppure se sia LUI a
            # produrre il movimento (e allora la cura e' il tetto). E' il criterio di chiusura
            # scritto in `Z79`. Byte-inerte: gira solo con `TRACCIA_D0`.
            if TRACCIA_D0: self._traccia_coesione(coesione_relazionale, tasso_dinamico, mask)
            if TRACCIA_D0: _tr_pre = self.d0.copy()
            if COES_ADIM:
                self.d0[mask] += self._sd0(_delta_coes, mask)
            else:
                self.d0[mask] += self._sd0(
                    np.clip(coesione_relazionale, -tasso_dinamico, tasso_dinamico), mask)
            if TRACCIA_D0: self._traccia_d0('S12_coesione', _tr_pre)
            if TRACCIA_D0: _tr_pre = self.d0.copy()
            if TRACCIA_D0: self._traccia_d0('P6_dopo_coesione', _tr_pre)
        #--- ACCOPPIAMENTO LATERALE DINAMICO E RELATIVO (Senza costanti improprie) ---
        if len(self.tw) and len(self.i) and self.n > 0:
            mask = (self.i < n) & (self.j < n)
            if mask.any():
                ii, jj = self.i[mask], self.j[mask]
                
                # 1. Intensità di campo locale e media di riferimento relativa
                I_nodi = np.abs(self.psi[:n]) ** 2 if hasattr(self, "psi") and len(self.psi) >= n else np.ones(n)
                I_med = max(float(np.mean(I_nodi)), 1e-9)
                
                # 2. Spin locale normalizzato rispetto al quanto di olonomia
                spin_relativo = np.abs(self.tw[mask]) / PHI_CRIT
                
                # 3. Geodetica e direzione ortogonale trasversale nel piano relazionale
                v_rel = self.pos[jj] - self.pos[ii]
                v_norm = np.maximum(np.linalg.norm(v_rel, axis=1, keepdims=True), 1e-9)
                dir_radiale = v_rel / v_norm
                
                # Vettore ortogonale (di lato) per il dragging laterale
                dir_laterale = np.stack([-dir_radiale[:, 1], dir_radiale[:, 0], np.zeros_like(dir_radiale[:, 0])], axis=1)
                
                # 4. Fattore di accoppiamento totalmente relativo (interazione vs inerzia locale)
                inerzia_locale = np.maximum(0.5 * (I_nodi[ii] + I_nodi[jj]) / I_med, 1e-3)
                accoppiamento_dinamico = spin_relativo / inerzia_locale
                
                # [MEM_MOTO_TUTTO] PUNTO (4): L'EFFETTO INDIRETTO, ed e' la ragione per cui questo
                # flag esiste. `MEM_MOTO` lo lascia VIVO -- spegne la scrittura su `d0` ma
                # `mem_mot` continua ad aggiornarsi, e QUESTA riga continua a leggerla e a
                # scrivere su `self.phi`. Qui si spegne anche quello.
                # ⚠ NON si conta sul fatto che `mem_mot` sia zero: `(phi + 0) % (4 pi)` e' un
                #   NO-OP solo se `phi` sta gia' nel dominio. Il ramo si spegne, non si annacqua.
                if MEM_MOTO_TUTTO:
                    # Proiezione del gradiente di memoria del moto sulla direzione trasversale
                    proiezione_trasversale = np.sum(self.mem_mot[ii] * dir_laterale, axis=1)

                    # Shift di fase emergente guidato interamente dallo stato del sistema e dalla deformazione metrica
                    d_archi = np.maximum(self.d[mask], 1e-6)
                    d0_archi = np.maximum(self.d0[mask], 1e-6)
                    shift_fase_dinamico = accoppiamento_dinamico * proiezione_trasversale * (d_archi / d0_archi)

                    # Limite geometrico causale del passo di fase per preservare la stabilità del campo
                    shift_fase_dinamico = np.clip(shift_fase_dinamico, -np.pi * 0.25, np.pi * 0.25)

                    # Applica lo shift al campo di fase senza alterare le coordinate fisse dei puntatori (net.pos)
                    # [MEM_FASE, cura (2) di MEM-HEBB-VERSO, decisione di Luca del 2026-10-04]
                    # IL SITO SI SPEGNE CON UN FLAG PROPRIO, e il DEFAULT lo tiene SPENTO.
                    # ⛔ MISURATO: scartava il 97.3% dei contributi, perche' `ii` CONTIENE
                    #   RIPETIZIONI e l'indicizzazione fancy in scrittura FA VINCERE L'ULTIMO.
                    #   Rapporto dei moduli scartati/applicati 36.2 (referto `2717308`).
                    #   QUALE contributo sopravvivesse dipendeva dall'ORDINE DELL'ARRAY.
                    # ⚠ E QUESTO `if` TOGLIE ANCHE IL `% self._dphi()`, non solo la somma:
                    #   vedi il commento otto righe sopra. Se `phi` uscisse dal dominio la
                    #   differenza sarebbe piu' grande di `shift_fase_dinamico`.
                    # `MEM_MOTO` e `MEM_MOTO_TUTTO` NON cambiano, e `mem_mot` continua ad
                    # aggiornarsi: si recinta QUESTA scrittura e nient'altro.
                    if MEM_FASE:
                        self.phi[ii] = (self.phi[ii] + shift_fase_dinamico) % self._dphi()
                if TRACCIA_D0: _tr_pre = self.d0.copy()
                if TRACCIA_D0: self._traccia_d0('P7_dopo_4917', _tr_pre)
        # [SCALA_MIN_PASSO, C3] IL FRENO SU `d0`, UNA VOLTA SOLA, a fine ciclo. `memoria_
        # hebbiana_moto` e' l'ULTIMA chiamata del passo nel driver e nelle rigiocate sigillate.
        # [T1] la CHIUSURA e il controllo degli INVARIANTI sono passati allo SCHEDULATORE
        #   (`esegui_passo`), in coda alla composizione. L'ORDINE RELATIVO E' PRESERVATO
        #   -- chiudi, poi verifica -- ed e' cio' che rende T1 byte-identico: il controllo
        #   guarda `d0` GIA' frenata, esattamente come prima.
        # [C5] IL CONTROLLO GIRA A FINE PASSO, su TUTTO lo stato. `memoria_hebbiana_moto` e'
        #   l'ULTIMA chiamata del ciclo nel driver e nelle rigiocate sigillate.

    def diagnostica(self):
        I = self.intensita()
        z = np.exp(1j * self.phi)
        w = self._pesi()
        num = np.abs(self._mat(w) @ z)
        den = np.maximum(np.bincount(self.i, w, minlength=self.n) +
                         np.bincount(self.j, w, minlength=self.n), 1e-9)
        li = self.lambda_nodi() if self.n and len(self.i) else np.full(self.n, LAM)
        ncrit = massa_critica_adattiva(self) if self.n and len(self.i) else 0.0
        rho_c = ncrit / max((4.0 / 3.0) * np.pi * LAM**3, 1e-9) if ncrit else 0.0
        return dict(I=I,
                    coer_g=float(abs(z.mean())) if self.n else 0.0,
                    coer_l=float(np.mean(np.clip(num / den, 0, 1))) if self.n else 0.0,
                    picco=float(I.max()) if len(I) else 0.0,
                    stress=float(np.median((self.d - self.d0) / np.maximum(self.d0, 1e-9))) if len(self.d) else 0.0,
                    # MEDIANA, non media: lo stress e' |d-d0|/d0 per arco. Pochi archi
                    # patologici (corti a riposo, tesi ora: ~2%) dominano la MEDIA e la
                    # gonfiano a valori enormi, pur essendo outlier. La mediana riflette
                    # lo stress TIPICO del sistema, robusto agli outlier - la fisica vera.
                    dil=float(np.mean(self.d) / max(np.mean(self.d0), 1e-9) - 1) if len(self.d) else 0.0,
                    tw=float(np.abs(self.tw).max()) if len(self.tw) else 0.0,
                    entro=float((self.d <= R_CONN()).mean()) if len(self.d) else 0.0,
                    d_med=float(np.mean(self.d)) if len(self.d) else 0.0,
                    ncrit_adattivo=float(ncrit),
                    rho_critica=float(rho_c),
                    lambda_eff_min=float(np.min(li)) if len(li) else LAM,
                    lambda_eff_med=float(np.median(li)) if len(li) else LAM,
                    lambda_eff_max=float(np.max(li)) if len(li) else LAM,
                    lambda_eff_ratio_med=float(np.median(li) / max(LAM, 1e-9)) if len(li) else 1.0,
                    rho_su_rhoc_max=float(np.max(I) / max(rho_c, 1e-9)) if len(I) and rho_c else 0.0)


net = Rete()
# [SCENA-1] il vuoto dell'`import` resta a `SEME_INIZIALE`: qui `SEMINA_LAM` e' ancora `False`
#   (i flag si applicano DOPO, in `_applica_flag`), e la cura del mondo del 2026-09-21 ha gia'
#   stabilito che questo vuoto viene RICOSTRUITO quando i flag sono noti. Cambiarlo qui
#   significherebbe deciderlo prima di sapere con quali flag si gira.
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
    acc = dict(passo=0.0)   # [T1] un solo tempo: il passo. Vedi il commento sotto.
    for k in range(N_PASSI):
        # CICLO COMPLETO identico al runtime (update): stessa fisica, stesse leggi, stesso ordine.
        # [T1] IL BENCHMARK PASSA DALL'ESECUTORE, e con questo PERDE il dettaglio per
        #   legge: prima cronometrava le cinque chiamate una per una. LO DICHIARO invece
        #   di lasciarlo scoprire: oggi misura il PASSO INTERO. Il dettaglio per legge
        #   tornera' strumentando lo SCHEDULATORE (strato 5), non ricopiando l'ordine qui.
        t0 = _t.time(); esegui_passo(net);           acc["passo"]   += _t.time() - t0
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
    cx puo' essere un numero (coordinata x, centro sull'asse) o una terna/array (x,y,z).

    ⛔ **LE SCENE CHE SEMINANO MASSE SOPRA IL VUOTO SONO DI EPOCA PRE-`A13`**
    *(decisione di Luca, 2026-09-25)*. Con `SEMINA_LAM` acceso **RIFIUTANO DI PARTIRE, e lo
    DICONO** (`A9`): **non si adattano in silenzio.**

    **PERCHE', ed e' misurato:** `_massa` chiede `n` nodi in un raggio `r` **scelto per la
    scena**, e quei raggi vengono dall'epoca in cui **una distanza sotto `LAM` era ammessa**.
    Il caso piu' chiaro: `_semina_n_masse` chiede `497` nodi in raggio `0.7 = 0.875 LAM`,
    **dove ce ne stanno `5`** — un rapporto di **`104`**. **Non e' una scena da adattare: e'
    una scena di un'altra fisica.**

    **La scena `(ii)` (`MASSE-COERENTI`) NON passa da qui**: le sue masse sono **regioni a fase
    coerente di un vuoto solo**, e non aggiungono nodi.
    """
    if SEMINA_LAM:
        raise SystemExit(
            "[massa] SCENA DI EPOCA PRE-`A13`: `_massa` semina %s nodi in un raggio scelto per\n"
            "  la scena, e quei raggi vengono dall'epoca in cui una distanza sotto `LAM` era\n"
            "  ammessa. Con `SEMINA_LAM` acceso questa scena NON PARTE, e NON si adatta in\n"
            "  silenzio (`A9`).\n"
            "  IL CASO PIU' CHIARO, misurato: `N-MASSE` chiede 497 nodi in raggio 0.7 = 0.875 LAM,\n"
            "  dove ce ne stanno 5. Rapporto 104.\n"
            "  CHE FARE: usare la scena `MASSE-COERENTI` (la scena `(ii)`), dove le masse sono\n"
            "  REGIONI A FASE COERENTE di un vuoto solo e non aggiungono nodi; oppure spegnere\n"
            "  `--semina-lam` e DICHIARARE che il run e' di epoca pre-`A13`." % n)
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


# ============================================================================================
# SCENA (ii) -- MASSA = REGIONE A FASE COERENTE IN UN VUOTO SOLO  (decisione di Luca, 2026-09-25)
# ============================================================================================
# **LE MASSE NON AGGIUNGONO NODI.** Si semina UN SOLO vuoto, fino a SATURAZIONE, e le masse sono
# TRE REGIONI di quel vuoto a cui si da' una FASE COMUNE. E' la differenza con la scena di
# `CURA 2`, dove ogni massa era una semina a se' e il vuoto non c'era.
#
# LA GEOMETRIA SI DERIVA, non si sceglie -- un solo ingresso, `--sep`:
#   centri sul cerchio di raggio `sep`       -> distanza fra centri adiacenti = sep*sqrt(3)
#   raggio della regione                     -> r = (sep*sqrt(3) - R_CONN)/2
#                                               cioe' IL VARCO FRA LE SUPERFICI E' `R_CONN`:
#                                               le regioni NON si toccano e NON si allacciano
#                                               direttamente, ma il vuoto fra loro si'.
#   raggio del vuoto                         -> Rv = sep + r + R_CONN
#                                               un guscio di `R_CONN` oltre la regione piu'
#                                               esterna, cosi' nessuna regione tocca il bordo.
#
# LE DUE SCENE, e sono LO STESSO CODICE con `--sep` diverso (misurate il 2026-09-25):
#   (a) "STESSO RAGGIO"   --sep 6.1158  -> r = 4.0964   vuoto 12.6122   ~411 nodi/regione
#   (b)                   --sep 4.0     -> r = 2.2641   vuoto  8.6641   ~ 70 nodi/regione
# ⚠ La `(a)` si chiama «STESSO RAGGIO», NON «stessa materia»: i 497 nodi per massa di `CURA 2`
#   stavano in un raggio `0.7 = 0.875 LAM`, dove ce ne stanno 5. Non c'e' una materia da
#   conservare, perche' quella materia era SOTTO LA SCALA DI PLANCK (`A13`).
_MC_VIDEO = {"nodi": 0, "fasi_casuali": False}   # riempiti da esegui_headless

def _semina_masse_coerenti():
    """SCENA (ii). Semina UN vuoto e marca TRE REGIONI a fase coerente. NON aggiunge nodi."""
    sep = _sep_video()
    rc = R_CONN()
    r = 0.5 * (sep * np.sqrt(3.0) - rc)
    if r <= 0:
        raise SystemExit(
            "[scena-ii] `--sep %.6f` da' un raggio di regione NEGATIVO (%.6f): con tre masse su\n"
            "  un cerchio di raggio `sep` i centri distano `sep*sqrt(3)`, e il varco fra le\n"
            "  superfici e' `R_CONN = %.6f`. Serve `sep > %.6f`." % (sep, r, rc, rc / np.sqrt(3.0)))
    Rv = sep + r + rc
    # --- UN SOLO VUOTO, e lo si VERIFICA invece di sperarlo. Se la rete ha gia' dei nodi,
    #     il vuoto dell'`import`/di `--nodi` si SOMMEREBBE a questo: due vuoti, non uno, e la
    #     scena non sarebbe quella decisa. NON lo aggiusto in silenzio (`A9`): lo DICO.
    if net.n:
        raise SystemExit(
            "[scena-ii] LA RETE HA GIA' %d NODI: la scena (ii) vuole UN SOLO VUOTO, e questo si\n"
            "  SOMMEREBBE. Si lancia con `--nodi 0`. NON svuoto la rete da solo (`A9`): svuotarla\n"
            "  significherebbe buttare via cio' che un altro flag ha chiesto, senza dirlo." % net.n)
    # --- IL VUOTO. `nodi = 0` -> SATURAZIONE (il numero lo decide la geometria). Il braccio di
    #     controllo di `P-GONFIA` passa il numero MISURATO qui, per avere lo STESSO `n`.
    _n = int(_MC_VIDEO.get("nodi") or 0)
    net.semina(-1 if _n <= 0 else _n, raggio=Rv, centro=(0.0, 0.0, 0.0))
    pos = np.asarray(net.pos, float)
    # --- LE TRE REGIONI. Nessun nodo nuovo: si assegna la FASE e si registra la coorte.
    _cas = bool(_MC_VIDEO.get("fasi_casuali"))
    dentro = np.zeros(net.n, bool)
    for k in range(3):
        ang = 2.0 * np.pi * k / 3.0
        c = np.array([sep * np.cos(ang), sep * np.sin(ang), 0.0])
        idx = np.where(np.linalg.norm(pos - c, axis=1) <= r)[0]
        if _cas:
            # BRACCIO DI CONTROLLO DI `S10` (Luca): fasi CASUALI anche DENTRO le regioni.
            # La coorte resta la STESSA -- cambia solo la fase -- cosi' `S10` si legge come
            # CONTRASTO e non in assoluto: il ~50 % che `Lam` da' per costruzione non si
            # confonde con mezzo successo.
            ph = net.rng.random(len(idx)) * net._dphi()
        else:
            # LA FASE DELLA REGIONE: **LA STESSA PER TUTTE E TRE**, al CENTRO del dominio.
            #
            # ① PERCHE' NON `0`: una fase a zero sta **esattamente sul taglio dell'avvolgimento**,
            #   e `phi % _dphi()` manda la coda gaussiana negativa a `~4 pi`. La fase resta
            #   coerente SUL CERCHIO, ma ogni statistica LINEARE la legge come disordine
            #   MASSIMO -- MISURATO: `std(phi) = 6.0798` per `massa_0` contro `0.0518` e
            #   `0.0468` delle altre due, **a fase identicamente coerente**. E `3.63` e' il
            #   valore di fasi CASUALI, quindi `6.08` e' **peggio del caso**: il segno che
            #   sbaglia la STATISTICA, non il dato. (La coerenza si misura `|<e^{i phi}>|`.)
            #
            # ②❗ PERCHE' UNA SOLA FASE, E NON UNA PER REGIONE -- **DECISIONE DI LUCA,
            #   2026-09-25, su una scelta di fisica che avevo fatto SENZA DICHIARARLA.**
            #   La prima stesura metteva ogni regione al centro di un TERZO diverso del
            #   dominio, `_dphi()*(k+0.5)/3`: evitava il taglio, ma **dava alle tre masse
            #   fasi SFASATE DI 120 GRADI in `exp(i phi)`**.
            #   **Masse sfasate INTERFERISCONO in parte in modo distruttivo**: fra loro
            #   nascono repulsione o cancellazione **dalla CONDIZIONE INIZIALE, non dalla
            #   dinamica** -- e la prima delle tre prove chiede proprio *«due masse si
            #   avvicinano?»*. Sarebbe stato un effetto messo dentro da me.
            #   **La scena vecchia usava la STESSA fase per tutte, e il codice diceva
            #   perche': «fase compatibile: le masse devono coesistere, non annichilarsi».**
            #   Se un giorno servissero masse sfasate, dev'essere una scelta DICHIARATA e
            #   un esperimento a parte.
            #
            # ③ PERCHE' `_dphi()/2`: sta **lontana dal taglio da entrambi i lati**, e nel
            #   campo -- che vede la fase su `2 pi` -- **equivale alla fase ZERO di prima**
            #   (`_dphi()/2 = 2 pi` sul dominio `4 pi`). **Nessun numero nuovo**: il centro
            #   di un intervallo non e' una manopola.
            # La dispersione `0.05` NON e' un numero nuovo: e' la stessa di `semina(fase=...)`.
            ph = net._dphi() / 2.0 + net.rng.normal(0, 0.05, len(idx))
        net.phi[idx] = ph % net._dphi()
        net.phi0[idx] = net.phi[idx]
        dentro[idx] = True
        et = "massa_%d" % k
        test["dati"].setdefault("coorti", {})[et] = idx
        test["dati"].setdefault("E0", {})[et] = None
    # il VUOTO come coorte a se': serve a `S9` (contrasto dentro/fuori) come DENOMINATORE.
    test["dati"].setdefault("coorti", {})["vuoto"] = np.where(~dentro)[0]
    test["dati"].setdefault("E0", {})["vuoto"] = None
    # ⚠ `conc_nodi` NON viene toccato, di proposito: le regioni NON sono masse SEMINATE, e
    #   marcarle come tali direbbe che il lignaggio viene da una semina che non c'e' stata.
    test["dati"]["scena_ii"] = dict(
        sep=float(sep), r_regione=float(r), raggio_vuoto=float(Rv), R_CONN=float(rc),
        n_vuoto=int(net.n), fasi_casuali=bool(_cas),
        saturazione=int(getattr(net, "_sl_saturazione", -1)),
        dentro=int(dentro.sum()), quota=float(dentro.mean()) if net.n else float("nan"))
    print("[scena-ii] sep %.6f  r_regione %.6f  raggio_vuoto %.6f  R_CONN %.6f" % (sep, r, Rv, rc))
    print("[scena-ii] n = %d   dentro le regioni = %d   QUOTA = %.4f   fasi_casuali = %s"
          % (net.n, int(dentro.sum()), dentro.mean() if net.n else float("nan"), _cas))


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
 "MASSE-COERENTI": [
   dict(cap=lambda: "SCENA (ii) 1/2 - UN SOLO VUOTO (sep %.4f), e le masse sono TRE REGIONI a "
                    "fase coerente: NON aggiungono nodi" % _sep_video(),
        al_via=lambda: _semina_masse_coerenti(), dur=120),
   dict(cap=lambda: "SCENA (ii) 2/2 - evoluzione libera: le regioni restano coerenti o si "
                    "erodono dal bordo; coerenza %.2f" % net.diagnostica()['coer_l'],
        dur=280)],
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


def _render_vista_rete_sola(net, M, R, dg):
    """Mostra l'evoluzione del grafo: nodi e archi nello stesso quadro."""
    from matplotlib.collections import LineCollection
    from mpl_toolkits.mplot3d.art3d import Line3DCollection

    n = net.n
    P3 = net.pos[:n] @ M
    P2 = net.pos[:n]                    # piano intrinseco fisico (x, y), non vista ruotata
    if hasattr(net, "psi") and len(net.psi) >= n:
        Ivis = np.abs(net.psi[:n]) ** 2
    else:
        Ivis = np.zeros(n)
    phi_g, _, dpozzo_tutti = net.pozzo_grafo(Ivis)
    chi = (net.perc_chi[:n] if hasattr(net, "perc_chi") and len(net.perc_chi) >= n
           else np.zeros(n))
    valid = ((net.i < n) & (net.j < n)) if len(net.i) else np.zeros(0, dtype=bool)
    indici = np.flatnonzero(valid)[:24000]
    na = len(indici)
    ii = net.i[indici] if na else np.zeros(0, dtype=int)
    jj = net.j[indici] if na else np.zeros(0, dtype=int)
    seg2 = np.stack([P2[ii, :2], P2[jj, :2]], axis=1) if na else np.zeros((0, 2, 2))
    tw = (np.abs(net.tw[indici]) / max(PHI_CRIT, 1e-9)
          if na and len(net.tw) > int(indici.max()) else np.zeros(na))
    # dpozzo_tutti e' gia' compresso sulla maschera degli archi validi;
    # indici serve invece per leggere i vettori originali i/j/tw.
    dpozzo = np.abs(dpozzo_tutti[:na]) if na else np.zeros(0)

    # La scala appartiene al grafo, non al campo: così l'evoluzione topologica resta leggibile.
    r_grafo_2d = float(np.max(np.linalg.norm(P2[:, :2], axis=1))) if n else 1.0
    r_grafo_2d = max(r_grafo_2d * 1.18, 1e-6)
    r_grafo_3d = float(np.max(np.linalg.norm(P3, axis=1))) if n else 1.0
    r_grafo_3d = max(r_grafo_3d * 1.18, 1e-6)
    phi_max = max(float(np.max(phi_g)) if n else 0.0, 1e-12)
    dimensione_nodi = 18.0 + 38.0 * np.sqrt(np.clip(phi_g / phi_max, 0.0, 1.0))
    dphi_max = max(float(np.max(dpozzo)) if na else 0.0, 1e-12)

    # Pannello principale: grafo XY, nodi e archi nello stesso spazio e nello stesso frame.
    if na:
        lc = LineCollection(seg2, cmap="plasma", linewidths=0.8, alpha=0.72,
                            zorder=1)
        lc.set_array(np.clip(dpozzo / dphi_max, 0.0, 1.0)); ax.add_collection(lc)
    if n:
        ax.scatter(P2[:, 0], P2[:, 1], c=phi_g, s=dimensione_nodi, cmap="magma",
                   vmin=0, vmax=phi_max, alpha=1.0, edgecolors="white", linewidths=0.35,
                   zorder=3)
    ax.set_xlim(-r_grafo_2d, r_grafo_2d); ax.set_ylim(-r_grafo_2d, r_grafo_2d)
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_title("EVOLUZIONE DEL GRAFO PLANARE · pozzo fisico\n"
                 f"frame {stato['nframe']} · N={n} · E={len(net.i)} · colore = phi_g",
                 fontsize=11, color="#0277bd", weight="bold")

    # Pannello centrale: la stessa rete nello spazio 3D.
    if na:
        seg3 = [[tuple(P3[a]), tuple(P3[b])] for a, b in zip(ii, jj)]
        lc3 = Line3DCollection(seg3, cmap="plasma", linewidths=0.65, alpha=0.65)
        lc3.set_array(np.clip(dpozzo / dphi_max, 0.0, 1.0)); ax3d.add_collection3d(lc3)
    if n:
        ax3d.scatter(P3[:, 0], P3[:, 1], P3[:, 2], c=phi_g, cmap="magma",
                     vmin=0, vmax=phi_max, s=dimensione_nodi, alpha=1.0,
                     edgecolors="white", linewidths=0.25)
    ax3d.view_init(elev=26, azim=-60)
    ax3d.set_xlim(-r_grafo_3d, r_grafo_3d); ax3d.set_ylim(-r_grafo_3d, r_grafo_3d)
    ax3d.set_zlim(-r_grafo_3d, r_grafo_3d)
    ax3d.set_axis_off()
    ax3d.set_title("RETE DINAMICA 3D · pozzo fisico\ncolore nodi = phi_g",
                   fontsize=9, color="#0277bd")

    # Pannello destro: seconda proiezione, utile per seguire separazione e collasso dei nodi.
    if na:
        seg_yz = np.stack([P3[ii][:, 1:3], P3[jj][:, 1:3]], axis=1)
        lc_yz = LineCollection(seg_yz, cmap="plasma", linewidths=0.65, alpha=0.7)
        lc_yz.set_array(np.clip(dpozzo / dphi_max, 0.0, 1.0)); ax2.add_collection(lc_yz)
    if n:
        ax2.scatter(P3[:, 1], P3[:, 2], c=phi_g, cmap="magma", vmin=0, vmax=phi_max,
                    s=dimensione_nodi, alpha=1.0, edgecolors="white", linewidths=0.35)
    ax2.set_xlim(-r_grafo_3d, r_grafo_3d); ax2.set_ylim(-r_grafo_3d, r_grafo_3d)
    ax2.set_aspect("equal"); ax2.axis("off")
    ax2.set_title("RETE DINAMICA · pendenza del pozzo\ncolore archi = |Δphi_g|",
                  fontsize=9, color="#0277bd")

    # Pannello metriche: stessi indicatori principali della vista campo.
    righe = [
        ("VISTA RETE", 14, "#0277bd", "bold"),
        ("stessa dinamica · stesso stato", 9, "#7b1fa2", "normal"), ("", 8, "#000", "normal"),
        (f"puntatori: {net.n} / {MAX_NODI}", 10, "#111", "normal"),
        (f"archi:     {len(net.i)}", 10, "#111", "normal"), ("", 8, "#000", "normal"),
        (f"phi_g: {phi_g.min() if n else 0:.3g} .. {phi_g.max() if n else 0:.3g}",
         10, "#7b1fa2", "normal"),
        (f"|Δphi_g| max: {dphi_max:.3g}", 10, "#7b1fa2", "normal"),
        ("— GEOMETRIA VIVA —", 10, "#7b1fa2", "bold"),
        (f"d medio:     {dg['d_med']:.3f}", 10, "#7b1fa2", "normal"),
        (f"dilatazione: {100 * dg['dil']:+.1f}%", 10, "#7b1fa2", "normal"),
        (f"stress:      {100 * dg['stress']:+.2f}%", 10, "#7b1fa2", "normal"), ("", 8, "#000", "normal"),
        ("— TOPOLOGIA —", 10, "#0277bd", "bold"),
        (f"torsione max: {dg['tw']:.1f} / {(3*np.pi if TORS_4PI else PHI_CRIT):.1f}", 10, "#0277bd", "normal"),
        (f"mitosi: {net.nati}  (negate {net.negate})", 10, "#0277bd", "normal"),
        (f"entro portata: {100 * dg['entro']:.0f}%", 10, "#0277bd", "normal"),
    ]
    y = 0.97
    for txt, sz, col, wt in righe:
        if txt: axt.text(0, y, txt, fontsize=sz, color=col, weight=wt, va="top")
        y -= 0.042 if txt else 0.018
    axc.text(0.5, 0.5, "VISTA RETE · premere N o usare --vista-campo per tornare alla vista attuale",
             ha="center", va="center", fontsize=11, color="#0277bd", weight="bold")


def _render_grafo_topologico(net, dg):
    """Visualizza solo la topologia: il layout non usa le coordinate XYZ.

    Le coordinate sul pannello sono un supporto grafico astratto; la fisica mostrata
    sui nodi e sugli archi resta quella del pozzo `phi_g` e della sua pendenza.
    """
    from matplotlib.collections import LineCollection

    n = net.n
    if n == 0:
        ax.set_title("GRAFO TOPOLOGICO · vuoto", fontsize=11, color="#0277bd")
        return
    phi_g, valid, dpozzo_tutti = net.pozzo_grafo()
    grado = np.bincount(np.concatenate([net.i[valid], net.j[valid]]),
                        minlength=n) if np.any(valid) else np.zeros(n)

    # Layout astratto: seleziona i nodi più connessi/densi solo per rendere leggibile
    # una rete enorme. La posizione sul pannello NON è net.pos e non entra nella fisica.
    limite = 2800
    punteggio = np.log1p(grado) * (1.0 + phi_g / max(float(phi_g.max()), 1e-12))
    sel = np.argsort(punteggio)[-min(n, limite):]
    sel = np.sort(sel)
    presente = np.zeros(n, dtype=bool); presente[sel] = True
    ang = 2.0 * np.pi * np.arange(len(sel)) / max(len(sel), 1)
    raggio = 1.0 + 0.18 * np.log1p(grado[sel]) / max(np.log1p(grado[sel]).max(), 1.0)
    Q = np.column_stack([raggio * np.cos(ang), raggio * np.sin(ang)])
    indice = np.full(n, -1, dtype=int); indice[sel] = np.arange(len(sel))

    archi = valid & presente[net.i] & presente[net.j]
    ia = indice[net.i[archi]]; ja = indice[net.j[archi]]
    seg = np.stack([Q[ia], Q[ja]], axis=1) if len(ia) else np.zeros((0, 2, 2))
    dp = np.abs(dpozzo_tutti[np.flatnonzero(archi)]) if len(ia) else np.zeros(0)
    dpmax = max(float(dp.max()) if len(dp) else 0.0, 1e-12)
    phimax = max(float(phi_g[sel].max()), 1e-12)

    if len(seg):
        lc = LineCollection(seg, cmap="plasma", linewidths=0.7, alpha=0.72, zorder=1)
        lc.set_array(np.clip(dp / dpmax, 0.0, 1.0)); ax.add_collection(lc)
    ax.scatter(Q[:, 0], Q[:, 1], c=phi_g[sel], s=14 + 34 * np.sqrt(phi_g[sel] / phimax),
               cmap="magma", vmin=0, vmax=phimax, edgecolors="white", linewidths=0.3,
               zorder=3)
    ax.set_xlim(-1.35, 1.35); ax.set_ylim(-1.35, 1.35)
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_title("GRAFO TOPOLOGICO ASTRATTO · non XYZ\n"
                 f"frame {stato['nframe']} · nodi mostrati {len(sel)}/{n} · "
                 f"archi {len(net.i)} · colore = phi_g / |Δphi_g|",
                 fontsize=10, color="#0277bd", weight="bold")


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
        # [T1] UN SOLO ESECUTORE: l'ordine e le fasi stanno in `PASSO_COMPOSIZIONE`, non
        #   ricopiati qui. Era il 26esimo posto in cui quell'ordine viveva cablato.
        esegui_passo(net)
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
        # La superficie deve usare ESATTAMENTE il pozzo fisico discreto phi_g.
        # Non si ricalcola una seconda sorgente continua e non si applica smoothing
        # globale: si interpola soltanto il valore gia' usato da GRAV_BIFASE.
        phi_nodo, _, _ = net.pozzo_grafo(Iv)
        tree = cKDTree(Pn)
        k_interp = min(16, n0)
        dd, kk = tree.query(pts2d, k=k_interp)
        if k_interp == 1:
            dd = dd[:, None]; kk = kk[:, None]
        pesi = 1.0 / np.maximum(dd, 1e-9)
        phi_w = np.sum(pesi * phi_nodo[kk], axis=1) / np.maximum(pesi.sum(axis=1), 1e-9)
        phi_w = phi_w.reshape(GXm.shape)
        pm = float(np.max(phi_w)) if phi_w.size else 0.0
        # Scala istantanea: il rilievo deve riflettere la quantita' corrente, senza
        # memoria del rendering precedente che potrebbe nascondere un secondo pozzo.
        scala = max(pm, 1e-6)
        prof_scala = _scala_sistema() * 0.9
        Zdef = -prof_scala * np.sqrt(np.clip(phi_w / scala, 0, 1)) if pm > 0 else np.zeros_like(GXm)
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
    ax3d.set_title("POZZO FISICO DEL GRAFO\n(phi_g usato da GRAV_BIFASE · interpolazione grafica)",
                   fontsize=9, color="#7b1fa2")

    P = net.pos @ M                            # i puntatori ruotano col campo
    # RETE DINAMICA: stesso pannello della vista dei puntatori, cosi' GUI e video
    # mostrano nella stessa finestra la composizione topologica e la risposta del campo.
    # Gli archi sono colorati per torsione; i nodi per densita' di interferenza.
    if len(net.i):
        na = min(len(net.i), 24000)  # limite solo di rendering: non modifica la fisica
        ee = np.arange(na)
        seg = np.stack([P[net.i[ee], :2], P[net.j[ee], :2]], axis=1)
        from matplotlib.collections import LineCollection
        tw_render = np.abs(net.tw[ee]) if len(net.tw) >= na else np.zeros(na)
        tw_norm = np.clip(tw_render / max(PHI_CRIT, 1e-9), 0.0, 2.0)
        lc = LineCollection(seg, cmap="viridis", linewidths=0.25, alpha=0.32)
        lc.set_array(tw_norm)
        ax2.add_collection(lc)
    # TRASPARENZA AL VUOTO: l'opacita' di ogni puntatore e' proporzionale alla sua intensita'
    # d'interferenza. Le masse (alta intensita', la materia coerente) restano visibili; il vuoto
    # ribollente (bassa intensita') diventa quasi trasparente. Cosi' si vede la materia, non la
    # tempesta di fondo. Non cambia la fisica: e' solo resa. La soglia e' relativa (mediana).
    Ivis = net.intensita()[:net.n]
    Iref = max(float(np.median(Ivis)) * 3.0, 1e-9)     # scala relativa (materia >> vuoto)
    alpha_nodo = np.clip(Ivis / Iref, 0.03, 1.0)       # vuoto ~0.03 (quasi invisibile), masse ~1
    ax2.scatter(P[:net.n, 0], P[:net.n, 1], c=Ivis, s=7, cmap="magma",
                vmin=-1, vmax=1, alpha=alpha_nodo, linewidths=0)
    ax2.set_xlim(-R*1.12, R*1.12); ax2.set_ylim(-R*1.12, R*1.12)
    ax2.set_aspect("equal"); ax2.axis("off")
    ax2.set_title("rete dinamica · archi=twist · nodi=|Psi|²", fontsize=9, color="#444")

    # In vista rete il pannello principale diventa un layout puramente topologico;
    # il pannello 3D continua invece a mostrare il pozzo fisico calcolato dal campo.
    if VISTA_RETE:
        ax.clear()
        _render_grafo_topologico(net, dg)

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
    elif k in ("n", "N"):
        _toggle_vista_rete()


def _btn(x, y, lab, cb, w=0.105, h=0.045):
    b = Button(plt.axes([x, y, w, h]), lab, color="#eceff1", hovercolor="#cfd8dc")
    b.on_clicked(cb); b.label.set_fontsize(8); return b


def _zoom(v):
    def _f(_=None): stato["zoom"] = float(np.clip(stato["zoom"] * v, 0.3, 4))
    return _f


def _pausa(_=None): stato["pausa"] = not stato["pausa"]


def _toggle_vista_rete(_=None):
    global VISTA_RETE
    VISTA_RETE = not VISTA_RETE
    print("[VISTA]", "RETE" if VISTA_RETE else "CAMPO")


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
    BOTTONI.append(_btn(0.674, 0.115, "vista rete", _toggle_vista_rete, w=0.10))
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
    global SCUOTIMENTO
    global MAX_NODI, P_LAM, TAU_LOC, ZETA_M, HAM_SRC, ALPHA_NAT, DIFF_RES, PLAST_MIT, ZETA_LOC, VERLET, ELAST_C, PLAST_DIN, GUSCIO_MORBIDO
    global TAU_LUCE, RUMORE_COLORATO
    global MITOSI_2LAM     # [CURA 5] senza questo l'assegnazione sarebbe una LOCALE, inerte
    global CONTRASTO_INTENSIVO   # [INERZIA-1(C)] idem: senza `global` il flag nasce MORTO,
    #   ed e' esattamente come `--semina-matura` e `--mitosi-2lam` sono stati inerti per un
    #   giorno intero, con i loro sigilli che PASSAVANO (li accendevano sul modulo).
    global SEMINA_MATURA   # [CURA 4] senza questo l'assegnazione sarebbe una LOCALE, inerte
    global TAU_A      # [ESPERIMENTO --tau-a] senza questo l'override sarebbe una LOCALE, cioe' INERTE IN SILENZIO
    global COPPIA_RECIPROCA, GRAV_AMPIEZZA
    global PEQ_ESATTO, PEQ_NASCITA_LOCALE, SCALA_MIN_PASSO, COES_CAUSALE, ANOM_SIMM
    global CONTROLLO_REGISTRO   # [RIPIEGHI-ZERO] senza la `global` l assegnamento sotto
    #   creerebbe una LOCALE e il flag nascerebbe MORTO -- e' il difetto documentato di
    #   `--tau-a`, `--semina-matura` e `--mitosi-2lam`, inerti per un giorno intero coi
    #   loro sigilli che PASSAVANO.
    global INVARIANTI
    global SEMINA_LAM
    global TEMPO_UNICO_MITOSI, POZZO_D
    global COPPIA_MIT, MU_PSI, MITMAX, GAMMA, LAM, SCALA_B, SCALA_AMP, TAU_USA_D0, CALORE_VETTORIALE, K_FRANGE, VIRIALE, CHI_BASC, ZETA_VIR, PAV_COM, SYNC_UPDATE, VERSO_CHI, LS_AZIM, POLO_MATURO, OLON_PART, SPINORE_VIVO, SPIN_LARMOR, SPIN_FEEDBACK, SPIN_POSITIVI, CHI_CORE, CS_DINAMICO, VISTA_RETE, TW_SPINORE, SPINORE_CORRETTO, CHI_DA_SPINORE, CHI_COOP, SCALA_MIN, COES_ADIM, RITMO_WRAP_2PI, TEMPO_PROPRIO_ORIENTATO, SYNC_SPINORE, DEPARAM_OROLOGIO, SYNC_FASE_OROLOGIO, KURAMOTO_SU2, DT, CAMPO_SPINORIALE, TEMPO_SEGNO, OROLOGIO_SEGNO, FORK_SU2, FORK_SU2_MEM, STEP2_OROLOGIO, GAMMA_TURBO
    if getattr(a, "dt", None) is not None:
        DT = float(a.dt); print(f"[dt] passo di tempo coordinata DT={DT} (test di convergenza; con dt/2 raddoppia --passi)")
    if getattr(a, "tau_d0", False):
        TAU_USA_D0 = True
        print("[tau] tau_p locale usa d0 (distanza di riposo) invece di d reale: forma piu' stabile")
    if getattr(a, "scuotimento", False):
        SCUOTIMENTO = True   # forza lo scuotimento del vuoto ON anche in regime deterministico (default off = segue il regime)
        print("[scuotimento] ribollio del vuoto FORZATO ON (regime deterministico + scuotimento): il vuoto ribolle ma la dinamica resta deterministica")
    if getattr(a, "calore_vett", False):
        CALORE_VETTORIALE = True
        print("[calore] calcio termico VETTORIALE+chirale attivo: omega_s 3D eccitato, phivel firmato da perc_chi")
    if getattr(a, "calore_scal", False):
        CALORE_VETTORIALE = False
        print("[calore] calcio termico SCALARE isotropo forzato (vettoriale spento per confronto)")
    MAX_NODI = a.maxnodi
    P_LAM = 1.0  # compatibilita' CLI: il valore passato a --plam non agisce piu' sulla fisica
    TAU_LOC = a.tauloc
    ZETA_M = a.zeta
    ZETA_LOC = bool(getattr(a, "zeta_loc", False))   # smorzamento locale (legge): default off = non-regressione
    VERLET = bool(getattr(a, "verlet", False))       # integratore metrico sperimentale: default off
    GUSCIO_MORBIDO = bool(getattr(a, "guscio_morbido", False))   # diffusione di superficie delle d0: default off
    if getattr(a, "tau_a_over", None) is not None:
        # A8: il ramo e' CONTATO -- qui basta un marcatore sul modulo, letto dal sigillo.
        TAU_A = float(a.tau_a_over)
        globals()["_TAU_A_OVERRIDE"] = TAU_A
        print(f"[tau-a] ESPERIMENTO: TAU_A sovrascritto a {TAU_A} (default del regime "
              f"'{REGIME}': {_TAU_A_REGIME}). NON e' una correzione, NON e' promosso, e la "
              f"combinazione TAU_A={TAU_A} con G_PH={G_PH} NON e' mai stata validata.")
    if getattr(a, "elast_c", None) is not None:
        ELAST_C = float(a.elast_c)
        print(f"[elast] ATTENZIONE: --elast-c e' un NO-OP DICHIARATO dal 2026-09-17. ELAST_C={ELAST_C} "
              f"e' impostato ma NON E' LETTO da nessun percorso fisico: la plasticita' usa ora "
              f"tau_p = max(d/cs, (d/cs)*rho_arco/peq), che non ha coefficienti. Il valore non ha effetto.")
    HAM_SRC = a.ham
    ALPHA_NAT = a.alfanat
    DIFF_RES = a.diffres
    PLAST_MIT = a.plastmit
    PLAST_DIN = bool(getattr(a, "plast_din", False))  # plasticita' metrica dinamica: default off
    COPPIA_MIT = a.coppia
    MU_PSI = a.mupsi
    GAMMA = a.gamma
    LAM = a.lam
    MITMAX = a.mitmax
    K_FRANGE = a.kfrange   # canale ORBITALE tangenziale (moto lungo le frange). 0 = spento (non-regressione)
    VIRIALE = bool(getattr(a, "viriale", False))   # conversione viriale (legge): default off = non-regressione
    GRAV_AMPIEZZA = bool(getattr(a, "grav_ampiezza", False))      # ampiezza nella correzione grav: default off = byte-identico
    COPPIA_RECIPROCA = bool(getattr(a, "coppia_reciproca", False))  # reciprocita' del torque spinoriale: default off = byte-identico
    CHI_BASC = bool(getattr(a, "chi_basc", False)) # basculamento chirale (legge): default off = non-regressione
    ZETA_VIR = bool(getattr(a, "zeta_vir", False)) # freno anisotropo (legge): default off = non-regressione
    PAV_COM = bool(getattr(a, "pav_com", False))   # pavimento comovente (legge): default off = muro assoluto 0.05
    SYNC_UPDATE = bool(getattr(a, "sync", False)) # aggiornamento sincrono (transazionale): default off
    # [PROMOZIONE 2026-09-18] ON di default come PREREQUISITO di SPIN_FEEDBACK (vedi :704).
    # `--spinore-vivo` resta accettato come NO-OP DICHIARATO (non rompe i comandi gia' scritti);
    # il braccio OFF e' `--senza-spinore-vivo`, che e' un DIAGNOSTICO.
    SPINORE_VIVO = not bool(getattr(a, "senza_spinore_vivo", False))
    SPIN_LARMOR = bool(getattr(a, "spin_larmor", False))   # campo trasverso geometrico (Larmor): default off
    # [CURA 1a, APPROVATA da Luca 2026-09-24] Il wrap del ritmo sul periodo GIUSTO.
    #   `D34` e' DIMOSTRATO sulla formula (`max|w4(a) - a| = 0.000e+00` su 100 001 punti:
    #   un wrap su `4pi` applicato a una differenza di `np.angle`, che ha periodo `2pi`,
    #   e' l'IDENTITA' e non avvolge niente). Sigillo `_sigillo_ritmo_wrap.py` 4/4, prova
    #   a 600 passi `Z123`. FINO A OGGI ERA ACCENDIBILE SOLO IN-PROCESS: senza opzione, il
    #   driver non poteva accenderla, e una cura che nessun run accende e' un ramo morto.
    RITMO_WRAP_2PI = bool(getattr(a, "ritmo_wrap_2pi", False))  # cura D34: default off, il driver la accende
    POZZO_D = bool(getattr(a, "pozzo_d", False))        # [D02] default SPENTO
    # [CURA 2 STRUTTURALE, 2026-09-27] L'ASSEGNAZIONE E' TOLTA: la legge non si spegne.
    #   `--tempo-unico-mitosi` resta ACCETTATA come NO-OP dichiarato (il driver la passa
    #   in ogni run, e ogni comando gia' scritto la contiene), e AVVISA.
    if getattr(a, "tempo_unico_mitosi", False):
        print("[tempo-unico-mitosi] NO-OP DICHIARATO dal 2026-09-27: la `CURA 2` e'"
              " STRUTTURALE e i rami a flag spento sono USCITI dal simulatore."
              " Il braccio OFF vive al tag `pre-cura2-strutturale`;"
              " i rami in csv/_archivio/rami_off_cura2.py.")
    # [CURA 4 e CURA 5] QUI, dove sta il `global`. Prima erano in `esegui_headless`, cioè
    #   in un'altra funzione, quindi LOCALI e INERTI: i flag da riga di comando erano MORTI.
    SEMINA_MATURA = bool(getattr(a, "semina_matura", False))   # [CURA 4]
    if SEMINA_MATURA:
        print("[cura4] SEMINA_MATURA ON: i nodi della semina iniziale nascono MATURI, e la "
              "rampa usa `_tempo_luce_nodo` invece di TAU_A (che resta la sola vita media "
              "spinoriale).")
    MITOSI_2LAM = bool(getattr(a, "mitosi_2lam", False))       # [CURA 5]
    # ### L'AVVISO `[cura5]` E' TOLTO, e il motivo e' che DIREBBE IL FALSO: annunciava
    #   *<<MITOSI_2LAM ON: un arco si divide SOLO se d >= 2 LAM>>* ### **come se fosse il
    #   flag a deciderlo.** Dal `6b` la legge vale ### **sempre**, e il flag e'
    #   ### **inerte**: l'annuncio lo dà ora il blocco `[flag-inerti]`, che e' il posto
    #   dove questo repo dichiara i flag che non fanno niente (come `PAV_COM`).
    CONTRASTO_INTENSIVO = bool(getattr(a, "contrasto_intensivo", False))  # [INERZIA-1(C)]
    if CONTRASTO_INTENSIVO:
        print("[inerzia-1C] IL CONTRASTO E' PER VICINO: rho_s normalizzato sullo STESSO "
              "conteggio di vicini che peq_nodo usa come denominatore. Coppia e inerzia "
              "scalano allo stesso modo; rho_s NON cambia altrove (cura LOCALE).")
    SEMINA_LAM = bool(getattr(a, "semina_lam", False))  # cura della semina: default off
    TW_SPINORE = bool(getattr(a, "tw_spinore", False))     # torsione 4pi -> Bloch (doppia copertura): default off
    # [CURA 1b, decisione di Luca 2026-09-24] IL PONTE INVERSO E' IMPEDITO, non sconsigliato.
    # `TW_SPINORE` fa scrivere lo SPINORE dalla TORSIONE: `tw` -> `omega_s` -> `_psi_spinor`
    # (`:3090-3100`, e la conseguenza a `:3264`). Sono le UNICHE DUE occorrenze della classe
    # `INVERSA` su 139 punti della mappa del `4pi` (`csv/_test_fork/_diag_D/MAPPA_4PI.md`):
    # il `4pi` di `_psi_spinor` e' VERO (spin 1/2), quello di `phi` da cui `tw` prende la
    # scala e' una CONVENZIONE del codice. Quindi il finto comanda il vero, ed e' il
    # contrario della freccia causale del par.4: «i nodi guidano, gli archi ricordano».
    # NON SI CANCELLA IL RAMO (par.10: il codice di una legge esclusa resta, ed e' l'evidenza
    # che spiega perche' esiste il suo sostituto -- `TW_SPINORE` esiste perche' `SPIN_LARMOR`
    # fallisce). E NON BASTA IL DEFAULT SPENTO: era gia' spento e non ha impedito nulla (`A9`).
    # NON RITIRA NULLA: `TW_SPINORE = False` in 9 run su 11 ricostruibili e `--tw-spinore` non
    # compare in nessun lanciatore committato (`csv/_test_fork/_RICOSTRUZIONE_config.txt`).
    if TW_SPINORE:
        raise SystemExit(
            "[tw-spinore] RIFIUTO DI PARTIRE: e' il ponte inverso.\n"
            "  La torsione `tw` prende la sua scala da `phi`, il cui dominio `4pi` e' una\n"
            "  CONVENZIONE del codice; lo spinore ha il `4pi` VERO (spin 1/2). Con questo\n"
            "  flag il finto scrive il vero: tw -> omega_s -> _psi_spinor (:3090-3100).\n"
            "  E' il contrario della freccia causale del par.4 di CLAUDE.md.\n"
            "  Vedi doc/REGISTRO_FISICA.md, scheda 8 `torsione-spinore`, e\n"
            "  doc/REFERTO_tw_spinore.md (il commento della legge e' falso: dichiara un\n"
            "  ANGOLO `tw/2` e somma una VELOCITA' angolare -- fattore 628.3 = 2pi/DT).\n"
            "  Per riaprirlo serve una decisione di Luca, non la rimozione di questa riga.")
    SPINORE_CORRETTO = bool(getattr(a, "spinore_corretto", False)) # master: orologio proprio + spinore primario complesso
    CHI_DA_SPINORE = bool(getattr(a, "chi_da_spinore", False))     # flag 3: perc_chi da doppia-copertura di _psi_spinor
    TEMPO_PROPRIO_ORIENTATO = bool(getattr(a, "tempo_proprio_orientato", False)) # flag 4: r con segno (toglie |.|)
    SYNC_SPINORE = bool(getattr(a, "sync_spinore", False))         # Kuramoto SU(2) sugli spinori: default off
    SCALA_MIN = bool(getattr(a, "scala_min", False))               # nessuna lunghezza sotto LAM
    COES_ADIM = bool(getattr(a, "coes_adim", False))               # coesione adimensionale e causale
    PEQ_ESATTO = bool(getattr(a, "peq_esatto", False))             # rilassamento esatto di peq (C1)
    PEQ_NASCITA_LOCALE = bool(getattr(a, "peq_nascita_locale", False))  # nascita locale di peq (C2)
    SCALA_MIN_PASSO = bool(getattr(a, "scala_min_passo", False))   # freno una volta per passo (C3)
    # [RIPIEGHI-ZERO] il DEFAULT E ACCESO: il flag SPEGNE, non accende. Scritto cosi perche
    #   una cura inerte a default non e una cura, e il sigillo ha bisogno di poterla
    #   spegnere DAL CLI (H-P3: un sigillo non configura il modulo a mano).
    CONTROLLO_REGISTRO = not bool(getattr(a, "senza_controllo_registro", False))
    COES_CAUSALE = bool(getattr(a, "coes_causale", False))         # coesione causale (C4)
    ANOM_SIMM = bool(getattr(a, "anom_simm", False))               # anomalia simmetrica (C1-bis)
    INVARIANTI = (str(getattr(a, "invarianti", "on")).lower() != "off")   # gli invarianti (C5)
    CHI_COOP = bool(getattr(a, "chi_coop", False))                 # cooperazione: chi_basc -> perc_geom, spinore -> perc_chi
    if CHI_DA_SPINORE and not SPINORE_CORRETTO:
        raise SystemExit("[errore] --chi-da-spinore richiede --spinore-corretto (senno' loop di feedback perc_chi->spinore->perc_chi)")
    if CHI_COOP and not SPINORE_CORRETTO:
        raise SystemExit("[errore] --chi-coop richiede --spinore-corretto (lo scrittore della carica e' il segno di doppia copertura di _psi_spinor)")
    if SPINORE_CORRETTO and not SPINORE_VIVO:
        raise SystemExit("[errore] --spinore-corretto richiede --spinore-vivo (il settore SU(2) dev'essere nel percorso vivo)")
    if SPINORE_CORRETTO:
        print("[spinore-corretto] MASTER: orologio proprio de Broglie + spinore primario complesso _psi_spinor (evaluate-then-commit, |psi|=1)")
    if CHI_DA_SPINORE:
        print("[chi-da-spinore] perc_chi dal segno di doppia-copertura di _psi_spinor (post-commit); CHI_BASC disattivato")
    if SCALA_MIN:
        print("[scala-min] NESSUNA LUNGHEZZA SOTTO LAM: non si rimappa il valore, si SMORZA LA "
              "DISCESA -- incremento >= 0 intatto bit per bit, incremento < 0 moltiplicato per "
              "max(0, 1-LAM/x). I sette pavimenti di d0 SPARISCONO; le nascite partono da LAM; "
              "per d la regola va sull incremento del Verlet. Zero coefficienti.")
    if not INVARIANTI:
        print("[invarianti] *** SPENTI su richiesta (--invarianti=off). Il programma NON si "
              "fermera' quando una grandezza esce dal suo dominio fisico. Serve a RIGIOCARE i "
              "run delle epoche 1 e 2, che violano regole oggi note (il peq negativo al passo "
              "1126) e che si vogliono riprodurre COM'ERANO. ***")
    else:
        # LIVELLO NUMERICO: un'eccezione con la RIGA ESATTA, invece di un `nan` che viaggia.
        # ⚠ L'UNDERFLOW **NON** si ferma: densita' come `1e-81` di un nodo neonato sono
        #   LEGITTIME. Si conta e basta.
        np.seterr(over='raise', divide='raise', invalid='raise', under='ignore')
        print("[invarianti] ACCESI (default). DUE LIVELLI: NUMERICO -- overflow, divisione per "
              "zero e valori non validi alzano un'eccezione con la riga esatta; l'UNDERFLOW NON "
              "ferma niente, perche' densita' come 1e-81 di un nodo neonato sono LEGITTIME. "
              "FISICO -- ogni grandezza di stato dentro il suo dominio, a fine passo, con gli "
              "INDICI e i valori. L'esplosione del 21/9 NON era un overflow (1.8e6 e' un numero "
              "normale): l'avrebbe presa solo la regola FISICA `peq >= 0`. Legge soltanto: su "
              "un run sano non cambia un bit.")
    if ANOM_SIMM:
        print("[anom-simm] L'ANOMALIA SIMMETRICA, SENZA PAVIMENTO: "
              "anom = 2*(rho-peq)/(rho+peq), con `0/0 := 0` DEFINITO (precedente: scala_p, "
              "Z67). Toglie il pavimento max(peq,1e-9), che e' un numero SCELTO e non esprime "
              "nessun vincolo fisico (A11): con peq negativo RIBALTAVA IL SEGNO e moltiplicava "
              "per 3.7e5 (Z94). Il caso peq->0 con rho ordinario passa da 1e+08 a ESATTAMENTE "
              "+2, e per anomalie piccole le due forme coincidono. "
              "*** RICHIEDE --peq-esatto: con peq < 0 il denominatore si annulla in peq = -rho "
              "ed e' un POLO, non un limite. Senza C1 questa cura sostituisce un pavimento con "
              "un polo. Il caso e' CONTATO, non assunto impossibile. ***")
        if not PEQ_ESATTO:
            print("[anom-simm] *** AVVISO GRAVE: --anom-simm SENZA --peq-esatto. `peq` puo' "
                  "andare negativo (Z94 lo ha misurato a -4.85e-04) e li' la forma simmetrica "
                  "HA UN POLO. Configurazione DICHIARATAMENTE non sicura. ***")
    if COES_CAUSALE:
        print("[coes-causale] LA COESIONE RISPETTA L'ISTANTE E IL CONO LOCALE: `d0` e `d` si "
              "leggono dalla fotografia di INIZIO PASSO invece che da un `d0` gia' spostato da "
              "sette scritture, e il tetto e' `cs_arco*DT` col `cs` del nodo PIU' LENTO invece "
              "di `LAM*sqrt(K_C)*DT`, che e' costruito su costanti di modulo e non conosce il "
              "cono del luogo (A5). Zero parametri: `_cs_nodo_prev` esiste gia'. NB: il tetto "
              "locale non e' sempre piu' stretto -- dove il cono e' veloce ALLARGA -- ed e' "
              "causalita', non prudenza.")
    if SCALA_MIN_PASSO:
        print("[scala-min-passo] IL FRENO UNA VOLTA PER PASSO: le sei scritture di `d0` e i "
              "sotto-passi di `d` NON frenano piu'; a fine passo si applica `_smorza` UNA "
              "VOLTA sulla VARIAZIONE TOTALE, dal valore di INIZIO passo. Cura il CRICCHETTO "
              "di Z91: frenare ogni scrittura separatamente rende il risultato dipendente "
              "dall'ORDINE delle leggi e, poiche' frena solo le discese, con spinte opposte di "
              "somma nulla NON da' zero. Applicato una volta sola sul totale il bias e' ZERO "
              "ESATTO. Lo snapshot di inizio passo segue la mitosi ai quattro siti di "
              "ristrutturazione; gli archi NATI nel passo non vengono frenati, e le nascite "
              "restano a LAM. Zero coefficienti.")
    if PEQ_NASCITA_LOCALE:
        print("[peq-nascita-locale] UNA SOLA LEGGE DI NASCITA PER `peq`: gli archi della "
              "creazione di coppia alla Schwinger nascono con `nan` e vengono CALIBRATI da "
              "step() sulla `rho` DEL LORO ARCO, esattamente come quelli di `_allaccia`. "
              "Prima prendevano `median(peq)`, LA MEDIANA GLOBALE: una statistica globale "
              "dentro una legge locale (A2), e quei nodi non hanno alcun rapporto con la "
              "mediana della rete. Zero parametri: il meccanismo esisteva gia'. L'eredita' "
              "della MITOSI non si tocca: un arco che si spezza non nasce, CONTINUA.")
    if PEQ_ESATTO:
        print("[peq-esatto] IL RILASSAMENTO DI `peq` IN FORMA ESATTA: "
              "peq <- rho + (peq-rho)*exp(-dt_e/tau_bg), piu' lo stesso passo esatto per la "
              "diffusione (splitting di Lie-Trotter, punto fisso `peq+flusso`). E' una "
              "COMBINAZIONE CONVESSA, quindi `min(peq,rho) <= peq_new <= max(peq,rho)` per "
              "QUALUNQUE passo: `peq` NON PUO' PIU' SCAVALCARE SOTTO ZERO. L'Eulero esplicito "
              "di prima scavalcava per dt_e/tau_bg > 1, misurato 1.2018 al passo 1126 del ramo "
              "D. Zero coefficienti nuovi: e' la stessa forma gia' imposta dal par.4 per i "
              "rilassamenti di primo ordine. NON toglie il pavimento di :4215.")
    if COES_ADIM:
        print("[coes-adim] COESIONE ADIMENSIONALE: i tre addendi normalizzati sulla densita' "
              "LOCALE dell'arco (I_med sparisce, era una media globale), e lo spostamento e' "
              "passo_causale * tanh(...) * filtro_portata, con |F| <= 1 PER COSTRUZIONE. "
              "Sostituisce il clip tanh(stress)*d0.")
    if CHI_COOP:
        print("[chi-coop] COOPERAZIONE: chi_basc SCRIVE perc_geom (geometria, letta dalla catena della "
              "torsione) e lo spinore scrive perc_chi (carica, letta dal campo B, dalla mitosi e da "
              "Schwinger). L'anello carica -> campo -> spinore -> carica e' quello NORMALE della "
              "fisica, sfasato di un passo.")
    if TEMPO_PROPRIO_ORIENTATO:
        print("[tempo-proprio-orientato] ritmo() con segno: r orientato (toglie |.| da f)")
    if SYNC_SPINORE:
        print("[sync-spinore] Kuramoto SU(2) sugli spinori: torque di allineamento omega_sync = forza*(nb x nb_media) in omega_tot")
    DEPARAM_OROLOGIO = bool(getattr(a, "deparam_orologio", False))  # de-param relazionale dell'orologio: default off
    if DEPARAM_OROLOGIO and not SPINORE_CORRETTO:
        print("[deparam-orologio] AVVISO: inerte senza --spinore-corretto (l'orologio de Broglie vive solo li').")
    if DEPARAM_OROLOGIO:
        print("[deparam-orologio] orologio RELAZIONALE: freq = coerenza d'arco intensiva (no |Psi|^2 estensiva, no rho_c globale, no volume)")
    SYNC_FASE_OROLOGIO = bool(getattr(a, "sync_fase_orologio", False)) # Kuramoto sul segno di doppia-copertura: default off
    if SYNC_FASE_OROLOGIO and not SPINORE_CORRETTO:
        print("[sync-fase-orologio] AVVISO: inerte senza --spinore-corretto (agisce sul segno di _psi_spinor); no-op.")
    if SYNC_FASE_OROLOGIO:
        print("[sync-fase-orologio] Kuramoto sul SEGNO di doppia-copertura: eta = dt*forza*sin(media_alpha-alpha), fase globale (nb invariante), O(dt^1)")
    KURAMOTO_SU2 = bool(getattr(a, "kuramoto_su2", False)) # Kuramoto SU(2) non-abeliano (spinore intero): default off
    if KURAMOTO_SU2 and not SPINORE_CORRETTO:
        print("[kuramoto-su2] AVVISO: inerte senza --spinore-corretto (agisce sullo spinore primario); no-op.")
    if KURAMOTO_SU2:
        print("[kuramoto-su2] Kuramoto SU(2) NON-ABELIANO: rotazione piena dello spinore verso la media SU(2) dei vicini (asse variabile nb x nb_bar), O(dt^1). nb SI muove (gravita' fisica, non 6.7e-16)")
    CAMPO_SPINORIALE = bool(getattr(a, "campo_spinoriale", False)) # [FASE 1] campo emesso dallo spinore: default off
    if CAMPO_SPINORIALE:
        print("[campo-spinoriale] FASI 1-3: campo Psi EMESSO dallo spinore (n,2) in calcola_psi; densita'/gravita' native (rho_spin, nb); FORZE = OVERLAP SPINORIALE <psi_i|psi_j> (coppia in step). Mitosi/coppie = Fase 4, ancora scalari. Riduzione-al-limite: spinore (e^{i phi},0) -> tutto scalare (sigilli 0.000e+00)")
    FORK_SU2 = bool(getattr(a, "fork_su2", False)) # [FORK SU(2) STRATO 0] arc-connection non-abeliana: default off
    if FORK_SU2 and not CAMPO_SPINORIALE:
        print("[fork-su2] AVVISO: inerte senza --campo-spinoriale (il trasporto agisce su _psi_spinor); no-op.")
    if FORK_SU2:
        print("[fork-su2] STRATO 0: la forza trasporta con N_ij/2 = cos(chi/2) U_ij in SU(2) (MESCOLA a,b -> non-abeliano). "
              "Peso = overlap di spin |<n_i|n_j>|, non una manopola. Allineati -> N/2=I -> riduzione ESATTA allo scalare; "
              "antipodali -> N=0. Bloch presi da _psi_spinor (gli stessi stati trasportati: connessione di Berry DI quegli stati).")
    FORK_SU2_MEM = bool(getattr(a, "fork_su2_mem", False)) # [FORK SU(2) STRATO 1] connessione con memoria: default off
    if FORK_SU2_MEM and not FORK_SU2:
        # SCELTA DOCUMENTATA: si IGNORA, non si forza FORK_SU2=True. Accendere da soli un meccanismo
        # che l'utente non ha chiesto violerebbe "un interruttore alla volta" (par.1); lasciare
        # FORK_SU2_MEM=True sarebbe invece uno stato INCOERENTE (memoria senza connessione su cui
        # vivere). Stessa convenzione dell'avviso --fork-su2 senza --campo-spinoriale qui sopra.
        print("[fork-su2-mem] AVVISO: richiede --fork-su2 (la memoria vive sulla connessione dello Strato 0). IGNORATO, flag riportato a OFF.")
        FORK_SU2_MEM = False
    if FORK_SU2_MEM:
        print("[fork-su2-mem] STRATO 1: la connessione N nasce dai Bloch RITARDATI n(t-tau), tau = d/cs (tempo-luce d'arco, "
              "zero parametri nuovi). ROMPE IL TEOREMA DI INERZIA dello Strato 0: psi(t) non e' autovettore di n(t-tau).sigma, "
              "quindi <psi_i|N|psi_j> != 2<psi_i|psi_j> e la FORZA CAMBIA. Rilassamento ESATTO alpha=1-exp(-dt/tau) con slerp "
              "geodetico sulla sfera (primo ordine, mai Verlet). A riposo o per tau->0 il ritardato torna al corrente -> "
              "riduzione allo Strato 0. Il TRASPORTO resta sugli spinori correnti.")
    # [PROMOSSO 2026-09-16] Default ON. `--step2-orologio` resta accettato (no-op, per non
    # rompere i comandi e gli script esistenti); `--senza-step2-orologio` lo spegne, ed
    # e' un DIAGNOSTICO, non fisica alternativa.
    STEP2_OROLOGIO = not bool(getattr(a, "senza_step2_orologio", False))
    if bool(getattr(a, "step2_orologio", False)):
        print("[step2-orologio] NB: --step2-orologio non serve piu', e' il DEFAULT dal "
              "2026-09-16 (par.10). Il flag resta accettato e non fa nulla.")
    if STEP2_OROLOGIO and not (CAMPO_SPINORIALE and DEPARAM_OROLOGIO):
        # Stessa convenzione degli altri avvisi: si IGNORA, non si forza. _phc vive nel ramo
        # --deparam-orologio; senza, non c'e' nulla da moltiplicare e il flag sarebbe incoerente.
        print("[step2-orologio] *** AVVISO GRAVE: lo STEP 2 e' FISICA DI DEFAULT dal 2026-09-16, "
              "ma richiede --campo-spinoriale + --deparam-orologio (l'orologio _phc vive li'). "
              "MANCANO, quindi e' SPENTO: questo run gira SENZA l'accoppiamento EM-metrica, "
              "cioe' su una fisica AMPUTATA rispetto al default. NON e' un'opzione: e' un "
              "prerequisito mancante. ***")
        STEP2_OROLOGIO = False
    if STEP2_OROLOGIO:
        print("[step2-orologio] STEP 2: omega_clk *= (cs/CS_M)^2 = OROLOGIO DI COMPTON (omega = m c^2/hbar, e nel modello c e' cs). "
              "Aggancia il tempo proprio dell'OROLOGIO a quello della METRICA, che erano scollegati. Zero parametri: a cs=CS_M il "
              "fattore e' 1 esatto. cs dal passo precedente (il settore metrico gira dopo). Tocca la MAGNITUDINE, mai il segno. "
              "NB: agisce sulla FASE (U(1)), NON sul Bloch: non organizza lo spin, e non deve.")
    TAU_LUCE = bool(getattr(a, "tau_luce", False))   # [FASE 2] rilassamento col tempo-luce d/cs: default off
    RUMORE_COLORATO = bool(getattr(a, "rumore_colorato", False))   # taglio spettrale: default off
    if RUMORE_COLORATO:
        print("[rumore-colorato] TAGLIO SPETTRALE: il calcio del vuoto non e' piu' bianco ma "
              "correlato su tau_c = LAM/CS_M = %.4g (= %.0f passi), con un processo di "
              "Ornstein-Uhlenbeck sul rumore stesso e `dt_n = DT*r` (non DT: e' un processo "
              "LOCALE). `amp` INVARIATA. MOTIVO: il rumore bianco discreto inietta a tutte le "
              "frequenze fino a Nyquist, incluse quelle che il passo non risolve; in natura non "
              "esiste. ZERO coefficienti: LAM e CS_M sono gia' nel sistema. "
              "ATTENZIONE: la ricorsione PRESERVA LA VARIANZA, quindi NON abbassa theta - se lo "
              "muove lo fa SALIRE (<=5%%). Si cabla perche' il rumore bianco e' SBAGLIATO, non "
              "perche' risolva l'aliasing (doc/PREDIZIONE_taglio_spettrale.md)."
              % (LAM / max(CS_M, 1e-12), (LAM / max(CS_M, 1e-12)) / max(DT, 1e-12)))
        if not SCUOTIMENTO:
            print("[rumore-colorato] AVVISO: SCUOTIMENTO e' SPENTO, quindi il flag e' INERTE "
                  "(non c'e' nessun calcio da colorare).")
        # [(b)2, 2026-09-27] L'AVVISO E' CADUTO CON IL RAMO: diceva che il rumore colorato
        #   agisce <<solo sul percorso VIVO (`not SYNC_UPDATE`)>> e quindi sarebbe inerte
        #   sotto `--sync`. Ora il percorso vivo E' L'UNICO -- i rami di `SYNC_UPDATE` sono
        #   archiviati -- quindi il rumore colorato agisce SEMPRE e l'avviso non ha piu' oggetto.

    if TAU_LUCE:
        print("[tau-luce] Il rilassamento di omega_s usa tau = d_nodo/cs_nodo (`_tempo_luce_nodo`), lo "
              "STESSO tau dello Strato 1, al posto di TAU_A*max(dens/dens_rif, 0.05). MOTIVO: "
              "inerzia = T^2 = (d/cs)^2, quindi il tempo che COSTRUISCE l'inerzia e quello che la "
              "RILASSA devono essere lo stesso; oggi sono due diversi nella stessa equazione. Zero "
              "coefficienti, zero floor nuovi. NB: |omega|_eq va come sqrt(tau), quindi theta cala di "
              "~13x: UN ORDINE DI GRANDEZZA, NON la soluzione dell'aliasing.")
    GAMMA_TURBO = float(getattr(a, "gamma_turbo", 1.0) or 1.0)  # [DIAGNOSTICO] default 1.0 = byte-identico
    # NB: si legge `a.cs_dinamico` DAGLI ARGOMENTI, non il globale CS_DINAMICO: quest'ultimo viene
    # assegnato PIU' SOTTO (:4842), quindi qui varrebbe ancora il default False e il guard
    # scatterebbe SEMPRE, azzerando il turbo anche quando --cs-dinamico e' passato. Preso davvero il
    # 2026-09-14: il primo run K=300 e' girato a K=1 senza che nulla lo segnalasse, tranne un avviso
    # che diceva il falso. Leggere dagli argomenti toglie del tutto la dipendenza dall'ordine.
    if GAMMA_TURBO != 1.0 and not bool(getattr(a, "cs_dinamico", False)):
        # Stessa convenzione degli altri avvisi: si IGNORA, non si forza. Senza --cs-dinamico,
        # cs = CS_M costante: non c'e' nessuna sensibilita' da amplificare e il flag sarebbe muto.
        print("[gamma-turbo] AVVISO: richiede --cs-dinamico (senza, cs = CS_M costante e K non morde). IGNORATO, K riportato a 1.0.")
        GAMMA_TURBO = 1.0
    if GAMMA_TURBO != 1.0:
        print("[gamma-turbo] AMPLIFICATORE DIAGNOSTICO K = %.4g: dentro _cs_nodo si usa GAMMA*K = %.5g al posto di GAMMA = %.5g. "
              "OVUNQUE ALTROVE GAMMA resta ORIGINALE (satura() e la saturazione del campo spinoriale NON sono toccate). "
              "NON e' il percorso certificato. E' un ISOLAMENTO DIAGNOSTICO, NON il regime reale ad alta densita': "
              "con GAMMA condiviso cambierebbero ENTRAMBI. Un esito positivo si legge come CONDIZIONALE "
              "('il gradiente di cs, in isolamento, retroagisce'), non come affermazione sul regime reale. "
              "NB: la colonna cs_* del diaglog (:5318) re-implementa cs inline e NON e' turboata: non usarla."
              % (GAMMA_TURBO, GAMMA * GAMMA_TURBO, GAMMA))
    TEMPO_SEGNO = bool(getattr(a, "tempo_segno", False)) # MOD 5.3a+5.3b: verso dalla materia/antimateria coerente + magnitudine torsionale
    if TEMPO_SEGNO and not (CAMPO_SPINORIALE and SPINORE_CORRETTO):
        raise SystemExit("[errore] --tempo-segno richiede --campo-spinoriale + --spinore-corretto (il segno di doppia-copertura e la coerenza vivono li')")
    if TEMPO_SEGNO:
        print("[tempo-segno] MOD 5.3a+5.3b: VERSO del tempo = materia/antimateria COERENTE (Feynman-Stuckelberg, s_k=1+(perc_chi-1)*m_coer, vuoto avanti); MAGNITUDINE = torsione 1+|tw|/PHI_CRIT. Firma solo l'evoluzione interna; eta/geometria = magnitudine. Da stato t-1 (causale). OFF = byte-identico.")
    OROLOGIO_SEGNO = bool(getattr(a, "orologio_segno", False)) # MOD 5.3c: firma dell'orologio de Broglie interno _phc col segno stabile
    if OROLOGIO_SEGNO and not (CAMPO_SPINORIALE and SPINORE_CORRETTO):
        raise SystemExit("[errore] --orologio-segno richiede --campo-spinoriale + --spinore-corretto (l'orologio de Broglie interno _phc vive li')")
    if OROLOGIO_SEGNO and not DEPARAM_OROLOGIO:
        print("[orologio-segno] AVVISO: _phc (orologio pura-fase) vive nel ramo --deparam-orologio; senza di esso la firma e' INERTE (no-op). Aggiungere --deparam-orologio per attivarla.")
    if OROLOGIO_SEGNO:
        print("[orologio-segno] MOD 5.3c: VERSO dell'orologio de Broglie interno _phc firmato da s_k=sign(perc_chi) STABILE (materia exp-, antimateria exp+, tempi speculari); |omega_clk| INVARIATA (S3b: solo verso). Fase globale: tocca SOLO il segno, non nb/gravita'/eta. OFF/tutta-materia = esatto.")
    # [PROMOZIONE 2026-09-18] ON di default. `--spin-feedback` resta accettato come NO-OP
    # DICHIARATO (non rompe i comandi gia'scritti); il braccio OFF e' `--senza-spin-feedback`,
    # che e' un DIAGNOSTICO. E' la stessa forma della promozione di STEP2_OROLOGIO: quando si
    # ribalta un default si cercano TUTTI i punti che ottenevano il vecchio comportamento per
    # OMISSIONE, altrimenti i rami di controllo diventano duplicati del ramo di prova.
    SPIN_FEEDBACK = not bool(getattr(a, "senza_spin_feedback", False))
    # ⚠ AVVISO ESPLICITO SUL PREREQUISITO -- MAI UN NO-OP MUTO (P5/A8, lezione dello Step 2 e della
    # FASE 5 inerte al 95.33 % per mesi). Il ramo e' `if SPINORE_VIVO and SPINORE and SPIN_FEEDBACK`:
    # con `SPINORE_VIVO` False il feedback e' ACCESO MA NON GIRA, e senza questo avviso non lo
    # direbbe nulla -- il metodo non verrebbe nemmeno chiamato, quindi nemmeno i contatori A8
    # scatterebbero. Un flag acceso che non gira e' peggio di un flag spento.
    if SPIN_FEEDBACK and not (SPINORE_VIVO and SPINORE):
        # ⚠ il nome da stampare e' quello che CAUSA l'assenza, non quello che la risolveva PRIMA:
        # dal 2026-09-18 `--spinore-vivo` e' un NO-OP dichiarato, e a spegnere e' `--senza-spinore-vivo`.
        # Un avviso che indica il flag sbagliato manda chi legge a cercare la causa dove non e'.
        _manca = [_n for _n, _v in (("--senza-spinore-vivo (spegne SPINORE_VIVO)", SPINORE_VIVO),
                                    ("SPINORE (flag di modulo)", SPINORE)) if not _v]
        print(f"[spin-feedback] AVVISO: il feedback spinore->archi e' ON di default dal 2026-09-18, "
              f"ma il suo ramo richiede SPINORE_VIVO e SPINORE, e manca {_manca}. "
              f"IL FEEDBACK NON GIRA IN QUESTO RUN. Non e' un errore: e' dichiarato perche' un flag "
              f"acceso e inerte e' peggio di un flag spento.", flush=True)
    elif SPIN_FEEDBACK:
        print("[spin-feedback] ON di default (2026-09-18): prerequisiti presenti, il ramo GIRA. "
              "Acceso PER DECISIONE e su basi di FORMA (cricchetto curato 1.112 -> 6.5e-16; G6: "
              "fase CUCITA, cambi di segno 0.0035 contro nullo 0.50; sigillo 12/12), NON perche' "
              "una misura lo abbia mostrato migliore: l'A/B a quattro semi NON ha mostrato effetto.",
              flush=True)
    else:
        print("[spin-feedback] SPENTO da --senza-spin-feedback: DIAGNOSTICO, non fisica alternativa. "
              "Un run di misura con questo flag gira senza la retroazione spinore->archi, e va "
              "dichiarato nel documento che lo usa.", flush=True)
    SPIN_POSITIVI = bool(getattr(a, "spin_positivi", False)) # selezione diagnostica perc_chi=+1
    CHI_CORE = bool(getattr(a, "chi_core", False)) # chiralità emergente del core locale
    CS_DINAMICO = bool(getattr(a, "cs_dinamico", False)) # velocita' metrica locale: default off
    VISTA_RETE = bool(getattr(a, "vista_rete", False)) # rendering alternativo rete-only: default campo
    VERSO_CHI = bool(getattr(a, "verso_chi", False)) # aggancio al verso chirale stabile: default off
    LS_AZIM = bool(getattr(a, "ls_azim", False))   # L.S vettoriale azimutale: default off
    POLO_MATURO = bool(getattr(a, "polo_maturo", False)) # polo maturo (strategia 3): default off
    OLON_PART = bool(getattr(a, "olon_part", False)) # olonomia nella partizione: default off
    if VERLET:
        print("[verlet] integratore metrico Velocity-Verlet (2 ordine) attivo")
    if OLON_PART:
        print("[olon-part] la partizione tangenziale usa curl + twist coerente (verso -> conversione)")
    if POLO_MATURO:
        print("[polo-maturo] al twist partecipa la chiralita del polo che matura (twn maggiore)")
    if LS_AZIM:
        print("[ls-azim] L.S vettoriale: verso tangenziale da (radiale x spinore), azimutale stabile")
    if VERSO_CHI:
        print("[verso-chi] FRAME_DRAG pilotato dal verso CHIRALE stabile (non dal tw oscillante)")
    if SYNC_UPDATE:
        print("[sync] ⚠ NO-OP ACCETTATO dal 2026-09-27: i rami di SYNC_UPDATE sono "
              "ARCHIVIATI (csv/_archivio/_sync_update.py). Il flag NON FA NIENTE: il suo "
              "raggio era UNA legge su cinque. La sincronia del passo intero e' ETC-PASSO.")
    if PAV_COM:
        print("[pav-com] ⚠ FLAG INERTE dal 2026-09-27: il pavimento di d0 e' ARCHIVIATO "
              "(csv/_archivio/_pavimenti_morti.py) e questo flag NON FA NIENTE. La "
              "garanzia sulle lunghezze e' LAM (--scala-min-passo, --semina-lam).")
    if ZETA_VIR:
        print("[zeta-vir] freno anisotropo attivo: beta *= cos2 della viriale (dissipa radiale, libera tangenziale)")
    if CHI_BASC:
        print("[chi-basc] basculamento chirale attivo: perc_chi vira secondo la torsione locale vs PHI_CRIT (2pi)")
    if CHI_CORE:
        print("[chi-core] frame-dragging guidato dalla chiralità emergente del core locale")
    if CS_DINAMICO:
        print("[cs-dinamico] velocità metrica locale cs_eff(rho) con profilo tanh e CFL dinamico")
    # COARSE-GRAINING: se richiesta una scala > 1, applico le regole di scala derivate.
    SCALA_B = float(a.scala)
    fattore_lam, fattore_gamma, SCALA_AMP = _fattori_coarse(SCALA_B)
    LAM = a.lam * fattore_lam
    GAMMA = a.gamma * fattore_gamma
    if SCALA_B != 1.0:
        print(f"[scala] coarse-graining B={SCALA_B:.0f}: ogni solitone rappresenta "
              f"{SCALA_B:.0f} fini | lambda_eff={LAM:.3f} | gamma_eff={GAMMA:.4f} | "
              f"R_conn={3.0*LAM:.2f} (scala con lambda). NB: la regione FISICA di semina "
              f"resta la stessa — i blocchi occupano lo spazio dei fini, piu' grossolanamente.")
    # ⚠⚠ IL MONDO SI COSTRUISCE SEMPRE QUI, DOPO I FLAG -- MAI AL CARICAMENTO.
    #   (Decisione di Luca, 2026-09-21; diagnosi in `Z87`. CATEGORIA D del par.10: e' la CURA di
    #    un difetto, quindi NESSUN FLAG -- un bug curato non ha un interruttore.)
    #
    #   PRIMA questa ricostruzione era CONDIZIONATA a `--seed`/`--nodi` e nel caso normale NON
    #   SCATTAVA: sopravviveva il vuoto costruito all'`import` (`net = Rete(); net.semina(...)`),
    #   cioe' in un momento in cui OGNI flag da riga di comando e' ancora al suo default di
    #   MODULO. **OTTO grandezze che la semina legge erano percio' INERTI sul vuoto, in
    #   silenzio** -- trovate con la chiusura transitiva su 20 funzioni a partire da
    #   `semina`/`_allaccia`, non a occhio:
    #       CALORE_VETTORIALE, CAMPO_SPINORIALE, GAMMA, LAM, MAX_NODI, SCALA_AMP, SCALA_MIN, TAU_A
    #   Fra queste `LAM` fissa il raggio di connessione `R_CONN = 3*LAM` CON CUI IL VUOTO SI
    #   ALLACCIA, e `CALORE_VETTORIALE` decide il calcio termico ALLA NASCITA dei nodi.
    #
    # ⚠ I 300 PASSI E IL RILASSAMENTO RESTANO CONDIZIONATI, e NON e' una dimenticanza: la
    #   costruzione dell'import NON li faceva, quindi eseguirli sempre cambierebbe il mondo di
    #   partenza di OGNI run -- che e' l'opposto di cio' che questa cura vuole. Restano dov'erano.
    #   L'ASIMMETRIA E' DICHIARATA, non subita.
    net = Rete(a.seed if a.seed is not None else 42)
    # [SCENA-1, strada (1), decisione di Luca 2026-09-25] IL VUOTO DI DEFAULT E' LA
    #   SATURAZIONE, senza un numero. Con `SEMINA_LAM` acceso, chiedere `SEME_INIZIALE = 900`
    #   nodi in raggio `4.0` **RIFIUTA**: la saturazione vera e' `455`. E non si aggira con un
    #   numero, perche' **la capienza DIPENDE DAL SEME** (misurato: 12807/12783/12812/12790).
    #   `semina(-1)` chiede la SATURAZIONE: il numero lo decide la GEOMETRIA.
    #   ⚠ SOLO a flag ACCESO: a flag spento la saturazione NON ESISTE (senza distanza minima
    #     non c'e' un limite), e `semina` lo dice da se' rifiutando `n < 0`.
    # [DRIVER-SCENA-II, 2026-09-26] `--nodi 0` = **NESSUN VUOTO QUI: lo costruisce la SCENA.**
    #   Prima `a.nodi` era guardato SOLO a flag spento: con `SEMINA_LAM` il ternario andava in
    #   saturazione e `--nodi 0` chiedeva ZERO nodi ottenendone **455** (misura 0, `M0a`). La
    #   scena `(ii)` vuole UN SOLO VUOTO e rifiutava -- correttamente: il difetto era QUI.
    #   ⚠ E' UN'ECCEZIONE IN MENO, NON UNA LEGGE IN PIU' (`STANDARD 10`): `--nodi 0` significava
    #   «niente» a flag spento e «saturazione» a flag acceso, DUE significati per un valore.
    #   Ora e' UNO SOLO in entrambi i rami. *(A flag spento il comportamento non cambia di un
    #   bit: `semina(0)` ritornava subito da se'.)*
    if a.nodi:
        net.semina(-1 if SEMINA_LAM else a.nodi)
    # ⚠ E IL PRE-RILASSAMENTO NON GIRA SU UNA RETE VUOTA: 300 `step()` con `n = 0` non sono un
    #   rilassamento, sono un giro a vuoto -- e su una rete vuota non c'e' niente da rilassare.
    #   Il ramo con `net.n > 0` e' INVARIATO.
    if net.n and (a.seed is not None or a.nodi != SEME_INIZIALE):
        for _ in range(300): net.step()
        net.rilassa_disegno(30)


def esegui_headless(a):
    from matplotlib.animation import FFMpegWriter
    global net
    _applica_flag(a)
    # N MASSE nel video: passo numero e raggio allo scenario. Lo zoom seguira' lo scaling perche'
    # l'inquadratura R si adatta all'estensione reale dei nodi (vedi update: R = max|pos|).
    # [SCENA (ii)] `--mc-nodi 0` = SATURAZIONE (il default). Il braccio di controllo di
    # `P-GONFIA` passa qui il numero MISURATO dal braccio acceso, per avere lo STESSO `n`.
    # ❌❌ LE DUE ASSEGNAZIONI STAVANO QUI, E I FLAG ERANO MORTI. Il `global` è dichiarato in
    #   `_applica_flag`, ma le assegnazioni erano in `esegui_headless`: **due funzioni
    #   diverse**, quindi qui erano VARIABILI LOCALI e il flag di modulo restava `False`.
    #   **`--semina-matura` e `--mitosi-2lam` NON FUNZIONAVANO DA RIGA DI COMANDO.**
    #   ⚠ E I DUE SIGILLI PASSAVANO UGUALMENTE, perche' impostavano `S.SEMINA_MATURA = True`
    #   **direttamente sul modulo**: non hanno mai provato il percorso CLI.
    #   Trovato dal SIGILLO DEL DRIVER (`MITOSI_2LAM False/False` in NUDA e CAMPAGNA).
    #   ✅ Le assegnazioni sono ora in `_applica_flag`, dove sta il `global` e dove stanno
    #   tutti gli altri flag. **E il commento che avevo scritto accanto al `global` diceva
    #   esattamente questo rischio: «senza questo l'assegnazione sarebbe una LOCALE, cioè
    #   INERTE IN SILENZIO». L'ho scritto e poi l'ho fatto.**
    _MC_VIDEO["nodi"] = int(getattr(a, "mc_nodi", 0) or 0)
    _MC_VIDEO["fasi_casuali"] = bool(getattr(a, "mc_fasi_casuali", False))
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
    # DB nel VIDEO: se --sync-db e il file esiste, CARICA lo stato (sovrascrive la scena appena
    # creata) e renderizza IN AVANTI da li' - senza risimulare la formazione. Stessa protezione
    # hash-versione del batch. Utile: batch veloce col DB fino al punto interessante, poi video
    # corto che riparte da quello stato. (Il tracking-masse/didascalie puo' rietichettarsi;
    # il rendering dell'interferenza e' corretto.)
    import os as _os_v
    _db_v = getattr(a, "sync_db", None)
    if _db_v and _os_v.path.exists(_db_v):
        try:
            net.carica_stato(_db_v)
            print(f"[db-video] stato CARICATO da {_db_v}: renderizzo IN AVANTI da nodi={net.n}", flush=True)
        except RuntimeError as _e_v:
            print(f"[db-video] {_e_v}", flush=True); raise
    elif _db_v:
        print(f"[db-video] {_db_v} non esiste: renderizzo dalla formazione (nessuno stato da caricare)", flush=True)
    _cartella_video = _os_v.path.dirname(a.out) if a.out else ""
    if _cartella_video:
        _os_v.makedirs(_cartella_video, exist_ok=True)
    w = FFMpegWriter(fps=a.fps, bitrate=4000,
                     metadata=dict(title=f"Muratore di Planck - {a.test}"))
    print(f"[headless] test={a.test} frame={n} fps={a.fps} - tutte le leggi attive")
    _da_libera = bool(getattr(a, "da_libera", False))
    if _da_libera:
        print("[video] --da-libera: la formazione NON viene registrata, solo l'evoluzione libera", flush=True)
    with w.saving(fig, a.out, dpi=a.dpi):
        _registrando = not _da_libera
        _grabbed = 0
        _fmax = n + (3000 if _da_libera else 0)
        for f in range(_fmax):
            update(f)
            if not _registrando and (test.get("nome") is None or test.get("fase", 0) >= 1):
                _registrando = True
                print(f"[video] EVOLUZIONE LIBERA a frame {f}: inizio registrazione", flush=True)
            if _registrando:
                w.grab_frame(); _grabbed += 1
            if (f + 1) % 25 == 0:
                d = net.diagnostica()
                print(f"   f={f+1} reg={_grabbed}/{n} nodi={net.n} torsione={d['tw']:.1f} "
                      f"mitosi={net.nati} fase={test.get('fase')} nome={test.get('nome')}", flush=True)
            if _grabbed >= n:
                break
    print(f"[headless] scritto {a.out} ({_grabbed} frame registrati)")
    # [RIPIEGHI-ZERO, punto 2 di Luca] IL RENDICONTO DELLA TOLLERANZA, a fine run: una grandezza
    #   di STATO mai apparsa resterebbe fuori dal controllo PER SEMPRE, in silenzio.
    _mai = registro_mai_apparse(net)
    print("[registro] grandezze di STATO MAI apparse: %s"
          % (", ".join(_mai) if _mai else "NESSUNA (tutte e %d si sono viste piene)"
             % len(REGISTRO_STATO)))
    if _mai:
        print("[registro] *** NON E' UNA CURIOSITA', E' UN ESITO: o non esistono in questa "
              "configurazione, e vanno dichiarate DERIVATE col loro motivo misurato, oppure "
              "qualcosa non le crea mai -- e allora il registro dice il falso. ***")


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
    p.add_argument("--scuotimento", action="store_true", dest="scuotimento",
                   help="FORZA lo scuotimento del vuoto ON anche in regime deterministico (default off = "
                        "segue il regime: OFF in deterministico, ON in stocastico). La dinamica resta "
                        "deterministica, ma il vuoto ribolle (temperatura). Applicato dopo --regime.")
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
    p.add_argument("--dt", type=float, default=None,
                   help="passo di tempo coordinata (default DT=0.01). Per il TEST DI CONVERGENZA dt vs dt/2: "
                        "con dt/2 raddoppia --passi per lo stesso tempo fisico. Default None = invariato (byte-identico).")
    p.add_argument("--nodi", type=int, default=SEME_INIZIALE, help="puntatori del seme iniziale")
    p.add_argument("--maxnodi", type=int, default=MAX_NODI,
                   help="GUARDIA DI MEMORIA sui puntatori (la mitosi ne crea: serve margine). "
                        "Dal 2026-09-28 quando morde IL RUN SI FERMA con `LimiteNodiSuperato`: "
                        "non tronca piu' in silenzio. Se morde, si RIALZA questo numero.")
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
                   help="deprecato: mantenuto per compatibilita', ignorato dalla schermatura ancorata a N_c")
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
    p.add_argument("--grav-ampiezza", action="store_true", dest="grav_ampiezza",
                   help="UNA DIREZIONE NON E' UNA FORZA: moltiplica cross(_nb_grav, nb) per "
                        "_rho_sorgente(), l'ampiezza che _nb_grav() divide via. Oggi il termine e' "
                        "un VERSORE (|_nb_grav| = 1 ovunque) e rho compare SOLO al denominatore "
                        "dentro l'inerzia. Zero numeri nuovi, nessun tetto. OFF = byte-identico.")
    p.add_argument("--coppia-reciproca", action="store_true", dest="coppia_reciproca",
                   help="RECIPROCITA': pesa il torque spinoriale cross(_nb_grav, nb) per ramp[k], "
                        "lo STESSO peso che il nodo ha come sorgente. Cura l'asimmetria misurata "
                        "(un neonato non pesa ma riceve 4.9 volte la coppia di un maturo). "
                        "Zero numeri nuovi, nessuna soglia. OFF di default = byte-identico.")
    p.add_argument("--chi-basc", action="store_true", dest="chi_basc",
                   help="BASCULAMENTO CHIRALE (legge, zero parametri): la chiralita' dei nodi "
                        "vira secondo la torsione locale rispetto al quanto PHI_CRIT (2pi): "
                        "chi=+1 dove il giro e' completo (materia), -1 dove no (spazio). Rompe "
                        "la simmetria casuale dei +-pi. Default off = non-regressione.")
    p.add_argument("--zeta-vir", action="store_true", dest="zeta_vir",
                   help="FRENO ANISOTROPO (legge, zero parametri): lo smorzamento beta viene "
                        "moltiplicato per cos2 della viriale (pieno sul radiale, ->0 sul "
                        "tangenziale). Dissipa il moto radiale, lascia vivere la rotazione. "
                        "Usa la sin2/cos2 della viriale (serve --viriale). Default off.")
    p.add_argument("--verlet", action="store_true", dest="verlet",
                   help="INTEGRATORE metrico Velocity-Verlet (2 ordine) invece di Eulero (1). "
                        "Default off: il ramo canonico resta invariato.")
    p.add_argument("--plast-din", action="store_true", dest="plast_din",
                   help="PLASTICITA' METRICA DINAMICA (legge, zero parametri): alla mitosi il d0 "
                        "dei nuovi archi riceve un offset plastico emergente da stress metrico "
                        "|d-d0|/d0 ed eccesso di torsione (|tw|/PHI_CRIT-1), saturato via tanh e "
                        "non-negativo. Sostituisce PLAST_MIT statico. Default off = non-regressione.")
    p.add_argument("--tau-a", type=float, default=None, dest="tau_a_over", metavar="V",
                   help="ESPERIMENTO (par.10 categoria ESPERIMENTI, OFF di default): sovrascrive "
                        "TAU_A. NON E' UNA CORREZIONE e NON si promuove. Serve a rispondere a una "
                        "domanda: TAU_A = 50 nel ramo deterministico era una CURA (per non far "
                        "divergere omega) o una scelta scaduta? Con --tau-a 2.0 si ottiene una "
                        "TERZA combinazione, mai validata: il 2.0 e' il valore 'canonico', ma il "
                        "canonico vuole anche G_PH = 0.15, e QUI G_PH resta 3e-3. "
                        "Il ramo deterministico e' gia' vicino al limite di divergenza (il suo "
                        "commento dice: '1e-4 e 0 divergono'), e TAU_A e' l'altro parametro dello "
                        "stesso equilibrio. Se diverge, e' un RISULTATO.")
    p.add_argument("--elast-c", type=float, default=None, dest="elast_c",
                   help="NO-OP DICHIARATO dal 2026-09-17: ELAST_C non e' piu' letto da nessun "
                        "percorso fisico (la plasticita' usa la forma viscoelastica causale). "
                        "Il flag resta accettato per non rompere gli script gia' scritti, e "
                        "STAMPA UN AVVISO. "
                        "Coefficiente del nucleo elastico (default storico 100). 0 = spento; "
                        "30/100/300 = test di sensibilita'.")
    p.add_argument("--guscio-morbido", action="store_true", dest="guscio_morbido",
                   help="DIFFUSIONE DI SUPERFICIE delle d0 (legge, zero parametri): aggiunge D*lap(d0) "
                        "con D = c_locale * spaziatura d'arco. Smussa SOLO il guscio (bordo ripido), "
                        "non il nucleo (lap ~0 dove uniforme). Clamp causale CFL. Default off (identico).")
    p.add_argument("--pav-com", action="store_true", dest="pav_com",
                   help="PAVIMENTO COMOVENTE (legge, zero parametri): il pavimento di d0 diventa "
                        "median(d0)-MAD(d0) (una dispersione sotto la mediana, scala col sistema) "
                        "invece del muro assoluto 0.05. Blocca il collasso anomalo locale, non il "
                        "respiro comovente. Default off = 0.05 assoluto (non-regressione).")
    p.add_argument("--olon-part", action="store_true", dest="olon_part",
                   help="OLONOMIA NELLA PARTIZIONE: la quota tangenziale usa curl + twist coerente "
                        "(non solo curl), cosi' il verso coerente comanda la conversione e il freno, "
                        "non solo la direzione. Usare con --polo-maturo --viriale. Default off.")
    p.add_argument("--polo-maturo", action="store_true", dest="polo_maturo",
                   help="POLO MATURO (legge): al twist partecipa la chiralita del polo che matura "
                        "(torsione locale maggiore), non la differenza dei poli. Rompe il "
                        "bilanciamento dei +-pi -> olonomia netta con verso. Usare con --chi-basc.")
    p.add_argument("--ls-azim", action="store_true", dest="ls_azim",
                   help="L.S VETTORIALE: il verso tangenziale della viriale viene dalla componente "
                        "azimutale di (radiale x spinore _nb), non da circ_arc oscillante. Da' un "
                        "verso azimutale STABILE (precessione). Usare con --viriale. Default off.")
    p.add_argument("--verso-chi", action="store_true", dest="verso_chi",
                   help="AGGANCIO AL VERSO STABILE: FRAME_DRAG pilotato dalla circolazione del solo "
                        "twist_dip chirale (segno fisso) invece del tw pieno (dominato da dph "
                        "oscillante che inverte il verso). Usare con --chi-basc. Default off.")
    p.add_argument("--sync", action="store_true", dest="sync",
                   help="AGGIORNAMENTO SINCRONO (transazionale): dph (ponte fase->twist/metrica) "
                        "legge la fase dallo snapshot di inizio passo, coerente coi pesi materia. "
                        "Jacobi invece di Gauss-Seidel: il passo diventa indipendente dall'ordine. "
                        "Il simplettico resta intatto. Default off = non-regressione.")
    p.add_argument("--senza-spinore-vivo", action="store_true", dest="senza_spinore_vivo",
                   help="DIAGNOSTICO, NON FISICA ALTERNATIVA. CONGELA lo spinore: spegne "
                        "_passo_spinoriale, che dal 2026-09-18 e' ON di default come prerequisito "
                        "di SPIN_FEEDBACK. Spegne quindi ANCHE il feedback, e l'avviso lo dichiara. "
                        "Serve agli A/B e all'attribuzione, non ai run di misura.")
    p.add_argument("--spinore-vivo", action="store_true", dest="spinore_vivo",
                   help="REINNESTO EVOLUZIONE SU(2): richiama _passo_spinoriale (rotazione del Bloch "
                        "+ eccitazione del vuoto) dentro step(), PRIMA del commit atomico (legge lo "
                        "snapshot t). Riattiva il settore non-abeliano orfano dal commit d2c76f3. "
                        "Cambia la fisica: A/B e rimisura (Berry, curvatura). Default off = spinore congelato.")
    p.add_argument("--spin-larmor", action="store_true", dest="spin_larmor",
                   help="CAMPO TRASVERSO GEOMETRICO (legge, zero parametri): al campo dello spinore "
                        "somma B_geo = <|tw|/PHI_CRIT * (n_i x n_j)>, termine non-abeliano perpendicolare "
                        "a n che sostiene la precessione di Larmor senza auto-spegnersi con l'ordine. "
                        "Richiede --spinore-vivo. Default off = non-regressione.")
    p.add_argument("--semina-lam", action="store_true", dest="semina_lam",
                   help="[CURA DELLA SEMINA] `A13`: LAM e' la scala di Planck del sistema, e "
                        "sotto LAM non esiste niente -- nemmeno una distanza fra nodi. Ogni "
                        "nodo nuovo viene messo a distanza >= LAM da QUALUNQUE nodo gia' "
                        "presente (stessa massa, altre masse, vuoto di fondo), con semina "
                        "casuale e scarto (RSA). Se n non entra nel raggio, la semina RIFIUTA "
                        "nominando n, raggio e massimo raggiunto: niente riduzioni silenziose. "
                        "Zero numeri nuovi. Default off.")
    p.add_argument("--pozzo-d", action="store_true", dest="pozzo_d",
                   help="[D02] Nel pozzo del grafo la lunghezza `L` viene da `self.d` (la "
                        "distanza REALE dell'arco, `A3-DISEGNO`) invece che da `self.pos` "
                        "(il "
                        "DISEGNO). Il risultato entra nella spinta `S09`, quindi a flag "
                        "acceso LA SPINTA CAMBIA: e' la cura, non un effetto collaterale. "
                        "Toglie anche il pavimento `1e-9`, che con `d >= LAM` non serve, e "
                        "CONTA i casi `d <= 0` invece di assumerli impossibili. NON tocca le "
                        "letture di `pos` come DIREZIONE in `memoria_hebbiana_moto`: quelle "
                        "sono `D03`. Default off.")
    p.add_argument("--tempo-unico-mitosi", action="store_true", dest="tempo_unico_mitosi",
                   help="[CURA 2] UN SOLO OROLOGIO dentro `mitosi()`. Gli usi di `tau_pp` come "
                        "TEMPO (il ritmo, la costante di rilassamento di `_rep`, il gradiente "
                        "di tempo proprio) passano all'orologio `dt_e` che il sistema gia' "
                        "definisce; gli usi come POSIZIONE sull'asse della torsione (soglia, "
                        "centro, inversione) restano com'erano. Piu': `prob` in forma di "
                        "Poisson `1-exp(-lambda)` invece del clip, e il rilassamento di `_rep` "
                        "in forma ESATTA con `tau = d/cs_arco` (una DURATA) invece "
                        "dell'Eulero con `tau_pp` (un numero puro). Default off.")
    p.add_argument("--ritmo-wrap-2pi", action="store_true", dest="ritmo_wrap_2pi",
                   help="[CURA D34, approvata 2026-09-24] Il ramo SPINORIALE di `ritmo()` avvolge "
                        "la differenza di fase sul periodo GIUSTO (2pi) invece che su 4pi. "
                        "MOTIVO: `np.angle` ha periodo 2pi, quindi la differenza sta in (-2pi, 2pi] "
                        "e un wrap su 4pi e' l'IDENTITA' -- non avvolge niente. Dimostrato sulla "
                        "formula (max|w4(a)-a| = 0.000e+00 su 100 001 punti), sigillo 4/4, prova a "
                        "600 passi (Z123). Default off per la byte-identita' dei sigilli; IL DRIVER "
                        "LA ACCENDE IN OGNI RUN.")
    p.add_argument("--tw-spinore", action="store_true", dest="tw_spinore",
                   help="AGGANCIO DOPPIA COPERTURA (legge, zero parametri): la torsione a 4pi (tw) fa "
                        "precedere il Bloch di tw/2 (spin-1/2) attorno all'asse sigma della chiralita' del "
                        "legame (sigma_x uguali, sigma_z opposti). Asse persistente (non si auto-spegne come "
                        "SPIN_LARMOR). Richiede --spinore-vivo. Default off = non-regressione.")
    p.add_argument("--spinore-corretto", action="store_true", dest="spinore_corretto",
                   help="MASTER gestione corretta dello spinore (zero parametri): (1) OROLOGIO PROPRIO di "
                        "de Broglie [omega_proprio=(rho/rho_c)*r_medio lungo l'asse di Bloch PROPRIO, pura "
                        "fase]; (2) SPINORE PRIMARIO complesso _psi_spinor (n x 2) in SU(2), Bloch derivato. "
                        "Evaluate-then-commit rigoroso, |psi|=1 ogni passo. Richiede --spinore-vivo. "
                        "Default off = byte-identico. NON aggancia perc_chi ne' orienta il ritmo (flag separati).")
    p.add_argument("--chi-da-spinore", action="store_true", dest="chi_da_spinore",
                   help="FLAG 3 (separato): perc_chi = segno di doppia-copertura di _psi_spinor DOPO il commit "
                        "di psi, e CHI_BASC disattivato. RICHIEDE --spinore-corretto (senno' loop). Default off.")
    p.add_argument("--scala-min", action="store_true", dest="scala_min",
                   help="NESSUNA LUNGHEZZA SOTTO LAM. Non rimappa il valore: SMORZA LA DISCESA. Un "
                        "incremento >= 0 resta intatto bit per bit; uno < 0 e' moltiplicato per "
                        "max(0, 1-LAM/x) col valore x PRIMA di quella scrittura. Vale per i dodici "
                        "scrittori di d0 e per l incremento del Verlet su d; i sette pavimenti di d0 "
                        "spariscono; le nascite partono da LAM. Zero coefficienti. Default off = "
                        "byte-identico.")
    p.add_argument("--coes-adim", action="store_true", dest="coes_adim",
                   help="COESIONE ADIMENSIONALE E CAUSALE: i tre addendi normalizzati sulla densita' "
                        "LOCALE dell'arco invece che su I_med (media globale, A2), e lo spostamento e' "
                        "passo_causale * tanh(...) * filtro_portata, con |F| <= 1 per costruzione invece "
                        "che per clip. Sostituisce il clip tanh(stress)*d0. Default off = byte-identico.")
    p.add_argument("--invarianti", dest="invarianti", default="on",
                   choices=["on", "off"],
                   help="GLI INVARIANTI (C5). ACCESI DI DEFAULT: il programma si FERMA al primo "
                        "passo in cui una grandezza esce dal suo DOMINIO FISICO, e dice DOVE "
                        "(grandezza, regola, passo, INDICI, valori, funzione). Due livelli: "
                        "NUMERICO (overflow/divisione per zero/valori non validi) e FISICO (il "
                        "registro DOMINI). L underflow NON ferma niente: densita come 1e-81 di "
                        "un nodo neonato sono legittime. Legge soltanto: su un run sano non "
                        "cambia un bit. --invarianti=off serve a RIGIOCARE i run delle epoche 1 "
                        "e 2, che violano regole oggi note e si vogliono riprodurre COM ERANO.")
    p.add_argument("--anom-simm", action="store_true", dest="anom_simm",
                   help="ANOMALIA SIMMETRICA SENZA PAVIMENTO: anom = 2*(rho-peq)/(rho+peq), con "
                        "0/0 := 0 DEFINITO. Toglie il pavimento max(peq,1e-9), che e' un numero "
                        "SCELTO e non esprime nessun vincolo fisico (A11): con peq negativo "
                        "ribaltava il segno e moltiplicava per 3.7e5 (Z94). Il caso peq->0 passa "
                        "da 1e+08 a ESATTAMENTE +2, e per anomalie piccole le due forme "
                        "coincidono. RICHIEDE --peq-esatto: con peq < 0 la forma simmetrica ha un "
                        "POLO in peq = -rho. Default off = byte-identico.")
    p.add_argument("--coes-causale", action="store_true", dest="coes_causale",
                   help="LA COESIONE CHE RISPETTA L'ISTANTE E IL CONO LOCALE: d0 e d si leggono "
                        "dalla fotografia di INIZIO PASSO (prima erano MISTI: densita' di fine "
                        "step sommata a un d0 gia' spostato da sette scritture), e il tetto "
                        "diventa cs_arco*DT col cs del nodo PIU' LENTO invece di LAM*sqrt(K_C)*DT, "
                        "che e' costruito su costanti di modulo e non conosce il cono del luogo "
                        "(A5). Zero parametri. Default off = byte-identico.")
    p.add_argument("--senza-controllo-registro", action="store_true",
                   dest="senza_controllo_registro",
                   help="SPEGNE il CONTROLLO UNICO del registro delle grandezze "
                        "(`RIPIEGHI-ZERO`). DEFAULT: il controllo e ACCESO, perche non e "
                        "un esperimento ma una CURA approvata, e un controllo spento non "
                        "impedisce niente (A9). QUESTO FLAG ESISTE PER IL SIGILLO: il "
                        "criterio C chiede che, col controllo SPENTO, la prova a guasto "
                        "torni a dare ZERO grandezze protette -- senno il sigillo non sta "
                        "misurando il controllo. Con il flag, ogni chiamata si CONTA in "
                        "`_g_registro_spento` invece di passare in silenzio.")
    p.add_argument("--scala-min-passo", action="store_true", dest="scala_min_passo",
                   help="IL FRENO DELLA SCALA MINIMA UNA VOLTA PER PASSO, sulla VARIAZIONE "
                        "TOTALE di d0 e di d, dal valore di INIZIO passo. Le sei scritture di d0 "
                        "e i sotto-passi di d non frenano piu'. Cura il CRICCHETTO di Z91: "
                        "frenare ogni scrittura separatamente rende il risultato dipendente "
                        "dall'ORDINE delle leggi, e con spinte opposte di somma nulla non da' "
                        "zero. Applicato una volta sola il bias e' ZERO ESATTO. Le nascite "
                        "restano a LAM. Zero coefficienti. Default off = byte-identico.")
    p.add_argument("--peq-nascita-locale", action="store_true", dest="peq_nascita_locale",
                   help="UNA SOLA LEGGE DI NASCITA PER peq, E LOCALE: gli archi della creazione "
                        "di coppia alla Schwinger nascono con nan e vengono calibrati da step() "
                        "sulla rho del LORO arco, come quelli di _allaccia, invece di prendere "
                        "median(peq) -- una statistica GLOBALE dentro una legge locale (A2). "
                        "Zero parametri: il meccanismo esisteva gia'. L'eredita' della mitosi "
                        "NON si tocca. Default off = byte-identico.")
    p.add_argument("--peq-esatto", action="store_true", dest="peq_esatto",
                   help="RILASSAMENTO ESATTO DI peq: peq <- rho + (peq-rho)*exp(-dt_e/tau_bg), "
                        "piu' lo stesso passo esatto per la diffusione (Lie-Trotter). E' una "
                        "combinazione convessa, quindi peq resta SEMPRE fra peq e rho e non puo' "
                        "scavalcare sotto zero per nessun passo. Cura il difetto misurato in Z94 "
                        "(Eulero esplicito con dt_e/tau_bg = 1.2018 -> peq negativo -> il pavimento "
                        "di :4215 ribalta il segno dell'anomalia e nsub esplode a 22591). Zero "
                        "coefficienti. Default off = byte-identico.")
    p.add_argument("--chi-coop", action="store_true", dest="chi_coop",
                   help="COOPERAZIONE chi_basc + spinore: `chi_basc` NON si spegne e scrive la GEOMETRIA in "
                        "perc_geom (letta dalla catena della torsione CHI_CORE/FRAME_DRAG/TORS_4PI), mentre "
                        "lo spinore scrive la CARICA in perc_chi (letta dal campo B del passo spinoriale, "
                        "dalla mitosi, da Schwinger e da TEMPO_SEGNO). RICHIEDE --spinore-corretto. "
                        "Default off = byte-identico.")
    p.add_argument("--tempo-proprio-orientato", action="store_true", dest="tempo_proprio_orientato",
                   help="FLAG 4 (separato, profondo): toglie |.| da f in ritmo() -> r con SEGNO (tempo proprio "
                        "orientato, non solo modulo). Cambia una legge di base. Default off.")
    p.add_argument("--sync-spinore", action="store_true", dest="sync_spinore",
                   help="KURAMOTO SU(2) SUGLI SPINORI (zero parametri): tira ogni spinore verso l'allineamento "
                        "con la media di vicinato, torque omega_sync = forza*(nb x nb_media) con nb_media=(wI@nb_t)/uno "
                        "e forza dal Kuramoto-phi esistente (K_SYNC, 2/pi, prof_rel, rinforzo_shear). Torque "
                        "istantaneo in omega_tot (rotazione), non nella memoria omega_s. Richiede settore spinore "
                        "vivo e K_SYNC!=0. Default off = byte-identico.")
    p.add_argument("--deparam-orologio", action="store_true", dest="deparam_orologio",
                   help="DE-PARAMETRIZZAZIONE RELAZIONALE dell'orologio de Broglie (zero parametri): la frequenza "
                        "propria omega_clk non e' piu' |Psi|^2 estensiva / rho_c GLOBALE (~95% connettivita', deg "
                        "2->379) ma la COERENZA D'ARCO intensiva sum_j w_ij cos(phi_i-phi_j)/sum_j w_ij (indipendente "
                        "dal grado, tetto naturale 1, nessun volume). Tocca SOLO l'orologio spinoriale, non la "
                        "Psi-sorgente di gravita'. Richiede --spinore-corretto. Default off = byte-identico.")
    p.add_argument("--sync-fase-orologio", action="store_true", dest="sync_fase_orologio",
                   help="KURAMOTO SUL SEGNO DI DOPPIA-COPERTURA (zero parametri): ordina relazionalmente il foglio "
                        "+- (alpha_k=arg<canon(nb_k)|psi_k>) tirandolo verso la media di vicinato con torque O(dt^1) "
                        "eta = dt*forza*sin(media_alpha-alpha), forza dal Kuramoto-phi (K_SYNC, prof_rel, rinforzo_shear). "
                        "Fase globale su psi -> nb invariante (gravita' intatta), agisce sul SEGNO non su phi. Richiede "
                        "--spinore-corretto. Default off = byte-identico.")
    p.add_argument("--fork-su2", action="store_true", dest="fork_su2",
                   help="[FORK SU(2) STRATO 0] ARC-CONNECTION non-abeliana nella forza: il trasporto smette di essere "
                        "uno SCALARE applicato uguale ad a e b (abeliano per STRUTTURA) e diventa la matrice di Berry "
                        "N_ij/2 = cos(chi/2) U_ij in SU(2), che MESCOLA a,b. Il peso cos(chi/2) = |<n_i|n_j>| e' "
                        "l'OVERLAP DI SPIN, non un parametro: e' cio' che resta non normalizzando il trasporto. "
                        "Allineati -> N/2 = I -> riduzione ESATTA al ramo scalare; antipodali -> N = 0. Zero parametri "
                        "nuovi. Richiede --campo-spinoriale. Default off = byte-identico.")
    p.add_argument("--fork-su2-mem", action="store_true", dest="fork_su2_mem",
                   help="[FORK SU(2) STRATO 1] CONNESSIONE CON MEMORIA: la connessione N_ij non nasce piu' dai Bloch "
                        "dell'ISTANTE ma da quelli RITARDATI n(t-tau), con tau = d/cs (tempo-luce dell'arco, zero "
                        "parametri nuovi). Serve a rompere il TEOREMA DI INERZIA dello Strato 0: costruita dagli stessi "
                        "stati che trasporta e nello stesso istante, la connessione di Berry e' l'identita' sull'overlap "
                        "e la forza non cambia di un bit (misurato 1.57e-15). Col ritardo psi(t) non e' piu' autovettore "
                        "di n(t-tau).sigma e la forza cambia: e' CAUSALITA' (cono di luce), non una taratura. Il Bloch "
                        "ritardato rilassa verso il corrente con slerp geodetico, alpha = 1-exp(-dt/tau) (passo esatto di "
                        "primo ordine, mai Verlet). A riposo, o per tau->0, torna allo Strato 0. Richiede --fork-su2. "
                        "Default off = byte-identico.")
    p.add_argument("--rumore-colorato", action="store_true", dest="rumore_colorato",
                   help="TAGLIO SPETTRALE del calcio del vuoto: invece di rumore BIANCO "
                        "(indipendente a ogni passo, banda infinita fino a Nyquist, che aliasa "
                        "per costruzione e in natura non esiste), un processo di "
                        "Ornstein-Uhlenbeck correlato su tau_c = LAM/CS_M, il tempo-luce del "
                        "solitone. DERIVATO: LAM e CS_M sono gia' nel sistema, zero coefficienti "
                        "nuovi, `amp` INVARIATA, `dt` = dt_n = DT*r (processo locale). "
                        "ATTENZIONE, scritto PRIMA di misurare: la ricorsione PRESERVA LA "
                        "VARIANZA, quindi NON abbassa theta e se lo muove lo fa SALIRE (<=5 %). "
                        "Si cabla perche' il rumore bianco e' fisicamente SBAGLIATO, non perche' "
                        "risolva l'aliasing. Default OFF.")
    p.add_argument("--tau-luce", action="store_true", dest="tau_luce",
                   help="[FASE 2] IL RILASSAMENTO DI omega_s USA IL TEMPO-LUCE d/cs invece della densita'. "
                        "Sostituisce SOLO `_tau = TAU_A*max(dens/dens_rif, 0.05)` con `d_nodo/cs_nodo`, "
                        "cioe' con `_tempo_luce_nodo()` - lo STESSO tau gia' cablato nello Strato 1. "
                        "MOTIVO su tre piani: (1) COERENZA - inerzia = T^2 = (d/cs)^2, quindi il tempo che "
                        "costruisce l'inerzia e quello che la rilassa devono essere LO STESSO, e oggi sono "
                        "due diversi nella stessa equazione; (2) PRINCIPIO - un sistema non puo' ricordare "
                        "piu' a lungo di quanto impieghi a sapere di se'; (3) MISURA - d/cs e' PIATTO "
                        "contro l'inerzia (+0.097 +- 0.0055) contro +1.176 +- 0.019 della riga attuale, "
                        "quindi non puo' cancellare il -1 della coppia. Zero coefficienti, zero floor "
                        "nuovi. NON e' la soluzione dell'aliasing: theta cala di ~13x, da ~112 a ~9 "
                        "giri/passo. Default off = byte-identico.")
    p.add_argument("--gamma-turbo", type=float, default=1.0, dest="gamma_turbo", metavar="K",
                   help="[DIAGNOSTICO, NON PERCORSO CERTIFICATO] amplifica di K la SENSIBILITA' DI cs ALLA "
                        "DENSITA': dentro _cs_nodo si usa GAMMA*K al posto di GAMMA, e SOLO li'. Default K=1 "
                        "= nessun effetto = byte-identico. Serve perche' alle densita' attuali cs e' MORTO "
                        "(I~0.05 contro la soglia ~1/GAMMA^2 ~ 400): il turbo abbassa la soglia cosi' che cs si "
                        "svegli a densita' raggiungibili. NON aggiunge fisica: accelera un meccanismo che ESISTE "
                        "(cs = cs(rho)) e che e' spento SOLO dalla scala. RISTRETTO di proposito: GAMMA e' "
                        "condiviso con satura() e con la saturazione del campo spinoriale, e turboarlo "
                        "globalmente cambierebbe la dinamica del campo invece della sensibilita' di cs, rendendo "
                        "il risultato inattribuibile. ONESTA': restringendo si rompe di proposito quella "
                        "condivisione, quindi e' un ISOLAMENTO DIAGNOSTICO e NON il regime reale ad alta "
                        "densita'. Richiede --cs-dinamico. Il criterio di lettura non e' 'l'effetto appare' ma "
                        "'l'effetto SCALA con K ed ESTRAPOLA con continuita' verso K=1'.")
    p.add_argument("--senza-step2-orologio", action="store_true", dest="senza_step2_orologio",
                   help="DIAGNOSTICO, NON FISICA ALTERNATIVA. Spegne lo STEP 2 (orologio <-> "
                        "metrica), che dal 2026-09-16 e' FISICA DI DEFAULT (par.10). Serve agli "
                        "A/B per misurare COSA FA quella legge, non ai run di misura. Un run di "
                        "misura con questo flag gira su un sistema in cui l'EM NON risponde alla "
                        "curvatura, e va dichiarato nel documento che lo usa.")
    p.add_argument("--step2-orologio", action="store_true", dest="step2_orologio",
                   help="[NO-OP dal 2026-09-16: PROMOSSO A DEFAULT, par.10. Il flag resta accettato per non "
                        "rompere comandi e script esistenti, ma non fa nulla; per spegnerlo serve "
                        "--senza-step2-orologio.] AGGANCIO OROLOGIO <-> METRICA: omega_clk *= (cs/CS_M)^2. E' l'OROLOGIO DI COMPTON "
                        "(omega = m c^2 / hbar): la frequenza propria di una massa va come c^2, e nel modello c e' cs. "
                        "Non e' una manopola ma fisica NECESSARIA e derivata: zero parametri, nessun floor, nessun "
                        "coefficiente, e a cs = CS_M il fattore vale esattamente 1 (riduzione al limite per costruzione). "
                        "Serve perche' la metrica legge solo |psi|^2 e l'orologio non legge cs: i due tempi propri "
                        "(metrico d/cs e orologio DT*r) erano SCOLLEGATI. Con cs < CS_M (pozzo, alta densita') l'orologio "
                        "RALLENTA come cs^2 = redshift gravitazionale. Agisce sulla FASE dello spinore (U(1)): NON muove "
                        "il Bloch (invariante per fase globale) e quindi NON organizza lo spin. Richiede "
                        "--campo-spinoriale + --deparam-orologio. Default off = byte-identico.")
    p.add_argument("--kuramoto-su2", action="store_true", dest="kuramoto_su2",
                   help="KURAMOTO SU(2) NON-ABELIANO (zero parametri): ruota lo SPINORE INTERO verso la media SU(2) "
                        "dei vicini psi_bar=(wI@psi)/|.| con rotazione geodetica attorno all'asse VARIABILE nb x nb_bar "
                        "(non commuta -> non-abeliano). Verso+segno ruotano INSIEME (il segno emerge per OLONOMIA). "
                        "Torque O(dt^1), forza dal Kuramoto-phi. nb SI muove (gravita' fisica, non 6.7e-16). Richiede "
                        "--spinore-corretto (+ --deparam-orologio sopra soglia). Default off = byte-identico.")
    p.add_argument("--trace-segno", action="store_true", dest="trace_segno",
                   help="TRACING per-passo del SEGNO di doppia-copertura (SOLO OSSERVAZIONE, pure-read, zero mutazioni): "
                        "dump per-passo di s_k=Re<canon(nb)|psi>, archi sign_i*sign_j, torque |media SU(2) vicini|, "
                        "twist, correlazioni sign-twn/geometria, eventi nati/coppie. Per capire perche' i segni si "
                        "cancellano (berry assoluta forte, firmata zero). Non tocca la fisica. Default off.")
    p.add_argument("--trace-out", dest="trace_out", default=None,
                   help="percorso del dump di --trace-segno (default: <diaglog>.trace.csv).")
    p.add_argument("--campo-spinoriale", action="store_true", dest="campo_spinoriale",
                   help="[FASE 1 dev-spinoriale] CAMPO EMESSO DALLO SPINORE (zero parametri): in calcola_psi costruisce "
                        "il campo Psi spinoriale (n,2) = _mat(w) @ (amp*_psi_spinor) con lo STESSO kernel del grafo, "
                        "saturato sulla NORMA (non ruota lo spinore), e rho=psi^dag psi. Calcolato IN PARALLELO "
                        "(self.psi_spin/rho_spin), NON ancora agganciato a gravita'/forze/mitosi (fasi 2-4). Riduzione-al-"
                        "limite: con _psi_spinor=(e^{i phi},0) la componente 0 == campo scalare. Default off = byte-identico.")
    p.add_argument("--tempo-segno", action="store_true", dest="tempo_segno",
                   help="MOD 5.3a+5.3b (dev-spinoriale, zero parametri): il VERSO del tempo proprio dalla "
                        "MATERIA/ANTIMATERIA COERENTE (Feynman-Stuckelberg): s_k=1+(perc_chi-1)*m_coer con "
                        "m_coer=clip(cos(phi-arg(Psi)),0,1) (materia coerente inverte col segno, il VUOTO incoerente "
                        "va avanti); omega/fase interne usano s_k*dt_n, eta/geometria usano |dt_n|. La MAGNITUDINE del "
                        "ritmo() diventa la torsione esplicita 1+|tw|/PHI_CRIT (il de Broglie del campo emesso, bocciato "
                        "da S3b). Da stato t-1 (causale). Richiede --campo-spinoriale + --spinore-corretto. Default off = byte-identico.")
    p.add_argument("--orologio-segno", action="store_true", dest="orologio_segno",
                   help="MOD 5.3c (dev-spinoriale, zero parametri): firma il VERSO dell'orologio de Broglie INTERNO "
                        "_phc = exp(-0.5j * s_k * omega_clk * dt) col segno di doppia-copertura STABILE s_k=sign(perc_chi) "
                        "(lignaggio, non l'istantaneo Re<canon|psi> che oscilla): materia exp(-), antimateria exp(+), "
                        "tempi SPECULARI. |omega_clk| INVARIATA (S3b: solo verso, non velocita'). Fase globale -> nb "
                        "invariante (gravita'/direzione intatte); eta/geometria = magnitudine. Vive nel ramo "
                        "--deparam-orologio (orologio pura-fase). Richiede --campo-spinoriale + --spinore-corretto. "
                        "Default off = byte-identico.")
    p.add_argument("--senza-spin-feedback", action="store_true", dest="senza_spin_feedback",
                   help="DIAGNOSTICO, NON FISICA ALTERNATIVA. Spegne il feedback spinore->archi, "
                        "che dal 2026-09-18 e' ON di default (par.10). Serve agli A/B e "
                        "all'attribuzione, non ai run di misura. NB: e' acceso PER DECISIONE e su "
                        "basi di FORMA -- l'A/B a quattro semi NON ha mostrato un effetto.")
    p.add_argument("--spin-feedback", action="store_true", dest="spin_feedback",
                   help="FEEDBACK LOCALE SPINORE->ARCHI: la parte immaginaria dell'overlap del lift "
                        "spinoriale aggiunge una coppia antisimmmetrica alle fasi. Richiede "
                        "--spinore-vivo. Default off = non-regressione.")
    p.add_argument("--spin-positivi", action="store_true", dest="spin_positivi",
                   help="MISURA SPINORE DI GRUPPO: registra anche la misura per-picco usando solo "
                        "i generatori perc_chi=+1. Diagnostica, non modifica la dinamica.")
    p.add_argument("--chi-core", action="store_true", dest="chi_core",
                   help="CHIRALITA' EMERGENTE DEL CORE: usa rho0/rhoc e il raggio locale del core "
                        "per il frame-dragging. Non seleziona il segno a priori; default off.")
    p.add_argument("--cs-dinamico", action="store_true", dest="cs_dinamico",
                   help="VELOCITA' METRICA LOCALE: cs_eff(rho) con transizione tanh, "
                        "pavimento locale emergente, media armonica sugli archi e CFL dinamico. Default off.")
    p.add_argument("--vista-rete", action="store_true", dest="vista_rete",
                   help="RENDERING RETE-ONLY: mantiene dinamica, metriche e pulsanti della vista campo "
                        "ma mostra nei tre pannelli solo nodi e archi. Default: vista campo attuale.")
    p.add_argument("--bussola", type=int, default=1,
                   help="1 = indicatore d'assi nel margine, 0 = nessun riferimento")
    p.add_argument("--giri", type=float, default=1.0,
                   help="giri di camera sulla durata della scena (0 = vista fissa)")
    p.add_argument("--sync-db", dest="sync_db", default=None,
                   help="DB DI STATO (idempotente+versionato): file da cui CARICARE lo stato a inizio "
                        "run (se esiste e la versione combacia) e su cui SALVARE periodicamente. "
                        "Permette di spezzare un run lungo in piu' sessioni.")
    p.add_argument("--db-cleanup", dest="db_cleanup", action="store_true",
                   help="cancella il DB di stato prima di partire (run pulito da zero). Usare quando "
                        "la fisica e' cambiata (il DB verrebbe comunque rifiutato per hash diverso).")
    p.add_argument("--da-libera", dest="da_libera", action="store_true",
                   help="VIDEO: non registra la formazione, inizia a registrare quando il sistema "
                        "entra in EVOLUZIONE LIBERA. Video corto e mirato.")
    p.add_argument("--db-ogni", dest="db_ogni", type=int, default=250,
                   help="ogni quanti passi salvare il DB di stato (default 250). Piu' basso = piu' "
                        "sicuro contro le interruzioni, ma piu' scritture su disco.")
    p.add_argument("--db-serie", dest="db_serie", action="store_true",
                   help="ARCHIVIO: i salvataggi che avvengono ogni --db-ogni passi vengono NUMERATI "
                        "(<stem>_000250.pkl...) invece che sovrascritti. OFF di default: senza, il "
                        "comportamento e' quello di sempre (un solo file, checkpoint di ripresa). "
                        "Se il path finisce in .gz lo snapshot e' compresso.")
    p.add_argument("--db-rigioca", dest="db_rigioca", nargs=2, type=int, default=None,
                   metavar=("DA", "A"),
                   help="ARCHIVIO: ricarica lo snapshot DA della serie, rigira fino ad A salvando "
                        "ogni --db-ogni passi. INFITTISCE l'archivio senza rifare il run. NON "
                        "sovrascrive gli snapshot che gia' esistono: li SALTA e li conta. Richiede "
                        "--db-serie.")
    p.add_argument("--batch", action="store_true",
                   help="processo batch: due masse, evoluzione lunga, misura la CONDENSAZIONE "
                        "nel vuoto fra le masse (ordine, densita', nuovo nucleo). Output numerico.")
    p.add_argument("--passi", type=int, default=3000,
                   help="batch: numero totale di passi di evoluzione (default 3000)")
    p.add_argument("--ogni", type=int, default=30,
                   help="batch: ogni quanti passi registrare una misura (default 30)")
    p.add_argument("--sep", type=float, default=2.3,
                   help="batch: raggio del cerchio su cui stanno le masse (default 2.3)")
    # [SCENA (ii), 2026-09-25] `0` = FINO A SATURAZIONE (il default): il numero lo decide la
    # GEOMETRIA, non un numero scelto. Il braccio di controllo di `P-GONFIA` (`SEMINA_LAM`
    # spento) passa qui il numero MISURATO dal braccio acceso, per avere lo STESSO `n`.
    # [CURA 5, 2026-09-25] `A13` ALLA NASCITA. OFF di default (par.1).
    p.add_argument("--mitosi-2lam", action="store_true",
                   help="[CURA 5] un arco si divide SOLO se `d_arco >= 2 LAM`, cioe' `A13` "
                        "applicato alla nascita: il figlio nasce a `d/2` dai genitori, e sotto "
                        "`LAM` non esiste una distanza. NON e' una legge nuova e non ha numeri "
                        "nuovi; TOGLIE l'intervento di `_nasce` sui figli della mitosi. Lo "
                        "SCHWINGER non e' toccato (resta `A3`). OFF di default: a flag spento il "
                        "comportamento e' BYTE-IDENTICO.")
    p.add_argument("--contrasto-intensivo", action="store_true", dest="contrasto_intensivo",
                   help="[INERZIA-1(C)] il CONTRASTO dell'inerzia diventa PER VICINO: "
                        "`rho_s` si normalizza sullo STESSO conteggio di vicini che "
                        "`peq_nodo` usa gia' come denominatore. Curato perche' i due fattori "
                        "scalavano in verso OPPOSTO nel numero di vicini (misurato: coppia "
                        "k^-0.25, contrasto k^+1.06..+2.47), e da k=77 a k=2 |omega| "
                        "esplodeva x150-176. LOCALE: `rho_s` NON cambia altrove. OFF di "
                        "default finche' il sigillo non passa.")
    # [CURA 4, 2026-09-25] L'ACCENSIONE DEL CAMPO. OFF di default (par.1).
    p.add_argument("--semina-matura", action="store_true",
                   help="[CURA 4] i nodi della SEMINA INIZIALE nascono MATURI (ramp = 1), e la "
                        "rampa dei pesi resta SOLO per i nati in dinamica col tempo "
                        "`_tempo_luce_nodo` invece di TAU_A. Cosi' i due ruoli di TAU_A si "
                        "separano: TAU_A resta SOLO la vita media della memoria spinoriale. "
                        "OFF di default: a flag spento il comportamento e' BYTE-IDENTICO.")
    p.add_argument("--mc-nodi", type=int, default=0,
                   help="SCENA (ii): nodi del vuoto; 0 = fino a saturazione (default)")
    # BRACCIO DI CONTROLLO DI `S10`: fasi casuali anche DENTRO le regioni. DIAGNOSTICO.
    p.add_argument("--mc-fasi-casuali", action="store_true",
                   help="SCENA (ii): fasi casuali dentro le regioni (controllo di S10)")
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


def _db_serie_path(base, step):
    """<stem>_%06d<ext>. Padding a SEI cifre: l'ordine alfabetico E' quello temporale.
    Funzione PURA sui path: nessuno stato, nessuna fisica."""
    import os as _o
    d, f = _o.path.split(base)
    stem, ext = (f[:-7], ".pkl.gz") if f.endswith(".pkl.gz") else _o.path.splitext(f)
    return _o.path.join(d, "%s_%06d%s" % (stem, step, ext))


def _db_serie_esistenti(base):
    """Gli snapshot gia' presenti della serie, ORDINATI per passo: [(passo, path), ...].
    Accetta sia `.pkl` sia `.pkl.gz` (retrocompatibilita')."""
    import glob as _g, os as _o, re as _re
    d, f = _o.path.split(base)
    stem = f[:-7] if f.endswith(".pkl.gz") else _o.path.splitext(f)[0]
    out = []
    for p in _g.glob(_o.path.join(d, stem + "_??????.pkl*")):
        m = _re.search(r"_(\d{6})\.pkl(\.gz)?$", p)
        if m:
            out.append((int(m.group(1)), p))
    return sorted(out)


def _db_identita_snapshot(stato, ver):
    """Il verdetto di identita' di UNO snapshot, con la STESSA REGOLA di `carica_stato`: il git
    BLOB dei byte se entrambi ce l'hanno, altrimenti il fallback sha256 (DB legacy / git assente).
    Ritorna `None` se compatibile, altrimenti il MOTIVO del rifiuto.

    ⚠ E' una SECONDA COPIA di quella regola, e lo dichiaro invece di tacerlo. `carica_stato` non si
    tocca (vincolo esplicito del mandato) e non si puo' riusare per una scansione, perche' APPLICA
    lo stato alla rete invece di limitarsi a leggerlo. Due copie di una regola possono DIVERGERE:
    se una cambia, cambiano entrambe."""
    db_blob = stato.get('blob')
    if db_blob is not None and ver.get('blob') is not None:
        if db_blob != ver['blob']:
            return ("blob %s, mentre il codice ORA e' %s -- ALTRA FISICA"
                    % (str(db_blob)[:8], str(ver['blob'])[:8]))
        return None
    db_hash = stato.get('content_hash', stato.get('code_hash'))
    if db_hash != ver.get('content_hash'):
        return ("sha256 %s, mentre il codice ORA e' %s [fallback: DB legacy o git assente]"
                % (db_hash, ver.get('content_hash')))
    return None


def _db_serie_verifica(base, ver):
    """RIFIUTA una serie che non e' di QUESTA FISICA. **Il discriminante e' IL BLOB, e nient'altro.**

    ⚠ STORIA DI QUESTA FUNZIONE, che e' il motivo per cui e' scritta cosi' (2026-09-19).
    La prima versione controllava la CADENZA: che ogni passo fosse multiplo di `--db-ogni` e che
    i passi fossero CONTIGUI. **Era un criterio AGGIUNTO rispetto al mandato, e rifiutava proprio
    il caso d'uso di `--db-rigioca`:** infittire un archivio SIGNIFICA rigirare con `--db-ogni` piu'
    piccolo, e una serie 250/500/750 non e' contigua a cadenza 50. **Dimostrato, non dedotto:**
    `csv/_seal_fork/_prova_D2_rigiocata_2026-09-19.txt`, 7/7, commit `edab9d4`.
    **CADENZE DIVERSE NELLA STESSA SERIE SONO LEGITTIME: e' il senso dell'archivio. Il rischio vero
    e' mescolare due FISICHE, non due cadenze.**
    E la vecchia versione sbagliava anche dalla parte opposta: **accettava file VUOTI, 0 byte, senza
    alcun blob** (`P4`), perche' guardava solo i NOMI. **Rifiutava il legittimo e accettava l'ignoto.**

    COSTO, misurato e non stimato (`csv/_seal_fork/_costo_archivio_2026-09-19.txt`): `0.156 s` per
    snapshot non compresso, `0.32 s` compresso -> **3.8 s per una serie da 24**, su un run che dura
    ore. **Per questo si controllano TUTTI gli snapshot e non solo quello che si carica**, che era
    cio' che il mandato chiedeva e che la prima versione delegava a `carica_stato`.

    ⚠ IL BUCO DEL PRESIDIO, dichiarato invece di essere taciuto: due run con lo STESSO blob ma
    SEME DIVERSO **non sono distinguibili dai `.pkl`**, perche' il seme NON e' fra gli `attrs`
    (c'e' `rng_state`, che e' lo stato DOPO N passi, non il seme).
    **E' un presidio PARZIALE, e chiamarlo totale sarebbe il difetto che A9 descrive.**"""
    import gzip as _gz, os as _o, pickle as _pk, time as _t
    ser = _db_serie_esistenti(base)
    if not ser:
        return ser, None
    guai = []
    _t0 = _t.perf_counter()
    for _passo_n, p in ser:
        nome = _o.path.basename(p)
        try:
            _apri = _gz.open if str(p).endswith('.gz') else open
            with _apri(p, 'rb') as _fh:
                st = _pk.load(_fh)
        except Exception as e:
            # UN FILE CHE NON SI APRE NON E' UNO SNAPSHOT. La vecchia versione non se ne accorgeva
            # nemmeno, perche' non apriva niente.
            guai.append("%s: ILLEGGIBILE (%s: %s)" % (nome, type(e).__name__, e))
            continue
        if not isinstance(st, dict):
            guai.append("%s: non e' uno snapshot (contiene %s)" % (nome, type(st).__name__))
            continue
        motivo = _db_identita_snapshot(st, ver)
        if motivo:
            guai.append("%s: %s" % (nome, motivo))
    _dt = _t.perf_counter() - _t0
    print("[db] serie: verificato il blob di %d snapshot su %d in %.1f s (TUTTI, non solo quello "
          "che si carica)" % (len(ser) - len(guai), len(ser), _dt))
    if guai:
        return ser, ("%d snapshot su %d NON sono di questa fisica:\n       %s"
                     % (len(guai), len(ser), "\n       ".join(guai[:5])))
    return ser, None


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
    # Una riga commento auto-descrittiva precede ogni report: conserva la
    # configurazione esatta del run senza confonderla con le colonne numeriche.
    import json as _json
    _parametri = dict(vars(a))
    _parametri.update({
        "seed_effettivo": seed,
        "nmasse_effettive": _nm,
        "passi_effettivi": passi,
        "ogni_effettivo": ogni,
        "sep_effettivo": sep,
        "leggi_attive": {
            "REGIME": REGIME, "SPINORE": SPINORE, "SPINORE_VIVO": SPINORE_VIVO,
            "SPIN_FEEDBACK": SPIN_FEEDBACK, "SPIN_LARMOR": SPIN_LARMOR,
            "CHI_CORE": CHI_CORE, "CS_DINAMICO": CS_DINAMICO,
            "SYNC_UPDATE": SYNC_UPDATE, "VERLET": VERLET,
            # [T1, P5] LA COMPOSIZIONE EFFETTIVA DEL PASSO nei risultati: con gli innesti
            #   (T5) l'ordine non sta piu' nel codice, quindi un referto che non lo scrive
            #   non dichiara la configurazione intera.
            "PASSO_COMPOSIZIONE": list(PASSO_COMPOSIZIONE),
            "VIRIALE": VIRIALE, "ZETA_VIR": ZETA_VIR, "PAV_COM": PAV_COM,
            "PLAST_DIN": PLAST_DIN, "TAU_USA_D0": TAU_USA_D0,
            "OLON_PART": OLON_PART, "POLO_MATURO": POLO_MATURO,
            "LS_AZIM": LS_AZIM, "VERSO_CHI": VERSO_CHI,
            "CHI_BASC": CHI_BASC, "ZETA_LOC": ZETA_LOC,
        },
        "costanti_effettive": {
            "LAM": LAM, "GAMMA": GAMMA, "SCALA_B": SCALA_B,
            "CS_M": CS_M, "K_C": K_C, "PHI_CRIT": PHI_CRIT,
        },
    })
    _metadata_csv = "# RUN_PARAMS " + _json.dumps(_parametri, ensure_ascii=False,
                                                    sort_keys=True, default=str,
                                                    separators=(",", ":"))
    print(f"[batch] condensazione: seed={seed} passi={passi} ogni={ogni} sep={sep} nmasse={_nm}")
    print(f"[batch] leggi attive: GRAV_BIFASE={GRAV_BIFASE} SPIN_ORBITA(via SPINORE)={SPINORE} "
          f"COPPIA_MIT={COPPIA_MIT} lambda={LAM:.3f}")
    Nc = massa_critica_collasso()
    net = Rete(seed); net.semina(80)
    for _ in range(6):
        esegui_passo(net)
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
        esegui_passo(net)

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
        if CS_DINAMICO and len(net.i):
            W_diag = net._mat(net._pesi())
            media_vicini_diag = (W_diag @ I2[:n]) / np.maximum(
                W_diag @ np.ones(n), 1e-9)
            u_diag = I2[:n] / np.maximum(media_vicini_diag, 1e-9)
            floor_diag = CS_M / (1.0 + GAMMA * np.sqrt(np.maximum(I2[:n], 0.0)))
            trans_diag = 0.5 * (1.0 + np.tanh(1.0 - u_diag))
            cs_nodo_diag = floor_diag + (CS_M - floor_diag) * trans_diag
            cs_arco_diag = (2.0 * cs_nodo_diag[net.i] * cs_nodo_diag[net.j] /
                            np.maximum(cs_nodo_diag[net.i] + cs_nodo_diag[net.j], 1e-12))
            cols['cs_eff_min'] = float(np.min(cs_arco_diag))
            cols['cs_eff_med'] = float(np.median(cs_arco_diag))
            cols['cs_eff_max'] = float(np.max(cs_arco_diag))
        # Misura locale delle masse: usa le coorti di nascita della scena come
        # dominio di riferimento stabile; il picco viene poi scelto da |Psi|^2
        # e il vicinato e' ricavato solo dagli archi topologici.
        try:
            for i_m, coorte in enumerate(coorti):
                idx_coorte = np.array(sorted(k for k in coorte if k < n), dtype=int)
                misura = net.misura_spin_picco_massa(idx_coorte)
                for nome, valore in misura.items():
                    cols[f'm{i_m}_picco_{nome}'] = round(float(valore), 7)
        except Exception:
            pass
        cols['n'] = n
        # LETTURA PURA del cache impostato dalla DINAMICA. chiralita_core_locale() MUTA
        # self._chi_core_nodi (riga ~954), letto dalla fisica a ~1967: il diaglog NON deve
        # richiamarla (muterebbe stato fisico) ne' ricalcolare a N nuovo. Solo lettura.
        if CHI_CORE:
            try:
                chi_core = getattr(net, '_chi_core_nodi', None)
                if chi_core is None or not len(chi_core):
                    chi_core = np.zeros(net.n)
                cols['chi_core_media'] = float(np.mean(chi_core))
                cols['chi_core_abs_media'] = float(np.mean(np.abs(chi_core)))
                cols['rho0_core_max'] = float(np.max(getattr(net, '_chi_core_rho0', np.zeros(1))))
                cols['rho_c_core'] = float(getattr(net, '_chi_core_rhoc', 0.0))
                cols['r_core_medio'] = float(np.mean(getattr(net, '_chi_core_raggio', np.zeros(1))))
            except Exception:
                pass
        cols['I2_min'], cols['I2_max'], cols['I2_mean'], cols['I2_absmax'] = _stat(I2)
        cols['r_min'], cols['r_max'], cols['r_mean'], _ = _stat(r)
        cols['tw_min'], cols['tw_max'], cols['tw_mean'], cols['tw_absmax'] = _stat(tw)
        cols['phi_min'], cols['phi_max'], cols['phi_mean'], _ = _stat(net.phi[:n])
        cols['phivel_min'], cols['phivel_max'], cols['phivel_mean'], cols['phivel_absmax'] = _stat(net.phivel[:n])
        cols['d_min'], cols['d_max'], cols['d_mean'], _ = _stat(net.d[:n] if len(net.d) >= n else net.d)
        cols['d0_min'], cols['d0_max'], cols['d0_mean'], _ = _stat(net.d0[:n] if len(net.d0) >= n else net.d0)
        # [`RAMPA-1`] I NODI DELLA SEMINA HANNO `eta = +inf`, quindi `_stat` su tutto darebbe
        #   `eta_max = inf` e **`eta_mean = inf`**: una colonna di `inf` **non e' un dato**, e un
        #   CSV e' il dato (`P6`). Le statistiche si fanno sui **finiti** -- cioe' sui nodi NATI
        #   IN DINAMICA, che sono quelli la cui rampa ha una storia -- e **il conto degli
        #   infiniti diventa una colonna sua**, `eta_inf`, che dice quanti nodi sono del vuoto
        #   dato. **Non si nasconde l'infinito: si separa, e si conta.**
        #   ⚠ Se TUTTI i nodi sono infiniti (prima della prima mitosi) `_stat` di un array vuoto
        #   da' `nan`: **`nan` qui significa «nessun nodo nato in dinamica»**, non «misura
        #   fallita», e `eta_inf` lo dice.
        _eta_v = net.eta[:n] if len(net.eta) >= n else net.eta
        _eta_fin = np.asarray(_eta_v, float)[np.isfinite(np.asarray(_eta_v, float))]
        cols['eta_min'], cols['eta_max'], cols['eta_mean'], _ = _stat(_eta_fin)
        cols['eta_inf'] = int(np.sum(~np.isfinite(np.asarray(_eta_v, float))))
        cols['tau_min'], cols['tau_max'], cols['tau_mean'], _ = _stat(tau)
        cols['dmin_nodi'] = dmin
        cols['xi_termo'] = float(getattr(net, 'xi_termo', 0.0))
        cols['n_archi'] = len(net.i)
        # CIRCOLAZIONE TOPOLOGICA: misura passiva sui cicli del grafo, indipendente
        # dall'embedding. Non entra nella dinamica finche' non viene validata.
        try:
            circ = net.circolazione_topologica()
            cols['n_cicli_topologici'] = circ['n_cicli']
            cols['circolazione_topologica_max'] = circ['circolazione_max']
            cols['circolazione_topologica_media_assoluta'] = circ['circolazione_media_assoluta']
            cols['circolazione_topologica_rms'] = circ.get('circolazione_rms', 0.0)
            cols['corrente_arco_max'] = circ.get('corrente_arco_max', 0.0)
            cols['gradiente_rho_arco_media_assoluta'] = circ.get('gradiente_rho_arco_media_assoluta', 0.0)
            cols['circolazione_topologica_media'] = circ.get('circolazione_media', 0.0)
            cols['olonomia_fase_max'] = circ.get('olonomia_max', 0.0)
            cols['olonomia_fase_media_assoluta'] = circ.get('olonomia_media_assoluta', 0.0)
            cols['olonomia_fase_rms'] = circ.get('olonomia_rms', 0.0)
            cols['berry_spin_max'] = circ.get('berry_spin_max', 0.0)
            cols['berry_spin_media_assoluta'] = circ.get('berry_spin_media_assoluta', 0.0)
            cols['berry_spin_rms'] = circ.get('berry_spin_rms', 0.0)
            cols['berry_spin_media'] = circ.get('berry_spin_media', 0.0)
            cols['berry_segno_media'] = circ.get('berry_segno_media', 0.0)                 # olonomia Bargmann _psi_spinor FIRMATA (gauge-inv): ~0 frustrato / !=0 ordine
            cols['berry_segno_media_assoluta'] = circ.get('berry_segno_media_assoluta', 0.0)
            cols['berry_segno_rms'] = circ.get('berry_segno_rms', 0.0)
            cols['n_cicli_segno'] = circ.get('n_cicli_segno', 0)
            cols['spin_feedback_arco'] = float(getattr(net, '_spin_feedback_last', 0.0))
            cols['spin_cluster_modulo'] = circ.get('spin_cluster_modulo', 0.0)
            cols['spin_cluster_omega'] = circ.get('spin_cluster_omega', 0.0)
            cols['spin_neel_modulo'] = circ.get('spin_neel_modulo', 0.0)
            cols['spin_neel_omega'] = circ.get('spin_neel_omega', 0.0)
        except Exception:
            pass
        # --- PARAMETRO D'ORDINE SPINORIALE COVARIANTE (globale, INTENSIVO, adimensionale) ---
        # spin_axis_R = |media dei VERSORI di Bloch| in [0,1]: 1 = spinori allineati, 0 = frustrati.
        # A differenza di spin_cluster_modulo (=|somma Bloch|/N, che DILUISCE ~1/sqrt(N) con l'espansione)
        # questa e' una media di versori: NON diluisce con N -> confrontabile a N appaiato (covariante).
        cols['spin_axis_R'] = 0.0
        _nb_g = getattr(net, '_nb', None)
        if _nb_g is not None and len(_nb_g) >= n and n > 0:
            _ax = np.asarray(_nb_g[:n], float)
            _u = _ax / np.maximum(np.linalg.norm(_ax, axis=1, keepdims=True), 1e-12)
            _w = np.maximum(I2, 0.0)
            if _w.sum() > 1e-9:
                cols['spin_axis_R'] = float(np.linalg.norm((_u * _w[:, None]).sum(0) / _w.sum()))
        # --- SEGNO DI DOPPIA-COPERTURA + VERSO, coerenza sugli archi (ORDER PARAMETER, pure-read) ---
        # segno_k = sign(Re<canon(nb_k)|psi_k>) = foglio ±1 che l'orologio pura-fase pilota (riga ~2265):
        # RISPONDE all'orologio, a differenza di spin_axis_R/berry_* (ciechi). Covariante (per-arco, intensivo).
        # Misura VERSO e SEGNO con lo STESSO metodo -> si ordinano INSIEME (un motore) o separati (due)?
        cols['segno_arco_coer'] = 0.0    # <sign_i*sign_j> pesato: +1 concorde, -1 alternato, 0 frustrato
        cols['segno_arco_coer_materia'] = 0.0  # PRESIDIO: <sign_i*sign_j> SOLO archi materia-materia (perc_chi>0): ordine vero vs separazione
        cols['n_arco_materia'] = 0             # PRESIDIO stat: numero archi materia-materia usati (perc_chi>0 su entrambi)
        cols['verso_arco_coer'] = 0.0    # <nb_i·nb_j> pesato: allineamento del verso di Bloch
        cols['segno_ov_absmedia'] = 0.0  # |Re<canon|psi>| medio: commitment a un foglio (intensivo)
        cols['spin_overlap_arco'] = 0.0  # <|<psi_i|psi_j>|^2> pesato: coerenza SU(2) PIENA (verso+segno), pure-read
        _psp = getattr(net, '_psi_spinor', None)
        if (_nb_g is not None and _psp is not None and len(_psp) >= n and len(_nb_g) >= n and n > 0 and len(net.i)):
            try:
                _nbf = np.asarray(_nb_g[:n], float)
                _canon = net._bloch_a_spinore(_nbf)
                _seg = np.real(np.sum(np.conj(_canon) * np.asarray(_psp[:n]), axis=1))  # Re<canon|psi> in [-1,1]
                _sgn = np.sign(_seg)
                _uu = _nbf / np.maximum(np.linalg.norm(_nbf, axis=1, keepdims=True), 1e-12)
                cols['segno_ov_absmedia'] = float(np.mean(np.abs(_seg)))
                _mk = (net.i < n) & (net.j < n)
                if _mk.any():
                    _ii = net.i[_mk]; _jj = net.j[_mk]
                    _wa = net._pesi()[_mk] if hasattr(net, '_pesi') else np.ones(int(_mk.sum()))
                    _dsum = max(float(np.sum(_wa)), 1e-12)
                    cols['segno_arco_coer'] = float(np.sum(_wa * _sgn[_ii] * _sgn[_jj]) / _dsum)
                    # PRESIDIO CRITICO (§5.1): coerenza del SEGNO di doppia-copertura _sgn DENTRO il settore
                    # MATERIA, selezionato con l'etichetta STABILE perc_chi>0 (materia/antimateria = s_k della
                    # firma), NON con _sgn stesso (che darebbe la tautologia _sgn*_sgn=+1). Distingue ORDINE VERO
                    # (sale dentro il solo settore materia) da SEPARAZIONE illusoria (il totale sale solo perche'
                    # gli archi materia-antimateria discordi sono esclusi). Baseline: _sgn scorrelato da perc_chi -> ~0.
                    _pcm = np.sign(np.asarray(net.perc_chi[:n])) if len(net.perc_chi) >= n else np.ones(n)
                    _mm = (_pcm[_ii] > 0) & (_pcm[_jj] > 0)
                    cols['n_arco_materia'] = int(_mm.sum())
                    if _mm.any():
                        _wmm = _wa[_mm]; _dmm = max(float(np.sum(_wmm)), 1e-12)
                        cols['segno_arco_coer_materia'] = float(np.sum(_wmm * _sgn[_ii][_mm] * _sgn[_jj][_mm]) / _dmm)
                    else:
                        cols['segno_arco_coer_materia'] = 0.0
                    cols['verso_arco_coer'] = float(np.sum(_wa * np.sum(_uu[_ii] * _uu[_jj], axis=1)) / _dsum)
                    _psi2 = np.asarray(_psp[:n])
                    _ovl = np.abs(np.sum(np.conj(_psi2[_ii]) * _psi2[_jj], axis=1)) ** 2   # |<psi_i|psi_j>|^2 (coerenza SU(2) piena)
                    cols['spin_overlap_arco'] = float(np.sum(_wa * _ovl) / _dsum)
            except Exception:
                pass
        # SCHERMATURA: osservabili della legge ancorata a N_c. La portata effettiva
        # mostra direttamente la differenza fra nucleo schermato e guscio non schermato.
        try:
            ncrit_scr = float(massa_critica_adattiva(net)) if n and len(net.i) else 0.0
            rho_c_scr = ncrit_scr / max((4.0 / 3.0) * np.pi * LAM**3, 1e-9) if ncrit_scr else 0.0
            lam_eff = net.lambda_nodi() if n and len(net.i) else np.full(n, LAM)
            cols['ncrit_adattivo'] = ncrit_scr
            cols['rho_critica'] = rho_c_scr
            cols['lambda_eff_min'] = float(np.min(lam_eff)) if len(lam_eff) else LAM
            cols['lambda_eff_med'] = float(np.median(lam_eff)) if len(lam_eff) else LAM
            cols['lambda_eff_max'] = float(np.max(lam_eff)) if len(lam_eff) else LAM
            cols['lambda_eff_ratio_med'] = float(np.median(lam_eff) / max(LAM, 1e-9)) if len(lam_eff) else 1.0
            cols['rho_su_rhoc_max'] = float(np.max(I2) / max(rho_c_scr, 1e-9)) if rho_c_scr else 0.0
        except Exception:
            pass
        # conteggi di degenerazione: quanti valori non-finiti o estremi
        cols['n_naninf'] = int(np.sum(~np.isfinite(I2)) + np.sum(~np.isfinite(net.phivel[:n])))
        cols['n_I2_grandi'] = int(np.sum(I2 > 1.0))     # nodi con |Psi|^2 anomalo
        cols['n_lontani'] = int(np.sum(r > 15.0))       # nodi scagliati lontano
        # MISURE PER-MASSA (massa 0 tracciata): isolano la singola massa dall'espansione GLOBALE
        # del sistema, per rispondere a decadimento/equilibrio/divergenza sulla massa VERA.
        m0_I2pesata = 0.0; m0_raggio = 0.0; m0_N = 0; m0_coer = 0.0; m0_spin = 0.0; m0_spin_disp = 0.0
        m0_spin_core = 0.0; m0_spin_core_disp = 0.0
        m0_spin_axis_R = 0.0; m0_omega_axis_R = 0.0; m0_spin_core_cv = 0.0
        m0_Mdyn = 0.0; m0_Mcoh = 0.0; m0_Rinerzia = 0.0; m0_Jrot = 0.0; m0_Jshell_frac = 0.0
        m0_Ncore = 0; m0_Nshell = 0
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
                    # SPIN DEL NUCLEO (TODO Checkpoint): vphi sui soli nodi della MASCHERA DEL NUCLEO,
                    # pesati per l'inerzia |Psi|^2, senza alcuna selezione di chiralita' (perc_chi).
                    if nuc.sum() >= 3:
                        vphi_nuc = vphi_m[nuc]; w_nuc = I2[idx_m][nuc]
                        if w_nuc.sum() > 1e-9:
                            m0_spin_core = float(np.sum(vphi_nuc * w_nuc) / w_nuc.sum())
                            m0_spin_core_disp = float(np.sqrt(np.sum(w_nuc*(vphi_nuc - m0_spin_core)**2)/w_nuc.sum()))
                    # --- OSSERVABILI COVARIANTI del NUCLEO (intensivi, adimensionali) per la sync SU(2) ---
                    # m0_spin_axis_R = |media versori di Bloch| nel nucleo in [0,1] (1=allineati, 0=frustrati):
                    # e' IL parametro d'ordine del Kuramoto spinoriale, non diluisce con N. m0_omega_axis_R =
                    # allineamento degli ASSI degli orologi (omega_s). m0_spin_core_cv = spin_core_disp
                    # normalizzata per la scala di frequenza comovente (mediana |phivel|, gauge) -> adimensionale.
                    _nbm = getattr(net, '_nb', None)
                    if _nbm is not None and len(_nbm) >= n and nuc.sum() >= 3:
                        _axc = np.asarray(_nbm[idx_m][nuc], float)
                        _uc = _axc / np.maximum(np.linalg.norm(_axc, axis=1, keepdims=True), 1e-12)
                        _wc = np.maximum(I2[idx_m][nuc], 0.0)
                        if _wc.sum() > 1e-9:
                            m0_spin_axis_R = float(np.linalg.norm((_uc * _wc[:, None]).sum(0) / _wc.sum()))
                    _omm = getattr(net, 'omega_s', None)
                    if _omm is not None and len(_omm) >= n and nuc.sum() >= 3:
                        _oax = np.asarray(_omm[idx_m][nuc], float)
                        _onrm = np.linalg.norm(_oax, axis=1)
                        _ok = _onrm > 1e-9
                        if _ok.sum() >= 3:
                            _ou = _oax[_ok] / _onrm[_ok][:, None]
                            m0_omega_axis_R = float(np.linalg.norm(_ou.mean(0)))
                    _fscale = float(np.median(np.abs(net.phivel[:n]))) if n > 0 else 0.0
                    m0_spin_core_cv = float(m0_spin_core_disp / _fscale) if _fscale > 1e-9 else 0.0
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
                    # ============ INERZIA E CONGELAMENTO DA GUSCIO (verifica densita' del guscio) ============
                    # Un guscio denso/esteso gonfia J=sum|Psi|^2 r^2 e R=M_dyn/M_coh -> congela la
                    # precessione. Misuro su nucleo+guscio, separando per coerenza col campo della massa.
                    try:
                        d_cm2 = np.linalg.norm(P[:, :2] - cm[:2], axis=1)
                        dom = np.where(d_cm2 < max(4.0*m0_raggio, 3.0))[0]
                        if len(dom) >= 3:
                            Id = I2[dom]; rd = np.linalg.norm(P[dom] - cm, axis=1)
                            fase_m = float(np.angle(np.sum(I2[idx_m] * np.exp(1j*net.phi[idx_m]))))
                            coh = np.cos(net.phi[dom] - fase_m)   # +1 nucleo (in fase), -1 guscio (antifase)
                            m0_Mdyn = float(np.sum(Id))           # massa dinamica (inerzia, senza segno)
                            m0_Mcoh = float(np.sum(Id * coh))     # massa coerente (guscio antifase sottrae)
                            m0_Rinerzia = float(m0_Mdyn / max(abs(m0_Mcoh), 1e-9))
                            Jr = Id * rd**2
                            m0_Jrot = float(np.sum(Jr))           # inerzia rotazionale sum|Psi|^2 r^2
                            shell = coh < 0
                            m0_Jshell_frac = float(np.sum(Jr[shell]) / max(m0_Jrot, 1e-9))
                            m0_Ncore = int(np.sum(~shell)); m0_Nshell = int(np.sum(shell))
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
        cols['m0_spin_core'] = m0_spin_core    # spin sulla MASCHERA DEL NUCLEO, pesato |Psi|^2, no perc_chi
        cols['m0_spin_core_disp'] = m0_spin_core_disp  # dispersione dello spin del nucleo
        cols['m0_spin_axis_R'] = m0_spin_axis_R        # COVARIANTE: |media versori Bloch| nel nucleo [0,1]
        cols['m0_omega_axis_R'] = m0_omega_axis_R      # COVARIANTE: allineamento assi orologi (omega_s) [0,1]
        cols['m0_spin_core_cv'] = m0_spin_core_cv      # COVARIANTE: spin_core_disp / scala freq comovente (adim.)
        cols['m0_Mdyn'] = m0_Mdyn              # sum|Psi|^2 (inerzia dinamica, guscio incluso)
        cols['m0_Mcoh'] = m0_Mcoh              # sum|Psi|^2 cos(phi-phi_m): guscio antifase sottrae
        cols['m0_Rinerzia'] = m0_Rinerzia      # M_dyn/|M_coh|: alto = pesante ma incoerente (guscio)
        cols['m0_Jrot'] = m0_Jrot              # sum|Psi|^2 r^2 = inerzia rotazionale
        cols['m0_Jshell_frac'] = m0_Jshell_frac  # frazione di J dovuta al guscio antifase
        cols['m0_Ncore'] = m0_Ncore
        cols['m0_Nshell'] = m0_Nshell
        cols['m0_vort_pos'] = m0_vort_pos     # numero di vortici (+1)
        cols['m0_vort_neg'] = m0_vort_neg     # numero di antivortici (-1)
        cols['m0_carica'] = m0_carica         # carica topologica netta = SPIN della massa
        cols['m0_coer_nucleo'] = m0_coer_nucleo   # coerenza del solo NUCLEO denso (locale)
        cols['m0_N_nucleo'] = m0_N_nucleo         # solitoni nel nucleo
        cols['m0_raggio_nucleo'] = m0_raggio_nucleo  # raggio del nucleo
        cols['m0_Lz'] = m0_Lz              # rotazione asse pattern per step = PRECESSIONE (spin)
        cols['m0_Lz_norm'] = m0_Lz_norm

        # SPIN DEL PICCO COSTRUTTIVO: misura locale sul picco di |Psi|^2 di ogni massa
        # tracciata. Non sostituisce m*_spin (che resta la velocita' di fase media):
        # qui chi_picco e spin_picco sono rispettivamente chiralita' e Bloch della massa.
        try:
            if getattr(net, 'conc_nodi', None) and getattr(net, 'masse_info', None):
                for i_m, mid in enumerate(sorted(net.masse_info.keys())):
                    idx_picco = []; pesi_picco = []
                    for k in range(min(len(net.conc_nodi), n)):
                        for voce in net.conc_nodi[k]:
                            if voce[0] == mid:
                                idx_picco.append(k); pesi_picco.append(voce[2]); break
                    misura = net.misura_spin_picco_massa(idx_picco, pesi_picco)
                    if misura['picco'] < 0 and 'coorti' in locals() and i_m < len(coorti):
                        # Durante l'inizializzazione il tracking puo' non avere ancora voci
                        # correnti; la coorte di nascita e' il fallback locale deterministico.
                        idx_picco = np.array(sorted(k for k in coorti[i_m] if k < n), dtype=int)
                        misura = net.misura_spin_picco_massa(idx_picco)
                    for nome, valore in misura.items():
                        cols[f'm{i_m}_picco_{nome}'] = round(float(valore), 7)
        except Exception:
            pass

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
                        misura = net.misura_spin_picco_massa(idxA, pesA)
                        for nome, valore in misura.items():
                            cols[f'm{i_lab}_picco_{nome}'] = round(float(valore), 7)
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
                # SCALA COMOVENTE dai BARICENTRI (indipendente da median(d0), che il pavimento tocca):
                # RMS della dispersione dei baricentri dal centroide globale = "taglia" del sistema.
                # Serve a misurare il raggio di precessione COMOVENTE (dist/scala) senza che il
                # pavimento di d0 contamini la scala. r_com_% = distanza fra masse / taglia comovente.
                try:
                    cms = np.array([info[mm[a]]['cm'][:2] for a in range(len(mm))])
                    if len(cms) >= 2:
                        centroide = cms.mean(0)
                        scala_com = float(np.sqrt(np.mean(np.sum((cms - centroide)**2, axis=1)))) or 1e-9
                        cols['scala_com'] = round(scala_com, 4)
                        for a in range(len(mm)):
                            for b in range(a+1, len(mm)):
                                dcom = float(np.linalg.norm(info[mm[b]]['cm'][:2]-info[mm[a]]['cm'][:2]))
                                cols['rcom_%d%d'%(a,b)] = round(dcom/scala_com, 4)  # raggio COMOVENTE
                except Exception:
                    pass
                # ANISOTROPIA s2 media (quota tangenziale della viriale): serve a testare la legge
                # R ~ s2^(2/3)/(1-s2). Da self._sin2_vir se la viriale/freno anisotropo e' attivo.
                if getattr(net, '_sin2_vir', None) is not None and len(net._sin2_vir):
                    cols['s2_medio'] = round(float(np.mean(net._sin2_vir)), 4)
                    cols['s2_max']   = round(float(np.max(net._sin2_vir)), 4)
                # ============ METRICHE COVARIANTI (adimensionali, immuni all'espansione) ============
                # Misurate DENTRO il motore come rapporti alla scala corrente: l'espansione non le
                # inflaziona, quindi le correlazioni fra queste sono FISICHE, non trend spuri.
                #  tw_q      = |tw|/2pi           -> twist in quanti di olonomia (gia' adimensionale)
                #  sync_rel  = <|dw|>/<|w|>       -> desincronizzazione RELATIVA (0=sincroni)
                #  d0_disp   = MAD(d0)/median(d0) -> dispersione della metrica (forma, non taglia)
                #  tw_ratio  = |tw|/median(|tw|)  -> disomogeneita' del twist
                try:
                    ii, jj = net.i, net.j
                    if len(net.tw):
                        cols['tw_q'] = round(float(np.mean(np.abs(net.tw))) / (2*np.pi), 5)
                        med_tw = float(np.median(np.abs(net.tw))) or 1e-9
                        cols['tw_disp'] = round(float(np.median(np.abs(np.abs(net.tw)-med_tw)))/med_tw, 5)
                    if len(net.phivel) >= n and len(ii):
                        pv = net.phivel[:n]
                        dpv = np.abs(pv[ii] - pv[jj])
                        wmean = float(np.mean(np.abs(pv))) + 1e-9
                        cols['sync_rel'] = round(float(np.mean(dpv)) / wmean, 5)
                    if len(net.d0):
                        med_d0 = float(np.median(net.d0)) or 1e-9
                        cols['d0_disp'] = round(float(np.median(np.abs(net.d0-med_d0)))/med_d0, 5)
                except Exception:
                    pass
                # ============ SEPARAZIONE SPAZIALE PER CHIRALITA' (ipotesi guscio/coda) ============
                # Test: le chi=-1 ("spazio"/antiparticelle) stanno FUORI (guscio/coda) e le chi=+1
                # ("materia") DENTRO (nuclei)? Misuro il raggio medio dal centro di massa globale di
                # ciascuna specie, COMOVENTE (diviso la dispersione RMS di tutti i nodi). Se
                # r_chi_neg > r_chi_pos in modo concorde -> le chi=-1 formano il guscio esterno.
                try:
                    Pn = net.pos[:n, :2]
                    if len(net.perc_chi) >= n and n > 10:
                        cen = Pn.mean(0)
                        rr = np.linalg.norm(Pn - cen, axis=1)
                        rms = float(np.sqrt(np.mean(rr**2))) or 1e-9
                        chi = net.perc_chi[:n]
                        mpos = chi > 0; mneg = chi < 0
                        if mpos.sum() > 0 and mneg.sum() > 0:
                            r_pos = float(np.mean(rr[mpos])) / rms   # raggio comovente materia (chi+1)
                            r_neg = float(np.mean(rr[mneg])) / rms   # raggio comovente spazio (chi-1)
                            cols['rchi_pos'] = round(r_pos, 4)
                            cols['rchi_neg'] = round(r_neg, 4)
                            cols['rchi_ratio'] = round(r_neg / max(r_pos, 1e-9), 4)  # >1 = chi-1 piu' esterne (guscio)
                            cols['frac_chi_neg'] = round(float(mneg.mean()), 4)
                except Exception:
                    pass
                # ============ PROFILO DI DENSITA' RADIALE (guscio globale vs nucleo) ============
                # Risponde al dubbio dello ZOOM: la camera puo' stare sempre "dentro la pelle" del
                # guscio e nasconderlo, ma il conteggio dei nodi per raggio no. Divido lo spazio in
                # 5 gusci concentrici comoventi (per frazione del raggio massimo) e conto i nodi in
                # ciascuno, normalizzati per l'area dell'anello (densita' superficiale). FIRMA:
                #  - GUSCIO GLOBALE: densita' bassa al centro, PICCO nell'anello ESTERNO (la pelle).
                #  - NUCLEO/consolidamento: PICCO al centro, densita' che cala verso fuori.
                # Cieco allo zoom: usa raggi veri dei puntatori, non la camera.
                try:
                    Pn2 = net.pos[:n, :2]
                    if n > 20:
                        cen2 = Pn2.mean(0)
                        rr2 = np.linalg.norm(Pn2 - cen2, axis=1)
                        rmax = float(np.percentile(rr2, 98)) or 1e-9      # raggio (robusto agli outlier)
                        bordi = np.linspace(0, rmax, 6)                    # 5 gusci
                        for gi in range(5):
                            in_g = (rr2 >= bordi[gi]) & (rr2 < bordi[gi+1])
                            area = np.pi * (bordi[gi+1]**2 - bordi[gi]**2) or 1e-9
                            cols['dens_g%d'%gi] = round(float(in_g.sum()) / area, 4)  # densita' superf. anello
                        # indice sintetico: densita' anello ESTERNO / densita' anello CENTRALE
                        dc = cols.get('dens_g0', 1e-9); de = cols.get('dens_g4', 0.0)
                        cols['guscio_idx'] = round(de / max(dc, 1e-9), 4)  # >1 = picco esterno (PELLE!)
                except Exception:
                    pass
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
                  'm0_spin_core','m0_spin_core_disp','m0_spin_axis_R','m0_omega_axis_R','m0_spin_core_cv',
                  'm0_Mdyn','m0_Mcoh','m0_Rinerzia','m0_Jrot','m0_Jshell_frac','m0_Ncore','m0_Nshell',
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
    righe = [_metadata_csv,
             "passo,n_tot,ord_centrale,dens_centrale,n_centrali,frac_nati_centrali,"
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
    # ============ DB DI STATO (idempotente + versionato): spezzare i run ============
    import os as _os
    _db = getattr(a, "sync_db", None)
    # Crea automaticamente le directory degli output personalizzati. Gli script
    # .bat le preparano gia', ma un comando diretto deve funzionare anche da una
    # checkout pulita (es. --diaglog out_test/verify.csv).
    for _percorso in (a.csv, diag_path, _db):
        _cartella = _os.path.dirname(_percorso) if _percorso else ""
        if _cartella:
            _os.makedirs(_cartella, exist_ok=True)
    if _db and getattr(a, "db_cleanup", False) and _os.path.exists(_db):
        _os.remove(_db); print(f"[db] --db-cleanup: rimosso {_db}, riparto pulito")
    _db_step0 = 0
    _db_ogni = max(1, int(getattr(a, "db_ogni", 250)))
    # [ARCHIVIO, 2026-09-19] Le opzioni si leggono QUI, dal namespace degli argomenti, e NON
    # diventano globali di modulo: cosi' la FISICA non puo' vederle nemmeno in linea di principio,
    # e la byte-identita' (V1/V2) e' vera per COSTRUZIONE oltre che per misura.
    _db_serie = bool(getattr(a, "db_serie", False))
    _db_rig = getattr(a, "db_rigioca", None)
    _db_scritti = _db_saltati = _db_falliti = 0
    _db_passi_fine = int(passi)
    if _db_rig and not _db_serie:
        raise SystemExit("[db] --db-rigioca richiede --db-serie: senza la serie non c'e' archivio "
                         "da infittire, e si sovrascriverebbe l'unico file.")
    if _db and _db_serie:
        # IL DISCRIMINANTE E' IL BLOB: si verifica la FISICA di ogni snapshot, non la cadenza.
        _ser, _guaio = _db_serie_verifica(_db, net._versione_codice())
        if _guaio:
            raise SystemExit("[db] RIFIUTO DI PARTIRE: %s\n"
                             "     Mescolare due FISICHE renderebbe l'archivio non interpretabile. "
                             "Usa una cartella pulita, --db-cleanup, o la versione del codice che "
                             "ha scritto quegli snapshot." % _guaio)
        if _db_rig:
            _da, _aa = int(_db_rig[0]), int(_db_rig[1])
            _p = _db_serie_path(_db, _da)
            if not _os.path.exists(_p):
                raise SystemExit("[db] RIFIUTO: lo snapshot di partenza %s non esiste." % _p)
            net.carica_stato(_p)
            _db_step0 = int(getattr(net, "_db_step", 0))
            _db_passi_fine = _aa
            if _db_step0 != _da:
                raise SystemExit("[db] RIFIUTO: il passo NEL FILE (%d) non e' quello NEL NOME (%d)."
                                 % (_db_step0, _da))
            print(f"[db] RIGIOCA: caricato {_p} (passo {_db_step0}), rigioco fino a {_aa}. "
                  f"Gli snapshot esistenti NON si sovrascrivono: si saltano e si contano.")
        elif _ser:
            _s, _p = _ser[-1]
            net.carica_stato(_p)
            _db_step0 = int(getattr(net, "_db_step", 0))
            print(f"[db] serie: {len(_ser)} snapshot presenti, riprendo dal piu' alto {_p} "
                  f"(passo {_db_step0}), nodi={net.n}")
        else:
            print(f"[db] serie: nessuno snapshot presente, parto da zero. Cadenza --db-ogni={_db_ogni}.")
    elif _db and _os.path.exists(_db):
        try:
            net.carica_stato(_db)
            _db_step0 = int(getattr(net, "_db_step", 0))
            print(f"[db] stato CARICATO da {_db}: riprendo da step interno {_db_step0}, nodi={net.n}")
        except RuntimeError as _e:
            print(f"[db] {_e}"); raise
    # diaglog: se RESUME (_db_step0>0) apro in APPEND e NON riscrivo l'header (continuita');
    # se fresh apro in WRITE. Cosi' il diaglog e' continuo attraverso i resume.
    if diag_path:
        _resume = _db_step0 > 0 and _os.path.exists(diag_path)
        if _resume:
            # tolgo l'eventuale OVERLAP: righe con step >= _db_step0 (il primo run puo' essere
            # proseguito oltre l'ultimo salvataggio DB). Tengo header + righe con step < _db_step0,
            # poi il loop appende da _db_step0 in avanti. Niente duplicati.
            try:
                _righe = open(diag_path).read().splitlines()
                _meta = _righe[0] if _righe and _righe[0].startswith("# RUN_PARAMS ") else _metadata_csv
                _hdr_idx = 1 if _righe and _righe[0].startswith("# RUN_PARAMS ") else 0
                _hdr = _righe[_hdr_idx] if len(_righe) > _hdr_idx else ""
                _data = _righe[_hdr_idx + 1:]
                _tenute = [_meta, _hdr] + [r for r in _data
                                            if r and r.split(",")[0].isdigit() and int(r.split(",")[0]) < _db_step0]
                open(diag_path, "w").write("\n".join(_tenute) + "\n")
            except Exception:
                pass
        diag_f = open(diag_path, "a" if _resume else "w")
        if not _resume:
            diag_f.write(_metadata_csv + "\n")
            diag_f.flush()
        if _resume:
            _diag_header = "GIA_SCRITTO"   # marca: non riscrivere l'header in append
        print(f"[batch] LOG DIAGNOSTICO COMPLETO {'(APPEND, resume)' if _resume else ''} -> {diag_path}")
    # TRACING SEGNO (--trace-segno): dump per-passo pure-read (zero mutazioni) per capire la cancellazione.
    trace_path = getattr(a, "trace_out", None) or ((diag_path + ".trace.csv") if diag_path else None)
    trace_f = None
    if bool(getattr(a, "trace_segno", False)) and trace_path:
        _os.makedirs(_os.path.dirname(trace_path) or ".", exist_ok=True)
        trace_f = open(trace_path, "w")
        trace_f.write("step,n,nati,coppie,s_abs_mean,frac_s_pos,archi_concordi,segno_arco,"
                      "torque,twn_su2pi,frac_twn_gt2pi,corr_sign_twn,corr_sign_nbz,s_firmata_mean\n")
        trace_f.flush()
        print(f"[trace-segno] dump per-passo (pure-read) -> {trace_path}")
    # RESUME CORRETTO: se ripreso dal DB a _db_step0, fai solo i passi RIMANENTI per arrivare al
    # totale 'passi' (non altri 'passi' interi), e numera il diaglog in CONTINUO (_db_step0 + step).
    _rimanenti = max(0, _db_passi_fine - _db_step0)
    if _db_step0 > 0:
        print(f"[db] resume: {_db_step0} passi gia' fatti, ne mancano {_rimanenti} per arrivare a {passi}")
    for step in range(_rimanenti + 1):
        _step_glob = _db_step0 + step   # passo GLOBALE (continuo attraverso i resume)
        if step > 0:
            _passo(net)
        # DB: salva periodicamente (default ogni 250 passi, configurabile con --db-ogni) cosi'
        # un run interrotto e' riprendibile senza perdere troppo lavoro.
        if _db and step > 0 and _step_glob % _db_ogni == 0:
            net._db_step = _step_glob
            # [ARCHIVIO] UNA RIGA AL PUNTO DI CHIAMATA: `salva_stato` non sa niente della serie.
            _p_db = _db_serie_path(_db, _step_glob) if _db_serie else _db
            if _db_rig and _os.path.exists(_p_db):
                # LA RIGIOCATA NON DISTRUGGE L'ARCHIVIO: salta e conta (A8, si dichiara a fine run).
                _db_saltati += 1
            else:
                try:
                    net.salva_stato(_p_db)
                    _db_scritti += 1
                except Exception as _e_db:
                    # UN SALVATAGGIO CHE FALLISCE IN SILENZIO E' IL DIFETTO PEGGIORE QUI.
                    _db_falliti += 1
                    print(f"[db] ⚠ SALVATAGGIO FALLITO a {_p_db}: {_e_db}", flush=True)
        if diag_f is not None:
            # IL DIAGLOG E' SOLO LETTURA: non deve mutare lo stato fisico. Le funzioni diagnostiche
            # ricalcolano/aggiornano cache di CONTINUITA' che la DINAMICA legge: self.psi (da _pesi ->
            # lambda_nodi), self._psi_prec (da ritmo(), tempo proprio), self._spinor_lift (feedback
            # spinoriale). Sotto --campo-spinoriale ANCHE psi_spin/rho_spin/_psi_spin_prec (ritmo 4pi,
            # _rho_sorgente, _nb_grav) e lo stato RNG (se una misura consuma random). Snapshot+restore
            # garantiscono byte-identita' della fisica con/senza diaglog.
            _snap_rng = net.rng.bit_generator.state
            _snap_fisica = {k: getattr(net, k) for k in ('psi', '_psi_prec', '_spinor_lift', '_psi_spinor', '_nb', '_nb_prec', '_nb_ret', 'omega_s', 'phi_s', 'psi_spin', 'rho_spin', '_psi_spin_prec') if hasattr(net, k)}
            d = _diag_completa(net, _step_glob); d['step'] = _step_glob
            # Tracking esplicito del picco costruttivo: usa conc_nodi, che include
            # i figli della mitosi, e la coorte solo come fallback iniziale.
            for i_m, (mid, coorte) in enumerate(zip(ids_massa, coorti)):
                idx_coorte, pesi_coorte = net.indici_massa_vivi(mid, coorte)
                misura = net.misura_spin_picco_massa(idx_coorte, pesi_coorte)
                for nome, valore in misura.items():
                    d[f'm{i_m}_picco_{nome}'] = round(float(valore), 7)
                confronto = net.misura_spin_picco_per_chiralita(idx_coorte, pesi_coorte)
                for nome in ('spin_plus', 'spin_minus', 'contrasto', 'q_x', 'q_y', 'q_z',
                             'q_modulo', 'n_plus', 'n_minus'):
                    d[f'm{i_m}_picco_{nome}'] = round(float(confronto[nome]), 7)
                if SPIN_POSITIVI:
                    misura_pos = net.misura_spin_picco_positivi(idx_coorte, pesi_coorte)
                    for nome, valore in misura_pos.items():
                        d[f'm{i_m}_picco_pos_{nome}'] = round(float(valore), 7)
            for _k, _v in _snap_fisica.items():   # RESTORE: il diaglog non lascia tracce sulla fisica
                setattr(net, _k, _v)
            net.rng.bit_generator.state = _snap_rng   # RESTORE RNG: byte-identita' con/senza diaglog
            if _diag_header is None or _diag_header == "GIA_SCRITTO":
                # ordine: colonne fisse note, poi le extra multimassa/interazione in coda
                extra = [k for k in d.keys() if k not in _DIAG_COLS]
                _scrivi_intestazione = (_diag_header is None)   # solo se fresh, non in append/resume
                _diag_header = list(_DIAG_COLS) + extra
                if _scrivi_intestazione:
                    diag_f.write(",".join(_diag_header) + "\n")
            diag_f.write(",".join(str(d.get(c, '')) for c in _diag_header) + "\n")
            diag_f.flush()   # flush a ogni step: se il run si blocca, il log fino al blocco e' salvo
        if trace_f is not None:
            # TRACING SEGNO: SOLO LETTURA (getattr + numpy, nessuna funzione mutante) -> non tocca la fisica.
            _tn = net.n
            _tpsi = np.asarray(getattr(net, '_psi_spinor', np.zeros((_tn, 2), complex)))[:_tn]
            _tnb = np.asarray(getattr(net, '_nb', np.zeros((_tn, 3))))[:_tn]
            _ti = net.i; _tj = net.j; _ttw = np.asarray(net.tw); _tdeg = np.asarray(net._deg)[:_tn]
            if len(_tpsi) >= _tn and len(_tnb) >= _tn and _tn > 0 and len(_ti):
                _tmk = (_ti < _tn) & (_tj < _tn); _tii = _ti[_tmk]; _tjj = _tj[_tmk]
                _tcanon = net._bloch_a_spinore(_tnb)
                _ts = np.real(np.sum(np.conj(_tcanon) * _tpsi, axis=1))
                _tsg = np.sign(_ts); _tprod = _tsg[_tii] * _tsg[_tjj]
                _ttwn = np.zeros(_tn); np.add.at(_ttwn, _ti, np.abs(_ttw)); np.add.at(_ttwn, _tj, np.abs(_ttw))
                _ttwn = _ttwn / np.maximum(_tdeg, 1)
                _tacc = np.zeros((_tn, 2), complex); np.add.at(_tacc, _tii, _tpsi[_tjj]); np.add.at(_tacc, _tjj, _tpsi[_tii])
                _ttorq = np.linalg.norm(_tacc, axis=1) / np.maximum(_tdeg, 1)
                def _tcc(x, y):
                    x = x - x.mean(); y = y - y.mean(); dn = np.sqrt((x * x).sum() * (y * y).sum())
                    return float((x * y).sum() / dn) if dn > 0 else 0.0
                _trow = [_step_glob, _tn, int(getattr(net, 'nati', 0)), int(getattr(net, 'coppie_nate', 0)),
                         float(np.mean(np.abs(_ts))), float(np.mean(_tsg > 0)), float(np.mean(_tprod > 0)),
                         float(np.mean(_tprod)), float(np.mean(_ttorq)), float(np.mean(_ttwn) / (2 * np.pi)),
                         float(np.mean(_ttwn > 2 * np.pi)), _tcc(_tsg, _ttwn), _tcc(_tsg, _tnb[:, 2]), float(np.mean(_ts))]
                trace_f.write(",".join(str(x) for x in _trow) + "\n"); trace_f.flush()
        if step % ogni == 0:
            # MISURA SOLA-LETTURA: la condensazione ricalcola psi e chiama misure per diagnostica;
            # snapshot/restore dei cache di CONTINUITA' che la DINAMICA legge (stesso set del diaglog +
            # cache campo-spinoriale + RNG), cosi' --ogni NON contamina il tempo proprio (ritmo() al passo
            # dopo legge self.psi/_psi_prec/_psi_spin_prec).
            _snap_cond_rng = net.rng.bit_generator.state
            _snap_cond = {k: getattr(net, k) for k in ('psi', '_psi_prec', '_spinor_lift', '_psi_spinor', '_nb', '_nb_prec', '_nb_ret', 'omega_s', 'phi_s', 'psi_spin', 'rho_spin', '_psi_spin_prec') if hasattr(net, k)}
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
            for _k, _v in _snap_cond.items():   # RESTORE: la misura condensazione non lascia tracce sulla fisica
                setattr(net, _k, _v)
            net.rng.bit_generator.state = _snap_cond_rng   # RESTORE RNG: --ogni non contamina lo stream
    dt = _t.time() - t0
    if diag_f is not None:
        diag_f.close()
        print(f"[batch] log diagnostico completo salvato in {diag_path}")
    with open(a.csv, "w") as f:
        f.write("\n".join(righe) + "\n")
    print(f"\n[batch] completato in {dt:.1f}s, {passi} passi. CSV salvato in {a.csv}")
    # [ARCHIVIO, 2026-09-19] IL CONTEGGIO SI DICHIARA. Era gia' contato e MAI STAMPATO: il commento
    # diceva "si dichiara a fine run" e non lo faceva (difetto D1, commit 312a3b4). Un ramo
    # silenzioso non e' un ramo (A8), e con il disco al 96 % un salvataggio fallito che non si
    # vede e' il difetto peggiore possibile per un archivio: te ne accorgeresti a run finito.
    if _db and (_db_scritti or _db_saltati or _db_falliti):
        print(f"[db] ARCHIVIO: {_db_scritti} snapshot scritti, {_db_saltati} saltati "
              f"(gia' presenti), {_db_falliti} FALLITI.")
        if _db_falliti:
            print(f"[db] *** ATTENZIONE: {_db_falliti} SALVATAGGI SONO FALLITI. L'ARCHIVIO E' "
                  f"INCOMPLETO: i passi mancanti NON sono recuperabili senza rigirare. ***")
    print("[batch] LETTURA condensazione: se dens_centrale e n_centrali CRESCONO e frac_nati resta")
    print("        ALTA mentre dist_masse NON crolla -> NUOVA massa dal vuoto (non accrescimento).")
    print("[batch] LETTURA picchi_nuovi: se picchi_nuovi passa da 0 a >=1 a un certo passo, quello e'")
    print("        il momento in cui una MASSA NUOVA si stacca dal vuoto (materia isolata che si crea).")
    print("[batch] LETTURA antiguscio: se compare un anello a coerenza_min BASSA (antifase) e raggio")
    print("        stabile oltre le masse, con nodi presenti -> GUSCIO DI ANTIFASE che avvolge i nuclei")
    print("        = massa di scala superiore (il guscio del sistema e antifase, non materia).")


def _avvisa_leggi_in_uso():
    """AVVISA se il run NON usa le leggi che Luca ha deciso di TENERE IN USO.

    **Decisione di Luca del 2026-09-27:** `VERLET` e il `REGIME` deterministico **si tengono
    come sono** -- nessuna archiviazione, nessun cambiamento -- e **l'importante e' che siano
    USATI**. Quindi un run che parte senza di loro **lo dice in chiaro**.

    ⚠⚠ **E' UN AVVISO, NON UN PRESIDIO** (`A9`): **non impedisce niente.** Luca l'ha
    chiesto cosi' (<<avviso, non blocco>>), e chi conta i presidi **non lo deve contare fra
    loro**. Un avviso vale quanto l'attenzione di chi legge lo stdout.

    Sta in coda a `_applica_regime` e **su entrambi i rami**, perche' `--regime` si applica
    DOPO `_applica_flag`: un controllo messo li' leggerebbe il `REGIME` di testa al file e
    **direbbe la cosa sbagliata proprio quando conta**.
    """
    # ⚠ I FLAG INERTI ACCESI: un flag che non fa niente e che qualcuno accende e' una
    #   ASPETTATIVA TRADITA, non un dettaglio. Si dichiara, e si dice DOVE e' finito.
    _inerti = []
    if L_CONSERVA:
        _inerti.append("L_CONSERVA: il suo ramo e' ARCHIVIATO in "
              "csv/_archivio/_l_conserva.py (era marcato <<ERRATA, NON usare>>: "
              "azzerava la precessione fisica reale). Il flag NON FA NIENTE.")
    if MITOSI_2LAM:
        _inerti.append("MITOSI_2LAM: il suo cancello e' diventato LEGGE INCONDIZIONATA "
              "nel commit `6b` (2026-10-04), e il ramo <<senza il flag>> e' "
              "ARCHIVIATO in csv/_archivio/_rami_off_cura2.py. Il flag NON FA "
              "NIENTE: un arco si divide SOLO se FRAZ_NASCITA*d >= LAM E "
              "(1-FRAZ_NASCITA)*d >= LAM, con o senza di lui.")
    if PAV_COM:
        _inerti.append("PAV_COM: il pavimento di d0 e' ARCHIVIATO in "
              "csv/_archivio/_pavimenti_morti.py. La garanzia sulle lunghezze e' LAM.")
    if SYNC_UPDATE:
        _inerti.append("SYNC_UPDATE: i suoi rami sono ARCHIVIATI in "
              "csv/_archivio/_sync_update.py. Il suo raggio era UNA legge su cinque.")
    if _inerti:
        print("[flag-inerti] ⚠ %d FLAG ACCESI CHE NON FANNO NIENTE:"
              % len(_inerti), flush=True)
        for _f in _inerti:
            print("[flag-inerti]    - " + _f, flush=True)
    _manca = []
    if not VERLET:
        _manca.append("VERLET e' SPENTO: il sottociclo metrico gira con EULERO ESPLICITO. "
              "`CENS-B8` -- il ramo detto <<sperimentale>> E' il percorso vivo, e Luca ha "
              "deciso di TENERLO. Un run senza Verlet non e' il percorso in uso.")
    if REGIME != "deterministico":
        _manca.append("il REGIME e' '%s' e non 'deterministico'. Il regime deterministico "
              "e' quello in uso per decisione di Luca (`COMPONENTI:C3`), e cambia QUATTRO "
              "interruttori insieme: SCUOTIMENTO, G_PH, TAU_A, calore_init." % REGIME)
    if _manca:
        print("[leggi-in-uso] ⚠ AVVISO (non blocco): questo run NON usa %d delle leggi "
              "che Luca ha deciso di tenere in uso." % len(_manca), flush=True)
        for _m in _manca:
            print("[leggi-in-uso]    - " + _m, flush=True)
    else:
        print("[leggi-in-uso] VERLET attivo e REGIME deterministico: le leggi in uso ci sono.",
              flush=True)


def _applica_regime(a):
    """Applica il --regime da riga di comando, rivalutando i globali che dipendono dal REGIME
    (SCUOTIMENTO, G_PH, TAU_A, _CALORE_INIT), valutati al caricamento del modulo prima del parsing.
    Vale per headless e interattivo: va chiamata dopo il parsing e prima di evolvere la rete."""
    reg = getattr(a, "regime", None)
    if reg is None:
        # nessun override: resta il REGIME di testa al file. MA L'AVVISO GIRA COMUNQUE --
        #   un `return` secco qui lo salterebbe proprio nel caso piu' comune.
        _avvisa_leggi_in_uso()
        return
    global REGIME, SCUOTIMENTO, G_PH, TAU_A, _CALORE_INIT
    REGIME = reg
    if reg == "deterministico":
        SCUOTIMENTO = False; G_PH = 3e-3; TAU_A = 50.0; _CALORE_INIT = 0.4
    else:
        SCUOTIMENTO = True;  G_PH = 0.15; TAU_A = 2.0;  _CALORE_INIT = 0.0
    print(f"[regime] '{reg}' da riga di comando: SCUOTIMENTO={SCUOTIMENTO} G_PH={G_PH} "
          f"TAU_A={TAU_A} calore_init={_CALORE_INIT}", flush=True)
    _avvisa_leggi_in_uso()


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
