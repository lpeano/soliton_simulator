# -*- coding: utf-8 -*-
"""**L'ORDINE FRA LA PRIMA LETTURA E LA PRIMA RISCRITTURA, dopo la nascita.**

**Mandato del guardiano, 2026-09-29, punto 1.** Il criterio del controllo unico **non e'**
*«stato o derivata»*:

> ### **Una DERIVATA LETTA fra la nascita e la sua riscrittura ha bisogno di una REGOLA DI
> NASCITA** *(come `psi`, `psi_spin`, `rho_spin` il 2026-09-28)*; ### **una NON letta in
> quell'intervallo puo' restare corta.**

**Il mio piano sbagliava qui, e la correzione e' di Luca:** `psi` **E'** derivata *(la scrive
`calcola_psi`)*, e ha avuto bisogno di ereditare **non** per la sua natura, ma perche'
### **una legge la leggeva dopo la mitosi e prima del ricalcolo** -- ed e' esattamente li' che
nasceva il flash.

## Come si misura, e ### **non e' una lettura del codice**

| | |
|---|---|
| **1** | scena **GRANDE** *(`nmasse` e `sep` dall'argv)*, seme `11`, avanti fino a ### **un passo CON NASCITA** *(il primo e' il `42`)* |
| **2** | la rete viene **sorvegliata**: una **sottoclasse dinamica** intercetta `__getattribute__` e `__setattr__` per **le sole grandezze del registro**, e **registra l'ORDINE** *(un contatore) e la FUNZIONE CHIAMANTE* |
| **3** | ### **il confine e' la NASCITA**: l'istante in cui `phi` viene assegnata **piu' lunga di prima** *(`n` E' `len(phi)`)* |
| **4** | da quell'istante, per ogni grandezza: la **prima LETTURA** e la **prima RISCRITTURA COMPLETA** *(`len == n`)* |

## I tre esiti, e il verdetto e' l'ORDINE

| | |
|---|---|
| ### **LETTA PRIMA** | ### **SERVE UNA REGOLA DI NASCITA.** E' il caso di `psi`: qualcuno la legge corta prima che la sua legge la riscriva |
| **RISCRITTA PRIMA** | **puo' restare corta**: nessuno la vede nell'intervallo |
| **MAI TOCCATA** | nell'intervallo non e' ne' letta ne' riscritta. ### **Si riporta, e NON e' un'assoluzione** *(nel passo dopo potrebbe esserlo)* |

> ### 📌 **E LE LETTURE SI DISTINGUONO IN DUE SPECIE, senno' il verdetto e' falso:** una funzione
> che **estende** una cache la **legge** per estenderla *(`np.concatenate([self.eta, ...])`)*.
> ### **Quella NON e' una lettura di legge: e' parte della riscrittura.** Si separa guardando la
> **funzione chiamante**: se e' raggiungibile dai siti di nascita e' una **lettura di estensione**.

### ⚠ **La sorveglianza NON cambia la fisica, e va detto come si garantisce**
`__getattribute__` restituisce **lo stesso oggetto**, `__setattr__` **scrive lo stesso valore**: si
**annota** e si delega. Il generatore `net.rng` non viene toccato. **E il braccio di CONTROLLO lo
verifica**: lo stesso passo, con e senza sorveglianza, ### **deve essere byte-identico**.

COMANDO:  python csv/_test_fork/_ordine_letture.py [--da=40] [--fino=72]
USCITA:   0 se il controllo byte-identico tiene e una nascita e' stata trovata; 1 altrimenti.
"""
import ast
import copy
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

SIM = os.path.join(RADICE, "soliton_simulator.py")
FUORI = os.path.join(RADICE, "csv", "_seal_fork", "_ordine_letture")
SCARTO = os.path.join(FUORI, "_scarto_cli")
RADICI_NASCITA = ("semina", "mitosi", "_allaccia")
# ⚠ `phi` e `i`/`j` sono i METRI (`n = len(phi)`, `m = len(i)`): si sorvegliano comunque, perche'
#   `phi` E' il confine, ma non sono voci del registro.
METRI = ("phi", "i", "j")
# le 23 del sigillo, per il braccio di CONTROLLO byte-identico
GRANDEZZE = ("d", "d0", "phi", "phi0", "phi_s", "phivel", "psi", "psi_spin", "eta", "tw", "twp",
             "vd", "peq", "mem_mot", "perc_chi", "perc_geom", "perc_tw", "omega_s", "_nb",
             "_nb_prec", "_psi_spinor", "_psi_prec", "_spinor_lift")


def raggiungibili(radici):
    """Le funzioni **raggiungibili** dai siti di nascita. *(Come in `_registro_grandezze.py`.)*"""
    albero = ast.parse(io.open(SIM, encoding="utf-8").read())
    fine = {x.name: x for x in ast.walk(albero)
            if isinstance(x, (ast.FunctionDef, ast.AsyncFunctionDef))}
    chiama = {}
    for nome, nodo in fine.items():
        s = set()
        for x in ast.walk(nodo):
            if isinstance(x, ast.Call):
                nc = getattr(x.func, "attr", None) or getattr(x.func, "id", None)
                if nc in fine and nc != nome:
                    s.add(nc)
        chiama[nome] = s
    fuori, coda = set(), []
    for r in radici:
        if r in fine:
            fuori.add(r)
            coda.append(r)
    while coda:
        cur = coda.pop(0)
        for succ in sorted(chiama.get(cur, ())):
            if succ not in fuori:
                fuori.add(succ)
                coda.append(succ)
    return fuori


def per_nodo_e_arco(net):
    """L'elenco **misurato**: `len == n` e `len == m`. *(Lo stesso criterio del registro.)*"""
    n, m = int(net.n), int(len(net.i))
    nodo, arco = [], []
    for k, v in sorted(vars(net).items()):
        if not isinstance(v, (np.ndarray, list)):
            continue
        try:
            L = len(v)
        except Exception:
            continue
        (nodo if L == n else arco if L == m else []).append(k)
    return nodo, arco


def _lun(v):
    try:
        return len(v)
    except Exception:
        return -1


def sorveglia(net, nomi):
    """Mette la rete **sotto sorveglianza** e restituisce il registratore.

    **Sottoclasse dinamica**, non una patch del simulatore: ### **nessun byte del simulatore
    cambia**, e a fine misura la classe si rimette com'era.
    """
    stato = {"k": 0, "confine": None, "eventi": [], "n_al_confine": None}
    OSS = set(nomi)
    base = type(net)

    class Sorvegliata(base):
        def __getattribute__(self, nome):
            v = base.__getattribute__(self, nome)
            if nome in OSS:
                stato["k"] += 1
                try:
                    chi = sys._getframe(1).f_code.co_name
                except Exception:
                    chi = "?"
                stato["eventi"].append((stato["k"], "R", nome, _lun(v), chi))
            return v

        def __setattr__(self, nome, valore):
            if nome in OSS:
                vecchia = _lun(base.__getattribute__(self, nome)
                               if hasattr(base, nome) or nome in self.__dict__ else None)
                base.__setattr__(self, nome, valore)
                stato["k"] += 1
                try:
                    chi = sys._getframe(1).f_code.co_name
                except Exception:
                    chi = "?"
                nuova = _lun(valore)
                stato["eventi"].append((stato["k"], "W", nome, nuova, chi))
                # ### IL CONFINE: `phi` assegnata PIU' LUNGA di prima -> `n` e' cresciuto.
                if nome == "phi" and stato["confine"] is None and nuova > vecchia >= 0:
                    stato["confine"] = stato["k"]
                    stato["n_al_confine"] = nuova
                return
            base.__setattr__(self, nome, valore)

    net.__class__ = Sorvegliata
    return stato, base


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
    return q


def _identiche(a, b):
    if set(a) != set(b):
        return False
    with np.errstate(all="ignore"):
        for k in a:
            x, y = np.asarray(a[k]), np.asarray(b[k])
            if x.shape != y.shape:
                return False
            try:
                if not np.array_equal(x, y, equal_nan=True):
                    return False
            except TypeError:
                if not np.array_equal(x, y):
                    return False
    return True


def carica(passi):
    import contextlib
    with contextlib.redirect_stdout(io.StringIO()):
        _S0, argv = _cli_flag.argv_del_driver(extra=["--seme=11"], dest=SCARTO)
        S, a = _cli_flag.carica_dal_cli(list(argv), nome="sim_ordine")
        S._NMASSE_VIDEO["n"] = max(2, int(getattr(a, "nmasse", 2)))
        S._NMASSE_VIDEO["sep"] = float(getattr(a, "sep", 3.0))
        S._NMASSE_VIDEO["size"] = None
        S.avvia_test("MASSE-COERENTI")()
        net = S.net
        for _ in range(passi):
            _passo.passo_pieno(S, net)
    return S, net


def principale():
    da, fino = 40, 72
    for x in sys.argv[1:]:
        if x.startswith("--da="):
            da = int(x.split("=", 1)[1])
        elif x.startswith("--fino="):
            fino = int(x.split("=", 1)[1])
    if not os.path.isdir(FUORI):
        os.makedirs(FUORI)
    RAGG = raggiungibili(RADICI_NASCITA)
    S, net = carica(da)
    nodo, arco = per_nodo_e_arco(net)
    voci = [k for k in nodo + arco if k not in METRI]
    osservate = sorted(set(voci) | set(METRI))
    print("scena ........ nmasse %d, sep %.4f  ->  n = %d, archi = %d   (dopo %d passi)"
          % (S._NMASSE_VIDEO["n"], S._NMASSE_VIDEO["sep"], net.n, len(net.i), da))
    print("sorvegliate .. %d  (%d voci del registro + %d metri: %s)"
          % (len(osservate), len(voci), len(METRI), ", ".join(METRI)))
    print("funzioni raggiungibili dai siti di nascita: %d" % len(RAGG))
    print("")

    # ---- il CONTROLLO: la sorveglianza non cambia un bit ---------------------------------
    print("=" * 104)
    print("CONTROLLO -- lo stesso passo CON e SENZA sorveglianza: byte-identico?")
    print("=" * 104)
    import contextlib
    A, B = copy.deepcopy(net), copy.deepcopy(net)
    S.net = A
    with contextlib.redirect_stdout(io.StringIO()):
        _passo.passo_pieno(S, A)
    fa = _foto(A)
    st_b, base_b = sorveglia(B, osservate)
    S.net = B
    with contextlib.redirect_stdout(io.StringIO()):
        _passo.passo_pieno(S, B)
    B.__class__ = base_b
    fb = _foto(B)
    sano = _identiche(fa, fb)
    print("  eventi registrati nel passo di prova: %d" % len(st_b["eventi"]))
    print("  ### %s" % ("CONTROLLO OK: la sorveglianza NON cambia un bit."
                        if sano else
                        "CONTROLLO FALLITO: la sorveglianza PERTURBA. LA MISURA NON VALE."))
    S.net = net
    if not sano:
        io.open(os.path.join(FUORI, "_ordine_letture.json"), "w", encoding="utf-8",
                newline=chr(10)).write(json.dumps(
                    {"vale": False, "motivo": "la sorveglianza perturba lo stato"},
                    indent=1, ensure_ascii=False))
        return 1
    print("")

    # ---- avanti fino a un passo CON NASCITA, sorvegliando ---------------------------------
    print("=" * 104)
    print("AVANTI FINO A UN PASSO CON NASCITA (il confine e' `phi` assegnata PIU' LUNGA)")
    print("=" * 104)
    passo, trovato, st = da, None, None
    while passo < fino:
        passo += 1
        C = copy.deepcopy(net)
        st, base = sorveglia(C, osservate)
        S.net = C
        with contextlib.redirect_stdout(io.StringIO()):
            _passo.passo_pieno(S, C)
        C.__class__ = base
        if st["confine"] is not None:
            trovato = passo
            print("  passo %d: ### NASCITA -- n da %d a %d, confine all'evento %d, eventi totali %d"
                  % (passo, net.n, st["n_al_confine"], st["confine"], len(st["eventi"])))
            break
        print("  passo %d: nessuna nascita (%d eventi)" % (passo, len(st["eventi"])))
        S.net = net
        with contextlib.redirect_stdout(io.StringIO()):
            _passo.passo_pieno(S, net)
    S.net = net
    if trovato is None:
        print("  ### NESSUNA NASCITA fino al passo %d: LA MISURA NON SI PUO' FARE." % fino)
        io.open(os.path.join(FUORI, "_ordine_letture.json"), "w", encoding="utf-8",
                newline=chr(10)).write(json.dumps(
                    {"vale": False, "motivo": "nessuna nascita entro il passo %d" % fino},
                    indent=1, ensure_ascii=False))
        return 1
    print("")

    # ---- l'ordine, dopo il confine --------------------------------------------------------
    conf, nn = st["confine"], st["n_al_confine"]
    dopo = [e for e in st["eventi"] if e[0] >= conf]
    esiti = {}
    for k in voci:
        mio = [e for e in dopo if e[2] == k]
        letture = [e for e in mio if e[1] == "R"]
        # ### una lettura fatta da chi ESTENDE non e' una lettura di legge: e' la riscrittura.
        legge = [e for e in letture if e[4] not in RAGG]
        estens = [e for e in letture if e[4] in RAGG]
        riscr = [e for e in mio if e[1] == "W" and e[3] == nn]
        pl = legge[0] if legge else None
        pr = riscr[0] if riscr else None
        if pl is None and pr is None:
            esito = "MAI TOCCATA"
        elif pl is None:
            esito = "RISCRITTA PRIMA"
        elif pr is None:
            esito = "LETTA E MAI RISCRITTA"
        else:
            esito = "LETTA PRIMA" if pl[0] < pr[0] else "RISCRITTA PRIMA"
        esiti[k] = {
            "esito": esito,
            "prima_lettura_di_legge": ({"evento": pl[0], "len": pl[3], "chi": pl[4]}
                                       if pl else None),
            "prima_riscrittura_completa": ({"evento": pr[0], "len": pr[3], "chi": pr[4]}
                                           if pr else None),
            "letture_di_legge": len(legge), "letture_di_estensione": len(estens),
            "prime_letture_di_estensione": [{"evento": e[0], "chi": e[4]} for e in estens[:3]],
        }
    print("=" * 104)
    print("L'ORDINE: prima LETTURA DI LEGGE contro prima RISCRITTURA COMPLETA (len == %d)" % nn)
    print("=" * 104)
    print("  %-22s %-24s %-28s %s" % ("grandezza", "esito", "prima lettura (chi)",
                                      "prima riscrittura (chi)"))
    for k in voci:
        r = esiti[k]
        pl, pr = r["prima_lettura_di_legge"], r["prima_riscrittura_completa"]
        print("  %-22s %-24s %-28s %s"
              % (k, r["esito"],
                 ("#%d %s" % (pl["evento"], pl["chi"]))[:28] if pl else "--",
                 ("#%d %s" % (pr["evento"], pr["chi"])) if pr else "--"))

    def q(e):
        return sorted(k for k in voci if esiti[k]["esito"] == e)
    print("")
    print("=" * 104)
    print("IL VERDETTO (criterio del guardiano, punto 1)")
    print("=" * 104)
    for e, nota in (("LETTA PRIMA", "### SERVE UNA REGOLA DI NASCITA"),
                    ("LETTA E MAI RISCRITTA", "### SERVE UNA REGOLA DI NASCITA"),
                    ("RISCRITTA PRIMA", "puo' restare corta"),
                    ("MAI TOCCATA", "non e' un'assoluzione: nel passo dopo potrebbe esserlo")):
        v = q(e)
        print("  %-24s %3d  %s" % (e, len(v), nota))
        if v:
            print("      %s" % ", ".join(v))
    OUT = os.path.join(FUORI, "_ordine_letture.json")
    io.open(OUT, "w", encoding="utf-8", newline=chr(10)).write(json.dumps(
        {"vale": True, "passo_di_nascita": trovato, "n_al_confine": nn,
         "evento_del_confine": conf, "eventi_totali": len(st["eventi"]),
         "nmasse": S._NMASSE_VIDEO["n"], "sep": S._NMASSE_VIDEO["sep"],
         "voci": voci, "metri": list(METRI), "controllo_byte_identico": True,
         "esiti": esiti}, indent=1, ensure_ascii=False, default=float))
    print("")
    print("scritto: " + OUT)
    return 0


if __name__ == "__main__":
    sys.exit(principale())
