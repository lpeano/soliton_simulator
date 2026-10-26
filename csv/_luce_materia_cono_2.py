# -*- coding: utf-8 -*-
r"""**C2 CORRETTA: LA LUCE E LA MATERIA ATTORNO A UN CONO** *(la parte 1 del mandato del 2026-10-26; [[LUCE-MATERIA-CONO]], [[PROGETTO-MITOSI]], [[LORENTZ-MATERIA-INTERFERENZA]])*: ### **le due
correzioni di `f94e45e9`: il disco dalla regola del mandato** *(il bordo a `3 L_tot` dalla sorgente)* ### **e la finestra d'uscita in una carta continua** *(sul piatto `4, 5, 0, 1`; sul cono `0, 1`)*.

> ### ⛔ **Il task history e' `2026-10-26_c2_corretta.md`.** ### **Strumenti in memoria; nessun file del nucleo.**
> ### **Importato, non copiato:** `_luce_materia_cono` *(`Disco`, `CampoGrafo`, `luce_iniziale`, `materia_iniziale`, `controlli`)*. ### **Riscritti in forma VETTORIALE, per la taglia:** ### **il generatore sparso
> e la distanza dal bordo** *(il controllo `0` li confronta AL BIT con quelli vecchi)*; ### **le corse, con l'insieme dei settori d'uscita come PARAMETRO** *(le stesse operazioni di quelle vecchie)*.

Gira con:  python csv/_luce_materia_cono_2.py > doc/referti_l2/luce_materia_cono_2.txt
"""
import io
import json
import math
import os
import sys
import time

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
_PO = os.path.join(RADICE, "primo_ordine")
for _p in (_QUI, _PO, os.path.join(_PO, "leggi")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import numpy as np                                             # noqa: E402

X0 = -55.0
BB = (24.0, 32.0, 40.0)
B_CONV = 32.0
W_LUCE = (6.0, 9.0)
Q_MAT = 0.7
W_MAT = (8.0, 11.0)
L_USCITA = 30.0
DT_MAT = 10.0
T_MAX_MAT = 6000.0
T_MAX_LUCE = 20000
R_CONTROLLO = 40
FATTORE_BORDO = 3.0
USCITA = {6: (4, 5, 0, 1), 5: (0, 1)}
INGRESSO = (2, 3)
TOLL_BANDA = 1e-10
TOLL_PI3 = 0.05
TOLL_EP = 0.05
TOLL_CHIAVE = 0.10
JSONL = os.path.join(RADICE, "doc", "referti_l2", "luce_materia_cono_2.jsonl")
OK = [0, 0]
FALLITE = []


def esito(che, passa, nota="", deve=True):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    if deve and not passa:
        FALLITE.append(che)
    print("  %-110s %s   %s" % (che[:110], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return passa


def scrivi(r):
    with io.open(JSONL, "a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n")


def raggio():
    """### Il lato `R` dalla regola: `L_tot = |x0| + 2 b_max/sqrt3 + 3 W + L_USCITA`; l'inraggio `>= |sorgente| + 3 L_tot`."""
    L_tot = abs(X0) + 2.0 * max(BB) / math.sqrt(3.0) + 3.0 * max(W_MAT[0], W_LUCE[0]) + L_USCITA
    src = math.hypot(X0, max(BB))
    R_in = src + FATTORE_BORDO * L_tot
    return int(math.ceil(R_in / (math.sqrt(3.0) / 2.0))), L_tot, src, R_in


# =====================================================================================
#   LA TAGLIA: il generatore sparso e la distanza dal bordo, VETTORIALI
# =====================================================================================
def nodo_estremita(ii, jj):
    h = np.empty(2 * len(ii), dtype=np.int64)
    h[0::2] = ii
    h[1::2] = jj
    return h


def H_sparso_v(ii, jj, nn):
    """### `H = I - P_u + P_-`, ### **le stesse voci nello STESSO ordine di `_luce_materia_cono.H_sparso`** *(cosi' la somma dei duplicati e' la stessa, al bit)*."""
    import scipy.sparse as sp
    m = len(ii)
    nh = nodo_estremita(ii, jj)
    E = np.argsort(nh, kind="stable")
    d = np.bincount(nh, minlength=nn)
    off = np.concatenate([[0], np.cumsum(d)[:-1]])
    d2 = d * d
    tot = int(d2.sum())
    v_of = np.repeat(np.arange(nn), d2)
    start = np.repeat(np.concatenate([[0], np.cumsum(d2)[:-1]]), d2)
    p = np.arange(tot) - start
    dv = d[v_of]
    a = E[off[v_of] + p // dv]
    b = E[off[v_of] + p % dv]
    val = -1.0 / dv.astype(float)
    k = np.arange(m)
    ra = np.stack([2 * k, 2 * k + 1, 2 * k, 2 * k + 1], axis=1).ravel()
    ca = np.stack([2 * k, 2 * k + 1, 2 * k + 1, 2 * k], axis=1).ravel()
    va = np.tile([0.5, 0.5, -0.5, -0.5], m)
    r = np.concatenate([np.arange(2 * m), a, ra])
    c = np.concatenate([np.arange(2 * m), b, ca])
    v = np.concatenate([np.ones(2 * m), val, va])
    return sp.csr_matrix((v, (r, c)), shape=(2 * m, 2 * m))


def dist_bordo_v(D):
    """### La distanza di grafo dal bordo *(BFS da tutti i nodi di bordo, `scipy.sparse.csgraph`)*."""
    import scipy.sparse as sp
    import scipy.sparse.csgraph as cg
    nn = D.nn
    bo = np.where(D.bordo)[0]
    r = np.concatenate([D.ii, D.jj, np.full(len(bo), nn)])
    c = np.concatenate([D.jj, D.ii, bo])
    A = sp.csr_matrix((np.ones(len(r)), (r, c)), shape=(nn + 1, nn + 1))
    A = A + A.T
    dd = cg.shortest_path(A, method="D", unweighted=True, indices=nn)
    return (dd[:nn] - 1).astype(int)


# =====================================================================================
#   LE CORSE, con i settori d'uscita come parametro
# =====================================================================================
def finestre(t, xy, peso_in, peso_out):
    import _luce_materia_cono as C
    PC = C.PERC_FINESTRA
    t, xy = np.asarray(t), np.asarray(xy)
    fin = np.asarray(peso_in) >= PC
    fout = (np.asarray(peso_out) >= PC) & (xy[:, 0] > 0.0)
    out = {"punti_in": int(fin.sum()), "punti_out": int(fout.sum())}
    if fin.sum() < 3 or fout.sum() < 3:
        out.update(theta_in=None, theta_out=None, delta=None)
        return out
    vin = np.polyfit(t[fin], xy[fin], 1)[0]
    vout = np.polyfit(t[fout], xy[fout], 1)[0]
    th_in, th_out = math.atan2(vin[1], vin[0]), math.atan2(vout[1], vout[0])
    out.update(theta_in=th_in, theta_out=th_out, delta=th_out - th_in, v_in=float(np.hypot(*vin)), v_out=float(np.hypot(*vout)))
    return out


def corsa_luce(D, db, b_y, W, uscita):
    import _luce_materia_cono as C
    campo = C.CampoGrafo(D.P, D.S, len(D.ii), np.full(len(D.ii), C.S_LUCE))
    C.luce_iniziale(D, campo, W, b_y)
    vicino_arco = (db[D.ii] <= C.D_BORDO) | (db[D.jj] <= C.D_BORDO)
    vicino_tri = vicino_arco[D.P].any(axis=1)
    ia, it = np.isin(D.sett_arco, INGRESSO), np.isin(D.sett_tri, INGRESSO)
    oa, ot = np.isin(D.sett_arco, uscita), np.isin(D.sett_tri, uscita)
    tt, xy, pin, pout, larg, guardia = [], [], [], [], [], 0.0
    H0 = float(campo.energia_arco().sum() + campo.energia_tri().sum())
    t, inizio, x0u, fermata = 0, None, None, "tempo"
    while True:
        ea, et = campo.energia_arco(), campo.energia_tri()
        tot = float(ea.sum() + et.sum())
        g = float((ea[vicino_arco].sum() + et[vicino_tri].sum()) / tot)
        guardia = max(guardia, g)
        c = (ea @ D.pos_arco + et @ D.pos_tri) / tot
        s_in = float((ea[ia].sum() + et[it].sum()) / tot)
        s_out = float((ea[oa].sum() + et[ot].sum()) / tot)
        tt.append(t * C.S_LUCE)
        xy.append(c)
        pin.append(s_in)
        pout.append(s_out)
        if s_out >= C.PERC_FINESTRA and c[0] > 0.0:
            d2 = (ea @ np.sum((D.pos_arco - c) ** 2, axis=1) + et @ np.sum((D.pos_tri - c) ** 2, axis=1)) / tot
            larg.append(math.sqrt(d2))
            if inizio is None:
                inizio, x0u = t, c
            elif np.linalg.norm(c - x0u) >= L_USCITA:
                fermata = "uscita"
                break
        if g > C.GUARDIA_BORDO:
            fermata = "bordo"
            break
        if t > T_MAX_LUCE:
            break
        campo.tick()
        t += 1
    r = finestre(tt, xy, pin, pout)
    r.update(tick=t, guardia=guardia, deriva_energia=(tot - H0) / H0, fermata=fermata, larghezza_uscita=float(np.mean(larg)) if larg else None)
    return r


def corsa_materia(D, db, A, nodo_h, b_y, W, uscita):
    import scipy.sparse.linalg as sla
    import _luce_materia_cono as C
    x, fuori = C.materia_iniziale(D, W, b_y)
    pos_h = D.pos[nodo_h]
    sett_h = D.sett[nodo_h]
    vicino = db[nodo_h] <= C.D_BORDO
    mi, mo = np.isin(sett_h, INGRESSO), np.isin(sett_h, uscita)
    tt, xy, pin, pout, larg, guardia = [], [], [], [], [], 0.0
    t, inizio, x0u, fermata = 0.0, None, None, "tempo"
    n0 = float(np.vdot(x, x).real)
    while True:
        w = np.abs(x) ** 2
        tot = float(w.sum())
        g = float(w[vicino].sum() / tot)
        guardia = max(guardia, g)
        c = (w @ pos_h) / tot
        s_in, s_out = float(w[mi].sum() / tot), float(w[mo].sum() / tot)
        tt.append(t)
        xy.append(c)
        pin.append(s_in)
        pout.append(s_out)
        if s_out >= C.PERC_FINESTRA and c[0] > 0.0:
            larg.append(math.sqrt(float(w @ np.sum((pos_h - c) ** 2, axis=1)) / tot))
            if inizio is None:
                inizio, x0u = t, c
            elif np.linalg.norm(c - x0u) >= L_USCITA:
                fermata = "uscita"
                break
        if g > C.GUARDIA_BORDO:
            fermata = "bordo"
            break
        if t >= T_MAX_MAT:
            break
        x = sla.expm_multiply(DT_MAT * A, x)
        t += DT_MAT
    r = finestre(tt, xy, pin, pout)
    r.update(tempo=t, guardia=guardia, norma=abs(tot - n0) / n0, fuori_banda=fuori, fermata=fermata, larghezza_uscita=float(np.mean(larg)) if larg else None)
    return r


def main(argv):
    del argv
    import _presidio
    import _universalita_massa as UM
    import _u1_prototipo as U
    import composizione as CM
    import scipy.sparse as sp
    import _luce_materia_cono as C
    _presidio.avvia(__file__)
    C.X0, C.Q_MAT = X0, Q_MAT
    R, L_tot, src, R_in = raggio()
    print("=" * 130)
    print("C2 CORRETTA: LA LUCE E LA MATERIA ATTORNO A UN CONO -- il disco dalla regola del mandato, la finestra d'uscita in una carta continua")
    print("=" * 130)
    blobs = {p: UM.blob(p) for p in ("soliton_simulator.py", "csv/_luce_materia_cono_2.py", "csv/_luce_materia_cono.py", "csv/_u1_prototipo.py", "csv/_u1_terzo.py", "csv/_massa_nei_difetti.py")}
    print("  il passo: %d pezzi, impronta %s (intatto); i blob nel repo: %s" % (len(CM.ORDINE), CM.IMPRONTA, "; ".join("%s %s" % (k, v["sha1-BYTE"]) for k, v in blobs.items())))
    print("  la configurazione: X0 %g BB %s B_CONV %g W_LUCE %s Q_MAT %g W_MAT %s L_USCITA %g DT_MAT %g T_MAX_MAT %g T_MAX_LUCE %d FATTORE_BORDO %g USCITA %s INGRESSO %s; da _luce_materia_cono: S_LUCE %g L_TORO %d N_K0 %d D_COPIA %g PERC_FINESTRA %g D_BORDO %d GUARDIA_BORDO %g"
          % (X0, BB, B_CONV, W_LUCE, Q_MAT, W_MAT, L_USCITA, DT_MAT, T_MAX_MAT, T_MAX_LUCE, FATTORE_BORDO, USCITA, INGRESSO, C.S_LUCE, C.L_TORO, C.N_K0, C.D_COPIA, C.PERC_FINESTRA, C.D_BORDO, C.GUARDIA_BORDO))
    print("  IL RAGGIO DALLA REGOLA: L_tot %.4f, la sorgente a %.4f, l'inraggio >= %.4f: R = %d" % (L_tot, src, R_in, R))
    print("-" * 130)
    io.open(JSONL, "w", encoding="utf-8").close()
    scrivi({"tipo": "testata", "blobs": blobs, "impronta": CM.IMPRONTA, "R": R, "L_tot": L_tot, "R_in": R_in})
    C.BL_LUCE.append(U.blocchi_campo(C.S_LUCE)[0])
    # ### il controllo 0
    dc, dg = C.controlli()
    esito("DEVE PASSARE (0): il campo su grafo e il generatore sparso vecchi contro i loro riferimenti (i controlli di _luce_materia_cono)", dc <= C.TOLL_CAMPO and dg <= C.TOLL_GEN, "%.1e %.1e" % (dc, dg))
    for n in (6, 5):
        Dp = C.Disco(n, R_CONTROLLO)
        h_old, h_new = C.H_sparso(Dp.ii, Dp.jj, Dp.nn), H_sparso_v(Dp.ii, Dp.jj, Dp.nn)
        bit = (h_old.indptr.tobytes() == h_new.indptr.tobytes() and h_old.indices.tobytes() == h_new.indices.tobytes() and h_old.data.tobytes() == h_new.data.tobytes())
        db_bit = np.array_equal(Dp.dist_bordo(), dist_bordo_v(Dp))
        esito("DEVE PASSARE (0): il disco %d di lato %d: il generatore sparso vettoriale = il vecchio AL BIT, e la distanza dal bordo uguale" % (n, R_CONTROLLO), bit and db_bit, "H %s, distanze %s" % (bit, db_bit))
    dischi = {}
    for n in (6, 5):
        t0 = time.time()
        D = C.Disco(n, R)
        g = D.gradi()
        interni = ~D.bordo
        interni[0] = False
        due = np.bincount(D.P.ravel(), minlength=len(D.ii))
        ba = D.bordo[D.ii] & D.bordo[D.jj]
        ok = g[0] == n and bool(np.all(g[interni] == 6)) and bool(np.all(due[~ba] == 2)) and bool(np.all(due[ba] == 1))
        db = dist_bordo_v(D)
        nh = nodo_estremita(D.ii, D.jj)
        Hs = H_sparso_v(D.ii, D.jj, D.nn)
        A = (-1j) * (Hs - sp.identity(Hs.shape[0], format="csr"))
        del Hs
        esito("DEVE PASSARE (0): il disco a %d settori di lato %d: il centro a %d, l'interno a 6, ogni arco interno in due triangoli" % (n, R, n), ok,
              "nodi %d, archi %d, triangoli %d (%.0f s)" % (D.nn, len(D.ii), len(D.P), time.time() - t0))
        scrivi({"tipo": "disco", "settori": n, "R": R, "nodi": int(D.nn), "archi": int(len(D.ii)), "triangoli": int(len(D.P))})
        dischi[n] = (D, db, A, nh)
    ris = []
    casi = [(n, "luce", b, W_LUCE[0]) for n in (6, 5) for b in BB] + [(5, "luce", B_CONV, W_LUCE[1])]
    casi += [(n, "materia", b, W_MAT[0]) for n in (6, 5) for b in BB] + [(5, "materia", B_CONV, W_MAT[1])]
    for n, chi, b, W in casi:
        D, db, A, nh = dischi[n]
        coppia = {}
        for lato in (+1, -1):
            t0 = time.time()
            r = corsa_luce(D, db, lato * b, W, USCITA[n]) if chi == "luce" else corsa_materia(D, db, A, nh, lato * b, W, USCITA[n])
            r.update(disco=n, chi=chi, b=b, lato=lato, W=W, secondi=time.time() - t0)
            coppia[lato] = r
            scrivi(dict(r, tipo="corsa"))
            print("  %-7s disco %d b %4g W %4g lato %+d: theta_in %s theta_out %s delta %s (punti %d/%d; fermata %s; guardia %.1e; larghezza all'uscita %s; %.0f s)"
                  % (chi, n, b, W, lato, "%+.5f" % r["theta_in"] if r["theta_in"] is not None else "-", "%+.5f" % r["theta_out"] if r["theta_out"] is not None else "-",
                     "%+.5f" % r["delta"] if r["delta"] is not None else "-", r["punti_in"], r["punti_out"], r["fermata"], r["guardia"],
                     "%.2f" % r["larghezza_uscita"] if r["larghezza_uscita"] is not None else "-", r["secondi"]))
            sys.stdout.flush()
        conv = (coppia[-1]["delta"] - coppia[+1]["delta"]) if coppia[-1]["delta"] is not None and coppia[+1]["delta"] is not None else None
        ris.append({"disco": n, "chi": chi, "b": b, "W": W, "sopra": coppia[+1], "sotto": coppia[-1], "convergenza": conv})
        scrivi({"tipo": "convergenza", "disco": n, "chi": chi, "b": b, "W": W, "convergenza": conv})
        print("  ### %s disco %d b %g W %g: LA CONVERGENZA %s (pi/3 = %.5f)" % (chi, n, b, W, "%+.5f" % conv if conv is not None else "-", math.pi / 3))
    print("-" * 130)
    print("### I CRITERI")

    def trova(n, chi, b, W):
        return [r for r in ris if r["disco"] == n and r["chi"] == chi and r["b"] == b and r["W"] == W][0]
    fb = max(r[l]["fuori_banda"] for r in ris if r["chi"] == "materia" for l in ("sopra", "sotto"))
    esito("DEVE PASSARE (0): il pacchetto di materia nella banda alta entro %g" % TOLL_BANDA, fb <= TOLL_BANDA, "%.1e" % fb)
    kL = 2 * np.pi * C.N_K0 / C.L_TORO
    ok1, nota1 = True, []
    for chi, k, W in (("luce", kL, W_LUCE[0]), ("materia", Q_MAT, W_MAT[0])):
        tol = 0.1 / (k * W)
        for b in BB:
            r = trova(6, chi, b, W)
            for lato in ("sopra", "sotto"):
                d = r[lato]["delta"]
                ok1 &= d is not None and abs(d) <= tol
                nota1.append("%s %g %s %s" % (chi[0], b, lato[:2], "%+.4f" % d if d is not None else "-"))
    esito("DEVE PASSARE (1): sul PIATTO |delta| <= 0.1/(|k| W) per i due fasci, la luce e la materia, a ogni b", ok1, "; ".join(nota1))
    cl = [trova(5, "luce", b, W_LUCE[0])["convergenza"] for b in BB]
    ok2 = all(c is not None and abs(c - math.pi / 3) / (math.pi / 3) <= TOLL_PI3 for c in cl) and cl[0] is not None and cl[-1] is not None and abs(cl[0] / cl[-1] - 1) <= TOLL_CHIAVE
    esito("DEVE PASSARE (2): la LUCE sul cono: pi/3 entro il %g%% a ogni b, e b %g/b %g entro il %g%% da 1" % (100 * TOLL_PI3, BB[0], BB[-1], 100 * TOLL_CHIAVE), ok2,
          " ".join("%+.5f" % c if c is not None else "-" for c in cl))
    cm = [trova(5, "materia", b, W_MAT[0])["convergenza"] for b in BB]
    ok3 = all(c is not None and abs(c - math.pi / 3) / (math.pi / 3) <= TOLL_PI3 for c in cm)
    esito("PUO' FALLIRE (3): la MATERIA sul cono: pi/3 entro il %g%% a ogni b" % (100 * TOLL_PI3), ok3, " ".join("%+.5f" % c if c is not None else "-" for c in cm), deve=False)
    ok4 = all(a is not None and c is not None and abs(a / c - 1) <= TOLL_EP for a, c in zip(cm, cl))
    esito("PUO' FALLIRE (4): il rapporto materia/luce entro %g da 1 a ogni b" % TOLL_EP, ok4,
          " ".join("%.4f" % (a / c) if a is not None and c is not None else "-" for a, c in zip(cm, cl)), deve=False)
    ch = cm[0] / cm[-1] if cm[0] is not None and cm[-1] is not None and cm[-1] != 0 else None
    esito("DEVE FALLIRE, PER LA CHIAVE GIUSTA (5): la materia va come 1/b; la chiave: conv(b %g)/conv(b %g) entro il %g%% da 1, non %g" % (BB[0], BB[-1], 100 * TOLL_CHIAVE, BB[-1] / BB[0]),
          ch is not None and abs(ch - 1) <= TOLL_CHIAVE, "%.4f" % ch if ch is not None else "-")
    print("### LA CONVERGENZA IN LARGHEZZA (b %g, il cono)" % B_CONV)
    for chi, Ws in (("luce", W_LUCE), ("materia", W_MAT)):
        v = [trova(5, chi, B_CONV, W)["convergenza"] for W in Ws]
        print("  %s: W %s -> %s" % (chi, Ws, " ".join("%+.5f" % x if x is not None else "-" for x in v)))
        scrivi({"tipo": "larghezza", "chi": chi, "W": list(Ws), "convergenza": v})
    print("### LA DIFFRAZIONE: la larghezza quadratica media all'uscita contro b (il cono, il fascio sotto)")
    for chi, W in (("luce", W_LUCE[0]), ("materia", W_MAT[0])):
        print("  %s: %s" % (chi, " ".join("b %g: %s" % (b, "%.2f" % trova(5, chi, b, W)["sotto"]["larghezza_uscita"] if trova(5, chi, b, W)["sotto"]["larghezza_uscita"] is not None else "-") for b in BB)))
    print("-" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    scrivi({"tipo": "esito", "passano": OK[0], "totale": OK[1], "deve_fallite": FALLITE})
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
