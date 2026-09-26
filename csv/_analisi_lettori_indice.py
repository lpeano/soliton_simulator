r"""**I SEI LETTORI E L'INDICE: che cosa aprono, che cosa estraggono, che campo MANCA.**

**Punto 5 del mandato (Luca, 2026-09-26):** *«i sei lettori leggono SOLO `doc/INDICE_ID.tsv` […]
Se uno ha bisogno di un campo che l'indice non ha, **dimmelo** invece di rileggere il Markdown.»*

> ## ⛔ **LA RISPOSTA E' CHE NESSUNO DEI SEI SI CONVERTE COM'E', e i motivi sono di TRE tipi.**
> **Non e' una difficolta': e' una MISURA**, e sta qui sotto voce per voce.

**MISURATO DALLO SCRIPT** *(non dal mio ricordo)*: quali file ciascuno apre, se **scrive** in un
registro, e quante righe ha. **GIUDIZIO MIO, dichiarato**: che cosa estrae e **quale campo gli
servirebbe**.

**NESSUN RUN, nessun simulatore.**
"""
# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Legge sorgenti e conta.
import io
import os
import re
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _QUI)
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, ".."))
DEST = os.path.join(RADICE, "doc", "LETTORI_INDICE_analisi.md")
NL = chr(10)

REGISTRI = ("STATO_RUN", "RAMIFICAZIONI", "REGISTRO_FISICA", "ASSIOMI", "COMPONENTI_PROMOSSE",
            "PATTERN_DI_PROVA", "INVENTARIO_passo_incompleto", "LISTA_CHIUSA")

# ------------------------------------------------------------------ i sei, col giudizio dichiarato
LETTORI = [
 ("csv/_punto_della_situazione.py", "CONSUMATORE",
  "estrae da ogni riga della coda `id`, `cosa` e **il MARCATORE DI AVANZAMENTO** *(`▶` IN CORSO, "
  "`⏸` IN CODA, `✅` FATTO, `❌` BLOCCATO, `⚠` CON RISERVA)*, e raggruppa per marcatore",
  "**`avanzamento`** — l'indice ha `stato` *(aperto/chiuso/…)*, che **non distingue IN CORSO da IN "
  "CODA**: e' proprio la distinzione che questo documento serve a mostrare"),
 ("csv/_seal_fork/_triage_difetti.py", "CONSUMATORE",
  "prende **le voci `CODICE`** di `RAMIFICAZIONI` e per ciascuna un **ESITO**, e asserisce che "
  "nessuna resti senza esito",
  "**`classe`** *(`CODICE`/`MISURA`/`PROVA`)* **e `esito`** — l'indice non ha ne' l'una ne' l'altro: "
  "sono la CHIAVE del triage"),
 ("csv/_cure_verificate.py", "GENERATORE",
  "legge **`soliton_simulator.py`** *(i flag)* e **SCRIVE** la sezione `CURE VERIFICATE` dentro "
  "`STATO_RUN`: apre il registro **per scriverci**, non per trovare difetti",
  "**`flag`, `default`, `sigillo`, `prova`, `esito`** — cinque campi che l'indice non ha; e "
  "comunque la sua FONTE e' il codice, non il registro"),
 ("csv/_quadro_unico.py", "GENERATORE",
  "legge **`soliton_simulator.py`** e il **driver**, e **SCRIVE** i tre elenchi nel `PUNTO DI "
  "RIPRESA` di `STATO_RUN`",
  "**`in_codice`, `acceso_nei_run`, `default`** — e come sopra: la fonte e' il codice"),
 ("csv/_blob_nelle_voci.py", "MISURA DELLA PROSA",
  "conta **quante voci dei registri portano il BLOB** del codice che le ha prodotte: il suo oggetto "
  "**E' la prosa dei registri**",
  "**nessuno**: convertirlo all'indice **distruggerebbe cio' che misura**. Se leggesse l'indice "
  "misurerebbe l'indice, non i registri"),
 ("csv/_inventario_passo.py", "FUORI PERIMETRO",
  "legge **gli script di `csv/`** e scrive `doc/INVENTARIO_passo_incompleto.md`: **non apre nessuno "
  "dei tre registri per trovare difetti**",
  "**nessuno**: non e' un consumatore dei registri"),
]

R = []


def P(s=""):
    R.append(s)


def misura(rel):
    t = io.open(os.path.join(RADICE, rel), encoding="utf-8", errors="replace").read()
    apre = sorted(set(x for x in REGISTRI if x in t))
    scrive = bool(re.search(r'io\.open\([^)]*(?:CODA|REG|DEST)[^)]*"w"', t)) or \
        bool(re.search(r'\.write\(', t)) and bool(re.search(r'"w"', t))
    return {"righe": len(t.split(NL)), "apre": apre, "scrive": scrive,
            "legge_sorgente": "soliton_simulator.py" in t}


P("# \U0001f50e **I SEI LETTORI E L'INDICE — che cosa aprono, e QUALE CAMPO MANCA**")
P()
P("*(**Generata** da `csv/_analisi_lettori_indice.py`. Punto 5 del mandato del 2026-09-26.)*")
P()
P("> ## ⛔ **NESSUNO DEI SEI SI CONVERTE COM'E', e i motivi sono di TRE tipi**")
P("> **due CONSUMATORI** hanno bisogno di **un campo che l'indice non ha**; **due GENERATORI**")
P("> leggono **il CODICE** e aprono il registro **per SCRIVERCI**; **uno misura la PROSA** dei")
P("> registri *(convertirlo distruggerebbe cio' che misura)* e **uno non tocca i tre registri**.")
P()
P("**Perche' lo dico invece di convertire:** Luca ha scritto *«se uno ha bisogno di un campo che")
P("l'indice non ha, **dimmelo** invece di rileggere il Markdown»*. **Vale per tutti e sei.**")
P()
P("## LA MISURA — dal sorgente, non a memoria")
P()
P("| strumento | righe | registri che NOMINA | legge il CODICE? | scrive? | classe |")
P("|---|--:|---|:--:|:--:|---|")
for rel, classe, _che, _campo in LETTORI:
    m = misura(rel)
    P("| `%s` | %d | %s | %s | %s | **%s** |"
      % (rel.replace("csv/", ""), m["righe"], ", ".join(m["apre"]) or "—",
         "SI" if m["legge_sorgente"] else "—", "SI" if m["scrive"] else "—", classe))
P()
P("## VOCE PER VOCE — che cosa estrae, e che campo servirebbe")
P()
for rel, classe, che, campo in LETTORI:
    P("### `%s` — **%s**" % (rel, classe))
    P()
    P("- **che cosa estrae oggi:** %s" % che)
    P("- **campo che manca all'indice:** %s" % campo)
    P()
P("---")
P()
P("## \U0001f4cc **LA PROPOSTA MINIMA: TRE CAMPI, e due strumenti si convertono**")
P()
P("| campo | a chi serve | da dove si ricava |")
P("|---|---|---|")
P("| **`avanzamento`** *(`IN CORSO`/`IN CODA`/`FATTO`/`BLOCCATO`/`CON RISERVA`)* | "
  "`_punto_della_situazione` | dal **primo marcatore della cella**, che e' esattamente cio' che "
  "quello strumento fa oggi — e porta con se' il suo difetto gia' curato: *conta il primo nel "
  "TESTO, non il primo di una lista* |")
P("| **`classe`** *(`CODICE`/`MISURA`/`PROVA`)* | `_triage_difetti` | dal tag `[EPOCA n · CLASSE]` "
  "delle righe di `RAMIFICAZIONI`, che l'indice oggi **butta via** *(lo togliamo dal titolo per "
  "renderlo leggibile)* |")
P("| **`esito`** | `_triage_difetti` | **NON si ricava**: e' il triage stesso a produrlo. "
  "Servirebbe che il triage **scrivesse** nell'indice, non che lo leggesse — **e questo cambia il "
  "verso del flusso**, quindi lo decide Luca |")
P()
P("**Con `avanzamento` e `classe`, DUE strumenti su sei si convertono** *(`_punto_della_situazione`")
P("e la META' in lettura di `_triage_difetti`)*. **Gli altri quattro NON sono consumatori di")
P("difetti**, e la condizione di fine del mandato — *«nessun consumatore apre piu' i registri per")
P("TROVARE DIFETTI»* — **per loro e' gia' vera oggi**, ma per una ragione diversa da quella")
P("attesa: **non li aprono per quello.**")
P()
P("## ⚠ COSA QUESTA ANALISI *NON* DICE")
P()
P("- **non dice che i quattro fuori perimetro siano a posto**: dice che **non cercano difetti**.")
P("  `_cure_verificate` e `_quadro_unico` **scrivono** dentro `STATO_RUN`, e questo resta un")
P("  accoppiamento: se un giorno l'indice diventasse la fonte anche delle CURE, andrebbero rifatti.")
P("- **la colonna «scrive?» e' un'euristica sul sorgente** *(cerca una `open(..., \"w\")` vicino a un")
P("  nome di registro)*: dice che lo strumento scrive **qualcosa**, non necessariamente nel registro.")
P("- **non ho convertito niente**: `LETTORI-INDICE` resta **APERTA**. Chiuderla adesso vorrebbe dire")
P("  dichiarare finito un lavoro che dipende da una decisione di Luca sui tre campi.")

io.open(DEST, "w", encoding="utf-8", newline=NL).write(NL.join(R) + NL)
print(NL.join(R[:26]))
print()
print("scritto %s" % DEST)
