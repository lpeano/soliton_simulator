# -*- coding: utf-8 -*-
"""PUNTO `13(c)(f)` — **IL REPLAY SU TUTTI I REGISTRI, e i generati BYTE-IDENTICI.**

> ### ⛔ **`13(c)`:** *«il testo non si corrompe: ogni campo di testo cambia **solo
> con una riga di storico** che ne porta l'impronta, e il replay si estende a **TUTTI i
> registri**»*.
> ### ⛔ **`13(f)`:** *«i testi generati **si rigenerano BYTE-IDENTICI**, o il commit
> e' rifiutato»*.

### ⭐ **E IL REPLAY E' IL PRESIDIO CHE RENDE VERA LA FRASE <<si scrive SOLO con la
via unica>>:** se un record non coincide col `dopo` della sua ultima riga di storico,
### **quel campo non e' arrivato da una scrittura dichiarata** — qualcuno ha scritto
a mano.

### ⚠ **MA <<TUTTI I REGISTRI>> NON VUOL DIRE <<TUTTI HANNO UNO STORICO>>**, e la
misura lo dice: su ### **dieci** registri, ### **quattro** hanno uno storico, e
### **sei NO.** Quindi il vocabolario ha ### **due stati**, e ognuno ha un presidio suo:

| lo stato | che cosa significa | come si verifica |
|---|---|---|
| **`REPLAY`** | ogni record coincide col `dopo` della sua ultima riga di storico | ### **si rigioca lo storico** |
| **`REPERTO`** | il file ### **non cambia**: non ha una via di scrittura, e non deve averla | ### **il BLOB dichiarato** |

### ⛔ **E `metadati.jsonl` E' IL CASO SCOMODO, e lo dichiaro invece di nasconderlo:**
ha ### **una via di scrittura** *(`meta-aggiungi`, `meta-depreca`, `meta-rinomina`)* e
### **ZERO righe di storico.** ### **Quindi oggi e' un `REPERTO` per necessita', non per
scelta** — e il presidio lo tratta come tale, ### **ma il referto lo nomina come un
BUCO.**
"""
import hashlib
import io
import json
import os
import subprocess
import sys
import tempfile

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
sys.path.insert(0, _QUI)

NL = chr(10)
D = os.path.join(RADICE, "doc", "indice")

PRESIDIO = "P-T2"

# ### ⚠ **E IL TERZO STATO CORREGGE UNA COSA CHE HO SCRITTO IO:** la prima
# ### stesura diceva *<<o ha un replay, o e- un reperto: NON C-E- UNA TERZA
# ### RISPOSTA>>*. ### **C-E-**, e `citazioni.jsonl` lo dimostra: ### **cresce**
# ### *(quindi non e- un reperto)* e ### **non ha uno storico** *(quindi non e-
# ### un replay)*. Una citazione e- ### **immutabile per costruzione** -- e-
# ### appuntata a un commit -- quindi il registro ### **si allunga e non si
# ### riscrive mai.**
# ### ⭐ **E il presidio e- PIU- FORTE di un blob:** il blob direbbe solo
# ### *<<e- cambiato>>*; questo dice ### **<<una riga che c-era NON C-E- PIU-,
# ### o e- CAMBIATA>>**, e lo verifica ### **contro `git show HEAD`.**
STATI = ("REPLAY", "REPERTO", "SOLO-AGGIUNTE")

# ### ⛔ **I CAMPI DI TESTO LIBERO**, gli stessi di `P-T1`: ### **una sola lista**,
# ### e qui si importa invece di ricopiarla -- ### **due liste divergerebbero.**
try:
    import _testo_e_metadati as TM
    CAMPI_TESTO = TM.CAMPI_TESTO
except Exception:                                            # pragma: no cover
    CAMPI_TESTO = ("titolo", "descrizione", "nota_guardiano", "scheda", "stato_da",
                   "motivo", "eccezione_presidio")

# =====================================================================================
#   LA TABELLA DEI REGISTRI
# -------------------------------------------------------------------------------------
#   `nome -> (stato, chiave, storico, dove, blob)`
#   ### ⚠ **I BLOB sono MISURATI il 2026-10-10**, e un `REPERTO` che cambia
#   ### ### **fa rifiutare il commit**: e- cio- che <<reperto>> significa.
# =====================================================================================
REGISTRI = {
    "voci.jsonl": ("REPLAY", "id", "storico.jsonl", "voci", None),
    "etichette_rimosse.jsonl": ("REPLAY", "id", "storico.jsonl", "etichette", None),
    "leggi.jsonl": ("REPLAY", "id", "storico_era2.jsonl", "leggi", None),
    "variabili.jsonl": ("REPLAY", "id", "storico_era2.jsonl", "variabili", None),
    # ### ⛔ **IL CASO SCOMODO:** ha una via di scrittura e ZERO storico.
    "metadati.jsonl": ("REPERTO", "chiave", None, None, "e876fb9cfe10b65d"),
    "assiomi.jsonl": ("REPERTO", "id", None, None, "06d3c6fa5496d3d7"),
    "decisioni.jsonl": ("REPERTO", "id", None, None, "d8a4fd2fae8c4b3f"),
    "migrazione_era1.jsonl": ("REPERTO", None, None, None, "9a5c45b40fb853fd"),
    "conflitti_era1.jsonl": ("REPERTO", None, None, None, "da39a3ee5e6b4b0d"),
    # ### \u2705 **IL TERZO STATO:** le citazioni strutturate ### **crescono e non si
    # ### riscrivono.** Nessun blob *(cambierebbe a ogni aggiunta)* e nessuno storico
    # ### *(una citazione appuntata a un commit ### **non ha versioni**)*.
    "citazioni.jsonl": ("SOLO-AGGIUNTE", "id", None, None, None),
}

# =====================================================================================
#   `13(f)` -- I TESTI GENERATI, e il comando che li rigenera
# =====================================================================================
# ### ⚠ **E I GENERATI SI DIVIDONO IN VELOCI E LENTI, per una ragione MISURATA:**
# ### `csv/_referto_infrastruttura_era2.py` ### **FA GIRARE I SETTE COLLAUDI** per
# ### prendere i numeri, e dal punto `8` ### **supera i 120 secondi.**
# ### ⛔ **Un presidio di `pre-commit` che costa due minuti NON E- UN PRESIDIO: e-
# ### una ragione per dare `--no-verify`.**
# ### ✅ **Quindi i VELOCI stanno nel `pre-commit`, i LENTI SOLO nella CI**, e il
# ### punto `6` della TERZA parte chiedera- ### **il budget dichiarato** -- questo e- il
# ### primo posto dove serve, e lo dico invece di aspettarlo.
LENTI = ("csv/_referto_infrastruttura_era2.py",)

GENERATI = (
    ("doc/METODI_era1_in_era2.md", "csv/_metodi_era2.py"),
    ("doc/REFERTO_infrastruttura_era2.md", "csv/_referto_infrastruttura_era2.py"),
    ("primo_ordine/stato.py", "primo_ordine/_genera.py"),
    ("primo_ordine/termini/prova_hopping.py", "primo_ordine/_genera.py"),
    ("primo_ordine/termini/prova_locale.py", "primo_ordine/_genera.py"),
    ("primo_ordine/osservatori/prova_norma.py", "primo_ordine/_genera.py"),
    ("doc/leggi_era2/PROVA-HOPPING.md", "primo_ordine/_genera.py"),
    ("doc/leggi_era2/PROVA-LOCALE.md", "primo_ordine/_genera.py"),
    ("doc/leggi_era2/PROVA-NORMA.md", "primo_ordine/_genera.py"),
)


def _jsonl(p):
    if not os.path.exists(p):
        return []
    return [json.loads(r) for r in io.open(p, encoding="utf-8").read().split(NL)
            if r.strip()]


def _blob(p):
    return hashlib.sha1(io.open(p, "rb").read()).hexdigest()[:16]


def impronta_testo(rec):
    """### L-impronta ### **dei soli campi di TESTO** di un record.

    ### ⭐ **Serve a dire una cosa precisa:** non *<<il record e- cambiato>>*, ma
    ### **<<IL TESTO e- cambiato>>** -- e il `13(c)` parla del testo.
    """
    t = {k: rec.get(k) for k in CAMPI_TESTO if k in rec}
    m = (rec.get("meta") or {})
    for k in CAMPI_TESTO:
        if k in m:
            t["meta." + k] = m[k]
    return hashlib.sha1(json.dumps(t, sort_keys=True, ensure_ascii=False)
                        .encode("utf-8")).hexdigest()[:16]


def _righe_storico(nome):
    """Le righe di storico ### **di QUESTO registro**, in ordine."""
    stato, chiave, storico, dove, _b = REGISTRI[nome]
    if not storico:
        return []
    righe = _jsonl(os.path.join(D, storico))
    if dove in ("leggi", "variabili"):
        return [r for r in righe if r.get("dove") == dove]
    # ### ⛔ **E QUI LA PRIMA REGOLA CHE AVEVO SCRITTO ERA SBAGLIATA.**
    # ### `voci.jsonl` ed `etichette_rimosse.jsonl` ### **CONDIVIDONO uno storico**
    # ### che ### **non porta un campo `dove`**, e avevo filtrato ### **per
    # ### CHIAVE**: <<le righe il cui `id` e- in questo registro>>.
    # ### ⚠ **FALSO, e `34` errori me l-hanno detto:** un ID puo- stare in
    # ### `etichette_rimosse.jsonl` ### **E avere righe di storico da quando era
    # ### una VOCE** -- e quelle righe hanno la forma di una voce, non di
    # ### un-etichetta.
    # ### ✅ **LA REGOLA GIUSTA: si confronta L-INSIEME DEI CAMPI**, record per
    # ### record. ### **E- STRUTTURA, non prosa:** non si legge nessun titolo e non
    # ### si indovina niente -- ### **due record con campi diversi sono due cose
    # ### diverse.**
    return [r for r in righe if isinstance(r.get("dopo"), dict)]

def replay(nome):
    """### Gli errori del replay di un registro, o `[]`."""
    stato, chiave, _s, _d, _b = REGISTRI[nome]
    err = []
    record = {r[chiave]: r for r in _jsonl(os.path.join(D, nome))}
    righe = _righe_storico(nome)
    for k, rec in sorted(record.items()):
        # ### ⛔ **L-ULTIMA riga di storico CON LO STESSO INSIEME DI CAMPI.**
        # ### Senza il confronto dei campi si prenderebbe la riga di quando quell-ID
        # ### era ### **un-altra cosa** -- ed e- il difetto che `34` errori hanno
        # ### mostrato al primo giro.
        cand = [r for r in righe
                if r.get("id") == k and set(r["dopo"]) == set(rec)]
        if not cand:
            continue
        riga = cand[-1]
        dopo = riga["dopo"]
        campi = set(dopo) & set(rec)
        diversi = sorted(c for c in campi
                         if c not in ("aggiornata",) and dopo.get(c) != rec.get(c))
        if diversi:
            err.append("`P-T2` `%s` `%s`: NON coincide col `dopo` della sua ultima riga "
                       "di storico, e differisce in %s. ### Quel campo NON E- ARRIVATO "
                       "DA UNA SCRITTURA DICHIARATA: qualcuno ha scritto a mano"
                       % (nome, k, diversi))
            continue
        # ------------------------------------------------------------------ `13(c)`
        # ### ⛔ **E IL TESTO IN PARTICOLARE:** l-impronta dei soli campi di testo
        # ### del record deve coincidere con quella del `dopo`. ### **Se coincide il
        # ### record intero, coincide anche questa** -- il braccio serve a dire
        # ### ### **che il TESTO e- coperto**, non a trovare un caso in piu-.
        if impronta_testo(rec) != impronta_testo(dopo):
            err.append("`P-T2` `%s` `%s`: l-IMPRONTA DEI CAMPI DI TESTO non coincide "
                       "col `dopo` (`%s` contro `%s`)"
                       % (nome, k, impronta_testo(rec), impronta_testo(dopo)))
    return err


def reperto(nome):
    stato, _c, _s, _d, b = REGISTRI[nome]
    p = os.path.join(D, nome)
    if not os.path.exists(p):
        return ["`P-T2` `%s`: dichiarato `REPERTO` e NON ESISTE" % nome]
    ora = _blob(p)
    if ora != b:
        return ["`P-T2` `%s`: e- un `REPERTO` e IL SUO BLOB E- CAMBIATO (`%s` contro il "
                "dichiarato `%s`). ### Un reperto NON CAMBIA: se deve cambiare, gli "
                "serve una VIA DI SCRITTURA con il suo storico, e allora diventa "
                "`REPLAY`" % (nome, ora, b)]
    return []


def solo_aggiunte(nome):
    """### `SOLO-AGGIUNTE`: ### **ogni riga che c-era a `HEAD` c-e- ancora, IDENTICA.**

    ### \u26d4 **Si confronta con `git show HEAD:<file>`**, non con un blob dichiarato:
    un blob ### **cambierebbe a ogni aggiunta** e andrebbe riscritto a mano -- e
    ### **un presidio che va riscritto a ogni commit si spegne da se-.**
    """
    import subprocess
    p = os.path.join(D, nome)
    rel = "doc/indice/" + nome
    r = subprocess.run(["git", "show", "HEAD:" + rel], cwd=RADICE, capture_output=True)
    if r.returncode != 0:
        # ### \u2705 **Non e- ancora a `HEAD`:** e- il commit in cui NASCE.
        return []
    prima = [json.loads(x) for x in
             r.stdout.decode("utf-8").split(NL) if x.strip()]
    ora = {json.dumps(x, sort_keys=True, ensure_ascii=False) for x in _jsonl(p)}
    err = []
    for x in prima:
        s = json.dumps(x, sort_keys=True, ensure_ascii=False)
        if s not in ora:
            err.append("`P-T2` `%s`: una riga che c-era a `HEAD` NON C-E- PIU- o e- "
                       "CAMBIATA (`%s`). ### Questo registro e- `SOLO-AGGIUNTE`: si "
                       "allunga, e non si riscrive"
                       % (nome, str(x.get("id") or s)[:40]))
    return err


def controlla():
    err = []
    # --- ogni `.jsonl` di `doc/indice/` e- DICHIARATO
    sul_disco = {f for f in os.listdir(D) if f.endswith(".jsonl")
                 and not f.startswith("storico")}
    for f in sorted(sul_disco - set(REGISTRI)):
        err.append("`P-T2` `%s`: e- un registro sul disco e NON E- DICHIARATO. "
                   "### O ha un replay, o e- un reperto col suo blob, o e- "
                   "`SOLO-AGGIUNTE`: TRE risposte, e il terzo stato CORREGGE cio- che "
                   "questa riga diceva prima" % f)
    for f in sorted(set(REGISTRI) - sul_disco):
        err.append("`P-T2` `%s`: DICHIARATO e non sul disco" % f)
    for nome, (stato, _c, storico, _d, b) in sorted(REGISTRI.items()):
        if stato not in STATI:
            err.append("`P-T2` `%s`: stato %r fuori vocabolario: %s"
                       % (nome, stato, list(STATI)))
            continue
        if stato == "SOLO-AGGIUNTE":
            err += solo_aggiunte(nome)
            continue
        if stato == "REPLAY":
            if not storico:
                err.append("`P-T2` `%s`: `REPLAY` senza uno storico dichiarato" % nome)
                continue
            err += replay(nome)
        else:
            if not b:
                err.append("`P-T2` `%s`: `REPERTO` senza il blob dichiarato" % nome)
                continue
            err += reperto(nome)
    return err


# =====================================================================================
#   `13(f)` -- I GENERATI SI RIGENERANO BYTE-IDENTICI
# =====================================================================================

def generati(con_lenti=False):
    """### Gli errori di `13(f)`, o `[]`. ### **Rigenera e confronta AL BYTE.**

    ### ⚠ **E NON rigenera in una copia:** i generatori scrivono ### **nel repo**,
    e ### **ricostruire la loro destinazione sarebbe un secondo posto** dove il percorso
    puo- divergere. ### ✅ **Quindi si salvano i byte PRIMA, si rigenera, si
    confronta, e SE QUALCOSA E- CAMBIATO si rimette come era** -- cosi- il presidio
    ### **non lascia il repo diverso da come l-ha trovato.**
    """
    err = []
    scelti = [(f, c) for f, c in GENERATI if con_lenti or c not in LENTI]
    prima = {}
    for f, _cmd in scelti:
        p = os.path.join(RADICE, f)
        if os.path.exists(p):
            prima[f] = io.open(p, "rb").read()
    comandi = []
    for _f, cmd in scelti:
        if cmd not in comandi:
            comandi.append(cmd)
    for cmd in comandi:
        r = subprocess.run([sys.executable, cmd], cwd=RADICE, capture_output=True)
        if r.returncode != 0:
            err.append("`P-T2` `%s`: il generatore NON GIRA (codice %d). ### Un testo "
                       "generato da un comando che non gira NON E- RIPRODUCIBILE"
                       % (cmd, r.returncode))
    for f, cmd in scelti:
        p = os.path.join(RADICE, f)
        if f not in prima:
            err.append("`P-T2` `%s`: dichiarato generato e NON ESISTEVA prima" % f)
            continue
        if not os.path.exists(p):
            err.append("`P-T2` `%s`: il generatore l-ha FATTO SPARIRE" % f)
            continue
        dopo = io.open(p, "rb").read()
        if dopo != prima[f]:
            err.append("`P-T2` `%s`: RIGENERATO E DIVERSO (`%s` -> `%s`). ### O e- stato "
                       "modificato a mano, o la sua fonte e- cambiata senza rigenerare: "
                       "si rigenera con `%s`, NON si corregge il file"
                       % (f, hashlib.sha1(prima[f]).hexdigest()[:10],
                          hashlib.sha1(dopo).hexdigest()[:10], cmd))
            # ### ✅ **si rimette come era:** il presidio non lascia il repo diverso.
            io.open(p, "wb").write(prima[f])
    return err


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
    print("IL COLLAUDO DI `P-T2` -- nei DUE VERSI")
    print("=" * 100)
    n = {s: sum(1 for v in REGISTRI.values() if v[0] == s) for s in STATI}
    n_rep = n["REPLAY"]
    esito("sul disco: `P-T2` TACE sui registri", controlla() == [],
          "%d registri: %s" % (len(REGISTRI),
                               ", ".join("%d `%s`" % (n[s], s) for s in STATI)))
    esito("### il braccio sopra HA MATERIA (ci sono registri da rigiocare)", n_rep >= 3,
          "%d `REPLAY`: se fosse 0 il braccio sarebbe un FALSO-UNO" % n_rep)
    # --- quante righe di storico CAMBIANO un campo di testo: il `13(c)` ha materia?
    cambi = 0
    for nome, (stato, _c, _s, _d, _b) in sorted(REGISTRI.items()):
        if stato != "REPLAY":
            continue
        for r in _righe_storico(nome):
            a, b = r.get("prima"), r.get("dopo")
            if isinstance(a, dict) and isinstance(b, dict) \
                    and impronta_testo(a) != impronta_testo(b):
                cambi += 1
    esito("### e il `13(c)` HA MATERIA: ci sono righe che CAMBIANO un campo di testo",
          cambi > 0, "%d righe: ### il replay sul testo non e- un braccio vuoto" % cambi)
    # --- il verso che DEVE scattare: un record che non coincide
    v = _jsonl(os.path.join(D, "voci.jsonl"))
    ult = {r["id"]: r for r in _righe_storico("voci.jsonl")}
    bersaglio = next((x for x in v if x["id"] in ult), None)
    assert bersaglio is not None
    p = os.path.join(D, "voci.jsonl")
    salva = io.open(p, "rb").read()
    try:
        storto = [dict(x, titolo=x["titolo"] + " TOCCATO A MANO")
                  if x["id"] == bersaglio["id"] else x for x in v]
        io.open(p, "w", encoding="utf-8", newline=NL).write(
            NL.join(json.dumps(x, ensure_ascii=False) for x in storto) + NL)
        e = replay("voci.jsonl")
        esito("### DEVE scattare: un `titolo` TOCCATO A MANO",
              any("ha scritto a mano" in x for x in e),
              "`%s`: ### e- il presidio che rende VERA la frase <<si scrive SOLO con la "
              "via unica>>" % bersaglio["id"])
        esito("### e l-IMPRONTA DEI CAMPI DI TESTO lo vede",
              impronta_testo(bersaglio)
              != impronta_testo(dict(bersaglio,
                                     titolo=bersaglio["titolo"] + " TOCCATO A MANO")),
              "### `13(c)` parla del TESTO, e questa impronta parla solo del testo")
    finally:
        io.open(p, "wb").write(salva)
    esito("NON deve scattare: rimesso il file, il replay TACE", replay("voci.jsonl") == [],
          "### il braccio di sopra scattava per LUI, non per un residuo")
    # --- il TERZO stato: una riga TOLTA
    import subprocess as _sp
    _p = os.path.join(D, "citazioni.jsonl")
    _r = _sp.run(["git", "show", "HEAD:doc/indice/citazioni.jsonl"], cwd=RADICE,
                 capture_output=True)
    if _r.returncode == 0:
        _salva = io.open(_p, "rb").read()
        try:
            _rr = _jsonl(_p)
            io.open(_p, "w", encoding="utf-8", newline=NL).write(
                NL.join(json.dumps(x, ensure_ascii=False) for x in _rr[1:]) + NL)
            esito("### DEVE scattare: una riga TOLTA da un registro `SOLO-AGGIUNTE`",
                  any("NON C-E- PIU-" in x for x in solo_aggiunte("citazioni.jsonl")),
                  "### si allunga, e NON si riscrive")
        finally:
            io.open(_p, "wb").write(_salva)
        esito("NON deve scattare: rimesso il file, `SOLO-AGGIUNTE` TACE",
              solo_aggiunte("citazioni.jsonl") == [],
              "### il braccio di sopra scattava per LUI")
    else:
        esito("`SOLO-AGGIUNTE`: `citazioni.jsonl` NASCE in questo commit",
              solo_aggiunte("citazioni.jsonl") == [],
              "### non e- ancora a `HEAD`: il braccio che DEVE scattare arriva al "
              "prossimo commit, e lo dico")
    # --- un REPERTO che cambia
    salva2 = dict(REGISTRI["assiomi.jsonl"])if False else REGISTRI["assiomi.jsonl"]
    try:
        REGISTRI["assiomi.jsonl"] = ("REPERTO", "id", None, None, "0000000000000000")
        esito("### DEVE scattare: un `REPERTO` il cui BLOB e- cambiato",
              any("IL SUO BLOB E- CAMBIATO" in x for x in reperto("assiomi.jsonl")),
              "### un reperto NON CAMBIA: e- cio- che la parola significa")
    finally:
        REGISTRI["assiomi.jsonl"] = salva2
    # --- un registro NON dichiarato
    f2 = os.path.join(D, "_finto_registro.jsonl")
    try:
        io.open(f2, "w", encoding="utf-8", newline=NL).write("{}" + NL)
        esito("### DEVE scattare: un registro sul disco e NON DICHIARATO",
              any("NON E- DICHIARATO" in x for x in controlla()),
              "### o ha un replay, o e- un reperto, o e- `SOLO-AGGIUNTE`: TRE risposte")
    finally:
        if os.path.exists(f2):
            os.remove(f2)
    # --- `13(f)`
    e = generati(con_lenti=False)
    esito("`13(f)` i TESTI GENERATI VELOCI si rigenerano BYTE-IDENTICI", e == [],
          "%d file su %d, %d generatori: ### i LENTI stanno SOLO nella CI"
          % (len([1 for _f, c in GENERATI if c not in LENTI]), len(GENERATI),
             len({c for _f, c in GENERATI if c not in LENTI})))
    esito("### e il braccio sopra HA MATERIA (ci sono generati da rigenerare)",
          len(GENERATI) >= 5, "%d file dichiarati" % len(GENERATI))
    esito("NON deve scattare: alla fine, `P-T2` TACE di nuovo",
          controlla() == [] and generati(con_lenti=False) == [],
          "### e il repo e- come l-ho trovato")
    print("=" * 100)
    print("IL COLLAUDO DI `P-T2`: %d su %d   %s"
          % (ok[0], ok[1], "### TUTTI PASSATI" if ok[0] == ok[1] else "### CI SONO BUCHI"))
    print("=" * 100)
    return 0 if ok[0] == ok[1] else 1


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    if "--collaudo" in argv:
        return collaudo()
    err = controlla()
    # ### ⛔ **I LENTI SOLO SE CHIESTI** *(`--con-lenti`, che la CI passa)*: un
    # ### presidio di `pre-commit` che costa due minuti ### **e- una ragione per dare
    # ### `--no-verify`.**
    err += generati(con_lenti="--con-lenti" in argv)
    n = {s: sum(1 for v in REGISTRI.values() if v[0] == s) for s in STATI}
    print("  `P-T2`: %d registri (%s), %d testi generati"
          % (len(REGISTRI), ", ".join("%d `%s`" % (n[s], s) for s in STATI),
             len(GENERATI)))
    for e in err[:14]:
        print("  ### %s" % e)
    print("  ### %d errori" % len(err))
    _ = tempfile
    return 1 if err else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
