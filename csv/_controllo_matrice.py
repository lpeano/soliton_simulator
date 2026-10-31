# -*- coding: utf-8 -*-
r"""**IL CONTROLLO DI `matrice` SUI REFERTI GIA' FATTI** *(UNA PROVA E UNA CORREZIONE DI STRUMENTO IN `csv/`, NESSUNA MODIFICA AL NUCLEO; il mandato di Luca delle `21:03` del `2026-10-31`;
[[PIANO-2D-3D]], [[PROGETTO-MASSA-COLLETTIVA]]; il task history `doc/TASK_HISTORY/2026-11-01_controllo_matrice.md`)*:
### **l'elenco AST di chi chiama `_dove_va_la_materia.matrice` (o `un_tick`, o una funzione che le chiama), con le righe che leggono lo stato DOPO la chiamata** *(la classe la do a mano, nel referto)*.

    python csv/_controllo_matrice.py --elenco > doc/referti_l2/controllo_matrice_elenco.txt
"""
import ast
import glob
import os
import re
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)

SRC = "_dove_va_la_materia"
RADICI = ((SRC, "matrice"), (SRC, "un_tick"))   # ### un_tick: la causa; matrice la chiama (un'estensione dichiarata nel task history)
# ### le letture dello stato: `z["st"]`, e le misure che lo leggono (il task history, criterio 1); la riga si STAMPA, la classe si da' a mano
LETTURE = re.compile(r'\[\s*"st"\s*\]|\.st\b|\bst\s*\[|\bforma\s*\(|\bpunto\s*\(|\banelli\s*\(|\bdensita\s*\(|\bmisure\s*\(|baricentro|\bcarica\w*\s*\(|\bpartenza\w*\s*\(')


def moduli():
    mm = {}
    for f in sorted(glob.glob(os.path.join(_QUI, "*.py"))):
        n = os.path.basename(f)[:-3]
        testo = open(f, encoding="utf-8").read()
        mm[n] = (ast.parse(testo), testo.splitlines())
    return mm


def alias(tree):
    am = {}
    for nd in ast.walk(tree):
        if isinstance(nd, ast.Import):
            for a in nd.names:
                am[a.asname or a.name] = a.name
        elif isinstance(nd, ast.ImportFrom) and nd.module:
            for a in nd.names:
                am[a.asname or a.name] = (nd.module, a.name)
    return am


def bersaglio(c, n, am):
    """### **`(modulo, funzione)` di una chiamata**, risolti gli alias; `None` se non si risolve."""
    if isinstance(c.func, ast.Attribute) and isinstance(c.func.value, ast.Name):
        m = am.get(c.func.value.id)
        return (m, c.func.attr) if isinstance(m, str) else None
    if isinstance(c.func, ast.Name):
        m = am.get(c.func.id)
        return m if isinstance(m, tuple) else (n, c.func.id)
    return None


def funzioni(tree):
    return [x for x in ast.walk(tree) if isinstance(x, ast.FunctionDef)]


def chiusura(mm):
    """### **Le funzioni che chiamano le RADICI, transitivamente** *(punto fisso)*."""
    sp = set(RADICI)
    cambiato = True
    while cambiato:
        cambiato = False
        for n, (t, _r) in mm.items():
            am = alias(t)
            for fn in funzioni(t):
                if (n, fn.name) in sp:
                    continue
                if any(isinstance(c, ast.Call) and bersaglio(c, n, am) in sp for c in ast.walk(fn)):
                    sp.add((n, fn.name))
                    cambiato = True
    return sp


def elenco():
    mm = moduli()
    sp = chiusura(mm)
    print("=" * 130)
    print("IL CONTROLLO DI matrice (Luca 21:03): L'ELENCO -- chi chiama %s.matrice o %s.un_tick, anche transitivamente; le righe DOPO la chiamata che leggono lo stato" % (SRC, SRC))
    print("  le letture cercate (la regex): %s" % LETTURE.pattern)
    print("  ### la riga si stampa, la classe (PULITO / SOSPETTO) la do a mano nel referto")
    print("=" * 130)
    dirette, trans = [], []
    for n, (t, righe) in mm.items():
        am = alias(t)
        for fn in funzioni(t):
            fine = max(getattr(x, "end_lineno", fn.lineno) or fn.lineno for x in ast.walk(fn) if hasattr(x, "lineno"))
            for c in ast.walk(fn):
                if not isinstance(c, ast.Call):
                    continue
                b = bersaglio(c, n, am)
                if b not in sp or (n, fn.name) in RADICI:
                    continue
                dopo = [(i + 1, righe[i].strip()) for i in range(c.lineno, fine) if LETTURE.search(righe[i]) and not righe[i].strip().startswith("#")]
                (dirette if b in RADICI else trans).append((n, c.lineno, fn.name, b, dopo))
    for titolo, lista in (("### LE CHIAMATE DIRETTE (a matrice o un_tick)", dirette), ("### LE CHIAMATE TRANSITIVE (a una funzione che le chiama)", trans)):
        print(titolo)
        file_ = sorted(set(x[0] for x in lista))
        print("  %d chiamate in %d file" % (len(lista), len(file_)))
        for n, ln, fnome, b, dopo in sorted(lista):
            print("  %s.py:%d  %s -> %s.%s   (letture dopo, nella stessa funzione: %d)" % (n, ln, fnome, b[0], b[1], len(dopo)))
            for i, r in dopo:
                print("      %d: %s" % (i, r[:150]))
        print("-" * 130)
    print("### LE ALTRE FUNZIONI `matrice` (non %s.matrice: elencate, NON controllate; il task history, Cosa NON so)" % SRC)
    altre = sorted(n for n, (t, _r) in mm.items() if n != SRC and any(fn.name == "matrice" for fn in funzioni(t)))
    print("  %d: %s" % (len(altre), " ".join(altre)))
    print("=" * 130)


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    if "--elenco" in argv:
        elenco()
    else:
        print(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
