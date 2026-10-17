# -*- coding: utf-8 -*-
"""I CENSIMENTI SUGLI STRUMENTI -- ### **chi materializza un albero, e chi scrive nel repo.**

> ### ⛔⛔ **PERCHE' QUESTO FILE ESISTE** *(`2026-10-17`, su rifiuto di `P-MOD`)*:
> questi due censimenti vivevano ### **dentro `_misura_mb1.py`**, che il braccio dei temporanei
> ha portato a ### **`746` righe su un tetto di `700`** -- e la regola e' chiara: ### **oltre
> SI DIVIDE, NON SI ALLUNGA.**
> ### ✅ **E uscire e' la cosa giusta comunque:** `_misura_mb1.py` misura ### **il raccordo
> al bit**; questi due ### **guardano gli STRUMENTI**, non la fisica. ### **Due cose, due moduli.**
> ### 📌 **E i due si somigliano per costruzione:** stesso perimetro, stesse tre cartelle
> fuori, ### **e entrambi rispondono a <<chi puo' sporcare il repo>>.**
"""
import io
import os

_QUI = os.path.dirname(os.path.abspath(__file__))
# ### ⚠ **LA RADICE, e non si eredita:** questo modulo e' importato, e ### **un importato
# ### che legge la radice dal chiamante guarda la cartella SBAGLIATA.**
RADICE = os.path.dirname(_QUI)

# ### ⛔ **IL PERIMETRO ATTIVO, e le tre cartelle che NON lo sono:** l'archivio, i sigilli
# ### vecchi e i test del fork ### **non girano piu'**, e un difetto la' dentro ### **non puo'
# ### sporcare il repo di oggi.**
FUORI_PERIMETRO = ("_archivio", "_seal_", "_test_")


def _tutti_i_py():
    """I `.py` del perimetro attivo, ### **in ordine e una volta sola.**"""
    import glob
    for q in sorted(glob.glob(os.path.join(RADICE, "csv", "**", "*.py"),
                              recursive=True)
                    + glob.glob(os.path.join(RADICE, "primo_ordine", "**", "*.py"),
                                recursive=True)):
        rel = os.path.relpath(q, RADICE).replace(os.sep, "/")
        if any(k in rel for k in FUORI_PERIMETRO):
            continue
        yield q, rel


# ### ⛔ **GLI STRUMENTI CHE MATERIALIZZANO UN ALBERO DEL PASSATO E VI ESEGUONO PYTHON.**
# ### ⚠ **La lista e' DICHIARATA, e uno nuovo FA FALLIRE** invece di passare: la stessa
# ### regola vale per lui, cioe' ### **nell-albero vecchio non si copia codice del passo.**
# ### 📌 **E <<materializzare un ALBERO>> non e' <<leggere un file da un commit>>:**
# ### `12` strumenti leggono TESTO da un commit *(documenti, indice)* e fanno girare
# ### ### **i comandi di OGGI** -- e quelli non hanno questo problema.
CONFRONTANO_ESEGUENDO = ("primo_ordine/_misura_mb1.py",)


def _censimento():
    """Chi materializza un albero del passato ### **e vi esegue python.**

    ### ⛔⛔ **CON L-AST, E NON CON UNA PAROLA** *(e la prima stesura cercava la
    parola: ha pescato ### **il commento che avevo appena scritto in `collauda.py`**)*.
    ### ✅ **Si cerca la FORMA VERA: una lista di argomenti che contiene `"worktree"`
    o `"archive"`** -- cioe' ### **una chiamata a `git`**, non una frase in prosa.
    ### ⭐ **E i commenti sono INVISIBILI all-AST**, che qui e' esattamente cio- che
    serve: e- la stessa lezione di `P-TAB`.
    """
    import ast
    tro = []
    for q, rel in _tutti_i_py():
        try:
            arb = ast.parse(io.open(q, encoding="utf-8").read())
        except SyntaxError:
            continue
        albero, esegue = False, False
        for n in ast.walk(arb):
            if isinstance(n, (ast.List, ast.Tuple)):
                for x in n.elts:
                    if (isinstance(x, ast.Constant)
                            and x.value in ("worktree", "archive")):
                        albero = True
            if isinstance(n, ast.Attribute) and n.attr == "executable":
                esegue = True
        if albero and esegue:
            tro.append(rel)
    return tro


# ### ⛔ **GLI STRUMENTI CHE POSSONO SCRIVERE NEL REPO: la lista e' VUOTA, e uno nuovo
# ### FA FALLIRE.** ### ⚠ **Il difetto, trovato dal guardiano il `2026-10-17`:** leggere
# ### `TEMP` dall'ambiente ha ### **un RIPIEGO**, e su Linux quel ripiego e'
# ### ### **la radice del repo** -- e questa misura ci lasciava ### **una copia INTERA
# ### dell'albero vecchio.** ### ✅ **`tempfile` non ha ripieghi.**
TEMPORANEI_AMMESSI = ()


def _censimento_temporanei():
    """Chi legge `TEMP` dall'ambiente, ### **nel perimetro attivo.**"""
    # ### la parola si cerca COME TESTO, e basta: il ripiego sta sempre accanto
    ago = "environ"
    ago2 = "TEMP"
    tro = []
    for q, rel in _tutti_i_py():
        t = io.open(q, encoding="utf-8").read()
        for riga in t.split(chr(10)):
            if ago in riga and ago2 in riga and not riga.strip().startswith("#"):
                tro.append(rel)
                break
    return tro
