# -*- coding: utf-8 -*-
r"""**IL TEST DI JEANS DEL MODELLO: I BRACCI DIAGNOSTICI** — *una misura, nessun codice di fisica.*

> ### ⛔ **Il task history e' `2026-10-19_jeans_del_modello.md`** *(`5f2a39e5`)*, con
> l'annotazione della decisione di Luca delle `21:45` *(`6f5299e2`)*: ### **`M1` e'
> l'equilibrio al tick `0`**, ### **le barre del fit usano la `t` di Student coi gradi di
> liberta' veri**, e ### **i bracci sono diagnostici, dal SOLO rumore d'arrotondamento.**
> ### **`LINEARE` e `Lambda_c` restano FERMI.**
> ### ⚠ **La versione di `d85360ab` aveva `M1` sbagliata** *(errore `n.18`: «resta uniforme
> per tutta la corsa» e' la domanda, non una precondizione)* e le barre gaussiane.

## ⭐ LA MATERIA UNIFORME

Lo stato invariante per traslazione: su ogni estremita' lo spinore ALLINEATO col suo `n`
*(`statica_protocollo.chi_allineato`)*, ampiezza `sqrt(x)`, `rho_k = x Lambda_m`.

## ⛔ LE PROVE *(se una cade: STOP)*

`M1` ### **la variazione di `rho_k` e `Lambda_k` nel PRIMO tick entro `256` ulp della scala**;
`M3` lo spettro di `psi` solo a `k = 0`; `M4` ### **la copertura della soglia di Student sui
semi `0`..`199`: `99.73%` entro `3` deviazioni binomiali.**

## ⭐ I BRACCI *(rapporto `1`, `dtau 0.5`, `2000` tick, `x = 0.1` se non detto; NESSUNA
perturbazione aggiunta)*

`D1` `x` in `{0.01, 0.1, 1}` · `D2` `cs` SPENTO · `D3` `dtau 0.25`, `4000` tick · `D4'` senza
`CAMM-FASE-VUOTO` · `D5` in ogni braccio, ### **la deriva di `G` nella fase esponenziale**
contro `max|delta rho|/rho_m` · `J4` ### **il braccio di `D4` a materia DINAMICA.**
### **Se il punto fisso di `cs` non converge, il braccio si chiude li'.**

Gira con:  python csv/_jeans_del_modello.py
Un braccio: python csv/_jeans_del_modello.py --braccio NOME
"""
import io
import json
import os
import subprocess
import sys
import time

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
_PO = os.path.join(RADICE, "primo_ordine")
for _p in (_QUI, _PO, os.path.join(_PO, "leggi")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import numpy as np                                             # noqa: E402

import _instabilita_vuoto as IV                                 # noqa: E402

SEME = 20261019
EPS = float(np.finfo(float).eps)
ULP_BANDA = 256.0              # _collauda_cs_l1.ULP_NORME
COPERTURA = 0.9973             # il significato di <<3 barre>>, tenuto (decisione di Luca)
SEMI_M4 = range(200)           # dichiarati nel task history
JSONL = os.path.join(RADICE, "doc", "referti_l2", "jeans_del_modello.jsonl")
D4_JSONL = os.path.join(RADICE, "doc", "referti_l2", "d4_bracci.jsonl")
IV_JSONL = os.path.join(RADICE, "doc", "referti_l2", "instabilita_vuoto.jsonl")
LEGGE_FASE = "CAMM-FASE-VUOTO"
RAPPORTO = 1.0

# nome -> (modo, x, dtau, tick)
BRACCI = {
    "D1 x 0.01": ("acceso", 0.01, 0.5, 2000),
    "D1 x 0.1": ("acceso", 0.1, 0.5, 2000),
    "D1 x 1": ("acceso", 1.0, 0.5, 2000),
    "D2 cs SPENTO": ("spento", 0.1, 0.5, 2000),
    "D3 dtau 0.25": ("acceso", 0.1, 0.25, 4000),
    "D4' senza fase": ("senza_fase", 0.1, 0.5, 2000),
}


def t_soglia():
    """### La soglia di Student al `99.73%` coi gradi di liberta' dei blocchi."""
    import scipy.stats as SS
    return float(SS.t.ppf(1.0 - (1.0 - COPERTURA) / 2.0, IV.BLOCCHI - 1))


# =====================================================================================
#   LA SCENA
# =====================================================================================
def scena(dtau, x):
    import scena_l2 as SC
    import statica_protocollo as PR
    inc, mot, st, par, _c, _per = SC.scena(dtau, PR.VUOTO, 0.0, PR.RAGGIO, False, True,
                                           False, PR.SEME, 1, lati=PR.LATI)
    st["psi_h"][...] = float(np.sqrt(x)) * PR.chi_allineato(PR.LATI, inc.m)
    return inc, mot, st, par


def spettro_psi(inc, st, lati):
    """### `(potenza fuori da k = 0) / (potenza a k = 0)`, ### **per tipo d'estremita'.**"""
    peggio = 0.0
    for tipo in range(4):
        h = np.arange(tipo % 2, 2 * inc.m, 2)[(np.arange(inc.m) % 2) == tipo // 2]
        for c in range(2):
            campo = np.zeros(inc.n, dtype=complex)
            campo[inc.nodo[h]] = st["psi_h"][h, c]
            f = np.abs(np.fft.fft2(campo.reshape(lati))) ** 2
            zero = float(f[0, 0])
            if zero > 0:
                peggio = max(peggio, (float(np.sum(f)) - zero) / zero)
    return peggio


def gamma_k(d0, d1, t0, t1, lati):
    """### `gamma(k)` per anelli di `|k|`: `[(|k|, lambda, media, barra, n)]`."""
    p0 = np.abs(np.fft.fft2(np.asarray(d0).reshape(lati))) ** 2
    p1 = np.abs(np.fft.fft2(np.asarray(d1).reshape(lati))) ** 2
    kx = np.fft.fftfreq(lati[0]) * lati[0]
    ky = np.fft.fftfreq(lati[1]) * lati[1]
    KX, KY = np.meshgrid(kx, ky, indexing="ij")
    kk = np.rint(np.sqrt(KX ** 2 + KY ** 2)).astype(int)
    ok = (p0 > 0) & (p1 > 0)
    g = np.full(p0.shape, np.nan)
    g[ok] = np.log(p1[ok] / p0[ok]) / (2.0 * (t1 - t0))
    fuori = []
    for q in range(1, int(kk.max()) + 1):
        sel = (kk == q) & ok
        n = int(np.sum(sel))
        if n < 2:
            continue
        v = g[sel]
        fuori.append((q, lati[0] / float(q), float(np.mean(v)),
                      float(np.std(v, ddof=1)) / np.sqrt(n), n))
    return fuori


# =====================================================================================
#   UN BRACCIO
# =====================================================================================
def braccio(nome):
    import energia_pesata as EP
    import flussi_parziali as FP
    import statica_protocollo as PR
    import tick as TK
    if nome == "J4":
        return braccio_j4()
    modo, x, dtau, tick = BRACCI[nome]
    inc, mot, st, par = scena(dtau, x)
    lm = float(np.mean(mot.densita_vuoto(st)))
    rm = float(np.mean(mot.densita_materia(st)))
    lc = RAPPORTO * lm
    fuori = {"nome": nome, "modo": modo, "x": x, "dtau": dtau, "tick": tick,
             "lambda_m": lm, "rho_m": rm, "lambda_c": lc,
             "cs_m": 1.0 if modo == "spento" else lm / (lm + lc),
             "spettro": spettro_psi(inc, st, PR.LATI)}
    salta = (LEGGE_FASE,) if modo == "senza_fase" else ()
    if modo != "spento":
        FP.accendi_cs(mot, lc, st)
    rho, lam, G = [], [], []

    def foto():
        rho.append(mot.densita_materia(st).copy())
        lam.append(mot.densita_vuoto(st).copy())
        G.append(float(EP.g_dello_stato(mot, st, par)))
    foto()
    fuori["non_converge"] = None
    try:
        for _t in range(tick):
            if modo == "spento":
                TK.tick(st, mot, par)
            else:
                TK.tick_con_cs(st, mot, par, lc, salta)
            foto()
    except AssertionError as e:
        # ### ⛔ **il braccio si CHIUDE qui**: si registra, senza cure.
        fuori["non_converge"] = {"tick": len(rho), "lam_min": float(np.min(lam[-1])),
                                 "lambda_c": lc, "msg": str(e)[:120]}
    rho, lam, G = np.array(rho), np.array(lam), np.array(G)
    # ### `M1` RIDEFINITA: l'equilibrio al tick 0 -- la variazione nel PRIMO tick
    if rho.shape[0] > 1:
        fuori["m1_rho_ulp"] = float(np.max(np.abs(rho[1] - rho[0]))) / (EPS * rm)
        fuori["m1_lam_ulp"] = float(np.max(np.abs(lam[1] - lam[0]))) / (EPS * lm)
    mr = np.max(np.abs(rho - rm), axis=1)
    ml = np.max(np.abs(lam - lm), axis=1)
    fuori["m_rho"] = [float(v) for v in mr]
    fuori["m_lam"] = [float(v) for v in ml]
    fuori["G"] = [float(v) for v in G]
    # ### `D5`: la deriva di G nella SOLA fase esponenziale
    fine = len(mr) - 1
    for t in range(len(mr)):
        if mr[t] >= IV.SOGLIA_PICCOLA * rm:
            fine = t
            break
    dg = float(abs(G[fine] - G[0]) / abs(G[0])) if G[0] else float("nan")
    dg20 = float(abs(G[min(IV.T0, fine)] - G[0]) / abs(G[0])) if G[0] else float("nan")
    cresc = float(mr[fine] / rm)
    fuori["d5"] = {"fine": int(fine), "dG_rel_fine": dg, "dG_rel_T0": dg20,
                   "crescita_fine": cresc, "rapporto": dg / cresc if cresc > 0 else None}
    for chiave, m, scala, campi, centro in (("rho", mr, rm, rho, rm),
                                            ("lam", ml, lm, lam, lm)):
        g, b, t0, t1 = IV.gamma_del_tratto(m, scala)
        r = {"gamma": g, "barra": b, "T0": t0, "T1": t1}
        if g is not None:
            t1c = min(t1, campi.shape[0] - 1)
            w = IV.onda(campi[t1c] - centro, PR.LATI)
            r["onda"] = {"lambda": w[0], "kx": w[1], "ky": w[2], "frazione": w[3]}
            r["gamma_k"] = gamma_k(campi[t0] - centro, campi[t1c] - centro, t0, t1c, PR.LATI)
        fuori[chiave] = r
    return fuori


def braccio_j4():
    """### Il braccio di `D4` a rapporto `1`, `x 0.01`, ### **con la materia DINAMICA.**"""
    import _misura_d4 as D4
    import scena_l2 as SC
    import statica_protocollo as PR
    import tick as TK
    PR.SOSTITUISCI = False
    lm = D4.lambda_medio(PR.DTAU[0])
    lc = RAPPORTO * lm
    per = SC.anelli(PR.LATI, 0)
    nodi = [v for d, nn in per.items() if d <= PR.RAGGIO for v in nn]
    rho_g = []
    vero = TK.tick_con_cs

    def avvolto(st, mot, par, lambda_c, salta):
        g = vero(st, mot, par, lambda_c, salta)
        rho_g.append(float(np.mean(mot.densita_materia(st)[nodi])))
        return g
    TK.tick_con_cs = avvolto
    fuori = {"nome": "J4", "x": 0.01, "dtau": PR.DTAU[0], "tick": PR.TICK_SCAN,
             "acceso": PR.T_SCAN, "lambda_m": lm, "lambda_c": lc, "non_converge": None}
    try:
        lam, drho, _dt, _per = PR.corri(PR.DTAU[0], 0.01, "S3", PR.TICK_SCAN, PR.T_SCAN,
                                        (0,), congela="no", lambda_c=lc)
        bl = PR.blocchi(lam, PR.inizio_finestra(PR.T_SCAN), PR.FINESTRE)
        fuori["dlam_blocchi"] = [float(v) for v in np.mean(bl[:, nodi], axis=1) - lm]
        fuori["drho_max"] = drho
    except AssertionError as e:
        fuori["non_converge"] = {"tick": len(rho_g), "msg": str(e)[:120]}
    finally:
        TK.tick_con_cs = vero
    fuori["rho_grumo"] = rho_g
    return fuori


def congelato_d4():
    import statica_protocollo as PR
    for r in io.open(D4_JSONL, encoding="utf-8"):
        b = json.loads(r)
        if (b["quale"] == "sorgente" and b["rapporto"] == RAPPORTO and b["dtau"] == 0.5
                and b["x"] == 0.01 and b["tick"] == PR.TICK_SCAN):
            an = [d for d in b["anelli"] if int(d) <= PR.RAGGIO]
            tot = sum(b["anelli"][d]["n"] for d in an)
            v = sum(b["anelli"][d]["n"] * np.array(b["anelli"][d]["lam"]) for d in an) / tot
            return [float(q) for q in v - b["lambda_medio"]]
    return None


def lancia(nome):
    out = subprocess.run([sys.executable, os.path.abspath(__file__), "--braccio", nome],
                         capture_output=True)
    righe = out.stdout.decode("utf-8", "replace").strip().splitlines()
    assert out.returncode == 0 and righe, ("il braccio %r e' morto: %s"
                                           % (nome, out.stderr.decode("utf-8", "replace")
                                              [-600:]))
    return json.loads(righe[-1])


# =====================================================================================
#   LE PROVE DELLO STRUMENTO
# =====================================================================================
def m4(ts):
    """### La copertura della soglia di Student sui semi `0`..`199`, a due `gamma` noti."""
    fuori = []
    for gamma in (1e-3, 1e-2):
        z = []
        for s in SEMI_M4:
            g = np.random.default_rng(s)
            t = np.arange(2001)
            m = 1e-6 * np.exp(gamma * t) * (1.0 + 0.01 * g.standard_normal(t.size))
            gf, b, _t0, _t1 = IV.gamma_del_tratto(m, 1.0)
            z.append((gf - gamma) / b)
        z = np.array(z)
        cop = float(np.mean(np.abs(z) <= ts))
        err = np.sqrt(COPERTURA * (1.0 - COPERTURA) / len(z))
        fuori.append((gamma, cop, err, abs(cop - COPERTURA) <= 3 * err,
                      float(np.mean(z)), float(np.std(z))))
    return fuori


def ieri_sera(ts):
    """### I verdetti del test d'instabilita' (`c2dd6453`) con la soglia di Student."""
    righe = []
    for r in io.open(IV_JSONL, encoding="utf-8"):
        b = json.loads(r)
        if b["gamma"] is None:
            continue
        z = b["gamma"] / b["barra"]
        righe.append((b["modo"], b["rapporto"], b["dtau"], b["ampiezza"], z, z >= ts))
    return righe


def _gt(b, r):
    s = b["dtau"] * b["cs_m"]
    return r["gamma"] / s, r["barra"] / s


def main(argv):
    if argv[:1] == ["--braccio"]:
        sys.stdout.write(json.dumps(braccio(argv[1])) + "\n")
        return 0
    import _presidio
    _presidio.avvia(__file__)
    import composizione as CM
    import statica_protocollo as PR
    ts = t_soglia()
    print("=" * 100)
    print("IL TEST DI JEANS DEL MODELLO: I BRACCI DIAGNOSTICI -- una misura")
    print("=" * 100)
    print("  la scena di D4: lati %s, VUOTO %.1f; il passo: impronta %s; rapporto %g;"
          " NESSUNA perturbazione aggiunta: il solo rumore d'arrotondamento"
          % (PR.LATI, PR.VUOTO, CM.IMPRONTA, RAPPORTO))
    print("  la soglia: t di Student al %.2f%% con %d gradi di liberta' = %.3f barre"
          % (100 * COPERTURA, IV.BLOCCHI - 1, ts))
    print("  i bracci si salvano mentre corrono in %s" % os.path.relpath(JSONL, RADICE))
    print("-" * 100)
    sys.stdout.flush()
    io.open(JSONL, "w", encoding="utf-8").close()
    bb = {}

    def corri(nome):
        t0 = time.time()
        b = lancia(nome)
        bb[nome] = b
        with io.open(JSONL, "a", encoding="utf-8") as f:
            f.write(json.dumps(b) + "\n")
        nc = b.get("non_converge")
        print("  %-15s [%.0f s]%s" % (nome, time.time() - t0, "" if nc is None
                                      else "   ### NON CONVERGE al tick %d, il braccio si"
                                      " chiude li': %s" % (nc["tick"], nc["msg"][:60])))
        sys.stdout.flush()
    # ------------------------------------------------------------ le prove
    print("### LE PROVE (se una cade, STOP)")
    for nome in ("D1 x 0.01", "D1 x 0.1", "D1 x 1"):
        corri(nome)
    ok = True
    for nome in ("D1 x 0.01", "D1 x 0.1", "D1 x 1"):
        b = bb[nome]
        m1 = (b["m1_rho_ulp"] <= ULP_BANDA and b["m1_lam_ulp"] <= ULP_BANDA)
        m3 = b["spettro"] <= ULP_BANDA * EPS
        ok &= m1 and m3
        print("  %-12s M1 (il primo tick): rho %.1f ulp, Lambda %.1f ulp (banda %g)  %s"
              "   | M3 fuori/zero %.1e  %s"
              % (nome, b["m1_rho_ulp"], b["m1_lam_ulp"], ULP_BANDA,
                 "PASSA" if m1 else "### FALLISCE", b["spettro"],
                 "PASSA" if m3 else "### FALLISCE"))
    for gamma, cop, err, passa, mz, sz in m4(ts):
        ok &= passa
        print("  M4 gamma noto %.0e, semi 0..199: copertura %.4f (attesa %.4f +- %.4f)  %s"
              "   [media di z %+.2f, dispersione %.2f]"
              % (gamma, cop, COPERTURA, err, "PASSA" if passa else "### FALLISCE", mz, sz))
    print("  ### I VERDETTI DEL TEST DI IERI SERA (c2dd6453) con la soglia %.2f:" % ts)
    for modo, rap, dt, a, z, inst in ieri_sera(ts):
        print("     %-11s rapporto %-5g dtau %-5g ampiezza %-6g  %+.1f barre  %s"
              % (modo, rap, dt, a, z, "### INSTABILE" if inst else "no"))
    if not ok:
        print("=" * 100)
        print("### ⛔ STOP: una prova e' caduta -- i bracci diagnostici NON si lanciano.")
        print("=" * 100)
        return 1
    # ------------------------------------------------------------ i bracci
    print("-" * 100)
    print("### I BRACCI DIAGNOSTICI (dal solo rumore)")
    for nome in ("D2 cs SPENTO", "D3 dtau 0.25", "D4' senza fase", "J4"):
        corri(nome)
    print("-" * 100)
    print("### gamma (in tick e in tempo proprio), il modo, la lunghezza minima")
    nomi = ("D1 x 0.01", "D1 x 0.1", "D1 x 1", "D2 cs SPENTO", "D3 dtau 0.25",
            "D4' senza fase")
    for nome in nomi:
        b = bb[nome]
        for chiave, che in (("rho", "rho"), ("lam", "Lambda")):
            r = b[chiave]
            if r["gamma"] is None:
                print("  %-15s %-7s non misurabile (tratto %d-%d)"
                      % (nome, che, r["T0"], r["T1"]))
                continue
            gt, _bt = _gt(b, r)
            o = r.get("onda", {})
            z = r["gamma"] / r["barra"] if r["barra"] > 0 else float("inf")
            print("  %-15s %-7s %+.4e +- %.1e (%6.1f barre) per tick  %+.4e tempo proprio"
                  "  %-10s modo lambda %.2f (%d,%d) %.2f"
                  % (nome, che, r["gamma"], r["barra"], z, gt,
                     "INSTABILE" if r["gamma"] > 0 and z >= ts else "no",
                     o.get("lambda", float("nan")), o.get("kx", 0), o.get("ky", 0),
                     o.get("frazione", float("nan"))))
            gk = r.get("gamma_k", [])
            sopra = [q for q in gk if q[3] > 0 and q[2] >= ts * q[3]]
            print("  %-15s %-7s anelli |k| con gamma(k) sopra la soglia: %s" % (
                "", "", ", ".join("%d (lambda %.1f)" % (q[0], q[1]) for q in sopra)
                or "nessuno"))
    print("-" * 100)
    print("### D1: gamma(rho) contro x")
    for nome in ("D1 x 0.01", "D1 x 0.1", "D1 x 1"):
        r = bb[nome]["rho"]
        print("  %-12s x %-5g gamma %s" % (nome, bb[nome]["x"], "non misurabile"
                                           if r["gamma"] is None else "%+.4e" % r["gamma"]))
    print("### D3: fisica o numerica")
    b1, b3 = bb["D1 x 0.1"], bb["D3 dtau 0.25"]
    for chiave in ("rho", "lam"):
        r1, r3 = b1[chiave], b3[chiave]
        if r1["gamma"] is None or r3["gamma"] is None:
            print("  %-4s non decidibile" % chiave)
            continue
        g1, s1 = _gt(b1, r1)
        g3, s3 = _gt(b3, r3)
        print("  %-4s tempo proprio: dtau 0.5 %+.4e, dtau 0.25 %+.4e -> %s   (per tick: %+.4e"
              " e %+.4e)" % (chiave, g1, g3, "FISICA (coincide entro la soglia)"
                             if abs(g1 - g3) <= ts * np.sqrt(s1 * s1 + s3 * s3)
                             else "NUMERICA (non coincide)", r1["gamma"], r3["gamma"]))
    print("### D2 e D4': quale legge alimenta la crescita")
    for nome in ("D2 cs SPENTO", "D4' senza fase"):
        r = bb[nome]["rho"]
        cresce = r["gamma"] is not None and r["gamma"] > 0 and r["gamma"] >= ts * r["barra"]
        print("  %-15s cresce? %s" % (nome, "SI'" if cresce else "no"))
    print("### D5: la deriva di G nella fase esponenziale (fino a max|delta rho| = 1%% rho_m)")
    for nome in nomi:
        d = bb[nome]["d5"]
        print("  %-15s fine %4d  |dG/G| al tick %d %.2e, alla fine %.2e;  max|delta rho|/rho_m"
              " %.2e;  rapporto %s"
              % (nome, d["fine"], IV.T0, d["dG_rel_T0"], d["dG_rel_fine"], d["crescita_fine"],
                 "%.2e" % d["rapporto"] if d["rapporto"] is not None else "--"))
    print("-" * 100)
    print("### J4: LA PROVA DEL PROTOCOLLO -- <delta Lambda> nel grumo per blocco")
    j4 = bb["J4"]
    cg = congelato_d4()
    if j4["non_converge"] is not None:
        print("  ### J4 NON CONVERGE: %s" % j4["non_converge"]["msg"])
    else:
        print("  %-8s %-16s %s" % ("blocco", "DINAMICA (J4)", "CONGELATA (963535bc)"))
        for i, v in enumerate(j4["dlam_blocchi"]):
            print("  %-8d %+-16.4f %s" % (i, v, "%+.4f" % cg[i] if cg else "--"))
    rg = j4["rho_grumo"]
    if rg:
        print("  rho del grumo (media sui nodi r <= %d): %s"
              % (PR.RAGGIO, ", ".join("tick %d %.4e" % (k, rg[k - 1])
                                      for k in (1, 100, 300, 600, 900, len(rg))
                                      if k <= len(rg))))
    print("=" * 100)
    print("### NESSUN VERDETTO DI FISICA OLTRE fisica/numerica E la legge che alimenta la"
          " crescita. LINEARE e Lambda_c FERMI.")
    print("=" * 100)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
