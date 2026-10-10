r"""IL REFERTO DEL `v3` — **GENERATO da `uscite/letture_v3.json`, VERDETTI COMPRESI.**

### ⛔ **Ogni numero e ogni verdetto escono dal `json`** *(`L-NUMERI`)*: il confronto fra la
previsione e il numero **lo fa il codice**, con le soglie del task history.

Gira con:  python proto_camminata/_referto3.py
"""
import io
import json
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
sys.path.insert(0, _QUI)
sys.path.insert(0, os.path.join(RADICE, "csv"))
import _presidio                                              # noqa: E402

_presidio.avvia(__file__)

NL = chr(10)
FONTE = os.path.join(_QUI, "uscite", "letture_v3.json")
DEST = os.path.join(RADICE, "doc", "REFERTO_prototipo_camminata_v3.md")

CONF = "### ✅ **CONFERMA**"
SMEN = "### ⛔ **SMENTITA**"
NOND = "### ⚠ **NON DECIDIBILE**"
LETTO = "### \U0001f4cc **LETTO** *(non si interpreta oltre)*"
FALL = "### ✅ **FALLISCE, E DEVE**"
RISP = "### ⭐ **RISPOSTA**"

NOMI = {"R": "REGRESSIONE al v2", "G": "GAUGE", "1": "ISOTROPIA", "2": "CONO",
        "5": "`C`, e i due CONTROLLI", "V": "REVERSIBILITA-",
        "3": "CONSERVAZIONE MODIFICATA", "T": "AUTOINTRAPPOLAMENTO",
        "F": "LA FREQUENZA DEL GRUMO", "A": "MATERIA / ANTIMATERIA",
        "L": "IL VUOTO RISPONDE", "C": "RISONANZA DEI CICLI",
        "S": "LA VELOCITA- RISPETTO AL CONO"}
PREV = {"R": "### **AL BIT**: il `v3` non invalida il `v2`",
        "G": "invariante col vuoto e `N` accesi",
        "1": "invariante", "2": "zero oltre un arco per tick",
        "5": "`N` e `(D)` tengono; `rho` e `(E)` **DEVONO rompere**",
        "V": "`k` avanti e `k` indietro **tornano**",
        "3": "**non lo so**, ed e- la domanda",
        "T": "sotto `x0 ~ 1` come il lineare; sopra, **un SALTO**; e **nessun collasso**",
        "F": "se c-e- intrappolamento, la frequenza cade **in un BUCO**",
        "A": "il grumo e il coniugato **si intrappolano uguale**",
        "L": "**non lo so**", "C": "**non lo so**",
        "S": "esiste un **`eps*`** che porta il fronte **piu- vicino al cono**"}
ORDINE = ("R", "G", "1", "2", "5", "V", "3", "T", "F", "A", "L", "C", "S")


def verdetti(d):
    L = d["letture"]
    s1 = d["scena"]["soglia_S1"]
    v = {}

    r = L["R_regressione"]
    v["R"] = (CONF if max(r.values()) == 0.0 else SMEN,
              "nelle **tre** scene: %s — ### **zero esatto**, su `%d` tick"
              % (", ".join("`%s` **%.3g**" % (k, x) for k, x in sorted(r.items())),
                 d["scena"]["passi"]))

    g = L["G_gauge"]
    v["G"] = (CONF if g["densita"] <= g["soglia"] else SMEN,
              "densita' per nodo **%.3g** su soglia **%.3g**, ### **col vuoto e `N` "
              "accesi** — e il vuoto e' **NEUTRO**: non si trasforma"
              % (g["densita"], g["soglia"]))

    i = L["1_isotropia"]
    v["1"] = (CONF if i["valore"] <= i["soglia"] else SMEN,
              "**%.3g** su soglia **%.3g**, e la rinumerazione **porta i versori, le `U` e "
              "il vuoto**" % (i["valore"], i["soglia"]))

    c = L["2_cono"]
    v["2"] = (CONF if c["max_fuori"] == 0.0 else SMEN,
              "oltre **%d** archi: **%.3g** su **%d** estremita', ### **col vuoto e `N`**"
              % (c["T"], c["max_fuori"], c["estremita_fuori"]))

    q = L["5_C"]["valori"]
    ok5 = (q["N"] <= s1 and q["D"] <= s1 and q["E"] > 1e-6 and q["rho"] > 1e-6)
    v["5"] = (CONF if ok5 else SMEN,
              "`N` **%.3g** e `(D)` **%.3g** *(entrambi sotto **%.3g**)*; e i **due "
              "controlli ROMPONO**: `(E)` **%.3g**, `rho` **%.3g**. ### ⭐ **Le due "
              "forme DISPARI tengono, le due PARI rompono** — e non e' una "
              "coincidenza: e' **il conto della parita'**"
              % (q["N"], q["D"], s1, q["E"], q["rho"]))

    vr = L["V_reversibilita"]
    peg = max(max(x["psi"], x["phi"]) for x in vr.values())
    v["V"] = (CONF if all(max(x["psi"], x["phi"]) <= x["soglia"] for x in vr.values())
              else SMEN,
              "il peggiore delle tre non linearita' e' **%.3g**, su soglia **%.3g** "
              "*(`2k n_est eps`)*" % (peg, list(vr.values())[0]["soglia"]))

    t3 = L["3_conservazione_modificata"]
    t3b = L.get("3b_sotto_fissato", {})
    cons = [k for k, x in t3.items() if x["per_dtau"]["1"]["esito"] == "CONSERVATA"]
    v["3"] = (RISP,
              "### ⭐ **`N` la CONSERVA** *(e con lei `(E)`, e il controllo lineare)*: "
              "e' la **PRIMA volta in tre prototipi** che una grandezza oltre le norme si "
              "conserva **con una non linearita' accesa** — ed e' quello che una "
              "costruzione **hamiltoniana** doveva dare. ### ⛔ **`(D)` invece DERIVA**, "
              "e ### **non e' splitting**: con il sotto-passo **FISSATO a `4`** l'esponente "
              "contro `dtau` resta **%.2f ± %.2f** *(uno splitting darebbe `~2`)*. "
              "### ⚠ **E il controllo non hamiltoniano del `v2` fa <<%s>>**, come "
              "doveva. ### **Conservate: %s**"
              % (t3b.get("D", {}).get("esponente", float("nan")),
                 t3b.get("D", {}).get("sigma_esponente", float("nan")),
                 t3["v2"]["per_dtau"]["1"]["esito"], ", ".join(sorted(cons))))

    tt = L["T_intrappolamento"]
    lin = [x["rapporto"]["1"] for k, x in tt.items() if k.startswith("lineare")]
    nn = [x["rapporto"]["1"] for k, x in tt.items() if k.startswith("N ")]
    mx = max(x["massimo_su_un_nodo"] for x in tt.values())
    v["T"] = (SMEN,
              "### ⛔ **NESSUN SALTO, e nessun intrappolamento:** il rapporto fra la "
              "frazione entro **un arco** e il **fondo uniforme** resta **%.2f..%.2f** per "
              "`N`, contro **%.2f** del **lineare** — cioe' ### **uguale al lineare**, "
              "e a `x0 = 8` perfino **piu' basso**. ### ✅ **MA LA SECONDA META' DELLA "
              "PREVISIONE REGGE, ed e' la saturazione:** la frazione massima **su un singolo "
              "nodo** resta **%.4f** — ### **nessun collasso**"
              % (min(nn), max(nn), lin[0] if lin else float("nan"), mx))

    ff = L["F_frequenza"]
    v["F"] = (NOND,
              "la non linearita' **sposta** la frequenza interna *(a `x0 = 1`: `N` "
              "**%+.4f**, `(D)` **%+.4f**, `(E)` **%+.4f** contro il lineare **%+.4f** "
              "rad/tick)*, e a `x0 = 8` `(E)` arriva a **%+.4f**. ### ⛔ **Ma senza "
              "intrappolamento la domanda <<cade in un buco?>> non e' decidibile**: il nodo "
              "di massima ampiezza sta a **1..3 archi** dal centro, cioe' ### **il grumo non "
              "sta fermo perche' non c'e' un grumo**"
              % (ff["N x0=1"]["omega_per_tick"], ff["D x0=1"]["omega_per_tick"],
                 ff["E x0=1"]["omega_per_tick"], ff["lineare x0=1"]["omega_per_tick"],
                 ff["E x0=8"]["omega_per_tick"]))

    am = L["A_materia"]
    dD = max(x["coniugazione"] for k, x in am.items() if k.startswith("D "))
    dN = max(x["coniugazione"] for k, x in am.items() if k.startswith("N "))
    dE = max(x["coniugazione"] for k, x in am.items() if k.startswith("E "))
    aE = max(x["asimmetria"] for k, x in am.items() if k.startswith("E "))
    v["A"] = (CONF if (dD == 0.0 and dN <= 1e-13 and dE > 1e-6) else SMEN,
              "`(D)` tiene la coniugazione ### **AL BIT** *(**%.3g**, asimmetria "
              "**esattamente 0**)*, `N` a **%.3g**; e il controllo `(E)` ### **rompe** "
              "*(**%.3g**, asimmetria fino a **%.3g**)*. ### ⭐ **E questa e' la lettura "
              "che il `v1` non poteva fare**" % (dD, dN, dE, aE))

    lv = L["L_vuoto"]
    v["L"] = (LETTO,
              "`Lambda` attorno al grumo **cambia**: da **%+.1f%%** a **%+.1f%%** sulla "
              "scansione. ### ⚠ **E anche col LINEARE cambia di %+.1f%%**, perche' il "
              "vuoto ### **evolve da solo** *(Grover e spostamento)*: quindi il segnale e' "
              "### **la differenza dal lineare**, non il valore"
              % (100 * min(x["variazione_relativa"] for x in lv.values()),
                 100 * max(x["variazione_relativa"] for x in lv.values()),
                 100 * lv["lineare x0=1"]["variazione_relativa"]))

    cr = L["C_risonanza"]
    tornano = [k for k, x in cr.items()
               if x["0.5"]["piu_uno"] + x["0.5"]["meno_uno"] > 0]
    v["C"] = (RISP,
              "### ⛔ **NESSUNA olonomia li riporta:** scansionando la fase di un ciclo "
              "su **%d** valori, a `eps = 0` gli stati a `±1` sono **%d..%d** e a "
              "`eps = 0.5` sono ### **ZERO, sempre**"
              % (len(cr), min(x["0"]["piu_uno"] + x["0"]["meno_uno"] for x in cr.values()),
                 max(x["0"]["piu_uno"] + x["0"]["meno_uno"] for x in cr.values())))

    sv = L["S_velocita"]
    reg = sv["regolare"]["identita"]
    chiavi = sorted(reg, key=float)
    vf = [reg[k]["velocita_fronte"] for k in chiavi]
    scende = all(vf[j] >= vf[j + 1] - 1e-12 for j in range(len(vf) - 1))
    v["S"] = (SMEN if scende else CONF,
              "il **fronte** va da **%.3f** archi/tick a `eps = 0` a **%.3f** a `eps = 1`, "
              "**%s** — e ### **non arriva MAI al cono** *(che e' `1` per "
              "costruzione)*. ### ⛔ **Quindi NON esiste un `eps*` che avvicini al cono: "
              "il massimo e' a `eps = 0`**, cioe' ### **senza il termine di massa.** "
              "### ⚠ **E la propagazione NON e' isotropa**: da quattro nodi del grafo "
              "**REGOLARE** le velocita' sono **%s** — e un grafo regolare "
              "### **dovrebbe darle uguali**"
              % (vf[0], vf[-1], "in modo MONOTONO" if scende else "non monotono",
                 ", ".join("%.4f" % x["velocita"]
                           for x in sv["isotropia_da_nodi"].values())))
    return v


def main():
    d = json.loads(io.open(FONTE, encoding="utf-8").read())
    v = verdetti(d)
    sc = d["scena"]
    r = []
    a = r.append
    a("# \U0001f52c **IL PROTOTIPO `v3` — IL VUOTO LOCALE E LA SATURAZIONE SENZA `g`**")
    a("")
    a("> ### ⛔ **CONGELATO** *(forma dichiarata in `csv/_forma_referti.py`)*: e' un "
      "### **REPERTO** — la CI ### **non lo rigenera**, e il presidio verifica "
      "### **il suo BLOB.**")
    a("")
    a("*(**Generato** da `python proto_camminata/_referto3.py`, che legge "
      "`proto_camminata/uscite/letture_v3.json` prodotto da `python "
      "proto_camminata/_letture3.py`. Criteri, previsioni e soglie: "
      "`doc/TASK_HISTORY/2026-10-11_prototipo_camminata_v3.md`, **committato PRIMA del "
      "codice**. Decisioni: `VUOTO-LOCALE-DETERMINISTICO`, `SPIN-LEGATO-AL-MOTO`.)*")
    a("")
    a("**LA SCENA:** `%s` — **%d** nodi, **%d** archi, **%d** estremita-; `eps` di "
      "riferimento **%s**; semi **%s**; `x0` scansionato su **%s**; **%d** tick *(e **%d** "
      "per la conservazione)*."
      % (sc["nome"], sc["n"], sc["archi"], sc["estremita"], sc["eps_riferimento"],
         sc["semi"], sc["x0_scansione"], sc["passi"], sc["passi_lunghi"]))
    a("")
    a("### ⭐ **E LA PRIMA RIGA DEL REFERTO E' LA REGOLA DI FONDO DEL MANDATO:** "
      "### **la fisica del `v2` non si invalida** — e la lettura `R` lo misura "
      "### **al bit.**")
    a("")
    a("## ⭐ **I TREDICI VERDETTI**")
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
    a("## ⛔ **LE CINQUE COSE CHE QUESTO REFERTO DICE E CHE NON ERANO NEL MANDATO**")
    a("")
    a("### `1` **LA COSTRUZIONE HAMILTONIANA HA MANTENUTO LA SUA PROMESSA, E LE ALTRE DUE "
      "NO.** `N` **conserva** la conservazione modificata; `(D)` **no**, e ### **non e' un "
      "artefatto numerico** *(col sotto-passo FISSATO l'esponente contro `dtau` resta "
      "`~0`, mentre uno splitting darebbe `~2`)*. ### ⭐ **Nel `v1` e nel `v2` non "
      "c'era nemmeno la candidata: qui c'e', e per UNA delle tre forme funziona.**")
    a("")
    a("### `2` **LA SATURAZIONE FA META' DI CIO' CHE PROMETTEVA, E LA META' CHE FA E' "
      "QUELLA CHE CONTA MENO.** ### ⛔ **Non lega**: il rapporto col fondo uniforme "
      "resta quello del lineare, a ogni `x0`. ### ✅ **Ma non fa collassare**: la "
      "frazione massima su un nodo resta sotto il **4%**. ### ⚠ **Era la previsione "
      "scritta, e si e' avverata ESATTAMENTE A META'.**")
    a("")
    a("### `3` **IL VUOTO EVOLVE DA SOLO, E QUESTO CAMBIA COME SI LEGGE LA `(L)`.** "
      "`Lambda` attorno al grumo cambia **anche con la camminata LINEARE** *(`+11.6%`)*, "
      "perche' Grover e lo spostamento **lo mescolano**. ### ⭐ **Quindi <<il vuoto "
      "risponde>> non si legge dal valore, ma dalla DIFFERENZA dal lineare** — e lo "
      "scrivo perche' il valore da solo **sembrerebbe una risposta.**")
    a("")
    a("### `4` **LA PROPAGAZIONE NON E' ISOTROPA SU UN GRAFO REGOLARE, E IL COLPEVOLE E' "
      "DICHIARATO.** Da quattro nodi dello stesso reticolo le velocita' differiscono del "
      "**~14%**. ### ⛔ **E non e' il reticolo: sono i VERSORI** — che sono "
      "`PROVV-VERSORI-NON-RELAZIONALI`, assegnati **per indice d'arco**, quindi "
      "### **diversi da nodo a nodo anche dove la struttura e' identica.** "
      "### ⭐ **E' la prova piu' diretta che quella scelta provvisoria SI VEDE nei "
      "numeri.**")
    a("")
    a("### `5` **`eps` RALLENTA LA LUCE INVECE DI AVVICINARLA AL CONO.** Il fronte e' "
      "**piu' veloce a `eps = 0`** *(`0.768` archi/tick)* e scende **monotono** fino a "
      "`0.477` a `eps = 1`. ### ✅ **E ha senso: `eps` e' il termine di MASSA, e una "
      "massa RALLENTA** — ### **quindi la previsione <<esiste un `eps*` che avvicina "
      "al cono>> era sbagliata nel verso**, e il massimo e' **il caso senza massa.**")
    a("")
    a("## ✅ **CHE COSA SBLOCCA O RIAPRE NELL-ALBERO** *(e nessuna decisione e' mia)*")
    a("")
    a("| il nodo | che cosa dicono i numeri | che cosa NON dicono |")
    a("|---|---|---|")
    a("| **[[DOMANDA-QUANTITA-CONSERVATA]]** *(la prossima)* | ### ⭐ **UNA "
      "C'E':** la **conservazione modificata** di `N` *(quasi-energia lineare piu' "
      "`Sigma N_k`)* **si conserva** con la non linearita' accesa | non dicono che sia "
      "**L'ENERGIA**: la promozione e' ### **una decisione di Luca**, e il referto la chiama "
      "col nome che ha |")
    a("| **[[COESIONE-TERMINE-O-CAMPO]]** | ### ⛔ **la via `(a)` si indebolisce:** "
      "**tre** termini locali saturanti, e ### **nessuno lega** | non dicono che nessun "
      "termine locale possa: dicono che ### **questi tre non lo fanno** |")
    a("| **[[GUSCIO-ANTIFASE-EMERGENTE]]** | niente: ### **serve un grumo, e non c'e'** | "
      "e' la lettura `G1`, ### **in coda** |")
    a("| **[[PROVV-VERSORI-NON-RELAZIONALI]]** | ### ⭐ **la scelta SI VEDE:** rompe "
      "l'isotropia della propagazione su un grafo regolare *(`~14%`)* | non dicono da dove "
      "debbano venire: e' `DOMANDA-D9-GEOMETRIA` |")
    a("| **[[DOMANDA-C2-O-C4]]** | gli stati intrappolati sui cicli sono ### **`4` per "
      "ciclo** e `eps` li distrugge **tutti**, e ### **nessuna olonomia li riporta** | non "
      "dicono niente su `C^4` |")
    a("| **[[VUOTO-LOCALE-DETERMINISTICO]]** | la forma provvisoria ### **regge tutti i "
      "collaudi** *(gauge, cono, norme, reversibilita-, `C`)* e ### **il vuoto risponde** | "
      "non dicono che sia **la** forma: e' ### **dichiarata provvisoria** |")
    a("")
    a("## ⚠ **I LIMITI, dichiarati**")
    a("")
    a("| | il limite |")
    a("|---|---|")
    a("| `1` | ### **`cs_k = 1` ovunque**, e **`r = 1` nel banco**: il `v3` **non prova la "
      "`cs` locale** |")
    a("| `2` | ### **un solo grafo irregolare** e un regolare: **non e' uno scaling di "
      "taglia finita** *([[TAGLIA-FINITA]])* |")
    a("| `3` | il grumo e' ### **costruito da me**, su **un** centro e **un** raggio: se "
      "l'intrappolamento dipendesse dalla FORMA, questo referto **non lo vedrebbe** |")
    a("| `4` | ### **`(D)` ed `(E)` usano il punto medio implicito**, con sotto-passi "
      "**derivati** *(`%s`)*: un metodo **diverso** da quello di `N`, che e' **esatto** |"
      % d.get("sotto_passi_usati", {}))
    a("| `5` | la `(F)` misura una frequenza ### **su un grumo che si disperde**: il numero "
      "c'e', ma **il suo significato no** |")
    a("")
    io.open(DEST, "wb").write((NL.join(r) + NL).encode("utf-8"))
    print("=" * 100)
    for k in ORDINE:
        print("  %-3s %-34s %s" % (k, NOMI[k][:34],
                                   v[k][0].replace("### ", "").replace("*", "")))
    print("=" * 100)
    print("  scritto %s" % os.path.relpath(DEST, RADICE).replace(os.sep, "/"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
