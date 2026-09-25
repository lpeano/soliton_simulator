# -*- coding: utf-8 -*-
"""**IL PERCORSO VERO DI UN FLAG: `argv` -> `_cli()` -> `_applica_flag()` -> MODULO.**

> ### **Un sigillo che imposta il modulo a mano prova LA LEGGE, non IL FLAG.**

E' il difetto misurato il 2026-09-25: `--semina-matura` e `--mitosi-2lam` erano **MORTI da riga
di comando** *(assegnazione in `esegui_headless`, `global` dichiarato in `_applica_flag`, quindi
una **locale silenziosamente inerte**)* e i loro sigilli **passavano ugualmente** `7/7` e `8/8`,
perche' accendevano il flag **sul modulo**. L'ha trovato il sigillo del driver, non i due sigilli.

**COSA OFFRE, e perche' sta in UN SOLO POSTO:**

* `argv_del_driver(extra)` -- **CATTURA** la `sys.argv` che il driver costruisce per il
  simulatore, eseguendo il **testo del driver** fino all'ancora `S._applica_flag(a)`.
  **Non la ricostruisce:** ricostruirla sarebbe **una SECONDA FORMULA per la stessa cosa**, ed e'
  l'errore che questo repo inseguue da giorni. *(Era il codice inline di
  `_sigillo_driver_accende.py`: qui e' fattorizzato, e quel sigillo ora lo usa.)*
* `senza(argv, opzione)` -- la stessa argv **MENO** un'opzione, con l'asserzione che ci fosse.
* `carica_dal_cli(argv, nome)` -- importa il simulatore in un modulo **privato** e lo configura
  **passando dal suo `_cli()`**, non assegnando attributi.

**PERCHE' IL BRACCIO OFF SI FA TOGLIENDO L'OPZIONE:** i flag delle cure sono `store_true`.
**`--semina-matura=off` NON ESISTE.** L'unico OFF che il CLI ammette e' *«un comando che
DIMENTICA il flag»* -- che e' anche, esattamente, il difetto contro cui il sigillo del driver
monta la guardia.

**⚠ E IL DRIVER NON PUO' DARE IL BRACCIO OFF DELLE CURE OBBLIGATORIE:** le accende
**incondizionatamente**, senza `if`. **E' `NUDA = CAMPAGNA`, di proposito.**

ASCII puro.
"""
import io
import os
import sys

NL = chr(10)
_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, ".."))
DRIVER = os.path.join(RADICE, "csv", "_test_fork", "_scena_video.py")
SIM = os.path.join(RADICE, "soliton_simulator.py")

# L'ANCORA: il punto del driver in cui i flag sono stati applicati e non un passo di fisica e'
# ancora partito. Si cerca nel TESTO INTERO e si pretende UNICA (`STANDARD 9`).
ANCORA = "S._applica_flag(a)"

# Gli argomenti che il driver prende PRIMA delle opzioni. `1` e' il numero di frame: il taglio
# all'ancora avviene molto prima che serva.
def posizionali(dest):
    return ["_scena_video.py", "1", dest]


def argv_del_driver(extra=None, dest=None):
    """Esegue il TESTO del driver fino all'ancora e restituisce `(S, argv_sim)`.

    `argv_sim` e' la `sys.argv` **che il driver ha costruito per il simulatore**, catturata
    aggiungendo UNA riga al testo eseguito -- non ricostruita.
    `S` e' il modulo del simulatore **gia' configurato dal driver**: utile per chi vuole
    leggere lo stato effettivo (e' cio' che fa `_sigillo_driver_accende.py`).
    """
    t = io.open(DRIVER, encoding="utf-8").read()
    assert t.count(ANCORA) == 1, "ancora non unica nel driver: %d" % t.count(ANCORA)
    testa = t[:t.index(ANCORA) + len(ANCORA)] + NL + "_ARGV_SIM = list(sys.argv)" + NL
    g = {"__name__": "__main__", "__file__": DRIVER}
    vecchia = list(sys.argv)
    cwd = os.getcwd()
    os.chdir(RADICE)
    sys.argv = posizionali(dest or os.path.join(_QUI, "_scarto_cli")) + list(extra or [])
    # Lo stdout del driver NON e' il referto di chi lo chiama: si CATTURA e si butta.
    import io as _io2
    _so = sys.stdout
    sys.stdout = _io2.StringIO()
    try:
        exec(compile(testa, DRIVER, "exec"), g)
    finally:
        sys.stdout = _so
        sys.argv = vecchia
        os.chdir(cwd)
    S = g.get("S") or sys.modules["soliton_simulator"]
    return S, list(g.get("_ARGV_SIM") or [])


def senza(argv, opzione):
    """La stessa argv MENO `opzione`, con l'asserzione che ci FOSSE.

    **L'asserzione e' il punto:** se un giorno il driver smettesse di passare quel flag, il
    braccio OFF diventerebbe **identico** al braccio ON e il sigillo passerebbe misurando
    NIENTE -- il falso PASS per mancanza di contrasto, gia' catalogato in `CLAUDE.md` par.9.
    """
    argv = list(argv)
    assert opzione in argv, ("l'argv del driver NON contiene %r: il braccio OFF sarebbe "
                            "IDENTICO all'ON, e il sigillo misurerebbe niente" % opzione)
    return [x for x in argv if x != opzione]


def argv_per(sim, argv):
    """L'argv FILTRATA sulle opzioni che QUEL simulatore dichiara, piu' le scartate.

    **Serve per il braccio «prima»:** il codice precedente a una cura **non conosce**
    l'opzione della cura, e passargliela farebbe morire `argparse` su un'opzione ignota.
    **E le opzioni note non si elencano a mano: si LEGGONO dal file** (`add_argument("--x"`),
    cioe' dalla stessa fonte che le dichiara.

    **Le SCARTATE si restituiscono perche' vanno nel referto:** dicono *quante e quali*
    opzioni il codice di prima non aveva, e se fossero piu' di quelle attese il confronto
    starebbe misurando anche altro. **Un filtro silenzioso sarebbe un difetto.**
    """
    import re
    noti = set(re.findall(r'add_argument\(\s*"(--[a-z0-9-]+)"',
                          io.open(sim, encoding="utf-8").read()))
    tenute, scartate = [], []
    for x in argv:
        if x.startswith("--") and x.split("=")[0] not in noti:
            scartate.append(x)
        else:
            tenute.append(x)
    return tenute, scartate


def carica_dal_cli(argv, nome="sim_cli", sim=None):
    """Importa il simulatore e lo configura **passando dal suo `_cli()`**.

    **Nessun attributo assegnato a mano:** si mette l'argv e si chiamano `_cli()` e
    `_applica_flag(a)`, cioe' **le due funzioni che il driver chiama**.
    Restituisce `(S, a)`.

    ⚠ **`_applica_flag` SEMINA ANCHE IL VUOTO** dal 2026-09-25 (`SCENA-1`:
    `net.semina(-1 if SEMINA_LAM else a.nodi)`). Non e' piu' una funzione di soli flag, e chi
    la chiama si ritrova un `S.net` gia' seminato: chi vuole un'altra scena si fa il proprio
    `S.Rete(...)`, come fa il driver stesso per le scene che non sono il vuoto.
    """
    import importlib.util as _iu
    sp = _iu.spec_from_file_location(nome, sim or SIM)
    S = _iu.module_from_spec(sp)
    sp.loader.exec_module(S)
    vecchia = list(sys.argv)
    sys.argv = list(argv)
    try:
        a = S._cli()
        S._applica_flag(a)
    finally:
        sys.argv = vecchia
    return S, a


def sim_prima_del_flag(nome_flag, dest, radice=None):
    """Estrae in BINARIO il simulatore **PRECEDENTE all'introduzione di `nome_flag`**.

    ### Perche' esiste, ed e' un difetto MISURATO il 2026-09-25
    I sigilli di `CURA 4` e `CURA 5` prendevano il codice «di prima» da
    **`HEAD:soliton_simulator.py`**. Era giusto **finche' la cura non era committata**;
    **dal commit della cura in poi HEAD LA CONTIENE**, e il braccio «prima» e' diventato
    **il braccio OFF di se stesso**: un confronto che passa per costruzione.
    **Non era vacuo quando e' stato scritto: LO E' DIVENTATO**, ed e' esattamente la
    famiglia di `T1` (`CLAUDE.md` par.0: *un criterio SCADUTO che confrontava il disco di
    OGGI con un blob di tre giorni fa*), curata nello stesso modo: **si ancora alla COPPIA
    DI BLOB CHE RACCHIUDE IL CAMBIAMENTO.**

    **E NON SI PINNA A MANO:** il commit che ha introdotto il flag si TROVA
    (`git log -S<flag>`, la voce piu' vecchia) e si prende **il suo PADRE**.
    **POI SI ASSERISCE CHE IL FILE ESTRATTO NON CONTENGA IL FLAG** -- e' il presidio che
    rende l'ancora auto-denunciante: se un giorno il flag comparisse prima, o se la ricerca
    trovasse il commit sbagliato, **si ferma invece di misurare niente** (`A9`).
    """
    import subprocess
    rad = radice or RADICE
    q = subprocess.run(["git", "log", "-S", nome_flag, "--format=%H", "--",
                        "soliton_simulator.py"], cwd=rad, capture_output=True, text=True)
    assert q.returncode == 0, q.stderr[:300]
    righe = [r.strip() for r in (q.stdout or "").split(NL) if r.strip()]
    assert righe, "nessun commit introduce %r in soliton_simulator.py" % nome_flag
    introduce = righe[-1]                      # la voce piu' VECCHIA: l'introduzione
    g = subprocess.run(["git", "cat-file", "-p", introduce + "^:soliton_simulator.py"],
                       cwd=rad, capture_output=True)
    assert g.returncode == 0, g.stderr[:300]
    byte = g.stdout
    # ⚠ IL PRESIDIO CHE RENDE L'ANCORA AUTO-DENUNCIANTE
    assert nome_flag.encode() not in byte, (
        "il codice estratto (%s^) CONTIENE GIA' %r: l'ancora e' sbagliata e il confronto "
        "misurerebbe NIENTE" % (introduce[:8], nome_flag))
    io.open(dest, "wb").write(byte)
    return introduce


def _booleani(S):
    return sorted(k for k, v in vars(S).items() if isinstance(v, bool) and k.isupper())


_CACHE_DRV = []          # il modulo di riferimento, caricato UNA VOLTA per processo


def scarto_dal_driver(S, argv=None):
    """I booleani di modulo in cui `S` DIFFERISCE dalla configurazione del DRIVER.

    Restituisce `(diverse, quanti_confrontati)`. **Il termine di paragone si costruisce
    caricando il simulatore con l'argv VERA del driver**, non da un elenco a mano: una cura
    nuova entra da se'.
    **Si calcola UNA VOLTA per processo** (`_CACHE_DRV`), perche' costa un `exec` del driver.
    """
    if not _CACHE_DRV:
        if argv is None:
            _S0, argv = argv_del_driver([])
        Sd, _ = carica_dal_cli(list(argv) + ["--nodi", "0"], nome="cfg_drv_p5")
        _CACHE_DRV.append(Sd)
    Sd = _CACHE_DRV[0]
    nomi = _booleani(Sd)
    div = [k for k in nomi if bool(getattr(S, k, None)) != bool(getattr(Sd, k))]
    return div, len(nomi)


def dichiara_configurazione(S, stampa, esenzione=None):
    """**`P5`: un referto dichiara LA CONFIGURAZIONE INTERA, non i flag che ho toccato.**

    *(Decisione di Luca, 2026-09-25, dopo `CONFIG-1`: sei misure erano state prese con
    **28 leggi su 31 spente** — `FORK_SU2`, `CAMPO_SPINORIALE`, `CS_DINAMICO`… — e ogni
    referto dichiarava solo i **quattro flag che avevo acceso io**. **Il flag era acceso, e
    intorno a lui il sistema era spento.**)*

    `stampa` e' la funzione con cui il referto scrive una riga (il solito `P`).
    **Restituisce `True` se la configurazione E' quella del driver.**

    ⚠ **Non dice «i flag sono giusti»: dice DOVE SI E' MISURATO.** Una misura fuori
    configurazione non e' sbagliata — e' **la misura di un altro sistema** — e va letta cosi'.
    """
    div, quanti = scarto_dal_driver(S)
    stampa("=" * 100)
    stampa("LA CONFIGURAZIONE INTERA (`P5`) -- non i flag toccati, TUTTI")
    stampa("=" * 100)
    stampa("  booleani di modulo confrontati con l'argv del DRIVER: %d" % quanti)
    if not div:
        stampa("  -> IN CONFIGURAZIONE DEL DRIVER: nessuna differenza. ZERO su %d." % quanti)
    else:
        stampa("  -> FUORI CONFIGURAZIONE DEL DRIVER: %d differenze su %d" % (len(div), quanti))
        for k in div:
            stampa("       %-26s qui %-6s   driver %s"
                   % (k, bool(getattr(S, k, None)), bool(getattr(cache_driver(), k))))
        if esenzione:
            stampa("  ESENZIONE DICHIARATA: %s" % esenzione)
    stampa("")
    return not div


def cache_driver():
    """Il modulo di riferimento (configurazione del driver), gia' caricato."""
    return _CACHE_DRV[0]


def esigi_configurazione(S, stampa, esenzione=None):
    """**FUORI CONFIGURAZIONE DEL DRIVER SI FERMA** (decisione di Luca), salvo esenzione.

    **Perche' e' uno STOP e non un avviso** (`A9`): un avviso in cima a un referto lungo
    **non impedisce niente**, e `CONFIG-1` e' successo **con gli avvisi al loro posto** —
    dichiaravo i flag accesi e la misura era di un altro sistema comunque.
    **L'esenzione resta possibile ma obbliga a DICHIARARE**, come `[SENZA-RELAZIONE]`.
    """
    ok = dichiara_configurazione(S, stampa, esenzione)
    if not ok and not esenzione:
        stampa("STOP: misura FUORI configurazione del driver e senza esenzione dichiarata.")
        raise SystemExit(3)
    return ok


def dichiara(S, nomi):
    """Le righe `STATO <nome> <valore>` per i flag richiesti, lette DAL MODULO."""
    return [(n, getattr(S, n, "ASSENTE")) for n in nomi]
