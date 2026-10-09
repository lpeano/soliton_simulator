# -*- coding: utf-8 -*-
"""PUNTO `3`: **era `1` per le ESPLICITE**, e `F8` allargato.

| | |
|---|---|
| ### **l'elenco DICHIARATO** | le `14` voci che `doc/CURE_fisica_ordine.md:26` chiama *«voci SOSPESE (non cancellate, restano aperte)»* → ### **era `1`, `SOSPESA`** |
| ### **le `38` nominate** | → ### **era `1`**; lo stato ### **dal punto `1`**, e ### **`SOSPESA` per quelle che il punto `1` non ha deciso** — perche' `F7` vieta era `1` + `APERTA`, ed e' la regola in vigore |

### ⛔ **DUE CONFLITTI VERI, e li dichiaro:** `PSI-FLASH` e `MASSA-ID-FISSO` sono `CHIUSA`
### **con una chiusura che viene dal TAG** *(«chiusa nell'era `1` (stato `chiuso` al tag
`era-1-secondo-ordine`)»)*, e ### **il documento le chiama SOSPESE.** Il mandato dice
`SOSPESA`, quindi ### **si riaprono**, e la vecchia chiusura ### **si toglie** — ma
### **era una chiusura DEL TAG, non di una riga che dice «chiuso».**

Gira con:  python csv/_era_esplicite.py
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
import indice as IX                                          # noqa: E402

# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Costruisce un lotto.
NL = chr(10)
D = os.path.join(RADICE, "doc", "indice")
DATA = "2026-10-09"
FONTE = "doc/CURE_fisica_ordine.md"

NOMINATE = ("ANCORE-1", "CONFIG-1", "PASSO-1", "PAT-1", "PAT-2", "C21", "C28", "Z31", "B2",
            "Z86", "Z145", "Z20", "Z100", "C5-INVARIANTI", "CHI-TORS-ZERO-FALSO", "D26",
            "CBIS-CRITERIO-VACUO", "CTRL-RISCELTA", "T4-TAUTOLOGICO", "PESO-MAX",
            "FINESTRA-DEL-PICCO", "FINESTRA-NON-DICHIARATA", "SIM-PRIMA-STANTIO",
            "OSSERVABILE-P1", "VELENO-ORIENTATO", "VELENO-ARCHI-KEEP",
            "VELENO-AUTORINFRESCO", "LUNGHEZZA-COME-SEGNALE", "H-ETC-2", "Q6", "R3", "R5",
            "U3", "B8", "B10", "ARCHI-PRIMI", "FATTI-AVVIO", "A5-PANNELLO")


def dichiarate():
    """### L'elenco ### **letto dal documento**, non ricopiato: la riga lo porta."""
    righe = io.open(os.path.join(RADICE, FONTE), encoding="utf-8").read().split(NL)
    cand = [(n, r) for n, r in enumerate(righe, 1) if "voci SOSPESE" in r]
    assert len(cand) == 1, "la riga delle <<voci SOSPESE>> non e- unica: %d" % len(cand)
    n, r = cand[0]
    ids = re.findall(r"`([A-Z0-9][A-Za-z0-9:_.\-]*)`", r)
    return ids, n, " ".join(r.split())


def main():
    voci = [json.loads(x) for x in
            io.open(os.path.join(D, "voci.jsonl"), encoding="utf-8").read().split(NL)
            if x.strip()]
    per = {v["id"]: v for v in voci}
    ids, n, riga = dichiarate()
    assert len(ids) == 14, "l-elenco dichiarato ha %d ID, non 14" % len(ids)
    lotto, conflitti = [], []
    fatte = set()

    def porta(i, st, perche, extra=None):
        v = per[i]
        campi = {}
        if str(v["era"]) != "1":
            campi["era"] = "1"
        if st and v["stato"] != st:
            if st not in IX.TRANSIZIONI.get(v["stato"], set()):
                # ### il ponte obbligato, come nel punto `1`
                lotto.append({"id": i, "quando": DATA, "campi": {"stato": "APERTA"},
                              "meta": {},
                              "motivo": ("(3) PONTE OBBLIGATO: da `%s` a `%s` TRANSIZIONI "
                                         "non lo ammette. E la chiusura che si toglie "
                                         "VENIVA DAL TAG, non da una riga che dice "
                                         "<<chiuso>>: %s"
                                         % (v["stato"], st,
                                            json.dumps(v["chiusura"],
                                                       ensure_ascii=False)[:150]))})
            campi["stato"] = st
            if st != "CHIUSA" and v["chiusura"]:
                campi["chiusura"] = {}
        if not campi:
            return
        if st and v["stato"] == "CHIUSA" and st != "CHIUSA":
            conflitti.append((i, v["chiusura"].get("criterio", ""), perche))
        if (campi.get("stato") or v["stato"]) == "SOSPESA" and not v["stato_era_1"]:
            campi["stato_era_1"] = "da-decidere"
        lotto.append({"id": i, "quando": DATA, "campi": campi,
                      "meta": {"nota_guardiano": (extra or perche)[:300]},
                      "motivo": "(3) " + perche})
        fatte.add(i)

    for i in ids:
        porta(i, "SOSPESA",
              "era 1 e SOSPESA: il documento %s:%d le chiama <<voci SOSPESE (non "
              "cancellate, restano aperte)>>, e la riga e- <<%s>>" % (FONTE, n, riga[:150]),
              extra=("punto 3: nell-elenco DICHIARATO <<voci SOSPESE>> di %s:%d"
                     % (FONTE, n)))
    for i in NOMINATE:
        if i in fatte:
            continue
        v = per[i]
        st = "SOSPESA" if v["stato"] == "APERTA" else None
        perche = ("era 1, nominata esplicitamente dal mandato. Lo stato viene dal punto 1"
                  + ("; il punto 1 NON l-ha deciso, e la regola in vigore dice che l-era 1 "
                     "NON CHIUSA e- SOSPESA (ed e- cio- che `F7` pretende)" if st else
                     " e resta `%s`" % v["stato"]))
        porta(i, st, perche, extra="punto 3: era 1, nominata dal mandato")
    p = os.path.join(D, "_lotti", "v3_s3.jsonl")
    io.open(p, "w", encoding="utf-8", newline=NL).write(
        NL.join(json.dumps(x, ensure_ascii=False) for x in lotto) + NL)
    io.open(os.path.join(D, "_p3_conflitti.json"), "w", encoding="utf-8",
            newline=NL).write(json.dumps(conflitti, ensure_ascii=False, indent=1))
    print("  l-elenco dichiarato: %d ID, da %s:%d" % (len(ids), FONTE, n))
    print("  scritto doc/indice/_lotti/v3_s3.jsonl: %d righe (%d voci)"
          % (len(lotto), len(fatte)))
    print("  ### I CONFLITTI, e li dichiaro: %d" % len(conflitti))
    for i, cr, _p in conflitti:
        print("      %-18s era CHIUSA con <<%s>>" % (i, cr[:90]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
