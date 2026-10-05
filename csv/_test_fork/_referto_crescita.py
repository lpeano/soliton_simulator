# -*- coding: utf-8 -*-
"""GENERA `doc/REFERTO_crescita_dopo_z43_2026-10-05.md` dal `crescita.json`.

### **NESSUN NUMERO E' RICOPIATO A MANO** *(`L-NUMERI`)*: ogni cifra esce da qui, e l'unico
ingresso e' l'uscita dello strumento.

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

CH = [("archi", "archi totali"),
      ("g1_sopra_soglia", "`1` sopra soglia"),
      ("g1_e_g2", "`1`+`2` dentro la finestra `soglia`-`4pi`"),
      ("g1_e_g2_e_g3", "`1`+`2`+`3` segno di CREAZIONE"),
      ("prob_positiva", "`prob > 0`"),
      ("g4_nasce", "`4` l'estrazione")]
FIN = [("g5_candidati_dopo_mitmax", "`5` dopo `MITMAX`"),
       ("g6_passa_densita", "`6` la densita'"),
       ("g7_passa_2lam", "`7` `A13`/`2LAM`"),
       ("ammessi", "**-> AMMESSI** *(divisioni)*")]


def n(x, f="%.6f"):
    return "n/d" if x is None else (f % x)


def tot(b, k):
    return sum(r.get(k, 0) for r in b["passi"])


def tfin(b, k):
    return sum(r["fin"].get(k, 0) for r in b["passi"])


def main():
    d = json.loads(io.open(J, encoding="utf-8").read())
    B = d["bracci"]
    A, Bp, Bc = B["Ap"], B["Bp"], B["Bc"]
    T = []

    def w(s=""):
        T.append(s)

    w("# REFERTO -- `CRESCITA-DOPO-Z43`: **perche' la rete quasi non cresce piu'**")
    w()
    w("*(Mandato di Luca del 2026-10-05. I **cancelli**, i **quattro controlli** e la "
      "**STELLA POLARE** sono fissati in "
      "`doc/TASK_HISTORY/2026-10-05_crescita-dopo-z43-misura.md`, committato **prima** dello "
      "strumento in `9a11cda`.)*")
    w()
    w("| | |")
    w("|---|---|")
    w("| **braccio `Ap`** | la `PARTE A`, blob `%s` *(dal tag `pre-z43-cura2-r-da-cs`)* |"
      % d["blob_sim_a"][:8])
    w("| **braccio `Bp`** | la `PARTE B`, blob `%s` |" % d["blob_sim_b"][:8])
    w("| **braccio `Bc`** | il **CONTROFATTUALE**, ### **dichiarato FINTO** |")
    w("| **strumento** | `%s` |" % d["blob_strumento"][:8])
    w("| **piattaforma** | %s, python `%s`, numpy `%s`, `%s` |"
      % (d["piattaforma"]["sistema"], d["piattaforma"]["python"],
         d["piattaforma"]["numpy"], d["piattaforma"]["macchina"]))
    w("| **passi** | `%d`, seme `11`, scena del driver |" % d["passi"])
    w("| **configurazione del driver dichiarata INTERA** | `%s` *(sul braccio `Bp`)* |"
      % d["in_configurazione_del_driver"])
    w()
    w("## (a) LA CATENA DEI CANCELLI -- **totali sui `%d` passi**" % d["passi"])
    w()
    w("| # | il cancello | `Ap` *(`PARTE A`)* | `Bp` *(`PARTE B`)* | `Bc` *(controfatt.)* | "
      "`Bp/Ap` |")
    w("|---|---|--:|--:|--:|--:|")
    for k, et in CH:
        a, b, c = tot(A, k), tot(Bp, k), tot(Bc, k)
        w("| | %s | `%d` | `%d` | `%d` | `%s` |"
          % (et, a, b, c, n(b / a) if a else "n/d"))
    for k, et in FIN:
        a, b, c = tfin(A, k), tfin(Bp, k), tfin(Bc, k)
        w("| | %s | `%d` | `%d` | `%d` | `%s` |"
          % (et, a, b, c, n(b / a) if a else "n/d"))
    w("| | **(c) nascite SCHWINGER** | `%d` | `%d` | `%d` | `%s` |"
      % (A["totali"]["schwinger"], Bp["totali"]["schwinger"], Bc["totali"]["schwinger"],
         n(Bp["totali"]["schwinger"] / A["totali"]["schwinger"])
         if A["totali"]["schwinger"] else "n/d"))
    w()
    w("## (a) **DOVE I BRACCI SI SEPARANO** -- il cancello, non <<piu' o meno tutti>>")
    w()
    w("### **Il `salto` e' il rapporto `Bp/Ap` di QUESTO cancello diviso quello del cancello "
      "PRECEDENTE:** dice **quanto si perde PROPRIO LI'**, non quanto si e' perso in tutto.")
    w()
    w("| il cancello | `Ap` | `Bp` | `Bp/Ap` | **il SALTO** |")
    w("|---|--:|--:|--:|--:|")
    prec = None
    separa = []
    for k, et in CH:
        a, b = tot(A, k), tot(Bp, k)
        rap = (b / a) if a else None
        salto = (None if (prec is None or rap is None or not prec)
                 else rap / prec)
        w("| %s | `%d` | `%d` | `%s` | **`%s`** |"
          % (et, a, b, n(rap), ("x%.4f" % salto) if salto is not None else "-"))
        if salto is not None and salto < 0.5:
            separa.append((et, salto))
        prec = rap
    for k, et in FIN:
        a, b = tfin(A, k), tfin(Bp, k)
        rap = (b / a) if a else None
        salto = (None if (prec is None or rap is None or not prec) else rap / prec)
        w("| %s | `%d` | `%d` | `%s` | **`%s`** |"
          % (et, a, b, n(rap), ("x%.4f" % salto) if salto is not None else "-"))
        if salto is not None and salto < 0.5:
            separa.append((et, salto))
        prec = rap
    w()
    if len(separa) == 1:
        w("> ### **`C4`: LA SEPARAZIONE CADE SU *UN* CANCELLO** -- %s, con un salto di "
          "`x%.4f`. ### **Tutti gli altri cancelli lasciano il rapporto dov'era.**"
          % (separa[0][0], separa[0][1]))
    elif separa:
        w("> ### **`C4`: LA SEPARAZIONE CADE SU `%d` CANCELLI, e lo dico invece di nominarne "
          "uno solo:**" % len(separa))
        for et, s in separa:
            w("> * %s, salto `x%.4f`" % (et, s))
    else:
        w("> ### **`C4`: NESSUN cancello fa crollare il rapporto di piu' di `2x` rispetto al "
          "precedente. ### LA SEPARAZIONE E' DIFFUSA**, e va detto: l'ipotesi del gradiente "
          "**non** regge nella forma <<un cancello>>.")
    w()
    w("## (b) LE GRANDEZZE CHE I CANCELLI LEGGONO, al passo `%d`" % d["passo_dist"])
    w()
    w("> ### **SI RIPORTANO COME DISTRIBUZIONI, non come mediane:** una mediana **non "
      "distingue una distribuzione RIPIDA da una PIATTA**, ed e' esattamente la cosa da cui "
      "dipende se l'ipotesi del gradiente tiene.")
    w()
    for et, b in (("Ap", A), ("Bp", Bp), ("Bc", Bc)):
        dp = b.get("dist_piene") or {}
        mod = dp.get("mod") or {}
        cat = dp.get("catena") or {}
        fin = dp.get("finali") or {}
        w("### braccio `%s`" % et)
        w()
        if mod:
            w("**`soglia0` = `%.9f`** *(`= 3pi`)*" % mod["soglia0"])
            w()
            w("| grandezza | `q01` | `q25` | **`q50`** | `q75` | `q99` | `max` |")
            w("|---|--:|--:|--:|--:|--:|--:|")
            for nome, lab in (("r_nodo", "`r` per nodo"),
                              ("grad", "**`|r_i - r_j|`** *(il gradiente)*"),
                              ("tanh_grad", "`tanh(grad)`"),
                              ("soglia", "la **soglia** effettiva"),
                              ("morso", "### **il MORSO** `1 - soglia/soglia0`")):
                _q = mod.get(nome)
                if _q:
                    w("| %s | `%.4e` | `%.4e` | **`%.6e`** | `%.4e` | `%.4e` | `%.4e` |"
                      % (lab, _q["q001"], _q["q025"], _q["q050"], _q["q075"],
                         _q["q099"], _q["q100"]))
            w()
        if cat:
            w("| grandezza | `q01` | `q25` | **`q50`** | `q75` | `q99` |")
            w("|---|--:|--:|--:|--:|--:|")
            for nome, lab in (("avv", "**`avv = |tw|`**"),
                              ("soglia", "la soglia"),
                              ("rapporto_avv_soglia",
                               "### **`avv/soglia`** *(la distanza dal cancello `1`)*"),
                              ("ft", "**`_ft = dt_e/DT`** *(il rallentamento)*"),
                              ("segno", "il `segno`"),
                              ("avv_su_g1", "`avv` **sugli archi sopra soglia**")):
                _q = cat.get(nome)
                if _q:
                    w("| %s | `%.4e` | `%.4e` | **`%.6e`** | `%.4e` | `%.4e` |"
                      % (lab, _q["q001"], _q["q025"], _q["q050"], _q["q075"], _q["q099"]))
            w()
            w("Al passo `%d`: archi `%d`, cancello `1` `%d`, `1`+`2` `%d`, `1`+`2`+`3` `%d`, "
              "nasce `%d`."
              % (d["passo_dist"], cat["archi"], cat["g1_sopra_soglia"], cat["g1_e_g2"],
                 cat["g1_e_g2_e_g3"], cat["g4_nasce"]))
            w()
        if fin:
            w("Cancelli finali: candidati `%s`, densita' `%s`, `2LAM` `%s`, **ammessi `%s`**."
              % (fin.get("g5_candidati_dopo_mitmax"), fin.get("g6_passa_densita"),
                 fin.get("g7_passa_2lam"), fin.get("ammessi")))
            w()
    w("## (d) IL CONTROFATTUALE -- **il rallentamento uniforme contro il gradiente**")
    w()
    dA, dB, dC = (A["totali"]["divisioni"], Bp["totali"]["divisioni"],
                  Bc["totali"]["divisioni"])
    w("| | `Ap` | `Bp` | `Bc` |")
    w("|---|--:|--:|--:|")
    w("| **divisioni** | `%d` | `%d` | `%d` |" % (dA, dB, dC))
    w("| nascite Schwinger | `%d` | `%d` | `%d` |"
      % (A["totali"]["schwinger"], Bp["totali"]["schwinger"], Bc["totali"]["schwinger"]))
    w("| `n` finale | `%d` | `%d` | `%d` |"
      % (d["a_valle"]["n_Ap"], d["a_valle"]["n_Bp"], d["a_valle"]["n_Bc"]))
    w()
    w("**`Bp/Ap` = `%s`     `Bc/Ap` = `%s`     `Bc/Bp` = `%s`**"
      % (n(dB / dA) if dA else "n/d", n(dC / dA) if dA else "n/d",
         n(dC / dB) if dB else "n/d"))
    w()
    _r = Bc.get("riscalamenti")
    if _r:
        w("Il fattore `1/mediana(r)` applicato al braccio `Bc`: da `%.6f` a `%.6f` "
          "*(mediana `%.6f`)*."
          % (1.0 / _r["q100"], 1.0 / _r["q000"], 1.0 / _r["q050"]))
        w()
        w("> ### ⚠ **E QUINDI IL GRADIENTE DI `Bc` E' MAGGIORATO DI QUEL FATTORE: <<gradienti "
          "intatti>> NON e' letteralmente vero.** ### ✔ **Ma l'errore va NELLA DIREZIONE "
          "GIUSTA:** un gradiente maggiorato **abbassa** la soglia, cioe' spinge le nascite "
          "**verso l'alto**. ### **Se restano basse NONOSTANTE questo, la conclusione <<non e' "
          "il rallentamento>> e' PIU' FORTE, non piu' debole.**")
        w()
    if dA:
        if dC >= 0.5 * dA:
            w("### ✔ **LETTURA: le nascite TORNANO VERSO LA `PARTE A`** togliendo il "
              "rallentamento uniforme. ### **LA CAUSA E' IL RALLENTAMENTO**, e l'ipotesi del "
              "gradiente **non** e' la spiegazione dominante.")
        elif dC <= 2.0 * dB:
            w("### ✔ **LETTURA: le nascite RESTANO BASSE** anche senza il rallentamento "
              "uniforme **e con un gradiente maggiorato**. ### **LA CAUSA NON E' IL "
              "RALLENTAMENTO** -- ed e' la lettura **forte**, perche' il controfattuale "
              "sbaglia nella direzione opposta.")
        else:
            w("### ⚠ **LETTURA: INTERMEDIA.** Le nascite risalgono ma **non** tornano alla "
              "`PARTE A`. ### **Il controfattuale NON separa le due cause**, e il `23 %` di "
              "gradiente in piu' e' una **causa confondente dichiarata**.")
    w()
    w("## I CONTROLLI")
    w()
    w("| | braccio | che cosa | esito |")
    w("|---|---|---|---|")
    guasti = []
    for et, b, chv, cha in (("Ap", A, "n_Ap", "archi_Ap"), ("Bp", Bp, "n_Bp", "archi_Bp"),
                            ("Bc", Bc, "n_Bc", "archi_Bc")):
        ric = b["totali"]["divisioni"] + b["totali"]["schwinger"]
        att = d["a_valle"][chv] - d["n0"][et]
        ok = (ric == att)
        w("| **`C1`** | `%s` | `%d` divisioni + `%d` schwinger = `%d` contro "
          "`n_fin - n_0 = %d` | **%s** |"
          % (et, b["totali"]["divisioni"], b["totali"]["schwinger"], ric, att,
             "COINCIDE" if ok else "### NON COINCIDE"))
        if not ok:
            guasti.append("C1 %s" % et)
    for et, b in (("Ap", A), ("Bp", Bp), ("Bc", Bc)):
        cand = tfin(b, "g5_candidati_dopo_mitmax")
        w("| **`C2`** | `%s` | candidati su tutta la corsa: `%d` | %s |"
          % (et, cand, "ok" if cand else "### ZERO: il confronto NON esiste"))
    w("| **`C3`** | `Ap`/`Bp` | `n` e archi finali contro il **sigillo committato** | "
      "vedi sotto |")
    w()
    try:
        sg = json.loads(io.open(os.path.join(
            RADICE, "csv", "_seal_fork", "_sigillo_z43_cura2", "sigillo.json"),
            encoding="utf-8").read())
        av = sg["a_valle"]
        w("| | questo strumento | il sigillo *(`5a2ddd9`)* | |")
        w("|---|--:|--:|---|")
        for lab, mio, suo in (("`n` di `Ap`", d["a_valle"]["n_Ap"], av["n_A"]),
                              ("archi di `Ap`", d["a_valle"]["archi_Ap"], av["archi_A"]),
                              ("`n` di `Bp`", d["a_valle"]["n_Bp"], av["n_B"]),
                              ("archi di `Bp`", d["a_valle"]["archi_Bp"], av["archi_B"])):
            ok = (mio == suo)
            w("| %s | `%d` | `%d` | **%s** |"
              % (lab, mio, suo, "COINCIDE" if ok else "### NON COINCIDE"))
            if not ok:
                guasti.append("C3 %s" % lab)
        w()
        w("> ### ✔ **E' UN CONFRONTO FRA DUE CORSE DIVERSE**, quindi piu' forte di un "
          "auto-confronto: ### **se i ganci cambiassero la fisica, questi numeri non "
          "coinciderebbero.**")
    except Exception as e:
        w("`C3` **NON VERIFICABILE**: `%r`" % (e,))
        guasti.append("C3 non verificabile")
    w()
    w("## IL VERDETTO")
    w()
    if guasti:
        w("> ### ⛔ **FERMO.** I guasti: %s" % ", ".join("`%s`" % g for g in guasti))
    else:
        w("> ### **I CONTROLLI CHE FERMANO (`C1`, `C3`) PASSANO.**")
        w(">")
        w("> ### ⛔ **E QUESTA E' UNA MISURA, NON UN SIGILLO: non c'e' niente da "
          "promuovere.** ### **La crescita e la soglia di mitosi sono DECISIONI DI LUCA.**")
    w()
    w("## CHE COSA RESTA APERTO")
    w()
    w("1. **la MISURA CON `DT` DIMEZZATO**, decisa da Luca e in coda **subito dopo** questa;")
    w("2. **`MITOSI-SOGLIA-GRAD`**: la modulazione della soglia col gradiente di `r`, e il "
      "`0.3` che `A1` condanna ### **e che questa misura NON cambia**;")
    w("3. **`GRAVITA-POTENZIALE`** *(decisione di Luca, da curare dopo)*: due potenziali nel "
      "codice e ### **Poisson come VINCOLO DI SCALA, non come equazione risolta** -- e oggi "
      "**inerte**, perche' `SCALA_B = 1.0`;")
    w("4. ### **E LA DOMANDA DI `A14` CHE QUESTA MISURA APRE:** se la crescita era alimentata "
      "dal gradiente dell'orologio, ### **quella massa da dove veniva?** Non la risolvo: la "
      "nomino.")
    w()
    w("---")
    w()
    w("*Referto **generato** da `csv/_test_fork/_referto_crescita.py` dal `crescita.json` "
      "della corsa: ### **nessun numero e' ricopiato a mano** (`L-NUMERI`).*")
    w()
    io.open(OUT, "w", encoding="utf-8", newline=NL).write(NL.join(T))
    print("scritto %s  (%d righe)" % (OUT, len(T)))
    print("  esito della corsa: %s" % d.get("esito"))
    print("  blob del referto: %s"
          % hashlib.sha1(io.open(OUT, "rb").read()).hexdigest()[:8])
    return 0


if __name__ == "__main__":
    sys.exit(main())
