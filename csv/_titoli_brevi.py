# -*- coding: utf-8 -*-
"""**`titolo_breve` DIVENTA BREVE DAVVERO** *(mandato di Luca, 2026-09-27, `INDICE-LEGGERO`)*.

Due regole, che il validatore imporra' da qui in avanti:

1. **`titolo_breve <= 100` caratteri.** Chi sfora si **accorcia**, e **la frase completa resta in
   `stato_da`** *(colonna quasi vuota: `6` righe su `771` prima di questo giro)*.
2. **nessun `titolo_breve` IDENTICO su ID diversi.** Chi collide prende `[<id>]` in coda.

**MISURATO PRIMA, e i numeri sono grossi:** `330` titoli oltre i 100 caratteri *(max `141`)* e
`34` gruppi di titoli identici -- di cui uno da **91 voci**.

> ### ⚠ **I DUPLICATI NON SONO COLLISIONI VERE, E VA DETTO.**
> I gruppi grandi sono **testi SEGNAPOSTO dell'importazione** -- *«(CITATO n volte, MAI definito in
> un registro)»* -- cioe' ID **citati e mai definiti**. **Non e' che due voci diverse portino lo
> stesso nome: e' che 91 voci non hanno ancora un nome.** La regola serve **da qui in avanti**: da
> oggi una collisione VERA non entra. **Accorciare non le definisce**, e restano da definire.

**IL DELTA E' ASSERITO COL DIFF:** `id`, `stato`, `blocca_run_base` e `famiglia` **non cambiano su
nessuna riga**, e lo script si ferma se cambiano. **Cambiano solo `titolo_breve` e `stato_da`.**

    python csv/_titoli_brevi.py --prova
    python csv/_titoli_brevi.py

ASCII puro.
"""
import io
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Accorcia titoli in un TSV.

NL = chr(10)
TAB = chr(9)
_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, ".."))
FONTE = os.path.join(RADICE, "doc", "INDICE_ID.tsv")
LIMITE = 100
INTOCCABILI = {0: "id", 4: "stato", 5: "blocca_run_base", 7: "famiglia"}


def accorcia(s, limite=LIMITE):
    """Taglia a `limite` **su un confine di parola**, e mette `...` a segnalarlo."""
    if len(s) <= limite:
        return s
    taglio = s[:limite - 3]
    sp = taglio.rfind(" ")
    if sp > limite // 2:
        taglio = taglio[:sp]
    return taglio.rstrip(" ,;:-") + "..."


def lavora(righe):
    """`(righe_nuove, quanti_accorciati, quanti_deduplicati)`. `righe` sono le righe di corpo."""
    celle = [r.split(TAB) for r in righe]
    for c in celle:
        while len(c) < 13:
            c.append("")
    n_acc = 0
    for c in celle:
        if len(c[2]) > LIMITE:
            intero = c[2]
            c[2] = accorcia(intero)
            # la frase COMPLETA va in `stato_da`, come ha chiesto Luca. Se c'e' gia' qualcosa,
            #   si accoda: non si sovrascrive cio' che un'altra mano ha scritto.
            c[8] = (c[8] + "  ") if c[8].strip() else ""
            c[8] += "titolo_breve INTERO: " + intero
            n_acc += 1
    # de-duplicazione: DOPO l'accorciamento, che puo' crearne di nuovi
    visti = {}
    n_dup = 0
    for c in celle:
        k = c[2]
        if k in visti:
            coda = " [" + c[0] + "]"
            base = accorcia(c[2], LIMITE - len(coda))
            c[2] = base + coda
            n_dup += 1
        visti.setdefault(c[2], c[0])
    return [TAB.join(c) for c in celle], n_acc, n_dup


def delta(prima, dopo):
    """Le colonne INTOCCABILI non cambiano su nessuna riga. Restituisce l'elenco delle violazioni."""
    fuori = []
    if len(prima) != len(dopo):
        return [("(conteggio)", "righe", len(prima), len(dopo))]
    for a, b in zip(prima, dopo):
        ca, cb = a.split(TAB), b.split(TAB)
        for k, nome in sorted(INTOCCABILI.items()):
            va = ca[k] if k < len(ca) else ""
            vb = cb[k] if k < len(cb) else ""
            if va != vb:
                fuori.append((ca[0], nome, va, vb))
    return fuori


if __name__ == "__main__":
    scrivi = "--prova" not in sys.argv[1:]
    testo = io.open(FONTE, encoding="utf-8", newline="").read()
    r = testo.split(NL)
    intest, corpo = r[0], [x for x in r[1:] if x.strip()]
    nuove, n_acc, n_dup = lavora(corpo)
    viol = delta(corpo, nuove)
    lung = [len(x.split(TAB)[2]) for x in nuove]
    from collections import Counter
    dupdopo = [k for k, v in Counter(x.split(TAB)[2] for x in nuove).items() if v > 1]
    print("=" * 92)
    print("`titolo_breve`: <= %d caratteri, e nessuno IDENTICO%s"
          % (LIMITE, "" if scrivi else "   (PROVA: non scrivo)"))
    print("=" * 92)
    print("  voci ............................... %d" % len(corpo))
    print("  titoli ACCORCIATI (>%d car.) ...... %d" % (LIMITE, n_acc))
    print("  titoli DE-DUPLICATI ................ %d" % n_dup)
    print("  lunghezza massima DOPO ............. %d" % (max(lung) if lung else 0))
    print("  duplicati DOPO ..................... %d" % len(dupdopo))
    print("  DELTA sulle colonne intoccabili (%s): %d violazioni"
          % (", ".join(INTOCCABILI.values()), len(viol)))
    for x in viol[:6]:
        print("      ** %s: %s  %r -> %r" % x)
    if viol or (max(lung) if lung else 0) > LIMITE or dupdopo:
        sys.exit(1)
    if scrivi:
        io.open(FONTE, "w", encoding="utf-8", newline=NL).write(NL.join([intest] + nuove) + NL)
        print("  SCRITTO doc/INDICE_ID.tsv")
    sys.exit(0)
