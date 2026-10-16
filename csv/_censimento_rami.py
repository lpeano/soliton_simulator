# -*- coding: utf-8 -*-
"""IL CENSIMENTO DI `P-R1` ESTESO A TUTTI I FILE DI FISICA — **e NON blocca niente.**

> ### ⛔ **MANDATO DI LUCA del `2026-10-16` alle `09:21`:** `P-R1` deve coprire
> ### **tutti** i file che contengono fisica, non una lista fissa — e il motivo e' che
> ### **il rapporto fra codice e indice dev'essere INFALLIBILE.**
> ### ⚠ **E IN QUESTO PEZZO NON SI DICHIARA NIENTE:** *«non dichiarare i rami, non
> cambiare la lista del presidio vero, non toccare il codice di fisica — alcuni rami
> potrebbero essere scelte di fisica nascoste, e quelle le decide Luca»*.

## ⭐⭐ IL BUCO, misurato

`P-R1` *(`csv/_rami_era2.py`)* guarda una lista **HARDCODED**: `stato.py`,
`hamiltoniana.py`, `passo.py`, `crescita.py`, `vuoto.py` e `termini/*.py`.
### ⛔ **NON guarda `motore.py`, `energia.py`, `flussi_parziali.py`, `saturazione.py` ne'
`materia_vuoto.py`** — cioe' **proprio dove sta la maggior parte della fisica.**

## ⭐ QUESTO CENSIMENTO **NON RISCRIVE LA LOGICA: LA IMPORTA**

Chiama `_rami_era2._conta` e `_rami_era2.default_nelle_firme`, e per l'aggiunta `C`
`_un_solo_esecutore.fase_a_mano`. ### ⛔ **E' la regola
`STRUMENTO-LEGGE-DALLA-TABELLA` applicata A UN PRESIDIO:** un censimento che riscrivesse
il conteggio dei rami misurerebbe **la SUA idea di ramo**, non quella di `P-R1` — e il
numero **non sarebbe confrontabile con niente.**

## ⛔ LA LISTA DEI FILE **SI DERIVA**, e il derivato **si CONFRONTA col dichiarato**

Ogni `.py` sotto `primo_ordine/`, meno gli `__init__.py`. ### ✅ **E' sicuro perche'
`H-FISICA-FUORI-LISTA` pretende che ognuno di quelli stia nella LISTA di
`csv/_file_fisica.py`** — e questo censimento **lo verifica a ogni corsa** invece di
fidarsi: se il derivato non e' contenuto nel dichiarato, **e' il hook a essere rotto.**
"""
import ast
import glob
import io
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
sys.path.insert(0, _QUI)
import _presidio                                              # noqa: E402

NL = chr(10)
NOME = "CENSIMENTO-RAMI"


# =====================================================================================
#   LA LISTA DEI FILE -- **derivata**, e confrontata col dichiarato
# -------------------------------------------------------------------------------------
def derivata():
    """Ogni `.py` sotto `primo_ordine/`, ### **dal disco e non da una lista.**"""
    f = glob.glob(os.path.join(RADICE, "primo_ordine", "**", "*.py"), recursive=True)
    return sorted(os.path.relpath(x, RADICE).replace(os.sep, "/") for x in f
                  if not x.endswith("__init__.py"))


def dichiarata():
    """La LISTA di `csv/_file_fisica.py`, ### **per il confronto.**"""
    import _file_fisica as FF
    return set(FF.sorvegliati())


def fuori_dal_dichiarato():
    """### ⛔ **Se non e' vuoto, `H-FISICA-FUORI-LISTA` E' ROTTO**, e si dice."""
    return sorted(set(derivata()) - dichiarata())


# =====================================================================================
#   L'AGGIUNTA `C` -- il buco di `P-ES1`, **in numero**
# -------------------------------------------------------------------------------------
# ### ⛔⛔ **`P-ES1` CERCA LA STRINGA LETTERALE `-1j`** (`FORMA_PASSO in seg`), quindi
# ### ### **`- 1j` con lo spazio LO EVADE.** ### ⚠ **Misurato per caso:** la prima stesura
# ### dell'Eulero di `_collauda_materia_vuoto.py`, scritta con lo spazio, ### **non veniva
# ### vista** -- il presidio si lamentava dell'### **eccezione ORFANA**, non del passo
# ### nascosto.
# ### ⚠ **E QUI NON SI CHIUDE:** *<<la decisione su come chiuderlo e' di Luca>>*, e `P-ES1`
# ### ha ### **eccezioni dichiarate** che un rivelatore nuovo potrebbe invalidare.
def _e_meno_i(n):
    """`True` se `n` ### **si ripiega a `-1j`**, in qualunque forma."""
    if isinstance(n, ast.Constant) and isinstance(n.value, complex):
        return n.value == -1j
    if isinstance(n, ast.UnaryOp) and isinstance(n.op, ast.USub):
        v = n.operand
        return (isinstance(v, ast.Constant) and isinstance(v.value, complex)
                and v.value == 1j)
    return False


def fase_a_mano_ast(rel, base=None):
    """Le funzioni che nominano `dt` e contengono ### **`-1j` SECONDO L'AST.**

    ### ⭐ **La differenza con la ricerca LETTERALE di `P-ES1` E' IL BUCO**, e si conta.
    """
    p = os.path.join(base or RADICE, rel)
    try:
        src = io.open(p, encoding="utf-8").read()
        arb = ast.parse(src, filename=p)
    except Exception:                                          # noqa: BLE001
        return []
    fuori = []
    for n in ast.walk(arb):
        if not isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        nomi = set()
        for x in ast.walk(n):
            if isinstance(x, ast.Name):
                nomi.add(x.id)
            elif isinstance(x, ast.Attribute):
                nomi.add(x.attr)
        if "dt" in nomi and any(_e_meno_i(x) for x in ast.walk(n)):
            fuori.append(n.name)
    return sorted(fuori)


# =====================================================================================
#   IL CENSIMENTO -- **`P-R1` in SOLA LETTURA, su tutti i file**
# -------------------------------------------------------------------------------------
def censisci(file=None, base=None):
    """Per ogni file: ### **i rami non dichiarati** e ### **i default nelle firme.**

    ### ⛔ **SOLA LETTURA:** nessun file si scrive, nessuna lista si cambia, e la
    logica e' ### **quella di `P-R1`**, importata.
    """
    import _rami_era2 as R1
    gia = set(R1.file_fisica())
    fuori = []
    for rel in (file if file is not None else derivata()):
        p = os.path.join(base or RADICE, rel)
        if not os.path.exists(p):
            continue
        try:
            rami = R1._conta(p)
            dflt = R1.default_nelle_firme(p)
        except Exception as e:                                 # noqa: BLE001
            fuori.append({"file": rel, "sorvegliato": rel in gia, "illeggibile": str(e)[:60],
                          "rami": {}, "non_dichiarati": {}, "default": []})
            continue
        nd = {}
        for fn, c in rami.items():
            if (rel, fn) not in R1.RAMI:
                nd[fn] = c
        fuori.append({"file": rel, "sorvegliato": rel in gia, "illeggibile": "",
                      "rami": rami, "non_dichiarati": nd, "default": dflt})
    return fuori


def buco_di_pes1(file=None, base=None):
    """Le funzioni che l'AST vede e ### **la ricerca LETTERALE di `P-ES1` NON vede.**"""
    import _un_solo_esecutore as ES
    fuori = []
    for rel in (file if file is not None else derivata()):
        p = os.path.join(base or RADICE, rel)
        if not os.path.exists(p):
            continue
        a = set(fase_a_mano_ast(rel, base=base))
        # ### ⚠ **`ES.passi_a_mano` legge da `RADICE`**, quindi col `base` finto si
        # ### passa il percorso ### **assoluto**: `os.path.join` con un assoluto
        # ### ### **lo restituisce tale e quale**, ed e' la via senza toccare il presidio.
        letto = set(ES.passi_a_mano(p if base else rel))
        if a - letto:
            fuori.append((rel, sorted(a - letto), sorted(letto)))
    return fuori


# =====================================================================================
#   IL REFERTO
# -------------------------------------------------------------------------------------
def referto(cens, buco, orfani):
    T = ["IL CENSIMENTO DI `P-R1` ESTESO A TUTTI I FILE DI FISICA", ""]
    sor = [r for r in cens if r["sorvegliato"]]
    non = [r for r in cens if not r["sorvegliato"]]
    nd_sor = sum(len(r["non_dichiarati"]) for r in sor)
    nd_non = sum(len(r["non_dichiarati"]) for r in non)
    ra_non = sum(sum(r["non_dichiarati"].values()) for r in non)
    df_sor = sum(len(r["default"]) for r in sor)
    df_non = sum(len(r["default"]) for r in non)
    T.append("  la lista dei file e- DERIVATA dal disco (ogni `.py` sotto"
             " `primo_ordine/`, meno gli `__init__`)")
    T.append("  e il derivato FUORI dal dichiarato di `csv/_file_fisica.py`: %d"
             "   ### se non fosse 0, `H-FISICA-FUORI-LISTA` sarebbe ROTTO" % len(orfani))
    T.append("")
    T.append("  %-28s %8s %8s" % ("", "oggi", "fuori"))
    T.append("  %-28s %8s %8s" % ("", "sorvegliati", "lista"))
    T.append("  " + "-" * 48)
    T.append("  %-28s %8d %8d" % ("file", len(sor), len(non)))
    T.append("  %-28s %8d %8d" % ("funzioni NON dichiarate", nd_sor, nd_non))
    T.append("  %-28s %8s %8d" % ("rami in quelle funzioni", "-", ra_non))
    T.append("  %-28s %8d %8d" % ("default nelle firme", df_sor, df_non))
    T.append("")
    T.append("  ### I FILE FUORI DALLA LISTA, ordinati per rami non dichiarati")
    T.append("  %-46s %6s %6s %7s" % ("file", "fn", "rami", "default"))
    T.append("  " + "-" * 70)
    for r in sorted(non, key=lambda x: -sum(x["non_dichiarati"].values())):
        if not r["non_dichiarati"] and not r["default"]:
            continue
        T.append("  %-46s %6d %6d %7d"
                 % (r["file"], len(r["non_dichiarati"]),
                    sum(r["non_dichiarati"].values()), len(r["default"])))
    T.append("")
    # ### ⛔⛔ **LA SEZIONE CHE SERVE A LUCA: i MODULI DI FISICA, funzione per
    # ### funzione.** ### ⚠ **La classificazione e- PER PREFISSO e la dichiaro:** un
    # ### file che comincia con `_collauda_` o `_misura_` e- ### **uno strumento**, gli
    # ### altri sono ### **moduli.** ### **Non e- una verita-: e- una convenzione del repo**,
    # ### e serve a mettere davanti agli occhi ### **i rami che potrebbero essere scelte di
    # ### fisica nascoste.**
    T.append("  ### I MODULI DI FISICA (non `_collauda_*`, non `_misura_*`), FUNZIONE PER"
             " FUNZIONE")
    T.append("  ### e- qui che una SCELTA DI FISICA NASCOSTA si cercherebbe: la decide Luca")
    T.append("  %-30s %-34s %6s" % ("file", "funzione", "rami"))
    T.append("  " + "-" * 74)
    for r in sorted(non, key=lambda x: x["file"]):
        base_n = r["file"].rsplit("/", 1)[-1]
        if base_n.startswith("_collauda_") or base_n.startswith("_misura_"):
            continue
        for fn, c in sorted(r["non_dichiarati"].items(), key=lambda t: (-t[1], t[0])):
            T.append("  %-30s %-34s %6d" % (r["file"], fn, c))
    T.append("")
    T.append("  ### L-AGGIUNTA `C`: IL BUCO DI `P-ES1` (la ricerca LETTERALE `-1j`)")
    if buco:
        for rel, solo_ast, letto in buco:
            T.append("  %-46s AST vede %s, la ricerca letterale %s"
                     % (rel, solo_ast, letto or "NIENTE"))
    else:
        T.append("  nessuna funzione EVADE oggi la ricerca letterale: il buco E- APERTO")
        T.append("  ma NON HA MATERIA nel repo di adesso -- e il braccio che segue lo"
                 " PROVA su un file finto")
    return NL.join(T)


# =====================================================================================
#   I CASI CHE DEVONO FALLIRE -- **fuori dal repo**
# -------------------------------------------------------------------------------------
_OK = []


def esito(che, passa, nota=""):
    _OK.append(bool(passa))
    print("  %-64s %s   %s" % (che[:64], "PASSA" if passa else "### FALLISCE", nota))


def collaudo():
    import shutil
    import tempfile
    print("=" * 100)
    print("IL COLLAUDO DEL CENSIMENTO: I CASI CHE DEVONO FALLIRE, FUORI DAL REPO")
    print("=" * 100)
    base = tempfile.mkdtemp(prefix="cens_")
    try:
        # ### ⛔ **① UN RAMO NON DICHIARATO in un file che OGGI E- ESCLUSO.**
        # ### Il nome e' quello di un file fuori dalla lista di `P-R1`, e la funzione
        # ### ### **non sta in `RAMI`**: deve COMPARIRE nel censimento.
        f1 = os.path.join(base, "primo_ordine")
        os.makedirs(f1)
        io.open(os.path.join(f1, "motore.py"), "wb").write(
            ("def finta(x):" + NL + "    if x:" + NL + "        return 1" + NL
             + "    return 0" + NL).encode("utf-8"))
        c = censisci(["primo_ordine/motore.py"], base=base)
        esito("### ① DEVE comparire: un ramo NON dichiarato in un file ESCLUSO oggi",
              c and c[0]["non_dichiarati"].get("finta") == 1,
              "`finta` con 1 ramo, e il file NON e- fra i sorvegliati: %s"
              % (not c[0]["sorvegliato"]))
        # ### ⛔ **② UN DEFAULT NELLA FIRMA, nello stesso file.**
        io.open(os.path.join(f1, "energia.py"), "wb").write(
            ("def finta2(x, quanti=3):" + NL + "    return x * quanti" + NL)
            .encode("utf-8"))
        c2 = censisci(["primo_ordine/energia.py"], base=base)
        esito("### ② DEVE comparire: un `default` nella firma, fuori dalla lista",
              c2 and [x for x in c2[0]["default"] if x[1] == "quanti"],
              "visto %s" % (c2[0]["default"],))
        # ### ⛔⛔ **③ IL BUCO DI `P-ES1`, MISURATO: `- 1j` CON LO SPAZIO.**
        # ### ✅ **L-AST lo vede e la ricerca LETTERALE no**, e questo e' il buco.
        io.open(os.path.join(f1, "vuoto.py"), "wb").write(
            ("def integra(st, dt, g):" + NL
             + "    return st + dt * (- 1j) * g" + NL).encode("utf-8"))
        b = buco_di_pes1(["primo_ordine/vuoto.py"], base=base)
        esito("### ③ DEVE comparire: `- 1j` con lo SPAZIO evade la ricerca letterale",
              b and b[0][1] == ["integra"] and b[0][2] == [],
              "AST vede %s, la ricerca letterale %s"
              % (b[0][1] if b else "-", (b[0][2] or "NIENTE") if b else "-"))
        # ### ⭐ **IL CONTROLLO CHE POTREBBE FALLIRE: con `-1j` ATTACCATO, li vedono
        # ### ### ENTRAMBI** -- altrimenti il braccio ③ non direbbe che il problema e'
        # ### ### **lo SPAZIO**, ma che il rivelatore letterale non funziona mai.
        io.open(os.path.join(f1, "crescita.py"), "wb").write(
            ("def integra2(st, dt, g):" + NL
             + "    return st + dt * (-1j) * g" + NL).encode("utf-8"))
        b2 = buco_di_pes1(["primo_ordine/crescita.py"], base=base)
        esito("### (c) e con `-1j` ATTACCATO il buco NON c-e-: lo vedono entrambi",
              not b2,
              "nessuna differenza: il problema e- LO SPAZIO, non il rivelatore")
        # ### ⭐ **E un file PULITO non da- niente.**
        io.open(os.path.join(f1, "stato.py"), "wb").write(
            ('"""Niente."""' + NL + "X = 1" + NL).encode("utf-8"))
        c3 = censisci(["primo_ordine/stato.py"], base=base)
        esito("### (c) e un file PULITO non da- NESSUN reperto",
              c3 and not c3[0]["non_dichiarati"] and not c3[0]["default"],
              "altrimenti il censimento vede FANTASMI")
    finally:
        shutil.rmtree(base, ignore_errors=True)
    # ### ⭐ **E SUL REPO: il derivato dev-essere CONTENUTO nel dichiarato.**
    orf = fuori_dal_dichiarato()
    esito("### (r) sul repo: ogni file derivato e- NEL DICHIARATO",
          not orf, "%d fuori%s" % (len(orf), ("   " + " ".join(orf[:4])) if orf else ""))
    print("=" * 100)
    print("IL COLLAUDO DEL CENSIMENTO: %d su %d   %s"
          % (sum(_OK), len(_OK),
             "### TUTTI PASSATI" if all(_OK) else "### CI SONO ROSSI"))
    print("=" * 100)
    return 0 if all(_OK) else 1


def main(argv):
    _presidio.avvia(__file__)
    if "--collaudo" in argv:
        return collaudo()
    cens = censisci()
    buco = buco_di_pes1()
    orf = fuori_dal_dichiarato()
    print(referto(cens, buco, orf))
    # ### ⛔ **NON BLOCCA NIENTE:** il mandato dice *<<il censimento, senza bloccare
    # ### niente>>*, e un censimento che rifiutasse un commit ### **dichiarerebbe i rami
    # ### al posto di Luca.**
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
