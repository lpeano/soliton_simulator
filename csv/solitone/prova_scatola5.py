# -*- coding: utf-8 -*-
r"""**R-SCATOLA AL 5%, LA PROVA SUL MATTONE DA SOLO** *(Luca `2026-11-16` `16:17`; la carta `doc/TASK_HISTORY/2026-11-16_scatola5.md`)*.

    E:\python\py3132\python.exe csv/solitone/prova_scatola5.py corsa --L 186 --da 0 --fino 3000 --registro prova-scatola5-L186 > <scratchpad>/prova_scatola5_L186_00000.txt
    E:\python\py3132\python.exe csv/solitone/prova_scatola5.py lettura --L 186 > doc/referti_l2/prova_scatola5_L186_lettura.txt

### **LA CORREZIONE DI LUCA (`16:58`):** **la regola e' quella di `porto.regola`, TRE clausole** *(la distanza dal centro al LATO del rombo `>= 3 R_ogg`, `R_A >= 2 R_ogg`, la fascia `>= 30`)*, **con `R_ogg` al 5%; la scena su `L 186`** *(la prima versione usava il raggio inscritto `L/2` e due clausole: `L 150`, sbagliato)*.

**La scena:** `convergenza.scena_L(L, R_A)` *(`L` dalla riga di comando; il toro MINIMO della regola al 5% per `R_ogg` 25: la distanza al lato `L sqrt(3)/4 >= 80` -> `L 186`)*; il vuoto fresco; il francobollo del mattone
`L162_MGU_03000` *(`convergenza_243.francobollo_L162("MGU", 0)`, come il porto)* nel nodo buono vicino al centro del bordo; **`R_ogg` al 5%** *(la regola di `porto_alone.raggi`)*; il bordo `R_A = 2 R_ogg`.
**La corsa:** G+U col lapse pieno *(`mattone_cottura.Corsa`, come il porto)*; la serie *(il picco a ogni tick; il raggio della materia, la massa, il raggio del 5% del vuoto ogni 50)*; le mappe ogni 100.
**Le funzioni di `porto.py` che dipendono da `L`** *(il nodo buono, il bordo, il salvataggio, la ripartenza)* **sono COPIATE qui con `L` dalla scena**: `porto.py` non e' toccato.
"""
import argparse
import glob
import json
import math
import os
import re
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_CSV = os.path.dirname(_QUI)
for _p in (_QUI, _CSV):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import convergenza as CV  # noqa: E402
import convergenza_243 as C243  # noqa: E402
import gauss_riuso as GR  # noqa: E402
import lapse_caldo as LC  # noqa: E402
import legati as LG  # noqa: E402
import mattone as MT  # noqa: E402
import mattone_cottura as CT  # noqa: E402
import mattone_rhoc as MR  # noqa: E402
import porto as PO  # noqa: E402
import porto_alone as PA  # noqa: E402

SOGLIA5 = 0.05                                  # ### Luca 16:17: R_ogg al 5%
R_OGG_MAX = 25.0                                # ### Luca 16:17: R_ogg 25; sopra, la corsa NON parte
FATTORE_R_A = 2.0                               # ### il bordo da 2 R_ogg
FATTORE_GAUSS = 10.0                            # ### come il porto (porto.FATTORE_GAUSS, "MIO, dichiarato")
OGNI, OGNI_MAPPA, OGNI_STATO, PRIMA = 50, 100, 1000, 50
DIR_REF = os.path.normpath(os.path.join(MT.DIR_REF, ".."))       # ### doc/referti_l2 (il principale)
OK = [0, 0]
FALLITE = []


def esito(che, passa, nota):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    if not passa:
        FALLITE.append(che)
    print("  DEVE PASSARE: %-110s %s   %s" % (che[:110], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()


def presidi():
    import _presidio
    GR.accendi()
    print("### IL RIUSO DELLA FATTORIZZAZIONE DI GAUSS: ACCESO (come le corse nuove del porto)")
    print("### L'INTERPRETE: %s (Python %s); PYTHONNOUSERSITE %s; TMP %s (R-AMBIENTE)" % (sys.executable, sys.version.split()[0], os.environ.get("PYTHONNOUSERSITE"), os.environ.get("TMP")))
    for m in ("convergenza", "convergenza_243", "gauss_riuso", "lapse_caldo", "legati", "mattone", "mattone_cottura", "mattone_rhoc", "porto", "porto_alone"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(os.path.join(_CSV, "_u1_prototipo.py"))
    _presidio.avvia(__file__)


def nodo_buono(fr, tgt, L):
    """### `porto.nodo_buono` COPIATA con `L` dalla scena."""
    from solitone import toro as TO
    A1, A2 = TO.vettori()
    best = None
    for n1 in range(int(math.floor(tgt[0])) - 3, int(math.floor(tgt[0])) + 4):
        for n2 in range(int(math.floor(tgt[1])) - 3, int(math.floor(tgt[1])) + 4):
            if (n1 - fr["centro"][0]) % 3 or (n2 - fr["centro"][1]) % 3:
                continue
            p = (n1 - tgt[0]) * A1 + (n2 - tgt[1]) * A2
            dd = float(np.hypot(p[0], p[1]))
            if best is None or dd < best[0]:
                best = (dd, n1 % L, n2 % L)
    return [best[1], best[2]]


def metti_bordo(Z, R_A):
    """### `porto.metti_bordo` COPIATA con `L` dalla scena."""
    from solitone import bordo as BO
    from solitone import toro as TO
    c0 = Z["bordo"]["c0"]
    g_e, gn, _r = BO.g_estremita(Z["z"], c0[0], c0[1], R_A, Z["bordo"]["g_max"])
    Z["g_e"], Z["g_nodo"] = g_e, gn
    Z["bordo"]["R_A"] = float(R_A)
    Z["r_c0"] = np.hypot(*TO.scarti(Z["m1"], Z["m2"], c0[0], c0[1], Z["L"]).T[:2])


def r5(Z, t):
    """### `(R_ogg al 5%, i raggi di porto_alone.raggi, il baricentro)`: la media per anello di `|phi - phi0|` attorno al baricentro di `rho`."""
    from solitone import toro as TO
    L = Z["L"]
    rho = MT.rho_di(Z)
    b = TO.centro(rho, Z["m1"], Z["m2"], L)[:2]
    r = np.hypot(*TO.scarti(Z["m1"], Z["m2"], b[0], b[1], L).T[:2])
    an = np.floor(r).astype(int)
    media = np.bincount(an, weights=PO.dphi_nodi(Z, t)) / np.maximum(np.bincount(an), 1)
    rr, _i = PA.raggi(media, int(TO.meta_periodo(L)))
    return rr[SOGLIA5], rr, b


def nomi(L):
    """### I nomi con `L`: lo stato su E:, la serie, le mappe, la soglia di Gauss."""
    return "scatola5_L%d" % L, os.path.join(DIR_REF, "prova_scatola5_L%d" % L)


def regola(Z, R, quando):
    """### LA REGOLA DI `porto.regola` CON `R_ogg` AL 5% *(la correzione di Luca 16:58)*: la distanza dal centro al LATO del rombo `>= 3 R_ogg`, `R_A >= 2 R_ogg`, la fascia `>= 30`; accanto, il raggio inscritto `meta_periodo`."""
    from solitone import toro as TO
    L = Z["L"]
    mp = TO.meta_periodo(L)
    A1, A2 = TO.vettori()
    a, b = L * A1, L * A2
    area = abs(float(a[0] * b[1] - a[1] * b[0]))
    lato = min(area / float(np.hypot(*a)), area / float(np.hypot(*b))) / 2.0
    R_A = Z["bordo"]["R_A"]
    c = (lato >= 3.0 * R, R_A >= 2.0 * R, lato - R_A >= 30.0)
    ok = all(c)
    print("### R-SCATOLA AL 5%% (%s): R_ogg %.1f; la distanza al lato del rombo %.2f = %.2f R_ogg (>= 3: %s); R_A %.1f = %.2f R_ogg (>= 2: %s); la fascia %.2f (>= 30: %s) -> %s; accanto, il raggio inscritto %.2f"
          % (quando, R, lato, lato / R, c[0], R_A, R_A / R, c[1], lato - R_A, c[2], "RISPETTATA" if ok else "### NON RISPETTATA", mp))
    sys.stdout.flush()
    return ok


def salva(Z, C, k, t, extra, NOME):
    import _vuoto_vivo_B as V
    meta = {"k": k, "t": t, "sha": V.shas(Z["z"]), "codice": "csv/solitone/prova_scatola5.py", "R_A": Z["bordo"]["R_A"], "L": Z["L"]}
    meta.update(extra)
    cs = LC.cs_prec()
    dati = {x: Z["st"][x] for x in Z["chiavi"]}
    dati.update(campo_A=C.campo.A, campo_E=C.campo.E)
    if cs is not None:
        dati["cs_prec"] = cs
    np.savez(os.path.join(MT.DIR_E, "%s_%05d.npz" % (NOME, k)), meta=np.array(json.dumps(meta)), **dati)


def carica(Z, f, rho_c, e):
    with np.load(f) as d:
        Z["metti"]({x: d[x].copy() for x in Z["chiavi"]})
        A, E = d["campo_A"].copy(), d["campo_E"].copy()
        meta = json.loads(str(d["meta"]))
        cs = d["cs_prec"].copy() if "cs_prec" in d.files else None
    metti_bordo(Z, meta["R_A"])
    return PO.campi(Z, rho_c, e, A, E), meta, cs


def corsa(L5, k_da, k_fino, reg):
    from solitone import _registro_corse as RC
    presidi()
    t00 = time.time()
    rho_c = MT.rho_c_assoluto()
    e = MT.PB.E_DECISO
    t0 = MT.G2.T0
    NOME, BASE = nomi(L5)
    F_GAUSS = BASE + "_gauss.json"
    print("=" * 130)
    print("R-SCATOLA AL 5%%, LA PROVA SUL MATTONE DA SOLO (Luca 16:17): L %d; da k %d a k %d; il tetto %g s; le mappe ogni %d" % (L5, k_da, k_fino, MT.TETTO_S, OGNI_MAPPA))
    print("=" * 130)
    with CV.scena_L(L5, FATTORE_R_A * R_OGG_MAX) as Z:
        L = Z["L"]
        assert L == L5
        from solitone import toro as TO
        print("### la scena: L %d, %d nodi; il centro del bordo %s; il raggio inscritto %.1f" % (L, Z["n"], Z["bordo"]["c0"], TO.meta_periodo(L)))
        if k_da == 0:
            fr = C243.francobollo_L162("MGU", 0)
            MT.vuoto_fresco(Z, t0)
            cd = nodo_buono(fr, Z["bordo"]["c0"], L)
            D = MT.incolla(Z, fr, cd, True)
            R, rr, b = r5(Z, t0)
            print("### incollato a %s (Delta %.6f); i raggi a k 0: %s; il baricentro (%.2f, %.2f)" % (cd, D, ", ".join("%g%% %s" % (100 * s, rr[s]) for s in sorted(rr, reverse=True)), b[0], b[1]))
            if R > R_OGG_MAX:
                print("### LA CORSA NON PARTE: R_ogg al 5%% %.1f > %g (la carta, sez. 2)" % (R, R_OGG_MAX))
                return 1
            metti_bordo(Z, FATTORE_R_A * R)
            if not regola(Z, R, "a k 0"):
                print("### LA CORSA NON PARTE: la regola al 5% non e' rispettata (FERMO, la correzione di Luca 16:58)")
                return 1
            C = PO.campi(Z, rho_c, e)
            g0 = C.residuo()
            soglia = FATTORE_GAUSS * g0
            with open(F_GAUSS, "w", encoding="utf-8", newline=chr(10)) as fh:
                json.dump({"L": L, "r0": g0, "soglia": soglia, "fattore": FATTORE_GAUSS, "R_ogg5": R, "R_A": FATTORE_R_A * R, "incollato": cd, "Delta": D, "codice": "csv/solitone/prova_scatola5.py"}, fh, indent=1)
            print("### il residuo di Gauss iniziale %.3e -> la soglia %.3e (%g volte, come il porto)" % (g0, soglia, FATTORE_GAUSS))
            cs = None
        else:
            with open(F_GAUSS, encoding="utf-8") as fh:
                soglia = float(json.load(fh)["soglia"])
            f_da, f_pr = [os.path.join(MT.DIR_E, "%s_%05d.npz" % (NOME, k)) for k in (k_da, k_da - PRIMA)]
            C, meta, cs = carica(Z, f_pr, rho_c, e)
            PO.accendi(cs)
            try:
                R0 = CT.Corsa(Z, C)
                R0.etichette([meta["centro"]])
                R0.inizio(k_da - PRIMA)
                for k in range(k_da - PRIMA + 1, k_da + 1):
                    R0.passo(k, t0 + k, 1.0, e)
            finally:
                LC.spegni()
            div = LG.uguale(Z, C, f_da)
            esito("la ripartenza da %s per %d tick = %s AL BIT (esclusa h_int)" % (os.path.basename(f_pr), PRIMA, os.path.basename(f_da)), not div, "diverse: %s" % div)
            if div:
                return 1
            C, meta, cs = carica(Z, f_da, rho_c, e)
            R = meta["R_ogg5"]
        S = {x: [] for x in ("pk_k", "picco", "k", "raggio", "M", "c1", "c2", "fuori", "r10", "r5", "r2", "gauss_k", "gauss")}
        MP = {"k": [], "rho": [], "dphi": []}
        PO.accendi(cs)
        fine = "finita"
        try:
            RC_ = CT.Corsa(Z, C)
            rho = MT.rho_di(Z)
            c = MT.centro_di(Z, rho)
            RC_.etichette([c])
            RC_.inizio(k_da)
            t1 = t_tappa = time.time()
            k = k_da
            for k in range(k_da, k_fino + 1):
                if k > k_da:
                    RC_.passo(k, t0 + k, 1.0, e)
                rho = MT.rho_di(Z)
                c = MT.centro_di(Z, rho)
                S["pk_k"].append(k)
                S["picco"].append(float(rho.max()))
                if (k - k_da) % CT.OGNI == 0:
                    RC_.etichette([c])
                if k % OGNI == 0:
                    rk, rr, _b = r5(Z, t0 + k)
                    S["k"].append(k)
                    S["raggio"].append(MR.raggio(Z, rho, c))
                    S["M"].append(float(rho.sum()))
                    S["c1"].append(c[0])
                    S["c2"].append(c[1])
                    S["fuori"].append(float(rho[Z["r_c0"] > Z["bordo"]["R_A"]].sum() / rho.sum()))
                    S["r10"].append(rr[0.10])
                    S["r5"].append(rr[0.05])
                    S["r2"].append(rr[0.02])
                if k % OGNI_MAPPA == 0:
                    MP["k"].append(k)
                    MP["rho"].append(rho.astype(np.float32))
                    MP["dphi"].append(PO.dphi_nodi(Z, t0 + k).astype(np.float32))
                if k % MT.OGNI_GAUSS == 0:
                    S["gauss_k"].append(k)
                    S["gauss"].append(C.residuo())
                if k % 250 == 0:
                    print("    k %5d  il picco %.4e  il raggio %.4f  la massa %.10e  oltre R_A %.3e  il 5%% del vuoto %s  Gauss %s  (%.0f s)" % (k, S["picco"][-1], S["raggio"][-1], S["M"][-1], S["fuori"][-1], S["r5"][-1],
                          "%.2e" % S["gauss"][-1] if S["gauss_k"] and S["gauss_k"][-1] == k else "--", time.time() - t00))
                    sys.stdout.flush()
                if k > k_da and (k % OGNI_STATO == 0 or k % OGNI_STATO == OGNI_STATO - PRIMA):
                    salva(Z, C, k, t0 + k, {"centro": [float(c[0]), float(c[1])], "R_ogg5": R}, NOME)
                adesso = time.time()
                if reg and adesso - t_tappa >= MT.TAPPA_S:
                    RC.tappa(reg, "k %d; %.3f s per tick; la memoria libera %.2f GB" % (k, (adesso - t1) / max(1, k - k_da), MT.memoria_gb()))
                    t_tappa = adesso
                if adesso - t1 > MT.TETTO_S:
                    fine = "il tetto di %g s a k %d (si riparte da %d)" % (MT.TETTO_S, k, (k // OGNI_STATO) * OGNI_STATO)
                    break
            if S["k"][-1] != k:
                rho = MT.rho_di(Z)
                S["k"].append(k)
                S["M"].append(float(rho.sum()))
                for x in ("raggio", "c1", "c2", "fuori", "r10", "r5", "r2"):
                    S[x].append(float("nan"))
        finally:
            LC.spegni()
        print("-" * 130)
        print("### %d tick in %.0f s (%.3f s per tick); %s" % (k - k_da, time.time() - t1, (time.time() - t1) / max(1, k - k_da), fine))
        RC_.tabella(["sol"])
        T = {x: np.array(v) for x, v in RC_.T.items()}
        bordoM = float(np.sum(T["Mp"] - T["Md"]))
        Rf, _rr, _b = r5(Z, t0 + k)
        regola(Z, Rf, "alla fine")
        Z["metti"]()
    np.savez_compressed(BASE + "_serie_%05d.npz" % k_da, **{x: np.array(v) for x, v in S.items()})
    f = BASE + "_mappe_%05d.npz" % k_da
    np.savez_compressed(f, tick=np.array(MP["k"], dtype=np.int32), rho=np.stack(MP["rho"]), dphi=np.stack(MP["dphi"]), L=np.int16(L5))
    print("### LE MAPPE: %d fotogrammi in %s, %.1f MB" % (len(MP["k"]), f, os.path.getsize(f) / 1e6))
    persa = S["M"][0] - S["M"][-1]
    print("### LA MASSA (alla stessa ultima misura, k %d): persa %.6e, uscita dal bordo %.6e, la differenza relativa %.3e" % (S["k"][-1], persa, bordoM, abs(persa - bordoM) / S["M"][0]))
    g = np.array(S["gauss"])
    esito("Gauss sotto la soglia (%.3e) a ogni controllo" % soglia, len(g) > 0 and float(g.max()) < soglia, "il massimo %.3e" % (float(g.max()) if len(g) else float("nan")))
    esito("la massa persa = la massa uscita dal bordo entro 1e-6 relativo", abs(persa - bordoM) / S["M"][0] <= 1e-6, "%.3e" % (abs(persa - bordoM) / S["M"][0]))
    print("=" * 130)
    print("ESITO: %d/%d controlli come devono; fallite %s; %s; %.0f s in tutto" % (OK[0], OK[1], FALLITE, fine, time.time() - t00))
    return 0 if not FALLITE else 1


# =====================================================================================
#   LA LETTURA: LE SOGLIE DELLA CARTA, sez. 3
# =====================================================================================
def periodo(k, p, da, a):
    """### Il periodo del respiro: la frequenza dominante della FFT del picco meno la media mobile su 101 tick, sui tick `[da, a]` *(la carta)*."""
    k = np.asarray(k)
    p = np.asarray(p, dtype=float)
    m = (k >= da - 50) & (k <= a + 50)
    k, p = k[m], p[m]
    o = np.argsort(k)
    k, p = k[o], p[o]
    assert np.all(np.diff(k) == 1), "il picco non e' a ogni tick"
    mm = np.convolve(p, np.ones(101) / 101.0, mode="same")
    q = (p - mm)[(k >= da) & (k <= a)]
    F = np.abs(np.fft.rfft(q - q.mean()))
    f = np.fft.rfftfreq(len(q), 1.0)
    j = 1 + int(np.argmax(F[1:]))
    return 1.0 / f[j]


def lettura(L5):
    import _presidio
    _presidio.avvia(__file__)
    print("=" * 130)
    print("R-SCATOLA AL 5%, LA LETTURA (la carta, sez. 3: le soglie fissate PRIMA)")
    print("=" * 130)
    S = {}
    _n, BASE = nomi(L5)
    print("### la corsa: L %d (%s_serie_*.npz)" % (L5, BASE))
    for f in sorted(glob.glob(BASE + "_serie_*.npz")):
        s = np.load(f)
        for x in s.files:
            S.setdefault(x, []).extend(list(s[x]))
    k5 = {int(a): i for i, a in enumerate(S["k"])}
    pk5 = dict(zip([int(a) for a in S["pk_k"]], S["picco"]))
    # ---------------------------------------------------------------- L 243 dal referto (la riga di ogni 250)
    R243 = {}
    for r in open(os.path.join(MT.DIR_REF, "conv_GU_L243.txt"), encoding="utf-8"):
        m = re.match(r"\s+k\s+(\d+)\s+il picco ([0-9.e+-]+)\s+il raggio ([0-9.]+)", r)
        if m:
            R243[int(m.group(1))] = (float(m.group(2)), float(m.group(3)))
    s3 = np.load(os.path.join(MT.DIR_REF, "porto_cottura_serie_00000.npz"))
    R324 = {int(a): float(b) for a, b in zip(s3["k"], s3["raggio"])}
    P324 = {int(a): float(b) for a, b in zip(s3["pk_k"], s3["picco"])}
    righe = []
    for nome, rif_r, rif_p in (("L 243", {k: v[1] for k, v in R243.items()}, {k: v[0] for k, v in R243.items()}), ("L 324", R324, P324)):
        comuni = sorted(k for k in rif_r if k in k5 and k > 0)
        dr = [abs(S["raggio"][k5[k]] - rif_r[k]) / rif_r[k] for k in comuni]
        dp = [abs(pk5[k] - rif_p[k]) / rif_p[k] for k in comuni if k in pk5 and k in rif_p]
        print("### %s: i tick comuni %d (%s ... %s)" % (nome, len(comuni), comuni[0] if comuni else "-", comuni[-1] if comuni else "-"))
        print("    il raggio della materia: il peggio %.3f%% (a k %d)" % (100 * max(dr), comuni[int(np.argmax(dr))]))
        print("    il picco: il peggio %.3f%%" % (100 * max(dp)))
        righe.append(("il raggio della materia contro %s entro l'1%% a ogni tick comune" % nome, max(dr) <= 0.01, "il peggio %.3f%%" % (100 * max(dr))))
        righe.append(("il picco contro %s entro il 2%% a ogni tick comune" % nome, max(dp) <= 0.02, "il peggio %.3f%%" % (100 * max(dp))))
    T5 = periodo(S["pk_k"], S["picco"], 250, 1750)
    T3 = periodo(s3["pk_k"], s3["picco"], 250, 1750)
    print("### il periodo del respiro (tick 250-1750): L %d %.2f, L 324 %.2f tick; la differenza %.3f%%" % (L5, T5, T3, 100 * abs(T5 - T3) / T3))
    righe.append(("il periodo del respiro contro L 324 entro il 3%", abs(T5 - T3) / T3 <= 0.03, "%.2f contro %.2f" % (T5, T3)))
    A = {}
    for r in open(os.path.join(MT.DIR_REF, "porto_alone_vuoto.txt"), encoding="utf-8"):
        m = re.match(r"\s+(L \d+)\s+k\s+(\d+):.*i raggi: (.*?); la meta'", r)
        if m:
            A[(m.group(1), int(m.group(2)))] = {float(x.split("%")[0]) / 100: x.split("% ")[1] for x in m.group(3).split(", ")}
    for (nome, k) in (("L 324", 950), ("L 324", 1000), ("L 243", 2000)):
        rif = float(A[(nome, k)][0.05])
        mio = float(S["r5"][k5[k]])
        print("### il raggio del 5%% del vuoto a k %d: L %d %.0f, %s %.0f" % (k, L5, mio, nome, rif))
        righe.append(("il raggio del 5%% del vuoto a k %d contro %s entro 1 nodo" % (k, nome), abs(mio - rif) <= 1.0, "%.0f contro %.0f" % (mio, rif)))
    print("-" * 130)
    for che, ok, nota in righe:
        esito(che, ok, nota)
    print("    (la massa: il DEVE della corsa, nel suo referto)")
    print("=" * 130)
    print("ESITO: %d/%d soglie; fallite %s -> R-SCATOLA al 5%% %s" % (OK[0], OK[1], FALLITE, "ADOTTATA (se la massa passa)" if not FALLITE else "### NON ADOTTATA: FERMO"))
    return 0 if not FALLITE else 1


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("cosa", choices=("corsa", "lettura"))
    ap.add_argument("--L", type=int, required=True)
    ap.add_argument("--da", type=int)
    ap.add_argument("--fino", type=int)
    ap.add_argument("--registro")
    x = ap.parse_args(argv)
    if x.cosa == "corsa":
        return corsa(x.L, x.da, x.fino, x.registro)
    return lettura(x.L)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
