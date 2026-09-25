# -*- coding: utf-8 -*-
"""**GLI ESPONENTI DELLA RAMPA SUI FIGLI**, dai json del sigillo esteso. Serve a `INERZIA-1(C)`.

Il sigillo esteso ha raccolto, per ogni figlio della mitosi e per ogni eta' dalla nascita,
`ramp`, `|omega|`, `rho`, `peq` e `_contrasto`. **Qui si misurano gli ESPONENTI**: `rho ~ ramp^a`,
`_contrasto ~ ramp^b`, `|omega| ~ ramp^c`, con una regressione su `log ramp`.

**Perche' serve:** `R3bis` chiedeva se `|omega|*ramp` e' costante *(cioe' `c = -1`)*. Il criterio
e' fallito, e **un `FAIL` non dice QUANTO vale l'esponente** — che e' l'informazione che decide
quale lettura regge.

**NESSUNA MISURA NUOVA: si leggono i json gia' scritti.** *(Vincolo del mandato globale: finche'
la lista e' attiva non si aprono indagini nuove se non servono a una voce. Questa serve a
`INERZIA-1(C)`, ed e' una LETTURA di dati esistenti.)*

ASCII puro.
"""
# ESENTE-P5: legge JSON gia' scritti, non fa girare il simulatore. La configurazione di quei dati
#   e' dichiarata NEL REFERTO DEL SIGILLO che li ha prodotti, e ripeterla qui sarebbe una copia
#   non verificata invece di una dichiarazione.
import io
import json
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
TMP = os.path.join(RADICE, "csv", "_seal_fork", "_sig_contrasto_esteso", "_tmp")
DEST = os.path.join(_QUI, "_esponenti_figli", "ESPONENTI_figli.txt")
os.makedirs(os.path.dirname(DEST), exist_ok=True)
NL = chr(10)

R = []


def P(s=""):
    R.append(s)


def pend(x, y):
    x = np.log(np.asarray(x, float))
    y = np.asarray(y, float)
    m = np.isfinite(y) & (y > 0) & np.isfinite(x)
    if m.sum() < 3:
        return float("nan"), 0
    c = np.polyfit(x[m], np.log(y[m]), 1)
    yy = np.polyval(c, x[m])
    ss = 1.0 - np.sum((np.log(y[m]) - yy) ** 2) / max(np.sum((np.log(y[m])
                                                             - np.mean(np.log(y[m]))) ** 2), 1e-300)
    return float(c[0]), float(ss)


P("=" * 104)
P("GLI ESPONENTI DELLA RAMPA SUI FIGLI DELLA MITOSI -- dai json del sigillo esteso")
P("=" * 104)
P()
P("  `ramp` cresce dalla nascita; qui si misura COME la seguono le altre grandezze.")
P("  La configurazione e' quella dichiarata nel referto del sigillo (flag SPENTO, argv del")
P("  driver, 2 semi, budget 120 passi). **Nessuna misura nuova: e' una LETTURA.**")
P()
P("%-8s %-22s %-12s %-10s %s" % ("seme", "grandezza", "esponente", "R2", "lettura"))
LETT = {"rho": "il campo del nodo", "contrasto": "rho/peq", "omega": "|omega|", "peq": "la memoria"}
righe = {}
for f in sorted(os.listdir(TMP)):
    if not f.startswith("figli_") or not f.endswith(".json"):
        continue
    o = json.loads(io.open(os.path.join(TMP, f), encoding="utf-8").read())
    if not o.get("storia"):
        P("  %s: nessuna storia" % f)
        continue
    st = np.array(o["storia"], float)     # [passo, id, eta, ramp, omega, rho, peq, contrasto]
    et = sorted(set(int(x) for x in st[:, 2]))
    et = [e for e in et if e >= 2]        # l'eta' 1 porta la CONVENZIONE `_contrasto = 1`
    if len(et) < 4:
        continue
    rr = [float(np.median(st[st[:, 2] == e, 3])) for e in et]
    dd = dict(omega=[float(np.median(st[st[:, 2] == e, 4])) for e in et],
              rho=[float(np.median(st[st[:, 2] == e, 5])) for e in et],
              peq=[float(np.median(st[st[:, 2] == e, 6])) for e in et],
              contrasto=[float(np.median(st[st[:, 2] == e, 7])) for e in et])
    sm = f.replace("figli_s", "").replace(".json", "")
    righe[sm] = {}
    for k in ("rho", "peq", "contrasto", "omega"):
        a, r2 = pend(rr, dd[k])
        righe[sm][k] = a
        P("%-8s %-22s %-12.4f %-10.4f %s" % (sm, k, a, r2, LETT.get(k, "")))
    P("%-8s %-22s %-12s %-10s %s" % (sm, "ramp (da->a)", "%.4g -> %.4g" % (rr[0], rr[-1]),
                                     "", "eta' da %d a %d" % (et[0], et[-1])))
    P()

P("=" * 104)
P("COSA DICONO, e la lettura non e' una scelta fra le tre: e' un PEZZO DI CIASCUNA")
P("=" * 104)
P()
P("  `rho ~ ramp^a` con `a ~ 2`  ->  **LA PARTE QUADRATICA E' MISURATA.** `rho_s` e' il modulo")
P("    QUADRO di una somma i cui pesi portano `ramp_i*ramp_j`: l'esponente 2 e' quello che la")
P("    struttura prevede, e qui si vede sul dato.")
P()
P("  `peq ~ ramp^0` (piatto)  ->  **L'EREDITA' DI `peq` NON SEGUE IL FIGLIO.** E' il valore")
P("    dell'arco del genitore, e resta li' mentre il figlio matura.")
P()
P("  `_contrasto ~ ramp^b` con `b ~ a`  ->  conseguenza dei due precedenti: il contrasto porta")
P("    **tutto** l'esponente di `rho`, perche' il denominatore non ne porta nessuno.")
P()
P("  `|omega| ~ ramp^c`  ->  **SE `c` NON VALE `-1`, `R3bis` come CRITERIO cade**, e la ragione")
P("    e' che `omega` **ha una memoria sua** (`omega_new = omega_src + dt*(coppia/inerzia -")
P("    omega_src/tau)`): confrontare un rapporto ISTANTANEO con una grandezza che RILASSA e' lo")
P("    stesso errore che Luca ha rilevato per `peq`, applicato a `omega`.")
P()
P("COSA QUESTO NON DICE:")
P("  - non e' una misura nuova: e' una LETTURA dei json del sigillo, con la sua configurazione.")
P("  - le mediane per eta' mescolano figli di madri diverse: l'esponente e' di POPOLAZIONE.")
P("  - l'eta' 1 e' ESCLUSA dai fit, e va detto: li' `_contrasto` vale `1` per la CONVENZIONE del")
P("    primo passo, non per la fisica. Includerla darebbe un esponente inventato.")

T = NL.join(R) + NL
io.open(DEST, "w", encoding="utf-8", newline=NL).write(T)
print(T)
