# -*- coding: utf-8 -*-
"""**LE DUE SCENE DELLA STRADA (ii)** -- massa = REGIONE A FASE COERENTE NEL VUOTO.

**Decisione di Luca, 2026-09-25.** Un vuoto **UNICO** seminato con `SEMINA_LAM` *(saturazione
esatta)* su una palla che contiene le tre regioni. **Le masse NON aggiungono nodi:** sono i nodi
del vuoto **dentro tre sfere**, a cui si assegna la **stessa fase**. **Zero numeri nuovi.**

**QUESTO STRUMENTO CALCOLA I NUMERI, NON LI STIMA:** la capienza viene dalla semina `RSA` vera
*(arresto derivato da `LAM`, Zhang-Torquato)*, e **quanti nodi cadono dentro le regioni** si
CONTA sulle posizioni prodotte.

**LA GEOMETRIA, e cosa è scelta e cosa è derivato:**

```
tre regioni su un cerchio di raggio `sep`  ->  distanza fra i CENTRI = sep*sqrt(3)  (corda 120')
intervallo fra i BORDI = sep*sqrt(3) - 2*r
  ** `intervallo = R_CONN` E' UNA SCELTA DI LUCA **, non una derivazione
raggio del VUOTO = sep + r + R_CONN      <- il minimo che contiene le tre regioni PIU' un
                                            guscio di R_CONN (il punto di una regione piu'
                                            lontano dall'origine sta a `sep + r`)
```

Sola lettura sul simulatore. ASCII puro.
"""
import io
import os
import re
import subprocess
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
DEST = os.path.join(_QUI, "_revisione", "SCENE_COERENTI.txt")
SEMI = (1, 2, 3, 4)

FIGLIO = r"""
import sys, re, numpy as np
sys.argv = ["soliton_simulator.py"]
import soliton_simulator as S
S.SEMINA_LAM = True
LAM = float(S.LAM); RC = float(S.R_CONN())
SQ3 = float(np.sqrt(3.0))

def _di(s):
    sys.stdout.write(s + chr(10)); sys.stdout.flush()

def semina(n, r, seed):
    net = S.Rete(seed)
    return net._semina_lam(n, r, (0.0, 0.0, 0.0))

def capienza(r, seed, ask=200000):
    net = S.Rete(seed)
    try:
        net._semina_lam(ask, r, (0.0, 0.0, 0.0)); return -1
    except SystemExit as ex:
        m = re.search(r"collocati\s*=\s*(\d+)", str(ex))
        return int(m.group(1)) if m else -2

def raggio_per(n, seed):
    lo, hi = 0.5, 40.0
    for _ in range(14):
        mid = 0.5 * (lo + hi)
        net = S.Rete(seed)
        try:
            net._semina_lam(n, mid, (0.0, 0.0, 0.0)); hi = mid
        except SystemExit:
            lo = mid
    return hi

_di("LAM %.6f RCONN %.6f" % (LAM, RC))

# --- (a) il raggio che contiene ~497 nodi
ra = [raggio_per(497, s) for s in SEMI]
RA = float(np.mean(ra))
_di("RA r = %.4f +- %.4f  (= %.3f LAM)  semi=%s" % (RA, float(np.std(ra)), RA / LAM,
                                                   ["%.3f" % x for x in ra]))
SEPA = (2.0 * RA + RC) / SQ3
VA = SEPA + RA + RC
_di("SCENA_A sep = %.4f   centri = %.4f   raggio_vuoto = %.4f  (= %.3f LAM)"
    % (SEPA, SEPA * SQ3, VA, VA / LAM))

# --- (b) sep = 4.0
SEPB = 4.0
RB = (SEPB * SQ3 - RC) / 2.0
VB = SEPB + RB + RC
_di("SCENA_B sep = %.4f   centri = %.4f   r_regione = %.4f   raggio_vuoto = %.4f  (= %.3f LAM)"
    % (SEPB, SEPB * SQ3, RB, VB, VB / LAM))

# --- il VUOTO: quanti nodi, e quanti cadono DENTRO le tre regioni
for eti, V, R_, SEP in (("A", VA, RA, SEPA), ("B", VB, RB, SEPB)):
    cap = [capienza(V, s) for s in SEMI]
    _di("VUOTO_%s raggio %.4f  capienza = %.1f +- %.1f  %s"
        % (eti, V, float(np.mean(cap)), float(np.std(cap)), cap))
    dentro, tot = [], []
    for s in SEMI:
        p = semina(int(np.mean(cap)) - 1, V, s)
        c = np.array([[SEP * np.cos(2 * np.pi * k / 3), SEP * np.sin(2 * np.pi * k / 3), 0.0]
                      for k in range(3)])
        m = np.zeros(len(p), bool)
        per_reg = []
        for k in range(3):
            mk = np.linalg.norm(p - c[k], axis=1) <= R_
            per_reg.append(int(mk.sum()))
            m |= mk
        dentro.append(int(m.sum())); tot.append(per_reg)
    _di("REGIONI_%s nodi dentro le TRE regioni = %.1f +- %.1f   per regione %s"
        % (eti, float(np.mean(dentro)), float(np.std(dentro)), tot[0]))
    _di("QUOTA_%s  materia / totale = %.4f" % (eti, float(np.mean(dentro)) / max(np.mean(cap), 1)))
"""


def main():
    try:
        os.makedirs(os.path.dirname(DEST))
    except OSError:
        pass
    f = io.open(DEST, "w", encoding="utf-8", newline="\n")

    def P(s):
        sys.stdout.write(s)
        f.write(s)

    grezzo = os.path.join(os.path.dirname(DEST), "SCENE_COERENTI.progresso.txt")
    if "--riusa" in sys.argv and os.path.exists(grezzo):
        P("!! `--riusa`: i numeri vengono da `%s`, NON rimisurati adesso\n#\n"
          % os.path.basename(grezzo))
        out = io.open(grezzo, encoding="utf-8", errors="replace").read()
        rc = 0
    else:
        with io.open(grezzo, "w", encoding="utf-8", newline="\n") as g:
            # ⚠ `SEMI` era definito nel GENITORE e non passato al figlio: NameError dopo la
            #   prima riga. Ora si inietta, come per gli altri strumenti.
            rc = subprocess.call([sys.executable, "-u", "-c", "SEMI = %r
" % (SEMI,) + FIGLIO],
                                 cwd=RADICE, stdout=g, stderr=subprocess.STDOUT)
        out = io.open(grezzo, encoding="utf-8", errors="replace").read()

    P("# LE DUE SCENE DELLA STRADA (ii) -- massa = REGIONE A FASE COERENTE NEL VUOTO\n#\n")
    P("# Decisione di Luca, 2026-09-25. Vuoto UNICO con `SEMINA_LAM`; le masse NON\n")
    P("# aggiungono nodi: sono i nodi del vuoto dentro tre sfere, a fase comune.\n")
    P("# I numeri sono CALCOLATI con la semina RSA vera, non stimati.\n#\n")
    if rc != 0:
        P("*** MORTO (rc=%d) ***\n%s\n" % (rc, out[-3000:]))
        f.close()
        return 1
    for x in out.splitlines():
        if x.split(" ")[0] in ("LAM", "RA", "SCENA_A", "SCENA_B") or \
           x.startswith(("VUOTO_", "REGIONI_", "QUOTA_")):
            P("  " + x + "\n")

    P("\n" + "=" * 100 + "\nCOME SI LEGGE, e cosa e' SCELTO\n" + "=" * 100 + "\n")
    P("  `intervallo = R_CONN` fra i bordi delle regioni e' una **SCELTA DI LUCA**, non una\n")
    P("  derivazione: e' il raggio a cui il vuoto si allaccia, quindi \"le regioni si vedono\n")
    P("  appena\". Tutto il resto segue.\n")
    P("\n  `raggio del vuoto = sep + r + R_CONN` e' il MINIMO che contiene le tre regioni piu'\n")
    P("  un guscio di `R_CONN`: il punto di una regione piu' lontano dall'origine sta a\n")
    P("  `sep + r`, e il guscio serve perche' le regioni **non tocchino il bordo del vuoto**.\n")
    P("\n  `QUOTA` e' la frazione di nodi che diventano MATERIA. **Non e' un parametro: e' una\n")
    P("  CONSEGUENZA della geometria**, e va guardata perche' se fosse vicina a `1` il vuoto\n")
    P("  non esisterebbe, e se fosse vicina a `0` le masse non esisterebbero.\n")
    P("\n  ⚠ I nodi \"dentro le regioni\" sono contati su una semina VERA a quel raggio, con la\n")
    P("  capienza misurata **meno uno** (per non farla rifiutare). **Non e' la scena: e' la\n")
    P("  sua geometria.** La scena vera la costruisce il simulatore.\n")
    f.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
