# -*- coding: utf-8 -*-
r"""LA DIAGNOSI DELLA MEMORIA — **in PARALLELO al run in volo, su una scena PICCOLA.**

### ⛔ **QUESTO FILE E' NUOVO, E NON NE TOCCA NESSUN ALTRO:** i moduli del run si
**IMPORTANO e si LEGGONO**, mai si modificano *(par.5)*. ### **La cura, se si trova, si
applica DOPO che il run ha chiuso.**

> ## ⭐ **IL FATTO DA SPIEGARE:** il run di `[[LEGAME-SCENE-GRANDI]]` cresce di
> ## **`+1.2` GB in UNA scena** *(`1382` → `2340` → `2613` → `2685` MB di privata)* con il
> ## checkpoint **FERMO**, su uno stato che a quella taglia e' **`4.5` MB** — cioe'
> ## ### **~`580` volte lo stato.** ### **Le cure di `4bc0ce9` sono PROTEZIONI: non
> ## spiegano la CAUSA.**

> ## ⛔ **IL TETTO DI SICUREZZA:** se questo processo supera `1.5` GB di privata
> ## ### **si ferma da solo** e scrive cio' che ha misurato fino a li'. ### **E gira a
> ## priorita' BASSA**, per non rallentare il run.

Gira con:  python proto_camminata/_diagnosi_memoria.py [PID_DEL_RUN]
"""
import gc
import io
import json
import math
import os
import sys
import time
import tracemalloc

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
sys.path.insert(0, _QUI)
sys.path.insert(0, os.path.join(RADICE, "csv"))
import _presidio                                              # noqa: E402

_presidio.avvia(__file__)

import psutil                                                 # noqa: E402

import camminata as CM                                        # noqa: E402
import camminata2 as C2M                                      # noqa: E402
import camminata3 as C3                                       # noqa: E402
import geometria as GE                                        # noqa: E402
import scena as SC                                            # noqa: E402
import scene3d as S3D                                         # noqa: E402
import segni1 as S1                                           # noqa: E402
import vuoto3 as V3                                           # noqa: E402
import _letture3 as L3                                        # noqa: E402
# ### ⛔ **SI IMPORTA IL MODULO DEL RUN, e questo e' LECITO:** importare e' LEGGERE.
# ### ⭐ **E serve proprio quello:** se misurassi una COPIA della sua `profilo`, misurerei
# ### ### **un'altra funzione** -- e la domanda e' su QUELLA.
import _letture_legame_grandi as LG                           # noqa: E402

SC._niente_simulatore()

N_SCENA = 2000
SEME = 11
X0 = 8.0
EPS_RIF = 0.5
# ### ⛔ **IL TETTO, in byte.** Non e' una scelta di comodo: e' il numero del mandato.
TETTO = int(1.5 * 1024 ** 3)
# ### quante volte si ripete un pezzo per vedere se la memoria SALE
GIRI = 60
USCITE = os.path.join(_QUI, "uscite")
FONTE = os.path.join(USCITE, "diagnosi_memoria.json")
IO = psutil.Process()


def privata():
    """### La memoria **PRIVATA** del processo, in byte. ### **E' quella che pesa sul
    commit**, cioe' quella che fa fallire un'allocazione."""
    m = IO.memory_info()
    return int(getattr(m, "private", getattr(m, "vms", 0)))


def mb(x):
    return x / 1048576.0


class Tetto(Exception):
    """### Il tetto di sicurezza ha scattato."""


def _guarda():
    if privata() > TETTO:
        raise Tetto("privata %.0f MB oltre il tetto di %.0f MB"
                    % (mb(privata()), mb(TETTO)))


def pendenza(xs, ys):
    """### La crescita **per giro**, con la sua `sigma` dai residui."""
    if len(xs) < 3:
        return {"per_giro_MB": float("nan"), "nota": "meno di tre punti"}
    x = np.asarray(xs, float)
    y = np.asarray([mb(v) for v in ys], float)
    a, b = np.polyfit(x, y, 1)
    res = y - (a * x + b)
    sa = (math.sqrt(float(np.sum(res ** 2)) / max(len(x) - 2, 1))
          / math.sqrt(float(np.sum((x - x.mean()) ** 2))))
    return {"per_giro_MB": float(a), "sigma": float(sa),
            "in_sigma": (abs(a) / sa) if sa > 0 else float("inf"),
            "cresce": bool(sa > 0 and a > 3.0 * sa),
            "da_MB": float(y[0]), "a_MB": float(y[-1]),
            "totale_MB": float(y[-1] - y[0]), "giri": int(x[-1])}


def misura(nome, fai, giri=GIRI, ogni=5):
    """### Ripete `fai` e guarda se la privata SALE. ### **E' il misurando centrale.**

    ### ⛔ **`gc.collect()` PRIMA del campione, non dopo:** cosi' cio' che si misura e'
    ### **cio' che NON si libera**, non la spazzatura che aspetta.
    """
    gc.collect()
    xs, ys = [0], [privata()]
    t0 = time.time()
    try:
        for k in range(1, giri + 1):
            fai()
            if k % ogni == 0:
                gc.collect()
                xs.append(k)
                ys.append(privata())
                _guarda()
    except Tetto as e:
        print("    ### TETTO: %s" % e)
        raise
    p = pendenza(xs, ys)
    p["secondi"] = time.time() - t0
    p["campioni"] = [[int(a), float(mb(b))] for a, b in zip(xs, ys)]
    print("    %-44s %+8.4f MB/giro  (%s)  %6.1f -> %6.1f MB   %.0f s"
          % (nome, p["per_giro_MB"],
             "### CRESCE" if p["cresce"] else "ferma",
             p["da_MB"], p["a_MB"], p["secondi"]))
    return p


def main():
    os.makedirs(USCITE, exist_ok=True)
    pid_run = int(sys.argv[1]) if len(sys.argv) > 1 else None
    fuori = {"blob": _presidio.timbro(__file__)["sha1"], "n_scena": N_SCENA,
             "seme": SEME, "x0": X0, "giri": GIRI, "tetto_MB": mb(TETTO),
             "pezzi": {}}

    # ================================================ il run in volo, PRIMA
    def vivo():
        if pid_run is None:
            return None
        try:
            p = psutil.Process(pid_run)
            return {"vivo": p.is_running(), "privata_MB": mb(
                int(getattr(p.memory_info(), "private", 0)))}
        except psutil.NoSuchProcess:
            return {"vivo": False}

    fuori["run_in_volo_prima"] = vivo()
    try:
        IO.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
        fuori["priorita"] = "BELOW_NORMAL"
    except Exception as e:                                    # noqa: BLE001
        fuori["priorita"] = "non abbassata: %s" % type(e).__name__
    print("=" * 100)
    print("LA DIAGNOSI DELLA MEMORIA -- scena piccola, in parallelo al run")
    print("  priorita': %s   run in volo: %s" % (fuori["priorita"],
                                                 fuori["run_in_volo_prima"]))

    # ================================================ la scena e lo stato
    sc = S3D.geometrico3d(N_SCENA, rilassati=True)
    geo = GE.scena_identita(sc)
    d = SC.distanze(sc, 0)
    ne = 2 * sc["m"]
    stato_MB = mb(ne * 2 * 16)
    fuori["scena"] = {"n": sc["n"], "m": sc["m"], "estremita": ne,
                      "stato_MB": stato_MB,
                      "nome": sc["nome"]}
    print("  scena: n = %d, m = %d, estremita' = %d, ### stato = %.2f MB"
          % (sc["n"], sc["m"], ne, stato_MB))
    print("  --- (a) e (c): la crescita PER PEZZO, %d giri ciascuno ---" % GIRI)

    st = C3.stato3(sc, SEME)
    uno = np.ones(sc["n"])
    psi0 = st["psi"].copy()
    phi0 = st["phi"].copy()
    fl_N = S1.flusso_di("+N")
    fl_D = S1.flusso_di("+D")
    tempi = LG.tempi_di(LG.diametro(sc)[0])
    fuori["tempi_del_run"] = tempi

    # ### ⛔ **OGNI PEZZO RIPARTE DALLO STESSO STATO:** altrimenti misurerei anche la
    # ### ### **crescita dello stato**, che non e' una perdita.
    PEZZI = (
        ("1 moneta_spin", lambda: C2M.moneta_spin(psi0, geo, EPS_RIF, uno, sc)),
        ("2 moneta_grover", lambda: CM.moneta_grover(psi0, sc)),
        ("3 spostamento_trasporto",
         lambda: C2M.spostamento_trasporto(psi0, geo, sc)),
        ("4 grover_scalare + spostamento_scalare",
         lambda: V3.spostamento_scalare(V3.grover_scalare(phi0, sc))),
        ("5 passo2 (il lineare intero)",
         lambda: C2M.passo2(psi0, sc, geo, uno, 1.0, EPS_RIF)),
        ("6 flusso +N", lambda: fl_N(psi0, phi0, sc, geo, 0.5)),
        ("7 flusso +D (punto medio IMPLICITO)",
         lambda: fl_D(psi0, phi0, sc, geo, 0.5)),
        ("8 passo3 con +N",
         lambda: C3.passo3(st, sc, geo, uno, 1.0, EPS_RIF, fl_N)),
        ("9 passo3 con +D",
         lambda: C3.passo3(st, sc, geo, uno, 1.0, EPS_RIF, fl_D)),
        ("10 la MISURA (raggi, frazioni, fondo)",
         lambda: (LG.raggio_in_archi(sc, st, d, 0.90),
                  LG.raggio_in_archi(sc, st, d, 0.50),
                  L3.frazione_entro(sc, st, 0, d, 1),
                  L3.fondo_uniforme(sc, d, 1))),
        ("11 grumo (la condizione iniziale)",
         lambda: L3.grumo(sc, geo, 0, 1, X0, seme=SEME)),
    )
    fermato = None
    try:
        for nome, fai in PEZZI:
            fuori["pezzi"][nome] = misura(nome, fai)
        # ================================================ (a) la `profilo` INTERA
        print("  --- (a) la `profilo` del run, come la chiama il run ---")
        for et, fl in (("+D", fl_D), ("+N", fl_N)):
            fuori["pezzi"]["12 profilo %s (come il run)" % et] = misura(
                "12 profilo %s (come il run)" % et,
                lambda fl=fl: LG.profilo(sc, geo, fl, X0, SEME, tempi, d),
                giri=8, ogni=1)
    except Tetto as e:
        fermato = str(e)

    # ================================================ (b) `tracemalloc`
    print("  --- (b) tracemalloc: le righe che crescono di piu' ---")
    tracemalloc.start(12)
    s0 = tracemalloc.take_snapshot()
    meta = []
    try:
        for k in range(6):
            LG.profilo(sc, geo, fl_D, X0, SEME, tempi, d)
            if k == 2:
                meta = tracemalloc.take_snapshot()
            _guarda()
    except Tetto as e:
        fermato = fermato or str(e)
    s1 = tracemalloc.take_snapshot()
    tot_trac = sum(x.size for x in s1.statistics("filename"))
    righe = []
    for st_ in s1.compare_to(s0, "lineno")[:15]:
        t = st_.traceback[0] if st_.traceback else None
        righe.append({"file": (t.filename if t else "?"),
                      "riga": (t.lineno if t else 0),
                      "crescita_MB": mb(st_.size_diff),
                      "blocchi": st_.count_diff, "totale_MB": mb(st_.size)})
    fuori["tracemalloc"] = {
        "tracciato_totale_MB": mb(tot_trac), "righe": righe,
        "meta_vs_inizio_MB": (mb(sum(x.size_diff for x in meta.compare_to(s0, "filename")))
                              if meta else float("nan")),
        # ### ⚠ **E IL LIMITE DI `tracemalloc` SI DICHIARA:** traccia le allocazioni che
        # ### passano dall'allocatore di Python, e ### **i buffer di `numpy` di norma NON
        # ### ci passano** *(`malloc` diretto)*. ### **Se il totale tracciato e' molto piu'
        # ### piccolo della crescita vista dal sistema, la causa e' FUORI dal suo
        # ### sguardo** -- e il confronto fra i due numeri e' ### **esso stesso un
        # ### risultato.**
        "nota": ("tracemalloc vede solo l'allocatore di Python: i buffer di numpy di "
                 "norma usano malloc diretto e NON compaiono")}
    tracemalloc.stop()
    for r in righe[:8]:
        print("    %+9.3f MB  %-46s :%d"
              % (r["crescita_MB"], os.path.basename(r["file"]), r["riga"]))
    print("    ### totale TRACCIATO da tracemalloc: %.1f MB"
          % fuori["tracemalloc"]["tracciato_totale_MB"])

    # ================================================ il run in volo, DOPO
    fuori["run_in_volo_dopo"] = vivo()
    fuori["fermato_dal_tetto"] = fermato
    fuori["privata_finale_MB"] = mb(privata())
    io.open(FONTE, "wb").write(
        (json.dumps(fuori, ensure_ascii=False, indent=1, sort_keys=True)
         + chr(10)).encode("utf-8"))
    print("-" * 100)
    print("  run in volo PRIMA: %s" % fuori["run_in_volo_prima"])
    print("  run in volo DOPO:  %s" % fuori["run_in_volo_dopo"])
    print("  privata finale di QUESTO processo: %.0f MB%s"
          % (fuori["privata_finale_MB"],
             ("   ### FERMATO DAL TETTO: %s" % fermato) if fermato else ""))
    print("  scritto %s" % os.path.relpath(FONTE, RADICE).replace(os.sep, "/"))
    print("=" * 100)
    return 0


if __name__ == "__main__":
    sys.exit(main())
