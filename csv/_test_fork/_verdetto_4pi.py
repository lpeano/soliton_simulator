# -*- coding: utf-8 -*-
"""VERDETTO della prima misura del settore spinoriale su sistema PULITO — (A) / (B) / (C).

Legge i CSV prodotti da `_osserva_vuoto.py` (osservatore sigillato 6/6 PASS sulla versione estesa)
e applica le soglie gia' fissate in `doc/PREDIZIONE_prima_misura_4pi.md`, committato PRIMA del run.

LE SOGLIE, ricopiate dalla predizione e NON ritoccate qui:
  (A) |chi_media - 90| < 3*SE in materia E nel p90;  |<n>|/(1/sqrt(N)) < 2;  |acorr| < 3*SE in OGNI bin
  (B) |chi_media - 90| > 5*SE  E  autocorr che decade a scala FINITA (un bin vicino > 3*SE e i
      lontani compatibili con 0)  E  |<n>| < 0.5      [serve su >= 2 semi]
  (C) chi scende  E  |<n>| > 0.5  E  autocorr > 0.5 anche nel bin PIU' LONTANO

NB: `SE = std/sqrt(n)` e' la barra INTERNA al run. Per il confronto FRA SEMI si usa la dispersione
dei due semi (C10: su questo sistema caotico la barra giusta e' ~3 volte quella interna).
"""
import csv, glob, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
NULL_MEDIA, NULL_STD = 90.000, 39.171          # direzioni di Bloch casuali (CLAUDE.md par.9)


def leggi(percorso):
    with open(percorso) as f:
        return list(csv.DictReader(f))


def g(riga, chiave, grad=False):
    v = riga.get(chiave)
    if v is None or v == "":
        return float("nan")
    try:
        x = float(v)
    except ValueError:
        return float("nan")
    return math.degrees(x) if grad else x


def analizza(percorso):
    r = leggi(percorso)
    u = r[-1]
    out = {"file": os.path.basename(percorso), "passi": int(float(u["passo"])),
           "n": int(float(u["n"])), "campioni": len(r)}
    for reg in ("mat", "vuo", "p90", "tot"):
        med = g(u, "chi_%s_media" % reg, grad=True)
        sd = g(u, "chi_%s_std" % reg, grad=True)
        nn = g(u, "chi_%s_n" % reg)
        se = sd / math.sqrt(nn) if nn > 1 else float("nan")
        out["chi_%s" % reg] = (med, sd, nn, se, (med - NULL_MEDIA) / se if se == se and se > 0 else float("nan"))
        out["fr10_%s" % reg] = g(u, "chi_%s_fr_lt10g" % reg)
        out["fr170_%s" % reg] = g(u, "chi_%s_fr_gt170g" % reg)
    out["nmod"] = g(u, "nmed_tot_mod"); out["natt"] = g(u, "nmed_tot_atteso")
    out["nmod_mat"] = g(u, "nmed_mat_mod"); out["natt_mat"] = g(u, "nmed_mat_atteso")
    out["theta_giri"] = g(u, "theta_giri_mediana")
    out["theta_fr30"] = g(u, "theta_fr_gt30g"); out["theta_fr360"] = g(u, "theta_fr_gt360g")
    out["r_std"] = g(u, "r_std"); out["r_iqr"] = g(u, "r_iqr"); out["r_med"] = g(u, "r_mediana")
    out["ac"] = [(g(u, "ac%d_d" % b), g(u, "ac%d" % b), g(u, "ac%d_se" % b)) for b in range(10)]
    out["serie_chi"] = [(int(float(x["passo"])), g(x, "chi_mat_media", grad=True)) for x in r]
    return out


def stampa(a):
    print("-" * 100)
    print("  %s   passi %d   n %d   campioni %d" % (a["file"], a["passi"], a["n"], a["campioni"]))
    print("-" * 100)
    print("  chi (gradi) - valore-null: %.3f +- %.3f   [z = (media-90)/SE, SE INTERNA al run]" % (NULL_MEDIA, NULL_STD))
    for reg, eti in (("mat", "MATERIA"), ("vuo", "VUOTO  "), ("p90", "p90    "), ("tot", "tutto  ")):
        med, sd, nn, se, z = a["chi_%s" % reg]
        print("    %s media %8.4f   std %7.4f   n %7d   SE %.4f   scarto %+.4f   z %+6.2f"
              % (eti, med, sd, int(nn), se, med - NULL_MEDIA, z))
    print("    frazioni ai poli degeneri:  <10 gradi  mat %.5f  p90 %.5f     >170 gradi  mat %.5f  p90 %.5f"
          % (a["fr10_mat"], a["fr10_p90"], a["fr170_mat"], a["fr170_p90"]))
    print()
    print("  |<n>| - valore-null 1/sqrt(N); la firma che smaschera il COLLASSO e' il confronto con 1")
    print("    tutto   |<n>| %.6f   atteso %.6f   rapporto %.3f   contro 1: %.4f"
          % (a["nmod"], a["natt"], a["nmod"] / max(a["natt"], 1e-12), a["nmod"]))
    print("    materia |<n>| %.6f   atteso %.6f   rapporto %.3f"
          % (a["nmod_mat"], a["natt_mat"], a["nmod_mat"] / max(a["natt_mat"], 1e-12)))
    print()
    print("  AUTOCORRELAZIONE <n_i . n_j> per bin di distanza - la firma che DISCRIMINA")
    print("    bin |  distanza |     acorr |        SE |    z")
    for b, (d, v, se) in enumerate(a["ac"]):
        z = v / se if se == se and se > 0 else float("nan")
        print("    %3d | %9.4f | %+9.5f | %9.5f | %+5.2f" % (b, d, v, se, z))
    print()
    print("  theta = |omega|*dt_n : mediana %.2f GIRI/passo   sopra 30 gradi/passo: %.4f   sopra 360: %.4f"
          % (a["theta_giri"], a["theta_fr30"], a["theta_fr360"]))
    print("  r : dispersione std %.6f   IQR %.6f   (mediana %.6f - deve valere 1: e' NORMALIZZATA,"
          % (a["r_std"], a["r_iqr"], a["r_med"]))
    print("      non e' una misura, vedi CLAUDE.md par.9)")


def verdetto(aa):
    print()
    print("=" * 100)
    print("VERDETTO contro doc/PREDIZIONE_prima_misura_4pi.md (soglie fissate PRIMA del run)")
    print("=" * 100)
    esiti = []
    for a in aa:
        zm = a["chi_mat"][4]; zp = a["chi_p90"][4]
        rap = a["nmod"] / max(a["natt"], 1e-12)
        zac = [abs(v / se) if se == se and se > 0 else 0.0 for d, v, se in a["ac"]]
        ac_far = a["ac"][-1][1]
        condA = (abs(zm) < 3 and abs(zp) < 3 and rap < 2 and max(zac) < 3)
        condB = (abs(zm) > 5 and zac[0] > 3 and max(zac[-3:]) < 3 and a["nmod"] < 0.5)
        condC = (zm < -5 and a["nmod"] > 0.5 and ac_far > 0.5)
        e = "(B)" if condB else ("C" if condC else ("(A)" if condA else "INDETERMINATO"))
        esiti.append(e)
        print("  %s  ->  %s      |z_mat| %.2f  |z_p90| %.2f  |<n>|/atteso %.2f  max|z_acorr| %.2f"
              % (a["file"], e, abs(zm), abs(zp), rap, max(zac)))
    print()
    if all(x == "(A)" for x in esiti):
        print("  ESITO (A) su tutti i semi - NIENTE CAMBIA.")
        print("  E il CAVEAT dichiarato nella predizione par.1, che NON si toglie:")
        print("    theta e' a %.0f giri/passo: il settore e' ALIASATO, e queste cure non lo risolvono."
              % max(a["theta_giri"] for a in aa))
        print("    (A) e' l'esito che l'aliasing produrrebbe DA SOLO. E' compatibile con 'non c'e'")
        print("    ordine' E con 'c'e' ordine e non lo vediamo': NON separa le due.")
        print("    La frase dicibile e' quella, piu' stretta, scritta nella predizione par.1.")
    elif all(x == "(B)" for x in esiti) and len(aa) >= 2:
        print("  ESITO (B) su >= 2 semi - COMPARE STRUTTURA. La doppia copertura era il pezzo mancante.")
    elif any(x == "C" for x in esiti):
        print("  ESITO (C) - COLLASSO, non struttura. Allineamento globale degenere.")
    else:
        print("  ESITI DISCORDANTI FRA SEMI: %s  -> nessun verdetto. Par.2.7: mai su un solo seme."
              % ", ".join(esiti))
    if len(aa) >= 2:
        print()
        print("  LA BARRA FRA SEMI (C10) - e' quella che conta, non la SE interna:")
        for eti, key in (("chi materia (gradi)", lambda a: a["chi_mat"][0]),
                         ("|<n>|", lambda a: a["nmod"]),
                         ("theta (giri/passo)", lambda a: a["theta_giri"]),
                         ("dispersione di r", lambda a: a["r_std"])):
            v = np.array([key(a) for a in aa], float)
            print("    %-22s %s   media %.6f   dev.std FRA SEMI %.6f"
                  % (eti, "  ".join("%.5f" % x for x in v), v.mean(), v.std(ddof=1)))
    print("=" * 100)


def main():
    file = sys.argv[1:] or sorted(glob.glob(os.path.join(HERE, "_vuoto_pulito*_s*.vuoto.csv")))
    if not file:
        print("nessun CSV trovato"); return 1
    aa = [analizza(f) for f in file]
    print("=" * 100)
    print("PRIMA MISURA DEL SETTORE SPINORIALE SU SISTEMA PULITO - %d semi" % len(aa))
    print("  entrambe le cure nel codice; NB: --cs-dinamico OFF in questi run, quindi la cura della")
    print("  cache cs e' INERTE qui: si sta esercitando l'orologio a 4pi, non il tempo-luce.")
    print("=" * 100)
    for a in aa:
        stampa(a)
    verdetto(aa)
    return 0


if __name__ == "__main__":
    sys.exit(main())
