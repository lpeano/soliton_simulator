# -*- coding: utf-8 -*-
"""IL PILOTA DEL RUN A 6000 PASSI -- i TRE numeri, e la CADENZA che ne DERIVA.

Non gira niente: LEGGE la serie prodotta dal pilota del driver. Girare e misurare sono due
mestieri, e tenerli separati permette di rifare la misura senza rifare il run.

I TRE NUMERI CHE IL MANDATO CHIEDE
  1. LA DURATA VERA PER FRAME, e come CRESCE con `n`. L'estrapolazione lineare SOTTOSTIMA -- lo
     dice il driver stesso -- quindi si riportano DUE modelli e si dichiara il range.
  2. IL PESO REALE di uno snapshot compresso a livello 1, e COME CRESCE. Il conto della serie si
     fa sul peso FINALE, non sul primo.
  3. IL TASSO `d(eta)/d(passo)` per FERMI e MOBILI **SEPARATI** (A3c: mai una mediana sulle due
     popolazioni), e `passi(ramp = 1) = TAU_A/(DT*r) = 5000/r` per ciascuno.

*** IL BUDGET DI SPAZIO E' FISSATO QUI, PRIMA DI GUARDARE I NUMERI ***
  Disco `C:` al 96 %, 20 GB liberi, e `os.replace` tiene DUE COPIE durante la scrittura.
  BUDGET = 5.0 GB per l'archivio, PIU' il picco di una copia doppia dello snapshot piu' grande.
  Restano cosi' ~15 GB liberi. **Il numero e' dichiarato PRIMA perche' non possa essere
  aggiustato DOPO per far tornare una cadenza comoda.**

*** COME SI SEPARANO FERMI E MOBILI, e perche' la soglia non e' scelta ***
  `Z46` ha misurato che il sistema si separa in DUE popolazioni "che non si parlano": il 93 % al
  PAVIMENTO di `ritmo()` (`r = 1.414213e-06`, `r/r_floor = 1.0000` su 4 intervalli su 4) e il
  resto a saturazione. Qui NON si sceglie una soglia: si prende `r_min` MISURATO e si guarda la
  frazione sotto `r_min*(1+eps)` per eps = 1e-6, 10, 100, 1000. **Se la separazione e' vera, la
  frazione non cambia**; se cambia, la soglia sta facendo lavoro e va DETTO invece di nasconderlo.
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

DEST = sys.argv[1] if len(sys.argv) > 1 else os.path.join("csv", "_test_fork", "_pilota6000scena")
BUDGET_GB = 5.0                 # DICHIARATO PRIMA, vedi il docstring
PASSI_TOT = 6000                # il run del mandato
TAU_A, DT = 50.0, 0.01          # si RILEGGONO dal modulo piu' sotto: questi sono solo il fallback
PASSI_PER_FRAME = 6


def carica(p):
    ap = gzip.open if p.endswith(".gz") else open
    with ap(p, "rb") as f:
        return pickle.load(f)


def main():
    global TAU_A, DT, PASSI_PER_FRAME
    sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..", "..")))
    try:
        import soliton_simulator as S
        TAU_A, DT, PASSI_PER_FRAME = float(S.TAU_A), float(S.DT), int(S.PASSI_PER_FRAME)
        print("costanti LETTE dal modulo: TAU_A=%s  DT=%s  PASSI_PER_FRAME=%s"
              % (TAU_A, DT, PASSI_PER_FRAME))
    except Exception as e:
        print("ATTENZIONE: costanti non lette dal modulo (%s): uso i fallback" % type(e).__name__)

    files = sorted(glob.glob(os.path.join(DEST, "scena_??????.pkl*")))
    if len(files) < 2:
        print("SERVONO ALMENO DUE SNAPSHOT: trovati %d in %s" % (len(files), DEST))
        return 2

    print("")
    print("=== 2. IL PESO, e come cresce ===")
    righe = []
    for p in files:
        st = carica(p)
        at = st["attrs"]
        passo = int(at.get("_db_step", -1))
        n = int(at.get("n", len(at.get("eta", []))))
        na = len(at.get("i", []))
        mb = os.path.getsize(p) / 1e6
        righe.append(dict(passo=passo, n=n, archi=na, mb=mb, at=at, blob=st.get("blob")))
        print("  passo %-6d n=%-8d archi=%-9d %8.3f MB   (%.4f MB per 1000 nodi)"
              % (passo, n, na, mb, 1000.0 * mb / max(n, 1)))
    print("  blob negli snapshot: %s" % sorted(set(r["blob"][:8] for r in righe if r["blob"])))

    # ⚠ IL MODELLO A TRE PARAMETRI E' DEGENERE SU QUESTI DATI, E IL PRIMO GIRO L'HA DIMOSTRATO:
    # con 3 punti e 3 incognite il fit INTERPOLA esattamente, e poiche' `archi` varia dello 0.13 %
    # mentre il peso varia del 4 %, il coefficiente per arco ESPLODE -> estrapolava 450 GB per
    # snapshot. Era un artefatto del MIO strumento, non un dato.
    # SI MISURA INVECE CIO' CHE SI PUO' MISURARE:
    #   (a) quanti ARCHI porta un nodo nuovo, dalla crescita osservata;
    #   (b) il peso per ARCO, che e' il termine dominante (d, d0, tw sono float64 PER ARCO).
    d_n = righe[-1]["n"] - righe[0]["n"]
    d_a = righe[-1]["archi"] - righe[0]["archi"]
    archi_per_nodo_nuovo = d_a / d_n if d_n else float("nan")
    mb_per_arco = righe[-1]["mb"] / max(righe[-1]["archi"], 1)
    print("  CRESCITA MISURATA: +%d nodi -> +%d archi  =  %.2f archi per nodo nuovo"
          % (d_n, d_a, archi_per_nodo_nuovo))
    print("     (il codice ne prescrive 2: il figlio nasce con due archi verso i genitori. Meno di 2")
    print("      significa che qualche arco viene anche RIMOSSO -- si misura, non si assume)")
    print("  peso per arco: %.4f kB   |  peso osservato: da %.2f a %.2f MB (%+.1f %%) mentre n fa %+.1f %%"
          % (1000 * mb_per_arco, righe[0]["mb"], righe[-1]["mb"],
             100 * (righe[-1]["mb"] / righe[0]["mb"] - 1), 100 * (righe[-1]["n"] / righe[0]["n"] - 1)))
    print("  -> IL PESO E' DOMINATO DAGLI ARCHI, CHE CRESCONO POCO: non da n.")
    ra = archi_per_nodo_nuovo

    print("")
    print("=== 1. LA DURATA, e come cresce ===")
    prog = os.path.join(DEST, "prog.csv")
    fr, tt, nn = [], [], []
    if os.path.exists(prog):
        for L in open(prog, encoding="utf-8"):
            if L.startswith("#") or L.startswith("frame"):
                continue
            c = L.strip().split(",")
            if len(c) >= 7:
                fr.append(int(c[0])); nn.append(int(c[2])); tt.append(float(c[6]))
    if len(fr) >= 3:
        dt_fr = [(tt[k] - tt[k - 1]) / (fr[k] - fr[k - 1]) for k in range(1, len(fr))]
        nm = [0.5 * (nn[k] + nn[k - 1]) for k in range(1, len(fr))]
        print("  costo per frame contro n:")
        for k in range(len(dt_fr)):
            print("     n~%-8.0f  %6.2f s/frame" % (nm[k], dt_fr[k]))
        # modello LINEARE in n: costo = a*n + b
        M = np.array([[x, 1.0] for x in nm], float)
        ca, *_ = np.linalg.lstsq(M, np.array(dt_fr, float), rcond=None)
        print("  MODELLO costo(s/frame) = %.6g*n + %.4g" % (ca[0], ca[1]))
    else:
        ca = None
        print("  progresso insufficiente (%d punti)" % len(fr))

    print("")
    print("=== 3. IL TASSO d(eta)/d(passo), FERMI e MOBILI SEPARATI (A3c) ===")
    print("    la legge DERIVATA (Z9, dal codice) e': d(eta)/d(passo) = DT*r  ->  passi(ramp=1) = TAU_A/(DT*r)")
    ultimo = righe[-1]
    r = np.asarray(ultimo["at"].get("_r_corrente"), float) if ultimo["at"].get("_r_corrente") is not None else None
    eta = np.asarray(ultimo["at"].get("eta"), float)
    if r is None or r.size == 0:
        print("  _r_corrente ASSENTE nello snapshot: il tasso non si misura, e NON lo stimo da eta")
        print("  (sarebbe CIRCOLARE: eta cresce PER r -- Z9-a lo vieta esplicitamente)")
        return 3
    rmin = float(np.min(r))
    print("  r: min %.6e  mediana %.6e  max %.6e   (n=%d)" % (rmin, float(np.median(r)), float(np.max(r)), r.size))
    print("  LA SOGLIA NON E' SCELTA -- frazione 'ferma' al variare del margine su r_min:")
    for eps in (1e-6, 10.0, 100.0, 1000.0):
        f = float(np.mean(r <= rmin * (1.0 + eps)))
        print("     r <= r_min*(1+%-8g)   fermi = %6.2f %%" % (eps, 100 * f))
    fermi = r <= rmin * (1.0 + 1e-6)
    mob = ~fermi
    print("  -> FERMI %d (%.2f %%)   MOBILI %d (%.2f %%)"
          % (fermi.sum(), 100 * fermi.mean(), mob.sum(), 100 * mob.mean()))
    for nome, sel in (("FERMI", fermi), ("MOBILI", mob)):
        if not sel.any():
            print("  %-7s: popolazione VUOTA" % nome); continue
        rm = float(np.median(r[sel]))
        tasso = DT * rm
        print("  %-7s  r mediano %.6e   d(eta)/d(passo) = DT*r = %.6e   passi(ramp=1) = %.4g"
              % (nome, rm, tasso, TAU_A / tasso if tasso > 0 else float("inf")))
    # Z9-a: i passi mancanti, sui soli MOBILI
    if mob.any():
        rmed_mob = float(np.median(r[mob]))
        mancanti = TAU_A / (DT * rmed_mob) - ultimo["passo"]
        print("  Z9-a  passi_mancanti = TAU_A/(DT*r_MED_MOBILI) - passi_fatti = %.0f - %d = %.0f"
              % (TAU_A / (DT * rmed_mob), ultimo["passo"], mancanti))
        print("        -> a %d passi il run %s la maturazione dei mobili"
              % (PASSI_TOT, "SUPERA" if PASSI_TOT >= TAU_A / (DT * rmed_mob) else "NON raggiunge"))
    # controprova sul tasso: eta misurata fra i due ultimi snapshot, sui nodi comuni
    if len(righe) >= 2:
        pre = righe[-2]
        e0 = np.asarray(pre["at"].get("eta"), float)
        dpasso = ultimo["passo"] - pre["passo"]
        m = min(e0.size, eta.size)
        d_eta = (eta[:m] - e0[:m]) / dpasso
        atteso = DT * r[:m]
        ok = np.isfinite(d_eta) & np.isfinite(atteso) & (atteso > 0)
        if ok.any():
            rap = float(np.median(d_eta[ok] / atteso[ok]))
            print("  CONTROPROVA (Z9: il falsificatore): d(eta)/d(passo) MISURATO / DT*r LETTO = %.4f"
                  % rap)
            print("     (Z9 dava 0.9977 e 0.9966 negli ultimi due intervalli: entro lo 0.3 %)")
            # ⚠ SE IL RAPPORTO NON E' ~1 NON SI SPIEGA: SI MISURA. Z9 aveva gia' visto 0.625 nel
            # primo intervallo e la ragione era che `r` SI MUOVE dentro l'intervallo, quindi `r`
            # campionato all'ESTREMO non rappresenta la media. Qui si verifica proprio quello,
            # confrontando `r` ai due estremi -- se `r` e' sceso, il rapporto DEVE essere > 1.
            r0 = pre["at"].get("_r_corrente")
            if r0 is not None:
                r0 = np.asarray(r0, float)
                mm = min(r0.size, r.size)
                med0, med1 = float(np.median(r0[:mm])), float(np.median(r[:mm]))
                print("     r mediano: %.6f al passo %d  ->  %.6f al passo %d   (%+.2f %%)"
                      % (med0, pre["passo"], med1, ultimo["passo"], 100 * (med1 / med0 - 1)))
                atteso_rap = 0.5 * (med0 + med1) / med1 if med1 else float("nan")
                print("     se `r` scende, usare l'ESTREMO FINALE SOTTOSTIMA: rapporto atteso con la")
                print("     media dei due estremi = %.4f   contro il %.4f misurato" % (atteso_rap, rap))
                if abs(atteso_rap - rap) < 0.1:
                    print("     -> LO SCARTO E' SPIEGATO DAL MOVIMENTO DI `r`, ed e' MISURATO: il")
                    print("        falsificatore di Z9 NON scatta. (Stesso effetto del suo 0.625.)")
                else:
                    print("     -> ATTENZIONE: lo scarto NON e' spiegato dal movimento di `r`.")
                    print("        NON lo spiego altrimenti: va riportato cosi'.")

    print("")
    print("=== LA CADENZA, DERIVATA dal budget dichiarato PRIMA (%.1f GB) ===" % BUDGET_GB)
    if ca is None:
        print("  impossibile senza il modello del costo"); return 0
    # n a fine run: si estrapola la crescita di n col FRAME, con DUE modelli
    frames_tot = PASSI_TOT // PASSI_PER_FRAME
    nfit = np.polyfit(fr, nn, 1)
    n_lin = float(np.polyval(nfit, frames_tot))
    # modello esponenziale (la mitosi e' moltiplicativa): log n lineare nel frame
    gfit = np.polyfit(fr, np.log(np.array(nn, float)), 1)
    n_exp = float(np.exp(np.polyval(gfit, frames_tot)))
    print("  n a %d frame:  LINEARE %.0f    ESPONENZIALE %.0f   <- DUE MODELLI, range DICHIARATO"
          % (frames_tot, n_lin, n_exp))
    print("  (riferimento STORICO, scena a 2400 passi: n = 8018 a 400 frame. Blob DIVERSO: e' un")
    print("   riferimento, non un dato di questo run -- A3c)")
    for nomeM, nfin in (("lineare", n_lin), ("esponenziale", n_exp)):
        # peso finale = peso attuale scalato sugli ARCHI attesi, che e' il termine dominante
        archi_fin = righe[-1]["archi"] + ra * max(nfin - righe[-1]["n"], 0)
        mb_fin = righe[-1]["mb"] * archi_fin / max(righe[-1]["archi"], 1)
        print("     archi attesi a fine run: %.0f (%+.1f %%)"
              % (archi_fin, 100 * (archi_fin / righe[-1]["archi"] - 1)))
        print("  [%s] n_fin=%.0f -> snapshot finale ~%.1f MB;  picco doppia copia ~%.1f MB"
              % (nomeM, nfin, mb_fin, 2 * mb_fin))
        print("     cadenza  snapshot   spazio stimato (media peso lineare in n)")
        for ogni_passi in (60, 120, 300, 600, 1200):
            k = PASSI_TOT // ogni_passi
            mb_medio = 0.5 * (righe[0]["mb"] + mb_fin)
            gb = k * mb_medio / 1000.0
            print("     %5d      %5d      %8.2f GB   %s"
                  % (ogni_passi, k, gb, "OK" if gb <= BUDGET_GB else "OLTRE IL BUDGET"))
    tot_s = sum(ca[0] * (nn[0] + (n_lin - nn[0]) * k / frames_tot) + ca[1] for k in range(frames_tot))
    print("  DURATA stimata (modello LINEARE di n, che SOTTOSTIMA): %.0f s = %.1f h" % (tot_s, tot_s / 3600))
    return 0


if __name__ == "__main__":
    sys.exit(main())
