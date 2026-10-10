r"""LE LETTURE DEL `v3` — **e le soglie sono quelle del task history, scritte PRIMA.**

> ### ⛔ **NIENTE SI DECIDE QUI.** Criteri, previsioni e soglie stanno in
> `doc/TASK_HISTORY/2026-10-11_prototipo_camminata_v3.md`, **committato prima del codice**.

| | la lettura | che cosa misura |
|---|---|---|
| `R` | **REGRESSIONE** | con `N` spento, lo spinore e' quello del `v2` **al bit** |
| `G` `1` `2` | gauge, isotropia, cono | **con il vuoto e `N` accesi** |
| `5` | **`C`** | le **tre** non linearita' *(elicita' locale, `(D)`, `(E)`)* piu' il controllo su `rho` |
| `V` | **REVERSIBILITA'** | `k` avanti e `k` indietro |
| `3` | **conservazione modificata** | le norme, e `quasi-energia lineare + Σ N_k` |
| `T` | **AUTOINTRAPPOLAMENTO** | la frazione entro `R` archi, **contro il fondo uniforme** |
| `F` | **la frequenza del grumo** | dalla fase nel tempo, e **se il grumo sta fermo** |
| `A` | **materia/antimateria** | il grumo e il suo **coniugato** |
| `L` | **il vuoto risponde** | `Λ` attorno al grumo, **letto e non interpretato** |
| `C` | **risonanza dei cicli** | si scansiona **l'olonomia** e si contano gli stati a `±1` |
| `S` | **la velocita' rispetto al CONO** | la pendenza di `distanza(t)`, in **archi per tick** |

### ⚠ **E LA GRANDEZZA CONSERVATA SI CHIAMA <<CONSERVAZIONE MODIFICATA>>, non <<energia>>:**
il task history diceva *«energia modificata»*, e **la promozione a <<energia>> e' una decisione
di Luca**, non mia.

Gira con:  python proto_camminata/_letture3.py
"""
import io
import json
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
sys.path.insert(0, _QUI)
sys.path.insert(0, os.path.join(RADICE, "csv"))
import _presidio                                              # noqa: E402

_presidio.avvia(__file__)

import camminata as CM                                         # noqa: E402
import camminata2 as C2                                        # noqa: E402
import camminata3 as C3                                        # noqa: E402
import geometria as GE                                         # noqa: E402
import interferenza3 as I3                                     # noqa: E402
import nonlineare2 as N2                                       # noqa: E402
import saturazione3 as S3                                      # noqa: E402
import scena as SC                                             # noqa: E402
import vuoto3 as V3                                            # noqa: E402
import _letture as L1                                          # noqa: E402

EPS = float(np.finfo(float).eps)
NLN = chr(10)
USCITE = os.path.join(_QUI, "uscite")
SEMI = (11, 23, 37, 53)
PASSI = 40
PASSI_LUNGHI = 200
EPS_RIF = 0.5
# ### ⛔ **`x0` SCANSIONATO SU POTENZE DI DUE**, da `1/8` a `8`: il ginocchio di `G'` e-
# ### a `x ~ 1`, quindi la scansione lo ### **attraversa** invece di sfiorarlo.
X0_SCANSIONE = (0.125, 0.5, 1.0, 2.0, 8.0)
RAGGI = (1, 2, 3)
# ### le tre non linearita-, affiancate
LE_TRE = (("N", S3.flusso), ("D", I3.flusso_D), ("E", I3.flusso_E))


def _autovettore_piu(n):
    """Lo spinore con `s.n = +1`: `(cos(th/2), e^{i fi} sin(th/2))`."""
    th = math.acos(max(-1.0, min(1.0, float(n[2]))))
    fi = math.atan2(float(n[1]), float(n[0]))
    return np.array([math.cos(0.5 * th),
                     complex(math.cos(fi), math.sin(fi)) * math.sin(0.5 * th)],
                    dtype=complex)


def grumo(sc, geo, centro, raggio, x0, lam0=V3.LAMBDA0, seme=11):
    """### Un grumo ### **allineato ai versori** *(`h > 0`)*, scalato per avere `x0`.

    ### ⭐ **E LA SCALA SI RICAVA, non si tara:** `h` e' ### **quadratica
    nell'ampiezza** e `Lambda` non dipende da lei, quindi ### **un solo passaggio** porta
    `x0` al valore voluto.
    """
    d = SC.distanze(sc, centro)
    dentro = [k for k in range(sc["n"]) if 0 <= d[k] <= raggio]
    psi = CM.stato_zero(sc)
    for e in range(2 * sc["m"]):
        if int(d[int(sc["nodo"][e])]) <= raggio:
            psi[e] = _autovettore_piu(geo["n"][e])
    psi = psi / math.sqrt(CM.norma(psi))
    phi = V3.vuoto_fondo(sc, lam0, seme)
    h = N2.elicita_nodo(psi, sc, geo)
    lam = V3.lambda_nodo(phi, sc)
    x = float(np.max(h[dentro] / lam[dentro]))
    psi = psi * math.sqrt(x0 / x) if x > 0 else psi
    return {"psi": psi, "phi": phi}, dentro, d


def frazione_entro(sc, st, centro, d, raggio):
    """La frazione di `rho` entro `raggio` archi dal centro."""
    rho = CM.rho_nodo(st["psi"], sc)
    tot = float(np.sum(rho))
    if tot <= 0:
        return float("nan")
    return float(np.sum(rho[d <= raggio]) / tot)


def fondo_uniforme(sc, d, raggio):
    """### **LA SOGLIA `S8`:** cio' che un'ampiezza **SPARSA** darebbe."""
    return float(np.sum(d <= raggio) / sc["n"])


def nodo_massimo(sc, st):
    return int(np.argmax(CM.rho_nodo(st["psi"], sc)))


def conservazione_modificata(st, sc, geo, r, dt, eps, quale="N"):
    """### La **quasi-energia lineare** piu' `Σ N_k`. ### ⚠ **NON si chiama <<energia>>.**"""
    # ### ⛔ **IL `quale` NON E- UN ABBELLIMENTO: era un DIFETTO MIO.** Al primo
    # ### giro misuravo **sempre la `N` del `v3`** *(quella sull-elicita- locale)*,
    # ### anche mentre giravano `(D)` e `(E)` -- che conservano **UN-ALTRA `N`.**
    # ### ⚠ **Il risultato era <<(D) DERIVA>>**, che non diceva niente di `(D)`:
    # ### diceva che **stavo misurando la grandezza sbagliata.**
    # ### ✅ **E l-ho visto perche- l-esponente contro `dtau` veniva `~0`:** una
    # ### deriva che **non scende con `dtau`** non e- splitting, quindi **o la grandezza
    # ### non e- conservata, o non e- LA SUA.**
    u = C2.passo2(st["psi"], sc, geo, r, dt, eps)
    lin = float(np.real(np.sum(np.conj(st["psi"]) * u)))
    lam = V3.lambda_nodo(st["phi"], sc)
    if quale == "N":
        num = N2.elicita_nodo(st["psi"], sc, geo)
    elif quale == "D":
        num = I3.elicita_interferenza(st["psi"], sc, geo)
    elif quale == "E":
        num = np.sum(np.abs(I3.campo_S(st["psi"], sc)) ** 2, axis=1)
    else:
        # ### `v2` e `lineare` NON hanno nessuna `N`: il `v2` e- una fase messa a mano
        # ### (non viene da un-energia), e il lineare non ha non linearita-. Quindi il
        # ### candidato e- la SOLA quasi-energia lineare, e per il `v2` DEVE derivare.
        return lin
    return lin + float(np.sum(S3.energia(num, lam)))


def distanza_media_e_fronte(sc, st, d):
    """### `(distanza media pesata, fronte al 95%)` ### **in archi**, sul grafo."""
    rho = CM.rho_nodo(st["psi"], sc)
    tot = float(np.sum(rho))
    if tot <= 0:
        return float("nan"), float("nan")
    media = float(np.sum(rho * d) / tot)
    ordine = np.argsort(d)
    cum = np.cumsum(rho[ordine]) / tot
    j = int(np.searchsorted(cum, 0.95))
    fronte = float(d[ordine[min(j, len(ordine) - 1)]])
    return media, fronte


def pendenza(x, y):
    return L1.pendenza(x, y)


def main():
    SC._niente_simulatore()
    os.makedirs(USCITE, exist_ok=True)
    sc = SC.irregolare()
    reg = SC.regolare()
    uno = np.ones(sc["n"], dtype=float)
    nest = 2 * sc["m"]
    gmax = int(sc["grado"].max())
    ident = GE.scena_identita(sc)
    gauge = GE.scena_gauge_puro(sc, SEMI[0])
    curva = GE.scena_curva(sc, SEMI[0])
    SCENE = (("identita", ident), ("gauge_puro", gauge), ("curva", curva))
    st0 = C3.stato3(sc, SEMI[0])
    tol = PASSI * gmax * EPS * math.sqrt(CM.norma(st0["psi"]))
    tolN = PASSI * nest * EPS
    out = {"scena": {"nome": sc["nome"], "n": sc["n"], "archi": sc["m"],
                     "estremita": nest, "regolare": reg["nome"],
                     "eps_riferimento": EPS_RIF, "semi": list(SEMI),
                     "passi": PASSI, "passi_lunghi": PASSI_LUNGHI,
                     "x0_scansione": list(X0_SCANSIONE), "raggi": list(RAGGI),
                     "soglia_S1": tol, "soglia_S3": tolN},
           "letture": {}}
    print("=" * 100)
    print("LE LETTURE DEL PROTOTIPO v3")
    print("=" * 100)
    print("  scena: %s   soglia S1 = %.3g" % (sc["nome"], tol))

    # ================================================================ (R)
    reg_r = {}
    for nome, geo in SCENE:
        a = st0["psi"].copy()
        for _ in range(PASSI):
            a = C2.passo2(a, sc, geo, uno, 1.0, EPS_RIF)
        b = dict(st0)
        for _ in range(PASSI):
            b = C3.passo3(b, sc, geo, uno, 1.0, EPS_RIF, None)
        reg_r[nome] = float(np.max(np.abs(b["psi"] - a)))
    out["letture"]["R_regressione"] = reg_r
    print("  R   regressione al v2: %s"
          % "  ".join("%s %.3g" % (k, v) for k, v in reg_r.items()))

    # ================================================================ (G) (1) (2)
    def ruota(p, g, fi):
        o = np.empty_like(p)
        for e in range(p.shape[0]):
            k = int(sc["nodo"][e])
            o[e] = np.exp(1j * fi[k]) * (g[k] @ p[e])
        return o

    si, sg = dict(st0), {"psi": ruota(st0["psi"], gauge["g"], gauge["fi"]),
                         "phi": st0["phi"].copy()}
    for _ in range(PASSI):
        si = C3.passo3(si, sc, ident, uno, 1.0, EPS_RIF, S3.flusso)
        sg = C3.passo3(sg, sc, gauge, uno, 1.0, EPS_RIF, S3.flusso)
    out["letture"]["G_gauge"] = {
        "densita": float(np.max(np.abs(CM.rho_nodo(si["psi"], sc)
                                       - CM.rho_nodo(sg["psi"], sc)))),
        "soglia": tol}
    nuova, pn, mappa = SC.rinumera(sc, 23)
    pas = [(int(mappa[2 * a]) // 2, int(mappa[2 * a]) % 2 == 1) for a in range(sc["m"])]
    n2 = np.zeros_like(ident["n"])
    n2[mappa] = ident["n"]
    U2 = np.zeros_like(ident["U"])
    for a_v, (a_n, girato) in enumerate(pas):
        U2[a_n] = ident["U"][a_v].conj().T if girato else ident["U"][a_v]
    g2 = {"nome": "portata", "U": U2, "n": n2, "come": "portata"}
    pp = {"psi": np.zeros_like(st0["psi"]), "phi": np.zeros_like(st0["phi"])}
    pp["psi"][mappa] = st0["psi"]
    pp["phi"][mappa] = st0["phi"]
    aa, bb = dict(st0), pp
    for _ in range(PASSI):
        aa = C3.passo3(aa, sc, ident, uno, 1.0, EPS_RIF, S3.flusso)
        bb = C3.passo3(bb, nuova, g2, np.ones(sc["n"]), 1.0, EPS_RIF, S3.flusso)
    rip = np.zeros_like(bb["psi"])
    rip[mappa] = aa["psi"]
    out["letture"]["1_isotropia"] = {"valore": float(np.max(np.abs(rip - bb["psi"]))),
                                     "soglia": tol}
    d0 = SC.distanze(sc, 0)
    T = max(1, int(d0.max()) // 2)
    e0 = int(np.nonzero(sc["nodo"] == 0)[0][0])
    u1 = {"psi": CM.stato_zero(sc), "phi": V3.vuoto_fondo(sc, V3.LAMBDA0, SEMI[0])}
    u1["psi"][e0, 0] = 1.0
    u2 = {"psi": u1["psi"].copy(), "phi": u1["phi"].copy()}
    u2["psi"][e0, 0] = 1.0 + 1e-3
    for _ in range(T):
        u1 = C3.passo3(u1, sc, curva, uno, 1.0, EPS_RIF, S3.flusso)
        u2 = C3.passo3(u2, sc, curva, uno, 1.0, EPS_RIF, S3.flusso)
    dif = np.abs(u1["psi"] - u2["psi"]).sum(axis=1)
    fu = dif[d0[sc["nodo"]] > T]
    out["letture"]["2_cono"] = {"T": T, "max_fuori": float(np.max(fu)) if fu.size else -1.0,
                                "estremita_fuori": int(fu.size)}
    print("  G12 gauge %.3g   isotropia %.3g   cono %.3g (T=%d)"
          % (out["letture"]["G_gauge"]["densita"], out["letture"]["1_isotropia"]["valore"],
             out["letture"]["2_cono"]["max_fuori"], T))

    # ================================================================ (5) e (V)
    cinque, vv = {}, {}
    for et, fl in LE_TRE + (("rho", S3.flusso_su_rho),):
        a = C3.coniuga3(C3.passo3(st0, sc, ident, uno, 1.0, EPS_RIF, fl))
        b = C3.passo3(C3.coniuga3(st0), sc, ident, uno, 1.0, EPS_RIF, fl)
        cinque[et] = float(np.max(np.abs(a["psi"] - b["psi"])))
    for et, fl in LE_TRE:
        k = 20
        c = dict(st0)
        for _ in range(k):
            c = C3.passo3(c, sc, curva, uno, 1.0, EPS_RIF, fl)
        for _ in range(k):
            c = C3.passo3_inverso(c, sc, curva, uno, 1.0, EPS_RIF, fl)
        vv[et] = {"psi": float(np.max(np.abs(c["psi"] - st0["psi"]))),
                  "phi": float(np.max(np.abs(c["phi"] - st0["phi"]))),
                  "soglia": 2 * k * nest * EPS}
    out["letture"]["5_C"] = {"valori": cinque, "soglia": tol}
    out["letture"]["V_reversibilita"] = vv
    print("  5   C: %s   (il controllo rho DEVE rompere)"
          % "  ".join("%s %.3g" % (k, v) for k, v in cinque.items()))

    # ================================================================ (3)
    # ### ⛔ **E LA DERIVA SI MISURA IN FUNZIONE DI `dtau`, non a `dtau = 1`
    # ### soltanto**, e il motivo e- che cambia la CONCLUSIONE: la composizione di Strang
    # ### ha un errore ### **`O(dtau^2)` sul tempo fisico fissato**, quindi una deriva che
    # ### ### **scende come `dtau^2`** dice ### **<<la grandezza E- conservata dal flusso
    # ### continuo, e quella deriva e- lo SPLITTING>>**, mentre una deriva che
    # ### ### **non scende** dice ### **<<non e- conservata>>.**
    # ### ⚠ **Sono due risposte opposte alla stessa domanda**, e a `dtau = 1`
    # ### ### **non si distinguono.**
    tre = {}
    T_FISICO = 50.0
    for et, fl in LE_TRE + (("v2", S3.flusso_v2), ("lineare", None)):
        per_dt = {}
        for dt in (1.0, 0.5, 0.25):
            passi = int(round(T_FISICO / dt))
            serie, tempo = [], []
            s = dict(st0)
            for i in range(1, passi + 1):
                s = C3.passo3(s, sc, curva, uno, dt, EPS_RIF, fl)
                if i % max(1, passi // 25) == 0:
                    serie.append(conservazione_modificata(s, sc, curva, uno, dt,
                                                      EPS_RIF, et))
                    tempo.append(i * dt)
            ris = passi * nest * EPS * (float(np.max(np.abs(serie))) or 1.0)
            cl = L1.classifica(tempo, serie, ris)
            per_dt["%g" % dt] = {
                "esito": cl["esito"], "pendenza": cl["pendenza"], "sigma": cl["sigma"],
                "escursione": cl.get("escursione"), "risoluzione": ris, "passi": passi,
                "norma_psi": abs(CM.norma(s["psi"]) - CM.norma(st0["psi"])),
                "norma_phi": abs(V3.norma_vuoto(s["phi"])
                                 - V3.norma_vuoto(st0["phi"]))}
        # ### la pendenza della DERIVA contro `dtau`, in log-log
        xs = [math.log(dt) for dt in (1.0, 0.5, 0.25)]
        ys = [math.log(abs(per_dt["%g" % dt]["pendenza"]) + 1e-300)
              for dt in (1.0, 0.5, 0.25)]
        esp, sesp = L1.pendenza(xs, ys)
        tre[et] = {"per_dtau": per_dt, "esponente": esp, "sigma_esponente": sesp}
    out["letture"]["3_conservazione_modificata"] = tre
    # ### ⛔ **LA LETTURA `3b`: LO STESSO CONTO COL SOTTO-PASSO FISSATO.**
    # ### ⚠ **Col sotto-passo ADATTIVO l-esponente non vuol dire niente**,
    # ### perche- il sotto-passo effettivo ### **cambia con `dtau`**: `3b` lo fissa a `4`
    # ### e rimisura. ### ✅ **Se l-esponente diventa `~2`, la deriva era
    # ### SPLITTING; se resta `~0`, la grandezza NON e- conservata da quel flusso** --
    # ### e sono ### **due risposte opposte.**
    treb = {}
    for et, fl in (("D", I3.flusso_D_fisso), ("E", I3.flusso_E_fisso)):
        per_dt = {}
        for dt in (1.0, 0.5, 0.25):
            passi = int(round(T_FISICO / dt))
            serie, tempo = [], []
            s = dict(st0)
            for i in range(1, passi + 1):
                s = C3.passo3(s, sc, curva, uno, dt, EPS_RIF, fl)
                if i % max(1, passi // 25) == 0:
                    serie.append(conservazione_modificata(s, sc, curva, uno, dt,
                                                          EPS_RIF, et))
                    tempo.append(i * dt)
            ris = passi * nest * EPS * (float(np.max(np.abs(serie))) or 1.0)
            cl = L1.classifica(tempo, serie, ris)
            per_dt["%g" % dt] = {"esito": cl["esito"], "pendenza": cl["pendenza"],
                                 "sigma": cl["sigma"], "passi": passi}
        xs = [math.log(dt) for dt in (1.0, 0.5, 0.25)]
        ys = [math.log(abs(per_dt["%g" % dt]["pendenza"]) + 1e-300)
              for dt in (1.0, 0.5, 0.25)]
        esp, sesp = L1.pendenza(xs, ys)
        treb[et] = {"per_dtau": per_dt, "esponente": esp, "sigma_esponente": sesp,
                    "sotto_fissato": 4}
    out["letture"]["3b_sotto_fissato"] = treb
    print("  3b  con il sotto-passo FISSATO a 4:")
    for k, v in treb.items():
        print("        %-8s dtau=1: %-20s   esponente %.2f +/- %.2f"
              % (k, v["per_dtau"]["1"]["esito"], v["esponente"], v["sigma_esponente"]))
    print("  3   conservazione modificata, deriva contro dtau (esponente):")
    for k, v in tre.items():
        print("        %-8s dtau=1: %-20s   esponente %.2f +/- %.2f"
              % (k, v["per_dtau"]["1"]["esito"], v["esponente"], v["sigma_esponente"]))

    # ================================================================ (T) (F) (A) (L)
    out["letture"]["T_intrappolamento"] = {}
    out["letture"]["F_frequenza"] = {}
    out["letture"]["A_materia"] = {}
    out["letture"]["L_vuoto"] = {}
    centro = 0
    for et, fl in LE_TRE + (("lineare", None),):
        for x0 in X0_SCANSIONE:
            ch = "%s x0=%g" % (et, x0)
            st, dentro, d = grumo(sc, ident, centro, 1, x0, seme=SEMI[0])
            fondi = {str(r): fondo_uniforme(sc, d, r) for r in RAGGI}
            lam0 = V3.lambda_nodo(st["phi"], sc)[dentro].mean()
            serie_c, serie_l, fasi, tempo = [], [], [], []
            s = dict(st)
            for t in range(1, PASSI + 1):
                s = C3.passo3(s, sc, ident, uno, 1.0, EPS_RIF, fl)
                serie_c.append(I3.coerenza(s["psi"], sc)[dentro].mean())
                serie_l.append(float(V3.lambda_nodo(s["phi"], sc)[dentro].mean()))
                S = I3.campo_S(s["psi"], sc)
                fasi.append(float(np.angle(np.sum(S[dentro]))))
                tempo.append(t)
            fr = {str(r): frazione_entro(sc, s, centro, d, r) for r in RAGGI}
            rho = CM.rho_nodo(s["psi"], sc)
            out["letture"]["T_intrappolamento"][ch] = {
                "frazione": fr, "fondo_uniforme": fondi,
                "rapporto": {k: fr[k] / fondi[k] for k in fr},
                "massimo_su_un_nodo": float(np.max(rho) / np.sum(rho)),
                "coerenza_media_fine": float(serie_c[-1]),
                "coerenza_media_inizio": float(serie_c[0])}
            # (F) la frequenza interna, dalla fase nel tempo (srotolata)
            f_un = np.unwrap(np.array(fasi))
            om, sg2 = pendenza(tempo, f_un)
            out["letture"]["F_frequenza"][ch] = {
                "omega_per_tick": om, "sigma": sg2,
                "nodo_massimo": nodo_massimo(sc, s),
                "distanza_del_massimo": int(d[nodo_massimo(sc, s)])}
            # (L) il vuoto risponde
            out["letture"]["L_vuoto"][ch] = {
                "Lambda_inizio": float(lam0), "Lambda_fine": float(serie_l[-1]),
                "variazione_relativa": float((serie_l[-1] - lam0) / lam0)}
            # (A) materia / antimateria
            if x0 in (1.0, 8.0):
                sc_ = C3.coniuga3(st)
                p, q = dict(st), sc_
                for _ in range(PASSI):
                    p = C3.passo3(p, sc, ident, uno, 1.0, EPS_RIF, fl)
                    q = C3.passo3(q, sc, ident, uno, 1.0, EPS_RIF, fl)
                fp = frazione_entro(sc, p, centro, d, 1)
                fq = frazione_entro(sc, q, centro, d, 1)
                out["letture"]["A_materia"][ch] = {
                    "frazione_piu": fp, "frazione_meno": fq,
                    "asimmetria": abs(fp - fq) / (fp + fq) if (fp + fq) else -1.0,
                    "coniugazione": float(np.max(np.abs(C3.coniuga3(p)["psi"]
                                                        - q["psi"])))}
        print("  T   %-9s %s" % (et, "  ".join(
            "x0=%g: %.2f" % (x0, out["letture"]["T_intrappolamento"]["%s x0=%g"
                                                                    % (et, x0)]
                             ["rapporto"]["1"]) for x0 in X0_SCANSIONE)))

    # ================================================================ (S)
    out["letture"]["S_velocita"] = velocita(reg, sc, ident, curva)

    # ================================================================ (C)
    out["letture"]["C_risonanza"] = risonanza(sc)

    # ### ✅ **E I SOTTO-PASSI USATI SI DICHIARANO**, perche- un numero
    # ### derivato che nessuno guarda ### **non e- una dichiarazione.**
    out["sotto_passi_usati"] = dict(I3.SOTTO_USATI)
    print("  ### i sotto-passi del punto medio, DERIVATI dalla convergenza: %s"
          % (out["sotto_passi_usati"] or "nessuno: il punto medio non e- servito"))
    dati = (json.dumps(out, indent=1, ensure_ascii=False, sort_keys=True,
                       default=float) + NLN).encode("utf-8")
    io.open(os.path.join(USCITE, "letture_v3.json"), "wb").write(dati)
    print("  " + "-" * 96)
    print("  scritto proto_camminata/uscite/letture_v3.json")
    print("=" * 100)
    return 0


def velocita(reg, sc, ident, curva):
    """### **(S) LA VELOCITA' RISPETTO AL CONO**, in archi per tick.

    ### ⚠ **La scena principale e' il REGOLARE**, e il motivo e' dichiarato nel task
    history: sull'irregolare l'eccentricita' e' `6`, quindi **il fronte satura in sei
    tick.**
    """
    fuori = {"regolare": {}, "irregolare": {}, "nota": ""}
    EPSG = (0.0, 0.125, 0.25, 0.375, 0.5, 0.75, 1.0)
    for nome_g, scg in (("regolare", reg), ("irregolare", sc)):
        d0 = SC.distanze(scg, 0)
        ecc = int(d0.max())
        tick = max(4, min(24, ecc - 2))
        uno = np.ones(scg["n"], dtype=float)
        for nome_s, geo in (("identita", GE.scena_identita(scg)),
                            ("curva", GE.scena_curva(scg, 11))):
            per_eps = {}
            for eps in EPSG:
                psi = CM.stato_zero(scg)
                for e in range(2 * scg["m"]):
                    if int(scg["nodo"][e]) == 0:
                        psi[e] = _autovettore_piu(geo["n"][e])
                psi = psi / math.sqrt(CM.norma(psi))
                st = {"psi": psi, "phi": V3.vuoto_zero(scg)}
                med, fro, tt = [], [], []
                for t in range(1, tick + 1):
                    st = C3.passo3(st, scg, geo, uno, 1.0, eps, None)
                    m, f = distanza_media_e_fronte(scg, st, d0)
                    med.append(m)
                    fro.append(f)
                    tt.append(t)
                vm, sm = L1.pendenza(tt, med)
                vf, sf = L1.pendenza(tt, fro)
                per_eps["%g" % eps] = {"velocita_media": vm, "sigma_media": sm,
                                       "velocita_fronte": vf, "sigma_fronte": sf,
                                       "tick": tick, "eccentricita": ecc}
            fuori[nome_g][nome_s] = per_eps
    # ### l-ISOTROPIA DELLA PROPAGAZIONE, sul regolare: da nodi diversi
    uno = np.ones(reg["n"], dtype=float)
    geo = GE.scena_identita(reg)
    da_nodi = {}
    for nodo in (0, 7, 31, 60):
        d0 = SC.distanze(reg, nodo)
        psi = CM.stato_zero(reg)
        for e in range(2 * reg["m"]):
            if int(reg["nodo"][e]) == nodo:
                psi[e] = _autovettore_piu(geo["n"][e])
        psi = psi / math.sqrt(CM.norma(psi))
        st = {"psi": psi, "phi": V3.vuoto_zero(reg)}
        med, tt = [], []
        for t in range(1, 25):
            st = C3.passo3(st, reg, geo, uno, 1.0, 0.5, None)
            m, _f = distanza_media_e_fronte(reg, st, d0)
            med.append(m)
            tt.append(t)
        v, s = L1.pendenza(tt, med)
        da_nodi[str(nodo)] = {"velocita": v, "sigma": s}
    fuori["isotropia_da_nodi"] = da_nodi
    vs = [x["velocita"] for x in da_nodi.values()]
    ss = [x["sigma"] for x in da_nodi.values()]
    fuori["isotropia_entro_3sigma"] = bool(
        max(vs) - min(vs) <= 3.0 * max(ss) if ss else False)
    print("  S   velocita- del fronte sul REGOLARE (identita), archi per tick:")
    print("        %s" % "  ".join(
        "eps=%s: %.3f" % (k, v["velocita_fronte"])
        for k, v in sorted(fuori["regolare"]["identita"].items(), key=lambda z: float(z[0]))))
    print("        e la media pesata: %s" % "  ".join(
        "eps=%s: %.3f" % (k, v["velocita_media"])
        for k, v in sorted(fuori["regolare"]["identita"].items(), key=lambda z: float(z[0]))))
    print("        isotropia da 4 nodi: %s entro 3 sigma   (%s)"
          % ("SI" if fuori["isotropia_entro_3sigma"] else "NO",
             ", ".join("%.4f" % v for v in vs)))
    return fuori


def risonanza(sc):
    """### **(C) LA RISONANZA DEI CICLI:** si scansiona l'olonomia di **un** ciclo.

    ### ⛔ **E' un CONTROLLO LINEARE:** `N` non c'entra. La domanda e' se con `eps > 0`
    **tornino** stati intrappolati per qualche olonomia.
    """
    import camminata2 as C2b
    fuori = {}
    uno = np.ones(sc["n"], dtype=float)
    base = GE.scena_identita(sc)
    cicli = GE.cicli_corti(sc, 4)
    arco_di = {}
    for a, (u, v) in enumerate(sc["archi"]):
        arco_di[(u, v)] = a
        arco_di[(v, u)] = a
    c0 = cicli[0]
    a0 = arco_di[(c0[0], c0[1])]
    for frazione in (0.0, 0.25, 0.5, 0.75, 1.0):
        geo = {"nome": "ris", "U": base["U"].copy(), "n": base["n"],
               "come": "olonomia scansionata"}
        geo["U"][a0] = np.exp(1j * math.pi * frazione) * geo["U"][a0]
        per_eps = {}
        for eps in (0.0, 0.5):
            om, lam = C2b.quasi_energie(sc, geo, uno, 1.0, eps)
            per_eps["%g" % eps] = {
                "piu_uno": int(np.sum(np.abs(lam - 1.0) < 1e-10)),
                "meno_uno": int(np.sum(np.abs(lam + 1.0) < 1e-10))}
        fuori["%g" % frazione] = per_eps
    print("  C   risonanza dei cicli (olonomia scansionata su un ciclo):")
    for k, v in sorted(fuori.items(), key=lambda z: float(z[0])):
        print("        fase=%s pi:  eps=0 -> %d/%d   eps=0.5 -> %d/%d"
              % (k, v["0"]["piu_uno"], v["0"]["meno_uno"],
                 v["0.5"]["piu_uno"], v["0.5"]["meno_uno"]))
    return fuori


if __name__ == "__main__":
    sys.exit(main())
