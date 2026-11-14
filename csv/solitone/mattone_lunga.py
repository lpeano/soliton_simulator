# -*- coding: utf-8 -*-
r"""**LA COTTURA LUNGA: IL MATTONE SI FERMA O SI DISSOLVE?** *(Luca `2026-11-14` `14:13`, L1-L7; la carta `doc/TASK_HISTORY/2026-11-13_strumento_mattone.md`, sez. `17`)*.

    python csv/solitone/mattone_lunga.py corsa --caso MGU|MU --registro lunga-<caso> > <scratchpad>/lunga_<caso>.txt   (poi doc/referti_l2/mattone/lunga_<caso>.txt)
    python csv/solitone/mattone_lunga.py referto > doc/referti_l2/mattone/lunga.txt   (e lunga_raggio_massa.png accanto)

### **`corsa`:** **(MGU) da `MGU_10000`, (MU) da `MU_05000`** *(il caricamento di `mattone_cottura_U`: `U` ricostruito dal campo)*, **campi pieni, la stessa legge, NESSUN arresto per «cotto»; pezzi di `1000` tick, lo
stato a fine pezzo su E: col prefisso `lunga_`; il tetto `18000` s.** **(MU) si ferma al primo pezzo in cui ha fatto ALMENO i tick di (MGU) finita** *(se (MGU) e' finita)*, **o al tetto** *(mio: il confronto del referto si fa
sui tick COMUNI)*. **Il picco, il raggio, la massa, il centro ogni `50` tick; il respiro a OGNI tick; per pezzo: S5' sulle due serie, i conti** *(la media sugli ultimi `100` tick)* **e la massa uscita dal bordo.**
### **L4, ARRESTO** *(un risultato, non un FERMO)*: **il picco sotto il `10%` di quello di partenza** *((MGU): `1291.6`, il picco medio dell'ultimo pezzo della cottura; (MU): il picco del suo stato di partenza, mio)*, **o la massa sotto
il `50%` di quella iniziale, o il raggio oltre `20` nodi.**
### **DEVE:** **i primi `50` tick di (MGU) = gli stessi `50` tick rifatti con `mattone_cottura.Corsa` e il caricamento di `mattone_cottura_U` AL BIT** *(esclusa `h_int`)*; **la somma dei pezzi dei conti ESATTA a ogni pezzo** *(`conti.pezzi`)*.
"""
import argparse
import json
import os
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_CSV = os.path.dirname(_QUI)
for _p in (_QUI, _CSV):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import conti as CO  # noqa: E402
import mattone as MT  # noqa: E402
import mattone_cottura as CT  # noqa: E402
import mattone_cottura_U as CU  # noqa: E402
import mattone_rhoc as MR  # noqa: E402

PARTENZA = {"MGU": 10000, "MU": 5000}     # ### L1
PICCO_COTTO_MGU = 1291.6                  # ### L4 (Luca 14:13): il picco medio dell'ultimo pezzo della cottura (aa0606f7)
PEZZO, OGNI, N_DEVE = 1000, 50, 50
TETTO_S = 18000.0                         # ### L2
SOGLIA_PICCO, SOGLIA_MASSA, RAGGIO_MAX = 0.10, 0.50, 20.0   # ### L4
DIR_REF = MT.DIR_REF
OK = [0, 0]
FALLITE = []


def esito(che, passa, nota, deve):
    OK[1] += 1
    buono = passa if deve else not passa
    OK[0] += 1 if buono else 0
    if not buono:
        FALLITE.append(che)
    print("  %s: %-100s %s   %s" % ("DEVE PASSARE" if deve else "DEVE FALLIRE", che[:100], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()


def json_di(caso):
    return os.path.join(DIR_REF, "lunga_%s.json" % caso)


def corsa(caso, nome_reg):
    import _presidio
    import _vuoto_vivo_B as V
    for m in ("mattone", "mattone_cottura", "mattone_cottura_U", "mattone_rhoc", "conti"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(os.path.join(_CSV, "_u1_prototipo.py"))
    _presidio.avvia(__file__)
    assert caso in PARTENZA
    t00 = time.time()
    rho_c = MT.rho_c_assoluto()
    e = MT.PB.E_DECISO
    k0 = PARTENZA[caso]
    print("=" * 130)
    print("LA COTTURA LUNGA (%s; Luca 14:13): da %s_%05d, campi pieni, nessun arresto per cotto; pezzi di %d tick, lo stato con il prefisso lunga_; il tetto %g s; L4: il picco sotto %g, la massa sotto %g, il raggio oltre %g"
          % (caso, caso, k0, PEZZO, TETTO_S, SOGLIA_PICCO, SOGLIA_MASSA, RAGGIO_MAX))
    print("=" * 130)
    with MT.scena(MT.CORSA_BASE, MT.T_BASE) as Z:
        # ---------------------------------------------------------------- il DEVE: i primi 50 tick = quelli di mattone_cottura (Corsa) col caricamento di mattone_cottura_U
        rif = None
        if caso == "MGU":
            C, _f = CU.carica_U(Z, caso, rho_c, k0)
            R = CT.Corsa(Z, C)
            R.etichette([MT.centro_di(Z, MT.rho_di(Z))])
            R.inizio(k0)
            for k in range(k0 + 1, k0 + N_DEVE + 1):
                R.passo(k, MT.T_BASE + k, 1.0, e)
                if k % CT.OGNI == 0:
                    R.etichette([MT.centro_di(Z, MT.rho_di(Z))])
            rif = {kk: Z["st"][kk].copy() for kk in Z["chiavi"]}
            rif.update(campo_A=C.campo.A.copy(), campo_E=C.campo.E.copy())
        # ---------------------------------------------------------------- la corsa lunga
        C, f0 = CU.carica_U(Z, caso, rho_c, k0)
        R = CT.Corsa(Z, C)
        rho = MT.rho_di(Z)
        c = MT.centro_di(Z, rho)
        R.etichette([c])
        R.inizio(k0)
        picco0 = PICCO_COTTO_MGU if caso == "MGU" else float(rho.max())
        M0 = float(rho.sum())
        S = {x: [] for x in ("k", "rmax", "raggio", "M", "c1", "c2")}
        RESP = {"k": [], "resp": []}
        P = []

        def misura(k):
            rho = MT.rho_di(Z)
            c = MT.centro_di(Z, rho)
            RESP["k"].append(k)
            RESP["resp"].append(MT.respiro(rho))
            if k % OGNI == 0:
                S["k"].append(k)
                S["rmax"].append(float(rho.max()))
                S["raggio"].append(MR.raggio(Z, rho, c))
                S["M"].append(float(rho.sum()))
                S["c1"].append(c[0])
                S["c2"].append(c[1])
            if k % CT.OGNI == 0:
                R.etichette([c])
        misura(k0)
        print("### la partenza %s: il picco %.4e (il riferimento di L4 %.4e), la massa %.10e, il raggio %.4f" % (f0, float(rho.max()), picco0, M0, S["raggio"][0]))
        t1 = t_tappa = time.time()
        k, arresto, fine = k0, None, None
        while fine is None:
            for k in range(k + 1, k + PEZZO + 1):
                R.passo(k, MT.T_BASE + k, 1.0, e)
                misura(k)
                if rif is not None and k == k0 + N_DEVE:
                    div = [x for x in rif if x not in CU.CHIAVI_SERVIZIO and not np.array_equal(rif[x], C.campo.A if x == "campo_A" else C.campo.E if x == "campo_E" else Z["st"][x])]
                    esito("i primi %d tick di (MGU) lunga = gli stessi tick con mattone_cottura.Corsa e mattone_cottura_U AL BIT (esclusa h_int)" % N_DEVE, not div, "diverse: %s" % div, True)
                    if div:
                        fine = "il DEVE dei primi %d tick FALLISCE: FERMO" % N_DEVE
                        break
                if k % OGNI == 0:
                    i = -1
                    if S["rmax"][i] < SOGLIA_PICCO * picco0:
                        arresto = "il picco %.4e sotto il %g di %.4e" % (S["rmax"][i], SOGLIA_PICCO, picco0)
                    elif S["M"][i] < SOGLIA_MASSA * M0:
                        arresto = "la massa %.6e sotto il %g di %.6e" % (S["M"][i], SOGLIA_MASSA, M0)
                    elif S["raggio"][i] > RAGGIO_MAX:
                        arresto = "il raggio %.4f oltre %g nodi" % (S["raggio"][i], RAGGIO_MAX)
                    if arresto:
                        fine = "ARRESTO L4 a k %d: %s (il solitone non esiste piu': un risultato)" % (k, arresto)
                        break
                if time.time() - t1 > TETTO_S:
                    fine = "il tetto di %g s a k %d" % (TETTO_S, k)
                    break
            if fine and "FERMO" in fine:
                break
            # ---------------------------------------------------------------- il pezzo: lo stato, S5', i conti, il bordo
            f = os.path.join(MT.DIR_E, "lunga_%s_%05d.npz" % (caso, k))
            dati = {kk: Z["st"][kk] for kk in Z["chiavi"]}
            dati.update(campo_A=C.campo.A, campo_E=C.campo.E)
            np.savez(f, meta=np.array(json.dumps({"caso": caso, "k": k, "t": MT.T_BASE + k, "e": e, "rho_c": rho_c, "sha": V.shas(Z["z"]), "codice": "csv/solitone/mattone_lunga.py"})), **dati)
            kk_r = np.array(RESP["k"])
            a = k - PEZZO
            s5, _ff = CT.s5p(kk_r, RESP["resp"], k) if k - k0 >= PEZZO else (float("nan"), None)
            k50 = kk_r % 50 == 0
            s5_50, _ff = CT.s5p(kk_r[k50], np.array(RESP["resp"])[k50], k) if k - k0 >= PEZZO else (float("nan"), None)
            T = {x: np.array(v) for x, v in R.T.items()}
            n = len(T["k"])
            ii = slice(max(1, n - 100), n)
            bordoM = float(np.sum(T["Mp"] - T["Md"]))
            bordoE = float(np.sum(T["totp"] + T["KVp"] - T["totd"] - T["KVd"]))
            res = float(np.mean(T["totd"][ii] + T["KVd"][ii])) - (T["totd"][0] + T["KVd"][0]) + bordoE
            cc = (S["c1"][-1], S["c2"][-1])
            PZ = CO.pezzi(Z, [cc], C.campo)
            jj = (np.array(S["k"]) > a) & (np.array(S["k"]) <= k)
            riga = {"k": k, "picco": float(np.mean(np.array(S["rmax"])[jj])), "raggio": float(np.mean(np.array(S["raggio"])[jj])), "M": S["M"][-1], "s5": s5, "s5_50": s5_50,
                    "materia": float(T["mat"][ii, 0].mean()), "fuori": float(T["mat"][ii, 1].mean()), "vuoto": float(T["vuo"][ii, 0].mean()), "KV": float(T["KVd"][ii].mean()),
                    "tot": float(T["totd"][ii].mean()), "bordoE": bordoE, "bordoM": bordoM, "residuo": res, "esatta": bool(PZ["somma_esatta_ok"]), "secondi": time.time() - t1,
                    "deriva": MT.distanza(Z["L"], cc, (S["c1"][0], S["c2"][0]))}
            P.append(riga)
            print("### pezzo fino a k %6d (%6.0f s): picco medio %.4e  raggio medio %.4f  massa %.10e  S5' %.4f (ogni 50: %.4f)  deriva %.4f  | materia %.6e fuori %.4e vuoto %.4e K+V %.4e tot %.6f | bordo E %+.4f M %.6e | residuo %+.4f | esatta %s"
                  % (k, riga["secondi"], riga["picco"], riga["raggio"], riga["M"], s5, s5_50, riga["deriva"], riga["materia"], riga["fuori"], riga["vuoto"], riga["KV"], riga["tot"], bordoE, bordoM, res, riga["esatta"]))
            sys.stdout.flush()
            if not riga["esatta"]:
                esito("la somma dei pezzi dei conti esatta a k %d" % k, False, "", True)
                fine = "la somma dei pezzi NON esatta: FERMO"
                break
            with open(json_di(caso), "w", encoding="utf-8", newline="\n") as fh:
                json.dump({"caso": caso, "k0": k0, "k": k, "finita": fine is not None, "fine": fine, "pezzi": P}, fh, indent=1)
            if time.time() - t_tappa >= 0:
                MT.tappa(nome_reg, "k %d; %.3f s per tick; il raggio medio %.4f; la memoria libera %.2f GB" % (k, (time.time() - t1) / (k - k0), riga["raggio"], MT.memoria_gb()))
                t_tappa = time.time()
            if caso == "MU" and os.path.exists(json_di("MGU")):
                with open(json_di("MGU"), encoding="utf-8") as fh:
                    jm = json.load(fh)
                if jm.get("finita") and (k - k0) >= (jm["k"] - jm["k0"]):
                    fine = "(MU) ha fatto %d tick, almeno quelli di (MGU) finita (%d)" % (k - k0, jm["k"] - jm["k0"])
    esito("la somma dei pezzi dei conti esatta a ogni pezzo (%d pezzi)" % len(P), all(p["esatta"] for p in P) and len(P) > 0, "", True)
    os.makedirs(DIR_REF, exist_ok=True)
    np.savez_compressed(os.path.join(DIR_REF, "lunga_%s_serie.npz" % caso), resp_k=np.array(RESP["k"]), resp=np.array(RESP["resp"]), **{x: np.array(v) for x, v in S.items()})
    with open(json_di(caso), "w", encoding="utf-8", newline="\n") as fh:
        json.dump({"caso": caso, "k0": k0, "k": k, "finita": True, "fine": fine, "arresto": arresto, "pezzi": P}, fh, indent=1)
    print("=" * 130)
    print("ESITO: %s; %d tick; %d/%d controlli come devono; fallite %s; %.0f s in tutto" % (fine, k - k0, OK[0], OK[1], FALLITE, time.time() - t00))
    return 0 if not FALLITE else 1


# =====================================================================================
#   IL REFERTO UNICO (L5)
# =====================================================================================
def tendenza(x, y):
    """### La velocita' per pezzo `dy/dx` e se RALLENTA, RESTA COSTANTE o ACCELERA *(la retta delle velocita' contro il tempo: la pendenza relativa sull'intervallo, soglia `+-25%`, mia)*."""
    v = np.diff(y) / np.diff(x)
    if len(v) < 3:
        return v, "troppo pochi pezzi", float("nan")
    p = np.polyfit(x[1:], v, 1)
    rel = p[0] * (x[-1] - x[1]) / abs(np.mean(v)) if np.mean(v) != 0 else float("nan")
    lett = "RALLENTA" if rel < -0.25 else ("ACCELERA" if rel > 0.25 else "RESTA COSTANTE")
    return v, lett, rel


def referto():
    import _presidio
    _presidio.avvia(__file__)
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    print("=" * 130)
    print("LA COTTURA LUNGA, IL REFERTO UNICO (Luca 14:13, L5): il raggio e la massa nel tempo; la velocita' per pezzo; (MGU) contro (MU); la massa uscita dal bordo contro la massa persa")
    print("=" * 130)
    J, SR = {}, {}
    for caso in ("MGU", "MU"):
        with open(json_di(caso), encoding="utf-8") as fh:
            J[caso] = json.load(fh)
        SR[caso] = np.load(os.path.join(DIR_REF, "lunga_%s_serie.npz" % caso))
        print("### (%s) da k %d a k %d (%d tick); la fine: %s" % (caso, J[caso]["k0"], J[caso]["k"], J[caso]["k"] - J[caso]["k0"], J[caso]["fine"]))
    n_com = min(len(J["MGU"]["pezzi"]), len(J["MU"]["pezzi"]))
    print("### i pezzi COMUNI: %d (il confronto si fa su questi)" % n_com)
    for caso in ("MGU", "MU"):
        pz = J[caso]["pezzi"]
        x = np.array([J[caso]["k0"]] + [p["k"] for p in pz], dtype=float) - J[caso]["k0"]
        s = SR[caso]
        r0, m0 = float(s["raggio"][0]), float(s["M"][0])
        rg = np.array([r0] + [p["raggio"] for p in pz])
        ms = np.array([m0] + [p["M"] for p in pz])
        vr, lr, rr = tendenza(x, rg)
        vm, lm, rm = tendenza(x, ms)
        print("-" * 130)
        print("### (%s) IL RAGGIO: la velocita' per pezzo (nodi per tick) %s" % (caso, " ".join("%+.2e" % v for v in vr)))
        print("    la lettura: %s (la variazione relativa della velocita' sull'intervallo %+.2f)" % (lr, rr))
        if lr == "RALLENTA" and len(vr) >= 3 and vr[-1] > 0 and vr[0] > vr[-1]:
            tau = (x[-1] - x[1]) / np.log(vr[1] / vr[-1]) if vr[1] > vr[-1] > 0 else float("nan")
            print("    il raggio di arrivo stimato (la velocita' che cala come esp(-t/tau), tau %.0f tick): %.3f" % (tau, rg[-1] + vr[-1] * tau))
        elif len(vr) and vr[-1] > 0:
            print("    a velocita' costante (l'ultima %.2e) il raggio arriva a %g nodi fra %.0f tick" % (vr[-1], RAGGIO_MAX, (RAGGIO_MAX - rg[-1]) / vr[-1]))
        print("### (%s) LA MASSA: la velocita' per pezzo (per tick) %s" % (caso, " ".join("%+.3e" % v for v in vm)))
        print("    la lettura: %s (%+.2f); relativa per tick nell'ultimo pezzo %.3e" % (lm, rm, vm[-1] / ms[-1] if len(vm) else float("nan")))
        if len(vm) and vm[-1] < 0:
            print("    a velocita' costante la massa arriva al %g dell'iniziale fra %.0f tick" % (SOGLIA_MASSA, (ms[-1] - SOGLIA_MASSA * m0) / -vm[-1]))
        bM = pz[-1]["bordoM"]
        print("### (%s) la massa persa %.6e; la massa uscita dal bordo %.6e; il rapporto %.4f %s" % (caso, m0 - ms[-1], bM, bM / (m0 - ms[-1]) if m0 != ms[-1] else float("nan"),
              "(TORNANO: la massa va nel bordo)" if abs(bM / (m0 - ms[-1]) - 1.0) < 0.05 else "(NON tornano: dove va il resto?)"))
        print("    la tabella per pezzo: k, il picco medio, il raggio medio, la massa, S5', S5' ogni 50, la deriva, il residuo dei conti")
        for p in pz:
            print("    %7d %.4e %8.4f %.10e %.4f %.4f %.4f %+12.4f" % (p["k"], p["picco"], p["raggio"], p["M"], p["s5"], p["s5_50"], p["deriva"], p["residuo"]))
    print("-" * 130)
    print("### (MGU) CONTRO (MU), PEZZO PER PEZZO (i tick dalla partenza; il raggio medio; la massa relativa all'iniziale)")
    for j in range(n_com):
        a, b = J["MGU"]["pezzi"][j], J["MU"]["pezzi"][j]
        print("    +%6d  raggio %.4f / %.4f   massa %.6f / %.6f" % (a["k"] - J["MGU"]["k0"], a["raggio"], b["raggio"], a["M"] / float(SR["MGU"]["M"][0]), b["M"] / float(SR["MU"]["M"][0])))
    fig, ax = plt.subplots(1, 2, figsize=(11, 4))
    for caso, col in (("MGU", "#3b6fb6"), ("MU", "#c9822b")):
        s = SR[caso]
        t = np.array(s["k"], dtype=float) - J[caso]["k0"]
        ax[0].plot(t, s["raggio"], color=col, lw=1.2, label="(%s)" % caso)
        ax[1].plot(t, np.array(s["M"]) / float(s["M"][0]), color=col, lw=1.2, label="(%s)" % caso)
    ax[0].set_xlabel("tick dalla partenza")
    ax[0].set_ylabel("raggio (nodi)")
    ax[1].set_xlabel("tick dalla partenza")
    ax[1].set_ylabel("massa / massa iniziale")
    for a_ in ax:
        a_.grid(alpha=0.3)
        a_.legend(frameon=False)
        for sp in ("top", "right"):
            a_.spines[sp].set_visible(False)
    fig.suptitle("La cottura lunga: (MGU) da k 10000, (MU) da k 5000")
    fig.tight_layout()
    png = os.path.join(DIR_REF, "lunga_raggio_massa.png")
    fig.savefig(png, dpi=110)
    print("=" * 130)
    print("### il grafico: %s" % png)
    return 0


def main(argv):
    if argv and argv[0] == "referto":
        return referto()
    ap = argparse.ArgumentParser()
    ap.add_argument("azione", choices=("corsa",))
    ap.add_argument("--caso", required=True, choices=sorted(PARTENZA))
    ap.add_argument("--registro")
    x = ap.parse_args(argv)
    return corsa(x.caso, x.registro)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
