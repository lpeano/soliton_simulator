# -*- coding: utf-8 -*-
r"""**`S-E`: IL MODO CHE CRESCE IN `R2`, PROIETTATO SUI RAMI DELLA CAMMINATA SOLA** *(quadrato e triangoli)*.

> ### ⛔ **Il task history e' `2026-10-22_s3_due_misure.md`**; la prova e' la `1` della sez. `3.2` di
> `doc/S3_RIPENSATA.md`. ### **Una misura: nessun file del nucleo si tocca.**

## CHE COSA SI MISURA *(precisato nel task history, sez. `1.2`)*
- ### **il modo che cresce:** l'autovettore di modulo massimo di `M(k)` *(la monodromia della base proiettata
  dopo `N` tick, `R2`, lato `32`, `x 0.1`)* ### **al `k` della banda** *(argmax della pendenza della norma)*;
- ### **i rami:** la cella di `M` e' REALE *(`re` poi `im`)*; ### **`u = (a + i b)/sqrt2` e' la PARTICELLA a `k`**
  *(evolve con `A(k)`, la camminata sola di `_triangoli.matrice_tick`)*, ### **`w = (a - i b)/sqrt2` la BUCA**
  *(evolve con `conj(A(-k))`)*; ### **i pesi** `|Q^H u|^2` e `|Q^H w|^2` *(`Q` dalla forma di Schur complessa: una
  base ORTONORMALE anche coi rami degeneri)*;
- ### **il segno:** con `lambda = e^{-i phi}` *(`phi` la fase per tick)* e `g = +` *(`nu_S3 > 0`)*, ### **la coppia
  (particella `b`, buca `h`) e' FOCALIZZANTE se `g * D < 0`**, ### **`D dtau = wrap(phi_b(k) + phi_b'(-k) - 2 phi_0)
  / 2`** *(`phi_b'(-k) = -phi_h`; `phi_0` il ramo di `A(0)` piu' sovrapposto alla `psi` dello stato uniforme)*.

Gira con:  python csv/_s3_rami.py
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
TOLL_UNIT = 1e-12              # |lambda| di A(k) = 1, dal task history
TOLL_SOMMA = 1e-10             # la somma dei pesi = 1, dal task history
SPARSO = 0.5                   # NON DECIDE se il ramo-particella massimo e' sotto il 50% delle particelle
JSONL = os.path.join(RADICE, "doc", "referti_l2", "s3_rami.jsonl")
J_GRADINO2 = os.path.join(RADICE, "doc", "referti_l2", "triangoli_gradino2.jsonl")
OK = [0, 0]


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    print("  %-78s %s   %s" % (che[:78], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return passa


def corsa_con_m(griglia, braccio):
    """### Il braccio `R2` di `_stabilita_triangoli.braccio_proiettato`, che RENDE anche `M` finale."""
    import _stabilita_lineare as SL
    import _stabilita_triangoli as ST
    lato, dtau, tempo, eps_rel = LATO, DTAU, SL.TEMPO_LUNGO, SL.EPS_REL
    d = len(griglia[0])
    nc = 6 * d
    inc, mot, st, par = ST.scena(griglia, braccio, lato, dtau)
    n = inc.n
    fondo = ST.celle(st, n, d)[0]                     # la cella dello stato uniforme, reale
    N = int(round(tempo / dtau))
    scale = (float(np.max(np.abs(st["psi_h"]))), float(np.max(np.abs(st["phi_h"]))))
    M = np.broadcast_to(np.eye(2 * nc, dtype=complex), (lato, lato, 2 * nc, 2 * nc)).copy()
    acc = np.zeros((lato, lato))
    zero = np.zeros((lato, lato))
    tt, Ln = [0.0], [zero]
    base = st
    for t in range(1, N + 1):
        R, dopo = ST.green(base, mot, par, (), lato, scale, eps_rel, d)
        ST.proietta(dopo, n, d)
        M = np.matmul(R, M)
        s = np.sqrt(np.sum(np.abs(M) ** 2, axis=(-2, -1)))
        M /= s[..., None, None]
        acc += np.log(s)
        base = dopo
        if t % SL.OGNI == 0 or t % (N // 4) == 0:
            tt.append(t * dtau)
            Ln.append(acc.copy())
    T = N * dtau
    g = SL.pendenze(tt, Ln, T / 2.0, T)
    return {"M": M, "meta_norm": g, "fondo": fondo, "d": d, "nc": nc}


def schur(A):
    import scipy.linalg as SLA
    Tm, Q = SLA.schur(A, output="complex")
    return np.diag(Tm).copy(), Q, float(np.max(np.abs(Tm - np.diag(np.diag(Tm)))))


def wrap(x):
    return float(np.angle(np.exp(1j * x)))


def esamina(nome, griglia, braccio, gamma_vecchio):
    import _triangoli as T
    t0 = time.time()
    c = corsa_con_m(griglia, braccio)
    g, M, nc = c["meta_norm"], c["M"], c["nc"]
    al_bit = bool(np.array_equal(g, gamma_vecchio))
    esito("%s: gamma (norma, seconda meta') AL BIT col referto committato" % nome, al_bit,
          "%.0f s" % (time.time() - t0))
    if not al_bit:
        return None
    L = LATO
    k = tuple(int(x) for x in np.unravel_index(int(np.argmax(g)), g.shape))
    mk = ((-k[0]) % L, (-k[1]) % L)
    lam, V = np.linalg.eig(M[k])
    i = int(np.argmax(np.abs(lam)))
    v = V[:, i] / np.linalg.norm(V[:, i])
    a, b = v[:nc], v[nc:]
    u = (a + 1j * b) / np.sqrt(2.0)
    w = (a - 1j * b) / np.sqrt(2.0)
    A = T.matrice_tick(griglia, L, DTAU)
    mod = float(np.max(np.abs(np.abs(np.linalg.eigvals(A[k])) - 1.0)))
    esito("%s: A(k) della camminata sola UNITARIA, |lambda| = 1 entro %g" % (nome, TOLL_UNIT),
          mod <= TOLL_UNIT, "%.3e" % mod)
    lp, Qp, offp = schur(A[k])
    lh, Qh, offh = schur(np.conj(A[mk]))
    l0, Q0, _o0 = schur(A[0, 0])
    cp = np.abs(Qp.conj().T @ u) ** 2
    ch = np.abs(Qh.conj().T @ w) ** 2
    somma = float(cp.sum() + ch.sum())
    esito("%s: la decomposizione e' completa, la somma dei pesi = 1 entro %g" % (nome, TOLL_SOMMA),
          abs(somma - 1.0) <= TOLL_SOMMA, "%.3e (Schur fuori diagonale %.1e, %.1e)"
          % (abs(somma - 1.0), offp, offh))
    # ### il fondo: la psi dello stato uniforme, nella cella complessa, sui rami di A(0)
    f = c["fondo"]
    z = f[:nc] + 1j * f[nc:]
    z[4 * c["d"]:] = 0.0                              # solo psi
    z = z / np.linalg.norm(z)
    c0 = np.abs(Q0.conj().T @ z) ** 2
    b0 = int(np.argmax(c0))
    phi = lambda l_: -float(np.angle(l_))             # noqa: E731  la fase per tick
    phi0 = phi(l0[b0])
    bp = int(np.argmax(cp))
    bh = int(np.argmax(ch))
    # ### la fase del ramo della buca a k e' -phi_b'(-k): quindi phi_b'(-k) = -phi(lh)
    phi_b = phi(lp[bp])
    phi_bm = -phi(lh[bh])
    Ddt = wrap(phi_b + phi_bm - 2.0 * phi0) / 2.0
    gsegno = 1.0
    foc = gsegno * Ddt < 0.0
    quota = float(cp[bp] / cp.sum()) if cp.sum() > 0 else 0.0
    print("  %s: la banda a k = %s (gamma %.4f); |autovalore di M| %.6e" % (nome, k, float(g[k]),
                                                                             float(np.abs(lam[i]))))
    print("      il fondo: la psi uniforme sul ramo %d di A(0) per %.6f; phi_0 %+.6f per tick"
          % (b0, float(c0[b0]), phi0))
    print("      PESI: particelle %.6f, buche %.6f" % (float(cp.sum()), float(ch.sum())))
    ordine = sorted([("particella", j, float(cp[j]), phi(lp[j])) for j in range(nc)] +
                    [("buca", j, float(ch[j]), phi(lh[j])) for j in range(nc)],
                    key=lambda r: -r[2])
    for tipo, j, p_, f_ in ordine[:10]:
        print("        %-10s ramo %2d  peso %.6f  fase per tick %+.6f" % (tipo, j, p_, f_))
    print("      LA COPPIA DI PESO MASSIMO: particella %d (%.4f, %.1f%% delle particelle), buca %d (%.4f);"
          " D dtau = %+.6e -> %s" % (bp, float(cp[bp]), 100 * quota, bh, float(ch[bh]), Ddt,
                                      "FOCALIZZANTE (g D < 0)" if foc else "NON focalizzante (g D >= 0)"))
    sys.stdout.flush()
    return {"nome": nome, "k": list(k), "gamma": float(g[k]), "pesi_particelle": cp.tolist(),
            "pesi_buche": ch.tolist(), "fasi_particelle": [phi(x) for x in lp],
            "fasi_buche": [phi(x) for x in lh], "fondo_ramo": b0, "fondo_peso": float(c0[b0]),
            "phi0": phi0, "coppia": [bp, bh], "D_dtau": Ddt, "focalizzante": bool(foc),
            "quota": quota}


def main(argv):
    del argv
    import _presidio
    _presidio.avvia(__file__)
    import _al_bit_cura_d0 as AB
    import _stabilita_lineare as SL
    import _triangoli as T
    import composizione as CM
    print("=" * 100)
    print("S-E: IL MODO CHE CRESCE IN R2, PROIETTATO SUI RAMI DELLA CAMMINATA SOLA")
    print("=" * 100)
    print("  R2: S3 sola, cs spento; lato %d, dtau %g, x %g, eps %g; base proiettata; N dtau %g; la"
          " banda = argmax della pendenza della norma (seconda meta')"
          % (LATO, DTAU, SL.X, T.EPS_MONETA, SL.TEMPO_LUNGO))
    print("  il passo: %d pezzi, impronta %s; g = + (nu_S3 > 0); focalizzante se g D < 0; NON DECIDE"
          " sotto il %d%% delle particelle" % (len(CM.ORDINE), CM.IMPRONTA, int(100 * SPARSO)))
    print("-" * 100)
    sys.stdout.flush()
    io.open(JSONL, "w", encoding="utf-8").close()
    vq = np.asarray(AB.committato()["R2 lato 32"]["pend"]["meta_norm"])
    vt = None
    for riga in io.open(J_GRADINO2, encoding="utf-8"):
        w = json.loads(riga)
        if w.get("nome") == "R2 triangoli SE eps 1e-07":
            vt = np.asarray(w["pend"]["meta_norm"])
    esiti = []
    for nome, griglia, br, vecchio in (("QUADRATO", T.QUADRATO, "Q", vq),
                                       ("TRIANGOLI", T.TRIANGOLI, "SE", vt)):
        r = esamina(nome, griglia, br, vecchio)
        if r is None:
            print("### STOP: %s non ripete il referto committato" % nome)
            return 1
        with io.open(JSONL, "a", encoding="utf-8") as f:
            f.write(json.dumps(r) + "\n")
        esiti.append(r)
        print("-" * 100)
    print("### LA LETTURA (la prova 1 della sez. 3.2)")
    sparsi = [r["nome"] for r in esiti if r["quota"] < SPARSO]
    non_foc = [r["nome"] for r in esiti if not r["focalizzante"]]
    if sparsi:
        verdetto = "NON DECIDE (peso sparso: %s)" % ", ".join(sparsi)
    elif non_foc:
        verdetto = "LA LETTURA 3.2 CADE (non focalizzante: %s)" % ", ".join(non_foc)
    else:
        verdetto = "LA LETTURA 3.2 TIENE (focalizzante sul quadrato e sui triangoli)"
    print("  ### %s" % verdetto)
    with io.open(JSONL, "a", encoding="utf-8") as f:
        f.write(json.dumps({"verdetto": verdetto}) + "\n")
    print("=" * 100)
    print("S-E: %d su %d controlli   %s" % (OK[0], OK[1], "### TUTTI PASSATI"
                                            if OK[0] == OK[1] else "### CI SONO BUCHI"))
    print("=" * 100)
    return 0 if OK[0] == OK[1] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
