# -*- coding: utf-8 -*-
"""PUNTO `14(c)(e)` — **UN ID NEL CODICE E' UN `@rif`, O NON ESISTE.**

> ### ⭐ **E' LA FRASE DEL MANDATO portata fino in fondo:** *«ogni errore e' nato da
> una macchina che leggeva la prosa»*. ### ⛔ **Un ID in un COMMENTO e' prosa**, e
> un riferimento che una macchina deve seguire ### **non puo' vivere nella prosa.**

| | che cosa impedisce | dove |
|---|---|---|
| `14(c)` | un ### **ID dell'indice dentro un commento `#`** di `primo_ordine/` | letto col ### **tokenizer**, non con una regex sul testo grezzo |
| `14(d)` | un ### **`@rif` verso un ID che NON esiste** | ### **via AST** |
| `14(e)` | un ### **`file:riga`** in un commento o in una stringa di `primo_ordine/` | il par.`2`: ### **i numeri di riga SONO SHIFTATI** |

### ⚠ **E IL CONFINE FRA COMMENTO E DOCSTRING LO DICHIARO, perche' non e' ovvio:**
il mandato dice ### **<<nei COMMENTI>>**, e io applico ### **esattamente quello.**

- un ### **commento `#`** sta ### **accanto a una riga di codice**: chi lo legge sta
  leggendo ### **il codice**, e un ID la' dentro ### **sembra un riferimento** —
  quindi ### **deve esserlo per davvero**, cioe' un `@rif`;
- un ### **docstring** e' ### **documentazione**: spiega ### **PERCHE'**, e in questo
  repo ### **le ragioni sono la parte che vale.** Vietare un ID nei docstring vorrebbe
  dire ### **togliere le ragioni**, e ### **nessun difetto di questo repo e' mai nato da
  un docstring.**

### ✅ **MISURATO il 2026-10-10:** `10` ID nei commenti *(curati)* e `33` nei
docstring *(### **che restano**, ed e' una scelta dichiarata, non una dimenticanza)*.
"""
import ast
import glob
import io
import json
import os
import re
import sys
import tokenize

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
sys.path.insert(0, _QUI)

NL = chr(10)
PRESIDIO = "P-RIF"

CARTELLA = "primo_ordine"
VISTA = os.path.join(RADICE, "doc", "RIFERIMENTI_era2.md")

_ID = re.compile(r"`([A-Z][A-Z0-9:_-]{2,})`")
_RIGA = re.compile(r"\.(?:py|md|yaml|yml|jsonl):\d+")

RUOLI = ("implementa", "verifica", "misura", "guardia", "genera")


def voci():
    p = os.path.join(RADICE, "doc", "indice", "voci.jsonl")
    return [json.loads(r) for r in io.open(p, encoding="utf-8").read().split(NL)
            if r.strip()]


def file_era2():
    f = sorted(glob.glob(os.path.join(RADICE, CARTELLA, "**", "*.py"), recursive=True))
    return [x.replace(os.sep, "/")[len(RADICE.replace(os.sep, "/")) + 1:]
            for x in f if "__pycache__" not in x]


def _token(rel):
    with io.open(os.path.join(RADICE, rel), "rb") as f:
        try:
            return list(tokenize.tokenize(f.readline))
        except Exception:
            return []


def id_nei_commenti(rel, ids):
    """### Gli ID che stanno ### **in un commento `#`**, col tokenizer.

    ### ⛔ **Col TOKENIZER e non con una regex sul testo grezzo:** una regex
    ### **non sa distinguere un `#` dentro una stringa** da un commento vero, e
    ### **un presidio che confonde i due o accusa il falso o tace sul vero.**
    """
    fuori = []
    for t in _token(rel):
        if t.type != tokenize.COMMENT:
            continue
        for m in _ID.findall(t.string):
            if m in ids:
                fuori.append((m, " ".join(t.string.split())[:110]))
    return fuori


def righe_indirizzate(rel):
    """### I `file:riga` ### **in un commento o in una stringa** *(punto `14(e)`)*."""
    fuori = []
    for t in _token(rel):
        if t.type not in (tokenize.COMMENT, tokenize.STRING):
            continue
        for m in _RIGA.findall(t.string):
            fuori.append((m, " ".join(t.string.split())[:110]))
    return fuori


def rif_dichiarati(rel):
    """### I `@rif` e le `rif(...)` di un file, ### **via AST**: `(id, ruolo, dove)`."""
    p = os.path.join(RADICE, rel)
    try:
        arb = ast.parse(io.open(p, encoding="utf-8").read(), filename=p)
    except Exception:
        return []
    fuori = []
    for nodo in ast.walk(arb):
        if isinstance(nodo, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for d in nodo.decorator_list:
                if not isinstance(d, ast.Call):
                    continue
                nome = getattr(d.func, "id", None) or getattr(d.func, "attr", None)
                if nome != "rif":
                    continue
                ruolo = None
                for kw in d.keywords:
                    if kw.arg == "ruolo" and isinstance(kw.value, ast.Constant):
                        ruolo = kw.value.value
                for a in d.args:
                    if isinstance(a, ast.Constant) and isinstance(a.value, str):
                        fuori.append((a.value, ruolo, "%s::%s" % (rel, nodo.name)))
    return fuori


def tutti_i_rif():
    fuori = []
    for rel in file_era2():
        fuori += rif_dichiarati(rel)
    return fuori


def controlla():
    err = []
    ids = {x["id"] for x in voci()}
    for rel in file_era2():
        # ------------------------------------------------------------------ `14(c)`
        for i, testo in id_nei_commenti(rel, ids):
            err.append("`P-RIF` `%s`: l-ID `%s` sta IN UN COMMENTO. ### Un riferimento "
                       "che una macchina deve seguire NON PUO- VIVERE NELLA PROSA: o e- "
                       "un `@rif(\"%s\", ruolo=...)`, o la frase va nel DOCSTRING (che e- "
                       "documentazione). Il commento: <<%s>>" % (rel, i, i, testo))
        # ------------------------------------------------------------------ `14(e)`
        for m, testo in righe_indirizzate(rel):
            err.append("`P-RIF` `%s`: c-e- un indirizzo A RIGA (`%s`). ### Il par.2: i "
                       "numeri di riga sono di blob vecchi e SONO SHIFTATI -- si cita "
                       "### UN NOME QUALIFICATO DI FUNZIONE. Il testo: <<%s>>"
                       % (rel, m, testo))
        # ------------------------------------------------------------------ `14(d)`
        for i, ruolo, dove in rif_dichiarati(rel):
            if i not in ids:
                err.append("`P-RIF` `%s`: il `@rif` verso `%s` punta a UN ID CHE NON "
                           "ESISTE. ### Un riferimento rotto e- peggio di nessun "
                           "riferimento: la voce si crea con `crea-lotto`" % (dove, i))
            if ruolo not in RUOLI:
                err.append("`P-RIF` `%s`: il `@rif` verso `%s` ha `ruolo` %r fuori "
                           "vocabolario: %s" % (dove, i, ruolo, list(RUOLI)))
    return err


def segnali():
    """### I SEGNALI: una voce di ### **LEGGE** senza nessun `implementa`.

    ### ⚠ **SEGNALA e non rifiuta** *(`A9`)*, e il mandato lo dice: una legge
    ### **puo- essere in tabella e non ancora implementata** -- e ### **rifiutarlo
    vorrebbe dire rifiutare un fatto vero.**
    """
    per_id = {}
    for i, ruolo, dove in tutti_i_rif():
        per_id.setdefault(i, []).append((ruolo, dove))
    fuori = []
    for v in sorted(voci(), key=lambda x: x["id"]):
        if not v.get("leggi"):
            continue
        # ### ⚠ **E LA PRIMA REGOLA CHE AVEVO SCRITTO ERA TROPPO RIGIDA:**
        # ### pretendeva un `@rif` di ruolo ### **`implementa`**, e ha segnalato
        # ### `MISURA-NORMA-ERA2` -- che e- ### **una MISURA**, e l-osservatore
        # ### ### **LA MISURA**, non la implementa. ### ✅ **La regola giusta:
        # ### NESSUN `@rif` DI NESSUN RUOLO** -- cioe- ### **niente nel codice la
        # ### tocca.**
        ruoli = {r for r, _d in per_id.get(v["id"], [])}
        if not ruoli:
            fuori.append("`P-RIF` segnale `%s`: e- una voce che nomina delle LEGGI e "
                         "### NESSUN `@rif` LA TOCCA, con nessun ruolo. ### O la legge "
                         "non c-e- ancora, o il riferimento manca" % v["id"])
    return fuori


def vista():
    """### `14(d)`: ### **IL VERSO OPPOSTO, GENERATO.** Per ogni voce, chi la tocca."""
    per_id = {}
    for i, ruolo, dove in tutti_i_rif():
        per_id.setdefault(i, []).append((ruolo, dove))
    L = []
    A = L.append
    A("# I RIFERIMENTI DEL CODICE DELL'ERA `2` — **il verso OPPOSTO**")
    A("")
    A("> ### ⛔ **QUESTA VISTA E' GENERATA** da `csv/_rif_nel_codice.py`: "
      "### **non si modifica a mano.**")
    A("")
    A("> ### ⭐ **E IL VERSO OPPOSTO E' CIO' CHE UN `@rif` COMPRA.** Un ID in un "
      "commento si legge ### **solo se si apre quel file**; un `@rif` si legge "
      "### **dall'AST**, quindi ### **si puo' girare**: da una voce all'elenco di chi la "
      "implementa, la verifica, la misura.")
    A("")
    if not per_id:
        A("### ⚠ **NESSUN `@rif` ANCORA**, e lo dico invece di stampare una tabella "
          "vuota: il costrutto esiste *(`primo_ordine/_rif.py`, collaudato "
          "### **byte-inerte**)*, e ### **i riferimenti si aggiungono mano a mano che la "
          "fisica dell'era `2` cresce.**")
    else:
        A("| la voce | il ruolo | chi |")
        A("|---|---|---|")
        for i in sorted(per_id):
            for ruolo, dove in sorted(per_id[i]):
                A("| **`%s`** | `%s` | `%s` |" % (i, ruolo, dove))
        A("")
        A("### **`%d` voci, `%d` riferimenti.**" % (len(per_id),
                                                    sum(len(x) for x in per_id.values())))
    A("")
    A("---")
    A("")
    A("*(Il presidio e la vista: `python csv/_rif_nel_codice.py`. "
      "Il collaudo nei due versi: `--collaudo`.)*")
    return NL.join(L) + NL


# =====================================================================================
#   IL COLLAUDO -- NEI DUE VERSI
# =====================================================================================

def collaudo():
    ok = [0, 0]

    def esito(che, passa, nota=""):
        ok[1] += 1
        ok[0] += 1 if passa else 0
        print("  %-64s %s   %s" % (che, "PASSA" if passa else "### FALLISCE", nota))

    ids = {x["id"] for x in voci()}
    print("=" * 100)
    print("IL COLLAUDO DI `P-RIF` -- nei DUE VERSI")
    print("=" * 100)
    esito("sul disco: `P-RIF` TACE", controlla() == [],
          "%d file di `primo_ordine/` guardati" % len(file_era2()))
    esito("### il braccio sopra HA MATERIA (ci sono file da guardare)",
          len(file_era2()) >= 10, "%d file" % len(file_era2()))
    # --- quanti ID stanno nei DOCSTRING: la scelta dichiarata
    n_doc = 0
    for rel in file_era2():
        for t in _token(rel):
            if t.type == tokenize.STRING:
                n_doc += len([m for m in _ID.findall(t.string) if m in ids])
    esito("### e gli ID nei DOCSTRING RESTANO, ed e- una scelta DICHIARATA", n_doc > 0,
          "%d ID nei docstring: ### il mandato dice <<nei COMMENTI>>, e nessun difetto "
          "di questo repo e- mai nato da un docstring" % n_doc)
    # --- i casi che DEVONO scattare, su un file FINTO
    import tempfile
    d = tempfile.mkdtemp()
    sotto = os.path.join(RADICE, CARTELLA, "_finto_rif.py")
    try:
        io.open(sotto, "w", encoding="utf-8", newline=NL).write(
            "# -*- coding: utf-8 -*-" + NL
            + "# ### `A16` dice una cosa" + NL
            + '"""e questo docstring nomina `A16`, e va bene."""' + NL)
        e = controlla()
        esito("### DEVE scattare: un ID in un COMMENTO",
              any("sta IN UN COMMENTO" in x for x in e),
              "### o e- un `@rif`, o la frase va nel docstring")
        esito("### e NON deve scattare per il DOCSTRING dello stesso file",
              not any("docstring" in x and "sta IN UN COMMENTO" in x for x in e),
              "### il confine fra commento e docstring e- DICHIARATO")
        io.open(sotto, "w", encoding="utf-8", newline=NL).write(
            "# -*- coding: utf-8 -*-" + NL
            + "# il sigillo sta a soliton_simulator.py:7772" + NL)
        esito("### DEVE scattare: un indirizzo A RIGA in un commento",
              any("indirizzo A RIGA" in x for x in controlla()),
              "### il par.`2`: i numeri di riga SONO SHIFTATI")
        io.open(sotto, "w", encoding="utf-8", newline=NL).write(NL.join([
            "# -*- coding: utf-8 -*-",
            "import sys, os",
            "sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))",
            "from _rif import rif",
            "",
            "",
            '@rif("ID-CHE-NON-ESISTE", ruolo="implementa")',
            "def finta():",
            "    return 1",
            "",
        ]) + NL)
        esito("### DEVE scattare: un `@rif` verso UN ID CHE NON ESISTE",
              any("ID CHE NON ESISTE" in x for x in controlla()),
              "### un riferimento rotto e- peggio di nessun riferimento")
        io.open(sotto, "w", encoding="utf-8", newline=NL).write(NL.join([
            "# -*- coding: utf-8 -*-",
            '@rif("A16", ruolo="inventato")',
            "def finta():",
            "    return 1",
            "",
        ]) + NL)
        esito("### DEVE scattare: un `ruolo` fuori vocabolario",
              any("fuori vocabolario" in x for x in controlla()))
    finally:
        if os.path.exists(sotto):
            os.remove(sotto)
        os.rmdir(d)
    esito("NON deve scattare: tolto il file finto, `P-RIF` TACE di nuovo",
          controlla() == [], "### i bracci di sopra scattavano per LUI")
    # --- la vista si rigenera BYTE-IDENTICA
    if os.path.exists(VISTA):
        esito("### la VISTA rigenerata e- BYTE-IDENTICA a quella sul disco",
              io.open(VISTA, encoding="utf-8").read() == vista(),
              "### altrimenti qualcuno l-ha modificata a mano")
    print("=" * 100)
    print("IL COLLAUDO DI `P-RIF`: %d su %d   %s"
          % (ok[0], ok[1], "### TUTTI PASSATI" if ok[0] == ok[1] else "### CI SONO BUCHI"))
    print("=" * 100)
    return 0 if ok[0] == ok[1] else 1


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    if "--collaudo" in argv:
        return collaudo()
    err = controlla()
    if not err:
        io.open(VISTA, "w", encoding="utf-8", newline=NL).write(vista())
    sg = segnali()
    print("  `P-RIF`: %d file di `primo_ordine/`, %d `@rif` dichiarati"
          % (len(file_era2()), len(tutti_i_rif())))
    for e in err[:14]:
        print("  ### %s" % e)
    if not err:
        for s in sg[:8]:
            print("  ~ %s" % s)
        print("  scritto doc/RIFERIMENTI_era2.md")
    print("  ### %d errori, %d segnali" % (len(err), len(sg)))
    return 1 if err else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
