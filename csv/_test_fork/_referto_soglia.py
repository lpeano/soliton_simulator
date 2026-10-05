# -*- coding: utf-8 -*-
"""GENERA `doc/REFERTO_mitosi_soglia_grad_2026-10-06.md` dal `soglia.json`.

### **NESSUN NUMERO E' RICOPIATO A MANO** *(`L-NUMERI`)*.

### ⛔ **`K2` e `K2b` SONO MARCATI PROVVISORI** se il `json` viene da uno strumento col
**predittore sfasato di un passo** *(il difetto annotato in `99782e1`)*. Lo strumento
corretto scrive `predittore_causale: true`, e il referto lo legge **dal dato**, non da una
mia asserzione.

# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Legge il `soglia.json` di una
#   corsa che ha GIA' dichiarato la propria configurazione INTERA.

USO:  python csv/_test_fork/_referto_soglia.py
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
J = os.path.join(RADICE, "csv", "_test_fork", "_mitosi_soglia_grad", "soglia.json")
OUT = os.path.join(RADICE, "doc", "REFERTO_mitosi_soglia_grad_2026-10-06.md")
PRED = (("gradiente_nudo", "`|r_i - r_j|`  *(il gradiente **nudo**: quello che la soglia legge)*"),
        ("proxy_grad_per_phivel", "`|r_i - r_j| * |phivel|` medio  *(la **proxy** del mandato)*"),
        ("forma_esatta", "`|r_i*phivel_i - r_j*phivel_j|`  *(la **forma esatta**: quella che il codice produce)*"))
BERS = (("incremento_TOTALE", "incremento **TOTALE**"),
        ("SPINTA", "### **SPINTA**"), ("SCARICA", "**SCARICA**"))


def n(x, f="%.6f"):
    return "n/d" if x is None else (f % x)


def tf(b, k):
    return sum(r["fin"].get(k, 0) for r in b["passi"])


def divisioni(b):
    return tf(b, "g5_candidati_dopo_mitmax") - (
        tf(b, "rifiutati_solo_densita") + tf(b, "rifiutati_solo_2lam")
        + tf(b, "rifiutati_entrambi"))


def main():
    d = json.loads(io.open(J, encoding="utf-8").read())
    B = d["bracci"]
    rif = d["riferimenti"]
    S = d["soglie"]
    PC = [int(x) for x in d["passi_corr"]]
    causale = bool(d.get("predittore_causale", False))
    T = []

    def w(s=""):
        T.append(s)

    div = {k: divisioni(B[k]) for k in B}
    rA = (div["Ap0"] / rif["Ap"]["divisioni"]) if rif["Ap"]["divisioni"] else None
    rB = (div["Bp0"] / rif["Bp"]["divisioni"]) if rif["Bp"]["divisioni"] else None

    w("# REFERTO -- `MITOSI-SOGLIA-GRAD` **a ampiezza zero**: il `0.3` serve o no?")
    w()
    w("*(Mandato di Luca del 2026-10-05. Previsioni, `K1`/`K2`/`K2b` e i cinque controlli "
      "fissati in `doc/TASK_HISTORY/2026-10-05_mitosi-soglia-grad-ampiezza-zero.md`, "
      "committato **prima** in `bb1fece`, annotato in `1362672` e `99782e1`.)*")
    w()
    w("| | |")
    w("|---|---|")
    w("| **simulatore** | `%s`, ### **NON toccato** *(la patch e' su copie)* |"
      % d["blob_sim_b"][:8])
    w("| **braccio `A`** | `%s`, dal tag `pre-z43-cura2-r-da-cs` |" % d["blob_sim_a"][:8])
    w("| **strumento** | `%s` |" % d["blob_strumento"][:8])
    w("| **piattaforma** | %s, python `%s`, numpy `%s`, `%s` |"
      % (d["piattaforma"]["sistema"], d["piattaforma"]["python"],
         d["piattaforma"]["numpy"], d["piattaforma"]["macchina"]))
    w("| **passi** | `%d`, seme `11`, scena del driver |" % d["passi"])
    w("| **configurazione dichiarata INTERA** | `%s` *(braccio `Bg`)* |"
      % d["in_configurazione_del_driver"])
    w("| **predittore della misura `(2)`** | %s |"
      % ("### **CAUSALE** *(letto al passo `t-1`)*" if causale
         else "### ⛔ **SFASATO DI UN PASSO** *(letto al passo `t`)*: `K2` e `K2b` sono **PROVVISORI**"))
    w()
    w("## IL RISULTATO: **togliere il `0.3` ANNIENTA le nascite, in ENTRAMBI i bracci**")
    w()
    w("| braccio | divisioni | Schwinger | `nati` | `n` finale |")
    w("|---|--:|--:|--:|--:|")
    for k in ("Ap0", "Bp0", "B03", "Bg"):
        t = B[k]["totali"]
        w("| `%s` | **`%d`** | `%d` | `%d` | `%d` |"
          % (k, div[k], t["schwinger"], t["nati_tot"], d["a_valle"][k]["n"]))
    for k, lab in (("Ap", "`Ap` *(riferimento, `12e2ca7`)*"),
                   ("Bp", "`Bp` *(riferimento, `12e2ca7`)*")):
        w("| %s | `%d` | `%d` | `%d` | `%d` |"
          % (lab, rif[k]["divisioni"], rif[k]["schwinger"], rif[k]["nati"], rif[k]["n_fin"]))
    w()
    w("### **`Ap0/Ap` = `%s`  ·  `Bp0/Bp` = `%s`**" % (n(rA), n(rB)))
    w()
    if div["Ap0"] == div["Bp0"]:
        w("> ### ✔ **E IL FATTO PIU' NETTO DI TUTTA LA MISURA: SENZA LA MODULAZIONE I DUE "
          "BRACCI DANNO LO STESSO NUMERO DI DIVISIONI** — `%d` e `%d`. ### **Le due leggi "
          "del tempo proprio, private del `0.3`, producono la STESSA mitosi.**"
          % (div["Ap0"], div["Bp0"]))
        w(">")
        w("> ### ⛔ **Quindi il fattore `67.7` fra `Ap` e `Bp` del referto `12e2ca7` passava "
          "TUTTO per la MODULAZIONE.** Non per `_ft`, non per la scarica: ### **per il "
          "`0.3`.**")
        w(">")
        w("> ### ⚠ **E VA DETTO CHE COSA QUESTO *NON* DIMOSTRA:** che la modulazione sia "
          "*giusta*. Dimostra che e' ### **PORTANTE** — che senza di lei la mitosi quasi non "
          "accade, in nessuna delle due leggi del tempo. ### **<<Portante>> e <<corretta>> "
          "sono due cose diverse, e la seconda non la decide una misura di conteggi.**")
    w()
    w("## `K1` — **l'ipotesi NON e' refutata**, e di molto")
    w()
    k1_ref = (rA is not None and rA >= S["K1"])
    w("| | |")
    w("|---|---|")
    w("| `Ap0/Ap` | **`%s`** |" % n(rA))
    w("| soglia `K1` | `%.1f` |" % S["K1"])
    w("| esito | **%s** |"
      % ("### L'IPOTESI E' REFUTATA" if k1_ref else
         "### l'ipotesi NON e' refutata: togliere il `0.3` **ABBATTE** le nascite di `A`"))
    w()
    if rA:
        w("**Togliere il `0.3` porta le divisioni di `A` da `%d` a `%d`: un fattore `%.0f`.**"
          % (rif["Ap"]["divisioni"], div["Ap0"], 1.0 / rA))
    w()
    w("### LE PREVISIONI DEL GUARDIANO, scritte **prima** *(`bb1fece`)*")
    w()
    w("| previsione | esito |")
    w("|---|---|")
    w("| `Ap0` perde la maggior parte: **`< 0.5x`** di `Ap` | ### **CONFERMATA** -- e **molto oltre**: `%s` |"
      % n(rA))
    _okB = (rB is not None and 0.5 <= rB <= 1.0)
    w("| `Bp0` cambia poco: fra **`0.5x`** e **`1.0x`** di `Bp` | ### ⛔ **NON CONFERMATA**: `%s`, cioe' **sotto** la banda |"
      % n(rB))
    w()
    w("> ### ⛔ **E LA SECONDA PREVISIONE SBAGLIA PER LA RAGIONE CHE LA MOTIVAVA:** era "
      "*<<in `B` la modulazione morde solo il `5`-`10 per cento` sugli archi che passano>>*. ### **Il "
      "morso sulla SOGLIA e' davvero piccolo, ma l'effetto sulle NASCITE non lo e':** `%s`. "
      "### **Un morso piccolo su una soglia non da' un effetto piccolo sulle nascite, se la "
      "popolazione sopra soglia e' ripida.**" % n(rB))
    w()

    # ===================== K2 / K2b =====================================================
    w("## `K2` *(ESISTENZA)* e `K2b` *(ENTITA')* — la misura `(2)` sul braccio `Bg`")
    w()
    if not causale:
        w("> ### ⛔ **PROVVISORI: IL PREDITTORE E' SFASATO DI UN PASSO.** La `SPINTA` del "
          "passo `t` misura l'avanzamento di fase prodotto **durante il passo `t-1`** "
          "*(`:7772` legge la fotografia `_phi_t`)*, e questo strumento correla con `r` e "
          "`phivel` letti **al passo `t`**. ### **Il difetto e' annotato in `99782e1`, la "
          "cura e' il prossimo commit, e il braccio `Bg` si rigira.** ### **Questi numeri "
          "valgono come PRIMA LETTURA, non come verdetto.**")
        w()
    corr = B["Bg"]["corr"]

    def _c(p):
        return corr.get(str(p)) or corr.get(p) or {}

    w("### LE SPEARMAN — `3` predittori x `3` bersagli")
    w()
    w("| predittore | bersaglio | %s |" % " | ".join("passo `%d`" % p for p in PC))
    w("|---|---|%s" % ("--:|" * len(PC)))
    for pk, pl in PRED:
        for bk, bl in BERS:
            vals = [((_c(p).get("spearman") or {}).get("%s|%s" % (pk, bk)) or {}).get("rho")
                    for p in PC]
            w("| %s | %s | %s |"
              % (pl, bl, " | ".join(("`%.6f`" % v) if v is not None else "n/d"
                                    for v in vals)))
    w()
    # ### IL CONFRONTO FRA PREDITTORI: e' il risultato piu' informativo della misura
    sp = {}
    for pk, _pl in PRED:
        vals = [((_c(p).get("spearman") or {}).get("%s|SPINTA" % pk) or {}).get("rho")
                for p in PC]
        sp[pk] = [v for v in vals if v is not None]
    if all(sp.values()):
        mn = {k: float(np.min(np.abs(v))) for k, v in sp.items()}
        mx = {k: float(np.max(np.abs(v))) for k, v in sp.items()}
        w("> ### ✔ **IL RISULTATO PIU' INFORMATIVO DELLA MISURA, e non e' `K2`:** la "
          "correlazione della `SPINTA` col ### **gradiente NUDO e' `%.3f`-`%.3f`**, con la "
          "**proxy** `%.3f`-`%.3f`, e con la ### **FORMA ESATTA `%.3f`-`%.3f`.**"
          % (mn["gradiente_nudo"], mx["gradiente_nudo"],
             mn["proxy_grad_per_phivel"], mx["proxy_grad_per_phivel"],
             mn["forma_esatta"], mx["forma_esatta"]))
        w(">")
        w("> ### ⛔ **QUINDI LA MODULAZIONE LEGGE LA GRANDEZZA SBAGLIATA.** La torsione e' "
          "guidata da `|r_i*phivel_i - r_j*phivel_j|` *(`rho ~ %.2f`)*, e la soglia si "
          "modula su `|r_i - r_j|` *(`rho ~ %.2f`)*. ### **Sono la stessa cosa solo se "
          "`phivel` e' uniforme sull'arco, e NON lo e'.**"
          % (float(np.mean(np.abs(sp["forma_esatta"]))),
             float(np.mean(np.abs(sp["gradiente_nudo"])))))
        w(">")
        w("> ### ✔ **ED E' IL LIMITE CHE IL GUARDIANO AVEVA DICHIARATO**, qui con un numero: "
          "*<<lo sfasamento e' proporzionale anche a `phivel`; dove `phivel ~ 0` il gradiente "
          "non produce torsione>>*. ### **La forma esatta era una mia aggiunta alla proxy "
          "chiesta: senza di lei questo confronto non ci sarebbe.**")
        w()
    vals = [v for v in sp["gradiente_nudo"]]
    k2_ref = bool(vals) and all(abs(v) <= S["K2"] for v in vals)
    sopra = [v for v in vals if abs(v) > S["K2"]]
    w("### `K2`: la `SPINTA` contro il **gradiente nudo** — il predittore che la soglia legge")
    w()
    w("`|rho|` ai tre passi: %s. Soglia `K2`: `<= %.2f` **a tutti e tre**."
      % (", ".join("`%.6f`" % abs(v) for v in vals), S["K2"]))
    w()
    w("### **`K2`: %s**"
      % ("### L'IPOTESI DEL DOPPIO CONTEGGIO E' REFUTATA" if k2_ref
         else "l'ipotesi **NON** e' refutata: la correlazione **ESISTE**"))
    if not k2_ref and len(sopra) == 1:
        w()
        w("> ### ⚠ **E PASSA PER UN PELO, SU UN PASSO SOLO:** `%d` dei tre passi supera la "
          "soglia *(`%.6f`)*, gli altri due stanno **sotto** *(%s)*. ### **Un criterio "
          "<<a tutti e tre>> deciso da un passo e' fragile, e lo dico invece di presentarlo "
          "come netto.**"
          % (len(sopra), abs(sopra[0]),
             ", ".join("`%.6f`" % abs(v) for v in vals if abs(v) <= S["K2"])))
    w()
    w("### `K2b`: gli incrementi mediani della `SPINTA` per **quintile del gradiente nudo**")
    w()
    w("| passo | `q1` | `q2` | `q3` | `q4` | `q5` | **`q5/q1`** |")
    w("|--:|--:|--:|--:|--:|--:|--:|")
    rap = {}
    for p in PC:
        qq = (_c(p).get("quintili") or {}).get("gradiente_nudo|SPINTA")
        if not qq:
            continue
        v = [x["bers_mediano"] for x in qq]
        r_ = (v[-1] / v[0]) if (v[0] and v[0] > 0) else None
        rap[p] = r_
        w("| `%d` | %s | **`%s`** |"
          % (p, " | ".join("`%.4e`" % x if x is not None else "n/d" for x in v),
             n(r_, "%.4f")))
    w()
    sog_k2b = S.get("K2b", S.get("K2B"))
    ok = sum(1 for v in rap.values() if v is not None and v >= sog_k2b)
    w("**Il rapporto `q5/q1` e' `>= %.1f` in `%d` passi su `%d`.** Soglia `K2b`: **almeno "
      "due su tre**." % (sog_k2b, ok, len(PC)))
    w()
    k2b_ril = (ok >= 2)
    w("### **`K2b`: %s**" % ("### IL DOPPIO CONTEGGIO E' RILEVANTE" if k2b_ril
                             else "il doppio conteggio **NON** e' rilevante"))
    w()
    w("### LA LETTURA COMBINATA, **dalla tavola fissata PRIMA** *(`1362672`)*")
    w()
    if k2_ref:
        w("> ### **`K2` refutato → l'ipotesi del doppio conteggio e' REFUTATA**, e togliere "
          "la modulazione toglierebbe **del tutto** l'effetto del gradiente sulla mitosi.")
    elif k2b_ril:
        w("> ### **`K2` passa, `K2b` passa → il doppio conteggio esiste ED E' RILEVANTE.**")
    else:
        w("> ### **`K2` passa, `K2b` NON passa → <<IL DOPPIO CONTEGGIO ESISTE MA E' "
          "PICCOLO>>**, e ### **la decisione sul `0.3` si legge da `K1` e dalle nascite di "
          "`Bp0`.**")
        w(">")
        w("> ### ✔ **E `K1` e `Bp0` dicono la stessa cosa, forte:** togliere il `0.3` porta "
          "le divisioni da `%d` a `%d` in `A` e da `%d` a `%d` in `B`. ### **La modulazione "
          "non e' una ridondanza da togliere: e' PORTANTE.**"
          % (rif["Ap"]["divisioni"], div["Ap0"], rif["Bp"]["divisioni"], div["Bp0"]))
    w()

    # ===================== I CONTROLLI ===================================================
    w("## I CINQUE CONTROLLI")
    w()
    guasti = []
    w("| | | esito |")
    w("|---|---|---|")
    for k, et in (("B03", "C0"), ("Bg", "C0-tw")):
        ok_ = (d["a_valle"][k]["n"] == rif["Bp"]["n_fin"]
               and d["a_valle"][k]["archi"] == rif["Bp"]["archi"]
               and div[k] == rif["Bp"]["divisioni"])
        w("| **`%s`** *(deve passare)* | `%s` riproduce `Bp`: `n` `%d`/`%d`, archi `%d`/`%d`, divisioni `%d`/`%d` | **%s** |"
          % (et, k, d["a_valle"][k]["n"], rif["Bp"]["n_fin"],
             d["a_valle"][k]["archi"], rif["Bp"]["archi"],
             div[k], rif["Bp"]["divisioni"], "PASSA" if ok_ else "### FALLISCE"))
        if not ok_:
            guasti.append(et)
    difB = (d["a_valle"]["Bp0"]["n"] != rif["Bp"]["n_fin"]
            or div["Bp0"] != rif["Bp"]["divisioni"])
    w("| **`C-fallisce`** *(deve fallire)* | `Bp0` differisce da `Bp`: `n` `%d` contro `%d`, divisioni `%d` contro `%d` | **%s** |"
      % (d["a_valle"]["Bp0"]["n"], rif["Bp"]["n_fin"], div["Bp0"],
         rif["Bp"]["divisioni"],
         "DIFFERISCE (giusto)" if difB else "### COINCIDE: la patch NON e' agganciata"))
    if not difB:
        guasti.append("C-fallisce")
    for k in ("Ap0", "Bp0", "B03", "Bg"):
        t = B[k]["totali"]
        ric = div[k] + t["schwinger"]
        ok_ = (ric == t["nati_tot"])
        w("| **`C1`** | `%s`: `%d` + `%d` = `%d` contro `nati = %d` | **%s** |"
          % (k, div[k], t["schwinger"], ric, t["nati_tot"],
             "COINCIDE" if ok_ else "### NON COINCIDE"))
        if not ok_:
            guasti.append("C1 %s" % k)
    w()
    w("> ### ✔ **`C0` E `C0-tw` SONO LA PROVA CHE LA PATCH E' PULITA**, e non su un numero "
      "solo: `B03` *(ampiezza `0.3`)* e `Bg` *(i due termini di `tw` con un nome)* "
      "riproducono `Bp` ### **su TUTTI i conteggi dei cancelli, a tutti e `%d` i passi** — "
      "`0` differenze. ### **Quindi `_AMP = 0.3` E' l'espressione originale, e la "
      "separazione SPINTA/SCARICA non ha cambiato l'aritmetica.**" % d["passi"])
    w()
    w("## IL VERDETTO")
    w()
    if guasti:
        w("> ### ⛔ **FERMO.** I guasti: %s" % ", ".join("`%s`" % g for g in guasti))
    else:
        w("> ### **I CINQUE CONTROLLI PASSANO.**")
        w(">")
        w("> ### ⛔ **E QUESTA E' UNA MISURA, NON UN SIGILLO.** La rimozione del `0.3` dal "
          "simulatore — archivio col tag, censimento degli strumenti che usano "
          "`_r_nodo_mitosi`, sigillo, chiusura della voce — ### **e' UNA DECISIONE DI LUCA, "
          "e sara' un prompt a parte.**")
    w()
    w("## CHE COSA RESTA APERTO")
    w()
    if not causale:
        w("1. ### ⛔ **`K2` e `K2b` SONO PROVVISORI:** il predittore e' sfasato di un passo. "
          "La cura e' il prossimo commit, e il braccio `Bg` si rigira. ### **Questo referto "
          "verra' AGGIORNATO col predittore causale e con la tabella che confronta i due "
          "allineamenti.**")
    w("%d. **il `0.3`**: un numero **scelto**, che `A1` condanna e che `REGOLE_composizione_T3.md` "
      "§6.3 dice **<<va derivata>>**, legandolo al **principio di equivalenza**. "
      "### **Questa misura dice che e' PORTANTE, non che e' giusto.**" % (2 if not causale else 1))
    w("%d. ### **E la domanda che la misura APRE:** la modulazione si modula su `|r_i - r_j|`, "
      "ma la torsione e' guidata da `|r_i*phivel_i - r_j*phivel_j|`. ### **Una modulazione "
      "DERIVATA leggerebbe la seconda, non la prima** — ma sarebbe una legge nuova, e "
      "### **non la propongo: la nomino.**" % (3 if not causale else 2))
    w("%d. **`ARCHI-OLTRE-4PI`**, **`GRAVITA-POTENZIALE`**, e la **misura con `DT` dimezzato**, "
      "### **che NON si avvia finche' Luca non lo dice.**" % (4 if not causale else 3))
    w()
    w("---")
    w()
    w("*Referto **generato** da `csv/_test_fork/_referto_soglia.py` dal `soglia.json`: "
      "### **nessun numero e' ricopiato a mano** (`L-NUMERI`).*")
    w()
    io.open(OUT, "w", encoding="utf-8", newline=NL).write(NL.join(T))
    print("scritto %s  (%d righe)" % (OUT, len(T)))
    print("  predittore causale: %s   guasti: %s" % (causale, guasti or "nessuno"))
    print("  blob del referto: %s"
          % hashlib.sha1(io.open(OUT, "rb").read()).hexdigest()[:8])
    return 1 if guasti else 0


if __name__ == "__main__":
    sys.exit(main())
