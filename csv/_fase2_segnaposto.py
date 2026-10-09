# -*- coding: utf-8 -*-
"""FASE 2, PUNTO 3: I SEGNAPOSTO (`NON_DEFINITA`) — **uno dei tre esiti, letto dalle
citazioni.**

| esito | come si decide | |
|---|---|---|
| ### **ALIAS** | l'id ### **ripulito dalla punteggiatura finale** coincide con un id o un alias di una voce VERA *(`CONFIG-1/` → `CONFIG-1`)* | esce da `voci.jsonl` e diventa un ### **alias** |
| ### **ETICHETTA DI DOCUMENTO** | ### **tutte** le citazioni stanno in ### **documenti** o in ### **strumenti dell'indice** *(`doc/LISTA_CHIUSA.md`, `csv/_cure_verificate.py`)*: sono ### **marcatori di sezione e titoli** *(`CURE-INIZIO`, `DOVE-VA`, `AAAA-MM-GG`)* | esce da `voci.jsonl`, va in ### **`etichette_rimosse.jsonl`** |
| ### **CONCETTO DA DEFINIRE** | e' citato ### **nel CODICE o nei SIGILLI** *(`soliton_simulator.py`, le sue copie `_sim_*`, `csv/_test_fork/`, `csv/_seal_fork/`)*: ### **il codice stesso lo nomina** | ### **RESTA**, con in `nota_guardiano` ### **dove e' nominato** |

### ⛔ **E LA CONSERVAZIONE SI MANTIENE:** ogni id che esce da `voci.jsonl` ### **entra in
`etichette_rimosse.jsonl` o fra gli alias**, e ### **`migrazione_era1.jsonl` riceve la riga
nuova** con la regola.

Gira con:  python csv/_fase2_segnaposto.py [--collaudo]
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
import indice as IX                                          # noqa: E402

# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Sposta voci dell'indice.
NL = chr(10)
D = os.path.join(RADICE, "doc", "indice")
LOTTI = os.path.join(D, "_lotti")
DATA = "2026-10-09"

# ### GLI STRUMENTI DELL'INDICE: una citazione LI' e' CONTABILITA', non una definizione.
STRUM = ("csv/_indice_riordino.py", "csv/_cure_verificate.py", "csv/_lista_chiusa.py",
         "csv/_punto_della_situazione.py", "csv/_indice_id.py", "csv/indice.py",
         "csv/_analisi_lettori_indice.py", "csv/_collisioni_id.py",
         "csv/_blob_nelle_voci.py", "csv/_confronto_pds.py", "csv/_archivio_relazioni.py",
         "csv/_registri_indice.py", "csv/migra_indice_v2.py", "csv/_fase2_segnaposto.py",
         "csv/_fase2_lotti.py", "csv/_fase2_lettura.py", "csv/_fase2_chiuse.py",
         "csv/_fase2_correzioni.py", "csv/_controlli_indice_v2.py",
         "csv/_doc_referto_indice.py", "csv/_censimento_non_tracciati.py")
RADICI_DOC = ("doc/", "CLAUDE.md", "README.md", "RELAZIONE_PER_CLAUDE.md",
              "CLAUDECONNECT.md", "STATO_CLAUDE_fork-su2.md", "ROADMAP_dev-spinoriale.md")
# ### I SETTE che il censimento lascia fuori dai due gruppi: li decido LEGGENDOLI.
A_MANO = {
    "AAAA-MM-GG": ("ETICHETTA", "e' il FORMATO DI UNA DATA, citato in `CLAUDE.md` e negli "
                                "script: non e' un ID, e' un segnaposto di formato"),
    "DA-DECIDERE": ("ETICHETTA", "e' un VALORE della vecchia colonna `stato`, non una voce"),
    "QQ777": ("ETICHETTA", "e' un marcatore di PROVA degli strumenti"),
    "ZZ999": ("ETICHETTA", "e' un marcatore di PROVA degli strumenti"),
    "QUADRO-INIZIO": ("ETICHETTA", "e' un MARCATORE DI SEZIONE di un documento"),
    "QUADRO-FINE": ("ETICHETTA", "e' un MARCATORE DI SEZIONE di un documento"),
    "RIDUZIONE-AL-LIMITE": ("CONCETTO", "e' la PROPRIETA' dichiarata dello spinore -- <<con "
                                        "`_psi_spinor=(e^{i phi},0)` la componente 0 == "
                                        "campo scalare>> -- e il codice la nomina. E' il "
                                        "soggetto di `CENS-A1`"),
}


def main(argv):
    collaudo = "--collaudo" in argv
    voci = [json.loads(r) for r in io.open(os.path.join(D, "voci.jsonl"), encoding="utf-8")
            if r.strip()]
    etich = [json.loads(r) for r in
             io.open(os.path.join(D, "etichette_rimosse.jsonl"), encoding="utf-8")
             if r.strip()]
    per = {v["id"]: v for v in voci}
    veri = set()
    for v in voci:
        if v["classe"] != "NON_DEFINITA":
            veri.add(v["id"])
            veri |= set(v["alias"])
    seg = [v for v in voci if v["classe"] == "NON_DEFINITA"]

    def files(v):
        return (v["meta"] or {}).get("file_citanti") or []

    def pulisci(i):
        return re.sub(r"[^A-Za-z0-9]+$", "", i)

    def nel_codice(v):
        return any(x == "soliton_simulator.py" or "_sim_" in x
                   or (x.startswith(("csv/_test_fork/", "csv/_seal_fork/"))
                       and x not in STRUM)
                   for x in files(v))

    def solo_doc_o_strumenti(v):
        f = files(v)
        return bool(f) and all(x in STRUM or x.startswith(RADICI_DOC) for x in f)

    alias, etichette, concetti = [], [], []
    for v in sorted(seg, key=lambda x: x["id"]):
        i = v["id"]
        if i in A_MANO:
            esito, perche = A_MANO[i]
            (etichette if esito == "ETICHETTA" else concetti).append((v, perche))
            continue
        p = pulisci(i)
        if p != i and p in veri:
            alias.append((v, p))
            continue
        if nel_codice(v):
            concetti.append((v, None))
            continue
        if solo_doc_o_strumenti(v):
            etichette.append((v, None))
            continue
        concetti.append((v, "citato in modo non classificabile: resta un CONCETTO"))

    print("=" * 96)
    print("I SEGNAPOSTO: %d" % len(seg))
    print("=" * 96)
    print("  ALIAS di una voce vera:        %3d   %s"
          % (len(alias), " ".join(v["id"] for v, _ in alias)))
    print("  ETICHETTA DI DOCUMENTO:        %3d" % len(etichette))
    print("  CONCETTO DA DEFINIRE (resta):  %3d" % len(concetti))
    if collaudo:
        print()
        print("  --collaudo: NON HO SCRITTO NIENTE.")
        return 0

    # ---------------------------------------------- `1` gli ALIAS
    tracce = []
    for v, bersaglio in alias:
        per[bersaglio]["alias"] = sorted(set(per[bersaglio]["alias"] + [v["id"]]))
        tracce.append({"id_vecchio": v["id"],
                       "dove": "voci.jsonl::alias di %s" % bersaglio,
                       "regola": "(fase2-b1) l'id RIPULITO dalla punteggiatura finale "
                                 "coincide con `%s`: e' lo stesso oggetto" % bersaglio})
    # ---------------------------------------------- `2` le ETICHETTE
    for v, perche in etichette:
        m = v["meta"] or {}
        etich.append({"id": v["id"], "citazioni_n": m.get("citazioni_n", 0),
                      "file_citanti": files(v)[:12],
                      "regola": ("(fase2-b2) %s" % (perche or
                                 "TUTTE le citazioni stanno in documenti o in strumenti "
                                 "dell'indice: e' un MARCATORE o un TITOLO, non una voce")),
                      "titolo_era1": v["titolo"][:100]})
        tracce.append({"id_vecchio": v["id"], "dove": "etichette_rimosse.jsonl",
                       "regola": "(fase2-b2) etichetta di documento, deciso dalle CITAZIONI"})
    fuori = {v["id"] for v, _ in alias} | {v["id"] for v, _ in etichette}
    voci = [v for v in voci if v["id"] not in fuori]

    IX._scrivi_jsonl(IX.VOCI, voci)
    IX._scrivi_jsonl(os.path.join(D, "etichette_rimosse.jsonl"), etich)
    io.open(os.path.join(D, "migrazione_era1.jsonl"), "a", encoding="utf-8",
            newline=NL).write(NL.join(json.dumps(x, ensure_ascii=False)
                                      for x in tracce) + NL)
    v2, r2 = IX.carica()
    IX.viste(v2, r2)
    err = IX.valida(v2, r2, verboso=False)
    assert not err, "LA VALIDAZIONE FALLISCE:" + NL + NL.join(err[:8])

    # ---------------------------------------------- `3` i CONCETTI: il lotto
    lotto = []
    for v, perche in concetti:
        f = files(v)
        dove = " ".join(f[:3])
        lotto.append({"id": v["id"], "quando": DATA, "campi": {},
                      "meta": {"nota_guardiano":
                               ("CONCETTO DA DEFINIRE: %s. Nominato in: %s"
                                % (perche or "il CODICE o i SIGILLI lo nominano",
                                   dove))[:300]},
                      "motivo": ("(fase2-b3) `%s` resta un CONCETTO DA DEFINIRE: e' citato "
                                 "%d volte, e fra i file che lo nominano ci sono <<%s>> -- "
                                 "cioe' il codice o i sigilli, non solo i documenti"
                                 % (v["id"], (v["meta"] or {}).get("citazioni_n") or 0,
                                    dove))})
    p = os.path.join(LOTTI, "segnaposto_concetti.jsonl")
    io.open(p, "w", encoding="utf-8", newline=NL).write(
        NL.join(json.dumps(x, ensure_ascii=False) for x in lotto) + NL)
    print()
    print("  scritto: voci.jsonl (%d), etichette_rimosse.jsonl (%d), +%d righe di traccia"
          % (len(voci), len(etich), len(tracce)))
    print("  e il lotto dei concetti: %s (%d voci)"
          % (os.path.relpath(p, RADICE).replace(chr(92), "/"), len(lotto)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
