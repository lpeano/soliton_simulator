# -*- coding: utf-8 -*-
"""SIGILLO DI `--sep` SUL DRIVER -- a default fa ESATTAMENTE quello che faceva.

Il driver aveva `--sep 8` CABLATO. Ora e' `--sep=X` NOMINALE con default `8`, nello stesso idioma
di `--serie=` e `--csv-progresso=`. Il rito del par.2 chiede DUE cose, e qui ci sono entrambe:

  S1  BYTE-IDENTICO A DEFAULT: il driver NUOVO, senza `--sep`, deve dare lo STESSO stato del
      driver VECCHIO (il blob committato PRIMA del cambiamento), a parita' di tutto il resto.
  S2  CONTROLLO POSITIVO: con `--sep=4.0` gli stati DEVONO differire. Un sigillo che verifica solo
      la byte-identita' a default passerebbe anche su codice morto (par.10.2).
  S3  E LA GEOMETRIA E' QUELLA CHIESTA, non una qualunque: a `--sep=4.0` le distanze fra i centri
      delle tre masse devono valere `4.0*sqrt(3) = 6.928`, non `8*sqrt(3)`.

Il criterio di confronto e' `uguale_contenuto` di `_sigillo_archivio.py`: IL criterio, non una sua
copia.

IL DRIVER VECCHIO si estrae da git IN BINARIO (`git cat-file -p <commit>:<path>`), mai con
`git checkout`: par.5-quinquies, la trappola CRLF.
ASCII PURO.
"""
import os
import pickle
import gzip
import glob
import re
import shutil
import subprocess
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, RADICE)
sys.path.insert(0, _QUI)
from _sigillo_archivio import uguale_contenuto      # IL criterio, non una sua copia

DRIVER = os.path.join(RADICE, "csv", "_test_fork", "_scena_video.py")
# il commit che contiene il driver PRIMA di `--sep`: quello della ripresa
COMMIT_PRIMA = "2a6e83c"
NF = 4              # frame per braccio: bastano, il criterio confronta 113 campi
OGNI = 2            # snapshot ogni 2 frame = 12 passi
BASE = os.path.join(RADICE, "csv", "_seal_fork", "_sig_sep")

esiti = []


def segna(nome, ok, det):
    esiti.append((nome, ok))
    print("%-4s %-6s %s" % (nome, "PASS" if ok else "FAIL", det))


def carica(p):
    ap = gzip.open if p.endswith(".gz") else open
    with ap(p, "rb") as f:
        return pickle.load(f)["attrs"]


def serie(d):
    fs = sorted(glob.glob(os.path.join(d, "scena_??????.pkl*")))
    return [(int(re.search(r"_(\d{6})\.", p).group(1)), p) for p in fs]


def gira(driver, dest, extra=()):
    if os.path.isdir(dest):
        shutil.rmtree(dest)      # cartella di SIGILLO, creata da questo script: non e' un archivio
    os.makedirs(dest, exist_ok=True)
    cmd = [sys.executable, driver, str(NF), dest, "--serie=%d" % OGNI] + list(extra)
    pr = subprocess.run(cmd, cwd=RADICE, capture_output=True, text=True,
                        encoding="utf-8", errors="replace")
    if pr.returncode != 0:
        print(pr.stdout[-2000:])
        print(pr.stderr[-2000:])
        raise SystemExit("il driver e' uscito con %d: %s" % (pr.returncode, " ".join(cmd)))
    return pr.stdout


def main():
    os.makedirs(BASE, exist_ok=True)
    vecchio = os.path.join(BASE, "_driver_prima.py")
    q = subprocess.run(["git", "cat-file", "-p", "%s:csv/_test_fork/_scena_video.py" % COMMIT_PRIMA],
                       cwd=RADICE, capture_output=True)
    if q.returncode != 0:
        raise SystemExit("non riesco a estrarre il driver di %s" % COMMIT_PRIMA)
    with open(vecchio, "wb") as f:          # BINARIO: niente riscrittura delle newline
        f.write(q.stdout)
    import hashlib
    print("driver PRIMA (%s): sha1 grezzo %s" % (COMMIT_PRIMA, hashlib.sha1(q.stdout).hexdigest()[:8]))
    with open(DRIVER, "rb") as f:
        dn = f.read()
    print("driver ORA            : sha1 grezzo %s" % hashlib.sha1(dn).hexdigest()[:8])
    print("")

    dA = os.path.join(BASE, "A_vecchio_default")
    dB = os.path.join(BASE, "B_nuovo_default")
    dC = os.path.join(BASE, "C_nuovo_sep4")
    print("braccio A: driver VECCHIO, default")
    gira(vecchio, dA)
    print("braccio B: driver NUOVO,   default")
    gira(DRIVER, dB)
    print("braccio C: driver NUOVO,   --sep=4.0")
    outC = gira(DRIVER, dC, ["--sep=4.0"])
    print("")

    sA, sB, sC = serie(dA), serie(dB), serie(dC)
    ok = [p for p, _ in sA] == [p for p, _ in sB] == [p for p, _ in sC]
    segna("S0", ok, "i tre bracci hanno gli STESSI passi: %s" % [p for p, _ in sA])
    if not sA or not sB:
        segna("S1", False, "manca uno dei due archivi")
        return 1

    a = carica(sA[-1][1])
    b = carica(sB[-1][1])
    kc = sorted(set(a) & set(b))
    diff = [k for k in kc if not uguale_contenuto(a[k], b[k])]
    segna("S1", not diff and len(set(a) ^ set(b)) == 0,
          "default: %d campi confrontati, %d diversi  -> %s"
          % (len(kc), len(diff), "IDENTICO" if not diff else "DIVERSI: %s" % diff[:6]))

    c = carica(sC[-1][1])
    kk = sorted(set(a) & set(c))
    dif2 = [k for k in kk if not uguale_contenuto(a[k], c[k])]
    segna("S2", len(dif2) > 0,
          "--sep=4.0 contro default: %d campi diversi su %d -> il flag FA QUALCOSA"
          % (len(dif2), len(kk)))

    # S3: LA GEOMETRIA E' PROPRIO QUELLA CHIESTA, non una qualunque.
    # Non si importa il simulatore ne' si cablano gli indici delle coorti: si guarda l'ESTENSIONE
    # RADIALE, che a sep dato vale `sep + raggio_massa` (le masse stanno su un cerchio di raggio
    # `sep` e hanno raggio ~0.72 misurato). E' un controllo senza assunzioni sugli indici.
    def estensione(at):
        pos = np.asarray(at["pos"])[:len(at["eta"])]
        return float(np.abs(np.linalg.norm(pos, axis=1)).max())

    eA, eC = estensione(a), estensione(c)
    attA, attC = 8.0 + 0.72, 4.0 + 0.72
    okA = abs(eA - attA) / attA < 0.12
    okC = abs(eC - attC) / attC < 0.12
    segna("S3", okA and okC,
          "estensione radiale: default %.3f (atteso ~%.2f) | --sep=4.0 %.3f (atteso ~%.2f)"
          % (eA, attA, eC, attC))

    print("")
    n_pass = sum(1 for _, o in esiti if o)
    print("ESITO: %d/%d" % (n_pass, len(esiti)))
    print("")
    if n_pass == len(esiti):
        print("VERDETTO: `--sep` e' INERTE A DEFAULT e FA QUALCOSA quando si passa.")
        print("  Il comando di `Z49` resta riproducibile VERBATIM.")
    else:
        print("VERDETTO: IL SIGILLO NON PASSA. Il driver NON si usa per il run.")
    print("NB: UNA scena, UN seme, %d frame. Prova che il DEFAULT non e' cambiato," % NF)
    print("  non che ogni valore di sep si comporti bene.")
    return 0 if n_pass == len(esiti) else 1


if __name__ == "__main__":
    sys.exit(main())
