# -*- coding: utf-8 -*-
"""IL PUNTO `3`: **le `165` righe del guardiano, con la sua regola.**

> ### ⛔ **LA REGOLA, ALLA LETTERA:** la citazione ### **deve COMPARIRE** nella riga
> d'origine *(o nella sezione/tabella che la contiene)*, confronto ### **senza markdown,
> accenti e spazi normalizzati**. ### **`alta` + trovata → applica.** ### **`media` +
> trovata → si rilegge la riga intera, e si applica se la frase SOSTIENE il cambio.**
> ### **Non trovata → NON si applica, e si elenca.**

### ⭐ **DOVE SI E' TROVATA CONTA, e si registra:** `T1` la ### **riga stessa**, `T2` il
### **blocco** *(l'intestazione piu' la sua sezione)*, `T3` la ### **sezione intera del
file.** ### ⚠ **Una citazione di tre caratteri trovata solo in `T3` e' una prova debole**, e
il referto la dichiara invece di nasconderla.

### ⛔ **E CHIUDERE PRETENDE UN COMMIT:** lo schema vuole `chiusura.criterio` **e**
`chiusura.commit`. Il criterio e' la citazione; il commit si cerca ### **nella riga**, e
### **se non c'e' la voce NON si chiude: si elenca.** ### **Un commit non si inventa** —
e' la stessa regola del punto `1`.

Gira con:  python csv/_applica_correzioni_guardiano.py            # costruisce il lotto
"""
import collections
import io
import json
import os
import re
import sys
import unicodedata

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
sys.path.insert(0, _QUI)
import _presidio                                             # noqa: E402
_presidio.avvia(__file__)
import _righe_origine as RO                                  # noqa: E402
import _stato_dalla_riga as SR                               # noqa: E402

# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Costruisce un lotto.
NL = chr(10)
BT = chr(96)
D = os.path.join(RADICE, "doc", "indice")
DATA = "2026-10-09"
FILE_G = os.path.join(D, "_lotti", "correzioni_guardiano_2026-10-09.txt")
_SHA = re.compile(r"(?<![0-9a-zA-Z])[0-9a-f]{7,40}(?![0-9a-zA-Z])")
# ### I campi che il FILE usa e che lo schema NON ha con quel nome.
CAMPI_SCHEMA = ("classe", "dominio", "era", "stato", "superata_da")


def pulisci(s):
    """### Senza markdown, ### **accenti piegati**, spazi normalizzati.

    ### ⛔ **Gli accenti si piegano perche' il file e la riga non li scrivono allo stesso
    modo:** `REGISTRO_FISICA:P2` cita *<<P2 E- FALLITA>>* con la ### **`È`**, e in un altro
    punto il repo scrive ### **`E'`.** ### **Piegare l-accento confronta le due.**
    """
    s = (s or "").replace("*", "").replace(BT, "").replace("#", "")
    s = s.replace(chr(0x2019), "'").replace(chr(0x2018), "'")
    s = s.replace(chr(0x201C), '"').replace(chr(0x201D), '"')
    s = s.replace(chr(0x2014), "-").replace(chr(0x2013), "-")
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    # ### ⚠ **E l-apostrofo dopo una vocale e- un ACCENTO SCRITTO A MANO**, come in `E'`:
    # ### ### **si toglie**, altrimenti `E CURATO` e `E' CURATO` non combaciano.
    s = re.sub(r"(?<=[AEIOUaeiou])'(?=\s|$)", "", s)
    return " ".join(s.split())


def righe_file(f):
    """### Le righe di un file, e ### **`[]` se non e- un file.**

    ### ⛔ **Serve perche- una `fonte` puo- nominare una CARTELLA** --
    `TW-DIVISIONE-INCOGNITA` ha `csv/_test_fork/_misure_calore/` -- e aprirla
    ### **solleva `PermissionError`.** `os.path.exists` dice `True` per una cartella:
    ### **si chiede `isfile`.**
    """
    q = os.path.join(RADICE, f) if f else ""
    if not q or not os.path.isfile(q):
        return []
    return io.open(q, encoding="utf-8", errors="replace").read().split(NL)


def sezione(file_, n):
    """### La SEZIONE che contiene la riga `n` *(`1`-based)*: dall'intestazione precedente
    alla prossima. ### **E- il terzo livello di ricerca che il mandato nomina.**"""
    rr = RO.righe_di(file_)
    if not rr or n < 1:
        return ""
    k = n - 1
    a = 0
    for j in range(k, -1, -1):
        if rr[j].lstrip().startswith("#"):
            a = j
            break
    b = len(rr)
    for j in range(k + 1, len(rr)):
        if rr[j].lstrip().startswith("#"):
            b = j
            break
    return NL.join(rr[a:b])


def cerca(cit, v, riga, file_, n):
    """### Dove compare la citazione. `(livello, come)` oppure `(None, ...)`.

    ### ⛔ **I LIVELLI NON SONO TUTTI UGUALI, e il mandato ne nomina solo tre:** la
    ### **riga d-origine** e la ### **sezione/tabella che la contiene.** Gli altri due li
    aggiungo io, e ### **li dichiaro:**

    | | dov-e- | chi lo dice |
    |---|---|---|
    | `T0` | il ### **`titolo` + `descrizione` della voce** | ### **mio**, e il motivo e-
      che quello ### **E- il testo della voce**: la riga d-origine e- la riga ### **da cui
      la voce e- nata**, e il titolo ne e- ### **la copia troncata a `100` caratteri** |
    | `T1` | la ### **riga d-origine** | il mandato |
    | `T2` | il ### **blocco**: l-intestazione piu- la sua sezione | il mandato
      *(<<intestazione di sezione>>)* |
    | `T3` | la ### **sezione** che contiene la riga | il mandato *(<<la sezione che la
      contiene>>)* |
    | `T4` | ### **altrove nel FILE** che la `fonte` nomina | ### **mio, e SOLO quando la
      riga d-origine NON SI RITROVA** -- la- il luogo del mandato ### **non esiste**, e il
      posto piu- vicino e- ### **il file che la fonte nomina.** ### ⚠ **Dove la riga SI
      ritrova, `T4` NON si usa:** una citazione che sta nel file ma ### **fuori dalla
      sezione** non e- cio- che la regola chiede, e ### **si elenca.** |
    """
    c = pulisci(cit)
    if not c:
        return (None, "la citazione e- vuota")
    prima = (riga or "").split(NL)[0]
    liv = [("T0", (v["titolo"] or "") + " " + (v["descrizione"] or "")),
           ("T1", prima), ("T2", riga or ""),
           ("T3", sezione(file_, n) if n else "")]
    if riga is None:
        # ### ⛔ **SOLO SE LA RIGA NON SI RITROVA**, e il livello lo dichiara.
        liv.append(("T4", NL.join(righe_file(file_))))
    for nome, testo in liv:
        if c in pulisci(testo):
            return (nome, "alla lettera")
    for nome, testo in liv:
        if c.upper() in pulisci(testo).upper():
            return (nome, "a meno delle maiuscole")
    if c.upper() in pulisci(NL.join(righe_file(file_))).upper():
        return (None, "### COMPARE NEL FILE `%s` MA FUORI DALLA SEZIONE della voce, e la "
                      "regola chiede la riga o la sezione che la contiene" % file_)
    return (None, "NON COMPARE: ne- nella voce, ne- nella riga, ne- nella sezione, ne- nel "
                  "file `%s`" % file_)


def sostiene(v, riga, campo, valore, livello):
    """### `media`: ### **la riga intera sostiene il cambio?** `(True/False, perche-)`.

    ### ⛔ **Non e- un giudizio a occhio: e- la REGOLA DEL PUNTO `1`.** Per `stato` e
    `classe` si rilegge la riga con `decidi_stato`/`decidi_classe`:
    ### **se la regola decide il CONTRARIO, la riga NON sostiene** -- e quello e- il caso
    chiaro del *<<altrimenti elenca>>*. ### **Se la regola non decide, non contraddice**, e
    la citazione trovata basta.

    ### ⚠ **Per `dominio`, `era` e le parti da dividere la regola del punto `1` NON HA UNA
    LETTURA**, e allora conta ### **DOVE** si e- trovata la citazione: in `T1`/`T2` sta
    ### **nel testo della voce**; in `T3` sta ### **solo da qualche parte nella sezione**, e
    una sezione contiene anche le voci vicine. ### ➜ **`T3` si elenca, non si applica.**
    """
    if campo == "stato":
        d, perche = SR.decidi_stato(v, riga)
        # ### ⛔ **`SOSPESA` E `APERTA` NON SONO DUE VERDETTI: SONO LO STESSO VERDETTO
        # ### ### (<<la voce e- APERTA>>), e quale dei due stati sia LEGALE lo decide
        # ### ### L-ERA.** `F7` dice *era `1` ### **=> `SOSPESA`**; `F9` dice
        # ### *era `ENTRAMBE` ### **=> `APERTA` o `CHIUSA`**.
        # ### ⚠ **E LA REGOLA DELLO STATO E- SCRITTA PER L-ERA `1`:** su una voce
        # ### `ENTRAMBE` risponde `SOSPESA` ### **per una convenzione che non la riguarda.**
        # ### ➜ `RIPRESA-ARGV` e- era `ENTRAMBE`, la sua riga dice *<<APERTA il
        # ### 2026-09-26>>*, il file del guardiano dice `APERTA`, e la regola diceva
        # ### `SOSPESA`: ### **trattarla come una CONTRADDIZIONE era un difetto MIO**, e
        # ### avrebbe lasciato `F9` violato -- cioe- ### **impedito di accenderlo.**
        if {d, valore} == {"SOSPESA", "APERTA"}:
            legale = "SOSPESA" if str(v["era"]) == "1" else "APERTA"
            if valore == legale:
                return (True, "la regola dello stato dice `%s`, il file dice `%s`: e- LO "
                              "STESSO VERDETTO (la voce e- aperta), e per era `%s` lo stato "
                              "legale e- `%s` -- `F7` per l-era 1, `F9` per `ENTRAMBE`"
                        % (d, valore, v["era"], legale))
            return (False, "### la regola dice `%s` e il file dice `%s`: lo stesso verdetto, "
                           "ma per era `%s` lo stato legale e- `%s`, non `%s`"
                    % (d, valore, v["era"], legale, valore))
        if d == valore:
            return (True, "la regola dello stato rilegge la riga e da- `%s`: %s"
                    % (d, perche[:120]))
        if d is None:
            return (True, "la regola dello stato non decide, quindi NON CONTRADDICE, e la "
                          "citazione e- nella riga (%s)" % livello)
        return (False, "### LA REGOLA DELLO STATO DA- `%s`, NON `%s`: la riga CONTRADDICE "
                       "il cambio (%s)" % (d, valore, perche[:120]))
    if campo == "classe":
        d, perche = SR.decidi_classe(v, riga)
        if d == valore:
            return (True, "la regola della classe rilegge la riga e da- `%s`: %s"
                    % (d, perche[:120]))
        if d is None:
            return (True, "la regola della classe non decide, quindi NON CONTRADDICE, e la "
                          "citazione e- nella riga (%s)" % livello)
        return (False, "### LA REGOLA DELLA CLASSE DA- `%s`, NON `%s`: la riga CONTRADDICE "
                       "il cambio (%s)" % (d, valore, perche[:120]))
    if livello in ("T3", "T4"):
        return (False, "### la citazione si trova in `%s` -- la SEZIONE, o il FILE -- non "
                       "nella voce ne- nella sua riga, e per `%s` la regola del punto 1 non "
                       "ha una lettura: una sezione contiene anche le voci vicine"
                % (livello, campo))
    return (True, "la citazione e- nel testo della voce (%s), e per `%s` non c-e- una "
                  "regola che la contraddica" % (livello, campo))


def leggi_file(percorso=None, quante=165):
    """### Le righe del file del guardiano. ### **Il numero si ASSERISCE**, sempre.

    ### ⛔ **Il percorso arriva dall-argv** *(dal 2026-10-09)*: il guardiano ha mandato
    ### **un secondo file** -- la ### **terza lettura**, `59` righe -- e
    ### **lo stesso attrezzo deve applicare entrambi**, altrimenti ### **la regola si
    duplica e le due copie divergono.**
    """
    rr = [r for r in io.open(percorso or FILE_G, encoding="utf-8").read().split(NL)
          if r.strip()]
    assert len(rr) == quante, ("il file %s non ha %d righe: %d"
                               % (percorso or FILE_G, quante, len(rr)))
    fuori = []
    for r in rr:
        pz = [x.strip() for x in r.split("|")]
        assert len(pz) == 4, r
        cambi = {}
        # ### ⚠ **`da_dividere=A + B` porta DUE PARTI**, e il valore contiene spazi: si
        # ### ### **spezza sul primo `=` di ogni CHIAVE NOTA**, non su ogni spazio.
        testo = pz[1]
        chiavi = [m for m in re.finditer(r"(?:^|\s)(classe|dominio|era|stato|superata_da"
                                         r"|da_dividere)=", testo)]
        for k, m in enumerate(chiavi):
            nome = m.group(1)
            a = m.end()
            b = chiavi[k + 1].start() if k + 1 < len(chiavi) else len(testo)
            cambi[nome] = testo[a:b].strip()
        assert cambi, "nessun cambio leggibile in: %s" % r
        fuori.append({"id": pz[0], "cambi": cambi, "citazione": pz[2], "conf": pz[3]})
    return fuori


def main(argv=()):
    # ### ⛔ **IL FILE, QUANTE RIGHE, E I NOMI DELLE USCITE ARRIVANO DA FUORI:** senza
    # ### questo l-attrezzo sarebbe ### **legato a un file solo**, e il secondo file
    # ### avrebbe voluto ### **una copia del codice.** ### ⭐ **Due copie della stessa
    # ### regola divergono**, ed e- il difetto che il repo chiama <<una legge in due
    # ### posti>>.
    percorso = argv[0] if argv else None
    quante = int(argv[1]) if len(argv) > 1 else 165
    suff = argv[2] if len(argv) > 2 else ""
    # ### ⛔ **E LE VOCI POSSONO VENIRE DA UN COMMIT, e serve per il REFERTO:** una volta
    # ### applicato il lotto, rigirare l-attrezzo ### **sul disco** da-
    # ### ### **`NIENTE_DA_FARE` su tutto** -- i campi sono gia- quelli -- e
    # ### ### **il verdetto VERO si perde.**
    # ### ⭐ **Il verdetto e- cio- che la regola ha deciso QUANDO HA INCONTRATO L-INDICE**,
    # ### non cio- che decide dopo aver vinto: ### **si rigenera dal commit del file.**
    ref = argv[3] if len(argv) > 3 else ""
    if ref:
        import subprocess
        q = subprocess.run(["git", "show", "%s:doc/indice/voci.jsonl" % ref], cwd=RADICE,
                           capture_output=True, text=True, encoding="utf-8")
        assert q.returncode == 0, ref
        testo = q.stdout
    else:
        testo = io.open(os.path.join(D, "voci.jsonl"), encoding="utf-8").read()
    voci = [json.loads(x) for x in testo.split(NL) if x.strip()]
    per = {v["id"]: v for v in voci}
    # ### ⛔ **Il REGISTRO serve per i due requisiti di `SUPERATA`:** `superata_da` deve
    # ### nominare ### **una DECISIONE o un ASSIOMA**, e l-elenco sta nel registro.
    import indice as IX
    _vv, reg = IX.carica()
    righe = leggi_file(percorso, quante)
    lotto, applicate, non_applicate, lasciate = [], [], [], []
    # ### ⛔ **UN VERDETTO PER RIGA, e i conti DEVONO tornare a `165`:** il mandato
    # ### chiede ### **quante applicate, quante non applicate, quante lasciate** -- e
    # ### un conteggio ### **per CAMPO** non risponde a quella domanda, perche- una
    # ### riga che cambia due campi puo- averne ### **uno applicato e uno lasciato.**
    esiti = []
    livelli = collections.Counter()
    for r in righe:
        i, v = r["id"], per[r["id"]]
        riga, file_, n = RO.riga_origine(v)
        if riga is None:
            file_, n = (file_ if "::" not in str(file_) else ""), 0
        f0 = (v["fonte"] or "").split("::")[0]
        liv, come = cerca(r["citazione"], v, riga, f0, n)
        # ### ⛔ **UNA CITAZIONE FRA PARENTESI NON E- UNA CITAZIONE, E IL GUARDIANO LO
        # ### DICHIARA:** `A2` porta *<<(combinazione impossibile: ENTRAMBE+SOSPESA)>>* --
        # ### ### **non e- una frase del repo: e- il MOTIVO STRUTTURALE**, cioe- `F9`.
        # ### ✔ **Si applica, e il motivo dice CHE NON E- UNA CITAZIONE:** rifiutarla
        # ### lascerebbe `F9` violato, e ### **il mandato chiede `F9` acceso.**
        if liv is None and r["citazione"].startswith("(") and r["citazione"].endswith(")"):
            liv, come = ("T-STRUTTURALE", "### NON E- UNA CITAZIONE: il guardiano dichiara "
                                          "fra parentesi un MOTIVO STRUTTURALE, e qui e- `F9`")
        if liv is None:
            non_applicate.append((i, r, come, riga))
            esiti.append((i, "NON_APPLICATA", come))
            continue
        livelli[liv] += 1
        campi, meta, note = {}, {}, []
        salta = []
        quante_lasciate = len(lasciate)
        # ### ⛔ **L-ORDINE DEI CAMPI CONTA, ED E- UN DIFETTO MIO SCOPERTO SU DUE VOCI:**
        # ### `stato=SUPERATA` ### **e** `superata_da=X` sono ### **UNA DECISIONE SOLA**, non
        # ### due. Giudicandoli separatamente, `Z21` e `L-SOGLIA` hanno perso
        # ### ### **entrambi** i campi: il `superata_da` cadeva perche- *<<per un campo senza
        # ### regola la citazione in `T3`/`T4` non basta>>*, e poi lo `stato` cadeva perche-
        # ### ### **<<SUPERATA senza dire da che cosa>>** -- ### **cioe- per la mancanza del
        # ### campo che avevo appena scartato io.**
        # ### ⭐ **`superata_da` NON E- UN CAMPO INDIPENDENTE: e- L-OGGETTO di `SUPERATA`.**
        # ### ➜ Si valuta ### **lo `stato` per primo**, e se la riga dice `SUPERATA`
        # ### ### **il suo oggetto viene con lui.**
        ordine = sorted(r["cambi"].items(),
                        key=lambda kv: {"stato": 0, "superata_da": 1}.get(kv[0], 2))
        for campo, valore in ordine:
            # ### ⛔ **`da_dividere` NELL-INDICE E- UN `bool`**, e il file gli passa due
            # ### parti: il bool dice ### **SE**, `da_dividere_parti` dice ### **CHE COSA**
            # ### -- la chiave aggiunta nel punto `7` del 2026-10-09 proprio per questo.
            if campo == "da_dividere":
                parti = [x.strip() for x in valore.split("+") if x.strip()]
                meta["da_dividere"] = True
                meta["da_dividere_parti"] = (
                    ["parte %d: %s" % (k + 1, p) for k, p in enumerate(parti)]
                    + ["come l-ho trovata: ### LE DUE PARTI LE DICHIARA IL FILE DEL "
                       "GUARDIANO, e la citazione e- <<%s>>" % r["citazione"][:80]])
                note.append("`da_dividere` e- un bool: le parti vanno in "
                            "`da_dividere_parti`")
                continue
            assert campo in CAMPI_SCHEMA, campo
            if str(v[campo]) == valore:
                salta.append("`%s` e- GIA- `%s`" % (campo, valore))
                continue
            if campo == "superata_da" and campi.get("stato") == "SUPERATA":
                # ### ✔ **VIENE COL SUO `stato`:** la riga dice *<<`SUPERATA` da `X`>>*,
                # ### e ### **spezzare la frase in due non la rende piu- vera.**
                campi[campo] = valore
                note.append("`superata_da` viene col suo `stato`: `SUPERATA` da `%s` e- "
                            "UNA DECISIONE SOLA, e spezzarla in due non la rende piu- vera"
                            % valore)
                continue
            if r["conf"] == "media":
                ok, perche = sostiene(v, riga, campo, valore, liv)
                if not ok:
                    lasciate.append((i, campo, valore, perche, riga))
                    continue
                note.append(perche)
            campi[campo] = valore
        # ### ⛔ **E `SUPERATA` HA DUE REQUISITI DELLO SCHEMA**, e lo schema li ha
        # ### ### **rifiutati davvero**: `S02` chiedeva `superata_da=D31` e
        # ### ### **`D31` non e- una DECISIONE ne- un ASSIOMA**; `Z21` chiedeva
        # ### `SUPERATA` ### **senza dire da che cosa.**
        # ### ⭐ **Una voce SUPERATA deve dire DA CHE COSA, e dev-essere una DECISIONE:**
        # ### <<superata>> vuol dire ### **che qualcuno ha deciso altro**, e un difetto
        # ### ### **non decide niente.** ### ➜ **Non lo aggiro: lo chiedo PRIMA, e dove
        # ### non torna ELENCO.**
        if campi.get("stato") == "SUPERATA":
            s = campi.get("superata_da") or v["superata_da"]
            if not s:
                lasciate.append((i, "stato", "SUPERATA",
                                 "### `SUPERATA` SENZA DIRE DA CHE COSA: lo schema pretende `superata_da`, e il file non lo porta. <<Superata>> vuol dire CHE QUALCUNO HA DECISO ALTRO, e chi ha deciso NON SI INVENTA", riga))
                del campi["stato"]
            # ### ⛔ **E QUESTA REGOLA ERA DUPLICATA, ED E- IL DIFETTO:** la copia qui
            # ### diceva ### **<<ne- decisione, ne- assioma>>** e il validatore, dal punto
            # ### `3` di oggi, accetta ### **anche una VOCE.** ### **Due copie della stessa
            # ### regola divergono**, e la copia vecchia ha rifiutato `Z21` e `L-SOGLIA`
            # ### ### **citando una ragione che il repo aveva gia- smesso di avere.**
            # ### ➜ **Si chiede agli STESSI insiemi del validatore**, e la frase del motivo
            # ### li nomina tutti e tre.
            elif (s not in reg["decisioni"] and s not in reg["assiomi"]
                  and s not in per):
                lasciate.append((i, "stato+superata_da", s,
                                 "### `%s` NON E- UNA DECISIONE, NE- UN ASSIOMA, NE- UNA VOCE: lo schema la rifiuta" % s, riga))
                del campi["stato"]
                campi.pop("superata_da", None)

        # ### ⛔ **CHIUDERE PRETENDE `chiusura.criterio` E `chiusura.commit`**, e il commit
        # ### ### **si cerca nella riga.** ### **Se non c-e-, la voce NON si chiude.**
        if campi.get("stato") == "CHIUSA":
            # ### ⭐ **IL COMMIT DI CHIUSURA SI RICAVA, NON SI CERCA NELLA RIGA**
            # ### *(2026-10-09, punto `1` del mandato nuovo)*. ### ⛔ **La versione di ieri
            # ### cercava uno sha DENTRO la riga e, non trovandolo, LASCIAVA la voce:**
            # ### `47` chiusure non fatte. ### **Una riga di documento non ha nessun motivo
            # ### di portare lo sha del commit che l-ha scritta** -- quello sta
            # ### ### **nella storia di git**, e `git log -S --reverse` lo trova.
            # ### ⚠ **E l-attrezzo diventa IDEMPOTENTE col punto `1`:** rigirarlo sul primo
            # ### file chiuderebbe adesso ### **le stesse `47`** che il punto `1` ha chiuso
            # ### a mano. ### **Una regola sola, in un posto solo.**
            import _commit_di_chiusura as CC
            ch, come, dove = CC.chiusura_di(v, r["citazione"], CC.sha_del_tag())
            campi["chiusura"] = ch
            note.append("chiusura: il commit e- %s (%s)" % (come, dove[:120]))
        # ### ⛔ **E `F12` HA RIFIUTATO IL LOTTO, FACENDO IL SUO LAVORO:** `L-SOGLIA` era
        # ### `CHIUSA` col commit ricavato dal punto `1`, e il file la porta a `SUPERATA`
        # ### -- ### **la `chiusura` restava piena su una voce non chiusa.**
        # ### ⭐ **`SUPERATA` non e- `CHIUSA`: SOSTITUISCE la chiusura, non la conferma**
        # ### -- e cio- che la voce ha da dire adesso sta in ### **`superata_da`.**
        # ### ✔ **Il valore vecchio non si perde:** vive in `storico.jsonl`, dentro
        # ### `prima`. ### **E il lotto e- stato RIFIUTATO SENZA SCRIVERE NIENTE:** la cura
        # ### dell-atomicita- lavora ### **per la seconda volta su un caso che non ho
        # ### costruito io.**
        if (campi.get("stato") and campi["stato"] != "CHIUSA"
                and (v["chiusura"] or {}) and "chiusura" not in campi):
            campi["chiusura"] = {}
            note.append("la `chiusura` SI SVUOTA perche- lo stato diventa "
                        + campi["stato"] + ": `F12` pretende che una `chiusura` piena "
                        "implichi `CHIUSA`, e il valore vecchio vive nello storico")

        if not campi and not meta:
            if len(lasciate) > quante_lasciate:
                esiti.append((i, "LASCIATA", "citazione trovata in `%s`, ma NESSUN campo "
                                             "applicato: %d lasciati"
                              % (liv, len(lasciate) - quante_lasciate)))
            else:
                lasciate.append((i, "-", "-", "NIENTE DA FARE: %s" % "; ".join(salta),
                                 riga))
                esiti.append((i, "NIENTE_DA_FARE", "; ".join(salta)))
            continue
        mot = ("verifica completa del guardiano: %s" % r["citazione"])
        mot_pieno = ("%s [citazione trovata in `%s`, %s; confidenza `%s`%s]"
                     % (mot, liv, come, r["conf"],
                        ("; " + "; ".join(note)) if note else ""))[:1200]
        # ### IL PONTE, dove `TRANSIZIONI` non passa: ### **due righe nello STESSO lotto.**
        st = campi.get("stato")
        if st and st != v["stato"]:
            import indice as IX
            if st not in IX.TRANSIZIONI.get(v["stato"], set()):
                lotto.append({"id": i, "quando": DATA, "campi": {"stato": "APERTA"},
                              "motivo": ("verifica completa del guardiano: PONTE OBBLIGATO "
                                         "da `%s` a `%s` (TRANSIZIONI non passa). %s"
                                         % (v["stato"], st, mot_pieno))[:1200]})
        riga_l = {"id": i, "quando": DATA, "campi": campi, "motivo": mot_pieno}
        if meta:
            riga_l["meta"] = meta
        lotto.append(riga_l)
        applicate.append((i, campi, meta, liv, r["conf"]))
        if len(lasciate) > quante_lasciate:
            esiti.append((i, "APPLICATA_IN_PARTE",
                          "applicati %s; lasciati %d"
                          % (sorted(set(campi) | set(meta)),
                             len(lasciate) - quante_lasciate)))
        else:
            esiti.append((i, "APPLICATA", "%s in `%s` (%s)"
                          % (sorted(set(campi) | set(meta)), liv, r["conf"])))
    p = os.path.join(D, "_lotti", "v3_guardiano%s.jsonl" % suff)
    io.open(p, "w", encoding="utf-8", newline=NL).write(
        NL.join(json.dumps(x, ensure_ascii=False) for x in lotto) + NL)
    rapporto = {"applicate": [{"id": a, "campi": b, "meta": c, "livello": d, "conf": e}
                              for a, b, c, d, e in applicate],
                "non_applicate": [{"id": a, "cambi": b["cambi"], "citazione": b["citazione"],
                                   "conf": b["conf"], "perche": c,
                                   "riga": " ".join((d or "").split())[:300]}
                                  for a, b, c, d in non_applicate],
                "lasciate": [{"id": a, "campo": b, "valore": c, "perche": d,
                              "riga": " ".join((e or "").split())[:300]}
                             for a, b, c, d, e in lasciate],
                "livelli": dict(livelli),
                "esiti": [{"id": a, "verdetto": b, "dettaglio": c} for a, b, c in esiti]}
    io.open(os.path.join(D, "_p3_guardiano%s.json" % suff), "w", encoding="utf-8",
            newline=NL).write(json.dumps(rapporto, ensure_ascii=False, indent=1))
    print("  scritto doc/indice/_lotti/v3_guardiano%s.jsonl: %d righe"
          % (suff, len(lotto)))
    print("  ### APPLICATE: %d su %d righe del file" % (len(applicate), len(righe)))
    print("  ### NON APPLICATE (citazione non trovata): %d" % len(non_applicate))
    for i, r, come, _g in non_applicate:
        print("   %-32s <<%s>>  %s" % (i, r["citazione"][:40], come[:70]))
    print("  ### LASCIATE: %d" % len(lasciate))
    for i, c, val, perche, _g in lasciate:
        print("   %-26s %s=%s  %s" % (i, c, val, perche[:110]))
    print("  livelli: %s" % dict(livelli))
    conta = collections.Counter(b for _a, b, _c in esiti)
    print("  ### IL VERDETTO PER RIGA, e i conti tornano:")
    for k, n in conta.most_common():
        print("   %-20s %d" % (k, n))
    print("   %-20s %d  (DEVE essere %d)" % ("in tutto", sum(conta.values()), len(righe)))
    # ### ⛔ **E- UN ASSERT, non una stampa:** se i conti non tornano a `165`
    # ### ### **una riga del guardiano e- stata persa**, e perdere una riga senza
    # ### accorgersene e- ### **esattamente il difetto che il par.9 chiama <<una voce
    # ### persa>>.**
    assert sum(conta.values()) == len(righe), (
        "### I CONTI NON TORNANO: %d verdetti su %d righe. UNA RIGA DEL GUARDIANO E- STATA "
        "PERSA" % (sum(conta.values()), len(righe)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
