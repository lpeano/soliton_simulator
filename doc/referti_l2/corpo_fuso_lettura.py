# -*- coding: utf-8 -*-
r"""**[M1519] PEZZO 3: LE LETTURE DI S1 E S2 E IL VERDETTO S3 DEL CORPO FUSO** *(DECISIONE DI LUCA, 2026-11-27 `15:19`, `18:24`, `18:59` punto 5; la carta `doc/CARTA_fondo_giusto.md`, «3-unetvicies, il seguito 2», scritta PRIMA)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/corpo_fuso_lettura.py noto > doc/referti_l2/corpo_fuso_lettura_noto.txt   (KL, KH, KH-neg, KHc: sui dati gia' letti)
    E:\python\py3132\python.exe doc/referti_l2/corpo_fuso_lettura.py lettura > doc/referti_l2/corpo_fuso.txt             (S1 su 217 stati, S2 sui giri 1, 2, 3r, il verdetto S3)

**S1:** gli stati `0..54000` ogni `250` *(`M2034/coppia/d1` fino a `6000`, `d1L` fino a `18000`, `M1519/d1T` fino a `30000`, `M1519/d1T_r` dopo)*; per stato A0, `d_p`, `d_m`, `R`, `max rho`, la norma, `w` *(per meta' se DUE, `FPC.w_di` totale se UNO)*, `chi` al centro, `H` e `H_chi`; per finestra di `500` `omega`; per finestra di `2500` il respiro di `R`. **S2:** i giri `1`, `2`, `3r`, C e D, A0 sui loro stati. **S3:** le regole della carta.
"""
import argparse
import json
import os
import re
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import coppia_a0 as A0  # noqa: E402
import corpo_fuso as CF  # noqa: E402
import corpo_fuso_v2 as CR  # noqa: E402
import due_corpi_lettura_v6 as L6  # noqa: E402
import chi_tick_v2 as CV2  # noqa: E402

L2, PF, FPC, CT, GD = A0.L2, A0.PF, L6.FPC, CF.CT, CF.GD
D1, D1L, D_T, D_TR = A0.D1, CF.D1L, CF.D_S1, CR.D_S1R
GIRI = (("1", os.path.join(CF.D_S2, "giro_1")), ("2", os.path.join(CF.D_S2, "giro_2")), ("3r", CR.D_G3R))
KS = list(range(0, 54001, 250))
KS_NOTO = list(range(0, 18001, 250))
KS_GIRO = list(range(0, CF.K_GIRO + 1, 250))
F500 = [(k, k + 500) for k in range(0, 54000, 500)]
W2500 = [(6250 + 2500 * i, 6250 + 2500 * (i + 1)) for i in range(19)]
V7_TXT = os.path.join(_QUI, "due_corpi_fondo_v7.txt")
TOL_C, MIN_UNO, MIN_FILA, RHO_COLL, R_COLL = 0.10, 8, 22, 5e4, 6.0   # ### le soglie di Luca ([M1519] S3) e le mie della carta


def avvia():
    import _presidio
    CF.avvia()
    for m in ("due_corpi_lettura_v4.py", "coppia_a0.py", "due_corpi_lettura_v6.py", "corpo_fuso_v2.py"):
        _presidio.avvia(os.path.join(_QUI, m))
    _presidio.avvia(__file__)
    assert os.path.normcase(L6.D1L) == os.path.normcase(D1L), "d1L: %s contro %s" % (L6.D1L, D1L)


def cartella(k):
    return D1 if k <= 6000 else (D1L if k <= 18000 else (D_T if k <= 30000 else D_TR))


def leggi_serie(cartelle):
    ser, om, meta = {}, [[], []], None
    for c, nome in cartelle:
        f = os.path.join(c, nome)
        PF.controlla(f)
        S = json.load(open(f, encoding="utf-8"))
        meta = meta or S["meta"]
        for r in S["serie"]:
            ser[int(r[0])] = r
        for j in range(2):
            om[j] += list(S["omega"][j])
    return ser, [np.array(o) for o in om], meta


def riga_v6(k, r, N0):
    """### la riga per stato di `due_corpi_lettura_v6` (il formato di `due_corpi_fondo_v7.txt`)."""
    extra = ("d_p %7.3f; w %.3f %.3f; chi ai picchi %+.2f %+.2f" % (r["dloc"], r["w"][0], r["w"][1], r["chi"][0], r["chi"][1])) if r["nloc"] == 2 else "d_p -"
    return "  k %5d: %-10s %s; d_m %7.3f; R %7.3f; max rho %.4e; N %+.2e" % (k, r["verd"], extra, r["dm"], r["R"], r["rmax"], r["N"] / N0 - 1.0)


class Lettore:
    """### A0 e le misure per stato; `dm` dalla serie se c'e'."""

    def __init__(self, centro):
        self.G = G = A0.geometria()
        self.centro = centro
        self.dxy = np.asarray(G["TO"].scarti(G["m1"], G["m2"], centro[0], centro[1], G["L"]))[:, :2]
        self.meta = [self.dxy[:, 1] < 0.0, self.dxy[:, 1] >= 0.0]

    def stato(self, f, ser=None, k=None):
        G, dxy = self.G, self.dxy
        r = A0.a0(G, f, self.centro)
        X = L2.leggi(f)
        rho = np.bincount(G["nodo"], weights=np.sum(np.abs(X["psi_h"]) ** 2, axis=1), minlength=G["n"])
        if ser is not None:
            s = ser[k]
            r["dm"] = float(np.hypot(s[4] - s[1], s[5] - s[2]))
        if r["nloc"] == 2:
            r["w"] = [FPC.w_di(rho * mm, G["L"]) for mm in self.meta]
            r["chi"] = [float(X["chi"][np.hypot(dxy[:, 0] - dxy[i, 0], dxy[:, 1] - dxy[i, 1]) < 4.0].mean()) for i in r["loc"]]
        r["w_tot"] = FPC.w_di(rho, G["L"]) if r["nloc"] == 1 else float("nan")
        im = r["im"]
        r["chi_c"] = float(X["chi"][np.hypot(dxy[:, 0] - dxy[im, 0], dxy[:, 1] - dxy[im, 1]) < 4.0].mean())
        return r


class Energia:
    """### `H` e `H_chi` (`chi_tick_v2.energia_chi_v2`) nella scena della ripresa; lo stato si ricarica SUL POSTO."""

    def __init__(self, Z, f):
        self.Z = Z
        self.R = CF.Ripresa10(Z, f, 0, "lettura")

    def carica(self, f):
        from solitone import _u1_oggi as UO
        Z, R = self.Z, self.R
        PF.controlla(f)
        with np.load(f) as z:
            for x in Z["chiavi"]:
                Z["st"][x][...] = z[x]
            R.C.campo.A[...] = z["campo_A"]
            R.C.campo.E[...] = z["campo_E"]
            for q in CT.CHIAVI_CHI:
                R.X[q][...] = z[q]
        UO.U1.scrivi_U(Z["mot"], R.C.campo)

    def H(self):
        z, R = self.Z["z"], self.R
        return CV2.energia_chi_v2(z["mot"], z["st"], z["par"], R.P, R.Lp, R.X, R.C.campo)

    def Hc_a_mano(self):
        P, X, Lp = self.R.P, self.R.X, self.R.Lp
        chi, pi = X["chi"], X["pi"]
        dch = chi[Lp.ii] - chi[Lp.jj]
        return 0.5 * float(np.sum(pi * pi)) / P.f + 0.5 * P.c2 * float(np.sum(dch * dch)) + 0.5 * P.m2 * float(np.sum(chi * chi)) + P.c0 * float(np.sum(chi))


def file_stato(k):
    return os.path.join(cartella(k), "stato_%06d.npz" % k)


# ---------------------------------------------------------------------------------------------------- noto
def noto():
    avvia()
    print("=" * 140)
    print("[M1519] PEZZO 3, I CASI NOTI DELLA LETTURA (la carta, il seguito 2): KL, KH, KH-neg, KHc")
    print("=" * 140)
    OK = {}

    def esito(che, ok, nota=""):
        OK[che] = bool(ok)
        print("  DEVE: %-112s %s %s" % (che, "PASSA" if ok else "### FALLISCE", nota))
        sys.stdout.flush()
    ser, _om, meta = leggi_serie([(D1, "serie.json"), (D1L, "serie.json")])
    LT = Lettore(meta["centro_coppia"])
    T = {k: LT.stato(file_stato(k), ser, k) for k in KS_NOTO}
    mie = [riga_v6(k, T[k], T[0]["N"]) for k in KS_NOTO]
    righe = [r.rstrip("\n") for r in open(V7_TXT, encoding="utf-8") if re.match(r"^  k +\d+: ", r)]
    diverse = [k for k, a, b in zip(KS_NOTO, mie, righe) if a != b]
    esito("(KL) le %d righe per stato 0..18000 = quelle di due_corpi_fondo_v7.txt carattere per carattere" % len(KS_NOTO), len(righe) == len(mie) and not diverse, "righe %d e %d; diverse a k %s" % (len(mie), len(righe), diverse[:5]))
    fa, fb = os.path.join(D1L, "stato_018000.npz"), os.path.join(D1L, "stato_017750.npz")
    with GD.TC.scena() as Z:
        E = Energia(Z, fa)
        h_nuova = E.H()
        Z["metti"]()
    with GD.TC.scena() as Z:
        E = Energia(Z, fb)
        h_b = E.H()
        E.carica(fa)
        h_sul_posto = E.H()
        hc = E.Hc_a_mano()
        Z["metti"]()
    esito("(KH) H di d1L/stato_018000: la scena nuova = ricaricato sul posto dopo stato_017750, AL BIT (H e H_chi)", h_nuova == h_sul_posto, "H %.12e, H_chi %.12e" % h_nuova)
    esito("(KH-neg) DEVE FALLIRE l'uguaglianza: H di stato_017750 e' DIVERSO da quello di stato_018000", h_b != h_nuova, "H %.12e contro %.12e" % (h_b[0], h_nuova[0]))
    esito("(KHc) H_chi dalla formula nello script = quello dello strumento entro 1e-12 relativo", abs(hc / h_sul_posto[1] - 1.0) < 1e-12, "%.12e contro %.12e" % (hc, h_sul_posto[1]))
    fall = [k for k, v in OK.items() if not v]
    print("### %d DEVE: %d PASSANO, %d FALLISCONO %s" % (len(OK), len(OK) - len(fall), len(fall), fall))
    print("=" * 140)
    return 0 if not fall else 1


# ---------------------------------------------------------------------------------------------------- lettura
def file_consecutive(KK, T, pred):
    """### le file di stati consecutivi (nell'ordine di `KK`) che soddisfano `pred`: `[(k_inizio, k_fine, n)]`."""
    out, i = [], 0
    while i < len(KK):
        if pred(T[KK[i]]):
            j = i
            while j + 1 < len(KK) and pred(T[KK[j + 1]]):
                j += 1
            out.append((KK[i], KK[j], j - i + 1))
            i = j + 1
        else:
            i += 1
    return out


def spezza(r):
    return r["nloc"] == 2 and r["dloc"] > 2.0 * max(r["w"])


def collassa_b(r):
    return r["rmax"] > RHO_COLL and r["R"] < R_COLL


def lettura():
    avvia()
    print("=" * 140)
    print("[M1519] PEZZO 3: IL CORPO FUSO, LE LETTURE DI S1 (0..54000) E DI S2 (I GIRI 1, 2, 3r) E IL VERDETTO S3 (le regole della carta, il seguito 2)")
    print("=" * 140)
    ser, om, meta = leggi_serie([(D1, "serie.json"), (D1L, "serie.json"), (D_TR, "serie.json")])
    assert len(om[0]) == 54000 and len(om[1]) == 54000, "omega: %d e %d tick, non 54000" % (len(om[0]), len(om[1]))
    LT = Lettore(meta["centro_coppia"])
    T, H = {}, {}
    with GD.TC.scena() as Z:
        E = Energia(Z, file_stato(0))
        for k in KS:
            f = file_stato(k)
            T[k] = LT.stato(f, ser, k)
            E.carica(f)
            H[k] = E.H()
        Z["metti"]()
    N0 = T[0]["N"]
    # ------------------------------------------------------------------ S1 per stato
    print("-" * 140)
    print("S1 (i) PER STATO: il verdetto A0, d_p, d_m, R, max rho, la norma; w (per corpo se DUE, totale se UNO); chi al centro; H, H_chi")
    print("-" * 140)
    for k in KS:
        r = T[k]
        ww = ("w %.3f %.3f" % tuple(r["w"])) if r["nloc"] == 2 else ("w %.3f" % r["w_tot"] if r["nloc"] == 1 else "w -")
        print("%s; %s; chi al centro %+.3f; H %.10e; H_chi %.10e  [%s]" % (riga_v6(k, r, N0), ww, r["chi_c"], H[k][0], H[k][1], os.path.basename(cartella(k))))
    dn = max(abs(T[k]["N"] / N0 - 1.0) for k in KS)
    okn = dn < A0.TOL_NORMA
    print("  DEVE: (la norma) max |N(k)/N(0) - 1| su %d stati = %.3e < 1e-9   %s" % (len(KS), dn, "PASSA" if okn else "### FALLISCE: FERMO"))
    nv = {v: sum(1 for k in KS if T[k]["verd"] == v) for v in sorted(set(T[k]["verd"] for k in KS))}
    print("  i verdetti su %d stati: %s; da k 6250: %s" % (len(KS), nv, {v: sum(1 for k in KS if k >= 6250 and T[k]["verd"] == v) for v in nv}))
    # ------------------------------------------------------------------ S1 per finestra di 500: omega
    print("-" * 140)
    print("S1 (ii) PER FINESTRA DI 500: omega medio per meta' e la media delle due (### la riserva della carta: dopo k 6250 le meta' non sono due corpi, e la media NON e' l'omega della psi intera)")
    print("-" * 140)
    for a, b in F500:
        o = [float(om[j][a:b].mean()) for j in range(2)]
        print("  (%5d, %5d]: omega %.6f %.6f; la media %.6f" % (a, b, o[0], o[1], 0.5 * (o[0] + o[1])))
    # ------------------------------------------------------------------ S1 per finestra di 2500
    print("-" * 140)
    print("S1 (iii) PER FINESTRA DI 2500 (da k 6250): il respiro di R, w medio (gli stati UNO), max rho medio, H e H_chi")
    print("-" * 140)
    righe_w = []
    for a, b in [(0, 6250)] + W2500:
        kk = [k for k in KS if a <= k <= b]
        R = [T[k]["R"] for k in kk]
        uno = [T[k]["w_tot"] for k in kk if T[k]["nloc"] == 1]
        resp = (max(R) - min(R)) / (sum(R) / len(R))
        wm = sum(uno) / len(uno) if uno else float("nan")
        if a >= 6250:
            righe_w.append((a, b, resp, wm, len(uno), len(kk)))
        print("  [%5d, %5d] (%2d stati): il respiro di R %.4f (R da %.3f a %.3f); UNO %2d, w medio %.4f; max rho medio %.4e; H %.10e -> %.10e (%+.3e rel); H_chi %.6e -> %.6e" % (
            a, b, len(kk), resp, min(R), max(R), len(uno), wm, float(np.mean([T[k]["rmax"] for k in kk])), H[kk[0]][0], H[kk[-1]][0], H[kk[-1]][0] / H[kk[0]][0] - 1.0, H[kk[0]][1], H[kk[-1]][1]))
    h18, h54 = H[18000][0], H[54000][0]
    print("  ### H a k 18000 %.10e, a k 54000 %.10e: %+.4e relativo (lo strumento NON e' sigillato su questa scena: e' un andamento)" % (h18, h54, h54 / h18 - 1.0))
    # ------------------------------------------------------------------ S2
    print("-" * 140)
    print("S2: I GIRI 1, 2, 3r (C: |maxchi(n+1)/maxchi(n) - 1| < 0.10 E il respiro di w del giro n+1 < 0.10; D: C no, ma max|chi| entro il 10% fra 2 e 3r)")
    print("-" * 140)
    J, TOT, A0G = {}, {}, {}
    for g, d in GIRI:
        f = os.path.join(d, "giro.json")
        PF.controlla(f)
        J[g] = j = json.load(open(f, encoding="utf-8"))
        TOT[g] = t = CR.totali(j)
        print("  GIRO %s (%s): la partenza %s, il residuo %.3e; P %d (%s), i picchi a k %s" % (g, d, j["partenza"], j["residuo_partenza"], j["P"], j["fonte"], j["picchi_k"]))
        print("    max|chi| %.4f; w medio %.4f (da %.4f a %.4f), il respiro %.4f; la profondita' media %+.4f; omega medio %.6f (la psi intera)" % (t["maxchi"], t["w_medio"], min(j["w"]), max(j["w"]), t["respiro"], t["profondita"], t["omega"]))
        for a, b, mc, w, pr, o in CR.per_finestra(j):
            print("    (%5d, %5d] max|chi| %10.4f  w %8.4f  profondita' %+10.4f  omega %.6f" % (a, b, mc, w, pr, o))
        A0G[g] = {k: LT.stato(os.path.join(d, "stato_%06d.npz" % k)) for k in KS_GIRO}
        nvg = {v: sum(1 for k in KS_GIRO if A0G[g][k]["verd"] == v) for v in sorted(set(A0G[g][k]["verd"] for k in KS_GIRO))}
        print("    A0 sui %d stati del giro: %s" % (len(KS_GIRO), nvg))
    C = {}
    for n, m in (("1", "2"), ("2", "3r")):
        rr = TOT[m]["maxchi"] / TOT[n]["maxchi"] - 1.0
        C[m] = (abs(rr) < TOL_C, TOT[m]["respiro"] < TOL_C, rr)
        print("  C fra %s e %s: max|chi| %.4f -> %.4f, |rapporto - 1| %.4f (%s); il respiro del giro %s %.4f (%s)  ->  %s" % (
            n, m, TOT[n]["maxchi"], TOT[m]["maxchi"], abs(rr), "SI" if C[m][0] else "NO", m, TOT[m]["respiro"], "SI" if C[m][1] else "NO", "PASSA" if C[m][0] and C[m][1] else "NON PASSA"))
    c_passa = [m for m in ("2", "3r") if C[m][0] and C[m][1]]
    D_vale = not c_passa and C["3r"][0]
    print("  ### C PASSA: %s; D (C no, max|chi| fermo fra 2 e 3r): %s" % (("al giro %s" % c_passa[0]) if c_passa else "NO", "SI" if D_vale else "NO"))
    # ------------------------------------------------------------------ S3
    print("-" * 140)
    print("S3: IL VERDETTO (le regole della carta, il seguito 2)")
    print("-" * 140)
    sp1 = [x for x in file_consecutive(KS, T, spezza) if x[2] >= MIN_FILA]
    sp2 = {g: [x for x in file_consecutive(KS_GIRO, A0G[g], spezza) if x[2] >= MIN_FILA] for g, _d in GIRI}
    lunghe = max([x[2] for x in file_consecutive(KS, T, spezza)] or [0])
    print("  SI SPEZZA? (DUE con d_p > 2 max w, per >= %d stati consecutivi): S1 %s (la fila piu' lunga %d stati); S2 %s" % (MIN_FILA, sp1 or "nessuna", lunghe, {g: v or "nessuna" for g, v in sp2.items()}))
    r4a = sum(x[2] for x in righe_w[:4]) / 4.0
    r4b = sum(x[2] for x in righe_w[-4:]) / 4.0
    col_a = r4b > r4a
    col_b = [x for x in file_consecutive(KS, T, collassa_b) if x[2] >= MIN_FILA]
    print("  COLLASSA? (a) il respiro di R: le prime 4 finestre %.4f, le ultime 4 %.4f -> %s (una corsa, nessuna barra: e' una lettura); (b) max rho > 5e4 e R < 6 per >= %d stati: %s" % (
        r4a, r4b, "CRESCE" if col_a else "non cresce", MIN_FILA, col_b or "nessuna"))
    verdetti = []
    if sp1 or any(sp2.values()):
        verdetti.append("SI SPEZZA")
    if col_a or col_b:
        verdetti.append("COLLASSA")
    if c_passa:
        wS2 = TOT[c_passa[0]]["w_medio"]
        ok = [(n_uno >= MIN_UNO and abs(wm / wS2 - 1.0) < TOL_C) for _a, _b, _r, wm, n_uno, _n in righe_w]
        istar = next((i for i in range(len(ok) - 1) if all(ok[i:])), None)
        print("  ESISTE: w_S2 %.4f (il giro %s); le finestre entro il 10%% con >= %d UNO: %s; i* %s" % (wS2, c_passa[0], MIN_UNO, "".join("1" if x else "0" for x in ok), (
            "%d (da k %d; il tempo di rilassamento %d tick dal secondo contatto)" % (istar, righe_w[istar][0], righe_w[istar][0] - 6250)) if istar is not None else "nessuna"))
        if not verdetti:
            verdetti.append("ESISTE E CI ARRIVA" if istar is not None else "ESISTE MA NON CI ARRIVA")
    if not verdetti:
        verdetti.append("ALTRO" + (" (D: max|chi| fermo entro il 10%% fra 2 e 3r, |rapporto - 1| %.4f; il respiro del giro 3r %.4f)" % (abs(C["3r"][2]), TOT["3r"]["respiro"]) if D_vale else " (C non passa, e D non vale)"))
    print("### IL VERDETTO S3: %s" % "; ".join(verdetti))
    print("=" * 140)
    return 0 if okn else 1


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("cosa", choices=("noto", "lettura"))
    a = ap.parse_args(argv)
    return {"noto": noto, "lettura": lettura}[a.cosa]()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
