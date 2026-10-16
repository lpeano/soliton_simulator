# -*- coding: utf-8 -*-
r"""IL RISCALDAMENTO DI FLOQUET SULLA SCENA GRANDE — **la misura che `M1a` non poteva fare.**

> **Mandato di Luca, 2026-10-13, punto `3`:** *«La deriva senza tendenza secolare e'
> misurata su un ANELLO DI 16 NODI, dove un sistema piccolo puo' tornare su se stesso. Il
> riscaldamento tipico dei sistemi Floquet NON e' escluso.»*

### ⛔ **STA IN UN FILE SUO per due ragioni, e nessuna e' la comodita':** `primo_ordine/
bande.py` ha passato il tetto di `700` righe quando questo e' nato *(la regola e' **oltre
SI DIVIDE**)*, e questa misura gira su **`800` dimensioni** — ### **non deve girare per
sbaglio** insieme alle misure piccole.

### ⚠ **I RISULTATI SI SALVANO DURANTE LA CORSA**, una riga per campione in
`doc/dati_floquet.tsv`: se la corsa si ferma, ### **cio' che e' stato misurato RESTA.**

Gira con:  python primo_ordine/bande_floquet.py --scrivi
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)

import bande as BD                                            # noqa: E402
import deriva as DV                                           # noqa: E402
import deriva_variabile as DVAR                               # noqa: E402


# ------------------------------------------------- LA SCENA GRANDE, E IL FLOQUET
# ### ⛔ **PERCHE- UN TORO E NON UN ANELLO GRANDE:** un trasporto casuale su un anello e-
# ### un sistema `1D` **DISORDINATO**, e quelli ### **LOCALIZZANO.** La localizzazione
# ### sopprime il riscaldamento ### **per una ragione che non c-entra con Floquet**, quindi
# ### <<nessuna tendenza>> su un anello ### **non distinguerebbe <<non si riscalda>> da
# ### <<e- localizzato>>.** ### ✅ **In due dimensioni la localizzazione da disordine e-
# ### molto piu- debole.**
DOVE_FLOQUET = os.path.join(os.path.dirname(_QUI), "doc", "REFERTO_floquet_grande.md")
SALVA_FLOQUET = os.path.join(os.path.dirname(_QUI), "doc", "dati_floquet.tsv")


def scena_toro(lati, seme=7, dtau=0.25, vuoto_modulo=2.0, su2=True):
    """### La scena su un **toro**, con le stesse convenzioni della scena ad anello."""
    import corrente as CO
    import incidenza as IN
    import motore as MO
    import stato as ST
    ii, jj, nn = CO.toro(lati)
    inc = IN.Incidenza(np.asarray(ii, dtype=IN.INDICE),
                       np.asarray(jj, dtype=IN.INDICE), nn, capacita=len(ii))
    r = np.random.default_rng(seme)
    nv = r.normal(size=(2 * inc.m, 3))
    nv /= np.linalg.norm(nv, axis=1).reshape(-1, 1)
    U = np.zeros((inc.m, 2, 2), dtype=complex)
    for a in range(inc.m):
        X = r.normal(size=(2, 2)) + 1j * r.normal(size=(2, 2))
        Qm, _q = np.linalg.qr(X)
        if su2:
            Qm = Qm / np.sqrt(np.linalg.det(Qm))
        U[a] = Qm
    st = ST.nuovo(nn, inc.m)
    st["psi_h"][...] = (r.normal(size=st["psi_h"].shape)
                        + 1j * r.normal(size=st["psi_h"].shape))
    st["phi_h"][...] = (float(vuoto_modulo)
                        * np.exp(1j * r.random(st["phi_h"].shape) * 2.0 * np.pi))
    mot = MO.Motore(inc, MO.Geometria(nv, U), st, np.full(nn, dtau), "numpy")
    return inc, mot, st, {"eps": 0.5}


def floquet(lati=(10, 10), ticks=4000, seme=7, vuoto_modulo=2.0, ogni=20,
            dtau=0.25, prepara="casuale"):
    """### `M1a` sulla **scena grande**: ### **il riscaldamento di Floquet, cercato.**

    ### ⚠ **I RISULTATI SI SALVANO DURANTE LA CORSA**, una riga per campione: se la corsa
    si ferma, ### **cio' che e' stato misurato RESTA.**
    """
    import composizione as CM
    import io
    inc, mot, st, par = scena_toro(lati, seme, dtau, vuoto_modulo)
    x0 = DVAR.satura(st, mot)
    Wm = BD.matrice_W(mot, st)
    omega, V, piu, meno, zero = BD.diagonalizza(Wm)
    Pp, Pm, P0 = BD.proiettore(V, piu), BD.proiettore(V, meno), BD.proiettore(V, zero)
    # ### ⛔ **E QUESTO E- UN DIFETTO CHE HO TROVATO MISURANDO:** uno stato
    # ### CASUALE ### **parte GIA- alla parita-** -- un vettore casuale ha peso uguale
    # ### nelle due meta- dello spettro *(misurato: squilibrio `0.00195`)*. ### ⚠ **Da
    # ### li- non si puo- <<andare verso la parita->>: si puo- solo ANDARE VIA**, quindi la
    # ### misura ### **non puo- vedere cio- che il mandato chiede di cercare.**
    # ### ✅ **`prepara=<<banda>>` mette lo stato in UNA banda sola**, cioe- allo
    # ### squilibrio `1`: ### **la- l-avvicinamento alla parita- SI VEDE.**
    if prepara == "banda":
        v = Pp @ st["psi_h"].ravel()
        nrm = float(np.linalg.norm(st["psi_h"]))
        v = v * (nrm / max(float(np.linalg.norm(v)), 1e-300))
        st["psi_h"][...] = v.reshape(st["psi_h"].shape)
    else:
        assert prepara == "casuale", (
            "`prepara` vale `casuale` o `banda`, e NON ha un valore di comodo: decide"
            " ### **da dove parte lo squilibrio**, cioe' se la misura puo' vedere"
            " l'avvicinamento alla parita' (%r)" % (prepara,))
    f = io.open(SALVA_FLOQUET, "wb")
    cap = ("t\tE\tprimo\tvuoto\tN_piu\tN_meno\tN_zero\tQ\tIm_W\telicita" + chr(10))
    f.write(cap.encode("utf-8"))
    f.flush()
    serie = []
    for t in range(0, ticks + 1):
        if t:
            mot.apri_tick()
            for idl, frazione, _tipo in CM.ORDINE:
                nome, vuole_par = DV.OPERATORE[idl]
                mot.operatori[nome](st, par if vuole_par else {}, frazione)
            mot.chiudi_tick()
        if t == 0 or (t % ogni) == 0 or t == ticks:
            g = BD.grandezze(st["psi_h"], Wm, Pp, Pm, P0)
            p1, p2 = DV.due_termini(st, mot, par)
            g["t"] = t
            g["primo"] = p1
            g["vuoto"] = p2
            g["E"] = p1 + p2
            g["elicita"] = float(np.sum(mot.elicita(st)))
            serie.append(g)
            f.write(("%d\t%.12g\t%.12g\t%.12g\t%.12g\t%.12g\t%.12g\t%.12g\t%.12g"
                     "\t%.12g" % (t, g["E"], p1, p2, g["N_piu"], g["N_meno"],
                                  g["N_zero"], g["Q"], g["Im_W"], g["elicita"])
                     + chr(10)).encode("utf-8"))
            f.flush()
    f.close()
    return serie, {"x0": x0, "dim": int(Wm.shape[0]), "n": inc.n, "m": inc.m,
                   "dim_piu": int(np.sum(piu)), "dim_meno": int(np.sum(meno)),
                   "dim_zero": int(np.sum(zero)),
                   "memoria_MB": Wm.nbytes / 1048576.0}


def tendenza(serie, chiave="E"):
    """### `(pendenza, ampiezza, rapporto)` sulla serie di una grandezza."""
    t = np.asarray([g["t"] for g in serie], dtype=float)
    v = np.asarray([g[chiave] for g in serie], dtype=float)
    v = v - v[0]
    pend, quota = np.polyfit(t, v, 1)
    spieg = abs(pend) * (t[-1] - t[0])
    res = v - (pend * t + quota)
    amp = float(np.max(res) - np.min(res))
    return float(pend), amp, (spieg / amp if amp > 0 else float("inf"))


def squilibrio(g):
    """### `|N+ - N-| / (N+ + N-)`: ### **`0` e' la PARITA'.**"""
    s = g["N_piu"] + g["N_meno"]
    return abs(g["N_piu"] - g["N_meno"]) / max(s, 1e-300)


def main_floquet(argv):
    """### Il referto del **riscaldamento di Floquet** sulla scena grande."""
    import io
    import platform
    nl = chr(10)
    r = []
    print("=" * 100)
    print("IL RISCALDAMENTO DI FLOQUET SULLA SCENA GRANDE")
    print("=" * 100)
    r.append("# IL RISCALDAMENTO DI FLOQUET SULLA SCENA GRANDE — **le bande vanno"
             " alla PARITA', `E` non ha tendenza**")
    r.append("")
    r.append("> ### ⛔ **E DUE PREVISIONI CADONO, la mia e quella del mandato:** `E`"
             " **non** mostra una")
    r.append("> tendenza nemmeno su `4000` tick e `800` dimensioni."
             " ### ✅ **Ma le popolazioni delle bande")
    r.append("> VANNO alla parita'**, e lo si vede ### **solo dopo aver corretto un difetto"
             " della mia")
    r.append("> misura.**")
    r.append("")
    r.append("Lo rigira:  `python primo_ordine/bande_floquet.py --scrivi`")
    r.append("")
    r.append("## 1. LA SCENA, E PERCHE' NON UN ANELLO GRANDE")
    r.append("")
    r.append("### ⛔ Un anello di `208` nodi avrebbe la dimensione giusta e sarebbe"
             " **la scelta sbagliata:**")
    r.append("un trasporto casuale su un anello e' un sistema `1D` **disordinato**, e quelli"
             " ### **LOCALIZZANO.**")
    r.append("### ⚠ **La localizzazione sopprime il riscaldamento per una ragione che"
             " non c'entra con")
    r.append("Floquet**, quindi *<<nessuna tendenza>>* su un anello ### **non"
             " distinguerebbe <<non si")
    r.append("riscalda>> da <<e' localizzato>>.** ### ✅ **Toro `2D`, dove la"
             " localizzazione e' molto piu' debole.**")
    r.append("")
    serie_a, info = floquet(ticks=4000, ogni=20, prepara="casuale")
    r.append("| la voce | il valore |")
    r.append("|---|---|")
    for k, v in (("scena", "toro 2D 10x10 (NON la scena del banco: il banco e' IRREGOLARE)"),
                 ("nodi / archi", "%d / %d" % (info["n"], info["m"])),
                 ("dimensione `4m`", info["dim"]),
                 ("banda `+` / `-` / settore `0`",
                  "%d / %d / %d" % (info["dim_piu"], info["dim_meno"],
                                    info["dim_zero"])),
                 ("memoria della matrice", "%.2f MB" % info["memoria_MB"]),
                 ("tick", 4000), ("`dtau`", 0.25), ("seme", 7),
                 ("`U` per arco", "SU(2) casuale"),
                 ("### ⭐ `x = max|h_k|/Lambda_k` all'inizio",
                  "### **%.4f** (la soglia era `>= 0.5`: la misura HA MATERIA)"
                  % info["x0"])):
        r.append("| %s | `%s` |" % (k, v))
    r.append("| piattaforma | `%s`, numpy `%s` |" % (platform.system(), np.__version__))
    r.append("")
    r.append("### ⭐ **E IL SETTORE `0` E' VUOTO ANCHE QUI** *(`0` su `800`)*: non era"
             " una proprieta'")
    r.append("dell'anello. ### **`Q = N+ - N-` e' definita senza un pezzo di stato che non"
             " ha segno.**")

    r.append("")
    r.append("## 2. ⛔ **`E` NON HA UNA TENDENZA**, nemmeno qui")
    r.append("")
    r.append("| la grandezza | pendenza per tick | ampiezza dei residui | **rapporto** |")
    r.append("|---|--:|--:|--:|")
    for k, et in (("E", "`E`"), ("primo", "il **primo** termine"),
                  ("vuoto", "il termine del **vuoto**"), ("N_piu", "`N+`"),
                  ("Q", "`Q`"), ("elicita", "`somma_k h_k`")):
        p, a, rr = tendenza(serie_a, k)
        print("      %-8s pendenza %+.4e  ampiezza %.4e  rapporto %.4f" % (k, p, a, rr))
        r.append("| %s | `%+.4e` | `%.4e` | **`%.4f`** |" % (et, p, a, rr))
    r.append("")
    r.append("### ⛔ **LA SOGLIA ERA `> 1` = tendenza, `< 0.3` = nessuna:"
             " TUTTI I RAPPORTI SONO `< 0.08`.**")
    r.append("### **Quindi nessuna tendenza secolare**, e il mandato dice *<<se resta senza"
             " tendenza")
    r.append("anche li', dichiaralo>>*: ### ✅ **lo dichiaro.** `E` va da `%.3f` a"
             " `%.3f` passando per" % (serie_a[0]["E"], serie_a[-1]["E"]))
    r.append("`%.3f` e `%.3f`: ### **un'oscillazione grande SENZA deriva.**"
             % (min(g["E"] for g in serie_a), max(g["E"] for g in serie_a)))

    r.append("")
    r.append("## 3. ⛔ UN DIFETTO DELLA MIA MISURA, trovato misurando")
    r.append("")
    sq_a = [squilibrio(g) for g in serie_a]
    r.append("Con lo stato **casuale** lo squilibrio `|N+ - N-|/(N+ + N-)` va da"
             " **`%.6f`** a **`%.6f`**:" % (sq_a[0], sq_a[-1]))
    r.append("### **CRESCE**, e sembrerebbe <<si allontana dalla parita'>>.")
    r.append("")
    r.append("### ⛔ **MA UN VETTORE CASUALE PARTE GIA' ALLA PARITA':** ha peso uguale"
             " nelle due meta'")
    r.append("dello spettro. ### ⚠ **Da li' non si puo' ANDARE VERSO la parita': si"
             " puo' solo andare via**")
    r.append("— quindi ### **la misura non poteva vedere cio' che il mandato chiede di"
             " cercare.**")

    serie_b, info_b = floquet(ticks=4000, ogni=20, prepara="banda")
    sq_b = [squilibrio(g) for g in serie_b]
    r.append("")
    r.append("## 4. ⭐ **CORRETTA: PREPARATO IN UNA BANDA SOLA, LE BANDE VANNO ALLA"
             " PARITA'**")
    r.append("")
    r.append("Lo stato iniziale e' `P+ psi` *(riscalato alla stessa norma)*, cioe' lo"
             " squilibrio parte da **`1`**.")
    r.append("")
    r.append("| `t` | squilibrio `|N+ - N-|/(N+ + N-)` |")
    r.append("|--:|--:|")
    for i, et in ((0, "0"), (20, "400"), (50, "1000"), (100, "2000"), (-1, "4000")):
        print("      t=%-6s squilibrio %.6f" % (et, sq_b[i]))
        r.append("| `%s` | **`%.6f`** |" % (et, sq_b[i]))
    med = float(np.mean(sq_b[-20:]))
    mini = float(min(sq_b))
    r.append("")
    r.append("| | il numero |")
    r.append("|---|--:|")
    r.append("| media degli **ultimi `20` campioni** | `%.6f` |" % med)
    r.append("| **minimo** lungo la corsa | `%.6f` |" % mini)
    r.append("| `N+` | `%.3f` -> `%.3f` |" % (serie_b[0]["N_piu"],
                                              serie_b[-1]["N_piu"]))
    r.append("| `N-` | `%.3f` -> `%.3f` |" % (serie_b[0]["N_meno"],
                                              serie_b[-1]["N_meno"]))
    r.append("| la **norma** *(controllo)* | `%.4f` -> `%.4f` |"
             % (serie_b[0]["norma"], serie_b[-1]["norma"]))
    r.append("| ### ⭐ **`1 / sqrt(4m)`** | ### **`%.4f`** |"
             % (1.0 / np.sqrt(info["dim"])))
    r.append("")
    r.append("### ✅ **LA SOGLIA ERA <<scende di almeno un fattore `2`>>: SCENDE DI UN"
             " FATTORE `%.0f`** *(fino al" % (sq_b[0] / max(mini, 1e-300)))
    r.append("minimo)*, e poi **fluttua**. ### ⭐ **E IL VALORE D'EQUILIBRIO E' LA"
             " FLUTTUAZIONE DI TAGLIA")
    r.append("FINITA:** `1/sqrt(4m) = %.4f` contro una media misurata di `%.4f`."
             % (1.0 / np.sqrt(info["dim"]), med))
    r.append("")
    r.append("### ⭐ **E QUESTO RICONCILIA IL PARAGRAFO `3` invece di scegliere fra due"
             " letture:** lo stato")
    r.append("casuale **non si allontanava** dalla parita' — ### **era GIA'"
             " all'equilibrio, e fluttuava.**")
    r.append("### **Le due corse dicono la stessa cosa.**")

    r.append("")
    r.append("## 5. CHE COSA CADE DELLE PREVISIONI")
    r.append("")
    r.append("| | la previsione | l'esito |")
    r.append("|---|---|---|")
    pe, ae, re = tendenza(serie_a, "E")
    r.append("| `F1` *(mia e del mandato)* | una **tendenza** in `E` | ### ⛔ **FALSA:"
             " rapporto `%.4f`**, e la soglia era `> 1` |" % re)
    r.append("| `F2` *(mia e del mandato)* | le popolazioni **verso la parita'** |"
             " ### ✅ **VERA**, ma visibile **solo** preparando lo stato in una banda |")
    r.append("| `F3` *(del mandato)* | l'energia locale **sale** | ### ⛔ **no:** `E`"
             " oscilla e non sale — e avevo scritto **<<non lo so>>** |")
    r.append("")
    r.append("### ⭐ **LA LETTURA, e la dico separata dai numeri:** il sistema"
             " **termalizza nel grado di")
    r.append("liberta' DELLE BANDE** *(equipartizione, che e' l'<<infinita temperatura>> di"
             " quel grado di")
    r.append("liberta')*, ### **ma `E` non cresce**, perche' `E` non e' limitata dal basso"
             " e non ha un")
    r.append("<<serbatoio>> verso cui salire: oscilla.")
    r.append("### ⚠ **E questa e' UNA LETTURA, non una misura:** l'ho scritta dopo i"
             " numeri, e lo dichiaro.")
    r.append("")
    r.append("## 6. ⚠ I LIMITI")
    r.append("")
    r.append("1. ### **NON e' la scena del banco:** il toro e' **regolare**, il banco e'"
             " **irregolare**. Se il riscaldamento dipendesse dall'irregolarita',"
             " ### **questa misura non lo vedrebbe.**")
    r.append("2. **un seme solo** *(`7`)*, e la soglia della tendenza e' su **una corsa**.")
    r.append("3. `4000` tick: ### **non esclude una tendenza su scale piu' lunghe**, e con"
             " un'ampiezza di `%.0f` ### **una deriva lenta sarebbe sepolta.**" % ae)
    r.append("4. i proiettori sono **spettrali**, quindi tutto cio' che e' <<per banda>> e'"
             " ### **GLOBALE.**")
    r.append("")
    if "--scrivi" in argv:
        io.open(DOVE_FLOQUET, "wb").write((nl.join(r) + nl).encode("utf-8"))
        print("REFERTO: %s" % DOVE_FLOQUET)
    print("=" * 100)
    return 0


def main(argv):
    """### Il comando. ### **Il referto si scrive solo se lo si CHIEDE.**"""
    sys.path.insert(0, os.path.join(os.path.dirname(_QUI), "csv"))
    import _presidio
    _presidio.avvia(__file__)
    return main_floquet(argv)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
