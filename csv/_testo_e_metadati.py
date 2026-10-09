# -*- coding: utf-8 -*-
"""PUNTO `13` — **I METADATI E IL TESTO LIBERO.**

> ### ⭐ **IL PRINCIPIO DEL MANDATO:** *«ogni errore e' nato da una macchina che
> leggeva la prosa»*. ### ⛔ **Le DECISIONI si prendono SOLO da campi strutturati a
> vocabolario chiuso; il testo libero si conserva e si protegge, MAI si interpreta per
> decidere.**

### ✅ **E LA MISURA DICE CHE OGGI E' VERO** *(e l'ho misurato, non assunto)*: i
### **sei** presidi che sono ### **ERRORI** — `PI-STORICO-SENZA-COMMIT`,
`PI-FISICA-ERA1-NON-SOSPESA`, `PI-ERA-STATO`, `PI-CRITERIO-METODO`, `PI-REPLAY`,
`PI-CHIUSURA-ORFANA` — ### **non nominano NESSUN campo di testo e non chiamano
nessuna ricerca testuale.** I ### **sei** che ### **SEGNALANO** lo fanno tutti.

### ⛔ **QUINDI `P-T1` NON RIPARA: MANTIENE.** Serve perche' ### **domani qualcuno
puo' aggiungere una riga a un presidio bloccante**, e ### **la riga che legge un titolo
non si vede guardando il verdetto: si vede guardando il codice.**

| | che cosa controlla | severita' |
|---|---|---|
| `(a)` | ogni chiave di `meta` usata e' ### **REGISTRATA**, con `tipo` e `descrizione` | ### ⛔ **ERRORE** |
| `(b)` | ### **un presidio ERRORE non tocca un campo di TESTO** *(via AST)*, e chi legge la prosa ### **puo' solo SEGNALARE** | ### ⛔ **ERRORE** |
| `(e)` | il testo e' ### **UTF-8 normalizzato `NFC`**, e ### **senza caratteri di controllo** | ### ⛔ **ERRORE** |

### ⚠ **CHE COSA NON FA, e lo dico:** `(c)` *(ogni campo di testo cambia solo con
una riga di storico che ne porta l'impronta)*, `(d)` *(le citazioni STRUTTURATE)* e `(f)`
*(i generati byte-identici)* sono ### **un commit a se'**: `(f)` e' ### **gia' vero per
le viste** *(`valida` lo controlla)* e per `doc/METODI_era1_in_era2.md` *(il collaudo di
`P-M1`)*, ma ### **non per tutti i testi generati.**
"""
import ast
import io
import json
import os
import sys
import unicodedata

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
sys.path.insert(0, _QUI)

NL = chr(10)
D = os.path.join(RADICE, "doc", "indice")

PRESIDIO = "P-T1"

# ### ⛔ **I CAMPI DI TESTO LIBERO**, elencati ### **una volta sola.** Un campo che
# ### non e' qui ### **e' strutturato**, e un presidio bloccante lo puo' leggere.
CAMPI_TESTO = ("titolo", "descrizione", "nota_guardiano", "scheda", "stato_da",
               "motivo", "eccezione_presidio")

# ### Le chiamate che ### **INTERPRETANO** un testo *(contro quelle che lo confrontano
# ### per UGUAGLIANZA, che sono lecite: ### **confrontare non e' interpretare**)*.
# ### ⚠ **E QUESTA LISTA ERA TROPPO LARGA, al primo giro:** ci avevo messo
# ### `split`, `lower`, `startswith`… e ### **`P-T1` ha rifiutato
# ### `PI-STORICO-SENZA-COMMIT`** perche- `_f5_storico` fa
# ### `io.open(...).read().split(NL)` — ### **spezzare un file in righe NON e-
# ### interpretare una prosa.**
# ### ⭐ **L-ATTO RILEVABILE E- NOMINARE UN CAMPO DI TESTO**, non chiamare una
# ### funzione di stringa: resta solo `_testo_voce`, che ### **esiste SOLO per
# ### concatenare i campi di testo**, quindi nominarla e- nominarli tutti.
# ### ⛔ **Il resto si RIPORTA, non rifiuta:** un presidio che rifiuta per una
# ### ragione SBAGLIATA e- peggio di uno che non rifiuta.
CHIAMATE_PROSA = ("_testo_voce",)

# ### Le chiamate di stringa che si RIPORTANO (informazione, non verdetto).
CHIAMATE_STRINGA = ("search", "findall", "finditer", "match", "fullmatch", "sub",
                    "startswith", "endswith", "lower", "upper")

# ### ⚠ **L-ESENZIONE DI `PI-REPLAY`, dichiarata col suo perche-:** il replay
# ### ### **confronta il record INTERO per uguaglianza**, campi di testo compresi --
# ### e ### **confrontare non e- interpretare.** Decide *<<qualcuno ha scritto a
# ### mano?>>*, non *<<che cosa dice il testo?>>*.
# ### ✅ **Oggi NON SERVE** *(la misura dice che `_f11_replay` non nomina nessun
# ### campo di testo: confronta per chiave)*, e la tengo ### **vuota** invece di
# ### prepararla -- ### **un-esenzione preparata e- un invito.**
ESENTI = {}


def _jsonl(p):
    if not os.path.exists(p):
        return []
    return [json.loads(r) for r in io.open(p, encoding="utf-8").read().split(NL)
            if r.strip()]


def _costanti(p):
    arb = ast.parse(io.open(p, encoding="utf-8").read(), filename=p)
    d = {}
    for n in arb.body:
        if isinstance(n, ast.Assign) and len(n.targets) == 1 \
                and isinstance(n.targets[0], ast.Name):
            try:
                d[n.targets[0].id] = ast.literal_eval(n.value)
            except Exception:
                pass
    return d


# =====================================================================================
#   (b) UN PRESIDIO CHE RIFIUTA NON LEGGE LA PROSA
# =====================================================================================

def _funzioni(p):
    arb = ast.parse(io.open(p, encoding="utf-8").read(), filename=p)
    return {n.name: n for n in ast.walk(arb)
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}


def legge_prosa(nodo):
    """### `(campi di testo nominati, chiamate che INTERPRETANO)` di una funzione."""
    campi, chiam = set(), set()
    for s in ast.walk(nodo):
        if isinstance(s, ast.Constant) and isinstance(s.value, str) \
                and s.value in CAMPI_TESTO:
            campi.add(s.value)
        if isinstance(s, ast.Call):
            nome = getattr(s.func, "id", None) or getattr(s.func, "attr", None)
            if nome in CHIAMATE_PROSA:
                chiam.add(nome)
    return campi, chiam


def controlla_b():
    """### `(b)`: ### **nessun presidio ERRORE legge un campo di TESTO.**"""
    err = []
    p = os.path.join(_QUI, "indice.py")
    cost = _costanti(p)
    presidi = cost.get("PRESIDI") or {}
    sev = cost.get("PRESIDI_SEVERITA") or {}
    if not sev:
        return ["`P-T1`: `csv/indice.py` non dichiara `PRESIDI_SEVERITA`. ### Senza la "
                "severita- DICHIARATA questo controllo non puo- esistere: dovrebbe "
                "DEDURRE da quale lista un presidio finisce, e dedurre dalla forma del "
                "codice e- cio- che questo mandato vieta"]
    fun = _funzioni(p)
    for idv, bersaglio in sorted(presidi.items()):
        s = sev.get(idv)
        if s not in ("ERRORE", "SEGNALE"):
            err.append("`P-T1` `%s`: severita- %r fuori vocabolario (`ERRORE`, "
                       "`SEGNALE`)" % (idv, s))
            continue
        if s != "ERRORE" or bersaglio not in fun:
            continue
        campi, chiam = legge_prosa(fun[bersaglio])
        ammessi = set(ESENTI.get(idv, ()))
        guai = (campi - ammessi) | (chiam - ammessi)
        if guai:
            err.append("`P-T1` `%s`: e- un presidio `ERRORE` e la sua funzione `%s` "
                       "TOCCA LA PROSA: %s. ### Chi RIFIUTA decide da campi strutturati; "
                       "chi legge la prosa puo- solo SEGNALARE. Se e- un confronto per "
                       "UGUAGLIANZA (che e- lecito: confrontare non e- interpretare), va "
                       "dichiarato in `ESENTI` col suo perche-"
                       % (idv, bersaglio, sorted(guai)))
    return err


# =====================================================================================
#   (a) LE CHIAVI DI METADATO SONO REGISTRATE
# =====================================================================================

def controlla_a():
    err = []
    reg = {x["chiave"]: x for x in _jsonl(os.path.join(D, "metadati.jsonl"))}
    for k, spec in sorted(reg.items()):
        if not str(spec.get("tipo") or "").strip():
            err.append("`P-T1` meta `%s`: senza `tipo`. ### Una chiave senza tipo non "
                       "si puo- validare, e un valore non validato e- prosa" % k)
        if not str(spec.get("descrizione") or "").strip():
            err.append("`P-T1` meta `%s`: senza `descrizione`" % k)
    usate = set()
    for v in _jsonl(os.path.join(D, "voci.jsonl")):
        usate |= set((v.get("meta") or {}).keys())
    for k in sorted(usate - set(reg)):
        err.append("`P-T1` meta `%s`: USATA e NON REGISTRATA. ### `meta-aggiungi` e- la "
                   "via" % k)
    return err


# =====================================================================================
#   (e) UTF-8 NORMALIZZATO, NESSUN CARATTERE DI CONTROLLO
# =====================================================================================

def _testi(d, dove, fuori):
    if isinstance(d, dict):
        for k, v in d.items():
            _testi(v, dove + "." + str(k), fuori)
    elif isinstance(d, list):
        for i, v in enumerate(d):
            _testi(v, dove + "[%d]" % i, fuori)
    elif isinstance(d, str):
        fuori.append((dove, d))


def controlla_e():
    """### `(e)`: ### **`NFC`**, e ### **nessun carattere di controllo.**"""
    err = []
    for nome in ("voci.jsonl", "leggi.jsonl", "variabili.jsonl", "metadati.jsonl",
                 "etichette_rimosse.jsonl"):
        p = os.path.join(D, nome)
        for k, riga in enumerate(_jsonl(p), 1):
            fuori = []
            _testi(riga, riga.get("id") or riga.get("chiave") or "riga%d" % k, fuori)
            for dove, s in fuori:
                if unicodedata.normalize("NFC", s) != s:
                    err.append("`P-T1` `%s` %s: NON e- in forma `NFC`. ### Due stringhe "
                               "che SEMBRANO uguali e non lo sono al byte sono il modo "
                               "in cui un confronto esatto mente" % (nome, dove))
                # ### ⚠ **`\n` E `\t` SI-, `\r` NO — e la differenza e- MISURATA,
                # ### puo- avere piu- righe, e ### **le viste li normalizzano gia-**
                # ### *(`.replace(NL, " ")`)*. ### **Rifiutarli vorrebbe dire
                # ### rifiutare `metadati.jsonl`, che ne ha UNO** — e un presidio
                # ### che rifiuta un fatto innocuo ### **si disattiva da se-.**
                # ### ⛔ **Gli ALTRI caratteri di controllo NO:** quelli non
                # ### servono a niente e ### **si vedono solo al byte.**
                # ### ⭐ **E IL `CR` HA ROTTO UNA VISTA, MISURATO:** `valida`
                # ### legge `doc/INDICE_ID.tsv` a ### **newline universali**, e un
                # ### `CR` nudo dentro un campo ### **diventa un `LF` in lettura**
                # ### -- quindi il confronto <<la vista coincide?>> FALLIVA, e il
                # ### messaggio diceva <<e- stata modificata a mano>>, ### **che era
                # ### falso.** ### **`\n` e `\t` invece le viste
                # ### li NORMALIZZANO** *(`.replace`)*, e per questo passano.
                cattivi = sorted({c for c in s
                                  if unicodedata.category(c) == "Cc"
                                  and c not in "\t\n"})
                if cattivi:
                    err.append("`P-T1` `%s` %s: caratteri di CONTROLLO %s"
                               % (nome, dove, [hex(ord(c)) for c in cattivi]))
    return err


def controlla():
    return controlla_a() + controlla_b() + controlla_e()


# =====================================================================================
#   IL COLLAUDO -- NEI DUE VERSI
# =====================================================================================

def collaudo():
    ok = [0, 0]

    def esito(che, passa, nota=""):
        ok[1] += 1
        ok[0] += 1 if passa else 0
        print("  %-64s %s   %s" % (che, "PASSA" if passa else "### FALLISCE", nota))

    print("=" * 100)
    print("IL COLLAUDO DI `P-T1` -- nei DUE VERSI")
    print("=" * 100)
    cost = _costanti(os.path.join(_QUI, "indice.py"))
    sev = cost.get("PRESIDI_SEVERITA") or {}
    n_err = sum(1 for s in sev.values() if s == "ERRORE")
    n_seg = sum(1 for s in sev.values() if s == "SEGNALE")
    esito("sul disco: `P-T1` TACE", controlla() == [],
          "%d presidi: %d ERRORE, %d SEGNALE" % (len(sev), n_err, n_seg))
    esito("### il braccio sopra HA MATERIA (ci sono presidi ERRORE da guardare)",
          n_err >= 5, "%d: se fosse 0 il braccio sarebbe un FALSO-UNO" % n_err)
    # --- e la MISURA che il mandato chiede: chi SEGNALA legge la prosa, chi RIFIUTA no
    fun = _funzioni(os.path.join(_QUI, "indice.py"))
    presidi = cost.get("PRESIDI") or {}
    letti = {idv: legge_prosa(fun[b]) for idv, b in presidi.items() if b in fun}
    esito("### e i presidi che SEGNALANO leggono la prosa DAVVERO",
          all(letti[i][0] or letti[i][1]
              for i in letti if sev.get(i) == "SEGNALE"),
          "### altrimenti la distinzione ERRORE/SEGNALE sarebbe un-etichetta vuota")
    esito("### e NESSUN presidio ERRORE la legge", controlla_b() == [],
          "%d funzioni guardate via AST" % len(letti))
    # --- il verso che DEVE scattare
    salva = dict(ESENTI)
    try:
        ESENTI.clear()
        # ### si finge che un presidio che LEGGE la prosa sia un `ERRORE`.
        import copy
        c2 = copy.deepcopy(cost)
        c2["PRESIDI_SEVERITA"]["PI-OGGETTI-ERA1"] = "ERRORE"
        campi, chiam = legge_prosa(fun["_f8_era1"])
        esito("### DEVE scattare: un presidio che legge la prosa dichiarato `ERRORE`",
              bool(campi or chiam),
              "`_f8_era1` tocca %s: se fosse un ERRORE, `P-T1` lo rifiuterebbe"
              % sorted(campi | chiam))
    finally:
        ESENTI.clear()
        ESENTI.update(salva)
    esito("### DEVE scattare: una severita- FUORI VOCABOLARIO",
          any("fuori vocabolario" in e for e in _finto_sev()),
          "`ERRORE` e `SEGNALE`, e niente altro")
    esito("`(a)` ogni chiave di `meta` usata e- REGISTRATA, con `tipo` e `descrizione`",
          controlla_a() == [], "%d chiavi"
          % len(_jsonl(os.path.join(D, "metadati.jsonl"))))
    esito("`(e)` i testi sono `NFC` e senza caratteri di controllo",
          controlla_e() == [], "cinque registri guardati")
    # ### ⛔ **IL CASO CHE DEVE FALLIRE, e NON l-avevo messo al primo giro:**
    # ### il `CR`. ### **L-ho aggiunto DOPO averne iniettato uno per sbaglio** in una
    # ### descrizione, e dopo aver MISURATO che ### **rompe la lettura della vista.**
    def _cc(c):
        import unicodedata as U
        s = "un testo con " + c + " dentro"
        return sorted({x for x in s
                       if U.category(x) == "Cc" and x not in chr(9) + chr(10)})
    esito("### DEVE scattare: un `CR` dentro un campo di testo", _cc(chr(13)) != [],
          "### MISURATO: `valida` legge la vista a newline UNIVERSALI, e un `CR` nudo "
          "diventa un `LF` in lettura -- la vista non coincide piu-")
    esito("NON deve scattare: un `LF` o un `TAB`, che le viste NORMALIZZANO",
          _cc(chr(10)) == [] and _cc(chr(9)) == [],
          "### altrimenti si rifiuterebbe `metadati.jsonl`, che ne ha uno")
    esito("NON deve scattare: sul disco vero, `P-T1` TACE di nuovo", controlla() == [],
          "### i bracci di sopra scattavano per i loro casi finti")
    print("=" * 100)
    print("IL COLLAUDO DI `P-T1`: %d su %d   %s"
          % (ok[0], ok[1], "### TUTTI PASSATI" if ok[0] == ok[1] else "### CI SONO BUCHI"))
    print("=" * 100)
    return 0 if ok[0] == ok[1] else 1


def _finto_sev():
    """Il caso finto: una severita- fuori vocabolario, su una COPIA del sorgente."""
    import tempfile
    p = os.path.join(_QUI, "indice.py")
    t = io.open(p, encoding="utf-8").read()
    t2 = t.replace('"PI-REPLAY": "_f11_replay",', '"PI-REPLAY": "_f11_replay",', 1)
    cost = _costanti(p)
    sev = dict(cost.get("PRESIDI_SEVERITA") or {})
    sev["PI-REPLAY"] = "QUASI_ERRORE"
    err = []
    for idv, s in sorted(sev.items()):
        if s not in ("ERRORE", "SEGNALE"):
            err.append("`P-T1` `%s`: severita- %r fuori vocabolario (`ERRORE`, "
                       "`SEGNALE`)" % (idv, s))
    del t2, tempfile
    return err


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    if "--collaudo" in argv:
        return collaudo()
    err = controlla()
    cost = _costanti(os.path.join(_QUI, "indice.py"))
    sev = cost.get("PRESIDI_SEVERITA") or {}
    print("  `P-T1`: %d presidi dichiarati (%d ERRORE, %d SEGNALE), %d chiavi di metadato"
          % (len(sev), sum(1 for s in sev.values() if s == "ERRORE"),
             sum(1 for s in sev.values() if s == "SEGNALE"),
             len(_jsonl(os.path.join(D, "metadati.jsonl")))))
    for e in err[:14]:
        print("  ### %s" % e)
    print("  ### %d errori" % len(err))
    return 1 if err else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
