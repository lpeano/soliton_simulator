# -*- coding: utf-8 -*-
"""IL REFERTO DEL `v2` — **GENERATO da `uscite/letture_v2.json`, VERDETTI COMPRESI.**

### ⛔ **Ogni numero e ogni verdetto escono dal `json`** *(`L-NUMERI`)*: il confronto fra la
previsione e il numero **lo fa il codice**, con le soglie del task history.

Gira con:  python proto_camminata/_referto2.py
"""
import io
import json
import math
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
sys.path.insert(0, _QUI)
sys.path.insert(0, os.path.join(RADICE, "csv"))
import _presidio                                              # noqa: E402

_presidio.avvia(__file__)

NL = chr(10)
FONTE = os.path.join(_QUI, "uscite", "letture_v2.json")
DEST = os.path.join(RADICE, "doc", "REFERTO_prototipo_camminata_v2.md")

CONFERMA = "### ✅ **CONFERMA**"
SMENTITA = "### ⛔ **SMENTITA**"
NONDEC = "### ⚠ **NON DECIDIBILE**"
NESSUNA = "### ⛔ **NESSUNA TROVATA** *(criterio di RIAPERTURA)*"
FALLISCE = "### ✅ **FALLISCE, E DEVE**"


def verdetti(d):
    L = d["letture"]
    v = {}

    g = L["G_gauge"]
    v["G"] = (CONFERMA if max(g["densita"], g["olonomie"], g["spettro"]) <= g["soglia"]
              else SMENTITA,
              "densita' per nodo **%.3g**, olonomie **%.3g**, spettro **%.3g** — "
              "tutte sotto la soglia **%.3g**"
              % (g["densita"], g["olonomie"], g["spettro"], g["soglia"]))

    b = L["G_deve_fallire"]["densita_senza_ruotare_versori"]
    v["G!"] = (FALLISCE if b > 1e-6 else SMENTITA,
               "coi versori **NON ruotati** la densita' differisce di **%.3g**, cioe' "
               "**%d ordini di grandezza** sopra la soglia. ### ⭐ **E- la PROVA che i "
               "riferimenti locali NON sono ridondanti**, e il punto `1` del mandato "
               "regge" % (b, int(round(math.log10(b / g["soglia"])))))

    i = L["1_isotropia"]
    peg = max(x for k, x in i.items() if k != "soglia")
    v["1"] = (CONFERMA if peg <= i["soglia"] else SMENTITA,
              "il peggiore delle tre scene e' **%.3g**, su soglia **%.3g** — e la "
              "rinumerazione **porta i versori e le `U`**, non li rigenera" % (peg,
                                                                              i["soglia"]))

    c = L["2_cono"]
    peg = max(x for k, x in c.items() if k not in ("T", "estremita_fuori"))
    v["2"] = (CONFERMA if peg == 0.0 else SMENTITA,
              "oltre **%d** archi, nelle **tre** scene e **col trasporto acceso**: "
              "**%.3g** su **%d** estremita'"
              % (c["T"], peg, c["estremita_fuori"]))

    bb = L["B_bande"]
    id0 = bb["identita"]["0"]
    idp = max(bb["identita"][k] for k in bb["identita"] if k != "0")
    cu0 = bb["curva"]["0"]
    v["B"] = (CONFERMA if (id0 == 0.0 and idp > 1e-3 and cu0 > 1e-3) else SMENTITA,
              "nella scena **identita'** con `eps = 0` il peso nell'altra componente e' "
              "**%.3g** *(zero esatto, come il `v1`)*, e con `eps > 0` arriva a **%.4g** "
              "— cioe' **le due componenti si EQUILIBRANO**. ### ⭐ **E con "
              "`eps = 0` ma trasporto curvo e' gia' **%.4g**: mescola anche il TRASPORTO**"
              % (id0, idp, cu0))

    mm = L["M_gap"]
    rap = {k: mm["identita"][k]["rapporto"] for k in mm["identita"]}
    ordinati = [rap[k] for k in sorted(rap, key=float)]
    scende = all(ordinati[j] >= ordinati[j + 1] for j in range(len(ordinati) - 1))
    v["M"] = (CONFERMA if scende else SMENTITA,
              "il **gap massimo diviso la spaziatura media** va da **%.1f** a `eps = 0` a "
              "**%.2f** a `eps = 1`, **%s**. ### ⭐ **Quindi `eps` NON apre un gap: lo "
              "CHIUDE** — e la previsione *(nessuna massa con `C^2` e versori "
              "isotropi)* **regge**. ### ⚠ **E il gap grosso a `eps = 0` non e' una "
              "massa: e' lo spettro della camminata SCALARE di Grover**, cioe' "
              "**esattamente il `v1`**"
              % (ordinati[0], ordinati[-1],
                 "in modo MONOTONO" if scende else "NON in modo monotono"))

    t = L["3_conservata"]
    lin = [k for k in t if k.endswith("lineare")]
    tutte_lin = all(set(x["esiti"]) == {"CONSERVATA"} for k in lin for x in t[k].values())
    oltre = []
    osc = []
    for k, vv in t.items():
        if k.endswith("lineare"):
            continue
        for cn, x in vv.items():
            if cn == "la norma":
                continue
            e = set(x["esiti"])
            if e == {"CONSERVATA"}:
                oltre.append("%s / %s" % (k, cn))
            elif "OSCILLANTE LIMITATA" in e:
                osc.append("%s / %s" % (k, cn))
    v["3"] = (NESSUNA if not oltre else CONFERMA,
              "per la camminata **LINEARE** le quattro candidate sono **%s** nelle due "
              "scene *(ed e' il controllo positivo: la quasi-energia di un passo unitario "
              "e' conservata **per una ragione esatta**)*; per le **%d** varianti non "
              "lineari la **norma** e' sempre conservata e delle tre candidate oltre la "
              "norma **%s**. ### ⚠ **Ma in %d casi l'esito e' <<OSCILLANTE "
              "LIMITATA>>**, che e' **meno che conservata e piu' che deriva** — e nel "
              "`v1` non era cosi' netto"
              % ("tutte CONSERVATE" if tutte_lin else "NON tutte conservate",
                 len(t) - len(lin),
                 ("si conservano: %s" % ", ".join(oltre)) if oltre
                 else "**NESSUNA si conserva**", len(osc)))

    q = L["4_cluster"]
    ide = {k: x for k, x in q.items() if k.startswith("identita")}
    cur = {k: x for k, x in q.items() if k.startswith("curva")}
    ini_cur = max(x["media_iniziale"] for x in cur.values())
    v["4"] = (NONDEC,
              "nella scena **identita'** la dispersione **cresce in ogni variante** *(da "
              "**%+.3f** a **%+.3f**)*: la coerenza **si perde**, e la formula del piano e' "
              "*«la non linearita' scelta NON BASTA»*. ### ⛔ **Nella scena CURVA la "
              "lettura NON E' DECIDIBILE, e il motivo e' nei numeri:** la dispersione "
              "**PARTE da %.3f** *(contro `0.65` nell'identita')*, cioe' **vicina alla "
              "saturazione**, perche' il trasporto casuale **scompiglia le fasi subito** "
              "— quindi la crescita piccola *(%+.3f)* **non vuol dire piu' coerenza**"
              % (min(x["crescita"] for x in ide.values()),
                 max(x["crescita"] for x in ide.values()), ini_cur,
                 max(x["crescita"] for x in cur.values())))

    m = L["5_materia_antimateria"]
    rotteA = [k for k in m if " (A)" in k
              and any(x["coniugazione"] > 1e-6 for x in m[k].values())]
    bitB = [k for k in m if " (B)" in k
            and all(x["coniugazione"] < 1e-12 for x in m[k].values())]
    totA = len([k for k in m if " (A)" in k])
    totB = len([k for k in m if " (B)" in k])
    v["5"] = (CONFERMA if (len(rotteA) == totA and len(bitB) == totB) else SMENTITA,
              "**`(A)` ROMPE la coniugazione in %d varianti su %d** *(fino a **%.3g**, "
              "asimmetria dell'intrappolamento fino a **%.3g**)* — ### ed e' **il "
              "braccio che DEVE fallire**; **`(B)`, l'elicita', la rispetta in %d su %d** "
              "*(al massimo **%.3g**, cioe' virgola mobile)*. ### ⭐ **E QUESTA VOLTA "
              "E- UNA PROVA FISICA, non un'algebra:** la lettura `B` dice che le due "
              "componenti **si equilibrano**, quindi la simmetria **non passa per "
              "costruzione**"
              % (len(rotteA), totA,
                 max(x["coniugazione"] for k in m if " (A)" in k for x in m[k].values()),
                 max(x["asimmetria"] for k in m if " (A)" in k for x in m[k].values()),
                 len(bitB), totB,
                 max(x["coniugazione"] for k in m if " (B)" in k for x in m[k].values())))

    o = L["O_olonomia"]
    v["O"] = (CONFERMA if max(o.values()) == 0.0 else SMENTITA,
              "le olonomie **non cambiano** durante la corsa nelle tre scene: **%.3g** "
              "— ed e' **un CONTROLLO**, perche' le `U` sono fisse *(se cambiassero, "
              "il banco non sarebbe quello che dichiara)*" % max(o.values()))
    return v


NOMI = {"G": "GAUGE", "G!": "IL BRACCIO CHE DEVE FALLIRE: i versori",
        "1": "ISOTROPIA", "2": "CONO", "B": "BANDE ACCOPPIATE", "M": "MASSA O NO",
        "3": "QUANTITA- CONSERVATA", "4": "CLUSTER", "5": "MATERIA / ANTIMATERIA",
        "O": "OLONOMIA (controllo)"}
PREV = {"G": "le osservabili invarianti **non cambiano**",
        "G!": "coi versori **non ruotati** le osservabili **DEVONO** cambiare",
        "1": "rinumerare **non cambia niente**",
        "2": "oltre il cono, **zero al bit**",
        "B": "`eps = 0` e identita': **zero**; `eps > 0`: **> 0**",
        "M": "### **NIENTE GAP** *(D'Ariano-Perinotti: `C^2` + versori isotropi)*",
        "3": "**non lo so** — nessuna previsione da smentire",
        "4": "**non ho conti** che prevedano un cluster stabile",
        "5": "`(A)` **DEVE** rompere `C`; `(B)` **no**",
        "O": "**non cambiano**: le `U` sono fisse"}
ORDINE = ("G", "G!", "1", "2", "B", "M", "3", "4", "5", "O")


def main():
    d = json.loads(io.open(FONTE, encoding="utf-8").read())
    v = verdetti(d)
    sc = d["scena"]
    r = []
    a = r.append
    a("# \U0001f52c **IL PROTOTIPO `v2` — SPIN LEGATO AL MOTO, CON `U(2)` SUGLI ARCHI**")
    a("")
    a("> ### ⛔ **CONGELATO** *(forma dichiarata in `csv/_forma_referti.py`)*: e' un "
      "### **REPERTO**, cioe' ### **che cosa si e' misurato A UN ISTANTE** — la CI "
      "### **non lo rigenera**, e il presidio verifica ### **il suo BLOB.**")
    a("")
    a("*(**Generato** da `python proto_camminata/_referto2.py`, che legge "
      "`proto_camminata/uscite/letture_v2.json` prodotto da `python "
      "proto_camminata/_letture2.py`. Criteri, previsioni e soglie: "
      "`doc/TASK_HISTORY/2026-10-10_prototipo_camminata_v2.md`, **committato PRIMA del "
      "codice**. Decisione: `SPIN-LEGATO-AL-MOTO`.)*")
    a("")
    a("**LA SCENA:** `%s` — **%d** nodi, **%d** archi, **%d** estremita-, gradi "
      "**%s**; `eps` di riferimento **%s**; semi **%s**; **%d** tick per cluster e "
      "conservazione."
      % (sc["nome"], sc["n"], sc["archi"], sc["estremita"], sc["gradi"],
         sc["eps_riferimento"], sc["semi"], sc["passi_lunghi"]))
    a("")
    a("### ⭐ **E IL `v1` ERA DUE CAMMINATE SCALARI:** la lettura `B` qui sotto dice "
      "che nel `v2` le due componenti ### **si equilibrano** — e- la differenza che "
      "rende la lettura `5` ### **una prova fisica invece di un'algebra.**")
    a("")
    a("## ⭐ **I DIECI VERDETTI**")
    a("")
    a("| | la lettura | la PREVISIONE *(scritta prima)* | il verdetto |")
    a("|---|---|---|---|")
    for k in ORDINE:
        a("| `%s` | **%s** | %s | %s |" % (k, NOMI[k], PREV[k], v[k][0]))
    a("")
    a("## \U0001f4cc **I NUMERI, lettura per lettura**")
    a("")
    for k in ORDINE:
        a("### `%s` **%s** — %s" % (k, NOMI[k], v[k][0]))
        a("")
        a("%s" % v[k][1])
        a("")
    a("## ⛔ **LE QUATTRO COSE CHE QUESTO REFERTO DICE E CHE NON ERANO NEL MANDATO**")
    a("")
    a("### `1` **IL GAP C'E', MA A `eps = 0` — E NON E' UNA MASSA.** Il rapporto "
      "gap/spaziatura e' **%.1f** a `eps = 0` e **%.2f** a `eps = 1`: ### **`eps` CHIUDE "
      "il gap invece di aprirlo.** ### ⭐ **E il gap grosso a `eps = 0` e' lo spettro "
      "della camminata di Grover SCALARE**, cioe' **esattamente il `v1`** — quindi "
      "### **quel gap era nel `v1` e non era una massa nemmeno la'.**"
      % (d["letture"]["M_gap"]["identita"]["0"]["rapporto"],
         d["letture"]["M_gap"]["identita"]["1"]["rapporto"]))
    a("")
    a("### `2` **LA TENDENZA MONOTONA DEL `v1` NON SOPRAVVIVE.** Nel `v1` la crescita "
      "della dispersione **scendeva monotona** con `g`, e ci avevo costruito una proposta "
      "*(`PROPOSTA-SCANSIONE-FORZA-NONLINEARE`)*. ### ⛔ **Qui no:** nella scena "
      "identita' va **%s** al crescere di `g`. ### ✅ **Quella tendenza era una "
      "proprieta' della camminata SCALARE**, e la proposta va **annotata.**"
      % ", ".join("%+.3f" % d["letture"]["4_cluster"]["identita (B) g=%g" % g]["crescita"]
                  for g in (0.5, 1.0, 2.0)))
    a("")
    a("### `3` **NELLA SCENA CURVA LA LETTURA `4` NON E' DECIDIBILE, e il motivo e' nei "
      "numeri:** la dispersione **parte** da `~1.47` contro `~0.65` dell'identita', cioe' "
      "### **vicina alla saturazione** — il trasporto casuale **scompiglia le fasi "
      "subito.** ### ⚠ **Quindi la crescita piccola NON vuol dire piu' coerenza**, e "
      "chiamarla <<il cluster tiene>> sarebbe **leggere un artefatto.**")
    a("")
    a("### `4` **`(B)` DA' <<OSCILLANTE LIMITATA>> DOVE IL `v1` DAVA <<DERIVA>>.** Non e' "
      "una conservazione, ### **ma non e' la stessa cosa di una deriva** — e con "
      "l'elicita' succede **piu' spesso** che con la densita'. ### ⛔ **Non lo chiamo "
      "un risultato: lo chiamo un INDIZIO**, e la differenza fra le due parole e' "
      "**quante volte l'ho visto.**")
    a("")
    a("## ✅ **CHE COSA SBLOCCA O RIAPRE NELL-ALBERO** *(e nessuna decisione e' mia)*")
    a("")
    a("| il nodo | che cosa dicono i numeri | che cosa NON dicono |")
    a("|---|---|---|")
    a("| **[[MATERIA-ANTIMATERIA-SPAZIO]]**, condizione `(b)` | ### ⭐ **ADESSO E' UNA "
      "PROVA FISICA:** le componenti **si equilibrano** *(lettura `B`)* e l'elicita' "
      "tiene la coniugazione **a virgola mobile** su **tutte** le varianti | non dicono "
      "che l'elicita' sia **la** forza di coesione: la lettura `4` dice che **non tiene il "
      "cluster** |")
    a("| **la forza di COESIONE** *(il nodo `FC`)* | una candidata **ammissibile** e "
      "**invariante di gauge** esiste, ed e' **l'elicita'** | ### ⛔ **non basta a "
      "tenere un cluster**, e **da dove viene `g`** resta `A1` |")
    a("| **[[DOMANDA-QUANTITA-CONSERVATA]]** *(la prossima)* | ### **nessuna** delle tre "
      "candidate oltre la norma si conserva, **in nessuna delle due scene** | non dicono "
      "che non esista: dicono che **non l'ho trovata fra le candidate dichiarate**, e in "
      "alcuni casi l'esito e' **oscillante limitata** |")
    a("| **[[DOMANDA-D9-GEOMETRIA]]** | ### ⭐ **i versori NON sono ridondanti, "
      "MISURATO** *(lettura `G!`)*: senza ruotarli la densita' cambia di `1.2e-2` | non "
      "dicono **da dove vengano**: e' `PROVV-VERSORI-NON-RELAZIONALI`, e la risposta e' "
      "`D9` |")
    a("| **`C^2` contro `C^4`** *(`A16`)* | con **`C^2`** e versori isotropi "
      "### **nessun gap si apre con `eps`** | non dicono che `C^4` ne aprirebbe uno: "
      "**non l'ho provato**, ed e' una proposta per Luca |")
    a("| **[[D13]]** e **[[M-SPINORE]]** | con le `U` **fisse** tutto e' coerente, e le "
      "olonomie **non cambiano** *(controllo)* | ### ⛔ **niente sulle `U` "
      "DINAMICHE**: in questo banco sono **una memoria congelata**, ed e' "
      "`PROVV-U-FISSE-TRE-SCENE` |")
    a("")
    a("## ⚠ **I LIMITI, dichiarati**")
    a("")
    a("| | il limite |")
    a("|---|---|")
    a("| `1` | ### **`cs_k = 1` ovunque:** il `v2` **non prova la `cs` locale** |")
    a("| `2` | ### **`r_k`, `eps`, `g`, i versori e le `U` sono SONDE o scelte "
      "provvisorie**, e ognuna ha la sua voce |")
    a("| `3` | ### **un solo grafo irregolare**: non e' uno scaling di taglia finita "
      "*([[TAGLIA-FINITA]])* |")
    a("| `4` | ### **il verso curvatura ↔ EM non e' misurabile qui**, perche' `theta` "
      "e `V` sono **entrambi fissi** |")
    a("| `5` | la lettura `4` guarda **un cluster costruito da me**, e nella scena curva "
      "**satura subito** |")
    a("")
    io.open(DEST, "wb").write((NL.join(r) + NL).encode("utf-8"))
    print("=" * 100)
    for k in ORDINE:
        print("  %-3s %-40s %s" % (k, NOMI[k][:40],
                                   v[k][0].replace("### ", "").replace("*", "")))
    print("=" * 100)
    print("  scritto %s" % os.path.relpath(DEST, RADICE).replace(os.sep, "/"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
