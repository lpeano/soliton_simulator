# -*- coding: utf-8 -*-
r"""**IL TRIANGOLO CON `chi` -- LA V4** *(il triangolo IN FASE t000: il mandato di Luca [M0333] delle `03:33`; la carta sez. `6`: i vertici del t120, le fasi `0, 0, 0`; il resto la v3 riga per riga)*. **LA V3:** *(il gemello ruotato ESATTO t120r28: la decisione di Luca delle `02:22` e la correzione delle `02:31`; la carta sez. `4`: `V1 = V0 + (45, 21)`, `V2 = V0 + (24, 45)` nelle coordinate del codice, il baricentro portato su quello del t120; `--quale` per compat, costo, prova; il resto la v2 riga per riga)*. **LA V2:** *(la v1, `triangolo_chi.py`, `178b033b`, prendeva come vertici del t120r la COPPIA restituita da `triangolo_ruotato.vertici_ruotati` -- i vertici di partenza e i ruotati --: un errore dello script; qui i RUOTATI; il resto riga per riga, i comandi con `_v2`)*. **IL TITOLO DELLA V1:** **IL TRIANGOLO CON `chi`: LE TRE SFASATE SUL VUOTO E IL GEMELLO RUOTATO** *(il mandato di Luca `2026-11-21` `23:23`; la carta `doc/TASK_HISTORY/2026-11-21_triangolo_chi.md`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/triangolo_chi_v4.py compat --quale t000 > doc/referti_l2/triangolo_chi_v4_compat.txt
    E:\python\py3132\python.exe doc/referti_l2/triangolo_chi_v4.py costo --quale t000 > doc/referti_l2/triangolo_chi_v4_costo.txt
    E:\python\py3132\python.exe doc/referti_l2/triangolo_chi_v4.py prova --quale t000 > doc/referti_l2/triangolo_chi_v4_prova.txt
    E:\python\py3132\python.exe doc/referti_l2/triangolo_chi_v4.py tronco --quale t000 --fino 200000 --registro <voce>

**La scena** *(`mattone_triangolo.corsa` riga per riga fino al tick `0`, coi ganci di `triangolo_120` e di `triangolo_ruotato`: i file NON si toccano)*: la scena di S162 *(`mattone.scena(CORSA_162, T_162)`)*, **NIENTE bordo sorbente** *(Luca: `g_e = 0`)*, il vuoto fresco, **tre francobolli del mattone di `L 162`** *(`triangolo_video.francobollo_L162`)* ai vertici equilateri *(`triangolo_120.vertici`; il ruotato `triangolo_ruotato.vertici_ruotati`, `+15` gradi)*, `psi_h` per `exp(i 0, 120, 240 gradi)`, la materia per SOMMA, il vuoto per PRODOTTO; il campo `porto.campi` *(`A = 0`, `E` da Gauss)*.
**`chi`:** `chi_tick_v2` *(l'inerzia `f`, `kappa` il NUMERO)*; `m0` dallo stato di partenza del triangolo *(la regola del mattone)*; `chi` al profilo statico, `pi = 0`, `Theta = 0`. **Il tronco:** dopo ogni tick `scattati = |theta_a| >= 2 pi`: lo stato PRIMA della regola, `scatto.json`, l'uscita `10`; gli stati ogni `250`.
"""
import argparse
import glob
import json
import math
import os
import shutil
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_RADICE = os.path.dirname(os.path.dirname(_QUI))
for _p in (_QUI, os.path.join(_RADICE, "csv", "solitone"), os.path.join(_RADICE, "csv"), os.path.join(_RADICE, "primo_ordine")):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import chi_tick as CT  # noqa: E402
import chi_tick_v2 as CV2  # noqa: E402
import chi_mattone as CM  # noqa: E402

BASE = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "CHI", "triangolo")
QUALI = ("t120", "t120r28", "t000")                                  # ### V4: t000, il triangolo IN FASE
FASI_T000 = (0.0, 0.0, 0.0)                                          # ### V4: Luca 03:33
SCELTE = []                                                          # ### V3: le scene scelte con --quale
GIUSTI = ((45, 21), (24, 45))                                        # ### V3: Luca 02:31, le coordinate (m1, m2) del codice
SBAGLIATI = ((24, 21), (-21, 45))                                    # ### V3: Luca 02:22, la base a 60 gradi: il caso che DEVE FALLIRE
FASI = (0.0, 2.0 * math.pi / 3.0, 4.0 * math.pi / 3.0)
QUANTO, SCATTO = 2.0 * math.pi, 10
OGNI, OGNI_STATO = 50, 250
ESITI = []


def esito(che, ok, nota=""):
    ESITI.append((che, bool(ok)))
    print("  %-112s %s   %s" % (che, "PASSA" if ok else "### FALLISCE", nota))
    sys.stdout.flush()


def fine():
    print("-" * 130)
    for c, ok in ESITI:
        print("  DEVE: %-110s %s" % (c, "PASSA" if ok else "### FALLISCE"))
    print("=" * 130)
    return 0 if all(ok for _c, ok in ESITI) else 1


def moduli():
    import mattone as MT
    import mattone_triangolo as MTR
    import triangolo_120 as T1
    import triangolo_ruotato as TRU
    import triangolo_video as TV
    import porto as PO
    return MT, MTR, T1, TRU, TV, PO


def vertici_r28(V120, L, vettori=GIUSTI):
    """### V3: `V0` = il primo vertice del t120, `V1 = V0 + v1`, `V2 = V0 + v2`, traslati col baricentro su quello del t120 *(al nodo piu' vicino)*. `(vertici, info)`."""
    MT = moduli()[0]
    from solitone import toro as TO
    A1, A2 = TO.vettori()
    V0 = [int(V120[0][0]), int(V120[0][1])]
    W = [V0, [V0[0] + vettori[0][0], V0[1] + vettori[0][1]], [V0[0] + vettori[1][0], V0[1] + vettori[1][1]]]
    b120 = np.mean(np.array([[float(v[0]), float(v[1])] for v in V120]), axis=0)
    bW = np.mean(np.array(W, dtype=float), axis=0)
    tr = [int(round(float(x))) for x in b120 - bW]
    W = [[(w[0] + tr[0]) % L, (w[1] + tr[1]) % L] for w in W]
    lati = [MT.distanza(L, W[a], W[b]) for a, b in ((0, 1), (1, 2), (2, 0))]

    def cart(v):
        p = float(v[0]) * np.asarray(A1, dtype=float) + float(v[1]) * np.asarray(A2, dtype=float)
        return p[:2]

    def verso(u, v):
        p, q = cart(u), cart(v)
        return float(p[0] * q[1] - p[1] * q[0])

    d1 = (V120[1][0] - V120[0][0], V120[1][1] - V120[0][1])
    d2 = (V120[2][0] - V120[0][0], V120[2][1] - V120[0][1])
    p1 = cart(vettori[0])
    ang = math.degrees(math.atan2(p1[1], p1[0]))
    dal_asse = min(abs(((ang - 60.0 * j) + 180.0) % 360.0 - 180.0) for j in range(6))
    buoni = all(x % 3 == 0 for x in tr) and all(c % 3 == 0 for v in vettori for c in v)
    return W, {"vettori": [list(v) for v in vettori], "traslazione": tr, "esatta": bool(np.all(b120 - bW == np.round(b120 - bW))), "baricentro_120": [float(x) for x in b120],
               "baricentro": [float(x) for x in bW + np.array(tr)], "lati": lati, "verso": verso(vettori[0], vettori[1]), "verso_120": verso(d1, d2), "angolo": ang, "dal_asse": dal_asse, "buoni": buoni}


def prepara(Z, quale):
    """### lo stato del tick `0` *(le righe di `mattone_triangolo.corsa`)*, SENZA bordo; `(C, info)`."""
    MT, MTR, T1, TRU, TV, PO = moduli()
    rho_c, e, t0 = MT.rho_c_assoluto(), MT.PB.E_DECISO, MT.G2.T0
    st, L = Z["st"], Z["L"]
    c0 = Z["bordo"]["c0"]
    fr = TV.francobollo_L162(0)
    if quale in ("t120", "t000"):                                    # ### V4: t000 sui vertici del t120
        V = T1.vertici(c0, fr, L)
    else:                                                              # ### V3: il gemello ESATTO (Luca 02:22, 02:31)
        V, I28 = vertici_r28(T1.vertici(c0, fr, L), L)
        assert I28["buoni"], "i vertici del t120r28 non sono sui nodi buoni del francobollo (la traslazione %s): FERMO" % I28["traslazione"]
    centri = [list(v) for v in V]
    Z["g_e"] = np.zeros_like(Z["g_e"])                                 # ### Luca: NIENTE bordo sorbente
    MT.vuoto_fresco(Z, t0)
    vuoto_psi = float(np.max(np.abs(st["psi_h"])))
    phi_F3 = st["phi_h"].copy()
    vuoto = {x: st[x].copy() for x in Z["chiavi"]}
    soli = []
    for j, c in enumerate(centri):
        for x in Z["chiavi"]:
            st[x][...] = vuoto[x]
        MT.incolla(Z, fr, c, True)
        fasi = FASI_T000 if quale == "t000" else FASI                    # ### V4
        if fasi[j] != 0.0:
            st["psi_h"][...] = st["psi_h"] * np.exp(1j * fasi[j])
        soli.append((st["psi_h"].copy(), st["phi_h"].copy()))
    psi = soli[0][0].copy()
    phi = soli[0][1].copy()
    for s_ in soli[1:]:
        psi = psi + s_[0]
        phi = phi * (s_[1] / phi_F3)
    st["psi_h"][...] = psi
    st["phi_h"][...] = phi
    C = PO.campi(Z, rho_c, e)
    lati = [MT.distanza(L, centri[a], centri[b]) for a, b in ((0, 1), (1, 2), (2, 0))]
    return C, {"quale": quale, "centri": centri, "lati": lati, "vuoto_psi": vuoto_psi, "masse_soli": [float(np.sum(np.abs(s_[0]) ** 2)) for s_ in soli],
               "francobollo": fr.get("file", "L162_MGU_03000"), "c0": list(c0), "fasi_gradi": [math.degrees(x) for x in (FASI_T000 if quale == "t000" else FASI)]}


def scena():
    MT = moduli()[0]
    return MT.scena(MT.CORSA_162, MT.T_162)


def compat():
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "chi_tick_v2.py"))
    _presidio.avvia(__file__)
    MT, MTR, T1, TRU, TV, PO = moduli()
    print("=" * 130)
    print("P0, LA COMPATIBILITA' DEL TRIANGOLO CON CHI (Luca 2026-11-21 23:23): sola lettura, nessun tick")
    print("=" * 130)
    for quale in SCELTE:
        with scena() as Z:
            print("### %s: la scena %s (T %d): L %d, n %d, m %d; s %r; rho_c %r, e %r; la forma %s; il bordo della scena R_A %.3f, c0 %s; il bordo nelle corse con chi: NESSUNO (g_e = 0)" % (
                quale, MT.CORSA_162, MT.T_162, Z["L"], Z["mot"].inc.n, Z["mot"].inc.m, float(Z["s"]), MT.rho_c_assoluto(), MT.PB.E_DECISO, MT.PB.FORMA, Z["bordo"]["R_A"], Z["bordo"]["c0"]))
            C, info = prepara(Z, quale)
            print("    i vertici %s; i lati %s; il vuoto senza materia prima dell'incollatura %s (max |psi_h| %.1e); le masse dei francobolli da soli %s" % (
                info["centri"], ["%.4f" % x for x in info["lati"]], info["vuoto_psi"] == 0.0, info["vuoto_psi"], ["%.12e" % x for x in info["masse_soli"]]))
            print("    le fasi dei tre francobolli %s gradi" % ["%.4f" % x for x in info["fasi_gradi"]])      # ### V4
            if quale == "t000":                                        # ### V4: i lati e le fasi
                esito("t000: i tre lati 39.0000 e i vertici del t120", all(abs(x - 39.0) < 1e-9 for x in info["lati"]) and [list(map(int, v)) for v in info["centri"]] == [[74, 68], [113, 68], [113, 107]], ", ".join("%.6f" % x for x in info["lati"]))
                esito("t000: le tre fasi 0, 0, 0", info["fasi_gradi"] == [0.0, 0.0, 0.0])
            if quale == "t120r28":                                     # ### V3: i lati, il baricentro, il verso, l'angolo; il caso coi vettori SBAGLIATI
                V120 = T1.vertici(Z["bordo"]["c0"], TV.francobollo_L162(0), Z["L"])
                _W, I = vertici_r28(V120, Z["L"])
                _Ws, Is = vertici_r28(V120, Z["L"], SBAGLIATI)
                print("    il t120r28: i vettori %s dal vertice di partenza del t120 %s; la traslazione %s (esatta %s); il baricentro %s (quello del t120 %s); i lati con la norma del codice %s; il verso %+.4f (il t120 %+.4f); l'angolo di V1 - V0 %.4f gradi, dall'asse piu' vicino %.4f; i nodi buoni %s" % (
                    I["vettori"], list(V120[0]), I["traslazione"], I["esatta"], I["baricentro"], I["baricentro_120"], ["%.4f" % x for x in I["lati"]], I["verso"], I["verso_120"], I["angolo"], I["dal_asse"], I["buoni"]))
                print("    coi vettori SBAGLIATI %s (la base a 60 gradi): i lati %s" % (Is["vettori"], ["%.4f" % x for x in Is["lati"]]))
                esito("t120r28: i tre lati 39.0000 con la norma del codice", all(abs(x - 39.0) < 1e-9 for x in I["lati"]), ", ".join("%.6f" % x for x in I["lati"]))
                esito("t120r28 DEVE FALLIRE: coi vettori sbagliati i lati NON sono 39", not all(abs(x - 39.0) < 1e-9 for x in Is["lati"]), ", ".join("%.4f" % x for x in Is["lati"]))
                esito("t120r28: lo stesso verso di giro del t120 e i nodi buoni del francobollo", I["verso"] * I["verso_120"] > 0.0 and I["buoni"])
                esito("t120r28: i vertici di prepara sono quelli stampati", [list(map(int, v)) for v in info["centri"]] == [list(map(int, v)) for v in _W])
            s_a = np.asarray(C.campo.s_a)
            print("    il campo U(1): s_a uniforme %s, %r; w %r; il Laplaciano di chi sul grafo della scena (n %d)" % (bool(np.all(s_a == s_a[0])), float(s_a[0]), float(C.campo.w[0]), Z["mot"].inc.n))
            P, m0 = CV2.parametri_v2(Z, None, None, MT.rho_c_assoluto(), MT.PB.E_DECISO, MT.G2.T0, float(Z["s"]), float(C.e0), stato={x: Z["st"][x] for x in Z["chiavi"]})
            print("    i parametri di chi (v2): %r; m0 dello stato di partenza %+.12e" % (P, m0))
            Z["metti"]()
    return fine()                                                      # ### V3: gli esiti del t120r28


def corsa(quale, k_fino, reg, d_out, f_da=None, scatta=True, v1=False, energia_ogni=None):
    """### il tick con `chi` sul triangolo, da `k 0` *(prepara)* o da `f_da`. `(codice, k, fine, serie_H)`."""
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "chi_tick_v2.py"))
    _presidio.avvia(__file__)
    MT, MTR, T1, TRU, TV, PO = moduli()
    from solitone import _registro_corse as RC
    rho_c, e, t0 = MT.rho_c_assoluto(), MT.PB.E_DECISO, MT.G2.T0
    os.makedirs(d_out, exist_ok=True)
    codice, serie_H = 0, []
    t00 = time.time()
    with scena() as Z:
        mot = Z["mot"]
        n, m = mot.inc.n, mot.inc.m
        s = float(Z["s"])
        Lp = CT.Laplaciano(mot)
        if f_da is None:
            C, info = prepara(Z, quale)
            P, m0 = CV2.parametri_v2(Z, None, None, rho_c, e, t0, s, float(C.e0), stato={x: Z["st"][x].copy() for x in Z["chiavi"]})
            Z["g_e"] = np.zeros_like(Z["g_e"])                         # ### NIENTE bordo, anche dopo metti
            X = CT.nuovo_X(n, m, CT.chi_statico(mot, Z["st"], Z["par"], P, Lp, m0))
            meta = dict(info, parametri={"kappa": P.kappa, "c0": P.c0, "m0": m0, "c2": P.c2, "m2": P.m2, "e0": P.e0, "s": P.s, "f": P.f})
            k_da = 0
            EX = {x: [] for x in ("k", "M", "H", "H_chi", "chi_medio", "max_theta", "picco")}
        else:
            assert open(f_da + ".sha1", encoding="utf-8").read().split()[0] == CM.sha1(f_da), "lo sha1 di %s NON coincide: la ripresa RIFIUTA" % f_da
            with np.load(f_da) as d:
                Xf = {x: d[x].copy() for x in d.files}
            meta = json.loads(str(Xf.pop("meta")))
            Z["metti"]({x: Xf[x] for x in Z["chiavi"]})
            Z["g_e"] = np.zeros_like(Z["g_e"])
            C = PO.campi(Z, rho_c, e, Xf["campo_A"], Xf["campo_E"])
            pm = meta["parametri"]
            P = CV2.Parametri2(pm["kappa"], pm["c0"], pm["s"], pm["e0"], pm["f"], pm["c2"], pm["m2"])
            m0 = pm["m0"]
            X = {q: Xf[q] for q in CT.CHIAVI_CHI}
            k_da = int(meta["k"])
            sfx = os.path.basename(f_da)[6:-4]
            with np.load(os.path.join(os.path.dirname(f_da), "serie_%s.npz" % sfx)) as d:
                EX = {x: list(d[x]) for x in d.files}
        if v1:
            P = CT.Parametri(P.kappa, P.c0, P.s, P.e0, P.c2, P.m2)
        tick = CT.tick_chi if v1 else CV2.tick_chi_v2
        energia = CT.energia_chi if v1 else CV2.energia_chi_v2
        print("### IL TRIANGOLO %s CON CHI (%s): da %s fino a k %d; i parametri %r; m0 %+.12e; gli stati in %s" % (
            quale, "il passo di OGGI" if v1 else "il passo v2", os.path.basename(f_da) if f_da else "k 0 (prepara)", k_fino, P, m0, d_out))
        sys.stdout.flush()

        def salva(k, fz, scatto=False):
            dati = {x: Z["st"][x] for x in Z["chiavi"]}
            dati.update(campo_A=C.campo.A, campo_E=C.campo.E, **{q: X[q] for q in CT.CHIAVI_CHI})
            np.savez(fz, meta=np.array(json.dumps(dict(meta, k=k, tronco_scatto=scatto))), **dati)
            h = CM.sha1(fz)
            with open(fz + ".sha1", "w", encoding="utf-8") as fh:
                fh.write(h + "\n")
            if not scatto:
                np.savez(os.path.join(d_out, "serie_%s.npz" % os.path.basename(fz)[6:-4]), **{q: np.array(v_) for q, v_ in EX.items()})
            return h

        def misura(k):
            H, Hc = energia(mot, Z["st"], Z["par"], P, Lp, X, C.campo)
            rh = CT.rho_di(mot, Z["st"])
            for x, v_ in (("k", k), ("M", float(np.sum(np.abs(Z["st"]["psi_h"]) ** 2))), ("H", H), ("H_chi", Hc), ("chi_medio", float(X["chi"].mean())),
                          ("max_theta", float(np.max(np.abs(X["theta_a"])))), ("picco", float(rh.max()))):
                EX[x].append(v_)
            return H

        t1 = t_tappa = time.time()
        k = k_da
        if f_da is None:
            misura(0)
        for k in range(k_da + 1, k_fino + 1):
            tick(Z["z"], C.campo, P, Lp, X)
            if scatta:
                sc = np.nonzero(np.abs(X["theta_a"]) >= QUANTO)[0]
                if sc.size:
                    fp = os.path.join(d_out, "prima_nascita_%06d.npz" % k)
                    h = salva(k, fp, scatto=True)
                    with open(os.path.join(d_out, "scatto.json"), "w", encoding="utf-8") as fh:
                        json.dump({"k": k, "file": fp, "sha1": h, "archi": [int(x) for x in sc[:20]], "quanti": int(sc.size)}, fh)
                    print("### IL PRIMO SCATTO a k %d (%d archi, il primo %d): %s sha1 %s; il tronco esce (%d)" % (k, sc.size, int(sc[0]), os.path.basename(fp), h[:8], SCATTO))
                    if reg:
                        RC.tappa(reg, "IL PRIMO SCATTO a k %d: %s sha1 %s" % (k, os.path.basename(fp), h[:8]))
                    codice = SCATTO
                    break
            if k % MT.OGNI_GAUSS == 0:
                C.residuo()
            if k % OGNI == 0:
                H = misura(k)
                if k % 250 == 0:
                    print("    k %6d  la massa %.12e  H %+.12e  H_chi %+.4e  max|Theta| %.4f  il picco %.4e  (%.0f s)" % (k, EX["M"][-1], H, EX["H_chi"][-1], EX["max_theta"][-1], EX["picco"][-1], time.time() - t00))
                    sys.stdout.flush()
            if energia_ogni and k % energia_ogni == 0:
                serie_H.append((k, energia(mot, Z["st"], Z["par"], P, Lp, X, C.campo)[0]))
            if k % OGNI_STATO == 0 or k == k_fino:
                hh = salva(k, os.path.join(d_out, "stato_%06d.npz" % k))
                if k % OGNI_STATO == 0:
                    print("    [stato] k %d sha1 %s" % (k, hh[:8]))
            adesso = time.time()
            if reg and adesso - t_tappa >= 3600.0:
                RC.tappa(reg, "k %d; %.3f s per tick; max |Theta| %.4f" % (k, (adesso - t1) / max(1, k - k_da), float(np.max(np.abs(X["theta_a"])))))
                t_tappa = adesso
        fin = ({x: Z["st"][x].copy() for x in Z["chiavi"]}, C.campo.A.copy(), C.campo.E.copy(), CT.copia_X(X))
        Z["metti"]()
    print("### %d tick in %.0f s (%.3f s per tick); il codice %d" % (k - k_da, time.time() - t1, (time.time() - t1) / max(1, k - k_da), codice))
    return codice, k, fin, serie_H


def costo():
    print("=" * 130)
    print("P1, IL COSTO DEL TICK CON CHI SUL TRIANGOLO (Luca 2026-11-21 23:23): 50 tick per scena")
    print("=" * 130)
    for quale in SCELTE:
        corsa(quale, 50, None, os.path.join(BASE, "costo", quale), scatta=False)
    return 0


def uguali(a, b):
    st1, A1, E1, X1 = a
    st2, A2, E2, X2 = b
    return [x for x in st1 if not np.array_equal(st1[x], st2[x])] + [x for x, p, q in (("A", A1, A2), ("E", E1, E2)) if not np.array_equal(p, q)] + [q for q in CT.CHIAVI_CHI if not np.array_equal(X1[q], X2[q])]


def prova():
    print("=" * 130)
    print("P2, LA PROVA BREVE DEL TRIANGOLO CON CHI (Luca 2026-11-21 23:23): 250 tick di fila contro 125 + salva + riprendi + 125; un byte; l'energia")
    print("=" * 130)
    for quale in SCELTE:
        d = os.path.join(BASE, "prova", quale)
        if os.path.isdir(d):
            shutil.rmtree(d)
        _c, _k, fila, H2 = corsa(quale, 250, None, os.path.join(d, "fila"), energia_ogni=50)
        corsa(quale, 125, None, os.path.join(d, "spezza"))
        fm = os.path.join(d, "spezza", "stato_000125.npz")
        _c, _k, rip, _h = corsa(quale, 250, None, os.path.join(d, "spezza"), f_da=fm)
        dd = uguali(fila, rip)
        print("### %s: 250 tick di fila contro la ripresa da %s: %s" % (quale, os.path.basename(fm), "AL BIT (psi, phi, A, E, chi, pi, Theta)" if not dd else "### DIVERSE: %s" % dd))
        esito("P2 %s: la ripresa AL BIT su ogni chiave" % quale, not dd)
        fr = os.path.join(d, "rotto", "stato_000125.npz")
        os.makedirs(os.path.dirname(fr), exist_ok=True)
        for x in ("stato_000125.npz", "stato_000125.npz.sha1", "serie_000125.npz"):
            shutil.copyfile(os.path.join(d, "spezza", x), os.path.join(d, "rotto", x))
        with open(fr, "r+b") as fh:
            fh.seek(os.path.getsize(fr) // 2)
            b = fh.read(1)
            fh.seek(os.path.getsize(fr) // 2)
            fh.write(bytes([b[0] ^ 0x01]))
        rif = False
        try:
            corsa(quale, 126, None, os.path.join(d, "rotto"), f_da=fr)
        except AssertionError as ex:
            rif = "sha1" in str(ex)
            print("### %s: un byte cambiato: %s" % (quale, ex))
        esito("P2 %s DEVE FALLIRE: un byte cambiato -> la ripresa RIFIUTA" % quale, rif)
        _c, _k, _f, H1 = corsa(quale, 250, None, os.path.join(d, "oggi"), v1=True, energia_ogni=50)
        h2, h1 = np.array([h for _k, h in H2]), np.array([h for _k, h in H1])
        d2 = float(np.max(np.abs(h2 - h2[0]))) / abs(h2[0])
        d1 = float(np.max(np.abs(h1 - h1[0]))) / abs(h1[0])
        print("### %s: la deriva relativa massima di H in 250 tick: il passo v2 %.3e, il passo di oggi %.3e" % (quale, d2, d1))
        esito("P2 %s: l'energia con chi v2 entro 10 volte la deriva del passo di oggi + 1e-12 (il criterio di K5)" % quale, d2 <= 10.0 * d1 + 1e-12, "%.2e" % d2)
    return fine()


def tronco(quale, k_fino, reg):
    d = os.path.join(BASE, quale)
    fs = sorted((f for f in glob.glob(os.path.join(d, "stato_*.npz")) if os.path.exists(f + ".sha1")), key=lambda f: int(os.path.basename(f)[6:-4]))
    f_da = fs[-1] if fs else None
    cod, _k, _f, _h = corsa(quale, k_fino, reg, d, f_da=f_da)
    return cod


def main(argv):
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    for x in ("compat", "costo", "prova"):
        q = sub.add_parser(x)
        q.add_argument("--quale", choices=QUALI, nargs="+", required=True)      # ### V3
    t = sub.add_parser("tronco")
    t.add_argument("--quale", choices=QUALI, required=True)
    t.add_argument("--fino", type=int, required=True)
    t.add_argument("--registro")
    x = ap.parse_args(argv)
    if x.cmd == "tronco":
        return tronco(x.quale, x.fino, x.registro)
    SCELTE[:] = x.quale
    return {"compat": compat, "costo": costo, "prova": prova}[x.cmd]()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
