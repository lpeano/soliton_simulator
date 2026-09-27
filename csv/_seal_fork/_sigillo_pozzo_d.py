r"""**SIGILLO DI `POZZO-D`** (`D02`) — nel pozzo del grafo `L` viene da `self.d`, non da `pos`.

*(criteri `W1`-`W4` dal task history `doc/TASK_HISTORY/2026-09-27_d02-pozzo-d.md`, committato
**prima** del codice. `W5` — l'A/B a 4 semi — sta in `csv/_test_fork/_ab_pozzo_d.py`.)*

| # | criterio | come si verifica |
|--:|---|---|
| **W1** | **a flag SPENTO, byte-identico** | firme `sha1` campo per campo contro il simulatore al **PADRE** del commit del flag (`H-P8`), scena `(ii)`(a), **`passo_pieno`** (`H-P9`), **un processo per braccio** |
| **W2** | **a flag ACCESO la spinta CAMBIA** *(e' la cura)* | `dpozzo` e `phi_g` differiscono, e si riporta **di quanto**: `max|Δ|`, e il rapporto `L_pos/L_d` **mediano e massimo** |
| **W3** | **il pavimento `1e-9` non serve piu'** | il contatore `_pozzo_d_nonpos`: **atteso `0`**, e **si CONTA** invece di assumerlo (`A8`) |
| **W4** | **il caso che DEVE fallire** | con **`pos` alterato** a `d` costante: a flag **ACCESO** il pozzo **NON cambia**, a flag **SPENTO** **cambia** |

> ### **`W4` E' IL CRITERIO CHE DIMOSTRA LA CURA, e `W2` da solo non basterebbe.**
> `W2` dice *«il numero e' cambiato»* — ma un numero cambia anche se si e' rotto qualcosa. **`W4`
> stacca la dipendenza e la mostra:** se muovo **solo `pos`** e il pozzo **non si muove**, allora
> `pos` **non entra piu'**; e la meta' a flag spento *(dove invece si muove)* dice che **il banco
> funziona** — senza quella, un «non cambia» potrebbe voler dire che non ho misurato nulla.

    python csv/_seal_fork/_sigillo_pozzo_d.py            # 12 passi
    python csv/_seal_fork/_sigillo_pozzo_d.py --corto    # 4 passi

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

_presidio.avvia(__file__)

NL = chr(10)
DEST = os.path.join(_QUI, "_sig_pozzo_d")
REFERTO = os.path.join(DEST, "REFERTO.txt")
SIM = "soliton_simulator.py"
FLAG = "POZZO_D"
SCENA2 = "MASSE-COERENTI"
R = []


def P(s=""):
    print(s)
    R.append(s)


def _git(*a):
    q = subprocess.run(["git"] + list(a), cwd=RADICE, capture_output=True)
    return q.returncode, q.stdout


def sim_prima(dest):
    """Il simulatore al **PADRE** del commit che ha introdotto `POZZO_D`, in binario, asserito."""
    c, fuori = _git("log", "--format=%H", "-S", FLAG, "--", SIM)
    if c or not fuori.strip():
        raise SystemExit("non trovo il commit che ha introdotto `%s`" % FLAG)
    intro = [x for x in fuori.decode().strip().split(NL) if x.strip()][-1]
    c2, byte = _git("show", "%s^:%s" % (intro, SIM))
    if c2:
        raise SystemExit("il PADRE di %s non ha %s" % (intro[:8], SIM))
    if FLAG.encode() in byte:
        raise SystemExit("IL FILE 'DI PRIMA' CONTIENE GIA' `%s`: ancora sbagliata, mi fermo (A9)"
                         % FLAG)
    io.open(dest, "wb").write(byte)
    import hashlib
    return intro[:8], hashlib.sha1(byte).hexdigest()[:8]


BRACCIO = '''# -*- coding: utf-8 -*-
import hashlib, json, os, sys
import numpy as np
sys.path.insert(0, os.path.join(%(rad)r, "csv"))
import _cli_flag, _passo
_S0, argv = _cli_flag.argv_del_driver(dest=os.path.join(%(rad)r, "csv", "_test_fork",
                                                        "_scarto_cli"))
argv = [x for x in argv] + %(extra)r
S, a = _cli_flag.carica_dal_cli(argv, nome="sim_pd", sim=%(sim)r)
S._NMASSE_VIDEO["n"] = max(2, int(getattr(a, "nmasse", 2)))
S._NMASSE_VIDEO["sep"] = float(getattr(a, "sep", 3.0))
S._NMASSE_VIDEO["size"] = None
S.avvia_test("MASSE-COERENTI")()
if hasattr(S, "passo_test"):
    S.passo_test()
for _ in range(%(passi)d):
    _passo.passo_pieno(S, S.net)          # `H-P9`: mai `net.step()` da solo
o = {"n": int(S.net.n), "archi": int(len(S.net.d)),
     "flag": bool(getattr(S, "POZZO_D", None)),
     "nonpos": int(getattr(S.net, "_pozzo_d_nonpos", -1)),
     "nonpos_tot": int(getattr(S.net, "_pozzo_d_tot", -1)), "firme": {}}
for k, v in sorted(vars(S.net).items()):
    if isinstance(v, np.ndarray):
        o["firme"][k] = "%%s|%%s|%%s" %% (v.shape, v.dtype,
                                       hashlib.sha1(v.tobytes()).hexdigest()[:16])
    elif isinstance(v, (int, float, bool)):
        o["firme"][k] = repr(v)
open(%(out)r, "w").write(json.dumps(o, sort_keys=True))
print("OK", o["n"], o["archi"], o["flag"], o["nonpos"])
'''


def braccio(nome, sim_path, passi, extra):
    dd = os.path.join(DEST, nome)
    if not os.path.isdir(dd):
        os.makedirs(dd)
    out = os.path.join(dd, "firme.json")
    scr = os.path.join(dd, "_braccio.py")
    io.open(scr, "w", encoding="utf-8", newline=NL).write(
        BRACCIO % dict(rad=RADICE, sim=sim_path, passi=passi, out=out, extra=list(extra)))
    q = subprocess.run([sys.executable, scr], cwd=RADICE, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    if q.returncode or not os.path.exists(out):
        return None, (q.stdout or "") + (q.stderr or "")
    return json.load(io.open(out, encoding="utf-8")), ""


def diff(a, b):
    if a is None or b is None:
        return None, []
    forma = (a["n"] == b["n"] and a["archi"] == b["archi"]
             and set(a["firme"]) == set(b["firme"]))
    return forma, sorted(k for k in a["firme"] if a["firme"][k] != b["firme"].get(k))


def scena(flag, pos_costante=False, seme=None, passi=4):
    """La scena `(ii)`(a) in-process, e `pozzo_grafo` chiamata direttamente. `(phi_g, dpozzo, S)`."""
    extra = (["--seme=%d" % seme] if seme is not None else [])
    _S0, argv = _cli_flag.argv_del_driver(
        extra=extra, dest=os.path.join(RADICE, "csv", "_test_fork", "_scarto_cli"))
    if flag:
        argv = list(argv) + ["--pozzo-d"]
    nome = "sim_w_%s_%s" % (int(flag), int(pos_costante))
    S, a = _cli_flag.carica_dal_cli(list(argv), nome=nome)
    S._NMASSE_VIDEO["n"] = max(2, int(getattr(a, "nmasse", 2)))
    S._NMASSE_VIDEO["sep"] = float(getattr(a, "sep", 3.0))
    S._NMASSE_VIDEO["size"] = None
    S.avvia_test(SCENA2)()
    # ⚠ SI AVANZA PRIMA DI CHIAMARE IL POZZO, e non e' un dettaglio: al passo 0 `psi` non
    #   esiste ancora (`len(psi) < n`), e `pozzo_grafo(None)` cade su un ramo che indicizza
    #   `None`. E' anche PIU' FEDELE: la chiamata vera (`:6637`) avviene DENTRO un passo.
    import _passo
    if hasattr(S, "passo_test"):
        S.passo_test()
    for _ in range(max(1, passi)):
        _passo.passo_pieno(S, S.net)          # `H-P9`
    if pos_costante:
        # ⚠ SI ALTERA SOLO `pos`, e in modo che le LUNGHEZZE da `pos` diventino COSTANTI: i nodi
        #   si mettono su una retta a passo 1. `self.d` NON si tocca. E' il banco di `W4`.
        n = int(S.net.n)
        p = np.zeros((n, 3), dtype=float)
        p[:, 0] = np.arange(n, dtype=float)
        S.net.pos = p
    # l'intensita' si passa ESPLICITA, come fa il chiamante vero: `pozzo_grafo(None)` con
    #   `psi` corto indicizza `None`, e sarebbe un errore mio, non del simulatore.
    if len(S.net.psi) >= S.net.n:
        I = np.abs(S.net.psi[:S.net.n]) ** 2
    else:
        I = np.abs(S.net.phi[:S.net.n]) * 0.0 + 1.0     # intensita' UNIFORME, dichiarata
    phi_g, _m, dpozzo = S.net.pozzo_grafo(I)
    return np.asarray(phi_g, float), np.asarray(dpozzo, float), S


if __name__ == "__main__":
    ar = sys.argv[1:]
    passi = 4 if "--corto" in ar else 12
    if not os.path.isdir(DEST):
        os.makedirs(DEST)
    P("=" * 104)
    P("SIGILLO DI `POZZO-D` (`D02`) -- `L` dal grafo, non dal disegno   (%d passi)" % passi)
    P("=" * 104)
    esiti = []

    # ------------------------------------------------------------------ W1
    vecchio = os.path.join(DEST, "_sim_prima.py")
    sha, blob = sim_prima(vecchio)
    P("")
    P("  W1  A FLAG SPENTO, BYTE-IDENTICO  (contro il PADRE di %s, blob %s)" % (sha, blob))
    a_p, e1 = braccio("prima", vecchio, passi, [])
    a_d, e2 = braccio("dopo_off", os.path.join(RADICE, SIM), passi, [])
    forma, div = diff(a_p, a_d)
    if a_p is None or a_d is None:
        P("      ** un braccio non e' arrivato in fondo **")
        P("         prima: %s" % e1.strip()[-200:])
        P("         dopo:  %s" % e2.strip()[-200:])
        ok1 = False
    else:
        P("      PRIMA  n %-6d archi %-8d campi %d" % (a_p["n"], a_p["archi"], len(a_p["firme"])))
        P("      DOPO   n %-6d archi %-8d campi %d   flag %s"
          % (a_d["n"], a_d["archi"], len(a_d["firme"]), a_d["flag"]))
        P("      stessa forma %-5s   DIVERSI %d %s" % (forma, len(div), div[:6]))
        ok1 = bool(forma) and not div and a_d["flag"] is False
    esiti.append(("W1  a flag spento, byte-identico", ok1))

    # ------------------------------------------------------------------ W2
    P("")
    P("  W2  A FLAG ACCESO LA SPINTA CAMBIA  (dichiarato: e' la cura)")
    phi_off, dp_off, S_off = scena(False, passi=passi)
    phi_on, dp_on, S_on = scena(True, passi=passi)
    n_arc = min(len(dp_off), len(dp_on))
    dmax = float(np.max(np.abs(dp_on[:n_arc] - dp_off[:n_arc]))) if n_arc else float("nan")
    pmax = float(np.max(np.abs(phi_on - phi_off))) if len(phi_on) == len(phi_off) else float("nan")
    # il rapporto L_pos/L_d, calcolato SULLA STESSA rete (quella a flag spento)
    net = S_off.net
    m = (net.i < net.n) & (net.j < net.n)
    ii, jj = net.i[m], net.j[m]
    v = net.pos[jj] - net.pos[ii]
    L_pos = np.maximum(np.linalg.norm(v, axis=1), 1e-9)
    L_d = np.asarray(net.d, float)[m]
    rap = L_pos / np.maximum(L_d, 1e-300)
    P("      archi confrontati %d   max|dpozzo_ON - dpozzo_OFF| %.6e" % (n_arc, dmax))
    P("      max|phi_g_ON - phi_g_OFF| %.6e" % pmax)
    P("      L_pos/L_d   mediano %.6f   max %.6f   min %.6f"
      % (float(np.median(rap)), float(np.max(rap)), float(np.min(rap))))
    ok2 = np.isfinite(dmax) and dmax > 0.0
    if not ok2:
        P("      ** LA SPINTA NON CAMBIA: `pos` e `d` coincidono dove conta, e la CURA E' INERTE.")
        P("         E' un RISCONTRO, non un fallimento -- ma va detto, non nascosto. **")
    esiti.append(("W2  a flag acceso la spinta CAMBIA", bool(ok2)))

    # ------------------------------------------------------------------ W3
    P("")
    P("  W3  IL PAVIMENTO `1e-9` NON SERVE PIU'  (e si CONTA, non si assume)")
    nn = int(getattr(S_on.net, "_pozzo_d_nonpos", -1))
    nt = int(getattr(S_on.net, "_pozzo_d_tot", -1))
    P("      `_pozzo_d_nonpos` %d su %d archi   (atteso 0)" % (nn, nt))
    P("      min(d) %.6e   LAM %.6f" % (float(np.min(L_d)) if len(L_d) else float("nan"),
                                        float(S_on.LAM)))
    ok3 = (nn == 0 and nt > 0)
    if nn > 0:
        P("      ** `d <= 0` ESISTE: `d >= LAM` NON e' invariante, e il pavimento va TENUTO **")
    esiti.append(("W3  zero `d <= 0`, contati", bool(ok3)))

    # ------------------------------------------------------------------ W4
    P("")
    P("  W4  IL CASO CHE DEVE FALLIRE -- `pos` alterato a `d` costante")
    phi_on2, dp_on2, _ = scena(True, pos_costante=True, passi=passi)
    phi_off2, dp_off2, _ = scena(False, pos_costante=True, passi=passi)
    k1 = min(len(dp_on), len(dp_on2))
    k2 = min(len(dp_off), len(dp_off2))
    d_on = float(np.max(np.abs(dp_on2[:k1] - dp_on[:k1]))) if k1 else float("nan")
    d_off = float(np.max(np.abs(dp_off2[:k2] - dp_off[:k2]))) if k2 else float("nan")
    P("      flag ACCESO  max|dpozzo(pos alterato) - dpozzo| = %.6e   (atteso 0: `pos` NON entra)"
      % d_on)
    P("      flag SPENTO  max|dpozzo(pos alterato) - dpozzo| = %.6e   (atteso > 0: il banco c'e')"
      % d_off)
    ok4 = (d_on == 0.0) and np.isfinite(d_off) and d_off > 0.0
    esiti.append(("W4  solo `pos` mosso: ON non cambia, OFF si'", bool(ok4)))

    P("")
    _cli_flag.dichiara_configurazione(S_on, P)
    P("")
    P("=" * 104)
    for nome, ok in esiti:
        P("  %-46s %s" % (nome, "PASS" if ok else "** FAIL **"))
    buoni = len([1 for _n, ok in esiti if ok])
    P("SIGILLO: %d/%d" % (buoni, len(esiti)))
    P("=" * 104)
    P()
    P("COSA QUESTO SIGILLO *NON* DICE:")
    P("  - **non dice che la cura AVVICINI le masse**: quello e' `W5`, l'A/B a 4 semi.")
    P("  - **`W2` misura al passo 0 della scena**, non dopo una dinamica: dice che il pozzo e'")
    P("    un'altra funzione, non che la gravita' cambi di tanto.")
    P("  - **`W3` dice che a questa configurazione `d > 0` sempre**, NON che sia un'invariante:")
    P("    e' un CONTATORE, e serve proprio perche' l'invariante non e' dimostrata.")
    io.open(REFERTO, "w", encoding="utf-8", newline=NL).write(NL.join(R) + NL)
    print(NL + "scritto %s" % os.path.relpath(REFERTO, RADICE).replace(chr(92), "/"))
    sys.exit(0 if buoni == len(esiti) else 1)
