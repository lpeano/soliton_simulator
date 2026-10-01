# -*- coding: utf-8 -*-
"""**IL SIGILLO DEL COMMIT 2 DEL RIORDINO: la DECISIONE separata dall'ESECUZIONE.**

**Criterio fissato dal piano PRIMA del codice** *(`doc/PIANO_riordino_mitosi.md`, parte (a))*:
### **deve restare IDENTICO AL BYTE — tutto: quali archi si dividono, quanti, e in quale ordine.**
*«La separazione decisione/esecuzione e' una RIORGANIZZAZIONE, non una cura.»*

| braccio | che cosa dimostra | che cosa lo fa FALLIRE |
|---|---|---|
| ### **`A`** | ### **byte-identico fino al passo 72** contro il blob di prima, ### **grandezze E CONTATORI** | **una** grandezza o **un** contatore diverso in **un** passo |
| ### **`B`** | ### **IL CASO CHE DEVE FALLIRE** (`P1-sexies`): un arco portato ### **sopra la sua soglia locale** deve ### **entrare nell'insieme dei sopra-soglia che `decidi_divisione` DICHIARA** | se l'insieme non cambia, ### **il `perche'` non descrive la decisione: la decora** |
| ### **`C`** | ### **LA MISURA CHE MI SERVE PER UNA CORREZIONE:** quanto vale la **soglia** DOVE AVVENGONO LE DIVISIONI, e il `|tw|` degli archi che si dividono ### **davvero** | niente: ### **e' una MISURA, non una prova** -- e il referto la riporta come tale |

### ⚠ **PERCHE' `B` NON MUOVE LA SOGLIA, come il piano diceva**
Il piano chiedeva *«si porta la soglia APPENA SOTTO il `|tw|` piu' alto fra gli archi che OGGI
stanno sotto soglia»*. ### **La soglia non ha un handle esterno:** nasce da `PHI_CRIT + π`
modulata dal gradiente, e ### **toccare `PHI_CRIT` cambia anche `ecc`, `pos_soglia`, `pos_tetto`**
— cioe' **tutto il criterio**, non la soglia.
### ➜ **Si fa la cosa equivalente e PIU' PULITA: si porta L'ARCO sopra la SUA soglia locale**, che
`decidi_divisione` ### **dichiara nel `perche'`.** ### **L'effetto misurato e' lo stesso** *(un
arco NOTO cambia lato)*, e ### **non si tocca nessuna costante di fisica.**
### ⚠ **E NON si prova su `sel`:** `prob` di un arco appena sopra soglia e' ### **minuscola**, e
un'estrazione casuale non e' un criterio. ### **Si prova sulla parte DETERMINISTICA**, che e'
quella che la separazione deve avere conservato.

COMANDO:  python csv/_seal_fork/_sig_decisione_separata.py [--passi=72]
USCITA:   0 se `A` e `B` passano; 1 altrimenti. Referto in
          `csv/_seal_fork/_sig_decisione_separata/`.
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

FUORI = os.path.join(RADICE, "csv", "_seal_fork", "_sig_decisione_separata")
SIM = os.path.join(RADICE, "soliton_simulator.py")
ANCORA = "decidi_divisione"
GRANDEZZE = ("d", "d0", "phi", "phi0", "phi_s", "phivel", "psi", "psi_spin", "eta", "tw", "twp",
             "vd", "peq", "mem_mot", "perc_chi", "perc_geom", "perc_tw", "omega_s", "_nb",
             "_nb_prec", "_psi_spinor", "_psi_prec", "_spinor_lift", "_rep")


def blob(percorso):
    return hashlib.sha1(io.open(percorso, "rb").read()).hexdigest()


def sim_prima(dest):
    """Il blob **PRIMA** del commit 2: il **PADRE** del commit che introduce `decidi_divisione`.

    ### **`H-P8`**: non si prende *«il codice di prima»* da `HEAD`, e non si fa `git cat-file` a
    mano: lo fa `_cli_flag.sim_prima_del_flag`, ### **che e' la funzione che il presidio
    riconosce.**
    """
    return _cli_flag.sim_prima_del_flag(ANCORA, dest, radice=RADICE)


def carica(sim, nome):
    with contextlib.redirect_stdout(io.StringIO()):
        _S0, argv = _cli_flag.argv_del_driver(extra=["--seme=11"],
                                              dest=os.path.join(FUORI, "_scarto_cli"))
        S, a = _cli_flag.carica_dal_cli(list(argv), nome=nome, sim=sim)
        S._applica_regime(a)
        S._NMASSE_VIDEO["n"] = max(2, int(getattr(a, "nmasse", 2)))
        S._NMASSE_VIDEO["sep"] = float(getattr(a, "sep", 3.0))
        S._NMASSE_VIDEO["size"] = None
        S.avvia_test("MASSE-COERENTI")()
    return S, S.net


def foto(net):
    q = {}
    for nome in GRANDEZZE:
        v = getattr(net, nome, None)
        if v is None:
            q[nome] = None
            continue
        a = np.asarray(v)
        if a.size == 0:
            q[nome] = ("vuota", list(a.shape))
            continue
        with np.errstate(invalid="ignore", over="ignore"):
            b = np.abs(a.astype(complex) if np.iscomplexobj(a) else a.astype(float))
            fin = np.isfinite(b)
            q[nome] = (list(a.shape),
                       float(np.sum(b[fin])) if fin.any() else 0.0,
                       float(np.max(b[fin])) if fin.any() else 0.0,
                       int(np.count_nonzero(~fin)))
    q["_n"] = int(net.n)
    q["_m"] = int(len(net.i))
    return q


def contatori(net):
    q = {}
    for k, v in sorted(vars(net).items()):
        if not k.startswith("_") or isinstance(v, bool):
            continue
        if isinstance(v, int):
            q[k] = int(v)
    q["negate"] = int(getattr(net, "negate", 0))
    return q


def diverse(a, b):
    return [(k, a.get(k), b.get(k)) for k in sorted(set(a) | set(b)) if a.get(k) != b.get(k)]


def principale():
    passi = 72
    for x in sys.argv[1:]:
        if x.startswith("--passi="):
            passi = int(x.split("=", 1)[1])
    if not os.path.isdir(FUORI):
        os.makedirs(FUORI)
    P = []

    def stampa(*x):
        r = " ".join(str(y) for y in x)
        P.append(r)
        print(r)

    stampa("=" * 104)
    stampa("IL SIGILLO DEL COMMIT 2: la DECISIONE separata dall'ESECUZIONE")
    stampa("=" * 104)
    PRIMA = os.path.join(FUORI, "_sim_prima_decisione.py")
    introduce = sim_prima(PRIMA)
    stampa("simulatore OGGI ..... %s" % blob(SIM)[:8])
    stampa("`%s` introdotto da %s" % (ANCORA, str(introduce)[:12]))
    stampa("blob PRIMA .......... %s   (estratto IN BINARIO, par.7)" % blob(PRIMA)[:8])
    # ⚠ IL CONTROLLO CHE IERI MANCAVA: il blob di PRIMA non deve contenere l'ancora.
    _t_prima = io.open(PRIMA, encoding="utf-8").read()
    _occ = _t_prima.count(ANCORA)
    stampa("occorrenze di `%s` nel blob di PRIMA: %d   %s"
           % (ANCORA, _occ, "<-- DEVE essere 0" if _occ else "(giusto)"))
    if _occ:
        stampa("  ### IL SIGILLO NON SI PUO' FARE: il <<codice di prima>> CONTIENE la cura.")
        stampa("      E' il difetto `SIM-PRIMA-STANTIO`, e qui e' un PRESIDIO.")
        return 1
    stampa("")
    _Sc, _netc = carica(None, "sig_c2_conf")
    _cli_flag.dichiara_configurazione(_Sc, stampa)
    stampa("")

    # ------------------------------------------------------------------ A
    stampa("=" * 104)
    stampa("BRACCIO A -- BYTE-IDENTICO fino al passo %d, grandezze E CONTATORI" % passi)
    stampa("=" * 104)
    SA, A = carica(PRIMA, "sig_c2_prima")
    SB, B = carica(None, "sig_c2_oggi")
    stampa("  n = %d / %d   archi = %d / %d" % (A.n, B.n, len(A.i), len(B.i)))
    primo, quante = None, 0
    soglie = []
    for k in range(1, passi + 1):
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                _passo.passo_pieno(SA, A)
                _passo.passo_pieno(SB, B)
        except Exception as e:
            stampa("  ### passo %d: ECCEZIONE %s -- %s"
                   % (k, type(e).__name__, str(e).split(chr(10))[0][:90]))
            return 1
        d = diverse(foto(A), foto(B))
        c = diverse(contatori(A), contatori(B))
        if d or c:
            quante += 1
            if primo is None:
                primo = {"passo": k, "grandezze": [x[0] for x in d],
                         "contatori": [{"nome": x[0], "prima": x[1], "oggi": x[2]} for x in c]}
                stampa("  ### passo %d: PRIMA DIFFERENZA -- %d grandezze (%s), %d contatori"
                       % (k, len(d), ", ".join(x[0] for x in d[:6]) or "nessuna", len(c)))
                for x in c[:8]:
                    stampa("      contatore `%s`: prima %s -> oggi %s" % x)
    ok_A = (primo is None)
    stampa("  ### A %s" % ("PASSA: %d passi, ZERO differenze -- grandezze E CONTATORI." % passi
                           if ok_A else "FALLISCE: %d passi su %d con differenze." % (quante,
                                                                                      passi)))

    # ------------------------------------------------------------------ C (misura)
    stampa("")
    stampa("=" * 104)
    stampa("BRACCIO C (MISURA, non prova) -- LA SOGLIA DOVE AVVENGONO LE DIVISIONI")
    stampa("=" * 104)
    sel, perche = B.decidi_divisione()
    mis = {}
    if perche and "soglia" in perche:
        sg = np.asarray(perche["soglia"], float)
        av = np.asarray(perche["avv"], float)
        pr = np.asarray(perche["prob"], float)
        sopra = av >= sg
        PHI = float(getattr(SB, "PHI_CRIT", 2 * np.pi))
        mis = {"soglia_min": float(sg.min()), "soglia_mediana": float(np.median(sg)),
               "soglia_max": float(sg.max()),
               "soglia_in_avvolgimenti": [float(sg.min() / PHI), float(sg.max() / PHI)],
               "archi_sopra_soglia": int(sopra.sum()), "archi": int(av.size),
               "avv_max": float(av.max()), "prob_max": float(pr.max()),
               "prob_max_sopra": (float(pr[sopra].max()) if sopra.any() else None),
               "avv_dei_sopra": ([float(x) for x in np.sort(av[sopra])[-10:]]
                                 if sopra.any() else []),
               "PHI_CRIT": PHI,
               "sel": (None if sel is None else [int(x) for x in sel])}
        stampa("  soglia: min %.6f  mediana %.6f  max %.6f   (in avvolgimenti: %.4f .. %.4f)"
               % (mis["soglia_min"], mis["soglia_mediana"], mis["soglia_max"],
                  mis["soglia_in_avvolgimenti"][0], mis["soglia_in_avvolgimenti"][1]))
        stampa("  archi SOPRA la soglia locale: %d su %d   |tw| max %.6f"
               % (mis["archi_sopra_soglia"], mis["archi"], mis["avv_max"]))
        stampa("  prob: max %.6e   fra i SOPRA-soglia: max %s"
               % (mis["prob_max"], mis["prob_max_sopra"]))
        if mis["avv_dei_sopra"]:
            stampa("  i |tw| piu' alti fra i sopra-soglia: %s"
                   % ["%.4f" % x for x in mis["avv_dei_sopra"]])
        stampa("  ### QUESTO E' IL NUMERO CHE MI SERVE: se la soglia qui vale ~%.2f, un arco con"
               % mis["soglia_mediana"])
        stampa("      |tw| fra 6.98 e 8.35 e' SOTTO soglia, e la mia spiegazione committata")
        stampa("      (<<la banda modulata scende a 6.597>>) NON REGGE su questa scena.")
    else:
        stampa("  `perche'` senza `soglia`: la rete non ha archi, o la decisione e' uscita subito.")

    # ------------------------------------------------------------------ B
    stampa("")
    stampa("=" * 104)
    stampa("BRACCIO B -- IL CASO CHE DEVE FALLIRE: un arco portato SOPRA la sua soglia locale")
    stampa("=" * 104)
    ok_B, datiB = False, {}
    if perche and "soglia" in perche:
        sg = np.asarray(perche["soglia"], float)
        av = np.asarray(perche["avv"], float)
        sopra = av >= sg
        if (~sopra).any():
            k = int(np.argmax(np.where(sopra, -1.0, av)))
            prima_sopra = bool(sopra[k])
            # ### si porta L'ARCO sopra la SUA soglia, non si muove la soglia.
            vecchio = float(B.tw[k])
            B.tw[k] = sg[k] * 1.000001
            _sel2, perche2 = B.decidi_divisione()
            sg2 = np.asarray(perche2["soglia"], float)
            av2 = np.asarray(perche2["avv"], float)
            sopra2 = av2 >= sg2
            dopo_sopra = bool(sopra2[k])
            n1, n2 = int(sopra.sum()), int(sopra2.sum())
            B.tw[k] = vecchio
            ok_B = (not prima_sopra) and dopo_sopra and (n2 == n1 + 1)
            datiB = {"arco": k, "tw_prima": vecchio, "soglia_locale": float(sg[k]),
                     "sopra_prima": prima_sopra, "sopra_dopo": dopo_sopra,
                     "quanti_sopra_prima": n1, "quanti_sopra_dopo": n2}
            stampa("  arco %d: |tw| %.6f, soglia locale %.6f" % (k, vecchio, sg[k]))
            stampa("  sopra-soglia PRIMA: %s   DOPO averlo portato a soglia*1.000001: %s"
                   % (prima_sopra, dopo_sopra))
            stampa("  quanti sopra soglia: %d -> %d   (atteso: +1 esatto)" % (n1, n2))
            stampa("  ### B %s" % ("PASSA: l'arco cambia lato, e `decidi_divisione` LO DICHIARA "
                                   "nel suo `perche'`."
                                   if ok_B else
                                   "FALLISCE: l'insieme dichiarato non e' cambiato come deve."))
        else:
            stampa("  ### B NON SI PUO' FARE: tutti gli archi sono sopra soglia.")
    else:
        stampa("  ### B NON SI PUO' FARE: `perche'` senza `soglia`.")

    stampa("")
    stampa("=" * 104)
    stampa("IL VERDETTO")
    stampa("=" * 104)
    for et, v in (("A", ok_A), ("B", ok_B)):
        stampa("  braccio %s ... %s" % (et, "PASSA" if v else "### FALLISCE"))
    stampa("  braccio C ... MISURA (non entra nel verdetto)")
    passa = ok_A and ok_B
    stampa("")
    stampa("### IL SIGILLO %s" % ("PASSA." if passa else "NON PASSA."))

    fuori = {"blob_sim_sha1_byte": blob(SIM), "blob_prima": blob(PRIMA),
             "introduce": str(introduce), "occorrenze_ancora_nel_prima": _occ,
             "passi": passi, "A": {"passa": ok_A, "passi_diversi": quante, "primo": primo},
             "B": {"passa": ok_B, "dati": datiB}, "C_misura": mis, "passa": passa}
    json.dump(fuori, io.open(os.path.join(FUORI, "_sig_decisione_separata.json"), "w",
                             encoding="utf-8"), indent=1, ensure_ascii=False)
    io.open(os.path.join(FUORI, "_corsa.txt"), "w", encoding="utf-8").write(chr(10).join(P))
    return 0 if passa else 1


if __name__ == "__main__":
    sys.exit(principale())
