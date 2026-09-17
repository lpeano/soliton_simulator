# -*- coding: utf-8 -*-
"""RIMISURA DI `Z9` sul blob attuale, e di `R6` (i lettori della cache).

`Z9` fu misurata sul blob `69ee5403` (commit `cdc0e41`):
    passo   1 : ramp mediano 0.0002
    passo  60 : ramp mediano 0.0106
    passo 120 : ramp mediano 0.0217
    eta ~0.009/passo  ->  ramp = 1 a ~5526 passi
Da allora: (2)(3)(5), il TEMPO 2, la correzione dello sfasamento `eta`. E `eta += dt_n` con
`dt_n = DT*r` e `r` che dipende da `psi`: il TEMPO 2 ha cambiato `psi`, quindi puo' aver cambiato
la VELOCITA' con cui `eta` cresce. La direzione NON si assume.

⚠ DUE SCENE, ed e' il punto metodologico:
  (A) la scena ORIGINALE (3 masse da 120, raggio 2.0, step+mitosi) -> CONFRONTABILE coi numeri
      di `cdc0e41`, perche' e' lo STESSO metodo;
  (B) la scena del BATCH (semina(80) + 6 riscaldamento + 3 masse in cerchio) -> il numero VALIDO
      oggi, perche' e' il sistema che gira davvero.
Riporto ENTRAMBE: un confronto fra due numeri presi in modo diverso non e' un confronto.
ASCII PURO.
"""
import importlib.util
import os
import sys

import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
SIM = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "soliton_simulator.py")

spec = importlib.util.spec_from_file_location("sim_z9", SIM)
M = importlib.util.module_from_spec(spec)
sys.modules["sim_z9"] = M
sys.argv = ["soliton_simulator.py"]
spec.loader.exec_module(M)
for _f in ("CS_DINAMICO", "CAMPO_SPINORIALE", "SPINORE_VIVO", "CHI_CORE",
           "FORK_SU2", "FORK_SU2_MEM", "SPINORE_CORRETTO"):
    setattr(M, _f, True)
TA = M.TAU_A

# ------------------------------------------------------------------ R6: i lettori della cache
pesi_reg = []
orig_pesi = M.Rete._pesi
orig_cs = M.Rete._cs_nodo
stato = {"scritta": False, "passo": 0}


def spia_pesi(self):
    fr = sys._getframe(1)
    csp = getattr(self, "_cs_nodo_prev", None)
    pesi_reg.append((stato["passo"], fr.f_code.co_name, stato["scritta"],
                     (csp is not None and len(csp) >= self.n)))
    return orig_pesi(self)


def spia_cs(self, I, w):
    out = orig_cs(self, I, w)
    stato["scritta"] = True
    return out


orig_step = M.Rete.step


def spia_step(self):
    stato["scritta"] = False
    return orig_step(self)


M.Rete._pesi = spia_pesi
M.Rete._cs_nodo = spia_cs
M.Rete.step = spia_step


def misura(scena, passi):
    """Restituisce la traiettoria di ramp/eta. `scena` costruisce e restituisce la rete."""
    r = scena()
    traj = []
    for k in range(1, passi + 1):
        stato["passo"] = k
        if SCENA_BATCH[0]:
            M.scuoti_vuoto(r); r.step(); r.mitosi(); r.rilassa_disegno(); r.memoria_hebbiana_moto()
        else:
            r.step(); r.mitosi()
        n = r.n
        eta = np.asarray(r.eta, float)[:n]
        ramp = np.minimum(1.0, eta / TA)
        traj.append((k, n, float(np.median(eta)), float(np.median(ramp)),
                     float(np.percentile(ramp, 5)), float(np.percentile(ramp, 95)),
                     float(np.mean(ramp == 0.0))))
    return traj


SCENA_BATCH = [False]


def scena_originale():
    r = M.Rete(seed=5)
    for c in [(-4., 0, 0), (4., 0, 0), (0., 4., 0)]:
        r.nuova_massa(120, raggio=2.0, centro=c, fase=0.0)
    return r


def scena_batch():
    r = M.Rete(5)
    r.semina(80)
    for _ in range(6):
        M.scuoti_vuoto(r); r.step(); r.mitosi(); r.rilassa_disegno(); r.memoria_hebbiana_moto()
    Nc = M.N_CRITICO() if callable(getattr(M, "N_CRITICO", None)) else 200
    for k in range(3):
        ang = 2 * np.pi * k / 3
        r.nuova_massa(int(Nc * 0.6), raggio=M._size_video(k, 0.8),
                      centro=(8.0 * np.cos(ang), 8.0 * np.sin(ang), 0.0), fase=0.0)
    r.aggiorna_pesi_concorrenza()
    return r


print("=" * 118)
print("RIMISURA DI Z9 -- blob %s" % os.path.basename(SIM))
print("=" * 118)

for eti, scena, batch in (("(A) SCENA ORIGINALE (confrontabile con cdc0e41)", scena_originale, False),
                          ("(B) SCENA DEL BATCH (il sistema che gira davvero)", scena_batch, True)):
    SCENA_BATCH[0] = batch
    pesi_reg.clear()
    traj = misura(scena, 120)
    print("\n--- %s ---" % eti)
    print("  %-7s %-7s %-12s %-14s %-12s %-12s %-12s" %
          ("passo", "n", "eta med", "RAMP med", "ramp p05", "ramp p95", "ramp=0 %"))
    for k, n, em, rm, p05, p95, z in traj:
        if k in (1, 20, 60, 120):
            print("  %-7d %-7d %-12.5g %-14.5g %-12.5g %-12.5g %-12.2f" %
                  (k, n, em, rm, p05, p95, 100.0 * z))
    e1, e120 = traj[0][2], traj[-1][2]
    cres = (e120 - e1) / (120 - 1)
    rm120 = traj[-1][3]
    passi_a_1 = (TA / cres) if cres > 0 else float("inf")
    print("  crescita di eta per passo : %.6g      (riferimento cdc0e41: ~0.009)" % cres)
    print("  passo estrapolato per ramp = 1 : %.0f   (riferimento cdc0e41: ~5526)" % passi_a_1)
    if batch:
        print("\n  R6 -- `_pesi()` per passo, e da che parte della scrittura della cache:")
        per_passo = {}
        for p, chi, dopo, ok in pesi_reg:
            per_passo.setdefault(p, []).append((chi, dopo, ok))
        campione = [p for p in sorted(per_passo) if p > 3][:5]
        for p in campione:
            v = per_passo[p]
            pre = sum(1 for _, d, _ in v if not d)
            post = sum(1 for _, d, _ in v if d)
            print("     passo %-4d totale %-4d   PRIMA %-4d   DOPO %-4d" % (p, len(v), pre, post))
        tot = [v for p, v in per_passo.items() if p > 3]
        npp = np.median([len(v) for v in tot]) if tot else 0
        pre_t = sum(sum(1 for _, d, _ in v if not d) for v in tot)
        post_t = sum(sum(1 for _, d, _ in v if d) for v in tot)
        print("     MEDIANA per passo: %.1f    (riferimento 8bfcf46: 16, con 9 PRIMA e 7 DOPO)"
              % npp)
        print("     totale PRIMA %d, totale DOPO %d" % (pre_t, post_t))
        chiam = {}
        for p, chi, d, ok in pesi_reg:
            if p > 3:
                chiam[chi] = chiam.get(chi, 0) + 1
        print("     per CHIAMANTE: %s" % ", ".join("%s=%d" % kv for kv in sorted(chiam.items(), key=lambda x: -x[1])))
        ko = sum(1 for p, _, _, ok in pesi_reg if p > 3 and not ok)
        tt = sum(1 for p, _, _, _ in pesi_reg if p > 3)
        print("     `_pesi()` come lettore di _cs_nodo_prev: fallback %d su %d (%.4f %%)"
              % (ko, tt, 100.0 * ko / max(tt, 1)))

print("\n" + "=" * 118)
print("""COME SI LEGGE
 (A) e' l'UNICO confronto lecito coi numeri di cdc0e41: stessa scena, stesso metodo.
 (B) e' il numero che vale per il sistema reale, ed e' quello da usare d'ora in poi.
 R6 si legge da (B): se `_pesi()` gira tutta da un lato della scrittura della cache, l'ostacolo
 e' caduto; se gira ancora a cavallo, regge.""")
