r"""**DOVE PUO' NASCERE LA LUCE SUI TRIANGOLI: il regime `s -> 1` e la moneta** *(solo spettri, in memoria; [[DECISIONE-SOLO-TRIANGOLI]], [[LUCE-VINCOLO-LAMPI-GAMMA]], [[SPAZIOTEMPO-3PIU1]])*.

> ### ⛔ **Il task history e' `2026-10-24_triangoli_dove_la_luce.md`** *(il metodo, le previsioni, i criteri, fissati prima)*. ### **`leggi.yaml`, l'impronta, la convenzione nel repo e il nucleo intatti.**
> ### **Importati, non copiati:** `_triangoli.scarto_c6`, `_triangoli_bassa_energia.matrice`, `_triangoli_forza` *(`v_max`, `coppia_K`, `blocchi`, `matrice_L`)*, `_triangoli_fattore.ramo_lungo`, `_triangoli_luce`
> *(`blocchi_di`, `dispersione`, `livelli`, `av`, `PUNTI`)*.

### **LE PAROLE:** ### **«il limite `s <= 1`»** *(la regola `B-5`)*, ### **«il regime `s -> 1`», «`v_max`»** *(la velocita' massima di gruppo misurata)*.

Gira con:  python csv/_triangoli_dove_la_luce.py > doc/referti_l2/triangoli_dove_la_luce.txt
"""
import io
import json
import math
import os
import subprocess
import sys
import time
import warnings

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
_PO = os.path.join(RADICE, "primo_ordine")
for _p in (_QUI, _PO, os.path.join(_PO, "leggi")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import numpy as np                                             # noqa: E402

RIF_BASSA = "8781162c"
RIF_FATTORE = "7daa8840"
RIF_LUCE = "77f9f850"
NB = 12
NV = 6
L = 48
S_A = (0.5, 0.7, 0.9, 0.95, 0.99, 0.999, 1.0)
S_B = (0.05, 0.3, 0.5, 0.9)
EPS_B = (0.0, 0.1, 0.25, 0.5, 0.75, 1.0, math.pi / 2.0)
CONV = ("simm", "oggi")
KMAX = 0.1
NK = 200
TOLL_LIV = 1e-9
TOLL_RIF = 1e-9
TOLL_VMAX = 1e-6
TOLL_C6 = 1e-12
TOLL_UNO = 0.01
TOLL_LUCE = 0.05
JSONL = os.path.join(RADICE, "doc", "referti_l2", "triangoli_dove_la_luce.jsonl")
OK = [0, 0]


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    print("  %-90s %s   %s" % (che[:90], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return passa


def scrivi(r):
    with io.open(JSONL, "a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(r) + "\n")


def f_(x, fm="%+.4f"):
    return "--" if x is None else fm % x


def git_jsonl(rif, rel):
    return [json.loads(x) for x in subprocess.run(["git", "show", "%s:%s" % (rif, rel)], capture_output=True, cwd=RADICE, check=True).stdout.decode("utf-8").splitlines() if x.strip()]


def livelli_cerchio(w):
    """### I livelli di `_triangoli_luce.livelli`, ### **uniti SUL CERCHIO** *(`-pi` e `+pi` sono lo stesso livello)*."""
    import _triangoli_luce as TL
    lv = TL.livelli(np.array([TL.av(x) for x in w]))
    if len(lv) > 1 and abs(TL.av(lv[-1][0] - lv[0][0])) < TOLL_LIV:
        lv[-1][1] += lv[0][1]
        lv = lv[1:]
    return lv


def settore(eps, s, nome):
    """### Gli spettri della materia e del vuoto, ai quattro punti: i livelli sul cerchio, i tocchi e la loro dispersione, il salto minimo fra livelli distinti sulla zona."""
    import _triangoli as T
    import _triangoli_bassa_energia as BE
    import _triangoli_luce as TL
    vero = T.EPS_MONETA
    A = BE.matrice(eps, s, L, nome)
    c6 = float(T.scarto_c6(A))
    out = {"c6": c6}
    for sett, sl in (("materia", slice(0, NB)), ("vuoto", slice(NB, NB + NV))):
        V = A[:, :, sl, sl]
        bl = TL.blocchi_di(V)
        W = -np.angle(np.linalg.eigvals(V))
        pt = {}
        for pn, pk in TL.PUNTI.items():
            lv = livelli_cerchio(W[pk])
            tocchi = []
            for w, m in lv:
                if m > 1 or abs(TL.av(w)) < TOLL_LIV:
                    rami = TL.dispersione(bl, pk, w, m)
                    if any(r["tipo"] != "piatto" for r in rami):
                        tocchi.append({"livello": w, "molteplicita": m, "rami": rami})
            pt[pn] = {"livelli": lv, "tocchi": tocchi}
        gmin, kmin = 9.0, None
        for i in range(L):
            for j in range(L):
                xs = [x for x, _m in livelli_cerchio(W[i, j])]
                if len(xs) < 2:
                    continue
                g = min(abs(TL.av(xs[(q + 1) % len(xs)] - xs[q])) for q in range(len(xs)))
                if g < gmin:
                    gmin, kmin = g, (i, j)
        lineari = [{"punto": pn, "livello": tc["livello"], "pendenza_su_s": r["pendenza"] / s, "anisotropia": r["anisotropia"]}
                   for pn, d in pt.items() for tc in d["tocchi"] for r in tc["rami"] if r["tipo"] == "lineare"]
        out[sett] = {"punti": pt, "salto_min": gmin, "k_salto_min": list(kmin) if kmin else None, "lineari": lineari, "V": V, "bl": bl}
    T.EPS_MONETA = vero
    return out


def coppia_pi(sp, s):
    """### La coppia attraverso `pi` a `Gamma` *(materia)*: il salto `2 pi - (alto - basso)` e la `v` di Einstein rispetto al centro `pi` *(dalla dispersione quadratica del livello alto)*."""
    import _triangoli_luce as TL
    # ### ⚠ il salto attraverso `pi` si legge sui livelli NON uniti sul cerchio (annotazione 1): uniti, a `s = 1` il livello a `pi` non sta piu' fra il piu' alto e il piu' basso
    lv = TL.livelli(-np.angle(np.linalg.eigvals(sp["materia"]["V"][0, 0])))
    xs = sorted(x for x, _m in lv)
    if len(xs) < 2:
        return None
    alto, basso = xs[-1], xs[0]
    salto = max(2.0 * np.pi - (alto - basso), 0.0)
    if salto < TOLL_LIV:
        salto = 0.0
    m_alto = [m for x, m in lv if x == alto][0]
    r = [q for q in TL.dispersione(sp["materia"]["bl"], (0, 0), alto, m_alto) if q["tipo"] == "quadratico"]
    v = math.sqrt(0.5 * salto * r[0]["curvatura"]) if (r and salto > TOLL_LIV) else None
    return {"salto": float(salto), "salto_su_s": float(salto / s), "v_einstein": v, "v_einstein_su_s": None if v is None else v / s}


def coppia_K_vb(eps, s):
    """### La coppia a `K` *(`_triangoli_forza.coppia_K`)*: il salto, e `v_b` dal fit iperbolico di `7daa8840` *(`ramo_lungo`, `k_max 0.1`, `200` punti)*."""
    import _triangoli_fattore as TFa
    import _triangoli_forza as TF
    bande = TF.coppia_K(eps, s)
    bl = TF.blocchi(eps, s)
    out = []
    for b in bande:
        qq, ww = TFa.ramo_lungo(bl, b["Q"], b["w"], KMAX * math.sqrt(3.0) / 2.0, NK)
        k = qq * 2.0 / math.sqrt(3.0)
        y = ww ** 2 - b["w"] ** 2
        X = np.stack([k ** 2, k ** 4], axis=1)
        c, *_ = np.linalg.lstsq(X, y, rcond=None)
        out.append({"w": b["w"], "v_b": float(math.sqrt(c[0])) if c[0] > 0 else None})
    return {"salto": float(abs(bande[1]["w"] - bande[0]["w"])), "bande": out}


def vmax_tutti(eps, s):
    import _triangoli_forza as TF
    A = TF.matrice_L(eps, s)
    vm, km, _w = TF.v_max(A)
    A2 = np.zeros((L, L, NB + NV, NB + NV), dtype=complex)
    A2[:, :, :NV, :NV] = A[:, :, NB:, NB:]
    A2[:, :, NV:NB, NV:NB] = np.eye(NB - NV)
    vv, kv, _w = TF.v_max(A2)
    return {"materia": vm, "vuoto": vv, "tutti": max(vm, vv), "k_materia": list(km), "k_vuoto": list(kv)}


def riga(eps, s, parte):
    t0 = time.time()
    rec = {"tipo": "riga", "parte": parte, "eps": eps, "s": s}
    c6 = 0.0
    for nome in CONV:
        sp = settore(eps, s, nome)
        c6 = max(c6, sp["c6"])
        rec[nome] = {sett: {k: v for k, v in sp[sett].items() if k not in ("V", "bl")} for sett in ("materia", "vuoto")}
        if nome == "simm":
            rec["coppia_pi"] = coppia_pi(sp, s)
    rec["c6"] = c6
    rec["v_max"] = vmax_tutti(eps, s)
    rec["coppia_K"] = coppia_K_vb(eps, s)
    vb = [b["v_b"] for b in rec["coppia_K"]["bande"] if b["v_b"]]
    rec["v_b_su_s"] = [x / s for x in vb]
    rec["v_b_su_v_max"] = [x / rec["v_max"]["tutti"] for x in vb]
    scrivi(rec)
    cp = rec["coppia_pi"] or {}
    print("  %s eps %-6.4g s %-6g: v_max/s %.4f (materia %.4f, vuoto %.4f) | coppia a K: salto %.5f, v_b/s %s, v_b/v_max %s | attraverso pi a Gamma: salto %s, v/s %s | c6 %.1e (%.0f s)"
          % (parte, eps, s, rec["v_max"]["tutti"] / s, rec["v_max"]["materia"] / s, rec["v_max"]["vuoto"] / s, rec["coppia_K"]["salto"], " ".join("%.4f" % x for x in rec["v_b_su_s"]),
             " ".join("%.4f" % x for x in rec["v_b_su_v_max"]), f_(cp.get("salto"), "%.5f"), f_(cp.get("v_einstein_su_s"), "%.4f"), c6, time.time() - t0))
    for nome in CONV:
        for sett in ("materia", "vuoto"):
            d = rec[nome][sett]
            tt = "; ".join("%s %+.4f(x%d): %s" % (pn, tc["livello"], tc["molteplicita"], ",".join(r["tipo"][:4] + ("" if r["esponente"] is None else "%.2f" % r["esponente"]) for r in tc["rami"]))
                           for pn, p in d["punti"].items() for tc in p["tocchi"])
            print("      %-4s %-7s salto minimo %.2e a %s | lineari: %s | tocchi: %s" % (nome, sett, d["salto_min"], d["k_salto_min"],
                                                                                   " ".join("%s v/s %.4f (aniso %.1e)" % (x["punto"], x["pendenza_su_s"], x["anisotropia"]) for x in d["lineari"]) or "nessuno", tt or "nessuno"))
    sys.stdout.flush()
    return rec


def main(argv):
    del argv
    import _presidio
    import _universalita_massa as UM
    import composizione as CM
    _presidio.avvia(__file__)
    warnings.simplefilter("ignore")
    print("=" * 110)
    print("DOVE PUO' NASCERE LA LUCE SUI TRIANGOLI: il regime s -> 1 e la moneta (solo spettri)")
    print("=" * 110)
    blobs = {r: UM.blob(r) for r in ("soliton_simulator.py", "csv/_triangoli.py", "csv/_triangoli_bassa_energia.py", "csv/_triangoli_forza.py", "csv/_triangoli_fattore.py",
                                     "csv/_triangoli_luce.py", "csv/_zero_simmetrico.py", "csv/_triangoli_dove_la_luce.py")}
    print("  il passo: %d pezzi, impronta %s (intatto); i blob nel repo: %s" % (len(CM.ORDINE), CM.IMPRONTA, "; ".join("%s %s" % (k, v["sha1-BYTE"]) for k, v in blobs.items())))
    print("  la configurazione: RIF %s %s %s; L %d; S_A %s; S_B %s; EPS_B %s; CONV %s; KMAX %g; NK %d; TOLL_LIV %g TOLL_RIF %g TOLL_VMAX %g TOLL_C6 %g TOLL_UNO %g TOLL_LUCE %g"
          % (RIF_BASSA, RIF_FATTORE, RIF_LUCE, L, S_A, S_B, EPS_B, CONV, KMAX, NK, TOLL_LIV, TOLL_RIF, TOLL_VMAX, TOLL_C6, TOLL_UNO, TOLL_LUCE))
    print("-" * 110)
    sys.stdout.flush()
    io.open(JSONL, "w", encoding="utf-8").close()
    scrivi({"tipo": "testata", "blobs": blobs})
    print("### PARTE A -- IL REGIME s -> 1 (eps 0; a s = 1 la scena NON e' rifiutata: si usa s = 1.0)")
    ra = [riga(0.0, s, "A") for s in S_A]
    print("### L'ANDAMENTO VERSO s = 1: l'esponente locale d ln|f(1) - f(s)| / d ln(1 - s) fra 0.9, 0.99, 0.999")
    uno = ra[-1]
    for nome, fn in (("v_max/s", lambda r: r["v_max"]["tutti"] / r["s"]), ("v_b/s (K)", lambda r: r["v_b_su_s"][0]), ("salto a K", lambda r: r["coppia_K"]["salto"]),
                     ("salto attraverso pi", lambda r: r["coppia_pi"]["salto"])):
        y = {r["s"]: fn(r) for r in ra}
        ps = []
        for a, b in ((0.9, 0.99), (0.99, 0.999)):
            da, db = abs(y[1.0] - y[a]), abs(y[1.0] - y[b])
            ps.append(math.log(da / db) / math.log((1 - a) / (1 - b)) if da > 0 and db > 0 else None)
        scrivi({"tipo": "andamento", "che": nome, "y": {str(k): v for k, v in y.items()}, "esponenti": ps})
        print("  %-20s %s | a s = 1: %.5f | esponenti %s" % (nome, " ".join("%g:%.5f" % (k, v) for k, v in y.items()), y[1.0], " ".join(f_(p, "%.3f") for p in ps)))
    print("-" * 110)
    print("### PARTE B -- LA MONETA (eps %s; s %s; la coppia a K seguita in eps e' <<il modo massivo piu' basso>>, dichiarato)" % (", ".join("%.4g" % e for e in EPS_B), S_B))
    rb = []
    for eps in EPS_B:
        for s in S_B:
            if eps == 0.0 and s == 0.5:
                rb.append([r for r in ra if r["s"] == 0.5][0])
                continue
            rb.append(riga(eps, s, "B" + (" ### eps 0.5, LA SCELTA DI LUCA" if eps == 0.5 else "")))
    print("-" * 110)
    print("### I CONTROLLI")
    rif_b = [r for r in git_jsonl(RIF_BASSA, "doc/referti_l2/triangoli_bassa_energia.jsonl") if r.get("tipo") == "salto_minimo" and r["eps"] == 0.0 and r["s"] == 0.3]
    rif_f = [r for r in git_jsonl(RIF_FATTORE, "doc/referti_l2/triangoli_fattore.jsonl") if r.get("tipo") == "fattori" and r["eps"] == 0.0 and r["s"] == 0.3 and r["banda"] == 0]
    rif_l = [r for r in git_jsonl(RIF_LUCE, "doc/referti_l2/triangoli_luce.jsonl") if r.get("tipo") == "cono" and r["s"] == 0.3]
    r03 = [r for r in rb if r["eps"] == 0.0 and r["s"] == 0.3][0]
    d1 = abs(r03["coppia_K"]["salto"] - rif_b[0]["salto"])
    d2 = abs(r03["coppia_K"]["bande"][0]["v_b"] - rif_f[0]["fattori"]["v_b"]["c"])
    d3 = abs(r03["v_max"]["materia"] - rif_l[0]["v_max_materia"])
    esito("DEVE PASSARE: a s 0.3, eps 0: il salto a K = %s, v_b = %s entro %g; v_max = %s entro %g" % (RIF_BASSA, RIF_FATTORE, TOLL_RIF, RIF_LUCE, TOLL_VMAX),
          d1 <= TOLL_RIF and d2 <= TOLL_RIF and d3 <= TOLL_VMAX, "%.1e %.1e %.1e" % (d1, d2, d3))
    tutte = ra + [r for r in rb if r not in ra]
    peg = max(r["c6"] for r in tutte)
    esito("DEVE PASSARE: lo spettro invariante per 60 gradi (sul cerchio) entro %g a ogni (eps, s), le due convenzioni" % TOLL_C6, peg < TOLL_C6, "il peggiore %.2e" % peg)
    lin03 = [x for nome in CONV for sett in ("materia", "vuoto") for x in r03[nome][sett]["lineari"]]
    tocchi03 = sum(len(p["tocchi"]) for nome in CONV for sett in ("materia", "vuoto") for p in r03[nome][sett]["punti"].values())
    esito("DEVE FALLIRE: <<a eps 0, s 0.3 esiste un modo lineare senza massa>> (la chiave: dei tocchi trovati, nessuno lineare)", tocchi03 > 0 and not lin03,
          "%d tocchi, %d lineari" % (tocchi03, len(lin03)))
    esito("PUO' FALLIRE: a s = 1, eps 0, v_max/s entro %g da 1" % TOLL_UNO, abs(uno["v_max"]["tutti"] - 1.0) <= TOLL_UNO, "%.4f" % uno["v_max"]["tutti"])
    lin1 = [x for nome in CONV for sett in ("materia", "vuoto") for x in uno[nome][sett]["lineari"]]
    esito("PUO' FALLIRE: a s = 1, eps 0, esiste un tocco lineare (senza massa)", bool(lin1), " ".join("%s v/s %.4f" % (x["punto"], x["pendenza_su_s"]) for x in lin1))
    buoni = []
    for r in tutte:
        if r["s"] > 0.5:
            continue
        lin = [x for nome in CONV for sett in ("materia", "vuoto") for x in r[nome][sett]["lineari"]]
        for x in lin:
            for vb in r["v_b_su_s"]:
                if abs(x["pendenza_su_s"] - vb) / vb < TOLL_LUCE:
                    buoni.append((r["eps"], r["s"], x["pendenza_su_s"], vb))
    nlin = sum(len(r[nome][sett]["lineari"]) for r in tutte if r["s"] <= 0.5 for nome in CONV for sett in ("materia", "vuoto"))
    esito("PUO' FALLIRE: un (eps, s <= 0.5) con un modo lineare senza massa a velocita' entro il 5%% da v_b della coppia a K", bool(buoni),
          "%d lineari a s <= 0.5; buoni: %s" % (nlin, buoni[:4]))
    print("=" * 110)
    print("DOVE PUO' NASCERE LA LUCE: %d su %d controlli   %s  (il verdetto di fisica sono le tabelle)" % (OK[0], OK[1], "### TUTTI PASSATI" if OK[0] == OK[1] else "### CI SONO BUCHI"))
    print("=" * 110)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
