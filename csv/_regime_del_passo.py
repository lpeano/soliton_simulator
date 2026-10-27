# -*- coding: utf-8 -*-
r"""**IL REGIME DEL PASSO: LA DERIVA DI `H_tot` A QUATTRO `s`** *([[ENERGIA-NON-CONSERVATA-S1]]; la risposta di Luca delle `20:00`; il task history
`doc/TASK_HISTORY/2026-10-27_energia_non_conservata_s1.md`, paragrafo `6`)*: ### **il solitone `S1` `N 1e5` sul toro `L 48`, il risolutore a ogni `s`,
`s = 0.3, 0.15, 0.075, 0.0375` allo stesso tempo fisico;** ### **il salto, la deriva dopo l'assestamento, il totale; i rapporti.**

> ### **In memoria; nessun file del nucleo.** ### **Importati, non copiati:** `_energia_del_legame.stato`, `_libro_dei_conti.conti_per_nodo`, `_libro_dei_conti_iv.assestamento`,
> `_scomposizione_solitone` *(`stato_uniforme`, `parti`)*, `_modi_pi_e_solitoni.largo`, `_solitoni_triangoli`, `_solitone_vuoto_congelato` *(`S` cambiato IN MEMORIA a ogni `s`)*.

Gira con:  python csv/_regime_del_passo.py > doc/referti_l2/regime_del_passo.txt
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

JSONL = os.path.join(RADICE, "doc", "referti_l2", "regime_del_passo.jsonl")
N = 1e5
L_TORO = 48
TAU = 600.0
PASSI = (0.3, 0.15, 0.075, 0.0375)
ZERO = "simm"
LAM_ZERO = 0.5
OMEGA = math.pi                # ### il massimo |E| per unita' di norma allo zero simmetrico (787296da)
TOLL_NORMA = 1e-10
PERDITA_VUOTO = 4175.1         # ### |Delta E_vuoto| di 15df5c63, N 1e5 L 48, a T_MAX (peso_deriva.txt)
SOGLIA_LETTURA = 0.01
RAPPORTO_MIN, RAPPORTO_MAX = 3.0, 5.0
NODI_L81_SU_L48 = (81.0 / 48.0) ** 2


def main(argv):
    del argv
    import _presidio
    import _universalita_massa as UM
    import _energia_del_legame as EL
    import _libro_dei_conti as LC
    import _libro_dei_conti_iv as LIV
    import _modi_pi_e_solitoni as MPS
    import _scomposizione_solitone as SC
    import _screening_forme_s3 as SF
    import _solitoni_triangoli as STR
    import _solitone_vuoto_congelato as VC
    import _triangoli_bassa_energia as BE
    import composizione as CM
    import tick as TK
    _presidio.avvia(__file__)
    print("=" * 130)
    print("IL REGIME DEL PASSO: LA DERIVA DI H_tot (IL LEGAME S1) A s 0.3, 0.15, 0.075, 0.0375 ALLO STESSO TEMPO FISICO; IL RISOLUTORE A OGNI s")
    print("=" * 130)
    blobs = {p: UM.blob(p) for p in ("soliton_simulator.py", "csv/_regime_del_passo.py", "csv/_energia_del_legame.py", "csv/_libro_dei_conti.py", "csv/_libro_dei_conti_iv.py")}
    print("  il passo: %d pezzi, impronta %s (intatto); i blob nel repo: %s" % (len(CM.ORDINE), CM.IMPRONTA, "; ".join("%s %s" % (k, v["sha1-BYTE"]) for k, v in blobs.items())))
    print("  la configurazione: N %g L_TORO %d TAU %g PASSI %s ZERO %s LAM_ZERO %g OMEGA pi TOLL_NORMA %g PERDITA_VUOTO %g SOGLIA_LETTURA %g RAPPORTO %g-%g; il toro fisso a ogni s (fattore = (L - 0.1)/w0)"
          % (N, L_TORO, TAU, PASSI, ZERO, LAM_ZERO, TOLL_NORMA, PERDITA_VUOTO, SOGLIA_LETTURA, RAPPORTO_MIN, RAPPORTO_MAX))
    print("-" * 130)
    if os.path.exists(JSONL):
        os.remove(JSONL)
    with io.open(JSONL, "a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps({"tipo": "testata", "blobs": blobs, "impronta": CM.IMPRONTA}, sort_keys=True) + "\n")
    s_vero = VC.S
    ris = {}
    try:
        for s in PASSI:
            VC.S = s                               # ### IN MEMORIA: il risolutore, la coppia, cs, e_K a questo s
            vero = MPS.LAM0
            MPS.LAM0 = STR.LAM0_TRI
            try:
                cc, _cy, _w0 = STR.c_triangoli(s)
                ls = MPS.largo(VC.FORMA, cc, s, N)
            finally:
                MPS.LAM0 = vero
            rec = {"larghezza": ls["larghezza"], "c": cc}
            fattore = (L_TORO - 0.1) / rec["larghezza"]
            L, inc, mot, st, par, pos, rr, Q, m1, m2, r_mat = EL.stato(N, fattore, rec)
            assert L == L_TORO, (s, L)
            incu, motu, stu = SC.stato_uniforme(L, Q, m1, m2)
            Eu, _a, _b, Mu, _c = SC.parti(incu, motu, stu)
            e_K = Eu / Mu
            n_t = int(round(TAU / s))
            hh, MM, VV = [], [], []
            t0 = time.time()
            with SF.forma(VC.FORMA), BE.conv(ZERO):
                for t in range(n_t + 1):
                    c = LC.conti_per_nodo(inc, mot, st, e_K, LAM_ZERO)
                    hh.append(math.fsum(c["tot"].tolist()))
                    MM.append(math.fsum(c["M"].tolist()))
                    VV.append(math.fsum(c["V"].tolist()))
                    if t < n_t:
                        TK.percorri_tick(st, mot, par, (), None, len(CM.ORDINE))
            sec = time.time() - t0
            H = np.array(hh)
            D = H - H[0]
            ta = LIV.assestamento(D)
            err = float(np.max(np.abs(H[ta:] - H[ta])))
            tt = np.arange(ta, n_t + 1) * s
            der = float(np.polyfit(tt, H[ta:], 1)[0]) if len(tt) >= 3 else float("nan")
            tot = float(np.max(np.abs(D)))
            dM = float(np.max(np.abs(np.array(MM) - MM[0])) / MM[0])
            dV = float(np.max(np.abs(np.array(VV) - VV[0])) / VV[0])
            r = {"s": s, "larghezza": rec["larghezza"], "mu": ls["mu"], "e_K": e_K, "tick": n_t, "t_a": ta, "tau_a": ta * s, "salto": float(D[ta]), "errore": err, "deriva": der,
                 "totale": tot, "dM": dM, "dV": dV, "secondi": sec, "s_omega": s * OMEGA, "s_omega_2pi": s * 2 * OMEGA}
            ris[s] = r
            print("  s %-6g: il risolutore: larghezza %.4f, mu %.6f, e_K %+.6f; %d tick; s omega %.4f (con 2 pi: %.4f); t_a %d (tempo %.2f); il SALTO %+.4e; l'errore dopo t_a %.4e; la DERIVA %+.4e per unita' di tempo; il totale max|D| %.4e (%.2f%% della perdita del vuoto); dM %.1e dV %.1e (%.0f s, %.2f ms per tick)"
                  % (s, rec["larghezza"], ls["mu"], e_K, n_t, s * OMEGA, 2 * s * OMEGA, ta, ta * s, D[ta], err, der, tot, 100 * tot / PERDITA_VUOTO, dM, dV, sec, 1000 * sec / n_t))
            sys.stdout.flush()
            with io.open(JSONL, "a", encoding="utf-8", newline="\n") as f:
                f.write(json.dumps(dict(r, tipo="passo", serie_ogni=[float(x) for x in D[::max(1, n_t // 400)]]), sort_keys=True) + "\n")
    finally:
        VC.S = s_vero
    print("-" * 130)
    print("### I RAPPORTI fra s consecutivi (s / s/2): la DERIVA, l'errore dopo t_a, il totale")
    for a, b in zip(PASSI[:-1], PASSI[1:]):
        ra, rb = ris[a], ris[b]
        print("  s %g / %g: la deriva %.4f; l'errore %.4f; il totale %.4f" % (a, b, ra["deriva"] / rb["deriva"] if rb["deriva"] else math.inf, ra["errore"] / rb["errore"], ra["totale"] / rb["totale"]))
    print("-" * 130)
    print("### I CRITERI")
    okm = all(r["dM"] <= TOLL_NORMA and r["dV"] <= TOLL_NORMA for r in ris.values())
    print("  %-110s %s   %s" % ("DEVE PASSARE: M e V entro %g a ogni s" % TOLL_NORMA, "PASSA" if okm else "### FALLISCE", "dM max %.1e dV max %.1e" % (max(r["dM"] for r in ris.values()), max(r["dV"] for r in ris.values()))))
    rap = ris[PASSI[2]]["deriva"] / ris[PASSI[3]]["deriva"] if ris[PASSI[3]]["deriva"] else math.inf
    okp = RAPPORTO_MIN <= rap <= RAPPORTO_MAX
    print("  %-110s %s   %.4f" % ("PUO' FALLIRE: fra s %g e %g il rapporto delle derive fra %g e %g" % (PASSI[2], PASSI[3], RAPPORTO_MIN, RAPPORTO_MAX), "PASSA" if okp else "### FALLISCE", rap))
    sotto = [s for s in PASSI if ris[s]["totale"] < SOGLIA_LETTURA * PERDITA_VUOTO]
    print("### LA LETTURA: il totale max|H_tot - H_tot(0)| sotto l'1%% della perdita del vuoto (%.2f) a s %s; il costo a quell's: %s"
          % (SOGLIA_LETTURA * PERDITA_VUOTO, sotto if sotto else "NESSUNO",
             "; ".join("s %g: %.0f s a L 48, stimati %.0f s per N 1e6 L 81 (i nodi x %.2f, a pari tempo fisico)" % (s, ris[s]["secondi"], ris[s]["secondi"] * NODI_L81_SU_L48, NODI_L81_SU_L48) for s in sotto) if sotto else "-"))
    with io.open(JSONL, "a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps({"tipo": "esito", "norme": okm, "rapporto_0075_00375": rap, "passa_rapporto": okp, "sotto_1pc": sotto}, sort_keys=True) + "\n")
    print("ESITO: DEVE %s; PUO' FALLIRE %s" % ("passa" if okm else "FALLISCE", "passa" if okp else "fallisce"))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
