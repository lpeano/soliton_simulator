r"""**CHI LEGGE GLI ID E I REGISTRI** — l'inventario che precede il `PASSO 3`.

**Ordine di Luca, 2026-09-26:** *«gli strumenti che oggi leggono ID o tabelle di difetti passano a
leggere `doc/INDICE_ID` come UNICA fonte. Prima un INVENTARIO di questi strumenti (quali, cosa
leggono oggi), poi la riscrittura, ciascuno col suo collaudo nei due versi.»*

## ⚠ «81 SCRIPT NOMINANO UN REGISTRO» NON E' IL PERIMETRO, ed e' il punto dell'inventario

Quattro classi, e **tre non si toccano**:

```
COPIA DEL SIMULATORE   `_sim_*.py`, `_old_sim_*.py`: 7000-10500 righe, nominano un documento in un
                       COMMENTO. Sono REPERTI: non si toccano.
SCRITTORE UNA VOLTA    `_zNNN_*.py`: hanno AGGIUNTO una voce a un registro e hanno gia' girato.
                       Non leggono per trovare difetti.
IMPORTATORE            `_indice_id.py`, `_collisioni_id.py`, `_rinomina_collisioni.py`: **DEVONO**
                       leggere il Markdown, perche' sono cio' che COSTRUISCE l'indice. La regola
                       «nessun parsing di tabelle» vale per i CONSUMATORI, non per l'importatore.
LETTORE                gli altri: leggono un registro per TROVARE voci. **Sono questi il PASSO 3.**
```

**NESSUN RUN, nessun simulatore.**
"""
# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Classifica script per contenuto.
import io
import os
import re
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _QUI)
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, ".."))
DEST = os.path.join(RADICE, "doc", "INVENTARIO_lettori_id.txt")
NL = chr(10)

REG = re.compile(r"STATO_RUN\.md|RAMIFICAZIONI\.md|ASSIOMI\.md|COMPONENTI_PROMOSSE\.md"
                 r"|LISTA_CHIUSA|PATTERN_DI_PROVA|REGISTRO_FISICA\.md|INVENTARIO_passo_incompleto")
IMPORTATORI = ["_indice_id.py", "_collisioni_id.py", "_rinomina_collisioni.py"]
R = []


def P(s=""):
    R.append(s)
    print(s)


def classe(rel, s):
    b = os.path.basename(rel)
    if re.match(r"_(sim|old_sim)", b) or b.endswith("._sim.py") or "_sim_" in b:
        return "copia-simulatore"
    if b in IMPORTATORI:
        return "IMPORTATORE"
    if re.match(r"_z\d+_", b):
        return "scrittore-una-volta"
    return "LETTORE"


def cosa_legge(s):
    fuori = sorted(set(REG.findall(s)))
    return ", ".join(x.replace(".md", "") for x in fuori)


FILE = []
for base, _d, ff in os.walk(os.path.join(RADICE, "csv")):
    if "__pycache__" in base:
        continue
    for f in ff:
        if not f.endswith(".py"):
            continue
        rel = os.path.relpath(os.path.join(base, f), RADICE).replace(os.sep, "/")
        s = io.open(os.path.join(RADICE, rel), encoding="utf-8", errors="replace").read()
        if not REG.search(s):
            continue
        # legge DAVVERO un registro, o lo nomina in un commento?
        # ⚠ EURISTICA CORRETTA: la prima versione cercava il nome del registro ACCANTO a un
        #   `open(`, e perdeva il caso NORMALE -- `CODA = os.path.join(RADICE, "doc",
        #   "STATO_RUN.md")` e poi `io.open(CODA)`. **Misurato: perdeva `_triage_difetti.py` e
        #   `_punto_della_situazione.py`, che sono due LETTORI VERI**, cioe' proprio il perimetro
        #   del `PASSO 3`. Un inventario che sbaglia il perimetro fa sbagliare la stima.
        _pat = ("STATO_RUN|RAMIFICAZIONI|ASSIOMI|COMPONENTI_PROMOSSE|LISTA_CHIUSA"
                "|PATTERN_DI_PROVA|REGISTRO_FISICA|INVENTARIO_passo")
        apre = (bool(re.search(r"os\.path\.join\([^\n]{0,70}(?:" + _pat + ")", s))
                or bool(re.search(r"(?:open|read_text)\([^\n]{0,80}(?:" + _pat + ")", s))
                or bool(re.search(r"(?:SORGENTE|FONTI|REGOLE|REGISTRI|GLOBALI|VIVI)"
                                  r"\s*=\s*[\[\{\(]", s)))
        FILE.append({"file": rel, "classe": classe(rel, s), "apre": apre,
                     "legge": cosa_legge(s), "righe": len(s.split(NL))})

P("=" * 112)
P("CHI LEGGE GLI ID E I REGISTRI -- l'inventario che precede il `PASSO 3`   (2026-09-26)")
P("=" * 112)
P()
_cl = {}
for x in FILE:
    _cl.setdefault(x["classe"], []).append(x)
P("  script che NOMINANO un registro: %d" % len(FILE))
for k in ("LETTORE", "IMPORTATORE", "scrittore-una-volta", "copia-simulatore"):
    P("     %-22s %3d" % (k, len(_cl.get(k, []))))
P()
P("  ⚠ IL PERIMETRO DEL `PASSO 3` SONO I **LETTORI** CHE APRONO DAVVERO UN REGISTRO: %d"
  % len([x for x in _cl.get("LETTORE", []) if x["apre"]]))
P()
for k in ("LETTORE", "IMPORTATORE"):
    P("-" * 112)
    P("%s" % k)
    P("-" * 112)
    P("%-42s %5s %6s  %s" % ("file", "righe", "apre?", "che registri nomina"))
    for x in sorted(_cl.get(k, []), key=lambda y: (not y["apre"], y["file"])):
        P("%-42s %5d %6s  %s" % (x["file"], x["righe"], "SI" if x["apre"] else "-", x["legge"][:52]))
    P()
P("-" * 112)
P("NON SI TOCCANO (e il conteggio dice perche' «81 file» non era il perimetro)")
P("-" * 112)
for k in ("scrittore-una-volta", "copia-simulatore"):
    P("  %-22s %3d file  -- %s"
      % (k, len(_cl.get(k, [])),
         "hanno gia' girato: aggiungevano una voce" if k.startswith("scrittore")
         else "REPERTI da 7000-10500 righe: nominano un documento in un commento"))
P()
P("=" * 112)
P("COSA QUESTO INVENTARIO *NON* DICE")
P("=" * 112)
P("  - **`apre?` e' un'euristica sul sorgente**, non un'esecuzione: dice che lo script apre un")
P("    registro o dichiara un elenco di fonti. **Un lettore che costruisce il path a pezzi non lo")
P("    vedo.**")
P("  - **non dice quanto costa riscrivere ciascuno**: la stima sta nella relazione, e **la parte")
P("    cara e' il collaudo nei due versi**, uno per strumento.")
P("  - **gli IMPORTATORI restano a leggere il Markdown**, ed e' una precisazione di merito: sono")
P("    cio' che COSTRUISCE l'indice. La regola vale per i **consumatori**.")

io.open(DEST, "w", encoding="utf-8", newline=NL).write(NL.join(R) + NL)
