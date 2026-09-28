# -*- coding: utf-8 -*-
"""**UNA SOLA LEGGE SCRIVE OGNI GRANDEZZA-SEGNO: verifica A RUNTIME.**

**Correzione del guardiano** *(Luca, 2026-09-28)* al documento delle regole di `T3`: avevo scritto
che `perc_chi` e' scritta **due volte nello stesso passo** e che *«la seconda sovrascrive la prima»*.
### **E' FALSO, e l'analisi statica non poteva vederlo:** le due scritture stanno in rami che **si
ESCLUDONO**.

```
:5639  if CHI_BASC and (CHI_COOP or not CHI_DA_SPINORE) ... :
           if CHI_COOP:      perc_geom[:n] = where(twn > soglia, 1, -1)     <- il ramo `if`
:5642      else:             perc_chi[:n]  = where(twn > soglia, 1, -1)     <- il ramo `else`
:5666  if _chi_da_psi and SPINORE_CORRETTO ... :
                             perc_chi[:n]  = where(real(_ov) >= 0, 1, -1)
```

**`:5639` e `:5642` sono `if`/`else` della STESSA condizione**, quindi **non girano mai insieme**.
**Col driver `CHI_COOP` e' ACCESO**, quindi: `perc_geom` **solo** da `:5639` *(la torsione)*, e
`perc_chi` **solo** da `:5666` *(il segno dello spinore)*.

### ➜ **La regola <<UNA SOLA legge scrive ogni grandezza-segno>> e' GIA' VERA PER COSTRUZIONE**, ed
e' la cura di `A6-PERCCHI`. **Va DICHIARATA, non curata**, e **non si archivia niente.**

**⚠ E la lezione sul metodo, che e' la terza volta in questa sessione:** l'analisi **statica** vede
**le scritture** e **non le condizioni che le escludono**. Qui ha prodotto un'eccezione inventata.
**Per questo il verdetto viene dalla COPERTURA DI RIGA, non dal conteggio.**

COMANDO:  python csv/_seal_fork/_sig_segni_una_legge.py [--passi=3]
USCITA:   0 se ogni grandezza-segno e' scritta da UN SOLO sito, 1 altrimenti.
"""
import hashlib
import io
import json
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, os.path.join(RADICE, "csv"))
import _presidio  # noqa: E402

_presidio.avvia(__file__)
import _cli_flag  # noqa: E402
import _passo  # noqa: E402

SIM = os.path.join(RADICE, "soliton_simulator.py")
BLOB = hashlib.sha1(io.open(SIM, "rb").read()).hexdigest()

# (riga, grandezza, che cos'e')
SITI = [(5639, "perc_geom", "dalla TORSIONE, ramo `if CHI_COOP`"),
        (5642, "perc_chi", "dalla TORSIONE, ramo `else` -> esclusivo col precedente"),
        (5666, "perc_chi", "dal SEGNO DELLO SPINORE (doppia copertura)")]
BERSAGLI = {r for r, _g, _c in SITI}
VISTE = {}


def _tr(frame, ev, _arg):
    if frame.f_code.co_filename != SIM:
        return None
    if ev == "line" and frame.f_lineno in BERSAGLI:
        VISTE[frame.f_lineno] = VISTE.get(frame.f_lineno, 0) + 1
    return _tr


def principale():
    passi = 3
    for x in sys.argv[1:]:
        if x.startswith("--passi="):
            passi = int(x.split("=", 1)[1])
    S0, argv = _cli_flag.argv_del_driver(extra=["--seme=11"],
                                        dest=os.path.join(_QUI, "_scarto_cli"))
    S, a = _cli_flag.carica_dal_cli(list(argv), nome="sim_segni")
    FLAG = {k: bool(getattr(S, k, False))
            for k in ("CHI_BASC", "CHI_COOP", "CHI_DA_SPINORE", "SPINORE_CORRETTO")}
    print("simulatore blob sha1-BYTE %s" % BLOB[:8])
    print("i flag che decidono: " + "  ".join("%s=%s" % (k, v) for k, v in FLAG.items()))
    S._NMASSE_VIDEO["n"] = 2
    S._NMASSE_VIDEO["sep"] = 3.0
    S._NMASSE_VIDEO["size"] = None
    S.avvia_test("MASSE-COERENTI")()
    net = S.net
    print("scena (ii)(a): n = %d, m = %d. %d passi pieni con la copertura attiva."
          % (net.n, len(net.i), passi))
    sys.settrace(_tr)
    try:
        for _ in range(passi):
            S.esegui_passo(net)
    finally:
        sys.settrace(None)
    print("")
    print("  %-6s %-11s %-9s %s" % ("riga", "grandezza", "esecuzioni", "che cos'e'"))
    per = {}
    for r, g, c in SITI:
        n = VISTE.get(r, 0)
        print("  :%-5d %-11s %-9d %s" % (r, g, n, c))
        if n:
            per.setdefault(g, []).append(r)
    print("")
    doppie = {g: v for g, v in per.items() if len(v) > 1}
    print("=" * 78)
    for g in sorted({g for _r, g, _c in SITI}):
        v = per.get(g, [])
        print("  %-11s scritta da %d sito/i: %s" % (g, len(v), v or "NESSUNO"))
    print("")
    if doppie:
        print("### GRANDEZZE-SEGNO SCRITTE DA PIU' DI UN SITO: %s" % doppie)
    else:
        print("### OGNI GRANDEZZA-SEGNO E' SCRITTA DA UN SOLO SITO.")
        print("    La regola <<una sola legge scrive ogni grandezza-segno>> e' VERA PER")
        print("    COSTRUZIONE col driver: va DICHIARATA, non curata.")
    print("=" * 78)
    OUT = os.path.join(_QUI, "_sig_segni_una_legge.json")
    io.open(OUT, "w", encoding="utf-8", newline=chr(10)).write(json.dumps(
        {"blob_sim": BLOB, "argv": argv[1:], "flag": FLAG, "passi": passi,
         "n": int(net.n), "m": int(len(net.i)),
         "esecuzioni": {str(k): v for k, v in sorted(VISTE.items())},
         "per_grandezza": per, "doppie": doppie, "passa": not doppie}, indent=1,
        ensure_ascii=False, sort_keys=True))
    print("")
    print("scritto: " + OUT)
    return 1 if doppie else 0


if __name__ == "__main__":
    sys.exit(principale())
