# -*- coding: utf-8 -*-
"""PUNTO `14(f)` — **`indice.py rinomina <vecchio> <nuovo>`: TUTTO IN UN COMMIT.**

> ### ⛔ *«aggiorna voce, alias, **ogni `@rif`** e **ogni `[[ID]]`** nei documenti
> vivi, **in UN commit** — e rinominare a mano → **i presidi lo rifiutano**»*.

### ⭐ **E L'ULTIMA META' DELLA FRASE E' GIA' VERA, e l'ho verificata:** rinominare a
mano ### **viene rifiutato da DUE presidi indipendenti** — `PI-REPLAY` *(la voce non
coincide piu' col `dopo` della sua ultima riga di storico: ### **qualcuno ha scritto a
mano**)* e `P-RIF` *(un `@rif` verso un ID che non esiste piu')*.
### ⛔ **Quindi questo comando non e' una comodita': e' L'UNICA VIA che non viene
rifiutata.**

### ⚠ **E I REPERTI NON SI TOCCANO** *(par.`9`)*: i `doc/REFERTO_*`, i
`doc/REPERTO_*` e i `doc/TASK_HISTORY/*` ### **tengono il nome vecchio**, che si risolve
### **con l'alias.** ### **Il nome vecchio diventa un `alias`**, non sparisce.

### ⛔ **E UN RINOMINAMENTO E' ATOMICO: o tutto, o niente.** Si calcola l'intero
cambiamento, ### **si valida**, e ### **solo allora si scrive** — perche' un
rinominamento a metà lascia ### **un indice che si contraddice.**
"""
import glob
import io
import json
import os
import re
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)

NL = chr(10)

# ### ⛔ **I DOCUMENTI VIVI, dove un `[[ID]]` si riscrive.** Elenco ### **chiuso**,
# ### e ### **i REPERTI non ci sono** *(par.`9`: non si riscrivono)*.
VIVI = ("CLAUDE.md", "RELAZIONE_PER_CLAUDE.md", "doc/ASSIOMI.md",
        "doc/PATTERN_DI_PROVA.md", "doc/REGISTRO_FISICA.md", "doc/STELLA_POLARE.md",
        "doc/INVENTARIO_strumenti.md", "doc/COMPONENTI_PROMOSSE.md",
        "doc/METODI_era1_in_era2.md", "doc/RIFERIMENTI_era2.md")
VIVI_GLOB = ("doc/REGOLE/*.md",)

# ### ⛔ **E QUESTI NON SI TOCCANO MAI**, e il perche- e- il par.`9`.
REPERTI_GLOB = ("doc/REFERTO_*.md", "doc/REPERTO_*.md", "doc/TASK_HISTORY/*.md")


def documenti_vivi():
    fuori = [x for x in VIVI if os.path.exists(os.path.join(RADICE, x))]
    for g in VIVI_GLOB:
        for p in sorted(glob.glob(os.path.join(RADICE, g))):
            fuori.append(p.replace(os.sep, "/")[len(RADICE.replace(os.sep, "/")) + 1:])
    return fuori


def reperti():
    fuori = []
    for g in REPERTI_GLOB:
        for p in sorted(glob.glob(os.path.join(RADICE, g))):
            fuori.append(p.replace(os.sep, "/")[len(RADICE.replace(os.sep, "/")) + 1:])
    return fuori


def file_rif():
    f = sorted(glob.glob(os.path.join(RADICE, "primo_ordine", "**", "*.py"),
                         recursive=True))
    base = RADICE.replace(os.sep, "/")
    return [x.replace(os.sep, "/")[len(base) + 1:] for x in f
            if "__pycache__" not in x]


def pianifica(voci, vecchio, nuovo):
    """### Il piano: ### **che cosa cambia, dove.** ### **Non scrive niente.**"""
    per = {v["id"]: v for v in voci}
    assert vecchio in per, "`%s` non e- una voce" % vecchio
    assert nuovo not in per, ("`%s` ESISTE GIA-: un rinominamento non puo- fondere due "
                              "voci" % nuovo)
    assert re.match(r"^[A-Z][A-Z0-9:_-]{2,}$", nuovo), (
        "`%s` non ha la forma di un ID" % nuovo)
    piano = {"voce": vecchio, "nuovo": nuovo, "rif": [], "vivi": [], "collegate": []}
    # ### i `@rif` nel codice
    pat_rif = re.compile(r'(@?rif\(\s*(?:"[^"]*"\s*,\s*)*)"' + re.escape(vecchio) + '"')
    for rel in file_rif():
        t = io.open(os.path.join(RADICE, rel), encoding="utf-8").read()
        n = len(pat_rif.findall(t)) + t.count('"%s"' % vecchio) * 0
        if ('"%s"' % vecchio) in t and "rif(" in t:
            piano["rif"].append((rel, t.count('"%s"' % vecchio)))
        del n
    # ### i `[[ID]]` nei documenti VIVI
    for rel in documenti_vivi():
        t = io.open(os.path.join(RADICE, rel), encoding="utf-8").read()
        c = t.count("[[%s]]" % vecchio)
        if c:
            piano["vivi"].append((rel, c))
    # ### le voci che lo NOMINANO nei campi strutturati
    for v in voci:
        tocchi = []
        # ### ⚠ **E QUESTA LISTA ERA TROPPO CORTA, al primo giro:** guardavo
        # ### solo `collegate`, `superata_da`, `padre` e `alias`, e ### **il collaudo
        # ### ha detto <<0 voci>> su `A17`** -- che e- nominato da piu- voci,
        # ### ### **nel campo `assiomi`.**
        # ### ⛔ **`assiomi`, `leggi` e `variabili` SONO RIFERIMENTI STRUTTURATI**:
        # ### rinominare senza toccarli lascerebbe ### **riferimenti rotti in campi che
        # ### un presidio legge.**
        for k in ("collegate", "superata_da", "padre", "alias", "assiomi", "leggi",
                  "variabili"):
            val = v.get(k)
            if isinstance(val, list) and vecchio in val:
                tocchi.append(k)
            elif isinstance(val, str) and val == vecchio:
                tocchi.append(k)
        if tocchi:
            piano["collegate"].append((v["id"], tocchi))
    return piano


def applica(voci, piano, motivo):
    """### Applica il piano ### **in memoria**, e torna `(voci, storia, scritture)`.

    ### ⛔ **ATOMICO: non scrive niente.** Chi chiama ### **valida**, e
    ### **solo se passa** scrive -- perche- un rinominamento a meta- lascia
    ### **un indice che si contraddice.**
    """
    vecchio, nuovo = piano["voce"], piano["nuovo"]
    per = {v["id"]: v for v in voci}
    prima = json.loads(json.dumps(per[vecchio]))
    v = per[vecchio]
    v["id"] = nuovo
    # ### ⛔ **IL NOME VECCHIO DIVENTA UN ALIAS**, non sparisce: i reperti lo
    # ### tengono, e ### **si risolve con l-alias** *(par.`9`)*.
    al = list(v.get("alias") or [])
    if vecchio not in al:
        al.append(vecchio)
    v["alias"] = sorted(al)
    storia = [{"quando": None, "id": nuovo, "motivo": motivo, "commit": "",
               "prima": prima, "dopo": json.loads(json.dumps(v))}]
    # ### i campi strutturati delle ALTRE voci
    for x in voci:
        if x["id"] == nuovo:
            continue
        p2 = json.loads(json.dumps(x))
        cambiata = False
        for k in ("collegate", "alias", "assiomi", "leggi", "variabili"):
            if isinstance(x.get(k), list) and vecchio in x[k]:
                x[k] = sorted(nuovo if y == vecchio else y for y in x[k])
                cambiata = True
        for k in ("superata_da", "padre"):
            if x.get(k) == vecchio:
                x[k] = nuovo
                cambiata = True
        if cambiata:
            storia.append({"quando": None, "id": x["id"], "motivo": motivo,
                           "commit": "", "prima": p2,
                           "dopo": json.loads(json.dumps(x))})
    # ### le scritture sui file
    scritture = {}
    for rel, _c in piano["rif"]:
        p = os.path.join(RADICE, rel)
        t = io.open(p, encoding="utf-8").read()
        scritture[rel] = t.replace('"%s"' % vecchio, '"%s"' % nuovo)
    for rel, _c in piano["vivi"]:
        p = os.path.join(RADICE, rel)
        t = io.open(p, encoding="utf-8").read()
        scritture[rel] = t.replace("[[%s]]" % vecchio, "[[%s]]" % nuovo)
    return voci, storia, scritture


def collaudo():
    """### Il collaudo: ### **sul piano**, senza scrivere niente."""
    sys.path.insert(0, _QUI)
    import _presidio
    _presidio.avvia(__file__)
    ok = [0, 0]

    def esito(che, passa, nota=""):
        ok[1] += 1
        ok[0] += 1 if passa else 0
        print("  %-64s %s   %s" % (che, "PASSA" if passa else "### FALLISCE", nota))

    voci = [json.loads(r) for r in
            io.open(os.path.join(RADICE, "doc", "indice", "voci.jsonl"),
                    encoding="utf-8").read().split(NL) if r.strip()]
    print("=" * 100)
    print("IL COLLAUDO DI `rinomina` -- sul PIANO, senza scrivere niente")
    print("=" * 100)
    # ### `A17` e- un buon bersaglio: ha un `@rif` e delle collegate.
    p = pianifica(voci, "A17", "A17-PROVA-RINOMINA")
    esito("il piano trova i `@rif` nel codice", len(p["rif"]) >= 1,
          "%d file: %s" % (len(p["rif"]), ", ".join(x for x, _ in p["rif"])))
    esito("### e il piano trova le voci che lo NOMINANO nei campi",
          len(p["collegate"]) >= 1, "%d voci" % len(p["collegate"]))
    v2, storia, scritture = applica(json.loads(json.dumps(voci)), p, "il collaudo")
    per = {x["id"]: x for x in v2}
    esito("### il nome VECCHIO diventa un `alias`, non sparisce",
          "A17" in (per["A17-PROVA-RINOMINA"]["alias"] or []),
          "### i reperti lo tengono, e si risolve con l-alias (par.9)")
    esito("### e il nome nuovo c-e-", "A17-PROVA-RINOMINA" in per and "A17" not in per)
    esito("### e ogni voce toccata ha la SUA riga di storico",
          len(storia) == 1 + len(p["collegate"]),
          "%d righe: 1 per la voce, %d per le collegate"
          % (len(storia), len(p["collegate"])))
    esito("### e il `@rif` nel codice e- riscritto",
          any('"A17-PROVA-RINOMINA"' in t for t in scritture.values()),
          "%d file da riscrivere" % len(scritture))
    # ### ⛔ **I REPERTI NON SI TOCCANO**, e il piano non li nomina.
    rp = set(reperti())
    esito("### e NESSUN REPERTO e- fra i file da riscrivere",
          not (set(scritture) & rp),
          "%d reperti, e il piano ne tocca %d" % (len(rp), len(set(scritture) & rp)))
    # ### i casi che DEVONO fallire
    for vecchio, nuovo, che in (("ID-CHE-NON-ESISTE", "X-UNO", "una voce che NON esiste"),
                                ("A17", "A16", "un nome NUOVO che ESISTE GIA-"),
                                ("A17", "minuscolo", "un nome che NON ha la forma di un ID")):
        try:
            pianifica(voci, vecchio, nuovo)
            esito("### DEVE scattare: %s" % che, False)
        except AssertionError:
            esito("### DEVE scattare: %s" % che, True)
    esito("### e il disco NON e- stato toccato",
          io.open(os.path.join(RADICE, "doc", "indice", "voci.jsonl"),
                  encoding="utf-8").read().count('"A17-PROVA-RINOMINA"') == 0,
          "### il collaudo lavora SUL PIANO: o tutto, o niente")
    print("=" * 100)
    print("IL COLLAUDO DI `rinomina`: %d su %d   %s"
          % (ok[0], ok[1], "### TUTTI PASSATI" if ok[0] == ok[1] else "### CI SONO BUCHI"))
    print("=" * 100)
    return 0 if ok[0] == ok[1] else 1


if __name__ == "__main__":
    sys.exit(collaudo())
