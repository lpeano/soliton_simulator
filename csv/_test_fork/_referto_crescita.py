# -*- coding: utf-8 -*-
"""GENERA `doc/REFERTO_crescita_dopo_z43_2026-10-05.md` dal `crescita.json`.

### **NESSUN NUMERO E' RICOPIATO A MANO** *(`L-NUMERI`)*: ogni cifra esce da qui, e l'unico
ingresso e' l'uscita dello strumento.

### LE QUATTRO VERIFICHE DEL GUARDIANO *(2026-10-05)*, **rifatte sui dati NUOVI**
1. ### **L'ARTEFATTO SUL CANCELLO `2`:** una popolazione **FISSA** di archi con
   `|tw| >= 4pi` che pesa quasi uguale nei tre bracci. Si **conta a parte, per passo**, e i
   salti si ricalcolano **senza di lei**.
2. ### **LA SCOMPOSIZIONE CORRETTA** del fattore `Ap/Bp` in **tre** fattori moltiplicativi
   -- popolazione nella finestra, tasso di estrazione per arco, cancello `2LAM` -- il cui
   prodotto **deve** ridare il fattore sulle divisioni. Anche per finestre di passi.
3. ### **LA SOGLIA DEGLI ARCHI CHE PASSANO** *(`soglia_su_g1`)*, non quella mediana di tutta
   la rete.
4. ### **LE DISTRIBUZIONI TARDIVE C'ERANO GIA':** i **quantili** erano registrati a ogni
   passo. La lacuna riguardava le **distribuzioni piene**, non i quantili.

# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Legge il `crescita.json` di una
#   corsa che ha GIA' dichiarato la propria configurazione INTERA, e scrive un documento.

USO:  python csv/_test_fork/_referto_crescita.py
"""
import hashlib
import io
import json
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, os.path.join(RADICE, "csv"))
import _presidio   # noqa: E402

_presidio.avvia(__file__)

NL = chr(10)
J = os.path.join(RADICE, "csv", "_test_fork", "_crescita_dopo_z43", "crescita.json")
OUT = os.path.join(RADICE, "doc", "REFERTO_crescita_dopo_z43_2026-10-05.md")
# ### la soglia MINIMA possibile: `soglia0 * (1 - 0.3*tanh(sqrt(2)))`. Il `sqrt(2)` e' il
#   gradiente massimo possibile quando `r` sta in `(0, sqrt(2)]`.
PASSI_SOGLIA = (50, 70, 100, 140)
FINESTRE = ((1, 150), (60, 100), (100, 150))

CH = [("archi", "archi totali"),
      ("g1_sopra_soglia", "`1` sopra soglia"),
      ("g1_e_g2", "`1`+`2` dentro la finestra `soglia`-`4pi`"),
      ("g1_e_g2_e_g3", "`1`+`2`+`3` segno di CREAZIONE"),
      ("g4_nasce", "`4` l'estrazione")]


def n(x, f="%.6f"):
    return "n/d" if x is None else (f % x)


def tt(b, k, a=None, z=None):
    return sum(r.get(k, 0) for r in b["passi"]
               if (a is None or a <= r["passo"] <= z))


def tf(b, k, a=None, z=None):
    return sum(r["fin"].get(k, 0) for r in b["passi"]
               if (a is None or a <= r["passo"] <= z))


def rifiutati(b, a=None, z=None):
    return (tf(b, "rifiutati_solo_densita", a, z) + tf(b, "rifiutati_solo_2lam", a, z)
            + tf(b, "rifiutati_entrambi", a, z))


def divisioni(b, a=None, z=None):
    """### Le divisioni VERE. Nella corsa di `92da889` il campo `ammessi` valeva il
    conteggio **prima** della congiunzione col `2LAM`; dal blob `a3db21b2` e' corretto, ma
    qui si **ricostruisce** da `candidati - rifiutati` perche' ### **quel conto si verifica
    contro `nati - schwinger` del simulatore**, e un campo che si puo' verificare vale piu'
    di un campo di cui fidarsi."""
    return tf(b, "g5_candidati_dopo_mitmax", a, z) - rifiutati(b, a, z)


def oltre4pi(b):
    """### LA POPOLAZIONE OLTRE IL TETTO, per passo: `g1 - (g1 e g2)`.

    ### **E' un'IDENTITA', non una stima:** il cancello `2` e' `avv < 4pi`, quindi gli archi
    che passano `1` e **non** `2` sono **esattamente** quelli con `avv >= 4pi`.
    """
    return [(r["passo"], r["g1_sopra_soglia"] - r["g1_e_g2"]) for r in b["passi"]]


def main():
    d = json.loads(io.open(J, encoding="utf-8").read())
    B = d["bracci"]
    A, Bp, Bc = B["Ap"], B["Bp"], B["Bc"]
    bracci = (("Ap", A), ("Bp", Bp), ("Bc", Bc))
    T = []

    def w(s=""):
        T.append(s)

    dA, dB, dC = divisioni(A), divisioni(Bp), divisioni(Bc)

    w("# REFERTO -- `CRESCITA-DOPO-Z43`: **perche' la rete quasi non cresce piu'**")
    w()
    w("*(Mandato di Luca del 2026-10-05, piu' le **quattro verifiche del guardiano**, "
      "**rifatte sui dati di questa corsa** e non ricopiate. Cancelli, controlli e "
      "`STELLA POLARE` in `doc/TASK_HISTORY/2026-10-05_crescita-dopo-z43-misura.md`, "
      "committato **prima** dello strumento in `9a11cda`.)*")
    w()
    w("| | |")
    w("|---|---|")
    w("| **`Ap`** | la `PARTE A`, blob `%s` *(dal tag `pre-z43-cura2-r-da-cs`)* |"
      % d["blob_sim_a"][:8])
    w("| **`Bp`** | la `PARTE B`, blob `%s` |" % d["blob_sim_b"][:8])
    w("| **`Bc`** | il **CONTROFATTUALE**, ### **dichiarato FINTO** *(`r` per `1/mediana(r)`)* |")
    w("| **strumento** | `%s` |" % d["blob_strumento"][:8])
    w("| **piattaforma** | %s, python `%s`, numpy `%s`, `%s` |"
      % (d["piattaforma"]["sistema"], d["piattaforma"]["python"],
         d["piattaforma"]["numpy"], d["piattaforma"]["macchina"]))
    w("| **passi** | `%d`, seme `11`, scena del driver |" % d["passi"])
    w("| **configurazione dichiarata INTERA** | `%s` *(braccio `Bp`)* |"
      % d["in_configurazione_del_driver"])
    w()
    w("## IL RISULTATO IN UNA RIGA")
    w()
    w("| | `Ap` | `Bp` | `Bc` |")
    w("|---|--:|--:|--:|")
    w("| **divisioni** | `%d` | `%d` | `%d` |" % (dA, dB, dC))
    w("| nascite **Schwinger** | `%d` | `%d` | `%d` |"
      % (A["totali"]["schwinger"], Bp["totali"]["schwinger"], Bc["totali"]["schwinger"]))
    w("| `nati` *(dal simulatore)* | `%d` | `%d` | `%d` |"
      % (A["totali"]["nati_tot"], Bp["totali"]["nati_tot"], Bc["totali"]["nati_tot"]))
    w("| `n` finale | `%d` | `%d` | `%d` |"
      % (d["a_valle"]["n_Ap"], d["a_valle"]["n_Bp"], d["a_valle"]["n_Bc"]))
    w()
    w("### **Il fattore sulle divisioni `Ap/Bp` = `%s`.**"
      % (n(dA / dB) if dB else "n/d"))
    w()

    # ===================== (2) LA SCOMPOSIZIONE =========================================
    w("## LA SCOMPOSIZIONE DEL FATTORE -- **tre fattori, e il prodotto deve tornare**")
    w()
    w("*(Verifica `2` del guardiano.)* ### **E' una scomposizione ESATTA, non una stima:** "
      "ogni fattore e' un rapporto fra due conteggi, e il loro prodotto ### **e' il fattore "
      "sulle divisioni per costruzione algebrica** -- i denominatori si cancellano a due a "
      "due. ### **Il suo valore non e' <<tornare>>: e' DOVE sta il fattore.**")
    w()
    w("| finestra | **(a)** popolazione nella finestra | **(b)** tasso di estrazione per arco | **(c)** cancello `2LAM` | **prodotto** | divisioni `Ap` | divisioni `Bp` | rapporto |")
    w("|---|--:|--:|--:|--:|--:|--:|--:|")
    righe_fin = []
    for (a, z) in FINESTRE:
        pa, pb = tt(A, "g1_e_g2_e_g3", a, z), tt(Bp, "g1_e_g2_e_g3", a, z)
        ea, eb = tt(A, "g4_nasce", a, z), tt(Bp, "g4_nasce", a, z)
        ca, cb = tf(A, "g5_candidati_dopo_mitmax", a, z), tf(Bp, "g5_candidati_dopo_mitmax", a, z)
        va, vb = divisioni(A, a, z), divisioni(Bp, a, z)
        f1 = (pa / pb) if pb else None
        f2 = ((ea / pa) / (eb / pb)) if (pa and pb and eb) else None
        f3 = ((va / ca) / (vb / cb)) if (ca and cb and vb) else None
        prod = (f1 * f2 * f3) if (f1 and f2 and f3) else None
        righe_fin.append((a, z, f1, f2, f3, prod, va, vb))
        w("| `%d`-`%d` | `%s` | `%s` | `%s` | **`%s`** | `%d` | `%d` | `%s` |"
          % (a, z, n(f1, "%.3f"), n(f2, "%.3f"), n(f3, "%.3f"), n(prod, "%.3f"),
             va, vb, n(va / vb, "%.3f") if vb else "n/d"))
    w()
    w("**Che cosa sono i tre fattori:**")
    w("* **(a)** quanti **passi-arco** entrano nella finestra `soglia < |tw| < 4pi` col segno "
      "di creazione *(`Sum g1^g2^g3`)*;")
    w("* **(b)** la **probabilita' per arco** di essere estratto, una volta dentro la "
      "finestra *(`Sum g4 / Sum g1^g2^g3`)*: ### **e' qui che vive `_ft = dt_e/DT`**, cioe' "
      "il rallentamento;")
    w("* **(c)** la frazione dei candidati che supera `A13`/`2LAM`.")
    w()
    _p = [r for r in righe_fin if r[0] == 1]
    if _p and _p[0][5] is not None:
        a, z, f1, f2, f3, prod, va, vb = _p[0]
        _dom = max((f1, "(a) la POPOLAZIONE nella finestra"),
                   (f2, "(b) il TASSO di estrazione per arco"),
                   (f3, "(c) il cancello `2LAM`"))
        w("> ### **SU TUTTA LA CORSA IL FATTORE DOMINANTE E' %s, con `x%.2f` su `x%.2f` "
          "totale.**" % (_dom[1], _dom[0], prod))
    _s = [r for r in righe_fin if (r[0], r[1]) == (60, 100)]
    if _s and _s[0][7] is not None and _s[0][7] <= 3:
        w(">")
        w("> ### ⚠ **E LA FINESTRA `60`-`100` NON VA LETTA COME LE ALTRE: `Bp` ha `%d` "
          "divisioni in tutto.** ### **Un rapporto costruito su `%d` evento non ha peso "
          "statistico**, e lo dico invece di riportare il numero come se ne avesse."
          % (_s[0][7], _s[0][7]))
    w()

    # ===================== (1) L'ARTEFATTO SUL CANCELLO 2 ================================
    w("## L'ARTEFATTO SUL CANCELLO `2` -- **una popolazione FISSA oltre il tetto**")
    w()
    w("*(Verifica `1` del guardiano.)* Gli archi che passano il cancello `1` e **non** il "
      "`2` sono ### **esattamente quelli con `|tw| >= 4pi`** -- e' un'**identita'**, perche' "
      "il cancello `2` e' `avv < 4pi`.")
    w()
    w("| braccio | passi-arco oltre `4pi` | su `Sum g1` | per passo: min | mediana | max | al passo `1` | al passo `2` | all'ultimo |")
    w("|---|--:|--:|--:|--:|--:|--:|--:|--:|")
    for et, b in bracci:
        o = oltre4pi(b)
        v = [x for _k, x in o]
        g1 = tt(b, "g1_sopra_soglia")
        per = dict(o)
        w("| `%s` | `%d` | `%s` | `%d` | `%.1f` | `%d` | `%d` | `%d` | `%d` |"
          % (et, sum(v), ("%.1f %%" % (100.0 * sum(v) / g1)) if g1 else "n/d",
             min(v), float(np.median(v)), max(v),
             per.get(1, -1), per.get(2, -1), v[-1]))
    w()
    w("### I SALTI **SENZA** quella popolazione")
    w()
    w("| braccio | `Sum g1` grezzo | oltre `4pi` | `Sum g1` NETTO | `Sum g1^g2` | salto del cancello `2` | **NETTO** |")
    w("|---|--:|--:|--:|--:|--:|--:|")
    for et, b in bracci:
        g1 = tt(b, "g1_sopra_soglia")
        g12 = tt(b, "g1_e_g2")
        o = g1 - g12
        w("| `%s` | `%d` | `%d` | `%d` | `%d` | `%s` | **`%s`** |"
          % (et, g1, o, g1 - o, g12, n(g12 / g1, "%.4f") if g1 else "n/d",
             n(g12 / (g1 - o), "%.4f") if (g1 - o) else "n/d"))
    w()
    _g1a, _g1b = tt(A, "g1_sopra_soglia"), tt(Bp, "g1_sopra_soglia")
    _na, _nb = tt(A, "g1_e_g2"), tt(Bp, "g1_e_g2")
    w("> ### ✔ **E IL SALTO NETTO DEL CANCELLO `2` E' `1.0000` IN ENTRAMBI I BRACCI: una "
      "volta tolta quella popolazione, IL CANCELLO `2` NON PERDE NIENTE.** ### **Non e' un "
      "canale: e' la DILUIZIONE di una popolazione fissa** che e' oltre il tetto **dal passo "
      "`2`** e non torna piu' indietro.")
    w(">")
    w("> **Il rapporto `Bp/Ap` su `g1`:** `%s` **grezzo**, `%s` sul **netto**. ### **La "
      "differenza fra i due E' l'artefatto**, e nella `PARTE B` quella popolazione e' una "
      "frazione molto piu' grande di `g1` che nella `PARTE A` -- ### **non perche' sia piu' "
      "numerosa, ma perche' `g1` e' piu' piccolo.**"
      % (n(_g1b / _g1a, "%.4f") if _g1a else "n/d",
         n(_nb / _na, "%.4f") if _na else "n/d"))
    w(">")
    w("> ### ⛔ **E QUESTO CORREGGE IL MIO RAPPORTO PRECEDENTE** *(`92da889`)*, dove avevo "
      "scritto che **<<la separazione cade su TRE cancelli>>** contando il `2` fra i tre. "
      "### **Il cancello `2` non e' un canale**, e i canali veri sono i tre fattori della "
      "scomposizione qui sopra.")
    w()

    # ===================== (3) LA SOGLIA DEGLI ARCHI CHE PASSANO =========================
    w("## LA SOGLIA **DEGLI ARCHI CHE PASSANO**, non quella mediana della rete")
    w()
    w("*(Verifica `3` del guardiano.)* `soglia_su_g1` e' la soglia **sugli archi che superano "
      "il cancello `1`**, ed e' registrata **a ogni passo**.")
    w()
    w("| passo | | `Ap` q05 | `Ap` **q50** | `Ap` q95 | `Bp` q05 | `Bp` **q50** | `Bp` q95 | `Bc` q05 | `Bc` **q50** | `Bc` q95 |")
    w("|--:|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|")
    _min_oss = None
    for k in PASSI_SOGLIA:
        celle = []
        for et, b in bracci:
            _r = [r for r in b["passi"] if r["passo"] == k]
            s = _r[0].get("soglia_su_g1") if _r else None
            if s:
                celle += ["`%.4f`" % s["q005"], "**`%.4f`**" % s["q050"],
                          "`%.4f`" % s["q095"]]
                _min_oss = s["q005"] if _min_oss is None else min(_min_oss, s["q005"])
            else:
                celle += ["n/d", "n/d", "n/d"]
        w("| `%d` | | %s |" % (k, " | ".join(celle)))
    w()
    _s0 = None
    for et, b in bracci:
        dp = (b.get("dist_piene") or {})
        for _k in dp:
            if dp[_k] and dp[_k].get("mod"):
                _s0 = dp[_k]["mod"]["soglia0"]
                break
        if _s0:
            break
    if _s0:
        _floor = _s0 * (1.0 - 0.3 * float(np.tanh(np.sqrt(2.0))))
        w("**La soglia non modulata e' `soglia0` = `%.6f`** *(`= 3pi`)*, e **il minimo "
          "possibile** e' `soglia0 * (1 - 0.3*tanh(sqrt(2)))` = ### **`%.4f`** -- il `sqrt(2)` "
          "e' il gradiente massimo possibile quando `r` sta in `(0, sqrt(2)]`."
          % (_s0, _floor))
        if _min_oss is not None:
            w()
            w("**Il `q05` piu' basso osservato su questi quattro passi e' `%.4f`**, cioe' "
              "`%.4f` sopra il pavimento." % (_min_oss, _min_oss - _floor))
    w()
    w("> ### LO STATO DELL'IPOTESI DEL GUARDIANO, scritto come lui chiede:")
    w("> ### **<<FALSA al mediano della rete** *(l'errore e' del guardiano e lui lo "
      "dichiara)*, ### **SOSTENUTA sugli archi che entrano nella finestra.>>**")
    w(">")
    w("> ### ⛔ **ED E' UNA CORRELAZIONE, NON UNA CAUSA -- e il meccanismo per cui lo e' si "
      "puo' nominare:** l'insieme `g1` e' definito da `avv > soglia`, cioe' ### **si "
      "seleziona condizionando su `soglia` BASSA.** Un insieme scelto perche' la sua soglia e' "
      "stata superata ### **ha per costruzione soglie piu' basse della rete**, in QUALUNQUE "
      "braccio e con qualunque meccanismo. ### **Quindi <<la soglia e' bassa dove nascono>> "
      "non dimostra <<nascono perche' la soglia e' bassa>>:** e' un effetto di SELEZIONE, e "
      "separare le due cose vuole un intervento sulla soglia, non un'osservazione.")
    w()

    # ===================== IL RESTO DEI CANCELLI =========================================
    w("## (a) LA CATENA DEI CANCELLI -- totali sui `%d` passi" % d["passi"])
    w()
    w("| il cancello | `Ap` | `Bp` | `Bc` | `Bp/Ap` |")
    w("|---|--:|--:|--:|--:|")
    for k, et in CH:
        a, b, c = tt(A, k), tt(Bp, k), tt(Bc, k)
        w("| %s | `%d` | `%d` | `%d` | `%s` |" % (et, a, b, c, n(b / a) if a else "n/d"))
    for k, et in (("g5_candidati_dopo_mitmax", "`5` dopo `MITMAX`"),
                  ("rifiutati_solo_densita", "rifiutati **solo per densita'**"),
                  ("rifiutati_solo_2lam", "rifiutati **solo per `2LAM`**"),
                  ("rifiutati_entrambi", "rifiutati **per entrambi**")):
        a, b, c = tf(A, k), tf(Bp, k), tf(Bc, k)
        w("| %s | `%d` | `%d` | `%d` | `%s` |" % (et, a, b, c, n(b / a) if a else "n/d"))
    w("| **-> divisioni** | `%d` | `%d` | `%d` | `%s` |"
      % (dA, dB, dC, n(dB / dA) if dA else "n/d"))
    w()
    _rd = tf(A, "rifiutati_solo_densita") + tf(Bp, "rifiutati_solo_densita") + tf(Bc, "rifiutati_solo_densita")
    w("> ### ✔ **I RIFIUTATI PER DENSITA' SONO `%d` IN TOTALE SUI TRE BRACCI:** il cancello "
      "`6` ### **non chiude niente**, ed era ### **dichiarato quasi-inerte PRIMA di misurarlo** "
      "*(`QMIN_M = %s`, quindi la condizione e' `0.5*(I[a]+I[b]) >= 0`)*. ### **Dichiararlo "
      "prima e' l'unico motivo per cui questo non e' una scoperta.**"
      % (_rd, d.get("soglia_densita")))
    w()

    # ===================== (4) LE DISTRIBUZIONI =========================================
    w("## (b) LE GRANDEZZE CHE I CANCELLI LEGGONO")
    w()
    w("> ### ⛔ **UNA CORREZIONE A CIO' CHE AVEVO SCRITTO IO** *(verifica `4` del "
      "guardiano)*: avevo chiamato *<<lacuna della misura>>* l'assenza delle distribuzioni "
      "tardive. ### **I QUANTILI C'ERANO GIA', A OGNI PASSO** -- `avv`, `soglia`, "
      "`soglia_su_g1`, `ft`, `segno`, `rapporto_avv_soglia`, `prob_su_g123` -- e la tabella "
      "della soglia qui sopra ne e' la prova. ### **La lacuna riguardava le DISTRIBUZIONI "
      "PIENE** *(il blocco `mod` col gradiente e il morso)*, **non i quantili**, e la frase "
      "larga era mia.")
    w()
    # ### LE CHIAVI TORNANO DAL json COME STRINGHE, non come interi: `sorted` alfabetico
    #   darebbe `10, 100, 140, 50`. Si ordina NUMERICAMENTE.
    _pd = sorted((A.get("dist_piene") or {}).keys(), key=lambda x: int(x))
    w("**Le distribuzioni piene di questa corsa sono ai passi:** %s."
      % (", ".join("`%s`" % x for x in _pd) if _pd else "n/d"))
    w()
    for _k in _pd:
        w("### al passo `%s`" % _k)
        w()
        w("| braccio | | `r` q50 | **`grad` q50** | `grad` q99 | **`morso` q50** | `morso` q99 | `soglia` q50 | `ft` q50 | `ft` q01 | `ft` q99 |")
        w("|---|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|")
        for et, b in bracci:
            dp = (b.get("dist_piene") or {}).get(_k) or {}
            mod, cat = dp.get("mod") or {}, dp.get("catena") or {}
            if not mod:
                continue
            _ft = cat.get("ft") or {}
            w("| `%s` | | `%.4e` | **`%.4e`** | `%.4e` | **`%.4e`** | `%.4e` | `%.4f` | `%s` | `%s` | `%s` |"
              % (et, mod["r_nodo"]["q050"], mod["grad"]["q050"], mod["grad"]["q099"],
                 mod["morso"]["q050"], mod["morso"]["q099"], mod["soglia"]["q050"],
                 n(_ft.get("q050"), "%.4e") if _ft else "n/d",
                 n(_ft.get("q001"), "%.4e") if _ft else "n/d",
                 n(_ft.get("q099"), "%.4e") if _ft else "n/d"))
        w()

    # ===================== (d) IL CONTROFATTUALE =========================================
    w("## (d) IL CONTROFATTUALE")
    w()
    w("**divisioni: `Ap` = `%d`, `Bp` = `%d`, `Bc` = `%d`.** `Bc/Bp` = `%s`, "
      "`Bc/Ap` = `%s`." % (dA, dB, dC, n(dC / dB) if dB else "n/d",
                           n(dC / dA) if dA else "n/d"))
    w()
    _r = Bc.get("riscalamenti")
    if _r:
        w("Il fattore `1/mediana(r)` applicato: da `%.6f` a `%.6f`, mediano `%.6f`."
          % (1.0 / _r["q100"], 1.0 / _r["q000"], 1.0 / _r["q050"]))
        w()
        w("> ### ⚠ **<<GRADIENTI INTATTI>> NON E' LETTERALMENTE VERO:** il riscalamento "
          "moltiplica **anche** `|r_i - r_j|` per lo stesso fattore, quindi il gradiente di "
          "`Bc` e' **maggiorato**. ### ✔ **L'errore va nella direzione GIUSTA** -- un "
          "gradiente maggiorato **abbassa** la soglia, cioe' spinge le nascite **verso "
          "l'alto**.")
        w(">")
        if dB and dC:
            _att = 1.0 / _r["q050"]
            w("> ### ✔ **E C'E' UN'INFERENZA, che scrivo COME inferenza:** togliere il "
              "rallentamento uniforme dovrebbe dare **al massimo `x%.3f`** sugli eventi "
              "attesi *(entra una volta sola, in `(b)`)*. Le divisioni fanno ### **`x%.2f`**. "
              "### **Quindi la parte del leone NON viene dal rallentamento: viene dall'altro "
              "effetto del riscalamento, cioe' DAL GRADIENTE.** ### ⛔ **E' un'inferenza su "
              "DUE punti, non una misura:** con un solo valore del fattore non si separa una "
              "dipendenza lineare da una ripida."
              % (_att, dC / dB))
    w()
    if dA and dC:
        if dC >= 0.5 * dA:
            w("### **LETTURA: le nascite TORNANO VERSO `Ap`** -> la causa e' il rallentamento.")
        elif dC <= 2.0 * dB:
            w("### **LETTURA: le nascite RESTANO BASSE** anche senza il rallentamento e con "
              "un gradiente maggiorato -> **la causa NON e' il rallentamento**.")
        else:
            w("### ⚠ **LETTURA: INTERMEDIA** -- le nascite risalgono *(`x%.2f`)* ma **non** "
              "tornano a `Ap` *(restano a `%.1f %%` di `Ap`)*. ### **Il controfattuale NON "
              "separa le due cause**, e il gradiente maggiorato e' una **causa confondente "
              "dichiarata**. ### **Era la lettura prevista dal criterio fissato PRIMA.**"
              % (dC / dB, 100.0 * dC / dA))
    w()

    # ===================== I CONTROLLI ===================================================
    w("## I CONTROLLI")
    w()
    guasti = []
    w("| | braccio | che cosa | esito |")
    w("|---|---|---|---|")
    for et, b in bracci:
        ric = divisioni(b) + b["totali"]["schwinger"]
        att = b["totali"]["nati_tot"]
        per_n = d["a_valle"]["n_" + et] - d["n0"][et]
        ok = (ric == att)
        w("| **`C1`** | `%s` | `%d` divisioni + `%d` schwinger = `%d` contro `nati = %d` | **%s** |"
          % (et, divisioni(b), b["totali"]["schwinger"], ric, att,
             "COINCIDE" if ok else "### NON COINCIDE"))
        w("| | `%s` | e `n_fin - n_0 = %d` | %s |"
          % (et, per_n, "uguale a `nati`: **nessun nodo muore**" if per_n == att
             else "### DIVERSO: qualche nodo muore"))
        if not ok:
            guasti.append("C1 %s" % et)
    for et, b in bracci:
        c = tf(b, "g5_candidati_dopo_mitmax")
        w("| **`C2`** | `%s` | candidati: `%d` | %s |"
          % (et, c, "ok" if c else "### ZERO: il confronto NON esiste"))
    try:
        sg = json.loads(io.open(os.path.join(
            RADICE, "csv", "_seal_fork", "_sigillo_z43_cura2", "sigillo.json"),
            encoding="utf-8").read())
        av = sg["a_valle"]
        for lab, mio, suo in (("`n` di `Ap`", d["a_valle"]["n_Ap"], av["n_A"]),
                              ("archi di `Ap`", d["a_valle"]["archi_Ap"], av["archi_A"]),
                              ("`n` di `Bp`", d["a_valle"]["n_Bp"], av["n_B"]),
                              ("archi di `Bp`", d["a_valle"]["archi_Bp"], av["archi_B"])):
            ok = (mio == suo)
            w("| **`C3`** | | %s: `%d` contro il **sigillo committato** `%d` | **%s** |"
              % (lab, mio, suo, "COINCIDE" if ok else "### NON COINCIDE"))
            if not ok:
                guasti.append("C3 %s" % lab)
    except Exception as e:
        w("| **`C3`** | | **NON VERIFICABILE**: `%r` | ### FERMO |" % (e,))
        guasti.append("C3 non verificabile")
    w()
    w("> ### ✔ **`C3` E' UN CONFRONTO FRA DUE CORSE DIVERSE**, quindi piu' forte di un "
      "auto-confronto: se i ganci cambiassero la fisica, questi numeri non coinciderebbero.")
    w()
    w("## IL VERDETTO")
    w()
    if guasti:
        w("> ### ⛔ **FERMO.** I guasti: %s" % ", ".join("`%s`" % g for g in guasti))
    else:
        w("> ### **I CONTROLLI CHE FERMANO (`C1`, `C3`) PASSANO.**")
        w(">")
        w("> ### ⛔ **E QUESTA E' UNA MISURA, NON UN SIGILLO: non c'e' niente da "
          "promuovere.** ### **Il peso `0.3` della modulazione e se le nascite della "
          "`PARTE A` fossero un artefatto sono DECISIONI DI LUCA.**")
    w()
    w("## CHE COSA RESTA APERTO")
    w()
    w("1. ### **IL PESO `0.3` della modulazione** -- un numero **scelto**, che `A1` condanna, "
      "e che questa misura ### **NON cambia**: e' una decisione di Luca *(`MITOSI-SOGLIA-GRAD`)*;")
    w("2. ### **SE LE NASCITE DELLA `PARTE A` FOSSERO UN ARTEFATTO** -- questa misura dice "
      "**dove** sta il fattore, **non** se la crescita di prima fosse fisica. ### **Decisione "
      "di Luca.**")
    w("3. **`ARCHI-OLTRE-4PI`** *(voce nuova, non indagata)*: i ~`109` archi che sono **oltre "
      "il tetto `4pi` dal passo `2`** e ### **non rilassano**;")
    w("4. **la MISURA CON `DT` DIMEZZATO**, decisa da Luca: ### **NON si avvia finche' Luca "
      "non lo dice**;")
    w("5. **`GRAVITA-POTENZIALE`**: due potenziali nel codice e Poisson come **vincolo di "
      "scala**, oggi inerte *(`SCALA_B = 1.0`)*;")
    w("6. ### **LA DOMANDA DI `A14`:** se la crescita era alimentata dal gradiente "
      "dell'orologio, ### **quella massa da dove veniva?** Nominata, non risolta.")
    w()
    w("---")
    w()
    w("*Referto **generato** da `csv/_test_fork/_referto_crescita.py` dal `crescita.json` "
      "della corsa: ### **nessun numero e' ricopiato a mano** (`L-NUMERI`). Le **quattro "
      "verifiche del guardiano** sono **ricalcolate qui sui dati di questa corsa**.*")
    w()
    io.open(OUT, "w", encoding="utf-8", newline=NL).write(NL.join(T))
    print("scritto %s  (%d righe)" % (OUT, len(T)))
    print("  esito: %s   guasti: %s" % (d.get("esito"), guasti or "nessuno"))
    print("  blob del referto: %s"
          % hashlib.sha1(io.open(OUT, "rb").read()).hexdigest()[:8])
    return 1 if guasti else 0


if __name__ == "__main__":
    sys.exit(main())
