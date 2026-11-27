# -*- coding: utf-8 -*-
r"""**[M1824] LA RIPRESA DI S1 E S2 DEL CORPO FUSO** *(DECISIONE DI LUCA, 2026-11-27 `18:24`, dalla posta, `625021df`; e `18:59`, in chat; la carta `doc/CARTA_fondo_giusto.md`, «3-unetvicies, il seguito. [M1824]», scritta PRIMA, `8aa80065`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/corpo_fuso_v2.py lettura_s2 > doc/referti_l2/corpo_fuso_s2_giri12.txt   (i giri 1 e 2 di S2, il criterio C fra 1 e 2)
    E:\python\py3132\python.exe doc/referti_l2/corpo_fuso_v2.py noto > doc/referti_l2/corpo_fuso_v2_noto.txt          (K0, K0-neg, KB, KB-neg, K2)
    E:\python\py3132\python.exe doc/referti_l2/corpo_fuso_v2.py corsa        (S1: d1T/stato_030000 -> k 54000, in M1519/d1T_r; dalla coda)
    E:\python\py3132\python.exe doc/referti_l2/corpo_fuso_v2.py giro3        (S2: il giro 3 da giro_2/partenza_giro_3.npz, in puntofisso_2M/giro_3r; dalla coda)

**Importa `corpo_fuso.py` e non lo riscrive:** `Ripresa10`, `giro_pf`, le costanti e i percorsi sono quelli. Le corse cadute *(`M1519/d1T`, `M1519/puntofisso_2M/giro_3`)* **non si toccano:** si leggono soltanto, per il confronto AL BIT.
"""
import argparse
import hashlib
import json
import os
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import corpo_fuso as CF  # noqa: E402

V2, D, PF, GD = CF.V2, CF.D, CF.PF, CF.GD
D_S1, D_S2, D1L = CF.D_S1, CF.D_S2, CF.D1L
D_S1R = os.path.join(CF.DIR, "d1T_r")
D_G3, D_G3R = os.path.join(D_S2, "giro_3"), os.path.join(D_S2, "giro_3r")
F_PART3 = os.path.join(D_S2, "giro_2", "partenza_giro_3.npz")
K_R, K_A = 30000, CF.K_A                  # ### S1 riparte da 30000 (la carta: la serie parziale finisce a 30000)
K_CONFRONTO_S1 = (30250, 30500, 30750, 31000)
K_CONFRONTO_S2 = (0, 250, 500, 750, 1000)  # ### k 0 in piu' dei quattro del mandato: e' gratis, e' lo stato caricato
FIN500 = 500


def avvia():
    import _presidio
    CF.avvia()
    _presidio.avvia(__file__)


def leggi_stato(f):
    PF.controlla(f)
    with np.load(f) as z:
        return {x: z[x].copy() for x in z.files if x != "meta"}


def diverse(dd, rif):
    """### le chiavi di `rif` in cui `dd` NON e' uguale AL BIT (e le chiavi mancanti)."""
    return [x for x in rif if x not in dd or not np.array_equal(np.asarray(dd[x]), rif[x])]


def serie_parziale_d1T():
    f = os.path.join(D_S1, "serie_parziale.json")
    PF.controlla(f)
    return json.load(open(f, encoding="utf-8"))


# ---------------------------------------------------------------------------------------------------- lettura_s2
def per_finestra(j):
    """### per finestra di 500 `(a, b]`: max|chi| (il massimo delle due finestre da 250), w e profondita' medie sui campioni ogni 100 con k in (a, b], omega medio sui tick a+1..b."""
    righe = []
    for i in range(CF.K_GIRO // FIN500):
        a, b = FIN500 * i, FIN500 * (i + 1)
        mc = max(j["maxchi_fin"][2 * i:2 * i + 2])
        ii = [q for q in range(len(j["w"])) if a < CF.OGNI_W * q <= b]
        w = sum(j["w"][q] for q in ii) / len(ii)
        pr = sum(j["profondita"][q] for q in ii) / len(ii)
        om = sum(j["omega"][a:b]) / float(b - a)
        righe.append((a, b, mc, w, pr, om))
    return righe


def totali(j):
    w = j["w"]
    wm = sum(w) / len(w)
    return {"maxchi": max(j["maxchi_fin"]), "w_medio": wm, "respiro": (max(w) - min(w)) / wm,
            "profondita": sum(j["profondita"]) / len(j["profondita"]), "omega": sum(j["omega"]) / len(j["omega"])}


def lettura_s2():
    import _presidio
    _presidio.avvia(__file__)
    print("=" * 130)
    print("[M1824] S2, I GIRI 1 E 2 DEL PUNTO FISSO ACCOPPIATO 2M (M1519/puntofisso_2M), PRIMA DEL LANCIO DEL GIRO 3; NESSUN VERDETTO S3")
    print("=" * 130)
    print("  le definizioni (la carta di [M0137] punto 6 e di [M1519]): max|chi| del giro = il massimo per tick su tutto il giro; il respiro = (w_max - w_min)/w_medio sui 61 campioni ogni 100;")
    print("  C fra il giro n e n+1: |maxchi(n+1)/maxchi(n) - 1| < 0.10 E il respiro del giro n+1 < 0.10")
    T = {}
    for g in (1, 2):
        f = os.path.join(D_S2, "giro_%d" % g, "giro.json")
        PF.controlla(f)
        j = json.load(open(f, encoding="utf-8"))
        assert j["giro"] == g and len(j["w"]) == 61 and len(j["maxchi_fin"]) == 24 and len(j["omega"]) == CF.K_GIRO
        T[g] = t = totali(j)
        print("-" * 130)
        print("GIRO %d: la partenza %s; il residuo di Gauss alla partenza %.3e; la massa %.10e" % (g, j["partenza"], j["residuo_partenza"], j["massa"]))
        print("  P %d (%s); i picchi di max|chi| a k %s; la finestra della media [%d, %d]" % (j["P"], j["fonte"], j["picchi_k"], j["finestra"][0], j["finestra"][1]))
        print("  max|chi| %.4f; w medio %.4f, w min %.4f, w max %.4f, il respiro %.4f; la profondita' media %+.4f; omega medio %.6f" % (
            t["maxchi"], t["w_medio"], min(j["w"]), max(j["w"]), t["respiro"], t["profondita"], t["omega"]))
        print("  %-14s %12s %10s %14s %12s" % ("finestra", "max|chi|", "w", "profondita'", "omega"))
        for a, b, mc, w, pr, om in per_finestra(j):
            print("  (%5d, %5d] %12.4f %10.4f %+14.4f %12.6f" % (a, b, mc, w, pr, om))
    r = T[2]["maxchi"] / T[1]["maxchi"] - 1.0
    c1, c2 = abs(r) < 0.10, T[2]["respiro"] < 0.10
    print("-" * 130)
    print("IL CRITERIO C FRA IL GIRO 1 E IL GIRO 2:")
    print("  max|chi|: %.4f -> %.4f, |rapporto - 1| = %.4f (< 0.10: %s)" % (T[1]["maxchi"], T[2]["maxchi"], abs(r), "SI" if c1 else "NO"))
    print("  il respiro del giro 2: %.4f (< 0.10: %s)" % (T[2]["respiro"], "SI" if c2 else "NO"))
    print("### C FRA 1 E 2: %s" % ("PASSA" if c1 and c2 else "NON PASSA"))
    print("=" * 130)
    return 0


# ---------------------------------------------------------------------------------------------------- noto
def noto():
    avvia()
    print("=" * 130)
    print("[M1824] I CASI NOTI DELLA RIPRESA (la carta, il seguito [M1824]): K0, K0-neg (S1), KB e KB-neg (il confronto al bit), K2 (la carica di S2)")
    print("=" * 130)
    OK = {}

    def esito(che, ok, nota=""):
        OK[che] = bool(ok)
        print("  DEVE: %-112s %s %s" % (che, "PASSA" if ok else "### FALLISCE", nota))
        sys.stdout.flush()
    SP = serie_parziale_d1T()
    rif = {int(r[0]): r for r in SP["serie"]}
    print("  la serie parziale di d1T: %d righe, da k %d a k %d; omega %d e %d tick" % (len(SP["serie"]), int(SP["serie"][0][0]), int(SP["serie"][-1][0]), len(SP["omega"][0]), len(SP["omega"][1])))
    f0, f1 = os.path.join(D_S1, "stato_029750.npz"), os.path.join(D_S1, "stato_030000.npz")
    fin = leggi_stato(f1)
    print("  il riferimento: %s (%d chiavi); la partenza %s" % (f1, len(fin), f0))
    # ---- KB, KB-neg: il confronto AL BIT che le corse usano per fermarsi
    esito("(KB) il confronto al bit: lo stato di riferimento contro se stesso = 0 chiavi diverse", diverse(fin, fin) == [])
    pert = {x: v.copy() for x, v in fin.items()}
    v = pert["psi_h"].reshape(-1)
    v[0] = np.nextafter(v[0].real, np.inf) + 1j * v[0].imag if np.iscomplexobj(v) else np.nextafter(v[0], np.inf)
    esito("(KB-neg) DEVE FALLIRE: un ulp cambiato in psi_h -> il confronto trova psi_h diversa", diverse(pert, fin) == ["psi_h"], "diverse: %s" % diverse(pert, fin))
    # ---- K0, K0-neg
    for caso in ("K0", "K0-neg"):
        t1 = time.time()
        with GD.TC.scena() as Z:
            R = CF.Ripresa10(Z, f0, 29750, "noto", scrivi_U=(caso == "K0"))
            r0 = R.misura(29750)
            if caso == "K0":
                esito("(carica) la riga della serie a k 29750 = quella della serie parziale di d1T AL BIT", r0 == rif[29750], "%r" % r0[:3])
            R.gira(250)
            dv = diverse(R.dati(), fin)
            if caso == "K0":
                esito("(K0) lo stato a k 30000 = d1T/stato_030000 AL BIT, ogni chiave (%d)" % len(fin), not dv, "diverse: %s" % dv)
                ks = [int(r[0]) for r in R.serie]
                esito("(K0) la serie %d..%d (%d righe) = la serie parziale di d1T AL BIT" % (ks[0], ks[-1], len(ks)), ks[0] == 29760 and ks[-1] == 30000 and all(r == rif[int(r[0])] for r in R.serie))
                nn = min(len(R.om[j]) for j in range(2))
                rel = max(abs(a - b) / abs(b) for j in range(2) for a, b in zip(R.om[j], SP["omega"][j][11750:12000]))
                esito("(K0) omega dei tick 29751..30000 (%d), i due corpi: |d omega|/omega < 1e-12 (Luca 13:12)" % nn, nn == 250 and rel < CF.TOL_OMEGA, "max rel %.3e" % rel)
            else:
                esito("(K0-neg) senza riscrivere geo.U lo stato a k 30000 e' DIVERSO da d1T/stato_030000", bool(dv), "diverse: %s" % dv)
            Z["metti"]()
        print("    (%s: %.0f s)" % (caso, time.time() - t1))
        sys.stdout.flush()
    # ---- K2: la carica di S2 (nessun tick): lo stato caricato da partenza_giro_3 con pi = 0 = giro_3/stato_000000 AL BIT
    with GD.TC.scena() as Z:
        R = CF.Ripresa10(Z, F_PART3, 0, "S2_giro_3", azzera_pi=True)
        dv = diverse(R.dati(), leggi_stato(os.path.join(D_G3, "stato_000000.npz")))
        esito("(K2) la carica di S2 da partenza_giro_3 (pi = 0) = giro_3/stato_000000 AL BIT, ogni chiave", not dv, "diverse: %s" % dv)
        Z["metti"]()
    fall = [k for k, v_ in OK.items() if not v_]
    print("### %d DEVE: %d PASSANO, %d FALLISCONO %s" % (len(OK), len(OK) - len(fall), len(fall), fall))
    print("=" * 130)
    return 0 if not fall else 1


# ---------------------------------------------------------------------------------------------------- corsa (S1)
def corsa():
    avvia()
    assert not os.path.exists(os.path.join(D_S1R, "stato_%06d.npz" % (K_R + CF.OGNI_STATO))), "%s c'e' gia': non si riscrive" % D_S1R
    os.makedirs(D_S1R, exist_ok=True)
    SP = serie_parziale_d1T()
    assert int(SP["serie"][-1][0]) == K_R and all(len(o) == K_R - CF.K_DA for o in SP["omega"]), "la serie parziale di d1T NON finisce a k %d" % K_R
    f_da = os.path.join(D_S1, "stato_%06d.npz" % K_R)
    t1 = time.time()
    with GD.TC.scena() as Z:
        R = CF.Ripresa10(Z, f_da, K_R, "d1T_r")
        r0 = R.misura(K_R)
        assert r0 == SP["serie"][-1], "la riga a k %d NON e' quella della serie parziale di d1T" % K_R
        R.serie = [list(r) for r in SP["serie"]]
        R.om = [list(o) for o in SP["omega"]]
        print("### [M1824] S1, d1''' ripresa: da %s, %d tick (fino a k %d); la riga a k %d = la serie parziale AL BIT; la serie e omega ripartono da li' (%d righe, %d tick)" % (
            f_da, K_A - K_R, K_A, K_R, len(R.serie), len(R.om[0])))
        sys.stdout.flush()

        def scrivi_serie(nome):
            f = os.path.join(D_S1R, nome)
            open(f, "w", encoding="utf-8").write(json.dumps({"meta": R.meta, "serie": R.serie, "omega": R.om}))
            PF.firma(f)

        def salva(kk):
            if kk % CF.OGNI_STATO:
                return
            dd = R.dati()
            fz = os.path.join(D_S1R, "stato_%06d.npz" % kk)
            np.savez(fz, meta=np.array(json.dumps(dict(R.meta, k=kk))), **dd)
            open(fz + ".sha1", "w", encoding="utf-8").write(hashlib.sha1(open(fz, "rb").read()).hexdigest() + "\n")
            u = R.serie[-1]
            print("    k %d: y1 %+.4f y2 %+.4f; max|chi| %.4e (%.0f s)" % (kk, u[2], u[5], u[-1], time.time() - t1))
            if kk in K_CONFRONTO_S1:
                dv = diverse(dd, leggi_stato(os.path.join(D_S1, "stato_%06d.npz" % kk)))
                print("    DEVE: lo stato a k %d = d1T/stato_%06d AL BIT: %s" % (kk, kk, "PASSA" if not dv else "### FALLISCE, diverse %s: LA CORSA SI FERMA" % dv))
                sys.stdout.flush()
                assert not dv, "lo stato a k %d NON e' quello di d1T: %s" % (kk, dv)
            sys.stdout.flush()
            if kk % CF.OGNI_PARZIALE == 0:
                scrivi_serie("serie_parziale.json")
        R.gira(K_A - K_R, salva)
        scrivi_serie("serie.json")
        Z["metti"]()
    print("### %d tick in %.0f s" % (K_A - K_R, time.time() - t1))
    ok = os.path.exists(os.path.join(D_S1R, "stato_%06d.npz.sha1" % K_A))
    print("### stato_%06d.npz %s" % (K_A, "ESISTE" if ok else "### NON ESISTE"))
    return 0 if ok else 1


# ---------------------------------------------------------------------------------------------------- giro3 (S2)
def giro3():
    avvia()
    assert not os.path.exists(D_G3R), "%s c'e' gia': non si riscrive" % D_G3R
    PF.controlla(F_PART3)
    f_rif = os.path.join(D1L, "stato_%06d.npz" % CF.K_DA)
    massa = PF.massa_di(f_rif)
    Q = PF.leggi_Q()
    g, d, f_part = 3, D_G3R, F_PART3
    print("### [M1824] S2, il giro %d ripreso: da %s (pi = 0), %d tick, in %s; la massa di riferimento %.10e (da %s)" % (g, f_part, CF.K_GIRO, d, massa, f_rif))
    sys.stdout.flush()
    os.makedirs(d)
    t1 = time.time()
    with GD.TC.scena() as Z:
        R = CF.Ripresa10(Z, f_part, 0, "S2_giro_%d" % g, azzera_pi=True)
        res0 = float(R.C.residuo())
        print("### giro %d: la partenza %s (pi = 0); il residuo di Gauss %.3e" % (g, f_part, res0))
        sys.stdout.flush()

        def salva(k):
            dd = R.dati()
            PF.salva_stato(os.path.join(d, "stato_%06d.npz" % k), dd, dict(R.meta, k=k, giro=g))
            if k in K_CONFRONTO_S2:
                dv = diverse(dd, leggi_stato(os.path.join(D_G3, "stato_%06d.npz" % k)))
                print("    DEVE: lo stato a k %d = giro_3/stato_%06d AL BIT: %s" % (k, k, "PASSA" if not dv else "### FALLISCE, diverse %s: IL GIRO SI FERMA" % dv))
                sys.stdout.flush()
                assert not dv, "lo stato a k %d NON e' quello di giro_3: %s" % (k, dv)
        salva(0)
        A = CF.giro_pf(R, CF.K_GIRO, salva, True)
        Z["metti"]()
    # ---- come nel giro di corpo_fuso.puntofisso, riga per riga
    Pp, kp, fonte = V2.periodo(A["mcf"])
    ka, kb = CF.K_GIRO - Pp, CF.K_GIRO
    psi_medio = (A["S"][kb] - A["S"][ka]) / float(kb - ka)
    chi_medio = (A["SC"][kb] - A["SC"][ka]) / float(kb - ka)
    import gravita_due_corpi_misure as GM
    X6, m6 = GM.leggi(os.path.join(d, "stato_%06d.npz" % CF.K_GIRO))
    dati = {x: X6[x] for x in X6}
    dati["psi_h"] = PF.trasforma(psi_medio, Q, R.n, massa)
    dati["chi"] = chi_medio
    dati["pi"] = np.zeros_like(X6["pi"])
    f_nuova = os.path.join(d, "partenza_giro_%d.npz" % (g + 1))
    PF.salva_stato(f_nuova, dati, dict(m6, giro=g + 1, finestra=[ka, kb], P=Pp))
    esce = {"giro": g, "partenza": f_part, "residuo_partenza": res0, "massa": massa, "w": A["w"], "maxchi_fin": A["mcf"], "profondita": A["pr"], "omega": A["om"],
            "P": Pp, "picchi_k": kp, "fonte": fonte, "finestra": [ka, kb], "partenza_nuova": f_nuova, "parametri": R.meta["parametri"]}
    f = os.path.join(d, "giro.json")
    open(f, "w", encoding="utf-8").write(json.dumps(esce))
    PF.firma(f)
    print("### giro %d: P %d (%s); i picchi a k %s; la finestra [%d, %d]; %d tick in %.0f s" % (g, Pp, fonte, kp, ka, kb, CF.K_GIRO, time.time() - t1))
    ok = os.path.exists(f + ".sha1")
    print("### il giro %d: %s" % (g, "CHIUSO" if ok else "### NON CHIUSO"))
    return 0 if ok else 1


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("cosa", choices=("lettura_s2", "noto", "corsa", "giro3"))
    a = ap.parse_args(argv)
    return {"lettura_s2": lettura_s2, "noto": noto, "corsa": corsa, "giro3": giro3}[a.cosa]()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
