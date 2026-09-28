# -*- coding: utf-8 -*-
"""**TUTTI i ripieghi dello schema `len(x) < n` -> valore di scorta.** *(mandato del guardiano,
2026-09-28: «elencali prima di curarli».)*

### Perche' esiste: la stessa forma ha morso TRE volte, e ogni volta per TUTTA LA RETE

| | sito | il valore di scorta |
|---|---|---|
| **1** | `lambda_nodi` `len(psi) < n` | ### `LAM` -- **la schermatura si spegneva** |
| **2** | `_rho_sorgente` `len(rho_spin) < n` | ### `abs(psi)^2` -- **un'altra densita'** |
| **3** | `_nb_grav` `len(psi_spin) < n` | ### `self._nb` -- **un'altra direzione di Bloch** |

**E le tre si assomigliano perche' sono LA STESSA COSA:** *una cache che la nascita non ha estesa,
e un valore di scorta che cambia la fisica di TUTTI in silenzio.*

### **DUE PASSAGGI, e il secondo e' quello che conta**
1. **STATICO**: dall'AST, ogni confronto fra un `len(...)` e `n`/`self.n`. **Trova la FORMA.**
2. ### **A RUNTIME**: quali di quei confronti **prendono davvero il ramo di scorta**, e in quale
   passo. Sul **passo di nascita** e su **quello dopo**, che sono i due in cui una cache resta
   corta. **Senza questo, l'elenco statico e' un elenco di sospetti.**

**Come legge i valori a runtime:** una `settrace` sulle sole righe bersaglio; quando una scatta,
ricostruisce `len(<argomento>)` e `<n>` **dal frame** *(`f_locals`, poi `f_globals`)*. ### **Sola
lettura: nessun file del simulatore e' toccato.**

COMANDO:  python csv/_test_fork/_ripieghi_len_n.py [--passi=46]
USCITA:   0 sempre: e' un ELENCO, non un sigillo.
"""
import ast
import io
import json
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, os.path.join(RADICE, "csv"))
import _presidio  # noqa: E402

_presidio.avvia(__file__)
import numpy as np  # noqa: E402
import _cli_flag  # noqa: E402
import _passo  # noqa: E402

SIM = os.path.join(RADICE, "soliton_simulator.py")
SRC = io.open(SIM, encoding="utf-8").read()
RIG = SRC.split(chr(10))
ARB = ast.parse(SRC)
FUORI = os.path.join(RADICE, "csv", "_seal_fork", "_sig_nascita_psi")


def _dentro(ln):
    q = [(b.end_lineno - b.lineno, b.name) for b in ast.walk(ARB)
         if isinstance(b, ast.FunctionDef) and b.lineno <= ln <= b.end_lineno]
    return min(q)[1] if q else "(modulo)"


def statico():
    """Ogni confronto fra un `len(...)` e `n` / `self.n`, dall'AST."""
    fuori = []
    for nd in ast.walk(ARB):
        if not isinstance(nd, ast.Compare) or len(nd.ops) != 1:
            continue
        sx, dx = nd.left, nd.comparators[0]
        for a, b, verso in ((sx, dx, "sx"), (dx, sx, "dx")):
            if not (isinstance(a, ast.Call) and isinstance(a.func, ast.Name)
                    and a.func.id == "len" and a.args):
                continue
            try:
                tb = ast.unparse(b)
                ta = ast.unparse(a.args[0])
            except Exception:
                continue
            if tb not in ("n", "self.n"):
                continue
            fuori.append({"riga": nd.lineno, "dentro": _dentro(nd.lineno),
                          "cosa": ta, "contro": tb, "verso": verso,
                          "op": type(nd.ops[0]).__name__,
                          "sorgente": RIG[nd.lineno - 1].strip()[:96]})
            break
    # una riga puo' portare piu' confronti: si tengono tutti, ma si deduplica (riga, cosa)
    visti, q = set(), []
    for v in fuori:
        k = (v["riga"], v["cosa"])
        if k not in visti:
            visti.add(k)
            q.append(v)
    return sorted(q, key=lambda x: x["riga"])


def principale():
    # ⚠ LA TRACCIA SI ACCENDE TARDI, E NON E' UN'OTTIMIZZAZIONE: una `settrace` su TUTTE le
    #   righe del simulatore, su una scena da 471564 archi, rende il run ~20 volte piu'
    #   lento -- MISURATO: il primo giro non finiva, e l'ho fermato. Il passo di nascita e'
    #   42, MISURATO due volte, quindi si traccia da 41. **Il prezzo, dichiarato:** dei passi
    #   PRIMA di 41 non si sa niente. Per quelli basta sapere che `n` non cresce.
    passi, traccia_da = 46, 41
    for x in sys.argv[1:]:
        if x.startswith("--passi="):
            passi = int(x.split("=", 1)[1])
        elif x.startswith("--traccia-da="):
            traccia_da = int(x.split("=", 1)[1])
    if not os.path.isdir(FUORI):
        os.makedirs(FUORI)
    siti = statico()
    print("=" * 100)
    print("PASSAGGIO 1 -- STATICO: i confronti fra un `len(...)` e `n` / `self.n`")
    print("=" * 100)
    print("  %-7s %-26s %-6s %-22s %s" % ("riga", "dentro", "op", "cosa", "sorgente"))
    for v in siti:
        print("  :%-6d %-26s %-6s %-22s %s"
              % (v["riga"], v["dentro"], v["op"], v["cosa"][:22], v["sorgente"][:44]))
    print("")
    print("  ### TROVATI %d confronti, in %d funzioni"
          % (len(siti), len({v["dentro"] for v in siti})))
    print("")

    import contextlib
    with contextlib.redirect_stdout(io.StringIO()):
        S0, argv = _cli_flag.argv_del_driver(extra=["--seme=11"],
                                            dest=os.path.join(FUORI, "_scarto_cli"))
        S, a = _cli_flag.carica_dal_cli(list(argv), nome="sim_ripieghi")
        S._NMASSE_VIDEO["n"] = max(2, int(getattr(a, "nmasse", 2)))
        S._NMASSE_VIDEO["sep"] = float(getattr(a, "sep", 3.0))
        S._NMASSE_VIDEO["size"] = None
        S.avvia_test("MASSE-COERENTI")()
        net = S.net
    print("scena: nmasse %d, sep %.4f  ->  n = %d, archi = %d"
          % (S._NMASSE_VIDEO["n"], S._NMASSE_VIDEO["sep"], net.n, len(net.i)))
    print("")

    PER_RIGA = {}
    for v in siti:
        PER_RIGA.setdefault(v["riga"], []).append(v)
    stato = {"passo": 0}
    reg = {}

    def _tr(frame, ev, _arg):
        if frame.f_code.co_filename != SIM:
            return None
        if ev == "line" and frame.f_lineno in PER_RIGA:
            for v in PER_RIGA[frame.f_lineno]:
                amb = {}
                amb.update(frame.f_globals)
                amb.update(frame.f_locals)
                try:
                    L = len(eval(v["cosa"], amb))          # noqa: S307 -- sonda, sola lettura
                    N = eval(v["contro"], amb)             # noqa: S307
                except Exception:
                    continue
                # IL RAMO DI SCORTA si prende quando la cache e' PIU' CORTA di `n`
                corta = bool(L < N)
                k = (stato["passo"], v["riga"], v["cosa"])
                d = reg.setdefault(k, {"volte": 0, "corte": 0, "L": None, "N": None})
                d["volte"] += 1
                if corta:
                    d["corte"] += 1
                    d["L"], d["N"] = int(L), int(N)
        return _tr

    nascita, serie = None, {}
    print("  la traccia si accende dal passo %d (prima: run NUDO)" % traccia_da)
    for k in range(1, passi + 1):
        stato["passo"] = k
        n_prima = int(net.n)
        if k == traccia_da:
            sys.settrace(_tr)
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                _passo.passo_pieno(S, net)
        finally:
            pass
        serie[k] = int(net.n) - n_prima
        if nascita is None and int(net.n) > n_prima:
            nascita = k
        if nascita and k >= nascita + 2:
            break
    sys.settrace(None)

    print("=" * 100)
    print("PASSAGGIO 2 -- A RUNTIME: quali prendono il RAMO DI SCORTA, e quando")
    print("=" * 100)
    print("  prima nascita al passo %s" % nascita)
    print("")
    interessanti = [k for k in (nascita, (nascita or 0) + 1, (nascita or 0) + 2) if k]
    print("  %-7s %-7s %-26s %-22s %-8s %-8s %s"
          % ("passo", "riga", "dentro", "cosa", "volte", "CORTE", "len -> n"))
    fuori = []
    for (p, riga, cosa), d in sorted(reg.items()):
        if not d["corte"]:
            continue
        nome = _dentro(riga)
        fuori.append({"passo": p, "riga": riga, "dentro": nome, "cosa": cosa,
                      "volte": d["volte"], "corte": d["corte"], "len": d["L"], "n": d["N"]})
        if p in interessanti or p <= 2:
            print("  %-7d :%-6d %-26s %-22s %-8d %-8d %s -> %s"
                  % (p, riga, nome, cosa[:22], d["volte"], d["corte"], d["L"], d["N"]))
    print("")
    al_parto = [v for v in fuori if v["passo"] == nascita]
    al_dopo = [v for v in fuori if v["passo"] == (nascita or 0) + 1]
    print("  ### AL PASSO DI NASCITA prendono il ramo di scorta: %d siti  ->  %s"
          % (len({v["riga"] for v in al_parto}),
             sorted({"%s:%d(%s)" % (v["dentro"], v["riga"], v["cosa"]) for v in al_parto})))
    print("  ### AL PASSO DOPO: %d siti  ->  %s"
          % (len({v["riga"] for v in al_dopo}),
             sorted({"%s:%d(%s)" % (v["dentro"], v["riga"], v["cosa"]) for v in al_dopo})))
    print("")
    print("  ⚠ QUESTO E' UN ELENCO, NON UN VERDETTO: un `len(x) < n` puo' essere LEGITTIMO")
    print("    (l'inizializzazione) oppure un RIPIEGO CHE CAMBIA LA FISICA. La differenza la")
    print("    fa CHE COSA restituisce il ramo di scorta, e va letta sito per sito.")
    OUT = os.path.join(_QUI, "_ripieghi_len_n.json")
    io.open(OUT, "w", encoding="utf-8", newline=chr(10)).write(json.dumps(
        {"statico": siti, "runtime_corte": fuori, "passo_nascita": nascita,
         "nati_per_passo": serie, "al_passo_di_nascita": al_parto, "al_passo_dopo": al_dopo,
         "nmasse": S._NMASSE_VIDEO["n"], "sep": S._NMASSE_VIDEO["sep"]},
        indent=1, ensure_ascii=False, sort_keys=True, default=float))
    print("")
    print("scritto: " + OUT)
    return 0


if __name__ == "__main__":
    sys.exit(principale())
