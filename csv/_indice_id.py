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
#   ...e una voce puo' DICHIARARE di non bloccare: la fonte vince sulla parola chiave.
BLOCCA_NO = r"NON BLOCCA|non blocca il run base"

# ------------------------------------------------------------------ LE SETTE FAMIGLIE (A-G)
#   ⚠ QUESTE REGOLE VENGONO DA `_lista_chiusa.py`, e **si spostano qui** perche' dal 2026-09-26
#   la famiglia e' una COLONNA DELL'INDICE (opzione (a) scelta da Luca): **un posto solo la
#   calcola**, e la vista la LEGGE invece di ricalcolarla.
#   L'ordine conta: la prima parola che attacca decide. `G` sta per ultima perche' le sue parole
#   sono le piu' comuni (misurato: quando stava prima si prendeva tutto).
FAMIGLIE = [
    ("A", "INERZIA E AVVIO"), ("B", "TEMPO UNICO"), ("C", "DOPPIA COPERTURA E CREAZIONE"),
    ("D", "SOGLIE TARATE E SOTTO PLANCK"), ("E", "DISEGNO E STATISTICHE GLOBALI"),
    ("F", "FRENO E CONTRAZIONE"), ("G", "ARRETRATO DEGLI STRUMENTI"),
]
REG_FAM = [
 (r"inerzia|contrasto|rho_s|\bramp\b|rampa|accension|\beta\b|omega|spinor|\bpeq\b|semina"
  r"|sorgente di campo", "A"),
 (r"freno|SCALA_MIN|smorza|\bd0\b|coesion|repulsion|dx/d|compression|\bLAM\b|_nasce"
  r"|archi|distanz", "F"),
 (r"fase|\bphi\b|\u03c6|2pi|4pi|2\u03c0|4\u03c0|torsion|\btw\b|mitosi|Schwinger|antifase"
  r"|wrap|SCALE-TW|copertura|soglia0", "C"),
 (r"tempo|dt_n|dt_e|orologio|ritmo|tau_pp|foliazion|causal|\btau\b", "B"),
 (r"soglia|clip|pavimento|tetto|QMIN|tarat|unita' assolute|massa_critica|costant|limite", "D"),
 (r"median|global|disegno|\bpos\b|statistic|rilassa_disegno", "E"),
 (r"presidi|hook|ancor|inventario|passo incompleto|step\(\)|argv|\bCLI\b|P1-bis|\bP5\b"
  r"|\bP8\b|\bP9\b|ripres|reperto|non ri-girabile|sigillo|blob|referto|script|lettori", "G"),
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


def _taglia(s, n):
    """Tronca **su un confine di parola**.

    ⚠ Tagliare a meta' parola **INVENTA UN ID**: `GLOBALE-DISEGNO` troncato a 117 caratteri
    diventava `GLOBALE-DIS`, e il presidio dell'indice -- giustamente -- lo segnalava come ID
    sconosciuto **in un documento che questa macchina stessa aveva scritto**.
    **Un troncamento non deve creare nomi.**
    """
    s = re.sub(r"\s+", " ", s or "").strip()
    if len(s) <= n:
        return s
    _t = s[:n - 1]
    _sp = _t.rfind(" ")
    return (_t[:_sp] if _sp > n // 2 else _t) + chr(0x2026)


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
    # ⚠ UN'ETICHETTA CHE ELENCA PIU' VOCI NON NE DEFINISCE NESSUNA. **Misurato:** la riga
    #   `| PROBLEMI-CHK3 · FAMIGLIE · FASCE-TAU | SOSPESI |` faceva risultare `PROBLEMI-CHK3`
    #   definito DUE volte -- una nella coda unica, dove la voce vive, e una qui, dove e' solo
    #   **citata insieme ad altre due**. E' la stessa famiglia dei RIMANDI: cita, non definisce.
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
    t = re.sub(r"\s+", " ", _nudo(riga).strip("| ")).strip()
    t = re.sub(r"^[A-Z][A-Za-z0-9-]{0,24}\s*[|—-]\s*", "", t)
    return _taglia(t, 111)


def breve_riga(v):
    """Un titolo di UNA riga, leggibile: il titolo, o la riga ridotta se il titolo e' vuoto."""
    # Senza questa pulizia lo smistamento stampa righe come
    #   `R2 VALE PER QUELLA SCENA [EPOCA 1 . MISURA] / NUOVO: il residuo...`, in cui **le prime sei
    #   parole non dicono nulla** a chi deve decidere.
    s = re.sub(r"\s+", " ", v["titolo"]).replace("|", "/").strip()
    s = re.sub(r"^" + re.escape(v["id"].split(":")[-1]) + r"\b\s*", "", s)
    s = re.sub(r"^(?:VALE SEMPRE|VALE PER QUELLA SCENA|CHIUSA PER \w+|DA RIVERIFICARE"
               r"|LA LETTURA CADE|APERT[AO]|CURAT[AO])\s*", "", s)
    s = re.sub(r"\[EPOCA[^\]]*\]\s*", "", s)
    s = re.sub(r"^[\s/\u2014-]+", "", s)
    return (s[:117] + "\u2026") if len(s) > 118 else s


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
            "riga": _t,
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
        "riga": "", "fonte": "(nessuna definizione trovata)", "tipo": _tipo,
        "stato": "da-decidere", "blocca": "", "alias": set()}

# ------------------------------------------------------------------ `blocca_run_base`
#   ❌ CORREZIONE DI LUCA, 2026-09-26: **la PAROLA CHIAVE da sola e' sbagliata.** `Z25`, `Z29` e
#   `Z73` uscivano `non-difetto` **e** `SI` insieme -- `Z73` perche' il suo testo dice «BLOCCA LA
#   MITOSI», che parla della MITOSI, non del run base. **Una parola che compare nel racconto di un
#   riscontro non e' una dichiarazione sul run base.**
#   REGOLA: **un `non-difetto`, un `chiuso`, una `teoria` o un `criterio-locale` NON bloccano MAI.**
for v in VOCI.values():
    if v["tipo"] in ("assioma", "standard") and v["stato"] == "da-decidere":
        v["stato"] = "teoria"
    _mai = (v["stato"] in ("chiuso", "non-difetto", "teoria")
            or v["tipo"] in ("assioma", "standard", "criterio-locale"))
    if _mai:
        v["blocca"] = "NO"                     # vince sulla parola chiave
    elif re.search(BLOCCA_NO, v.get("riga", "")):
        v["blocca"] = "NO"                     # la fonte lo DICHIARA
    elif v["blocca"] != "SI":
        v["blocca"] = "DA-DECIDERE"
    # la famiglia: dalla riga intera dove c'e', dal titolo altrimenti
    v["fam"] = "?"
    for pat, k in REG_FAM:
        if re.search(pat, v.get("riga", "") or v["titolo"], re.I):
            v["fam"] = k
            break

# ================================================================== SCRITTURA
COL = ["id", "alias", "titolo_breve", "fonte_principale", "stato", "blocca_run_base", "tipo",
       "famiglia"]
out = [TAB.join(COL)]
for k in sorted(VOCI):
    v = VOCI[k]
    out.append(TAB.join([v["id"], ",".join(sorted(v["alias"])),
                         re.sub(r"[\t\n]", " ", v["titolo"]), v["fonte"],
                         v["stato"], v["blocca"], v["tipo"], v["fam"]]))
io.open(DEST, "w", encoding="utf-8", newline=NL).write(NL.join(out) + NL)

outx = [TAB.join(["forma", "motivo", "citazioni"])]
for tok, mot, n in ESCL:
    outx.append(TAB.join([tok, mot, str(n)]))
io.open(DEST_X, "w", encoding="utf-8", newline=NL).write(NL.join(outx) + NL)

# ================================================================== lo SMISTAMENTO per Luca
#   ⚠ SOLO i tipi che possono bloccare un run base, e SOLO se aperti o da decidere. **`SI`/`NO`
#   NON si riempiono a intuito: questa lista e' la BASE su cui decide Luca** (ordine suo).
TIPI_SMIST = ("difetto", "fronte", "misura", "cura")
SMIST = [v for v in VOCI.values()
         if v["tipo"] in TIPI_SMIST and v["stato"] in ("aperto", "da-decidere")]
_sm = [u"# 🧮 **SMISTAMENTO PER IL RUN BASE — la lista su cui decide Luca** *(2026-09-26)*",
       u"",
       u"*(**Generata** da `csv/_indice_id.py` dall'indice: nessuna riga e' ricopiata a mano.)*",
       u"",
       u"> ## ⚠ **`blocca_run_base` NON E' RIEMPITO A INTUITO.**",
       u"> Qui stanno **solo** le voci che potrebbero bloccare: tipo `difetto`, `fronte`, `misura`",
       u"> o `cura`, **e** stato `aperto` o `da-decidere`. **Le decide Luca**, riga per riga.",
       u"> Tutto il resto — `chiuso`, `non-difetto`, `teoria`, `criterio-locale`, `assioma`,",
       u"> `standard` — **non blocca MAI**, ed e' gia' `NO` nell'indice **per regola, non per",
       u"> giudizio**.",
       u"",
       u"```",
       u"voci nell'indice          %d" % len(VOCI),
       u"in questo smistamento     %d   (tipo difetto/fronte/misura/cura E stato aperto/da-decidere)"
       % len(SMIST),
       u"```",
       u""]
for k, nome in FAMIGLIE + [("?", "SENZA FAMIGLIA — nessuna regola ha deciso")]:
    vv = [v for v in SMIST if v["fam"] == k]
    if not vv:
        continue
    _sm += [u"## FAMIGLIA **%s** — %s   *(%d voci)*" % (k, nome, len(vv)), u"",
            u"| blocca? | id | che cos'e' | fonte |", u"|:--:|---|---|---|"]
    for v in sorted(vv, key=lambda x: (x["tipo"], x["id"])):
        _sm.append(u"| `%s` | **%s** | %s | `%s` |"
                   % (v["blocca"], v["id"], breve_riga(v), v["fonte"].split("::")[0]
                      .replace("doc/", "")))
    _sm.append(u"")
_sm += [u"---", u"",
        u"**COSA QUESTA LISTA NON DICE:**",
        u"- **non dice che le altre %d voci siano irrilevanti**: dice che **non possono bloccare un"
        % (len(VOCI) - len(SMIST)),
        u"  run base** perche' sono chiuse, sono teoria, o sono etichette locali di un sigillo.",
        u"- **il titolo e' UNA riga**: la spiegazione sta nella fonte, e la fonte e' nella colonna.",
        u"- **`DA-DECIDERE` e' la risposta onesta**, non una casella vuota: nessun documento dichiara",
        u"  che quella voce blocchi o non blocchi il run base."]
io.open(os.path.join(RADICE, "doc", "SMISTAMENTO_run_base.md"), "w", encoding="utf-8",
        newline=NL).write(NL.join(_sm) + NL)

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
_fm = Counter(v["fam"] for v in VOCI.values())
P("  per FAMIGLIA:         %s" % ", ".join("%s=%d" % x for x in sorted(_fm.items())))
P()
_male = [v["id"] for v in VOCI.values()
         if v["blocca"] == "SI" and (v["stato"] in ("chiuso", "non-difetto", "teoria")
                                     or v["tipo"] == "criterio-locale")]
P("  CONTROLLO di Luca: righe con stato chiuso/non-difetto/teoria (o criterio-locale) E blocca SI:")
P("      %d   -> %s" % (len(_male), "PASS" if not _male else "FAIL: " + ", ".join(_male[:12])))
P("  SMISTAMENTO (tipo difetto/fronte/misura/cura, stato aperto/da-decidere): %d voci" % len(SMIST))
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
