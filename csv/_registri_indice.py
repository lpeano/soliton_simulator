# -*- coding: utf-8 -*-
"""I QUATTRO REGISTRI DEI VOCABOLARI dell'indice `v2` — **GENERATI dalle fonti**.

`doc/indice/leggi.jsonl` · `variabili.jsonl` · `assiomi.jsonl` · `decisioni.jsonl`

### ⛔ **Nessuno dei quattro si scrive a mano:** ciascuno si ### **estrae dalla sua fonte**, e
lo script ### **ASSERISCE** che la fonte contenga cio' che si aspetta. ### ➜ **Se una fonte
cambia forma, il registro NON si scrive** invece di scriverne uno vecchio.

| registro | la fonte |
|---|---|
| `leggi.jsonl` | la ### **TAVOLA** di `csv/_test_fork/_doc_traduzione.py`, che genera `doc/TRADUZIONE_IN_H.md` |
| `variabili.jsonl` | la lista ### **`GIA_CENSITE`** di `csv/_test_fork/_censimento_leggi.py` *(le variabili di `doc/MEMORIE_MANCANTI.md`)*, piu' quelle ### **trovate dal censimento** |
| `assiomi.jsonl` | le intestazioni di ### **`doc/ASSIOMI.md`**, e i ### **sotto-punti** citati nel testo |
| `decisioni.jsonl` | le ### **schede** `<!-- SCHEDA nome=… -->` di `doc/REGISTRO_FISICA.md` che portano *«decisione di Luca»* |

Gira con:  python csv/_registri_indice.py
"""
import ast
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

# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Estrae dai sorgenti e dai
# documenti con l'AST e con espressioni, e il risultato non dipende da nessun flag.
NL = chr(10)
FUORI = os.path.join(RADICE, "doc", "indice")
P = []


def stampa(s=""):
    P.append(s)
    print(s, flush=True)


# ### ⛔ **DUE VIE DI SCRITTURA SU DUE FILE, E PRIMA NON C-ERA NESSUN ARBITRO.**
# ### `leggi.jsonl` e `variabili.jsonl` li ### **genera questo script**, leggendo le
# ### schede di `doc/REGISTRO_FISICA.md` *(l-era `1`)*; ### **ma gli stessi due file
# ### ricevono anche i record dell-era `2`** per la via dell-indice, con le loro righe
# ### in `storico_era2.jsonl`.
# ### ⚠ **MISURATO il 2026-10-10:** un giro di questo script ### **cancellava
# ### QUATTRO record** -- `PROVA-HOPPING`, `PROVA-LOCALE`, `PROVA-NORMA` e
# ### `V-PSI-ERA2` -- cioe- ### **esattamente quelli dell-era `2`**, perche- `scrivi()`
# ### apre in modo `w` e ### **riscrive da zero.**
# ### ⭐ **E CONTA PERCHE- IL CONTO DELLE LEGGI DI `primo_ordine/timbro.py` ESCE
# ### DALLA TABELLA:** un giro del generatore dell-era `1` lo avrebbe portato a
# ### ### **zero senza toccare un file di codice.**
# ### ✅ **L-ARBITRO, in una riga: cio- che l-ALTRA VIA ha dichiarato in uno
# ### storico NON SI TOCCA.** ### **La fonte dell-era `1` e- il REGISTRO_FISICA, la
# ### fonte dell-era `2` e- lo STORICO, e il file e- la somma delle due.**
STORICO_ERA2 = "storico_era2.jsonl"
DOVE_ERA2 = {"leggi.jsonl": "leggi", "variabili.jsonl": "variabili"}


def dell_era_2(nome):
    """### Gli ID che ### **l-altra via** ha scritto in questo registro."""
    dove = DOVE_ERA2.get(nome)
    if not dove:
        return set()
    p = os.path.join(FUORI, STORICO_ERA2)
    if not os.path.exists(p):
        return set()
    fuori = set()
    for r in io.open(p, encoding="utf-8").read().split(NL):
        if not r.strip():
            continue
        d = json.loads(r)
        if d.get("dove") == dove and d.get("id"):
            fuori.add(d["id"])
    return fuori


def _sul_disco(nome):
    """I record che ci sono ### **adesso**, per `id`."""
    p = os.path.join(FUORI, nome)
    if not os.path.exists(p):
        return {}
    return {d["id"]: d for d in (json.loads(r) for r in
                                 io.open(p, encoding="utf-8").read().split(NL) if r.strip())}


def scrivi(nome, righe):
    """### Una voce per riga, ### **ordinate per `id`**, chiavi in ordine fisso."""
    # ### ✅ **L-ARBITRO: i record dell-ALTRA VIA si TENGONO.**
    tenuti = dell_era_2(nome)
    if tenuti:
        ora = _sul_disco(nome)
        gia = {r["id"] for r in righe}
        persi = sorted(k for k in tenuti if k not in ora and k not in gia)
        # ### ⛔ **UN RECORD DELL-ALTRA VIA CHE NON E- NE- SUL DISCO NE- FRA I
        # ### GENERATI E- GIA- PERSO**, e questo script ### **non lo puo- ricostruire**:
        # ### si FERMA e dice come riaverlo. ### **Tacere qui vorrebbe dire scrivere il
        # ### file senza di lui, cioe- RENDERE DEFINITIVA la perdita.**
        assert not persi, (
            "### IL RECORD DELL-ERA 2 %s NON E- PIU- NEL FILE %s, e lo storico dice che "
            "c-era: NON POSSO RICOSTRUIRLO. ### Riprendilo coi byte committati -- "
            "`git cat-file -p HEAD:doc/indice/%s` -- e rilancia" % (persi, nome, nome))
        for k in sorted(tenuti - gia):
            righe = list(righe) + [ora[k]]
    righe = sorted(righe, key=lambda r: r["id"])
    ids = [r["id"] for r in righe]
    assert len(ids) == len(set(ids)), "id duplicati in %s: %s" % (
        nome, [x for x in ids if ids.count(x) > 1][:5])
    p = os.path.join(FUORI, nome)
    io.open(p, "w", encoding="utf-8", newline=NL).write(
        NL.join(json.dumps(r, ensure_ascii=False, sort_keys=False) for r in righe) + NL)
    stampa("  %-20s %4d voci%s" % (nome, len(righe),
                                     ("   (di cui %d TENUTI dall-altra via: l-era 2)"
                                      % len(tenuti)) if tenuti else ""))
    return len(righe)


def slug(s):
    """### Da un nome umano a un pezzo di ID: maiuscole, solo `A-Z0-9-`."""
    s = s.upper()
    s = re.sub(r"[ÀÁÂÃÄ]", "A", s)
    s = re.sub(r"[ÈÉÊË]", "E", s)
    s = re.sub(r"[ÌÍÎÏ]", "I", s)
    s = re.sub(r"[ÒÓÔÕÖ]", "O", s)
    s = re.sub(r"[ÙÚÛÜ]", "U", s)
    s = re.sub(r"[^A-Z0-9]+", "-", s)
    return s.strip("-")


# ==========================================================================
#   `1` LE LEGGI -- dalla TAVOLA del generatore di doc/TRADUZIONE_IN_H.md
# ==========================================================================
def leggi_le_leggi():
    src = io.open(os.path.join(_QUI, "_test_fork", "_doc_traduzione.py"),
                  encoding="utf-8").read()
    albero = ast.parse(src)
    tav = None
    for n in albero.body:
        if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) \
                and n.targets[0].id == "TAVOLA":
            tav = ast.literal_eval(n.value)
    assert tav, "la TAVOLA non si trova in _doc_traduzione.py"
    assert len(tav) >= 20, "la TAVOLA ha solo %d righe: la fonte e' cambiata" % len(tav)
    fuori = []
    for (nome, anc, var, classe, _ex, _esito) in tav:
        # ### l'ancora e' un NOME DI FUNZIONE o DI FLAG, MAI una riga
        ancora = anc.split("(")[0].strip().strip("`")
        fuori.append({
            "id": "L-" + slug(nome)[:40],
            "titolo": nome,
            "ancora": ancora,
            "variabile": var,
            "classe_traduzione": classe,
            "fonte": "doc/TRADUZIONE_IN_H.md::%s" % slug(nome)[:40],
        })
    return fuori


# ==========================================================================
#   `2` LE VARIABILI -- da GIA_CENSITE piu' il censimento
# ==========================================================================
def leggi_le_variabili():
    src = io.open(os.path.join(_QUI, "_test_fork", "_censimento_leggi.py"),
                  encoding="utf-8").read()
    albero = ast.parse(src)
    gia = None
    for n in albero.body:
        if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) \
                and n.targets[0].id == "GIA_CENSITE":
            gia = list(ast.literal_eval(n.value))
    assert gia and len(gia) >= 35, "GIA_CENSITE non si trova o e' cambiata"
    cen = json.load(io.open(os.path.join(_QUI, "_test_fork", "_censimento_leggi",
                                         "censimento.json"), encoding="utf-8"))
    scritte = {}
    for s in cen["scritture"]:
        scritte.setdefault(s["variabile"], []).append(s["funzione"])
    fuori = []
    for v in sorted(set(gia)):
        fuori.append({
            "id": "V-" + slug(v),
            "nome": v,
            "censita_in": "doc/MEMORIE_MANCANTI.md",
            "scritta_da": sorted(set(scritte.get(v, [])))[:6],
            "scritture": len(scritte.get(v, [])),
        })
    # ### e le QUATTRO trovate dal censimento e NON nel documento: si registrano,
    # ### perche' una voce potrebbe riferirsi a loro
    for v in ("xi_termo", "nati", "negate", "_cura4_maturi"):
        if v in scritte:
            fuori.append({"id": "V-" + slug(v), "nome": v,
                          "censita_in": "csv/_test_fork/_censimento_leggi (NON in "
                                        "doc/MEMORIE_MANCANTI.md)",
                          "scritta_da": sorted(set(scritte[v]))[:6],
                          "scritture": len(scritte[v])})
    return fuori


# ==========================================================================
#   `3` GLI ASSIOMI -- dalle intestazioni di doc/ASSIOMI.md
# ==========================================================================
def leggi_gli_assiomi():
    t = io.open(os.path.join(RADICE, "doc", "ASSIOMI.md"), encoding="utf-8").read()
    righe = t.split(NL)
    fuori, visti = [], set()
    for i, r in enumerate(righe, 1):
        m = re.match(r"^##\s+`?(A\d+)`?\s*[—-]", r)
        if not m:
            continue
        a = m.group(1)
        if a in visti:
            continue
        visti.add(a)
        tit = re.sub(r"^##\s+`?A\d+`?\s*[—-]\s*", "", r)
        tit = re.sub(r"[*#❗`]", "", tit).strip()
        fuori.append({"id": a, "titolo": tit[:100], "riga_fonte": i,
                      "fonte": "doc/ASSIOMI.md::%s" % a, "sotto_punti": []})
    assert len(fuori) >= 15, "trovati solo %d assiomi: la fonte e' cambiata" % len(fuori)
    # ### I SOTTO-PUNTI: si cercano NEL TESTO (`A14.2`, `A15.3`, `A16.1`, `A17.4`, `A3b`)
    per_id = {x["id"]: x for x in fuori}
    for m in re.finditer(r"\bA(\d+)\.(\d)\b", t):
        a, s = "A" + m.group(1), m.group(1) + "." + m.group(2)
        if a in per_id and ("A" + s) not in per_id[a]["sotto_punti"]:
            per_id[a]["sotto_punti"].append("A" + s)
    for x in fuori:
        x["sotto_punti"] = sorted(x["sotto_punti"])
    # ### le VARIANTI con lettera (`A3b`, `A3c`) si registrano come id a se'
    for m in sorted(set(re.findall(r"\bA(\d+[a-c])\b", t))):
        i2 = "A" + m
        if i2 not in per_id:
            fuori.append({"id": i2, "titolo": "(variante di A%s, citata nel testo)"
                          % re.sub(r"[a-c]", "", m), "riga_fonte": 0,
                          "fonte": "doc/ASSIOMI.md::%s" % i2, "sotto_punti": []})
    return fuori


# ==========================================================================
#   `4` LE DECISIONI -- dalle schede di doc/REGISTRO_FISICA.md
# ==========================================================================
def leggi_le_decisioni():
    t = io.open(os.path.join(RADICE, "doc", "REGISTRO_FISICA.md"), encoding="utf-8").read()
    pezzi = re.split(r"<!--\s*SCHEDA nome=([a-z0-9-]+)[^>]*-->", t)
    fuori = []
    # pezzi = [testa, nome1, corpo1, nome2, corpo2, ...]
    for k in range(1, len(pezzi) - 1, 2):
        nome, corpo = pezzi[k], pezzi[k + 1]
        m = re.search(r"[Dd]ecisione di Luca[^.]*?(\d{4}-\d{2}-\d{2})", corpo)
        m2 = re.search(r"DECISIONE DEL (\d{4}-\d{2}-\d{2})", corpo)
        data = (m.group(1) if m else (m2.group(1) if m2 else ""))
        if not re.search(r"[Dd]ecisione di Luca", corpo):
            continue                       # ### non e' una decisione: e' una scheda di legge
        tit = ""
        mt = re.search(r"^##\s+(.+)$", corpo, re.M)
        if mt:
            tit = re.sub(r"[*#⛔⭐❗`]", "", mt.group(1)).strip()
        presa = bool(re.search(r"PRESA", corpo))
        fuori.append({"id": "DEC-" + slug(nome), "nome_scheda": nome,
                      "titolo": tit[:100], "data": data, "presa": presa,
                      "fonte": "doc/REGISTRO_FISICA.md::SCHEDA nome=%s" % nome})
    # ### E GLI ASSIOMI SONO DECISIONI DI LUCA: `A16` e `A17` si registrano anche qui,
    # ### perche' una voce puo' essere SUPERATA DA un assioma.
    for a, data, tit in (("A16", "2026-10-08", "lo stato e' uno, ed evolve al primo ordine "
                                               "sotto una sola H"),
                         ("A17", "2026-10-08", "ogni comportamento e' determinato solo dal "
                                               "suo ambito: niente pos nella fisica")):
        fuori.append({"id": "DEC-" + a, "nome_scheda": "", "titolo": tit, "data": data,
                      "presa": True, "fonte": "doc/ASSIOMI.md::%s" % a})
    # ### ✅ **E I NODI DELL-ALBERO DELLE SCELTE, da `doc/ALBERO_era2.yaml`.**
    # ### ⛔ **Entrano QUI, PER GENERAZIONE, e non a mano:** `decisioni.jsonl` e-
    # ### ### **un file generato** -- un nodo scritto a mano la- dentro
    # ### ### **sarebbe cancellato al primo giro** *(misurato il 2026-10-10,
    # ### `DUE-VIE-SU-LEGGI-JSONL`)*. ### **La fonte dell-albero e- il `yaml`, e il
    # ### presidio che lo valida e- `P-ALB`.**
    # ### ⚠ **E UN NODO DELL-ALBERO PORTA TRE CAMPI IN PIU-** -- `etichetta`,
    # ### `dipende_da`, `argomento_noto` -- ### **che i record dell-era `1` non hanno.**
    # ### **Lo dichiaro invece di uniformare:** `dipende_da` su una decisione dell-era
    # ### `1` sarebbe ### **una lista vuota inventata**, e l-`etichetta` locale
    # ### ### **non esiste** per loro. ### **Un campo assente dice <<non si applica>>;
    # ### un campo vuoto direbbe <<nessuna dipendenza>>, che e- un-altra cosa.**
    import _albero_era2
    alb, _radici = _albero_era2.carica()
    rotto = _albero_era2.controlla(alb, _radici)
    assert not rotto, ("### L-ALBERO NON PASSA `P-ALB` e NON LO GENERO: %s"
                       % rotto[:2])
    for n in alb:
        riga = {"id": n["id"], "nome_scheda": "", "titolo": n["titolo"][:100],
                "data": "2026-10-10", "presa": bool(n["presa"]),
                "fonte": n["fonte"], "etichetta": n["etichetta"],
                "dipende_da": list(n["dipende_da"]),
                "argomento_noto": bool(n["argomento_noto"])}
        # ### \u2705 **`superata_da` SOLO DOVE C-E-, dal `2026-10-10`** *(decisione di
        # ### Luca)*, e per la ragione che questo file dichiara otto righe sopra:
        # ### ### **un campo assente dice <<non si applica>>, un campo vuoto direbbe
        # ### <<niente la supera>>** -- e sono due cose diverse.
        # ### \u26a0 **E COSI- LA MIGRAZIONE NON TOCCA LE ALTRE RIGHE:** e- la lezione
        # ### di `527e70c`, dove aggiungere tre campi a tutte le voci ### **ha spento un
        # ### confronto col passato in silenzio.**
        if n.get("superata_da"):
            riga["superata_da"] = n["superata_da"]
        fuori.append(riga)
    assert len(fuori) >= 5, "trovate solo %d decisioni: la fonte e' cambiata" % len(fuori)
    return fuori


def main():
    # ### ⛔ **`P` SI SVUOTA A OGNI GIRO, e me l-ha insegnato un file COMMITTATO
    # ### INQUINATO:** `collaudo()` chiama `main()` ### **quattro volte**, e `P` e- una
    # ### lista di MODULO -- quindi `_registri.txt` si ritrovava con ### **quattro
    # ### intestazioni** e il file committato in `4553d6a` le portava.
    # ### ⭐ **Un generatore che ACCUMULA non e- idempotente**, e l-idempotenza e-
    # ### esattamente cio- che la CI misura col `git diff`.
    del P[:]
    os.makedirs(FUORI, exist_ok=True)
    stampa("=" * 104)
    stampa("I QUATTRO REGISTRI DEI VOCABOLARI -- generati dalle fonti, non scritti a mano")
    stampa("  le fonti: doc/REGISTRO_FISICA.md, doc/ASSIOMI.md, doc/ALBERO_era2.yaml,")
    stampa("            primo_ordine/leggi/leggi.yaml, e doc/indice/storico_era2.jsonl")
    stampa("=" * 104)
    n1 = scrivi("leggi.jsonl", leggi_le_leggi())
    n2 = scrivi("variabili.jsonl", leggi_le_variabili())
    n3 = scrivi("assiomi.jsonl", leggi_gli_assiomi())
    n4 = scrivi("decisioni.jsonl", leggi_le_decisioni())
    stampa()
    stampa("  in tutto: %d ID di vocabolario" % (n1 + n2 + n3 + n4))
    io.open(os.path.join(FUORI, "_registri.txt"), "w", encoding="utf-8",
            newline=NL).write(NL.join(P) + NL)
    return 0


def collaudo():
    """### L-ARBITRO fra le due vie, ### **nei due versi.**

    ### ⛔ **IL CASO CHE DEVE FALLIRE SI COSTRUISCE DAI DATI VERI** (`P1-sexies`):
    si toglie ### **un record dell-era `2`** dal file, si fa girare il generatore, e
    ### **si pretende che SI FERMI** -- poi si rimette, e si verifica che il file sia
    tornato ### **identico al byte.**
    """
    import hashlib
    ok = [0, 0]

    def esito(che, passa, nota=""):
        ok[1] += 1
        ok[0] += 1 if passa else 0
        print("  %-62s %s   %s" % (che, "PASSA" if passa else "### FALLISCE", nota))

    print("=" * 100)
    print("IL COLLAUDO DELL-ARBITRO fra le DUE VIE -- nei DUE VERSI")
    print("=" * 100)
    nomi = sorted(DOVE_ERA2)
    tutti = {n: sorted(dell_era_2(n)) for n in nomi}
    for n in nomi:
        print("  %-20s id dell-era 2: %s" % (n, ", ".join(tutti[n]) or "nessuno"))
    esito("### il collaudo ha MATERIA: ci sono record dell-altra via",
          sum(len(v) for v in tutti.values()) > 0,
          "%d in tutto: ### senza di loro questo collaudo non proverebbe NIENTE"
          % sum(len(v) for v in tutti.values()))

    # ------------------------------------------------- 1) IDEMPOTENZA, al byte
    main()
    b1 = {n: io.open(os.path.join(FUORI, n), "rb").read() for n in nomi}
    main()
    b2 = {n: io.open(os.path.join(FUORI, n), "rb").read() for n in nomi}
    esito("NON deve scattare: DUE giri di seguito danno gli STESSI BYTE",
          b1 == b2,
          "### un generatore che non e- idempotente non si puo- mettere in una CI col "
          "`git diff`")
    for n in nomi:
        d = set(_sul_disco(n))          # ### le CHIAVI sono gli `id`
        esito("NON deve scattare: `%s` contiene TUTTI i record dell-altra via" % n,
              set(tutti[n]) <= d,
              "%d su %d: ### e- la cancellazione che un giro FACEVA, e adesso non fa piu-"
              % (len(set(tutti[n]) & d), len(tutti[n])))

    # ------------------------------------------------- 2) il caso che DEVE GRIDARE
    n = next((x for x in nomi if tutti[x]), None)
    p = os.path.join(FUORI, n)
    b0 = io.open(p, "rb").read()
    sha0 = hashlib.sha1(b0).hexdigest()
    try:
        vittima = tutti[n][0]
        resto = [r for r in io.open(p, encoding="utf-8").read().split(NL)
                 if r.strip() and json.loads(r)["id"] != vittima]
        io.open(p, "w", encoding="utf-8", newline=NL).write(NL.join(resto) + NL)
        gridato = False
        try:
            main()
        except AssertionError as e:
            gridato = "NON E- PIU- NEL FILE" in str(e)
        esito("### DEVE scattare: un record dell-altra via GIA- PERSO FERMA il generatore",
              gridato,
              "`%s` tolto da `%s`: ### tacere qui vorrebbe dire scrivere il file senza di "
              "lui, cioe- RENDERE DEFINITIVA la perdita" % (vittima, n))
    finally:
        io.open(p, "wb").write(b0)
        main()
    esito("### e il file e- tornato IDENTICO AL BYTE",
          hashlib.sha1(io.open(p, "rb").read()).hexdigest() == sha0,
          "`%s`: ### un collaudo che lascia danno non e- un collaudo" % sha0[:8])
    print("=" * 100)
    print("IL COLLAUDO DELL-ARBITRO: %d su %d   %s"
          % (ok[0], ok[1], "### TUTTI PASSATI" if ok[0] == ok[1] else "### CI SONO BUCHI"))
    print("=" * 100)
    return 0 if ok[0] == ok[1] else 1


if __name__ == "__main__":
    if "--collaudo" in sys.argv[1:]:
        sys.exit(collaudo())
    sys.exit(main())
