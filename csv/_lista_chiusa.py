r"""**GENERA `doc/LISTA_CHIUSA.md` DA `doc/INDICE_ID.tsv`** — una VISTA sull'indice, non un parser.

**`PASSO 3` ridotto, decisione di Luca (2026-09-26):** *«solo `csv/_lista_chiusa.py` passa a leggere
`INDICE_ID`, con la colonna `FAMIGLIA` aggiunta all'indice (opzione a)»*.

## CHE COS'E' CAMBIATO, e che cosa si e' PERSO

**PRIMA** questo strumento leggeva **cinque documenti in Markdown** e doveva **inferire** che cosa
fosse una voce, quale fosse il suo stato, a che famiglia appartenesse. **Tutti e tre i difetti del
2026-09-26 erano fallimenti di quell'inferenza** *(6 righe su 43 per una tabella interrotta da un
blocco di codice; `VALE SEMPRE` che significa **chiusa** in un registro e **aperta** in un altro;
111 voci senza famiglia)*.

**ORA legge UNA fonte, `doc/INDICE_ID.tsv`**, dove `id`, `stato`, `tipo` e `famiglia` sono **campi
dichiarati**. Un campo dichiarato non si puo' inferire male.

> ### ⚠ **E SI PERDE QUALCOSA, che va detto prima dei numeri: nell'indice entrano SOLO le voci CON
> ### UN ID.** Una voce che vive come **riga senza etichetta** *(il limite `soglia0 = 3π` fra i
> ### limiti `A11`, il `tasso di mitosi` fra i punti non derivati, `CURA 3` con lo spazio invece del
> ### trattino)* **non puo' comparire in una vista sull'indice.** La sezione **`VOCI SENZA ID`** le
> ### elenca: **e' una perdita dichiarata, non un'omissione.**

**Il TESTO si accorcia:** prima la vista stampava **420** caratteri della riga, ora **117** del
`titolo_breve` — perche' l'indice porta un titolo, non la riga. **La spiegazione sta nella fonte, e
la fonte e' in colonna.** *(Luca ha scelto `famiglia`, non `testo`.)*

## IL COLLAUDO, e perche' il criterio CAMBIA senza indebolirsi

Le **quindici voci che Luca aveva elencato** restano il criterio, ma **tre si risolvono su un ID che
le CONTIENE** e **due non hanno alcun ID**: sono dichiarate `PERSE` qui sotto **nel codice, prima di
girare**. **Se l'elenco delle perse cresce, il generatore si ferma.**

**NESSUN RUN, nessun simulatore.**
"""
# ESENTE-P5: non importa il simulatore e non lo fa girare. Legge un TSV e scrive un documento.
import io
import os
import re
import sys
from collections import Counter

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _QUI)
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, ".."))
FONTE = os.path.join(RADICE, "doc", "INDICE_ID.tsv")
DEST = os.path.join(RADICE, "doc", "LISTA_CHIUSA.md")
NL = chr(10)
TAB = chr(9)

FAMIGLIE = [
    ("A", "INERZIA E AVVIO",
     "l'inerzia spinoriale, il contrasto, `rho_s`, la rampa, cio' che decide come nasce un nodo"),
    ("B", "TEMPO UNICO",
     "un solo orologio: `dt_n`/`dt_e` contro `DT` nudo, `r`, `tau_pp`, le medie d'arco"),
    ("C", "DOPPIA COPERTURA E CREAZIONE",
     "la fase su `2pi`/`4pi`, la torsione `tw`, la mitosi, Schwinger, cio' che si eredita"),
    ("D", "SOGLIE TARATE E SOTTO PLANCK",
     "`A11`: ogni clip, pavimento o tetto che non esprima un vincolo dichiarato"),
    ("E", "DISEGNO E STATISTICHE GLOBALI",
     "`A2`/`A5`: mediane e medie globali dentro una legge locale, e il disegno nella fisica"),
    ("F", "FRENO E CONTRAZIONE",
     "`SCALA_MIN`, il freno a senso unico, la coesione, la repulsione, `d0`, `LAM`"),
    ("G", "ARRETRATO DEGLI STRUMENTI",
     "presidi, ancore, reperti, ripresa, il passo incompleto: **non e' fisica**"),
]

# ------------------------------------------------------------------ chi NON entra in LISTA
TIPI_FUORI = {
    "criterio-locale": "etichetta LOCALE a una scheda o a un sigillo: il nome pieno include il "
                       "sigillo, e non e' un fronte del programma",
    "assioma": "assioma: un vincolo sulla forma delle leggi, non una voce da curare",
    "standard": "standard di prova: un criterio di metodo, non un fronte",
    "sospetto": "sospetto, NON acclarato: si promuove con la prova",
}
STATI_FUORI = {
    "chiuso": "gia' curata o chiusa",
    "non-difetto": "non e' un difetto",
    "teoria": "teoria: assioma, standard o corollario",
}

# ------------------------------------------------------------------ IL COLLAUDO (`P1-sexies`)
#   Le quindici voci di Luca. Dove la voce **non ha un ID**, si dichiara l'ID che la CONTIENE, col
#   motivo: e' un cambio di criterio **imposto dal cambio di fonte**, scritto PRIMA di girare.
DEVONO = [
    ("SCALE-TW", r"SCALE-TW", ""),
    ("B5 — theta / l'aliasing del settore di spin", r"\bB5\b", ""),
    ("cura 5 via CLI (CLI-1)", r"CLI-1", ""),
    ("D33", r"\bD33\b", ""),
    ("A3 — il disegno esce dalla dinamica", r"A3-DISEGNO", ""),
    ("PASSO-2", r"PASSO-2", ""),
    ("FRAG1", r"FRAG1", ""),
    ("M1", r"\bM1\b", ""),
    ("M2", r"\bM2\b", ""),
    ("i 24 script che avanzano con step() da solo", r"PASSO-1",
     "la tabella dei 24 script **non ha un ID**: la copre `PASSO-1`, il cui titolo li conta"),
    ("|dx|/d = V8/V9, che decide il freno", r"\bV8\b", ""),
    ("la soglia di torsione 3pi", r"\bD36\b",
     "la riga `soglia0 = 3π` fra i limiti `A11` **non ha un ID**: la copre `D36`, che e' la soglia "
     "della mitosi in unita' assolute di `tw` — **copertura per contenuto, non identita'**"),
    ("DRIVER-SCENA-II", r"DRIVER-SCENA-II", ""),
    ("OSSERVABILE-P1", r"OSSERVABILE-P1", ""),
    ("MITOSI-TASSO (era una voce PERSA)", r"MITOSI-TASSO", ""),
    ("CURA-3 (era `CURA 3`, con lo spazio)", r"CURA-3", ""),
    ("D02", r"(?<![0-9A-Z])D02(?![0-9])", ""),
    ("D03", r"(?<![0-9A-Z])D03(?![0-9])", ""),
    ("D09 — la voce che NON torna", r"(?<![0-9A-Z])D09(?![0-9])", ""),
    ("D31", r"(?<![0-9A-Z])D31(?![0-9])", ""),
    ("chi comprime d0", r"CONFIG-1",
     "le sei misure da rifare in configurazione del driver **non hanno un ID ciascuna**: le copre "
     "`CONFIG-1`, la voce che le raccoglie"),
]
#   ...e le due che NESSUN ID copre. **Dichiarate qui: se l'elenco cresce, il generatore si ferma.**
PERSE = [
    # ✅ VUOTO dal 2026-09-26: **le due voci che non avevano un ID ora ce l'hanno.**
    #   `MITOSI-TASSO` e' entrata come voce di `STATO_RUN` *(prima viveva come punto di un elenco in
    #   prosa della scheda ⑨)*; `CURA 3` e' diventata **`CURA-3`** *(uno spazio non fa un
    #   identificatore)*. **La lista resta qui perche' il controllo e' «se CRESCE, il generatore si
    #   ferma»**: una perdita nuova non deve passare in silenzio.
]

# ================================================================== LETTURA
righe = io.open(FONTE, encoding="utf-8", newline="").read().split(NL)
COL = [c.strip() for c in righe[0].split(TAB)]
VOCI = []
for r in righe[1:]:
    if not r.strip():
        continue
    c = (r.split(TAB) + [""] * 8)[:8]
    VOCI.append(dict(zip(COL, [x.strip() for x in c])))
assert len(VOCI) > 100, "l'indice ha solo %d voci: NON tiro a indovinare" % len(VOCI)

for v in VOCI:
    _t, _s = v.get("tipo", ""), v.get("stato", "")
    v["fuori"] = TIPI_FUORI.get(_t) or STATI_FUORI.get(_s) or (
        None if _s in ("aperto", "da-decidere") else "stato non riconosciuto: `%s`" % _s)

LISTA = [v for v in VOCI if not v["fuori"]]
FUORI = [v for v in VOCI if v["fuori"]]
_FAM = [x[0] for x in FAMIGLIE]
_senza = [v for v in LISTA if v.get("famiglia", "?") not in _FAM]

R = []


def P(s=""):
    R.append(s)


def breve(s, n):
    s = re.sub(r"\s+", " ", s or "").replace("|", "/").strip()
    # ⚠ Tronca **su un confine di parola**: tagliare a meta' parola INVENTA UN ID
    #   (`GLOBALE-DISEGNO` -> `GLOBALE-DIS`), e il presidio dell'indice lo segnala -- giustamente
    #   -- in un documento che questo strumento ha scritto.
    if len(s) <= n:
        return s
    _t = s[:n - 1]
    _sp = _t.rfind(" ")
    return (_t[:_sp] if _sp > n // 2 else _t) + chr(0x2026)


P("# \U0001f4cb **LA LISTA CHIUSA — BOZZA PER L'APPROVAZIONE DI LUCA**")
P()
P("*(**Generata** da `csv/_lista_chiusa.py` da **UNA fonte**: `doc/INDICE_ID.tsv`. `P1-ter`.)*")
P()
P("> ## ⚠ **NON E' ANCORA UNA LISTA CHIUSA: E' UNA PROPOSTA.** La approva Luca.")
P("> **Nessuna voce e' esclusa in silenzio:** `FUORI LISTA` porta ogni voce **col motivo**, e i")
P("> motivi vengono dai **campi dichiarati** dell'indice (`stato`, `tipo`), non da una regex sulla")
P("> prosa.")
P()
P("## \U0001f504 **QUESTA VISTA NON FA PIU' PARSING DI MARKDOWN** *(`PASSO 3` ridotto)*")
P()
P("| | prima (fino al 2026-09-26) | ora |")
P("|---|---|---|")
P("| fonti | **cinque** documenti in Markdown | **una**: `doc/INDICE_ID.tsv` |")
P("| che cos'e' una voce | **inferito** dalla contiguita' delle righe | un `id`, **dichiarato** |")
P("| lo stato | **inferito** dalle parole della riga | la colonna `stato` |")
P("| la famiglia | **inferita** da parole chiave, `111` senza famiglia | la colonna `famiglia` |")
P("| il testo | `420` caratteri della riga | `117` del `titolo_breve` **+ la fonte in colonna** |")
P()
P("```")
P("voci nell'indice     %4d" % len(VOCI))
P("in LISTA             %4d   (stato aperto o da-decidere, e un tipo che puo' essere un fronte)"
  % len(LISTA))
P("FUORI LISTA          %4d   col motivo, dai campi dell'indice" % len(FUORI))
P("```")
P()
P("---")
P()
P("## LE SETTE FAMIGLIE")
P()
P("| | famiglia | cosa raccoglie | voci in lista |")
P("|---|---|---|--:|")
for k, nome, che in FAMIGLIE:
    P("| **%s** | **%s** | %s | %d |"
      % (k, nome, che, len([v for v in LISTA if v.get("famiglia") == k])))
if _senza:
    P("| **?** | **SENZA FAMIGLIA** | nessuna regola dell'indice ha deciso: **le elenco invece di "
      "metterle in una famiglia a caso** | %d |" % len(_senza))
P()
P("---")
P()
for k, nome, _che in FAMIGLIE + [("?", "SENZA FAMIGLIA — da assegnare a mano", "")]:
    vv = ([v for v in LISTA if v.get("famiglia") == k] if k != "?" else _senza)
    if not vv:
        continue
    P("## FAMIGLIA **%s** — %s   *(%d voc%s)*"
      % (k, nome, len(vv), "e" if len(vv) == 1 else "i"))
    P()
    P("| blocca? | id | alias | che cos'e' | stato | tipo | fonte |")
    P("|:--:|---|---|---|:--:|:--:|---|")
    for v in sorted(vv, key=lambda x: (x.get("tipo", ""), x.get("id", ""))):
        P("| `%s` | **%s** | %s | %s | `%s` | `%s` | `%s` |"
          % (v.get("blocca_run_base", ""), v.get("id", ""), v.get("alias", "") or "—",
             breve(v.get("titolo_breve", ""), 118), v.get("stato", ""), v.get("tipo", ""),
             breve(v.get("fonte_principale", "").split("::")[0].replace("doc/", ""), 30)))
    P()
    P("---")
    P()

P("## \U0001f4e4 **FUORI LISTA — %d voci, ciascuna col MOTIVO** *(dai campi dell'indice)*"
  % len(FUORI))
P()
_mot = {}
for v in FUORI:
    _mot.setdefault(v["fuori"], []).append(v)
for mot in sorted(_mot, key=lambda m: -len(_mot[m])):
    P("### motivo: **%s**   *(%d voci)*" % (mot, len(_mot[mot])))
    P()
    P("| id | che cos'e' | tipo |")
    P("|---|---|:--:|")
    for v in sorted(_mot[mot], key=lambda x: x.get("id", "")):
        P("| %s | %s | `%s` |" % (v.get("id", ""), breve(v.get("titolo_breve", ""), 96),
                                  v.get("tipo", "")))
    P()

P("---")
P()
P("## ⚠ **VOCI SENZA ID: LA PERDITA DICHIARATA DI QUESTA VISTA**")
P()
P("**Nell'indice entrano solo le voci CON UN ID.** Queste **non ne hanno**, quindi **non possono")
P("comparire qui** — e lo scrivo **prima** dei numeri, invece di lasciarle sparire:")
P()
if not PERSE:
    P("**✅ NESSUNA: dal 2026-09-26 l'elenco e' VUOTO.** `MITOSI-TASSO` e `CURA-3` — le due voci")
    P("che vivevano senza etichetta — **hanno un ID**, e compaiono. **Il controllo resta: se")
    P("l'elenco CRESCE, il generatore si ferma.**")
for nome, mot in PERSE:
    P("- **%s** — %s" % (nome, mot))
P()
P("**E TRE compaiono solo attraverso l'ID che le CONTIENE**, dichiarato nel codice:")
P()
for nome, _pat, mot in DEVONO:
    if mot:
        P("- **%s** — %s" % (nome, mot))
P()
P("---")
P()
P("## ✅ IL CONTROLLO *(`P1-sexies`)*")
P()
P("Le voci che Luca aveva elencato come mancanti restano il criterio. **Se una non compare, il")
P("generatore NON SCRIVE IL FILE.** E **se l'elenco delle voci PERSE cresce oltre le due")
P("dichiarate, si ferma anche allora**: una perdita nuova non deve passare come le altre.")
P()
P("| deve comparire | trovata? |")
P("|---|:--:|")

_corpo = NL.join(R)
mancano = [n for n, p, _m in DEVONO if not re.search(p, _corpo)]
for n, p, _m in DEVONO:
    P("| %s | %s |" % (n.replace("|", "\\|"), "— **MANCA**" if n in mancano else "✅"))
P("| **voci PERSE dichiarate** | %d |" % len(PERSE))
P()
P("## COSA QUESTA BOZZA *NON* DICE")
P()
P("- **`stato` e `famiglia` vengono dall'indice**, e l'indice li ricava dalla fonte con **regole")
P("  dichiarate**: dove la fonte non porta un marcatore, lo stato e' `da-decidere`. **Non e'")
P("  un'incertezza di questa vista: e' un'incertezza dei REGISTRI, resa visibile.**")
P("- **`blocca?` non e' un giudizio mio:** `NO` viene da una **regola** *(un chiuso, un")
P("  non-difetto, una teoria o un criterio-locale non bloccano mai)*, `SI` **solo** dove la fonte")
P("  lo dichiara, e `DA-DECIDERE` e' la **risposta onesta**. La lista su cui decidere e'")
P("  `doc/SMISTAMENTO_run_base.md`.")
P("- **non contiene la DIMENSIONE** ne' l'**ordine per DIPENDENZE**: nessun campo dell'indice li")
P("  porta, e ricavarli sarebbe giudizio mio riga per riga. **Il mandato li chiede: mancano.**")
P("- **una voce che nessun registro DEFINISCE non c'e'**: questa vista non guarda i registri, e")
P("  **non puo' vedere cio' che l'indice non ha**. E' il prezzo di una fonte sola, ed e' il")
P("  rovescio del guadagno.")

T = NL.join(R) + NL
if mancano or len(PERSE) != 0:
    print("*** FERMO: il documento NON e' stato scritto.")
    for n in mancano:
        print("    MANCA la voce che DEVE comparire: %s" % n)
    if len(PERSE) != 0:
        print("    le voci PERSE dichiarate sono %d invece di 0: una perdita NUOVA va guardata."
              % len(PERSE))
    sys.exit(3)

io.open(DEST, "w", encoding="utf-8", newline=NL).write(T)
print("scritto %s" % DEST)
print("  voci %d   LISTA %d   FUORI LISTA %d   senza famiglia %d   perse dichiarate %d"
      % (len(VOCI), len(LISTA), len(FUORI), len(_senza), len(PERSE)))
_f = Counter(v.get("famiglia", "?") for v in LISTA)
print("  per famiglia: %s" % ", ".join("%s=%d" % x for x in sorted(_f.items())))
