r"""**IL PILOTA DELLA `PROVA 1`** — 4 semi, **un processo per seme** (`STANDARD 1`), il referto.

*(criteri `V1`-`V6` di `doc/TASK_HISTORY/2026-09-27_pilota-prova1.md`, scritti **prima**.)*

> ## ⚠ **NON E' IL RUN BASE.** `doc/SMISTAMENTO_run_base.md` conta **5 `SI` aperti**.
> **Nessuna conclusione sulla gravita' da qui: solo i numeri e i limiti** *(mandato di Luca)*.

**L'OSSERVABILE DI `V2`, scritto prima di guardare:**

    A(t) = [ (m(t) - m(0)) - (c(t) - c(0)) ] / m(0)

con `m` la distanza fra i CENTRI di due masse e `c` quella fra i due punti di **CONTROLLO** nel
vuoto **alla stessa distanza iniziale**. **Adimensionale**, e la barra e' **fra semi** (`P3`,
`t(3) = 3.182`). **Se `m` e `c` calano uguale, `A = 0` e non e' gravita': e' contrazione globale.**

> ### ⚠ **I CONTROLLI SONO FISSI: scelti UNA VOLTA al passo 0 e poi SEGUITI.**
> **Con la RISCELTA l'osservabile va a ZERO per costruzione**, perche' la coppia di vuoto
> viene cercata alla distanza **del momento** fra le masse: `c(t) ~ m(t)`, quindi `A -> 0`
> **qualunque cosa faccia la gravita'**. **Misurato in `K5b`** *(`csv/_osservabile_p1.py
> --collaudo-controlli`)*: su un effetto vero del `-5 %` la riscelta legge **`+0.025 %`**.
> *(`CTRL-RISCELTA`, difetto trovato da Luca il 2026-09-27 dentro il mio stesso
> `COSA-RICONTROLLARE`: l'avevo chiamato «limite DICHIARATO», e dichiararlo non basta -- `A9`.)*
> **La riscelta resta nel referto come DIAGNOSTICO**, cosi' il difetto e' visibile nei dati
> del run stesso invece di essere solo raccontato.

    python csv/_test_fork/_pilota_prova1.py                 # 4 semi, 120 passi
    python csv/_test_fork/_pilota_prova1.py --passi 4 --checkpoint 0,2,4    # impianto
    python csv/_test_fork/_pilota_prova1.py --solo-referto  # rilegge i json e rifa' il referto

ASCII puro.
"""
import io
import json
import os
import subprocess
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, os.path.join(RADICE, "csv"))

import _presidio                                                       # noqa: E402
import _cli_flag                                                       # noqa: E402
import _osservabile_p1 as OP                                           # noqa: E402

_presidio.avvia(__file__)

NL = chr(10)
DEST = os.path.join(_QUI, "_pilota_prova1")
REFERTO = os.path.join(DEST, "REFERTO.txt")
SEMI = [11, 12, 13, 14]
R = []


def P(s=""):
    print(s)
    R.append(s)


def lancia(semi, passi, cps):
    """Un processo per seme, **in parallelo**: sono bracci indipendenti (`STANDARD 1`)."""
    proc = {}
    for s in semi:
        dd = os.path.join(DEST, "seme_%d" % s)
        if not os.path.isdir(dd):
            os.makedirs(dd)
        out = os.path.join(dd, "misura.json")
        if os.path.exists(out):
            os.remove(out)
        log = io.open(os.path.join(dd, "log.txt"), "w", encoding="utf-8", newline=NL)
        proc[s] = (subprocess.Popen(
            [sys.executable, os.path.join(_QUI, "_pilota_prova1_braccio.py"),
             "--seme", str(s), "--passi", str(passi),
             "--checkpoint", ",".join(str(c) for c in cps), "--out", out],
            cwd=RADICE, stdout=log, stderr=subprocess.STDOUT), log, out)
    fuori = {}
    for s, (q, log, out) in proc.items():
        q.wait()
        log.close()
        fuori[s] = json.load(io.open(out, encoding="utf-8")) if os.path.exists(out) else None
    return fuori


def leggi(semi):
    fuori = {}
    for s in semi:
        out = os.path.join(DEST, "seme_%d" % s, "misura.json")
        fuori[s] = json.load(io.open(out, encoding="utf-8")) if os.path.exists(out) else None
    return fuori


def blocco(d, passo):
    for b in d["blocchi"]:
        if int(b["passo"]) == int(passo):
            return b
    return None


def barra(valori, etichetta, unita="", P=P, nullo=None):
    """La riga con IC95 fra semi, e **il LIMITE quando contiene lo zero** (presidio del nullo)."""
    o = OP.dispersione(valori)
    if o["ic95"] is None:
        P("    %-46s %s" % (etichetta, o.get("nota", "un solo valore")))
        return o
    lo, hi = o["ic95"]
    zero = (lo <= 0.0 <= hi)
    coda = ""
    if zero:
        ris = max(abs(lo), abs(hi))
        coda = "   CONTIENE LO ZERO -> LIMITE |x| < %.4g%s" % (ris, unita)
    P("    %-46s %+.5f %s  sd %.5f  IC95 [%+.5f, %+.5f]  n=%d%s"
      % (etichetta, o["media"], unita, o["sd"], lo, hi, o["n"], coda))
    return o


def referto(dati, passi, cps):
    semi = sorted(k for k in dati if dati[k] is not None)
    mancanti = [k for k in dati if dati[k] is None]
    P("=" * 108)
    P("PILOTA DELLA `PROVA 1`  --  %d semi, %d passi, checkpoint %s" % (len(semi), passi, cps))
    P("=" * 108)
    P("  ** NON E' IL RUN BASE: `doc/SMISTAMENTO_run_base.md` conta 5 `SI` APERTI. **")
    P("  ** Nessuna conclusione sulla gravita' da qui: solo i numeri e i limiti. **")
    # `H-P5`: IL REFERTO DICHIARA LA CONFIGURAZIONE INTERA, non i flag che ho toccato.
    # Si carica il simulatore UNA volta con l'argv del driver e si confrontano TUTTI i
    # booleani di modulo. Non dice <<i flag sono giusti>>: dice DOVE SI E' MISURATO.
    _S0, _argv = _cli_flag.argv_del_driver(
        dest=os.path.join(RADICE, "csv", "_test_fork", "_scarto_cli"))
    _S, _a = _cli_flag.carica_dal_cli(list(_argv), nome="sim_referto_pilota")
    _cli_flag.dichiara_configurazione(_S, P)
    if mancanti:
        P("  ** SEMI NON ARRIVATI IN FONDO: %s -- e si dicono, non si tolgono. **" % mancanti)
    if not semi:
        P("  NESSUN SEME. Il referto si fermerebbe qui.")
        return
    d0 = dati[semi[0]]
    P()
    P("  configurazione: POZZO_D %s   sep %.4f   r_regione %.4f   dphi %.4f   LAM %.3f"
      % (d0["pozzo_d"], d0["sep"], d0["r_regione"], d0["dphi"], d0["LAM"]))
    P("  nodi al passo 0: %s          nodi alla fine: %s"
      % ([dati[s]["n0"] for s in semi], [dati[s]["n_finale"] for s in semi]))
    P("  `kappa` scelto per seme: %s" % {s: dati[s]["kappa"] for s in semi})
    P("  regola: %s" % d0["kappa_regola"])

    # ------------------------------------------------------------------ LA CALIBRAZIONE (`V5`)
    P()
    P("-" * 108)
    P("CALIBRAZIONE DEL CRITERIO DI FASE AL PASSO 0  --  la risposta e' NOTA (`P1-sexies`)")
    P("-" * 108)
    P("  ⚠ IL CRITERIO DI FASE NON E' SCRITTO NEL CODICE: la scena costruisce la regione da `pos`")
    P("    e POI le assegna la fase. Il criterio si DERIVA: |wrap(phi - dphi/2)| <= kappa*0.05,")
    P("    con dphi/2 e 0.05 PRESI DALLA SCENA. L'unica scelta e' `kappa`.")
    P("  ⚠ E LA FASE E' LA STESSA PER TUTTE E TRE LE REGIONI (scelta dichiarata di Luca): quindi")
    P("    la fase NON separa le masse, e la separazione dev'essere di GRAFO.")
    P()
    P("  kappa | selez. | contam. MIS | contam. PREV | R-COMP prec/rich/vuote | R-VICINO prec/rich")
    for kp in [v["kappa"] for v in blocco(d0, 0)["calibrazione"]]:
        rr = []
        for s in semi:
            v = [x for x in blocco(dati[s], 0)["calibrazione"] if x["kappa"] == kp][0]
            rr.append(v)
        m = lambda f: float(np.mean([f(v) for v in rr]))                             # noqa: E731
        P("    %d   | %6.0f | %11.1f | %12.1f |  %.4f/%.4f/%.1f     |  %.4f/%.4f"
          % (kp, m(lambda v: v["selezionati"]), m(lambda v: v["contaminanti_misurati"]),
             m(lambda v: v["contaminanti_previsti"]),
             m(lambda v: v["regole"]["R-COMP"]["precisione_min"]),
             m(lambda v: v["regole"]["R-COMP"]["richiamo_min"]),
             m(lambda v: v["regole"]["R-COMP"]["masse_vuote"]),
             m(lambda v: v["regole"]["R-VICINO"]["precisione_min"]),
             m(lambda v: v["regole"]["R-VICINO"]["richiamo_min"])))
    P("  (medie sui %d semi. `contam. PREV` = 2*kappa*0.05/dphi del vuoto: il valore SOTTO" % len(semi))
    P("   IPOTESI NULLA del criterio di fase. Se MIS ~ PREV, i nodi in piu' sono vuoto entrato")
    P("   per caso, non massa nuova.)")

    # ------------------------------------------------------------------ `V1` I CONTROLLI
    P()
    P("-" * 108)
    P("`V1` -- I PUNTI DI CONTROLLO **FISSI** (scelti al passo 0 e SEGUITI)")
    P("-" * 108)
    f0 = blocco(d0, 0)["controlli_fissi"]
    P("  metro di <<lontano dalle masse>>: distanza di grafo > r_regione = %.4f da OGNI nodo"
      % f0["metro_lontananza"])
    P("  coppie chieste per coppia di masse: %d     candidati nel vuoto: %s"
      % (f0["quante_chieste"],
         [blocco(dati[s], 0)["controlli_fissi"]["candidati_lontani"] for s in semi]))
    for c in cps:
        f = [blocco(dati[s], c)["controlli_fissi"] for s in semi]
        P("  passo %4d   usate %s su %s   ESCLUSE: dentro una regione %s  componenti %s  inf %s"
          % (c, [x["usate"] for x in f], [x["totali"] for x in f],
             [x["esclusi_dentro"] for x in f], [x["esclusi_componenti"] for x in f],
             [x["esclusi_inf"] for x in f]))
    P("  (le esclusioni si CONTANO e NON si sostituiscono: sostituirle rifarebbe la riscelta"
      " con un altro nome.)")

    # ------------------------------------------------------------------ `V2` L'OSSERVABILE
    P()
    P("-" * 108)
    P("`V2` -- L'OSSERVABILE:  A(t) = [(m(t)-m(0)) - (c(t)-c(0))] / m(0)      [IC95 FRA SEMI]")
    P("-" * 108)
    coppie = sorted(blocco(d0, 0)["coppie_passo0"].keys())
    for c in cps:
        if c == 0:
            continue
        P("  passo %d:" % c)
        for cp in coppie:
            am, ac, aa, ar, arA = [], [], [], [], []
            for s in semi:
                b0, bt = blocco(dati[s], 0), blocco(dati[s], c)
                m0 = b0["coppie_passo0"][cp]["centro_centro"]
                mt = bt["coppie_passo0"][cp]["centro_centro"]
                if not (np.isfinite(m0) and m0 > 0):
                    continue
                am.append((mt - m0) / m0)
                # i controlli FISSI: la MEDIA sulle coppie non escluse, per seme
                righe = bt["controlli_fissi"]["coppie"].get(cp, [])
                v = [(r["distanza"] - r["distanza_0"]) / m0 for r in righe
                     if not r["escluso"] and np.isfinite(r["distanza"])]
                if v:
                    ac.append(float(np.mean(v)))
                    aa.append((mt - m0) / m0 - float(np.mean(v)))
                # e la RISCELTA, come DIAGNOSTICO del difetto `CTRL-RISCELTA`
                k0 = b0["controlli"]["coppie"].get(cp)
                kt = bt["controlli"]["coppie"].get(cp)
                if k0 and kt:
                    ar.append((kt["distanza"] - k0["distanza"]) / m0)
                    arA.append((mt - m0) / m0 - (kt["distanza"] - k0["distanza"]) / m0)
            barra(am, "%s  masse         (m(t)-m(0))/m(0)" % cp)
            barra(ac, "%s  CONTROLLI FISSI  (c(t)-c(0))/m(0)" % cp)
            barra(aa, "%s  A(t) = masse - FISSI   <- L'OSSERVABILE" % cp)
            barra(ar, "%s  [diagn.] controlli RISCELTI" % cp)
            barra(arA, "%s  [diagn.] A con la RISCELTA (difettosa)" % cp)
        P()
    P("  ⚠ LE DUE ULTIME RIGHE DI OGNI COPPIA SONO IL DIFETTO `CTRL-RISCELTA`, TENUTO A VISTA:")
    P("    `controlli()` RISCEGLIE la coppia di vuoto alla distanza DEL MOMENTO fra le masse,")
    P("    quindi `c(t) ~ m(t)` e `A -> 0` PER COSTRUZIONE. Se la riga [diagn.] A e' vicina a")
    P("    zero mentre l'osservabile NON lo e', si sta vedendo il difetto, non la fisica.")
    P("    (`K5b`: su un effetto vero del -5 %% la riscelta legge +0.025 %%.)")

    # ------------------------------------------------------------------ `V5` MIGRAZIONE
    P()
    P("-" * 108)
    P("`V5` -- LA MASSA SEGUE I NODI O LA COERENZA?   soglia: sovrapp >= 90 %% E spost < LAM")
    P("-" * 108)
    masse = sorted(blocco(d0, 0)["fase"]["per_massa"].keys())
    for c in cps:
        P("  passo %4d" % c)
        for k in masse:
            so = [blocco(dati[s], c)["fase"]["per_massa"][k]["sovrapposizione"] for s in semi]
            sp = [blocco(dati[s], c)["fase"]["per_massa"][k]["spostamento_medoide"] for s in semi]
            nn = [blocco(dati[s], c)["fase"]["per_massa"][k]["n"] for s in semi]
            P("    %-9s sovrapp %s   spost_medoide %s   n_fase %s"
              % (k, ["%.4f" % x for x in so], ["%.3f" % x for x in sp], nn))
    P()
    P("  IL VERDETTO DI `V5`, col criterio scritto prima:")
    for c in cps:
        so = [blocco(dati[s], c)["fase"]["per_massa"][k]["sovrapposizione"]
              for s in semi for k in masse]
        sp = [blocco(dati[s], c)["fase"]["per_massa"][k]["spostamento_medoide"]
              for s in semi for k in masse]
        so = [x for x in so if np.isfinite(x)]
        sp = [x for x in sp if np.isfinite(x)]
        ok = bool(so and sp and min(so) >= 0.90 and max(sp) < d0["LAM"])
        P("    passo %4d  min(sovrapp) %.4f   max(spost) %.4f   ->  %s"
          % (c, (min(so) if so else float("nan")), (max(sp) if sp else float("nan")),
             "LA MASSA SEGUE I NODI" if ok else "NON passa la soglia: vedi la nota"))
    P("  ⚠ E LA RISOLUZIONE DI `V5` E' LIMITATA DALLA CONTAMINAZIONE: se la precisione di")
    P("    `R-VICINO` al passo 0 e' ~0.80, un quinto dei nodi della regione di fase e' VUOTO")
    P("    entrato per caso, e il medoide di quella regione si sposta ANCHE per quello.")
    P("    Il confronto `coppie_fase` contro `coppie_passo0` dice di quanto.")

    # ------------------------------------------------------------------ le due distanze
    P()
    P("  LE DUE DISTANZE (nodi del passo 0 contro regioni ATTUALI): se divergono, si dice.")
    for c in cps:
        for cp in coppie:
            a = [blocco(dati[s], c)["coppie_passo0"][cp]["centro_centro"] for s in semi]
            b = [blocco(dati[s], c)["coppie_fase"][cp]["centro_centro"] for s in semi]
            dif = [y - x for x, y in zip(a, b) if np.isfinite(x) and np.isfinite(y)]
            P("    passo %4d %s   passo0 %.4f   fase %.4f   differenza media %+.4f"
              % (c, cp, float(np.mean(a)), float(np.nanmean(b)),
                 (float(np.mean(dif)) if dif else float("nan"))))

    # ------------------------------------------------------------------ `V6` LA FORMA
    P()
    P("-" * 108)
    P("`V6` -- LA FORMA: costante se OGNI grandezza resta entro la dispersione FRA SEMI del passo 0")
    P("-" * 108)
    # WARN L'ORDINE NON E' CASUALE, e la ragione e' MISURATA nel simulatore:
    #   `coer_campo = |<e^{i phi}>|` E' IL CRITERIO -- e' la coerenza COME IL CAMPO LA
    #   SENTE, e `Z118`/`Z120` dicono che in **31 righe su 31** il campo legge `phi` da
    #   `exp`/`cos`/`sin`, dove `phi` e `phi + 2 pi` sono IDENTICI. La doppia copertura
    #   vive nel SEGNO dello spinore e nei MEZZI ANGOLI, **non in `phi`**.
    #   `coer_dominio` e i `foglio_*` sono DIAGNOSTICI: contano la miscela di fogli, che
    #   la fisica del campo non vede ma **la TORSIONE distingue**.
    #   *(Ritiro di Luca, 2026-09-27, di una sua correzione della mattina -> `COER-4PI`.)*
    campi = [("n", ""), ("raggio", ""), ("p10", ""), ("p50", ""), ("p90", ""),
             ("coer_campo", " <- IL CRITERIO"), ("coer_dominio", " (diagn. fogli)"),
             ("foglio_0", " (diagnostico)"), ("foglio_1", " (diagnostico)")]
    for campo, _nota in campi:
        v0 = [blocco(dati[s], 0)["forma_passo0"][k][campo] for s in semi for k in masse]
        o0 = OP.dispersione(v0)
        P("  %-13s%-16s passo 0: media %12.5f  sd FRA SEMI+MASSE %.5f"
          % (campo, _nota, o0["media"], o0["sd"]))
        for c in cps:
            if c == 0:
                continue
            vt = [blocco(dati[s], c)["forma_passo0"][k][campo] for s in semi for k in masse]
            ot = OP.dispersione(vt)
            dd = ot["media"] - o0["media"]
            dentro = abs(dd) <= (o0["sd"] if np.isfinite(o0["sd"]) else np.inf)
            P("                   passo %4d: media %12.5f  delta %+12.5f  %s"
              % (c, ot["media"], dd, "entro la sd del passo 0" if dentro
                 else "** FUORI dalla sd del passo 0 **"))

    # ------------------------------------------------------------------ ALLUNGAMENTO
    P()
    P("-" * 108)
    P("`V6` -- CENTRI CONTRO SUPERFICI AFFACCIATE:  se le superfici si avvicinano PIU' dei centri")
    P("        oltre la barra, e' un ALLUNGAMENTO (possibile effetto mareale). E' un RISULTATO,")
    P("        non un difetto, e NON VA CORRETTO.")
    P("-" * 108)
    for c in cps:
        if c == 0:
            continue
        for cp in coppie:
            dc, ds, dl = [], [], []
            for s in semi:
                b0, bt = blocco(dati[s], 0), blocco(dati[s], c)
                c0 = b0["coppie_passo0"][cp]["centro_centro"]
                ct = bt["coppie_passo0"][cp]["centro_centro"]
                s0 = b0["coppie_passo0"][cp]["insieme_insieme"]
                st = bt["coppie_passo0"][cp]["insieme_insieme"]
                if not (np.isfinite(c0) and c0 > 0 and np.isfinite(s0) and s0 > 0):
                    continue
                dc.append((ct - c0) / c0)
                ds.append((st - s0) / s0)
                dl.append((st - s0) / s0 - (ct - c0) / c0)
            P("  passo %4d %s" % (c, cp))
            barra(dc, "   centri    (relativo)")
            barra(ds, "   superfici (relativo)")
            o = barra(dl, "   ALLUNGAMENTO = superfici - centri")
            if o["ic95"] and o["ic95"][1] < 0:
                P("      -> LE SUPERFICI SI AVVICINANO PIU' DEI CENTRI, oltre la barra: ALLUNGAMENTO.")

    # ------------------------------------------------------------------ `V3`/`V4` LE NASCITE
    P()
    P("-" * 108)
    P("`V3` -- DOVE SONO I NODI NATI (metro: `LAM`, la scala minima; varco entro il 10 %% del cammino)")
    P("-" * 108)
    for c in cps:
        if c == 0:
            continue
        P("  passo %4d   zone di TUTTI i nodi (media sui semi): %s"
          % (c, {z: round(float(np.mean([blocco(dati[s], c)["zone_tutti"][z] for s in semi])), 1)
                 for z in ("massa", "varco", "vuoto")}))
        for t in ("mitosi", "schwinger", "altro"):
            v = {z: round(float(np.mean([blocco(dati[s], c)["nascite_per_zona"][t][z]
                                         for s in semi])), 1)
                 for z in ("massa", "varco", "vuoto")}
            if sum(v.values()) > 0:
                P("               nati per %-10s %s" % (t, v))
        nc = [blocco(dati[s], c).get("nascite_per_chiamata", {}) for s in semi]
        chiavi = sorted({k for x in nc for k in x})
        P("               nodi creati per CHIAMATA del passo: %s"
          % {k: round(float(np.mean([x.get(k, 0) for x in nc])), 1) for k in chiavi})
        nd = [blocco(dati[s], c).get("nati_distanza_massa") for s in semi]
        nd = [x for x in nd if x]
        if nd:
            P("               distanza dei NATI dalla massa piu' vicina: p05 %.3f  p50 %.3f  p95 %.3f"
              % (float(np.mean([x["p05"] for x in nd])),
                 float(np.mean([x["p50"] for x in nd])),
                 float(np.mean([x["p95"] for x in nd]))))
    P()
    P("-" * 108)
    P("`V4` -- LE SCORCIATOIE DI SCHWINGER:  `2*dd < d` dell'arco (residuo `A3-DISEGNO`)")
    P("-" * 108)
    for c in cps:
        if c == 0:
            continue
        sw = [blocco(dati[s], c)["schwinger"] for s in semi]
        tot = float(np.mean([x["coppie"] for x in sw]))
        sc = float(np.mean([x["scorciatoie"] for x in sw]))
        P("  passo %4d   coppie %8.1f   scorciatoie %8.1f   (%s)   non trovate %.1f  ambigue %.1f"
          % (c, tot, sc, ("%.2f %%" % (100.0 * sc / tot)) if tot > 0 else "nessuna coppia",
             float(np.mean([x["arco_non_trovato"] for x in sw])),
             float(np.mean([x["ambigui"] for x in sw]))))
        rm = [x.get("rapporto_mediano") for x in sw if x.get("rapporto_mediano") is not None]
        if rm:
            P("               `2*dd/d` mediano %.4f   minimo %.4f"
              % (float(np.mean(rm)),
                 float(np.min([x["rapporto_min"] for x in sw if "rapporto_min" in x]))))
    P()
    P("=" * 108)
    P("FINE. Nessuna conclusione sulla gravita': il pilota dice se le grandezze si MISURANO.")
    P("=" * 108)


if __name__ == "__main__":
    A = sys.argv[1:]

    def opz(nome, dflt):
        return A[A.index(nome) + 1] if nome in A else dflt
    passi = int(opz("--passi", "120"))
    cps = sorted(set(int(x) for x in opz("--checkpoint", "0,40,80,120").split(",")))
    semi = [int(x) for x in opz("--semi", ",".join(str(s) for s in SEMI)).split(",")]
    if not os.path.isdir(DEST):
        os.makedirs(DEST)
    if "--collaudo" in A:
        sys.path.insert(0, _QUI)
        import _pilota_prova1_braccio as B
        raise SystemExit(0 if B.stampa_collaudo_coerenza() == 4 else 1)
    dati = leggi(semi) if "--solo-referto" in A else lancia(semi, passi, [c for c in cps if c > 0])
    referto(dati, passi, cps)
    io.open(REFERTO, "w", encoding="utf-8", newline=NL).write(NL.join(R) + NL)
    print(NL + "referto in %s" % REFERTO)
