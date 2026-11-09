# -*- coding: utf-8 -*-
r"""**T4-B, LA DIAGNOSI DEL VERSO DELLA FASE** *(Luca `2026-11-09` `08:56`; il task history `doc/TASK_HISTORY/2026-11-07_u1_prototipo_verificato.md`, sez. `16.2`)*. [[U1-PROTOTIPO-TRIANGOLI]]

    python csv/solitone/u1_t4b_fase.py > doc/referti_l2/u1_t4b_fase.txt

**Il banco di `u1_t4b.py`** *(importato, non toccato)*, **a `e*`, i `24` `k`, tre `eps` `1e-4`, `5e-5`, `2.5e-5`.** **`p` la pendenza di `ln V` contro `ln eps`.**
**I DEVE:** `D-G` *(fotone e ottica in fase: `|p - 2| <= 0.1` dove `V` sopra `1000` volte l'arrotondamento)*; `D-G0` *(la gauge in fase: `|p| <= 0.01`)*;
`D-P` *(il controllo positivo: (->) e (<- ampiezza) del fotone, `|p| <= 0.01`)*; `D-F` *(DEVE FALLIRE: `D-G` applicato alla gauge in fase)*. **E T4B-L stampato per verso, per banda, per `k`.**
"""
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))
import solitone  # noqa: E402,F401  (i percorsi)

EPS3 = (1e-4, 5e-5, 2.5e-5)    # ### sez. 16.2
TOLL_G = 0.1                   # ### sez. 16.2: D-G
TOLL_0 = 0.01                  # ### sez. 16.2: D-G0, D-P
FATT_PAV = 1000.0              # ### sez. 16.2
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


def indici(m, n, i):
    return (i // 3) * m + 3 * np.arange(n) + (i % 3)


def indietro(T4B, U1, B, bl, t1, t2, dpsi, ep):
    """### Le righe di `u1_t4b.main`, verso (<-): la parte di fotone, ottica e gauge della differenza dei campi, `/ (2 eps)`, con `|dpsi| = 1`."""
    c = B.c
    n, m, L = c.n, c.m, T4B.L
    _, ap, eP = B.tick(dpsi=ep * dpsi)
    _, am, eM = B.tick(dpsi=-ep * dpsi)
    dX = np.concatenate([ap - am, eP - eM]) / (2 * ep)
    kk = [(t1, t2)]
    if not (abs(math.remainder(2 * t1, 2 * math.pi)) < 1e-12 and abs(math.remainder(2 * t2, 2 * math.pi)) < 1e-12):
        kk.append((-t1, -t2))
    parte = {"fotone": 0.0, "ottica": 0.0, "gauge": 0.0}
    for (s1, s2) in kk:
        bks = T4B.bande_k(U1, bl, s1, s2)[0]
        ph = np.exp(-1j * (s1 * B.m1 + s2 * B.m2))
        xh = np.array([np.sum(dX[indici(m, n, i)] * ph) for i in range(6)]) / (L * L)
        resto = xh.copy()
        for nm in ("fotone", "ottica"):
            vec = sum(uu * np.vdot(ww, xh) for uu, ww in zip(bks[nm][1], bks[nm][2]))
            resto = resto - vec
            parte[nm] += L * L * float(np.vdot(vec, vec).real)
        parte["gauge"] += L * L * float(np.vdot(resto, resto).real)
    return {k: math.sqrt(v) for k, v in parte.items()}


def main():
    import _presidio
    import _u1_prototipo as U1
    import _triangoli_forza as TF
    from solitone import u1_t4b as T4B
    _presidio.avvia(os.path.join(os.path.dirname(_QUI), "_u1_prototipo.py"))
    _presidio.avvia(os.path.join(_QUI, "u1_t4b.py"))
    _presidio.avvia(__file__)
    estar = U1.E_PROVA[1]
    L, S = T4B.L, T4B.S
    print("=" * 130)
    print("T4-B, LA DIAGNOSI DEL VERSO DELLA FASE (sez. 16.2): L %d, s %g, e* %.10f, eps %s, conv %s; k = 2 pi n d / L, n %s, d %s"
          % (L, S, estar, EPS3, T4B.CONV, list(T4B.N_K), T4B.DIREZ))
    print("=" * 130)
    bl, _f, _r = U1.blocchi_campo(S)
    V = {}
    with TF.conv(T4B.CONV):
        B = T4B.Banco(U1, estar)
        _p0, a0, e0 = B.tick()     # ### la sez. 16.2 annotata: le scale del pavimento, nella stessa convenzione
        scala = {"<-": float(np.sqrt(np.sum(a0 * a0) + np.sum(e0 * e0))), "->": float(np.sqrt(np.sum(np.abs(_p0) ** 2)))}
        print("### le scale del pavimento: il campo dello sfondo dopo un tick %.3e, psi %.6f" % (scala["<-"], scala["->"]))
        c = B.c
        n, m = c.n, c.m
        nodo = B.mot.inc.nodo
        psi0 = B.foto["psi_h"]
        for d in T4B.DIREZ:
            for nk in T4B.N_K:
                t1, t2 = 2 * math.pi * nk * d[0] / L, 2 * math.pi * nk * d[1] / L
                bk = T4B.bande_k(U1, bl, t1, t2)[0]
                fase = t1 * B.m1 + t2 * B.m2
                cosn = np.cos(fase)[nodo]
                for pnome, fatt in (("<-fase", 1j), ("<-ampiezza", 1.0)):
                    dpsi = fatt * psi0 * cosn[:, None]
                    dpsi = dpsi / float(np.sqrt(np.sum(np.abs(dpsi) ** 2)))
                    for ep in EPS3:
                        for b, v in indietro(T4B, U1, B, bl, t1, t2, dpsi, ep).items():
                            V[(d, nk, pnome, b, ep)] = v
                # ---------------- (->) il fotone, le righe di u1_t4b.main
                u = bk["fotone"][1][0]
                u = u * np.exp(-1j * np.angle(u[int(np.argmax(np.abs(u)))]))
                x = np.zeros(2 * m)
                for i in range(6):
                    x[indici(m, n, i)] = np.real(u[i] * np.exp(1j * fase))
                nx = float(np.sqrt(np.sum(x * x)))
                for ep in EPS3:
                    pp = B.tick(dA=ep * x[:m] / nx, dE=ep * x[m:] / nx)[0]
                    pm = B.tick(dA=-ep * x[:m] / nx, dE=-ep * x[m:] / nx)[0]
                    V[(d, nk, "->", "fotone", ep)] = float(np.sqrt(np.sum(np.abs(pp - pm) ** 2))) / (2 * ep)
                if nk == 12:
                    for nm in ("fotone", "ottica"):
                        uu = bk[nm][1][0]
                        uu = uu * np.exp(-1j * np.angle(uu[int(np.argmax(np.abs(uu)))]))
                        print("  STAMPA d %s n 12, %s: u reale %s | u immaginaria %s" % (d, nm, " ".join("%+.4f" % a for a in uu.real), " ".join("%+.4f" % a for a in uu.imag)))
                sys.stdout.flush()
    lne = np.log(np.array(EPS3))
    # ### il pavimento: l'arrotondamento della differenza simmetrica, eps_macchina x la SCALA di cio' che si sottrae / eps
    # ### (l'annotazione della sez. 16.2: la scala del campo dello sfondo per (<-), la norma di psi = 1 per (->))

    def pend(d, nk, ver, b):
        y = np.array([V[(d, nk, ver, b, ep)] for ep in EPS3])
        pav = FATT_PAV * np.finfo(float).eps * scala[ver[:2]] / np.array(EPS3)
        if np.any(y <= pav):
            return None, y
        return float(np.polyfit(lne, np.log(y), 1)[0]), y
    righe = [("<-fase", "fotone"), ("<-fase", "ottica"), ("<-fase", "gauge"), ("<-ampiezza", "fotone"), ("<-ampiezza", "ottica"), ("<-ampiezza", "gauge"), ("->", "fotone")]
    print("-" * 130)
    print("### p = la pendenza di ln V contro ln eps (\"pav\" = sotto %g x l'arrotondamento a qualche eps: eps_macchina x la scala / eps); T4B-L = |V(1e-4) - V(5e-5)| / V(1e-4)" % FATT_PAV)
    print("  %6s %3s | %s" % ("d", "n", " | ".join("%-21s" % ("%s %s" % r) for r in righe)))
    P = {}
    for d in T4B.DIREZ:
        for nk in T4B.N_K:
            pezzi = []
            for (ver, b) in righe:
                p, y = pend(d, nk, ver, b)
                P[(d, nk, ver, b)] = p
                tl = abs(y[0] - y[1]) / y[0] if y[0] > 0 else float("nan")
                pezzi.append("%-21s" % (("p %+.3f L %.1e" % (p, tl)) if p is not None else ("pav (V %.1e)" % y[0])))
            print("  %6s %3d | %s" % ("%d,%d" % d, nk, " | ".join(pezzi)))
    print("-" * 130)

    def tutti(ver, b):
        return [P[(d, nk, ver, b)] for d in T4B.DIREZ for nk in T4B.N_K]
    for b in ("fotone", "ottica"):
        pp = [p for p in tutti("<-fase", b) if p is not None]
        peg = max(abs(p - 2.0) for p in pp) if pp else float("nan")
        esito("D-G %s in fase: |p - 2| <= %g a ogni k sopra il pavimento" % (b, TOLL_G), bool(pp) and peg <= TOLL_G, "%d k sopra il pavimento su %d; il peggiore |p - 2| %.3f" % (len(pp), len(tutti("<-fase", b)), peg))
    pg = tutti("<-fase", "gauge")
    esito("D-G0 la gauge in fase: |p| <= %g a ogni k (primo ordine)" % TOLL_0, all(p is not None for p in pg) and max(abs(p) for p in pg) <= TOLL_0,
          "il peggiore |p| %s" % ("%.2e" % max(abs(p) for p in pg) if all(p is not None for p in pg) else "pav"))
    for ver in ("->", "<-ampiezza"):
        pf = [p for p in tutti(ver, "fotone") if p is not None]
        esito("D-P il fotone (%s): |p| <= %g a ogni k sopra il pavimento (primo ordine)" % (ver, TOLL_0), bool(pf) and max(abs(p) for p in pf) <= TOLL_0,
              "%d k su %d; il peggiore |p| %.2e" % (len(pf), len(tutti(ver, "fotone")), max(abs(p) for p in pf) if pf else float("nan")))
    pgf = [p for p in pg if p is not None]
    esito("D-F il test D-G applicato alla gauge in fase: |p - 2| <= %g" % TOLL_G, bool(pgf) and max(abs(p - 2.0) for p in pgf) <= TOLL_G,
          "il peggiore |p - 2| %.3f" % (max(abs(p - 2.0) for p in pgf) if pgf else float("nan")), deve=False)
    print("=" * 130)
    print("ESITO: %d/%d controlli come devono; fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main())
