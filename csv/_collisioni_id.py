r"""**LE COLLISIONI DI ID** — stesso nome, voci DIVERSE. **Misura, non cura.**

**PERCHE' ESISTE:** `A3` non e' una voce, sono **tre** — l'**assioma** di `doc/ASSIOMI.md` *(«niente
si normalizza sul proprio insieme»)*, il fronte **chiuso per dimostrazione** di `RAMIFICAZIONI`
*(«FDT del solo scuotimento»)* e la voce **APERTA** di `STATO_RUN` *(«il disegno esce dalla
dinamica»)*. **Chi cita `A3` non dice quale.**

## CHE COS'E' UNA DEFINIZIONE, e questa e' la scelta che decide tutto il resto

```
DEFINIZIONE   l'ID sta nell'ETICHETTA di una riga di tabella, oppure APRE un'intestazione,
              IN UN REGISTRO GLOBALE
CITAZIONE     l'ID compare nel testo, in qualunque documento
```

## ⚠ LO SPAZIO DEGLI ID **GLOBALI** E' RISTRETTO, E IL PERCHE' E' MISURATO

Al primo giro questo strumento ha trovato **294 collisioni su 317 ID**, cioe' un numero che non
significa niente. **Due cause, entrambe legittime, e vanno DICHIARATE invece di filtrate in
silenzio:**

- **`doc/LISTA_CHIUSA.md` e' una VISTA GENERATA**: ricopia ogni voce dei registri, quindi **duplica
  per costruzione** ogni ID. Non definisce nulla.
- **`doc/REGISTRO_FISICA.md` usa etichette LOCALI**: `A1`, `A2`, `P2`, `V8`, `S9` sono **i criteri di
  UN sigillo** o **i punti di verifica di UNA scheda**, non nomi globali. Il loro nome pieno e'
  *«`V8` della scheda `freno-legge`»*. **Trattarle come ID globali fa collidere ogni sigillo con
  ogni altro.**

**Restano registri GLOBALI:** `ASSIOMI` *(assiomi)*, `RAMIFICAZIONI` *(fronti `A`/`B`/`C`/`D`/`Z`)*,
`STATO_RUN` *(difetti `Dxx`, sospetti `Sxx`, voci di coda)*, `COMPONENTI_PROMOSSE` *(componenti,
citate come «`COMPONENTI_PROMOSSE.md` `B9`»)*, `PATTERN_DI_PROVA` *(gli `STANDARD`)*.

**Si contano le DEFINIZIONI per trovare la collisione, le CITAZIONI per decidere CHI TIENE IL NOME:
la voce piu' citata lo tiene** *(regola di Luca)*.
**⚠ L'attribuzione delle citazioni e' una MISURA DI PROSSIMITA', non un'attribuzione certa:** una
`A3` in prosa **non dice** a quale voce si riferisce. Percio' la rinomina tocca **le DEFINIZIONI**, e
le citazioni si risolvono con l'**alias**.

**NESSUN RUN, nessun simulatore: legge documenti e stampa una tabella.**
"""
# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Conta occorrenze in documenti.
import io
import os
import re
import sys
from collections import Counter, defaultdict

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _QUI)
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, ".."))
DEST = os.path.join(RADICE, "doc", "COLLISIONI_ID.txt")
NL = chr(10)

# ------------------------------------------------------------------ i registri GLOBALI
GLOBALI = ["doc/ASSIOMI.md", "doc/RAMIFICAZIONI.md", "doc/STATO_RUN.md",
           "doc/PATTERN_DI_PROVA.md"]
#   ...e i documenti ESCLUSI dalle definizioni, col motivo (nessuna esclusione in silenzio):
ESCLUSI = [("doc/LISTA_CHIUSA.md", "VISTA GENERATA: ricopia le voci dei registri e le duplica"),
           ("doc/REGISTRO_FISICA.md", "etichette LOCALI a una scheda o a un sigillo (`V8`, `A1`, "
            "`P2`): il nome pieno e' «`V8` della scheda `freno-legge`»"),
           ("doc/INVENTARIO_strumenti.md", "elenca STRUMENTI, non voci"),
           ("doc/COMPONENTI_PROMOSSE.md",
            "etichette LOCALI alle sue tabelle -- `A1`-`A8` le RAGIONI di una promozione, "
            "`B1`-`B10` i FLAG candidati, `C1`-`C5` gli ESPERIMENTI -- e si citano SEMPRE "
            "qualificate: \u00abCOMPONENTI_PROMOSSE.md `B9`\u00bb. **Nell'indice vanno col namespace** "
            "(`COMPONENTI:B9`), che disambigua senza toccare il documento")]
#   Dove la rinomina e' lecita (ordine di Luca):
RINOMINABILI = ["doc/STATO_RUN.md", "doc/RAMIFICAZIONI.md", "doc/REGISTRO_FISICA.md",
                "doc/LISTA_CHIUSA.md"]

# ------------------------------------------------------------------ le SEZIONI che NON definiscono
#   ⚠ UNA TABELLA CHE RIPORTA L'ESITO DELLE VOCI DI UN ALTRO REGISTRO NON LE DEFINISCE: LE CITA.
#   `STATO_RUN` ha una tabella GENERATA con l'esito di ogni voce `CODICE` di `RAMIFICAZIONI`: i suoi
#   `Zxx` sono **rimandi**, non voci nuove. Senza questa esclusione la regola di Luca rinominerebbe
#   **un rimando**, cioe' romperebbe il collegamento fra i due registri invece di disambiguare.
#   Misurato: e' la causa della maggior parte delle collisioni `Zxx`.
SEZ_NON_DEFINISCONO = [
    (r"ESITO DI OGNI VOCE", "tabella GENERATA con l'esito delle voci di RAMIFICAZIONI: le CITA"),
]

# ❌ LA FORMA CORRETTA il 2026-09-26, e due voci vere ne erano ESCLUSE:
#   `A3-DISEGNO` — nata dalla rinomina del `PASSO 1` — ha lo stem di **due** caratteri, e la
#   forma ne chiedeva **tre**; `FRAG1` ha **le cifre in coda** (`[A-Z]{2,}\d{1,3}`) e nessuna
#   alternativa la copriva. **Il collaudo della vista le ha trovate mancanti**, ed e' il
#   motivo per cui il collaudo si scrive prima.
#   ⚠ RESTA FUORI, dichiarato: un'etichetta di UNA SOLA PAROLA MAIUSCOLA senza cifre ne'
#   trattino (`CONTAGIO`) **non e' un ID in questo spazio** — e' la specifica di Luca
#   («nomi MAIUSCOLI col trattino»), e accettarla vorrebbe dire prendere ogni parola
#   maiuscola della prosa. **Quelle voci hanno bisogno di un ID, non di una regex piu'
#   larga.**
FORMA = re.compile(r"(?:[A-Z]\d{1,3}[a-z]?|STANDARD\s+[0-9①-⑳]+"
                   r"|[A-Z][A-Z0-9]{1,}(?:-[A-Z0-9()/]+)+|[A-Z]{2,}\d{1,3})")
SIMBOLI = (u"✅❌⚠❓⛔⏸⭐➤▶❗☑"
           u"\U0001f7e5\U0001f7e7\U0001f7e9\U0001f4cb\U0001f4e4\U0001f6d1\U0001f3af")


def testo(p):
    return io.open(os.path.join(RADICE, p), encoding="utf-8", newline="").read()


def _nudo(s):
    return re.sub(r"[`*#>_~]", "", re.sub("[" + SIMBOLI + "]", " ", s)).strip()


def def_di(riga):
    """L'ID definito da questa riga: etichetta di tabella o apertura d'intestazione."""
    if re.match(r"^#{1,6}\s", riga):
        c = _nudo(riga.lstrip("# "))
    elif riga.startswith("|"):
        c = _nudo(riga.strip().strip("|").split("|")[0])
    else:
        return None
    # ❌ DIFETTO CORRETTO il 2026-09-26: lo STEM era `[A-Z][A-Za-z0-9]{0,4}`, cioe'
    #   **cinque caratteri al massimo**, e un nome piu' lungo col trattino NON veniva
    #   riconosciuto come DEFINIZIONE. **Misurato:** `CONFIG-1`, `POTENZE-1`, `ANCORE-1`,
    #   `INERZIA-1(C)`, `RIPRESA-ARGV`, `REPERTI-IMMUTABILI` finivano fra i «CITATI e MAI
    #   DEFINITI» -- senza fonte, senza stato, senza famiglia -- **mentre sono voci definite
    #   in una riga di tabella.** `SCALE-TW` passava solo perche' `SCALE` ha esattamente
    #   cinque lettere: **il difetto era invisibile per un carattere.**
    m = re.match(r"^([A-Z][A-Z0-9]{1,17}(?:-[A-Z0-9()/]+)+|[A-Z][A-Za-z0-9]{0,4}(?:-[A-Z0-9()/]+)*|STANDARD\s+[0-9①-⑳]+)"
                 r"(?:[\s.,:—-]|$)", c)
    if not m:
        return None
    i = m.group(1).rstrip(".")
    # ⚠ UN'ETICHETTA CHE ELENCA PIU' VOCI NON NE DEFINISCE NESSUNA -- ma il test va fatto
    #   **SUBITO DOPO L'ID**, non sulla cella intera: il primo tentativo cercava un `·` **in
    #   qualunque punto**, e il `·` sta anche dentro `[EPOCA 1 · CODICE]`, che e' in **ogni** riga
    #   di `RAMIFICAZIONI`. **Misurato: le definizioni crollavano da 291 a 130 e i `fronte` da 141
    #   a 8** -- un filtro troppo largo svuota l'indice in silenzio.
    _resto = c[len(m.group(1)):].strip()
    if _resto.startswith("·") and re.match(r"^[A-Z][A-Z0-9\-()/]{2,}",
                                              _resto.lstrip("· ").strip()):
        return None
    return i if FORMA.fullmatch(i) and not re.fullmatch(r"[A-Z]", i) else None


def titolo_di(riga):
    return re.sub(r"\s+", " ", _nudo(riga).strip("| ")).strip()[:120]


# ------------------------------------------------------------------ le DEFINIZIONI
DEF = defaultdict(list)                       # id -> [(file, riga, sezione, titolo)]
SALTATE = []
for p in GLOBALI:
    sez = ""
    for k, riga in enumerate(testo(p).split(NL), 1):
        i = def_di(riga)
        if re.match(r"^#{1,4}\s", riga) and not i:
            sez = titolo_di(riga)[:44]
        _vista = None
        for pat, mot in SEZ_NON_DEFINISCONO:
            if re.search(pat, sez):
                _vista = mot
                break
        if i and _vista:
            SALTATE.append((p, k, sez, i, _vista))
            continue
        if i:
            DEF[i].append((p, k, sez, titolo_di(riga)))

# ------------------------------------------------------------------ le CITAZIONI, per file
FILES = []
for base, _d, ff in os.walk(os.path.join(RADICE, "doc")):
    for f in ff:
        if f.endswith(".md") or f.endswith(".txt"):
            FILES.append(os.path.relpath(os.path.join(base, f), RADICE).replace(os.sep, "/"))
FILES += ["CLAUDE.md", "RELAZIONE_PER_CLAUDE.md"]
CIT = defaultdict(Counter)
for p in sorted(set(FILES)):
    try:
        t = testo(p)
    except Exception:
        continue
    for m in FORMA.finditer(t):
        CIT[m.group(0)][p] += 1


def reg(p):
    return os.path.basename(p).replace(".md", "")


def voci_di(dd):
    """Le VOCI distinte di un ID: una per (registro, sezione) — la stessa voce ripetuta in
    piu' righe dello stesso registro/sezione NON e' una collisione."""
    v = defaultdict(list)
    for p, k, s, t in dd:
        v[(reg(p), s)].append((p, k, t))
    return v


COLL = {i: voci_di(dd) for i, dd in DEF.items() if len(voci_di(dd)) > 1}

R = []


def P(s=""):
    R.append(s)


P("=" * 120)
P("LE COLLISIONI DI ID -- stesso nome, voci DIVERSE   (2026-09-26)")
P("=" * 120)
P()
P("  registri GLOBALI letti (%d): %s" % (len(GLOBALI), ", ".join(reg(p) for p in GLOBALI)))
P("  ESCLUSI dalle definizioni, col motivo:")
for p, mot in ESCLUSI:
    P("    %-32s %s" % (reg(p), mot))
P()
P("  ID definiti: %d      IN COLLISIONE (piu' di una voce): %d" % (len(DEF), len(COLL)))
P("  righe SALTATE perche' in una sezione-VISTA (citano, non definiscono): %d" % len(SALTATE))
for _p, _k, _s, _i, _m in SALTATE[:3]:
    P("      es.  %s:%d  `%s`  -- %s" % (_p, _k, _i, _m))
P("  Una VOCE = una coppia (registro, sezione). La stessa voce ripetuta in piu' righe dello")
P("  stesso registro NON e' una collisione.")
P()
P("=" * 120)
P("LE COLLISIONI, e la PROPOSTA di chi tiene il nome")
P("=" * 120)
for i in sorted(COLL, key=lambda x: (-sum(CIT[x].values()), x)):
    vv = COLL[i]
    tot = sum(CIT[i].values())
    peso = Counter()
    for f, n in CIT[i].items():
        peso[reg(f)] += n
    P()
    P("-" * 120)
    P("`%s`  --  %d voci,  %d citazioni in %d file" % (i, len(vv), tot, len(CIT[i])))
    # ⚠ IL CONTEGGIO PER REGISTRO E' UN PROXY SBAGLIATO PER GLI ASSIOMI E GLI STANDARD:
    #   un assioma e' citato **per nome nudo** in `CLAUDE.md` e in ogni referto, e quelle citazioni
    #   non si attribuiscono a nessun registro. La regola nuda «vince il piu' citato nel proprio
    #   registro» **rinominerebbe l'assioma** -- misurato: `A1` ASSIOMI 8 contro RAMIFICAZIONI 23.
    #   Percio' il genere viene PRIMA del conteggio, ed e' una scelta dichiarata:
    #      ASSIOMI e STANDARD non si rinominano MAI; fra gli altri decide il conteggio.
    # ❌ DIFETTO MIO, CORRETTO: qui c'era `kv[0][0]`, che e' **la prima LETTERA** del nome del
    #   registro, non il registro. Quindi il confronto con ("ASSIOMI", ...) era sempre falso e il
    #   `peso` sempre 0: **l'ordine era quello di lettura dei file**, e gli assiomi risultavano
    #   primi **per caso**, non per la regola. Una regola che sembra funzionare per la ragione
    #   sbagliata e' peggio di una regola assente.
    ord_v = sorted(vv, key=lambda kv: (0 if kv[0] in ("ASSIOMI", "PATTERN_DI_PROVA") else 1,
                                       -peso.get(kv[0], 0), kv[0], kv[1]))
    for n, (rg, sz) in enumerate(ord_v):
        p, k, t = vv[(rg, sz)][0]
        _agire = "TIENE " if n == 0 else ("rinomina" if p in RINOMINABILI else "NON RINOMINABILE")
        P("   %-16s %-22s cit.nel.registro %4d   %s:%d" % (_agire, rg, peso.get(rg, 0), p, k))
        P("        sezione: %s" % (sz or "(nessuna)"))
        P("        titolo : %s" % t[:104])
    P("   citazioni per file (prime 6): %s"
      % ", ".join("%s=%d" % (k2, v) for k2, v in peso.most_common(6)))
P()
P("=" * 120)
P("COSA QUESTO STRUMENTO *NON* DICE")
P("=" * 120)
P("  - **non dice quale voce intendeva chi ha scritto una citazione**: nessun conteggio lo puo'")
P("    dire. Percio' la rinomina tocca **le DEFINIZIONI**, e le citazioni si risolvono con l'ALIAS.")
P("  - **il conteggio per registro NON e' il conteggio per VOCE**: se un registro definisce due")
P("    voci con lo stesso ID, le loro citazioni **non sono separabili**. Dove succede, la scelta")
P("    di chi tiene il nome e' **la sezione, non il numero**, e va decisa a mano.")
P("  - **non vede una voce che nessun registro GLOBALE definisce** (vive solo in prosa).")
P("  - gli ID **locali** a una scheda o a un sigillo (`V8`, `T3`, `Q6`) **non sono in questo")
P("    spazio**: il loro nome pieno include la scheda, e li' non c'e' collisione.")

T = NL.join(R) + NL
io.open(DEST, "w", encoding="utf-8", newline=NL).write(T)
print(T)
