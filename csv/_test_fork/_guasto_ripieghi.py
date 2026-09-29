# -*- coding: utf-8 -*-
"""**PROVA A GUASTO DEI RIPIEGHI: il COMPORTAMENTO, non la lettura.**

**Mandato del guardiano, 2026-09-28.** Tre volte una mia regola di classificazione ha **nascosto**
i siti che cercava *(`full(n,…)` contato come «estende», la condizione fusa chiamata
«inizializzazione», `==`/`!=` messi fuori dal mandato)*, e una quarta volta il mio strumento
leggeva **il ramo sbagliato** degli `IfExp`.

> ### **Quattro volte una LETTURA ha sbagliato. Questa prova non legge: GUASTA, e guarda.**

## La procedura, e ogni passo ha la sua ragione

| | |
|---|---|
| **1** | scena **GRANDE** -- `nmasse` e `sep` **DALL'ARGV, come fa il pilota** -- seme `11`, fino al **passo 30**: **prima di qualsiasi nascita**, cosi' lo stato BASE e' pulito. **Copia profonda, `net.rng` compreso** *(il generatore e' un attributo della rete: `:1976`)* |
| **2** | ### **l'elenco delle grandezze per nodo si trova IN AUTOMATICO**: ogni attributo della rete che allo stato BASE e' un array o una lista con `len == n`. ### ⚠ **`phi` si esclude e si DICHIARA:** `n` **E'** `len(phi)` *(property `:2063`)*, quindi accorciarla non accorcia una cache -- **cambia `n`** |
| **3** | ### **CONTROLLO**: dallo stato BASE **un passo due volte, da due copie**. Se non e' byte-identico ### **la prova NON VALE e si ferma** |
| **4** | per ogni grandezza, **due guasti da due copie fresche**: **CORTA** *(via l'ultimo elemento)* e **LUNGA** *(l'ultimo duplicato in coda)*, poi **un passo pieno** |
| **5** | ### **IL CASO CHE DEVE FALLIRE**: il guasto CORTO su `psi` sul blob **PRE-CURA** deve dare ### **RIPIEGO SILENZIOSO SU TUTTA LA RETE** -- e' il flash. **Se non risulta, la prova si ferma e lo dice** |

## I quattro esiti

| | |
|---|---|
| ### **PROTETTO** | solleva un errore **DICHIARATO** *(`CacheCorta`, `SchermaturaSpenta`, `LimiteNodiSuperato`, `ComposizioneNonValida`)* |
| **ROTTO RUMOROSO** | eccezione **non** dichiarata *(`IndexError`, `ValueError`…)*: col **tipo** e la **riga** |
| ### **RIPIEGO SILENZIOSO** | il passo **finisce**, e lo stato cambia. ### **Se cambia oltre l'ULTIMO nodo, l'effetto e' su TUTTA LA RETE** |
| **INERTE** | il passo finisce e **niente** cambia. ### **Si riporta, e NON vuol dire protetto** |

> ### 📌 **IL CRITERIO, fissato dal guardiano PRIMA dei numeri:** una grandezza e' **«a posto»**
> solo se **entrambi** i guasti danno **PROTETTO**, ### **oppure** se danno **INERTE** ed e'
> **DIMOSTRATO** che nessuna legge del passo la legge. **«Inerte» da solo non basta.**

## Due scelte di misura che vanno dette

1. **le grandezze PER ARCO si confrontano INTERE**, quelle **per nodo** sui **primi `n-1`**: cosi'
   un cambiamento su un nodo e' **per costruzione** un effetto **su qualcun altro**, non sul nodo
   che ho guastato io. *(Tagliare un array per arco a `n-1` avrebbe guardato `12801` archi su
   `471564`.)*
2. ### **la RIGA RESPONSABILE si TROVA, non si indovina:** per le grandezze che ripiegano in
   silenzio il passo si **rigira con un tracciatore** limitato alle funzioni della tabella
   generata, e si registra **quale delle righe elencate ha ESEGUITO**. *(E' misura, non lettura:
   e' il punto della prova.)*
3. ### **il confronto sanifica PRIMA della sottrazione, sotto `errstate`**, e `NaN` contro `NaN`
   conta **uguale**. *(Il simulatore impone `np.seterr(invalid='raise')` a `:8835`: sanificare
   dopo ha ucciso il primo giro dentro il CONTROLLO. E `invalid` scatta su `inf - inf`, non su un
   `nan` che passa -- quindi le grandezze **non finite** ora si **ELENCANO**.)*

COMANDO:  python csv/_test_fork/_guasto_ripieghi.py [--passi=30] [--salta-precura]
USCITA:   0 se il controllo tiene e il caso che deve fallire fallisce; 1 altrimenti.
"""
import copy
import hashlib
import io
import json
import os
import re
import sys
import traceback

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, os.path.join(RADICE, "csv"))
import _presidio  # noqa: E402

_presidio.avvia(__file__)
import numpy as np  # noqa: E402
import _cli_flag  # noqa: E402
import _passo  # noqa: E402

FUORI = os.path.join(RADICE, "csv", "_seal_fork", "_guasto_ripieghi")
TABELLA = os.path.join(RADICE, "doc", "RIPIEGHI_classi.md")
ANCORA_CURA = "_eredita_psi_figli"
# le 23 grandezze del sigillo, le stesse che confronta `_hashseed_prova.py`
GRANDEZZE = ("d", "d0", "phi", "phi0", "phi_s", "phivel", "psi", "psi_spin", "eta", "tw", "twp",
             "vd", "peq", "mem_mot", "perc_chi", "perc_geom", "perc_tw", "omega_s", "_nb",
             "_nb_prec", "_psi_spinor", "_psi_prec", "_spinor_lift")
# I METRI si escludono e si DICHIARANO: `phi` definisce `n` (property) e `i`/`j` definiscono `m`.
#   Accorciarli non accorcia una cache: CAMBIA IL BERSAGLIO, e il confronto perde il riferimento.
ESCLUSE = ("phi", "i", "j")
# CacheLunga E' NATA DOPO QUESTO STRUMENTO (`RIPIEGHI-ZERO`, 2026-09-29): senza aggiungerla qui
#   il lato LUNGA risultava ROTTO RUMOROSO mentre era PROTETTO, e il verdetto del criterio `A`
#   sarebbe stato FALSO. MISURATO: 23 grandezze su 23 etichettate male.
DICHIARATI_NOMI = ("CacheCorta", "CacheLunga", "SchermaturaSpenta", "LimiteNodiSuperato",
                   "ComposizioneNonValida")


def _t(x):
    return x if isinstance(x, str) else str(x)


# ---------------------------------------------------------------------------------------------
# I SITI DELLA TABELLA GENERATA: servono al TRACCIATORE, non al giudizio.
# ---------------------------------------------------------------------------------------------
def siti_della_tabella():
    """Legge `doc/RIPIEGHI_classi.md` e restituisce `{riga: (funzione, cache, classe)}`.

    **Non decide niente:** serve solo a sapere **quali righe guardare** col tracciatore.
    """
    q = {}
    if not os.path.isfile(TABELLA):
        return q
    for r in io.open(TABELLA, encoding="utf-8"):
        m = re.match(r"^\|\s*`:(\d+)`\s*\|\s*`([^`]*)`\s*\|\s*`([^`]*)`\s*\|"
                     r"\s*([A-Z]+)\s*\|\s*(.*?)\s*\|", r)
        if m:
            q[int(m.group(1))] = (m.group(2), m.group(3), m.group(5)[:60])
    return q


class Tracciatore(object):
    """Registra **quali** delle righe elencate hanno ESEGUITO durante un passo.

    Si limita alle funzioni che compaiono nella tabella: un tracciatore su tutto il simulatore
    a `n = 12802` non finisce.
    """

    def __init__(self, siti, file_sim):
        self.righe = set(siti)
        self.funzioni = {v[0] for v in siti.values()}
        self.base = os.path.basename(file_sim)
        self.viste = set()

    def globale(self, frame, evento, arg):
        if frame.f_code.co_name in self.funzioni \
                and os.path.basename(frame.f_code.co_filename) == self.base:
            return self.locale
        return None

    def locale(self, frame, evento, arg):
        if evento == "line" and frame.f_lineno in self.righe:
            self.viste.add(frame.f_lineno)
        return self.locale


# ---------------------------------------------------------------------------------------------
# LO STATO, E IL CONFRONTO
# ---------------------------------------------------------------------------------------------
def _foto(net):
    q = {}
    for k in GRANDEZZE:
        v = getattr(net, k, None)
        if v is None:
            continue
        try:
            q[k] = np.array(v, copy=True)
        except Exception:
            pass
    q["__n"] = int(net.n)
    q["__archi"] = int(len(net.i))
    return q


def _diff(xa, ya):
    """**La differenza: sotto `errstate`, e sanificando PRIMA -- non dopo.**

    ### Perche' esiste, ed e' un FALLIMENTO MISURATO il 2026-09-28
    Il simulatore imposta **`np.seterr(over='raise', divide='raise', invalid='raise')`** a
    `:8835`, **con gli invarianti ACCESI, che sono il default**. Io sanificavo con `nan_to_num`
    **DOPO** la sottrazione, cioe' **dopo** l'operazione che alza l'eccezione:
    ### **il primo giro e' morto nel CONTROLLO, e non per la fisica.**

    ### ⚠ **E `invalid` NON scatta su un `nan` che passa: scatta su `inf - inf`.** Quindi almeno
    una grandezza per nodo porta un `inf` -- e adesso ### **si ELENCA** *(`non_finiti`)* invece di
    far morire il confronto.

    **`NaN` contro `NaN` conta UGUALE:** e' lo **stesso stato**, non un cambiamento.
    """
    with np.errstate(all="ignore"):
        try:
            eq = np.asarray(xa == ya)
        except Exception:
            return None, 0.0
        try:
            eq = eq | (np.isnan(xa) & np.isnan(ya))
        except (TypeError, ValueError):
            pass
        diverso = ~eq
        try:
            fx = np.nan_to_num(xa.astype(complex), nan=0.0, posinf=0.0, neginf=0.0)
            fy = np.nan_to_num(ya.astype(complex), nan=0.0, posinf=0.0, neginf=0.0)
            s = float(np.abs(fx - fy).max()) if bool(diverso.any()) else 0.0
        except Exception:
            s = float("nan")
    return diverso, s


def non_finiti(net, elenco):
    """Quali grandezze portano `inf` o `nan`, e quanti. ### **Si ELENCA: e' un fatto sullo stato.**

    *(Il primo giro e' morto proprio su questo, senza dire quale grandezza fosse.)*
    """
    q = {}
    with np.errstate(all="ignore"):
        for k in list(elenco) + [x for x in GRANDEZZE if x not in elenco]:
            v = getattr(net, k, None)
            if v is None:
                continue
            try:
                arr = np.asarray(v)
                if arr.dtype.kind not in "fc":
                    continue
                q_inf, q_nan = int(np.sum(np.isinf(arr))), int(np.sum(np.isnan(arr)))
            except Exception:
                continue
            if q_inf or q_nan:
                q[k] = {"inf": q_inf, "nan": q_nan, "elementi": int(arr.size)}
    return q


def _confronta(a, b, n_nodi, n_archi):
    """Quante grandezze, quanti **nodi** e quanti **archi** cambiano, e lo scostamento massimo.

    **Per nodo:** i primi `n_nodi - 1`, cioe' **escludendo il nodo che ho guastato io**.
    **Per arco:** ### **tutti**, perche' un array per arco tagliato a `n_nodi` non e' guardato.
    """
    cambiate, nodi, archi, scost, forme = [], 0, 0, 0.0, []
    for k in sorted(set(a) | set(b)):
        if k.startswith("__"):
            continue
        x, y = a.get(k), b.get(k)
        if x is None or y is None:
            cambiate.append(k + "(assente)")
            continue
        per_arco = (len(x) == n_archi and n_archi != n_nodi)
        m = min(len(x), len(y)) if per_arco else min(len(x), len(y), max(0, n_nodi - 1))
        if m == 0:
            continue
        xa, ya = np.asarray(x[:m]), np.asarray(y[:m])
        if xa.shape != ya.shape:
            forme.append(k)
            cambiate.append(k + "(forma)")
            continue
        diverso, s = _diff(xa, ya)
        if diverso is None or not bool(diverso.any()):
            continue
        cambiate.append(k)
        scost = max(scost, s)
        ax = diverso.reshape(len(diverso), -1)
        quanti = int(np.sum(ax.any(axis=1)))
        if per_arco:
            archi = max(archi, quanti)
        else:
            nodi = max(nodi, quanti)
    return {"cambiate": cambiate, "quante": len(cambiate), "nodi": nodi, "archi": archi,
            "forme_diverse": forme, "scostamento_max": scost,
            "oltre_l_ultimo_nodo": bool(nodi or archi or forme)}


def _un_passo(S, net, tracciatore=None):
    import contextlib
    with contextlib.redirect_stdout(io.StringIO()):
        if tracciatore is not None:
            sys.settrace(tracciatore.globale)
        try:
            _passo.passo_pieno(S, net)
        finally:
            if tracciatore is not None:
                sys.settrace(None)


# ---------------------------------------------------------------------------------------------
# LA SCENA
# ---------------------------------------------------------------------------------------------
def carica(sim, passi):
    """La scena **GRANDE**: `nmasse` e `sep` **da `a`**, come fa il pilota."""
    import contextlib
    with contextlib.redirect_stdout(io.StringIO()):
        _S0, argv = _cli_flag.argv_del_driver(extra=["--seme=11"],
                                              dest=os.path.join(FUORI, "_scarto_cli"))
        S, a = _cli_flag.carica_dal_cli(list(argv), sim=sim,
                                        nome="sim_guasto_" + ("pre" if sim else "oggi"))
        S._NMASSE_VIDEO["n"] = max(2, int(getattr(a, "nmasse", 2)))
        S._NMASSE_VIDEO["sep"] = float(getattr(a, "sep", 3.0))
        S._NMASSE_VIDEO["size"] = None
        S.avvia_test("MASSE-COERENTI")()
        net = S.net
        for _ in range(passi):
            _passo.passo_pieno(S, net)
    return S, net


def per_nodo(net):
    """**L'elenco, trovato in automatico:** `len == n` **oppure `len == m`**, allo stato BASE.

    ### Perche' anche gli ARCHI, ed e' il criterio `D` del sigillo
    La prima stesura guardava **solo** `len == n`, quindi ### **le grandezze per ARCO non venivano
    guastate affatto** -- e il <<controllo positivo sugli archi>> del piano ### **non era coperto da
    nessuna misura.** *(Lo ha mostrato il primo giro del sigillo: `d` `d0` `peq` `tw` `twp` `vd`
    `_rep` non comparivano nella tabella.)*
    """
    n, m = int(net.n), int(len(net.i))
    q, sospette = [], []
    for k, v in sorted(vars(net).items()):
        if k in ESCLUSE:
            continue
        if not isinstance(v, (np.ndarray, list)):
            continue
        try:
            L = len(v)
        except Exception:
            continue
        if L not in (n, m):
            continue
        q.append(k)
        # ⚠ una grandezza PER ARCO potrebbe avere `len == n` per caso: si segnala.
        if n == m:
            sospette.append(k)
    return q, sospette


def _guasta(C, k, guasto):
    v = getattr(C, k)
    if isinstance(v, np.ndarray):
        setattr(C, k, v[:-1].copy() if guasto == "CORTA" else np.concatenate([v, v[-1:]]))
    else:
        setattr(C, k, list(v[:-1]) if guasto == "CORTA" else list(v) + [v[-1]])


def prova(S, net, elenco, foto_controllo, DICH, siti, file_sim, quali=None, eco=True):
    """I due guasti per ogni grandezza. Restituisce `{grandezza: {guasto: esito}}`."""
    n0, m0 = int(net.n), int(len(net.i))
    esiti = {}
    for k in (quali if quali is not None else elenco):
        riga = {}
        for guasto in ("CORTA", "LUNGA"):
            C = copy.deepcopy(net)
            try:
                _guasta(C, k, guasto)
            except Exception as e:
                riga[guasto] = {"esito": "NON GUASTABILE", "dettaglio": _t(e)[:90]}
                continue
            S.net = C
            try:
                _un_passo(S, C)
            except Exception as e:
                tb = traceback.extract_tb(sys.exc_info()[2])
                dove = "%s:%d" % (os.path.basename(tb[-1].filename), tb[-1].lineno) if tb else "?"
                riga[guasto] = {"esito": "PROTETTO" if isinstance(e, DICH) else "ROTTO RUMOROSO",
                                "tipo": type(e).__name__, "dove": dove,
                                "messaggio": _t(e).split(chr(10))[0][:110]}
                continue
            cc = _confronta(foto_controllo, _foto(C), n0, m0)
            riga[guasto] = {"esito": "RIPIEGO SILENZIOSO" if cc["quante"] else "INERTE"}
            riga[guasto].update(cc)
            # ### la riga responsabile si TROVA: si rigira il passo col tracciatore.
            if cc["quante"] and siti:
                D = copy.deepcopy(net)
                _guasta(D, k, guasto)
                S.net = D
                tr = Tracciatore(siti, file_sim)
                try:
                    _un_passo(S, D, tracciatore=tr)
                except Exception:
                    pass
                riga[guasto]["righe_eseguite"] = sorted(tr.viste)
                riga[guasto]["righe_responsabili"] = [
                    ":%d %s (%s) %s" % (r, siti[r][0], siti[r][1], siti[r][2])
                    for r in sorted(tr.viste) if siti[r][1].split(".")[-1] == k]
        esiti[k] = riga
        S.net = net
        if eco:
            def _s(g):
                r = riga.get(g, {})
                e = r.get("esito", "?")
                return e if e not in ("PROTETTO", "ROTTO RUMOROSO") \
                    else e + " (%s)" % r.get("tipo", "?")
            c = riga.get("CORTA", {})
            print("  %-24s %-24s %-24s %s"
                  % (k, _s("CORTA")[:24], _s("LUNGA")[:24],
                     ("%d gr / %d nodi / %d archi / %.2e" % (c.get("quante", 0), c.get("nodi", 0),
                                                             c.get("archi", 0),
                                                             c.get("scostamento_max", 0.0))
                      if c.get("esito") == "RIPIEGO SILENZIOSO" else "")))
    return esiti


def principale():
    passi, precura = 30, True
    for x in sys.argv[1:]:
        if x.startswith("--passi="):
            passi = int(x.split("=", 1)[1])
        elif x == "--salta-precura":
            precura = False
    if not os.path.isdir(FUORI):
        os.makedirs(FUORI)
    siti = siti_della_tabella()
    SIM_OGGI = os.path.join(RADICE, "soliton_simulator.py")
    BLOB = hashlib.sha1(io.open(SIM_OGGI, "rb").read()).hexdigest()

    S, net = carica(None, passi)
    DICH = tuple(c for c in (getattr(S, x, None) for x in DICHIARATI_NOMI) if isinstance(c, type))
    n0, m0 = int(net.n), int(len(net.i))
    print("simulatore ... soliton_simulator.py, blob sha1-BYTE %s" % BLOB[:8])
    print("scena ........ nmasse %d, sep %.4f  ->  n = %d, archi = %d   (dopo %d passi)"
          % (S._NMASSE_VIDEO["n"], S._NMASSE_VIDEO["sep"], n0, m0, passi))
    print("dichiarati ... %s" % ", ".join(c.__name__ for c in DICH))
    print("siti nella tabella generata (per il tracciatore): %d" % len(siti))
    print("")

    # ---- 2: l'elenco, in automatico -----------------------------------------------------
    elenco, sospette = per_nodo(net)
    print("=" * 108)
    print("GRANDEZZE PER NODO (len == n allo stato BASE), trovate IN AUTOMATICO: %d" % len(elenco))
    print("=" * 108)
    for k in elenco:
        print("  %-26s len %-8d %s" % (k, len(getattr(net, k)),
                                       "<== SOSPETTA: per ARCO con len == n per caso"
                                       if k in sospette else ""))
    print("")
    print("  ESCLUSA E DICHIARATA: `phi`. `n` E' `len(phi)` (property :2063): accorciarla non")
    print("  accorcia una cache, CAMBIA `n` -- e allora il confronto non avrebbe riferimento.")
    print("  SOSPETTE (per arco con len == n per caso): %s"
          % (", ".join(sospette) if sospette else "NESSUNA (n = %d != archi = %d)" % (n0, m0)))
    print("")
    nf = non_finiti(net, elenco)
    print("  NON FINITI allo stato BASE (`inf` o `nan`): %s" % ("NESSUNO" if not nf else ""))
    for k in sorted(nf):
        print("    %-26s inf %-8d nan %-8d su %d elementi"
              % (k, nf[k]["inf"], nf[k]["nan"], nf[k]["elementi"]))
    if nf:
        print("  ⚠ E' IL MOTIVO PER CUI IL PRIMO GIRO E' MORTO: `np.seterr(invalid='raise')`")
        print("    (:8835) e `inf - inf`. Ora si elenca e il confronto sanifica PRIMA.")
    print("")

    # ---- 3: il CONTROLLO ----------------------------------------------------------------
    print("=" * 108)
    print("CONTROLLO -- un passo DUE VOLTE da due copie di BASE: byte-identico?")
    print("=" * 108)
    A, B = copy.deepcopy(net), copy.deepcopy(net)
    S.net = A
    _un_passo(S, A)
    fa = _foto(A)
    S.net = B
    _un_passo(S, B)
    fb = _foto(B)
    S.net = net
    c = _confronta(fa, fb, n0, m0)
    print("  grandezze diverse: %d %s   scostamento max %.3e"
          % (c["quante"], c["cambiate"][:6], c["scostamento_max"]))
    if c["quante"]:
        print("  ### CONTROLLO FALLITO: LA PROVA NON VALE, e non si finge che valga.")
        io.open(os.path.join(FUORI, "_guasto_ripieghi.json"), "w", encoding="utf-8",
                newline=chr(10)).write(json.dumps(
                    {"vale": False, "controllo": c, "non_finiti_a_BASE": nf,
                     "motivo": "un passo da due copie di BASE non e' byte-identico"},
                    indent=1, ensure_ascii=False, default=float))
        return 1
    print("  ### CONTROLLO OK: il passo e' deterministico dalla copia, `net.rng` compreso.")
    print("")

    # ---- 4: i guasti --------------------------------------------------------------------
    print("=" * 108)
    print("I GUASTI: per ogni grandezza, CORTA e LUNGA da una copia FRESCA di BASE")
    print("=" * 108)
    print("  %-24s %-24s %-24s %s" % ("grandezza", "CORTA", "LUNGA", "(CORTA) che cambia"))
    esiti = prova(S, net, elenco, fa, DICH, siti, SIM_OGGI)

    # ---- il criterio del guardiano ------------------------------------------------------
    def _cl(f):
        return sorted(k for k, r in esiti.items() if f(r))

    def _uno(f):
        return sorted({k for k, r in esiti.items() for g in ("CORTA", "LUNGA")
                       if f(r.get(g, {}))})
    a_posto = _cl(lambda r: r.get("CORTA", {}).get("esito") == "PROTETTO"
                  and r.get("LUNGA", {}).get("esito") == "PROTETTO")
    inerti = _cl(lambda r: r.get("CORTA", {}).get("esito") == "INERTE"
                 and r.get("LUNGA", {}).get("esito") == "INERTE")
    silenzio = _uno(lambda r: r.get("esito") == "RIPIEGO SILENZIOSO")
    rumore = _uno(lambda r: r.get("esito") == "ROTTO RUMOROSO")
    tutta_rete = _uno(lambda r: r.get("nodi", 0) > 0 or r.get("archi", 0) > 0
                      or r.get("forme_diverse"))
    print("")
    print("=" * 108)
    print("IL CRITERIO (fissato dal guardiano PRIMA dei numeri)")
    print("=" * 108)
    print("  A POSTO -- PROTETTO su ENTRAMBI i guasti ....... %3d  %s" % (len(a_posto), a_posto))
    print("  INERTI su entrambi (NON <<a posto>>) ........... %3d  %s" % (len(inerti), inerti))
    print("  ### RIPIEGO SILENZIOSO ......................... %3d  %s" % (len(silenzio), silenzio))
    print("  ROTTO RUMOROSO ................................. %3d  %s" % (len(rumore), rumore))
    print("  ### EFFETTO OLTRE L'ULTIMO NODO (tutta la rete)  %3d  %s"
          % (len(tutta_rete), tutta_rete))
    print("")
    print("  ⚠ <<INERTE>> NON VUOL DIRE PROTETTO: vuol dire che in QUESTO passo nessuna legge")
    print("    l'ha letta. Per dirla <<a posto>> serve DIMOSTRARE che nessuna legge la legge.")
    print("")

    # ---- 5: IL CASO CHE DEVE FALLIRE ----------------------------------------------------
    esito_precura, fallito_come_deve = None, None
    if precura:
        print("=" * 108)
        print("IL CASO CHE DEVE FALLIRE -- `psi` CORTA sul blob PRE-CURA: deve essere il FLASH")
        print("=" * 108)
        PRECURA = os.path.join(FUORI, "_sim_precura.py")
        introduce = _cli_flag.sim_prima_del_flag(ANCORA_CURA, PRECURA)
        B_PRE = hashlib.sha1(io.open(PRECURA, "rb").read()).hexdigest()
        print("  `%s` introdotto da %s -> il PADRE e' il blob PRE-CURA %s"
              % (ANCORA_CURA, introduce[:8], B_PRE[:8]))
        if B_PRE == BLOB:
            print("  ### I DUE BLOB COINCIDONO: il caso che deve fallire NON E' FATTIBILE.")
            return 1
        Sp, netp = carica(PRECURA, passi)
        DICHp = tuple(c for c in (getattr(Sp, x, None) for x in DICHIARATI_NOMI)
                      if isinstance(c, type))
        np0, mp0 = int(netp.n), int(len(netp.i))
        print("  scena PRE-CURA: n = %d, archi = %d   (dopo %d passi)" % (np0, mp0, passi))
        Ap = copy.deepcopy(netp)
        Sp.net = Ap
        _un_passo(Sp, Ap)
        fap = _foto(Ap)
        Sp.net = netp
        ep = prova(Sp, netp, ["psi"], fap, DICHp, siti, PRECURA, quali=["psi"])
        esito_precura = ep.get("psi", {})
        cp = esito_precura.get("CORTA", {})
        fallito_come_deve = bool(cp.get("esito") == "RIPIEGO SILENZIOSO"
                                 and (cp.get("nodi", 0) > 1 or cp.get("archi", 0) > 0))
        print("")
        print("  esito: %s -- %d grandezze, %d nodi, %d archi, scostamento max %.3e"
              % (cp.get("esito", "?"), cp.get("quante", 0), cp.get("nodi", 0),
                 cp.get("archi", 0), cp.get("scostamento_max", 0.0)))
        for r in cp.get("righe_responsabili", []):
            print("  riga responsabile TROVATA col tracciatore: %s" % r)
        print("  ### %s" % ("IL CASO CHE DEVE FALLIRE FALLISCE COME DEVE: il ripiego silenzioso"
                            " su tutta la rete c'e'."
                            if fallito_come_deve else
                            "IL CASO CHE DEVE FALLIRE NON HA FALLITO: LA PROVA NON DIMOSTRA"
                            " NIENTE, e lo dico."))
        print("")

    OUT = os.path.join(FUORI, "_guasto_ripieghi.json")
    io.open(OUT, "w", encoding="utf-8", newline=chr(10)).write(json.dumps(
        {"blob_sim_sha1_byte": BLOB, "passi_base": passi, "n_base": n0, "archi_base": m0,
         "nmasse": S._NMASSE_VIDEO["n"], "sep": S._NMASSE_VIDEO["sep"],
         "errori_dichiarati": [c.__name__ for c in DICH], "vale": True,
         "grandezze_per_nodo": elenco, "sospette_per_arco": sospette, "escluse": list(ESCLUSE),
         "non_finiti_a_BASE": nf,
         "controllo": c, "esiti": esiti,
         "a_posto": a_posto, "inerti": inerti, "ripiego_silenzioso": silenzio,
         "rotto_rumoroso": rumore, "effetto_oltre_ultimo_nodo": tutta_rete,
         "caso_che_deve_fallire": {"fatto": bool(precura), "esito": esito_precura,
                                   "fallisce_come_deve": fallito_come_deve}},
        indent=1, ensure_ascii=False, default=float))
    print("scritto: " + OUT)
    return 0 if (not precura or fallito_come_deve) else 1


if __name__ == "__main__":
    sys.exit(principale())
