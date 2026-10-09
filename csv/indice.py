# -*- coding: utf-8 -*-
"""L'INDICE `v2` — **l'UNICA via di lettura e di scrittura**.

```
python csv/indice.py valida
python csv/indice.py cerca [--dominio X] [--stato X] [--era X] [--blocca SI|NO]
                           [--legge ID] [--variabile ID] [--assioma ID] [--meta k=v]
python csv/indice.py aggiorna ID --campo nome=valore | --meta k=v --motivo "..." [--commit SHA]
python csv/indice.py aggiorna-lotto LOTTO.jsonl     # la STESSA via, in blocco
python csv/indice.py crea-lotto LOTTO.jsonl        # la STESSA via, per FAR NASCERE una voce
python csv/indice.py storico-commit               # riempie il campo `commit` DAI LOG
python csv/indice.py segnali                      # i PRESIDI: segnalano, NON decidono
python csv/indice.py etichette-lotto LOTTO.jsonl   # la via per le ETICHETTE rimosse
python csv/indice.py da-decidere                  # CIO- SU CUI L-INDICE ASPETTA LUCA
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
import subprocess
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

# =====================================================================================
#   LA DICHIARAZIONE DEGLI ID -- punto `12(a)`, e i nomi sono quelli NUOVI del `12(b)`
# -------------------------------------------------------------------------------------
#   ### ⛔ **DODICI PRESIDI IN UN FILE: quindi `PRESIDI` e non `PRESIDIO`.**
#   ### `P-C1` legge questa tabella ### **via AST** e verifica che ### **ogni ID sia
#   ### nell-indice** e che ### **la funzione esista nel modulo.**
#   ### ⭐ **E i nomi sono CAMBIATI il 2026-10-09:** si chiamavano `F1`…`F12`,
#   ### e quei nomi ### **COLLIDEVANO con ID veri** *(`F1`-`F3` segnaposto, `F4`-`F5`
#   ### difetti)*. ### **Il nome vecchio vive come alias NAMESPACED**
#   ### *(`VALIDATORE:F1`)*: nudo collidirebbe, ed e- la ragione del rinominamento.
# =====================================================================================
PRESIDI = {
    "PI-GEMELLE": "_f1_gemelle",
    "PI-SIMBOLI-ERA1": "_f2_era2",
    "PI-PAROLE-STRUMENTO": "_f3_fisica_strumenti",
    "PI-ETICHETTA-DEFINITA": "_f4_etichette",
    "PI-STORICO-SENZA-COMMIT": "_f5_storico",
    "PI-NOTA-CONTRADDICE-LISTA": "_f6_note",
    "PI-FISICA-ERA1-NON-SOSPESA": "_f7_stato",
    "PI-OGGETTI-ERA1": "_f8_era1",
    "PI-ERA-STATO": "_f9_era_stato",
    "PI-CRITERIO-METODO": "_f10_criterio_metodo",
    "PI-REPLAY": "_f11_replay",
    "PI-CHIUSURA-ORFANA": "_f12_chiusura_orfana",
}

# ### ⛔ **LA FORMA DI UN-ECCEZIONE SI COSTRUISCE DALLA TABELLA `PRESIDI`.**
# ### Scrivere l-elenco a mano qui sarebbe ### **un secondo posto** dove i nomi
# ### dei presidi possono divergere -- e ### **divergerebbero**, perche- i nomi
# ### sono appena cambiati.
_FORMA_ECC = r"^(" + "|".join(re.escape(k) for k in PRESIDI) + r"):\s*(.+)$"

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
            # ### ⭐ **E DAL 2026-10-09 ACCETTA ANCHE L-ID DI UNA VOCE**, e il mandato lo
            # ### dice: ### **una voce promossa o fusa in un-altra e- superata DA QUELLA.**
            # ### ⛔ **La mia regola di ieri -- *<<un difetto non decide niente>>* -- era
            # ### vera per una DECISIONE e falsa per una PROMOZIONE:** `S02` e-
            # ### ### **PROMOSSO** a `D31`, e `D31` e- una voce. ### **Rifiutarla
            # ### significava pretendere che ogni superamento venisse da FUORI l-indice**,
            # ### e un indice che non sa dire *<<questa e- diventata quella>>*
            # ### ### **perde la storia delle fusioni.**
            elif (s not in reg["decisioni"] and s not in reg["assiomi"]
                  and s not in {w["id"] for w in voci}):
                err.append("`%s`: superata_da `%s` non e' una decisione, ne' un assioma, "
                           "ne' una voce"
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
    # ### ⛔ **QUESTI DUE VANNO PRIMA DEL RITORNO, e non e- un dettaglio:** dipendono
    # ### ### **SOLO dalle voci**, e `aggiorna_lotto` valida con `derivati=False`
    # ### ### **PRIMA DI SCRIVERE**. Finche- stavano dopo, un lotto che violava `PI-FISICA-ERA1-NON-SOSPESA`
    # ### ### **VENIVA SCRITTO** e solo allora l-assert scattava: l-indice restava
    # ### ### **CORROTTO**, e l-ho ripristinato con `git checkout`. L-ha dimostrato una
    # ### prova end-to-end, e la promessa *<<se non passa NON SI SCRIVE NIENTE>>*
    # ### ### **era falsa.**
    err += _f7_stato(voci)
    # ### `PI-CRITERIO-METODO` SI ACCENDE, `PI-ERA-STATO` NO, e la differenza e- ### **misurata, non di gusto:**
    # ### `PI-CRITERIO-METODO` viola su ### **ZERO** voci, `PI-ERA-STATO` su ### **CINQUE**. `indice.py valida`
    # ### gira nel `pre-commit`: un presidio bloccante con violazioni in piedi
    # ### ### **blocca ogni commit del repo**, compreso quello che lo accende.
    # ### ✔ **E ADESSO `PI-ERA-STATO` E- ACCESO, NELLO STESSO COMMIT CHE CURA LE CINQUE** -- `A2`,
    # ### `LUNGA-BATTITO-CADUTA`, `PRESTAZIONI-CORSE`, `REPERTI-IMMUTABILI`,
    # ### `RIPRESA-ARGV`: quattro passano ad `APERTA`, una a era `1`.
    # ### ⛔ **In DUE commit non si poteva**, e Luca lo ha riconosciuto: *<<F9 e F10 si
    # ### accendono NELLO STESSO COMMIT delle correzioni che li rendono veri, mai
    # ### prima>>*. Il commit che accendesse `PI-ERA-STATO` prima ### **sarebbe bloccato dal suo
    # ### stesso hook**, perche- `indice.py valida` gira nel `pre-commit`.
    err += _f9_era_stato(voci)
    err += _f10_criterio_metodo(voci)
    # ### `PI-CHIUSURA-ORFANA` SI ACCENDE QUI, ### **nello stesso commit che cura le `41`** -- e- la
    # ### ### **quarta volta** che l-ordine non e- libero, e stavolta stava scritto nel
    # ### task history ### **prima di muovermi.**
    err += _f12_chiusura_orfana(voci)
    err += _eccezioni_malformate(voci)
    # ### L'INDICE INVERTITO e le VISTE: DERIVATI, e si CONFRONTANO
    if not derivati:
        return err
    # ### `PI-STORICO-SENZA-COMMIT` e la FORMA delle ECCEZIONI sono ERRORI, non segnali, e stanno QUI: il
    # ### mandato dice *<<storico senza commit -> ERRORE, non segnale>>*, e
    # ### un-eccezione che NON CITA non e- un-eccezione, e- una via di fuga.
    err += _f5_storico(voci)
    # ### `PI-REPLAY` STA QUI, accanto a `PI-STORICO-SENZA-COMMIT`, perche- ### **legge il disco** *(lo storico e il
    # ### tag)* e non solo la lista: ### **non e- puro**, e il `derivati=False` di
    # ### `aggiorna_lotto` lo salta ### **di proposito** -- durante un lotto lo storico
    # ### nuovo ### **non e- ancora scritto**, e `PI-REPLAY` accuserebbe ogni voce del lotto.
    # ### ✔ **Dopo la scrittura `valida` gira INTERO, e li- `PI-REPLAY` controlla.**
    err += _f11_replay(voci)
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
        # ### I SEGNALI NON CAMBIANO IL CODICE D-USCITA, e per questo si stampano
        # ### DOPO il verdetto e FUORI da `err`: un segnale che blocca NON E- UN
        # ### SEGNALE. La lista intera la da- `python csv/indice.py segnali`.
        _s = segnali(voci, reg, verboso=False)
        _n = sum(len(x[2]) for x in _s)
        print("  ### i PRESIDI contro le mescolanze: %d segnali (%s). NON bloccano: "
              "`indice.py segnali`"
              % (_n, "  ".join("%s=%d" % (x[0], len(x[2])) for x in _s)))
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
                    "commit": commit or "", "commit_base": _head(),
                    "prima": prima, "dopo": v},
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
        # ### TOGLIERE UN METADATO E- UNA COSA DIVERSA DA SVUOTARLO, e serve:
        # ### `nota_guardiano` ha regex `^.{1,300}$`, quindi ### **non si puo- mettere a
        # ### stringa vuota.** E una ### **domanda a cui si e- risposto non si riscrive: si
        # ### TOGLIE** -- la risposta vive in `superata_da` e nello storico.
        for k in (r.get("meta_togli") or []):
            assert k in v["meta"], ("`%s`: la chiave meta `%s` NON ESISTE, e togliere "
                                    "cio- che non esiste NASCONDE un errore" % (idv, k))
            del v["meta"][k]
        v["aggiornata"] = {"data": r.get("quando") or _oggi(), "commit": r.get("commit", "")}
        storia.append({"quando": v["aggiornata"]["data"], "id": idv, "motivo": motivo,
                       "commit": r.get("commit", ""), "commit_base": _head(),
                       "prima": prima, "dopo": json.loads(json.dumps(v))})
    # ### ⚠ **SI VALIDA `derivati=False` PRIMA di scrivere**, perche' l'indice invertito e
    # ### le viste sono ### **per costruzione stale** finche' non si riscrivono: controllarli
    # ### qui vorrebbe dire rifiutare OGNI lotto. ### ➜ **E si rivalida INTERO DOPO**, viste
    # ### comprese: cosi' nessun controllo si perde.
    # ### ⛔ **`PI-STORICO-SENZA-COMMIT` NON dipende dalle voci** -- guarda `storico.jsonl` sul disco contro
    # ### `HEAD` -- quindi ### **si chiede PRIMA di scrivere**, non alla fine: alla fine
    # ### sarebbe ### **un allarme su un file GIA- SCRITTO.**
    err = _f5_storico(voci) + valida(voci, reg, verboso=False, derivati=False)
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
        # ### ⚠ **La voce-modello era `FISICA`/era `1`/`APERTA`, che da oggi `PI-FISICA-ERA1-NON-SOSPESA` VIETA:**
        # ### il caso SANO sarebbe diventato un fallimento. ### **Era `ENTRAMBE`**, e il
        # ### caso di `PI-FISICA-ERA1-NON-SOSPESA` ce l-ha suo.
             "dominio": "FISICA", "era": "ENTRAMBE", "stato": "APERTA", "blocca": False,
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
        # ### ⭐ **I DUE VERSI DEL PUNTO `3`** *(2026-10-09)*: `superata_da` accetta
        # ### ### **anche l-ID di una VOCE** -- una voce ### **promossa o fusa** in
        # ### un-altra e- superata ### **da quella** -- e ### **rifiuta cio- che non e-
        # ### ne- decisione, ne- assioma, ne- voce.** ### ⛔ **Senza il verso negativo
        # ### la regola nuova non e- una regola: e- un PERMESSO.**
        ("una VOCE come `superata_da` (il verso POSITIVO del punto 3)",
         [base(stato="SUPERATA", superata_da="B", stato_era_1=""),
          base(id="B")], True),
        ("### `superata_da` che NON e- ne- decisione, ne- assioma, ne- voce",
         [base(stato="SUPERATA", superata_da="NON-ESISTE-NIENTE")], False),
        # ### ⭐ **E `PI-ERA-STATO` AMMETTE `SUPERATA` PER `ENTRAMBE`**, che corregge una mia
        # ### strettezza; ma ### **`SOSPESA` resta VIETATA**, e il caso accanto lo prova.
        ("era `ENTRAMBE` con `SUPERATA` (il verso POSITIVO di `PI-ERA-STATO`)",
         [base(stato="SUPERATA", superata_da="B"), base(id="B")], True),
        ("### `PI-ERA-STATO`: era `ENTRAMBE` con stato `SOSPESA`, che resta VIETATO",
         [base(stato="SOSPESA", stato_era_1="aperto")], False),
        ("### SOSPESA senza stato_era_1", [base(stato="SOSPESA")], False),
        ("### `PI-FISICA-ERA1-NON-SOSPESA`: FISICA/era 1 con stato APERTA",
         [base(era="1", stato="APERTA")], False),
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
# ==========================================================================
#   I PRESIDI CONTRO LE MESCOLANZE  --  SEGNALANO, non decidono
# ==========================================================================
# ### ⛔ **LA REGOLA CHE LI GOVERNA:** sono ### **deterministici** e ### **SEGNALANO**; la
# ### decisione e- di chi legge. ### **Un segnale si chiude in due modi soli:**
# ### ### **correggendo la voce**, oppure con ### **`meta.eccezione_presidio`**, che deve
# ### ### **CITARE IL TESTO ALLA LETTERA.**
# ### ⚠ **`PI-STORICO-SENZA-COMMIT` e- L-UNICO che e- un ERRORE**, e il mandato lo dice: *«storico senza commit ->
# ### errore, non segnale»*.
# ### ⛔ **E `PI-GEMELLE` non puo- leggere l-intenzione:** *«come lo stesso fatto»* non e- rilevabile
# ### da un programma. `PI-GEMELLE` segnala ### **che l-ID c-e-**; che sia *lo stesso fatto* lo decide
# ### chi legge. ### **E- esattamente il motivo per cui questi presidi SEGNALANO.**

# ### I simboli dell-ERA 1: se una voce dell-era `2` li nomina, sta ancora parlando del
# ### vecchio codice. (`PI-SIMBOLI-ERA1`)
ERA1_SIMBOLI = ("phivel", "phidot", "M_PH", "perc_chi", "perc_geom", "mem_mot",
                "dir_laterale", "Nose-Hoover", "scuotimento", "sync", "SCALAMIN")
# ### Le parole degli STRUMENTI: se le dice il titolo di una voce `FISICA`, quella voce parla
# ### del modo di verificare, non della natura. (`PI-PAROLE-STRUMENTO`)
STRUMENTI = ("sigillo", "criterio", "controllo positivo", "caso che deve fallire",
             "commento", "docstring", "README", "hook", "presidio", "CRLF")
# ### GENERATE: una riga qui ELENCA un ID, non lo DEFINISCE. (`PI-ETICHETTA-DEFINITA`)
# ### ⛔ **E- lo stesso FALSO-UNO del controllo `C4`, che leggeva `doc/INDICE.md`.**
VISTE_GENERATE = ("doc/LISTA_CHIUSA.md", "doc/INDICE.md", "doc/INDICE_ID.tsv",
                  "doc/INDICE_ID_dettaglio.md", "doc/indice/")
# ### Che cosa diceva ciascuna lista del guardiano. (`PI-NOTA-CONTRADDICE-LISTA`)
LISTE_GUARDIANO = {"1": (None, "ENTRAMBE", None),
                   "2": ("FISICA", "2", "AGENDA"),
                   "3": ("FISICA", "1", "SOSPESA")}
# ### ⛔ **`_DOMINI_PAROLA` e `_STATI_PAROLA` SONO STATE TOLTE**, non lasciate morte:
# ### servivano a `PI-NOTA-CONTRADDICE-LISTA` per ### **leggere la prosa della nota**, ed e- proprio cio- che
# ### ### **sbagliava** *(«candidata SUPERATA dalla decisione» letto come lo stato
# ### `SUPERATA`)*. ### **Un vocabolario che non si usa piu- si cancella**, altrimenti
# ### il prossimo lo riusa.
_TOKEN = re.compile(r"[A-Za-z][A-Za-z0-9_:.-]*")
# ### Lo schema `D`/`Z`: una riga della tavola `D` che cita la sua `Z`. (`PI-GEMELLE`)
_DZ = re.compile(r"^D\d+[a-z]?$")
_ZZ = re.compile(r"^Z\d+[a-z]?$")
_RIGA_NNNN = re.compile(r":\d{3,5}(?![0-9])")
_FLAG = re.compile(r"(?<![A-Za-z0-9])--[a-z][a-z0-9-]{2,}")


def _coperto(v, quale):
    """### `meta.eccezione_presidio`: la voce dichiara che quel segnale ### **e- stato
    guardato e va bene cosi-.** ### ⚠ **La FORMA la controlla `valida`** *(vedi
    `_eccezioni_malformate`)*: senza quel controllo l-eccezione sarebbe ### **una via di
    fuga a costo zero.**"""
    for e in (v.get("meta") or {}).get("eccezione_presidio", []) or []:
        if str(e).strip().upper().startswith(quale + ":"):
            return True
    return False


def _testo_voce(v):
    return " ".join([v.get("titolo") or "", v.get("descrizione") or "",
                     v.get("fonte") or "", (v.get("meta") or {}).get("nota_guardiano") or ""])


def _eccezioni_malformate(voci):
    """### ⛔ **UN-ECCEZIONE CHE NON CITA NON E- UN-ECCEZIONE: e- una via di fuga.**

    La forma obbligata e- ### **`F<n>: <motivo>`**, e il motivo deve contenere
    ### **un pezzo LETTERALE di almeno `20` caratteri** del testo della voce
    *(titolo, descrizione, fonte o nota)*. ### **Cosi- l-eccezione e- VERIFICABILE**, e non
    si puo- zittire un presidio con una frase generica.
    """
    err = []
    for v in voci:
        for e in (v.get("meta") or {}).get("eccezione_presidio", []) or []:
            s = str(e)
            # ### ⛔ **LA FORMA SEGUE IL RINOMINAMENTO** *(punto `12(b)`)*: il prefisso
            # ### e- ### **l-ID del presidio**, e `_PRESIDI_NOMI` lo prende
            # ### ### **dalla tabella `PRESIDI`** -- cosi- ### **non c-e- un
            # ### secondo posto** dove l-elenco possa divergere.
            m = re.match(_FORMA_ECC, s.strip())
            if not m:
                err.append("`%s`: `eccezione_presidio` fuori forma: serve `F<n>: <motivo>`, "
                           "trovato %r" % (v["id"], s[:60]))
                continue
            testo = " ".join(_testo_voce(v).split())
            motivo = " ".join(m.group(2).split())
            if not any(testo[k:k + 20] and testo[k:k + 20] in motivo
                       for k in range(max(1, len(testo) - 19))):
                err.append("`%s`: l-eccezione `%s` NON CITA IL TESTO ALLA LETTERA (serve un "
                           "pezzo di almeno 20 caratteri del titolo, della descrizione, "
                           "della fonte o della nota)" % (v["id"], m.group(1)))
    return err


def _f5_righe(vive, n_head):
    """### LA LOGICA DI `PI-STORICO-SENZA-COMMIT`, PURA: nessun disco, nessun git.

    ### ⛔ **Esiste per una ragione precisa:** il collaudo deve poterla provare
    ### **senza toccare l-indice vero**, e il mandato lo dice. ### **Un collaudo che per
    provare un presidio deve scrivere nell-indice e- lo stesso difetto che nel giro scorso
    ha cancellato `867` classificazioni** *(`C4` che rilanciava la migrazione)*.
    """
    err = []
    for k in range(min(n_head, len(vive))):
        riga = vive[k] if isinstance(vive[k], dict) else json.loads(vive[k])
        if not riga.get("commit"):
            err.append("`PI-STORICO-SENZA-COMMIT` storico riga %d: GIA- COMMITTATA e senza `commit`. Gira "
                       "`python csv/indice.py storico-commit`" % (k + 1))
    return err[:20]


# ### ⛔ **IL TAG DELLA FINE DELLA MIGRAZIONE.** Le voci ### **senza storico** non sono un
# ### buco: sono ### **quelle che nessuno ha ancora toccato**, e il loro stato giusto e-
# ### ### **quello con cui sono nate.** `3ef2326` e- il commit in cui la migrazione ha
# ### finito di scriverle.
FINE_MIGRAZIONE = "3ef2326"
# ### I campi che `PI-REPLAY` confronta: ### **tutti quelli dello schema tranne `aggiornata`**, che
# ### e- ### **un timbro di QUANDO**, non un dato della voce -- e lo riscrive ogni lotto,
# ### anche quando non cambia niente.
CHIAVI_F11 = tuple(k for k in CHIAVI if k != "aggiornata")


def _f11_righe(voci, ultimo, nati):
    """### `PI-REPLAY`, ### **la parte PURA:** ogni voce coincide col `dopo` della sua ULTIMA riga
    di storico; ### **le voci senza storico** coincidono con il loro stato alla fine della
    migrazione; ### **una voce nata dopo e senza storico e- un ERRORE.**

    ### ⭐ **E- IL PRESIDIO PIU- FORTE DI TUTTI, e il perche- e- questo:** gli altri guardano
    ### **se un campo e- plausibile**; `PI-REPLAY` guarda ### **se il campo e- ARRIVATO DA UNA
    SCRITTURA DICHIARATA.** ### ⛔ **Una modifica a mano a `voci.jsonl` -- anche con le viste
    rigenerate, anche se passa TUTTI gli altri controlli -- qui NON PASSA**, perche-
    ### **non ha una riga di storico che la spieghi.**

    ### ⚠ **E- l-unico presidio che rende VERA la frase <<si scrive SOLO con `indice.py
    aggiorna`>>** *(par.9)*: prima era ### **una regola scritta**, e `A9` dice che una regola
    scritta ### **non impedisce niente.**

    ### ⛔ **`aggiornata` NON si confronta:** e- un timbro di ### **quando**, non un dato
    della voce.
    """
    err = []
    for v in voci:
        u = ultimo.get(v["id"])
        if u is None:
            m = nati.get(v["id"])
            if m is None:
                err.append("`PI-REPLAY` `%s`: NATA DOPO la migrazione e SENZA STORICO. Una voce "
                           "nuova si crea con `crea-lotto`, che scrive la sua riga: se la "
                           "riga non c-e-, la voce e- stata scritta A MANO" % v["id"])
                continue
            d = [k for k in CHIAVI_F11
                 if json.dumps(v[k], sort_keys=True)
                 != json.dumps(m.get(k), sort_keys=True)]
            if d:
                err.append("`PI-REPLAY` `%s`: NON ha storico, quindi deve coincidere col suo "
                           "stato a %s (fine della migrazione), e invece differisce in %s"
                           % (v["id"], FINE_MIGRAZIONE, d[:5]))
            continue
        d = [k for k in CHIAVI_F11
             if json.dumps(v[k], sort_keys=True)
             != json.dumps((u.get("dopo") or {}).get(k), sort_keys=True)]
        if d:
            err.append("`PI-REPLAY` `%s`: NON coincide col `dopo` della sua ULTIMA riga di storico "
                       "(%s), e differisce in %s. Il campo non e- arrivato da una scrittura "
                       "dichiarata: qualcuno ha scritto A MANO"
                       % (v["id"], u.get("quando", ""), d[:5]))
    return err


def _f11_nati():
    """### Le voci ### **alla fine della migrazione**, o `{}` se il tag non si legge."""
    q = subprocess.run(["git", "show", "%s:doc/indice/voci.jsonl" % FINE_MIGRAZIONE],
                       cwd=RADICE, capture_output=True, text=True, encoding="utf-8")
    if q.returncode != 0:
        return {}
    fuori = {}
    for r in q.stdout.split(NL):
        if r.strip():
            w = json.loads(r)
            fuori[w["id"]] = w
    return fuori


def _f11_ultimo(percorso=None):
    """### Per ogni id, ### **l-ULTIMA riga di storico.**"""
    p = percorso or STORICO
    fuori = {}
    if not os.path.exists(p):
        return fuori
    for r in io.open(p, encoding="utf-8").read().split(NL):
        if r.strip():
            s = json.loads(r)
            fuori[s["id"]] = s
    return fuori


def _f11_replay(voci):
    """### `PI-REPLAY` sul disco: legge `storico.jsonl` e ### **le voci al tag.**

    ### ⚠ **Se il tag non si legge il presidio TACE, e lo dichiaro:** senza il
    ### **punto di partenza** non si puo- dire se una voce senza storico sia giusta --
    ### **meglio tacere che accusare.**
    """
    if not os.path.exists(STORICO):
        return []
    nati = _f11_nati()
    if not nati:
        return []
    return _f11_righe(voci, _f11_ultimo(), nati)


def _f5_storico(voci):
    """### `PI-STORICO-SENZA-COMMIT`: una riga di storico ### **GIA- COMMITTATA** senza il suo `commit`.

    ### ⛔ **E- UN ERRORE, non un segnale**, e il mandato lo dice.
    ### ⚠ **MA SOLO PER LE RIGHE GIA- COMMITTATE, e questa e- una MIA DERIVAZIONE:** nella
    forma letterale *(«ogni riga senza commit e- un errore»)* il presidio
    ### **bloccherebbe OGNI COMMIT DI UN LOTTO**, perche- `aggiorna-lotto` scrive righe con
    `commit` vuoto -- ### **il commit che le conterra- non esiste ancora** *(e- il ritardo
    dichiarato nel blocco `D`)*. ### ✔ **Le righe presenti in `HEAD` devono avere il loro
    commit; quelle aggiunte DOPO `HEAD` sono esattamente il ritardo, e sono esenti.**
    ### **Cosi- `PI-STORICO-SENZA-COMMIT` obbliga a girare `storico-commit` prima del commit successivo**, invece
    di impedire il commit.
    """
    del voci
    if not os.path.exists(STORICO):
        return []
    vive = [r for r in io.open(STORICO, encoding="utf-8").read().split(NL) if r.strip()]
    q = subprocess.run(["git", "show", "HEAD:doc/indice/storico.jsonl"], cwd=RADICE,
                       capture_output=True, text=True, encoding="utf-8")
    if q.returncode != 0:
        return []
    return _f5_righe(vive, len([r for r in q.stdout.split(NL) if r.strip()]))


DA_DECIDERE = os.path.join(D, "DA_DECIDERE_LUCA.md")
_DD_NOTA = re.compile(r"da\s+(decidere|confermare)\s+da\s+Luca[\s:,-]*(.*)$", re.I)


def da_decidere(voci, reg):
    """### UN ELENCO SOLO: tutto cio- su cui l-indice ASPETTA LUCA.

    ### ⛔ **Nel codice NON c-e- nessuna lista di ID: ci sono i TRE CRITERI**, e l-elenco
    e- cio- che trovano. ### **Il mandato dice «generato e non scritto a mano»**, e la
    ragione e- precisa: ### **un elenco mezzo generato SEMBRA COMPLETO.**

      * ① la `nota_guardiano` dice *«da decidere / confermare da Luca»* -> la domanda e-
        ### **cio- che la nota stessa chiede**;
      * ② la voce ha `meta.omonimo` -> ### **quale dei `N` significati?**;
      * ③ `stato = DA_CLASSIFICARE` e la classe ### **NON e- `NON_DEFINITA`** -> che
        classe, dominio, era e stato?

    ### ⚠ **I segnaposto NON ci vanno**, e il mandato lo dice: sono tanti, e sono
    ### **il lavoro che resta**, non una domanda aperta.
    """
    del reg
    righe = {}

    def dom(idv, q):
        righe.setdefault(idv, []).append(q)

    for v in voci:
        nota = (v.get("meta") or {}).get("nota_guardiano") or ""
        m = _DD_NOTA.search(nota)
        if m:
            coda = " ".join(m.group(2).split())[:200]
            if m.group(1).lower().startswith("conf"):
                dom(v["id"], "CONFERMI `%s`/era `%s`? %s"
                    % (v["dominio"], v["era"], coda))
            else:
                dom(v["id"], coda or "la nota chiede una decisione e non dice quale")
        om = (v.get("meta") or {}).get("omonimo") or []
        if om:
            # ### ⚠ **L-ULTIMA VOCE DI `omonimo` PUO- ESSERE UN TRONCAMENTO**
            # ### *(<<... e altre N definizioni>>)*: contarla come un significato
            # ### ### **direbbe un numero piu- piccolo del vero.** `D3` ha `8`
            # ### definizioni e `7` voci nel meta: la domanda deve dire ### **ALMENO.**
            tronco = bool(om) and str(om[-1]).strip().startswith("...")
            dom(v["id"], "OMONIMO: quale %s significati dichiarati in `meta.omonimo`? "
                         "NON si scegli da se-"
                         % (("di ALMENO %d" % (len(om) - 1)) if tronco
                            else ("dei %d" % len(om))))
        if v["stato"] == "DA_CLASSIFICARE" and v["classe"] != "NON_DEFINITA":
            d = (v.get("meta") or {}).get("motivo_dubbio") or ""
            dom(v["id"], "CHE CLASSE, DOMINIO, ERA E STATO? %s"
                % (" ".join(d.split())[:200] if d else "il dubbio non e- dichiarato"))
    per = {v["id"]: v for v in voci}
    nd = sum(1 for v in voci if v["classe"] == "NON_DEFINITA")
    R = [
         "# CIO' SU CUI L-INDICE ASPETTA LUCA — **un elenco solo, GENERATO**",
         "",
         "> ### ⛔ **Questo file e' GENERATO da `python csv/indice.py da-decidere`: NON si scrive a mano.** Nel codice ### **non c'e' nessuna lista di ID**: ci sono ### **tre criteri** — la nota che dice *<<da decidere/confermare da Luca>>*, il metadato `omonimo`, e lo stato `DA_CLASSIFICARE` su una voce che ### **non e' un segnaposto.**",
         "",
         "| | |",
         "|---|--:|",
    ]
    R.append("| **voci che aspettano una decisione** | ### **`%d`** |" % len(righe))
    R.append("| **domande in tutto** | `%d` |" % sum(len(x) for x in righe.values()))
    R.append("| **segnaposto `NON_DEFINITA`**, che NON sono una domanda | `%d` |" % nd)
    R += ["", "---", ""]
    gruppi = [("gli OMONIMI -- due nomi e una cosa, e NON si scegli",
               lambda i: bool((per[i].get("meta") or {}).get("omonimo"))),
              ("le CLASSIFICAZIONI da confermare",
               lambda i: any(q.startswith("CONFERMI") for q in righe[i])),
              ("le DOMANDE aperte", lambda i: True)]
    visti = set()
    for titolo, quali in gruppi:
        dentro = [i for i in sorted(righe) if i not in visti and quali(i)]
        if not dentro:
            continue
        visti |= set(dentro)
        R += ["## %s -- `%d`" % (titolo, len(dentro)), "",
              "| id | `classe`/`dominio`/era/stato | LA DOMANDA | LA FRASE |",
              "|---|---|---|---|"]
        for i in dentro:
            v = per[i]
            frase = " ".join(((v.get("titolo") or "") + " "
                              + (v.get("descrizione") or "")).split())[:150]
            R.append("| `%s` | `%s`/`%s`/`%s`/`%s` | %s | %s |"
                     % (i, v["classe"], v["dominio"], v["era"], v["stato"],
                        "<br>".join(q.replace("|", "/") for q in righe[i]),
                        frase.replace("|", "/")))
        R += ["", "---", ""]
    R.append("> ### \u2b50 **Una decisione non presa e- un dato; una decisione presa al "
             "posto di Luca e- un difetto.** Questo file e- il primo: ### **tutto cio- che "
             "l-indice NON sa, in un posto solo.**")
    R.append("")
    io.open(DA_DECIDERE, "w", encoding="utf-8", newline=NL).write(NL.join(R) + NL)
    print("  scritto doc/indice/DA_DECIDERE_LUCA.md: %d voci, %d domande, %d righe"
          % (len(righe), sum(len(x) for x in righe.values()), len(R)))
    return righe


# ### ⭐ **GLI OGGETTI CONCRETI DELL-ERA `1`** *(`PI-OGGETTI-ERA1`, dal 2026-10-09)*. Il guardiano:
# ### *<<vale per ### **ENTRAMBE** una REGOLA DI LAVORO o uno strumento che sopravvive;
# ### e- ### **era 1** cio- che riguarda un OGGETTO CONCRETO dell-era 1>>*.
# ### ⛔ **E un oggetto concreto si riconosce da COME SI SCRIVE, non dalla parola:** un flag
# ### da ### **`--`**, non dalla parola *<<flag>>*; il blob dal ### **suo sha1**, non dalla
# ### parola *<<blob>>*. ### **Per questo `P6` -- <<ogni csv di misura porta BLOB, SEME e
# ### TUTTI I FLAG>> -- NON scatta: e- una REGOLA, e non nomina nessun flag.**
ERA1_OGGETTI = (
    # ### il SIGILLO DI UNA CURA, in tutte le forme in cui lo scriviamo
    (r"sigill\w*\s+(?:di|del|della|dell)\s*(?:la\s+)?cura", "il sigillo di una cura"),
    (r"scena\s*\(ii\)", "la scena (ii)"),
    (r"\bpilot[ao]\b", "il pilota"),
    (r"\.pkl\b", "un `.pkl`"),
    (r"b8c21049", "il blob b8c21049"),
    # ### ⚠ **un FLAG si riconosce dai due trattini ATTACCATI a una lettera:** cosi- il
    # ### ### **`--` usato come lineetta** *(<<-- e poi>>)* non conta.
    (r"(?<![A-Za-z0-9-])--[a-z][a-z0-9-]{2,}", "un flag `--...`"),
    (r"\bCURA\s*\d", "CURA n"),
    # ### ⭐ **ALLARGATO il 2026-10-09**, perche- il guardiano dichiara che `PI-OGGETTI-ERA1` era
    # ### ### **troppo stretto:** una ### **funzione o una variabile del simulatore** e- un
    # ### oggetto concreto dell-era 1 ### **tanto quanto un `.pkl`**, e cosi- uno
    # ### ### **script di `csv/_test_fork` o `csv/_seal_fork`.**
    (r"\bphivel\b|\bperc_[a-z]+|\b_avvelena_[a-z]*"
     r"|\bpasso_pieno\b|\bnet\.step\b|\bmitosi\b|\bcalcola_psi\b"
     r"|\bsmp_apri\b|\bsmpchiudi\b|\bpsispin\w*|\bcsnodoprev\b"
     r"|\bomega_s\b|\bchiralita_core_locale\b|\bforma_passo0\b",
     "una funzione o una variabile del simulatore"),
    (r"csv/_test_fork|csv/_seal_fork", "uno script di csv/_test_fork o csv/_seal_fork"),
    # ### ⛔ **IL MARCATORE «un file `.py` del repo» E- USCITO IL 2026-10-09, e il guardiano
    # ### ### dichiara l-errore suo -- ma IL MARCATORE L-AVEVO AGGIUNTO IO** *(mandato
    # ### dell-era delle voci di metodo)*, con la scusa che `PAT-1` nomina
    # ### `dovespingelagravita.py`.
    # ### ⭐ **PERCHE- ERA SBAGLIATO:** ### **quasi ogni voce di METODO nomina un `.py`** --
    # ### un presidio, un attrezzo, un collaudo -- e un `.py` ### **non e- un oggetto
    # ### dell-era `1`: e- un oggetto DEL REPO**, che vive ### **in entrambe le ere.**
    # ### ⛔ **Faceva `17` dei `20` segnali**, e quei `17` li avevo ### **elencati nel
    # ### referto come «il confine fra le due frasi dell-era»**: non erano un confine,
    # ### erano ### **rumore di un marcatore mio.**
    # ### ⚠ **E AVEVO GIA- TOLTO UN MARCATORE MIO UNA VOLTA** *(il `FLAG-COSTANTE`, perche-
    # ### rompeva `FALSO-ZERO`)*: ### **questo l-ho tenuto, e per quattro giri.**
    # ### ⛔ **UN PATTERN CHE AVEVO AGGIUNTO IO, E L-HO TOLTO.** Volevo far scattare
    # ### `CONFIG-1` su un ### **FLAG-COSTANTE** (`FORK_SU2`, `TAU_LUCE`), e il pattern
    # ### ### **faceva scattare `FALSO-ZERO` su `REGISTRO_STATO`** -- il caso che il mandato
    # ### dice che ### **NON deve scattare.** ### ✔ **E non serviva:** `CONFIG-1` scatta
    # ### ### **dal suo `csv/_config_delle_misure.py`**, che la riga d-origine nomina.
    # ### ⭐ **Un marcatore che il mandato non chiede e che rompe un caso negativo
    # ### si TOGLIE, non si aggiusta.**
)
_ERA1_RE = tuple((re.compile(r, re.I), q) for r, q in ERA1_OGGETTI)


_RIGHE = {}


def _riga_origine_di(v):
    """### La riga d-origine della voce, ### **o la stringa vuota.**

    ### ⚠ **L-import e- QUI DENTRO e non in testa**, perche- `csv/_righe_origine.py`
    importa a sua volta questo modulo: ### **un import in testa sarebbe circolare.**
    """
    i = v["id"]
    if i not in _RIGHE:
        try:
            import _righe_origine as _RO
            r = _RO.riga_origine(v)[0]
        except Exception:
            r = None
        _RIGHE[i] = " ".join((r or "").split())
    return _RIGHE[i]


def _f8_era1(voci):
    """### `PI-OGGETTI-ERA1`: una voce `ENTRAMBE` NON CHIUSA che nomina un oggetto concreto dell-era `1`.

    ### ⛔ **SEGNALA, non decide:** il mandato dice che i segnali che restano
    ### **si ELENCANO, non si correggono.**
    ### ⚠ **Solo le NON CHIUSE**, e il mandato lo dice: ### **una voce chiusa non si sposta
    piu-.**
    """
    fuori = []
    for v in voci:
        if str(v["era"]) != "ENTRAMBE" or v["stato"] == "CHIUSA" or _coperto(v, "PI-OGGETTI-ERA1"):
            continue
        # ### ⛔ **F8 LEGGEVA UN TITOLO TRONCATO, ed e- L-ERRORE (d) applicato a un
        # ### presidio:** il titolo di `CONFIG-1` finisce *<<28 LEGGI SU 31 SPENTE,
        # ### misurato...>>*, e ### **la riga d-origine nomina `csv/_config_delle_misure.py`
        # ### e i flag `FORK_SU2`, `CAMPO_SPINORIALE`, `TAU_LUCE`.** Il mandato dice che
        # ### `PI-OGGETTI-ERA1` ### **deve** scattare su `CONFIG-1`: ### **senza la riga d-origine non
        # ### puo-.**
        t = ((v.get("titolo") or "") + " " + (v.get("descrizione") or "")
             + " " + _riga_origine_di(v))
        visti = []
        for r, q in _ERA1_RE:
            m = r.search(t)
            if m:
                visti.append("%s (<<%s>>)" % (q, " ".join(m.group(0).split())[:40]))
        if visti:
            fuori.append((v["id"], "era `ENTRAMBE` ma nomina un oggetto dell-era 1: "
                                   + "; ".join(visti[:4])))
    return fuori


def _f12_chiusura_orfana(voci):
    """### `PI-CHIUSURA-ORFANA`: una `chiusura` non vuota ### **su una voce che non e- `CHIUSA`.**

    ### ⛔ **E- UN ERRORE, non un segnale:** una voce che porta *<<chiusa dal commit `X`
    con criterio `Y`>>* e ### **non e- chiusa MENTE** -- e mente ### **in un campo che
    un programma legge** *(`valida` pretende `criterio` e `commit` quando lo stato e-
    `CHIUSA`; il rovescio ### **non lo chiedeva nessuno**)*.

    ### ⚠ **Da dove venivano le `41`:** ### **dalla migrazione.** Avevano tutte
    `commit` = `era-1-secondo-ordine` *(il NOME del tag)* e criterio *<<chiusa
    nell-era 1 (stato `chiuso` al tag …)>>*, e il lavoro dopo le ha portate a
    `SOSPESA` ### **lasciando la `chiusura` dietro.**

    ### ⭐ **E la cura NON ha scelto fra i due campi a caso: ha chiesto al DOCUMENTO.**
    `40` righe ### **non chiudono** -> la `chiusura` ### **si svuota**; `1` chiude
    *(`Z22`)* -> ### **`CHIUSA`**, col commit ricavato.

    ### **E- PURA**, come `PI-FISICA-ERA1-NON-SOSPESA` e `PI-ERA-STATO`: il collaudo la prova ### **su una COPIA.**
    """
    err = []
    for v in voci:
        ch = v["chiusura"] or {}
        if ch and v["stato"] != "CHIUSA":
            err.append("`PI-CHIUSURA-ORFANA` `%s`: la `chiusura` e- piena (commit `%s`) ma lo stato e- "
                       "`%s`. Una voce che dice <<chiusa dal commit X>> e non e- chiusa "
                       "MENTE, e mente in un campo che un programma legge"
                       % (v["id"], ch.get("commit", "")[:40], v["stato"]))
    return err


def _f9_era_stato(voci):
    """### `PI-ERA-STATO`: l-era e lo stato ### **non sono indipendenti.**

    ### **La regola del mandato:** era `ENTRAMBE` ### **=> stato `APERTA` o `CHIUSA`**;
    era `2` ### **=> stato `AGENDA`.** ### ⭐ **Il perche- e- che l-era dice QUANDO una
    cosa vive, e lo stato dice COM-E- ADESSO:** una voce che vale per ### **entrambe le
    ere** non puo- essere ### **SOSPESA**, perche- <<sospesa>> vuol dire
    ### **<<rimandata all-era 2>>** -- e una cosa che vale ### **anche** nell-era 2
    ### **non si puo- rimandare a se stessa.** Una voce dell-era `2` e- ### **agenda**,
    perche- l-era 2 ### **non e- cominciata.**

    ### ⛔ **NON E- NEL VALIDATORE, E NON E- UN PRESIDIO** *(`A9`)*: il mandato lo
    vuole ### **BLOCCANTE**, e oggi ### **`5` voci lo violano** -- `A2`,
    `LUNGA-BATTITO-CADUTA`, `PRESTAZIONI-CORSE`, `REPERTI-IMMUTABILI`, `RIPRESA-ARGV`.
    ### **`indice.py valida` gira nel `pre-commit`**, quindi accenderlo adesso
    ### **bloccherebbe OGNI COMMIT DEL REPO**, compreso quello che lo accende: l-hook
    gira il codice ### **dell-albero di lavoro.** ### ➜ **La riga che lo accende sta
    nello STESSO commit che cura le `5`**, e la cura e- ### **il file del guardiano.**

    ### ⚠ **E le `5` si curano in DUE modi diversi** -- portarle a `APERTA`, oppure
    portarle a ### **era `1`** *(dove `SOSPESA` e- lecito, e `PI-OGGETTI-ERA1` segnala proprio che
    nominano oggetti dell-era 1)*. ### ⛔ **QUALE DEI DUE lo dice il file, non io.**

    ### **E- PURA**, come `PI-FISICA-ERA1-NON-SOSPESA`: il collaudo la prova ### **su una COPIA.**
    """
    err = []
    for v in voci:
        # ### ⭐ **UN SEGNAPOSTO SI SALTA:** `DA_CLASSIFICARE` non e- uno stato, e-
        # ### ### **l-assenza di uno stato** -- la stessa scelta del punto `1` del
        # ### 2026-10-09, dove lo stato non si decide prima della classe.
        if v["stato"] == "DA_CLASSIFICARE":
            continue
        e = str(v["era"])
        # ### ⭐ **`SUPERATA` ENTRA FRA GLI AMMESSI il 2026-10-09**, e corregge
        # ### ### **una MIA strettezza:** avevo scritto *<<`ENTRAMBE` => `APERTA` o
        # ### `CHIUSA`>>* ### **alla lettera del mandato**, e una voce che vale per entrambe
        # ### le ere ### **puo- essere SUPERATA** da una decisione o da un-altra voce.
        # ### ⛔ **<<Superata>> non e- <<rimandata>>:** e- ### **risolta da fuori**, e per
        # ### questo non cade nel divieto che colpisce `SOSPESA`.
        if e == "ENTRAMBE" and v["stato"] not in ("APERTA", "CHIUSA", "SUPERATA"):
            err.append("`PI-ERA-STATO` `%s`: era `ENTRAMBE` con stato `%s`. Una voce che vale per "
                       "ENTRAMBE le ere e- APERTA o CHIUSA: <<sospesa>> vuol dire "
                       "<<rimandata all-era 2>>, e una cosa che vale ANCHE nell-era 2 "
                       "non si puo- rimandare a se stessa"
                       % (v["id"], v["stato"]))
        if e == "2" and v["stato"] != "AGENDA":
            err.append("`PI-ERA-STATO` `%s`: era `2` con stato `%s`. L-era 2 NON E- COMINCIATA: "
                       "una sua voce e- AGENDA" % (v["id"], v["stato"]))
    return err


def _f10_criterio_metodo(voci):
    """### `PI-CRITERIO-METODO`: una voce di classe `CRITERIO` ### **sta nel dominio `METODO`.**

    ### ⭐ **Un criterio e- una REGOLA DI GIUDIZIO**, e una regola di giudizio
    ### **non e- fisica**: dice ### **come si decide**, non ### **come va il mondo.**
    ### ⛔ **E- UN ERRORE, non un segnale**, e il mandato lo dice: *<<entrambi errori
    (validazione bloccante)>>*.

    ### ✔ **QUESTO SI PUO- ACCENDERE SUBITO: le violazioni oggi sono ZERO**, misurate
    sulle `846` voci a `bfb1596`. ### **Un presidio che si accende su zero violazioni
    non ha bisogno di nessuna cura prima** -- ed e- per questo che `PI-ERA-STATO` e `PI-CRITERIO-METODO`,
    che il mandato chiede ### **insieme**, ### **si separano: uno si puo-, l-altro no.**

    ### ⚠ **E lo zero NON e- un FALSO-ZERO:** il punto `4` del 2026-10-09 ha portato
    `REGISTRO_FISICA:D37` da `CRITERIO`/`INFRASTRUTTURA` a `DIFETTO`, e
    `REGISTRO_FISICA:C3` a `CRITERIO`/`METODO`. ### **Lo zero di oggi e- il risultato di
    quelle cure**, e il collaudo lo prova ### **con un caso che DEVE scattare.**
    """
    err = []
    for v in voci:
        if v["classe"] == "CRITERIO" and v["dominio"] != "METODO":
            err.append("`PI-CRITERIO-METODO` `%s`: classe `CRITERIO` nel dominio `%s`. Un criterio e- "
                       "una REGOLA DI GIUDIZIO, e una regola di giudizio non e- fisica: "
                       "dice COME SI DECIDE, non come va il mondo" % (v["id"],
                                                                      v["dominio"]))
    return err


def _f7_stato(voci):
    """### `PI-FISICA-ERA1-NON-SOSPESA`: una voce `FISICA` dell-era `1` con uno stato che non e- `SOSPESA` ne-
    `CHIUSA`.

    ### ⛔ **E- UN ERRORE, non un segnale**, e il mandato lo dice: *<<la validazione
    fallisce>>*. ### **La regola in vigore: la fisica dell-era `1` NON CHIUSA e- `SOSPESA`**
    -- e l-### **<<APERTO>>** che un documento scrive e- lo stato ### **dell-era `1`**, che
    sta in `stato_era_1`.

    ### ⚠ **Nasce da un errore mio:** nel punto `5` del 2026-10-09 ho ripristinato `4` voci
    leggendo lo stato da `## APERTO <ID>` e ### **l-ho messo nel campo `stato`**, che e- lo
    stato ### **di oggi**. Avevo ### **dichiarato la provenienza del dato**, e questo mi ha
    fatto sembrare prudente ### **un errore di campo**: ### **per questo la regola ha un
    presidio e non solo una riga in `par9.md`.**

    ### ⛔ **E- PURA** *(prende la lista, non legge il disco)* perche- ### **il collaudo deve
    poterla provare su una COPIA**, mai sull-indice vero.
    """
    err = []
    for v in voci:
        # ### ⭐ **`SUPERATA` STA CON `CHIUSA`, NON CON `APERTA`:** la regola dice *<<la
        # ### fisica dell-era 1 ### **NON CHIUSA** e- SOSPESA>>*, e una voce
        # ### ### **superata da una decisione NON E- APERTA** -- e- risolta ### **da
        # ### fuori.** `TRANSIZIONI` lo conferma: da `SUPERATA` si esce ### **solo verso
        # ### `APERTA`**, cioe- ### **solo riaprendola.**
        # ### ⭐ **ESTESO A QUALSIASI DOMINIO il 2026-10-09**, e il perche- e- che la
        # ### regola non parlava di fisica: ### **una voce dell-era 1 NON CHIUSA e-
        # ### SOSPESA**, e vale per `METODO`, `INFRASTRUTTURA` e `DOCUMENTAZIONE` come per
        # ### `FISICA`. ### **Violava su 16 voci** -- le 14 `CENS-*`, `D32-CONTATORE` e
        # ### `RAMI-OFF-CURA2` -- e ### **sono state curate PRIMA che il presidio si
        # ### accendesse**, perche- un presidio bloccante acceso prima della cura
        # ### ### **rende il lotto che lo curerebbe inapplicabile.**
        vietato = (str(v["era"]) == "1"
                   and v["stato"] not in ("SOSPESA", "CHIUSA", "SUPERATA"))
        if vietato:
            err.append("`PI-FISICA-ERA1-NON-SOSPESA` `%s`: `%s`/era `1` con stato `%s`. Una voce dell-era 1 "
                       "NON CHIUSA e- SOSPESA; se quello stato viene da un documento "
                       "(<<APERTO>>), e- lo stato DELL-ERA 1 e va in `stato_era_1`"
                       % (v["id"], v["dominio"], v["stato"]))
    return err


def _f1_gemelle(voci):
    """### `PI-GEMELLE`: il titolo di una voce ### **cita l-ID di un-altra**, e ### **dominio o era
    DIFFERISCONO.**"""
    ids = {v["id"]: v for v in voci}
    fuori = []
    for v in voci:
        if _coperto(v, "PI-GEMELLE"):
            continue
        for tok in set(_TOKEN.findall(v.get("titolo") or "")):
            w = ids.get(tok)
            if w is None or w["id"] == v["id"]:
                continue
            # ### LA RESTRIZIONE DEL 2026-10-09, E IL DIFETTO ERA MIO: CITARE UN ASSIOMA
            # ### NON E- ESSERE GEMELLE. `D24` e- un difetto dell-era 1 che VIOLA `A2`, e
            # ### `A2` vale per ### **ENTRAMBE** le ere: <<differiscono>> e- GIUSTO che sia
            # ### vero, e non e- una mescolanza. Lo stesso per i presidi (`H-*`) e per i
            # ### SEGNAPOSTO, che ### **non hanno ancora un dominio ne- un-era.**
            # ### ### **42 dei 49 segnali erano questo**, e io ne avevo dichiarati 12.
            if w["classe"] in ("STANDARD", "PRESIDIO", "NON_DEFINITA"):
                continue
            # ### ⛔ **LO STATO E- USCITO DAL CONTROLLO IL 2026-10-09, ed e- un errore che
            # ### ### il guardiano dichiara SUO -- ma l-applicazione era MIA.** Lo avevo
            # ### esteso allo stato *<<solo per lo schema `D`/`Z`>>* ### **alla lettera del
            # ### prompt**, e nel referto avevo scritto che le ### **`9` coppie
            # ### disallineate erano «UN RITROVATO»**: ### **le ho elencate come un
            # ### difetto, ed erano LA FORMA GIUSTA.**
            # ### ⭐ **LA DISTINZIONE CHE NON AVEVO:** la voce `D` e- ### **il DIFETTO**, la
            # ### `Z` e- ### **il REPERTO che lo ha trovato.** Io le leggevo come
            # ### ### **<<la stessa cosa scritta due volte>>**, e sono ### **un difetto e
            # ### la misura che lo ha scoperto** -- e ### **una misura resta
            # ### un-AVVERTENZA anche dopo che il difetto e- curato** *(`D19` CURATO,
            # ### `Z88` aperta come avvertenza)*.
            # ### ✔ **Restano `dominio` ed `era`:** quelli ### **devono** coincidere,
            # ### perche- il difetto e il suo reperto ### **parlano della stessa cosa,
            # ### nella stessa era.**
            if w["dominio"] != v["dominio"] or str(w["era"]) != str(v["era"]):
                fuori.append((v["id"], "il titolo cita `%s`, che e- `%s`/era `%s`, mentre "
                                       "questa e- `%s`/era `%s`"
                              % (w["id"], w["dominio"], w["era"],
                                 v["dominio"], v["era"])))
    return fuori


def _f2_era2(voci):
    """### `PI-SIMBOLI-ERA1`: una voce dell-era `2` che ### **nomina il vecchio codice.**"""
    fuori = []
    for v in voci:
        if str(v["era"]) != "2" or _coperto(v, "PI-SIMBOLI-ERA1"):
            continue
        t = _testo_voce(v)
        tl = t.lower()
        visti = [s for s in ERA1_SIMBOLI if s.lower() in tl]
        if _RIGA_NNNN.search(t):
            visti.append("un numero di riga `" + _RIGA_NNNN.search(t).group(0) + "`")
        m = _FLAG.search(t)
        if m:
            visti.append("un flag `" + m.group(0) + "`")
        if visti:
            fuori.append((v["id"], "era `2` ma nomina l-era `1`: " + ", ".join(visti[:5])))
    return fuori


def _f3_fisica_strumenti(voci):
    """### `PI-PAROLE-STRUMENTO`: una voce `FISICA` il cui ### **TITOLO** parla di strumenti.

    ### ⚠ **Solo il titolo**, e il mandato dice cosi-: *«il cui TITOLO parla di…»*.
    ### **Preso alla lettera**, e se risulta troppo stretto lo si scrive invece di allargarlo.
    """
    fuori = []
    for v in voci:
        if v["dominio"] != "FISICA" or _coperto(v, "PI-PAROLE-STRUMENTO"):
            continue
        tl = (v.get("titolo") or "").lower()
        visti = [s for s in STRUMENTI if s.lower() in tl]
        if visti:
            fuori.append((v["id"], "`FISICA`, ma il titolo parla di strumenti: "
                          + ", ".join("`%s`" % s for s in visti[:5])))
    return fuori


# ### ⛔ **LA REGOLA DELL-INTESTAZIONE** *(punto `5` del 2026-10-09)*. `PI-ETICHETTA-DEFINITA` segnalava `30`
# ### etichette, e ### **circa meta- erano intestazioni in cui l-ID sta DENTRO LA PROSA**:
# ### *<<`### 1.2 ⚠ E LA LETTURA CHE DECIDE DAVVERO — dichiarata POST-HOC, non era fissata
# ### prima`>>*. ### **`POST-HOC` non e- il soggetto di quell-intestazione: e- un aggettivo.**
# ### Lo stesso per `RI-LETTO`, `RI-VERIFICATI`, `SOVRA-CORREGGE`, che sono ### **VERBI.**
# ###
# ### ✔ **UN-INTESTAZIONE DEFINISCE SE, E SOLO SE:**
# ###   ① si toglie dall-inizio, ripetutamente, cio- che NON porta significato -- i `#`, gli
# ###     spazi, i ### **simboli non alfanumerici** *(`⛔` `✅` `⚠` `⭐` `➜` `①` `*` backtick
# ###     `—` `§`)*, la ### **numerazione** *(`5.`, `1.2`, `5-bis.`, `§38`)* e ### **una
# ###     parola di STATO** *(`APERTO`, `CHIUSO`, `APERTA`, `CHIUSA`, `RISOLTO`,
# ###     `SOSPESO`)*; ### **e il resto COMINCIA con l-ID** -- cioe- ### **l-ID e- il
# ###     SOGGETTO**;
# ###   ② ### **e c-e- CONTENUTO:** altri `3` caratteri sulla riga dopo l-ID,
# ###     ### **oppure** almeno una riga non vuota e non-intestazione ### **SOTTO**.
# ### ⚠ **Il ② serve a `## APERTO CURA1-CORTO`**, dove il contenuto e- ### **il paragrafo
# ### sotto**: l-intestazione e- nuda, la sezione no. ### **<<Senza contenuto>> vuol dire
# ### che non c-e- NIENTE, ne- accanto ne- sotto.**
_H_SIMBOLI = re.compile(r"^[^0-9A-Za-z]+")
_H_NUM = re.compile(r"^(?:§\s*)?\d+(?:[.-][0-9A-Za-z]+)*\.?\s*")
_H_STATO = re.compile(r"^(?:APERTO|APERTA|CHIUSO|CHIUSA|RISOLTO|RISOLTA|SOSPESO|SOSPESA)\b\s*", re.I)


def _intestazione_definisce(righe, k, idv):
    """### `righe[k]` e- un-intestazione: ### **definisce `idv`?** Vedi la regola sopra."""
    t = re.sub(r"^#{1,6}\s*", "", righe[k])
    for _ in range(8):
        prima = t
        for r in (_H_SIMBOLI, _H_NUM, _H_STATO):
            t = r.sub("", t, count=1)
        if t == prima:
            break
    if not t.startswith(idv):
        return False
    resto = t[len(idv):]
    # ### ⛔ **e l-ID deve finire DOVE FINISCE IL TOKEN:** `S1` non definisce `S10`.
    if resto[:1] and (resto[0].isalnum() or resto[0] in "_:-"):
        return False
    if len(resto.strip()) >= 3:
        return True
    # ### ② il CONTENUTO puo- stare SOTTO: `## APERTO CURA1-CORTO` + il paragrafo
    for r in righe[k + 1:k + 12]:
        if r.strip().startswith("#"):
            break
        if len(r.strip()) >= 3:
            return True
    return False


def _f4_etichette(etich):
    """### `PI-ETICHETTA-DEFINITA`: un-etichetta rimossa che ### **in un documento E- DEFINITA.**"""
    fuori = []
    riga_t = "|"
    for e in etich:
        idv = e["id"]
        # ### ⛔ **UN-ETICHETTA NON HA UN `meta`:** non e- una voce, e lo schema delle
        # ### voci non la riguarda. ### **Quindi la sua eccezione sta in un campo suo**,
        # ### `eccezione_presidio`, scritto con `etichette-lotto` -- la stessa via, con
        # ### la sua riga di storico.
        if e.get("eccezione_presidio"):
            continue
        q = re.escape(idv)
        rt = re.compile(r"^\s*\|\s*\**\s*`?" + q + r"`?\s*\**\s*\|")
        it = re.compile(r"^#{1,6}\s.*(?<![A-Za-z0-9_:-])" + q + r"(?![A-Za-z0-9_:-])")
        for f in (e.get("file_citanti") or []):
            fp = str(f).replace(chr(92), "/")
            if any(fp == g or fp.startswith(g) for g in VISTE_GENERATE):
                continue
            p = os.path.join(RADICE, fp)
            if not os.path.exists(p):
                continue
            trovata = None
            righe = io.open(p, encoding="utf-8", errors="replace").read().split(NL)
            for n, r in enumerate(righe, 1):
                if rt.match(r):
                    trovata = ("una riga di tabella", n)
                    break
                # ### ⛔ **NON BASTA CHE L-INTESTAZIONE CONTENGA L-ID:** vedi la regola
                # ### dell-intestazione qui sopra.
                if it.match(r) and _intestazione_definisce(righe, n - 1, idv):
                    trovata = ("un-intestazione", n)
                    break
            if trovata:
                fuori.append((idv, "etichetta rimossa, ma %s la DEFINISCE in `%s:%d`"
                              % (trovata[0], fp, trovata[1])))
                break
    del riga_t
    return fuori


# ### ⛔ **UNA NOTA PUO- DICHIARARE UNA TRIPLA**, e allora la tripla e- un-ASSERZIONE:
# ### *<<correzione v3 blocco G2: ### **FISICA/era 1/SOSPESA**>>* dice
# ### ### **che cos-e- la voce**, e se la voce e- cambiata ### **la nota e- SCADUTA.**
# ### ⚠ **E NON E- LEGGERE LA PROSA:** serve ### **la forma esatta**
# ### `DOMINIO/era N/STATO`. Sulle `846` voci la trovano ### **`6` note**, e
# ### ### **una sola e- incoerente: `G1`** -- esattamente il caso che il mandato
# ### nomina. ### ⛔ **La via grossolana -- <<la nota nomina uno stato diverso>> --
# ### dava `69` SEGNALI**, perche- la maggior parte delle note parla
# ### ### **di un-altra era o fa una DOMANDA** *(<<superata da A16?>>)*: era
# ### ### **la condizione di FERMO scritta nel task history**, e mi sono fermato.
_TRIPLA = re.compile(r"(FISICA|METODO|INFRASTRUTTURA|DOCUMENTAZIONE)\s*/\s*era\s*"
                    r"(1|2|ENTRAMBE)\s*/\s*(APERTA|CHIUSA|SOSPESA|AGENDA|SUPERATA)",
                    re.I)


def _f6_note(voci):
    """### `PI-NOTA-CONTRADDICE-LISTA`: una `nota_guardiano` che ### **nomina una lista del guardiano** e che
    ### **contraddice** il dominio, l-era o lo stato della voce.

    ### ⛔ **NON SI LEGGE LA PROSA, e la prima stesura lo faceva:** cercava nella nota le
    parole `SUPERATA`, `SOSPESA`, `fisica`… e le prendeva per ### **asserzioni di stato.**
    ### **`11` dei `13` segnali erano UNA SOLA FRASE** -- *«candidata ### **SUPERATA** dalla
    decisione sulla sincronizzazione»*, che e- ### **prosa.** ### **Un presidio che legge la
    prosa legge male**, e l-ha trovato il presidio stesso guardando la sua uscita.

    ### ✔ **Si confronta con CIO- CHE LA LISTA `N` DICEVA** *(`LISTE_GUARDIANO`, una tabella
    dichiarata)*. ### ⚠ **E una nota che si DICHIARA correzione non si guarda:**
    *<<correzione della lista 2 …>>* ### **non e- incoerente, e- informativa.**
    """
    fuori = []
    for v in voci:
        nota = (v.get("meta") or {}).get("nota_guardiano") or ""
        if not nota or _coperto(v, "PI-NOTA-CONTRADDICE-LISTA"):
            continue
        # ### ✔ **PRIMA LA TRIPLA DICHIARATA**, che vale ### **anche per una nota che si
        # ### dice <<correzione>>:** una correzione ### **dichiara cio- che la voce E-**, e
        # ### se la voce si e- mossa ### **la dichiarazione e- SCADUTA.** `G1` dice
        # ### *<<correzione v3 blocco G2: FISICA/era 1/SOSPESA>>* e oggi e- ### **`CHIUSA`**,
        # ### perche- il guardiano ha dichiarato che e- ### **<<FATTO>>.**
        mt = _TRIPLA.search(nota)
        if mt:
            d, e, s = (x.upper() for x in mt.groups())
            g2 = []
            if v["dominio"] != d:
                g2.append("la nota dichiara `%s`, la voce e- `%s`" % (d, v["dominio"]))
            if str(v["era"]).upper() != e:
                g2.append("la nota dichiara era `%s`, la voce e- era `%s`" % (e, v["era"]))
            if v["stato"] != s:
                g2.append("la nota dichiara `%s`, la voce e- `%s`" % (s, v["stato"]))
            if g2:
                fuori.append((v["id"], "la nota DICHIARA una tripla `dominio/era/stato` e "
                                       "la voce non e- piu- quella: %s" % "; ".join(g2)))
                continue
        m = re.search(r"list[ae]\s*([123])?\s*del guardiano", nota, re.I)
        if not m:
            continue
        # ### UNA NOTA CHE SI DICHIARA CORREZIONE NON SI GUARDA: <<correzione della lista
        # ### 2 ...>> NON e- incoerente, e- INFORMATIVA. Segnalarla sarebbe un FALSO-UNO.
        if "correzione" in nota.lower() or not m.group(1):
            continue
        dom, era, stato = LISTE_GUARDIANO[m.group(1)]
        guai = []
        if dom and v["dominio"] != dom:
            guai.append("la lista diceva `%s`, la voce e- `%s`" % (dom, v["dominio"]))
        if era and str(v["era"]) != era:
            guai.append("la lista diceva era `%s`, la voce e- era `%s`" % (era, v["era"]))
        if stato and v["stato"] != stato:
            guai.append("la lista diceva `%s`, la voce e- `%s`" % (stato, v["stato"]))
        if guai:
            fuori.append((v["id"], "la nota nomina la lista `%s` del guardiano e la voce "
                                   "NON e- piu- cio- che quella lista diceva: %s"
                          % (m.group(1), "; ".join(guai))))
    return fuori


def segnali(voci, reg, verboso=True):
    """### I CINQUE PRESIDI CHE SEGNALANO. ### ⛔ **NON cambiano il codice d-uscita.**"""
    del reg
    etich = [json.loads(r) for r in io.open(ETICH, encoding="utf-8").read().split(NL)
             if r.strip()] if os.path.exists(ETICH) else []
    n_fisica = sum(1 for v in voci if v["dominio"] == "FISICA")
    n_era2 = sum(1 for v in voci if str(v["era"]) == "2")
    n_note = sum(1 for v in voci
                 if re.search(r"list[ae]\s*[123]?\s*del guardiano",
                              (v.get("meta") or {}).get("nota_guardiano") or "", re.I))
    tutti = [("PI-GEMELLE", "GEMELLE: il titolo cita l-ID di un-altra, e dominio o era differiscono",
              _f1_gemelle(voci), len(voci)),
             ("PI-SIMBOLI-ERA1", "ERA 2 PULITA: una voce dell-era 2 che nomina simboli dell-era 1",
              _f2_era2(voci), n_era2),
             ("PI-PAROLE-STRUMENTO", "FISICA CHE PARLA DI STRUMENTI: il titolo di una voce FISICA",
              _f3_fisica_strumenti(voci), n_fisica),
             ("PI-ETICHETTA-DEFINITA", "ETICHETTA CON DEFINIZIONE: un-etichetta che un documento DEFINISCE",
              _f4_etichette(etich), len(etich)),
             ("PI-NOTA-CONTRADDICE-LISTA", "NOTE COERENTI: una nota che nomina una lista e la contraddice",
              _f6_note(voci), n_note),
             ("PI-OGGETTI-ERA1", "ERA 1 NEL TESTO: una voce ENTRAMBE che nomina un oggetto concreto",
              _f8_era1(voci),
              sum(1 for v in voci if str(v["era"]) == "ENTRAMBE"
                  and v["stato"] != "CHIUSA"))]
    if verboso:
        print("=" * 96)
        print("I PRESIDI CONTRO LE MESCOLANZE  --  SEGNALANO, NON DECIDONO")
        print("=" * 96)
        for sig, che, fuori, su in tutti:
            # ### ⚠ **IL TOOL MISURA, LA LETTURA STA NEL REFERTO.** La soglia del
            # ### `10%` l-ho fissata nel task history ### **prima di misurare**, ed e-
            # ### un FATTO utile; ma ### **<<TROPPO GROSSO>> e- un GIUDIZIO**, e su un
            # ### denominatore di `25` una percentuale non vuol dire niente. Quindi il
            # ### tool dice ### **che la soglia e- superata**, e il referto dice
            # ### ### **se il presidio e- troppo grosso DAVVERO.**
            grosso = ""
            if su and len(fuori) > su * 0.10:
                grosso = ("   ### oltre il 10%% di %d -- la LETTURA sta nel referto"
                          % su)
            print("  %s  %-70s %4d segnali su %d%s"
                  % (sig, che[:70], len(fuori), su, grosso))
        print()
        for sig, _che, fuori, _su in tutti:
            if not fuori:
                continue
            print("-" * 96)
            print("### `%s`: %d" % (sig, len(fuori)))
            print("-" * 96)
            for i, msg in fuori:
                print("  %-26s %s" % (i, msg))
        print()
        print("  ### I SEGNALI NON SI CORREGGONO DA QUI: si chiudono correggendo la voce,")
        print("  ### oppure con `meta.eccezione_presidio` CHE CITA IL TESTO ALLA LETTERA.")
    return tutti


def _head():
    """### `HEAD` adesso: il commit ### **su cui** la modifica e- fatta. Si sa, a differenza
    del commit che la ### **conterra-**."""
    q = subprocess.run(["git", "rev-parse", "--short=8", "HEAD"], cwd=RADICE,
                       capture_output=True, text=True)
    return (q.stdout or "").strip() if q.returncode == 0 else ""


def storico_commit():
    """### IL BLOCCO `D`: riempie il campo `commit` di ogni riga dello storico.

    ### ⛔ **Non si indovina: si LEGGE DAI LOG.** `storico.jsonl` e- ### **solo in
    aggiunta**, quindi per ogni commit che l-ha toccato le righe
    `[quante_prima, quante_dopo)` sono ### **esattamente quelle che quel commit ha
    scritto.** ### ✔ **E LA PREMESSA SI VERIFICA:** se una versione vecchia non e- un
    ### **prefisso** di quella nuova lo storico ### **non e- piu- solo-in-aggiunta**, e
    allora ### **questa funzione SI FERMA** invece di scrivere numeri sbagliati.

    ### ⚠ **UN LOTTO DI RITARDO, e non e- un difetto nascosto:** le righe scritte DOPO
    l-ultimo commit non hanno ancora un commit che le contenga, e restano vuote fino al
    giro dopo. ### **E- la conseguenza di quando esiste un commit**, non una scelta.
    """
    righe = [r for r in io.open(STORICO, encoding="utf-8").read().split(NL) if r.strip()]
    vive = [json.loads(r) for r in righe]
    q = subprocess.run(["git", "log", "--reverse", "--format=%h", "--",
                        "doc/indice/storico.jsonl"], cwd=RADICE, capture_output=True,
                       text=True)
    commits = [c for c in (q.stdout or "").split() if c]
    print("=" * 96)
    print("IL CAMPO `commit` DELLO STORICO -- preso DAI LOG, non indovinato")
    print("=" * 96)
    print("  righe: %d   commit che hanno toccato il file: %d" % (len(vive), len(commits)))
    prec, assegnate = 0, 0
    for c in commits:
        qc = subprocess.run(["git", "show", "%s:doc/indice/storico.jsonl" % c], cwd=RADICE,
                            capture_output=True, text=True, encoding="utf-8")
        sue = [r for r in (qc.stdout or "").split(NL) if r.strip()]
        # ### LA PREMESSA, VERIFICATA: la versione di allora e- un PREFISSO di oggi.
        assert len(sue) <= len(righe), ("`%s`: aveva %d righe, oggi il file ne ha %d: lo "
                                        "storico NON e- solo-in-aggiunta" % (c, len(sue),
                                                                             len(righe)))
        for k, r in enumerate(sue):
            a, b = json.loads(r), vive[k]
            assert (a["id"], a["quando"], a["motivo"]) == (b["id"], b["quando"],
                                                           b["motivo"]), (
                "`%s`: la riga %d di allora NON e- la riga %d di oggi: lo storico e- stato "
                "RISCRITTO, e questa funzione si ferma" % (c, k + 1, k + 1))
        n = 0
        for k in range(prec, len(sue)):
            if not vive[k].get("commit"):
                vive[k]["commit"] = c
                n += 1
        if len(sue) > prec:
            print("  %-10s righe %5d..%-5d  (%d)  %s" % (c, prec + 1, len(sue),
                                                         len(sue) - prec,
                                                         "riempite %d" % n))
        assegnate += n
        prec = max(prec, len(sue))
    restano = [k for k, v in enumerate(vive) if not v.get("commit")]
    print()
    print("  riempite: %d   senza commit: %d" % (assegnate, len(restano)))
    if restano:
        print("  ### LE %d SENZA COMMIT SONO LE RIGHE %d..%d, scritte DOPO l-ultimo commit:"
              % (len(restano), restano[0] + 1, restano[-1] + 1))
        print("  ### il commit che le conterra- NON ESISTE ANCORA. Si riempiono al giro dopo,")
        print("  ### ed e- IL LOTTO DI RITARDO dichiarato nel sorgente di questa funzione.")
    if assegnate:
        io.open(STORICO, "w", encoding="utf-8", newline=NL).write(
            NL.join(json.dumps(v, ensure_ascii=False) for v in vive) + NL)
        print("  scritto doc/indice/storico.jsonl")
    return 0


def etichette_lotto(percorso):
    """### LA VIA DI SCRITTURA PER LE ETICHETTE RIMOSSE.

    ### ⚠ **Perche- serviva:** il punto `5` del 2026-10-09 deve ### **chiudere un
    segnale di `PI-ETICHETTA-DEFINITA` su un'etichetta** *(`GLOBALE-DIS`: la sua unica definizione dice
    che l'ID ### **non esiste**)* e ### **lasciare una nota «da decidere da Luca»** su
    tre altre. ### ⛔ **Un'etichetta NON ha un `meta`**, perche- non e- una voce: la
    sua eccezione e la sua nota stanno in ### **campi suoi**, e `PI-ETICHETTA-DEFINITA` li legge.

    ### ✔ **Resta LA STESSA VIA:** ogni modifica ### **una riga di storico**, col
    motivo, e ### **se un ID non e- fra le etichette il lotto non parte.**
    """
    righe = [json.loads(r) for r in io.open(percorso, encoding="utf-8").read()
             .split(NL) if r.strip()]
    etich = [json.loads(r) for r in io.open(ETICH, encoding="utf-8").read().split(NL)
             if r.strip()]
    per = {e["id"]: e for e in etich}
    storia = []
    for r in righe:
        idv = r["id"]
        assert idv in per, "`%s` NON e- fra le etichette rimosse" % idv
        e = per[idv]
        prima = json.loads(json.dumps(e))
        for k, val in r.items():
            if k in ("id", "motivo", "quando"):
                continue
            e[k] = val
        motivo = r.get("motivo") or ("(etichetta) aggiornata: " + ", ".join(
            k for k in r if k not in ("id", "motivo", "quando")))
        assert len(motivo) >= 20, "`%s`: motivo troppo corto" % idv
        storia.append({"quando": r.get("quando") or _oggi(), "id": idv,
                       "motivo": motivo, "commit": "", "commit_base": _head(),
                       "prima": prima, "dopo": json.loads(json.dumps(e))})
    _scrivi_jsonl(ETICH, etich)
    with io.open(STORICO, "a", encoding="utf-8", newline=NL) as f:
        for s in storia:
            f.write(json.dumps(s, ensure_ascii=False) + NL)
    print("  lotto ETICHETTE applicato: %d etichette, %d righe di storico"
          % (len(righe), len(storia)))


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
                       "commit": r.get("commit", ""), "commit_base": _head(),
                       "prima": None, "dopo": json.loads(json.dumps(v))})
    # ### ⛔ **`PI-STORICO-SENZA-COMMIT` NON dipende dalle voci** -- guarda `storico.jsonl` sul disco contro
    # ### `HEAD` -- quindi ### **si chiede PRIMA di scrivere**, non alla fine: alla fine
    # ### sarebbe ### **un allarme su un file GIA- SCRITTO.**
    err = _f5_storico(voci) + valida(voci, reg, verboso=False, derivati=False)
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
    if cmd == "etichette-lotto":
        etichette_lotto(pos[0])
        return 0
    if cmd == "era2-lotto":
        # ### ⛔ **LA VIA DI SCRITTURA DEI REGISTRI DELL-ERA `2`**, e sta QUI perche- il
        # ### mandato dice *<<via `indice.py`>>*: ### **una sola porta**, come per le voci.
        # ### ⚠ **Il codice vive in `csv/_indice_era2.py`** -- `indice.py` e- gia-
        # ### ### **lungo**, e un file che cresce senza fine ### **nessuno lo rilegge.**
        import _indice_era2 as _E2
        return _E2.lotto(pos[0])
    if cmd == "era2-valida":
        import _indice_era2 as _E2
        return 1 if _E2.valida() else 0
    if cmd == "storico-commit":
        return storico_commit()
    if cmd == "segnali":
        segnali(voci, reg)
        return 0
    if cmd == "da-decidere":
        da_decidere(voci, reg)
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
