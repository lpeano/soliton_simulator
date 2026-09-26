# -*- coding: utf-8 -*-
"""**I CONTROLLI DI FINE DEL RIORDINO DELLE REGOLE** *(mandato di Luca 2026-09-26, punto 2)*.

Cinque controlli, **tutti misurati, nessuno asserito**:

| | controllo | criterio |
|---|---|---|
| **C1** | ognuna delle **76 regole** dell'inventario si **ritrova** nel file di destinazione *(testo o rimando)*, oppure e' **TOLTA col motivo scritto** | nessuna persa |
| **C2** | il **posto 2** *(`doc/PATTERN_DI_PROVA.md`)* | **<= 10 regole** |
| **C3** | `CLAUDE.md` | **<= 400 righe**, e le **righe lette all'avvio MISURATE** prima e dopo |
| **C4** | i **collaudi** dei hook e del validatore | **ripassano tutti** |
| **C5** | ogni **`P`** e **`STANDARD`** citato da un hook | **esiste ancora col nome giusto** |

**L'inventario NON si ricopia: si LEGGE da `doc/REGOLE_proposta.md`**, che e' il documento
approvato da Luca -- cosi' il controllo non puo' mentire su quante regole c'erano (`L-NUMERI`).

    python csv/_controlli_riordino.py

ASCII puro.
"""
import io
import os
import re
import subprocess
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Conta righe e cerca stringhe.

NL = chr(10)
TAB = chr(9)
_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, ".."))
TAG = "regole-pre-riordino"
PROPOSTA = os.path.join(RADICE, "doc", "REGOLE_proposta.md")
RIMANDO = "doc/STORIA_REGOLE.md"          # la tavola che dice dove vive OGGI ogni sezione

DESTINAZIONI = {
    "1": ["doc/ASSIOMI.md", "doc/PATTERN_DI_PROVA.md"],
    "2": ["doc/PATTERN_DI_PROVA.md"],
    "3": ["csv/_hook_presidi.py", "csv/_hook_relazione.py", "csv/_hook_fisica.py",
          "csv/_presidio_indice.py", "csv/_presidio_commenti_flag.py",
          "csv/_presidio_righe.py", "csv/_indice_id.py",
          ".githooks/pre-commit", ".githooks/commit-msg", "CLAUDE.md"],
    "4": ["CLAUDE.md"],
    "5": ["doc/STATO_RUN.md", "doc/INDICE_ID.tsv", "doc/REGISTRO_FISICA.md",
          "doc/COMPONENTI_PROMOSSE.md", "doc/FATTI_dal_codice.md", "CLAUDE.md"],
    "X": ["doc/PATTERN_DI_PROVA.md", "doc/ASSIOMI.md", "CLAUDE.md"],   # le regole che ESCONO
}

# l'elenco dei documenti letti all'avvio, PRIMA (par.0-bis di allora) e DOPO (par.0 di oggi)
AVVIO_PRIMA = ["CLAUDE.md", "doc/ASSIOMI.md", "doc/PATTERN_DI_PROVA.md",
               "doc/BUSSOLA_dev-spinoriale.md", "doc/BUSSOLA_TECNICA_dev-spinoriale.md",
               "doc/ROADMAP_fork_SU2.md", "doc/PROTOCOLLO_test_olonomia.md",
               "doc/SYSTASIS_nota_concettuale.md"]
AVVIO_DOPO = ["CLAUDE.md", "doc/ASSIOMI.md", "doc/PATTERN_DI_PROVA.md"]

COLLAUDI = [
    ("presidi dei hook", ["csv/_hook_presidi.py", "--collaudo"]),
    ("H-RIGHE (CLAUDE.md <= 400)", ["csv/_presidio_righe.py", "--collaudo"]),
    ("validatore dell'indice", ["csv/_indice_id.py", "--collaudo"]),
    ("presidio dell'indice", ["csv/_presidio_indice.py", "--collaudo"]),
    ("istruzioni dell'indice", ["csv/_collaudo_istruzioni.py"]),
    ("migrazione dei fatti", ["csv/_riordino_fatti.py", "--verifica"]),
    ("archivio della storia", ["csv/_riordino_storia.py", "--verifica"]),
    ("archivio delle relazioni", ["csv/_archivio_relazioni.py", "--verifica"]),
]

# i nomi che i hook citano: si estraggono dai SORGENTI, non si ricopiano
CITAZIONE = re.compile(r"(?:H-[A-Z][A-Za-z0-9-]*|STANDARD\s+\d+|P\d+(?:-[a-z]+)*)")
SORGENTI_HOOK = ["csv/_hook_presidi.py", "csv/_hook_relazione.py", "csv/_hook_fisica.py",
                 "csv/_presidio_indice.py", "csv/_presidio_commenti_flag.py",
                 "csv/_presidio_righe.py", ".githooks/pre-commit", ".githooks/commit-msg"]


def testo(rel):
    try:
        return io.open(os.path.join(RADICE, rel), encoding="utf-8", errors="replace").read()
    except Exception:
        return ""


def righe(rel):
    t = testo(rel)
    return t.count(NL) + (1 if t and not t.endswith(NL) else 0)


def righe_al_tag(rel):
    q = subprocess.run(["git", "show", "%s:%s" % (TAG, rel)], cwd=RADICE, capture_output=True)
    if q.returncode:
        return 0
    t = q.stdout.decode("utf-8", "replace")
    return t.count(NL) + (1 if t and not t.endswith(NL) else 0)


# ⚠ LE EQUIVALENZE DICHIARATE: la proposta aveva proposto nomi SEMANTICI per i presidi dei hook
#   (`H-CLI`, `H-CONFIG`, ...); Luca ha approvato il prefisso `H-` scrivendo `H-P3`, `H-P5`, ...
#   cioe' **il nome di prima col prefisso**. Il nome della proposta non esiste piu': qui si
#   dichiara IN CHE COSA e' diventato, invece di far passare la regola per «persa».
EQUIVALENZE = {
    "H-CLI": "H-P3", "H-CONFIG": "H-P5", "H-COMMENTI": "H-P7", "H-ANCORA": "H-P8",
    "H-RELAZIONE": "H-P1-bis", "H-FISICA": "H-REG-R",
}
FINE_INVENTARIO = "## 🔒 TRE MECCANISMI"      # oltre questo titolo non c'e' piu' inventario


def inventario():
    """[(id, posto)] letto da `doc/REGOLE_proposta.md`. L'inventario NON si ricopia."""
    fuori, posto = [], None
    for r in testo(os.path.relpath(PROPOSTA, RADICE).replace(chr(92), "/")).split(NL):
        if r.startswith(FINE_INVENTARIO):
            break
        m = re.match(r"^### . POSTO \*\*(\d)\*\*", r)
        if m:
            posto = m.group(1)
            continue
        if "**ESCONO**" in r:
            posto = "X"
            continue
        m2 = re.match(r"^\| \*\*([^*]+)\*\* \|", r)
        if m2 and posto:
            fuori.append((m2.group(1).strip(), posto))
    return fuori


def c1():
    inv = inventario()
    trovate, perse = [], []
    for i, posto in inv:
        cerca = EQUIVALENZE.get(i, i)
        dove = None
        for rel in DESTINAZIONI[posto] + [RIMANDO]:
            if cerca in testo(rel):
                dove = rel + ("   (come `%s`)" % cerca if cerca != i else "")
                break
        (trovate if dove else perse).append((i, posto, dove))
    return inv, trovate, perse


def c2():
    t = testo("doc/PATTERN_DI_PROVA.md")
    dentro = t.split("## STANDARD")[-1].split("### Le regole che valgono qui")[0]
    n = len([r for r in dentro.split(NL) if re.match(r"^\| \*\*[^|]+\*\* \|", r)])
    return n


def c5():
    _c, corpo = None, []
    for k, r in enumerate(io.open(os.path.join(RADICE, "doc", "INDICE_ID.tsv"),
                                  encoding="utf-8", newline="").read().split(NL)):
        if k and r.strip():
            corpo.append(r)
    noti = set()
    for r in corpo:
        c = r.split(TAB)
        noti.add(c[0])
        if len(c) > 1 and c[1]:
            noti |= set(x for x in c[1].split(",") if x)
    # le forme DICHIARATE non-id contano come note: e' il meccanismo previsto dall'indice
    escl = set()
    for k, r in enumerate(io.open(os.path.join(RADICE, "doc", "INDICE_ID_ESCLUSI.tsv"),
                                  encoding="utf-8", newline="").read().split(NL)):
        if k and r.strip():
            escl.add(r.split(TAB)[0])
    citati, ignoti = set(), []
    for rel in SORGENTI_HOOK:
        for m in CITAZIONE.finditer(testo(rel)):
            citati.add(m.group(0))
    for x in sorted(citati):
        if x not in noti and x not in escl:
            ignoti.append(x)
    return sorted(citati), ignoti


if __name__ == "__main__":
    P = print
    P("=" * 96)
    P("CONTROLLI DI FINE DEL RIORDINO DELLE REGOLE   (2026-09-26)")
    P("=" * 96)
    esiti = []

    inv, trovate, perse = c1()
    P("")
    P("C1  LE %d REGOLE DELL'INVENTARIO" % len(inv))
    per_posto = {}
    for i, p, d in trovate:
        per_posto.setdefault(p, 0)
        per_posto[p] += 1
    for p in sorted(per_posto):
        P("      posto %s: %2d ritrovate" % (p, per_posto[p]))
    P("      RITROVATE %d su %d      PERSE %d" % (len(trovate), len(inv), len(perse)))
    for i, p, _d in perse:
        P("        ** PERSA: %s (posto %s)" % (i, p))
    esiti.append(("C1  nessuna regola persa", not perse))

    n2 = c2()
    P("")
    P("C2  POSTO 2 -- doc/PATTERN_DI_PROVA.md")
    P("      regole nella tabella STANDARD ... %d   (tetto 10)" % n2)
    if n2 > 10:
        P("      ** IL TETTO NON E' RISPETTATO, ed e' DICHIARATO, non nascosto.**")
        P("      La proposta annunciava 10 e ne dava 12: quel numero era sbagliato in")
        P("      aritmetica. Con le modifiche di Luca (`P4` resta sola, `L-SOGLIA` va in")
        P("      `P1-sexies`) il conto misurato e' 11, e `par.2` non e' una riga ma la")
        P("      LISTA DI CONTROLLO. L'undicesima da fondere NON l'ho scelta io: la")
        P("      fusione che Luca ha rifiutato era una di queste. Le tre candidate, con")
        P("      quello che si perderebbe, sono in fondo a doc/PATTERN_DI_PROVA.md.")
    esiti.append(("C2  posto 2 <= 10", n2 <= 10))

    n_cl = righe("CLAUDE.md")
    n_cl_prima = righe_al_tag("CLAUDE.md")
    P("")
    P("C3  CLAUDE.md E LE RIGHE LETTE ALL'AVVIO")
    P("      CLAUDE.md  PRIMA %5d  ->  DOPO %5d   (tetto 400)" % (n_cl_prima, n_cl))
    a_prima = sum(righe_al_tag(x) for x in AVVIO_PRIMA)
    a_dopo = sum(righe(x) for x in AVVIO_DOPO)
    P("      righe lette all'avvio, MISURATE:")
    for x in AVVIO_PRIMA:
        P("          PRIMA  %-46s %5d" % (x, righe_al_tag(x)))
    P("          PRIMA  %-46s %5d" % ("TOTALE (8 documenti)", a_prima))
    for x in AVVIO_DOPO:
        P("          DOPO   %-46s %5d" % (x, righe(x)))
    P("          DOPO   %-46s %5d" % ("TOTALE (3 documenti)", a_dopo))
    P("      riduzione: %d righe, cioe' il %.0f %%" % (a_prima - a_dopo,
                                                      100.0 * (a_prima - a_dopo) / max(a_prima, 1)))
    esiti.append(("C3  CLAUDE.md <= 400 righe", n_cl <= 400))

    P("")
    P("C4  I COLLAUDI")
    tutti = True
    for nome, cmd in COLLAUDI:
        q = subprocess.run([sys.executable] + [os.path.join(RADICE, cmd[0])] + cmd[1:],
                           cwd=RADICE, capture_output=True, text=True, encoding="utf-8",
                           errors="replace")
        ok = (q.returncode == 0)
        tutti = tutti and ok
        P("      %-34s %s" % (nome, "PASS" if ok else "** FAIL **"))
    esiti.append(("C4  tutti i collaudi passano", tutti))

    citati, ignoti = c5()
    P("")
    P("C5  I NOMI CITATI DAI HOOK")
    P("      nomi distinti citati ............ %d" % len(citati))
    P("      %s" % ", ".join(citati))
    P("      NON presenti nell'indice ........ %d %s"
      % (len(ignoti), ", ".join(ignoti) if ignoti else ""))
    esiti.append(("C5  ogni nome citato esiste nell'indice", not ignoti))

    P("")
    P("=" * 96)
    for nome, ok in esiti:
        P("  %-44s %s" % (nome, "PASS" if ok else "** FAIL **"))
    buoni = len([1 for _n, o in esiti if o])
    P("ESITO: %d/%d" % (buoni, len(esiti)))
    P("=" * 96)
    sys.exit(0 if buoni == len(esiti) else 1)
