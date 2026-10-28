# -*- coding: utf-8 -*-
r"""**LA RILETTURA DELLA BUCA CONTRO IL CONGELATO** *(la risposta di Luca delle `14:27` del `2026-10-28`, parte `1`; [[VUOTO-SUL-FONDO]], [[PROGETTO-MASSA-COLLETTIVA]];
il task history `doc/TASK_HISTORY/2026-10-28_rilettura_buca_e_deriva.md`)*: ### **sui dati di `bd87c0d5`, senza corse nuove:** ### **la larghezza di ogni corsa diviso quella del
congelato allo stesso tick, dalla fine della rampa;** ### **la vita e lo scarto relativi;** ### **la tanh contro il `sin^2` a durata uguale, dove i dati lo permettono.**

> ### ⚠ **IL LIMITE DEI DATI** *(dichiarato prima dei numeri)*: ### **il congelato c'e' solo col fondo e fino al tick `8000`:** ### **il rapporto esiste solo sui tick comuni `<= 8000`.**
> ### **L'uniforme usa il congelato del fondo SOLO con `--uniforme-vale`,** ### **cioe' se `(c0)` di `_deriva_congelato` e' passato al bit.**

    python csv/_rilettura_buca.py [--uniforme-vale] > doc/referti_l2/rilettura_buca.txt
"""
import io
import json
import math
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
_PO = os.path.join(RADICE, "primo_ordine")
for _p in (_QUI, _PO, os.path.join(_PO, "leggi")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

PARTI = os.path.join(RADICE, "doc", "referti_l2", "solitone_con_la_buca")
SALITA = (0.1, 0.9)            # ### il tempo di salita: da r = 0.1 a r = 0.9


def carica():
    corse = {}
    for n in sorted(os.listdir(PARTI)):
        if n.endswith(".jsonl"):
            x = json.loads(io.open(os.path.join(PARTI, n), encoding="utf-8").read())
            if x.get("tipo") == "corsa":
                corse[(x["taglia"], x["scena"], x["modo"])] = x
    return corse


def tempi_rampa(forma, T_r, s):
    """### **Dalla funzione `rampa` dello script delle corse:** ### **il tick in cui `r = 1`, e il tempo di salita `10%`-`90%`, in tempo fisico.**"""
    import _solitone_con_la_buca as B
    t10 = t90 = None
    t = 0
    while True:
        r = B.rampa(t, forma, T_r, s)
        if t10 is None and r >= SALITA[0]:
            t10 = t
        if t90 is None and r >= SALITA[1]:
            t90 = t
        if r == 1.0:
            return {"durata": t * s, "t_rampa": t, "salita": (t90 - t10) * s}
        t += 1


def rilettura(r, cong, toll, fmin):
    """### **Il rapporto `w / w_cong` sui tick comuni dopo la rampa** *(e durante, come lettura)*."""
    wc = {x["t"]: x["larghezza"] for x in cong["serie"]}
    comuni = [x for x in r["serie"] if x["t"] in wc]
    dopo = [x for x in comuni if x["t"] >= r["t_rampa"]]
    prima = [x for x in comuni if x["t"] < r["t_rampa"]]
    rel = [(x["t"], x["larghezza"] / wc[x["t"]], x["frazione"]) for x in dopo]
    vita = None
    for t, q, fr in rel:
        if abs(q - 1.0) > toll or fr < fmin:
            vita = t - r["t_rampa"]
            break
    return {"n_comuni_dopo": len(rel), "ultimo_comune": rel[-1][0] if rel else None, "vita_rel": vita,
            "scarto_max_dopo": max(abs(q - 1.0) for _t, q, _f in rel) if rel else None,
            "scarto_max_in_rampa": max(abs(x["larghezza"] / wc[x["t"]] - 1.0) for x in prima) if prima else None,
            "q_fine_rampa": rel[0][1] if rel else None, "q_ultimo": rel[-1][1] if rel else None}


def vita_testo(v, r):
    if v["n_comuni_dopo"] == 0:
        return "non misurabile (nessun tick comune dopo la rampa)"
    if v["vita_rel"] is None:
        return "oltre %d tick dopo la rampa (tempo fisico %.1f)" % (v["ultimo_comune"] - r["t_rampa"], (v["ultimo_comune"] - r["t_rampa"]) * r["s"])
    return "%d tick (tempo fisico %.1f)" % (v["vita_rel"], v["vita_rel"] * r["s"])


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    import _solitone_con_la_buca as B
    import _solitoni_triangoli as STR
    uniforme_vale = "--uniforme-vale" in argv
    corse = carica()
    toll, fmin = STR.TOLL_LARGH, STR.FRAZ_MIN
    print("=" * 130)
    print("LA RILETTURA DELLA BUCA CONTRO IL CONGELATO (Luca 14:27, parte 1): w(t) / w_congelato(t) sui tick comuni dopo la rampa; i dati di bd87c0d5, nessuna corsa")
    print("=" * 130)
    print("  la configurazione: TOLL_LARGH %g FRAZ_MIN %g (la frazione ASSOLUTA); SALITA %s; il riferimento: <taglia>_fondo_congelato; l'uniforme contro il congelato del fondo: %s"
          % (toll, fmin, SALITA, "SI (--uniforme-vale: (c0) di _deriva_congelato al bit)" if uniforme_vale else "NO (senza riferimento)"))
    print("  la correzione e' dichiarata DOPO i numeri di 58791831; quel referto resta com'e'")
    print("-" * 130)
    out = {}
    for t in B.TAGLIE:
        cong = corse[(t, "fondo", "congelato")]
        print("### %s: il congelato fino al tick %d; la sua larghezza / w_in a 4000 e a 8000: %.4f, %.4f"
              % (t, cong["T_MAX"], [x["larghezza"] for x in cong["serie"] if x["t"] == 4000][0] / cong["w_in"],
                 [x["larghezza"] for x in cong["serie"] if x["t"] == 8000][0] / cong["w_in"]))
        for sc in B.SCENE:
            if sc == "uniforme" and not uniforme_vale:
                print("  %-8s: senza riferimento" % sc)
                continue
            for m in B.MODI_RAMPA:
                r = corse[(t, sc, m)]
                v = rilettura(r, cong, toll, fmin)
                out[(t, sc, m)] = v
                print("  %-8s %-8s rampa fino al tick %5d: la vita relativa %s; scarto relativo massimo dopo %s, in rampa %s; w/w_cong alla fine della rampa %s, all'ultimo tick comune %s"
                      % (sc, m, r["t_rampa"], vita_testo(v, r), "%.3f" % v["scarto_max_dopo"] if v["scarto_max_dopo"] is not None else "-",
                         "%.3f" % v["scarto_max_in_rampa"] if v["scarto_max_in_rampa"] is not None else "-",
                         "%.4f" % v["q_fine_rampa"] if v["q_fine_rampa"] is not None else "-", "%.4f" % v["q_ultimo"] if v["q_ultimo"] is not None else "-"))
    print("-" * 130)
    print("### LA VITA RELATIVA CONTRO T_r (la tanh e il sin^2; None = non si rompe fino all'ultimo tick comune; - = non misurabile)")
    for t in B.TAGLIE:
        for sc in B.SCENE:
            if sc == "uniforme" and not uniforme_vale:
                continue
            for f in B.FORME:
                vv = []
                for T in B.T_RAMPE:
                    v = out[(t, sc, "%s%g" % (f, T))]
                    vv.append("-" if v["n_comuni_dopo"] == 0 else ("oltre" if v["vita_rel"] is None else str(v["vita_rel"])))
                print("  %-7s %-8s %-4s T_r %s: %s" % (t, sc, f, list(B.T_RAMPE), vv))
    print("-" * 130)
    print("### LA DURATA UGUALE (le funzioni di rampa dello script delle corse, s %g)" % B.S_CORSA)
    tr = {(f, T): tempi_rampa(f, T, B.S_CORSA) for f in B.FORME for T in B.T_RAMPE}
    for (f, T), d in sorted(tr.items()):
        print("  %-4s T_r %3g: durata %.3f, salita 10-90%% %.3f (tick di fine %d)" % (f, T, d["durata"], d["salita"], d["t_rampa"]))
    uguali = [(a, b) for a in tr for b in tr if a[0] == "tanh" and b[0] == "sin2" and (abs(tr[a]["durata"] - tr[b]["durata"]) < B.S_CORSA or abs(tr[a]["salita"] - tr[b]["salita"]) < B.S_CORSA)]
    print("  coppie tanh/sin^2 a durata o salita UGUALE (entro un tick): %s" % (uguali if uguali else "NESSUNA"))
    if not uguali:
        vic = []
        for a in [k for k in tr if k[0] == "tanh"]:
            b = min([k for k in tr if k[0] == "sin2"], key=lambda k: abs(math.log(tr[k]["salita"] / tr[a]["salita"])))
            vic.append((a, b, tr[a]["salita"] / tr[b]["salita"]))
        print("  le piu' vicine per tempo di salita (NON uguali):")
        for a, b, q in sorted(vic):
            for t in B.TAGLIE:
                for sc in B.SCENE:
                    if sc == "uniforme" and not uniforme_vale:
                        continue
                    va, vb = out[(t, sc, "%s%g" % a)], out[(t, sc, "%s%g" % b)]
                    print("    tanh T_r %g contro sin2 T_r %g (salita tanh/sin2 %.3f) %-7s %-8s: vita relativa %s contro %s"
                          % (a[1], b[1], q, t, sc, "-" if va["n_comuni_dopo"] == 0 else va["vita_rel"], "-" if vb["n_comuni_dopo"] == 0 else vb["vita_rel"]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
