# -*- coding: utf-8 -*-
r"""**IL PILOTA DI `TL120`: LO SPARPAGLIO DELLE PARTENZE SU `L 81`** *(Luca `2026-11-05` `14:14`; il task history `doc/TASK_HISTORY/2026-11-05_TL120_densita_o_rientro.md`)*
    python csv/solitone/carta_pilota.py --corsa PL1 > doc/referti_l2/pilota_PL1.txt      # il referto breve di un seme (PL1 .. PL4)
    python csv/solitone/carta_pilota.py > doc/referti_l2/pilota_tl120.txt                # il referto del pilota: lo sparpaglio di ln t e il numero di semi del secondo stadio
### **Il seme** `PLk`: la partenza di `TF3` piu' il rumore relativo `1e-10` *(il seme `k`)*, `F3`, senza bordo, fino a `30000` o all'arresto *(`partenza.py`: il primo blocco di `1000` sopra `5` per `1000`,
l'arresto `2000` dopo)*. ### **I DEVE di un seme:** `R0` il rumore registrato = la configurazione *(l'ampiezza, il seme)*; `R0-F` *(deve fallire)* il primo campione = quello di `TF3` al bit *(il rumore c'e')*;
`PA` la partenza registrata in corsa = quella riletta dai campioni *(`partenza.rileggi`)*; `A4` il libro col par della corsa. **Le misure:** la partenza, l'arresto, la velocita' e la direzione per blocco, la distanza
del centro da quello di `TF3` *(`D5` a `1e-10`)*. ### **Il pilota:** le partenze dei semi, la media e la deviazione standard di `ln t` *(`TF3`, senza rumore, stampata accanto, non contata)*, **il numero di semi
che servirebbe al secondo stadio** *(la formula dichiarata in `diag_tl120_costo.py.txt`: `n >= 2 (z sd / (ln 2.19 - ln 1.48))^2`, a `2` e `3` sigma)*.
"""
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))
import solitone  # noqa: E402,F401  (i percorsi)

SEMI = ("PL1", "PL2", "PL3", "PL4")
DIST = math.log((120.0 / 81.0) ** 2) - math.log(120.0 / 81.0)   # ### la distanza da risolvere fra densita' e rientro (diag_tl120_costo)

OK = [0, 0]
FALLITE = []


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    if not passa:
        FALLITE.append(che)
    print("  %-120s %s   %s" % (che[:120], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return passa


def seme(nome, s, CA, CD, PA, T3, TO, V, c3):
    rr, cc, _d, _a = CA.serie(nome)
    if not rr:
        print("### %s: NESSUN PEZZO" % nome)
        return None
    L = rr[0]["L"]
    A1, A2 = TO.vettori()
    ult = rr[-1]
    amp, sm = CA.RUMORE[nome]
    esito("DEVE PASSARE: R0 %s il rumore registrato = la configurazione (ampiezza %g, seme %d), in ogni pezzo" % (nome, amp, sm),
          all(r.get("rumore", {}).get("ampiezza") == amp and r["rumore"].get("seme") == sm for r in rr), "sha della partenza %s" % rr[0].get("rumore", {}).get("sha_partenza"))
    esito("DEVE FALLIRE: R0-F %s il primo campione e' quello di TF3 al bit" % nome, not cc[0]["per"] == c3[0]["per"], "w %s %.15f, TF3 %.15f" % (nome, cc[0]["per"]["w"], c3[0]["per"]["w"]))
    st, ferma = PA.rileggi(cc, s, L, A1, A2, CD.pendenza)
    reg = ult.get("partenza", {}).get("t_p")
    esito("DEVE PASSARE: PA %s la partenza registrata in corsa = quella riletta dai campioni" % nome, reg == st["t_p"], "in corsa %s, riletta %s" % (reg, st["t_p"]))
    esito("DEVE PASSARE: A4 %s il libro col par della corsa" % nome, all(r.get("libro") == "col par della corsa" and r["eps"] == V.EPS for r in rr), "")
    print("  %s: %d pezzi, fino al tick %d (tempo %.1f); ### L'ARRESTO: %s" % (nome, len(rr), ult["t1"], ult["t1"] * s, ult.get("fermata") or ("la fine a %g" % (ult["t_fine"] * s) if ult["t1"] >= ult["t_fine"] else "### NON FINITA")))
    tq, X, ww, fl, _al = T3.traiettoria(cc, L, s)
    righe = CD.finestre(nome, tq, X, ww, fl, 0.0, float(tq[-1]), PA.PASSO, False)
    print("  la velocita' e la direzione per blocco (per 1000, gradi): %s" % "; ".join("%.0f %.2f %+.0f" % (a, v, ang) for a, _b, v, ang, _w, _x, _m in righe))
    t3, X3, _w3, _f3, _a3 = T3.traiettoria(c3, L, s)
    k = min(len(tq), len(t3))
    d = np.hypot(*(X[:k] - X3[:k]).T)
    pr = [(tt, float(d[i])) for i, tt in enumerate(tq[:k]) if i % 667 == 0]
    print("  ### D5 a 1e-10: la distanza del centro da quello di TF3 (nodi), ogni ~1000: %s" % "; ".join("%.0f %.2e" % x for x in pr))
    if st["t_p"] is not None:
        rb = [r for r in righe if r[0] == st["t_p"]]
        if rb:
            print("  ### la partenza a %g: la velocita' %.2f per 1000, la direzione %+.1f gradi (TF3: 16000, %.2f per 1000)" % (st["t_p"], rb[0][2], rb[0][3], 14.007))
    return st["t_p"]


def main(argv):
    import _presidio
    import _vuoto_vivo_B as V
    from solitone import carta_deriva as CD
    from solitone import carta_tf3_lunga as T3
    from solitone import corsa_accensione as CA
    from solitone import partenza as PA
    from solitone import toro as TO
    for m in ("__init__", "corsa_accensione", "partenza", "carta_deriva", "carta_tf3_lunga", "toro"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(__file__)
    s = V.CORSE[CA.NOME][2]
    c3 = CA.serie("TF3")[1] + CA.serie("TF3C")[1]
    quali = [argv[argv.index("--corsa") + 1]] if "--corsa" in argv else list(SEMI)
    print("=" * 130)
    print("IL PILOTA DI TL120 (Luca 2026-11-05 14:14): %s; la partenza di TF3 piu' il rumore relativo, F3, senza bordo; la partenza: il primo blocco di %g sopra %g per 1000, l'arresto %g dopo"
          % (", ".join(quali), PA.PASSO, PA.SOGLIA, PA.DOPO))
    print("=" * 130)
    tp = {}
    for nome in quali:
        print("-" * 130)
        tp[nome] = seme(nome, s, CA, CD, PA, T3, TO, V, c3)
    if "--corsa" not in argv:
        print("-" * 130)
        val = [v for v in tp.values() if v is not None]
        print("### IL PILOTA: le partenze %s (TF3 senza rumore: 16000, stampata, non contata)" % ", ".join("%s %s" % kv for kv in tp.items()))
        if len(val) >= 2:
            lg = np.log(np.array(val))
            sd = float(np.std(lg, ddof=1))
            print("  ln t: la media %.4f (t %.0f), la deviazione standard %.4f (%d semi con la partenza); la distanza da risolvere ln 2.19 - ln 1.48 = %.4f" % (lg.mean(), math.exp(lg.mean()), sd, len(val), DIST))
            for z in (2.0, 3.0):
                print("  ### il secondo stadio, a %g sigma: n >= %d semi per L (n >= 2 (z sd / %.3f)^2)" % (z, math.ceil(2.0 * (z * sd / DIST) ** 2), DIST))
        else:
            print("  ### meno di due semi con la partenza: lo sparpaglio non si stima (i semi senza partenza entro 30000 sono un fatto, scritto qui)")
    print("=" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
