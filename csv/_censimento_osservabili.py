# -*- coding: utf-8 -*-
r"""**CHI LEGGE `mot.cs` IN UN'OSSERVABILE** — *l'errore `n.12`, censito e non elencato.*

> ### ⛔⛔ **PERCHE' ESISTE** *(`2026-10-18`)*: `energia_pesata.g_pesata` legge i pesi da
> ### **`mot.cs`**, e ### **dopo `tick_con_cs` `mot.cs` e' il `cs` del CENTRO** di quel
> tick. ### **Un'osservabile che lo usa confronta istanti diversi**, e la differenza e'
> ### **`O(dtau)`** -- e' l'### **errore `n.12` del guardiano**, che mi ha fatto misurare
> `1.002` dove il passo dava `2.091`.

## ⭐ CHE COSA CERCA, E PERCHE' COSI'

### ✅ **CON L'AST, e per TRE forme**: ### **`g_pesata(`** *(l'osservabile sbagliata)*,
### **`pesi(`** e ### **`pesi_dal_passo(`** *(i pesi del passo, usati a mano)*, e
### **`.cs`** *(la lettura diretta)*.
### ⛔ **E NON cerca <<dopo un tick>>:** quello ### **non si legge dall'AST** -- si legge
### **una riga alla volta**, e il censimento ### **dice DOVE guardare**, non chi e'
colpevole.

## ⚠ E DUE LISTE DICHIARATE, perche' non tutte le letture sono un difetto

### ✅ **`LEGITTIMI`**: chi ### **DEVE** usare i pesi del passo -- ### **i pezzi del
passo** *(`flussi_parziali`, `motore`)*, e ### **chi misura la differenza FRA le due
letture.**
### ⛔ **E un nome in piu' in quella lista e' un'eccezione che si paga:** va
### **col suo motivo**, e il presidio ### **non guarda i commenti.**

Gira con:  python csv/_censimento_osservabili.py
"""
import ast
import glob
import io
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
RADICE = os.path.dirname(_QUI)

# ### ⛔ **LE TRE FORME CHE SI CERCANO**, dichiarate per nome.
CHIAMATE = ("g_pesata", "pesi", "pesi_dal_passo")
ATTRIBUTO = "cs"
# ### ⛔ **CHI PUO' LEGGERE I PESI DEL PASSO, e il perche' di ciascuno.**
LEGITTIMI = {
    "primo_ordine/flussi_parziali.py":
        "E' IL PASSO: `dtau_nodo` legge `mot.cs` perche' il tempo proprio E' quello."
        " Qui `mot.cs` non e' un'osservabile: e' la dinamica",
    "primo_ordine/motore.py":
        "E' IL REGISTRO DEL PASSO: `self.cs` nasce qui, e i rami che lo guardano decidono"
        " QUALE SCHEMA gira -- non misurano niente",
    "primo_ordine/tick.py":
        "E' IL PASSO: `cs_al_centro` SCRIVE `mot.cs`, ed e' il punto fisso di `D2`",
    "primo_ordine/energia_pesata.py":
        "E' LA CASA DELLE DUE LETTURE: `pesi` da' quelli del PASSO, `pesi_dello_stato`"
        " quelli dello STATO, e `g_pesata` resta per dire QUANTO LE DUE DISTANO. Il"
        " docstring di `pesi_dello_stato` dichiara la differenza",
}
FUORI_PERIMETRO = ("_archivio", "_seal_", "_test_")


def _righe_che_leggono(p):
    """### Le righe che nominano una delle tre forme, ### **con l'AST.**"""
    try:
        arb = ast.parse(io.open(p, encoding="utf-8").read())
    except (SyntaxError, OSError):
        return []
    fuori = []
    for n in ast.walk(arb):
        if isinstance(n, ast.Call):
            f = n.func
            nome = (f.attr if isinstance(f, ast.Attribute)
                    else (f.id if isinstance(f, ast.Name) else None))
            if nome in CHIAMATE:
                fuori.append((n.lineno, nome + "()"))
        elif isinstance(n, ast.Attribute) and n.attr == ATTRIBUTO:
            fuori.append((n.lineno, "." + ATTRIBUTO))
    return sorted(set(fuori))


def censisci():
    """### `(sospetti, legittimi)`: ### **contati, non elencati a mano.**"""
    sospetti, leg = [], []
    for q in sorted(glob.glob(os.path.join(RADICE, "primo_ordine", "**", "*.py"),
                              recursive=True)
                    + glob.glob(os.path.join(RADICE, "csv", "**", "*.py"),
                                recursive=True)):
        rel = os.path.relpath(q, RADICE).replace(os.sep, "/")
        if any(k in rel for k in FUORI_PERIMETRO):
            continue
        righe = _righe_che_leggono(q)
        if not righe:
            continue
        (leg if rel in LEGITTIMI else sospetti).append((rel, righe))
    return sospetti, leg


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    sospetti, leg = censisci()
    print("=" * 100)
    print("CHI LEGGE `mot.cs` IN UN'OSSERVABILE -- l'errore `n.12`, CENSITO")
    print("=" * 100)
    print("  le forme cercate: %s e `.%s`   (con l'AST)"
          % (", ".join("`%s()`" % q for q in CHIAMATE), ATTRIBUTO))
    print("-" * 100)
    print("  ### I FILE DA GUARDARE, e sono %d:" % len(sospetti))
    tot = 0
    for rel, righe in sospetti:
        tot += len(righe)
        print("     %-44s %s" % (rel, "  ".join("%d:%s" % r for r in righe)))
    print("-" * 100)
    print("  ### E I %d DICHIARATI LEGITTIMI, col loro motivo:" % len(leg))
    for rel, righe in leg:
        print("     %-44s %d righe" % (rel, len(righe)))
    print("-" * 100)
    print("  ### CONTATI: %d file da guardare, %d righe in tutto; %d file legittimi."
          % (len(sospetti), tot, len(leg)))
    print("  ### ⚠ E <<da guardare>> NON vuol dire <<sbagliato>>: vuol dire che la")
    print("  ###   riga va letta, perche' se e' un'OSSERVABILE DOPO UN TICK e' l'errore")
    print("  ###   `n.12`. ### Il censimento dice DOVE, non chi.")
    print("=" * 100)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
