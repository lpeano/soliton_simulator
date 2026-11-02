# -*- coding: utf-8 -*-
r"""**LE MAPPE PER L'ANIMAZIONE** *(Luca, `2026-11-02` `15:49`; il task history `doc/TASK_HISTORY/2026-11-02_accensione_lenta.md`, sez. `12`)*: ### **il campo vero, ogni tanto,
FUORI dal repo; nel repo solo l'indice.**

### **Un'istantanea:** `rho` *(`sum_h |psi_h|^2`)* e `Lambda` *(`|phi_h|^2`)* per nodo in `float32` *(`_energia_del_legame.densita`)*, `t`, il centro periodico, `lam` *(la rampa)*.
### **Un file per pezzo:** `<radice>/<corsa>/<corsa>_<t0>.npz`, compresso, con gli indici dei nodi *(`d1 = m1 - L//2`, `d2 = m2 - L//2`)* e i vettori del toro una volta.
"""
import hashlib
import os
import shutil

import numpy as np

RADICE = r"E:\soliton_simulator\mappe"     # ### Luca 15:49: il disco esterno degli archivi
OGNI = 100                                 # ### Luca 15:49: un'istantanea ogni 100 tick (15 unita' di tempo)
VOLTE_SPAZIO = 10                          # ### Luca 15:49: lo spazio libero almeno 10 volte la stima (il disco pieno del 30 ottobre)


def stima(nodi, quante):
    """### **La stima in byte:** `rho` e `Lambda` in `float32` per istantanea, senza compressione."""
    return 2 * 4 * nodi * quante


def controlla_disco(radice, byte_stimati):
    """### **Il DEVE del disco:** `(ok, libero, nota)`. La radice deve esistere o potersi creare, essere scrivibile *(un file scritto e cancellato)*, e avere almeno
    `VOLTE_SPAZIO` volte la stima libera."""
    try:
        os.makedirs(radice, exist_ok=True)
        prova = os.path.join(radice, "_scrivibile.tmp")
        with open(prova, "wb") as fh:
            fh.write(b"ok")
        os.remove(prova)
    except OSError as e:
        return False, 0, "non scrivibile: %s" % e
    libero = shutil.disk_usage(radice).free
    ok = libero >= VOLTE_SPAZIO * byte_stimati
    return ok, libero, "libero %d byte, richiesti %d (%d x la stima)" % (libero, VOLTE_SPAZIO * byte_stimati, VOLTE_SPAZIO)


def istantanea(z, t, lam, centro):
    """### **Un'istantanea dallo stato `z`:** `{"t", "rho", "Lambda", "centro", "lam"}`; ### **lo stato non si tocca** *(si legge solo)*."""
    import _energia_del_legame as EL
    rho, la = EL.densita(z["inc"], z["st"])
    return {"t": int(t), "rho": rho.astype(np.float32), "Lambda": la.astype(np.float32), "centro": np.asarray(centro, dtype=float), "lam": float(lam)}


def scrivi(percorso, ii, m1, m2, L):
    """### **Le istantanee `ii` in un `.npz` compresso** *(scritto in un temporaneo, poi rinominato)*: `(dimensione, sha1)`."""
    from solitone import toro as TO
    A1, A2 = TO.vettori()
    os.makedirs(os.path.dirname(percorso), exist_ok=True)
    tmp = percorso + ".tmp.npz"
    np.savez_compressed(tmp, t=np.array([i["t"] for i in ii], dtype=np.int64), rho=np.stack([i["rho"] for i in ii]), Lambda=np.stack([i["Lambda"] for i in ii]),
                        centro=np.stack([i["centro"] for i in ii]), lam=np.array([i["lam"] for i in ii]),
                        d1=(np.asarray(m1) - L // 2).astype(np.int16), d2=(np.asarray(m2) - L // 2).astype(np.int16), A1=A1, A2=A2, L=np.int64(L))
    os.replace(tmp, percorso)
    return os.path.getsize(percorso), sha1(percorso)


def sha1(percorso):
    h = hashlib.sha1()
    with open(percorso, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def leggi(percorso):
    with np.load(percorso) as d:
        return {k: d[k] for k in d.files}


def riga_indice(percorso, s):
    """### **La riga dell'indice:** il percorso, la dimensione, lo `sha1`, l'intervallo di tempo *(`t` per `s`)*, quante istantanee."""
    d = leggi(percorso)
    return "%s  %d byte  sha1 %s  tempo %.2f .. %.2f  %d istantanee" % (percorso, os.path.getsize(percorso), sha1(percorso), d["t"][0] * s, d["t"][-1] * s, len(d["t"]))
