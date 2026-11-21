# -*- coding: utf-8 -*-
r"""**I RAMI CON L'ORIENTAMENTO EREDITATO -- LA V2 DI `mitosi_rami.py`** *(D2 di Luca `2026-11-21` `23:13`; la carta `doc/TASK_HISTORY/2026-11-21_orientamento_combinatorio.md`, sez. `4`; `mitosi_rami.py` e' IN USO e non si tocca: qui riga per riga, salvo: la regola `mitosi_regola_v2`; F3 a ogni nascita; `ori_cicli` nello stato; `riprendi_v2`; il sottocomando `riparti`)*. **IL TITOLO DELLA V1:** **IL TRONCO COMUNE E I DUE RAMI, C2-EXT E MITOSI** *(il ramo `mitosi`; Luca `2026-11-20` `18:40`; la carta `doc/TASK_HISTORY/2026-11-20_covariante_di_stella.md` del ramo `primo-ordine`, sez. `14`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/mitosi_rami.py prova > doc/referti_l2/mitosi_rami_prova.txt
    E:\python\py3132\python.exe doc/referti_l2/mitosi_rami.py tronco --da c2 --fino 40000 --registro <voce>        (--da ultimo dopo un riavvio)
    E:\python\py3132\python.exe doc/referti_l2/mitosi_rami.py ramo --nome MITOSI --da primo --dopo 10000 --registro <voce>
    E:\python\py3132\python.exe doc/referti_l2/mitosi_rami.py ramo --nome C2EXT --da primo --dopo 10000 --registro <voce>

**Importa `mitosi_lunga.py` senza toccarlo** *(`riprendi`, `misure_su`, `passi`, `scala`, `stato_di`, `diverse`)*.
**`tronco`:** il passo di C2 *(= MITOSI al bit, P6.0)*, `Theta`; **al primo scatto lo stato DOPO il passo e `Theta`, PRIMA della regola** *(`prima_nascita_<k>.npz`)*, `scatto.json`, **l'uscita `10`.** **`ramo`:** da quello stato *(`--da primo`)* o dall'ultimo proprio *(`--da ultimo`)*; **MITOSI fa per prima cosa la nascita del tick dello scatto** *(se riparte dal tronco)*; C2-EXT no.
**`gauss_acc`:** la correzione di Gauss SOMMATA sulle nascite, per arco *(segue la crescita: i tenuti, i nuovi a `0`)*; si salva con lo stato.
**Le misure ogni `50` tick** *(la serie `serie_<k>.npz` a ogni stato)*: quelle di C2; **D1** *(la mediana dei passi agli anelli `40` e `60` dei nodi ORIGINARI)*; **E1** *(`r50`, `r90`, `w` in passi)*; `E_persa`; le nascite; **la norma di `gauss_acc`, il suo massimo all'anello piu' lontano in passi** *(gli archi con un capo alla distanza massima)* **e all'anello `40`.** **A ogni nascita** *(D2, D3, `nascite_<k>.json`)*: `k`, il raggio del nodo nuovo dal centro, **la sua distanza in passi dalla sorgente**, i `DH`, la norma di `Ec`.
**`prova`** *(la carta sez. `14.3`)*: lo scatto FORZATO *(`Theta` di un arco a `2 pi` dopo il passo di `k 3002`; solo qui)*: **R1** il ramo MITOSI = la corsa continua *(`3005`)* AL BIT; **R2** il ramo C2-EXT = la continua spenta AL BIT; **R3** la ripresa dopo una nascita col `gauss_acc` AL BIT; **DEVE FALLIRE** il ramo MITOSI senza la nascita iniziale.
"""
import datetime
import glob
import json
import os
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import mitosi_lunga as ML  # noqa: E402
import mitosi_regola_v2 as MR2  # noqa: E402
import campo_orientato as CO  # noqa: E402

MR, MC, PS = ML.MR, ML.MC, ML.PS
CSB = MC.CSB
BASE = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "mitosi_rami")
OGNI, OGNI_STATO = 50, 250
SCATTO = 10


# ------------------------------------------------------------------------------------------ le nascite col gauss_acc
class Rami(ML.Nascite):
    def __init__(self, base, gacc, centro):
        ML.Nascite.__init__(self, base.cont, base.e_persa, base.nascite, base.accese)
        self.gacc = np.array(gacc, dtype=float)
        self.centro = centro
        self.sorgente = None

    def nasci(self, Z, C, a, k, perche):
        """### `mitosi_lunga.Nascite.nasci` riga per riga, in piu' `Ec`, `gauss_acc`, il luogo (D3)."""
        t1 = time.time()
        H0 = MR.energia_corsa(Z, C)
        R, S = MR2.regola(Z, C, int(a), "stella")
        keep, mb = S["keep"], S["mb"]
        nuovi = len(S["ii"]) - mb
        Ec = S["campo"].E - np.concatenate([C.campo.E[keep], np.zeros(nuovi)])
        assert self.gacc.shape == (keep.size,), "gauss_acc non segue il grafo"
        inf = MR.applica(Z, C, self.cont, S)
        eu, dp, tri, _gradi = MR.grafo_ok(np.asarray(S["ii"]), np.asarray(S["jj"]), int(R["nodi"]["n"]) + 1)
        f3 = bool(eu and dp and tri and S["coerenti"] and bool(np.all(C.campo.asg[:, 0] == -C.campo.asg[:, 1])))
        self.gacc = np.concatenate([self.gacc[keep], np.zeros(nuovi)]) + Ec
        H1 = MR.energia_corsa(Z, C)
        d9 = abs(H1 - S["H"]) / abs(S["H"])
        self.e_persa -= (H1 - H0)
        self.nascite += 1
        nd = R["nodi"]
        n = nd["n"]
        ii, jj = np.asarray(Z["mot"].inc.nodo[0::2]), np.asarray(Z["mot"].inc.nodo[1::2])
        src = int(np.argmin(ML.raggi(Z, self.centro_materia(Z))))
        dn = int(ML.passi(ii, jj, Z["mot"].inc.n, src)[n])
        r_n = float(ML.raggi(Z, self.centro)[n])
        b = {"k": int(k), "a": int(a), "perche": perche, "nodi": {x: int(v) for x, v in nd.items()}, "scelto": int(R["scelto"]), "gap": float(R["gap"]),
             "DH_nascita": float(R["H_nascita"] - H0), "DH_flip": float(S["H"] - R["H_nascita"]) if R["scelto"] >= 0 else 0.0, "DH": float(H1 - H0), "P9": float(d9),
             "res": float(S["res"]), "E_persa": self.e_persa, "t": time.time() - t1, "ok": bool(inf["ok_fuori"] and inf["ok_geo"] and inf["ok_U"]), "F3": f3,
             "pos": [float(Z["m1"][-1]), float(Z["m2"][-1])], "r": r_n, "passi": dn, "Ec_norma": float(np.linalg.norm(Ec)), "Ec_max": float(np.max(np.abs(Ec)))}
        self.bilanci.append(b)
        print("    [nascita %d] k %d, l'arco %d (%s): n %d a r %.2f, %d passi dalla sorgente; DH nascita %+.4e flip %+.4e; P9 %.1e; |Ec| %.3e; E_persa %+.6e (%.1f s)" % (
            self.nascite, k, a, perche, n, r_n, dn, b["DH_nascita"], b["DH_flip"], d9, b["Ec_norma"], self.e_persa, b["t"]))
        sys.stdout.flush()
        assert b["ok"] and d9 <= 1e-12 and f3, "la nascita NON e' entrata nel motore come il candidato (P9 %.1e) o F3 cade (%s): FERMO" % (d9, f3)
        return b

    @staticmethod
    def centro_materia(Z):
        return PS.MT.centro_di(Z, PS.MT.rho_di(Z))


# ------------------------------------------------------------------------------------------ salva, gli stati, la ripresa
def salva(Z, C, NS, k, t, meta, f):
    """### `mitosi_lunga.salva` riga per riga, col `gauss_acc` (sempre) e il grafo (dopo la prima nascita)."""
    mot = Z["mot"]
    dati = {x: Z["st"][x] for x in Z["chiavi"]}
    dati.update(campo_A=C.campo.A, campo_E=C.campo.E, theta_a=NS.cont.theta, gauss_acc=NS.gacc, ori_cicli=C.campo.ori_cicli())
    cs = PS.LC.cs_prec()
    if cs is not None:
        dati["cs_prec"] = cs
    if NS.nascite:
        dati.update(ii=np.asarray(mot.inc.nodo[0::2]), jj=np.asarray(mot.inc.nodo[1::2]), geo_n=mot.geo.n, campo_vec=C.campo.vec,
                    m1=np.asarray(Z["m1"], dtype=float), m2=np.asarray(Z["m2"], dtype=float))
    meta = dict(meta, k=int(k), t=float(t), E_persa=NS.e_persa, nascite=NS.nascite, n=int(mot.inc.n))
    os.makedirs(os.path.dirname(f), exist_ok=True)
    np.savez(f, meta=np.array(json.dumps(meta)), **dati)
    s = ML.sha1(f)
    with open(f + ".sha1", "w", encoding="utf-8") as fh:
        fh.write(s + "\n")
    return s


def stati(d):
    out = []
    for f in sorted(glob.glob(os.path.join(d, "stato_*.npz"))):
        k = int(os.path.basename(f)[6:11])
        ok = os.path.exists(f + ".sha1") and open(f + ".sha1", encoding="utf-8").read().split()[0] == ML.sha1(f)
        out.append((k, f, ok))
    return out


def ultimo(d):
    """### lo stato integro piu' recente *(`notte.py`, R3)*."""
    for k, f, ok in reversed(stati(d)):
        if ok:
            return k, f
        print("### R3: lo stato %s NON e' integro: si prende quello prima" % os.path.basename(f))
    return None


def ori_toro(Z):
    """### l'orientamento del toro della scena dai vettori d'arco del reticolo REGOLARE *(UNA volta: `mitosi_corsa.campo_generico`, la stessa costruzione)*."""
    import u1_generico as UG
    from solitone import toro as TO
    mot = Z["mot"]
    ii0, jj0, n0 = np.asarray(mot.inc.nodo[0::2], dtype=np.int64), np.asarray(mot.inc.nodo[1::2], dtype=np.int64), int(mot.inc.n)
    assert len(ii0) == 3 * n0, "la scena NON e' il toro di partenza"
    A1, A2 = TO.vettori()
    A1, A2 = np.asarray(A1, dtype=float)[:2], np.asarray(A2, dtype=float)[:2]
    vec = np.tile(np.stack([A1, A2, A1 + A2]), (n0, 1))
    g = UG.CampoGenerico(ii0, jj0, n0, vec, 1.0, "noncompatto", np.ones(len(ii0)), np.ones(len(ii0)), lambda *_: 1.0)
    return CO.orientamento_da_vec(g)


def riprendi_v2(Z, f, rho_c, e, accese):
    """### `mitosi_lunga.riprendi` col campo ORIENTATO: dal toro *(l'orientamento del reticolo regolare, UNA volta)*; da uno stato cresciuto VECCHIO *(senza `ori_cicli`: l'orientamento RICOSTRUITO lungo le nascite registrate, e controllato contro quello del prodotto vettoriale)*; da uno stato della v2 *(`ori_cicli` LETTO: il campo si costruisce senza nessun prodotto vettoriale)*."""
    import json as _json
    import _u1_prototipo as U1
    import contatore as COn
    from solitone import posizioni as PZ
    with np.load(f) as d:
        chiavi = set(d.files)
    ori0 = ori_toro(Z) if not Z.get("cresciuto") else None
    if "ii" not in chiavi:
        C, NS0, meta, cs = ML.riprendi(Z, f, rho_c, e, accese)
        C.campo = CO.orientato_da(C.campo, ori0)
        U1.scrivi_U(Z["mot"], C.campo)
        return C, NS0, meta, cs
    if "ori_cicli" not in chiavi:
        C, NS0, meta, cs = ML.riprendi(Z, f, rho_c, e, accese)
        fn = os.path.join(os.path.dirname(f), "nascite_%05d.json" % int(meta["k"]))
        with open(fn, encoding="utf-8") as fh:
            B = _json.load(fh)
        ori, dkl = MR2.ricostruisci(ori0, B)
        oggi = CO.orientamento_da_vec(C.campo)
        assert ori == oggi and not dkl, "l'orientamento ricostruito lungo le nascite NON e' quello di oggi (%d diversi, k/l %s): FERMO" % (sum(ori.get(x) != oggi.get(x) for x in set(ori) | set(oggi)), dkl)
        C.campo = CO.orientato_da(C.campo, ori)
        U1.scrivi_U(Z["mot"], C.campo)
        return C, NS0, meta, cs
    # ### lo stato della v2: le righe di mitosi_lunga.riprendi (il grafo cresciuto), il campo ORIENTATO dallo stato
    s_ = ML.sha1(f)
    with open(f + ".sha1", encoding="utf-8") as fh:
        assert fh.read().split()[0] == s_, "lo sha1 di %s NON coincide: la ripresa RIFIUTA" % f
    with np.load(f) as d:
        X = {x: d[x].copy() for x in d.files}
    meta = _json.loads(str(X.pop("meta")))
    cs = X.get("cs_prec")
    cont = COn.Contatore.riprendi(X)
    mot, st = Z["mot"], Z["st"]
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
    g = CO.CampoOrientato(ii, jj, n, X["campo_vec"], g0.e, g0.forma, np.full(len(ii), s0), np.full(len(ii), U1.L_SU_LS), lambda *_: U1.AREA, CO.da_cicli(X["ori_cicli"]))
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
    return C, ML.Nascite(cont, meta["E_persa"], meta["nascite"], accese), meta, cs


def apri(Z, f, rho_c, e, accese):
    C, NS0, meta, cs = riprendi_v2(Z, f, rho_c, e, accese)
    with np.load(f) as d:
        g = d["gauss_acc"].copy() if "gauss_acc" in d.files else np.zeros(Z["mot"].inc.m)
    return C, Rami(NS0, g, meta["centro"]), meta, cs


# ------------------------------------------------------------------------------------------ il ciclo
def ciclo(nome, modo, f, k_fino, reg, ferma_alle=None, forza=None, nascita_iniziale=True, d_out=None, dopo_scatto=None):
    """### `modo`: `tronco`, `mitosi`, `c2ext`. `(codice, k, stato_di)`; codice `0` finito, `SCATTO` il primo scatto (tronco), `3` sospesa."""
    from solitone import _registro_corse as RC
    MT, CV, MRo = PS.MT, PS.CV, PS.MR
    rho_c, e, t0 = MT.rho_c_assoluto(), MT.PB.E_DECISO, MT.G2.T0
    t00 = time.time()
    d_out = d_out or os.path.join(BASE, nome)
    limite = datetime.datetime.fromisoformat(ferma_alle) if ferma_alle else None
    codice = 0
    with CV.scena_L(186, PS.FATTORE_R_A * PS.R_OGG_MAX) as Z:
        C, NS, meta, cs = apri(Z, f, rho_c, e, modo == "mitosi")
        k_da = int(meta["k"])
        centro = meta["centro"]
        print("### %s (%s): da %s (k %d, sha1 %s), fino a k %d; le nascite %s" % (nome, modo, f, k_da, ML.sha1(f)[:8], k_fino, "ACCESE" if modo == "mitosi" else "SPENTE"))
        PS.PO.accendi(cs)
        try:
            from solitone import toro as TO
            L = Z["L"]
            v = np.arange(L * L)
            r0 = np.hypot(*TO.scarti((v // L).astype(float), (v % L).astype(float), centro[0], centro[1], L).T[:2])
            anelli = {R_: np.nonzero((r0 >= R_ - 0.5) & (r0 < R_ + 0.5))[0] for R_ in ML.ANELLI}
            X = {}
            fs = os.path.join(d_out, "serie_%05d.npz" % k_da)
            if os.path.exists(fs):
                with np.load(fs) as d:
                    X = {x: list(d[x]) for x in d.files}
            fn = os.path.join(d_out, "nascite_%05d.json" % k_da)
            if os.path.exists(fn):
                with open(fn, encoding="utf-8") as fh:
                    NS.bilanci = json.load(fh)
            Mi = ML.misure_su(Z, centro, {x: X[x] for x in X if not x.startswith("D_") and not x.startswith("G_")} or None)
            nomi_D = ("D_k", "D_med40", "D_med60", "D_r50", "D_r90", "D_w", "D_n", "D_epersa", "G_norma", "G_max_lontano", "G_max_40", "G_d_max")
            DS = {x: X.get(x, []) for x in nomi_D}
            RC_ = CSB.corsa_senza_bordo()(Z, C)
            RC_.etichette([meta["lab"]])
            RC_.inizio(k_da)
            if modo == "mitosi" and nascita_iniziale and meta.get("tronco_scatto"):
                sc = NS.cont.scattati()
                assert sc.size, "lo stato del tronco NON ha un arco scattato"
                NS.nasci(Z, C, int(sc[0]), k_da, "lo scatto del tronco; %d in attesa" % (sc.size - 1))
                Mi = ML.misure_su(Z, centro, Mi.S)
                RC_.etichette([meta["lab"]])
            t1 = t_tappa = time.time()
            R5 = rg = float("nan")
            k = k_da
            for k in range(k_da, k_fino + 1):
                if k > k_da:
                    RC_.passo(k, t0 + k, 1.0, e)
                    mot = Z["mot"]
                    csp = PS.LC.cs_prec()
                    assert csp is not None and np.array_equal(csp, mot.cs), "il cs del tick non e' quello del punto fisso"
                    NS.cont.accumula(mot, mot.cs)
                    if forza is not None and k == forza[0]:
                        a_ = forza[1]
                        th = float(NS.cont.theta[a_])
                        NS.cont.theta[a_] = th + 2.0 * np.pi * (1.0 if th >= 0.0 else -1.0)      # ### SOLO nella prova: lo scatto forzato
                    sc = NS.cont.scattati()
                    if sc.size:
                        if modo == "tronco":
                            fp = os.path.join(d_out, "prima_nascita_%05d.npz" % k)
                            s = salva(Z, C, NS, k, t0 + k, dict(meta, tronco_scatto=True), fp)
                            with open(os.path.join(d_out, "scatto.json"), "w", encoding="utf-8") as fh:
                                json.dump({"k": k, "file": fp, "sha1": s, "archi": [int(x) for x in sc[:20]], "quanti": int(sc.size)}, fh)
                            print("### IL PRIMO SCATTO a k %d (%d archi, il primo %d): lo stato PRIMA della regola %s sha1 %s; il tronco esce (%d)" % (k, sc.size, int(sc[0]), os.path.basename(fp), s[:8], SCATTO))
                            if reg:
                                RC.tappa(reg, "IL PRIMO SCATTO a k %d: %s sha1 %s" % (k, os.path.basename(fp), s[:8]))
                            codice = SCATTO
                            break
                        if modo == "mitosi":
                            NS.nasci(Z, C, int(sc[0]), k, "scattato; %d in attesa" % (sc.size - 1))
                            Mi = ML.misure_su(Z, centro, Mi.S)
                            RC_.etichette([meta["lab"]])
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
                    ii, jj = np.asarray(Z["mot"].inc.nodo[0::2]), np.asarray(Z["mot"].inc.nodo[1::2])
                    src = int(np.argmin(ML.raggi(Z, c)))
                    dd = ML.passi(ii, jj, Z["mot"].inc.n, src)
                    e1 = ML.scala(dd, rho)
                    da_ = np.minimum(dd[ii], dd[jj])
                    lont = da_ >= int(dd.max()) - 1
                    a40 = np.isin(ii, anelli[40.0]) | np.isin(jj, anelli[40.0])
                    g = np.abs(NS.gacc)
                    for x_, v_ in (("D_k", k), ("D_med40", float(np.median(dd[anelli[40.0]]))), ("D_med60", float(np.median(dd[anelli[60.0]]))),
                                   ("D_r50", e1[0]), ("D_r90", e1[1]), ("D_w", e1[2]), ("D_n", NS.nascite), ("D_epersa", NS.e_persa),
                                   ("G_norma", float(np.linalg.norm(NS.gacc))), ("G_max_lontano", float(g[lont].max())), ("G_max_40", float(g[a40].max())), ("G_d_max", int(dd.max()))):
                        DS[x_].append(v_)
                    if k % 250 == 0:
                        S = Mi.S
                        print("    k %5d  M %.12e  E %+.10e  E_persa %+.6e  nascite %d  n %d  D1 %.1f/%.1f  E1 %s  |gauss_acc| %.3e (lontano %.3e)  (%.0f s)" % (
                            k, S["M"][-1], S["E"][-1], NS.e_persa, NS.nascite, Z["mot"].inc.n, DS["D_med40"][-1], DS["D_med60"][-1], e1, DS["G_norma"][-1], DS["G_max_lontano"][-1], time.time() - t00))
                        sys.stdout.flush()
                sospendi = limite is not None and datetime.datetime.now() >= limite
                if k > k_da and (k % OGNI_STATO == 0 or k == k_fino or sospendi):
                    s = salva(Z, C, NS, k, t0 + k, dict(meta, tronco_scatto=False), os.path.join(d_out, "stato_%05d.npz" % k))
                    np.savez(os.path.join(d_out, "serie_%05d.npz" % k), **{x: np.array(v_) for x, v_ in list(Mi.S.items()) + list(DS.items())})
                    with open(os.path.join(d_out, "nascite_%05d.json" % k), "w", encoding="utf-8") as fh:
                        json.dump(NS.bilanci, fh)
                    print("    [stato] k %d sha1 %s" % (k, s[:8]))
                    sys.stdout.flush()
                if sospendi:
                    print("### SOSPESA alle %s a k %d" % (datetime.datetime.now().strftime("%H:%M:%S"), k))
                    codice = 3
                    break
                adesso = time.time()
                if reg and adesso - t_tappa >= MT.TAPPA_S:
                    RC.tappa(reg, "k %d; %.3f s per tick; nascite %d; la memoria libera %.2f GB" % (k, (adesso - t1) / max(1, k - k_da), NS.nascite, MT.memoria_gb()))
                    t_tappa = adesso
            fine = ML.stato_di(Z, C, NS)
            fine["gauss_acc"] = NS.gacc.copy()
        finally:
            PS.LC.spegni()
    print("### %s: %d tick in %.0f s; %d nascite; E_persa %+.6e; il codice %d" % (nome, k - k_da, time.time() - t00, NS.nascite, NS.e_persa, codice))
    return codice, k, fine


# ------------------------------------------------------------------------------------------ la prova del punto di ramificazione
def prova():
    import _presidio
    import shutil
    _presidio.avvia(os.path.join(_QUI, "mitosi_lunga.py"))
    _presidio.avvia(__file__)
    PS.presidi()
    a = ML.primo_arco()
    KF, KS, KE = 3002, 3005, 3008
    d = os.path.join(BASE, "PROVA")
    if os.path.isdir(d):
        shutil.rmtree(d)
    esiti = []
    print("=" * 130)
    print("LA PROVA DEL PUNTO DI RAMIFICAZIONE (Luca 2026-11-20 18:40; la carta sez. 14.3): lo scatto FORZATO dell'arco %d a k %d (solo qui)" % (a, KF))
    print("=" * 130)
    # ### la corsa continua con le nascite accese, e con le nascite spente
    _c, _k, cont_m = ciclo("PROVA_cont_m", "mitosi", MC.F_C2, KS, None, forza=(KF, a), d_out=os.path.join(d, "cont_m"))
    _c, _k, cont_c = ciclo("PROVA_cont_c", "c2ext", MC.F_C2, KS, None, forza=(KF, a), d_out=os.path.join(d, "cont_c"))
    # ### il tronco
    cod, kt, _f = ciclo("PROVA_tronco", "tronco", MC.F_C2, KS, None, forza=(KF, a), d_out=os.path.join(d, "tronco"))
    with open(os.path.join(d, "tronco", "scatto.json"), encoding="utf-8") as fh:
        sj = json.load(fh)
    print("### il tronco: il codice %d a k %d; scatto.json %s" % (cod, kt, sj))
    esiti.append(("il tronco esce col codice dello scatto al tick forzato", cod == SCATTO and kt == KF and sj["k"] == KF))
    _c, _k, ramo_m = ciclo("PROVA_m", "mitosi", sj["file"], KS, None, d_out=os.path.join(d, "ramo_m"))
    _c, _k, ramo_c = ciclo("PROVA_c", "c2ext", sj["file"], KS, None, d_out=os.path.join(d, "ramo_c"))
    _c, _k, senza = ciclo("PROVA_senza", "mitosi", sj["file"], KS, None, nascita_iniziale=False, d_out=os.path.join(d, "ramo_senza"))
    d1, d2, d3 = ML.diverse(cont_m, ramo_m), ML.diverse(cont_c, ramo_c), ML.diverse(cont_m, senza)
    print("### R1: il ramo MITOSI contro la corsa continua (k %d): %s" % (KS, "AL BIT su ogni chiave, A, E, cs_prec, il grafo, i versori, Theta, le posizioni, E_persa, gauss_acc" if not d1 else "### DIVERSE: %s" % d1))
    esiti.append(("R1: il ramo MITOSI = la corsa continua con le nascite AL BIT", not d1))
    print("### R2: il ramo C2-EXT contro la corsa continua spenta: %s" % ("AL BIT" if not d2 else "### DIVERSE: %s" % d2))
    esiti.append(("R2: il ramo C2-EXT = la corsa continua spenta AL BIT", not d2))
    print("### DEVE FALLIRE: il ramo MITOSI SENZA la nascita iniziale: %s" % ("### UGUALE" if not d3 else "diverse: %s" % d3[:6]))
    esiti.append(("DEVE FALLIRE: il ramo MITOSI senza la nascita iniziale e' diverso", bool(d3)))
    # ### R3: la ripresa del ramo MITOSI dall'ultimo suo stato (k 3005) fino a KE, contro la continua fino a KE
    _c, _k, cont_e = ciclo("PROVA_cont_e", "mitosi", MC.F_C2, KE, None, forza=(KF, a), d_out=os.path.join(d, "cont_e"))
    u = ultimo(os.path.join(d, "ramo_m"))
    _c, _k, rip = ciclo("PROVA_rip", "mitosi", u[1], KE, None, d_out=os.path.join(d, "ramo_m"))
    d4 = ML.diverse(cont_e, rip)
    print("### R3: la ripresa del ramo MITOSI da %s fino a k %d contro la continua: %s" % (os.path.basename(u[1]), KE, "AL BIT" if not d4 else "### DIVERSE: %s" % d4))
    esiti.append(("R3: la ripresa dopo una nascita col gauss_acc AL BIT", not d4))
    g = cont_e["gauss_acc"]
    print("    gauss_acc dopo la nascita: la norma %.3e, il massimo %.3e" % (float(np.linalg.norm(g)), float(np.max(np.abs(g)))))
    print("-" * 130)
    for nm, ok in esiti:
        print("  DEVE: %-112s %s" % (nm, "PASSA" if ok else "### FALLISCE"))
    print("=" * 130)
    return 0 if all(ok for _n, ok in esiti) else 1


def main(argv):
    import argparse
    import _presidio
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("prova")
    t = sub.add_parser("tronco")
    t.add_argument("--da", required=True)
    t.add_argument("--fino", type=int, required=True)
    t.add_argument("--registro")
    t.add_argument("--ferma-alle")
    q = sub.add_parser("riparti")
    q.add_argument("--da", required=True)
    q.add_argument("--fino", type=int, required=True)
    q.add_argument("--nome", required=True)
    q.add_argument("--registro")
    r = sub.add_parser("ramo")
    r.add_argument("--nome", choices=("MITOSI", "C2EXT"), required=True)
    r.add_argument("--da", choices=("primo", "ultimo"), required=True)
    r.add_argument("--dopo", type=int, required=True)
    r.add_argument("--registro")
    r.add_argument("--ferma-alle")
    x = ap.parse_args(argv)
    if x.cmd == "prova":
        return prova()
    if x.cmd == "riparti":
        _presidio.avvia(os.path.join(_QUI, "mitosi_regola_v2.py"))
        _presidio.avvia(__file__)
        PS.presidi()
        cod, k, _f = ciclo(x.nome, "mitosi", x.da, x.fino, x.registro, d_out=os.path.join(BASE, x.nome))
        return cod
    _presidio.avvia(os.path.join(_QUI, "mitosi_lunga.py"))
    _presidio.avvia(__file__)
    PS.presidi()
    from solitone import _registro_corse as RC
    if x.cmd == "tronco":
        d = os.path.join(BASE, "TRONCO")
        if x.da == "c2":
            f = MC.F_C2
        else:
            u = ultimo(d)
            assert u is not None, "nessuno stato integro del tronco"
            f = u[1]
            if x.registro:
                RC.tappa(x.registro, "RIPRESA del tronco da k %d, %s sha1 %s" % (u[0], os.path.basename(f), ML.sha1(f)[:8]))
        cod, k, _f = ciclo("TRONCO", "tronco", f, x.fino, x.registro, ferma_alle=x.ferma_alle, d_out=d)
        return cod
    d = os.path.join(BASE, x.nome)
    with open(os.path.join(BASE, "TRONCO", "scatto.json"), encoding="utf-8") as fh:
        sj = json.load(fh)
    k_fine = int(sj["k"]) + int(x.dopo)
    if x.da == "primo":
        f = sj["file"]
        assert ML.sha1(f) == sj["sha1"], "lo stato del tronco NON e' integro"
    else:
        u = ultimo(d)
        assert u is not None, "nessuno stato integro di %s" % x.nome
        f = u[1]
        if x.registro:
            RC.tappa(x.registro, "RIPRESA di %s da k %d, %s sha1 %s" % (x.nome, u[0], os.path.basename(f), ML.sha1(f)[:8]))
    cod, k, _f = ciclo(x.nome, "mitosi" if x.nome == "MITOSI" else "c2ext", f, k_fine, x.registro, ferma_alle=x.ferma_alle, d_out=d)
    return cod


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
