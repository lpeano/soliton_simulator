r"""**SIGILLO DI `CURA2-STRUTTURALE`** — i rami `else` escono e **non cambia un bit**.

*(criteri dettati da Luca, 2026-09-27)*

| # | criterio | come si verifica |
|--:|---|---|
| **C1** | **byte-identici col flag ACCESO**, contro il simulatore **al tag `pre-cura2-strutturale`** | scena `(ii)`(a), **2 semi**, **un processo per braccio** (`STANDARD 1`), **firme `sha1`** campo per campo (`STANDARD 2`) |
| **C2** | **il caso che DEVE fallire:** al tag **col flag SPENTO** i byte **cambiano** | se non cambiassero, i rami tolti **non facevano niente** e l'archivio conserverebbe codice morto **per un'altra ragione** |
| **C3** | **il driver: 0 differenze di configurazione** | `_cli_flag.scarto_dal_driver` (`H-P5`) |
| **C4** | **la mitosi DEVE aver girato** *(l'analogo di `N5`)* | `_rep_taupp_tot > 0` su **tutti** i bracci: se e' `0`, `C1` sarebbe **byte-identita' di codice mai eseguito** |

> ### ⚠ **QUESTO SIGILLO AVANZA CON `csv/_passo.py passo_pieno`, NON con le cinque chiamate a mano.**
> Il sigillo di `D32` era il **25esimo** strumento caduto su *«`net.step()` non e' un passo»*
> (`PASSO-1`), **e la mia correzione ha ricopiato le cinque chiamate**, aggiungendo il
> **26esimo posto** in cui quell'ordine vive cablato. **`passo_pieno` legge l'ordine DAL CODICE**
> e **rifiuta di girare** se simulatore e driver divergono: e' l'unico modo che non scade.
> *(E' il difetto registrato come `PASSO-PIENO`.)*

    python csv/_seal_fork/_sigillo_cura2_strutturale.py            # 12 passi, 2 semi
    python csv/_seal_fork/_sigillo_cura2_strutturale.py --corto    # 1 seme

ASCII puro.
"""
import io
import json
import os
import subprocess
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, os.path.join(RADICE, "csv"))

import _presidio                                                       # noqa: E402
import _cli_flag                                                       # noqa: E402

_presidio.avvia(__file__)

NL = chr(10)
DEST = os.path.join(_QUI, "_sig_cura2_strutturale")
REFERTO = os.path.join(DEST, "REFERTO.txt")
TAG = "pre-cura2-strutturale"
SEMI = [11, 12]
R = []


def P(s=""):
    print(s)
    R.append(s)


def sim_al_tag(dest):
    """Il simulatore AL TAG, estratto **in binario** (par.5-quinquies), con l'asserzione che
    contenga ancora i rami `else` -- senza quella, un'ancora sbagliata misurerebbe niente."""
    q = subprocess.run(["git", "show", "%s:soliton_simulator.py" % TAG], cwd=RADICE,
                       capture_output=True)
    if q.returncode:
        raise SystemExit("il tag %s non si legge" % TAG)
    byte = q.stdout
    if b"TEMPO_UNICO_MITOSI = False" not in byte:
        raise SystemExit("IL FILE AL TAG NON HA `TEMPO_UNICO_MITOSI = False`: ancora sbagliata, "
                         "mi fermo invece di misurare niente (A9)")
    io.open(dest, "wb").write(byte)
    import hashlib
    return hashlib.sha1(byte).hexdigest()[:8]


# il braccio: UN PROCESSO, e avanza con `passo_pieno` (mai `net.step()` da solo)
BRACCIO = '''# -*- coding: utf-8 -*-
import hashlib, json, os, sys
import numpy as np
sys.path.insert(0, os.path.join(%(rad)r, "csv"))
import _cli_flag, _passo
_S0, argv = _cli_flag.argv_del_driver(extra=%(extra)r,
                                     dest=os.path.join(%(rad)r, "csv", "_test_fork",
                                                       "_scarto_cli"))
argv = [x for x in argv if x != %(togli)r]
S, a = _cli_flag.carica_dal_cli(argv, nome="sim_c2", sim=%(sim)r)
S._NMASSE_VIDEO["n"] = max(2, int(getattr(a, "nmasse", 2)))
S._NMASSE_VIDEO["sep"] = float(getattr(a, "sep", 3.0))
S._NMASSE_VIDEO["size"] = None
S.avvia_test("MASSE-COERENTI")()
# ⚠ `passo_pieno`, NON `net.step()`: legge l'ordine DAL CODICE e rifiuta se sim e driver divergono
if hasattr(S, "passo_test"):
    S.passo_test()
for _ in range(%(passi)d):
    _passo.passo_pieno(S, S.net)
o = {"n": int(S.net.n), "archi": int(len(S.net.d)),
     "taupp_tot": int(getattr(S.net, "_rep_taupp_tot", 0)),
     "flag": bool(getattr(S, "TEMPO_UNICO_MITOSI", None)), "firme": {}}
for k, v in sorted(vars(S.net).items()):
    if isinstance(v, np.ndarray):
        o["firme"][k] = "%%s|%%s|%%s" %% (v.shape, v.dtype,
                                       hashlib.sha1(v.tobytes()).hexdigest()[:16])
    elif isinstance(v, (int, float, bool)):
        o["firme"][k] = repr(v)
open(%(out)r, "w").write(json.dumps(o, sort_keys=True))
print("OK", o["n"], o["archi"], o["taupp_tot"], o["flag"])
'''


def braccio(nome, sim_path, passi, seme, togli_flag=False):
    dd = os.path.join(DEST, nome)
    if not os.path.isdir(dd):
        os.makedirs(dd)
    out = os.path.join(dd, "firme.json")
    scr = os.path.join(dd, "_braccio.py")
    io.open(scr, "w", encoding="utf-8", newline=NL).write(
        BRACCIO % dict(rad=RADICE, sim=sim_path, passi=passi, out=out,
                       extra=["--seme=%d" % seme],
                       togli=("--tempo-unico-mitosi" if togli_flag else "")))
    q = subprocess.run([sys.executable, scr], cwd=RADICE, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    if q.returncode or not os.path.exists(out):
        return None, (q.stdout or "") + (q.stderr or "")
    return json.load(io.open(out, encoding="utf-8")), ""


def confronta(a, b):
    if a is None or b is None:
        return None, None
    forma = (a["n"] == b["n"] and a["archi"] == b["archi"]
             and set(a["firme"]) == set(b["firme"]))
    div = sorted(k for k in a["firme"] if a["firme"][k] != b["firme"].get(k))
    return forma, div


if __name__ == "__main__":
    ar = sys.argv[1:]
    corto = "--corto" in ar
    passi = int(ar[ar.index("--passi") + 1]) if "--passi" in ar else 12
    semi = SEMI[:1] if corto else SEMI
    if not os.path.isdir(DEST):
        os.makedirs(DEST)
    P("=" * 104)
    P("SIGILLO DI `CURA2-STRUTTURALE` -- i rami `else` escono%s   (%d passi, %d semi)"
      % ("   (GIRO CORTO)" if corto else "", passi, len(semi)))
    P("=" * 104)
    P("")
    P("  avanzamento: `csv/_passo.py passo_pieno` -- NON `net.step()`, NON le cinque")
    P("               chiamate a mano. `passo_pieno` legge l'ordine DAL CODICE (`PASSO-PIENO`).")
    import _passo
    P("  ordine del passo, letto: %s" % ", ".join(n for _t, n in _passo.ordine()))
    vecchio = os.path.join(DEST, "_sim_al_tag.py")
    blob = sim_al_tag(vecchio)
    P("  simulatore AL TAG `%s`: blob %s, e contiene `= False` (asserito)" % (TAG, blob))
    esiti = []

    # ------------------------------------------------------------------ C1 e C4
    P("")
    P("  C1/C4  BYTE-IDENTICI COL FLAG ACCESO, contro il tag -- %d semi, un processo per braccio"
      % len(semi))
    ok1 = True
    ok4 = True
    per_seme = {}
    for s in semi:
        a_tag, e1 = braccio("tag_on_s%d" % s, vecchio, passi, s)
        a_new, e2 = braccio("new_s%d" % s, os.path.join(RADICE, "soliton_simulator.py"), passi, s)
        forma, div = confronta(a_tag, a_new)
        per_seme[s] = (a_tag, a_new)
        if a_tag is None or a_new is None:
            P("      seme %-4d ** un braccio non e' arrivato in fondo **" % s)
            P("          tag: %s" % e1.strip()[-200:])
            P("          new: %s" % e2.strip()[-200:])
            ok1 = ok4 = False
            continue
        P("      seme %-4d TAG n %-6d archi %-8d flag %-5s taupp_tot %d"
          % (s, a_tag["n"], a_tag["archi"], a_tag["flag"], a_tag["taupp_tot"]))
        P("               NEW n %-6d archi %-8d flag %-5s taupp_tot %d"
          % (a_new["n"], a_new["archi"], a_new["flag"], a_new["taupp_tot"]))
        P("               stessa forma %-5s   campi %d   DIVERSI %d %s"
          % (forma, len(a_tag["firme"]), len(div), div[:6]))
        ok1 = ok1 and bool(forma) and not div
        ok4 = ok4 and a_tag["taupp_tot"] > 0 and a_new["taupp_tot"] > 0
    esiti.append(("C1  byte-identici col flag acceso, %d semi" % len(semi), ok1))
    esiti.append(("C4  la mitosi HA girato (taupp_tot > 0)", ok4))

    # ------------------------------------------------------------------ C2
    P("")
    P("  C2  IL CASO CHE DEVE FALLIRE -- al tag col flag SPENTO i byte DEVONO cambiare")
    s0 = semi[0]
    a_off, e3 = braccio("tag_off_s%d" % s0, vecchio, passi, s0, togli_flag=True)
    a_on = per_seme.get(s0, (None, None))[0]
    forma2, div2 = confronta(a_on, a_off)
    if a_off is None or a_on is None:
        P("      ** un braccio non e' arrivato in fondo: %s **" % e3.strip()[-200:])
        ok2 = False
    else:
        P("      seme %-4d flag ACCESO %-5s taupp_tot %d    flag SPENTO %-5s taupp_tot %d"
          % (s0, a_on["flag"], a_on["taupp_tot"], a_off["flag"], a_off["taupp_tot"]))
        P("               stessa forma %s   campi DIVERSI %d   %s"
          % (forma2, len(div2), div2[:6]))
        ok2 = (a_off["flag"] is False) and bool(div2)
        if not div2:
            P("      ** ZERO CAMPI DIVERSI: i rami tolti NON facevano niente, e questo criterio")
            P("         esiste per dirlo invece di lasciarlo credere **")
    esiti.append(("C2  al tag col flag SPENTO i byte CAMBIANO", ok2))

    # ------------------------------------------------------------------ C3
    P("")
    _S, _argv = _cli_flag.argv_del_driver(
        dest=os.path.join(RADICE, "csv", "_test_fork", "_scarto_cli"))
    div3, quanti = _cli_flag.scarto_dal_driver(_S, argv=_argv)
    P("  C3  IL DRIVER -- 0 differenze di configurazione (`H-P5`)")
    P("      booleani confrontati %d   DIVERSI %d %s" % (quanti, len(div3), div3[:8]))
    P("      `TEMPO_UNICO_MITOSI` nel modulo: %s   (ora e' una LEGGE, non un flag)"
      % getattr(_S, "TEMPO_UNICO_MITOSI", None))
    esiti.append(("C3  driver: 0 differenze sui booleani", not div3))
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
    P("  - **non dice che la `CURA 2` sia la legge GIUSTA**: dice che togliere i rami spenti non")
    P("    cambia un bit, e che quei rami FACEVANO qualcosa (`C2`), quindi l'archivio conserva")
    P("    codice vero e non codice morto.")
    P("  - **`C2` misura il TAG contro il TAG**, non il nuovo contro il vecchio a flag spento:")
    P("    nel nuovo il ramo spento NON ESISTE PIU', e chiederglielo sarebbe un test vuoto.")
    P("  - **%d passi non sono un run.**" % passi)
    io.open(REFERTO, "w", encoding="utf-8", newline=NL).write(NL.join(R) + NL)
    print(NL + "scritto %s" % os.path.relpath(REFERTO, RADICE).replace(chr(92), "/"))
    sys.exit(0 if buoni == len(esiti) else 1)
