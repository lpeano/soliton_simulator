# -*- coding: utf-8 -*-
"""LA RIGIOCATA `0 -> 120` DEL RAMO B, campionata a OGNI PASSO. L'ORIGINE, non l'escalation.

Criteri FISSATI PRIMA in `doc/TASK_HISTORY/2026-09-20_rigiocata-0-120.md` (`23834ff`).

*** ⚠ IL SIGILLO INTERNO [BLOCCANTE] -- senza, questa rigiocata non vale niente ***
  La rigiocata deve riprodurre **ESATTAMENTE** il ramo B. Se il ciclo differisse di una chiamata da
  quello del driver, la traiettoria **divergerebbe** e si starebbe misurando **un altro run**.
  **CRITERIO: al passo 120 lo stato deve essere IDENTICO a `_ab_B/scena_000120.pkl.gz`**, campo per
  campo, col criterio `uguale_contenuto` dei sigilli. **Se fallisce, il risultato e' BUTTATO e si
  riporta il fallimento invece di pubblicare i numeri.**

*** IL CICLO SI COPIA DAL DRIVER, NON SI REINVENTA ***
  Da `csv/_test_fork/_scena_video.py`:
      passo_test()  una volta per frame
      poi PASSI_PER_FRAME volte:
          scuoti_vuoto(net) ; net.step() ; net.mitosi() ; net.rilassa_disegno() ; net.memoria_hebbiana_moto()
  E l'argv e' quello del ramo B: `--sep 4.0`, tutti i flag, **SENZA `--chi-basc`**.

*** CADENZA: OGNI PASSO, e il perche' e' un numero ***
  Un passo costa ~4 s, la misura ~2 ms (percentili su array gia' in memoria): **lo 0.05 %**.
  Campionare cinque volte piu' fitto **non si vede nel costo**.
  **Tutte le misure sono PURE READ**: si leggono gli attributi. **Nessuna `diagnostica()`**, che scrive.

*** ⚠ NUMERATORE E DENOMINATORE SEPARATI ***
  `d/d0` puo' salire perche' `d` CRESCE o perche' `d0` CALA: **sono due fenomeni diversi**, e si
  stampano **entrambi**, mai solo il rapporto.

*** COSA NON E' RICOSTRUIBILE, e si dichiara ***
  `n1` e `n2` sono locali di `step` (`src`, `beta`): **non ricostruibili da fuori**. Solo **`n3`**.
ASCII PURO.
"""
import os
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, RADICE)
sys.path.insert(0, os.path.join(RADICE, "csv", "_seal_fork"))
os.chdir(RADICE)

CINQUE = [16, 481, 621, 627, 837]
COPPIA = (16, 481)          # l'arco che al 120 e' gia' il piu' teso, e al 240 il peggiore
NPASSI = 120
DT, CS_M = 0.01, 2.0        # dichiarati, per `n3`

# ⚠ L'OPZIONE SI LEGGE PRIMA CHE `sys.argv` VENGA SOVRASCRITTO, e il perche' e' un bug che ho
# GIA' FATTO: qui sotto `sys.argv` viene rimpiazzato con l'argv del SIMULATORE, quindi leggere
# `--traccia` DOPO significa leggerlo da una lista che non lo contiene piu'. Il flag risultava
# SEMPRE False, la rigiocata girava senza traccia, e NIENTE lo segnalava: il sigillo interno
# passava lo stesso, perche' senza traccia la fisica e' identica per costruzione.
TRACCIA = "--traccia" in sys.argv
TRACCIA_VD = "--traccia-vd" in sys.argv

# ---- l'argv del RAMO B, copiato dal driver (senza `--chi-basc`)
sys.argv = ["soliton_simulator.py", "--test", "N-MASSE", "--nmasse", "3", "--sep", "4.0",
            "--giri", "0", "--campo-spinoriale", "--spinore-vivo", "--spinore-corretto",
            "--chi-core", "--calore-scal", "--deparam-orologio", "--verlet", "--fork-su2",
            "--fork-su2-mem", "--cs-dinamico", "--tau-luce", "--rumore-colorato",
            "--pav-com", "--guscio-morbido", "--zeta-vir", "--plast-din",
            "--viriale", "--olon-part"]
import soliton_simulator as S

# [TRACCIA_D0, 2026-09-20] `--traccia` accende la strumentazione dei 19 punti che toccano `d0`.
# ⚠ SI ACCENDE QUI, PRIMA di `avvia_test`, perche' la semina stessa scrive `d0` (`:2083`).
# ⚠ E il SIGILLO INTERNO in fondo diventa il criterio `Z3` del mandato: se la strumentazione
#   avesse toccato il PERCORSO, la rigiocata smetterebbe di riprodurre il ramo B e si vedrebbe li'.
if TRACCIA:
    if not hasattr(S, "TRACCIA_D0"):
        raise SystemExit("questo simulatore non ha TRACCIA_D0")
    S.TRACCIA_D0 = True
    print("TRACCIA_D0 = True   (19 siti strumentati)")
if TRACCIA_VD:
    if not hasattr(S, "TRACCIA_VD"):
        raise SystemExit("questo simulatore non ha TRACCIA_VD")
    S.TRACCIA_VD = True
    print("TRACCIA_VD = True   (i tre termini di `acc`, separati)")

a = S._cli()
S._applica_regime(a)
S._applica_flag(a)
S._NMASSE_VIDEO["n"] = 3
S._NMASSE_VIDEO["sep"] = 4.0
S._NMASSE_VIDEO["size"] = None
print("CHI_BASC dal MODULO (dev'essere False): %s" % S.CHI_BASC)
S.avvia_test("N-MASSE")()
net = S.net
print("semina: n = %d  archi = %d" % (net.n, len(net.i)))
assert net.n == 2391, "n alla semina e' %d, non 2391: NON e' la stessa scena" % net.n


def arco(i0, j0):
    """l'indice dell'arco (i0,j0) CERCATO PER COPPIA DI NODI, non per posizione"""
    ii = np.asarray(net.i); jj = np.asarray(net.j)
    s = ((ii == i0) & (jj == j0)) | ((ii == j0) & (jj == i0))
    k = np.flatnonzero(s)
    return int(k[0]) if len(k) else -1


def rango(v, x):
    return 100.0 * float(np.mean(np.asarray(v) < x))


def misura(passo):
    d = np.asarray(net.d); d0 = np.asarray(net.d0); vd = np.abs(np.asarray(net.vd))
    ii = np.asarray(net.i); jj = np.asarray(net.j)
    m = min(len(d), len(d0), len(vd), len(ii), len(jj))
    d, d0, vd, ii, jj = d[:m], d0[:m], vd[:m], ii[:m], jj[:m]
    rap = d / np.maximum(d0, 1e-12)
    n = net.n
    dg = np.asarray(net._deg)[:n]
    pv = np.abs(np.asarray(net.phivel))[:n]
    k = arco(*COPPIA)
    r = dict(passo=passo, n=n, archi=m,
             # la POPOLAZIONE
             pd50=float(np.median(rap)), pd99=float(np.percentile(rap, 99)), pdmax=float(rap.max()),
             pv50=float(np.median(vd)), pv99=float(np.percentile(vd, 99)), pvmax=float(vd.max()),
             pd0=float(np.median(d0)), pdd=float(np.median(d)),
             n3=float(np.ceil(vd.max() * DT / (0.1 * max(float(np.median(d)), 0.1)))),
             # L'ARCO 16-481: numeratore e denominatore SEPARATI
             k=k, ad=float(d[k]) if k >= 0 else np.nan,
             ad0=float(d0[k]) if k >= 0 else np.nan,
             arap=float(rap[k]) if k >= 0 else np.nan,
             avd=float(vd[k]) if k >= 0 else np.nan)
    for x in CINQUE:
        s = (ii == x) | (jj == x)
        r["deg_%d" % x] = int(dg[x])
        r["pv_%d" % x] = float(pv[x])
        r["pvr_%d" % x] = rango(pv, pv[x])
        r["rap50_%d" % x] = float(np.median(rap[s])) if s.any() else np.nan
        r["rapmax_%d" % x] = float(rap[s].max()) if s.any() else np.nan
        r["vdmax_%d" % x] = float(vd[s].max()) if s.any() else np.nan
    return r


def geometria():
    """par.2 del mandato: i cinque sono i piu' connessi PERCHE' stanno al centro?"""
    n = net.n
    pos = np.asarray(net.pos)[:n]
    dg = np.asarray(net._deg)[:n]
    bar = pos.mean(axis=0)
    r = np.linalg.norm(pos - bar, axis=1)
    print("")
    print("--- par.2  LA GEOMETRIA ALLA SEMINA: `_deg` e' la distanza dal baricentro? ---")
    print("  baricentro = [%.3f %.3f %.3f]   |r| p50 %.4g  p99 %.4g  max %.4g"
          % (bar[0], bar[1], bar[2], np.median(r), np.percentile(r, 99), r.max()))
    cc = float(np.corrcoef(r, dg)[0, 1])
    print("  CORRELAZIONE fra distanza dal baricentro e `_deg`, su tutti i %d nodi: %+.4f" % (n, cc))
    print("  (il NULLO per variabili indipendenti su n=%d e' ~1/sqrt(n) = %.4f; 3 sigma = %.4f)"
          % (n, 1.0 / np.sqrt(n), 3.0 / np.sqrt(n)))
    print("  %-7s %10s %10s %10s %10s" % ("nodo", "|r|", "rango |r|", "_deg", "rango deg"))
    for x in CINQUE:
        print("  %-7d %10.4g %9.1f%% %10d %9.1f%%"
              % (x, r[x], rango(r, r[x]), dg[x], rango(dg, dg[x])))
    # e i nodi PIU connessi in assoluto: dove stanno?
    top = np.argsort(-dg)[:20]
    print("  i 20 nodi PIU' connessi: |r| p50 %.4g (contro %.4g di tutti) -> rango medio %.1f%%"
          % (np.median(r[top]), np.median(r), np.mean([rango(r, r[q]) for q in top])))


def main():
    geometria()
    print("")
    print("--- LA SERIE `0 -> %d`, campionata a OGNI PASSO ---" % NPASSI)
    print("  arco %d-%d: si segue per COPPIA DI NODI. Indice alla semina: %d"
          % (COPPIA[0], COPPIA[1], arco(*COPPIA)))
    print("")
    print("  %-6s %-6s | %9s %9s %9s %9s | %8s %8s %8s | %6s %8s"
          % ("passo", "n", "16-481 d", "16-481 d0", "d/d0", "|vd|",
             "pop d/d0", "pop |vd|", "pop d0", "n3", "pop dmax"))
    S.stato["nframe"] = 0
    _stato_al_salvataggio = {}      # lo stato NEL PUNTO in cui il driver salva, non a fine giro
    serie = [misura(0)]
    r = serie[0]
    print("  %-6d %-6d | %9.4g %9.4g %9.4g %9.4g | %8.4g %8.4g %8.4g | %6.0f %8.4g"
          % (0, r["n"], r["ad"], r["ad0"], r["arap"], r["avd"],
             r["pd50"], r["pv50"], r["pd0"], r["n3"], r["pdmax"]))
    t0 = time.time()
    passo = 0
    for _frame in range(NPASSI // int(S.PASSI_PER_FRAME)):
        S.passo_test()
        for _ in range(int(S.PASSI_PER_FRAME)):
            S.scuoti_vuoto(net); net.step(); net.mitosi()
            net.rilassa_disegno(); net.memoria_hebbiana_moto()
            passo += 1
            # ⚠ `_passo_corrente` NON viene impostato da nessuno nel percorso batch: `_traccia_d0`
            # lo legge con `getattr(..., -1)` e restava SEMPRE `-1`. Il riassunto aggregato non ne
            # risentiva, ma il DETTAGLIO per-arco filtrava su `passo % 10` e `-1 % 10 == 9` in
            # Python: TUTTE le righe venivano saltate, e la tabella usciva VUOTA senza un errore.
            # Lo imposta la rigiocata, che il passo lo sa.
            net._passo_corrente = passo
            r = misura(passo)
            serie.append(r)
            if passo % 5 == 0 or passo <= 3:
                print("  %-6d %-6d | %9.4g %9.4g %9.4g %9.4g | %8.4g %8.4g %8.4g | %6.0f %8.4g"
                      % (passo, r["n"], r["ad"], r["ad0"], r["arap"], r["avd"],
                         r["pd50"], r["pv50"], r["pd0"], r["n3"], r["pdmax"]), flush=True)
        S.stato["nframe"] += 1
        # [CORREZIONE dopo il FALLIMENTO del sigillo, 2026-09-20] IL DRIVER CHIAMA `diagnostica()`
        # PER LA SUA RIGA DI PROGRESSO (`_scena_video.py:277`, `if fr % 5 == 0 or fr == 1`), e
        # `diagnostica()` chiama `self._pesi()`, che incrementa `_g_kernel_alpha_tot` (`:2834`).
        # Saltandola, la mia rigiocata era PIU' PURA del driver -- e il sigillo l'ha PRESO:
        # 136 campi su 137 identici, e l'unico diverso era proprio quel contatore.
        # ⚠ NON HO ALLARGATO IL CRITERIO DOPO AVER VISTO IL RISULTATO: ho corretto il ciclo.
        # E `_db_step` lo scrive il driver quando salva la serie (`fr % SERIE == 0`).
        _fr = _frame + 1
        # ⚠ L'ORDINE E' QUELLO DEL DRIVER, e NON e' indifferente: il blocco che SALVA
        # (`if SERIE and ...`) sta PRIMA del blocco che chiama `diagnostica()`
        # (`if fr % 5 == 0 or fr == 1`). Quindi lo snapshot del passo 120 e' scattato PRIMA
        # della diagnostica del frame 20.
        # MISURATO con una sonda: `diagnostica()` costa **5** chiamate a `_pesi()`
        # (non una), e `salva_stato()` ne costa **0**. Da cui i conti tornano:
        #   riferimento 1554 = fisica 1534 + 4 diagnostiche x5   (frame 1, 5, 10, 15)
        #   prima versione 1559 = fisica 1534 + 5 diagnostiche x5 (avevo contato anche il fr 20)
        # LA FISICA COINCIDE ESATTAMENTE: 1534 = 1534. L'errore era di ORDINE, non di fisica.
        if _fr % 20 == 0:
            net._db_step = _fr * int(S.PASSI_PER_FRAME)
            _stato_al_salvataggio.clear()
            for _k, _v in net.__dict__.items():
                if _k == "rng":
                    continue
                if isinstance(_v, (np.ndarray, int, float, bool, np.integer, np.floating, str)):
                    _stato_al_salvataggio[_k] = _v.copy() if isinstance(_v, np.ndarray) else _v
        if _fr % 5 == 0 or _fr == 1:
            net.diagnostica()
    print("  [%d passi in %.1f s = %.2f s/passo]" % (passo, time.time() - t0,
                                                     (time.time() - t0) / max(passo, 1)))

    # ---- i cinque, ogni 10 passi
    print("")
    print("--- I CINQUE: `_deg`, `phivel` (col rango), e la tensione dei loro archi ---")
    print("  %-6s | %s" % ("passo", " | ".join("%-28s" % ("nodo %d: deg  pv(rango) d/d0max" % x)
                                               for x in CINQUE[:3])))
    for r in serie:
        if r["passo"] % 10:
            continue
        pezzi = []
        for x in CINQUE[:3]:
            pezzi.append("%4d %6.1f(p%4.1f) %7.4g"
                         % (r["deg_%d" % x], r["pv_%d" % x], r["pvr_%d" % x], r["rapmax_%d" % x]))
        print("  %-6d | %s" % (r["passo"], " | ".join(pezzi)))

    # ---- LA TRACCIA: chi ha scritto `d0`, quanto, e chi ha tagliato
    if TRACCIA:
        log = getattr(net, "_traccia_d0_log", [])
        glob = getattr(net, "_g_traccia_d0", {})
        # ⚠ GUARDIA: chiedere la traccia e non ottenerla dev'essere un ERRORE, non un silenzio.
        # Senza questa riga il bug dell'argv sarebbe passato inosservato una seconda volta.
        if not log:
            raise SystemExit("*** --traccia chiesto ma il log e' VUOTO: la traccia NON si e' "
                             "accesa. Non pubblico numeri che non ho. ***")
        print("")
        print("=" * 118)
        print("CHI SCRIVE `d0` -- %d voci su %d siti, in %d passi" % (len(log), len(glob), NPASSI))
        print("=" * 118)
        agg = {}
        for v in log:
            k = v["sito"]
            e = agg.setdefault(k, {"n": 0, "somma": 0.0, "maxass": 0.0, "tocc": 0,
                                   "tagl": 0, "len_cambia": 0})
            e["n"] += 1
            if v.get("tocc", -1) >= 0:
                e["somma"] += v.get("somma", 0.0)
                e["tocc"] += v.get("tocc", 0)
                e["maxass"] = max(e["maxass"], v.get("maxass", 0.0))
            else:
                e["len_cambia"] += 1
            e["tagl"] += v.get("tagliati_tracc", 0)
        print("  %-22s %6s %8s %16s %12s %8s" %
              ("sito", "giri", "tocchi", "SOMMA ALGEBRICA", "max|delta|", "tagliati"))
        for k in sorted(agg, key=lambda x: agg[x]["somma"]):
            e = agg[k]
            print("  %-22s %6d %8d %+16.6e %12.4e %8d%s" %
                  (k, e["n"], e["tocc"], e["somma"], e["maxass"], e["tagl"],
                   "   (len cambia %d volte)" % e["len_cambia"] if e["len_cambia"] else ""))
        mai = [k for k in ("S01_archi_nuovi", "S02_rilass_visco", "S03_diff_guscio",
                           "S04_rilass_TAU_P", "S05_spinta_locale", "S06_mitosi", "S07_schwinger",
                           "S08_proj", "S09_spinta_med", "S10_grav_med", "S11_flusso",
                           "S12_coesione", "P1_dopo_rilass", "P2_dopo_spinta", "P3_dopo_proj",
                           "P4_dopo_grav", "P5_dopo_flusso", "P6_dopo_coesione", "P7_dopo_4917")
               if k not in agg]
        print("  ⚠ SITI MAI SCATTATI in %d passi (A8: un ramo che non gira e' comportamento"
              " sconosciuto): %s" % (NPASSI, mai if mai else "nessuno"))
        # l'arco 16-481, sito per sito, ai passi dei SALTI
        print("")
        print("  L'ARCO 16-481, sito per sito. `prima -> dopo` (e `d` accanto):")
        print("  %-6s %-22s %12s %12s %12s" % ("passo", "sito", "d0 prima", "d0 dopo", "d"))
        _righe_arco = 0
        for v in log:
            t = v.get("16-481")
            if not t or v["passo"] % 10:
                continue
            if t[0] == t[1]:
                continue
            _righe_arco += 1
            print("  %-6d %-22s %12.6f %12.6f %12.6f" % (v["passo"], v["sito"], t[0], t[1], t[2]))
        if not _righe_arco:
            raise SystemExit("*** la tabella per-arco e' VUOTA: o il passo non e' registrato, o "
                             "l'arco non e' stato trovato. Non pubblico una tabella vuota. ***")

    # ---- par.4: `coesione_relazionale` PRIMA del clip. IL CLIP PROTEGGE O PRODUCE?
    if TRACCIA:
        cl = getattr(net, "_traccia_coes_log", [])
        if not cl:
            raise SystemExit("*** il log della coesione e' VUOTO. Non pubblico numeri che non ho. ***")
        print("")
        print("=" * 118)
        print("par.4  `coesione_relazionale` PRIMA DEL CLIP -- il clip PROTEGGE o PRODUCE?")
        print("=" * 118)
        print("  criterio, fissato prima:  |coes| >> tetto -> il clip PROTEGGE, il difetto e' nel")
        print("  TERMINE;  |coes| ~ tetto -> il clip PRODUCE il movimento, e il tetto e' la cura.")
        print("")
        print("  %-6s %9s %9s %11s %11s %11s | %s" %
              ("passo", "archi", "saturi", "|c|/t p50", "|c|/t p99", "|c|/t max", "arco 16-481: coes / tetto"))
        for v in cl:
            if v["passo"] % 10:
                continue
            t = v.get("16-481")
            det = ("%12.6g / %-10.6g  rap %.4g" % (t[0], t[1], abs(t[0]) / max(abs(t[1]), 1e-300))
                   ) if t else "(arco assente)"
            print("  %-6d %9d %9d %11.4g %11.4g %11.4g | %s" %
                  (v["passo"], v["n_archi"], v["sat"], v["rap_p50"], v["rap_p99"], v["rap_max"], det))
        tot = sum(v["n_archi"] for v in cl); sat = sum(v["sat"] for v in cl)
        print("")
        print("  SATURI su TUTTI i campioni: %d su %d = %.2f %%" % (sat, tot, 100.0 * sat / max(tot, 1)))

    # ---- CHI SPINGE `d`: i tre termini di `acc`, separati
    if TRACCIA_VD:
        vl = getattr(net, "_traccia_vd_log", [])
        if not vl:
            raise SystemExit("*** --traccia-vd chiesto ma il log e' VUOTO. Non pubblico numeri "
                             "che non ho. ***")
        print("")
        print("=" * 124)
        print("CHI SPINGE `d` -- i TRE termini di `acc = cs^2*lap + src - beta*vd`, SEPARATI e col SEGNO")
        print("=" * 124)
        print("  RIASSUNTO sugli archi dei cinque nodi (mediane col segno, e massimi in valore assoluto)")
        print("  %-6s %12s %12s %12s | %11s %11s %11s" %
              ("passo", "cs2*lap p50", "src p50", "-beta*vd p50",
               "|cs2lap|max", "|src|max", "|betavd|max"))
        for v in vl:
            if v["passo"] % 10:
                continue
            print("  %-6d %12.4e %12.4e %12.4e | %11.4e %11.4e %11.4e" %
                  (v["passo"], v["lap_p50"], v["src_p50"], v["bet_p50"],
                   v["lap_max"], v["src_max"], v["bet_max"]))
        print("")
        print("  DETTAGLIO sull'arco 16-481 (cercato per COPPIA DI NODI):")
        print("  %-6s %12s %12s %12s | %9s %9s %9s %9s" %
              ("passo", "cs2*lap", "src", "-beta*vd", "d", "d0", "vd", "beta"))
        _n = 0
        for v in vl:
            t = v.get("16-481")
            if not t or v["passo"] % 10:
                continue
            _n += 1
            print("  %-6d %12.4e %12.4e %12.4e | %9.4g %9.4g %9.4g %9.4g" %
                  (v["passo"], t[0], t[1], t[2], t[3], t[4], t[5], t[6]))
        if not _n:
            raise SystemExit("*** la tabella per-arco e' VUOTA. Non pubblico una tabella vuota. ***")
        # CHI DOMINA, contato invece che guardato a occhio
        vinc = {"cs2*lap": 0, "src": 0, "-beta*vd": 0}
        for v in vl:
            t = v.get("16-481")
            if not t:
                continue
            a = [abs(t[0]), abs(t[1]), abs(t[2])]
            vinc[["cs2*lap", "src", "-beta*vd"][a.index(max(a))]] += 1
        tot = sum(vinc.values())
        print("")
        print("  CHI DOMINA sull'arco, passo per passo (su %d passi): %s" % (tot, vinc))

    # ---- IL SIGILLO INTERNO [BLOCCANTE]  (= `Z3` del mandato quando TRACCIA e' acceso)
    print("")
    print("=" * 118)
    print("SIGILLO INTERNO [BLOCCANTE]: la rigiocata riproduce il ramo B?")
    print("=" * 118)
    import gzip, pickle
    from _sigillo_archivio import uguale_contenuto
    with gzip.open("csv/_test_fork/_ab_B/scena_000120.pkl.gz", "rb") as f:
        rif = pickle.load(f)["attrs"]
    # ⚠ SI CONFRONTA LO STATO AL PUNTO DI SALVATAGGIO, non quello a fine funzione:
    # il driver scatta lo snapshot PRIMA della `diagnostica()` del frame 20.
    mio = _stato_al_salvataggio
    print("  (stato catturato nel punto in cui il driver chiama `salva_stato`, %d campi)" % len(mio))
    com = sorted(set(rif) & set(mio))
    diff = [kk for kk in com if not uguale_contenuto(rif[kk], mio[kk])]
    # ⚠ L'INTERSEZIONE NASCONDE LE ASSENZE: un campo che sta solo da una parte non viene
    # confrontato e non comparirebbe fra i "diversi". Si stampa, se no lo zero mente.
    solo_rif = sorted(set(rif) - set(mio))
    solo_mio = sorted(set(mio) - set(rif))
    print("  campi confrontati: %d   DIVERSI: %d" % (len(com), len(diff)))
    print("  solo nel RIFERIMENTO: %d %s   |   solo nella RIGIOCATA: %d %s"
          % (len(solo_rif), solo_rif[:5], len(solo_mio), solo_mio[:5]))
    if diff:
        print("  *** FALLITO. Primi diversi: %s ***" % diff[:8])
        # ⚠ SENZA I VALORI, un FAIL non dice NIENTE su cosa correggere: si stampano.
        for kk in diff[:10]:
            va, vb = rif[kk], mio[kk]
            if np.isscalar(va) or isinstance(va, (int, float, np.integer, np.floating)):
                print("      %-28s riferimento %-14s rigiocata %-14s  delta %s"
                      % (kk, va, vb, (vb - va) if isinstance(va, (int, float,
                         np.integer, np.floating)) else "n/d"))
            else:
                print("      %-28s (array) shape %s contro %s"
                      % (kk, getattr(va, "shape", None), getattr(vb, "shape", None)))
        print("  *** LA RIGIOCATA NON RIPRODUCE IL RAMO B: i numeri qui sopra NON VALGONO. ***")
        return 1
    print("  PASS -- %d campi IDENTICI. La rigiocata E' il ramo B, e la serie vale." % len(com))
    print("  (e lo zero non e' mancanza di confronto: %d campi confrontati, n=%d in entrambi)"
          % (len(com), net.n))
    return 0


if __name__ == "__main__":
    sys.exit(main())
