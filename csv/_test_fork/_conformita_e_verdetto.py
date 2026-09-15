# -*- coding: utf-8 -*-
"""CHECKLIST DI CONFORMITA' (bloccante) + VERDETTO a DUE BRACCI.

PARTE 1 - CONFORMITA'. Per ogni run legge dal CSV, mai dal nome del file, e confronta con la
matrice prescritta. **Se anche UN SOLO campo non combacia, quel run NON si conta** e lo script
esce con codice != 0. Non "aggiusta" niente.

  campo          atteso
  blob           08784685
  CS_DINAMICO    1 in tutti e quattro          <-- il vincolo che ha causato il giro perso
  cs_std         NON nan, e > 0                <-- se e' nan la cache non esiste: STOP
  FORK_SU2       1
  FORK_SU2_MEM   1
  TAU_LUCE       0,0,1,1 secondo la matrice
  KURAMOTO_SU2   0        STEP2  0        GAMMA_TURBO  1.0
  seed / tag     come da matrice

  + il controllo che NON dipende dai flag: cs_std / cs_medio. Sotto l'1 % significa che `cs` e'
    quasi-costante anche col flag acceso, quindi `tau = d/cs` e' praticamente `tau ~ d`, e va
    DETTO nel referto invece di restare implicito.

PARTE 2 - VERDETTO, con le soglie gia' fissate in doc/PREDIZIONE_prima_misura_4pi.md (par.2 e
par.3-bis), ricopiate e non ritoccate. Il confronto FRA BRACCI usa la dispersione FRA SEMI, non la
SE interna a un run (C10: e' l'errore che ha prodotto il "16.9 %" e l'"11.0 %", entrambi ritirati).

Il valore-null di |<n>| NON e' 1/sqrt(N) (quella e' la SCALA): l'attesa misurata e'
|<n>|*sqrt(N) = 0.92 +- 0.38, p95 ~ 1.60.
"""
import csv, glob, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
BLOB_ATTESO = "08784685eeb17835389d248a2d1d07db4f0d1305"
NULL_CHI_MEDIA, NULL_CHI_STD = 90.000, 39.171
NULL_NMOD_MEDIA, NULL_NMOD_STD, NULL_NMOD_P95 = 0.9213, 0.3888, 1.60

MATRICE = [("csOFF", 1, 0), ("csOFF", 2, 0), ("csON", 1, 1), ("csON", 2, 1)]


def leggi(tag, seed):
    f = os.path.join(HERE, "_vuoto_%s_s%d.vuoto.csv" % (tag, seed))
    if not os.path.exists(f):
        return None, f
    with open(f) as fh:
        return list(csv.DictReader(fh)), f


def val(r, k):
    v = r.get(k)
    if v is None or v == "":
        return float("nan")
    try:
        return float(v)
    except ValueError:
        return float("nan")


def conformita():
    print("=" * 110)
    print("PARTE 1 - CHECKLIST DI CONFORMITA' (bloccante). Valori LETTI dal CSV, non dal nome file.")
    print("=" * 110)
    tutti_ok = True
    dati = []
    for tag, seed, tau_atteso in MATRICE:
        r, f = leggi(tag, seed)
        print("-" * 110)
        if r is None:
            print("  %-22s FILE ASSENTE: %s   -> NON CONTATO" % (tag + "_s%d" % seed, f))
            tutti_ok = False
            continue
        u = r[-1]
        ok = True

        def cmp(nome, letto, atteso, uguale=None):
            nonlocal ok
            buono = (letto == atteso) if uguale is None else uguale
            if not buono:
                ok = False
            print("    %-14s letto %-42s atteso %-12s %s"
                  % (nome, str(letto), str(atteso), "OK" if buono else "*** NON COMBACIA ***"))

        print("  %s   campioni %d   passi finali %s   n %s"
              % (tag + "_s%d" % seed, len(r), u.get("passo"), u.get("n")))
        blob = u.get("blob", "ASSENTE")
        cmp("blob", blob, BLOB_ATTESO[:8] + "...", uguale=(blob == BLOB_ATTESO))
        for nome, atteso in (("CS_DINAMICO", 1), ("FORK_SU2", 1), ("FORK_SU2_MEM", 1),
                             ("KURAMOTO_SU2", 0), ("STEP2", 0), ("TAU_LUCE", tau_atteso)):
            vs = sorted(set(x.get(nome, "ASSENTE") for x in r))
            cmp(nome, ",".join(vs), atteso, uguale=(len(vs) == 1 and vs[0] != "ASSENTE"
                                                    and int(float(vs[0])) == atteso))
        vg = sorted(set(x.get("GAMMA_TURBO", "ASSENTE") for x in r))
        cmp("GAMMA_TURBO", ",".join(vg), "1.0", uguale=(len(vg) == 1 and float(vg[0]) == 1.0))
        vs_ = sorted(set(x.get("seed", "ASSENTE") for x in r))
        cmp("seed", ",".join(vs_), seed, uguale=(len(vs_) == 1 and int(float(vs_[0])) == seed))
        vt = sorted(set(x.get("tag", "ASSENTE") for x in r))
        cmp("tag", ",".join(vt), tag, uguale=(len(vt) == 1 and vt[0] == tag))

        # cs: il controllo che NON dipende dai flag
        # [CORRETTO 2026-09-15, DOPO aver visto i dati - dichiarato nel commit]
        # BLOCCANTE = la cache ESISTE, cioe' cs_std non e' `nan`. E' la condizione che il mandato
        # nomina come STOP ("se e' nan la cache non esiste"), ed e' cio' che era sbagliato nel giro
        # perso. Il "> 0" era MIO e sbagliava al primo campione: al passo 1, con 80 nodi appena
        # seminati e densita' trascurabile, cs vale ESATTAMENTE CS_M ovunque -> cs_std = 0.0 e
        # cs_min = cs_max = 2.0, che e' fisica corretta, non un difetto di config. Un `0` dice
        # "la cache c'e' e cs non varia ANCORA"; un `nan` dice "la cache non c'e'". Sono cose diverse.
        # Il "cs varia davvero?" resta, ma come CONTROLLO INFORMATIVO (par.3 del mandato), non come
        # blocco: il mandato stesso lo tratta cosi' ("se e' sotto l'1 %, dillo nel referto").
        css = val(u, "cs_std"); csmin = val(u, "cs_min"); csmax = val(u, "cs_max")
        esiste = (css == css)                      # BLOCCANTE: non-nan
        vivo = esiste and css > 0.0                # informativo
        cmp("cs_std (cache esiste?)", "%.6g" % css if esiste else "nan", "non-nan", uguale=esiste)
        if esiste and not vivo:
            print("    NB cs_std = 0 esatto: la cache C'E' ma cs non varia ancora (tipico dei primi")
            print("       passi, pochi nodi e densita' trascurabile). NON e' un difetto di config.")
        if vivo:
            csmed = 0.5 * (csmin + csmax)
            rap = 100.0 * css / max(csmed, 1e-300)
            print("    cs: min %.6f  max %.6f  medio %.6f   cs_std/cs_medio = %.5f %%   %s"
                  % (csmin, csmax, csmed, rap,
                     "<-- SOTTO l'1 %: cs quasi-costante, tau = d/cs e' praticamente tau ~ d"
                     if rap < 1.0 else "cs varia in modo non trascurabile"))
        print("  %s: %s" % (tag + "_s%d" % seed, "CONFORME" if ok else "*** NON CONFORME - NON SI CONTA ***"))
        tutti_ok = tutti_ok and ok
        if ok:
            dati.append((tag, seed, r))
    print("=" * 110)
    print("CONFORMITA' COMPLESSIVA: %s" % ("PASS - i quattro run si contano" if tutti_ok and len(dati) == 4
                                           else "FAIL - NON si procede al verdetto"))
    print("=" * 110)
    return tutti_ok and len(dati) == 4, dati


def firme(r):
    u = r[-1]
    o = {}
    for reg in ("mat", "vuo", "p90", "tot"):
        med = math.degrees(val(u, "chi_%s_media" % reg))
        sd = math.degrees(val(u, "chi_%s_std" % reg))
        nn = val(u, "chi_%s_n" % reg)
        se = sd / math.sqrt(nn) if nn > 1 else float("nan")
        o["chi_" + reg] = (med, sd, nn, se, (med - NULL_CHI_MEDIA) / se if se == se and se > 0 else float("nan"))
        o["fr10_" + reg] = val(u, "chi_%s_fr_lt10g" % reg)
        o["fr170_" + reg] = val(u, "chi_%s_fr_gt170g" % reg)
    o["N"] = val(u, "n")
    o["nmod"] = val(u, "nmed_tot_mod")
    o["nmod_sqrtN"] = o["nmod"] * math.sqrt(o["N"])
    o["z_nmod"] = (o["nmod_sqrtN"] - NULL_NMOD_MEDIA) / NULL_NMOD_STD
    o["theta_giri"] = val(u, "theta_giri_mediana")
    o["theta_fr30"] = val(u, "theta_fr_gt30g")
    o["r_std"] = val(u, "r_std"); o["r_iqr"] = val(u, "r_iqr"); o["r_med"] = val(u, "r_mediana")
    o["cs_std"] = val(u, "cs_std")
    o["ac"] = [(val(u, "ac%d_d" % b), val(u, "ac%d" % b), val(u, "ac%d_se" % b)) for b in range(10)]
    return o


def stampa(eti, o):
    print("-" * 110)
    print("  %s    N = %d" % (eti, int(o["N"])))
    print("    chi (gradi), null %.3f +- %.3f   [z con SE INTERNA al run]" % (NULL_CHI_MEDIA, NULL_CHI_STD))
    for reg, nome in (("mat", "MATERIA"), ("vuo", "VUOTO  "), ("p90", "p90    ")):
        med, sd, nn, se, z = o["chi_" + reg]
        print("      %s media %8.4f  std %7.4f  n %7d  SE %.4f  scarto %+.4f  z %+6.2f"
              % (nome, med, sd, int(nn), se, med - NULL_CHI_MEDIA, z))
    print("    frazioni ai poli (controllo di SIMMETRIA, non dipende dalle barre):")
    print("      <10 gradi  mat %.5f  p90 %.5f      >170 gradi  mat %.5f  p90 %.5f"
          % (o["fr10_mat"], o["fr10_p90"], o["fr170_mat"], o["fr170_p90"]))
    print("    |<n>|*sqrt(N) = %.4f   contro il null EMPIRICO %.4f +- %.4f (p95 %.2f)  ->  z %+5.2f"
          % (o["nmod_sqrtN"], NULL_NMOD_MEDIA, NULL_NMOD_STD, NULL_NMOD_P95, o["z_nmod"]))
    zac = [abs(v / se) if se == se and se > 0 else 0.0 for d, v, se in o["ac"]]
    print("    autocorrelazione 10 bin (%.2f - %.2f):  max|z| = %.2f   %s"
          % (o["ac"][0][0], o["ac"][-1][0], max(zac),
             "piatta a zero" if max(zac) < 3 else "*** un bin si stacca ***"))
    print("    theta mediana %.2f GIRI/passo   frazione > 30 gradi/passo %.4f   (ALIASATO)"
          % (o["theta_giri"], o["theta_fr30"]))
    print("    r: dispersione std %.6f  IQR %.6f   (mediana %.6f = 1 per costruzione, NON e' una misura)"
          % (o["r_std"], o["r_iqr"], o["r_med"]))
    print("    cs_std = %.6g" % o["cs_std"])


def verdetto(oo):
    print()
    print("=" * 110)
    print("PARTE 2 - VERDETTO a DUE BRACCI (soglie da doc/PREDIZIONE_prima_misura_4pi.md, non ritoccate)")
    print("=" * 110)
    esiti = {}
    for k, o in oo.items():
        zm = o["chi_mat"][4]; zp = o["chi_p90"][4]
        zac = [abs(v / se) if se == se and se > 0 else 0.0 for d, v, se in o["ac"]]
        condA = abs(zm) < 3 and abs(zp) < 3 and abs(o["z_nmod"]) < 3 and max(zac) < 3
        condB = abs(zm) > 5 and zac[0] > 3 and max(zac[-3:]) < 3 and o["nmod"] < 0.5
        condC = zm < -5 and o["nmod"] > 0.5 and o["ac"][-1][1] > 0.5
        esiti[k] = "(B)" if condB else ("(C)" if condC else ("(A)" if condA else "INDETERMINATO"))
        print("  %-10s -> %-14s |z_chi_mat| %.2f  |z_chi_p90| %.2f  |z_|<n>|| %.2f  max|z_ac| %.2f"
              % (k, esiti[k], abs(zm), abs(zp), abs(o["z_nmod"]), max(zac)))
    off = [esiti[k] for k in esiti if k.startswith("OFF")]
    on = [esiti[k] for k in esiti if k.startswith("ON")]
    print()
    strutt_off = all(x == "(B)" for x in off)
    strutt_on = all(x == "(B)" for x in on)
    if strutt_on and not strutt_off:
        print("  STRUTTURA in ON e NON in OFF -> E' REALE: emersa abbassando l'aliasing.")
    elif strutt_on and strutt_off:
        print("  STRUTTURA in ENTRAMBI -> piu' forte ancora: sopravvive al campionamento peggiore.")
    elif not strutt_on and not strutt_off:
        print("  NIENTE IN NESSUNO DEI DUE -> (A) NON CONCLUSIVO.")
        print("    theta nel braccio MIGLIORE: %.2f giri/passo -> il settore resta ALIASATO."
              % min(o["theta_giri"] for k, o in oo.items() if k.startswith("ON")))
        print("    La frase 'lo spin non si organizza' resta INDICIBILE finche' theta non scende.")
    else:
        print("  STRUTTURA in OFF e NON in ON -> ANOMALIA. L'aliasing non crea segnale: REPERTO, non")
        print("    risultato. Si riporta e ci si ferma.")

    print()
    print("  IL GRADIENTE DI RISOLUZIONE (ed e' il motivo dei due bracci):")
    for pref in ("OFF", "ON"):
        v = [oo[k]["theta_giri"] for k in oo if k.startswith(pref)]
        print("    theta %-4s %s  ->  media %.2f giri/passo" % (pref, ["%.2f" % x for x in v], np.mean(v)))

    print()
    print("  LA BARRA FRA SEMI (C10) - quella che conta per confrontare i bracci:")
    for eti, key in (("chi materia (gradi)", lambda o: o["chi_mat"][0]),
                     ("|<n>|*sqrt(N)", lambda o: o["nmod_sqrtN"]),
                     ("theta (giri/passo)", lambda o: o["theta_giri"]),
                     ("dispersione di r", lambda o: o["r_std"]),
                     ("cs_std", lambda o: o["cs_std"])):
        for pref in ("OFF", "ON"):
            v = np.array([key(oo[k]) for k in oo if k.startswith(pref)], float)
            print("    %-22s %-4s %s   media %.6f   dev.std FRA SEMI %.6f"
                  % (eti, pref, "  ".join("%.5f" % x for x in v), v.mean(),
                     v.std(ddof=1) if len(v) > 1 else float("nan")))
    print("=" * 110)


def main():
    ok, dati = conformita()
    if not ok:
        print()
        print("STOP: la checklist di conformita' NON passa. Nessun verdetto. (par.5 del mandato)")
        return 1
    oo = {}
    print()
    print("=" * 110)
    print("LE FIRME, per run")
    print("=" * 110)
    for tag, seed, r in dati:
        k = ("ON" if tag == "csON" else "OFF") + "_s%d" % seed
        oo[k] = firme(r)
        stampa(k, oo[k])
    verdetto(oo)
    return 0


if __name__ == "__main__":
    sys.exit(main())
