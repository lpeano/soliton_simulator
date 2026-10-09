# -*- coding: utf-8 -*-
"""PUNTO `4`: **dominio e classe delle ESPLICITE**, ogni motivo **con la frase**.

### ⛔ **La frase e' LA RIGA D'ORIGINE**, non il titolo troncato — e dove la riga non si
ritrova, ### **si dichiara** e si cita il titolo.

Gira con:  python csv/_dominio_esplicite.py
"""
import io
import json
import os
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

# ### `(classe, dominio, era, perche')` — `None` = **non si tocca.**
P4 = {
    "C10": (None, "METODO", None, "il mandato lo dice esplicitamente"),
    "C12": (None, "METODO", None, "il mandato lo dice esplicitamente"),
    "Y2": (None, "METODO", None, "il mandato lo dice esplicitamente"),
    "CENS-A3": (None, "DOCUMENTAZIONE", None,
                "e- un difetto di DOCUMENTAZIONE come le sue sorelle CENS-*"),
    "PRESIDIO-RIFIUTO-SOLO-SIGILLI": (None, "DOCUMENTAZIONE", None,
                                      "il mandato lo dice esplicitamente"),
    "OKN-ASSERT": (None, "INFRASTRUTTURA", None, "il mandato lo dice esplicitamente"),
    "Z54": (None, "INFRASTRUTTURA", None, "il mandato lo dice esplicitamente"),
    "Z55": (None, "INFRASTRUTTURA", None, "il mandato lo dice esplicitamente"),
    "REGISTRO_FISICA:D35": ("DIFETTO", "FISICA", None, "il mandato lo dice esplicitamente"),
    "REGISTRO_FISICA:D37": ("DIFETTO", "INFRASTRUTTURA", "1",
                            "e- `CRITERIO`+`INFRASTRUTTURA`, e questo VIOLA LA REGOLA DELLA "
                            "CLASSE del 2026-10-09: un CRITERIO si aspetta in METODO. Il "
                            "mandato scioglie il nodo dalla parte della CLASSE: non e- un "
                            "criterio, e- un DIFETTO"),
    "REGISTRO_FISICA:C3": ("CRITERIO", "METODO", None,
                           "e- un CRITERIO, e un criterio va in METODO (regola del "
                           "2026-10-09)"),
    "COMPONENTI:Z30": ("FRONTE", "FISICA", None, "il mandato lo dice esplicitamente"),
    "RISCRITTURA-GO": ("FRONTE", None, None, "il mandato lo dice esplicitamente"),
    "PRESTAZIONI-CORSE": ("FRONTE", None, None, "il mandato lo dice esplicitamente"),
    "POZZO-D": ("CURA", None, None, "il mandato lo dice esplicitamente"),
    "CURA2-STRUTTURALE": ("CURA", None, None, "il mandato lo dice esplicitamente"),
}


def main():
    voci = [json.loads(x) for x in
            io.open(os.path.join(D, "voci.jsonl"), encoding="utf-8").read().split(NL)
            if x.strip()]
    per = {v["id"]: v for v in voci}
    manca = [i for i in P4 if i not in per]
    assert not manca, "NON sono voci: %s" % manca
    lotto, fermi = [], []
    for i in sorted(P4):
        cl, dom, era, perche = P4[i]
        v = per[i]
        r = RO.riga_origine(v)[0]
        frase = (RO.norm(r)[:220] if r is not None
                 else ("(la riga d-origine NON si ritrova; il titolo dice) "
                       + RO.norm(v["titolo"])[:180]))
        campi = {}
        if cl and v["classe"] != cl:
            campi["classe"] = cl
        if dom and v["dominio"] != dom:
            campi["dominio"] = dom
        if era and str(v["era"]) != era:
            campi["era"] = era
            # ### ⛔ **`F7` HA BLOCCATO IL PRIMO TENTATIVO**, e ha fatto bene:
            # ### `REGISTRO_FISICA:D37` sarebbe diventata ### **era 1 + APERTA**, e la
            # ### regola in vigore dice che ### **l-era 1 NON CHIUSA e- SOSPESA.**
            # ### ### **Lo stato NON lo scelgo io: lo impone la regola che il presidio
            # ### fa rispettare.**
            if v["stato"] == "APERTA":
                campi["stato"] = "SOSPESA"
                if not v["stato_era_1"]:
                    campi["stato_era_1"] = "aperto"
        if not campi:
            fermi.append((i, "era GIA- cosi-: `%s`/`%s`/era `%s`"
                          % (v["classe"], v["dominio"], v["era"])))
            continue
        lotto.append({"id": i, "quando": DATA, "campi": campi,
                      "meta": {"nota_guardiano": ("punto 4: " + perche)[:300]},
                      "motivo": ("(4) %s. Da `%s`/`%s`/era `%s` a %s. La frase: <<%s>>"
                                 % (perche, v["classe"], v["dominio"], v["era"],
                                    ", ".join("%s=%s" % (k, campi[k])
                                              for k in sorted(campi)), frase))})
    p = os.path.join(D, "_lotti", "v3_s4.jsonl")
    io.open(p, "w", encoding="utf-8", newline=NL).write(
        NL.join(json.dumps(x, ensure_ascii=False) for x in lotto) + NL)
    print("  scritto doc/indice/_lotti/v3_s4.jsonl: %d voci su %d" % (len(lotto), len(P4)))
    for i, m in fermi:
        print("      GIA- A POSTO  %-32s %s" % (i, m))
    senza = [x["id"] for x in lotto if "NON si ritrova" in x["motivo"]]
    if senza:
        print("  ### senza riga d-origine (il motivo cita IL TITOLO, e lo dichiara): %s"
              % " ".join(senza))
    return 0


if __name__ == "__main__":
    sys.exit(main())
