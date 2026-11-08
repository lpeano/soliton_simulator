# -*- coding: utf-8 -*-
r"""**IL PERIODO DI `TB3`: METODO (p1) O FISICA (p2)?** *(Luca `2026-11-08` `20:57`, M3; il task history `doc/TASK_HISTORY/2026-11-07_allungamenti_coppia_30000.md`, sez. `7.9`)*. [[PIANO-2D-3D]]

    python csv/solitone/periodo_tb3.py > doc/referti_l2/periodo_tb3.txt

**Sulle serie INTERE di `TB3` e `TBS`** *(da `t 1000` alla fine)*, **per ognuna delle sei grandezze di `stazionarieta.serie_singolo`, tolta la retta:**
**(m1) il periodogramma della serie intera** *(il picco, stampato)*; **(m2) Welch, finestra di Hann, segmenti di `7000` e di `9500` unita'** *(nessuno multiplo di `1500`)*
**sovrapposti a meta'; (m3) il caso NULLO: l'AR(1) col ritardo-1 della serie, il suo spettro teorico scalato alla potenza media di Welch, la soglia al `99%`**
*(il `chi^2` coi gradi di liberta' equivalenti di Welch, `36 K^2 / (19 K - 1)` per Hann a meta' sovrapposizione)* **corretta per il numero di bin guardati** *(Bonferroni)*.
### **I CONTROLLI:** `PE-P` *(DEVE PASSARE: AR(1) piu' un seno a `2300`, ritrovato sopra la soglia entro un bin, a tutte e due le lunghezze)*;
`PE-N` *(DEVE FALLIRE: l'AR(1) puro, «un picco sopra la soglia»)*; `PE-W` *(STAMPA: il metodo vecchio `stazionarieta.periodo` su `[1000, 10000]` di `20` AR(1) puri)*.
"""
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))
import solitone  # noqa: E402,F401  (i percorsi)

T_DA = 1000.0                  # ### come stazionarieta (Luca q-s1: dopo la rampa)
SEGMENTI = (7000.0, 9500.0)    # ### mio, dichiarato (sez. 7.9): non multipli di 1500; il periodo piu' lungo guardato L/2 (3500, 4750) contiene 2300
P_MIN = 300.0                  # ### mio, dichiarato: i periodi guardati da 300 a L/2
ALFA = 0.01                    # ### sez. 7.9: il 99%, poi Bonferroni
P_SENO = 2300.0                # ### PE-P
AMP_SENO = 3.0                 # ### PE-P: 3 volte la deviazione del rumore
VICINO_A = 1500.0              # ### il periodo da spiegare
OK = [0, 0]
FALLITE = []


def esito(che, passa, nota="", deve=True):
    OK[1] += 1
    buono = passa if deve else not passa
    OK[0] += 1 if buono else 0
    if not buono:
        FALLITE.append(che)
    print("  %s: %-110s %s   %s" % ("DEVE PASSARE" if deve else "DEVE FALLIRE", che[:110], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return buono


def togli_retta(t, x):
    return x - np.polyval(np.polyfit(t, x, 1), t)


def welch(x, dt, L):
    """### `(f, potenza, K)`: Hann, segmenti di `L` unita', meta' sovrapposti, la media di ogni segmento tolta."""
    n = int(round(L / dt))
    passo = n // 2
    w = np.hanning(n)
    pot, K = None, 0
    for a in range(0, len(x) - n + 1, passo):
        y = x[a:a + n] - np.mean(x[a:a + n])
        p = np.abs(np.fft.rfft(w * y)) ** 2
        pot = p if pot is None else pot + p
        K += 1
    return np.fft.rfftfreq(n, dt), pot / K, K


def soglia_ar1(x, dt, f, pot, K, sel):
    """### la soglia per bin: lo spettro dell'AR(1) col ritardo-1 di `x`, scalato alla potenza media di Welch nei bin `sel`, per `chi^2_nu(1 - alfa / nbin) / nu`."""
    from scipy.stats import chi2
    y = x - x.mean()
    phi = float(np.dot(y[:-1], y[1:]) / np.dot(y, y))
    s_ar = (1.0 - phi * phi) / (1.0 - 2.0 * phi * np.cos(2.0 * math.pi * f * dt) + phi * phi)
    s_ar = s_ar * (np.mean(pot[sel]) / np.mean(s_ar[sel]))
    nu = 36.0 * K * K / (19.0 * K - 1.0)
    nbin = int(sel.sum())
    return s_ar * chi2.ppf(1.0 - ALFA / nbin, nu) / nu, phi, nu, nbin


def picchi(t, x, L):
    """### `(lista dei picchi sopra la soglia [(P, pot/soglia)], il picco piu' forte (P, pot/soglia), il passo in P a quel picco, phi, nu, K)`."""
    dt = float(np.median(np.diff(t)))
    f, pot, K = welch(x, dt, L)
    with np.errstate(divide="ignore"):
        P = np.where(f > 0, 1.0 / np.where(f > 0, f, 1.0), np.inf)
    sel = (P >= P_MIN) & (P <= L / 2.0)
    s, phi, nu, nbin = soglia_ar1(x, dt, f, pot, K, sel)
    r = np.where(sel, pot / s, 0.0)
    massimi = [k for k in range(1, len(r) - 1) if r[k] > 1.0 and r[k] >= r[k - 1] and r[k] >= r[k + 1]]   # ### solo i MASSIMI LOCALI: il lobo di Hann non conta due volte
    sopra = sorted([(float(P[k]), float(r[k])) for k in massimi], key=lambda q: -q[1])
    k = int(np.argmax(r))
    df = float(f[1] - f[0])
    return sopra, (float(P[k]), float(r[k])), float(P[k] ** 2 * df), phi, nu, K


def ar1(n, phi, rg):
    e = rg.normal(size=n)
    a = np.empty(n)
    a[0] = e[0] / math.sqrt(1.0 - phi * phi)
    for i in range(1, n):
        a[i] = phi * a[i - 1] + e[i]
    return a


def leggi(nome, t, x):
    """### stampa (m1), (m2) per una grandezza; rende `{L: (sopra, forte, passo)}`."""
    sel = t >= T_DA
    tt, xx = t[sel], togli_retta(t[sel], x[sel])
    dt = float(np.median(np.diff(tt)))
    p1 = np.abs(np.fft.rfft(xx)) ** 2
    f1 = np.fft.rfftfreq(len(xx), dt)
    s1 = (f1 > 0) & (1.0 / np.where(f1 > 0, f1, 1.0) >= P_MIN)
    k1 = int(np.argmax(np.where(s1, p1, 0.0)))
    out = {}
    riga = ["(m1) intera: il picco P %.0f (passo %.0f)" % (1.0 / f1[k1], (1.0 / f1[k1]) ** 2 * (f1[1] - f1[0]))]
    for L in SEGMENTI:
        sopra, forte, passo, phi, nu, K = picchi(tt, xx, L)
        out[L] = (sopra, forte, passo)
        riga.append("(m2) L %.0f K %d nu %.1f phi %.4f: il piu' forte P %.0f (passo %.0f) a %.2f della soglia; sopra la soglia %s"
                    % (L, K, nu, phi, forte[0], passo, forte[1], ", ".join("%.0f (%.2f)" % q for q in sopra) if sopra else "NESSUNO"))
    print("    %-12s %s" % (nome, riga[0]))
    for r_ in riga[1:]:
        print("    %-12s %s" % ("", r_))
    sys.stdout.flush()
    return out


def stesso_periodo(out):
    """### il massimo PIU' FORTE sopra la soglia, alle due lunghezze, allo STESSO periodo entro il passo piu' largo: `(si/no, P)`."""
    a, b = (out[L][0] for L in SEGMENTI)
    if not a or not b:
        return False, None
    Pa, Pb = a[0][0], b[0][0]
    if abs(Pa - Pb) <= max(Pa * Pa / SEGMENTI[0], Pb * Pb / SEGMENTI[1]):
        return True, 0.5 * (Pa + Pb)
    return False, None


def main():
    import _presidio
    import _vuoto_vivo_B as V
    from solitone import corsa_accensione as CA
    from solitone import stazionarieta as ST
    _presidio.avvia(os.path.join(_QUI, "corsa_accensione.py"))
    _presidio.avvia(os.path.join(_QUI, "stazionarieta.py"))
    _presidio.avvia(__file__)
    s = V.CORSE[CA.NOME][2]
    print("=" * 130)
    print("IL PERIODO DI TB3 (Luca 20:57, M3): da t %g; Welch Hann segmenti %s a meta'; periodi da %g a L/2; il nullo AR(1) al %g%% con Bonferroni; s %g"
          % (T_DA, SEGMENTI, P_MIN, 100 * (1 - ALFA), s))
    print("=" * 130)
    # ------------------------------------------------------------ i controlli, sulla lunghezza e il phi dello spostamento di TB3
    t3, s3 = ST.serie_singolo("TB3", s)
    sel = t3 >= T_DA
    tt = t3[sel]
    x0 = togli_retta(tt, s3["spostamento"][sel])
    y0 = x0 - x0.mean()
    phi3 = float(np.dot(y0[:-1], y0[1:]) / np.dot(y0, y0))
    print("### I CONTROLLI (AR(1) con phi %.4f, %d campioni, dt %.2f, come lo spostamento di TB3)" % (phi3, len(tt), float(np.median(np.diff(tt)))))
    rg = np.random.default_rng(2026)
    rum = ar1(len(tt), phi3, rg)
    seno = rum + AMP_SENO * float(np.std(rum)) * np.sin(2.0 * math.pi * tt / P_SENO)
    ok_p = True
    note = []
    for L in SEGMENTI:
        sopra, forte, passo, _phi, _nu, _K = picchi(tt, togli_retta(tt, seno), L)
        trovato = bool(sopra) and abs(sopra[0][0] - P_SENO) <= sopra[0][0] ** 2 / L   # ### il massimo PIU' FORTE, entro un bin
        ok_p = ok_p and trovato
        note.append("L %.0f: %s" % (L, ", ".join("%.0f (%.2f)" % q for q in sopra) or "nessuno"))
    esito("PE-P l'AR(1) piu' un seno di periodo %g: ritrovato SOPRA la soglia entro un bin, a tutte e due le lunghezze" % P_SENO, ok_p, "; ".join(note))
    falso = False
    note = []
    for L in SEGMENTI:
        sopra, forte, passo, _phi, _nu, _K = picchi(tt, togli_retta(tt, rum), L)
        falso = falso or bool(sopra)
        note.append("L %.0f: il piu' forte P %.0f a %.2f della soglia" % (L, forte[0], forte[1]))
    esito("PE-N l'AR(1) PURO: un picco sopra la soglia", falso, "; ".join(note), deve=False)
    trovati = []
    for i in range(20):
        r_ = ar1(len(t3), phi3, np.random.default_rng(100 + i))
        P_, _ps = ST.periodo(t3, r_, ST.T_PERIODO[0], ST.T_PERIODO[1])
        trovati.append(P_)
    print("  STAMPA: PE-W il metodo vecchio (stazionarieta.periodo su %s) su 20 AR(1) puri: un 'periodo' in %d su 20: %s"
          % (ST.T_PERIODO, sum(p is not None for p in trovati), ", ".join("%.0f" % p if p else "-" for p in trovati)))
    # ------------------------------------------------------------ le serie vere
    esiti = {}
    for nome in ("TB3", "TBS"):
        t, ser = ST.serie_singolo(nome, s)
        print("### %s: fino a t %.0f, %d campioni" % (nome, t[-1], len(t)))
        for k in sorted(ser):
            out = leggi(k, t, ser[k])
            esiti[(nome, k)] = stesso_periodo(out)
    print("### LE LETTURE (fissate nella sez. 7.9 prima della misura)")
    for (nome, k), (si, P) in sorted(esiti.items()):
        print("  %-4s %-12s un picco sopra la soglia allo STESSO periodo alle due lunghezze: %s" % (nome, k, "SI', P %.0f" % P if si else "no"))
    si3, P3 = esiti[("TB3", "spostamento")]
    siS, PS = esiti[("TBS", "spostamento")]
    if not si3:
        let = "(p1) METODO: nello spostamento di TB3 nessun picco sopra la soglia allo stesso periodo alle due lunghezze"
    elif siS and abs(PS - P3) <= max(P3 * P3 / SEGMENTI[0], 1.0):
        let = "AMBIGUO: TB3 e TBS allo STESSO periodo (%.0f e %.0f): si chiede a Luca" % (P3, PS)
    elif siS:
        let = "(p2) FISICA: TB3 a P %.0f, TBS a un periodo DIVERSO (%.0f)" % (P3, PS)
    else:
        let = "TB3 a P %.0f sopra la soglia, TBS senza picco: non previsto dalle letture, si scrive e si chiede a Luca" % P3
    print("  LA LETTURA: %s" % let)
    print("=" * 130)
    print("### %d su %d%s" % (OK[0], OK[1], ("   FALLITE: " + "; ".join(FALLITE)) if FALLITE else "   TUTTI COME DEVONO"))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main())
