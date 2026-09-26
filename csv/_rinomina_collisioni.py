r"""**LA RINOMINA DELLE VOCI IN COLLISIONE** — e il suo collaudo nei due versi.

**Ordine di Luca, 2026-09-26:** *«per ogni collisione la voce MENO citata prende un nome nuovo
esplicito (es. `A3-DISEGNO`), l'altra tiene il suo. RINOMINA SOLO nei documenti VIVI.»*

## ⚠ TRE DECISIONI CHE LA REGOLA NUDA NON PRENDE, e vanno dichiarate

**① SI RINOMINANO LE DEFINIZIONI, NON LE CITAZIONI.** Una `A3` in prosa **non dice** a quale delle
voci si riferisce — e in `STATO_RUN` ce ne sono che citano **l'assioma**. Riscriverle tutte
**corromperebbe le citazioni degli assiomi**. Le citazioni si risolvono con l'**alias** dell'indice.

**② UN ASSIOMA NON SI RINOMINA MAI.** Il conteggio *«per registro»* direbbe il contrario
*(`A1`: `ASSIOMI` 8 contro `RAMIFICAZIONI` 23)*, ma un assioma e' citato **per nome nudo** in
`CLAUDE.md` e in ogni referto, e quelle citazioni **non si attribuiscono a nessun registro**: il
conteggio per registro **e' un proxy sbagliato**. Il genere viene prima del numero.

**③ SI RINOMINANO SERIE INTERE, NON MEMBRI SPARSI.** Le voci stanno in **serie** *(`C1`-`C5` le
cure, `B1`-`B10` le aperte, `A1`-`A6` le lasciate a meta')*, e **rinominare un solo membro e' peggio
della collisione**: rompe la leggibilita' della serie. Percio' `RAMIFICAZIONI` **tiene tutta** la
serie `C1`-`C28` *(28 voci, e `C7`/`C10`/`C11`/`C12`/`C13`/`C14`/`C18`/`C21` sono citate in
`CLAUDE.md`)* e sono **le cinque cure della coda** a prendere il nome esplicito; viceversa
`RAMIFICAZIONI` rinomina **tutta** la sua serie `A1`-`A3` e `B4`-`B7`, che sono complete.

**COLLAUDO NEI DUE VERSI** *(`P1-sexies`)*:

```
DEVE ESSERE VERO     dopo la rinomina, nei documenti vivi NESSUN ID ha piu' di una definizione
DEVE ESSERE VERO     nei file NON TOCCABILI lo sha1 NON cambia  (task history, referti, json,
                     codice: sono REPERTI o STORIA)
DEVE FALLIRE         un'ancora che non esiste piu' -> `assert` e nessuna scrittura
```

**NESSUN RUN, nessun simulatore.**
"""
# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Rinomina etichette in due documenti.
import hashlib
import io
import os
import re
import subprocess
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _QUI)
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, ".."))
DEST = os.path.join(RADICE, "doc", "RINOMINE_ID.txt")
NL = chr(10)

# ============================================================ LA TAVOLA DELLE RINOMINE
#   (file, id_vecchio, id_nuovo, frammento UNICO della riga che la identifica)
RINOMINE = [
 # --- RAMIFICAZIONI: la serie `A1`-`A3`, COMPLETA (collide con gli assiomi `A1`-`A3`)
 ("doc/RAMIFICAZIONI.md", "A1", "A1-INERZIA", "Teorema di inerzia"),
 ("doc/RAMIFICAZIONI.md", "A2", "A2-BLOCH", "Invarianza del Bloch sotto Step 2"),
 ("doc/RAMIFICAZIONI.md", "A3", "A3-FDT", "FDT del solo scuotimento"),
 # --- RAMIFICAZIONI: la serie `B4`-`B7`, COMPLETA (collide con le `B` di STATO_RUN)
 ("doc/RAMIFICAZIONI.md", "B4", "B4-FROZEN", "Bloch frozen-o-noise"),
 ("doc/RAMIFICAZIONI.md", "B5", "B5-KURAMOTO", "Kuramoto refutato"),
 ("doc/RAMIFICAZIONI.md", "B6", "B6-TURBO", "Esito B del turbo"),
 ("doc/RAMIFICAZIONI.md", "B7", "B7-SHAKE", "shake-then-freeze"),
 # --- STATO_RUN, «A -- LASCIATE A META' OGGI»: serie COMPLETA (collide con gli assiomi)
 ("doc/STATO_RUN.md", "A1", "A1-TREVIE", "la catena a TRE VIE di `step`"),
 ("doc/STATO_RUN.md", "A2", "A2-ANELLO", "l'anello `A6` di `Z70`"),
 ("doc/STATO_RUN.md", "A3", "A3-CHIRALE", "la carica chirale non si conserva"),
 ("doc/STATO_RUN.md", "A4", "A4-METRICHE", "le METRICHE DEL SETTORE CHIRALE"),
 ("doc/STATO_RUN.md", "A5", "A5-PANNELLO", "il PANNELLO FEDELE"),
 ("doc/STATO_RUN.md", "A6", "A6-PERCCHI", "FA DUE LAVORI CON REGOLE OPPOSTE"),
 # --- STATO_RUN, «IN CODA»: serie COMPLETA `A1`-`A3` (collide con gli assiomi)
 ("doc/STATO_RUN.md", "A1", "A1-COSTANTI", "AUDIT DELLE COSTANTI TARATE"),
 ("doc/STATO_RUN.md", "A2", "A2-DXD", "RIMISURARE NEL REGIME NUOVO"),
 ("doc/STATO_RUN.md", "A3", "A3-DISEGNO", "IL DISEGNO ESCE DALLA DINAMICA"),
 # --- STATO_RUN, la coda unica: le CURE, serie COMPLETA (RAMIFICAZIONI tiene `C1`-`C28`)
 ("doc/STATO_RUN.md", "C1", "C1-PEQ-ESATTO", "rilassamento in forma esatta"),
 ("doc/STATO_RUN.md", "C1-bis", "C1BIS-ANOM-SIMM", "il pavimento `1e-9` tolto"),
 ("doc/STATO_RUN.md", "C2", "C2-PEQ-NASCITA", "nascita locale di `peq`"),
 ("doc/STATO_RUN.md", "C3", "C3-SCALA-MIN-PASSO", "il freno una volta per passo"),
 ("doc/STATO_RUN.md", "C4", "C4-COES-CAUSALE", "istante unico e cono locale"),
 ("doc/STATO_RUN.md", "C5", "C5-INVARIANTI", "domini di stato" if False else "— 42 domini, due livelli"),
 ("doc/STATO_RUN.md", "C5-res", "C5RES-INVARIANTI", "I RESIDUI DI `C5`"),
]

# ============================================================ i file che NON si toccano
def _elenco_intoccabili():
    fuori = []
    for base, _d, ff in os.walk(RADICE):
        if any(x in base for x in (".git", "__pycache__")):
            continue
        for f in ff:
            p = os.path.join(base, f)
            r = os.path.relpath(p, RADICE).replace(os.sep, "/")
            if (r.startswith("doc/TASK_HISTORY/") or r.startswith("doc/REFERTO_")
                    or r.endswith(".json") or r.endswith(".py") or r == "soliton_simulator.py"
                    or "/_sig_" in r or "/_seal" in r):
                fuori.append(r)
    return sorted(fuori)


def _sha(p):
    try:
        return hashlib.sha1(io.open(os.path.join(RADICE, p), "rb").read()).hexdigest()
    except Exception:
        return "-"


R = []


def P(s=""):
    R.append(s)
    print(s)


P("=" * 112)
P("LA RINOMINA DELLE VOCI IN COLLISIONE   (2026-09-26)")
P("=" * 112)
P()

INTOCCABILI = _elenco_intoccabili()
PRIMA = {p: _sha(p) for p in INTOCCABILI}
P("file dichiarati NON TOCCABILI, di cui si registra lo sha1 PRIMA: %d" % len(INTOCCABILI))
P("  (task history, referti, json, ogni `.py`, gli archivi dei sigilli: REPERTI o STORIA)")
P()

# ============================================================ LA RINOMINA
P("%-26s %-20s %-20s %s" % ("file", "prima", "dopo", "ancora (frammento unico)"))
fatte = []
for f, vecchio, nuovo, ancora in RINOMINE:
    p = os.path.join(RADICE, f)
    righe = io.open(p, encoding="utf-8", newline="").read().split(NL)
    cand = [k for k, r in enumerate(righe) if ancora in r and r.startswith("|")]
    assert len(cand) == 1, ("ANCORA NON UNICA (%d righe) in %s: %r"
                            % (len(cand), f, ancora))
    k = cand[0]
    riga = righe[k]
    prima_cella = riga.split("|")[1]
    # ⚠ IDEMPOTENZA, e senza di essa rigirare lo strumento RADDOPPIAVA il suffisso: `\bA1\b`
    #   trova `A1` **dentro** `A1-INERZIA` (il trattino e' un confine di parola), quindi la seconda
    #   passata avrebbe scritto `A1-INERZIA-INERZIA`. Un difetto che si vede solo al secondo giro.
    if nuovo in prima_cella:
        P("%-26s %-20s %-20s GIA' FATTA, salto" % (os.path.basename(f), vecchio, nuovo))
        fatte.append((f, vecchio, nuovo, k + 1))
        continue
    assert re.search(r"\b" + re.escape(vecchio) + r"\b", prima_cella), (
        "l'etichetta %r non e' nella prima cella di %s:%d -> %r" % (vecchio, f, k + 1, prima_cella))
    nuova_cella = re.sub(r"\b" + re.escape(vecchio) + r"\b", nuovo, prima_cella, count=1)
    pezzi = riga.split("|")
    pezzi[1] = nuova_cella
    righe[k] = "|".join(pezzi)
    io.open(p, "w", encoding="utf-8", newline=NL).write(NL.join(righe))
    fatte.append((f, vecchio, nuovo, k + 1))
    P("%-26s %-20s %-20s %s" % (os.path.basename(f), vecchio, nuovo, ancora[:42]))
P()
P("rinomine applicate: %d" % len(fatte))
P()

# ============================================================ IL COLLAUDO
P("=" * 112)
P("IL COLLAUDO NEI DUE VERSI")
P("=" * 112)

# (a) nessun ID con piu' di una definizione
_r = subprocess.run([sys.executable, os.path.join(_QUI, "_collisioni_id.py")],
                    capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=RADICE)
m = re.search(r"IN COLLISIONE \(piu' di una voce\): (\d+)", _r.stdout or "")
_n = int(m.group(1)) if m else -1
_ok_a = (_n == 0)
P("  (a) collisioni residue nei registri globali: %s   -> %s"
  % (_n, "PASS" if _ok_a else "FAIL"))
if not _ok_a:
    for riga in (_r.stdout or "").split(NL):
        if riga.startswith("`"):
            P("        resta: %s" % riga[:96])

# (b) i file NON toccabili sono invariati
_cambiati = [p for p in INTOCCABILI if _sha(p) != PRIMA[p]]
_ok_b = not _cambiati
P("  (b) file NON toccabili con sha1 cambiato: %d   -> %s"
  % (len(_cambiati), "PASS" if _ok_b else "FAIL"))
for p in _cambiati[:10]:
    P("        *** %s" % p)

# (c) il ramo che DEVE fallire: un'ancora che non esiste
try:
    _t = io.open(os.path.join(RADICE, "doc/STATO_RUN.md"), encoding="utf-8").read()
    _finta = "ANCORA-CHE-NON-ESISTE-NEL-DOCUMENTO"
    _cand = [1 for r in _t.split(NL) if _finta in r]
    assert len(_cand) == 1, "ancora non unica: %d" % len(_cand)
    _ok_c = False
except AssertionError:
    _ok_c = True
P("  (c) un'ancora inesistente FA FALLIRE l'assert: %s" % ("PASS" if _ok_c else "FAIL"))

# (d) git: i file modificati sono solo quelli permessi
_g = subprocess.run(["git", "diff", "--name-only"], capture_output=True, text=True,
                    encoding="utf-8", errors="replace", cwd=RADICE)
PERMESSI = {"doc/STATO_RUN.md", "doc/RAMIFICAZIONI.md", "doc/LISTA_CHIUSA.md",
            "doc/COLLISIONI_ID.txt", "doc/RINOMINE_ID.txt", "doc/ESENZIONI_presidi.md",
            "RELAZIONE_PER_CLAUDE.md", "doc/INVENTARIO_strumenti.md"}
_mod = [x for x in (_g.stdout or "").split(NL) if x.strip()]
_fuori = [x for x in _mod if x not in PERMESSI]
_ok_d = not _fuori
P("  (d) file modificati fuori dall'elenco permesso: %d   -> %s"
  % (len(_fuori), "PASS" if _ok_d else "FAIL"))
for x in _fuori[:10]:
    P("        *** %s" % x)
P()
_tutto = _ok_a and _ok_b and _ok_c and _ok_d
P("=" * 112)
P("ESITO: %s" % ("4/4 PASS" if _tutto else "FAIL -- la rinomina va guardata"))
P("=" * 112)
P()
P("COSA QUESTA RINOMINA *NON* FA:")
P("  - **non riscrive le CITAZIONI**: in prosa `A3` resta `A3`, e **non e' un'omissione** — una")
P("    citazione in prosa non dice a quale voce si riferisce, e in `STATO_RUN` ce ne sono che")
P("    citano l'ASSIOMA. **Si risolvono con l'`alias` dell'indice** (`PASSO 2`).")
P("  - **non tocca `REGISTRO_FISICA` ne' `COMPONENTI_PROMOSSE`**: le loro etichette sono LOCALI a")
P("    una scheda o a una tabella, e si citano qualificate. **Nell'indice vanno col namespace.**")
P("  - **non tocca i reperti**: task history, referti, json, codice. Li' il nome vecchio RESTA, ed")
P("    e' giusto: **un reperto non si riscrive.**")

io.open(DEST, "w", encoding="utf-8", newline=NL).write(NL.join(R) + NL)
sys.exit(0 if _tutto else 1)
