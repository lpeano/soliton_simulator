# -*- coding: utf-8 -*-
r"""**LA CORSA MITOSI CON LE NASCITE, E LE SUE PROVE** *(il ramo `mitosi`; Luca `2026-11-20` `16:37`, `17:08`; la carta `doc/TASK_HISTORY/2026-11-20_covariante_di_stella.md` del ramo `primo-ordine`, sez. `10`-`12`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/mitosi_lunga.py nasce > doc/referti_l2/mitosi_nasce.txt
    E:\python\py3132\python.exe doc/referti_l2/mitosi_lunga.py p8 > doc/referti_l2/mitosi_p8.txt
    E:\python\py3132\python.exe doc/referti_l2/mitosi_lunga.py corsa --nome MITOSI --da 3000 --fino K --nascite si --registro <voce>

**Il passo** = il passo di C2 *(`controllo_senza_bordo.corsa_senza_bordo`: P6.0 lo prova al bit con quello di MITOSI)*, poi **`Theta`**, poi **se un arco e' scattato, UNA nascita** *(D-M4)*: **l'arco scattato di indice MINORE** *(la carta della mitosi sez. `7`; gli altri aspettano col loro `Theta`)*, **la regola intera** *(`mitosi_regola.regola`, `applica`)*, `E_persa -= DH`, il bilancio stampato, **P9 controllato a ogni nascita** *(se cade: FERMO)*. **`--nascite no`: il ramo C2-EXT** *(lo stesso codice: il TRONCO COMUNE)*.
**Le misure** *(quelle di C2, `controllo_senza_bordo.Misure`, ogni `OGNI` tick)*: **dopo la crescita `r` dalle posizioni** *(B4)* **e gli archi dal grafo nuovo**; **`R_ogg` al `5%` NON e' definito dalla prima nascita** *(usa `righe` e il vuoto di riferimento del bordo, della taglia vecchia: `nan`, dichiarato)*; **in piu' D1 ed E1 in passi** *(`passi`: le righe di `doc/referti_l2/distanza_passi.py` del ramo `primo-ordine`, `1fe8df14`; gli anelli `40` e `60` dei nodi ORIGINARI, fissati dalle posizioni di partenza; la sorgente il nodo piu' vicino al baricentro)*.
**Lo stato salvato** *(ogni `OGNI_STATO` tick; e lo stato PRIMA della prima nascita, `prima_nascita_<k>.npz`: il punto da cui riparte il ramo C2-EXT)*: le chiavi, `A`, `E`, `cs_prec`, `theta_a`, `E_persa`; **dopo la prima nascita anche il grafo** *(`ii`, `jj`, i versori, i vettori d'arco del campo, le posizioni)*. **La ripresa:** il toro della scena cresciuto in UNA crescita fino al grafo salvato *(i sopravvissuti del toro per primi nell'ordine, poi gli altri: l'ordine che `Incidenza.cresci` conserva; CONTROLLATO)*, poi i valori salvati.

**`nasce`** *(la carta sez. `10.3`: N e P6.1; e il costo)*: da C2 a `k 3000`, un tick, **la nascita FORZATA** sul primo arco nell'ordine di scatto, poi `20` tick: **il tick gira; `M` e `V` contro i `20` tick senza nascita dallo stesso stato** *(entro `10` volte, o `1e-13`)*; **Gauss** sotto `10` volte il residuo di prima; **le misure della corsa** girano sul grafo cresciuto; **P6.1:** dopo UN tick, nato contro non nato, **la differenza per anello in passi dal nodo nuovo** *(`psi`, `phi` per nodo; `E` per arco prima e dopo il tick; NESSUNA soglia)*; **il costo:** il tick prima e dopo, la nascita.
**`p8`:** **`10` tick con la nascita forzata al primo, di fila, contro `5` + salva + riprendi + `5`**: ogni chiave, `A`, `E`, `cs_prec`, il grafo, i versori, `Theta`, le posizioni, `E_persa` AL BIT; **DEVE FALLIRE:** un byte dello stato salvato cambiato -> la ripresa RIFIUTA *(lo sha1)*.
"""
import hashlib
import json
import os
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import mitosi_regola as MR  # noqa: E402

MC, PS = MR.MC, MR.PS
CSB = MC.CSB
DIR = os.path.join("E:" + os.sep, "soliton_simulator", "controllo")
OGNI, OGNI_STATO = 50, 250
ANELLI = (40.0, 60.0)
N_DOPO = 20
N_P8, K_P8 = 10, 5


# ------------------------------------------------------------------------------------------ i passi (distanza_passi.py, 1fe8df14)
def passi(ii, jj, n, sorgente):
    import scipy.sparse as sp
    from scipy.sparse import csgraph
    A = sp.csr_matrix((np.ones(2 * len(ii)), (np.concatenate([ii, jj]), np.concatenate([jj, ii]))), shape=(n, n))
    d = csgraph.shortest_path(A, unweighted=True, indices=int(sorgente))
    assert np.all(np.isfinite(d)), "il grafo non e' connesso"
    return d.astype(np.int64)


def scala(d, rho):
    o = np.argsort(d, kind="stable")
    cum = np.cumsum(rho[o]) / float(np.sum(rho))
    r50, r90 = int(d[o][np.searchsorted(cum, 0.5)]), int(d[o][np.searchsorted(cum, 0.9)])
    w = float(np.sqrt(np.sum(rho * d.astype(float) ** 2) / np.sum(rho)))
    return r50, r90, w


def raggi(Z, c):
    from solitone import toro as TO
    return np.hypot(*TO.scarti(np.asarray(Z["m1"], dtype=float), np.asarray(Z["m2"], dtype=float), c[0], c[1], Z["L"]).T[:2])


# ------------------------------------------------------------------------------------------ il passo con le nascite
class Nascite(object):
    """### Il contatore, `E_persa`, il registro delle nascite; `passo_dopo(Z, C, k)` dopo il passo di C2."""

    def __init__(self, cont, e_persa, nascite, accese):
        self.cont, self.e_persa, self.nascite, self.accese = cont, float(e_persa), int(nascite), bool(accese)
        self.bilanci = []
        self.prima = None

    def nasci(self, Z, C, a, k, perche):
        t1 = time.time()
        H0 = MR.energia_corsa(Z, C)
        R, S = MR.regola(Z, C, int(a), "stella")
        inf = MR.applica(Z, C, self.cont, S)
        H1 = MR.energia_corsa(Z, C)
        d9 = abs(H1 - S["H"]) / abs(S["H"])
        self.e_persa -= (H1 - H0)
        self.nascite += 1
        nd = R["nodi"]
        b = {"k": int(k), "a": int(a), "perche": perche, "nodi": {x: int(v) for x, v in nd.items()}, "scelto": int(R["scelto"]), "gap": float(R["gap"]),
             "DH_nascita": float(R["H_nascita"] - H0), "DH_flip": float(S["H"] - R["H_nascita"]) if R["scelto"] >= 0 else 0.0, "DH": float(H1 - H0), "P9": float(d9),
             "res": float(S["res"]), "E_persa": self.e_persa, "t": time.time() - t1, "ok": bool(inf["ok_fuori"] and inf["ok_geo"] and inf["ok_U"]),
             "pos": [float(Z["m1"][-1]), float(Z["m2"][-1])]}
        self.bilanci.append(b)
        print("    [nascita %d] k %d, l'arco %d (%s): i %d j %d k %d l %d n %d%s; DH nascita %+.6e flip %+.6e (lo scarto %.2e |H|); P9 %.1e; Gauss %.1e; E_persa %+.6e (%.1f s)" % (
            self.nascite, k, a, perche, nd["i"], nd["j"], nd["k"], nd["l"], nd["n"], (" m %d" % nd["m"]) if "m" in nd else " (nessun flip: pari merito)",
            b["DH_nascita"], b["DH_flip"], R["gap"], d9, S["res"], self.e_persa, b["t"]))
        sys.stdout.flush()
        assert b["ok"] and d9 <= 1e-12, "la nascita NON e' entrata nel motore come il candidato (P9 %.1e): FERMO" % d9
        return b

    def scatta(self, Z, C, k, prima_di_nascere=None):
        """### `Theta` dopo il passo; se le nascite sono accese e un arco e' scattato, `prima_di_nascere()` (alla prima) e la nascita."""
        mot = Z["mot"]
        cs = PS.LC.cs_prec()
        assert cs is not None and np.array_equal(cs, mot.cs), "il cs del tick non e' quello del punto fisso"
        self.cont.accumula(mot, mot.cs)
        if not self.accese:
            return None
        sc = self.cont.scattati()
        if not sc.size:
            return None
        if self.nascite == 0 and prima_di_nascere is not None:
            prima_di_nascere()
        return self.nasci(Z, C, int(sc[0]), k, "scattato; %d in attesa" % (sc.size - 1))


# ------------------------------------------------------------------------------------------ salva e riprendi col grafo
def sha1(f):
    h = hashlib.sha1()
    with open(f, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def salva(Z, C, NS, k, t, meta, f):
    mot = Z["mot"]
    dati = {x: Z["st"][x] for x in Z["chiavi"]}
    dati.update(campo_A=C.campo.A, campo_E=C.campo.E, theta_a=NS.cont.theta)
    cs = PS.LC.cs_prec()
    if cs is not None:
        dati["cs_prec"] = cs
    if NS.nascite:
        dati.update(ii=np.asarray(mot.inc.nodo[0::2]), jj=np.asarray(mot.inc.nodo[1::2]), geo_n=mot.geo.n, campo_vec=C.campo.vec,
                    m1=np.asarray(Z["m1"], dtype=float), m2=np.asarray(Z["m2"], dtype=float))
    meta = dict(meta, k=int(k), t=float(t), E_persa=NS.e_persa, nascite=NS.nascite, n=int(mot.inc.n))
    os.makedirs(os.path.dirname(f), exist_ok=True)
    np.savez(f, meta=np.array(json.dumps(meta)), **dati)
    s = sha1(f)
    with open(f + ".sha1", "w", encoding="utf-8") as fh:
        fh.write(s + "\n")
    return s


def riprendi(Z, f, rho_c, e, accese):
    """### Da uno stato di C2 *(senza `theta_a`: allora `k 3000` e `Theta` dai segmenti)* o da uno stato MITOSI *(col grafo se cresciuto)*. `(C, NS, meta, cs)`."""
    import _u1_prototipo as U1
    import u1_generico as UG
    import contatore as CO
    from solitone import posizioni as PZ
    s = sha1(f)
    with open(f + ".sha1", encoding="utf-8") as fh:
        assert fh.read().split()[0] == s, "lo sha1 di %s NON coincide: la ripresa RIFIUTA" % f
    with np.load(f) as d:
        X = {x: d[x].copy() for x in d.files}
    meta = json.loads(str(X.pop("meta")))
    cs = X.get("cs_prec")
    if "theta_a" not in X:
        C, meta, cs, _s = CSB.riprendi(Z, f, False, rho_c, e)
        MC.campo_generico(Z, C)
        assert int(meta["k"]) == MC.K_C2, "uno stato di C2 senza Theta: solo k 3000 ha Theta dai segmenti"
        return C, Nascite(MC.theta_C2(), 0.0, 0, accese), meta, cs
    cont = CO.Contatore.riprendi(X)
    mot, st = Z["mot"], Z["st"]
    if "ii" not in X:
        Z["metti"]({x: X[x] for x in Z["chiavi"]})
        PS.metti_bordo(Z, meta["R_A"])
        Z["g_e"] = np.zeros_like(Z["g_e"])
        C = PS.PO.campi(Z, rho_c, e, X["campo_A"], X["campo_E"])
        MC.campo_generico(Z, C)
        return C, Nascite(cont, meta["E_persa"], meta["nascite"], accese), meta, cs
    # ### IL GRAFO CRESCIUTO: il toro della scena in UNA crescita
    Z["metti"]()
    PS.metti_bordo(Z, meta["R_A"])
    Z["g_e"] = np.zeros_like(Z["g_e"])
    m0 = mot.inc.m
    C = PS.PO.campi(Z, rho_c, e, np.zeros(m0), np.zeros(m0))
    g0, _info = MC.campo_generico(Z, C)
    ii0, jj0, n0 = np.asarray(mot.inc.nodo[0::2], dtype=np.int64), np.asarray(mot.inc.nodo[1::2], dtype=np.int64), int(mot.inc.n)
    ii, jj, n = X["ii"].astype(np.int64), X["jj"].astype(np.int64), int(meta["n"])
    N = n + 1
    k0 = ii0 * N + jj0
    kS = ii * N + jj
    tieni = np.isin(k0, kS)
    ms = int(tieni.sum())
    assert np.array_equal(kS[:ms], k0[tieni]), "il grafo salvato NON comincia coi sopravvissuti del toro nell'ordine"
    A, E = X["campo_A"], X["campo_E"]
    u = np.exp(1j * (g0.e * A))
    U = np.zeros((len(ii), 2, 2), dtype=complex)
    U[:, 0, 0] = u
    U[:, 1, 1] = u
    ini = {"psi_h": X["psi_h"][2 * ms:], "phi_h": X["phi_h"][2 * ms:], "geo_n": X["geo_n"][2 * ms:], "geo_U": U[ms:], "dtau": np.full(n - n0, float(mot.dtau[0]))}
    for x in Z["chiavi"]:
        if X[x].shape[0] == n:
            ini["nodo:" + x] = X[x][n0:]
    if mot.cs is not None:
        ini["cs"] = X["cs_prec"][n0:]
    mot.apri_tick()
    mot.cresci(tieni, ii[ms:], jj[ms:], n - n0, ini)
    mot.chiudi_tick()
    assert np.array_equal(np.asarray(mot.inc.nodo), MR.nodo_h(ii, jj)), "il grafo ricostruito NON e' quello salvato"
    for x in Z["chiavi"]:
        st[x] = X[x].copy()
    mot.geo.n[...] = X["geo_n"]
    s0 = float(g0.s_a[0])
    g = UG.CampoGenerico(ii, jj, n, X["campo_vec"], g0.e, g0.forma, np.full(len(ii), s0), np.full(len(ii), U1.L_SU_LS), lambda *_: U1.AREA)
    g.A[...] = A
    g.E[...] = E
    C.campo = g
    U1.scrivi_U(mot, g)
    Z["m1"], Z["m2"] = X["m1"], X["m2"]
    Z["n"] = mot.inc.n
    Z["nodo"] = np.asarray(mot.inc.nodo)
    Z["g_e"] = np.zeros(2 * mot.inc.m)
    for x, perche in PZ.RIFIUTATI.items():
        if x in Z:
            Z[x] = PZ.Rifiutato(x, perche)
    Z["cresciuto"] = int(meta["nascite"])
    return C, Nascite(cont, meta["E_persa"], meta["nascite"], accese), meta, cs


def stato_di(Z, C, NS):
    mot = Z["mot"]
    out = {x: Z["st"][x].copy() for x in Z["chiavi"]}
    cs = PS.LC.cs_prec()
    out.update(A=C.campo.A.copy(), E=C.campo.E.copy(), cs_prec=None if cs is None else cs.copy(), ii=np.asarray(mot.inc.nodo[0::2]).copy(),
               jj=np.asarray(mot.inc.nodo[1::2]).copy(), geo=mot.geo.n.copy(), theta=NS.cont.theta.copy(), m1=np.asarray(Z["m1"], dtype=float).copy(),
               m2=np.asarray(Z["m2"], dtype=float).copy(), E_persa=np.array([NS.e_persa]))
    return out


def diverse(a, b):
    out = []
    for x in a:
        p, q = a[x], b[x]
        if (p is None) != (q is None):
            out.append(x)
        elif p is not None and not (p.shape == q.shape and np.array_equal(p, q)):
            out.append(x)
    return out


def primo_arco():
    with np.load(os.path.join(MR.DIR_T, "candidati.npz")) as d:
        archi, T = d["archi"].copy(), d["T"].copy()
    return int(archi[np.argsort(T, kind="stable")[0]])


def misure_su(Z, centro, S=None):
    """### `controllo_senza_bordo.Misure` sul grafo di adesso: `r` dalle posizioni, gli archi dal motore; la serie `S` conservata."""
    import controllo_senza_bordo as CS2
    Mi = CS2.Misure.__new__(CS2.Misure)
    Mi.Z = Z
    Mi.r = raggi(Z, centro)
    Mi.ii, Mi.jj = np.asarray(Z["mot"].inc.nodo[0::2]), np.asarray(Z["mot"].inc.nodo[1::2])
    Mi.S = S if S is not None else {x: [] for x in ("k", "M", "E", "R5", "raggio") + tuple("Min_%g" % r for r in CS2.R_MASSA) + tuple("Jp_%g" % r for r in CS2.R_J) + tuple("Jn_%g" % r for r in CS2.R_J)}
    return Mi


# ------------------------------------------------------------------------------------------ nasce: N, P6.1, il costo
def nasce():
    import _presidio
    MT, CV = PS.MT, PS.CV
    _presidio.avvia(os.path.join(_QUI, "mitosi_regola.py"))
    _presidio.avvia(__file__)
    PS.presidi()
    rho_c, e, t0 = MT.rho_c_assoluto(), MT.PB.E_DECISO, MT.G2.T0
    a = primo_arco()
    esiti = []
    print("=" * 130)
    print("UNA NASCITA FORZATA NELLA CORSA E %d TICK DOPO; P6.1; IL COSTO (Luca 2026-11-20 16:37, 17:08; la carta sez. 10.3, 12)" % N_DOPO)
    print("=" * 130)
    k1 = MC.K_C2 + 1
    bracci = {}
    for nome in ("senza", "con"):
        with CV.scena_L(186, PS.FATTORE_R_A * PS.R_OGG_MAX) as Z:
            C, NS, meta, cs = riprendi(Z, MC.F_C2, rho_c, e, False)
            PS.PO.accendi(cs)
            try:
                R = CSB.corsa_senza_bordo()(Z, C)
                R.etichette([meta["lab"]])
                R.inizio(MC.K_C2)
                R.passo(k1, t0 + k1, 1.0, e)
                NS.scatta(Z, C, k1)
                B = {"k1": stato_di(Z, C, NS), "res_prima": MR.residuo(C.campo, MT.rho_di(Z))}
                if nome == "con":
                    B["b"] = NS.nasci(Z, C, a, k1, "FORZATA")
                    R.etichette([meta["lab"]])                               # ### le etichette dei pezzi della taglia nuova
                    B["nato"] = stato_di(Z, C, NS)
                B["M"], B["V"], B["res"], B["tt"] = [], [], [], []
                for q, k in enumerate(range(k1 + 1, k1 + 1 + N_DOPO)):
                    B["M"].append(float(np.sum(np.abs(Z["st"]["psi_h"]) ** 2)))
                    B["V"].append(float(np.sum(np.abs(Z["st"]["phi_h"]) ** 2)))
                    B["res"].append(MR.residuo(C.campo, MT.rho_di(Z)))
                    t1 = time.time()
                    R.passo(k, t0 + k, 1.0, e)
                    NS.scatta(Z, C, k)
                    B["tt"].append(time.time() - t1)
                    if q == 0:
                        B["uno"] = stato_di(Z, C, NS)
                B["M"].append(float(np.sum(np.abs(Z["st"]["psi_h"]) ** 2)))
                B["V"].append(float(np.sum(np.abs(Z["st"]["phi_h"]) ** 2)))
                B["res"].append(MR.residuo(C.campo, MT.rho_di(Z)))
                if nome == "con":
                    try:
                        Mi = misure_su(Z, meta["centro"])
                        rho = MT.rho_di(Z)
                        rg = PS.MR.raggio(Z, rho, MT.centro_di(Z, rho))
                        Mi.misura(k1 + N_DOPO, R, float("nan"), rg)
                        B["mis"] = "M %.12e, E %.10e, il raggio %.4f, Min12.4 %.6e, J45 + %.4e" % (Mi.S["M"][-1], Mi.S["E"][-1], rg, Mi.S["Min_12.4"][-1], Mi.S["Jp_45"][-1])
                    except Exception as ex:  # noqa: BLE001
                        B["mis"] = None
                        print("### le misure sul grafo cresciuto ALZANO: %r" % ex)
                    B["fine"] = stato_di(Z, C, NS)
            finally:
                PS.LC.spegni()
        bracci[nome] = B
    S0, S1 = bracci["senza"], bracci["con"]
    ok_k1 = not diverse(S0["k1"], S1["k1"])
    print("### prima della nascita (k %d) i due bracci AL BIT: %s" % (k1, ok_k1))
    esiti.append(("il tick prima della nascita: i due bracci AL BIT", ok_k1))
    b = S1["b"]
    nd = b["nodi"]
    n = nd["n"]
    # ### N
    def drel(x):
        return max(abs(v - x[0]) for v in x) / x[0]
    dM0, dV0, dM1, dV1 = drel(S0["M"]), drel(S0["V"]), drel(S1["M"]), drel(S1["V"])
    print("### N: %d tick dopo la nascita: la materia %.1e, il vuoto %.1e (le variazioni relative massime); senza la nascita %.1e e %.1e" % (N_DOPO, dM1, dV1, dM0, dV0))
    esiti.append(("N: M e V dopo la nascita come senza (entro 10 volte, o 1e-13)", dM1 <= max(10 * dM0, 1e-13) and dV1 <= max(10 * dV0, 1e-13)))
    print("### N: Gauss: prima della nascita %.2e; dopo la nascita %.2e; nei %d tick il massimo %.2e (senza la nascita %.2e)" % (S1["res_prima"], S1["res"][0], N_DOPO, max(S1["res"]), max(S0["res"])))
    esiti.append(("N: Gauss nei %d tick dopo la nascita sotto 10 volte il residuo di prima" % N_DOPO, max(S1["res"]) <= 10 * S1["res_prima"]))
    print("### N: le misure della corsa sul grafo cresciuto: %s" % S1["mis"])
    esiti.append(("N: le misure della corsa girano sul grafo cresciuto", S1["mis"] is not None))
    fin = S1["fine"]
    ok_t = fin["theta"].size == fin["ii"].size and fin["m1"].size == n + 1
    print("### Theta %d archi (il grafo %d); le posizioni %d nodi; E_persa %+.6e" % (fin["theta"].size, fin["ii"].size, fin["m1"].size, float(fin["E_persa"][0])))
    esiti.append(("Theta e le posizioni seguono il grafo", ok_t))
    # ### P6.1: dopo UN tick, nato contro non nato
    u0, u1 = S0["uno"], S1["uno"]
    N_ = n + 2
    kv = u0["ii"].astype(np.int64) * N_ + u0["jj"]
    kn = u1["ii"].astype(np.int64) * N_ + u1["jj"]
    keep = np.isin(kv, kn)
    dove = MR.dove_di(keep)
    assert np.array_equal(kn[:int(keep.sum())], kv[keep]), "i sopravvissuti non sono nell'ordine"
    hv = np.nonzero(np.repeat(keep, 2))[0]
    hn = dove[hv]
    nodo_v = MR.nodo_h(u0["ii"], u0["jj"])[hv]
    dpsi = np.sqrt(np.sum(np.abs(u1["psi_h"][hn] - u0["psi_h"][hv]) ** 2, axis=1))
    dphi = np.abs(u1["phi_h"][hn] - u0["phi_h"][hv])
    d = passi(u1["ii"], u1["jj"], n + 1, n)
    Pn = np.zeros(n)
    Fn = np.zeros(n)
    np.maximum.at(Pn, nodo_v, dpsi)
    np.maximum.at(Fn, nodo_v, dphi)
    av = np.nonzero(keep)[0]
    an = dove[2 * av] // 2
    dE0 = np.abs(S1["nato"]["E"][an] - S0["k1"]["E"][av])
    dE1 = np.abs(u1["E"][an] - u0["E"][av])
    da = np.minimum(d[u0["ii"][av]], d[u0["jj"][av]])
    print("### P6.1 (nessuna soglia): dopo UN tick, nato contro non nato dallo stesso stato di k %d; per anello in PASSI dal nodo nuovo %d:" % (k1, n))
    print("      d   nodi    max |d psi|     max |d phi|     max |d E| prima del tick   max |d E| dopo")
    for dd in list(range(0, 11)) + [15, 20, 30, 40, 60, int(d.max())]:
        sel = d[:n] == dd
        sa = da == dd
        if sel.any():
            print("    %4d %6d    %.3e       %.3e       %.3e                  %.3e" % (dd, int(sel.sum()), Pn[sel].max(), Fn[sel].max(), dE0[sa].max() if sa.any() else 0.0, dE1[sa].max() if sa.any() else 0.0))
    zero = [dd for dd in range(int(d.max()) + 1) if (d[:n] == dd).any() and Pn[d[:n] == dd].max() == 0.0 and Fn[d[:n] == dd].max() == 0.0]
    print("    gli anelli con la differenza ZERO al bit in psi e phi: %s" % (zero[:10] if zero else "nessuno"))
    # ### il costo
    t0m, t1m = float(np.median(S0["tt"])), float(np.median(S1["tt"]))
    print("### IL COSTO: il tick senza la nascita (mediana di %d) %.3f s; dopo la nascita %.3f s (%.4f); la nascita %.1f s (%.2f tick)" % (N_DOPO, t0m, t1m, t1m / t0m, b["t"], b["t"] / t0m))
    print("-" * 130)
    for nm, ok in esiti:
        print("  DEVE: %-112s %s" % (nm, "PASSA" if ok else "### FALLISCE"))
    print("=" * 130)
    return 0 if all(ok for _n, ok in esiti) else 1


# ------------------------------------------------------------------------------------------ p8: la ripresa al bit dopo una nascita
def p8():
    import _presidio
    MT, CV = PS.MT, PS.CV
    _presidio.avvia(os.path.join(_QUI, "mitosi_regola.py"))
    _presidio.avvia(__file__)
    PS.presidi()
    rho_c, e, t0 = MT.rho_c_assoluto(), MT.PB.E_DECISO, MT.G2.T0
    a = primo_arco()
    esiti = []
    print("=" * 130)
    print("P8: LA RIPRESA AL BIT DOPO UNA NASCITA (la carta sez. 10.3): %d tick di fila contro %d + salva + riprendi + %d; la nascita forzata al primo tick" % (N_P8, K_P8, N_P8 - K_P8))
    print("=" * 130)
    f = os.path.join(DIR, "P8_mitosi", "stato_%05d.npz" % (MC.K_C2 + K_P8))

    def corri(spezza):
        with CV.scena_L(186, PS.FATTORE_R_A * PS.R_OGG_MAX) as Z:
            C, NS, meta, cs = riprendi(Z, MC.F_C2, rho_c, e, True)
            PS.PO.accendi(cs)
            try:
                R = CSB.corsa_senza_bordo()(Z, C)
                R.etichette([meta["lab"]])
                R.inizio(MC.K_C2)
                for k in range(MC.K_C2 + 1, MC.K_C2 + N_P8 + 1):
                    R.passo(k, t0 + k, 1.0, e)
                    NS.scatta(Z, C, k)
                    if k == MC.K_C2 + 1:
                        NS.nasci(Z, C, a, k, "FORZATA")
                        R.etichette([meta["lab"]])
                    if spezza and k == MC.K_C2 + K_P8:
                        s = salva(Z, C, NS, k, t0 + k, meta, f)
                        print("    [stato] k %d: %s sha1 %s" % (k, os.path.basename(f), s[:8]))
                        break
                out = stato_di(Z, C, NS)
            finally:
                PS.LC.spegni()
        if not spezza:
            return out
        with CV.scena_L(186, PS.FATTORE_R_A * PS.R_OGG_MAX) as Z:
            C, NS, meta, cs = riprendi(Z, f, rho_c, e, True)
            PS.PO.accendi(cs)
            try:
                R = CSB.corsa_senza_bordo()(Z, C)
                R.etichette([meta["lab"]])
                R.inizio(MC.K_C2 + K_P8)
                for k in range(MC.K_C2 + K_P8 + 1, MC.K_C2 + N_P8 + 1):
                    R.passo(k, t0 + k, 1.0, e)
                    NS.scatta(Z, C, k)
                out = stato_di(Z, C, NS)
            finally:
                PS.LC.spegni()
        return out
    x, y = corri(False), corri(True)
    dv = diverse(x, y)
    print("### P8: %d tick di fila contro la ripresa: %s" % (N_P8, "AL BIT su ogni chiave, A, E, cs_prec, il grafo, i versori, Theta, le posizioni, E_persa" if not dv else "### DIVERSE: %s" % dv))
    esiti.append(("P8: la ripresa dopo una nascita AL BIT", not dv))
    # ### DEVE FALLIRE: un byte cambiato
    with open(f, "rb") as fh:
        raw = bytearray(fh.read())
    q = len(raw) // 2
    raw[q] ^= 0x01
    g = f.replace(".npz", "_toccato.npz")
    with open(g, "wb") as fh:
        fh.write(bytes(raw))
    with open(f + ".sha1", encoding="utf-8") as fh, open(g + ".sha1", "w", encoding="utf-8") as gh:
        gh.write(fh.read())
    try:
        with CV.scena_L(186, PS.FATTORE_R_A * PS.R_OGG_MAX) as Z:
            riprendi(Z, g, rho_c, e, True)
        rifiuta = False
    except AssertionError as ex:
        rifiuta = "sha1" in str(ex)
    print("### DEVE FALLIRE: un byte cambiato (il byte %d): la ripresa %s" % (q, "RIFIUTA (lo sha1)" if rifiuta else "### ACCETTA"))
    esiti.append(("DEVE FALLIRE: un byte cambiato nello stato salvato: la ripresa rifiuta", rifiuta))
    print("-" * 130)
    for nm, ok in esiti:
        print("  DEVE: %-112s %s" % (nm, "PASSA" if ok else "### FALLISCE"))
    print("=" * 130)
    return 0 if all(ok for _n, ok in esiti) else 1


# ------------------------------------------------------------------------------------------ la corsa
def corsa(nome, k_da, k_fino, accese, reg, sorgente):
    import controllo_senza_bordo as CS2
    from solitone import _registro_corse as RC
    import _presidio
    MT, CV, MRo = PS.MT, PS.CV, PS.MR
    _presidio.avvia(os.path.join(_QUI, "mitosi_regola.py"))
    _presidio.avvia(__file__)
    PS.presidi()
    rho_c, e, t0 = MT.rho_c_assoluto(), MT.PB.E_DECISO, MT.G2.T0
    t00 = time.time()
    d_out = os.path.join(DIR, nome)
    f = sorgente if sorgente else (MC.F_C2 if k_da == MC.K_C2 else os.path.join(d_out, "stato_%05d.npz" % k_da))
    print("=" * 130)
    print("LA CORSA %s (Luca 2026-11-20 16:37, 17:08): da k %d a k %d, le nascite %s; lo stato di partenza %s" % (nome, k_da, k_fino, "ACCESE" if accese else "SPENTE (il ramo C2-EXT)", f))
    print("=" * 130)
    with CV.scena_L(186, PS.FATTORE_R_A * PS.R_OGG_MAX) as Z:
        C, NS, meta, cs = riprendi(Z, f, rho_c, e, accese)
        PS.PO.accendi(cs)
        centro = meta["centro"]
        try:
            from solitone import toro as TO
            L = Z["L"]
            v = np.arange(L * L)
            r0 = np.hypot(*TO.scarti((v // L).astype(float), (v % L).astype(float), centro[0], centro[1], L).T[:2])
            anelli = {R_: np.nonzero((r0 >= R_ - 0.5) & (r0 < R_ + 0.5))[0] for R_ in ANELLI}
            serie_f = os.path.join(d_out, "serie_%05d.npz" % k_da)
            X = {}
            if os.path.exists(serie_f) and k_da != MC.K_C2:
                with np.load(serie_f) as d:
                    X = {x: list(d[x]) for x in d.files}
            Mi = misure_su(Z, centro, {x: X[x] for x in X if not x.startswith("D_")} or None)
            DS = {x: X.get(x, []) for x in ("D_k", "D_med40", "D_med60", "D_r50", "D_r90", "D_w", "D_n", "D_epersa")}
            RC_ = CSB.corsa_senza_bordo()(Z, C)
            RC_.etichette([meta["lab"]])
            RC_.inizio(k_da)

            def prima_di_nascere():
                fp = os.path.join(d_out, "prima_nascita_%05d.npz" % k)
                s = salva(Z, C, NS, k, t0 + k, meta, fp)
                print("    [stato PRIMA della prima nascita] k %d: %s sha1 %s (il punto del ramo C2-EXT)" % (k, os.path.basename(fp), s[:8]))
            t1 = t_tappa = time.time()
            k = k_da
            R5 = rg = float("nan")
            e1 = None
            for k in range(k_da, k_fino + 1):
                if k > k_da:
                    RC_.passo(k, t0 + k, 1.0, e)
                    if NS.scatta(Z, C, k, prima_di_nascere) is not None:
                        Mi = misure_su(Z, centro, Mi.S)
                        RC_.etichette([meta["lab"]])                         # ### le etichette dei pezzi della taglia nuova
                rho = MT.rho_di(Z)
                c = MT.centro_di(Z, rho)
                if k > k_da and k % PS.CT.OGNI == 0:
                    RC_.etichette([c])
                    meta["lab"] = [float(x) for x in c]
                if k % PS.OGNI == 0:
                    R5 = PS.r5(Z, t0 + k)[0] if not NS.nascite else float("nan")
                    rg = MRo.raggio(Z, rho, c)
                if k % MT.OGNI_GAUSS == 0:
                    C.residuo()
                if k % OGNI == 0 and not (k == k_da and k_da > 0):
                    Mi.misura(k, RC_, R5, rg)
                    src = int(np.argmin(raggi(Z, c)))
                    dd = passi(np.asarray(Z["mot"].inc.nodo[0::2]), np.asarray(Z["mot"].inc.nodo[1::2]), Z["mot"].inc.n, src)
                    e1 = scala(dd, rho)
                    for x_, v_ in (("D_k", k), ("D_med40", float(np.median(dd[anelli[40.0]]))), ("D_med60", float(np.median(dd[anelli[60.0]]))),
                                   ("D_r50", e1[0]), ("D_r90", e1[1]), ("D_w", e1[2]), ("D_n", NS.nascite), ("D_epersa", NS.e_persa)):
                        DS[x_].append(v_)
                if k % 250 == 0:
                    S = Mi.S
                    if S["M"] and DS["D_med40"]:
                        print("    k %5d  la massa %.12e  l'energia %+.10e  E_persa %+.6e  nascite %d  n %d  D1 %.1f/%.1f  E1 %s  (%.0f s)" % (
                            k, S["M"][-1], S["E"][-1], NS.e_persa, NS.nascite, Z["mot"].inc.n, DS["D_med40"][-1], DS["D_med60"][-1], e1, time.time() - t00))
                    sys.stdout.flush()
                if k > k_da and k % OGNI_STATO == 0:
                    s = salva(Z, C, NS, k, t0 + k, meta, os.path.join(d_out, "stato_%05d.npz" % k))
                    np.savez(os.path.join(d_out, "serie_%05d.npz" % k), **{x: np.array(v_) for x, v_ in list(Mi.S.items()) + list(DS.items())})
                    with open(os.path.join(d_out, "nascite_%05d.json" % k), "w", encoding="utf-8") as fh:
                        json.dump(NS.bilanci, fh)
                    print("    [stato] k %d sha1 %s" % (k, s[:8]))
                adesso = time.time()
                if reg and adesso - t_tappa >= MT.TAPPA_S:
                    RC.tappa(reg, "k %d; %.3f s per tick; nascite %d; la memoria libera %.2f GB" % (k, (adesso - t1) / max(1, k - k_da), NS.nascite, MT.memoria_gb()))
                    t_tappa = adesso
        finally:
            PS.LC.spegni()
    print("-" * 130)
    print("### %d tick in %.0f s (%.3f s per tick); %d nascite; E_persa %+.6e" % (k - k_da, time.time() - t1, (time.time() - t1) / max(1, k - k_da), NS.nascite, NS.e_persa))
    print("=" * 130)
    return 0


def main(argv):
    import argparse
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("nasce")
    sub.add_parser("p8")
    r = sub.add_parser("corsa")
    r.add_argument("--nome", required=True)
    r.add_argument("--da", type=int, required=True)
    r.add_argument("--fino", type=int, required=True)
    r.add_argument("--nascite", choices=("si", "no"), required=True)
    r.add_argument("--registro")
    r.add_argument("--sorgente")
    x = ap.parse_args(argv)
    if x.cmd == "nasce":
        return nasce()
    if x.cmd == "p8":
        return p8()
    return corsa(x.nome, x.da, x.fino, x.nascite == "si", x.registro, x.sorgente)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
