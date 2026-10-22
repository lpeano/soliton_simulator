# -*- coding: utf-8 -*-
r"""**LA MASSA DELLA CAMMINATA VICINO AL CONO: `Delta(s)` fra `0.5` e `1`, e la prova che conta solo `s`** *(e quindi `cs`)*.

> ### ⛔ **Il task history e' `2026-10-22_massa_vicino_al_cono.md`.** ### **`dtau`, `eps` e `cs` SOLO nella scena** *(in memoria)*; ### **`leggi.yaml` e
> l'impronta intatti.**

## IL METODO *(dichiarato nel task history)*
### **Le fasi PER TICK**, ### **i rami seguiti PER CONTINUITA' in `k`** *(lungo `(m, 0)`: l'assegnazione che massimizza la sovrapposizione dei vettori propri
fra `k` e `k + 1`)*, ### **srotolate**; il fit per tick `sqrt(Dt^2 + vt^2 k^2) - Dt` *(`k <= 0.25 pi`)*, ### **`Delta = Dt / dtau`**.
### **La misura `2`:** `mot.cs` UNIFORME a mano *(niente `Lambda_c`)*, `dtau_nodo = dtau cs`; ### **le fasi per tick su ogni `k`, confrontate.**

Gira con:  python csv/_massa_vicino_al_cono.py
"""
import io
import json
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
_PO = os.path.join(RADICE, "primo_ordine")
for _p in (_QUI, _PO, os.path.join(_PO, "leggi")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import numpy as np                                             # noqa: E402

LATI = (32, 64)
EPS_LISTA = (0.0, 0.5)
S_LISTA = (0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.99, 1.0)
S_FIT = (0.8, 0.9, 0.95, 0.99)
COPPIE = (((0.5, 1.0), (1.0, 0.5)), ((0.25, 1.0), (0.5, 0.5)), ((0.9, 1.0), (1.0, 0.9)))
TOLL_FASI = 1e-10
TOLL_FIT = 0.05
TOLL_TAGLIE = 0.01
JSONL = os.path.join(RADICE, "doc", "referti_l2", "massa_vicino_al_cono.jsonl")
OK = [0, 0]


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    print("  %-82s %s   %s" % (che[:82], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return passa


def matrice(L, dt, eps, cs=None):
    """### `A(k)` complessa della camminata sola *(come `_stabilita_lineare.camminata_complessa`)*, con `cs` uniforme a mano."""
    import _stabilita_lineare as SL
    vero = SL.EPS_MONETA
    SL.EPS_MONETA = eps
    try:
        inc, mot, st, par = SL.scena(L, dt, SL.X)
        if cs is not None:
            mot.cs = np.full(inc.n, float(cs))
            mot.lambda_c = None
        n = inc.n
        for k in st:
            st[k][...] = 0
        A = np.empty((L, L, SL.NC, SL.NC), dtype=complex)
        for c in range(SL.NC):
            p = SL.copia(st)
            SL.perturba(p, c, 1.0)
            SL.passo(p, mot, par, False, (SL.S3,), 0.0)
            r = SL.celle(p, n)
            z = r[:, :SL.NC] + 1j * r[:, SL.NC:]
            A[:, :, :, c] = np.fft.fft2(z.reshape(L, L, SL.NC), axes=(0, 1))
    finally:
        SL.EPS_MONETA = vero
    return A


def rami_seguiti(A, L):
    """### Le fasi per tick del settore della materia lungo `(m, 0)`, i rami seguiti per continuita' e srotolati."""
    from scipy.optimize import linear_sum_assignment
    h = L // 2
    lam, V = np.linalg.eig(A[0, 0, :8, :8])
    fasi = [-np.angle(lam)]
    for m in range(1, h + 1):
        l2, V2 = np.linalg.eig(A[m % L, 0, :8, :8])
        ov = np.abs(V.conj().T @ V2)
        r, c = linear_sum_assignment(-ov)
        ordine = np.empty(8, dtype=int)
        ordine[r] = c
        l2, V2 = l2[ordine], V2[:, ordine]
        fasi.append(-np.angle(l2))
        V = V2
    return np.unwrap(np.array(fasi), axis=0)


def misura(L, dt, eps, cs=None):
    """### `Delta` e `c` in TRE unita' *(aggiunta di Luca delle `21:30`)*: per tick, per tempo coordinato *(/ `dtau`)*, per tempo
    proprio *(/ `cs dtau`)*. ### **I rami dispersivi: `|v_g|` massimo per unita' di tempo PROPRIO `> 0.1`.**"""
    import _moneta_massa as MM
    c_ = 1.0 if cs is None else float(cs)
    s = dt * c_
    A = matrice(L, dt, eps, cs)
    ph = rami_seguiti(A, L)
    kk = 2.0 * np.pi * np.arange(L // 2 + 1) / L
    vg_t = np.gradient(ph, kk, axis=0)                      # per tick
    disp = [b for b in range(8) if float(np.max(np.abs(vg_t[:, b]))) / s > 0.1]
    sel = kk <= 0.25 * np.pi + 1e-12
    fits = [MM.fit_massa(kk[sel], ph[sel, b] - ph[0, b]) for b in disp]
    k1 = kk[1]
    Dt = float(np.median([f[0] for f in fits])) if fits else float("nan")
    ct = float(np.median([abs(vg_t[1, b]) / k1 for b in disp])) if disp else float("nan")
    return {"lato": L, "dtau": dt, "cs": c_, "s": s, "eps": eps, "dispersivi": len(disp),
            "Delta_tick": Dt, "Delta_coord": Dt / dt, "Delta_proprio": Dt / s, "Delta": Dt / s,
            "c_tick": ct, "c_coord": ct / dt, "c_proprio": ct / s, "c": ct / s,
            "scarto_fit": max([f[2] for f in fits], default=float("nan")),
            "pendenza": float(np.median([abs(vg_t[1, b]) for b in disp])) / s if disp else float("nan"),
            "r21": float(np.median([abs(vg_t[2, b] / vg_t[1, b]) for b in disp if vg_t[1, b]])) if disp else float("nan")}


def misura_s(L, s, eps):
    return misura(L, s, eps)


def main(argv):
    del argv
    import _presidio
    _presidio.avvia(__file__)
    import composizione as CM
    print("=" * 100)
    print("LA MASSA DELLA CAMMINATA VICINO AL CONO: Delta(s) fra 0.5 e 1, e la prova che conta solo s")
    print("=" * 100)
    print("  il passo: %d pezzi, impronta %s (intatto); cs spento nella misura 1 (s = dtau); i rami seguiti per continuita'"
          % (len(CM.ORDINE), CM.IMPRONTA))
    print("-" * 100)
    sys.stdout.flush()
    io.open(JSONL, "w", encoding="utf-8").close()
    # ------------------------------------------------------------ MISURA 1
    print("### MISURA 1 -- Delta VICINO AL CONO")
    R = {}
    for L in LATI:
        for eps in EPS_LISTA:
            for s in S_LISTA:
                r = misura_s(L, s, eps)
                R[(L, eps, s)] = r
                print("  lato %d eps %-3g s %-5g: %d rami; Delta per tick %.6f, per tempo coordinato %.6f, per tempo proprio %.6f;"
                      " c per tick %.5f, coord. %.5f, proprio %.5f; v_g(2)/v_g(1) %.3f; fit %.3f%s"
                      % (L, eps, s, r["dispersivi"], r["Delta_tick"], r["Delta_coord"], r["Delta_proprio"], r["c_tick"],
                         r["c_coord"], r["c_proprio"], r["r21"], r["scarto_fit"],
                                                         "  ### FIT NON LEGGIBILE" if not r["scarto_fit"] <= TOLL_FIT else ""))
                sys.stdout.flush()
                with io.open(JSONL, "a", encoding="utf-8") as f:
                    f.write(json.dumps(r) + "\n")
    print("### LE LETTURE DELLA MISURA 1")
    let = {}
    for L in LATI:
        for eps in EPS_LISTA:
            D = [R[(L, eps, s)]["Delta"] for s in S_LISTA]
            leggibili = [R[(L, eps, s)]["scarto_fit"] <= TOLL_FIT for s in S_LISTA]
            mono = all(D[i + 1] <= D[i] + 1e-12 for i in range(len(D) - 1) if leggibili[i] and leggibili[i + 1])
            zero = D[-1] <= 0.01 * D[0]
            xs = [np.log(1.0 - s) for s in S_FIT if R[(L, eps, s)]["Delta"] > 0 and R[(L, eps, s)]["scarto_fit"] <= TOLL_FIT]
            ys = [np.log(R[(L, eps, s)]["Delta"]) for s in S_FIT if R[(L, eps, s)]["Delta"] > 0
                  and R[(L, eps, s)]["scarto_fit"] <= TOLL_FIT]
            p = float(np.polyfit(xs, ys, 1)[0]) if len(xs) >= 2 else float("nan")
            v = "LA MASSA SI SPEGNE AL CONO" if (mono and zero) else "NON si spegne (o non si legge)"
            print("  lato %d eps %g: Delta %s; monotono? %s; a s = 1 %.2e (<= 1%% di s 0.5? %s); p (fit fra 0.8 e 0.99, %d punti)"
                  " = %.3f (previsto 1) -> ### %s" % (L, eps, ["%.4f" % x for x in D], mono, D[-1], zero, len(xs), p, v))
            let[(L, eps)] = {"Delta": D, "monotono": bool(mono), "zero": bool(zero), "p": p, "verdetto": v}
    for eps in EPS_LISTA:
        a, b = let[(32, eps)]["p"], let[(64, eps)]["p"]
        print("  eps %g: p a lato 32 %.4f, a lato 64 %.4f -> entro 1%%? %s" % (eps, a, b, abs(b - a) <= TOLL_TAGLIE * abs(a)))
    print("-" * 100)
    # ------------------------------------------------------------ MISURA 2
    print("### MISURA 2 -- CONTA SOLO s? (cs uniforme a mano); e LA MASSA INVARIANTE LOCALMENTE? (aggiunta di Luca, 21:30)")
    tutte = True
    invariante = True
    m2 = []
    for L in LATI:
        for eps in EPS_LISTA:
            for (d1, c1), (d2, c2) in COPPIE:
                f1 = np.sort(-np.angle(np.linalg.eigvals(matrice(L, d1, eps, c1))), axis=-1)
                f2 = np.sort(-np.angle(np.linalg.eigvals(matrice(L, d2, eps, c2))), axis=-1)
                dmax = float(np.max(np.abs(np.angle(np.exp(1j * (f1 - f2))))))
                ok = dmax <= TOLL_FASI
                tutte &= ok
                esito("lato %d eps %g: s %g da (dtau %g, cs %g) e da (dtau %g, cs %g): le fasi per tick" % (
                    L, eps, d1 * c1, d1, c1, d2, c2), ok, "%.3e" % dmax)
                a, b = misura(L, d1, eps, c1), misura(L, d2, eps, c2)
                inv = abs(b["Delta_proprio"] - a["Delta_proprio"]) <= 0.01 * abs(a["Delta_proprio"])
                invariante &= inv
                print("      Delta per tick %.6f / %.6f; per tempo coordinato %.6f / %.6f; per tempo PROPRIO %.6f / %.6f -> %s"
                      % (a["Delta_tick"], b["Delta_tick"], a["Delta_coord"], b["Delta_coord"], a["Delta_proprio"],
                         b["Delta_proprio"], "INVARIANTE (entro 1%)" if inv else "### DIPENDE DAL POSTO"))
                print("      c per tick %.5f / %.5f; coordinato %.5f / %.5f; proprio %.5f / %.5f"
                      % (a["c_tick"], b["c_tick"], a["c_coord"], b["c_coord"], a["c_proprio"], b["c_proprio"]))
                sys.stdout.flush()
                m2.append({"lato": L, "eps": eps, "coppia": [[d1, c1], [d2, c2]], "scarto": dmax, "a": a, "b": b,
                           "invariante": bool(inv)})
    print("  ### CONTA SOLO s? %s" % ("SI': la massa dipende da cs attraverso s" if tutte else "NO"))
    print("  ### MASSA INVARIANTE LOCALMENTE? %s" % ("SI': Delta per tempo proprio uguale nelle due meta' di ogni coppia"
                                                 if invariante else "NO: la massa dipende dal posto anche per l'osservatore locale"
                                                 " (il principio di equivalenza e' in gioco)"))
    with io.open(JSONL, "a", encoding="utf-8") as f:
        f.write(json.dumps({"letture_1": {"%d %g" % k: v for k, v in let.items()}, "misura_2": m2,
                            "conta_solo_s": bool(tutte),
                            "invariante_localmente": bool(invariante)}) + "\n")
    print("=" * 100)
    print("LA MASSA VICINO AL CONO: %d su %d controlli (la misura 2)   %s" % (OK[0], OK[1], "### TUTTI PASSATI"
                                                                           if OK[0] == OK[1] else "### CI SONO BUCHI"))
    print("=" * 100)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
