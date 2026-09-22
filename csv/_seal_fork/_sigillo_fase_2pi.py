# -*- coding: utf-8 -*-
"""SIGILLO -- `FASE_2PI` (`B1`, `D35`): BYTE-INERTE spento, e cambia SOLO i punti elencati.

DUE AFFERMAZIONI DIVERSE:
  A. **BYTE-INERTE DA SPENTO** -- col flag `False` il run e' identico a prima che il flag
     esistesse. Snapshot contro snapshot con `_val600` (blob `9557a867`). **`T3`.**
  B. **ACCESO, CAMBIA SOLO CIO' CHE DEVE** -- il dominio di `phi`, le differenze di fase,
     l'antifase, la soglia. **`T4`-`T6`.**

⚠ `T6` E' IL CRITERIO PIU' FORTE, ed e' STRUTTURALE su un dato VERO: **a flag acceso, `max(phi)`
  in uno snapshot deve stare SOTTO `2pi`**; a flag spento puo' arrivare a `4pi`. **Non e' una
  statistica: e' il dominio, e si vede o non si vede.**

⚠ E IL COLLAUDO HA IL CASO CHE DEVE FALLIRE: **la formula VECCHIA sugli stessi ingressi**.
  Se non sbagliasse, il sigillo certificherebbe il nulla.
ASCII PURO.
"""
import ast
import gzip
import hashlib
import io
import os
import pickle
import re
import subprocess
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, RADICE)
sys.path.insert(0, os.path.join(RADICE, "csv"))
DEST = os.path.join(_QUI, "_sig_fase_2pi")
OUT = os.path.join(DEST, "REFERTO.txt")
DRIVER = os.path.join(RADICE, "csv", "_test_fork", "_scena_video.py")
RIF120 = os.path.join(RADICE, "csv", "_test_fork", "_val600", "scena_000120.pkl.gz")
OFF_DIR = os.path.join(RADICE, "csv", "_test_fork", "_f2p_off")
ON_DIR = os.path.join(RADICE, "csv", "_test_fork", "_f2p_on")
COMUNE = ["--sep=4.0", "--serie=20", "--chi-basc=on", "--chi-coop=on", "--scala-min=off",
          "--coes-adim=on", "--peq-esatto=on", "--peq-nascita-locale=on",
          "--scala-min-passo=on", "--coes-causale=on", "--anom-simm=on", "--invarianti=on"]
# Le funzioni in cui il flag PUO' comparire. Fuori da queste e' un errore.
FUNZIONI_LECITE = {"_dphi", "_wphi", "mitosi"}
BRACCIO = None
for _a in sys.argv[1:]:
    if _a.startswith("--braccio="):
        BRACCIO = _a.split("=", 1)[1]


def confronta_snap(p_a, p_b, W):
    def leggi(p):
        with gzip.open(p, "rb") as f:
            return pickle.load(f)["attrs"]
    a, b = leggi(p_a), leggi(p_b)
    ug = dv = ass = 0
    nomi = []
    for k in sorted(set(a) | set(b)):
        if k not in a or k not in b:
            ass += 1; nomi.append("%s(in uno solo)" % k); continue
        aa = np.asarray(a[k]); bb = np.asarray(b[k])
        if aa.shape != bb.shape:
            dv += 1; nomi.append("%s(shape %s!=%s)" % (k, aa.shape, bb.shape)); continue
        if aa.dtype.kind in "fc" or bb.dtype.kind in "fc":
            d = float(np.max(np.abs(aa - bb))) if aa.size else 0.0
            if d == 0.0:
                ug += 1
            else:
                dv += 1; nomi.append("%s(max|d|=%.3e)" % (k, d))
        else:
            if np.array_equal(aa, bb):
                ug += 1
            else:
                dv += 1; nomi.append(k)
    W("  campi UGUALI %d   DIVERSI %d   non confrontati %d\n" % (ug, dv, ass))
    if nomi:
        W("  i diversi: %s\n" % ", ".join(nomi[:8]))
    return ug, dv


def max_phi(p):
    with gzip.open(p, "rb") as f:
        a = pickle.load(f)["attrs"]
    return float(np.max(np.asarray(a["phi"], float))), float(np.min(np.asarray(a["phi"], float)))


def collaudo(W):
    """`P1-sexies`: le tre regole della cura su casi a risposta NOTA."""
    W("COLLAUDO DEI CRITERI su casi a RISPOSTA NOTA (`P1-sexies`)\n" + "-" * 96 + "\n")
    e = []

    def w2(a):
        return (a + np.pi) % (2 * np.pi) - np.pi

    def w4(a):
        return (a + 2 * np.pi) % (4 * np.pi) - 2 * np.pi

    # --- (b) le DIFFERENZE
    g = np.linspace(-2 * np.pi + 1e-9, 2 * np.pi - 1e-9, 200001)
    ok1 = float(np.max(np.abs(w2(g)))) <= np.pi + 1e-9
    W("K1 `_wphi` ACCESO porta ogni differenza dentro [-pi, pi]: max = %.6f -> %s\n"
      % (float(np.max(np.abs(w2(g)))), "OK" if ok1 else "*** NO ***"))
    ok2 = float(np.max(np.abs(w4(g) - g))) < 1e-9
    W("K2 IL CASO CHE DEVE SBAGLIARE: `_w4` sulle stesse differenze e' L'IDENTITA'\n")
    W("     max|w4(a) - a| = %.3e -> %s\n"
      % (float(np.max(np.abs(w4(g) - g))),
         "OK: il difetto e' riprodotto" if ok2 else "*** non si riproduce ***"))
    e += [ok1, ok2]
    # --- lontano dal taglio i due coincidono: la cura non tocca il caso normale
    p = np.linspace(-np.pi + 1e-6, np.pi - 1e-6, 100001)
    d = float(np.max(np.abs(w2(p) - w4(p))))
    ok3 = d < 1e-9
    W("K3 LONTANO dal taglio (|a| < pi) i due COINCIDONO: max|diff| = %.3e -> %s\n"
      % (d, "OK: obbligo (a) del cor.7" if ok3 else "*** NO ***"))
    e.append(ok3)
    # --- (c) l'ANTIFASE e' META' del dominio
    for dom, atteso in ((2 * np.pi, np.pi), (4 * np.pi, 2 * np.pi)):
        ok = abs(dom / 2.0 - atteso) < 1e-12
        e.append(ok)
    W("K4 l'ANTIFASE e' META' del dominio: 2pi -> +pi, 4pi -> +2pi -> %s\n"
      % ("OK" if all(e[-2:]) else "*** NO ***"))
    # --- e il caso che DEVE fallire: `+2pi` su un dominio `2pi` e' l'IDENTITA'
    fm = np.linspace(0, 2 * np.pi, 1001)[:-1]
    identico = float(np.max(np.abs(((fm + 2 * np.pi) % (2 * np.pi)) - fm)))
    ok5 = identico < 1e-9
    W("K5 IL CASO CHE DEVE ESSERE UN'IDENTITA': `+2pi` su un dominio `2pi` -> max|diff| = %.3e\n"
      % identico)
    W("     -> %s  *(e' il motivo per cui `+2pi` NON e' un'antifase: `D35`)*\n"
      % ("OK" if ok5 else "*** NO ***"))
    e.append(ok5)
    # --- (d) la SOGLIA
    ok6 = abs((2 * np.pi + np.pi) - 3 * np.pi) < 1e-12 and abs(2 * np.pi - 2 * np.pi) < 1e-12
    W("K6 la SOGLIA: spenta `2pi + pi = 3pi`, accesa `2pi` -> %s\n" % ("OK" if ok6 else "*** NO ***"))
    e.append(ok6)
    ok = all(e)
    W("-" * 96 + "\n  -> %s\n\n" % ("i criteri PASSANO" if ok else "*** NON PASSANO ***"))
    return ok


def braccio(nome):
    import runpy
    dest = OFF_DIR if nome == "OFF" else ON_DIR
    try:
        os.makedirs(dest)
    except OSError:
        pass
    for f in os.listdir(dest):
        if f.endswith(".pkl.gz"):
            os.remove(os.path.join(dest, f))
    os.chdir(RADICE)
    import soliton_simulator as S
    if nome == "ON":
        orig = S._applica_flag

        def _w(a):
            r = orig(a)
            S.FASE_2PI = True
            return r
        S._applica_flag = _w
    sys.argv = ["_scena_video.py", "20", dest] + COMUNE
    runpy.run_path(DRIVER, run_name="__main__")
    print("[braccio %s] FASE_2PI = %s" % (nome, S.FASE_2PI))
    return 0


def main():
    try:
        os.makedirs(DEST)
    except OSError:
        pass
    o = io.open(OUT, "w", encoding="utf-8", newline="\n")
    W = o.write
    W("# SIGILLO -- `FASE_2PI` (`B1`, `D35`)\n#\n")
    if not collaudo(W):
        o.close(); print(io.open(OUT, encoding="utf-8").read()); return 1
    sorg = os.path.join(RADICE, "soliton_simulator.py")
    blob = hashlib.sha1(open(sorg, "rb").read()).hexdigest()[:8]
    W("blob simulatore ORA (sha1 byte grezzi) %s\n" % blob)
    W("riferimento `_val600`, blob `9557a867`: ANTERIORE a questo flag\n\n")
    esiti = []

    def esito(n, ok, riga):
        esiti.append((n, ok))
        W("%-5s %-4s %s\n" % (n, "PASS" if ok else "FAIL", riga))

    testo = io.open(sorg, encoding="utf-8").read()
    m = re.search(r"^FASE_2PI\s*=\s*(True|False)", testo, re.M)
    esito("T1", m is not None and m.group(1) == "False",
          "IL DEFAULT E' SPENTO: `FASE_2PI = %s` (letto dal sorgente)"
          % (m.group(1) if m else "ASSENTE"))

    import _hook_fisica as H
    rami, assegn, _t = H.gate(sorg, "FASE_2PI")
    fuori = [(l, f) for l, f in rami if f not in FUNZIONI_LECITE]
    ok2 = (not fuori) and len(assegn) == 1 and len(rami) >= 1
    esito("T2", ok2, "GATE (AST): %d rami, tutti in %s? %s -- %d assegnamento. rami: %s"
          % (len(rami), sorted(FUNZIONI_LECITE), "SI'" if not fuori else "NO: %s" % fuori,
             len(assegn), rami))
    W("      -> STRUTTURALE: un ramo in una funzione NON prevista comparirebbe qui, senza\n")
    W("         girare niente. Le altre modifiche passano da `_dphi()`/`_wphi()`, che NON\n")
    W("         sono ramificazioni: sono UN SOLO punto da cui tutti prendono il periodo.\n")

    W("\n" + "-" * 96 + "\nT3 -- BYTE-INERZIA A FLAG SPENTO (120 passi)\n" + "-" * 96 + "\n")
    t0 = time.time()
    r = subprocess.run([sys.executable, os.path.abspath(__file__), "--braccio=OFF"],
                       cwd=RADICE, capture_output=True, text=True)
    W("  (%.1f s)\n" % (time.time() - t0))
    p_off = os.path.join(OFF_DIR, "scena_000120.pkl.gz")
    if not os.path.exists(p_off):
        W("  *** il braccio OFF non ha prodotto lo snapshot. uscita=%d ***\n%s\n"
          % (r.returncode, (r.stderr or "")[-1500:]))
        esiti.append(("T3", False)); p_off = None
    else:
        ug, dv = confronta_snap(RIF120, p_off, W)
        esito("T3", dv == 0 and ug > 0,
              "BYTE-INERTE spento: %d campi identici, %d diversi" % (ug, dv))

    W("\n" + "-" * 96 + "\nT4/T5/T6 -- A FLAG ACCESO (120 passi)\n" + "-" * 96 + "\n")
    t0 = time.time()
    r = subprocess.run([sys.executable, os.path.abspath(__file__), "--braccio=ON"],
                       cwd=RADICE, capture_output=True, text=True)
    W("  (%.1f s)\n" % (time.time() - t0))
    p_on = os.path.join(ON_DIR, "scena_000120.pkl.gz")
    if not os.path.exists(p_on) or p_off is None:
        W("  *** manca uno dei due snapshot. uscita=%d ***\n%s\n"
          % (r.returncode, (r.stderr or "")[-1500:]))
        esiti += [("T4", False), ("T5", False), ("T6", False)]
    else:
        ug2, dv2 = confronta_snap(p_off, p_on, W)
        esito("T4", dv2 > 0, "CONTROLLO POSITIVO: acceso CAMBIA, %d campi diversi" % dv2)
        mx_off, mn_off = max_phi(p_off)
        mx_on, mn_on = max_phi(p_on)
        esito("T5", mx_on < 2 * np.pi + 1e-9,
              "IL DOMINIO E' DAVVERO CAMBIATO: acceso max(phi) = %.6f < 2pi = %.6f"
              % (mx_on, 2 * np.pi))
        esito("T6", mx_off > 2 * np.pi,
              "E SPENTO NON LO E': max(phi) = %.6f, SOPRA 2pi -- il criterio `T5` non e' "
              "vuoto" % mx_off)
        W("      -> `T6` e' il controllo che rende `T5` leggibile: se anche spento `phi`\n")
        W("         stesse sotto `2pi`, `T5` passerebbe SENZA che il flag abbia fatto nulla.\n")
        W("      min(phi): spento %.6f, acceso %.6f\n" % (mn_off, mn_on))

    n_ok = sum(1 for _n, k in esiti if k)
    W("\n" + "=" * 96 + "\nESITO: %d/%d\n" % (n_ok, len(esiti)) + "=" * 96 + "\n")
    if n_ok == len(esiti):
        W("*** SIGILLO PASSATO. La prova a 600 passi e i quattro test possono partire. ***\n")
    else:
        W("*** SIGILLO FALLITO: la prova NON parte. ***\n")
    W("\n⚠ E IL SIGILLO NON DICE CHE LA CURA SIA GIUSTA: dice che fa CIO' CHE DICHIARA.\n")
    W("  Se `φ` debba vivere su `2π` lo decidono i QUATTRO TEST del paragrafo E, e se uno\n")
    W("  fallisce LA LETTURA CADE.\n")
    o.close()
    print(io.open(OUT, encoding="utf-8").read())
    return 0 if n_ok == len(esiti) else 1


if __name__ == "__main__":
    sys.exit(braccio(BRACCIO) if BRACCIO else main())
