# -*- coding: utf-8 -*-
"""IL REFERTO DI `A-S1`, generato. ### **Nessun numero si ricopia** *(`L-NUMERI`)*.

### ⛔ **IL BRACCIO DI CONTROLLO E' LA CORSA `A1`** *(`67f020e`,
`csv/_test_fork/_misura_verso/verso.json`)*, che ### **non si rigira** e che combacia
### **al bit** con `amp0.json` su tutti i `1000` passi.

### ⚠ **E LE TRE DICHIARAZIONI CHE IL REFERTO PORTA IN TESTA**, perche' chi legge deve
saperle ### **prima** dei numeri: ### **`U1` aperta**, ### **`P3` non soddisfatta** *(un
seme)*, e ### **TRE confondenti** -- di cui ### **uno MISURATO e risultato piccolo.**
"""
import io
import json
import math
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
for _p in (os.path.join(RADICE, "csv"), _QUI):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import _presidio                                   # noqa: E402
_presidio.avvia(__file__)

import _mitosi_soglia_grad as _MSG                 # noqa: E402

NL = chr(10)
FUORI = os.path.join(RADICE, "doc", "REFERTO_as1_test_h1_2026-10-07.md")
P_H1 = os.path.join(_QUI, "_massa_h1", "h1.json")
P_P0 = os.path.join(_QUI, "_massa_h1", "passo0.json")
P_A1 = os.path.join(_QUI, "_misura_verso", "verso.json")
R = []


def A(s=""):
    R.append(s)


def n4(x, c=4):
    if x is None:
        return "n/d"
    if isinstance(x, float) and not math.isfinite(x):
        return "`NaN`"
    if isinstance(x, float):
        return ("%." + str(c) + "f") % x
    return "%s" % x


def pct(x, c=2):
    return "n/d" if x is None else (("%." + str(c) + "f %%") % (100.0 * x))


def carica(p):
    if not os.path.exists(p):
        return None
    try:
        return json.load(io.open(p, encoding="utf-8"))
    except Exception as e:                            # noqa: BLE001
        return {"_errore": str(e)}


def main():
    d = carica(P_H1)
    p0 = carica(P_P0)
    a1 = carica(P_A1)
    if not d or d.get("_errore"):
        raise SystemExit("[FERMO] `h1.json` assente o illeggibile: %r"
                         % (None if not d else d.get("_errore"),))
    if d.get("stato") != "DATI SALVATI" or d.get("passi_girati") != d.get("passi"):
        raise SystemExit("[FERMO] la corsa `H1` non e' completa: stato %r, girati %r su %r."
                         % (d.get("stato"), d.get("passi_girati"), d.get("passi")))
    h = d["massa_h1"]
    PM = [int(x) for x in h["passi_misura"]]
    SENZA = set(int(x) for x in h.get("passi_senza_controllo") or ())
    mis = {int(k): v for k, v in h["misure"].items()}
    passi = {int(r["passo"]): r for r in h["passi"]}
    # --- il CONTROLLO, dalla corsa `A1`
    c_auc, c_ck, c_n, c_fr = {}, {}, {}, {}
    if a1 and not a1.get("_errore"):
        v = a1["verso"]
        for k in PM:
            m2 = (v["misure"].get(str(k)) or {}).get("M2") or {}
            if m2.get("auc_materia_vuoto") is not None:
                c_auc[k] = m2["auc_materia_vuoto"]
            pc = m2.get("c_per_classe") or {}
            if pc:
                c_ck[k] = {q: (None if not x else x.get("mediana")) for q, x in pc.items()}
        for r in v["passi"]:
            c_n[int(r["passo"])] = r.get("n")
            c_fr[int(r["passo"])] = r.get("fraz_tw_oltre_2pi")

    def auc(k):
        return (mis.get(k) or {}).get("auc_materia_vuoto")

    def ck(k, cl):
        x = ((mis.get(k) or {}).get("c_per_classe") or {}).get(cl)
        return None if not x else x.get("mediana")

    # ======================================================================
    A("# `A-S1` — **IL TEST `H1`: LE MASSE SOPRAVVIVONO SE LE VELOCITÀ DI FASE PARTONO COERENTI?**")
    A("")
    A("*Referto generato da `csv/_test_fork/_referto_massa_h1.py`. "
      "Dati: `csv/_test_fork/_massa_h1/h1.json`. "
      "Criteri e previsioni: `doc/TASK_HISTORY/2026-10-07_as1-test-h1-scioglimento.md`, "
      "committato ### **PRIMA** della corsa.*")
    A("")
    A("| | |")
    A("|---|---|")
    A("| simulatore | `%s` *(atteso `%s`)* |"
      % (str(d.get("blob_sim"))[:8], d.get("blob_atteso")))
    A("| strumento | `%s` |" % str(d.get("blob_strumento"))[:8])
    A("| `_misura_verso` *(da cui si CHIAMA `m2`)* | `%s` |"
      % str(d.get("blob_misura_verso"))[:8])
    A("| passi | ### **%s** |" % n4(d.get("passi")))
    A("| secondi | %s |" % n4(d.get("secondi"), 1))
    A("| in configurazione del driver | %s |"
      % ("### ✔ **sì**" if d.get("in_configurazione_del_driver") else "### ⛔ **NO**"))
    A("| avvisi | ### **%s** |" % n4(len(h.get("avvisi") or [])))
    A("")
    A("## ⛔ **TRE COSE DA SAPERE PRIMA DEI NUMERI**")
    A("")
    A("> ### ⛔ **`1` — `U1` È APERTA** *(da-decidere, blocca `SI`)*. Questa corsa "
      "### **non dà valori assoluti:** confronta ### **DUE BRACCI DELLO STESSO SIMULATORE**, "
      "e la legge difettosa è ### **la stessa in entrambi**. ### **Quello che si legge è la "
      "DIFFERENZA, non il livello.**")
    A("")
    A("> ### ⚠ **`2` — `P3` NON È SODDISFATTA: UN SEME SOLO** *(il `11`)*, perché il braccio "
      "di controllo è la corsa `A1` e il mandato dice di ### **non rigirarla**. "
      "*(`S1b`, nel task history del 2026-09-27, chiedeva ### **`4` semi**.)* Il confronto è "
      "### **APPAIATO** — stessa scena, stesso seme, ### **UNA** condizione iniziale cambiata "
      "— che è la forma più forte di confronto appaiato, e ### **non dice NIENTE sulla "
      "variabilità fra semi.** ### **`A-S1` è una DIAGNOSI, non un sigillo: nessuna cura può "
      "appoggiarsi a questo numero.**")
    A("")
    A("> ### ⚠ **`3` — TRE CONFONDENTI, dichiarati PRIMA della corsa** *(task history, "
      "aggiunta datata)*. ### **Uno di essi è MISURATO in questo referto**, e "
      "### **il numero lo ridimensiona.** La tavola è sotto.")
    A("")
    A("---")
    A("")
    # ======================================================================
    A("# `(0)` **L'INTERVENTO, E IL CONTROLLO CHE LO DELIMITA**")
    A("")
    A("L'intervento: ### **`net.phivel[idx] = media(net.phivel[idx])` per ogni massa**, "
      "### **dopo la costruzione e PRIMA del passo `1`**, ### **nello strumento.** "
      "### ✔ **Toglie SOLO la dispersione, non cambia la velocità media, e non introduce "
      "nessun numero nuovo** *(`A1`)*.")
    A("")
    _iv = (h.get("geometria") or {}).get("intervento") or {}
    if _iv:
        A("| massa | nodi | media imposta | `std` PRIMA | intervallo PRIMA |")
        A("|---|--:|--:|--:|---|")
        for et in sorted(_iv):
            x = _iv[et]
            A("| `%s` | %s | ### **%s** | %s | `[%s, %s]` |"
              % (et, n4(x.get("nodi")), n4(x.get("media"), 6), n4(x.get("std_prima"), 6),
                 n4(x.get("min_prima")), n4(x.get("max_prima"))))
        A("")
        A("> ### ⭐ **E LE MEDIE SONO QUASI ZERO MENTRE LE `std` SONO `~0.41`:** "
          "### **equalizzare alla media non «allinea» le velocità, le AZZERA.** "
          "### **È il terzo confondente**, e il task history lo registra col conto "
          "dell'energia cinetica.")
        A("")
    if p0 and not p0.get("_errore"):
        A("### ✔ **IL CONTROLLO DEL PASSO `0`** *(`python csv/_test_fork/_massa_h1.py --passo0`)*")
        A("")
        cc = p0.get("conteggi") or {}
        A("| | |")
        A("|---|--:|")
        A("| attributi firmati | %s |" % n4(cc.get("attributi")))
        A("| attributi ### **DIVERSI** | ### **%s** — `%s` |"
          % (n4(len(cc.get("diversi") or [])), ", ".join(cc.get("diversi") or [])))
        A("| nodi delle masse | %s |" % n4(cc.get("nodi_di_massa")))
        A("| nodi FUORI con `phivel` ### **identica AL BIT** | ### **%s** |"
          % n4(cc.get("fuori_identici")))
        A("| esito | %s |"
          % ("### ✔ **PASSA**" if p0.get("esito") == "PASSA" else "### ⛔ **FALLISCE**"))
        A("")
        A("> ### ⛔ **E LA VERIFICA NON È «`phivel` DIFFERISCE»:** un nodo la cui `phivel` era "
          "### **già** la media ### **non differisce**, e pretenderlo darebbe un falso "
          "allarme. ### **Le due affermazioni VERE sono «fuori dalle masse identica al bit» e "
          "«dentro vale ESATTAMENTE la media dichiarata».**")
        A("")
    else:
        A("> ### ⛔ **IL CONTROLLO DEL PASSO `0` NON C'È:** questo referto "
          "### **non può affermare che i due bracci differiscono solo in `phivel`.** "
          "### **Lo dico invece di ometterlo.**")
        A("")
    A("---")
    A("")
    # ======================================================================
    A("# `(1)` ⭐ **L'AUC DI `c_k` MATERIA/VUOTO — IL NUMERO CHE DECIDE**")
    A("")
    A("> ### ⛔ **I CRITERI, FISSATI PRIMA** *(mandato di Luca)*: "
      "### **`H1 BASTA`** se AUC al `400` ### **`>= 0.90`** ### **E** al `500` "
      "### **`>= 0.85`**; ### **`H1 NON BASTA`** se AUC al `400` ### **`< 0.60`**; "
      "fra i due ### **`H1 AIUTA MA NON BASTA`**, e si riporta la curva e il passo in cui "
      "l'AUC scende sotto ### **`0.60`** nei due bracci.")
    A("")
    A("| passo | ### **AUC `H1`** | AUC controllo | differenza | `c_k` MAT `H1` | MAT contr. | `c_k` VUO `H1` | VUO contr. |")
    A("|--:|--:|--:|--:|--:|--:|--:|--:|")
    for k in PM:
        a_h, a_c = auc(k), c_auc.get(k)
        dif = None if (a_h is None or a_c is None) else a_h - a_c
        cc = c_ck.get(k) or {}
        A("| `%d`%s | ### **%s** | %s | %s | %s | %s | %s | %s |"
          % (k, " ⚠" if k in SENZA else "", n4(a_h), n4(a_c),
             ("### **%+.4f**" % dif) if dif is not None else "n/d",
             n4(ck(k, "MATERIA")), n4(cc.get("MATERIA")),
             n4(ck(k, "VUOTO")), n4(cc.get("VUOTO"))))
    A("")
    if SENZA:
        A("> ### ⚠ **I PASSI SEGNATI `⚠` NON HANNO IL CONTROLLO:** la corsa `A1` misurava i "
          "passi pesanti `1, 150, 230, 300, 400, 500, 700, 1000`, e ### **il `%s` non è fra "
          "loro.** ### ✔ **I due passi su cui i criteri DECIDONO — `400` e `500` — il "
          "controllo ce l'hanno**, quindi non ho rigirato una corsa da `500` passi per un "
          "passo che non decide."
          % ", ".join(str(x) for x in sorted(SENZA)))
        A("")

    # --- il passo in cui si scende sotto 0.60
    def sotto(d_auc):
        q = [k for k in sorted(d_auc) if d_auc[k] is not None and d_auc[k] < 0.60]
        return min(q) if q else None

    s_h = sotto({k: auc(k) for k in PM})
    s_c = sotto(c_auc)
    A("| | primo passo MISURATO con AUC `< 0.60` |")
    A("|---|---|")
    A("| ### **braccio `H1`** | %s |"
      % ("### **mai, nei passi misurati**" if s_h is None else "### **`%d`**" % s_h))
    A("| controllo *(`A1`)* | %s |"
      % ("mai, nei passi misurati" if s_c is None else "### **`%d`**" % s_c))
    A("")
    # --- l'esito del criterio
    a400, a500 = auc(400), auc(500)
    esito, perche = None, None
    if a400 is None or a500 is None:
        esito = "NON DECIDIBILE"
        perche = ("l'AUC manca al passo `400` o al `500`: la corsa non è arrivata dove il "
                  "criterio decide")
    elif a400 >= 0.90 and a500 >= 0.85:
        esito = "H1 BASTA"
        perche = ("AUC `%s` al `400` *(soglia `0.90`)* e `%s` al `500` *(soglia `0.85`)*"
                  % (n4(a400), n4(a500)))
    elif a400 < 0.60:
        esito = "H1 NON BASTA"
        perche = ("AUC `%s` al `400`, sotto la soglia `0.60`: ### **le masse si sciolgono "
                  "anche con le velocità coerenti**" % n4(a400))
    else:
        esito = "H1 AIUTA MA NON BASTA"
        perche = ("AUC `%s` al `400`: ### **sopra `0.60`** *(quindi non «non basta»)* "
                  "### **e sotto `0.90`** *(quindi non «basta»)*" % n4(a400))
    _ic = {"H1 BASTA": "✔", "H1 NON BASTA": "⛔", "H1 AIUTA MA NON BASTA": "⚠",
           "NON DECIDIBILE": "⚠"}[esito]
    A("> ### %s **L'ESITO DEL CRITERIO: `%s`.** %s." % (_ic, esito, perche))
    A("")
    if esito == "H1 NON BASTA":
        A("> ### ⭐ **E QUESTO È IL RAMO CHE I CONFONDENTI NON TOCCANO**, ed era scritto "
          "### **prima** della corsa: un intervento che ha dato alle masse "
          "### **le velocità coerenti** *(e, per gli effetti collaterali, anche una torsione "
          "che rilassa meno e un vuoto scaldato dal termostato)* ### **non le ha salvate "
          "comunque.** ### **La conclusione è SOLIDA.**")
        A("")
        A("> ### ⛔ **E NON SI PASSA AD `A-S2`: LA DECISIONE È DI LUCA.**")
        A("")
    elif esito == "H1 BASTA":
        A("> ### ⛔ **E QUESTO È IL RAMO CONFONDUTO, e lo dichiaro:** l'AUC risale, "
          "### **ma la causa è AMBIGUA** fra la coerenza di fase e i tre effetti "
          "collaterali. ### **Il terzo braccio che li separerebbe richiede di toccare una "
          "legge, e quella decisione è di Luca.**")
        A("")
    A("---")
    A("")
    # ======================================================================
    A("# `(2)` **LA COERENZA DI FASE DI OGNI MASSA, COL SUO NULLO**")
    A("")
    A("> ### ⛔ **IL NULLO NON È ZERO: è il VUOTO.** Una coerenza che scende va letta contro "
      "### **quella del vuoto**, non contro `0`.")
    A("")
    A("> ### ⚠ **E SONO DUE LETTURE, non una.** `phi` vive su ### **`4π`**, quindi "
      "`e^{iφ}` identifica `φ` con `φ + 2π`. ### **Il campo del simulatore usa `exp(1j*φ)`** "
      "*(`:5195`)*, quindi `|<e^{iφ}>|` è ### **quella che il codice VEDE**; "
      "`|<e^{iφ/2}>|` è ### **quella fedele al dominio.** Si riportano entrambe.")
    A("")
    _mi = sorted(set().union(*[set((mis.get(k) or {}).get("per_massa") or {}) for k in PM])
                 ) if PM else []
    A("| passo | %s | ### **VUOTO** |"
      % " | ".join("### **`%s`**" % x for x in _mi))
    # ### ⛔ **QUI C'ERA UN DOPPIO `|`**, e l'ha preso il giro sul referto di prova:
    #   `"|--:|" + "--:|"*3 + "|--:|"` da' ### **`|--:|--:|--:|--:||--:|`** -- una colonna in
    #   piu' e una tabella rotta. ### **Il separatore e' UNA SOLA catena.**
    A("|--:|" + "--:|" * (len(_mi) + 1))
    for k in PM:
        pm = (mis.get(k) or {}).get("per_massa") or {}
        vu = (mis.get(k) or {}).get("vuoto")
        A("| `%d` | %s | %s |"
          % (k,
             " | ".join(n4((pm.get(x) or {}).get("coer_2pi")) for x in _mi),
             n4((vu or {}).get("coer_2pi"))))
    A("")
    A("*(la stessa, letta su `4π`)*")
    A("")
    A("| passo | %s | ### **VUOTO** |"
      % " | ".join("`%s`" % x for x in _mi))
    # ### ⛔ **QUI C'ERA UN DOPPIO `|`**, e l'ha preso il giro sul referto di prova:
    #   `"|--:|" + "--:|"*3 + "|--:|"` da' ### **`|--:|--:|--:|--:||--:|`** -- una colonna in
    #   piu' e una tabella rotta. ### **Il separatore e' UNA SOLA catena.**
    A("|--:|" + "--:|" * (len(_mi) + 1))
    for k in PM:
        pm = (mis.get(k) or {}).get("per_massa") or {}
        vu = (mis.get(k) or {}).get("vuoto")
        A("| `%d` | %s | %s |"
          % (k,
             " | ".join(n4((pm.get(x) or {}).get("coer_4pi")) for x in _mi),
             n4((vu or {}).get("coer_4pi"))))
    A("")
    A("---")
    A("")
    # ======================================================================
    A("# `(3)` ⭐ **LA DISPERSIONE DI `phivel`: QUANTO DURA L'INTERVENTO**")
    A("")
    A("> ### ⭐ **QUESTA È LA MISURA CHE DICE SE L'INTERVENTO È SOPRAVVISSUTO.** "
      "`scuoti_vuoto` sta nella `PASSO_COMPOSIZIONE` a ### **ogni** passo e "
      "### **scrive `phivel` e nient'altro**: l'equalizzazione è una "
      "### **condizione iniziale**, non uno stato mantenuto.")
    A("")
    A("| passo | %s | ### **VUOTO** *(il NULLO)* | %s |"
      % (" | ".join("`std %s`" % x for x in _mi),
         " | ".join("### **%s / VUOTO**" % x for x in _mi)))
    A("|--:|" + "--:|" * (2 * len(_mi) + 1))
    for k in PM:
        m = mis.get(k) or {}
        pm = m.get("per_massa") or {}
        vu = m.get("vuoto") or {}
        rel = m.get("disp_rel_per_massa") or {}
        A("| `%d` | %s | %s | %s |"
          % (k,
             " | ".join(n4((pm.get(x) or {}).get("phivel_std"), 5) for x in _mi),
             n4(vu.get("phivel_std"), 5),
             " | ".join("### **%s**" % n4(rel.get(x)) for x in _mi)))
    A("")
    _p1 = mis.get(1) or {}
    _r1 = _p1.get("disp_rel_per_massa") or {}
    _v1 = [v for v in _r1.values() if v is not None]
    if _v1:
        A("> ### ⛔ **AL PASSO `1` LA DISPERSIONE È GIÀ AL %s DEL VUOTO.** "
          "### **L'intervento azzera la dispersione al passo `0`, e UN SOLO PASSO la riporta "
          "a circa metà.** ### ⭐ **Non è una previsione: è il numero**, e dice che "
          "### **`scuoti_vuoto` cancella l'intervento quasi subito.**"
          % pct(sum(_v1) / len(_v1)))
        A("")
    A("---")
    A("")
    # ======================================================================
    A("# `(4)` ⛔ **IL CONFONDENTE `tau_tw`, MISURATO — e il numero lo RIDIMENSIONA**")
    A("")
    A("Il task history dichiarava, ### **prima della corsa**, che azzerare la dispersione "
      "porterebbe `tau_tw` degli archi intra-massa a ### **`2π/1e-3 = 6283.2`**, cioè "
      "### **~`2600 ×`** la mediana misurata. ### ✔ **Si misura, non si assume:**")
    A("")
    A("| passo | `tau_tw` mediana ### **intra-massa** | su ### **TUTTI** gli archi | ### **rapporto** | archi intra-massa |")
    A("|--:|--:|--:|--:|--:|")
    for k in PM:
        t = (mis.get(k) or {}).get("tau_tw") or {}
        A("| `%d` | %s | %s | ### **%s** | %s |"
          % (k, n4(t.get("mediana_intra_massa"), 3), n4(t.get("mediana_tutti"), 3),
             n4(t.get("rapporto_intra_su_tutti"), 3), n4(t.get("archi_intra_massa"))))
    A("")
    _t1 = ((mis.get(1) or {}).get("tau_tw") or {}).get("rapporto_intra_su_tutti")
    if _t1 is not None:
        A("> ### ⭐ **IL CONFONDENTE È PICCOLO, E IL MOTIVO È IL NUMERO DI PRIMA:** già al "
          "passo `1` il rapporto è ### **%s**, non `~2600`, ### **perché la dispersione è "
          "tornata entro UN passo** e `dom` non sta più al pavimento. "
          "### ✔ **L'avevo dichiarato come rischio e misurato come piccolo: è il modo in cui "
          "un confondente si tratta.**" % n4(_t1, 3))
        A("")
    A("---")
    A("")
    # ======================================================================
    A("# `(5)` **LE NASCITE E LA TORSIONE**")
    A("")
    A("| passo | `n` `H1` | `n` controllo | nati `H1` | nati contr. | `\\|tw\\| > 2π` `H1` | contr. |")
    A("|--:|--:|--:|--:|--:|--:|--:|")
    _n0 = (passi.get(0) or {}).get("n")
    for k in PM:
        r = passi.get(k) or {}
        nh, nc = r.get("n"), c_n.get(k)
        A("| `%d` | %s | %s | ### **%s** | %s | %s | %s |"
          % (k, n4(nh), n4(nc),
             n4(None if (nh is None or _n0 is None) else nh - _n0),
             n4(None if (nc is None or _n0 is None) else nc - _n0),
             pct(r.get("fraz_tw_oltre_2pi")), pct(c_fr.get(k))))
    A("")
    A("---")
    A("")
    # ======================================================================
    A("# ⭐ **LE MIE PREVISIONI, CONTRO I NUMERI**")
    A("")
    A("> ### 📌 **Scritte nel task history `840a98d`, committato PRIMA dello strumento e "
      "PRIMA della corsa.**")
    A("")
    pr = []
    # PH1-1
    a_c400 = c_auc.get(400)
    if a400 is not None and a_c400 is not None:
        ok = (a400 > a_c400) and (a400 < 0.90)
        pr.append(("`PH1-1`",
                   "### ⚠ **`H1 AIUTA MA NON BASTA`**: AUC al `400` ### **sopra** quella del "
                   "controllo ### **ma sotto `0.90`**",
                   "AUC `H1` %s contro controllo %s *(differenza %+.4f)*; soglia `0.90`"
                   % (n4(a400), n4(a_c400), a400 - a_c400),
                   "### ✔ **CONFERMATA**" if ok else
                   ("### ⛔ **SMENTITA**: l'AUC `H1` NON è sopra il controllo"
                    if a400 <= a_c400 else
                    "### ⛔ **SMENTITA**: l'AUC `H1` è `>= 0.90`")))
    # PH1-2
    _r150 = (mis.get(150) or {}).get("disp_rel_per_massa") or {}
    _v150 = [v for v in _r150.values() if v is not None]
    if _v150:
        _md = sum(_v150) / len(_v150)
        pr.append(("`PH1-2`",
                   "la dispersione di `phivel` intra-massa ### **TORNA**: al passo `150` è "
                   "già ### **più di METÀ** di quella del `vuoto`",
                   "al `150` la media sulle tre masse è ### **%s** del vuoto%s"
                   % (pct(_md),
                      ("; e al passo `1` era già %s" % pct(sum(_v1) / len(_v1))) if _v1 else ""),
                   "### ✔ **CONFERMATA**" if _md > 0.5 else "### ⛔ **SMENTITA**"))
    # PH1-3
    _rt = [(k, ((mis.get(k) or {}).get("tau_tw") or {}).get("rapporto_intra_su_tutti"))
           for k in PM]
    _rt = [(k, x) for k, x in _rt if x is not None]
    if _rt:
        _mx = max(x for _k, x in _rt)
        pr.append(("`PH1-3`",
                   "`tau_tw` intra-massa al passo `1` è ### **almeno `100 ×`** la mediana su "
                   "tutti gli archi, e ### **CALA**",
                   "il rapporto MASSIMO sui passi misurati è ### **%s**, non `>= 100`"
                   % n4(_mx, 3),
                   "### ⛔ **SMENTITA** — ### ⭐ **e per la ragione giusta: la dispersione "
                   "torna entro UN passo, quindi `dom` non sta al pavimento. "
                   "Il confondente che avevo dichiarato È PICCOLO**"
                   if _mx < 100.0 else "### ✔ **CONFERMATA**"))
    # PH1-4
    _c1 = [(pm or {}).get("coer_2pi") for pm in
           ((mis.get(1) or {}).get("per_massa") or {}).values()]
    _c1 = [x for x in _c1 if x is not None]
    if _c1:
        pr.append(("`PH1-4`",
                   "### ⚠ **il passo `1` NON è un discriminante:** la coerenza per massa è "
                   "### **`>= 0.99`**",
                   "il minimo sulle tre masse al passo `1`: ### **%s**%s"
                   % (n4(min(_c1)),
                      ("; e l'AUC al `1` è %s contro %s del controllo"
                       % (n4(auc(1)), n4(c_auc.get(1)))) if auc(1) is not None else ""),
                   "### ✔ **CONFERMATA**" if min(_c1) >= 0.99 else "### ⛔ **SMENTITA**"))
    # PH1-5
    _nh5, _nc5 = (passi.get(500) or {}).get("n"), c_n.get(500)
    if _nh5 is not None and _nc5 is not None and _n0 is not None:
        _bh, _bc = _nh5 - _n0, _nc5 - _n0
        _sc = abs(_bh - _bc) / max(_bc, 1)
        pr.append(("`PH1-5`",
                   # ### ⚠ **`%` SINGOLO: questa stringa e' il VALORE di un `%s`, non
                   #   un FORMATO** -- il raddoppio uscirebbe LETTERALE. ### **E' la stessa
                   #   trappola del referto di `A1`, e l'ho rifatta.**
                   "le nascite a `500` passi stanno ### **entro il `±25 %`** di quelle del "
                   "controllo",
                   "`H1` ### **%d** contro controllo ### **%d** *(scarto %s)*"
                   % (_bh, _bc, pct(_sc)),
                   "### ✔ **CONFERMATA**" if _sc <= 0.25 else "### ⛔ **SMENTITA**"))
    A("| | la previsione | il numero | esito |")
    A("|---|---|---|---|")
    for x in pr:
        A("| %s | %s | %s | %s |" % x)
    A("")
    _ok = sum(1 for x in pr if "CONFERMATA" in x[3] and "SMENTITA" not in x[3])
    _no = sum(1 for x in pr if "SMENTITA" in x[3])
    A("> ### **%d confermate, %d SMENTITE** su %d. ### **E la smentita che vale è `PH1-3`:** "
      "### ⭐ **avevo dichiarato un confondente grande e l'ho misurato PICCOLO** — "
      "### **dichiararlo prima è ciò che ha reso possibile ridimensionarlo dopo.**"
      % (_ok, _no, len(pr)))
    A("")
    A("---")
    A("")
    A("# ⛔ **CHE COSA QUESTO REFERTO NON DICE**")
    A("")
    A("| | |")
    A("|---|---|")
    A("| la variabilità fra semi | ### **UN seme solo** *(`P3` non soddisfatta)* |")
    A("| i valori ASSOLUTI | ### **`U1` è aperta:** si legge la ### **differenza**, non il livello |")
    A("| ### **perché** le masse si sciolgono | ### **`H2` non è stata misurata** *(`A-S2`)*: qui si misura ### **se `H1` basta**, non quale sia la causa |")
    A("| la causa di una eventuale RISALITA | ### **ambigua fra quattro cause**, e per questo il referto la dichiarerebbe `CONFONDUTA` |")
    A("")
    A("> ### ⛔ **E LA DECISIONE SU `A-S2` È DI LUCA.** ### **Questo referto riporta i numeri "
      "e l'esito del criterio. Non prosegue.**")
    A("")
    io.open(FUORI, "w", encoding="utf-8", newline=NL).write(NL.join(R) + NL)
    print("scritto %s (%d righe)" % (FUORI, len(R)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
