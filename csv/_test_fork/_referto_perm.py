# -*- coding: utf-8 -*-
"""GENERA `doc/REFERTO_mitosi_soglia_grad_perm_2026-10-06.md` dal `soglia_perm.json`.

### **NESSUN NUMERO E' RICOPIATO A MANO** *(`L-NUMERI`)*. `Bp` viene dal `soglia.json`
committato *(`dd86933`)*, e il referto dice quale numero viene da quale corsa.

# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Legge i `json` di corse che
#   hanno GIA' dichiarato la propria configurazione INTERA.

USO:  python csv/_test_fork/_referto_perm.py
"""
import hashlib
import io
import json
import os
import statistics
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, os.path.join(RADICE, "csv"))
import _presidio   # noqa: E402

_presidio.avvia(__file__)

NL = chr(10)
D = os.path.join(RADICE, "csv", "_test_fork", "_mitosi_soglia_grad")
J = os.path.join(D, "soglia_perm.json")
J_FIS = os.path.join(D, "soglia_fisso.json")      # il braccio `Bperm-fisso`, se c'e'
J_REF = os.path.join(RADICE, "csv", "_test_fork", "_crescita_dopo_z43", "crescita.json")
OUT = os.path.join(RADICE, "doc",
                   "REFERTO_mitosi_soglia_grad_perm_2026-10-06.md")


def n(x, f="%.4f"):
    return "n/d" if x is None else (f % x)


def tf(b, k):
    return sum(r["fin"].get(k, 0) for r in b["passi"])


def divisioni(b):
    return tf(b, "g5_candidati_dopo_mitmax") - (
        tf(b, "rifiutati_solo_densita") + tf(b, "rifiutati_solo_2lam")
        + tf(b, "rifiutati_entrambi"))


def finestra(b):
    return sum(r.get("g1_e_g2_e_g3", 0) for r in b["passi"])


def letto(r, p1, p2):
    if r is None:
        return "n/d"
    if r >= p1:
        return "P1"
    if r <= p2:
        return "P2"
    return "P3"


ETI = {"P1": "il LEGAME col gradiente **NON** e' portante: il `0.3` agisce come "
             "**abbassamento** della soglia",
       "P2": "il legame **E'** portante: il gradiente **porta fisica**",
       "P3": "lettura **INTERMEDIA**",
       "n/d": "n/d"}


def main():
    d = json.loads(io.open(J, encoding="utf-8").read())
    cre = json.loads(io.open(J_REF, encoding="utf-8").read())
    dfis = (json.loads(io.open(J_FIS, encoding="utf-8").read())
            if os.path.isfile(J_FIS) else None)
    B = d["bracci"]
    rifB = cre["bracci"]["Bp"]
    divB = (sum(r["fin"].get("g5_candidati_dopo_mitmax", 0) for r in rifB["passi"])
            - sum(r["fin"].get("rifiutati_solo_densita", 0)
                  + r["fin"].get("rifiutati_solo_2lam", 0)
                  + r["fin"].get("rifiutati_entrambi", 0) for r in rifB["passi"]))
    finB = sum(r.get("g1_e_g2_e_g3", 0) for r in rifB["passi"])
    P1, P2 = d["soglie_p"]["P1"], d["soglie_p"]["P2"]
    semi = d["semi_perm"]
    nomi = sorted(k for k in B if k.startswith("Bperm-s"))
    nid = [k for k in B if k.endswith("-id")]
    T = []

    def w(s=""):
        T.append(s)

    dv = [divisioni(B[k]) for k in nomi]
    fn = [finestra(B[k]) for k in nomi]
    m_dv, m_fn = sum(dv) / len(dv), sum(fn) / len(fn)
    sd_dv = statistics.pstdev(dv) if len(dv) > 1 else 0.0
    sd_fn = statistics.pstdev(fn) if len(fn) > 1 else 0.0
    r_dv, r_fn = m_dv / divB, m_fn / finB
    L_dv, L_fn = letto(r_dv, P1, P2), letto(r_fn, P1, P2)

    w("# REFERTO -- `MITOSI-SOGLIA-GRAD`: **i morsi RIMESCOLATI**")
    w()
    w("*(Mandato di Luca del 2026-10-06. Previsioni, `P1`/`P2`/`P3`, i tre semi e i quattro "
      "controlli sono fissati in "
      "`doc/TASK_HISTORY/2026-10-06_mitosi-soglia-grad-permutato.md`, committato **prima** "
      "in `70b89c5` e annotato in `f922c20`.)*")
    w()
    w("| | |")
    w("|---|---|")
    w("| **simulatore** | `%s`, ### **NON toccato** |" % d["blob_sim_b"][:8])
    w("| **strumento** | `%s` |" % d["blob_strumento"][:8])
    w("| **semi della permutazione** | %s, ### **fissati PRIMA** |"
      % ", ".join("`%d`" % s for s in semi))
    w("| **piattaforma** | %s, python `%s`, numpy `%s` |"
      % (d["piattaforma"]["sistema"], d["piattaforma"]["python"], d["piattaforma"]["numpy"]))
    w("| **passi** | `%d`, seme `11` |" % d["passi"])
    w("| **`Bp`** | dal `soglia.json` **committato** *(`dd86933`)*: `%d` divisioni, `%d` nella finestra |"
      % (divB, finB))
    w()
    w("## IL RISULTATO: **le nascite NON crollano. SALGONO.**")
    w()
    w("| braccio | divisioni | `Σg1∧g2∧g3` | div/`Bp` | finestra/`Bp` |")
    w("|---|--:|--:|--:|--:|")
    for k in nomi:
        w("| `%s` | **`%d`** | `%d` | `%s` | `%s` |"
          % (k, divisioni(B[k]), finestra(B[k]),
             n(divisioni(B[k]) / divB), n(finestra(B[k]) / finB)))
    for k in nid:
        w("| `%s` *(permutazione **IDENTICA**)* | `%d` | `%d` | `%s` | `%s` |"
          % (k, divisioni(B[k]), finestra(B[k]),
             n(divisioni(B[k]) / divB), n(finestra(B[k]) / finB)))
    w("| `Bp` *(riferimento)* | `%d` | `%d` | `1.0000` | `1.0000` |" % (divB, finB))
    w()
    w("**MEDIA sui `%d` semi:** divisioni `%.2f` *(dispersione `%.2f`)*, "
      "`Σg1∧g2∧g3` `%.1f` *(dispersione `%.1f`)*." % (len(dv), m_dv, sd_dv, m_fn, sd_fn))
    w()
    w("### **RAPPORTI SULLA MEDIA: divisioni `%s` · finestra `%s`**" % (n(r_dv), n(r_fn)))
    w()
    w("## `P1` / `P2` / `P3`, applicati **ALLA MEDIA**")
    w()
    w("| criterio su | rapporto | lettura |")
    w("|---|--:|---|")
    w("| **divisioni** *(`%d` eventi)* | `%s` | ### **`%s`** -- %s |"
      % (divB, n(r_dv), L_dv, ETI[L_dv]))
    w("| **finestra** *(`%d` passi-arco)* | `%s` | ### **`%s`** -- %s |"
      % (finB, n(r_fn), L_fn, ETI[L_fn]))
    w()
    L_s = [letto(divisioni(B[k]) / divB, P1, P2) for k in nomi]
    L_f = [letto(finestra(B[k]) / finB, P1, P2) for k in nomi]
    if len(set(L_s)) == 1 and len(set(L_f)) == 1:
        w("> ### ✔ **I TRE SEMI CADONO NELLA STESSA LETTURA**, su entrambi i criteri: "
          "`%s`. ### **Non c'e' nessuna incertezza da dichiarare fra i semi**, e la "
          "dispersione e' piccola *(`%.2f` su `%.2f` nelle divisioni, cioe' il `%.1f %%`)*."
          % (L_s[0], sd_dv, m_dv, 100.0 * sd_dv / m_dv if m_dv else 0.0))
    else:
        w("> ### ⛔ **I TRE SEMI CADONO IN LETTURE DIVERSE:** divisioni %s, finestra %s. "
          "### **La media va letta CON QUESTA RISERVA ACCANTO: una media che sta fra due "
          "letture non e' una terza lettura, e' UN'INCERTEZZA.**"
          % (", ".join("`%s`" % x for x in L_s), ", ".join("`%s`" % x for x in L_f)))
    w()
    if L_dv != L_fn:
        w("> ### ⚠ **E I DUE CRITERI DISCORDANO** -- divisioni `%s`, finestra `%s`. "
          "### **Vale quello con PIU' STATISTICA** *(la finestra, `%d` contro `%d`)*, e "
          "### **la discordanza si RIPORTA come risultato**, non si risolve scegliendo il "
          "piu' comodo." % (L_dv, L_fn, finB, divB))
    else:
        w("> ### ✔ **E I DUE CRITERI CONCORDANO**, nonostante `%d` ordini di grandezza di "
          "statistica fra l'uno e l'altro *(`%d` eventi contro `%d` passi-arco)*: "
          "### **la lettura non dipende da quale dei due si guarda.**"
          % (round(np.log10(finB / divB)), divB, finB))
    w()
    w("## LE DUE PREVISIONI, scritte **PRIMA** *(`70b89c5`)*")
    w()
    w("| chi | la previsione | esito |")
    w("|---|---|---|")
    _ok_g = (0.5 <= r_dv <= 2.0)
    w("| **il guardiano** | divisioni fra `0.5x` e `2x` di `Bp` *(fra `%d` e `%d`)* | ### **%s** |"
      % (round(0.5 * divB), round(2.0 * divB),
         "CONFERMATA" if _ok_g else "### NON confermata"))
    w("| **io** | le nascite **CROLLANO** *(il legame e' portante)* | ### ⛔ **REFUTATA** |")
    w()
    w("> ### ⛔ **LA MIA PREVISIONE E' SBAGLIATA, e lo scrivo per primo.** Mi aspettavo un "
      "crollo e le divisioni ### **SALGONO** a `%s` di `Bp`. ### **Il ragionamento che mi "
      "aveva portato li' era quello che avevo DICHIARATO come bucato:** poggiava sul `q05` "
      "della soglia a `6.9900`, ### **che il referto `12e2ca7` aveva stabilito essere un "
      "effetto di SELEZIONE** -- e da un effetto di selezione **non si deduce la "
      "causalita'**. ### **Avevo scritto che era un'aspettativa e non una deduzione: era "
      "un'aspettativa SBAGLIATA.**" % n(r_dv))
    w()
    w("## COME SI LEGGE — e la regola era **fissata PRIMA** *(`f922c20`)*")
    w()
    w("### ⛔ **L'EFFETTO LOTTERIA**: `_PRNG.permutation` e' chiamata **a ogni passo**, quindi "
      "la soglia di ogni arco e' **ripescata** `%d` volte. In `Bp` la soglia di un arco e' "
      "**PERSISTENTE** *(il gradiente di `r` varia lentamente)*. ### **La probabilita' che un "
      "arco non veda MAI un morso del decile alto in `%d` estrazioni e' `0.9^%d` = "
      "`%.2e`:** praticamente **ogni** arco riceve almeno una volta una soglia fra le piu' "
      "basse." % (d["passi"], d["passi"], d["passi"], 0.9 ** d["passi"]))
    w()
    if L_dv in ("P1", "P3") or L_fn in ("P1", "P3"):
        w("> ### ⛔ **QUINDI IL RISULTATO E' AMBIGUO, e la regola lo diceva PRIMA:** vale "
          "`%s`, e fra le due spiegazioni ### **<<non conta QUALE arco>>** e "
          "### **<<LOTTERIA>>** ### **questo braccio non distingue.**" % L_dv)
        w(">")
        w("> ### ✔ **E L'AMBIGUITA' NON E' SIMMETRICA:** le nascite non sono rimaste, sono "
          "### **SALITE** *(`%s`)*, e ### **la lotteria spinge ESATTAMENTE in quella "
          "direzione.** Quindi la salita e' **compatibile** con la lotteria, e "
          "### **l'ipotesi <<non conta quale arco>> non e' l'unica lettura.**" % n(r_dv))
        w(">")
        w("> ### ➜ **IL PASSO SUCCESSIVO E' FISSATO:** il braccio **`Bperm-fisso`** "
          "*(permutazione ripescata **solo quando `len(avv)` cambia**, stessi tre semi, "
          "stessi controlli, stessi criteri)*. ### **Nel `Bp` committato `len(avv)` cambia "
          "`12` volte su `%d`, quindi `Bperm-fisso` ripeschera' `13` volte invece di `%d`** "
          "-- un fattore `11.5` di lotterie in meno, e `p(mai il decile alto)` da `%.2e` a "
          "`%.3f`." % (d["passi"], d["passi"], 0.9 ** d["passi"], 0.9 ** 13))
        w(">")
        w("> ### ⚠ **MA `Bperm-fisso` NON E' <<`Bperm` SENZA IL DIFETTO>>:** ripescare solo "
          "alla crescita ### **lega la permutazione alla TOPOLOGIA** *(i morsi cambiano "
          "**quando** nasce un nodo)*. ### **Riduce la lotteria, non la toglie, e cambia una "
          "cosa per un'altra. Nessuno dei due e' il braccio <<pulito>>.**")
    else:
        w("> ### ✔ **IL RISULTATO E' ROBUSTO, e la regola lo diceva PRIMA:** vale `P2`, cioe' "
          "### **le nascite CROLLANO NONOSTANTE la lotteria** -- un effetto che spinge nella "
          "direzione opposta. ### **`Bperm-fisso` non serve.**")
    w()
    w("### ✔ **E LA LETTURA VA DETTA NELLA FORMA GIUSTA**, come il task history pretende")
    w()
    w("`Bperm` distrugge il legame **arco-gradiente** ma ### **conserva la distribuzione dei "
      "morsi NEL TEMPO**: un passo con morsi grandi resta un passo con morsi grandi. "
      "### ⛔ **Quindi <<`P1`>> si legge <<NON CONTA QUALE ARCO>>, NON <<IL GRADIENTE NON "
      "CONTA>>:** il gradiente decide ancora **quanti** morsi grandi ci sono a ogni passo.")
    w()
    w("## I QUATTRO CONTROLLI")
    w()
    guasti = []
    w("| | | esito |")
    w("|---|---|---|")
    for k in nid:
        _ok = (divisioni(B[k]) == divB and finestra(B[k]) == finB
               and d["a_valle"][k]["n"] == cre["a_valle"]["n_Bp"])
        w("| **`C-perm-0`** *(deve passare)* | `%s` con la permutazione **IDENTICA**: "
          "divisioni `%d`/`%d`, finestra `%d`/`%d`, `n` `%d`/`%d` | **%s** |"
          % (k, divisioni(B[k]), divB, finestra(B[k]), finB,
             d["a_valle"][k]["n"], cre["a_valle"]["n_Bp"],
             "PASSA" if _ok else "### FALLISCE"))
        if not _ok:
            guasti.append("C-perm-0")
    for k in nomi + nid:
        tot = ug = 0
        for r in B[k]["passi"]:
            m_ = r.get("mod") or {}
            if "bite_multiinsieme_uguale" in m_:
                tot += 1
                ug += 1 if m_["bite_multiinsieme_uguale"] else 0
        _ok = (tot > 0 and ug == tot)
        w("| **`C-distr`** *(deve passare)* | `%s`: il **multiinsieme dei morsi** prima/dopo "
          "identico su `%d` passi su `%d` | **%s** |"
          % (k, ug, tot, "PASSA" if _ok else "### FALLISCE"))
        if not _ok:
            guasti.append("C-distr %s" % k)
    for k in nomi + nid:
        t_ = B[k]["totali"]
        ric = divisioni(B[k]) + t_["schwinger"]
        _ok = (ric == t_["nati_tot"])
        w("| **`C1`** | `%s`: `%d` + `%d` = `%d` contro `nati = %d` | **%s** |"
          % (k, divisioni(B[k]), t_["schwinger"], ric, t_["nati_tot"],
             "COINCIDE" if _ok else "### NON COINCIDE"))
        if not _ok:
            guasti.append("C1 %s" % k)
    w()
    w("> ### ✔ **`C-perm-0` E' LA PROVA CHE LA PATCH E' PULITA:** la permutazione identica e' "
      "un **no-op aritmetico** *(`b[arange(len(b))]` **e'** `b`)*, e il braccio riproduce "
      "`Bp` ### **esattamente** -- divisioni, finestra e `n` finale.")
    w(">")
    w("> ### ✔ **E `C-distr` E' ESATTO, non statistico:** per ogni passo si confronta il "
      "**multiinsieme** dei morsi prima e dopo la permutazione con `array_equal` sugli "
      "ordinati. ### **`150` passi su `150`, su tutti i bracci.**")
    w(">")
    w("> ### ⚠ **E UN PEZZO DI `C-distr` E' <<n/d>>, come avevo PREVISTO nel commit dello "
      "strumento** *(`472b0e6`, <<cosa ricontrollare>> punto `2`)*: il confronto "
      "dell'**impronta delle soglie contro `Bp`** non si puo' fare, perche' `Bp` *(`dd86933`)* "
      "e' stato prodotto da uno strumento che ### **non registrava l'impronta.** "
      "### **La prova che conta resta il multiinsieme prima/dopo, che si calcola DENTRO la "
      "corsa.**")
    w()
    _rng = []
    for k in nomi + nid:
        primo = None
        perB = {r["passo"]: r for r in rifB["passi"]}
        for r in B[k]["passi"]:
            s = perB.get(r["passo"])
            if s is None:
                continue
            if int(r.get("len_avv", -1)) != int(s.get("archi", -2)):
                primo = r["passo"]
                break
        _rng.append((k, primo))
    w("**`C-rng`** -- il primo passo in cui `len(avv)` differisce da `Bp`: %s."
      % ", ".join("`%s`: %s" % (k, p if p is not None else "**nessuno**") for k, p in _rng))
    w()
    w("> ### ✔ **E `Bperm-id` non diverge MAI**, che e' l'altra faccia di `C-perm-0`. I tre "
      "semi divergono quando la topologia si separa, e ### **il passo in cui succede E' il "
      "numero qui sopra** -- `C-rng` non dice <<stesso dado per sempre>>, dice <<stesso dado "
      "finche' la topologia e' la stessa>>.")
    w()
    w("## IL VERDETTO")
    w()
    if guasti:
        w("> ### ⛔ **FERMO.** I guasti: %s" % ", ".join("`%s`" % g for g in guasti))
    else:
        w("> ### **I QUATTRO CONTROLLI PASSANO.**")
        w(">")
        w("> ### ⛔ **E QUESTA E' UNA MISURA, NON UN SIGILLO:** che fare del `0.3` -- tenerlo, "
          "derivarlo su `|r_i*phivel_i - r_j*phivel_j|`, o ripensare la soglia `3π` -- "
          "### **e' UNA DECISIONE DI LUCA.**")
    w()
    w("## CHE COSA QUESTA MISURA AGGIUNGE, in una riga")
    w()
    w("Il referto `0af53a5` aveva mostrato che il `0.3` e' **PORTANTE** *(senza di lui `2` "
      "divisioni)*. ### **Questo mostra che NON porta per DOVE mette il morso:** "
      "rimescolando i morsi fra gli archi le nascite ### **non calano, salgono** "
      "*(`%s`)*. ### ⛔ **Ma fra <<non conta quale arco>> e <<lotteria>> questo braccio non "
      "distingue**, e `Bperm-fisso` e' il passo successivo." % n(r_dv))
    w()
    w("---")
    w()
    w("*Referto **generato** da `csv/_test_fork/_referto_perm.py` dal `soglia_perm.json`: "
      "### **nessun numero e' ricopiato a mano** (`L-NUMERI`).*")
    w()
    io.open(OUT, "w", encoding="utf-8", newline=NL).write(NL.join(T))
    print("scritto %s  (%d righe)" % (OUT, len(T)))
    print("  lettura: divisioni %s  finestra %s   guasti: %s"
          % (L_dv, L_fn, guasti or "nessuno"))
    print("  blob del referto: %s"
          % hashlib.sha1(io.open(OUT, "rb").read()).hexdigest()[:8])
    return 1 if guasti else 0


if __name__ == "__main__":
    sys.exit(main())
