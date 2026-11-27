# -*- coding: utf-8 -*-
r"""**[M0137-B] IL PUNTO FISSO CON CHI ACCESO** *(DECISIONE DI LUCA, 2026-11-25 01:37, dalla posta; la carta `doc/CARTA_fondo_giusto.md`, sez. `3-sedecies`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/fondo_puntofisso_chi.py noto > doc/referti_l2/fondo_puntofisso_chi_noto.txt
    E:\python\py3132\python.exe doc/referti_l2/fondo_puntofisso_chi.py giro --g 1          (dalla coda; il giro dopo, a giro chiuso)
    E:\python\py3132\python.exe doc/referti_l2/fondo_puntofisso_chi.py lettura > doc/referti_l2/fondo_puntofisso_chi.txt

**Un giro:** `6000` tick di `chi_tick_v2.tick_chi_v2` *(kappa acceso)* nella forma `L-1` *(`due_corpi_fondo_v3`: il nucleo preso prima della scena, `U` riscritto dopo i parametri)*; **ogni `100` tick in memoria:** `w` *(la formula di `torneo_tenuta.misura`)*, `max|chi|`, la profondita' *(chi medio su `[0, 4)` dal baricentro)*, la somma progressiva di `psi e^{i theta}` *(`theta` dagli `omega` per tick)*; **gli stati ogni `250`.** **Alla fine:** la finestra col metodo della v3b *(`fondo_puntofisso_v3b.periodo`)*, `psi` mediato, riproiettato su `Q_K` e riportato alla massa *(`fondo_puntofisso.trasforma`)*; **le altre chiavi, i campi, `chi`, `pi`, `Theta` dallo stato a `k 6000`**. **I parametri di chi:** calcolati al giro `1` e scritti nel suo `giro.json`; i giri dopo li rileggono.
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
import due_corpi_fondo_v3 as D3  # noqa: E402
import fondo_puntofisso_v3b as V3B  # noqa: E402

D = D3.D
F1, G4, PF, CT, CV2 = D.F1, D.G4, D.PF, D.CT, D.CV2
DIR = os.path.join(PF.CTRL, "M0137", "puntofisso_chi")
K_GIRO, OGNI, OGNI_STATO = 6000, 100, 250
SOGLIA_CHI, SOGLIA_W = 0.10, 0.10          # ### Luca, il criterio C


def w_di(rho, L):
    """### la formula di `torneo_tenuta.misura` sulla `rho` in memoria."""
    lis = F1.TT.lisciata(rho, L)
    mx = float(lis.max())
    return math.sqrt(float(np.sum(lis > 0.5 * mx)) * math.sqrt(3.0) / 2.0 / math.pi)


def profondita(Z, rho, chi):
    from solitone import toro as TO
    b = TO.centro(rho, Z["m1"], Z["m2"], Z["L"])[:2]
    d = np.asarray(TO.scarti(Z["m1"], Z["m2"], b[0], b[1], Z["L"]))[:, :2]
    return float(chi[np.hypot(d[:, 0], d[:, 1]) < 4.0].mean())


def partenza_di(g):
    return G4.PARTENZA_G4 if g == 1 else os.path.join(DIR, "giro_%d" % (g - 1), "partenza_giro_%d.npz" % g)


def parametri_giro1():
    f = os.path.join(DIR, "giro_1", "giro.json")
    PF.controlla(f)
    p = json.load(open(f, encoding="utf-8"))["parametri"]
    return CV2.Parametri2(p["kappa"], p["c0"], p["s"], p["e0"], p["f"], p["c2"], p["m2"])


def carica(Z, g):
    """### `(C, P, X, info)` per il giro `g`."""
    mot = Z["mot"]
    F1.OGGETTO = partenza_di(g)
    C, info = D.costruisci(Z, 1, campi_stato=True)
    if g == 1:
        P, Pon, m0 = D.parametri(Z, C, True)
        X = CT.nuovo_X(mot.inc.n, mot.inc.m, CT.chi_statico(mot, Z["st"], Z["par"], Pon, CT.Laplaciano(mot), m0))
        info = dict(info, m0=m0)
    else:
        P = parametri_giro1()
        with np.load(F1.OGGETTO) as z:
            X = {q: z[q].copy() for q in CT.CHIAVI_CHI}
    return C, P, X, info


def giro(g):
    D.avvia()
    import _presidio
    _presidio.avvia(__file__)
    f_part = partenza_di(g)
    PF.controlla(f_part)
    d = os.path.join(DIR, "giro_%d" % g)
    assert not os.path.exists(d), "%s c'e' gia': non si riscrive" % d
    os.makedirs(d)
    Q = PF.leggi_Q()
    massa = PF.massa_di(PF.PARTENZA_1)
    t1 = time.time()
    with D.GD.TC.scena() as Z:
        mot, n, L = Z["mot"], Z["n"], Z["L"]
        nodo = np.asarray(mot.inc.nodo)
        Lp = CT.Laplaciano(mot)
        C, P, X, info = carica(Z, g)
        meta = dict(info, giro=g, partenza=f_part, parametri={"kappa": P.kappa, "c0": P.c0, "s": P.s, "e0": P.e0, "f": P.f, "c2": P.c2, "m2": P.m2})
        print("### [M0137] giro %d: la partenza %s; i parametri %r; l'impronta %s" % (g, f_part, P, D.GD.impronta(Z, C, X)[:12]))
        sys.stdout.flush()
        rho = np.bincount(nodo, weights=np.sum(np.abs(Z["st"]["psi_h"]) ** 2, axis=1), minlength=n)
        ws, mc, pr, om = [w_di(rho, L)], [float(np.max(np.abs(X["chi"])))], [profondita(Z, rho, X["chi"])], []
        somma = np.zeros_like(Z["st"]["psi_h"])
        S = {0: somma.copy()}
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
            if kk % OGNI == 0:
                S[kk] = somma.copy()
                r = np.bincount(nodo, weights=np.sum(np.abs(Z["st"]["psi_h"]) ** 2, axis=1), minlength=n)
                ws.append(w_di(r, L))
                mc.append(float(np.max(np.abs(X["chi"]))))
                pr.append(profondita(Z, r, X["chi"]))
            if kk % OGNI_STATO == 0:
                salva(kk)
            if kk % 500 == 0:
                print("    k %d: w %.3f, max|chi| %.3f, la profondita' %+.3f, omega %+.6f (%.0f s)" % (kk, ws[-1], mc[-1], pr[-1], o, time.time() - t1))
                sys.stdout.flush()
        salva(0)
        D.ciclo(Z, C, P, Lp, X, K_GIRO, dopo)
        Z["metti"]()
    per = V3B.periodo(ws, OGNI, K_GIRO)
    esce = {"giro": g, "partenza": f_part, "w": ws, "maxchi": mc, "profondita": pr, "omega": om, "periodo": {q: v for q, v in per.items() if q not in ("lisciata", "lisciata_k")},
            "parametri": meta["parametri"], "m0": info.get("m0")}
    if "fermo" not in per:
        ka, kb = per["finestra"]
        psi_medio = (S[kb] - S[ka]) / float(kb - ka)
        import gravita_due_corpi_misure as GM
        X6, m6 = GM.leggi(os.path.join(d, "stato_%06d.npz" % K_GIRO))
        dati = {x: X6[x] for x in X6}
        dati["psi_h"] = PF.trasforma(psi_medio, Q, n, massa)
        f_nuova = os.path.join(d, "partenza_giro_%d.npz" % (g + 1))
        PF.salva_stato(f_nuova, dati, dict(m6, k=3000, giro=g + 1, finestra=[ka, kb]))
        esce["partenza_nuova"] = f_nuova
    f = os.path.join(d, "giro.json")
    open(f, "w", encoding="utf-8").write(json.dumps(esce))
    PF.firma(f)
    print("### giro %d: %s; %d tick in %.0f s" % (g, V3B.descrivi(per), K_GIRO, time.time() - t1))
    return 0 if "fermo" not in per else 2


def noto():
    D.avvia()
    import _presidio
    import gravita_due_corpi_misure as GM
    _presidio.avvia(__file__)
    print("=" * 130)
    print("[M0137] I CASI NOTI DEL PUNTO FISSO CON CHI (la carta sez. 3-sedecies)")
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
        C, info = D.costruisci(Z, 1, campi_stato=True)
        P, Pon, m0 = D.parametri(Z, C, True)
        chi_s = CT.chi_statico(mot, Z["st"], Z["par"], Pon, Lp, m0)
        Fs = float(np.max(np.abs(CT.forza(mot, Z["st"], Z["par"], Pon, Lp, chi_s))))
        F0 = float(np.max(np.abs(CT.forza(mot, Z["st"], Z["par"], Pon, Lp, np.zeros(n)))))
        esito("(K2, l'equivalente dichiarato) max|forza(chi_statico)| almeno 100 volte sotto max|forza(0)|", Fs < F0 / 100.0, "%.3e contro %.3e (il rapporto %.3e); m0 %.6e, c0 %.6e" % (Fs, F0, Fs / F0, m0, Pon.c0))
        Q = PF.leggi_Q()
        massa = PF.massa_di(PF.PARTENZA_1)
        pq = PF.trasforma(Z["st"]["psi_h"].copy(), Q, n, massa)
        r = abs(float(np.sum(np.abs(pq) ** 2)) / massa - 1.0)
        esito("(K3) la riproiezione su Q_K riporta alla massa entro 1e-12", r < 1e-12, "%.1e" % r)
        Z["metti"]()
    fall = [k for k, v in OK.items() if not v]
    print("### %d DEVE: %d PASSANO, %d FALLISCONO %s" % (len(OK), len(OK) - len(fall), len(fall), fall))
    print("=" * 130)
    return 0 if not fall else 1


def lettura():
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "fondo_puntofisso_v3b.py"))
    _presidio.avvia(__file__)
    print("=" * 130)
    print("[M0137] IL PUNTO FISSO CON CHI (la carta sez. 3-sedecies): per giro, per finestra di 500; il criterio C (max|chi| fra giri < %.0f%% E il respiro < %.0f%%)" % (100 * SOGLIA_CHI, 100 * SOGLIA_W))
    print("=" * 130)
    G = []
    for g in (1, 2, 3):
        f = os.path.join(DIR, "giro_%d" % g, "giro.json")
        if not os.path.exists(f + ".sha1"):
            break
        PF.controlla(f)
        G.append(json.load(open(f, encoding="utf-8")))
    for x in G:
        ws, mc, pr, om = np.array(x["w"]), np.array(x["maxchi"]), np.array(x["profondita"]), np.array(x["omega"])
        print("  giro %d (i parametri %s; m0 %s):" % (x["giro"], x["parametri"], x.get("m0")))
        for k0 in range(0, K_GIRO, 500):
            i0, i1 = k0 // OGNI, (k0 + 500) // OGNI
            print("    [%4d, %4d]: max|chi| %.3f; w medio %.3f (da %.3f a %.3f); la profondita' media %+.3f; omega medio %+.7f" % (
                k0, k0 + 500, float(mc[i0:i1 + 1].max()), float(ws[i0:i1 + 1].mean()), float(ws[i0:i1 + 1].min()), float(ws[i0:i1 + 1].max()), float(pr[i0:i1 + 1].mean()), float(om[k0:k0 + 500].mean())))
        rs = (ws.max() - ws.min()) / ws.mean()
        print("  ### giro %d: max|chi| del giro %.3f; il respiro %.4f; il periodo: %s" % (x["giro"], float(mc.max()), rs, V3B.descrivi(x["periodo"]) if "finestra" in x["periodo"] or "fermo" in x["periodo"] else x["periodo"]))
    for a, b in zip(G, G[1:]):
        ra = float(np.max(b["maxchi"])) / float(np.max(a["maxchi"])) - 1.0
        wb = np.array(b["w"])
        rs = float((wb.max() - wb.min()) / wb.mean())
        ok = abs(ra) < SOGLIA_CHI and rs < SOGLIA_W
        print("### IL CRITERIO C fra il giro %d e il giro %d: max|chi| cambia del %+.2f%%; il respiro del giro %d %.4f: %s" % (a["giro"], b["giro"], 100 * ra, b["giro"], rs, "PASSA" if ok else "NON PASSA"))
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
