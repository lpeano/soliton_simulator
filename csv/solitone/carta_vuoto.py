# -*- coding: utf-8 -*-
r"""**IL SOLITONE VESTITO: LA LETTURA SULLA CARTA** *(il mandato di Luca delle `01:04` del `2026-11-02`, passo `2`, con la correzione delle `01:06`; il task history
`doc/TASK_HISTORY/2026-11-02_solitone_vestito.md`)*: ### **i test del vuoto (`V0`-`V4`), le bande del vuoto attorno a `F0`, dove cadono `n mu` di BG-F-0.15 e `nu` di `F0`;**
### **la vita di BG-F-0.15 con la soglia della decisione `9`**, dai campioni committati di `_vuoto_vivo_B`.

    python csv/solitone/carta_vuoto.py > doc/referti_l2/solitone_vestito_carta.txt
"""
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))

import solitone  # noqa: E402,F401  (i percorsi)

NOME = "BG-F-0.15"
ARMONICHE = (1, 2, 3)          # ### n mu, n = 1, 2, 3 (il mandato)
OK = [0, 0]
FALLITE = []


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    if not passa:
        FALLITE.append(che)
    print("  %-110s %s   %s" % (che[:110], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return passa


def main():
    import _presidio
    for m in ("__init__", "protetto", "vuoto", "test_vuoto"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(__file__)
    import _vuoto_vivo_B as V
    from solitone import test_vuoto
    from solitone import vuoto as VU
    sol, vuoto, s = V.CORSE[NOME]
    testa, _camp, dd, _rr = V.serie(NOME)
    mu = testa["info"]["mu"]
    P = 2.0 * math.pi / s
    print("=" * 130)
    print("IL SOLITONE VESTITO (Luca 01:04, passo 2): LA LETTURA SULLA CARTA -- le bande del vuoto linearizzato attorno a F0 (il tick intero, psi = 0), n mu e nu, la vita con la soglia 9")
    print("  la configurazione: %s (%s, il vuoto %s, s %g, eps %g, N %.0e, L %d, la forma della tabella, cs spento); ARMONICHE %s; la soglia della vita %g (_massimo_di_B.SOGLIA, decisione 9)"
          % (NOME, sol, vuoto, s, V.EPS, V.N, V.L, ARMONICHE, V.MB.SOGLIA))
    print("  il periodo delle frequenze 2 pi/s = %.6f; mu di %s (il primo pezzo committato) %+.12f, il residuo per tick della partenza %.3e" % (P, NOME, mu, testa["info"]["residuo"]))
    print("=" * 130)
    r = test_vuoto.gira(esito)
    A, taglio, inter, gap, nu = r["A"], r["taglio"], r["inter"], r["gap"], r["nu"]
    L = r["L"]
    print("### LE BANDE DEL VUOTO (le frequenze -arg/s mod 2 pi/s su %d x %d punti k, le 3 direzioni %s; gli intervalli dal taglio %.6f, nel mezzo del gap piu' largo %.6f)" % (L, L, r["dirs"], taglio, gap))
    for j, (lo, hi) in enumerate(inter):
        print("    banda %d: in assoluto [%.6f, %.6f] mod %.6f, larga %.6f" % (j, np.mod(lo + taglio, P), np.mod(hi + taglio, P), P, hi - lo))
    fusi = VU.unione(inter)
    cop = sum(hi - lo for lo, hi in fusi)
    gapl = ["[%.6f, %.6f]" % (np.mod(a[1] + taglio, P), np.mod(b[0] + taglio, P)) for a, b in zip(fusi, fusi[1:] + [[fusi[0][0] + P, 0.0]])]
    print("    l'unione: %d intervalli, coprono %.6f su %.6f (%.2f%%); i gap: %s" % (len(fusi), cop, P, 100.0 * cop / P, ", ".join(gapl)))
    print("    a Gamma (k = 0) le 6 frequenze: %s" % " ".join("%.6f" % x for x in sorted(np.mod(-np.angle(np.linalg.eigvals(A[0, 0])) / s, P))))
    print("### DOVE CADONO n mu (la lettura di Luca) E nu di F0 (il margine: la distanza dal bordo di banda piu' vicino, NEGATIVO se dentro)")
    for n_ in ARMONICHE:
        fr = float(np.mod(n_ * mu, P))
        d, m, jj = VU.margine(fr, taglio, inter, s)
        print("    %d mu = %.9f (mod 2 pi/s %.9f): %s, margine %+.6f%s" % (n_, n_ * mu, fr, "### DENTRO una banda del vuoto" if d else "fuori dalle bande", m, (" (bande %s)" % jj) if jj else ""))
    d_nu, m_nu, j_nu = r["margine_nu"]
    print("    nu (F0) = %.9f: %s, margine %+.3e%s" % (nu, "dentro" if d_nu else "sul bordo" if m_nu <= test_vuoto.TOLL_BORDO else "fuori", m_nu, (" (bande %s)" % j_nu) if j_nu else ""))
    print("### LA VITA DI %s CON LA SOGLIA DELLA DECISIONE 9 (il primo tau con |D|/|psi0| >= %g; i campioni D committati di _vuoto_vivo_B, ogni %d tick)" % (NOME, V.MB.SOGLIA, V.OGNI_D))
    sopra = [d for d in dd if d["nD"] >= V.MB.SOGLIA]
    print("    i campioni: %d, da tempo %.1f a %.1f; il primo: tempo %.1f, |D|/|psi0| %.4e" % (len(dd), dd[0]["t"] * s, dd[-1]["t"] * s, dd[0]["t"] * s, dd[0]["nD"]))
    if sopra:
        print("    t_vita (soglia 9) = %.1f%s" % (sopra[0]["t"] * s, ": ### il PRIMO campione -- la soglia misura la deriva della partenza non ferma, non una perdita" if sopra[0] is dd[0] else ""))
    else:
        print("    |D|/|psi0| resta sotto la soglia in tutti i campioni")
    print("=" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    return 0 if OK[0] == OK[1] else 1


if __name__ == "__main__":
    sys.exit(main())
