r"""**GENERA `doc/SMISTAMENTO_run_base.md` DAI DATI** — indice + ordine, nessuna decisione nel codice.

**Ultimo passo del refactoring (Luca, 2026-09-26):** *«l'indice diventa la FONTE, non una vista»*.
Prima questa vista viveva **dentro l'importatore**, e con lei **le decisioni**: `DECISIONI`,
`TIPO_A_MANO`, `ORDINE` erano **letterali Python**. Ora:

```
doc/INDICE_ID.tsv    le voci, con `stato`, `blocca_run_base`, `tipo`, `famiglia`, `motivo`, `nota`
doc/ORDINE_SI.tsv    l'ordine di lavoro: `n`, `voce`, `perche_viene_qui`, `stima`
```

> ### **NESSUNA DECISIONE E' IN QUESTO FILE.** Se una riga dello smistamento va cambiata, si cambia
> ### **il dato**, non il codice — ed e' il senso di *«l'indice e' la fonte»*.

**La vista NON si modifica a mano:** si rigenera da qui.
"""
# ESENTE-P5: non importa il simulatore e non lo fa girare. Legge due TSV e scrive un documento.
import io
import os
import re
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _QUI)
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, ".."))
INDICE = os.path.join(RADICE, "doc", "INDICE_ID.tsv")
ORDINE = os.path.join(RADICE, "doc", "ORDINE_SI.tsv")
DEST = os.path.join(RADICE, "doc", "SMISTAMENTO_run_base.md")
REVISIONE_DOC = "REVISIONE_SI_2026-09-26.md"
NL = chr(10)
TAB = chr(9)

FAMIGLIE = [("A", "INERZIA E AVVIO"), ("B", "TEMPO UNICO"), ("C", "DOPPIA COPERTURA E CREAZIONE"),
            ("D", "SOGLIE TARATE E SOTTO PLANCK"), ("E", "DISEGNO E STATISTICHE GLOBALI"),
            ("F", "FRENO E CONTRAZIONE"), ("G", "ARRETRATO DEGLI STRUMENTI")]
TIPI_SMIST = ("difetto", "fronte", "misura", "cura")


def tsv(p):
    r = io.open(p, encoding="utf-8", newline="").read().split(NL)
    col = [c.strip() for c in r[0].split(TAB)]
    fuori = []
    for x in r[1:]:
        if x.strip():
            c = (x.split(TAB) + [""] * len(col))[:len(col)]
            fuori.append(dict(zip(col, [y.strip() for y in c])))
    return fuori


def breve(s, n):
    s = re.sub(r"\s+", " ", s or "").replace("|", "/").strip()
    if len(s) <= n:
        return s
    _t = s[:n - 1]
    _sp = _t.rfind(" ")
    return (_t[:_sp] if _sp > n // 2 else _t) + chr(0x2026)


VOCI = tsv(INDICE)
ORD = tsv(ORDINE)
SMIST = [v for v in VOCI if v["tipo"] in TIPI_SMIST and v["stato"] in ("aperto", "da-decidere")]
SI = [v for v in SMIST if v["blocca_run_base"] == "SI"]
DV = [v for v in SMIST if v["blocca_run_base"] not in ("SI", "NO")]

R = []


def P(s=""):
    R.append(s)


P("# \U0001f9ee **SMISTAMENTO PER IL RUN BASE — la lista su cui decide Luca** *(2026-09-26)*")
P()
P("*(**Generata** da `csv/_vista_smistamento.py` **dai DATI**: `doc/INDICE_ID.tsv` +")
P("`doc/ORDINE_SI.tsv`. **Nessuna decisione sta nel codice**, e questa vista **non si modifica a")
P("mano**: si rigenera.)*")
P()
P("> ## ⚠ **`blocca_run_base` NON E' RIEMPITO A INTUITO.**")
P("> Qui stanno **solo** le voci che potrebbero bloccare: tipo `difetto`, `fronte`, `misura` o")
P("> `cura`, **e** stato `aperto` o `da-decidere`. Tutto il resto — `chiuso`, `non-difetto`,")
P("> `teoria`, `criterio-locale`, `assioma`, `standard` — **non blocca MAI**, ed e' `NO`")
P("> **per regola, non per giudizio**.")
P()
P("```")
P("voci nell'indice          %d" % len(VOCI))
P("in questo smistamento     %d   (tipo difetto/fronte/misura/cura E stato aperto/da-decidere)"
  % len(SMIST))
P("di cui blocca SI          %d" % len(SI))
P("```")
P()
P("## \U0001f3af **L'ORDINE DI LAVORO DEI `SI`** — %d voci, e l'ordine E' PER DIPENDENZA" % len(SI))
P()
P("> **Il lavoro sui `SI` comincia SOLO col via di Luca.** L'ordine e i motivi vengono da")
P("> **`doc/ORDINE_SI.tsv`**, che e' un DATO: si cambia la' dentro, non qui.")
P()
P("| # | voce | perche' viene qui | stima |")
P("|--:|---|---|--:|")
for o in sorted(ORD, key=lambda x: int(x["n"]) if x["n"].isdigit() else 99):
    P("| %s | **%s** | %s | %s |" % (o["n"], o["voce"], o["perche_viene_qui"], o["stima"]))
P()
P("**\U0001f4d6 LA REVISIONE STORICA DI OGNI VOCE** *(che cosa e' VERIFICATO sul codice e che cosa e'")
P("INFERENZA)*: %s"
  % " · ".join("[%s](%s)" % (v["id"], v["revisione"].replace("doc/", ""))
                 for v in sorted(SMIST, key=lambda x: x["id"])
                 if v.get("revisione") and "non-bloccano" not in v["revisione"]))
P()
P("**Le voci che NON bloccano hanno la loro sezione qui:** [NON BLOCCANO](%s#non-bloccano)."
  % REVISIONE_DOC)
P()
if DV:
    P("## ⚠ **VOCI CHE NON TORNANO CON LA PROVA DATA**")
    P()
    P("| voce | `blocca` | perche' non torna |")
    P("|---|:--:|---|")
    for v in DV:
        P("| **%s** | `%s` | %s |" % (v["id"], v["blocca_run_base"], v.get("motivo", "")))
    P()
for k, nome in FAMIGLIE + [("?", "SENZA FAMIGLIA — nessuna regola ha deciso")]:
    vv = [v for v in SMIST if (v["famiglia"] == k if k != "?"
                               else v["famiglia"] not in [x[0] for x in FAMIGLIE])]
    if not vv:
        continue
    P("## FAMIGLIA **%s** — %s   *(%d voci)*" % (k, nome, len(vv)))
    P()
    P("| blocca? | id | che cos'e' | **il motivo, in una frase** | fonte |")
    P("|:--:|---|---|---|---|")
    for v in sorted(vv, key=lambda x: (x["tipo"], x["id"])):
        P("| `%s` | **%s** | %s | %s | `%s` |"
          % (v["blocca_run_base"], v["id"], breve(v["titolo_breve"], 118),
             v.get("motivo", "(senza motivo: DIFETTO DEL DATO)"),
             v["fonte_principale"].split("::")[0].replace("doc/", "")))
    P()
P("---")
P()
P("**COSA QUESTA LISTA NON DICE:**")
P("- **non dice che le altre %d voci siano irrilevanti**: dice che **non possono bloccare un run"
  % (len(VOCI) - len(SMIST)))
P("  base** perche' sono chiuse, sono teoria, o sono etichette locali di un sigillo.")
P("- **il titolo e' UNA riga**: la spiegazione sta nella fonte, e la fonte e' in colonna.")
P("- **`motivo` viene dalla COLONNA dell'indice**, non da una regola di questo script: se una riga")
P("  non ha motivo, **manca il DATO**, e lo dice.")

io.open(DEST, "w", encoding="utf-8", newline=NL).write(NL.join(R) + NL)
print("scritto %s" % DEST)
print("  voci %d   smistamento %d   SI %d   da verificare %d" % (len(VOCI), len(SMIST), len(SI), len(DV)))
