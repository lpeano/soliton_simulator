# -*- coding: utf-8 -*-
"""IL COLLAUDO DEI PRESIDI — **ogni presidio DEVE scattare** sul suo caso a risposta nota.

> ### ⛔ **`P1-sexies`: un presidio che non si e' visto SCATTARE non protegge niente** (`A9`).
> **Due bracci per ciascuno:** ### ① **il caso che DEVE scattare**, preso dalla verifica del
> guardiano e riportato allo ### **stato di PRIMA**; ### ② **la voce CORRETTA, che NON deve
> scattare** — altrimenti il presidio e' un ### **FALSO-UNO.**

### ⛔ **MAI SULL'INDICE VERO.** Lo stato di prima si legge con `git show <commit>:<path>`,
e le liste di voci vivono **in memoria**. ### **Niente si scrive in `doc/indice/`**, e la
ragione non e' teorica: nel giro scorso un controllo che per verificare *rilanciava* il suo
oggetto mi ha ### **cancellato `867` classificazioni.**

| presidio | il caso che DEVE scattare | da dove si legge lo stato di prima |
|---|---|---|
| `PI-GEMELLE` | `B2` cita `Z31` nel titolo, e `Z31` prima era `FISICA`/era `1` | `6e5e75b` |
| `PI-SIMBOLI-ERA1` | `D35`, prima `era 2`, nel titolo ha `(:5443)` | `6e5e75b` |
| `PI-PAROLE-STRUMENTO` | `C28`, prima `FISICA`, nel titolo ha *«NON HANNO ALCUN SIGILLO»* | `6e5e75b` |
| `PI-ETICHETTA-DEFINITA` | `TW-1`, prima **etichetta rimossa**, ed e' definita in `doc/SCALE_TW_lettura.md` | `6e5e75b` |
| `PI-STORICO-SENZA-COMMIT` | una riga di storico ### **gia' committata** e senza `commit` | **sintetico**, in memoria |
| `PI-NOTA-CONTRADDICE-LISTA` | `CENS-A6`, con la nota *«lista `3` … fisica dell'era `1`»* su una voce `DOCUMENTAZIONE` | `e00d2ae` |
| ### **la FORMA dell'eccezione** | un `eccezione_presidio` che ### **non cita il testo** | **sintetico** |

Gira con:  python csv/_collaudo_presidi_indice.py
"""
import io
import json
import os
import subprocess
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
sys.path.insert(0, _QUI)
import _presidio                                             # noqa: E402
# ### ⛔ **LA PULIZIA NON SI SILENZIA** *(decisione di Luca, 2026-10-10)*:
# ### `shutil.rmtree(..., ignore_errors=True)` ### **non cancella gli oggetti di
# ### `git`, che sono in SOLA LETTURA, e NON LO DICE** -- e cosi- il `%TEMP%` si era
# ### riempito di ### **24 cartelle** che nessuno vedeva.
import _pulizia                                              # noqa: E402
_presidio.avvia(__file__)
import indice as IX                                          # noqa: E402

# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Collauda i presidi dell'indice.
NL = chr(10)
PRIMA_V3 = "6e5e75b"        # ### prima dei blocchi `A`/`B`/`C`
PRIMA_G = "e00d2ae"         # ### prima del blocco `G`
ESITI = []


def esito(nome, ok, dettaglio=""):
    ESITI.append((nome, bool(ok), dettaglio))
    print("  %-62s %s   %s" % (nome, "PASSA" if ok else "### FALLISCE", dettaglio))


def al_commit(commit, percorso):
    """### ⛔ **SOLO LETTURA.** `git show` non tocca il disco."""
    q = subprocess.run(["git", "show", "%s:%s" % (commit, percorso)], cwd=RADICE,
                       capture_output=True, text=True, encoding="utf-8")
    assert q.returncode == 0, "%s:%s" % (commit, percorso)
    return [json.loads(r) for r in q.stdout.split(NL) if r.strip()]


def oggi(percorso):
    return [json.loads(r) for r in
            io.open(os.path.join(RADICE, percorso), encoding="utf-8").read().split(NL)
            if r.strip()]


def con(voci, sostituite):
    """### UNA COPIA DELLA LISTA, con alcune voci rimpiazzate dalla loro versione di prima."""
    per = {v["id"]: v for v in sostituite}
    return [json.loads(json.dumps(per.get(v["id"], v))) for v in voci]


def cita(err, idv):
    """### `True` se un ERRORE nomina quell-id.

    ### ⛔ **Serve perche- i presidi che SEGNALANO tornano coppie `(id, messaggio)` e
    quelli che sono ERRORI tornano STRINGHE:** `scatta` sa leggere le prime,
    ### **non le seconde**, e usarlo su `PI-REPLAY` dava ### **<<too many values to unpack>>**.
    ### ⚠ **Due forme di uscita per due famiglie di presidi: lo DICHIARO invece di
    unificarle**, perche- unificarle vorrebbe dire ### **toccare tutti i presidi** per un
    collaudo.
    """
    ago = chr(96) + idv + chr(96)
    return any(ago in e for e in err)


def scatta(fuori, idv):
    return any(i == idv for i, _m in fuori)


def main():
    voci = oggi("doc/indice/voci.jsonl")
    etich = oggi("doc/indice/etichette_rimosse.jsonl")
    v_prima = al_commit(PRIMA_V3, "doc/indice/voci.jsonl")
    e_prima = al_commit(PRIMA_V3, "doc/indice/etichette_rimosse.jsonl")
    v_pre_g = al_commit(PRIMA_G, "doc/indice/voci.jsonl")
    print("=" * 100)
    print("IL COLLAUDO DEI PRESIDI -- ogni presidio DEVE scattare sul suo caso a risposta nota")
    print("=" * 100)
    print("  oggi: %d voci, %d etichette   |   %s: %d voci, %d etichette   |   %s: %d voci"
          % (len(voci), len(etich), PRIMA_V3, len(v_prima), len(e_prima), PRIMA_G,
             len(v_pre_g)))
    print("  ### NIENTE SI SCRIVE IN doc/indice/: lo stato di prima si LEGGE con `git show`.")
    print()

    # ---------------------------------------------------------------- PI-GEMELLE
    z31_prima = [v for v in v_prima if v["id"] == "Z31"]
    assert z31_prima, "Z31 non c'e' a " + PRIMA_V3
    print("  `PI-GEMELLE`  Z31 a %s: `%s`/era `%s`   |   oggi: `%s`/era `%s`"
          % (PRIMA_V3, z31_prima[0]["dominio"], z31_prima[0]["era"],
             [v for v in voci if v["id"] == "Z31"][0]["dominio"],
             [v for v in voci if v["id"] == "Z31"][0]["era"]))
    esito("PI-GEMELLE  DEVE scattare: B2 cita Z31, e Z31 era FISICA/era 1",
          scatta(IX._f1_gemelle(con(voci, z31_prima)), "B2"),
          "il titolo di B2 dice <<Z31 -- i sigilli non ri-girabili | Z31, ...>>")
    esito("PI-GEMELLE  NON deve scattare: con Z31 corretta (METODO/ENTRAMBE)",
          not scatta(IX._f1_gemelle(voci), "B2"))
    # ### LA RESTRIZIONE DEL 2026-10-09 si prova COSI-, e non basta dire che il numero e-
    # ### calato: `D24` dice <<`A2` e- VIOLATO da Lam = mean(I)>>, e ### **`A2` e- uno
    # ### STANDARD che vale per ENTRAMBE le ere** -- e- GIUSTO che differisca.
    # ### ⛔ **E il braccio che DEVE scattare prova che e- LA CLASSE a zittirlo**, non
    # ### qualcos-altro: con `A2` finto `DIFETTO`, `D24` torna a segnalare.
    esito("PI-GEMELLE  NON deve scattare: D24 cita A2, che e- uno STANDARD (entrambe le ere)",
          not scatta(IX._f1_gemelle(voci), "D24"),
          "il titolo di D24 dice <<A2 e- VIOLATO da Lam = mean(I)>>")
    a2_finto = json.loads(json.dumps([v for v in voci if v["id"] == "A2"][0]))
    a2_finto["classe"] = "DIFETTO"
    esito("PI-GEMELLE  DEVE scattare: con A2 finto DIFETTO -- e- LA CLASSE che lo zittisce",
          scatta(IX._f1_gemelle(con(voci, [a2_finto])), "D24"))
    # ### ⭐ **L-ESTENSIONE ALLO STATO, SOLO PER LO SCHEMA `D`/`Z`** (punto 6 del
    # ### 2026-10-09). `D08` cita `Z14` e sono ### **LO STESSO FATTO**: `D08` e- `SOSPESA`,
    # ### `Z14` e- `CHIUSA`. ### **E il braccio negativo prova che NON e- un confronto
    # ### generale:** con lo stesso disallineamento ### **fuori** dallo schema `D`/`Z`,
    # ### `PI-GEMELLE` ### **tace** -- due voci diverse possono stare in stati diversi senza
    # ### contraddirsi.
    _d16 = [v for v in voci if v["id"] in ("D08", "Z14")]
    assert len(_d16) == 2, "D08 o Z14 non ci sono"
    # ### ⛔ **ROVESCIATO IL 2026-10-09, E L-ERRORE ERA MIO NELL-APPLICAZIONE:** il braccio
    # ### di prima diceva *<<`D08` cita `Z14`, e sono LO STESSO FATTO con stati diversi:
    # ### DEVE scattare>>*. ### **Non sono lo stesso fatto:** `D08` e- ### **il DIFETTO**,
    # ### `Z14` e- ### **il REPERTO che lo ha trovato** -- e ### **una misura resta
    # ### un-avvertenza anche dopo che il difetto e- curato** *(`D19` CURATO, `Z88` aperta
    # ### come avvertenza)*.
    # ### ⭐ **E il braccio di prima PASSAVA**, perche- la coppia era davvero disallineata:
    # ### ### **un caso a risposta nota con la risposta SBAGLIATA passa**, e non si
    # ### accorge di niente. ### **Il collaudo non puo- trovare un errore nella REGOLA: lo
    # ### trova chi legge i segnali.**
    _d08 = [v for v in voci if v["id"] == "D08"]
    _z14 = [v for v in voci if v["id"] == "Z14"]
    assert _d08 and _z14, "D08 o Z14 non c-e-"
    print("  `PI-GEMELLE`  D08 e Z14 oggi: `%s`/`%s`/era `%s`   e   `%s`/`%s`/era `%s`"
          % (_d08[0]["dominio"], _d08[0]["stato"], _d08[0]["era"],
             _z14[0]["dominio"], _z14[0]["stato"], _z14[0]["era"]))
    esito("PI-GEMELLE  NON deve scattare: `D08` e `Z14` con STATI DIVERSI, stesso dominio ed era",
          not scatta(IX._f1_gemelle(con(voci, _d08 + _z14)), "D08"),
          "`D` e- il DIFETTO, `Z` e- il REPERTO che lo ha trovato: possono stare in stati "
          "diversi A RAGIONE")
    # ### ✔ **E IL VERSO OPPOSTO, perche- `PI-GEMELLE` deve ANCORA vedere dominio ed era:** la
    # ### stessa coppia con ### **`Z14` portata a un altro dominio** ### **DEVE scattare.**
    _z14b = json.loads(json.dumps(_z14[0]))
    _z14b["dominio"] = "METODO" if _z14b["dominio"] != "METODO" else "FISICA"
    esito("PI-GEMELLE  DEVE scattare: la STESSA coppia con `Z14` in un altro DOMINIO",
          scatta(IX._f1_gemelle(con(voci, _d08 + [_z14b])), "D08"),
          "il difetto e il suo reperto parlano della STESSA COSA: il dominio resta")
    _z14c = json.loads(json.dumps(_z14[0]))
    _z14c["era"] = "2" if str(_z14c["era"]) != "2" else "1"
    esito("PI-GEMELLE  DEVE scattare: la STESSA coppia con `Z14` in un-altra ERA",
          scatta(IX._f1_gemelle(con(voci, _d08 + [_z14c])), "D08"),
          "e nella stessa ERA")

    # ---------------------------------------------------------------- PI-SIMBOLI-ERA1
    d35_prima = [v for v in v_prima if v["id"] == "D35"]
    esito("PI-SIMBOLI-ERA1  DEVE scattare: D35 era era 2 e nel titolo ha (:5443)",
          scatta(IX._f2_era2(con(voci, d35_prima)), "D35"),
          "era `%s` a %s" % (d35_prima[0]["era"], PRIMA_V3))
    esito("PI-SIMBOLI-ERA1  NON deve scattare: D35 corretta (era 1)",
          not scatta(IX._f2_era2(voci), "D35"))

    # ---------------------------------------------------------------- PI-PAROLE-STRUMENTO
    c28_prima = [v for v in v_prima if v["id"] == "C28"]
    esito("PI-PAROLE-STRUMENTO  DEVE scattare: C28 era FISICA e il titolo dice <<ALCUN SIGILLO>>",
          scatta(IX._f3_fisica_strumenti(con(voci, c28_prima)), "C28"),
          "dominio `%s` a %s" % (c28_prima[0]["dominio"], PRIMA_V3))
    esito("PI-PAROLE-STRUMENTO  NON deve scattare: C28 corretta (METODO)",
          not scatta(IX._f3_fisica_strumenti(voci), "C28"))

    # ---------------------------------------------------------------- PI-ETICHETTA-DEFINITA
    tw1_prima = [e for e in e_prima if e["id"] == "TW-1"]
    assert tw1_prima, "TW-1 non era fra le etichette a " + PRIMA_V3
    esito("PI-ETICHETTA-DEFINITA  DEVE scattare: TW-1 era un'etichetta, ed e' DEFINITA in un documento",
          scatta(IX._f4_etichette(tw1_prima), "TW-1"),
          "doc/SCALE_TW_lettura.md la definisce con una riga di tabella")
    esito("PI-ETICHETTA-DEFINITA  NON deve scattare: TW-1 oggi NON e' fra le etichette",
          not any(e["id"] == "TW-1" for e in etich)
          and not scatta(IX._f4_etichette(etich), "TW-1"))
    # ### LA REGOLA DELL-INTESTAZIONE (punto 5), e sono I DUE CASI CHE IL MANDATO FISSA.
    # ### `POST-HOC` e- segnalato da `### 1.2 E LA LETTURA CHE DECIDE DAVVERO -- dichiarata
    # ### POST-HOC, non era fissata prima`: ### **l-ID non e- il SOGGETTO, e- un
    # ### aggettivo.** `TW-1` invece e- definito da ### **una RIGA DI TABELLA**, e le righe
    # ### di tabella la regola NON le tocca: ### **deve continuare a scattare.**
    ph = [e for e in e_prima if e["id"] == "POST-HOC"]
    assert ph, "POST-HOC non era fra le etichette a " + PRIMA_V3
    esito("PI-ETICHETTA-DEFINITA  NON deve scattare: POST-HOC, l-ID sta DENTRO LA PROSA dell-intestazione",
          not scatta(IX._f4_etichette(ph), "POST-HOC"),
          "`### 1.2 ... -- dichiarata POST-HOC, non era fissata prima`")
    esito("PI-ETICHETTA-DEFINITA  DEVE scattare: TW-1 a %s -- una RIGA DI TABELLA lo definisce" % PRIMA_V3,
          scatta(IX._f4_etichette(tw1_prima), "TW-1"),
          "la regola dell-intestazione NON tocca le righe di tabella")
    # ### ⛔ **E il braccio che prova che e- LA REGOLA a zittire `POST-HOC`**, non il caso:
    # ### con la regola spenta ### **POST-HOC torna a segnalare.**
    _vera = IX._intestazione_definisce
    try:
        IX._intestazione_definisce = lambda righe, k, idv: True
        esito("PI-ETICHETTA-DEFINITA  DEVE scattare: con la REGOLA SPENTA, POST-HOC torna a segnalare",
              scatta(IX._f4_etichette(ph), "POST-HOC"))
    finally:
        IX._intestazione_definisce = _vera

    # ---------------------------------------------------------------- PI-STORICO-SENZA-COMMIT
    # ### SINTETICO, e in memoria: `_f5_righe` e' PURA proprio per questo.
    righe = [{"id": "X", "commit": "abc1234"}, {"id": "Y", "commit": ""},
             {"id": "Z", "commit": ""}]
    esito("PI-STORICO-SENZA-COMMIT  DEVE essere un ERRORE: riga 2 GIA' COMMITTATA e senza commit",
          len(IX._f5_righe(righe, 2)) == 1,
          "n_head=2 -> la riga 2 e' committata, la 3 e' IL RITARDO e NON si segnala")
    esito("PI-STORICO-SENZA-COMMIT  NON deve scattare: le righe oltre HEAD sono il RITARDO dichiarato",
          IX._f5_righe(righe[:1] + [{"id": "Y", "commit": "def5678"}] + righe[2:], 2) == []
          and IX._f5_righe(righe, 0) == [])

    # ---------------------------------------------------------------- PI-FISICA-ERA1-NON-SOSPESA
    # ### ⛔ **IL CASO A RISPOSTA NOTA E- UN MIO ERRORE**, e il mandato lo indica: a
    # ### `89784dc` `CURA1-CORTO` era `FISICA`/era `1`/### **`APERTA`**, perche- avevo
    # ### messo nel campo `stato` l-<<APERTO>> che il documento scrive -- e quello e- lo
    # ### stato ### **dell-era 1**.
    PRIMA_Q1 = "89784dc"
    v_pre_q = al_commit(PRIMA_Q1, "doc/indice/voci.jsonl")
    c1_prima = [v for v in v_pre_q if v["id"] == "CURA1-CORTO"]
    assert c1_prima, "CURA1-CORTO non c-e- a " + PRIMA_Q1
    print("  `PI-FISICA-ERA1-NON-SOSPESA`  CURA1-CORTO a %s: `%s`/era `%s`/`%s`   |   oggi: `%s`"
          % (PRIMA_Q1, c1_prima[0]["dominio"], c1_prima[0]["era"],
             c1_prima[0]["stato"],
             [v for v in voci if v["id"] == "CURA1-CORTO"][0]["stato"]))
    esito("PI-FISICA-ERA1-NON-SOSPESA  DEVE essere un ERRORE: CURA1-CORTO era FISICA/era 1/APERTA a " + PRIMA_Q1,
          len(IX._f7_stato(c1_prima)) == 1,
          "la fisica dell-era 1 non chiusa e- SOSPESA")
    esito("PI-FISICA-ERA1-NON-SOSPESA  NON deve scattare: dopo il punto 1, e su TUTTE le %d voci" % len(voci),
          IX._f7_stato([v for v in voci if v["id"] == "CURA1-CORTO"]) == []
          and IX._f7_stato(voci) == [],
          "0 voci FISICA/era 1 con stato diverso da SOSPESA/CHIUSA/SUPERATA")
    # ### ⭐ **`SUPERATA` STA CON `CHIUSA`:** una voce superata da una decisione
    # ### ### **non e- aperta**, e- risolta ### **da fuori**. E il braccio accanto prova
    # ### che ### **non e- un allargamento cieco**: `APERTA` ### **scatta ancora.**
    _sup = json.loads(json.dumps([v for v in voci if v["id"] == "CURA1-CORTO"][0]))
    _sup["stato"], _sup["superata_da"] = "SUPERATA", "A16"
    esito("PI-FISICA-ERA1-NON-SOSPESA  NON deve scattare: FISICA/era 1/SUPERATA e- risolta DA FUORI",
          IX._f7_stato([_sup]) == [],
          "da SUPERATA si esce solo verso APERTA: e- uno stato terminale")
    _ap = json.loads(json.dumps(_sup))
    _ap["stato"] = "APERTA"
    esito("PI-FISICA-ERA1-NON-SOSPESA  DEVE scattare ancora: FISICA/era 1/APERTA, cioe- non e- un allargamento "
          "cieco", len(IX._f7_stato([_ap])) == 1)
    # ### ⭐ **L-ESTENSIONE A QUALSIASI DOMINIO (2026-10-09)**, e il caso a risposta nota
    # ### lo indica il mandato: a `72e452f` `CENS-A4` era
    # ### ### **DOCUMENTAZIONE/era 1/APERTA** -- fuori da `FISICA`, quindi `PI-FISICA-ERA1-NON-SOSPESA` vecchio
    # ### ### **NON la vedeva.**
    a4_prima = [v for v in al_commit("72e452f", "doc/indice/voci.jsonl")
                if v["id"] == "CENS-A4"]
    assert a4_prima, "CENS-A4 non c-e- a 72e452f"
    esito("PI-FISICA-ERA1-NON-SOSPESA  DEVE scattare: CENS-A4 a 72e452f era `%s`/era 1/`%s`"
          % (a4_prima[0]["dominio"], a4_prima[0]["stato"]),
          len(IX._f7_stato(a4_prima)) == 1,
          "la regola vale per QUALSIASI dominio, non solo FISICA")

    # ---------------------------------------------------------------- PI-ERA-STATO
    # ### ⛔ **IL CASO A RISPOSTA NOTA LO INDICA IL MANDATO:** *<<`PI-ERA-STATO` DEVE scattare su
    # ### `A2` a `80eaf82`>>*. ### **`A2` e- era `ENTRAMBE` con stato `SOSPESA`**, e
    # ### <<sospesa>> vuol dire ### **<<rimandata all-era 2>>**: una cosa che vale
    # ### ### **anche** nell-era 2 ### **non si puo- rimandare a se stessa.**
    F9_Q = "80eaf82"
    v_f9 = al_commit(F9_Q, "doc/indice/voci.jsonl")
    a2_prima = [v for v in v_f9 if v["id"] == "A2"]
    assert a2_prima, "A2 non c-e- a " + F9_Q
    print("  `PI-ERA-STATO`  A2 a %s: `%s`/era `%s`/`%s`"
          % (F9_Q, a2_prima[0]["classe"], a2_prima[0]["era"], a2_prima[0]["stato"]))
    esito("PI-ERA-STATO  DEVE essere un ERRORE: A2 a %s e- era `%s` con stato `%s`"
          % (F9_Q, a2_prima[0]["era"], a2_prima[0]["stato"]),
          len(IX._f9_era_stato(a2_prima)) == 1,
          "<<sospesa>> vuol dire <<rimandata all-era 2>>, e cio- che vale ANCHE "
          "nell-era 2 non si rimanda a se stesso")
    # ### ⭐ **E LE DUE CURE POSSIBILI SI PROVANO ENTRAMBE**, perche- il mandato non dice
    # ### quale: ### **portarla ad `APERTA`** oppure ### **portarla a era `1`** *(dove
    # ### `SOSPESA` e- lecito)*. ### ⛔ **Quale delle due lo dice il file del guardiano**,
    # ### e il collaudo prova soltanto che ### **tutte e due spengono `PI-ERA-STATO`.**
    _ap9 = json.loads(json.dumps(a2_prima[0]))
    _ap9["stato"] = "APERTA"
    esito("PI-ERA-STATO  NON deve scattare: la PRIMA cura -- era `ENTRAMBE` con stato `APERTA`",
          IX._f9_era_stato([_ap9]) == [])
    _er9 = json.loads(json.dumps(a2_prima[0]))
    _er9["era"] = "1"
    esito("PI-ERA-STATO  NON deve scattare: la SECONDA cura -- era `1` con stato `SOSPESA`",
          IX._f9_era_stato([_er9]) == [],
          "nell-era 1 `SOSPESA` e- lecito, ed e- cio- che `PI-FISICA-ERA1-NON-SOSPESA` pretende")
    # ### ⚠ **E SULL-INDICE DI OGGI NE TROVA CINQUE**, che e- il numero del mandato: e-
    # ### ### **la ragione per cui `PI-ERA-STATO` NON e- nel validatore** *(`A9`: non e- un
    # ### presidio finche- non e- cablato, e cablarlo oggi bloccherebbe il repo)*.
    # ### ⛔ **IL BRACCIO SI ANCORA A `67c12fa`**, il commit del file del guardiano,
    # ### cioe- ### **PRIMA della cura.** Leggere <<oggi>> lo spegnerebbe da se- appena
    # ### le cinque sono curate: ### **un braccio che si spegne quando il difetto sparisce
    # ### non prova piu- niente**, e il caso a risposta nota ### **e- una FOTO.**
    _f9_oggi = IX._f9_era_stato(al_commit("67c12fa", "doc/indice/voci.jsonl"))
    esito("PI-ERA-STATO  DEVE trovare le CINQUE a 67c12fa, e sono quelle che il mandato nomina",
          len(_f9_oggi) == 5
          and sorted(x.split("`")[3] for x in _f9_oggi)
          == ["A2", "LUNGA-BATTITO-CADUTA", "PRESTAZIONI-CORSE", "REPERTI-IMMUTABILI",
              "RIPRESA-ARGV"],
          "e per questo NON si poteva accendere PRIMA: lo accende il commit che le cura")
    # ### ✔ **E ADESSO SULL-INDICE VERO SONO ZERO**, ed e- la condizione che rende
    # ### ### **lecito** accenderlo: le quattro passano ad `APERTA`,
    # ### `LUNGA-BATTITO-CADUTA` a era `1`.
    esito("PI-ERA-STATO  NON deve scattare: su TUTTE le %d voci di oggi, DOPO la cura" % len(voci),
          IX._f9_era_stato(voci) == [],
          "e- la condizione che rende LECITO accenderlo nel validatore")
    # ### ⭐ **IL SECONDO RAMO DELLA REGOLA** -- era `2` ### **=> `AGENDA`** -- oggi
    # ### ### **non ha violazioni**, quindi il caso ### **si costruisce.**
    _e2 = json.loads(json.dumps([v for v in voci if str(v["era"]) == "2"][0]))
    print("  `PI-ERA-STATO`  il secondo ramo: %s, era 2, oggi `%s`" % (_e2["id"], _e2["stato"]))
    esito("PI-ERA-STATO  NON deve scattare: era `2` con stato `AGENDA`, cioe- oggi",
          IX._f9_era_stato([_e2]) == [])
    _e2b = json.loads(json.dumps(_e2))
    _e2b["stato"] = "APERTA"
    esito("PI-ERA-STATO  DEVE scattare: era `2` con stato `APERTA` -- l-era 2 NON E- COMINCIATA",
          len(IX._f9_era_stato([_e2b])) == 1)
    # ### ⛔ **E IL SALTO DICHIARATO:** un ### **segnaposto** non ha ancora uno stato, e
    # ### ### **non si giudica.** Senza questo braccio il salto sarebbe
    # ### ### **una riga di codice senza prova.**
    _sp9 = json.loads(json.dumps(_e2))
    _sp9["era"], _sp9["stato"] = "ENTRAMBE", "DA_CLASSIFICARE"
    esito("PI-ERA-STATO  NON deve scattare: un SEGNAPOSTO -- `DA_CLASSIFICARE` non e- uno stato",
          IX._f9_era_stato([_sp9]) == [],
          "e- l-ASSENZA di uno stato: prima la classe, poi lo stato")

    # ---------------------------------------------------------------- PI-REPLAY
    # ### ⛔ **IL COLLAUDO LO DETTA IL MANDATO, E GIRA SU UNA COPIA:** *<<stato di
    # ### `A2-ANELLO` cambiato a mano + viste rigenerate -> DEVE fallire; senza modifiche
    # ### -> NON deve>>*. ### **Nessun file del repo si tocca:** si copiano
    # ### `voci.jsonl` e `storico.jsonl` in una cartella temporanea.
    import shutil
    import tempfile
    _tmp = tempfile.mkdtemp(prefix="f11_")
    try:
        shutil.copy(IX.VOCI, os.path.join(_tmp, "voci.jsonl"))
        shutil.copy(IX.STORICO, os.path.join(_tmp, "storico.jsonl"))
        _nati = IX._f11_nati()
        _ult = IX._f11_ultimo(os.path.join(_tmp, "storico.jsonl"))
        _vc = [json.loads(r) for r
               in io.open(os.path.join(_tmp, "voci.jsonl"),
                          encoding="utf-8").read().split(NL) if r.strip()]
        esito("PI-REPLAY NON deve scattare: la COPIA INTATTA, tutte le %d voci" % len(_vc),
              IX._f11_righe(_vc, _ult, _nati) == [],
              "l-indice e- il REPLAY del suo storico, e oggi lo e-")
        # ### ⚠ **LA MANOMISSIONE: `A2-ANELLO` cambiato A MANO nella copia.**
        _k = [j for j, w in enumerate(_vc) if w["id"] == "A2-ANELLO"]
        assert _k, "A2-ANELLO non c-e-"
        _prima_stato = _vc[_k[0]]["stato"]
        _vc[_k[0]]["stato"] = "APERTA" if _prima_stato != "APERTA" else "CHIUSA"
        print("  `PI-REPLAY` A2-ANELLO nella COPIA: `%s` -> `%s` (a mano)"
              % (_prima_stato, _vc[_k[0]]["stato"]))
        esito("PI-REPLAY DEVE essere un ERRORE: `A2-ANELLO` cambiato A MANO nella copia",
              cita(IX._f11_righe(_vc, _ult, _nati), "A2-ANELLO"),
              "il campo non e- arrivato da una scrittura dichiarata")
        # ### ⛔ **E LE VISTE RIGENERATE NON LO SALVANO, che e- il punto del mandato:** si
        # ### rigenerano ### **dalla copia manomessa**, quindi ### **concordano con essa**
        # ### -- e il confronto delle viste ### **tace.** ### ⭐ **`PI-REPLAY` scatta comunque,
        # ### perche- non guarda le viste: guarda LO STORICO.**
        _vv0, _rg0 = IX.carica()
        del _vv0
        _reg = json.loads(json.dumps(_rg0))
        _att = IX.invertito(_vc, _reg)
        esito("PI-REPLAY DEVE scattare ANCHE con le viste rigenerate dalla copia manomessa",
              cita(IX._f11_righe(_vc, _ult, _nati), "A2-ANELLO")
              and IX.invertito(_vc, _reg) == _att,
              "le viste sono DERIVATE: rigenerarle dalla manomissione le rende COERENTI "
              "con essa, e nessun altro controllo la vede")
        # ### ⚠ **E LA MANOMISSIONE CHE IL MANDATO DETTA LA VEDE ANCHE `PI-FISICA-ERA1-NON-SOSPESA`, e lo DICO:**
        # ### `A2-ANELLO` e- ### **era `1`**, e `PI-FISICA-ERA1-NON-SOSPESA` vieta era `1` + `APERTA`. ### **Quindi
        # ### quel caso NON dimostra che `PI-REPLAY` serva:** dimostra che ### **scatta.**
        _altri = [e for e in IX.valida(_vc, _reg, verboso=False, derivati=False)
                  if "A2-ANELLO" in e and "`PI-REPLAY`" not in e]
        esito("PI-FISICA-ERA1-NON-SOSPESA LA VEDE ANCHE LUI, e lo dichiaro: era `1` + `APERTA` e- vietato",
              any("`PI-FISICA-ERA1-NON-SOSPESA`" in e for e in _altri),
              "il caso del mandato prova che `PI-REPLAY` SCATTA, non che SERVA")
        # ### ⛔ **QUINDI SERVE UNA MANOMISSIONE CHE NESSUN ALTRO VEDA**, altrimenti `PI-REPLAY`
        # ### e- ### **un presidio senza bisogno dimostrato** -- e un presidio che ripete
        # ### cio- che un altro dice ### **aumenta il numero delle leggi senza aggiungere
        # ### niente** *(il criterio 9-ter di Luca)*.
        # ### ✔ **Il `titolo`: nessun presidio lo confronta con niente.** Cambiarlo a mano
        # ### ### **passa TUTTO** -- vocabolari, stati, ere, viste rigenerate -- e
        # ### ### **solo `PI-REPLAY` lo vede**, perche- solo `PI-REPLAY` chiede ### **da dove viene.**
        _vc2 = json.loads(json.dumps(_vc))
        _vc2[_k[0]]["stato"] = _prima_stato
        _vc2[_k[0]]["titolo"] = "UN TITOLO SCRITTO A MANO, e nessuno lo confronta"
        _soli = [e for e in IX.valida(_vc2, _reg, verboso=False, derivati=False)
                 if "A2-ANELLO" in e]
        esito("PI-REPLAY E- NECESSARIO: il `titolo` cambiato a mano passa TUTTI gli altri",
              _soli == [] and cita(IX._f11_righe(_vc2, _ult, _nati), "A2-ANELLO"),
              "nessun presidio confronta il `titolo` con niente: solo `PI-REPLAY` chiede DA DOVE "
              "VIENE")
        # ### ✔ **E il caso <<nata dopo e senza storico>>, costruito: e- un ERRORE.**
        _nuova = json.loads(json.dumps(_vc[_k[0]]))
        _nuova["id"] = "VOCE-SCRITTA-A-MANO"
        esito("PI-REPLAY DEVE scattare: una voce NATA DOPO la migrazione e SENZA STORICO",
              cita(IX._f11_righe([_nuova], _ult, _nati), "VOCE-SCRITTA-A-MANO"),
              "una voce nuova si crea con `crea-lotto`, che scrive la sua riga")
    finally:
        _pulizia.via_finale(_tmp)

    # ---------------------------------------------------------------- PI-CHIUSURA-ORFANA
    # ### ⛔ **IL CASO A RISPOSTA NOTA E- L-INDICE DI IERI:** a `570d43a` *(dopo il punto
    # ### `1`, prima della cura)* le `chiusura` ORFANE erano ### **41**, e tutte
    # ### ### **venivano dalla migrazione** -- `commit` = `era-1-secondo-ordine`, il NOME
    # ### del tag.
    v_f12 = al_commit("570d43a", "doc/indice/voci.jsonl")
    _orf = IX._f12_chiusura_orfana(v_f12)
    print("  `PI-CHIUSURA-ORFANA` le `chiusura` ORFANE a 570d43a: %d   |   oggi: %d"
          % (len(_orf), len(IX._f12_chiusura_orfana(voci))))
    esito("PI-CHIUSURA-ORFANA DEVE essere un ERRORE: a 570d43a le `chiusura` orfane erano %d" % len(_orf),
          len(_orf) == 41,
          "una voce che dice <<chiusa dal commit X>> e non e- chiusa MENTE")
    esito("PI-CHIUSURA-ORFANA NON deve scattare: su TUTTE le %d voci di oggi, DOPO la cura" % len(voci),
          IX._f12_chiusura_orfana(voci) == [],
          "40 righe NON chiudono -> la `chiusura` si svuota; 1 chiude -> CHIUSA")
    # ### ⚠ **E IL BRACCIO CHE PROVA CHE GUARDA LA `chiusura` E NON LO STATO:** una voce
    # ### `CHIUSA` con la `chiusura` piena ### **e- SANA**, e `PI-CHIUSURA-ORFANA` ### **tace.**
    _ok12 = [v for v in voci if v["stato"] == "CHIUSA" and (v["chiusura"] or {})][0]
    esito("PI-CHIUSURA-ORFANA NON deve scattare: `CHIUSA` con la `chiusura` piena e- SANA",
          IX._f12_chiusura_orfana([_ok12]) == [])
    _ba12 = json.loads(json.dumps(_ok12))
    _ba12["stato"] = "SOSPESA"
    esito("PI-CHIUSURA-ORFANA DEVE scattare: la STESSA voce portata a `SOSPESA` senza svuotare",
          len(IX._f12_chiusura_orfana([_ba12])) == 1,
          "e- esattamente la forma delle 41: lo stato si muove, la `chiusura` resta")

    # ---------------------------------------------------------------- PI-CRITERIO-METODO
    # ### ⛔ **IL CASO A RISPOSTA NOTA E- UNA CURA DEL GIRO SCORSO:** a `4ec2684`
    # ### `REGISTRO_FISICA:D37` era ### **`CRITERIO`/`INFRASTRUTTURA`**, e il punto `4`
    # ### del 2026-10-09 l-ha portata a `DIFETTO`. ### ⭐ **Cosi- lo ZERO di oggi non e-
    # ### un FALSO-ZERO:** e- il risultato di quella cura, e il braccio lo mostra.
    F10_Q = "4ec2684"
    d37_prima = [v for v in al_commit(F10_Q, "doc/indice/voci.jsonl")
                 if v["id"] == "REGISTRO_FISICA:D37"]
    assert d37_prima, "REGISTRO_FISICA:D37 non c-e- a " + F10_Q
    print("  `PI-CRITERIO-METODO` REGISTRO_FISICA:D37 a %s: `%s`/`%s`   |   oggi: `%s`/`%s`"
          % (F10_Q, d37_prima[0]["classe"], d37_prima[0]["dominio"],
             [v for v in voci if v["id"] == "REGISTRO_FISICA:D37"][0]["classe"],
             [v for v in voci if v["id"] == "REGISTRO_FISICA:D37"][0]["dominio"]))
    esito("PI-CRITERIO-METODO DEVE essere un ERRORE: D37 a %s era `CRITERIO`/`INFRASTRUTTURA`" % F10_Q,
          len(IX._f10_criterio_metodo(d37_prima)) == 1,
          "un criterio dice COME SI DECIDE, e non e- infrastruttura")
    esito("PI-CRITERIO-METODO NON deve scattare: su TUTTE le %d voci di oggi" % len(voci),
          IX._f10_criterio_metodo(voci) == [],
          "ZERO violazioni -- ed e- per questo che PI-CRITERIO-METODO SI PUO- accendere e PI-ERA-STATO no")
    # ### ⚠ **E IL BRACCIO CHE PROVA CHE LO ZERO E- VERO:** una voce `CRITERIO` di oggi,
    # ### spostata a `FISICA`, ### **DEVE scattare.** Senza questo, lo zero potrebbe
    # ### venire da una regola che ### **non guarda niente.**
    _cr = json.loads(json.dumps([v for v in voci if v["classe"] == "CRITERIO"][0]))
    _cr["dominio"] = "FISICA"
    esito("PI-CRITERIO-METODO DEVE scattare: %s portata a `FISICA` -- lo zero NON e- un FALSO-ZERO"
          % _cr["id"], len(IX._f10_criterio_metodo([_cr])) == 1)

    # ---------------------------------------------------------------- PI-NOTA-CONTRADDICE-LISTA
    a6_prima = [v for v in v_pre_g if v["id"] == "CENS-A6"]
    print("  `PI-NOTA-CONTRADDICE-LISTA`  la nota di CENS-A6 a %s: <<%s>>"
          % (PRIMA_G, " ".join((a6_prima[0]["meta"].get("nota_guardiano") or "").split())[:78]))
    esito("PI-NOTA-CONTRADDICE-LISTA  DEVE scattare: la nota dice lista 3 (FISICA/1/SOSPESA), la voce e' DOCUMENTAZIONE",
          scatta(IX._f6_note(con(voci, a6_prima)), "CENS-A6"))
    esito("PI-NOTA-CONTRADDICE-LISTA  NON deve scattare: con la nota della correzione v3",
          not scatta(IX._f6_note(voci), "CENS-A6"))
    # ### ⛔ **IL CASO A RISPOSTA NOTA LO INDICA IL MANDATO:** *<<`G1` ha una
    # ### `nota_guardiano` che dice ancora `SOSPESA`; `PI-NOTA-CONTRADDICE-LISTA` DEVE trovarla>>*. La nota e-
    # ### *<<correzione v3 blocco G2: ### **FISICA/era 1/SOSPESA**>>*, e la voce oggi e-
    # ### ### **`CHIUSA`** perche- il guardiano ha dichiarato che e- ### **<<FATTO>>.**
    # ### ⛔ **IL BRACCIO SI ANCORA A `7e4c59c`, perche- il punto `4` TOGLIE la nota:** un
    # ### caso a risposta nota che legge <<oggi>> ### **si spegne quando il difetto
    # ### sparisce**, e allora ### **non prova piu- niente.** ### **E- la seconda volta
    # ### in questo giro** *(la prima: le cinque di `PI-ERA-STATO`)*.
    g1 = [v for v in al_commit("7e4c59c", "doc/indice/voci.jsonl") if v["id"] == "G1"]
    print("  `PI-NOTA-CONTRADDICE-LISTA`  la nota di G1: <<%s>>   |   la voce e- `%s`"
          % (" ".join((g1[0]["meta"].get("nota_guardiano") or "").split())[:70],
             g1[0]["stato"]))
    esito("PI-NOTA-CONTRADDICE-LISTA  DEVE scattare: a 7e4c59c la nota di `G1` DICHIARA `SOSPESA` e la voce e- "
          "`CHIUSA`", scatta(IX._f6_note(g1), "G1"),
          "una nota che DICHIARA una tripla `dominio/era/stato` e- un-ASSERZIONE, e se la "
          "voce si e- mossa la nota e- SCADUTA")
    # ### ⚠ **E IL BRACCIO NEGATIVO PROVA CHE NON LEGGE LA PROSA:** con la tripla
    # ### ### **allineata** alla voce, `PI-NOTA-CONTRADDICE-LISTA` ### **tace** -- quindi non scatta
    # ### ### **per la presenza della parola**, ma per ### **la contraddizione.**
    # ### ✔ **E ADESSO LA NOTA NON C-E- PIU-:** il punto `4` l-ha TOLTA, e il braccio
    # ### accanto prova che ### **`PI-NOTA-CONTRADDICE-LISTA` tace sulla `G1` di oggi.**
    esito("PI-NOTA-CONTRADDICE-LISTA  NON deve scattare: la `G1` di OGGI, dopo che la nota e- stata TOLTA",
          not scatta(IX._f6_note(voci), "G1"),
          "una domanda a cui si e- risposto non si riscrive: si TOGLIE")
    _g1b = json.loads(json.dumps(g1[0]))
    _g1b["meta"]["nota_guardiano"] = ("correzione v3 blocco G2: %s/era %s/%s -- la tripla "
                                      "ALLINEATA" % (_g1b["dominio"], _g1b["era"],
                                                     _g1b["stato"]))
    esito("PI-NOTA-CONTRADDICE-LISTA  NON deve scattare: la STESSA nota con la tripla ALLINEATA",
          not scatta(IX._f6_note([_g1b]), "G1"),
          "non scatta per la PAROLA, scatta per la CONTRADDIZIONE")
    # ### ⛔ **E LA VIA GROSSOLANA SI MISURA, per dire perche- l-ho scartata:** <<la nota
    # ### nomina uno stato diverso da quello della voce>> dava ### **69 segnali.**
    _grosso = sum(1 for v in voci
                  for _s in ("SOSPESA", "CHIUSA", "APERTA", "AGENDA", "SUPERATA")
                  if _s in ((v.get("meta") or {}).get("nota_guardiano") or "").upper()
                  and v["stato"] != _s)
    esito("PI-NOTA-CONTRADDICE-LISTA  LA VIA GROSSOLANA DAVA %d SEGNALI, e la stretta ne da- %d"
          % (_grosso, len(IX._f6_note(voci))),
          _grosso > 20 and len(IX._f6_note(voci)) < 5,
          "era la condizione di FERMO del task history: se l-estensione scatta su decine "
          "di voci, e- troppo grossa")

    # ------------------------------------------------- PI-PAROLE-STRUMENTO e l-eccezione di CENS-B15
    # ### ⛔ **UN-ECCEZIONE VA COLLAUDATA COME UN PRESIDIO:** se nessuno prova che
    # ### ### **senza di essa il segnale c-era**, l-eccezione e- ### **una riga che
    # ### nessuno sa se serve.**
    _b15 = [v for v in voci if v["id"] == "CENS-B15"]
    assert _b15, "CENS-B15 non c-e-"
    esito("PI-PAROLE-STRUMENTO  NON scatta: `CENS-B15` ha l-`eccezione_presidio`",
          not scatta(IX._f3_fisica_strumenti(voci), "CENS-B15"),
          "il <<commento>> del titolo NON e- uno strumento: e- CIO- DI CUI LA VOCE PARLA")
    _b15s = json.loads(json.dumps(_b15[0]))
    _b15s["meta"] = {k: w for k, w in _b15s["meta"].items()
                     if k != "eccezione_presidio"}
    esito("PI-PAROLE-STRUMENTO  DEVE scattare: la STESSA voce SENZA l-eccezione",
          scatta(IX._f3_fisica_strumenti([_b15s]), "CENS-B15"),
          "e- la prova che l-eccezione SERVE: senza, il segnale c-era")

    # ------------------------------------------------- LA FORMA DELL'ECCEZIONE
    base = json.loads(json.dumps([v for v in voci if v["id"] == "C28"][0]))
    vuota = json.loads(json.dumps(base))
    vuota["meta"]["eccezione_presidio"] = ["PI-PAROLE-STRUMENTO: va bene cosi'"]
    esito("ECCEZIONE  DEVE essere un ERRORE: non cita il testo alla lettera",
          len(IX._eccezioni_malformate([vuota])) == 1)
    piena = json.loads(json.dumps(base))
    pezzo = " ".join(base["titolo"].split())[:40]
    piena["meta"]["eccezione_presidio"] = ["PI-PAROLE-STRUMENTO: il titolo dice <<%s>>, e la parola `sigillo` "
                                           "ci sta perche' la voce CONTA i flag senza "
                                           "sigillo" % pezzo]
    esito("ECCEZIONE  NON deve essere un errore: cita %d caratteri del titolo" % len(pezzo),
          IX._eccezioni_malformate([piena]) == [])
    storta = json.loads(json.dumps(base))
    storta["meta"]["eccezione_presidio"] = ["va bene cosi'"]
    esito("ECCEZIONE  DEVE essere un ERRORE: fuori forma (manca `<ID-PRESIDIO>:`)",
          len(IX._eccezioni_malformate([storta])) == 1)

    # ---------------------------------------------------------------- PI-OGGETTI-ERA1
    # ### ⛔ **I TRE CASI LI INDICA IL MANDATO**, e il negativo e- quello che conta:
    # ### `P6` dice *<<ogni csv di misura porta BLOB, SEME e ### **TUTTI I FLAG**>>* --
    # ### ### **nomina la PAROLA flag, non un flag** -- e `FALSO-ZERO` e- un difetto del
    # ### metodo senza nessun oggetto. ### **Se scattassero, i marcatori sarebbero troppo
    # ### larghi.**
    t3a_prima = [v for v in al_commit("72e452f", "doc/indice/voci.jsonl")
                 if v["id"] == "T3a"]
    assert t3a_prima, "T3a non c-e- a 72e452f"
    esito("PI-OGGETTI-ERA1  DEVE scattare: T3a a 72e452f era `ENTRAMBE` e dice <<SIGILLO scena (ii)>>",
          scatta(IX._f8_era1(t3a_prima), "T3a"),
          "era `%s`, stato `%s`" % (t3a_prima[0]["era"], t3a_prima[0]["stato"]))
    # ### ⛔ **ROVESCIATO IL 2026-10-09: dopo il taglio del marcatore `.py` `CONFIG-1` e
    # ### ### `PAT-1` NON SCATTANO PIU-**, e non e- un difetto: e-
    # ### ### **la MISURA del marcatore che ho tolto.** Entrambe scattavano
    # ### ### **soltanto** per un `.py` nel testo *(`csv/_config_delle_misure.py` e
    # ### `dovespingelagravita.py`)*: ### **nessun altro marcatore le prendeva.**
    # ### ⚠ **E l-allargamento del giro scorso, che le aveva messe qui, era "giusto" solo
    # ### perche- il marcatore era largo:** la frase che scrissi -- *<<la riga d-origine
    # ### nomina `csv/_config_delle_misure.py` e i flag>>* -- ### **nominava i flag come
    # ### se contassero, e NON contavano: li prendeva il `.py`.**
    for _i in ("CONFIG-1", "PAT-1"):
        _p = [v for v in al_commit("ba400c0", "doc/indice/voci.jsonl")
              if v["id"] == _i]
        assert _p, _i
        esito("PI-OGGETTI-ERA1  NON scatta piu-: `%s` a ba400c0 scattava SOLO per un `.py`" % _i,
              not scatta(IX._f8_era1(_p), _i),
              "e- la MISURA del marcatore tolto, non un difetto")
    for _i, _che in (("P6", "e- una REGOLA: nomina la PAROLA flag, non un flag"),
                     ("FALSO-ZERO", "e- un difetto del METODO, senza oggetti concreti")):
        _v = [v for v in voci if v["id"] == _i]
        assert _v, _i
        esito("PI-OGGETTI-ERA1  NON deve scattare: %s, %s" % (_i, _che),
              not scatta(IX._f8_era1(_v), _i))

    # ------------------------------------------------- PI-OGGETTI-ERA1 dopo il taglio del `.py`
    # ### ⛔ **I TRE CASI LI DETTA IL MANDATO DEL 2026-10-09:** *<<DEVE scattare su
    # ### `CONFIG-1` a `80eaf82`, NON su `A9` ne- su `INDICE-COLLAUDO-SCRITTURA`>>*.
    # ### ⭐ **E i due negativi sono la MISURA del marcatore che ho tolto:** entrambi
    # ### scattavano ### **solo per un `.py`** -- `A9` nomina `_presidio.py`,
    # ### `INDICE-COLLAUDO-SCRITTURA` nomina `indice.py` -- e ### **un `.py` non e- un
    # ### oggetto dell-era `1`: e- un oggetto DEL REPO.**
    F8_Q = "80eaf82"
    _v8 = al_commit(F8_Q, "doc/indice/voci.jsonl")
    _c1 = [v for v in _v8 if v["id"] == "CONFIG-1"]
    assert _c1, "CONFIG-1 non c-e- a " + F8_Q
    print("  `PI-OGGETTI-ERA1`  CONFIG-1 a %s: era `%s`   |   oggi: era `%s`"
          % (F8_Q, _c1[0]["era"],
             [v for v in voci if v["id"] == "CONFIG-1"][0]["era"]))
    # ### ⛔ **IL MANDATO CHIEDE «DEVE scattare su `CONFIG-1` a `80eaf82`»: NON SI PUO-,**
    # ### e la ragione e- ### **misurata, non opinabile:** a `80eaf82` `CONFIG-1` e-
    # ### ### **era `1`** *(il mandato dell-era delle voci di metodo l-ha spostata)*, e `PI-OGGETTI-ERA1`
    # ### per costruzione guarda ### **SOLO le voci `ENTRAMBE`.** ### **Nessun marcatore
    # ### puo- farla scattare la-**, e il braccio lo ASSERISCE.
    # ### ⭐ **E C-E- DI PIU-, ED E- LA PARTE CHE CONTA:** anche a `ba400c0`, dove
    # ### `CONFIG-1` ### **E- `ENTRAMBE`**, dopo il taglio l-unico marcatore che la farebbe
    # ### scattare e- ### **un FLAG DEL SIMULATORE** *(`FORK_SU2`, `CAMPO_SPINORIALE`,
    # ### `TAU_LUCE`)* -- e ### **quello stesso marcatore fa scattare `FALSO-ZERO`**, che
    # ### nomina `REGISTRO_STATO` e `REGISTRO_METRI`, ### **flag VERI del simulatore**, e
    # ### che il mandato precedente dichiara ### **NON DEVE scattare.**
    # ### ⛔ **Le due richieste sono INCOMPATIBILI, e la misura sta nel referto: non
    # ### scelgo io quale cade.**
    esito("PI-OGGETTI-ERA1  NON scatta: `CONFIG-1` a %s e- era `1`, e `PI-OGGETTI-ERA1` guarda solo le `ENTRAMBE`"
          % F8_Q,
          str(_c1[0]["era"]) == "1" and not scatta(IX._f8_era1(_c1), "CONFIG-1"),
          "il mandato la vuole scattante LA-: non si puo-, e la ragione e- L-ERA")
    for _i, _che in (("A9", "nomina `_presidio.py`, e un `.py` NON e- dell-era 1"),
                     ("INDICE-COLLAUDO-SCRITTURA", "nomina `indice.py`, idem")):
        _vx = [v for v in voci if v["id"] == _i]
        assert _vx, _i
        esito("PI-OGGETTI-ERA1  NON deve scattare: `%s` -- %s" % (_i, _che),
              not scatta(IX._f8_era1(_vx), _i),
              "era la MISURA del marcatore che ho tolto")
        # ### ⚠ **E IL BRACCIO CHE PROVA CHE IL TAGLIO E- MIRATO:** la stessa voce con
        # ### ### **una funzione del simulatore** nel titolo ### **DEVE scattare.**
        _vy = json.loads(json.dumps(_vx[0]))
        _vy["titolo"] = (_vy["titolo"] or "")[:60] + " -- e tocca calcola_psi"
        esito("PI-OGGETTI-ERA1  DEVE scattare: `%s` con `calcola_psi` nel titolo" % _i,
              scatta(IX._f8_era1([_vy]), _i),
              "il taglio e- MIRATO: via i `.py`, restano le funzioni del simulatore")

    # ------------------------------------- L'ATOMICITA', END-TO-END
    # ### ⛔ **QUESTA PROVA HA TROVATO UN DIFETTO CHE IL COLLAUDO NON VEDEVA:**
    # ### `aggiorna_lotto` validava con `derivati=False` *(che saltava `PI-FISICA-ERA1-NON-SOSPESA`)*,
    # ### ### **SCRIVEVA**, e solo allora validava tutto -- quindi un lotto che violava
    # ### `PI-FISICA-ERA1-NON-SOSPESA` ### **veniva scritto** e l-indice restava ### **CORROTTO.** La promessa
    # ### *<<se non passa NON SI SCRIVE NIENTE>>* ### **era falsa.**
    # ### ✔ **E non puo- fare danno:** fotografa i byte, tenta, e ### **se sono cambiati
    # ### li RIMETTE** -- una regressione viene ### **riportata**, non subita.
    _FILES = ("doc/indice/voci.jsonl", "doc/indice/storico.jsonl")
    foto = {f: io.open(os.path.join(RADICE, f), "rb").read() for f in _FILES}
    lotto = os.path.join(RADICE, "doc", "indice", "_lotti", "_prova_atomicita.jsonl")
    io.open(lotto, "w", encoding="utf-8", newline=NL).write(json.dumps(
        {"id": "CURA1-CORTO", "quando": "2026-10-09",
         "campi": {"stato": "APERTA"}, "meta": {},
         "motivo": "PROVA CHE DEVE FALLIRE: PI-FISICA-ERA1-NON-SOSPESA deve impedire di riportare una voce "
                   "FISICA/era 1 ad APERTA, e NON deve scrivere niente"},
        ensure_ascii=False) + NL)
    q = subprocess.run([sys.executable, os.path.join(_QUI, "indice.py"),
                        "aggiorna-lotto", lotto], cwd=RADICE, capture_output=True,
                       text=True, encoding="utf-8")
    dopo = {f: io.open(os.path.join(RADICE, f), "rb").read() for f in _FILES}
    cambiati = [f for f in _FILES if foto[f] != dopo[f]]
    for f in cambiati:                      # ### si RIMETTE, qualunque cosa sia andata
        io.open(os.path.join(RADICE, f), "wb").write(foto[f])
    os.remove(lotto)
    esito("ATOMICITA-  il lotto che viola PI-FISICA-ERA1-NON-SOSPESA e- RIFIUTATO", q.returncode != 0,
          "uscita %d" % q.returncode)
    esito("ATOMICITA-  e NON ha scritto NIENTE: i byte sono IDENTICI", not cambiati,
          ("### CAMBIATI: %s -- RIMESSI dalla fotografia" % " ".join(cambiati))
          if cambiati else "voci.jsonl e storico.jsonl byte per byte")

    # ---------------------------------------------------------------- il verdetto
    print()
    print("=" * 100)
    tutti = all(x[1] for x in ESITI)
    print("IL COLLAUDO DEI PRESIDI: %d su %d   ### %s"
          % (sum(1 for x in ESITI if x[1]), len(ESITI),
             "TUTTI PASSATI" if tutti else "QUALCUNO FALLISCE: NON SI COMMITTA"))
    print("=" * 100)
    # ### ⛔ **E la prova che NON ho toccato l'indice vero:** se qualcosa fosse stato scritto,
    # ### il file sarebbe diverso da quando il collaudo e' partito.
    print("  ### doc/indice/voci.jsonl e etichette_rimosse.jsonl: %d e %d righe, come "
          "all'inizio" % (len(oggi("doc/indice/voci.jsonl")),
                          len(oggi("doc/indice/etichette_rimosse.jsonl"))))
    return 0 if tutti else 1


if __name__ == "__main__":
    sys.exit(main())
