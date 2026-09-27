# -*- coding: utf-8 -*-
"""Porta le (A) e le (B) del censimento nell'indice, GENERANDO le righe (`L-NUMERI`).

**Non si ricopia a mano:** si legge `doc/CENSIMENTO_intenzioni.md` e si estraggono i campi.
Gli ID sono `CENS-A<n>` / `CENS-B<n>`, con `alias` **namespacizzato** `CENSIMENTO:A<n>` —
le etichette locali del censimento **non si riscrivono** (sono reperti).
"""
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
RAD = r"C:\Users\lpeano\soliton_simulator"
TAB, NL = chr(9), chr(10)
C = io.open(os.path.join(RAD, "doc", "CENSIMENTO_intenzioni.md"), encoding="utf-8").read()


def pulisci(s):
    """Un campo TSV: niente tab, niente a capo, niente `|` di tabella agli estremi."""
    s = s.replace(TAB, " ").replace(NL, " ").strip()
    s = re.sub(r"\s+", " ", s)
    return s.strip("| ").strip()


# ------------------------------------------------------------------ (A): sezioni
VOCI = []
for m in re.finditer(r"^## `(A\d+)` -- (.+?)$", C, re.M):
    sig, tit = m.group(1), m.group(2)
    fine = C.find(NL + "## ", m.end())
    fine = fine if fine > 0 else C.find(NL + "# ", m.end())
    corpo = C[m.end():fine if fine > 0 else len(C)]
    campi = {}
    for k in ("dove", "data di nascita", "cosa promette", "prova", "attiva nel driver"):
        mm = re.search(r"\| \*\*%s\*\* \| (.+?) \|\s*$" % re.escape(k), corpo, re.M)
        campi[k] = pulisci(mm.group(1)) if mm else "(non estratto)"
    VOCI.append(("A", sig, pulisci(tit), campi))

# ------------------------------------------------------------------ (B): una tabella sola
i0 = C.index("# (B) COSTRUITA E MAI MISURATA")
i1 = C.index("# (C) MISURATA")
for riga in C[i0:i1].split(NL):
    mm = re.match(r"\| \*\*`(B\d+)`\*\* \| (.*?) \| (.*?) \| (.*?) \| (.*?) \| (.*?) \|\s*$", riga)
    if not mm:
        continue
    sig = mm.group(1)
    campi = {"dove": pulisci(mm.group(2)), "data di nascita": pulisci(mm.group(3)),
             "cosa promette": pulisci(mm.group(4)), "prova": pulisci(mm.group(5)),
             "attiva nel driver": pulisci(mm.group(6))}
    tit = campi["cosa promette"][:70]
    VOCI.append(("B", sig, tit, campi))

print("estratte: %d (A) + %d (B) = %d"
      % (sum(1 for v in VOCI if v[0] == "A"), sum(1 for v in VOCI if v[0] == "B"), len(VOCI)))

# ------------------------------------------------------------------ le righe d'indice
P = os.path.join(RAD, "doc", "INDICE_ID.tsv")
t = io.open(P, encoding="utf-8").read()
nuove = 0
for classe, sig, tit, campi in VOCI:
    idx = "CENS-%s" % sig
    if (NL + idx + TAB) in t:
        print("  gia':", idx)
        continue
    nascita = campi["data di nascita"]
    breve = ("[%s] %s" % (classe, tit))[:100]
    lungo = ("titolo_breve INTERO: [classe %s del censimento] %s" % (classe, tit))
    nota = ("DAL CENSIMENTO DELLE INTENZIONI (doc/CENSIMENTO_intenzioni.md, commit b109f29), "
            "classe (%s) = %s. "
            "DOVE: %s. "
            "DATA DI NASCITA: %s. "
            "COSA PROMETTE: %s. "
            "PROVA: %s. "
            "ATTIVA NEL DRIVER: %s. "
            "⚠ LA DATA E' LA PRIMA APPARIZIONE DELLA STRINGA, non dell'intenzione; e 670310f "
            "(2026-08-28) e' il commit che importa il simulatore INTERO, quindi quella data "
            "significa <<c'era dal primo blob>> e l'eta' reale puo' essere MAGGIORE. "
            "⚠ blocca_run_base e' DA-DECIDERE: l'ordine delle cure lo approva Luca, e una "
            "decisione senza prova non passa il validatore. "
            "⚠ E PER LA DECISIONE (3) DI LUCA: cio' che oggi e' ATTIVO RESTA ATTIVO -- la cura e' "
            "DICHIARARLO e renderlo strutturale (commento vero, flag coerente, voce d'indice), "
            "NON spegnerlo."
            % (classe,
               "dichiarata e FALSA nel codice" if classe == "A" else "costruita e mai misurata",
               campi["dove"], nascita, campi["cosa promette"], campi["prova"],
               campi["attiva nel driver"]))
    riga = TAB.join([idx, "CENSIMENTO:%s" % sig, breve,
                     "doc/CENSIMENTO_intenzioni.md", "aperto", "DA-DECIDERE",
                     "difetto" if classe == "A" else "sospetto", "?",
                     lungo, "IN CODA", "", "", nota])
    if not t.endswith(NL):
        t += NL
    t += riga + NL
    nuove += 1
io.open(P, "w", encoding="utf-8", newline=NL).write(t)
print("righe aggiunte all'indice: %d" % nuove)
