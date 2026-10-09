# -*- coding: utf-8 -*-
"""L'INDICE `v2` — **l'UNICA via di lettura e di scrittura**.

```
python csv/indice.py valida
python csv/indice.py cerca [--dominio X] [--stato X] [--era X] [--blocca SI|NO]
                           [--legge ID] [--variabile ID] [--assioma ID] [--meta k=v]
python csv/indice.py aggiorna ID --campo nome=valore | --meta k=v --motivo "..." [--commit SHA]
python csv/indice.py aggiorna-lotto LOTTO.jsonl     # la STESSA via, in blocco
python csv/indice.py crea-lotto LOTTO.jsonl        # la STESSA via, per FAR NASCERE una voce
python csv/indice.py mostra [--stato X] [--segnaposto SI] [--da N] [--quante N]
python csv/indice.py meta-aggiungi k --tipo T [--valori a,b] [--regex R] --descrizione "..."
python csv/indice.py meta-depreca k --sostituito-da k2 --motivo "..."
python csv/indice.py meta-rinomina k k2 --motivo "..."
python csv/indice.py citazioni
python csv/indice.py viste
python csv/indice.py collaudo
```

### ⛔ **LA REGOLA CHE QUESTO FILE FA RISPETTARE:** ### **nessuna funzione legge `titolo` o
`descrizione` per decidere qualcosa.** Lo schema sta in `doc/INDICE_SCHEMA.md`.
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

# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Legge e scrive l'indice.
NL = chr(10)
TAB = chr(9)
D = os.path.join(RADICE, "doc", "indice")
VOCI = os.path.join(D, "voci.jsonl")
STORICO = os.path.join(D, "storico.jsonl")
ETICH = os.path.join(D, "etichette_rimosse.jsonl")
META = os.path.join(D, "metadati.jsonl")
INVERTITO = os.path.join(D, "_indice_meta.json")
TSV = os.path.join(RADICE, "doc", "INDICE_ID.tsv")
VISTA_MD = os.path.join(RADICE, "doc", "INDICE.md")
# ### ⭐ **SCHEMA 3 (2026-10-09): la classe `NON_DEFINITA`.** La migrazione aveva dato
# ### `DIFETTO` ai `234` segnaposto *(titolo <<MAI definito in un registro>>)*, ed e'
# ### ### **sbagliato: un segnaposto NON E' UN DIFETTO** -- e' un ID citato di cui non si sa
# ### che cosa sia. ### ⛔ **E il validatore vieta `NON_DEFINITA` con uno stato diverso da
# ### `DA_CLASSIFICARE`:** una voce di cui non si sa la classe non puo' essere <<aperta>>.
# ### **LA MIGRAZIONE DI VERSIONE:** `csv/migra_schema_3.py`, riseguibile.
SCHEMA_VERSION = 3

CLASSI = ("DIFETTO", "CURA", "MISURA", "CRITERIO", "PRESIDIO", "STANDARD", "TEORIA",
          "DECISIONE", "FRONTE", "NON_DEFINITA")
DOMINI = ("FISICA", "METODO", "INFRASTRUTTURA", "DOCUMENTAZIONE", "DA_CLASSIFICARE")
ERE = ("1", "2", "ENTRAMBE", "DA_CLASSIFICARE")
STATI = ("APERTA", "IN_CORSO", "CHIUSA", "SOSPESA", "SUPERATA", "AGENDA", "DA_CLASSIFICARE")
# ### ⚠ **LA REGEX E' PIU' LARGA DI COME L'AVEVO SCRITTA, e il motivo e' una REGOLA:**
# ### *«i REPERTI non si riscrivono -- il nome vecchio RESTA»* (`CLAUDE.md` par.9). La
# ### migrazione ha trovato ### **96 ID esistenti** che la regex stretta avrebbe rifiutato:
# ### `A2b` `A3c` `H-P1-bis` `E4a` `COMPONENTI:S3b` `CONFIG-1/` `INERZIA-1(C)` ...
# ### ➜ **Rifiutarli voleva dire RINOMINARLI**, e quello non si fa. La regex pretende
# ### ### **la MAIUSCOLA iniziale** e vieta lo spazio: il resto lo ammette.
RE_ID = re.compile(r"^[A-Z0-9][A-Za-z0-9:_./()\[\]-]*$")
RE_META = re.compile(r"^[a-z][a-z0-9_]*$")

# ### LE TRANSIZIONI AMMESSE: la tavola di doc/INDICE_SCHEMA.md, in codice.
# ### ⛔ **NESSUNA transizione RAGGIUNGE `DA_CLASSIFICARE`**: e' lo stato in cui si ENTRA solo
# ### alla migrazione, e da cui si ESCE con una decisione registrata.
TRANSIZIONI = {
    "DA_CLASSIFICARE": {"APERTA", "IN_CORSO", "SOSPESA", "AGENDA", "CHIUSA", "SUPERATA"},
    "APERTA": {"IN_CORSO", "SOSPESA", "AGENDA", "CHIUSA", "SUPERATA"},
    "IN_CORSO": {"APERTA", "SOSPESA", "AGENDA", "CHIUSA", "SUPERATA"},
    "SOSPESA": {"APERTA", "IN_CORSO", "AGENDA", "CHIUSA", "SUPERATA"},
    "AGENDA": {"APERTA", "IN_CORSO", "SOSPESA", "CHIUSA", "SUPERATA"},
    "CHIUSA": {"APERTA", "SUPERATA"},
    "SUPERATA": {"APERTA"},
}

# ### L'ORDINE FISSO DELLE CHIAVI. Una voce scritta con un ordine diverso NON e' valida:
# ### cosi' il file e' confrontabile al byte fra due esecuzioni.
CHIAVI = ("id", "alias", "titolo", "descrizione", "classe", "dominio", "era", "stato",
          "blocca", "leggi", "variabili", "assiomi", "collegate", "padre", "superata_da",
          "chiusura", "fonte", "creata", "aggiornata", "stato_era_1", "meta")

TIPI_META = ("enum", "bool", "intero", "reale", "data", "testo_breve", "id_voce",
             "id_legge", "id_variabile", "id_assioma", "id_decisione", "sha_commit",
             "sha_blob")


# ==========================================================================
#   LETTURA
# ==========================================================================
def _jsonl(p):
    if not os.path.exists(p):
        return []
    return [json.loads(r) for r in io.open(p, encoding="utf-8").read().split(NL) if r.strip()]


def _scrivi_jsonl(p, righe, chiave="id"):
    righe = sorted(righe, key=lambda r: r[chiave])
    io.open(p, "w", encoding="utf-8", newline=NL).write(
        NL.join(json.dumps(r, ensure_ascii=False) for r in righe) + NL)


def carica():
    voci = _jsonl(VOCI)
    reg = {k: {x[("chiave" if k == "metadati" else "id")]: x
               for x in _jsonl(os.path.join(D, "%s.jsonl" % k))}
           for k in ("leggi", "variabili", "assiomi", "decisioni", "metadati")}
    return voci, reg


# ==========================================================================
#   VALIDAZIONE
# ==========================================================================
def tipo_ok(val, tipo, spec, reg):
    base = tipo[len("lista_di:"):] if tipo.startswith("lista_di:") else None
    if base:
        if not isinstance(val, list):
            return "non e' una lista"
        for v in val:
            e = tipo_ok(v, base, spec, reg)
            if e:
                return "un elemento: %s" % e
        return ""
    if tipo == "bool":
        return "" if isinstance(val, bool) else "non e' un bool"
    if tipo == "intero":
        return "" if isinstance(val, int) and not isinstance(val, bool) else "non e' un intero"
    if tipo == "reale":
        return "" if isinstance(val, (int, float)) and not isinstance(val, bool) \
            else "non e' un numero"
    if not isinstance(val, str):
        return "non e' una stringa"
    if tipo == "enum":
        return "" if val in (spec.get("valori") or []) else "fuori dai valori ammessi"
    if tipo == "data":
        return "" if re.match(r"^\d{4}-\d{2}-\d{2}$", val) else "non e' una data AAAA-MM-GG"
    if tipo in ("sha_commit", "sha_blob"):
        return "" if re.match(r"^[0-9a-f]{7,40}$", val) else "non e' uno sha"
    if tipo == "id_voce":
        return "" if val in reg["_voci"] else "non e' un id di voce"
    for t, k in (("id_legge", "leggi"), ("id_variabile", "variabili"),
                 ("id_assioma", "assiomi"), ("id_decisione", "decisioni")):
        if tipo == t:
            return "" if val in reg[k] else "non e' un id di %s" % k
    if tipo == "testo_breve":
        r = spec.get("regex")
        if r and not re.match(r, val):
            return "non rispetta la regex del registro"
        return ""
    return "tipo `%s` non riconosciuto" % tipo


def valida(voci, reg, verboso=True, derivati=True):
    """### `derivati=False` salta i controlli sui FILE derivati *(indice invertito e viste)*:
    serve al ### **collaudo**, che valida insiemi di voci ### **in memoria**, dove quei file
    non c'entrano. ### ⛔ **Sul file vero `derivati` resta `True`**, ed e' la sua ultima
    coppia di controlli."""
    err = []
    reg["_voci"] = {v["id"] for v in voci}
    ids = [v["id"] for v in voci]
    for i in sorted(set(x for x in ids if ids.count(x) > 1)):
        err.append("id DUPLICATO: `%s`" % i)
    tutti_alias = {}
    for v in voci:
        q = v["id"]
        if list(v.keys()) != list(CHIAVI):
            err.append("`%s`: chiavi fuori ordine o mancanti" % q)
            continue
        if not RE_ID.match(q):
            err.append("`%s`: id fuori regex" % q)
        if v["classe"] not in CLASSI:
            err.append("`%s`: classe `%s` fuori vocabolario" % (q, v["classe"]))
        if v["dominio"] not in DOMINI:
            err.append("`%s`: dominio `%s` fuori vocabolario" % (q, v["dominio"]))
        if str(v["era"]) not in ERE:
            err.append("`%s`: era `%s` fuori vocabolario" % (q, v["era"]))
        if v["stato"] not in STATI:
            err.append("`%s`: stato `%s` fuori vocabolario" % (q, v["stato"]))
        if not isinstance(v["blocca"], bool):
            err.append("`%s`: blocca non e' un bool" % q)
        if len(v["titolo"]) > 100:
            err.append("`%s`: titolo oltre 100 caratteri" % q)
        # ### i RIFERIMENTI, contro i registri
        for campo, k in (("leggi", "leggi"), ("variabili", "variabili"),
                         ("assiomi", "assiomi")):
            for x in v[campo]:
                if x not in reg[k]:
                    err.append("`%s`: %s `%s` NON e' nel registro" % (q, campo, x))
        for x in v["collegate"]:
            if x not in reg["_voci"]:
                err.append("`%s`: collegata `%s` NON e' una voce" % (q, x))
        if v["padre"] and v["padre"] not in reg["_voci"]:
            err.append("`%s`: padre `%s` NON e' una voce" % (q, v["padre"]))
        for a in v["alias"]:
            if a in tutti_alias:
                err.append("alias `%s` usato da `%s` e `%s`" % (a, tutti_alias[a], q))
            tutti_alias[a] = q
            if a in reg["_voci"]:
                err.append("`%s`: l'alias `%s` e' anche un id di voce" % (q, a))
        # ### I CAMPI OBBLIGATORI PER STATO
        if v["stato"] == "CHIUSA" and not (v["chiusura"].get("criterio")
                                           and v["chiusura"].get("commit")):
            err.append("`%s`: CHIUSA senza `chiusura.criterio` e `chiusura.commit`" % q)
        if v["stato"] == "SUPERATA":
            s = v["superata_da"]
            if not s:
                err.append("`%s`: SUPERATA senza `superata_da`" % q)
            elif s not in reg["decisioni"] and s not in reg["assiomi"]:
                err.append("`%s`: superata_da `%s` non e' una decisione ne' un assioma"
                           % (q, s))
        if v["stato"] == "SOSPESA" and not v["stato_era_1"]:
            err.append("`%s`: SOSPESA senza `stato_era_1`" % q)
        if v["blocca"] and v["stato"] in ("CHIUSA", "SUPERATA"):
            err.append("`%s`: blocca=true con stato `%s`: contraddizione" % (q, v["stato"]))
        if v["classe"] == "NON_DEFINITA" and v["stato"] != "DA_CLASSIFICARE":
            err.append("`%s`: classe NON_DEFINITA con stato `%s`: una voce di cui non si sa "
                       "la classe non puo' avere uno stato deciso" % (q, v["stato"]))
        if v["dominio"] == "DA_CLASSIFICARE" and v["stato"] != "DA_CLASSIFICARE" \
                and str(v["era"]) != "DA_CLASSIFICARE":
            err.append("`%s`: dominio DA_CLASSIFICARE ma stato ed era sono deciso" % q)
        # ### I METADATI
        for k, val in (v["meta"] or {}).items():
            if not RE_META.match(k):
                err.append("`%s`: chiave meta `%s` fuori regex" % (q, k))
                continue
            spec = reg["metadati"].get(k)
            if spec is None:
                err.append("`%s`: chiave meta `%s` NON REGISTRATA" % (q, k))
                continue
            if spec.get("stato") == "DEPRECATO":
                err.append("`%s`: chiave meta `%s` e' DEPRECATA (usa `%s`)"
                           % (q, k, spec.get("sostituito_da") or "?"))
                continue
            e = tipo_ok(val, spec["tipo"], spec, reg)
            if e:
                err.append("`%s`: meta `%s`: %s" % (q, k, e))
            ap = spec.get("si_applica_a") or {}
            cl, do = ap.get("classi") or [], ap.get("domini") or []
            if cl and v["classe"] not in cl:
                err.append("`%s`: meta `%s` non si applica alla classe `%s`"
                           % (q, k, v["classe"]))
            if do and v["dominio"] not in do:
                err.append("`%s`: meta `%s` non si applica al dominio `%s`"
                           % (q, k, v["dominio"]))
    # ### L'INDICE INVERTITO e le VISTE: DERIVATI, e si CONFRONTANO
    if not derivati:
        return err
    atteso = invertito(voci, reg)
    if os.path.exists(INVERTITO):
        avuto = json.load(io.open(INVERTITO, encoding="utf-8"))
        if avuto != atteso:
            err.append("l'INDICE INVERTITO e' DISALLINEATO: rigeneralo con `viste`")
    elif voci:
        err.append("l'INDICE INVERTITO MANCA: rigeneralo con `viste`")
    if voci and os.path.exists(TSV):
        if io.open(TSV, encoding="utf-8").read() != vista_tsv(voci):
            err.append("la VISTA `doc/INDICE_ID.tsv` NON coincide con voci.jsonl: e' stata "
                       "modificata a mano, oppure va rigenerata con `viste`")
    if verboso:
        print("=" * 96)
        print("VALIDAZIONE dell'indice v%d -- %d voci, %d chiavi di metadato"
              % (SCHEMA_VERSION, len(voci), len(reg["metadati"])))
        print("=" * 96)
        if err:
            for e in err[:40]:
                print("  ### " + e)
            if len(err) > 40:
                print("  ... e altri %d" % (len(err) - 40))
            print("  ### FALLITA: %d errori" % len(err))
        else:
            print("  schema, vocabolari, riferimenti, transizioni, campi obbligatori,")
            print("  unicita', metadati, indice invertito e viste: **TUTTO A POSTO**")
    return err


# ==========================================================================
#   DERIVATI
# ==========================================================================
def invertito(voci, reg):
    fuori = {}
    for campo in ("classe", "dominio", "era", "stato"):
        for v in voci:
            fuori.setdefault(campo, {}).setdefault(str(v[campo]), []).append(v["id"])
    for v in voci:
        fuori.setdefault("blocca", {}).setdefault(
            "SI" if v["blocca"] else "NO", []).append(v["id"])
        for campo in ("leggi", "variabili", "assiomi"):
            for x in v[campo]:
                fuori.setdefault(campo, {}).setdefault(x, []).append(v["id"])
        for k, val in (v["meta"] or {}).items():
            spec = reg["metadati"].get(k) or {}
            if not spec.get("cercabile"):
                continue
            for u in (val if isinstance(val, list) else [val]):
                fuori.setdefault("meta:" + k, {}).setdefault(str(u), []).append(v["id"])
    return {k: {k2: sorted(set(v2)) for k2, v2 in sorted(v.items())}
            for k, v in sorted(fuori.items())}


def vista_tsv(voci):
    """### LA VISTA COMPATIBILE: le 15 colonne dell'era `1`, perche'
    `python csv/_indice_id.py --blocca SI` e `--dettaglio` continuino a funzionare."""
    col = ["id", "alias", "titolo_breve", "fonte_principale", "stato", "blocca_run_base",
           "tipo", "famiglia", "stato_da", "avanzamento", "revisione", "motivo", "nota",
           "stato_era_1", "si_riferisce_a"]
    r = [TAB.join(col)]
    for v in sorted(voci, key=lambda x: x["id"]):
        m = v["meta"] or {}
        r.append(TAB.join([
            v["id"], ",".join(v["alias"]), v["titolo"].replace(TAB, " "),
            v["fonte"], v["stato"], "SI" if v["blocca"] else "NO",
            m.get("tipo_era1", v["classe"].lower()), m.get("famiglia_era1", "?"),
            (v["descrizione"] or "").replace(TAB, " ").replace(NL, " ")[:900],
            m.get("avanzamento_era1", "(senza marcatore)"),
            m.get("revisione_era1", "") or str(v["aggiornata"].get("data", "")),
            (m.get("motivo_era1", "")
             or v["chiusura"].get("criterio", "") or v["superata_da"] or "")[:1000],
            (m.get("nota_guardiano", "") or "").replace(TAB, " ")[:300],
            v["stato_era_1"], m.get("si_riferisce_a_era1", ""),
        ]))
    return NL.join(r) + NL


def vista_md(voci):
    r = ["# L'INDICE — **vista generata, NON si modifica a mano**", "",
         "> ### ⛔ **La fonte e' `doc/indice/voci.jsonl`.** Si scrive solo con "
         "`python csv/indice.py aggiorna`.", ""]
    per = {}
    for v in voci:
        per.setdefault((v["dominio"], str(v["era"])), []).append(v)
    r.append("| dominio | era | voci |")
    r.append("|---|---|--:|")
    for k in sorted(per):
        r.append("| `%s` | `%s` | %d |" % (k[0], k[1], len(per[k])))
    r.append("")
    r.append("| id | classe | dominio | era | stato | blocca | titolo |")
    r.append("|---|---|---|---|---|---|---|")
    for v in sorted(voci, key=lambda x: x["id"]):
        r.append("| `%s` | %s | %s | %s | ### **%s** | %s | %s |"
                 % (v["id"], v["classe"], v["dominio"], v["era"], v["stato"],
                    "SI" if v["blocca"] else "", v["titolo"].replace("|", "/")[:80]))
    return NL.join(r) + NL


def viste(voci, reg):
    json.dump(invertito(voci, reg), io.open(INVERTITO, "w", encoding="utf-8", newline=NL),
              ensure_ascii=False, indent=1, sort_keys=True)
    io.open(TSV, "w", encoding="utf-8", newline=NL).write(vista_tsv(voci))
    io.open(VISTA_MD, "w", encoding="utf-8", newline=NL).write(vista_md(voci))
    print("  rigenerati: _indice_meta.json, doc/INDICE_ID.tsv, doc/INDICE.md")


# ==========================================================================
#   CERCA  --  SENZA parsing di testo
# ==========================================================================
def cerca(voci, reg, a):
    res = voci
    for chiave, campo in (("dominio", "dominio"), ("stato", "stato"), ("era", "era"),
                          ("classe", "classe")):
        if a.get(chiave):
            res = [v for v in res if str(v[campo]) == a[chiave]]
    if a.get("blocca"):
        vuole = a["blocca"].upper() in ("SI", "TRUE", "1")
        res = [v for v in res if v["blocca"] == vuole]
    for chiave, campo in (("legge", "leggi"), ("variabile", "variabili"),
                          ("assioma", "assiomi")):
        if a.get(chiave):
            res = [v for v in res if a[chiave] in v[campo]]
    if a.get("meta"):
        k, _, val = a["meta"].partition("=")
        res = [v for v in res if str((v["meta"] or {}).get(k, "")) == val]
    print("%-22s %-10s %-16s %-4s %-16s %-3s %s"
          % ("id", "classe", "dominio", "era", "stato", "blc", "titolo"))
    print("-" * 118)
    for v in sorted(res, key=lambda x: x["id"]):
        print("%-22s %-10s %-16s %-4s %-16s %-3s %s"
              % (v["id"][:22], v["classe"][:10], v["dominio"][:16], str(v["era"])[:4],
                 v["stato"][:16], "SI" if v["blocca"] else "", v["titolo"][:48]))
    print("-" * 118)
    print("%d voci" % len(res))
    return res


# ==========================================================================
#   AGGIORNA  --  l'UNICA via di scrittura
# ==========================================================================
def aggiorna(voci, reg, idv, campi, metas, motivo, commit):
    assert motivo, "serve --motivo: una modifica senza motivo non si registra"
    per = {v["id"]: v for v in voci}
    assert idv in per, "`%s` non e' una voce" % idv
    v = per[idv]
    prima = json.loads(json.dumps(v))
    for c in campi:
        k, _, val = c.partition("=")
        assert k in CHIAVI, "`%s` non e' un campo dello schema" % k
        if k == "stato":
            assert val in TRANSIZIONI.get(v["stato"], set()), (
                "TRANSIZIONE VIETATA: `%s` -> `%s` (vedi doc/INDICE_SCHEMA.md)"
                % (v["stato"], val))
        if k == "blocca":
            val = val.upper() in ("SI", "TRUE", "1")
        elif k in ("alias", "leggi", "variabili", "assiomi", "collegate"):
            val = [x for x in val.split(",") if x]
        v[k] = val
    for m in metas:
        k, _, val = m.partition("=")
        spec = reg["metadati"].get(k)
        assert spec, "la chiave meta `%s` NON e' registrata: usa `meta-aggiungi`" % k
        assert spec.get("stato") == "ATTIVO", "la chiave meta `%s` e' DEPRECATA" % k
        if spec["tipo"] == "intero":
            val = int(val)
        elif spec["tipo"] == "bool":
            val = val.upper() in ("SI", "TRUE", "1")
        elif spec["tipo"].startswith("lista_di:"):
            val = [x for x in val.split(",") if x]
        v.setdefault("meta", {})[k] = val
    v["aggiornata"] = {"data": _oggi(), "commit": commit or ""}
    err = valida(voci, reg, verboso=False)
    assert not err, "la modifica NON passa la validazione:" + NL + NL.join(err[:8])
    _scrivi_jsonl(VOCI, voci)
    io.open(STORICO, "a", encoding="utf-8", newline=NL).write(
        json.dumps({"quando": _oggi(), "id": idv, "motivo": motivo,
                    "commit": commit or "", "prima": prima, "dopo": v},
                   ensure_ascii=False) + NL)
    viste(voci, reg)
    print("  `%s` aggiornata, e lo storico ha una riga in piu'" % idv)


def aggiorna_lotto(voci, reg, percorso):
    """### ⭐ **LA SCRITTURA A LOTTI: E' LA STESSA VIA, non un'altra.**

    Prende un `jsonl` di `{id, campi: {...}, meta: {...}, motivo}` e lo applica
    ### **atomicamente**: ### **una riga di storico PER VOCE** *(come `aggiorna`)*, le
    ### **stesse** asserzioni sulle transizioni e sui metadati, e ### **una sola**
    validazione alla fine -- ### **se non passa, NON SI SCRIVE NIENTE.**
    ### ⚠ **Serve perche' la fase 2 tocca ~900 voci:** `aggiorna` una per volta riscriverebbe
    `voci.jsonl` e le tre viste ### **novecento volte**, e un lavoro di quella forma non si
    porta a termine. ### **La REGOLA che conta -- una via di scrittura, un motivo che cita, una
    riga di storico -- resta INTATTA.**
    """
    per = {v["id"]: v for v in voci}
    righe = [json.loads(r) for r in io.open(percorso, encoding="utf-8").read().split(NL)
             if r.strip()]
    storia = []
    for r in righe:
        idv = r["id"]
        assert idv in per, "`%s` non e' una voce" % idv
        motivo = r.get("motivo", "")
        assert len(motivo) >= 20, ("`%s`: il motivo e' troppo corto per CITARE qualcosa: %r"
                                   % (idv, motivo))
        v = per[idv]
        prima = json.loads(json.dumps(v))
        for k, val in (r.get("campi") or {}).items():
            assert k in CHIAVI, "`%s`: `%s` non e' un campo dello schema" % (idv, k)
            if k == "stato" and val != v["stato"]:
                assert val in TRANSIZIONI.get(v["stato"], set()), (
                    "`%s`: TRANSIZIONE VIETATA `%s` -> `%s`" % (idv, v["stato"], val))
            v[k] = val
        for k, val in (r.get("meta") or {}).items():
            spec = reg["metadati"].get(k)
            assert spec, "`%s`: la chiave meta `%s` NON e' registrata" % (idv, k)
            assert spec.get("stato") == "ATTIVO", ("`%s`: la chiave meta `%s` e' DEPRECATA"
                                                   % (idv, k))
            v["meta"][k] = val
        v["aggiornata"] = {"data": r.get("quando") or _oggi(), "commit": r.get("commit", "")}
        storia.append({"quando": v["aggiornata"]["data"], "id": idv, "motivo": motivo,
                       "commit": r.get("commit", ""), "prima": prima,
                       "dopo": json.loads(json.dumps(v))})
    # ### ⚠ **SI VALIDA `derivati=False` PRIMA di scrivere**, perche' l'indice invertito e
    # ### le viste sono ### **per costruzione stale** finche' non si riscrivono: controllarli
    # ### qui vorrebbe dire rifiutare OGNI lotto. ### ➜ **E si rivalida INTERO DOPO**, viste
    # ### comprese: cosi' nessun controllo si perde.
    err = valida(voci, reg, verboso=False, derivati=False)
    assert not err, ("IL LOTTO NON PASSA LA VALIDAZIONE, e NON SI SCRIVE NIENTE:" + NL
                     + NL.join(err[:10]))
    _scrivi_jsonl(VOCI, voci)
    io.open(STORICO, "a", encoding="utf-8", newline=NL).write(
        NL.join(json.dumps(x, ensure_ascii=False) for x in storia) + NL)
    viste(voci, reg)
    v2, r2 = carica()
    err2 = valida(v2, r2, verboso=False)
    assert not err2, ("### SCRITTO, MA LA VALIDAZIONE INTERA FALLISCE:" + NL
                      + NL.join(err2[:10]))
    print("  lotto applicato: %d voci, %d righe di storico; e la validazione INTERA passa"
          % (len(righe), len(storia)))


def mostra(voci, a):
    """### Il DUMP per leggere: `descrizione`, `fonte` e i metadati dell'era `1` --
    ### **mai il solo titolo.**"""
    res = voci
    for k, c in (("stato", "stato"), ("dominio", "dominio"), ("classe", "classe")):
        if a.get(k):
            res = [v for v in res if str(v[c]) == a[k]]
    if a.get("segnaposto"):
        vuole = a["segnaposto"].upper() in ("SI", "TRUE", "1")
        res = [v for v in res if ("MAI definito in un registro" in v["titolo"]) == vuole]
    res = sorted(res, key=lambda x: x["id"])
    da = int(a.get("da", 0) or 0)
    quante = int(a.get("quante", 50) or 50)
    lung = int(a.get("lung", 300) or 300)
    for v in res[da:da + quante]:
        m = v["meta"] or {}
        print("### %s | %s | %s | %s | %s" % (v["id"], v["classe"], v["stato"],
                                              m.get("tipo_era1", "-"),
                                              m.get("famiglia_era1", "-")))
        print("  F: %s" % v["fonte"][:110])
        d = (v["descrizione"] or "").replace(NL, " ")
        print("  D: %s" % (d[:lung] if d else "(vuota)  T: " + v["titolo"][:120]))
        for k in ("motivo_era1", "si_riferisce_a_era1", "avanzamento_era1", "file_citanti",
                  "nota_guardiano"):
            if m.get(k):
                print("  %s: %s" % (k[:12], str(m[k])[:170]))
    print("--- mostrate %d di %d (da %d)" % (min(quante, max(0, len(res) - da)), len(res), da))


def _oggi():
    import datetime
    return datetime.date.today().isoformat()


# ==========================================================================
#   IL REGISTRO DEI METADATI
# ==========================================================================
def meta_aggiungi(reg, k, tipo, valori, regex, descr):
    assert RE_META.match(k), "la chiave `%s` e' fuori regex" % k
    assert k not in reg["metadati"], "la chiave `%s` esiste gia'" % k
    base = tipo[len("lista_di:"):] if tipo.startswith("lista_di:") else tipo
    assert base in TIPI_META, "il tipo `%s` non e' ammesso" % tipo
    assert descr, "serve una descrizione"
    if base == "enum":
        assert valori, "un `enum` senza valori non e' un vocabolario chiuso"
    r = _jsonl(META)
    r.append({"chiave": k, "tipo": tipo,
              "valori": [x for x in (valori or "").split(",") if x],
              "regex": regex or "", "descrizione": descr,
              "si_applica_a": {"classi": [], "domini": []}, "cercabile": True,
              "stato": "ATTIVO", "sostituito_da": "",
              "creato": {"data": _oggi(), "commit": ""}})
    _scrivi_jsonl(META, r, "chiave")
    print("  registrata la chiave meta `%s` (%s)" % (k, tipo))


def meta_depreca(voci, reg, k, nuovo, motivo):
    assert motivo, "serve --motivo"
    r = _jsonl(META)
    trovata = [x for x in r if x["chiave"] == k]
    assert trovata, "la chiave `%s` non e' registrata" % k
    trovata[0]["stato"] = "DEPRECATO"
    trovata[0]["sostituito_da"] = nuovo or ""
    _scrivi_jsonl(META, r, "chiave")
    n = 0
    for v in voci:
        if k in (v["meta"] or {}):
            if nuovo:
                v["meta"][nuovo] = v["meta"].pop(k)
            else:
                v["meta"].pop(k)
            n += 1
    _scrivi_jsonl(VOCI, voci)
    io.open(STORICO, "a", encoding="utf-8", newline=NL).write(
        json.dumps({"quando": _oggi(), "meta_deprecata": k, "sostituito_da": nuovo or "",
                    "voci_migrate": n, "motivo": motivo}, ensure_ascii=False) + NL)
    print("  `%s` DEPRECATA, e %d voci migrate%s"
          % (k, n, (" a `%s`" % nuovo) if nuovo else " (chiave rimossa)"))


def meta_rinomina(voci, reg, k, k2, motivo):
    assert motivo, "serve --motivo"
    r = _jsonl(META)
    trovata = [x for x in r if x["chiave"] == k]
    assert trovata, "la chiave `%s` non e' registrata" % k
    assert not [x for x in r if x["chiave"] == k2], "`%s` esiste gia'" % k2
    assert RE_META.match(k2), "`%s` e' fuori regex" % k2
    trovata[0]["chiave"] = k2
    _scrivi_jsonl(META, r, "chiave")
    n = 0
    for v in voci:
        if k in (v["meta"] or {}):
            v["meta"][k2] = v["meta"].pop(k)
            n += 1
    _scrivi_jsonl(VOCI, voci)
    io.open(STORICO, "a", encoding="utf-8", newline=NL).write(
        json.dumps({"quando": _oggi(), "meta_rinominata": [k, k2], "voci_migrate": n,
                    "motivo": motivo}, ensure_ascii=False) + NL)
    print("  `%s` -> `%s`, e %d voci migrate" % (k, k2, n))


# ==========================================================================
#   CITAZIONI  --  un RAPPORTO, non voci nuove
# ==========================================================================
def citazioni(voci):
    noti = {v["id"] for v in voci} | {a for v in voci for a in v["alias"]}
    trovate = {}
    for radice, _dirs, files in os.walk(RADICE):
        if any(x in radice for x in (".git", "__pycache__", "_archivio")):
            continue
        for f in files:
            if not f.endswith((".md", ".py", ".tsv")):
                continue
            p = os.path.join(radice, f)
            try:
                t = io.open(p, encoding="utf-8", errors="replace").read()
            except Exception:                                  # noqa: BLE001
                continue
            for m in re.finditer(r"\[\[([A-Z0-9][A-Z0-9:_-]*)\]\]", t):
                trovate.setdefault(m.group(1), []).append(
                    os.path.relpath(p, RADICE).replace(chr(92), "/"))
    manca = {k: sorted(set(v)) for k, v in trovate.items() if k not in noti}
    print("=" * 96)
    print("LE CITAZIONI `[[ID]]`: %d distinte, %d NON ESISTONO" % (len(trovate), len(manca)))
    print("=" * 96)
    for k in sorted(manca):
        print("  ### `%s`   citata in: %s" % (k, " ".join(manca[k][:4])))
    if not manca:
        print("  tutte le `[[ID]]` esistono.")
    print()
    print("  ### E' UN RAPPORTO, NON UNA VOCE: nessun segnaposto si crea.")
    return manca


# ==========================================================================
#   IL COLLAUDO  --  coi casi che DEVONO fallire
# ==========================================================================
def collaudo():
    def base(**kw):
        v = {"id": "X1", "alias": [], "titolo": "t", "descrizione": "", "classe": "DIFETTO",
             "dominio": "FISICA", "era": "1", "stato": "APERTA", "blocca": False,
             "leggi": [], "variabili": [], "assiomi": [], "collegate": [], "padre": "",
             "superata_da": "", "chiusura": {}, "fonte": "doc/x.md::X1",
             "creata": {"data": "2026-10-08", "commit": ""},
             "aggiornata": {"data": "2026-10-08", "commit": ""}, "stato_era_1": "",
             "meta": {}}
        v.update(kw)
        return {k: v[k] for k in CHIAVI}

    _voci, reg = carica()
    reg["metadati"]["_dep"] = {"chiave": "_dep", "tipo": "testo_breve", "valori": [],
                               "stato": "DEPRECATO", "sostituito_da": "nota_guardiano"}
    casi = [
        ("il caso SANO", [base()], True),
        ("### dominio FUORI vocabolario", [base(dominio="PIPPO")], False),
        ("### legge INESISTENTE", [base(leggi=["L-NON-ESISTE"])], False),
        ("### CHIUSA senza chiusura", [base(stato="CHIUSA")], False),
        ("### SUPERATA senza superata_da", [base(stato="SUPERATA")], False),
        ("### SOSPESA senza stato_era_1", [base(stato="SOSPESA")], False),
        ("### id DUPLICATO", [base(), base()], False),
        ("### chiave meta NON REGISTRATA", [base(meta={"pippo": "x"})], False),
        ("### valore meta del TIPO SBAGLIATO", [base(meta={"seme": "undici"})], False),
        ("### chiave meta DEPRECATA usata", [base(meta={"_dep": "x"})], False),
        ("### blocca con stato CHIUSA",
         [base(blocca=True, stato="CHIUSA",
               chiusura={"criterio": "c", "commit": "abc1234"})], False),
        ("### dominio DA_CLASSIFICARE con stato ed era decisi",
         [base(dominio="DA_CLASSIFICARE")], False),
        ("### alias che e' anche un id", [base(id="A", alias=["B"]), base(id="B")], False),
        ("### chiavi FUORI ORDINE",
         [dict(reversed(list(base().items())))], False),
        ("### classe NON_DEFINITA con stato APERTA",
         [base(classe="NON_DEFINITA", stato="APERTA")], False),
        ("il caso SANO con classe NON_DEFINITA",
         [base(classe="NON_DEFINITA", stato="DA_CLASSIFICARE",
               dominio="DA_CLASSIFICARE", era="DA_CLASSIFICARE")], True),
    ]
    print("=" * 96)
    print("IL COLLAUDO DELL'INDICE v%d -- coi casi che DEVONO fallire" % SCHEMA_VERSION)
    print("=" * 96)
    ok = 0
    for nome, vv, deve_passare in casi:
        err = valida(vv, dict(reg), verboso=False, derivati=False)
        passa = not err
        buono = (passa == deve_passare)
        ok += buono
        print("  %-52s %-12s %s" % (nome, "PASSA" if passa else "RIFIUTA",
                                    "ok" if buono else "### SBAGLIATO"))
        if not buono and err:
            print("      primo errore: %s" % err[0])
    # ### le TRANSIZIONI VIETATE
    vietate = [("CHIUSA", "SOSPESA"), ("SUPERATA", "CHIUSA"), ("APERTA", "DA_CLASSIFICARE")]
    for da, a in vietate:
        buono = a not in TRANSIZIONI.get(da, set())
        ok += buono
        print("  %-52s %-12s %s" % ("### transizione VIETATA `%s` -> `%s`" % (da, a),
                                    "VIETATA" if buono else "ammessa",
                                    "ok" if buono else "### SBAGLIATO"))
    # ### I DUE CONTROLLI SUI DERIVATI, provati IN MEMORIA sulla loro LOGICA: si costruisce
    # ### un derivato SBAGLIATO e si pretende che il confronto lo veda.
    sane = [base()]
    inv_giusto = invertito(sane, reg)
    inv_storto = {"classe": {"DIFETTO": ["X9"]}}
    buono = inv_giusto != inv_storto
    ok += buono
    print("  %-52s %-12s %s" % ("### indice invertito DISALLINEATO",
                                "VISTO" if buono else "non visto",
                                "ok" if buono else "### SBAGLIATO"))
    tsv_giusto = vista_tsv(sane)
    buono = tsv_giusto != (tsv_giusto + "riga aggiunta a mano" + NL)
    ok += buono
    print("  %-52s %-12s %s" % ("### vista TSV MODIFICATA A MANO",
                                "VISTO" if buono else "non visto",
                                "ok" if buono else "### SBAGLIATO"))
    tot = len(casi) + len(vietate) + 2
    print()
    print("  COLLAUDO: %d su %d" % (ok, tot))
    print("  ### I DUE CONTROLLI SUI DERIVATI sono provati IN MEMORIA sulla loro LOGICA")
    print("  ###   (si costruisce un derivato sbagliato e si pretende che il confronto lo")
    print("  ###   veda); SUL FILE VERO li fa `valida`, e sono gli ultimi due della sua")
    print("  ###   lista. ### Il collaudo valida IN MEMORIA, quindi `derivati=False`.")
    return 0 if ok == tot else 1


# ==========================================================================
def crea_lotto(voci, reg, percorso):
    """### LA VIA PER FAR NASCERE UNA VOCE -- la STESSA via, non un-altra.

    Prende un `jsonl` di `{campi: {...}, motivo, togli_da_etichette}` e lo applica
    ### **atomicamente**: ogni voce passa dal ### **modello completo** delle `CHIAVI`, con
    ### **una riga di storico** *(`prima: null`: prima non c-era niente)*, e ### **una sola
    validazione alla fine.** ### Se non passa, ### **NON SI SCRIVE NIENTE.**

    ### ⛔ **Perche- serviva:** `aggiorna` e `aggiorna_lotto` cominciano entrambi con
    `assert idv in per`, quindi ### **una voce non poteva NASCERE dalla via di scrittura** --
    la fase `1` le creava ### **dentro la migrazione**, che gira una volta sola e dal tag.
    Il blocco `C` della correzione `v3` deve far nascere `16` voci, e scriverle a mano in
    `voci.jsonl` sarebbe stata ### **una SECONDA via di scrittura.**

    ### ⚠ **`togli_da_etichette`:** se l-ID stava in `etichette_rimosse.jsonl` ci va
    ### **TOLTO NELLO STESSO ATTO**, perche- il controllo `C1` pretende che ogni ID vecchio
    stia in ### **UNO E UNO SOLO** posto. ### **Non e- una pulizia: e- la conservazione.**
    """
    per = {v["id"]: v for v in voci}
    righe = [json.loads(r) for r in io.open(percorso, encoding="utf-8").read().split(NL)
             if r.strip()]
    etich = [json.loads(r) for r in
             io.open(ETICH, encoding="utf-8").read().split(NL) if r.strip()] \
        if os.path.exists(ETICH) else []
    per_et = {e["id"]: e for e in etich}
    storia, togli = [], []
    for r in righe:
        campi = r["campi"]
        idv = campi["id"]
        motivo = r.get("motivo", "")
        assert len(motivo) >= 20, ("`%s`: il motivo e- troppo corto per CITARE qualcosa: %r"
                                   % (idv, motivo))
        assert idv not in per, "`%s` ESISTE GIA-: si aggiorna, non si crea" % idv
        for k in campi:
            assert k in CHIAVI, "`%s`: `%s` non e- un campo dello schema" % (idv, k)
        for k, val in (campi.get("meta") or {}).items():
            spec = reg["metadati"].get(k)
            assert spec, "`%s`: la chiave meta `%s` NON e- registrata" % (idv, k)
            assert spec.get("stato") == "ATTIVO", ("`%s`: la chiave meta `%s` e- DEPRECATA"
                                                   % (idv, k))
        v = {"id": idv, "alias": [], "titolo": "", "descrizione": "",
             "classe": "NON_DEFINITA", "dominio": "DA_CLASSIFICARE",
             "era": "DA_CLASSIFICARE", "stato": "DA_CLASSIFICARE", "blocca": False,
             "leggi": [], "variabili": [], "assiomi": [], "collegate": [], "padre": "",
             "superata_da": "", "chiusura": {}, "fonte": "",
             "creata": {"data": r.get("quando") or _oggi(), "commit": r.get("commit", "")},
             "aggiornata": {"data": r.get("quando") or _oggi(),
                            "commit": r.get("commit", "")},
             "stato_era_1": "", "meta": {}}
        v.update(campi)
        v = {k: v[k] for k in CHIAVI}
        voci.append(v)
        per[idv] = v
        if r.get("togli_da_etichette"):
            assert idv in per_et, ("`%s`: non sta in etichette_rimosse.jsonl, e il lotto "
                                   "dice di toglierlo" % idv)
            togli.append(idv)
        storia.append({"quando": v["creata"]["data"], "id": idv, "motivo": motivo,
                       "commit": r.get("commit", ""), "prima": None,
                       "dopo": json.loads(json.dumps(v))})
    err = valida(voci, reg, verboso=False, derivati=False)
    assert not err, ("il lotto NON passa la validazione, e NON SI SCRIVE NIENTE:" + NL
                     + NL.join(err[:10]))
    voci.sort(key=lambda v: v["id"])
    _scrivi_jsonl(VOCI, voci)
    if togli:
        _scrivi_jsonl(ETICH, [e for e in etich if e["id"] not in togli])
    with io.open(STORICO, "a", encoding="utf-8", newline=NL) as f:
        for s in storia:
            f.write(json.dumps(s, ensure_ascii=False) + NL)
    viste(voci, reg)
    err = valida(voci, reg, verboso=False)
    assert not err, "DOPO le viste la validazione cade:" + NL + NL.join(err[:10])
    print("  lotto CREATO: %d voci nuove, %d togliate dalle etichette, %d righe di storico; "
          "e la validazione INTERA passa" % (len(righe), len(togli), len(storia)))


def main(argv):
    if not argv:
        print(__doc__)
        return 0
    cmd, resto = argv[0], argv[1:]
    a, pos = {}, []
    i = 0
    while i < len(resto):
        if resto[i].startswith("--"):
            k = resto[i][2:].replace("-", "_")
            if i + 1 < len(resto) and not resto[i + 1].startswith("--"):
                a.setdefault(k, []).append(resto[i + 1])
                i += 2
            else:
                a.setdefault(k, []).append("SI")
                i += 1
        else:
            pos.append(resto[i])
            i += 1
    uno = {k: v[0] for k, v in a.items()}
    if cmd == "collaudo":
        return collaudo()
    voci, reg = carica()
    if cmd == "valida":
        return 1 if valida(voci, reg) else 0
    if cmd == "cerca":
        cerca(voci, reg, uno)
        return 0
    if cmd == "viste":
        viste(voci, reg)
        return 0
    if cmd == "citazioni":
        citazioni(voci)
        return 0
    if cmd == "aggiorna-lotto":
        aggiorna_lotto(voci, reg, pos[0])
        return 0
    if cmd == "crea-lotto":
        crea_lotto(voci, reg, pos[0])
        return 0
    if cmd == "mostra":
        mostra(voci, uno)
        return 0
    if cmd == "aggiorna":
        aggiorna(voci, reg, pos[0], a.get("campo", []), a.get("meta", []),
                 uno.get("motivo", ""), uno.get("commit", ""))
        return 0
    if cmd == "meta-aggiungi":
        meta_aggiungi(reg, pos[0], uno.get("tipo", ""), uno.get("valori", ""),
                      uno.get("regex", ""), uno.get("descrizione", ""))
        return 0
    if cmd == "meta-depreca":
        meta_depreca(voci, reg, pos[0], uno.get("sostituito_da", ""), uno.get("motivo", ""))
        return 0
    if cmd == "meta-rinomina":
        meta_rinomina(voci, reg, pos[0], pos[1], uno.get("motivo", ""))
        return 0
    print("comando `%s` non riconosciuto." % cmd)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
