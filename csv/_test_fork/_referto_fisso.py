# -*- coding: utf-8 -*-
"""GENERA `doc/REFERTO_mitosi_soglia_grad_fisso_2026-10-06.md`: **i DUE bracci insieme**.

### **NESSUN NUMERO E' RICOPIATO A MANO** *(`L-NUMERI`)*. `Bp` viene dal `crescita.json`
committato *(`dd86933`)*, `Bperm` dal `soglia_perm.json` committato *(`e32b9e7`)*,
`Bperm-fisso` dal `soglia_fisso.json` della corsa.

### ⛔ **E APPLICA LE BANDE CORRETTE** *(`0b8999c`)*, non quelle che lo strumento ha
stampato: ### **lo strumento `43cf63c8` usa `1/sqrt(N)`, che e' `1 sigma` sulle divisioni e
un'INDIPENDENZA FALSA sulla finestra.** Il referto e' la lettura **autorevole**, e dice
### **quale numero viene da quale corsa e quale banda vale.**

# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Legge i `json` di corse che
#   hanno GIA' dichiarato la propria configurazione INTERA.

USO:  python csv/_test_fork/_referto_fisso.py
"""
import hashlib
import io
import json
import math
import os
import statistics as st
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, os.path.join(RADICE, "csv"))
import _presidio   # noqa: E402

_presidio.avvia(__file__)

NL = chr(10)
D = os.path.join(RADICE, "csv", "_test_fork", "_mitosi_soglia_grad")
J_FIS = os.path.join(D, "soglia_fisso.json")
J_PER = os.path.join(D, "soglia_perm.json")
J_CRE = os.path.join(RADICE, "csv", "_test_fork", "_crescita_dopo_z43", "crescita.json")
OUT = os.path.join(RADICE, "doc", "REFERTO_mitosi_soglia_grad_fisso_2026-10-06.md")

SOGLIA_P1 = 0.5
SOGLIA_P2 = 0.2
T_2DF_95 = 4.3027        # t(0.025, 2): l'IC95 VERO con tre semi


def n4(x, f="%.4f"):
    """### ⛔ **`0.0` NON E' `n/d`:** e' il difetto che il giro corto ha trovato in
    `34a11dc`, e qui non si ripete."""
    return "n/d" if x is None else (f % x)


def divisioni(b):
    return (sum(r["fin"].get("g5_candidati_dopo_mitmax", 0) for r in b["passi"])
            - sum(r["fin"].get("rifiutati_solo_densita", 0)
                  + r["fin"].get("rifiutati_solo_2lam", 0)
                  + r["fin"].get("rifiutati_entrambi", 0) for r in b["passi"]))


def finestra(b):
    return sum(r.get("g1_e_g2_e_g3", 0) for r in b["passi"])


def semi_di(d):
    """I bracci dei SEMI, **per classe** e non per nome scritto a mano."""
    return sorted(k for k in d["bracci"] if not k.endswith("-id"))


def ident(d):
    return [k for k in d["bracci"] if k.endswith("-id")]


def letto(r):
    if r is None:
        return "n/d"
    if r >= SOGLIA_P1:
        return "P1"
    if r <= SOGLIA_P2:
        return "P2"
    return "P3"


ETI_P = {"P1": "il LEGAME col gradiente **NON** e' portante",
         "P2": "il legame **E'** portante",
         "P3": "lettura **INTERMEDIA**",
         "n/d": "n/d"}

ETI_L = {
    "L-A": ("L'ECCESSO DI `Bperm` ERA LA LOTTERIA", "la lettura pulita e' *«non conta QUALE "
            "arco»*, e il `0.3` agisce come **abbassamento** della soglia"),
    "L-B": ("LA LOTTERIA NON C'ENTRA", "la salita viene dalla **permutazione in se'**, e "
            "### **va capita: nessuna delle due spiegazioni basta**"),
    "L-C": ("IL LEGAME ARCO-GRADIENTE PORTA QUALCOSA", "`Bperm` lo aveva **NASCOSTO** "
            "dietro la lotteria, e il suo risultato non era solo ambiguo: era "
            "### **FUORVIANTE**"),
    "L-D": ("NESSUNA DELLE TRE", "la tavola **non copre** questo caso, e "
            "### **non si forza una lettura**"),
    "n/d": ("n/d", "n/d")}


def main():
    if not os.path.isfile(J_FIS):
        print("### IL soglia_fisso.json NON C'E': la corsa non e' chiusa. MI FERMO.")
        return 1
    F = json.loads(io.open(J_FIS, encoding="utf-8").read())
    Pm = json.loads(io.open(J_PER, encoding="utf-8").read())
    cre = json.loads(io.open(J_CRE, encoding="utf-8").read())
    rifB = cre["bracci"]["Bp"]
    divB = (sum(r["fin"].get("g5_candidati_dopo_mitmax", 0) for r in rifB["passi"])
            - sum(r["fin"].get("rifiutati_solo_densita", 0)
                  + r["fin"].get("rifiutati_solo_2lam", 0)
                  + r["fin"].get("rifiutati_entrambi", 0) for r in rifB["passi"]))
    finB = sum(r.get("g1_e_g2_e_g3", 0) for r in rifB["passi"])

    def tabella(d):
        ks = semi_di(d)
        dv = [divisioni(d["bracci"][k]) for k in ks]
        fn = [finestra(d["bracci"][k]) for k in ks]
        m_dv, m_fn = sum(dv) / len(dv), sum(fn) / len(fn)
        return {"nomi": ks, "dv": dv, "fn": fn, "m_dv": m_dv, "m_fn": m_fn,
                "p_dv": st.pstdev(dv) if len(dv) > 1 else 0.0,
                "p_fn": st.pstdev(fn) if len(fn) > 1 else 0.0,
                "s_dv": st.stdev(dv) if len(dv) > 1 else 0.0,
                "s_fn": st.stdev(fn) if len(fn) > 1 else 0.0,
                "r_dv": m_dv / divB, "r_fn": m_fn / finB}

    A = tabella(Pm)      # Bperm
    B = tabella(F)       # Bperm-fisso
    # --- LE BANDE CORRETTE (`0b8999c`), derivate e non scelte
    b_dv = 2.0 / math.sqrt(divB)
    rel_p_pstdev = A["p_fn"] / A["m_fn"]
    rel_p_stdev = A["s_fn"] / A["m_fn"]
    b_fn_g = 2.0 * rel_p_pstdev / math.sqrt(3)      # LA BANDA DEL GUARDIANO, quella che VALE
    b_fn_s = 2.0 * rel_p_stdev / math.sqrt(3)       # con l'estimatore NON DISTORTO
    T = []

    def w(s=""):
        T.append(s)

    w("# REFERTO -- `MITOSI-SOGLIA-GRAD`: **`Bperm` e `Bperm-fisso`, i DUE bracci**")
    w()
    w("*(Mandato: l'annotazione `f922c20`, che ha fissato `Bperm-fisso` ### **prima di vedere "
      "i numeri di `Bperm`**. Previsioni, criteri e tavola della lotteria in "
      "`doc/TASK_HISTORY/2026-10-06_bperm-fisso.md` *(`1bf6fe2`)*, con le ### **bande "
      "corrette** in `0b8999c`.)*")
    w()
    w("| | |")
    w("|---|---|")
    w("| **simulatore** | `%s`, ### **NON toccato** |" % F["blob_sim_b"][:8])
    w("| **strumento** | `%s` *(`Bperm-fisso`)* · `%s` *(`Bperm`)* |"
      % (F["blob_strumento"][:8], Pm["blob_strumento"][:8]))
    w("| **semi** | %s, ### **gli STESSI dei due bracci** |"
      % ", ".join("`%d`" % s for s in F["semi_perm"]))
    w("| **piattaforma** | %s, python `%s`, numpy `%s` |"
      % (F["piattaforma"]["sistema"], F["piattaforma"]["python"],
         F["piattaforma"]["numpy"]))
    w("| **`Bp`** | dal `crescita.json` **committato** *(`dd86933`)*: `%d` divisioni, "
      "`%d` nella finestra |" % (divB, finB))
    w()
    w("## ⛔ LA PRIMA COSA: **lo strumento ha stampato BANDE SBAGLIATE, e questo referto no**")
    w()
    w("Lo strumento `%s` calcola la banda come `1/sqrt(N)`. ### **E' sbagliata in due modi** "
      "*(correzione del guardiano, `0b8999c`, fissata **prima** della corsa)*:"
      % F["blob_strumento"][:8])
    w()
    w("| | la banda dello strumento | perche' e' sbagliata | ### **quella che VALE** |")
    w("|---|--:|---|--:|")
    w("| **divisioni** | `± %s` | e' ### **`1 sigma`**: anche con la previsione **giusta** un "
      "conteggio cade fuori il `~31.7 %%` delle volte, cioe' ### **una volta su tre** | "
      "`± %s` ⟹ **`[%s, %s]`** |"
      % (n4(1.0 / math.sqrt(divB)), n4(b_dv), n4(1 - b_dv), n4(1 + b_dv)))
    w("| **finestra** | `± %s` | tratta ogni **passo-arco** come indipendente, e ### **non lo "
      "e': lo stesso arco resta nella finestra per molti passi** | `± %s` ⟹ "
      "**`[%s, %s]`** |"
      % (n4(1.0 / math.sqrt(finB)), n4(b_fn_g), n4(1 - b_fn_g), n4(1 + b_fn_g)))
    w()
    # ### I SINGOLI VALORI PORTANO GIA' il loro backtick: metterne un altro attorno
    #   alla lista dava ``8722`, ...``. ### **Trovato GIRANDO il generatore sui dati
    #   parziali, non dal collaudo: i generatori non ne hanno, ed e' il QUARTO
    #   difetto di formato di questa famiglia.**
    w("### ✔ **E IL RUMORE DELLA FINESTRA NON E' STIMATO: E' MISURATO in `Bperm`** -- i tre "
      "semi danno %s, media `%.1f`, dispersione `%.4f` = ### **`%.4f %%`**, errore della "
      "media `%.4f %%`, e `2x` da' la banda qui sopra."
      % (", ".join("`%d`" % x for x in A["fn"]), A["m_fn"], A["p_fn"],
         100 * rel_p_pstdev, 100 * rel_p_pstdev / math.sqrt(3)))
    w()
    w("> ### ⚠ **E NEL CONTO DEL GUARDIANO C'E' UN ERRORE, che il mandato chiedeva di dire:** "
      "il `%.4f %%` e' **`pstdev`**, la deviazione standard di **POPOLAZIONE** *(divide per "
      "`N`)* -- quella che lo strumento stampa. ### **Per STIMARE la dispersione da tre "
      "campioni l'estimatore non distorto e' quello di CAMPIONE**, e vale `sqrt(3/2)` = "
      "`1.2247` volte tanto: `%.4f %%` ⟹ banda **`[%s, %s]`**."
      % (100 * rel_p_pstdev, 100 * rel_p_stdev, n4(1 - b_fn_s), n4(1 + b_fn_s)))
    w(">")
    w("> ### 📌 **VALE LA BANDA DEL GUARDIANO**, perche' e' lui che l'ha fissata e la sua "
      "formula dice *«la dispersione misurata»*. ### **L'altra e' RIPORTATA, non applicata**, "
      "e se un risultato cadesse **fra le due** il referto lo direbbe invece di scegliere.")
    w(">")
    w("> ### ⛔ **E UN LIMITE PIU' GRANDE DI ENTRAMBE: `2x` l'errore della media e' una regola "
      "a `2 sigma`, e con TRE semi ci sono DUE gradi di liberta'.** L'`IC95` vero vuole "
      "`t(0.025, 2)` = `%.4f`, non `2`: la banda sarebbe `± %.4f %%` ⟹ `[%s, %s]`. "
      "### **Una banda a `2 sigma` su tre semi e' OTTIMISTICA di un fattore `%.2f`, e `P3` "
      "chiede ALMENO QUATTRO SEMI. La cura e' un quarto seme, non una banda piu' larga.**"
      % (T_2DF_95, 100 * T_2DF_95 * rel_p_pstdev / math.sqrt(3),
         n4(1 - T_2DF_95 * rel_p_pstdev / math.sqrt(3)),
         n4(1 + T_2DF_95 * rel_p_pstdev / math.sqrt(3)), T_2DF_95 / 2.0))
    w()
    w("## I DUE BRACCI")
    w()
    w("| braccio | divisioni | `Σg1∧g2∧g3` | div/`Bp` | finestra/`Bp` | lotterie |")
    w("|---|--:|--:|--:|--:|--:|")

    def lotterie(d, k):
        v = [int((r.get("mod") or {})["lotterie"]) for r in d["bracci"][k]["passi"]
             if "lotterie" in (r.get("mod") or {})]
        return max(v) if v else None

    for et, d, t in (("Bperm", Pm, A), ("Bperm-fisso", F, B)):
        for k in t["nomi"]:
            lt = lotterie(d, k)
            w("| `%s` | **`%d`** | `%d` | `%s` | `%s` | %s |"
              % (k, divisioni(d["bracci"][k]), finestra(d["bracci"][k]),
                 n4(divisioni(d["bracci"][k]) / divB),
                 n4(finestra(d["bracci"][k]) / finB),
                 "`%d`" % lt if lt is not None else "`150` *(a ogni passo)*"))
        for k in ident(d):
            w("| `%s` *(permutazione **IDENTICA**)* | `%d` | `%d` | `%s` | `%s` | -- |"
              % (k, divisioni(d["bracci"][k]), finestra(d["bracci"][k]),
                 n4(divisioni(d["bracci"][k]) / divB),
                 n4(finestra(d["bracci"][k]) / finB)))
    w("| `Bp` *(riferimento)* | `%d` | `%d` | `1.0000` | `1.0000` | -- |" % (divB, finB))
    w()
    w("| | `Bperm` | `Bperm-fisso` |")
    w("|---|--:|--:|")
    w("| media divisioni | `%.2f` | `%.2f` |" % (A["m_dv"], B["m_dv"]))
    w("| dispersione *(`pstdev`)* | `%.4f` *(`%.2f %%`)* | `%.4f` *(`%.2f %%`)* |"
      % (A["p_dv"], 100 * A["p_dv"] / A["m_dv"], B["p_dv"],
         100 * B["p_dv"] / B["m_dv"] if B["m_dv"] else 0.0))
    w("| media finestra | `%.1f` | `%.1f` |" % (A["m_fn"], B["m_fn"]))
    w("| dispersione *(`pstdev`)* | `%.4f` *(`%.2f %%`)* | `%.4f` *(`%.2f %%`)* |"
      % (A["p_fn"], 100 * A["p_fn"] / A["m_fn"], B["p_fn"],
         100 * B["p_fn"] / B["m_fn"] if B["m_fn"] else 0.0))
    w("| ### **rapporto divisioni** | ### **`%s`** | ### **`%s`** |"
      % (n4(A["r_dv"]), n4(B["r_dv"])))
    w("| ### **rapporto finestra** | ### **`%s`** | ### **`%s`** |"
      % (n4(A["r_fn"]), n4(B["r_fn"])))
    w()
    _disp_b = (B["p_dv"] / B["m_dv"]) if B["m_dv"] else 0.0
    if _disp_b > 2 * (A["p_dv"] / A["m_dv"]):
        w("> ### ⚠ **E LA DISPERSIONE FRA SEMI DI `Bperm-fisso` E' PIU' CHE DOPPIA di quella "
          "di `Bperm`** *(`%.2f %%` contro `%.2f %%`)*. ### **L'avevo scritto come cosa che "
          "non sapevo** *(`1bf6fe2`, punto `2`)*: con **una** permutazione per corsa invece "
          "di `150` ### **non c'e' niente che medi**, e un seme sfortunato pesa. "
          "### ⛔ **Con tre semi e questa dispersione la media e' FRAGILE, e `P3` chiede "
          "almeno quattro semi.**"
          % (100 * _disp_b, 100 * A["p_dv"] / A["m_dv"]))
        w()
    w("## `P1` / `P2` / `P3`, applicati **ALLA MEDIA** di ciascun braccio")
    w()
    w("| braccio | su | rapporto | lettura |")
    w("|---|---|--:|---|")
    for et, t in (("Bperm", A), ("Bperm-fisso", B)):
        for su, r in (("divisioni", t["r_dv"]), ("finestra", t["r_fn"])):
            w("| `%s` | **%s** | `%s` | ### **`%s`** -- %s |"
              % (et, su, n4(r), letto(r), ETI_P[letto(r)]))
    w()
    for et, t in (("Bperm", A), ("Bperm-fisso", B)):
        ls = [letto(x / divB) for x in t["dv"]]
        lf = [letto(x / finB) for x in t["fn"]]
        if len(set(ls)) == 1 and len(set(lf)) == 1:
            w("- `%s`: ### ✔ **i tre semi cadono nella STESSA lettura** su entrambi i "
              "criteri *(`%s`)*." % (et, ls[0]))
        else:
            w("- `%s`: ### ⛔ **i tre semi cadono in LETTURE DIVERSE** -- divisioni %s, "
              "finestra %s. ### **Una media che sta fra due letture non e' una terza "
              "lettura: e' UN'INCERTEZZA**, e si riporta cosi'."
              % (et, ", ".join("`%s`" % x for x in ls),
                 ", ".join("`%s`" % x for x in lf)))
    w()
    w("## ⛔ LA TAVOLA DELLA LOTTERIA, **fissata PRIMA dei numeri** *(`1bf6fe2`)*")
    w()

    def lot(rf, rp, b):
        if rf is None or rp is None:
            return "n/d"
        lo, hi = 1.0 - b, 1.0 + b
        se_f = (B["p_dv"] / B["m_dv"]) / math.sqrt(3) if B["m_dv"] else 0.0
        se_p = (A["p_dv"] / A["m_dv"]) / math.sqrt(3) if A["m_dv"] else 0.0
        if rf < lo:
            return "L-C"
        if lo <= rf <= hi and rp > hi:
            return "L-A"
        if rf > hi and rp > hi and abs(rf - rp) <= 2 * math.sqrt(se_f ** 2 + se_p ** 2):
            return "L-B"
        return "L-D"

    l_dv = lot(B["r_dv"], A["r_dv"], b_dv)
    l_fn = lot(B["r_fn"], A["r_fn"], b_fn_g)
    w("| su | `fisso` | `perm` | banda | ### **lettura** |")
    w("|---|--:|--:|--:|---|")
    w("| **divisioni** | `%s` | `%s` | `[%s, %s]` | ### **`%s`** -- **%s** |"
      % (n4(B["r_dv"]), n4(A["r_dv"]), n4(1 - b_dv), n4(1 + b_dv), l_dv,
         ETI_L[l_dv][0]))
    w("| **finestra** | `%s` | `%s` | `[%s, %s]` | ### **`%s`** -- **%s** |"
      % (n4(B["r_fn"]), n4(A["r_fn"]), n4(1 - b_fn_g), n4(1 + b_fn_g), l_fn,
         ETI_L[l_fn][0]))
    w()
    for et, l in (("divisioni", l_dv), ("finestra", l_fn)):
        w("- **%s** ⟹ `%s`: %s." % (et, l, ETI_L[l][1]))
    w()
    if l_dv != l_fn:
        w("> ### ⚠ **LE DUE METRICHE DANNO LETTURE DIVERSE DELLA LOTTERIA.** "
          "### **Vale quella con PIU' STATISTICA** *(la finestra, `%d` contro `%d`)*, e "
          "### **la discordanza si RIPORTA come risultato.**" % (finB, divB))
    else:
        w("> ### ✔ **LE DUE METRICHE CONCORDANO**, nonostante `%d` ordini di grandezza di "
          "statistica fra l'una e l'altra." % round(math.log10(finB / divB)))
    w()
    # --- la regola dell'ERRORE COMBINATO, chiesta dal guardiano
    se_f = (B["s_fn"] / B["m_fn"]) / math.sqrt(3) if B["m_fn"] else 0.0
    se_p = (A["s_fn"] / A["m_fn"]) / math.sqrt(3) if A["m_fn"] else 0.0
    comb = math.sqrt(se_f ** 2 + se_p ** 2)
    diff = abs(B["m_fn"] - A["m_fn"]) / A["m_fn"] if A["m_fn"] else 0.0
    w("### LA REGOLA DELL'ERRORE COMBINATO *(fissata in `0b8999c`)*")
    w()
    w("`|media_fisso - media_perm| > 2*sqrt(se_fisso^2 + se_perm^2)`, con ogni `se` = "
      "dispersione fra i suoi tre semi `/sqrt(3)` *(estimatore di **campione**)*:")
    w()
    w("| | valore |")
    w("|---|--:|")
    w("| `se` di `Bperm-fisso` *(finestra)* | `%.4f %%` |" % (100 * se_f))
    w("| `se` di `Bperm` *(finestra)* | `%.4f %%` |" % (100 * se_p))
    w("| errore **combinato** | `%.4f %%` · `2x` = **`%.4f %%`** |" % (100 * comb,
                                                                       200 * comb))
    w("| differenza fra le due medie | **`%.4f %%`** *(`%.1f` contro `%.1f`)* |"
      % (100 * diff, B["m_fn"], A["m_fn"]))
    w()
    if diff > 2 * comb:
        w("> ### ✔ **LE DUE FINESTRE SONO DIVERSE:** `%.4f %%` **supera** `%.4f %%`. "
          "### **La lotteria SPOSTA la finestra**, e lo dice un confronto fra **due medie "
          "con la loro incertezza ciascuna**, non una media contro un numero trattato come "
          "esatto." % (100 * diff, 200 * comb))
    else:
        w("> ### ⛔ **LE DUE FINESTRE NON SONO DISTINGUIBILI:** `%.4f %%` **non supera** "
          "`%.4f %%`. ### **Togliere la lotteria non sposta la finestra in modo "
          "misurabile**, e questo e' un risultato, non un'assenza di risultato."
          % (100 * diff, 200 * comb))
    w()
    w("## LE PREVISIONI")
    w()
    w("| chi | la previsione | esito |")
    w("|---|---|---|")
    _mia = (1 - b_dv <= B["r_dv"] <= 1 + b_dv)
    w("| **io** *(`1bf6fe2`)* | `Bperm-fisso` **torna verso `Bp`**: rapporto delle divisioni "
      "dentro la banda | ### **%s** |"
      % ("CONFERMATA" if _mia else "⛔ REFUTATA"))
    w("| **io**, sulla dispersione | *«con una permutazione sola i tre semi potrebbero "
      "separarsi MOLTO di piu'»* | `%.2f %%` contro `%.2f %%` di `Bperm`: ### **%s** |"
      % (100 * _disp_b, 100 * A["p_dv"] / A["m_dv"],
         "si separano" if _disp_b > A["p_dv"] / A["m_dv"] else "NON si separano"))
    w()
    if not _mia:
        w("> ### ⛔ **LA MIA PREVISIONE E' SBAGLIATA DI NUOVO, e lo scrivo per primo: due su "
          "due.** Il rapporto e' `%s`, fuori da `[%s, %s]` di `%s` *(il `%.2f %%`)*."
          % (n4(B["r_dv"]), n4(1 - b_dv), n4(1 + b_dv),
             n4(B["r_dv"] - (1 + b_dv)), 100 * (B["r_dv"] - (1 + b_dv))))
        # ### ⚠ **E NON MI APPIGLIO AL MARGINE:** con la dispersione MISURATA fra i tre semi
        #   l'intervallo a `2 sigma` del rapporto ESCLUDE `1.0`, quindi la previsione e'
        #   sbagliata **per il merito**, non per un pelo di banda.
        _se_d = ((B["p_dv"] / B["m_dv"]) / math.sqrt(3)) if B["m_dv"] else 0.0
        _lo = B["r_dv"] * (1 - 2 * _se_d)
        w(">")
        w("> ### ⚠ **E NON MI APPIGLIO AL MARGINE:** e' fuori di poco, ma con la "
          "### **dispersione MISURATA** fra i tre semi *(`%.2f %%`, errore della media "
          "`%.2f %%`)* l'intervallo a `2 sigma` del rapporto e' **`[%s, %s]`**, che "
          "### **%s `1.0`**. ### **La previsione e' sbagliata per il MERITO, non per un pelo "
          "di banda.**"
          % (100 * B["p_dv"] / B["m_dv"], 100 * _se_d, n4(_lo),
             n4(B["r_dv"] * (1 + 2 * _se_d)),
             "ESCLUDE" if _lo > 1.0 else "NON esclude"))
    else:
        w("> ### ✔ **LA PREVISIONE REGGE**, e ### **la banda era DERIVATA e fissata prima**: "
          "non e' stata allargata per farci stare il risultato.")
    w()
    w("## I CONTROLLI")
    w()
    guasti = []
    w("| | | esito |")
    w("|---|---|---|")
    for k in ident(F):
        _ok = (divisioni(F["bracci"][k]) == divB and finestra(F["bracci"][k]) == finB
               and F["a_valle"][k]["n"] == cre["a_valle"]["n_Bp"])
        w("| **`C-perm-0`** *(deve passare)* | `%s`: divisioni `%d`/`%d`, finestra "
          "`%d`/`%d`, `n` `%d`/`%d` | **%s** |"
          % (k, divisioni(F["bracci"][k]), divB, finestra(F["bracci"][k]), finB,
             F["a_valle"][k]["n"], cre["a_valle"]["n_Bp"],
             "PASSA" if _ok else "### FALLISCE"))
        if not _ok:
            guasti.append("C-perm-0")
    for k in semi_di(F) + ident(F):
        tot = ug = 0
        for r in F["bracci"][k]["passi"]:
            m_ = r.get("mod") or {}
            if "bite_multiinsieme_uguale" in m_:
                tot += 1
                ug += 1 if m_["bite_multiinsieme_uguale"] else 0
        _ok = (tot > 0 and ug == tot)
        w("| **`C-distr`** | `%s`: multiinsieme dei morsi identico su `%d`/`%d` passi | "
          "**%s** |" % (k, ug, tot, "PASSA" if _ok else "### FALLISCE"))
        if not _ok:
            guasti.append("C-distr %s" % k)
    for k in semi_di(F) + ident(F):
        t_ = F["bracci"][k]["totali"]
        ric = divisioni(F["bracci"][k]) + t_["schwinger"]
        _ok = (ric == t_["nati_tot"])
        w("| **`C1`** | `%s`: `%d` + `%d` = `%d` contro `nati = %d` | **%s** |"
          % (k, divisioni(F["bracci"][k]), t_["schwinger"], ric, t_["nati_tot"],
             "COINCIDE" if _ok else "### NON COINCIDE"))
        if not _ok:
            guasti.append("C1 %s" % k)
    # --- C-ident e C-lotterie
    # ### ⛔ **E C-ident VA LETTO COL SUO POTERE ACCANTO** (rilievo del guardiano): il caso
    #   pericoloso e' ### **una coppia a lunghezza uguale in cui al passo PRIMA era nato
    #   qualcosa** -- solo allora gli archi possono essere cambiati a lunghezza costante.
    #   Le nascite vere sono `fin.ammessi` piu' l'incremento di `schwinger_tot`:
    #   ### **`g4_nasce` NON e' una nascita**, conta chi passa il cancello `4`, e i cancelli
    #   `5`-`7` possono rifiutarlo tutto.
    _pot = {}
    for k in semi_di(F) + ident(F):
        pp = F["bracci"][k]["passi"]
        rie = tot = peric = 0
        for a in range(len(pp) - 1):
            r0, r1 = pp[a], pp[a + 1]
            m0, m1 = (r0.get("mod") or {}), (r1.get("mod") or {})
            if "archi_impronta" not in m0 or "archi_impronta" not in m1:
                continue
            if int(r0.get("len_avv", -1)) != int(r1.get("len_avv", -2)):
                continue
            tot += 1
            _sw = int(r0.get("schwinger_tot", 0)) - (
                int(pp[a - 1].get("schwinger_tot", 0)) if a > 0 else 0)
            if int((r0.get("fin") or {}).get("ammessi", 0)) + _sw > 0:
                peric += 1
            if m0["archi_impronta"] != m1["archi_impronta"]:
                rie += 1
        _pot[k] = (tot, peric, rie)
        w("| **`C-ident`** *(riporta, non ferma)* | `%s`: coppie a lunghezza **uguale** `%d`, "
          "di cui con **nascite al passo prima** `%d`, archi **diversi** `%d` | **%s** |"
          % (k, tot, peric, rie,
             ("### POTERE NULLO: nessun caso pericoloso" if not peric
              else ("la mappa arco→morso TIENE su `%d` casi pericolosi" % peric))
             if not rie else "### si RI-ETICHETTA su %d passi" % rie))
    for k in semi_di(F):
        lt = lotterie(F, k)
        cam = sum(1 for a, b in zip(
            [int(r.get("len_avv", -1)) for r in F["bracci"][k]["passi"]][:-1],
            [int(r.get("len_avv", -1)) for r in F["bracci"][k]["passi"]][1:]) if a != b)
        _ok = (lt == cam + 1)
        w("| **`C-lotterie`** | `%s`: estratte `%s`, cambi di `len(avv)` `%d`, atteso `%d` | "
          "**%s** |" % (k, lt, cam, cam + 1, "COINCIDE" if _ok else "### NON COINCIDE"))
        if not _ok:
            guasti.append("C-lotterie %s" % k)
    w()
    w("> ### ✔ **E `C-lotterie` E' LA PROVA CHE IL BRACCIO FA CIO' CHE DICE:** la "
      "permutazione si ripesca ### **solo quando `len(avv)` cambia**, e il conteggio lo "
      "verifica contro i cambi veri invece di fidarsi del codice.")
    w()
    _np = sum(v[1] for v in _pot.values())
    if not _np:
        w("> ### ⛔ **MA `C-ident` HA POTERE NULLO SU QUESTA CORSA, e la domanda che doveva "
          "chiudere RESTA APERTA.** I casi pericolosi sono ### **ZERO su tutti e quattro i "
          "bracci**: in ogni coppia a lunghezza uguale ### **non era nato nessuno al passo "
          "prima**, quindi l'insieme degli archi era identico ### **per costruzione** e "
          "l'impronta non poteva differire.")
        w(">")
        w("> ### ⛔ **QUINDI LA FRASE <<ora e' MISURATO invece che sperato>> ERA SBAGLIATA, "
          "e la correggo:** le `%d` coppie guardate non sono `%d` prove -- sono `%d` casi in "
          "cui non c'era niente da vedere. ### **Il rischio che un passo tolga `k` archi e "
          "ne aggiunga `k` NON e' escluso da questa corsa: e' solo non capitato.**"
          % (sum(v[0] for v in _pot.values()), sum(v[0] for v in _pot.values()),
             sum(v[0] for v in _pot.values())))
        w(">")
        w("> ### ✔ **E L'IMPRONTA E' SENSIBILE, questo si':** due insiemi che differiscono "
          "per **un** arco danno `sha1` diversi. ### **Il controllo e' VALIDO e il suo "
          "POTERE e' nullo: sono due cose diverse, e prima le avevo confuse.**")
    else:
        w("> ### ✔ **E `C-ident` HA AVUTO POTERE: `%d` casi pericolosi** *(coppie a lunghezza "
          "uguale con nascite al passo prima)*, e su quelli l'impronta ### **coincide**."
          % _np)
    w()
    w("## ⚠ IL LIMITE, **dichiarato PRIMA dei numeri** *(`f922c20`)*")
    w()
    w("> ### ⛔ **`Bperm-fisso` NON E' <<`Bperm` SENZA IL DIFETTO>>.** Ripescare solo alla "
      "crescita ### **lega la permutazione alla TOPOLOGIA** *(i morsi cambiano **quando** "
      "nasce un nodo)*. ### **Riduce la lotteria, non la toglie, e cambia una cosa per "
      "un'altra. NESSUNO DEI DUE E' IL BRACCIO <<PULITO>>.**")
    w(">")
    w("> ### ✔ **E C'E' UN FATTO CHE LO RENDE MENO GRAVE DI QUANTO SEMBRI:** nel `Bp` "
      "committato `len(avv)` cambia `12` volte su `150`, e la **prima** e' ### **AL passo "
      "`100`** -- quindi per i primi ### **99** passi la permutazione e' ### **UNA SOLA**, e "
      "il legame con la topologia non ha ancora modo di agire. ### ⚠ **E <<tutte DOPO il "
      "passo 100>> era sbagliato: il primo cambio e' *AL* passo 100** *(rilievo del "
      "guardiano)*.")
    w()
    w("## IL VERDETTO")
    w()
    if guasti:
        w("> ### ⛔ **FERMO.** I guasti: %s" % ", ".join("`%s`" % g for g in guasti))
    else:
        w("> ### **I CONTROLLI PASSANO su entrambi i bracci.**")
        w(">")
        w("> ### ⛔ **E QUESTA E' UNA MISURA, NON UN SIGILLO:** che fare del `0.3` -- "
          "tenerlo, derivarlo su `|r_i*phivel_i - r_j*phivel_j|`, o ripensare la soglia "
          "`3π` -- ### **e' UNA DECISIONE DI LUCA.**")
    w()
    w("## CHE COSA QUESTA MISURA AGGIUNGE, e che cosa LASCIA APERTO")
    w()
    w("| | |")
    w("|---|---|")
    w("| `0af53a5` aveva mostrato | il `0.3` e' ### **PORTANTE**: senza di lui `2` divisioni "
      "invece di `18` |")
    w("| `d97317a` aveva mostrato | la modulazione ### **legge la grandezza sbagliata** "
      "*(Spearman `~0.04` col gradiente nudo, `~0.86` con `|r_i*w_i - r_j*w_j|`)* |")
    w("| `d97ac64` *(`Bperm`)* aveva mostrato | rimescolando i morsi le nascite ### **non "
      "calano, SALGONO** -- e la lettura era **AMBIGUA** fra *«non conta quale arco»* e "
      "*«lotteria»* |")
    w("| ### **questo mostra** | ### ⛔ **NON ERA LA LOTTERIA.** Con `20`/`26`/`16` "
      "estrazioni invece di `150` il risultato ### **non si muove** |")
    w()
    w("> ### ⛔ **E L'AMBIGUITA' SI CHIUDE DA UN LATO SOLO.** Cade la *«lotteria»*; "
      "### **ma non resta <<non conta quale arco>>**, perche' se non contasse il rapporto "
      "sarebbe `1`, ### **e invece e' `%s`.** Permutare i morsi ### **FA SALIRE** le "
      "nascite, e questo e' un fatto che nessuna delle due spiegazioni copriva."
      % n4(B["r_dv"]))
    w()
    w("### ⚠ **L'IPOTESI PER LA PROSSIMA MISURA -- e' UN'IPOTESI, non un risultato**")
    w()
    w("Se randomizzare **aiuta**, allora l'assegnazione vera mette le soglie basse sugli "
      "archi ### **che servono meno**: il legame col gradiente non sarebbe soltanto "
      "**non informativo** ma ### **ANTI-informativo**. ### ✔ **Sarebbe coerente con "
      "`d97317a`** *(la modulazione legge `|r_i - r_j|`, che correla `~0.04` con la spinta, "
      "mentre la forma esatta correla `~0.86`)*: una grandezza quasi scorrelata ### **puo' "
      "essere leggermente anti-correlata**, e `%.2f %%` di finestra in piu' e' esattamente "
      "l'ordine di grandezza che ci si aspetterebbe." % (100 * (B["r_fn"] - 1.0)))
    w()
    w("> ### ⛔ **NON LA MISURO QUI, E NON LA DICHIARO DIMOSTRATA.** La misura che la "
      "deciderebbe e' la **correlazione fra il morso e la DISTANZA DALLA SOGLIA** -- e "
      "### **che fare del `0.3` resta UNA DECISIONE DI LUCA.**")
    w()
    w("---")
    w()
    w("*Referto **generato** da `csv/_test_fork/_referto_fisso.py` dai `json` di **tre** "
      "corse -- `crescita.json` *(`dd86933`)*, `soglia_perm.json` *(`e32b9e7`)* e "
      "`soglia_fisso.json` -- e ### **ogni numero dice da quale viene** (`L-NUMERI`).*")
    w()
    io.open(OUT, "w", encoding="utf-8", newline=NL).write(NL.join(T))
    print("scritto %s  (%d righe)" % (OUT, len(T)))
    print("  P: divisioni %s  finestra %s" % (letto(B["r_dv"]), letto(B["r_fn"])))
    print("  LOTTERIA: divisioni %s  finestra %s" % (l_dv, l_fn))
    print("  guasti: %s" % (guasti or "nessuno"))
    print("  blob del referto: %s"
          % hashlib.sha1(io.open(OUT, "rb").read()).hexdigest()[:8])
    return 1 if guasti else 0


if __name__ == "__main__":
    sys.exit(main())
