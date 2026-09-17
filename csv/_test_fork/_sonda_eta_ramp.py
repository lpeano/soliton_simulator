# -*- coding: utf-8 -*-
"""SONDA: `ramp` di un figlio appena nato, PRIMA e DOPO `eta += dt_n`.

L'IPOTESI (mandato par.1):
    :3018   w = self._pesi(); self.eta += dt_n
            ^^^^^^^^^^^^^^^   ^^^^^^^^^^^^^^^
            usa eta VECCHIA   POI la incrementa
  un figlio nato nella mitosi precedente ha eta = 0  ->  ramp = 0 ESATTO  ->  tutti i suoi archi
  hanno peso zero  ->  psi = 0  ->  rho_sorgente = 0.
  PRIMA del TEMPO 2 `calcola_psi()` RICALCOLAVA `_pesi()` piu' tardi, DOPO l'incremento: ramp
  minuscolo ma NON zero.

Misura ① (il test diretto) e ③ (il conto dei pesi). La ② e' risolta dalla LETTURA del codice.
Osserva e delega: nessuna logica toccata.
ASCII PURO.
"""
import sys as _sys_enc  # PRESIDIO ENCODING (CLAUDE.md): lo stdout di Windows e' cp1252 e
# uccide qualunque print con un carattere non-ASCII. E' successo SETTE volte, l'ultima allo
# script che stava CONTANDO le occorrenze. Il `# -*- coding: utf-8 -*-` NON basta: riguarda il
# SORGENTE, non lo STDOUT. Questa riga lo risolve alla radice.
try:
    _sys_enc.stdout.reconfigure(encoding="utf-8")
    _sys_enc.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass
import importlib.util
import os
import sys

import numpy as np

SIM = sys.argv[1] if len(sys.argv) > 1 else "soliton_simulator.py"
spec = importlib.util.spec_from_file_location("sim_eta", SIM)
M = importlib.util.module_from_spec(spec)
sys.modules["sim_eta"] = M
sys.argv = ["soliton_simulator.py"]
spec.loader.exec_module(M)
for _f in ("CS_DINAMICO", "CAMPO_SPINORIALE", "SPINORE_VIVO", "CHI_CORE",
           "FORK_SU2", "FORK_SU2_MEM", "SPINORE_CORRETTO"):
    setattr(M, _f, True)

DT = M.DT
TA = M.TAU_A
reg = []
orig_pesi = M.Rete._pesi
stato = {"in_step": False}


def spia_pesi(self):
    """Chiamata da step:3018 PRIMA dell'incremento di eta: e' li' che si misura."""
    fr = sys._getframe(1)
    w = orig_pesi(self)
    if fr.f_code.co_name == "step" and stato["in_step"]:
        n = self.n
        eta = np.asarray(self.eta, float)[:n]
        grado = (np.bincount(self.i, minlength=n)[:n] +
                 np.bincount(self.j, minlength=n)[:n]) if len(self.i) else np.zeros(n)
        neo = (grado == 2) & (eta <= 0.0)          # figli della mitosi, eta ancora a zero
        if neo.any():
            ramp_pre = np.minimum(1.0, eta / TA)
            # dt_n per nodo: se l'orologio e' locale e' DT*r, altrimenti DT. Uso il caso peggiore
            # (DT nudo) come limite inferiore dell'incremento: se anche cosi' ramp_post non e' zero,
            # a maggior ragione non lo e' col ritmo.
            eta_post = eta + DT
            ramp_post = np.minimum(1.0, eta_post / TA)
            idx = np.where(neo)[0]
            # i pesi degli archi di questi nodi
            m_arc = np.isin(self.i, idx) | np.isin(self.j, idx)
            wz = w[m_arc] if m_arc.any() else np.array([])
            reg.append(dict(
                n=int(n), neo=int(neo.sum()),
                eta_pre=float(np.max(eta[neo])),
                ramp_pre_max=float(np.max(ramp_pre[neo])),
                ramp_pre_zero=int(np.sum(ramp_pre[neo] == 0.0)),
                ramp_post_min=float(np.min(ramp_post[neo])),
                ramp_post_zero=int(np.sum(ramp_post[neo] == 0.0)),
                archi_neo=int(m_arc.sum()),
                archi_peso_zero=int(np.sum(wz == 0.0)) if wz.size else 0,
                peso_max=float(np.max(wz)) if wz.size else -1.0,
            ))
    return w


orig_step = M.Rete.step


def spia_step(self):
    stato["in_step"] = True
    try:
        return orig_step(self)
    finally:
        stato["in_step"] = False


M.Rete._pesi = spia_pesi
M.Rete.step = spia_step

# scena del batch, riprodotta dal sorgente
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
for kk in range(40):
    M.scuoti_vuoto(r); r.step(); r.mitosi(); r.rilassa_disegno(); r.memoria_hebbiana_moto()

print("=" * 112)
print("SONDA `eta` / `ramp` -- il figlio appena nato pesa zero PRIMA dell'incremento?")
print("  simulatore: %s   TAU_A = %s   DT = %s" % (os.path.basename(SIM), TA, DT))
print("=" * 112)
if not reg:
    print("  NESSUN passo con figli a eta = 0 osservato: l'ipotesi NON e' testabile su questa scena.")
    sys.exit(0)

print("\n--- (1) IL TEST DIRETTO: ramp PRIMA e DOPO l'incremento di eta ---")
print("  %-7s %-7s %-12s %-14s %-14s %-14s" %
      ("passo", "neo", "eta PRIMA", "ramp PRIMA", "ramp DOPO", "ramp DOPO=0?"))
for k, x in enumerate(reg[:10]):
    print("  %-7d %-7d %-12.6g %-14.6g %-14.6g %-14s" %
          (k, x["neo"], x["eta_pre"], x["ramp_pre_max"], x["ramp_post_min"],
           "%d/%d" % (x["ramp_post_zero"], x["neo"])))
tot_neo = sum(x["neo"] for x in reg)
pre_zero = sum(x["ramp_pre_zero"] for x in reg)
post_zero = sum(x["ramp_post_zero"] for x in reg)
print("\n  su %d nodi-passo appena nati osservati:" % tot_neo)
print("    ramp PRIMA dell'incremento ESATTAMENTE 0 : %d  (%.2f %%)" % (pre_zero, 100.0 * pre_zero / max(tot_neo, 1)))
print("    ramp DOPO  l'incremento   ESATTAMENTE 0 : %d  (%.2f %%)" % (post_zero, 100.0 * post_zero / max(tot_neo, 1)))
print("    ramp DOPO, valore minimo osservato       : %.6g" % min(x["ramp_post_min"] for x in reg))

print("\n--- (3) IL CONTO DEI PESI: gli archi del neonato hanno peso zero? ---")
ta = sum(x["archi_neo"] for x in reg)
tz = sum(x["archi_peso_zero"] for x in reg)
print("  archi incidenti ai neonati        : %d" % ta)
print("  di cui con peso ESATTAMENTE ZERO  : %d  (%.2f %%)" % (tz, 100.0 * tz / max(ta, 1)))
print("  peso massimo osservato su un arco di neonato: %.6g" % max(x["peso_max"] for x in reg))

print("\n" + "=" * 112)
if pre_zero == tot_neo and post_zero == 0 and tz == ta:
    print("IPOTESI CONFERMATA (1) e (3): ramp e' ZERO ESATTO prima dell'incremento e NON zero dopo,")
    print("e TUTTI gli archi del neonato hanno peso esattamente zero.")
elif pre_zero < tot_neo:
    print("IPOTESI CADUTA su (1): ramp NON e' zero prima dell'incremento in %d casi su %d."
          % (tot_neo - pre_zero, tot_neo))
else:
    print("ESITO MISTO: si riporta senza forzare una sintesi.")
