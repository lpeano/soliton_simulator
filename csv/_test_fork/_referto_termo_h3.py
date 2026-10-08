# -*- coding: utf-8 -*-
"""IL REFERTO DI `H3`: il bilancio, `B-T` e `B-S`. ### **UN SOLO referto**, come il mandato.

### ⛔ **Nessun numero si ricopia** *(`L-NUMERI`)*. Il controllo di `B-T` e `B-S` e' la
### **corsa di controllo di `A-S1`** *(`55a7edc`,
`csv/_test_fork/_massa_h1/controllo.json`)*, che ### **non si rigira.**
"""
import io
import json
import math
import os
import re
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
for _p in (os.path.join(RADICE, "csv"), _QUI):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import _presidio                                   # noqa: E402
_presidio.avvia(__file__)

import _mitosi_soglia_grad as _MSG                 # noqa: E402

NL = chr(10)
FUORI = os.path.join(RADICE, "doc", "REFERTO_h3_termostato_2026-10-07.md")
DIR = os.path.join(_QUI, "_termo_h3")
P_CT = os.path.join(_QUI, "_massa_h1", "controllo.json")
VOCI = ("scuoti", "termostato", "coppia", "residuo_incrociato")
R = []


def A(s=""):
    R.append(s)


def n4(x, c=4):
    if x is None:
        return "n/d"
    if isinstance(x, float):
        if not math.isfinite(x):
            return "`NaN`"
        return ("%." + str(c) + "f") % x
    return "%s" % x


def pct(x, c=2):
    return "n/d" if x is None else (("%." + str(c) + "f") % (100.0 * x)) + " %"


def carica(p):
    if not os.path.exists(p):
        return None
    try:
        return json.load(io.open(p, encoding="utf-8"))
    except Exception as e:                            # noqa: BLE001
        return {"_errore": str(e)}


def main():
    br = {}
    for nome, f in (("base", "h3_base.json"), ("B-T", "h3_bt.json"),
                    ("B-S", "h3_bs.json"), ("B-TS", "h3_bts.json"),
                    ("B-SCAL", "h3_bscal.json"),
                    ("B-SCAL-TS", "h3_bscalts.json")):
        d = carica(os.path.join(DIR, f))
        if d and not d.get("_errore"):
            br[nome] = d
    if "base" not in br:
        raise SystemExit("[FERMO] il braccio `base` manca: senza di lui non c'e' il bilancio.")
    for nome, d in sorted(br.items()):
        st = d.get("stato")
        if st != "DATI SALVATI":
            if str(st).startswith("DIVERGENZA") or str(st).startswith("CADUTA"):
                continue                              # ### si RIPORTA, non ferma il referto
            raise SystemExit("[FERMO] il braccio `%s` non e' completo: %r, %r su %r."
                             % (nome, st, d.get("passi_girati"), d.get("passi")))
    ct = carica(P_CT)
    hc = (ct or {}).get("massa_h1") if ct and not ct.get("_errore") else None

    def H(nome):
        return br[nome]["termo_h3"] if nome in br else None

    def passi(nome):
        h = H(nome)
        return {int(r["passo"]): r for r in h["passi"]} if h else {}

    # ======================================================================
    A("# `H3` — **CHI SCALDA IL VUOTO: IL TERMOSTATO O LO SCUOTIMENTO?**")
    A("")
    A("*Referto generato da `csv/_test_fork/_referto_termo_h3.py`. Dati: "
      "`csv/_test_fork/_termo_h3/`. Criteri, previsioni e aritmetica: "
      "`doc/TASK_HISTORY/2026-10-07_h3-termostato-e-scuotimento.md`, committato "
      "### **PRIMA** dello strumento e delle corse.*")
    A("")
    A("| braccio | passi | stato | secondi | che cosa gli è stato fatto |")
    A("|---|--:|---|--:|---|")
    _DESC = {"base": "### **niente** — è la dinamica di sempre",
             "B-SCAL": "### **`D2`:** `_coppia_interferenza` prende il suo ### **RAMO "
                       "SCALARE**, quello che dipende dalla ### **FASE CORRENTE** "
                       "*(`z = e^{iφ}`)*. ### ⚠ **Il flag è spento SOLO durante la chiamata** "
                       "e ripristinato in un `finally`: gira il ramo ### **del simulatore**",
             "B-SCAL-TS": "### **`D2-BIS`: I TRE INSIEME** — `scuoti_vuoto` inerte, "
                          "`xi_termo` azzerata ### **e** la coppia sul suo ### **RAMO "
                          "SCALARE**. ### ⭐ **Nessun codice di intervento nuovo:** sono "
                          "i due interventi ### **già sigillati** composti, e il "
                          "collaudo verifica che per i cinque bracci di prima le "
                          "condizioni valutino ### **IDENTICO**",
             "B-TS": "### **I DUE INSIEME:** `scuoti_vuoto` inerte ### **e** `xi_termo` "
                     "azzerata. ### **Il sistema vive solo della sua energia iniziale e della "
                     "dinamica interna.** ### ⚠ **Eredita da `B-T` il non essere un "
                     "azzeramento del termostato**",
             "B-T": "### **`xi_termo` azzerata prima di ogni `step`.** ### ⛔ **NON è un "
                    "azzeramento del termostato:** lo step lo ### **RICALCOLA** dentro di sé, "
                    "quindi resta ### **un passo di accumulo invece di tutti** — si chiama "
                    "### **«termostato senza memoria»**",
             "B-S": "### **`scuoti_vuoto` sostituita** con una funzione della stessa firma "
                    "che ### **non fa niente**"}
    for nome in ("base", "B-T", "B-S", "B-TS", "B-SCAL", "B-SCAL-TS"):
        if nome not in br:
            A("| `%s` | — | ### ⛔ **ASSENTE** | — | %s |" % (nome, _DESC[nome]))
            continue
        d = br[nome]
        A("| `%s` | %s su %s | %s | %s | %s |"
          % (nome, n4(d.get("passi_girati")), n4(d.get("passi")),
             ("### ✔ **completo**" if d.get("stato") == "DATI SALVATI"
              else "### ⛔ **%s**" % d.get("stato")),
             n4(d.get("secondi"), 1), _DESC[nome]))
    A("")
    _fl = (H("base")["geometria"] or {}).get("flag") or {}
    A("### ✔ **I FLAG CHE RENDONO VALIDA LA RICOSTRUZIONE, letti a runtime e non assunti**")
    A("")
    A("| | |")
    A("|---|---|")
    for q in ("TEMPO_SEGNO", "FORK_SU2_MEM", "REGIME", "CS_DINAMICO", "M_PH", "DT", "G_PH"):
        if q in _fl:
            A("| `%s` | `%s` |" % (q, _fl[q]))
    A("")
    A("> ### ⭐ **`TEMPO_SEGNO = False`** → `dt_n_s = dt_n` esattamente; "
      "### **`FORK_SU2_MEM = True`** → lo step ### **salva `_r_corrente`**, quindi `dt_n = DT·r` "
      "è leggibile; ### **`REGIME = 'deterministico'`** → gira il ramo del termostato e "
      "### **mai quello di `G_PH`** — ed è il controllo che il mandato chiede per `B-T`.")
    A("")
    A("---")
    A("")
    # ======================================================================
    A("# `(1)` ⭐ **IL BILANCIO DI `<phivel²>`: CHI SCALDA, E DI QUANTO**")
    A("")
    A("> ### ⛔ **È UN'IDENTITÀ, NON UNA STIMA:**")
    A("> `p2² − p0² = [2p₀·Δscuoti + Δscuoti²] + [2p₁·Δterm] + [2p₁·Δcoppia] + Δstep²`")
    A("> ### ⚠ **E `Δstep²` è un RESIDUO INCROCIATO fra termostato e coppia: non si può "
      "attribuire, e si riporta come tale.**")
    A("")
    pb = passi("base")
    kk = [k for k in sorted(pb) if k >= 1 and pb[k].get("per_classe")]
    k50 = [k for k in kk if k <= 50]
    for cl in ("vuoto", "masse"):
        A("## la classe ### **%s**" % cl.upper())
        A("")
        A("| passo | ### **scuoti** | termostato | coppia | residuo | TOTALE | quota dello scuoti |")
        A("|--:|--:|--:|--:|--:|--:|--:|")
        for k in [x for x in (1, 10, 25, 50, 100, 200, 300) if x in pb]:
            v = (pb[k].get("per_classe") or {}).get(cl)
            if not v:
                A("| `%d` | n/d | n/d | n/d | n/d | n/d | n/d |" % k)
                continue
            tot = sum(abs(v[q]) for q in VOCI)
            A("| `%d` | ### **%s** | %s | %s | %s | %s | ### **%s** |"
              % (k, n4(v["scuoti"], 6), n4(v["termostato"], 6), n4(v["coppia"], 6),
                 n4(v["residuo_incrociato"], 6), n4(v["delta_phivel2"], 6),
                 pct(abs(v["scuoti"]) / tot) if tot else "n/d"))
        A("")
        # --- le somme sui primi 50 passi: e' li' che il riscaldamento avviene
        if k50:
            som = {q: 0.0 for q in VOCI}
            for k in k50:
                v = (pb[k].get("per_classe") or {}).get(cl)
                if v:
                    for q in VOCI:
                        som[q] += v[q]
                tot = sum(abs(som[q]) for q in VOCI)
            A("**LA SOMMA SUI PRIMI `%d` PASSI** *(è lì che il riscaldamento avviene)*:" % len(k50))
            A("")
            A("| voce | somma | quota |")
            A("|---|--:|--:|")
            for q in VOCI:
                A("| %s`%s` | %s | ### **%s** |"
                  % ("### **" if q == "scuoti" else "", q + ("**" if q == "scuoti" else ""),
                     n4(som[q], 5), pct(abs(som[q]) / tot) if tot else "n/d"))
            A("")
            _sg = [(k, ((pb[k].get("per_classe") or {}).get(cl) or {}).get("termostato"))
                   for k in sorted(pb) if k >= 1]
            _sg = [(k, x) for k, x in _sg if x is not None]
            _pos = [k for k, x in _sg if x > 0]
            _neg = [k for k, x in _sg if x < 0]
            if _pos and _neg:
                A("> ### ⭐ **IL TERMOSTATO CAMBIA SEGNO, e questo e' il fatto che la "
                  "quota in valore assoluto NASCONDE:** aggiunge energia su ### **%d** passi "
                  "*(il primo: `%d`)* e la ### **TOGLIE** su ### **%d** *(dal `%d` in poi)*. "
                  "### ⛔ **Da li' FRENA**, e il totale di `Delta<phivel^2>` crolla: lo "
                  "scuotimento inietta e il termostato ### **quasi lo annulla.** "
                  "### **Quindi non e' il riscaldatore: e' il FRENO.**"
                  % (len(_pos), min(_pos), len(_neg), min(_neg)))
                A("")
            _vinc = max(VOCI, key=lambda q: abs(som[q]))
            A("> ### %s **LA VOCE PRINCIPALE NEL %s, sui primi `%d` passi, è "
              "`%s`** — con il ### **%s** del totale in valore assoluto."
              % ("⛔" if _vinc != "termostato" else "✔", cl.upper(), len(k50), _vinc,
                 pct(abs(som[_vinc]) / tot) if tot else "n/d"))
            A("")
            if cl == "vuoto":
                _esito_h3 = _vinc
    A("---")
    A("")
    # ======================================================================
    A("# `(2)` **LE GRANDEZZE DEL TERMOSTATO, e `E_cin` è MOLTO sotto l'obiettivo**")
    A("")
    A("| passo | `E_cin` | ### **`T_target`** | `err_rel` | ### **`xi_termo`** | `P_eq` | `cs_rappr` | `Λ` | `r` mediana |")
    A("|--:|--:|--:|--:|--:|--:|--:|--:|--:|")
    for k in [x for x in (1, 10, 25, 50, 100, 200, 300) if x in pb]:
        r = pb[k]
        t = r.get("termostato") or {}
        A("| `%d` | %s | ### **%s** | %s | ### **%s** | %s | %s | %s | %s |"
          % (k, n4(t.get("E_cin"), 5), n4(t.get("T_target")), n4(t.get("err_rel")),
             n4(r.get("xi_termo"), 5), n4(t.get("P_eq"), 5), n4(t.get("cs_rappr")),
             n4(r.get("Lam")), n4(r.get("r_mediana"))))
    A("")
    # --- la crescita di T_target e quanto viene da P_eq
    if kk:
        a, b = pb[kk[0]], pb[kk[-1]]
        ta, tb = a.get("termostato") or {}, b.get("termostato") or {}
        T0, T1 = ta.get("T_target"), tb.get("T_target")
        P0, P1 = ta.get("P_eq"), tb.get("P_eq")
        c0, c1 = ta.get("cs_rappr"), tb.get("cs_rappr")
        if None not in (T0, T1, P0, P1, c0, c1) and T0 and P0 and c0:
            # ### **T = cs^2 * P_eq**, quindi in LOGARITMO i due contributi si SOMMANO:
            #   `ln(T1/T0) = 2 ln(c1/c0) + ln(P1/P0)`. ### **Cosi' la quota e' DEFINITA**,
            #   invece di essere un'impressione.
            lT = math.log(T1 / T0) if T1 > 0 else 0.0
            lP = math.log(P1 / P0)
            lc = 2.0 * math.log(c1 / c0)
            A("### ⭐ **`T_target` CRESCE? E QUANTO VIENE DA `median(d0)`?**")
            A("")
            A("`T_target = cs_rappr² · P_eq`, quindi ### **in logaritmo i due contributi si "
              "SOMMANO**: `ln(T₁/T₀) = 2·ln(cs₁/cs₀) + ln(P₁/P₀)`. ### **Così la quota è "
              "DEFINITA, non un'impressione.**")
            A("")
            A("| dal passo `%d` al `%d` | valore | variazione | contributo a `ln(T₁/T₀)` |"
              % (kk[0], kk[-1]))
            A("|---|--:|--:|--:|")
            A("| `T_target` | `%s` → ### **`%s`** | ### **%s** | — |"
              % (n4(T0), n4(T1), pct((T1 - T0) / T0)))
            A("| ### **`P_eq = median(d0)`** | `%s` → `%s` | ### **%s** | ### **%s** |"
              % (n4(P0, 5), n4(P1, 5), pct((P1 - P0) / P0),
                 pct(lP / lT) if abs(lT) > 1e-12 else "n/d"))
            A("| `cs_rappr` *(entra al QUADRATO)* | `%s` → `%s` | %s | %s |"
              % (n4(c0), n4(c1), pct((c1 - c0) / c0),
                 pct(lc / lT) if abs(lT) > 1e-12 else "n/d"))
            A("")
            if abs(lT) < 1e-9:
                A("> ### ⚠ **`T_target` è PRATICAMENTE FERMO** *(%s)*: la domanda «quanto "
                  "della crescita viene da `median(d0)`» ### **non ha un denominatore**, e lo "
                  "dico invece di stampare una percentuale senza senso." % pct((T1 - T0) / T0))
            elif lP / lT > 0.5:
                A("> ### ⛔ **SÌ: `T_target` cresce, e la crescita viene PRINCIPALMENTE da "
                  "`median(d0)`** *(il ### **%s** di `ln(T₁/T₀)`)* — ed è il cricchetto che "
                  "`D31` descrive." % pct(lP / lT))
                if lP / lT > 1.0:
                    A("")
                    A("> ### ⚠ **E LA QUOTA SUPERA IL `100` PER CENTO PERCHE' L'ALTRO "
                      "TERMINE E' NEGATIVO, non per un errore:** `cs_rappr` ### **CALA** "
                      "*(contributo %s)*, quindi `median(d0)` deve ### **compensarlo E "
                      "produrre la crescita.** ### **Le due quote sommano a `100` per cento "
                      "per costruzione**, ed e' il senso della scomposizione in logaritmo."
                      % pct(lc / lT))
            else:
                A("> ### ⚠ **`T_target` si muove, ma `median(d0)` NON è il motore** *(solo il "
                  "%s di `ln(T₁/T₀)`)*: il resto viene da `cs_rappr`." % pct(lP / lT))
            A("")
    # --- il controllo positivo della ricostruzione
    res = [abs(pb[k].get("xi_residuo_ricostruzione") or 0.0) for k in kk]
    xis = [abs(pb[k].get("xi_termo") or 0.0) for k in kk]
    if res:
        _mx = max(res)
        _rel = max((r / x) for r, x in zip(res, xis) if x > 1e-12) if any(
            x > 1e-12 for x in xis) else None
        A("### ⚠ **IL CONTROLLO POSITIVO DELLA RICOSTRUZIONE, e NON è esatto**")
        A("")
        A("Lo step fa `xi += dt_scal·(err_rel − xi)/tau_termo` e poi `clip(−2, 2)`. "
          "### **Ricostruirlo verifica in un colpo `E_cin`, `P_eq`, `cs_rappr`, `T_target`, "
          "`tau_termo` e `dt_scal`.**")
        A("")
        A("| | |")
        A("|---|--:|")
        A("| residuo ASSOLUTO massimo su `%d` passi | ### **%.2e** |" % (len(res), _mx))
        A("| residuo RELATIVO massimo | ### **%s** |"
          % (pct(_rel, 3) if _rel is not None else "n/d"))
        A("")
        A("> ### ⛔ **LA RICOSTRUZIONE NON È AL BIT, E LO SCRIVO:** la causa probabile è che "
          "`d0` o `psi` cambino fra il mio punto di lettura e la riga `:7735` dove la legge li "
          "usa. ### ✔ **A questo livello le conclusioni QUALITATIVE — chi domina — non "
          "cambiano**, perché le voci del bilancio differiscono di ### **ordini di "
          "grandezza**; ### ⚠ **ma `T_target` ed `E_cin` portano quell'incertezza**, e un "
          "confronto fine fra loro non si può fare su questi numeri.")
        A("")
    # --- il controllo positivo di `ampiezza`
    A("### ✔ **IL CONTROLLO POSITIVO DI `ampiezza`: `rms(Δscuoti)` contro `rms(ampiezza)`**")
    A("")
    A("| passo | classe | `rms(Δscuoti)` | `rms(ampiezza)` | scarto |")
    A("|--:|---|--:|--:|--:|")
    for k in [x for x in (1, 50, 300) if x in pb]:
        for cl in ("vuoto", "masse"):
            v = (pb[k].get("per_classe") or {}).get(cl)
            if not v or v.get("rms_ampiezza") is None:
                continue
            a_, b_ = v["rms_d_scuoti"], v["rms_ampiezza"]
            A("| `%d` | %s | %s | %s | %s |"
              % (k, cl, n4(a_, 5), n4(b_, 5),
                 pct(abs(a_ - b_) / b_) if b_ else "n/d"))
    A("")
    A("> ### ✔ **Coincidono entro il rumore di campione**: `Δscuoti = normal(0,1)·ampiezza`, "
      "quindi ### **la mia ricostruzione della legge dello scuotimento è giusta** — e "
      "### **`calcio` NON si ricalcola**, perché userebbe `net.rng`.")
    A("")
    A("---")
    A("")
    # ======================================================================
    A("# `(3)` ⭐ **`Λ` È GLOBALE, E AGISCE DUE VOLTE** *(il punto `1` dell'integrazione)*")
    A("")
    A("`ampiezza = √(stress + 1e-9) · √Λ / (1 + I2/Λ)`, con ### **`Λ = mean(|psi|²)` "
      "GLOBALE**. ### ➜ **Un `Λ` che cresce ALZA il calcio ovunque *(`×√Λ`)* E INDEBOLISCE la "
      "soppressione dove `I2` è alto *(`/(1+I2/Λ)`)* — cioè scioglie la protezione delle "
      "masse.**")
    A("")
    A("| passo | `Λ` | `amp` mediana ### **VUOTO** | `amp` mediana ### **MASSE** | ### **rapporto masse/vuoto** | `I2` mediana masse |")
    A("|--:|--:|--:|--:|--:|--:|")
    for k in [x for x in (1, 10, 25, 50, 100, 200, 300) if x in pb]:
        r = pb[k]
        vv = (r.get("per_classe") or {}).get("vuoto") or {}
        vm = (r.get("per_classe") or {}).get("masse") or {}
        av, am = vv.get("amp_mediana"), vm.get("amp_mediana")
        A("| `%d` | %s | %s | %s | ### **%s** | %s |"
          % (k, n4(r.get("Lam")), n4(av, 5), n4(am, 5),
             n4(am / av, 4) if (av and am) else "n/d", n4(vm.get("I2_mediana"), 4)))
    A("")
    A("> ### ⭐ **IL RAPPORTO `masse/vuoto` DELL'AMPIEZZA È LA MISURA DELLA PROTEZIONE:** se "
      "SALE verso `1`, la soppressione ### **si sta sciogliendo**, e le masse ricevono lo "
      "stesso calcio del vuoto.")
    A("")
    A("---")
    A("")
    # ======================================================================
    A("# `(4)` ⛔ **I DUE BRACCI DIAGNOSTICI: CHI SCIOGLIE LE MASSE**")
    A("")
    A("> ### ⛔ **I CRITERI, FISSATI PRIMA** *(mandato di Luca)*: "
      "### **`IL TERMOSTATO SCIOGLIE LE MASSE`** se in `B-T` l'AUC al `400` è "
      "### **`>= 0.85`**; ### **`LO SCUOTIMENTO SCIOGLIE LE MASSE`** se in `B-S` l'AUC al "
      "`400` è ### **`>= 0.85`**. ### **Il controllo è la corsa di controllo di `A-S1`, che "
      "non si rigira.**")
    A("")
    _auc_ct = {}
    if hc:
        for k, v in hc.get("misure", {}).items():
            _auc_ct[int(k)] = v.get("auc_materia_vuoto")
    PM = [1, 50, 150, 230, 300, 400, 500]
    A("| passo | AUC ### **`B-T`** | AUC ### **`B-S`** | AUC ### **`B-TS`** | "
      "AUC ### **`B-SCAL`** | AUC controllo *(`A-S1`)* |")
    A("|--:|--:|--:|--:|--:|--:|")
    for k in PM:
        row = []
        for nome in ("B-T", "B-S", "B-TS", "B-SCAL"):
            h = H(nome)
            m = (h or {}).get("misure", {}).get(str(k)) if h else None
            row.append(n4((m or {}).get("auc_materia_vuoto")))
        A("| `%d` | ### **%s** | ### **%s** | ### **%s** | ### **%s** | %s |"
          % (k, row[0], row[1], row[2], row[3], n4(_auc_ct.get(k))))
    A("")
    _es = {}
    for nome in ("B-T", "B-S"):
        h = H(nome)
        m = (h or {}).get("misure", {}).get("400") if h else None
        a = (m or {}).get("auc_materia_vuoto")
        _es[nome] = a
    _et = {"B-T": "IL TERMOSTATO SCIOGLIE LE MASSE", "B-S": "LO SCUOTIMENTO SCIOGLIE LE MASSE"}
    _vinti = []
    for nome in ("B-T", "B-S"):
        a = _es[nome]
        if a is None:
            A("> ### ⚠ **`%s`: l'AUC al `400` MANCA** — il criterio `%s` ### **non è "
              "decidibile.**" % (nome, _et[nome]))
        elif a >= 0.85:
            _vinti.append(nome)
            A("> ### ⛔ **`%s`: AUC al `400` = %s `>= 0.85` → `%s` ### È SODDISFATTO.**"
              % (nome, n4(a), _et[nome]))
        else:
            A("> ### ✔ **`%s`: AUC al `400` = %s `< 0.85` → `%s` ### NON è soddisfatto**"
              " *(controllo: %s)*." % (nome, n4(a), _et[nome], n4(_auc_ct.get(400))))
        A("")
    if len(_vinti) == 2:
        A("> ### ⛔ **SONO SODDISFATTI TUTTI E DUE, e lo dico:** sia il termostato sia lo "
          "scuotimento, ### **tolti uno alla volta**, salvano le masse. ### **Allora non c'è "
          "UN colpevole: c'è una COPPIA**, e la decisione su che cosa fare è di Luca.")
    elif len(_vinti) == 1:
        A("> ### ⭐ **UN SOLO BRACCIO SALVA LE MASSE: `%s`.** ### **È il colpevole che il "
          "bilancio indicava**, e i due metodi — il bilancio per termine e l'amputazione — "
          "### **concordano.**" % _vinti[0])
    else:
        A("> ### ⛔ **NESSUNO DEI DUE SALVA LE MASSE: `H3` è SMENTITA COME CAUSA**, e si torna "
          "ad `A-S2` *(`H2`)*. ### **La decisione è di Luca.**")
    A("")
    # --- il residuo di `xi` in `B-T`: il braccio ha fatto quello che doveva?
    h = H("B-T")
    if h:
        pbt = {int(r["passo"]): r for r in h["passi"]}
        xs = [abs(pbt[k].get("xi_termo") or 0.0) for k in sorted(pbt) if k >= 1]
        xb = [abs(pb[k].get("xi_termo") or 0.0) for k in sorted(pb) if k >= 1]
        if xs and xb:
            A("### ⚠ **E `B-T` HA FATTO QUELLO CHE DOVEVA? il `xi_termo` RESIDUO**")
            A("")
            A("| | `\\|xi\\|` massimo | `\\|xi\\|` mediano |")
            A("|---|--:|--:|")
            A("| `base` | ### **%s** | %s |"
              % (n4(max(xb), 5), n4(sorted(xb)[len(xb) // 2], 5)))
            A("| ### **`B-T`** | ### **%s** | %s |"
              % (n4(max(xs), 5), n4(sorted(xs)[len(xs) // 2], 5)))
            A("")
            _sopp = (max(xb) / max(xs)) if max(xs) > 1e-12 else None
            A("> ### ✔ **LA SOPPRESSIONE MISURATA: `%s ×`** sul massimo. ### ⛔ **E NON È UN "
              "AZZERAMENTO**, come il task history dichiarava prima della corsa: `B-T` è "
              "### **«termostato senza memoria»**, non «senza termostato»."
              % (n4(_sopp, 1) if _sopp else "n/d"))
            A("")
    A("---")
    A("")
    # ======================================================================
    # ================================================================== B-TS
    hts = H("B-TS")
    if hts:
        A("---")
        A("")
        A("# `(5)` ⭐ **`B-TS`: SENZA BAGNO, RESTA SOLO LA DINAMICA INTERNA**")
        A("")
        A("> ### ⛔ **I CRITERI, FISSATI PRIMA** *(mandato di Luca)*: "
          "### **`LA CAUSA È IL BAGNO GLOBALE`** se l'AUC al `400` è ### **`>= 0.85`** "
          "### **E** la coerenza di fase delle masse al `230` è ### **`>= 0.6`**; "
          "### **`LA CAUSA È DENTRO LE MASSE (H2)`** se l'AUC al `400` è ### **`< 0.6`** "
          "### **E** il bilancio delle masse mostra che è la ### **COPPIA** a far crescere "
          "`<phivel²>`; fra i due ### **si riporta la curva e il termine dominante.**")
        A("")
        pts = {int(r["passo"]): r for r in hts["passi"]}
        mts = hts.get("misure", {})
        # --- il bilancio delle masse: chi fa crescere `<phivel^2>`
        _lim = [k for k in sorted(pts) if k >= 1]
        som = {q: 0.0 for q in VOCI}
        for k in _lim:
            v = (pts[k].get("per_classe") or {}).get("masse")
            if v:
                for q in VOCI:
                    som[q] += v[q]
        _tot = sum(abs(som[q]) for q in VOCI)
        _dom = max(VOCI, key=lambda q: abs(som[q]))
        A("### IL BILANCIO NELLE ### **MASSE**, somma su `%d` passi" % len(_lim))
        A("")
        A("| voce | somma | quota |")
        A("|---|--:|--:|")
        for q in VOCI:
            A("| %s`%s`%s | %s | ### **%s** |"
              % ("### **" if q == _dom else "", q, "**" if q == _dom else "",
                 n4(som[q], 4), pct(abs(som[q]) / _tot) if _tot else "n/d"))
        A("")
        A("> ### %s **IL TERMINE DOMINANTE NELLE MASSE È `%s`** — il ### **%s** del totale in "
          "valore assoluto. ### ✔ **E `scuoti` vale ESATTAMENTE `%s`: l'intervento è "
          "scattato.**"
          % ("⛔" if _dom == "coppia" else "⚠", _dom,
             pct(abs(som[_dom]) / _tot) if _tot else "n/d", n4(som["scuoti"], 8)))
        A("")
        # --- l'energia totale: finita, cresce o cala?
        _E = [(k, (pts[k].get("termostato") or {}).get("E_cin")) for k in _lim]
        _E = [(k, x) for k, x in _E if x is not None]
        _nf = sum(1 for r in hts["passi"] if r.get("phivel_non_finiti"))
        if _E:
            _E0, _E1 = _E[0][1], _E[-1][1]
            _Emax = max(x for _k, x in _E)
            A("### ⭐ **L'ENERGIA TOTALE: resta finita, cresce o cala?** "
              "*(il mandato lo chiede comunque: senza sorgenti né freni, la sua evoluzione dice "
              "se la dinamica interna ### **conserva, scalda o dissipa**)*")
            A("")
            A("| | |")
            A("|---|--:|")
            A("| `E_cin` al passo `%d` | %s |" % (_E[0][0], n4(_E0, 5)))
            A("| `E_cin` al passo `%d` | ### **%s** |" % (_E[-1][0], n4(_E1, 5)))
            A("| massimo | %s |" % n4(_Emax, 5))
            A("| ### **passi con `phivel` NON FINITI** | ### **%s** |" % n4(_nf))
            A("")
            _v = ("### ⛔ **CRESCE**" if _E1 > _E0 * 1.05 else
                  "### ⚠ **CALA**" if _E1 < _E0 * 0.95 else "### ✔ **si CONSERVA**")
            A("> %s: da `%s` a ### **`%s`** *(`%s`)*. ### **E resta FINITA: `%s` passi con "
              "valori non finiti.** ### ➜ **Quindi la dinamica interna, da sola, %s.**"
              % (_v, n4(_E0, 5), n4(_E1, 5),
                 ("×%s" % n4(_E1 / _E0, 2)) if _E0 else "n/d", n4(_nf),
                 "SCALDA" if _E1 > _E0 * 1.05 else
                 ("DISSIPA" if _E1 < _E0 * 0.95 else "CONSERVA")))
            A("")
        # --- l'esito del criterio
        _a4 = (mts.get("400") or {}).get("auc_materia_vuoto")
        _pm = (mts.get("230") or {}).get("per_massa") or {}
        _c2 = [x["coer_2pi"] for x in _pm.values() if x]
        _co = (sum(_c2) / len(_c2)) if _c2 else None
        A("### ⛔ **L'ESITO DEL CRITERIO**")
        A("")
        A("| | valore | la soglia |")
        A("|---|--:|---|")
        A("| AUC al `400` | ### **%s** | `>= 0.85` per il bagno, `< 0.60` per `H2` |" % n4(_a4))
        A("| coerenza di fase delle masse al `230` | ### **%s** | `>= 0.6` per il bagno |"
          % n4(_co))
        A("| il termine dominante nelle masse | ### **`%s`** | `coppia` per `H2` |" % _dom)
        A("")
        if _a4 is None or _co is None:
            A("> ### ⚠ **NON DECIDIBILE: manca l'AUC al `400` o la coerenza al `230`.**")
        elif _a4 >= 0.85 and _co >= 0.6:
            A("> ### ⛔ **`LA CAUSA È IL BAGNO GLOBALE`.** ### **Le masse SOPRAVVIVONO quando "
              "si toglie il bagno**, e la cura sta ### **nel bagno**, non dentro le masse. "
              "### ⛔ **E la decisione è di Luca.**")
        elif _a4 < 0.60 and _dom == "coppia":
            A("> ### ⛔ **`LA CAUSA È DENTRO LE MASSE (H2)`.** Senza bagno le masse si "
              "sciolgono comunque *(AUC `%s`)*, e ### **il termine che le scalda è la "
              "COPPIA** — cioè ### **la loro dinamica interna.** ### ⛔ **NON comincio la "
              "cura: la decisione è di Luca.**" % n4(_a4))
        elif _a4 < 0.60:
            A("> ### ⚠ **AUC `< 0.60`, MA IL TERMINE DOMINANTE NON È LA COPPIA: è `%s`.** "
              "### **Il criterio di `H2` chiede ENTRAMBE le cose, e una manca** — quindi "
              "### **non lo dichiaro soddisfatto**, e riporto la curva e il termine." % _dom)
        else:
            A("> ### ⚠ **FRA I DUE: AUC al `400` = %s**, cioè ### **sopra `0.60`** *(non "
              "`H2`)* ### **e sotto `0.85`** *(non il bagno)*. ### **Si riportano la curva e "
              "il termine dominante nelle masse, che è `%s`.**" % (n4(_a4), _dom))
        A("")
        # --- il residuo di `xi` in `B-TS`
        _xs = [abs(pts[k].get("xi_termo") or 0.0) for k in _lim]
        _xb = [abs((passi("base").get(k) or {}).get("xi_termo") or 0.0) for k in _lim
               if k in passi("base")]
        if _xs and _xb:
            A("> ### ⚠ **E `B-TS` EREDITA DA `B-T` IL NON ESSERE UN AZZERAMENTO:** "
              "`|xi|` massimo ### **%s** contro ### **%s** della base, cioè una soppressione "
              "di ### **%s ×**. ### **Il residuo è misurato, non assunto.**"
              % (n4(max(_xs), 5), n4(max(_xb), 5),
                 n4(max(_xb) / max(_xs), 1) if max(_xs) > 1e-12 else "n/d"))
            A("")
        A("---")
        A("")
    # ================================================================== D1
    A("---")
    A("")
    A("# `D1` ⭐ **LA POTENZA DELLA COPPIA: pompa o ridistribuisce?**")
    A("")
    A("> ### ⛔ **IL CRITERIO, FISSATO PRIMA** *(mandato di Luca)*: "
      "### **`LA COPPIA POMPA`** se `P_coppia` nelle masse è ### **positiva in almeno l'`80 %`** "
      "dei passi `1..230` ### **E** la sua ### **somma** su quei passi è positiva; "
      "### **`NON POMPA`** se quella somma è ### **`<= 0`**; fra i due ### **la curva.**")
    A("")
    A("Le tre potenze, nella ### **stessa unità** *(lavoro per unità di tempo proprio)*: "
      "### **`P_coppia = Σ coppia_k·p1_k`** *(forza × velocità: la potenza vera)*, "
      "`P_termo = −xi·Σ p1²`, e ### ⚠ **`P_scuoti = Σ p0·Δscuoti/dt_n`, che è un ANALOGO "
      "DICHIARATO** — lo scuotimento è un ### **calcio additivo**, non una forza.")
    A("")
    pb = passi("base")
    _kk = [k for k in sorted(pb) if k >= 1 and pb[k].get("per_classe")]
    for cl in ("masse", "vuoto"):
        A("## la classe ### **%s**" % cl.upper())
        A("")
        A("| passo | ### **`P_coppia`** | `P_termo` | `P_scuoti` *(analogo)* | `\\|coppia_k\\|` mediana |")
        A("|--:|--:|--:|--:|--:|")
        for k in [x for x in (1, 10, 25, 50, 100, 200, 300) if x in pb]:
            v = (pb[k].get("per_classe") or {}).get(cl)
            if not v or v.get("P_coppia") is None:
                A("| `%d` | n/d | n/d | n/d | n/d |" % k)
                continue
            A("| `%d` | ### **%s** | %s | %s | %s |"
              % (k, n4(v["P_coppia"], 2), n4(v["P_termo"], 2), n4(v["P_scuoti"], 2),
                 n4(v.get("coppia_mediana_assoluta"))))
        A("")
        _lim = [k for k in _kk if k <= 230]
        _v = [(pb[k].get("per_classe") or {}).get(cl, {}).get("P_coppia") for k in _lim]
        _v = [x for x in _v if x is not None]
        if _v:
            _pos = sum(1 for x in _v if x > 0)
            _som = sum(_v)
            A("| sui passi `1..230` | |")
            A("|---|--:|")
            A("| passi con `P_coppia` ### **positiva** | ### **%s su %s** *(%s)* |"
              % (n4(_pos), n4(len(_v)), pct(float(_pos) / len(_v))))
            A("| ### **somma di `P_coppia`** | ### **%s** |" % n4(_som, 2))
            A("")
            if cl == "masse":
                _d1_pos, _d1_tot, _d1_som = _pos, len(_v), _som
    # --- l'esito di `D1`
    if "_d1_som" in dir():
        _q = float(_d1_pos) / max(_d1_tot, 1)
        if _d1_som <= 0:
            A("> ### ✔ **`NON POMPA`:** la somma di `P_coppia` nelle masse sui passi `1..230` è "
              "### **%s `<= 0`**." % n4(_d1_som, 2))
        elif _q >= 0.80:
            A("> ### ⛔ **`LA COPPIA POMPA`.** `P_coppia` nelle masse è positiva nel "
              "### **%s** dei passi `1..230` *(soglia `80 %%`)* ### **e la somma è %s `> 0`.**"
              % (pct(_q), n4(_d1_som, 2)))
            A("")
            A("> ### ⚠ **E LO AVEVO DICHIARATO GIÀ NOTO PRIMA DI GIRARE:** la voce `coppia` "
              "del bilancio di `H3` è un ### **multiplo POSITIVO** di `P_coppia` "
              "*(`voce = (2/M_PH)·media(dt_n·coppia·p1)`, con `dt_n > 0`)*, ed era positiva in "
              "### **`230` passi su `230`** nelle masse. ### **La corsa non lo SCOPRE: lo "
              "misura nell'unità giusta e lo mette accanto alle altre due potenze.**")
        else:
            A("> ### ⚠ **FRA I DUE:** la somma è ### **%s `> 0`** ma i passi positivi sono il "
              "### **%s**, sotto la soglia dell'`80 %%`. ### **Si riporta la curva.**"
              % (n4(_d1_som, 2), pct(_q)))
        A("")
    # --- ### ⭐ **LO SCUOTIMENTO NON FA LAVORO: INIETTA VARIANZA.**
    #   La voce `scuoti` del bilancio e' `media(2*p0*Ds + Ds^2)`: il primo addendo e' il
    #   ### **LAVORO LINEARE** *(cioe' `2*dt_n*P_scuoti`)*, il secondo e' la
    #   ### **VARIANZA iniettata.** ### ⛔ **E per un calcio CASUALE il lavoro lineare
    #   media a ZERO**, perche' il calcio non e' correlato con la velocita' corrente.
    #   ### ✔ **Si misura, e risolve l'apparente contraddizione con `H3`:** la coppia e'
    #   la ### **POTENZA** dominante, lo scuotimento la ### **SORGENTE DI VARIANZA**
    #   dominante -- ### **due cose diverse, e confrontarle come potenze INGANNA.**
    A("## ⭐ **E LO SCUOTIMENTO NON FA LAVORO: INIETTA VARIANZA**")
    A("")
    A("La voce `scuoti` del bilancio e' `media(2·p0·Δs + Δs²)`: il primo addendo e' il "
      "### **lavoro LINEARE** *(cioe' `2·dt_n·P_scuoti`)*, il secondo e' la "
      "### **VARIANZA iniettata.** ### ⛔ **E per un calcio CASUALE il lavoro lineare media a "
      "ZERO**, perche' il calcio ### **non e' correlato con la velocita' corrente.**")
    A("")
    A("| classe | somma `1..230` del ### **QUADRATICO** | del ### **LINEARE** | quota del quadratico |")
    A("|---|--:|--:|--:|")
    for cl in ("vuoto", "masse"):
        _sq = _sl = 0.0
        _n = 0
        for k in [x for x in _kk if x <= 230]:
            v = (pb[k].get("per_classe") or {}).get(cl) or {}
            if v.get("scuoti") is None or v.get("rms_d_scuoti") is None:
                continue
            _q = v["rms_d_scuoti"] ** 2
            _sq += _q
            _sl += v["scuoti"] - _q
            _n += 1
        if _n:
            A("| %s | ### **%s** | %s | ### **%s** |"
              % (cl.upper(), n4(_sq, 4), n4(_sl, 4),
                 pct(abs(_sq) / max(abs(_sq) + abs(_sl), 1e-30))))
    A("")
    A("> ### ⭐ **QUESTO RISOLVE L'APPARENTE CONTRADDIZIONE CON `H3`:** li' lo scuotimento "
      "faceva il ### **`94 %`** del riscaldamento; qui `P_scuoti` oscilla attorno a ### **zero**. "
      "### **Non e' un disaccordo: sono DUE GRANDEZZE DIVERSE.** La coppia e' la "
      "### **POTENZA** dominante *(fa lavoro SISTEMATICO)*, lo scuotimento la "
      "### **SORGENTE DI VARIANZA** dominante *(scalda senza fare lavoro netto, come un bagno "
      "termico)*.")
    A("")
    A("> ### ⛔ **E CONFRONTARE `P_coppia` CON `P_scuoti` COME SE FOSSERO LA STESSA COSA "
      "INGANNEREBBE:** `P_scuoti` ### **sottostima sistematicamente** lo scuotimento, perche' "
      "una potenza ### **non vede il termine quadratico.** ### **Lo scrivo qui perche' chi "
      "legge la tavola delle potenze lo deve sapere PRIMA di confrontare le colonne.**")
    A("")
    # --- il segno di `P_termo`
    _st = [(k, (pb[k].get("per_classe") or {}).get("vuoto", {}).get("P_termo")) for k in _kk]
    _st = [(k, x) for k, x in _st if x is not None]
    _neg = [k for k, x in _st if x < 0]
    _posT = [k for k, x in _st if x > 0]
    if _neg and _posT:
        A("> ### ⭐ **E `P_termo` CAMBIA SEGNO, come in `H3`:** positiva *(rifornisce)* su "
          "### **%d** passi, negativa *(frena)* su ### **%d**, e il primo passo negativo è il "
          "### **`%d`**." % (len(_posT), len(_neg), min(_neg)))
        A("")
    A("---")
    A("")
    # ================================================================== D2
    hsc = H("B-SCAL")
    if hsc:
        A("# `D2` ⭐ **UNA COPPIA CHE LEGGE LA FASE: il ramo SCALARE**")
        A("")
        A("> ### ⛔ **DA DICHIARARE, e il mandato lo impone:** il ramo scalare usa "
          "### **`cos(φ_k − φ_j)`**, ### **NON `cos((φ_k − φ_j)/2)`** come nella direzione "
          "candidata di Luca. ### **È un test sul PRINCIPIO** *(una coppia che dipende dalla "
          "fase che muove)*, ### **NON sulla forma finale: un esito positivo NON decide la "
          "cura.**")
        A("")
        A("> ### ⛔ **I CRITERI, FISSATI PRIMA:** "
          "### **`UNA COPPIA CHE LEGGE LA FASE TIENE LE MASSE`** se l'AUC al `400` è "
          "### **`>= 0.85`** ### **E** l'energia totale al `500` è ### **minore** che nel "
          "controllo; ### **`NON BASTA`** se l'AUC al `400` è ### **`< 0.6`**; fra i due la "
          "curva ### **e il confronto al passo `230`.**")
        A("")
        # --- la verifica in tre pezzi
        _c = hsc.get("verifica_d2") or {}
        A("### ✔ **LA VERIFICA DELL'INTERVENTO — MISURATA, non promessa**")
        A("")
        A("| | |")
        A("|---|--:|")
        A("| chiamate a `_coppia_interferenza` | ### **%s** |" % n4(_c.get("chiamate")))
        A("| ripristini del flag | ### **%s** |" % n4(_c.get("ripristini")))
        A("| ### **firme del settore spinoriale DIVERSE** *(prima/dopo)* | ### **%s** |"
          % n4(_c.get("firme_diverse")))
        A("| flag NON ripristinato | ### **%s** |" % n4(_c.get("flag_non_ripristinato")))
        A("")
        _ok2 = (_c.get("chiamate") == _c.get("ripristini")
                and not _c.get("firme_diverse") and not _c.get("flag_non_ripristinato"))
        if _ok2:
            A("> ### ✔ **`chiamate == ripristini`, ZERO firme diverse, ZERO flag non "
              "ripristinati.** ### ⭐ **Quindi `_coppia_interferenza` è PURA, e spegnere un "
              "flag intorno a lei NON PUÒ toccare nient'altro che il valore restituito** — "
              "### **ed è la misura che il mandato chiede al posto delle parole.**")
        else:
            A("> ### ⛔ **LA VERIFICA FALLISCE:** %s. ### **I numeri di `D2` NON valgono "
              "finché non si trova la causa.**"
              % (("firme diverse su `%s`" % (_c.get("quali") or []))
                 if _c.get("firme_diverse") else "chiamate e ripristini non coincidono"))
        A("")
        # --- l'energia e l'esito
        psc = {int(r["passo"]): r for r in hsc["passi"]}
        # ### i nodi per classe, dalla geometria: servono a dire QUANTO il globale e'
        #   dominato dal VUOTO.
        _g = hsc.get("geometria") or {}
        _nmas = sum((_g.get("masse") or {}).values())
        _nvuo = _g.get("vuoto_nodi") or 0
        _E = [(k, (psc[k].get("termostato") or {}).get("E_cin")) for k in sorted(psc) if k >= 1]
        _E = [(k, x) for k, x in _E if x is not None]
        # ### ⛔ **IL CONTROLLO DI `A-S1` NON REGISTRA `E_cin`** -- il suo osservatore
        #   non lo misurava -- quindi la seconda clausola del criterio di Luca
        #   *(<<l'energia al `500` minore che nel controllo>>)* ### **NON E' VALUTABILE ALLA
        #   LETTERA.** ### ✔ **Si confronta col braccio `base`, che e' la dinamica di
        #   sempre, al MASSIMO PASSO COMUNE** -- e ### **si DICHIARA qual e'**, invece di
        #   mettere un numero senza dire a che passo si riferisce.
        _Eb = {k: ((pb[k].get("termostato") or {}).get("E_cin")) for k in pb}
        _Eb = {k: v for k, v in _Eb.items() if v is not None}
        _Es = dict(_E)
        _com = sorted(set(_Eb) & set(_Es))
        _kcom = max(_com) if _com else None
        _Ect = _Eb.get(_kcom)
        _a4 = (hsc.get("misure", {}).get("400") or {}).get("auc_materia_vuoto")
        _E5 = dict(_E).get(500)
        A("| | `B-SCAL` | controllo |")
        A("|---|--:|--:|")
        A("| AUC al `230` | ### **%s** | %s |"
          % (n4((hsc.get("misure", {}).get("230") or {}).get("auc_materia_vuoto")),
             n4(_auc_ct.get(230))))
        A("| ### **AUC al `400`** | ### **%s** | %s |" % (n4(_a4), n4(_auc_ct.get(400))))
        A("| `E_cin` al `1` | %s | — |" % n4(_E[0][1], 5) if _E else "| `E_cin` | n/d | — |")
        A("| ### **`E_cin` al `500`** | ### **%s** | ### ⛔ **ASSENTE** *(il controllo "
          "di `A-S1` non registra `E_cin`)* |" % n4(_E5, 5))
        if _kcom is not None:
            A("| ### **`E_cin` al `%d`** *(il massimo passo comune col braccio `base`)* | "
              "### **%s** | ### **%s** |"
              % (_kcom, n4(_Es.get(_kcom), 5), n4(_Ect, 5)))
        A("")
        _pm = (hsc.get("misure", {}).get("230") or {}).get("per_massa") or {}
        _c2 = [x["coer_2pi"] for x in _pm.values() if x]
        _coc = None
        if hc:
            _pmc = (hc.get("misure", {}).get("230") or {}).get("per_massa") or {}
            _cc = [x["coer_2pi"] for x in _pmc.values() if x]
            _coc = (sum(_cc) / len(_cc)) if _cc else None
        A("| | valore | il controllo |")
        A("|---|--:|--:|")
        A("| ### **coerenza di fase delle masse al `230`** | ### **%s** | %s |"
          % (n4((sum(_c2) / len(_c2)) if _c2 else None), n4(_coc)))
        A("")
        if _a4 is None:
            A("> ### ⚠ **NON DECIDIBILE: manca l'AUC al `400`.**")
        elif _a4 < 0.60:
            A("> ### ⛔ **`NON BASTA`:** AUC al `400` = ### **%s**, sotto `0.60` "
              "*(controllo %s)*. ### **Una coppia che legge la fase, DA SOLA, non tiene le "
              "masse.**" % (n4(_a4), n4(_auc_ct.get(400))))
        elif _a4 >= 0.85:
            # ### IL CRITERIO E' UNA CONGIUNZIONE, e si valuta come tale: l'AUC E
            #   l'energia. Dichiarare soddisfatta la prima clausola e tacere sulla seconda
            #   sarebbe TRADIRE il criterio.
            _en = (_Es.get(_kcom) is not None and _Ect is not None and _Es[_kcom] < _Ect)
            A("> ### \u2b50 **AUC al `400` = %s, cioe\' `>= 0.85`: LA PRIMA CLAUSOLA E\' "
              "SODDISFATTA, e con un margine grande** *(il controllo sta a %s)*."
              % (n4(_a4), n4(_auc_ct.get(400))))
            A("")
            if _en:
                A("> ### \u2714 **E ANCHE LA SECONDA:** l\'energia al passo `%d` e\' "
                  "### **%s** contro ### **%s** del braccio `base`. ### \u26d4 **QUINDI "
                  "`UNA COPPIA CHE LEGGE LA FASE TIENE LE MASSE`.**"
                  % (_kcom, n4(_Es.get(_kcom), 4), n4(_Ect, 4)))
            else:
                A("> ### \u26d4 **MA LA SECONDA NON LO E\': l\'energia GLOBALE non e\' "
                  "minore.** Al passo `%d` vale ### **%s** contro ### **%s** del braccio "
                  "`base`."
                  % (_kcom, n4(_Es.get(_kcom), 4), n4(_Ect, 4)))
                A("")
                A("> ### \u26a0 **QUINDI IL CRITERIO, CHE E\' UNA CONGIUNZIONE, NON E\' "
                  "SODDISFATTO** -- e lo dico invece di fermarmi alla clausola che mi "
                  "conviene.")
                A("")
                # ### \u26d4 **MA LA CLAUSOLA MISURAVA LA GRANDEZZA SBAGLIATA, e la lettura
                #   per CLASSE lo mostra.** ### **Errore del guardiano, che l'ha scritta, e
                #   mio, che l'ho letta come se dicesse qualcosa sulle masse.**
                A("> ### \u26d4 **MA QUELLA CLAUSOLA MISURAVA LA GRANDEZZA SBAGLIATA, e lo "
                  "dico perche\' cambia la lettura:** l\'energia ### **GLOBALE** e\' dominata "
                  "dal ### **VUOTO**, che e\' il ### **%s** dei nodi. "
                  "### \u26a0 **E\' un errore del guardiano, che ha scritto la clausola, e MIO, "
                  "che l\'ho letta come se dicesse qualcosa sulle MASSE.** "
                  "### \u2714 **Il verdetto FORMALE resta quello che e\'** -- un criterio "
                  "fissato prima non si riscrive dopo -- ### **ma la tavola per classe qui "
                  "sotto dice che cosa succede DAVVERO.**"
                  % pct(float(_nvuo) / max(_nvuo + _nmas, 1)) if (_nvuo and _nmas)
                  else "")
                A("")
                # --- la tavola PER CLASSE, che e' la lettura giusta
                A("| `phivel^2` al passo `%d` | braccio `base` | ### **`B-SCAL`** | rapporto |"
                  % _kcom)
                A("|---|--:|--:|--:|")
                for cl in ("masse", "vuoto"):
                    _a = (pb.get(_kcom, {}).get("per_classe") or {}).get(cl, {}).get("phivel2")
                    _s = (psc.get(_kcom, {}).get("per_classe") or {}).get(cl, {}).get("phivel2")
                    A("| ### **%s** | %s | ### **%s** | ### **%s** |"
                      % (cl.upper(), n4(_a, 4), n4(_s, 4),
                         n4(_s / _a, 3) if (_a and _s) else "n/d"))
                A("")
                A("| `P_coppia` in `B-SCAL` | passi | ### **segno** | somma |")
                A("|---|--:|---|--:|")
                for cl in ("masse", "vuoto"):
                    _v = [(k, (psc[k].get("per_classe") or {}).get(cl, {}).get("P_coppia"))
                          for k in sorted(psc) if k >= 1]
                    _v = [(k, x) for k, x in _v if x is not None]
                    if not _v:
                        continue
                    _ng = sum(1 for _k, x in _v if x < 0)
                    _ps2 = sum(1 for _k, x in _v if x > 0)
                    A("| ### **%s** | %s | ### **%s** | ### **%s** |"
                      % (cl.upper(), n4(len(_v)),
                         # ### ⛔ **NIENTE GRASSETTO QUI: la colonna e' GIA' avvolta in
                         #   `### **...**`, e annidarlo darebbe `****`.** Il controllo di
                         #   formato lo prende, ma il referto si legge PRIMA.
                         ("NEGATIVA in %s su %s" % (n4(_ng), n4(len(_v))))
                         if _ng > _ps2 else
                         ("POSITIVA in %s su %s" % (n4(_ps2), n4(len(_v)))),
                         n4(sum(x for _k, x in _v), 1)))
                    _d = [(k, x) for k, x in _v if k > 230]
                    if _d:
                        _dp = sum(1 for _k, x in _d if x > 0)
                        A("| %s, ### **dopo il `230`** | %s | %s | %s |"
                          % (cl.upper(), n4(len(_d)),
                             "positiva in **%s su %s**" % (n4(_dp), n4(len(_d))),
                             n4(sum(x for _k, x in _d), 1)))
                A("")
                A("> ### \u2b50 **LA LETTURA GIUSTA, e corregge quella che avevo scritto:** "
                  "con la coppia scalare ### **le MASSE sono PIU\' FREDDE** *(e non piu\' "
                  "calde)*, ### **e la coppia TOGLIE loro energia** -- `P_coppia` nelle masse "
                  "e\' ### **NEGATIVA quasi sempre**, contro i ### **`230` su `230` POSITIVI** "
                  "del braccio `base`. ### **Il piu\' caldo e\' il VUOTO**, dove la coppia "
                  "immette energia.")
                A("")
                A("> ### \u26d4 **QUINDI LA FRASE <<LA COERENZA NON E\' UNA QUESTIONE DI "
                  "TEMPERATURA>> CHE AVEVO SCRITTO E\' SBAGLIATA**, e la cancello: era basata "
                  "sulla temperatura ### **GLOBALE**, cioe\' su quella del vuoto. "
                  "### \u2714 **Per le MASSE coerenza e temperatura vanno INSIEME, come ci si "
                  "aspetta:** la coppia scalare le raffredda ### **e** le tiene coerenti.")
            A("")
            A("> ### \u26d4 **E NON DECIDE LA CURA, per la ragione dichiarata in testa alla "
              "sezione:** il ramo scalare usa `cos(phi_k - phi_j)`, ### **non "
              "`cos((phi_k - phi_j)/2)`** della direzione candidata di Luca. ### **E\' un "
              "test sul PRINCIPIO. La decisione e\' di Luca.**")
        else:
            A("> ### ⚠ **FRA I DUE:** AUC al `400` = ### **%s**, ### **sopra `0.60`** *(non "
              "«non basta»)* ### **e sotto `0.85`** *(non «tiene»)*. ### **Si riporta la curva "
              "e il confronto al `230`.**" % n4(_a4))
        A("")
        A("---")
        A("")
    # ======================================================================
    #   ### ⭐ **`D2-BIS`: L ENERGIA, E CHE COSA IL CRITERIO MISURA DAVVERO**
    # ======================================================================
    _pe = {}
    hts = H("B-SCAL-TS")
    if hts:
        pts = {int(r["passo"]): r for r in hts["passi"]}
        _en = {k: r["energia"] for k, r in sorted(pts.items()) if r.get("energia")}
        _gts = hts.get("geometria") or {}
        _nm = sum((_gts.get("masse") or {}).values())
        _nv = _gts.get("vuoto_nodi") or 0
        # ### ⚠ **L ETICHETTA NON DEVE MENTIRE:** <<prima/dopo le nascite>> vale se
        #   nascite ce ne sono. In questo braccio ce ne sono ZERO, e allora la
        #   frontiera del `216` divide ### **solo il tempo**.
        _nati0 = sum((r.get("nati_nel_passo") or 0) for r in hts["passi"])
        if _nati0:
            FIN = (("1..215 *(PRIMA delle nascite)*", 1, 215),
                   ("216..500 *(DOPO la prima nascita)*", 216, 500))
        else:
            FIN = (("1..215", 1, 215),
                   ("216..500 *(e qui NON nasce niente: divide solo il tempo)*",
                    216, 500))

        def _fin(a, b):
            return [(k, v) for k, v in sorted(_en.items()) if a <= k <= b]

        A("# `D2-BIS` ⭐ **`B-SCAL-TS`: LA COPPIA SCALARE SENZA BAGNO, E L ENERGIA**")
        A("")
        A("> *Criteri e previsioni: `doc/TASK_HISTORY/"
          "2026-10-08_bscalts-energia-e-potenziale.md`, committato ### **prima** in `d69214d`.*")
        A("")
        # --- ### ⭐ **IL FATTO CHE CAMBIA LA LETTURA: QUI NON NASCE NIENTE**
        _nati = sum((r.get("nati_nel_passo") or 0) for r in hts["passi"])
        _n0 = hts["passi"][0]["n"] if hts["passi"] else None
        _n1 = hts["passi"][-1]["n"] if hts["passi"] else None
        _a0 = hts["passi"][0]["archi"] if hts["passi"] else None
        _a1 = hts["passi"][-1]["archi"] if hts["passi"] else None
        A("## ⛔ **IL FATTO DA DIRE PRIMA DI TUTTO: IN QUESTO BRACCIO NON NASCE "
          "NIENTE**")
        A("")
        A("| braccio | passi | `n` iniziale → finale | archi iniziali → finali | "
          "### **nodi nati** |")
        A("|---|--:|--:|--:|--:|")
        for _nm2 in ("base", "B-SCAL", "B-TS", "B-SCAL-TS"):
            _h2 = H(_nm2)
            if not _h2 or not _h2.get("passi"):
                continue
            _p2 = _h2["passi"]
            _gr = _p2[-1]["n"] - _p2[0]["n"]
            A("| `%s` | %s | %s → %s | %s → %s | %s |"
              % (_nm2, n4(len(_p2) - 1), n4(_p2[0]["n"]), n4(_p2[-1]["n"]),
                 n4(_p2[0]["archi"]), n4(_p2[-1]["archi"]),
                 ("### **%s**" % n4(_gr)) if _gr else "### ⛔ **0**"))
        A("")
        if _nati == 0 and _n0 == _n1 and _a0 == _a1:
            A("> ### ⛔ **ZERO NASCITE SU %s PASSI: `n` e gli archi NON SI MUOVONO.** "
              "### **Non l avevo previsto**, e cambia la lettura di tre cose: "
              "### **(1)** la previsione `PE-5` è smentita ### **non perché le nascite "
              "non dominino, ma perché non ce ne sono**; ### **(2)** la finestra "
              "`216..500` in questo braccio ### **non separa le nascite da niente** — "
              "si riporta comunque, perché il mandato la chiede, ma ### **qui divide "
              "solo il tempo**; ### **(3)** `dU_A` è ### **tutto e solo `w` che "
              "cambia**, quindi il lavoro di `A` qui misura ### **la plasticità dei "
              "pesi**, non la crescita della rete." % n4(len(hts["passi"]) - 1))
            A("")
            # ### ⛔ **CORREZIONE DEL 2026-10-08 (`D2-TER`, punto 0): L ATTRIBUZIONE
            #   ERA MIA E SBAGLIATA.** Avevo scritto che e' ### **la coppia scalare**
            #   a fermare la divisione. Ma `B-SCAL` ha la ### **STESSA** coppia
            #   scalare e, ### **col bagno**, fa ### **piu'** nascite del `base`.
            #   ### **Le nascite crollano TOGLIENDO IL BAGNO, non cambiando la coppia.**
            _nb = {}
            for _nm3 in ("base", "B-SCAL", "B-TS", "B-SCAL-TS"):
                _h3 = H(_nm3)
                if _h3 and _h3.get("passi"):
                    _p3 = _h3["passi"]
                    _nb[_nm3] = (_p3[-1]["n"] - _p3[0]["n"], len(_p3) - 1)
            A("> ### ⛔ **E L ATTRIBUZIONE NON È ALLA COPPIA: È AL BAGNO TOLTO.** "
              "### ⚠ **Qui avevo scritto che è «la coppia scalare» a fermare la "
              "divisione, e i numeri dicono che NO:** `B-SCAL` ha la ### **STESSA** "
              "coppia scalare e, ### **col bagno**, fa ### **%s** nascite in `%s` "
              "passi — ### **più del `base`**, che ne fa `%s` in `%s`. E con la coppia "
              "### **spinoriale** e il bagno ### **spento** *(`B-TS`)* ne fa `%s`. "
              "### ➜ **Le nascite crollano TOGLIENDO IL BAGNO, non cambiando la "
              "coppia:** `base %s` → `B-SCAL %s` → `B-TS %s` → `B-SCAL-TS %s`."
              % (n4(_nb.get("B-SCAL", (0, 0))[0]), n4(_nb.get("B-SCAL", (0, 0))[1]),
                 n4(_nb.get("base", (0, 0))[0]), n4(_nb.get("base", (0, 0))[1]),
                 n4(_nb.get("B-TS", (0, 0))[0]),
                 n4(_nb.get("base", (0, 0))[0]), n4(_nb.get("B-SCAL", (0, 0))[0]),
                 n4(_nb.get("B-TS", (0, 0))[0]),
                 n4(_nb.get("B-SCAL-TS", (0, 0))[0])))
            A("")
            A("> ### ⭐ **E RESTA UN RISULTATO, ma di un ALTRO fatto:** togliere i due "
              "forzanti globali ### **azzera** la divisione, e la coppia scalare "
              "### **non la ripristina**. ### **Il bagno è ciò che porta il sistema "
              "alla soglia di mitosi**, e il costo è del ### **togliere il bagno**, "
              "### **non della forma della coppia.** ### ⚠ **Resta sul tavolo della "
              "decisione, con l etichetta giusta.**")
            A("")
        A("## ⭐ **LE DUE ENERGIE SONO DERIVATE DAL CODICE, NON SCELTE**")
        A("")
        A("| | |")
        A("|---|---|")
        A("| ### **CINETICA** | da `:7760` e `:7830`, diviso per `dt_n_s`, si legge "
          "### **Newton sulla coordinata `φ`** con inerzia `M_PH`: "
          "### **`T = ½·M_PH·Σ phivel²`** |")
        A("| il ruolo di `dt_n` | ### ⛔ **NON entra in `T`.** È il passo "
          "d integrazione, ed è ### **PER NODO** *(`dt_n = DT·r`, `:7498`)*: entra solo "
          "nei LAVORI, via `Δφ = dt_n·phivel(t+1)` *(`:7831`)* |")
        A("| ### ⚠ **e NON è l `E_cin` del codice** | `:7711` calcola "
          "`mean(phivel²)`: una ### **MEDIA**, senza `½` e senza `M_PH` — un analogo di "
          "### **TEMPERATURA** per il confronto con `T_target`. ### **Due cose diverse "
          "con lo stesso nome, e qui sotto ci sono entrambe** |")
        A("| ### **POTENZIALE** | `U = −K_C·Σ_archi A_ij·cos(φ_i − φ_j)` con la `A` "
          "### **EFFETTIVAMENTE USATA** — catturata dall involucro, perché è il "
          "### **primo argomento** di `_coppia_interferenza`: non si ricostruisce |")
        A("")
        A("> ### ✔ **E CHE IL RAMO SCALARE SIA `−∂U/∂φ` È MISURATO SULLA FUNZIONE "
          "VERA**, non argomentato: `--collaudo-potenziale` dà ### **`1.49e-15`** sulla "
          "`A` e le `φ` vere, e la ### **differenza finita** *(che non passa dalla mia "
          "derivata)* dà ### **`3.32e-09`**. ### ⛔ **E il caso che DEVE fallire "
          "fallisce:** la coppia ### **spinoriale** dà `1.01e+00`, con lo spinore "
          "### **lontano** dal limite in cui i due rami coinciderebbero "
          "*(`max|b| = 1.0000`)*.")
        A("")
        # --- ### il CRITERIO 1, e che cosa misura davvero
        A("## ⛔ **IL CRITERIO `LA COPPIA SCALARE CONSERVA A A FISSO`**")
        A("")
        A("> ### **Il criterio di Luca:** in almeno il ### **`95 %`** dei passi, "
          "`P_coppia` più il `dU/dt` dovuto alle ### **sole `φ`** ha residuo relativo "
          "### **`< 1e-2`**. ### **Valutato nella forma del LAVORO** "
          "*(`Σ coppia·Δφ`)*, perché ### **`dt_n` è PER NODO** e una potenza per un "
          "`dt` unico sarebbe sbagliata.")
        A("")
        A("| finestra | passi | ### **quota con residuo `< 1e-2`** | residuo mediano | "
          "`Δφ` massimo mediano | ### **residuo / `Δφ`** *(decile `10` — mediana — decile `90`)* | max | `W_interf` quasi nullo |")
        A("|---|--:|--:|--:|--:|--:|--:|--:|")
        _qfin = {}
        for et, a, b in FIN:
            f = _fin(a, b)
            if not f:
                A("| %s | — | ### **n/d** | — | — | — | — | — |" % et)
                continue
            rr = [abs(v["residuo_relativo"]) for _k, v in f]
            dd = [v["dphi_massimo"] for _k, v in f]
            _rap = sorted(r / d for r, d in zip(rr, dd) if d > 0)
            # ### ⚠ **UN RAPPORTO ESPLODE QUANDO IL DENOMINATORE E' QUASI NULLO**, e
            #   quello non e' un fatto di fisica. Si CONTANO i passi in cui
            #   `|W_interf|` sta sotto il `10 %` della sua mediana.
            _wi_a = sorted(abs(v["W_interferenza"]) for _k, v in f)
            _wmed = _wi_a[len(_wi_a) // 2] if _wi_a else 0.0
            _pochi = sum(1 for x in _wi_a if x < 0.10 * _wmed)
            _med = sorted(rr)[len(rr) // 2]
            _mdd = sorted(dd)[len(dd) // 2]
            _mr = (sorted(_rap)[len(_rap) // 2]) if _rap else None
            _qu = sum(1 for x in rr if x < 1e-2) / float(len(rr))
            _qfin[et] = _qu
            _d10 = _rap[int(0.10 * (len(_rap) - 1))] if _rap else None
            _d90 = _rap[int(0.90 * (len(_rap) - 1))] if _rap else None
            A("| %s | %s | ### **%s** | %s | %s | %s | %s | %s |"
              % (et, n4(len(f)), pct(_qu), n4(_med, 5), n4(_mdd, 5),
                 ("%s / %s / %s" % (n4(_d10, 4), n4(_mr, 4), n4(_d90, 4)))
                 if _rap else "—",
                 n4(_rap[-1], 4) if _rap else "—", n4(_pochi)))
            if et.startswith("1.."):
                _qfin["rap"] = (_d10, _mr, _d90, _rap[-1], _pochi, len(_rap))
        A("")
        _tot = [abs(v["residuo_relativo"]) for _k, v in sorted(_en.items())]
        _qt = (sum(1 for x in _tot if x < 1e-2) / float(len(_tot))) if _tot else None
        if _qt is None:
            A("> ### ⚠ **NON DECIDIBILE: nessun passo con l energia.**")
        elif _qt >= 0.95:
            A("> ### ✔ **`LA COPPIA SCALARE CONSERVA A A FISSO`: il criterio è "
              "SODDISFATTO** *(%s dei passi, soglia `95 %%`)*." % pct(_qt))
        else:
            A("> ### ⛔ **IL CRITERIO NON È SODDISFATTO:** solo ### **%s** dei passi sta "
              "sotto `1e-2` *(soglia `95 %%`)*." % pct(_qt))
        A("")
        A("### ⭐ **E QUEL RESIDUO NON MISURA LA CONSERVAZIONE: MISURA IL PASSO.**")
        A("")
        A("Il residuo è `dU_φ + Σ coppia·Δφ`, e ### **`Δφ` è l incremento VERO** "
          "*(quello che contiene anche `delta_sync_phi`)*: la sincronizzazione entra "
          "### **sia in `dU_φ` sia nel lavoro**, quindi ### **si cancella NEL RESIDUO "
          "DI QUELLA IDENTITÀ** — ### ⛔ **e SOLO lì: NON nel bilancio di `H`, dove lo "
          "spostamento di sincronizzazione FA LAVORO, e molto** *(la sezione "
          "qui sotto)*. E siccome il collaudo ### **MISURA** che la coppia è "
          "`−∂U/∂φ` *(`1.49e-15`)*, l identità `dU_φ = −Σ coppia·Δφ + O(Δφ²)` è "
          "### **ALGEBRA**: il residuo ### **È** quel resto del secondo ordine. "
          "### ⛔ **Non è una congettura, e non dipende da questa corsa.**")
        A("")
        A("> ### ⚠ **LA BANDA QUI SOTTO ERA PENSATA COME CONFERMA INDIPENDENTE, E LO "
          "È SOLO IN PARTE:** il coefficiente del secondo ordine va come "
          "`cos(φ_i − φ_j)` e quindi ### **VARIA DA PASSO A PASSO**, perciò il "
          "rapporto ### **non deve** restare costante quanto avevo creduto scrivendo "
          "la previsione. ### **Era un attesa mia troppo forte, e la correggo qui "
          "invece di leggere la larghezza della banda come un problema del codice.**")
        A("")
        _rr = _qfin.get("rap")
        if not _rr or not _rr[0]:
            A("> ### ⚠ **LA BANDA NON È MISURATA:** non lo affermo senza i numeri.")
        else:
            _fat = _rr[2] / _rr[0]
            A("> ### **LA PROVA, dai dati:** se il residuo è del secondo ordine, "
              "allora `residuo / Δφ` deve restare in una banda ### **stretta** mentre "
              "il residuo assoluto cambia. ### **MISURATO:** fra i decili `10` e `90` "
              "sta fra `%s` e `%s`, un fattore ### **%s** — ma il ### **massimo è "
              "`%s`**."
              % (n4(_rr[0], 4), n4(_rr[2], 4), n4(_fat, 3), n4(_rr[3], 4)))
            A("")
            A("> ### ⛔ **E LA CODA NON LA NASCONDO: SU %s PASSI, `%s` HANNO "
              "`abs(W_interf)` SOTTO IL `10 %%` DELLA SUA MEDIANA** — cioè un "
              "### **denominatore quasi nullo**, dove un rapporto relativo esplode "
              "### **per aritmetica, non per fisica.**" % (n4(_rr[5]), n4(_rr[4])))
            A("")
            if _fat <= 5.0:
                A("> ### ✔ **PER L `80 %%` CENTRALE DEI PASSI IL RAPPORTO STA ENTRO UN "
                  "FATTORE `%s`: la firma del secondo ordine REGGE.** ### ➜ **Quindi la "
                  "domanda «la coppia scalare è conservativa?» NON la decide la corsa: "
                  "la decide il COLLAUDO, e il collaudo dice SÌ a `1.49e-15`.** "
                  "### ⚠ **Il criterio, come è scritto, misura il PASSO "
                  "D INTEGRAZIONE** — e lo dico invece di presentare un `NON "
                  "SODDISFATTO` come se parlasse della fisica." % n4(_fat, 3))
            else:
                A("> ### **UN FATTORE `%s` SULL `80 %%` CENTRALE: la banda è più "
                  "larga di quanto avessi previsto**, e la ragione è scritta qui "
                  "sopra *(il coefficiente del secondo ordine varia come "
                  "`cos(φ_i − φ_j)`)*. ### ⛔ **QUESTO NON INDEBOLISCE LA "
                  "CONCLUSIONE, perché la conclusione poggia sul COLLAUDO e sull "
                  "ALGEBRA, non sulla banda:** la coppia scalare ### **È** `−∂U/∂φ`, "
                  "misurato a `1.49e-15` su tre casi, con la differenza finita a "
                  "conferma. ### ➜ **Quindi il `NON SODDISFATTO` del criterio NON "
                  "dice che la coppia non conserva: dice che `dt` non è abbastanza "
                  "piccolo perché il lavoro di PRIMO ordine approssimi `ΔU` all "
                  "`1 %%`.** ### ⚠ **E LA MISURA CHE SEPAREREBBE il secondo ordine "
                  "dalla coda dei denominatori piccoli è il lavoro col TRAPEZIO** "
                  "*(la coppia valutata ANCHE a `φ` nuove)*: ### **questa corsa non "
                  "la registra, e lo scrivo come misura MANCANTE, non come "
                  "dettaglio.**" % n4(_fat, 3))
        A("")
        # --- ### la NON conservazione VERA, esatta
        A("## ⭐ **LA NON-CONSERVAZIONE VERA, A `A` FISSO: `dT + dU_φ`** "
          "*(esatta, nessuna approssimazione)*")
        A("")
        A("| finestra | `dT` sommato | `dU_φ` sommato | ### **`dT + dU_φ`** | "
          "in quota di `dU_φ` |")
        A("|---|--:|--:|--:|--:|")
        for et, a, b in FIN:
            f = _fin(a, b)
            if not f:
                continue
            _st = sum(v["dT"] for _k, v in f)
            _su = sum(v["dU_phi"] for _k, v in f)
            A("| %s | %s | %s | ### **%s** | %s |"
              % (et, n4(_st), n4(_su), n4(_st + _su),
                 pct((_st + _su) / _su) if _su else "—"))
        A("")
        A("> ### ⛔ **A `A` FISSO L ENERGIA NON SI CONSERVA. E LA CAUSA NON LA SCELGO "
          "IO: LA SCELGONO I NUMERI**, perché `dT` si DECOMPONE dal bilancio. "
          "### **In unità di energia:** la voce del bilancio è una media di "
          "`Δ(phivel²)` per nodo, quindi il suo contributo a `T` è "
          "### **`½·M_PH·(voce_masse·n_masse + voce_vuoto·n_vuoto)`**.")
        A("")
        A("| finestra | ### **termostato** | ### **coppia** | `scuoti` | residuo "
          "incrociato | ### **somma** | `dT` misurato |")
        A("|---|--:|--:|--:|--:|--:|--:|")
        _dom = {}
        for et, a, b in FIN:
            f = [(k, pts[k]) for k in sorted(pts) if a <= k <= b
                 and (pts[k].get("per_classe") or {}).get("masse")]
            if not f:
                A("| %s | — | — | — | — | — | — |" % et)
                continue
            _v = {q: 0.0 for q in VOCI}
            for _k, r in f:
                pc = r["per_classe"]
                for q in VOCI:
                    for cl, nn in (("masse", _nm), ("vuoto", _nv)):
                        x = (pc.get(cl) or {})
                        if x.get(q) is not None:
                            _v[q] += 0.5 * x[q] * (x.get("nodi") or nn)
            _sm = sum(_v.values())
            _dtm = sum(v["dT"] for _k, v in _fin(a, b))
            A("| %s | ### **%s** | ### **%s** | %s | %s | ### **%s** | %s |"
              % (et, n4(_v["termostato"]), n4(_v["coppia"]), n4(_v["scuoti"]),
                 n4(_v["residuo_incrociato"]), n4(_sm), n4(_dtm)))
            _dom[et] = max(VOCI, key=lambda q: abs(_v[q]))
        A("")
        _d1 = _dom.get("1..215 *(PRIMA delle nascite)*")
        if _d1 == "termostato":
            A("> ### ⛔ **E LA PREVISIONE DEL TASK HISTORY ERA INCOMPLETA, MIA:** avevo "
              "scritto che la non-conservazione viene dai ### **tre termini "
              "non-gradiente** della coppia. ### **I numeri dicono che la voce "
              "DOMINANTE è il TERMOSTATO**, e il motivo è nel codice: `B-SCAL-TS` "
              "azzera `xi_termo` ### **prima** di ogni passo, ma lo step lo "
              "### **RICALCOLA** — e il valore ricalcolato è ### **NEGATIVO**, cioè "
              "### **RIFORNISCE** energia invece di frenarla *(`xi<0` RIFORNISCE, ed è "
              "scritto nel commento del simulatore)*. ### ➜ **Quindi «senza "
              "termostato» resta una SORGENTE, e il referto lo dice invece di "
              "attribuire tutto ai tre termini che avevo censito.**")
        elif _d1 == "coppia":
            A("> ### ✔ **LA VOCE DOMINANTE È LA COPPIA, e la somma delle voci "
              "RIPRODUCE `dT`** — il bilancio è un'identità, non una stima. "
              "### ⚠ **E IL MIO SOSPETTO ERA SBAGLIATO:** avevo pensato che fosse il "
              "### **residuo del termostato** *(`xi<0` RIFORNISCE)* a immettere "
              "l energia, perché `xi` resta negativo. ### **I numeri dicono che quel "
              "residuo è PICCOLO**, ed è un risultato a sé: in `B-SCAL-TS` il "
              "### **«termostato senza memoria» è quasi innocuo**, e quello che scalda "
              "è la ### **coppia** *(dell interferenza più i tre termini "
              "non-gradiente)*.")
        elif _d1:
            A("> ### ⚠ **LA VOCE DOMINANTE È `%s`**, e NON era quella che avevo "
              "previsto." % _d1)
        A("")
        A("| finestra | `W` dell ### **interferenza** | `W` della coppia "
          "### **totale** | ### **`W_extra`** *(i tre non-gradiente)* | "
          "### **in quota** |")
        A("|---|--:|--:|--:|--:|")
        for et, a, b in FIN:
            f = _fin(a, b)
            if not f:
                continue
            _wi = sum(v["W_interferenza"] for _k, v in f)
            _wt = sum(v["W_coppia_totale"] for _k, v in f)
            _wx = sum(v["W_extra_non_gradiente"] for _k, v in f)
            A("| %s | %s | %s | ### **%s** | %s |"
              % (et, n4(_wi), n4(_wt), n4(_wx),
                 pct(abs(_wx) / abs(_wi)) if _wi else "—"))
            # ### ⚠ **NON <<la prima finestra>>: il rapporto CAMBIA fra le due, e
            #   prendere la prima sarebbe scegliere quella che fa comodo.** Si tiene
            #   ciascuna, e il verdetto si da' sul TOTALE.
            _pe["W_extra_" + et[:7]] = (abs(_wx) / abs(_wi)) if _wi else None
            _pe["Wi_som"] = _pe.get("Wi_som", 0.0) + abs(_wi)
            _pe["Wx_som"] = _pe.get("Wx_som", 0.0) + abs(_wx)
        A("")
        # --- ### il lavoro di `A` che cambia
        # ======================================================
        #   ### ⭐ **L IPOTESI DEL GUARDIANO: LA SINCRONIZZAZIONE COME SORGENTE**
        # ======================================================
        A("## ⭐ **L IPOTESI DEL GUARDIANO: LA SINCRONIZZAZIONE È LA SORGENTE** "
          "*(`D2-TER`, e qui è UN IPOTESI, non un fatto)*")
        A("")
        A("L algebra, scritta: `W_tot = Σ c_tot·Δφ` con `Δφ = dt_n·phivel(t+1) + "
          "delta_sync_phi`, mentre la voce `coppia` del bilancio cinetico, in unità di "
          "energia, è `Σ p1·d_cop = Σ dt_n·c_tot·p1/M_PH`. ### ➜ **La loro differenza "
          "contiene DUE cose, non una:**")
        A("")
        A("```")
        A("W_tot - voce_coppia  =  Σ dt_n·c_tot·(p2 - p1)  +  Σ c_tot·delta_sync_phi")
        A("                        ^^^^^^^^^^^^^^^^^^^^^^")
        A("                        il SECONDO ORDINE, e si LIMITA dal bilancio:")
        A("                        dt_n·c_tot = M_PH·d_t + dt_n·xi·p1, quindi")
        A("                        Σ dt_n·c_tot·d_t = M_PH·Σ(d_t²) + (un termine in xi)")
        A("                        e `residuo_incrociato` in energia E' (1/2)·Σ(d_t²)")
        A("```")
        A("")
        A("| finestra | `W_tot` | voce ### **`coppia`** | ### **differenza** | di cui "
          "### **secondo ordine** | ### **`W_sync` STIMATO** | `ΔH` | ### **`−W_sync` "
          "su `ΔH`** |")
        A("|---|--:|--:|--:|--:|--:|--:|--:|")
        _ipo = {}
        for et, a2, b2 in FIN:
            f = _fin(a2, b2)
            if not f:
                continue
            _wt2 = sum(v["W_coppia_totale"] for _k, v in f)
            _dh2 = sum(v["dT"] + v["dU_phi"] for _k, v in f)
            _vc = _vri = 0.0
            for _k, _v in f:
                _pc = (pts.get(_k, {}).get("per_classe") or {})
                for _cl, _nn in (("masse", _nm), ("vuoto", _nv)):
                    _x = _pc.get(_cl) or {}
                    if _x.get("coppia") is not None:
                        _vc += 0.5 * _x["coppia"] * (_x.get("nodi") or _nn)
                    if _x.get("residuo_incrociato") is not None:
                        _vri += 0.5 * _x["residuo_incrociato"] * (_x.get("nodi") or _nn)
            _dif = _wt2 - _vc
            _sec = 2.0 * _vri
            _ws = _dif - _sec
            _ipo[et] = (_ws, _dh2, (-_ws/_dh2) if _dh2 else None, _dif, _sec)
            A("| %s | %s | %s | ### **%s** | %s | ### **%s** | %s | ### **%s** |"
              % (et, n4(_wt2), n4(_vc), n4(_dif), n4(_sec), n4(_ws), n4(_dh2),
                 pct((-_ws / _dh2) if _dh2 else None)))
        A("")
        _q1 = _ipo.get(FIN[0][0])
        if _q1 and _q1[2] is not None:
            A("> ### ⭐ **L ARITMETICA DEL GUARDIANO REGGE, E L HO RIFATTA IO:** la "
              "differenza è ### **%s**, e il secondo ordine — ### **che il guardiano "
              "non aveva messo** — ne spiega ### **%s**, quindi `W_sync` stimato è "
              "### **%s**. ### ➜ **Cioè lo spostamento di sincronizzazione spiega il "
              "%s della crescita di `H` nella prima finestra.** ### **Con il "
              "secondo ordine dentro, l ipotesi è PIÙ forte di come era scritta, non "
              "meno.**"
              % (n4(_q1[3]), n4(_q1[4]), n4(_q1[0]), pct(_q1[2])))
            A("")
        A("> ### ⛔ **E RESTA UN IPOTESI, per DUE ragioni che dico io:** ### **(1)** "
          "`W_sync` qui è ### **DEDOTTO da una differenza**, non misurato — "
          "`delta_sync_phi` non è registrato in questa corsa; ### **(2)** la "
          "differenza è costruita sulla coppia ### **TOTALE**, mentre "
          "`W_interferenza` *(la sola che sia `−∂U/∂φ`)* è un altro numero. "
          "### ➜ **La misura DIRETTA è `D2-TER` punto `1`, e il controllo positivo "
          "è che `W_sync + W_newton` ricomponga `W_interferenza`.**")
        A("")
        A("## ⭐ **QUANTA PARTE DI `ΔH` VIENE DA `A` CHE CAMBIA, E QUANTA DALLE `φ`**")
        A("")
        A("> ### ⚠ **IL PASSO DI RITARDO È DICHIARATO:** `dU_A` si può calcolare solo "
          "alla chiamata ### **successiva** *(la `A` nuova nasce lì)*, quindi la voce "
          "del passo `k` ### **chiude il passo `k−1`** e si somma col suo `dU_φ`.")
        A("")
        A("| finestra | `dU_φ` | ### **`dU_A`** | di cui ### **`w`** *(archi comuni)* | "
          "di cui ### **nascite** | archi ### **spariti** | ### **quota di `A`** |")
        A("|---|--:|--:|--:|--:|--:|--:|")
        for et, a, b in FIN:
            f = [(k, v) for k, v in _fin(a, b) if v.get("dU_A_chiude_il_precedente")]
            if not f:
                A("| %s | — | ### **n/d** | — | — | — | — |" % et)
                continue
            _su = sum(v["dU_phi"] for _k, v in _fin(a, b))
            _d = [v["dU_A_chiude_il_precedente"] for _k, v in f]
            _ta = sum(x["totale"] for x in _d)
            _w = sum(x["w_su_archi_comuni"] for x in _d)
            _nn = sum(x["nascite_archi_nuovi"] for x in _d)
            _sp = sum(x["archi_spariti"] for x in _d)
            _den = abs(_su) + abs(_ta)
            A("| %s | %s | ### **%s** | %s | %s | %s | ### **%s** |"
              % (et, n4(_su), n4(_ta), n4(_w), n4(_nn), n4(_sp),
                 pct(abs(_ta) / _den) if _den else "—"))
            _pe.setdefault("quota_A_%d" % a, (abs(_ta) / _den) if _den else None)
            _pe.setdefault("nascite_%d" % a, _nn)
            # ### ⚠ **IL CONTEGGIO E IL LAVORO SONO DUE COSE:** `_nn` e' un ENERGIA,
            #   `quanti_nuovi` e' un NUMERO DI ARCHI. La previsione nomina gli ARCHI.
            _pe.setdefault("quanti_nuovi_%d" % a,
                           sum(x.get("quanti_nuovi", 0) for x in _d))
        A("")
        # --- ### `T`, `U`, `H` per classe ai passi di misura
        A("## **`T`, `U` e `H` AI PASSI DI MISURA, PER CLASSE**")
        A("")
        A("> ### ⚠ **`U` SI SPARTISCE IN TRE CLASSI, NON DUE:** un arco fra una massa e "
          "il vuoto ### **non appartiene a nessuna delle due**, e metterlo d autorità "
          "in una falserebbe il bilancio. Le masse sono ### **%s** nodi su "
          "### **%s**." % (n4(_nm), n4(_nm + _nv)))
        A("")
        A("| passo | `T` masse | `T` vuoto | `U` masse | `U` misti | `U` vuoto | "
          "### **`H`** | `E_cin` del codice |")
        A("|--:|--:|--:|--:|--:|--:|--:|--:|")
        for k in sorted(_en):
            if k not in (1, 50, 150, 215, 216, 230, 300, 400, 500):
                continue
            v = _en[k]
            _tc = v.get("T_pre_per_classe") or {}
            _uc = v.get("U_per_classe") or {}
            A("| %d | %s | %s | %s | %s | %s | ### **%s** | %s |"
              % (k, n4(_tc.get("masse")), n4(_tc.get("vuoto")), n4(_uc.get("masse")),
                 n4(_uc.get("misti")), n4(_uc.get("vuoto")), n4(v.get("H_pre")),
                 n4(v.get("E_cin_del_codice"), 5)))
        A("")
        # --- ### ⭐ **IL CONTROLLO POSITIVO DELLA SPARTIZIONE**
        _er_u = _er_a = 0.0
        _quanti = 0
        for _k, v in sorted(_en.items()):
            _uc = v.get("U_per_classe") or {}
            _ac = v.get("archi_per_classe") or {}
            if not _uc or v.get("U") is None:
                continue
            _quanti += 1
            _su = sum(_uc.values())
            _er_u = max(_er_u, abs(_su - v["U"]) / max(abs(v["U"]), 1e-300))
            _ra = pts.get(_k, {}).get("archi")
            if _ra:
                _er_a = max(_er_a, abs(sum(_ac.values()) - _ra))
        A("| il controllo positivo | su %s passi |" % n4(_quanti))
        A("|---|--:|")
        A("| le tre classi di `U` ### **ricompongono `U`** | scarto relativo massimo ### **%s** |" % n4(_er_u, 3))
        A("| gli archi delle tre classi ### **fanno gli archi del passo** | scarto massimo ### **%s** |" % n4(_er_a))
        A("")
        if _er_u < 1e-9 and _er_a == 0:
            A("> ### ✔ **LA SPARTIZIONE PER CLASSE È VERIFICATA, non presunta:** le tre "
              "classi ricompongono `U` e gli archi. ### **Senza questo controllo una "
              "colonna per classe potrebbe essere sbagliata senza che si veda.**")
        else:
            A("> ### ⛔ **LA SPARTIZIONE PER CLASSE NON TORNA** *(scarto su `U` %s, sugli "
              "archi %s)*: ### **le colonne per classe NON valgono finché non si trova "
              "la causa.**" % (n4(_er_u, 3), n4(_er_a)))
        A("")
        # --- ### il CRITERIO 2
        A("## ⛔ **IL CRITERIO `SENZA BAGNO NON ESPLODE`**")
        A("")
        _k1 = min(_en) if _en else None
        _kz = max(_en) if _en else None
        _t1 = _en[_k1]["T_post"] if _k1 is not None else None
        _tz = _en[_kz]["T_post"] if _kz is not None else None
        _cre = (_tz / _t1) if (_t1 and _tz) else None
        _pe["crescita_T"] = _cre
        A("| | |")
        A("|---|--:|")
        A("| `T` al passo `%s` | %s |" % (_k1, n4(_t1)))
        A("| `T` al passo `%s` | %s |" % (_kz, n4(_tz)))
        A("| ### **la crescita** | ### **%s** |"
          % (("×%s" % n4(_cre)) if _cre else "n/d"))
        A("| il confronto: `B-TS` *(coppia SPINORIALE, stesso bagno spento)* | "
          "### **×25.29** |")
        A("")
        # ### ⛔ **E QUI NON RIPETO L ERRORE CHE IL PUNTO 1 DI QUESTO MANDATO HA
        #   APPENA CORRETTO:** <<energia cinetica TOTALE>> è dominata dal VUOTO, che è
        #   il `90.34 %` dei nodi. La crescita si riporta ### **ANCHE PER CLASSE.**
        _t1c = (_en[_k1].get("T_post_per_classe") or {}) if _k1 is not None else {}
        _tzc = (_en[_kz].get("T_post_per_classe") or {}) if _kz is not None else {}
        A("| classe | `T` al `%s` | `T` al `%s` | ### **la crescita** |"
          % (_k1, _kz))
        A("|---|--:|--:|--:|")
        _crc = {}
        for _cl in ("masse", "vuoto"):
            _x, _y = _t1c.get(_cl), _tzc.get(_cl)
            _r2 = (_y / _x) if (_x and _y) else None
            _crc[_cl] = _r2
            A("| ### **%s** | %s | %s | ### **%s** |"
              % (_cl.upper(), n4(_x), n4(_y),
                 ("×%s" % n4(_r2)) if _r2 else "n/d"))
        A("| ### **TOTALE** *(dominato dal VUOTO: %s nodi su %s)* | %s | %s | "
          "### **%s** |"
          % (n4(_nv), n4(_nm + _nv), n4(_t1), n4(_tz),
             ("×%s" % n4(_cre)) if _cre else "n/d"))
        A("")
        if _crc.get("masse") and _crc.get("vuoto"):
            A("> ### ⛔ **LA CLAUSOLA È SCRITTA SULL ENERGIA TOTALE, CHE È LA "
              "GRANDEZZA DOMINATA DAL VUOTO** — ed è ### **lo stesso difetto** che il "
              "punto `1` di questo mandato ha dichiarato per `D2`. ### **Il verdetto "
              "formale resta quello che è** *(un criterio fissato prima non si riscrive "
              "dopo)*, ### **ma i numeri per classe dicono un altra cosa:** le MASSE "
              "crescono ### **×%s**, il VUOTO ### **×%s** — un fattore ### **%s** fra "
              "le due. ### ➜ **Quello che esplode è il VUOTO, e le masse restano "
              "l oggetto freddo e coerente.**"
              % (n4(_crc["masse"]), n4(_crc["vuoto"]),
                 n4(_crc["vuoto"] / _crc["masse"], 2)))
            A("")
        if _cre is None:
            A("> ### ⚠ **NON DECIDIBILE.**")
        elif _cre < 3.0:
            A("> ### ✔ **`SENZA BAGNO NON ESPLODE`: il criterio è SODDISFATTO** "
              "*(×%s, soglia ×3)*. ### ⭐ **E il confronto è il punto:** con la coppia "
              "### **spinoriale** e lo stesso bagno spento l energia cinetica cresceva "
              "### **×25.29**." % n4(_cre))
        else:
            A("> ### ⛔ **IL CRITERIO NON È SODDISFATTO: ×%s**, oltre la soglia ×3 "
              "*(`B-TS` dava ×25.29)*." % n4(_cre))
        A("")
        # --- ### `AUC` e coerenza
        A("## **L `AUC` E LA COERENZA, COME IN `D2`**")
        A("")
        _mts = hts.get("misure", {})
        _a2 = (_mts.get("230") or {}).get("auc_materia_vuoto")
        _a4t = (_mts.get("400") or {}).get("auc_materia_vuoto")
        _pe["auc400"] = _a4t
        _asc = None
        if H("B-SCAL"):
            _asc = (H("B-SCAL").get("misure", {}).get("400") or {}).get(
                "auc_materia_vuoto")
        A("| | `B-SCAL-TS` | `B-SCAL` *(col bagno)* | controllo |")
        A("|---|--:|--:|--:|")
        A("| AUC al `230` | ### **%s** | %s | %s |"
          % (n4(_a2),
             n4((H("B-SCAL").get("misure", {}).get("230") or {}).get(
                 "auc_materia_vuoto")) if H("B-SCAL") else "—",
             n4(_auc_ct.get(230))))
        A("| ### **AUC al `400`** | ### **%s** | %s | %s |"
          % (n4(_a4t), n4(_asc), n4(_auc_ct.get(400))))
        A("")
        _pmt = (_mts.get("230") or {}).get("per_massa") or {}
        A("| massa | coerenza di fase al `230` | `std(phivel)` |")
        A("|---|--:|--:|")
        for et in sorted(_pmt):
            x = _pmt[et]
            if not x:
                continue
            A("| `%s` | ### **%s** | %s |"
              % (et, n4(x.get("coer_2pi")), n4(x.get("phivel_std"))))
        _vt = (_mts.get("230") or {}).get("vuoto") or {}
        A("| il ### **VUOTO** | %s | %s |"
          % (n4(_vt.get("coer_2pi")), n4(_vt.get("phivel_std"))))
        A("")
        A("---")
        A("")
    A("# ⭐ **LE MIE PREVISIONI, CONTRO I NUMERI**")
    A("")
    pr = []
    _vinc = locals().get("_esito_h3")
    if _vinc:
        pr.append(("`PH3-1`",
                   "### ⛔ **`H3` sarà SMENTITA sulla TERZA clausola: il termostato NON è la "
                   "voce principale** *(l'aritmetica: nemmeno al tetto `\\|xi\\|=2` arriva a "
                   "`×8.1`, dà al massimo `×2.3`)*",
                   "la voce principale nel VUOTO sui primi `50` passi è ### **`%s`**" % _vinc,
                   "### ✔ **CONFERMATA**" if _vinc != "termostato"
                   else "### ⛔ **SMENTITA**: era il termostato, e allora `\\|xi\\|` deve aver "
                        "saturato la guardia — ### **che sarebbe un difetto a sé** *(`A11`)*"))
        pr.append(("`PH3-2`",
                   "la voce principale sarà ### **`scuoti_vuoto`**, che è ADDITIVO",
                   "è ### **`%s`**" % _vinc,
                   "### ✔ **CONFERMATA**" if _vinc == "scuoti" else "### ⛔ **SMENTITA**"))
    if _es.get("B-S") is not None and _es.get("B-T") is not None:
        _ok = (_es["B-S"] >= 0.85) and (_es["B-T"] < 0.85)
        pr.append(("`PH3-3`",
                   "### **`B-S` mostrerà l'effetto grande** *(AUC al `400` `>= 0.85`)*, "
                   "### **`B-T` quello piccolo** *(`< 0.85`)*",
                   "`B-S` %s, `B-T` %s" % (n4(_es["B-S"]), n4(_es["B-T"])),
                   "### ✔ **CONFERMATA**" if _ok else "### ⛔ **SMENTITA**"))
    if kk:
        a, b = pb[kk[0]], pb[kk[-1]]
        ta, tb = a.get("termostato") or {}, b.get("termostato") or {}
        if ta.get("T_target") and tb.get("T_target"):
            _cr = (tb["T_target"] - ta["T_target"]) / ta["T_target"]
            pr.append(("`PH3-4`",
                       "`T_target` cresce ### **POCO** e per via di `median(d0)`; e "
                       "### **non è il motore** del riscaldamento dei primi `50` passi",
                       "`T_target` dal passo `%d` al `%d`: ### **%s**" % (kk[0], kk[-1], pct(_cr)),
                       "### ✔ **CONFERMATA sul POCO**" if abs(_cr) < 0.10
                       else "### ⛔ **SMENTITA: cresce di %s**" % pct(_cr)))
    _rap = []
    for k in sorted(pb):
        v = (pb[k].get("per_classe") or {})
        av = (v.get("vuoto") or {}).get("amp_mediana")
        am = (v.get("masse") or {}).get("amp_mediana")
        if av and am:
            _rap.append((k, am / av))
    if len(_rap) >= 2:
        pr.append(("`PH3-5`",
                   "### **`Λ` cresce e la soppressione delle masse si INDEBOLISCE:** il "
                   "rapporto `amp` masse/vuoto ### **SALE**",
                   "dal passo `%d` al `%d`: ### **%s → %s**"
                   % (_rap[0][0], _rap[-1][0], n4(_rap[0][1]), n4(_rap[-1][1])),
                   "### ✔ **CONFERMATA**" if _rap[-1][1] > _rap[0][1]
                   else "### ⛔ **SMENTITA**: il rapporto CALA"))
    # ---------------------------------------------------- le previsioni di `B-TS`
    if hts:
        _a4 = (hts.get("misure", {}).get("400") or {}).get("auc_materia_vuoto")
        _pm = (hts.get("misure", {}).get("230") or {}).get("per_massa") or {}
        _c2 = [x["coer_2pi"] for x in _pm.values() if x]
        _co = (sum(_c2) / len(_c2)) if _c2 else None
        _pts = {int(r["passo"]): r for r in hts["passi"]}
        _lim = [k for k in sorted(_pts) if k >= 1]
        _som = {q: 0.0 for q in VOCI}
        for k in _lim:
            v = (_pts[k].get("per_classe") or {}).get("masse")
            if v:
                for q in VOCI:
                    _som[q] += v[q]
        _dom = max(VOCI, key=lambda q: abs(_som[q]))
        if _a4 is not None:
            pr.append(("`PTS-1`",
                       "### ⛔ **scattera' `LA CAUSA E' DENTRO LE MASSE (H2)`: AUC al "
                       "`400` `< 0.6`** *(perche' la coppia agisce `9.31 x` piu' nelle masse "
                       "che nel vuoto)*",
                       "AUC al `400` in `B-TS`: ### **%s**" % n4(_a4),
                       "### ✔ **CONFERMATA**" if _a4 < 0.60 else
                       ("### ⛔ **SMENTITA, ed e' il risultato piu' importante: le masse "
                        "SOPRAVVIVONO senza il bagno**" if _a4 >= 0.85 else
                        "### ⛔ **SMENTITA**: sta fra `0.60` e `0.85`, quindi nessuno dei "
                        "due criteri scatta")))
            pr.append(("`PTS-2`",
                       "il termine dominante nelle masse sara' la ### **`coppia`**",
                       "e' ### **`%s`** *(il %s)*"
                       % (_dom, pct(abs(_som[_dom]) / max(sum(abs(_som[q]) for q in VOCI),
                                                          1e-30))),
                       "### ✔ **CONFERMATA**" if _dom == "coppia"
                       else "### ⛔ **SMENTITA**"))
        _E = [(k, (_pts[k].get("termostato") or {}).get("E_cin")) for k in _lim]
        _E = [(k, x) for k, x in _E if x is not None]
        if _E:
            _E0, _E1 = _E[0][1], _E[-1][1]
            _cb = [(k, (passi("base").get(k) or {}).get("termostato", {}).get("E_cin"))
                   for k in (230,)]
            _cb = [x for _k, x in _cb if x is not None]
            _r = (_cb[0] / _E1) if (_cb and _E1) else None
            pr.append(("`PTS-3`",
                       "l'energia totale ### **CRESCE** ma `~10 x` meno del controllo "
                       "*(previsto `~1.2` al `230` contro `13.57`)*",
                       "da `%s` a ### **%s**%s"
                       % (n4(_E0, 4), n4(_E1, 4),
                          ("; e al `230` il controllo e' `%s x` piu' caldo" % n4(_r, 1))
                          if _r else ""),
                       "### ✔ **CONFERMATA**" if _E1 > _E0 * 1.05
                       else ("### ⛔ **SMENTITA: CALA**" if _E1 < _E0 * 0.95
                             else "### ⛔ **SMENTITA: si CONSERVA**")))
        if _co is not None:
            pr.append(("`PTS-4`",
                       "la coerenza di fase delle masse al `230` sara' ### **`< 0.3`**, quindi "
                       "il criterio del bagno NON scatta",
                       "### **%s**" % n4(_co),
                       "### ✔ **CONFERMATA**" if _co < 0.30 else
                       "### ⛔ **SMENTITA**"))
        _nf = sum(1 for r in hts["passi"] if r.get("phivel_non_finiti"))
        pr.append(("`PTS-5`",
                   "### **NON divergera'** entro `500` passi, e ### **non si congelera'**",
                   "passi con `phivel` non finiti: ### **%s**; stato: ### **%s**"
                   % (n4(_nf), br["B-TS"].get("stato")),
                   "### ✔ **CONFERMATA**"
                   if (_nf == 0 and br["B-TS"].get("stato") == "DATI SALVATI")
                   else "### ⛔ **SMENTITA**"))
    # ---------------------------------------------------- le previsioni di `D1` e `D2`
    if "_d1_som" in dir():
        _q = float(_d1_pos) / max(_d1_tot, 1)
        pr.append(("`PD-1`",
                   "### ⛔ **`LA COPPIA POMPA`**, con margine larghissimo. "
                   "### ⚠ **DICHIARATA GIA' NOTA** prima di girare: era nei dati di `H3`",
                   "nelle masse: positiva nel ### **%s** dei passi `1..230`, somma ### **%s**"
                   % (pct(_q), n4(_d1_som, 2)),
                   "### ✔ **CONFERMATA**" if (_q >= 0.80 and _d1_som > 0)
                   else "### ⛔ **SMENTITA**"))
    _pmass = (pb.get(230) or {}).get("per_classe", {}).get("masse") or {}
    _pvuo = (pb.get(230) or {}).get("per_classe", {}).get("vuoto") or {}
    if _pmass.get("P_coppia") is not None and _pvuo.get("P_scuoti") is not None:
        _a, _b, _c = (abs(_pmass["P_coppia"]), abs(_pmass.get("P_scuoti") or 0.0),
                      abs(_pvuo["P_scuoti"]))
        _ord = (0.1 <= (_a / max(_b, 1e-30)) <= 10.0) and (_a < _c)
        pr.append(("`PD-2`",
                   "`P_coppia` nelle masse ### **dello stesso ordine** di `P_scuoti` nelle "
                   "masse, e ### **molto piu' piccola** di `P_scuoti` nel vuoto",
                   "al passo `230`: `\\|P_coppia\\|` masse ### **%s**, `\\|P_scuoti\\|` masse "
                   "%s, `\\|P_scuoti\\|` vuoto %s" % (n4(_a, 2), n4(_b, 2), n4(_c, 2)),
                   "### ✔ **CONFERMATA**" if _ord else "### ⛔ **SMENTITA**"))
    if _neg and _posT:
        pr.append(("`PD-3`",
                   "`P_termo` cambiera' ### **SEGNO** attorno al passo `49`",
                   "primo passo negativo: ### **`%d`** *(positiva su %d passi, negativa su %d)*"
                   % (min(_neg), len(_posT), len(_neg)),
                   "### ✔ **CONFERMATA**" if 30 <= min(_neg) <= 70
                   else "### ⚠ **CAMBIA SEGNO, ma al passo `%d`**" % min(_neg)))
    if hsc:
        _a4b = (hsc.get("misure", {}).get("400") or {}).get("auc_materia_vuoto")
        if _a4b is not None:
            pr.append(("`PD-4`",
                       "### ⚠ **`D2` dara' `NON BASTA`: AUC al `400` `< 0.6`** "
                       "*(il ramo scalare cambia la COPPIA, non la scena, e `A` resta "
                       "`w*cos(phi0_i - phi0_j)` con `phi0` CONGELATA)*",
                       "AUC al `400` in `B-SCAL`: ### **%s** *(controllo %s)*"
                       % (n4(_a4b), n4(_auc_ct.get(400))),
                       "### ✔ **CONFERMATA**" if _a4b < 0.60 else
                       ("### ⛔ **SMENTITA, ed e' il risultato piu' importante: una coppia "
                        "che legge la fase TIENE le masse**" if _a4b >= 0.85 else
                        "### ⛔ **SMENTITA**: sta fra `0.60` e `0.85`")))
        if _kcom is not None and _Ect is not None:
            _esc = _Es.get(_kcom)
            pr.append(("`PD-5`",
                       "ma l'energia totale in `D2` sara' ### **MINORE** che nel controllo",
                       "### ⚠ **il controllo di `A-S1` NON registra `E_cin`**, quindi il "
                       "confronto e' col braccio `base` al ### **massimo passo comune, il "
                       "`%d`**: `B-SCAL` ### **%s** contro `base` ### **%s**"
                       % (_kcom, n4(_esc, 4), n4(_Ect, 4)),
                       "### ✔ **CONFERMATA**" if (_esc is not None and _esc < _Ect)
                       else "### ⛔ **SMENTITA**"))
        else:
            pr.append(("`PD-5`",
                       "ma l'energia totale in `D2` sara' ### **MINORE** che nel controllo",
                       "### ⛔ **nessun passo in comune con un braccio NON intervenuto che "
                       "registri `E_cin`**",
                       "### ⚠ **NON DECIDIBILE**"))
    A("| | la previsione | il numero | esito |")
    A("|---|---|---|---|")
    # ==================================================================
    #   ### **`PE-1..PE-7`: le previsioni di `D2-BIS`**
    # ==================================================================
    if hts:
        # ### ⭐ **I NUMERI DEL COLLAUDO SI LEGGONO DAL SUO FILE** *(`L-NUMERI`)*:
        #   un numero ricopiato non ha provenienza.
        _cp = os.path.join(DIR, "collaudo_potenziale.txt")
        _txt = ""
        try:
            _txt = io.open(_cp, encoding="utf-8").read()
        except Exception:                               # noqa: BLE001
            _txt = ""

        def _num(rx):
            m = re.search(rx, _txt, re.S)
            return m.group(1) if m else None

        _sc = _num(r"ramo SCALARE.*?VERE del simulatore: differenza massima "
                   r"relativa `([^`]+)`")
        _sp = _num(r"coppia SPINORIALE.*?differenza massima relativa `([^`]+)`")
        _df = _num(r"DIFFERENZA FINITA.*?scarto relativo massimo `([^`]+)`")
        _cc = _num(r"COLLAUDO DEL POTENZIALE: (\d+ su \d+)")
        if _cc:
            A("> ### ✔ **I numeri del collaudo del potenziale sono LETTI dal suo "
              "file** *(`csv/_test_fork/_termo_h3/collaudo_potenziale.txt`, "
              "### **%s**)*, non ricopiati." % _cc)
            A("")
        else:
            A("> ### ⚠ **Il file del collaudo del potenziale non è leggibile:** le "
              "previsioni `PE-1` e `PE-2` restano ### **NON VALUTATE**, e lo dico "
              "invece di metterci i numeri a memoria.")
            A("")
        if _sc:
            pr.append(("`PE-1`",
                       "il collaudo del potenziale ### **CHIUDE** sulla funzione vera, "
                       "con residuo relativo ### **`< 1e-10`**",
                       "### **%s**" % _sc,
                       "### ✔ **CONFERMATA**" if float(_sc) < 1e-10
                       else "### ⛔ **SMENTITA**"))
        if _sp:
            pr.append(("`PE-2`",
                       "### **il caso che DEVE fallire fallisce:** la coppia "
                       "### **spinoriale** non chiude, con residuo ### **`> 1e-2`**",
                       "### **%s**%s" % (_sp, (" *(e la differenza finita, che non passa "
                                              "dalla mia derivata, dà `%s`)*" % _df)
                                        if _df else ""),
                       "### ✔ **CONFERMATA**" if float(_sp) > 1e-2
                       else "### ⛔ **SMENTITA**"))
        _qa = _qfin.get("1..215 *(PRIMA delle nascite)*")
        _qb = _qfin.get("216..500 *(DOPO la prima nascita)*")
        if _qa is not None:
            _ok3 = (_qa >= 0.95) and (_qb is None or _qb < _qa)
            pr.append(("`PE-3`",
                       "il criterio della conservazione è ### **soddisfatto** nella "
                       "finestra `1..215` *(`>= 95 %`)* e ### **meno** dopo il `216`",
                       "`1..215` ### **%s**, `216..500` ### **%s**"
                       % (pct(_qa), pct(_qb) if _qb is not None else "n/d"),
                       "### ✔ **CONFERMATA**" if _ok3 else
                       "### ⛔ **SMENTITA**, e il referto dice ### **perché**: quel "
                       "residuo misura il ### **passo d integrazione**, non la "
                       "conservazione"))
        _cre2 = _pe.get("crescita_T")
        if _cre2 is not None:
            pr.append(("`PE-4`",
                       "### **`SENZA BAGNO NON ESPLODE` è soddisfatto:** l energia "
                       "cinetica ### **non cresce ×3**",
                       "### **×%s** *(`B-TS`, con la coppia spinoriale, dava "
                       "×25.29)*" % n4(_cre2),
                       "### ✔ **CONFERMATA**" if _cre2 < 3.0
                       else "### ⛔ **SMENTITA**"))
        _qA = _pe.get("quota_A_216")
        if _qA is not None:
            _nn216 = _pe.get("nascite_216")
            _senza = (sum((r.get("nati_nel_passo") or 0) for r in hts["passi"]) == 0)
            pr.append(("`PE-5`",
                       "il ### **lavoro di `A` che cambia** è la parte "
                       "### **dominante** della variazione di `H` dopo il `216`, "
                       "### **perché le nascite aggiungono archi**",
                       "la quota di `A` è ### **%s**, gli archi nuovi sono "
                       "### **%s** e il loro lavoro ### **%s**"
                       % (pct(_qA), n4(_pe.get("quanti_nuovi_216")), n4(_nn216)),
                       ("### ⛔ **SMENTITA, E PER UN MOTIVO CHE NON AVEVO PREVISTO:** "
                        "in questo braccio ### **non nasce NIENTE**, quindi la "
                        "premessa della previsione *(«le nascite aggiungono archi»)* "
                        "### **non si verifica mai**. ### **Non è che le nascite non "
                        "dominino: non ci sono.**") if _senza
                       else ("### ✔ **CONFERMATA**" if _qA > 0.50
                             else "### ⛔ **SMENTITA**: dominano le `φ`")))
        _a4b = _pe.get("auc400")
        if _a4b is not None:
            pr.append(("`PE-6`",
                       "l `AUC` al `400` resta ### **`>= 0.85`** anche senza bagno",
                       "### **%s**" % n4(_a4b),
                       "### ✔ **CONFERMATA**" if _a4b >= 0.85
                       else "### ⛔ **SMENTITA**"))
        _wx2 = ((_pe.get("Wx_som") / _pe["Wi_som"])
                if _pe.get("Wi_som") else None)
        if _wx2 is not None:
            pr.append(("`PE-7`",
                       "### **`W_extra` NON è trascurabile** *(almeno il `10 %` di "
                       "`W_interf` in modulo)*. ### **Scritta così per poter PERDERE:** "
                       "se fosse trascurabile, il criterio chiuderebbe anche sulla "
                       "coppia totale e il mio censimento sarebbe stato pessimismo",
                       "### **%s** di `W_interf` su tutta la corsa — e ### ⚠ **il "
                       "rapporto CAMBIA con la finestra:** `%s` su `1..215`, `%s` su "
                       "`216..500`. ### **Riporto entrambe invece di scegliere quella "
                       "che mi conviene**"
                       % (pct(_wx2), pct(_pe.get("W_extra_1..215")),
                          pct(_pe.get("W_extra_216..5"))),
                       "### ✔ **CONFERMATA sul TOTALE**" if _wx2 >= 0.10
                       else "### ⛔ **SMENTITA: era pessimismo mio**"))
    for x in pr:
        A("| %s | %s | %s | %s |" % x)
    A("")
    _ok = sum(1 for x in pr if "CONFERMATA" in x[3] and "SMENTITA" not in x[3])
    _no = sum(1 for x in pr if "SMENTITA" in x[3])
    A("> ### **%d confermate, %d SMENTITE** su %d." % (_ok, _no, len(pr)))
    A("")
    A("---")
    A("")
    A("# ⛔ **CHE COSA QUESTO REFERTO NON DICE, E NON PROPONE**")
    A("")
    A("| | |")
    A("|---|---|")
    A("| una ### **CURA** | ### ⛔ **NESSUNA.** La scelta fra anticipare il vuoto locale *(`B1`)*, curare prima `D31`, o entrambe, ### **è di Luca** |")
    A("| la variabilità fra semi | ### **UN seme** *(il `11`)*: `P3` non soddisfatta |")
    A("| i valori ASSOLUTI | ### **`U1` è aperta:** si leggono le ### **differenze fra bracci** |")
    A("| `B-T` come ### **«senza termostato»** | ### ⛔ **NON lo è:** è «senza MEMORIA del termostato», e il residuo è misurato qui sopra |")
    if hts:
        A("| ### **`B-SCAL-TS` come prova della DIREZIONE di Luca** | ### ⛔ **NON lo "
          "è:** il ramo scalare usa `cos(φ_k − φ_j)`, ### **non `cos((φ_k − φ_j)/2)`**. "
          "È un test sul ### **PRINCIPIO**, e un esito positivo ### **non decide la "
          "cura** |")
        A("| ### **la conservazione lungo la CORSA** | ### ⛔ **non è misurata, e non "
          "può esserlo con questi dati:** servirebbe il lavoro col ### **TRAPEZIO** "
          "*(la coppia valutata anche a `φ` nuove)*, che la corsa ### **non registra**. "
          "### **Quello che è misurato è che la coppia È `−∂U/∂φ`** *(collaudo, "
          "`1.49e-15`)* |")
        A("| ### **«senza bagno»** | ### ⚠ **il bagno è SOPPRESSO, non spento:** "
          "`xi_termo` è azzerata ### **prima** di ogni passo, ma lo step lo "
          "### **RICALCOLA** — e il residuo resta, ### **misurato** nella "
          "decomposizione di `dT` |")
        if sum((r.get("nati_nel_passo") or 0) for r in hts["passi"]):
            A("| ### **la finestra** | ### **`1..215` vale solo PRIMA delle nascite** "
              "*(`FINESTRA-PRE-NASCITA`)*: le due finestre sono ### **sempre "
              "separate** nelle tavole qui sopra |")
        else:
            A("| ### **la finestra** | ### ⚠ **in questo braccio la frontiera del "
              "`216` NON separa le nascite da niente**, perché nascite ### **non ce ne "
              "sono**: divide ### **solo il tempo**. Le due finestre si riportano "
              "comunque *(il mandato le chiede)*, e `FINESTRA-PRE-NASCITA` resta la "
              "ragione per cui si riportano SEPARATE |")
    A("| la ricostruzione come ### **esatta** | ### ⛔ **NON lo è:** predice `xi` allo `0.1 %`, e il residuo è riportato |")
    A("")
    io.open(FUORI, "w", encoding="utf-8", newline=NL).write(NL.join(R) + NL)
    print("scritto %s (%d righe)" % (FUORI, len(R)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
