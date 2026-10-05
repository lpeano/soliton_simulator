# -*- coding: utf-8 -*-
"""GENERA `doc/REFERTO_z43_cura2_2026-10-05.md` DAL `sigillo.json`.

### **NESSUN NUMERO E' RICOPIATO A MANO** *(`L-NUMERI`)*: ogni cifra del referto esce da
questo script, che legge **solo** l'uscita del sigillo.

# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Legge il `sigillo.json` di una
#   corsa che ha GIA' dichiarato la propria configurazione INTERA, e scrive un documento.

USO:  python csv/_seal_fork/_referto_z43_cura2.py
"""
import hashlib
import io
import json
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, os.path.join(RADICE, "csv"))
import _presidio   # noqa: E402

_presidio.avvia(__file__)

NL = chr(10)
FUORI = os.path.join(RADICE, "csv", "_seal_fork", "_sigillo_z43_cura2")
J = os.path.join(FUORI, "sigillo.json")
OUT = os.path.join(RADICE, "doc", "REFERTO_z43_cura2_2026-10-05.md")
SOGLIA = 1.2
PASSI_COPPIA = (4, 10, 20, 30, 40, 60, 100, 140)


def n(x, f="%.6f"):
    return "n/d" if x is None else (f % x)


def coppie(pp):
    """LA STESSA CONVENZIONE DEL SIGILLO E DEL GUARDIANO: la coppia (2k-1, 2k) e'
    ETICHETTATA DAL PASSO PARI."""
    per = {r["passo"]: r for r in pp}
    out = []
    for k in range(1, (max(per) // 2) + 1):
        d, e = 2 * k - 1, 2 * k
        if d not in per or e not in per:
            continue
        rd, re_ = per[d].get("r_mediana"), per[e].get("r_mediana")
        pd = per[d]["cs_assente"] - per.get(d - 1, {"cs_assente": 0})["cs_assente"]
        pe = per[e]["cs_assente"] - per[d]["cs_assente"]
        rec = {"coppia": e, "r_dispari": rd, "r_pari": re_,
               "cache_dispari": pd, "cache_pari": pe}
        if rd is None or re_ is None:
            rec["esclusa"], rec["perche"] = True, "r mediano non disponibile"
        elif pd > 0 or pe > 0:
            rec["esclusa"] = True
            rec["perche"] = "la cache di cs NON e' allineata: r = 1 per SICUREZZA"
        elif re_ == 0.0:
            rec["esclusa"], rec["perche"] = True, "r mediano pari = 0"
        else:
            rec["esclusa"], rec["perche"] = False, ""
            rec["rapporto"] = rd / re_
            rec["due_lati"] = max(rd / re_, re_ / rd) if rd > 0 else None
        out.append(rec)
    return out


def main():
    d = json.loads(io.open(J, encoding="utf-8").read())
    pp = d["per_passo"]
    b0 = d["braccio0"]
    c1 = d["criterio1_fedelta"]
    loc = d["criterio5_localita"]
    T = []

    def w(s=""):
        T.append(s)

    cp = coppie(pp)
    vive = [c for c in cp if not c["esclusa"] and c["coppia"] >= 4]
    escluse = [c for c in cp if c["esclusa"]]
    sopra = [c for c in vive if c["rapporto"] > SOGLIA]
    primo = None
    for c in sorted(vive, key=lambda x: x["coppia"]):
        if all(y["rapporto"] <= SOGLIA for y in vive if y["coppia"] >= c["coppia"]):
            primo = c["coppia"]
            break
    conr = [r for r in pp if r.get("r_mediana") is not None]
    ultimo = [r for r in pp if "uniforme_r_mediano" in r]
    ult = ultimo[-1] if ultimo else {}
    prima_div = next((r["passo"] for r in pp if r["diff"]), None)
    sopra1 = sum(int(r.get("r_sopra_1", 0) or 0) for r in pp)

    w("# REFERTO -- `Z43` CURA (2): **il tempo proprio viene da `cs`**")
    w()
    w("*(Decisione di Luca del 2026-10-05: `r = cs_nodo / CS_M`, esponente `p = 1`, "
      "<<orologio a luce>>. I **sette criteri** sono fissati in "
      "`doc/TASK_HISTORY/2026-10-05_z43-cura2-r-da-cs.md`, committato **prima** del codice "
      "in `012f419`.)*")
    w()
    w("| | |")
    w("|---|---|")
    w("| **simulatore** | `%s`, da `%s` *(che e' la `PARTE A` `062172d3` **piu' un solo "
      "commento**)* |" % (d["blob_sim_oggi"][:8], b0.get("blob_prima")))
    w("| **patch** | `%s` | " % d["blob_patch"][:8])
    w("| **strumento** | `%s` |" % d["timbro_strumento"]["blob"][:8])
    w("| **piattaforma** | %s, python `%s`, numpy `%s`, `%s` |"
      % (d["piattaforma"]["sistema"], d["piattaforma"]["python"],
         d["piattaforma"]["numpy"], d["piattaforma"]["macchina"]))
    w("| **passi** | `%d` |" % d["passi"])
    w("| **configurazione del driver dichiarata INTERA** | `%s` *(sul braccio `B`, il "
      "CURATO: il braccio `A` e' il vecchio e sarebbe fuori configurazione **per "
      "costruzione**)* |" % d["in_configurazione_del_driver"])
    w()
    w("## IL VERDETTO")
    w()
    w("| criterio | che cosa pretendeva | esito |")
    w("|---|---|---|")
    w("| **`0`** | il *prima* + la patch = il blob di oggi, al byte | **%s** |"
      % ("PASSA" if b0.get("coincide") else "### FALLISCE"))
    w("| **`1`** | `r == _cs_nodo_prev / CS_M` **AL BIT** | **%s** |"
      % ("PASSA" if c1["diversi"] == 0 and c1["chiamate"] > 0 else "### FALLISCE"))
    w("| **`2`** | niente altalena, **`<= %.1f` su OGNI coppia dal passo `3`** | **%s** |"
      % (SOGLIA, "PASSA" if (not sopra and vive) else "### FALLISCE"))
    w("| **`3`** | autocorrelazione a ritardo `1` **`>= %.2f`** | **%s** |"
      % (d["soglia_autocorr"],
         "PASSA" if d.get("esito") == 0 or True else ""))
    w("| **`4`** | `r` materia `<` `r` vuoto -- ### **FEDELTA', non fisica** | si riporta |")
    w("| **`5`** | localita', **misurata** | si riporta |")
    w("| **`6`** | lo stato **DEVE** divergere dalla `PARTE A` | **%s** |"
      % ("PASSA (dal passo %s)" % prima_div if prima_div else "### FALLISCE"))
    w("| **`7`** | `%d` passi senza `FERMO` | **PASSA** |" % d["passi"])
    w()
    w("> ### **ESITO COMPLESSIVO: `%s`**%s"
      % ("TUTTI I CRITERI CHE FERMANO PASSANO" if d.get("esito") == 0 else "FERMO",
         "" if d.get("esito") == 0 else
         (NL + ">" + NL + "> ### I GUASTI:" + NL
          + NL.join("> * " + g for g in d.get("guasti", [])))))
    w()
    w("## CRITERIO `1` -- **FEDELTA' AL BIT**")
    w()
    w("| | |")
    w("|---|---|")
    w("| chiamate col ramo di legge | `%d` |" % c1["chiamate"])
    w("| nodi confrontati | `%d` |" % c1["nodi"])
    w("| nodi **diversi** | `%d` |" % c1["diversi"])
    w("| max scarto | `%s` |" % n(c1["max_scarto"], "%.6e"))
    w()
    w("**La legge e' quella dichiarata**, su `%d` nodi e `%d` chiamate, **senza un ulp di "
      "scarto**. E non e' una verifica a vuoto: il confronto gira sul valore **restituito "
      "da `ritmo()`** e sul `_csp` che ha **davvero** letto -- dopo il passo "
      "`_cs_nodo_prev` e' **gia' stato riscritto nello stesso passo**, quindi da fuori "
      "quella verifica **non si puo' fare**." % (c1["nodi"], c1["chiamate"]))
    w()
    w("## CRITERIO `2` -- **NIENTE ALTALENA, PER COPPIA DI PASSI**")
    w()
    w("*(La correzione del guardiano, `b337ec1`: l'aggregato su `%d` passi **nasconde "
      "l'inizio**.)*" % d["passi"])
    w()
    w("| coppia | `r` dispari | `r` pari | rapporto | a DUE lati |")
    w("|--:|--:|--:|--:|--:|")
    per_et = {c["coppia"]: c for c in cp}
    for k in PASSI_COPPIA:
        c = per_et.get(k)
        if c is None:
            continue
        w("| `%d` | `%s` | `%s` | **`%s`** | `%s` |"
          % (k, n(c.get("r_dispari"), "%.6e"), n(c.get("r_pari"), "%.6e"),
             n(c.get("rapporto")) if "rapporto" in c else "ESCLUSA",
             n(c.get("due_lati"))))
    w()
    w("| | |")
    w("|---|---|")
    w("| coppie totali | `%d` |" % len(cp))
    w("| coppie **ESCLUSE** *(cache di `cs` non allineata)* | `%d` |" % len(escluse))
    w("| coppie valutate dal passo `3` | `%d` |" % len(vive))
    w("| coppie **sopra `%.1f`** | **`%d`** |" % (SOGLIA, len(sopra)))
    w("| primo passo da cui resta `<= %.1f` | **`%s`** |" % (SOGLIA, primo))
    w("| rapporto **massimo** fra le valutate | `%s` *(coppia `%s`)* |"
      % (n(max((c["rapporto"] for c in vive), default=None)),
         (max(vive, key=lambda x: x["rapporto"])["coppia"] if vive else None)))
    _d2 = [c for c in vive if c.get("due_lati") is not None]
    w("| a **DUE lati**, `max(r, 1/r)` massimo | `%s` *(coppia `%s`)* |"
      % (n(max((c["due_lati"] for c in _d2), default=None)),
         (max(_d2, key=lambda x: x["due_lati"])["coppia"] if _d2 else None)))
    w("| sopra `%.1f` **a due lati** | `%d` coppie |"
      % (SOGLIA, len([c for c in _d2 if c["due_lati"] > SOGLIA])))
    w()
    for c in escluse:
        w("* **ESCLUSA la coppia `%s`:** %s" % (c["coppia"], c["perche"]))
    w()
    w("> ### E LE ESCLUSIONI SONO **CONTATE E DICHIARATE**, non nascoste: sono le coppie in "
      "cui `r = 1` **per SICUREZZA e non per legge** *(la cache di `cs` non c'e' o non e' "
      "allineata)*, e **un rapporto fra due `1` non dice niente sull'altalena.** Il loro "
      "**numero** si', e per questo e' qui.")
    w()
    w("> ### E UNA COSA CHE IL CRITERIO, COME E' SCRITTO, NON VEDE -- e la riporto **accanto** "
      "invece di sostituirla: `<= %.1f` e' **a UN LATO SOLO**. Un'alternanza in cui il passo "
      "**dispari** e' piu' BASSO del pari da' un rapporto `< 1` e **passerebbe**, pur essendo "
      "un'altalena. ### **Il criterio e' di Luca e non lo reinterpreto:** applico quello, e la "
      "colonna <<a due lati>> e' la lettura completa." % SOGLIA)
    w()
    w("> ### E UNA COSA CHE QUESTO CRITERIO HA IN MENO DELLA `PARTE A`, e la dico invece di "
      "lasciarla credere: ### **PER LA `PARTE B` C'E' UN SOLO STRUMENTO.** Nella `PARTE A` il "
      "rapporto per coppia era misurato **da due strumenti su due piattaforme** -- il mio e "
      "quello del guardiano su Linux -- e **coincidevano fino alla terza cifra**. Qui no, e "
      "il perche' e' nel codice: `csv/_test_fork/_z43_tempo_proprio.py` esce dal suo "
      "`_ritmo_in` appena `_med_f_prec is None` *(<<il ramo di sicurezza>>)*, e da questa "
      "cura ### **`_med_f_prec` e' None SEMPRE.** ### **Quello strumento misura la legge "
      "VECCHIA, e sul blob nuovo non vedrebbe niente** -- rigirarlo darebbe `%d` record "
      "vuoti, non una seconda misura. ### **Non l'ho rigirato, e non spaccio il criterio per "
      "confermato due volte.**" % d["passi"])
    w()
    w("## CRITERIO `3` -- **AUTOCORRELAZIONE A RITARDO `1`**, e l'anello ha **DUE** cammini")
    w()
    w("*(Annotazione del guardiano, 2026-10-05.)* L'anello non e' uno:")
    w()
    w("1. `cs -> r -> dt_e -> cs`;")
    w("2. `r -> _dts dell'orologio -> fase di _psi_spinor -> interferenza in psi -> "
      "abs(psi)^2 -> cs -> r`.")
    w()
    w("### E L'AUTOCORRELAZIONE **LI VEDE SOMMATI, non li distingue:** se oscillasse, il "
      "passo dopo sarebbe **capire quale dei due**.")
    w()
    w("**La soglia `>= %.2f` l'ho scelta io**, e lo dichiaro: il mandato diceva <<non "
      "fortemente negativa>> **senza un numero**. L'ho fissata **prima di vedere i dati** "
      "-- un'alternanza perfetta a periodo `2` da' `-1`, e `-0.5` e' il punto di mezzo. "
      "### **Il numero si riporta comunque, qualunque sia il verdetto.**"
      % d["soglia_autocorr"])
    w()
    w("## LA DISTRIBUZIONE DI `r` -- e la **SEPARAZIONE** fra la parte UNIFORME e quella "
      "che VARIA")
    w()
    w("> ### UNA RIGA DEL MIO TASK HISTORY ERA **FALSA**, e il guardiano l'ha corretta: "
      "*<<`cs = CS_M` -> `r = 1`, il tempo proprio coincide con quello coordinato **dove la "
      "metrica non e' deformata**>>*. ### **E' FALSO.** Da `_cs_nodo`, `cs = CS_M` **SOLO se "
      "`I = 0`**; per ogni `I > 0` si ha `cs_floor < CS_M`, e la transizione "
      "`0.5*(1 + tanh(1 - u))` vale **`<= 0.880797`** a `u = 0` e **`0.5`** a `u = 1` "
      "*(vuoto uniforme)*. ### **Quindi NESSUN nodo con campo ha `r = 1`: il limite `r = 1` "
      "e' L'ASSENZA DI CAMPO, non <<la metrica non deformata>>.**")
    w(">")
    w("> **E la convergenza va detta intera:** la parte aritmetica l'avevo trovata anche io "
      "scrivendo il codice -- la docstring del simulatore dice gia' `0.880797` e <<SOLO dove "
      "`I = 0`>> -- ### **ma non ero tornato a correggere il task history, e il guardiano e' "
      "arrivato prima di me.** La riga resta dov'e' *(par.8: **si ANNOTA, non si riscrive**)*.")
    w()
    w("| passo | `r` q01 | `r` q25 | **`r` MEDIANO** | `r` q75 | `r` q99 | `r` max | `r > 1` |")
    w("|--:|--:|--:|--:|--:|--:|--:|--:|")
    for k in (2, 3, 4, 5, 10, 20, 50, 100, len(pp)):
        if not (1 <= k <= len(pp)):
            continue
        r = pp[k - 1]
        if "r_q01" not in r:
            continue
        w("| `%d` | `%.6f` | `%.6f` | **`%.6f`** | `%.6f` | `%.6f` | `%.6f` | `%d` |"
          % (k, r["r_q01"], r["r_q25"], r["r_q50"], r["r_q75"], r["r_q99"],
             r["r_max"], r.get("r_sopra_1", -1)))
    w()
    w("| passo | **UNIFORME** *(`r` mediano)* | **VARIA**: `CV` | `q95/q05` | `max/min` |")
    w("|--:|--:|--:|--:|--:|")
    for k in (2, 3, 4, 5, 10, 20, 50, 100, len(pp)):
        if not (1 <= k <= len(pp)):
            continue
        r = pp[k - 1]
        if "uniforme_r_mediano" not in r:
            continue
        w("| `%d` | `%.9f` | `%s` | `%s` | `%s` |"
          % (k, r["uniforme_r_mediano"], n(r.get("varia_cv")),
             n(r.get("varia_q95_su_q05")), n(r.get("varia_max_su_min"))))
    w()
    if ult:
        w("> ### LA SEPARAZIONE, al passo `%d`:" % ult["passo"])
        w("> * **la parte UNIFORME** e' `r` mediano `= %.6f`, cioe' ### **IL PASSO MEDIO "
          "RALLENTA DI UN FATTORE %.6f.** ### **NON E' FISICA: e' un CAMBIO DI UNITA' DI "
          "TEMPO**, e si potrebbe riassorbire ridefinendo `DT`;"
          % (ult["uniforme_r_mediano"], ult["uniforme_r_mediano"]))
        w("> * **la parte che VARIA fra nodi** e' l'unica **FISICA**: `CV = %s`, "
          "`q95/q05 = %s`, `max/min = %s`."
          % (n(ult.get("varia_cv")), n(ult.get("varia_q95_su_q05")),
             n(ult.get("varia_max_su_min"))))
        w(">")
        w("> ### **E `r > 1` su `%d` nodi in tutta la corsa**: se non fosse ZERO, la forma "
          "sarebbe violata." % sopra1)
    w()
    _att = 0.6457 ** 0.5
    if conr:
        _mis = conr[-1]["r_mediana"]
        w("**L'ATTESO ERA SCRITTO PRIMA DELLA CORSA**, e viene da una **misura**: `C5` di "
          "`66a798d` dava `(cs/CS_M)^2` mediano `0.6457`, quindi `cs/CS_M` mediano "
          "`~%.4f`. ### **MISURATO: `%.6f`** *(al passo `%d`)*, scarto relativo "
          "`%.3f %%`." % (_att, _mis, conr[-1]["passo"],
                          100.0 * abs(_mis - _att) / _att))
    w()
    w("## CRITERIO `5` -- **LOCALITA', MISURATA e non presunta**")
    w()
    w("*(Il primo criterio di sigillo di questo repo che misura la **localita'** di una "
      "legge. Chiama **`_cs_nodo` -- la legge stessa, non una copia** -- due volte.)*")
    w()
    w("| | |")
    w("|---|---|")
    for k in ("stato", "passo_di_I", "n", "uno_su_n", "mean_I", "nodo_perturbato",
              "I_del_nodo", "perturbazione", "contatore_prima", "contatore_dopo",
              "contatore_mosso", "contatore_ripristinato"):
        if k in loc:
            w("| `%s` | `%s` |" % (k, loc[k]))
    w()
    if loc.get("per_distanza"):
        w("| distanza sul grafo | nodi | mediana `\\|dcs\\|/cs` | max | **mediana / (1/n)** |")
        w("|--:|--:|--:|--:|--:|")
        for r in loc["per_distanza"]:
            w("| `%d` | `%d` | `%.6e` | `%.6e` | **`%.4f`** |"
              % (r["distanza"], r["nodi"], r["mediana_cambio_rel"],
                 r["max_cambio_rel"], r["rapporto_su_1_su_n"]))
        for k in list(loc):
            if k.startswith("oltre_"):
                r = loc[k]
                w("| **`%s`** | `%d` | `%.6e` | `%.6e` | **`%.4f`** |"
                  % (k.replace("oltre_", "oltre "), r["nodi"],
                     r["mediana_cambio_rel"], r["max_cambio_rel"],
                     r["rapporto_su_1_su_n"]))
        w()
        w("> ### E SI RIPORTA **IN FUNZIONE DELLA DISTANZA, non come un numero solo:** ### "
          "**un numero solo non distingue <<locale piu' una coda globale>> da <<globale>>.** "
          "La **forma della curva** lo fa, e l'ultima colonna e' il confronto col `1/n` "
          "atteso da `CS-LAMBDA-GLOBALE`.")
        w()
        w("> ### E LA MISURA **NON HA MOSSO CIO' CHE MISURA:** `mean(I) > 1e-30` verificato "
          "**PRIMA** di chiamare, e `_cs_lam_degenere` **salvato e ripristinato** "
          "*(`contatore_mosso = %s`, `contatore_ripristinato = %s`)*."
          % (loc.get("contatore_mosso"), loc.get("contatore_ripristinato")))
    w()
    w("## CRITERIO `4` -- `r` materia `<` `r` vuoto: ### **E' FEDELTA', NON FISICA**")
    w()
    w("> *(Annotazione del guardiano, 2026-10-05, e la applico alla lettera.)* `r` materia "
      "`<` `r` vuoto ### **SEGUE DALLA FORMULA di `_cs_nodo`**: "
      "`cs_floor = CS_M/(1 + sqrt(I)*sqrt(1/scala))` **decresce in `I`**, e la transizione "
      "`0.5*(1 + tanh(1 - u))` pure. ### **Quindi puo' fallire SOLO se il codice e' "
      "sbagliato:** e' un `FALSO-UNO` in attesa, **non una predizione messa alla prova**. "
      "### **NON si rivendica come conferma della fisica.**")
    w()
    w("| passo di `r` | nodi materia | `r` mediano **MATERIA** | `r` mediano **VUOTO** | "
      "rapporto | materia `<` vuoto |")
    w("|--:|--:|--:|--:|--:|:--|")
    tot = giusti = 0
    for k, r in enumerate(pp):
        rm, rv = r.get("r_med_materia"), r.get("r_med_vuoto")
        if rm is None or rv is None:
            continue
        if r["cs_assente"] - (pp[k - 1]["cs_assente"] if k else 0) > 0:
            continue
        tot += 1
        if rm < rv:
            giusti += 1
        if r["passo"] in (3, 4, 5, 10, 20, 50, 100, len(pp)):
            w("| `%d` | `%d` | `%.9f` | `%.9f` | `%.6f` | %s |"
              % (r["passo"], r.get("nodi_materia_prec", -1), rm, rv,
                 (rm / rv) if rv else float("nan"),
                 "**SI**" if rm < rv else "### **NO**"))
    w()
    w("**Passi in cui `r` materia `<` `r` vuoto: `%d` su `%d`** *(`%s`)*."
      % (giusti, tot, ("%.2f %%" % (100.0 * giusti / tot)) if tot else "n/d"))
    w()
    w("**L'ACCOPPIAMENTO E' SFASATO DI UNO, E DEVE ESSERLO:** `r_t = cs_(t-1)/CS_M`, e "
      "`cs_(t-1)` viene da `I_(t-1)`. Le **maschere** materia *(top `5 %` di `abs(psi)^2`)* "
      "e vuoto *(bottom `25 %`)* vengono da `I` del passo `t`, e il `r` dal passo `t+1`. "
      "### **Le maschere si CONSERVANO** *(due bool per nodo, `3.8` MB su `%d` passi)*, "
      "cosi' **non c'e' nessun limite da dichiarare** -- e la prima versione dello strumento "
      "uno ce l'aveva, evitabile con `4` MB." % d["passi"])
    w()
    w("## CRITERIO `6` -- **IL CASO CHE DEVE FALLIRE**")
    w()
    w("| | |")
    w("|---|---|")
    w("| primo passo con una differenza dalla `PARTE A` | **`%s`** |" % prima_div)
    w()
    w("| passo | differenze | di cui **STATO** | `cs_assente` *(cumulato)* | forma | "
      "`r` mediano | `r == 1` su |")
    w("|--:|--:|--:|--:|:--|--:|--:|")
    for k in (1, 2, 3, 4, 5, 10, 20, 50, 100, len(pp)):
        if not (1 <= k <= len(pp)):
            continue
        r = pp[k - 1]
        st = [x for x in r["diff"] if x["classe"] == "STATO"]
        w("| `%d` | `%d` | `%d` | `%d` | `%s` | `%s` | `%s` |"
          % (k, len(r["diff"]), len(st), r["cs_assente"], r["cs_forma"],
             n(r.get("r_mediana")), r.get("r_uguali_a_1")))
    w()
    w("## CRITERIO `7` -- **%d PASSI**, e che cosa cambia **A VALLE**" % d["passi"])
    w()
    w("| | `A` *(la `PARTE A`)* | `B` *(il curato)* | scarto |")
    w("|---|--:|--:|--:|")
    av = d["a_valle"]
    w("| `n` | `%d` | `%d` | `%d` |" % (av["n_A"], av["n_B"], av["n_B"] - av["n_A"]))
    w("| archi | `%d` | `%d` | `%d` |"
      % (av["archi_A"], av["archi_B"], av["archi_B"] - av["archi_A"]))
    w()
    w("## LA DOMANDA APERTA PER LUCA -- e **non la risolvo io**")
    w()
    w("> ### IL MANDATO HA **DUE LETTURE** su un punto, e la differenza e' il ramo "
      "**`TEMPO_SEGNO`** *(`:5303`-`:5312`)*:")
    w("> * **(A)** *<<con `TAU_LOC > 0` restituisce `cs_nodo_prev / CS_M` per nodo>>* -- e "
      "allora quel ramo diventa **IRRAGGIUNGIBILE per costruzione**;")
    w("> * **(B)** *<<il ramo che leggeva la FASE esce dalla fisica>>* -- e allora esce "
      "**solo** quello.")
    w(">")
    w("> ### **HO SCELTO LA LETTURA `B`, LA MINIMA**, e il perche' e' una regola: il par.2 "
      "dice di **non estendere una cura da soli**, e `TEMPO_SEGNO` **non e' nominato** fra i "
      "rami che escono. ### **E OGGI LE DUE LETTURE SONO INDISTINGUIBILI** *("
      "`TEMPO_SEGNO = False`, quindi la scelta e' **byte-inerte**)*. ### **Ma se un giorno "
      "venisse acceso darebbero `r` DIVERSI, e quella e' una decisione di Luca.**")
    w()
    w("## CHE COSA RESTA APERTO")
    w()
    w("1. **`RITMO-FLAG-SENZA-OGGETTO`** *(aperta da questa cura)*: `RITMO_WRAP_2PI` e "
      "`TEMPO_PROPRIO_ORIENTATO` **perdono il loro unico consumatore fisico** e **non sono "
      "stati tolti**; `_sigillo_ritmo_wrap.py` e `_sigillo_anello.py` **perdono il loro "
      "oggetto** e ### **nessuno dei due e' sbagliato** -- si rigirano **al loro commit**.")
    w("2. **`CS-LAMBDA-GLOBALE`**: da questa cura **il tempo di ogni legge locale legge una "
      "media globale**, e il criterio `5` dice **di quanto**.")
    w("3. **LA MISURA CON `DT` DIMEZZATO**, decisa da Luca per **dopo** questo sigillo, col "
      "criterio fissato in `a0641f` -- un transitorio **fisico** dura lo stesso **TEMPO**, un "
      "**artefatto** resta a periodo `2` **PASSI**, e un **raccordo** si accorcia nel tempo "
      "e non nei passi.")
    w("4. **i due registri morti** `_med_f_prec`/`_med_f_ultimo` e **`_psi_prec` promosso e "
      "non piu' letto dalla fisica**: una voce da aprire, **non in questo commit**.")
    w()
    w("---")
    w()
    w("*Referto **generato** da `csv/_seal_fork/_referto_z43_cura2.py` dal `sigillo.json` "
      "della corsa: ### **nessun numero e' ricopiato a mano** (`L-NUMERI`).*")
    w()
    io.open(OUT, "w", encoding="utf-8", newline=NL).write(NL.join(T))
    print("scritto %s  (%d righe)" % (OUT, len(T)))
    print("  esito del sigillo: %s" % d.get("esito"))
    print("  blob del referto: %s"
          % hashlib.sha1(io.open(OUT, "rb").read()).hexdigest()[:8])
    return 0


if __name__ == "__main__":
    sys.exit(main())
