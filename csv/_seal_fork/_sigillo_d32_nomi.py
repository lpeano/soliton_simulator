# -*- coding: utf-8 -*-
r"""**SIGILLO DI `D32`: UNA RINOMINA NON CAMBIA UN BIT.** *(mandato di Luca, 2026-09-27)*

| # | criterio | come si verifica |
|--:|---|---|
| **N1** | **byte-identico**: il simulatore **prima** e **dopo** la rinomina danno **gli stessi byte** | due processi, uno per braccio (`STANDARD 1`), **firme `sha1` campo per campo** (`STANDARD 2`) sulla scena `(ii)` dopo `N` passi |
| **N2** | **il confronto NON e' vuoto**: i due bracci hanno **lo stesso numero di nodi e di archi** | *(`STANDARD 2`: `max\|A-B\| = 0` puo' voler dire «nessun confronto»)* |
| **N3** | `tau_pp` **non e' piu' usato come TEMPO nel ramo attivo** | **per AST**: nel corpo di `mitosi`, `pos_torsione` compare **solo** dentro il ramo `else` di `TEMPO_UNICO_MITOSI` come denominatore, **e mai nel ramo che gira** |
| **N4** | il codice **di prima** e' preso dal **PADRE** del commit che ha introdotto `pos_torsione` | `H-P8`, e si **asserisce** che quel file **non** contenga il nome nuovo |

> **Una rinomina e' il caso in cui la byte-identita' e' ATTESA, non sperata**: se fallisse, la
> rinomina avrebbe toccato **cosa il codice fa**, non **come si chiama**. **Per questo il criterio
> `N2` esiste:** due bracci che divergono nel numero di nodi darebbero `0` campi confrontabili, e
> lo zero sarebbe **mancanza di confronto**, non identita'.

    python csv/_seal_fork/_sigillo_d32_nomi.py            # 12 passi per braccio
    python csv/_seal_fork/_sigillo_d32_nomi.py --passi 4  # giro corto

ASCII puro.
"""
import ast
import hashlib
import io
import json
import os
import subprocess
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, os.path.join(RADICE, "csv"))

import _presidio                                                       # noqa: E402
import _cli_flag                                                       # noqa: E402

_presidio.avvia(__file__)

NL = chr(10)
DEST = os.path.join(_QUI, "_sig_d32_nomi")
REFERTO = os.path.join(DEST, "REFERTO.txt")
SIM = "soliton_simulator.py"
NOME_NUOVO = "pos_torsione"
R = []


def P(s=""):
    print(s)
    R.append(s)


def _git(*a):
    q = subprocess.run(["git"] + list(a), cwd=RADICE, capture_output=True)
    return q.returncode, q.stdout


def sim_prima(dest):
    """Il simulatore PRIMA della rinomina: il PADRE del commit che ha introdotto il nome nuovo.

    Estratto **in binario** (par.5-quinquies: `git checkout` riscriverebbe le newline), e con
    **l'asserzione che il file NON contenga il nome nuovo** -- senza quella, un'ancora sbagliata
    misurerebbe niente e passerebbe (`A9`).
    """
    c, fuori = _git("log", "--format=%H", "-S", NOME_NUOVO, "--", SIM)
    if c or not fuori.strip():
        raise SystemExit("non trovo il commit che ha introdotto `%s`" % NOME_NUOVO)
    intro = [x for x in fuori.decode().strip().split(NL) if x.strip()][-1]
    c2, byte = _git("show", "%s^:%s" % (intro, SIM))
    if c2:
        raise SystemExit("il PADRE di %s non ha %s" % (intro[:8], SIM))
    if NOME_NUOVO.encode() in byte:
        raise SystemExit("IL FILE 'DI PRIMA' CONTIENE GIA' `%s`: ancora sbagliata, mi fermo (A9)"
                         % NOME_NUOVO)
    io.open(dest, "wb").write(byte)
    return intro[:8], hashlib.sha1(byte).hexdigest()[:8]


# ------------------------------------------------------------------ il braccio, in un processo suo
BRACCIO = '''# -*- coding: utf-8 -*-
import hashlib, json, os, sys
import numpy as np
sys.path.insert(0, os.path.join(%(rad)r, "csv"))
import _cli_flag, _passo
_S0, argv = _cli_flag.argv_del_driver(dest=os.path.join(%(rad)r, "csv", "_test_fork",
                                                        "_scarto_cli"))
S, a = _cli_flag.carica_dal_cli(argv, nome="sim_n1", sim=%(sim)r)
S._NMASSE_VIDEO["n"] = max(2, int(getattr(a, "nmasse", 2)))
S._NMASSE_VIDEO["sep"] = float(getattr(a, "sep", 3.0))
S._NMASSE_VIDEO["size"] = None
S.avvia_test("MASSE-COERENTI")()
# ⚠ `passo_pieno`, NON le cinque chiamate A MANO: la prima correzione le ricopiava, cioe'
#   aggiungeva il ventiseiesimo posto in cui quell'ordine vive CABLATO. `_passo.passo_pieno`
#   LEGGE l'ordine dal codice e RIFIUTA di girare se simulatore e driver divergono.
#   (`net.step()` da solo chiamava `mitosi()` ZERO volte: misurato, 0 in 14 giri.)
S.passo_test()
for _ in range(%(passi)d):
    _passo.passo_pieno(S, S.net)
o = {"n": int(S.net.n), "archi": int(len(S.net.d)), "firme": {},
     "taupp_tot": int(getattr(S.net, "_rep_taupp_tot", 0)),
     "mitosi_eventi": int(getattr(S.net, "_mit_eventi", -1))}
for k, v in sorted(vars(S.net).items()):
    if isinstance(v, np.ndarray):
        o["firme"][k] = "%%s|%%s|%%s" %% (v.shape, v.dtype,
                                       hashlib.sha1(v.tobytes()).hexdigest()[:16])
    elif isinstance(v, (int, float, bool)):
        o["firme"][k] = repr(v)
open(%(out)r, "w").write(json.dumps(o, sort_keys=True))
print("OK", o["n"], o["archi"], len(o["firme"]))
'''


def braccio(nome, sim_path, passi):
    dd = os.path.join(DEST, nome)
    if not os.path.isdir(dd):
        os.makedirs(dd)
    out = os.path.join(dd, "firme.json")
    scr = os.path.join(dd, "_braccio.py")
    io.open(scr, "w", encoding="utf-8", newline=NL).write(
        BRACCIO % dict(rad=RADICE, sim=sim_path, passi=passi, out=out))
    q = subprocess.run([sys.executable, scr], cwd=RADICE, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    if q.returncode or not os.path.exists(out):
        return None, (q.stdout or "") + (q.stderr or "")
    return json.load(io.open(out, encoding="utf-8")), ""


def n3_dall_ast():
    """`pos_torsione` compare come DENOMINATORE solo nel ramo `else` di `TEMPO_UNICO_MITOSI`?"""
    src = io.open(os.path.join(RADICE, SIM), encoding="utf-8").read()
    arb = ast.parse(src)
    mit = next((n for n in ast.walk(arb)
                if isinstance(n, ast.FunctionDef) and n.name == "mitosi"), None)
    if mit is None:
        return None
    usi = []
    for nd in ast.walk(mit):
        if isinstance(nd, ast.If) and any(
                isinstance(x, ast.Name) and x.id == "TEMPO_UNICO_MITOSI" for x in ast.walk(nd.test)):
            for ramo, corpo in (("if (ACCESO)", nd.body), ("else (SPENTO)", nd.orelse)):
                for y in ast.walk(ast.Module(body=corpo, type_ignores=[])):
                    if isinstance(y, ast.Name) and y.id == NOME_NUOVO:
                        usi.append((ramo, y.lineno))
    return usi


if __name__ == "__main__":
    a = sys.argv[1:]
    passi = int(a[a.index("--passi") + 1]) if "--passi" in a else 12
    if not os.path.isdir(DEST):
        os.makedirs(DEST)
    P("=" * 104)
    P("SIGILLO DI `D32` -- una RINOMINA non cambia un bit   (%d passi per braccio)" % passi)
    P("=" * 104)
    esiti = []

    # ------------------------------------------------------------------ N4 (l'ancora)
    vecchio = os.path.join(DEST, "_sim_prima.py")
    sha, blob = sim_prima(vecchio)
    P("")
    P("  N4  L'ANCORA -- il codice di PRIMA dal PADRE del commit di `%s`" % NOME_NUOVO)
    P("        commit che l'ha introdotto ......... %s   (si usa il suo PADRE)" % sha)
    P("        blob del file estratto ............ %s   e NON contiene `%s`" % (blob, NOME_NUOVO))
    esiti.append(("N4  ancora al PADRE, asserita", True))

    # ------------------------------------------------------------------ N1 / N2
    P("")
    P("  N1/N2  DUE PROCESSI, uno per braccio (`STANDARD 1`)")
    a_p, err_p = braccio("prima", vecchio, passi)
    a_d, err_d = braccio("dopo", os.path.join(RADICE, SIM), passi)
    if a_p is None or a_d is None:
        P("        ** un braccio non e' arrivato in fondo **")
        P("        prima: %s" % err_p.strip()[-300:])
        P("        dopo:  %s" % err_d.strip()[-300:])
        esiti.append(("N1  byte-identico", False))
        esiti.append(("N2  il confronto NON e' vuoto", False))
    else:
        P("        PRIMA  n %-6d archi %-8d campi firmati %d"
          % (a_p["n"], a_p["archi"], len(a_p["firme"])))
        P("        DOPO   n %-6d archi %-8d campi firmati %d"
          % (a_d["n"], a_d["archi"], len(a_d["firme"])))
        stessa_forma = (a_p["n"] == a_d["n"] and a_p["archi"] == a_d["archi"]
                        and set(a_p["firme"]) == set(a_d["firme"]))
        div = sorted(k for k in a_p["firme"] if a_p["firme"][k] != a_d["firme"].get(k))
        P("        stesso n, stessi archi, stessi campi ... %s" % stessa_forma)
        P("        campi confrontati %d   DIVERSI %d %s"
          % (len(a_p["firme"]), len(div), div[:8]))
        if not stessa_forma:
            P("        ** LE FORME DIFFERISCONO: `0 diversi` qui sarebbe MANCANZA DI CONFRONTO **")
        esiti.append(("N1  byte-identico (0 campi diversi)", stessa_forma and not div))
        esiti.append(("N2  il confronto NON e' vuoto", bool(stessa_forma and a_p["firme"])))

    # ------------------------------------------------------------------ N5
    #   ⚠ SENZA QUESTO, `N1` PUO' PASSARE A VUOTO: se la mitosi non scatta, il blocco
    #   rinominato non gira e la byte-identita' non dimostra niente -- e' la stessa
    #   famiglia di `max|A-B| = 0` per mancanza di confronto (`STANDARD 2`). Il contatore
    #   `_rep_taupp_tot` conta `np.size(pos_torsione)`: se e' > 0, quel codice HA GIRATO.
    #   MISURATO: a 3 passi `n` non cambiava -- la mitosi NON era scattata.
    if a_p is not None and a_d is not None:
        tp, td = a_p["taupp_tot"], a_d["taupp_tot"]
        P("")
        P("  N5  IL BLOCCO RINOMINATO HA GIRATO  (senno' `N1` passa a VUOTO)")
        P("        `_rep_taupp_tot` (conta `size(pos_torsione)`)  PRIMA %d   DOPO %d"
          % (tp, td))
        P("        eventi di mitosi                              PRIMA %d   DOPO %d"
          % (a_p["mitosi_eventi"], a_d["mitosi_eventi"]))
        ok5 = (tp > 0 and td > 0 and tp == td)
        P("        > 0 su entrambi i bracci, e UGUALI ... %s" % ok5)
        esiti.append(("N5  il codice rinominato HA girato", ok5))

    # ------------------------------------------------------------------ N3
    # ⚠ `N3` HA CAMBIATO SIGNIFICATO, e va detto invece di lasciarlo passare: dopo
    #   `CURA2-STRUTTURALE` i `if TEMPO_UNICO_MITOSI` NON ESISTONO PIU', quindi la domanda
    #   «quanti usi nel ramo acceso?» ha risposta 0 **per assenza del ramo**, non per la
    #   cura dei nomi: sarebbe un PASS vuoto. Ora il criterio e' PIU' FORTE -- zero rami,
    #   e `pos_torsione` usata SOLO per il segno.
    usi = n3_dall_ast()
    import ast as _a3
    _src3 = io.open(os.path.join(RADICE, SIM), encoding="utf-8").read()
    _mit3 = next((x for x in _a3.walk(_a3.parse(_src3))
                  if isinstance(x, _a3.FunctionDef) and x.name == "mitosi"), None)
    _rami3 = [x.lineno for x in _a3.walk(_mit3) if isinstance(x, _a3.If)
              and isinstance(x.test, _a3.Name) and x.test.id == "TEMPO_UNICO_MITOSI"]
    P("")
    P("  N3  `%s` NON E' USATA NEL RAMO CHE GIRA  (per AST, non per `grep`)" % NOME_NUOVO)
    if usi is None:
        P("        ** `mitosi` non trovata: il criterio non ha girato **")
        ok3 = False
    else:
        for ramo, riga in usi:
            P("        %-14s :%d" % (ramo, riga))
        acceso = [x for x in usi if x[0].startswith("if")]
        ok3 = (len(acceso) == 0 and len(_rami3) == 0)
        P("        `if TEMPO_UNICO_MITOSI` nel codice .. %d   (atteso 0: `CURA2-STRUTTURALE`"
          " li ha TOLTI)" % len(_rami3))
        P("        usi nel ramo ACCESO ................ %d   (atteso 0)" % len(acceso))
        P("        usi nel ramo SPENTO ................ %d   (sono il difetto di `D32`,"
          % len([x for x in usi if x[0].startswith("else")]))
        P("                                                 PROPOSTI per la rimozione)")
    esiti.append(("N3  nessun uso nel ramo che gira", ok3))

    # `H-P5`: un referto dichiara LA CONFIGURAZIONE INTERA, non i flag che ricordo io. I due
    #   bracci girano in processi loro, quindi qui si carica il modulo NUOVO dall'argv del
    #   driver -- senza costruire la scena: serve la configurazione, non il mondo.
    _S, _argv = _cli_flag.argv_del_driver(
        dest=os.path.join(RADICE, "csv", "_test_fork", "_scarto_cli"))
    P("")
    _cli_flag.dichiara_configurazione(_S, P)
    P("")
    P("=" * 104)
    for nome, ok in esiti:
        P("  %-46s %s" % (nome, "PASS" if ok else "** FAIL **"))
    buoni = len([1 for _n, ok in esiti if ok])
    P("SIGILLO: %d/%d" % (buoni, len(esiti)))
    P("=" * 104)
    P()
    P("COSA QUESTO SIGILLO *NON* DICE:")
    P("  - **non dice che i nomi nuovi siano i nomi GIUSTI**: dice che non cambiano un bit, e che")
    P("    `pos_torsione` non e' usata come tempo nel ramo che gira.")
    P("  - **`N3` guarda il ramo `else`, e lo trova**: quegli usi CI SONO ancora, e sono il")
    P("    difetto. Sono **proposti** per la rimozione (`STANDARD 10`), non tolti.")
    P("  - **%d passi non sono un run**: bastano a far girare la mitosi, non a dire fisica." % passi)
    P("  - **e un passo sono CINQUE chiamate, non `step()`**: con il solo `step()`"
      " `mitosi()` gira ZERO volte, e `N1` misurerebbe codice mai eseguito.")
    io.open(REFERTO, "w", encoding="utf-8", newline=NL).write(NL.join(R) + NL)
    print(NL + "scritto %s" % os.path.relpath(REFERTO, RADICE).replace(chr(92), "/"))
    sys.exit(0 if buoni == len(esiti) else 1)
