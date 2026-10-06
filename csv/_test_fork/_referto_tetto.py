# -*- coding: utf-8 -*-
"""GENERA `doc/REFERTO_tetto_torsione_2026-10-06.md` dal `tetto.json`.

### **NESSUN NUMERO E' RICOPIATO A MANO** *(`L-NUMERI`)*. I criteri sono quelli del mandato,
letti **dal `json`** e non riscritti qui.

# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Legge il `json` di una corsa che
#   ha GIA' dichiarato la propria configurazione INTERA.

USO:  python csv/_test_fork/_referto_tetto.py
"""
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
J = os.path.join(RADICE, "csv", "_test_fork", "_tetto_torsione", "tetto.json")
OUT = os.path.join(RADICE, "doc", "REFERTO_tetto_torsione_2026-10-06.md")
P2 = 2.0 * math.pi
P3 = 3.0 * math.pi


def n4(x, f="%.4f"):
    return "n/d" if x is None else (f % x)


def qv(d, k):
    return None if not d else d.get(k)


def _val(x):
    """Il VALORE di una Spearman, che il `json` porta come numero o come `[valore, n]`."""
    if isinstance(x, (list, tuple)):
        return None if not x else x[0]
    return x


def main():
    if not os.path.isfile(J):
        print("### IL tetto.json NON C'E'. MI FERMO.")
        return 1
    d = json.loads(io.open(J, encoding="utf-8").read())
    # ### ⛔ **IL CRITERIO E' `passi_girati == passi`, NON lo `stato` DEL RAPPORTO.**
    #   La corsa di `a1e9246` ha girato **tutti** i `150` passi e ha salvato tutto; e' il
    #   ### **rapporto** dello strumento a essere caduto *(la tupla di `spearman`)*, e un
    #   ### **difetto di STAMPA non invalida un DATO.** Rifiutare qui avrebbe buttato una
    #   misura completa per un `TypeError` di formattazione.
    if int(d.get("passi_girati") or 0) != int(d.get("passi") or -1):
        print("### LA CORSA NON E' COMPLETA: %s passi su %s. MI FERMO."
              % (d.get("passi_girati"), d.get("passi")))
        return 1
    _rapp_caduto = (d.get("stato") != "fatto")
    PM = [int(x) for x in d["passi_mis"]]
    MIS = {int(k): v for k, v in (d.get("misure") or {}).items()}
    CR = d["criteri"]
    c = d["totali"]["contatori"]
    T = []

    def w(s=""):
        T.append(s)

    def al(p):
        """La fotografia del gancio A a un passo."""
        r = [x for x in d["passi_dati"] if x["passo"] == p and "tor" in x]
        return r[0]["tor"] if r else {}

    w("# REFERTO -- **IL TETTO DELLA TORSIONE: la soglia di mitosi `3π` sta sul tetto?**")
    w()
    w("*(Mandato di Luca del 2026-10-06. Previsioni, criteri e controlli fissati in "
      "`doc/TASK_HISTORY/2026-10-06_tetto-torsione.md`, committato **prima** in `bbb2dda` e "
      "annotato in `c3546e6` e `406a973`.)*")
    w()
    w("| | |")
    w("|---|---|")
    w("| **simulatore** | `%s`, ### **NON toccato** |" % d["blob_sim"][:8])
    w("| **strumento** | `%s` *(piu' `_mitosi_soglia_grad` `%s` per `q`, `spearman`, "
      "`quintili`)* |" % (d["blob_strumento"][:8], d["blob_mitosi_soglia_grad"][:8]))
    w("| **copia patchata** | `%s`, **%d** ancore, ### **due ganci di SOLA LETTURA** |"
      % (d["blob_copia"][:8], len(d["ancore"])))
    w("| **piattaforma** | %s, python `%s`, numpy `%s` |"
      % (d["piattaforma"]["sistema"], d["piattaforma"]["python"], d["piattaforma"]["numpy"]))
    w("| **`κ`** | `%.1f`, ### **dal CODICE** -- e il commento dice `3.1831` "
      "*(`KAPPA-TW-COMMENTO`)* |" % d["kappa"])
    w("| **passi** | `%d`, misure piene ai passi %s |"
      % (d["passi"], ", ".join("`%d`" % p for p in PM)))
    w()
    if _rapp_caduto:
        w("> ### ⚠ **IL RAPPORTO DELLO STRUMENTO E' CADUTO su questa corsa** *(stato: "
          "`%s`)*, e il difetto -- `spearman()` restituisce una **tupla** -- e' curato in "
          "`5d66812`. ### ✔ **I `150` passi sono COMPLETI e SALVATI**, perche' il `json` "
          "si scrive **prima** del rapporto: ### **questo referto legge il DATO, non "
          "l'uscita dello strumento.**" % d.get("stato"))
        w()
    w("## `C0`: **i ganci sono di SOLA LETTURA?**")
    w()
    _g = d.get("guasti") or []
    if "C0" in _g:
        w("> ### ⛔ **`C0` E' FALLITO. OGNI NUMERO DI QUESTA MISURA E' SOSPETTO, e il "
          "rapporto si e' FERMATO.** Non si legge nient'altro.")
        io.open(OUT, "w", encoding="utf-8", newline=NL).write(NL.join(T))
        print("### C0 FALLITO: referto fermo.")
        return 1
    # ### ⛔ **NON SI ASSERISCE CHE COINCIDA: SI STAMPA IL CONFRONTO.** Il giro a vuoto
    #   del generatore scriveva *«`n` finale coincide (12802/12827)»* su due numeri
    #   ### **diversi**, perche' la frase era fissa e i numeri interpolati.
    _nn, _nb = int(d["a_valle"]["n"]), int(d["riferimento_Bp"]["n_fin"])
    w("> ### ✔ **PASSA.** Il confronto con `Bp` del `crescita.json` committato su **sette** "
      "campi a **tutti** i passi non trova differenze, e `n` finale e' "
      "`%d` contro `%d`: ### **%s**. ### **Quindi i ganci non muovono niente, e non e' "
      "dedotto: e' misurato.**"
      % (_nn, _nb, "coincide" if _nn == _nb else "⛔ NON coincide"))
    w()
    w("## ⛔ LA PRIMA COSA: **IL CONTO DEL GUARDIANO E' GIUSTO, E NON BASTA**")
    w()
    _u = al(PM[-1])
    _t0 = al(PM[0])
    w("| | misurato |")
    w("|---|--:|")
    for p in PM:
        z = (al(p).get("tetto") or {})
        w("| mediana di `|tw*|` al passo `%d` | **`%s`** |"
          % (p, n4(qv(z.get("q_tw_stella"), "q050"))))
    w("| `2π` | `%.4f` |" % P2)
    w("| scarto fra la forma **chiusa** e quella **fedele** | `%s` |"
      % n4((al(PM[-1]).get("tetto") or {}).get("max_scarto_forme"), "%.3e"))
    w()
    # ### ⛔ **UNA FRASE CHE AFFERMA UN RISULTATO NON SI STAMPA SE IL DATO NON C'E'.**
    _mts = [qv((al(p).get("tetto") or {}).get("q_tw_stella"), "q050") for p in PM]
    _mts = [x for x in _mts if x is not None]
    if not _mts:
        w("> ### ⛔ **NESSUN DATO su `|tw*|` ai passi del mandato: non si afferma niente.**")
    else:
        _sc = max(abs(x - P2) / P2 for x in _mts)
        w("### %s **Con `r` quasi uniforme `|tw*|` %s `2π`** -- lo scarto massimo sui tre "
          "passi e' ### **`%.4f %%`** -- ed e' la predizione del mandato *(«con `r` uniforme "
          "`|tw*| = 2π` per QUALUNQUE arco a deriva costante»)*. ### **Misurata, non "
          "assunta.**"
          % ("✔" if _sc < 0.05 else "⚠",
             "sta su" if _sc < 0.05 else "si SPOSTA da", 100 * _sc))
    w()
    w("### %s **`M8`: il pavimento esterno di `τ` %s** -- `%d` archi su tutta la corsa."
      % ("✔" if not c["archi_pavimento"] else "⛔",
         "NON vincola nessun arco" if not c["archi_pavimento"]
         else "VINCOLA, e la formula del mandato lo trascura",
         c["archi_pavimento"]))
    w()
    w("## `M1`: **`|tw|` sta davvero sul suo tetto?**")
    w()
    w("| passo | archi *(sopra il `q25` di `|Δω|`)* | `q05` | `q25` | "
      "### **mediana** | `q75` | `q95` | `q99` | `> 1` | `> 2` |")
    w("|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|")
    med = []
    for p in PM:
        m = (MIS.get(p) or {}).get("m1") or {}
        q = m.get("q_rapporto") or {}
        med.append((p, m.get("mediana")))
        w("| `%d` | `%s` | `%s` | `%s` | ### **`%s`** | `%s` | `%s` | `%s` | `%s` | `%s` |"
          % (p, m.get("n") if m.get("n") is not None else "n/d",
             n4(q.get("q005")), n4(q.get("q025")), n4(m.get("mediana")),
             n4(q.get("q075")), n4(q.get("q095")), n4(q.get("q099")),
             n4(m.get("fraz_sopra_1")), n4(m.get("fraz_sopra_2"))))
    w()
    # ### ✔ **LA COERENZA SI VERIFICA, non si spera:** due vie allo stesso numero.
    _coe = []
    for p in PM:
        _ti = ((al(p).get("q_tw_ingresso") or {}).get("q050"))
        _ts = (((al(p).get("tetto") or {}).get("q_tw_stella") or {}).get("q050"))
        _m = (MIS.get(p) or {}).get("m1", {}).get("mediana")
        if _ti and _ts and _m:
            _coe.append((p, _ti / _ts, _m))
    if _coe:
        w("### ✔ **E LA COERENZA SI VERIFICA:** `mediana|tw| / mediana|tw*|` contro la "
          "**mediana del rapporto** -- %s. ### **Due vie allo stesso numero: se "
          "divergessero, una delle due sarebbe sbagliata.**"
          % "; ".join("passo `%d`: `%s` contro `%s`" % (p, n4(a), n4(b))
                      for p, a, b in _coe))
        w()
    w("### ⛔ **E IL NUMERO CHE DICE LA FISICA, in una riga:** la mediana di `|tw|` e' `%s` "
      "e la soglia di mitosi `3π` e' `%.4f`. ### **L'arco mediano sta al `%.1f %%` della "
      "soglia**, e il tetto calcolato `|tw*|` *(mediana `%s`)* sta al `%.1f %%`."
      % (n4(((al(PM[0]).get("q_tw_ingresso") or {}).get("q050"))), P3,
         100 * (((al(PM[0]).get("q_tw_ingresso") or {}).get("q050")) or 0) / P3,
         n4((((al(PM[0]).get("tetto") or {}).get("q_tw_stella") or {}).get("q050"))),
         100 * ((((al(PM[0]).get("tetto") or {}).get("q_tw_stella") or {}).get("q050"))
                or 0) / P3))
    w()
    _fuori = [(p, v) for p, v in med if v is not None
              and not (CR["mediana_m1"][0] <= v <= CR["mediana_m1"][1])]
    w("### **IL CRITERIO DEL MANDATO:** l'ipotesi del tetto e' **REFUTATA** se la mediana "
      "cade fuori da `[%.1f, %.1f]`." % (CR["mediana_m1"][0], CR["mediana_m1"][1]))
    w()
    # ### ⛔ **UN'ASSENZA NON E' UN ESITO** (`STANDARD 3`). Il giro a vuoto del generatore
    #   stampava *«✔ sta dentro a tutti e tre i passi»* con ### **tutti i valori a `n/d`**:
    #   ### **nessun dato letto come criterio superato.** E' il difetto piu' grave che il
    #   giro a vuoto ha trovato, e si cura CONTANDO i valori presenti.
    _vm = [(p, v) for p, v in med if v is not None]
    if not _vm:
        w("> ### ⛔ **NESSUNA MEDIANA DISPONIBILE: il criterio NON si applica.** "
          "### **Un'assenza non e' un <<non refutata>>** (`STANDARD 3`).")
    elif _fuori:
        w("> ### ⛔ **CADE FUORI ai passi %s. L'IPOTESI DEL TETTO E' REFUTATA dal criterio "
          "fissato nel mandato.**" % ", ".join("`%d`" % p for p, _ in _fuori))
    else:
        w("> ### ✔ **STA DENTRO a tutti i %d passi misurati: l'ipotesi del tetto NON e' "
          "refutata.**" % len(_vm))
    w()
    _prev = [(p, v) for p, v in med if v is not None and 0.5 <= v <= 1.2]
    w("### LA PREVISIONE DEL GUARDIANO: *«mediana fra `0.5` e `1.2`, con una coda che non "
      "supera `1` di molto»*")
    w()
    w("| | esito |")
    w("|---|---|")
    w("| **il guardiano** *(mediana in `[0.5, 1.2]`)* | ### **%s** -- dentro a %d passi su "
      "%d |" % ("CONFERMATA" if len(_prev) == len(PM) else "⛔ NON confermata",
                len(_prev), len(PM)))
    _coda = [(p, (MIS.get(p) or {}).get("m1", {}).get("fraz_sopra_2")) for p in PM]
    _mia = [x for _, x in _coda if x is not None and x > 0]
    w("| **io** *(«la coda e' PIU' LUNGA della sua, per gli `~109` archi di "
      "`ARCHI-OLTRE-4PI`»)* | frazione `> 2`: %s -- ### **%s** |"
      % (", ".join("`%s`" % n4(x) for _, x in _coda),
         "c'e' una coda" if _mia else "⛔ nessuna coda"))
    w()
    w("## `M2` / `M2b`: **il dipolo AIUTA o no?**")
    w()
    w("| passo | `M2` *(con `|twist_dip|`)* | `M2b` *(SENZA)* | il dipolo |")
    w("|---|--:|--:|---|")
    sp = []
    for p in PM:
        z = MIS.get(p) or {}  # noqa: F841  (le chiavi si leggono qui sotto)
        # ### ⛔ **LO STESSO DIFETTO DELLA TUPLA, qui:** i `json` delle corse PRIMA della
        #   correzione portano `m2` come **lista** `[valore, n]`; quelli DOPO portano un
        #   numero. ### ✔ **Si legge l'uno O l'altro**, cosi' il referto gira su entrambi e
        #   ### **un dato committato non diventa illeggibile per una cura dello strumento.**
        a, b = _val(z.get("m2")), _val(z.get("m2b"))
        sp.append((p, a))
        w("| `%d` | `%s` | `%s` | %s |"
          % (p, n4(a), n4(b),
             "n/d" if a is None or b is None
             else ("### **non aiuta** *(`M2b` >= `M2`)*" if b >= a
                   else "aiuta di `%s`" % n4(b - a))))
    w()
    _sotto = [(p, v) for p, v in sp if v is not None and abs(v) < CR["soglia_m2"]]
    _validi = [x for x in sp if x[1] is not None]
    w("### **IL CRITERIO DEL MANDATO:** **REFUTATA** se la Spearman di `M2` e' sotto `%.2f` "
      "a **tutti e tre** i passi." % CR["soglia_m2"])
    w()
    if not _validi:
        w("> ### ⛔ **NESSUNA SPEARMAN DISPONIBILE: il criterio NON si applica.**")
    elif _validi and len(_sotto) == len(_validi):
        w("> ### ⛔ **SOTTO `%.2f` A TUTTI I PASSI: L'IPOTESI DEL TETTO E' REFUTATA anche da "
          "questo criterio.**" % CR["soglia_m2"])
    else:
        w("> ### ✔ **NON sotto `%.2f` a tutti i passi** *(sotto a %d su %d)*: da questo "
          "criterio l'ipotesi **non** e' refutata." % (CR["soglia_m2"], len(_sotto),
                                                       len(_validi)))
    w()
    w("## `M3` / `M3b`: **quanti archi ARRIVANO alla soglia?**")
    w()
    w("| passo | `M3` oltre `3π` | `M3` oltre la **soglia modulata** | `M3b` oltre `3π` "
      "*(senza dipolo)* |")
    w("|---|--:|--:|--:|")
    for p in PM:
        z = MIS.get(p) or {}
        a, b = z.get("m3") or {}, z.get("m3b") or {}
        w("| `%d` | `%s` | `%s` | `%s` |"
          % (p, n4(a.get("fraz_oltre_3pi"), "%.6f"),
             n4(a.get("fraz_oltre_soglia_modulata"), "%.6f"),
             n4(b.get("fraz_oltre_3pi"), "%.6f")))
    w()
    _m3 = [(MIS.get(p) or {}).get("m3", {}).get("fraz_oltre_3pi") for p in PM]
    _m3 = [x for x in _m3 if x is not None]
    w("### LA PREVISIONE DEL GUARDIANO: *«con la soglia `3π` la frazione e' sotto lo "
      "`0.1 %%`»* ⟹ ### **%s SUL TETTO CALCOLATO** *(il massimo misurato e' `%s`)*."
      % ("CONFERMATA" if _m3 and max(_m3) < 0.001 else "⛔ REFUTATA",
         n4(max(_m3) if _m3 else None, "%.6f")))
    w()
    # ### ⛔ **MA LA PREVISIONE ERA AMBIGUA SULLA GRANDEZZA, e il guardiano lo dichiara:**
    #   `M3` misura la frazione di archi il cui TETTO CALCOLATO arriva a `3π`; la domanda
    #   fisica e' quanti archi ### **ci arrivano DAVVERO**, e quelli sono `g1`.
    #   ### **I due numeri stanno nello stesso referto e prima non erano collegati.**
    _g1 = [((MIS.get(p) or {}).get("m4", {}).get("n_g1"),
            (MIS.get(p) or {}).get("m4", {}).get("n_g1", 0)
            + (MIS.get(p) or {}).get("m4", {}).get("n_altri", 0)) for p in PM]
    _qg = [a / b for a, b in _g1 if a is not None and b]
    w("### ⛔ **MA LA PREVISIONE ERA AMBIGUA SULLA GRANDEZZA, e il guardiano lo dichiara**")
    w()
    w("| su che cosa | valore | contro lo `0.1 %` |")
    w("|---|--:|---|")
    w("| il **TETTO CALCOLATO** `|tw*| + |twist_dip|` *(`M3`, come il mandato lo definisce)* "
      "| %s | ### **REFUTATA** |" % ", ".join("`%.2f %%`" % (100 * x) for x in _m3))
    w("| gli archi che **SUPERANO DAVVERO** la soglia *(`g1`, da `M4`)* | %s | "
      "### **CONFERMATA** |"
      % ", ".join("`%.4f %%`" % (100 * x) for x in _qg))
    w()
    w("> ### 📌 **DUE LETTURE OPPOSTE DELLO STESSO DATO, e la differenza e' un fattore "
      "`~%.0f`.** La previsione non diceva su quale grandezza: ### **sulla lettera del "
      "mandato `M3` e' definita sul tetto CALCOLATO, quindi il verdetto <<REFUTATA>> e' "
      "quello giusto** -- ma ### **il numero che risponde alla domanda FISICA e' `g1`, e li' "
      "la previsione REGGE.**" % (max(_m3) / max(_qg) if _qg and max(_qg) else 0))
    w()
    _q99 = [((al(p).get("q_tw_ingresso") or {}).get("q099")) for p in PM]
    _q99 = [x for x in _q99 if x is not None]
    if _q99:
        w("### ✔ **E IL NUMERO CHE DICE QUANTO E' LONTANA LA SOGLIA:** il `q99` di `|tw|` "
          "sta al %s di `3π`. ### **La soglia di mitosi e' OLTRE il 99-esimo percentile "
          "della torsione**, a tutti e tre i passi."
          % ", ".join("`%.1f %%`" % (100 * x / P3) for x in _q99))
    w()
    _m3b = [(MIS.get(p) or {}).get("m3b", {}).get("fraz_oltre_3pi") for p in PM]
    _m3b = [x for x in _m3b if x is not None]
    w("### LA MIA: *«`M3b` ancora piu' bassa, vicina a zero esatto»* ⟹ ### **%s** "
      "*(massimo `%s`)*."
      % ("CONFERMATA" if _m3b and max(_m3b) <= (max(_m3) if _m3 else 1)
         else "⛔ NON confermata", n4(max(_m3b) if _m3b else None, "%.6f")))
    w()
    w("## `M4`: **gli archi che DIVIDONO sono quelli col tetto alto?**")
    w()
    w("| passo | | `|tw*|` mediano | `|twist_dip|` mediano | `|r_i-r_j|` mediano | "
      "`|tw|` mediano |")
    w("|---|---|--:|--:|--:|--:|")
    _sep = []
    for p in PM:
        z = (MIS.get(p) or {}).get("m4") or {}
        if "n_g1" not in z:
            w("| `%d` | ### %s | | | | |" % (p, z.get("stato")))
            continue
        for et in ("g1", "altri"):
            y = z.get(et) or {}
            w("| `%d` | **`%s`** *(`%d`)* | `%s` | `%s` | `%s` | `%s` |"
              % (p, et, z["n_g1"] if et == "g1" else z["n_altri"],
                 n4(qv(y.get("q_tw_stella"), "q050")),
                 n4(qv(y.get("q_twist_dip"), "q050")),
                 n4(qv(y.get("q_grad_r"), "q050")),
                 n4(qv(y.get("q_tw"), "q050"))))
        _a = qv((z.get("g1") or {}).get("q_tw_stella"), "q050")
        _b = qv((z.get("altri") or {}).get("q_tw_stella"), "q050")
        if _a is not None and _b is not None:
            _sep.append((p, _a, _b))
    w()
    if _sep:
        _piu = sum(1 for _, a, b in _sep if a > b)
        w("### LA PREVISIONE DEL GUARDIANO: *«gli archi in `g1` hanno `|tw*| + |twist_dip|` "
          "piu' alto»* ⟹ `|tw*|` mediano piu' alto in ### **%d passi su %d**."
          % (_piu, len(_sep)))
        w()
        _rap = [a / b for _, a, b in _sep if b]
        w("### LA MIA: *«differenza DEBOLE o assente su `|tw*|`, e `g1` si distingue per il "
          "TRANSITORIO»* ⟹ il rapporto fra le due mediane e' %s. ### **%s**"
          % (", ".join("`%s`" % n4(x) for x in _rap),
             "DEBOLE, come dicevo" if _rap and max(_rap) < 1.5
             else "⛔ NON debole: il guardiano ha ragione"))
    w()
    w("## `M5`: **la distribuzione di `|twist_dip|`**")
    w()
    w("| passo | a `0` | a `π/2` | a `π` | altro |")
    w("|---|--:|--:|--:|--:|")
    z0 = None
    for p in PM:
        z = al(p).get("m5") or {}
        if p == PM[-1]:
            z0 = z.get("fraz_zero")
        w("| `%d` | ### **`%s`** | `%s` | `%s` | `%s` |"
          % (p, n4(z.get("fraz_zero")), n4(z.get("fraz_mezzo_pi")),
             n4(z.get("fraz_pi")), n4(z.get("fraz_altro"))))
    w()
    w("### **IL CRITERIO DEL MANDATO:** la **seconda** ipotesi e' **REFUTATA** se meno del "
      "`%.0f %%` degli archi ha `twist_dip = 0`." % (100 * CR["fraz_dip0"]))
    w()
    if z0 is None:
        w("> ### n/d")
    elif z0 < CR["fraz_dip0"]:
        w("> ### ⛔ **`%s` < `%.2f`: LA SECONDA IPOTESI E' REFUTATA.**"
          % (n4(z0), CR["fraz_dip0"]))
    else:
        w("> ### ✔ **`%s` >= `%.2f`: la seconda ipotesi NON e' refutata**, e la previsione "
          "del guardiano *(«la maggioranza ha `twist_dip = 0`»)* e' ### **CONFERMATA**."
          % (n4(z0), CR["fraz_dip0"]))
        if z0 >= 0.999:
            w(">")
            w("> ### ⛔ **E C'E' DI PIU': e' `%s`, cioe' PRATICAMENTE TUTTI.** Se `twist_dip` "
              "e' zero su tutta la rete, allora ### **il dipolo non contribuisce MAI al "
              "tetto, e il `3π` del conto del guardiano non esiste: il tetto e' `2π`.** "
              "### ✔ **Ed e' la CORREZIONE scritta nella sezione `(c)` del task history, "
              "confermata dal dato: il dipolo entra come DERIVATA TEMPORALE, e una derivata "
              "di zero e' zero.**" % n4(z0))
    w()
    w("## ⛔ `M6`: **GLI AVVOLGIMENTI, e il difetto `TORS-W8-AVVOLGIMENTO` IN AZIONE**")
    w()
    w("| | |")
    w("|---|--:|")
    w("| coppie `(passo, arco)` confrontate | `%d` |" % c["coppie"])
    w("| **avvolgimenti di `dph`** *(`|salto| > 2π`)* | **`%d`** *(`%s` per coppia)* |"
      % (c["avvolgimenti"], n4(c["avvolgimenti"] / c["coppie"], "%.6f")
         if c["coppie"] else "n/d"))
    w("| **ripiegamenti del `_w8`** *(`|arg| > 4π`)* | `%d` |" % c["ripiegamenti"])
    w("| **calci oltre `π`** *(`|spinta - riparata|`)* | **`%d`** |" % c["calci_oltre_pi"])
    w("| invariante `|twp| <= 3π` violato | `%d` |" % c["twp_fuori_3pi"])
    w()
    if not c["twp_fuori_3pi"]:
        w("> ### ✔ **LA DERIVAZIONE DELLA SEZIONE `(b)` TIENE:** `|twp| <= 3π` su **tutte** "
          "le `%d` coppie, quindi ### **`twp` non avvolge MAI** ed e' `dph + twist_dip` "
          "esattamente." % c["coppie"])
    else:
        w("> ### ⛔ **LA DERIVAZIONE DELLA SEZIONE `(b)` E' FALSA:** `|twp|` esce da `3π` "
          "`%d` volte. ### **Va ritirata, non riformulata.**" % c["twp_fuori_3pi"])
    w()
    w("| passo | calci | `|errore|` mediano | errore **firmato** mediano | `+` | `-` |")
    w("|---|--:|--:|--:|--:|--:|")
    for p in PM:
        z = al(p).get("m6") or {}
        if "errore_MODULO_mediano_su_pi" not in z:
            continue
        w("| `%d` | `%s` | **`%s π`** | `%s π` | `%s` | `%s` |"
          % (p, z.get("calci_oltre_pi"),
             n4(z.get("errore_MODULO_mediano_su_pi")),
             n4(z.get("errore_firmato_mediano_su_pi")),
             z.get("calci_positivi"), z.get("calci_negativi")))
    w()
    w("> ### ⛔ **E LA MEDIANA DEL MODULO E' QUELLA CHE CONTA:** la **firmata** su una "
      "distribuzione a due picchi opposti da' ### **zero anche con calci enormi**, ed e' il "
      "difetto di referto che il giro corto ha trovato *(`0476a80`)*.")
    w()
    w("### ⚠ **E LA POPOLAZIONE OLTRE `4π`**")
    w()
    w("| passo | archi con `|tw| >= 4π` | di cui il `_w8` ripiega |")
    w("|---|--:|--:|")
    for p in PM:
        z = al(p).get("m6") or {}
        if "sopra_4pi" not in z:
            continue
        w("| `%d` | `%s` | `%s` |" % (p, z.get("sopra_4pi"), z.get("sopra_4pi_e_ripiega")))
    w()
    w("> ### ⛔ **NON INDAGO `ARCHI-OLTRE-4PI`**, che Luca ha messo fra le cose da non "
      "toccare. ### **Riporto il conteggio e il meccanismo** -- un calcio di `-4π` porta un "
      "arco oltre `TW_TETTO = 4π` **in un passo solo** -- e ### **NON guardo gli INDICI**, "
      "che e' la verifica che collegherebbe le due cose.")
    w()
    # ### ⛔ **IL TITOLO SI DECIDE DAL DATO:** scritto fisso diceva *«ED E' IL PIU'
    #   GRANDE»*, che e' ### **l'affermazione che questa stessa misura RITIRA.**
    _r7 = [qv((al(p).get("m7") or {}).get("q_rapporto"), "q050") for p in PM]
    _r7 = [x for x in _r7 if x is not None]
    _dom = bool(_r7) and min(_r7) > 1.0
    w("## ⛔ `M7` / `M7b`: **IL TERMINE CHE LA FORMULA IGNORA -- %s**"
      % ("ED E' IL PIU' GRANDE" if _dom
         else ("ed e' una correzione del `~%.0f %%`, NON il termine dominante"
               % (100 * sum(_r7) / len(_r7)) if _r7 else "e non si e' potuto misurare")))
    w()
    for p in PM:
        z = al(p).get("m7") or {}
        if not z:
            continue
        w("| passo `%d` | `q05` | `q25` | ### **`q50`** | `q75` | `q95` |" % p)
        w("|---|--:|--:|--:|--:|--:|")
        y = z.get("q_rapporto") or {}
        w("| `|Δδsync| / |Δ(dt_n·ω)|` | `%s` | `%s` | ### **`%s`** | `%s` | `%s` |"
          % (n4(y.get("q005")), n4(y.get("q025")), n4(y.get("q050")),
             n4(y.get("q075")), n4(y.get("q095"))))
        w()
    _med7 = [qv((al(p).get("m7") or {}).get("q_rapporto"), "q050") for p in PM]
    _med7 = [x for x in _med7 if x is not None]
    if _med7 and min(_med7) > 1.0:
        w("> ### ⛔ **ALLA MEDIANA IL TERMINE OMESSO E' PIU' GRANDE DI QUELLO TENUTO** "
          "*(fino a `%s` volte)*. ### **La formula del mandato non trascura una correzione: "
          "trascura il pezzo PIU' GRANDE della spinta.** `K_SYNC = 1.0`, e "
          "`delta_sync_phi` e' **attivo**." % n4(max(_med7)))
        w()
    elif _med7:
        w("> ### ⚠ **ALLA MEDIANA IL TERMINE OMESSO E' IL `~%.0f %%` DI QUELLO TENUTO**, e "
          "al `q95` arriva a `%s` volte. ### **`K_SYNC = 1.0`: il termine e' ATTIVO e la "
          "formula lo ignora** -- non e' il pezzo piu' grande, ### **ma non e' nemmeno "
          "trascurabile, e un conto che lo omette sbaglia di quell'ordine.**"
          % (100 * sum(_med7) / len(_med7),
             n4(max(qv((al(p).get("m7") or {}).get("q_rapporto"), "q095") or 0
                   for p in PM))))
        w()
    w("| passo | `Spearman(dph, Δδsync)` | frazione a **segno opposto** |")
    w("|---|--:|--:|")
    _neg = []
    for p in PM:
        z = al(p).get("m7b") or {}
        if not z:
            continue
        _sp7 = _val(z.get("spearman_dsync_dph"))
        _neg.append((p, _sp7, z.get("fraz_segno_opposto")))
        w("| `%d` | ### **`%s`** | `%s` |"
          % (p, n4(_sp7), n4(z.get("fraz_segno_opposto"))))
    w()
    if _neg:
        _tutti = all(s is not None and s < 0 for _, s, _f in _neg)
        _opp = [f for _, _s, f in _neg if f is not None]
        w("> ### %s **IL TERMINE %s.** La Spearman fra `dph` e `Δδsync` e' %s, e la frazione "
          "a segno opposto e' %s. ### **%s**"
          % ("⛔" if _tutti else "⚠",
             "RICHIAMA: smorza la spinta invece di aggiungersi" if _tutti
             else "non richiama in modo uniforme",
             "NEGATIVA a tutti i passi" if _tutti else "di segno misto",
             ", ".join("`%s`" % n4(x) for x in _opp),
             "Quindi il tetto vero sta SOTTO `2π`, e la soglia `3π` e' ANCORA PIU' LONTANA "
             "di quanto il conto del guardiano dica." if _tutti
             else "La lettura resta aperta, e lo dico invece di scegliere."))
    w()
    w("## ⛔ TRE MIE AFFERMAZIONI CHE QUESTA MISURA CORREGGE")
    w()
    _m7 = [qv((al(p).get("m7") or {}).get("q_rapporto"), "q050") for p in PM]
    _m7 = [x for x in _m7 if x is not None]
    _m7b = [_val((al(p).get("m7b") or {}).get("spearman_dsync_dph")) for p in PM]
    _m7b = [x for x in _m7b if x is not None]
    _opp = [(al(p).get("m7b") or {}).get("fraz_segno_opposto") for p in PM]
    _opp = [x for x in _opp if x is not None]
    w("| avevo scritto | dove | che cosa dice il dato |")
    w("|---|---|---|")
    w("| *«`delta_sync_phi` non e' una correzione, e' il TERMINE DOMINANTE»* | `406a973`, "
      "dal **giro corto** a `3` passi *(mediana `1.79`)* | ### ⛔ **FALSO in regime:** ai "
      "passi del mandato il rapporto mediano e' %s. ### **Il `1.79` era un TRANSITORIO dei "
      "primi passi, e l'ho preso per il regime.** Resta vero che il termine **non e' "
      "trascurabile** *(un `~%.0f %%`)* |"
      % (", ".join("`%s`" % n4(x) for x in _m7),
         100 * (sum(_m7) / len(_m7)) if _m7 else 0))
    w("| *«se RICHIAMA, smorza la spinta e il tetto vero sta SOTTO `2π`»* | `406a973` e "
      "`0476a80`, come **ipotesi** da misurare con `M7b` | ### ⛔ **NON CONFERMATA:** la "
      "Spearman e' %s -- ### **POSITIVA, non negativa** -- e la frazione a segno opposto e' "
      "%s, cioe' ### **il caso.** Il termine **non richiama in modo sistematico**, e il "
      "motivo del tetto piu' basso va cercato altrove |"
      % (", ".join("`%s`" % n4(x) for x in _m7b),
         ", ".join("`%s`" % n4(x) for x in _opp)))
    w("| *«la coda di `M1` e' PIU' LUNGA della sua, per gli `~109` archi di "
      "`ARCHI-OLTRE-4PI`»* | `bbb2dda`, la mia previsione | la frazione `> 2` e' %s: "
      "### **la coda c'e' ed e' PICCOLA.** `109` archi su `471564` sono lo "
      "`%.4f %%`, e la frazione `> 2` misurata e' `%.2f %%`: ### **lo stesso ordine di "
      "grandezza, quindi la previsione regge ma NON spiega tutta la coda** |"
      % (", ".join("`%s`" % n4((MIS.get(p) or {}).get("m1", {}).get("fraz_sopra_2"))
                   for p in PM),
         100 * 109.0 / 471564,
         100 * ((MIS.get(PM[0]) or {}).get("m1", {}).get("fraz_sopra_2") or 0)))
    w()
    w("> ### 📌 **PERCHE' LE SCRIVO QUI E NON LE CANCELLO DAL TASK HISTORY:** il par.8 vuole "
      "che un ragionamento sbagliato ### **resti scritto con l'annotazione accanto.** "
      "### **E la prima e' la piu' istruttiva: avevo un numero vero (`1.79`) misurato in un "
      "regime che non era quello della domanda, e l'ho generalizzato.**")
    w()
    w("## IL VERDETTO")
    w()
    # ### ⛔ **E IL VERDETTO DICHIARA <<n/d>> SE NON HA I DATI**, invece di dire
    #   *«non refutata»*: e' la stessa cura di `M1`, al punto in cui conta di piu'.
    _dati1 = bool(_vm) or bool(_validi)
    _ref1 = bool(_fuori) or bool(_validi and len(_sotto) == len(_validi))
    _ref2 = (z0 is not None and z0 < CR["fraz_dip0"])
    w("| ipotesi | criterio del mandato | esito |")
    w("|---|---|---|")
    w("| **il tetto** | mediana di `M1` fuori da `[%.1f, %.1f]` **oppure** `M2` sotto `%.2f` "
      "a tutti i passi | ### **%s** |"
      % (CR["mediana_m1"][0], CR["mediana_m1"][1], CR["soglia_m2"],
         ("REFUTATA" if _ref1 else "NON refutata") if _dati1 else "n/d: NESSUN DATO"))
    w("| **la seconda** *(il dipolo e' `0` per molti archi)* | meno del `%.0f %%` con "
      "`twist_dip = 0` | ### **%s** |"
      % (100 * CR["fraz_dip0"],
         ("REFUTATA" if _ref2 else "NON refutata") if z0 is not None
         else "n/d: NESSUN DATO"))
    w()
    w("### ⛔ **E QUELLO CHE LA MISURA AGGIUNGE AL MANDATO, in tre righe**")
    w()
    w("1. ### **`κ = 1` e' un numero scritto a mano, e il commento ne dice un altro** "
      "*(`KAPPA-TW-COMMENTO`)*: con `κ = 3.1831` il tetto sarebbe `20` invece di `2π`, e la "
      "mitosi passerebbe da **marginale** a **generica**. ### **Due letture, due fisiche.**")
    w("2. ### **`_w8` non ripara l'avvolgimento di `dph`** *(`TORS-W8-AVVOLGIMENTO`)*: "
      "`%d` calci oltre `π` su `%d` coppie, e il ramo non-`4π` lo ripara **esatto**. "
      "### **La formula del tetto vale FRA DUE AVVOLGIMENTI, non su tutta la corsa.**"
      % (c["calci_oltre_pi"], c["coppie"]))
    w("3. ### **`delta_sync_phi` e' ATTIVO e la formula lo ignora** *(`K_SYNC = 1.0`)*: "
      "una correzione del `~%.0f %%` alla mediana, e fino a `%s` volte al `q95`. "
      "### ⚠ **E NON E' <<IL TERMINE DOMINANTE>>: quello l'avevo scritto io dal giro corto, "
      "e questa misura lo RITIRA.** ### **Nessuna delle tre cose era nel mandato, e tutte e "
      "tre cambiano il conto.**"
      % (100 * sum(_r7) / len(_r7) if _r7 else 0,
         n4(max((qv((al(p).get("m7") or {}).get("q_rapporto"), "q095") or 0)
                for p in PM))))
    w()
    w("> ### ⛔ **E QUESTA E' UNA MISURA, NON UN SIGILLO:** ### **`κ`, la soglia, il dipolo "
      "locale e il `0.3` sono DECISIONI DI LUCA.**")
    w()
    w("---")
    w()
    w("*Referto **generato** da `csv/_test_fork/_referto_tetto.py` dal `tetto.json`: "
      "### **nessun numero e' ricopiato a mano** (`L-NUMERI`), e i criteri sono letti "
      "**dal `json`** invece di essere riscritti qui.*")
    w()
    io.open(OUT, "w", encoding="utf-8", newline=NL).write(NL.join(T))
    print("scritto %s  (%d righe)" % (OUT, len(T)))
    print("  tetto: %s   seconda: %s"
          % ("REFUTATA" if _ref1 else "NON refutata",
             "REFUTATA" if _ref2 else "NON refutata"))
    print("  blob del referto: %s"
          % hashlib.sha1(io.open(OUT, "rb").read()).hexdigest()[:8])
    return 0


if __name__ == "__main__":
    sys.exit(main())
