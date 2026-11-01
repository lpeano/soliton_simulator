# -*- coding: utf-8 -*-
r"""**I TEST DELLE MISURE** *(il task history `2026-11-01_cassetta_solitone`, `M1`-`M6`)*: ### **i numeri gia' committati, AL BIT; il periodo su una serie sintetica.**"""
import json
import math
import os

import numpy as np

from . import RADICE
from . import misure as MI
from . import protetto as P


def primo(percorso):
    with open(percorso, encoding="utf-8") as f:
        return json.loads(f.readline())


def _righe(percorso):
    with open(percorso, encoding="utf-8") as f:
        return f.read().splitlines()


def gira(esito, partenze):
    import _consolida_B as CO
    import _coppia_di_B as CB
    import _deriva_congelato as DC
    import _dove_va_la_materia as DV
    import _livelli_piatti as LP
    import _modo_di_R as MR
    import _modo_lento as ML
    import _salti_nel_cuore as SN
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _stato_fermo as SFM
    import _strada_b_lati as SL
    import _triangoli_bassa_energia as BE
    import _vuoto_vivo_B as V
    print("### LE MISURE (csv/solitone/misure.py)")
    S, FORMA, N, L, EPS = LP.S, LP.FORMA, CB.N, CB.L, CB.EPS_LUNGA
    esito("DEVE PASSARE: le costanti = quelle degli strumenti (SOGLIA_VITA, SIGMA_FORMA, GRUPPI_LIMITE)",
          MI.SOGLIA_VITA == MR.SOGLIA == SL.SATURAZIONE == ML.SATURAZIONE and MI.SIGMA_FORMA == LP.SIGMA_FORMA and MI.GRUPPI_LIMITE == CO.GRUPPI, "")
    # ### M1: il campione a t 0 della corsa rigenerata di salti_nel_cuore (lo stato di Newton di B, la scena di riferimento)
    ref = primo(os.path.join(SN.DIR_JSON, "rig_000000.jsonl"))
    o = primo(os.path.join(CB.DIR_JSON, "lunga_B_00000.jsonl"))
    psi0, _mu, _da = CB.partenza_corsa("B")
    assert SFM.sha(psi0) == o["sha_partenza"]
    with P.scena_riferimento(N, L, EPS, S, FORMA) as (rec, z, phi0, _p):
        w0 = rec["larghezza"]
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            w_in = DC.forma(z, w0)[0]
        h = MI.lunghezza_arco(z)
        z["st"]["psi_h"][...] = psi0
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            c = MI.campione(z, 0, w_in, h)
            pt = MI.punto(z, 0, w_in, w0, S)
    esito("DEVE PASSARE: M1 w_in, h e il campione a t 0 (x, y, w, f_win, f_liscia) = rig_000000.jsonl AL BIT", w_in == ref["w_in"] and h == ref["h"] and c == ref["campioni"][0],
          "f_liscia %.15f" % c["f_liscia"])
    p0 = dict(o["punti"][0])
    esito("DEVE PASSARE: M1 il punto a t 0 (w, f_win, f_3w0, picco, M) = lunga_B_00000.jsonl (a8e0e43b) AL BIT", all(pt[k] == p0[k] for k in ("w", "f_win", "f_3w0", "picco", "M")), "alone %.3e" % MI.alone(pt))
    esito("DEVE FALLIRE: M1 la finestra netta = la liscia (f_win = f_liscia)", c["f_win"] != c["f_liscia"], "%.6f contro %.6f" % (c["f_win"], c["f_liscia"]))
    # ### M2: lo stato di BG-F-0.15 a tick 20000 (vuoto vivo): il campione, l'alone e la riga D = l'ultimo pezzo
    sol, vuoto, s = V.CORSE["BG-F-0.15"]
    pz = sorted(n for n in os.listdir(V.DIR_JSON) if n.startswith("BG-F-0.15_") and n.endswith(".jsonl"))
    ult = primo(os.path.join(V.DIR_JSON, pz[-1]))
    p0, mu = partenze["psi0_BG_F"], partenze["mu_BG_F"]
    with P.scena_vuoto(N, L, V.EPS, s, FORMA, vuoto) as (rec, z, phi0, _pK):
        w0 = rec["larghezza"]
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            w_in = DC.forma(z, w0)[0]
        h = MI.lunghezza_arco(z)
        bande = MI.Bande(DV.autovettori(DV.matrice(z, phi0, DV.AMP))[1], z["L"])
        with np.load(os.path.join(V.DIR_NPZ, "BG-F-0.15.npz")) as dati:
            t = int(dati["t"])
            for k in z["st"]:
                if isinstance(z["st"][k], np.ndarray):
                    z["st"][k][...] = dati[k]
        assert t == ult["t1"] and V.shas(z) == ult["sha_fine"], "lo stato NON e' la fine dell'ultimo pezzo"
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            c = MI.campione(z, t, w_in, h)
            a = MI.alone(MI.punto(z, t, w_in, w0, s))
        D = np.exp(1j * mu * s * t) * z["st"]["psi_h"] - p0
        rd = MI.riga_D(bande, D, float(np.linalg.norm(p0)), t)
    cr, dr = ult["campioni"][-1], ult["D"][-1]
    esito("DEVE PASSARE: M2 BG-F-0.15 a tick %d: il campione e l'alone = l'ultimo campione AL BIT" % t, cr["t"] == t and all(c[k] == cr[k] for k in ("x", "y", "w", "f_win", "f_liscia")) and a == cr["alone"],
          "f_liscia %.6f alone %.6f" % (c["f_liscia"], a))
    esito("DEVE PASSARE: M2 la riga D (|D|/|psi0| e le frazioni di banda) = l'ultima riga D AL BIT", dr["t"] == t and rd == dr, "nD %.6f B %.6f" % (rd["nD"], rd["bande"]["B"]))
    # ### M3: il limite del tasso sui pezzi di a8e0e43b
    dd = [d for x in CO.pezzi(CB.DIR_JSON, "lunga_B_") for d in x["D"]]
    with open(os.path.join(CO.DIR_JSON, "limite_3000.json"), encoding="utf-8") as f:
        lm_ref = json.loads(f.read())
    lm = MI.limite(dd, S)
    esito("DEVE PASSARE: M3 il limite del tasso (piatte, A) = limite_3000.json AL BIT", lm == lm_ref, "piatte %.3e A %.3e" % (lm["gruppi"]["piatte"]["limite"], lm["gruppi"]["A"]["limite"]))
    # ### M4: la forma della crescita, i casi del collaudo di _livelli_piatti
    rl = _righe(os.path.join(RADICE, "doc", "referti_l2", "livelli_piatti.txt"))
    vera = LP.leggi(os.path.join(LP.DIR_JSON, "breve_R_1e6.json"))
    tv, yv = np.array(vera["t5"], dtype=float) * vera["s"], np.array(vera["nD5"])
    tau = np.arange(1, int(round(LP.T_BREVE / LP.PASSO_BREVE)) + 1) * LP.PASSO_BREVE
    casi = (("|D| = 1e-8 t", tau, 1e-8 * tau, "lineare"), ("la serie VERA di breve_R_1e6", tv, yv, "lineare"),
            ("|D| = 1e-8 e^{0.06 t}", tau, 1e-8 * np.exp(0.06 * tau), "esponenziale"),
            ("|D| = 1e-8 (t + e^{0.0331 t})", tau, 1e-8 * (tau + np.exp(0.0331 * tau)), "esponenziale"),
            ("|D| = 1e-8 (il caso nullo", tau, 1e-8 + 0.0 * tau, "potenza t^0"))
    for nome, tt, y, atteso in casi:
        m = y > 0
        fn = MI.forma_pendenze(tt[m], y[m], MI.SOGLIA_VITA)
        nota = "%s; %d campioni > 0; gamma %.5f +- %.5f, gamma t_ultimo %.3f, b %.4f +- %.4f" % (fn["forma"], int(m.sum()), fn["gamma"], fn["sigma_gamma"], fn["gamma"] * fn["t_ultimo"], fn["b"], fn["sigma_b"])
        trovate = [r for r in rl if "DEVE dare %s: %s" % (atteso.upper(), nome) in r]
        esito("DEVE PASSARE: M4 %s -> %s, = la riga di livelli_piatti.txt" % (nome, atteso), fn["forma"] == atteso and len(trovate) == 1 and trovate[0].rstrip().endswith(nota), nota)
    # ### M5: la vita, gli OSSERVATO di modo_di_R.txt
    rm = _righe(os.path.join(RADICE, "doc", "referti_l2", "modo_di_R.txt"))
    for nome, f in (("r 1 (s 0.3; 03142636)", "modo_r1_s0.3.json"), ("r 1.5247 (s 0.15; 03142636)", "modo_r1.52.json")):
        mm = LP.leggi(os.path.join(MR.DIR_ML, f))
        v = MI.vita(np.array(mm["t"], dtype=float) * mm["s"], np.array(mm["nD"]))
        oss = ("OSSERVATO %.1f" % v) if v is not None else "mai sopra"
        trovate = [r for r in rm if r.lstrip().startswith(nome) and "OSSERVATO" in r]
        esito("DEVE PASSARE: M5 la vita di %s = la riga di modo_di_R.txt" % nome, len(trovate) == 1 and trovate[0].rstrip().endswith(oss), oss)
    # ### M6: il periodo dai cambi di segno, col passo (una serie sintetica; il passo 3 tick, come in 03142636)
    passo = 3
    for T_vero, giusto in ((99.0, True), (3.3, False)):
        i = np.arange(4000)
        pr = np.cos(2.0 * math.pi * i * passo / T_vero + 0.1)
        r = MI.periodo_dai_cambi(pr, passo)
        tol = 2.0 * passo / (r["cambi"] - 1)               # ### la risoluzione della media dei cambi
        letto = abs(r["periodo"] - T_vero) <= tol
        in_alias = min(abs(x - T_vero) for x in r["alias"]) <= tol
        if giusto:
            esito("DEVE PASSARE: M6 un periodo vero di %g tick (%g passi) letto giusto (entro la risoluzione %.2e)" % (T_vero, T_vero / passo, tol), letto, "letto %.4f" % r["periodo"])
        else:
            esito("DEVE PASSARE: M6 un periodo vero di %g tick (%g passi, sotto Nyquist %g): NON letto giusto, ma il vero fra gli alias" % (T_vero, T_vero / passo, r["nyquist"]), not letto and in_alias,
                  "letto %.4f; gli alias %s" % (r["periodo"], " ".join("%.4f" % x for x in r["alias"])))
    try:
        MI.periodo_dai_cambi(pr)
        rifiutato = False
    except TypeError:
        rifiutato = True
    esito("DEVE FALLIRE: M6 il periodo SENZA il passo", rifiutato, "")
