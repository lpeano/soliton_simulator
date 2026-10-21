# -*- coding: utf-8 -*-
r"""**TRIANGOLI, GRADINO 2: `S3` E LA STABILITA' LINEARE (`R2`) SUL TORO TRIANGOLARE, BRACCI `SN` E `SE`.**

> ### ⛔ **Il task history e' `2026-10-21_triangoli_gradino2.md`**; il progetto `doc/PROGETTO_TRIANGOLI.md`
> *(`a840e8f7`)*, il gradino `1` `csv/_triangoli.py` *(`3008bd13`)*. ### **`eps = 0.5`. `leggi.yaml`
> intatto. NESSUNA CURA.**

## ⭐ L'ESTENSIONE, E PERCHE' IN UN FILE A PARTE
`csv/_stabilita_lineare.py` ha ### **le `4` estremita' scritte dentro** *(`celle`, `perturba`, `uniformita`,
e `proietta` col suo `4 * n`)*. ### **Qui le stesse funzioni, in `d`** *(gli archi propri del nodo)*:
la cella e' `6d` complessi, ### **`24` reali sul quadrato** *(`d = 2`)*, ### **`36` sui triangoli** *(`d = 3`)*.
### **Il file di prima resta AL BIT**, e i suoi referti si rigirano anche a HEAD. La scena e' il
costruttore di `_triangoli.py`; ### **il controllo che ripete la cosa giusta e' `R2` di `594417f6` AL BIT
sul quadrato del costruttore generale.**

## I BRACCI *(la scelta di scala e' di Luca: qui si misurano DUE)*
- ### **`SN`, stessa densita' per nodo:** le ampiezze per estremita' `* sqrt(4/6)` *(`psi` e `phi`)*: per
  nodo `rho` e `Lambda` come il quadrato.
- ### **`SE`, stessa ampiezza per estremita':** `x = 0.1`, vuoto `1`, come `594417f6`: per nodo `* 6/4`.

Gira con:  python csv/_stabilita_triangoli.py
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
EPS_REL_2 = 1e-6               # la seconda ampiezza della linearita' (P2 di 2026-10-20)
ULP_ESATTA = 64                # la camminata sola: N * 64 ulp (come c2_esatto_lungo)
ULP_P3 = 64
RIF_MANDATO = 0.407            # il massimo del quadrato citato dal mandato (stimatore degli autovalori)
BANDA_PREV = (0.37, 0.45)      # la previsione della banda, sez. j del progetto
STABILE = 1e-3                 # STABILE se il massimo <= 1e-3 * RIF_MANDATO, dal mandato
S3 = "CAMM-MATERIA-VUOTO"
JSONL = os.path.join(RADICE, "doc", "referti_l2", "triangoli_gradino2.jsonl")
OK = [0, 0]


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    print("  %-78s %s   %s" % (che[:78], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return passa


# =====================================================================================
#   LA SCENA, I BRACCI
# =====================================================================================
def scena(griglia, braccio, lato=LATO, dtau=DTAU):
    """### Il costruttore di `_triangoli`; `SN` riscala `psi_h` e `phi_h` per `sqrt(4/6)`."""
    import _stabilita_lineare as SL
    import _triangoli as T
    inc, mot, st, par = T.scena(griglia, lato, dtau, SL.X)
    if braccio == "SN":
        f = float(np.sqrt(4.0 / 6.0))
        st["psi_h"] *= f
        st["phi_h"] *= f
    else:
        assert braccio in ("SE", "Q"), braccio
    return inc, mot, st, par


# =====================================================================================
#   LA CELLA, L'IMPULSO, LA FUNZIONE DI GREEN, LA PROIEZIONE -- in `d`
# =====================================================================================
def celle(st, n, d):
    """### `(n, 12d)` reali: le `2d` estremita' dei `d` archi propri -- `psi` (`4d`) e `phi` (`2d`)."""
    z = np.concatenate([st["psi_h"].reshape(n, 4 * d), st["phi_h"].reshape(n, 2 * d)], axis=1)
    return np.concatenate([z.real, z.imag], axis=1)


def perturba(st, j, e, d):
    nc = 6 * d
    c, im = j % nc, j >= nc
    dd = 1j * e if im else e
    if c < 4 * d:
        st["psi_h"][c // 2, c % 2] += dd
    else:
        st["phi_h"][c - 4 * d] += dd


def green(base, mot, par, salta, lato, scale, eps_rel, d, dopo=None):
    """### `R(k)` `(L, L, 12d, 12d)` di un tick dalla base, `cs` SPENTO."""
    import _stabilita_lineare as SL
    n = lato * lato
    nc = 6 * d
    if dopo is None:
        dopo = SL.copia(base)
        SL.passo(dopo, mot, par, False, salta, 0.0)
    c0 = celle(dopo, n, d)
    R = np.empty((lato, lato, 2 * nc, 2 * nc), dtype=complex)
    for j in range(2 * nc):
        e = eps_rel * scale[0 if (j % nc) < 4 * d else 1]
        p = SL.copia(base)
        perturba(p, j, e, d)
        SL.passo(p, mot, par, False, salta, 0.0)
        dd = (celle(p, n, d) - c0) / e
        R[:, :, :, j] = np.fft.fft2(dd.reshape(lato, lato, 2 * nc), axes=(0, 1))
    return R, dopo


def uniformita(st, n, d):
    c = celle(st, n, d)
    s = float(np.max(np.abs(c))) or 1.0
    return float(np.max(np.abs(c - c[0]))) / (EPS * s)


def proietta(st, n, d):
    """### Ogni campo sulla MEDIA DELLE CELLE: per nodo, o per estremita' (`2d` per nodo)."""
    for v in st.values():
        if v.shape[0] == n:
            v[...] = np.mean(v, axis=0)
        elif v.shape[0] == 2 * d * n:
            w = v.reshape((n, 2 * d) + v.shape[1:])
            w[...] = np.mean(w, axis=0)
        else:
            raise AssertionError("un campo di forma %r non e' ne' per nodo ne' per estremita'"
                                 % (v.shape,))


def braccio_proiettato(nome, griglia, braccio, eps_rel, tempo, lato=LATO, dtau=DTAU):
    """### `braccio_proiettato` di `_stabilita_lineare`, in `d`, `cs` SPENTO (`R2`)."""
    import _stabilita_lineare as SL
    d = len(griglia[0])
    nc = 6 * d
    inc, mot, st, par = scena(griglia, braccio, lato, dtau)
    n = inc.n
    lm = float(np.mean(mot.densita_vuoto(st)))
    rm = float(np.mean(mot.densita_materia(st)))
    cs_m = 1.0
    N = int(round(tempo / dtau))
    assert N % 4 == 0, "N = %d non si divide in quattro quarti" % N
    scale = (float(np.max(np.abs(st["psi_h"]))), float(np.max(np.abs(st["phi_h"]))))
    fuori = {"nome": nome, "braccio": braccio, "d": d, "lato": lato, "dtau": dtau, "x": SL.X,
             "acceso": False, "salta": [], "eps_rel": eps_rel, "N": N, "cs_m": cs_m,
             "rho_m": rm, "lambda_m": lm, "fine": "N", "proiettata": True}
    M = np.broadcast_to(np.eye(2 * nc, dtype=complex), (lato, lato, 2 * nc, 2 * nc)).copy()
    acc = np.zeros((lato, lato))
    zero = np.zeros((lato, lato))
    tt, Le, Ln, Lq = [0.0], [zero], [zero], {}
    unif = uniformita(st, n, d)
    t0 = time.time()
    base = st
    for t in range(1, N + 1):
        R, dopo = green(base, mot, par, (), lato, scale, eps_rel, d)
        unif = max(unif, uniformita(dopo, n, d))
        proietta(dopo, n, d)
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


# =====================================================================================
#   I CONTROLLI DEL METODO SUI TRIANGOLI
# =====================================================================================
def esatta(griglia, lato=LATO, dtau=DTAU):
    """### La camminata sola, ESATTA, su `N dtau = 100`: `max |ln|lambda(A^N)||`."""
    import _stabilita_lineare as SL
    d = len(griglia[0])
    inc, mot, st, par = scena(griglia, "SE", lato, dtau)
    for k in st:
        st[k][...] = 0
    zero = SL.copia(st)
    SL.passo(zero, mot, par, False, (S3,), 0.0)
    R, _ = green(st, mot, par, (S3,), lato, (1.0, 1.0), 1.0, d, dopo=zero)
    N = int(round(SL.TEMPO_LUNGO / dtau))
    lam = np.linalg.eigvals(np.linalg.matrix_power(R, N))
    return {"N": N, "dev": float(np.max(np.abs(np.log(np.abs(lam)))))}


def prova_p1(griglia, braccio):
    import _stabilita_lineare as SL
    inc, mot, st, par = scena(griglia, braccio)
    SL.passo(st, mot, par, False, (), 0.0)
    a, b = SL.copia(st), SL.copia(st)
    for k in SL.CACHE:
        b[k][...] = 0
    SL.passo(a, mot, par, False, (), 0.0)
    SL.passo(b, mot, par, False, (), 0.0)
    return np.array_equal(a["psi_h"], b["psi_h"]) and np.array_equal(a["phi_h"], b["phi_h"])


def prova_p3(griglia, braccio):
    import _stabilita_lineare as SL
    d = len(griglia[0])
    nc = 6 * d
    inc, mot, st, par = scena(griglia, braccio)
    scale = (float(np.max(np.abs(st["psi_h"]))), float(np.max(np.abs(st["phi_h"]))))
    peggio, al_bit = 0.0, True
    for j in (0, 5, 13, 20, 2 * nc - 1):
        p = SL.copia(st)
        perturba(p, j, SL.EPS_REL * scale[0 if (j % nc) < 4 * d else 1], d)
        SL.passo(p, mot, par, False, (), 0.0)
        a = SL.copia(st)
        SL.passo(a, mot, par, False, (), 0.0)
        c = SL.copia(st)
        SL.passo(c, mot, par, False, (), 0.0)
        for k in ("psi_h", "phi_h"):
            dd = float(np.max(np.abs(a[k] - c[k])))
            al_bit &= bool(np.array_equal(a[k], c[k]))
            peggio = max(peggio, dd / (EPS * float(np.max(np.abs(c[k])))))
    return peggio, al_bit


# =====================================================================================
#   LA ZONA ESAGONALE E LA ROTAZIONE
# =====================================================================================
def zona(lato):
    """### Per ogni `(m_x, m_y)`: il `k` rappresentante (|k| minimo) e l'etichetta.

    `a1 = (1, 0)`, `a2 = (-1/2, sqrt3/2)`; `k . a_i = 2 pi m_i / L`; `K` a `|k| = 4 pi / 3`.
    """
    A = np.array([[1.0, 0.0], [-0.5, np.sqrt(3.0) / 2.0]])
    B = 2.0 * np.pi * np.linalg.inv(A).T          # righe b_i, a_i . b_j = 2 pi delta_ij
    # ### i reciproci stanno a `30` e `90` gradi: i punti `M` (`b/2`) a `30 + 60 i`, ### **i
    # ### vertici `K` a `60 i`**, a `|K| = |b| / sqrt3 = 4 pi / 3`
    vert = [(4.0 * np.pi / 3.0) * np.array([np.cos(np.deg2rad(60 * i)),
                                            np.sin(np.deg2rad(60 * i))]) for i in range(6)]
    kv = np.zeros((lato, lato, 2))
    dk = np.zeros((lato, lato))
    for mx in range(lato):
        for my in range(lato):
            meglio = None
            for p in (-1, 0, 1):
                for q in (-1, 0, 1):
                    k = ((mx + p * lato) * B[0] + (my + q * lato) * B[1]) / lato
                    if meglio is None or np.dot(k, k) < np.dot(meglio, meglio) - 1e-12:
                        meglio = k
            kv[mx, my] = meglio
            dk[mx, my] = min(float(np.linalg.norm(meglio - v)) for v in vert)
    h = lato // 2
    M = {(h, 0), (0, h), (h, h)}
    dmin = float(np.min(dk))
    K = {(a, b) for a in range(lato) for b in range(lato) if dk[a, b] <= dmin + 1e-9}
    lab = np.full((lato, lato), "interno", dtype=object)
    lab[0, 0] = "centro"
    for a, b in M:
        lab[a, b] = "M"
    for a, b in K:
        lab[a, b] = "K"
    return kv, lab, M, K, dmin


def ruota60(g):
    """### `g` ai `k` ruotati di `60` gradi: `(m_x, m_y) -> (-m_y, m_x + m_y)` (`_triangoli.ruota60`)."""
    L = g.shape[0]
    mx, my = np.meshgrid(np.arange(L), np.arange(L), indexing="ij")
    return g[(-my) % L, (mx + my) % L]


def per_json(b):
    fuori = {}
    for k, v in b.items():
        if isinstance(v, np.ndarray):
            fuori[k] = v.tolist()
        elif isinstance(v, dict):
            fuori[k] = {kk: (vv.tolist() if isinstance(vv, np.ndarray) else vv)
                        for kk, vv in v.items()}
        elif isinstance(v, list):
            fuori[k] = [x.tolist() if isinstance(x, np.ndarray) else x for x in v]
        else:
            fuori[k] = v
    return fuori


# =====================================================================================
#   IL PROGRAMMA
# =====================================================================================
def main(argv):
    del argv
    import _presidio
    _presidio.avvia(__file__)
    import _al_bit_cura_d0 as AB
    import _stabilita_lineare as SL
    import _triangoli as T
    import composizione as CM
    import energia_pesata as EP
    print("=" * 100)
    print("TRIANGOLI, GRADINO 2: S3 E LA STABILITA' LINEARE (R2) SUL TORO TRIANGOLARE, BRACCI SN E SE")
    print("=" * 100)
    print("  LA CONFIGURAZIONE INTERA, dichiarata:")
    print("  R2: S3 sola, cs SPENTO; lato %d, dtau %g, x %g, eps %g; base proiettata; N dtau %g;"
          " gamma = la pendenza della NORMA sulla seconda meta' (e accanto gli autovalori)"
          % (LATO, DTAU, SL.X, T.EPS_MONETA, SL.TEMPO_LUNGO))
    print("  il passo: %d pezzi, impronta %s; la cella 6d complessi (24 reali sul quadrato, 36 sui"
          " triangoli)" % (len(CM.ORDINE), CM.IMPRONTA))
    print("  SN: psi e phi per sqrt(4/6) (rho e Lambda per nodo come il quadrato); SE: le ampiezze di"
          " 594417f6 (per nodo * 6/4)")
    print("  soglie: base <= %g ulp; esatta N*%d ulp; P3 %d ulp; linearita' e C6 %g * max gamma;"
          " STABILE <= %g * %g; banda %s" % (SL.SOGLIA_UNIF, ULP_ESATTA, ULP_P3, SL.BANDA_LIN,
                                            STABILE, RIF_MANDATO, BANDA_PREV))
    print("-" * 100)
    sys.stdout.flush()
    io.open(JSONL, "w", encoding="utf-8").close()

    def salva(b):
        with io.open(JSONL, "a", encoding="utf-8") as f:
            f.write(json.dumps(per_json(b)) + "\n")

    # ------------------------------------------------------------ 1. S3 sui triangoli
    print("### 1. S3 SUI TRIANGOLI: il passo intero (14 pezzi, S3 compreso), cs spento")
    _i, mot, st, par = scena(T.TRIANGOLI, "SE")
    try:
        for _t in range(8):
            SL.passo(st, mot, par, False, (), 0.0)
        gira = None
    except Exception as e:                                    # noqa: BLE001
        gira = "%s: %s" % (type(e).__name__, str(e)[:120])
    if not esito("S3 gira sui triangoli col passo di oggi, senza toccare il codice", gira is None,
                 gira or "8 tick, rho medio %.6f, Lambda medio %.6f"
                 % (float(np.mean(mot.densita_materia(st))), float(np.mean(mot.densita_vuoto(st))))):
        print("### STOP: S3 non gira sui triangoli")
        return 1
    print("-" * 100)

    # ------------------------------------------------------------ 2. i controlli
    print("### 2. I CONTROLLI")
    vecchi = AB.committato()
    t0 = time.time()
    q = braccio_proiettato("R2 lato 32 QUADRATO", T.QUADRATO, "Q", SL.EPS_REL, SL.TEMPO_LUNGO)
    v = vecchi["R2 lato 32"]
    diversi = [c for c in AB.CAMPI if not np.array_equal(np.asarray(q[c]), np.asarray(v[c]))]
    diversi += ["pend." + k for k in v["pend"]
                if not np.array_equal(np.asarray(q["pend"][k]), np.asarray(v["pend"][k]))]
    if not esito("DEVE RIUSCIRE: R2 di 594417f6 AL BIT sul quadrato del costruttore generale",
                 not diversi, ("10 campi identici, %.0f s" % (time.time() - t0)) if not diversi
                 else "### DIVERSI: %s" % ", ".join(diversi)):
        print("### STOP: lo strumento esteso non ripete 594417f6")
        return 1
    salva(q)
    ex = esatta(T.TRIANGOLI)
    tetto = ex["N"] * ULP_ESATTA * EPS
    if not esito("DEVE RIUSCIRE: la camminata sola sui triangoli ESATTA, N dtau 100: <= N*64 ulp",
                 ex["dev"] <= tetto, "%.3e contro %.3e (N %d)" % (ex["dev"], tetto, ex["N"])):
        print("### STOP: il metodo e' rotto sui triangoli")
        return 1
    for br in ("SN", "SE"):
        if not esito("P1 %s: un tick con le cache azzerate = con le cache, AL BIT" % br,
                     prova_p1(T.TRIANGOLI, br)):
            print("### STOP: le cache sono memoria")
            return 1
        u, bit = prova_p3(T.TRIANGOLI, br)
        if not esito("P3 %s: nessuna memoria in mot" % br, bit or u <= ULP_P3,
                     "%s, %.1f ulp" % ("AL BIT" if bit else "non al bit", u)):
            print("### STOP: la funzione di Green ha una memoria in `mot`")
            return 1
    print("-" * 100)

    # ------------------------------------------------------------ 3. i bracci
    print("### 3. R2 SUI TRIANGOLI, I DUE BRACCI")
    bb = {}
    for br, eps_rel in (("SN", SL.EPS_REL), ("SE", SL.EPS_REL), ("SN", EPS_REL_2)):
        nome = "R2 triangoli %s eps %g" % (br, eps_rel)
        b = braccio_proiettato(nome, T.TRIANGOLI, br, eps_rel, SL.TEMPO_LUNGO)
        print("  %-30s rho_m %.6f  Lambda_m %.6f  nu_S3/OMEGA_H %.10f  uniformita' %.1f ulp  %.0f s  %s"
              % (nome, b["rho_m"], b["lambda_m"], b["nu_s3"] / EP.OMEGA_H, b["uniformita_ulp"],
                 b["secondi"], b["fine"]))
        sys.stdout.flush()
        salva(b)
        if b["fine"] != "N":
            print("### STOP: %s" % b["fine"])
            return 1
        bb[(br, eps_rel)] = b
    for br in ("SN", "SE"):
        esito("la base %s: uniformita' <= %g ulp per tutto l'intervallo" % (br, SL.SOGLIA_UNIF),
              bb[(br, SL.EPS_REL)]["uniformita_ulp"] <= SL.SOGLIA_UNIF,
              "%.1f ulp" % bb[(br, SL.EPS_REL)]["uniformita_ulp"])
    g1 = np.asarray(bb[("SN", SL.EPS_REL)]["pend"]["meta_norm"])
    g2 = np.asarray(bb[("SN", EPS_REL_2)]["pend"]["meta_norm"])
    banda = SL.BANDA_LIN * float(np.max(g1))
    dl = float(np.max(np.abs(g1 - g2)))
    esito("DEVE RIUSCIRE: la linearita' su SN, 1e-7 contro 1e-6", dl <= banda,
          "%.3e contro %.3e" % (dl, banda))
    for br in ("SN", "SE"):
        g = np.asarray(bb[(br, SL.EPS_REL)]["pend"]["meta_norm"])
        dr = float(np.max(np.abs(g - ruota60(g))))
        esito("DEVE RIUSCIRE: l'isotropia C6 di gamma(k) sui triangoli, %s" % br,
              dr <= SL.BANDA_LIN * float(np.max(g)),
              "%.3e contro %.3e" % (dr, SL.BANDA_LIN * float(np.max(g))))
    gq = np.asarray(q["pend"]["meta_norm"])
    dq = float(np.max(np.abs(gq - ruota60(gq))))
    esito("DEVE FALLIRE: l'isotropia C6 di gamma(k) sul QUADRATO (594417f6)",
          dq > SL.BANDA_LIN * float(np.max(gq)),
          "%.3e contro %.3e" % (dq, SL.BANDA_LIN * float(np.max(gq))))
    print("-" * 100)

    # ------------------------------------------------------------ 4. le letture
    print("### 4. LE LETTURE (fissate nel task history)")
    kv, lab, Mp, Kp, dmin = zona(LATO)
    print("  la zona esagonale: M %s; K (i piu' vicini ai vertici, a %.4f su |K| %.4f) %s"
          % (sorted(Mp), dmin, 4.0 * np.pi / 3.0, sorted(Kp)))
    h = LATO // 2
    qn, qe = gq, np.asarray(q["pend"]["meta_eig"])
    iq = np.unravel_index(int(np.argmax(qn)), qn.shape)
    print("  QUADRATO: max gamma (norma) %.4f a %s; (autovalori) %.4f; (pi,0) %.4f  (pi,pi) %.4f;"
          " nu_S3/OMEGA_H %.10f" % (float(qn.max()), tuple(int(x) for x in iq), float(qe.max()),
                                    float(qn[h, 0]), float(qn[h, h]), q["nu_s3"] / EP.OMEGA_H))
    letture = {}
    for br in ("SN", "SE"):
        b = bb[(br, SL.EPS_REL)]
        g = np.asarray(b["pend"]["meta_norm"])
        ge = np.asarray(b["pend"]["meta_eig"])
        i = np.unravel_index(int(np.argmax(g)), g.shape)
        dove = lab[i]
        bordo = np.array([[lab[a, c] in ("centro", "M", "K") for c in range(LATO)]
                          for a in range(LATO)])
        gb = np.where(bordo, -np.inf, g)
        ib = np.unravel_index(int(np.argmax(gb)), g.shape)
        mb = float(gb[ib])
        et = {"max": float(g.max()), "dove": dove, "k": [int(x) for x in i],
              "rapporto_norma": float(g.max()) / float(qn.max()),
              "rapporto_mandato": float(g.max()) / RIF_MANDATO,
              "max_eig": float(ge.max()),
              "stabile": float(g.max()) <= STABILE * RIF_MANDATO,
              "banda": mb, "banda_k": [int(x) for x in ib],
              "banda_tiene": BANDA_PREV[0] <= mb <= BANDA_PREV[1],
              "M": {str(k): float(g[k]) for k in sorted(Mp)},
              "K": {str(k): float(g[k]) for k in sorted(Kp)},
              "centro": float(g[0, 0]), "nu_s3_omega": b["nu_s3"] / EP.OMEGA_H}
        letture[br] = et
        print("  %s: max gamma %.4f a %s (%s), |k| %.4f; rapporto col quadrato (norma %.4f) %.4f, col"
              " 0.407 del mandato %.4f; autovalori %.4f" % (br, et["max"], tuple(et["k"]), dove,
                                                            float(np.linalg.norm(kv[i])),
                                                            float(qn.max()), et["rapporto_norma"],
                                                            et["rapporto_mandato"], et["max_eig"]))
        print("      STABILE (max <= %.3e)? %s;  LA BANDA (escluso centro, M, K): %.4f a %s ->"
              " previsione %s-%s %s" % (STABILE * RIF_MANDATO, "SI'" if et["stabile"] else "NO",
                                        mb, tuple(et["banda_k"]), BANDA_PREV[0], BANDA_PREV[1],
                                        "TIENE" if et["banda_tiene"] else "### NON TIENE"))
        print("      IL BORDO: M %s;  K %s;  centro %+.4f;  nu_S3/OMEGA_H %.10f (quadrato %.10f)"
              % ("  ".join("%s %.4f" % (k, v_) for k, v_ in et["M"].items()),
                 "  ".join("%s %.4f" % (k, v_) for k, v_ in et["K"].items()), et["centro"],
                 et["nu_s3_omega"], q["nu_s3"] / EP.OMEGA_H))
        sys.stdout.flush()
    with io.open(JSONL, "a", encoding="utf-8") as f:
        f.write(json.dumps({"letture": letture}) + "\n")
    print("=" * 100)
    print("TRIANGOLI, GRADINO 2: %d su %d   %s" % (OK[0], OK[1], "### TUTTI PASSATI"
                                                   if OK[0] == OK[1] else "### CI SONO BUCHI"))
    print("=" * 100)
    return 0 if OK[0] == OK[1] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
