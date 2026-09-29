# -*- coding: utf-8 -*-
"""**IL SIGILLO DEL CONTROLLO UNICO DELLO SCHEDULATORE** *(`RIPIEGHI-ZERO`, 2026-09-29)*.

**Criteri fissati da Luca PRIMA del codice** *(piano `f684353f`, par.5)*. I bracci `A` e `D` li
ha girati `csv/_test_fork/_guasto_ripieghi.py`; qui stanno **`B`**, **`C`** ed **`E`**, e il
**riepilogo** cita `A`/`D` dal loro referto committato.

| braccio | che cosa dimostra | che cosa lo fa FALLIRE |
|---|---|---|
| **`A`** *(altrove)* | la prova a guasto da' **PROTETTO su CORTA e LUNGA** per **tutte** le grandezze di **STATO** | un solo `INERTE`, `ROTTO RUMOROSO` o `RIPIEGO SILENZIOSO` su una voce di STATO |
| **`D`** *(altrove)* | **controllo positivo sugli ARCHI**: anche le 7 per arco sono protette | un `INERTE` o un ripiego su una per arco |
| ### **`B`** | ### **byte-identico fino al passo 72** contro il blob **PRE-CONTROLLO**, sul **dominio comune** | **una** grandezza diversa in **un** passo |
| ### **`C`** | ### **IL CASO CHE DEVE FALLIRE** (`P1-sexies`): col controllo **SPENTO**, i guasti tornano a **NON** essere protetti | se restano protetti anche a controllo spento, ### **il sigillo non sta misurando il controllo** |
| ### **`E`** | un run **SANO CON NASCITE** arriva al **72** ### **senza un solo `CacheCorta`/`CacheLunga`** | un solo errore: vuol dire che ho messo una **DERIVATA** fra le STATO |
| ### **`F`** | ### **il RENDICONTO DELLA TOLLERANZA** *(punto 2 di Luca)*: **quali** grandezze di STATO non si sono **MAI** viste piene | ### **anche UNA SOLA**: la tolleranza dell'assenza diventerebbe un **varco**, e quella grandezza resterebbe fuori dal controllo **per sempre, in silenzio** |

### ⚠ Due scelte di misura, dichiarate prima dei numeri

1. **`B` confronta PASSO PER PASSO**, non solo alla fine: ### **il primo passo in cui qualcosa
   cambia e' l'informazione**, e una somma finale la nasconderebbe. *(E' il braccio `E` di
   `PSI-FLASH` che ho sbagliato una volta sommando su domini diversi.)*
2. **il blob PRE-CONTROLLO si estrae con `git cat-file -p` IN BINARIO** *(par.7: **non**
   `git checkout`, per la trappola CRLF)*, e si mette **accanto ai dati**.

COMANDO:  python csv/_seal_fork/_sig_controllo_unico.py [--passi=72] [--prima=<sha>]
USCITA:   0 se TUTTI i bracci passano; 1 altrimenti.
"""
import copy
import hashlib
import io
import json
import os
import subprocess
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))   # il sigillo sta in csv/_seal_fork/: DUE livelli
sys.path.insert(0, os.path.join(RADICE, "csv"))
import _presidio  # noqa: E402

_presidio.avvia(__file__)
import numpy as np  # noqa: E402
import _cli_flag  # noqa: E402
import _passo  # noqa: E402

FUORI = os.path.join(RADICE, "csv", "_seal_fork", "_sig_controllo_unico")
SIM = os.path.join(RADICE, "soliton_simulator.py")
# il blob PRE-CONTROLLO: l'ultimo prima del controllo unico. **Non e' un hash scelto a mano:** e'
#   il PADRE del commit che introduce `_ferma_se_registro_incoerente`, e si ricava da git.
ANCORA_CONTROLLO = "_ferma_se_registro_incoerente"
GRANDEZZE = ("d", "d0", "phi", "phi0", "phi_s", "phivel", "psi", "psi_spin", "eta", "tw", "twp",
             "vd", "peq", "mem_mot", "perc_chi", "perc_geom", "perc_tw", "omega_s", "_nb",
             "_nb_prec", "_psi_spinor", "_psi_prec", "_spinor_lift")
REFERTO_A = os.path.join(RADICE, "csv", "_seal_fork", "_guasto_ripieghi", "_guasto_ripieghi.json")


def _t(x):
    return x if isinstance(x, str) else x.decode("utf-8", "replace")


def blob(percorso):
    return hashlib.sha1(io.open(percorso, "rb").read()).hexdigest()


def sim_prima_del_controllo(dest):
    """Estrae il simulatore **PRIMA** del controllo unico, **passando da `_cli_flag`**.

    ### Perche' NON lo estraggo a mano, ed e' il presidio `H-P8` che me l'ha impedito
    La prima stesura faceva `git cat-file -p <introduce>^:soliton_simulator.py` da se'.
    ### **`H-P8` l'ha RIFIUTATA, e aveva ragione**: `_cli_flag.sim_prima_del_flag` fa la stessa
    cosa **ancorando al PADRE del commit che introduce l'ancora**, ed e' la funzione che il
    presidio riconosce. ### **Meno codice e un presidio in piu', invece di uno aggirato.**
    *(Il difetto che `H-P8` esiste per impedire: `ANCORE-1`, **25 sigilli** che prendevano <<il
    codice di prima>> da `HEAD` e diventavano VUOTI appena la cura era committata.)*
    """
    return _cli_flag.sim_prima_del_flag(ANCORA_CONTROLLO, dest, radice=RADICE)


def carica(sim, extra_sim=None):
    """La scena **GRANDE**: `nmasse` e `sep` **da `a`**, come fa il pilota."""
    import contextlib
    with contextlib.redirect_stdout(io.StringIO()):
        _S0, argv = _cli_flag.argv_del_driver(extra=["--seme=11"],
                                              dest=os.path.join(FUORI, "_scarto_cli"))
        S, a = _cli_flag.carica_dal_cli(list(argv) + list(extra_sim or []),
                                        nome="sig_cu_%s" % (abs(hash((sim, tuple(extra_sim or ()))))
                                                            % 99991),
                                        sim=sim)
        S._NMASSE_VIDEO["n"] = max(2, int(getattr(a, "nmasse", 2)))
        S._NMASSE_VIDEO["sep"] = float(getattr(a, "sep", 3.0))
        S._NMASSE_VIDEO["size"] = None
        S.avvia_test("MASSE-COERENTI")()
    return S, S.net


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
    q["__m"] = int(len(net.i))
    return q


def _diverse(a, b):
    """Le grandezze diverse **sul DOMINIO COMUNE**, con lo scostamento massimo."""
    fuori = []
    with np.errstate(all="ignore"):
        for k in sorted(set(a) | set(b)):
            if k.startswith("__"):
                continue
            x, y = a.get(k), b.get(k)
            if x is None or y is None:
                fuori.append((k, "assente", 0.0))
                continue
            L = min(len(x), len(y))
            xa, ya = np.asarray(x[:L]), np.asarray(y[:L])
            if xa.shape != ya.shape:
                fuori.append((k, "forma %s vs %s" % (xa.shape, ya.shape), 0.0))
                continue
            try:
                uguale = np.array_equal(xa, ya, equal_nan=True)
            except TypeError:
                uguale = np.array_equal(xa, ya)
            if uguale:
                continue
            try:
                d = np.abs(np.nan_to_num(xa.astype(complex), nan=0.0, posinf=0.0, neginf=0.0)
                           - np.nan_to_num(ya.astype(complex), nan=0.0, posinf=0.0, neginf=0.0))
                s = float(d.max())
            except Exception:
                s = float("nan")
            fuori.append((k, "valori", s))
    return fuori


def braccio_B(passi, prima):
    """**Byte-identico fino al passo `passi`, PASSO PER PASSO, sul dominio comune.**"""
    import contextlib
    print("=" * 104)
    print("BRACCIO B -- BYTE-IDENTICO fino al passo %d contro il blob PRE-CONTROLLO" % passi)
    print("=" * 104)
    SA, netA = carica(prima)
    SB, netB = carica(None)
    print("  PRIMA: %s   OGGI: %s" % (blob(prima)[:8], blob(SIM)[:8]))
    print("  n = %d / %d   archi = %d / %d" % (netA.n, netB.n, len(netA.i), len(netB.i)))
    primo, quante = None, 0
    for k in range(1, passi + 1):
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                _passo.passo_pieno(SA, netA)
                _passo.passo_pieno(SB, netB)
        except Exception as e:
            print("  ### passo %d: ECCEZIONE %s -- %s" % (k, type(e).__name__,
                                                          str(e).split(chr(10))[0][:90]))
            return False, {"passo": k, "eccezione": type(e).__name__,
                           "messaggio": str(e)[:400]}
        d = _diverse(_foto(netA), _foto(netB))
        if d:
            quante += 1
            if primo is None:
                primo = {"passo": k, "grandezze": [x[0] for x in d],
                         "scostamento_max": max(x[2] for x in d)}
                print("  ### passo %d: PRIMA DIFFERENZA -- %d grandezze: %s   scost. max %.3e"
                      % (k, len(d), ", ".join(x[0] for x in d[:6]), primo["scostamento_max"]))
    if primo is None:
        print("  ### B PASSA: %d passi, ZERO differenze in ogni passo." % passi)
        return True, {"passi": passi, "passi_diversi": 0}
    print("  ### B FALLISCE: %d passi su %d con differenze." % (quante, passi))
    return False, {"passi": passi, "passi_diversi": quante, "primo": primo}


def braccio_E(passi):
    """**Un run SANO CON NASCITE arriva al passo `passi` senza un solo errore del registro.**

    Restituisce anche `(S, net)`: il braccio **`F`** legge da **QUESTA** rete, cosi' il rendiconto
    della tolleranza parla del **run appena fatto** e non di un altro.
    """
    import contextlib
    print("")
    print("=" * 104)
    print("BRACCIO E -- run SANO con NASCITE fino al passo %d: nessun errore del registro" % passi)
    print("=" * 104)
    S, net = carica(None)
    n0 = int(net.n)
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            for _ in range(passi):
                _passo.passo_pieno(S, net)
    except Exception as e:
        print("  ### E FALLISCE: %s -- %s" % (type(e).__name__, str(e).split(chr(10))[0][:90]))
        return False, {"eccezione": type(e).__name__, "messaggio": str(e)[:600]}
    nato = int(net.n) - n0
    print("  n da %d a %d (### %d nati), controlli fatti %d, assenze contate %d"
          % (n0, net.n, nato, getattr(net, "_g_registro_controlli", 0),
             getattr(net, "_g_registro_assenti", 0)))
    print("  ### E %s" % ("PASSA: nessun CacheCorta/CacheLunga in un run sano CON NASCITE."
                          if nato > 0 else
                          "NON DIMOSTRA NIENTE: ZERO NASCITE, e il criterio chiede un run CON"
                          " nascite."))
    return nato > 0, {"n_iniziale": n0, "n_finale": int(net.n), "nati": nato,
                      "controlli": int(getattr(net, "_g_registro_controlli", 0)),
                      "assenze_contate": int(getattr(net, "_g_registro_assenti", 0))}, S, net


def braccio_F(net, S):
    """### **Il RENDICONTO della tolleranza: che cosa non e' MAI apparso.**

    *(Punto 2 di Luca, 2026-09-29.)* L'assenza e' tollerata **per grandezza, fino alla prima
    apparizione** -- necessario, perche' `_nb_ret` e' il Bloch **ritardato**. ### **Ma una
    tolleranza senza rendiconto e' un VARCO**, e questo braccio lo chiude: **se anche UNA sola
    grandezza di STATO non si e' mai vista piena, il sigillo lo RIPORTA come esito.**
    """
    print("")
    print("=" * 104)
    print("BRACCIO F -- il RENDICONTO della tolleranza: grandezze di STATO MAI apparse")
    print("=" * 104)
    mai = S.registro_mai_apparse(net)
    apparse = len(S.REGISTRO_STATO) - len(mai)
    print("  grandezze di STATO: %d   apparse almeno una volta: %d   ### MAI apparse: %d"
          % (len(S.REGISTRO_STATO), apparse, len(mai)))
    if mai:
        print("  ### %s" % ", ".join(mai))
        print("  ### F FALLISCE: o non esistono in questa configurazione -- e vanno dichiarate")
        print("      DERIVATE col loro motivo misurato -- oppure qualcosa non le crea mai, e")
        print("      allora IL REGISTRO DICE IL FALSO. In entrambi i casi restano FUORI dal")
        print("      controllo in silenzio, ed e' il varco che il punto 2 chiude.")
    else:
        print("  ### F PASSA: tutte e %d si sono viste piene, quindi la tolleranza dell assenza"
              % len(S.REGISTRO_STATO))
        print("      NON lascia nessuna grandezza fuori dal controllo.")
    return (not mai), {"stato": len(S.REGISTRO_STATO), "apparse": apparse, "mai_apparse": mai}


def braccio_C(passi_base):
    """### **IL CASO CHE DEVE FALLIRE:** col controllo SPENTO i guasti NON sono piu' protetti."""
    import contextlib
    print("")
    print("=" * 104)
    print("BRACCIO C -- IL CASO CHE DEVE FALLIRE: controllo SPENTO, i guasti tornano scoperti")
    print("=" * 104)
    S, net = carica(None, extra_sim=["--senza-controllo-registro"])
    print("  CONTROLLO_REGISTRO = %s   (il flag SPEGNE)" % S.CONTROLLO_REGISTRO)
    if S.CONTROLLO_REGISTRO:
        print("  ### C NON SI PUO' FARE: il flag non ha spento il controllo.")
        return False, {"motivo": "il flag non spegne"}
    with contextlib.redirect_stdout(io.StringIO()):
        for _ in range(passi_base):
            _passo.passo_pieno(S, net)
    DICH = tuple(c for c in (getattr(S, x, None) for x in
                             ("CacheCorta", "CacheLunga", "SchermaturaSpenta",
                              "LimiteNodiSuperato", "ComposizioneNonValida"))
                 if isinstance(c, type))
    n, m = int(net.n), int(len(net.i))
    prot, esiti = [], {}
    for nome, classe in S.REGISTRO_STATO:
        ok = []
        for guasto in ("CORTA", "LUNGA"):
            C = copy.deepcopy(net)
            v = getattr(C, nome)
            try:
                if isinstance(v, np.ndarray):
                    setattr(C, nome, v[:-1].copy() if guasto == "CORTA"
                            else np.concatenate([v, v[-1:]]))
                else:
                    setattr(C, nome, list(v[:-1]) if guasto == "CORTA" else list(v) + [v[-1]])
            except Exception:
                ok.append("NON GUASTABILE")
                continue
            S.net = C
            try:
                with contextlib.redirect_stdout(io.StringIO()):
                    _passo.passo_pieno(S, C)
                ok.append("PASSA")
            except Exception as e:
                ok.append("PROTETTO" if isinstance(e, DICH) else "ROTTO(%s)" % type(e).__name__)
        S.net = net
        esiti[nome] = ok
        if ok == ["PROTETTO", "PROTETTO"]:
            prot.append(nome)
    print("  grandezze di STATO provate: %d   (n = %d, m = %d)" % (len(esiti), n, m))
    print("  ### PROTETTE su ENTRAMBI i guasti, a controllo SPENTO: %d  %s"
          % (len(prot), prot if prot else ""))
    print("  chiamate a controllo spento, CONTATE: %d" % getattr(net, "_g_registro_spento", 0))
    passa = (len(prot) == 0)
    print("  ### C %s" % ("PASSA: a controllo spento NESSUNA e' protetta su entrambi i lati,"
                          " quindi la protezione viene DAL CONTROLLO."
                          if passa else
                          "FALLISCE: %d restano protette anche a controllo spento, quindi il"
                          " sigillo NON sta misurando il controllo." % len(prot)))
    return passa, {"protette_a_controllo_spento": prot, "esiti": esiti,
                   "chiamate_spente": int(getattr(net, "_g_registro_spento", 0))}


def principale():
    passi = 72
    for x in sys.argv[1:]:
        if x.startswith("--passi="):
            passi = int(x.split("=", 1)[1])
    if not os.path.isdir(FUORI):
        os.makedirs(FUORI)
    PRIMA = os.path.join(FUORI, "_sim_prima_controllo.py")
    introduce = sim_prima_del_controllo(PRIMA)
    print("simulatore OGGI ........ %s" % blob(SIM)[:8])
    print("`%s` introdotto da %s" % (ANCORA_CONTROLLO, str(introduce)[:12]))
    print("blob PRE-CONTROLLO ..... %s   (estratto IN BINARIO, par.7)" % blob(PRIMA)[:8])
    print("")

    # ### `P5`: LA CONFIGURAZIONE INTERA, non i flag toccati. E' l'omissione che avevo
    #   dichiarato per `_guasto_ripieghi.py`, e qui NON la ripeto.
    _Sc, _netc = carica(None)
    _cli_flag.dichiara_configurazione(_Sc, print)
    print("")

    esiti = {}
    esiti["B"] = braccio_B(passi, PRIMA)
    _ok_E, _dati_E, _S_E, _net_E = braccio_E(passi)
    esiti["E"] = (_ok_E, _dati_E)
    esiti["F"] = braccio_F(_net_E, _S_E)
    esiti["C"] = braccio_C(30)

    # --- A e D dal referto committato della prova a guasto
    print("")
    print("=" * 104)
    print("BRACCI A e D -- dal referto di `_guasto_ripieghi.py` (gia' girato e committato)")
    print("=" * 104)
    A_ok = D_ok = False
    a_dati = {}
    if os.path.isfile(REFERTO_A):
        j = json.load(io.open(REFERTO_A, encoding="utf-8"))
        S, net = carica(None)
        stato = [k for k, _c in S.REGISTRO_STATO]
        aposto = set(j.get("a_posto") or [])
        mancano = sorted(set(stato) - aposto)
        archi = sorted(k for k, c in S.REGISTRO_STATO if c == "arco")
        archi_ok = sorted(set(archi) - aposto)
        A_ok, D_ok = (not mancano), (not archi_ok)
        a_dati = {"stato": len(stato), "a_posto": len(aposto & set(stato)),
                  "mancano": mancano, "archi": len(archi), "archi_non_a_posto": archi_ok,
                  "ripiego_silenzioso": j.get("ripiego_silenzioso") or []}
        print("  A: grandezze di STATO %d, a posto %d, mancano %s"
              % (len(stato), len(aposto & set(stato)), mancano if mancano else "NESSUNA"))
        print("  D: per arco %d, non a posto %s" % (len(archi), archi_ok if archi_ok else "NESSUNA"))
        print("  RIPIEGO SILENZIOSO residuo (anche su DERIVATE): %s"
              % (j.get("ripiego_silenzioso") or "NESSUNO"))
    else:
        print("  ### referto di A NON TROVATO: %s" % REFERTO_A)

    print("")
    print("=" * 104)
    print("IL VERDETTO")
    print("=" * 104)
    tutti = {"A": A_ok, "D": D_ok, "B": esiti["B"][0], "C": esiti["C"][0],
             "E": esiti["E"][0], "F": esiti["F"][0]}
    for k in ("A", "B", "C", "D", "E", "F"):
        print("  braccio %s ... %s" % (k, "PASSA" if tutti[k] else "### FALLISCE"))
    passa = all(tutti.values())
    print("")
    print("### IL SIGILLO %s" % ("PASSA: tutti e cinque i bracci." if passa
                                 else "FALLISCE, e NON lo aggiusto: si committa e si FERMA."))
    OUT = os.path.join(FUORI, "_sig_controllo_unico.json")
    io.open(OUT, "w", encoding="utf-8", newline=chr(10)).write(json.dumps(
        {"blob_oggi": blob(SIM), "blob_prima": blob(PRIMA), "introduce": str(introduce),
         "passi": passi, "bracci": tutti,
         "B": esiti["B"][1], "C": esiti["C"][1], "E": esiti["E"][1], "F": esiti["F"][1],
         "A_e_D": a_dati,
         "passa": passa}, indent=1, ensure_ascii=False, default=float))
    print("scritto: " + OUT)
    return 0 if passa else 1


if __name__ == "__main__":
    sys.exit(principale())
