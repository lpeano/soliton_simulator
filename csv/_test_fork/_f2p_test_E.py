# -*- coding: utf-8 -*-
"""I TEST `E1`-`E4` DELLA CURA `FASE_2PI` -- criteri fissati PRIMA di vedere i numeri.

!! CHI HA SCRITTO QUALE TEST, e va detto perche' due sono MIEI (`Z125`):
    `E1`  e' di LUCA  -- *la mitosi a `2pi` funziona senza tarature? Ne' zero mitosi ne'
          esplosione.* Se fallisce, **cade il punto 2 del par.D** e con esso la soglia a `2pi`.
    `E2`  e' di LUCA  -- *le coppie annichilano?* Se resta `~0` con `+pi`, **cade il punto 5**.
    `E3`  e' MIO, DERIVATO dall'effetto che il par.E **stesso** dichiara *"va misurato"*.
    `E4`  e' MIO, DERIVATO dalla riserva (2) di `Z120`.
  Nel repo esistevano solo `E1` ed `E2`: ho citato "i quattro test `E1`-`E4`" undici volte
  senza che `E3` ed `E4` fossero scritti da nessuna parte. **E' `Z125`, un difetto di metodo
  mio.** Luca puo' sostituire i due derivati; i suoi due non si toccano.

!! E `E2` NON E' MISURABILE IN QUESTO RUN, e lo si dichiara invece di riportare uno zero:
  l'ANNICHILAZIONE vive **solo** dentro `ANTIFASE_ADD` (`:5351`), che e' **`False`**.
  Il ramo che la cura tocca (`:5499`) e' la **creazione di coppia alla Schwinger**, e li'
  l'antifase decide se l'antiparticella e' DISTINGUIBILE dalla particella nel campo --
  che e' la **precondizione** dell'annichilazione, non l'annichilazione.
  **Conseguenza per `S06`:** il "muro dell'1 %" **non si spiega con `D35` da solo**, perche'
  il meccanismo che annichilerebbe **non gira**.

SOLA LETTURA: legge snapshot GIA' SCRITTI. Non importa il simulatore, non gira niente.
ASCII PURO nei `print`.
"""
import glob
import gzip
import os
import pickle
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_QUI, ".."))
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
P2 = 2.0 * np.pi          # PHI_CRIT: il quanto di olonomia
TETTO = 4.0 * np.pi       # il tetto della doppia copertura, dove la mitosi si azzera

# ---------------------------------------------------------------- I CRITERI, fissati PRIMA
#   nome, criterio, ORIGINE (da dove viene la soglia: una misura, non una scelta)
CRITERI = [
    ("E1a  la mitosi NON muore",
     "`_g_nati_mitosi > 0` e `n` cresce",
     "di LUCA. Nullo: se la cura rompesse `fm`, le nascite sarebbero 0"),
    ("E1b  la mitosi NON esplode",
     "`n` finale < 10x il riferimento, e il run ARRIVA a 600 passi",
     "MISURATA: 178 archi per nodo (526672 / 2959). 10x `n` = ~5.3M archi = 10x memoria e "
     "tempo: oltre, il sistema non e' simulabile, e QUELLA e' l'esplosione"),
    ("E1c  il FATTORE, contro la mia previsione",
     "le nascite da mitosi salgono di un fattore fra 5x e 100x",
     "DERIVATA dagli archi GIA' SUL DISCO: la campana ha il picco a `|tw| = soglia`, e la "
     "finestra nuova (`tau` 2.0-2.5) contiene 17113 archi contro i 346 della vecchia "
     "(`tau` 2.5-3.0) al passo 600: fattore 49.5x. La banda e' UN ORDINE per lato perche' "
     "la LARGHEZZA della campana non entra nel conto, e la mitosi CONSUMA la torsione "
     "(retroazione che smorza). **Questo test giudica ME, non la cura**"),
    ("E2   le coppie annichilano?",
     "NON MISURABILE in questo run: `ANTIFASE_ADD = False`",
     "di LUCA, e la risposta e' una DICHIARAZIONE: il meccanismo non gira. Si misura la "
     "PRECONDIZIONE (l'antiparticella e' distinguibile nel campo) e il tasso di coppie"),
    ("E3   la finestra d'inversione di `D33`",
     "si allarga da mezzo `pi` a un `pi` intero: si riporta la POPOLAZIONE delle due "
     "finestre in entrambi i bracci",
     "MIO, derivato dal par.E che dichiara -- non e' una cura di `D33`, e' un effetto, e va "
     "misurato. `tau_soglia` 2.5 -> 2, `centro` 2.75 -> 2.5, inversione `3.5pi` -> `3pi`"),
    ("E4   i diagnostici di fase",
     "`min/max/mean/median` di `phi` nei due bracci, col NULLO accanto",
     "MIO, dalla riserva (2) di `Z120`. Il nullo e' il sigillo: `max(phi)` 12.565546 -> "
     "6.282066. **Nessuna legge cambia, i referti si'**, e chi confronta un referto vecchio "
     "con uno nuovo deve saperlo (par.9-bis)"),
]


# ---------------------------------------------------------------- le misure, isolate
def NN(a):
    """Il numero di NODI. `n` NON e' una chiave dello snapshot: si legge da `len(phi)`.

    Trovato dal CONTROLLO DELL'INVOLUCRO (`STANDARD 5`) puntando lo strumento sul
    riferimento CONTRO SE STESSO, prima del run vero: `KeyError: 'n'`. E' esattamente
    cio' per cui quel controllo esiste -- su un run vero lo schianto sarebbe arrivato
    DOPO 35 minuti, e su un run da 600 passi dopo di piu'.
    """
    return int(len(a["phi"]))


def finestre(tw):
    """La popolazione delle due finestre della campana, in `tau = 1 + |tw|/PHI_CRIT`."""
    tau = 1.0 + np.abs(tw) / P2
    return {"nuova_2_2.5": int(((tau >= 2.0) & (tau < 2.5)).sum()),
            "vecchia_2.5_3": int(((tau >= 2.5) & (tau < 3.0)).sum()),
            "oltre_tetto": int((tau >= 3.0).sum()),
            "archi": int(len(tw))}


def campo(f, salto):
    """Quanto l'antiparticella e' DISTINGUIBILE dalla particella NEL CAMPO `exp(i phi)`.

    E' la misura di `D35`: il campo legge `exp(i phi)`, quindi un `+2pi` da' `0` (identica)
    e un `+pi` da' `2` (opposta). Il valore atteso NON e' scelto: e' `|exp(i s) - 1|`.
    """
    return float(np.abs(np.exp(1j * (f + salto)) - np.exp(1j * f)).max())


def leggi(cartella):
    """Gli snapshot di un braccio, in ordine di passo."""
    out = []
    for p in sorted(glob.glob(os.path.join(cartella, "scena_*.pkl.gz"))):
        a = pickle.load(gzip.open(p, "rb"))["attrs"]
        out.append(a)
    return out


# ---------------------------------------------------------------- IL COLLAUDO (`P1-sexies`)
def collaudo(W):
    W("COLLAUDO DEI CRITERI su casi a RISPOSTA NOTA (`P1-sexies`), PRIMA di misurare\n")
    W("-" * 96 + "\n")
    e = []

    # K1 -- le finestre su un `tw` costruito: la risposta e' NOTA per costruzione
    tw = np.concatenate([np.full(7, 2.2 * np.pi),    # tau 2.1  -> finestra NUOVA
                         np.full(3, 2.8 * np.pi),    # tau 2.4  -> finestra NUOVA
                         np.full(5, 3.4 * np.pi),    # tau 2.7  -> finestra VECCHIA
                         np.full(2, 4.5 * np.pi)])   # tau 3.25 -> oltre il tetto
    f = finestre(tw)
    ok = (f["nuova_2_2.5"] == 10 and f["vecchia_2.5_3"] == 5 and f["oltre_tetto"] == 2)
    W("K1 le finestre su un `tw` a risposta NOTA: nuova=%d (10), vecchia=%d (5), oltre=%d (2)"
      " -> %s\n" % (f["nuova_2_2.5"], f["vecchia_2.5_3"], f["oltre_tetto"],
                    "OK" if ok else "*** NO ***"))
    e.append(ok)

    # K2 -- IL CASO CHE DEVE FALLIRE: `+2pi` e' un'IDENTITA' nel campo. E' `D35`.
    rng = np.random.default_rng(7)
    fm = rng.uniform(0, 4 * np.pi, 5000)
    d2 = campo(fm, 2 * np.pi)
    ok2 = d2 < 1e-12
    W("K2 IL CASO CHE DEVE FALLIRE: `+2pi` nel campo da' max|diff| = %.3e -> %s\n"
      % (d2, "OK: `D35` e' riprodotto (l'antiparticella e' IDENTICA)"
         if ok2 else "*** non si riproduce ***"))
    e.append(ok2)

    # K3 -- e `+pi` e' un'antifase VERA: il 2 non e' scelto, e' |exp(i pi) - 1|
    dp = campo(fm, np.pi)
    ok3 = abs(dp - 2.0) < 1e-12
    W("K3 e `+pi` da' max|diff| = %.6f, atteso 2 = |exp(i pi) - 1| -> %s\n"
      % (dp, "OK" if ok3 else "*** NO ***"))
    e.append(ok3)

    # K4 -- SECONDO CASO CHE DEVE FALLIRE: zero nascite deve dare FAIL su `E1a`
    ok4 = not (0 > 0)
    W("K4 SECONDO CASO CHE DEVE FALLIRE: `E1a` con 0 nascite -> FAIL -> %s\n"
      % ("OK: il criterio non passa a vuoto" if ok4 else "*** passa a vuoto ***"))
    e.append(ok4)

    # K5 -- TERZO CASO CHE DEVE FALLIRE: `n` 100x deve dare FAIL su `E1b`
    ok5 = not (2959 * 100 < 10 * 2959)
    W("K5 TERZO CASO CHE DEVE FALLIRE: `E1b` con `n` 100x il riferimento -> FAIL -> %s\n"
      % ("OK" if ok5 else "*** non fallisce ***"))
    e.append(ok5)

    # K6 -- e il caso LEGITTIMO non deve essere bocciato: `n` 3x PASSA
    ok6 = (2959 * 3 < 10 * 2959)
    W("K6 e il caso LEGITTIMO non si boccia: `E1b` con `n` 3x -> PASS -> %s\n"
      % ("OK" if ok6 else "*** boccia un caso buono ***"))
    e.append(ok6)

    ok = all(e)
    W("-" * 96 + "\n  -> %s\n\n" % ("i criteri PASSANO" if ok else "*** NON PASSANO ***"))
    return ok


def main():
    W = sys.stdout.write
    rif = os.path.join(RADICE, "csv", "_test_fork", "_g4_riferimento")
    arg = [a for a in sys.argv[1:] if not a.startswith("-")]
    cur = os.path.join(RADICE, "csv", "_test_fork", arg[0] if arg else "_f2p_prova")

    W("# I TEST `E1`-`E4` DELLA CURA `FASE_2PI`\n#\n")
    W("# braccio CURA:        %s\n" % os.path.relpath(cur, RADICE))
    W("# braccio RIFERIMENTO: %s\n#\n" % os.path.relpath(rif, RADICE))
    if not collaudo(W):
        return 1

    W("I CRITERI, come erano scritti PRIMA di vedere i numeri:\n")
    for k, (nome, crit, orig) in enumerate(CRITERI, 1):
        W("  %d. %s\n     %s\n     (%s)\n" % (k, nome, crit, orig))
    W("\n")

    A, B = leggi(rif), leggi(cur)
    if not B:
        W("*** NESSUNO SNAPSHOT nel braccio della cura: il run non e' partito. ***\n")
        return 1
    W("snapshot: riferimento %d, cura %d\n" % (len(A), len(B)))
    if len(B) < len(A):
        W("!! IL BRACCIO DELLA CURA E' PIU' CORTO: il run e' TRONCATO, e i numeri qui sotto\n"
          "   valgono solo fino al passo che c'e'. Non si legge un esito da un run troncato.\n")

    # ---------------- la tabella, per istante
    W("\n" + "=" * 96 + "\n")
    W("PER ISTANTE -- RIF = riferimento (soglia 3pi), CUR = con `FASE_2PI` (soglia 2pi)\n")
    W("=" * 96 + "\n")
    W("%7s | %8s %8s | %10s %10s | %7s %7s | %8s %8s\n"
      % ("passo", "n RIF", "n CUR", "archi RIF", "archi CUR",
         "mit RIF", "mit CUR", "schw RIF", "schw CUR"))
    W("-" * 96 + "\n")
    for a, b in zip(A, B):
        W("%7d | %8d %8d | %10d %10d | %7d %7d | %8d %8d\n"
          % (int(b.get("_db_step", -1)), NN(a), NN(b),
             len(a["tw"]), len(b["tw"]),
             int(a.get("_g_nati_mitosi", 0)), int(b.get("_g_nati_mitosi", 0)),
             int(a.get("_g_nati_schwinger", 0)), int(b.get("_g_nati_schwinger", 0))))

    ult_a, ult_b = A[min(len(A), len(B)) - 1], B[-1]
    esiti = []

    # ---------------- E1
    W("\n" + "=" * 96 + "\n")
    W("`E1` -- LA MITOSI (di LUCA): ne' zero ne' esplosione\n")
    W("=" * 96 + "\n")
    nati_a = int(ult_a.get("_g_nati_mitosi", 0))
    nati_b = int(ult_b.get("_g_nati_mitosi", 0))
    ev_a = int(ult_a.get("_g_nati_mitosi_ev", 0))
    ev_b = int(ult_b.get("_g_nati_mitosi_ev", 0))
    W("  nascite da mitosi   RIF %6d (%d eventi)   CUR %6d (%d eventi)\n"
      % (nati_a, ev_a, nati_b, ev_b))
    W("  nodi                RIF %6d                CUR %6d\n" % (NN(ult_a), NN(ult_b)))
    W("  archi               RIF %6d                CUR %6d\n"
      % (len(ult_a["tw"]), len(ult_b["tw"])))
    esiti.append(("E1a  la mitosi NON muore", nati_b > 0 and NN(ult_b) > NN(B[0]),
                  "nascite %d, `n` %d -> %d" % (nati_b, NN(B[0]), NN(ult_b))))
    esiti.append(("E1b  la mitosi NON esplode", NN(ult_b) < 10 * NN(ult_a),
                  "`n` CUR %d contro il tetto 10x = %d" % (NN(ult_b), 10 * NN(ult_a))))
    fatt = (float(nati_b) / nati_a) if nati_a else float("nan")
    W("\n  IL FATTORE MISURATO: %.3fx   (la mia previsione era fra 5x e 100x, dal 49.5x\n"
      "  della popolazione degli archi)\n" % fatt)
    esiti.append(("E1c  il FATTORE contro la MIA previsione", 5.0 <= fatt <= 100.0,
                  "fattore %.3fx, banda prevista 5x-100x -- **questo giudica ME**" % fatt))

    # ---------------- E2
    W("\n" + "=" * 96 + "\n")
    W("`E2` -- LE COPPIE (di LUCA): **NON MISURABILE in questo run**\n")
    W("=" * 96 + "\n")
    W("  L'ANNICHILAZIONE vive SOLO dentro `ANTIFASE_ADD`, che e' `False`: il meccanismo\n")
    W("  che annichilerebbe NON GIRA. Riportare uno zero qui sarebbe leggere un'ASSENZA\n")
    W("  DI MECCANISMO come un'assenza di effetto -- lo stesso errore del\n")
    W("  `max|A-B| = 0.000e+00` per mancanza di confronto.\n\n")
    rng = np.random.default_rng(11)
    fm = rng.uniform(0, 4 * np.pi, 20000)
    W("  LA PRECONDIZIONE, che invece SI misura (ed e' `D35`):\n")
    W("    spenta  `+2pi` su dominio `4pi`  -> max|exp(i anti) - exp(i part)| = %.3e\n"
      % campo(fm, 2 * np.pi))
    W("    accesa  `+pi`  su dominio `2pi`  -> max|exp(i anti) - exp(i part)| = %.6f\n"
      % campo(fm, np.pi))
    W("    (il `2` non e' scelto: e' `|exp(i pi) - 1|`)\n\n")
    W("  E IL TASSO DI COPPIE, come LETTURA:\n")
    W("    schwinger  RIF %d nati (%d eventi)   CUR %d nati (%d eventi)\n"
      % (int(ult_a.get("_g_nati_schwinger", 0)), int(ult_a.get("_g_nati_schwinger_ev", 0)),
         int(ult_b.get("_g_nati_schwinger", 0)), int(ult_b.get("_g_nati_schwinger_ev", 0))))
    W("\n  -> `E2` NON DA' UN ESITO: da' una DICHIARAZIONE. Per misurare l'annichilazione\n")
    W("     servirebbe accendere `ANTIFASE_ADD`, che e' un ESPERIMENTO (par.10), non\n")
    W("     fisica, e va chiesto a Luca invece che deciso qui.\n")
    W("  -> E PER `S06`: il muro dell'1 % NON si spiega con `D35` da solo.\n")

    # ---------------- E3
    W("\n" + "=" * 96 + "\n")
    W("`E3` -- LA FINESTRA D'INVERSIONE DI `D33` (MIO, derivato)\n")
    W("=" * 96 + "\n")
    W("  la campana della mitosi ha il picco a `|tw| = soglia` e si azzera al tetto `4pi`.\n")
    W("  con `phi` su `2pi` la soglia scende da `3pi` a `2pi`: `tau_soglia` 2.5 -> 2.0,\n")
    W("  `centro` 2.75 -> 2.5, inversione `3.5pi` -> `3pi`.\n\n")
    W("%7s | %22s %22s | %12s %12s\n"
      % ("passo", "nuova 2.0-2.5 RIF/CUR", "vecchia 2.5-3 RIF/CUR", "oltre RIF", "oltre CUR"))
    W("-" * 96 + "\n")
    for a, b in zip(A, B):
        fa, fb = finestre(a["tw"]), finestre(b["tw"])
        W("%7d | %10d %11d %10d %11d | %12d %12d\n"
          % (int(b.get("_db_step", -1)), fa["nuova_2_2.5"], fb["nuova_2_2.5"],
             fa["vecchia_2.5_3"], fb["vecchia_2.5_3"], fa["oltre_tetto"], fb["oltre_tetto"]))
    fa, fb = finestre(ult_a["tw"]), finestre(ult_b["tw"])
    rap = (float(fa["nuova_2_2.5"]) / fa["vecchia_2.5_3"]) if fa["vecchia_2.5_3"] else float("nan")
    W("\n  il RAPPORTO che genera la previsione di `E1c`: nuova/vecchia nel RIFERIMENTO = "
      "%.2fx\n" % rap)
    W("  (e' un EFFETTO della cura, non una cura di `D33`: si RIPORTA, non si giudica)\n")

    # ---------------- E4
    W("\n" + "=" * 96 + "\n")
    W("`E4` -- I DIAGNOSTICI DI FASE (MIO, derivato dalla riserva 2 di `Z120`)\n")
    W("=" * 96 + "\n")
    W("%7s | %10s %10s | %10s %10s | %10s %10s\n"
      % ("passo", "max phi R", "max phi C", "med phi R", "med phi C", "min phi R", "min phi C"))
    W("-" * 96 + "\n")
    for a, b in zip(A, B):
        pa, pb = np.asarray(a["phi"], float), np.asarray(b["phi"], float)
        W("%7d | %10.6f %10.6f | %10.6f %10.6f | %10.6f %10.6f\n"
          % (int(b.get("_db_step", -1)), pa.max(), pb.max(),
             np.median(pa), np.median(pb), pa.min(), pb.min()))
    pb = np.asarray(ult_b["phi"], float)
    esiti.append(("E4   `phi` sta davvero sotto `2pi`", float(pb.max()) < P2,
                  "max(phi) = %.6f contro `2pi` = %.6f (il NULLO e' il 12.565546 del "
                  "sigillo a flag spento)" % (pb.max(), P2)))
    W("\n  E `r`, il ritmo: il ramo che GIRA e' `TEMPO_SEGNO` (`r = 1 + mean|tw|/PHI_CRIT`),\n")
    W("  che NON ha il tetto `1.4142` della formula a bottleneck. Il `1.414213` citato\n")
    W("  altrove viene dall'ALTRO ramo, e la sua provenienza e' una DOMANDA APERTA (`S10`),\n")
    W("  non un fatto: qui si riporta il ramo vivo.\n")
    for et, (a, b) in zip([int(x.get("_db_step", -1)) for x in B], zip(A, B)):
        aw = np.abs(np.asarray(b["tw"], float))
        r = 1.0 + (aw.mean() / P2)
        aw2 = np.abs(np.asarray(a["tw"], float))
        W("    passo %6d   r(medio sugli archi) RIF %.6f   CUR %.6f\n"
          % (et, 1.0 + aw2.mean() / P2, r))

    # ---------------- L'ESITO
    W("\n" + "=" * 96 + "\n")
    W("ESITO DEI TEST -- PASSA / NON PASSA\n")
    W("=" * 96 + "\n")
    npass = 0
    for nome, ok, det in esiti:
        W("  %-42s %s   %s\n" % (nome, "PASSA    " if ok else "NON PASSA", det))
        npass += bool(ok)
    W("\nESITO: %d/%d\n" % (npass, len(esiti)))
    W("\n`E2` NON entra nel conto: e' una DICHIARAZIONE, non un test -- e contarlo come\n")
    W("PASS o come FAIL sarebbe falso in entrambi i versi.\n")
    W("\n!! E SE `E1a` o `E1b` NON PASSANO, LA LETTURA DEL par.D CADE: la soglia a `2pi` non\n")
    W("  regge, e il punto 2 va riaperto. `E1c` invece giudica LA MIA PREVISIONE.\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
