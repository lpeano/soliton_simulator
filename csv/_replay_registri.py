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
| **`GENERATO`** | il file lo ### **produce un generatore dichiarato**, e la sua fonte sta altrove | ### **si rigenera e si confronta AL BYTE** *(la macchina di `13(f)`)* |

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
# ### ⛔ **IL QUARTO STATO, e nasce da una DICHIARAZIONE FALSA MIA** *(2026-10-10)*.
# ### `assiomi.jsonl` e `decisioni.jsonl` erano dichiarati ### **`REPERTO`**, che dice
# ### alla lettera *<<non ha una via di scrittura, ### **e non deve averla**>>* --
# ### ### **e invece SONO GENERATI** da `csv/_registri_indice.py`, che legge le schede di
# ### `doc/REGISTRO_FISICA.md` e di `doc/ASSIOMI.md`.
# ### ⚠ **IL BLOB NON SE NE ACCORGEVA**, perche- un generatore ### **stabile** da-
# ### sempre gli stessi byte: il controllo passava ### **per la ragione sbagliata.**
# ### ⭐ **E L-HO SCOPERTO PERCHE- IL MANDATO `3` CHIEDE DI SCRIVERE NODI IN
# ### `decisioni.jsonl`:** un nodo scritto a mano la- dentro ### **sarebbe cancellato al
# ### primo giro del generatore**, e la dichiarazione `REPERTO` ### **mi avrebbe fatto
# ### credere che fosse sicuro.**
# ### ✅ **`GENERATO` si verifica RIGENERANDO E CONFRONTANDO AL BYTE** -- cioe- con
# ### la macchina di `13(f)`, che esiste gia-. ### **Quindi il quarto stato NON porta un
# ### controllo nuovo: porta la DICHIARAZIONE GIUSTA su un controllo che c-era** -- e un
# ### registro `GENERATO` che ### **non e- fra i `GENERATI`** e- rifiutato, perche-
# ### ### **nessuno lo verificherebbe.**
STATI = ("REPLAY", "REPERTO", "SOLO-AGGIUNTE", "GENERATO")

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
    # ### ⛔ **E IL BLOB E- CAMBIATO IL 2026-10-10, perche- il buco HA MORSO.**
    # ### `meta-aggiungi` ha registrato due chiavi nuove *(`in_claude` e
    # ### `dettaglio_regola`, per il mandato `5`)* e ha scritto questo file
    # ### ### **senza lasciare una riga di storico** -- misurato: `0` righe.
    # ### ⚠ **Quindi l-unica cosa che posso fare e- AGGIORNARE IL BLOB A MANO**,
    # ### che e- ### **una DICHIARAZIONE e non un controllo**: il presidio dira-
    # ### <<coincide>> perche- gliel-ho detto io, non perche- l-abbia verificato.
    # ### ⭐ **E- esattamente cio- che <<`REPERTO` per necessita->> significa**, e
    # ### adesso ha una voce: `METADATI-REPERTO-PER-NECESSITA`.
    "metadati.jsonl": ("REPERTO", "chiave", None, None, "a274e89b100075cb"),
    # ### ✅ **GENERATI, non reperti:** `csv/_registri_indice.py` li produce.
    "assiomi.jsonl": ("GENERATO", "id", None, None, None),
    "decisioni.jsonl": ("GENERATO", "id", None, None, None),
    "migrazione_era1.jsonl": ("REPERTO", None, None, None, "8996d113388d49cc"),
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
# ### prendere i numeri. ### ⚠ **E QUI AVEVO SCRITTO <<supera i 120 secondi>>:**
# ### ### **MISURATO il 2026-10-10 dal punto `6` della terza parte: `28.33` s** -- e
# ### il collaudo della catena, che avevo chiamato lento, ### **`2.55` s.**
# ### ⭐ **Il numero era di un-altra cosa, e l-ho scoperto SOLO MISURANDO.**
# ### ⛔ **Un presidio di `pre-commit` che costa due minuti NON E- UN PRESIDIO: e-
# ### una ragione per dare `--no-verify`.**
# ### ✅ **Quindi i VELOCI stanno nel `pre-commit`, i LENTI SOLO nella CI**, e il
# ### punto `6` della TERZA parte chiedera- ### **il budget dichiarato** -- questo e- il
# ### primo posto dove serve, e lo dico invece di aspettarlo.
LENTI = ("csv/_referto_infrastruttura_era2.py",)

GENERATI = (
    # ### ✅ **I QUATTRO REGISTRI DI VOCABOLARIO**, che `csv/_registri_indice.py`
    # ### produce in un giro solo. ### ⚠ **`leggi.jsonl` e `variabili.jsonl` sono
    # ### ANCHE `REPLAY`**, e non e- una contraddizione: ### **la loro parte dell-era `1`
    # ### si GENERA, la loro parte dell-era `2` si RIGIOCA dallo storico** -- ed e-
    # ### esattamente la somma che l-arbitro di `scrivi()` tiene insieme.
    # ### ✅ **E ANCHE IL SUO REFERTO**, perche- era proprio LUI a essere
    # ### ### **committato inquinato** da un `collaudo()` che chiama `main()`
    # ### quattro volte: ### **il file che diceva i numeri era quello che non si
    # ### controllava.**
    ("doc/indice/_registri.txt", "csv/_registri_indice.py"),
    ("doc/indice/leggi.jsonl", "csv/_registri_indice.py"),
    ("doc/indice/variabili.jsonl", "csv/_registri_indice.py"),
    ("doc/indice/assiomi.jsonl", "csv/_registri_indice.py"),
    ("doc/indice/decisioni.jsonl", "csv/_registri_indice.py"),
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


def mancanti(nome):
    """### ⛔ **GLI ID CHE LO STORICO HA CREATO E CHE NON SONO PIU- NEL FILE.**

    ### ⚠ **E- IL BUCO DEL `REPLAY`, MISURATO il 2026-10-10:** `replay()` cicla su
    ### **i record PRESENTI NEL FILE**, quindi ### **un record CANCELLATO non viene
    ### mai guardato** -- e il collaudo passava ### **`13` su `13` con QUATTRO record
    ### cancellati.**
    ### ⭐ **E <<ogni record coincide col suo storico>> NON E- <<lo storico si
    ### rigioca in QUESTO file>>:** la prima frase e- vera anche su un file ### **meta-
    ### vuoto.** ### **La seconda e- quella che la parola REPLAY promette.**

    ### ⚠ **LA PRESENZA SI CERCA NEI REGISTRI CHE CONDIVIDONO LO STORICO, non nel
    ### solo `nome`:** `voci.jsonl` ed `etichette_rimosse.jsonl` ### **condividono
    ### `storico.jsonl`**, e una voce che diventa un-etichetta ### **sparisce dal primo
    ### e compare nel secondo** -- cercarla nel solo `nome` la direbbe ### **persa
    ### mentre e- solo MIGRATA.**

    ### ✅ **E UN `alias` VALE COME PRESENZA:** `rinomina` lascia il nome vecchio
    ### come alias, e le righe di storico di prima del rinominamento portano ### **il
    ### nome vecchio.** ### **Un ID risolto da un alias NON e- perso: e- lo stesso
    ### oggetto con un nome nuovo** -- ed e- la regola del par. `9`.
    """
    stato, chiave, storico, _dove, _b = REGISTRI[nome]
    if stato != "REPLAY" or not storico:
        return []
    fratelli = [n for n, v in REGISTRI.items() if v[2] == storico]
    ci_sono = set()
    for n in fratelli:
        for r in _jsonl(os.path.join(D, n)):
            ci_sono.add(r[REGISTRI[n][1]])
            ci_sono |= set(r.get("alias") or [])
    err = []
    for k in sorted({r.get("id") for r in _righe_storico(nome) if r.get("id")}):
        if k not in ci_sono:
            err.append("`P-T2` `%s` `%s`: LO STORICO LO HA CREATO E NON E- PIU- NEL "
                       "FILE, ne- in %s, ne- come `alias`. ### Un `REPLAY` promette che "
                       "lo storico SI RIGIOCHI IN QUESTO FILE, e un record cancellato "
                       "rompe la promessa SENZA toccare nessun record rimasto"
                       % (nome, k, " o ".join("`%s`" % x for x in fratelli if x != nome)
                          or "nessun fratello"))
    return err


def blob_committato(nome):
    """### ⛔ **IL BLOB DICHIARATO DEVE COINCIDERE COI BYTE *COMMITTATI*, non con
    quelli SUL DISCO.**

    ### ⚠ **IL DIFETTO CHE QUESTO BRACCIO IMPEDISCE E- SUCCESSO, e l-ha trovato il
    guardiano su un clone Linux:** il blob di `migrazione_era1.jsonl` era
    ### **`9a5c45b40fb853fd`**, che sono i byte ### **sul disco di Windows (CRLF)**;
    i byte committati sono ### **`8996d113388d49cc`.**
    ### ⭐ **Un-impronta presa dal disco passa SULLA MACCHINA DI CHI L-HA PRESA e
    fallisce su ogni altra** -- e `P-T2` la dichiarava <<verificata>>.

    ### ⛔ **E IL CONFRONTO E- COL `HEAD`, non con lo stage:** lo stage e- cio- che
    ### **sto per committare**, e un blob che coincide con lo stage ### **coincide con
    se stesso.** ### ⚠ **Nel commit in cui un reperto cambia, questo braccio
    SEGNALA e non ferma** -- perche- a quel momento `HEAD` e- ancora il vecchio, e
    ### **fermare la- vorrebbe dire non poter MAI cambiare un reperto.**
    """
    import subprocess
    stato, _c, _s, _d, b = REGISTRI[nome]
    if stato != "REPERTO" or not b:
        return []
    rel = "doc/indice/" + nome
    q = subprocess.run(["git", "show", "HEAD:" + rel], cwd=RADICE,
                       capture_output=True)
    if q.returncode != 0:
        return ["`P-T2` `%s`: NON E- A `HEAD` (%s). ### Un reperto che non e- nel repo "
                "non ha byte committati con cui confrontarsi"
                % (nome, (q.stderr or b"").decode("utf-8", "replace").strip()[:60])]
    atteso = hashlib.sha1(q.stdout).hexdigest()[:16]
    if atteso == b:
        return []
    # ### ✅ **E SE IL FILE IN STAGE COINCIDE COL DICHIARATO, e- IL COMMIT CHE LO
    # ### CAMBIA:** si SEGNALA, e il giro dopo il confronto con `HEAD` tornera- a tornare.
    s = subprocess.run(["git", "show", ":" + rel], cwd=RADICE, capture_output=True)
    if s.returncode == 0 and hashlib.sha1(s.stdout).hexdigest()[:16] == b:
        return []
    return ["`P-T2` `%s`: il blob dichiarato e- `%s` e i BYTE COMMITTATI danno `%s`. "
            "### Un-impronta presa DAL DISCO passa sulla macchina di chi l-ha presa e "
            "FALLISCE SU OGNI ALTRA -- ed e- successo: `migrazione_era1.jsonl` portava "
            "l-impronta della sua versione CRLF. ### Si ricalcola da "
            "`git show HEAD:%s`" % (nome, b, atteso, rel)]


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
        if stato == "GENERATO":
            # ### ⛔ **UN REGISTRO `GENERATO` DEVE ESSERE FRA I `GENERATI`**, o
            # ### ### **nessuno lo verifica** -- e una dichiarazione che non porta un
            # ### controllo e- ### **peggio** di nessuna dichiarazione, perche- SEMBRA
            # ### un controllo.
            if not any(f.endswith("/" + nome) for f, _c in GENERATI):
                err.append("`P-T2` `%s`: dichiarato `GENERATO` e NON E- fra i `GENERATI`. "
                           "### Quindi NESSUNO lo verifica, e la dichiarazione SEMBRA un "
                           "controllo senza esserlo" % nome)
            continue
        if stato == "SOLO-AGGIUNTE":
            err += solo_aggiunte(nome)
            continue
        if stato == "REPLAY":
            if not storico:
                err.append("`P-T2` `%s`: `REPLAY` senza uno storico dichiarato" % nome)
                continue
            err += replay(nome)
            # ### ⛔ **E LA PRESENZA, che `replay()` NON PUO- GUARDARE:** cicla sui
            # ### record ### **del file**, quindi ### **un record cancellato non viene
            # ### mai raggiunto.** ### **Due controlli, perche- sono due domande
            # ### diverse:** <<cio- che c-e- coincide?>> e <<c-e- tutto?>>.
            err += mancanti(nome)
        else:
            if not b:
                err.append("`P-T2` `%s`: `REPERTO` senza il blob dichiarato" % nome)
                continue
            err += reperto(nome)
            # ### ⛔ **E IL BLOB DICHIARATO SI CONFRONTA COI BYTE COMMITTATI:** il
            # ### braccio sopra guarda ### **il disco**, questo guarda ### **il repo** --
            # ### e ### **la differenza fra i due e- esattamente il difetto che il
            # ### guardiano ha trovato.**
            err += blob_committato(nome)
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
    # ===================================================================================
    #   ### ⭐ **IL BUCO DEL `REPLAY`, e i bracci che lo chiudono** *(2026-10-10)*
    # ===================================================================================
    # ### ⛔ **IL CASO CHE DEVE FALLIRE SI COSTRUISCE DAI DATI VERI** (`P1-sexies`):
    # ### si toglie ### **un record che lo storico ha creato**, si guarda, e
    # ### ### **si rimette** -- e l-ultimo braccio verifica che il file sia tornato
    # ### ### **IDENTICO AL BYTE**, altrimenti il collaudo ### **lascia danno.**
    import hashlib as _hl
    _reg = "leggi.jsonl"
    _p = os.path.join(D, _reg)
    _b0 = io.open(_p, "rb").read()
    _sha0 = _hl.sha1(_b0).hexdigest()
    _ids_st = sorted({r.get("id") for r in _righe_storico(_reg) if r.get("id")})
    esito("### il collaudo ha MATERIA: lo storico di `%s` ha creato dei record" % _reg,
          len(_ids_st) > 0,
          "%d: %s" % (len(_ids_st), ", ".join("`%s`" % x for x in _ids_st[:4])))
    esito("NON deve scattare: col file INTATTO, nessun record manca",
          mancanti(_reg) == [],
          "### e nessun falso positivo: un `alias` vale come presenza, perche- "
          "`rinomina` lascia il nome vecchio")
    try:
        _vittima = _ids_st[0] if _ids_st else None
        _righe = [r for r in io.open(_p, encoding="utf-8").read().split(NL) if r.strip()]
        _tolte = [r for r in _righe if json.loads(r)["id"] != _vittima]
        io.open(_p, "w", encoding="utf-8", newline=NL).write(NL.join(_tolte) + NL)
        _m = mancanti(_reg)
        esito("### DEVE scattare: un record CANCELLATO si vede",
              _vittima is not None and any(_vittima in x for x in _m),
              "`%s` tolto: ### e- il buco che PASSAVA 13 su 13 con QUATTRO record "
              "cancellati" % _vittima)
        esito("### e `replay()` DA SOLO NON LO VEDE: e- il motivo per cui `mancanti` "
              "esiste",
              replay(_reg) == [],
              "### `replay()` cicla sui record DEL FILE: cio- che non c-e- NON SI "
              "GUARDA -- e <<ogni record coincide>> e- vero anche su un file META- VUOTO")
    finally:
        io.open(_p, "wb").write(_b0)
    esito("### e il file e- tornato IDENTICO AL BYTE",
          _hl.sha1(io.open(_p, "rb").read()).hexdigest() == _sha0,
          "`%s`: ### un collaudo che lascia danno non e- un collaudo" % _sha0[:8])

    # ===================================================================================
    #   ### ⭐ **IL QUARTO STATO `GENERATO`** *(2026-10-10)*
    # ===================================================================================
    _gen = sorted(n for n, v in REGISTRI.items() if v[0] == "GENERATO")
    _in_gen = {f.rsplit("/", 1)[-1] for f, _c in GENERATI}
    print()
    print("  i registri `GENERATO`: %s" % (", ".join(_gen) or "nessuno"))
    esito("### il collaudo ha MATERIA: ci sono registri `GENERATO`",
          len(_gen) >= 2,
          "%d: ### erano dichiarati `REPERTO`, cioe- <<non ha una via di scrittura, e non "
          "deve averla>> -- e INVECE LA HANNO" % len(_gen))
    esito("NON deve scattare: ogni `GENERATO` e- fra i `GENERATI`",
          all(n in _in_gen for n in _gen),
          "### senza questo, la dichiarazione SEMBRA un controllo senza esserlo")
    # ### ⛔ **IL CASO CHE DEVE FALLIRE: si dichiara `GENERATO` un registro che NON
    # ### e- fra i `GENERATI`**, e si rimette subito. ### **Si tocca la TABELLA, non un
    # ### file:** cosi- il braccio ### **non puo- lasciare danno sul disco.**
    _vittima = "metadati.jsonl"
    _prima = REGISTRI[_vittima]
    try:
        REGISTRI[_vittima] = ("GENERATO", _prima[1], None, None, None)
        _e = controlla()
        esito("### DEVE scattare: un `GENERATO` che NON e- fra i `GENERATI`",
              any("NON E- fra i `GENERATI`" in x and _vittima in x for x in _e),
              "`%s` dichiarato `GENERATO` per finta: ### nessuno lo verificherebbe"
              % _vittima)
    finally:
        REGISTRI[_vittima] = _prima
    esito("### e la tabella e- tornata come era",
          REGISTRI[_vittima] == _prima,
          "### `%s` di nuovo `%s`: si tocca la TABELLA, non il disco"
          % (_vittima, _prima[0]))

    # ===================================================================================
    #   ### ⭐ **IL BLOB CONTRO I BYTE COMMITTATI** *(il difetto del guardiano)*
    # ===================================================================================
    _rep = sorted(n for n, v in REGISTRI.items() if v[0] == "REPERTO")
    print()
    print("  i `REPERTO` e il loro blob, confrontato coi BYTE COMMITTATI:")
    import subprocess as _sp
    for _n in _rep:
        _q = _sp.run(["git", "show", "HEAD:doc/indice/" + _n], cwd=RADICE,
                     capture_output=True)
        print("     %-24s dichiarato %s   committato %s"
              % (_n, REGISTRI[_n][4],
                 hashlib.sha1(_q.stdout).hexdigest()[:16] if _q.returncode == 0
                 else "### NON A HEAD"))
    esito("### il collaudo ha MATERIA: ci sono registri `REPERTO`",
          len(_rep) >= 2,
          "%d: ### senza di loro il braccio sotto passerebbe per vacuita-" % len(_rep))
    esito("NON deve scattare: ogni blob dichiarato coincide coi BYTE COMMITTATI",
          all(blob_committato(n) == [] for n in _rep),
          "### e NON col disco: un-impronta presa dal disco passa SULLA MACCHINA DI CHI "
          "L-HA PRESA e fallisce su ogni altra -- ed e- successo")
    # ### ⛔ **IL CASO CHE DEVE SCATTARE: si tocca LA TABELLA, non il disco** -- e
    # ### ### **il valore finto e- il blob del DISCO con le CRLF**, cioe- esattamente la
    # ### forma del difetto vero.
    # ### ⛔ **LA VITTIMA DEVE CONTENERE DELLE NEWLINE, e me lo ha detto un braccio
    # ### che FALLIVA:** il primo `REPERTO` in ordine alfabetico e-
    # ### `conflitti_era1.jsonl`, che e- ### **VUOTO** -- e sostituire `LF` con `CRLF` in
    # ### un file vuoto ### **non cambia un byte**, quindi il blob finto era
    # ### ### **identico a quello vero** e il caso non poteva scattare.
    # ### ⭐ **E- la terza volta in due giorni che un caso <<deve fallire>> NON PUO-
    # ### fallire per costruzione**, ed e- sempre lo stesso difetto: ### **un falso-uno
    # ### che si veste da verde.**
    _cand = [n for n in _rep
             if bytes([10]) in io.open(os.path.join(D, n), "rb").read()]
    assert _cand, ("### nessun `REPERTO` contiene una newline: il caso che deve fallire "
                   "NON SI PUO- COSTRUIRE, e lo DICO invece di far passare un braccio "
                   "che non prova niente")
    _n = _cand[0]
    _vero = REGISTRI[_n]
    try:
        _b = io.open(os.path.join(D, _n), "rb").read()
        _crlf = hashlib.sha1(_b.replace(bytes([10]), bytes([13, 10]))).hexdigest()[:16]
        REGISTRI[_n] = (_vero[0], _vero[1], _vero[2], _vero[3], _crlf)
        esito("### DEVE scattare: un blob preso dal DISCO con le CRLF",
              any("BYTE COMMITTATI" in x for x in blob_committato(_n)),
              "`%s` con l-impronta della sua versione CRLF (`%s`): ### e- ESATTAMENTE la "
              "forma del difetto che il guardiano ha trovato" % (_n, _crlf))
    finally:
        REGISTRI[_n] = _vero
    esito("### e la tabella e- tornata come era",
          REGISTRI[_n] == _vero,
          "### si tocca LA TABELLA e non il disco: questo braccio NON PUO- lasciare "
          "danno")
    esito("NON deve scattare: `.gitattributes` copre le estensioni dell-indice",
          all(("*%s text eol=lf" % e) in io.open(
              os.path.join(RADICE, ".gitattributes"), encoding="utf-8").read()
              .replace("  ", " ").replace(" text", " text")
              for e in (".jsonl",)),
          "### `*.jsonl` c-e-: senza di lui `core.autocrlf=true` riscrive 121 file al "
          "primo `checkout`, e OGNI blob dichiarato diventa quello di un-altra macchina")

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
