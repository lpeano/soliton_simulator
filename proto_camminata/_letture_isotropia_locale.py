# -*- coding: utf-8 -*-
r"""L'ISOTROPIA LOCALE — `I1` si attenua con la distanza? `I2` si riduce costruendo meglio?

### ⛔ **SONO OSSERVATORI, NON LEGGI:** nessuna variante diventa la scena di default
*(il mandato lo dice)*, `soliton_simulator.py` e `leggi.yaml` **non si toccano**.

> ## ⛔ **LE POSIZIONI SONO SOLO DA OSSERVATORE.** Entrano nel **costruttore di scena**
> ## *(una condizione iniziale)* e nel **misurando** *(«in che direzione va quest'arco»)*,
> ## ### **e MAI nel passo:** `sc` non le contiene, e il braccio sorgente del collaudo
> ## verifica che `(iv-U)` e `(iv-R)` ### **non le leggano.**

> ## ⭐ **LE TRE GRANDEZZE, dopo la correzione del guardiano** *(`d9f8f78` le confondeva)*:
> ## **irregolarita' per nodo** *(dispersione fra direzioni, mediata sui nodi)* ·
> ## **anisotropia del profilo MEDIO** *(dispersione del profilo mediato sui nodi)* ·
> ## **rumore atteso** *(`irregolarita'/sqrt(N)`)*. ### **Solo la seconda sopra la terza
> ## e' anisotropia VERA.**

Soglie e previsioni: `doc/TASK_HISTORY/2026-10-11_isotropia_locale.md`, **committato PRIMA**
(`e9dbae1`).

Gira con:  python proto_camminata/_letture_isotropia_locale.py
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
import camminata2 as C2                                       # noqa: E402
import geometria as GE                                        # noqa: E402
import pesi4 as P4                                            # noqa: E402
import scena as SC                                            # noqa: E402
import scene3d as S3D                                         # noqa: E402

SC._niente_simulatore()

# ### ⛔ **LA VELOCITA' DEL FRONTE E' MISURATA, non scelta:** `0.6193` archi/tick, dal
# ### referto del `v4`. ### **Serve a sapere quale `t` il diametro CONSENTE.**
V_FRONTE = 0.6193
# ### ⭐ **I TEMPI DEL MANDATO.** `t = 30` vorrebbe `n ~ 40000`, e si DICHIARA.
TEMPI = (4, 6, 10, 15, 20, 25, 30)
N_I1 = 26000
L_CONTROLLO = 20
# ### ⭐ **LE TAGLIE DI `M-A`**, e il motivo e' nell'aggiunta di Luca: la `d_s` ###
# ### **dipende dalla taglia** *(la stessa `(i)`: `2.578` a `1728`, `2.92` a `4000`)*,
# ### quindi un compromesso misurato a ### **una sola taglia** non si distingue da un
# ### effetto di ### **taglia finita.**
TAGLIE_DS = (4000, 10000, 26000)
# ### ⛔ **E LA TAGLIA GRANDE PER IL PAVIMENTO** *(`M-C`)*: la stessa di `I1`, cosi'
# ### il confronto con lo `0.17` di `(i)` e' ### **alla STESSA taglia e con lo STESSO
# ### protocollo** -- altrimenti sarebbe un confronto fra due esperimenti diversi.
N_I2 = 1728
T_I2 = 10
NODI = 40
SEME_NODI = 1
USCITE = os.path.join(_QUI, "uscite")
FONTE = os.path.join(USCITE, "letture_isotropia_locale.json")
RIFERIMENTO = "(i) uniformi, gradi 2-6"
COMBINAZIONE = "(ii)+(iv-U) respinti + tutti i vicini, pesi uguali"
RESPINTI = "(ii) respinti, gradi 2-6"
TUTTI_VICINI = "(iv-U) Delaunay, pesi U"
CONTROLLO_PESI = "(iv-V) Delaunay, pesi V"


def diametro(sc, campiona=40):
    """### Il diametro, **campionato** su `n` grande: e' un **limite inferiore**, e il
    nome del campo lo dice."""
    passo = max(1, sc["n"] // campiona)
    d = max(int(SC.distanze(sc, k).max()) for k in range(0, sc["n"], passo))
    return d, bool(passo == 1)


def _potenza(serie):
    """### L'esponente di `t^(-a)`, con la sua `sigma`, e il verdetto a `3 sigma`."""
    if len(serie) < 3:
        return {"esponente": float("nan"), "nota": "meno di tre punti"}
    x = np.log([s[0] for s in serie])
    y = np.log([s[1] for s in serie])
    a, b = np.polyfit(x, y, 1)
    res = y - (a * x + b)
    sa = (math.sqrt(float(np.sum(res ** 2)) / max(len(x) - 2, 1))
          / math.sqrt(float(np.sum((x - x.mean()) ** 2))))
    return {"esponente": float(a), "sigma": float(sa),
            "in_sigma": (abs(a) / sa) if sa > 0 else float("inf"),
            "verdetto": ("SI ATTENUA" if a < -3 * sa
                         else ("RESTA PIATTA" if abs(a) <= 3 * sa else "CRESCE"))}


def _pavimento(serie):
    """### Il **PAVIMENTO**: gli ultimi due `t` differiscono entro `3 sigma`?"""
    if len(serie) < 2:
        return {"nota": "meno di due punti"}
    dd = abs(serie[-1][1] - serie[-2][1])
    sg = math.sqrt(serie[-1][2] ** 2 + serie[-2][2] ** 2)
    return {"differenza": float(dd), "sigma": float(sg),
            "in_sigma": (dd / sg) if sg > 0 else float("inf"),
            "valore": float(serie[-1][1]),
            "verdetto": "PAVIMENTO" if dd <= 3 * sg else "ANCORA IN DISCESA"}


# =====================================================================================
#   I1 — L'IRREGOLARITA' CONTRO LA DISTANZA
# =====================================================================================
def contro_t(nome, sc, pos):
    """### L'irregolarita' contro `t`, con l'esponente e il pavimento.

    ### ⭐ **E' LA STESSA VIA PER TUTTE LE SCENE** *(`I1`, il controllo cubico, il
    pavimento di `(ii)` in `M-C`, e la combinazione in `M-B`)*: ### **un confronto fra
    pavimenti ha senso solo se i pavimenti sono misurati con lo STESSO protocollo.**
    """
    fuori = {}
    diam, esatto = diametro(sc)
    # ### ⛔ **IL FRONTE NON DEVE FARE IL GIRO:** `t_max = diametro/(2 v)`.
    tmax = int(diam / (2 * V_FRONTE))
    nodi = S3D.nodi_a_caso(sc, NODI, SEME_NODI)
    print("    --- %s: n = %d, diametro >= %d, t_max = %d ---"
          % (nome, sc["n"], diam, tmax))
    v = {"n": sc["n"], "m": sc["m"], "diametro": diam,
         "diametro_esatto": esatto, "t_max": tmax, "nodi": len(nodi),
         "etichetta": S3D.etichetta(sc["nome"]), "tempi": {}, "oltre_t_max": []}
    serie = []
    for t in TEMPI:
        if t > tmax:
            v["oltre_t_max"].append(t)
            print("    %-5d ### OLTRE `t_max` = %d: NON SI MISURA (il fronte "
                  "farebbe il giro)" % (t, tmax))
            continue
        t0 = time.time()
        r = S3D.isotropia(sc, pos, passi=t, nodi=nodi)
        e = r["euclideo"]
        serie.append((t, e["irregolarita"], e["sigma_irregolarita"]))
        v["tempi"][str(t)] = {k: e[k] for k in
                              ("irregolarita", "sigma_irregolarita", "anisotropia",
                               "rumore", "aniso_su_rumore", "sistematica")}
        v["tempi"][str(t)]["secondi"] = time.time() - t0
        print("    %-5d %-9.4f +- %-9.4f aniso %-9.4f rumore %-9.4f a/r %-6.2f %s"
              % (t, e["irregolarita"], e["sigma_irregolarita"], e["anisotropia"],
                 e["rumore"], e["aniso_su_rumore"],
                 "### SISTEMATICA" if e["sistematica"] else "al rumore"))
    v["potenza"] = _potenza(serie)
    v["pavimento"] = _pavimento(serie)
    print("    ### l'esponente: t^(%+.3f +- %.3f) -> %s   |   il pavimento: %s"
          % (v["potenza"].get("esponente", float("nan")),
             v["potenza"].get("sigma", float("nan")),
             v["potenza"].get("verdetto", "?"),
             v["pavimento"].get("verdetto", "?")))
    fuori[nome] = v
    return fuori


def i1():
    """### `I1`: il geometrico a `n = 26000`, e il ### **cubico come CONTROLLO.**"""
    fuori = {}
    fuori.update(contro_t("geometrico3d n=%d" % N_I1, S3D.geometrico3d(N_I1),
                          S3D.punti3d(N_I1, 11)))
    fuori.update(contro_t("cubico L=%d (controllo)" % L_CONTROLLO,
                          S3D.cubico(L_CONTROLLO), S3D.punti_cubico(L_CONTROLLO)))
    return fuori


# =====================================================================================
#   I2 — LE VARIANTI, tutte alla STESSA taglia
# =====================================================================================
def _varianti():
    """### Le sette varianti. ### **`(i)` e' il RIFERIMENTO**, `(iv-V)` il **CONTROLLO
    DICHIARATO** *(pesi dalla geometria, che la decisione `9` vieta nella fisica)*."""
    # ### ⛔ **IL BRACCIO E' UN CAMPO DELLA TUPLA, NON SI RICAVA DAL NOME.** Lo
    # ### ricavavo con `nome.split(...)`, e la combinazione `(ii)+(iv-U)` lo ### **ha
    # ### rotto subito** *(`KeyError: '(ii'`)*: ### **leggere una decisione da un titolo
    # ### e' la cosa che `[[DECISIONE-VUOLE-UN-CAMPO]]` vieta**, e qui si e' vista
    # ### fallire ### **dieci minuti dopo averla scritta.**
    casi = [(RIFERIMENTO, S3D.geometrico3d(N_I2), S3D.punti3d(N_I2, 11), None, None),
            (RESPINTI, S3D.geometrico3d(N_I2, rilassati=True),
             S3D.punti3d_rilassati(N_I2, 11), None, None),
            ("(iii) uniformi, gradi 4-6", S3D.geometrico3d(N_I2, gmin=4, gmax=6),
             S3D.punti3d(N_I2, 11), None, None)]
    sc_iv = P4.scena_delaunay(N_I2)
    pos_iv = P4.punti_delaunay(N_I2, 11)
    for br in P4.BRACCI:
        casi.append(("(iv-%s) Delaunay, pesi %s" % (br, br), sc_iv, pos_iv,
                     P4.peso_di(sc_iv, br), br))
    # ### ⭐ **LA COMBINAZIONE `(ii)+(iv-U)`, che l'aggiunta di Luca chiede:** punti
    # ### che si ### **RESPINGONO**, ### **tutti i vicini** collegati, ### **pesi tutti
    # ### uguali.** ### ⛔ **E PRENDE LE STESSE MISURE DELLE ALTRE**, perche' entra
    # ### nella stessa lista: ### **non c'e' una via separata che potrebbe divergere.**
    sc_c = P4.scena_delaunay(N_I2, rilassati=True)
    casi.append((COMBINAZIONE, sc_c, P4.punti_delaunay(N_I2, 11, rilassati=True),
                 P4.peso_di(sc_c, "U"), "U"))
    return casi


def _costo(sc, peso, giri=20):
    """### Il **COSTO PER TICK**, misurato: la variante `(iv)` ha `2.8` volte gli archi."""
    geo = GE.scena_identita(sc)
    psi = CM.stato_casuale(sc, 11)
    un = np.ones(sc["n"])
    t0 = time.time()
    for _ in range(giri):
        if peso is None:
            psi = C2.passo2(psi, sc, geo, un, 1.0, 0.5)
        else:
            x = C2.moneta_spin(psi, geo, 0.5, un * 1.0, sc)
            x = P4.grover_pesato(x, sc, peso)
            psi = C2.spostamento_trasporto(x, geo, sc)
    return (time.time() - t0) / giri


def i2():
    fuori = {"n": N_I2, "passi": T_I2, "nodi": NODI, "varianti": {},
             "riferimento": RIFERIMENTO, "controllo_pesi": CONTROLLO_PESI}
    for nome, sc, pos, peso, braccio in _varianti():
        diam, esatto = diametro(sc)
        ds = S3D.dimensione_spettrale(
            sc, diam, semi_nodi=(0, sc["n"] // 3, sc["n"] // 2))
        nodi = S3D.nodi_a_caso(sc, NODI, SEME_NODI)
        r = S3D.isotropia(sc, pos, passi=T_I2, nodi=nodi, peso=peso)
        e = r["euclideo"]
        v = {k: e[k] for k in ("irregolarita", "sigma_irregolarita", "anisotropia",
                               "rumore", "aniso_su_rumore", "sistematica")}
        v.update({"n": sc["n"], "m": sc["m"], "diametro": diam,
                  "diametro_esatto": esatto, "d_s": ds["d_s"], "r2_d_s": ds["r2"],
                  "gradi": [int(sc["grado"].min()), int(sc["grado"].max())],
                  "costo_per_tick": _costo(sc, peso),
                  "braccio": braccio,
                  # ### ⛔ **E QUESTO CAMPO DICE SE I PESI VENGONO DALLE POSIZIONI**, che
                  # ### e' esattamente la cosa che la seconda versione del mandato vieta.
                  "pesi_dalle_posizioni": bool(P4.LEGGE_POSIZIONI[braccio])
                  if braccio is not None else False,
                  # ### ⭐ **LA CORRELAZIONE: lo sbilanciamento SPIEGA l'irregolarita'?**
                  "correlazione": S3D.correlazione(sc, pos, r, peso)})
        fuori["varianti"][nome] = v
        print("  %-28s m %-6d gradi %-7s d_s %-7.3f irr %.4f+-%.4f  a/r %-6.2f "
              "costo %.4f s  pearson %+.3f (%.1f sigma)"
              % (nome, sc["m"], "%d..%d" % tuple(v["gradi"]), ds["d_s"],
                 v["irregolarita"], v["sigma_irregolarita"], v["aniso_su_rumore"],
                 v["costo_per_tick"], v["correlazione"]["pearson"],
                 v["correlazione"]["in_sigma"]))
    # ### ⛔ **IL CONFRONTO, ed e' LA DOMANDA DEL MANDATO:** quanto `(iv-U)` e `(iv-R)` si
    # ### avvicinano a `(iv-V)`?
    rif = fuori["varianti"][RIFERIMENTO]
    vor = fuori["varianti"][CONTROLLO_PESI]
    conf = {}
    for nome, v in fuori["varianti"].items():
        if nome == RIFERIMENTO:
            continue
        sg = math.sqrt(v["sigma_irregolarita"] ** 2 + rif["sigma_irregolarita"] ** 2)
        sv = math.sqrt(v["sigma_irregolarita"] ** 2 + vor["sigma_irregolarita"] ** 2)
        gua = rif["irregolarita"] - v["irregolarita"]
        guav = rif["irregolarita"] - vor["irregolarita"]
        conf[nome] = {
            "guadagno": gua, "in_sigma": (gua / sg) if sg > 0 else float("inf"),
            "quota_del_guadagno_di_voronoi": (gua / guav) if abs(guav) > 1e-12
            else float("nan"),
            "contro_voronoi_in_sigma": (abs(v["irregolarita"] - vor["irregolarita"]) / sv)
            if sv > 0 else float("inf"),
            "sopra_soglia": bool(sg > 0 and abs(gua) > 3.0 * sg)}
    fuori["confronto_col_riferimento"] = conf
    # ### ⭐ **`s10`: I DUE EFFETTI SI SOMMANO?** Il guadagno della combinazione contro
    # ### la ### **SOMMA dei due guadagni separati**, con le `sigma` propagate in
    # ### quadratura. ### ⛔ **E la previsione era NO, si sovrappongono.**
    if COMBINAZIONE in fuori["varianti"]:
        g_ii = conf[RESPINTI]["guadagno"]
        g_iv = conf[TUTTI_VICINI]["guadagno"]
        g_c = conf[COMBINAZIONE]["guadagno"]
        s_ii = fuori["varianti"][RESPINTI]["sigma_irregolarita"]
        s_iv = fuori["varianti"][TUTTI_VICINI]["sigma_irregolarita"]
        s_c = fuori["varianti"][COMBINAZIONE]["sigma_irregolarita"]
        s_rif = rif["sigma_irregolarita"]
        # ### la `sigma` della SOMMA dei due guadagni: i due `(i)` entrano due volte
        s_somma = math.sqrt(s_ii ** 2 + s_iv ** 2 + 2.0 * s_rif ** 2)
        s_dif = math.sqrt(s_c ** 2 + s_rif ** 2 + s_somma ** 2)
        dif = g_c - (g_ii + g_iv)
        fuori["s10_additivita"] = {
            "guadagno_respinti": g_ii, "guadagno_tutti_vicini": g_iv,
            "somma_dei_due": g_ii + g_iv, "sigma_somma": s_somma,
            "guadagno_combinazione": g_c, "sigma_combinazione": s_c,
            "differenza": dif, "sigma_differenza": s_dif,
            "in_sigma": (abs(dif) / s_dif) if s_dif > 0 else float("inf"),
            "verdetto": ("ADDITIVI" if s_dif > 0 and abs(dif) <= 3.0 * s_dif
                         else ("SI SOVRAPPONGONO" if dif < 0 else "PIU CHE ADDITIVI")),
            "sopra_il_massimo_dei_due": bool(g_c > max(g_ii, g_iv))}
    return fuori


def m_a():
    """### `M-A`: la **dimensione spettrale a TAGLIA GRANDE**, con lo stesso protocollo.

    > ### ⛔ **E IL CRITERIO E' LO SCARTO DA `3`, NON IL VALORE** *(soglia `s9`)*:
    > ### **`d_s > 3` e' un difetto come `d_s < 3`** -- un grafo con dimensione spettrale
    > `3.5` ### **non e' uno spazio tridimensionale.**
    """
    fuori = {"taglie": list(TAGLIE_DS), "famiglie": {}}
    famiglie = (
        (RIFERIMENTO, lambda n: S3D.geometrico3d(n)),
        (RESPINTI, lambda n: S3D.geometrico3d(n, rilassati=True)),
        (TUTTI_VICINI, lambda n: P4.scena_delaunay(n)),
        (COMBINAZIONE, lambda n: P4.scena_delaunay(n, rilassati=True)),
    )
    for nome, fab in famiglie:
        riga = {}
        for n in TAGLIE_DS:
            t0 = time.time()
            try:
                sc = fab(n)
            except MemoryError as e:
                # ### ⛔ **UNA TAGLIA CHE SFORA SI DICHIARA, e la misura si FERMA alla
                # ### precedente** -- ### **senza ridurre la precisione**, come il mandato
                # ### ⚠ **E SI PRENDE *SOLO* `MemoryError`:** un `except Exception`
                # ### scriverebbe <<non misurata>> anche su ### **un MIO errore di
                # ### codice** -- cioe' trasformerebbe ### **un difetto in un limite di
                # ### taglia**, che e' il modo piu' pulito di nascondere un difetto.
                # ### del legame ha gia' stabilito.
                riga[str(n)] = {"non_misurata": "%s: %s" % (type(e).__name__, e)}
                print("    %-46s n = %-7d ### NON MISURATA: %s"
                      % (nome, n, type(e).__name__))
                break
            diam, esatto = diametro(sc)
            ds = S3D.dimensione_spettrale(
                sc, diam, semi_nodi=(0, sc["n"] // 3, sc["n"] // 2))
            riga[str(n)] = {
                "d_s": ds["d_s"], "r2": ds["r2"], "potenza": bool(ds["potenza"]),
                "scarto_da_3": abs(ds["d_s"] - 3.0), "n": sc["n"], "m": sc["m"],
                "diametro": diam, "diametro_esatto": esatto,
                "gradi": [int(sc["grado"].min()), int(sc["grado"].max())],
                "secondi": time.time() - t0}
            print("    %-46s n = %-7d d_s %-7.3f |d_s-3| %-7.3f m %-7d gradi %-8s "
                  "(%.0f s)"
                  % (nome, n, ds["d_s"], abs(ds["d_s"] - 3.0), sc["m"],
                     "%d..%d" % (sc["grado"].min(), sc["grado"].max()),
                     time.time() - t0))
            del sc
        # ### ⭐ **IL VERDETTO `s8`: CRESCE in modo monotono E arriva a `3`?**
        vive = [(int(k), v["d_s"]) for k, v in sorted(riga.items(), key=lambda x: int(x[0]))
                if "d_s" in v]
        mono = all(vive[i][1] <= vive[i + 1][1] for i in range(len(vive) - 1)) \
            if len(vive) >= 2 else None
        ult = vive[-1] if vive else None
        fuori["famiglie"][nome] = {
            "per_taglia": riga, "monotona": mono,
            "taglia_massima": (ult[0] if ult else None),
            "d_s_massima": (ult[1] if ult else float("nan")),
            "scarto_da_3": (abs(ult[1] - 3.0) if ult else float("nan")),
            "verdetto_s8": ("TENDE A 3" if (mono and ult and abs(ult[1] - 3.0) <= 0.3)
                            else ("NON ARRIVA A 3" if ult else "NON MISURATA"))}
    # ### ⛔ **E IL CONFRONTO `s9`: chi ha lo SCARTO minore alla taglia massima.**
    buone = {k: v["scarto_da_3"] for k, v in fuori["famiglie"].items()
             if v["scarto_da_3"] == v["scarto_da_3"]}
    fuori["piu_tridimensionale"] = (min(buone, key=buone.get) if buone else None)
    return fuori


def m_c():
    """### `M-C` e la parte di `M-B` contro `t`: il **PAVIMENTO** a taglia grande.

    ### ⛔ **ALLA STESSA TAGLIA DI `I1` E CON LA STESSA VIA**, altrimenti il confronto
    con lo `0.17` di `(i)` ### **sarebbe fra due esperimenti diversi.**
    """
    fuori = {}
    for nome, fab, fabp in (
            (RESPINTI, lambda n: S3D.geometrico3d(n, rilassati=True),
             lambda n: S3D.punti3d_rilassati(n, 11)),
            (COMBINAZIONE, lambda n: P4.scena_delaunay(n, rilassati=True),
             lambda n: P4.punti_delaunay(n, 11, rilassati=True))):
        try:
            sc = fab(N_I1)
            pos = fabp(N_I1)
        except MemoryError as e:
            fuori[nome] = {"non_misurata": "%s: %s" % (type(e).__name__, e)}
            print("    %-46s ### NON MISURATA a n = %d: %s"
                  % (nome, N_I1, type(e).__name__))
            continue
        fuori.update(contro_t("%s n=%d" % (nome, N_I1), sc, pos))
        del sc, pos
    return fuori


def uniformita():
    """### La **PROVA** che `(ii)` rende i punti davvero piu' uniformi: la distanza al
    **primo vicino**. ### ⛔ **Senza questa, <<respinti>> e' una PAROLA.**"""
    from scipy.spatial import cKDTree
    fuori = {}
    for nome, p in (("(i) uniformi", S3D.punti3d(N_I2, 11)),
                    ("(ii) respinti", S3D.punti3d_rilassati(N_I2, 11))):
        d, _ = cKDTree(p, boxsize=1.0).query(p, k=2)
        d1 = d[:, 1]
        fuori[nome] = {"media": float(np.mean(d1)), "minimo": float(np.min(d1)),
                       "dispersione_relativa": float(np.std(d1, ddof=1) / np.mean(d1))}
        print("  %-16s primo vicino: media %.5f  minimo %.5f  dispersione %.4f"
              % (nome, fuori[nome]["media"], fuori[nome]["minimo"],
                 fuori[nome]["dispersione_relativa"]))
    a, b = fuori["(i) uniformi"], fuori["(ii) respinti"]
    fuori["rapporto_minimi"] = (b["minimo"] / a["minimo"]) if a["minimo"] > 0 \
        else float("nan")
    fuori["rapporto_dispersioni"] = (b["dispersione_relativa"]
                                     / a["dispersione_relativa"])
    return fuori


def main():
    os.makedirs(USCITE, exist_ok=True)
    fuori = {"blob": _presidio.timbro(__file__)["sha1"], "tempi_chiesti": list(TEMPI),
             "velocita_fronte": V_FRONTE}
    print("=" * 100)
    print("  --- la prova di UNIFORMITA' dei punti (serve a `(ii)`) ---")
    fuori["uniformita"] = uniformita()
    print("  --- I1: l'irregolarita' contro la distanza ---")
    fuori["I1"] = i1()
    print("  --- I2: le varianti, tutte a n = %d e t = %d ---" % (N_I2, T_I2))
    fuori["I2"] = i2()
    if "s10_additivita" in fuori["I2"]:
        a = fuori["I2"]["s10_additivita"]
        print("    ### s10: guadagno combinazione %.4f contro somma dei due %.4f "
              "-> %.1f sigma, %s"
              % (a["guadagno_combinazione"], a["somma_dei_due"], a["in_sigma"],
                 a["verdetto"]))
    print("  --- M-A: la dimensione spettrale a TAGLIA GRANDE ---")
    fuori["M_A"] = m_a()
    print("    ### la piu' tridimensionale alla taglia massima: %s"
          % fuori["M_A"]["piu_tridimensionale"])
    print("  --- M-C: il pavimento a taglia grande ---")
    fuori["M_C"] = m_c()
    io.open(FONTE, "wb").write(
        (json.dumps(fuori, ensure_ascii=False, indent=1, sort_keys=True)
         + chr(10)).encode("utf-8"))
    print("-" * 100)
    print("  scritto %s" % os.path.relpath(FONTE, RADICE).replace(os.sep, "/"))
    print("=" * 100)
    return 0


if __name__ == "__main__":
    sys.exit(main())
