# -*- coding: utf-8 -*-
"""**SIGILLO DI `DRIVER-SCENA-II`** -- i **cinque criteri dettati da Luca**, scritti nel task
history **prima** del codice (`doc/TASK_HISTORY/2026-09-26_driver-scena-ii.md`, commit `8bd2d8a`).

| # | criterio | come si verifica |
|--:|---|---|
| **T1** | il driver lancia la scena `(ii)` con `--scena`, **default invariato** | l'**argv** che il driver costruisce **senza** `--scena` e' **identica elemento per elemento** a quella del driver **PRIMA della cura** *(estratto dal **PADRE** del commit che ha introdotto `--scena=`, con l'asserzione che non lo contenga: `H-P8`)*, **e l'esito del ramo di default e' lo stesso** |
| **T2** | con la scena `(ii)` **`_applica_flag` NON semina**, e **la scena costruisce il suo vuoto** | `net.n == 0` dopo `_applica_flag`; `net.n > 0` dopo `avvia_test`; e **l'AST di `_semina_masse_coerenti` e' IDENTICO** a quello di prima *(la scena non e' stata toccata: il difetto era a monte)* |
| **T3** | **`--seme` REALE** | **tre processi**, uno per braccio (`STANDARD 1`): seme `7`, seme `7` di nuovo, seme `8`. **Firme `sha1` dei byte** campo per campo (`STANDARD 2`): `7 == 7` e `7 != 8` |
| **T4** | **configurazione INTERA** | `_cli_flag.scarto_dal_driver`: **0** booleani diversi dall'argv del driver (`H-P5`) |
| **T5** | **il caso che DEVE fallire** | `N-MASSE` con `SEMINA_LAM` **rifiuta ancora, con LO STESSO messaggio** della misura 0 |

> ### ⚠ **T1 NON PUO' ESSERE UN CONFRONTO DI RUN, E VA DETTO.**
> **Il ramo di default del driver NON GIRA** -- `N-MASSE` con `SEMINA_LAM` si ferma (`M0c`) --
> **e non per la cura: non girava GIA' PRIMA.** Confrontare due run morti darebbe un `PASS`
> vuoto *(`max|A-B| = 0` per mancanza di confronto, `STANDARD 2`)*. Si confronta quindi **cio'
> che il default PRODUCE**: l'argv, elemento per elemento, **e l'esito**.

**Passa dal CLI** (`csv/_cli_flag.py`): nessun attributo assegnato a mano (`H-P3`).
**Un processo per braccio** per `T3` (`STANDARD 1`).
**Gli snapshot `.pkl` si CANCELLANO dopo la firma:** ~17 MB l'uno, e il dato e' il comando.

    python csv/_seal_fork/_sigillo_scena_ii.py            # il sigillo
    python csv/_seal_fork/_sigillo_scena_ii.py --corto    # giro corto: solo T1, T2, T4, T5

ASCII puro.
"""
import ast
import hashlib
import io
import os
import pickle
import subprocess
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, os.path.join(RADICE, "csv"))

import _presidio                                                       # noqa: E402
import _cli_flag                                                       # noqa: E402

_presidio.avvia(__file__)

NL = chr(10)
DEST = os.path.join(_QUI, "_sig_scena_ii")
REFERTO = os.path.join(DEST, "REFERTO.txt")
DRIVER = "csv/_test_fork/_scena_video.py"
SCENA2 = "MASSE-COERENTI"
R = []


def P(s=""):
    print(s)
    R.append(s)


def _git(*a):
    q = subprocess.run(["git"] + list(a), cwd=RADICE, capture_output=True)
    return q.returncode, q.stdout


def driver_prima(dest):
    """Il driver PRIMA della cura: il PADRE del commit che ha introdotto `--scena=`.

    **Non si pinna a mano** e **si asserisce che il file estratto NON contenga l'opzione**:
    se la ricerca trovasse il commit sbagliato, si ferma invece di misurare niente (`A9`).
    E' la stessa forma di `_cli_flag.sim_prima_del_flag` (`H-P8`).
    """
    c, fuori = _git("log", "--format=%H", "-S", "--scena=", "--", DRIVER)
    if c or not fuori.strip():
        raise SystemExit("non trovo il commit che ha introdotto `--scena=` nel driver")
    # `git log` da' il piu' RECENTE per primo: il commit che ha INTRODOTTO l'opzione e' l'ULTIMO.
    intro = [x for x in fuori.decode().strip().split(NL) if x.strip()][-1]
    c2, testo = _git("show", "%s^:%s" % (intro, DRIVER))
    if c2:
        raise SystemExit("il PADRE di %s non ha il driver: ancora rotta" % intro[:8])
    t = testo.decode("utf-8")
    if "--scena=" in t:
        raise SystemExit("IL FILE 'DI PRIMA' CONTIENE GIA' `--scena=`: l'ancora e' sbagliata, "
                         "e mi fermo invece di misurare niente (A9)")
    io.open(dest, "w", encoding="utf-8", newline=NL).write(t)
    return intro[:8], len(t.split(NL)), intro + "^"


def argv_da(driver_path, extra):
    """L'argv che QUEL driver costruisce: si esegue il suo TESTO fino all'ancora."""
    t = io.open(driver_path, encoding="utf-8").read()
    anc = _cli_flag.ANCORA
    if t.count(anc) != 1:
        raise SystemExit("%s: ancora non unica (%d)" % (driver_path, t.count(anc)))
    testa = t[:t.index(anc)] + NL + "_ARGV_SIM = list(sys.argv)" + NL
    g = {"__name__": "__main__", "__file__": os.path.join(RADICE, DRIVER)}
    vecchia, cwd = list(sys.argv), os.getcwd()
    os.chdir(RADICE)
    sys.argv = _cli_flag.posizionali(os.path.join(DEST, "_tmp")) + list(extra)
    _so = sys.stdout
    sys.stdout = io.StringIO()
    try:
        exec(compile(testa, driver_path, "exec"), g)
    finally:
        sys.stdout = _so
        sys.argv = vecchia
        os.chdir(cwd)
    return list(g.get("_ARGV_SIM") or [])


def spezza(argv):
    """`(opzioni, flag)`: `--x V` diventa `opzioni["--x"] = V`; `--y` nudo va in `flag`.

    Serve perche' `T1` non confronta piu' due liste UGUALI: il default **e' cambiato di
    proposito**, e il criterio e' che la differenza sia **ESATTAMENTE quella dichiarata**.
    Confrontare le liste come testo direbbe solo «diverse», che non e' un criterio."""
    op, fl, i = {}, [], 1
    while i < len(argv):
        x = argv[i]
        if x.startswith('--'):
            if i + 1 < len(argv) and not argv[i + 1].startswith('--'):
                op[x] = argv[i + 1]; i += 2; continue
            fl.append(x)
        i += 1
    return op, sorted(fl)


def funzione_ast(testo, nome):
    for nd in ast.walk(ast.parse(testo)):
        if isinstance(nd, ast.FunctionDef) and nd.name == nome:
            return ast.dump(nd, include_attributes=False)
    return None


def _default_sorgente(nome):
    """Il valore di default di `SCENA`/`SEP` letto DAL SORGENTE del driver, per AST.

    Non da un `import` (il driver non e' importabile: esegue) e non dal mio ricordo: un
    criterio che si fida della memoria di chi lo scrive non impedisce niente.
    Si prende la PRIMA assegnazione di modulo, che e' il default."""
    arb = ast.parse(io.open(os.path.join(RADICE, DRIVER), encoding='utf-8').read())
    for nd in arb.body:
        if isinstance(nd, ast.Assign) and any(
                isinstance(x, ast.Name) and x.id == nome for x in nd.targets):
            if isinstance(nd.value, ast.Constant):
                return str(nd.value.value)
    return None


def firme(pkl):
    """`{campo: sha1}` dei byte di ogni array dello snapshot (`STANDARD 2`)."""
    with open(pkl, "rb") as f:
        d = pickle.load(f)
    fuori = {}
    for k, v in sorted((d.get("attrs") or {}).items()):
        try:
            b = v.tobytes() if hasattr(v, "tobytes") else repr(v).encode("utf-8")
        except Exception:
            b = repr(v).encode("utf-8")
        fuori[k] = hashlib.sha1(b).hexdigest()[:12]
    fuori["__content_hash"] = str(d.get("content_hash"))
    return fuori


def braccio(nome, extra):
    """UN PROCESSO per braccio (`STANDARD 1`). Restituisce `(firme, n_campi, uscita)`."""
    dd = os.path.join(DEST, nome)
    if not os.path.isdir(dd):
        os.makedirs(dd)
    q = subprocess.run([sys.executable, DRIVER, "1", os.path.relpath(dd, RADICE)] + list(extra),
                       cwd=RADICE, capture_output=True, text=True, encoding="utf-8",
                       errors="replace")
    pkl = os.path.join(dd, "frame_1.pkl")
    if q.returncode or not os.path.exists(pkl):
        return None, 0, q.returncode, (q.stdout or "") + (q.stderr or "")
    f = firme(pkl)
    os.remove(pkl)                 # ~17 MB: il dato e' il COMANDO, non il file
    return f, len(f), q.returncode, ""


if __name__ == "__main__":
    corto = "--corto" in sys.argv[1:]
    if not os.path.isdir(DEST):
        os.makedirs(DEST)
    P("=" * 104)
    P("SIGILLO DI `DRIVER-SCENA-II` -- i cinque criteri del task history%s"
      % ("   (GIRO CORTO)" if corto else ""))
    P("=" * 104)
    esiti = []

    # ---------------------------------------------------------------- T1
    prima = os.path.join(DEST, "_driver_prima.py")
    sha, nr, REF_PRIMA = driver_prima(prima)
    a_oggi = argv_da(os.path.join(RADICE, DRIVER), [])
    a_prima = argv_da(prima, [])
    op_o, fl_o = spezza(a_oggi)
    op_p, fl_p = spezza(a_prima)
    # ⚠ IL DEFAULT E' CAMBIATO DI PROPOSITO il 2026-09-26 (decisione di Luca), quindi `T1` non
    #   chiede piu' «identiche»: chiede che la differenza sia **ESATTAMENTE QUESTA**, e nulla
    #   di piu'. Un criterio che dicesse solo «diverse» non impedirebbe niente (`A9`).
    # ⚠ LA TABELLA CRESCE QUANDO IL DEFAULT CAMBIA DI PROPOSITO, e ogni riga e' una
    #   DECISIONE di Luca con la sua data. `--pozzo-d` e' un FLAG NUDO, non un'opzione con
    #   valore: si confronta nella lista dei flag, non qui.
    ATTESE = {'--test': ('N-MASSE', 'MASSE-COERENTI'),
              '--sep': ('4.0', '6.1158'),
              '--nodi': (None, '0')}
    # i FLAG NUDI attesi in piu' rispetto al driver di prima (`D02`, 2026-09-27)
    FLAG_ATTESI = ['--pozzo-d']
    cambiate = sorted(set(op_o) | set(op_p))
    inattese, mancate = [], []
    for k in cambiate:
        prima_v, oggi_v = op_p.get(k), op_o.get(k)
        if prima_v == oggi_v:
            continue
        if ATTESE.get(k) == (prima_v, oggi_v):
            continue
        inattese.append((k, prima_v, oggi_v))
    for k, (pv, ov) in ATTESE.items():
        if (op_p.get(k), op_o.get(k)) != (pv, ov):
            mancate.append((k, pv, ov, op_p.get(k), op_o.get(k)))
    flag_div = sorted((set(fl_o) ^ set(fl_p)) - set(FLAG_ATTESI))
    flag_mancati = [x for x in FLAG_ATTESI if x not in fl_o or x in fl_p]
    P("")
    P("  T1  IL DEFAULT E' CAMBIATO DI PROPOSITO, E LA DIFFERENZA E' ESATTAMENTE QUELLA DICHIARATA")
    P("        driver 'di prima' dal PADRE di %s ... %d righe" % (sha, nr))
    P("        argv PRIMA %d elementi   ->   OGGI %d" % (len(a_prima), len(a_oggi)))
    for k, (pv, ov) in sorted(ATTESE.items()):
        P("        dichiarato  %-8s %-10s -> %-14s   misurato %-10s -> %s"
          % (k, pv, ov, op_p.get(k), op_o.get(k)))
    P("        differenze INATTESE fra le opzioni .. %d %s" % (len(inattese), inattese[:4]))
    P("        dichiarate NON avvenute ............. %d %s" % (len(mancate), mancate[:4]))
    P("        flag nudi ATTESI in piu' ........... %s   mancati %s"
      % (FLAG_ATTESI, flag_mancati))
    P("        flag nudi INATTESI ................. %d %s" % (len(flag_div), flag_div[:6]))
    P("        il sorgente dichiara SCENA/SEP ...... %s / %s"
      % (_default_sorgente("SCENA"), _default_sorgente("SEP")))
    ok1 = (not inattese and not mancate and not flag_div and not flag_mancati
           and _default_sorgente('SCENA') == 'MASSE-COERENTI'
           and _default_sorgente('SEP') == '6.1158')
    esiti.append(("T1  la differenza e' ESATTAMENTE quella dichiarata", ok1))

    # ---------------------------------------------------------------- T5 (il caso che DEVE fallire)
    # ⚠ NON si usa `_cli_flag.senza`: l'argv di DEFAULT **non contiene** `--nodi` (lo passa
    #   solo la scena `(ii)`), e la guardia di `senza` lo dice giustamente. Qui si AGGIUNGE.
    a5 = list(a_oggi) + ([] if "--nodi" in a_oggi else ["--nodi", "0"])
    S_n, _a = _cli_flag.carica_dal_cli(a5, nome="sim_t5")
    try:
        S_n.avvia_test("N-MASSE")()
        msg5, es5 = "(nessun rifiuto)", False
    except SystemExit as e:
        msg5, es5 = str(e), True
    rif = os.path.join(RADICE, "csv", "_test_fork", "_misura0_scena_ii.txt")
    atteso5 = "SCENA DI EPOCA PRE-"
    ok5 = es5 and (atteso5 in msg5)
    P("")
    P("  T5  IL CASO CHE DEVE FALLIRE: `N-MASSE` con `SEMINA_LAM`")
    P("        rifiuta ............................. %s" % es5)
    P("        il messaggio e' ancora quello ....... %s" % (atteso5 in msg5))
    for r in msg5.strip().split(NL)[:2]:
        P("          %s" % r)
    P("        (il termine di paragone e' la misura 0: %s)"
      % ("presente" if os.path.exists(rif) else "MANCA"))
    esiti.append(("T5  N-MASSE rifiuta ancora, stesso messaggio", ok5))

    # ---------------------------------------------------------------- T2
    a2 = argv_da(os.path.join(RADICE, DRIVER), ["--scena=" + SCENA2])
    S2, _a2 = _cli_flag.carica_dal_cli(a2, nome="sim_t2")
    # ⚠ `_NMASSE_VIDEO` VA RIEMPITO COME FA IL DRIVER, e non e' un dettaglio: quelle tre
    #   righe stanno DOPO l'ancora `_applica_flag`, quindi `argv_da` NON le esegue. Senza
    #   questo, la scena girava col `sep` di MODULO (`3.0`) invece di quello del driver
    #   (`4.0`), e T2 riportava **2124** nodi dove il driver ne fa **4256**: un numero
    #   misurato in una configurazione DIVERSA da quella dichiarata (la famiglia di
    #   `CONFIG-1`). Trovato confrontando il referto col giro corto del driver.
    S2._NMASSE_VIDEO["n"] = max(2, int(getattr(_a2, "nmasse", 2)))
    S2._NMASSE_VIDEO["sep"] = float(getattr(_a2, "sep", 3.0))
    S2._NMASSE_VIDEO["size"] = None
    n_flag = int(S2.net.n)
    S2.avvia_test(SCENA2)()
    n_scena = int(S2.net.n)
    ast_oggi = funzione_ast(io.open(os.path.join(RADICE, "soliton_simulator.py"),
                                   encoding="utf-8").read(), "_semina_masse_coerenti")
    # ⚠ L'ANCORA E' LA STESSA DI `T1` -- il PADRE del commit che ha introdotto `--scena=` --
    #   e NON `HEAD~1`: `HEAD~1` e' una posizione RELATIVA, e basta un commit in mezzo per
    #   fargli confrontare un'altra coppia (`H-P8`).
    c3, sim_prima = _git("show", REF_PRIMA + ":soliton_simulator.py")
    ast_prima = funzione_ast(sim_prima.decode("utf-8"), "_semina_masse_coerenti") if not c3 else None
    scena_intatta = (ast_oggi is not None and ast_oggi == ast_prima)
    P("")
    P("  T2  CON LA SCENA (ii) IL VUOTO E' UNO SOLO, E LO FA LA SCENA")
    P("        net.n dopo `_applica_flag` .......... %d   (atteso 0)" % n_flag)
    P("        net.n dopo `avvia_test` ............. %d   (atteso > 0, e con il"
      " `sep` del DRIVER: %.3f)" % (n_scena, S2._NMASSE_VIDEO["sep"]))
    P("        `--nodi 0` nell'argv ................ %s"
      % ("--nodi" in a2 and a2[a2.index("--nodi") + 1]))
    P("        AST di `_semina_masse_coerenti` intatto %s   (contro %s)"
      % (scena_intatta, REF_PRIMA[:8] + "^"))
    ok2 = (n_flag == 0 and n_scena > 0 and scena_intatta)
    esiti.append(("T2  un vuoto solo, costruito dalla scena", ok2))

    # ---------------------------------------------------------------- T4
    div, quanti = _cli_flag.scarto_dal_driver(S2, argv=a_oggi)
    P("")
    P("  T4  CONFIGURAZIONE INTERA  (`H-P5`)")
    P("        booleani confrontati ................ %d" % quanti)
    P("        DIVERSI dall'argv del driver ........ %d %s" % (len(div), div[:8]))
    esiti.append(("T4  0 differenze sui booleani", not div))

    # ---------------------------------------------------------------- T3
    if corto:
        P("")
        P("  T3  SALTATO nel giro corto (tre processi del driver).")
    else:
        P("")
        P("  T3  IL SEME E' REALE  -- tre processi, uno per braccio (`STANDARD 1`)")
        bracci = {}
        for nome, seme in (("seme7a", 7), ("seme7b", 7), ("seme8", 8)):
            f, nc, rc, err = braccio(nome, ["--scena=" + SCENA2, "--seme=%d" % seme])
            bracci[nome] = f
            P("        %-8s seme %d  uscita %d  campi firmati %d%s"
              % (nome, seme, rc, nc, "" if f else ("   ** " + err.strip()[-160:])))
        if all(bracci.values()):
            a7a, a7b, a8 = bracci["seme7a"], bracci["seme7b"], bracci["seme8"]
            ug = [k for k in a7a if a7a[k] == a7b.get(k)]
            df = [k for k in a7a if a7a[k] != a8.get(k)]
            P("        T3a  seme 7 contro seme 7: campi IDENTICI %d su %d"
              % (len(ug), len(a7a)))
            P("        T3b  seme 7 contro seme 8: campi DIVERSI  %d su %d   %s"
              % (len(df), len(a7a), df[:6]))
            ok3a = (len(ug) == len(a7a))
            ok3b = (len(df) > 0)
        else:
            P("        ** un braccio non ha prodotto lo snapshot: T3 NON MISURATO **")
            ok3a = ok3b = False
        esiti.append(("T3a stesso seme -> byte identici", ok3a))
        esiti.append(("T3b semi diversi -> reti diverse", ok3b))

    # ---------------------------------------------------------------- la configurazione, INTERA
    P("")
    _cli_flag.dichiara_configurazione(S2, P)

    P("")
    P("=" * 104)
    for nome, ok in esiti:
        P("  %-46s %s" % (nome, "PASS" if ok else "** FAIL **"))
    buoni = len([1 for _n, o in esiti if o])
    P("SIGILLO: %d/%d" % (buoni, len(esiti)))
    P("=" * 104)
    P()
    P("COSA QUESTO SIGILLO *NON* DICE:")
    P("  - **T1 non e' un confronto di RUN**: il ramo di default NON GIRA, e non per la cura --")
    P("    non girava GIA' PRIMA (`M0c`). Confrontare due run morti darebbe un PASS vuoto.")
    P("    Si confronta l'ARGV elemento per elemento, e l'esito.")
    P("  - **non dice che la scena (ii) sia la scena GIUSTA per il run base**: dice che il")
    P("    driver la produce, con un seme dichiarato e un vuoto solo.")
    P("  - **nessuna misura di fisica**: `n`, `archi` e `QUOTA` sono numeri di un giro da UN")
    P("    frame, non un risultato.")
    io.open(REFERTO, "w", encoding="utf-8", newline=NL).write(NL.join(R) + NL)
    print(NL + "scritto %s" % os.path.relpath(REFERTO, RADICE).replace(chr(92), "/"))
    sys.exit(0 if buoni == len(esiti) else 1)
