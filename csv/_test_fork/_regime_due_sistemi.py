# -*- coding: utf-8 -*-
"""**`REGIME-DUE-SISTEMI`: di quanto differiscono i due sistemi che si chiamano allo stesso modo?**

**Mandato del guardiano del 2026-10-01**, dalla trappola trovata col **commit 0-bis**.

### IL FATTO, letto dal codice
| dove | che cosa fa |
|---|---|
| il **ramo di modulo** *(sempre eseguito)* | `_SCUOTIMENTO_REGIME = True` ### **in ENTRAMBI i rami** |
| `_applica_regime` *(solo se `--regime` e' passato)* | ### **`SCUOTIMENTO = False`** per il deterministico |

### ➜ **Due run che si chiamano ENTRAMBI <<regime deterministico>> non sono lo stesso sistema**, e
il vuoto acceso o spento ### **non e' un dettaglio: e' il termostato e la sorgente di asimmetria.**

### CHE COSA MISURA, e che cosa NON decide
Misura ### **di QUANTO** differiscono, passo per passo, sulle grandezze di stato **e sui
contatori** — lo stesso schema del braccio `B` del sigillo del controllo unico.
### ⚠ **Non decide la cura:** la differenza, grande o piccola, ### **non e' il problema.** Il
problema e' che ### **due sistemi diversi abbiano lo stesso nome**, e la misura serve solo a dire
### **se la via <<allineare `_applica_regime` al modulo>> butterebbe via un sistema che qualcuno ha
misurato** *(il braccio `O2` di `_sigillo_osservatore.py`)*.

### ⚠ IL SISTEMA DI RIFERIMENTO, dichiarato *(decisione di Luca)*
### **`REGIME` deterministico DAL MODULO, `SCUOTIMENTO = True`, SENZA `--regime`.** E' il braccio
`A` di questo confronto; il braccio `B` e' *«lo stesso nome, l'altro sistema»*.

COMANDO:  python csv/_test_fork/_regime_due_sistemi.py [--passi=72]
USCITA:   `csv/_test_fork/_regime_due_sistemi/_regime_due_sistemi.json` + stdout.
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

FUORI = os.path.join(RADICE, "csv", "_test_fork", "_regime_due_sistemi")
SIM = os.path.join(RADICE, "soliton_simulator.py")
GRANDEZZE = ("d", "d0", "phi", "phi0", "phi_s", "phivel", "psi", "psi_spin", "eta", "tw", "twp",
             "vd", "peq", "mem_mot", "perc_chi", "perc_geom", "perc_tw", "omega_s", "_nb",
             "_nb_prec", "_psi_spinor", "_psi_prec", "_spinor_lift")
CICLICHE = ("phi", "phi0", "phi_s")


def blob(percorso):
    return hashlib.sha1(io.open(percorso, "rb").read()).hexdigest()


def carica(nome, extra):
    """### ⚠ **IL PERCORSO DEL CLI HA TRE PASSI, E `carica_dal_cli` NE FA DUE.**

    **Difetto mio, e il primo run l'ha scoperto dando `0 differenze`:** `_cli_flag.carica_dal_cli`
    esegue `_cli()` e `_applica_flag(a)` — ### **le due funzioni che il driver chiama fino
    all'ancora** — ma ### **`_applica_regime` NON e' fra quelle**: il simulatore la chiama a
    `:11742`, **dopo**, nel suo punto d'ingresso. ### ➜ **Quindi passare `--regime` a
    `carica_dal_cli` NON FA NIENTE**, e il mio primo confronto ### **misurava due volte lo stesso
    sistema** — il che spiega lo `0` e lo rende ### **privo di significato, non rassicurante.**

    ### ✅ **La cura e' chiamare la funzione DEL SIMULATORE, come fa gia' `_osserva_vuoto.py`**
    *(`:283`: `S._applica_regime(arg)`)*. ### **Non e' configurare il modulo a mano** (`H-P3`): e'
    ### **completare il percorso del CLI** con la funzione che il percorso vero usa.
    *(E `_osserva_vuoto.py` lo fa **giusto**: l'ho verificato prima di sospettarlo.)*

    ⚠ **Con `extra` vuoto `_applica_regime` esce subito** *(nessun override)*, ### **ma si chiama
    su ENTRAMBI i rami**, cosi' i due percorsi sono **identici nella struttura** e la differenza
    puo' venire **solo** dal flag.
    """
    with contextlib.redirect_stdout(io.StringIO()):
        _S0, argv = _cli_flag.argv_del_driver(extra=["--seme=11"],
                                              dest=os.path.join(FUORI, "_scarto_cli"))
        S, a = _cli_flag.carica_dal_cli(list(argv) + list(extra), nome=nome)
        # ### IL TERZO PASSO DEL PERCORSO, che `carica_dal_cli` non fa.
        S._applica_regime(a)
        S._NMASSE_VIDEO["n"] = max(2, int(getattr(a, "nmasse", 2)))
        S._NMASSE_VIDEO["sep"] = float(getattr(a, "sep", 3.0))
        S._NMASSE_VIDEO["size"] = None
        S.avvia_test("MASSE-COERENTI")()
    return S, S.net


def foto(net, periodo):
    """Le grandezze, come scalari confrontabili: somma, massimo, e la forma."""
    fuori = {}
    for nome in GRANDEZZE:
        v = getattr(net, nome, None)
        if v is None:
            fuori[nome] = None
            continue
        a = np.asarray(v)
        if a.size == 0:
            fuori[nome] = {"forma": list(a.shape), "vuota": True}
            continue
        with np.errstate(invalid="ignore", over="ignore"):
            b = np.abs(a.astype(complex) if np.iscomplexobj(a) else a.astype(float))
            fin = np.isfinite(b)
            fuori[nome] = {"forma": list(a.shape),
                           "somma_assoluta": float(np.sum(b[fin])) if fin.any() else 0.0,
                           "massimo": float(np.max(b[fin])) if fin.any() else 0.0,
                           "non_finiti": int(np.count_nonzero(~fin))}
    fuori["_n"] = int(net.n)
    fuori["_m"] = int(len(net.i))
    return fuori


def contatori(net):
    q = {}
    for k, v in sorted(vars(net).items()):
        if not k.startswith("_g_") or isinstance(v, bool):
            continue
        if isinstance(v, int):
            q[k] = int(v)
    return q


def diverse(a, b):
    fuori = []
    for k in sorted(set(a) | set(b)):
        x, y = a.get(k), b.get(k)
        if x == y:
            continue
        fuori.append({"grandezza": k, "A": x, "B": y})
    return fuori


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
    stampa("REGIME-DUE-SISTEMI -- di quanto differiscono i due sistemi che hanno lo STESSO NOME")
    stampa("=" * 104)
    stampa("simulatore ..... %s" % blob(SIM)[:8])
    stampa("questo strumento %s" % blob(os.path.abspath(__file__))[:8])
    stampa("passi .......... %d" % passi)
    stampa("")

    SA, A = carica("regime_riferimento", [])
    SB, B = carica("regime_col_flag", ["--regime", "deterministico"])
    _cli_flag.dichiara_configurazione(SA, stampa)
    stampa("")
    stampa("=" * 104)
    stampa("I DUE SISTEMI, come li vede il modulo")
    stampa("=" * 104)
    quali = ("REGIME", "SCUOTIMENTO", "G_PH", "TAU_A", "_CALORE_INIT")
    stampa("  %-16s %-26s %-26s" % ("", "A = RIFERIMENTO (senza flag)", "B = col --regime"))
    scarti = {}
    for k in quali:
        va, vb = getattr(SA, k, None), getattr(SB, k, None)
        scarti[k] = {"A": va, "B": vb, "uguale": (va == vb)}
        stampa("  %-16s %-26s %-26s %s"
               % (k, va, vb, "" if va == vb else "### DIVERSO"))
    stampa("")
    stampa("  ### E' la TRAPPOLA `--regime`: lo STESSO nome di regime, DUE sistemi.")

    # --- il confronto passo per passo
    stampa("")
    stampa("=" * 104)
    stampa("IL CONFRONTO, PASSO PER PASSO")
    stampa("=" * 104)
    periodo = float(A._dphi())
    primo = None
    serie = []
    for k in range(1, passi + 1):
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                _passo.passo_pieno(SA, A)
                _passo.passo_pieno(SB, B)
        except Exception as e:
            stampa("  ### passo %d: ECCEZIONE %s -- %s"
                   % (k, type(e).__name__, str(e).split(chr(10))[0][:90]))
            return 1
        fa, fb = foto(A, periodo), foto(B, periodo)
        d = diverse(fa, fb)
        c = diverse(contatori(A), contatori(B))
        serie.append({"passo": k, "grandezze_diverse": len(d), "contatori_diversi": len(c),
                      "n_A": fa["_n"], "n_B": fb["_n"], "m_A": fa["_m"], "m_B": fb["_m"]})
        if (d or c) and primo is None:
            primo = {"passo": k, "grandezze": d[:8], "contatori": c[:8],
                     "quante_grandezze": len(d), "quanti_contatori": len(c)}
            stampa("  ### passo %d: PRIMA DIFFERENZA -- %d grandezze, %d contatori"
                   % (k, len(d), len(c)))
            for x in d[:6]:
                stampa("      `%s`: A %s" % (x["grandezza"], x["A"]))
                stampa("      %s  B %s" % (" " * (len(x["grandezza"]) + 2), x["B"]))

    fa, fb = foto(A, periodo), foto(B, periodo)
    finali = diverse(fa, fb)
    stampa("")
    stampa("=" * 104)
    stampa("LO STATO FINALE, al passo %d" % passi)
    stampa("=" * 104)
    stampa("  n: A %d  B %d      archi: A %d  B %d"
           % (fa["_n"], fb["_n"], fa["_m"], fb["_m"]))
    stampa("  grandezze con somma o massimo DIVERSI: %d su %d"
           % (len(finali), len(GRANDEZZE)))
    for x in finali[:10]:
        k = x["grandezza"]
        if isinstance(x["A"], dict) and isinstance(x["B"], dict):
            sa = x["A"].get("somma_assoluta")
            sb = x["B"].get("somma_assoluta")
            rel = (abs(sb - sa) / max(abs(sa), 1e-30)) if (sa is not None and sb is not None) \
                else float("nan")
            stampa("      %-14s somma|.| A %.6e  B %.6e   scarto relativo %.3e"
                   % (k, sa or 0.0, sb or 0.0, rel))
        else:
            stampa("      %-14s A %s   B %s" % (k, x["A"], x["B"]))

    stampa("")
    stampa("=" * 104)
    stampa("CHE COSA QUESTA MISURA DECIDE, e che cosa NON decide")
    stampa("=" * 104)
    if primo is None:
        stampa("  I due sistemi NON si distinguono su %d passi, su queste grandezze." % passi)
        stampa("  ### Allora la via (1) -- allineare `_applica_regime` al modulo -- NON butterebbe")
        stampa("      via nulla di misurato, perche' non c'e' nulla da misurare. ⚠ MA la via (2)")
        stampa("      RESTA PREFERIBILE: il problema non e' la grandezza della differenza, e' che")
        stampa("      DUE SISTEMI DIVERSI ABBIANO LO STESSO NOME.")
    else:
        stampa("  I due sistemi si separano al passo %d." % primo["passo"])
        stampa("  ### Allora la via (1) -- allineare `_applica_regime` al modulo -- BUTTEREBBE VIA")
        stampa("      UN SISTEMA CHE QUALCUNO HA MISURATO: il braccio `O2` di")
        stampa("      `_sigillo_osservatore.py` e' un A/B a variabile singola costruito PROPRIO su")
        stampa("      questa differenza. ### Resta la via (2): rinominare cio' che produce.")
    stampa("  ⚠ E I REFERTI PRODOTTI SUL SISTEMA `B` SI MARCANO, NON SI RISCRIVONO (par.9):")
    stampa("      csv/_test_fork/_sigillo_osservatore.py (braccio O2) e")
    stampa("      csv/_test_fork/_osserva_vuoto.py (flag --regime-det).")

    fuori = {"blob_sim_sha1_byte": blob(SIM), "blob_strumento": blob(os.path.abspath(__file__)),
             "passi": passi, "i_due_sistemi": scarti, "prima_differenza": primo,
             "serie": serie, "stato_finale_diverse": finali,
             "si_distinguono": bool(primo)}
    json.dump(fuori, io.open(os.path.join(FUORI, "_regime_due_sistemi.json"), "w",
                             encoding="utf-8"), indent=1, ensure_ascii=False)
    io.open(os.path.join(FUORI, "_corsa.txt"), "w", encoding="utf-8").write(chr(10).join(P))
    stampa("")
    stampa("scritto: %s" % os.path.join(FUORI, "_regime_due_sistemi.json"))
    return 0


if __name__ == "__main__":
    sys.exit(principale())
