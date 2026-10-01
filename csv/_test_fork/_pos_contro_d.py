# -*- coding: utf-8 -*-
"""**`M5`: QUALI LEGGI LEGGONO `pos` E QUALI SOLO `d`** — la posizione del figlio e' FISICA o DISEGNO?

**Mandato del guardiano del 2026-10-01** *(ed era gia' nel piano come «il primo passo, e non e'
quello che sembra»)*.

### PERCHE' CONTA, e non e' una curiosita'
Se `pos` fosse ### **solo disegno**, la frazione `t` conterebbe **solo** per `d`/`d0`, e la
decisione su `t` sarebbe ### **una decisione sulla LUNGHEZZA, non sulla posizione.**
### **E c'e' gia' un indizio MISURATO che dice il contrario:** `SCHW-CORTI` — lo Schwinger prende
`dd` **da `pos`**, e il **39.06 %** delle coppie **accorcia il grafo**. ### **Quindi `pos` entra
nella metrica almeno in un punto**, ed e' il residuo `A3-DISEGNO`.

### DUE MISURE, e dicono COSE DIVERSE
| | |
|---|---|
| ### **STATICA (AST + grafo delle chiamate)** | ### **chi PUO' leggere**: completa, e **non dipende dalla scena** |
| ### **A RUNTIME (intercettazione)** | ### **chi HA letto** in un passo vero: dice **che cosa gira davvero**, ma solo su **questa** scena |

### ⚠ **E IL TIPO DEL LETTORE NON LO DECIDO IO:** viene da ### **`_PASSO_TIPI`**, la tabella del
simulatore, attraverso `csv/_test_fork/_ordine_letture.py`, che si **importa** invece di
ricopiarlo *(`9-ter`: due copie sarebbero due leggi)*.

### ⚠ **UN LIMITE DELLA PARTE STATICA, dichiarato**
`self.pos[k] = x` e' un **Subscript in scrittura** che contiene un **Attribute in lettura**:
### **una scrittura di elemento, all'AST, somiglia a una lettura.** Si **separa** guardando il
genitore del nodo, e ### **i due conti si riportano distinti** invece di fonderli.

### ⚠ **I NOMI DELLE MISURE: la forma corta `M0`…`M6` e' LOCALE A QUESTO FILE**
Nell'indice ### **`M1`, `M2`, `M3`, `M4` ESISTONO GIA'**, e `M2` e' *«LA MITOSI — ① il figlio
nasce nel PUNTO MEDIO»*, cioe' ### **lo stesso argomento**: la forma nuda ### **risolverebbe al
difetto sbagliato.** ### **Fuori da qui si scrive `DIVISIONE-AUTOCONSISTENTE:M0` … `:M6`.**

COMANDO:  python csv/_test_fork/_pos_contro_d.py [--passi=1]
USCITA:   `csv/_test_fork/_pos_contro_d/_pos_contro_d.json` + stdout.
"""
import ast
import contextlib
import hashlib
import io
import json
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, os.path.join(RADICE, "csv"))
sys.path.insert(0, _QUI)
import _presidio  # noqa: E402

_presidio.avvia(__file__)
import numpy as np  # noqa: E402
import _cli_flag  # noqa: E402
import _passo  # noqa: E402
import _ordine_letture as OL  # noqa: E402  -- si IMPORTA la regola del tipo, non si ricopia

FUORI = os.path.join(RADICE, "csv", "_test_fork", "_pos_contro_d")
SIM = os.path.join(RADICE, "soliton_simulator.py")
BERSAGLI = ("pos", "d", "d0")


def blob(percorso):
    return hashlib.sha1(io.open(percorso, "rb").read()).hexdigest()


def carica(nome):
    with contextlib.redirect_stdout(io.StringIO()):
        _S0, argv = _cli_flag.argv_del_driver(extra=["--seme=11"],
                                              dest=os.path.join(FUORI, "_scarto_cli"))
        S, a = _cli_flag.carica_dal_cli(list(argv), nome=nome)
        S._NMASSE_VIDEO["n"] = max(2, int(getattr(a, "nmasse", 2)))
        S._NMASSE_VIDEO["sep"] = float(getattr(a, "sep", 3.0))
        S._NMASSE_VIDEO["size"] = None
        S.avvia_test("MASSE-COERENTI")()
    return S, S.net


def letture_statiche():
    """`{bersaglio: {funzione: {'letture': k, 'scritture': k, 'elementi': k}}}`, dall'AST."""
    albero = ast.parse(io.open(SIM, encoding="utf-8").read())
    genitore = {}
    for nodo in ast.walk(albero):
        for figlio in ast.iter_child_nodes(nodo):
            genitore[figlio] = nodo
    fuori = {b: {} for b in BERSAGLI}
    for fn in ast.walk(albero):
        if not isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        for nodo in ast.walk(fn):
            if not isinstance(nodo, ast.Attribute) or nodo.attr not in BERSAGLI:
                continue
            # solo `self.X` / `net.X`: un `altro.d` non e' la stessa grandezza.
            base = getattr(nodo.value, "id", None)
            if base not in ("self", "net"):
                continue
            g = genitore.get(nodo)
            voce = fuori[nodo.attr].setdefault(fn.name, {"letture": 0, "scritture": 0,
                                                         "elementi": 0})
            if isinstance(nodo.ctx, ast.Store):
                voce["scritture"] += 1
            elif isinstance(g, ast.Subscript) and isinstance(getattr(g, "ctx", None), ast.Store):
                # ### `self.pos[k] = x`: SCRITTURA DI ELEMENTO, non una lettura.
                voce["elementi"] += 1
            else:
                voce["letture"] += 1
    return fuori


def sorveglia_runtime(net, S):
    """**Conta le letture VERE di `pos`, `d`, `d0`, e dice CHI legge.**

    Si usa la stessa tecnica di `_ordine_letture.py`: una **sottoclasse dinamica** che intercetta
    `__getattribute__`. ### **Il nome del lettore si prende dallo STACK** *(`sys._getframe`)*, non
    da un'ipotesi.
    """
    conti = {b: {} for b in BERSAGLI}
    base = type(net)

    class Spiata(base):
        def __getattribute__(self, nome):
            if nome in BERSAGLI:
                try:
                    f = sys._getframe(1)
                    chi = f.f_code.co_name
                    # se il chiamante e' questo file, non e' una lettura del simulatore
                    if os.path.abspath(f.f_code.co_filename) != os.path.abspath(__file__):
                        c = conti[nome]
                        c[chi] = c.get(chi, 0) + 1
                except Exception:
                    pass
            return base.__getattribute__(self, nome)

    net.__class__ = Spiata
    return conti, base


def principale():
    passi = 1
    for a in sys.argv[1:]:
        if a.startswith("--passi="):
            passi = int(a.split("=", 1)[1])
    if not os.path.isdir(FUORI):
        os.makedirs(FUORI)
    P = []

    def stampa(*x):
        r = " ".join(str(y) for y in x)
        P.append(r)
        print(r)

    stampa("=" * 104)
    stampa("M5 -- QUALI LEGGI LEGGONO `pos` E QUALI SOLO `d`")
    stampa("=" * 104)
    stampa("simulatore ..... %s" % blob(SIM)[:8])
    stampa("questo strumento %s" % blob(os.path.abspath(__file__))[:8])
    stampa("")

    S, net = carica("pos_contro_d")
    _cli_flag.dichiara_configurazione(S, stampa)
    stampa("")

    tipi, _nascita = OL.tipi_dei_lettori(S)
    # ### I TIPI CHE NON SONO LEGGI VENGONO DA `_ordine_letture.NON_LEGGI`, non da una mia
    #   tupla: una seconda copia sarebbe una seconda legge (`9-ter`), e il giorno in cui
    #   `_PASSO_TIPI` guadagna un tipo nuovo le due copie direbbero cose diverse.
    non_leggi = sorted(set(OL.NON_LEGGI))
    stampa("tipi dei lettori presi da `_PASSO_TIPI` (tabella del simulatore): %d funzioni mappate"
           % len(tipi))
    stampa("tipi che NON sono leggi: %s" % (non_leggi or "(nessuno)"))
    stampa("")

    # ------------------------------------------------------------- STATICA
    stampa("=" * 104)
    stampa("STATICA (AST + grafo delle chiamate): CHI PUO' LEGGERE")
    stampa("=" * 104)
    st = letture_statiche()
    riassunto = {}
    for b in BERSAGLI:
        lettori = {f: v for f, v in st[b].items() if v["letture"] > 0}
        # il tipo di ciascun lettore, dalla tabella del simulatore
        come_legge, come_altro = [], []
        for f in sorted(lettori):
            tt = tipi.get(f)
            if tt is None:
                come_altro.append((f, "(non raggiungibile da una voce del passo)"))
            elif set(tt) - set(non_leggi):
                come_legge.append((f, ",".join(sorted(tt))))
            else:
                come_altro.append((f, ",".join(sorted(tt))))
        riassunto[b] = {"lettori": len(lettori), "come_legge": len(come_legge),
                        "non_legge_o_fuori_passo": len(come_altro),
                        "funzioni_legge": [f for f, _ in come_legge],
                        "funzioni_non_legge": [f for f, _ in come_altro],
                        "scritture_dirette": {f: v["scritture"] for f, v in st[b].items()
                                              if v["scritture"]},
                        "scritture_di_elemento": {f: v["elementi"] for f, v in st[b].items()
                                                  if v["elementi"]}}
        stampa("  `%s`: %d funzioni la LEGGONO -- %d dentro una LEGGE, %d osservatore/disegno o "
               "fuori dal passo" % (b, len(lettori), len(come_legge), len(come_altro)))
        for f, tt in come_legge:
            stampa("      LEGGE    %-34s [%s]" % (f, tt))
        for f, tt in come_altro[:14]:
            stampa("      altro    %-34s [%s]" % (f, tt))
        if len(come_altro) > 14:
            stampa("      ... e altre %d" % (len(come_altro) - 14))
        stampa("")

    # ------------------------------------------------------------- RUNTIME
    stampa("=" * 104)
    stampa("A RUNTIME: CHI HA LETTO DAVVERO, in %d passo/i di questa scena" % passi)
    stampa("=" * 104)
    conti, _base = sorveglia_runtime(net, S)
    with contextlib.redirect_stdout(io.StringIO()):
        for _ in range(passi):
            _passo.passo_pieno(S, net)
    run = {}
    for b in BERSAGLI:
        voci = sorted(conti[b].items(), key=lambda x: -x[1])
        dentro_legge = [(f, k) for f, k in voci
                        if tipi.get(f) and (set(tipi[f]) - set(non_leggi))]
        run[b] = {"lettori": len(voci), "letture_totali": int(sum(k for _, k in voci)),
                  "dentro_una_legge": [{"funzione": f, "letture": int(k)}
                                       for f, k in dentro_legge],
                  "tutti": [{"funzione": f, "letture": int(k)} for f, k in voci[:30]]}
        stampa("  `%s`: %d lettori distinti, %d letture in totale"
               % (b, len(voci), run[b]["letture_totali"]))
        for f, k in voci[:12]:
            tt = tipi.get(f)
            et = ("LEGGE" if tt and (set(tt) - set(non_leggi)) else
                  (",".join(sorted(tt)) if tt else "fuori dal passo"))
            stampa("      %-34s %8d   [%s]" % (f, k, et))
        if len(voci) > 12:
            stampa("      ... e altri %d lettori" % (len(voci) - 12))
        stampa("")

    # ------------------------------------------------------------- IL VERDETTO
    stampa("=" * 104)
    stampa("IL VERDETTO: la posizione del figlio e' FISICA o solo DISEGNO?")
    stampa("=" * 104)
    pos_legge = riassunto["pos"]["funzioni_legge"]
    stampa("  `pos` letta DENTRO UNA LEGGE (statica): %d funzioni" % len(pos_legge))
    stampa("  `pos` letta dentro una legge (runtime): %d funzioni"
           % len(run["pos"]["dentro_una_legge"]))
    if pos_legge:
        stampa("  ### ➜ `pos` E' FISICA, non solo disegno: ci sono leggi che la leggono.")
        stampa("        Allora la frazione `t` decide ANCHE una posizione, non solo una lunghezza,")
        stampa("        e `DIVISIONE-AUTOCONSISTENTE` non puo' trattarla come un dettaglio di resa.")
    else:
        stampa("  ### ➜ Nessuna LEGGE legge `pos`: sarebbe solo DISEGNO, e `t` conterebbe solo")
        stampa("        per `d`/`d0`. ⚠ Da confrontare con `SCHW-CORTI`, che dice il contrario:")
        stampa("        se i due si contraddicono, VINCE LA LETTURA DEL CODICE e si cerca l'errore")
        stampa("        in questo strumento.")

    fuori = {"blob_sim_sha1_byte": blob(SIM), "blob_strumento": blob(os.path.abspath(__file__)),
             "passi": passi, "tipi_non_leggi": non_leggi,
             "statica": riassunto, "runtime": run,
             "verdetto_pos_letta_da_una_legge": bool(pos_legge)}
    json.dump(fuori, io.open(os.path.join(FUORI, "_pos_contro_d.json"), "w", encoding="utf-8"),
              indent=1, ensure_ascii=False)
    io.open(os.path.join(FUORI, "_corsa.txt"), "w", encoding="utf-8").write(chr(10).join(P))
    stampa("")
    stampa("scritto: %s" % os.path.join(FUORI, "_pos_contro_d.json"))
    return 0


if __name__ == "__main__":
    sys.exit(principale())
