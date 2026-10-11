# -*- coding: utf-8 -*-
r"""IL COMPLETAMENTO DEL LEGAME — `C1` le scene grandi, `C2` la misura in ARCHI ASSOLUTI.

### ⛔ **SONO OSSERVATORI, NON LEGGI:** `soliton_simulator.py` e `leggi.yaml` **non si
toccano**, e le candidate `-N`/`-D` restano **accendibili e mai di default**.

> ## ⭐ **PERCHE' UN MISURANDO NUOVO:** il vecchio confronta la frazione entro un arco
> ## col **FONDO UNIFORME**, e quel fondo e' `(nodi entro r)/n` " cioe' ### **dipende
> ## dalla TAGLIA attraverso il DENOMINATORE.** Il misurando nuovo ### **conta ARCHI** e
> ## non ha denominatore: ### **il raggio che contiene il `50%` e il `90%` della norma**,
> ## e la ### **frazione entro `r = 1, 2, 3` archi** " sempre contro il ### **LINEARE
> ## ALLA STESSA TAGLIA.**

> ## ⛔ **E LA MISURA VECCHIA SI TIENE ACCANTO**, come il mandato chiede: se le due si
> ## contraddicono, ### **la vecchia era il difetto** " e la contraddizione si vede solo
> ## se ci sono entrambe.

Soglie e previsioni: `doc/TASK_HISTORY/2026-10-11_legame_scene_grandi.md`, **committato
PRIMA** (`7fdb942`).

Gira con:  python proto_camminata/_letture_legame_grandi.py
"""
import io
import json
import math
import os
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
sys.path.insert(0, _QUI)
sys.path.insert(0, os.path.join(RADICE, "csv"))
import _presidio                                              # noqa: E402

_presidio.avvia(__file__)

import camminata as CM                                        # noqa: E402
import camminata2 as C2M                                      # noqa: E402
import camminata3 as C3                                       # noqa: E402
import geometria as GE                                        # noqa: E402
import scena as SC                                            # noqa: E402
import scene3d as S3D                                         # noqa: E402
import segni1 as S1                                           # noqa: E402
import _letture3 as L3                                        # noqa: E402

SC._niente_simulatore()

EPS = float(np.finfo(float).eps)
SEMI = (11, 23, 37, 53)
EPS_RIF = 0.5
# ### ⛔ **MISURATA, NON SCELTA:** `0.6193` archi/tick, dal referto del `v4`.
V_FRONTE = 0.6193
# ### ⭐ **I RAGGI IN ARCHI ASSOLUTI che il mandato nomina**, e le due frazioni di norma.
RAGGI_ASSOLUTI = (1, 2, 3)
FRAZIONI = (0.50, 0.90)
# ### ⚠ **LA GRIGLIA DI `x0` E' QUELLA DI `M1`, non una ridotta:** cambiarla renderebbe
# ### il confronto col referto vecchio ### **un confronto fra due esperimenti.**
X0 = S1.X0_GRIGLIA
# ### ⛔ **LA GRIGLIA RIDOTTA, E IL MOTIVO E' MISURATO.** Il primo run e' caduto, e i
# ### suoi tempi dicono perche': `0.05` s per passo-caso a `m = 4000`, ### **`0.49` a
# ### `m = 24000`, `1.61` a `m = 81000`** -- cioe' `140` casi *(`5` varianti x `7` `x0` x
# ### `4` semi)* su una scena grande costano ### **ore.**
# ### ⭐ **E LA RIDUZIONE NON TOCCA LA PRECISIONE DI UN CASO: toglie PUNTI DI SCAN.**
# ### I `4` semi restano `4`, i `6` tempi restano `6`. ### **Cio' che si riduce e' la
# ### griglia di `x0`**, e la si riduce ### **dove l'effetto NON c'e'**: nel `1D` del primo
# ### run l'unico caso che lega e' ### **`+D` a `x0 = 8`**, cioe' ### **il piu' saturo** --
# ### quindi la sotto-griglia tiene ### **il piu' saturo piu' due riferimenti.**
# ### ⚠ **E SI DICHIARA PER SCENA:** la griglia PIENA resta dove si paga, e il campo
# ### `griglia_x0` del `json` dice ### **quale delle due ha girato.**
X0_RIDOTTA = (1.0, 4.0, 8.0)
# ### ⛔ **LA SOGLIA FRA LE DUE, in ESTREMITA' D'ARCO**: `2 m` e' la dimensione di
# ### `psi`, cioe' ### **la grandezza che decide il costo di un passo.**
MAX_ARCHI_GRIGLIA_PIENA = 50000
# ### DICHIARATO: IL TETTO DEL TEMPO DI OSSERVAZIONE, e il motivo e' DOPPIO.
# ### `1` `M1` osservava a `min(40, t_max)`, quindi lo STESSO tetto rende la misura nuova
# ###   confrontabile con il referto vecchio -- con un tetto diverso sarebbero DUE
# ###   ESPERIMENTI.
# ### `2` MISURATO sull'anello a `n = 400`: le differenze dal lineare CALANO in modo
# ###   monotono con `t` (per `+D` a `x0 = 4`: `0.5052` a `t = 4`, `0.0709` a `t = 80`),
# ###   quindi osservare a `t` grande NON aggiunge informazione: DILUISCE.
# ### E l'ammissibilita' resta un LIMITE SUPERIORE: il tetto non la sostituisce, la
# ###   stringe -- il tempo usato e' `min(t_ammissibile, T_TETTO)`.
T_TETTO = 40
USCITE = os.path.join(_QUI, "uscite")
FONTE = os.path.join(USCITE, "letture_legame_grandi.json")


# =====================================================================================
#   `C1` — LE SCENE, e la REGOLA DI AMMISSIBILITA'
# =====================================================================================
def diametro(sc, campiona=40):
    """### Campionato su `n` grande: e' un **limite inferiore**, e il campo lo dice."""
    passo = max(1, sc["n"] // campiona)
    d = max(int(SC.distanze(sc, k).max()) for k in range(0, sc["n"], passo))
    return d, bool(passo == 1)


def t_ammissibile(diam):
    """### ⛔ **LA CONDIZIONE DI `C1`: il fronte NON arriva a META' del diametro.**

    `0.6193 * t < diametro/2`, e si torna il ### **piu' grande `t` intero** che la
    rispetta. ### **Non e' una scelta: e' una disuguaglianza con un numero misurato.**
    """
    t = int(math.floor((diam / 2.0) / V_FRONTE))
    while t > 0 and V_FRONTE * t >= diam / 2.0:
        t -= 1
    return t


def tempi_di(diam, quanti=6):
    """### I `t` dove si campiona, **tutti ammissibili**, spalmati su `[4, t_amm]`."""
    ta = min(t_ammissibile(diam), T_TETTO)
    if ta < 4:
        return []
    passi = sorted({int(round(x)) for x in np.linspace(4, ta, quanti)})
    return [t for t in passi if 4 <= t <= ta]


def scene_c1():
    """### Le scene di `C1`, e ### **ENTRAMBE le varianti geometriche.**

    ### ⛔ **PERCHE' DUE E NON UNA:** le misure dell'isotropia indicano i punti
    ### **respinti** su ogni asse tranne uno *(lo scarto da `3`, dove i due ### **non sono
    distinguibili**)*, ma ### **la scelta della scena principale e' di Luca**
    *(`[[DOMANDA-QUALE-SCENA-3D-PRINCIPALE]]`)* " quindi si misura su ### **tutte e due**,
    e ### **non si decide qui.**

    ### ⭐ **E L'ANELLO C'E' PERCHE' E' IL LIMITE NOTO:** in `1D` il `+D` lega con effetto
    che ### **CRESCE con la taglia**, misurato. ### **Se il misurando nuovo non ritrovasse
    quello, il misurando sarebbe rotto** " e non la fisica.
    """
    # ### ⚠ **E <<L'ANELLO>> SI CHIAMA `regolare`, non `anello`:** e' il ### **circolante
    # ### con salti `(1, 2)`**, quello che il referto del legame usa come `1D`
    # ### *(`d_s = 1.001` con `r2 = 1.0000`, misurato)*. ### **Ho cercato `SC.anello` e non
    # ### esiste** " e un nome che non esiste e' meglio di un nome che esiste e fa altro.
    return (("regolare n=2000 (limite noto 1D)", lambda: SC.regolare(2000),
             "regolare (1D)"),
            # ### ⭐ **LA PRINCIPALE VA PER PRIMA, dopo il limite noto:** e' la
            # ### ### **`(ii)` dei punti che si respingono** *(decisione di Luca del
            # ### `2026-10-11`, `[[SCENA-3D-PRINCIPALE]]`)*. ### ⛔ **E l'ordine NON
            # ### e' estetico: il primo run e' caduto sulla quarta scena, e cio' che
            # ### viene DOPO non si misura** -- quindi cio' che conta di piu' sta
            # ### ### **davanti.**
            ("geometrico3d n=4000 respinti (PRINCIPALE)",
             lambda: S3D.geometrico3d(4000, rilassati=True), "geometrico3d respinti"),
            ("geometrico3d n=26000 respinti (PRINCIPALE)",
             lambda: S3D.geometrico3d(26000, rilassati=True), "geometrico3d respinti"),
            # ### la `(i)` RESTA, perche' e' la scena su cui il referto vecchio ha
            # ### misurato: ### **togliere la colonna renderebbe il confronto impossibile**
            ("geometrico3d n=4000 uniformi", lambda: S3D.geometrico3d(4000),
             "geometrico3d uniformi"),
            ("geometrico3d n=26000 uniformi", lambda: S3D.geometrico3d(26000),
             "geometrico3d uniformi"),
            # ### il CONTROLLO dichiarato
            ("cubico L=20", lambda: S3D.cubico(20), "cubico (3D)"),
            ("cubico L=30", lambda: S3D.cubico(30), "cubico (3D)"))
            # ### ⛔ **E `cubico L=40` NON C'E' PIU', e il motivo e' MISURATO due
            # ### volte.** `1` Il primo run ci e' ### **CADUTO con `MemoryError`**:
            # ### `n = 64000`, `m = 192000`, e il passo implicito tiene piu' array
            # ### `complex128` da `384000` elementi insieme. `2` E il ### **TEMPO**: il
            # ### salto `L = 20` -> `L = 30` costa ### **`4.98` volte** *(`1631` -> `8114`
            # ### s)*, quindi `L = 40` costerebbe ### **~`11` ore.**
            # ### ✅ **E il mandato dice cosa fare: <<una taglia che sfora si DICHIARA
            # ### e si ferma alla precedente>>** -- ### **senza ridurre la precisione.**
            # ### ⚠ **Quindi il cubico ha DUE taglie ammissibili** *(`L = 20` e
            # ### `L = 30`)*, che e' ### **il minimo che `c2-quater` chiede**: con una in
            # ### meno il controllo ### **non deciderebbe.**


def costo_per_tick(sc, geo, giri=5):
    """### Il costo, **misurato**: una taglia che non si paga ### **si dichiara.**"""
    st = C3.stato3(sc, 11)
    fl = S1.flusso_di("lineare")
    uno = np.ones(sc["n"])
    t0 = time.time()
    for _ in range(giri):
        st = C3.passo3(st, sc, geo, uno, 1.0, EPS_RIF, fl)
    return (time.time() - t0) / giri


# =====================================================================================
#   `C2` — IL MISURANDO IN ARCHI ASSOLUTI
# =====================================================================================
def raggio_in_archi(sc, st, d, frazione):
    """### Il raggio **IN ARCHI** che contiene `frazione` della norma.

    ### ⛔ **NESSUN DENOMINATORE CHE DIPENDE DALLA TAGLIA:** e' un conteggio di archi, e
    il suo valore massimo e' il diametro " non `n`.
    """
    rho = CM.rho_nodo(st["psi"], sc)
    tot = float(np.sum(rho))
    if tot <= 0:
        return float("nan")
    cum = 0.0
    for r in range(0, int(d.max()) + 1):
        cum = float(np.sum(rho[(d >= 0) & (d <= r)]))
        if cum / tot >= frazione:
            return float(r)
    return float(d.max())


def profilo(sc, geo, fl, x0, seme, tempi, d):
    """### **UNA sola evoluzione, campionata a TUTTI i `t`.**

    ### ⭐ **E' il motivo per cui <<il raggio contro `t`>> costa quanto una misura sola:**
    rifare l'evoluzione per ogni `t` costerebbe ### **la somma dei `t`** invece del loro
    ### **massimo.**
    """
    st, _dentro, dd = L3.grumo(sc, geo, 0, 1, x0, seme=seme)
    out = {"raggio_iniziale": raggio_in_archi(sc, st, d, 0.90), "per_t": {}}
    uno = np.ones(sc["n"])
    z = dict(st)
    ultimo = 0
    for t in tempi:
        for _ in range(t - ultimo):
            z = C3.passo3(z, sc, geo, uno, 1.0, EPS_RIF, fl)
        ultimo = t
        riga = {"r%d" % int(100 * f): raggio_in_archi(sc, z, d, f) for f in FRAZIONI}
        for r in RAGGI_ASSOLUTI:
            riga["entro_%d" % r] = L3.frazione_entro(sc, z, 0, dd, r)
        # ### ⚠ **E LA MISURA VECCHIA ACCANTO**, col suo fondo che dipende dalla taglia
        riga["vecchia_rapporto"] = (
            L3.frazione_entro(sc, z, 0, dd, 1) / L3.fondo_uniforme(sc, dd, 1))
        riga["norma"] = float(CM.norma(z["psi"]))
        out["per_t"][str(t)] = riga
    return out


def _retta(xs, ys):
    """### La pendenza con la sua `sigma`, dai residui. ### **Serve a `c2`.**"""
    if len(xs) < 3:
        return {"pendenza": float("nan"), "nota": "meno di tre punti"}
    x = np.asarray(xs, dtype=float)
    y = np.asarray(ys, dtype=float)
    if not np.all(np.isfinite(y)):
        return {"pendenza": float("nan"), "nota": "valori non finiti"}
    a, b = np.polyfit(x, y, 1)
    res = y - (a * x + b)
    sa = (math.sqrt(float(np.sum(res ** 2)) / max(len(x) - 2, 1))
          / math.sqrt(float(np.sum((x - x.mean()) ** 2))))
    return {"pendenza": float(a), "sigma": float(sa),
            "in_sigma": (abs(a) / sa) if sa > 0 else float("inf"),
            "ferma": bool(sa > 0 and abs(a) <= 3.0 * sa)}


def _salva(fuori):
    """### ⛔ **IL CHECKPOINT, e nasce da un DANNO MISURATO.** Il primo run ha girato
    ### **`2.8` ore** *(`255` + `1631` + `8114` s)*, e' caduto sulla scena dopo, e ### **ha
    perso TUTTO** -- perche' il `json` si scriveva ### **solo alla fine.**

    ### ✅ **Adesso si scrive DOPO OGNI SCENA.** Un risultato che esiste e non e' su
    disco ### **non esiste.**
    """
    os.makedirs(USCITE, exist_ok=True)
    io.open(FONTE, "wb").write(
        (json.dumps(fuori, ensure_ascii=False, indent=1, sort_keys=True)
         + chr(10)).encode("utf-8"))


def c1_c2(fuori_tutto=None):
    fuori = {"velocita_fronte": V_FRONTE, "semi": len(SEMI), "griglia_x0": list(X0),
             "griglia_x0_ridotta": list(X0_RIDOTTA),
             "soglia_griglia_piena": MAX_ARCHI_GRIGLIA_PIENA,
             "raggi_assoluti": list(RAGGI_ASSOLUTI), "frazioni": list(FRAZIONI),
             "per_scena": {}}
    for nome, fab, fam in scene_c1():
        t0 = time.time()
        try:
            sc = fab()
        except MemoryError as e:
            # ### ⛔ **SOLO `MemoryError`:** un `except Exception` scriverebbe <<non
            # ### misurata>> anche su ### **un MIO errore di codice.**
            fuori["per_scena"][nome] = {"non_misurata": "MemoryError: %s" % e}
            print("  --- %-34s ### NON COSTRUITA: memoria esaurita" % nome)
            continue
        geo = GE.scena_identita(sc)
        diam, esatto = diametro(sc)
        tempi = tempi_di(diam)
        amm = bool(tempi) and V_FRONTE * max(tempi) < diam / 2.0
        d = SC.distanze(sc, 0)
        scena = {"n": sc["n"], "m": sc["m"], "diametro": diam,
                 "diametro_esatto": esatto, "famiglia": fam,
                 "t_ammissibile": t_ammissibile(diam), "tempi": tempi,
                 "ammissibile": amm, "costo_per_tick": costo_per_tick(sc, geo),
                 "secondi_costruzione": time.time() - t0,
                 "etichetta_dimensione": S3D.etichetta(sc["nome"])}
        print("  --- %-34s n %-7d m %-7d diam %-6s t_amm %-4d tempi %s  %s"
              % (nome, sc["n"], sc["m"], ("%d" % diam) if esatto else (">=%d" % diam),
                 scena["t_ammissibile"], tempi,
                 "AMMISSIBILE" if amm else "### NON AMMISSIBILE"))
        if not amm:
            # ### ⛔ **UNA SCENA NON AMMISSIBILE NON SI MISURA**, e si dichiara:
            # ### ### **misurarla darebbe un numero che parla del BORDO.**
            fuori["per_scena"][nome] = {"_scena": scena,
                                        "non_misurata": "scena NON ammissibile"}
            continue
        # ### ⛔ **LA GUARDIA SULLA MISURA, e il primo run e' caduto QUI:** a
        # ### `L = 40` *(`n = 64000`, `m = 192000`)* il passo implicito tiene piu' array
        # ### `complex128` da `384000` elementi insieme, e ### **la memoria e' finita.**
        # ### ✅ **Adesso una scena che non entra in memoria si DICHIARA e le altre
        # ### CONTINUANO**, invece di portarsi via la corsa intera.
        # LA GUARDIA SULLA MISURA, e il primo run e' caduto QUI, non nella
        # costruzione: a `L = 40` (`n = 64000`, `m = 192000`) il passo implicito
        # tiene piu' array `complex128` da `384000` elementi insieme, e la memoria
        # e' finita DENTRO `profilo`.
        # Adesso una scena che non entra in memoria si DICHIARA e le altre
        # CONTINUANO, invece di portarsi via la corsa intera -- e con il checkpoint
        # cio' che era gia' misurato RESTA SU DISCO.
        # E SOLO `MemoryError`: un `except Exception` scriverebbe <<non misurata>>
        # anche su un MIO errore di codice.
        try:
            per_var = {}
            griglia = X0 if 2 * sc["m"] <= MAX_ARCHI_GRIGLIA_PIENA else X0_RIDOTTA
            scena["griglia_x0"] = list(griglia)
            scena["griglia_piena"] = bool(griglia is X0)
            for et in S1.VARIANTI:
                fl = S1.flusso_di(et)
                per_x0 = {}
                for x0 in griglia:
                    prove = [profilo(sc, geo, fl, x0, s, tempi, d) for s in SEMI]
                    riga = {"x0": x0,
                            "raggio_iniziale": float(np.mean(
                                [p["raggio_iniziale"] for p in prove])),
                            "per_t": {}}
                    for t in tempi:
                        q = {}
                        for ch in list(prove[0]["per_t"][str(t)]):
                            vv = [p["per_t"][str(t)][ch] for p in prove]
                            q[ch] = float(np.mean(vv))
                            q[ch + "_sigma"] = (float(np.std(vv, ddof=1))
                                                / math.sqrt(len(vv))) if len(vv) > 1 else 0.0
                        riga["per_t"][str(t)] = q
                    # ### ⭐ **LA PENDENZA DEL RAGGIO CONTRO `t`**, che e' `c2`
                    riga["pendenza_r90"] = _retta(
                        tempi, [riga["per_t"][str(t)]["r90"] for t in tempi])
                    riga["pendenza_r50"] = _retta(
                        tempi, [riga["per_t"][str(t)]["r50"] for t in tempi])
                    per_x0["%g" % x0] = riga
                per_var[et] = per_x0
            # ============================================ il confronto col LINEARE
            for et in S1.VARIANTI:
                if et == "lineare":
                    continue
                for k in per_var[et]:
                    a = per_var[et][k]
                    b = per_var["lineare"][k]
                    t_fin = str(tempi[-1])
                    # ### IL CONFRONTO COL LINEARE SI FA A **OGNI** `t`, non solo
                    # ### all'ultimo: sull'anello le differenze CALANO con `t`, quindi
                    # ### riportare solo l'ultimo nasconderebbe l'andamento -- e
                    # ### l'andamento e' meta' del fatto.
                    a["per_t_contro_lineare"] = {}
                    for tt in tempi:
                        q2 = {}
                        for r in RAGGI_ASSOLUTI:
                            ch = "entro_%d" % r
                            aa = a["per_t"][str(tt)][ch]
                            bb = b["per_t"][str(tt)][ch]
                            s2 = math.sqrt(a["per_t"][str(tt)][ch + "_sigma"] ** 2
                                           + b["per_t"][str(tt)][ch + "_sigma"] ** 2)
                            q2[ch] = {"differenza": aa - bb, "sigma_combinato": s2,
                                      "in_sigma": (abs(aa - bb) / s2) if s2 > 0 else 0.0,
                                      "effetto_relativo": ((aa - bb) / bb) if bb
                                      else float("nan"),
                                      "sopra": bool(s2 > 0 and (aa - bb) > 3.0 * s2)}
                        q2["r90"] = {"candidata": a["per_t"][str(tt)]["r90"],
                                     "lineare": b["per_t"][str(tt)]["r90"]}
                        a["per_t_contro_lineare"][str(tt)] = q2
                    # ### `c2-bis`: il RAPPORTO fra le due pendenze
                    pa, pb = a["pendenza_r90"], b["pendenza_r90"]
                    rap = {"nota": "pendenze non confrontabili"}
                    if (pa.get("pendenza") == pa.get("pendenza")
                            and pb.get("pendenza") == pb.get("pendenza")
                            and abs(pb.get("pendenza", 0.0)) > 0):
                        q = pa["pendenza"] / pb["pendenza"]
                        # ### la `sigma` del rapporto, propagata
                        sq = abs(q) * math.sqrt(
                            (pa.get("sigma", 0.0) / pa["pendenza"]) ** 2
                            + (pb.get("sigma", 0.0) / pb["pendenza"]) ** 2) \
                            if pa["pendenza"] != 0 else float("nan")
                        rap = {"rapporto": q, "sigma": sq,
                               "in_sigma_da_1": (abs(q - 1.0) / sq) if sq > 0
                               else float("inf"),
                               # ### ⛔ **LA SOGLIA E' LA SIGNIFICATIVITA', NON UN VALORE**
                               # ### *(`A1`)*: *«piu' lentamente»* vuol dire ### **sotto `1`
                               # ### di piu' di `3 sigma`**, e ### **nessun numero scelto.**
                               "piu_lenta": bool(sq > 0 and (1.0 - q) > 3.0 * sq)}
                    # ### `c2-ter`: la frazione entro pochi archi, contro il lineare
                    frz = {}
                    for r in RAGGI_ASSOLUTI:
                        ch = "entro_%d" % r
                        aa = a["per_t"][t_fin][ch]
                        bb = b["per_t"][t_fin][ch]
                        sg = math.sqrt(a["per_t"][t_fin][ch + "_sigma"] ** 2
                                       + b["per_t"][t_fin][ch + "_sigma"] ** 2)
                        frz[ch] = {"candidata": aa, "lineare": bb, "differenza": aa - bb,
                                   "sigma_combinato": sg,
                                   "in_sigma": (abs(aa - bb) / sg) if sg > 0 else 0.0,
                                   # ### ⭐ **l'EFFETTO RELATIVO, accanto al `sigma`**
                                   "effetto_relativo": ((aa - bb) / bb) if bb else
                                   float("nan"),
                                   "sopra": bool(sg > 0 and (aa - bb) > 3.0 * sg)}
                    # ### ⭐ **E LA MISURA VECCHIA ACCANTO**, per vedere se contraddice
                    va = a["per_t"][t_fin]["vecchia_rapporto"]
                    vb = b["per_t"][t_fin]["vecchia_rapporto"]
                    sgv = math.sqrt(a["per_t"][t_fin]["vecchia_rapporto_sigma"] ** 2
                                    + b["per_t"][t_fin]["vecchia_rapporto_sigma"] ** 2)
                    a["contro_lineare"] = {
                        "t_finale": tempi[-1],
                        "pendenza_candidata": pa, "pendenza_lineare": pb,
                        "rapporto_pendenze": rap, "frazioni": frz,
                        "vecchia": {"candidata": va, "lineare": vb, "differenza": va - vb,
                                    "sigma_combinato": sgv,
                                    "in_sigma": (abs(va - vb) / sgv) if sgv > 0 else 0.0,
                                    "piu_concentrato": bool(sgv > 0
                                                            and (va - vb) > 3.0 * sgv)},
                        # ### ⛔ **IL VERDETTO DI `C2`:** *(il raggio **si ferma** OPPURE
                        # ### **cresce piu' lentamente**)* ### **E** la frazione entro pochi
                        # ### archi ### **resta SOPRA.**
                        "verdetto": (
                            "RESTA CONCENTRATO"
                            if ((pa.get("ferma") or rap.get("piu_lenta"))
                                and any(frz[q2]["sopra"] for q2 in frz))
                            else "SI DISPERDE")}
            per_var["_scena"] = scena
            fuori["per_scena"][nome] = per_var
        except MemoryError as e:
            scena["non_misurata"] = "MemoryError: %s" % e
            fuori["per_scena"][nome] = {"_scena": scena,
                                        "non_misurata": "MemoryError: %s" % e}
            print("      ### NON MISURATA: memoria esaurita durante la misura")
            if fuori_tutto is not None:
                fuori_tutto["C1_C2"] = fuori
                _salva(fuori_tutto)
            continue
        # ### ✅ **E SI SALVA SUBITO**, prima di toccare la scena dopo.
        if fuori_tutto is not None:
            fuori_tutto["C1_C2"] = fuori
            _salva(fuori_tutto)
        conta = {"RESTA CONCENTRATO": 0, "SI DISPERDE": 0}
        vinti = []
        for et in S1.VARIANTI:
            if et == "lineare":
                continue
            for k, v in per_var[et].items():
                c = v.get("contro_lineare")
                if not c:
                    continue
                conta[c["verdetto"]] = conta.get(c["verdetto"], 0) + 1
                if c["verdetto"] == "RESTA CONCENTRATO":
                    vinti.append((et, k))
        print("      RESTA %-3d  DISPERDE %-3d  concentrati: %-28s  (%.0f s)"
              % (conta["RESTA CONCENTRATO"], conta["SI DISPERDE"],
                 str(vinti[:4]) if vinti else "NESSUNO", time.time() - t0))
        del sc, geo, d
    # ### ⭐ **`c2-quater`: il verdetto per FAMIGLIA vuole DUE taglie ammissibili.**
    fuori["per_famiglia"] = per_famiglia(fuori)
    return fuori


def per_famiglia(fuori):
    """### ⛔ **<<LEGATO>> SOLO SU DUE TAGLIE** *(`c2-quater`, e `TAGLIA-FINITA`)*.

    ### **Un verdetto su una taglia sola e' una retta per un punto.**
    """
    fam = {}
    for nome, v in fuori["per_scena"].items():
        sc_ = v.get("_scena") or {}
        f = sc_.get("famiglia", "?")
        g = fam.setdefault(f, {"taglie_ammissibili": [], "per_caso": {}})
        if not sc_.get("ammissibile"):
            continue
        g["taglie_ammissibili"].append(sc_["n"])
        for et in S1.VARIANTI:
            if et == "lineare" or et not in v:
                continue
            for k, q in v[et].items():
                c = q.get("contro_lineare")
                if not c:
                    continue
                g["per_caso"].setdefault("%s|%s" % (et, k), []).append(
                    {"n": sc_["n"], "verdetto": c["verdetto"],
                     "effetto_entro_1": c["frazioni"]["entro_1"]["effetto_relativo"],
                     "in_sigma_entro_1": c["frazioni"]["entro_1"]["in_sigma"]})
    for f, g in fam.items():
        legati = []
        for caso, righe in g["per_caso"].items():
            quante = sum(1 for r in righe if r["verdetto"] == "RESTA CONCENTRATO")
            if quante >= 2:
                legati.append({"caso": caso, "taglie": quante,
                               "effetto_massimo": max(abs(r["effetto_entro_1"])
                                                       for r in righe)})
        # ### ⭐ **ORDINATI PER EFFETTO**, che e' la regola di forma
        g["legati"] = sorted(legati, key=lambda x: -x["effetto_massimo"])
        g["verdetto"] = ("LEGA su almeno due taglie" if g["legati"]
                         else ("NON LEGA" if len(g["taglie_ammissibili"]) >= 2
                               else "UNA SOLA TAGLIA AMMISSIBILE: non si decide"))
    return fam


def main():
    os.makedirs(USCITE, exist_ok=True)
    fuori = {"blob": _presidio.timbro(__file__)["sha1"]}
    print("=" * 100)
    print("  --- C1 e C2: le scene grandi, e la misura in ARCHI ASSOLUTI ---")
    fuori["C1_C2"] = c1_c2(fuori)
    print("  --- i verdetti PER FAMIGLIA (due taglie, c2-quater) ---")
    for f, g in sorted(fuori["C1_C2"]["per_famiglia"].items()):
        print("    %-28s taglie ammissibili %-22s  ### %s"
              % (f, g["taglie_ammissibili"], g["verdetto"]))
        for q in g["legati"][:5]:
            print("        %-22s su %d taglie, effetto massimo %+.4f"
                  % (q["caso"], q["taglie"], q["effetto_massimo"]))
    io.open(FONTE, "wb").write(
        (json.dumps(fuori, ensure_ascii=False, indent=1, sort_keys=True)
         + chr(10)).encode("utf-8"))
    print("-" * 100)
    print("  scritto %s" % os.path.relpath(FONTE, RADICE).replace(os.sep, "/"))
    print("=" * 100)
    return 0


if __name__ == "__main__":
    sys.exit(main())
