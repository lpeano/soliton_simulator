# -*- coding: utf-8 -*-
"""L'ERA DELLE VOCI DI METODO E STRUMENTI — **il punto `2`.**

> ### ⭐ **La distinzione, e il guardiano dichiara che la precedente era TROPPO GROSSA:**
> ### **`ENTRAMBE`** = una ### **REGOLA DI LAVORO** o ### **uno strumento che sopravvive**;
> ### **era `1`** = cio' che riguarda un ### **OGGETTO CONCRETO dell'era `1`** *(un sigillo di
> una cura, la scena `(ii)`, il pilota, un `.pkl`, il blob `b8c21049`, ### **una funzione o un
> flag di `soliton_simulator.py`**)*.

### ⛔ **`era` e `stato` vanno NELLO STESSO LOTTO**, perche' `era 1` + `APERTA` e'
### **esattamente cio' che `F7` vieta**: separarli renderebbe il primo lotto inapplicabile.

Gira con:  python csv/_era_metodo.py
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

# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Costruisce un lotto per l'indice.
NL = chr(10)
D = os.path.join(RADICE, "doc", "indice")
DATA = "2026-10-09"

# ==========================================================================
#   LE 35, raggruppate COME LE SCRIVE IL MANDATO
# ==========================================================================
GEMELLE = ["REGISTRO_FISICA:" + x for x in
           ("A1", "A2", "A7", "C1", "E1c", "E2", "E4", "S1", "S4", "T4", "T5", "U2-5")]
METODO = ("T3a", "T3b", "V5-SOGLIA", "FOGLIO-NULLO", "FORMA-N-VUOTO", "AB-CONTROLLI",
          "VELENO-DOMINI", "Z142", "D12", "Z89", "Z15", "D13", "Z11")
STRUMENTI = ("CLI-1", "FRAG1", "M0a", "SYNCDB-HEADLESS", "VIDEO-SCENA",
             "CELLE-NAN-APPESE-NOME-SCADUTO", "INVENTARIO-SIGILLI-SENZA-COMMIT",
             "SIGILLO-COMPARATORE-DUPLICATO", "SIGILLO-REGISTRO-NON-CONFRONTABILE",
             "SIGILLO-SENZA-CONFIGURAZIONE")
PERCHE = {}
for _i in GEMELLE:
    PERCHE[_i] = ("e- il CRITERIO DI VERIFICA di una legge dell-era 1, e le sue gemelle "
                  "(REGISTRO_FISICA:A5, U2-6, COMPONENTI:S2, S3) sono GIA- era 1")
for _i in METODO:
    PERCHE[_i] = ("riguarda un OGGETTO CONCRETO dell-era 1 -- un sigillo, la scena (ii), un "
                  "`.pkl`, il pilota, o una funzione del simulatore -- non una regola di "
                  "lavoro")
for _i in STRUMENTI:
    PERCHE[_i] = ("riguarda uno STRUMENTO O UN SIGILLO CONCRETO dell-era 1, non una regola "
                  "che sopravvive alla riscrittura")

# ### ⚠ **I DUE CASI LIMITE, e li dichiaro invece di nasconderli fra i 35.**
LIMITE = {
    "REGISTRO_FISICA:A1":
        "<<flag SPENTO = BYTE-IDENTICO al codice precedente, firma dei byte, un processo per "
        "braccio>> e- UNA FORMA che vale per qualunque era. MA IL SOGGETTO E- UN FLAG del "
        "simulatore, e la forma generica VIVE GIA- in doc/PATTERN_DI_PROVA.md, che e- il "
        "posto delle regole di prova: questa voce e- IL CRITERIO DI QUEL SIGILLO",
    "REGISTRO_FISICA:S1":
        "idem: <<flag SPENTO = byte-identico: firma dei byte su tutti i campi, un processo "
        "per braccio>>. La forma e- generica, il soggetto e- UN FLAG",
}
# ### ⛔ **LE ECCEZIONI TROVATE LEGGENDO: nessuna.** Il mandato ne ammette *(«se il testo
# ### parla in realta' di una REGOLA che vale anche per l'era `2`, NON spostarla»)*, e
# ### ### **ho cercato: non ce n'e'.** Se un giorno ce ne fosse una, va QUI col suo testo.
ECCEZIONI = {}


def main():
    voci = [json.loads(r) for r in io.open(os.path.join(D, "voci.jsonl"), encoding="utf-8")
            if r.strip()]
    per = {v["id"]: v for v in voci}
    tutte = list(GEMELLE) + list(METODO) + list(STRUMENTI)
    assert len(tutte) == len(set(tutte)) == 35, len(tutte)
    lotto = []
    for i in tutte:
        v = per[i]
        assert i not in ECCEZIONI, i
        assert str(v["era"]) == "ENTRAMBE", "`%s`: era `%s`, non ENTRAMBE" % (i, v["era"])
        t = " ".join(((v["titolo"] or "") + " " + (v["descrizione"] or "")).split())
        # ### ⛔ **`stato`: SOSPESA, oppure CHIUSA SE LO E- GIA-** -- il mandato lo dice, e
        # ### ### **una voce chiusa non si riapre per cambiarle l-era.**
        st = "CHIUSA" if v["stato"] == "CHIUSA" else "SOSPESA"
        campi = {"era": "1", "stato": st}
        if st == "SOSPESA" and not v["stato_era_1"]:
            campi["stato_era_1"] = "aperto"
        nota = ("punto 2: era 1 e non ENTRAMBE -- " + PERCHE[i])
        if i in LIMITE:
            nota = ("punto 2: CASO LIMITE, e lo dichiaro -- " + LIMITE[i])
        lotto.append({"id": i, "quando": DATA, "campi": campi,
                      "meta": {"nota_guardiano": nota[:300]},
                      "motivo": ("(2) da era ENTRAMBE a era 1, stato `%s`, DOMINIO E CLASSE "
                                 "INVARIATI (`%s`/`%s`). %s. Il testo dice <<%s>>"
                                 % (st, v["dominio"], v["classe"],
                                    LIMITE.get(i, PERCHE[i]), t[:90]))})
    p = os.path.join(D, "_lotti", "v3_r2.jsonl")
    io.open(p, "w", encoding="utf-8", newline=NL).write(
        NL.join(json.dumps(x, ensure_ascii=False) for x in lotto) + NL)
    print("  scritto doc/indice/_lotti/v3_r2.jsonl: %d voci" % len(lotto))
    print("  (2) %d gemelle di criteri, %d di metodo, %d di strumenti"
          % (len(GEMELLE), len(METODO), len(STRUMENTI)))
    print("  ### LE ECCEZIONI TROVATE LEGGENDO: %d" % len(ECCEZIONI))
    print("  ### I DUE CASI LIMITE, dichiarati:")
    for i in sorted(LIMITE):
        print("      %-22s %s" % (i, LIMITE[i][:96]))
    c = {}
    for x in lotto:
        c[x["campi"]["stato"]] = c.get(x["campi"]["stato"], 0) + 1
    print("  gli stati: %s" % c)
    return 0


if __name__ == "__main__":
    sys.exit(main())
