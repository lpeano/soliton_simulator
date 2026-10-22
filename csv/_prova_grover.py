# -*- coding: utf-8 -*-
r"""**LA PROVA DI GROVER: LA STESSA `S3` CON LA MONETA DI FOURIER, SU QUADRATO E TRIANGOLI** *(una diagnosi)*.

> ### ⛔ **Il task history e' `2026-10-22_prova_grover.md`.** ### **La sostituzione e' SOLO IN MEMORIA:** l'operatore
> `grover` del motore *(e `grover_scalare` in `F2`)* ### **si rimpiazza nella scena costruita qui** *(`_triangoli.scena`
> avvolta)*; ### **`leggi.yaml`, il passo e l'impronta non si toccano.** ### **Nessuna cura scelta.**

## IL FLUSSO DI FOURIER, senza numeri
`F_jl = w^{jl}/sqrt d`, `w = e^{2 pi i/d}`, sulle `d` estremita' del nodo ### **in ordine ciclico** *(l'angolo della
direzione)*; `F = sum_j e^{i phi_j} P_j` *(ramo principale, `-1 -> +pi` come Grover)*; ### **`F(theta) = sum_j e^{i phi_j
theta/pi} P_j`**, `theta = pi s frazione` ### **come Grover** *(`s` uniforme: si asserisce)*.

Gira con:  python csv/_prova_grover.py
"""
import contextlib
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
TOLL_PIATTA = 1e-8             # una fase uguale a ogni k entro 1e-8, dal mandato
MIN_VARIAZIONE = 1e-3          # l'ampiezza minima di un ramo con Fourier, dal mandato
ULP_ESATTA = 64
COLPEVOLE, INNOCENTE, STABILE = 0.1, 0.5, 1e-3
X_DILUITA = 1e-4
JSONL = os.path.join(RADICE, "doc", "referti_l2", "prova_grover.jsonl")
J_GRADINO2 = os.path.join(RADICE, "doc", "referti_l2", "triangoli_gradino2.jsonl")
OK = [0, 0]


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    print("  %-80s %s   %s" % (che[:80], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return passa


# =====================================================================================
#   LA MONETA DI FOURIER, IN MEMORIA
# =====================================================================================
def ordine_ciclico(inc, nv):
    """### `(n, d)`: le estremita' di ogni nodo, ordinate per angolo della direzione."""
    o = np.argsort(inc.nodo, kind="stable")
    d = inc.m * 2 // inc.n
    E = o.reshape(inc.n, d)
    ang = np.mod(np.arctan2(nv[E, 1], nv[E, 0]), 2.0 * np.pi)
    return np.take_along_axis(E, np.argsort(ang, axis=1), axis=1)


def flusso_fourier(d):
    """### `(phi, Q)`: le fasi principali e la base ortonormale di `F` (Schur complessa)."""
    import scipy.linalg as SLA
    j = np.arange(d)
    F = np.exp(2j * np.pi * np.outer(j, j) / d) / np.sqrt(d)
    Tm, Q = SLA.schur(F, output="complex")
    return np.angle(np.diag(Tm)), Q


def installa(mot, inc, nv, quali):
    import flussi_parziali as FP
    E = ordine_ciclico(inc, nv)
    d = E.shape[1]
    phi, Q = flusso_fourier(d)

    def applica(vista, frazione):
        s = FP.s_nodo(mot)
        assert float(np.max(s)) == float(np.min(s)), "s NON uniforme: il flusso di Fourier qui vuole un solo theta"
        theta = np.pi * float(s[0]) * FP._frazione_valida(frazione)
        Ft = (Q * np.exp(1j * phi * theta / np.pi)) @ Q.conj().T
        vista[E] = np.einsum("ij,njc->nic", Ft, vista[E])

    def op_psi(st, parametri, frazione):
        applica(st["psi_h"], frazione)
        mot.applicazioni["grover"] += 1
        return st

    def op_phi(st, parametri, frazione):
        applica(st["phi_h"].reshape(-1, 1), frazione)
        mot.applicazioni["grover_scalare"] += 1
        return st
    if "psi" in quali:
        mot.operatori["grover"] = op_psi
    if "phi" in quali:
        mot.operatori["grover_scalare"] = op_phi


@contextlib.contextmanager
def variante(quali, x=None):
    """### `_triangoli.scena` avvolta: la scena costruita ha Fourier al posto di Grover (`quali`)."""
    import _triangoli as T
    vero = T.scena

    def scena(griglia, lato, dtau, x_):
        inc, mot, st, par = vero(griglia, lato, dtau, x_ if x is None else x)
        if quali:
            installa(mot, inc, T.versori(inc.m, griglia[1]), quali)
        return inc, mot, st, par
    T.scena = scena
    try:
        yield
    finally:
        T.scena = vero


# =====================================================================================
#   LA CAMMINATA SOLA: BANDE PIATTE, ESATTEZZA, ISOTROPIA
# =====================================================================================
def wrap(x):
    return np.angle(np.exp(1j * x))


def piatte(B):
    """### Le fasi uguali a OGNI `k` entro `TOLL_PIATTA`, e l'ampiezza dei rami ordinati per fase."""
    ph = np.angle(np.linalg.eigvals(B))
    trovate = []
    for c in ph[0, 0]:
        if all(abs(wrap(c - t)) > TOLL_PIATTA for t in trovate):
            if np.all(np.min(np.abs(wrap(ph - c)), axis=-1) <= TOLL_PIATTA):
                trovate.append(float(c))
    s = np.sort(ph, axis=-1)
    amp = (s.max(axis=(0, 1)) - s.min(axis=(0, 1)))
    return trovate, amp


def ruota(A, geo):
    import _triangoli as T
    if geo == "T":
        return T.ruota60(A)
    L = A.shape[0]
    mx, my = np.meshgrid(np.arange(L), np.arange(L), indexing="ij")
    return A[(-my) % L, mx]


def camminata(geo, quali):
    import _stabilita_lineare as SL
    import _triangoli as T
    gr = T.QUADRATO if geo == "Q" else T.TRIANGOLI
    d = len(gr[0])
    with variante(quali):
        A = T.matrice_tick(gr, LATO, DTAU)
    fuori = float(max(np.max(np.abs(A[:, :, :4 * d, 4 * d:])), np.max(np.abs(A[:, :, 4 * d:, :4 * d]))))
    N = int(round(SL.TEMPO_LUNGO / DTAU))
    dev = float(np.max(np.abs(np.log(np.abs(np.linalg.eigvals(np.linalg.matrix_power(A, N)))))))
    pp, ap = piatte(A[:, :, :4 * d, :4 * d])
    pf, af = piatte(A[:, :, 4 * d:, 4 * d:])
    f0 = np.sort(np.angle(np.linalg.eigvals(A)), axis=-1)
    f1 = np.sort(np.angle(np.linalg.eigvals(ruota(A, geo))), axis=-1)
    iso = float(np.max(np.abs(wrap(f0 - f1))))
    return {"N": N, "dev": dev, "fuori_settore": fuori, "piatte_psi": pp, "piatte_phi": pf,
            "amp_psi_min": float(ap.min()), "amp_phi_min": float(af.min()), "iso": iso}


# =====================================================================================
#   IL PROGRAMMA
# =====================================================================================
def main(argv):
    del argv
    import _al_bit_cura_d0 as AB
    import _presidio
    _presidio.avvia(__file__)
    import _stabilita_lineare as SL
    import _stabilita_triangoli as ST
    import _triangoli as T
    import composizione as CM
    print("=" * 100)
    print("LA PROVA DI GROVER: S3 CON LA MONETA DI FOURIER (IN MEMORIA), QUADRATO E TRIANGOLI")
    print("=" * 100)
    print("  il passo: %d pezzi, impronta %s (intatto); R2: S3 sola, cs spento, lato %d, dtau %g, x %g,"
          " eps %g, base proiettata, N dtau %g, la norma, seconda meta'" % (len(CM.ORDINE), CM.IMPRONTA,
                                                                            LATO, DTAU, SL.X, T.EPS_MONETA,
                                                                            SL.TEMPO_LUNGO))
    print("  F1: Fourier per la materia (grover); F2: per materia e vuoto (grover, grover_scalare); l'ordine"
          " ciclico per angolo; il flusso allo stesso angolo di Grover")
    print("-" * 100)
    sys.stdout.flush()
    io.open(JSONL, "w", encoding="utf-8").close()

    def salva(r):
        with io.open(JSONL, "a", encoding="utf-8") as f:
            f.write(json.dumps(r) + "\n")

    # ------------------------------------------------------------ 1. la camminata sola
    print("### 1. LA CAMMINATA SOLA")
    cammi = {}
    for geo in ("Q", "T"):
        for nome, quali in (("GROVER", ()), ("F1", ("psi",)), ("F2", ("psi", "phi"))):
            c = camminata(geo, quali)
            cammi[(geo, nome)] = c
            salva({"camminata": [geo, nome], **c})
            print("  %s %-6s: |lambda(A^N)| -1 max %.2e (tetto %.2e); fuori settore %.1e; piatte psi %s phi %s;"
                  " ampiezza minima dei rami psi %.3e phi %.3e; isotropia %s %.3e"
                  % (geo, nome, c["dev"], c["N"] * ULP_ESATTA * EPS, c["fuori_settore"],
                     ["%.6f pi" % (v / np.pi) for v in c["piatte_psi"]],
                     ["%.6f pi" % (v / np.pi) for v in c["piatte_phi"]], c["amp_psi_min"], c["amp_phi_min"],
                     "C4" if geo == "Q" else "C6", c["iso"]))
            sys.stdout.flush()
    for geo in ("Q", "T"):
        g = cammi[(geo, "GROVER")]
        tutte = g["piatte_psi"] + g["piatte_phi"]
        attese = [-np.pi / 4, -np.pi / 8]
        viste = all(any(abs(abs(v) - abs(a)) <= TOLL_PIATTA for v in tutte) for a in attese)
        if not esito("DEVE FALLIRE %s: Grover HA bande piatte (le fasi pi/4 e pi/8, in un segno)" % geo,
                     viste, "%d trovate" % len(tutte)):
            print("### STOP: il test delle bande piatte e' cieco")
            return 1
        for nome, settori in (("F1", ("psi",)), ("F2", ("psi", "phi"))):
            c = cammi[(geo, nome)]
            esito("DEVE RIUSCIRE %s %s: unitaria ed esatta, entro N*64 ulp" % (geo, nome),
                  c["dev"] <= c["N"] * ULP_ESATTA * EPS, "%.3e" % c["dev"])
            nessuna = all(not c["piatte_" + s] for s in settori)
            amp = min(c["amp_" + s + "_min"] for s in settori)
            esito("DEVE RIUSCIRE %s %s: nessuna banda piatta (settori %s), ramo minimo > %g"
                  % (geo, nome, "+".join(settori), MIN_VARIAZIONE), nessuna and amp > MIN_VARIAZIONE,
                  "ampiezza minima %.3e" % amp)
    print("-" * 100)

    # ------------------------------------------------------------ 2. la stabilita' lineare
    print("### 2. LA STABILITA' LINEARE R2")
    vq = AB.committato()["R2 lato 32"]
    vt = None
    for riga in io.open(J_GRADINO2, encoding="utf-8"):
        w = json.loads(riga)
        if w.get("nome") == "R2 triangoli SE eps 1e-07":
            vt = w
    risultati = {}
    for geo, br, gr in (("Q", "Q", T.QUADRATO), ("T", "SE", T.TRIANGOLI)):
        t0 = time.time()
        b = ST.braccio_proiettato("R2 %s GROVER" % geo, gr, br, SL.EPS_REL, SL.TEMPO_LUNGO)
        v = vq if geo == "Q" else vt
        bit = all(np.array_equal(np.asarray(b["pend"][k]), np.asarray(v["pend"][k])) for k in v["pend"]) and \
            np.array_equal(np.asarray(b["gamma"]), np.asarray(v["gamma"]))
        if not esito("DEVE RIUSCIRE %s: con Grover lo strumento ridà %s AL BIT" % (
                geo, "594417f6" if geo == "Q" else "bb0ef057"), bit, "%.0f s" % (time.time() - t0)):
            print("### STOP: lo strumento non ripete il referto con Grover")
            return 1
        risultati[(geo, "GROVER", SL.X)] = np.asarray(b["pend"]["meta_norm"])
        for nome, quali, x in (("F1", ("psi",), None), ("F2", ("psi", "phi"), None)) + (
                (("F2", ("psi", "phi"), X_DILUITA),) if geo == "Q" else ()):
            t0 = time.time()
            with variante(quali, x):
                b = ST.braccio_proiettato("R2 %s %s x %g" % (geo, nome, x or SL.X), gr, br, SL.EPS_REL,
                                          SL.TEMPO_LUNGO)
            g = np.asarray(b["pend"]["meta_norm"])
            risultati[(geo, nome, x or SL.X)] = g
            i = tuple(int(a) for a in np.unravel_index(int(np.argmax(g)), g.shape))
            print("  %s %s x %-6g: max gamma %.4f a %s; uniformita' %.1f ulp; %.0f s"
                  % (geo, nome, x or SL.X, float(g.max()), i, b["uniformita_ulp"], time.time() - t0))
            sys.stdout.flush()
            salva({"stabilita": [geo, nome, x or SL.X], "max": float(g.max()), "dove": list(i),
                   "uniformita_ulp": b["uniformita_ulp"], "meta_norm": g.tolist()})
    print("-" * 100)

    # ------------------------------------------------------------ 3. le letture
    print("### 3. LE LETTURE (sul massimo di gamma su tutti i k)")
    kv, lab, _M, _K, _d = ST.zona(LATO)
    letture = {}
    for nome in ("F1", "F2"):
        q = {}
        for geo in ("Q", "T"):
            gG = float(risultati[(geo, "GROVER", SL.X)].max())
            gF = risultati[(geo, nome, SL.X)]
            i = tuple(int(a) for a in np.unravel_index(int(np.argmax(gF)), gF.shape))
            dove = ("(%s)" % lab[i]) if geo == "T" else ""
            q[geo] = float(gF.max()) / gG
            print("  %s %s: %.4f contro Grover %.4f -> rapporto %.4f; a %s %s; STABILE? %s"
                  % (nome, geo, float(gF.max()), gG, q[geo], i, dove,
                     "SI'" if float(gF.max()) <= STABILE * gG else "no"))
        if all(v <= COLPEVOLE for v in q.values()):
            v = "GROVER COLPEVOLE"
        elif all(v >= INNOCENTE for v in q.values()):
            v = "GROVER INNOCENTE"
        else:
            v = "PARZIALE"
        letture[nome] = {"rapporti": q, "verdetto": v}
        print("  ### %s: %s" % (nome, v))
    gD = float(risultati[("Q", "F2", X_DILUITA)].max())
    gG = float(risultati[("Q", "GROVER", SL.X)].max())
    dil = gD > STABILE * gG
    print("  ### F2 a x %g sul quadrato: max %.4f -> %s" % (X_DILUITA, gD, "INSTABILE: il logaritmo resta un"
                                                                         " colpevole indipendente"
                                                         if dil else "STABILE"))
    salva({"letture": letture, "diluita": {"max": gD, "instabile": bool(dil)}})
    print("=" * 100)
    print("LA PROVA DI GROVER: %d su %d controlli   %s" % (OK[0], OK[1], "### TUTTI PASSATI"
                                                          if OK[0] == OK[1] else "### CI SONO BUCHI"))
    print("=" * 100)
    return 0 if OK[0] == OK[1] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
