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


# ---------------------------------------------------------------------------------------------
# LA TRIAGE PER RUOLO, e il criterio e' DICHIARATO invece che lasciato all'impressione.
# P5 dice "ogni ramo else su un PERCORSO FISICO va contato": una guardia dentro `_diag_completa`
# o dentro `update` non e' sullo stesso piano di una dentro `step`. L'elenco resta COMPLETO --
# nessuna riga sparisce -- ma ogni riga porta il suo ruolo, cosi' l'ordine di cura e' visibile.
#
# FISICA = le funzioni che `step()` / `mitosi()` / il ciclo del driver attraversano davvero.
# L'elenco e' scritto a mano DAL CODICE e va riletto se il file cambia: e' una DICHIARAZIONE,
# non una deduzione automatica, e dichiararla e' il punto.
FISICA = {
    "step", "mitosi", "memoria_hebbiana_moto", "_passo_spinoriale", "_pesi", "_cs_nodo",
    "_cs_nodo_campo", "_bloch_ritardato", "_tempo_luce_nodo", "_coppia_interferenza",
    "_rho_sorgente", "_nb_grav", "ritmo", "lambda_nodi", "_allaccia", "semina",
    "_eredita_spinore_figli", "scuoti_vuoto", "calcola_psi", "_grado", "_riallinea_tracking",
    "_aggiorna_lift_spinoriale", "_feedback_spinoriale_archi", "_estendi_psi_spinor",
    "chiralita_core_locale", "_bloch_a_spinore", "_mat", "_mat2", "_costruisci_struttura",
    "rilassa_disegno", "_togli_rotazione_rigida", "_base_cicli_topologici", "__init__",
    "carica_stato", "salva_stato", "_registra_concorrenza", "_agg_voce",
}


def ruolo(nome):
    if nome in FISICA:
        return "FISICA"
    if nome.startswith("_render") or nome.startswith("_dbg") or nome in ("update", "_f", "_muovi"):
        return "RENDER"
    return "DIAGN."


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
    a_ruoli = defaultdict(int)
    for i, r in enumerate(righe):
        s = r.strip()
        if not (s.startswith("if ") or s.startswith("elif ") or " if " in s):
            continue
        if not pat_a.search(s):
            continue
        a_tot += 1
        f = fn.get(i + 1, "<modulo>")
        a_ruoli[ruolo(f)] += 1
        print("  %-7s :%-5d %-26s %s" % (ruolo(f), i + 1, f, ctx(i)))
    print("  -> %d occorrenze:  %s"
          % (a_tot, "  ".join("%s %d" % (k, v) for k, v in sorted(a_ruoli.items()))))
    print("")

    # ------------------------------------------------------------------ B: default su maschera
    print("=" * 126)
    print("SCHEMA B -- DEFAULT FISICO DA `np.zeros`/`np.full` POI RIEMPITO SU UNA MASCHERA PARZIALE")
    print("=" * 126)
    alloc = re.compile(r"(\w+)\s*=\s*np\.(zeros|full|zeros_like|full_like|ones)\s*\(")
    b_tot = 0
    b_ruoli = defaultdict(int)
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
                    f = fn.get(i + 1, "<modulo>")
                    b_ruoli[ruolo(f)] += 1
                    print("  %-7s :%-5d %-26s %s" % (ruolo(f), i + 1, f, ctx(i)))
                    print("        -> :%-5d riempita solo su [%s]   %s"
                          % (k + 1, dentro.strip()[:30], ctx(k)))
                    break
    print("  -> %d occorrenze:  %s"
          % (b_tot, "  ".join("%s %d" % (k, v) for k, v in sorted(b_ruoli.items()))))
    print("")

    # ------------------------------------------------------------------ C: saturazioni
    print("=" * 126)
    print("SCHEMA C -- SATURAZIONI: `tanh`, `clip`, `x/sqrt(1+x**2)`  (il punto di saturazione E' una scala)")
    print("=" * 126)
    pat_c = re.compile(r"np\.tanh\s*\(|np\.clip\s*\(|/\s*np\.sqrt\s*\(\s*1(\.0)?\s*\+|np\.minimum\s*\(\s*1\.0|np\.maximum\s*\(\s*0\.0")
    c_tot = c_vere = c_dominio = 0
    per_fn = defaultdict(int)
    c_ruoli = defaultdict(int)
    for i, r in enumerate(righe):
        if r.lstrip().startswith("#"):
            continue
        if not pat_c.search(r):
            continue
        f = fn.get(i + 1, "<modulo>")
        # UN CLIP AL DOMINIO DI arccos NON E' UNA SCALA: clip(x, -1, 1) prima di arccos e' esatto
        # per costruzione (il coseno fra due versori VIVE in [-1,1], e il clip toglie solo
        # l'errore di arrotondamento). Si separa, perche' metterlo in elenco con le saturazioni
        # vere -- quelle in cui un tanh incontra una grandezza NON limitata, che e' l'anomalia (1)
        # del mandato -- annegherebbe le seconde sotto le prime.
        dominio = ("arccos" in r or "arcsin" in r) and "clip" in r
        c_tot += 1
        per_fn[f] += 1
        if dominio:
            c_dominio += 1
            continue
        c_vere += 1
        c_ruoli[ruolo(f)] += 1
        print("  %-7s :%-5d %-26s %s" % (ruolo(f), i + 1, f, ctx(i)))
    print("  -> %d saturazioni VERE (%s)  +  %d clip al DOMINIO di arccos/arcsin (esatti, non scale)"
          % (c_vere, "  ".join("%s %d" % (k, v) for k, v in sorted(c_ruoli.items())), c_dominio))
    print("     totale grezzo %d in %d funzioni" % (c_tot, len(per_fn)))
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
    print("TOTALI:  A %d guardie (FISICA %d) | B %d default (FISICA %d) | "
          "C %d saturazioni vere (FISICA %d) | D %d memorie"
          % (a_tot, a_ruoli["FISICA"], b_tot, b_ruoli["FISICA"], c_vere, c_ruoli["FISICA"], d_tot))
    print("=" * 126)
    print("LO SCRIPT NON GIUDICA: ELENCA. Un'occorrenza in elenco non e' un difetto finche' non la")
    print("si guarda -- ma una NON in elenco non si guardera' mai, ed e' quello il punto.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
