r"""**`W5` — L'A/B DI `POZZO-D`**: la distanza fra le masse, flag ON contro OFF, **4 semi**.

*(criterio `W5` del task history `doc/TASK_HISTORY/2026-09-27_d02-pozzo-d.md`, scritto **prima**.)*

**COME**, e ogni scelta e' quella che le regole impongono:

* **scena `(ii)`(a)** in configurazione del **driver**, `--sep 6.1158`;
* **`120` passi** *(giro corto: Luca ha detto niente run lungo)*, avanzati con **`passo_pieno`**
  (`H-P9`) — **mai `net.step()` da solo**;
* **UN PROCESSO PER BRACCIO** (`STANDARD 1`): `4 semi x 2 bracci = 8 processi`;
* la distanza fra le masse **lungo il grafo pesato con `d`**, da **`csv/_osservabile_p1.py`**
  *(centro = medoide di grafo, nessun `pos`)*;
* **la barra e' quella FRA SEMI** (`P3`), col `t` di Student per **3** gradi di liberta'.

> ### ⚠ **IL NULLO NON E' ZERO, ed e' scritto prima di guardare.**
> Al **passo 0** la dispersione fra semi della distanza vale **`sd 0.146`-`0.510`** su distanze
> `~10.7` *(misurato ieri, `OSSERVABILE-P1` `K5`)*. **Un effetto piu' piccolo di quello non si
> legge.** E poiche' i bracci sono **appaiati sul seme**, si guarda **la differenza per seme**, che
> ha una barra piu' piccola della dispersione assoluta.

    python csv/_test_fork/_ab_pozzo_d.py               # 4 semi, 120 passi
    python csv/_test_fork/_ab_pozzo_d.py --passi 12    # giro corto d'impianto

ASCII puro.
"""
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
import _osservabile_p1 as OP                                           # noqa: E402

_presidio.avvia(__file__)

NL = chr(10)
DEST = os.path.join(_QUI, "_ab_pozzo_d")
REFERTO = os.path.join(DEST, "REFERTO.txt")
SEMI = [11, 12, 13, 14]
R = []


def P(s=""):
    print(s)
    R.append(s)


BRACCIO = '''# -*- coding: utf-8 -*-
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.join(%(rad)r, "csv"))
import _cli_flag, _passo, _osservabile_p1 as OP
_S0, argv = _cli_flag.argv_del_driver(extra=["--seme=%(seme)d"],
                                     dest=os.path.join(%(rad)r, "csv", "_test_fork",
                                                       "_scarto_cli"))
argv = list(argv) + (["--pozzo-d"] if %(flag)s else [])
S, a = _cli_flag.carica_dal_cli(argv, nome="sim_ab")
S._NMASSE_VIDEO["n"] = max(2, int(getattr(a, "nmasse", 2)))
S._NMASSE_VIDEO["sep"] = float(getattr(a, "sep", 3.0))
S._NMASSE_VIDEO["size"] = None
S.avvia_test("MASSE-COERENTI")()
coorti = S.test["dati"]["coorti"]
rr = float(S.test["dati"]["scena_ii"]["r_regione"])
o0 = OP.misura(S.net, coorti)                       # la distanza al PASSO 0
if hasattr(S, "passo_test"):
    S.passo_test()
for _ in range(%(passi)d):
    _passo.passo_pieno(S, S.net)                    # `H-P9`: mai `net.step()` da solo
o1 = OP.misura(S.net, coorti)                       # e dopo i passi
fuori = {"seme": %(seme)d, "flag": bool(S.POZZO_D), "n0": int(o0["n"]), "n1": int(o1["n"]),
         "sep": float(S._NMASSE_VIDEO["sep"]), "r_regione": rr,
         "nonpos": int(getattr(S.net, "_pozzo_d_nonpos", -1)),
         "passo0": dict((k, float(v["centro_centro"])) for k, v in o0["coppie"].items()),
         "dopo": dict((k, float(v["centro_centro"])) for k, v in o1["coppie"].items())}
open(%(out)r, "w").write(json.dumps(fuori, sort_keys=True))
print("OK", %(seme)d, %(flag)s, fuori["n0"], fuori["n1"])
'''


def braccio(seme, flag, passi):
    nome = "seme%d_%s" % (seme, "on" if flag else "off")
    dd = os.path.join(DEST, nome)
    if not os.path.isdir(dd):
        os.makedirs(dd)
    out = os.path.join(dd, "misura.json")
    scr = os.path.join(dd, "_braccio.py")
    io.open(scr, "w", encoding="utf-8", newline=NL).write(
        BRACCIO % dict(rad=RADICE, seme=seme, flag=bool(flag), passi=passi, out=out))
    q = subprocess.run([sys.executable, scr], cwd=RADICE, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    if q.returncode or not os.path.exists(out):
        return None, (q.stdout or "") + (q.stderr or "")
    return json.load(io.open(out, encoding="utf-8")), ""


if __name__ == "__main__":
    a = sys.argv[1:]
    passi = int(a[a.index("--passi") + 1]) if "--passi" in a else 120
    if not os.path.isdir(DEST):
        os.makedirs(DEST)
    P("=" * 104)
    P("`W5` -- A/B DI `POZZO-D`: la distanza fra le masse, ON contro OFF   (%d passi, %d semi)"
      % (passi, len(SEMI)))
    P("=" * 104)
    P("  un processo per braccio (`STANDARD 1`): %d bracci. Avanzamento `passo_pieno` (`H-P9`)."
      % (2 * len(SEMI)))
    dati = {}
    for s in SEMI:
        for flag in (False, True):
            d, err = braccio(s, flag, passi)
            if d is None:
                P("  seme %-4d %-3s ** non arrivato in fondo: %s **"
                  % (s, "ON" if flag else "OFF", err.strip()[-180:]))
                continue
            dati[(s, flag)] = d
            P("  seme %-4d %-3s n %d -> %d   nonpos %d"
              % (s, "ON" if flag else "OFF", d["n0"], d["n1"], d["nonpos"]))
    coppie = sorted(set(k for d in dati.values() for k in d["dopo"]))
    P("")
    P("  LA DISTANZA DOPO %d PASSI, per seme e per coppia" % passi)
    P("  %-22s %-8s %12s %12s %12s   %s"
      % ("coppia", "seme", "OFF", "ON", "ON-OFF", "(passo 0 OFF)"))
    delte = {}
    for k in coppie:
        for s in SEMI:
            do, dn = dati.get((s, False)), dati.get((s, True))
            if not do or not dn or k not in do["dopo"] or k not in dn["dopo"]:
                continue
            off, on = do["dopo"][k], dn["dopo"][k]
            delte.setdefault(k, []).append(on - off)
            P("  %-22s %-8d %12.6f %12.6f %+12.6f   %12.6f"
              % (k, s, off, on, on - off, do["passo0"][k]))
    P("")
    P("  LA BARRA E' FRA SEMI (`P3`), e i bracci sono APPAIATI sul seme")
    for k in coppie:
        v = delte.get(k) or []
        if len(v) < 2:
            P("  %-22s meno di 2 semi: nessuna barra (`P3`)" % k)
            continue
        d = OP.dispersione(v)
        dentro = (d["ic95"] and d["ic95"][0] <= 0.0 <= d["ic95"][1])
        P("  %-22s Delta medio %+10.6f   sd %9.6f   t(%d) %.3f   IC95 [%+.6f, %+.6f]   %s"
          % (k, d["media"], d["sd"], d["gdl"], d["t"] or 0,
             (d["ic95"] or (float("nan"),) * 2)[0], (d["ic95"] or (float("nan"),) * 2)[1],
             "CONTIENE LO ZERO" if dentro else "NON contiene lo zero"))
        if dentro:
            ris = abs((d["ic95"][1] - d["ic95"][0]) / 2.0)
            P("        -> si scrive come LIMITE: il flag non sposta la distanza di piu' di")
            P("           %.6f (risoluzione di QUESTO test), su una distanza di ~%.2f."
              % (ris, abs(dati[(SEMI[0], False)]["dopo"][k])))
    # `H-P5`: il referto dichiara LA CONFIGURAZIONE INTERA, non i flag che ricordo io. I
    #   bracci girano in processi loro, quindi qui si carica il modulo dall'argv del driver
    #   (ramo OFF) e si dichiara: **il ramo ON differisce per `--pozzo-d` e NIENT'ALTRO**,
    #   e questo si legge dalla colonna `flag` di ogni braccio, non da questa frase.
    _S, _argv = _cli_flag.argv_del_driver(
        dest=os.path.join(RADICE, "csv", "_test_fork", "_scarto_cli"))
    P("")
    _cli_flag.dichiara_configurazione(_S, P)
    P("  (ramo OFF. Il ramo ON aggiunge SOLO `--pozzo-d`: lo dice la colonna `flag` di")
    P("   ogni braccio, letta dal modulo e non da questa riga.)")
    P("")
    P("=" * 104)
    P("COSA QUESTO A/B *NON* DICE:")
    P("  - **non e' la `PROVA 1`**: dice se la CURA sposta la distanza a %d passi, non se le" % passi)
    P("    masse si avvicinano.")
    P("  - **%d passi sono un GIRO CORTO**: la divergenza `L_pos/L_d` si ACCUMULA (misurato:" % passi)
    P("    `3.2e-03` a 4 passi, `1.07e-01` a 12), quindi un effetto piccolo qui **non dice** che")
    P("    sia piccolo a campo maturo. Si scrive come LIMITE, non come «nessun effetto».")
    P("  - **la barra e' fra 4 semi**, il minimo che `P3` ammette: `t(3) = 3.182`.")
    io.open(REFERTO, "w", encoding="utf-8", newline=NL).write(NL.join(R) + NL)
    print(NL + "scritto %s" % os.path.relpath(REFERTO, RADICE).replace(chr(92), "/"))
    sys.exit(0)
