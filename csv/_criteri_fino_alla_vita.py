# -*- coding: utf-8 -*-
r"""**I CRITERI `2` E `3` DEL CONTO DELL'ENERGIA DEL LEGAME, FINO ALLA VITA** *([[ENERGIA-DEL-LEGAME]]; la parte 1 del mandato dopo `15df5c63`;
il task history `doc/TASK_HISTORY/2026-10-27_criteri_fino_alla_vita.md`)*: ### **legge il jsonl di `csv/_energia_del_legame.py` e rivaluta i criteri
`2` e `3` sul massimo per `t <= vita`** *(la correzione dichiarata dopo i numeri, decisione di Luca delle `12:37`)*; ### **la differenza fra i due zeri
nel tempo, col fit esponenziale da `vita` a `T_MAX`, e i due controlli del fit;** ### **la luce: il fronte e `v_max` in unita' di `c = s`.**
### **Nessuna corsa nuova.**

Gira con:  python csv/_criteri_fino_alla_vita.py > doc/referti_l2/criteri_fino_alla_vita.txt
"""
import io
import json
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
for _p in (_QUI, os.path.join(RADICE, "primo_ordine")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

RIF = os.path.join(RADICE, "doc", "referti_l2", "energia_del_legame.jsonl")
JSONL = os.path.join(RADICE, "doc", "referti_l2", "criteri_fino_alla_vita.jsonl")
VITA = {1e6: 320, 1e5: 140}
T_MAX = 2000
PEZZI = ("cost", "cin", "leg", "vuo", "tot")
REGIONI = ("vicino", "lontano", "totale")
TOLL_2 = 1e-3
TOLL_3 = 1e-6
R2_MIN = 0.9            # ### la lettura «regolare» del task history
SALTO = 1.0             # ### un salto: log10 g cresce di piu' di una decade fra due punti
S = 0.3
C_LUCE = S              # ### `c = r s` archi per tick, `r = 1` sul piatto (`0764d566`)
SEME = 20261027
P1_R = 0.01
P1_RUMORE = 0.1
P1_TOLL = 0.05

_esiti = []


def esito(nome, ok, dettaglio):
    _esiti.append((nome, ok))
    print("  %-110s %s   %s" % (nome[:110], "PASSA" if ok else "### FALLISCE", dettaglio))


def scrivi(r):
    io.open(JSONL, "a", encoding="utf-8", newline="\n").write(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n")


def delta(x, t, reg, pz):
    a = [s for s in x["serie"] if s["t"] == t][0]
    return a["E"][reg][pz] - x["serie"][0]["E"][reg][pz]


def scarto_zeri(s_, o_, t):
    """### Il peggiore su regioni e pezzi di `|Delta E(simm) - Delta E(oggi) - 2 pi (lambda_s - lambda_o) Delta norma| / N |e_K(0)|`
    *(la stessa formula di `_energia_del_legame_dove.py`)*."""
    sc = s_["N"] * abs(s_["e_K"])
    peg = (0.0, "")
    for reg in REGIONI:
        for pz in PEZZI:
            c = 0.0
            if pz in ("cost", "tot"):
                c += 2 * math.pi * (s_["lambda"] - o_["lambda"]) * delta(o_, t, reg, "M")
            if pz in ("vuo", "tot"):
                c += 2 * math.pi * (s_["lambda"] - o_["lambda"]) * delta(o_, t, reg, "V")
            x = abs(delta(s_, t, reg, pz) - delta(o_, t, reg, pz) - c) / sc
            if x > peg[0]:
                peg = (x, "%s %s" % (reg, pz))
    return peg


def fit(tt, gg):
    """### Il fit di `ln g` contro `t`: il tasso per tick, `R^2`, e i salti *(i passi in cui `log10 g` cresce di piu' di `SALTO`)*."""
    tt = np.asarray(tt, float)
    lg = np.log(np.asarray(gg, float))
    a, b = np.polyfit(tt, lg, 1)
    res = lg - (a * tt + b)
    r2 = 1.0 - float(np.sum(res ** 2)) / float(np.sum((lg - lg.mean()) ** 2))
    d10 = np.diff(lg) / math.log(10.0)
    salti = [(int(tt[i + 1]), float(d10[i])) for i in range(len(d10)) if d10[i] > SALTO]
    return float(a), r2, salti


def main(argv):
    del argv
    import _presidio
    import _universalita_massa as UM
    _presidio.avvia(__file__)
    if os.path.exists(JSONL):
        os.remove(JSONL)
    print("=" * 130)
    print("I CRITERI 2 E 3 DEL CONTO DELL'ENERGIA DEL LEGAME, FINO ALLA VITA (la correzione dichiarata dopo i numeri, Luca 12:37); LA DIFFERENZA FRA I DUE ZERI NEL TEMPO; LA LUCE")
    print("=" * 130)
    blobs = {p: UM.blob(p) for p in ("csv/_criteri_fino_alla_vita.py", "csv/_energia_del_legame.py", "csv/_energia_del_legame_dove.py", "doc/referti_l2/energia_del_legame.jsonl")}
    print("  i blob nel repo: %s" % "; ".join("%s %s" % (k, v["sha1-BYTE"]) for k, v in blobs.items()))
    print("  la configurazione: VITA %s T_MAX %d TOLL_2 %g TOLL_3 %g R2_MIN %g SALTO %g S %g C_LUCE %g SEME %d P1 r %g rumore %g toll %g"
          % (VITA, T_MAX, TOLL_2, TOLL_3, R2_MIN, SALTO, S, C_LUCE, SEME, P1_R, P1_RUMORE, P1_TOLL))
    scrivi({"tipo": "testata", "blobs": blobs})
    righe = [json.loads(l) for l in io.open(RIF, encoding="utf-8")]
    cc = [r for r in righe if r.get("tipo") == "corsa"]
    v_max = [r for r in righe if r.get("tipo") == "esito"][0]["v_max"]
    for x in cc:
        assert x["vita20"] == VITA[x["N"]] or x["modo"] == "congelato", (x["N"], x["L"], x["modo"], x["vita20"])   # ### la vita a 20 tick (74f99039); a 10 tick N 1e5 da' 130
    print("-" * 130)
    print("### I CONTROLLI DELLO STRUMENTO DEL FIT (sulla griglia dei tempi di N 1e5: da 140 a 2000 ogni 10)")
    tt = list(range(VITA[1e5], T_MAX + 1, 10))
    rng = np.random.default_rng(SEME)
    g1 = [1e-14 * math.exp(P1_R * t) * math.exp(P1_RUMORE * rng.standard_normal()) for t in tt]
    a1, r21, s1 = fit(tt, g1)
    esito("DEVE PASSARE (p1): un esponenziale sintetico col rumore del %g%%: il tasso entro il %g%% e R2 >= %g, nessun salto" % (100 * P1_RUMORE, 100 * P1_TOLL, R2_MIN),
          abs(a1 - P1_R) <= P1_TOLL * P1_R and r21 >= R2_MIN and not s1, "tasso %.5f R2 %.4f salti %d" % (a1, r21, len(s1)))
    g2 = [1e-14 if t < 500 else 1e-5 for t in tt]
    a2, r22, s2 = fit(tt, g2)
    esito("DEVE PASSARE (p2): un gradino a t 500: la lettura dice NON regolare", not (r22 >= R2_MIN and not s2), "tasso %.5f R2 %.4f salti %s" % (a2, r22, s2))
    print("-" * 130)
    print("### (2) LE TAGLIE, IL MASSIMO PER t <= vita: |Delta E(L1) - Delta E(L2)| / N |e_K(0)|, il totale di ogni pezzo")
    peg2 = (0.0, "")
    for N in (1e6, 1e5):
        for z in ("simm", "oggi"):
            for m in ("intero", "congelato"):
                a, b = [x for x in cc if x["N"] == N and x["zero"] == z and x["modo"] == m]
                sc = N * abs(a["e_K"])
                mx = (0.0, 0, "")
                for t in range(0, VITA[N] + 1, 10):
                    for pz in PEZZI:
                        v = abs(delta(a, t, "totale", pz) - delta(b, t, "totale", pz)) / sc
                        if v > mx[0]:
                            mx = (v, t, pz)
                print("  N %-7g %-4s %-9s: il peggiore per t <= %d: %.2e (t %d, %s)" % (N, z, m, VITA[N], mx[0], mx[1], mx[2]))
                scrivi({"tipo": "taglie", "N": N, "zero": z, "modo": m, "peggiore": mx[0], "t": mx[1], "pezzo": mx[2]})
                if mx[0] > peg2[0]:
                    peg2 = (mx[0], "N %g %s %s t %d %s" % (N, z, m, mx[1], mx[2]))
    print("### (3) I DUE ZERI, IL MASSIMO PER t <= vita: ogni regione e pezzo, tolto 2 pi lambda volte la norma")
    peg3 = (0.0, "")
    serie_g = {}
    for N in (1e6, 1e5):
        for L in sorted({x["L"] for x in cc if x["N"] == N}):
            for m in ("intero", "congelato"):
                s_, o_ = [x for x in cc if x["N"] == N and x["L"] == L and x["modo"] == m and x["zero"] in ("simm", "oggi")]
                if s_["zero"] != "simm":
                    s_, o_ = o_, s_
                g = [(t, scarto_zeri(s_, o_, t)) for t in range(0, T_MAX + 1, 10)]
                serie_g[(N, L, m)] = g
                mx = max((x[1][0], x[0], x[1][1]) for x in g if x[0] <= VITA[N])
                print("  N %-7g L %3d %-9s: il peggiore per t <= %d: %.2e (t %d, %s)" % (N, L, m, VITA[N], mx[0], mx[1], mx[2]))
                scrivi({"tipo": "zeri", "N": N, "L": L, "modo": m, "peggiore": mx[0], "t": mx[1], "dove": mx[2],
                        "serie": [{"t": t, "g": v[0], "dove": v[1]} for t, v in g]})
                if mx[0] > peg3[0]:
                    peg3 = (mx[0], "N %g L %d %s t %d %s" % (N, L, m, mx[1], mx[2]))
    print("-" * 130)
    print("### LA DIFFERENZA FRA I DUE ZERI NEL TEMPO, DALLA VITA A T_MAX (tick intero): il fit di ln g contro t; regolare se R2 >= %g e nessun salto di piu' di %g decade in 10 tick" % (R2_MIN, SALTO))
    for (N, L, m), g in sorted(serie_g.items(), key=lambda kv: (-kv[0][0], kv[0][1], kv[0][2])):
        if m != "intero":
            continue
        dopo = [(t, v[0]) for t, v in g if t >= VITA[N]]
        nulli = [t for t, v in dopo if v <= 0.0]
        if nulli:
            print("  N %-7g L %3d: %d punti con g = 0 (il primo a t %d): il fit non si fa" % (N, L, len(nulli), nulli[0]))
            continue
        tt_, gg_ = [t for t, _ in dopo], [v for _, v in dopo]
        a, r2, salti = fit(tt_, gg_)
        meta = len(tt_) // 2
        a_1, _r1, _s1 = fit(tt_[:meta + 1], gg_[:meta + 1])
        a_2, _r2, _s2 = fit(tt_[meta:], gg_[meta:])
        prima = max(v[0] for t, v in g if t <= VITA[N])
        regolare = r2 >= R2_MIN and not salti
        print("  %sN %-7g L %3d: g alla vita %.2e, a T_MAX %.2e (fino alla vita il massimo %.2e); il tasso %.5f per tick, R2 %.4f, salti %s; il tasso nella prima meta' %.5f (t %d-%d), nella seconda %.5f (t %d-%d) -> %s"
              % ("### " if (N, L) == (1e5, 48) else "", N, L, gg_[0], gg_[-1], prima, a, r2, salti if salti else "nessuno",
                 a_1, tt_[0], tt_[meta], a_2, tt_[meta], tt_[-1], "REGOLARE" if regolare else "NON REGOLARE"))
        scrivi({"tipo": "crescita", "N": N, "L": L, "tasso": a, "R2": r2, "salti": salti, "tasso_prima_meta": a_1, "tasso_seconda_meta": a_2,
                "g_vita": gg_[0], "g_tmax": gg_[-1], "regolare": regolare})
    print("-" * 130)
    print("### LA LUCE: c = s = %g archi per tick (0764d566); il fronte del vuoto e v_max della coppia in unita' di c" % C_LUCE)
    for x in sorted(cc, key=lambda x: (-x["N"], x["L"], x["modo"], x["zero"])):
        if x["velocita_fronte"] is None:   # ### col vuoto congelato non c'e' un fronte del vuoto
            print("  N %-7g L %3d %-9s %-4s: nessun fronte (il vuoto non si muove)" % (x["N"], x["L"], x["modo"], x["zero"]))
            continue
        print("  N %-7g L %3d %-9s %-4s: il fronte %.4f archi per tick = %.3f c (punti del fit %d)" % (x["N"], x["L"], x["modo"], x["zero"], x["velocita_fronte"], x["velocita_fronte"] / C_LUCE, x["punti_fronte"]))
    print("  v_max della coppia %.6f archi per tick = %.3f c" % (v_max, v_max / C_LUCE))
    scrivi({"tipo": "luce", "c": C_LUCE, "v_max": v_max, "v_max_su_c": v_max / C_LUCE,
            "fronti": [{"N": x["N"], "L": x["L"], "modo": x["modo"], "zero": x["zero"], "v": x["velocita_fronte"], "v_su_c": x["velocita_fronte"] / C_LUCE} for x in cc if x["velocita_fronte"] is not None]})
    print("-" * 130)
    print("### I CRITERI CORRETTI (dopo i numeri, Luca 12:37)")
    esito("DEVE PASSARE (2'): le taglie, il massimo per t <= vita, entro %g di N |e_K(0)|" % TOLL_2, peg2[0] <= TOLL_2, "%.2e (%s)" % peg2)
    esito("DEVE PASSARE (3'): i due zeri, il massimo per t <= vita, entro %g di N |e_K(0)|" % TOLL_3, peg3[0] <= TOLL_3, "%.2e (%s)" % peg3)
    print("-" * 130)
    fall = [n for n, ok in _esiti if not ok and n.startswith("DEVE")]
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (sum(ok for _, ok in _esiti), len(_esiti), len(fall), fall))
    scrivi({"tipo": "esito", "passano": sum(ok for _, ok in _esiti), "totale": len(_esiti), "deve_fallite": fall})
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
