# -*- coding: utf-8 -*-
r"""**LA SCOMPOSIZIONE DELL'ENERGIA A RIPOSO DEL SOLITONE** *(la parte 2 del mandato del 2026-10-27; [[SOLITONE-VUOTO-CONGELATO]], [[PROGETTO-MASSA-COLLETTIVA]])*: ### **sull'oggetto stabile col vuoto
congelato** *(`S1`, `N 1e6`)*: ### **i costituenti `N e_K`, la parte cinetica, il legame col vuoto** *(con l'energia della forma `S1`, non quella `S3` scritta in `termini_di_h`)*.

> ### ⛔ **Il task history e' `2026-10-27_scomposizione_solitone.md`.** ### **In memoria; nessun file del nucleo.**
> ### **Importati, non copiati:** `_solitone_vuoto_congelato` *(`VUOTO`, le costanti)*, `_solitoni_triangoli` *(`c_triangoli`, `profilo_u`, `A1`, `A2`, `AREA_NODO`, `RAGGIO_FRAZ`)*, `_modi_pi_e_solitoni.largo`, `_screening_forme_s3` *(`forma`, `pezzi_di`)*,
> `energia_pesata.termini_di_h`, `_triangoli_forza.coppia_K`, `scena_l2.scena_toro`, `tick.percorri_tick`. ### **La costruzione dello stato ripete le righe di `_solitone_vuoto_congelato.corsa`** *(il criterio `1` la confronta col referto, al bit)*.

Gira con:  python csv/_scomposizione_solitone.py > doc/referti_l2/scomposizione_solitone.txt
"""
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

N_SOL = 1e6
FATTORI = (12.0, 18.0)
T_FROZEN = 2000
TOLL_FORMA = 1e-8
TOLL_NORMA = 1e-10
TOLL_CONV = 0.01
RIF = os.path.join(RADICE, "doc", "referti_l2", "solitone_vuoto_congelato.jsonl")
JSONL = os.path.join(RADICE, "doc", "referti_l2", "scomposizione_solitone.jsonl")
OK = [0, 0]
FALLITE = []
PAR = {"eps": 0.0}


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


def F1(x):
    return x - np.arctan(x)


def scena(L):
    import scena_l2 as SL
    import _solitone_vuoto_congelato as VC
    inc, mot, st, par = SL.scena_toro("triangoli", (L, L), 1.0, 0.1)
    mot.cs = np.full(inc.n, VC.S)
    mot.lambda_c = None
    par = dict(par)
    par["eps"] = 0.0
    return inc, mot, st, par


def posizioni(L, n):
    import _solitoni_triangoli as STR
    v = np.arange(n)
    m1, m2 = v // L, v % L
    d1 = (m1 - L // 2 + L // 2) % L - L // 2
    d2 = (m2 - L // 2 + L // 2) % L - L // 2
    pos = d1[:, None] * STR.A1 + d2[:, None] * STR.A2
    return m1, m2, pos


def stato_solitone(L, rec):
    """### Le righe di `_solitone_vuoto_congelato.corsa` che costruiscono lo stato di partenza."""
    import _solitoni_triangoli as STR
    import _solitone_vuoto_congelato as VC
    import _triangoli_forza as TF
    import scena_l2 as SL
    inc, mot, st, par = scena(L)
    n = inc.n
    q, r, u = STR.profilo_u(VC.FORMA, rec["c"], VC.S, N_SOL, STR.LAM0_TRI, rec["larghezza"])
    m1, m2, pos = posizioni(L, n)
    rr = np.hypot(pos[:, 0], pos[:, 1])
    g = np.interp(rr, r, u, right=0.0) * math.sqrt(STR.AREA_NODO)
    Q = TF.coppia_K(0.0, VC.S)[0]["Q"][:, 0]
    cel = g[:, None] * Q[None, :] * np.exp(2j * np.pi * (m1 + m2) / 3.0)[:, None]
    cel *= math.sqrt(N_SOL / float(np.sum(np.abs(cel) ** 2)))
    st["psi_h"][...] = cel.reshape(st["psi_h"].shape)
    st["phi_h"][...] = SL.VUOTO_PER_ESTREMITA
    return inc, mot, st, par, pos, Q, m1, m2


def stato_uniforme(L, Q, m1, m2):
    inc, mot, st, par = scena(L)
    cel = Q[None, :] * np.exp(2j * np.pi * (m1 + m2) / 3.0)[:, None]
    st["psi_h"][...] = cel.reshape(st["psi_h"].shape)
    st["phi_h"][...] = 0.0
    return inc, mot, st


def parti(inc, mot, st):
    import energia_pesata as EP
    import _solitone_vuoto_congelato as VC

    def H(s):
        pn, pa = EP.termini_di_h(mot, s, PAR)
        return float(np.sum(pn)) + float(np.sum(pa))
    s0 = dict(st)
    s0["phi_h"] = np.zeros_like(st["phi_h"])
    E_mat = H(s0)
    s1 = dict(st)
    s1["psi_h"] = np.zeros_like(st["psi_h"])
    E_vuoto = H(s1)
    rho = np.zeros(inc.n)
    np.add.at(rho, inc.nodo, np.sum(np.abs(st["psi_h"]) ** 2, axis=1))
    lam = np.zeros(inc.n)
    np.add.at(lam, inc.nodo, np.abs(st["phi_h"]) ** 2)
    E_leg = float(np.sum(lam * F1(rho / lam)))
    del VC
    return E_mat, E_vuoto, E_leg, float(rho.sum()), float(lam.sum())


def misure(inc, st, pos, w0):
    import _solitoni_triangoli as STR
    rho = np.zeros(inc.n)
    np.add.at(rho, inc.nodo, np.sum(np.abs(st["psi_h"]) ** 2, axis=1))
    M = float(rho.sum())
    c = (rho @ pos) / M
    w2 = float(rho @ np.sum((pos - c) ** 2, axis=1)) / M
    fr = float(rho[np.hypot(pos[:, 0] - c[0], pos[:, 1] - c[1]) <= STR.RAGGIO_FRAZ * w0].sum()) / M
    return math.sqrt(w2), fr


def main(argv):
    del argv
    import _presidio
    import _universalita_massa as UM
    import _modi_pi_e_solitoni as MPS
    import _screening_forme_s3 as SF
    import _solitoni_triangoli as STR
    import _solitone_vuoto_congelato as VC
    import composizione as CM
    import tick as TK
    _presidio.avvia(__file__)
    print("=" * 130)
    print("LA SCOMPOSIZIONE DELL'ENERGIA A RIPOSO DEL SOLITONE: S1, N 1e6, il vuoto congelato; i costituenti N e_K, la parte cinetica, il legame (l'energia di S1)")
    print("=" * 130)
    blobs = {p: UM.blob(p) for p in ("soliton_simulator.py", "csv/_scomposizione_solitone.py", "csv/_solitone_vuoto_congelato.py", "csv/_solitoni_triangoli.py", "primo_ordine/energia_pesata.py", "doc/referti_l2/solitone_vuoto_congelato.jsonl")}
    print("  il passo: %d pezzi, impronta %s (intatto); i blob nel repo: %s" % (len(CM.ORDINE), CM.IMPRONTA, "; ".join("%s %s" % (k, v["sha1-BYTE"]) for k, v in blobs.items())))
    print("  la configurazione: N_SOL %g FATTORI %s T_FROZEN %d TOLL_FORMA %g TOLL_NORMA %g TOLL_CONV %g; da _solitone_vuoto_congelato: FORMA %s S %g VUOTO %s" % (N_SOL, FATTORI, T_FROZEN, TOLL_FORMA, TOLL_NORMA, TOLL_CONV, VC.FORMA, VC.S, VC.VUOTO))
    print("  il legame: Lambda F_1(rho/Lambda), F_1(x) = x - arctan x (termini_di_h scrive la forma S3 del nucleo)")
    print("-" * 130)
    io.open(JSONL, "w", encoding="utf-8").close()
    scrivi({"tipo": "testata", "blobs": blobs, "impronta": CM.IMPRONTA})
    # ### il controllo della forma
    xs = np.logspace(-4, 3, 50)
    al, _be = SF.pezzi_di("S1")(xs, np.ones_like(xs))
    h = 1e-6
    der = (F1(xs * (1 + h)) - F1(xs * (1 - h))) / (2 * h * xs)
    dforma = float(np.max(np.abs(der - al)))
    esito("DEVE PASSARE (2): la forma del legame: F_1' = alpha_1 di _screening_forme_s3 entro %g (50 x da 1e-4 a 1e3)" % TOLL_FORMA, dforma <= TOLL_FORMA, "%.1e" % dforma)
    rif = {}
    for l in io.open(RIF, encoding="utf-8"):
        d = json.loads(l)
        if d.get("tipo") == "corsa" and d["N"] == N_SOL and d["modo"] == "congelato" and d["zero"] == "oggi":
            rif[d["L"]] = d
    vero = MPS.LAM0
    MPS.LAM0 = STR.LAM0_TRI
    try:
        c, cy, w0k = STR.c_triangoli(VC.S)
        q = MPS.largo(VC.FORMA, c, VC.S, N_SOL)
    finally:
        MPS.LAM0 = vero
    rec = {"larghezza": q["larghezza"], "c": c, "mu": q["mu"]}
    ris = []
    ok1 = True
    for fat in FATTORI:
        L = int(3 * math.ceil(fat * rec["larghezza"] / 3.0))
        inc, mot, st, par, pos, Q, m1, m2 = stato_solitone(L, rec)
        w_in, fr_in = misure(inc, st, pos, rec["larghezza"])
        d = rif.get(L)
        ok1 &= d is not None and d["w_iniziale"] == w_in and d["serie"][0][2] == fr_in
        incu, motu, stu = stato_uniforme(L, Q, m1, m2)
        Eu, _ev, _el, Mu, _lu = parti(incu, motu, stu)
        e_K = Eu / Mu
        out = {"L": L, "e_K": e_K}
        for quando in ("t0", "t%d" % T_FROZEN):
            if quando != "t0":
                phi0 = st["phi_h"].copy()
                with SF.forma(VC.FORMA):
                    for _ in range(T_FROZEN):
                        TK.percorri_tick(st, mot, par, VC.VUOTO, None, len(CM.ORDINE))
                        st["phi_h"][...] = phi0
            E_mat, E_v, E_leg, M, V = parti(inc, mot, st)
            E0 = E_mat + E_leg
            E_cos = M * e_K
            E_cin = E_mat - E_cos
            w, fr = misure(inc, st, pos, rec["larghezza"])
            out[quando] = {"E_mat": E_mat, "E_vuoto": E_v, "E_legame": E_leg, "E0": E0, "N_eK": E_cos, "E_cin": E_cin, "M": M, "V": V, "larghezza": w, "frazione": fr,
                           "f_costituenti": E_cos / E0, "f_cinetica": E_cin / E0, "f_legame": E_leg / E0, "legame_per_costituente": E_leg / M}
            o = out[quando]
            print("  L %3d %-6s: E0 %+.6e = N e_K %+.6e + cinetica %+.6e + legame %+.6e (il vuoto %+.1e) | le frazioni: costituenti %+.4f, cinetica %+.4f, legame %+.4f | il legame per costituente %+.5f (e_K %+.5f, mu %+.5f) | larghezza %.3f"
                  % (L, quando, E0, E_cos, E_cin, E_leg, E_v, o["f_costituenti"], o["f_cinetica"], o["f_legame"], o["legame_per_costituente"], e_K, rec["mu"], w))
            sys.stdout.flush()
        out["dM"] = abs(out["t%d" % T_FROZEN]["M"] - out["t0"]["M"]) / out["t0"]["M"]
        out["dV"] = abs(out["t%d" % T_FROZEN]["V"] - out["t0"]["V"]) / out["t0"]["V"]
        ris.append(out)
        scrivi(dict(out, tipo="scomposizione"))
    print("-" * 130)
    print("### I CRITERI")
    esito("DEVE PASSARE (1): lo stato a t = 0 = quello della parte 1 (la larghezza e la frazione al bit col jsonl di 74f99039)", ok1, "")
    esito("DEVE PASSARE (3): M e V dopo %d tick col vuoto congelato entro %g" % (T_FROZEN, TOLL_NORMA), all(o["dM"] <= TOLL_NORMA and o["dV"] <= TOLL_NORMA for o in ris),
          " ".join("%.1e/%.1e" % (o["dM"], o["dV"]) for o in ris))
    a, b = ris
    conv = max(abs(a[k][f] - b[k][f]) for k in ("t0", "t%d" % T_FROZEN) for f in ("f_costituenti", "f_cinetica", "f_legame"))
    esito("DEVE PASSARE (4): le frazioni alle due taglie entro %g" % TOLL_CONV, conv <= TOLL_CONV, "%.2e" % conv)
    print("-" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    scrivi({"tipo": "esito", "passano": OK[0], "totale": OK[1], "deve_fallite": FALLITE})
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
