# -*- coding: utf-8 -*-
r"""**[M1330-B] IL PUNTO FISSO DEL SOLITONE: L'OGGETTO AL FONDO A K SENZA RESPIRO** *(DECISIONE DI LUCA, 2026-11-24 13:30; la carta `doc/CARTA_fondo_giusto.md`, sez. `3-bis`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/fondo_puntofisso.py noto > doc/referti_l2/fondo_puntofisso_noto.txt
    E:\python\py3132\python.exe doc/referti_l2/fondo_puntofisso.py corsa         (M1330_puntofisso, dalla coda: tre giri)
    E:\python\py3132\python.exe doc/referti_l2/fondo_puntofisso.py lettura > doc/referti_l2/fondo_puntofisso.txt

**Un giro:** (i) `2000` tick a `N = 1` col tick della tenuta, gli stati ogni `50`, `omega` per tick, `w` ogni `50`; (ii) il periodo fra i primi due minimi locali stretti di `w`, la media di `psi_j e^{+i theta_j}` sul periodo (`theta_j` = la somma degli `omega` misurati); (iii) la riproiezione su `Q_K` cella per cella e la massa di partenza; le altre chiavi e i campi dallo stato a `k_b`. **Tre giri**; il criterio `(w_max - w_min)/w_medio < 5%` sull'ultimo. **Senza due minimi: FERMO** (codice `2`).
"""
import argparse
import hashlib
import json
import math
import os
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import fondo_1c as F1  # noqa: E402

CTRL = os.path.join("E:" + os.sep, "soliton_simulator", "controllo")
PARTENZA_1 = os.path.join(CTRL, "M1658", "tenuta", "L-1_proiezione_K", "stato_003000.npz")
F_Q = os.path.join(CTRL, "M1658", "c1_parti", "Q_K.npz")
DIR = os.path.join(CTRL, "M1330", "puntofisso")
GIRI, K_GIRO, OGNI = 3, 2000, 50
SOGLIA = 0.05
F_OMEGA_CADUTA = os.path.join(CTRL, "M1658", "c1_omega", "omega.json")


def sha1(f):
    return hashlib.sha1(open(f, "rb").read()).hexdigest()


def firma(f):
    open(f + ".sha1", "w", encoding="utf-8").write(sha1(f) + "\n")


def controlla(f):
    assert open(f + ".sha1", encoding="utf-8").read().split()[0] == sha1(f), "lo sha1 di %s NON coincide" % f


def leggi_Q():
    controlla(F_Q)
    with np.load(F_Q) as z:
        return z["Q"].copy()


def trasforma(psi_medio, Q, n, massa):
    """### (iii): la riproiezione cella per cella su `Q` e la massa `massa`."""
    psi = psi_medio.reshape(n, 12)
    pr = psi @ Q.conj() @ Q.T
    pr = pr * math.sqrt(massa / float(np.sum(np.abs(pr) ** 2)))
    return pr.reshape(psi_medio.shape)


def minimi(ws):
    """### i minimi locali stretti sulla griglia: indici `i` con `w[i] < w[i-1]` e `w[i] < w[i+1]`."""
    return [i for i in range(1, len(ws) - 1) if ws[i] < ws[i - 1] and ws[i] < ws[i + 1]]


def salva_stato(f, dati, meta):
    np.savez(f, meta=np.array(json.dumps(meta)), **dati)
    firma(f)


def nuova_partenza(X_b, psi_nuovo, meta, f):
    dati = {x: X_b[x] for x in X_b}
    dati["psi_h"] = psi_nuovo
    salva_stato(f, dati, meta)


def massa_di(f):
    import gravita_due_corpi_misure as GM
    X, _m = GM.leggi(f)
    return float(np.sum(np.abs(X["psi_h"]) ** 2))


def noto():
    import _presidio
    import gravita_due_corpi_misure as GM
    F1.avvia()
    _presidio.avvia(__file__)
    print("=" * 130)
    print("[M1330-B1] IL CASO NOTO DEL GIRO (la carta sez. 3-bis): la media = l'identita', il proiettore = l'identita' 12 x 12 -> lo stato k 3000 AL BIT")
    print("=" * 130)
    OK = {}

    def esito(che, ok, nota=""):
        OK[che] = bool(ok)
        print("  DEVE: %-100s %s %s" % (che, "PASSA" if ok else "### FALLISCE", nota))
    X, meta = GM.leggi(PARTENZA_1)
    n = X["psi_h"].size // 12
    massa = float(np.sum(np.abs(X["psi_h"]) ** 2))
    I12 = np.eye(12, dtype=complex)
    p_id = trasforma(X["psi_h"] * np.exp(1j * 0.0), I12, n, massa)
    esito("la media di un solo stato (theta 0) e il proiettore identita': psi_h = lo stato AL BIT", np.array_equal(p_id, X["psi_h"]), "max |d| %.1e" % float(np.max(np.abs(p_id - X["psi_h"]))))
    os.makedirs(DIR, exist_ok=True)
    f_id = os.path.join(DIR, "noto_identita.npz")
    if os.path.exists(f_id):
        os.remove(f_id)
        os.remove(f_id + ".sha1")
    nuova_partenza(X, p_id, dict(meta), f_id)
    Y = {}
    for nome, f in (("originale", PARTENZA_1), ("identita'", f_id)):
        F1.FS.stato_di = lambda sorgente, kstato, f=f: f
        with F1.TC.scena() as Z:
            C, _info, _dxy, _forma, _X = F1.FS.carica(Z, "K", 3000)
            Y[nome] = {x: Z["st"][x].copy() for x in Z["chiavi"]}
            Y[nome].update(A=C.campo.A.copy(), E=C.campo.E.copy())
            Z["metti"]()
    diversi = [x for x in Y["originale"] if not np.array_equal(Y["originale"][x], Y["identita'"][x])]
    esito("lo stato riscritto e ricaricato con FS.carica = l'originale ricaricato, TUTTE le chiavi e A, E AL BIT", not diversi, "diversi %s" % diversi)
    Q = leggi_Q()
    p_q = trasforma(X["psi_h"], Q, n, massa)
    d = float(np.max(np.abs(p_q - X["psi_h"])))
    esito("DEVE FALLIRE: lo stesso con Q_K: psi_h diverso", d > 0.0, "max |d| %.3e" % d)
    fall = [k for k, v in OK.items() if not v]
    print("### %d DEVE: %d PASSANO, %d FALLISCONO %s" % (len(OK), len(OK) - len(fall), len(fall), fall))
    return 0 if not fall else 1


def giro(g, f_part, Q, massa, MV, P0):
    import ripresa_F0_v2 as RF
    import gravita_due_corpi_misure as GM
    d = os.path.join(DIR, "giro_%d" % g)
    assert not os.path.exists(d), "%s c'e' gia': non si riscrive" % d
    os.makedirs(d)
    _G20, _ia, e0, MT = F1.CL.parametri()
    F1.FS.stato_di = lambda sorgente, kstato: f_part
    om, S, t1 = [], {0: None}, time.time()
    with F1.TC.scena() as Z:
        C, info, _dxy, _forma, _X = F1.FS.carica(Z, "K", 3000)
        n, s = Z["n"], float(Z["s"])
        N = np.ones(n)
        nodo, L = np.asarray(Z["mot"].inc.nodo), Z["L"]

        def salva(k):
            f = os.path.join(d, "stato_%06d.npz" % k)
            dati = {x: Z["st"][x] for x in Z["chiavi"]}
            dati.update(campo_A=C.campo.A, campo_E=C.campo.E)
            salva_stato(f, dati, dict(info, k=k, giro=g, partenza=f_part))
            return f
        ws = [F1.TT.misura(salva(0), nodo, n, L)[0]]
        print("### giro %d: la partenza %s; OGNI_GAUSS %d; k 0: w %.3f, la massa %.6f" % (g, f_part, MT.OGNI_GAUSS, ws[0], float(np.sum(np.abs(Z["st"]["psi_h"]) ** 2))))
        sys.stdout.flush()
        somma = np.zeros_like(Z["st"]["psi_h"])
        theta = 0.0
        S[0] = somma.copy()
        with RF.col_nucleo(MV, P0), MV.forma_esplicita("L-1"):
            assert MV.ATTIVA == "L-1" and MV.pezzi is P0
            for kk in range(1, K_GIRO + 1):
                prima = Z["st"]["psi_h"].copy()
                F1.CS.tick_var(Z["z"], C.campo, s, e0, N, False, 0)
                o = float(-np.angle(np.vdot(prima, Z["st"]["psi_h"])))
                om.append(o)
                theta += o
                somma += Z["st"]["psi_h"] * np.exp(1j * theta)
                if kk % MT.OGNI_GAUSS == 0:
                    C.residuo()
                if kk % OGNI == 0:
                    S[kk] = somma.copy()
                    ws.append(F1.TT.misura(salva(kk), nodo, n, L)[0])
                    if kk % 250 == 0:
                        print("    k %d: w %.3f, omega %+.7f (%.0f s)" % (kk, ws[-1], o, time.time() - t1))
                        sys.stdout.flush()
        Z["metti"]()
    mi = minimi(ws)
    esce = {"giro": g, "partenza": f_part, "w": ws, "omega": om, "minimi_k": [OGNI * i for i in mi]}
    print("### giro %d: i minimi locali stretti di w ai k %s; w min %.3f, max %.3f, medio %.3f: (max - min)/medio %.4f" % (
        g, esce["minimi_k"], min(ws), max(ws), float(np.mean(ws)), (max(ws) - min(ws)) / float(np.mean(ws))))
    if len(mi) < 2:
        esce["fermo"] = "meno di due minimi locali in %d tick" % K_GIRO
        f = os.path.join(d, "giro.json")
        open(f, "w", encoding="utf-8").write(json.dumps(esce))
        firma(f)
        print("### FERMO: %s" % esce["fermo"])
        return None
    ka, kb = OGNI * mi[0], OGNI * mi[1]
    psi_medio = (S[kb] - S[ka]) / float(kb - ka)
    X_b, meta_b = GM.leggi(os.path.join(d, "stato_%06d.npz" % kb))
    psi_nuovo = trasforma(psi_medio, Q, n, massa)
    f_nuova = os.path.join(d, "partenza_giro_%d.npz" % (g + 1))
    nuova_partenza(X_b, psi_nuovo, dict(meta_b, k=3000, giro=g + 1, periodo=[ka, kb]), f_nuova)
    esce.update(periodo=[ka, kb], partenza_nuova=f_nuova)
    f = os.path.join(d, "giro.json")
    open(f, "w", encoding="utf-8").write(json.dumps(esce))
    firma(f)
    print("### giro %d: il periodo (%d, %d]; la partenza del giro %d: %s (sha1 %s)" % (g, ka, kb, g + 1, f_nuova, sha1(f_nuova)[:8]))
    return f_nuova


def corsa():
    import _presidio
    F1.avvia()
    _presidio.avvia(__file__)
    MV, P0 = F1.TT.nucleo()
    Q = leggi_Q()
    massa = massa_di(PARTENZA_1)
    f = PARTENZA_1
    for g in range(1, GIRI + 1):
        f = giro(g, f, Q, massa, MV, P0)
        if f is None:
            return 2
    return 0


def lettura():
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "fondo_1c.py"))
    _presidio.avvia(__file__)
    print("=" * 130)
    print("[M1330-B] IL PUNTO FISSO (la carta sez. 3-bis): w per giro, il periodo, il criterio (w_max - w_min)/w_medio < %.0f%% sull'ultimo giro" % (100 * SOGLIA))
    print("=" * 130)
    G = []
    for g in range(1, GIRI + 1):
        f = os.path.join(DIR, "giro_%d" % g, "giro.json")
        if not os.path.exists(f + ".sha1"):
            break
        controlla(f)
        G.append(json.load(open(f, encoding="utf-8")))
    for x in G:
        ws = x["w"]
        print("  giro %d: w (k 0, 50, ..., 2000): %s" % (x["giro"], " ".join("%.2f" % w for w in ws)))
        print("          i minimi ai k %s; il periodo %s; (max - min)/medio %.4f%s" % (x["minimi_k"], x.get("periodo"), (max(ws) - min(ws)) / float(np.mean(ws)), ("; ### FERMO: " + x["fermo"]) if "fermo" in x else ""))
    if len(G) == GIRI and "fermo" not in G[-1]:
        ws = G[-1]["w"]
        r = (max(ws) - min(ws)) / float(np.mean(ws))
        print("### IL CRITERIO sull'ultimo giro: %.4f %s %.2f: %s" % (r, "<" if r < SOGLIA else ">=", SOGLIA, "PASSA" if r < SOGLIA else "NON PASSA"))
    else:
        print("### IL CRITERIO: NON MISURATO (%d giri su %d)" % (len(G), GIRI))
    if G:
        print("-" * 130)
        print("[M1330-B4] IL CONTROLLO NEGATIVO DI omega A RIPOSO ([M0140]): omega per tick del giro 1 (a riposo, k 3000 -> 5000) accanto alla caduta V2 x1 (M1658/c1_omega)")
        print("-" * 130)
        controlla(F_OMEGA_CADUTA)
        oc = np.array(json.load(open(F_OMEGA_CADUTA, encoding="utf-8"))["omega"])
        orip = np.array(G[0]["omega"])
        for k in range(0, K_GIRO, 250):
            print("  omega [%4d, %4d]: a riposo %+.7f; cadendo %+.7f; cadendo - riposo %+.2e" % (k + 1, k + 250, float(orip[k:k + 250].mean()), float(oc[k:k + 250].mean()), float(oc[k:k + 250].mean() - orip[k:k + 250].mean())))
        print("### a riposo: l'ultima finestra - la prima %+.3e; cadendo %+.3e" % (float(orip[-250:].mean() - orip[:250].mean()), float(oc[-250:].mean() - oc[:250].mean())))
    print("=" * 130)
    return 0


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("cosa", choices=("noto", "corsa", "lettura"))
    a = ap.parse_args(argv)
    return {"noto": noto, "corsa": corsa, "lettura": lettura}[a.cosa]()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
