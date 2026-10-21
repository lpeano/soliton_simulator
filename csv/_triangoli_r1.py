# -*- coding: utf-8 -*-
r"""**TRIANGOLI, GRADINO 2-BIS: `R1` *(`cs` + `CAMM-FASE-VUOTO`)* SUL TORO TRIANGOLARE, BRACCIO `SN`.**

> ### ⛔ **Il task history e' `2026-10-21_triangoli_r1.md`**; il gradino `2` e' `csv/_stabilita_triangoli.py`
> *(`bb0ef057`)*. ### **Una MISURA: nessun file del nucleo si tocca, NESSUNA CURA.**

## ⭐ CHE COSA AGGIUNGE AL GRADINO `2`
### **`cs` ACCESO:** la funzione di Green passa `acceso` a `_stabilita_lineare.passo`, che chiama
`tick.tick_con_cs`; ### **la sequenza di `_stabilita_lineare.braccio_proiettato` con `acceso`, nello stesso
ordine** *(`lm`, `Lambda_c = RAPPORTO * lm`, `cs_m`, `accendi_cs`, la scala)*, ### **il tempo proprio
`t dtau cs_m`.** ### **Il controllo che ripete la cosa giusta: `R1` di `594417f6` AL BIT sul quadrato.**
### **E si LEGGONO** *(senza usarli)*: `s` dopo il tick della base *(il cono)* e i contatori del punto fisso.

Gira con:  python csv/_triangoli_r1.py
"""
import io
import json
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

EPS = float(np.finfo(float).eps)
LATO = 32
DTAU = 0.125
EPS_REL_2 = 1e-6
ULP_ESATTA = 64
ULP_P3 = 64
RIF_MANDATO = 0.545            # R1 del quadrato citato dal mandato (stimatore degli autovalori)
STABILE = 1e-3                 # STABILE se il massimo <= 1e-3 * RIF_MANDATO, dal mandato
R2_TRI = "R2 triangoli SN eps 1e-07"
JSONL = os.path.join(RADICE, "doc", "referti_l2", "triangoli_r1.jsonl")
J_GRADINO2 = os.path.join(RADICE, "doc", "referti_l2", "triangoli_gradino2.jsonl")
OK = [0, 0]


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    print("  %-78s %s   %s" % (che[:78], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return passa


def green(base, mot, par, lc, lato, scale, eps_rel, d, cono):
    """### `R(k)` di un tick dalla base, `cs` ACCESO; `cono` raccoglie `s` e i giri dopo la base."""
    import _stabilita_lineare as SL
    import _stabilita_triangoli as ST
    import flussi_parziali as FP
    n = lato * lato
    nc = 6 * d
    dopo = SL.copia(base)
    SL.passo(dopo, mot, par, True, (), lc)
    # ### SOLO LETTURA: `s` del tick della base, e i giri del suo punto fisso
    cono["s"] = max(cono["s"], float(np.max(FP.dtau_nodo(mot))) / float(FP.dtau_rif(mot)))
    cono["giri"] = max(cono["giri"], int(mot.giri_omega))
    c0 = ST.celle(dopo, n, d)
    R = np.empty((lato, lato, 2 * nc, 2 * nc), dtype=complex)
    for j in range(2 * nc):
        e = eps_rel * scale[0 if (j % nc) < 4 * d else 1]
        p = SL.copia(base)
        ST.perturba(p, j, e, d)
        SL.passo(p, mot, par, True, (), lc)
        cono["giri"] = max(cono["giri"], int(mot.giri_omega))
        dd = (ST.celle(p, n, d) - c0) / e
        R[:, :, :, j] = np.fft.fft2(dd.reshape(lato, lato, 2 * nc), axes=(0, 1))
    return R, dopo


def braccio_r1(nome, griglia, braccio, eps_rel, tempo, lato=LATO, dtau=DTAU):
    """### `braccio_proiettato` di `_stabilita_lineare` con `acceso = True`, in `d`."""
    import _stabilita_lineare as SL
    import _stabilita_triangoli as ST
    import flussi_parziali as FP
    d = len(griglia[0])
    nc = 6 * d
    inc, mot, st, par = ST.scena(griglia, braccio, lato, dtau)
    n = inc.n
    lm = float(np.mean(mot.densita_vuoto(st)))
    rm = float(np.mean(mot.densita_materia(st)))
    lc = SL.RAPPORTO * lm
    cs_m = lm / (lm + lc)
    FP.accendi_cs(mot, lc, st)
    N = int(round(tempo / dtau))
    assert N % 4 == 0, "N = %d non si divide in quattro quarti" % N
    scale = (float(np.max(np.abs(st["psi_h"]))), float(np.max(np.abs(st["phi_h"]))))
    fuori = {"nome": nome, "braccio": braccio, "d": d, "lato": lato, "dtau": dtau, "x": SL.X,
             "acceso": True, "salta": [], "eps_rel": eps_rel, "N": N, "cs_m": cs_m,
             "rho_m": rm, "lambda_m": lm, "lambda_c": lc, "fine": "N", "proiettata": True}
    M = np.broadcast_to(np.eye(2 * nc, dtype=complex), (lato, lato, 2 * nc, 2 * nc)).copy()
    acc = np.zeros((lato, lato))
    zero = np.zeros((lato, lato))
    tt, Le, Ln, Lq = [0.0], [zero], [zero], {}
    unif = ST.uniformita(st, n, d)
    cono = {"s": 0.0, "giri": 0}
    t0 = time.time()
    base = st
    for t in range(1, N + 1):
        R, dopo = green(base, mot, par, lc, lato, scale, eps_rel, d, cono)
        unif = max(unif, ST.uniformita(dopo, n, d))
        ST.proietta(dopo, n, d)
        M = np.matmul(R, M)
        s = np.sqrt(np.sum(np.abs(M) ** 2, axis=(-2, -1)))
        M /= s[..., None, None]
        acc += np.log(s)
        base = dopo
        if t % SL.OGNI == 0 or t % (N // 4) == 0:
            le = acc + np.log(np.max(np.abs(np.linalg.eigvals(M)), axis=-1))
            tt.append(t * dtau * cs_m)
            Le.append(le)
            Ln.append(acc.copy())
            if t % (N // 4) == 0:
                Lq[t // (N // 4)] = le
        if time.time() - t0 > SL.BUDGET_LUNGO:
            fuori["fine"] = "BUDGET superato al passo %d di %d" % (t, N)
            break
    fuori["secondi"] = time.time() - t0
    fuori["uniformita_ulp"] = unif
    fuori["nu_s3"] = lm ** 2 / (rm + lm) ** 2
    fuori["s_max"] = cono["s"]
    fuori["giri_max"] = cono["giri"]
    fuori["avvisi_omega"] = int(mot.avvisi_omega)
    fuori["fattore_omega_max"] = float(mot.fattore_omega_max)
    if fuori["fine"] != "N":
        return fuori
    T = N * dtau * cs_m
    tq = T / 4.0
    fuori["gamma"] = Lq[4] / T
    fuori["gamma_meta"] = Lq[2] / (T / 2.0)
    fuori["quarti"] = [(Lq[q] - (Lq[q - 1] if q > 1 else 0.0)) / tq for q in (1, 2, 3, 4)]
    fuori["pend"] = {"meta_eig": SL.pendenze(tt, Le, T / 2.0, T),
                     "meta_norm": SL.pendenze(tt, Ln, T / 2.0, T),
                     "q4_eig": SL.pendenze(tt, Le, 3.0 * T / 4.0, T),
                     "q4_norm": SL.pendenze(tt, Ln, 3.0 * T / 4.0, T)}
    return fuori


def prova_p1(griglia, braccio):
    import _stabilita_lineare as SL
    import _stabilita_triangoli as ST
    import flussi_parziali as FP
    inc, mot, st, par = ST.scena(griglia, braccio)
    lc = float(np.mean(mot.densita_vuoto(st)))
    FP.accendi_cs(mot, lc, st)
    SL.passo(st, mot, par, True, (), lc)
    a, b = SL.copia(st), SL.copia(st)
    for k in SL.CACHE:
        b[k][...] = 0
    SL.passo(a, mot, par, True, (), lc)
    SL.passo(b, mot, par, True, (), lc)
    return np.array_equal(a["psi_h"], b["psi_h"]) and np.array_equal(a["phi_h"], b["phi_h"])


def prova_p3(griglia, braccio):
    import _stabilita_lineare as SL
    import _stabilita_triangoli as ST
    import flussi_parziali as FP
    d = len(griglia[0])
    nc = 6 * d
    inc, mot, st, par = ST.scena(griglia, braccio)
    lc = float(np.mean(mot.densita_vuoto(st)))
    FP.accendi_cs(mot, lc, st)
    scale = (float(np.max(np.abs(st["psi_h"]))), float(np.max(np.abs(st["phi_h"]))))
    peggio, al_bit = 0.0, True
    for j in (0, 5, 13, 20, 2 * nc - 1):
        p = SL.copia(st)
        ST.perturba(p, j, SL.EPS_REL * scale[0 if (j % nc) < 4 * d else 1], d)
        SL.passo(p, mot, par, True, (), lc)
        a = SL.copia(st)
        SL.passo(a, mot, par, True, (), lc)
        c = SL.copia(st)
        SL.passo(c, mot, par, True, (), lc)
        for k in ("psi_h", "phi_h"):
            dd = float(np.max(np.abs(a[k] - c[k])))
            al_bit &= bool(np.array_equal(a[k], c[k]))
            peggio = max(peggio, dd / (EPS * float(np.max(np.abs(c[k])))))
    return peggio, al_bit


def main(argv):
    del argv
    import _presidio
    _presidio.avvia(__file__)
    import _al_bit_cura_d0 as AB
    import _stabilita_lineare as SL
    import _stabilita_triangoli as ST
    import _triangoli as T
    import composizione as CM
    import energia_pesata as EP
    print("=" * 100)
    print("TRIANGOLI, GRADINO 2-BIS: R1 (cs + CAMM-FASE-VUOTO) SUL TORO TRIANGOLARE, BRACCIO SN")
    print("=" * 100)
    print("  LA CONFIGURAZIONE INTERA, dichiarata:")
    print("  R1: cs ACCESO, Lambda_c = %g * Lambda medio; lato %d, dtau %g, x %g, eps %g; base proiettata;"
          " N dtau %g; gamma = la pendenza della NORMA sulla seconda meta' (e accanto gli autovalori)"
          % (SL.RAPPORTO, LATO, DTAU, SL.X, T.EPS_MONETA, SL.TEMPO_LUNGO))
    print("  il passo: %d pezzi, impronta %s; GIRI_MAX_OMEGA %d, avviso oltre %d; la cella 6d complessi"
          % (len(CM.ORDINE), CM.IMPRONTA, EP.GIRI_MAX_OMEGA, EP.GIRI_AVVISO_OMEGA))
    print("  SN: psi e phi per sqrt(4/6) (rho e Lambda per nodo come il quadrato)")
    print("  soglie: base <= %g ulp; esatta N*%d ulp; P3 %d ulp; linearita' e C6 %g * max gamma;"
          " STABILE <= %g * %g" % (SL.SOGLIA_UNIF, ULP_ESATTA, ULP_P3, SL.BANDA_LIN, STABILE,
                                   RIF_MANDATO))
    print("-" * 100)
    sys.stdout.flush()
    io.open(JSONL, "w", encoding="utf-8").close()

    def salva(b):
        with io.open(JSONL, "a", encoding="utf-8") as f:
            f.write(json.dumps(ST.per_json(b)) + "\n")

    # ------------------------------------------------------------ i controlli
    print("### 1. I CONTROLLI")
    vecchi = AB.committato()
    t0 = time.time()
    q = braccio_r1("R1 lato 32 QUADRATO", T.QUADRATO, "Q", SL.EPS_REL, SL.TEMPO_LUNGO)
    v = vecchi["R1 lato 32"]
    diversi = [c for c in AB.CAMPI if not np.array_equal(np.asarray(q[c]), np.asarray(v[c]))]
    diversi += ["pend." + k for k in v["pend"]
                if not np.array_equal(np.asarray(q["pend"][k]), np.asarray(v["pend"][k]))]
    if not esito("DEVE RIUSCIRE: R1 di 594417f6 AL BIT sul quadrato del costruttore generale",
                 not diversi, ("10 campi identici, %.0f s" % (time.time() - t0)) if not diversi
                 else "### DIVERSI: %s" % ", ".join(diversi)):
        print("### STOP: lo strumento non ripete 594417f6")
        return 1
    salva(q)
    ex = ST.esatta(T.TRIANGOLI)
    tetto = ex["N"] * ULP_ESATTA * EPS
    if not esito("DEVE RIUSCIRE: la camminata sola sui triangoli ESATTA, N dtau 100: <= N*64 ulp",
                 ex["dev"] <= tetto, "%.3e contro %.3e (N %d)" % (ex["dev"], tetto, ex["N"])):
        print("### STOP: il metodo e' rotto sui triangoli")
        return 1
    if not esito("P1 SN cs acceso: un tick con le cache azzerate = con le cache, AL BIT",
                 prova_p1(T.TRIANGOLI, "SN")):
        print("### STOP: le cache sono memoria")
        return 1
    u, bit = prova_p3(T.TRIANGOLI, "SN")
    if not esito("P3 SN cs acceso: nessuna memoria in mot", bit or u <= ULP_P3,
                 "%s, %.1f ulp" % ("AL BIT" if bit else "non al bit", u)):
        print("### STOP: la funzione di Green ha una memoria in `mot`")
        return 1
    print("-" * 100)

    # ------------------------------------------------------------ R1 sui triangoli
    print("### 2. R1 SUI TRIANGOLI, SN")
    bb = {}
    for eps_rel in (SL.EPS_REL, EPS_REL_2):
        nome = "R1 triangoli SN eps %g" % eps_rel
        b = braccio_r1(nome, T.TRIANGOLI, "SN", eps_rel, SL.TEMPO_LUNGO)
        print("  %-28s rho_m %.6f Lambda_m %.6f Lambda_c %.6f cs_m %.6f uniformita' %.1f ulp  %.0f s  %s"
              % (nome, b["rho_m"], b["lambda_m"], b["lambda_c"], b["cs_m"], b["uniformita_ulp"],
                 b["secondi"], b["fine"]))
        print("      il cono: s max %.6f;  il punto fisso: giri max %d, avvisi %d, fattore max %.4f"
              % (b["s_max"], b["giri_max"], b["avvisi_omega"], b["fattore_omega_max"]))
        sys.stdout.flush()
        salva(b)
        if b["fine"] != "N":
            print("### STOP: %s" % b["fine"])
            return 1
        bb[eps_rel] = b
    print("  il quadrato: il cono s max %.6f;  giri max %d, avvisi %d, fattore max %.4f"
          % (q["s_max"], q["giri_max"], q["avvisi_omega"], q["fattore_omega_max"]))
    b = bb[SL.EPS_REL]
    esito("la base SN: uniformita' <= %g ulp per tutto l'intervallo" % SL.SOGLIA_UNIF,
          b["uniformita_ulp"] <= SL.SOGLIA_UNIF, "%.1f ulp" % b["uniformita_ulp"])
    esito("il cono: s <= 1 a ogni nodo, dopo ogni tick della base", b["s_max"] <= 1.0,
          "s max %.6f" % b["s_max"])
    esito("il contatore degli avvisi del punto fisso, STAMPATO", True,
          "%d avvisi (oltre %d giri), giri max %d" % (b["avvisi_omega"], EP.GIRI_AVVISO_OMEGA,
                                                      b["giri_max"]))
    g1 = np.asarray(b["pend"]["meta_norm"])
    g2 = np.asarray(bb[EPS_REL_2]["pend"]["meta_norm"])
    banda = SL.BANDA_LIN * float(np.max(g1))
    dl = float(np.max(np.abs(g1 - g2)))
    esito("DEVE RIUSCIRE: la linearita' su SN, 1e-7 contro 1e-6", dl <= banda,
          "%.3e contro %.3e" % (dl, banda))
    dr = float(np.max(np.abs(g1 - ST.ruota60(g1))))
    esito("DEVE RIUSCIRE: l'isotropia C6 di gamma(k) sui triangoli, SN", dr <= banda,
          "%.3e contro %.3e" % (dr, banda))
    gq = np.asarray(q["pend"]["meta_norm"])
    dq = float(np.max(np.abs(gq - ST.ruota60(gq))))
    esito("DEVE FALLIRE: l'isotropia C6 di R1 sul QUADRATO (594417f6)",
          dq > SL.BANDA_LIN * float(np.max(gq)),
          "%.3e contro %.3e" % (dq, SL.BANDA_LIN * float(np.max(gq))))
    print("-" * 100)

    # ------------------------------------------------------------ le letture
    print("### 3. LE LETTURE (fissate nel task history)")
    kv, lab, Mp, Kp, dmin = ST.zona(LATO)
    h = LATO // 2
    qe = np.asarray(q["pend"]["meta_eig"])
    iq = np.unravel_index(int(np.argmax(gq)), gq.shape)
    print("  QUADRATO R1: max gamma (norma) %.4f a %s; (autovalori) %.4f; (pi,0) %.4f  (pi,pi) %.4f;"
          " banda (punto_banda) %.4f" % (float(gq.max()), tuple(int(x) for x in iq), float(qe.max()),
                                         float(gq[h, 0]), float(gq[h, h]),
                                         float(gq[SL.punto_banda(gq, LATO)])))
    ge = np.asarray(b["pend"]["meta_eig"])
    i = np.unravel_index(int(np.argmax(g1)), g1.shape)
    bordo = np.array([[lab[a, c] in ("centro", "M", "K") for c in range(LATO)] for a in range(LATO)])
    gb = np.where(bordo, -np.inf, g1)
    ib = np.unravel_index(int(np.argmax(gb)), g1.shape)
    # ### R2 sui triangoli e sul quadrato, dai referti committati
    r2t = None
    for riga in io.open(J_GRADINO2, encoding="utf-8"):
        w = json.loads(riga)
        if w.get("nome") == R2_TRI:
            r2t = np.asarray(w["pend"]["meta_norm"])
    r2q = np.asarray(vecchi["R2 lato 32"]["pend"]["meta_norm"])
    r2t_b = float(np.max(np.where(bordo, -np.inf, r2t)))
    et = {"max": float(g1.max()), "dove": lab[i], "k": [int(x) for x in i],
          "rapporto_norma": float(g1.max()) / float(gq.max()),
          "rapporto_mandato": float(g1.max()) / RIF_MANDATO, "max_eig": float(ge.max()),
          "stabile": float(g1.max()) <= STABILE * RIF_MANDATO,
          "banda": float(gb[ib]), "banda_k": [int(x) for x in ib], "banda_r2": r2t_b,
          "M": {str(k): float(g1[k]) for k in sorted(Mp)},
          "K": {str(k): float(g1[k]) for k in sorted(Kp)}, "centro": float(g1[0, 0]),
          "tolto_r1": 1.0 - float(g1.max()) / float(gq.max()),
          "tolto_r2": 1.0 - float(r2t.max()) / float(r2q.max())}
    print("  R1 TRIANGOLI SN: max gamma %.4f a %s (%s), |k| %.4f; rapporto col quadrato (norma %.4f)"
          " %.4f, col 0.545 del mandato %.4f; autovalori %.4f"
          % (et["max"], tuple(et["k"]), et["dove"], float(np.linalg.norm(kv[i])), float(gq.max()),
             et["rapporto_norma"], et["rapporto_mandato"], et["max_eig"]))
    print("      STABILE (max <= %.3e)? %s" % (STABILE * RIF_MANDATO, "SI'" if et["stabile"] else "NO"))
    print("      IL BORDO: M %s;  K %s;  centro %+.4f  -- il quadrato (pi,0) %.4f  (pi,pi) %.4f"
          % ("  ".join("%s %.4f" % (k, v_) for k, v_ in et["M"].items()),
             "  ".join("%s %.4f" % (k, v_) for k, v_ in et["K"].items()), et["centro"],
             float(gq[h, 0]), float(gq[h, h])))
    print("      LA BANDA (escluso centro, M, K): %.4f a %s -- R2 sui triangoli %.4f"
          % (et["banda"], tuple(et["banda_k"]), r2t_b))
    print("      QUANTO I TRIANGOLI TOLGONO (1 - max tri / max quadrato, norma): R1 %.4f   R2 %.4f"
          "   (R2: %.4f contro %.4f)" % (et["tolto_r1"], et["tolto_r2"], float(r2t.max()),
                                         float(r2q.max())))
    with io.open(JSONL, "a", encoding="utf-8") as f:
        f.write(json.dumps({"letture": et}) + "\n")
    print("=" * 100)
    print("TRIANGOLI, R1: %d su %d   %s" % (OK[0], OK[1], "### TUTTI PASSATI"
                                            if OK[0] == OK[1] else "### CI SONO BUCHI"))
    print("=" * 100)
    return 0 if OK[0] == OK[1] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
