# -*- coding: utf-8 -*-
"""LA MIGRAZIONE DELL'INDICE ALLO SCHEMA `2` — **RIESEGUIBILE e IDEMPOTENTE**.

### ⛔ **DA DOVE PARTE:** l'indice ### **al tag `era-1-secondo-ordine`** *(`13` colonne, gli
stati ORIGINALI)* piu' le ### **due colonne aggiunte su `primo-ordine`** *(`9f23313`)*.
### ➜ **Non parte dal file corrente**, perche' quello ha gia' i `629` `SOSPESA-ERA-1` fatti
### **per parole chiave** — cioe' l'errore che questa migrazione ### **bonifica**.

### ⭐ **IDEMPOTENTE:** due esecuzioni ### **danno gli stessi byte.** Nessuna data di oggi,
nessun ordine casuale: le righe si ordinano per `id`, e `creata`/`aggiornata` portano la
### **data della migrazione dichiarata**, non `today()`.

Gira con:  python csv/migra_indice_v2.py [--collaudo]
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
import indice as IX                                          # noqa: E402

# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Migra un indice.
NL = chr(10)
TAB = chr(9)
D = os.path.join(RADICE, "doc", "indice")
TAG = "era-1-secondo-ordine"
DATA = "2026-10-08"            # ### la data DICHIARATA della migrazione, non `today()`
P = []

# ==========================================================================
#   LA TAVOLA DI CORRISPONDENZA `tipo` -> `classe`  (doc/INDICE_SCHEMA.md `⑥`)
# ==========================================================================
CLASSE_DA_TIPO = {
    "difetto": "DIFETTO", "sospetto": "DIFETTO", "cura": "CURA", "misura": "MISURA",
    "criterio-locale": "CRITERIO", "presidio": "PRESIDIO", "standard": "STANDARD",
    "assioma": "STANDARD", "fronte": "FRONTE", "altro": "DIFETTO",
}
# ### `altro` NON e' un'informazione: la classe si mette, ma il DOMINIO resta DA_CLASSIFICARE.
TIPI_SENZA_DOMINIO = ("altro",)

# ==========================================================================
#   LE LISTE DEL GUARDIANO, applicate ESPLICITAMENTE
# ==========================================================================
# ### ⚠ **LA SCELTA FRA `METODO` E `INFRASTRUTTURA` E' MIA, e il motivo e' accanto a ciascuna.**
# ### LA REGOLA CHE HO USATO:
# ###   `METODO`          = come si RAGIONA e come si MISURA (un falso zero, una finestra che
# ###                       non prova niente, una regola di lavoro, una soglia senza pavimento)
# ###   `INFRASTRUTTURA`  = gli STRUMENTI e i FILE (un sigillo, un presidio, un inventario, una
# ###                       corsa, una piattaforma, il formato di un documento)
L1 = {
    "MASSA-ID": ("INFRASTRUTTURA", "l'identita' di una massa negli strumenti"),
    "PASSO-1": ("METODO", "che cosa conta come <<un passo>> in una misura"),
    "PASSO-PIENO": ("METODO", "net.step() non e' un passo: e' una regola di misura"),
    "PRESTAZIONI-CORSE": ("INFRASTRUTTURA", "i tempi delle corse"),
    "VIDEO-SCENA": ("INFRASTRUTTURA", "il rendering"),
    "ESENTE-P3": ("METODO", "quando P3 non si applica: e' una regola di lavoro"),
    "D26": ("METODO", "una lezione su come si legge un confronto"),
    "FALSO-UNO": ("METODO", "la lezione del falso uno"),
    "FALSO-ZERO": ("METODO", "la lezione del falso zero"),
    "INVENTARIO-SIGILLI-SENZA-COMMIT": ("INFRASTRUTTURA", "l'inventario e i blob"),
    "PRESIDIO-RIFIUTO-SOLO-SIGILLI": ("INFRASTRUTTURA", "la portata di un presidio"),
    "VELENO-DOMINI": ("METODO", "la sonda del veleno e i domini"),
    "FINESTRA-PRE-NASCITA": ("METODO", "una finestra che non prova niente"),
    "LINGUAGGIO-REGOLE": ("METODO", "come si scrivono le regole"),
    "LUNGHEZZA-COME-SEGNALE": ("METODO", "la lunghezza di un documento come segnale"),
    "NON-TRACCIATI": ("INFRASTRUTTURA", "i file non tracciati"),
    "SIGILLO-COMPARATORE-DUPLICATO": ("INFRASTRUTTURA", "un sigillo"),
    "SIGILLO-SENZA-CONFIGURAZIONE": ("INFRASTRUTTURA", "un sigillo"),
    "H-ETC-2": ("INFRASTRUTTURA", "un hook"),
    "P1": ("METODO", "una regola di lavoro"),
    "P2": ("METODO", "una regola di lavoro"),
    "P3": ("METODO", "una regola di lavoro"),
    "P4": ("METODO", "una regola di lavoro"),
    "P5": ("METODO", "una regola di lavoro"),
    "P6": ("METODO", "una regola di lavoro"),
    "Q6": ("METODO", "una lezione di metodo"),
    "R3": ("METODO", "una lezione di metodo"),
    "R5": ("METODO", "una lezione di metodo"),
    "STATI-LOCALI": ("INFRASTRUTTURA", "lo stato locale di uno strumento"),
    "U3": ("METODO", "una lezione di metodo"),
    "CENS-B16": ("METODO", "un censimento di dichiarazioni"),
    "ROBUSTEZZA-FISICA": ("METODO", "il gradino di robustezza: un criterio di misura"),
    "TAGLIA-FINITA": ("METODO", "la taglia finita come limite di una misura"),
    "CLI-1": ("INFRASTRUTTURA", "il percorso CLI dei sigilli -- MANTIENE blocca"),
    "C21": ("INFRASTRUTTURA", "uno strumento"),
    "D13": ("METODO", "una lezione di metodo"),
    "D12": ("METODO", "una lezione di metodo"),
    "Z89": ("METODO", "una lezione di metodo"),
    "Z15": ("METODO", "una lezione di metodo"),
    "Z125": ("METODO", "una lezione di metodo"),
    "Z142": ("METODO", "una lezione di metodo"),
    "PAT-1": ("METODO", "un pattern di prova"),
    "PAT-2": ("METODO", "un pattern di prova"),
    "REG-R": ("INFRASTRUTTURA", "il presidio del registro"),
    "REG-V": ("INFRASTRUTTURA", "il presidio del registro"),
    "ANCORE-1": ("INFRASTRUTTURA", "le ancore nei patch"),
    "CONFIG-1": ("INFRASTRUTTURA", "il referto di configurazione"),
    "REPERTI-IMMUTABILI": ("METODO", "i reperti non si riscrivono: una regola"),
    "RIPRESA-ARGV": ("INFRASTRUTTURA", "l'argv alla ripresa"),
    "COLLAUDO-NON-ESEGUITO": ("INFRASTRUTTURA", "un collaudo che non gira"),
    "CONTA-RIGHE": ("INFRASTRUTTURA", "wc -l e i newline finali"),
    "PIATTAFORMA-NON-TIMBRATA": ("INFRASTRUTTURA", "la piattaforma non timbrata"),
    "FUGA-MULTIRIGA": ("INFRASTRUTTURA", "l'escape multiriga negli script"),
    "H-REGR-LARGA": ("INFRASTRUTTURA", "un hook troppo largo"),
    "RELAZIONE-BINARIA": ("INFRASTRUTTURA", "il formato della relazione"),
    "INDICE-LEGGERO": ("INFRASTRUTTURA", "il formato dell'indice"),
    "FATTI-AVVIO": ("INFRASTRUTTURA", "i fatti letti all'avvio"),
    "SIGILLO-REGISTRO-NON-CONFRONTABILE": ("INFRASTRUTTURA", "un sigillo"),
    "CELLE-NAN-APPESE-NOME-SCADUTO": ("INFRASTRUTTURA", "un nome scaduto in uno strumento"),
    "SYNCDB-HEADLESS": ("INFRASTRUTTURA", "l'ambiente di corsa"),
    "ARCHI-PRIMI": ("INFRASTRUTTURA", "l'ordine degli archi negli strumenti"),
    "IMPL-2": ("INFRASTRUTTURA", "un dettaglio d'implementazione"),
}
L2 = ("FRECCE-IMPOSTE MEMORIE-MANCANTI M-FLUSSO M-LEGAMI MEM-VERSO "
      "TETTO-CAUSALE-TEMPO-COORDINATO DIVISIONE-AUTOCONSISTENTE ENERGIA-NON-DEFINITA "
      "GRAVITA-POTENZIALE REVERSIBILITA-LOCALE VUOTO-LOCALE-DETERMINISTICO "
      "CARICA-SIMMETRIA-FASE LOSCHMIDT-ECO D03 CONSERVAZIONE-LOCALE CARICA-PERCORSO "
      "CARICA-DI-GAUGE CARICA-ROTAZIONE SCHWINGER-UN-NODO D15 D35 D38 SCHW-SOTTO-LAM "
      "M-SPINORE M-MASSA M-ISTERESI MODELLO-MINIMO A3-DISEGNO G1 Z104 G4-MEMARCO M1 "
      "FASCE-TAU GEOMETRIA-DELLA-CRESCITA LORENTZ-MATERIA-INTERFERENZA "
      "EM-CURVATURA-BIDIREZIONALE Y1 RISCRITTURA-GO FASE-TRASCINAMENTO-3D "
      "MEM-HEBB-PIANO-XY INVARIANZA-LOCALE-CS AUDIT-CURE MASSE-PESI-SOVRAPPOSTE").split()
L3 = ("A1-COSTANTI CLIP-INVENTARIO W5 COMPONENTI:B11 COMPONENTI:C3 COMPONENTI:S3 "
      "REGISTRO_FISICA:A4 REGISTRO_FISICA:A5 REGISTRO_FISICA:A6 REGISTRO_FISICA:E3 "
      "REGISTRO_FISICA:U2-6 REGISTRO_FISICA:V6 DOPPIA-COP POTATURA-GUARDIE SCHED-PASSO "
      "ARCHI-OLTRE-4PI CENS-A1 CENS-A3 CENS-A6 CS-LAMBDA-GLOBALE MCRIT-RICALCOLO "
      "MEM-HEBB-VERSO MITOSI-2LAM-ACCESO PEQ-SEL-STANTIO PHI0-CONGELATA "
      "PRE-RILASSAMENTO-FUORI-PASSO REG-A REGIME-DUE-SISTEMI SCHERMATURA-LEGGE-REVISIONE "
      "SMP-APRI-COMMENTO Z43 GUSCIO-ANTIFASE-EMERGENTE SCHW-CORTI TERMOSTATO-E-FRENO "
      "H-ETC-1 CENS-B1 CENS-B8 GEOM-SENZA-VERSO SCIOGLIMENTO-FASE SPINORE-SENZA-FASE "
      "CENS-A2 CENS-A7 CENS-B7 D31 SCALE-TW U1").split()
NOTE_SUPERATA = {
    "DOPPIA-COP": "candidata SUPERATA da A16", "CENS-A1": "candidata SUPERATA da A16",
    "SPINORE-SENZA-FASE": "candidata SUPERATA da A16",
    "CENS-A6": "candidata SUPERATA dalla decisione sulla sincronizzazione",
    "MCRIT-RICALCOLO": "candidata SUPERATA dalla decisione (A): la soglia e' il bilancio",
    "U1": "candidata SUPERATA dalla decisione (A): la soglia e' il bilancio",
    "REG-A": "candidata SUPERATA dal censimento di doc/TRADUZIONE_IN_H.md",
    "TERMOSTATO-E-FRENO": "candidata SUPERATA da A16",
    "SCIOGLIMENTO-FASE": "candidata SUPERATA: spiegata da D2-D2-TER",
    "PHI0-CONGELATA": "candidata SUPERATA: trasportata via M-LEGAMI",
}
RE_SEGNAPOSTO = re.compile(r"^\(CITATO \d+ volte, MAI definito in un registro")
# ### I FILE CHE LA MIGRAZIONE STESSA GENERA: non sono prove, sono il suo output.
GENERATI = ("doc/INDICE_ID.tsv", "doc/INDICE.md", "doc/REFERTO_indice_v2.md")
# ### I FILE in cui una citazione NON fa di un ID una voce: messaggi, task history, referti.
SOLO_DOCUMENTO = ("doc/TASK_HISTORY/", "doc/REFERTO_", "doc/STORIA_REGOLE.md",
                  "doc/RELAZIONE", "RELAZIONE_PER_CLAUDE.md", "doc/RIPRESA_",
                  "doc/relazioni/", "doc/LISTA_CHIUSA.md", "doc/STATO_RUN.md",
                  "doc/INDICE", "doc/PASSAGGIO_", "doc/PUNTO_", "doc/CENSIMENTO_",
                  ".github/", "CLAUDE.md", "doc/REGOLE/")


def stampa(s=""):
    P.append(s)
    print(s, flush=True)


def riga(c="-", n=104):
    stampa(c * n)


# ==========================================================================
def vecchio_indice():
    """### L'indice AL TAG (`13` colonne, stati ORIGINALI) piu' le DUE colonne di `9f23313`."""
    t = subprocess.run(["git", "show", "%s:doc/INDICE_ID.tsv" % TAG], cwd=RADICE,
                       capture_output=True, text=True, encoding="utf-8")
    assert t.returncode == 0, "il tag %s non si legge" % TAG
    r = [x for x in t.stdout.split(NL) if x.strip()]
    testa = r[0].split(TAB)
    assert len(testa) == 13, "al tag le colonne sono %d, non 13" % len(testa)
    vv = {}
    for x in r[1:]:
        c = x.split(TAB)
        c += [""] * (13 - len(c))
        v = dict(zip(testa, c))
        vv[v["id"]] = v
    # ### le due colonne aggiunte su `primo-ordine`: si leggono da git, non dal disco,
    # ### perche' il disco verra' SOVRASCRITTO dalla vista.
    t2 = subprocess.run(["git", "show", "9f23313:doc/INDICE_ID.tsv"], cwd=RADICE,
                        capture_output=True, text=True, encoding="utf-8")
    assert t2.returncode == 0, "il commit 9f23313 non si legge"
    r2 = [x for x in t2.stdout.split(NL) if x.strip()]
    testa2 = r2[0].split(TAB)
    for x in r2[1:]:
        c = x.split(TAB)
        c += [""] * (len(testa2) - len(c))
        v2 = dict(zip(testa2, c))
        if v2["id"] in vv:
            vv[v2["id"]]["_stato_era_1"] = v2.get("stato_era_1", "") or v2["stato"]
            vv[v2["id"]]["_si_riferisce_a"] = v2.get("si_riferisce_a", "")
    return vv


def dichiarati_etichetta():
    """### Gli ID dichiarati ### **<<etichetta, non ID>>** in una nota `[SENZA-INDICE: …]`
    di un messaggio di commit. ### ⛔ **E' la dichiarazione che Luca ha chiesto di usare**, e
    i messaggi sono l'unico posto in cui vive."""
    t = subprocess.run(["git", "log", "--all", "--format=%B"], cwd=RADICE,
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace").stdout
    fuori = set()
    for m in re.finditer(r"\[SENZA-INDICE:([^\]]{0,4000})\]", t):
        for w in re.findall(r"(?<![A-Za-z0-9_:-])([A-Z][A-Z0-9:_-]{1,40})"
                            r"(?![A-Za-z0-9_:-])", m.group(1)):
            fuori.add(w)
    return fuori


def conta_citazioni(ids):
    """### Quante volte un ID e' citato, e DOVE: la prova su cui si decide un segnaposto."""
    per = {i: [] for i in ids}
    pat = re.compile(r"(?<![A-Z0-9_:-])(" + "|".join(
        sorted((re.escape(i) for i in ids), key=len, reverse=True)) + r")(?![A-Z0-9_:-])")
    for rad, dirs, files in os.walk(RADICE):
        dirs[:] = [x for x in dirs if x not in (".git", "__pycache__", "_archivio")]
        for f in files:
            if not f.endswith((".md", ".py", ".txt")):
                continue
            rel = os.path.relpath(os.path.join(rad, f), RADICE).replace(chr(92), "/")
            # ### ⛔ **I FILE GENERATI SI ESCLUDONO, e il controllo `C4` me l'ha preso:**
            # ### la seconda esecuzione trovava gli ID citati in ### **`doc/INDICE.md`**,
            # ### che la PRIMA aveva generato -- quindi `file_citanti` cambiava e i
            # ### segnaposto prendevano una strada diversa. ### **La migrazione non era
            # ### idempotente perche' LEGGEVA UNA VISTA CHE LEI STESSA SCRIVE.**
            if rel.startswith("doc/indice/") or rel in GENERATI:
                continue
            try:
                t = io.open(os.path.join(rad, f), encoding="utf-8", errors="replace").read()
            except Exception:                                  # noqa: BLE001
                continue
            for m in set(pat.findall(t)):
                per[m].append(rel)
    return {k: sorted(set(v)) for k, v in per.items()}


def voce_nuova(**kw):
    v = {"id": "", "alias": [], "titolo": "", "descrizione": "", "classe": "DIFETTO",
         "dominio": "DA_CLASSIFICARE", "era": "DA_CLASSIFICARE",
         "stato": "DA_CLASSIFICARE", "blocca": False, "leggi": [], "variabili": [],
         "assiomi": [], "collegate": [], "padre": "", "superata_da": "", "chiusura": {},
         "fonte": "", "creata": {"data": DATA, "commit": ""},
         "aggiornata": {"data": DATA, "commit": ""}, "stato_era_1": "", "meta": {}}
    v.update(kw)
    return {k: v[k] for k in IX.CHIAVI}


STATO_DA_ERA1 = {"chiuso": "CHIUSA", "non-difetto": "CHIUSA", "teoria": "APERTA",
                 "aperto": "APERTA", "da-decidere": "APERTA", "SOSPESA-ERA-1": "APERTA"}


def main(argv):
    solo_collaudo = "--collaudo" in argv
    os.makedirs(D, exist_ok=True)
    vecchie = vecchio_indice()
    riga("=")
    stampa("LA MIGRAZIONE DELL'INDICE ALLO SCHEMA 2 -- dal tag %s" % TAG)
    riga("=")
    stampa("  voci al tag: %d" % len(vecchie))

    _v, reg = IX.carica()
    segnaposto = [i for i, v in vecchie.items() if RE_SEGNAPOSTO.match(v["titolo_breve"])]
    stampa("  SEGNAPOSTO <<(CITATO N volte, MAI definito in un registro)>>: %d"
           % len(segnaposto))
    cit = conta_citazioni(set(segnaposto))

    # ### ⛔ **UN TERZO DIFETTO DELL'INDICE VECCHIO: 11 ID CONTENGONO UNO SPAZIO**
    # ### *(`STANDARD 6`, `STANDARD ⑤`)*. Sono ### **voci VERE** -- gli standard
    # ### numerati del metodo -- ma un ID con uno spazio non e' usabile. ### ➜ **Si
    # ### normalizza, e IL NOME VECCHIO RESTA COME ALIAS:** e' esattamente il
    # ### meccanismo che `CLAUDE.md` par.9 prescrive *(<<i reperti non si riscrivono:
    # ### il nome vecchio resta, e si risolve con l'alias>>)*. ### **I numerali
    # ### cerchiati si traslitterano**, perche' la regex vuole ASCII.
    CERCHIATI = dict(zip('①②③④⑤⑥⑦⑧⑨⑩', [str(k + 1) for k in range(10)]))

    def id_usabile(i):
        for k, v in CERCHIATI.items():
            i = i.replace(k, v)
        return re.sub(r"\s+", "-", i.strip())

    voci, etichette, tracce, conflitti = [], [], [], []
    normali = {i: v for i, v in vecchie.items() if i not in segnaposto}

    # ---------------------------------------------- (a) i CAMPI MECCANICI
    for i, v in sorted(normali.items()):
        tipo = v["tipo"]
        classe = CLASSE_DA_TIPO.get(tipo, "DIFETTO")
        s1 = v.get("_stato_era_1") or v["stato"]
        meta = {}
        # ### ⛔ **`motivo` e `revisione` ERANO PERSI, e il validatore della vista me
        # ### l'ha preso:** `motivo` e' ### **la PROVA che giustifica `blocca SI`**, e
        # ### `_indice_id.py` la pretende. ### **Niente testo si perde** e' una regola del
        # ### mandato, e la stavo violando su due colonne.
        for k, c in (("tipo_era1", "tipo"), ("famiglia_era1", "famiglia"),
                     ("avanzamento_era1", "avanzamento"),
                     ("motivo_era1", "motivo"), ("revisione_era1", "revisione")):
            if v.get(c):
                meta[k] = v[c]
        if v.get("_si_riferisce_a") and v["_si_riferisce_a"] != "(non trovato)":
            meta["si_riferisce_a_era1"] = v["_si_riferisce_a"][:200]
        # ### i RIFERIMENTI solo se il valore vecchio COINCIDE con un ID dei registri
        leggi = [x for x in [v.get("_si_riferisce_a", "")] if x in reg["leggi"]]
        varia = [("V-" + x.upper().replace("_", "-")) for x in
                 (v.get("_si_riferisce_a") or "").split(",")
                 if ("V-" + x.upper().replace("_", "-")) in reg["variabili"]]
        nuovo_id = id_usabile(i)
        alias0 = [x for x in (v["alias"] or "").split(",") if x and x != i]
        if nuovo_id != i:
            alias0.append(i)          # ### IL NOME VECCHIO RESTA
            tracce.append({"id_vecchio": i, "dove": "voci.jsonl::alias di %s" % nuovo_id,
                           "regola": "(a3) l'ID conteneva uno SPAZIO: normalizzato, e il "
                                     "nome vecchio RESTA come alias"})
        voci.append(voce_nuova(
            id=nuovo_id, alias=alias0,
            titolo=v["titolo_breve"][:100], descrizione=v["stato_da"],
            classe=("TEORIA" if s1 == "teoria" else classe),
            blocca=(v["blocca_run_base"] == "SI"),
            fonte=v["fonte_principale"] or ("doc/STATO_RUN.md::%s" % i),
            stato_era_1=s1, meta=meta, leggi=leggi, variabili=sorted(set(varia)),
            dominio=("DA_CLASSIFICARE" if tipo in TIPI_SENZA_DOMINIO else
                     ("METODO" if classe in ("PRESIDIO", "STANDARD") else
                      "DA_CLASSIFICARE")),
            era=("ENTRAMBE" if classe in ("PRESIDIO", "STANDARD") else "DA_CLASSIFICARE"),
            stato=("CHIUSA" if s1 in ("chiuso", "non-difetto") else
                   ("APERTA" if classe in ("PRESIDIO", "STANDARD") else
                    "DA_CLASSIFICARE")),
            chiusura=({"criterio": "chiusa nell'era 1 (stato `%s` al tag %s)" % (s1, TAG),
                       "commit": TAG, "data": DATA}
                      if s1 in ("chiuso", "non-difetto") else {})))
        if nuovo_id == i:
            tracce.append({"id_vecchio": i, "dove": "voci.jsonl::id",
                           "regola": "(a) meccanica"})

    per_id = {v["id"]: v for v in voci}

    # ### ⛔ **UN DIFETTO DELL'INDICE VECCHIO, che la migrazione fa emergere:** la colonna
    # ### `alias` conteneva cose che ### **NON sono alias**. ### `21` di esse sono
    # ### ### **ID DI ALTRE VOCI** *(`A1-COSTANTI` aveva alias `A1`, e `A1` e' una voce)*, e
    # ### ### `6` erano ### **condivise fra due voci**. ### ➜ **Un alias e' un ALTRO NOME
    # ### DELLA STESSA COSA:** se punta a una voce diversa e' un ### **COLLEGAMENTO**, e se
    # ### due voci lo rivendicano ### **non e' un alias di nessuna.**
    tutti_ids = set(per_id)
    quante = {}
    for v in voci:
        for a in v["alias"]:
            quante[a] = quante.get(a, 0) + 1
    n_coll = n_tolti = 0
    for v in voci:
        tieni = []
        for a in v["alias"]:
            if a in tutti_ids:
                if a not in v["collegate"]:
                    v["collegate"].append(a)
                n_coll += 1
                tracce.append({"id_vecchio": v["id"], "dove": "collegate",
                               "regola": "(a2) l'alias `%s` E' UNA VOCE: e' un "
                                         "collegamento, non un alias" % a})
            elif quante[a] > 1:
                n_tolti += 1
                tracce.append({"id_vecchio": v["id"], "dove": "alias tolto",
                               "regola": "(a2) l'alias `%s` era rivendicato da %d voci: "
                                         "non e' un alias" % (a, quante[a])})
            else:
                tieni.append(a)
        v["alias"] = sorted(set(tieni))
        v["collegate"] = sorted(set(v["collegate"]))
    stampa("  ALIAS DELL'ERA 1 BONIFICATI: %d diventati COLLEGAMENTI (erano ID di voci), "
           "%d tolti (condivisi fra piu' voci)" % (n_coll, n_tolti))

    # ---------------------------------------------- (b) i SEGNAPOSTO
    def norm(s):
        return s.upper().replace("_", "-")
    noti = {}
    for v in voci:
        noti[norm(v["id"])] = v["id"]
        for a in v["alias"]:
            noti[norm(a)] = v["id"]
    # ### GLI ID DI VOCABOLARIO: un assioma, una legge, una variabile, una decisione NON
    # ### sono voci dell'indice. Un segnaposto che coincide con uno di loro e' un ID di
    # ### REGISTRO citato nei documenti, non un difetto.
    vocab = set()
    for k in ("leggi", "variabili", "assiomi", "decisioni"):
        vocab |= set(reg[k])
    dich = dichiarati_etichetta()
    stampa("  ID dichiarati <<etichetta, non ID>> in una nota [SENZA-INDICE]: %d"
           % len(dich))
    n_alias = n_etic = n_dc = n_voc = n_dich = 0
    for i in sorted(segnaposto):
        vv = vecchie[i]
        files = cit.get(i, [])
        # ### REGOLA (b0): e' un ID DI VOCABOLARIO
        if i in vocab or norm(i) in vocab:
            etichette.append({"id": i, "citazioni_n": len(files),
                              "file_citanti": files[:12],
                              "regola": "(b0) e' un ID di VOCABOLARIO, non una voce",
                              "titolo_era1": vv["titolo_breve"][:100]})
            tracce.append({"id_vecchio": i, "dove": "etichette_rimosse.jsonl",
                           "regola": "(b0) ID di vocabolario"})
            n_voc += 1
            continue
        # ### REGOLA 1: coincide, normalizzato, con un id o un alias di una voce VERA
        bersaglio = noti.get(norm(i))
        if bersaglio and bersaglio != i:
            per_id[bersaglio]["alias"] = sorted(set(per_id[bersaglio]["alias"] + [i]))
            tracce.append({"id_vecchio": i, "dove": "voci.jsonl::alias di %s" % bersaglio,
                           "regola": "(b1) coincide normalizzato"})
            n_alias += 1
            continue
        # ### REGOLA 2: TUTTE le citazioni in messaggi, task history o referti
        solo_doc = files and all(any(f.startswith(x) for x in SOLO_DOCUMENTO)
                                 for f in files)
        if i in dich:
            n_dich += 1
        if solo_doc or not files or i in dich:
            etichette.append({"id": i, "citazioni_n": len(files), "file_citanti": files,
                              "regola": ("(b2) DICHIARATA etichetta in una nota "
                                         "[SENZA-INDICE]" if i in dich else
                                         "(b2) tutte le citazioni sono in documenti"),
                              "titolo_era1": vv["titolo_breve"][:100]})
            tracce.append({"id_vecchio": i, "dove": "etichette_rimosse.jsonl",
                           "regola": "(b2) etichetta di documento"})
            n_etic += 1
            continue
        # ### REGOLA 3: resta come voce DA_CLASSIFICARE
        ni = id_usabile(i)
        # ### ⛔ **E DUE ID VECCHI POSSONO NORMALIZZARSI NELLO STESSO:** `STANDARD 5` e
        # ### `STANDARD ⑤` sono ### **lo stesso standard scritto in due modi.** ### ➜ **Il
        # ### secondo diventa ALIAS del primo**, e non si perde niente.
        if ni in per_id:
            per_id[ni]["alias"] = sorted(set(per_id[ni]["alias"] + [i]))
            tracce.append({"id_vecchio": i, "dove": "voci.jsonl::alias di %s" % ni,
                           "regola": "(a4) normalizzato COINCIDE con `%s`: e' lo stesso "
                                     "oggetto scritto in due modi" % ni})
            n_alias += 1
            continue
        al = [i] if ni != i else []
        if al:
            tracce.append({"id_vecchio": i, "dove": "voci.jsonl::alias di %s" % ni,
                           "regola": "(a3) l'ID conteneva uno SPAZIO: normalizzato, e il "
                                     "nome vecchio RESTA come alias"})
        voci.append(voce_nuova(id=ni, alias=al, titolo=vv["titolo_breve"][:100],
                               descrizione=vv["stato_da"], classe="DIFETTO",
                               fonte="doc/STATO_RUN.md::%s" % i,
                               stato_era_1=vv.get("_stato_era_1") or vv["stato"],
                               meta={"citazioni_n": len(files),
                                     "file_citanti": files[:12]}))
        per_id[ni] = voci[-1]
        if not al:
            tracce.append({"id_vecchio": i, "dove": "voci.jsonl::id",
                           "regola": "(b3) resta DA_CLASSIFICARE"})
        n_dc += 1
    stampa("      -> ID di VOCABOLARIO (regola b0): %d" % n_voc)
    stampa("      -> alias di una voce vera: %d" % n_alias)
    stampa("      -> di cui DICHIARATI etichetta in una nota [SENZA-INDICE]: %d" % n_dich)
    stampa("      -> etichette di documento (fuori da voci.jsonl): %d" % n_etic)
    stampa("      -> restano DA_CLASSIFICARE: %d" % n_dc)

    # ---------------------------------------------- (c) LE LISTE DEL GUARDIANO
    def applica(idv, **kw):
        v = per_id.get(idv)
        if v is None:
            conflitti.append({"id": idv, "motivo": "NON ESISTE nell'indice del tag"})
            return None
        v.update(kw)
        return v

    # ### ⛔ **E IL CONTROLLO `C3` MI HA PRESO UN DIFETTO D'ORDINE:** la passata
    # ### strutturale `(e)` sulle `TEORIA` girava ### **DOPO** le liste e le
    # ### ### **SOVRASCRIVEVA** -- `REVERSIBILITA-LOCALE` e `GEOMETRIA-DELLA-CRESCITA`
    # ### hanno `stato_era_1 = teoria`, quindi diventavano `TEORIA` ed `era
    # ### DA_CLASSIFICARE` invece di restare `AGENDA`/`2` come la lista dice.
    # ### ➜ **Le voci che una lista ha deciso si MARCANO, e la passata strutturale le
    # ### SALTA.** ### **Una decisione dichiarata batte un'inferenza, sempre.**
    decise = set()
    n_l1 = n_l2 = n_l3 = 0
    for idv, (dom, perche) in sorted(L1.items()):
        v = applica(idv, dominio=dom, era="ENTRAMBE")
        if v:
            v["stato"] = STATO_DA_ERA1.get(v["stato_era_1"], "APERTA")
            v["meta"]["nota_guardiano"] = ("lista 1 del guardiano: %s -- %s" % (dom, perche))
            decise.add(v["id"])
            if v["stato"] == "CHIUSA" and not v["chiusura"]:
                v["chiusura"] = {"criterio": "chiusa nell'era 1", "commit": TAG,
                                 "data": DATA}
            n_l1 += 1
    for idv in L2:
        v = applica(idv, dominio="FISICA", era="2", stato="AGENDA")
        if v:
            v["meta"]["nota_guardiano"] = "lista 2 del guardiano: programma dell'era 2"
            decise.add(v["id"])
            if idv == "LOSCHMIDT-ECO":
                v["meta"]["nota_guardiano"] += " -- anche metodo"
            v["chiusura"] = {}
            n_l2 += 1
    for idv in L3:
        v = applica(idv, dominio="FISICA", era="1", stato="SOSPESA")
        if v:
            if not v["stato_era_1"]:
                v["stato_era_1"] = "aperto"
            nota = "lista 3 del guardiano: fisica dell'era 1, sospesa"
            if idv in NOTE_SUPERATA:
                nota += " -- " + NOTE_SUPERATA[idv]
            v["meta"]["nota_guardiano"] = nota
            decise.add(v["id"])
            v["chiusura"] = {}
            n_l3 += 1
    stampa("  LISTE DEL GUARDIANO applicate: L1 %d/%d, L2 %d/%d, L3 %d/%d"
           % (n_l1, len(L1), n_l2, len(L2), n_l3, len(L3)))
    if conflitti:
        stampa("      ### CONFLITTI (ID non trovati): %d -- %s"
               % (len(conflitti), " ".join(x["id"] for x in conflitti[:10])))

    # ---------------------------------------------- (d) e (e) il resto, STRUTTURALE
    n_pad = n_dc2 = n_teo = 0
    for v in voci:
        if v["id"] in decise:
            continue                  # ### una LISTA l'ha decisa: non si tocca
        if v["classe"] == "TEORIA":
            v["dominio"] = "FISICA" if v["dominio"] == "DA_CLASSIFICARE" else v["dominio"]
            v["era"] = "DA_CLASSIFICARE"
            v["stato"] = STATO_DA_ERA1.get(v["stato_era_1"], "APERTA")
            v["meta"].setdefault("nota_guardiano", "classe TEORIA: da leggere al triage")
            n_teo += 1
            continue
        if v["stato"] != "DA_CLASSIFICARE":
            continue
        # ### un CRITERIO con un padre eredita dominio ed era del padre
        if v["classe"] == "CRITERIO" and v["padre"] and v["padre"] in per_id:
            p = per_id[v["padre"]]
            v["dominio"], v["era"] = p["dominio"], p["era"]
            v["stato"] = p["stato"] if p["stato"] != "DA_CLASSIFICARE" else "DA_CLASSIFICARE"
            n_pad += 1
            continue
        n_dc2 += 1
    stampa("  STRUTTURALE: TEORIA %d, criteri con padre %d, restano DA_CLASSIFICARE %d"
           % (n_teo, n_pad, n_dc2))

    # ### coerenza finale: dominio DA_CLASSIFICARE deve avere stato o era DA_CLASSIFICARE
    for v in voci:
        if v["dominio"] == "DA_CLASSIFICARE" and v["stato"] != "DA_CLASSIFICARE" \
                and v["era"] != "DA_CLASSIFICARE":
            v["era"] = "DA_CLASSIFICARE"
        if v["stato"] != "SOSPESA":
            pass
        if v["stato"] == "SOSPESA" and not v["stato_era_1"]:
            v["stato_era_1"] = "aperto"
        if v["stato"] != "CHIUSA":
            v["chiusura"] = {}
        if v["stato"] != "SUPERATA":
            v["superata_da"] = ""
        if v["blocca"] and v["stato"] in ("CHIUSA", "SUPERATA"):
            v["stato"] = "APERTA"
            v["chiusura"] = {}

    if solo_collaudo:
        stampa()
        stampa("  --collaudo: NON HO SCRITTO NIENTE.")
        return 0

    IX._scrivi_jsonl(IX.VOCI, voci)
    IX._scrivi_jsonl(os.path.join(D, "etichette_rimosse.jsonl"), etichette)
    io.open(os.path.join(D, "migrazione_era1.jsonl"), "w", encoding="utf-8",
            newline=NL).write(NL.join(json.dumps(x, ensure_ascii=False)
                                      for x in sorted(tracce,
                                                      key=lambda y: y["id_vecchio"])) + NL)
    io.open(os.path.join(D, "conflitti_era1.jsonl"), "w", encoding="utf-8",
            newline=NL).write(NL.join(json.dumps(x, ensure_ascii=False)
                                      for x in conflitti) + (NL if conflitti else ""))
    voci2, reg2 = IX.carica()
    IX.viste(voci2, reg2)
    stampa()
    stampa("  scritti voci.jsonl (%d), etichette_rimosse.jsonl (%d), migrazione_era1.jsonl "
           "(%d), conflitti_era1.jsonl (%d)"
           % (len(voci), len(etichette), len(tracce), len(conflitti)))
    io.open(os.path.join(D, "_migrazione.txt"), "w", encoding="utf-8",
            newline=NL).write(NL.join(P) + NL)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
