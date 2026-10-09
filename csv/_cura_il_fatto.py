# -*- coding: utf-8 -*-
"""LA CURA DEL DIFETTO «IL FATTO» — **le voci che NON sono nei DATI del guardiano.**

> ### ⛔ **IL DIFETTO ERA MIO, ED E' SCRITTO NEI MIEI STESSI MOTIVI.** Il lotto del punto `1`
> *(2026-10-09)* ha chiuso sei voci col criterio *«la riga dice **FATTO**»*, e la frase
> citata e' ### **«IL FATTO: soglia0 = …»**, ### **«(c) IL FATTO PIU' GROSSO»**,
> ### **«IL FATTO: median(lambda_nodi()) vale 0.8000»**. ### ⭐ **Il criterio di chiusura
> CITAVA la prova che la chiusura era sbagliata**, e non l'ho visto.

**Chi cura chi:** le voci toccate dal difetto ### **che il file del guardiano NON nomina**
*(le altre le decide il file, e il punto `3` le applica con la sua regola)*. L'elenco non e'
scritto a mano: ### **viene da `doc/indice/_il_fatto.json`** meno gli ID del file.

### ⛔ **E LA TRANSIZIONE `CHIUSA` → `SOSPESA` E' VIETATA:** si passa per `APERTA`
### **nello stesso lotto**, due righe di storico — la prima dice ### **che la chiusura era
sbagliata**, la seconda ### **dove va la voce.**

Gira con:  python csv/_cura_il_fatto.py
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
import _stato_dalla_riga as SR                               # noqa: E402

# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Costruisce un lotto.
NL = chr(10)
D = os.path.join(RADICE, "doc", "indice")
DATA = "2026-10-09"
FILE_G = os.path.join(D, "_lotti", "correzioni_guardiano_2026-10-09.txt")


def nei_dati():
    """### Gli ID che il file del guardiano nomina. ### **Si leggono dal FILE**, non da me."""
    rr = [r for r in io.open(FILE_G, encoding="utf-8").read().split(NL) if r.strip()]
    assert len(rr) == 165, "il file del guardiano non ha 165 righe: %d" % len(rr)
    return {r.split("|")[0].strip() for r in rr}


def main():
    voci = [json.loads(x) for x in
            io.open(os.path.join(D, "voci.jsonl"), encoding="utf-8").read().split(NL)
            if x.strip()]
    per = {v["id"]: v for v in voci}
    toccate = json.loads(io.open(os.path.join(D, "_il_fatto.json"),
                                 encoding="utf-8").read())
    dati = nei_dati()
    lotto, lasciate = [], []
    for x in toccate:
        i = x["id"]
        v = per[i]
        if i in dati:
            lasciate.append((i, "E- NEI DATI del guardiano: la decide il file, e il punto 3 "
                                "la applica con la sua regola"))
            continue
        # ### ⛔ **UN SEGNAPOSTO NON PRENDE UNO STATO**, ed e- la stessa scelta del punto
        # ### `1`: ### **prima la classe, poi lo stato.** `M3` e- `NON_DEFINITA`, e il
        # ### difetto non le ha fatto niente ### **perche- il punto 1 la saltava gia-.**
        if v["classe"] == "NON_DEFINITA":
            lasciate.append((i, "SEGNAPOSTO (`NON_DEFINITA`): il punto 1 la saltava gia-, "
                                "e il difetto NON le ha cambiato niente. La sua riga e- "
                                "<<## (1) IL FATTO, trovato durante il collaudo>>, cioe- "
                                "### IL CASO DI SCUOLA del difetto"))
            continue
        r = RO.riga_origine(v)[0]
        nuovo, perche = SR.decidi_stato(v, r)
        # ### ⭐ **E DOVE LA REGOLA CORRETTA NON DECIDE, LO STATO TORNA DOV-ERA.** Non e-
        # ### un-invenzione: la `CHIUSA` di oggi ### **l-ha scritta il mio lotto**, e se la
        # ### regola che l-ha scritta era sbagliata ### **la scrittura si disfa.** Lo stato
        # ### di prima era `SOSPESA`, e per l-era `1` e- ### **cio- che `F7` pretende.**
        if nuovo is None:
            nuovo = "SOSPESA"
            perche = ("la regola CORRETTA non decide NIENTE su questa riga, e la `CHIUSA` "
                      "di oggi l-ha scritta IL MIO LOTTO col difetto: la scrittura si "
                      "disfa, e lo stato torna a `SOSPESA` -- dov-era prima del punto 1, "
                      "e cio- che `F7` pretende per l-era 1")
        if nuovo == v["stato"]:
            lasciate.append((i, "la regola corretta da- `%s`, che e- gia- lo stato su disco"
                                % nuovo))
            continue
        mot = ("(2) IL DIFETTO <<IL FATTO>>, E IL DIFETTO ERA MIO: la parola `FATTO` conta "
               "SOLO se non e- preceduta da `IL`/`il` e non e- seguita da `:`. Il mio lotto "
               "del punto 1 aveva chiuso questa voce citando <<%s>>, cioe- "
               "### IL SOSTANTIVO, non il verbo. %s"
               % (" ".join((v["chiusura"].get("criterio") or "")
                           .split())[-96:].strip(), perche))[:1200]
        # ### IL PONTE, due righe nello STESSO lotto.
        lotto.append({"id": i, "quando": DATA, "campi": {"stato": "APERTA"},
                      "motivo": ("(2) PONTE OBBLIGATO: da `CHIUSA` a `%s` TRANSIZIONI non "
                                 "passa, e si passa per `APERTA`. QUESTA RIGA DICE CHE LA "
                                 "CHIUSURA ERA SBAGLIATA: %s" % (nuovo, mot))[:1200]})
        lotto.append({"id": i, "quando": DATA,
                      "campi": {"stato": nuovo, "chiusura": {}},
                      "meta": {"motivo_dubbio": ("chiusa dal difetto <<IL FATTO>> nel punto "
                                                 "1 del 2026-10-09, e riportata a `%s` dalla "
                                                 "regola corretta" % nuovo)[:300]},
                      "motivo": mot})
    p = os.path.join(D, "_lotti", "v3_il_fatto.jsonl")
    io.open(p, "w", encoding="utf-8", newline=NL).write(
        NL.join(json.dumps(x, ensure_ascii=False) for x in lotto) + NL)
    print("  scritto doc/indice/_lotti/v3_il_fatto.jsonl: %d righe (%d voci, col PONTE)"
          % (len(lotto), len(lotto) // 2))
    print("  ### LE VOCI CURATE QUI (NON nei dati del guardiano):")
    for x in lotto[1::2]:
        print("   %-22s -> %-10s  e la `chiusura` si SVUOTA" % (x["id"],
                                                                x["campi"]["stato"]))
    print("  ### LE VOCI LASCIATE, e il perche' di ciascuna:")
    for i, p2 in lasciate:
        print("   %-22s %s" % (i, p2[:150]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
