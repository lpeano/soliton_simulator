# -*- coding: utf-8 -*-
r"""**LA FRECCIA DI `F0`: UNA SCELTA DEL VUOTO O UNA LEGGE?** *(Luca `2026-11-02` `19:21`, la parte `1`; il task history `doc/TASK_HISTORY/2026-11-02_freccia_F0.md`)*:
### **un controllo sulla carta, sulla scena di BG-F-0.15** *(`L 81`, il vuoto `fondo_uniforme`)*.
    python csv/solitone/freccia_F0.py > doc/referti_l2/freccia_F0.txt
### **(f1)** le fasi per direzione di `F0`-`F3` *(`_solitone_dal_fondo.FASI`)*, lette dal campo; ### **(f2)** `F0` ruotato di `60` .. `300` gradi e allo specchio lungo `A1 + A2`:
uguale a meno di una fase globale a uno dei quattro?; ### **(f3)** l'energia del vuoto *(`_vuoto_sul_fondo.energia`)*; ### **(f4)** la freccia per nodo
*(`sum phi u` sulle estremita' del nodo, `u` il versore verso l'altro capo: la definizione dichiarata nel task history)*; ### **(f5)** il tick del vuoto
*(`vuoto.tick_vuoto`)* commuta con le rotazioni? *(il controllo MIO, dichiarato: non entra nelle letture (v1)-(v3))*.
### **Le rotazioni sugli indici:** `R60 (m1, m2) -> (m1 - m2, m1)` *(`A1 -> A1 + A2`, `A2 -> -A1`)*; lo specchio `(m1, m2) -> (m2, m1)` *(scambia `A1` e `A2`)*.
"""
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))
import solitone  # noqa: E402,F401  (i percorsi)

TOLL_UGUALE = 1e-12            # ### (f2): |R F0 - c F_k| / |F_k| e ||c| - 1| (il task history, sez. 2)
TOLL_TICK = 1e-12              # ### (f5): |tick(R F0) - R tick(F0)| / |tick(F0)| (il task history, sez. 1)

OK = [0, 0]
FALLITE = []


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    if not passa:
        FALLITE.append(che)
    print("  %-120s %s   %s" % (che[:120], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return passa


def struttura(inc, L, dirs):
    """### **Per ogni arco** `a` *(capi `i = nodo[2a]`, `j = nodo[2a+1]`)*: la direzione positiva `k` in `dirs`, l'estremita' alla CODA e alla TESTA, il versore da `i` a `j`;
    ### **e la chiave** `(nodo, altro capo) -> estremita'`."""
    from solitone import toro as TO
    A1, A2 = TO.vettori()
    v = np.arange(inc.n)
    m1, m2 = v // L, v % L
    kk, coda, testa, u, chiave = [], [], [], [], {}
    for a in range(inc.m):
        i, j = int(inc.nodo[2 * a]), int(inc.nodo[2 * a + 1])
        d = ((int(m1[j] - m1[i]) + L // 2) % L - L // 2, (int(m2[j] - m2[i]) + L // 2) % L - L // 2)
        pos = d if (d[0] > 0 or (d[0] == 0 and d[1] > 0)) else (-d[0], -d[1])
        kk.append(dirs.index(pos))
        coda.append(2 * a if pos == d else 2 * a + 1)
        testa.append(2 * a + 1 if pos == d else 2 * a)
        u.append(d[0] * A1 + d[1] * A2)
        assert (i, j) not in chiave and (j, i) not in chiave, "due archi fra gli stessi nodi"
        chiave[(i, j)], chiave[(j, i)] = 2 * a, 2 * a + 1
    return np.array(kk), np.array(coda), np.array(testa), np.array(u), chiave


def mappa(L, quale):
    """### **La mappa dei nodi** `v -> R v` *(`quale` = `"R60"` o `"S"`)*."""
    v = np.arange(L * L)
    m1, m2 = v // L, v % L
    if quale == "R60":
        return ((m1 - m2) % L) * L + m1 % L
    return m2 * L + m1


def ruota(phi, inc, chiave, R):
    """### **Il campo trasportato:** `phi'[estremita' (R i, R j)] = phi[estremita' (i, j)]`."""
    out = np.empty_like(phi)
    for a in range(inc.m):
        i, j = int(inc.nodo[2 * a]), int(inc.nodo[2 * a + 1])
        out[chiave[(int(R[i]), int(R[j]))]] = phi[2 * a]
        out[chiave[(int(R[j]), int(R[i]))]] = phi[2 * a + 1]
    return out


def fasi_lette(phi, kk, coda, testa, ndir):
    """### **Il valore alla coda per direzione** *(e se e' COSTANTE, con la testa opposta)*: `(valori, costante)`."""
    val, cost = [], True
    for k in range(ndir):
        c, t = phi[coda[kk == k]], phi[testa[kk == k]]
        val.append(complex(c[0]))
        cost = cost and bool(np.all(c == c[0])) and bool(np.all(t == -c[0]))
    return val, cost


def uguale(x, y):
    """### **`x = c y` a meno di una fase globale?** `(uguale, c, scarto)`."""
    c = complex(np.vdot(y, x) / np.vdot(y, y))
    sc = float(np.linalg.norm(x - c * y) / np.linalg.norm(y))
    return sc <= TOLL_UGUALE and abs(abs(c) - 1.0) <= TOLL_UGUALE, c, sc


def freccia(phi, inc, u):
    """### **`a(v) = sum phi u`** sulle estremita' del nodo `v` *(un vettore complesso)*: `(n, 2)`."""
    a = np.zeros((inc.n, 2), dtype=complex)
    np.add.at(a, inc.nodo[0::2], phi[0::2, None] * u)
    np.add.at(a, inc.nodo[1::2], phi[1::2, None] * (-u))
    return a


def leggi_freccia(a):
    """### **Tolta la fase globale** *(quella che rende `a . a` reale positivo)*: il modulo, l'angolo, la parte immaginaria che resta; e se e' uguale su ogni nodo."""
    a0 = a[0]
    f = np.exp(-0.5j * np.angle(a0[0] ** 2 + a0[1] ** 2))
    r, im = (f * a0).real, (f * a0).imag
    uni = float(np.max(np.abs(a - a0)))
    return float(np.hypot(*r)), math.degrees(math.atan2(r[1], r[0])), float(np.hypot(*im)), uni


def main(argv):
    del argv
    import _presidio
    import _solitone_dal_fondo as SD
    import _vuoto_sul_fondo as VSF
    import _vuoto_vivo_B as V
    import scena_l2 as SL
    from solitone import vuoto as VU
    for m in ("__init__", "toro", "vuoto"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(__file__)
    s = V.CORSE["BG-F-0.15"][2]
    print("=" * 130)
    print("LA FRECCIA DI F0 (Luca 19:21, la parte 1): la scena di BG-F-0.15 (s %g, L %d, eps %g), il vuoto fondo_uniforme (VUOTO_PER_ESTREMITA %g)" % (s, V.L, V.EPS, SL.VUOTO_PER_ESTREMITA))
    print("  la configurazione: TOLL_UGUALE %g TOLL_TICK %g; FASI %s; DIREZIONI %s" % (TOLL_UGUALE, TOLL_TICK, [(n, tuple(round(x, 6) for x in f)) for n, f in SD.FASI], SD.DIREZIONI))
    print("  le letture di Luca, scritte prima: (v1) i quattro sono F0 con la freccia ruotata, alla stessa energia: una SCELTA del vuoto; (v2) qualche rotazione di F0")
    print("  fuori dalla famiglia o con energia diversa: la freccia e' nelle LEGGI; (v3) altro. ### (f3) e' un FALSO-UNO dichiarato prima: ogni flusso costante ha la stessa energia")
    print("=" * 130)
    with V.scena(s, "fondo", V.EPS) as (_rec, z, _phi0, _pK):
        inc, L = z["inc"], z["L"]
        dirs = list(SD.DIREZIONI)
        kk, coda, testa, u, chiave = struttura(inc, L, dirs)
        vuoti = {n: SD.fondo_con_fasi(inc, L, f) * SL.VUOTO_PER_ESTREMITA for n, f in SD.FASI}
        f0 = VSF.fondo_uniforme(inc, L, SL.VUOTO_PER_ESTREMITA)[0]
        esito("DEVE PASSARE: F-0 F0 = fondo_con_fasi((0,0,0)) = _vuoto_sul_fondo.fondo_uniforme AL BIT", vuoti["F0"].tobytes() == f0.tobytes())
        R60, S = mappa(L, "R60"), mappa(L, "S")
        rot = {}
        x = f0
        for k in range(1, 7):
            x = ruota(x, inc, chiave, R60)
            rot["R%d" % (60 * k)] = x
        sp = ruota(f0, inc, chiave, S)
        esito("DEVE PASSARE: F-R0 sei rotazioni di 60 gradi sono l'identita' AL BIT, e lo specchio due volte", rot["R360"].tobytes() == f0.tobytes()
              and ruota(sp, inc, chiave, S).tobytes() == f0.tobytes())
        rot = {k: v for k, v in rot.items() if k != "R360"}
        rot["S"] = sp
        cost = all(fasi_lette(v, kk, coda, testa, len(dirs))[1] for v in rot.values())
        esito("DEVE PASSARE: F-R1 ogni campo ruotato e' un flusso costante per direzione (coda c_d, testa -c_d)", cost)
        ug, _c, sc = uguale(vuoti["F0"], vuoti["F1"])
        esito("DEVE FALLIRE: F-R-F il confronto a meno di una fase dice F0 = F1", not ug, "scarto %.3e" % sc)
        # ------------------------------------------------------------------ (f1)
        print("-" * 130)
        print("### (f1) LE FASI PER DIREZIONE, LETTE DAL CAMPO (la coda; in gradi), e la freccia per nodo (f4)")
        print("  %-6s %-48s %-10s %-10s %-10s %-10s" % ("", "A2 (120) / A1 (0) / A1+A2 (60)", "|freccia|", "angolo", "|Im|", "non unif."))
        tutti = dict(vuoti)
        tutti.update({"F0 " + k: v for k, v in rot.items()})
        for n, phi in tutti.items():
            val, cst = fasi_lette(phi, kk, coda, testa, len(dirs))
            m, ang, im, uni = leggi_freccia(freccia(phi, inc, u))
            print("  %-8s %-48s %-10.6f %-10.3f %-10.3e %-10.3e%s" % (n, " / ".join("%+8.2f" % math.degrees(np.angle(c)) for c in val), m, ang, im, uni, "" if cst else "  ### NON costante"))
        # ------------------------------------------------------------------ (f2)
        print("-" * 130)
        print("### (f2) OGNI F0 RUOTATO CONTRO F0-F3, A MENO DI UNA FASE GLOBALE (uguale entro %g)" % TOLL_UGUALE)
        for n, phi in rot.items():
            righe = []
            for k, fk in vuoti.items():
                ok, c, sc = uguale(phi, fk)
                righe.append("%s %s (scarto %.2e, fase %+.1f)" % (k, "SI" if ok else "no", sc, math.degrees(np.angle(c))))
            print("  F0 %-5s %s" % (n, "; ".join(righe)))
        # ------------------------------------------------------------------ (f3)
        print("-" * 130)
        print("### (f3) L'ENERGIA DEL VUOTO (_vuoto_sul_fondo.energia, phi_h, psi = 0): tutto, nodo, arco")
        st = dict(z["st"])
        E = {}
        for n, phi in tutti.items():
            st["phi_h"] = phi
            E[n] = (VSF.energia(z["mot"], st, "phi_h", "tutto"), VSF.energia(z["mot"], st, "phi_h", "nodo"), VSF.energia(z["mot"], st, "phi_h", "arco"))
            print("  %-8s %+.15e  %+.15e  %+.15e" % (n, E[n][0], E[n][1], E[n][2]))
        e0 = E["F0"][0]
        print("  lo scarto relativo massimo da F0: %.3e" % max(abs(e[0] / e0 - 1.0) for e in E.values()))
        # ------------------------------------------------------------------ (f5)
        print("-" * 130)
        print("### (f5) IL TICK DEL VUOTO COMMUTA CON LE ROTAZIONI? (il controllo MIO, dichiarato; vuoto.tick_vuoto, il tick intero a psi = 0; entro %g)" % TOLL_TICK)
        T0 = VU.tick_vuoto(z, f0)
        nT = float(np.linalg.norm(T0))
        print("  F0 dopo un tick: |tick(F0) - F0| / |F0| = %.3e" % (float(np.linalg.norm(T0 - f0)) / float(np.linalg.norm(f0))))
        diff_f = []
        for n, phi in rot.items():
            Tn = VU.tick_vuoto(z, phi)
            if n == "S":
                RT = ruota(T0, inc, chiave, S)
            else:
                RT = T0
                for _k in range(int(n[1:]) // 60):
                    RT = ruota(RT, inc, chiave, R60)
            d = float(np.linalg.norm(Tn - RT)) / nT
            diff_f.append(float(np.linalg.norm(Tn - T0)) / nT)
            print("  F0 %-5s |tick(R F0) - R tick(F0)| / |tick(F0)| = %.3e   %s" % (n, d, "commuta" if d <= TOLL_TICK else "### NON commuta"))
        esito("DEVE FALLIRE: F5-F tick(R F0) uguale a tick(F0) non ruotato (entro %g), per ogni rotazione" % TOLL_TICK, not all(x <= TOLL_TICK for x in diff_f),
              "il minimo %.3e" % min(diff_f))
    print("=" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))


if __name__ == "__main__":
    main(sys.argv[1:])
