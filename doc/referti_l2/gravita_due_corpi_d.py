# -*- coding: utf-8 -*-
r"""**[M1017-K] I DUE MATTONI CON LA DISTANZA COME ARGOMENTO -- LA SCENA, IL CASO NOTO, LA CORSA** *(il mandato di Luca [M1017] del `2026-11-22`; la carta `doc/TASK_HISTORY/2026-11-22_gravita_60.md`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/gravita_due_corpi_d.py caso_noto > doc/referti_l2/gravita_60_caso_noto.txt
    E:\python\py3132\python.exe doc/referti_l2/gravita_due_corpi_d.py corsa --d 60 --chi on --fino 3000 --registro <voce>      (on o off; la coppia IN FASE)

**Le righe di `gravita_due_corpi.vertici` e `prepara_coppia`** *(905f91d6)* **con la distanza `d` al posto della costante `DIST = (39, 0)`**: il nodo buono piu' vicino a `(L/2 - d/2, L/2)`, il secondo `+ (d, 0)`. **Il resto si importa da `gravita_due_corpi`** *(`parametri`, `impronta`, `tick_U`, `FASI`, `BASE`, `OGNI_STATO`)*: nessuna riga di fisica nuova.
**Il caso noto:** (i) `d = 39`: lo stato di partenza AL BIT con `CHI/due_corpi/F-on/stato_000000.npz` e l'impronta del log di F-on; (ii) `d = 60`, `kappa = 0`: `50` tick del tick v2 = `50` del tick U con `cs = s`, AL BIT; DEVE FALLIRE con `kappa` vero.
"""
import argparse
import hashlib
import json
import math
import os
import re
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import triangolo_chi_v4 as TC  # noqa: E402
import chi_tick as CT  # noqa: E402
import chi_tick_v2 as CV2  # noqa: E402
import gravita_due_corpi as GD  # noqa: E402

ESITI = []


def esito(che, ok, nota=""):
    ESITI.append((che, bool(ok)))
    print("  DEVE: %-110s %s %s" % (che, "PASSA" if ok else "### FALLISCE", nota))


def vertici(fr, L, d):
    """### `gravita_due_corpi.vertici` riga per riga, con `DIST = (d, 0)`."""
    from solitone import toro as TO
    A1, A2 = TO.vettori()
    tgt = (0.5 * L - 0.5 * d, 0.5 * L)
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
    assert d % 3 == 0, "il vettore della coppia non porta su un nodo buono"
    return [V0, [V0[0] + d, V0[1]]], tgt


def prepara_coppia(Z, scena, d):
    """### `gravita_due_corpi.prepara_coppia` riga per riga, con `vertici(fr, L, d)`."""
    MT, MTR, T1, TRU, TV, PO = TC.moduli()
    rho_c, e, t0 = MT.rho_c_assoluto(), MT.PB.E_DECISO, MT.G2.T0
    st, L = Z["st"], Z["L"]
    fr = TV.francobollo_L162(0)
    centri, tgt = vertici(fr, L, d)
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
        if GD.FASI[scena][j] != 0.0:
            st["psi_h"][...] = st["psi_h"] * np.exp(1j * GD.FASI[scena][j])
        soli.append((st["psi_h"].copy(), st["phi_h"].copy()))
    st["psi_h"][...] = soli[0][0] + soli[1][0]
    st["phi_h"][...] = soli[0][1] * (soli[1][1] / phi_F3)
    C = PO.campi(Z, rho_c, e)
    return C, {"scena": scena, "d": d, "centri": centri, "bersaglio": list(tgt), "distanza": MT.distanza(L, centri[0], centri[1]), "vuoto_psi": vuoto_psi,
               "fasi_gradi": [math.degrees(x) for x in GD.FASI[scena]], "masse_soli": [float(np.sum(np.abs(s_[0]) ** 2)) for s_ in soli]}


def avvia():
    import _presidio
    for m in ("chi_tick.py", "chi_tick_v2.py", "triangolo_chi_v4.py", "gravita_due_corpi.py"):
        _presidio.avvia(os.path.join(_QUI, m))
    _presidio.avvia(__file__)


def caso_noto():
    avvia()
    print("=" * 130)
    print("[M1017-K] IL CASO NOTO: (i) d = 39, lo stato di partenza AL BIT con [M0417] F-on; (ii) d = 60, kappa = 0, 50 tick del tick v2 = 50 del tick U AL BIT; DEVE FALLIRE con kappa vero")
    print("=" * 130)
    f0 = os.path.join(GD.BASE, "F-on", "stato_000000.npz")
    assert open(f0 + ".sha1", encoding="utf-8").read().split()[0] == hashlib.sha1(open(f0, "rb").read()).hexdigest(), "lo sha1 di %s NON coincide" % f0
    imp_log = None
    with open(os.path.join(GD.BASE, "log_F-on.txt"), encoding="utf-8", errors="replace") as h:
        for r in h:
            m = re.search(r"L'IMPRONTA DELLO STATO DI PARTENZA ([0-9a-f]{40})", r)
            if m:
                imp_log = m.group(1)
                break
    assert imp_log, "l'impronta non e' nel log di F-on: FERMO"
    with np.load(f0) as z:
        rif = {x: z[x].copy() for x in z.files if x != "meta"}
    out = {}
    with TC.scena() as Z:
        mot = Z["mot"]
        n, m = mot.inc.n, mot.inc.m
        Lp = CT.Laplaciano(mot)
        # ### (i) d = 39
        C, info = prepara_coppia(Z, "F", 39)
        P, Pon, m0 = GD.parametri(Z, C, True)
        X = CT.nuovo_X(n, m, CT.chi_statico(mot, Z["st"], Z["par"], Pon, Lp, m0))
        imp = GD.impronta(Z, C, X)
        nuovo = {x: Z["st"][x] for x in Z["chiavi"]}
        nuovo.update(campo_A=C.campo.A, campo_E=C.campo.E, **{q: X[q] for q in CT.CHIAVI_CHI})
        diverse = sorted(x for x in rif if not np.array_equal(rif[x], nuovo[x]))
        print("### (i) d = 39: i vertici %s, la distanza %.4f; m0 %+.12e; l'impronta %s (il log di F-on %s); le chiavi diverse da F-on/stato_000000: %s" % (
            info["centri"], info["distanza"], m0, imp, imp_log, diverse or "nessuna"))
        esito("K (i): d = 39, lo stato di partenza AL BIT con F-on/stato_000000 (ogni chiave) e l'impronta uguale a quella del log", not diverse and imp == imp_log)
        Z["metti"]()
        # ### (ii) d = 60
        for nome in ("v2 kappa 0", "U cs = s", "v2 kappa vero"):
            C, info = prepara_coppia(Z, "F", 60)
            P, Pon, m0 = GD.parametri(Z, C, nome == "v2 kappa vero")
            X = CT.nuovo_X(n, m, CT.chi_statico(mot, Z["st"], Z["par"], Pon, Lp, m0))
            G = (np.asarray(info["centri"][0], float) + np.asarray(info["centri"][1], float)) / 2.0
            print("### (ii) %s: i vertici %s (il bersaglio %s; il punto medio %s, il centro del toro %s), la distanza %.4f; kappa %r, c0 %r, m0 %+.12e; l'impronta di partenza %s" % (
                nome, info["centri"], ["%.2f" % x for x in info["bersaglio"]], G.tolist(), [Z["L"] / 2.0] * 2, info["distanza"], P.kappa, P.c0, m0, GD.impronta(Z, C, X)[:12]))
            for _t in range(50):
                if nome == "U cs = s":
                    GD.tick_U(Z["z"], C.campo, P.s)
                else:
                    CV2.tick_chi_v2(Z["z"], C.campo, P, Lp, X)
            out[nome] = ({x: Z["st"][x].copy() for x in Z["chiavi"]}, C.campo.A.copy(), C.campo.E.copy(), np.array(mot.cs, dtype=float, copy=True))
            Z["metti"]()
        s = float(Pon.s)

    def div(a, b):
        return [x for x in a[0] if not np.array_equal(a[0][x], b[0][x])] + [q for q, p, r in (("A", a[1], b[1]), ("E", a[2], b[2])) if not np.array_equal(p, r)]
    d0, d1 = div(out["v2 kappa 0"], out["U cs = s"]), div(out["v2 kappa vero"], out["U cs = s"])
    cs_ok = bool(np.all(out["v2 kappa 0"][3] == s))
    print("### (ii) v2 kappa 0 contro U: %s; cs = s esatto %s; v2 kappa vero contro U: le chiavi diverse %s" % (d0 or "AL BIT", cs_ok, d1))
    esito("K (ii): d = 60, kappa = 0: il tick v2 = il tick U con cs = s AL BIT dopo 50 tick (la materia, A, E), cs = s esatto", not d0 and cs_ok)
    esito("K (ii) DEVE FALLIRE: d = 60, kappa vero: la materia diversa dopo 50 tick", "psi_h" in d1)
    print("-" * 130)
    print("ESITO: %d/%d" % (sum(ok for _c, ok in ESITI), len(ESITI)))
    print("=" * 130)
    return 0 if all(ok for _c, ok in ESITI) else 1


def corsa(d, chi_on, k_fino, reg):
    """### `gravita_due_corpi.corsa` riga per riga, la coppia IN FASE a distanza `d`; gli stati in `CHI/due_corpi/F<d>-<on|off>`."""
    avvia()
    from solitone import _registro_corse as RC
    MT = TC.moduli()[0]
    nome = "F%d-%s" % (d, "on" if chi_on else "off")
    d_out = os.path.join(GD.BASE, nome)
    os.makedirs(d_out, exist_ok=True)
    with TC.scena() as Z:
        mot = Z["mot"]
        n, m = mot.inc.n, mot.inc.m
        Lp = CT.Laplaciano(mot)
        C, info = prepara_coppia(Z, "F", d)
        P, Pon, m0 = GD.parametri(Z, C, chi_on)
        X = CT.nuovo_X(n, m, CT.chi_statico(mot, Z["st"], Z["par"], Pon, Lp, m0))
        meta = dict(info, corsa=nome, parametri={"kappa": P.kappa, "c0": P.c0, "m0": m0, "c2": P.c2, "m2": P.m2, "e0": P.e0, "s": P.s, "f": P.f, "kappa_on": Pon.kappa})
        print("### %s: i vertici %s, la distanza %.4f, le fasi %s; i parametri %r; m0 %+.12e; L'IMPRONTA DELLO STATO DI PARTENZA %s; gli stati in %s" % (
            nome, info["centri"], info["distanza"], info["fasi_gradi"], P, m0, GD.impronta(Z, C, X), d_out))
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
            if k % GD.OGNI_STATO == 0 or k == k_fino:
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
    c.add_argument("--d", type=int, required=True)
    c.add_argument("--chi", choices=("on", "off"), required=True)
    c.add_argument("--fino", type=int, required=True)
    c.add_argument("--registro")
    x = ap.parse_args(argv)
    if x.cmd == "caso_noto":
        return caso_noto()
    return corsa(x.d, x.chi == "on", x.fino, x.registro)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
