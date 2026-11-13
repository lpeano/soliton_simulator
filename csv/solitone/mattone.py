# -*- coding: utf-8 -*-
r"""**LO STRUMENTO «MATTONE»** *(Luca `2026-11-13` `18:47`, `18:58`; le scelte S1-S8 del guardiano su delega di Luca; il task history `doc/TASK_HISTORY/2026-11-13_strumento_mattone.md`)*.

    python csv/solitone/mattone.py prepara --caso MG|MU|MGU --registro mattone-<caso>   (lo stdout nello scratchpad; gli stati su E:\soliton_simulator\mattone)
    python csv/solitone/mattone.py controllo --caso MG|MU|MGU --registro mattone-ctrl-<caso>
    python csv/solitone/mattone.py registro apri|chiudi ...   (il registro del ramo, doc/REGISTRO_CORSE_mattone.md)

### **Il solitone di base** *(S1)*: **TBS a `10000`, `L 81`** *(la moneta e lo zero di C35-pi; la partenza SIMMETRIZZATA, dichiarata)*, **il bordo di TBS.**
### **La preparazione** *(S2-S4)*: **`r(k) = sin^2(pi k / (2 K))`, `K = 4000`, poi `1000` tick a campi pieni** *(`5000`, stati ogni `1000` su E:)*; **(MG) il lapse `N_eff = 1 + r (N - 1)`**
*(`p6_bracci.con_rampa`, nel tick vero e nelle copie del punto fisso; `rho_c` ASSOLUTO dei bracci di P6, letto da `p6_bracci/0.npz`)*; **(MU) `e(k) = r(k) e*`:** **al primo `e > 0` il campo `E` = Gauss sparso**
*(`A = 0`)*, **poi `E` riscalato per `e(k)/e(k-1)`**; ### **la correzione del BORDO** *(mia, dichiarata)*: **l'assorbimento toglie materia senza corrente; `E` si corregge col Gauss sparso della SOLA materia tolta**
*(cosi' il controllo di Gauss misura tutto il resto)*; **(MGU) le due rampe con `p6_bracci.tick_GU`.**
### **«Calmo»** *(S5)*: **il respiro** *(picco-picco di `rho max x (somma rho) / somma rho^2`, la misura del video triplo)* **negli ultimi `1000` tick sotto `0.30`, il centro entro `0.2` nodi.**
### **Il francobollo** *(S6)*: **`R_t`** = **il raggio oltre il quale il `|dphi|` medio per anello resta sotto il `2%` di quello dell'anello del vuoto** *(LA MIA LETTURA: l'anello col `|dphi|` medio
MASSIMO)*, **non meno di `25`; il raccordo `cos^2` largo `4`; `psi` e `phi`;** ### **la fase del vuoto allineata** *(`Delta = arg somma conj(phi_dest) phi_franc` sul raccordo, tolta)*; **lo spostamento intero
MULTIPLO DI `3`** *(il disegno di fase di F3 ha periodo `3`)*; **il campo U NON si ritaglia: Gauss sparso dopo l'incollatura.**
### **Il controllo del metodo** *(S7)*: **il francobollo su `L 162` nella scena di S162** *(il bordo di S162, al posto del suo solitone)*, **`1000` tick coi campi pieni: il centro entro `0.2` nodi, il respiro entro il
`25%` di quello del mattone, il salto di energia all'incollatura scritto.**
"""
import argparse
import contextlib
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
import solitone  # noqa: E402,F401  (i percorsi)
import p6_bracci as PBR  # noqa: E402  (con_rampa, tick_GU: RIPRESI, non riscritti)
import p6_u_breve as PB  # noqa: E402  (gauss_sparso, rho_nodi, E_DECISO, FORMA)
import s5_coppia_lapse as G2  # noqa: E402  (eps_top_tl4b, R_LAPSE)

RADICE = os.path.dirname(_CSV)
CASI = ("MG", "MU", "MGU")
CORSA_BASE, T_BASE = "TBS", 10000          # ### S1
CORSA_162, T_162 = "S162", 10000           # ### S7: la scena e il bordo di S162 (il suo stato di partenza a 10000 solo per la posizione del solitone)
K_RAMPA, N_PIENO, PEZZO = 4000, 1000, 1000  # ### S2
OGNI, OGNI_GAUSS = 50, 250                 # ### S4: Gauss ogni 250
SOGLIA_CALMO, FERMO_CENTRO = 0.30, 0.2     # ### S5
TOLL_RESPIRO = 0.25                        # ### S7
N_CONTROLLO = 1000                         # ### S7
SOGLIA_RT, RT_MIN, RACCORDO = 0.02, 25.0, 4.0   # ### S6
TOLL_GAUSS = 1e-10                         # ### il DEVE di Gauss
TETTO_S = 18000.0                          # ### Luca 18:57
MEM_MIN_GB = 2.0                           # ### la protezione del guardiano (18:58): sotto 2 GB si ferma la corsa del mattone
TAPPA_S = 600.0
DIR_E = r"E:\soliton_simulator\mattone"
DIR_REF = os.path.join(RADICE, "doc", "referti_l2", "mattone")
REGISTRO_MATTONE = os.path.join(RADICE, "doc", "REGISTRO_CORSE_mattone.md")


def r_di(k):
    """### S2: `sin^2(pi k / (2 K))` fino a `K`, poi `1`."""
    return math.sin(math.pi * k / (2.0 * K_RAMPA)) ** 2 if k < K_RAMPA else 1.0


def respiro(rr):
    """### Il rapporto del video triplo: `rho max x (somma rho) / somma rho^2`."""
    return float(rr.max() * rr.sum() / np.sum(rr * rr))


def rho_c_assoluto():
    with np.load(os.path.join(PBR.DIR_OUT, "0.npz")) as d:
        return float(json.loads(str(d["meta"]))["rho_c"])


# =====================================================================================
#   LA SCENA
# =====================================================================================
@contextlib.contextmanager
def scena(corsa, t_stato):
    """### **La scena di una corsa** *(come G2 e le G1)*: `Z` con lo stato a `t_stato` caricato, il bordo, la fase del vuoto, `e_K`; ### **lo stato rimesso dentro `Z["metti"]()`.**"""
    import _deriva_congelato as DC
    import _dove_va_la_materia as DV
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _triangoli_bassa_energia as BE
    import _vuoto_vivo_B as V
    from solitone import bordo as BO
    from solitone import corsa_accensione as CA
    from solitone import protetto as P
    sol, vuoto, s = V.CORSE[CA.NOME]
    T_acc, _f = CA.CORSE[corsa]
    K = int(round(T_acc / s))
    rr = CA.serie(corsa)[0]
    x_st = [x for r in rr for x in (r.get("stati") or []) if x["t"] == t_stato]
    assert len(x_st) == 1, "lo stato di %s a %d NON e' uno solo" % (corsa, t_stato)
    bor = rr[-1]["bordo"]
    with np.load(os.path.join(CA.DIR_NPZ, CA.FASE)) as d:
        tab_c, omega = d["c"].copy(), float(d["omega"])
        assert int(d["K"]) == K
    with CA.con_L(CA.LCORSA.get(corsa)), V.scena(s, vuoto, V.EPS) as (rec, z, phi0, pK):
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            DC.forma(z, rec["larghezza"])
        salvato = {k: v.copy() for k, v in z["st"].items() if isinstance(v, np.ndarray)}
        V.partenza(sol, z, phi0, pK, s)
        e_K = P.e_K(z)
        DV.autovettori(DV.matrice(z, phi0, DV.AMP))
        phi_v = CA.vuoto_della_corsa(z, corsa)
        for k, v in salvato.items():
            z["st"][k][...] = v
        st, mot = z["st"], z["mot"]
        n, L = z["inc"].n, z["L"]
        chiavi = sorted(k for k, v in st.items() if isinstance(v, np.ndarray))
        cs0, lc0 = mot.cs, getattr(mot, "lambda_c", None)
        U0 = mot.geo.U.copy()
        with np.load(x_st[0]["file"]) as d:
            stato = {k: d[k].copy() for k in chiavi}

        def metti(st_dato=None):
            for k in chiavi:
                st[k][...] = (st_dato or stato)[k]
            mot.cs, mot.lambda_c = cs0, lc0
            mot.geo.U[...] = U0
        metti()
        assert V.shas(z) == x_st[0]["sha"], "lo stato di %s a %d NON e' quello registrato" % (corsa, t_stato)
        nodo = np.asarray(z["inc"].nodo)
        v_ = np.arange(n)
        g_e = BO.g_estremita(z, bor["c0"][0], bor["c0"][1], bor["R_A"], bor["g_max"])[0]
        Z = {"z": z, "st": st, "mot": mot, "par": z["par"], "n": n, "L": L, "nodo": nodo, "m1": v_ // L, "m2": v_ % L, "chiavi": chiavi, "stato": stato,
             "metti": metti, "phi_v": phi_v, "tab_c": tab_c, "omega": omega, "K": K, "s": s, "e_K": e_K, "g_e": g_e, "bordo": bor, "U0": U0,
             "righe": np.argsort(nodo, kind="stable").reshape(n, 6), "x_st": x_st[0]}
        try:
            with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
                yield Z
        finally:
            metti()


def vuoto_fresco(Z, t):
    """### `phi = c(t) F3`, `psi = 0` *(il vuoto della corsa allo stesso tick)*."""
    from solitone import bordo as BO
    Z["st"]["psi_h"][...] = 0.0
    Z["st"]["phi_h"][...] = BO.c_di(t, Z["tab_c"], Z["K"], Z["omega"]) * Z["phi_v"]


def energia(Z):
    import _libro_dei_conti as LC
    import _vuoto_vivo_B as V
    return float(np.sum(LC.conti_per_nodo(Z["z"]["inc"], Z["mot"], Z["st"], Z["e_K"], V.LAM_ZERO, Z["par"])["tot"]))


def rho_di(Z):
    return PB.rho_nodi(Z["st"], Z["nodo"], Z["n"])


def centro_di(Z, rho):
    from solitone import toro as TO
    return TO.centro(rho, Z["m1"], Z["m2"], Z["L"])[:2]


def distanza(L, a, b):
    from solitone import toro as TO
    p = TO.scarti(np.array([a[0]]), np.array([a[1]]), b[0], b[1], L)[0]
    return float(np.hypot(p[0], p[1]))


# =====================================================================================
#   IL TICK DEL MATTONE
# =====================================================================================
class Campi(object):
    """### **I campi di un caso** *(S3, S4)*: il lapse con la rampa, la U(1) con `e(k)`; ### **la correzione del bordo** *(Gauss sparso della materia tolta)*."""

    def __init__(self, Z, caso, rho_c, e_star):
        from solitone import _u1_oggi as UO
        self.Z, self.caso, self.legge, self.e_star = Z, caso, ("rho_c", rho_c), e_star
        self.e0 = G2.eps_top_tl4b()
        self.campo = UO.campo_della_scena(Z["z"], 0.0, PB.FORMA) if caso in ("MU", "MGU") else None
        self.e_prec = 0.0

    def gauss(self, b):
        E, _D = PB.gauss_sparso(self.campo, b)
        return E

    def residuo(self):
        """### `max |div E - e (rho - media)| / (e max rho)`; `0` se `e = 0`."""
        if self.campo is None or self.campo.e == 0.0:
            return 0.0
        rho = rho_di(self.Z)
        G = self.campo.div() - self.campo.e * (rho - rho.mean())
        return float(np.max(np.abs(G))) / (self.campo.e * float(rho.max()))

    def tick(self, k, t, r, e):
        """### Il tick `k` *(`t` assoluto)* con la rampa `r` e la carica `e`; poi il bordo *(con la correzione di Gauss)*."""
        from solitone import _u1_oggi as UO
        from solitone import bordo as BO
        from solitone import tick_lapse as TL
        Z = self.Z
        if self.campo is not None:
            if e > 0.0 and self.e_prec == 0.0:
                rho = rho_di(Z)
                self.campo.A[...] = 0.0
                self.campo.E[...] = self.gauss(e * (rho - rho.mean()))     # ### S4: al primo e > 0, Gauss sparso
            elif self.e_prec > 0.0:
                self.campo.E *= e / self.e_prec                             # ### S4: E riscalato
            self.campo.e = e
            self.e_prec = e
        if self.caso == "MG":
            with PBR.con_rampa(r):
                TL.tick(Z["mot"], Z["st"], Z["par"], Z["s"], self.legge, eps_a=self.e0)
        elif self.caso == "MU":
            UO.tick(Z["z"], t, Z["K"], self.campo, True)
        else:
            with PBR.con_rampa(r):
                PBR.tick_GU(Z["z"], Z["s"], self.legge, self.e0, self.campo)
        rho_prima = rho_di(Z) if self.campo is not None and self.campo.e > 0.0 else None
        BO.assorbi(Z["st"], Z["g_e"], BO.c_di(t, Z["tab_c"], Z["K"], Z["omega"]) * Z["phi_v"])
        if rho_prima is not None:
            drho = rho_di(Z) - rho_prima                                     # ### la materia TOLTA dal bordo (negativa)
            self.campo.E += self.gauss(self.campo.e * (drho - drho.mean()))  # ### la correzione del bordo (dichiarata)


# =====================================================================================
#   IL FRANCOBOLLO
# =====================================================================================
def ritaglia(Z, centro, phi_rif):
    """### **S6:** `R_t` dal `|dphi|` per anello *(`dphi = phi - phi_rif` per nodo, la somma dei moduli delle `6` componenti)*; il francobollo: gli scarti interi dal centro ARROTONDATO,
    `psi` e `phi` delle righe di ciascun nodo, il peso `w` *(`1` fino a `R_t`, `cos^2` fino a `R_t + 4`)*."""
    from solitone import toro as TO
    L, n, righe = Z["L"], Z["n"], Z["righe"]
    c1, c2 = int(round(centro[0])) % L, int(round(centro[1])) % L
    pos = TO.scarti(Z["m1"], Z["m2"], c1, c2, L)
    r = np.hypot(pos[:, 0], pos[:, 1])
    dphi = np.abs(Z["st"]["phi_h"] - phi_rif).reshape(n * 6, -1).sum(axis=1)
    dn = np.zeros(n)
    np.add.at(dn, Z["nodo"], dphi)
    anelli = np.floor(r).astype(int)
    media = np.bincount(anelli, weights=dn) / np.maximum(np.bincount(anelli), 1)
    i_max = int(np.argmax(media))                       # ### l'anello del vuoto: il |dphi| medio MASSIMO (la mia lettura, dichiarata)
    sotto = media < SOGLIA_RT * media[i_max]
    R_t = None
    for j in range(i_max + 1, len(media)):
        if sotto[j:int(L / 2)].all():
            R_t = float(j)
            break
    assert R_t is not None, "R_t non trovato: il |dphi| non scende sotto il 2% prima di L/2"
    R_t = max(R_t, RT_MIN)
    dentro = r <= R_t + RACCORDO
    d1 = ((Z["m1"] - c1 + L // 2) % L) - L // 2
    d2 = ((Z["m2"] - c2 + L // 2) % L) - L // 2
    w = np.where(r <= R_t, 1.0, np.cos(0.5 * math.pi * np.clip((r - R_t) / RACCORDO, 0.0, 1.0)) ** 2)
    vv = np.nonzero(dentro)[0]
    return {"o1": d1[vv], "o2": d2[vv], "w": w[vv], "r": r[vv], "psi": Z["st"]["psi_h"][righe[vv]].copy(), "phi": Z["st"]["phi_h"][righe[vv]].copy(),
            "R_t": R_t, "anello_vuoto": i_max, "centro": (c1, c2), "dphi_anelli": media[:int(R_t + RACCORDO) + 2]}


def incolla(Z, fr, centro, allinea):
    """### **S6:** il francobollo nel toro di `Z` al centro intero `centro` *(lo spostamento dal centro d'origine MULTIPLO di `3`)*; `psi = w psi_f + (1 - w) psi`; `phi = w phi_f e^{-i Delta} + (1 - w) phi`,
    ### `Delta = arg somma conj(phi) phi_f` sul raccordo *(se `allinea`; se no `0`)*. `Delta`."""
    L, righe = Z["L"], Z["righe"]
    assert (centro[0] - fr["centro"][0]) % 3 == 0 and (centro[1] - fr["centro"][1]) % 3 == 0, "lo spostamento NON e' multiplo di 3: il disegno di fase di F3 non combacia"
    vv = ((centro[0] + fr["o1"]) % L) * L + (centro[1] + fr["o2"]) % L
    rr = righe[vv]
    st = Z["st"]
    ring = fr["w"] < 1.0
    Delta = float(np.angle(np.sum(np.conj(st["phi_h"][rr[ring]]) * fr["phi"][ring]))) if allinea else 0.0
    wp = fr["w"].reshape((-1,) + (1,) * (fr["psi"].ndim - 1))
    wf = fr["w"].reshape((-1,) + (1,) * (fr["phi"].ndim - 1))
    st["psi_h"][rr] = wp * fr["psi"] + (1.0 - wp) * st["psi_h"][rr]
    st["phi_h"][rr] = wf * fr["phi"] * np.exp(-1j * Delta) + (1.0 - wf) * st["phi_h"][rr]
    return Delta


# =====================================================================================
#   IL REGISTRO DEL RAMO
# =====================================================================================
def registro(argv):
    from solitone import _registro_corse as RC
    with RC.su_file(REGISTRO_MATTONE, RC.TAPPE[0]):
        return RC.main(argv)


def tappa(nome, testo):
    from solitone import _registro_corse as RC
    if not nome:
        return
    with RC.su_file(REGISTRO_MATTONE, RC.TAPPE[0]):
        RC.tappa(nome, testo)


def memoria_gb():
    import psutil
    return psutil.virtual_memory().available / 1e9


# =====================================================================================
#   LA PREPARAZIONE (S2-S5)
# =====================================================================================
def prepara(caso, nome_reg):
    import _presidio
    import _vuoto_vivo_B as V
    _presidio.avvia(__file__)
    assert caso in CASI
    rho_c = rho_c_assoluto()
    os.makedirs(DIR_E, exist_ok=True)
    t00 = time.time()
    print("=" * 130)
    print("IL MATTONE (%s): TBS a %d, L 81; la rampa sin^2 in %d tick, poi %d a campi pieni; rho_c ASSOLUTO %.6f (p6_bracci/0.npz); e* %.7e; stati ogni %d su %s; il registro %s"
          % (caso, T_BASE, K_RAMPA, N_PIENO, rho_c, PB.E_DECISO, PEZZO, DIR_E, nome_reg))
    print("=" * 130)
    S = {k: [] for k in ("k", "r", "e", "c1", "c2", "rmax", "resp", "M", "E", "KV", "gauss")}
    fermo = None
    with scena(CORSA_BASE, T_BASE) as Z:
        C = Campi(Z, caso, rho_c, PB.E_DECISO)

        def misura(k, r, e):
            rho = rho_di(Z)
            c = centro_di(Z, rho)
            S["k"].append(k)
            S["r"].append(r)
            S["e"].append(e)
            S["c1"].append(c[0])
            S["c2"].append(c[1])
            S["rmax"].append(float(rho.max()))
            S["resp"].append(respiro(rho))
            S["M"].append(float(rho.sum()))
            S["E"].append(energia(Z))
            S["KV"].append(C.campo.K() + C.campo.V() if C.campo is not None else 0.0)
            S["gauss"].append(C.residuo() if (k % OGNI_GAUSS == 0) else float("nan"))
        misura(0, 0.0, 0.0)
        t1 = t_tappa = time.time()
        n_tot = K_RAMPA + N_PIENO
        for k in range(1, n_tot + 1):
            r = r_di(k)
            e = r * PB.E_DECISO if caso in ("MU", "MGU") else 0.0
            C.tick(k, T_BASE + k, r if caso in ("MG", "MGU") else 1.0, e)
            if k % OGNI == 0:
                misura(k, r, e)
                if k % OGNI_GAUSS == 0 or k % 500 == 0:
                    print("    k %5d  r %.6f  e %.4e  c (%.3f, %.3f)  rmax %.4e  respiro %.4f  M %.10e  E %.10e  K+V %.4e  Gauss %s  (%.0f s)" % (
                        k, r, e, S["c1"][-1], S["c2"][-1], S["rmax"][-1], S["resp"][-1], S["M"][-1], S["E"][-1], S["KV"][-1],
                        "%.2e" % S["gauss"][-1] if S["gauss"][-1] == S["gauss"][-1] else "--", time.time() - t1))
                    sys.stdout.flush()
            if k % PEZZO == 0:
                f = os.path.join(DIR_E, "%s_%05d.npz" % (caso, k))
                dati = {kk: Z["st"][kk] for kk in Z["chiavi"]}
                meta = {"caso": caso, "k": k, "t": T_BASE + k, "r": r, "e": e, "rho_c": rho_c, "sha": V.shas(Z["z"]), "codice": "csv/solitone/mattone.py"}
                if C.campo is not None:
                    dati.update(campo_A=C.campo.A, campo_E=C.campo.E)
                np.savez(f, meta=np.array(json.dumps(meta)), **dati)
                print("### lo stato a k %d: %s (sha di psi_h %s)" % (k, f, meta["sha"].get("psi_h")))
            adesso = time.time()
            if adesso - t_tappa >= TAPPA_S:
                mem = memoria_gb()
                tappa(nome_reg, "k %d; %.3f s per tick dall'inizio; la memoria libera %.2f GB" % (k, (adesso - t1) / k, mem))
                t_tappa = adesso
                if mem < MEM_MIN_GB:
                    fermo = "la memoria libera %.2f GB sotto %g GB a k %d: la corsa del mattone si ferma (il principale ha la precedenza)" % (mem, MEM_MIN_GB, k)
                    print("### FERMO: %s" % fermo)
                    break
            if adesso - t1 > TETTO_S:
                fermo = "il tetto di %g s a k %d" % (TETTO_S, k)
                print("### FERMO: %s" % fermo)
                break
    # ---------------------------------------------------------------- il referto
    os.makedirs(DIR_REF, exist_ok=True)
    np.savez_compressed(os.path.join(DIR_REF, "%s_serie.npz" % caso), **{k: np.array(v) for k, v in S.items()})
    kk = np.array(S["k"])
    ult = kk >= kk[-1] - N_PIENO
    resp = np.array(S["resp"])[ult]
    amp = float(resp.max() - resp.min())
    cc = list(zip(np.array(S["c1"])[ult], np.array(S["c2"])[ult]))
    spost = max(distanza(81, c, cc[0]) for c in cc)     # ### L 81: il lato di TBS
    g = np.array(S["gauss"])
    g = g[g == g]
    print("-" * 130)
    print("### (%s) %d tick in %.0f s; il FERMO %s" % (caso, int(kk[-1]), time.time() - t00, fermo))
    print("    gli ultimi %d tick: il respiro (picco-picco) %.4f (la soglia %.2f, meta' di (B) del video triplo 0.594); il centro si sposta al piu' di %.4f nodi (la soglia %g)" % (N_PIENO, amp, SOGLIA_CALMO, spost, FERMO_CENTRO))
    if caso in ("MU", "MGU"):
        print("    il residuo di Gauss: il massimo sui controlli ogni %d tick %.3e (il DEVE: sotto %g)" % (OGNI_GAUSS, float(g.max()) if len(g) else float("nan"), TOLL_GAUSS))
    calmo = fermo is None and amp < SOGLIA_CALMO and spost <= FERMO_CENTRO
    print("  LA LETTURA (S5): %s" % ("CALMO" if calmo else "NON CALMO"))
    print("=" * 130)
    ok_gauss = True if caso == "MG" else (len(g) > 0 and float(g.max()) < TOLL_GAUSS)
    print("ESITO: calmo %s; Gauss sotto %g: %s" % (calmo, TOLL_GAUSS, ok_gauss))
    return 0 if (calmo and ok_gauss) else 1


# =====================================================================================
#   IL CONTROLLO DEL METODO (S7)
# =====================================================================================
def controllo(caso, nome_reg):
    import _presidio
    _presidio.avvia(__file__)
    from solitone import bordo as BO
    rho_c = rho_c_assoluto()
    f81 = os.path.join(DIR_E, "%s_%05d.npz" % (caso, K_RAMPA + N_PIENO))
    serie = np.load(os.path.join(DIR_REF, "%s_serie.npz" % caso))
    kk = serie["k"]
    ult = kk >= kk[-1] - N_PIENO
    amp_m = float(serie["resp"][ult].max() - serie["resp"][ult].min())
    t_m = T_BASE + K_RAMPA + N_PIENO
    print("=" * 130)
    print("IL CONTROLLO DEL METODO (%s, S7): il francobollo del mattone (%s) su L 162 nella scena di S162; %d tick coi campi pieni; il respiro del mattone negli ultimi %d tick %.4f" % (caso, f81, N_CONTROLLO, N_PIENO, amp_m))
    print("=" * 130)
    with scena(CORSA_BASE, T_BASE) as Z81:
        with np.load(f81) as d:
            Z81["metti"]({k: d[k] for k in Z81["chiavi"]})
            campo81 = (d["campo_A"].copy(), d["campo_E"].copy()) if "campo_A" in d.files else None
        rho81 = rho_di(Z81)
        c81 = centro_di(Z81, rho81)
        st81 = {k: Z81["st"][k].copy() for k in Z81["chiavi"]}
        E81 = energia(Z81)
        vuoto_fresco(Z81, t_m)
        phi_rif81 = Z81["st"]["phi_h"].copy()
        E81_vuoto = energia(Z81)
        Z81["metti"](st81)
        fr = ritaglia(Z81, c81, phi_rif81)
    E_sol = E81 - E81_vuoto
    print("### il francobollo: R_t %.1f (l'anello del vuoto %d); %d nodi; il centro d'origine %s; E_sol = E(mattone) - E(vuoto fresco a L 81) = %.6e" % (fr["R_t"], fr["anello_vuoto"], len(fr["w"]), fr["centro"], E_sol))
    with scena(CORSA_162, T_162) as Z:
        c_s = centro_di(Z, rho_di(Z))
        cd = [int(round(c_s[i])) for i in (0, 1)]
        cd = [cd[i] - ((cd[i] - fr["centro"][i]) % 3) for i in (0, 1)]          # ### lo spostamento multiplo di 3
        t0 = G2.T0
        vuoto_fresco(Z, t0)
        E_v162 = energia(Z)
        salvo = {k: Z["st"][k].copy() for k in Z["chiavi"]}
        out = {}
        for allinea in (False, True):
            for k in Z["chiavi"]:
                Z["st"][k][...] = salvo[k]
            D = incolla(Z, fr, cd, allinea)
            out[allinea] = (D, energia(Z) - E_v162 - E_sol)
        print("### incollato a %s (S162: il solitone a (%.2f, %.2f)); il salto di energia all'incollatura E - E(vuoto 162) - E_sol: allineato %.6e (Delta %.6f), NON allineato %.6e"
              % (cd, c_s[0], c_s[1], out[True][1], out[True][0], out[False][1]))
        C = Campi(Z, caso, rho_c, PB.E_DECISO)
        if C.campo is not None:
            rho = rho_di(Z)
            C.campo.A[...] = 0.0
            C.campo.E[...] = C.gauss(PB.E_DECISO * (rho - rho.mean()))
            C.campo.e = PB.E_DECISO
            C.e_prec = PB.E_DECISO
        rho = rho_di(Z)
        c0 = centro_di(Z, rho)
        R = [respiro(rho)]
        cen = [c0]
        gmax = C.residuo()
        t1 = t_tappa = time.time()
        for k in range(1, N_CONTROLLO + 1):
            C.tick(k, t0 + k, 1.0, PB.E_DECISO if caso in ("MU", "MGU") else 0.0)
            if k % OGNI == 0:
                rho = rho_di(Z)
                R.append(respiro(rho))
                cen.append(centro_di(Z, rho))
                if k % OGNI_GAUSS == 0:
                    gmax = max(gmax, C.residuo())
            if time.time() - t_tappa >= TAPPA_S:
                tappa(nome_reg, "k %d; %.3f s per tick; la memoria libera %.2f GB" % (k, (time.time() - t1) / k, memoria_gb()))
                t_tappa = time.time()
        spost = max(distanza(Z["L"], c, cen[0]) for c in cen)
        amp = float(max(R) - min(R))
    print("-" * 130)
    print("### %d tick in %.0f s: il centro si sposta al piu' di %.4f nodi (la soglia %g); il respiro %.4f contro il mattone %.4f (il rapporto %.3f; la tolleranza %g)"
          % (N_CONTROLLO, time.time() - t1, spost, FERMO_CENTRO, amp, amp_m, amp / amp_m if amp_m else float("inf"), TOLL_RESPIRO))
    if caso in ("MU", "MGU"):
        print("    il residuo di Gauss: il massimo %.3e (sotto %g)" % (gmax, TOLL_GAUSS))
    ok = spost <= FERMO_CENTRO and abs(amp - amp_m) <= TOLL_RESPIRO * amp_m and (caso == "MG" or gmax < TOLL_GAUSS)
    print("=" * 130)
    print("ESITO: il controllo del metodo %s" % ("PASSA" if ok else "### FALLISCE"))
    return 0 if ok else 1


def main(argv):
    if argv and argv[0] == "registro":
        return registro(argv[1:])
    ap = argparse.ArgumentParser()
    ap.add_argument("azione", choices=("prepara", "controllo"))
    ap.add_argument("--caso", required=True, choices=CASI)
    ap.add_argument("--registro")
    x = ap.parse_args(argv)
    return prepara(x.caso, x.registro) if x.azione == "prepara" else controllo(x.caso, x.registro)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
