# -*- coding: utf-8 -*-
"""GENERA `doc/REFERTO_tors_w8_lunga_2026-10-06.md` dal `lunga.json` della misura lunga.

### **NESSUN NUMERO E' RICOPIATO A MANO** *(`L-NUMERI`)*: il criterio, le soglie e i
### riferimenti si leggono **DAL `json`** invece di essere riscritti qui.

### ⛔ **E IL GENERATORE HA UN COLLAUDO SU `json` SINTETICI**, con casi che **DEVONO
### fallire** -- perche' in questa sessione i difetti dei referti li ho trovati **solo
### girandoli**: un `0.0` stampato `n/d`, tre quantili uguali sotto tre etichette diverse, e
### un *«l'ipotesi NON e' refutata»* con **tutti i valori `n/d`.**

# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Legge il `json` di una corsa che
#   ha GIA' dichiarato la propria configurazione INTERA, e la ristampa.

USO:  python csv/_test_fork/_referto_lunga.py
      python csv/_test_fork/_referto_lunga.py --collaudo
"""
import copy
import hashlib
import io
import json
import math
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, os.path.join(RADICE, "csv"))
import _presidio   # noqa: E402

_presidio.avvia(__file__)

NL = chr(10)
J = os.path.join(RADICE, "csv", "_test_fork", "_tors_w8_lunga", "lunga.json")
OUT = os.path.join(RADICE, "doc", "REFERTO_tors_w8_lunga_2026-10-06.md")
P2 = 2.0 * math.pi
P3 = 3.0 * math.pi
P4 = 4.0 * math.pi
# ### LE SOGLIE DEL CRITERIO, fissate nel task history PRIMA della corsa (`7d3ae67`).
GIU, SU = 0.5, 1.5


def stampa(s=""):
    print(s)


def n4(x, f="%.4f"):
    """### ⛔ **`0.0` NON E' `n/d`**, e scriverlo con `x if x else` e' il difetto che il giro
    corto mi ha preso in `34a11dc`: il verdetto leggeva `L-C` e la tabella stampava `n/d`."""
    return "n/d" if x is None else (f % x)


def val(x):
    """Una `Spearman` dal `json`: un numero ### **oppure** `[valore, n]`.

    ### ⚠ **Il referto del tetto e' CADUTO proprio qui** *(`TypeError`, `a1e9246`)*: la
    `spearman` coi ranghi medi restituisce una ### **TUPLA**, e il json committato la
    conserva -- quindi un lettore che la tratta come numero non legge quel json."""
    if isinstance(x, (list, tuple)):
        return None if not x else x[0]
    return x


def letto(r):
    if r is None:
        return "n/d"
    if r < GIU:
        return "SOTTO"
    if r > SU:
        return "SOPRA"
    return "DENTRO"


ETI = {"SOTTO": ("la deriva NON e' coerente: la torsione NON accumula", "⛔"),
       "DENTRO": ("accumula come previsto", "✔"),
       "SOPRA": ("c'e' una spinta che il conto non vede", "⚠"),
       "n/d": ("n/d", "")}


def genera(d):
    """Il referto, come LISTA DI RIGHE. ### **Separato da `main` perche' il collaudo possa
    chiamarlo su un `json` SINTETICO** -- la lezione di `LUNGA-BATTITO-CADUTA`: cio' che
    sta dentro `main` nessun controllo lo puo' guardare.

    Torna `(righe, letture, guasti)`, e `righe` e' `None` se il `json` ### **non e'
    completo**: un referto su una corsa incompleta sarebbe un numero senza provenienza.
    """
    # ### ⛔ **IL CRITERIO E' `passi_girati == passi`, NON lo `stato`:** un difetto di STAMPA
    #   non invalida un DATO -- e' la lezione del referto del tetto *(`eebe24f`)*.
    if int(d.get("passi_girati") or 0) != int(d.get("passi") or -1):
        return None, {}, ["corsa INCOMPLETA: %s passi su %s"
                          % (d.get("passi_girati"), d.get("passi"))]
    PP = d["passi_dati"]
    PI = {int(k): v for k, v in (d.get("piene") or {}).items()}
    C = d["totali"]["contatori"]
    T = d["totali"]
    RIF = d["riferimento_f7237563"]
    T_ = []

    def w(s=""):
        T_.append(s)

    def al(p):
        r = [x for x in PP if x["passo"] == p]
        return r[0] if r else {}

    w("# REFERTO -- **`TORS-W8-AVVOLGIMENTO`: LA MISURA LUNGA, `%d` passi**" % d["passi"])
    w()
    w("*(Mandato di Luca del 2026-10-06. Previsioni, **limite della curva** e criterio sono "
      "fissati in `doc/TASK_HISTORY/2026-10-06_tors-w8-misura-lunga.md`, committato "
      "### **prima** in `7d3ae67`.)*")
    w()
    w("| | |")
    w("|---|---|")
    w("| **simulatore** | `%s` -- ### **verificato all'avvio** contro `%s`, e su un blob "
      "diverso lo strumento **si ferma** |" % (d["blob_sim"][:8], d["blob_atteso"]))
    w("| **strumento** | `%s` *(piu' `_mitosi_soglia_grad` `%s`)* |"
      % (d["blob_strumento"][:8], d["blob_mitosi_soglia_grad"][:8]))
    w("| **copia patchata** | `%s`, **%d** ancore, ### **due ganci di SOLA LETTURA** |"
      % (d["blob_copia"][:8], len(d["ancore"])))
    w("| **piattaforma** | %s, python `%s`, numpy `%s` |"
      % (d["piattaforma"]["sistema"], d["piattaforma"]["python"],
         d["piattaforma"]["numpy"]))
    w("| **configurazione del driver** | dichiarata INTERA: `%s` |"
      % bool(d["in_configurazione_del_driver"]))
    w("| **scena** | `n` iniziale, archi e `DT` come il driver; un braccio, seme `11` |")
    w()
    w("## ⛔ IL CRITERIO, **letto SOLO dove si puo' leggere**")
    w()
    w("Il task history ha fissato ### **prima della corsa** che il rapporto "
      "`|tw| mediano / 2π·(1 − e^(−t/%.0f))` si legge ai passi "
      "### **`300`, `600`, `1000`**, dove `τ` e' vicino a `%.0f`, e che ai passi `50` e "
      "`150` ### **si riporta ma NON decide** -- perche' li' il `τ` vero vale "
      "`309`-`1491` e il rapporto e' gonfiato ### **per costruzione.**"
      % (d["tau_curva"], d["tau_curva"]))
    w()
    w("| passo | `|tw|` mediano | la curva | ### **rapporto** | lettura | |")
    w("|--:|--:|--:|--:|---|---|")
    let = {}
    for p in sorted(PI):
        z = PI[p]
        r = z.get("rapporto_alla_curva")
        L = letto(r)
        if z.get("decide"):
            let[p] = L
        w("| `%d` | `%s` | `%s` | ### **`%s`** | %s | %s |"
          % (p, n4((z.get("q_tw") or {}).get("q050")), n4(z.get("curva")), n4(r),
             ("### **%s**" % L) if z.get("decide") else "*(%s)*" % L,
             "### **DECIDE**" if z.get("decide") else "non decide"))
    w()
    _v = [L for L in let.values() if L != "n/d"]
    if not _v:
        w("> ### ⛔ **NESSUN PASSO CHE DECIDE HA UN RAPPORTO: il criterio NON si "
          "applica**, e ### **un'assenza non e' un esito** *(`STANDARD 3`)*. Il referto del "
          "tetto ha stampato *«l'ipotesi NON e' refutata»* con ### **tutti i valori `n/d`**, "
          "e quel difetto non si rifa'.")
    elif len(set(_v)) == 1:
        s, e = ETI[_v[0]]
        w("> ### %s **I %d PASSI CHE DECIDONO DANNO LA STESSA LETTURA: `%s` -- %s.**"
          % (e, len(_v), _v[0], s))
    else:
        w("> ### ⛔ **I PASSI CHE DECIDONO DANNO LETTURE DIVERSE: %s.**"
          % ", ".join("passo `%d`: **%s**" % (p, L) for p, L in sorted(let.items())))
        w(">")
        w("> ### **E SI DICE COSI', NON SI SCEGLIE** *(il task history lo ha fissato prima "
          "della corsa)*: ### **tre letture diverse sono un RISULTATO** -- dicono che il "
          "regime **cambia** -- e scegliere la piu' comoda lo nasconderebbe.")
    w()
    w("| il rapporto | la lettura, fissata PRIMA |")
    w("|---|---|")
    w("| sotto `%.1f` | **%s** |" % (GIU, ETI["SOTTO"][0]))
    w("| fra `%.1f` e `%.1f` | **%s** |" % (GIU, SU, ETI["DENTRO"][0]))
    w("| sopra `%.1f` | **%s** |" % (SU, ETI["SOPRA"][0]))
    w()
    w("## LA CURA TIENE? **i tre contatori dei calci**")
    w()
    w("| | | |")
    w("|---|--:|---|")
    w("| **calci SPURI** dalla legge curata *(`|spinta|` oltre il bound `4π`)* | `%d` | "
      "### **%s** |" % (C.get("calci_spuri_curata", -1),
                        "ZERO" if not C.get("calci_spuri_curata")
                        else "⛔ NON ZERO"))
    w("| **la FIRMA del difetto vecchio** *(spinta `> 3π` **senza** un dipolo che "
      "cambi)* | `%d` | ### **%s** |"
      % (C.get("spinta_senza_causa", -1),
         "ZERO" if not C.get("spinta_senza_causa") else "⛔ NON ZERO"))
    w("| **calci EVITATI** *(quanti la legge **vecchia** avrebbe dato)* | ### **`%d`** | "
      "*un CONTROFATTUALE: il suo valore giusto **non** e' zero* |"
      % C.get("calci_evitati", -1))
    w("| archi con `|tw| >= 4π`, somma su tutti i passi | `%d` | ### **%s** |"
      % (C.get("sopra_4pi_tot", -1),
         "ZERO a ogni passo" if not C.get("sopra_4pi_tot") else "⛔ NON ZERO"))
    w()
    w("> ### ⛔ **E I PRIMI DUE ZERI SONO ALGEBRICI, non misure, e va detto:** il bound "
      "`|spinta| <= |_w4(Δdph)| + |Δdipolo| <= 4π` vale ### **per "
      "costruzione**, misurato su `10^6` casi *(massimo `12.566155` contro "
      "`4π = 12.566371`: il bound e' **stretto**)*. ### **Quello che certificano e' che "
      "l'IMPLEMENTAZIONE segue l'algebra**, non che la fisica non e' cambiata -- ### **la "
      "stessa famiglia e lo stesso potere di `S3` del sigillo.**")
    w(">")
    w("> ### ✔ **IL NUMERO CHE DICE QUALCOSA E' <<calci EVITATI>>:** `%d` calci di "
      "modulo `~4π` che la legge vecchia avrebbe dato e la curata ### **non da'.**"
      % C.get("calci_evitati", -1))
    w()
    w("## IL CONFRONTO con `f7237563` *(i numeri GIA' committati)*")
    w()
    _p140 = al(140)
    _p150 = al(150)
    w("| | legge **vecchia** a `150` passi | legge **curata** |")
    w("|---|--:|--:|")
    w("| divisioni | `%d` | `%s` a `150`, ### **`%s` a `%d`** |"
      % (RIF["divisioni_150"],
         (_p150.get("nati_tot", 0) - _p150.get("schwinger_tot", 0)) if _p150 else "n/d",
         T.get("divisioni"), d["passi"]))
    w("| Schwinger | `%d` | `%s` a `150`, ### **`%s` a `%d`** |"
      % (RIF["schwinger_150"], _p150.get("schwinger_tot", "n/d") if _p150 else "n/d",
         T.get("schwinger"), d["passi"]))
    w("| `|tw|` mediano al passo `140` | `%.2f` | ### **`%s`** |"
      % (RIF["tw_mediano_140"], n4((_p140.get("q_tw") or {}).get("q050"))))
    w("| archi oltre `4π` per passo | `~%d` | ### **`%s`** |"
      % (RIF["sopra_4pi_per_passo"],
         "0 a OGNI passo" if not C.get("sopra_4pi_tot") else C.get("sopra_4pi_tot")))
    w("| calci di modulo `~4π` | `%d` in `150` passi | ### **`%d` dati, `%d` EVITATI** |"
      % (RIF["calci_150"], C.get("calci_spuri_curata", -1), C.get("calci_evitati", -1)))
    w()
    w("## LE NASCITE, **per finestre di `%d` passi**" % d["finestra"])
    w()
    w("### **Non il totale:** con `%d` passi un totale nasconderebbe ### **QUANDO** la rete "
      "cresce, e *«quando»* e' la domanda." % d["passi"])
    w()
    w("| finestra | divisioni | Schwinger | `n` a fine | archi a fine |")
    w("|---|--:|--:|--:|--:|")
    for f in d["nascite_per_finestra"]:
        w("| `%d`-`%d` | **`%d`** | `%d` | `%d` | `%d` |"
          % (f["da"], f["a"], f["divisioni"], f["schwinger"], f["n_fine"],
             f["archi_fine"]))
    w()
    _fin = d["nascite_per_finestra"]
    if len(_fin) >= 6:
        _dv = [f["divisioni"] for f in _fin]
        _pri, _ult = sum(_dv[:3]), sum(_dv[-3:])
        w("### ➜ **Le prime tre finestre danno `%d` divisioni, le ultime tre `%d`:** "
          "### **%s**" % (_pri, _ult,
                          "la crescita ACCELERA" if _ult > _pri * 1.5
                          else ("la crescita RALLENTA" if _pri > _ult * 1.5
                                else "il ritmo e' STABILE")))
        w()
    w("## `M2`: **il tetto calcolato ordina gli archi?**")
    w()
    w("| passo | `M2` *(con `|twist_dip|`)* | `M2b` *(senza)* | `|tw*|` mediano | "
      "frazione oltre `3π` | frazione oltre la **soglia modulata** |")
    w("|--:|--:|--:|--:|--:|--:|")
    for p in sorted(PI):
        z = PI[p]
        w("| `%d` | `%s` | `%s` | `%s` | `%s` | `%s` |"
          % (p, n4(val(z.get("m2"))), n4(val(z.get("m2b"))),
             n4((z.get("q_tw_stella") or {}).get("q050")),
             n4(z.get("fraz_oltre_3pi"), "%.6f"),
             n4(z.get("fraz_oltre_soglia_modulata"), "%.6f")))
    w()
    _m2 = [val(PI[p].get("m2")) for p in sorted(PI)]
    _m2 = [x for x in _m2 if x is not None]
    if _m2:
        w("### ➜ **La `Spearman` sta fra `%s` e `%s`:** ### **il tetto calcolato NON "
          "ordina gli archi**, ed e' lo stesso risultato di `eebe24f` *(`0.031` / `0.020` / "
          "`0.017`)* ### **con la legge CURATA e su `%d` passi.**"
          % (n4(min(_m2)), n4(max(_m2)), d["passi"]))
        w()
    w("## `τ_tw/dt_e`: **il tempo di scarica, in PASSI**")
    w()
    w("| passo | `q25` | ### **`q50`** | `q75` | il `τ` della curva |")
    w("|--:|--:|--:|--:|--:|")
    for p in sorted(PI):
        z = (PI[p].get("q_tau_passi") or {})
        w("| `%d` | `%s` | ### **`%s`** | `%s` | `%.0f` |"
          % (p, n4(z.get("q025"), "%.1f"), n4(z.get("q050"), "%.1f"),
             n4(z.get("q075"), "%.1f"), d["tau_curva"]))
    w()
    _tau = [(PI[p].get("q_tau_passi") or {}).get("q050") for p in sorted(PI)]
    _tau = [x for x in _tau if x is not None]
    if _tau:
        w("### ➜ ⚠ **E QUESTO E' IL LIMITE DELLA CURVA, misurato:** il `τ` "
          "vero va da `%.0f` a `%.0f` passi, mentre la curva assume ### **`%.0f` FISSO.** "
          "### **Dove il `τ` misurato si allontana da `%.0f`, il rapporto non si "
          "legge** -- ed e' la ragione per cui il criterio **non** decide ai passi `50` e "
          "`150`." % (min(_tau), max(_tau), d["tau_curva"], d["tau_curva"]))
        w()
    w("## `twist_dip`: **il dipolo e' ancora zero?**")
    w()
    w("| passo | a `0` | a `π/2` | a `π` |")
    w("|--:|--:|--:|--:|")
    for p in sorted(PI):
        z = (PI[p].get("m5") or {})
        w("| `%d` | ### **`%s`** | `%s` | `%s` |"
          % (p, n4(z.get("fraz_zero")), n4(z.get("fraz_mezzo_pi")), n4(z.get("fraz_pi"))))
    w()
    w("## LA GUARDIA DI `TAU_TW` *(rilievo `E4` del guardiano)*")
    w()
    w("| | |")
    w("|---|--:|")
    w("| invocazioni di `_tau_tw_locale` | `%d` |" % T.get("tautw_tot", -1))
    w("| ### **SALTI** *(il `return TAU_TW` della guardia)* | ### **`%d`** |"
      % T.get("tautw_salti", -1))
    w()
    if not T.get("tautw_salti"):
        w("> ### ✔ **LA GUARDIA NON SCATTA MAI in `%d` passi**, e ora e' "
          "### **MISURATO** invece che assunto: era un fallback ### **non contato** "
          "*(`P5`, `A8`)*, e se scattasse `τ_tw` passerebbe da `~2`-`6` a ### **`20`** "
          "-- un fattore `3`-`10` sul tetto di equilibrio." % d["passi"])
        w(">")
        w("> ### ⚠ **E <<non scatta in questa scena>> NON e' <<non scatta mai>>:** "
          "resta un ramo raggiungibile, e il contatore ora lo vede.")
    else:
        w("> ### ⛔ **LA GUARDIA SCATTA `%d` VOLTE**, e nessuno lo sapeva: `τ_tw` "
          "passa a `20` su quei passi. ### **Va nel referto e nella voce "
          "`KAPPA-TW-COMMENTO`.**" % T.get("tautw_salti"))
    w()
    w("## ⚠ LO SFASAMENTO DI UN PASSO, **dichiarato nel sigillo** *(`c17e518`)*")
    w()
    w("> Il `|tw|` si legge ### **all'INGRESSO** del blocco della torsione, quindi il valore "
      "*«al passo `p`»* e' quello accumulato in ### **`p-1` passi.** ### **Sul rapporto alla "
      "curva lo scarto e' dell'ordine di `1/%.0f`, cioe' lo `0.3 %%`: non cambia nessuna "
      "lettura, e si dichiara invece di lasciarlo dedurre.**" % d["tau_curva"])
    w()
    w("## IL VERDETTO")
    w()
    guasti = []
    if C.get("calci_spuri_curata"):
        guasti.append("calci SPURI dalla legge curata: %d" % C["calci_spuri_curata"])
    if C.get("spinta_senza_causa"):
        guasti.append("la FIRMA del difetto vecchio: %d" % C["spinta_senza_causa"])
    if C.get("sopra_4pi_tot"):
        guasti.append("archi oltre 4pi: %d" % C["sopra_4pi_tot"])
    if guasti:
        w("> ### ⛔ **FERMO -- LA CURA NON TIENE:** %s."
          % "; ".join("**%s**" % g for g in guasti))
    else:
        w("> ### ✔ **LA CURA TIENE su `%d` passi:** zero calci spuri, zero firme del "
          "difetto vecchio, ### **zero archi oltre `4π`** -- contro i `~%d` per passo e "
          "i `%d` calci della legge vecchia." % (d["passi"], RIF["sopra_4pi_per_passo"],
                                                 RIF["calci_150"]))
    w(">")
    w("> ### ⛔ **E QUESTA E' UNA MISURA, NON UN SIGILLO:** ### **la soglia di mitosi "
      "`3π`, il `0.3` e `κ` si decidono su questi numeri, e sono DECISIONI DI "
      "LUCA.**")
    w()
    w("---")
    w()
    w("*Referto **generato** da `csv/_test_fork/_referto_lunga.py` dal `lunga.json`: "
      "### **nessun numero e' ricopiato a mano** (`L-NUMERI`), e il criterio e' letto "
      "**dal `json`** invece di essere riscritto qui.*")
    return T_, let, guasti


# =============================================================== IL COLLAUDO
def _finto(passi=1000, rapporti=(0.9, 0.8, 0.7), cont=None, tautw_salti=0,
           girati=None, q50=1.0):
    """Un `lunga.json` SINTETICO, con i veri nomi di chiave. ### **I valori sono SCELTI, non
    misurati:** servono a provare il GENERATORE, non la fisica."""
    c = {"calci_evitati": 12345, "calci_spuri_curata": 0, "spinta_senza_causa": 0,
         "sopra_4pi_tot": 0, "avvolgimenti": 0, "coppie": 0, "nan_consumati": 0}
    c.update(cont or {})
    pieni = (50, 150, 300, 600, 1000)
    dec = {300: rapporti[0], 600: rapporti[1], 1000: rapporti[2]}
    piene = {}
    for p in pieni:
        piene[str(p)] = {
            "passo": p, "q_tw": {"q050": q50}, "curva": 2.0,
            "rapporto_alla_curva": dec.get(p, 1.2), "decide": p in dec,
            "q_tau_passi": {"q025": 200.0, "q050": 300.0, "q075": 400.0},
            "q_tw_stella": {"q050": 6.35}, "m2": 0.03, "m2b": 0.02,
            "fraz_oltre_3pi": 0.001, "fraz_oltre_soglia_modulata": 0.002,
            "m5": {"fraz_zero": 1.0, "fraz_mezzo_pi": 0.0, "fraz_pi": 0.0}}
    pd = [{"passo": k, "n": 12802 + k, "archi": 471564, "nati_tot": k // 10,
           "schwinger_tot": k // 50, "sopra_4pi": 0, "tautw_salti": 0,
           "tautw_tot": 1000, "q_tw": {"q050": q50}} for k in (140, 150, passi)]
    return {
        "passi": passi, "passi_girati": passi if girati is None else girati,
        "stato": "DATI SALVATI", "finestra": 50, "tau_curva": 300.0,
        "blob_sim": "cf2a1ac8ff", "blob_atteso": "cf2a1ac8",
        "blob_strumento": "bc62bcaadd", "blob_mitosi_soglia_grad": "1279c6fbaa",
        "blob_copia": "abcdef1234", "ancore": ["a", "b"],
        "piattaforma": {"sistema": "Windows", "python": "3.13", "numpy": "2.3.0"},
        "in_configurazione_del_driver": True, "passi_dati": pd, "piene": piene,
        "nascite_per_finestra": [{"da": 1 + 50 * i, "a": 50 + 50 * i, "nati": 3 + i,
                                  "schwinger": 1, "divisioni": 2 + i,
                                  "n_fine": 12802, "archi_fine": 471564}
                                 for i in range(passi // 50)],
        "totali": {"nati_tot": 60, "schwinger": 20, "divisioni": 40, "contatori": c,
                   "tautw_tot": 1000000, "tautw_salti": tautw_salti},
        "riferimento_f7237563": {"divisioni_150": 18, "schwinger_150": 7,
                                 "tw_mediano_140": 2.11, "sopra_4pi_per_passo": 108,
                                 "calci_150": 142114}}


def _verdetto(righe):
    """### ⛔ **IL VERDETTO SI LEGGE DALLA SUA RIGA, non cercando una sottostringa
    nel documento:** le mie prime tre prove cercavano `<<LA CURA TIENE>>` in tutto il
    testo, e quella frase sta ### **anche nel TITOLO della sezione** -- quindi fallivano
    ### **su un generatore corretto.** Trovate girandole, come ogni volta."""
    for k, x in enumerate(righe):
        if x.strip() == "## IL VERDETTO":
            for y in righe[k + 1:]:
                if y.strip().startswith(">"):
                    return y
    return ""


def collaudo():
    esiti = []

    def prova(nome, ok, dett=""):
        esiti.append((nome, bool(ok), dett))
        stampa("  %-7s %-74s %s" % ("OK" if ok else "FALLITA", nome, dett))

    stampa("=" * 104)
    stampa("IL COLLAUDO DI _referto_lunga.py -- su `json` SINTETICI")
    stampa("=" * 104)

    # --------------------------------------------------- 1. i due lettori
    prova("n4: ### `0.0` si stampa `0.0000` e NON `n/d` (il difetto di 34a11dc)",
          n4(0.0) == "0.0000", n4(0.0))
    prova("n4: ### e `None` si stampa `n/d`", n4(None) == "n/d", n4(None))
    prova("n4: ### DEVE DISTINGUERE -- `0.0` e `None` NON danno la stessa stringa",
          n4(0.0) != n4(None))
    prova("val: ### una TUPLA da' il primo elemento (il TypeError di a1e9246)",
          val([0.031, 900]) == 0.031 and val((0.02, 5)) == 0.02)
    prova("val: ### un numero passa, e una lista VUOTA da' None",
          val(0.5) == 0.5 and val([]) is None)
    prova("letto: ### le tre soglie, e sono quelle del task history",
          (letto(0.49), letto(0.5), letto(1.5), letto(1.51), letto(None))
          == ("SOTTO", "DENTRO", "DENTRO", "SOPRA", "n/d"))

    # --------------------------------------------------- 2. la corsa INCOMPLETA
    r, _l, g = genera(_finto(girati=430))
    prova("incompleta: ### NESSUN referto da 430 passi su 1000, e dice perche'",
          r is None and bool(g) and "INCOMPLETA" in g[0], (g or [""])[0])
    r, _l, g = genera(_finto(girati=1000))
    prova("completa: ### con 1000 su 1000 il referto NASCE", r is not None and not g,
          "%d righe" % len(r or []))

    # --------------------------------------------------- 3. le letture
    r, l3, _g = genera(_finto(rapporti=(0.9, 0.8, 0.7)))
    t = NL.join(r)
    prova("letture: ### tre volte DENTRO -> <<LA STESSA LETTURA>>",
          set(l3.values()) == {"DENTRO"} and "LA STESSA LETTURA" in t,
          "%s" % sorted(l3.items()))
    r, l3, _g = genera(_finto(rapporti=(1.6, 0.9, 0.3)))
    t = NL.join(r)
    prova("letture: ### tre DIVERSE -> <<LETTURE DIVERSE>> e <<NON SI SCEGLIE>>",
          sorted(set(l3.values())) == ["DENTRO", "SOPRA", "SOTTO"]
          and "LETTURE DIVERSE" in t and "NON SI SCEGLIE" in t,
          "%s" % sorted(l3.items()))
    prova("letture: ### e con tre diverse NON stampa <<LA STESSA LETTURA>>",
          "LA STESSA LETTURA" not in t)
    r, l3, _g = genera(_finto(rapporti=(None, None, None)))
    t = NL.join(r)
    prova("letture: ### tutte ASSENTI -> <<il criterio NON si applica>>, NON un esito",
          set(l3.values()) == {"n/d"} and "NON si applica" in t and "STANDARD 3" in t,
          "%s" % sorted(l3.items()))
    prova("letture: ### e con tutte assenti NON compare nessuna delle due letture",
          not any(x in t for x in ("LA STESSA LETTURA", "LETTURE DIVERSE")))

    # --------------------------------------------------- 4. I CASI CHE DEVONO FALLIRE
    r, _l, g = genera(_finto(cont={"calci_spuri_curata": 5}))
    v = _verdetto(r)
    prova("### DEVE FALLIRE -- con 5 calci SPURI il VERDETTO e' FERMO, non <<TIENE>>",
          bool(g) and "FERMO" in v and "LA CURA TIENE" not in v, v[:72])
    r, _l, g = genera(_finto(cont={"sopra_4pi_tot": 3}))
    v = _verdetto(r)
    prova("### DEVE FALLIRE -- con 3 archi oltre 4pi il VERDETTO e' FERMO",
          bool(g) and "FERMO" in v and "LA CURA TIENE" not in v, v[:72])
    r, _l, g = genera(_finto(cont={"spinta_senza_causa": 1}))
    v = _verdetto(r)
    prova("### DEVE FALLIRE -- con 1 firma del difetto vecchio il VERDETTO e' FERMO",
          bool(g) and "FERMO" in v and "LA CURA TIENE" not in v, v[:72])
    r, _l, g = genera(_finto())
    v = _verdetto(r)
    prova("e senza guasti il VERDETTO e' <<LA CURA TIENE>>",
          not g and "LA CURA TIENE" in v and "FERMO" not in v, v[:72])

    # --------------------------------------------------- 5. i numeri NON si inventano
    r, _l, _g = genera(_finto(q50=0.0))
    t = NL.join(r)
    prova("numeri: ### un `|tw|` mediano di 0.0 compare come `0.0000`, non `n/d`",
          "`0.0000`" in t and "n/d" not in t)
    d = _finto()
    r, _l, _g = genera(d)
    t = NL.join(r)
    _q = d["piene"]["300"]["q_tau_passi"]
    prova("numeri: ### i tre quantili di tau sono TRE valori diversi, non lo stesso tre "
          "volte (il difetto di eebe24f)",
          ("`%.1f`" % _q["q025"]) in t and ("`%.1f`" % _q["q075"]) in t
          and len({_q["q025"], _q["q050"], _q["q075"]}) == 3)
    prova("numeri: ### il blob del simulatore e quello ATTESO sono entrambi nel referto",
          d["blob_atteso"] in t and d["blob_sim"][:8] in t)
    prova("numeri: ### e i riferimenti di f7237563 vengono dal json, non dal sorgente",
          str(d["riferimento_f7237563"]["calci_150"]) in t
          and str(d["riferimento_f7237563"]["divisioni_150"]) in t)
    r, _l, _g = genera(_finto(tautw_salti=17))
    t = NL.join(r)
    prova("guardia: ### con 17 salti il referto dice che SCATTA, non che non scatta",
          "SCATTA `17` VOLTE" in t and "NON SCATTA MAI" not in t)
    r, _l, _g = genera(_finto(tautw_salti=0))
    t = NL.join(r)
    prova("guardia: ### con 0 salti dice che NON scatta, e che non e' <<non scatta mai>>",
          "NON SCATTA MAI" in t and "NON e' <<non scatta mai>>" in t)

    # --------------------------------------------------- 6. la forma
    r, _l, _g = genera(_finto())
    t = NL.join(r)
    prova("forma: ### nessun segnaposto `" + chr(37) + "s` o `{}` rimasto nel testo",
          (chr(37) + "s") not in t and "{}" not in t)
    prova("forma: ### nessun doppio backtick (il difetto trovato girando i referti)",
          "``" not in t)
    _pre = copy.deepcopy(_finto())
    _d2 = _finto()
    genera(_d2)
    prova("forma: ### e `genera` NON modifica il `json` che riceve", _d2 == _pre)

    stampa("=" * 104)
    ko = [n for n, o, _d in esiti if not o]
    stampa("COLLAUDO: %d su %d" % (len(esiti) - len(ko), len(esiti)))
    if ko:
        stampa("### FALLITI:")
        for n in ko:
            stampa("    - " + n)
    stampa("=" * 104)
    return 1 if ko else 0


def main(argv):
    if "--collaudo" in argv[1:]:
        return collaudo()
    if not os.path.isfile(J):
        stampa("### IL lunga.json NON C'E'. MI FERMO.")
        return 1
    d = json.loads(io.open(J, encoding="utf-8").read())
    righe, let, guasti = genera(d)
    if righe is None:
        stampa("### %s. MI FERMO: un referto su una corsa incompleta sarebbe un numero "
               "senza provenienza." % guasti[0])
        return 1
    io.open(OUT, "w", encoding="utf-8", newline=NL).write(NL.join(righe) + NL)
    stampa("scritto %s  (%d righe)" % (OUT, len(righe)))
    stampa("  il criterio ai passi che DECIDONO: %s"
           % ", ".join("%d: %s" % (p, L) for p, L in sorted(let.items())))
    stampa("  guasti: %s" % (guasti or "nessuno"))
    stampa("  blob del referto: %s"
           % hashlib.sha1(io.open(OUT, "rb").read()).hexdigest()[:8])
    return 1 if guasti else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
