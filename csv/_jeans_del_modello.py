# -*- coding: utf-8 -*-
r"""**IL TEST DI JEANS DEL MODELLO, CON MATERIA UNIFORME DINAMICA** — *una misura.*

> ### ⛔ **Il task history e' `2026-10-19_jeans_del_modello.md`** *(`5f2a39e5`)*: la
> materia uniforme, le prove `M1`-`M4`, i bracci `J1`-`J4`, la misura e i criteri ### **sono
> fissati la', prima di questa corsa.** ### **`LINEARE` e `Lambda_c` restano FERMI.**

## ⭐ LA MATERIA UNIFORME

### **Lo stato invariante per traslazione:** su ogni estremita' lo spinore ALLINEATO col suo
`n` *(`statica_protocollo.chi_allineato`)*, ampiezza `sqrt(x)`, cosi' `rho_k = x Lambda_m`.
### **Stazionario per le DENSITA'** per simmetria del passo, ### **non autostato di `psi`.**

## ⛔ PRIMA LE PROVE, POI I BRACCI

`M1` equilibrio *(`256` ulp ogni `64` tick)* · `M2` `M`, `V` nella stessa banda, `G` riportata ·
`M3` lo spettro di `psi` solo a `k = 0` · `M4` il fit su una successione sintetica.
### **Se una cade: STOP**, e i bracci `J` NON si lanciano.
`J1` `x` in `{0.01, 0.1, 1}` · `J2` `cs` spento · `J3` `dtau 0.25` · `J4` il braccio di `D4` a
materia DINAMICA *(`congela = "no"`)* contro quello congelato di `963535bc`.

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
ULP_BANDA = 256.0              # _collauda_cs_l1.ULP_NORME, ogni 64 tick (la scala di D3)
TICK_BANDA = 64
JSONL = os.path.join(RADICE, "doc", "referti_l2", "jeans_del_modello.jsonl")
D4_JSONL = os.path.join(RADICE, "doc", "referti_l2", "d4_bracci.jsonl")

# nome -> (modo, x, dtau, tick, ampiezza)
BRACCI = {
    "M1 x 0.01": ("acceso", 0.01, 0.5, 2000, 0.0),
    "M1 x 0.1": ("acceso", 0.1, 0.5, 2000, 0.0),
    "M1 x 1": ("acceso", 1.0, 0.5, 2000, 0.0),
    "J1 x 0.01": ("acceso", 0.01, 0.5, 2000, 1e-6),
    "J1 x 0.1": ("acceso", 0.1, 0.5, 2000, 1e-6),
    "J1 x 1": ("acceso", 1.0, 0.5, 2000, 1e-6),
    "J2 cs SPENTO": ("spento", 0.1, 0.5, 2000, 1e-6),
    "J3 dtau 0.25": ("acceso", 0.1, 0.25, 4000, 1e-6),
}
RAPPORTO = 1.0


# =====================================================================================
#   LA SCENA E LA PERTURBAZIONE
# =====================================================================================
def scena(dtau, x):
    import scena_l2 as SC
    import statica_protocollo as PR
    inc, mot, st, par, _c, _per = SC.scena(dtau, PR.VUOTO, 0.0, PR.RAGGIO, False, True,
                                           False, PR.SEME, 1, lati=PR.LATI)
    st["psi_h"][...] = float(np.sqrt(x)) * PR.chi_allineato(PR.LATI, inc.m)
    return inc, mot, st, par


def perturba(st, a):
    """### `phi` e `psi` per `sqrt(1 + a r)`, `r` a media pesata nulla: ### **`V` e `M`.**"""
    g = np.random.default_rng(SEME)
    for chiave in ("phi_h", "psi_h"):
        v = st[chiave]
        w = np.abs(v) ** 2 if v.ndim == 1 else np.sum(np.abs(v) ** 2, axis=1)
        r = g.standard_normal(w.shape[0])
        r = r - float(np.sum(w * r)) / float(np.sum(w))
        f = np.sqrt(1.0 + a * r)
        if v.ndim == 1:
            v *= f
        else:
            v *= f.reshape(-1, 1)


def spettro_psi(inc, st, lati):
    """### `(potenza fuori da k = 0) / (potenza a k = 0)`, ### **per tipo d'estremita'.**"""
    import statica_protocollo as PR
    peggio = 0.0
    for tipo in range(4):
        h = np.arange(tipo % 2, 2 * inc.m, 2)[(np.arange(inc.m) % 2) == tipo // 2]
        for c in range(2):
            campo = np.zeros(inc.n, dtype=complex)
            campo[inc.nodo[h]] = st["psi_h"][h, c]
            f = np.abs(np.fft.fft2(campo.reshape(lati))) ** 2
            zero = float(f[0, 0])
            fuori = float(np.sum(f)) - zero
            if zero > 0:
                peggio = max(peggio, fuori / zero)
    _ = PR
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
    modo, x, dtau, tick, a = BRACCI[nome]
    inc, mot, st, par = scena(dtau, x)
    lm = float(np.mean(mot.densita_vuoto(st)))
    rm = float(np.mean(mot.densita_materia(st)))
    lc = RAPPORTO * lm
    fuori = {"nome": nome, "modo": modo, "x": x, "dtau": dtau, "tick": tick, "ampiezza": a,
             "lambda_m": lm, "rho_m": rm, "lambda_c": lc,
             "cs_m": 1.0 if modo == "spento" else lm / (lm + lc),
             "spettro": spettro_psi(inc, st, PR.LATI)}
    if a > 0:
        perturba(st, a)
    if modo != "spento":
        FP.accendi_cs(mot, lc, st)
    g0 = EP.g_dello_stato(mot, st, par)
    rho, lam, M, V, G = [], [], [], [], []

    def foto():
        rho.append(mot.densita_materia(st).copy())
        lam.append(mot.densita_vuoto(st).copy())
        M.append(float(np.sum(rho[-1])))
        V.append(float(np.sum(lam[-1])))
        G.append(float(EP.g_dello_stato(mot, st, par)))
    foto()
    fuori["non_converge"] = None
    try:
        for _t in range(tick):
            if modo == "spento":
                TK.tick(st, mot, par)
            else:
                TK.tick_con_cs(st, mot, par, lc, ())
            foto()
    except AssertionError as e:
        fuori["non_converge"] = {"tick": len(rho), "lam_min": float(np.min(lam[-1])),
                                 "lambda_c": lc, "msg": str(e)[:120]}
    rho, lam = np.array(rho), np.array(lam)
    t = np.arange(rho.shape[0])
    banda = ULP_BANDA * EPS * np.maximum(1.0, t / float(TICK_BANDA))
    fuori["m1_rho"] = float(np.max(np.max(np.abs(rho - rm), axis=1) / (banda * rm)))
    fuori["m1_lam"] = float(np.max(np.max(np.abs(lam - lm), axis=1) / (banda * lm)))
    fuori["m2_M"] = float(np.max(np.abs(np.array(M) - M[0]) / (banda * abs(M[0]))))
    fuori["m2_V"] = float(np.max(np.abs(np.array(V) - V[0]) / (banda * abs(V[0]))))
    fuori["m2_G"] = float(np.max(np.abs(np.array(G) - g0)) / abs(g0)) if g0 else None
    mr = np.max(np.abs(rho - rm), axis=1)
    ml = np.max(np.abs(lam - lm), axis=1)
    fuori["m_rho"] = [float(v) for v in mr]
    fuori["m_lam"] = [float(v) for v in ml]
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
    import statica_protocollo as PR
    import tick as TK
    PR.SOSTITUISCI = False
    lm = D4.lambda_medio(PR.DTAU[0])
    lc = RAPPORTO * lm
    rho_g = []
    vero = TK.tick_con_cs
    grumo = {"nodi": None}

    def avvolto(st, mot, par, lambda_c, salta):
        g = vero(st, mot, par, lambda_c, salta)
        if grumo["nodi"] is None:
            import scena_l2 as SC
            per = SC.anelli(PR.LATI, 0)
            grumo["nodi"] = [v for d, nn in per.items() if d <= PR.RAGGIO for v in nn]
        rho_g.append(float(np.mean(mot.densita_materia(st)[grumo["nodi"]])))
        return g
    TK.tick_con_cs = avvolto
    fuori = {"nome": "J4", "x": 0.01, "dtau": PR.DTAU[0], "tick": PR.TICK_SCAN,
             "acceso": PR.T_SCAN, "lambda_m": lm, "lambda_c": lc, "non_converge": None}
    try:
        lam, drho, _dt, per = PR.corri(PR.DTAU[0], 0.01, "S3", PR.TICK_SCAN, PR.T_SCAN,
                                       (0,), congela="no", lambda_c=lc)
        nodi = [v for d, nn in per.items() if d <= PR.RAGGIO for v in nn]
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
    """### `<delta Lambda>` del grumo per blocco, ### **dal braccio CONGELATO di `D4`.**"""
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
#   LE PROVE E LA LETTURA
# =====================================================================================
def m4():
    """### Il fit su `exp(gamma t)(1 + 0.01 n_t)`: ### **restituisce `gamma` entro 3 barre?**"""
    g = np.random.default_rng(SEME)
    fuori = []
    for gamma in (1e-3, 1e-2):
        t = np.arange(2001)
        m = 1e-6 * np.exp(gamma * t) * (1.0 + 0.01 * g.standard_normal(t.size))
        gf, b, t0, t1 = IV.gamma_del_tratto(m, 1.0)
        fuori.append((gamma, gf, b, t0, t1,
                      gf is not None and abs(gf - gamma) <= 3 * b))
    return fuori


def m4_diagnosi():
    """### INFORMAZIONE, non criterio: ### **lo stesso fit su `200` semi** *(0..199)*.

    ### Dice se lo strumento ha un BIAS *(la media di `z = (gamma_fit - gamma)/barra`)* e se
    le sue barre sono giuste *(la dispersione di `z`: `1` se lo sono)*, e quanti casi escono
    da `3` barre per caso.
    """
    fuori = []
    for gamma in (1e-3, 1e-2):
        z = []
        for s in range(200):
            g = np.random.default_rng(s)
            t = np.arange(2001)
            m = 1e-6 * np.exp(gamma * t) * (1.0 + 0.01 * g.standard_normal(t.size))
            gf, b, _t0, _t1 = IV.gamma_del_tratto(m, 1.0)
            z.append((gf - gamma) / b)
        z = np.array(z)
        fuori.append((gamma, float(np.mean(z)), float(np.std(z)),
                      float(np.mean(np.abs(z) > 3))))
    return fuori


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
    print("=" * 100)
    print("IL TEST DI JEANS DEL MODELLO, CON MATERIA UNIFORME DINAMICA -- una misura")
    print("=" * 100)
    print("  la scena di D4: lati %s, VUOTO %.1f; il passo: impronta %s; rapporto %g;"
          " congela = no" % (PR.LATI, PR.VUOTO, CM.IMPRONTA, RAPPORTO))
    print("  la materia: lo spinore allineato su ogni estremita', ampiezza sqrt(x); la"
          " perturbazione su psi e phi, seme %d" % SEME)
    print("  la banda di M1/M2: %g ulp ogni %d tick" % (ULP_BANDA, TICK_BANDA))
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
        print("  %-14s [%.0f s]%s" % (nome, time.time() - t0, "" if nc is None
                                      else "   ### NON CONVERGE al tick %d: %s"
                                      % (nc["tick"], nc["msg"][:70])))
        sys.stdout.flush()
    # ------------------------------------------------------------ M1-M4
    print("### SAPER CREARE LA MATERIA: M1-M4 (se una cade, STOP)")
    for nome in ("M1 x 0.01", "M1 x 0.1", "M1 x 1"):
        corri(nome)
    ok = True
    for nome in ("M1 x 0.01", "M1 x 0.1", "M1 x 1"):
        b = bb[nome]
        m1 = b["non_converge"] is None and b["m1_rho"] <= 1.0 and b["m1_lam"] <= 1.0
        m2 = b["m2_M"] <= 1.0 and b["m2_V"] <= 1.0
        m3 = b["spettro"] <= ULP_BANDA * EPS
        ok &= m1 and m2 and m3
        print("  %-12s M1 rho %.3f lam %.3f (di banda) %s | M2 M %.3f V %.3f %s, G %.3e"
              " | M3 fuori/zero %.2e %s"
              % (nome, b["m1_rho"], b["m1_lam"], "PASSA" if m1 else "### FALLISCE",
                 b["m2_M"], b["m2_V"], "PASSA" if m2 else "### FALLISCE",
                 b["m2_G"] if b["m2_G"] is not None else float("nan"), b["spettro"],
                 "PASSA" if m3 else "### FALLISCE"))
    for gamma, gf, b, t0, t1, passa in m4():
        ok &= passa
        print("  M4 gamma noto %.0e: il fit da' %s (tratto %d-%d)   %s"
              % (gamma, "non misurabile" if gf is None else "%.4e +- %.1e" % (gf, b), t0, t1,
                 "PASSA" if passa else "### FALLISCE"))
    print("  ### (nel test di ieri sera M4 NON c'era: lo strumento e' lo stesso, e vale"
          " anche per lui)")
    print("  ### INFORMAZIONE, non criterio: lo stesso fit su 200 semi (0..199)")
    for gamma, mz, sz, fz in m4_diagnosi():
        print("     gamma %.0e: media di z %+.2f (bias)   dispersione di z %.2f (1 se le barre"
              " sono giuste)   fuori da 3 barre %.1f%%" % (gamma, mz, sz, 100 * fz))
    if not ok:
        print("=" * 100)
        print("### ⛔ STOP: una prova di M1-M4 e' caduta -- i bracci J NON si lanciano.")
        print("=" * 100)
        return 1
    # ------------------------------------------------------------ J1-J4
    print("-" * 100)
    print("### I BRACCI J")
    for nome in ("J1 x 0.01", "J1 x 0.1", "J1 x 1", "J2 cs SPENTO", "J3 dtau 0.25", "J4"):
        corri(nome)
    print("-" * 100)
    print("### gamma (in tick e in tempo proprio) di max|delta rho| e di max|delta Lambda|")
    for nome in ("J1 x 0.01", "J1 x 0.1", "J1 x 1", "J2 cs SPENTO", "J3 dtau 0.25"):
        b = bb[nome]
        for chiave, che in (("rho", "rho"), ("lam", "Lambda")):
            r = b[chiave]
            if r["gamma"] is None:
                print("  %-14s %-7s non misurabile (tratto %d-%d)"
                      % (nome, che, r["T0"], r["T1"]))
                continue
            gt, btau = _gt(b, r)
            o = r.get("onda", {})
            inst = r["gamma"] > 0 and r["gamma"] >= 3 * r["barra"]
            print("  %-14s %-7s %+.3e +- %.1e (%5.1f) tick  %+.3e tempo proprio  %-10s"
                  " modo lambda %.2f (%d,%d) frazione %.2f"
                  % (nome, che, r["gamma"], r["barra"],
                     r["gamma"] / r["barra"] if r["barra"] > 0 else float("nan"), gt,
                     "INSTABILE" if inst else "no", o.get("lambda", float("nan")),
                     o.get("kx", 0), o.get("ky", 0), o.get("frazione", float("nan"))))
            gk = r.get("gamma_k", [])
            sopra = [q for q in gk if q[3] > 0 and q[2] >= 3 * q[3]]
            print("  %-14s %-7s gamma(|k|) sopra 3 barre: %s" % (
                "", "", ", ".join("|k| %d (lambda %.1f)" % (q[0], q[1]) for q in sopra)
                or "nessun anello -> nessuna lunghezza minima"))
    print("-" * 100)
    b1, b3 = bb["J1 x 0.1"], bb["J3 dtau 0.25"]
    for chiave in ("rho", "lam"):
        r1, r3 = b1[chiave], b3[chiave]
        if r1["gamma"] is None or r3["gamma"] is None:
            print("  J3 %s: non decidibile" % chiave)
            continue
        g1, s1 = _gt(b1, r1)
        g3, s3 = _gt(b3, r3)
        print("  J3 %-4s gamma in tempo proprio: dtau 0.5 %+.3e, dtau 0.25 %+.3e -> %s"
              % (chiave, g1, g3, "coincide entro 3 barre" if abs(g1 - g3)
                 <= 3 * np.sqrt(s1 * s1 + s3 * s3) else "NON coincide"))
    gl = [bb[n]["lam"]["gamma"] for n in ("J1 x 0.01", "J1 x 0.1", "J1 x 1")]
    print("  alla Jeans? gamma(Lambda) ai tre x: %s" % ", ".join(
        "non misurabile" if g is None else "%+.3e" % g for g in gl))
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
        print("  rho del grumo nel tempo (media sui nodi r <= %d): tick 1 %.4e, %s"
              % (PR.RAGGIO, rg[0], ", ".join("tick %d %.4e" % (k, rg[k - 1])
                                             for k in (100, 300, 600, 900, len(rg))
                                             if k <= len(rg))))
    print("=" * 100)
    print("### NESSUN VERDETTO DI FISICA OLTRE I CRITERI: i numeri. LINEARE e Lambda_c FERMI.")
    print("=" * 100)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
