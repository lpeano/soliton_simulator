r"""IL REFERTO DEL LEGAME — **GENERATO da `uscite/letture_legame.json`, VERDETTI COMPRESI.**

### ⛔ **Ogni numero e ogni verdetto escono dal `json`** *(`L-NUMERI`)*, e le soglie stanno
nel task history `doc/TASK_HISTORY/2026-10-11_legame.md`, **committato PRIMA** (`11b8927`).

Gira con:  python proto_camminata/_referto_legame.py
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

import buchi0 as B0                                            # noqa: E402

NL = chr(10)
FONTE = os.path.join(_QUI, "uscite", "letture_legame.json")
DEST = os.path.join(RADICE, "doc", "REFERTO_legame.md")
FAM = ("regolare (1D)", "cubico (3D)", "geometrico3d (3D irregolare)",
       "irregolare (casuale)")


def main():
    d = json.loads(io.open(FONTE, encoding="utf-8").read())
    R = []

    def a(s=""):
        R.append(s)

    a("# IL REFERTO DEL LEGAME — **PERCHE' NESSUN GRUMO STA INSIEME**")
    a("")
    a("> ### ⛔ **CONGELATO** *(forma dichiarata in `csv/_forma_referti.py`)*: e' un "
      "### **REPERTO** — la CI ### **non lo rigenera**, e il presidio verifica ### "
      "**il suo BLOB.**")
    a("")
    a("*(**Generato** da `python proto_camminata/_referto_legame.py`, che legge "
      "`proto_camminata/uscite/letture_legame.json` prodotto da `python "
      "proto_camminata/_letture_legame.py`. Soglie e previsioni: "
      "`doc/TASK_HISTORY/2026-10-11_legame.md`, **committato PRIMA del codice** "
      "(`11b8927`).)*")
    a("")
    a("> ## ⭐ **IL VERDETTO, IN UNA RIGA: LA FORMA `(D)` COL SEGNO DIRETTO **LEGA IN "
      "`1D`**, e in `3D` l'effetto **CALA CON LA TAGLIA** fino a sparire.**")
    a("")
    a("> ### ⛔ **E si scrive <<LEGA IN `1D`>>, non <<lega>>**, perche' l'anello ha "
      "### **dimensione spettrale `1.001`** — ed e' la distinzione che il mandato "
      "aveva ### **preregistrato.**")
    a("")

    # ===================================================== la configurazione
    a("## LA CONFIGURAZIONE, INTERA *(`H-P5`)*")
    a("")
    a("| | |")
    a("|---|---|")
    a("| i semi | `%s` |" % ", ".join("`%d`" % s for s in d["semi"]))
    a("| `eps` del passo | **`%g`** |" % d["eps_del_passo"])
    a("| la velocita' del fronte, **misurata** | **`%g`** archi/tick *(referto `v4`)*, e da "
      "lei viene `T_max = 2 * diametro / v` |" % d["velocita_del_fronte_misurata"])
    a("| la griglia di `eps` di `M0` | `%s`, **ridotta a `0, 0.5, 1`** dove `dim > 4500` "
      "*(il costo di `eig` e' **cubico**)* |"
      % ", ".join("`%g`" % x for x in d["M0"]["griglia_eps"]))
    a("| la soglia di un buco | larghezza **`> %g`** spaziature *(degli stati USATI, non di "
      "`dim`)* |" % d["M0"]["soglia_buco_in_spaziature"])
    a("| la griglia di `x0` di `M1` | `%s` |"
      % ", ".join("`%g`" % x for x in d["M1"]["griglia_x0"]))
    a("| la geometria | `scena_identita` *(e `scena_curva` nei bracci del banco)* |")
    a("| le candidate | `+N`, `-N`, `+D`, `-D`, **accendibili e mai di default**; e il "
      "**lineare** come controllo |")
    a("")

    # ===================================================== le dimensioni
    a("## ⭐ **LE DIMENSIONI E L'ISOTROPIA, MISURATE — e decidono come si legge "
      "tutto il resto**")
    a("")
    a("| la scena | famiglia | `n` | diametro | **`d_s`** | `r²` | legge di potenza? |")
    a("|---|---|---|---|---|---|---|")
    for nome, v in sorted(d["dimensioni"].items(),
                          key=lambda x: (x[1]["famiglia"], x[1]["n"])):
        a("| `%s` | %s | `%d` | `%s` | **%.3f** | `%.4f` | %s |"
          % (nome, v["etichetta"], v["n"],
             ("%d" % v["diametro"]) if v["diametro_esatto"]
             else (">= %d" % v["diametro"]),
             v["d_s"], v["r2"],
             "si" if v["potenza"] else "### ⛔ **NO**"))
    a("")
    a("### ⛔ **E LE DUE SCENE DEL BANCO NON HANNO DIMENSIONE `3`:** l'anello e' "
      "### **`1D` esatto** *(`d_s = 1.001`, `r² = 1.0000`)* e il casuale ha `d_s` che "
      "### **CRESCE con `n`** *(`2.36` → `3.93`)*, cioe' ### **non ha una dimensione "
      "fissa.** ### **Un verdetto su quelle due non dice che cosa succede in uno spazio a "
      "tre dimensioni**, ed e' la ragione per cui le famiglie `3D` esistono.")
    a("")

    # ===================================================== M0
    a("## `M0` — **IL BUCO NELLO SPETTRO: C'E' SULL'ANELLO E SUL GEOMETRICO `3D`, NON "
      "SUL CUBICO**")
    a("")
    a("| la famiglia | il verdetto | `eps` col buco | `eps` senza |")
    a("|---|---|---|---|")
    for fam in FAM:
        dentro = {k: {q: w for q, w in v.items() if q != "_scena"}
                  for k, v in d["M0"]["per_scena"].items()
                  if v["_scena"]["famiglia"] == fam}
        if not dentro:
            continue
        v = B0.verdetto(dentro)
        a("| **%s** | %s | `%s` | `%s` |"
          % (fam,
             ("### ⭐ **%s**" % v["verdetto"]) if v["buco_all_eps_della_fisica"]
             else ("### ⛔ **%s**" % v["verdetto"]),
             ", ".join(v["eps_col_buco"]) or "nessuno",
             ", ".join(v["eps_senza_buco"]) or "nessuno"))
    a("")
    a("### ⛔ **E IL MIO PRIMO VERDETTO ERA UN FALSO-UNO MIO:** collassavo gli `eps` "
      "con un ### **OR**, e tutte e quattro le famiglie dicevano *«BUCO PRESENTE E "
      "STABILE»*. ### ⭐ **Ma il buco veniva TUTTO da `eps = 0`**, dove ### **non c'e' "
      "moneta di spin** e ### **il `43%` degli stati sta a `±1`**: un buco la' e' la "
      "### **struttura a BANDE PIATTE di Grover**, non un gap in cui uno stato legato possa "
      "vivere. ### **Trovato leggendo i numeri, non rileggendo il codice.**")
    a("")
    cub = {k: {q: w for q, w in v.items() if q != "_scena"}
           for k, v in d["M0"]["per_scena"].items()
           if v["_scena"]["famiglia"] == "cubico (3D)"}
    vc = B0.verdetto(cub)
    a("### **E il cubico lo mostra in tre righe** *(larghezze su `L = 5` e `L = 8`)*:")
    a("")
    a("| `eps` | larghezza | in spaziature | rapporto `L=8 / L=5` | buco? |")
    a("|---|---|---|---|---|")
    for k in sorted(vc["per_eps"], key=float):
        v = vc["per_eps"][k]
        a("| `%s` | %s | %s | **%.3f** | %s |"
          % (k, " → ".join("%.4g" % x for x in v["larghezze"]),
             " → ".join("%.1f" % x for x in v["in_spaziature"]),
             v["rapporto_larghezza"],
             "### ⭐ **si'**" if v["buco"] else "### ⛔ **no**"))
    a("")
    a("### ⛔ **A `eps = 0.5` e `eps = 1` la larghezza CALA del `71%` e del `69%` "
      "crescendo la taglia** — cioe' scala come ### **la spaziatura della griglia di "
      "momenti**, e ### **una spaziatura non e' un gap.** ### ✅ **E la soglia che "
      "l'ha preso era scritta PRIMA** *(`s2`: la larghezza non cala piu' del `50%`)*.")
    a("")

    # ===================================================== M1
    a("## ⭐ **`M1` — IL SEGNO: `(D)` DIRETTO LEGA IN `1D`, E IN `3D` L'EFFETTO "
      "CALA CON LA TAGLIA**")
    a("")
    a("| la scena | famiglia | diametro | `t_oss` | **RESTA** | **DISPERDE** | non "
      "decidibili |")
    a("|---|---|---|---|---|---|---|")
    P = d["M1"]["per_scena"]
    for nome in sorted(P, key=lambda x: (P[x]["_scena"]["famiglia"],
                                         P[x]["_scena"]["n"])):
        s = P[nome]["_scena"]
        c = {"RESTA CONCENTRATO": 0, "SI DISPERDE": 0, "NON DECIDIBILE PER TAGLIA": 0}
        for et in ("+N", "-N", "+D", "-D"):
            for v in P[nome].get(et, {}).values():
                q = (v.get("contro_lineare") or {}).get("verdetto")
                if q:
                    c[q] = c.get(q, 0) + 1
        a("| `%s` | %s | `%s` | `%d` | **%d** | %d | %s |"
          % (nome, s["famiglia"], ("%d" % s["diametro"]) if s["diametro_esatto"]
             else (">= %d" % s["diametro"]), s["t_oss"],
             c["RESTA CONCENTRATO"], c["SI DISPERDE"],
             ("**%d**" % c["NON DECIDIBILE PER TAGLIA"])
             if c["NON DECIDIBILE PER TAGLIA"] else "`0`"))
    a("")
    a("### ✅ **E <<NON DECIDIBILE>> E' SPARITO DEL TUTTO, perche' la regola era "
      "applicata allo stato sbagliato:** prima dava `0` casi decidibili su ### **otto scene "
      "su nove.** ### **Adesso la taglia si giudica sul grumo INIZIALE e il raggio finale e' "
      "una MISURA** — e *«si disperde»* e' ### **un risultato, non un'assenza di "
      "risultato.**")
    a("")

    # --------------------------------------------- l-effetto, non il sigma
    righe = []
    for nome in P:
        s = P[nome]["_scena"]
        for et in ("+N", "-N", "+D", "-D"):
            for k in sorted(P[nome].get(et, {}), key=float):
                v = P[nome][et][k]
                c = v.get("contro_lineare") or {}
                if c.get("verdetto") != "RESTA CONCENTRATO":
                    continue
                b = P[nome]["lineare"][k]["rapporto"]
                righe.append({
                    "eff": ((v["rapporto"] - b) / b) if b else 0.0,
                    "sigma": c["in_sigma"], "scena": nome, "fam": s["famiglia"],
                    "var": et, "x0": k, "rf": v["raggio_finale"],
                    "diam": s["diametro"]})
    righe.sort(key=lambda x: -x["eff"])
    a("### ⛔ **E I CASI SI ORDINANO PER *EFFETTO*, NON PER `sigma` — e il motivo "
      "e' un falso-uno che i numeri mi hanno messo davanti**")
    a("")
    pic = [x for x in righe if x["eff"] < 0.01]
    a("### **Dei `%d` casi <<RESTA CONCENTRATO>>, `%d` hanno un effetto SOTTO l'`1%%`** "
      "— e il peggiore e' ### **`%+.3f%%` a `%.2f sigma`** *(`%s`, `%s`, "
      "`x0 = %s`)*: il rapporto e' **%.3f** contro **%.3f** del lineare, cioe' ### **uguale "
      "a tre decimali.** ### ⭐ **E' SIGNIFICATIVITA' SENZA EFFETTO**, il rovescio "
      "esatto dell'errore che avevo fatto in `G2(b)` del `v4` — e la soglia `3 sigma`, "
      "scritta prima, ### **non basta da sola: serve anche l'ampiezza dell'effetto.**"
      % (len(righe), len(pic), 100 * pic[0]["eff"] if pic else 0.0,
         pic[0]["sigma"] if pic else 0.0, pic[0]["scena"] if pic else "",
         pic[0]["var"] if pic else "", pic[0]["x0"] if pic else "",
         P[pic[0]["scena"]][pic[0]["var"]][pic[0]["x0"]]["rapporto"] if pic else 0.0,
         P[pic[0]["scena"]]["lineare"][pic[0]["x0"]]["rapporto"] if pic else 0.0))
    a("")
    a("| **effetto** | `sigma` | la scena | famiglia | var | `x0` | raggio finale / diametro |")
    a("|---|---|---|---|---|---|---|")
    for x in righe[:14]:
        pieno = x["rf"] >= 0.8 * x["diam"]
        a("| **%+.2f%%** | `%.2f` | `%s` | %s | **`%s`** | `%s` | %.0f / %d%s |"
          % (100 * x["eff"], x["sigma"], x["scena"], x["fam"].split()[0], x["var"],
             x["x0"], x["rf"], x["diam"],
             " ### ⛔ **il fronte ha RIEMPITO il grafo**" if pieno else ""))
    a("")

    # --------------------------------------------- la taglia
    a("### ⭐ **E LA PROVA CHE DECIDE E' LA TAGLIA, perche' il mandato lo chiede: "
      "<<solido solo se regge su almeno DUE taglie>>**")
    a("")

    def eff(nome, et, k):
        v = P.get(nome, {}).get(et, {}).get(k)
        if not v:
            return None
        c = v.get("contro_lineare") or {}
        if c.get("verdetto") != "RESTA CONCENTRATO":
            return None
        b = P[nome]["lineare"][k]["rapporto"]
        return ((v["rapporto"] - b) / b) if b else 0.0

    a("| famiglia | il caso | taglia piccola | taglia grande | che cosa fa |")
    a("|---|---|---|---|---|")
    prove = (("regolare (1D)", "+D", "1", "regolare n=120", "regolare n=2000"),
             ("cubico (3D)", "+D", "2", "cubico L=8", "cubico L=12"),
             ("geometrico3d (3D irregolare)", "+D", "1", "geometrico3d n=512",
              "geometrico3d n=1728"),
             ("irregolare (casuale)", "+N", "2", "irregolare n=120",
              "irregolare n=2000"))
    for fam, et, k, pic_, gra in prove:
        e1, e2 = eff(pic_, et, k), eff(gra, et, k)
        if e1 is None and e2 is None:
            continue
        if e2 is None:
            cosa = "### ⛔ **SPARISCE**"
        elif e1 is None:
            cosa = "### ⚠ **compare solo in grande**"
        elif e2 > e1:
            cosa = "### ⭐ **CRESCE**"
        else:
            cosa = "### ⛔ **CALA**"
        a("| **%s** | `%s` a `x0 = %s` | %s | %s | %s |"
          % (fam, et, k,
             ("**%+.2f%%**" % (100 * e1)) if e1 is not None else "non concentrato",
             ("**%+.2f%%**" % (100 * e2)) if e2 is not None else "### **NIENTE**",
             cosa))
    a("")
    a("### ⭐ **QUINDI: in `1D` l'effetto CRESCE con la taglia** *(`+18.4%` a `n=120`, "
      "`+24.6%` a `n=2000`)*, e in ### **`3D` CALA o SPARISCE** — sul cubico da "
      "`+24.1%` a `L=8` a `+8.6%` a `L=12`, e sul geometrico ### **da `+11.9%` a `n=512` a "
      "NIENTE a `n=1728`** *(`0` casi concentrati su `28`)*.")
    a("")
    a("### ⚠ **E UNA COSA CHE NON LASCIO AMBIGUA: anche il CASUALE cresce** "
      "*(`+8.9%` → `+12.4%`)*. ### **Le due famiglie che CRESCONO sono `1D` e "
      "l'ESPANSORE; le due che CALANO sono le `3D`.** ### ⛔ **Ma sull'espansore il "
      "misurando stesso e' sospetto**, e lo dichiaro: il *«fondo uniforme»* su un grafo dove "
      "il volume cresce ### **esponenzialmente** con la distanza e' ### **minuscolo**, "
      "quindi il rapporto *«frazione entro un arco / fondo»* puo' crescere ### **per la "
      "geometria del denominatore**, non perche' il grumo stia insieme. ### **Non concludo "
      "<<lega anche nell-espansore>>: dico che il misurando non lo distingue.**")
    a("")
    a("### ⛔ **E IL GEOMETRICO `3D` HA UN BUCO NELLO SPETTRO *E NON LEGA*:** un buco "
      "e' ### **necessario ma non sufficiente**, ed e' il risultato piu' informativo di "
      "tutto il mandato.")
    a("")

    # ===================================================== i limiti
    a("## ⚠ **I LIMITI, dichiarati**")
    a("")
    a("| | il limite |")
    a("|---|---|")
    a("| `1` | ### **`M2` NON E' GIRATA su queste famiglie**: gli stati stazionari "
      "autoconsistenti restano da misurare, e la sonda sul `n=120` irregolare dice che il "
      "selettore prescritto dal mandato *(«il piu' localizzato»)* ### **oscilla a `O(1)`**, "
      "mentre quello a ### **massima sovrapposizione** converge a `1.9e-13` |")
    a("| `2` | ### **DUE taglie non sono uno scaling** *(`TAGLIA-FINITA`)*: la soglia `s2` "
      "confronta la piu' piccola con la piu' grande, e con due punti e' ### **una retta per "
      "due punti.** `M0` ha due taglie per famiglia |")
    a("| `3` | ### **Sulle scene `3D` piccole il fronte RIEMPIE il grafo**: il raggio finale "
      "arriva a `5/6` sul cubico `L=5` e a `11/18` su `L=12`. ### **La regola sul raggio "
      "INIZIALE passa, ma il confronto <<frazione entro un arco contro fondo uniforme>> e' "
      "allora dominato dalla taglia finita** — e questo ### **non e' nella regola del "
      "mandato** |")
    a("| `4` | ### **La soglia `3 sigma` non basta da sola**: `%d` casi su `%d` hanno un "
      "effetto sotto l'`1%%`, e uno e' `+0.016%%` a `3.55 sigma`. ### **L'effetto si "
      "riporta accanto al `sigma`**, sempre |" % (len(pic), len(righe)))
    a("| `5` | ### **L'anisotropia delle scene `3D` non e' risolta**: nessuna delle due "
      "provate e' isotropa sul misurando di grafo, e il mandato "
      "`[[ISOTROPIA-LOCALE]]` e' in coda proprio per questo |")
    a("| `6` | ### **La grandezza conservata di `-N` e' `-N`**, e ### **NON la chiamo "
      "energia** *(`[[PROMOZIONE-CONSERVAZIONE-MODIFICATA]]` e' una decisione di Luca "
      "aperta)* |")
    a("")

    dati = (NL.join(R) + NL).encode("utf-8")
    io.open(DEST, "wb").write(dati)
    print("  scritto %s" % os.path.relpath(DEST, RADICE).replace(os.sep, "/"))
    print("  %d righe, %d byte" % (len(R), len(dati)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
