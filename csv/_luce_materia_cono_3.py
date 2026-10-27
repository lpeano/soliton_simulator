# -*- coding: utf-8 -*-
r"""**C2, LA MATERIA RIFATTA** *(la decisione di Luca del 2026-10-27, 01:17; [[LUCE-MATERIA-CONO]], [[PROGETTO-MITOSI]], [[LORENTZ-MATERIA-INTERFERENZA]])*: ### **la materia col segno del tempo CORRETTO**
*(`exp(+i (H - I) t)`)*, ### **`q 1.0`, `W 12`, il raggio dalla stessa regola, il tempo massimo dal percorso; l'angolo dall'IMPULSO MEDIO della parte uscita** *(il baricentro come controllo)*; ### **e la prova a vuoto della lettura dall'impulso sulla LUCE.**

> ### ⛔ **Il task history e' `2026-10-27_c2_materia.md`.** ### **Strumenti in memoria; nessun file del nucleo.**
> ### **Importati, non copiati:** `_luce_materia_cono` *(`Disco`, `CampoGrafo`, `luce_iniziale`, `materia_iniziale`, `reticolo`, `tipo_arco`, `PERC_FINESTRA`)*, `_luce_materia_cono_2` *(`H_sparso_v`, `dist_bordo_v`, `nodo_estremita`, `finestre`)*, `_u1_prototipo.blocchi_campo`.

Gira con:  python csv/_luce_materia_cono_3.py > doc/referti_l2/luce_materia_cono_3.txt
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
Q_MAT = 0.7                     # ### i parametri del mandato delle 08:57: la stima sotto un'ora per corsa (la correzione del guardiano delle 01:36)
W_MAT = 8.0
V_MAT = 0.1005                  # ### la velocita' di gruppo del generatore a q 0.7 lungo +x (0.10051)
W_LUCE = 6.0
L_USCITA = 30.0
DT_MAT = 10.0
FATTORE_T = 1.05                # ### il tempo massimo della materia: 1.05 x il percorso / v (il baricentro va a 0.0998, lo 0.7% sotto)
PEZZI = os.path.join(RADICE, "db_era2")   # ### i pezzi, uno per corsa: si riprende da quelli chiusi (db_era2/*.parziale e' ignorato da git)
FATTORE_BORDO = 3.0
USCITA = {6: (4, 5, 0, 1), 5: (0, 1)}
INGRESSO = (2, 3)
R_PROVA = 300                   # ### la prova a vuoto sulla luce: un cono di lato 300, b 32
B_PROVA = 32.0
TOLL_PROVA = 0.01
TOLL_PI3 = 0.05
TOLL_CHIAVE = 0.10
TOLL_BANDA = 1e-10
JSONL = os.path.join(RADICE, "doc", "referti_l2", "luce_materia_cono_3.jsonl")
OK = [0, 0]
FALLITE = []
A1 = np.array([1.0, 0.0])
A2 = np.array([-0.5, math.sqrt(3.0) / 2.0])
B_RET = np.array([A1, A2])


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
    L_tot = abs(X0) + 2.0 * max(BB) / math.sqrt(3.0) + 3.0 * W_MAT + L_USCITA
    src = math.hypot(X0, max(BB))
    R_in = src + FATTORE_BORDO * L_tot
    return int(math.ceil(R_in / (math.sqrt(3.0) / 2.0))), L_tot, src, R_in


def percorso(b):
    """### Il percorso del baricentro fino alla fine della finestra d'uscita *(la stessa forma di `L_tot`, al `b` della corsa)*."""
    return abs(X0) + 2.0 * b / math.sqrt(3.0) + 3.0 * W_MAT + L_USCITA


# =====================================================================================
#   LE MAPPE DELLA CARTA: lo slot e le coordinate di reticolo di ogni estremita' e di ogni arco
# =====================================================================================
def mappa(D):
    import _luce_materia_cono as C
    m = len(D.ii)
    slot = np.empty(2 * m, dtype=np.int8)
    mpos = np.empty((2 * m, 2), dtype=np.int64)
    tipo = np.empty(m, dtype=np.int8)
    mpart = np.empty((m, 2), dtype=np.int64)
    segno = np.empty(m, dtype=np.int8)
    for k in range(m):
        pu, pv = D.lat_arco[k]
        a, da, mm = C.tipo_arco(pu, pv)
        mu, mv = C.reticolo(pu), C.reticolo(pv)
        tipo[k], mpart[k], segno[k] = a, mm, (1 if da == 0 else -1)
        if da == 0:
            slot[2 * k], slot[2 * k + 1] = a, 3 + a
        else:
            slot[2 * k], slot[2 * k + 1] = 3 + a, a
        mpos[2 * k], mpos[2 * k + 1] = mu, mv
    return {"slot": slot, "mpos": mpos, "tipo": tipo, "mpart": mpart, "segno": segno}


def k_materia(x, mp, sel):
    """### L'impulso della materia sulle estremita' `sel`, ### **dalla TRASFORMATA per slot nelle coordinate di reticolo della carta:** ### **ogni frequenza va alla valle piu' vicina** *(`K` o `K'`)*,
    ### **`q = k - valle`;** ### **ritorna `q` medio sul peso TOTALE** *(la direzione di moto ha la stessa relazione con `q` nelle due valli)*, ### **il peso in `K` e in `K'`, e `q` di ciascuna.**"""
    w = np.abs(x) ** 2
    idx = np.where(sel & (w > 1e-12 * float(w[sel].max())))[0]
    mm = mp["mpos"][idx]
    lo = mm.min(axis=0)
    n = int(2 ** math.ceil(math.log2(max(mm.max(axis=0) - lo) + 1))) * 2
    P = np.zeros((n, n))
    for sl in range(6):
        s_ = idx[mp["slot"][idx] == sl]
        if not len(s_):
            continue
        z = np.zeros((n, n), dtype=complex)
        q = mp["mpos"][s_] - lo
        np.add.at(z, (q[:, 0], q[:, 1]), x[s_])
        # ### psi ~ e^{+i t.m}: fft2 mette il picco a +t
        P += np.abs(np.fft.fft2(z)) ** 2
    t1 = 2 * np.pi * np.fft.fftfreq(n)
    T1, T2 = np.meshgrid(t1, t1, indexing="ij")
    out = {}
    tot_q, tot_w = np.zeros(2), 0.0
    dK = []
    for nome, tv in (("K", (2 * np.pi / 3, 2 * np.pi / 3)), ("K'", (-2 * np.pi / 3, -2 * np.pi / 3))):
        d1 = (T1 - tv[0] + np.pi) % (2 * np.pi) - np.pi
        d2 = (T2 - tv[1] + np.pi) % (2 * np.pi) - np.pi
        qc = np.linalg.solve(B_RET, np.stack([d1.ravel(), d2.ravel()]))
        dK.append((nome, qc, np.hypot(qc[0], qc[1])))
    vicino_K = dK[0][2] <= dK[1][2]
    Pr = P.ravel()
    for nome, qc, _d in dK:
        m_ = vicino_K if nome == "K" else ~vicino_K
        ww = float(Pr[m_].sum())
        qq = np.array([float(Pr[m_] @ qc[0][m_]), float(Pr[m_] @ qc[1][m_])]) / ww if ww > 0 else np.zeros(2)
        out[nome] = {"peso": ww, "q": [float(qq[0]), float(qq[1])]}
        tot_q += qq * ww
        tot_w += ww
    q_tot = tot_q / tot_w
    out["frazione_K"] = out["K"]["peso"] / tot_w
    return q_tot, out


def k_luce(campo, D, mp, sel_arco, verso):
    """### L'impulso medio della luce sugli archi `sel_arco`: ### **la potenza della trasformata di `A` per tipo d'arco nelle coordinate di reticolo** *(col segno dell'orientazione)*, ### **nel semipiano `k . verso > 0`** *(il campo e' reale)*, ### **la media pesata attorno al picco.**"""
    a_ = np.abs(campo.A)
    idx = np.where(sel_arco & (a_ > 1e-6 * float(a_[sel_arco].max())))[0]
    mm = mp["mpart"][idx]
    lo = mm.min(axis=0)
    n = int(2 ** math.ceil(math.log2(max(mm.max(axis=0) - lo) + 1))) * 2
    P = np.zeros((n, n))
    for a in range(3):
        z = np.zeros((n, n))
        s_ = idx[mp["tipo"][idx] == a]
        if not len(s_):
            continue
        q = mp["mpart"][s_] - lo
        z[q[:, 0], q[:, 1]] = campo.A[s_] * mp["segno"][s_]
        P += np.abs(np.fft.fft2(z)) ** 2
    t1 = 2 * np.pi * np.fft.fftfreq(n)
    T1, T2 = np.meshgrid(t1, t1, indexing="ij")
    kx = np.linalg.solve(B_RET, np.stack([T1.ravel(), T2.ravel()]))
    KX, KY = kx[0].reshape(n, n), kx[1].reshape(n, n)
    meta = (KX * verso[0] + KY * verso[1]) > 0
    Pm = np.where(meta, P, 0.0)
    i = np.unravel_index(np.argmax(Pm), Pm.shape)
    k0 = np.array([KX[i], KY[i]])
    vic = meta & ((KX - k0[0]) ** 2 + (KY - k0[1]) ** 2 <= (3.0 / W_LUCE) ** 2)
    w = Pm * vic
    return np.array([float((w * KX).sum() / w.sum()), float((w * KY).sum() / w.sum())])


# =====================================================================================
#   LE CORSE
# =====================================================================================
def corsa_luce(D, db, mp, b_y, n_sett):
    import _luce_materia_cono as C
    import _luce_materia_cono_2 as C2
    campo = C.CampoGrafo(D.P, D.S, len(D.ii), np.full(len(D.ii), C.S_LUCE))
    C.luce_iniziale(D, campo, W_LUCE, b_y)
    ia = np.isin(D.sett_arco, INGRESSO)
    oa = np.isin(D.sett_arco, USCITA[n_sett])
    ot = np.isin(D.sett_tri, USCITA[n_sett])
    it = np.isin(D.sett_tri, INGRESSO)
    k_in = k_luce(campo, D, mp, ia, (1.0, 0.0))
    tt, xy, pin, pout = [], [], [], []
    t, inizio, x0u, fermata = 0, None, None, "tempo"
    while True:
        ea, et = campo.energia_arco(), campo.energia_tri()
        tot = float(ea.sum() + et.sum())
        c = (ea @ D.pos_arco + et @ D.pos_tri) / tot
        s_in = float((ea[ia].sum() + et[it].sum()) / tot)
        s_out = float((ea[oa].sum() + et[ot].sum()) / tot)
        tt.append(t * C.S_LUCE)
        xy.append(c)
        pin.append(s_in)
        pout.append(s_out)
        if s_out >= C.PERC_FINESTRA and c[0] > 0.0:
            if inizio is None:
                inizio, x0u = t, c
            elif np.linalg.norm(c - x0u) >= L_USCITA:
                fermata = "uscita"
                break
        if t * C.S_LUCE * 1.0 > 2.0 * percorso(abs(b_y)):
            break
        campo.tick()
        t += 1
    r = C2.finestre(tt, xy, pin, pout)
    verso = (math.cos(r["theta_out"]), math.sin(r["theta_out"])) if r["theta_out"] is not None else (1.0, 0.0)
    k_out = k_luce(campo, D, mp, oa, verso)
    th_in, th_out = math.atan2(k_in[1], k_in[0]), math.atan2(k_out[1], k_out[0])
    r.update(tick=t, fermata=fermata, k_in=[float(x) for x in k_in], k_out=[float(x) for x in k_out], delta_impulso=th_out - th_in, frazione_uscita=pout[-1])
    return r


def corsa_materia(D, db, A, nh, mp, b_y, n_sett):
    import scipy.sparse.linalg as sla
    import _luce_materia_cono as C
    import _luce_materia_cono_2 as C2
    x, fuori = C.materia_iniziale(D, W_MAT, b_y)
    pos_h = D.pos[nh]
    sett_h = D.sett[nh]
    vicino = db[nh] <= C.D_BORDO
    mi, mo = np.isin(sett_h, INGRESSO), np.isin(sett_h, USCITA[n_sett])
    q_in, valli_in = k_materia(x, mp, mi)
    T_max = FATTORE_T * percorso(abs(b_y)) / V_MAT
    tt, xy, pin, pout, guardia = [], [], [], [], 0.0
    t = 0.0
    n0 = float(np.vdot(x, x).real)
    while True:
        w = np.abs(x) ** 2
        tot = float(w.sum())
        guardia = max(guardia, float(w[vicino].sum() / tot))
        tt.append(t)
        xy.append((w @ pos_h) / tot)
        pin.append(float(w[mi].sum() / tot))
        pout.append(float(w[mo].sum() / tot))
        if t >= T_max:
            break
        x = sla.expm_multiply(DT_MAT * A, x)
        t += DT_MAT
    r = C2.finestre(tt, xy, pin, pout)
    q_out, valli_out = k_materia(x, mp, mo)
    th_in, th_out = math.atan2(q_in[1], q_in[0]), math.atan2(q_out[1], q_out[0])
    r.update(tempo=t, T_max=T_max, guardia=guardia, norma=abs(tot - n0) / n0, fuori_banda=fuori, q_in=[float(v) for v in q_in], q_out=[float(v) for v in q_out],
             valli_in=valli_in, valli_out=valli_out, frazione_K_in=valli_in["frazione_K"], frazione_K_out=valli_out["frazione_K"],
             delta_impulso=th_out - th_in, frazione_uscita=pout[-1])
    return r


def disco(n, R):
    import scipy.sparse as sp
    import _luce_materia_cono as C
    import _luce_materia_cono_2 as C2
    D = C.Disco(n, R)
    db = C2.dist_bordo_v(D)
    nh = C2.nodo_estremita(D.ii, D.jj)
    Hs = C2.H_sparso_v(D.ii, D.jj, D.nn)
    # ### ⭐ IL SEGNO DEL TEMPO, CORRETTO: il tick e' exp(-i pi s mu), mu = 1 - lambda, cioe' exp(+i pi s (H - I)): il generatore della materia va col +
    A = (+1j) * (Hs - sp.identity(Hs.shape[0], format="csr"))
    return D, db, nh, A, mappa(D)


def main(argv):
    del argv
    import _presidio
    import _universalita_massa as UM
    import _u1_prototipo as U
    import composizione as CM
    import _luce_materia_cono as C
    _presidio.avvia(__file__)
    C.X0, C.Q_MAT = X0, Q_MAT
    R, L_tot, src, R_in = raggio()
    print("=" * 130)
    print("C2, LA MATERIA RIFATTA: il segno del tempo corretto, q 1.0, W 12, il tempo dal percorso, l'angolo dall'impulso medio; e la prova a vuoto sulla luce")
    print("=" * 130)
    blobs = {p: UM.blob(p) for p in ("soliton_simulator.py", "csv/_luce_materia_cono_3.py", "csv/_luce_materia_cono_2.py", "csv/_luce_materia_cono.py", "csv/_u1_prototipo.py")}
    print("  il passo: %d pezzi, impronta %s (intatto); i blob nel repo: %s" % (len(CM.ORDINE), CM.IMPRONTA, "; ".join("%s %s" % (k, v["sha1-BYTE"]) for k, v in blobs.items())))
    print("  la configurazione: X0 %g BB %s Q_MAT %g W_MAT %g V_MAT %g W_LUCE %g L_USCITA %g DT_MAT %g FATTORE_BORDO %g USCITA %s INGRESSO %s R_PROVA %d B_PROVA %g TOLL_PROVA %g TOLL_PI3 %g TOLL_CHIAVE %g"
          % (X0, BB, Q_MAT, W_MAT, V_MAT, W_LUCE, L_USCITA, DT_MAT, FATTORE_BORDO, USCITA, INGRESSO, R_PROVA, B_PROVA, TOLL_PROVA, TOLL_PI3, TOLL_CHIAVE))
    print("  IL RAGGIO DALLA REGOLA: L_tot %.4f, la sorgente a %.4f, l'inraggio >= %.4f: R = %d; il tempo massimo della materia = il percorso / %g" % (L_tot, src, R_in, R, V_MAT))
    print("-" * 130)
    io.open(JSONL, "w", encoding="utf-8").close()
    scrivi({"tipo": "testata", "blobs": blobs, "impronta": CM.IMPRONTA, "R": R, "L_tot": L_tot})
    C.BL_LUCE.append(U.blocchi_campo(C.S_LUCE)[0])
    # ### la prova a vuoto sulla luce
    t0 = time.time()
    Dp, dbp, _nh, _A, mpp = disco(5, R_PROVA)
    prova = {}
    for lato in (+1, -1):
        prova[lato] = corsa_luce(Dp, dbp, mpp, lato * B_PROVA, 5)
    cp = prova[-1]["delta_impulso"] - prova[+1]["delta_impulso"]
    scrivi({"tipo": "prova_luce", "R": R_PROVA, "b": B_PROVA, "sopra": prova[+1], "sotto": prova[-1], "convergenza_impulso": cp})
    print("  LA PROVA A VUOTO (il cono di lato %d, b %g, la luce): dall'impulso sopra %+.5f sotto %+.5f -> la convergenza %+.5f; dal baricentro %+.5f (%.0f s)"
          % (R_PROVA, B_PROVA, prova[+1]["delta_impulso"], prova[-1]["delta_impulso"], cp, (prova[-1]["delta"] or 0) - (prova[+1]["delta"] or 0), time.time() - t0))
    esito("DEVE PASSARE (prova): la lettura dall'impulso ridà pi/3 entro l'%g%% sulla luce" % (100 * TOLL_PROVA), abs(cp - math.pi / 3) <= TOLL_PROVA * math.pi / 3, "%+.5f" % cp)
    del Dp, dbp, _nh, _A, mpp
    ris = []
    for n in (6, 5):
        t0 = time.time()
        if all(os.path.exists(os.path.join(PEZZI, "c2m_%d_%g_%+d.parziale" % (n, b, lato))) for b in BB for lato in (+1, -1)):
            D = db = nh = A = mp = None
        else:
            D, db, nh, A, mp = disco(n, R)
        if D is not None:
            print("  il disco a %d settori di lato %d: %d nodi, %d archi (%.0f s)" % (n, R, D.nn, len(D.ii), time.time() - t0))
        for b in BB:
            coppia = {}
            for lato in (+1, -1):
                t0 = time.time()
                pz = os.path.join(PEZZI, "c2m_%d_%g_%+d.parziale" % (n, b, lato))
                if os.path.exists(pz):
                    r = json.loads(io.open(pz, encoding="utf-8").read())
                    print("  (il pezzo %s, gia' chiuso: ripreso)" % os.path.basename(pz))
                else:
                    r = corsa_materia(D, db, A, nh, mp, lato * b, n)
                    r.update(disco=n, chi="materia", b=b, lato=lato, secondi=time.time() - t0)
                    tmp = pz + ".tmp"
                    io.open(tmp, "w", encoding="utf-8", newline="\n").write(json.dumps(r, ensure_ascii=False, sort_keys=True))
                    os.replace(tmp, pz)
                coppia[lato] = r
                scrivi(dict(r, tipo="corsa"))
                print("  materia disco %d b %4g lato %+d: dal baricentro %s (punti %d/%d); dall'impulso %+.5f; la frazione uscita %.3f; il peso in K %.4f -> %.4f; la guardia %.1e; T_max %.0f (%.0f s)"
                      % (n, b, lato, "%+.5f" % r["delta"] if r["delta"] is not None else "-", r["punti_in"], r["punti_out"], r["delta_impulso"], r["frazione_uscita"],
                         r["frazione_K_in"], r["frazione_K_out"], r["guardia"], r["T_max"], r["secondi"]))
                sys.stdout.flush()
            cb = (coppia[-1]["delta"] - coppia[+1]["delta"]) if coppia[-1]["delta"] is not None and coppia[+1]["delta"] is not None else None
            ci = coppia[-1]["delta_impulso"] - coppia[+1]["delta_impulso"]
            ris.append({"disco": n, "chi": "materia", "b": b, "sopra": coppia[+1], "sotto": coppia[-1], "convergenza": cb, "convergenza_impulso": ci})
            scrivi({"tipo": "convergenza", "disco": n, "b": b, "convergenza": cb, "convergenza_impulso": ci})
            print("  ### materia disco %d b %g: LA CONVERGENZA dal baricentro %s, dall'impulso %+.5f (pi/3 = %.5f)" % (n, b, "%+.5f" % cb if cb is not None else "-", ci, math.pi / 3))
        del D, db, nh, A, mp
    print("-" * 130)
    print("### I CRITERI")

    def trova(n, chi, b):
        return [r for r in ris if r["disco"] == n and r["chi"] == chi and r["b"] == b][0]
    fb = max(r[l]["fuori_banda"] for r in ris for l in ("sopra", "sotto"))
    esito("DEVE PASSARE (0): il pacchetto di materia nella banda entro %g" % TOLL_BANDA, fb <= TOLL_BANDA, "%.1e" % fb)
    tol = 0.1 / (Q_MAT * W_MAT)
    ok1, n1 = True, []
    for b in BB:
        r = trova(6, "materia", b)
        for lato in ("sopra", "sotto"):
            d = r[lato]["delta"]
            ok1 &= d is not None and abs(d) <= tol
            n1.append("%g %s %s / impulso %+.4f" % (b, lato[:2], "%+.4f" % d if d is not None else "-", r[lato]["delta_impulso"]))
    esito("DEVE PASSARE (1): sul PIATTO nessuna deviazione dal baricentro, entro 0.1/(|q| W) = %.4f, i due fasci, a ogni b" % tol, ok1, "; ".join(n1))
    cm = [trova(5, "materia", b)["convergenza"] for b in BB]
    esito("PUO' FALLIRE (2): la MATERIA sul cono converge di pi/3 entro il %g%% a ogni b (dal baricentro)" % (100 * TOLL_PI3),
          all(c is not None and abs(c - math.pi / 3) <= TOLL_PI3 * math.pi / 3 for c in cm), " ".join("%+.5f" % c if c is not None else "-" for c in cm), deve=False)
    print("  il controllo, dall'impulso medio: %s" % " ".join("%+.5f" % trova(5, "materia", b)["convergenza_impulso"] for b in BB))
    ch = cm[0] / cm[-1] if cm[0] is not None and cm[-1] is not None and cm[-1] != 0 else None
    esito("DEVE FALLIRE, PER LA CHIAVE GIUSTA (3): la materia va come 1/b; la chiave: conv(b %g)/conv(b %g) entro il %g%% da 1, non %g" % (BB[0], BB[-1], 100 * TOLL_CHIAVE, BB[-1] / BB[0]),
          ch is not None and abs(ch - 1) <= TOLL_CHIAVE, "%.4f" % ch if ch is not None else "-")
    print("### LE VALLI: la frazione del peso in K all'uscita, fascio per fascio (una lettura)")
    for n in (6, 5):
        for b in BB:
            r = trova(n, "materia", b)
            print("  disco %d b %g: sopra %.4f, sotto %.4f (all'ingresso %.4f, %.4f)" % (n, b, r["sopra"]["frazione_K_out"], r["sotto"]["frazione_K_out"], r["sopra"]["frazione_K_in"], r["sotto"]["frazione_K_in"]))
    print("-" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    scrivi({"tipo": "esito", "passano": OK[0], "totale": OK[1], "deve_fallite": FALLITE})
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
