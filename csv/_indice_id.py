r"""**GENERA `doc/INDICE_ID.tsv`** — l'indice di TUTTI gli ID, e `doc/INDICE_ID_ESCLUSI.tsv`.

**Ordine di Luca, 2026-09-26** *(`PASSO 2`)*: un **INDICE**, non un registro completo. Le
spiegazioni lunghe restano nei documenti; qui sta **dove vive** ogni ID e **che cos'e'**.

## LE COLONNE

```
id | alias | titolo_breve | fonte_principale | stato | blocca_run_base | tipo
```

**`stato`** ∈ `aperto` `chiuso` `non-difetto` `teoria` `da-decidere`
**`blocca_run_base`** ∈ `SI` `NO` `DA-DECIDERE`
**`tipo`** ∈ `difetto` `assioma` `standard` `presidio` `misura` `altro` **+ quattro che aggiungo**:
`sospetto`, `fronte`, `cura`, `criterio-locale`. **Li aggiungo invece di schiacciarli su `altro`**:
un `Sxx` marcato `difetto` sarebbe **falso** *(un sospetto non e' acclarato)*, e marcato `altro`
sarebbe **nascosto**.

## ⚠ DUE REGOLE CHE TENGO STRETTE, e sono di Luca

**① LO STATO SI PRENDE DALLA FONTE. Dove e' ambiguo: `da-decidere`. NON SI INDOVINA.**
**② `blocca_run_base` E' `DA-DECIDERE` quasi sempre**, perche' **nessun documento lo dichiara**:
vale `SI` solo dove il testo dice *«bloccante»* o *«prima di qualunque giro lungo»*, e `NO` dove la
voce e' chiusa, e' teoria o non e' un difetto. **Riempire questa colonna a intuito sarebbe il
difetto di oggi moltiplicato per trecento.**

## GLI ID **LOCALI** VANNO COL NAMESPACE, NON SI ESCLUDONO

`V8` della scheda `freno-legge`, `A1` dei criteri di un sigillo, `B9` di `COMPONENTI_PROMOSSE`
entrano come **`REGISTRO_FISICA:V8`**, **`COMPONENTI:B9`**. La **forma nuda** diventa un `alias`
**solo se un registro solo la definisce**: se due la definiscono, **nessun alias**, e una citazione
nuda resta **AMBIGUA** — cosa che il presidio **dice**, invece di scegliere per conto proprio.

## NIENTE ESCLUSI INVISIBILI

Ogni forma trovata dallo sweep che **non e' un ID** *(`BYTE-INERTE`, `NON-ABELIANO`, `NO-OP`…)* va
in **`doc/INDICE_ID_ESCLUSI.tsv`** **col motivo e col numero di citazioni**. Niente si butta in
silenzio.

**NESSUN RUN, nessun simulatore.**
"""
# ESENTE-P5: non importa il simulatore e non lo fa girare. Genera due indici da documenti.
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
DEST = os.path.join(RADICE, "doc", "INDICE_ID.tsv")
DEST_X = os.path.join(RADICE, "doc", "INDICE_ID_ESCLUSI.tsv")
REFERTO = os.path.join(RADICE, "doc", "INDICE_ID_referto.txt")
NL = chr(10)
TAB = chr(9)

# ------------------------------------------------------------------ i registri, e che cosa sono
#   (file, namespace, tipo di default)
REGISTRI = [
    ("doc/ASSIOMI.md", "", "assioma"),
    ("doc/PATTERN_DI_PROVA.md", "", "standard"),
    ("doc/RAMIFICAZIONI.md", "", "fronte"),
    ("doc/STATO_RUN.md", "", "altro"),
    ("doc/REGISTRO_FISICA.md", "REGISTRO_FISICA", "criterio-locale"),
    ("doc/COMPONENTI_PROMOSSE.md", "COMPONENTI", "criterio-locale"),
    # ⚠ `CLAUDE.md` DEFINISCE I PRESIDI (`P1`-`P6` in par.0-ter) e le regole, e mancava:
    #   `P6` risultava «citato 59 volte e mai definito». Un registro che si legge per primo e che
    #   l'indice non guarda e' esattamente il difetto che questo indice deve togliere.
    ("CLAUDE.md", "", "presidio"),
]
#   le sezioni che NON definiscono (viste e rimandi)
SEZ_VISTA = [(r"ESITO DI OGNI VOCE", "tabella generata: cita le voci di RAMIFICAZIONI")]
#   il tipo, per sezione, dove la sezione lo dice meglio del registro
TIPO_SEZ = [
    (r"DIFETTI APERTI", "difetto"),
    (r"SOSPETTI", "sospetto"),
    (r"CURE VERIFICATE|LA CODA UNICA", "cura"),
    (r"PRESIDIO STRUTTURALE", "presidio"),
    (r"DIAGNOSI CHIUSE|CHIUSE PER MISURA|CHIUSE PER DIMOSTRAZIONE", "misura"),
]
#   lo stato, dai marcatori della fonte -- e dove non c'e' marcatore: `da-decidere`
STATO = [
    (r"NON E' UN DIFETTO|NON È UN DIFETTO", "non-difetto"),
    (r"RITIRAT[AO]", "non-difetto"),
    (r"\bCURAT[OA]\b|\bCHIUS[AO]\b|\bCHIUSE\b|✅|\bFATTE\b|\bFINIT[OA]\b|VALE SEMPRE"
     r"|CHIUSA PER", "chiuso"),
    (r"\bAPERT[AO]\b|⛔|❗|DA RIVERIFICARE|DA RIFARE|NON MISURAT|IN VERIFICA", "aperto"),
]
BLOCCA_SI = r"BLOCCANTE|PRIMA DI QUALUNQUE GIRO|prima del run base|URGENTE, PRIMA"

FORMA = re.compile(r"(?:[A-Z]\d{1,3}[a-z]?|STANDARD\s+[0-9①-⑳]+"
                   r"|[A-Z][A-Z0-9]{2,}(?:-[A-Z0-9()/]+)+)")
SIMBOLI = (u"✅❌⚠❓⛔⏸⭐➤▶❗☑"
           u"\U0001f7e5\U0001f7e7\U0001f7e9\U0001f4cb\U0001f4e4\U0001f6d1\U0001f3af")

# ------------------------------------------------------------------ gli ESCLUSI: forme che NON sono ID
NON_SONO_ID = [
    (r"^(BYTE|PURE|PRE|NO|NON|SENZA|NATO|COLLO|ON|OFF|SOLO|TUTTO|ZERO|META|MAX|MIN|SUB)-",
     "locuzione del testo, non un identificatore"),
    (r"-(INERTE|INERTI|IDENTICO|IDENTICA|READ|OP|GO|ABELIANO|DI|FISICA|CURA|FORK|SPENTA|NATO)$",
     "locuzione del testo, non un identificatore"),
    (r"^(CLAUDE|README|MEMORY|TODO|NOTA|FILE|PATH|CSV|JSON|YAML|TSV|HTML|PNG|MP4|PKL|GZ)\b",
     "nome di file o di formato"),
    (r"^[A-Z]{2,}_[A-Z]", "nome di FLAG o di costante del codice"),
    # ⚠ I NUMERALI A PAROLE: `SETTE-OTTO`, `DUE-TRE`. Aggiunti perche' `SETTE-OTTO` in un
    #   messaggio di commit ha **bloccato il commit** -- e il presidio ha fatto bene: la forma
    #   *sembra* un ID. **Si chiude classificando, non con un'eccezione dichiarata.**
    (r"^(UN|UNO|DUE|TRE|QUATTRO|CINQUE|SEI|SETTE|OTTO|NOVE|DIECI|CENTO|MILLE)-",
     "numerale a parole, non un identificatore"),
    (r"-(UN|UNO|DUE|TRE|QUATTRO|CINQUE|SEI|SETTE|OTTO|NOVE|DIECI|CENTO|MILLE)$",
     "numerale a parole, non un identificatore"),
]

R = []


def P(s=""):
    R.append(s)
    print(s)


def testo(p):
    return io.open(os.path.join(RADICE, p), encoding="utf-8", newline="").read()


def _nudo(s):
    return re.sub(r"[`*#>_~]", "", re.sub("[" + SIMBOLI + "]", " ", s)).strip()


def def_di(riga):
    if re.match(r"^#{1,6}\s", riga):
        c = _nudo(riga.lstrip("# "))
    elif riga.startswith("|"):
        c = _nudo(riga.strip().strip("|").split("|")[0])
    elif re.match(r"^\*\*(?:`)?[A-Z]", riga):
        # In `CLAUDE.md` i presidi si aprono in GRASSETTO, non con un'intestazione:
        #   `**P1 -- NON USARE L'ASSOCIAZIONE...**`. Senza questo ramo, `P1`-`P6` non esistono.
        c = _nudo(riga)
    else:
        return None
    m = re.match(r"^([A-Z][A-Za-z0-9]{0,4}(?:-[A-Z0-9()/]+)*|STANDARD\s+[0-9①-⑳]+)"
                 r"(?:[\s.,:—-]|$)", c)
    if not m:
        return None
    i = m.group(1).rstrip(".")
    return i if FORMA.fullmatch(i) and not re.fullmatch(r"[A-Z]", i) else None


def titolo_di(riga):
    t = re.sub(r"\s+", " ", _nudo(riga).strip("| ")).strip()
    t = re.sub(r"^[A-Z][A-Za-z0-9-]{0,24}\s*[|—-]\s*", "", t)
    return t[:110]


def primo(regole, testo_, altrimenti):
    for pat, val in regole:
        if re.search(pat, testo_):
            return val
    return altrimenti


# ================================================================== LE DEFINIZIONI
VOCI = {}          # chiave -> dict
NUDE = defaultdict(set)
for f, ns, tipo_reg in REGISTRI:
    sez = ""
    for k, riga in enumerate(testo(f).split(NL), 1):
        i = def_di(riga)
        if re.match(r"^#{1,4}\s", riga) and not i:
            sez = titolo_di(riga)[:60] or _nudo(riga.lstrip("# "))[:60]
        if not i:
            continue
        if any(re.search(pat, sez) for pat, _m in SEZ_VISTA):
            continue
        chiave = ("%s:%s" % (ns, i)) if ns else i
        if chiave in VOCI:
            continue                    # la prima definizione e' quella principale
        _t = _nudo(riga)
        VOCI[chiave] = {
            "id": chiave,
            "titolo": titolo_di(riga) or "(senza titolo)",
            "fonte": "%s::%s" % (f, (titolo_di(riga) or "")[:40]),
            "tipo": primo(TIPO_SEZ, sez, tipo_reg),
            "stato": primo(STATO, _t, "da-decidere"),
            "blocca": "SI" if re.search(BLOCCA_SI, _t) else "",
            "alias": set(),
        }
        NUDE[i].add(chiave)

# le forme NUDE degli ID con namespace diventano alias SOLO se univoche
for nudo, chiavi in NUDE.items():
    if len(chiavi) == 1:
        c = list(chiavi)[0]
        if c != nudo:
            VOCI[c]["alias"].add(nudo)

# gli alias dalle RINOMINE del PASSO 1 (generati dal referto, non ricopiati)
_rin = 0
for riga in testo("doc/RINOMINE_ID.txt").split(NL):
    m = re.match(r"^(RAMIFICAZIONI|STATO_RUN)\.md\s+(\S+)\s+(\S+)\s", riga)
    if m and m.group(3) in VOCI:
        VOCI[m.group(3)]["alias"].add(m.group(2))
        _rin += 1

# ================================================================== LE CITAZIONI
# ⚠ I PROPRI OUTPUT NON SI CONTANO, E IL PERCHE' E' UN DIFETTO MISURATO: il referto del
#   collaudo del presidio **stampa** gli ID inventati `ZZ999` e `D97`; lo sweep li leggeva, li
#   metteva nell'indice come «citati e mai definiti», e **al giro dopo il collaudo PASSAVA su
#   entrambi i casi che DEVONO fallire**. **Uno strumento che si nutre dei propri output si
#   autoconferma.**
AUTO_PRODOTTI = ("INDICE_ID", "COLLISIONI_ID", "RINOMINE_ID", "COLLAUDO_presidio_indice",
                 "INVENTARIO_lettori_id")
FILES, AUTO_SALTATI = [], []
for base, _d, ff in os.walk(os.path.join(RADICE, "doc")):
    for f2 in ff:
        if not (f2.endswith(".md") or f2.endswith(".txt")):
            continue
        rel2 = os.path.relpath(os.path.join(base, f2), RADICE).replace(os.sep, "/")
        if any(x in rel2 for x in AUTO_PRODOTTI):
            AUTO_SALTATI.append(rel2)
            continue
        FILES.append(rel2)
FILES += ["CLAUDE.md", "RELAZIONE_PER_CLAUDE.md"]
CIT = Counter()
for p in sorted(set(FILES)):
    try:
        t = testo(p)
    except Exception:
        continue
    for m in FORMA.finditer(t):
        CIT[m.group(0)] += 1

NOTI = set(VOCI)
for v in VOCI.values():
    NOTI |= set(v["alias"])

# ================================================================== gli ESCLUSI, e i NON DEFINITI
ESCL, NONDEF = [], []
for tok, n in sorted(CIT.items(), key=lambda kv: -kv[1]):
    if tok in NOTI:
        continue
    mot = primo(NON_SONO_ID, tok, None)
    if mot:
        ESCL.append((tok, mot, n))
    else:
        NONDEF.append((tok, n))

# ------------------------------------------------------------------ i criteri LOCALI di sigillo
#   ⚠ Un token citato SOLO in referti, sigilli e task history — e MAI in un registro vivo — e'
#   un'ETICHETTA DI CRITERIO di quel sigillo (`T1`, `S1`, `R3`, `K3`, `Q6`): il suo nome pieno
#   include il sigillo. **Non e' un ID globale**, e chiamarlo `altro` lo nasconderebbe fra le voci
#   vere. Si classifica per DOVE e' citato, che e' un dato, non un giudizio.
VIVI_SET = set(["doc/STATO_RUN.md", "doc/RAMIFICAZIONI.md", "doc/ASSIOMI.md",
                "doc/REGISTRO_FISICA.md", "doc/COMPONENTI_PROMOSSE.md",
                "doc/PATTERN_DI_PROVA.md", "CLAUDE.md"])
DOVE = defaultdict(set)
for p in sorted(set(FILES)):
    try:
        _t2 = testo(p)
    except Exception:
        continue
    for m in FORMA.finditer(_t2):
        DOVE[m.group(0)].add(p)

# i CITATI e non definiti entrano NELL'INDICE: non si nascondono
_loc = 0
for tok, n in NONDEF:
    _in_vivi = bool(DOVE.get(tok, set()) & VIVI_SET)
    _tipo = "altro" if _in_vivi else "criterio-locale"
    if not _in_vivi:
        _loc += 1
    VOCI[tok] = {
        "id": tok,
        "titolo": ("(CITATO %d volte, MAI definito in un registro%s)"
                   % (n, "" if _in_vivi else "; citato solo in referti/sigilli/task history")),
        "fonte": "(nessuna definizione trovata)", "tipo": _tipo,
        "stato": "da-decidere", "blocca": "", "alias": set()}

# blocca_run_base: NO dove la voce e' chiusa / teoria / non-difetto; altrimenti DA-DECIDERE
for v in VOCI.values():
    if v["blocca"] == "SI":
        continue
    v["blocca"] = ("NO" if (v["stato"] in ("chiuso", "non-difetto")
                            or v["tipo"] in ("assioma", "standard")) else "DA-DECIDERE")
    if v["tipo"] in ("assioma", "standard") and v["stato"] == "da-decidere":
        v["stato"] = "teoria"

# ================================================================== SCRITTURA
COL = ["id", "alias", "titolo_breve", "fonte_principale", "stato", "blocca_run_base", "tipo"]
out = [TAB.join(COL)]
for k in sorted(VOCI):
    v = VOCI[k]
    out.append(TAB.join([v["id"], ",".join(sorted(v["alias"])),
                         re.sub(r"[\t\n]", " ", v["titolo"]), v["fonte"],
                         v["stato"], v["blocca"], v["tipo"]]))
io.open(DEST, "w", encoding="utf-8", newline=NL).write(NL.join(out) + NL)

outx = [TAB.join(["forma", "motivo", "citazioni"])]
for tok, mot, n in ESCL:
    outx.append(TAB.join([tok, mot, str(n)]))
io.open(DEST_X, "w", encoding="utf-8", newline=NL).write(NL.join(outx) + NL)

# ================================================================== il referto
P("=" * 104)
P("`doc/INDICE_ID.tsv` -- L'INDICE DI TUTTI GLI ID   (2026-09-26)")
P("=" * 104)
P()
P("  voci nell'indice: %d      esclusi (non sono ID): %d" % (len(VOCI), len(ESCL)))
P("  alias dalle RINOMINE del PASSO 1: %d       alias dalla forma NUDA univoca: %d"
  % (_rin, sum(1 for v in VOCI.values() for a in v["alias"] if ":" in v["id"])))
P()
_st = Counter(v["stato"] for v in VOCI.values())
_tp = Counter(v["tipo"] for v in VOCI.values())
_bl = Counter(v["blocca"] for v in VOCI.values())
P("  per STATO:            %s" % ", ".join("%s=%d" % x for x in _st.most_common()))
P("  per TIPO:             %s" % ", ".join("%s=%d" % x for x in _tp.most_common()))
P("  per BLOCCA_RUN_BASE:  %s" % ", ".join("%s=%d" % x for x in _bl.most_common()))
P()
P("  file SALTATI perche' sono OUTPUT di questa stessa macchina: %d  (%s)"
  % (len(AUTO_SALTATI), ", ".join(os.path.basename(x) for x in sorted(AUTO_SALTATI))))
P("     uno strumento che si nutre dei propri output si AUTOCONFERMA: il referto del collaudo")
P("     stampa `ZZ999`, e lo sweep lo metteva nell'indice.")
P()
P("  CITATI e MAI DEFINITI in un registro (entrano con `da-decidere`): %d" % len(NONDEF))
P("      di cui citati SOLO in referti/sigilli/task history -> `criterio-locale`: %d" % _loc)
for tok, n in NONDEF[:12]:
    P("      %-22s %d citazioni" % (tok, n))
P()
P("=" * 104)
P("COSA QUESTO INDICE *NON* DICE")
P("=" * 104)
P("  - **`blocca_run_base` e' `DA-DECIDERE` su %d voci su %d**, e non e' pigrizia: **nessun"
  % (_bl.get("DA-DECIDERE", 0), len(VOCI)))
P("    documento lo dichiara**. Vale `SI` solo dove il testo dice «bloccante» o «prima di")
P("    qualunque giro lungo». **Riempirla a intuito sarebbe indovinare, e Luca l'ha vietato.**")
P("  - **`stato = da-decidere` significa che la fonte non porta un marcatore riconoscibile**, non")
P("    che la voce sia in sospeso. Sono %d voci." % _st.get("da-decidere", 0))
P("  - **il titolo e' TRONCATO a 110 caratteri**: l'indice dice DOVE vive una voce, non che cosa")
P("    dice. La spiegazione resta nel documento.")
P("  - **la fonte e' `file::ancora`, non `file:riga`**: un numero di riga marcisce al primo")
P("    inserimento, un frammento di titolo si trova con una ricerca.")
P("  - **gli ESCLUSI sono %d forme** riconosciute come locuzioni, nomi di file o di flag: stanno in"
  % len(ESCL))
P("    `doc/INDICE_ID_ESCLUSI.tsv` **col motivo e col numero di citazioni**, non in silenzio.")

io.open(REFERTO, "w", encoding="utf-8", newline=NL).write(NL.join(R) + NL)
