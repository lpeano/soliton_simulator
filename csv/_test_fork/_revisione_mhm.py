# -*- coding: utf-8 -*-
"""REVISIONE (2) e (3) -- **TABELLE GENERATE DALL'AST.** Sola lettura, nessun run.

**(2)** Per ogni scrittura di `d` o `d0` dentro `memoria_hebbiana_moto`: quale **TEMPO**, quale
**CONO**, quali **STATISTICHE GLOBALI** e da dove, il **DIFETTO NOTO**, e se quella famiglia e'
**CURATA ALTROVE E NON QUI**.

**(3)** Ogni legge del file che usa **`DT` di coordinata** dove il tempo unico vorrebbe `dt_e`.

⚠ **COME SI LEGGE UNA DIPENDENZA, e il metodo va dichiarato perche' decide cosa si vede:**
si parte dai NOMI letti nell'espressione scritta e si **RISALE** agli assegnamenti di quei nomi
**dentro la stessa funzione**, ripetendo fino a chiusura. **E' una chiusura SINTATTICA, non un
dataflow**: vede cio' che e' scritto nella funzione, **non** cio' che accade dentro i metodi
chiamati. **Quindi e' un LIMITE INFERIORE: cio' che trova c'e' davvero; cio' che non trova puo'
esserci lo stesso.** *(I metodi chiamati sono elencati a parte, cosi' il buco e' visibile.)*

ASCII puro.
"""
import ast
import io
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
SORGENTE = os.path.join(RADICE, "soliton_simulator.py")
DEST = os.path.join(_QUI, "_revisione", "MHM_e_DT.txt")

# i marcatori che si cercano nella chiusura, e che cosa significano
TEMPO = {"DT": "DT di COORDINATA", "dt_e": "dt_e PROPRIO d'arco",
         "dt_n": "dt_n proprio di NODO", "_dt_e_ultimo": "dt_e PROPRIO (letto)"}
CONO = {"c_sistema": "GLOBALE (LAM*sqrt(K_C))", "passo_causale": "GLOBALE (c_sistema*DT)",
        "cs_arco": "LOCALE d'arco", "_cs_nodo_prev": "LOCALE di nodo"}
GLOB = ("median", "mean", "percentile", "std")
FONTE = {"self.pos": "dal DISEGNO (`pos`)", "self.d0": "da `d0`", "self.d": "da `d`"}
DIFETTI = [
    ("c_sistema", "`D18` -- cono GLOBALE dove serve quello LOCALE",
     "**SI': `COES_CAUSALE` (`C4`) usa il cono LOCALE** -- ma solo nella COESIONE"),
    ("passo_causale", "`D18` -- tetto causale dal cono GLOBALE",
     "**SI': `COES_CAUSALE` (`C4`)**, e solo li'"),
    ("median", "`A2` / `D01` -- statistica GLOBALE dentro una legge LOCALE",
     "**SI': `PEQ_NASCITA_LOCALE` (`C2`) e `SCALA_P` (`Z67`)** -- ma non in questi siti"),
    ("mean", "`A2` -- statistica GLOBALE dentro una legge LOCALE", "in parte"),
    ("self.pos", "`D02` -- legge IL DISEGNO invece della distanza REALE", "NO, mai curato"),
    ("np.clip", "`A11` -- un limite che potrebbe nascondere un difetto",
     "**SI': `ANOM_SIMM` (`C1-bis`) e `PEQ_ESATTO` (`C1`)** -- altrove"),
]


def fn(alb, nome):
    for n in ast.walk(alb):
        if isinstance(n, ast.FunctionDef) and n.name == nome:
            return n
    return None


def nomi(nodo):
    out = set()
    for n in ast.walk(nodo):
        if isinstance(n, ast.Name):
            out.add(n.id)
        elif isinstance(n, ast.Attribute):
            out.add(ast.unparse(n))
            out.add(n.attr)
    return out


def chiusura(f, partenza, maxgiri=12):
    """Risale agli assegnamenti DENTRO la funzione. Chiusura SINTATTICA, non dataflow."""
    ass = {}
    for x in ast.walk(f):
        tg, val = [], None
        if isinstance(x, ast.Assign):
            tg, val = x.targets, x.value
        elif isinstance(x, ast.AugAssign):
            tg, val = [x.target], x.value
        if val is None:
            continue
        for b in tg:
            ass.setdefault(ast.unparse(b), []).append(val)
    vis, front, testo = set(), set(partenza), []
    for _ in range(maxgiri):
        nuovi = set()
        for k in list(front):
            if k in vis:
                continue
            vis.add(k)
            for v in ass.get(k, []):
                testo.append(ast.unparse(v))
                nuovi |= nomi(v)
        front = nuovi - vis
        if not front:
            break
    return vis, " ; ".join(testo)


def main():
    try:
        os.makedirs(os.path.dirname(DEST))
    except OSError:
        pass
    f = io.open(DEST, "w", encoding="utf-8", newline="\n")

    def P(s):
        sys.stdout.write(s)
        f.write(s)

    src = io.open(SORGENTE, encoding="utf-8").read()
    alb = ast.parse(src)
    mhm = fn(alb, "memoria_hebbiana_moto")
    P("# REVISIONE (2)(3) -- GENERATA DALL'AST, nessun run\n#\n")
    P("# `memoria_hebbiana_moto`: righe %d-%d (%d righe)\n#\n"
      % (mhm.lineno, mhm.end_lineno, mhm.end_lineno - mhm.lineno))

    # ---------------------------------------------------------------- (2)
    P("=" * 110 + "\n(2) LE SCRITTURE DI `d`/`d0` IN `memoria_hebbiana_moto`\n" + "=" * 110 + "\n")
    scritture = []
    for x in ast.walk(mhm):
        tg = x.targets if isinstance(x, ast.Assign) else (
            [x.target] if isinstance(x, ast.AugAssign) else [])
        for b in tg:
            s = ast.unparse(b)
            if s.startswith("self.d0") or s.startswith("self.d["):
                scritture.append((x.lineno, ast.unparse(x), x.value))
    scritture.sort()
    P("  trovate %d scritture\n\n" % len(scritture))
    for ln, codice, val in scritture:
        dip, testo = chiusura(mhm, nomi(val))
        tut = testo + " " + codice
        tt = [v for k, v in TEMPO.items() if k in dip or (k + " ") in tut or (k + ")") in tut]
        cc = [v for k, v in CONO.items() if k in dip or k in tut]
        gg = [g for g in GLOB if (g + "(") in tut]
        ff = [v for k, v in FONTE.items() if k in tut]
        P("  :%-5d %s\n" % (ln, codice[:100]))
        P("        TEMPO      %s\n" % (", ".join(tt) or "— *(nessun tempo esplicito nella chiusura)*"))
        P("        CONO       %s\n" % (", ".join(cc) or "—"))
        P("        GLOBALI    %s\n" % (", ".join(gg) or "—"))
        P("        LEGGE DA   %s\n" % (", ".join(ff) or "—"))
        dd = []
        for marc, dif, cur in DIFETTI:
            if marc in tut:
                dd.append("%s   [curato altrove? %s]" % (dif, cur))
        for x2 in dd:
            P("        DIFETTO    %s\n" % x2)
        if not dd:
            P("        DIFETTO    — *(nessun marcatore noto nella chiusura)*\n")
        P("\n")

    chiamati = sorted({ast.unparse(x.func) for x in ast.walk(mhm)
                       if isinstance(x, ast.Call) and isinstance(x.func, ast.Attribute)
                       and ast.unparse(x.func).startswith("self.")})
    P("  ⚠ IL LIMITE DEL METODO: la chiusura e' SINTATTICA e si ferma al bordo della funzione.\n")
    P("     Questi metodi sono CHIAMATI e il loro interno NON e' letto:\n     %s\n\n"
      % ", ".join(chiamati))

    # ---------------------------------------------------------------- (3)
    P("=" * 110 + "\n(3) OGNI USO DI `DT` NEL FILE, per funzione\n" + "=" * 110 + "\n")
    P("  `DT` e' il tempo di COORDINATA. `CLAUDE.md` par.9: *il tic dei processi locali e'\n")
    P("  `dt_n = DT*r`, non `DT`; `DT` nudo impone la foliazione sincrona globale, cioe'\n")
    P("  UN FRAME PREFERITO.* Qui si contano i siti, **non si giudica**: alcuni usi di `DT`\n")
    P("  sono LEGITTIMI (il conteggio dei sottopassi CFL, la costruzione di `dt_e` stesso).\n\n")
    righe = {}
    for n in ast.walk(alb):
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for r in range(n.lineno, (n.end_lineno or n.lineno) + 1):
                righe.setdefault(r, n.name)
    usi = {}
    for n in ast.walk(alb):
        if isinstance(n, ast.Name) and n.id == "DT":
            usi.setdefault(righe.get(n.lineno, "(modulo)"), []).append(n.lineno)
    P("  %-34s %6s  righe\n" % ("funzione", "usi"))
    for k in sorted(usi, key=lambda z: -len(usi[z])):
        v = sorted(set(usi[k]))
        P("  %-34s %6d  %s\n" % (k, len(usi[k]), ", ".join(str(x) for x in v[:12])))
    P("\n  TOTALE usi di `DT`: %d in %d funzioni\n"
      % (sum(len(v) for v in usi.values()), len(usi)))
    P("\n  E DOVE `DT` INCONTRA UN CONO (`c_sistema`, `cs_arco`): e' li' che il tempo unico\n")
    P("  vorrebbe `dt_e`, perche' un TETTO CAUSALE e' `velocita' x TEMPO PROPRIO`.\n")
    for n in ast.walk(alb):
        if isinstance(n, ast.Assign):
            s = ast.unparse(n)
            if "DT" in s and ("cs_arco" in s or "c_sistema" in s):
                P("    :%-5d %-28s %s\n" % (n.lineno, righe.get(n.lineno, "?"), s[:90]))
    f.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
