# -*- coding: utf-8 -*-
"""PUNTO `6`: **gemelle e duplicati** — ### **dichiarati, NON fusi.**

| | |
|---|---|
| ### **le GEMELLE `D`/`Z`** | una riga della tavola `D` che cita la sua `Z` *(es. `D15` → «`Z71`, letto dal codice»)* e' ### **LO STESSO FATTO**: `stato`, `dominio` ed `era` ### **devono coincidere**, e dove non coincidono ### **`F1` segnala** |
| ### **i DUPLICATI** | `meta.duplicato_di` + `collegate`, e ### **NON si fondono**: `A12`/`STANDARD-8`, `REGISTRO_FISICA:REG-R`/`REG-R`/`H-REG-R`, `C5RES-INVARIANTI`/`D05`, `PASSO-PIENO`/`H-P9` |

### ⛔ **`duplicato_di` NON sceglie un originale.** Ogni membro del gruppo nomina
### **gli altri**, e nessuno e' «il vero»: scegliere sarebbe ### **fondere a meta'**, e il
mandato dice ### **NON FUSI.**

Gira con:  python csv/_gemelle_duplicati.py
"""
import io
import json
import os
import re
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
sys.path.insert(0, _QUI)
import _presidio                                             # noqa: E402
_presidio.avvia(__file__)
import _righe_origine as RO                                  # noqa: E402

# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Costruisce un lotto.
NL = chr(10)
D = os.path.join(RADICE, "doc", "indice")
DATA = "2026-10-09"

GRUPPI = (("A12", "STANDARD-8"),
          ("REGISTRO_FISICA:REG-R", "REG-R", "H-REG-R"),
          ("C5RES-INVARIANTI", "D05"),
          ("PASSO-PIENO", "H-P9"))
_Z = re.compile(r"(?<![A-Za-z0-9_-])(Z\d+[a-z]?)(?![A-Za-z0-9_-])")
_D = re.compile(r"^D\d+[a-z]?$")


def coppie_dz(per):
    """### Le coppie `D`→`Z`: una riga `D` che ### **cita la sua `Z`.**"""
    fuori = []
    for i in sorted(per):
        if not _D.match(i):
            continue
        t = (per[i]["titolo"] or "") + " " + (per[i]["descrizione"] or "")
        for z in _Z.findall(t):
            if z in per:
                fuori.append((i, z))
                break
    return fuori


def main():
    voci = [json.loads(x) for x in
            io.open(os.path.join(D, "voci.jsonl"), encoding="utf-8").read().split(NL)
            if x.strip()]
    per = {v["id"]: v for v in voci}
    lotto = []
    # ---------------------------------------------- i DUPLICATI
    for g in GRUPPI:
        manca = [i for i in g if i not in per]
        assert not manca, "NON sono voci: %s" % manca
        for i in g:
            altri = [x for x in g if x != i]
            v = per[i]
            coll = sorted(set(v["collegate"]) | set(altri))
            r = RO.riga_origine(v)[0]
            frase = (RO.norm(r)[:170] if r is not None
                     else "(la riga d-origine NON si ritrova) " + RO.norm(v["titolo"])[:140])
            lotto.append({"id": i, "quando": DATA,
                          "campi": {"collegate": coll},
                          "meta": {"duplicato_di": altri,
                                   "nota_guardiano":
                                   ("punto 6: DUPLICATO di %s -- dichiarato, NON fuso. "
                                    "`duplicato_di` non sceglie un originale: ogni membro "
                                    "nomina gli altri" % ", ".join(altri))[:300]},
                          "motivo": ("(6) DUPLICATO DICHIARATO, NON FUSO: lo stesso fatto "
                                     "sta anche in %s. `duplicato_di` NON sceglie un "
                                     "originale -- scegliere sarebbe FONDERE A META-, e il "
                                     "mandato dice NON FUSI. La frase: <<%s>>"
                                     % (", ".join("`%s`" % x for x in altri), frase))})
    # ---------------------------------------------- le GEMELLE `D`/`Z`
    dz = coppie_dz(per)
    dis = []
    for d, z in dz:
        a, b = per[d], per[z]
        if (a["stato"], a["dominio"], str(a["era"])) == (b["stato"], b["dominio"],
                                                         str(b["era"])):
            continue
        ra = RO.riga_origine(a)[0]
        rb = RO.riga_origine(b)[0]
        dis.append({"D": d, "Z": z,
                    "D_stato": "%s/%s/era %s" % (a["dominio"], a["stato"], a["era"]),
                    "Z_stato": "%s/%s/era %s" % (b["dominio"], b["stato"], b["era"]),
                    "D_riga": RO.norm(ra)[:220] if ra else "(non si ritrova)",
                    "Z_riga": RO.norm(rb)[:220] if rb else "(non si ritrova)"})
    io.open(os.path.join(D, "_p6_gemelle_dz.json"), "w", encoding="utf-8",
            newline=NL).write(json.dumps({"coppie": dz, "disallineate": dis},
                                         ensure_ascii=False, indent=1))
    p = os.path.join(D, "_lotti", "v3_s6.jsonl")
    io.open(p, "w", encoding="utf-8", newline=NL).write(
        NL.join(json.dumps(x, ensure_ascii=False) for x in lotto) + NL)
    print("  scritto doc/indice/_lotti/v3_s6.jsonl: %d voci (%d gruppi)"
          % (len(lotto), len(GRUPPI)))
    print("  le coppie `D`->`Z`: %d, di cui DISALLINEATE %d" % (len(dz), len(dis)))
    print("  ### NON LE ALLINEO: il mandato dice <<se no, F1 segnala>>, e allinearle")
    print("  ### vorrebbe dire SCEGLIERE quale dei due stati e- giusto. Le elenco.")
    for x in dis:
        print("      %-7s %-26s  <->  %-7s %s" % (x["D"], x["D_stato"], x["Z"],
                                                  x["Z_stato"]))
    print("  scritto doc/indice/_p6_gemelle_dz.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
