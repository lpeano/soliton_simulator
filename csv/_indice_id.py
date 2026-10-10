r"""**IL VALIDATORE DELL'INDICE** — `doc/INDICE_ID.tsv` e' la **FONTE**, e questo la CONTROLLA.

**Ultimo passo del refactoring (Luca, 2026-09-26):** *«l'indice diventa la FONTE, non una vista»*.

> ## ⛔ **QUESTO FILE NON GENERA PIU' NIENTE.**
> L'importatore che leggeva il Markdown e ricostruiva l'indice **ha girato per l'ultima volta** ed e'
> in **`csv/_archivio/_indice_id_importatore.py`**: sta li' come **storia**, e **non si rilancia**
> *(rilanciarlo sovrascriverebbe la fonte con una ricostruzione, cioe' butterebbe via le decisioni
> scritte nelle colonne)*.

## COSA CONTROLLA

```
SCHEMA        l'intestazione e' esattamente quella attesa, e ogni riga ha lo stesso numero di campi
VOCABOLARI    `stato`, `blocca_run_base`, `tipo`, `famiglia`, `avanzamento` stanno nei valori ammessi
ID            unici, non vuoti, e nella FORMA degli ID
COERENZA      un `chiuso`/`non-difetto`/`teoria`/`criterio-locale` **non blocca mai**
NESSUNA PERDITA  ogni voce presente al tag `lista-chiusa-v1` c'e' ancora, salvo le cancellazioni
                 DICHIARATE qui sotto col motivo
MOTIVO        ogni voce con `blocca = SI` porta il suo `motivo`: una decisione senza prova non passa
```

## DA ORA IN POI

- **un difetto nuovo si scrive come RIGA di `doc/INDICE_ID.tsv`**; la spiegazione lunga sta in
  `doc/STATO_RUN.md` **con lo stesso ID**;
- **il hook rifiuta un ID nuovo in un documento vivo che non ha la sua riga** *(gia' attivo:
  `csv/_presidio_indice.py`, stadio `commit-msg`)*;
- **le viste si rigenerano e non si modificano a mano:** `csv/_lista_chiusa.py`,
  `csv/_vista_smistamento.py`, `csv/_punto_della_situazione.py`.

**`--collaudo`** prova i DUE versi: l'indice vero passa, una copia guasta **fallisce**.
"""
# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Valida un TSV.
import io
import os
import re
import subprocess
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _QUI)
import _presidio

RADICE = os.path.abspath(os.path.join(_QUI, ".."))
FONTE = os.path.join(RADICE, "doc", "INDICE_ID.tsv")
REFERTO = os.path.join(RADICE, "doc", "INDICE_ID_validazione.txt")
TAG = "lista-chiusa-v1"
NL = chr(10)
TAB = chr(9)

# ### ⚠ **DAL 2026-10-08 LE COLONNE SONO `15`, NON `13`** *(la chiusura dell'era `1`)*: la
# ### sospensione richiede di ### **conservare lo stato originale** (`stato_era_1`) e di dire
# ### ### **a quale legge o variabile la voce si riferisce** (`si_riferisce_a`).
# ### ⛔ **E `CLAUDE.md` par.9 dice ancora «un TSV di 13 colonne»:** quella riga va aggiornata,
# ### ### **ed e' una decisione di Luca** -- `CLAUDE.md` e' il flusso di lavoro, non uno
# ### strumento, e non lo tocco da solo.
COL = ["id", "alias", "titolo_breve", "fonte_principale", "stato", "blocca_run_base", "tipo",
       "famiglia", "stato_da", "avanzamento", "revisione", "motivo", "nota",
       "stato_era_1", "si_riferisce_a"]
# ### ⭐ **`SOSPESA-ERA-1` dal 2026-10-08** *(decisione di Luca: la chiusura dell'era `1`)*:
# ### una voce sospesa ### **NON e' chiusa** -- il difetto c'e' ancora, ma riguarda una legge
# ### che la riscrittura al primo ordine potrebbe ### **togliere, tradurre o lasciare intatta**,
# ### e il triage si fa ### **a riscrittura finita** *(`doc/TRIAGE_ERA_1.md`)*.
# ### ⛔ **E NON sta fra gli stati che contraddicono `blocca_run_base = SI`:** una bloccante
# ### sospesa ### **resta bloccante**, perche' blocca le corse dell'era `1`.
# ### ⛔ **DAL 2026-10-08 QUESTO FILE VALIDA UNA *VISTA*, NON LA FONTE** *(schema `2`)*: la
# ### fonte e' `doc/indice/voci.jsonl` e il validatore vero e' ### **`csv/indice.py valida`**,
# ### agganciato al `pre-commit`. ### **Questo resta perche' `--blocca SI`, `--cerca` e
# ### `--dettaglio` sono comandi che si usano**, e la vista li fa funzionare senza riscriverli.
# ### ➜ **Gli stati dello schema `2` si aggiungono al vocabolario**; quelli dell'era `1`
# ### restano, perche' la colonna `stato_era_1` li porta ancora.
STATI = {"aperto", "chiuso", "non-difetto", "teoria", "da-decidere", "SOSPESA-ERA-1",
         "APERTA", "IN_CORSO", "CHIUSA", "SOSPESA", "SUPERATA", "AGENDA",
         "DA_CLASSIFICARE"}
BLOCCA = {"SI", "NO", "DA-DECIDERE", "DA VERIFICARE"}
# ### ⚠ **E `non_definita` SI AGGIUNGE AL VOCABOLARIO DELLA VISTA** *(schema `3`)*: la
# ### colonna `tipo` della vista porta la ### **classe** quando il metadato `tipo_era1` non
# ### c'e', e un segnaposto non ha un `tipo` dell'era `1`.
# ### ⚠ **E `decisione` E- ARRIVATO IL 2026-10-10**, perche- il vocabolario `CLASSI`
# ### dello schema `v3` lo ammette ### **da sempre** *(`DECISIONE`)* e questa vista
# ### ### **era rimasta indietro**: le prime due voci di quella classe hanno fatto
# ### fallire il `pre-commit` con *<<tipo `decisione` non ammesso>>*.
# ### ⛔ **NON l-ho aggirato scegliendo un-altra classe:** una domanda a Luca E- una
# ### `DECISIONE`, e ### **piegare il dato per far tacere una vista vecchia sarebbe il
# ### difetto peggiore** -- la vista esiste per RAPPRESENTARE il dato, non il contrario.
# ### ⚠ **`criterio` E- ENTRATO IL `2026-10-10`, e il motivo e- preciso:** la
# ### vista compatibile scrive `meta.tipo_era1` ### **se c-e-**, e altrimenti
# ### ### **`classe.lower()`**. ### **Le 97 voci `CRITERIO` di prima portavano
# ### TUTTE un `tipo_era1`** *(94 su 97: `criterio-locale`)*, quindi la parola
# ### `criterio` ### **non era mai arrivata qui.** ### ⛔ **Le prime DUE
# ### voci `CRITERIO` dell-era 2 non hanno un tipo dell-era 1 -- e metterglielo
# ### SAREBBE UNA BUGIA**, perche- `tipo_era1` dice *<<che cosa era nell-era 1>>*
# ### e queste ### **nell-era 1 non c-erano.**
TIPI = {"difetto", "sospetto", "fronte", "misura", "cura", "presidio", "assioma",
        "standard", "criterio", "criterio-locale", "decisione", "teoria",
        "altro",
        "non_definita"}
FAM = {"A", "B", "C", "D", "E", "F", "G", "?"}
TITOLO_MAX = 100     # [INDICE-LEGGERO] un titolo breve dev'essere breve: la stampa e' UNA riga
AVANZ = {"FATTO", "IN CORSO", "IN CODA", "BLOCCATO", "CON RISERVA", "(senza marcatore)"}
FORMA = re.compile(r"(?:[A-Z]\d{1,3}[a-z]?|STANDARD\s+[0-9①-⑳]+"
                   r"|[A-Z][A-Z0-9]*(?:-[A-Za-z0-9()/]+)+|[A-Z]{2,}\d{1,3}"
                   r"|[A-Z_]+:[A-Za-z0-9\-()/]+)")

#   ⚠ LO STEM DI UNA LETTERA, ammesso il 2026-09-26: `H-P3` e `L-SOGLIA` hanno UNA
#   lettera prima del trattino -- e `H-P1-bis` ha una CODA MINUSCOLA, come il
#   `P1-bis` che tutti citano -- e la forma chiedeva DUE lettere e tutto maiuscolo -- quindi il validatore
#   RIFIUTAVA i nomi che Luca stesso aveva dettato. Misurato: senza questa riga sedici
#   voci nuove su sedici erano 'senza FORMA'.
#   ⚠ LE CANCELLAZIONI DICHIARATE: una voce sparita rispetto al tag e' un ERRORE, salvo queste.
CANCELLAZIONI = {
    "CLI-1)": "token SPURIO: la parentesi della prosa attaccata all'id "
              "*(`(CLI-1)` letto come un nome)*. Curato il 2026-09-26: le parentesi devono essere "
              "BILANCIATE.",
}


def leggi(percorso):
    r = io.open(percorso, encoding="utf-8", newline="").read().split(NL)
    return [c.strip() for c in r[0].split(TAB)], [x for x in r[1:] if x.strip()]


def valida(percorso):
    """`(errori, quante_voci)`. Un errore e' una stringa leggibile: nessun `assert` muto."""
    err = []
    titoli = {}          # titolo_breve -> id, per la regola di UNICITA'
    col, righe = leggi(percorso)
    if col != COL:
        err.append("SCHEMA: intestazione diversa da quella attesa.%s     attesa: %s%s     trovata: %s"
                   % (NL, TAB.join(COL), NL, TAB.join(col)))
        return err, 0
    visti = {}
    for k, x in enumerate(righe, 2):
        c = x.split(TAB)
        if len(c) != len(COL):
            err.append("riga %d: %d campi invece di %d" % (k, len(c), len(COL)))
            continue
        v = dict(zip(COL, [y.strip() for y in c]))
        i = v["id"]
        if not i:
            err.append("riga %d: `id` VUOTO" % k)
            continue
        if i in visti:
            err.append("riga %d: id `%s` DUPLICATO (gia' alla riga %d)" % (k, i, visti[i]))
        visti[i] = k
        if not FORMA.fullmatch(i):
            err.append("riga %d: l'id `%s` non ha la FORMA di un id" % (k, i))
        if v["stato"] not in STATI:
            err.append("riga %d (`%s`): stato `%s` non ammesso" % (k, i, v["stato"]))
        if v["blocca_run_base"] not in BLOCCA:
            err.append("riga %d (`%s`): blocca_run_base `%s` non ammesso"
                       % (k, i, v["blocca_run_base"]))
        if v["tipo"] not in TIPI:
            err.append("riga %d (`%s`): tipo `%s` non ammesso" % (k, i, v["tipo"]))
        if v["famiglia"] not in FAM:
            err.append("riga %d (`%s`): famiglia `%s` non ammessa" % (k, i, v["famiglia"]))
        if v["avanzamento"] not in AVANZ:
            err.append("riga %d (`%s`): avanzamento `%s` non ammesso" % (k, i, v["avanzamento"]))
        # COERENZA: chi e' chiuso, teoria o locale NON blocca
        if v["blocca_run_base"] == "SI" and (v["stato"] in ("chiuso", "non-difetto", "teoria")
                                            or v["tipo"] in ("assioma", "standard",
                                                             "criterio-locale")):
            err.append("riga %d (`%s`): blocca SI ma stato `%s` / tipo `%s`: contraddizione"
                       % (k, i, v["stato"], v["tipo"]))
        # una decisione SENZA PROVA non passa
        if v["blocca_run_base"] == "SI" and not v["motivo"]:
            err.append("riga %d (`%s`): blocca SI **senza `motivo`**: una decisione senza prova"
                       % (k, i))
        # [INDICE-LEGGERO, 2026-09-27] IL TITOLO BREVE DEV'ESSERE BREVE, E UNICO.
        #   Breve, perche' l'indice si INTERROGA e la stampa e' una riga: un titolo da 141
        #   caratteri (il massimo misurato) la fa a pezzi. La frase intera vive in `stato_da`.
        #   Unico, perche' due voci diverse con lo stesso nome sono la collisione che l'indice
        #   esiste per curare -- ed e' successo: `A3` era tre cose.
        if len(v["titolo_breve"]) > TITOLO_MAX:
            err.append("riga %d (`%s`): titolo_breve di %d caratteri, il tetto e' %d. "
                       "Si accorcia (csv/_titoli_brevi.py) e la frase intera va in `stato_da`."
                       % (k, i, len(v["titolo_breve"]), TITOLO_MAX))
        tb = v["titolo_breve"].strip()
        if tb:
            if tb in titoli:
                err.append("riga %d (`%s`): titolo_breve IDENTICO a quello di `%s`: due voci "
                           "diverse con lo stesso nome sono una collisione." % (k, i, titoli[tb]))
            else:
                titoli[tb] = i
    return err, len(visti)


def perdite():
    """Le voci presenti al tag e assenti adesso, tolte quelle DICHIARATE."""
    q = subprocess.run(["git", "show", "%s:doc/INDICE_ID.tsv" % TAG], cwd=RADICE,
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    if q.returncode:
        return None, "il tag `%s` non si legge: %s" % (TAG, (q.stderr or "").strip()[:80])
    al_tag = set(x.split(TAB)[0].strip() for x in (q.stdout or "").split(NL)[1:] if x.strip())
    _c, righe = leggi(FONTE)
    ora = set(x.split(TAB)[0].strip() for x in righe)
    # ### ⛔ **DALLO SCHEMA 2 UN ID PUO' NON ESSERE PIU' UN `id` E NON ESSERE PERSO:** puo'
    # ### essere un ### **ALIAS** *(il nome vecchio di una voce normalizzata)* oppure
    # ### un'### **ETICHETTA RIMOSSA** *(un ID citato nei documenti che non era una voce)*.
    # ### ➜ **Il controllo impara i due posti**, altrimenti grida <<perse>> su `89` ID che
    # ### la migrazione ha ### **conservato e tracciato** *(`doc/indice/migrazione_era1.jsonl`)*.
    for x in righe:
        c2 = x.split(TAB)
        if len(c2) > 1:
            ora |= set(a2.strip() for a2 in c2[1].split(",") if a2.strip())
    _et = os.path.join(RADICE, "doc", "indice", "etichette_rimosse.jsonl")
    if os.path.exists(_et):
        import json as _json
        for _r in io.open(_et, encoding="utf-8"):
            if _r.strip():
                ora.add(_json.loads(_r)["id"])
    return sorted((al_tag - ora) - set(CANCELLAZIONI)), None


def voci(percorso=None):
    """`[dict]` di tutte le voci, nell'ordine del file. Testo COMPLETO, mai troncato."""
    c, righe = leggi(percorso or FONTE)
    fuori = []
    for r in righe:
        v = r.split(TAB)
        while len(v) < len(COL):
            v.append("")
        fuori.append(dict(zip(COL, v)))
    return fuori


def _riga_corta(v, largh=80):
    """UNA riga: id, stato, blocca, famiglia, titolo TAGLIATO A `largh`.

    ⚠ **IL TAGLIO E' SOLO DI VISUALIZZAZIONE, MAI DI CONFRONTO** (mandato di Luca, 2026-09-27):
    chi cerca guarda il testo INTERO, e solo la stampa e' corta. Confrontare sul troncato
    significherebbe non trovare cio' che sta oltre l'ottantesimo carattere.
    """
    tb = v["titolo_breve"]
    return "%-16s %-12s %-12s %-3s %s" % (v["id"], v["stato"], v["blocca_run_base"],
                                          v["famiglia"], tb[:largh])


def interroga(a, percorso=None):
    """I comandi di interrogazione. Restituisce `0` se ha risposto, `None` se non tocca a lui."""
    vv = voci(percorso)

    def elenca(sel, cosa):
        print("=" * 96)
        print("INDICE -- %s: %d voci su %d" % (cosa, len(sel), len(vv)))
        print("%-16s %-12s %-12s %-3s %s" % ("id", "stato", "blocca", "fam", "titolo (tagliato a 80)"))
        print("-" * 96)
        for v in sel:
            print(_riga_corta(v))
        print("-" * 96)
        print("  il DETTAGLIO di una voce:  python csv/_indice_id.py --dettaglio <ID>")
        return 0

    if "--cerca" in a:
        # ⚠ UGUAGLIANZA ESATTA SULL'ID INTERO, MAI un prefisso: `D02` non deve trovare `D021`
        #   ne' `D02-X`. E' la regola che Luca ha dettato, e il collaudo la prova nei due versi.
        chiave = a[a.index("--cerca") + 1]
        sel = [v for v in vv if v["id"] == chiave or chiave in
               [x for x in v["alias"].split(",") if x]]
        if not sel:
            print("nessuna voce con id (o alias) ESATTAMENTE `%s`." % chiave)
            simili = [v["id"] for v in vv if chiave in v["id"] and v["id"] != chiave]
            if simili:
                print("  ⚠ ci sono id che lo CONTENGONO, e NON sono lui: %s"
                      % ", ".join(simili[:12]))
            return 0
        return elenca(sel, "id esattamente `%s`" % chiave)
    if "--dettaglio" in a:
        chiave = a[a.index("--dettaglio") + 1]
        sel = [v for v in vv if v["id"] == chiave]
        if not sel:
            print("nessuna voce con id ESATTAMENTE `%s`." % chiave)
            return 0
        v = sel[0]
        print("=" * 96)
        print("DETTAGLIO di `%s`" % v["id"])
        print("=" * 96)
        for k in COL:
            if v[k].strip():
                print("  %-18s %s" % (k, v[k]))
        return 0
    if "--aperti" in a:
        return elenca([v for v in vv if v["stato"] == "aperto"], "stato `aperto`")
    if "--blocca" in a:
        q = a[a.index("--blocca") + 1]
        return elenca([v for v in vv if v["blocca_run_base"] == q], "blocca_run_base `%s`" % q)
    if "--famiglia" in a:
        q = a[a.index("--famiglia") + 1]
        return elenca([v for v in vv if v["famiglia"] == q], "famiglia `%s`" % q)
    if "--testo" in a:
        # la ricerca e' sul testo COMPLETO di TUTTE le colonne. Solo la STAMPA e' troncata.
        q = a[a.index("--testo") + 1].lower()
        sel = [v for v in vv if any(q in v[k].lower() for k in COL)]
        return elenca(sel, "testo `%s` in QUALUNQUE colonna (ricerca sul testo COMPLETO)" % q)
    return None


def collaudo():
    """I DUE versi: l'indice vero PASSA, una copia GUASTA fallisce."""
    R = []

    def P(s=""):
        R.append(s)
        print(s)

    P("=" * 96)
    P("COLLAUDO DEL VALIDATORE -- i DUE versi   (2026-09-26)")
    P("=" * 96)
    P()
    e, n = valida(FONTE)
    ok1 = not e
    P("  DEVE PASSARE  l'indice VERO (%d voci) -> %s" % (n, "PASS" if ok1 else "FAIL"))
    for x in e[:6]:
        P("      %s" % x)
    casi = [
        ("uno stato inventato", 4, "verde"),
        ("un tipo inventato", 6, "cosa"),
        ("una famiglia inventata", 7, "Z"),
        ("un `blocca SI` su una voce CHIUSA", 5, "SI"),
    ]
    esiti = [ok1]
    _c, righe = leggi(FONTE)
    tmp = os.path.join(RADICE, "doc", "_indice_guasto.tmp")
    for nome, campo, valore in casi:
        # si guasta UNA riga, e si sceglie una riga `chiuso` per il caso della contraddizione
        idx = 0
        if valore == "SI":
            idx = next((j for j, x in enumerate(righe) if x.split(TAB)[4] == "chiuso"), 0)
        c = righe[idx].split(TAB)
        c[campo] = valore
        guaste = list(righe)
        guaste[idx] = TAB.join(c)
        io.open(tmp, "w", encoding="utf-8", newline=NL).write(
            TAB.join(COL) + NL + NL.join(guaste) + NL)
        e2, _ = valida(tmp)
        os.remove(tmp)
        ok = bool(e2)
        esiti.append(ok)
        P("  DEVE FALLIRE  %-36s -> %s" % (nome, "RIFIUTA: " + e2[0][:52] if ok else "*** PASSA ***"))
    # ---------------------------------------------------- [INDICE-LEGGERO] i quattro casi
    P()
    P("  INDICE-LEGGERO (2026-09-27) -- i quattro casi, nei DUE versi")
    # (1) `--cerca` e' UGUAGLIANZA: `D02` non deve trovare `D021`
    OLTRE = ("parolachiavelontana")
    finte = [TAB.join(["D02", "", "il difetto vero", "x", "aperto", "NO", "difetto", "F",
                       "", "(senza marcatore)", "", "", ""]),
             TAB.join(["D021", "", "un ID SINTETICO che CONTIENE D02", "x", "aperto", "NO",
                       "difetto", "F", "", "(senza marcatore)", "", "", ""]),
             TAB.join(["D02-X", "", "un altro che lo contiene col trattino", "x", "aperto", "NO",
                       "difetto", "F", "", "(senza marcatore)", "", "", ""]),
             TAB.join(["LUNGA", "", "un titolo di prova", "x", "aperto", "NO", "difetto", "F",
                       "", "(senza marcatore)", "",
                       "a" * 95 + " " + OLTRE, ""])]
    tmp2 = os.path.join(RADICE, "doc", "_indice_finto.tmp")
    io.open(tmp2, "w", encoding="utf-8", newline=NL).write(
        TAB.join(COL) + NL + NL.join(finte) + NL)
    vv = voci(tmp2)
    trovati = [v["id"] for v in vv if v["id"] == "D02"]
    ok_c1 = (trovati == ["D02"])
    P("  DEVE TROVARE SOLO `D02`   cercando `D02` fra D02/D021/D02-X -> %s   %s"
      % (trovati, "OK" if ok_c1 else "*** SBAGLIATO ***"))
    esiti.append(ok_c1)
    # (2) una parola OLTRE l'ottantesimo carattere: `--testo` la TROVA
    v_l = [v for v in vv if v["id"] == "LUNGA"][0]
    posizione = v_l["motivo"].lower().find(OLTRE)
    trova = [v["id"] for v in vv if any(OLTRE in v[k].lower() for k in COL)]
    corto = [v["id"] for v in vv if any(OLTRE in v[k][:80].lower() for k in COL)]
    ok_c2 = (trova == ["LUNGA"] and corto == [])
    P("  DEVE TROVARE la parola al carattere %d   sul testo COMPLETO %s, sul TRONCATO %s   %s"
      % (posizione, trova, corto, "OK" if ok_c2 else "*** SBAGLIATO ***"))
    P("      (se il confronto usasse il troncamento, quella parola sarebbe INTROVABILE)")
    esiti.append(ok_c2)
    os.remove(tmp2)
    # (3) due titoli brevi IDENTICI: il validatore RIFIUTA
    c3 = righe[0].split(TAB)
    c4 = righe[1].split(TAB)
    while len(c4) < len(COL):
        c4.append("")
    c4[2] = c3[2]
    g3 = list(righe)
    g3[1] = TAB.join(c4)
    io.open(tmp, "w", encoding="utf-8", newline=NL).write(
        TAB.join(COL) + NL + NL.join(g3) + NL)
    e3, _n3 = valida(tmp)
    os.remove(tmp)
    ok_c3 = any("IDENTICO" in x for x in e3)
    P("  DEVE FALLIRE  due titoli brevi IDENTICI -> %s   %s"
      % ("RIFIUTA" if ok_c3 else "*** PASSA ***", "OK" if ok_c3 else "*** SBAGLIATO ***"))
    esiti.append(ok_c3)
    # (4) un titolo oltre il tetto: il validatore RIFIUTA
    c5 = righe[0].split(TAB)
    while len(c5) < len(COL):
        c5.append("")
    c5[2] = "t" * (TITOLO_MAX + 1)
    g5 = list(righe)
    g5[0] = TAB.join(c5)
    io.open(tmp, "w", encoding="utf-8", newline=NL).write(
        TAB.join(COL) + NL + NL.join(g5) + NL)
    e5, _n5 = valida(tmp)
    os.remove(tmp)
    ok_c4 = any("titolo_breve di %d" % (TITOLO_MAX + 1) in x for x in e5)
    P("  DEVE FALLIRE  un titolo di %d caratteri (tetto %d) -> %s   %s"
      % (TITOLO_MAX + 1, TITOLO_MAX, "RIFIUTA" if ok_c4 else "*** PASSA ***",
         "OK" if ok_c4 else "*** SBAGLIATO ***"))
    esiti.append(ok_c4)

    _p, _err = perdite()
    ok_p = (_p == [])
    esiti.append(ok_p)
    P()
    P("  VOCI PERSE rispetto al tag `%s`: %s   -> %s"
      % (TAG, "nessuna" if ok_p else _p, "PASS" if ok_p else "FAIL"))
    P("    cancellazioni DICHIARATE (%d):" % len(CANCELLAZIONI))
    for k2, m in CANCELLAZIONI.items():
        P("      `%s` -- %s" % (k2, m))
    P()
    tutto = all(esiti)
    P("=" * 96)
    P("ESITO: %s" % ("%d/%d PASS -- il validatore IMPEDISCE, non descrive"
                    % (len(esiti), len(esiti)) if tutto else "FAIL"))
    P("=" * 96)
    P()
    P("COSA QUESTO COLLAUDO *NON* DICE:")
    P("  - **non dice che i CONTENUTI siano giusti**: dice che sono **ben formati e coerenti**. Che")
    P("    `D02` blocchi davvero il run base non lo decide uno schema.")
    P("  - **non controlla il testo di `motivo`**: controlla che **ci sia** dove `blocca = SI`.")
    io.open(REFERTO, "w", encoding="utf-8", newline=NL).write(NL.join(R) + NL)
    return 0 if tutto else 1


if __name__ == "__main__":
    _presidio.avvia(__file__)
    if "--collaudo" in sys.argv:
        sys.exit(collaudo())
    _q = interroga(sys.argv[1:])
    if _q is not None:
        sys.exit(_q)
    e, n = valida(FONTE)
    p, msg = perdite()
    print("VALIDAZIONE di doc/INDICE_ID.tsv -- %d voci, %d colonne" % (n, len(COL)))
    if msg:
        print("  ⚠ %s" % msg)
    if p:
        e = e + ["VOCI PERSE rispetto al tag %s: %s" % (TAG, ", ".join(p))]
    if e:
        print("*** %d VIOLAZIONI:" % len(e))
        for x in e[:40]:
            print("    %s" % x)
        sys.exit(1)
    print("  schema, vocabolari, id, coerenza, motivo, nessuna perdita: **TUTTO A POSTO**")
    print("  (questo file NON genera: l'importatore e' in csv/_archivio/ e non si rilancia)")
    sys.exit(0)
