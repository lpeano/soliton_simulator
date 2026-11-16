# -*- coding: utf-8 -*-
r"""**I PORTI GRANDI: `L 324`** *(Luca `2026-11-15` `12:04`, parte B; la regola della scatola `12:01`; la carta `doc/TASK_HISTORY/2026-11-13_strumento_mattone.md`, sez. `24.4`-`24.6`)*.

    python csv/solitone/porto.py vuoto > doc/referti_l2/mattone/porto_vuoto.txt                                          (B1: i DEVE della scena, la soglia di Gauss)
    python csv/solitone/porto.py cuoci --da 0 --fino 6000 --registro porto-cottura > <scratchpad>/porto_cottura_00000.txt  (B2; se il tetto ferma: --da l'ultimo stato)
    python csv/solitone/porto.py corsa --tipo coppia-fase|coppia-pi|t120|trifoglio|misto --da 0 --fino 6000 --registro porto-<tipo> > <scratchpad>/porto_<tipo>_00000.txt   (B3)
    python csv/solitone/porto.py lettura > doc/referti_l2/mattone/porto_lettura.txt

### **LA SCENA:** **`convergenza.scena_L(324, R_A)`** *(come `L 243`)*; **i DEVE del vuoto di `convergenza_243.controlla_vuoto_senza_cucitura`**; ### **IL BORDO DI OGNI CORSA: `R_A = 2 R_ogg`** *(Luca `13:23`, la correzione n.168: non `3`)*, **`R_ogg` misurato sullo
stato incollato al tick `0`** *(`r_ogg`: attorno al baricentro di TUTTA la materia, `|phi - phi0|` per nodo, la media per anello; il primo raggio oltre l'anello massimo da cui resta sotto il `2%` del massimo fino alla
meta' del lato; R-SCATOLA-1)*; **la regola stampata all'inizio e alla fine** *(R-SCATOLA-2; Luca `13:23`: la distanza al LATO della cella, circa `140` su `L 324`, `>= 3 R_ogg`; `R_A >= 2 R_ogg`; almeno `30` nodi fra `R_A` e il lato; se no la corsa NON parte)*.
### **LA SOGLIA DI GAUSS SU `L 324`** *(`vuoto`)*: **`10` volte il residuo del mattone incollato al tick `0`** *(MIA, dichiarata: la scena vuota non ha un residuo definito)*, **scritta in `porto_gauss.json` PRIMA di ogni corsa.**
### **LA PARTENZA A CALDO** *(7-bis)*: **`CALDO`** *(la decisione A3, sez. `24`: spenta)*; **IL RIUSO DI GAUSS: `GAUSS_RIUSO`** *(Luca `15:07`: acceso, AL BIT)*; **l'interprete stampato** *(R-AMBIENTE)*; **`cs_prec` salvato accanto a ogni stato.** **Gli stati a `k % 1000 == 0` e `950`: ogni ripartenza rifa' `50` tick AL BIT** *(esclusa `h_int`)*.
### **`cuoci`:** **il francobollo di `L 162` al nodo buono piu' vicino al centro del bordo, G+U, Gauss; COTTO quando il picco medio fra le ultime due finestre di `500` tick cambia meno del `2%`** *(controllato ogni
`1000` da `2000`; al piu' `6000`)*; **`cottura_L324_MGU.json`.**
### **`corsa`:** **(coppia-fase, coppia-pi) due francobolli di `L 324` a `d = 35` lungo `A1` attorno al centro del bordo** *(coppia-pi: il secondo per `-1`)*; **(t120, trifoglio, misto) il triangolo di `triangolo_equilatero`,
`(13, 0)`, il lato `39`** *(le fasi: `0, 120, 240`; `0, 0, 0`; `0, 180, 0`)*. **Ogni `50` tick le distanze o i lati, le masse, i raggi, i centri, le CULLE** *(il centro di `|phi - phi0|` sul pezzo di ciascuno)* **e le
distanze fra le culle** *(VERE sul toro)*, **la massa oltre `R_A`; il picco a ogni tick; il giro della fase ogni `100`** *(i triangoli)*; **le mappe ogni `50`, un file ogni `FOTO_FILE` fotogrammi** *(sotto `50 MB`)*;
**Gauss ogni `250`; B4: oltre `R_A` `1e-4` scritto, `1e-2` L'ARRESTO.**
"""
import argparse
import contextlib
import glob
import json
import math
import os
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_CSV = os.path.dirname(_QUI)
for _p in (_QUI, _CSV):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import convergenza as CV  # noqa: E402
import convergenza_243 as C243  # noqa: E402
import gauss_riuso as GR  # noqa: E402
import lapse_caldo as LC  # noqa: E402
import legati as LG  # noqa: E402
import mattone as MT  # noqa: E402
import mattone_cottura as CT  # noqa: E402
import mattone_cottura_U as CU  # noqa: E402
import mattone_rhoc as MR  # noqa: E402
import mattone_triangolo as MTR  # noqa: E402
import triangolo_120 as T120  # noqa: E402
import triangolo_equilatero as TE  # noqa: E402

L = 324                                         # ### Luca B1
R_A_PROVV = 135.0                               # ### la scena si costruisce con questo; ogni corsa lo rimette a 3 R_ogg
SOGLIA_ROGG = 0.02                              # ### R-SCATOLA-1 (Luca 12:01)
SCATOLA_LATO, SCATOLA_BORDO = 3.0, 2.0          # ### R-SCATOLA-1
FATTORE_R_A = 2.0                               # ### Luca 13:23 (n.168 del guardiano): R_A = 2 R_ogg, NON 3
FASCIA_MIN = 30.0                               # ### Luca 13:23: almeno 30 nodi di bordo che assorbe fra R_A e la distanza al lato
FATTORE_GAUSS = 10.0                            # ### MIO, dichiarato
CALDO = False                                   # ### la decisione A3 (sez. 24): si scrive nel commit di questo file
GAUSS_RIUSO = True                              # ### Luca 15:07: AL BIT (prova_gauss.txt, 1d913fd1): il riuso della fattorizzazione per le corse NUOVE
COTTO, MAX_COTTURA, PRIMO_CONTROLLO, OGNI_CONTROLLO = 0.02, 6000, 2000, 1000
D_COPPIA, AB = 35.0, (13, 0)
TIPI = {"coppia-fase": (0.0, 0.0), "coppia-pi": (0.0, math.pi), "t120": T120.FASI, "trifoglio": (0.0, 0.0, 0.0), "misto": (0.0, math.pi, 0.0)}
OGNI, OGNI_GIRO, OGNI_FOTO, FOTO_FILE = 50, 100, 50, 35
OGNI_STATO, PRIMA = 1000, 50
AVVISO, ARRESTO = 1e-4, 1e-2
F_GAUSS = os.path.join(MT.DIR_REF, "porto_gauss.json")
F_COTTURA = os.path.join(MT.DIR_REF, "cottura_L324_MGU.json")
OK = [0, 0]
FALLITE = []


def esito(che, passa, nota):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    if not passa:
        FALLITE.append(che)
    print("  DEVE PASSARE: %-110s %s   %s" % (che[:110], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()


def presidi():
    import _presidio
    if GAUSS_RIUSO:
        GR.accendi()                                            # ### p6_u_breve.gauss_sparso -> la fattorizzazione riusata (in memoria; spenta all'uscita del processo)
        print("### IL RIUSO DELLA FATTORIZZAZIONE DI GAUSS: ACCESO (Luca 15:07; AL BIT, prova_gauss.txt)")
    import sys as _s
    print("### L'INTERPRETE: %s (Python %s); PYTHONNOUSERSITE %s; TMP %s (R-AMBIENTE)" % (_s.executable, _s.version.split()[0], os.environ.get("PYTHONNOUSERSITE"), os.environ.get("TMP")))
    for m in ("convergenza", "convergenza_243", "gauss_riuso", "lapse_caldo", "legati", "mattone", "mattone_cottura", "mattone_cottura_U", "mattone_rhoc", "mattone_triangolo", "triangolo_120", "triangolo_equilatero"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(os.path.join(_CSV, "_u1_prototipo.py"))
    _presidio.avvia(__file__)


@contextlib.contextmanager
def scena():
    with CV.scena_L(L, R_A_PROVV) as Z:
        yield Z


def metti_bordo(Z, R_A):
    from solitone import bordo as BO
    c0 = Z["bordo"]["c0"]
    g_e, gn, _r = BO.g_estremita(Z["z"], c0[0], c0[1], R_A, Z["bordo"]["g_max"])
    Z["g_e"], Z["g_nodo"] = g_e, gn
    Z["bordo"]["R_A"] = float(R_A)
    from solitone import toro as TO
    Z["r_c0"] = np.hypot(*TO.scarti(Z["m1"], Z["m2"], c0[0], c0[1], L).T[:2])


def dphi_nodi(Z, t):
    from solitone import bordo as BO
    n = Z["n"]
    phi0 = BO.c_di(t, Z["tab_c"], Z["K"], Z["omega"]) * Z["phi_v"]
    d = np.sqrt(np.sum(np.abs(Z["st"]["phi_h"] - phi0).reshape(n * 6, -1) ** 2, axis=1))
    return np.sqrt(np.sum(d[Z["righe"]] ** 2, axis=1))


def r_ogg(Z, t):
    """### **R-SCATOLA-1:** `(R_ogg, il baricentro)`: attorno al baricentro di `rho`, la media per anello di `|phi - phi0|`; il primo raggio oltre l'anello massimo da cui resta sotto il `2%` del massimo."""
    from solitone import toro as TO
    rho = MT.rho_di(Z)
    b = TO.centro(rho, Z["m1"], Z["m2"], L)[:2]
    r = np.hypot(*TO.scarti(Z["m1"], Z["m2"], b[0], b[1], L).T[:2])
    dn = dphi_nodi(Z, t)
    an = np.floor(r).astype(int)
    media = np.bincount(an, weights=dn) / np.maximum(np.bincount(an), 1)
    meta = int(TO.meta_periodo(L))
    i_max = int(np.argmax(media[:meta]))
    sotto = media < SOGLIA_ROGG * media[i_max]
    for j in range(i_max + 1, meta):
        if sotto[j:meta].all():
            return float(j), b
    return float("inf"), b


def distanza_lato():
    """### **Luca `13:23`:** la distanza dal centro al lato piu' vicino della cella `L A1`, `L A2` *(il rombo: `area / lato / 2`)*; **e, accanto, la meta' del periodo piu' corto** *(`toro.meta_periodo`: la distanza dalle immagini)*."""
    from solitone import toro as TO
    A1, A2 = TO.vettori()
    a, b = L * A1, L * A2
    area = abs(float(a[0] * b[1] - a[1] * b[0]))
    return min(area / float(np.hypot(*a)), area / float(np.hypot(*b))) / 2.0, TO.meta_periodo(L)


def regola(R, R_A):
    """### **R-SCATOLA** *(Luca `12:01`, `13:23`)*: `(il lato >= 3 R_ogg, R_A >= 2 R_ogg, il lato - R_A >= 30)`."""
    lato, _mp = distanza_lato()
    return lato >= SCATOLA_LATO * R, R_A >= SCATOLA_BORDO * R, lato - R_A >= FASCIA_MIN


def scatola(Z, t, quando):
    R, b = r_ogg(Z, t)
    lato, mp = distanza_lato()
    R_A = Z["bordo"]["R_A"]
    c = regola(R, R_A)
    ok = all(c)
    print("### R-SCATOLA (%s): R_ogg %.1f (il baricentro %.2f, %.2f); la distanza al lato %.2f = %.2f R_ogg (>= %g: %s); R_A %.1f = %.2f R_ogg (>= %g: %s); la fascia %.1f (>= %g: %s); la meta' del periodo %.1f (accanto) -> %s"
          % (quando, R, b[0], b[1], lato, lato / R, SCATOLA_LATO, c[0], R_A, R_A / R, SCATOLA_BORDO, c[1], lato - R_A, FASCIA_MIN, c[2], mp, "RISPETTATA" if ok else "### NON RISPETTATA"))
    return R, ok


def campi(Z, rho_c, e, A=None, E=None):
    import _u1_prototipo as U1
    C = MT.Campi(Z, "MGU", rho_c, e)
    if A is None:
        rho = MT.rho_di(Z)
        C.campo.A[...] = 0.0
        C.campo.E[...] = C.gauss(e * (rho - rho.mean()))
    else:
        C.campo.A[...] = A
        C.campo.E[...] = E
    C.campo.e = e
    C.e_prec = e
    U1.scrivi_U(Z["mot"], C.campo)
    return C


def salva(Z, C, k, t, nome, extra):
    import _vuoto_vivo_B as V
    meta = {"k": k, "t": t, "sha": V.shas(Z["z"]), "codice": "csv/solitone/porto.py", "R_A": Z["bordo"]["R_A"]}
    meta.update(extra)
    cs = LC.cs_prec()
    dati = {x: Z["st"][x] for x in Z["chiavi"]}
    dati.update(campo_A=C.campo.A, campo_E=C.campo.E)
    if cs is not None:
        dati["cs_prec"] = cs
    np.savez(os.path.join(MT.DIR_E, "%s_%05d.npz" % (nome, k)), meta=np.array(json.dumps(meta)), **dati)


def carica(Z, f, rho_c, e):
    with np.load(f) as d:
        Z["metti"]({x: d[x].copy() for x in Z["chiavi"]})
        A, E = d["campo_A"].copy(), d["campo_E"].copy()
        meta = json.loads(str(d["meta"]))
        cs = d["cs_prec"].copy() if "cs_prec" in d.files else None
    metti_bordo(Z, meta["R_A"])
    return campi(Z, rho_c, e, A, E), meta, cs


def soglia_gauss():
    with open(F_GAUSS, encoding="utf-8") as fh:
        return float(json.load(fh)["soglia"])


def accendi(cs):
    if CALDO:
        LC.accendi("caldo", cs)
    else:
        LC.accendi("freddo")


def nodo_buono(fr, tgt):
    """### Il nodo piu' vicino a `tgt` *(indici)* con lo spostamento multiplo di `3` dal centro del francobollo."""
    from solitone import toro as TO
    A1, A2 = TO.vettori()
    best = None
    for n1 in range(int(math.floor(tgt[0])) - 3, int(math.floor(tgt[0])) + 4):
        for n2 in range(int(math.floor(tgt[1])) - 3, int(math.floor(tgt[1])) + 4):
            if (n1 - fr["centro"][0]) % 3 or (n2 - fr["centro"][1]) % 3:
                continue
            p = (n1 - tgt[0]) * A1 + (n2 - tgt[1]) * A2
            dd = float(np.hypot(p[0], p[1]))
            if best is None or dd < best[0]:
                best = (dd, n1 % L, n2 % L)
    return [best[1], best[2]]


def deve_ripartenza(Z, nome, k_da, rho_c, e, t_di, etichette):
    """### Il DEVE: dallo stato a `k_da - 50` *(e il suo `cs_prec`)*, `50` tick = lo stato a `k_da` AL BIT."""
    f_da, f_pr = [os.path.join(MT.DIR_E, "%s_%05d.npz" % (nome, k)) for k in (k_da, k_da - PRIMA)]
    C, meta, cs = carica(Z, f_pr, rho_c, e)
    accendi(cs)
    try:
        R = CT.Corsa(Z, C)
        R.etichette(etichette(meta))
        R.inizio(k_da - PRIMA)
        for k in range(k_da - PRIMA + 1, k_da + 1):
            R.passo(k, t_di(k), 1.0, e)
    finally:
        LC.spegni()
    div = LG.uguale(Z, C, f_da)
    esito("la ripartenza da %s per %d tick = %s AL BIT (esclusa h_int)" % (os.path.basename(f_pr), PRIMA, os.path.basename(f_da)), not div, "diverse: %s" % div)
    return not div


# =====================================================================================
#   B1: LA SCENA E LA SOGLIA DI GAUSS
# =====================================================================================
def vuoto():
    presidi()
    rho_c = MT.rho_c_assoluto()
    e = MT.PB.E_DECISO
    fr = C243.francobollo_L162("MGU", 0)
    t0 = MT.G2.T0
    print("=" * 130)
    print("IL PORTO GRANDE, LA SCENA (Luca 12:04, B1): L %d; il vuoto fresco al tick %d; il mattone di L 162 al centro; R_A = %g R_ogg; la soglia di Gauss = %g volte il residuo iniziale (mia)" % (L, t0, FATTORE_R_A, FATTORE_GAUSS))
    print("=" * 130)
    with scena() as Z:
        from solitone import toro as TO
        print("### la scena: L %d, %d nodi; il centro del bordo %s; la meta' del periodo %.1f; R_A provvisorio %g" % (L, Z["n"], Z["bordo"]["c0"], TO.meta_periodo(L), R_A_PROVV))
        MT.vuoto_fresco(Z, t0)
        e1, e3, nd = C243.controlla_vuoto_senza_cucitura(Z)
        esito("(L %d) il vuoto fresco: |phi_j|^2 = 1 fuori dal bordo (%d nodi) entro %g" % (L, nd, CV.TOLL_VUOTO), e1 <= CV.TOLL_VUOTO, "%.3e" % e1)
        esito("(L %d) il vuoto fresco: lo stesso disegno di fase ogni 3 nodi entro %g (la cucitura esclusa)" % (L, CV.TOLL_VUOTO), e3 <= CV.TOLL_VUOTO, "%.3e" % e3)
        cd = nodo_buono(fr, Z["bordo"]["c0"])
        D = MT.incolla(Z, fr, cd, True)
        R, _b = r_ogg(Z, t0)
        metti_bordo(Z, FATTORE_R_A * R)
        _R, ok = scatola(Z, t0, "il mattone di L 162 incollato")
        esito("R-SCATOLA per il mattone (le tre condizioni, Luca 13:23)", ok, "R_ogg %.1f" % R)
        C = campi(Z, rho_c, e)
        g0 = C.residuo()
        Z["metti"]()
    s = FATTORE_GAUSS * g0
    with open(F_GAUSS, "w", encoding="utf-8", newline=chr(10)) as fh:
        json.dump({"L": L, "r0": g0, "soglia": s, "fattore": FATTORE_GAUSS, "R_ogg_mattone": R, "R_A": FATTORE_R_A * R, "incollato": cd, "Delta": D, "codice": "csv/solitone/porto.py"}, fh, indent=1)
    print("### incollato a %s (Delta %.6f); R_ogg %.1f, R_A %.1f; IL RESIDUO DI GAUSS INIZIALE %.3e -> LA SOGLIA SU L %d %.3e (%g volte, mia); %s" % (cd, D, R, FATTORE_R_A * R, g0, L, s, FATTORE_GAUSS, F_GAUSS))
    print("=" * 130)
    print("ESITO: %d/%d controlli come devono; fallite %s" % (OK[0], OK[1], FALLITE))
    return 0 if not FALLITE else 1


# =====================================================================================
#   B2: LA COTTURA SU L 324
# =====================================================================================
def cuoci(k_da, k_fino, reg):
    presidi()
    t00 = time.time()
    rho_c = MT.rho_c_assoluto()
    e = MT.PB.E_DECISO
    t0 = MT.G2.T0
    soglia = soglia_gauss()
    nome = "porto_cottura"
    print("=" * 130)
    print("IL PORTO GRANDE, LA COTTURA (Luca 12:04, B2): da k %d a k %d; COTTO se il picco medio fra le ultime due finestre di 500 cambia meno del %g (ogni %d da %d, al piu' %d); Gauss sotto %.3e; CALDO %s"
          % (k_da, k_fino, COTTO, OGNI_CONTROLLO, PRIMO_CONTROLLO, MAX_COTTURA, soglia, CALDO))
    print("=" * 130)
    fr = C243.francobollo_L162("MGU", 0) if k_da == 0 else None
    PK = {"k": [], "picco": []}
    for f in sorted(glob.glob(os.path.join(MT.DIR_REF, "porto_cottura_serie_*.npz"))):
        s = np.load(f)
        for a, b in zip(s["pk_k"], s["picco"]):
            if int(a) <= k_da and (not PK["k"] or a > PK["k"][-1]):
                PK["k"].append(int(a))
                PK["picco"].append(float(b))
    with scena() as Z:
        if k_da == 0:
            MT.vuoto_fresco(Z, t0)
            cd = nodo_buono(fr, Z["bordo"]["c0"])
            MT.incolla(Z, fr, cd, True)
            R, _b = r_ogg(Z, t0)
            metti_bordo(Z, FATTORE_R_A * R)
            if not all(regola(R, FATTORE_R_A * R)):
                scatola(Z, t0, "PRIMA della cottura")
                print("### LA COTTURA NON PARTE: R-SCATOLA non rispettata (Luca 13:23: FERMO solo di questa corsa)")
                return 1
            C = campi(Z, rho_c, e)
            cs = None
        else:
            if not deve_ripartenza(Z, nome, k_da, rho_c, e, lambda k: t0 + k, lambda m: [m["centro"]]):
                print("ESITO: ### FERMO: la ripartenza NON e' esatta")
                return 1
            C, _m, cs = carica(Z, os.path.join(MT.DIR_E, "%s_%05d.npz" % (nome, k_da)), rho_c, e)
        scatola(Z, t0 + k_da, "all'inizio")
        S = {x: [] for x in ("pk_k", "picco", "k", "raggio", "M", "c1", "c2", "fuori", "gauss_k", "gauss")}
        accendi(cs)
        fine = "finita"
        cotto = None
        try:
            R = CT.Corsa(Z, C)
            rho = MT.rho_di(Z)
            c = MT.centro_di(Z, rho)
            R.etichette([c])
            R.inizio(k_da)
            t1 = t_tappa = time.time()
            for k in range(k_da, k_fino + 1):
                if k > k_da:
                    R.passo(k, t0 + k, 1.0, e)
                rho = MT.rho_di(Z)
                c = MT.centro_di(Z, rho)
                S["pk_k"].append(k)
                S["picco"].append(float(rho.max()))
                if k > k_da or k_da == 0:
                    PK["k"].append(k)
                    PK["picco"].append(float(rho.max()))
                if (k - k_da) % CT.OGNI == 0:
                    R.etichette([c])
                if k % OGNI == 0:
                    S["k"].append(k)
                    S["raggio"].append(MR.raggio(Z, rho, c))
                    S["M"].append(float(rho.sum()))
                    S["c1"].append(c[0])
                    S["c2"].append(c[1])
                    S["fuori"].append(float(rho[Z["r_c0"] > Z["bordo"]["R_A"]].sum() / rho.sum()))
                if k % MT.OGNI_GAUSS == 0:
                    S["gauss_k"].append(k)
                    S["gauss"].append(C.residuo())
                if k % 250 == 0:
                    print("    k %5d  il picco %.4e  il raggio %.4f  la massa %.10e  oltre R_A %.3e  Gauss %s  (%.0f s)" % (k, S["picco"][-1], S["raggio"][-1], S["M"][-1], S["fuori"][-1],
                          "%.2e" % S["gauss"][-1] if S["gauss_k"] and S["gauss_k"][-1] == k else "--", time.time() - t00))
                    sys.stdout.flush()
                if k > k_da and (k % OGNI_STATO == 0 or k % OGNI_STATO == OGNI_STATO - PRIMA):
                    salva(Z, C, k, t0 + k, nome, {"centro": [float(c[0]), float(c[1])]})
                if k > k_da and k >= PRIMO_CONTROLLO and k % OGNI_CONTROLLO == 0:
                    pk = dict(zip(PK["k"], PK["picco"]))
                    p1 = float(np.mean([pk[j] for j in range(k - 999, k - 499)]))
                    p2 = float(np.mean([pk[j] for j in range(k - 499, k + 1)]))
                    cotto = abs(p2 - p1) / p1 < COTTO
                    print("### LA COTTURA a k %d: il picco medio %d-%d %.4e, %d-%d %.4e: %.4f (la soglia %g) -> %s" % (k, k - 999, k - 500, p1, k - 499, k, p2, abs(p2 - p1) / p1, COTTO, "COTTO" if cotto else "non ancora"))
                    sys.stdout.flush()
                    if cotto:
                        with open(F_COTTURA, "w", encoding="utf-8", newline=chr(10)) as fh:
                            json.dump({"caso": "MGU", "L": L, "k": k, "t": t0 + k, "file": os.path.join(MT.DIR_E, "%s_%05d.npz" % (nome, k)), "cotto": True, "picchi": [p1, p2],
                                       "raggio": S["raggio"][-1], "codice": "csv/solitone/porto.py"}, fh, indent=1)
                        fine = "COTTO a k %d" % k
                        break
                adesso = time.time()
                if reg and adesso - t_tappa >= MT.TAPPA_S:
                    MT.tappa(reg, "k %d; %.3f s per tick; la memoria libera %.2f GB" % (k, (adesso - t1) / max(1, k - k_da), MT.memoria_gb()))
                    t_tappa = adesso
                if adesso - t1 > MT.TETTO_S:
                    fine = "il tetto di %g s a k %d (si riparte da %d)" % (MT.TETTO_S, k, (k // OGNI_STATO) * OGNI_STATO)
                    break
            giri = list(LC.STATO["giri"])
        finally:
            LC.spegni()
        print("-" * 130)
        print("### %d tick in %.0f s (%.3f s per tick); %s; i giri del punto fisso: la media %.4f" % (k - k_da, time.time() - t1, (time.time() - t1) / max(1, k - k_da), fine, float(np.mean(giri)) if giri else float("nan")))
        R.tabella(["sol"])
        scatola(Z, t0 + k, "alla fine")
        Z["metti"]()
    np.savez_compressed(os.path.join(MT.DIR_REF, "porto_cottura_serie_%05d.npz" % k_da), **{x: np.array(v) for x, v in S.items()})
    g = np.array(S["gauss"])
    esito("Gauss sotto la soglia di L %d (%.3e) a ogni controllo" % (L, soglia), len(g) > 0 and float(g.max()) < soglia, "il massimo %.3e" % (float(g.max()) if len(g) else float("nan")))
    if cotto is False and k >= MAX_COTTURA:
        print("### NON COTTO entro %d tick" % MAX_COTTURA)
    print("=" * 130)
    print("ESITO: %d/%d controlli come devono; fallite %s; %s; %.0f s in tutto" % (OK[0], OK[1], FALLITE, fine, time.time() - t00))
    return 0 if not FALLITE else 1


# =====================================================================================
#   B3: LE CORSE
# =====================================================================================
def francobollo_L324():
    """### Il mattone cotto su `L 324` *(`cottura_L324_MGU.json`)*, ritagliato nella scena di `L 324`."""
    with open(F_COTTURA, encoding="utf-8") as fh:
        ct = json.load(fh)
    assert ct["cotto"]
    with scena() as Z:
        with np.load(ct["file"]) as d:
            Z["metti"]({x: d[x] for x in Z["chiavi"]})
        rho = MT.rho_di(Z)
        c = MT.centro_di(Z, rho)
        st = {x: Z["st"][x].copy() for x in Z["chiavi"]}
        MT.vuoto_fresco(Z, int(ct["t"]))
        phi_rif = Z["st"]["phi_h"].copy()
        Z["metti"](st)
        fr = MT.ritaglia(Z, c, phi_rif)
        fr["file"] = ct["file"]
        Z["metti"]()
    return fr


def posti_tipo(tipo, fr, c0):
    from solitone import toro as TO
    if tipo.startswith("coppia"):
        A1, _A2 = TO.vettori()
        return [nodo_buono(fr, (c0[0] + s * 0.5 * D_COPPIA, c0[1])) for s in (-1.0, 1.0)]       # ### lungo A1: A1 = (1, 0) negli indici
    a, b = AB
    ra, rb = TE.R(a, b)
    P = nodo_buono(fr, (c0[0] - (a + ra), c0[1] - (b + rb)))
    return TE.vertici(P, a, b, L)


def corsa(tipo, k_da, k_fino, reg):
    from solitone import carta_coppia as CC
    from solitone import toro as TO
    presidi()
    t00 = time.time()
    rho_c = MT.rho_c_assoluto()
    e = MT.PB.E_DECISO
    t0 = MT.G2.T0
    soglia = soglia_gauss()
    fasi = TIPI[tipo]
    nsol = len(fasi)
    nome = "porto_%s" % tipo
    print("=" * 130)
    print("IL PORTO GRANDE, LA CORSA %s (Luca 12:04, B3): da k %d a k %d; L %d; le fasi %s; Gauss sotto %.3e; CALDO %s; il tetto %g s" % (tipo, k_da, k_fino, L, ["%.1f" % math.degrees(f) for f in fasi], soglia, CALDO, MT.TETTO_S))
    print("=" * 130)
    fr = francobollo_L324() if k_da == 0 else None
    with scena() as Z:
        m1, m2 = Z["m1"], Z["m2"]
        c0 = Z["bordo"]["c0"]
        xs = TO.scarti(m1, m2, c0[0], c0[1], L)[:, 0]

        def centri_di(rho, prec):
            if tipo.startswith("coppia"):
                a, b = CC.centri_semipiani(rho, m1, m2, L, xs, 0.0)
                return [list(map(float, a)), list(map(float, b))], None
            cen, lab = MTR.centri_pezzi(Z, rho, prec)
            return [list(map(float, c)) for c in cen], lab
        if k_da == 0:
            V = posti_tipo(tipo, fr, c0)
            MT.vuoto_fresco(Z, t0)
            phi_F3 = Z["st"]["phi_h"].copy()
            vuoto0 = {x: Z["st"][x].copy() for x in Z["chiavi"]}
            soli, masse = [], []
            for j, cpos in enumerate(V):
                for x in Z["chiavi"]:
                    Z["st"][x][...] = vuoto0[x]
                MT.incolla(Z, fr, cpos, True)
                if fasi[j] != 0.0:
                    Z["st"]["psi_h"][...] = Z["st"]["psi_h"] * np.exp(1j * fasi[j])
                soli.append((Z["st"]["psi_h"].copy(), Z["st"]["phi_h"].copy()))
                masse.append(float(np.sum(np.abs(soli[-1][0]) ** 2)))
            psi, phi = soli[0][0].copy(), soli[0][1].copy()
            for s_ in soli[1:]:
                psi = psi + s_[0]
                phi = phi * (s_[1] / phi_F3)
            Z["st"]["psi_h"][...] = psi
            Z["st"]["phi_h"][...] = phi
            R0, _b = r_ogg(Z, t0)
            metti_bordo(Z, FATTORE_R_A * R0)
            if not all(regola(R0, FATTORE_R_A * R0)):
                scatola(Z, t0, "PRIMA della corsa")
                print("### LA CORSA NON PARTE: R-SCATOLA non rispettata (Luca 13:23: FERMO solo di questa corsa)")
                return 1
            C = campi(Z, rho_c, e)
            cs = None
            lati = [MT.distanza(L, V[a], V[b]) for a, b in ((0, 1), (1, 2), (2, 0))] if nsol == 3 else [MT.distanza(L, V[0], V[1])]
            print("### i posti %s; le distanze vere %s; le masse dei francobolli da soli %s; R_ogg %.1f, R_A %.1f" % (V, ["%.6f" % x for x in lati], ["%.15e" % m for m in masse], R0, FATTORE_R_A * R0))
            esito("le masse dei francobolli da soli uguali entro 1e-10 relativo", (max(masse) - min(masse)) / max(masse) <= 1e-10, "%.3e" % ((max(masse) - min(masse)) / max(masse)))
            if nsol == 3:
                esito("i tre lati uguali entro 1e-9 (il lato atteso %.6f)" % TE.lato(*AB), max(lati) - min(lati) <= 1e-9 and abs(lati[0] - TE.lato(*AB)) <= 1e-9, "max - min %.3e" % (max(lati) - min(lati)))
            cen = [list(map(float, v)) for v in V]
        else:
            if not deve_ripartenza(Z, nome, k_da, rho_c, e, lambda k: t0 + k, lambda m: m["centri"]):
                print("ESITO: ### FERMO: la ripartenza NON e' esatta")
                return 1
            C, meta, cs = carica(Z, os.path.join(MT.DIR_E, "%s_%05d.npz" % (nome, k_da)), rho_c, e)
            cen = meta["centri"]
        R_ini, _ok = scatola(Z, t0 + k_da, "all'inizio")
        S = {x: [] for x in ("k", "gauss_k", "gauss", "fuori") + tuple("%s_%d" % (q, j) for q in ("M", "raggio", "c1", "c2", "u1", "u2") for j in range(nsol))
             + tuple("d_%d%d" % ij for ij in ((0, 1), (1, 2), (2, 0))[:(3 if nsol == 3 else 1)]) + tuple("du_%d%d" % ij for ij in ((0, 1), (1, 2), (2, 0))[:(3 if nsol == 3 else 1)])}
        G = {"k": [], "grande": [], "somma": [], "dens": [], "comp": []}
        PK = [[] for _j in range(nsol)]
        MP = {"k": [], "rho": [], "dphi": [], "E": [], "centri": []}
        pezzo = [0]
        st_ = {"cen": cen}

        def scarica_mappe():
            if not MP["k"]:
                return
            geo = T120.geometria(Z)
            f = os.path.join(MT.DIR_REF, "porto_%s_mappe_%05d_%02d.npz" % (tipo, k_da, pezzo[0]))
            np.savez_compressed(f, tick=np.array(MP["k"], dtype=np.int32), rho=np.stack(MP["rho"]), dphi=np.stack(MP["dphi"]), E=np.stack(MP["E"]), centri=np.stack(MP["centri"]), **geo)
            print("    [mappe] %d fotogrammi (k %d ... %d) in %s, %.1f MB" % (len(MP["k"]), MP["k"][0], MP["k"][-1], os.path.basename(f), os.path.getsize(f) / 1e6))
            for x in MP:
                MP[x] = []
            pezzo[0] += 1

        def misura(k, R):
            rho = MT.rho_di(Z)
            cen, lab = centri_di(rho, st_["cen"])
            st_["cen"] = cen
            if lab is None:
                from conti import etichette as ETI
                lab = ETI(Z, cen)
            for j in range(nsol):
                sel = lab == j
                PK[j].append(float(rho[sel].max()) if sel.any() else float("nan"))
            fare = k % OGNI == 0
            if fare or k % OGNI_FOTO == 0:
                dn = dphi_nodi(Z, t0 + k)
            if fare:
                S["k"].append(k)
                culle = []
                for j in range(nsol):
                    sel = lab == j
                    S["M_%d" % j].append(float(rho[sel].sum()))
                    S["raggio_%d" % j].append(MR.raggio(Z, rho, cen[j]))
                    S["c1_%d" % j].append(cen[j][0])
                    S["c2_%d" % j].append(cen[j][1])
                    u = TO.centro(np.where(sel, dn, 0.0), m1, m2, L)[:2]
                    culle.append(u)
                    S["u1_%d" % j].append(float(u[0]))
                    S["u2_%d" % j].append(float(u[1]))
                for a, b in ((0, 1), (1, 2), (2, 0))[:(3 if nsol == 3 else 1)]:
                    S["d_%d%d" % (a, b)].append(MT.distanza(L, cen[a], cen[b]))
                    S["du_%d%d" % (a, b)].append(MT.distanza(L, culle[a], culle[b]))
                S["fuori"].append(float(rho[Z["r_c0"] > Z["bordo"]["R_A"]].sum() / rho.sum()))
            if k % MT.OGNI_GAUSS == 0:
                S["gauss_k"].append(k)
                S["gauss"].append(C.residuo())
            if nsol == 3 and k % OGNI_GIRO == 0:
                g, grande, gs, dens, _r = T120.misura_dentro(Z, cen)
                G["k"].append(k)
                G["grande"].append(float(g[grande]))
                G["somma"].append(gs)
                G["dens"].append(dens)
                G["comp"].append(g)
            if k % OGNI_FOTO == 0:
                MP["k"].append(k)
                MP["rho"].append(rho.astype(np.float32))
                MP["dphi"].append(dn.astype(np.float32))
                MP["E"].append(np.sqrt(np.sum(C.campo.E.reshape(Z["n"], 3) ** 2, axis=1)).astype(np.float32))
                MP["centri"].append(np.array(cen, dtype=np.float32))
                if len(MP["k"]) >= FOTO_FILE:
                    scarica_mappe()
            if fare and k % 250 == 0:
                dd = " ".join("%.4f" % S[x][-1] for x in S if x.startswith("d_"))
                du = " ".join("%.4f" % S[x][-1] for x in S if x.startswith("du_"))
                print("    k %5d  d %s  le culle %s  masse %s  raggi %s  oltre R_A %.3e%s  Gauss %s%s  (%.0f s)" % (k, dd, du, " ".join("%.6e" % S["M_%d" % j][-1] for j in range(nsol)),
                      " ".join("%.4f" % S["raggio_%d" % j][-1] for j in range(nsol)), S["fuori"][-1], "  ### OLTRE %g (B4)" % AVVISO if S["fuori"][-1] > AVVISO else "",
                      "%.2e" % S["gauss"][-1] if S["gauss_k"] and S["gauss_k"][-1] == k else "--", ("  il giro %+.2f, la somma %+.2f, la densita' al centro %.4e" % (G["grande"][-1], G["somma"][-1], G["dens"][-1])) if G["k"] and G["k"][-1] == k else "",
                      time.time() - t00))
                sys.stdout.flush()
            if k > k_da and (k % OGNI_STATO == 0 or k % OGNI_STATO == OGNI_STATO - PRIMA):
                salva(Z, C, k, t0 + k, nome, {"centri": cen})
        accendi(cs)
        fine = "finita"
        try:
            R = CT.Corsa(Z, C)
            R.etichette(st_["cen"])
            R.inizio(k_da)
            misura(k_da, R)
            if k_da == 0 and nsol == 3:
                g0 = G["grande"][0]
                print("### il giro al tick 0: la componente piu' grande %+.6f; la somma %+.6f; le 12 %s" % (g0, G["somma"][0], " ".join("%+.0f" % x for x in G["comp"][0])))
                if tipo == "t120":
                    esito("il giro della componente piu' grande al tick 0 = +1", abs(g0 - 1.0) < 1e-9, "%+.6f" % g0)
            if FALLITE:
                print("ESITO: ### FERMO: un DEVE del tick 0 fallisce (%s)" % FALLITE)
                return 1
            t1 = t_tappa = time.time()
            for k in range(k_da + 1, k_fino + 1):
                R.passo(k, t0 + k, 1.0, e)
                if (k - k_da) % CT.OGNI == 0:
                    R.etichette(st_["cen"])
                misura(k, R)
                adesso = time.time()
                if reg and adesso - t_tappa >= MT.TAPPA_S:
                    MT.tappa(reg, "k %d; %.3f s per tick; la memoria libera %.2f GB" % (k, (adesso - t1) / (k - k_da), MT.memoria_gb()))
                    t_tappa = adesso
                if S["fuori"] and S["fuori"][-1] > ARRESTO:
                    fine = "L'ARRESTO (B4): la massa oltre R_A %.3e > %g a k %d" % (S["fuori"][-1], ARRESTO, k)
                    break
                if adesso - t1 > MT.TETTO_S:
                    fine = "il tetto di %g s a k %d (si riparte da %d)" % (MT.TETTO_S, k, (k // OGNI_STATO) * OGNI_STATO)
                    break
            giri = list(LC.STATO["giri"])
        finally:
            LC.spegni()
        scarica_mappe()
        print("-" * 130)
        print("### %d tick in %.0f s (%.3f s per tick); %s; i giri del punto fisso: la media %.4f" % (k - k_da, time.time() - t1, (time.time() - t1) / max(1, k - k_da), fine, float(np.mean(giri)) if giri else float("nan")))
        R.tabella(["ABC"[j] for j in range(nsol)])
        R_fin, _ok = scatola(Z, t0 + k, "alla fine")
        Z["metti"]()
    np.savez_compressed(os.path.join(MT.DIR_REF, "porto_%s_serie_%05d.npz" % (tipo, k_da)), **{("picco_%d" % j): np.array(v) for j, v in enumerate(PK)}, **{x: np.array(v) for x, v in S.items()})
    if G["k"]:
        np.savez_compressed(os.path.join(MT.DIR_REF, "porto_%s_giro_%05d.npz" % (tipo, k_da)), **{x: np.array(v) for x, v in G.items()})
    # ---------------------------------------------------------------- R-CONTI-2: la tabella delle forze (finestre di 500 tick)
    kk = np.array(S["k"], dtype=float)
    dm = np.mean([np.array(S[x]) for x in S if x.startswith("d_")], axis=0)
    print("### LA TABELLA DELLE FORZE (R-CONTI-2; la distanza media fra i centri, finestre di 500 tick): d, d'' (la parabola)")
    for a in range(int(kk[0]), int(kk[-1]), 500):
        j = (kk >= a) & (kk <= a + 500)
        if j.sum() >= 5:
            acc, ea = CC.curvatura(kk[j], dm[j])
            print("    tick %5d-%5d: d da %.6f a %.6f; d'' %+.4e +- %.1e (%.1f errori)" % (a, a + 500, dm[j][0], dm[j][-1], acc, ea, abs(acc) / ea if ea else float("inf")))
    g = np.array(S["gauss"])
    esito("Gauss sotto la soglia di L %d (%.3e) a ogni controllo" % (L, soglia), len(g) > 0 and float(g.max()) < soglia, "il massimo %.3e" % (float(g.max()) if len(g) else float("nan")))
    print("=" * 130)
    print("ESITO: %d/%d controlli come devono; fallite %s; %s; %.0f s in tutto" % (OK[0], OK[1], FALLITE, fine, time.time() - t00))
    return 0 if not FALLITE else 1


# =====================================================================================
#   LA LETTURA (B4)
# =====================================================================================
def lettura():
    import _presidio
    _presidio.avvia(__file__)
    print("=" * 130)
    print("IL PORTO GRANDE, LA LETTURA (Luca 12:04, B4): le previsioni P1, P2', P3, P4; le inversioni come legati.py (la serie lisciata, 11 punti, +- 1000 tick)")
    print("=" * 130)
    for tipo in TIPI:
        pz = sorted(glob.glob(os.path.join(MT.DIR_REF, "porto_%s_serie_*.npz" % tipo)))
        if not pz:
            print("### %s: nessuna serie" % tipo)
            continue
        nsol = len(TIPI[tipo])
        pd, pu, s0, s1 = [], [], np.load(pz[0]), np.load(pz[-1])
        for f in pz:
            s = np.load(f)
            pd.append((s["k"], np.mean([s[x] for x in s.files if x.startswith("d_")], axis=0)))
            pu.append((s["k"], np.mean([s[x] for x in s.files if x.startswith("du_")], axis=0)))
        k, dm = LG.serie_unita(pd)
        _k, du = LG.serie_unita(pu)
        print("### %s (i pezzi %s)" % (tipo, [os.path.basename(f) for f in pz]))
        inv = LG.leggi_inversioni("la distanza media fra i centri", k, dm)
        print("      la distanza media fra le culle da %.4f a %.4f" % (du[0], du[-1]))
        for j in range(nsol):
            dc = MT.distanza(L, (s0["c1_%d" % j][0], s0["c2_%d" % j][0]), (s1["c1_%d" % j][-1], s1["c2_%d" % j][-1]))
            dcu = MT.distanza(L, (s0["u1_%d" % j][0], s0["u2_%d" % j][0]), (s1["u1_%d" % j][-1], s1["u2_%d" % j][-1]))
            print("      (P4) il solitone %d si sposta di %.4f, la sua culla di %.4f -> %s" % (j, dc, dcu, "LA CULLA FERMA (meno di un quarto)" if dcu < 0.25 * dc else "### la culla si muove"))
        mx = [x for x in inv if x[2] == "max"]
        if tipo == "coppia-fase":
            print("    (P1) OSCILLA: le inversioni %d -> %s" % (len(inv), "CONFERMATA" if len(inv) >= 2 else "### NON CONFERMATA: una SORPRESA"))
        if tipo == "coppia-pi":
            print("    (P2') si allontana e NON torna: %s -> %s" % ("nessun massimo" if not mx else "il primo massimo %.3f a k %d" % (mx[0][1], mx[0][0]),
                  "CONFERMATA" if (not mx and dm[-1] >= dm.max() - 1e-12) else "### NON CONFERMATA: una SORPRESA"))
        if tipo == "t120":
            print("    (P3) SI ALLARGA: %s (da %.4f a %.4f); NESSUNA fusione: il minimo %.4f" % ("si'" if dm[-1] > dm[0] else "### NO", dm[0], dm[-1], dm.min()))
            gz = sorted(glob.glob(os.path.join(MT.DIR_REF, "porto_t120_giro_*.npz")))
            gg = np.concatenate([np.load(f)["grande"] for f in gz]) if gz else np.array([])
            print("    (P3) IL VORTICE: il giro della piu' grande %s" % ("RESTA +1" if len(gg) and np.all(np.rint(gg) == 1) else "### NON resta +1"))
    print("=" * 130)
    return 0


def main(argv):
    if argv and argv[0] == "vuoto":
        return vuoto()
    if argv and argv[0] == "lettura":
        return lettura()
    ap = argparse.ArgumentParser()
    ap.add_argument("azione", choices=("cuoci", "corsa"))
    ap.add_argument("--tipo", choices=sorted(TIPI))
    ap.add_argument("--da", type=int, required=True)
    ap.add_argument("--fino", type=int, required=True)
    ap.add_argument("--registro")
    x = ap.parse_args(argv)
    if x.azione == "cuoci":
        return cuoci(x.da, min(x.fino, MAX_COTTURA), x.registro)
    assert x.tipo, "--tipo"
    return corsa(x.tipo, x.da, x.fino, x.registro)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
