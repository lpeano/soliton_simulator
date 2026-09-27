# -*- coding: utf-8 -*-
"""**I RAMI MORTI COL DRIVER, dentro cio' che la cura (c) di `ETC-PASSO` riscrivera'.**

**Perimetro (decisione di Luca, 2026-09-27):** **solo** le cinque leggi del passo pieno e **cio'
che chiamano**. Il resto di `CLIP-INVENTARIO` resta voce aperta, **da fare dopo la cura**.

**IL CRITERIO E' DECISO DAI FLAG, NON DAL CAMPIONAMENTO**, e la differenza e' tutta:
  - un ramo **MORTO** e' un ramo la cui condizione dipende **solo da flag di modulo** e che, coi
    valori dell'argv del driver, **non puo' essere raggiunto**. E' una proprieta' della
    configurazione, **non di un giro**;
  - un ramo **NON ESERCITATO** e' un ramo che in `N` passi non e' girato **ma potrebbe**. **Non e'
    morto**, e archiviarlo sarebbe un errore.
**Un conteggio basato sui soli 3 passi non distinguerebbe le due cose**, ed e' l'errore che questo
strumento esiste per non fare.

**COME:**
1. si configura il modulo con l'**argv COSTRUITO DAL DRIVER** (non ricostruito) e si leggono i
   valori effettivi dei flag di modulo;
2. si calcolano le funzioni **raggiungibili** dalle cinque leggi *(l'ordine viene da `csv/_passo.py`)*;
3. per ogni `if`/`elif` e per ogni **ternario**, si prova a **valutare il test** in un ambiente che
   contiene **solo** i flag di modulo. Se ci riesce: il ramo che risulta **irraggiungibile e' MORTO**
   e si dice **quale** (`if` oppure `else`). Se il test contiene nomi di *runtime*, e'
   **NON DECIDIBILE** e non entra nell'elenco;
4. **CORROBORAZIONE con la COPERTURA DI RIGA** *(`sys.settrace`, 3 passi pieni)*: un ramo dichiarato
   morto che **esegue** e' un difetto DELL'ANALISI, e lo strumento lo urla.

**⚠ I LIMITI (`A9`):** i flag si leggono **una volta**, dopo la configurazione; un flag che venisse
riassegnato **durante** il passo renderebbe il verdetto falso *(nessuno lo fa oggi, ma non e'
verificato)*. E la raggiungibilita' e' **statica e per nome**: alias e `getattr` non si vedono.

COMANDO:  python csv/_test_fork/_etc_rami_morti.py [--passi=3]
"""
import ast
import hashlib
import io
import json
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, os.path.join(RADICE, "csv"))
import _presidio  # noqa: E402

_presidio.avvia(__file__)
import _cli_flag  # noqa: E402
import _passo  # noqa: E402

SIM = os.path.join(RADICE, "soliton_simulator.py")
SRC = io.open(SIM, encoding="utf-8").read()
RIG = SRC.split(chr(10))
ARB = ast.parse(SRC)

METODI, FUNZIONI = {}, {}
for _n in ast.walk(ARB):
    if isinstance(_n, ast.ClassDef) and _n.name == "Rete":
        for _k in _n.body:
            if isinstance(_k, (ast.FunctionDef, ast.AsyncFunctionDef)):
                METODI[_k.name] = _k
for _n in ARB.body:
    if isinstance(_n, ast.FunctionDef):
        FUNZIONI[_n.name] = _n


def raggiungibili(leggi):
    visti, coda = set(), list(leggi)
    while coda:
        x = coda.pop()
        if x in visti:
            continue
        visti.add(x)
        c = METODI.get(x) or FUNZIONI.get(x)
        if c is None:
            continue
        for n in ast.walk(c):
            if isinstance(n, ast.Call):
                f = n.func
                nm = f.attr if isinstance(f, ast.Attribute) else (
                    f.id if isinstance(f, ast.Name) else None)
                if nm and (nm in METODI or nm in FUNZIONI) and nm not in visti:
                    coda.append(nm)
    return visti


def contenitore(linea, vive):
    """La funzione VIVA piu' interna che contiene `linea`."""
    dentro = None
    for nome in vive:
        c = METODI.get(nome) or FUNZIONI.get(nome)
        if c is None:
            continue
        if c.lineno <= linea <= (c.end_lineno or c.lineno):
            if dentro is None or c.lineno > dentro[0]:
                dentro = (c.lineno, nome)
    return dentro[1] if dentro else None


def principale():
    passi = 3
    for x in sys.argv[1:]:
        if x.startswith("--passi="):
            passi = int(x.split("=", 1)[1])

    blob = hashlib.sha1(io.open(SIM, "rb").read()).hexdigest()
    S0, argv = _cli_flag.argv_del_driver(extra=["--seme=11"],
                                        dest=os.path.join(_QUI, "_scarto_cli"))
    S, a = _cli_flag.carica_dal_cli(list(argv), nome="sim_rami")
    print("simulatore blob sha1-BYTE %s" % blob[:8])
    print("CONFIGURAZIONE INTERA (%d voci): %s" % (len(argv), " ".join(argv[1:])))
    print("")

    # ------------------------------------------------------------------ i FLAG del run
    FLAG = {}
    for k, v in vars(S).items():
        if k.isupper() and isinstance(v, (bool, int, float, str, type(None))):
            FLAG[k] = v
    print("flag di modulo leggibili: %d" % len(FLAG))

    LEGGI = [n for _t, n in _passo.ordine()]
    VIVE = raggiungibili(LEGGI)
    print("le cinque leggi: " + " -> ".join(LEGGI))
    print("funzioni RAGGIUNGIBILI (il perimetro della cura (c)): %d" % len(VIVE))
    print("")

    # ------------------------------------------------------------------ i rami decidibili
    def valuta(test):
        """(valore, nomi) se il test dipende SOLO da flag; (None, nomi) altrimenti."""
        nomi = sorted({n.id for n in ast.walk(test) if isinstance(n, ast.Name)})
        if not nomi or any(n not in FLAG for n in nomi):
            return None, nomi
        try:
            return bool(eval(compile(ast.Expression(test), "<test>", "eval"),
                             {"__builtins__": {}}, dict(FLAG))), nomi
        except Exception:
            return None, nomi

    MORTI, NONDEC = [], 0
    for nome in sorted(VIVE):
        c = METODI.get(nome) or FUNZIONI.get(nome)
        if c is None:
            continue
        for n in ast.walk(c):
            if isinstance(n, ast.If):
                v, nomi = valuta(n.test)
                if v is None:
                    NONDEC += 1
                    continue
                if v is False:
                    a0, z0 = n.body[0].lineno, n.body[-1].end_lineno or n.body[-1].lineno
                    _vive = []
                    for s in n.orelse:
                        _vive += list(range(s.lineno, (s.end_lineno or s.lineno) + 1))
                    MORTI.append({"tipo": "if", "dentro": nome, "riga": n.lineno,
                                  "righe_morte": [a0, z0], "righe_vive": _vive,
                                  "righe_test": list(range(n.test.lineno,
                                                           (n.test.end_lineno or n.test.lineno) + 1)),
                                  "test": ast.unparse(n.test)[:90],
                                  "flag": [x for x in nomi if x in FLAG],
                                  "valori": {x: FLAG[x] for x in nomi if x in FLAG},
                                  "perche": "il test e' FALSO coi flag del driver",
                                  "sorgente": RIG[n.lineno - 1].strip()[:110]})
                elif v is True and n.orelse:
                    a0 = n.orelse[0].lineno
                    z0 = n.orelse[-1].end_lineno or n.orelse[-1].lineno
                    _vive = []
                    for s in n.body:
                        _vive += list(range(s.lineno, (s.end_lineno or s.lineno) + 1))
                    MORTI.append({"tipo": "else", "dentro": nome, "riga": n.lineno,
                                  "righe_morte": [a0, z0], "righe_vive": _vive,
                                  "righe_test": list(range(n.test.lineno,
                                                           (n.test.end_lineno or n.test.lineno) + 1)),
                                  "test": ast.unparse(n.test)[:90],
                                  "flag": [x for x in nomi if x in FLAG],
                                  "valori": {x: FLAG[x] for x in nomi if x in FLAG},
                                  "perche": "il test e' VERO coi flag del driver: muore l'else",
                                  "sorgente": RIG[n.lineno - 1].strip()[:110]})
            elif isinstance(n, ast.IfExp):
                v, nomi = valuta(n.test)
                if v is None:
                    NONDEC += 1
                    continue
                ramo = n.orelse if v else n.body
                vivo = n.body if v else n.orelse
                MORTI.append({"tipo": "ternario", "dentro": nome, "riga": n.lineno,
                              "righe_morte": [ramo.lineno, ramo.end_lineno or ramo.lineno],
                              "righe_vive": list(range(vivo.lineno,
                                                       (vivo.end_lineno or vivo.lineno) + 1)),
                              "righe_test": list(range(n.test.lineno,
                                                       (n.test.end_lineno or n.test.lineno) + 1)),
                              "test": ast.unparse(n.test)[:90],
                              "flag": [x for x in nomi if x in FLAG],
                              "valori": {x: FLAG[x] for x in nomi if x in FLAG},
                              "perche": ("muore il ramo %s: il test e' %s coi flag del driver"
                                         % ("`else`" if v else "`if`", v)),
                              "sorgente": RIG[n.lineno - 1].strip()[:110]})

    # ⚠ LA COPERTURA PER RIGA NON BASTA A CORROBORARE UN RAMO, e la prima stesura ci e' caduta:
    #   in un TERNARIO (`x if F else y`) e in un `if F: y` su UNA riga, il ramo morto **condivide
    #   la riga** con quello vivo. Dichiarare morta quella riga e poi vederla eseguire non prova
    #   che l'analisi sbagli: prova che la RIGA non e' l'unita' giusta.
    #   **Lo strumento me l'ha urlato al primo giro: 37 righe <<morte>> avevano eseguito.**
    #   Quindi si corrobora **solo sulle righe ESCLUSIVE** del ramo morto -- quelle che non
    #   ospitano ne' il test ne' il ramo vivo -- e i rami senza righe esclusive si contano a parte,
    #   dichiarati NON CORROBORABILI PER RIGA.
    #   ⚠ E SI TOLGONO ANCHE LE RIGHE DEL **TEST**, non solo `n.lineno`: in un ternario scritto
    #     su due righe -- `x = (A` / `if F else B)` -- il test sta sulla SECONDA riga, insieme al
    #     ramo morto, mentre `n.lineno` e' la PRIMA. Togliere solo `n.lineno` lasciava dentro la
    #     riga del test, e **lo strumento l'ha beccato**: restava UN solo contraddittorio, `:5272`,
    #     ed era proprio questa forma (`chi_core = (... if CHI_COOP else ...)`).
    for m in MORTI:
        a0, z0 = m["righe_morte"]
        esc = (set(range(a0, z0 + 1)) - set(m.get("righe_vive", []))
               - set(m.get("righe_test", [])) - {m["riga"]})
        m["righe_esclusive"] = sorted(esc)
    righe_morte = set()
    for m in MORTI:
        righe_morte.update(m["righe_esclusive"])
    senza_esclusive = [m for m in MORTI if not m["righe_esclusive"]]

    print("=" * 96)
    print("RAMI MORTI COL DRIVER, dentro il perimetro della cura (c)")
    print("=" * 96)
    print("")
    print("  rami MORTI (decisi dai flag)     : %d" % len(MORTI))
    print("  test NON DECIDIBILI (runtime)    : %d   <- NON entrano nell'elenco" % NONDEC)
    print("  righe ESCLUSIVE del ramo morto   : %d" % len(righe_morte))
    print("  rami NON CORROBORABILI per riga  : %d   (il ramo morto condivide la riga col vivo:"
          % len(senza_esclusive))
    print("                                        ternari e `if` su una riga sola)")
    print("")

    # ------------------------------------------------------------------ corroborazione
    VISTE = set()

    def _tr(frame, ev, _arg):
        if frame.f_code.co_filename != SIM:
            return None
        if ev == "line" and frame.f_lineno in righe_morte:
            VISTE.add(frame.f_lineno)
        return _tr

    S._NMASSE_VIDEO["n"] = 2
    S._NMASSE_VIDEO["sep"] = 3.0
    S._NMASSE_VIDEO["size"] = None
    S.avvia_test("MASSE-COERENTI")()
    net = S.net
    print("  CORROBORAZIONE: %d passi pieni su n = %d, m = %d, con la copertura attiva sulle"
          % (passi, net.n, len(net.i)))
    print("  %d righe dichiarate morte..." % len(righe_morte))
    sys.settrace(_tr)
    try:
        for _ in range(passi):
            _passo.passo_pieno(S, net)
    finally:
        sys.settrace(None)
    print("")
    if VISTE:
        print("  ### %d RIGHE ESCLUSIVE DI UN RAMO MORTO HANNO ESEGUITO: L'ANALISI E' SBAGLIATA."
              % len(VISTE))
        print("      righe: %s" % sorted(VISTE)[:20])
    else:
        print("  ### ZERO righe dichiarate morte hanno eseguito: la copertura CONFERMA i flag.")
    print("")

    # ------------------------------------------------------------------ la tabella
    print("=" * 96)
    print("LA TABELLA")
    print("=" * 96)
    print("")
    print("  %-6s %-26s %-6s %-9s %s" % ("riga", "dentro", "tipo", "morte", "flag = valore"))
    for m in sorted(MORTI, key=lambda x: x["riga"]):
        n_righe = m["righe_morte"][1] - m["righe_morte"][0] + 1
        print("  :%-5d %-26s %-6s %-9s %s"
              % (m["riga"], m["dentro"], m["tipo"], "%d righe" % n_righe,
                 ", ".join("%s=%s" % (k, v) for k, v in sorted(m["valori"].items()))[:46]))
    print("")
    perflag = {}
    for m in MORTI:
        for f in m["flag"]:
            perflag[f] = perflag.get(f, 0) + 1
    print("  I FLAG COINVOLTI, per quanti rami ciascuno (%d flag distinti):" % len(perflag))
    for f, c in sorted(perflag.items(), key=lambda x: (-x[1], x[0])):
        print("    %-26s %3d rami   (valore col driver: %s)" % (f, c, FLAG.get(f)))

    OUT = os.path.join(_QUI, "_etc_rami_morti.json")
    io.open(OUT, "w", encoding="utf-8", newline=chr(10)).write(json.dumps(
        {"blob_sim": blob, "argv": argv[1:], "leggi": LEGGI, "funzioni_vive": sorted(VIVE),
         "n_morti": len(MORTI), "n_non_decidibili": NONDEC,
         "righe_esclusive_totali": len(righe_morte),
         "n_non_corroborabili_per_riga": len(senza_esclusive),
         "copertura_ha_eseguito": sorted(VISTE), "passi": passi,
         "flag_coinvolti": perflag, "morti": sorted(MORTI, key=lambda x: x["riga"])},
        indent=1, ensure_ascii=False, sort_keys=True))
    print("")
    print("scritto: " + OUT)
    return 0 if not VISTE else 2


if __name__ == "__main__":
    sys.exit(principale())
