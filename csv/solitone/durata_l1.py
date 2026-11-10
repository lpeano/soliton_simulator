# -*- coding: utf-8 -*-
r"""**L1, LA FORMA DEL DECADIMENTO DEL CUORE** *(Luca `2026-11-09` `12:08`; il task history `doc/TASK_HISTORY/2026-11-09_legge_della_durata.md`, sez. `2` (L1) e `4`)*. [[PIANO-2D-3D]]

    python csv/solitone/durata_l1.py > doc/referti_l2/durata_l1.txt

**Il cuore vero** *(sez. `4.1`)*: `M_cuore = f_liscia x bordo.M`, dai campioni dei jsonl di `TB3` e `TBS` *(`corsa_accensione.serie`)*. **Le medie su finestre di `P = 311` unita' da `t 1000`;**
**tre fit** *(esponenziale, potenza, lineare)*; **`N_eff` dalla `tau_int` di Sokal dei residui** *(`stazionarieta.tau_int`)*, **il piu' piccolo dei tre; `AIC = N_eff ln(RSS/N) + 2k`.**
**L1-P** *(una sintetica esponenziale: vince l'esponenziale)*, **L1-F** *(DEVE FALLIRE: una sintetica lineare, «vince l'esponenziale»)*, **L1-S** *(la sensibilita', stampata)*. **Le letture `f1`-`f4`.**
"""
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))
import solitone  # noqa: E402,F401  (i percorsi)

NOMI = ("TB3", "TBS")          # ### sez. 2, L1
P = 311.0                      # ### sez. 2, L1: P di TB3, la stessa per TBS (dichiarata)
T_DA = 1000.0                  # ### sez. 2, L1: dopo la rampa
VINCE, PREFERITO = 10.0, 2.0   # ### sez. 2, L1: Burnham e Anderson
FRAZ_TAU_P = 1.0 / 3.0         # ### sez. 4.2: L1-P con tau = un terzo della finestra osservata
OK = [0, 0]
FALLITE = []


def esito(che, passa, nota="", deve=True):
    OK[1] += 1
    buono = passa if deve else not passa
    OK[0] += 1 if buono else 0
    if not buono:
        FALLITE.append(che)
    print("  %s: %-104s %s   %s" % ("DEVE PASSARE" if deve else "DEVE FALLIRE", che[:104], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return buono


def medie(t, x):
    """### Le medie su finestre consecutive di `P` da `T_DA`, solo finestre INTERE."""
    tm, xm = [], []
    a = T_DA
    while a + P <= t[-1]:
        m = (t >= a) & (t < a + P)
        tm.append(float(t[m].mean()))
        xm.append(float(x[m].mean()))
        a += P
    return np.array(tm), np.array(xm)


def esp(t, M0, tau):
    return M0 * np.exp(-t / tau)


def pot(t, M0, t0, a):
    return M0 * (1.0 + t / t0) ** (-a)


def fit(t, x):
    """### I tre fit: `{nome: (parametri, residui, k)}`. Gli iniziali dal lineare *(nessun numero scelto: la pendenza e l'intercetta dei dati)*."""
    from scipy.optimize import curve_fit
    A = np.vstack([np.ones_like(t), t]).T
    c, *_ = np.linalg.lstsq(A, x, rcond=None)
    out = {"lineare": ((float(c[0]), float(-c[1])), x - A @ c, 2)}
    tau0 = float(c[0] / max(-c[1], 1e-300))
    pe, _ = curve_fit(esp, t, x, p0=(c[0], tau0), maxfev=20000)
    out["esponenziale"] = (tuple(float(v) for v in pe), x - esp(t, *pe), 2)
    try:
        pp, _ = curve_fit(pot, t, x, p0=(c[0], tau0, 1.0), maxfev=20000)
        out["potenza"] = (tuple(float(v) for v in pp), x - pot(t, *pp), 3)
    except RuntimeError as ex:      # ### un fit che non converge e' un DATO da stampare, non da nascondere
        out["potenza"] = (None, None, 3, str(ex)[:80])
    return out


def giudizio(t, x, stampa=True, nome=""):
    from solitone import stazionarieta as ST
    F = fit(t, x)
    N = len(t)
    taus = {k: ST.tau_int(v[1])[0] for k, v in F.items() if v[1] is not None}
    tau = max(taus.values())
    n_eff = N / (2.0 * tau)
    aic = {k: n_eff * math.log(float(np.sum(v[1] ** 2)) / N) + 2 * v[2] for k, v in F.items() if v[1] is not None}
    ordine = sorted(aic, key=aic.get)
    margine = aic[ordine[1]] - aic[ordine[0]]
    if margine >= VINCE:
        verd = "vince %s" % ordine[0]
    elif margine >= PREFERITO:
        verd = "%s preferito, non deciso" % ordine[0]
    else:
        verd = "nessuno vince"
    if stampa:
        print("  %-6s N %d medie; tau_int dei residui %s; N_eff %.1f (il piu' piccolo)" % (nome, N, ", ".join("%s %.2f" % kv for kv in sorted(taus.items())), n_eff))
        for k in ("esponenziale", "potenza", "lineare"):
            v = F[k]
            if v[1] is None:
                print("    %-13s il fit NON converge: %s" % (k, v[3]))
                continue
            print("    %-13s parametri %s; rms dei residui %.4e; AIC %+.3f" % (k, ", ".join("%.6g" % p for p in v[0]), float(np.sqrt(np.mean(v[1] ** 2))), aic[k]))
        print("    l'ordine %s; il margine %.3f: %s" % (" < ".join(ordine), margine, verd))
    return {"F": F, "aic": aic, "ordine": ordine, "margine": margine, "verdetto": verd, "n_eff": n_eff}


def main():
    import _presidio
    from solitone import corsa_accensione as CA
    from solitone import stazionarieta as ST  # noqa: F401
    for m in ("__init__", "corsa_accensione", "stazionarieta"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(__file__)
    import _vuoto_vivo_B as V
    s = V.CORSE[CA.NOME][2]
    print("=" * 130)
    print("L1, LA FORMA DEL DECADIMENTO DEL CUORE (M_cuore = f_liscia x bordo.M): %s; le finestre P %g da t %g; AIC = N_eff ln(RSS/N) + 2k; vince sopra %g, preferito sopra %g" % (NOMI, P, T_DA, VINCE, PREFERITO))
    print("=" * 130)
    ris = {}
    for nome in NOMI:
        _rr, camp = CA.serie(nome)[:2]
        _tt, primo = np.unique([c["t"] for c in camp], return_index=True)   # ### i pezzi consecutivi hanno il campione del confine due volte: uno solo
        camp = [camp[i] for i in primo]
        t = np.array([c["t"] for c in camp], dtype=float) * s
        Mc = np.array([c["f_liscia"] * c["bordo"]["M"] for c in camp], dtype=float)
        tm, xm = medie(t, Mc)
        print("### %s: %d campioni, t da %.1f a %.1f; M_cuore a t 0 %.6e, all'ultimo %.6e; %d finestre" % (nome, len(t), t[0], t[-1], Mc[0], Mc[-1], len(tm)))
        g = giudizio(tm, xm, True, nome)
        Fe, Fl = g["F"]["esponenziale"], g["F"]["lineare"]
        sens = float(np.max(np.abs(esp(tm, *Fe[0]) - (Fl[0][0] - Fl[0][1] * tm)))) / float(np.std(Fe[1]))
        print("    L1-S la sensibilita': max |fit esponenziale - fit lineare| / dev. dei residui = %.4f (%s)" % (sens, "sotto 1: la finestra NON PUO' distinguere le forme" if sens < 1.0 else "sopra 1"))
        ris[nome] = (tm, xm, g, sens)
    print("-" * 130)
    tm, xm, g, _s = ris["TBS"]
    Fe = g["F"]["esponenziale"]
    tau_p = FRAZ_TAU_P * (tm[-1] - tm[0])
    rumore = Fe[1]
    sint_e = xm[0] * np.exp(-(tm - tm[0]) / tau_p) + rumore
    ge = giudizio(tm, sint_e, False)
    esito("L1-P una sintetica ESPONENZIALE (tau %.1f = 1/3 della finestra, i residui di TBS come rumore): vince l'esponenziale" % tau_p, ge["verdetto"] == "vince esponenziale",
          "%s (il margine %.2f)" % (ge["verdetto"], ge["margine"]))
    pend0 = xm[0] / tau_p
    sint_l = xm[0] - pend0 * (tm - tm[0]) + rumore
    gl = giudizio(tm, sint_l, False)
    esito("L1-F una sintetica LINEARE (la stessa pendenza iniziale, gli stessi residui): vince l'esponenziale", gl["verdetto"] == "vince esponenziale",
          "%s (il margine %.2f)" % (gl["verdetto"], gl["margine"]), deve=False)
    print("-" * 130)
    lett = {"vince esponenziale": "f1", "vince potenza": "f2", "vince lineare": "f3"}
    for nome in NOMI:
        tm, xm, g, sens = ris[nome]
        print("  LA LETTURA, %s: (%s) %s; il margine %.3f%s" % (nome, lett.get(g["verdetto"], "f4"), g["verdetto"], g["margine"], "; ### L1-S %.3f: la finestra non puo' distinguere" % sens if sens < 1.0 else ""))
    print("  la stessa forma in TB3 e TBS: %s" % ("si'" if ris["TB3"][2]["verdetto"] == ris["TBS"][2]["verdetto"] else "no"))
    print("=" * 130)
    print("ESITO: %d/%d controlli come devono; fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main())
