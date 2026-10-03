# -*- coding: utf-8 -*-
"""**IL CENSIMENTO DI `perc_geom`: dove nasce un suo valore per un nodo NUOVO.**

### `PASSO 1` del `COMMIT 5` del riordino, e gira **PRIMA del codice** *(mandato del guardiano
su decisione di Luca del 2026-09-29)*.

## I SEI PEZZI

| | |
|---|---|
| **0** | ### **IL FATTO STRUTTURALE, MISURATO:** i posti di `perc_geom`, `tw`, `i`, `j`, `_deg` in `ORDINE_DI_NASCITA`, e la **classe** di ciascuno. ### **Decide se la derivazione si PUO' calcolare dov'e' la regola oggi.** |
| **1** | ### **DALL'AST:** ogni scrittura di `perc_geom` in TUTTO il file, classificata *(inizializza · estende · in posto · altro)*, con riga e funzione — ### **anche nei rami spenti** |
| **2** | ### **DAL RUNTIME:** un **descrittore di dato** registra ogni scrittura con `len` prima/dopo e ### **i valori NUOVI**, sulle ### **TRE scene** del commit 4 |
| **3** | ### **LA DIFFERENZA `1` meno `2`, riga per riga COL MOTIVO.** Una riga vista dal runtime e non dall'AST e' ### **un buco dell'AST**, non una curiosita' |
| **4** | ### **IL PUNTO `(d)` DEL MANDATO:** quanti nati hanno un `perc_geom` ereditato ### **diverso da `-1`**, ### **PER EVENTO** |
| **5** | ### **CHE COSA DAREBBE LA DERIVAZIONE, misurato SENZA toccare il simulatore:** si avvolge `nascita` e alla ### **FINE** di ogni chiamata si calcola la formula sui nati |

### 📌 **PERCHE' IL PEZZO `5` SI MISURA ALLA FINE DI `nascita` E NON DOVE STA LA REGOLA:**
la regola di `perc_geom` sta al posto **17** e `tw` al posto **31**, quindi ### **dove sta la
regola oggi il `tw` dei nuovi archi NON ESISTE ANCORA.** Misurare li' darebbe `-1` **per il
motivo sbagliato** — cioe' misurerebbe la costante, non la derivazione.

## ⛔ **LA SEMANTICA DELLA SPIA, e va letta PRIMA del pezzo `3`**

Il descrittore intercetta il ### **REBIND** *(`self.perc_geom = ...`)*, **non** la scrittura
### **IN POSTO** *(`self.perc_geom[:n] = ...`, che e' un `__get__` seguito da `__setitem__`
sull'array)*. ### ➜ **Quindi `chi_basc` -- che e' LA DEFINIZIONE -- NON compare nella
colonna del runtime**, e nel pezzo `3` finirebbe fra le *<<viste dall'AST e mai girate>>*
### **come se fosse codice morto. NON LO E'.**

### ✅ **E NON SI CURA CON PIU' MACCHINARIO, SI CURA COL CONTATORE CHE IL REPO HA GIA':**
`_g_chibasc_su_geom` *(`:7559`)* conta ### **quante volte `chi_basc` scrive la GEOMETRIA**, e
`_g_chibasc_su_chi` *(`:7562`)* quante volte scrive la carica. ### **Il referto li riporta**, e
cosi' la riga `:7560` e' spiegata da un ### **numero misurato** invece che da una mia frase.

### ⚠ **E IL PEZZO `5` E' LA MISURA CHE DEVE PRECEDERE IL CODICE:** da' il contatore `-1`/`+1`
**atteso** e il numero del punto `(d)` ### **prima** che il codice esista, cosi' il sigillo ha
una previsione da confrontare invece di un risultato da accettare.

**COMANDO:** `python csv/_test_fork/_censimento_perc_geom.py`
**USCITA:** `csv/_test_fork/_censimento_perc_geom/`
"""
import ast
import contextlib
import hashlib
import importlib.util
import io
import json
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_QUI, ".."))
import _presidio   # noqa: E402

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, os.path.join(RADICE, "csv"))
import numpy as np   # noqa: E402
import _cli_flag     # noqa: E402
import _passo        # noqa: E402

SIM = os.path.join(RADICE, "soliton_simulator.py")
FUORI = os.path.join(_QUI, "_censimento_perc_geom")
NL = chr(10)
GRANDEZZA = "perc_geom"
# ### LE TRE SCENE DEL COMMIT 4, e sono un DATO di questo strumento
SCENE = (("corta", 11, 72), ("lunga", 11, 150), ("altro_seme", 12, 72))


def blob(p):
    return hashlib.sha1(io.open(p, "rb").read()).hexdigest()


# ----------------------------------------------------------------------------- PEZZO 1: l'AST
class Scritture(ast.NodeVisitor):
    """Ogni scrittura di `perc_geom`, con la funzione che la contiene.

    ### LE QUATTRO FORME CHE CERCA, e le cerca TUTTE perche' trovarne tre e dire
    *<<zero nella quarta>>* e' la forma di `FALSO-ZERO`:
      `x.perc_geom = ...` · `x.perc_geom[...] = ...` · `setattr(x, "perc_geom", ...)` ·
      e il nome in una VARIABILE (`setattr(x, nome, ...)`), che si DICHIARA come non risolto.
    """

    def __init__(self, righe):
        self.righe = righe
        self.trovate = []
        self.pila = ["<modulo>"]
        self.setattr_variabile = []

    def _dentro(self):
        return self.pila[-1]

    def visit_FunctionDef(self, nodo):
        self.pila.append(nodo.name)
        self.generic_visit(nodo)
        self.pila.pop()

    visit_AsyncFunctionDef = visit_FunctionDef

    def _aggiungi(self, riga, forma):
        testo = self.righe[riga - 1].strip() if 0 < riga <= len(self.righe) else "?"
        self.trovate.append({"riga": riga, "dentro": self._dentro(), "forma": forma,
                             "testo": testo[:160], "classe": _classifica(testo)})

    def visit_Assign(self, nodo):
        for t in nodo.targets:
            if isinstance(t, ast.Attribute) and t.attr == GRANDEZZA:
                self._aggiungi(t.lineno, "attributo")
            elif (isinstance(t, ast.Subscript) and isinstance(t.value, ast.Attribute)
                  and t.value.attr == GRANDEZZA):
                self._aggiungi(t.value.lineno, "in posto (slice)")
        self.generic_visit(nodo)

    def visit_AugAssign(self, nodo):
        t = nodo.target
        if isinstance(t, ast.Attribute) and t.attr == GRANDEZZA:
            self._aggiungi(t.lineno, "aumento (+=)")
        elif (isinstance(t, ast.Subscript) and isinstance(t.value, ast.Attribute)
              and t.value.attr == GRANDEZZA):
            self._aggiungi(t.value.lineno, "aumento in posto")
        self.generic_visit(nodo)

    def visit_Call(self, nodo):
        if (isinstance(nodo.func, ast.Name) and nodo.func.id == "setattr"
                and len(nodo.args) >= 2):
            arg = nodo.args[1]
            if isinstance(arg, ast.Constant) and arg.value == GRANDEZZA:
                self._aggiungi(nodo.lineno, "setattr col nome scritto")
            elif not isinstance(arg, ast.Constant):
                self.setattr_variabile.append({"riga": nodo.lineno, "dentro": self._dentro()})
        self.generic_visit(nodo)


def _classifica(testo):
    t = testo.replace(" ", "")
    if "np.zeros(0" in t:
        return "inizializza (array VUOTO: nessun valore)"
    if "concatenate" in t:
        return "ESTENDE (nasce un valore per un nodo nuovo)"
    if ("perc_geom[:" in t) or ("perc_geom[" in t and "]=" in t):
        return "in posto (riscrive nodi che ESISTONO)"
    return "altro"


# ------------------------------------------------------------------- PEZZO 2: la spia, runtime
class Diario:
    def __init__(self):
        self.scritture = []
        self.len_prec = None

    def scrivi(self, obj, v, dove, riga):
        try:
            nuovo = int(len(v))
        except TypeError:
            nuovo = -1
        prec = self.len_prec
        cresciuta = (prec is not None and nuovo > prec)
        voce = {"dove": dove, "riga": riga, "len_prima": prec, "len_dopo": nuovo,
                "cresciuta": bool(cresciuta)}
        if cresciuta:
            try:
                voce["valori_nuovi"] = [int(x) for x in np.asarray(v)[prec:nuovo]]
            except Exception:
                voce["valori_nuovi"] = None
        self.scritture.append(voce)
        self.len_prec = nuovo


class Spia:
    """Descrittore di dato: il valore resta in `obj.__dict__` COL SUO NOME VERO.

    ### E' la tecnica gia' provata da `_copertura_derivate.py`: ### **`vars(net)` lo
    vede come prima**, quindi il controllo unico e la regola di confronto ### **non si
    accorgono di niente.** Un'ombra con un altro nome avrebbe falsato cio' che il
    controllo guarda.
    """

    def __init__(self, nome, diario):
        self.nome = nome
        self.diario = diario

    def __get__(self, obj, tipo=None):
        if obj is None:
            return self
        try:
            return obj.__dict__[self.nome]
        except KeyError:
            raise AttributeError(self.nome)

    def __set__(self, obj, v):
        f = sys._getframe(1)
        self.diario.scrivi(obj, v, f.f_code.co_name, f.f_lineno)
        obj.__dict__[self.nome] = v

    def __delete__(self, obj):
        obj.__dict__.pop(self.nome, None)


# --------------------------------------------- PEZZO 5: che cosa DAREBBE la derivazione, oggi
def derivazione(sim, net):
    """### LA FORMULA DI `chi_basc`, applicata com'e' alla nascita. E le DUE differenze
    sono dichiarate nel referto: il grado si RICALCOLA *(`_grado()` non e' ancora
    girato)* e la torsione e' `self.tw` *(alla nascita non esiste lo SNAPSHOT `_tw_t`)*.
    """
    n = int(len(net.phi))
    i = np.asarray(net.i)
    j = np.asarray(net.j)
    tw = np.asarray(net.tw, dtype=float)
    if n == 0 or len(i) == 0:
        return np.full(n, -1, dtype=int), np.zeros(n)
    deg = np.maximum(np.bincount(i, minlength=n) + np.bincount(j, minlength=n), 1)
    twabs = np.abs(tw)
    twn = np.zeros(n)
    np.add.at(twn, i, twabs)
    np.add.at(twn, j, twabs)
    twn = twn / deg[:n]
    return np.where(twn > sim.PHI_CRIT, 1, -1).astype(int), twn


def una_scena(nome, seme, passi, stampa):
    """Importa a mano per potersi mettere FRA l'import e `_applica_flag`.

    ### `H-P3` e' rispettato nella sostanza: si passa per le STESSE DUE funzioni che
    chiama il driver (`_cli` e `_applica_flag`), e ### **nessun attributo e' messo a
    mano.** La spia va installata prima, perche' `_applica_flag` ### **semina**, e la
    scrittura della semina e' uno dei siti del censimento.
    """
    spec = importlib.util.spec_from_file_location("_sim_cens_%s" % nome, SIM)
    sim = importlib.util.module_from_spec(spec)
    diario = Diario()
    nati = []
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(sim)
        setattr(sim.Rete, GRANDEZZA, Spia(GRANDEZZA, diario))
        # ### LA FINESTRA DEL PEZZO 5: alla FINE di ogni `nascita`, per EVENTO
        _nascita_vera = sim.nascita

        def nascita_spiata(net, evento, c):
            n0 = int(c["n0"])
            fuori = _nascita_vera(net, evento, c)
            der, twn = derivazione(sim, net)
            eredita = np.asarray(net.perc_geom)
            n = int(len(net.phi))
            for k in range(n0, n):
                nati.append({"evento": evento, "nodo": int(k),
                             "ereditato": int(eredita[k]) if k < len(eredita) else None,
                             "derivato": int(der[k]), "twn": float(twn[k])})
            return fuori

        sim.nascita = nascita_spiata
        # e le regole chiamano `nascita` per nome di modulo? NO: `mitosi` la chiama come
        # `nascita(self, ...)`, cioe' risolve il GLOBALE del modulo -> la spia prende.
        _S0, argv = _cli_flag.argv_del_driver(
            extra=["--seme=%d" % seme], dest=os.path.join(FUORI, "_scarto_%s" % nome))
        vecchia = list(sys.argv)
        sys.argv = list(argv)
        try:
            a = sim._cli()
            sim._applica_flag(a)
        finally:
            sys.argv = vecchia
        sim._applica_regime(a)
        sim._NMASSE_VIDEO["n"] = max(2, int(getattr(a, "nmasse", 2)))
        sim._NMASSE_VIDEO["sep"] = float(getattr(a, "sep", 3.0))
        sim._NMASSE_VIDEO["size"] = None
        sim.avvia_test("MASSE-COERENTI")()
        net = sim.net
        for _ in range(passi):
            _passo.passo_pieno(sim, net)
    cont = {c: int(getattr(net, c, 0))
            for c in ("_g_chibasc_su_geom", "_g_chibasc_su_chi")}
    return sim, diario, nati, cont


def principale():
    righe_out = []

    def stampa(*x):
        s = " ".join(str(y) for y in x)
        righe_out.append(s)
        print(s)

    if not os.path.isdir(FUORI):
        os.makedirs(FUORI)
    sorgente = io.open(SIM, encoding="utf-8").read()
    righe_sim = sorgente.split(NL)

    stampa("=" * 100)
    stampa("IL CENSIMENTO DI `perc_geom`: dove nasce un suo valore per un nodo NUOVO")
    stampa("=" * 100)
    stampa("  simulatore .. %s (sha1 byte grezzi)" % blob(SIM)[:8])
    stampa("  strumento ... %s" % blob(os.path.abspath(__file__))[:8])
    stampa("  scene ....... %s" % ", ".join("%s(seme %d, %d passi)" % s for s in SCENE))
    stampa("")

    # --------------------------------------------------------------- PEZZO 0
    with contextlib.redirect_stdout(io.StringIO()):
        spec = importlib.util.spec_from_file_location("_sim_cens0", SIM)
        s0 = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(s0)
    ordine = list(s0.ORDINE_DI_NASCITA)
    stampa("-" * 100)
    stampa("PEZZO 0 -- IL FATTO STRUTTURALE: i posti in `ORDINE_DI_NASCITA`, e le CLASSI")
    stampa("    PHI_CRIT = %.15f   (> 0 ? %s  -> twn = 0 da' -1 col confronto STRETTO)"
           % (s0.PHI_CRIT, s0.PHI_CRIT > 0))
    stampa("")
    stampa("    %-4s %-12s %-26s %s" % ("pos", "grandezza", "classe (divisione)", "nota"))
    interessanti = ("i", "j", "_deg", "perc_chi", GRANDEZZA, "tw", "twp")
    posti = {}
    for k, nome in enumerate(ordine):
        if nome not in interessanti:
            continue
        posti[nome] = k
        v = s0.REGOLE_NASCITA.get(("divisione", nome)) or {}
        nota = ""
        if v.get("classe") == "collocata":
            nota = "<-- COLLOCATA: gira DOPO nascita(), quindi DENTRO la nascita e' STANTIO"
        stampa("    %-4d %-12s %-26s %s" % (k, nome, str(v.get("classe"))[:26], nota))
    stampa("")
    pg, ptw = posti.get(GRANDEZZA), posti.get("tw")
    stampa("    ### `perc_geom` sta al posto %s, `tw` al posto %s." % (pg, ptw))
    if pg is not None and ptw is not None and pg < ptw:
        stampa("    ### ==> QUANDO LA REGOLA DI `perc_geom` GIRA, IL `tw` DEI NUOVI ARCHI")
        stampa("    ###     NON ESISTE ANCORA. Una derivazione scritta LI' leggerebbe lo")
        stampa("    ###     stato VECCHIO e darebbe -1 PER IL MOTIVO SBAGLIATO: sarebbe la")
        stampa("    ###     COSTANTE -1 TRAVESTITA DA DERIVAZIONE.")
        stampa("    ###     SERVE IL VINCOLO 3: `perc_geom` DOPO `tw`.")
    else:
        stampa("    ### l'ordine NON e' quello atteso: il disegno del commit 5 va rifatto.")
    stampa("")

    # --------------------------------------------------------------- PEZZO 1
    v = Scritture(righe_sim)
    v.visit(ast.parse(sorgente))
    stampa("-" * 100)
    stampa("PEZZO 1 -- DALL'AST: ogni scrittura di `perc_geom` in TUTTO il file (anche rami spenti)")
    stampa("    trovate: %d" % len(v.trovate))
    stampa("")
    for x in sorted(v.trovate, key=lambda y: y["riga"]):
        stampa("    :%-6d %-26s %s" % (x["riga"], x["dentro"][:26], x["classe"]))
        stampa("            %s" % x["testo"])
    if v.setattr_variabile:
        stampa("")
        stampa("    ### LIMITE DICHIARATO: %d `setattr` col nome in una VARIABILE, non risolti:"
               % len(v.setattr_variabile))
        for x in v.setattr_variabile:
            stampa("        :%-6d %s" % (x["riga"], x["dentro"]))
    else:
        stampa("")
        stampa("    ### nessun `setattr` col nome in una variabile: niente da dichiarare.")
    estendono = [x for x in v.trovate if x["classe"].startswith("ESTENDE")]
    stampa("")
    stampa("    ### LE SCRITTURE CHE FANNO NASCERE UN VALORE (estendono): %d" % len(estendono))
    for x in sorted(estendono, key=lambda y: y["riga"]):
        stampa("        :%-6d %s" % (x["riga"], x["dentro"]))
    stampa("")

    # ------------------------------------------------------- PEZZI 2, 4, 5
    tutte = {}
    for nome, seme, passi in SCENE:
        stampa("-" * 100)
        stampa("SCENA `%s` -- seme %d, %d passi" % (nome, seme, passi))
        sim, diario, nati, cont = una_scena(nome, seme, passi, stampa)
        viste = {}
        for s in diario.scritture:
            k = (s["dove"], s["riga"])
            d = viste.setdefault(k, {"n": 0, "cresciute": 0, "nuovi": 0})
            d["n"] += 1
            if s["cresciuta"]:
                d["cresciute"] += 1
                d["nuovi"] += (s["len_dopo"] - s["len_prima"])
        stampa("  PEZZO 2 -- DAL RUNTIME: %d scritture, da %d righe distinte"
               % (len(diario.scritture), len(viste)))
        stampa("    %-28s %-8s %8s %8s %8s" % ("funzione", "riga", "scritt.", "crescite",
                                               "nodi nuovi"))
        for (dove, riga), d in sorted(viste.items(), key=lambda y: y[0][1]):
            stampa("    %-28s :%-7d %8d %8d %8d"
                   % (dove[:28], riga, d["n"], d["cresciute"], d["nuovi"]))
        stampa("")
        stampa("  ### E LA SPIA VEDE I *REBIND*, NON LE SCRITTURE IN POSTO: `chi_basc`")
        stampa("  ###   (`:7560`), che e' LA DEFINIZIONE, scrive con `perc_geom[:n] = ...`")
        stampa("  ###   e quindi NON compare sopra. NON e' codice morto, e il numero lo dice:")
        stampa("  ###     _g_chibasc_su_geom = %d   (chi_basc scrive la GEOMETRIA)"
               % cont["_g_chibasc_su_geom"])
        stampa("  ###     _g_chibasc_su_chi  = %d   (chi_basc scrive la CARICA)"
               % cont["_g_chibasc_su_chi"])
        if cont["_g_chibasc_su_geom"] == 0:
            stampa("  ### ⛔ ZERO: in questa configurazione `chi_basc` NON scrive la")
            stampa("  ###   geometria, e allora la DEFINIZIONE non gira: il commit 5 va")
            stampa("  ###   ridisegnato, perche' deriverebbe da una legge spenta.")
        # --- PEZZO 4 + 5
        per_ev = {}
        for x in nati:
            d = per_ev.setdefault(x["evento"], {"n": 0, "er_m1": 0, "er_p1": 0,
                                                "der_m1": 0, "der_p1": 0, "diversi": 0})
            d["n"] += 1
            d["er_m1" if x["ereditato"] == -1 else "er_p1"] += 1
            d["der_m1" if x["derivato"] == -1 else "der_p1"] += 1
            if x["ereditato"] != x["derivato"]:
                d["diversi"] += 1
        stampa("")
        stampa("  PEZZO 4 e 5 -- I NATI: ereditato contro DERIVATO, per evento")
        stampa("    %-12s %6s | %8s %8s | %8s %8s | %s"
               % ("evento", "nati", "er. -1", "er. +1", "der. -1", "der. +1", "DIVERSI"))
        tot_div = 0
        for ev in sorted(per_ev):
            d = per_ev[ev]
            tot_div += d["diversi"]
            stampa("    %-12s %6d | %8d %8d | %8d %8d | %d"
                   % (ev, d["n"], d["er_m1"], d["er_p1"], d["der_m1"], d["der_p1"],
                      d["diversi"]))
        twn_max = max([x["twn"] for x in nati], default=0.0)
        stampa("    ### `twn` dei nati: MAX %.6e  contro PHI_CRIT %.6f  -> sopra soglia? %s"
               % (twn_max, sim.PHI_CRIT, twn_max > sim.PHI_CRIT))
        stampa("")
        if tot_div == 0:
            stampa("  ### IL PUNTO (d) DA' ZERO IN QUESTA SCENA: nessun nato ha un `perc_geom`")
            stampa("  ###   ereditato diverso dalla derivazione. ==> IL COMMIT 5 SAREBBE")
            stampa("  ###   BYTE-IDENTICO QUI, e i bracci (a)-(c) NON PROVEREBBERO NIENTE:")
            stampa("  ###   il sigillo deve appoggiarsi a un CONTROLLO POSITIVO COSTRUITO.")
        else:
            stampa("  ### IL PUNTO (d): %d nati su %d hanno l'ereditato DIVERSO dal derivato."
                   % (tot_div, len(nati)))
            stampa("  ###   ==> IL COMMIT 5 NON E' BYTE-IDENTICO in questa scena, e la PRIMA")
            stampa("  ###   differenza attesa e' `perc_geom` di quei nati.")
        stampa("")
        tutte[nome] = {"seme": seme, "passi": passi, "contatori_chibasc": cont,
                       "scritture_runtime": [{"dove": k[0], "riga": k[1], **d}
                                             for k, d in sorted(viste.items(),
                                                                key=lambda y: y[0][1])],
                       "nati": len(nati), "per_evento": per_ev,
                       "twn_max_dei_nati": twn_max, "diversi": tot_div}

    # --------------------------------------------------------------- PEZZO 3
    stampa("-" * 100)
    stampa("PEZZO 3 -- LA DIFFERENZA `AST` meno `RUNTIME`, riga per riga COL MOTIVO")
    righe_ast = {x["riga"] for x in v.trovate}
    righe_rt = set()
    for nome in tutte:
        for s in tutte[nome]["scritture_runtime"]:
            righe_rt.add(s["riga"])
    solo_ast = sorted(righe_ast - righe_rt)
    solo_rt = sorted(righe_rt - righe_ast)
    stampa("    righe che SCRIVONO secondo l'AST ........ %d" % len(righe_ast))
    stampa("    righe che hanno SCRITTO nel runtime ..... %d" % len(righe_rt))
    stampa("")
    stampa("    ### VISTE DALL'AST E MAI GIRATE: %d" % len(solo_ast))
    for r in solo_ast:
        x = [y for y in v.trovate if y["riga"] == r][0]
        stampa("        :%-6d %-26s %s" % (r, x["dentro"][:26], x["classe"]))
        stampa("                %s" % x["testo"])
        if "in posto" in x["classe"] or "in posto" in x["forma"]:
            stampa("                ### IL MOTIVO: e' una scrittura IN POSTO, e la spia")
            stampa("                ###   intercetta i REBIND. NON vuol dire che non gira --")
            stampa("                ###   per `chi_basc` il contatore `_g_chibasc_su_geom`")
            stampa("                ###   sopra dice quante volte ha girato DAVVERO.")
        elif "inizializza" in x["classe"]:
            stampa("                ### IL MOTIVO: array VUOTO, nessun valore nasce qui")
            stampa("                ###   (e il rebind lo vede: se non compare nel runtime e'")
            stampa("                ###   perche' la riga sta in un ramo non percorso).")
    stampa("")
    if solo_rt:
        stampa("    ### GIRATE E NON VISTE DALL'AST: %d -- E' UN BUCO DELL'AST, NON UNA"
               % len(solo_rt))
        stampa("    ###   CURIOSITA': la colonna dell'AST non e' completa.")
        for r in solo_rt:
            stampa("        :%d" % r)
    else:
        stampa("    ### GIRATE E NON VISTE DALL'AST: ZERO. Le due colonne si chiudono, e")
        stampa("    ###   QUESTO E' IL CONTROLLO che lo zero dell'AST non sia un FALSO-ZERO.")
    stampa("")
    stampa("=" * 100)
    stampa("### IL VERDETTO DEL CENSIMENTO")
    stampa("###   %d siti dall'AST, di cui %d ESTENDONO (fanno nascere un valore)."
           % (len(v.trovate), len(estendono)))
    stampa("###   %d righe hanno scritto nel runtime; %d viste dall'AST non girano; %d"
           % (len(righe_rt), len(solo_ast), len(solo_rt)))
    stampa("###   girate e non viste dall'AST.")
    dtot = sum(tutte[n]["diversi"] for n in tutte)
    stampa("###   IL PUNTO (d), sulle tre scene: %d nati con ereditato != derivato." % dtot)
    stampa("=" * 100)

    esito = {"blob_sim": blob(SIM), "blob_strumento": blob(os.path.abspath(__file__)),
             "PHI_CRIT": s0.PHI_CRIT, "posti_ordine_nascita": posti,
             "ordine_nascita": ordine,
             "ast": v.trovate, "ast_setattr_variabile": v.setattr_variabile,
             "ast_estendono": estendono,
             "scene": tutte, "solo_ast": solo_ast, "solo_runtime": solo_rt,
             "punto_d_totale": dtot}
    io.open(os.path.join(FUORI, "_censimento.json"), "w", encoding="utf-8",
            newline=NL).write(json.dumps(esito, indent=1, ensure_ascii=False, default=str))
    io.open(os.path.join(FUORI, "_corsa.txt"), "w", encoding="utf-8",
            newline=NL).write(NL.join(righe_out) + NL)
    print("  referto .. %s" % FUORI)


if __name__ == "__main__":
    principale()
