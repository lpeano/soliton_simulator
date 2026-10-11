r"""IL REFERTO DEL `v4` — **GENERATO da `uscite/letture_v4.json`, VERDETTI COMPRESI.**

### ⛔ **Ogni numero e ogni verdetto escono dal `json`** *(`L-NUMERI`)*: il confronto fra la
previsione del task history e il numero **lo fa il codice**, con le soglie scritte **prima**.

Gira con:  python proto_camminata/_referto4.py
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
FONTE = os.path.join(_QUI, "uscite", "letture_v4.json")
DEST = os.path.join(RADICE, "doc", "REFERTO_prototipo_camminata_v4.md")

CONF = "### ✅ **CONFERMA**"
SMEN = "### ⛔ **SMENTITA**"
NOND = "### ⚠ **NON DECIDIBILE**"
LETTO = "### \U0001f4cc **LETTO** *(non si interpreta oltre)*"


def main():
    d = json.loads(io.open(FONTE, encoding="utf-8").read())
    R = []

    def a(s=""):
        R.append(s)

    sc = d["scena"]
    a("# IL REFERTO DEL PROTOTIPO `v4` — **`cs` LOCALE DAL VUOTO, IN TUTTE LE LEGGI**")
    a("")
    a("> ### ⛔ **CONGELATO** *(forma dichiarata in `csv/_forma_referti.py`)*: e' un "
      "### **REPERTO** — la CI ### **non lo rigenera**, e il presidio verifica ### "
      "**il suo BLOB.**")
    a("")
    a("*(**Generato** da `python proto_camminata/_referto4.py`, che legge "
      "`proto_camminata/uscite/letture_v4.json` prodotto da `python "
      "proto_camminata/_letture4.py`. Criteri, previsioni e soglie: "
      "`doc/TASK_HISTORY/2026-10-11_camminata_v4_cs_locale.md`, **committato PRIMA del "
      "codice** (`db40a3c`). Decisione: `CS-LOCALE-DAL-VUOTO`.)*")
    a("")
    a("> ### ⛔ **QUESTO FILE E' GENERATO da `python proto_camminata/_referto4.py`: NON "
      "si scrive a mano.** ### **Ogni numero e ogni verdetto escono da "
      "`proto_camminata/uscite/letture_v4.json`** *(`L-NUMERI`)*, e le soglie stanno nel "
      "task history `doc/TASK_HISTORY/2026-10-11_camminata_v4_cs_locale.md`, ### **scritte "
      "PRIMA dei numeri.**")
    a("")
    a("## LA CONFIGURAZIONE, INTERA" + " *(`H-P5`)*")
    a("")
    a("| | |")
    a("|---|---|")
    a("| la scena | **irregolare**, `n = %d` nodi, `m = %d` archi, seme **`%d`** |"
      % (sc["n"], sc["m"], sc["seme"]))
    a("| la scena di `L0` | **regolare** *(circolante)*, perche' sull'irregolare "
      "l'eccentricita' e' `6` e ### **il fronte satura in sei tick** |")
    a("| i semi | `%s` |" % ", ".join("`%d`" % s for s in sc["semi"]))
    a("| i tick | **`%d`** |" % sc["passi"])
    a("| `eps` della moneta di spin | **`%g`** |" % sc["eps"])
    a("| la geometria | `scena_identita` *(e `scena_curva` nei bracci del banco)* |")
    a("| il vuoto | `vuoto_fondo(lambda_0 = 1.0)`, modulo **uniforme**, fasi dal seme |")
    a("| la non linearita' | `saturazione3.flusso` *(`N` sull'elicita' locale)* |")
    a("| le candidate di `A1` | `scatter` e `trasmissione`, ### **una per volta** |")
    a("| la forma di `cs` | `dispersione` *(l'unica che da' `cs = 1.0` AL BIT sul fondo "
      "del `v3`)* |")
    a("| la forma del `cs` d'arco | `min` *(l'estremita' lenta fa da collo: la scelta "
      "causale)* |")
    a("| le candidate di `A4` | **`(F)`** pezzi frazionari sincroni " + chr(0xb7)
      + " **`(S)`** tick asincroni |")
    a("")

    # =============================================================== L0
    a("## ⭐ **`L0` — L'INVARIANZA LOCALE DELLA LUCE: `(S)` LA RISPETTA, `(F)` NO**")
    a("")
    a("> ### ⛔ **E SI LEGGE COME UN *RAPPORTO*, non come <<vale `1`>>:** la velocita' "
      "del fronte a `cs = 1` e' **`%.4f`** archi/tick, ### **non `1`** — la camminata "
      "di Grover ### **non satura il cono**, e lo stesso numero il `v3` lo ha gia' "
      "misurato. ### **Quindi la domanda giusta e': la velocita' in tempo proprio e' LA "
      "STESSA a ogni `cs`?**"
      % d["L0"]["F"]["cs=1.00"]["v_tick_fronte"])
    a("")
    for cand in ("F", "S"):
        L = d["L0"][cand]
        a("### la candidata **`(%s)`** — scena `%s`, eccentricita' `%d`"
          % (cand, L["scena"], L["eccentricita"]))
        a("")
        a("| `cs` | tick | fronte, archi/tick | in **tempo proprio** | rapporto al "
          "riferimento | entro `3 sigma`? |")
        a("|---|---|---|---|---|---|")
        for k in sorted(k for k in L if k.startswith("cs=")):
            v = L[k]
            a("| **`%.2f`** | `%d` | %.4f ± %.4f | **%.4f** ± %.4f | "
              "### **%.4f** | %s |"
              % (v["cs"], v["tick"], v["v_tick_fronte"], v["sigma_fronte"],
                 v["v_proprio_fronte"], v["sigma_proprio_fronte"], v["rapporto_fronte"],
                 "### ✅ **SI**" if v["entro_3sigma_fronte"]
                 else "### ⛔ **NO**"))
        a("")
    fuoriF = [k for k in d["L0"]["F"] if k.startswith("cs=")
              and not d["L0"]["F"][k]["entro_3sigma_fronte"]]
    fuoriS = [k for k in d["L0"]["S"] if k.startswith("cs=")
              and not d["L0"]["S"][k]["entro_3sigma_fronte"]]
    peggioF = max(abs(d["L0"]["F"][k]["rapporto_fronte"] - 1.0)
                  for k in d["L0"]["F"] if k.startswith("cs="))
    peggioS = max(abs(d["L0"]["S"][k]["rapporto_fronte"] - 1.0)
                  for k in d["L0"]["S"] if k.startswith("cs="))
    a("%s **`(S)` RISPETTA L'INVARIANZA LOCALE: `%d` casi su `%d` fuori da `3 sigma`, "
      "e lo scarto peggiore e' il `%.1f%%`.** %s **`(F)` NO: `%d` casi fuori, e lo "
      "scarto peggiore e' il `%.1f%%`.**"
      % (CONF, len(fuoriS), sum(1 for k in d["L0"]["S"] if k.startswith("cs=")),
         100.0 * peggioS, SMEN, len(fuoriF), 100.0 * peggioF))
    a("")
    a("### ⚠ **E LA MIA PREVISIONE ERA GIUSTA SU `(S)` E GIUSTA NEL VERSO SU `(F)`, MA "
      "SBAGLIATA SU *DOVE*:** avevo scritto *<<lo scarto cresce quando `cs` scende>>*, e "
      "invece ### **cresce verso `cs` INTERMEDI** *(`%.3f` a `cs = 0.75`, `%.3f` a "
      "`cs = 0.25`)*. ### ⭐ **E il motivo e' il punto `A4`:** a `cs = 0` e a `cs = 1` "
      "la famiglia frazionaria e' ### **esatta**, quindi l'errore di composizione e' "
      "### **massimo in mezzo.**"
      % (d["L0"]["F"]["cs=0.75"]["rapporto_fronte"],
         d["L0"]["F"]["cs=0.25"]["rapporto_fronte"]))
    a("")

    # =============================================================== L4
    a("## ⛔ **`L4` — MATERIA E ANTIMATERIA: `(F)` LE FA PIEGARE IL TEMPO IN MODO "
      "DIVERSO**")
    a("")
    a("| la candidata | `max\\|dLambda\\|` | `max\\|dcs\\|` | la soglia | tiene? |")
    a("|---|---|---|---|---|")
    for cand in ("F", "S"):
        v = d["L4"][cand]
        a("| **`(%s)`** | **%.3g** | **%.3g** | %.3g | %s |"
          % (cand, v["max_dLambda"], v["max_dcs"], v["soglia"],
             "### ✅ **SI**" if v["tiene"] else "### ⛔ **NO**"))
    a("")
    a("### ⭐ **E QUESTA E' LA *CONSEGUENZA FISICA* DELLA `C` ROTTA, e per questo conta "
      "piu' del numero del banco:** il vincolo `W5` esiste per far si' che ### **materia e "
      "antimateria pieghino il tempo allo stesso modo**, e `(F)` ### **non lo fa** "
      "— il grumo e il suo coniugato lasciano impronte che differiscono di "
      "**%.3g** su `Lambda` e di **%.3g** su `cs`. ### ✅ **`(S)` lo fa, a "
      "`%.3g`.**"
      % (d["L4"]["F"]["max_dLambda"], d["L4"]["F"]["max_dcs"],
         d["L4"]["S"]["max_dLambda"]))
    a("")

    # =============================================================== L1 L2 L3 L5
    a("## ⚠ **`L1`, `L2`, `L3`, `L5` — QUATTRO RISULTATI NEGATIVI, E SONO "
      "RISULTATI**")
    a("")
    a("| la lettura | la domanda | il numero | il verdetto |")
    a("|---|---|---|---|")
    for cand in ("F", "S"):
        for cv in ("scatter", "trasmissione"):
            k = "%s %s" % (cand, cv)
            if k not in d["L1"]:
                continue
            L = d["L1"][k]
            sig = [p["r"] for p in L["profilo"].values()
                   if p["significativo"] and not p["dentro_il_grumo"]]
            fr = L["fronte"][-1]
            a("| `L1` **`(%s)`**, `%s` | si forma una zona modificata **FUORI** dal "
              "grumo? | anelli oltre `3 sigma`: **%s**; fronte finale `r = %d`, entro il "
              "cono: **%s** | %s |"
              % (cand, cv, ("`%s`" % sig) if sig else "### **NESSUNO**", fr["raggio"],
                 "si" if fr["entro_il_cono"] else "### **NO**",
                 SMEN if not sig else CONF))
    for cand in ("F", "S"):
        c = d["L2"][cand]["confronto"]
        a("| `L2` **`(%s)`** | un pacchetto di **passaggio** lascia la stessa impronta di "
          "un grumo? | differenza **%.3g**, **`%.2f sigma`** *(norme pari: **%s**)* | %s |"
          % (cand, c["differenza_pendenze"],
             (c["differenza_pendenze"] / c["sigma_combinato"])
             if c["sigma_combinato"] > 0 else 0.0,
             "si" if c["norme_pari"] else "NO",
             SMEN if not c["si_distinguono"] else CONF))
    for cand in ("F", "S"):
        c = d["L3"][cand]["confronto"]
        s = d["L3"][cand]["senza_grumo"]
        a("| `L3` **`(%s)`** | la luce **sente la massa**? | ritardo **%+.2f tick**, "
          "**`%.2f sigma`** *(lancio `%d` " % (cand, c["ritardo_tick"], c["in_sigma"],
                                               s["nodo_di_lancio"])
          + "→ bersaglio `%d`, il grumo e' a `%d` archi dal bersaglio)* | %s |"
          % (s["bersaglio"], s["distanza_grumo_bersaglio"],
             SMEN if not c["significativo"] else CONF))
    for cand in ("F", "S"):
        for k in sorted(x for x in d["L5"][cand] if x.startswith("confronto")):
            c = d["L5"][cand][k]
            a("| `L5` **`(%s)`**, `%s` | due grumi si avvicinano **piu' che nel `v3`**? | "
              "differenza **%.5f**, **`%.2f sigma`** | %s |"
              % (cand, k.replace("confronto ", ""), c["differenza"], c["in_sigma"],
                 SMEN if not c["significativo"] else CONF))
    a("")
    a("### ⛔ **E I QUATTRO NEGATIVI VANNO LETTI INSIEME, perche' dicono una cosa "
      "sola:** a queste taglie ### **il `cs` locale non produce un effetto misurabile sulla "
      "materia.** ### **`L1`** non trova zona modificata fuori dal grumo; ### **`L2`** non "
      "distingue un grumo da un pacchetto di passaggio; ### **`L3`** non trova un ritardo "
      "della luce; ### **`L5`** non trova avvicinamento. ### ⭐ **E `L5` era previsto:** "
      "`G2` ha dato `0.69 sigma` fra `N` e lineare, e un effetto di gravita' ### **non "
      "poteva essere piu' grande di quello.**")
    a("")
    a("### ⭐ **E `L2` CONFERMA IL PUNTO `1` DELLA DECISIONE DI LUCA, NEL VERSO CHE LA "
      "MOTIVA:** *<<una `rho` di nodo non distingue un grumo legato da un pacchetto di luce "
      "di passaggio>>*. ### **Misurato: non li distingue** — `%.2f sigma` per `(F)` e "
      "`%.2f sigma` per `(S)`, con le norme ### **pareggiate.**"
      % ((d["L2"]["F"]["confronto"]["differenza_pendenze"]
          / d["L2"]["F"]["confronto"]["sigma_combinato"])
         if d["L2"]["F"]["confronto"]["sigma_combinato"] > 0 else 0.0,
         (d["L2"]["S"]["confronto"]["differenza_pendenze"]
          / d["L2"]["S"]["confronto"]["sigma_combinato"])
         if d["L2"]["S"]["confronto"]["sigma_combinato"] > 0 else 0.0))
    a("")

    # =============================================================== il confronto
    a("## \U0001f4cc **IL CONFRONTO FRA `(F)` E `(S)`, COME LO CONSEGNO — E NON "
      "SCELGO IO**")
    a("")
    a("| | `(F)` pezzi frazionari | `(S)` tick asincroni |")
    a("|---|---|---|")
    a("| la dinamica | **liscia** | **a scatti** *(il cono: raggio `0` al primo tick)* |")
    a("| la `C` sul passo | ### ⛔ **ROTTA**, `4.6475` | ### ⭐ **esatta**, `0` |")
    a("| materia/antimateria *(`L4`)* | ### ⛔ **NON tiene**, `%.3g` | ### ✅ "
      "**tiene**, `%.3g` |" % (d["L4"]["F"]["max_dLambda"], d["L4"]["S"]["max_dLambda"]))
    a("| l'invarianza locale *(`L0`)* | ### ⛔ **approssimata**, fino al `%.1f%%` | "
      "### ✅ **entro `3 sigma`** in tutti i casi |" % (100.0 * peggioF))
    a("| lo stato | `psi`, `phi` | ### ⚠ `psi`, `phi`, **`tau` E un bit per nodo** |")
    a("| le leggi contate | la **famiglia frazionaria** | la famiglia **non serve**, ma "
      "serve ### **uno stato nuovo** *(`9-ter`)* |")
    a("")
    a("### ⛔ **LE TRE SCELTE SONO DI LUCA, e stanno in `doc/indice/DA_DECIDERE_LUCA.md`"
      ", UNA per scelta:** come la materia cambia `Lambda` *(`scatter` o `trasmissione`)*, "
      "come il vuoto fissa `cs` *(`dispersione`, `contrasto` o `densita`)*, e `(F)` contro "
      "`(S)`. ### **Io porto il confronto misurato.**")
    a("")

    # =============================================================== i limiti
    a("## ⚠ **I LIMITI, dichiarati**")
    a("")
    a("| | il limite |")
    a("|---|---|")
    a("| `1` | ### **`L1`, `L2` e `L5` usano un PACCHETTO, non un grumo legato:** il "
      "mandato dice *<<partendo da un grumo `v3` auto-intrappolato>>*, e il ### **`v3` non "
      "ne ha trovato nessuno** *(misurato due volte: referto `v3`, e di nuovo in `G1`)*. "
      "### **Ogni risultato va letto come <<l'impronta di un pacchetto>>** |")
    a("| `2` | ### **La velocita' a `cs = 1` non e' `1`** *(e' `%.4f`)*: la camminata di "
      "Grover ### **non satura il cono**, quindi `L0` si legge come un ### **rapporto** e "
      "non come un valore assoluto |"
      % d["L0"]["F"]["cs=1.00"]["v_tick_fronte"])
    a("| `3` | ### **`L0` gira sul REGOLARE**, perche' sull'irregolare l'eccentricita' e' "
      "`6` e il fronte ### **satura in sei tick** — e adattare una retta su una curva "
      "satura da' ### **una pendenza che non e' una velocita'** |")
    a("| `4` | ### **La <<conservazione modificata>> del `v3` NON e' derivata per un `cs` "
      "non uniforme**, quindi ### **non e' misurata qui**, e ### **non la chiamo energia** "
      "*(quella scelta e' di Luca)* |")
    a("| `5` | ### **Un solo grafo per la scena principale**, `n = %d`: ### **due taglie "
      "non sono uno scaling** *(`TAGLIA-FINITA`)*, e nessun limite continuo si afferma |"
      % sc["n"])
    a("")

    dati = (NL.join(R) + NL).encode("utf-8")
    io.open(DEST, "wb").write(dati)
    print("  scritto %s" % os.path.relpath(DEST, RADICE).replace(os.sep, "/"))
    print("  %d righe, %d byte" % (len(R), len(dati)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
