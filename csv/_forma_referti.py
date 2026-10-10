# -*- coding: utf-8 -*-
"""LA FORMA DI UN TESTO GENERATO — **REPERTO CONGELATO** *oppure* **VISTA VIVA**, mai
### **entrambe.**

> ### ⛔ **IL MANDATO DI LUCA, `2026-10-10`, punto `4`:** *«Decidi e ### **DICHIARA una
> forma**: o il referto di un mandato chiuso e' un ### **REPERTO congelato al suo commit**
> *(e la CI non lo rigenera piu')*, o ### **si rigenera e allora non e' una fotografia**.
> ### **Non entrambe.** Misura quanti referti cadono oggi e scrivi il numero.»*

### 📌 **LA DECISIONE, e vale per i testi generati di questo repo:**

| | |
|---|---|
| **`REPERTO`** | un testo che dice ### **che cosa si e' misurato A UN ISTANTE.** ### ⛔ **La CI NON lo rigenera**, e il presidio verifica ### **il suo BLOB**: un reperto si tocca solo ### **a mano**, e allora si vede. ### **Si RIMISURA rigirando il suo comando AL SUO COMMIT**, come un sigillo. |
| **`VIVO`** | un testo che dice ### **com'e' il repo OGGI** *(i metodi, i riferimenti, lo stato dell'infrastruttura)*. ### ✅ **La CI lo rigenera e pretende la diff VUOTA**, perche' non ha una data: ### **se cambia, e' perche' il repo e' cambiato e il testo era scaduto.** |

### ⚠ **IL MOTIVO, MISURATO e non ragionato:** rigenerati il `2026-10-10`, **`4` referti su
`6`** cambiavano. ### **Due per FOTOGRAFIA** — `1012` → `1013` ID, `128` → `131` metodi,
`40` → `41` presidi: ### **il referto non era sbagliato, il repo si era mosso.** ### ⭐ **E
uno era cambiato NELLE ORE fra il commit che lo ha scritto e quello dopo**, per i miei
stessi commit. ### **Un documento che scade dal commit che lo scrive non si puo' tenere
byte-identico con un `git diff`.**

### ⭐ **E LA REGOLA C'ERA GIA', per i sigilli:** `CLAUDE.md` par.`6` dice che ### **un
sigillo si rigira AL SUO COMMIT**, e che ### **un sigillo vecchio che non passa sul blob di
oggi NON E' UN DIFETTO.** ### **Un referto di mandato chiuso e' lo stesso oggetto**, e
questa non e' una regola nuova *(`9-ter`)*: e' ### **quella, applicata dove mancava.**

### ⛔ **E LA DISTINZIONE E' UN CAMPO, NON UN GIUDIZIO** *(par.`9`: «se una decisione serve
a un programma, serve un CAMPO»)*: sta in `TESTI`, qui sotto, e ### **il presidio rifiuta un
testo generato che non vi compaia.**

Gira con:  python csv/_forma_referti.py  ·  --collaudo
"""
import glob
import hashlib
import io
import os
import re
import subprocess
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
sys.path.insert(0, _QUI)
import _presidio                                             # noqa: E402

# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Guarda la FORMA dei testi
# generati: quali si congelano e quali si rigenerano.

PRESIDIO = "REFERTO-FOTOGRAFIA-RIGENERATA"

NL = chr(10)
VIVO, REPERTO = "VIVO", "REPERTO"
WORKFLOW = os.path.join(".github", "workflows", "era2.yml")

# ### ⚠ **IL SENTINELLA, e serve per ARMARE un braccio:** `DISCO` vuol dire
# ### ### **<<leggi il workflow dal disco>>**, e `None` vuol dire ### **<<il
# ### workflow NON SI LEGGE>>**. ### **Senza due valori distinti il caso <<manca il
# ### workflow>> non si potrebbe provare**, e sarebbe un ramo muto (`A8`).
DISCO = "--dal-disco--"

# ### ⛔ **IL REGISTRO: `(file, stato, che cos-e-, il comando che lo produce, BLOB)`.**
# ### ⚠ **Il `BLOB` e- `sha1` dei BYTE COMMITTATI, primi 16** -- e si confronta con
# ### ### **`git show`**, non col disco: ### **confrontare un disco con se stesso e- il
# ### difetto `BLOB-DAL-DISCO-NON-DAL-REPO`**, e l-ho gia- fatto una volta.
# ### ⭐ **E UN `VIVO` NON HA BLOB**: il suo blob e- ### **quello di oggi**, per
# ### definizione, e dichiararlo vorrebbe dire congelarlo.
TESTI = (
    ("doc/REFERTO_seconda_parte_era2.md", REPERTO, "il mandato `1` di `6`",
     "python csv/_referto_seconda_parte.py --con-lenti", "3e875ce029615cec"),
    ("doc/REFERTO_decisioni_43_era2.md", REPERTO, "il mandato `2` di `6`",
     "python csv/_referto_decisioni_43.py", "edd91d9f9d3e339f"),
    ("doc/REFERTO_piano_era2.md", REPERTO, "il mandato `3` di `6`",
     "python csv/_referto_piano_era2.py", "4c2484f7174826d5"),
    ("doc/REFERTO_infrastruttura_era2_terza.md", REPERTO, "il mandato `4` di `6`",
     "python csv/_referto_terza_parte.py", "f50484aedb24f167"),
    ("doc/REFERTO_regole_era2.md", REPERTO, "il mandato `5` di `6`",
     "python csv/_referto_regole.py", "2e4f2252ceac30cc"),
    # ### ⭐ **IL CASO PIU- CHIARO DI TUTTI:** questo nasce da una misura fatta sul
    # ### simulatore `3ddc56d9`, che ### **non e- quello di oggi** -- quindi
    # ### ### **non si puo- rigenerare NEANCHE VOLENDO**, e chiamarlo <<vivo>> sarebbe
    # ### una bugia.
    ("doc/CONTRATTO_nascita.md", REPERTO,
     "la misura dell-ordine delle estrazioni, sul simulatore `3ddc56d9`",
     "python csv/_contratto_nascita.py", "298aafc36a25793d"),
    # ### ✅ **TROVATO DAL PRESIDIO STESSO, al primo giro:** si dichiarava
    # ### ### **generato** e ### **non stava nel registro.** E- l-analisi del
    # ### ### **punto 5 del mandato del `2026-09-26`**, quindi ### **un reperto.**
    ("doc/LETTORI_INDICE_analisi.md", REPERTO,
     "l-analisi dei sei lettori, al mandato del `2026-09-26`",
     "python csv/_analisi_lettori_indice.py", "33579194ec0ccf02"),
    # ### ⛔ **E QUESTO E- UN `REPERTO` PER FORZA, non per scelta:** dice
    # ### ### **quanto spazio era libero a un istante**, e lo spazio libero
    # ### ### **cambia da un minuto all-altro.** ### **Un `VIVO` fallirebbe un minuto
    # ### dopo averlo scritto** -- ed e- esattamente il caso che il presidio descrive
    # ### nella sua riga <<non FALLIRE il giorno dopo averla scritta>>.
    # ### ⛔ **E IL MANIFEST DELL-ARCHIVIO E- IL `REPERTO` PIU- STRETTO DI
    # ### TUTTI:** e- la fotografia di una operazione ### **IRREVERSIBILE** -- i file
    # ### ### **non sono piu- nel repo** -- e rigenerarlo vorrebbe dire ### **rifare lo
    # ### spostamento**, che non si puo- rifare due volte.
    # ### ⛔ **IL REFERTO DEL PROTOTIPO E- UN `REPERTO`, e il motivo e- doppio:**
    # ### ### **nasce da una CORSA** *(`python proto_camminata/_letture.py`, minuti)*, e
    # ### ### **dice che cosa si e- misurato il 2026-10-10** -- non <<com-e- il repo
    # ### oggi>>. ### ⚠ **Rigenerarlo in CI vorrebbe dire RIFARE LA CORSA a ogni
    # ### commit**, e un referto che costa minuti ### **e- la ragione numero uno per
    # ### spegnere un passo di CI** *(`A9` dal lato del tempo)*.
    ("doc/REFERTO_prototipo_camminata_v2.md", REPERTO,
     "le dieci letture del prototipo `v2`, al `2026-10-10`",
     "python proto_camminata/_referto2.py", "d523a9ab53ac0931"),
    ("doc/REFERTO_prototipo_camminata.md", REPERTO,
     "le sette letture del prototipo della camminata, al `2026-10-10`",
     # ### ⚠ **IL BLOB CAMBIA PERCHE- IL REFERTO E- STATO ANNOTATO** *(la lettura
     # ### del guardiano sul `v1`, 2026-10-10)*, e l-annotazione sta ### **NEL
     # ### GENERATORE**, non nel file: ### **un REPERTO ritoccato a mano si vede**, ma uno
     # ### ### **rigenerato con l-annotazione dentro resta RIPRODUCIBILE.**
     "python proto_camminata/_referto.py", "5d2223c98bca09df"),
    ("doc/ARCHIVIO_E_2026-10-10.tsv", REPERTO,
     "lo spostamento su `E:` del `2026-10-10`",
     "python csv/_archivia_su_e.py --esegui", "20fa1129a49ee9dd"),
    ("doc/SPAZIO_DISCO_2026-10-10.md", REPERTO,
     "lo spazio su disco al mandato del `2026-10-10`",
     "python csv/_spazio_disco.py", "25bfc8c629cdd777"),
    ("doc/REFERTO_infrastruttura_era2.md", VIVO,
     "lo stato dell-infrastruttura dell-era `2` OGGI",
     "python csv/_referto_infrastruttura_era2.py", ""),
    ("doc/RIFERIMENTI_era2.md", VIVO, "i riferimenti dentro il codice OGGI",
     "python csv/_rif_nel_codice.py", ""),
    ("doc/METODI_era1_in_era2.md", VIVO, "i metodi dell-era `1` OGGI",
     "python csv/_metodi_era2.py", ""),
    # ### ⭐ **E QUESTI DUE sono il caso piu- puro di `VIVO`:** contano
    # ### ### **le voci e gli ID dell-indice**, quindi ### **scadono al commit che cambia
    # ### l-indice.** ### ✅ **Il `pre-commit` li rigenera e li mette in stage**, e la
    # ### CI pretende la diff vuota: e- ### **esattamente il contratto di un `VIVO`.**
    ("doc/indice/_controlli.txt", VIVO, "i controlli della migrazione, OGGI",
     "python csv/_controlli_indice_v2.py --scrivi", ""),
    ("doc/COLLAUDO_presidio_indice.txt", VIVO,
     "il collaudo dei presidi dell-indice, OGGI",
     "python csv/_presidio_indice.py --collaudo --scrivi", ""),
)


def _blob_committati(rel):
    """### I blob ### **dal REPO**, non dal disco: ### **quello a `HEAD` E quello nello
    STAGE.**

    ### ⚠ **PERCHE- DUE E NON UNO:** nel commit che ### **dichiara** un reperto, i
    byte nuovi stanno ### **nello stage** e `HEAD` porta ancora i vecchi; in ogni commit
    dopo, i due coincidono. ### ⛔ **E guardare SOLO `HEAD` significherebbe non poter
    MAI dichiarare un blob nello stesso commit che lo produce.**
    ### ⭐ **E NON si guarda il DISCO:** confrontare un disco con se stesso e- il
    difetto `BLOB-DAL-DISCO-NON-DAL-REPO`, e l-ho gia- fatto una volta.
    """
    fuori = []
    for arg in ("HEAD:" + rel, ":" + rel):
        q = subprocess.run(["git", "show", arg], cwd=RADICE, capture_output=True)
        if q.returncode == 0:
            fuori.append(hashlib.sha1(q.stdout).hexdigest()[:16])
    return fuori


def _workflow():
    p = os.path.join(RADICE, WORKFLOW)
    if not os.path.exists(p):
        return None
    return io.open(p, encoding="utf-8", errors="replace").read()


def _nominati(testo):
    """I file che la CI ### **rigenera e pretende identici** *(`git diff --exit-code`)*."""
    fuori = set()
    for m in re.finditer(r"git diff --exit-code --([^\n]*)", testo or ""):
        for x in m.group(1).split():
            if x.endswith((".md", ".jsonl", ".tsv", ".txt")):
                fuori.add(x.strip())
    return fuori


def controlla(testo=DISCO, registro=None):
    """### `[]` se la forma e- rispettata. ### **`testo` e `registro` si passano per
    poterli SABOTARE nel collaudo senza toccare il disco.**"""
    reg = TESTI if registro is None else registro
    wf = _workflow() if testo == DISCO else testo
    err = []
    if not reg:
        return ["### `%s`: il REGISTRO E- VUOTO, e un presidio su un registro vuoto "
                "tace per VACUITA-" % PRESIDIO]
    if wf is None:
        err.append("### `%s`: `%s` NON SI LEGGE, e senza il workflow i due controlli "
                   "sulla CI non provano niente" % (PRESIDIO, WORKFLOW))
    nom = _nominati(wf)
    noti = {r[0] for r in reg}
    for rel, stato, _che, _cmd, blob in reg:
        if stato not in (VIVO, REPERTO):
            err.append("### `%s` `%s`: lo stato `%s` non e- ne- `%s` ne- `%s`"
                       % (PRESIDIO, rel, stato, VIVO, REPERTO))
            continue
        if stato == REPERTO:
            if not blob:
                err.append("### `%s` `%s`: e- un `%s` e NON DICHIARA IL BLOB -- e senza "
                           "il blob un reperto si puo- riscrivere a mano e nessuno lo "
                           "vede" % (PRESIDIO, rel, REPERTO))
            else:
                veri = _blob_committati(rel)
                if not veri:
                    err.append("### `%s` `%s`: non e- NE- a `HEAD` NE- nello stage"
                               % (PRESIDIO, rel))
                elif blob not in veri:
                    err.append(
                        "### `%s` `%s`: il blob dichiarato e- `%s` e i BYTE COMMITTATI "
                        "danno `%s`. ### Un `%s` si tocca solo A MANO, quindi questo e- "
                        "UNA MODIFICA A MANO -- oppure il reperto e- stato RIGENERATO, "
                        "che e- la cosa che la forma VIETA"
                        % (PRESIDIO, rel, blob, " / ".join(veri), REPERTO))
            # ### ⭐ **E IL REPERTO DEVE DIRLO IN TESTA.** Il passo di CI che
            # ### ho tolto portava un commento che dice la cosa giusta:
            # ### *<<un referto SCADUTO dice numeri che non sono quelli di oggi, e
            # ### ### **SEMBRA FATTO**>>*. ### ✅ **Per un reperto <<scaduto>> e- la
            # ### parola sbagliata** -- non ha mai parlato di oggi -- ### **ma il
            # ### <<sembra fatto>> resta vero**, e si cura facendogli ### **DIRE in testa
            # ### che e- congelato**, non pretendendolo identico a una misura di oggi.
            p = os.path.join(RADICE, rel)
            testa = ""
            if os.path.exists(p):
                testa = "".join(io.open(p, encoding="utf-8",
                                        errors="replace").readlines()[:8])
            if "CONGELATO" not in testa:
                err.append(
                    "### `%s` `%s`: e- un `%s` e NON DICE IN TESTA di essere CONGELATO. "
                    "### Chi lo legge lo prenderebbe per una misura di OGGI, e un "
                    "documento che <<sembra fatto>> e- peggio di uno che tace"
                    % (PRESIDIO, rel, REPERTO))
            if rel in nom:
                err.append(
                    "### `%s` `%s`: e- un `%s` e LA CI LO RIGENERA pretendendo la diff "
                    "vuota. ### E- <<ENTRAMBE>>, che il mandato VIETA: un reperto e- una "
                    "fotografia, e pretenderla identica a una misura di oggi la fa "
                    "FALLIRE il giorno dopo averla scritta" % (PRESIDIO, rel, REPERTO))
        else:
            if blob:
                err.append("### `%s` `%s`: e- un `%s` e DICHIARA UN BLOB -- dichiararlo "
                           "vorrebbe dire congelarlo" % (PRESIDIO, rel, VIVO))
            if rel not in nom:
                err.append(
                    "### `%s` `%s`: e- un `%s` e LA CI NON LO RIGENERA. ### Un testo che "
                    "dice <<com-e- il repo OGGI>> e che nessuno ricontrolla INVECCHIA IN "
                    "SILENZIO, e sembra fatto" % (PRESIDIO, rel, VIVO))
    # ### ⛔ **IL PERIMETRO E- DICHIARATO E DECIDIBILE, e non <<tutto cio- che
    # ### sembra generato>>.** ### ⚠ **Il primo giro me l-ha insegnato due volte:**
    # ### cercando <<GENERATO>> nelle prime righe ho preso ### **un modello**
    # ### *(`_corpo_punto_ripresa.md` dice <<RIGENERATO per intero>>)*, e allargando il
    # ### criterio sono arrivato a ### **sedici errori** su documenti che nessuno aveva
    # ### chiesto di classificare.
    # ### ⭐ **E IL NUMERO CHE DECIDE: in `doc/` ci sono `119` referti, e la CI ne
    # ### rigenerava `5`.** ### **La forma <<un referto e- un REPERTO congelato>> e-
    # ### quella che il repo ha SEMPRE avuto per `114` su `119`** -- e ### **le cinque
    # ### eccezioni sono esattamente quelle che si sono rotte.**
    # ### ✅ **Quindi il perimetro con i DENTI e- <<cio- che la CI rigenera>>**: li-
    # ### la forma e- una scelta attiva, e ### **li- si decide.** Il resto si
    # ### ### **CONTA e si DICHIARA** -- sotto, come segnale — invece di coprirlo a
    # ### meta-.
    # ### ⛔ **E IL COMANDO UNICO NON PUO- RIGENERARE UN REPERTO.** ### ⭐ **Il
    # ### primo giro di questo presidio me l-ha trovato addosso, su un clone pulito:**
    # ### `collauda.py` faceva girare il generatore della seconda parte, che
    # ### ### **riscriveva un reperto** e gli ### **toglieva la riga `CONGELATO`** -- e
    # ### poi questo presidio, che gira dopo, ### **lo vedeva mancare.**
    # ### ⚠ **<<ENTRAMBE>> non riguarda SOLO la CI: riguarda OGNI cosa che rigenera**,
    # ### e il comando unico e- la piu- facile da dimenticare.
    # ### ⚠ **E SI GUARDA SOLO IL BLOCCO `COLLAUDI`, non tutto il file:** al primo
    # ### giro cercavo il nome ### **in tutto il testo**, e ### **il mio stesso commento
    # ### che spiega la cura faceva scattare il presidio.** ### **E- la classe della
    # ### regex che non distingue un COMMENTO da un USO**, e ci sono cascato di nuovo.
    _cl = os.path.join(RADICE, "primo_ordine", "collauda.py")
    _tutto = (io.open(_cl, encoding="utf-8", errors="replace").read()
              if os.path.exists(_cl) else "")
    _m = re.search(r"^COLLAUDI = \((.*?)^\)", _tutto, re.S | re.M)
    # ### ⛔ **E DAL BLOCCO SI TOLGONO I COMMENTI**, perche- il commento che spiega
    # ### questa cura ### **sta dentro il blocco**, accanto alla riga che ha togliato --
    # ### ed e- il posto giusto. ### ✅ **Un controllo deve guardare il CODICE**, non
    # ### le parole che lo descrivono.
    _testo_cl = NL.join(r for r in (_m.group(1) if _m else "").split(NL)
                        if not r.strip().startswith("#"))
    if _tutto and not _testo_cl:
        err.append("### `%s`: `collauda.py` c-e- ma il blocco `COLLAUDI` NON SI LEGGE -- "
                   "e senza quel blocco questo controllo tace per VACUITA-" % PRESIDIO)
    for rel, stato, _che, cmd, _b in reg:
        if stato != REPERTO or not cmd:
            continue
        _vai = cmd.replace("python ", "").split()[0]
        if _vai and _vai in _testo_cl:
            err.append(
                "### `%s` `%s`: e- un `%s` e IL COMANDO UNICO (`collauda.py`) fa girare "
                "`%s`, che lo RIGENERA. ### <<ENTRAMBE>> non riguarda solo la CI: "
                "riguarda OGNI cosa che rigenera" % (PRESIDIO, rel, REPERTO, _vai))
    for rel in sorted(nom):
        if rel.endswith((".md", ".txt")) and rel not in noti:
            err.append("### `%s` `%s`: LA CI LO RIGENERA e NON STA NEL REGISTRO -- "
                       "quindi nessuno ha deciso se e- un `%s` o un `%s`"
                       % (PRESIDIO, rel, REPERTO, VIVO))
    return err


def segnale():
    """### Il CONTO di cio- che il perimetro NON copre. ### **Si dichiara, non si tace.**

    ### ⚠ **NON e- un errore e non ferma niente**: sono ### **gli altri testi
    generati del repo**, che nessun mandato ha chiesto di classificare. ### ⛔ **Ma il
    numero sta scritto**, perche- ### **un perimetro che non dice quanto lascia fuori
    sembra coprire tutto.**
    """
    tutti = sorted(glob.glob(os.path.join(RADICE, "doc", "REFERTO_*.md")))
    noti = {r[0] for r in TESTI}
    dentro = [p for p in tutti
              if ("doc/" + os.path.basename(p)) in noti]
    return ("i referti in `doc/`: %d, e nel registro ne stanno %d -- "
            "gli altri %d sono REPERTI per la forma dichiarata (nessuno li rigenera), "
            "e NON hanno un blob dichiarato: e- il buco noto di questa forma"
            % (len(tutti), len(dentro), len(tutti) - len(dentro)))


def collaudo():
    ok = [0, 0]

    def esito(che, passa, nota=""):
        ok[1] += 1
        ok[0] += 1 if passa else 0
        print("  %-64s %s   %s" % (che, "PASSA" if passa else "### FALLISCE", nota))

    print("=" * 100)
    print("IL COLLAUDO DELLA FORMA DEI TESTI GENERATI -- nei DUE VERSI")
    print("=" * 100)
    wf = _workflow()
    rep = [r for r in TESTI if r[1] == REPERTO]
    viv = [r for r in TESTI if r[1] == VIVO]
    esito("sul disco: la forma e- rispettata", controlla() == [],
          "%d testi: %d reperti, %d vivi" % (len(TESTI), len(rep), len(viv)))
    esito("### i due gruppi HANNO MATERIA", len(rep) >= 3 and len(viv) >= 2,
          "### se uno fosse vuoto il presidio proverebbe UNA SOLA delle due forme")
    esito("### e la CI nomina davvero dei file", len(_nominati(wf)) >= 5,
          "%d file nominati in un `git diff --exit-code`" % len(_nominati(wf)))
    # ---------------------------------------------------- i casi che DEVONO fallire
    rotto = [(a, b, c, d, ("0" * 16) if e else e) for a, b, c, d, e in TESTI]
    esito("### DEVE scattare: il BLOB di un reperto NON COINCIDE",
          any("i BYTE COMMITTATI danno" in x for x in controlla(registro=rotto)),
          "### un reperto si tocca solo a mano, quindi un blob diverso E- una modifica")
    senza = [(a, b, c, d, "") for a, b, c, d, _e in TESTI]
    esito("### DEVE scattare: un reperto SENZA blob",
          any("NON DICHIARA IL BLOB" in x for x in controlla(registro=senza)),
          "### senza blob un reperto si riscrive a mano e nessuno lo vede")
    # ### ⛔ **IL CASO CENTRALE DEL MANDATO: <<NON ENTRAMBE>>.** Si aggiunge al
    # ### workflow, ### **IN MEMORIA**, un passo che rigenera un reperto.
    vittima = rep[0][0]
    wf2 = (wf or "") + NL + "          git diff --exit-code -- " + vittima + NL
    esito("### DEVE scattare: la CI RIGENERA un reperto (<<entrambe>>)",
          any("E- <<ENTRAMBE>>" in x for x in controlla(testo=wf2)),
          "### e- il caso che il mandato VIETA: `%s`" % vittima)
    # ### e il verso opposto: un `VIVO` che nessuno ricontrolla
    wf3 = (wf or "").replace("git diff --exit-code -- " + viv[0][0], "echo nulla")
    esito("### DEVE scattare: un `VIVO` che la CI NON rigenera",
          any("LA CI NON LO RIGENERA" in x for x in controlla(testo=wf3)),
          "### un testo <<di oggi>> che nessuno ricontrolla INVECCHIA IN SILENZIO")
    # ### ⛔ **E IL BRACCIO DEL <<CONGELATO>>, armato SENZA SCRIVERE SUL DISCO:**
    # ### si dichiara reperto un testo ### **VIVO**, che in testa non lo dice -- e il
    # ### controllo ### **deve accorgersene.**
    travestito = [(a, REPERTO if a == viv[0][0] else b, c, d,
                   ("0" * 16) if a == viv[0][0] else e) for a, b, c, d, e in TESTI]
    esito("### DEVE scattare: un reperto che NON DICE di essere congelato",
          any("NON DICE IN TESTA" in x for x in controlla(registro=travestito)),
          "### travestito da reperto: `%s`" % viv[0][0])
    # ### ⛔ **Il braccio si arma togliendo UN VIVO**, cioe- un file che
    # ### ### **la CI rigenera**: quello e- il perimetro con i denti.
    fuori = [r for r in TESTI if r[0] != viv[0][0]]
    esito("### DEVE scattare: un testo che la CI rigenera e che NON sta nel registro",
          any("NON STA NEL REGISTRO" in x for x in controlla(registro=fuori)),
          "### chi legge non saprebbe se congelarlo o rigenerarlo: `%s`" % viv[0][0])
    # ### ⛔ **IL BRACCIO DEL CASO NUOVO:** si dichiara reperto un testo il cui
    # ### generatore ### **E- in `collauda.py`** -- cioe- il difetto vero di stamattina.
    _vivo_in_cl = [(a, REPERTO if a == viv[0][0] else b, c, d,
                    ("0" * 16) if a == viv[0][0] else e) for a, b, c, d, e in TESTI]
    esito("### DEVE scattare: un reperto che IL COMANDO UNICO rigenera",
          any("IL COMANDO UNICO" in x for x in controlla(registro=_vivo_in_cl)),
          "### e- il difetto che il presidio ha trovato ADDOSSO A ME su un clone pulito")
    esito("### DEVE scattare: il registro VUOTO",
          any("REGISTRO E- VUOTO" in x for x in controlla(registro=())),
          "### un presidio su un registro vuoto tace per VACUITA-")
    esito("### DEVE scattare: il workflow che NON SI LEGGE",
          any("NON SI LEGGE" in x for x in controlla(testo=None)),
          "### senza il workflow i due controlli sulla CI non provano niente")
    esito("NON deve scattare: rimesso tutto, la forma TACE", controlla() == [],
          "### i bracci di sopra scattavano per i loro casi finti")
    print("=" * 100)
    print("IL COLLAUDO DELLA FORMA: %d su %d   %s"
          % (ok[0], ok[1], "### TUTTI PASSATI" if ok[0] == ok[1] else "### CI SONO BUCHI"))
    print("=" * 100)
    return 0 if ok[0] == ok[1] else 1


def main(argv):
    _presidio.avvia(__file__)
    if "--collaudo" in argv:
        return collaudo()
    err = controlla()
    rep = [r for r in TESTI if r[1] == REPERTO]
    viv = [r for r in TESTI if r[1] == VIVO]
    print("  `%s`: %d testi generati -- %d `%s` (congelati, la CI NON li rigenera), "
          "%d `%s` (la CI li rigenera e pretende la diff vuota)"
          % (PRESIDIO, len(TESTI), len(rep), REPERTO, len(viv), VIVO))
    print("  ### SEGNALE, e NON un errore: %s" % segnale())
    for e in err[:12]:
        print("  %s" % e)
    print("  ### %d errori" % len(err))
    return 1 if err else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
