r"""**`V1` GRATIS** — il salvataggio ha toccato la fisica? Il confronto fra i DUE run del pilota.

*(Rilievo di Luca, 2026-09-27: *«confrontali con quelli di `c4517a9`; se il blob è lo stesso, le
misure devono essere IDENTICHE campo per campo»*.)*

**PERCHÉ È «GRATIS»:** il secondo run *(`pilota-prova1-stati`, con `--salva-stati --ogni 2`)* usa
**gli stessi 4 semi, lo stesso blob e lo stesso numero di passi** del primo
*(`pilota-prova1-bis`)*. **Se il salvataggio è davvero pure-read, i `misura.json` devono coincidere
campo per campo** — ed è **`V1` provato su 4 semi e 120 passi**, non su un giro corto.

> ### ⚠ **E I DUE SEMI NON SONO UGUALI COME PROVA.**
> **`--ogni 2` è stato passato SOLO al primo seme**, quindi:
> * **seme `11`** esercita **`salva_fotogramma`**, che chiama **`pozzo_grafo`** *(con snapshot e
>   restore dei due contatori)* e legge `self.psi` — **è il test FORTE**;
> * **semi `12`, `13`, `14`** esercitano **solo `salva_stato`**, che copia array — **test debole**.
> **Citare «4 semi» senza questa distinzione direbbe più di quanto la prova vale.**

**I campi di METADATO sono ATTESI diversi** *(`salvataggio`, `ogni`, `blob_sim`, i percorsi degli
`.npz`)*: sono **nati col salvataggio**, e confonderli con la fisica sarebbe l'errore.

    python csv/_test_fork/_v1_ripetizione.py

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

_presidio.avvia(__file__)

# ESENTE-H-P5: confronta due `misura.json` gia' prodotti, ciascuno da un run che ha dichiarato la
#   propria configurazione intera nel proprio referto. Non carica il simulatore.

NL = chr(10)
VECCHIO = "c4517a9"          # il commit che porta i `misura.json` del PRIMO pilota
SEMI = [11, 12, 13, 14]
META = {"salvataggio", "ogni", "blob_sim", "stati", "frames"}
R = []


def P(s=""):
    print(s)
    R.append(s)


def da_git(commit, percorso):
    q = subprocess.run(["git", "show", "%s:%s" % (commit, percorso)], cwd=RADICE,
                       capture_output=True)
    if q.returncode:
        return None
    return json.loads(q.stdout.decode("utf-8"))


def confronta(a, b, dove=""):
    """Le differenze fra due strutture annidate. Restituisce `[(percorso, va, vb), ...]`."""
    fuori = []
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            if dove == "" and k in META:
                continue
            if k not in a or k not in b:
                fuori.append(("%s/%s" % (dove, k), "ASSENTE" if k not in a else "presente",
                              "ASSENTE" if k not in b else "presente"))
                continue
            fuori += confronta(a[k], b[k], "%s/%s" % (dove, k))
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            fuori.append((dove + "/len", len(a), len(b)))
        else:
            for q, (x, y) in enumerate(zip(a, b)):
                fuori += confronta(x, y, "%s[%d]" % (dove, q))
    else:
        if isinstance(a, float) and isinstance(b, float):
            if not (a == b or (np.isnan(a) and np.isnan(b))):
                fuori.append((dove, a, b))
        elif a != b:
            fuori.append((dove, a, b))
    return fuori


def principale():
    P("=" * 108)
    P("`V1` GRATIS -- il salvataggio ha toccato la FISICA?")
    P("=" * 108)
    P("  primo pilota  : i `misura.json` al commit %s" % VECCHIO)
    P("  secondo run   : i `misura.json` sul disco (con `--salva-stati --ogni 2`)")
    P("  Il blob del simulatore e' LO STESSO nei due run: `e203f9a8` (byte grezzi) /")
    P("  `c968d4d8` (git), dal registro dei run. Quindi il confronto VALE.")
    P()
    P("  ⚠ E I SEMI NON VALGONO UGUALE: `--ogni 2` e' andato SOLO al seme 11, che quindi esercita")
    P("    `salva_fotogramma` -> `pozzo_grafo` (il test FORTE). Gli altri tre esercitano solo")
    P("    `salva_stato`, che copia array (test DEBOLE).")
    P()
    P("  seme | forza del test          | campi diversi | esito")
    tot = 0
    for s in SEMI:
        rel = "csv/_test_fork/_pilota_prova1/seme_%d/misura.json" % s
        a = da_git(VECCHIO, rel)
        p = os.path.join(RADICE, rel)
        b = json.load(io.open(p, encoding="utf-8")) if os.path.exists(p) else None
        if a is None or b is None:
            P("  %4d | -                       | -             | ** manca un file **" % s)
            tot += 1
            continue
        diff = confronta(a, b)
        tot += len(diff)
        forza = "FORTE (pozzo_grafo)" if s == SEMI[0] else "debole (solo salva_stato)"
        P("  %4d | %-23s | %13d | %s"
          % (s, forza, len(diff), "IDENTICI" if not diff else "** DIVERSI **"))
        for d in diff[:8]:
            P("       %s :  %r  contro  %r" % d)
        if len(diff) > 8:
            P("       ... e altri %d" % (len(diff) - 8))
    P()
    if tot == 0:
        P("  ✅ **`V1` E' PROVATO: ZERO campi diversi su 4 semi e 120 passi.**")
        P("  Il salvataggio degli stati e dei fotogrammi NON tocca la fisica, e la prova non e' un")
        P("  giro corto: e' il run intero, ripetuto.")
        P("  ⚠ Con la distinzione detta sopra: il seme 11 prova anche `pozzo_grafo` con lo")
        P("    snapshot/restore dei contatori; gli altri tre provano il solo `salva_stato`.")
    else:
        P("  ** MI FERMO: %d campi DIVERSI. **" % tot)
        P("  Il salvataggio AVREBBE TOCCATO LA FISICA, e allora gli stati e il video vanno")
        P("  RIVISTI: non descriverebbero il sistema che il primo pilota ha misurato.")
    P("=" * 108)
    return tot == 0


if __name__ == "__main__":
    ok = principale()
    io.open(os.path.join(_QUI, "_pilota_prova1", "V1_ripetizione.txt"), "w",
            encoding="utf-8", newline=NL).write(NL.join(R) + NL)
    raise SystemExit(0 if ok else 1)
