# -*- coding: utf-8 -*-
r"""**I NOMI DEL RAMO DEL PUNTO MEDIO PER PEZZO, CONTATI** — *prima e dopo la rimozione.*

> ### ⛔ **PERCHE' ESISTE** *(`2026-10-19`)*: il mandato della rimozione *(decisione di Luca
> del `2026-10-18`, `21:48`)* dice ### **«rifai TU il censimento con uno script,
> documentazione compresa, e scrivi il numero che hai visto; se e' diverso, spiega la
> differenza»**. Il guardiano conta ### **`8` file e `37` righe** fuori da `doc/` e dalla
> relazione.

## ⭐ CHE COSA CONTA

### **Le righe che contengono almeno uno dei nomi** *(come parola intera)*, in ### **ogni
file tracciato da git** *(`git ls-files`)*, separate in ### **CODICE** *(fuori da `doc/` e
da `RELAZIONE_PER_CLAUDE.md`: il perimetro del guardiano)* e ### **DOCUMENTAZIONE**.
### ⚠ **Questo file e' escluso**, e lo dice: contiene la lista dei nomi.

## ⛔ IL MODO `--dopo`

### **A rimozione fatta, nel CODICE i nomi tolti devono essere `0`.** Restano ammessi:
`_misura_punto_medio` *(il file RESTA, col censimento dei `14` pezzi)*. ### **Se un nome
tolto resta nel codice, lo script ESCE con `1`.**

Gira con:  python csv/_censimento_ramo_punto_medio.py [--dopo]
"""
import io
import os
import re
import subprocess
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
QUESTO = "csv/_censimento_ramo_punto_medio.py"

# ### ⛔ **I NOMI DEL PERIMETRO DEL GUARDIANO**, dalla coda *(sezione della rimozione)*.
NOMI = ("regola_punto_medio", "hop_phi_punto_medio", "s_arco_da_lambda", "z_arco_da_s",
        "hop_phi_con_s", "giri_peso", "EPS_PUNTO_FISSO", "_misura_punto_medio")
# ### **Ammessi DOPO:** il file della misura resta, quindi il suo nome resta.
AMMESSI_DOPO = ("_misura_punto_medio",)
_RE = {n: re.compile(r"(?<![A-Za-z0-9_])" + re.escape(n) + r"(?![A-Za-z0-9_])") for n in NOMI}


def tracciati():
    out = subprocess.check_output(["git", "ls-files"], cwd=RADICE)
    return [x for x in out.decode("utf-8").splitlines() if x.strip()]


def e_codice(rel):
    return not (rel.startswith("doc/") or rel == "RELAZIONE_PER_CLAUDE.md")


def censisci():
    """### `{rel: [(riga, nomi)]}` per ogni file con almeno una riga."""
    fuori = {}
    for rel in tracciati():
        if rel == QUESTO:
            continue
        p = os.path.join(RADICE, rel)
        try:
            testo = io.open(p, encoding="utf-8").read()
        except (UnicodeDecodeError, OSError):
            continue
        righe = []
        for k, r in enumerate(testo.splitlines(), 1):
            nn = [n for n in NOMI if _RE[n].search(r)]
            if nn:
                righe.append((k, nn))
        if righe:
            fuori[rel] = righe
    return fuori


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    dopo = "--dopo" in argv
    c = censisci()
    cod = {r: v for r, v in c.items() if e_codice(r)}
    doc = {r: v for r, v in c.items() if not e_codice(r)}
    print("=" * 100)
    print("I NOMI DEL RAMO DEL PUNTO MEDIO PER PEZZO, CONTATI -- %s la rimozione"
          % ("DOPO" if dopo else "PRIMA"))
    print("=" * 100)
    print("  i nomi: %s" % ", ".join(NOMI))
    print("  le righe che contengono almeno un nome (parola intera), nei file tracciati da"
          " git; escluso questo file")
    for titolo, gruppo in (("CODICE (fuori da doc/ e dalla relazione)", cod),
                           ("DOCUMENTAZIONE (doc/ e la relazione)", doc)):
        print("-" * 100)
        print("### %s: %d file, %d righe" % (titolo, len(gruppo),
                                             sum(len(v) for v in gruppo.values())))
        for rel in sorted(gruppo):
            per_nome = {}
            for _k, nn in gruppo[rel]:
                for n in nn:
                    per_nome[n] = per_nome.get(n, 0) + 1
            print("     %-52s %3d   %s" % (rel, len(gruppo[rel]),
                                           "  ".join("%s:%d" % x
                                                     for x in sorted(per_nome.items()))))
    ok = True
    if dopo:
        rimasti = [(rel, k, nn) for rel, v in cod.items() for (k, nn) in v
                   if any(n not in AMMESSI_DOPO for n in nn)]
        print("-" * 100)
        print("### DOPO: righe di CODICE con un nome TOLTO (ammesso solo %s): %d"
              % (", ".join(AMMESSI_DOPO), len(rimasti)))
        for rel, k, nn in rimasti:
            print("     %s:%d  %s" % (rel, k, ", ".join(nn)))
        ok = not rimasti
        print("     %s" % ("PASSA" if ok else "### FALLISCE"))
    print("=" * 100)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
