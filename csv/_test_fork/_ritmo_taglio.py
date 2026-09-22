# -*- coding: utf-8 -*-
"""A1 -- LA MISURA, PRIMA DELLA CORREZIONE. Quante volte `ritmo()` attraversa il taglio a +-pi.

Mandato di Luca, 2026-09-22. **NESSUNA MODIFICA AL SIMULATORE**: questo strumento avvolge
`Rete.ritmo` dall'esterno e misura. Il flag della correzione NON esiste ancora.

IL DIFETTO, verificato dall'algebra e non supposto (`:2584-2585`):
    a      = np.angle(_ps[:,0]) - np.angle(_psp[:,0])      -> a in (-2pi, 2pi]
    signed = ((a + 2pi) % (4pi) - 2pi) / DT
  Per `a` in (-2pi, 2pi) quel wrap **E' L'IDENTITA'**: non avvolge niente.
  Il wrap GIUSTO per una differenza di OSSERVABILI e' `((a + pi) % 2pi) - pi`.
  CASO: fase da `pi-0.05` a `-pi+0.05` (avanza di 0.1) -> 2pi: **+0.1** ; 4pi: **-6.183**.

E LA CATENA A VALLE, letta dal codice (`:2626-2645`):
    med  = median(|f|) del passo PRECEDENTE          f = signed (o |signed|)
    x    = f / med
    r    = x/sqrt(1+x^2) + 1e-6                      SATURA a ~1 per x -> inf
    r_n  = r / (1/sqrt(2) + 1e-6)                    -> satura a ~1.4142
  **QUINDI `r` NON HA UN CLIP A `1e6`.** Ha un TETTO a `~1.4142` e un PAVIMENTO a `~1.4142e-6`
  *(il `+1e-6` additivo)*. **Il rapporto `max/min = 1.000e+06` e' `1/1e-6` PER COSTRUZIONE**, e
  chiamarlo "clip a 1e6" era MIO ERRORE (`Z110`): si corregge nella relazione.

  **DUE ESTREMI, NON UNO:**
    * `r` al TETTO  (~1.4142)    <- `|f|` enorme: e' cio' che il taglio produce;
    * `r` al PAVIMENTO (~1.4e-6) <- `|f| ~ 0`. **E il taglio ci arriva per via INDIRETTA:**
      gonfia `median(|f|)`, quindi abbassa `x` di TUTTI gli altri.

I CRITERI, SCRITTI PRIMA DI VEDERE I NUMERI:
  (1) **FREQUENZA.** Se la frazione di nodi con `|a| > pi` e' **ZERO su tutti i passi**, il
      difetto e' **INERTE in questa scena** e si dice cosi'. Altrimenti si riportano media e
      massimo per passo.
  (2) **ARRICCHIMENTO AL TETTO.** Sia `f_a` la frazione di nodi con `|a| > pi` nel passo, e
      `f_a|tetto` la stessa frazione RISTRETTA ai nodi con `r` al tetto.
      **Sotto ipotesi nulla `f_a|tetto = f_a`.** Il difetto SPIEGA il tetto se
      `f_a|tetto >= 5 * f_a` **e** `f_a|tetto >= 0.5`. Fra `1x` e `5x`: **contribuisce ma non
      spiega**, e si scrive cosi'.
  (3) **EFFETTO SUL GAUGE.** Si riporta `median(|f|)` col taglio e `median(|f|)` che si sarebbe
      avuto col wrap a 2pi, **sullo stesso passo**. Se il rapporto e' `~1`, il taglio non muove
      il gauge e (2) e' tutta la storia. **Questo si calcola SENZA cambiare la dinamica:** e' una
      lettura parallela, non un secondo ramo.

  ⚠ **LIMITE DICHIARATO PRIMA:** il ramo 2pi si calcola **sui valori del ramo 4pi**, cioe' su una
    traiettoria prodotta dal difetto. **Dice cosa sarebbe successo IN QUEL PASSO, non cosa
    succede in un run corretto.** Quello lo dira' la prova a 600 passi col flag.

SOLA LETTURA sul simulatore: `ritmo()` e' avvolto e il valore restituito **non e' toccato**.
ASCII PURO.
"""
import io
import os
import runpy
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, RADICE)
DRIVER = os.path.join(RADICE, "csv", "_test_fork", "_scena_video.py")
DEST = os.path.join(RADICE, "csv", "_test_fork", "_ritmo_taglio")
OUT = os.path.join(DEST, "REFERTO.md")
COMUNE = ["--sep=4.0", "--serie=20", "--chi-basc=on", "--chi-coop=on", "--scala-min=off",
          "--coes-adim=on", "--peq-esatto=on", "--peq-nascita-locale=on",
          "--scala-min-passo=on", "--coes-causale=on", "--anom-simm=on", "--invarianti=on"]
FRAME = 20
for _a in sys.argv[1:]:
    if _a.startswith("--frame="):
        FRAME = int(_a.split("=", 1)[1])


def w2(a):
    """Il wrap GIUSTO per una differenza di OSSERVABILI: periodo 2pi."""
    return (a + np.pi) % (2 * np.pi) - np.pi


def w4(a):
    """Il wrap SCRITTO nel codice: su (-2pi, 2pi) e' l'identita'."""
    return (a + 2 * np.pi) % (4 * np.pi) - 2 * np.pi


def collaudo(W):
    """`P1-sexies`: i due wrap su casi a risposta NOTA, e quello che DEVE sbagliare."""
    W("COLLAUDO (`P1-sexies`), PRIMA di misurare\n" + "-" * 96 + "\n")
    e = []
    # il caso del mandato: la fase avanza di 0.1 attraversando il taglio
    a = (-np.pi + 0.05) - (np.pi - 0.05)
    v2, v4 = float(w2(a)), float(w4(a))
    ok1 = abs(v2 - 0.1) < 1e-12
    W("K1 attraversa il taglio, avanzo VERO +0.1 -> wrap 2pi da' %+.6f -> %s\n"
      % (v2, "OK" if ok1 else "*** NO ***"))
    ok2 = abs(v4 - (a)) < 1e-12 and abs(v4 + 6.1832) < 1e-3
    W("K2 IL CASO CHE DEVE SBAGLIARE: lo stesso, col wrap 4pi -> %+.6f\n" % v4)
    W("     e' L'IDENTITA' su `a` (%+.6f), cioe' NON AVVOLGE -> %s\n"
      % (a, "OK: il difetto e' riprodotto" if ok2 else "*** il difetto NON si riproduce ***"))
    e += [ok1, ok2]
    # identita' su tutto (-2pi, 2pi): il wrap 4pi non tocca NIENTE
    g = np.linspace(-2 * np.pi + 1e-9, 2 * np.pi - 1e-9, 100001)
    ok3 = float(np.max(np.abs(w4(g) - g))) < 1e-9
    W("K3 il wrap 4pi su TUTTO (-2pi, 2pi): max|w4(a) - a| = %.3e -> %s\n"
      % (float(np.max(np.abs(w4(g) - g))), "OK: identita' ovunque" if ok3 else "*** NO ***"))
    ok4 = float(np.max(np.abs(w2(g)))) <= np.pi + 1e-9
    W("K4 il wrap 2pi porta TUTTO dentro [-pi, pi]: max = %.6f -> %s\n"
      % (float(np.max(np.abs(w2(g)))), "OK" if ok4 else "*** NO ***"))
    e += [ok3, ok4]
    # l'arricchimento: due casi a risposta nota
    tetto = np.array([True, True, True, True, False, False, False, False])
    tag = np.array([True, True, True, True, False, False, False, False])
    fa = float(np.mean(tag)); fat = float(np.mean(tag[tetto]))
    ok5 = (fat == 1.0) and (fa == 0.5)
    W("K5 arricchimento PERFETTO (tutti i tagliati sono al tetto): f_a=%.2f f_a|tetto=%.2f -> %s\n"
      % (fa, fat, "OK" if ok5 else "*** NO ***"))
    tag2 = np.array([True, False, True, False, True, False, True, False])
    fa2 = float(np.mean(tag2)); fat2 = float(np.mean(tag2[tetto]))
    ok6 = abs(fat2 - fa2) < 1e-12
    W("K6 IL CASO CHE DEVE DARE ZERO EFFETTO: tagliati sparsi a caso -> f_a=%.2f "
      "f_a|tetto=%.2f\n" % (fa2, fat2))
    W("     uguali -> nessun arricchimento -> %s\n"
      % ("OK: il criterio non inventa un effetto" if ok6 else "*** ne inventa uno ***"))
    e += [ok5, ok6]
    ok = all(e)
    W("-" * 96 + "\n  -> %s\n\n" % ("i criteri PASSANO" if ok else "*** NON PASSANO ***"))
    return ok


def main():
    W = sys.stdout.write
    if not collaudo(W):
        return 1
    try:
        os.makedirs(DEST)
    except OSError:
        pass
    for f in os.listdir(DEST):
        if f.endswith(".pkl.gz"):
            os.remove(os.path.join(DEST, f))

    os.chdir(RADICE)
    import soliton_simulator as S
    dati = []
    orig = S.Rete.ritmo

    def avvolto(self):
        """PURE-READ: calcola cio' che serve e restituisce IL VALORE ORIGINALE, intatto."""
        _ps = getattr(self, "psi_spin", None)
        _psp = getattr(self, "_psi_spin_prec", None)
        r = orig(self)
        try:
            n = self.n
            if (S.CAMPO_SPINORIALE and _ps is not None and _psp is not None
                    and len(_ps) == n and len(_psp) == n and n > 1):
                a = np.angle(_ps[:, 0]) - np.angle(_psp[:, 0])
                f4 = np.abs(w4(a)) / S.DT
                f2 = np.abs(w2(a)) / S.DT
                rr = np.asarray(r, float)[:n] if r is not None else np.ones(n)
                tetto = rr > 1.4142
                pavim = rr < 1.0e-5
                tag = np.abs(a) > np.pi
                dati.append(dict(
                    n=int(n), f_a=float(np.mean(tag)), n_tag=int(np.sum(tag)),
                    f_a_tetto=(float(np.mean(tag[tetto])) if tetto.any() else float("nan")),
                    q_tetto=float(np.mean(tetto)), q_pavim=float(np.mean(pavim)),
                    med4=float(np.median(f4)), med2=float(np.median(f2)),
                    rmin=float(np.min(rr)), rmax=float(np.max(rr))))
        except Exception as e:
            dati.append(dict(errore=str(e)))
        return r
    S.Rete.ritmo = avvolto

    sys.argv = ["_scena_video.py", str(FRAME), DEST] + COMUNE
    t0 = time.time()
    runpy.run_path(DRIVER, run_name="__main__")
    dt = time.time() - t0

    buoni = [d for d in dati if "errore" not in d]
    o = io.open(OUT, "w", encoding="utf-8", newline="\n")
    Wf = o.write
    Wf("# `A1` — IL TAGLIO A `+-pi` IN `ritmo()`: **la misura, PRIMA della correzione**\n\n")
    Wf("> Generato da `csv/_test_fork/_ritmo_taglio.py`. **Il simulatore NON e' toccato:**\n")
    Wf("> `ritmo()` e' avvolto e il valore restituito **non viene modificato**.\n")
    Wf("> %d frame (= %d passi), %.1f s, %d chiamate utili su %d.\n\n"
       % (FRAME, FRAME * 6, dt, len(buoni), len(dati)))
    if not buoni:
        Wf("**NESSUNA CHIAMATA UTILE:** il ramo spinoriale non e' stato raggiunto. "
           "**Si dichiara, non si conclude.**\n")
        o.close(); print(io.open(OUT, encoding="utf-8").read()); return 1

    def col(k):
        return np.asarray([d[k] for d in buoni], float)

    fa = col("f_a"); fat = col("f_a_tetto")
    Wf("## (1) FREQUENZA — quante volte si attraversa il taglio\n\n")
    Wf("| | valore |\n|---|--:|\n")
    Wf("| chiamate misurate | %d |\n" % len(buoni))
    Wf("| **frazione di nodi con `|a| > pi`**, media | **%.4e** |\n" % float(np.mean(fa)))
    Wf("| la stessa, massimo | %.4e |\n" % float(np.max(fa)))
    Wf("| chiamate con **almeno un** attraversamento | %d su %d |\n"
       % (int(np.sum(col("n_tag") > 0)), len(buoni)))
    Wf("| nodi tagliati per chiamata, media | %.2f |\n" % float(np.mean(col("n_tag"))))
    Wf("| nodi tagliati per chiamata, massimo | %d |\n" % int(np.max(col("n_tag"))))

    Wf("\n## (2) ARRICCHIMENTO AL TETTO\n\n")
    Wf("> Sotto **ipotesi nulla** `f_a|tetto = f_a`. Il difetto **SPIEGA** il tetto se\n")
    Wf("> `f_a|tetto >= 5 * f_a` **e** `f_a|tetto >= 0.5`.\n\n")
    Wf("| | valore |\n|---|--:|\n")
    Wf("| quota di nodi al TETTO (`r > 1.4142`), media | %.4e |\n" % float(np.mean(col("q_tetto"))))
    Wf("| quota di nodi al PAVIMENTO (`r < 1e-5`), media | %.4e |\n"
       % float(np.mean(col("q_pavim"))))
    Wf("| `f_a` medio *(il nullo)* | **%.4e** |\n" % float(np.mean(fa)))
    _fat = fat[np.isfinite(fat)]
    Wf("| **`f_a|tetto` medio** | **%s** |\n"
       % ("%.4e" % float(np.mean(_fat)) if _fat.size else "— nessun nodo al tetto"))
    if _fat.size and float(np.mean(fa)) > 0:
        arr = float(np.mean(_fat)) / float(np.mean(fa))
        Wf("| **arricchimento** | **%.2f x** |\n" % arr)
        if arr >= 5.0 and float(np.mean(_fat)) >= 0.5:
            v = "**SPIEGA il tetto**"
        elif arr > 1.2:
            v = "**contribuisce, NON spiega**"
        else:
            v = "**non c'e' arricchimento**"
        Wf("\n**ESITO DEL CRITERIO (2): %s.**\n" % v)
    else:
        Wf("\n**ESITO DEL CRITERIO (2): NON CALCOLABILE** *(nessun nodo al tetto, oppure "
           "`f_a = 0`)*. **Si dichiara, non si conclude.**\n")

    Wf("\n## (3) EFFETTO SUL GAUGE `median(|f|)`\n\n")
    m4 = col("med4"); m2 = col("med2")
    rap = m4 / np.maximum(m2, 1e-300)
    Wf("| | valore |\n|---|--:|\n")
    Wf("| `median(|f|)` col wrap **4pi** *(quello in vigore)*, mediana | %.6e |\n"
       % float(np.median(m4)))
    Wf("| `median(|f|)` col wrap **2pi** *(quello giusto)*, mediana | %.6e |\n"
       % float(np.median(m2)))
    Wf("| **rapporto `4pi / 2pi`**, mediana | **%.6f** |\n" % float(np.median(rap)))
    Wf("| lo stesso, massimo | %.6f |\n" % float(np.max(rap)))
    Wf("\n⚠ **LIMITE DICHIARATO PRIMA:** il ramo `2pi` e' calcolato **sui valori del ramo "
       "`4pi`**, cioe' su una traiettoria prodotta dal difetto. **Dice cosa sarebbe successo IN "
       "QUEL PASSO, non cosa succede in un run corretto.**\n")
    Wf("\n## E `r` NON HA UN CLIP A `1e6`\n\n")
    Wf("Dal codice (`:2643-2645`): `r = x/sqrt(1+x^2) + 1e-6`, poi `/(1/sqrt(2) + 1e-6)`.\n")
    Wf("**Tetto `~1.4142`, pavimento `~1.4142e-6`: il rapporto `max/min = 1e+06` e' `1/1e-6` "
       "PER COSTRUZIONE.**\n\n")
    Wf("| | misurato |\n|---|--:|\n")
    Wf("| `min(r)` sul run | %.6e |\n" % float(np.min(col("rmin"))))
    Wf("| `max(r)` sul run | %.6e |\n" % float(np.max(col("rmax"))))
    Wf("\n**LIMITI: UN seme, UNA scena, %d passi.**\n" % (FRAME * 6))
    o.close()
    print(io.open(OUT, encoding="utf-8").read())
    return 0


if __name__ == "__main__":
    sys.exit(main())
