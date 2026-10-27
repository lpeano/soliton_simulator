# -*- coding: utf-8 -*-
r"""**LA SCOMPOSIZIONE DELL'ENERGIA A RIPOSO A UNO ZERO `lambda` GENERICO** *(il mandato breve del 2026-10-27, 08:59, parte 1; [[SCOMPOSIZIONE-SOLITONE]], [[SOLITONE-VUOTO-CONGELATO]])*: ### **lo stesso solitone e la
stessa scomposizione di `dc4a1437`, con la famiglia di convenzioni `exp(i theta (lambda I - P))`** *(`0` oggi, `1/2` il simmetrico, `1` l'alternativa)*; ### **lo spostamento dell'energia MISURATO dalla rotazione.**

> ### ⛔ **Il task history e' `2026-10-27_scomposizione_zero_lambda.md`.** ### **In memoria; nessun file del nucleo.**
> ### **Importati, non copiati:** `_scomposizione_solitone` *(`scena`, `stato_solitone`, `stato_uniforme`, `parti`, `misure`)*, `_solitone_vuoto_congelato`, `_solitoni_triangoli`, `_modi_pi_e_solitoni.largo`,
> `_screening_forme_s3.forma`, `_zero_simmetrico.convenzione_simmetrica`, `_gravita_collettiva.convenzione_alternativa`, `tick.percorri_tick`. ### **Il `rec` del solitone ripete le righe di `_scomposizione_solitone.main`.**

Gira con:  python csv/_scomposizione_zero_lambda.py > doc/referti_l2/scomposizione_zero_lambda.txt
"""
import contextlib
import io
import json
import math
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
_PO = os.path.join(RADICE, "primo_ordine")
for _p in (_QUI, _PO, os.path.join(_PO, "leggi")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import numpy as np                                             # noqa: E402

LAMBDE = tuple(round(0.1 * i, 10) for i in range(11)) + (0.25, 0.75)
L_DINAMICA = 0.5
TOLL_RIF = 1e-4
TOLL_SPOST = 1e-9
TOLL_LIN = 1e-6
TOLL_NORMA = 1e-10
TOLL_CONV = 0.01
RIF = os.path.join(RADICE, "doc", "referti_l2", "scomposizione_solitone.jsonl")
JSONL = os.path.join(RADICE, "doc", "referti_l2", "scomposizione_zero_lambda.jsonl")
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


@contextlib.contextmanager
def convenzione(lam):
    """### **`exp(i theta (lambda I - P))`** per ogni pezzo parziale: ### **il pezzo di oggi a `(1 - lambda) f`, poi quello dell'ALTERNATIVA a `lambda f`** *(il meccanismo di
    `_zero_simmetrico.convenzione_simmetrica`, coi pesi)*; ### **a `lambda = 0` solo oggi, a `1` solo l'alternativa.**"""
    import _gravita_collettiva as GC
    import flussi_parziali as FP
    g0, hp0, hf0 = FP.grover, FP.hop_psi, FP.hop_phi
    with GC.convenzione_alternativa():
        ga, hpa, hfa = FP.grover, FP.hop_psi, FP.hop_phi
    if lam == 0.0:
        yield
        return

    def comp(oggi, alt):
        if lam == 1.0:
            return alt

        def f(mot, x, frazione):
            oggi(mot, x, (1.0 - lam) * frazione)
            return alt(mot, x, lam * frazione)
        return f
    FP.grover, FP.hop_psi, FP.hop_phi = comp(g0, ga), comp(hp0, hpa), comp(hf0, hfa)
    try:
        yield
    finally:
        FP.grover, FP.hop_psi, FP.hop_phi = g0, hp0, hf0


def un_tick(st, mot, par, salta, conv):
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import composizione as CM
    import tick as TK
    with SF.forma(VC.FORMA), conv:
        TK.percorri_tick(st, mot, par, salta, None, len(CM.ORDINE))


def rotazione(L, Q, m1, m2, lam, campo):
    """### **`(<x|T_lambda x>, 1 - |<x|T x>|/|x|^2)`:** ### **lo stato uniforme del ramo** *(`campo` `psi`, il vuoto uniforme congelato: i pezzi del vuoto saltati)* ### **o il vuoto uniforme** *(`phi`, la materia a zero)*."""
    import _scomposizione_solitone as SC
    import _solitone_vuoto_congelato as VC
    import scena_l2 as SL
    inc, mot, st = SC.stato_uniforme(L, Q, m1, m2)
    _i, _m, _s, par = SC.scena(L)
    # ### il vuoto uniforme in tutti e due i casi: con `Lambda = 0` la forma `S1` divide per zero; ### per `psi` i pezzi del vuoto sono saltati, ### e il legame da' la STESSA fase a ogni `lambda` (si cancella nella differenza)
    st["phi_h"][...] = SL.VUOTO_PER_ESTREMITA
    if campo == "phi":
        st["psi_h"][...] = 0.0
    chiave = campo + "_h"
    x0 = st[chiave].copy()
    un_tick(st, mot, par, VC.VUOTO if campo == "psi" else (), convenzione(lam))
    ov = complex(np.vdot(x0.ravel(), st[chiave].ravel()))
    nn = float(np.sum(np.abs(x0) ** 2))
    return ov, 1.0 - abs(ov) / nn


def main(argv):
    del argv
    import _presidio
    import _universalita_massa as UM
    import _modi_pi_e_solitoni as MPS
    import _scomposizione_solitone as SC
    import _screening_forme_s3 as SF
    import _solitoni_triangoli as STR
    import _solitone_vuoto_congelato as VC
    import _zero_simmetrico as ZS
    import composizione as CM
    import tick as TK
    _presidio.avvia(__file__)
    print("=" * 130)
    print("LA SCOMPOSIZIONE DELL'ENERGIA A RIPOSO A UNO ZERO lambda GENERICO: S1, N 1e6, il vuoto congelato; la famiglia exp(i theta (lambda I - P)), lo spostamento misurato dalla rotazione")
    print("=" * 130)
    blobs = {p: UM.blob(p) for p in ("soliton_simulator.py", "csv/_scomposizione_zero_lambda.py", "csv/_scomposizione_solitone.py", "csv/_solitone_vuoto_congelato.py", "csv/_zero_simmetrico.py",
                                     "csv/_gravita_collettiva.py", "primo_ordine/energia_pesata.py", "doc/referti_l2/scomposizione_solitone.jsonl")}
    print("  il passo: %d pezzi, impronta %s (intatto); i blob nel repo: %s" % (len(CM.ORDINE), CM.IMPRONTA, "; ".join("%s %s" % (k, v["sha1-BYTE"]) for k, v in blobs.items())))
    print("  la configurazione: LAMBDE %s L_DINAMICA %g TOLL_RIF %g TOLL_SPOST %g TOLL_LIN %g TOLL_NORMA %g TOLL_CONV %g; da _scomposizione_solitone: N_SOL %g FATTORI %s T_FROZEN %d; da _solitone_vuoto_congelato: FORMA %s S %g VUOTO %s"
          % (LAMBDE, L_DINAMICA, TOLL_RIF, TOLL_SPOST, TOLL_LIN, TOLL_NORMA, TOLL_CONV, SC.N_SOL, SC.FATTORI, SC.T_FROZEN, VC.FORMA, VC.S, VC.VUOTO))
    print("  il legame: Lambda F_1(rho/Lambda), F_1(x) = x - arctan x (S1; _scomposizione_solitone.parti); E_mat col vuoto a zero (l'N S3 di termini_di_h li' vale 0)")
    print("  lo spostamento: Delta e(lambda) = -[arg <x|T_lambda x> - arg <x|T_0 x>] / s sullo stato uniforme (la fase per tick e' -s E: la rotazione di 74f99039 e' -arg); E_mat(lambda) = E_mat(0) + M Delta e; del vuoto (fuori da E0) solo Delta e_vuoto, crudo: la relazione fase-energia del vuoto non e' verificata qui")
    print("-" * 130)
    io.open(JSONL, "w", encoding="utf-8").close()
    scrivi({"tipo": "testata", "blobs": blobs, "impronta": CM.IMPRONTA})
    rif = {}
    for l in io.open(RIF, encoding="utf-8"):
        d = json.loads(l)
        if d.get("tipo") == "scomposizione":
            rif[d["L"]] = d
    vero = MPS.LAM0
    MPS.LAM0 = STR.LAM0_TRI
    try:
        c, _cy, _w0k = STR.c_triangoli(VC.S)
        q = MPS.largo(VC.FORMA, c, VC.S, SC.N_SOL)
    finally:
        MPS.LAM0 = vero
    rec = {"larghezza": q["larghezza"], "c": c, "mu": q["mu"]}
    tq = "t%d" % SC.T_FROZEN
    ris, ok1, n1, ok2, ok3, n3, ok4, n4, ok5, n5 = [], True, [], True, True, [], True, [], True, []
    for fat in SC.FATTORI:
        L = int(3 * math.ceil(fat * rec["larghezza"] / 3.0))
        # ### (2) la famiglia contro oggi e contro convenzione_simmetrica, un tick sullo stato del solitone
        prove = {}
        for nome, cv in (("0", convenzione(0.0)), ("oggi", contextlib.nullcontext()), ("1/2", convenzione(0.5)), ("simm", ZS.convenzione_simmetrica())):
            inc, mot, st, par, pos, Q, m1, m2 = SC.stato_solitone(L, rec)
            un_tick(st, mot, par, VC.VUOTO, cv)
            prove[nome] = st["psi_h"].tobytes()
        b2 = prove["0"] == prove["oggi"] and prove["1/2"] == prove["simm"]
        ok2 &= b2
        print("  L %3d: la famiglia a lambda 0 = il tick di oggi al bit %s; a lambda 1/2 = convenzione_simmetrica al bit %s" % (L, prove["0"] == prove["oggi"], prove["1/2"] == prove["simm"]))
        # ### (3) lo spostamento misurato
        ov0, eig0 = rotazione(L, Q, m1, m2, 0.0, "psi")
        vv0, _ev0 = rotazione(L, Q, m1, m2, 0.0, "phi")
        spost, spost_v = {}, {}
        for lam in LAMBDE:
            ov, eig = rotazione(L, Q, m1, m2, lam, "psi")
            vv, _ev = rotazione(L, Q, m1, m2, lam, "phi")
            de = -float(np.angle(ov / ov0)) / VC.S
            spost[lam] = de
            spost_v[lam] = -float(np.angle(vv / vv0)) / VC.S
            ok3 &= abs(de - 2 * math.pi * lam) <= TOLL_SPOST and eig <= TOLL_SPOST
            n3.append(max(abs(de - 2 * math.pi * lam), eig))
            print("  L %3d lambda %.2f: Delta e %+.12f (2 pi lambda %+.12f, scarto %.1e); il vuoto (crudo) %+.12f; autostato 1-|<x|Tx>| %.1e; la rotazione per tick %+.9f"
                  % (L, lam, de, 2 * math.pi * lam, de - 2 * math.pi * lam, spost_v[lam], eig, float(np.angle(ov))))
            sys.stdout.flush()
        # ### le energie: lo stato a t 0, e dopo T_FROZEN tick col vuoto congelato a lambda 0 e a L_DINAMICA
        incu, motu, stu = SC.stato_uniforme(L, Q, m1, m2)
        Eu, _ev, _el, Mu, _lu = SC.parti(incu, motu, stu)
        e_K0 = Eu / Mu
        print("  L %3d: e_K(0) %+.6f per unita' di norma; -arg <x|T x> / s dello stato uniforme %+.6f (la lettura: H e' il generatore al primo ordine)" % (L, e_K0, -float(np.angle(ov0)) / VC.S))
        stati = {}
        for lam_d in (0.0, L_DINAMICA):
            inc, mot, st, par, pos, Q, m1, m2 = SC.stato_solitone(L, rec)
            stati[(lam_d, "t0")] = SC.parti(inc, mot, st) + SC.misure(inc, st, pos, rec["larghezza"])
            phi0 = st["phi_h"].copy()
            with SF.forma(VC.FORMA), convenzione(lam_d):
                for _ in range(SC.T_FROZEN):
                    TK.percorri_tick(st, mot, par, VC.VUOTO, None, len(CM.ORDINE))
                    st["phi_h"][...] = phi0
            stati[(lam_d, tq)] = SC.parti(inc, mot, st) + SC.misure(inc, st, pos, rec["larghezza"])
            print("  L %3d: %d tick col vuoto congelato e la convenzione lambda %.2f: fatto" % (L, SC.T_FROZEN, lam_d))
            sys.stdout.flush()
        out = {"L": L, "e_K0": e_K0, "spostamento": {str(k): v for k, v in spost.items()}, "spostamento_vuoto": {str(k): v for k, v in spost_v.items()}, "righe": []}
        for quando in ("t0", tq):
            E_mat0, E_v0, E_leg, M, V, _w, _fr = stati[(0.0, quando)]
            E_cin = E_mat0 - M * e_K0
            for lam in LAMBDE:
                E_mat = E_mat0 + M * spost[lam]
                N_eK = M * (e_K0 + spost[lam])
                E0 = E_mat + E_leg
                r = {"quando": quando, "lambda": lam, "E0": E0, "N_eK": N_eK, "E_cin": E_mat - N_eK, "E_legame": E_leg, "E_vuoto_0": E_v0, "Delta_e_vuoto": spost_v[lam], "M": M, "V": V,
                     "f_costituenti": N_eK / E0, "f_cinetica": (E_mat - N_eK) / E0, "f_legame": E_leg / E0, "e_K": e_K0 + spost[lam]}
                out["righe"].append(r)
                print("  L %3d %-6s lambda %.2f: E0 %+.6e = N e_K %+.6e + cinetica %+.6e + legame %+.6e | le frazioni: costituenti %+.4f, cinetica %+.4f, legame %+.4f | e_K %+.5f"
                      % (L, quando, lam, E0, N_eK, r["E_cin"], E_leg, r["f_costituenti"], r["f_cinetica"], r["f_legame"], r["e_K"]))
            # ### (1) contro dc4a1437
            r0 = [x for x in out["righe"] if x["quando"] == quando and x["lambda"] == 0.0][0]
            d = rif.get(L)
            sc1 = max(abs(r0[f] - d[quando][f]) for f in ("f_costituenti", "f_cinetica", "f_legame")) if d and quando in d else float("inf")
            ok1 &= sc1 <= TOLL_RIF
            n1.append("L %d %s %.1e" % (L, quando, sc1))
            # ### (4) la linearita' di N e_K, e lambda dove e_K = 0 e dove E0 = 0
            la = np.array(LAMBDE)
            ne = np.array([x["N_eK"] for x in out["righe"] if x["quando"] == quando])
            e0 = np.array([x["E0"] for x in out["righe"] if x["quando"] == quando])
            pf = np.polyfit(la, ne, 1)
            res = float(np.max(np.abs(np.polyval(pf, la) - ne)) / np.max(np.abs(ne)))
            pe = np.polyfit(la, e0, 1)
            out["lambda_eK_zero_" + quando] = float(-pf[1] / pf[0])
            out["lambda_E0_zero_" + quando] = float(-pe[1] / pe[0])
            ok4 &= res <= TOLL_LIN
            n4.append("L %d %s lin %.1e" % (L, quando, res))
            print("  L %3d %-6s: N e_K lineare in lambda (lo scarto dal fit %.1e relativo, la pendenza / M %+.9f); e_K = 0 a lambda %.5f; E0 = 0 a lambda %.5f"
                  % (L, quando, res, pf[0] / M, out["lambda_eK_zero_" + quando], out["lambda_E0_zero_" + quando]))
        # ### (4) il legame e la cinetica dopo la dinamica a L_DINAMICA, contro lambda 0
        Em0, _a, El0, M0, _b, _c, _d = stati[(0.0, tq)]
        Em1, _a, El1, M1, V1, _c, _d = stati[(L_DINAMICA, tq)]
        Ec0, Ec1 = Em0 - M0 * e_K0, Em1 - M1 * e_K0
        dl, dc = abs(El1 - El0) / abs(El0), abs(Ec1 - Ec0) / abs(Ec0)
        ok4 &= dl <= TOLL_LIN and dc <= TOLL_LIN
        n4.append("L %d dinamica legame %.1e cinetica %.1e" % (L, dl, dc))
        out["dinamica"] = {"legame_0": El0, "legame_l": El1, "cinetica_0": Ec0, "cinetica_l": Ec1, "rel_legame": dl, "rel_cinetica": dc}
        print("  L %3d: dopo %d tick a lambda %.2f contro lambda 0: il legame %+.9e / %+.9e (%.1e relativo), la cinetica %+.6e / %+.6e (%.1e relativo); la larghezza %.4f / %.4f"
              % (L, SC.T_FROZEN, L_DINAMICA, El1, El0, dl, Ec1, Ec0, dc, stati[(L_DINAMICA, tq)][5], stati[(0.0, tq)][5]))
        # ### (5) M e V con la convenzione
        M_0, V_0 = stati[(L_DINAMICA, "t0")][3], stati[(L_DINAMICA, "t0")][4]
        dM, dV = abs(M1 - M_0) / M_0, abs(V1 - V_0) / V_0
        ok5 &= dM <= TOLL_NORMA and dV <= TOLL_NORMA
        n5.append("%.1e/%.1e" % (dM, dV))
        ris.append(out)
        scrivi(dict(out, tipo="scomposizione"))
    print("-" * 130)
    print("### LA LETTURA: con lo zero simmetrico (lambda 1/2)")
    for out in ris:
        for x in out["righe"]:
            if x["lambda"] == 0.5:
                print("  L %3d %-6s: i costituenti %+.4f, la cinetica %+.4f, il legame %+.4f dell'energia a riposo (E0 %+.6e, e_K %+.5f)"
                      % (out["L"], x["quando"], x["f_costituenti"], x["f_cinetica"], x["f_legame"], x["E0"], x["e_K"]))
    print("-" * 130)
    print("### I CRITERI")
    esito("DEVE PASSARE (1): lo zero di oggi (lambda 0) ridà le frazioni di 9adcb3b1 (il suo jsonl) entro %g" % TOLL_RIF, ok1, "; ".join(n1))
    esito("DEVE PASSARE (2): la famiglia a lambda 0 = il tick di oggi, a lambda 1/2 = convenzione_simmetrica, AL BIT (un tick sul solitone)", ok2, "")
    esito("DEVE PASSARE (3): lo spostamento misurato Delta e(lambda) = 2 pi lambda entro %g, e lo stato uniforme autostato entro %g" % (TOLL_SPOST, TOLL_SPOST), ok3, "il peggiore %.1e" % max(n3))
    esito("DEVE PASSARE (4): N e_K lineare entro %g; il legame e la cinetica dopo la dinamica a lambda %g = lambda 0 entro %g relativo" % (TOLL_LIN, L_DINAMICA, TOLL_LIN), ok4, "; ".join(n4))
    a, b = ris
    conv = max(abs(x[f] - y[f]) for x, y in zip(a["righe"], b["righe"]) for f in ("f_costituenti", "f_cinetica", "f_legame"))
    ok5 &= conv <= TOLL_CONV
    esito("DEVE PASSARE (5): M e V dopo %d tick a lambda %g entro %g; le frazioni alle due taglie entro %g (a ogni lambda)" % (SC.T_FROZEN, L_DINAMICA, TOLL_NORMA, TOLL_CONV), ok5,
          "%s; le taglie %.2e" % (" ".join(n5), conv))
    print("-" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    scrivi({"tipo": "esito", "passano": OK[0], "totale": OK[1], "deve_fallite": FALLITE})
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
