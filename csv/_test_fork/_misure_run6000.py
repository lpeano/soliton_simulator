# -*- coding: utf-8 -*-
"""LE MISURE DEL RUN A 6000 PASSI -- i cinque blocchi del par.3 del mandato.

LEGGE l'archivio, non gira niente. E' il punto dell'archivio: molte misure diverse sugli STESSI
.pkl, senza rigirare. (Z50 e Z51 sono state fatte cosi'.)

I CINQUE BLOCCHI
  1. Z9-b  median(ramp[i]*ramp[j]) sugli archi INTERNI ALLA COORTE ORIGINALE, a ogni snapshot.
           E' IL CRITERIO DI CHIUSURA DI Z9, e PUO' FALLIRE: se `r` scendesse al pavimento il
           numero smetterebbe di crescere e il criterio resterebbe aperto per sempre.
  2. ramp per coorte: percentili, fr(ramp > 0.5) e fr(ramp > 0.9). A 2400 passi: 0.3768 e ZERO.
  3. p95/p05 di ramp[i]*ramp[j]: si STRINGE col maturare? (partiva da 2.31, a 2400 era 8.56)
  4. LE CONSEGUENZE, che il registro dichiara MAI MISURATE: base, psi, rho_spin, cs.
  5. IL CICLO oltre dove Z49 si fermava, in unita' COMOVENTI.

*** TRE PRESIDI CABLATI, non raccomandati ***
(a) LA COORTE ORIGINALE E' ANAGRAFICA, e l'indice E' l'ordine di nascita: i nodi si appendono in
    coda (:3958, verificato in Z9/Z46). N0 = n del PRIMO snapshot, STAMPATO. Non e' la coorte "per
    massa": `masse_info` e `conc_archi` sono VUOTI negli snapshot (misurato), quindi quella
    domanda NON si puo' porre qui, e non la spaccio per la stessa.
(b) LE SOGLIE NON DEVONO FARE LAVORO: dove ne serve una (la regione interna del ciclo) si riporta
    la curva per PIU' soglie. Se il risultato cambia con la soglia, e' la soglia a parlare, e va
    detto invece di scegliere quella che piace.
(c) `_r_corrente` ha DUE ELEMENTI IN MENO di `eta` (2849 contro 2851, misurato): e' scritto prima
    dell'ultima mitosi. Si tronca al minimo e SI DICHIARA quante volte -- un troncamento silenzioso
    e' un ramo silenzioso (A8).

*** E CIO' CHE QUESTO SCRIPT NON FA ***
Nessuna identificazione (bounce, oscillone, protone, confinamento): i NUMERI e la FORMA.
UN SEME, UNA SCENA. E ogni numero eredita `--tau-luce`, il cui sigillo e' 6/7.
ASCII PURO.
"""
import glob
import gzip
import os
import pickle
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
import _presidio

_presidio.avvia(__file__)

DEST = sys.argv[1] if len(sys.argv) > 1 else os.path.join("csv", "_test_fork", "_g6000")
FRAZ_INTERNA = (0.3, 0.4, 0.5, 0.6)      # piu' soglie, di proposito: vedi il presidio (b)
_tronca = [0]


def carica(p):
    ap = gzip.open if p.endswith(".gz") else open
    with ap(p, "rb") as f:
        return pickle.load(f)


def ramp_di(at, TAU_A):
    """ramp = min(1, eta/TAU_A). LA LEGGE E' DEL CODICE (:2649), non una definizione mia."""
    return np.minimum(1.0, np.asarray(at["eta"], float) / TAU_A)


def q(x, p):
    return float(np.percentile(x, p)) if len(x) else float("nan")


def main():
    sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..", "..")))
    import soliton_simulator as S
    TAU_A = float(S.TAU_A)
    print("TAU_A = %s   DT = %s   (LETTE dal modulo)" % (TAU_A, S.DT))

    files = sorted(glob.glob(os.path.join(DEST, "scena_??????.pkl*")))
    print("snapshot trovati: %d in %s" % (len(files), DEST))
    if len(files) < 2:
        print("SERVONO ALMENO DUE SNAPSHOT."); return 2

    st0 = carica(files[0])
    N0 = int(len(st0["attrs"]["eta"]))
    print("COORTE ORIGINALE = i primi %d indici (n al primo snapshot, passo %s). ANAGRAFICA."
          % (N0, st0["attrs"].get("_db_step")))
    print("blob: %s" % str(st0.get("blob"))[:8])
    print("")

    hdr = ("%-8s %-8s %-9s | %-9s %-9s %-8s | %-8s %-8s | %-9s %-9s"
           % ("passo", "n", "archi", "Z9b", "fr>0.5", "fr>0.9", "p95/p05", "rampMed", "|psi|", "rho_spin"))
    print("=== 1/2/3 -- Z9-b, ramp per coorte, dispersione del kernel ===")
    print(hdr)
    print("-" * len(hdr))
    serie = []
    for p in files:
        st = carica(p)
        at = st["attrs"]
        passo = int(at.get("_db_step", -1))
        ramp = ramp_di(at, TAU_A)
        i = np.asarray(at["i"], np.int64); j = np.asarray(at["j"], np.int64)
        # (1) Z9-b: archi INTERNI alla coorte originale
        dentro = (i < N0) & (j < N0)
        prod = ramp[i[dentro]] * ramp[j[dentro]]
        z9b = float(np.median(prod)) if prod.size else float("nan")
        # (2) ramp della coorte originale
        ro = ramp[:N0]
        f05, f09 = float(np.mean(ro > 0.5)), float(np.mean(ro > 0.9))
        # (3) dispersione del kernel
        p95, p05 = q(prod, 95), q(prod, 5)
        rap = p95 / p05 if p05 > 0 else float("inf")
        # (4) conseguenze
        psi = np.abs(np.asarray(at["psi"]))
        rho = np.asarray(at["rho_spin"], float)
        # ⚠ NON SI TRATTIENE `at`: 100 snapshot x ~50 MB decompressi = ~5 GB di RAM, e lo script
        # morirebbe di OOM DOPO aver letto mezzo archivio. Si tengono solo i NUMERI; i blocchi 4 e
        # 5 rileggono i file uno alla volta. Costa I/O, non memoria.
        serie.append(dict(passo=passo, n=len(ramp), archi=len(i), z9b=z9b, f05=f05, f09=f09,
                          rap=rap, rampmed=float(np.median(ro)), file=p,
                          maturi=float(np.mean(prod >= 1.0)),
                          psi=float(np.median(psi)), rho=float(np.median(rho))))
        del at, st, ramp, i, j, prod, psi, rho
        print("%-8d %-8d %-9d | %-9.6f %-9.4f %-8.4f | %-8.3f %-8.4f | %-9.3e %-9.3e"
              % (passo, len(ramp), len(i), z9b, f05, f09, rap, float(np.median(ro)),
                 float(np.median(psi)), float(np.median(rho))))

    u = serie[-1]
    print("")
    print("=== VERDETTO su Z9-b (il criterio di chiusura di Z9) ===")
    print("  a 2400 passi valeva 0.074950 (TRE masse, blob a1ae5090 -- RIFERIMENTO, blob diverso: A3c)")
    print("  ORA, al passo %d: %.6f   -> x%.2f" % (u["passo"], u["z9b"], u["z9b"] / 0.074950))
    print("  frazione di archi MATURI (prod == 1): %.6f" % u["maturi"])
    if u["z9b"] >= 1.0:
        print("  *** Z9-b == 1: IL CRITERIO E' SODDISFATTO. Z9 SI CHIUDE. ***")
    else:
        print("  Z9-b NON soddisfatto: manca un fattore %.2f. Z9 RESTA APERTA." % (1.0 / u["z9b"]))
    cre = [s["z9b"] for s in serie]
    if len(cre) >= 3:
        print("  la crescita SATURA?  ultimo terzo/primo terzo degli incrementi: %.3f"
              % ((cre[-1] - cre[-len(cre) // 3]) / max(cre[len(cre) // 3] - cre[0], 1e-12)))
        print("     (< 1 = satura, come P2 prevede; >= 1 = cresce ancora lineare)")
    print("  p95/p05: da %.3f a %.3f   -> %s (P7 prevedeva NON-MONOTONIA: cresce e poi CALA)"
          % (serie[0]["rap"], u["rap"], "SI STRINGE" if u["rap"] < serie[0]["rap"] else "NON si stringe"))
    print("  massimo di p95/p05 lungo il run: %.3f al passo %d"
          % (max(s["rap"] for s in serie),
             serie[int(np.argmax([s["rap"] for s in serie]))]["passo"]))

    print("")
    print("=== 4 -- LE CONSEGUENZE (il registro le dichiara MAI MISURATE) ===")
    print("%-8s %-11s %-11s %-11s %-10s %-9s %-10s %-10s"
          % ("passo", "|psi| med", "rho_spin", "cs med", "cs_std/cs%", "grado med", "r med mob", "passi(r=1)"))
    for s in serie:
        at = carica(s["file"])["attrs"]          # RILETTO, non trattenuto
        cs = np.asarray(at.get("_cs_nodo_prev", []), float)
        cs = cs[np.isfinite(cs)]
        csm = float(np.median(cs)) if cs.size else float("nan")
        css = float(np.std(cs) / csm) if cs.size and csm else float("nan")
        deg = np.asarray(at.get("_deg", []), float)
        # `r` E' LETTO da _r_corrente, MAI stimato da eta: sarebbe CIRCOLARE (Z9-a lo vieta).
        # E `_r_corrente` puo' essere PIU' CORTO di eta (misurato: 2849 contro 2851), perche' e'
        # scritto prima dell'ultima mitosi: si tronca al minimo e SI CONTA (A8).
        rr = at.get("_r_corrente")
        rmed = passi1 = float("nan")
        if rr is not None:
            rr = np.asarray(rr, float)
            if rr.size != len(at["eta"]):
                _tronca[0] += 1
            rr = rr[np.isfinite(rr)]
            if rr.size:
                mob = rr > np.min(rr) * (1.0 + 1e-6)
                rmed = float(np.median(rr[mob])) if mob.any() else float(np.median(rr))
                passi1 = TAU_A / (float(S.DT) * rmed) if rmed > 0 else float("inf")
        print("%-8d %-11.4e %-11.4e %-11.6f %-10.4f %-9.1f %-10.4f %-10.0f"
              % (s["passo"], s["psi"], s["rho"], csm, 100 * css,
                 float(np.median(deg)) if deg.size else float("nan"), rmed, passi1))
    print("  P9 prevedeva cs VIVO (~10 %, non 0.01 %): Z39 aveva misurato 17.6 %.")
    print("  E la colonna passi(r=1) e' il presidio di P3: se `r` SCENDE, quel numero SALE e Z9-b")
    print("  puo' smettere di crescere -- il modo in cui Z9 resterebbe aperta PER SEMPRE.")

    print("")
    print("=== 5 -- IL CICLO, in unita' COMOVENTI ===")
    print("  R_anello(t) = mediana del raggio dei nodi ad ALTO GRADO (p90), che Z46 identifica")
    print("  con le masse seminate. La regione interna si misura in FRAZIONI di R_anello, non in")
    print("  raggio assoluto: un sistema che si espande campionato a raggio fisso ALIASA (par.4).")
    print("%-8s %-10s %-10s | %s" % ("passo", "R_anello", "n", "nodi interni per frazione " + str(FRAZ_INTERNA)))
    for s in serie:
        at = carica(s["file"])["attrs"]          # RILETTO, non trattenuto
        pos = np.asarray(at["pos"], float)
        deg = np.asarray(at.get("_deg", []), float)
        m = min(len(pos), len(deg))
        rr = np.linalg.norm(pos[:m], axis=1)
        if m == 0:
            continue
        alto = deg[:m] >= np.percentile(deg[:m], 90)
        R = float(np.median(rr[alto])) if alto.any() else float("nan")
        conta = [int(np.sum(rr < f * R)) for f in FRAZ_INTERNA]
        print("%-8d %-10.4f %-10d | %s" % (s["passo"], R, len(rr), conta))
    print("  Z49 (2400 passi, blob DIVERSO): nodi(interni) 900 -> 221 -> 907, dilatazione che")
    print("  RIMBALZAVA (-7.44 -> -2.70 -> -4.21 -> +2.80 -> -1.13 %). RIFERIMENTO, non dato (A3c).")
    print("  P10 prevedeva almeno un SECONDO minimo; P11 che il secondo periodo sia PIU' LUNGO.")
    if _tronca[0]:
        print("")
        print("  NB (A8): troncamento per disallineamento di lunghezza applicato %d volte." % _tronca[0])
    print("")
    print("UN SEME, UNA SCENA. Nessuna identificazione. Ogni numero eredita --tau-luce (sigillo 6/7).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
