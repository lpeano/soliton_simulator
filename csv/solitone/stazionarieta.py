# -*- coding: utf-8 -*-
r"""**LA LETTURA DI STAZIONARIETA'** *(Luca `2026-11-07` `10:50`, le decisioni q-s1..q-s6; il task history `doc/TASK_HISTORY/2026-11-07_allungamenti_coppia_30000.md`, sez. `5` e `7`)*. [[PIANO-2D-3D]]

    python csv/solitone/stazionarieta.py > doc/referti_l2/stazionarieta.txt

### **Il criterio:** **due finestre adiacenti `[T - 2W, T - W]`, `[T - W, T]`** *(contate da `t 1000`, dopo la rampa)* **con medie che differiscono meno di `2 sqrt(e1^2 + e2^2)` per TUTTE le
grandezze; «stazionario da `t X`» quando vale per TRE controlli di fila** *(le fini dei pezzi, ogni `1500` unita')*. **L'errore della media `sigma sqrt(2 tau_int / N)`, `tau_int` di Sokal
con `c = 5`. `W = 3 P`, `P` il picco del periodogramma fra `t 1000` e `10000`, stimato una volta** *(`6000` se non si stima)*. ### **I DEVE:** `ST-P`, `ST-B` *(un AR(1): Sokal)*, `ST-I`;
**`ST-S`** *(stampa)* **su `S162`, `TB3`, `TBS`; `ST-F`** *(DEVE FALLIRE)* **su casi COSTRUITI** *(Luca `18:08`: una serie stazionaria e la stessa con una deriva nota)*; **la pendenza col suo errore nel tempo, il ritmo di perdita e la vita come estrapolazione** *(s3)*; **il periodo di `TB3` a un altro passo e dentro i pezzi.** **Le funzioni le usa anche `carta_coppia`.**
"""
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))
import solitone  # noqa: E402,F401  (i percorsi)

C_SOKAL = 5.0                  # ### Luca q-s3: il taglio standard di Sokal (e di emcee)
T_RAMPA = 1000.0               # ### Luca q-s1: le finestre da t 1000
T_PERIODO = (1000.0, 10000.0)  # ### Luca q-s5: P stimato una volta, sulla serie fino a 10000
W_RIPIEGO = 6000.0             # ### sez. 4.2: se P non si stima
PASSO_CONTROLLI = 1500.0       # ### le fini dei pezzi: 10000 tick x s 0.15
FATTORE_DIFF = 2.0             # ### sez. 4.2: meno di 2 volte l'errore della differenza
CONTROLLI_DI_FILA = 3          # ### sez. 4.2
FATTORE_B = 1.5                # ### ST-B, mio, dichiarato: tau_int entro un fattore 1.5
TOLL_I = 0.01                  # ### ST-I, mio, dichiarato
T_PARTENZA_TF3C = 16000.0      # ### ST-F: la partenza di TF3C
OK = [0, 0]
FALLITE = []
VITA = {}
PASSI_PERIODO = (1000, 700)    # ### Luca 18:08: il periodo di TB3 a un altro passo (tick)
TICK_PEZZO = 10000


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    if not passa:
        FALLITE.append(che)
    print("  %-118s %s   %s" % (che[:118], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return passa


def tau_int(x):
    """### `(tau_int, M)`: `1/2 + somma_{k=1..M} rho(k)`, `M` il piu' piccolo con `M >= C_SOKAL tau_int(M)`; `rho` dall'FFT con la media tolta."""
    x = np.asarray(x, dtype=float)
    n = len(x)
    if n < 4 or float(np.var(x)) == 0.0:
        return 0.5, 0
    y = x - x.mean()
    f = np.fft.rfft(y, 2 * n)
    ac = np.fft.irfft(f * np.conj(f))[:n]
    rho = ac / ac[0]
    tau = 0.5
    for M in range(1, n):
        tau += rho[M]
        if M >= C_SOKAL * tau:
            return float(tau), M
    return float(tau), n - 1


def errore_media(x):
    x = np.asarray(x, dtype=float)
    tau, _M = tau_int(x)
    return float(np.std(x)) * math.sqrt(2.0 * max(tau, 0.5) / len(x))


def periodo(t, x, t_da, t_a):
    """### `(P, passo)`: il picco del periodogramma della serie su `[t_da, t_a]`, tolta la retta; `(None, None)` se non c'e' un picco interno."""
    t = np.asarray(t, dtype=float)
    x = np.asarray(x, dtype=float)
    sel = (t >= t_da) & (t <= t_a)
    tt, xx = t[sel], x[sel]
    if len(tt) < 8:
        return None, None
    xx = xx - np.polyval(np.polyfit(tt, xx, 1), tt)
    dt = float(np.median(np.diff(tt)))
    pot = np.abs(np.fft.rfft(xx)) ** 2
    fr = np.fft.rfftfreq(len(xx), dt)
    k = int(np.argmax(pot[1:])) + 1
    if k <= 1 or k >= len(fr) - 1:
        return None, None
    P = 1.0 / fr[k]
    passo = P * P * (fr[1] - fr[0])                 # ### dP = P^2 df
    return float(P), float(passo)


def allungamento(rho, xx, yy):
    """### `sqrt(l_max / l_min)` del tensore d'inerzia della densita' `rho` sulle coordinate cartesiane `(xx, yy)` *(gia' scartate dal centro)*."""
    w = np.asarray(rho, dtype=float)
    m = float(w.sum())
    cx, cy = float((w * xx).sum() / m), float((w * yy).sum() / m)
    dx, dy = xx - cx, yy - cy
    I = np.array([[(w * dx * dx).sum(), (w * dx * dy).sum()], [(w * dx * dy).sum(), (w * dy * dy).sum()]]) / m
    ev = np.linalg.eigvalsh(I)
    return float(math.sqrt(ev[1] / ev[0]))


def pendenza(t, x):
    """### `(pendenza, errore)` ai minimi quadrati: l'errore `sigma_res sqrt(2 tau_int / N) / sqrt(somma (t - tbar)^2 / N)` *(Luca s3: dalla `tau_int` di Sokal)*."""
    t = np.asarray(t, dtype=float)
    x = np.asarray(x, dtype=float)
    p = np.polyfit(t, x, 1)
    res = x - np.polyval(p, t)
    tau, _M = tau_int(res)
    n = len(t)
    st_ = math.sqrt(float(np.sum((t - t.mean()) ** 2)) / n)
    err = float(np.std(res)) * math.sqrt(2.0 * max(tau, 0.5) / n) / st_ if st_ > 0 else float("inf")
    return float(p[0]), err


def pendenze_nel_tempo(t, x, W, t_controlli):
    """### `[(T, pendenza, errore)]` nelle finestre `[T - W, T]`."""
    t = np.asarray(t, dtype=float)
    out = []
    for T in t_controlli:
        if T - W < T_RAMPA or T > t[-1] + 1e-9:
            continue
        sel = (t >= T - W) & (t <= T)
        out.append((T,) + pendenza(t[sel], np.asarray(x)[sel]))
    return out


CONSERVATE = ("E + E_ass", "E")   # ### Luca 18:42: le grandezze conservate col criterio delle due medie; tutte le altre DERIVANO (il criterio delle pendenze)


def lettura(t, serie, W, t_controlli):
    """### **IL REGIME DI DECADIMENTO** *(Luca `18:42`)*: per ogni `T`, le due finestre `[T - 2W, T - W]` e `[T - W, T]`: **le grandezze CONSERVATE** con le medie che differiscono meno
    di `2 sqrt(e1^2 + e2^2)`; **quelle che DERIVANO** con le PENDENZE che differiscono meno di `2 sqrt(e1^2 + e2^2)`; `t_X` il primo `T` di `CONTROLLI_DI_FILA` controlli di fila con
    TUTTE nel loro regime. `(t_X o None, righe)`."""
    t = np.asarray(t, dtype=float)
    righe = []
    di_fila = 0
    t_x = None
    for T in t_controlli:
        if T - 2.0 * W < T_RAMPA or T > t[-1] + 1e-9:
            continue
        a = (t >= T - 2.0 * W) & (t < T - W)
        b = (t >= T - W) & (t <= T)
        ok, det = True, {}
        for nome, x in serie.items():
            x = np.asarray(x, dtype=float)
            if nome in CONSERVATE:
                m1, m2 = float(x[a].mean()), float(x[b].mean())
                e1, e2 = errore_media(x[a]), errore_media(x[b])
            else:
                m1, e1 = pendenza(t[a], x[a])
                m2, e2 = pendenza(t[b], x[b])
            sig = math.sqrt(e1 * e1 + e2 * e2)
            passa = abs(m2 - m1) < FATTORE_DIFF * sig if sig > 0 else m2 == m1
            ok = ok and passa
            det[nome] = (m1, m2, sig, passa)
        di_fila = di_fila + 1 if ok else 0
        if di_fila >= CONTROLLI_DI_FILA and t_x is None:
            t_x = T
        righe.append((T, ok, di_fila, det))
    return t_x, righe


def serie_singolo(nome, s):
    """### Le grandezze di un singolo dai jsonl: `(t in unita', {nome: array})`."""
    from solitone import corsa_accensione as CA
    _rr, camp = CA.serie(nome)[:2]
    t = np.array([c["t"] for c in camp], dtype=float) * s
    con_bordo = "bordo" in camp[0] and camp[0]["bordo"].get("E_ass") is not None
    E = np.array([c["E"]["totale"]["tot"] for c in camp])
    if con_bordo:
        E = E + np.array([c["bordo"]["E_ass"] for c in camp])
    x = np.array([c["x"] for c in camp], dtype=float)
    y = np.array([c["y"] for c in camp], dtype=float)
    out = {"E + E_ass" if con_bordo else "E": E, "w": np.array([c["w"] for c in camp], dtype=float),
           "alone": np.array([c["alone"] for c in camp], dtype=float), "spostamento": np.hypot(x - x[0], y - y[0])}
    if con_bordo:
        Ma = np.array([c["bordo"]["M_ass"] for c in camp], dtype=float)
        out["emissione"] = np.concatenate([[0.0], np.diff(Ma)])
        VITA[nome] = (t, Ma, np.array([c["bordo"]["M_dentro"] for c in camp], dtype=float))
        out["cuore"] = VITA[nome][2]
    return t, out


def stampa_lettura(nome, t, serie, W, P, passo):
    t_c = np.arange(PASSO_CONTROLLI, t[-1] + 1e-9, PASSO_CONTROLLI)
    t_x, righe = lettura(t, serie, W, t_c)
    print("  %-8s fino a t %.0f; P %s; W %.0f; le grandezze %s" % (nome, t[-1], ("%.1f (passo %.1f)" % (P, passo)) if P else "non stimato", W, sorted(serie)))
    for T, ok, df, det in righe:
        print("    T %7.0f  %s di fila %d  %s" % (T, "si" if ok else "no", df, "  ".join("%s %s" % (k, "ok" if v[3] else "NO(%.2g)" % (abs(v[1] - v[0]) / v[2] if v[2] else float("inf"))) for k, v in sorted(det.items()))))
    print("    LA LETTURA: %s" % ("il REGIME DI DECADIMENTO raggiunto da t %.0f entro la finestra osservata" % t_x if t_x is not None else "il regime NON raggiunto entro t %.0f (la finestra osservata)" % t[-1]))
    # ### (s3, Luca 18:08) la PENDENZA nella finestra col suo errore, nel tempo; se cala; il ritmo di perdita e la vita (estrapolazione)
    for k in sorted(serie):
        pp = pendenze_nel_tempo(t, serie[k], W, t_c)
        if not pp:
            continue
        TT = np.array([q[0] for q in pp])
        sl = np.array([q[1] for q in pp])
        print("    (s3) %-12s la pendenza nella finestra, nel tempo: %s" % (k, "  ".join("%.0f:%+.3e(%.1e)" % q for q in pp)))
        if len(pp) >= 3:
            c, ce = pendenza(TT, sl)
            print("    (s3) %-12s la pendenza della pendenza %+.3e +- %.1e: %s" % (k, c, ce, "CALA in modulo (si avvicina a uno stato fisso)" if c * sl.mean() < 0 and abs(c) > 2 * ce else ("COSTANTE entro l'errore" if abs(c) <= 2 * ce else "CRESCE in modulo")))
    return t_x, righe


def main():
    import _presidio
    import _vuoto_vivo_B as V
    from solitone import corsa_accensione as CA
    _presidio.avvia(os.path.join(_QUI, "corsa_accensione.py"))
    _presidio.avvia(__file__)
    s = V.CORSE[CA.NOME][2]
    print("=" * 130)
    print("LA LETTURA DI STAZIONARIETA' (Luca q-s1..q-s6): Sokal c %g; finestre da t %g; P su %s; W = 3P (ripiego %g); controlli ogni %g; %d di fila; s %g" % (C_SOKAL, T_RAMPA, T_PERIODO, W_RIPIEGO, PASSO_CONTROLLI, CONTROLLI_DI_FILA, s))
    print("=" * 130)
    rng = np.random.default_rng(7)
    # ------------------------------------------------------------ ST-P
    P0 = 137.0
    tt = np.arange(0.0, 20000.0, 1.5)
    x = np.sin(2 * math.pi * tt / P0) + 0.3 * rng.normal(size=len(tt))
    P, passo = periodo(tt, x, 0.0, 20000.0)
    esito("DEVE PASSARE: ST-P il periodo di un sin di periodo %g piu' rumore, entro il passo del periodogramma" % P0, P is not None and abs(P - P0) <= passo, "P %.3f passo %.3f" % (P or -1, passo or -1))
    # ------------------------------------------------------------ ST-B
    phi = 0.9
    n = 200000
    e = rng.normal(size=n)
    a = np.empty(n)
    a[0] = e[0]
    for i in range(1, n):
        a[i] = phi * a[i - 1] + e[i]
    tb, _M = tau_int(a)
    teo = (1 + phi) / (2 * (1 - phi))
    esito("DEVE PASSARE: ST-B tau_int di Sokal su un AR(1) phi %g: il teorico %.2f entro un fattore %g" % (phi, teo, FATTORE_B), teo / FATTORE_B <= tb <= teo * FATTORE_B, "%.3f (M %d)" % (tb, _M))
    # ------------------------------------------------------------ ST-I
    g = np.linspace(-20, 20, 161)
    X, Y = np.meshgrid(g, g)
    rho = np.exp(-(X / 6.0) ** 2 / 2 - (Y / 3.0) ** 2 / 2)
    al = allungamento(rho.ravel(), X.ravel(), Y.ravel())
    esito("DEVE PASSARE: ST-I l'allungamento di un'ellisse gaussiana di rapporto 2 entro %g" % TOLL_I, abs(al - 2.0) <= 2.0 * TOLL_I, "%.4f" % al)
    # ------------------------------------------------------------ ST-S, ST-F
    print("### ST-S (STAMPA, non un DEVE): dove il criterio avrebbe fermato")
    for nome in ("S162", "TB3", "TBS"):
        if not CA.nomi(nome):
            print("  %s: nessun jsonl" % nome)
            continue
        t, ser = serie_singolo(nome, s)
        d = ser["spostamento"]
        P, passo = periodo(t, d, T_PERIODO[0], T_PERIODO[1])
        W = 3.0 * P if P else W_RIPIEGO
        stampa_lettura(nome, t, ser, W, P, passo)
    # ------------------------------------------------------------ la VITA (s3), il periodo di TB3 (Luca 18:08)
    print("### (s3) IL RITMO DI PERDITA E LA VITA (una ESTRAPOLAZIONE: la massa dentro il bordo diviso il ritmo di M_ass nell'ultima finestra)")
    for nome, (tv, Ma, Md) in sorted(VITA.items()):
        sel = tv >= tv[-1] - 6000.0
        r_, re_ = pendenza(tv[sel], Ma[sel])
        print("  %-8s dM_ass/dt nell'ultima finestra di 6000: %.4e +- %.1e; M dentro %.4e; la vita estrapolata %s" % (nome, r_, re_, Md[-1], "%.3e unita'" % (Md[-1] / r_) if r_ > 0 else "-"))
    print("### IL PERIODO DI TB3 (Luca 18:08: il sospetto che 1500 sia il passo dei controlli; mio: o la lunghezza di un pezzo)")
    if CA.nomi("TB3"):
        t3, s3 = serie_singolo("TB3", s)
        d3 = s3["spostamento"]
        for passo in PASSI_PERIODO:
            k = int(round(passo / 10))
            P_, ps_ = periodo(t3[::k], d3[::k], T_PERIODO[0], T_PERIODO[1])
            print("  il campionamento a %d tick: P %s" % (passo, "%.1f (passo %.1f)" % (P_, ps_) if P_ else "non stimato"))
        Tp = TICK_PEZZO * s
        pot, n_p = None, 0
        for a0 in np.arange(0.0, t3[-1], Tp):
            sel = (t3 >= a0 + 50.0) & (t3 < a0 + Tp - 50.0)
            if sel.sum() < 64:
                continue
            xx = d3[sel] - np.polyval(np.polyfit(t3[sel], d3[sel], 1), t3[sel])
            nn = 1 << int(np.floor(np.log2(sel.sum())))
            pw = np.abs(np.fft.rfft(xx[:nn])) ** 2
            pot = pw if pot is None else pot[:len(pw)] + pw[:len(pot)]
            n_p += 1
        if pot is not None:
            fr = np.fft.rfftfreq((len(pot) - 1) * 2, float(np.median(np.diff(t3))))
            kk = int(np.argmax(pot[1:])) + 1
            print("  DENTRO I PEZZI (le serie spezzate alle riprese, %d pezzi, la potenza mediata): il picco a P %.1f" % (n_p, 1.0 / fr[kk]))
    # ------------------------------------------------------------ ST-F su casi COSTRUITI (Luca 18:08 e 18:42)
    print("### ST-F SU CASI COSTRUITI (Luca 18:42): una deriva COSTANTE piu' l'AR(1) DEVE dare il regime e la pendenza ritrovata; una deriva che ACCELERA DEVE dare non ancora")
    ts = np.arange(0.0, 30000.0, 1.5)
    rg = np.random.default_rng(11)
    e = rg.normal(size=len(ts))
    ar = np.empty(len(ts))
    ar[0] = e[0]
    for i_ in range(1, len(ts)):
        ar[i_] = 0.9 * ar[i_ - 1] + e[i_]
    base = ar + 2.0 * np.sin(2 * math.pi * ts / 700.0)
    deriva = 5e-4
    W = 3 * 700.0
    t_c = np.arange(PASSO_CONTROLLI, ts[-1] + 1e-9, PASSO_CONTROLLI)
    costante = base + deriva * ts
    accelera = base + deriva * ts * (ts / 10000.0)          # ### la pendenza cresce: deriva x 2 t / 10000
    tx_c, _r = lettura(ts, {"x": costante}, W, t_c)
    tx_a, _r = lettura(ts, {"x": accelera}, W, t_c)
    pd, pde = pendenza(ts[ts >= T_RAMPA], costante[ts >= T_RAMPA])
    esito("DEVE PASSARE: ST-F-C la deriva COSTANTE di %g piu' l'AR(1) e un'oscillazione: il regime raggiunto" % deriva, tx_c is not None, "da t %s" % tx_c)
    esito("DEVE PASSARE: ST-F-P la pendenza misurata ritrova la deriva entro 2 volte il suo errore", abs(pd - deriva) <= 2 * pde, "%.4e +- %.1e" % (pd, pde))
    esito("DEVE FALLIRE: ST-F la deriva che ACCELERA risulta nel regime", tx_a is None, "da t %s" % tx_a)
    print("### TF3 + TF3C (stampa, come prima)")
    t1, s1 = serie_singolo("TF3", s)
    t2, s2 = serie_singolo("TF3C", s)
    t = np.concatenate([t1, t2[t2 > t1[-1]]])
    ser = {k: np.concatenate([s1[k], s2[k][t2 > t1[-1]]]) for k in s1}
    P, passo = periodo(t, ser["spostamento"], T_PERIODO[0], T_PERIODO[1])
    stampa_lettura("TF3+TF3C", t, ser, 3.0 * P if P else W_RIPIEGO, P, passo)
    print("=" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main())
