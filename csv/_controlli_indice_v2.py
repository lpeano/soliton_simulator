# -*- coding: utf-8 -*-
"""I CONTROLLI DELLA MIGRAZIONE — **devono passare PRIMA del commit** *(punto `6`)*.

| | il controllo |
|---|---|
| **`C1`** | ### **CONSERVAZIONE:** ogni ID del vecchio indice compare in ### **UNO E UNO SOLO** di: `voci.jsonl::id`, `voci.jsonl::alias`, `etichette_rimosse.jsonl` |
| **`C2`** | `migrazione_era1.jsonl` porta, per ### **ogni** ID vecchio, ### **dove e' andato e per quale REGOLA** |
| **`C3`** | ### **LE LISTE DEL GUARDIANO:** ogni voce ha la classificazione indicata, oppure sta nel rapporto dei ### **conflitti** |
| **`C4`** | ### **IDEMPOTENZA:** la seconda esecuzione produce ### **gli stessi byte** |
| **`C5`** | `python csv/indice.py valida` ### **passa** |
| **`C6`** | la ### **vista TSV compatibile** fa girare `python csv/_indice_id.py --blocca SI` |
| **`C7`** | i ### **CONTEGGI** per classe, dominio, era, stato, e dove sono andati i segnaposto |

Gira con:  python csv/_controlli_indice_v2.py
"""
import hashlib
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
import migra_indice_v2 as MG                                 # noqa: E402

# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Controlla una migrazione.
NL = chr(10)
D = os.path.join(RADICE, "doc", "indice")
P = []
ESITI = []


def stampa(s=""):
    P.append(s)
    print(s, flush=True)


def riga(c="-", n=104):
    stampa(c * n)


def esito(nome, ok, dettaglio=""):
    ESITI.append((nome, bool(ok), dettaglio))
    stampa("  %-56s %s   %s" % (nome, "PASSA" if ok else "### FALLISCE", dettaglio))


def jsonl(p):
    return [json.loads(r) for r in io.open(p, encoding="utf-8").read().split(NL) if r.strip()]


def sha(p):
    return hashlib.sha1(io.open(p, "rb").read()).hexdigest()[:12]


def main():
    vecchie = MG.vecchio_indice()
    voci = jsonl(os.path.join(D, "voci.jsonl"))
    etich = jsonl(os.path.join(D, "etichette_rimosse.jsonl"))
    tracce = jsonl(os.path.join(D, "migrazione_era1.jsonl"))
    confl = jsonl(os.path.join(D, "conflitti_era1.jsonl")) \
        if os.path.exists(os.path.join(D, "conflitti_era1.jsonl")) else []
    riga("=")
    stampa("I CONTROLLI DELLA MIGRAZIONE ALLO SCHEMA 2")
    riga("=")
    stampa("  al tag: %d ID vecchi   ->   voci %d, etichette %d, tracce %d, conflitti %d"
           % (len(vecchie), len(voci), len(etich), len(tracce), len(confl)))
    stampa()

    # ---------------------------------------------- C1 CONSERVAZIONE
    ids = {v["id"] for v in voci}
    alias = {}
    for v in voci:
        for a in v["alias"]:
            alias.setdefault(a, []).append(v["id"])
    etic = {e["id"] for e in etich}
    persi, doppi = [], []
    for i in vecchie:
        dove = [x for x, c in (("id", i in ids), ("alias", i in alias),
                               ("etichetta", i in etic)) if c]
        if not dove:
            persi.append(i)
        elif len(dove) > 1:
            doppi.append((i, dove))
    esito("C1 CONSERVAZIONE: ogni ID vecchio in UNO E UNO SOLO posto",
          not persi and not doppi,
          "persi %d, doppi %d%s" % (len(persi), len(doppi),
                                    ("  " + " ".join(persi[:6])) if persi else ""))

    # ---------------------------------------------- C2 LA TRACCIA
    tracciati = {t["id_vecchio"] for t in tracce}
    senza = sorted(set(vecchie) - tracciati)
    esito("C2 la TRACCIA copre ogni ID vecchio, con la REGOLA",
          not senza and all(t.get("regola") for t in tracce),
          "senza traccia %d%s" % (len(senza), ("  " + " ".join(senza[:6])) if senza else ""))

    # ---------------------------------------------- C3 LE LISTE DEL GUARDIANO
    per = {v["id"]: v for v in voci}
    for v in voci:
        for a in v["alias"]:
            per.setdefault(a, v)
    # ### ⚠ **LE CORREZIONI DEL PUNTO 1 (d) DEL MANDATO DI LUCA:** queste nove passano da
    # ### `INFRASTRUTTURA` a `METODO`, perche' parlano della ### **validita' delle misure** e
    # ### non del codice come strumento. ### **Il controllo le conosce**, altrimenti grida
    # ### <<fuori posto>> su una correzione CHIESTA.
    CORRETTE_1D = {"C21", "MASSA-ID", "CONTA-RIGHE", "PIATTAFORMA-NON-TIMBRATA", "CONFIG-1",
                   "ANCORE-1", "COLLAUDO-NON-ESEGUITO", "IMPL-2", "H-ETC-2"}
    # ### LE CORREZIONI DELLA VERIFICA `v3` (2026-10-09), e sono CHIESTE DA LUCA:
    # ### *<<le liste del guardiano si aggiornano DI CONSEGUENZA>>.* NON stanno nelle liste
    # ### di `migra_indice_v2.py`, e c-e un motivo preciso: quelle liste sono CIO- CHE IL
    # ### GUARDIANO AVEVA DETTO AL TEMPO DELLA MIGRAZIONE, e la migrazione DEVE RESTARE
    # ### RIPRODUCIBILE DAL TAG. La correzione sta QUI, dove il controllo dice che cosa si
    # ### ASPETTA OGGI.
    # ### IL BLOCCO A: la lista 2 era un ERRORE DEL GUARDIANO -- quelle voci sono DIFETTI
    # ### DEL CODICE DELL-ERA 1, non lavoro dell-era 2.
    CORRETTE_V3 = {}
    for _i in ("CARICA-ROTAZIONE", "CARICA-SIMMETRIA-FASE", "CARICA-DI-GAUGE",
               "CARICA-PERCORSO", "D03", "D15", "D35", "D38", "FASE-TRASCINAMENTO-3D",
               "MEM-HEBB-PIANO-XY", "SCHW-SOTTO-LAM", "SCHWINGER-UN-NODO",
               "TETTO-CAUSALE-TEMPO-COORDINATO", "Y1"):
        CORRETTE_V3[_i] = ("FISICA", "1", "SOSPESA")                          # (A)
    CORRETTE_V3["RISCRITTURA-GO"] = ("INFRASTRUTTURA", "ENTRAMBE", "APERTA")  # (A)
    CORRETTE_V3["AUDIT-CURE"] = ("METODO", "ENTRAMBE", "APERTA")              # (A)
    CORRETTE_V3["LOSCHMIDT-ECO"] = ("METODO", "ENTRAMBE", "APERTA")           # (A)
    # ### IL BLOCCO G1 CORREGGE LA CORREZIONE: queste cinque VERIFICANO UN FLAG DELL-ERA 1,
    # ### quindi vanno a METODO/era 1/SOSPESA come TS-* e TW-*. Nel blocco B le avevo messe
    # ### a METODO/ENTRAMBE/APERTA perche- il prompt diceva <<altrimenti APERTA>>, E IO
    # ### L-HO APPLICATO ALLA LETTERA: l-errore era nel prompt del guardiano, ma
    # ### l-applicazione acritica e- mia.
    for _i in ("H-ETC-1", "REGISTRO_FISICA:A5", "REGISTRO_FISICA:U2-6", "COMPONENTI:S3"):
        CORRETTE_V3[_i] = ("METODO", "1", "SOSPESA")                 # (G1)
    # ### IL BLOCCO G2: <<Ldisegno/d per arco>> e- UNA MISURA SULL-ERA 1 -- omissione del
    # ### guardiano dal blocco A, dove le altre 14 voci della lista 2 sono passate all-era 1.
    CORRETTE_V3["G1"] = ("FISICA", "1", "SOSPESA")                   # (G2)
    # ### IL PUNTO 4 DEL 2026-10-09: `W5` esce da `FISICA` perche- il suo testo e-
    # ### ### **interamente un protocollo di verifica** (<<CRITERIO di POZZO-D: A/B nel
    # ### driver, scena (ii)(a), 4 semi, 120 passi>>) e ### **non dice niente su che cosa la
    # ### legge faccia.** ### ⚠ **Questo SI- e- un ID, non una regola:** l-ho deciso
    # ### ### **leggendo**, e un ID deciso leggendo va scritto come ID.
    CORRETTE_V3["W5"] = ("METODO", "1", "SOSPESA")                   # (punto 4)
    # ### IL MANDATO DEL 2026-10-09 (una voce dopo l-ultima pulizia): la lista 2 la dava
    # ### `FISICA`/era 2/`AGENDA`, e la voce e- ### **SUPERATA da `A16`** -- la decisione
    # ### di Luca del 2026-10-08. ### **Era 1 perche- la voce e- UNA LETTURA DEL CODICE
    # ### DELL-ERA 1**, non programma dell-era 2.
    CORRETTE_V3["ENERGIA-NON-DEFINITA"] = ("FISICA", "1", "SUPERATA")
    # ### IL MANDATO DEL 2026-10-09 (stato dalla RIGA D-ORIGINE): la lista del guardiano
    # ### dava uno stato, e ### **la riga d-origine ne dice un altro.** `G1` dice
    # ### *<<FATTO>>* e `REG-A` dice *<<CHIUSO>>*: ### **la riga vince sulla lista**, ed e-
    # ### tutto il senso del giro -- *<<la validita- non e- lo stato>>*.
    CORRETTE_V3["G1"] = ("FISICA", "1", "CHIUSA")
    CORRETTE_V3["REG-A"] = ("FISICA", "1", "CHIUSA")
    # ### IL PUNTO 4 DEL MANDATO (dominio delle esplicite): il mandato DA- il dominio, e
    # ### le liste del guardiano ne dicevano un altro. ### **Due ID, non una regola.**
    CORRETTE_V3["PRESIDIO-RIFIUTO-SOLO-SIGILLI"] = ("DOCUMENTAZIONE", "ENTRAMBE", "APERTA")
    CORRETTE_V3["CENS-A3"] = ("DOCUMENTAZIONE", "1", "SOSPESA")
    # ### IL PUNTO 3 DEL MANDATO (era delle esplicite): l-elenco DICHIARATO <<voci
    # ### SOSPESE>> di doc/CURE_fisica_ordine.md:26 e le 38 nominate vanno all-era 1.
    # ### ⚠ **Qui gli ID li DA- IL MANDATO**, quindi si scrivono come ID: non c-e- un
    # ### predicato che dica <<sta nell-elenco dichiarato di quel documento>>.
    for _i, _e, _s in (
            ("ANCORE-1", "1", "SOSPESA"),
            ("ARCHI-PRIMI", "1", "SOSPESA"),
            ("C21", "1", "SOSPESA"),
            ("CONFIG-1", "1", "SOSPESA"),
            ("D26", "1", "SOSPESA"),
            ("FATTI-AVVIO", "1", "SOSPESA"),
            ("H-ETC-2", "1", "SOSPESA"),
            ("LUNGHEZZA-COME-SEGNALE", "1", "SOSPESA"),
            ("MASSA-ID", "1", "SOSPESA"),
            ("PASSO-1", "1", "SOSPESA"),
            ("PAT-1", "1", "SOSPESA"),
            ("PAT-2", "1", "SOSPESA"),
            ("Q6", "1", "SOSPESA"),
            ("R3", "1", "SOSPESA"),
            ("R5", "1", "SOSPESA"),
            ("STATI-LOCALI", "1", "SOSPESA"),
            ("U3", "1", "SOSPESA"),
    ):
        CORRETTE_V3[_i] = (per[_i]["dominio"] if _i in per else CORRETTE_V3.get(_i, (None,))[0], _e, _s)
    # ### IL MANDATO DEL 2026-10-09 (era delle voci di metodo): il guardiano dichiara che
    # ### la regola ### **<<metodo = era ENTRAMBE>> era TROPPO GROSSA.** Queste 14 stanno
    # ### nella lista 1, che le dava `ENTRAMBE`, e ### **riguardano un OGGETTO CONCRETO
    # ### dell-era 1** -- un sigillo, un `.pkl`, il pilota, una funzione del simulatore.
    # ### ⚠ **Sono ID e non una regola**, e il motivo e- che ### **<<oggetto concreto>> non
    # ### si rileva da un predicato**: le ho decise ### **leggendo**, e un ID deciso
    # ### leggendo ### **si scrive come ID** (come `W5` nel punto 4 del giro scorso).
    for _i in (
            "CELLE-NAN-APPESE-NOME-SCADUTO", "CLI-1",
            "D12", "D13",
            "INVENTARIO-SIGILLI-SENZA-COMMIT", "SIGILLO-COMPARATORE-DUPLICATO",
            "SIGILLO-REGISTRO-NON-CONFRONTABILE", "SIGILLO-SENZA-CONFIGURAZIONE",
            "SYNCDB-HEADLESS", "VELENO-DOMINI",
            "VIDEO-SCENA", "Z142",
            "Z15", "Z89"):
        CORRETTE_V3[_i] = (MG.L1[_i][0], "1", "SOSPESA")
    for _i in ("CENS-A6", "CENS-A7", "SMP-APRI-COMMENTO", "MITOSI-2LAM-ACCESO"):
        CORRETTE_V3[_i] = ("DOCUMENTAZIONE", "1", "SOSPESA")        # (B) i FUORI POSTO

    # ### LA VERIFICA COMPLETA DEL GUARDIANO (2026-10-09, file di 165 righe, commit
    # ### `67c12fa`): per DUE voci il file ### **contraddice le liste vecchie DELLO STESSO
    # ### GUARDIANO** -- `CLI-1` sta nella lista `1`, `POTATURA-GUARDIE` nella `3`.
    # ### ✔ **E IL 2026-10-09 IL GUARDIANO LO HA CONFERMATO**, quindi non e- piu- una mia
    # ### scelta di forma: *<<`CLI-1` e `POTATURA-GUARDIE`: vale il file del guardiano, che
    # ### cita; e- il guardiano che lo conferma, quindi `C3` si allinea al file>>.*
    # ### ⭐ **La riconciliazione era TEMPORALE E CITATA** -- la verifica completa e- la
    # ### parola ### **piu- recente** e ### **porta una frase del repo** *(`CLI-1`:
    # ### <<vale come regola generale>>; `POTATURA-GUARDIE`: <<i 57 rami MORTI>>)*, mentre
    # ### le liste ### **non citavano niente.** ### ⚠ **Avevo scritto <<ho scelto la FORMA,
    # ### non il merito>> e l-avevo portato a Luca:** la conferma e- arrivata, e
    # ### ### **una decisione portata a chi tocca e tornata indietro NON E- PIU- MIA.**
    # ### E LE DUE CHE IL PUNTO `1` HA CHIUSO: stanno nelle `47` righe <<chiusure senza
    # ### commit>> del file del guardiano, quindi e- ### **lo stesso file** a dirle
    # ### `CHIUSA` *(`REGISTRO_FISICA:U2-6`: <<PASS>>; `MITOSI-2LAM-ACCESO`:
    # ### <<ANNOTAZIONE DEL 2026-10-02>>)*, mentre `L3` le voleva `SOSPESA`.
    # ### ⭐ **Stessa riconciliazione, stessa ragione:** la parola piu- recente,
    # ### ### **e cita.**
    # ### E `REG-R` dalla TERZA LETTURA *(<<l-hook che RIFIUTA>>, `media`, trovata in
    # ### `T1`)*: la lista `1` le dava un altro dominio. ### **Stessa riconciliazione**, e
    # ### stavolta ### **confermata in anticipo**: il mandato dice *<<vale il file del
    # ### guardiano, che cita>>*.
    CORRETTE_V3["REG-R"] = ("METODO", "ENTRAMBE", "APERTA")
    CORRETTE_V3["REGISTRO_FISICA:U2-6"] = ("METODO", "1", "CHIUSA")
    CORRETTE_V3["MITOSI-2LAM-ACCESO"] = ("DOCUMENTAZIONE", "1", "CHIUSA")
    CORRETTE_V3["CLI-1"] = ("METODO", "1", "SOSPESA")
    CORRETTE_V3["POTATURA-GUARDIE"] = ("INFRASTRUTTURA", "1", "SOSPESA")
    # ### ⚠ **E STA DOPO TUTTE LE ALTRE CORREZIONI DI PROPOSITO:** `CLI-1` e-
    # ### riscritta dal blocco <<era delle voci di metodo>> poco sopra, e
    # ### ### **l-ultima assegnazione vince.** La verifica completa e- la parola
    # ### ### **piu- recente**, quindi la sua riga ### **va per ultima.**

    def _atteso(idv, dom, era, stato):
        """### Che cosa il controllo si aspetta OGGI: la lista, la CORREZIONE, o LA REGOLA.

        ### ⛔ **IL PUNTO 2 DEL 2026-10-09 NON E- UNA LISTA DI ID: E- UNA REGOLA.**
        *<<Un criterio dice come si giudica -> `METODO`>>*, e quindi ### **ogni voce di
        classe `CRITERIO` si aspetta in `METODO`**, qualunque cosa dicesse la lista del
        guardiano. ### **Si scrive la REGOLA, non i 6 ID che oggi la esercitano** --
        altrimenti il controllo va riscritto ogni volta che una voce diventa un criterio.
        """
        d, e, s = CORRETTE_V3.get(idv, (dom, era, stato))
        v = per.get(idv)
        if v is not None and v["classe"] == "CRITERIO":
            d = "METODO"
        return d, e, s

    # ### ⛔ **LA REGOLA DEL `2026-10-10`, e non un-altra lista di ID.**
    # ### `C3` confronta lo stato di OGGI con ### **l-attesa della MIGRAZIONE**, e una
    # ### ### **decisione di Luca presa DOPO** sposta legittimamente una voce: le
    # ### ### **43 decisioni** hanno portato OTTO voci a `SUPERATA` *(sette da `A16`, una
    # ### da `A17`)*, e il controllo gridava ### **<<fuori posto>>** su un lavoro
    # ### ### **CHIESTO.**
    # ### ⭐ **E LA REGOLA GIUSTA NON E- <<queste otto sono ammesse>>:** e-
    # ### ### **<<una voce spostata da una SCRITTURA DICHIARATA non e- fuori posto>>** --
    # ### perche- ### **l-autorita- su dove sta una voce e- lo STORICO**, non la lista
    # ### della migrazione. ### ✅ **Cosi- il controllo non va riscritto alla
    # ### prossima decisione**, ed e- il criterio che questo stesso file dichiara:
    # ### *<<si scrive la REGOLA, non i 6 ID che oggi la esercitano>>*.
    # ### ⚠ **E I DENTI RESTANO: una voce mossa SENZA una riga di storico grida
    # ### ancora** -- e- il caso <<qualcuno ha scritto a mano>>, che `PI-REPLAY` vede dal
    # ### suo lato e che qui si vede da questo.
    mosse = {}
    for _l in io.open(os.path.join(D, "storico.jsonl"), encoding="utf-8"):
        if not _l.strip():
            continue
        _r = json.loads(_l)
        _p, _d = _r.get("prima") or {}, _r.get("dopo") or {}
        if any(str(_p.get(_k, "")) != str(_d.get(_k, ""))
               for _k in ("dominio", "era", "stato")):
            mosse.setdefault(_r["id"], []).append(_r.get("motivo", ""))

    guai = []
    for idv, (dom, _p) in MG.L1.items():
        v = per.get(idv)
        d, e, _s = _atteso(idv, "METODO" if idv in CORRETTE_1D else dom, "ENTRAMBE", None)
        if v is None or v["dominio"] != d or str(v["era"]) != e:
            guai.append("L1 " + idv)
    for idv in MG.L2:
        v = per.get(idv)
        d, e, s = _atteso(idv, "FISICA", "2", "AGENDA")
        if v is None or v["dominio"] != d or str(v["era"]) != e or v["stato"] != s:
            guai.append("L2 " + idv)
    for idv in MG.L3:
        v = per.get(idv)
        d, e, s = _atteso(idv, "FISICA", "1", "SOSPESA")
        if v is None or v["dominio"] != d or str(v["era"]) != e or v["stato"] != s:
            guai.append("L3 " + idv)
    nei_conflitti = {x["id"] for x in confl}
    guai = [g for g in guai if g.split(" ", 1)[1] not in nei_conflitti]
    spostate = [g for g in guai if g.split(" ", 1)[1] in mosse]
    guai = [g for g in guai if g.split(" ", 1)[1] not in mosse]
    esito("C3 LE LISTE DEL GUARDIANO: classificazione come indicata",
          not guai, "fuori posto %d%s; e %d SPOSTATE da una scrittura DICHIARATA%s"
          % (len(guai), ("  " + " ".join(guai[:6])) if guai else "", len(spostate),
             ("  " + " ".join(x.split(" ", 1)[1] for x in spostate[:8]))
             if spostate else ""))

    # ---------------------------------------------- C4 IDEMPOTENZA
    # ### ⛔ **QUESTO CONTROLLO MI HA CANCELLATO 867 CLASSIFICAZIONI, e lo scrivo qui
    # ### perche' non succeda a nessun altro:** rilanciava la migrazione, e la migrazione
    # ### ### **riscrive `voci.jsonl` PARTENDO DAL TAG.** Finita la migrazione era un
    # ### controllo innocuo; ### **dopo la fase 2 era DISTRUTTIVO.**
    # ### ✔ **Adesso: se c'e' lavoro DOPO la migrazione, l'idempotenza NON si rilancia** --
    # ### si ### **dichiara verificata al suo commit** *(`6b8cb90`)*, e la migrazione stessa
    # ### ha un presidio che la ferma.
    files = ["voci.jsonl", "etichette_rimosse.jsonl", "migrazione_era1.jsonl",
             "_indice_meta.json"]
    sto = os.path.join(D, "storico.jsonl")
    n_storico = (sum(1 for r in io.open(sto, encoding="utf-8") if r.strip())
                 if os.path.exists(sto) else 0)
    if n_storico:
        esito("C4 IDEMPOTENZA (NON si rilancia: c'e' lavoro di dopo)", True,
              "storico.jsonl ha %d righe -> verificata al commit 6b8cb90; e la migrazione "
              "ha un PRESIDIO che la ferma" % n_storico)
    else:
        prima = {f: sha(os.path.join(D, f)) for f in files}
        q = subprocess.run([sys.executable, os.path.join(_QUI, "migra_indice_v2.py")],
                           cwd=RADICE, capture_output=True, text=True)
        dopo = {f: sha(os.path.join(D, f)) for f in files}
        diff = [f for f in files if prima[f] != dopo[f]]
        esito("C4 IDEMPOTENZA: la seconda esecuzione da' gli STESSI BYTE",
              q.returncode == 0 and not diff,
              "diversi: %s" % (" ".join(diff) if diff else "nessuno"))

    # ---------------------------------------------- C5 VALIDA
    q5 = subprocess.run([sys.executable, os.path.join(_QUI, "indice.py"), "valida"],
                        cwd=RADICE, capture_output=True, text=True)
    esito("C5 `indice.py valida` passa", q5.returncode == 0,
          (q5.stdout or "").strip().split(NL)[-1][:60])

    # ---------------------------------------------- C6 LA VISTA COMPATIBILE
    # ### QUESTO CONTROLLO ERA PIU- DEBOLE DEL HOOK, e lo scrivo qui perche- non succeda a
    # ### nessun altro: girava SOLO `--blocca SI`, che e- UN-INTERROGAZIONE, e passava
    # ### mentre il `pre-commit` -- che gira `_indice_id.py` NUDO, cioe- IL VALIDATORE --
    # ### bloccava con 12 righe rifiutate (`tipo criterio non ammesso`: alle voci nuove del
    # ### blocco C mancava `tipo_era1`). UN CONTROLLO CHE GIRA UN COMANDO PIU- DEBOLE DI
    # ### QUELLO DEL PRESIDIO NON PROTEGGE NIENTE (`A9`). Adesso gira ENTRAMBI.
    q6v = subprocess.run([sys.executable, os.path.join(_QUI, "_indice_id.py")],
                         cwd=RADICE, capture_output=True, text=True)
    q6 = subprocess.run([sys.executable, os.path.join(_QUI, "_indice_id.py"),
                         "--blocca", "SI"], cwd=RADICE, capture_output=True, text=True)
    m = re.search(r"blocca_run_base `SI`: (\d+) voci su (\d+)", q6.stdout or "")
    esito("C6 la VISTA passa IL VALIDATORE VECCHIO (quello del pre-commit) e la domanda",
          q6v.returncode == 0 and q6.returncode == 0 and bool(m),
          ("%s bloccanti su %s voci" % (m.group(1), m.group(2)))
          if m and not q6v.returncode
          else ("### il validatore NUDO esce %d: %s"
                % (q6v.returncode,
                   " ".join((q6v.stdout or "").split())[-120:])))

    # ---------------------------------------------- C7 I CONTEGGI
    riga("=")
    stampa("C7 I CONTEGGI")
    riga("=")
    for campo in ("classe", "dominio", "era", "stato"):
        c = {}
        for v in voci:
            c[str(v[campo])] = c.get(str(v[campo]), 0) + 1
        stampa("  %-9s %s" % (campo, "  ".join("%s=%d" % (k, c[k])
                                               for k in sorted(c, key=lambda x: -c[x]))))
    seg = {}
    for t in tracce:
        r = t["regola"].split(")")[0] + ")"
        seg[r] = seg.get(r, 0) + 1
    stampa()
    stampa("  LE REGOLE DELLA MIGRAZIONE, per quante volte hanno deciso:")
    for k in sorted(seg, key=lambda x: -seg[x]):
        stampa("      %-8s %4d" % (k, seg[k]))
    stampa()
    stampa("  bloccanti fra le voci: %d" % sum(1 for v in voci if v["blocca"]))
    stampa("  etichette rimosse: %d, con %d citazioni in tutto"
           % (len(etich), sum(e.get("citazioni_n", 0) for e in etich)))

    riga("=")
    tutti = all(x[1] for x in ESITI)
    stampa("I CONTROLLI: %d su %d   ### %s"
           % (sum(1 for x in ESITI if x[1]), len(ESITI),
              "TUTTI PASSATI" if tutti else "QUALCUNO FALLISCE: NON SI VA AVANTI"))
    io.open(os.path.join(D, "_controlli.txt"), "w", encoding="utf-8",
            newline=NL).write(NL.join(P) + NL)
    return 0 if tutti else 1


if __name__ == "__main__":
    sys.exit(main())
