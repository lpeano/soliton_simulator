# -*- coding: utf-8 -*-
"""SONDA: i nodi con `rho_sorgente <= 0` c'erano gia' PRIMA del TEMPO 2?

Il blob vecchio (9dfd91c4) NON ha i contatori cablati: sarebbe impossibile leggerli da li'.
Quindi la misura e' fatta **DALL'ESTERNO**, con lo STESSO osservatore applicato a entrambi i blob --
il che e' anche metodologicamente migliore: la misura e' identica **per costruzione**, non perche'
due strumentazioni si somigliano.

Uso:  python _sonda_rho_zero.py <percorso_del_simulatore> <etichetta>
Scrive un JSON accanto, che il confronto legge.
ASCII PURO.
"""
import importlib.util
import json
import os
import sys

import numpy as np

SIM = sys.argv[1]
ETI = sys.argv[2]
OUT = sys.argv[3]

spec = importlib.util.spec_from_file_location("sim_" + ETI, SIM)
M = importlib.util.module_from_spec(spec)
sys.modules["sim_" + ETI] = M
sys.argv = ["soliton_simulator.py"]
spec.loader.exec_module(M)

for _f in ("CS_DINAMICO", "CAMPO_SPINORIALE", "SPINORE_VIVO", "CHI_CORE",
           "FORK_SU2", "FORK_SU2_MEM", "SPINORE_CORRETTO"):
    setattr(M, _f, True)

reg = []
orig = M.Rete._passo_spinoriale
stato = {"inv": 0, "passo": 0}


def spia(self, i, j, w, dt_n, *a, **k):
    stato["inv"] += 1
    n = self.n
    rs = np.asarray(self._rho_sorgente(), float)[:n]
    ko = ~(np.isfinite(rs) & (rs > 0))
    rec = {"inv": stato["inv"], "passo": stato["passo"], "n": int(n),
           "ko": int(ko.sum()),
           "zero_esatto": int(np.sum(rs == 0.0)),
           "sotto_1e300": int(np.sum((rs > 0) & (rs < 1e-300))),
           "non_finiti": int(np.sum(~np.isfinite(rs)))}
    if ko.any():
        grado = (np.bincount(self.i, minlength=n)[:n] +
                 np.bincount(self.j, minlength=n)[:n]) if len(self.i) else np.zeros(n)
        eta = np.asarray(getattr(self, "eta", np.zeros(n)), float)[:n]
        TA = getattr(M, "TAU_A", 50.0)
        ramp = np.minimum(1.0, eta / TA)
        # ramp mediano dei VICINI dei nodi senza campo
        vic = []
        if len(self.i):
            for lato_a, lato_b in ((self.i, self.j), (self.j, self.i)):
                m = ko[lato_a]
                if m.any():
                    vic.append(ramp[lato_b[m]])
        vic = np.concatenate(vic) if vic else np.array([np.nan])
        rec.update({
            "grado_ko_med": float(np.median(grado[ko])) if ko.any() else -1.0,
            "grado_ok_med": float(np.median(grado[~ko])) if (~ko).any() else -1.0,
            "eta_ko_med": float(np.median(eta[ko])) if ko.any() else -1.0,
            "eta_ok_med": float(np.median(eta[~ko])) if (~ko).any() else -1.0,
            "ramp_vicini_ko_med": float(np.nanmedian(vic)),
            "ramp_med_tutti": float(np.median(ramp)),
        })
    reg.append(rec)
    return orig(self, i, j, w, dt_n, *a, **k)


M.Rete._passo_spinoriale = spia

# LA SCENA E' QUELLA DEL BATCH, riprodotta dal sorgente (~:5993-6014) e NON inventata:
# semina(80) + SEI passi di riscaldamento + N masse in cerchio di raggio `sep`.
# La prima versione di questa sonda usava una scena mia (3 nuova_massa, raggio 2.0) e dava
# 60 invocazioni contro le 66 del batch: la differenza ERANO i sei passi di riscaldamento.
# Una sonda che non riproduce la scena misura un altro sistema.
SEP = 8.0
NMASSE = 3
r = M.Rete(5)
r.semina(80)
for _ in range(6):
    M.scuoti_vuoto(r); r.step(); r.mitosi(); r.rilassa_disegno(); r.memoria_hebbiana_moto()
Nc = M.N_CRITICO() if callable(getattr(M, "N_CRITICO", None)) else 200
for k in range(NMASSE):
    ang = 2 * np.pi * k / NMASSE
    cx, cy = SEP * np.cos(ang), SEP * np.sin(ang)
    r.nuova_massa(int(Nc * 0.6), raggio=M._size_video(k, 0.8), centro=(cx, cy, 0.0), fase=0.0)
r.aggiorna_pesi_concorrenza()
for kk in range(60):
    stato["passo"] = kk
    M.scuoti_vuoto(r); r.step(); r.mitosi(); r.rilassa_disegno(); r.memoria_hebbiana_moto()

json.dump({"etichetta": ETI, "sim": SIM, "reg": reg}, open(OUT, "w"))
con = [x for x in reg if x["ko"] > 0]
print("[%s] invocazioni %d | con nodi rho<=0: %d | ultima: %s | ko totali: %d"
      % (ETI, len(reg), len(con), (con[-1]["inv"] if con else "-"),
         sum(x["ko"] for x in reg)))
