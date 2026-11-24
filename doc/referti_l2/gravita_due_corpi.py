# -*- coding: utf-8 -*-
r"""**[M0417-K] IL TEST PULITO DELLA GRAVITA': DUE MATTONI, `chi` ACCESO CONTRO `chi` SPENTO -- LA SCENA, LA CORSA, IL CASO NOTO** *(il mandato di Luca `2026-11-22` `04:17`; la carta `doc/TASK_HISTORY/2026-11-22_gravita_due_corpi.md`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/gravita_due_corpi.py caso_noto > doc/referti_l2/gravita_due_corpi_caso_noto.txt
    E:\python\py3132\python.exe doc/referti_l2/gravita_due_corpi.py corsa --scena F --chi on --fino 3000 --registro <voce>      (F o S; on o off)

**La scena** *(le righe di `triangolo_chi_v4.prepara` con DUE francobolli)*: il toro S162, il vuoto fresco, `L162_MGU_03000` in `V0` *(il nodo buono piu' vicino a `(L/2 - 19.5, L/2)`)* e in `V1 = V0 + (39, 0)`; le fasi (F) `0, 0` o (S) `0, 120`; la materia per SOMMA, il vuoto per PRODOTTO; `porto.campi`; `g_e = 0`. **`chi`:** `chi_tick_v2.parametri_v2` *(`kappa` il numero, `c0 = kappa m0`, `m0` della coppia)*, `chi` al profilo statico di «on»; **«off»:** gli stessi parametri con `kappa = 0` e lo STESSO `c0`. **Il caso noto:** con `kappa = 0`, `50` tick del tick v2 contro `50` tick del tick U con `cs = s` *(le stesse righe senza `chi`)*, AL BIT; DEVE FALLIRE con `kappa` vero.
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
import triangolo_chi_v4 as TC  # noqa: E402
import chi_tick as CT  # noqa: E402
import chi_tick_v2 as CV2  # noqa: E402

BASE = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "CHI", "due_corpi")
FASI = {"F": (0.0, 0.0), "S": (0.0, 2.0 * math.pi / 3.0)}
DIST = (39, 0)
OGNI_STATO = 250
ESITI = []


def esito(che, ok, nota=""):
    ESITI.append((che, bool(ok)))
    print("  %-112s %s   %s" % (che, "PASSA" if ok else "### FALLISCE", nota))
    sys.stdout.flush()


def vertici(fr, L):
    from solitone import toro as TO
    A1, A2 = TO.vettori()
    tgt = (0.5 * L - 0.5 * DIST[0], 0.5 * L - 0.5 * DIST[1])
    best = None
    for n1 in range(int(math.floor(tgt[0])) - 3, int(math.floor(tgt[0])) + 4):
        for n2 in range(int(math.floor(tgt[1])) - 3, int(math.floor(tgt[1])) + 4):
            if (n1 - fr["centro"][0]) % 3 or (n2 - fr["centro"][1]) % 3:
                continue
            p = (n1 - tgt[0]) * np.asarray(A1, float) + (n2 - tgt[1]) * np.asarray(A2, float)
            dd = float(np.hypot(p[0], p[1]))
            if best is None or dd < best[0]:
                best = (dd, [n1, n2])
    V0 = best[1]
    assert DIST[0] % 3 == 0 and DIST[1] % 3 == 0, "il vettore della coppia non porta su un nodo buono"
    return [V0, [V0[0] + DIST[0], V0[1] + DIST[1]]], tgt


def prepara_coppia(Z, scena):
    """### lo stato del tick `0` della coppia, SENZA bordo; `(C, info)`."""
    MT, MTR, T1, TRU, TV, PO = TC.moduli()
    rho_c, e, t0 = MT.rho_c_assoluto(), MT.PB.E_DECISO, MT.G2.T0
    st, L = Z["st"], Z["L"]
    fr = TV.francobollo_L162(0)
    centri, tgt = vertici(fr, L)
    Z["g_e"] = np.zeros_like(Z["g_e"])
    MT.vuoto_fresco(Z, t0)
    vuoto_psi = float(np.max(np.abs(st["psi_h"])))
    phi_F3 = st["phi_h"].copy()
    vuoto = {x: st[x].copy() for x in Z["chiavi"]}
    soli = []
    for j, c in enumerate(centri):
        for x in Z["chiavi"]:
            st[x][...] = vuoto[x]
        MT.incolla(Z, fr, c, True)
        if FASI[scena][j] != 0.0:
            st["psi_h"][...] = st["psi_h"] * np.exp(1j * FASI[scena][j])
        soli.append((st["psi_h"].copy(), st["phi_h"].copy()))
    st["psi_h"][...] = soli[0][0] + soli[1][0]
    st["phi_h"][...] = soli[0][1] * (soli[1][1] / phi_F3)
    C = PO.campi(Z, rho_c, e)
    return C, {"scena": scena, "centri": centri, "bersaglio": list(tgt), "distanza": MT.distanza(L, centri[0], centri[1]), "vuoto_psi": vuoto_psi,
               "fasi_gradi": [math.degrees(x) for x in FASI[scena]], "masse_soli": [float(np.sum(np.abs(s_[0]) ** 2)) for s_ in soli]}


def impronta(Z, C, X):
    """### lo sha1 dello stato fisico *(le chiavi, `A`, `E`, `chi`, `pi`, `Theta`, in quest'ordine; il `meta` escluso)*."""
    h = hashlib.sha1()
    for x in Z["chiavi"]:
        h.update(np.ascontiguousarray(Z["st"][x]).tobytes())
    for a in (C.campo.A, C.campo.E, X["chi"], X["pi"], X["theta_a"]):
        h.update(np.ascontiguousarray(a).tobytes())
    return h.hexdigest()


def parametri(Z, C, chi_on):
    MT = TC.moduli()[0]
    P, m0 = CV2.parametri_v2(Z, None, None, MT.rho_c_assoluto(), MT.PB.E_DECISO, MT.G2.T0, float(Z["s"]), float(C.e0), stato={x: Z["st"][x].copy() for x in Z["chiavi"]})
    Pon = P
    if not chi_on:
        P = CV2.Parametri2(0.0, P.c0, P.s, P.e0, P.f, P.c2, P.m2)              # ### off: kappa = 0, lo STESSO c0
    return P, Pon, m0


def tick_U(z, campo, s):
    """### il tick U con `cs = s` uniforme: le righe di `tick_chi_v2` SENZA `chi` *(il riferimento del caso noto)*."""
    import composizione as CM
    import tick as TK
    from solitone import _u1_oggi as UO
    mot, st, par = z["mot"], z["st"], z["par"]
    campo.spinta(0.5)
    mot.cs = np.full(mot.inc.n, float(s))
    mot.lambda_c = None
    with UO.avvolto(mot, campo, True):
        TK.percorri_tick(st, mot, par, (), None, len(CM.ORDINE))
    campo.spinta(0.5)


def caso_noto():
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "chi_tick_v2.py"))
    _presidio.avvia(os.path.join(_QUI, "triangolo_chi_v4.py"))
    _presidio.avvia(__file__)
    print("=" * 130)
    print("[M0417-K] IL CASO NOTO: kappa = 0, 50 tick del tick v2 contro 50 tick del tick U con cs = s (la materia, A, E AL BIT); DEVE FALLIRE con kappa vero")
    print("=" * 130)
    out = {}
    with TC.scena() as Z:
        mot = Z["mot"]
        n, m = mot.inc.n, mot.inc.m
        Lp = CT.Laplaciano(mot)
        for nome in ("v2 kappa 0", "U cs = s", "v2 kappa vero"):
            C, info = prepara_coppia(Z, "F")
            P, Pon, m0 = parametri(Z, C, nome == "v2 kappa vero")
            X = CT.nuovo_X(n, m, CT.chi_statico(mot, Z["st"], Z["par"], Pon, Lp, m0))
            print("### %s: i vertici %s (il bersaglio %s), la distanza %.4f; le fasi %s; kappa %r, c0 %r, f %r; l'impronta di partenza %s" % (
                nome, info["centri"], ["%.2f" % x for x in info["bersaglio"]], info["distanza"], info["fasi_gradi"], P.kappa, P.c0, P.f, impronta(Z, C, X)[:12]))
            for _t in range(50):
                if nome == "U cs = s":
                    tick_U(Z["z"], C.campo, P.s)
                else:
                    CV2.tick_chi_v2(Z["z"], C.campo, P, Lp, X)
            cs = np.array(mot.cs, dtype=float, copy=True)
            out[nome] = ({x: Z["st"][x].copy() for x in Z["chiavi"]}, C.campo.A.copy(), C.campo.E.copy(), cs, float(np.max(np.abs(X["theta_a"]))))
            Z["metti"]()
    s = float(Pon.s)

    def diverse(a, b):
        return [x for x in a[0] if not np.array_equal(a[0][x], b[0][x])] + [q for q, p, r in (("A", a[1], b[1]), ("E", a[2], b[2])) if not np.array_equal(p, r)]
    d0 = diverse(out["v2 kappa 0"], out["U cs = s"])
    d1 = diverse(out["v2 kappa vero"], out["U cs = s"])
    cs_ok = bool(np.all(out["v2 kappa 0"][3] == s))
    print("### v2 kappa 0 contro U: %s; cs = s esatto %s; max |Theta| %.3e" % ("AL BIT su ogni chiave, A, E" if not d0 else "### DIVERSE: %s" % d0, cs_ok, out["v2 kappa 0"][4]))
    print("### v2 kappa vero contro U: le chiavi diverse %s" % d1)
    esito("K: con kappa = 0 il tick v2 = il tick U con cs = s, AL BIT (la materia, A, E), cs = s esatto", not d0 and cs_ok)
    esito("K DEVE FALLIRE: con kappa vero la materia diversa dopo 50 tick", "psi_h" in d1)
    print("-" * 130)
    for c, ok in ESITI:
        print("  DEVE: %-110s %s" % (c, "PASSA" if ok else "### FALLISCE"))
    print("=" * 130)
    return 0 if all(ok for _c, ok in ESITI) else 1


def corsa(scena, chi_on, k_fino, reg):
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "chi_tick_v2.py"))
    _presidio.avvia(os.path.join(_QUI, "triangolo_chi_v4.py"))
    _presidio.avvia(__file__)
    from solitone import _registro_corse as RC
    MT = TC.moduli()[0]
    nome = "%s-%s" % (scena, "on" if chi_on else "off")
    d_out = os.path.join(BASE, nome)
    os.makedirs(d_out, exist_ok=True)
    with TC.scena() as Z:
        mot = Z["mot"]
        n, m = mot.inc.n, mot.inc.m
        Lp = CT.Laplaciano(mot)
        C, info = prepara_coppia(Z, scena)
        P, Pon, m0 = parametri(Z, C, chi_on)
        X = CT.nuovo_X(n, m, CT.chi_statico(mot, Z["st"], Z["par"], Pon, Lp, m0))
        meta = dict(info, corsa=nome, parametri={"kappa": P.kappa, "c0": P.c0, "m0": m0, "c2": P.c2, "m2": P.m2, "e0": P.e0, "s": P.s, "f": P.f, "kappa_on": Pon.kappa})
        print("### %s: i vertici %s, la distanza %.4f, le fasi %s; i parametri %r; m0 %+.12e; L'IMPRONTA DELLO STATO DI PARTENZA %s; gli stati in %s" % (
            nome, info["centri"], info["distanza"], info["fasi_gradi"], P, m0, impronta(Z, C, X), d_out))
        sys.stdout.flush()

        def salva(k):
            fz = os.path.join(d_out, "stato_%06d.npz" % k)
            dati = {x: Z["st"][x] for x in Z["chiavi"]}
            dati.update(campo_A=C.campo.A, campo_E=C.campo.E, **{q: X[q] for q in CT.CHIAVI_CHI})
            np.savez(fz, meta=np.array(json.dumps(dict(meta, k=k))), **dati)
            h = hashlib.sha1(open(fz, "rb").read()).hexdigest()
            with open(fz + ".sha1", "w", encoding="utf-8") as fh:
                fh.write(h + "\n")
            return h

        print("    [stato] k 0 sha1 %s" % salva(0)[:8])
        t1 = t_tappa = time.time()
        for k in range(1, k_fino + 1):
            CV2.tick_chi_v2(Z["z"], C.campo, P, Lp, X)
            if k % MT.OGNI_GAUSS == 0:
                C.residuo()
            if k % OGNI_STATO == 0 or k == k_fino:
                print("    [stato] k %d sha1 %s  max|Theta| %.4f  (%.0f s)" % (k, salva(k)[:8], float(np.max(np.abs(X["theta_a"]))), time.time() - t1))
                sys.stdout.flush()
            if reg and time.time() - t_tappa >= 3600.0:
                RC.tappa(reg, "k %d; %.3f s per tick" % (k, (time.time() - t1) / k))
                t_tappa = time.time()
        Z["metti"]()
    print("### %d tick in %.0f s (%.3f s per tick)" % (k_fino, time.time() - t1, (time.time() - t1) / k_fino))
    return 0


def main(argv):
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("caso_noto")
    c = sub.add_parser("corsa")
    c.add_argument("--scena", choices=("F", "S"), required=True)
    c.add_argument("--chi", choices=("on", "off"), required=True)
    c.add_argument("--fino", type=int, required=True)
    c.add_argument("--registro")
    x = ap.parse_args(argv)
    if x.cmd == "caso_noto":
        return caso_noto()
    return corsa(x.scena, x.chi == "on", x.fino, x.registro)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
