# -*- coding: utf-8 -*-
"""**LA SOGLIA LOCALE DOVE AVVENGONO LE DIVISIONI — misurata DENTRO la decisione.**

**Mandato del guardiano del 2026-10-01, punto 2:** riprodurre la sua misura col mio strumento.
E' ### **il «braccio in piu'» che avevo dichiarato** in `0487c20` e non avevo girato.

### ⛔ **PERCHE' SERVE: IL BRACCIO `C` DEL SIGILLO DEL COMMIT 2 ERA SBAGLIATO**
Quel braccio chiamava `decidi_divisione()` ### **FUORI dal passo**, dopo il ciclo dei 72, e
leggeva `soglia = 3π` ### **esatto su tutti gli archi** — da cui avevo concluso *«la modulazione
non agisce»*. ### **La conclusione era falsa, e la causa e' una riga:**

```
_r_nodo_mitosi():  r = getattr(self, "_r_corrente", None)
                   if r is None or len(r) < n:        # <-- QUI
                       self._tum_r_salti += 1
                       return np.ones(n)              # OROLOGIO UNIFORME
```
### **Il passo 72 ha partorito**, quindi `n` era cresciuto a `12812` mentre `_r_corrente` —
scritta da `step` **prima** della mitosi di quel passo — era lunga `12811`. ### **`len(r) < n` ➜
fallback a `np.ones` ➜ `grad_modula = 0` ➜ `soglia = soglia0` esatto.**
### ⚠ **E `_r_corrente` sta in `REGISTRO_DERIVATE` PROPRIO PER QUESTO** *(«la legge la trova GIA
RISCRITTA da `step`»)*: ### **il registro dichiarava che la sua lunghezza non e' un invariante, e
io l'ho ignorato.** ### **Stessa famiglia di `_smp_d0`: una grandezza valida SOLO DENTRO il passo.**

### ✅ **QUINDI QUI SI MISURA DENTRO LA DECISIONE**
Si avvolge `decidi_divisione` e si registra ### **al momento in cui decide, sullo stato su cui
decide**: la soglia locale degli archi in `sel`, il loro `|tw|`, le statistiche della soglia su
tutta la rete, e ### **il contatore `_tum_r_salti`, che DIMOSTRA se il fallback e' scattato.**

COMANDO:  python csv/_test_fork/_soglia_alla_divisione.py [--passi=72] [--seme=11]
USCITA:   `csv/_test_fork/_soglia_alla_divisione/_soglia_alla_divisione.json` + stdout.
"""
import contextlib
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

FUORI = os.path.join(RADICE, "csv", "_test_fork", "_soglia_alla_divisione")
SIM = os.path.join(RADICE, "soliton_simulator.py")


def blob(percorso):
    return hashlib.sha1(io.open(percorso, "rb").read()).hexdigest()


def carica(nome, seme):
    with contextlib.redirect_stdout(io.StringIO()):
        _S0, argv = _cli_flag.argv_del_driver(extra=["--seme=%d" % seme],
                                              dest=os.path.join(FUORI, "_scarto_cli"))
        S, a = _cli_flag.carica_dal_cli(list(argv), nome=nome)
        S._applica_regime(a)
        S._NMASSE_VIDEO["n"] = max(2, int(getattr(a, "nmasse", 2)))
        S._NMASSE_VIDEO["sep"] = float(getattr(a, "sep", 3.0))
        S._NMASSE_VIDEO["size"] = None
        S.avvia_test("MASSE-COERENTI")()
    return S, S.net


def principale():
    seme, passi = 11, 72
    for x in sys.argv[1:]:
        if x.startswith("--seme="):
            seme = int(x.split("=", 1)[1])
        elif x.startswith("--passi="):
            passi = int(x.split("=", 1)[1])
    if not os.path.isdir(FUORI):
        os.makedirs(FUORI)
    P = []

    def stampa(*x):
        r = " ".join(str(y) for y in x)
        P.append(r)
        print(r)

    stampa("=" * 104)
    stampa("LA SOGLIA LOCALE DOVE AVVENGONO LE DIVISIONI -- misurata DENTRO la decisione")
    stampa("=" * 104)
    stampa("simulatore ..... %s" % blob(SIM)[:8])
    stampa("questo strumento %s" % blob(os.path.abspath(__file__))[:8])
    stampa("seme %d   passi %d" % (seme, passi))
    stampa("")
    S, net = carica("soglia_div", seme)
    _cli_flag.dichiara_configurazione(S, stampa)
    stampa("")

    # ------------------------------------------------- la spia DENTRO la decisione
    dentro = []
    stato = {"passo": 0}
    vero_dec = net.decidi_divisione

    def dec_spia():
        salti_prima = int(getattr(net, "_tum_r_salti", 0))
        sel, perche = vero_dec()
        riga = {"passo": stato["passo"],
                "salti_r_prima": salti_prima,
                "salti_r_dopo": int(getattr(net, "_tum_r_salti", 0)),
                "n": int(net.n), "m": int(len(net.i)),
                # ⚠ MIO DIFETTO, e il run si e' fermato: `array or []` CHIAMA bool() su un
                #   array, e numpy SOLLEVA (<<the truth value of an array ... is ambiguous>>).
                #   Si guarda `is None`, che e' la sola domanda che si volesse fare.
                "len_r_corrente": (-1 if getattr(net, "_r_corrente", None) is None
                                   else int(len(net._r_corrente)))}
        if perche and "soglia" in perche:
            sg = np.asarray(perche["soglia"], float)
            av = np.asarray(perche["avv"], float)
            sopra = av >= sg
            riga.update({"soglia_min": float(sg.min()), "soglia_mediana": float(np.median(sg)),
                         "soglia_max": float(sg.max()),
                         "archi_sopra": int(sopra.sum()),
                         "avv_max": float(av.max())})
            if sel is not None and len(sel):
                riga["divisi"] = [{"arco": int(k), "tw": float(av[k]), "soglia": float(sg[k]),
                                   "sopra": bool(av[k] >= sg[k])} for k in sel]
                riga["somma_tw_divisi"] = float(np.sum(av[np.asarray(sel)]))
        dentro.append(riga)
        return sel, perche

    net.decidi_divisione = dec_spia

    # ------------------------------------------------- la spia sui confini di voce
    voci = []
    vero_ctrl = S._ferma_se_registro_incoerente

    def ctrl_spia(nt, dove, voce=None, comp=None):
        voci.append({"passo": stato["passo"], "voce": voce,
                     "S_tw": float(np.sum(np.abs(np.asarray(nt.tw, float)))),
                     "n": int(nt.n), "m": int(len(nt.i))})
        return vero_ctrl(nt, dove, voce=voce, comp=comp)

    S._ferma_se_registro_incoerente = ctrl_spia

    for k in range(1, passi + 1):
        stato["passo"] = k
        with contextlib.redirect_stdout(io.StringIO()):
            _passo.passo_pieno(S, net)
    S._ferma_se_registro_incoerente = vero_ctrl

    # ------------------------------------------------- il referto
    stampa("=" * 104)
    stampa("GLI ARCHI CHE SI DIVIDONO, con la LORO soglia locale")
    stampa("=" * 104)
    stampa("  %6s %10s %12s %12s %8s" % ("passo", "arco", "|tw|", "soglia loc.", "sopra?"))
    eventi = [r for r in dentro if r.get("divisi")]
    for r in eventi:
        for d in r["divisi"]:
            stampa("  %6d %10d %12.4f %12.4f %8s"
                   % (r["passo"], d["arco"], d["tw"], d["soglia"], d["sopra"]))
    tutti_sopra = all(d["sopra"] for r in eventi for d in r["divisi"])
    stampa("")
    stampa("  ### TUTTI gli archi divisi sono SOPRA la loro soglia locale: %s" % tutti_sopra)

    stampa("")
    stampa("=" * 104)
    stampa("LA SOGLIA SULLA RETE, a ogni decisione")
    stampa("=" * 104)
    sm = [r["soglia_min"] for r in dentro if "soglia_min" in r]
    sx = [r["soglia_max"] for r in dentro if "soglia_max" in r]
    sa = [r["archi_sopra"] for r in dentro if "archi_sopra" in r]
    salti = [r["salti_r_dopo"] - r["salti_r_prima"] for r in dentro]
    if sm:
        stampa("  soglia MINIMA sulla rete: da %.4f a %.4f   (3 pi = %.4f)"
               % (min(sm), max(sm), 3 * np.pi))
        stampa("  soglia MASSIMA sulla rete: da %.4f a %.4f" % (min(sx), max(sx)))
        stampa("  archi sopra la soglia locale: da %d a %d" % (min(sa), max(sa)))
        stampa("  ### LA MODULAZIONE AGISCE: se la soglia minima e' sotto 3 pi, `grad_modula`")
        stampa("      NON e' zero, e la soglia SCENDE dove il tempo proprio ha un gradiente.")
    stampa("")
    stampa("  ### IL FALLBACK DI `_r_nodo_mitosi` (l'orologio UNIFORME): scattato %d volte"
           % sum(salti))
    stampa("      su %d decisioni. Se e' ZERO, la soglia misurata qui e' quella VERA -- ed e'"
           % len(dentro))
    stampa("      la differenza col braccio C del sigillo, che chiamava la decisione FUORI dal")
    stampa("      passo, quando `len(_r_corrente) < n` e il fallback SCATTA.")

    stampa("")
    stampa("=" * 104)
    stampa("E LA VARIAZIONE DI sum|tw| NELLA VOCE `mitosi` E' ESATTAMENTE -sum|tw| DEI DIVISI?")
    stampa("=" * 104)
    per_passo = {}
    for i in range(1, len(voci)):
        if voci[i].get("voce") == "mitosi":
            per_passo[voci[i]["passo"]] = voci[i]["S_tw"] - voci[i - 1]["S_tw"]
    confronti = []
    for r in eventi:
        atteso = -r.get("somma_tw_divisi", 0.0)
        visto = per_passo.get(r["passo"])
        if visto is None:
            continue
        confronti.append({"passo": r["passo"], "atteso": atteso, "visto": visto,
                          "scarto": abs(visto - atteso)})
        stampa("  passo %3d: atteso %+12.4f   visto %+12.4f   scarto %.3e"
               % (r["passo"], atteso, visto, abs(visto - atteso)))
    quadra = all(c["scarto"] < 1e-6 for c in confronti) if confronti else False
    stampa("")
    stampa("  ### IL CONTO QUADRA: %s" % quadra)
    if quadra:
        stampa("      Quindi `TW-DIVISIONE-INCOGNITA` E' SCIOLTA: non c'era contraddizione,")
        stampa("      c'era una soglia misurata nel posto sbagliato.")

    fuori = {"blob_sim_sha1_byte": blob(SIM), "blob_strumento": blob(os.path.abspath(__file__)),
             "seme": seme, "passi": passi,
             "decisioni": len(dentro), "eventi": eventi,
             "tutti_i_divisi_sopra_soglia": bool(tutti_sopra),
             "soglia_min_fra_le_decisioni": (min(sm) if sm else None),
             "soglia_max_fra_le_decisioni": (max(sx) if sx else None),
             "archi_sopra_min": (min(sa) if sa else None),
             "archi_sopra_max": (max(sa) if sa else None),
             "fallback_r_scattato": int(sum(salti)),
             "confronti_sum_tw": confronti, "il_conto_quadra": bool(quadra),
             "tre_pi": float(3 * np.pi)}
    json.dump(fuori, io.open(os.path.join(FUORI, "_soglia_alla_divisione.json"), "w",
                             encoding="utf-8"), indent=1, ensure_ascii=False)
    io.open(os.path.join(FUORI, "_corsa.txt"), "w", encoding="utf-8").write(chr(10).join(P))
    stampa("")
    stampa("scritto: %s" % os.path.join(FUORI, "_soglia_alla_divisione.json"))
    return 0


if __name__ == "__main__":
    sys.exit(principale())
