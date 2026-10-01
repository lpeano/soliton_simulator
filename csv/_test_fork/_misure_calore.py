# -*- coding: utf-8 -*-
"""**LE MISURE DI `DIVISIONE-AUTOCONSISTENTE`, allargate al CALORE: `M0`, `M1`, `M3`, `M4`, `M6`.**

**Mandato del guardiano del 2026-10-01, su priorita' di Luca** *(«qua si gioca veramente la
dinamica pulita di tutto»)*. **Nessuna riga del simulatore: solo misura.**

| | che cosa misura |
|---|---|
| **`M0`** | ### **esiste un'energia totale?** Le parti **misurabili** della risposta |
| **`M1`** | ### **quanta `|tw|` sparisce** per passo con le divisioni, come **frazione** del totale |
| **`M3`** | il **termostato Nose-Hoover**: serie di `xi_termo`, `E_cin`, `T_target`; frena o rifornisce; clip e pavimenti; e ### **quanto cambierebbe `T_target`** con la mediana di **TUTTI** gli archi |
| **`M4`** | ### **il bilancio di una divisione**: prima e dopo la voce `mitosi`, separando il **calcio** dalla **cancellazione dell'arco** |
| **`M6`** | lo **scuotimento** come **sorgente**: quanta agitazione immette, **dove**, e ### **quanta torsione** |

### ⭐ **COME SI MISURA, ed e' il punto dello strumento: LE VOCI DELLO SCHEDULATORE**
Non si tocca il simulatore e non si spezza il passo: si mette una **spia** su
`_ferma_se_registro_incoerente`, che il commit 1 chiama ### **dopo OGNI voce** *(generalizzazione
2)*. ### ➜ **Ogni confine di voce diventa un punto di misura**, e la variazione di una grandezza
si puo' ### **ATTRIBUIRE ALLA VOCE** invece di essere letta a fine passo come un totale.
### **Il presidio del commit 1 diventa l'imbragatura di misura di questo**, e non era previsto.

### ⚠ CHE COSA QUESTO STRUMENTO **NON** FA
### **Non chiama <<energia>> cio' che non lo e'.** Le somme che calcola sono **grandezze con le
dimensioni** di un'energia *(`K_fase`, `K_metr`)* oppure **proxy DICHIARATI** *(`Q2`)*, e `M0`
spiega **quali** sono energie vere e quali no. ### **Un bilancio su una grandezza che non si
conserva nemmeno in principio non e' un bilancio: e' una somma.**

### ⚠ **I NOMI DELLE MISURE: la forma corta `M0`…`M6` e' LOCALE A QUESTO FILE**
Nell'indice ### **`M1`, `M2`, `M3`, `M4` ESISTONO GIA'**, e `M2` e' *«LA MITOSI — ① il figlio
nasce nel PUNTO MEDIO»*, cioe' ### **lo stesso argomento**: la forma nuda ### **risolverebbe al
difetto sbagliato.** ### **Fuori da qui si scrive `DIVISIONE-AUTOCONSISTENTE:M0` … `:M6`.**

COMANDO:  python csv/_test_fork/_misure_calore.py [--passi=72]
USCITA:   il referto `csv/_test_fork/_misure_calore/_misure_calore.json` + stdout.
"""
import copy
import hashlib
import io
import json
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, os.path.join(RADICE, "csv"))
import _presidio  # noqa: E402

_presidio.avvia(__file__)
import numpy as np  # noqa: E402
import _cli_flag  # noqa: E402
import _passo  # noqa: E402

FUORI = os.path.join(RADICE, "csv", "_test_fork", "_misure_calore")
SIM = os.path.join(RADICE, "soliton_simulator.py")
# i contatori delle nascite, PER EVENTO: servono a dire QUALE evento ha agito in quel passo.
CONTATORI_NASCITA = ("_g_nati_mitosi", "_g_nati_mitosi_ev", "_g_nati_schwinger",
                     "_g_nati_schwinger_ev", "_g_sm_nascite")


def blob(percorso):
    return hashlib.sha1(io.open(percorso, "rb").read()).hexdigest()


def carica(nome):
    """La scena **GRANDE**, di riferimento: `nmasse` e `sep` **da `a`**, come fa il pilota.

    ### **E' lo STESSO caricamento del sigillo del controllo unico** *(`_sig_controllo_unico.py`)*,
    e lo e' di proposito: ### **un'altra scena sarebbe un altro sistema**, e il mandato dice
    *«sistema di riferimento»*.
    """
    import contextlib
    with contextlib.redirect_stdout(io.StringIO()):
        _S0, argv = _cli_flag.argv_del_driver(extra=["--seme=11"],
                                              dest=os.path.join(FUORI, "_scarto_cli"))
        S, a = _cli_flag.carica_dal_cli(list(argv), nome=nome)
        S._NMASSE_VIDEO["n"] = max(2, int(getattr(a, "nmasse", 2)))
        S._NMASSE_VIDEO["sep"] = float(getattr(a, "sep", 3.0))
        S._NMASSE_VIDEO["size"] = None
        S.avvia_test("MASSE-COERENTI")()
    return S, S.net


def scalari(net):
    """**Le grandezze SCALARI a un confine di voce.** Nomi onesti: `K_` solo dove e' cinetica."""
    n, m = int(net.n), int(len(net.i))
    pv = np.asarray(net.phivel)[:n]
    vd = np.asarray(net.vd)
    d = np.asarray(net.d)
    d0 = np.asarray(net.d0)
    tw = np.asarray(net.tw)
    with np.errstate(over="ignore", invalid="ignore"):
        return {
            "n": n, "m": m,
            # `M_PH = 1.0` UNIFORME (lo dice il codice a :6297), quindi questa E' una cinetica.
            "K_fase": float(np.sum(pv.astype(float) ** 2) * 0.5),
            # cinetica del settore metrico: `vd` e' la velocita' di `d`. Massa d'arco non
            #   dichiarata nel modello -> si usa 1, E SI DICHIARA.
            "K_metr": float(np.sum(vd.astype(float) ** 2) * 0.5),
            # ⚠ PROXY DICHIARATO, NON UN'ENERGIA: la forza e' `cs^2 (M - I) q`, non `-k q`.
            "Q2": float(np.sum((d - d0).astype(float) ** 2)),
            "S_tw": float(np.sum(np.abs(tw.astype(float)))),
            "S_tw_max": float(np.max(np.abs(tw)) if m else 0.0),
            "xi_termo": float(getattr(net, "xi_termo", 0.0)),
            # `E_cin` COME LO VEDE IL TERMOSTATO: una MEDIA, non una somma (:6334).
            "E_cin_termo": float(np.mean(pv.astype(float) ** 2)) if n else 0.0,
            # `P_eq` nei DUE modi: la fetta di oggi e TUTTI gli archi (`P-EQ-MEDIANA-ARCHI`).
            "P_eq_fetta": float(np.median(d0[:n])) if n else 1.0,
            "P_eq_tutti": float(np.median(d0)) if m else 1.0,
        }


def m0_struttura(S, net):
    """### **`M0`: ESISTE UN'ENERGIA TOTALE? Le parti MISURABILI della risposta.**

    La parte **di lettura** sta nel referto e nel piano. Qui stanno i **numeri** che decidono, e
    sono **tre domande con una risposta numerica**:

    | | |
    |---|---|
    | **1** | esiste una **funzione** che calcoli un'energia totale? ### **Si cerca per AST**, non a memoria |
    | **2** | il settore **metrico** e' un **gradiente**? ### **Lo e' SOLO se `cs_arco` e' uniforme** — e `cs_arco` nasce da `cs_nodo`, che si misura |
    | **3** | quali termini sono **espressamente non conservativi**? Si **contano** e si misura **la loro presenza** |
    """
    import ast
    sorgente = io.open(SIM, encoding="utf-8").read()
    albero = ast.parse(sorgente)
    # 1) le funzioni il cui NOME promette un'energia -- e che cosa restituiscono DAVVERO.
    candidate = {}
    for nodo in ast.walk(albero):
        if isinstance(nodo, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if "ener" in nodo.name.lower() or "energ" in nodo.name.lower():
                _doc = ast.get_docstring(nodo) or "(senza docstring)"
                candidate[nodo.name] = _doc.split(chr(10))[0][:120]
    # 2) `cs_nodo`: se NON e' uniforme, `cs_arco` non lo e', e la forza metrica NON e' un gradiente.
    # ⚠ MIO DIFETTO, e il run si e' fermato: PRIMA del primo passo `_cs_nodo_prev` e' uno
    #   SCALARE 0-d (o assente), e `len()` di un oggetto senza dimensioni SOLLEVA. Si usa
    #   `atleast_1d` e `.size`. ### E la correzione non e' solo tecnica: lo scarto di `cs` va
    #   misurato su uno stato SVILUPPATO, non sulla semina -- per questo `M0` ora gira DOPO il run.
    csn = np.atleast_1d(np.asarray(getattr(net, "_cs_nodo_prev", []), dtype=float))
    uniforme = (csn.size > 0 and float(np.max(csn) - np.min(csn)) == 0.0)
    scarto = (float((np.max(csn) - np.min(csn)) / max(abs(float(np.median(csn))), 1e-30))
              if csn.size else None)
    # lo scarto RELATIVO FRA I DUE ESTREMI di uno stesso arco: e' quello che rompe la simmetria
    #   di `diag(cs^2)(I - M)`, perche' `M` e' simmetrica ma `diag(cs^2) M` no.
    if csn.size and len(net.i):
        a = csn[np.asarray(net.i)]
        b = csn[np.asarray(net.j)]
        with np.errstate(divide="ignore", invalid="ignore"):
            rel = np.abs(a - b) / np.maximum(np.abs(a + b) * 0.5, 1e-30)
        arco_scarto = {"mediano": float(np.median(rel)), "massimo": float(np.max(rel)),
                       "archi_con_scarto_non_nullo": int(np.count_nonzero(rel > 0.0)),
                       "archi": int(len(rel))}
    else:
        arco_scarto = None
    return {
        "funzioni_che_promettono_energia": candidate,
        "cs_nodo_uniforme": bool(uniforme),
        "cs_nodo_scarto_relativo_totale": scarto,
        "cs_sui_due_estremi_di_un_arco": arco_scarto,
        "CS_DINAMICO": bool(getattr(S, "CS_DINAMICO", False)),
        "FORK_SU2_MEM": bool(getattr(S, "FORK_SU2_MEM", False)),
        "VERLET": bool(getattr(S, "VERLET", False)),
        "M_PH": float(getattr(S, "M_PH", float("nan"))),
    }


def principale():
    passi = 72
    for a in sys.argv[1:]:
        if a.startswith("--passi="):
            passi = int(a.split("=", 1)[1])
    if not os.path.isdir(FUORI):
        os.makedirs(FUORI)
    P = []

    def stampa(*x):
        r = " ".join(str(y) for y in x)
        P.append(r)
        print(r)

    stampa("=" * 104)
    stampa("LE MISURE DI `DIVISIONE-AUTOCONSISTENTE` + CALORE -- M0, M1, M3, M4, M6")
    stampa("=" * 104)
    stampa("simulatore ..... %s   (sha1 dei byte grezzi)" % blob(SIM)[:8])
    stampa("questo strumento %s" % blob(os.path.abspath(__file__))[:8])
    stampa("passi .......... %d" % passi)
    stampa("")

    S, net = carica("misure_calore")
    _cli_flag.dichiara_configurazione(S, stampa)
    stampa("")


    # ------------------------------------------------- la SPIA sulle voci
    per_voce = []
    stato = {"passo": 0, "foto": None, "prima_mitosi": None, "calcio": []}
    vero = S._ferma_se_registro_incoerente

    def spia(nt, dove, voce=None, comp=None):
        s = scalari(nt)
        prec = stato["foto"]
        riga = {"passo": stato["passo"], "voce": voce, "dove": dove}
        riga.update(s)
        # ### M4, LA CURA DEL 2026-10-01: il CALCIO si misura ATTORNO ALLA VOCE `mitosi`, non
        #   prima-e-dopo il passo. ⚠ MIO DIFETTO, e il suo stesso numero l'ha smentito: col
        #   confronto sull'INTERO PASSO risultavano mossi 102448 genitori sia su `phi` sia su
        #   `phivel` -- cioe' TUTTI i nodi, perche' `step` e `scuoti_vuoto` li muovono tutti.
        #   ### Quel numero non parlava del calcio: parlava del passo.
        #   La composizione mette `step` SUBITO PRIMA di `mitosi`, quindi la fotografia
        #   <<prima della mitosi>> e' quella del confine precedente -- e si tiene SOLO quella.
        if voce == "mitosi" and stato["prima_mitosi"] is not None:
            _pm = stato["prima_mitosi"]
            _n0 = len(_pm["phi"])
            _ph = np.asarray(nt.phi)[:_n0]
            _pv = np.asarray(nt.phivel)[:_n0]
            _dphi = np.abs(((_ph - _pm["phi"] + np.pi) % (2 * np.pi)) - np.pi)
            _dpv = np.abs(_pv - _pm["phivel"])
            stato["calcio"].append({
                "passo": stato["passo"], "n_prima": int(_n0), "n_dopo": int(nt.n),
                "genitori_con_phi_mosso": int(np.count_nonzero(_dphi > 0.0)),
                "genitori_con_phivel_mosso": int(np.count_nonzero(_dpv > 0.0)),
                "dphi_somma": float(np.sum(_dphi)), "dphi_max": float(np.max(_dphi)),
                "dphivel_somma": float(np.sum(_dpv)), "dphivel_max": float(np.max(_dpv)),
                # la cinetica dei SOLI nodi che c'erano prima, contro quella di TUTTI:
                #   serve a separare <<i nati entrano nella somma>> da <<il calcio muove phivel>>.
                "K_fase_vecchi_prima": float(0.5 * np.sum(_pm["phivel"] ** 2)),
                "K_fase_vecchi_dopo": float(0.5 * np.sum(_pv ** 2)),
                "K_fase_tutti_dopo": float(0.5 * np.sum(np.asarray(nt.phivel)[:int(nt.n)] ** 2)),
            })
        # la fotografia per il confine DOPO (cioe' <<prima della prossima voce>>)
        stato["prima_mitosi"] = {"phi": np.asarray(nt.phi)[:int(nt.n)].copy(),
                                 "phivel": np.asarray(nt.phivel)[:int(nt.n)].copy()}
        if prec is not None:
            for k in ("K_fase", "K_metr", "Q2", "S_tw"):
                riga["d_" + k] = s[k] - prec[k]
            riga["d_n"] = s["n"] - prec["n"]
            riga["d_m"] = s["m"] - prec["m"]
        stato["foto"] = s
        per_voce.append(riga)
        return vero(nt, dove, voce=voce, comp=comp)

    S._ferma_se_registro_incoerente = spia

    stampa("")
    stampa("=" * 104)
    stampa("IL RUN: %d passi, con la SPIA sui CONFINI DI VOCE (generalizzazione 2)" % passi)
    stampa("=" * 104)
    import contextlib
    mitosi_dettaglio = []
    for k in range(1, passi + 1):
        stato["passo"] = k
        cont_prima = {c: int(getattr(net, c, 0)) for c in CONTATORI_NASCITA}
        with contextlib.redirect_stdout(io.StringIO()):
            _passo.passo_pieno(S, net)
        cont_dopo = {c: int(getattr(net, c, 0)) for c in CONTATORI_NASCITA}
        nati = {c: cont_dopo[c] - cont_prima[c] for c in CONTATORI_NASCITA}
        if any(nati.values()):
            # ⚠ IL CONTEGGIO DELLE NASCITE resta sul passo (i contatori sono cumulativi); il
            #   CALCIO invece si misura ATTORNO ALLA VOCE, e lo fa la spia.
            mitosi_dettaglio.append({"passo": k, "nati": nati})
    S._ferma_se_registro_incoerente = vero
    stampa("  confini di voce misurati: %d" % len(per_voce))
    stampa("  passi con NASCITE: %d" % len(mitosi_dettaglio))

    # ---------------------------------------------------------------- M0
    stampa("")
    stampa("=" * 104)
    stampa("M0 -- ESISTE UN'ENERGIA TOTALE? (le parti MISURABILI, su stato SVILUPPATO)")
    stampa("=" * 104)
    m0 = m0_struttura(S, net)
    stampa("  funzioni il cui NOME promette un'energia: %d"
           % len(m0["funzioni_che_promettono_energia"]))
    for k, v in m0["funzioni_che_promettono_energia"].items():
        stampa("      `%s` -> %s" % (k, v))
    stampa("  M_PH = %s   (uniforme: la cinetica di fase e' 0.5*sum(phivel^2))" % m0["M_PH"])
    stampa("  CS_DINAMICO = %s   VERLET = %s   FORK_SU2_MEM = %s"
           % (m0["CS_DINAMICO"], m0["VERLET"], m0["FORK_SU2_MEM"]))
    stampa("  cs_nodo UNIFORME: %s   (scarto relativo fra gli estremi del campo: %s)"
           % (m0["cs_nodo_uniforme"], m0["cs_nodo_scarto_relativo_totale"]))
    if m0["cs_sui_due_estremi_di_un_arco"]:
        a = m0["cs_sui_due_estremi_di_un_arco"]
        stampa("  cs sui DUE ESTREMI di uno stesso arco: scarto mediano %.3e, massimo %.3e"
               % (a["mediano"], a["massimo"]))
        stampa("      archi con scarto NON NULLO: %d su %d"
               % (a["archi_con_scarto_non_nullo"], a["archi"]))
    stampa("  ### SE cs NON E' UNIFORME, la forza metrica cs^2 (M - I) q NON E' UN GRADIENTE:")
    stampa("      `M` e' simmetrica, ma `diag(cs^2) M` NON LO E'. Quindi per il settore metrico")
    stampa("      NON esiste un'energia potenziale, e non e' una mia opinione: e' la matrice.")

    # ---------------------------------------------------------------- M1
    stampa("")
    stampa("=" * 104)
    stampa("M1 -- QUANTA |tw| SPARISCE con le divisioni, come FRAZIONE del totale")
    stampa("=" * 104)
    mit = [r for r in per_voce if r.get("voce") == "mitosi" and "d_S_tw" in r]
    m1 = []
    for r in mit:
        base = r["S_tw"] - r["d_S_tw"]
        m1.append({"passo": r["passo"], "d_S_tw": r["d_S_tw"], "S_tw_prima": base,
                   "frazione": (r["d_S_tw"] / base) if base else 0.0,
                   "d_m": r.get("d_m", 0), "d_n": r.get("d_n", 0)})
    persi = [x for x in m1 if x["d_S_tw"] < 0]
    stampa("  voci `mitosi` misurate: %d   di cui con |tw| in CALO: %d" % (len(m1), len(persi)))
    if m1:
        fr = [x["frazione"] for x in m1]
        stampa("  variazione RELATIVA di sum|tw| sulla voce `mitosi`:")
        stampa("      mediana %.3e   minima %.3e   massima %.3e"
               % (float(np.median(fr)), float(np.min(fr)), float(np.max(fr))))
        tot = sum(x["d_S_tw"] for x in m1)
        stampa("  somma algebrica delle variazioni su %d passi: %.6e" % (len(m1), tot))
        stampa("  sum|tw| all'inizio %.6e -> alla fine %.6e"
               % (per_voce[0]["S_tw"], per_voce[-1]["S_tw"]))

    # ---------------------------------------------------------------- M3
    stampa("")
    stampa("=" * 104)
    stampa("M3 -- IL TERMOSTATO NOSE-HOOVER")
    stampa("=" * 104)
    fine = [r for r in per_voce if r.get("voce") == "step"]
    xi = [r["xi_termo"] for r in fine]
    ec = [r["E_cin_termo"] for r in fine]
    pf = [r["P_eq_fetta"] for r in fine]
    pt = [r["P_eq_tutti"] for r in fine]
    frena = sum(1 for x in xi if x > 0)
    rifornisce = sum(1 for x in xi if x < 0)
    clip = sum(1 for x in xi if abs(abs(x) - 2.0) <= 0.0)
    m3 = {"passi": len(xi), "xi_frena": frena, "xi_rifornisce": rifornisce, "xi_nullo":
          len(xi) - frena - rifornisce, "xi_al_clip": clip,
          "xi_min": (float(np.min(xi)) if xi else None),
          "xi_max": (float(np.max(xi)) if xi else None),
          "xi_mediano": (float(np.median(xi)) if xi else None),
          "E_cin_min": (float(np.min(ec)) if ec else None),
          "E_cin_max": (float(np.max(ec)) if ec else None),
          "P_eq_fetta_mediana": (float(np.median(pf)) if pf else None),
          "P_eq_tutti_mediana": (float(np.median(pt)) if pt else None),
          "serie_xi": [float(x) for x in xi], "serie_E_cin": [float(x) for x in ec],
          "serie_P_eq_fetta": [float(x) for x in pf], "serie_P_eq_tutti": [float(x) for x in pt]}
    if pf and pt:
        rap = [(b / a) if a else float("nan") for a, b in zip(pf, pt)]
        m3["T_target_rapporto_tutti_su_fetta"] = {
            "mediano": float(np.median(rap)), "minimo": float(np.min(rap)),
            "massimo": float(np.max(rap))}
        stampa("  ### P-EQ-MEDIANA-ARCHI: `T_target` = cs_rappr^2 * P_eq, e `cs_rappr` NON cambia")
        stampa("      -> IL RAPPORTO DI T_target E' ESATTAMENTE IL RAPPORTO DI P_eq.")
        stampa("      P_eq(tutti gli archi) / P_eq(i primi n): mediano %.6f  min %.6f  max %.6f"
               % (float(np.median(rap)), float(np.min(rap)), float(np.max(rap))))
        stampa("      cioe' T_target cambierebbe di quel fattore SU TUTTO IL SISTEMA.")
    stampa("  xi_termo: frena (xi>0) in %d passi, RIFORNISCE (xi<0) in %d, nullo in %d"
           % (frena, rifornisce, m3["xi_nullo"]))
    stampa("  xi_termo: min %.6e  mediano %.6e  max %.6e   al CLIP +-2 esatto: %d volte"
           % (m3["xi_min"] or 0.0, m3["xi_mediano"] or 0.0, m3["xi_max"] or 0.0, clip))
    stampa("  E_cin (la MEDIA che vede il termostato): min %.6e  max %.6e"
           % (m3["E_cin_min"] or 0.0, m3["E_cin_max"] or 0.0))
    stampa("  P_eq mediana: fetta dei primi n = %.6e   TUTTI gli archi = %.6e"
           % (m3["P_eq_fetta_mediana"] or 0.0, m3["P_eq_tutti_mediana"] or 0.0))
    stampa("  ### il PAVIMENTO 1e-6 di `Tt = max(T_target, 1e-6)`: P_eq non ci si avvicina")
    stampa("      (se la mediana di P_eq e' %.3e, T_target = cs^2 * P_eq e' molto sopra 1e-6)"
           % (m3["P_eq_fetta_mediana"] or 0.0))

    # ---------------------------------------------------------------- M4
    stampa("")
    stampa("=" * 104)
    stampa("M4 -- IL BILANCIO DI UNA DIVISIONE: il CALCIO contro la CANCELLAZIONE DELL'ARCO")
    stampa("=" * 104)
    m4 = {"per_passo": mitosi_dettaglio, "voci_mitosi": []}
    for r in mit:
        m4["voci_mitosi"].append({k: r.get(k) for k in
                                  ("passo", "d_K_fase", "d_K_metr", "d_Q2", "d_S_tw", "d_n",
                                   "d_m", "K_fase", "K_metr", "Q2", "S_tw", "n", "m")})
    calcio = [x for x in stato["calcio"] if x["n_dopo"] > x["n_prima"]]
    m4["calcio_attorno_alla_voce"] = stato["calcio"]
    if mitosi_dettaglio:
        stampa("  passi con nascite: %d   voci `mitosi` con n cresciuto: %d"
               % (len(mitosi_dettaglio), len(calcio)))
    if calcio:
        gm = sum(x["genitori_con_phi_mosso"] for x in calcio)
        gv = sum(x["genitori_con_phivel_mosso"] for x in calcio)
        stampa("  ### IL CALCIO, MISURATO ATTORNO ALLA VOCE `mitosi` (non sul passo intero):")
        stampa("      genitori (nodi che c'erano PRIMA) con `phi` mosso ...... %d" % gm)
        stampa("      genitori con `phivel` mosso ............................ %d" % gv)
        stampa("      somma |dphi| %.6e   max |dphi| %.6e"
               % (sum(x["dphi_somma"] for x in calcio),
                  max(x["dphi_max"] for x in calcio)))
        stampa("      somma |dphivel| %.6e   max |dphivel| %.6e"
               % (sum(x["dphivel_somma"] for x in calcio),
                  max(x["dphivel_max"] for x in calcio)))
        # ### LA CONCLUSIONE SI DERIVA DAL NUMERO. (Nella prima stesura era CABLATA nel testo, e
        #   il suo stesso numero l'ha smentita: e' il difetto che `L-NUMERI` esiste per impedire.)
        if gv == 0 and gm > 0:
            stampa("  ### -> IL CALCIO SPOSTA `phi` E NON `phivel`: non cambia 0.5*sum(phivel^2)")
            stampa("      dei nodi che c'erano, cambia la FASE -- cioe' il termine di")
            stampa("      INTERFERENZA, che e' proprio il pezzo di cui M0 dice che NON esiste")
            stampa("      come funzione di stato (connessione dal Bloch RITARDATO).")
        elif gv > 0:
            stampa("  ### -> IL CALCIO TOCCA ANCHE `phivel` su %d genitori: la premessa del" % gv)
            stampa("      mandato (<<sposta phi, non phivel>>) NON regge, e va corretta.")
        else:
            stampa("  ### -> nessun genitore mosso: in questi passi il calcio NON HA AGITO.")
        # separazione fra <<i nati entrano nella somma>> e <<il calcio muove phivel>>
        dv = sum(x["K_fase_vecchi_dopo"] - x["K_fase_vecchi_prima"] for x in calcio)
        dt_ = sum(x["K_fase_tutti_dopo"] - x["K_fase_vecchi_prima"] for x in calcio)
        stampa("  ### LA CINETICA DI FASE, SEPARATA:")
        stampa("      variazione sui SOLI nodi che c'erano prima ... %+.6e" % dv)
        stampa("      variazione includendo i NATI ................. %+.6e" % dt_)
        stampa("      -> la differenza, %+.6e, e' CIO' CHE I NATI PORTANO DENTRO la somma,"
               % (dt_ - dv))
        stampa("         e NON e' energia che il calcio ha dato a qualcuno.")
    for r in m4["voci_mitosi"]:
        if r.get("d_m") or r.get("d_n"):
            stampa("  passo %3d: d_n %+d  d_m %+d  d_K_fase %+.3e  d_K_metr %+.3e  d_Q2 %+.3e  "
                   "d_S_tw %+.3e" % (r["passo"], r["d_n"] or 0, r["d_m"] or 0,
                                     r["d_K_fase"] or 0.0, r["d_K_metr"] or 0.0,
                                     r["d_Q2"] or 0.0, r["d_S_tw"] or 0.0))

    # ---------------------------------------------------------------- M6
    stampa("")
    stampa("=" * 104)
    stampa("M6 -- LO SCUOTIMENTO COME SORGENTE: quanta agitazione, DOVE, e quanta TORSIONE")
    stampa("=" * 104)
    sc = [r for r in per_voce if r.get("voce") == "scuoti_vuoto" and "d_K_fase" in r]
    m6 = {"voci": [{k: r.get(k) for k in ("passo", "d_K_fase", "d_K_metr", "d_Q2", "d_S_tw")}
                   for r in sc]}
    if sc:
        dk = [r["d_K_fase"] for r in sc]
        dt = [r["d_S_tw"] for r in sc]
        m6["d_K_fase_mediano"] = float(np.median(dk))
        m6["d_K_fase_somma"] = float(np.sum(dk))
        m6["d_K_fase_positivi"] = int(sum(1 for x in dk if x > 0))
        m6["d_S_tw_somma"] = float(np.sum(dt))
        m6["d_S_tw_non_nulli"] = int(sum(1 for x in dt if x != 0.0))
        stampa("  voci `scuoti_vuoto` misurate: %d" % len(sc))
        stampa("  IMMETTE nella cinetica di fase: d_K_fase mediano %+.6e, somma %+.6e, "
               "positivo in %d passi su %d"
               % (m6["d_K_fase_mediano"], m6["d_K_fase_somma"], m6["d_K_fase_positivi"], len(sc)))
        stampa("  ### TORSIONE IMMESSA: d_S_tw somma %+.6e, passi con variazione non nulla %d"
               % (m6["d_S_tw_somma"], m6["d_S_tw_non_nulli"]))
        stampa("      (`scuoti_vuoto` scrive SOLO `net.phivel`: se questo numero e' 0, la")
        stampa("       sorgente del vuoto NON immette avvolgimento, e i DUE bilanci -- energia e")
        stampa("       avvolgimento -- hanno sorgenti DIVERSE.)")
        stampa("  DOVE: l'ampiezza e' PER NODO (stress locale * coerenza locale), quindi e' una")
        stampa("        agitazione LOCALE e non un bagno globale -- al contrario del Nose-Hoover.")

    # ------------------------------------------- il confronto fra le voci (attribuzione)
    stampa("")
    stampa("=" * 104)
    stampa("ATTRIBUZIONE ALLE VOCI: chi muove che cosa (somma su tutti i passi)")
    stampa("=" * 104)
    voci = []
    for v in (S.PASSO_COMPOSIZIONE if hasattr(S, "PASSO_COMPOSIZIONE") else ()):
        rr = [r for r in per_voce if r.get("voce") == v and "d_K_fase" in r]
        if not rr:
            continue
        voci.append({"voce": v, "n": len(rr),
                     "d_K_fase": float(np.sum([r["d_K_fase"] for r in rr])),
                     "d_K_metr": float(np.sum([r["d_K_metr"] for r in rr])),
                     "d_Q2": float(np.sum([r["d_Q2"] for r in rr])),
                     "d_S_tw": float(np.sum([r["d_S_tw"] for r in rr]))})
    stampa("  %-24s %14s %14s %14s %14s" % ("voce", "sum d_K_fase", "sum d_K_metr", "sum d_Q2",
                                            "sum d_S_tw"))
    for x in voci:
        stampa("  %-24s %+14.4e %+14.4e %+14.4e %+14.4e"
               % (x["voce"], x["d_K_fase"], x["d_K_metr"], x["d_Q2"], x["d_S_tw"]))

    fuori = {"blob_sim_sha1_byte": blob(SIM), "blob_strumento": blob(os.path.abspath(__file__)),
             "passi": passi, "M0": m0, "M1": m1, "M3": m3, "M4": m4, "M6": m6,
             "attribuzione_voci": voci,
             "primo_confine": per_voce[0] if per_voce else None,
             "ultimo_confine": per_voce[-1] if per_voce else None}
    json.dump(fuori, io.open(os.path.join(FUORI, "_misure_calore.json"), "w", encoding="utf-8"),
              indent=1, ensure_ascii=False)
    io.open(os.path.join(FUORI, "_corsa.txt"), "w", encoding="utf-8").write(chr(10).join(P))
    stampa("")
    stampa("scritto: %s" % os.path.join(FUORI, "_misure_calore.json"))
    return 0


if __name__ == "__main__":
    sys.exit(principale())
