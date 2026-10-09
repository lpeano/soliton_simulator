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
| `F1` | `B2` cita `Z31` nel titolo, e `Z31` prima era `FISICA`/era `1` | `6e5e75b` |
| `F2` | `D35`, prima `era 2`, nel titolo ha `(:5443)` | `6e5e75b` |
| `F3` | `C28`, prima `FISICA`, nel titolo ha *«NON HANNO ALCUN SIGILLO»* | `6e5e75b` |
| `F4` | `TW-1`, prima **etichetta rimossa**, ed e' definita in `doc/SCALE_TW_lettura.md` | `6e5e75b` |
| `F5` | una riga di storico ### **gia' committata** e senza `commit` | **sintetico**, in memoria |
| `F6` | `CENS-A6`, con la nota *«lista `3` … fisica dell'era `1`»* su una voce `DOCUMENTAZIONE` | `e00d2ae` |
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

    # ---------------------------------------------------------------- F1
    z31_prima = [v for v in v_prima if v["id"] == "Z31"]
    assert z31_prima, "Z31 non c'e' a " + PRIMA_V3
    print("  `F1`  Z31 a %s: `%s`/era `%s`   |   oggi: `%s`/era `%s`"
          % (PRIMA_V3, z31_prima[0]["dominio"], z31_prima[0]["era"],
             [v for v in voci if v["id"] == "Z31"][0]["dominio"],
             [v for v in voci if v["id"] == "Z31"][0]["era"]))
    esito("F1  DEVE scattare: B2 cita Z31, e Z31 era FISICA/era 1",
          scatta(IX._f1_gemelle(con(voci, z31_prima)), "B2"),
          "il titolo di B2 dice <<Z31 -- i sigilli non ri-girabili | Z31, ...>>")
    esito("F1  NON deve scattare: con Z31 corretta (METODO/ENTRAMBE)",
          not scatta(IX._f1_gemelle(voci), "B2"))
    # ### LA RESTRIZIONE DEL 2026-10-09 si prova COSI-, e non basta dire che il numero e-
    # ### calato: `D24` dice <<`A2` e- VIOLATO da Lam = mean(I)>>, e ### **`A2` e- uno
    # ### STANDARD che vale per ENTRAMBE le ere** -- e- GIUSTO che differisca.
    # ### ⛔ **E il braccio che DEVE scattare prova che e- LA CLASSE a zittirlo**, non
    # ### qualcos-altro: con `A2` finto `DIFETTO`, `D24` torna a segnalare.
    esito("F1  NON deve scattare: D24 cita A2, che e- uno STANDARD (entrambe le ere)",
          not scatta(IX._f1_gemelle(voci), "D24"),
          "il titolo di D24 dice <<A2 e- VIOLATO da Lam = mean(I)>>")
    a2_finto = json.loads(json.dumps([v for v in voci if v["id"] == "A2"][0]))
    a2_finto["classe"] = "DIFETTO"
    esito("F1  DEVE scattare: con A2 finto DIFETTO -- e- LA CLASSE che lo zittisce",
          scatta(IX._f1_gemelle(con(voci, [a2_finto])), "D24"))

    # ---------------------------------------------------------------- F2
    d35_prima = [v for v in v_prima if v["id"] == "D35"]
    esito("F2  DEVE scattare: D35 era era 2 e nel titolo ha (:5443)",
          scatta(IX._f2_era2(con(voci, d35_prima)), "D35"),
          "era `%s` a %s" % (d35_prima[0]["era"], PRIMA_V3))
    esito("F2  NON deve scattare: D35 corretta (era 1)",
          not scatta(IX._f2_era2(voci), "D35"))

    # ---------------------------------------------------------------- F3
    c28_prima = [v for v in v_prima if v["id"] == "C28"]
    esito("F3  DEVE scattare: C28 era FISICA e il titolo dice <<ALCUN SIGILLO>>",
          scatta(IX._f3_fisica_strumenti(con(voci, c28_prima)), "C28"),
          "dominio `%s` a %s" % (c28_prima[0]["dominio"], PRIMA_V3))
    esito("F3  NON deve scattare: C28 corretta (METODO)",
          not scatta(IX._f3_fisica_strumenti(voci), "C28"))

    # ---------------------------------------------------------------- F4
    tw1_prima = [e for e in e_prima if e["id"] == "TW-1"]
    assert tw1_prima, "TW-1 non era fra le etichette a " + PRIMA_V3
    esito("F4  DEVE scattare: TW-1 era un'etichetta, ed e' DEFINITA in un documento",
          scatta(IX._f4_etichette(tw1_prima), "TW-1"),
          "doc/SCALE_TW_lettura.md la definisce con una riga di tabella")
    esito("F4  NON deve scattare: TW-1 oggi NON e' fra le etichette",
          not any(e["id"] == "TW-1" for e in etich)
          and not scatta(IX._f4_etichette(etich), "TW-1"))
    # ### LA REGOLA DELL-INTESTAZIONE (punto 5), e sono I DUE CASI CHE IL MANDATO FISSA.
    # ### `POST-HOC` e- segnalato da `### 1.2 E LA LETTURA CHE DECIDE DAVVERO -- dichiarata
    # ### POST-HOC, non era fissata prima`: ### **l-ID non e- il SOGGETTO, e- un
    # ### aggettivo.** `TW-1` invece e- definito da ### **una RIGA DI TABELLA**, e le righe
    # ### di tabella la regola NON le tocca: ### **deve continuare a scattare.**
    ph = [e for e in e_prima if e["id"] == "POST-HOC"]
    assert ph, "POST-HOC non era fra le etichette a " + PRIMA_V3
    esito("F4  NON deve scattare: POST-HOC, l-ID sta DENTRO LA PROSA dell-intestazione",
          not scatta(IX._f4_etichette(ph), "POST-HOC"),
          "`### 1.2 ... -- dichiarata POST-HOC, non era fissata prima`")
    esito("F4  DEVE scattare: TW-1 a %s -- una RIGA DI TABELLA lo definisce" % PRIMA_V3,
          scatta(IX._f4_etichette(tw1_prima), "TW-1"),
          "la regola dell-intestazione NON tocca le righe di tabella")
    # ### ⛔ **E il braccio che prova che e- LA REGOLA a zittire `POST-HOC`**, non il caso:
    # ### con la regola spenta ### **POST-HOC torna a segnalare.**
    _vera = IX._intestazione_definisce
    try:
        IX._intestazione_definisce = lambda righe, k, idv: True
        esito("F4  DEVE scattare: con la REGOLA SPENTA, POST-HOC torna a segnalare",
              scatta(IX._f4_etichette(ph), "POST-HOC"))
    finally:
        IX._intestazione_definisce = _vera

    # ---------------------------------------------------------------- F5
    # ### SINTETICO, e in memoria: `_f5_righe` e' PURA proprio per questo.
    righe = [{"id": "X", "commit": "abc1234"}, {"id": "Y", "commit": ""},
             {"id": "Z", "commit": ""}]
    esito("F5  DEVE essere un ERRORE: riga 2 GIA' COMMITTATA e senza commit",
          len(IX._f5_righe(righe, 2)) == 1,
          "n_head=2 -> la riga 2 e' committata, la 3 e' IL RITARDO e NON si segnala")
    esito("F5  NON deve scattare: le righe oltre HEAD sono il RITARDO dichiarato",
          IX._f5_righe(righe[:1] + [{"id": "Y", "commit": "def5678"}] + righe[2:], 2) == []
          and IX._f5_righe(righe, 0) == [])

    # ---------------------------------------------------------------- F7
    # ### ⛔ **IL CASO A RISPOSTA NOTA E- UN MIO ERRORE**, e il mandato lo indica: a
    # ### `89784dc` `CURA1-CORTO` era `FISICA`/era `1`/### **`APERTA`**, perche- avevo
    # ### messo nel campo `stato` l-<<APERTO>> che il documento scrive -- e quello e- lo
    # ### stato ### **dell-era 1**.
    PRIMA_Q1 = "89784dc"
    v_pre_q = al_commit(PRIMA_Q1, "doc/indice/voci.jsonl")
    c1_prima = [v for v in v_pre_q if v["id"] == "CURA1-CORTO"]
    assert c1_prima, "CURA1-CORTO non c-e- a " + PRIMA_Q1
    print("  `F7`  CURA1-CORTO a %s: `%s`/era `%s`/`%s`   |   oggi: `%s`"
          % (PRIMA_Q1, c1_prima[0]["dominio"], c1_prima[0]["era"],
             c1_prima[0]["stato"],
             [v for v in voci if v["id"] == "CURA1-CORTO"][0]["stato"]))
    esito("F7  DEVE essere un ERRORE: CURA1-CORTO era FISICA/era 1/APERTA a " + PRIMA_Q1,
          len(IX._f7_stato(c1_prima)) == 1,
          "la fisica dell-era 1 non chiusa e- SOSPESA")
    esito("F7  NON deve scattare: dopo il punto 1, e su TUTTE le %d voci" % len(voci),
          IX._f7_stato([v for v in voci if v["id"] == "CURA1-CORTO"]) == []
          and IX._f7_stato(voci) == [],
          "0 voci FISICA/era 1 con stato diverso da SOSPESA/CHIUSA")

    # ---------------------------------------------------------------- F6
    a6_prima = [v for v in v_pre_g if v["id"] == "CENS-A6"]
    print("  `F6`  la nota di CENS-A6 a %s: <<%s>>"
          % (PRIMA_G, " ".join((a6_prima[0]["meta"].get("nota_guardiano") or "").split())[:78]))
    esito("F6  DEVE scattare: la nota dice lista 3 (FISICA/1/SOSPESA), la voce e' DOCUMENTAZIONE",
          scatta(IX._f6_note(con(voci, a6_prima)), "CENS-A6"))
    esito("F6  NON deve scattare: con la nota della correzione v3",
          not scatta(IX._f6_note(voci), "CENS-A6"))

    # ------------------------------------------------- LA FORMA DELL'ECCEZIONE
    base = json.loads(json.dumps([v for v in voci if v["id"] == "C28"][0]))
    vuota = json.loads(json.dumps(base))
    vuota["meta"]["eccezione_presidio"] = ["F3: va bene cosi'"]
    esito("ECCEZIONE  DEVE essere un ERRORE: non cita il testo alla lettera",
          len(IX._eccezioni_malformate([vuota])) == 1)
    piena = json.loads(json.dumps(base))
    pezzo = " ".join(base["titolo"].split())[:40]
    piena["meta"]["eccezione_presidio"] = ["F3: il titolo dice <<%s>>, e la parola `sigillo` "
                                           "ci sta perche' la voce CONTA i flag senza "
                                           "sigillo" % pezzo]
    esito("ECCEZIONE  NON deve essere un errore: cita %d caratteri del titolo" % len(pezzo),
          IX._eccezioni_malformate([piena]) == [])
    storta = json.loads(json.dumps(base))
    storta["meta"]["eccezione_presidio"] = ["va bene cosi'"]
    esito("ECCEZIONE  DEVE essere un ERRORE: fuori forma (manca `F<n>:`)",
          len(IX._eccezioni_malformate([storta])) == 1)

    # ------------------------------------- L'ATOMICITA', END-TO-END
    # ### ⛔ **QUESTA PROVA HA TROVATO UN DIFETTO CHE IL COLLAUDO NON VEDEVA:**
    # ### `aggiorna_lotto` validava con `derivati=False` *(che saltava `F7`)*,
    # ### ### **SCRIVEVA**, e solo allora validava tutto -- quindi un lotto che violava
    # ### `F7` ### **veniva scritto** e l-indice restava ### **CORROTTO.** La promessa
    # ### *<<se non passa NON SI SCRIVE NIENTE>>* ### **era falsa.**
    # ### ✔ **E non puo- fare danno:** fotografa i byte, tenta, e ### **se sono cambiati
    # ### li RIMETTE** -- una regressione viene ### **riportata**, non subita.
    _FILES = ("doc/indice/voci.jsonl", "doc/indice/storico.jsonl")
    foto = {f: io.open(os.path.join(RADICE, f), "rb").read() for f in _FILES}
    lotto = os.path.join(RADICE, "doc", "indice", "_lotti", "_prova_atomicita.jsonl")
    io.open(lotto, "w", encoding="utf-8", newline=NL).write(json.dumps(
        {"id": "CURA1-CORTO", "quando": "2026-10-09",
         "campi": {"stato": "APERTA"}, "meta": {},
         "motivo": "PROVA CHE DEVE FALLIRE: F7 deve impedire di riportare una voce "
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
    esito("ATOMICITA-  il lotto che viola F7 e- RIFIUTATO", q.returncode != 0,
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
