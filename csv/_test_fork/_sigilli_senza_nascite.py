# -*- coding: utf-8 -*-
"""**QUALI SIGILLI PASSATI NON COPRONO LE NASCITE** *(punto ② del rilievo del guardiano, 2026-09-28)*

**Il rilievo:** `csv/_test_fork/_hashseed_prova.py` impone `sep = 3.0` e `nmasse = 2` **a mano**,
mentre il dump registra `_argv` col `--sep 6.1158` del driver. Quindi **tutti i sigilli che dicono
«scena `(ii)(a)`, argv del driver» sono girati sulla scena PICCOLA** -- `2107` nodi, e
### **ZERO nascite in 40 passi**. **Per quelli la byte-identita' NON copre le nascite.**

**COME LO DERIVA, e il criterio e' dichiarato:** per ogni commit che ha toccato
`soliton_simulator.py`, guarda se le righe **aggiunte o togliute** cadono nella **regione delle
NASCITE** -- riconosciuta da marcatori che esistono **solo** li':

| marcatore | perche' e' della regione delle nascite |
|---|---|
| `concatenate([self.` · `vstack([self.` | **estensioni**: esistono solo quando qualcosa nasce |
| `COPPIA_MIT` · `coppie_nate` · `anti` | il **canale di Schwinger** |
| `pos_figlio` · `d0new` · `perc_tw` | la **mitosi dopo il `return 0`** |
| `_g_nati_` | i **contatori delle nascite** |

### ⚠ IL LIMITE, DICHIARATO (`A9`): e' un criterio **PER TESTO**, non per raggiungibilita'. Un
commit puo' comparire perche' ha toccato un `concatenate` **fuori** dalla mitosi, e uno puo'
**mancare** se ha cambiato la regione senza toccare nessuno dei marcatori. ### **E' UN ELENCO DA
LEGGERE, non un verdetto.**

COMANDO:  python csv/_test_fork/_sigilli_senza_nascite.py [--da <commit>]
USCITA:   0 sempre: e' un elenco.
"""
import io
import json
import os
import subprocess
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, os.path.join(RADICE, "csv"))
import _presidio  # noqa: E402

_presidio.avvia(__file__)

MARCATORI = ("concatenate([self.", "vstack([self.", "COPPIA_MIT", "coppie_nate",
             "pos_figlio", "d0new", "perc_tw", "_g_nati_")
NL = chr(10)


def _git(*a):
    p = subprocess.run(["git"] + list(a), cwd=RADICE, capture_output=True)
    return (p.stdout or b"").decode("utf-8", "replace")


def principale():
    da = None
    for k, x in enumerate(sys.argv[1:]):
        if x == "--da" and k + 2 <= len(sys.argv[1:]):
            da = sys.argv[1:][k + 1]
    campo = (da + "..HEAD") if da else "HEAD"
    righe = [r for r in _git("log", "--format=%H|%h|%ad|%s", "--date=short", campo,
                             "--", "soliton_simulator.py").split(NL) if r.strip()]
    print("commit che hanno toccato il simulatore: %d" % len(righe))
    print("")
    fuori = []
    for r in righe:
        h, corto, data, sogg = (r.split("|", 3) + ["", "", ""])[:4]
        d = _git("show", "--format=", "--unified=0", h, "--", "soliton_simulator.py")
        tocca = sorted({m for m in MARCATORI
                        for l in d.split(NL)
                        if l[:1] in "+-" and l[1:2] != l[:1] and m in l})
        if not tocca:
            continue
        # il SIGILLO: lo si cerca fra i file del commit e nel soggetto
        files = [x for x in _git("show", "--format=", "--name-only", h).split(NL)
                 if x.strip() and ("_seal" in x or "sig" in x.lower())]
        fuori.append({"commit": corto, "data": data, "soggetto": sogg[:88],
                      "marcatori": tocca, "file_di_sigillo": files[:4]})
    print("=" * 96)
    print("COMMIT CHE HANNO TOCCATO LA REGIONE DELLE NASCITE: %d" % len(fuori))
    print("=" * 96)
    print("")
    for v in fuori:
        print("  %-9s %-11s %s" % (v["commit"], v["data"], v["soggetto"]))
        print("      marcatori: %s" % ", ".join(v["marcatori"]))
        if v["file_di_sigillo"]:
            print("      sigilli nel commit: %s" % ", ".join(
                os.path.basename(x) for x in v["file_di_sigillo"]))
        print("")
    print("=" * 96)
    print("### PER QUESTI LA BYTE-IDENTITA' MISURATA SULLA SCENA PICCOLA NON COPRE LE NASCITE.")
    print("### Non vuol dire che siano sbagliati: vuol dire che il loro braccio di byte-identita'")
    print("### NON HA PERCORSO quei rami, e quindi NON DICE NIENTE su di essi.")
    print("=" * 96)
    OUT = os.path.join(_QUI, "_sigilli_senza_nascite.json")
    io.open(OUT, "w", encoding="utf-8", newline=NL).write(json.dumps(
        {"marcatori": list(MARCATORI), "commit_totali": len(righe),
         "commit_nella_regione": fuori}, indent=1, ensure_ascii=False, sort_keys=True))
    print("")
    print("scritto: " + OUT)
    return 0


if __name__ == "__main__":
    sys.exit(principale())
