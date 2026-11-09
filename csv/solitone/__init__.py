# -*- coding: utf-8 -*-
r"""**LA CASSETTA DEGLI ATTREZZI DEL SOLITONE** *(il mandato di Luca delle `01:22` del `2026-11-01`; il task history `doc/TASK_HISTORY/2026-11-01_cassetta_solitone.md`)*:
### **un modulo per tema, le STESSE espressioni degli strumenti che hanno prodotto i referti, e i test che lo verificano AL BIT.**

    uscite    le uscite (n0)-(n3), le coppie dispersive, i margini; lo spettro SOLO dalla scena
    protetto  la scena, la coppia di B a Gamma, la scelta dentro la coppia, l'inviluppo, A a K, mu di Rayleigh
    misure    il cuore (netto e liscio), w, l'alone, il baricentro; le bande di D, le rotazioni, il periodo col passo;
              la forma della crescita, la vita, il limite del tasso
    vuoto     le bande del vuoto attorno a F0 (il tick intero con psi = 0), dove cade una frequenza, il margine
    respiro   la serie densa del cuore (il tick intero, a ogni tick), Omega dai picchi, le frequenze sul cerchio (il margine, la somma di due bande)
    accensione il tick col vuoto acceso di lam (la rampa sin^2), mu di Rayleigh del tick intero, la vita a meta' del cuore
    toro       le misure sul toro: il centro periodico (la media circolare sugli indici), l'immagine piu' vicina, l'alone per settore

    python csv/solitone/collauda.py > doc/referti_l2/cassetta_solitone.txt

### **Nessun file del nucleo; gli script vecchi restano come sono, coi loro referti.**
"""
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
CSV = os.path.dirname(_QUI)
RADICE = os.path.dirname(CSV)
_PO = os.path.join(RADICE, "primo_ordine")
for _p in (CSV, _PO, os.path.join(_PO, "leggi")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

# ### P3 (Luca 2026-11-09 13:16; il task history del prototipo, sez. 20): sul ramo primo-ordine congelato, cs ACCESO e' vietato (energia_pesata.applica alza)
from solitone import ramo as _ramo  # noqa: E402
_ramo.vieta_cs()
