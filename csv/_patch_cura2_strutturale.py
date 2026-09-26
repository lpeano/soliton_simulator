# -*- coding: utf-8 -*-
"""**LA `CURA 2` DIVENTA STRUTTURALE: i quattro rami `else` escono dal simulatore.**
*(decisione di Luca, 2026-09-27)*

**PERCHE' PER AST E NON A STRINGHE:** togliere un `if` significa **de-indentare il suo corpo di
quattro spazi**, su quattro blocchi da 2 a 19 righe. Una tabella di sostituzioni a stringhe su
quel lavoro e' il modo piu' facile di sbagliare **un** blocco e non accorgersene. Qui i blocchi si
trovano **dall'albero sintattico**, e il controllo e' che **il corpo del ramo acceso sia lo stesso
testo, de-indentato di 4 e nient'altro**.

**LA FORMA DEL FLAG, e la scelta e' dichiarata:**

| | scelta | perche' |
|---|---|---|
| **la costante** | **`TEMPO_UNICO_MITOSI = True`, e RESTA un booleano di modulo** | cosi' continua a comparire nella **dichiarazione della configurazione** (`H-P5` la enumera con `vars(S)`): **cancellarla la farebbe sparire dal referto**, e `H-P5` chiede la configurazione **INTERA** |
| **l'opzione CLI** | **`--tempo-unico-mitosi` resta ACCETTATA come NO-OP DICHIARATO**, e **stampa un avviso** | il driver la passa in ogni run e **ogni comando gia' scritto** la contiene: toglierla farebbe morire `argparse`. E' la forma gia' usata per `--step2-orologio` |
| **l'assegnazione** | **TOLTA da `_applica_flag`** | e' cio' che rende la legge **strutturale**: nessun percorso puo' piu' spegnerla |
| **nessun `--senza-...`** | **di proposito, e va detto** | `par.10` lo chiede per una **promozione**, dove il ramo OFF resta nel codice. **Qui i rami ESCONO:** il braccio OFF vive **al tag `pre-cura2-strutturale`**, non in un flag. **Un `--senza-` che non ha un ramo dove andare sarebbe un flag che mente.** |

    python csv/_patch_cura2_strutturale.py --prova
    python csv/_patch_cura2_strutturale.py

ASCII puro.
"""
import ast
import io
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Riscrive un sorgente per AST.

NL = chr(10)
_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, ".."))
SIM = os.path.join(RADICE, "soliton_simulator.py")
FLAG = "TEMPO_UNICO_MITOSI"
TAG = "pre-cura2-strutturale"

NOTA = ("# [CURA 2 STRUTTURALE, 2026-09-27] IL RAMO `if %s:` E' STATO TOLTO: "
        "la legge e' SEMPRE questa." % FLAG)
NOTA2 = ("#   Il ramo `else` e' ARCHIVIATO in `csv/_archivio/rami_off_cura2.py` e si rilancia "
         "dal tag `%s`." % TAG)


def blocchi(src):
    """I quattro `if FLAG:` dent`mitosi`, dal piu' in basso al piu' in alto (si taglia da sotto)."""
    arb = ast.parse(src)
    mit = next(n for n in ast.walk(arb)
               if isinstance(n, ast.FunctionDef) and n.name == "mitosi")
    fuori = []
    for nd in ast.walk(mit):
        if isinstance(nd, ast.If) and isinstance(nd.test, ast.Name) and nd.test.id == FLAG:
            a_if = nd.lineno
            b_corpo = max(y.end_lineno for y in nd.body)
            a_else = min(y.lineno for y in nd.orelse) if nd.orelse else None
            b_else = max(y.end_lineno for y in nd.orelse) if nd.orelse else None
            fuori.append((a_if, b_corpo, a_else, b_else, nd.col_offset))
    fuori.sort(reverse=True)
    return fuori


def togli(src):
    """Restituisce `(nuovo, resoconto)`. Il corpo del ramo acceso resta, de-indentato di 4."""
    righe = src.split(NL)
    res = []
    for a_if, b_corpo, a_else, b_else, col in blocchi(src):
        corpo = righe[a_if:b_corpo]          # le righe del ramo ACCESO (a_if e' 1-based)
        nuovo = []
        for r in corpo:
            if not r.strip():
                nuovo.append(r)
                continue
            if not r.startswith(" " * (col + 4)):
                raise SystemExit("riga non indentata come atteso a :%d: %r" % (a_if, r[:60]))
            nuovo.append(r[4:])
        testa = " " * col
        fine = b_else if b_else else b_corpo
        righe[a_if - 1:fine] = ([testa + NOTA, testa + NOTA2] + nuovo)
        res.append((a_if, b_corpo - a_if, (b_else - a_else + 1) if a_else else 0))
    return NL.join(righe), sorted(res)


COPPIE = [
    # la costante diventa `True`, e RESTA un booleano di modulo (`H-P5` la enumera)
    ("TEMPO_UNICO_MITOSI = False  # [CURA 2, 2026-09-24] UN SOLO OROLOGIO DENTRO `mitosi()`.",
     "TEMPO_UNICO_MITOSI = True   # [CURA 2 -> STRUTTURALE, 2026-09-27: decisione di Luca]"
     + NL
     + "                        # ⚠ NON E' PIU' UN FLAG: E' UNA LEGGE. I quattro rami `else`"
     + NL
     + "                        # sono USCITI dal simulatore, e l'assegnazione da `_applica_flag`"
     + NL
     + "                        # e' stata TOLTA: nessun percorso puo' piu' spegnerla."
     + NL
     + "                        # RESTA un booleano di MODULO di proposito: cosi' continua a"
     + NL
     + "                        # comparire nella dichiarazione della configurazione (`H-P5` la"
     + NL
     + "                        # enumera con `vars(S)`), e cancellarla la farebbe SPARIRE dal"
     + NL
     + "                        # referto proprio mentre diventa obbligatoria."
     + NL
     + "                        # IL BRACCIO OFF VIVE AL TAG `pre-cura2-strutturale`, non in un"
     + NL
     + "                        # flag: per questo NON c'e' un `--senza-tempo-unico-mitosi`."
     + NL
     + "                        # I rami: `csv/_archivio/rami_off_cura2.py`."
     + NL
     + "                        # [CURA 2, 2026-09-24] UN SOLO OROLOGIO DENTRO `mitosi()`.", 1),
    # l'assegnazione esce da `_applica_flag`
    ('    TEMPO_UNICO_MITOSI = bool(getattr(a, "tempo_unico_mitosi", False))  # CURA 2: default off',
     "    # [CURA 2 STRUTTURALE, 2026-09-27] L'ASSEGNAZIONE E' TOLTA: la legge non si spegne."
     + NL
     + "    #   `--tempo-unico-mitosi` resta ACCETTATA come NO-OP dichiarato (il driver la passa"
     + NL
     + "    #   in ogni run, e ogni comando gia' scritto la contiene), e AVVISA."
     + NL
     + '    if getattr(a, "tempo_unico_mitosi", False):'
     + NL
     + '        print("[tempo-unico-mitosi] NO-OP DICHIARATO dal 2026-09-27: la `CURA 2` e\'"'
     + NL
     + '              " STRUTTURALE e i rami a flag spento sono USCITI dal simulatore."'
     + NL
     + '              " Il braccio OFF vive al tag `pre-cura2-strutturale`;"'
     + NL
     + '              " i rami in csv/_archivio/rami_off_cura2.py.")', 1),
]


if __name__ == "__main__":
    scrivi = "--prova" not in sys.argv[1:]
    src = io.open(SIM, encoding="utf-8", newline="").read()
    print("=" * 96)
    print("`CURA 2` STRUTTURALE: i quattro rami `else` escono%s"
          % ("" if scrivi else "   (PROVA: non scrivo)"))
    print("=" * 96)
    bl = blocchi(src)
    print("  `if %s:` trovati dentro `mitosi` .... %d" % (FLAG, len(bl)))
    if len(bl) != 4:
        raise SystemExit("attesi 4 blocchi, trovati %d: il codice e' cambiato" % len(bl))
    nuovo, res = togli(src)
    for a_if, n_on, n_off in res:
        print("      `if` a :%-6d corpo ACCESO %2d righe (resta)   ramo `else` %2d righe (esce)"
              % (a_if, n_on, n_off))
    fatte = 0
    for vecchio, nn, attese in COPPIE:
        n = nuovo.count(vecchio)
        if n != attese:
            raise SystemExit("ancora attesa %d volte, trovata %d: %s" % (attese, n, vecchio[:80]))
        nuovo = nuovo.replace(vecchio, nn)
        fatte += 1
    print("  sostituzioni asserite (costante, assegnazione) .... %d" % fatte)
    # i controlli, e sono il punto: l'AST dice che nessun `if FLAG` e' rimasto, e il file compila
    try:
        arb2 = ast.parse(nuovo)
    except SyntaxError as e:
        raise SystemExit("IL FILE NUOVO NON COMPILA: %s" % e)
    rimasti = [n.lineno for n in ast.walk(arb2)
               if isinstance(n, ast.If) and isinstance(n.test, ast.Name) and n.test.id == FLAG]
    print("  `if %s:` RIMASTI (atteso 0) ......... %d %s" % (FLAG, len(rimasti), rimasti))
    glob = [n.lineno for n in ast.walk(arb2)
            if isinstance(n, ast.Global) and FLAG in n.names]
    print("  `global %s` (resta: non fa danno) ... %s" % (FLAG, glob))
    assegn = [n.lineno for n in ast.walk(arb2) if isinstance(n, ast.Assign)
              and any(isinstance(t, ast.Name) and t.id == FLAG for t in n.targets)]
    print("  assegnazioni a %s (atteso 1: la costante) ... %s" % (FLAG, assegn))
    if rimasti or len(assegn) != 1:
        sys.exit(1)
    if scrivi:
        io.open(SIM, "w", encoding="utf-8", newline=NL).write(nuovo)
        print("  SCRITTO soliton_simulator.py   (%d righe -> %d)"
              % (src.count(NL), nuovo.count(NL)))
    sys.exit(0)
