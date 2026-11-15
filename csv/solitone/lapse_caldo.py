# -*- coding: utf-8 -*-
r"""**LA PARTENZA A CALDO DEL PUNTO FISSO DEL LAPSE** *(7-bis; Luca `2026-11-15` `12:04`, A1; la carta `doc/TASK_HISTORY/2026-11-13_strumento_mattone.md`, sez. `24`)*.

### **Un ADATTATORE, fuori dal nucleo:** **`accendi("caldo")` sostituisce IN MEMORIA `tick_lapse.cs_al_centro` con `cs_al_centro_caldo`: lo STESSO corpo** *(la stessa tolleranza `EPS_CS`, lo stesso `GIRI_MAX`, lo
stesso `omega`)*, **cambia SOLO la partenza: `prec` = il `cs` a cui e' arrivato il punto fisso del tick PRECEDENTE** *(`STATO["cs"]`; al primo tick, se non c'e', la partenza di oggi `cs_di` dello stato)*.
**`accendi("freddo")`: l'originale com'e', avvolto solo per CONTARE i giri** *(e tenere il `cs` a cui arriva: cosi' una corsa a freddo puo' passare a caldo)*. **`spegni()` rimette l'originale.**
### **Chi lo chiama:** **`p6_bracci.tick_GU`** *((MGU), attraverso il modulo)* **e `tick_lapse.tick`** *((MG), per nome nel suo modulo)*: **tutti e due vedono la sostituzione.**
### **La ripartenza:** **`STATO["cs"]` fa parte dello stato della corsa: si salva come `cs_prec` accanto allo stato e si rimette con `metti_cs`.** **A caldo le corse NON sono uguali al bit a quelle a freddo, solo
entro la tolleranza del punto fisso** *(dichiarato, Luca A3)*.
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_CSV = os.path.dirname(_QUI)
for _p in (_QUI, _CSV):
    if _p not in sys.path:
        sys.path.insert(0, _p)
from solitone import tick_lapse as TL  # noqa: E402

_ORIGINALE = TL.cs_al_centro
STATO = {"cs": None, "giri": [], "modo": None}


def cs_al_centro_caldo(mot, st, par, s, legge, senza_reazione, omega=1.0, giri_max=None, storia=None):
    """### **`tick_lapse.cs_al_centro` riga per riga, la partenza a caldo.** `(cs, giri)`."""
    TK = TL.TK
    meta = TK.meta_del_palindromo()
    prec = STATO["cs"].copy() if STATO["cs"] is not None else TL.cs_di(mot, st, s, legge)     # ### LA SOLA DIFFERENZA
    for giri in range(1, (TK.GIRI_MAX if giri_max is None else giri_max) + 1):
        copia = {k: (v.copy() if hasattr(v, "copy") else v) for k, v in st.items()}
        mot.cs = prec
        mot.lambda_c = None
        if not senza_reazione:
            TL.reazione(mot, copia, par, s, legge, 0.5)
        TK.percorri_tick(copia, mot, par, (), None, meta)
        nuovo = TL.cs_di(mot, copia, s, legge)
        scarto = float(np.max(np.abs(nuovo - prec)))
        if storia is not None:
            storia.append(scarto)
        if scarto <= TK.EPS_CS * float(np.max(np.abs(nuovo))):
            STATO["cs"] = nuovo.copy()
            STATO["giri"].append(giri)
            return nuovo, giri
        prec = nuovo if omega == 1.0 else prec + omega * (nuovo - prec)
    raise AssertionError("il punto fisso di cs del lapse (a caldo) NON converge in %d giri (ultimo scarto %.3e)" % (giri, scarto))


def cs_al_centro_freddo(*a, **kw):
    """### **L'originale com'e'**; conta i giri e tiene il `cs` a cui arriva."""
    cs, giri = _ORIGINALE(*a, **kw)
    STATO["cs"] = cs.copy()
    STATO["giri"].append(giri)
    return cs, giri


def accendi(modo, cs=None):
    """### `modo` `"caldo"` o `"freddo"`; `cs` la partenza del primo tick a caldo *(il `cs_prec` salvato)*; i giri si azzerano."""
    assert modo in ("caldo", "freddo")
    STATO["modo"] = modo
    STATO["giri"] = []
    STATO["cs"] = None if cs is None else np.array(cs, dtype=float).copy()
    TL.cs_al_centro = cs_al_centro_caldo if modo == "caldo" else cs_al_centro_freddo


def spegni():
    TL.cs_al_centro = _ORIGINALE
    STATO["modo"] = None


def cs_prec():
    """### Il `cs` da salvare accanto allo stato *(`None` se non c'e' ancora)*."""
    return None if STATO["cs"] is None else STATO["cs"].copy()
