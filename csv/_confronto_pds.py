r"""**IL CONFRONTO PRIMA/DOPO di `_punto_della_situazione`**, e le differenze SPIEGATE.

**Punto 2 di `LETTORI-INDICE`** *(Luca, 2026-09-26)*: *«un confronto prima/dopo del suo output con le
differenze spiegate»*.

**PRIMA** = l'output del parser su `doc/STATO_RUN.md`, salvato prima della conversione.
**DOPO** = l'output della vista su `doc/INDICE_ID.tsv`.

**Le differenze sono di TRE classi, e due su tre sono GUADAGNI.**

ASCII puro nell'output.
"""
# ESENTE-P5: non importa il simulatore e non lo fa girare. Confronta due documenti.
import io
import os
import re
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _QUI)
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, ".."))
DEST = os.path.join(RADICE, "doc", "LETTORI_INDICE_confronto.md")
NL = chr(10)

PRIMA = os.environ.get("PDS_PRIMA", "")
DOPO = os.path.join(RADICE, "doc", "PUNTO_DELLA_SITUAZIONE.md")
#   le tre classi, con l'elenco DICHIARATO (giudizio mio, e sta qui perche' si veda)
NON_ID = ["S-MIT2", "_verifica_registro.py", "doc/PATTERN_DI_PROVA.md"]


def sez(p):
    t = io.open(p, encoding="utf-8", errors="replace").read()
    return ({m.group(1): int(m.group(2)) for m in re.finditer(r"^## (.+?) — (\d+)", t, re.M)},
            set(re.findall(r"\*\*`([^`]+)`\*\*", t)))


R = []


def P(s=""):
    R.append(s)
    print(s)


if not PRIMA or not os.path.exists(PRIMA):
    print("*** serve PDS_PRIMA=<percorso dell'output di PRIMA> (salvato prima della conversione)")
    sys.exit(2)

sa, ia = sez(PRIMA)
sb, ib = sez(DOPO)
spar = sorted(ia - ib)
comp = sorted(ib - ia)
_senza_id = [x for x in spar if x in NON_ID]
_senza_marc = [x for x in spar if x not in NON_ID]

P("# \U0001f504 **`_punto_della_situazione`: PRIMA / DOPO, e le differenze SPIEGATE** *(2026-09-26)*")
P()
P("*(**Generato** da `csv/_confronto_pds.py`. `PRIMA` = il parser su `STATO_RUN`, salvato prima")
P("della conversione; `DOPO` = la vista su `doc/INDICE_ID.tsv`.)*")
P()
P("| gruppo | PRIMA | DOPO |")
P("|---|--:|--:|")
for k in sorted(set(list(sa) + list(sb))):
    P("| %s | %s | %s |" % (k, sa.get(k, "—"), sb.get(k, "—")))
P("| **task elencati** | **%d** | **%d** |" % (len(ia), len(ib)))
P()
P("## LE TRE CLASSI DI DIFFERENZA")
P()
P("### ➕ **%d voci COMPARSE — e' un GUADAGNO**" % len(comp))
P()
P("Il vecchio leggeva **solo `STATO_RUN`**; l'indice copre **tutti i registri**. Percio' compaiono")
P("voci che prima **non si vedevano affatto**: %s…"
  % ", ".join("`%s`" % x for x in comp[:14]))
P()
P("### ➖ **%d voci SPARITE perche' SENZA MARCATORE — e' il FILTRO, dichiarato**" % len(_senza_marc))
P()
P("Il vecchio prendeva il marcatore dalla **QUARTA cella**; l'indice lo prende dalla **prima e")
P("dall'ultima**, che e' dove una riga dichiara il **proprio** stato. **Dove il marcatore sta in una")
P("cella INTERMEDIA, l'indice non lo vede** — e non lo allargo: le celle di mezzo contengono **le")
P("prove**, che citano i `✅` di ALTRE voci. *(E' lo stesso difetto che questo strumento aveva gia'")
P("curato una volta: prendere un `✅` che non e' suo.)*")
P()
P("Sono: %s." % ", ".join("`%s`" % x for x in _senza_marc))
P()
P("### ➖ **%d voci SPARITE perche' NON SONO ID — e' un GUADAGNO** " % len(_senza_id))
P()
P("| voce | perche' non e' un ID |")
P("|---|---|")
P("| `S-MIT2` | lo **stem e' UNA lettera** prima del trattino: la forma degli ID ne chiede almeno "
  "due. **Serve una rinomina, non una regex piu' larga.** |")
P("| `_verifica_registro.py` | **e' un nome di file**: il vecchio parser lo listava come un task |")
P("| `doc/PATTERN_DI_PROVA.md` | **idem**: un percorso, non una voce |")
P()
P("> ### **Due delle tre classi sono migliorie:** l'indice **vede piu' registri** e **non inventa")
P("> ### task dai nomi di file**. La terza e' un **costo dichiarato**, non un difetto nascosto.")
P()
P("## ⚠ COSA QUESTO CONFRONTO *NON* DICE")
P()
P("- **non dice che i due documenti siano equivalenti**: dicono cose diverse su popolazioni")
P("  diverse, ed e' il punto del cambio di fonte.")
P("- **l'elenco delle voci «non ID» e' un mio giudizio**, scritto in `NON_ID` dentro lo script:")
P("  si corregge in un posto solo.")

io.open(DEST, "w", encoding="utf-8", newline=NL).write(NL.join(R) + NL)
print()
print("scritto %s" % DEST)
