# -*- coding: utf-8 -*-
r"""**GLI `R` DI `D4` CONTRO L'ALGEBRA ESATTA DELLA FORMA** — *l'errore `n.16` del guardiano.*

> ### ⛔ **PERCHE' ESISTE** *(`2026-10-19`)*: il criterio `LINEARE` di `D4` confronta
> `delta cs` con `delta Lambda`, ma ### **`cs` si calcola da `Lambda` con la forma**
> `cs = Lambda/(Lambda + Lambda_c)` -- quindi verifica ### **soprattutto l'algebra della
> forma.** Il guardiano chiede di verificare con uno script che gli `R` misurati somiglino a
> ### **`R_forma = (Lambda_m + Lambda_c)/(Lambda_m + Lambda_c + delta Lambda)`**, cioe' al
> rapporto ESATTO fra la differenza finita della forma e il suo sviluppo lineare.

## ⭐ CHE COSA FA, SENZA RIGIRARE NIENTE

Legge i bracci salvati da `D4` *(`doc/referti_l2/d4_bracci.jsonl`, commit `7d061581`)*, e per
ogni coppia sorgente/base che converge calcola, ### **blocco per blocco** sui nodi del grumo:
`R = <delta cs>/<delta Lambda>/cs'(Lambda_m)` e `R_forma` con lo stesso `<delta Lambda>`.
### **Riporta la differenza in barre** *(la barra e' quella fra i blocchi della differenza)*.
### ⚠ **E' una lettura, non un criterio:** il verdetto di `LINEARE` resta SOSPESO.

Gira con:  python csv/_r_contro_forma.py
"""
import io
import json
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
JSONL = os.path.join(RADICE, "doc", "referti_l2", "d4_bracci.jsonl")
RAGGIO = 1                    # statica_protocollo.RAGGIO: il grumo, come in D4

import numpy as np                                             # noqa: E402


def _media_grumo(b, chiave):
    anelli = [d for d in b["anelli"] if int(d) <= RAGGIO]
    tot = sum(b["anelli"][d]["n"] for d in anelli)
    return sum(b["anelli"][d]["n"] * np.array(b["anelli"][d][chiave]) for d in anelli) / tot


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    righe = [json.loads(r) for r in io.open(JSONL, encoding="utf-8") if r.strip()]
    basi = {(b["rapporto"], b["dtau"], b["tick"]): b for b in righe if b["quale"] == "base"}
    print("=" * 100)
    print("GLI `R` DI `D4` CONTRO L'ALGEBRA ESATTA DELLA FORMA -- l'errore n.16 del guardiano")
    print("=" * 100)
    print("  i dati: %s (%d bracci, commit 7d061581)" % (os.path.relpath(JSONL, RADICE),
                                                       len(righe)))
    print("  R = <delta cs>/<delta Lambda>/cs'(Lambda_m);  R_forma = (Lm + Lc)/(Lm + Lc +"
          " <delta Lambda>);  per blocco, sul grumo (r <= %d)" % RAGGIO)
    print("-" * 100)
    print("  %-8s %-6s %-5s %-12s %-12s %-12s %-12s %s"
          % ("rapporto", "dtau", "x", "<dLambda>", "R", "R_forma", "R - R_forma", "barre"))
    for b in sorted(righe, key=lambda q: (q["rapporto"], q["dtau"], q["x"], q["tick"])):
        if b["quale"] != "sorgente" or b["non_converge"]:
            continue
        b0 = basi.get((b["rapporto"], b["dtau"], b["tick"]))
        if b0 is None or b0["non_converge"]:
            continue
        lm, lc = b["lambda_medio"], b["lambda_c"]
        csp = lc / (lm + lc) ** 2
        dcs = _media_grumo(b, "cs") - _media_grumo(b0, "cs")
        dl = _media_grumo(b, "lam") - _media_grumo(b0, "lam")
        r = dcs / dl / csp
        rf = (lm + lc) / (lm + lc + dl)
        dd = r - rf
        m = float(np.mean(dd))
        s = float(np.std(dd, ddof=1)) / np.sqrt(dd.size)
        print("  %-8g %-6g %-5g %+-12.4e %-12.6f %-12.6f %+-12.3e %.1f"
              % (b["rapporto"], b["dtau"], b["x"], float(np.mean(dl)), float(np.mean(r)),
                 float(np.mean(rf)), m, abs(m) / s if s > 0 else float("nan")))
    print("=" * 100)
    print("### E' UNA LETTURA, NON UN CRITERIO: il verdetto di LINEARE resta SOSPESO.")
    print("=" * 100)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
