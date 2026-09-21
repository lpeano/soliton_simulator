# -*- coding: utf-8 -*-
"""SIGILLO DI `--chi-coop=on|off` SUL DRIVER -- a default fa ESATTAMENTE quello che faceva.

Il driver non ha MAI passato `--chi-coop` (il flag nasce oggi), quindi il DEFAULT e' `off` --
l'opposto di `--chi-basc=on`, e per la STESSA ragione: il default e' quello che riproduce
l'argv ATTUALE VERBATIM.

⚠ QUESTO SIGILLO ISOLA IL DRIVER, NON IL SIMULATORE. Il driver VECCHIO, estratto da git, importa
  `soliton_simulator` dalla RADICE, cioe' il simulatore di OGGI. E' voluto: qui si misura se
  l'opzione nuova ha cambiato l'argv, e la byte-identita' del SIMULATORE e' `Z1` dell'altro
  sigillo (`_sigillo_chicoop.py`). Due domande diverse, due sigilli.

  D0  i due blob, in BYTE GREZZI (`sha1`), mai `git hash-object` (C18).
  D1  [BLOCCANTE] driver NUOVO a default == driver VECCHIO. Una divergenza = STOP.
  D2  CONTROLLO POSITIVO: con `--chi-coop=on` gli stati DEVONO differire. Un sigillo di sola
      byte-identita' passerebbe anche su codice morto (par.10.2).
  D3  E DIFFERISCONO PER LA COSA GIUSTA: `CHI_COOP` letto DAL MODULO (P6: dai dati, non dal
      comando) deve valere `False` a default e `True` con `on`. D2 dice che il flag cambia
      QUALCOSA, D3 che cambia LA COSA GIUSTA.
  D4  E NIENT'ALTRO E' CAMBIATO: gli altri flag identici fra i tre bracci -- par.1 (un
      interruttore alla volta) VERIFICATO invece che asserito. `CHI_BASC` ci sta DENTRO, ed e'
      il punto: la cooperazione NON deve spegnere `chi_basc`.

IL DRIVER VECCHIO si estrae da git IN BINARIO (`git cat-file -p <commit>:<path>`), mai con
`git checkout`: par.5-quinquies, la trappola CRLF.
ASCII PURO.
"""
import glob
import gzip
import hashlib
import os
import pickle
import re
import shutil
import subprocess
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, RADICE)
sys.path.insert(0, _QUI)
from _sigillo_archivio import uguale_contenuto      # IL criterio, non una sua copia

DRIVER = os.path.join(RADICE, "csv", "_test_fork", "_scena_video.py")
COMMIT_PRIMA = "79be011"        # il driver PRIMA di `--chi-coop=`
for _x in sys.argv[1:]:
    if _x.startswith("--commit-prima="):
        COMMIT_PRIMA = _x.split("=", 1)[1]
NF = 4
OGNI = 2
BASE = os.path.join(RADICE, "csv", "_seal_fork", "_sig_chicoop_driver")
FLAG_ALTRI = ("CAMPO_SPINORIALE", "SPINORE_VIVO", "SPINORE_CORRETTO", "CHI_CORE", "CS_DINAMICO",
              "TAU_LUCE", "CHI_BASC", "FORK_SU2", "FORK_SU2_MEM", "STEP2_OROLOGIO",
              "SPIN_FEEDBACK", "CALORE_VETTORIALE", "PLAST_DIN", "VERLET", "TAU_LOC")

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
    d = {}
    for m in re.finditer(r"^    ([A-Z_0-9]+)\s+(True|False|ASSENTE)\s*$", out, re.M):
        d[m.group(1)] = m.group(2)
    return d


def gira(driver, dest, extra=()):
    if os.path.isdir(dest):
        shutil.rmtree(dest)      # cartella di SIGILLO, creata da questo script
    os.makedirs(dest, exist_ok=True)
    cmd = [sys.executable, driver, str(NF), dest, "--serie=%d" % OGNI] + list(extra)
    pr = subprocess.run(cmd, cwd=RADICE, capture_output=True, text=True,
                        encoding="utf-8", errors="replace")
    if pr.returncode != 0:
        print(pr.stdout[-2000:]); print(pr.stderr[-2000:])
        raise SystemExit("il driver e' uscito con %d: %s" % (pr.returncode, " ".join(cmd)))
    return pr.stdout


def main():
    os.makedirs(BASE, exist_ok=True)
    # IL DRIVER ESTRATTO VA MESSO DOVE IL DRIVER VIVE: fa `sys.path.insert(0, <suo_dir>/..)`
    # per trovare `_presidio`, quindi altrove muore con ModuleNotFoundError. Misurato, non previsto.
    vecchio = os.path.join(RADICE, "csv", "_test_fork", "_driver_prima_chicoop.py")
    q = subprocess.run(["git", "cat-file", "-p",
                        "%s:csv/_test_fork/_scena_video.py" % COMMIT_PRIMA],
                       cwd=RADICE, capture_output=True)
    if q.returncode != 0:
        raise SystemExit("non riesco a estrarre il driver di %s" % COMMIT_PRIMA)
    with open(vecchio, "wb") as f:          # BINARIO: niente riscrittura delle newline
        f.write(q.stdout)
    print("D0  driver PRIMA (%s): sha1 GREZZO %s"
          % (COMMIT_PRIMA, hashlib.sha1(q.stdout).hexdigest()[:8]))
    with open(DRIVER, "rb") as f:
        dn = f.read()
    print("D0  driver ORA            : sha1 GREZZO %s" % hashlib.sha1(dn).hexdigest()[:8])
    print("D0  (NB: NON e' `git hash-object`. C18.)")
    print("")

    dA = os.path.join(BASE, "A_vecchio_default")
    dB = os.path.join(BASE, "B_nuovo_default")
    dC = os.path.join(BASE, "C_nuovo_coop")
    print("braccio A: driver VECCHIO, default        (nessun `--chi-coop`)")
    outA = gira(vecchio, dA)
    print("braccio B: driver NUOVO,   default        (atteso: identico ad A)")
    outB = gira(DRIVER, dB)
    print("braccio C: driver NUOVO,   --chi-coop=on  (atteso: DIVERSO)")
    outC = gira(DRIVER, dC, ["--chi-coop=on"])
    print("")

    sA, sB, sC = serie(dA), serie(dB), serie(dC)
    segna("D0b", [p for p, _ in sA] == [p for p, _ in sB] == [p for p, _ in sC],
          "i tre bracci hanno gli STESSI passi: %s" % [p for p, _ in sA])
    if not sA or not sB:
        segna("D1", False, "manca uno dei due archivi")
        return 1

    a, b = carica(sA[-1][1]), carica(sB[-1][1])
    kc = sorted(set(a) & set(b))
    diff = [k for k in kc if not uguale_contenuto(a[k], b[k])]
    ok1 = (not diff) and len(set(a) ^ set(b)) == 0
    segna("D1", ok1, "default: %d campi confrontati, %d diversi -> %s"
          % (len(kc), len(diff), "IDENTICO" if not diff else "DIVERSI: %s" % diff[:6]))
    if not ok1:
        print("  *** D1 e' BLOCCANTE: il default NON riproduce il driver di prima. FERMO. ***")
        return 1

    c = carica(sC[-1][1])
    kk = sorted(set(a) & set(c))
    dif2 = [k for k in kk if not uguale_contenuto(a[k], c[k])]
    segna("D2", len(dif2) > 0,
          "--chi-coop=on contro default: %d campi diversi su %d -> il flag FA QUALCOSA"
          % (len(dif2), len(kk)))

    fA, fB, fC = flag_dal_modulo(outA), flag_dal_modulo(outB), flag_dal_modulo(outC)
    segna("D3", fB.get("CHI_COOP") == "False" and fC.get("CHI_COOP") == "True",
          "CHI_COOP DAL MODULO: nuovo-default=%s  nuovo-on=%s   (il driver vecchio non lo stampa: %s)"
          % (fB.get("CHI_COOP"), fC.get("CHI_COOP"), fA.get("CHI_COOP", "assente dalla lista")))

    sbagliati = [f for f in FLAG_ALTRI if not (fA.get(f) == fB.get(f) == fC.get(f))]
    segna("D4", not sbagliati,
          "gli altri %d flag identici nei TRE bracci (CHI_BASC COMPRESO: la cooperazione NON lo "
          "spegne): %s" % (len(FLAG_ALTRI), "si'" if not sbagliati
                           else "NO -> %s" % [(f, fA.get(f), fC.get(f)) for f in sbagliati]))

    print("")
    n_pass = sum(1 for _, o in esiti if o)
    print("ESITO: %d/%d" % (n_pass, len(esiti)))
    print("")
    if n_pass == len(esiti):
        print("VERDETTO: `--chi-coop=` e' INERTE A DEFAULT, FA QUALCOSA con `on`, e la cosa che fa")
        print("  e' accendere CHI_COOP LASCIANDO ACCESO CHI_BASC. Il driver si puo' usare.")
    else:
        print("VERDETTO: IL SIGILLO NON PASSA. Il driver NON si usa per il run.")
    print("NB: UNA scena, UN seme, %d frame. Prova che il DEFAULT non e' cambiato e che l'opzione" % NF)
    print("  agisce sul flag giusto, NON che la cooperazione produca una fisica migliore.")
    return 0 if n_pass == len(esiti) else 1


if __name__ == "__main__":
    sys.exit(main())
