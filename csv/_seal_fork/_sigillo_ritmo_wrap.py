# -*- coding: utf-8 -*-
"""SIGILLO -- `RITMO_WRAP_2PI` (`D34`): BYTE-INERTE spento, e CORREGGE il taglio acceso.

DUE AFFERMAZIONI DIVERSE, e nessuna sostituisce l'altra:
  A. **BYTE-INERTE DA SPENTO** -- col flag `False` il run e' identico a prima che il flag
     esistesse. Si misura contro **`_val600`** (blob `9557a867`), snapshot contro snapshot.
  B. **ACCESO, DA' LA FREQUENZA VERA** -- su un caso sintetico che attraversa il taglio a
     `+-pi`, e **il caso che DEVE fallire e' la formula VECCHIA sullo stesso caso**.

⚠ PERCHE' `B` SI FA SU UN CASO SINTETICO E NON SUL RUN: sul run non esiste una "frequenza
  vera" con cui confrontarsi -- e' quello che si sta misurando. Su un caso costruito la
  risposta e' NOTA (`+0.1/DT`), e li' il criterio puo' fallire.

⚠ E `T4` E' IL CONTROLLO POSITIVO che il par.10 criterio 2 impone: **un sigillo che verifica
  solo la byte-identita' a OFF passerebbe anche su codice morto.** Si dimostra che acceso il
  flag CAMBIA QUALCOSA nel simulatore vero.

⚠ SCRITTO SUI SETTE PATTERN STANDARD. In particolare il **2** (firme dei byte, non `max|delta|`)
  e il **4** (snapshot contro snapshot, allo stesso istante).
ASCII PURO.
"""
import hashlib
import io
import os
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
DEST = os.path.join(_QUI, "_sig_ritmo_wrap")
OUT = os.path.join(DEST, "REFERTO.txt")
DRIVER = os.path.join(RADICE, "csv", "_test_fork", "_scena_video.py")
RIF120 = os.path.join(RADICE, "csv", "_test_fork", "_val600", "scena_000120.pkl.gz")
DEST_INERZIA = os.path.join(RADICE, "csv", "_test_fork", "_rw_inerzia")
COMUNE = ["--sep=4.0", "--serie=20", "--chi-basc=on", "--chi-coop=on", "--scala-min=off",
          "--coes-adim=on", "--peq-esatto=on", "--peq-nascita-locale=on",
          "--scala-min-passo=on", "--coes-causale=on", "--anom-simm=on", "--invarianti=on"]
BRACCIO = None
SALTA = False
for _a in sys.argv[1:]:
    if _a.startswith("--braccio="):
        BRACCIO = _a.split("=", 1)[1]
    if _a == "--senza-inerzia":
        SALTA = True


def w2(a, dt):
    return ((a + np.pi) % (2 * np.pi) - np.pi) / dt


def w4(a, dt):
    return ((a + 2 * np.pi) % (4 * np.pi) - 2 * np.pi) / dt


def confronta_snap(p_a, p_b, W):
    """Pattern 4. Niente `astype(float)` sui complessi: scarta la parte immaginaria."""
    import gzip
    import pickle

    def leggi(p):
        with gzip.open(p, "rb") as f:
            return pickle.load(f)["attrs"]
    a, b = leggi(p_a), leggi(p_b)
    ug = dv = assenti = 0
    nomi = []
    for k in sorted(set(a) | set(b)):
        if k not in a or k not in b:
            assenti += 1; nomi.append("%s(in uno solo)" % k); continue
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
    W("  campi UGUALI %d   DIVERSI %d   non confrontati %d\n" % (ug, dv, assenti))
    if nomi:
        W("  i diversi: %s\n" % ", ".join(nomi[:10]))
    return ug, dv


def collaudo(W):
    """`P1-sexies`: i due wrap su casi a risposta NOTA, e quello che DEVE fallire."""
    W("COLLAUDO DEI CRITERI su casi a RISPOSTA NOTA (`P1-sexies`)\n" + "-" * 96 + "\n")
    e = []
    DT = 0.01
    # IL CASO DEL MANDATO: la fase avanza di 0.1 attraversando il taglio
    a = (-np.pi + 0.05) - (np.pi - 0.05)
    vero = 0.1 / DT
    v2, v4 = float(w2(a, DT)), float(w4(a, DT))
    ok1 = abs(v2 - vero) < 1e-9
    W("K1 attraversa il taglio: il wrap NUOVO da' %+.4f, la frequenza VERA e' %+.4f -> %s\n"
      % (v2, vero, "OK" if ok1 else "*** NO ***"))
    ok2 = abs(v4 - vero) > 100.0
    W("K2 IL CASO CHE DEVE FALLIRE: la formula VECCHIA sullo stesso caso da' %+.4f\n" % v4)
    W("     sbaglia di %+.4f -> %s\n"
      % (v4 - vero, "OK: il difetto e' riprodotto" if ok2 else "*** NON si riproduce ***"))
    e += [ok1, ok2]
    # LONTANO dal taglio i due wrap COINCIDONO: la cura non cambia il caso normale
    g = np.linspace(-np.pi + 1e-6, np.pi - 1e-6, 100001)
    d = float(np.max(np.abs(w2(g, DT) - w4(g, DT))))
    ok3 = d < 1e-9
    W("K3 LONTANO dal taglio (|a| < pi) i due wrap COINCIDONO: max|diff| = %.3e -> %s\n"
      % (d, "OK: la cura non tocca il caso normale" if ok3 else "*** li cambia ***"))
    e.append(ok3)
    # e OLTRE il taglio DEVONO differire, senno' la cura non curerebbe niente
    g2 = np.concatenate([np.linspace(-2 * np.pi + 1e-6, -np.pi - 1e-6, 50000),
                         np.linspace(np.pi + 1e-6, 2 * np.pi - 1e-6, 50000)])
    d2 = float(np.min(np.abs(w2(g2, DT) - w4(g2, DT))))
    ok4 = d2 > 100.0
    W("K4 OLTRE il taglio DEVONO differire: min|diff| = %.3e -> %s\n"
      % (d2, "OK" if ok4 else "*** la cura non curerebbe niente ***"))
    e.append(ok4)
    # il wrap nuovo porta TUTTO dentro [-pi, pi]/DT
    ok5 = float(np.max(np.abs(w2(np.linspace(-2 * np.pi, 2 * np.pi, 100001), DT)))) <= np.pi / DT + 1e-6
    W("K5 il wrap NUOVO porta tutto dentro [-pi, pi]/DT -> %s\n" % ("OK" if ok5 else "*** NO ***"))
    e.append(ok5)
    ok = all(e)
    W("-" * 96 + "\n  -> %s\n\n" % ("i criteri PASSANO" if ok else "*** NON PASSANO ***"))
    return ok


def braccio(nome):
    """Pattern 1: un processo tutto suo."""
    import runpy
    dest = DEST_INERZIA if nome == "OFF" else os.path.join(RADICE, "csv", "_test_fork", "_rw_on")
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
            S.RITMO_WRAP_2PI = True
            return r
        S._applica_flag = _w
    sys.argv = ["_scena_video.py", "20", dest] + COMUNE
    runpy.run_path(DRIVER, run_name="__main__")
    print("[braccio %s] RITMO_WRAP_2PI = %s" % (nome, S.RITMO_WRAP_2PI))
    return 0


def main():
    try:
        os.makedirs(DEST)
    except OSError:
        pass
    o = io.open(OUT, "w", encoding="utf-8", newline="\n")
    W = o.write
    W("# SIGILLO -- `RITMO_WRAP_2PI` (`D34`)\n")
    W("# BYTE-INERTE spento, e CORREGGE il taglio acceso.\n#\n")
    if not collaudo(W):
        o.close(); print(io.open(OUT, encoding="utf-8").read()); return 1

    blob = hashlib.sha1(
        open(os.path.join(RADICE, "soliton_simulator.py"), "rb").read()).hexdigest()[:8]
    W("blob simulatore ORA (sha1 byte grezzi) %s\n" % blob)
    W("riferimento `_val600`, blob `9557a867`: ANTERIORE a questo flag\n\n")
    esiti = []

    def esito(n, ok, riga):
        esiti.append((n, ok))
        W("%-5s %-4s %s\n" % (n, "PASS" if ok else "FAIL", riga))

    # ---- T1: il default e' SPENTO, letto dal sorgente
    t = io.open(os.path.join(RADICE, "soliton_simulator.py"), encoding="utf-8").read()
    import re
    m = re.search(r"^RITMO_WRAP_2PI\s*=\s*(True|False)", t, re.M)
    ok1 = (m is not None and m.group(1) == "False")
    esito("T1", ok1, "IL DEFAULT E' SPENTO: `RITMO_WRAP_2PI = %s` (letto dal sorgente)"
          % (m.group(1) if m else "ASSENTE"))

    # ---- T2: il flag gate UNA sola ramificazione, dentro `ritmo`
    sys.path.insert(0, os.path.join(RADICE, "csv"))
    import _hook_fisica as H
    rami, assegn, _tut = H.gate(os.path.join(RADICE, "soliton_simulator.py"), "RITMO_WRAP_2PI")
    ok2 = (len(rami) == 1 and rami[0][1] == "ritmo" and len(assegn) == 1)
    esito("T2", ok2, "GATE (AST): %d ramificazione in `%s`, %d assegnamento -> %s"
          % (len(rami), rami[0][1] if rami else "?", len(assegn), rami))
    W("      -> STRUTTURALE: se comparisse un secondo ramo, o se finisse in un'altra\n")
    W("         funzione, questo criterio lo direbbe senza girare niente.\n")

    if SALTA:
        W("\nT3/T4 SALTATI su richiesta: la BYTE-INERZIA NON e' dimostrata.\n")
        esiti += [("T3", False), ("T4", False)]
    else:
        # ---- T3: BYTE-INERTE da spento, contro `_val600`
        W("\n" + "-" * 96 + "\nT3 -- BYTE-INERZIA A FLAG SPENTO (120 passi, snapshot vs snapshot)\n")
        W("-" * 96 + "\n")
        p_off = os.path.join(DEST_INERZIA, "scena_000120.pkl.gz")
        t0 = time.time()
        r = subprocess.run([sys.executable, os.path.abspath(__file__), "--braccio=OFF"],
                           cwd=RADICE, capture_output=True, text=True)
        W("  (%.1f s)\n" % (time.time() - t0))
        if not os.path.exists(p_off):
            W("  *** il braccio OFF non ha prodotto lo snapshot. uscita=%d ***\n%s\n"
              % (r.returncode, (r.stderr or "")[-1500:]))
            esiti.append(("T3", False))
            p_off = None
        else:
            ug, dv = confronta_snap(RIF120, p_off, W)
            esito("T3", dv == 0 and ug > 0,
                  "BYTE-INERTE spento: %d campi identici, %d diversi" % (ug, dv))

        # ---- T4: IL CONTROLLO POSITIVO -- acceso DEVE cambiare qualcosa
        W("\n" + "-" * 96 + "\nT4 -- IL CONTROLLO POSITIVO: acceso, DEVE cambiare qualcosa\n")
        W("-" * 96 + "\n")
        p_on = os.path.join(RADICE, "csv", "_test_fork", "_rw_on", "scena_000120.pkl.gz")
        t0 = time.time()
        r = subprocess.run([sys.executable, os.path.abspath(__file__), "--braccio=ON"],
                           cwd=RADICE, capture_output=True, text=True)
        W("  (%.1f s)\n" % (time.time() - t0))
        if not os.path.exists(p_on) or p_off is None:
            W("  *** manca uno dei due snapshot. uscita=%d ***\n%s\n"
              % (r.returncode, (r.stderr or "")[-1500:]))
            esiti.append(("T4", False))
        else:
            ug2, dv2 = confronta_snap(p_off, p_on, W)
            esito("T4", dv2 > 0,
                  "ACCESO CAMBIA: %d campi diversi contro il braccio spento" % dv2)
            W("      -> par.10 criterio 2: un sigillo che verifica solo la byte-identita' a\n")
            W("         OFF passerebbe anche su CODICE MORTO. Questo dimostra che il flag FA.\n")

    n_ok = sum(1 for _n, k in esiti if k)
    W("\n" + "=" * 96 + "\nESITO: %d/%d\n" % (n_ok, len(esiti)) + "=" * 96 + "\n")
    if n_ok == len(esiti):
        W("*** SIGILLO PASSATO. La prova a 600 passi puo' partire. ***\n")
    else:
        W("*** SIGILLO FALLITO: la prova NON parte. ***\n")
    W("\nLIMITI: `T3`/`T4` su 120 passi, UN seme, UNA scena. Cio' che li rende conclusivi non e'\n")
    W("  il numero di passi ma `T2` (strutturale) e il collaudo (risposta NOTA).\n")
    W("⚠ E `T4` dice che il flag CAMBIA, NON che il cambiamento sia una cura: su un sistema\n")
    W("  caotico due run che differiscono di 1e-16 divergono comunque. **QUANTO** e **in che\n")
    W("  direzione** lo dira' la prova a 600 passi, con le previsioni gia' scritte (`94351c9`).\n")
    o.close()
    print(io.open(OUT, encoding="utf-8").read())
    return 0 if n_ok == len(esiti) else 1


if __name__ == "__main__":
    sys.exit(braccio(BRACCIO) if BRACCIO else main())
