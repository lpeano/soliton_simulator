# -*- coding: utf-8 -*-
"""LA SCANSIONE DEI QUATTRO SCHEMI, in TUTTO il simulatore.

Mandato: doc/TASK_HISTORY/2026-09-20_anomalie-viriale-zetavir.md (7398f94).
Le correzioni vanno OVUNQUE lo schema compaia: l'elenco del mandato e' il punto di partenza, NON
il perimetro. Questo script produce l'elenco COMPLETO, con le righe.

I QUATTRO SCHEMI
  A  una GUARDIA che salta una legge in silenzio:  `len(X) == len(Y)` / `len(X) >= len(Y)` dentro
     un `if`, senza un contatore nel ramo che NON scatta. E' lo schema di (2), ed e' la famiglia
     di C7 (71.88 %) e C11 (95.33 %): rami inerti per mesi senza che nessun sigillo se ne accorga.
  B  un DEFAULT FISICO preso da `np.zeros`/`np.full` su una MASCHERA PARZIALE: si alloca pieno, si
     riempie solo dove la maschera e' vera, e il resto resta al valore di comodo. E' lo schema di
     (3): il valore fuori maschera e' una DECISIONE FISICA presa da un'allocazione.
  C  una SATURAZIONE (`tanh`, `clip`, `x/sqrt(1+x^2)`) confrontata con una grandezza NON limitata.
     E' lo schema di (1): il punto di saturazione diventa UNA SCALA IMPLICITA, mai dichiarata.
  D  una MEMORIA `self._*` scritta in una funzione e letta in un'ALTRA, senza che l'ordine sia
     dichiarato. E' lo schema di (4), ed e' la famiglia di Z19 (quattro occorrenze aperte).

NON GIUDICA: elenca. Un'occorrenza in elenco non e' un difetto finche' non la si guarda -- ma una
NON in elenco non si guardera' mai, ed e' quello il punto.
ASCII PURO.
"""
import ast
import io
import os
import re
import sys
from collections import defaultdict

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
SORG = os.path.join(RADICE, "soliton_simulator.py")


def funzioni(albero):
    """Mappa riga -> nome della funzione che la contiene (la piu' interna)."""
    m = {}
    for nodo in ast.walk(albero):
        if isinstance(nodo, (ast.FunctionDef, ast.AsyncFunctionDef)):
            fine = getattr(nodo, "end_lineno", nodo.lineno)
            for r in range(nodo.lineno, fine + 1):
                pr = m.get(r)
                if pr is None or nodo.lineno > pr[1]:
                    m[r] = (nodo.name, nodo.lineno)
    return {r: v[0] for r, v in m.items()}


def main():
    testo = io.open(SORG, encoding="utf-8").read()
    righe = testo.split("\n")
    albero = ast.parse(testo)
    fn = funzioni(albero)
    import hashlib
    d = open(SORG, "rb").read()
    print("sorgente: soliton_simulator.py   sha1 GREZZO %s   (%d righe)"
          % (hashlib.sha1(d).hexdigest()[:8], len(righe)))
    print("")

    def ctx(i):
        return righe[i].strip()[:110]

    # ------------------------------------------------------------------ A: le guardie
    print("=" * 126)
    print("SCHEMA A -- GUARDIE CHE SALTANO UNA LEGGE: `len(X) == len(Y)` o `len(X) >= len(Y)` in un if")
    print("=" * 126)
    pat_a = re.compile(r"\blen\s*\([^()]*\)\s*(==|>=|<=|!=|>|<)\s*(len\s*\(|self\.n\b|\bn\b)")
    a_tot = 0
    for i, r in enumerate(righe):
        s = r.strip()
        if not (s.startswith("if ") or s.startswith("elif ") or " if " in s):
            continue
        if not pat_a.search(s):
            continue
        a_tot += 1
        print("  :%-5d %-26s %s" % (i + 1, fn.get(i + 1, "<modulo>"), ctx(i)))
    print("  -> %d occorrenze" % a_tot)
    print("")

    # ------------------------------------------------------------------ B: default su maschera
    print("=" * 126)
    print("SCHEMA B -- DEFAULT FISICO DA `np.zeros`/`np.full` POI RIEMPITO SU UNA MASCHERA PARZIALE")
    print("=" * 126)
    alloc = re.compile(r"(\w+)\s*=\s*np\.(zeros|full|zeros_like|full_like|ones)\s*\(")
    b_tot = 0
    for i, r in enumerate(righe):
        m = alloc.search(r)
        if not m:
            continue
        nome = m.group(1)
        # si cerca un riempimento PARZIALE dello stesso nome entro 12 righe
        rip = re.compile(r"\b%s\s*\[" % re.escape(nome))
        for k in range(i + 1, min(i + 13, len(righe))):
            mm = rip.search(righe[k])
            if mm and "=" in righe[k].split("]", 1)[-1]:
                dentro = righe[k][mm.end():righe[k].find("]", mm.end())]
                if dentro.strip() and dentro.strip() not in (":", "...",):
                    b_tot += 1
                    print("  :%-5d %-26s %s" % (i + 1, fn.get(i + 1, "<modulo>"), ctx(i)))
                    print("        -> :%-5d riempita solo su [%s]   %s"
                          % (k + 1, dentro.strip()[:30], ctx(k)))
                    break
    print("  -> %d occorrenze" % b_tot)
    print("")

    # ------------------------------------------------------------------ C: saturazioni
    print("=" * 126)
    print("SCHEMA C -- SATURAZIONI: `tanh`, `clip`, `x/sqrt(1+x**2)`  (il punto di saturazione E' una scala)")
    print("=" * 126)
    pat_c = re.compile(r"np\.tanh\s*\(|np\.clip\s*\(|/\s*np\.sqrt\s*\(\s*1(\.0)?\s*\+|np\.minimum\s*\(\s*1\.0|np\.maximum\s*\(\s*0\.0")
    c_tot = 0
    per_fn = defaultdict(int)
    for i, r in enumerate(righe):
        if r.lstrip().startswith("#"):
            continue
        if not pat_c.search(r):
            continue
        c_tot += 1
        f = fn.get(i + 1, "<modulo>")
        per_fn[f] += 1
        print("  :%-5d %-26s %s" % (i + 1, f, ctx(i)))
    print("  -> %d occorrenze in %d funzioni" % (c_tot, len(per_fn)))
    print("")

    # ------------------------------------------------------------------ D: memorie fra funzioni
    print("=" * 126)
    print("SCHEMA D -- MEMORIE `self._*` SCRITTE IN UNA FUNZIONE E LETTE IN UN'ALTRA")
    print("=" * 126)
    scrive = defaultdict(set)
    legge = defaultdict(set)
    for nodo in ast.walk(albero):
        if not isinstance(nodo, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        for sub in ast.walk(nodo):
            if isinstance(sub, ast.Attribute) and isinstance(sub.value, ast.Name) \
                    and sub.value.id == "self" and sub.attr.startswith("_"):
                if isinstance(sub.ctx, ast.Store):
                    scrive[sub.attr].add(nodo.name)
                elif isinstance(sub.ctx, ast.Load):
                    legge[sub.attr].add(nodo.name)
    d_tot = 0
    for attr in sorted(set(scrive) & set(legge)):
        sc, le = scrive[attr], legge[attr]
        altrove = le - sc
        if not altrove:
            continue
        d_tot += 1
        print("  %-24s scritta in: %-46s letta ANCHE in: %s"
              % (attr, ", ".join(sorted(sc))[:44], ", ".join(sorted(altrove))[:60]))
    print("  -> %d memorie con scrittura e lettura in funzioni DIVERSE" % d_tot)
    print("")

    print("=" * 126)
    print("TOTALI:  A %d guardie | B %d default su maschera | C %d saturazioni | D %d memorie"
          % (a_tot, b_tot, c_tot, d_tot))
    print("=" * 126)
    print("LO SCRIPT NON GIUDICA: ELENCA. Un'occorrenza in elenco non e' un difetto finche' non la")
    print("si guarda -- ma una NON in elenco non si guardera' mai, ed e' quello il punto.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
