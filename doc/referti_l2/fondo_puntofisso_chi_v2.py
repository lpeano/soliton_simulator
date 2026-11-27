# -*- coding: utf-8 -*-
r"""**[M0414] IL PUNTO FISSO ACCOPPIATO (psi, chi)** *(DECISIONE DI LUCA, 2026-11-25 04:14, dalla posta; la carta `doc/CARTA_fondo_giusto.md`, sez. `3-sedecies`, il blocco [M0414]; `fondo_puntofisso_chi.py` e' usato e non si riscrive)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/fondo_puntofisso_chi_v2.py noto > doc/referti_l2/fondo_puntofisso_chi_v2_noto.txt
    E:\python\py3132\python.exe doc/referti_l2/fondo_puntofisso_chi_v2.py giro --g 1          (dalla coda; il giro dopo a giro chiuso)
    E:\python\py3132\python.exe doc/referti_l2/fondo_puntofisso_chi_v2.py lettura > doc/referti_l2/fondo_puntofisso_chi_v2.txt

**Un giro:** `6000` tick di `tick_chi_v2` *(kappa acceso, i parametri del giro 1 di [M0137])* nella forma `L-1`. **Ogni tick** `max|chi|` *(il massimo per finestra di `250`)*; **ogni `100`** `w`, la profondita'; **ogni `250`** le somme progressive di `psi e^{i theta}` e di chi. **B':** `P` = la distanza fra gli ULTIMI due picchi di `max|chi|` per finestra *(un picco: `3` finestre in salita stretta prima, `3` in discesa stretta dopo)*; senza due picchi `P = 2500`. **B'':** la nuova partenza = `psi` medio su `[6000 - P, 6000]`, riproiettato e riportato alla massa; **chi medio** sulla stessa finestra; **`pi = 0`**; le altre chiavi e i campi dallo stato a `k 6000`. **La partenza del giro 1:** `M0137/puntofisso_chi/giro_3/stato_006000.npz` con `pi = 0`.
"""
import argparse
import json
import math
import os
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import fondo_puntofisso_chi as FPC  # noqa: E402

D, F1, G4, PF, CT, CV2 = FPC.D, FPC.F1, FPC.G4, FPC.PF, FPC.CT, FPC.CV2
DIR = os.path.join(PF.CTRL, "M0414", "puntofisso_accoppiato")
PARTENZA_1 = os.path.join(FPC.DIR, "giro_3", "stato_006000.npz")
K_GIRO, OGNI_W, FIN = 6000, 100, 250
P_RIPIEGO = 2500           # ### Luca, B'
SOGLIA_CHI, SOGLIA_W = FPC.SOGLIA_CHI, FPC.SOGLIA_W


def picchi(v):
    """### gli indici `i` con `v[i-3] < v[i-2] < v[i-1] < v[i] > v[i+1] > v[i+2] > v[i+3]`."""
    return [i for i in range(3, len(v) - 3) if v[i - 3] < v[i - 2] < v[i - 1] < v[i] > v[i + 1] > v[i + 2] > v[i + 3]]


def periodo(v):
    """### `(P, picchi_k, fonte)`: gli ultimi due picchi, o il ripiego."""
    pk = picchi(v)
    kp = [FIN * (i + 1) for i in pk]          # ### la finestra i copre (250 i, 250 (i + 1)]: si nomina col suo k finale
    if len(pk) >= 2:
        return kp[-1] - kp[-2], kp, "gli ultimi due picchi, a k %d e %d" % (kp[-2], kp[-1])
    return P_RIPIEGO, kp, "il ripiego %d (%d picchi)" % (P_RIPIEGO, len(pk))


def partenza_di(g):
    return PARTENZA_1 if g == 1 else os.path.join(DIR, "giro_%d" % (g - 1), "partenza_giro_%d.npz" % g)


def giro(g):
    D.avvia()
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "fondo_puntofisso_chi.py"))
    _presidio.avvia(__file__)
    import gravita_due_corpi_misure as GM
    f_part = partenza_di(g)
    PF.controlla(f_part)
    d = os.path.join(DIR, "giro_%d" % g)
    assert not os.path.exists(d), "%s c'e' gia': non si riscrive" % d
    os.makedirs(d)
    Q = PF.leggi_Q()
    massa = PF.massa_di(PF.PARTENZA_1)
    P = FPC.parametri_giro1()
    t1 = time.time()
    with D.GD.TC.scena() as Z:
        mot, n, L = Z["mot"], Z["n"], Z["L"]
        nodo = np.asarray(mot.inc.nodo)
        Lp = CT.Laplaciano(mot)
        F1.OGGETTO = f_part
        C, info = D.costruisci(Z, 1, campi_stato=True)
        with np.load(f_part) as z:
            X = {"chi": z["chi"].copy(), "pi": np.zeros_like(z["pi"]), "theta_a": z["theta_a"].copy()}
        res0 = float(C.residuo())
        meta = dict(info, giro=g, partenza=f_part, parametri={"kappa": P.kappa, "c0": P.c0, "s": P.s, "e0": P.e0, "f": P.f, "c2": P.c2, "m2": P.m2})
        print("### [M0414] giro %d: la partenza %s (pi = 0); il residuo di Gauss alla partenza %.3e; i parametri %r" % (g, f_part, res0, P))
        sys.stdout.flush()
        rho = np.bincount(nodo, weights=np.sum(np.abs(Z["st"]["psi_h"]) ** 2, axis=1), minlength=n)
        ws, pr, om = [FPC.w_di(rho, L)], [FPC.profondita(Z, rho, X["chi"])], []
        mcf, mc_cur = [], [float(np.max(np.abs(X["chi"])))]
        somma, schi = np.zeros_like(Z["st"]["psi_h"]), np.zeros_like(X["chi"])
        S, SC = {0: somma.copy()}, {0: schi.copy()}
        th = [0.0]

        def salva(k):
            f = os.path.join(d, "stato_%06d.npz" % k)
            dati = {x: Z["st"][x] for x in Z["chiavi"]}
            dati.update(campo_A=C.campo.A, campo_E=C.campo.E, **{q: X[q] for q in CT.CHIAVI_CHI})
            PF.salva_stato(f, dati, dict(meta, k=k))

        def dopo(kk, prima):
            o = float(-np.angle(np.vdot(prima, Z["st"]["psi_h"])))
            om.append(o)
            th[0] += o
            somma[...] += Z["st"]["psi_h"] * np.exp(1j * th[0])
            schi[...] += X["chi"]
            mc_cur.append(float(np.max(np.abs(X["chi"]))))
            if kk % OGNI_W == 0:
                r = np.bincount(nodo, weights=np.sum(np.abs(Z["st"]["psi_h"]) ** 2, axis=1), minlength=n)
                ws.append(FPC.w_di(r, L))
                pr.append(FPC.profondita(Z, r, X["chi"]))
            if kk % FIN == 0:
                S[kk], SC[kk] = somma.copy(), schi.copy()
                mcf.append(max(mc_cur[1:]) if len(mc_cur) > 1 else mc_cur[0])
                mc_cur[:] = [mc_cur[-1]]
                salva(kk)
            if kk % 500 == 0:
                print("    k %d: w %.3f, max|chi| (la finestra) %.3f, la profondita' %+.3f, omega %+.6f (%.0f s)" % (kk, ws[-1], mcf[-1], pr[-1], o, time.time() - t1))
                sys.stdout.flush()
        salva(0)
        D.ciclo(Z, C, P, Lp, X, K_GIRO, dopo)
        Z["metti"]()
    Pp, kp, fonte = periodo(mcf)
    ka, kb = K_GIRO - Pp, K_GIRO
    psi_medio = (S[kb] - S[ka]) / float(kb - ka)
    chi_medio = (SC[kb] - SC[ka]) / float(kb - ka)
    X6, m6 = GM.leggi(os.path.join(d, "stato_%06d.npz" % K_GIRO))
    dati = {x: X6[x] for x in X6}
    dati["psi_h"] = PF.trasforma(psi_medio, Q, n, massa)
    dati["chi"] = chi_medio
    dati["pi"] = np.zeros_like(X6["pi"])
    f_nuova = os.path.join(d, "partenza_giro_%d.npz" % (g + 1))
    PF.salva_stato(f_nuova, dati, dict(m6, k=3000, giro=g + 1, finestra=[ka, kb], P=Pp))
    esce = {"giro": g, "partenza": f_part, "residuo_partenza": res0, "w": ws, "maxchi_fin": mcf, "profondita": pr, "omega": om,
            "P": Pp, "picchi_k": kp, "fonte": fonte, "finestra": [ka, kb], "partenza_nuova": f_nuova, "parametri": meta["parametri"]}
    f = os.path.join(d, "giro.json")
    open(f, "w", encoding="utf-8").write(json.dumps(esce))
    PF.firma(f)
    print("### giro %d: P %d (%s); i picchi a k %s; la finestra [%d, %d]; %d tick in %.0f s" % (g, Pp, fonte, kp, ka, kb, K_GIRO, time.time() - t1))
    return 0


def noto():
    D.avvia()
    import _presidio
    import gravita_due_corpi_misure as GM
    _presidio.avvia(os.path.join(_QUI, "fondo_puntofisso_chi.py"))
    _presidio.avvia(__file__)
    print("=" * 130)
    print("[M0414] I CASI NOTI DEL PUNTO FISSO ACCOPPIATO (la carta sez. 3-sedecies, [M0414])")
    print("=" * 130)
    OK = {}

    def esito(che, ok, nota=""):
        OK[che] = bool(ok)
        print("  DEVE: %-100s %s %s" % (che, "PASSA" if ok else "### FALLISCE", nota))
        sys.stdout.flush()
    with D.GD.TC.scena() as Z:
        mot = Z["mot"]
        n, m = mot.inc.n, mot.inc.m
        Lp = CT.Laplaciano(mot)
        F1.OGGETTO = G4.PARTENZA_G4
        C, info = D.costruisci(Z, 1, campi_stato=True)
        P, Pon, m0 = D.parametri(Z, C, False)
        X = CT.nuovo_X(n, m, CT.chi_statico(mot, Z["st"], Z["par"], Pon, Lp, m0))
        D.ciclo(Z, C, P, Lp, X, 100, lambda kk, prima: None)
        Xg, _m = GM.leggi(os.path.join(PF.DIR, "giro_4", "stato_000100.npz"))
        dv = [x for x in Z["chiavi"] if not np.array_equal(Z["st"][x], Xg[x])] + [q for q, a_, b_ in (("A", C.campo.A, Xg["campo_A"]), ("E", C.campo.E, Xg["campo_E"])) if not np.array_equal(a_, b_)]
        esito("(K1) kappa 0, i campi dello stato, 100 tick nella forma L-1 = la tenuta del giro 4 a k 100 AL BIT", not dv, "diverse %s" % dv)
        Z["metti"]()
    base = [10.0 + 0.1 * i for i in range(24)]
    v = list(base)
    for c in (4, 14):
        for j, a_ in ((-3, 1.0), (-2, 2.0), (-1, 3.0), (0, 4.0), (1, 3.0), (2, 2.0), (3, 1.0)):
            v[c + j] = base[c + j] + 10.0 * a_
    Pp, kp, fonte = periodo(v)
    esito("(K5) due picchi a 10 finestre (2500 tick): P 2500", Pp == 2500 and len(kp) == 2, "P %d, i picchi a k %s (%s)" % (Pp, kp, fonte))
    v1 = list(base)
    for j, a_ in ((-3, 1.0), (-2, 2.0), (-1, 3.0), (0, 4.0), (1, 3.0), (2, 2.0), (3, 1.0)):
        v1[9 + j] = base[9 + j] + 10.0 * a_
    P1_, kp1, fonte1 = periodo(v1)
    esito("(K5) DEVE FALLIRE i due picchi: con un picco solo P e' il ripiego dichiarato, non una distanza", len(kp1) == 1 and fonte1.startswith("il ripiego"), "%s" % fonte1)
    c = np.array([-100.0, -37.0, 5.0, 0.0])
    Np = 2500
    sc = np.zeros_like(c)
    S0 = sc.copy()
    for _ in range(Np):
        sc += c
    med = (sc - S0) / float(Np)
    esito("(K6) la media di un chi costante (a valori interi) su 2500 tick = lo stesso chi AL BIT; pi = 0", np.array_equal(med, c), "%s" % med)
    fall = [k for k, v_ in OK.items() if not v_]
    print("### %d DEVE: %d PASSANO, %d FALLISCONO %s" % (len(OK), len(OK) - len(fall), len(fall), fall))
    print("=" * 130)
    return 0 if not fall else 1


def lettura():
    import _presidio
    _presidio.avvia(__file__)
    print("=" * 130)
    print("[M0414] IL PUNTO FISSO ACCOPPIATO: per giro; il criterio C (max|chi| fra giri < %.0f%% E il respiro < %.0f%%); D se serve" % (100 * SOGLIA_CHI, 100 * SOGLIA_W))
    print("=" * 130)
    G = []
    for g in (1, 2, 3):
        f = os.path.join(DIR, "giro_%d" % g, "giro.json")
        if not os.path.exists(f + ".sha1"):
            break
        PF.controlla(f)
        G.append(json.load(open(f, encoding="utf-8")))
    for x in G:
        ws, mc, pr, om = np.array(x["w"]), np.array(x["maxchi_fin"]), np.array(x["profondita"]), np.array(x["omega"])
        print("  giro %d: il residuo di Gauss alla partenza %.3e; P %d (%s); i picchi a k %s; la finestra della media %s" % (x["giro"], x["residuo_partenza"], x["P"], x["fonte"], x["picchi_k"], x["finestra"]))
        print("    max|chi| per finestra di 250: %s" % " ".join("%.1f" % a for a in mc))
        for k0 in range(0, K_GIRO, 500):
            i0, i1 = k0 // OGNI_W, (k0 + 500) // OGNI_W
            print("    [%4d, %4d]: w medio %.3f (da %.3f a %.3f); la profondita' media %+.3f; omega medio %+.7f" % (
                k0, k0 + 500, float(ws[i0:i1 + 1].mean()), float(ws[i0:i1 + 1].min()), float(ws[i0:i1 + 1].max()), float(pr[i0:i1 + 1].mean()), float(om[k0:k0 + 500].mean())))
        print("  ### giro %d: max|chi| del giro %.3f; il respiro %.4f; la profondita' media %+.3f; omega medio %+.7f" % (x["giro"], float(mc.max()), float((ws.max() - ws.min()) / ws.mean()), float(pr.mean()), float(om.mean())))
    ok_c = False
    for a, b in zip(G, G[1:]):
        ra = float(np.max(b["maxchi_fin"])) / float(np.max(a["maxchi_fin"])) - 1.0
        wb = np.array(b["w"])
        rs = float((wb.max() - wb.min()) / wb.mean())
        ok = abs(ra) < SOGLIA_CHI and rs < SOGLIA_W
        ok_c = ok_c or ok
        print("### IL CRITERIO C fra il giro %d e il giro %d: max|chi| cambia del %+.2f%%; il respiro del giro %d %.4f: %s" % (a["giro"], b["giro"], 100 * ra, b["giro"], rs, "PASSA" if ok else "NON PASSA"))
    if len(G) == 3 and not ok_c:
        ra = float(np.max(G[2]["maxchi_fin"])) / float(np.max(G[1]["maxchi_fin"])) - 1.0
        if abs(ra) < SOGLIA_CHI:
            Pp = G[2]["P"]
            print("### D: C non passa in 3 giri, ma max|chi| e' fermo entro il 10%% (%+.2f%%): il respiro e' un modo normale. Omega_b = 2 pi / P = 2 pi / %d = %.6e per tick; la profondita' media del giro 3 %+.3f" % (100 * ra, Pp, 2 * math.pi / Pp, float(np.mean(G[2]["profondita"]))))
        else:
            print("### D NON SI APPLICA: max|chi| non e' fermo entro il 10%% (%+.2f%%)" % (100 * ra))
    print("=" * 130)
    return 0


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("cosa", choices=("noto", "giro", "lettura"))
    ap.add_argument("--g", type=int, choices=(1, 2, 3))
    a = ap.parse_args(argv)
    if a.cosa == "giro":
        return giro(a.g)
    return {"noto": noto, "lettura": lettura}[a.cosa]()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
