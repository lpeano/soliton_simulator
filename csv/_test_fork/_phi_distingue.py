# -*- coding: utf-8 -*-
"""LA VERIFICA DI `B1`: esiste UNA riga in cui qualcosa distingue `phi` da `phi + 2pi`?

Mandato di Luca, 2026-09-22 sera. **SOLA LETTURA. Se esiste, la decisione si ribalta.**

LA DOMANDA, posta con precisione: per ogni uso di `phi` (o `phi0`, `_phi_t`), **l'espressione
che lo contiene da' un risultato DIVERSO se a `phi` si somma `2pi`?**

COSA NON DISTINGUE, e si esclude:
  * `exp(1j * phi)`, `cos(phi)`, `sin(phi)`, `np.angle(...)` -- periodo `2pi` ESATTO;
  * `% (2pi)` e `% (4pi)` -- gli avvolgimenti (la torsione: `_w4`, `_w8`), gia' noti;
  * `+ 2pi` come antifase -- gia' noto (`D35`).

COSA DISTINGUE, ed e' cio' che si cerca:
  * **MEZZI ANGOLI**: `exp(0.5j * phi)`, `cos(phi/2)`, `phi/2` -- periodo `4pi`;
  * **USI GREZZI**: `phi` in aritmetica, confronti, medie, differenze NON avvolte;
  * qualunque altro uso che non passi da una funzione a periodo `2pi`.

⚠ LO STRUMENTO RESTRINGE, NON DECIDE. Riporta OGNI uso non-periodico con la riga; **la
  lettura una per una la faccio io**, e le righe stanno nel referto perche' le legga anche Luca.

⚠ E IL CRITERIO E' ASIMMETRICO, di proposito: **in caso di dubbio un uso finisce fra i
  CANDIDATI**, non fra gli esclusi. **Un falso allarme costa una lettura; un falso silenzio
  costa la decisione.**
ASCII PURO.
"""
import ast
import hashlib
import io
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
SORGENTE = os.path.join(RADICE, "soliton_simulator.py")
OUT = os.path.join(_QUI, "_diag_D", "PHI_DISTINGUE.md")

# I nomi che PORTANO `phi`. `phi_s` NON c'e': e' l'altro angolo dello spinore, non questo.
NOMI_PHI = {"phi", "phi0", "_phi_t", "fm", "anti", "_phi_prec"}
PERIODICHE = {"exp", "cos", "sin", "angle", "cosh", "sinh"}


def _e_pi(n):
    return isinstance(n, ast.Attribute) and n.attr == "pi"


def _val(n):
    """Il valore numerico di un nodo COSTANTE, se lo e'. `None` altrimenti."""
    if isinstance(n, ast.Constant) and isinstance(n.value, (int, float, complex)):
        return n.value
    if isinstance(n, ast.UnaryOp) and isinstance(n.op, ast.USub):
        v = _val(n.operand)
        return None if v is None else -v
    if isinstance(n, ast.BinOp) and isinstance(n.op, ast.Mult):
        a, b = _val(n.left), _val(n.right)
        return None if (a is None or b is None) else a * b
    return None


def porta_phi(nodo):
    """Il sottoalbero contiene un accesso a una grandezza che porta `phi`?"""
    for x in ast.walk(nodo):
        if isinstance(x, ast.Attribute) and x.attr in NOMI_PHI:
            return x.attr
        if isinstance(x, ast.Name) and x.id in NOMI_PHI:
            return x.id
    return None


def coefficiente(nodo, quale):
    """Il coefficiente che MOLTIPLICA `phi` dentro l'espressione. `None` se non si capisce.

    ⚠ `None` NON significa 1: significa NON SO, e chi non sa finisce fra i CANDIDATI.
    """
    if isinstance(nodo, (ast.Attribute, ast.Name)):
        return 1.0
    if isinstance(nodo, ast.BinOp) and isinstance(nodo.op, ast.Mult):
        for x, y in ((nodo.left, nodo.right), (nodo.right, nodo.left)):
            if porta_phi(x) == quale and porta_phi(y) is None:
                v = _val(y)
                c = coefficiente(x, quale)
                return None if (v is None or c is None) else v * c
        return None
    if isinstance(nodo, ast.BinOp) and isinstance(nodo.op, ast.Div):
        if porta_phi(nodo.left) == quale and porta_phi(nodo.right) is None:
            v = _val(nodo.right)
            c = coefficiente(nodo.left, quale)
            return None if (v is None or c is None or v == 0) else c / v
        return None
    if isinstance(nodo, ast.BinOp) and isinstance(nodo.op, (ast.Add, ast.Sub)):
        # `phi_i - phi_j`: il coefficiente di CIASCUNO e' +-1, e l'espressione resta a 2pi
        ca = coefficiente(nodo.left, quale) if porta_phi(nodo.left) == quale else 0.0
        cb = coefficiente(nodo.right, quale) if porta_phi(nodo.right) == quale else 0.0
        if ca is None or cb is None:
            return None
        return ca + (-cb if isinstance(nodo.op, ast.Sub) else cb)
    if isinstance(nodo, ast.Subscript):
        return coefficiente(nodo.value, quale)
    if isinstance(nodo, ast.UnaryOp) and isinstance(nodo.op, ast.USub):
        c = coefficiente(nodo.operand, quale)
        return None if c is None else -c
    return None


def intero(c):
    """Il coefficiente e' INTERO (in unita' di `1` o di `1j`)? Allora il periodo resta `2pi`."""
    if c is None:
        return False
    if isinstance(c, complex):
        if abs(c.real) > 1e-12:
            return False
        c = c.imag
    return abs(c - round(c)) < 1e-12


def analizza(testo):
    albero = ast.parse(testo)
    righe = testo.splitlines()
    di_chi = {}
    for nodo in ast.walk(albero):
        if isinstance(nodo, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for x in ast.walk(nodo):
                ln = getattr(x, "lineno", None)
                if ln is not None:
                    pre = di_chi.get(ln)
                    if pre is None or nodo.lineno > pre[1]:
                        di_chi[ln] = (nodo.name, nodo.lineno)

    coperti = set()          # (riga, colonna) degli usi SPIEGATI da un contesto periodico
    candidati = []

    # --- 1. gli usi DENTRO una funzione periodica, col loro COEFFICIENTE
    for nodo in ast.walk(albero):
        if not (isinstance(nodo, ast.Call) and isinstance(nodo.func, ast.Attribute)
                and nodo.func.attr in PERIODICHE and nodo.args):
            continue
        arg = nodo.args[0]
        q = porta_phi(arg)
        if q is None:
            continue
        c = coefficiente(arg, q)
        r = nodo.lineno
        fn = di_chi.get(r, ("<modulo>", 0))[0]
        src = righe[r - 1].strip()
        if intero(c):
            for x in ast.walk(arg):
                if isinstance(x, (ast.Attribute, ast.Name)):
                    coperti.add((getattr(x, "lineno", r), getattr(x, "col_offset", -1)))
        else:
            candidati.append(dict(riga=r, fn=fn, quale=q, perche="MEZZO ANGOLO o coefficiente "
                                  "NON INTERO dentro `%s` (coeff=%s)" % (nodo.func.attr, c),
                                  src=src))
            for x in ast.walk(arg):
                if isinstance(x, (ast.Attribute, ast.Name)):
                    coperti.add((getattr(x, "lineno", r), getattr(x, "col_offset", -1)))

    # --- 2. gli usi dentro un AVVOLGIMENTO `% (k pi)`: gia' noti, si escludono
    for nodo in ast.walk(albero):
        if isinstance(nodo, ast.BinOp) and isinstance(nodo.op, ast.Mod):
            if porta_phi(nodo.left) is None:
                continue
            v = _val(nodo.right)
            e_pi_mult = (isinstance(nodo.right, ast.BinOp)
                         and any(_e_pi(z) for z in (nodo.right.left, nodo.right.right)))
            if e_pi_mult or (v is not None):
                for x in ast.walk(nodo.left):
                    if isinstance(x, (ast.Attribute, ast.Name)):
                        coperti.add((getattr(x, "lineno", nodo.lineno),
                                     getattr(x, "col_offset", -1)))

    # --- 3. TUTTO IL RESTO: ogni accesso non coperto e' un CANDIDATO
    for nodo in ast.walk(albero):
        q = None
        if isinstance(nodo, ast.Attribute) and nodo.attr in NOMI_PHI:
            q = nodo.attr
        elif isinstance(nodo, ast.Name) and nodo.id in NOMI_PHI:
            q = nodo.id
        if q is None:
            continue
        chiave = (nodo.lineno, nodo.col_offset)
        if chiave in coperti:
            continue
        r = nodo.lineno
        fn = di_chi.get(r, ("<modulo>", 0))[0]
        candidati.append(dict(riga=r, fn=fn, quale=q,
                              perche="USO GREZZO: non passa da nessuna funzione a periodo "
                                     "`2pi` e non e' dentro un avvolgimento",
                              src=righe[r - 1].strip()))
    visti, out = set(), []
    for c in sorted(candidati, key=lambda z: (z["riga"], z["perche"])):
        k = (c["riga"], c["perche"][:20])
        if k in visti:
            continue
        visti.add(k)
        out.append(c)
    return out


def collaudo(W):
    """`P1-sexies`, e i casi che DEVONO comparire fra i candidati."""
    W("COLLAUDO (`P1-sexies`), PRIMA di cercare\n" + "-" * 96 + "\n")
    e = []

    def prova(nome, sorgente, deve_comparire, spiega):
        c = analizza("import numpy as np\nclass R(object):\n    def f(self):\n" + sorgente)
        c = [x for x in c if "MEZZO" in x["perche"] or "GREZZO" in x["perche"]]
        ok = (len(c) > 0) == deve_comparire
        e.append(ok)
        W("%-4s %s -> %s  %s\n"
          % (nome, spiega, "CANDIDATO" if c else "escluso", "OK" if ok else "*** NO ***"))
        return c

    prova("K1", "        return np.exp(1j * self.phi)\n", False,
          "`exp(1j*phi)` -- periodo 2pi ESATTO")
    prova("K2", "        return np.cos(self.phi[i] - self.phi[j])\n", False,
          "`cos(phi_i - phi_j)` -- differenza, periodo 2pi")
    prova("K3", "        return (self.phi + 0.1) % (4 * np.pi)\n", False,
          "un AVVOLGIMENTO: gia' noto, si esclude")
    c4 = prova("K4", "        return np.exp(-0.5j * self.phi)\n", True,
               "**DEVE COMPARIRE**: `exp(-0.5j*phi)` -- MEZZO ANGOLO, periodo 4pi")
    prova("K5", "        return np.cos(self.phi / 2.0)\n", True,
          "**DEVE COMPARIRE**: `cos(phi/2)` -- mezzo angolo")
    prova("K6", "        return self.phi.mean()\n", True,
          "**DEVE COMPARIRE**: `phi.mean()` -- uso GREZZO")
    prova("K7", "        return self.phi > 3.0\n", True,
          "**DEVE COMPARIRE**: un CONFRONTO su `phi`")
    ok8 = bool(c4) and "coeff" in c4[0]["perche"]
    e.append(ok8)
    W("K8  il candidato dice IL COEFFICIENTE, non solo che c'e' -> %s\n"
      % ("OK" if ok8 else "*** NO ***"))
    ok = all(e)
    W("-" * 96 + "\n  -> %s\n\n" % ("i criteri PASSANO" if ok else "*** NON PASSANO ***"))
    return ok


def main():
    W = sys.stdout.write
    if not collaudo(W):
        return 1
    testo = io.open(SORGENTE, encoding="utf-8").read()
    blob = hashlib.sha1(open(SORGENTE, "rb").read()).hexdigest()[:8]
    cand = analizza(testo)
    mezzi = [c for c in cand if "MEZZO" in c["perche"]]
    grezzi = [c for c in cand if "GREZZO" in c["perche"]]
    o = io.open(OUT, "w", encoding="utf-8", newline="\n")
    Wf = o.write
    Wf("# LA VERIFICA DI `B1` — **esiste una riga che distingue `φ` da `φ + 2π`?**\n\n")
    Wf("> Generato da `csv/_test_fork/_phi_distingue.py`. **Blob `%s`.** Sola lettura.\n" % blob)
    Wf("> **Lo strumento RESTRINGE, non decide:** riporta ogni uso che **non** passa da una "
       "funzione a periodo `2π` e **non** sta dentro un avvolgimento. **La lettura e' una per "
       "una.**\n>\n")
    Wf("> **⚠ Il criterio e' ASIMMETRICO di proposito:** in caso di dubbio un uso finisce fra "
       "i **candidati**. **Un falso allarme costa una lettura; un falso silenzio costa la "
       "decisione.**\n\n")
    Wf("**CANDIDATI: %d** — di cui **MEZZI ANGOLI: %d** e **USI GREZZI: %d**.\n\n"
       % (len(cand), len(mezzi), len(grezzi)))
    for tit, gruppo in (("MEZZI ANGOLI — **questi DISTINGUEREBBERO `φ` da `φ+2π`**",
                         mezzi),
                        ("USI GREZZI — **da leggere uno per uno**", grezzi)):
        Wf("## %s\n\n" % tit)
        if not gruppo:
            Wf("*(nessuno)*\n\n")
            continue
        Wf("| riga | funzione | quale | perché | codice |\n|--:|---|:--:|---|---|\n")
        for c in gruppo:
            Wf("| `%d` | `%s` | `%s` | %s | `%s` |\n"
               % (c["riga"], c["fn"], c["quale"], c["perche"],
                  c["src"][:95].replace("|", "\\|")))
        Wf("\n")
    o.close()
    print(io.open(OUT, encoding="utf-8").read())
    return 0


if __name__ == "__main__":
    sys.exit(main())
