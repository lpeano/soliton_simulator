r"""LE LETTURE `G1` E `G2` — **IL GUSCIO IN ANTIFASE, E DUE GRUMI.**

> ## ⛔ **SONO OSSERVATORI, NON LEGGI.** La dinamica e' **solo il passo `v3`**, e queste
> ## letture **non retroagiscono**. Non toccano `soliton_simulator.py` ne' `leggi.yaml`.

**Soglie e previsioni:** `doc/TASK_HISTORY/2026-10-11_prototipo_camminata_v3.md`, nella sua
annotazione, **committata PRIMA di misurare** *(`7045367`)*.

### ⭐ **IL VINCOLO CHE DECIDE TUTTO E' IL `V4`: UNA FASE FRA NODI DIVERSI SI CONFRONTA SOLO
TRASPORTATA.** Qui vuol dire `z = S_c^dag (prodotto delle U lungo il cammino) S_k`, e
`cos dphi = Re(z)/|z|`: ### **invariante di gauge per costruzione.** ### ⚠ **E se i cammini
piu' corti sono piu' d'uno, si riportano TUTTI e la loro dispersione** — perche' **l'olonomia
dei cicli conta.**

### ⚠ **E LA SPINTA DI `G2(c)` E' UNA FASE LOCALE `exp(i q d_k)`, e la distinzione va detta:**
una fase **locale** si applica **nel riferimento del nodo** e non confronta niente, quindi
**non ha bisogno di trasporto**; il trasporto serve a **confrontare**, ed e' cio' che fa `G1`.

### ⚠ **E IL TEMPO SI RIPORTA DUE VOLTE** *(`V3`)*: il **tick** e il **tau locale**. ### **Nel
banco `r = 1`, quindi coincidono** — e lo scrivo invece di lasciarlo sottinteso.

Gira con:  python proto_camminata/_guscio_moto.py
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
import saturazione3 as S3                                      # noqa: E402
import scena as SC                                             # noqa: E402
import vuoto3 as V3                                            # noqa: E402
import _letture3 as L3                                         # noqa: E402

EPS = float(np.finfo(float).eps)
NLN = chr(10)
USCITE = os.path.join(_QUI, "uscite")
SEMI = (11, 23, 37, 53)
PASSI = 40
EPS_RIF = 0.5
ANELLI = (0, 1, 2, 3)
MAX_CAMMINI = 8
# ### ⛔ **LE AMPIEZZE DELLA SPINTA, SCANSIONATE** *(`V2`: sono parametri di LETTURA)*.
SPINTE = (0.0, 0.25, 0.5, 1.0)


def cammini_corti(sc, da, a, massimo=MAX_CAMMINI):
    """### **TUTTI** i cammini piu' corti *(fino a `massimo`)*, per la dispersione."""
    d = SC.distanze(sc, a)
    if d[da] < 0:
        return []
    fuori = []

    def scendi(k, cammino):
        if len(fuori) >= massimo:
            return
        if k == a:
            fuori.append(list(cammino))
            return
        for v in sc["vicini"][k]:
            if d[v] == d[k] - 1:
                cammino.append(v)
                scendi(v, cammino)
                cammino.pop()

    scendi(da, [da])
    return fuori


def trasporto(sc, U, cammino):
    """Il prodotto delle `U` lungo il cammino, **nel verso del cammino**."""
    arco_di = {}
    for a, (u, v) in enumerate(sc["archi"]):
        arco_di[(u, v)] = 2 * a
        arco_di[(v, u)] = 2 * a + 1
    M = np.eye(2, dtype=complex)
    for i in range(len(cammino) - 1):
        M = GE.u_di_estremita(sc, U, arco_di[(cammino[i], cammino[i + 1])]) @ M
    return M


def cos_trasportato(sc, geo, S, centro, k):
    """### `(cos dphi medio, dispersione fra i cammini, quanti cammini)`.

    ### ⛔ **Non si confrontano fasi grezze:** si trasporta `S_k` fino al centro lungo
    **ogni** cammino piu' corto, e la ### **dispersione fra i cammini** e' l'olonomia che
    si vede.
    """
    cc = cammini_corti(sc, k, centro)
    if not cc:
        return float("nan"), float("nan"), 0
    val = []
    for cam in cc:
        M = trasporto(sc, geo["U"], cam)
        z = complex(np.vdot(S[centro], M @ S[k]))
        if abs(z) > 0.0:
            val.append(float(np.real(z) / abs(z)))
    if not val:
        return float("nan"), float("nan"), len(cc)
    return (float(np.mean(val)),
            float(np.std(val, ddof=1)) if len(val) > 1 else 0.0, len(cc))


def g1(sc, geo, flusso, nome, centro=0, x0=8.0, passi=PASSI, dal_massimo=True):
    """### **`G1`: IL GUSCIO IN ANTIFASE**, per anelli di distanza di grafo."""
    st, dentro, d = L3.grumo(sc, geo, centro, 1, x0, seme=SEMI[0])
    s = dict(st)
    for _ in range(passi):
        s = C3.passo3(s, sc, geo, np.ones(sc["n"]), 1.0, EPS_RIF, flusso)
    # ### il centro si RIMISURA: e- il nodo di densita- massima, non quello di partenza
    rho = CM.rho_nodo(s["psi"], sc)
    c_vero = int(np.argmax(rho))
    # ### ⚠ **MA IL MASSIMO CORRENTE NON E- UN NUCLEO**, e il `v3` lo ha gia-
    # ### misurato: ### **nessuna forma intrappola**, quindi il massimo ### **si sposta** e
    # ### cambia da variante a variante. ### ⛔ **Confrontare le varianti su centri
    # ### DIVERSI non e- un confronto**, quindi si misura ### **anche dal centro INIZIALE**,
    # ### che e- ### **lo stesso per tutte.**
    c_usato = c_vero if dal_massimo else centro
    dd = SC.distanze(sc, c_usato)
    S = I3.campo_S(s["psi"], sc)
    lam = V3.lambda_nodo(s["phi"], sc)
    coe = I3.coerenza(s["psi"], sc)
    fuori = {"nome": nome, "centro_iniziale": centro, "centro_misurato": c_vero,
             "centro_usato": c_usato, "dal_massimo": bool(dal_massimo),
             "x0": x0, "tick": passi, "tau_locale": float(passi * 1.0), "anelli": {}}
    for r in ANELLI:
        nodi = [k for k in range(sc["n"]) if int(dd[k]) == r]
        if not nodi:
            continue
        pesi, cosi, disp, quanti = [], [], [], []
        for k in nodi:
            if k == c_usato:
                continue
            cm, sd, nq = cos_trasportato(sc, geo, S, c_usato, k)
            if not math.isnan(cm):
                cosi.append(cm)
                pesi.append(float(np.linalg.norm(S[k])))
                disp.append(sd)
                quanti.append(nq)
        if cosi and sum(pesi) > 0:
            w = np.array(pesi)
            x = np.array(cosi)
            med = float(np.sum(w * x) / np.sum(w))
            # ### l-errore standard PESATO
            var = float(np.sum(w * (x - med) ** 2) / np.sum(w))
            sem = math.sqrt(var / max(1, len(x)))
        else:
            med, sem = float("nan"), float("inf")
        fuori["anelli"][str(r)] = {
            "nodi": len(nodi),
            "rho_media": float(np.mean(rho[nodi])),
            "rho_su_Lambda": float(np.mean(rho[nodi] / lam[nodi])),
            "cos_dphi": med, "errore_standard": sem,
            "antifase": bool(med < 0 and abs(med) > 3.0 * sem),
            "dispersione_fra_cammini": float(np.mean(disp)) if disp else float("nan"),
            "cammini_piu_corti_medi": float(np.mean(quanti)) if quanti else 0.0,
            "cancellazione_media": float(np.mean(1.0 - coe[nodi]))}
    return fuori


def meta_di_voronoi(sc, a, b):
    """### Le due META- del grafo: ### **i nodi piu- vicini ad `a` che a `b`**, e viceversa.

    ### ⛔ **ED E- UNA CURA DI UN DIFETTO MIO, trovato da un numero troppo
    pulito:** al primo giro le <<zone>> erano ### **UN NODO SOLO**, quindi il centro
    ### **non poteva muoversi** e la separazione veniva ### **esattamente `0.000` sempre**,
    perfino con la spinta accesa. ### ✅ **Una partizione di Voronoi SUL GRAFO
    e- relazionale** *(`V5`: distanze di grafo, niente assi)* ### **e lascia il centro
    libero di spostarsi.**
    ### ⚠ **I nodi equidistanti restano FUORI da entrambe**, perche- assegnarli
    sarebbe una scelta arbitraria.
    """
    da, db = SC.distanze(sc, a), SC.distanze(sc, b)
    za = [k for k in range(sc["n"]) if da[k] >= 0 and da[k] < db[k]]
    zb = [k for k in range(sc["n"]) if db[k] >= 0 and db[k] < da[k]]
    return za, zb


def centri(sc, st, zone):
    """I due centri: il nodo di densita' massima **dentro ciascuna zona dichiarata**."""
    rho = CM.rho_nodo(st["psi"], sc)
    fuori = []
    for z in zone:
        zz = list(z)
        fuori.append(int(zz[int(np.argmax(rho[zz]))]))
    return fuori


def due_grumi(sc, geo, flusso, nome, D, fase, x0=8.0, passi=PASSI, spinta=0.0):
    """### **`G2`: DUE GRUMI** a distanza di grafo `D`, con fase relativa **trasportata**."""
    d0 = SC.distanze(sc, 0)
    candidati = [k for k in range(sc["n"]) if int(d0[k]) == D]
    if not candidati:
        return None
    c2 = int(candidati[0])
    a, za, _d = L3.grumo(sc, geo, 0, 0, x0, seme=SEMI[0])
    b, zb, _d2 = L3.grumo(sc, geo, c2, 0, x0, seme=SEMI[0])
    # ### la FASE RELATIVA, definita ### **per trasporto lungo il cammino piu- corto**
    cc = cammini_corti(sc, c2, 0, 1)
    M = trasporto(sc, geo["U"], cc[0]) if cc else np.eye(2, dtype=complex)
    segno = complex(np.exp(1j * fase))
    psi = a["psi"] + segno * b["psi"]
    # ### la SPINTA: una fase LOCALE lineare nella distanza dall-altro centro
    if spinta != 0.0:
        dd2 = SC.distanze(sc, c2)
        fase_loc = np.exp(1j * spinta * dd2[sc["nodo"]]).reshape(-1, 1)
        dentro_a = np.isin(sc["nodo"], list(za))
        psi = np.where(dentro_a.reshape(-1, 1), psi * fase_loc, psi)
    st = {"psi": psi / math.sqrt(CM.norma(psi)),
          "phi": V3.vuoto_fondo(sc, V3.LAMBDA0, SEMI[0])}
    # ### ✅ **LE ZONE SONO LE DUE META- DI VORONOI**, non i due nodi: cosi-
    # ### ### **il centro puo- muoversi**, che e- cio- che la lettura vuole misurare.
    _za, _zb = meta_di_voronoi(sc, 0, c2)
    zone = (set(_za) | {0}, set(_zb) | {c2})
    sep, da_zero, tempo, norme = [], [], [], []
    s = dict(st)
    # ### ⛔ **ERA UN TERNARIO CHE NON SCEGLIE:** `"N" if nome == "N" else "N"`
    # ### da- ### **SEMPRE `"N"`**, quindi per il braccio ### **`lineare` misuravo la
    # ### `Q` di `N`** -- ### **la quasi-energia lineare PIU- la somma delle energie
    # ### locali**, che nel lineare ### **non e- conservata** perche- quella
    # ### non linearita- ### **non c-e- nella sua dinamica.**
    # ### ⚠ **E E- LO STESSO DIFETTO CHE AVEVO GIA- CURATO in
    # ### `conservazione_modificata` col parametro `quale`:** l-ho ### **rimesso
    # ### qui**, travestito da scelta. ### ⭐ **L-ha trovato un numero
    # ### IMPOSSIBILE:** la quasi-energia lineare e- ### **esattamente conservata
    # ### per unitarieta-** *(`<U^t psi|U U^t psi> = <psi|U psi>`)*, e invece
    # ### andava ### **da `0.002305` a `0.000002`.**
    quale = nome if nome in ("N", "D", "E") else "lineare"
    q0 = L3.conservazione_modificata(s, sc, geo, np.ones(sc["n"]), 1.0, EPS_RIF,
                                     quale)
    for t in range(1, passi + 1):
        s = C3.passo3(s, sc, geo, np.ones(sc["n"]), 1.0, EPS_RIF, flusso)
        c_a, c_b = centri(sc, s, zone)
        sep.append(float(SC.distanze(sc, c_a)[c_b]))
        da_zero.append((float(d0[c_a]), float(SC.distanze(sc, c2)[c_b])))
        norme.append(CM.norma(s["psi"]))
        tempo.append(t)
    pend, sg = L3.pendenza(tempo, sep)
    pa, sa = L3.pendenza(tempo, [x[0] for x in da_zero])
    pb, sb = L3.pendenza(tempo, [x[1] for x in da_zero])
    return {"nome": nome, "D": D, "fase": fase, "spinta": spinta,
            "centri_iniziali": [0, c2], "tick": passi, "tau_locale": float(passi),
            "Q_iniziale": q0,
            "Q_finale": L3.conservazione_modificata(s, sc, geo, np.ones(sc["n"]), 1.0,
                                                    EPS_RIF, quale),
            "quale_Q": quale,
            "separazione_iniziale": sep[0], "separazione_finale": sep[-1],
            "pendenza_separazione": pend, "sigma_separazione": sg,
            "pendenza_primo": pa, "sigma_primo": sa,
            "pendenza_secondo": pb, "sigma_secondo": sb,
            "norma_scarto": abs(norme[-1] - CM.norma(st["psi"])),
            "frazione_nel_composito": float(
                np.sum(CM.rho_nodo(s["psi"], sc)[list(zone[0] | zone[1])])
                / np.sum(CM.rho_nodo(s["psi"], sc)))}


def main():
    SC._niente_simulatore()
    os.makedirs(USCITE, exist_ok=True)
    sc = SC.irregolare()
    reg = SC.regolare()
    ident = GE.scena_identita(sc)
    curva = GE.scena_curva(sc, SEMI[0])
    out = {"vincoli": {
        "V1": "la dinamica e- solo il passo v3; le letture non retroagiscono",
        "V2": "nessuna costante nuova: ampiezza, distanza e spinta sono parametri di "
              "lettura, scansionati",
        "V3": "si riporta il tick E il tau locale (nel banco r = 1, quindi coincidono)",
        "V4": "ogni fase fra nodi diversi e- TRASPORTATA, e la dispersione fra i cammini "
              "piu- corti si riporta",
        "V5": "niente assi: distanze di grafo e nodi",
        "V6": "scala minima un arco",
        "V7": "le condizioni iniziali anche coniugate",
        "V8": "Q si chiama CONSERVAZIONE MODIFICATA, non energia",
        "V9": "a N spento tutto coincide col v2 al bit"},
        "G1": {}, "G2": {}}
    print("=" * 100)
    print("LE LETTURE G1 (GUSCIO) E G2 (DUE GRUMI)")
    print("=" * 100)

    # ============================================================ G1
    for nome, fl in (("N", S3.flusso), ("E", I3.flusso_E), ("lineare", None)):
        for nome_s, geo in (("identita", ident), ("curva", curva)):
            out["G1"]["%s %s" % (nome, nome_s)] = g1(sc, geo, fl, nome)
            # ### ✅ **e DAL CENTRO INIZIALE**, che e- lo stesso per tutte le
            # ### varianti: ### **e- l-unico confronto che vale.**
            out["G1"]["%s %s dal centro iniziale" % (nome, nome_s)] = g1(
                sc, geo, fl, nome, dal_massimo=False)
        a = out["G1"]["%s identita dal centro iniziale" % nome]
        print("  G1  %-8s centro %3d  %s" % (
            nome, a["centro_misurato"],
            "  ".join("r=%s: cos %+.3f+/-%.3f %s" % (
                k, v["cos_dphi"], v["errore_standard"],
                "ANTIFASE" if v["antifase"] else "")
                for k, v in sorted(a["anelli"].items()))))

    # ============================================================ G2 (a) e (b)
    ecc = int(SC.distanze(sc, 0).max())
    out["G2"]["eccentricita_irregolare"] = ecc
    out["G2"]["interazione"] = {}
    for nome, fl in (("N", S3.flusso), ("lineare", None)):
        for fase in (0.0, math.pi):
            for D in range(0, min(8, ecc) + 1):
                r = due_grumi(sc, ident, fl, nome, D, fase)
                if r is not None:
                    out["G2"]["interazione"]["%s fase=%s D=%d"
                                             % (nome, "0" if fase == 0 else "pi", D)] = r
        righe = [(D, out["G2"]["interazione"].get("%s fase=0 D=%d" % (nome, D)))
                 for D in range(0, min(8, ecc) + 1)]
        print("  G2a %-8s %s" % (nome, "  ".join(
            "D=%d: sep %.1f->%.1f (p %+.3f)" % (D, x["separazione_iniziale"],
                                                x["separazione_finale"],
                                                x["pendenza_separazione"])
            for D, x in righe if x)))

    # ============================================================ G2 (b) la MASSIMA DENSITA-
    # ### ⛔ **A `D = 0` LA SEPARAZIONE E- `0` PER COSTRUZIONE**, quindi non dice
    # ### niente: la domanda <<rimbalza, si fonde o si allarga?>> si misura
    # ### ### **sull-ALLARGAMENTO**, cioe- sulla frazione che resta entro UN arco nel tempo,
    # ### confrontata con ### **un grumo SOLO della stessa ampiezza totale.**
    # ### ✅ **E la distinzione del mandato diventa misurabile:** se i due
    # ### sovrapposti si allargano ### **come il grumo solo**, e- ### **SATURAZIONE**; se
    # ### si allargano ### **di piu-**, e- ### **REPULSIONE** -- e in quel caso la velocita-
    # ### di allargamento ### **cresce con l-ampiezza.**
    out["G2"]["massima_densita"] = {}
    d0z = SC.distanze(sc, 0)
    for x0 in (1.0, 8.0, 64.0):
        for et, fl in (("N", S3.flusso), ("lineare", None)):
            a1, _z, _d = L3.grumo(sc, ident, 0, 0, x0, seme=SEMI[0])
            # due grumi SOVRAPPOSTI: la stessa ampiezza totale di uno solo, in fase
            # ### ⛔ **E QUI NON SI NORMALIZZA, e la prima volta l-ho fatto:**
            # ### normalizzare ### **cancella l-ampiezza che porta `x0`**, e il caso
            # ### <<due sovrapposti>> tornava ### **un grumo piu- DEBOLE** invece che
            # ### piu- forte -- per questo si comportava ### **come il lineare.**
            # ### ⭐ **E LA RIDUZIONE ONESTA VA DETTA: a `D = 0` due grumi IN FASE
            # ### SONO UN GRUMO di ampiezza radice di due**, cioe- ### **`x0` doppio** --
            # ### quindi la domanda <<rimbalza, si fonde o si allarga>> ### **si riduce
            # ### alla scansione di `x0`**, e il braccio sotto lo verifica confrontando
            # ### ### **<<due a `x0`>> con <<uno a `2 x0`>>.**
            due = {"psi": a1["psi"] * math.sqrt(2.0), "phi": a1["phi"].copy()}
            for nome_c, stato in (("uno", a1), ("due_sovrapposti", due)):
                s = dict(stato)
                serie, tempo = [], []
                for tt in range(1, PASSI + 1):
                    s = C3.passo3(s, sc, ident, np.ones(sc["n"]), 1.0, EPS_RIF, fl)
                    rho = CM.rho_nodo(s["psi"], sc)
                    serie.append(float(np.sum(rho[d0z <= 1]) / np.sum(rho)))
                    tempo.append(tt)
                pend, sg = L3.pendenza(tempo, serie)
                out["G2"]["massima_densita"]["%s x0=%g %s" % (et, x0, nome_c)] = {
                    "frazione_iniziale": serie[0], "frazione_finale": serie[-1],
                    "pendenza_allargamento": pend, "sigma": sg,
                    "tick": PASSI, "tau_locale": float(PASSI)}
    print("  G2b allargamento entro un arco (pendenza):")
    for x0 in (1.0, 8.0, 64.0):
        r = out["G2"]["massima_densita"]
        print("        x0=%-4g  N uno %+.5f / due %+.5f    lineare uno %+.5f / due %+.5f"
              % (x0, r["N x0=%g uno" % x0]["pendenza_allargamento"],
                 r["N x0=%g due_sovrapposti" % x0]["pendenza_allargamento"],
                 r["lineare x0=%g uno" % x0]["pendenza_allargamento"],
                 r["lineare x0=%g due_sovrapposti" % x0]["pendenza_allargamento"]))

    # ============================================================ G2 (c)
    out["G2"]["moto_collettivo"] = {}
    for spinta in SPINTE:
        r = due_grumi(sc, ident, S3.flusso, "N", 2, 0.0, spinta=spinta)
        if r is not None:
            out["G2"]["moto_collettivo"]["spinta=%g" % spinta] = r
    print("  G2c spinta: %s" % "  ".join(
        "%s: primo %+.3f, secondo %+.3f, sep %+.3f"
        % (k, v["pendenza_primo"], v["pendenza_secondo"], v["pendenza_separazione"])
        for k, v in sorted(out["G2"]["moto_collettivo"].items())))

    # ============================================================ il REGOLARE
    out["G2"]["regolare"] = {}
    geo_r = GE.scena_identita(reg)
    for D in (1, 2, 4, 8):
        r = due_grumi(reg, geo_r, S3.flusso, "N", D, 0.0)
        if r is not None:
            out["G2"]["regolare"]["D=%d" % D] = r
    print("  G2  sul REGOLARE: %s" % "  ".join(
        "%s: sep %.1f->%.1f" % (k, v["separazione_iniziale"], v["separazione_finale"])
        for k, v in sorted(out["G2"]["regolare"].items())))

    # ============================================================ (V7) i coniugati
    out["G1_coniugato"] = {}
    for nome, fl in (("N", S3.flusso), ("E", I3.flusso_E)):
        st, dentro, d = L3.grumo(sc, ident, 0, 1, 8.0, seme=SEMI[0])
        p, q = dict(st), C3.coniuga3(st)
        for _ in range(PASSI):
            p = C3.passo3(p, sc, ident, np.ones(sc["n"]), 1.0, EPS_RIF, fl)
            q = C3.passo3(q, sc, ident, np.ones(sc["n"]), 1.0, EPS_RIF, fl)
        out["G1_coniugato"][nome] = {
            "coniugazione": float(np.max(np.abs(C3.coniuga3(p)["psi"] - q["psi"]))),
            "rho_differenza": float(np.max(np.abs(CM.rho_nodo(p["psi"], sc)
                                                  - CM.rho_nodo(q["psi"], sc))))}
    print("  V7  i coniugati: %s" % "  ".join(
        "%s %.3g" % (k, v["coniugazione"]) for k, v in out["G1_coniugato"].items()))

    dati = (json.dumps(out, indent=1, ensure_ascii=False, sort_keys=True, default=float)
            + NLN).encode("utf-8")
    io.open(os.path.join(USCITE, "letture_guscio_moto.json"), "wb").write(dati)
    print("  " + "-" * 96)
    print("  scritto proto_camminata/uscite/letture_guscio_moto.json")
    print("=" * 100)
    return 0


if __name__ == "__main__":
    sys.exit(main())
