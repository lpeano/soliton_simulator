# -*- coding: utf-8 -*-
"""**L'ORDINE FRA LA PRIMA LETTURA E LA PRIMA RISCRITTURA, dopo la nascita.**

**Mandato del guardiano, 2026-09-29, punto 1.** Il criterio del controllo unico **non e'**
*«stato o derivata»*:

> ### **Una DERIVATA LETTA fra la nascita e la sua riscrittura ha bisogno di una REGOLA DI
> NASCITA** *(come `psi`, `psi_spin`, `rho_spin` il 2026-09-28)*; ### **una NON letta in
> quell'intervallo puo' restare corta.**

**Il mio piano sbagliava qui, e la correzione e' di Luca:** `psi` **E'** derivata *(la scrive
`calcola_psi`)*, e ha avuto bisogno di ereditare **non** per la sua natura, ma perche'
### **una legge la leggeva dopo la mitosi e prima del ricalcolo** — ed e' li' che nasceva il flash.

## ⛔ I QUATTRO difetti della PRIMA stesura *(`3a35664d`, fallimento in `249ee3c`)*

**La corsa era valida, il verdetto NO.** Tutti e quattro venivano dall'aver fissato **un solo
metro**:

| | difetto | la cura, qui |
|---|---|---|
| **①** | la riscrittura completa cercata come `len == n` ### **anche per le grandezze PER ARCO**, che sono piene a `m`: tutte e nove risultavano *«mai riscritta»* **per costruzione** | ### **il bersaglio e' `n` per i nodi e `m` per gli archi**, e la classe si fissa **PRIMA** della nascita |
| **②** | il confine era la riga di `phi`, ### **ma la mitosi estende `pos` a `:6640`, un evento PRIMA**: `pos` risultava *«letta prima»*, ### **un artefatto** | ### **la finestra parte da quando la voce `mitosi` RITORNA** — dentro `mitosi` nessuna legge legge |
| **③** | la finestra si chiudeva a **fine passo**, e non distingueva *«riscritta al passo dopo prima che qualcuno la legga»* da *«letta corta al passo dopo»* — ### **il caso di `_xi_rumore`** | ### **la finestra continua NEL PASSO SEGUENTE** |
| **④** | ogni lettura contava come *«lettura di legge»*, ### **anche quella di `verifica_invarianti`**, che `_PASSO_TIPI` dichiara **`osservatore`: LEGGE SOLTANTO** | ### **il TIPO del lettore si prende da `_PASSO_TIPI`**, la tabella del simulatore: `osservatore` e `disegno` **non** sono leggi |

## Come si misura, e ### **non e' una lettura del codice**

| | |
|---|---|
| **1** | scena **GRANDE**, seme `11`, avanti fino a ### **un passo CON NASCITA** — che si **cerca**, non si assume |
| **2** | la rete e' **sorvegliata** da una **sottoclasse dinamica**: `__getattribute__`, `__setattr__` e ### **`mitosi`**, per le sole grandezze del registro. Registra **ordine** e **funzione chiamante** |
| **3** | ### **la finestra si apre quando `mitosi` RITORNA** *(se `n` e' cresciuto)* e si chiude **a fine del passo SEGUENTE** |
| **4** | per ogni grandezza, nella finestra: prima **lettura di LEGGE**, prima lettura dell'**osservatore**, prima **riscrittura COMPLETA** *(al proprio bersaglio)* |

## Gli esiti

| | |
|---|---|
| ### **PIENA A FINE MITOSI** | e' gia' lunga al suo bersaglio quando `mitosi` ritorna: ### **nessuno puo' vederla corta.** E' il caso di chi **ha** una regola di nascita |
| ### **LETTA PRIMA** | ### **SERVE UNA REGOLA DI NASCITA** — una **legge** la legge corta prima che venga riscritta |
| **RISCRITTA PRIMA** | **puo' restare corta**: nessuna legge la vede |
| **SOLO L'OSSERVATORE** | la guarda solo `verifica_invarianti` / il disegno: ### **si riporta, e va deciso a parte** |
| **MAI TOCCATA** | in **due** passi non e' ne' letta ne' riscritta. ### **Non e' un'assoluzione** |

### ⚠ **La sorveglianza NON cambia la fisica, e il CONTROLLO lo verifica:** lo stesso passo con
e senza, ### **byte-identico**. Se non lo e', `vale: false` e si ferma.
**E non si tiene un elenco di eventi:** si registrano **solo le PRIME occorrenze** *(43 voci)* —
la prima stesura ne teneva **1,9 milioni per passo**.

COMANDO:  python csv/_test_fork/_ordine_letture.py [--da=40] [--fino=72]
USCITA:   0 se il controllo tiene e una nascita e' stata trovata; 1 altrimenti.
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
# ⚠ `phi` e `i`/`j` sono i METRI (`n = len(phi)`, `m = len(i)`): si sorvegliano -- `phi` serve a
#   sapere se `n` e' cresciuto -- ma NON sono voci del registro.
METRI = ("phi", "i", "j")
# i tipi di `_PASSO_TIPI` che NON sono leggi. **Dalla tabella del simulatore, non da una mia idea.**
NON_LEGGI = ("osservatore", "disegno")
GRANDEZZE = ("d", "d0", "phi", "phi0", "phi_s", "phivel", "psi", "psi_spin", "eta", "tw", "twp",
             "vd", "peq", "mem_mot", "perc_chi", "perc_geom", "perc_tw", "omega_s", "_nb",
             "_nb_prec", "_psi_spinor", "_psi_prec", "_spinor_lift")


def _grafo():
    """`{funzione: {chiamate}}` e l'insieme dei nomi definiti, dall'AST del simulatore."""
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
    return fine, chiama


def raggiungibili_da(radici, fine, chiama):
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


def tipi_dei_lettori(S):
    """`{funzione: {tipi delle VOCI che la possono raggiungere}}`.

    ### **Il tipo viene da `_PASSO_TIPI`, che e' la tabella del SIMULATORE** — non da una mia
    classificazione. Una funzione raggiungibile da piu' voci porta **tutti** i loro tipi.
    """
    fine, chiama = _grafo()
    fasi = dict(getattr(S, "_PASSO_FASI", {}))
    fuori = {}
    for voce, tipo in getattr(S, "_PASSO_TIPI", {}).items():
        radice = fasi.get(voce, voce)
        for f in raggiungibili_da((radice,), fine, chiama):
            fuori.setdefault(f, set()).add(tipo)
    return fuori, raggiungibili_da(RADICI_NASCITA, fine, chiama)


def _lun(v):
    try:
        return len(v)
    except Exception:
        return -1


def per_nodo_e_arco(net):
    n, m = int(net.n), int(len(net.i))
    nodo, arco = [], []
    for k, v in sorted(vars(net).items()):
        if not isinstance(v, (np.ndarray, list)):
            continue
        L = _lun(v)
        if L == n:
            nodo.append(k)
        elif L == m:
            arco.append(k)
    return nodo, arco


def sorveglia(net, nomi, tipi, classe):
    """Mette la rete **sotto sorveglianza**. Restituisce `(stato, classe_originale)`.

    ### **Nessun byte del simulatore cambia:** e' una **sottoclasse dinamica**, e a fine misura la
    classe si rimette com'era. Si **annota** e si **delega**: stesso oggetto in lettura, stesso
    valore in scrittura.
    """
    base = type(net)
    st = {"k": 0, "finestra": False, "fine_mitosi": None, "n": None, "m": None,
          "bersaglio": {}, "primi": {}, "cresciuto": False, "eventi_contati": 0,
          "len_a_fine_mitosi": None}
    OSS = set(nomi)

    def _reg(nome, specie, lung, chi):
        st["eventi_contati"] += 1
        if not st["finestra"]:
            return
        p = st["primi"].setdefault(nome, {})
        if specie == "W":
            if lung == st["bersaglio"].get(nome) and "riscrittura" not in p:
                p["riscrittura"] = {"evento": st["k"], "chi": chi, "len": lung}
            return
        t = tipi.get(chi, set())
        e_legge = bool(t) and not t.issubset(set(NON_LEGGI))
        chiave = "lettura_legge" if e_legge else "lettura_non_legge"
        if chiave not in p:
            p[chiave] = {"evento": st["k"], "chi": chi, "len": lung,
                         "tipi": sorted(t) or ["(fuori dalle voci)"]}

    class Sorvegliata(base):
        def __getattribute__(self, nome):
            v = base.__getattribute__(self, nome)
            if nome in OSS:
                st["k"] += 1
                try:
                    chi = sys._getframe(1).f_code.co_name
                except Exception:
                    chi = "?"
                _reg(nome, "R", _lun(v), chi)
            return v

        def __setattr__(self, nome, valore):
            base.__setattr__(self, nome, valore)
            if nome in OSS:
                st["k"] += 1
                try:
                    chi = sys._getframe(1).f_code.co_name
                except Exception:
                    chi = "?"
                _reg(nome, "W", _lun(valore), chi)

        def mitosi(self, *a, **k):
            d = base.__getattribute__(self, "__dict__")
            n_prima = _lun(d.get("phi"))
            r = base.mitosi(self, *a, **k)
            # ### LA FINESTRA SI APRE QUI: dentro `mitosi` nessuna legge legge.
            if not st["finestra"]:
                n_dopo = _lun(d.get("phi"))
                st["fine_mitosi"] = st["k"]
                st["n"], st["m"] = n_dopo, _lun(d.get("i"))
                st["cresciuto"] = bool(n_dopo > n_prima >= 0)
                if st["cresciuto"]:
                    # ### IL BERSAGLIO SI FISSA QUI, non a fine passo: `n` per i nodi, `m` per
                    #   gli archi. **Fissarlo dopo il passo era un difetto della stesura di
                    #   mezzo: durante il passo di nascita nessuna riscrittura sarebbe stata
                    #   registrata**, e l'ho preso prima di girare.
                    st["bersaglio"] = {k: (st["n"] if classe.get(k) == "nodo" else st["m"])
                                       for k in classe}
                    st["len_a_fine_mitosi"] = {k: _lun(d.get(k)) for k in classe}
                    st["finestra"] = True
            return r

    net.__class__ = Sorvegliata
    return st, base


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
    import contextlib
    da, fino = 40, 72
    for x in sys.argv[1:]:
        if x.startswith("--da="):
            da = int(x.split("=", 1)[1])
        elif x.startswith("--fino="):
            fino = int(x.split("=", 1)[1])
    if not os.path.isdir(FUORI):
        os.makedirs(FUORI)
    S, net = carica(da)
    tipi, _ragg = tipi_dei_lettori(S)
    nodo, arco = per_nodo_e_arco(net)
    # ### LA CLASSE SI FISSA PRIMA DELLA NASCITA: e' il difetto (1) della prima stesura.
    classe = {}
    for k in nodo:
        classe[k] = "nodo"
    for k in arco:
        classe[k] = "arco"
    voci = [k for k in nodo + arco if k not in METRI]
    classe_voci = {k: classe[k] for k in voci}
    osservate = sorted(set(voci) | set(METRI))
    print("scena ........ nmasse %d, sep %.4f  ->  n = %d, archi = %d   (dopo %d passi)"
          % (S._NMASSE_VIDEO["n"], S._NMASSE_VIDEO["sep"], net.n, len(net.i), da))
    print("sorvegliate .. %d  (%d voci + %d metri: %s)"
          % (len(osservate), len(voci), len(METRI), ", ".join(METRI)))
    print("classe FISSATA PRIMA della nascita: %d per nodo, %d per arco"
          % (len(nodo) - sum(1 for x in METRI if x in nodo),
             len(arco) - sum(1 for x in METRI if x in arco)))
    print("tipi dei lettori presi da `_PASSO_TIPI`: %d funzioni mappate; NON leggi: %s"
          % (len(tipi), ", ".join(NON_LEGGI)))
    print("")

    # ---- il CONTROLLO --------------------------------------------------------------------
    print("=" * 104)
    print("CONTROLLO -- lo stesso passo CON e SENZA sorveglianza: byte-identico?")
    print("=" * 104)
    A, B = copy.deepcopy(net), copy.deepcopy(net)
    S.net = A
    with contextlib.redirect_stdout(io.StringIO()):
        _passo.passo_pieno(S, A)
    fa = _foto(A)
    stb, baseb = sorveglia(B, osservate, tipi, classe_voci)
    S.net = B
    with contextlib.redirect_stdout(io.StringIO()):
        _passo.passo_pieno(S, B)
    B.__class__ = baseb
    sano = _identiche(fa, _foto(B))
    S.net = net
    print("  eventi intercettati nel passo di prova: %d" % stb["eventi_contati"])
    print("  ### %s" % ("CONTROLLO OK: la sorveglianza NON cambia un bit." if sano else
                        "CONTROLLO FALLITO: la sorveglianza PERTURBA. LA MISURA NON VALE."))
    if not sano:
        io.open(os.path.join(FUORI, "_ordine_letture.json"), "w", encoding="utf-8",
                newline=chr(10)).write(json.dumps(
                    {"vale": False, "motivo": "la sorveglianza perturba lo stato"}, indent=1))
        return 1
    print("")

    # ---- la misura -----------------------------------------------------------------------
    print("=" * 104)
    print("AVANTI FINO A UN PASSO CON NASCITA. La finestra si apre quando `mitosi` RITORNA,")
    print("e si chiude a FINE DEL PASSO SEGUENTE.")
    print("=" * 104)
    st, base = sorveglia(net, osservate, tipi, classe_voci)
    passo, nascita, dopo_la_nascita = da, None, 0
    pieno_a_fine_mitosi = None
    while passo < fino:
        passo += 1
        with contextlib.redirect_stdout(io.StringIO()):
            _passo.passo_pieno(S, net)
        if nascita is None and st["cresciuto"]:
            nascita = passo
            pieno_a_fine_mitosi = st["len_a_fine_mitosi"]
            print("  passo %d: ### NASCITA -- n = %d, m = %d, `mitosi` ritorna all'evento %d"
                  % (passo, st["n"], st["m"], st["fine_mitosi"]))
            dopo_la_nascita = 1
            continue
        if nascita is not None:
            dopo_la_nascita += 1
            if dopo_la_nascita >= 2:
                print("  passo %d: passo SEGUENTE percorso, finestra chiusa" % passo)
                break
        else:
            print("  passo %d: nessuna nascita" % passo)
    net.__class__ = base
    if nascita is None:
        print("  ### NESSUNA NASCITA fino al passo %d: LA MISURA NON SI PUO' FARE." % fino)
        io.open(os.path.join(FUORI, "_ordine_letture.json"), "w", encoding="utf-8",
                newline=chr(10)).write(json.dumps(
                    {"vale": False, "motivo": "nessuna nascita entro %d" % fino}, indent=1))
        return 1
    print("")

    # ---- il verdetto ---------------------------------------------------------------------
    esiti = {}
    for k in voci:
        p = st["primi"].get(k, {})
        bers = st["n"] if classe.get(k) == "nodo" else st["m"]
        ll, ln, rr = (p.get("lettura_legge"), p.get("lettura_non_legge"), p.get("riscrittura"))
        if ll and rr:
            esito = "LETTA PRIMA" if ll["evento"] < rr["evento"] else "RISCRITTA PRIMA"
        elif ll:
            esito = "LETTA E MAI RISCRITTA"
        elif rr:
            esito = "RISCRITTA PRIMA"
        elif ln:
            esito = "SOLO L'OSSERVATORE"
        else:
            esito = "MAI TOCCATA"
        esiti[k] = {"classe": classe.get(k), "bersaglio": bers, "esito": esito,
                    "lettura_di_legge": ll, "lettura_non_di_legge": ln, "riscrittura": rr}
    print("=" * 104)
    print("L'ORDINE, nella finestra (bersaglio: n = %d per i nodi, m = %d per gli archi)"
          % (st["n"], st["m"]))
    print("=" * 104)
    print("  %-20s %-5s %-22s %-26s %s"
          % ("grandezza", "cl.", "esito", "prima lettura di LEGGE", "prima riscrittura"))
    for k in voci:
        r = esiti[k]
        ll, rr = r["lettura_di_legge"], r["riscrittura"]
        print("  %-20s %-5s %-22s %-26s %s"
              % (k, r["classe"][:4], r["esito"],
                 ("#%d %s" % (ll["evento"], ll["chi"]))[:26] if ll else "--",
                 ("#%d %s" % (rr["evento"], rr["chi"])) if rr else "--"))

    def q(e):
        return sorted(k for k in voci if esiti[k]["esito"] == e)
    print("")
    print("=" * 104)
    print("IL VERDETTO (criterio del guardiano, punto 1)")
    print("=" * 104)
    for e, nota in (("LETTA PRIMA", "### SERVE UNA REGOLA DI NASCITA"),
                    ("LETTA E MAI RISCRITTA", "### SERVE UNA REGOLA DI NASCITA"),
                    ("RISCRITTA PRIMA", "puo' restare corta"),
                    ("SOLO L'OSSERVATORE", "la guarda solo il controllo di dominio o il disegno"),
                    ("MAI TOCCATA", "in DUE passi: e NON e' un'assoluzione")):
        v = q(e)
        print("  %-24s %3d  %s" % (e, len(v), nota))
        if v:
            print("      %s" % ", ".join(v))
    OUT = os.path.join(FUORI, "_ordine_letture.json")
    io.open(OUT, "w", encoding="utf-8", newline=chr(10)).write(json.dumps(
        {"vale": True, "passo_di_nascita": nascita, "n": st["n"], "m": st["m"],
         "evento_fine_mitosi": st["fine_mitosi"], "eventi_intercettati": st["eventi_contati"],
         "nmasse": S._NMASSE_VIDEO["n"], "sep": S._NMASSE_VIDEO["sep"],
         "voci": voci, "metri": list(METRI), "classe": classe,
         "len_a_fine_mitosi": pieno_a_fine_mitosi, "controllo_byte_identico": True,
         "non_leggi": list(NON_LEGGI), "esiti": esiti},
        indent=1, ensure_ascii=False, default=float))
    print("")
    print("scritto: " + OUT)
    return 0


if __name__ == "__main__":
    sys.exit(principale())
