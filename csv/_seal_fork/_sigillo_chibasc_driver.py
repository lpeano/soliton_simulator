# -*- coding: utf-8 -*-
"""SIGILLO DI `--chi-basc=on|off` SUL DRIVER -- a default fa ESATTAMENTE quello che faceva.

Il driver aveva `--chi-basc` CABLATO nell'argv (`:109`). Ora e' `--chi-basc=on|off` NOMINALE con
default `on`, nello stesso idioma di `--serie=`, `--csv-progresso=` e `--sep=`.

⚠ NON E' UNA MODIFICA AL SIMULATORE: `CHI_BASC = False` e' gia' il default di MODULO (`:746`), ed
  era il DRIVER ad accenderlo. Qui si rende esplicito un interruttore che c'era gia'.

Il rito del par.2 chiede DUE cose, e qui ce ne sono TRE:

  C1  BYTE-IDENTICO A DEFAULT [BLOCCANTE]: il driver NUOVO, senza l'opzione, deve dare lo STESSO
      stato del driver VECCHIO (il blob committato PRIMA del cambiamento).
  C2  CONTROLLO POSITIVO: con `--chi-basc=off` gli stati DEVONO differire. Un sigillo che verifica
      solo la byte-identita' a default passerebbe anche su codice morto (par.10.2).
  C3  E DIFFERISCONO PER LA COSA GIUSTA: `CHI_BASC` letto DAL MODULO (il driver lo stampa dopo
      `_applica_flag`, che e' il percorso ufficiale, P6: dai dati e non dal comando) deve valere
      `True` a default e `False` con `off`. C2 dice che il flag cambia QUALCOSA, C3 che cambia LA
      COSA GIUSTA -- ed e' la differenza fra questo sigillo e uno che passerebbe anche se
      l'opzione spegnesse per sbaglio `--plast-din`.
  C4  E NIENT'ALTRO E' CAMBIATO: gli altri 14 flag stampati devono essere IDENTICI fra i tre
      bracci. E' il par.1 (un interruttore alla volta) VERIFICATO invece che asserito.

Il criterio di confronto e' `uguale_contenuto` di `_sigillo_archivio.py`: IL criterio, non una sua
copia. IL DRIVER VECCHIO si estrae da git IN BINARIO (`git cat-file -p <commit>:<path>`), mai con
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
# il commit che contiene il driver PRIMA di `--chi-basc=`: quello del task history di oggi
COMMIT_PRIMA = "bb1d727"
for _x in sys.argv[1:]:
    if _x.startswith("--commit-prima="):
        COMMIT_PRIMA = _x.split("=", 1)[1]
NF = 4              # frame per braccio: bastano, il criterio confronta oltre 100 campi
OGNI = 2            # snapshot ogni 2 frame = 12 passi
BASE = os.path.join(RADICE, "csv", "_seal_fork", "_sig_chibasc")
FLAG_ALTRI = ("CAMPO_SPINORIALE", "SPINORE_VIVO", "SPINORE_CORRETTO", "CHI_CORE", "CS_DINAMICO",
              "TAU_LUCE", "FORK_SU2", "FORK_SU2_MEM", "STEP2_OROLOGIO", "SPIN_FEEDBACK",
              "CALORE_VETTORIALE", "PLAST_DIN", "VERLET", "TAU_LOC")

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


def flag_dal_modulo(out):
    """I flag come il MODULO li ha DOPO `_applica_flag`, non come il comando li chiedeva."""
    d = {}
    for m in re.finditer(r"^    ([A-Z_0-9]+)\s+(True|False|ASSENTE)\s*$", out, re.M):
        d[m.group(1)] = m.group(2)
    return d


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
    # IL DRIVER ESTRATTO VA MESSO DOVE IL DRIVER VIVE: fa `sys.path.insert(0, <suo_dir>/..)` per
    # trovare `_presidio`, quindi fuori da `csv/_test_fork/` muore con ModuleNotFoundError.
    # Misurato la volta scorsa, non previsto.
    vecchio = os.path.join(RADICE, "csv", "_test_fork", "_driver_prima_chibasc.py")
    q = subprocess.run(["git", "cat-file", "-p", "%s:csv/_test_fork/_scena_video.py" % COMMIT_PRIMA],
                       cwd=RADICE, capture_output=True)
    if q.returncode != 0:
        raise SystemExit("non riesco a estrarre il driver di %s" % COMMIT_PRIMA)
    with open(vecchio, "wb") as f:          # BINARIO: niente riscrittura delle newline
        f.write(q.stdout)
    import hashlib
    print("driver PRIMA (%s): sha1 grezzo %s"
          % (COMMIT_PRIMA, hashlib.sha1(q.stdout).hexdigest()[:8]))
    with open(DRIVER, "rb") as f:
        dn = f.read()
    print("driver ORA              : sha1 grezzo %s" % hashlib.sha1(dn).hexdigest()[:8])
    print("")

    dA = os.path.join(BASE, "A_vecchio_default")
    dB = os.path.join(BASE, "B_nuovo_default")
    dC = os.path.join(BASE, "C_nuovo_off")
    print("braccio A: driver VECCHIO, default          (`--chi-basc` cablato)")
    outA = gira(vecchio, dA)
    print("braccio B: driver NUOVO,   default          (atteso: identico ad A)")
    outB = gira(DRIVER, dB)
    print("braccio C: driver NUOVO,   --chi-basc=off   (atteso: DIVERSO)")
    outC = gira(DRIVER, dC, ["--chi-basc=off"])
    print("")

    sA, sB, sC = serie(dA), serie(dB), serie(dC)
    ok = [p for p, _ in sA] == [p for p, _ in sB] == [p for p, _ in sC]
    segna("C0", ok, "i tre bracci hanno gli STESSI passi: %s" % [p for p, _ in sA])
    if not sA or not sB:
        segna("C1", False, "manca uno dei due archivi")
        return 1

    a = carica(sA[-1][1])
    b = carica(sB[-1][1])
    kc = sorted(set(a) & set(b))
    diff = [k for k in kc if not uguale_contenuto(a[k], b[k])]
    ok1 = (not diff) and len(set(a) ^ set(b)) == 0
    segna("C1", ok1, "default: %d campi confrontati, %d diversi  -> %s"
          % (len(kc), len(diff), "IDENTICO" if not diff else "DIVERSI: %s" % diff[:6]))
    if not ok1:
        print("  *** C1 e' BLOCCANTE: il default NON riproduce il driver di prima. FERMO. ***")
        return 1

    c = carica(sC[-1][1])
    kk = sorted(set(a) & set(c))
    dif2 = [k for k in kk if not uguale_contenuto(a[k], c[k])]
    segna("C2", len(dif2) > 0,
          "--chi-basc=off contro default: %d campi diversi su %d -> il flag FA QUALCOSA"
          % (len(dif2), len(kk)))

    fA, fB, fC = flag_dal_modulo(outA), flag_dal_modulo(outB), flag_dal_modulo(outC)
    segna("C3", fA.get("CHI_BASC") == "True" and fB.get("CHI_BASC") == "True"
          and fC.get("CHI_BASC") == "False",
          "CHI_BASC DAL MODULO: vecchio=%s  nuovo-default=%s  nuovo-off=%s"
          % (fA.get("CHI_BASC"), fB.get("CHI_BASC"), fC.get("CHI_BASC")))

    # C4: UN INTERRUTTORE ALLA VOLTA, verificato invece che asserito.
    sbagliati = [f for f in FLAG_ALTRI
                 if not (fA.get(f) == fB.get(f) == fC.get(f))]
    segna("C4", not sbagliati,
          "gli altri %d flag sono identici nei TRE bracci: %s"
          % (len(FLAG_ALTRI), "si'" if not sbagliati
             else "NO -> %s" % [(f, fA.get(f), fC.get(f)) for f in sbagliati]))

    print("")
    n_pass = sum(1 for _, o in esiti if o)
    print("ESITO: %d/%d" % (n_pass, len(esiti)))
    print("")
    if n_pass == len(esiti):
        print("VERDETTO: `--chi-basc=` e' INERTE A DEFAULT, FA QUALCOSA con `off`, e la cosa che fa")
        print("  e' spegnere CHI_BASC e NIENT'ALTRO. Il driver si puo' usare per i due run.")
    else:
        print("VERDETTO: IL SIGILLO NON PASSA. Il driver NON si usa per il run.")
    print("NB: UNA scena, UN seme, %d frame. Prova che il DEFAULT non e' cambiato e che l'opzione" % NF)
    print("  agisce sul flag giusto, NON che `chi_basc` spento produca una fisica migliore.")
    return 0 if n_pass == len(esiti) else 1


if __name__ == "__main__":
    sys.exit(main())
