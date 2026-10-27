# -*- coding: utf-8 -*-
r"""**IL VUOTO DA SOLO CON UN DISTURBO** *(il mandato breve del 2026-10-27, 08:59, parte 2; [[VUOTO-DA-SOLO]], [[CANALE-CS-SECONDA-SORGENTE]])*: ### **le scene di `e9e42332` con un disturbo casuale del vuoto
di ampiezza relativa `1e-6` per estremita':** ### **stabile, o solo stazionario?** ### **`(i)` `cs` spento, `(ii)` `cs` acceso a `Lambda_c` = la media di `Lambda` per nodo** *(il rapporto `1`)*; ### **il controllo nullo senza disturbo.**

> ### ⛔ **Il task history e' `2026-10-27_vuoto_disturbato.md`.** ### **In memoria; nessun file del nucleo.**
> ### **Importati, non copiati:** `_solitone_vuoto_congelato` *(`S`, `FORMA`)*, `_screening_forme_s3.forma`, `scena_l2.scena_toro`, `tick.percorri_tick`, `tick.tick_con_cs`.

Gira con:  python csv/_vuoto_disturbato.py > doc/referti_l2/vuoto_disturbato.txt
"""
import io
import json
import math
import os
import sys
import time

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
_PO = os.path.join(RADICE, "primo_ordine")
for _p in (_QUI, _PO, os.path.join(_PO, "leggi")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import numpy as np                                             # noqa: E402

LATI = (48, 69, 81, 120)
L_NULLO = 48
T_MAX = 2000
OGNI = 20
AMPIEZZA = 1e-6
SEME = 20261027
RAPPORTO = 1.0
SOGLIE = (0.1, 1.0)
TOLL_NORMA = 1e-10
TOLL_STABILE = 1e-5
GAMMA_RIF = 0.402
VITE_SOLITONE = (320, 140)
JSONL = os.path.join(RADICE, "doc", "referti_l2", "vuoto_disturbato.jsonl")
OK = [0, 0]
FALLITE = []


def esito(che, passa, nota="", deve=True):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    if deve and not passa:
        FALLITE.append(che)
    print("  %-110s %s   %s" % (che[:110], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return passa


def scrivi(r):
    with io.open(JSONL, "a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n")


def tasso(serie, da):
    """### La pendenza di `log(scarto)` contro `t`, sui punti con `t >= da` e scarto `> 0`."""
    p = [(t, math.log(sc)) for t, _a, _b, sc in serie if t >= da and sc > 0.0]
    if len(p) < 3:
        return None
    t, y = np.array(p).T
    return float(np.polyfit(t, y, 1)[0])


def corsa(L, cs_acceso, disturbo):
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import composizione as CM
    import scena_l2 as SL
    import tick as TK
    inc, mot, st, par = SL.scena_toro("triangoli", (L, L), 1.0, 0.1)
    n = inc.n
    mot.cs = np.full(n, VC.S)
    mot.lambda_c = None
    par = dict(par)
    par["eps"] = 0.0
    st["psi_h"][...] = 0.0
    st["phi_h"][...] = SL.VUOTO_PER_ESTREMITA
    if disturbo:
        xi = np.random.default_rng(SEME).standard_normal(st["phi_h"].shape)
        st["phi_h"][...] *= 1.0 + AMPIEZZA * xi
    nodo = inc.nodo
    gr = np.bincount(nodo, minlength=n).astype(float)

    def lam_e():
        x = np.zeros(n)
        np.add.at(x, nodo, np.abs(st["phi_h"]) ** 2)
        return x / gr
    lc = RAPPORTO * float(np.mean(mot.densita_vuoto(st))) if cs_acceso else None
    V0 = float(np.sum(np.abs(st["phi_h"]) ** 2))
    serie, dV = [], 0.0
    primo = {s_: None for s_ in SOGLIE}
    t0 = time.time()
    with SF.forma(VC.FORMA):
        for t in range(T_MAX + 1):
            if t % OGNI == 0:
                le = lam_e()
                sc = float(np.std(le))
                serie.append([t, float(le.min()), float(le.max()), sc])
                dV = max(dV, abs(float(np.sum(np.abs(st["phi_h"]) ** 2)) - V0) / V0)
                for s_ in SOGLIE:
                    if primo[s_] is None and sc > s_:
                        primo[s_] = t
            if t < T_MAX:
                if cs_acceso:
                    TK.tick_con_cs(st, mot, par, lc, ())
                else:
                    TK.percorri_tick(st, mot, par, (), None, len(CM.ORDINE))
    cs_fine = None if mot.cs is None else [float(np.min(mot.cs)), float(np.max(mot.cs))]
    return {"tipo": "corsa", "L": L, "cs_acceso": cs_acceso, "disturbo": disturbo, "lambda_c": lc, "cs_fine": cs_fine, "dV": dV, "scarto_iniziale": serie[0][3],
            "scarto_max": max(x[3] for x in serie), "scarto_finale": serie[-1][3], "tasso": tasso(serie, 0), "tasso_seconda_meta": tasso(serie, T_MAX // 2),
            "primo": {str(k): v for k, v in primo.items()}, "serie": serie, "secondi": time.time() - t0}


def main(argv):
    del argv
    import _presidio
    import _universalita_massa as UM
    import _solitone_vuoto_congelato as VC
    import composizione as CM
    _presidio.avvia(__file__)
    print("=" * 130)
    print("IL VUOTO DA SOLO CON UN DISTURBO: le scene di e9e42332, il disturbo relativo %g per estremita'; (i) cs spento, (ii) cs acceso (il rapporto %g); il controllo nullo" % (AMPIEZZA, RAPPORTO))
    print("=" * 130)
    blobs = {p: UM.blob(p) for p in ("soliton_simulator.py", "csv/_vuoto_disturbato.py", "csv/_solitone_vuoto_congelato.py", "primo_ordine/tick.py", "primo_ordine/flussi_parziali.py")}
    print("  il passo: %d pezzi, impronta %s (intatto); i blob nel repo: %s" % (len(CM.ORDINE), CM.IMPRONTA, "; ".join("%s %s" % (k, v["sha1-BYTE"]) for k, v in blobs.items())))
    print("  la configurazione: LATI %s L_NULLO %d T_MAX %d OGNI %d AMPIEZZA %g SEME %d RAPPORTO %g SOGLIE %s TOLL_NORMA %g TOLL_STABILE %g GAMMA_RIF %g VITE_SOLITONE %s; da _solitone_vuoto_congelato: S %g FORMA %s"
          % (LATI, L_NULLO, T_MAX, OGNI, AMPIEZZA, SEME, RAPPORTO, SOGLIE, TOLL_NORMA, TOLL_STABILE, GAMMA_RIF, VITE_SOLITONE, VC.S, VC.FORMA))
    print("  la materia a zero; (i) mot.cs = S, lambda_c None, tick.percorri_tick; (ii) tick.tick_con_cs con Lambda_c = RAPPORTO x la media di Lambda per nodo a t 0 (dopo il disturbo); dtau 1: il tasso per tick = per unita' di N dtau")
    print("-" * 130)
    io.open(JSONL, "w", encoding="utf-8").close()
    scrivi({"tipo": "testata", "blobs": blobs, "impronta": CM.IMPRONTA})
    ris = []
    piano = [(L_NULLO, True, False)] + [(L, cs, True) for L in LATI for cs in (False, True)]
    for L, cs, dist in piano:
        r = corsa(L, cs, dist)
        ris.append(r)
        scrivi(r)
        print("  L %3d %-12s %-14s: lo scarto di Lambda per estremita' %.3e -> max %.3e, finale %.3e; il tasso per tick %s (seconda meta' %s); oltre 0.1: %s, oltre 1: %s; dV %.1e; Lambda_c %s, cs alla fine %s (%.0f s)"
              % (L, "cs ACCESO" if cs else "cs spento", "disturbato" if dist else "SENZA disturbo", r["scarto_iniziale"], r["scarto_max"], r["scarto_finale"],
                 "%+.3e" % r["tasso"] if r["tasso"] is not None else "-", "%+.3e" % r["tasso_seconda_meta"] if r["tasso_seconda_meta"] is not None else "-",
                 r["primo"]["0.1"], r["primo"]["1.0"], r["dV"], "%.6f" % r["lambda_c"] if r["lambda_c"] is not None else "None", r["cs_fine"], r["secondi"]))
        sys.stdout.flush()
    print("-" * 130)
    print("### LA LETTURA: col cs acceso il tasso contro %g (974d411a: R1, S1, il quadrato, la materia x 0.1, per unita' di N dtau); il tempo all'ordine 1 contro la vita del solitone %s" % (GAMMA_RIF, VITE_SOLITONE))
    for r in ris:
        if r["disturbo"]:
            g = r["tasso"]
            t1 = r["primo"]["1.0"]
            stima = (math.log(1.0 / r["scarto_iniziale"]) / g) if g and g > 0 and r["scarto_iniziale"] > 0 else None
            print("  L %3d %-10s: il tasso %s (%s di %g); all'ordine 1 %s (la stima dal tasso %s)"
                  % (r["L"], "cs ACCESO" if r["cs_acceso"] else "cs spento", "%+.3e" % g if g is not None else "-", "%.3f" % (g / GAMMA_RIF) if g is not None else "-", GAMMA_RIF,
                     "a %d tick" % t1 if t1 is not None else "non arrivato", "%.0f tick" % stima if stima else "-"))
    print("-" * 130)
    print("### I CRITERI")
    esito("DEVE PASSARE (1): V conservato entro %g relativo (ogni corsa)" % TOLL_NORMA, all(r["dV"] <= TOLL_NORMA for r in ris), "il peggiore %.1e" % max(r["dV"] for r in ris))
    nu = [r for r in ris if not r["disturbo"]][0]
    esito("DEVE PASSARE (2): il controllo nullo, cs acceso SENZA disturbo a L %d: lo scarto 0 al bit per T_MAX" % L_NULLO, nu["scarto_max"] == 0.0, "%.1e" % nu["scarto_max"])
    sc = max(r["scarto_max"] for r in ris if r["disturbo"] and not r["cs_acceso"])
    esito("PUO' FALLIRE (3): (i) cs spento, lo scarto non supera %g fino a T_MAX (a ogni L)" % TOLL_STABILE, sc <= TOLL_STABILE, "lo scarto massimo %.3e" % sc, deve=False)
    print("-" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    scrivi({"tipo": "esito", "passano": OK[0], "totale": OK[1], "deve_fallite": FALLITE})
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
