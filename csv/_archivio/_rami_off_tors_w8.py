# -*- coding: utf-8 -*-
"""I RAMI CHE ESCONO con la cura di `TORS-W8-AVVOLGIMENTO` (2026-10-06).

### ⛔ **COPIATI VERBATIM dal blob di PRIMA** *(`f7237563`, dal commit `5c46856`,
estratto con `git cat-file -p` in **binario**)*, non riscritti a memoria -- e il
generatore ha **ASSERITO** che ogni blocco compaia **esattamente una volta** in quel blob.
### **Questo file NON GIRA e non va importato: e' un ARCHIVIO.**

### ⚠ **E A DIFFERENZA DELL'ARCHIVIO DELLA `CURA 2` DI `Z43`, qui i rami erano VIVI:**
il blocco della torsione del ramo `TORS_4PI` ### **girava a ogni passo su ogni arco**, e
`_allaccia` gira alla semina. ### **Non e' codice morto che esce: e' una legge che viene**
### **sostituita.**

### ⚠ **E I BLOCCHI STANNO FRA APICI SINGOLI TRIPLI, non doppi:** il corpo di
`_tau_tw_locale` ### **contiene la sua docstring**, e un delimitatore doppio la
chiuderebbe a meta'. ### **Il generatore lo ASSERISCE invece di sperarlo.**

**Il simulatore di prima si rilancia dal tag** ### **`pre-tors-w8-cura`**, e i byte esatti
si recuperano con `git cat-file -p pre-tors-w8-cura:soliton_simulator.py`
### **in BINARIO** *(par.7: `git checkout` ha la trappola `CRLF`)*.
"""

# ESENTE-H-P8: un FALSO POSITIVO, e lo DICHIARO invece di spostare il testo per schivarlo.
#   Il rilevatore cerca `cat-file` dentro una STRINGA con una parola tipo <<prima>> vicino:
#   qui la stringa e' LA DOCSTRING DI UN ARCHIVIO, che ### NON GIRA, non si importa e non
#   estrae niente. Dice al lettore COME recuperare i byte, e nomina IL TAG, non `HEAD`.
#   ### E IL GEMELLO `_rami_off_z43_cura2.py` NON INCIAMPA, ma non per una differenza di
#   sostanza: la sua stessa istruzione sta in un COMMENTO, che l'AST non vede. Potevo
#   spostare la mia riga in un commento e passare il controllo in silenzio:
#   ### NON LO FACCIO -- sarebbe schivare un presidio sfruttando un accidente del
#   rilevatore, e la traccia in `doc/ESENZIONI_presidi.md` vale piu' del commit pulito.
#   E' la SETTIMA volta per questa famiglia, e la sesta e' nel patch di questa stessa cura.

# ==============================================================================================
# IL BLOCCO DELLA TORSIONE, ramo `TORS_4PI` -- LA LEGGE SOSTITUITA
# ==============================================================================================
#   `_w8` ha periodo 8pi e l'avvolgimento di `dph` e' di 4pi: un salto di 4pi NON e' un
#   multiplo del suo periodo, quindi NON viene riparato. MISURATO: 142114 calci di modulo
#   4pi ESATTI in 150 passi (eebe24f), e il ramo non-4pi ripara entro 1.9e-15.
#   E `twp` portava LA SOMMA AVVOLTA `_w8(dph + twist_dip)`, mentre il ramo non-4pi ci
#   scriveva `dph`: UN NOME, DUE SIGNIFICATI. Dopo la cura ne ha UNO.
RAMO_TORSIONE_4PI = r'''
            _ttw = _tau_tw_locale(self) if TAU_LOCALI else TAU_TW
            self.tw += self._w8(dph + twist_dip - self.twp) - dt_e * self.tw / _ttw
            self.twp = self._w8(dph + twist_dip)
'''

# ==============================================================================================
# `_allaccia` (la SEMINA) -- IL CALCIO DI NASCITA DELLA SCENA
# ==============================================================================================
#   `twp = 0` NON e' <<nessuna storia>>: e' <<fase precedente ZERO>>, quindi al primo
#   passo la spinta valeva `dph + twist_dip - 0`. MISURATO al passo 1 su f7237563: spinta
#   mediana 3.0950, MASSIMA 9.4248 = 3pi ESATTO -- il massimo possibile di
#   |dph + twist_dip|, cioe' IL CALCIO SATURAVA IL SUO LIMITE TEORICO.
#   E col tempo di scarica di 309 passi, in 150 passi ne sopravviveva il 61.5%: LA
#   TORSIONE DELLA RETE ERA QUASI TUTTA QUESTO.
RAMO_ALLACCIA_SEMINA = r'''
        self.tw = np.concatenate([self.tw, np.zeros(len(dd))])
        self.twp = np.concatenate([self.twp, np.zeros(len(dd))])
'''

# ==============================================================================================
# `_tau_tw_locale` -- LA GUARDIA CHE NESSUNO CONTAVA
# ==============================================================================================
#   Il `return TAU_TW` del ramo di guardia era il TERZO consumatore di `TAU_TW`, e nessun
#   contatore lo vedeva (rilievo `E4` del guardiano). Se scattasse, tau_tw passerebbe da
#   ~2-6 (misurato: 2.4055 al passo 50) a 20: un fattore 3-10 sul tetto di equilibrio.
#   ### LA CURA NON CAMBIA IL VALORE RESTITUITO: aggiunge i quattro contatori di `A8`,
#   byte-inerti. QUINDI QUESTO RAMO NON ESCE -- entra in OSSERVAZIONE, ed e' qui perche'
#   chi legge veda com'era prima dei contatori.
RAMO_TAU_TW_PRIMA_DEI_CONTATORI = r'''
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
'''

# ==============================================================================================
# CHE COSA **NON** ESCE, e dirlo e' il punto
# ==============================================================================================
#   - IL RAMO NON-4PI (`_w4(dph - twp)` con `twp = dph`): NON si tocca, e NON aveva il
#     difetto -- `_w4` ha periodo 4pi, lo STESSO di `_wphi`, quindi ripara. Dopo la cura
#     i due rami scrivono LA STESSA COSA in `twp`.
#   - LE DUE REGOLE DI NASCITA di `twp` (`_rn_div_twp`, `_rn_sch_twp`): restano, perche'
#     il ramo non-4pi le usa e col marcatore il ramo 4pi non le legge piu'. Togliere una
#     riga che non fa piu' danno e' un RITOCCO, non una cura, e andrebbe in un commit suo.
#   - I 45 LETTORI di `tw`: la semantica di `tw` non cambia (resta l'ACCUMULO), cambia
#     come si calcola il suo INCREMENTO. Sono due cose diverse.
