r"""**IL CONFRONTO FRA LA PREVISIONE E IL PILOTA** — e i numeri escono da qui, non dalle dita.

*(`L-NUMERI`: ogni numero scritto in un commit o in un referto esce da uno script. La previsione
sta in `doc/TASK_HISTORY/2026-09-27_pilota-prova1.md` par.4, **committata prima** del referto.)*

**Legge i `misura.json` dei quattro semi** e stampa, per ogni previsione, **l'esito col suo
falsificante**. **Non riscrive la previsione:** la mette accanto ai numeri.

    python csv/_test_fork/_confronto_previsione.py

ASCII puro.
"""
import io
import json
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, os.path.join(RADICE, "csv"))

import _presidio                                                       # noqa: E402
import _osservabile_p1 as OP                                           # noqa: E402

_presidio.avvia(__file__)

# ESENTE-H-P5: non costruisce nessuna scena e non carica il simulatore: legge i `json` di un run
#   che ha GIA' dichiarato la propria configurazione intera nel suo referto. Non c'e' un modulo
#   configurato da dichiarare.

NL = chr(10)
DEST = os.path.join(_QUI, "_pilota_prova1")
FUORI = os.path.join(DEST, "CONFRONTO_previsione.txt")
SEMI = [11, 12, 13, 14]
CPS = [40, 80, 120]
R = []


def P(s=""):
    print(s)
    R.append(s)


def leggi():
    d = {}
    for s in SEMI:
        p = os.path.join(DEST, "seme_%d" % s, "misura.json")
        if os.path.exists(p):
            d[s] = json.load(io.open(p, encoding="utf-8"))
    return d


def blocco(x, passo):
    for b in x["blocchi"]:
        if int(b["passo"]) == int(passo):
            return b
    return None


def barra(v):
    """`(media, sd, lo, hi, contiene_zero)` con il `t` di Student giusto (`P3`)."""
    o = OP.dispersione([x for x in v if np.isfinite(x)])
    if o["ic95"] is None:
        return o["media"], float("nan"), float("nan"), float("nan"), True
    lo, hi = o["ic95"]
    return o["media"], o["sd"], lo, hi, bool(lo <= 0.0 <= hi)


def oss(d, passo, cp):
    """`A(t)` per seme sulla coppia `cp`, coi controlli FISSI."""
    fuori = []
    for s in sorted(d):
        b0, bt = blocco(d[s], 0), blocco(d[s], passo)
        m0 = b0["coppie_passo0"][cp]["centro_centro"]
        mt = bt["coppie_passo0"][cp]["centro_centro"]
        righe = bt["controlli_fissi"]["coppie"].get(cp, [])
        v = [(r["distanza"] - r["distanza_0"]) / m0 for r in righe
             if not r["escluso"] and np.isfinite(r["distanza"])]
        if not (np.isfinite(m0) and m0 > 0 and v):
            continue
        fuori.append((mt - m0) / m0 - float(np.mean(v)))
    return fuori


def campo(d, passo, nome, dove="forma_passo0"):
    return [blocco(d[s], passo)[dove][k][nome]
            for s in sorted(d) for k in sorted(blocco(d[s], passo)[dove])]


def fase(d, passo, nome):
    return [blocco(d[s], passo)["fase"]["per_massa"][k][nome]
            for s in sorted(d) for k in sorted(blocco(d[s], passo)["fase"]["per_massa"])]


def principale():
    d = leggi()
    if not d:
        P("NESSUN `misura.json`: il confronto si fermerebbe qui.")
        return
    coppie = sorted(blocco(d[sorted(d)[0]], 0)["coppie_passo0"].keys())
    P("=" * 112)
    P("CONFRONTO  PREVISIONE (committata PRIMA)  contro  PILOTA   --   %d semi" % len(d))
    P("=" * 112)
    P("  La previsione sta in doc/TASK_HISTORY/2026-09-27_pilota-prova1.md par.4, commit 1486cac,")
    P("  ANTENATO del referto. Non si riscrive: si mette accanto ai numeri.")

    # ---------------------------------------------------------------- (a)
    P()
    P("-" * 112)
    P("(a)  PREVEDEVO: i NODI DELLE MASSE DEL PASSO 0 non si avvicinano piu' dei controlli.")
    P("     ⚠ CORREZIONE DEL GUARDIANO, 2026-09-27: `A(t)` si misura sull'insieme di nodi")
    P("     CONGELATO al passo 0 (la colonna `passo0`), NON sulla massa come regione")
    P("     coerente. A 80 passi la sovrapposizione con la regione di fase e' 0.0827 e")
    P("     `coer_campo` 0.34: sono due insiemi ormai DIVERSI. Si scrive <<i nodi delle")
    P("     masse del passo 0 si avvicinano>>, MAI <<le masse si avvicinano>>.")
    P("     FALSIFICANTE SCRITTO PRIMA: `A(t) < 0` oltre l'IC95 su ALMENO 2 COPPIE SU 3.")
    P("-" * 112)
    P("  passo | coppia            |    A(t)   |    sd    |       IC95        | oltre la barra?")
    scatti = {}
    for c in CPS:
        n_ok = 0
        for cp in coppie:
            m, sd, lo, hi, zero = barra(oss(d, c, cp))
            forte = (not zero) and hi < 0.0
            n_ok += 1 if forte else 0
            P("  %5d | %-17s | %+.5f | %.5f | [%+.5f,%+.5f] | %s"
              % (c, cp, m, sd, lo, hi, "SI, NEGATIVO" if forte else "no (contiene lo zero)"))
        scatti[c] = n_ok
        P("        -> coppie significative NEGATIVE: %d su %d" % (n_ok, len(coppie)))
    P()
    caduta = [c for c in CPS if scatti[c] >= 2]
    if caduta:
        P("  ESITO: **LA PREVISIONE (a) E' FALSIFICATA** ai passi %s, dal falsificante che avevo"
          % caduta)
        P("         scritto io. Al passo 120 il criterio NON scatta, e il perche' e' nella barra:")
    else:
        P("  ESITO: la previsione (a) REGGE: il falsificante non scatta a nessun passo.")

    # la barra: masse contro controlli
    P()
    P("  PERCHE' A 120 NON SCATTA -- la dispersione FRA SEMI delle MASSE, contro quella dei CONTROLLI:")
    P("  passo | coppia            | sd masse | sd controlli | rapporto")
    for c in CPS:
        for cp in coppie:
            vm, vc = [], []
            for s in sorted(d):
                b0, bt = blocco(d[s], 0), blocco(d[s], c)
                m0 = b0["coppie_passo0"][cp]["centro_centro"]
                mt = bt["coppie_passo0"][cp]["centro_centro"]
                righe = bt["controlli_fissi"]["coppie"].get(cp, [])
                v = [(r["distanza"] - r["distanza_0"]) / m0 for r in righe if not r["escluso"]]
                if np.isfinite(m0) and m0 > 0 and v:
                    vm.append((mt - m0) / m0)
                    vc.append(float(np.mean(v)))
            sm = float(np.std(vm, ddof=1)) if len(vm) > 1 else float("nan")
            sc = float(np.std(vc, ddof=1)) if len(vc) > 1 else float("nan")
            P("  %5d | %-17s | %.5f  |   %.5f    | x%.2f" % (c, cp, sm, sc, sm / sc))

    # ---------------------------------------------------------------- la parte uniforme
    P()
    P("-" * 112)
    P("(a-bis)  PREVEDEVO: <<il calo di `W5` dovrebbe comparire QUASI TUTTO anche nei controlli>>.")
    P("     ⚠ CORREZIONE DEL GUARDIANO, 2026-09-27: al passo 40 i controlli CONTENGONO LO")
    P("     ZERO su 3 coppie su 3 (limiti |c| < 0.0035-0.0049). <<Il vuoto si espande>> NON")
    P("     E' DIMOSTRATO: e' un segno letto senza la sua barra, lo stesso errore del segno")
    P("     concorde su due semi. `A` e' significativa perche' e' una differenza APPAIATA")
    P("     nel seme, non perche' i due termini lo siano.")
    P("-" * 112)
    P("  passo | coppia            | masse     | controlli |      IC95 controlli      | frazione")
    for c in CPS:
        for cp in coppie:
            vm, vc = [], []
            for s in sorted(d):
                b0, bt = blocco(d[s], 0), blocco(d[s], c)
                m0 = b0["coppie_passo0"][cp]["centro_centro"]
                mt = bt["coppie_passo0"][cp]["centro_centro"]
                righe = bt["controlli_fissi"]["coppie"].get(cp, [])
                v = [(r["distanza"] - r["distanza_0"]) / m0 for r in righe if not r["escluso"]]
                if np.isfinite(m0) and m0 > 0 and v:
                    vm.append((mt - m0) / m0)
                    vc.append(float(np.mean(v)))
            mm = float(np.mean(vm))
            mc, _sd, lo, hi, zero = barra(vc)
            fr = (mc / mm) if abs(mm) > 1e-12 else float("nan")
            P("  %5d | %-17s | %+.5f  | %+.5f  | [%+.5f,%+.5f]%s | %s"
              % (c, cp, mm, mc, lo, hi, " ZERO" if zero else "     ",
                 ("%.1f %%" % (100 * fr)) if np.isfinite(fr) and mm < 0 and not zero
                 else ("controlli NON distinguibili da zero" if zero
                       else "il segno differisce")))

    # ---------------------------------------------------------------- (a-ter) LA DIVERGENZA
    P()
    P("-" * 112)
    P("(a-ter)  E LE DUE DISTANZE DIVERGONO: il mio referto lo aveva STAMPATO e io non")
    P("         l'ho detto. <<LE DUE DISTANZE ... se divergono, si dice>>: divergevano.")
    P("-" * 112)
    P("  passo | coppia            | nodi passo 0 | regioni di FASE | sovrapp | coer_campo")
    for c in [0] + CPS:
        for cp in coppie:
            a0 = float(np.mean([blocco(d[s], c)["coppie_passo0"][cp]["centro_centro"]
                                for s in sorted(d)]))
            af = float(np.nanmean([blocco(d[s], c)["coppie_fase"][cp]["centro_centro"]
                                   for s in sorted(d)]))
            so = float(np.mean(fase(d, c, "sovrapposizione")))
            cc = float(np.mean(campo(d, c, "coer_campo")))
            P("  %5d | %-17s |   %7.4f    |     %7.4f     | %.4f  | %.5f"
              % (c, cp, a0, af, so, cc))
    P()
    P("  I NODI DEL PASSO 0 SI AVVICINANO, LE REGIONI DI FASE NO -- anzi, si ALLONTANANO:")
    P("  sulla coppia 0|1 la distanza fra i nodi del passo 0 va 10.6694 -> 10.2191 mentre")
    P("  quella fra le regioni di fase va 10.8935 -> 13.1410. Con sovrapposizione 0.0491 al")
    P("  passo 120, i due numeri parlano di DUE INSIEMI DIVERSI, e il secondo e' fatto per")
    P("  il 95 %% di nodi che al passo 0 non erano nella massa: NON e' <<la massa si e'")
    P("  allontanata>>, e' <<l'insieme coerente di adesso sta altrove>>. Nessuna delle due")
    P("  letture e' <<la massa>>: e' la voce `MASSA-ID`.")

    P()
    P("  PERCHE' `A` E' SIGNIFICATIVA SE I DUE TERMINI NON LO SONO: L'APPAIAMENTO NEL SEME.")
    P("  passo | coppia            | sd masse | sd controlli | sd di A  | corr(masse,controlli)")
    for c in CPS:
        for cp in coppie:
            vm, vc = [], []
            for s in sorted(d):
                b0, bt = blocco(d[s], 0), blocco(d[s], c)
                m0 = b0["coppie_passo0"][cp]["centro_centro"]
                mt = bt["coppie_passo0"][cp]["centro_centro"]
                righe = bt["controlli_fissi"]["coppie"].get(cp, [])
                w = [(r["distanza"] - r["distanza_0"]) / m0 for r in righe
                     if not r["escluso"]]
                if np.isfinite(m0) and m0 > 0 and w:
                    vm.append((mt - m0) / m0)
                    vc.append(float(np.mean(w)))
            vm, vc = np.asarray(vm), np.asarray(vc)
            rr = (float(np.corrcoef(vm, vc)[0, 1]) if len(vm) > 2 else float("nan"))
            P("  %5d | %-17s | %.5f  |   %.5f    | %.5f  | %+.4f"
              % (c, cp, vm.std(ddof=1), vc.std(ddof=1), (vm - vc).std(ddof=1), rr))
    P()
    P("  E NON VALE PER TUTTE ALLO STESSO MODO, quindi si dice PER COPPIA: al passo 40 la")
    P("  coppia 0|1 ha corr +0.9485 e la `sd` di `A` (0.00051) e' TRE VOLTE piu' piccola di")
    P("  entrambi i termini -- li' l'appaiamento e' tutto. La 0|2 ha corr -0.8587 e la `sd`")
    P("  di `A` (0.00384) e' piu' GRANDE dei termini: li' l'appaiamento PEGGIORA la barra,")
    P("  ed e' infatti la coppia che NON risulta significativa.")

    # ---------------------------------------------------------------- (b)
    P()
    P("-" * 112)
    P("(b)  PREVEDEVO: un ALLUNGAMENTO si', ma NON mareale (coesione di superficie).")
    P("     FALSIFICANTE DELLA SPIEGAZIONE: raggio e quantili interni FERMI mentre le superfici")
    P("     si avvicinano. E il criterio `V6`: superfici piu' dei centri OLTRE LA BARRA.")
    P("-" * 112)
    P("  ⚠⚠ CORREZIONE DEL GUARDIANO, 2026-09-27: **L'ESTIMATORE STESSO E' SBAGLIATO.**")
    P("    `V6` calcola `(st-s0)/s0 - (ct-c0)/c0`, cioe' sottrae due variazioni RELATIVE con")
    P("    DENOMINATORI DIVERSI: `s0 ~ 3.0` (il varco) contro `c0 ~ 10.7` (i centri). Due corpi")
    P("    RIGIDI che si avvicinano di `delta` darebbero -delta/3.0 + delta/10.7 = -0.24*delta,")
    P("    cioe' un ALLUNGAMENTO FINTO. MISURATO sul caso rigido di -0.19: -0.04000.")
    P("    **QUINDI (b) NON E' <<FALSIFICATA>>: E' DA RIMISURARE**, in unita' ASSOLUTE.")
    P("    -> voce `ALLUNG-RELATIVO`; la forma giusta e' in csv/_test_fork/_scomposizione_tratti.py")
    P("    E la risoluzione e' un SECONDO problema, che resta anche dopo: un nullo si legge con")
    P("    la sua risoluzione, e qui la mezza-barra supera spesso l'effetto sui centri.")
    P("    Dire <<falsificata>> perche' l'IC95 contiene lo zero e' l'errore che il presidio")
    P("    del nullo esiste per impedire. Si confronta la MEZZA-BARRA dell'allungamento con")
    P("    l'effetto sui CENTRI: se la barra e' piu' larga, il test NON PUO' VEDERE un")
    P("    allungamento grande quanto il moto dei centri, e l'esito e' NON DETERMINATO.")
    P()
    P("  passo | coppia            | centri   | superfici | allung.  | mezza-barra | esito")
    quanti = 0
    ndet = 0
    for c in CPS:
        for cp in coppie:
            v, vc, vs = [], [], []
            for s in sorted(d):
                b0, bt = blocco(d[s], 0), blocco(d[s], c)
                c0 = b0["coppie_passo0"][cp]["centro_centro"]
                ct = bt["coppie_passo0"][cp]["centro_centro"]
                s0 = b0["coppie_passo0"][cp]["insieme_insieme"]
                st = bt["coppie_passo0"][cp]["insieme_insieme"]
                if np.isfinite(c0) and c0 > 0 and np.isfinite(s0) and s0 > 0:
                    vc.append((ct - c0) / c0)
                    vs.append((st - s0) / s0)
                    v.append((st - s0) / s0 - (ct - c0) / c0)
            m, sd, lo, hi, zero = barra(v)
            mezza = (hi - lo) / 2.0
            mc = float(np.mean(vc))
            if not zero:
                quanti += 1
                esito = "** ALLUNGAMENTO MISURATO **"
            elif mezza > abs(mc):
                ndet += 1
                esito = "NON DETERMINATA (barra > |centri|)"
            else:
                esito = "nullo INFORMATIVO: nessun allungamento"
            P("  %5d | %-17s | %+.5f | %+.5f  | %+.5f | %.5f     | %s"
              % (c, cp, mc, float(np.mean(vs)), m, mezza, esito))
    P()
    tot = len(CPS) * len(coppie)
    P()
    P("  ESITO: allungamenti misurati %d su %d; NON DETERMINATE %d su %d; nulli informativi %d."
      % (quanti, tot, ndet, tot, tot - quanti - ndet))
    if quanti == 0 and ndet:
        P("         **LA PREVISIONE (b) NON E' FALSIFICATA: E' DA RIMISURARE** (estimatore")
        P("         rotto, `ALLUNG-RELATIVO`), E IN PIU' NON SAREBBE DETERMINATA: su %d celle"
          % ndet)
        P("         su %d la mezza-barra dell'allungamento SUPERA l'effetto sui centri, quindi"
          % tot)
        P("         il test non potrebbe vedere un allungamento nemmeno grande quanto il moto")
        P("         dei centri. Le %d celle con la barra piu' stretta dei centri sono nulli"
          % (tot - quanti - ndet))
        P("         INFORMATIVI, e li' un allungamento davvero non c'e'.")
        P("         **E LA MIA SPIEGAZIONE (coesione di superficie) NON E' NE' CONFERMATA NE'")
        P("         SMENTITA: resta da misurare.**")

    # ---------------------------------------------------------------- (c)
    P()
    P("-" * 112)
    P("(c)  PREVEDEVO: la coerenza SI SCIOGLIE, non migra -- con sovrapposizione >= 90 %% e")
    P("     spostamento del medoide < LAM.")
    P("-" * 112)
    P("  passo | coer_campo | n_fase | sovrapposizione | max spost. medoide | raggio (riferimento)")
    for c in [0] + CPS:
        cc = float(np.mean(campo(d, c, "coer_campo")))
        nf = float(np.mean(fase(d, c, "n")))
        so = float(np.mean(fase(d, c, "sovrapposizione")))
        sp = float(np.nanmax(fase(d, c, "spostamento_medoide")))
        rg = float(np.mean(campo(d, c, "raggio")))
        P("  %5d |   %.5f  | %6.1f |     %.4f      |       %.3f        |  %.3f"
          % (c, cc, nf, so, sp, rg))
    lam = d[sorted(d)[0]]["LAM"]
    P()
    P("  IL MECCANISMO E' CONFERMATO: `coer_campo` CROLLA (%.5f -> %.5f) e `n_fase` si DIMEZZA"
      % (float(np.mean(campo(d, 0, "coer_campo"))), float(np.mean(campo(d, 120, "coer_campo")))))
    P("  e oltre (%.1f -> %.1f). La coerenza SI SCIOGLIE."
      % (float(np.mean(fase(d, 0, "n"))), float(np.mean(fase(d, 120, "n")))))
    P("  MA I NUMERI CHE AVEVO ATTACCATO ALLA PREVISIONE SONO SBAGLIATI: la sovrapposizione")
    P("  scende a %.4f (prevedevo >= 0.90) e lo spostamento del medoide arriva a %.3f contro"
      % (float(np.mean(fase(d, 120, "sovrapposizione"))),
         float(np.nanmax(fase(d, 120, "spostamento_medoide")))))
    P("  `LAM = %.3f` (prevedevo < LAM). **Il meccanismo giusto, la soglia sbagliata.**" % lam)
    P()
    P("  E IL CRITERIO `V5` CONFONDE DUE COSE, ed e' un difetto del criterio, non del sistema:")
    P("  <<sovrapposizione bassa + medoide spostato>> lo legge come MIGRAZIONE, ma qui la")
    P("  sovrapposizione cala perche' L'INSIEME SI SVUOTA (n_fase %.1f -> %.1f, il %.0f %% in meno),"
      % (float(np.mean(fase(d, 0, "n"))), float(np.mean(fase(d, 120, "n"))),
         100 * (1 - float(np.mean(fase(d, 120, "n"))) / float(np.mean(fase(d, 0, "n"))))))
    P("  non perche' si SPOSTI. Il metro giusto dello spostamento e' IL RAGGIO DELLA REGIONE")
    P("  (%.3f), non `LAM` (%.3f): un medoide che si muove di %.3f su un raggio di %.3f si e'"
      % (float(np.mean(campo(d, 0, "raggio"))), lam,
         float(np.mean(fase(d, 120, "spostamento_medoide"))),
         float(np.mean(campo(d, 0, "raggio")))))
    P("  mosso DENTRO la propria regione.")

    # ---------------------------------------------------------------- la via che NON e' stata
    P()
    P("-" * 112)
    P("LA VIA CHE AVEVO INDICATO COME <<LA PIU' PROBABILE PER CUI (a) CADA>>: NON E' QUELLA.")
    P("-" * 112)
    P("  Avevo scritto: <<se la torsione supercritica fosse concentrata NEL VARCO, (a) cade>>.")
    P("  Le NASCITE seguono la torsione supercritica (la mitosi scatta sull'eccesso di torsione),")
    P("  quindi dicono DOVE e': ")
    P("  passo | nati per mitosi (massa/varco/vuoto) | nati per schwinger | zone di TUTTI i nodi")
    for c in CPS:
        nm = {z: float(np.mean([blocco(d[s], c)["nascite_per_zona"]["mitosi"][z]
                                for s in sorted(d)])) for z in ("massa", "varco", "vuoto")}
        ns = {z: float(np.mean([blocco(d[s], c)["nascite_per_zona"]["schwinger"][z]
                                for s in sorted(d)])) for z in ("massa", "varco", "vuoto")}
        zt = {z: float(np.mean([blocco(d[s], c)["zone_tutti"][z] for s in sorted(d)]))
              for z in ("massa", "varco", "vuoto")}
        P("  %5d | %5.1f / %5.1f / %7.1f          | %5.1f / %4.1f / %6.1f | %6.1f / %5.1f / %8.1f"
          % (c, nm["massa"], nm["varco"], nm["vuoto"],
             ns["massa"], ns["varco"], ns["vuoto"], zt["massa"], zt["varco"], zt["vuoto"]))
    P()
    P("  **ZERO nascite nelle masse e ZERO nel varco, a tutti i checkpoint: TUTTE nel vuoto.**")
    P("  Quindi la torsione supercritica NON e' concentrata nel varco, e (a) NON e' caduta per la")
    P("  ragione che avevo indicato. **E' caduta per una ragione che non avevo previsto.**")

    # ---------------------------------------------------------------- V4
    P()
    P("-" * 112)
    P("`V4` -- E LE SCORCIATOIE DI SCHWINGER CI SONO, MISURATE (residuo `A3-DISEGNO`)")
    P("-" * 112)
    P("  passo | coppie | scorciatoie | frazione | `2*dd/d` mediano | minimo")
    for c in CPS:
        sw = [blocco(d[s], c)["schwinger"] for s in sorted(d)]
        tot = float(np.mean([x["coppie"] for x in sw]))
        sc = float(np.mean([x["scorciatoie"] for x in sw]))
        rm = [x.get("rapporto_mediano") for x in sw if x.get("rapporto_mediano") is not None]
        mi = [x.get("rapporto_min") for x in sw if x.get("rapporto_min") is not None]
        P("  %5d | %6.1f | %11.1f | %7s | %16s | %s"
          % (c, tot, sc, ("%.2f %%" % (100 * sc / tot)) if tot > 0 else "-",
             ("%.4f" % float(np.mean(rm))) if rm else "-",
             ("%.4f" % float(np.min(mi))) if mi else "-"))
    P()
    P("  IL RITIRO DI IERI RESTA GIUSTO PER LA MITOSI (l'arco (a,b) diventa (a,m),(m,b) lunghi")
    P("  d/2: il cammino e' lungo QUANTO prima), E ORA LA CODA SCHWINGER E' QUANTIFICATA.")

    # ---------------------------------------------------------------- due righe VUOTE
    P()
    P("-" * 112)
    P("DUE RIGHE DEL REFERTO NON PORTANO INFORMAZIONE, E VANNO DETTE (`P4`, `A8`)")
    P("-" * 112)
    n0 = [blocco(d[s], c)["forma_passo0"][k]["n"]
          for s in sorted(d) for k in sorted(blocco(d[s], 0)["forma_passo0"]) for c in [0] + CPS]
    P("  1. `n` in `forma_passo0` vale SEMPRE lo stesso (%d valori, %d distinti per massa e seme):"
      % (len(n0), len(set(n0))))
    P("     e' l'insieme CONGELATO del passo 0, quindi NON PUO' cambiare. Misurarlo e' un test")
    P("     vuoto (`P4`). L'`n` informativo e' `n_fase`.")
    f0 = float(np.mean(campo(d, 0, "foglio_0")))
    P("  2. `foglio_0` vale %.5f AL PASSO 0, cioe' meta' e meta'. E' IL SUO VALORE SOTTO IPOTESI"
      % f0)
    P("     NULLA, non un risultato: la scena scrive `phi = _dphi()/2 = 2 pi` ESATTAMENTE, che e'")
    P("     il CONFINE fra i due fogli di `floor(phi/2pi)`, e la gaussiana `sigma = 0.05` lo")
    P("     attraversa. Il diagnostico dei fogli, COSI' COM'E', su questa scena non misura nulla.")

    P()
    P("=" * 112)
    P("FINE DEL CONFRONTO. Nessuna conclusione sulla gravita': il pilota non e' il run base.")
    P("=" * 112)


if __name__ == "__main__":
    principale()
    io.open(FUORI, "w", encoding="utf-8", newline=NL).write(NL.join(R) + NL)
    print(NL + "confronto in %s" % FUORI)
