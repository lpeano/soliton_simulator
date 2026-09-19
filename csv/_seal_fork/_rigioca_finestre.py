# -*- coding: utf-8 -*-
"""LE DUE FINESTRE FINI -- rigiocate a risoluzione 6 passi, CON IL LORO SIGILLO.

PERCHE' DUE E NON UNA (mandato di Luca, 2026-09-19)
  B) 180 -> 240: l'intervallo in cui `omega_s` max salta di CINQUE ORDINI (0.35 -> 7.58e+04) e
     `r` p25 crolla (1.2094 -> 0.2991). 60 passi di risoluzione non bastano a dire cosa accade.
  A) 0 -> 60: **`r` era GIA' AL TETTO al primo snapshot** (p25/p50/p75 = 1.4126/1.4141/1.4142).
     Quindi la domanda non e' "quando si rompe" ma "ERA GIA' ROTTO ALLA NASCITA?".
     Se `r` nasce al tetto, `ritmo()` non degenera: PARTE FUORI SCALA -- e sarebbe un difetto di
     FORMA, non un evento. Questa finestra e' l'unica che l'archivio non puo' dare.

*** LA RISOLUZIONE E' 6 PASSI, NON 5, E IL PERCHE' VA DETTO ***
  Il mandato chiede `--db-ogni 5`. Ma quello e' il flag di `batch_condensazione`; QUI gira il
  DRIVER della scena, che campiona in FRAME, e `PASSI_PER_FRAME = 6`. La granularita' piu' fine
  ottenibile e' UN FRAME = 6 passi -> `--serie=1`. Si ottengono DIECI istanti per finestra, non
  dodici. Non e' un dettaglio da tacere: e' il limite dello strumento.

*** IL SIGILLO, e se non passa SI FERMA ***
  A) partendo da ZERO, lo stato al passo 60 deve essere IDENTICO a `scena_000060.pkl.gz`.
     (E' anche un test di riproducibilita' del run da capo, che non era mai stato fatto.)
  B) ripartendo dal passo 180, lo stato al passo 240 deve essere IDENTICO a `scena_000240.pkl.gz`.
  Il criterio di confronto si IMPORTA da `_sigillo_archivio` -- quello gia' corretto una volta --
  e NON si riscrive.

NON TOCCA L'ARCHIVIO: `_g6000` si legge in sola lettura; si scrive in cartelle NUOVE.
Il driver usato e' `_scena_video_ripresa.py`, perche' quello del run e' stato ripristinato a
`f14ea4bd` e NON ha `--riprendi`. Va dichiarato in ogni referto che usi questi dati.
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

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, RADICE)
sys.path.insert(0, _QUI)
from _sigillo_archivio import uguale_contenuto

DRIVER = os.path.join(RADICE, "csv", "_test_fork", "_scena_video_ripresa.py")
ARCH = os.path.join(RADICE, "csv", "_test_fork", "_g6000")
PPF = 6
esiti = []


def segna(n, ok, d):
    esiti.append((n, ok, d))
    print("%-5s %-6s %s" % (n, "PASS" if ok else "FAIL", d), flush=True)


def carica(p):
    ap = gzip.open if p.endswith(".gz") else open
    with ap(p, "rb") as f:
        return pickle.load(f)


def confronta(p_atteso, p_ottenuto, tag):
    a = carica(p_atteso)["attrs"]
    b = carica(p_ottenuto)["attrs"]
    kc = sorted(set(a) & set(b))
    soli = sorted(set(a) ^ set(b))
    guai = [k for k in kc if not uguale_contenuto(a[k], b[k])]
    ok = (not guai) and (not soli) and len(kc) > 50
    segna(tag, ok, "%d campi confrontati, %d diversi%s%s"
          % (len(kc), len(guai), ("  -> " + str(guai[:6])) if guai else "  -> IDENTICO",
             ("  chiavi sole: " + str(soli[:5])) if soli else ""))
    return ok


def gira(dest, nframe, riprendi):
    cmd = [sys.executable, DRIVER, str(nframe), dest, "--serie=1"]
    if riprendi:
        cmd.append("--riprendi")
    t0 = time.time()
    pr = subprocess.run(cmd, cwd=RADICE, capture_output=True, text=True,
                        encoding="utf-8", errors="replace", timeout=7200)
    return pr, time.time() - t0


def passi_in(d):
    return sorted(int(re.search(r"_(\d{6})\.", p).group(1))
                  for p in glob.glob(os.path.join(d, "scena_??????.pkl*")))


def main():
    print("risoluzione: 1 frame = %d passi (il driver campiona in FRAME; --db-ogni 5 non e'"
          " rappresentabile)" % PPF)
    print("")
    # ---------------- FINESTRA A: 0 -> 60, DA ZERO ----------------------------
    A = os.path.join(RADICE, "csv", "_test_fork", "_fin_A")
    shutil.rmtree(A, ignore_errors=True)
    os.makedirs(A)
    print("FINESTRA A: dal passo 0 al 60, DA ZERO (nessuna ripresa). 10 frame.")
    prA, tA = gira(A, 60 // PPF, riprendi=False)
    pa = passi_in(A)
    print("   passi prodotti: %s   in %.0f s   rc=%s" % (pa, tA, prA.returncode))
    if prA.returncode != 0:
        for r in (prA.stdout + prA.stderr).splitlines()[-10:]:
            print("      | " + r)
    ok_a = confronta(os.path.join(ARCH, "scena_000060.pkl.gz"),
                     os.path.join(A, "scena_000060.pkl.gz"), "SA") \
        if os.path.exists(os.path.join(A, "scena_000060.pkl.gz")) else \
        (segna("SA", False, "lo snapshot 60 non e' stato prodotto"), False)[1]

    # ---------------- FINESTRA B: 180 -> 240, CON RIPRESA ---------------------
    print("")
    B = os.path.join(RADICE, "csv", "_test_fork", "_fin_B")
    shutil.rmtree(B, ignore_errors=True)
    os.makedirs(B)
    shutil.copy2(os.path.join(ARCH, "scena_000180.pkl.gz"),
                 os.path.join(B, "scena_000180.pkl.gz"))
    print("FINESTRA B: dal passo 180 al 240, RIPRESA dallo snapshot 180. fino al frame 40.")
    prB, tB = gira(B, 240 // PPF, riprendi=True)
    pb = passi_in(B)
    print("   passi prodotti: %s   in %.0f s   rc=%s" % (pb, tB, prB.returncode))
    rip = [r for r in (prB.stdout or "").splitlines() if "RIPRESA" in r]
    print("   %s" % (rip[0].strip() if rip else "*** nessuna riga RIPRESA ***"))
    if prB.returncode != 0:
        for r in (prB.stdout + prB.stderr).splitlines()[-10:]:
            print("      | " + r)
    ok_b = confronta(os.path.join(ARCH, "scena_000240.pkl.gz"),
                     os.path.join(B, "scena_000240.pkl.gz"), "SB") \
        if os.path.exists(os.path.join(B, "scena_000240.pkl.gz")) else \
        (segna("SB", False, "lo snapshot 240 non e' stato prodotto"), False)[1]

    # ---------------- CONTROPROVA: il confronto sa dire DIVERSO? --------------
    print("")
    try:
        d = not uguale_contenuto(
            carica(os.path.join(ARCH, "scena_000060.pkl.gz"))["attrs"]["eta"],
            carica(os.path.join(ARCH, "scena_002700.pkl.gz"))["attrs"]["eta"])
        segna("SC", d, "due istanti DIVERSI risultano diversi: il confronto NON e' cieco")
    except Exception as e:
        segna("SC", False, "controprova non eseguibile: %s" % e)

    print("")
    ok = sum(1 for _, o, _ in esiti if o)
    print("ESITO: %d/%d" % (ok, len(esiti)))
    print("")
    if ok_a and ok_b:
        print("VERDETTO: LE DUE FINESTRE SONO RIPRODOTTE FEDELMENTE.")
        print("  A: ripartendo DA ZERO si riottiene lo snapshot 60 -- il run e' riproducibile da capo.")
        print("  B: ripartendo dal 180 si riottiene lo snapshot 240.")
        print("  I dati fini sono in csv/_test_fork/_fin_A e _fin_B, e si leggono con _cronologia.py.")
    else:
        print("VERDETTO: *** LA RIPRODUZIONE NON COMBACIA. SI FERMA. ***")
        print("  Non si legge la cronologia fine di una finestra che non riproduce l'originale:")
        print("  sarebbe una traiettoria DIVERSA raccontata come se fosse la stessa.")
    return 0 if (ok_a and ok_b) else 1


if __name__ == "__main__":
    sys.exit(main())
