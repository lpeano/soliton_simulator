"""[dev-spinoriale] TEST-GRATIS S3b (MOD 5.3 relazionale) — nessuna modifica al codice.

DOMANDA: l'orologio de Broglie del PRIMARIO _psi_spinor (avanzamento della fase di
doppia-copertura alpha_k = arg<canon(nb_k)|_psi_spinor_k> sull'otto) riproduce la
DILATAZIONE torsionale che il codice usa gia' (tau_nodo = 1 + media_archi|tw|/PHI_CRIT)?

Se |Delta-alpha|/DT correla forte con tau_nodo (e rapporto ~ costante) -> S3b PASSA:
il de Broglie E' la dilatazione, implemento come sorgente unica. Se scorrelati -> S3b FALLISCE:
il de Broglie NON e' la dilatazione giusta -> rivedere (dilatazione da TW_SPINORE esplicito).

Config Fase 5, DETERMINISTICO (SCUOTIMENTO=False). Causale: alpha da stati committati a
step consecutivi (t-1 vs t-2). Pairing sui primi min(n) nodi; per-step corr riportate
(l'index-shift da mitosi/morte contamina poco su finestra corta -> si vede se il segnale c'e').
"""
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import numpy as np
import soliton_simulator as sm

sm.CAMPO_SPINORIALE = True
sm.SPINORE_VIVO = True
sm.SPINORE_CORRETTO = True
sm.CHI_CORE = True
sm.SCUOTIMENTO = False   # deterministico

PHI = sm.PHI_CRIT
DT = sm.DT


def alpha_nodi(net):
    """fase di doppia-copertura per-nodo alpha_k = arg<canon(nb_k)|_psi_spinor_k>."""
    n = net.n
    ps = getattr(net, "_psi_spinor", None)
    if ps is None or len(ps) < n:
        return None
    canon = net._bloch_a_spinore(net._nb[:n])
    ov = np.sum(np.conj(canon) * ps[:n], axis=1)
    return np.angle(ov)   # [-pi, pi]


def tau_nodo_torsione(net):
    """dilatazione canonica del codice: 1 + media_archi_incidenti(|tw|)/PHI_CRIT."""
    n = net.n
    aw = np.abs(net.tw)
    acc = np.zeros(n)
    i, j = net.i, net.j
    mi = i < n; mj = j < n
    np.add.at(acc, i[mi], aw[mi])
    np.add.at(acc, j[mj], aw[mj])
    deg = getattr(net, "_deg", None)
    if deg is None or len(deg) < n:
        deg = np.bincount(i[mi], minlength=n)[:n] + np.bincount(j[mj], minlength=n)[:n]
    else:
        deg = np.asarray(deg)[:n]
    return 1.0 + acc / np.maximum(deg, 1) / PHI


def wrap(x):
    return (x + np.pi) % (2 * np.pi) - np.pi


net = sm.Rete(seed=1)
net.semina(120)
for _ in range(60):   # formazione
    net.step()

prev_alpha = alpha_nodi(net)
prev_n = net.n

print("step   n    corr(|da|/DT, tau_nodo)   corr(|da|/DT, mean|tw|)   slope   freq_med   tau_med")
corrs_tau = []
corrs_tw = []
slopes = []
for s in range(12):
    net.step()
    a = alpha_nodi(net)
    n = net.n
    m = min(len(prev_alpha), len(a), prev_n, n)
    da = wrap(a[:m] - prev_alpha[:m])
    freq = np.abs(da) / DT                       # frequenza de Broglie grezza (magnitudine)
    tau = tau_nodo_torsione(net)[:m]             # dilatazione torsionale
    twmean = (tau - 1.0) * PHI                   # media|tw| per-nodo (parte variabile)
    ok = np.isfinite(freq) & np.isfinite(tau)
    fx, tx, wx = freq[ok], tau[ok], twmean[ok]
    if len(fx) > 10 and np.std(fx) > 0 and np.std(tx) > 0:
        c_tau = np.corrcoef(fx, tx)[0, 1]
        c_tw = np.corrcoef(fx, wx)[0, 1] if np.std(wx) > 0 else float('nan')
        slope = np.polyfit(tx, fx, 1)[0]
        corrs_tau.append(c_tau); corrs_tw.append(c_tw); slopes.append(slope)
        print(f"{s:4d} {n:5d}   {c_tau:+.4f}                  {c_tw:+.4f}                {slope:+.4f}   {np.median(fx):.4f}   {np.median(tx):.4f}")
    prev_alpha = a; prev_n = n

print("\n=== SINTESI S3b ===")
if corrs_tau:
    print(f"  corr(|da|/DT, tau_nodo)  media={np.mean(corrs_tau):+.4f}  (min={np.min(corrs_tau):+.4f} max={np.max(corrs_tau):+.4f})")
    print(f"  corr(|da|/DT, mean|tw|)  media={np.nanmean(corrs_tw):+.4f}")
    print(f"  slope medio              {np.mean(slopes):+.4f}")
    esito = np.mean(corrs_tau)
    print(f"  ESITO: {'S3b PLAUSIBILE (corr forte >0.5)' if esito > 0.5 else ('S3b DUBBIO (0.2-0.5)' if esito > 0.2 else 'S3b FALLISCE (corr ~0, de Broglie != dilatazione torsionale)')}")
else:
    print("  nessuna misura valida")
