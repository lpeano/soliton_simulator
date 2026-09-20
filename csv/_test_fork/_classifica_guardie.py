# -*- coding: utf-8 -*-
"""LE GUARDIE `len(...)` SU PERCORSO FISICO: cosa succede QUANDO FALLISCONO, e CHI le ha introdotte.

Mandato: doc/TASK_HISTORY/2026-09-20_precondizione-e-pannello.md (4e122c3).

DUE DOMANDE PER OGNI SITO, e nessuna delle due si risponde a occhio:

  1 COSA SUCCEDE AL FALLIMENTO -- si legge dall'AST, non dal testo:
      TERNARIO      `x = A if len(..)==n else B`   il default e' INLINE e VISIBILE: gia' un else
      PRECONDIZ.    al fallimento `return` o `raise`  legittima, ma il SILENZIO no
      ESTENSIONE    un ramo ALLUNGA o TRONCA l'array testato   e' LA CURA ad A8b: non si tocca
      DEFAULT       al fallimento si prosegue con un valore di comodo   DIFETTO
      SALTO         al fallimento non succede NIENTE, la legge e' saltata   famiglia gia' curata
      GIA' CURATA   ha gia' un contatore `_g_*` accanto

  2 CHI L'HA INTRODOTTA -- `git log -S "<riga>" --reverse`, e si legge LA PRIMA riga.
    ⚠ NON `git blame`: blame da' l'ULTIMO tocco. Sul sito :3182 blame diceva `f7051c3`, `-S` dice
    `94c2609`: UN COMMIT INTERO DI DIFFERENZA. E' l'errore gia' preso nel giro scorso.

Il criterio di ruolo (FISICA / DIAGN. / RENDER) si IMPORTA da `_scansione_schemi.py`: IL criterio,
non una sua copia.

NON GIUDICA, CLASSIFICA. Il giudizio caso per caso viene dopo, e il mandato chiede che sia
dichiarato per ognuno.
ASCII PURO.
"""
import ast
import io
import os
import re
import subprocess
import sys
from collections import defaultdict

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
sys.path.insert(0, _QUI)
import _presidio

_presidio.avvia(__file__)

from _scansione_schemi import FISICA, ruolo, funzioni   # IL criterio, non una copia

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
SORG = os.path.join(RADICE, "soliton_simulator.py")
ESTENDE = ("concatenate", "vstack", "hstack", "resize", "append", "pad", "full", "zeros", "ones")


def testa_len(nodo):
    """il test contiene un confronto che coinvolge `len(...)`?"""
    for s in ast.walk(nodo):
        if isinstance(s, ast.Call) and isinstance(s.func, ast.Name) and s.func.id == "len":
            return True
    return False


def nomi_testati(test):
    """i nomi dentro i `len(...)` del test, come stringa leggibile."""
    fuori = []
    for s in ast.walk(test):
        if isinstance(s, ast.Call) and isinstance(s.func, ast.Name) and s.func.id == "len":
            try:
                fuori.append(ast.unparse(s.args[0]))
            except Exception:
                fuori.append("?")
    return fuori


def estende(rami, nomi):
    """un ramo ALLUNGA o TRONCA uno degli array testati?"""
    for r in rami:
        for s in ast.walk(r) if not isinstance(r, list) else [x for y in r for x in ast.walk(y)]:
            if isinstance(s, ast.Call) and isinstance(s.func, ast.Attribute) \
                    and s.func.attr in ESTENDE:
                return True
            # troncamento:  self.X = self.X[:n]
            if isinstance(s, ast.Assign):
                try:
                    b = ast.unparse(s.targets[0])
                    if any(b == x or b.endswith("." + x.split(".")[-1]) for x in nomi) \
                            and isinstance(s.value, ast.Subscript):
                        return True
                except Exception:
                    pass
    return False


def ripara(corpo, nomi):
    """il ramo RIPARA la precondizione invece di saltare la legge?
    `if len(psi) < n: self.calcola_psi()` NON salta niente: rimedia e prosegue."""
    for x in corpo:
        for sub in ast.walk(x):
            if isinstance(sub, ast.Call) and isinstance(sub.func, ast.Attribute) \
                    and sub.func.attr in ("calcola_psi", "_grado", "_costruisci_struttura",
                                          "_riallinea_tracking", "_estendi_psi_spinor"):
                return True
            if isinstance(sub, ast.Assign):
                try:
                    if ast.unparse(sub.targets[0]) in nomi:
                        return True
                except Exception:
                    pass
    return False


def classifica(nodo, nomi):
    if isinstance(nodo, ast.IfExp):
        return "TERNARIO"
    # ---- le famiglie di FALSO POSITIVO trovate al PRIMO giro, e ognuna ha il suo perche'.
    # Le elenco invece di correggerle in silenzio: un classificatore che cambia senza dirlo
    # produce tabelle che non si possono confrontare fra un giro e il successivo.
    corpo0, alt0 = nodo.body, nodo.orelse
    # (1) CONTROLLO DI CICLO: `if len(cicli) >= massimo: break` non e' una guardia su una legge.
    if any(isinstance(x, (ast.Break, ast.Continue)) for x in corpo0):
        return "CICLO"
    # (2) TRONCAMENTO con `del`: `if len(conc_nodi) > n: del conc_nodi[n:]` e' ESTENSIONE
    #     (la stessa cura ad A8b, scritta in senso opposto). `estende()` non vedeva il `del`.
    if any(isinstance(x, ast.Delete) for x in corpo0):
        return "ESTENSIONE"
    # (3) IL RAMO RIPARA la precondizione invece di saltare: non e' un salto.
    if ripara(corpo0, nomi):
        return "RIPARA"
    # (4) VACUITA': `if len(proj):` senza confronto -- "c'e' qualcosa da fare?". Se l'insieme e'
    #     vuoto non c'e' NIENTE da decidere, e nessun default viene preso.
    if isinstance(nodo.test, ast.Call) and isinstance(nodo.test.func, ast.Name) \
            and nodo.test.func.id == "len":
        return "VACUITA'"
    if isinstance(nodo.test, ast.BoolOp) and any(
            isinstance(v, ast.Call) and isinstance(v.func, ast.Name) and v.func.id == "len"
            for v in nodo.test.values) and not any(
            isinstance(v, ast.Compare) for v in nodo.test.values):
        return "VACUITA'"
    corpo, alt = nodo.body, nodo.orelse
    if estende([corpo], nomi) or estende([alt], nomi):
        # l'estensione puo' stare in uno dei due rami a seconda di come e' scritta la condizione
        if any(isinstance(x, (ast.Return, ast.Raise)) for x in alt):
            return "PRECONDIZ."
        return "ESTENSIONE"
    if any(isinstance(x, (ast.Return, ast.Raise)) for x in alt):
        return "PRECONDIZ."
    if any(isinstance(x, (ast.Return, ast.Raise)) for x in corpo) and not alt:
        # `if len(X) < n: return`  -> il fallimento della PRECONDIZIONE e' nel CORPO
        return "PRECONDIZ."
    if not alt:
        return "SALTO"
    if any(isinstance(x, (ast.Assign, ast.AugAssign)) for x in alt):
        return "DEFAULT"
    return "ALTRO"


def introdotta(riga, cache):
    """il commit che ha INTRODOTTO la riga: `git log -S`, PRIMA riga dell'output."""
    k = riga.strip()
    if k in cache:
        return cache[k]
    pr = subprocess.run(["git", "log", "--reverse", "-S", k, "--date=short",
                         "--format=%h|%ad|%s", "--", "soliton_simulator.py"],
                        cwd=RADICE, capture_output=True, text=True,
                        encoding="utf-8", errors="replace")
    out = (pr.stdout or "").strip().split("\n")[0] if pr.returncode == 0 else ""
    cache[k] = out
    return out


def main():
    testo = io.open(SORG, encoding="utf-8").read()
    righe = testo.split("\n")
    albero = ast.parse(testo)
    fn = funzioni(albero)
    import hashlib
    d = open(SORG, "rb").read()
    print("sorgente: sha1 GREZZO %s   (%d righe)   funzioni FISICA dichiarate: %d"
          % (hashlib.sha1(d).hexdigest()[:8], len(righe), len(FISICA)))
    print("")

    siti = []
    for nodo in ast.walk(albero):
        if not isinstance(nodo, (ast.If, ast.IfExp)):
            continue
        if not testa_len(nodo.test):
            continue
        L = nodo.lineno
        f = fn.get(L, "<modulo>")
        if ruolo(f) != "FISICA":
            continue
        nomi = nomi_testati(nodo.test)
        siti.append((L, f, classifica(nodo, nomi), righe[L - 1].strip()))
    siti.sort()

    # gia' curati: la riga o le due precedenti contengono un contatore `_g_`
    def curata(L):
        # ⚠ anche `_rep_guardia_`: e' IL MODELLO (`:3972`), non un difetto. Al primo giro il
        # controllo cercava solo `_g_` e lo classificava come SALTO -- falso positivo su quello
        # che il mandato indica ESPLICITAMENTE come esempio da imitare.
        return any(("_g_" in righe[k] or "_rep_guardia_" in righe[k])
                   for k in range(max(0, L - 4), min(len(righe), L + 4)))

    cache = {}
    per_classe = defaultdict(list)
    print("=" * 134)
    print("LE GUARDIE `len(...)` SU PERCORSO FISICO -- classe, riga, e COMMIT CHE L'HA INTRODOTTA")
    print("=" * 134)
    print("%-11s %-6s %-24s %-26s %s" % ("classe", "riga", "funzione", "introdotta da", "codice"))
    for L, f, cl, src in siti:
        if curata(L):
            cl = "GIA' CURATA"
        st = introdotta(src, cache)
        per_classe[cl].append((L, f, st, src))
        print("%-11s :%-5d %-24s %-26s %s" % (cl, L, f[:24], st[:26], src[:58]))

    print("")
    print("=" * 134)
    print("RIEPILOGO PER CLASSE")
    print("=" * 134)
    for cl in sorted(per_classe, key=lambda k: -len(per_classe[k])):
        print("  %-12s %3d" % (cl, len(per_classe[cl])))
    print("  %-12s %3d" % ("TOTALE", sum(len(v) for v in per_classe.values())))

    print("")
    print("=" * 134)
    print("I COMMIT D'ORIGINE, raggruppati: una ragione DICHIARATA si vede dal messaggio")
    print("=" * 134)
    perc = defaultdict(int)
    for cl in per_classe:
        for L, f, st, src in per_classe[cl]:
            perc[st] += 1
    for st in sorted(perc, key=lambda k: -perc[k]):
        print("  %-3d siti  %s" % (perc[st], st[:110] if st else "(nessun commit trovato)"))

    print("")
    print("LO SCRIPT CLASSIFICA, NON GIUDICA. Il giudizio caso per caso viene dopo, e va dichiarato.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
