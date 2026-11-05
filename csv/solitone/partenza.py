# -*- coding: utf-8 -*-
r"""**LA PARTENZA DEL MOTO E L'ARRESTO** *(Luca `2026-11-05` `14:14`; il task history `doc/TASK_HISTORY/2026-11-05_TL120_densita_o_rientro.md`, 4 e 5)*
### **La partenza:** il primo blocco di `PASSO` con la velocita' sopra `SOGLIA` per `1000`; **l'arresto:** `DOPO` unita' di tempo dopo l'inizio di quel blocco.
### **La definizione e' quella delle tabelle dei referti** *(`carta_deriva.finestre` su `carta_tf3_lunga.traiettoria`)*: il centro periodico srotolato *(le differenze di `c1`, `c2` riportate in
`[-L/2, L/2)`, sommate in ordine dal primo campione)*, la velocita' per blocco `1000 hypot(pendenza(t, X), pendenza(t, Y))` sui campioni con `t` in `[a, a + PASSO)`, almeno `3`, i blocchi da `0`.
**Qui si aggiorna campione per campione** *(per la corsa: lo stato e' un dict serializzabile, portato da un pezzo all'altro come quello di `giro`)*, **con le stesse operazioni** *(i test: `test_partenza`)*.
"""
import math

import numpy as np

SOGLIA = 5.0                   # ### Luca 14:14: la velocita' per 1000 sopra cui il moto e' partito
PASSO = 1000.0                 # ### Luca 14:14: i blocchi di 1000
DOPO = 2000.0                  # ### Luca 14:14: l'arresto 2000 unita' di tempo dopo la partenza


def nuovo():
    """### **Lo stato iniziale:** il blocco aperto da `0`, lo srotolamento da zero, nessuna partenza."""
    return {"a": 0.0, "tt": [], "x": [], "y": [], "c": None, "u": [0.0, 0.0], "blocchi": [], "t_p": None}


def _chiudi(st, pendenza):
    if len(st["tt"]) >= 3:
        tt = np.array(st["tt"])
        v = math.hypot(1000 * pendenza(tt, np.array(st["x"])), 1000 * pendenza(tt, np.array(st["y"])))
        st["blocchi"].append([st["a"], st["a"] + PASSO, v])
        if st["t_p"] is None and v > SOGLIA:
            st["t_p"] = st["a"]
    st["tt"], st["x"], st["y"] = [], [], []


def aggiorna(st, t, c1, c2, L, A1, A2, pendenza):
    """### **Un campione** *(il tempo `t`, il centro periodico `c1`, `c2` negli indici)*: chiude i blocchi finiti, srotola, aggiunge. `pendenza` e' `carta_deriva.pendenza`
    *(passata, non importata: la stessa funzione delle tabelle)*. ### **Ritorna `True` se la corsa va fermata** *(`t >= t_p + DOPO`)*."""
    while t >= st["a"] + PASSO:
        _chiudi(st, pendenza)
        st["a"] += PASSO
    if st["c"] is not None:
        st["u"][0] += ((c1 - st["c"][0] + 0.5 * L) % L) - 0.5 * L
        st["u"][1] += ((c2 - st["c"][1] + 0.5 * L) % L) - 0.5 * L
    st["c"] = [c1, c2]
    X = st["u"][0] * A1 + st["u"][1] * A2
    st["tt"].append(t)
    st["x"].append(float(X[0]))
    st["y"].append(float(X[1]))
    return st["t_p"] is not None and t >= st["t_p"] + DOPO


def rileggi(camp, s, L, A1, A2, pendenza):
    """### **La partenza su una corsa gia' scritta** *(i campioni uniti)*: lo stato finale, e il tempo in cui la corsa si sarebbe fermata *(`None` se mai)*."""
    st = nuovo()
    ferma = None
    for c in camp:
        if aggiorna(st, c["t"] * s, c["per"]["c1"], c["per"]["c2"], L, A1, A2, pendenza) and ferma is None:
            ferma = c["t"] * s
    return st, ferma
