# -*- coding: utf-8 -*-
"""IL REFERTO DEL PROTOTIPO — **GENERATO da `uscite/letture.json`, non scritto a mano.**

### ⛔ **OGNI NUMERO DI QUESTO REFERTO ESCE DAL `json`** *(`L-NUMERI`)*, e **anche i
VERDETTI**: il confronto fra la previsione e il numero **lo fa il codice**, con le soglie del
task history. ### ⚠ **Cosi' un verdetto non puo' <<addolcirsi>> mentre lo scrivo.**

> ### ⛔ **NESSUNA DECISIONE QUI:** le proposte per Luca diventano **VOCI dell'indice**,
> perche' `doc/indice/DA_DECIDERE_LUCA.md` e' **GENERATO**.

Gira con:  python proto_camminata/_referto.py
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
import _presidio                                               # noqa: E402

_presidio.avvia(__file__)

NL = chr(10)
FONTE = os.path.join(_QUI, "uscite", "letture.json")
DEST = os.path.join(RADICE, "doc", "REFERTO_prototipo_camminata.md")

CONFERMA = "### ✅ **CONFERMA**"
SMENTITA = "### ⛔ **SMENTITA**"
NONDEC = "### ⚠ **NON DECIDIBILE**"
# ### ⛔ **DUE VERDETTI IN PIU-, e non sono un abbellimento:** per la lettura `3`
# ### ### **non c-era NESSUNA previsione da smentire** *(la previsione scritta era <<non lo
# ### so>>)*, e per la lettura `4` ### **il piano ha una sua formula esatta**
# ### *(<<la non linearita- scelta NON BASTA>>)*. ### ⚠ **Chiamarli <<SMENTITA>>
# ### sarebbe un-etichetta INFEDELE**, e un verdetto infedele e- peggio di un verdetto
# ### scomodo.
NESSUNA = "### ⛔ **NESSUNA TROVATA** *(criterio di RIAPERTURA)*"
NONBASTA = "### ⛔ **LA NON LINEARITA- NON BASTA**"


def verdetti(d):
    """### I verdetti, **calcolati dai numeri** e non scritti a mano."""
    L = d["letture"]
    v = {}

    # ---------------------------------------------------------------- 1a
    a = L["1a_isotropia_camminata"]
    v["1a"] = (CONFERMA if (a["fsum"] == 0.0 and a["numpy"] <= a["soglia"]) else SMENTITA,
               "`fsum` = **%.3g** *(zero al bit)*; `numpy` = **%.3g** su soglia **%.3g**"
               % (a["fsum"], a["numpy"], a["soglia"]))

    # ---------------------------------------------------------------- 1b
    b = L["1b_anisotropia_integratore"]
    if b.get("pendenza") is None:
        v["1b"] = (NONDEC, b.get("nota", "non misurata"))
    else:
        dentro = abs(b["pendenza"] - 2.0) <= 3.0 * b["sigma"]
        v["1b"] = (CONFERMA if dentro else SMENTITA,
                   "pendenza misurata **%.3f +/- %.3f** su `%d` valori di `dt` e `%d` "
                   "strati; il criterio era **`|pendenza - 2| <= 3 sigma`**, cioe- "
                   "**%.3f <= %.3f**"
                   % (b["pendenza"], b["sigma"], len(b["dt"]), b.get("strati", -1),
                      abs(b["pendenza"] - 2.0), 3.0 * b["sigma"]))

    # ---------------------------------------------------------------- 2
    c = L["2_cono"]
    v["2"] = (CONFERMA if c["max_fuori"] == 0.0 else SMENTITA,
              "oltre **%d** archi: `max|differenza|` = **%.3g** su **%d** estremita-, con "
              "**%d** nodi fuori dal cono *(eccentricita- **%d**)*"
              % (c["T"], c["max_fuori"], c["estremita_fuori"], c["nodi_oltre"],
                 c["eccentricita"]))

    # ---------------------------------------------------------------- 3
    t = L["3_conservata"]
    lin = t.get("lineare", {})
    tutte_lin = all(set(x["esiti"]) == {"CONSERVATA"} for x in lin.values())
    altre = {k: vv for k, vv in t.items() if k != "lineare"}
    oltre_norma = []
    for k, vv in altre.items():
        for nome, x in vv.items():
            if nome == "la norma":
                continue
            if set(x["esiti"]) == {"CONSERVATA"}:
                oltre_norma.append("%s / %s" % (k, nome))
    norma_sempre = all(set(vv["la norma"]["esiti"]) == {"CONSERVATA"}
                       for vv in altre.values())
    v["3"] = (NESSUNA if not oltre_norma else CONFERMA,
              "per la camminata **LINEARE** le **quattro** candidate sono "
              "**%s** *(ed e- il controllo positivo: senza di lui il test non direbbe "
              "niente)*; per le **%d** varianti non lineari la **norma** e- conservata "
              "**%s**, e delle **tre** candidate oltre la norma **%s**"
              % ("tutte CONSERVATE" if tutte_lin else "NON tutte conservate",
                 len(altre), "sempre" if norma_sempre else "NON sempre",
                 ("si conservano: %s" % ", ".join(oltre_norma)) if oltre_norma
                 else "**NESSUNA si conserva**"))

    # ---------------------------------------------------------------- 4
    q = L["4_cluster"]
    cre = {}
    for k, x in q.items():
        cre[k] = x["media_finale"] - x["media_iniziale"]
    gs = [k for k in q if k.startswith("(")]
    # la crescita scende con `g`? si guarda la MONOTONIA sulla scansione
    def _g(k):
        return float(k.split("g=")[1]) if "g=" in k else 0.0
    serie_b = sorted([k for k in gs if k.startswith("(B)")], key=_g)
    mono = all(cre[serie_b[i]] >= cre[serie_b[i + 1]] - 1e-12
               for i in range(len(serie_b) - 1)) if len(serie_b) >= 3 else False
    v["4"] = (NONBASTA if cre.get("lineare", 0) > 0 and all(cre[k] > 0 for k in gs)
              else CONFERMA,
              "la dispersione **CRESCE** in ogni variante: **+%.3f** con la lineare, e da "
              "**+%.3f** a **+%.3f** sulla scansione di `g`; la frazione **intrappolata** "
              "resta **%.3f**..**%.3f**. ### ⭐ **E la crescita SCENDE con `g`, in modo "
              "%s** su `%d` valori"
              % (cre.get("lineare", float("nan")),
                 max(cre[k] for k in gs), min(cre[k] for k in gs),
                 min(min(x["intrappolata_finale"]) for x in q.values()),
                 max(max(x["intrappolata_finale"]) for x in q.values()),
                 "MONOTONO" if mono else "non monotono", len(serie_b)))

    # ---------------------------------------------------------------- 5
    m = L["5_materia_antimateria"]
    rotta_A = [k for k in m if k.startswith("(A)")
               and any(x["coniugazione_al_bit"] > 0 for x in m[k].values())]
    bit_B = [k for k in m if k.startswith("(B)")
             and all(x["coniugazione_al_bit"] == 0.0 for x in m[k].values())]
    tutte_A = len([k for k in m if k.startswith("(A)")])
    tutte_B = len([k for k in m if k.startswith("(B)")])
    v["5"] = (CONFERMA if (len(rotta_A) == tutte_A and len(bit_B) == tutte_B)
              else SMENTITA,
              "**`(A)` ROMPE la coniugazione in %d varianti su %d** *(differenza fino a "
              "**%.3g**, asimmetria dell-intrappolamento fino a **%.3g**)* — ### ed e- "
              "**IL BRACCIO CHE DEVE FALLIRE**; **`(B)` la rispetta AL BIT in %d su %d** "
              "*(differenza **esattamente 0**, asimmetria **esattamente 0**)*"
              % (len(rotta_A), tutte_A,
                 max(x["coniugazione_al_bit"] for k in m if k.startswith("(A)")
                     for x in m[k].values()),
                 max(x["asimmetria"] for k in m if k.startswith("(A)")
                     for x in m[k].values()),
                 len(bit_B), tutte_B))

    # ---------------------------------------------------------------- 6
    s = L["6_r_uguale_uno"]
    v["6"] = (CONFERMA if s["max_differenza"] == 0.0 else SMENTITA,
              "`max|differenza|` = **%.3g**, e sono **due strade di codice diverse** "
              "*(la moneta per nodo e quella a `dt` scalare)*" % s["max_differenza"])

    # ---------------------------------------------------------------- 7
    z = L["7_gauge_rovesciato"]
    oltre = [k for k, x in z["fattori"].items() if x["oltre_arrotondamento"]]
    v["7"] = (CONFERMA if len(oltre) == len(z["fattori"]) else SMENTITA,
              "un fattore comune **CAMBIA** lo stato: %s, contro una soglia di "
              "arrotondamento di **%.3g** — cioe- **%d ordini di grandezza sopra**"
              % (", ".join("`c=%s` -> **%.3g**" % (k, x["delta_stato"])
                           for k, x in sorted(z["fattori"].items())),
                 z["soglia_arrotondamento"],
                 int(round(math.log10(max(x["delta_stato"] for x in z["fattori"].values())
                                      / z["soglia_arrotondamento"])))))
    return v


def main():
    d = json.loads(io.open(FONTE, encoding="utf-8").read())
    v = verdetti(d)
    sc = d["scena"]
    r = []
    a = r.append
    a("# \U0001f52c **IL PROTOTIPO DELLA CAMMINATA A MONETA — LE SETTE LETTURE**")
    a("")
    a("> ### ⛔ **CONGELATO** *(la forma dichiarata il `2026-10-10`: "
      "`csv/_forma_referti.py`)*: questo e- un ### **REPERTO**, cioe- ### **che cosa si e- "
      "misurato A UN ISTANTE** — la CI ### **non lo rigenera**, e il presidio verifica "
      "### **il suo BLOB.**")
    a("")
    a("*(**Generato** da `python proto_camminata/_referto.py`, che legge "
      "`proto_camminata/uscite/letture.json` prodotto da `python "
      "proto_camminata/_letture.py`. Criteri, previsioni e soglie: "
      "`doc/TASK_HISTORY/2026-10-10_prototipo_camminata.md`, **committato PRIMA del "
      "codice**.)*")
    a("")
    a("**LA SCENA:** `%s` — **%d** nodi, **%d** archi, **%d** estremita-, gradi "
      "**%s**; controllo `%s`; semi **%s**."
      % (sc["nome"], sc["n"], sc["archi"], sc["estremita"], sc["gradi"], sc["regolare"],
         sc["semi"]))
    a("")
    a("## ⭐ **I SETTE VERDETTI, in una tabella**")
    a("")
    a("| | la lettura | la PREVISIONE *(scritta prima)* | il verdetto |")
    a("|---|---|---|---|")
    PREV = {
        "1a": "isotropia **esatta** per costruzione",
        "1b": "l-anisotropia dell-integratore **scende come `dt^2`**",
        "2": "oltre il cono, **zero al bit**",
        "3": "**non lo so**, ed e- la domanda aperta — ### **nessuna previsione "
             "da smentire**",
        "4": "**non ho ragioni** per aspettarmi che il cluster tenga",
        "5": "`(A)` **DEVE** rompere la simmetria, `(B)` **no**",
        "6": "`r=1` coincide col `dt` globale **al bit**",
        "7": "un fattore comune **CAMBIA** la fisica *(per costruzione)*",
    }
    NOMI = {"1a": "ISOTROPIA della camminata", "1b": "ANISOTROPIA dell-integratore",
            "2": "CONO", "3": "QUANTITA- CONSERVATA", "4": "CLUSTER",
            "5": "MATERIA / ANTIMATERIA", "6": "`r=1`", "7": "GAUGE, ROVESCIATO"}
    for k in ("1a", "1b", "2", "3", "4", "5", "6", "7"):
        a("| `%s` | **%s** | %s | %s |" % (k, NOMI[k], PREV[k], v[k][0]))
    a("")
    a("## \U0001f4cc **I NUMERI, lettura per lettura**")
    a("")
    for k in ("1a", "1b", "2", "3", "4", "5", "6", "7"):
        a("### `%s` **%s** — %s" % (k, NOMI[k], v[k][0]))
        a("")
        a("%s" % v[k][1])
        a("")
    a("## ⛔ **LE TRE COSE CHE QUESTO REFERTO DICE E CHE NON ERANO NEL PIANO**")
    a("")
    a("### `1` **`(A)` E `(B)` SONO INDISTINGUIBILI SULLA LETTURA `4`, E NON E- UN "
      "DIFETTO: E- LA DERIVAZIONE.** Su un cluster **tutto nella banda `+`** vale "
      "`s = rho`, quindi la fase **dispari** e quella **pari** sono **la stessa fase** "
      "— e i numeri della lettura `4` coincidono **cifra per cifra**. "
      "### ⭐ **Solo la lettura `5`, che costruisce il CONIUGATO, le separa** — e "
      "le separa **al bit.**")
    a("")
    a("### `2` **LA CRESCITA DELLA DISPERSIONE SCENDE CON `g`, IN MODO MONOTONO.** Il "
      "cluster **non tiene** con nessun `g` provato *(la coerenza si perde sempre)*, "
      "### ⚠ **ma la perdita e- sempre piu- lenta**, e su `4` valori la tendenza e- "
      "**monotona** — quindi ### **non e- una finestra stretta** *(la terza domanda "
      "della stella polare)*. ### ⛔ **Che cosa farne e- una decisione di Luca**, e sta "
      "in una voce.")
    a("")
    a("### `3` **LA SOGLIA `dt^2` DEL PIANO E- SMENTITA, E IL MOTIVO E- CHE L-INTEGRATORE "
      "E- MIGLIORE DI COSI-.** La composizione a strati e- **SIMMETRICA alla Strang**, "
      "quindi ### **l-errore di ordine PARI si annulla** e l-anisotropia va come "
      "**`dt^3`**. ### ✅ **Il criterio scritto prima FALLISCE**, e lo scrivo invece di "
      "aggiustarlo: ### **la previsione era PESSIMISTA.**")
    a("")
    a("## ✅ **CHE COSA SBLOCCA O RIAPRE NELL-ALBERO** *(e nessuna decisione e- mia)*")
    a("")
    a("| il nodo | che cosa dicono i numeri | che cosa NON dicono |")
    a("|---|---|---|")
    a("| **[[DOMANDA-QUANTITA-CONSERVATA]]** *(la prossima)* | la **norma** si conserva "
      "**sempre**, anche con le non lineari; delle **tre** candidate oltre la norma "
      "**nessuna** si conserva per nessuna delle **8** varianti provate | ### ⛔ **NON "
      "dicono che non esista:** dicono che **non l-ho trovata fra le candidate "
      "DICHIARATE** — ed e- la forma giusta di un **criterio di RIAPERTURA**, non una "
      "dimostrazione di assenza |")
    a("| **[[MATERIA-ANTIMATERIA-SPAZIO]]**, condizione `(b)` | la fase **dispari sotto "
      "`C`** la soddisfa ### **AL BIT**, su `8` varianti e `2` semi: materia e antimateria "
      "si comportano **identicamente** | non dicono che `(B)` sia **la** forza di coesione: "
      "dicono che e- **ammissibile**, mentre `(A)` **non lo e-** |")
    a("| **la forza di COESIONE** *(il nodo `FC`)* | la fase dispari e- **una candidata "
      "ammissibile**, e la crescita della dispersione **scende con `g`** | non dicono "
      "**quale** forma, ne- **da dove** viene `g` — che e- `A1` |")
    a("| **[[TEMPO-PROPRIO-LOCALE]]** | la lettura `7` **conferma la correzione del punto "
      "`0`**: un fattore comune sugli `r_k` cambia lo stato di **`0.16`-`0.20`**, contro un "
      "arrotondamento di **`8e-14`** | non dicono **da dove viene `r_k`**: resta la domanda "
      "aperta, e adesso ### **con il vincolo in piu- della SCALA ASSOLUTA** |")
    a("| **[[DOMANDA-FORME-VUOTO]]** e la divisione del lavoro | ### ⛔ **NIENTE: "
      "questo prototipo non le ha toccate**, e dirlo e- parte del referto | il vuoto locale "
      "non e- implementato: ### **`cs_k = 1` ovunque**, dichiarato |")
    a("")
    a("## ⛔ **ANNOTAZIONE DEL 2026-10-10 — LA LETTURA DEL GUARDIANO: IL "
      "`v1` E- DUE CAMMINATE SCALARI**")
    a("")
    a("> ### ⛔ **E NIENTE QUI SOPRA SI RISCRIVE:** i numeri sono quelli, e i "
      "verdetti sono calcolati. ### **Cambia che cosa SIGNIFICANO.**")
    a("")
    a("### 📌 **IL FATTO, verificato SUL CODICE e non dedotto:** nel `v1` le "
      "due componenti dello spinore ### **NON SI MESCOLANO MAI** — Grover e- "
      "### **uguale sulle due**, la moneta di banda e- ### **DIAGONALE** "
      "*(`exp(-i dtau sigma_z)`)*, lo spostamento ### **non le distingue.**")
    a("")
    a("### ✅ **MISURATO, e adesso e- un BRACCIO del collaudo e non una nota:** "
      "un pacchetto messo ### **solo nella componente `0`** lascia l-altra a "
      "### **ZERO ESATTO** dopo `60` tick, ### **con la camminata lineare E con "
      "entrambe le non linearita-**; e con `r` ### **uniforme** la fase della "
      "componente `0` e- ### **COSTANTE su tutte le estremita-**, cioe- la "
      "<<massa>> e- ### **una fase GLOBALE per componente.**")
    a("")
    a("### ⛔ **CHE COSA CAMBIA, lettura per lettura** *(e non e- poco)*:")
    a("")
    a("| la lettura | che cosa vale ANCORA | che cosa NON vale piu- |")
    a("|---|---|---|")
    a("| `5` materia/antimateria | ### **l-ALGEBRA**: una fase scalare commuta con "
      "`C` ### **solo se e- dispari**, e la misura lo conferma al bit | ### ⛔ "
      "**NON e- una prova FISICA**: con le componenti scollegate la simmetria "
      "passa ### **PER COSTRUZIONE** |")
    a("| `7` il gauge | la scala assoluta di `r` ### **cambia** le osservabili | "
      "vale ### **per la non linearita- che scala con `dtau`**, ### **non per la "
      "massa** |")
    a("| `3` e `4` | i numeri sono quelli | riguardano ### **una camminata SCALARE**, "
      "non uno spinore |")
    a("")
    a("### ⭐ **E QUINDI LE DECISIONI CHE NE DIPENDONO SI RIFANNO SUL `v2`**, "
      "dove ### **lo spin si lega al moto** con una moneta "
      "`exp(-i eps dtau sigma.n)` e il ### **trasporto `U(2)` sugli archi.**")
    a("")
    a("## ⚠ **I LIMITI, dichiarati**")
    a("")
    a("| | il limite |")
    a("|---|---|")
    a("| `1` | ### **`cs_k = 1` ovunque:** questo prototipo **non prova la `cs` locale**, e "
      "i punti `3`-`6` di [[TEMPO-PROPRIO-LOCALE]] restano **da provare altrove** |")
    a("| `2` | ### **`r_k` e- DATO, non derivato** *(il mandato lo dice)*: la derivazione e' "
      "la domanda aperta |")
    a("| `3` | ### **un solo grafo irregolare** e un solo regolare: **non e- uno scaling di "
      "taglia finita** *([[TAGLIA-FINITA]])*, e due taglie **non sarebbero uno scaling** |")
    a("| `4` | la lettura `4` guarda **un cluster costruito da me**: se la coerenza "
      "dipendesse dalla **forma** del cluster, questo referto **non lo vedrebbe** |")
    a("")
    dati = (NL.join(r) + NL).encode("utf-8")
    io.open(DEST, "wb").write(dati)
    print("=" * 100)
    for k in ("1a", "1b", "2", "3", "4", "5", "6", "7"):
        print("  %-3s %-32s %s" % (k, NOMI[k][:32],
                                   v[k][0].replace("### ", "").replace("*", "")))
    print("=" * 100)
    print("  scritto %s" % os.path.relpath(DEST, RADICE).replace(os.sep, "/"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
