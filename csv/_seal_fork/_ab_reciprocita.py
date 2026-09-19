# -*- coding: utf-8 -*-
"""A/B DELLA RECIPROCITA' -- il ramo A e' anche il SIGILLO di byte-identita'.

Letture FISSATE PRIMA: doc/TASK_HISTORY/2026-09-19_reciprocita.md (9549805).
Blob del simulatore: 1a5e0796 (era 7c4dec1d). Flag: COPPIA_RECIPROCA, OFF di default.

I DUE RAMI, variabile singola
  A  snapshot 192 -> 240, blob NUOVO, flag OFF   -> DEVE riprodurre lo snapshot 240 dell'archivio
  B  snapshot 192 -> 240, blob NUOVO, flag ON    -> la cura
stesso driver, stessa cadenza, stesso seme, STESSO OVERRIDE.

*** PERCHE' IL RAMO A E' ANCHE IL SIGILLO ***
Lo snapshot 240 dell'archivio e' stato prodotto dal blob VECCHIO (7c4dec1d). Se il ramo A -- blob
NUOVO, flag OFF -- lo riproduce BYTE-IDENTICO, allora la modifica e' INERTE a flag spento:
PROVATO, non argomentato. Se non lo riproduce e' la lettura ALPHA: STOP, e il ramo B non si
guarda nemmeno.

*** L'OVERRIDE E' SIMMETRICO, ed e' il pezzo che rende l'A/B valido ***
Entrambi i rami usano --override-blob. Se solo il ramo curato saltasse `carica_stato`, la
differenza potrebbe venire DA LI'. (Rilievo di Luca.)

LE QUATTRO LETTURE
  alpha  A non riproduce il 240              -> STOP, non si guarda B
  beta   B: omega_s max resta 1e2-1e3        -> la cura NON morde: l'asimmetria non era la causa
  gamma  B: omega_s max scende DI ORDINI e l'inerzia al pavimento cala -> la cura morde
  delta  omega_s scende MA compare un'altra degenerazione -> si riporta COSI'

⚠ NESSUN NUMERO DEL RAMO B E' UN RISULTATO DI FISICA: e' un esperimento su META' RUN, e serve a
decidere se rifare il run da capo. Il mandato lo vieta esplicitamente.
ASCII PURO.
"""
import glob
import gzip
import os
import pickle
import re
import shutil
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
sys.path.insert(0, _QUI)
from _sigillo_archivio import uguale_contenuto

DRIVER = os.path.join(RADICE, "csv", "_test_fork", "_scena_video_ripresa.py")
# ⚠ L'ARCHIVIO DI RIFERIMENTO E' _fin_B, NON _g6000: il passo 192 NON ESISTE in _g6000, che ha
# cadenza 60 (60, 120, 180, 240...). Il 192 e' nella rigiocata fine a 6 passi -- e quella
# rigiocata e' SIGILLATA 3/3: il suo snapshot 240 e' gia' stato verificato BYTE-IDENTICO a
# quello di _g6000 (voce SB di _rigioca_finestre.txt). Quindi il confronto del ramo A contro
# _fin_B/scena_000240 e' equivalente al confronto contro l'archivio, e lo e' PER MISURA.
ARCH = os.path.join(RADICE, "csv", "_test_fork", "_fin_B")
PPF = 6
DA, A_ = 192, 240
esiti = []


def segna(n, ok, d):
    esiti.append((n, ok, d))
    print("%-5s %-6s %s" % (n, "PASS" if ok else "FAIL", d), flush=True)


def carica(p):
    ap = gzip.open if p.endswith(".gz") else open
    with ap(p, "rb") as f:
        return pickle.load(f)


def gira(dest, extra):
    os.makedirs(dest, exist_ok=True)
    shutil.copy2(os.path.join(ARCH, "scena_%06d.pkl.gz" % DA),
                 os.path.join(dest, "scena_%06d.pkl.gz" % DA))
    cmd = [sys.executable, DRIVER, str(A_ // PPF), dest, "--serie=1",
           "--riprendi", "--override-blob"]
    if extra:
        cmd.append("--extra=" + extra)
    t0 = time.time()
    pr = subprocess.run(cmd, cwd=RADICE, capture_output=True, text=True,
                        encoding="utf-8", errors="replace", timeout=7200)
    return pr, time.time() - t0


def stat(at):
    om = np.linalg.norm(np.asarray(at["omega_s"], float), axis=1)
    n = len(at["eta"])
    deg = np.asarray(at["_deg"], float)[:n]
    r = np.asarray(at["_r_corrente"], float); r = r[np.isfinite(r)]
    d0 = np.asarray(at["d0"], float)
    f = np.asarray(at.get("_fatt_cs_ultimo", []), float)
    pav = at.get("_inerzia_al_pavimento", 0); tot = max(at.get("_inerzia_tot", 1), 1)
    return dict(n=n, om50=float(np.median(om)), om95=float(np.percentile(om, 95)),
                ommax=float(om.max()), sopra=int(np.sum(om > 1e2)),
                deg50=float(np.median(deg)), r50=float(np.median(r)) if r.size else float("nan"),
                d0max=float(d0.max()), fcsmax=float(f.max()) if f.size else float("nan"),
                pav=pav / tot, om=om)


def main():
    base = os.path.join(RADICE, "csv", "_seal_fork", "_ab_tmp")
    shutil.rmtree(base, ignore_errors=True)
    A = os.path.join(base, "A"); B = os.path.join(base, "B")
    try:
        print("RAMO A: blob NUOVO, flag OFF  (deve riprodurre l'archivio)")
        prA, tA = gira(A, None)
        print("   rc=%s in %.0f s" % (prA.returncode, tA))
        ov = [r for r in (prA.stdout or "").splitlines() if "OVERRIDE" in r]
        print("   %s" % (ov[0].strip() if ov else "*** nessuna riga OVERRIDE ***"))
        pa = os.path.join(A, "scena_%06d.pkl.gz" % A_)
        if not os.path.exists(pa):
            for r in (prA.stdout + prA.stderr).splitlines()[-12:]:
                print("      | " + r)
            segna("SA", False, "il ramo A non ha prodotto lo snapshot %d" % A_)
            return 1
        rif = carica(os.path.join(ARCH, "scena_%06d.pkl.gz" % A_))["attrs"]
        va = carica(pa)["attrs"]
        kc = sorted(set(rif) & set(va)); soli = sorted(set(rif) ^ set(va))
        guai = [k for k in kc if not uguale_contenuto(rif[k], va[k])]
        ok_a = (not guai) and (not soli) and len(kc) > 50
        segna("SA", ok_a, "ramo A contro archivio: %d campi, %d diversi%s"
              % (len(kc), len(guai), ("  -> " + str(guai[:6])) if guai else "  -> IDENTICO"))
        if not ok_a:
            print("")
            print("VERDETTO: *** LETTURA ALPHA. La modifica NON e' inerte a flag OFF. ***")
            print("  Il ramo B NON si guarda: una cura che cambia il comportamento a flag SPENTO")
            print("  ha gia' toccato cio' che non doveva.")
            return 1

        print("")
        print("RAMO B: blob NUOVO, flag ON (--coppia-reciproca)")
        prB, tB = gira(B, "--coppia-reciproca")
        print("   rc=%s in %.0f s" % (prB.returncode, tB))
        att = [r for r in (prB.stdout or "").splitlines() if "coppia-reciproca" in r.lower()]
        print("   flag letto dal modulo: %s" % (att[0].strip()[:100] if att else "(nessun avviso)"))
        pb = os.path.join(B, "scena_%06d.pkl.gz" % A_)
        if not os.path.exists(pb):
            for r in (prB.stdout + prB.stderr).splitlines()[-12:]:
                print("      | " + r)
            segna("SB", False, "il ramo B non ha prodotto lo snapshot %d" % A_)
            return 1
        segna("SB", True, "ramo B prodotto")

        print("")
        print("=" * 116)
        print("IL CONFRONTO, passo %d -> %d" % (DA, A_))
        print("=" * 116)
        print("%-10s | %-11s %-11s %-11s %-8s | %-8s %-8s %-9s %-9s %-8s"
              % ("ramo", "om p50", "om p95", "om MAX", "n>1e2", "deg p50", "r p50",
                 "d0 max", "fcs max", "pav/tot"))
        fs = {"A (OFF)": os.path.join(A, "scena_%06d.pkl.gz" % A_),
              "B (ON)": pb, "archivio": os.path.join(ARCH, "scena_%06d.pkl.gz" % A_)}
        S = {}
        for nome, p in fs.items():
            s = stat(carica(p)["attrs"]); S[nome] = s
            print("%-10s | %-11.4g %-11.4g %-11.4g %-8d | %-8.0f %-8.4f %-9.4g %-9.4g %-8.4f"
                  % (nome, s["om50"], s["om95"], s["ommax"], s["sopra"],
                     s["deg50"], s["r50"], s["d0max"], s["fcsmax"], s["pav"]))
        # il nodo 2393
        print("")
        print("IL NODO 2393 (il neonato che parte al 198)")
        print("%-10s | %-12s %-12s %-12s %-12s" % ("ramo", "|omega_s|", "ramp", "rho_spin", "deg"))
        for nome, p in fs.items():
            at = carica(p)["attrs"]
            om = np.linalg.norm(np.asarray(at["omega_s"], float), axis=1)
            eta = np.asarray(at["eta"], float)
            import soliton_simulator as _S
            k = 2393
            print("%-10s | %-12.6g %-12.6g %-12.6g %-12.0f"
                  % (nome, om[k], min(1.0, eta[k] / float(_S.TAU_A)),
                     float(np.asarray(at["rho_spin"], float)[k]),
                     float(np.asarray(at["_deg"], float)[k])))
        print("")
        a, b = S["A (OFF)"], S["B (ON)"]
        rap = b["ommax"] / a["ommax"] if a["ommax"] else float("nan")
        print("omega_s MAX:  A = %.4g   B = %.4g   ->  B/A = %.4g" % (a["ommax"], b["ommax"], rap))
        print("nodi > 1e2 :  A = %d      B = %d" % (a["sopra"], b["sopra"]))
        print("inerzia pav:  A = %.4f   B = %.4f" % (a["pav"], b["pav"]))
        print("")
        if rap > 0.1:
            print("-> LETTURA BETA: omega_s max resta dello stesso ordine (B/A = %.3g)." % rap)
            print("   LA CURA NON MORDE: l'asimmetria non era la causa dell'evento.")
        elif b["pav"] <= a["pav"]:
            print("-> LETTURA GAMMA: omega_s max scende di %.3g ordini e l'inerzia al pavimento"
                  % (-np.log10(max(rap, 1e-300))))
            print("   NON sale. LA CURA MORDE. Si riporta a Luca per la decisione del par.3.")
        else:
            print("-> LETTURA DELTA: omega_s scende (B/A = %.3g) MA l'inerzia al pavimento SALE"
                  % rap)
            print("   (%.4f -> %.4f). Una cura che sposta il problema NON e' una cura." % (a["pav"], b["pav"]))
        print("")
        print("NESSUN NUMERO DEL RAMO B E' UN RISULTATO DI FISICA: esperimento su META' RUN.")
        return 0
    finally:
        shutil.rmtree(base, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
