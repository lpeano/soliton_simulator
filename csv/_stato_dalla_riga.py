# -*- coding: utf-8 -*-
"""LO STATO E LA CLASSE **DALLA RIGA D'ORIGINE** — punti `1` e `2`.

> ### ⭐ **LA VALIDITA' NON E' LO STATO.** *«VALE SEMPRE»*, *«VALE PER QUELLA SCENA»*,
> *«LIMITE DICHIARATO»* ### **non dicono se una cosa e' fatta**: dicono ### **fin dove vale
> cio' che si e' trovato.** Vanno in `meta.validita`.

### ⛔ **IL COLLAUDO GIRA PRIMA DI APPLICARE**, su una COPIA, sui `7` casi che il mandato
fissa: ### **se uno esce diverso, la regola e' sbagliata e si ferma.**

Gira con:  python csv/_stato_dalla_riga.py collaudo    # i 7 casi, PRIMA
           python csv/_stato_dalla_riga.py 1           # il lotto dello stato
           python csv/_stato_dalla_riga.py 2           # il lotto della classe
"""
import io
import json
import os
import re
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
sys.path.insert(0, _QUI)
import _presidio                                             # noqa: E402
_presidio.avvia(__file__)
import _righe_origine as RO                                  # noqa: E402

# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Legge documenti.
NL = chr(10)
D = os.path.join(RADICE, "doc", "indice")
DATA = "2026-10-09"
sys.path.insert(0, _QUI)
import indice as IX                                          # noqa: E402
TRANSIZ = IX.TRANSIZIONI
_SHA = re.compile(r"(?<![0-9a-f])[0-9a-f]{7,40}(?![0-9a-f])")

# ==========================================================================
#   LA VALIDITA'  --  e NON e' lo stato
# ==========================================================================
VALIDITA = (("VALE SEMPRE", "vale sempre"),
            ("VALE PER QUELLA SCENA", "vale per quella scena"),
            ("LIMITE DICHIARATO", "limite dichiarato"))

# ==========================================================================
#   LO STATO  --  le due liste del mandato, alla lettera
# ==========================================================================
CHIUDE = ("CHIUSA", "CHIUSO", "CURATO E SIGILLATO", "CURATA E SIGILLATA",
          "CURATE E SIGILLATE", "CURA IN CODICE", "FATTO", "FATTA", "FINITO", "FINITA",
          "RITIRATA", "RITIRATO", chr(0x2705))
APRE = ("DOMANDA APERTA", "NON INIZIATO", "NON INIZIATA", "NON CURATO", "NON CURATA",
        "DA RIVERIFICARE", "SI CHIUDE QUANDO", "CHIUDE CHI", "RESTA APERTA",
        "RESTA APERTO", "APERTA", "APERTO")
# ### ⛔ **LA NEGAZIONE CONTA, e un caso del mandato lo dimostra:** `A2-ANELLO` dice
# ### *«… la cura e' un giro a se' e ### **non e' stata fatta**»* — la parola `FATTA` c'e', ma
# ### ### **negata.** Senza questo controllo la voce risulterebbe ### **ambigua**, e il
# ### mandato la vuole ### **`SOSPESA`.**
NEGA = re.compile(r"(?:\bnon\b|\bmai\b|\bnessun\w*\b)[^.;|]{0,14}$", re.I)


def norm(s):
    return RO.norm(s)


# ### ⛔ **IL CONFINE DI PAROLA, e un caso del mandato lo dimostra:** la riga di `Z83`
# ### contiene *<<d0 -> ### **in-FINITO** distorce>>*, e ### **`infinito` contiene
# ### `FINITO`.** Senza il confine la voce risultava ### **AMBIGUA**, e il mandato la vuole
# ### ### **`SOSPESA`.** ### **Una parola cercata per sottostringa non e- la parola.**
_CONF = {}


def _re_parola(w):
    if w not in _CONF:
        if w.isalpha() or " " in w:
            _CONF[w] = re.compile(r"(?<![A-Za-z])" + re.escape(w) + r"(?![A-Za-z])", re.I)
        else:
            _CONF[w] = re.compile(re.escape(w))
    return _CONF[w]


# ### ⛔ **IL DIFETTO <<IL FATTO>>, e lo dichiara il guardiano:** la parola `FATTO`
# ### ### **non dice sempre che una cosa e- fatta.**
# ### • *<<### **IL FATTO** che d scenda sotto LAM …>>* — qui `FATTO` e-
# ###   ### **un SOSTANTIVO**: introduce una frase, e ### **non chiude niente.**
# ### • *<<`FATTO:` …>>* — coi due punti e- ### **un-ETICHETTA DI CAMPO**, come
# ###   <<MISURA:>> o <<ESITO:>>: dice ### **dove si legge**, non ### **che e- finito.**
# ### ➜ **Quindi `FATTO`/`FATTA` contano SOLO se** non precedute da `IL`/`il`
# ### ### **e** non seguite da `:`.
# ### ⭐ **E- lo stesso errore della NEGAZIONE, un livello piu- su:** `NEGA` guarda
# ### ### **se la parola e- negata**, questo guarda ### **se la parola e- un verbo.**
_IL_PRIMA = __import__("re").compile(r"\bil\s+$", __import__("re").I)
_FATTO = ("FATTO", "FATTA")


def _scarta(t, k, w):
    """### `True` se questa occorrenza di `w` a `k` ### **non e- una parola di stato.**

    ### ⚠ **Pura e condivisa da `trova` e da `_pos`:** se stesse in uno solo dei due,
    ### **la decisione e la POSIZIONE non userebbero la stessa regola** -- e la regola
    <<la prima parola di stato vince>> ### **si legge dalla posizione.**
    """
    if w.upper() not in _FATTO:
        return False
    if _IL_PRIMA.search(t[:k]):
        return True
    return t[k + len(w):k + len(w) + 1] == ":"


def trova(testo, parole):
    """### Le parole di `parole` presenti in `testo`, ### **a CONFINE DI PAROLA** e
    ### **salvo quelle NEGATE.**"""
    t = norm(testo)
    fuori = []
    for w in parole:
        for m in _re_parola(w).finditer(t):
            k = m.start()
            if not NEGA.search(t[:k]) and not _scarta(t, k, w):
                fuori.append((w, " ".join(t[max(0, k - 40):k + len(w) + 40].split())))
                break
    return fuori


def registro_di_corse(testo):
    """### ⛔ **L'ERRORE `(a)` DEL GUARDIANO:** un `## APERTO <ID>` e' ### **l'intestazione di
    un REGISTRO DI CORSE**, e la corsa sotto finisce con *«chiuso … FINITO»*.
    ### **L'`APERTO` dell'intestazione NON e' lo stato di oggi: e' il titolo del registro.**
    """
    t = norm(testo)
    primo = t.split(" - ")[0].split(" avvio ")[0]
    e_intestazione = primo.lstrip().startswith("#") and "APERTO" in primo.upper()
    finito = ("FINITO" in t.upper() or "chiuso" in t)
    return e_intestazione and finito


def _pos(testo, w):
    """### Dove compare la parola, ### **a confine e non negata.** `10**9` se non c-e-."""
    t = norm(testo)
    for m in _re_parola(w).finditer(t):
        if not NEGA.search(t[:m.start()]) and not _scarta(t, m.start(), w):
            return m.start()
    return 10 ** 9


def _cella(testo, k):
    """### In quale CELLA della riga cade la posizione `k`: le celle sono separate da `|`.

    ### ⛔ **Serve perche- la narrazione sta in una cella DIVERSA dallo stato**, e due
    parole in celle diverse ### **non si contraddicono: si susseguono.**
    """
    if k >= 10 ** 9:
        return -1
    return norm(testo)[:k].count("|")


def decidi_stato(v, riga):
    """### La decisione, e ### **i tre esiti sono quelli del mandato.**"""
    if riga is None:
        return (None, "nessuna riga d'origine")
    reg = registro_di_corse(riga)
    ch = trova(riga, CHIUDE)
    ap = trova(riga, APRE)
    if reg:
        # ### l'`APERTO` dell'intestazione si TOGLIE, non si pesa
        ap = [x for x in ap if x[0] not in ("APERTO", "APERTA")]
    # ### ⛔ **LA RIGA RACCONTA ANCHE LA STORIA, e due casi del mandato lo dimostrano.**
    # ### `Z83` dice *<<lo stress resta ### **finito** SENZA spostare la media>>* -- un
    # ### ### **AGGETTIVO**, non lo stato; `Z25` dice *<<il difetto non e- stato
    # ### misurabile: fronte ### **aperto**>>* -- la ### **storia passata**, mentre la
    # ### cella di stato dice *<<CHIUSA>>*.
    # ### ✔ **LO STATO E- LA PRIMA PAROLA DI STATO CHE COMPARE**, perche- nelle righe di
    # ### questi registri ### **la cella dello stato viene PRIMA** e la narrazione dopo.
    # ### ⚠ **E resta AMBIGUA se la parola dell-altro gruppo sta NELLA STESSA CELLA:** la-
    # ### ### **non e- storia, e- contraddizione.**
    # ### ⭐ **Senza questo, la regola alla lettera dava 5 su 7** -- e il mandato dice che se
    # ### un caso noto esce diverso ### **la regola e- sbagliata.** Il collaudo ha deciso.
    if not ch and not ap:
        return (None, "NESSUNA parola decide: %s" % norm(riga)[:150])
    primo_ch = min((_pos(riga, w) for w, _c in ch), default=10 ** 9)
    primo_ap = min((_pos(riga, w) for w, _c in ap), default=10 ** 9)
    vince_ch = primo_ch < primo_ap
    w, ctx = (ch if vince_ch else ap)[0]
    altre = ap if vince_ch else ch
    cella = _cella(riga, min(primo_ch, primo_ap))
    dentro = [x for x in altre if _cella(riga, _pos(riga, x[0])) == cella]
    if dentro:
        return (None, "AMBIGUA, e nella STESSA CELLA: dice <<%s>> e <<%s>> -- %s"
                % (w, dentro[0][0], ctx[:110]))
    if vince_ch:
        return ("CHIUSA", "la riga dice <<%s>> (la PRIMA parola di stato): %s"
                % (w, ctx[:150]))
    st = "AGENDA" if str(v["era"]) == "2" else "SOSPESA"
    return (st, "la riga dice <<%s>> (la PRIMA parola di stato): %s" % (w, ctx[:150]))


# ### ⛔ **LE VOCI CHE IL PUNTO `5` RISERVA A LUCA: il punto `1` NON le tocca.**
RISERVATE = ("Z47", "A3-DISEGNO", "G4-MEMARCO", "Z104", "O4", "K2a", "K2b",
             "SPINORE-SENZA-FASE", "MASSA-CRITICA-LOCALE")

# ==========================================================================
#   IL COLLAUDO  --  PRIMA di applicare, e sui casi del mandato
# ==========================================================================
ATTESI = (("Z83", "SOSPESA"), ("Z47", "RISERVATA"), ("Z25", "CHIUSA"), ("Z42", "CHIUSA"),
          ("CURA1-CORTO", "CHIUSA"), ("G1", "CHIUSA"), ("A2-ANELLO", "SOSPESA"))


def collaudo():
    vv = {v["id"]: v for v in RO.voci()}
    print("=" * 104)
    print("IL COLLAUDO DELLA REGOLA DELLO STATO -- sui 7 casi del mandato, PRIMA di applicare")
    print("=" * 104)
    ok = 0
    for i, atteso in ATTESI:
        v = vv[i]
        riga = RO.riga_origine(v)[0]
        if i in RISERVATE:
            dato, perche = ("RISERVATA", "il punto 5 la riserva a Luca: il punto 1 NON la "
                                         "tocca")
        else:
            dato, perche = decidi_stato(v, riga)
            dato = dato or "NON TOCCATA"
        buono = (dato == atteso)
        ok += buono
        print("  %-14s atteso %-12s dato %-12s %s"
              % (i, atteso, dato, "PASSA" if buono else "### FALLISCE"))
        print("      %s" % perche[:150])
    print("=" * 104)
    print("IL COLLAUDO: %d su %d   ### %s"
          % (ok, len(ATTESI),
             "TUTTI PASSATI" if ok == len(ATTESI)
             else "LA REGOLA E' SBAGLIATA: NON SI APPLICA"))
    print("=" * 104)
    return 0 if ok == len(ATTESI) else 1


def punto1():
    """### Il LOTTO del punto `1`: `meta.validita` e lo stato ### **dalla riga.**

    ### ⛔ **IL COLLAUDO GIRA PRIMA, e se non passa il lotto non si scrive.**
    ### ⚠ **E una transizione va in DUE righe:** `TRANSIZIONI` non ammette
    `CHIUSA` -> `SOSPESA`, e da `CHIUSA` si esce ### **solo verso `APERTA` o `SUPERATA`**.
    ### ➜ **Si passa per `APERTA` NELLO STESSO LOTTO**, con due righe di storico: la prima
    dice ### **che la chiusura era sbagliata**, la seconda ### **dove va la voce.**
    ### **Lo stato intermedio non si vede mai**, perche- `aggiorna-lotto` valida una volta
    ### **alla fine.**
    """
    assert collaudo() == 0, "il collaudo NON passa: la regola e- sbagliata"
    vv = RO.voci()
    lotto, amb, val, cam = [], [], 0, 0
    for v in vv:
        riga = RO.riga_origine(v)[0]
        if riga is None:
            continue
        n = norm(riga)
        # ### ⓵ LA VALIDITA-, che ### **NON e- lo stato**
        vista = [q for w, q in VALIDITA if w.lower() in n.lower()]
        meta = {}
        if vista and (v.get("meta") or {}).get("validita") != vista[0]:
            meta["validita"] = vista[0]
            val += 1
        # ### ⓶ LO STATO
        campi, mot = {}, ""
        if v["classe"] == "NON_DEFINITA":
            # ### ⛔ **LO SCHEMA LO VIETA, e ha ragione:** una voce di cui non si sa la
            # ### classe ### **non puo- avere uno stato deciso.** Un segnale di stato nella
            # ### riga di un SEGNAPOSTO non basta: ### **prima la classe, poi lo stato.**
            amb.append((v["id"], "SEGNAPOSTO: classe NON_DEFINITA, e lo schema vieta uno "
                                 "stato deciso. Prima la classe, poi lo stato"))
        elif v["id"] in RISERVATE:
            amb.append((v["id"], "RISERVATA al punto 5: NON si tocca"))
        else:
            st, perche = decidi_stato(v, riga)
            if st is None:
                amb.append((v["id"], perche))
            elif st != v["stato"]:
                # ### ⛔ **CHIUDERE PRETENDE IL COMMIT CHE HA CHIUSO**, e lo schema lo
                # ### impone: `CHIUSA` senza `chiusura.criterio` e `chiusura.commit`
                # ### ### **non passa la validazione.** Il CRITERIO sta nella riga; il
                # ### COMMIT ### **solo se la riga lo porta.**
                # ### ✔ **E l-ostacolo fa un filtro GIUSTO al posto mio:** fra le `53` che
                # ### la regola chiuderebbe, `26` sono righe ### **senza sha** -- e la-
                # ### dentro ci sono ### **assiomi e regole** (`A5`, `A9`,
                # ### `AUTO-MANUTENZIONE`), la cui riga d-origine e- ### **una DEFINIZIONE,
                # ### non una chiusura.** Un assioma ### **non e- <<fatto>>: VALE.**
                # ### ⛔ **Un commit non si inventa**, quindi quelle NON si chiudono e
                # ### ### **si elencano.**
                if st == "CHIUSA":
                    m = _SHA.search(n)
                    if not m:
                        amb.append((v["id"],
                                    "la riga dice CHIUSA ma NON PORTA IL COMMIT che ha "
                                    "chiuso, e lo schema lo pretende: non lo invento -- "
                                    + perche[:120]))
                        if not meta:
                            continue
                        st = None
                    else:
                        campi["chiusura"] = {
                            "criterio": perche[:200], "commit": m.group(0),
                            "data": DATA}
                if st is not None:
                    campi["stato"] = st
                    mot = perche
                    cam += 1
        if not meta and not campi:
            continue
        # ### la transizione vietata si attraversa in DUE righe
        if campi.get("stato") and campi["stato"] not in TRANSIZ.get(v["stato"], set()):
            ponte = "APERTA" if "APERTA" in TRANSIZ.get(v["stato"], set()) else None
            assert ponte, ("`%s`: da `%s` a `%s` NON si puo-, e non c-e- il ponte"
                           % (v["id"], v["stato"], campi["stato"]))
            lotto.append({"id": v["id"], "quando": DATA,
                          "campi": {"stato": ponte}, "meta": {},
                          "motivo": ("(1) PONTE OBBLIGATO: da `%s` a `%s` TRANSIZIONI non "
                                     "lo ammette, e da `%s` si esce solo verso `APERTA` o "
                                     "`SUPERATA`. Questa riga dice CHE LA CHIUSURA ERA "
                                     "SBAGLIATA; la prossima dice dove va la voce. %s"
                                     % (v["stato"], campi["stato"], v["stato"],
                                        mot[:120]))})
        m = ("(1) " + (mot or "solo `meta.validita`: LA VALIDITA- NON E- LO STATO")
             + ((" | validita = <<%s>>" % meta["validita"]) if meta else ""))
        lotto.append({"id": v["id"], "quando": DATA, "campi": campi, "meta": meta,
                      "motivo": m[:1400]})
    p = os.path.join(D, "_lotti", "v3_s1.jsonl")
    io.open(p, "w", encoding="utf-8", newline=NL).write(
        NL.join(json.dumps(x, ensure_ascii=False) for x in lotto) + NL)
    io.open(os.path.join(D, "_p1_ambigue.json"), "w", encoding="utf-8",
            newline=NL).write(json.dumps(amb, ensure_ascii=False, indent=1))
    print()
    print("  scritto doc/indice/_lotti/v3_s1.jsonl: %d righe" % len(lotto))
    print("  (1) %d stati cambiati, %d validita- scritte, %d AMBIGUE o riservate"
          % (cam, val, len(amb)))
    print("  scritto doc/indice/_p1_ambigue.json")
    return 0


# ==========================================================================
#   LA CLASSE DALLA RIGA  --  punto `2`
# ==========================================================================
# ### ⛔ **La stessa tecnica dello stato, e le stesse due trappole:** ### **confine di
# ### parola** e ### **la PRIMA che compare vince** -- perche- la riga racconta anche la
# ### storia, e ### **una cura chiusa nomina il difetto che ha curato.**
CL_CURA = ("CURATO E SIGILLATO", "CURATA E SIGILLATA", "CURATE E SIGILLATE",
           "CURA IN CODICE", "CURATO IN CODICE", "CURATA IN CODICE")
CL_DIFETTO = ("E- UN DIFETTO", "E UN DIFETTO", "DIFETTO ACCLARATO", "DIFETTO MIO",
              "DIFETTO VERO")
CL_MISURA = ("CHIUSA PER MISURA", "CHIUSO PER MISURA")
_NUM = re.compile(r"\d+[.,]\d+|\d+\s*%|\d+\s*/\s*\d+")
# ### ⛔ **UN `?` NELLA PROSA NON E- UNA DOMANDA**, e la prima stesura lo contava: cosi-
# ### ### **`A1`, `A7b`, `A10` -- ASSIOMI -- diventavano `FRONTE`**, perche- la loro sezione
# ### contiene un punto di domanda e la voce e- aperta. ### **Un assioma non e- un fronte:
# ### e- una legge di FORMA, e non si chiude ne- si apre.** ### ✔ **Serve la domanda
# ### DICHIARATA.**
_DOMANDA = re.compile(r"DOMANDA APERTA|LA DOMANDA:|DOMANDA DEL GUARDIANO", re.I)
_PROGRAMMA = re.compile(r"PROGRAMMA|PROGETTO|NON INIZIAT|SI CHIUDE QUANDO|CHIUDE CHI", re.I)


def decidi_classe(v, riga):
    """### La classe dalla riga, ### **con la PRIMA che compare che vince.**"""
    if riga is None:
        return (None, "nessuna riga d-origine")
    n = norm(riga)
    cand = []
    for cl, parole in (("CURA", CL_CURA), ("DIFETTO", CL_DIFETTO),
                       ("MISURA", CL_MISURA)):
        for w, ctx in trova(n, parole):
            cand.append((_pos(n, w), cl, w, ctx))
    # ### ⚠ **<<un esito misurato>> vale solo se la voce e- CHIUSA**: un numero in una voce
    # ### aperta e- ### **una misura DA FARE**, non un esito.
    if v["stato"] == "CHIUSA":
        m = _NUM.search(n)
        if m:
            cand.append((m.start() + 10 ** 6, "MISURA", "un esito misurato",
                         n[max(0, m.start() - 40):m.start() + 50]))
    # ### ⛔ **`FRONTE` SOLO se la voce e- APERTA e il testo e- una domanda o un programma**,
    # ### e il mandato lo dice: ### **un fronte chiuso non e- un fronte.**
    aperta = v["stato"] in ("APERTA", "SOSPESA", "AGENDA")
    if aperta:
        m = _DOMANDA.search(n) or _PROGRAMMA.search(n)
        if m:
            cand.append((m.start() + 2 * 10 ** 6, "FRONTE",
                         "una domanda o un programma, e la voce e- aperta",
                         n[max(0, m.start() - 40):m.start() + 50]))
    if not cand:
        return (None, "NESSUNA parola decide la classe: %s" % n[:140])
    cand.sort()
    quali = sorted({c[1] for c in cand})
    if len(quali) > 1 and cand[0][0] < 10 ** 6 and cand[1][0] < 10 ** 6:
        return (None, "AMBIGUA: la riga porta %s -- %s"
                % ("/".join(quali), cand[0][3][:110]))
    _k, cl, w, ctx = cand[0]
    return (cl, "la riga dice <<%s>> (la PRIMA che compare): %s" % (w, ctx[:150]))


def punto2():
    """### Il LOTTO della classe. ### **Ambigui: si elencano, non si toccano.**"""
    vv = RO.voci()
    lotto, amb, cam = [], [], 0
    for v in vv:
        riga = RO.riga_origine(v)[0]
        if riga is None:
            continue
        if v["classe"] == "NON_DEFINITA":
            # ### ⛔ **Un segnaposto non prende una classe da una riga:** la sua riga
            # ### ### **non e- una definizione** -- e- il posto dove l-ID e- CITATO.
            amb.append((v["id"], "SEGNAPOSTO: la sua riga e- dove l-ID e- CITATO, "
                                 "non dove e- definito"))
            continue
        if v["id"] in RISERVATE:
            amb.append((v["id"], "RISERVATA al punto 5: NON si tocca"))
            continue
        cl, perche = decidi_classe(v, riga)
        if cl is None:
            amb.append((v["id"], perche))
            continue
        if cl == v["classe"]:
            continue
        cam += 1
        lotto.append({"id": v["id"], "quando": DATA, "campi": {"classe": cl},
                      "meta": {},
                      "motivo": "(2) LA CLASSE DALLA RIGA: da `%s` a `%s`. %s"
                                % (v["classe"], cl, perche[:200])})
    p = os.path.join(D, "_lotti", "v3_s2.jsonl")
    io.open(p, "w", encoding="utf-8", newline=NL).write(
        NL.join(json.dumps(x, ensure_ascii=False) for x in lotto) + NL)
    io.open(os.path.join(D, "_p2_ambigue.json"), "w", encoding="utf-8",
            newline=NL).write(json.dumps(amb, ensure_ascii=False, indent=1))
    print("  scritto doc/indice/_lotti/v3_s2.jsonl: %d voci" % len(lotto))
    print("  (2) %d classi cambiate, %d non toccate" % (cam, len(amb)))
    return 0


def main(argv):
    assert argv and argv[0] in ("collaudo", "1", "2"), __doc__
    if argv[0] == "collaudo":
        return collaudo()
    if argv[0] == "1":
        return punto1()
    if argv[0] == "2":
        return punto2()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
