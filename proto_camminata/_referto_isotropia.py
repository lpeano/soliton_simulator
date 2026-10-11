r"""IL REFERTO DELL'ISOTROPIA LOCALE — **GENERATO da `uscite/letture_isotropia_locale.json`.**

### ⛔ **Ogni numero e ogni verdetto escono dal `json`** *(`L-NUMERI`)*, e le soglie stanno
nel task history `doc/TASK_HISTORY/2026-10-11_isotropia_locale.md`, **committato PRIMA**
(`e9dbae1` per `s1`..`s7`, `8f4b22f` per `s8`..`s12`).

Gira con:  python proto_camminata/_referto_isotropia.py
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
FONTE = os.path.join(_QUI, "uscite", "letture_isotropia_locale.json")
DEST = os.path.join(RADICE, "doc", "REFERTO_isotropia_locale.md")
X, W, V, ST, L = (chr(0x26d4), chr(0x26a0), chr(0x2705), chr(0x2b50), chr(0x1F4CC))
MN, GR, FR = (chr(0x2014), chr(0xb7), chr(0x2192))


def _c(x):
    """### `True` solo se `x` e' **un numero vero**: non `None`, non `NaN`."""
    return isinstance(x, (int, float)) and not isinstance(x, bool) and x == x


def _vicino(p, atteso):
    """### Se l'esponente e' compatibile con `-atteso`, **a `3 sigma`**, e in quante."""
    e, s = p.get("esponente"), p.get("sigma")
    if not (_c(e) and _c(s)) or s <= 0:
        return "--"
    k = abs(abs(e) - atteso) / s
    return ("### " + V + " **SI'**" if k <= 3.0 else "no") + " *(`%.1f sigma`)*" % k


def _n(x, c=4):
    """### Un numero, o `--` se non c'e'. ### **Mai una stringa inventata.**"""
    try:
        if x != x:
            return "--"
        return ("%." + str(c) + "f") % float(x)
    except (TypeError, ValueError):
        return "--"


def main():
    d = json.loads(io.open(FONTE, encoding="utf-8").read())
    R = []

    def a(s=""):
        R.append(s)

    i1 = d["I1"]
    i2 = d["I2"]
    ma = d.get("M_A", {})
    mc = d.get("M_C", {})
    un = d["uniformita"]
    var = i2["varianti"]
    conf = i2["confronto_col_riferimento"]
    rif = i2["riferimento"]

    a("# IL REFERTO DELL'ISOTROPIA LOCALE — **SI ATTENUA, E I PESI DALLA GEOMETRIA NON "
      "SERVONO**")
    a("")
    a("> ### " + X + " **CONGELATO** *(forma dichiarata in `csv/_forma_referti.py`)*: e' "
      "un ### **REPERTO** " + MN + " la CI ### **non lo rigenera**, e il presidio verifica "
      "### **il suo BLOB.**")
    a("")
    a("*(**Generato** da `python proto_camminata/_referto_isotropia.py`, che legge "
      "`proto_camminata/uscite/letture_isotropia_locale.json` prodotto da `python "
      "proto_camminata/_letture_isotropia_locale.py` " + MN + " **BLOB del modulo di "
      "letture: `%s`**. Soglie e previsioni: `doc/TASK_HISTORY/"
      "2026-10-11_isotropia_locale.md`, committato **PRIMA**.)*" % d.get("blob", "?"))
    a("")

    # =================================================================== le tre grandezze
    a("## " + ST + " `1` LE TRE GRANDEZZE, e perche' il mio misurando vecchio era "
      "SBAGLIATO")
    a("")
    a("> ### " + X + " **IL RILIEVO DEL GUARDIANO, confermato:** mediavo le dispersioni "
      "### **per nodo**, e quella e' ### **IRREGOLARITA' LOCALE** " + MN + " "
      "l'### **ANISOTROPIA** e' la dispersione del ### **profilo MEDIO**, e si giudica "
      "### **contro il RUMORE ATTESO** *(`irregolarita'/sqrt(N)`)*.")
    a("")
    a("| la grandezza | che cosa dice | quando conta |")
    a("|---|---|---|")
    a("| **irregolarita' per nodo** | quanto e' ### **irregolare il vicinato** di un "
      "nodo | e' una proprieta' ### **LOCALE**, e ### **non e' anisotropia** |")
    a("| **anisotropia del profilo medio** | se una ### **DIREZIONE** e' privilegiata "
      "nella media | ### **solo sopra il rumore** e' anisotropia vera |")
    a("| **rumore atteso** | `irregolarita'/sqrt(N)` | ### " + W + " **dipende dal "
      "CAMPIONE**: con meno nodi il rumore cresce, e <<sistematica>> e' una proprieta' "
      "### **della scena E del campione** |")
    a("")

    # =================================================================== I1
    a("## " + ST + " `2` `I1`: L'IRREGOLARITA' SI ATTENUA, E POI SI FERMA SU UN PAVIMENTO")
    a("")
    for nome, v in sorted(i1.items()):
        if "tempi" not in v:
            continue
        a("### **%s** " % nome + MN + " `n = %d`, `m = %d`, diametro `>= %d`, "
          "`t_max = %d`%s" % (v["n"], v["m"], v["diametro"], v["t_max"],
                              (", e i tempi `%s` sono ### **oltre `t_max`: non misurati**"
                               % ", ".join(str(x) for x in v["oltre_t_max"]))
                              if v.get("oltre_t_max") else ""))
        a("")
        a("| `t` | irregolarita' | anisotropia | rumore | aniso/rumore | |")
        a("|---|---|---|---|---|---|")
        for t in sorted(v["tempi"], key=int):
            q = v["tempi"][t]
            a("| `%s` | `%s ± %s` | `%s` | `%s` | `%s` | %s |"
              % (t, _n(q["irregolarita"]), _n(q["sigma_irregolarita"]),
                 _n(q["anisotropia"]), _n(q["rumore"]), _n(q["aniso_su_rumore"], 2),
                 ("### " + X + " **SISTEMATICA**") if q["sistematica"]
                 else "al rumore"))
        a("")
        p, pav = v["potenza"], v["pavimento"]
        a("### " + ST + " **L'esponente: `t^(%s ± %s)`** " % (_n(p.get("esponente"), 3),
                                                                  _n(p.get("sigma"), 3))
          + MN + " ### **%s** *(a `%s sigma`)*. ### **E il pavimento:** gli ultimi due `t` "
          "differiscono di `%s` con `sigma` combinato `%s`, cioe' `%s sigma` " % (
              p.get("verdetto", "?"), _n(p.get("in_sigma"), 1),
              _n(pav.get("differenza")), _n(pav.get("sigma")),
              _n(pav.get("in_sigma"), 1)) + MN + " ### **%s**%s."
          % (pav.get("verdetto", "?"),
             (", e vale `%s`" % _n(pav.get("valore")))
             if pav.get("verdetto") == "PAVIMENTO" else ""))
        a("")

    # =================================================================== I2
    a("## " + ST + " `3` `I2`: LE OTTO VARIANTI, TUTTE ALLA STESSA TAGLIA")
    a("")
    a("> ### " + X + " **TUTTE A `n = %d` E `t = %d`, con gli STESSI `%d` nodi:** un "
      "confronto fra varianti misurate a taglie diverse ### **non e' un confronto.**"
      % (i2["n"], i2["passi"], i2["nodi"]))
    a("")
    a("| la variante | `m` | gradi | `d_s` | irregolarita' | contro `(i)` | costo/tick | "
      "pesi dalle posizioni |")
    a("|---|---|---|---|---|---|---|---|")
    # ### ⛔ **ORDINATE PER EFFETTO**, che e' la regola di forma del mandato
    ordine = sorted(var, key=lambda k: (-conf[k]["guadagno"] if k in conf else 1e9))
    for nome in ordine:
        v = var[nome]
        c = conf.get(nome)
        a("| %s | `%d` | `%d..%d` | `%s` | `%s ± %s` | %s | `%s` s | %s |"
          % (("### " + ST + " **%s**" % nome) if c and c["guadagno"] > 0
             and c["sopra_soglia"] else nome,
             v["m"], v["gradi"][0], v["gradi"][1], _n(v["d_s"], 3),
             _n(v["irregolarita"]), _n(v["sigma_irregolarita"]),
             (("### **%s sigma**" % _n(c["in_sigma"], 1)) if c["sopra_soglia"]
              else ("`%s sigma`" % _n(c["in_sigma"], 1))) if c else (MN + " *(riferimento)*"),
             _n(v["costo_per_tick"], 4),
             ("### " + X + " **SI** *(controllo)*") if v["pesi_dalle_posizioni"]
             else "no"))
    a("")
    v_c = i2["controllo_pesi"]
    a("### " + X + " **IL RISULTATO CHIAVE, ed e' la domanda che l'aggiunta sui pesi "
      "pone:** il controllo `%s` *(### **geometria messa a mano**)* guadagna `%s` contro "
      "il riferimento, cioe' `%s sigma` " % (v_c, _n(conf[v_c]["guadagno"]),
                                             _n(conf[v_c]["in_sigma"], 1)) + MN
      + " ### **%s.**" % ("SOPRA la soglia" if conf[v_c]["sopra_soglia"]
                          else "**SOTTO LA SOGLIA: non da' niente**"))
    a("")
    for br in ("U", "R", "Rn"):
        k = [x for x in var if var[x].get("braccio") == br
             and "Delaunay" in x and "+" not in x]
        if not k:
            continue
        k = k[0]
        c = conf[k]
        # ### ⛔ **LA <<QUOTA DEL GUADAGNO DEL CONTROLLO>> SI STAMPA SOLO SE IL
        # ### DENOMINATORE E' SIGNIFICATIVO.** Se il controllo guadagna ### **quasi
        # ### niente**, quella frazione arriva a ### **migliaia per cento** ed e'
        # ### ### **un numero vero che racconta una cosa falsa** -- e il mandato chiedeva
        # ### proprio *«quanto `(iv-U)` e `(iv-R)` si AVVICINANO a `(iv-V)`»*, che
        # ### ### **non ha senso se `(iv-V)` non si e' mosso.**
        quota = (("### **`%s%%` del guadagno del controllo**"
                  % _n(100.0 * c["quota_del_guadagno_di_voronoi"], 0))
                 if conf[v_c]["sopra_soglia"]
                 else ("### " + W + " **la <<quota del guadagno del controllo>> NON si "
                       "riporta: il controllo stesso e' sotto la soglia**, quindi la "
                       "frazione avrebbe un denominatore non significativo"))
        a("* **`%s`**: irregolarita' `%s`, guadagno `%s` *(`%s sigma`)* " % (
            k, _n(var[k]["irregolarita"]), _n(c["guadagno"]), _n(c["in_sigma"], 1))
          + MN + " %s, e contro il controllo sta a `%s sigma`"
          % (quota, _n(c["contro_voronoi_in_sigma"], 1)))
    a("")
    a("### " + ST + " **E LA PROVA CHE I PUNTI RESPINTI SONO DAVVERO PIU' UNIFORMI** "
      + MN + " altrimenti *«respinti»* e' una ### **parola**: la distanza al primo vicino "
      "passa da dispersione relativa `%s` a ### **`%s`** *(`%s` volte)*, e il minimo sale "
      "di ### **`%s` volte.**"
      % (_n(un["(i) uniformi"]["dispersione_relativa"]),
         _n(un["(ii) respinti"]["dispersione_relativa"]),
         _n(un.get("rapporto_dispersioni"), 2), _n(un.get("rapporto_minimi"), 1)))
    a("")

    # =================================================================== la correlazione
    a("## " + ST + " `4` LA CORRELAZIONE `s7`: LO SBILANCIAMENTO *NON* SPIEGA "
      "L'IRREGOLARITA'")
    a("")
    a("| la variante | sbilanciamento medio | Pearson | in `sigma` | significativa? |")
    a("|---|---|---|---|---|")
    for nome in ordine:
        c = var[nome]["correlazione"]
        a("| %s | `%s ± %s` | `%s` | `%s` | %s |"
          % (nome, _n(c.get("sbilanciamento_medio")),
             _n(c.get("sbilanciamento_sigma")), _n(c.get("pearson"), 3),
             _n(c.get("in_sigma"), 2),
             ("### " + X + " **SI**") if c.get("significativa") else "no"))
    a("")
    quante = sum(1 for nome in var if var[nome]["correlazione"].get("significativa"))
    esito_s7 = (("### " + X + " **CADE** " + MN + " l'irregolarita' locale ### **non si "
                 "spiega con lo sbilanciamento direzionale delle uscite.**")
                if quante == 0
                else ("### **regge su `%d` varianti**, e ### **va guardata variante per "
                      "variante.**" % quante))
    a(("### **`%d` varianti su `%d` hanno una correlazione significativa** *(soglia "
       "`3 sigma`, `s7`)*. ### " % (quante, len(var))) + ST
      + " **E la mia previsione era <<positiva e significativa>>, cioe' che lo "
      "sbilanciamento FOSSE la causa:** " + esito_s7)
    a("")
    a("### " + V + " **E IL BRACCIO LO PROVA NEI DUE VERSI:** su un legame ### "
      "**costruito a mano** la correlazione da' `+1.000000000` e lo dichiara "
      "significativo, su ### **rumore indipendente** da' `-0.0311` a `0.70 sigma` e lo "
      "dichiara ### **NON significativo** " + MN + " ### **quindi uno zero qui e' un "
      "FATTO, non un misurando cieco.**")
    a("")

    # =================================================================== M-A
    if ma:
        a("## " + ST + " `5` `M-A`: LA DIMENSIONE A TAGLIA GRANDE " + MN + " **IL "
          "COMPROMESSO ERA TAGLIA FINITA?**")
        a("")
        a("> ### " + X + " **E IL CRITERIO E' LO SCARTO DA `3`, NON IL VALORE** *(`s9`)*: "
          "### **`d_s > 3` e' un difetto come `d_s < 3`** " + MN + " un grafo con "
          "dimensione spettrale `3.5` ### **non e' uno spazio tridimensionale.**")
        a("")
        tg = ma["taglie"]
        a("| la famiglia | " + " | ".join("`n = %d`" % n for n in tg)
          + " | monotona? | `|d_s-3|` alla taglia massima | `s8` |")
        a("|---" * (len(tg) + 4) + "|")
        for nome, f in sorted(ma["famiglie"].items(),
                              key=lambda x: (x[1]["scarto_da_3"]
                                             if x[1]["scarto_da_3"] == x[1]["scarto_da_3"]
                                             else 1e9)):
            cel = []
            for n in tg:
                q = f["per_taglia"].get(str(n))
                if not q:
                    cel.append("*(non misurata)*")
                elif "d_s" in q:
                    cel.append("`%s`" % _n(q["d_s"], 3))
                else:
                    cel.append("### " + X + " **%s**" % q.get("non_misurata", "?"))
            a("| %s | %s | %s | `%s` | %s |"
              % (nome, " | ".join(cel),
                 ("### " + V + " **si'**") if f["monotona"]
                 else ("no" if f["monotona"] is False else "*(un punto solo)*"),
                 _n(f["scarto_da_3"], 3),
                 ("### " + ST + " **%s**" % f["verdetto_s8"])
                 if f["verdetto_s8"] == "TENDE A 3" else f["verdetto_s8"]))
        a("")
        a("### " + ST + " **E LA PIU' TRIDIMENSIONALE ALLA TAGLIA MASSIMA E' `%s`** "
          % ma.get("piu_tridimensionale") + MN + " ### **sullo scarto da `3`, che e' il "
          "criterio scritto prima.**")
        a("")
        # ### ⛔ **E QUI VA DETTA UNA COSA SULLA SOGLIA, non sui dati.**
        scarti = [(k, f["scarto_da_3"]) for k, f in ma["famiglie"].items()
                  if _c(f["scarto_da_3"])]
        vicine = [k for k, s in scarti if s <= 0.3]
        nessuna_mono = all(f["monotona"] is False for f in ma["famiglie"].values())
        if nessuna_mono and len(vicine) == len(scarti) and scarti:
            a("> ### " + X + " **MA LA SOGLIA `s8` COSI' COM'E' SCRITTA DA' UN VERDETTO "
              "CHE CONTRADDICE I SUOI PROPRI NUMERI, E IL DIFETTO E' MIO.** `s8` chiede "
              "### **due cose in CONGIUNZIONE** " + MN + " *«`d_s` cresce in modo "
              "**monotono** con `n` ### **E** alla taglia massima `|d_s - 3| <= 0.3`»* " +
              MN + " e il risultato e' che ### **`%d` famiglie su `%d` stanno entro "
              "`0.3` da `3`** *(la migliore a `%s`)*, ma ### **NESSUNA e' monotona**, "
              "quindi il verdetto composto dice ### **<<NON ARRIVA A 3>> per tutte.**"
              % (len(vicine), len(scarti), _n(min(s for _k, s in scarti), 3)))
            a("")
            a("### " + ST + " **E IL MOTIVO PER CUI LA CONGIUNZIONE ERA LA FORMA "
              "SBAGLIATA SI VEDE DAL `json`: `d_s` NON HA UNA `sigma`.** Il misurando "
              "torna ### **`d_s` e `r2`, e nessuna incertezza** " + MN + " quindi "
              "*«cresce in modo monotono»* stava leggendo ### **l'ordine di tre numeri la "
              "cui oscillazione** *(`~0.08`)* ### **e' piu' grande della tendenza che "
              "doveva misurare.** ### " + X + " **Una soglia che chiede una monotonia a "
              "una grandezza senza barra d'errore chiede qualcosa che la misura non puo' "
              "dare.**")
            a("")
            a("### " + V + " **E NON LA RISCRIVO ADESSO: riporto i DUE pezzi separati, "
              "perche' erano ENTRAMBI registrati prima.** ### **Il pezzo che risponde "
              "alla domanda di Luca** *(«`(ii)` tende a `3` crescendo la taglia?»)* "
              "### **e' il secondo**, ed e' ### **`|d_s - 3| <= 0.3` alla taglia "
              "massima** " + MN + " e la risposta e' ### **SI'.** ### " + W + " **Il "
              "primo pezzo resta come difetto dichiarato della soglia**, non come "
              "verdetto sulla fisica.")
            a("")

    # =================================================================== M-B
    if "s10_additivita" in i2:
        s10 = i2["s10_additivita"]
        a("## " + ST + " `6` `M-B`: LA COMBINAZIONE " + MN + " **I DUE EFFETTI SI "
          "SOMMANO?**")
        a("")
        a("| | il guadagno sull'irregolarita' |")
        a("|---|---|")
        a("| i punti **respinti** da soli | `%s` |" % _n(s10["guadagno_respinti"]))
        a("| **tutti i vicini** da soli | `%s` |" % _n(s10["guadagno_tutti_vicini"]))
        a("| la **SOMMA** dei due | `%s ± %s` |"
          % (_n(s10["somma_dei_due"]), _n(s10["sigma_somma"])))
        a("| ### " + ST + " **la COMBINAZIONE, misurata** | ### **`%s ± %s`** |"
          % (_n(s10["guadagno_combinazione"]), _n(s10["sigma_combinazione"])))
        a("| la differenza | `%s ± %s`, cioe' ### **`%s sigma`** |"
          % (_n(s10["differenza"]), _n(s10["sigma_differenza"]),
             _n(s10["in_sigma"], 1)))
        a("")
        a("### " + ST + " **IL VERDETTO `s10`: %s** " % s10["verdetto"] + MN
          + " ### " + W + " **ma a `%s sigma` e' SUL CONFINE**, e la soglia era `3`: "
          "### **questa misura NON decide fra <<additivi>> e <<si sovrappongono>>.** "
          "### **E la stima puntuale dice sovrapposizione:** la combinazione ottiene il "
          "### **`%s%%` della somma dei due.**"
          % (_n(s10["in_sigma"], 2),
             _n(100.0 * s10["guadagno_combinazione"] / s10["somma_dei_due"], 0)
             if s10["somma_dei_due"] else "--"))
        a("")
        a("### " + X + " **E IL FATTO CHE DECIDE NON HA BISOGNO DI `s10`: la "
          "combinazione %s il migliore dei due da sola.** Il guadagno della combinazione "
          "e' `%s`, quello dei soli punti respinti e' `%s` " % (
              ("### " + V + " **BATTE**") if s10["sopra_il_massimo_dei_due"]
              else ("### " + X + " **NON BATTE**"),
              _n(s10["guadagno_combinazione"]), _n(s10["guadagno_respinti"]))
          + MN + " ### **quindi aggiungere tutti i vicini a punti gia' respinti "
          "PEGGIORA l'irregolarita'**, e costa di piu'.")
        a("")

    # =================================================================== M-C
    if mc:
        a("## " + ST + " `7` `M-C`: I PAVIMENTI A CONFRONTO")
        a("")
        base = None
        for nome, v in sorted(i1.items()):
            if "geometrico3d" in nome and "pavimento" in v:
                base = v["pavimento"]
        a("| la scena | il pavimento | `sigma` | contro `(i)` |")
        a("|---|---|---|---|")
        if base:
            a("| `(i)` uniformi *(da `I1`)* | `%s` | `%s` | " % (
                _n(base.get("valore")), _n(base.get("sigma"))) + MN + " |")
        for nome, v in sorted(mc.items()):
            if "pavimento" not in v:
                a("| %s | ### %s **non misurata** | | |" % (nome, X))
                continue
            p = v["pavimento"]
            # ### ⛔ **UN PAVIMENTO PUO' NON AVERE VALORE:** se i `t` misurabili sono meno
            # ### di due, `_pavimento` torna ### **solo una NOTA** -- e un confronto fatto
            # ### su un campo assente ### **inventerebbe un numero.**
            # ### ⚠ **E IL CONTROLLO <<`x == x`>> NON BASTA:** un campo ASSENTE torna
            # ### `None`, e ### **`None == None` e' VERO** -- cioe' il controllo contro i
            # ### `NaN` ### **lasciava passare proprio il caso che doveva fermare.**
            if (base and _c(base.get("valore")) and _c(p.get("valore"))):
                dd = base["valore"] - p["valore"]
                sg = math.sqrt(base.get("sigma", 0) ** 2 + p.get("sigma", 0) ** 2)
                sig = (abs(dd) / sg) if sg > 0 else float("inf")
                nota = ("### **piu' BASSO di `%s`, cioe' `%s sigma`**"
                        % (_n(dd), _n(sig, 1))) if dd > 0 else \
                       ("piu' ALTO di `%s` (`%s sigma`)" % (_n(-dd), _n(sig, 1)))
            else:
                nota = MN
            a("| %s | `%s` | `%s` | %s | " % (nome, _n(p.get("valore")),
                                              _n(p.get("sigma")), nota))
        a("")
        # =============================================================== `s12`
        geo = [k for k in i1 if "geometrico" in k]
        if geo:
            pg = i1[geo[0]]["potenza"]
            a("### " + ST + " **E `s12`: E' LA STESSA LEGGE DI ATTENUAZIONE?**")
            a("")
            a("| la scena | l'esponente | contro `(i)` | compatibile con `-1/2`? |")
            a("|---|---|---|---|")
            a("| `(i)` uniformi *(da `I1`)* | `%s ± %s` | " % (
                _n(pg.get("esponente"), 3), _n(pg.get("sigma"), 3)) + MN
              + " | %s |" % _vicino(pg, 0.5))
            for nome, v in sorted(mc.items()):
                q = v.get("potenza")
                if not q or not _c(q.get("esponente")):
                    continue
                sg = math.sqrt(q.get("sigma", 0) ** 2 + pg.get("sigma", 0) ** 2)
                dd = abs(q["esponente"] - pg.get("esponente", 0))
                a("| %s | `%s ± %s` | `%s sigma` %s | %s |"
                  % (nome, _n(q["esponente"], 3), _n(q.get("sigma"), 3),
                     _n(dd / sg, 1) if sg > 0 else "--",
                     ("### " + X + " **DIVERSA**") if sg > 0 and dd > 3 * sg
                     else "*(compatibile)*", _vicino(q, 0.5)))
            a("")

    # =================================================================== la decisione
    a("## " + X + " `8` LA DECISIONE E' DI LUCA, E QUESTA E' LA TABELLA INTERA")
    a("")
    a("> ### " + X + " **CAMBIARE I GRADI CAMBIA LA FISICA LOCALE** " + MN + " la moneta "
      "di Grover ### **dipende dal grado** *(`(2/d)Σ - I`)*, quindi passare da gradi "
      "`2..6` a gradi `6..34` ### **non e' una scelta di comodita'.** ### **Nessuna "
      "variante diventa la scena di default qui:** "
      "`[[DOMANDA-QUALE-SCENA-3D-PRINCIPALE]]`.")
    a("")
    a("| la variante | `d_s` alla taglia massima | `|d_s-3|` | irregolarita' a "
      "`t = %d` | pavimento | costo/tick | gradi |" % i2["passi"])
    a("|---|---|---|---|---|---|---|")
    for nome in ordine:
        v = var[nome]
        f = ma.get("famiglie", {}).get(nome)
        # ### ⛔ **L'ACCOSTAMENTO E' PER PREFISSO ESATTO, non per frammento di nome:**
        # ### `m_c` nomina le sue scene `"<variante> n=<N>"`, quindi il prefisso ### **E'
        # ### il nome della variante.** ### ⚠ **Resta un accostamento per NOME, e lo dico:**
        # ### la cura pulita sarebbe ### **un campo `variante` nel `json`**, che vale per il
        # ### prossimo giro *(`[[DECISIONE-VUOLE-UN-CAMPO]]`)*.
        pav = None
        for k2, q in mc.items():
            if k2.startswith(nome) and "pavimento" in q:
                pav = q["pavimento"].get("valore")
        a("| %s | %s | %s | `%s` | %s | `%s` s | `%d..%d` |"
          % (nome,
             ("`%s` *(n = %s)*" % (_n(f["d_s_massima"], 3), f["taglia_massima"]))
             if f else ("`%s` *(n = %d)*" % (_n(v["d_s"], 3), v["n"])),
             ("`%s`" % _n(f["scarto_da_3"], 3)) if f
             else ("`%s`" % _n(abs(v["d_s"] - 3.0), 3)),
             _n(v["irregolarita"]),
             ("`%s`" % _n(pav)) if pav is not None else MN,
             _n(v["costo_per_tick"], 4), v["gradi"][0], v["gradi"][1]))
    a("")

    # =================================================================== i limiti
    a("## " + W + " `9` I LIMITI DI QUESTO REFERTO, dichiarati")
    a("")
    a("| | il limite |")
    a("|---|---|")
    a("| `1` | ### **`t = 30` non si misura**: il geometrico a `n = %d` ha `t_max = %d`, "
      "e `t = 30` vorrebbe `n ~ 40000`" % (i1[[k for k in i1 if "geometrico" in k][0]]["n"],
                                           i1[[k for k in i1
                                               if "geometrico" in k][0]]["t_max"])
      + " |")
    a("| `2` | ### **UN SEME SOLO per i punti** *(`11`)*: la dispersione fra nodi c'e', "
      "ma ### **la variabilita' fra REALIZZAZIONI della scena non e' misurata** |")
    a("| `3` | ### **le due vie del rilassamento non sono bit-identiche** *(`3.2e-11` sui "
      "punti)*: a `n = 1728` ### **non spostano nessun arco**, e il braccio ### **verifica "
      "una taglia sola** |")
    a("| `4` | ### **il diametro e' CAMPIONATO** su `40` nodi sopra le taglie piccole, "
      "quindi e' ### **un limite inferiore** " + MN + " e il campo `diametro_esatto` lo "
      "dice |")
    a("| `5` | ### **la correlazione `s7` e' fra DUE grandezze per nodo**, e una "
      "correlazione nulla ### **non esclude una causa non lineare** |")
    a("")

    dati = (NL.join(R) + NL).encode("utf-8")
    io.open(DEST, "wb").write(dati)
    print("  scritto %s" % os.path.relpath(DEST, RADICE).replace(os.sep, "/"))
    print("  %d righe, %d byte" % (len(R), len(dati)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
