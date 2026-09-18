# -*- coding: utf-8 -*-
"""LA RETROAZIONE: `f` DIPENDE DA `r` DEL PASSO PRIMA?  (prerequisito di stabilita' del par.2)

Progettazione in doc/TASK_HISTORY/2026-09-18_frequenza-riferimento.md (b6308d1). **NESSUNA CURA.**

PERCHE' QUESTA MISURA ESISTE, e non era nel mandato:
  `TAU_LOC = 1.0` (:251) -> `r = r_normalized` SENZA smorzamento, e `dt_n = DT*r` (:2972).
  Oggi `x = f/median(|f|)` tiene `median(r) = 1` PER COSTRUZIONE: qualunque deriva globale di `f`
  viene divisa via, e `dt_n ~ DT`. Con un riferimento ASSOLUTO quella stabilizzazione SPARISCE.
  SE `f` DIPENDE DA `dt_n` -- cioe' da `r` del passo prima -- SI CHIUDE UN ANELLO:
      r scende -> dt_n scende -> la fase avanza meno -> f scende -> x scende -> r scende ancora
  e il punto fisso sarebbe `r = 0`: IL TEMPO SI FERMEREBBE. Se invece `f` NON dipende da `r`,
  l'anello non c'e' e il candidato e' stabile.
  *** NON E' UN'ARGOMENTAZIONE DA ACCETTARE: E' UNA PREMESSA DA MISURARE. ***

COME, e il disegno conta piu' del risultato:
  E1  PENDENZA TRASVERSALE `log f(t+1)` contro `log r(t)`, NODO PER NODO, a piu' istanti.
      pendenza ~ +1  -> `f` E' PROPORZIONALE al tic locale: L'ANELLO C'E'.
      pendenza ~  0  -> `f` non vede `r`: l'anello NON c'e'.
      Si riporta la `SE` E la dispersione FRA ISTANTI (P3/C10: la SE interna e' ~3 volte troppo
      piccola su questo sistema, e la barra buona e' quella fra ripetizioni).
  E2  IL CONTROLLO NULLO, senza cui E1 non si legge: la stessa pendenza di `log f(t+1)` contro
      `log f(t)`. Se `f` e' fortemente autocorrelato e `r` e' una funzione di `f`, una pendenza
      positiva in E1 puo' venire TUTTA da li'. Si riporta il confronto.
  E3  E la PENDENZA PARZIALE: `log f(t+1)` contro `log r(t)` A PARITA' di `log f(t)` (regressione
      a due regressori). E' la sola che separa 'f segue il tic' da 'f segue se stesso'.
ASCII PURO.
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")))
import _presidio
_presidio.avvia(__file__)

import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, ROOT)
os.chdir(ROOT)
sys.argv = ["soliton_simulator.py"]
import soliton_simulator as S

for _f in ("CAMPO_SPINORIALE", "CS_DINAMICO", "CHI_CORE", "FORK_SU2", "FORK_SU2_MEM",
           "SPINORE_CORRETTO"):
    setattr(S, _f, True)

print("=" * 118)
print("LA RETROAZIONE -- `f` dipende da `r` del passo prima?   [120 passi, seme 5]")
print("=" * 118)
print("  TAU_LOC = %.6g  (se 1.0, r = r_normalized SENZA smorzamento)   DT = %.6g" % (S.TAU_LOC, S.DT))

REG = []
_orig = S.Rete.ritmo


def spia(self):
    out = _orig(self)
    try:
        n = self.n
        _ps = getattr(self, "psi_spin", None); _psp = getattr(self, "_psi_spin_prec", None)
        if not (_ps is not None and _psp is not None and len(_ps) == n and len(_psp) == n
                and S.CAMPO_SPINORIALE):
            REG.append(None); return out
        a = np.angle(np.asarray(_ps)[:, 0]) - np.angle(np.asarray(_psp)[:, 0])
        f = np.abs(((a + 2 * np.pi) % (4 * np.pi) - 2 * np.pi) / S.DT)
        rr = np.asarray(out, float) if out is not None and np.ndim(out) else np.full(n, np.nan)
        REG.append(dict(n=n, f=f, r=rr[:n] if rr.size >= n else np.full(n, np.nan)))
    except Exception:
        REG.append(None)
    return out


S.Rete.ritmo = spia
r = S.Rete(5)
r.semina(80)
for _ in range(6):
    S.scuoti_vuoto(r); r.step(); r.mitosi(); r.rilassa_disegno(); r.memoria_hebbiana_moto()
Nc = S.N_CRITICO() if callable(getattr(S, "N_CRITICO", None)) else 200
for k in range(3):
    ang = 2 * np.pi * k / 3
    r.nuova_massa(int(Nc * 0.6), raggio=S._size_video(k, 0.8),
                  centro=(8.0 * np.cos(ang), 8.0 * np.sin(ang), 0.0), fase=0.0)
r.aggiorna_pesi_concorrenza()
for _ in range(120):
    S.scuoti_vuoto(r); r.step(); r.mitosi(); r.rilassa_disegno(); r.memoria_hebbiana_moto()
S.Rete.ritmo = _orig

B = [x for x in REG if x is not None]
print("\n  invocazioni utilizzabili: %d su %d" % (len(B), len(REG)))
rr0 = np.concatenate([x["r"] for x in B[-30:]])
rr0 = rr0[np.isfinite(rr0)]
print("  `r` COME LO RESTITUISCE IL CODICE (30 passi): min %.6g  p05 %.6g  MEDIANA %.6g  p95 %.6g  max %.6g"
      % (rr0.min(), np.percentile(rr0, 5), np.median(rr0), np.percentile(rr0, 95), rr0.max()))
print("  (e' il numero che moltiplica DT: dt_n = DT*r. La mediana deve valere 1 PER COSTRUZIONE.)")


def pend(y, x):
    """pendenza OLS e la sua SE. Nessuna soglia inventata: si riportano numero ed errore."""
    m = np.isfinite(x) & np.isfinite(y)
    if m.sum() < 30:
        return np.nan, np.nan, 0
    x = x[m]; y = y[m]
    xc = x - x.mean(); yc = y - y.mean()
    sxx = float(np.sum(xc * xc))
    if sxx <= 0:
        return np.nan, np.nan, int(m.sum())
    b = float(np.sum(xc * yc) / sxx)
    res = yc - b * xc
    se = float(np.sqrt(np.sum(res ** 2) / max(len(x) - 2, 1) / sxx))
    return b, se, int(m.sum())


def pend2(y, x1, x2):
    """pendenza PARZIALE su x1 tenendo x2 fisso (due regressori + intercetta)."""
    m = np.isfinite(y) & np.isfinite(x1) & np.isfinite(x2)
    if m.sum() < 40:
        return np.nan, 0
    X = np.column_stack([np.ones(m.sum()), x1[m], x2[m]])
    try:
        beta, *_ = np.linalg.lstsq(X, y[m], rcond=None)
    except Exception:
        return np.nan, 0
    return float(beta[1]), int(m.sum())


print("\n--- E1/E2/E3 -- `f(t+1)` contro `r(t)`, e il controllo nullo `f(t+1)` contro `f(t)` ---")
print("  %-8s %-7s | %-22s | %-22s | %-14s"
      % ("istante", "n", "E1  d log f(t+1)/d log r(t)", "E2  NULLO: vs log f(t)", "E3  PARZIALE"))
b1s, b2s, b3s = [], [], []
IDX = [k for k in range(2, len(B) - 1)]
CAMP = IDX[::max(len(IDX) // 8, 1)][:8]
for k in CAMP:
    p, c = B[k], B[k + 1]
    m = min(len(p["f"]), len(c["f"]))
    if m < 50:
        continue
    lf1 = np.log10(np.maximum(c["f"][:m], 1e-30))
    lf0 = np.log10(np.maximum(p["f"][:m], 1e-30))
    lr0 = np.log10(np.maximum(p["r"][:m], 1e-30))
    vivi = (p["f"][:m] > 0) & (c["f"][:m] > 0) & np.isfinite(lr0)
    lf1, lf0, lr0 = lf1[vivi], lf0[vivi], lr0[vivi]
    b1, se1, n1 = pend(lf1, lr0)
    b2, se2, _ = pend(lf1, lf0)
    b3, _ = pend2(lf1, lr0, lf0)
    if np.isfinite(b1):
        b1s.append(b1); b2s.append(b2); b3s.append(b3)
    print("  %-8d %-7d | %+8.4f  SE %-9.4f | %+8.4f  SE %-9.4f | %+8.4f"
          % (k, n1, b1, se1, b2, se2, b3))
if b1s:
    print("  %-8s %-7s | %+8.4f  sd %-9.4f | %+8.4f  sd %-9.4f | %+8.4f  sd %.4f"
          % ("MEDIANA", len(b1s), np.median(b1s), np.std(b1s), np.median(b2s), np.std(b2s),
             np.median(b3s), np.std(b3s)))
print("""
  COME SI LEGGE -- fissato PRIMA (task history b6308d1):
    E3 (la PARZIALE) ~ +1  -> `f` E' PROPORZIONALE al tic locale: L'ANELLO C'E', e con un
                              riferimento ASSOLUTO `r` non avrebbe piu' nulla che lo stabilizza.
    E3 ~ 0                 -> `f` non vede `r`: l'anello NON c'e', il candidato e' stabile.
  E1 DA SOLA NON DECIDE: `r` e' una funzione di `f(t)`, quindi l'autocorrelazione di `f` (E2) puo'
  produrre una pendenza positiva DA SOLA. La barra buona e' la dispersione FRA ISTANTI, non la SE
  interna (P3/C10: la SE interna e' ~3 volte troppo piccola su questo sistema).""")

print("\n" + "=" * 118)
