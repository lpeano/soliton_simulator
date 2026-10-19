# -*- coding: utf-8 -*-
r"""**IL TEST DI INSTABILITA' DEL VUOTO UNIFORME** — *una misura, nessun codice di fisica.*

> ### ⛔ **Il task history e' `2026-10-19_instabilita_vuoto.md`** *(`027a3f70`, annotato in
> `91311771`)*, che fissa la scena, la perturbazione, i bracci, il tratto, le barre e i
> criteri ### **prima** di questa corsa. ### **`LINEARE` e `Lambda_c` restano FERMI.**

## ⭐ LA SCENA E LA PERTURBAZIONE

La scena di `D4` *(`statica_protocollo`: toro `31x31`, `Lambda_medio = 4`)* ### **senza
sorgente** *(`psi = 0`)*. Per ogni estremita' `h`, con `w_h = |phi_h|^2` e `r_h` normale
standard *(### seme `20261019`)*: `r <- r - (somma w r)/(somma w)` e
### **`phi_h <- phi_h * sqrt(1 + a r_h)`** -- la fase non cambia e `V` si conserva.

## ⭐ LA MISURA

`m(t) = max_k |Lambda_k(t) - Lambda_medio|`; ### **il tratto** da `T0 = 20` al primo tick con
`m >= 1e-2 Lambda_medio` *(o la fine)*, «non misurabile» sotto `50` tick; ### **`gamma`** la
media delle pendenze di `ln m` in `5` blocchi, la barra la loro deviazione su `sqrt(5)`;
### **in tempo proprio** `gamma / (dtau cs_m)`. ### **La lunghezza d'onda** del modo
dominante: la FFT 2D di `delta Lambda` al tick `T1`, il massimo di `|FFT|^2` escluso `k = 0`,
in archi, con la sua frazione di potenza.

## ⛔ I BRACCI

`(1)` `cs` acceso ai tre rapporti · `(2)` senza `CAMM-FASE-VUOTO` · `(3)` ### **`cs`
SPENTO, il caso che DEVE fallire** · `(4)` `dtau = 0.25`, `4000` tick · `(5)` ampiezza `1e-9`.
### **Un processo per braccio**, e ogni braccio si scrive SUBITO in
`doc/referti_l2/instabilita_vuoto.jsonl`.

Gira con:  python csv/_instabilita_vuoto.py
Un braccio: python csv/_instabilita_vuoto.py --braccio RAPPORTO DTAU TICK AMPIEZZA MODO
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

SEME = 20261019
T0 = 20
SOGLIA_PICCOLA = 1e-2
TRATTO_MIN = 50
BLOCCHI = 5
JSONL = os.path.join(RADICE, "doc", "referti_l2", "instabilita_vuoto.jsonl")
LEGGE_FASE = "CAMM-FASE-VUOTO"


# =====================================================================================
#   UN BRACCIO
# =====================================================================================
def perturba(st, a):
    """### `phi_h *= sqrt(1 + a r_h)`, con `somma w r = 0`: ### **`V` si conserva.**"""
    phi = st["phi_h"]
    w = np.abs(phi) ** 2
    r = np.random.default_rng(SEME).standard_normal(phi.shape[0])
    r = r - float(np.sum(w * r)) / float(np.sum(w))
    phi *= np.sqrt(1.0 + a * r)


def gamma_del_tratto(m, lm):
    """### `(gamma, barra, T0, T1)` in tick, ### **o `None` se il tratto e' troppo corto.**"""
    t1 = len(m)
    for t in range(T0, len(m)):
        if m[t] >= SOGLIA_PICCOLA * lm:
            t1 = t
            break
    if t1 - T0 < TRATTO_MIN:
        return None, None, T0, t1
    lati = np.linspace(T0, t1, BLOCCHI + 1).astype(int)
    pend = []
    for i in range(BLOCCHI):
        tt = np.arange(lati[i], lati[i + 1])
        pend.append(float(np.polyfit(tt, np.log(np.asarray(m)[tt]), 1)[0]))
    return (float(np.mean(pend)), float(np.std(pend, ddof=1)) / np.sqrt(BLOCCHI),
            T0, t1)


def onda(delta, lati):
    """### `(lambda in archi, kx, ky, frazione di potenza)` del modo dominante."""
    f = np.abs(np.fft.fft2(np.asarray(delta).reshape(lati))) ** 2
    tot = float(np.sum(f)) - float(f[0, 0])
    f[0, 0] = -1.0
    i, j = np.unravel_index(int(np.argmax(f)), f.shape)
    kx = i if i <= lati[0] // 2 else i - lati[0]
    ky = j if j <= lati[1] // 2 else j - lati[1]
    lam = 1.0 / np.sqrt((kx / float(lati[0])) ** 2 + (ky / float(lati[1])) ** 2)
    return float(lam), int(kx), int(ky), float(f[i, j]) / tot if tot > 0 else float("nan")


def braccio(rapporto, dtau, tick, a, modo):
    import flussi_parziali as FP
    import scena_l2 as SC
    import statica_protocollo as PR
    import tick as TK
    _inc, mot, st, par, _c, _per = SC.scena(dtau, PR.VUOTO, 0.0, PR.RAGGIO, False, True,
                                            False, PR.SEME, 1, lati=PR.LATI)
    lm = float(np.mean(mot.densita_vuoto(st)))
    lc = rapporto * lm
    perturba(st, a)
    salta = (LEGGE_FASE,) if modo == "senza_fase" else ()
    if modo != "spento":
        FP.accendi_cs(mot, lc, st)
    campi = [mot.densita_vuoto(st).copy()]
    fuori = {"rapporto": rapporto, "dtau": dtau, "tick": tick, "ampiezza": a, "modo": modo,
             "lambda_medio": lm, "lambda_c": lc,
             "cs_m": 1.0 if modo == "spento" else lm / (lm + lc),
             "V_prima_dopo": [float(np.sum(campi[0])), None]}
    try:
        for _t in range(tick):
            if modo == "spento":
                TK.tick(st, mot, par)
            else:
                TK.tick_con_cs(st, mot, par, lc, salta)
            campi.append(mot.densita_vuoto(st).copy())
        fuori["non_converge"] = None
    except AssertionError as e:
        lam = mot.densita_vuoto(st)
        fuori["non_converge"] = {"tick": len(campi), "lam_min": float(np.min(lam)),
                                 "lambda_c": lc, "msg": str(e)[:120]}
    campi = np.array(campi)
    fuori["V_prima_dopo"][1] = float(np.sum(campi[-1]))
    m = np.max(np.abs(campi - lm), axis=1)
    g, b, t0, t1 = gamma_del_tratto(m, lm)
    fuori.update({"m": [float(v) for v in m], "gamma": g, "barra": b, "T0": t0, "T1": t1})
    if t1 > 0:
        w = onda(campi[min(t1, len(campi) - 1)] - lm, PR.LATI)
        fuori["onda"] = {"lambda": w[0], "kx": w[1], "ky": w[2], "frazione": w[3]}
    return fuori


def lancia(*arg):
    out = subprocess.run([sys.executable, os.path.abspath(__file__), "--braccio"]
                         + [str(x) for x in arg], capture_output=True)
    righe = out.stdout.decode("utf-8", "replace").strip().splitlines()
    assert out.returncode == 0 and righe, ("il braccio %r e' morto: %s"
                                           % (arg, out.stderr.decode("utf-8", "replace")
                                              [-600:]))
    return json.loads(righe[-1])


# =====================================================================================
#   LA LETTURA
# =====================================================================================
def _gt(b):
    """### `gamma` in tempo proprio e la sua barra."""
    s = b["dtau"] * b["cs_m"]
    return b["gamma"] / s, b["barra"] / s


def _instabile(b):
    return b["gamma"] is not None and b["gamma"] > 0 and b["gamma"] >= 3 * b["barra"]


def main(argv):
    if argv[:1] == ["--braccio"]:
        a = argv[1:]
        r = braccio(float(a[0]), float(a[1]), int(a[2]), float(a[3]), a[4])
        sys.stdout.write(json.dumps(r) + "\n")
        return 0
    import _presidio
    _presidio.avvia(__file__)
    import composizione as CM
    import statica_protocollo as PR
    piano = [("(1) r 0.1", (0.1, 0.5, 2000, 1e-6, "acceso")),
             ("(1) r 1", (1.0, 0.5, 2000, 1e-6, "acceso")),
             ("(1) r 10", (10.0, 0.5, 2000, 1e-6, "acceso")),
             ("(2) senza fase", (1.0, 0.5, 2000, 1e-6, "senza_fase")),
             ("(3) cs SPENTO", (1.0, 0.5, 2000, 1e-6, "spento")),
             ("(4) dtau 0.25", (1.0, 0.25, 4000, 1e-6, "acceso")),
             ("(5) ampiezza 1e-9", (1.0, 0.5, 2000, 1e-9, "acceso"))]
    print("=" * 100)
    print("IL TEST DI INSTABILITA' DEL VUOTO UNIFORME -- una misura")
    print("=" * 100)
    print("  la scena di D4 senza sorgente: lati %s, VUOTO %.1f, SEME scena %d; il passo:"
          " impronta %s" % (PR.LATI, PR.VUOTO, PR.SEME, CM.IMPRONTA))
    print("  la perturbazione: phi_h *= sqrt(1 + a r_h), r normale, seme %d, somma w r = 0"
          % SEME)
    print("  il tratto: da T0 = %d al primo m >= %g Lambda_m (minimo %d tick); %d blocchi"
          % (T0, SOGLIA_PICCOLA, TRATTO_MIN, BLOCCHI))
    print("  i bracci si salvano mentre corrono in %s" % os.path.relpath(JSONL, RADICE))
    print("-" * 100)
    sys.stdout.flush()
    io.open(JSONL, "w", encoding="utf-8").close()
    bb = {}
    for nome, arg in piano:
        t0 = time.time()
        b = lancia(*arg)
        bb[nome] = b
        with io.open(JSONL, "a", encoding="utf-8") as f:
            f.write(json.dumps(b) + "\n")
        nc = b["non_converge"]
        print("  %-18s m(0) %.2e  m(fine) %.2e  V %.15g -> %.15g%s  [%.0f s]"
              % (nome, b["m"][0], b["m"][-1], b["V_prima_dopo"][0], b["V_prima_dopo"][1],
                 "" if nc is None else "   ### NON CONVERGE al tick %d (Lambda min %.4f,"
                 " Lambda_c %.4f)" % (nc["tick"], nc["lam_min"], nc["lambda_c"]),
                 time.time() - t0))
        sys.stdout.flush()
    print("-" * 100)
    print("### gamma, nel tratto (in tick e in tempo proprio), e il modo che cresce")
    print("  %-18s %-12s %-26s %-26s %-6s %s"
          % ("braccio", "tratto", "gamma / tick (barre)", "gamma / tempo proprio",
             "inst.", "il modo: lambda (kx,ky) frazione"))
    for nome, _arg in piano:
        b = bb[nome]
        o = b.get("onda") or {}
        if b["gamma"] is None:
            print("  %-18s %-12s non misurabile (tratto < %d tick)"
                  % (nome, "%d-%d" % (b["T0"], b["T1"]), TRATTO_MIN))
            continue
        gt, btau = _gt(b)
        print("  %-18s %-12s %+.3e +- %.1e (%5.1f)  %+.3e +- %.1e   %-6s %.2f (%d,%d) %.2f"
              % (nome, "%d-%d" % (b["T0"], b["T1"]), b["gamma"], b["barra"],
                 b["gamma"] / b["barra"] if b["barra"] > 0 else float("nan"), gt, btau,
                 "SI" if _instabile(b) else "no", o.get("lambda", float("nan")),
                 o.get("kx", 0), o.get("ky", 0), o.get("frazione", float("nan"))))
    print("-" * 100)
    print("### I CRITERI (task history 027a3f70, annotazione 91311771)")
    ok = [0, 0]

    def esito(che, passa, nota):
        ok[1] += 1
        ok[0] += 1 if passa else 0
        print("  %-64s %s   %s" % (che[:64], "PASSA" if passa else "### FALLISCE", nota))
    b3 = bb["(3) cs SPENTO"]
    esito("(3) il caso che DEVE fallire: a cs SPENTO NON e' instabile",
          b3["gamma"] is not None and not _instabile(b3),
          "gamma %s" % ("non misurabile" if b3["gamma"] is None
                        else "%+.3e a %.1f barre" % (b3["gamma"], b3["gamma"] / b3["barra"])))
    for nome in ("(1) r 0.1", "(1) r 1", "(1) r 10", "(2) senza fase"):
        b = bb[nome]
        print("  %-64s %s" % (nome + ": instabile?", "non misurabile" if b["gamma"] is None
                              else ("### SI'" if _instabile(b) else "no")))
    b1, b4, b5 = bb["(1) r 1"], bb["(4) dtau 0.25"], bb["(5) ampiezza 1e-9"]
    if b1["gamma"] is not None and b4["gamma"] is not None:
        g1, s1 = _gt(b1)
        g4, s4 = _gt(b4)
        fis = abs(g1 - g4) <= 3 * np.sqrt(s1 * s1 + s4 * s4)
        print("  (4) gamma in tempo proprio: dtau 0.5 %+.3e, dtau 0.25 %+.3e -> %s"
              "   (in tick: %+.3e e %+.3e)"
              % (g1, g4, "FISICA (coincide entro 3 barre)" if fis
                 else "NUMERICA (non coincide entro 3 barre)", b1["gamma"], b4["gamma"]))
    else:
        print("  (4) non decidibile: gamma non misurabile in uno dei due bracci")
    if b1["gamma"] is not None and b5["gamma"] is not None:
        lin = abs(b1["gamma"] - b5["gamma"]) <= 3 * np.sqrt(b1["barra"] ** 2
                                                            + b5["barra"] ** 2)
        print("  (5) gamma a 1e-6 %+.3e, a 1e-9 %+.3e -> %s"
              % (b1["gamma"], b5["gamma"], "LINEARE" if lin else "NON lineare"))
    else:
        print("  (5) non decidibile: gamma non misurabile in uno dei due bracci")
    print("=" * 100)
    print("### I CRITERI DI CONTROLLO: %d su %d.  ### NESSUNA DECISIONE: LINEARE e Lambda_c"
          " restano FERMI." % (ok[0], ok[1]))
    print("=" * 100)
    return 0 if ok[0] == ok[1] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
