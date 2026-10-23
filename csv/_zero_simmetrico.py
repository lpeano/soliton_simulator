r"""**LO ZERO SIMMETRICO IN MEMORIA: la forza, Einstein e l'universalita' coi pezzi parziali a generatore simmetrico** *(nessun cambiamento del nucleo)*.

> ### ⛔ **Il task history e' `2026-10-23_zero_simmetrico.md`** *(le verifiche, le previsioni, il metodo, i criteri, fissati prima)*. ### **La convenzione simmetrica SOLO in memoria:**
> ### **il pezzo di oggi a meta' frazione, poi quello di `_gravita_collettiva.convenzione_alternativa()` a meta' frazione** *(`exp(-i theta P/2) exp(i theta (I - P)/2) = exp(i theta (I - 2P)/2)`)*.
> ### **`leggi.yaml`, l'impronta e il nucleo intatti.** ### **Importati, non copiati:** `_forza_da_cs`, `_scala_e_zero`, `_gravita_collettiva`, `_massa_vicino_al_cono`, `_universalita_massa`.

### **(ii)** `A_simm = e^{-i pi s} A_oggi`. ### **PARTE A:** ### **`omega(0)` continua, `omega''`, `v`, `D`, `Q` nelle due convenzioni.** ### **PARTE B:** ### **la forza** *(Hamilton e
il pacchetto di `_forza_da_cs.corsa`)* ### **nelle due convenzioni**, ### **la dinamica a `eta = 0` e nel gradiente.** ### **PARTE C:** ### **`Vi` di `E0` e `M`, e `Q` per specie.**

Gira con:  python csv/_zero_simmetrico.py > doc/referti_l2/zero_simmetrico.txt
"""
import contextlib
import io
import json
import os
import sys
import warnings

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
_PO = os.path.join(RADICE, "primo_ordine")
for _p in (_QUI, _PO, os.path.join(_PO, "leggi")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import numpy as np                                             # noqa: E402

S_A = (0.3, 0.5, 0.7, 0.9, 0.95)
EPS_A = (0.0, 0.25, 0.5, 1.0)
S0_B = (0.3, 0.5, 0.9)
EPS_B = (0.0, 0.5)
ETA_CORSA = (0.0, 5e-4, 1e-3, -1e-3, 5e-3, 1e-2, -1e-2)
ETA_MODULI = (5e-4, 1e-3, 5e-3, 1e-2)
ETA_LETTI = (1e-3, 1e-2)
LX = (128, 256)
L_A = 64
TOLL_SERV = 1e-12
TOLL_LIN = 0.05
TICK_DIN = 100
CONV = ("oggi", "simm")
J_FORZA = os.path.join(RADICE, "doc", "referti_l2", "forza_da_cs.jsonl")
JSONL = os.path.join(RADICE, "doc", "referti_l2", "zero_simmetrico.jsonl")
OK = [0, 0]


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    print("  %-82s %s   %s" % (che[:82], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return passa


def scrivi(r):
    with io.open(JSONL, "a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(r) + "\n")


def f_(x, fm="%+.4e"):
    return "--" if x is None else fm % x


@contextlib.contextmanager
def convenzione_simmetrica():
    """### **`exp(i theta (I - 2P)/2)`** per ogni pezzo parziale: ### **il pezzo di oggi a `f/2`, poi quello dell'ALTERNATIVA a `f/2`** *(le funzioni prese dentro
    `convenzione_alternativa()`, il suo meccanismo)*."""
    import _gravita_collettiva as GC
    import flussi_parziali as FP
    g0, hp0, hf0 = FP.grover, FP.hop_psi, FP.hop_phi
    with GC.convenzione_alternativa():
        ga, hpa, hfa = FP.grover, FP.hop_psi, FP.hop_phi

    def comp(oggi, alt):
        def f(mot, x, frazione):
            oggi(mot, x, 0.5 * frazione)
            return alt(mot, x, 0.5 * frazione)
        return f
    FP.grover, FP.hop_psi, FP.hop_phi = comp(g0, ga), comp(hp0, hpa), comp(hf0, hfa)
    try:
        yield
    finally:
        FP.grover, FP.hop_psi, FP.hop_phi = g0, hp0, hf0


def conv(nome):
    return convenzione_simmetrica() if nome == "simm" else contextlib.nullcontext()


def nome_curv(rg):
    return "curv %s Dt %.4f" % ("+" if rg["segno"] > 0 else "-", rg["Dt"])


# =====================================================================================
#   (ii) IL CONTROLLO DI SERVIZIO
# =====================================================================================
def servizio_ii():
    import _massa_vicino_al_cono as MV
    peg = 0.0
    for eps in EPS_A:
        for s in S_A + (1.0,):
            A = MV.matrice(16, 1.0, eps, s)
            with convenzione_simmetrica():
                B = MV.matrice(16, 1.0, eps, s)
            peg = max(peg, float(np.abs(B - np.exp(-1j * np.pi * s) * A).max()))
    return peg


# =====================================================================================
#   PARTE A E C -- I RAMI NELLE DUE CONVENZIONI
# =====================================================================================
def righe_rami(nome, eps):
    """### Ogni ramo a ogni `s` di `_scala_e_zero.S_LISTA` *(lato `64`)*: la fase continua, `omega''`, `v`, `E0`, `M`, `D`, `Q`."""
    import _gravita_collettiva as GC
    import _scala_e_zero as Z
    out = []
    with conv(nome):
        C, salto = Z.cammino(eps)
        for s in Z.S_LISTA:
            lista, ph, _A = Z.rami_a(L_A, s, eps)
            for g in GC.gruppi(lista):
                b = [r for r in lista if abs(r["omega0"] - g["omega0"]) <= GC.TOLL_DISTINTI and r["omega1"] in g["omega1"]][0]["ramo"]
                w2 = Z.curvatura(ph, b, L_A)
                lv = Z.livelli(C, s, g["omega0"])
                wc = sorted({round(float(Z.a_(C[0], s)["w"][i]), 9) for i in lv})
                lvl = min(lv) if lv else None
                if lvl is not None:
                    w3 = [float(Z.a_(C[0], x)["w"][lvl]) for x in (s * (1 - Z.H), s, s * (1 + Z.H))]
                    D = GC.dproprio(w3[0], w3[1], w3[2], s * (1 - Z.H), s, s * (1 + Z.H))
                    w_c = w3[1]
                else:
                    D = w_c = None
                rec = {"tipo": "ramo", "convenzione": nome, "eps": eps, "s": s, "ramo": "curv %s Dt %.4f" % ("+" if w2 > 0 else "-", g["Dt"]),
                       "Dt": g["Dt"], "v": g["v"], "omega0_principale": g["omega0"], "omega0_continua": w_c, "ambiguo": len(wc) != 1, "livello": lvl,
                       "omega2": w2, "E0": None if w_c is None else w_c / s, "M": w2 / s, "D": D,
                       "Q": None if w_c is None else w_c * w2 / g["v"] ** 2, "Q_principale": g["omega0"] * w2 / g["v"] ** 2}
                out.append(rec)
                scrivi(rec)
    return out, salto


# =====================================================================================
#   PARTE B -- LA FORZA
# =====================================================================================
def previsione(nome, eps, s0, rg):
    """### `a_H` e `a_RG` di `557d94d6` *(le stesse formule: `a_H = -omega'' (d omega0/ds) ds/dx`, `a_RG = -v^2 (ds/dx)/s0`)*, coi due spettri `s0 (1 +- eta)`."""
    import _forza_da_cs as F
    out = {}
    with conv(nome):
        for eta in ETA_MODULI:
            sm, sp = s0 * (1.0 - eta), s0 * (1.0 + eta)
            # ### nella simmetrica `omega(0)` e' spostata di `pi s`: ### **il ramo si segue col suo `omega(0)` SPOSTATO**, altrimenti fra i due rami di `eps 0`
            # ### *(lo stesso `Dt`)* `segui` prenderebbe l'altro
            sh = (lambda x: np.pi * x) if nome == "simm" else (lambda x: 0.0)
            rm = F.segui(F.rami(sm, eps)[0], dict(rg, omega0=F.avvolgi(rg["omega0"] + sh(sm))))
            rp = F.segui(F.rami(sp, eps)[0], dict(rg, omega0=F.avvolgi(rg["omega0"] + sh(sp))))
            dw = F.avvolgi(rp["omega0"] - rm["omega0"]) / (sp - sm)
            w2 = rg["segno"] * rg["v"] ** 2 / rg["Dt"]
            for Lx in LX:
                dsdx = -s0 * eta * 2.0 * np.pi / Lx
                out[(eta, Lx)] = {"d_omega0_ds": float(dw), "a_H": float(-w2 * dw * dsdx), "a_RG": float(-rg["v"] ** 2 * dsdx / s0)}
    return out


def evolvi(nome, Lx, eps, s0, eta, Q, tick):
    """### La scena di `_forza_da_cs.corsa` *(lo stesso toro, lo stesso profilo, lo stesso pacchetto)* evoluta per `tick`: ### **`|psi|^2` e `|phi|^2` alla fine.**"""
    import _forza_da_cs as F
    import _stabilita_lineare as SL
    import scena_l2 as SC
    import statica_protocollo as PR
    with conv(nome):
        inc, mot, st, par, _c, _p = SC.scena(1.0, PR.VUOTO, 0.0, PR.RAGGIO, False, True, False, PR.SEME, 1, lati=(Lx, F.LY))
        par["eps"] = float(eps)
        x = (np.arange(inc.n) // F.LY).astype(float)
        mot.cs = s0 * (1.0 + eta * np.cos(2.0 * np.pi * x / Lx))
        mot.lambda_c = None
        for k in st:
            st[k][...] = 0
        G = np.exp(-(x - Lx / 4.0) ** 2 / (2.0 * (Lx / 16.0) ** 2))
        cel = G[:, None] * Q[:, 0][None, :]
        cel /= np.sqrt(np.sum(np.abs(cel) ** 2))
        st["psi_h"][...] = cel.reshape(st["psi_h"].shape)
        for _t in range(tick):
            SL.passo(st, mot, par, False, (SL.S3,), 0.0)
    return np.abs(st["psi_h"]) ** 2, np.abs(st["phi_h"]) ** 2


def parte_B():
    import _forza_da_cs as F
    print("### PARTE B -- LA FORZA nelle due convenzioni (s0 %s, eta %s, eps %s, Lx %s; la corsa di _forza_da_cs)" % (S0_B, ETA_CORSA, EPS_B, LX))
    tab, M, vett = [], {}, {}
    for eps in EPS_B:
        c0 = F.catena_principale(eps)
        for s0 in S0_B:
            lista0, BB0, _ = F.rami(s0, eps)
            for rg in F.righe_del_ramo(lista0, F.bersaglio(c0, s0)):
                Q = F.spazio_del_ramo(BB0, rg)[0]
                nr = nome_curv(rg)
                vett[(eps, s0, nr)] = Q
                for nome in CONV:
                    prev = previsione(nome, eps, s0, rg)
                    for Lx in LX:
                        for eta in ETA_CORSA:
                            with conv(nome):
                                r = F.corsa(Lx, eps, s0, eta, Q)
                            r.update(convenzione=nome, ramo=nr, nome_forza=rg["nome"])
                            M[(nome, eps, s0, nr, Lx, eta)] = r
                            scrivi(dict(r, tipo="corsa"))
                    for Lx in LX:
                        for eta in ETA_LETTI:
                            r, h = M[(nome, eps, s0, nr, Lx, eta)], M[(nome, eps, s0, nr, Lx, eta / 2.0)]
                            lin = r["a"] / h["a"] if r["a"] is not None and h["a"] else None
                            lin_ok = lin is not None and abs(lin / 2.0 - 1.0) < TOLL_LIN
                            p = prev[(eta, Lx)]
                            a = r["a"]
                            rec = {"tipo": "forza", "convenzione": nome, "eps": eps, "s0": s0, "ramo": nr, "nome_forza": rg["nome"], "Lx": Lx, "eta": eta,
                                   "a_mis": a, "sigma_a": r["sigma_a"], "a_H": p["a_H"], "a_RG": p["a_RG"], "d_omega0_ds": p["d_omega0_ds"],
                                   "mis_su_RG": None if a is None else a / p["a_RG"], "mis_su_H": None if a is None or p["a_H"] == 0 else a / p["a_H"],
                                   "H_su_RG": p["a_H"] / p["a_RG"], "lin": lin, "leggibile": bool(r["leggibile"] and lin_ok)}
                            tab.append(rec)
                            scrivi(rec)
                            print("  %-4s eps %-3g s0 %-4g %-18s Lx %d eta %-5g: a %s (+- %s) | a/a_RG %s  a/a_H %s  a_H/a_RG %s | lin %s | %s%s"
                                  % (nome, eps, s0, nr, Lx, eta, f_(a), f_(r["sigma_a"], "%.1e"), f_(rec["mis_su_RG"], "%+.3f"), f_(rec["mis_su_H"], "%+.3f"),
                                     f_(rec["H_su_RG"], "%+.3f"), f_(lin, "%.3f"),
                                     "--" if a is None else ("verso cs BASSO" if rec["mis_su_RG"] > 0 else "verso cs ALTO"), "" if rec["leggibile"] else "  ### NON SI LEGGE"))
                            sys.stdout.flush()
    return tab, M, vett


def main(argv):
    del argv
    import _forza_da_cs as F
    import _presidio
    import _scala_e_zero as Z
    import _universalita_massa as UM
    import composizione as CM
    _presidio.avvia(__file__)
    print("=" * 100)
    print("LO ZERO SIMMETRICO IN MEMORIA: la forza, Einstein e l'universalita' coi pezzi parziali a generatore simmetrico")
    print("=" * 100)
    blobs = {r: UM.blob(r) for r in ("soliton_simulator.py", "csv/_massa_vicino_al_cono.py", "csv/_universalita_massa.py", "csv/_forza_da_cs.py", "csv/_stabilita_lineare.py",
                                     "csv/_gravita_collettiva.py", "csv/_scala_e_zero.py", "csv/_zero_simmetrico.py", "doc/referti_l2/forza_da_cs.jsonl")}
    print("  il passo: %d pezzi, impronta %s (intatto); la convenzione simmetrica SOLO in memoria; i blob nel repo: %s"
          % (len(CM.ORDINE), CM.IMPRONTA, "; ".join("%s %s" % (k, v["sha1-BYTE"]) for k, v in blobs.items())))
    print("  la configurazione: S_A %s; EPS_A %s; S0_B %s; EPS_B %s; ETA %s; LX %s; L_A %d; TOLL_SERV %g; TOLL_LIN %g; TICK_DIN %d; Z.S_LISTA %s"
          % (S_A, EPS_A, S0_B, EPS_B, ETA_CORSA, LX, L_A, TOLL_SERV, TOLL_LIN, TICK_DIN, Z.S_LISTA))
    print("-" * 100)
    sys.stdout.flush()
    io.open(JSONL, "w", encoding="utf-8").close()
    scrivi({"tipo": "testata", "blobs": blobs})
    warnings.simplefilter("ignore")
    # ---------------------------------------------------------------- (ii)
    peg = servizio_ii()
    esito("DEVE PASSARE (ii): A_simm = e^{-i pi s} A_oggi, la matrice intera a ogni k, s %s e 1, eps %s" % (S_A, EPS_A), peg < TOLL_SERV, "il peggiore %.2e" % peg)
    # ---------------------------------------------------------------- A e C
    print("### PARTE A -- I RAMI NELLE DUE CONVENZIONI (lato %d; la fase continua da s 0.02)" % L_A)
    righe = []
    for nome in CONV:
        for eps in EPS_A:
            rr, salto = righe_rami(nome, eps)
            righe += rr
            print("  [%s eps %g: il salto massimo sul cammino fine %.2e]" % (nome, eps, salto))
    for eps in EPS_A:
        for s in S_A:
            for nome in CONV:
                for r in [x for x in righe if x["convenzione"] == nome and x["eps"] == eps and x["s"] == s]:
                    print("  %-4s eps %-4g s %-4g %-18s: w0 princ %+.6f cont %s | w'' %+.5f v %.5f | E0 %s M %+.4f D %s | Q %s (princ %+.4f)%s"
                          % (nome, eps, s, r["ramo"], r["omega0_principale"], f_(r["omega0_continua"], "%+.6f"), r["omega2"], r["v"], f_(r["E0"], "%+.5f"),
                             r["M"], f_(r["D"], "%+.3e"), f_(r["Q"], "%+.4f"), r["Q_principale"], " AMBIGUO" if r["ambiguo"] else ""))
    sys.stdout.flush()
    # ---------------------------------------------------------------- C
    print("### PARTE C -- L'UNIVERSALITA' nella convenzione simmetrica: Vi di E0 e di M fra specie seguite da s 0.02, e Q per specie")
    spec = {}
    for r in righe:
        if r["convenzione"] == "simm" and r["livello"] is not None:
            spec.setdefault((r["eps"], r["livello"]), {})[r["s"]] = r
    spec = {k: v for k, v in spec.items() if Z.S_RIF in v}
    for k, v in sorted(spec.items()):
        print("  specie (eps %g, liv %d, %s): Q(s) %s" % (k[0], k[1], v[Z.S_RIF]["ramo"], " ".join("%g:%s" % (s, f_(v[s]["Q"], "%+.3f")) for s in sorted(v))))
        scrivi({"tipo": "Q_specie", "eps": k[0], "livello": k[1], "Q": {str(s): v[s]["Q"] for s in sorted(v)}})
    ch = sorted(spec)
    for a in range(len(ch)):
        for b in range(a + 1, len(ch)):
            i, j = spec[ch[a]], spec[ch[b]]
            for gr in ("E0", "M"):
                if i[Z.S_RIF][gr] is None or j[Z.S_RIF][gr] is None or abs(j[Z.S_RIF][gr]) <= Z.TOLL_ZERO:
                    continue
                R0 = i[Z.S_RIF][gr] / j[Z.S_RIF][gr]
                if abs(R0) <= Z.TOLL_ZERO:
                    continue
                vv = {s: abs(i[s][gr] / j[s][gr] - R0) / abs(R0) for s in Z.S_LISTA if s in i and s in j and i[s][gr] is not None and abs(j[s][gr] or 0) > Z.TOLL_ZERO}
                p = Z.esponente(vv)
                scrivi({"tipo": "universalita", "convenzione": "simm", "i": list(ch[a]), "j": list(ch[b]), "grandezza": gr, "R0": R0, "Vi": {str(s): x for s, x in vv.items()}, "esponente": p})
                print("  (eps %g, liv %d) / (eps %g, liv %d) %-2s: R0 %+.5f | Vi %s | esponente %s"
                      % (ch[a][0], ch[a][1], ch[b][0], ch[b][1], gr, R0, " ".join("%g:%.2e" % (s, x) for s, x in vv.items()), f_(p, "%.3f")))
    # ---------------------------------------------------------------- B
    tab, M, vett = parte_B()
    # il servizio: oggi a s0 0.9 contro 557d94d6
    assert F.committata(J_FORZA), "il jsonl di 557d94d6 non e' committato e pulito"
    vecchi = {(r["Lx"], r["eps"], r["s0"], r["eta"], r["ramo"]): r for r in (json.loads(l) for l in io.open(J_FORZA, encoding="utf-8")) if r.get("tipo") == "corsa"}
    peg, n = 0.0, 0
    for (nome, eps, s0, nr, Lx, eta), r in M.items():
        v = vecchi.get((Lx, eps, s0, eta, r["nome_forza"]))
        if nome == "oggi" and v is not None and r["a"] is not None and v["a"] is not None:
            n += 1
            peg = max(peg, abs(r["a"] - v["a"]) / max(abs(v["a"]), 1e-300))
    esito("DI SERVIZIO: la convenzione di oggi rifatta a s0 0.9 = 557d94d6, entro 1e-12 relativo, su %d corse" % n, n > 0 and peg < 1e-12, "il peggiore %.2e" % peg)
    # la dinamica
    chiavi = [k for k in vett if k[0] == 0.5 and k[1] == 0.5] or sorted(vett)
    Q = vett[chiavi[0]]
    print("### LA DINAMICA a eta 0 e 1e-2: il pacchetto di %s, Lx 128, %d tick" % (chiavi[0], TICK_DIN))
    d = {}
    for eta in (0.0, 1e-2):
        p0, f0 = evolvi("oggi", 128, 0.5, 0.5, eta, Q, TICK_DIN)
        p1, f1 = evolvi("simm", 128, 0.5, 0.5, eta, Q, TICK_DIN)
        d[eta] = max(float(np.abs(p1 - p0).max()) / float(p0.max()), float(np.abs(f1 - f0).max()) / max(float(f0.max()), 1e-300) if f0.max() > 0 else float(np.abs(f1 - f0).max()))
        scrivi({"tipo": "dinamica", "eta": eta, "tick": TICK_DIN, "scarto": d[eta]})
    esito("DEVE PASSARE: eta = 0, |psi|^2 e |phi|^2 al tick %d uguali nelle due convenzioni entro 1e-12 (Lx 128, s0 0.5, eps 0.5)" % TICK_DIN, d[0.0] < 1e-12, "%.2e" % d[0.0])
    esito("DEVE FALLIRE: <<la dinamica a eta 1e-2 e' uguale a quella di oggi>> (per la chiave giusta: lo scarto finito)", np.isfinite(d[1e-2]) and not d[1e-2] < 1e-12,
          "lo scarto %.4e" % d[1e-2])
    q = [r for r in tab if r["convenzione"] == "simm" and r["eps"] == 0.0 and r["s0"] == 0.3 and r["leggibile"]]
    esito("PUO' FALLIRE: eps 0, s0 0.3, i due rami con a_mis/a_RG > 0 e entro il 20%% di 1 (simmetrica, %d righe leggibili)" % len(q),
          len(q) > 0 and len({r["ramo"] for r in q}) == 2 and all(r["mis_su_RG"] > 0 and abs(r["mis_su_RG"] - 1.0) < 0.2 for r in q),
          "; ".join("%s Lx %d eta %g: %+.3f" % (r["ramo"], r["Lx"], r["eta"], r["mis_su_RG"]) for r in q))
    print("=" * 100)
    print("LO ZERO SIMMETRICO: %d su %d controlli   %s  (il verdetto di fisica sono le tabelle)" % (OK[0], OK[1], "### TUTTI PASSATI" if OK[0] == OK[1] else "### CI SONO BUCHI"))
    print("=" * 100)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
