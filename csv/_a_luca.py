# -*- coding: utf-8 -*-
"""PUNTO `5`: le **nove a Luca**, ### **SENZA TOCCARLE.**

> ### ⛔ **«Senza toccare» significa:** ### **ne' `classe`, ne' `dominio`, ne' `era`, ne'
> `stato`.** Si aggiunge ### **soltanto la domanda** in `nota_guardiano`, e
> `doc/indice/DA_DECIDERE_LUCA.md` ### **le raccoglie da se'** — il suo primo criterio e'
> proprio *«la nota dice «da decidere da Luca»»*.

### ⚠ **E la FRASE non va nella nota:** l'elenco generato porta gia' una colonna
### **«LA FRASE»** coi primi `150` caratteri del testo. ### **Scriverla due volte vorrebbe
dire tenerla in due posti, e due copie divergono.**

Gira con:  python csv/_a_luca.py
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

DOMANDE = {
    "Z47": "era 2? il testo dice <<PROGETTO DI LUNGO PERIODO -- NON INIZIATO. GEOMETRIA "
           "RELAZIONALE SENZA EMBEDDING>>, e un progetto non iniziato somiglia all-era 2",
    "O4": "era 2? e- un-OBIEZIONE AL BERSAGLIO (la conservazione dell-energia), e un-obiezione "
          "al bersaglio non si chiude nell-era 1",
    "A3-DISEGNO": "superata da A16/A17? le due decisioni di Luca del 2026-10-08 riscrivono "
                  "cio- che questa voce chiede",
    "G4-MEMARCO": "superata da A16/A17?",
    "Z104": "superata da A16/A17?",
    "K2a": "era 1 o ENTRAMBE? dipende se cio- che dice riguarda un oggetto concreto dell-era "
           "1 o una regola che sopravvive",
    "K2b": "era 1 o ENTRAMBE?",
    "SPINORE-SENZA-FASE": "contiene una DIREZIONE DI LUCA per l-era 2: va letta come "
                          "programma dell-era 2 o come difetto dell-era 1?",
    "MASSA-CRITICA-LOCALE": "contiene una DIREZIONE DI LUCA per l-era 2: va letta come "
                            "programma dell-era 2 o come difetto dell-era 1?",
}


def main():
    voci = [json.loads(x) for x in
            io.open(os.path.join(D, "voci.jsonl"), encoding="utf-8").read().split(NL)
            if x.strip()]
    per = {v["id"]: v for v in voci}
    manca = [i for i in DOMANDE if i not in per]
    assert not manca, "NON sono voci: %s" % manca
    lotto = []
    for i in sorted(DOMANDE):
        v = per[i]
        r = RO.riga_origine(v)[0]
        frase = (RO.norm(r)[:200] if r is not None
                 else "(la riga d-origine NON si ritrova) " + RO.norm(v["titolo"])[:160])
        nota = "da decidere da Luca: " + DOMANDE[i]
        assert len(nota) <= 300, "`%s`: la nota supera i 300 caratteri" % i
        lotto.append({"id": i, "quando": DATA, "campi": {},
                      "meta": {"nota_guardiano": nota},
                      "motivo": ("(5) A LUCA, SENZA TOCCARE: `classe`, `dominio`, `era` e "
                                 "`stato` restano `%s`/`%s`/`%s`/`%s`. Si aggiunge SOLO la "
                                 "domanda, e doc/indice/DA_DECIDERE_LUCA.md la raccoglie da "
                                 "se-. La domanda: %s. La frase: <<%s>>"
                                 % (v["classe"], v["dominio"], v["era"], v["stato"],
                                    DOMANDE[i], frase))})
    p = os.path.join(D, "_lotti", "v3_s5.jsonl")
    io.open(p, "w", encoding="utf-8", newline=NL).write(
        NL.join(json.dumps(x, ensure_ascii=False) for x in lotto) + NL)
    print("  scritto doc/indice/_lotti/v3_s5.jsonl: %d voci" % len(lotto))
    print("  ### NESSUN campo di classificazione toccato: solo `meta.nota_guardiano`")
    for x in lotto:
        assert x["campi"] == {}, x["id"]
        print("      %-24s %s" % (x["id"], x["meta"]["nota_guardiano"][:92]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
