# -*- coding: utf-8 -*-
"""**`RELAZIONE_PER_CLAUDE.md` -> UN FILE PER GIORNO in `doc/relazioni/`**
*(mandato di Luca 2026-09-26, punto `g`)*.

**Perche' non e' estetica:** la relazione e' il file che una sessione nuova legge **per primo**,
e a **20436 righe non la legge nessuno per intero** -- quindi il suo scopo e' **gia' perso**.
Il file vivo tiene **solo il giorno corrente**; i giorni chiusi stanno in
`doc/relazioni/<AAAA-MM-GG>.md`, e `git log` resta l'indice.

**LA REGOLA DI TAGLIO, dichiarata perche' il taglio e' un GIUDIZIO e non una misura:**

* si taglia su **ogni intestazione (`#` o `##`) che CONTIENE una data** `20\\d\\d-\\d\\d-\\d\\d`;
* il pezzo che segue appartiene a **quella** data, **fino al taglio successivo**;
* cio' che precede il **primo** taglio e' il **preambolo** e resta nel file vivo, perche' dice
  **come si legge** la relazione, non che cosa e' successo un giorno;
* **una riga non si riscrive e non si perde:** un controllo confronta le righe in ingresso con
  la somma di quelle in uscita, e lo script **si ferma** se non torna.

    python csv/_archivio_relazioni.py            # scrive l'archivio e asciuga il file vivo
    python csv/_archivio_relazioni.py --verifica # misura e basta, non tocca niente

ASCII puro.
"""
import io
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Divide un documento per giorno.

NL = chr(10)
_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, ".."))
VIVO = os.path.join(RADICE, "RELAZIONE_PER_CLAUDE.md")
ARCHIVIO = os.path.join(RADICE, "doc", "relazioni")
DATA = re.compile(r"20\d\d-\d\d-\d\d")
OGGI = "2026-09-26"


def dividi(testo):
    """[(giorno|None, righe)] -- il primo elemento e' il preambolo, con giorno `None`."""
    righe = testo.split(NL)
    tagli = []
    for i, r in enumerate(righe):
        if r.startswith("# ") or r.startswith("## "):
            m = DATA.search(r)
            if m:
                tagli.append((i, m.group(0)))
    pezzi = []
    if not tagli or tagli[0][0] > 0:
        pezzi.append((None, righe[:tagli[0][0] if tagli else len(righe)]))
    for k, (i, g) in enumerate(tagli):
        j = tagli[k + 1][0] if k + 1 < len(tagli) else len(righe)
        pezzi.append((g, righe[i:j]))
    return pezzi


def per_giorno(pezzi):
    d = {}
    for g, righe in pezzi:
        if g is None:
            continue
        d.setdefault(g, []).extend(righe)
    return d


def testa_viva(preambolo, giorni, oggi):
    """Il file vivo: il preambolo + SOLO il giorno corrente + l'indice dell'archivio."""
    fuori = list(preambolo)
    while fuori and not fuori[-1].strip():
        fuori.pop()
    fuori += ["", "---", "",
              "## L'ARCHIVIO PER GIORNO - **il file vivo tiene SOLO %s**" % oggi, "",
              "> **Regola di Luca, 2026-09-26.** A 20436 righe questo file non lo leggeva "
              "nessuno per intero, **quindi il suo scopo era gia' perso**. I giorni chiusi "
              "stanno in `doc/relazioni/`, uno per giorno, e `git log` resta l'indice.",
              "> *(Diviso da `csv/_archivio_relazioni.py`, che dichiara la regola di taglio.)*",
              "", "| giorno | righe | file |", "|---|--:|---|"]
    for g in sorted(giorni):
        if g == oggi:
            continue
        fuori.append("| `%s` | %d | [`doc/relazioni/%s.md`](doc/relazioni/%s.md) |"
                     % (g, len(giorni[g]), g, g))
    fuori += ["", "---", ""]
    fuori += giorni.get(oggi, ["*(nessuna voce ancora per oggi)*"])
    return NL.join(fuori).rstrip(NL) + NL


if __name__ == "__main__":
    solo = "--verifica" in sys.argv[1:]
    testo = io.open(VIVO, encoding="utf-8").read()
    pezzi = dividi(testo)
    preambolo = pezzi[0][1] if pezzi and pezzi[0][0] is None else []
    giorni = per_giorno(pezzi)
    n_in = len(testo.split(NL))          # elementi del taglio: la somma delle uscite conta cosi'
    n_out = len(preambolo) + sum(len(v) for v in giorni.values())
    print("=" * 92)
    print("RELAZIONE_PER_CLAUDE.md -> doc/relazioni/<giorno>.md")
    print("=" * 92)
    print("  righe in ingresso .............. %d" % n_in)
    print("  righe di preambolo (restano) ... %d" % len(preambolo))
    print("  giorni riconosciuti ............ %d" % len(giorni))
    for g in sorted(giorni):
        print("      %s  %6d righe%s" % (g, len(giorni[g]),
                                         "   <- OGGI, resta nel file vivo" if g == OGGI else ""))
    print("  righe in uscita (somma) ........ %d" % n_out)
    if n_in != n_out:
        print("  ** NON TORNA: %d righe di differenza **" % (n_in - n_out))
        sys.exit(1)
    if solo:
        sys.exit(0)
    if not os.path.isdir(ARCHIVIO):
        os.makedirs(ARCHIVIO)
    for g in sorted(giorni):
        if g == OGGI:
            continue
        cap = ["# RELAZIONE - **%s**" % g, "",
               "> *(Archivio: staccato da `RELAZIONE_PER_CLAUDE.md` il 2026-09-26 da "
               "`csv/_archivio_relazioni.py`. **Verbatim**, nessuna riga riscritta.)*", ""]
        io.open(os.path.join(ARCHIVIO, "%s.md" % g), "w", encoding="utf-8",
                newline=NL).write(NL.join(cap + giorni[g]).rstrip(NL) + NL)
    nuovo = testa_viva(preambolo, giorni, OGGI)
    io.open(VIVO, "w", encoding="utf-8", newline=NL).write(nuovo)
    print("  SCRITTI %d file in doc/relazioni/" % (len(giorni) - (1 if OGGI in giorni else 0)))
    print("  RELAZIONE_PER_CLAUDE.md ora e' %d righe" % nuovo.count(NL))
    sys.exit(0)
