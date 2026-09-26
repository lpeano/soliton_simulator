# -*- coding: utf-8 -*-
"""**`par.9` DI `CLAUDE.md` -> `doc/FATTI_dal_codice.md`, ORDINATO PER FUNZIONE.**

*(Mandato di Luca del 2026-09-26, punto `e`. Lo spostamento e' **MECCANICO**: le righe si
tagliano e si riattaccano **verbatim**, e un controllo verifica che **ogni riga non vuota
dell'originale** sia presente nell'uscita. Il giudizio mio e' **solo** la destinazione di
ciascun punto, che sta in `DESTINAZIONE` -- una riga per punto, cosi' si corregge in un posto solo.)*

**I NUMERI DI RIGA DEL SIMULATORE SONO MISURATI DALL'AST**, non ricopiati: le righe citate nei
fatti sono di blob vecchi e **sono shiftate** (lo dice il primo punto di `par.9`). Qui ogni
intestazione porta la riga **di oggi**, e se una funzione non esiste piu' lo script **lo dice**.

    python csv/_riordino_fatti.py            # genera doc/FATTI_dal_codice.md
    python csv/_riordino_fatti.py --verifica # solo il controllo: nessuna riga persa

ASCII puro.
"""
import ast
import io
import os
import subprocess
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Sposta prosa fra due documenti.

NL = chr(10)
_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, ".."))
TAG = "regole-pre-riordino"          # la FONTE di `par.9`: il tag, non il disco
USCITA = os.path.join(RADICE, "doc", "FATTI_dal_codice.md")
SIM = os.path.join(RADICE, "soliton_simulator.py")

# la sezione `par.9` dentro `CLAUDE.md`, cercata PER TITOLO e non per riga (par.0)
TITOLO = "## 9. FATTI VERIFICATI DAL CODICE"
FINE = "## 9-bis."

# ------------------------------------------------------------------ LA DESTINAZIONE DI OGNI PUNTO
#   chiave = numero d'ordine del punto in `par.9` (1..53, contati dai punti di primo livello)
#   valore = il gruppo in cui finisce.  I gruppi che NON sono funzioni cominciano per chiocciola.
DESTINAZIONE = {
    1:  "@righe",                     # la tabella di conversione fra blob
    2:  "_coppia_interferenza",
    3:  "_cs_nodo",
    4:  "ritmo",
    5:  "_passo_spinoriale",
    6:  "mitosi",
    7:  "_bloch_ritardato",
    8:  "ritmo",
    9:  "@presidi",
    10: "@presidi",
    11: "@presidi",
    12: "@presidi",
    13: "_eredita_spinore_figli",
    14: "_passo_spinoriale",
    15: "_passo_spinoriale",
    16: "_passo_spinoriale",
    17: "_passo_spinoriale",
    18: "mitosi",
    19: "_passo_spinoriale",
    20: "_passo_spinoriale",
    21: "@presidi",
    22: "_passo_spinoriale",
    23: "_passo_spinoriale",
    24: "_passo_spinoriale",
    25: "_passo_spinoriale",
    26: "@presidi",
    27: "_tempo_luce_nodo",
    28: "@presidi",
    29: "@presidi",
    30: "@presidi",
    31: "@presidi",
    32: "_tempo_luce_nodo",
    33: "ritmo",
    34: "@presidi",
    35: "@presidi",
    36: "_bloch_ritardato",
    37: "_cs_nodo",
    38: "_tempo_luce_nodo",
    39: "@presidi",
    40: "@presidi",
    41: "salva_stato",
    42: "memoria_hebbiana_moto",
    43: "rapporto_guardie",
    44: "memoria_hebbiana_moto",
    45: "memoria_hebbiana_moto",
    46: "_passo_spinoriale",
    47: "_passo_spinoriale",
    48: "@presidi",
    49: "@presidi",
    50: "salva_stato",
    51: "salva_stato",
    52: "@fuori",
    53: "@presidi",
}

# una riga per gruppo: a che cosa serve quella funzione, per chi la apre la prima volta
CHE_COSA = {
    "_coppia_interferenza": "la forza fra due nodi: e' qui che il trasporto e' SCALARE, "
                            "quindi abeliano per struttura.",
    "_cs_nodo": "la velocita' delle onde metriche per nodo (`cs_floor`).",
    "ritmo": "l'orologio: `r`, `dt_n = DT*r`, e la doppia copertura a 4pi.",
    "_passo_spinoriale": "il passo dello spinore di nodo: `omega_s`, la coppia, l'inerzia, "
                         "il rilassamento, l'orologio de Broglie.",
    "mitosi": "la nascita di un nodo nuovo.",
    "_bloch_ritardato": "lo STRATO 1: il Bloch ritardato, `alpha = 1-exp(-dt_n/tau)`.",
    "_eredita_spinore_figli": "che cosa il figlio eredita dal padre alla nascita.",
    "_tempo_luce_nodo": "`tau = d/cs`, e la cache `_cs_nodo_prev` da cui dipende.",
    "salva_stato": "lo snapshot su disco, e l'archivio a serie.",
    "memoria_hebbiana_moto": "la memoria del moto: `scala_p`, `MEM_MOTO`, il filtro di portata.",
    "rapporto_guardie": "i contatori delle guardie: quante volte un ramo e' stato saltato.",
}

INTESTAZIONE_GRUPPO = {
    "@righe": ("LE RIGHE CITATE NEI FATTI SONO DI BLOB VECCHI",
               "Si cerca **per NOME di funzione o di flag, mai per riga**. La tabella qui "
               "sotto e' storica e si legge per sapere **a quale blob** un numero si riferiva."),
    "@presidi": ("I PRESIDI DI LETTURA nati da questi fatti",
                 "**Non sono fatti sul codice: sono modo di leggere una misura.** Stanno qui "
                 "perche' sono nati **da** questi fatti; la regola che li copre vive al "
                 "**posto 2** (`doc/PATTERN_DI_PROVA.md`) o fra gli **assiomi**."),
    "@fuori": ("FATTI CHE NON RIGUARDANO IL SIMULATORE", ""),
}


def _testo(_p):
    """`CLAUDE.md` **dal TAG**, non dal disco: il riordino ha tolto `par.9` dal disco, e uno
    strumento che leggesse il disco alla seconda esecuzione **non troverebbe piu' niente**.
    E' la stessa ragione di `csv/_riordino_storia.py`."""
    q = subprocess.run(["git", "show", "%s:CLAUDE.md" % TAG], cwd=RADICE, capture_output=True)
    if q.returncode:
        raise SystemExit("il tag %s non si legge: %s"
                         % (TAG, (q.stderr or b"").decode("utf-8", "replace")[:160]))
    return q.stdout.decode("utf-8")


def sezione_par9(testo):
    """Le righe di `par.9`, cercate per TITOLO. Restituisce (intestazione, corpo)."""
    righe = testo.split(NL)
    a = b = -1
    for i, r in enumerate(righe):
        if r.startswith(TITOLO):
            a = i
        elif a >= 0 and r.startswith(FINE):
            b = i
            break
    if a < 0 or b < 0:
        raise SystemExit("par.9 non trovata in CLAUDE.md (titolo o fine assenti)")
    corpo = righe[a + 1:b]
    while corpo and not corpo[-1].strip():
        corpo.pop()
    return righe[a], corpo


def punti(corpo):
    """Taglia il corpo nei punti di primo livello. Nessuna riga si perde: la somma torna."""
    tagli = [i for i, r in enumerate(corpo) if r.startswith("- ")]
    if not tagli or tagli[0] != 0:
        raise SystemExit("il corpo di par.9 non comincia con un punto di primo livello")
    fuori = []
    for k, i in enumerate(tagli):
        j = tagli[k + 1] if k + 1 < len(tagli) else len(corpo)
        fuori.append(corpo[i:j])
    return fuori


def righe_funzioni():
    """Mappa nome -> riga, misurata dall'AST del simulatore (la PRIMA definizione)."""
    arb = ast.parse(io.open(SIM, encoding="utf-8", errors="replace").read())
    dove = {}
    for nd in ast.walk(arb):
        if isinstance(nd, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if nd.name not in dove or nd.lineno < dove[nd.name]:
                dove[nd.name] = nd.lineno
    return dove


def costruisci():
    _intest, corpo = sezione_par9(_testo(TAG))
    blocchi = punti(corpo)
    if len(blocchi) != len(DESTINAZIONE):
        raise SystemExit("punti trovati %d, destinazioni %d: la mappa e' scaduta"
                         % (len(blocchi), len(DESTINAZIONE)))
    dove = righe_funzioni()
    manca = [g for g in set(DESTINAZIONE.values())
             if not g.startswith("@") and g not in dove]
    per_gruppo = {}
    for k, b in enumerate(blocchi, 1):
        per_gruppo.setdefault(DESTINAZIONE[k], []).append(b)

    # le funzioni in ordine di comparsa nel simulatore; i gruppi non-funzione in coda
    funzioni = sorted([g for g in per_gruppo if not g.startswith("@")],
                      key=lambda g: dove.get(g, 10 ** 9))
    ordine = ["@righe"] + funzioni + ["@presidi", "@fuori"]

    fuori = []
    fuori.append("# I FATTI VERIFICATI DAL CODICE - **ordinati per FUNZIONE del simulatore**")
    fuori.append("")
    fuori.append("> **Non sono regole: sono cio' che il codice FA oggi.** Erano `par.9` di "
                 "`CLAUDE.md`, e da li' vengono **verbatim**.")
    fuori.append("> **Si legge QUANDO SERVE, non all'avvio** - e la regola in `CLAUDE.md` e' "
                 "*«prima di toccare una funzione, leggi i suoi fatti qui»*.")
    fuori.append(">")
    fuori.append("> *(Generato da `csv/_riordino_fatti.py`. Le righe del simulatore sono "
                 "**misurate dall'AST**, non ricopiate: quelle dentro i fatti sono di blob "
                 "vecchi e vanno lette come storiche.)*")
    fuori.append("")
    fuori.append("| funzione | riga di oggi | quanti fatti |")
    fuori.append("|---|--:|--:|")
    for g in funzioni:
        fuori.append("| `%s` | `soliton_simulator.py:%d` | %d |"
                     % (g, dove[g], len(per_gruppo[g])))
    fuori.append("")
    fuori.append("---")
    fuori.append("")

    for g in ordine:
        if g not in per_gruppo:
            continue
        if g.startswith("@"):
            tit, sotto = INTESTAZIONE_GRUPPO[g]
            fuori.append("## %s" % tit)
            if sotto:
                fuori.append("")
                fuori.append("> %s" % sotto)
        else:
            fuori.append("## `%s`" % g)
            fuori.append("")
            fuori.append("*(oggi a `soliton_simulator.py:%d` - **misurato dall'AST**. %s)*"
                         % (dove[g], CHE_COSA.get(g, "")))
        fuori.append("")
        for b in per_gruppo[g]:
            fuori.extend(b)
        fuori.append("")
        fuori.append("---")
        fuori.append("")
    if manca:
        fuori.append("> **FUNZIONI CITATE E NON PIU' PRESENTI NEL SIMULATORE:** %s"
                     % ", ".join("`%s`" % m for m in sorted(manca)))
        fuori.append("")
    return NL.join(fuori) + NL, corpo, manca


def verifica(nuovo, corpo):
    """Nessuna riga non vuota dell'originale puo' mancare dall'uscita."""
    dentro = set(nuovo.split(NL))
    return [r for r in corpo if r.strip() and r not in dentro]


if __name__ == "__main__":
    nuovo, corpo, manca = costruisci()
    perse = verifica(nuovo, corpo)
    print("=" * 92)
    print("par.9 -> doc/FATTI_dal_codice.md")
    print("=" * 92)
    print("  righe di par.9 (corpo) ......... %d" % len(corpo))
    print("  punti di primo livello ......... %d" % len(DESTINAZIONE))
    print("  funzioni con almeno un fatto ... %d"
          % len(set(v for v in DESTINAZIONE.values() if not v.startswith("@"))))
    print("  righe NON RITROVATE nell'uscita  %d" % len(perse))
    for r in perse[:10]:
        print("      %s" % r[:88])
    if manca:
        print("  funzioni citate e assenti ...... %s" % ", ".join(sorted(manca)))
    if perse:
        sys.exit(1)
    if "--verifica" not in sys.argv[1:]:
        io.open(USCITA, "w", encoding="utf-8", newline=NL).write(nuovo)
        print("  SCRITTO %s (%d righe)"
              % (os.path.relpath(USCITA, RADICE).replace(chr(92), "/"), nuovo.count(NL)))
    sys.exit(0)
