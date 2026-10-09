# -*- coding: utf-8 -*-
"""PUNTO `7`: **le due parti di una voce da dividere** — ### **senza dividerla.**

### ⛔ **`da_dividere` e' un `bool`**, e il mandato chiede *«`meta.da_dividere` con
### **le due parti e la frase di ciascuna**»*: ### **un booleano non puo' portarle.**
### ➜ **Il bool resta** *(dice SE)* e si aggiunge ### **`da_dividere_parti`** *(dice
### **CHE COSA**)*, perche' `M2` e `B6` lo usano gia' col bool e
### **cambiare il tipo di una chiave in uso romperebbe loro.**

### ⭐ **E la divisione si LEGGE, dove il testo la dichiara:** `E4-LAM` dice *«DUE cose,
distinte: ① … ②»*, `B10` dice *«DUE fatti nuovi. ① … ②»*,
`SCHERMATURA-LEGGE-REVISIONE` dice *«TRE PUNTI … (a) … (b) … (c)»*.
### ⚠ **Dove il testo NON la dichiara, la divisione e' MIA e lo scrive.**

Gira con:  python csv/_da_dividere.py
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

LE16 = ("E4-LAM", "Z18", "Z121", "Z78", "Z39", "Z53", "CENS-A2", "CENS-B4", "CENS-B8",
        "B6", "B7", "B10", "LUNGA-BATTITO-CADUTA", "SCHERMATURA-LEGGE-REVISIONE",
        "SPINORE-SENZA-FASE", "MASSA-CRITICA-LOCALE")

# ### I MARCATORI con cui il repo scrive <<due cose>>: cerchi numerati, lettere, <<DUE/TRE>>.
_MARCA = re.compile(r"[①②③④]|(?<![A-Za-z0-9])\([abc]\)(?![A-Za-z0-9])")
_ANNUNCIO = re.compile(r"\b(DUE|TRE|QUATTRO)\s+(cose|fatti|punti|parti|difetti|"
                       r"domande|misure)\b", re.I)


def parti_dal_testo(t):
    """### Le parti ### **che il testo DICHIARA**, o `None`.

    ### ⛔ **Non si inventa un annuncio:** serve un marcatore *(`①`, `(a)`)* ### **e almeno
    due.**
    """
    marche = [m.start() for m in _MARCA.finditer(t)]
    if len(marche) < 2:
        return None
    fuori = []
    for k, s in enumerate(marche):
        fine = marche[k + 1] if k + 1 < len(marche) else min(len(t), s + 260)
        fuori.append(" ".join(t[s:fine].split())[:240])
    return fuori[:4]


def main():
    voci = [json.loads(x) for x in
            io.open(os.path.join(D, "voci.jsonl"), encoding="utf-8").read().split(NL)
            if x.strip()]
    per = {v["id"]: v for v in voci}
    manca = [i for i in LE16 if i not in per]
    assert not manca, "NON sono voci: %s" % manca
    lotto, dichiarate, mie = [], [], []
    for i in LE16:
        v = per[i]
        r = RO.riga_origine(v)[0]
        # ### ⛔ **UN DIFETTO GENERALE DEL RITROVAMENTO, e lo dichiaro:** il prefisso di
        # ### `fonte` puo- combaciare con una riga che e- ### **SOLO L-ID** -- per
        # ### `MASSA-CRITICA-LOCALE` la riga <<ritrovata>> e- `MASSA-CRITICA-LOCALE.`,
        # ### cioe- ### **una citazione nella prosa, senza contenuto.**
        # ### ✔ **Se la riga e- PIU- CORTA del titolo della voce, i campi ne sanno di
        # ### piu-**, e si usano quelli. ### ⚠ **NON cambio `riga_origine`:** i punti 1 e 2
        # ### sono ### **gia- applicati** con quella, e cambiarla adesso farebbe divergere
        # ### il referto da cio- che e- stato scritto. ### **Il difetto va nel referto.**
        if r is not None and len(RO.norm(r)) < len(RO.norm(v["titolo"] or "")):
            r = None
        da_riga = r is not None
        t = RO.norm(r) if da_riga else RO.norm(
            (v["titolo"] or "") + " " + (v["descrizione"] or ""))
        parti = parti_dal_testo(t)
        if parti:
            dichiarate.append(i)
            come = ("il TESTO dichiara le parti (%s%s)"
                    % (("l-annuncio e- <<%s>>, e " % _ANNUNCIO.search(t).group(0))
                       if _ANNUNCIO.search(t) else "",
                       "i marcatori sono nel testo"))
        else:
            # ### ⚠ **La divisione e- MIA**: si taglia sul separatore piu- forte, e
            # ### ### **lo si dichiara.**
            pezzi = [x.strip() for x in t.split(" | ") if len(x.strip()) > 24]
            if len(pezzi) < 2:
                pezzi = [x.strip() for x in re.split(r"(?<=[.;])\s+", t)
                         if len(x.strip()) > 24]
            if len(pezzi) < 2:
                # ### ⚠ **IL TERZO TAGLIO: LA CONGIUNZIONE.** `CENS-A2` dice *<<TORS_4PI:
                # ### "Prova sperimentale, default off", ### **e** il default e- True>>*:
                # ### le due parti sono ### **cio- che il commento DICE** e ### **cio- che
                # ### il codice FA**, e il testo le unisce con una <<e>>.
                pezzi = [x.strip() for x in
                         re.split(r"(?<=[,\"])\s+(?:e|ma|mentre|invece)\s+", t)
                         if len(x.strip()) > 18]
            assert len(pezzi) >= 2, "`%s`: non riesco a trovare due parti in <<%s>>" % (i, t)
            parti = [" ".join(x.split())[:240] for x in pezzi[:2]]
            mie.append(i)
            come = ("### LA DIVISIONE E- MIA, e il testo NON la dichiara: tagliata sul "
                    "separatore piu- forte")
        etichette = ["parte %d: %s" % (k + 1, p) for k, p in enumerate(parti)]
        etichette.append("come l-ho trovata: " + come
                         + ("" if da_riga else " -- E LA RIGA D-ORIGINE NON SI RITROVA: le "
                                              "parti vengono dal titolo e dalla "
                                              "descrizione"))
        lotto.append({"id": i, "quando": DATA, "campi": {},
                      "meta": {"da_dividere": True, "da_dividere_parti": etichette,
                               "nota_guardiano":
                               ("punto 7: DA DIVIDERE in %d parti, e NON si divide: la "
                                "divisione la decide Luca. Le parti con la frase stanno in "
                                "meta.da_dividere_parti" % len(parti))[:300]},
                      "motivo": ("(7) DA DIVIDERE, e NON SI DIVIDE: la voce porta %d cose "
                                 "distinte. %s. Le parti: %s"
                                 % (len(parti), come,
                                    " /// ".join(p[:150] for p in parti)))})
    p = os.path.join(D, "_lotti", "v3_s7.jsonl")
    io.open(p, "w", encoding="utf-8", newline=NL).write(
        NL.join(json.dumps(x, ensure_ascii=False) for x in lotto) + NL)
    print("  scritto doc/indice/_lotti/v3_s7.jsonl: %d voci" % len(lotto))
    print("  ### il TESTO dichiara le parti: %d  -> %s" % (len(dichiarate),
                                                           " ".join(dichiarate)))
    print("  ### la divisione e- MIA:        %d  -> %s" % (len(mie), " ".join(mie)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
