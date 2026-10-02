# -*- coding: utf-8 -*-
"""**LE DERIVATE ALLA NASCITA: le letture SPORCHE e, soprattutto, LA COPERTURA.**

La misura che il `COMMIT 4` *(le derivate sporche, par.(d) del piano)* richiede
### **prima** del codice. E la domanda che la governa e' di Luca:

> ### **<<Come sai che il veleno e' passato per tutte le leggi se fai solo 72 passi?>>**

### ⛔ **Il `NaN` prova SOLO le letture che nel run AVVENGONO.** Uno zero del veleno
### **senza la copertura e' un `FALSO-ZERO`** — e sarebbe il nono di una forma che in
due giorni ne ha collezionati otto.

## I QUATTRO PEZZI, e sono i criteri fissati PRIMA dei numeri

| | |
|---|---|
| **1** | ### **COPERTURA DAL RUNTIME:** per ogni derivata, ### **quali RIGHE di quali funzioni l'hanno LETTA** dopo una nascita — ### **tracciamento, non stima** |
| **2** | ### **LETTURE DALL'AST:** ### **tutte** le letture di ogni derivata in ### **tutto** il simulatore, ### **compresi i rami che non girano** |
| **3** | ### **LA DIFFERENZA `2` meno `1`, RIGA PER RIGA**, ciascuna ### **col suo MOTIVO** |
| **4** | ### **PIU' DI UNA SCENA:** seme 11/72 passi, un run ### **LUNGO (150)** e un ### **ALTRO SEME**, coi loro eventi di nascita |

### \U0001f4cc **E IL VERDETTO SI SCRIVE COSI', e non altrimenti:**
> ### **<<zero letture sporche su `N` PROVATE, `M` NON PROVATE (elencate)>>**

### ⛔ **MAI <<nessuna derivata sporca>>:** quella frase afferma qualcosa su cio' che
### **non e' stato guardato.**

## COME SI MISURA, e perche' UNA sola instrumentazione basta per DUE domande

Sulle 10 voci di `REGISTRO_DERIVATE` *(### **derivate dal sorgente**, non scelte a
mano)* si installa un ### **DESCRITTORE DI DATO** sulla classe `Rete`. Il valore resta
### **in `net.__dict__` col suo nome vero** — cosi' `vars(net)` lo vede come prima, e
il controllo unico e la regola di confronto non si accorgono di niente.

Ogni lettura e ogni scrittura registrano ### **`(funzione, riga)`** del chiamante
*(`sys._getframe(1)`)*. Dentro la ### **finestra della nascita** *(dal ritorno di
`mitosi` con almeno un nato, fino alla fine del passo)*:

| | |
|---|---|
| una ### **LETTURA prima della prima SCRITTURA** | e' una ### **lettura SPORCA**, ed e' la domanda di sempre |
| l'insieme delle ### **righe che leggono** | e' la ### **COPERTURA**, ed e' la domanda nuova |

### ✅ **Le due domande hanno la stessa instrumentazione**, e questo non e' un
risparmio: e' la ragione per cui ### **la copertura e' DELLO STESSO run** che da' lo
zero, invece di essere una stima fatta a parte.

**COMANDO:** `python csv/_test_fork/_copertura_derivate.py`
**USCITA:** `csv/_test_fork/_copertura_derivate/`
"""
import ast
import contextlib
import hashlib
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
import _cli_flag   # noqa: E402
import _passo      # noqa: E402

SIM = os.path.join(RADICE, "soliton_simulator.py")
FUORI = os.path.join(_QUI, "_copertura_derivate")
NL = chr(10)
# ### LE TRE SCENE, dichiarate: il mandato chiede piu' di una.
SCENE = (("corta", 11, 72), ("lunga", 11, 150), ("altro_seme", 12, 72))
# le funzioni che NON stanno sotto `esegui_passo`: una lettura la' non e' mai provata
# da un veleno applicato dentro il passo.
# ### I LETTORI CHE SONO PRESIDIO, NON LEGGE -- e l'elenco e' DICHIARATO, non derivato.
#   Il collaudo su quattro passi ha mostrato che fra i lettori di OGNI derivata c'e'
#   ### il CONTROLLO UNICO, che scorre il registro con `getattr(net, nome, None)`.
#   ### QUELLE LETTURE NON SONO <<una legge che legge una derivata>>: sono il presidio
#   che GUARDA -- e col veleno sono ### ESATTAMENTE CIO' CHE DEVE LEGGERE il `NaN`.
#   Contarle fra le letture sporche direbbe che il controllo e' un difetto.
#   ### E' un elenco DICHIARATO: se un domani un presidio nuovo legge le derivate e non
#   e' qui, le sue letture finiscono fra quelle di fisica -- cioe' l'errore cade dalla
#   parte PRUDENTE (una lettura in piu' da spiegare, non una in meno).
LETTORI_DI_PRESIDIO = ("_ferma_se_registro_incoerente", "rapporto_guardie", "_forma_di",
                       "_registro_coerente", "_censimento", "grandezze", "foto",
                       "_diagnostica", "stato_registro")
FUORI_DAL_PASSO = ("_applica_flag", "_cli", "esegui_headless", "main", "_salva_scena",
                   "rilassa_disegno", "semina")


def blob(p):
    return hashlib.sha1(io.open(p, "rb").read()).hexdigest()


def derivate_dal_sorgente(albero):
    """Le voci di `REGISTRO_DERIVATE`, DERIVATE dal sorgente e non scelte a mano."""
    for n in ast.walk(albero):
        if (isinstance(n, ast.Assign) and len(n.targets) == 1
                and isinstance(n.targets[0], ast.Name)
                and n.targets[0].id == "REGISTRO_DERIVATE"):
            fuori = []
            for e in n.value.elts:
                if (isinstance(e, (ast.Tuple, ast.List)) and e.elts
                        and isinstance(e.elts[0], ast.Constant)):
                    fuori.append(e.elts[0].value)
            return fuori
    return []


def _letta_qui(nodo, nomi):
    """Il nodo e' una LETTURA di una derivata? Restituisce il nome, o `None`.

    ### ⛔ E IL PRIMO COLLAUDO HA TROVATO QUI UN FALSO ZERO, il NONO della serie:
    la prima stesura guardava ### **solo `self.<nome>`** (un `ast.Attribute`), e il
    referto diceva ### **16 letture, TUTTE di `_sin2_vir`, e ZERO per le altre nove** --
    mentre il ### **runtime ne trovava per tutte e dieci.** Le altre si leggono con
    ### **`getattr(self, "<nome>", <ripiego>)`**, che e' una `ast.Call` e non un
    `ast.Attribute`. ### **Un conteggio dall'AST che ignora `getattr` non e' un
    conteggio: e' un elenco di una forma sintattica.**

    ### ✅ **E l'ha trovato IL COLLAUDO SU QUATTRO PASSI, non il giro vero:** il
    confronto fra le due colonne (AST contro runtime) era ### **il controllo positivo**
    di questo pezzo, ed e' la ragione per cui esiste.
    """
    if (isinstance(nodo, ast.Attribute) and isinstance(nodo.ctx, ast.Load)
            and isinstance(nodo.value, ast.Name) and nodo.value.id == "self"
            and nodo.attr in nomi):
        return nodo.attr
    # `getattr(self, "<nome>", ...)` -- e `hasattr` NON e' una lettura del valore,
    #   ma passa dal descrittore, quindi il runtime la vede: si conta anche quella.
    if (isinstance(nodo, ast.Call) and isinstance(nodo.func, ast.Name)
            and nodo.func.id in ("getattr", "hasattr") and len(nodo.args) >= 2
            and isinstance(nodo.args[0], ast.Name) and nodo.args[0].id in ("self", "net")
            and isinstance(nodo.args[1], ast.Constant)
            and nodo.args[1].value in nomi):
        return nodo.args[1].value
    return None


def _valori_possibili(funzione, nomi):
    """`{variabile: set(nomi di derivata)}` per le assegnazioni di LETTERALI.

    ### ⛔ IL SECONDO BUCO CHE IL COLLAUDO HA TROVATO: `_chi_geom_nodi` e
    `_fatt_cs_ultimo` restavano a ZERO nell'AST mentre il runtime li leggeva, e il
    motivo e' al `:7285`:

        `_cache_tors = '_chi_geom_nodi' if CHI_COOP else '_chi_core_nodi'`

    ### **Il nome della grandezza finisce in una VARIABILE**, e poi si legge con
    `getattr(self, _cache_tors)`. ### **Un conteggio che si ferma al letterale
    nell'argomento non la vede** -- e la vedrebbe il runtime, cioe' le due colonne
    sarebbero incoerenti ### **senza che nessuna delle due sia sbagliata.**

    ### ✅ Qui si risolvono i casi in cui i valori possibili sono ### **letterali
    nello stesso corpo** (anche dentro un `IfExp`), e il resto resta nell'elenco
    *<<per NOME VARIABILE>>* -- ### **dichiarato come limite, non nascosto.**
    """
    fuori = {}
    for n in ast.walk(funzione):
        if not isinstance(n, ast.Assign) or len(n.targets) != 1:
            continue
        b = n.targets[0]
        if not isinstance(b, ast.Name):
            continue
        viste = {c.value for c in ast.walk(n.value)
                 if isinstance(c, ast.Constant) and isinstance(c.value, str)
                 and c.value in nomi}
        if viste:
            fuori.setdefault(b.id, set()).update(viste)
    return fuori


def _getattr_variabile(nodo):
    """Un `getattr(self, <VARIABILE>)`: il runtime lo vede, l'AST NON sa su CHI."""
    return (isinstance(nodo, ast.Call) and isinstance(nodo.func, ast.Name)
            and nodo.func.id in ("getattr", "hasattr", "setattr") and len(nodo.args) >= 2
            and isinstance(nodo.args[0], ast.Name) and nodo.args[0].id in ("self", "net")
            and not isinstance(nodo.args[1], ast.Constant))


def letture_dall_ast(albero, nomi):
    """TUTTE le letture `self.<deriv>` nel file: `{deriv: [(funzione, riga, gate)]}`.

    ### Comprese quelle nei rami che non girano — e' il pezzo **2** del mandato.
    Il `gate` e' l'elenco delle condizioni `if` che racchiudono la riga, come testo:
    serve al pezzo **3** per dire ### **perche'** una riga non e' stata provata.
    """
    fuori = {k: [] for k in nomi}
    variabili = []
    possibili = {}

    def scendi(nodo, funzione, gate):
        for figlio in ast.iter_child_nodes(nodo):
            if isinstance(figlio, ast.FunctionDef):
                possibili[figlio.name] = _valori_possibili(figlio, fuori)
                scendi(figlio, figlio.name, gate)
                continue
            if isinstance(figlio, ast.If):
                t = ast.unparse(figlio.test)
                for st in figlio.body:
                    scendi(st, funzione, gate + [t])
                for st in figlio.orelse:
                    scendi(st, funzione, gate + ["not (%s)" % t])
                # e la condizione stessa puo' leggere una derivata
                for x in ast.walk(figlio.test):
                    nx = _letta_qui(x, fuori)
                    if nx:
                        fuori[nx].append((funzione, x.lineno, list(gate)))
                continue
            nome = _letta_qui(figlio, fuori)
            if nome:
                fuori[nome].append((funzione, figlio.lineno, list(gate)))
            elif (_getattr_variabile(figlio)
                  and isinstance(figlio.args[1], ast.Name)
                  and figlio.args[1].id in possibili.get(funzione, {})):
                # ### il nome e' in una VARIABILE, ma i suoi valori possibili sono
                #   LETTERALI nello stesso corpo: si attribuisce a TUTTI, perche'
                #   quale dei due scatti dipende da un flag -- e il pezzo 3 lo dira'.
                for _n in sorted(possibili[funzione][figlio.args[1].id]):
                    fuori[_n].append((funzione, figlio.lineno, list(gate)))
            elif _getattr_variabile(figlio):
                variabili.append({"funzione": funzione, "riga": figlio.lineno,
                                  "codice": ast.unparse(figlio)[:120]})
            scendi(figlio, funzione, gate)

    scendi(albero, "<modulo>", [])
    for k in fuori:
        visti, puliti = set(), []
        for f, r, g in fuori[k]:
            if (f, r) in visti:
                continue
            visti.add((f, r))
            puliti.append({"funzione": f, "riga": r, "gate": g})
        fuori[k] = sorted(puliti, key=lambda x: x["riga"])
    visti, var = set(), []
    for v in variabili:
        if (v["funzione"], v["riga"]) in visti:
            continue
        visti.add((v["funzione"], v["riga"]))
        var.append(v)
    return fuori, sorted(var, key=lambda x: x["riga"])


class Spia:
    """Il DESCRITTORE: registra `(funzione, riga)` di ogni lettura e scrittura.

    ### Il valore resta in `instance.__dict__` COL SUO NOME VERO, e non e' un
    dettaglio: `vars(net)` lo vede come prima, quindi ### **il controllo unico e la
    regola di confronto non si accorgono di niente.** Un'ombra con un altro nome
    avrebbe cambiato cio' che il controllo guarda — cioe' avrebbe falsato la misura
    nel modo piu' subdolo.
    """

    def __init__(self, nome, diario):
        self.nome = nome
        self.diario = diario

    def __get__(self, obj, tipo=None):
        if obj is None:
            return self
        f = sys._getframe(1)
        self.diario.leggi(self.nome, f.f_code.co_name, f.f_lineno)
        try:
            return obj.__dict__[self.nome]
        except KeyError:
            raise AttributeError(self.nome)

    def __set__(self, obj, v):
        f = sys._getframe(1)
        self.diario.scrivi(self.nome, f.f_code.co_name, f.f_lineno)
        obj.__dict__[self.nome] = v

    def __delete__(self, obj):
        obj.__dict__.pop(self.nome, None)


class Diario:
    """Che cosa e' stato letto e scritto, e DOVE. Nella finestra e fuori."""

    def __init__(self, nomi):
        self.nomi = list(nomi)
        self.finestra = False
        self.coperte = {k: set() for k in nomi}        # (funzione, riga) che LEGGONO
        self.coperte_finestra = {k: set() for k in nomi}
        self.coperte_presidio = {k: set() for k in nomi}   # il CONTROLLO che guarda
        self.scritte = {k: set() for k in nomi}
        self.sporche = []                              # letture PRIMA della scrittura
        self.gia_scritta = set()                       # nella finestra corrente
        self.passi_con_nascita = 0

    def apri_finestra(self):
        self.finestra = True
        self.gia_scritta = set()
        self.passi_con_nascita += 1

    def chiudi_finestra(self):
        self.finestra = False

    def leggi(self, nome, funzione, riga):
        # ### IL PRESIDIO NON E' UNA LEGGE, e tenerli separati e' il punto: il controllo
        #   unico scorre il registro con `getattr(net, nome, None)`, quindi LEGGE OGNI
        #   derivata a ogni confine di voce. ### Col veleno quella e' ESATTAMENTE la
        #   lettura che DEVE vedere il `NaN`: contarla fra le sporche direbbe che il
        #   controllo e' un difetto.
        if funzione in LETTORI_DI_PRESIDIO:
            self.coperte_presidio[nome].add((funzione, riga))
            return
        self.coperte[nome].add((funzione, riga))
        if self.finestra:
            self.coperte_finestra[nome].add((funzione, riga))
            if nome not in self.gia_scritta:
                self.sporche.append({"grandezza": nome, "funzione": funzione, "riga": riga})

    def scrivi(self, nome, funzione, riga):
        self.scritte[nome].add((funzione, riga))
        if self.finestra:
            self.gia_scritta.add(nome)


def carica(nome, seme, sim):
    with contextlib.redirect_stdout(io.StringIO()):
        _S0, argv = _cli_flag.argv_del_driver(extra=["--seme=%d" % seme],
                                              dest=os.path.join(FUORI, "_scarto_" + nome))
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
    return sim, sim.net


def una_scena(etichetta, seme, passi, nomi, stampa):
    """Un run con la spia installata. Restituisce il `Diario` e i contatori di nascita."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("_sim_cop_%s" % etichetta, SIM)
    sim = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(sim)
    S, net = carica(etichetta, seme, sim)
    diario = Diario(nomi)
    # ### LA SPIA SI INSTALLA DOPO IL CARICAMENTO, e lo dichiaro: il pre-rilassamento
    #   NON gira con l'argv del driver (MISURATO: `PRE-RILASSAMENTO-FUORI-PASSO`,
    #   zero `step()` fuori dallo schedulatore), quindi non c'e' niente da perdere
    #   prima di questo punto. Se un domani quella misura cambiasse, questa riga
    #   diventerebbe un buco -- e per questo le due voci si leggono insieme.
    for k in nomi:
        setattr(sim.Rete, k, Spia(k, diario))
    _mitosi0 = sim.Rete.mitosi

    def mitosi_spiata(self, *a, **k):
        r = _mitosi0(self, *a, **k)
        if r:
            diario.apri_finestra()
        return r

    sim.Rete.mitosi = mitosi_spiata
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            for _ in range(passi):
                diario.chiudi_finestra()
                _passo.passo_pieno(S, net)
        ev = (int(getattr(net, "_g_nati_mitosi_ev", 0)),
              int(getattr(net, "_g_nati_schwinger_ev", 0)),
              int(getattr(net, "_g_nati_mitosi", 0)),
              int(getattr(net, "_g_nati_schwinger", 0)))
    finally:
        sim.Rete.mitosi = _mitosi0
        for k in nomi:
            try:
                delattr(sim.Rete, k)
            except AttributeError:
                pass
    stampa("    passi %d, seme %d .. passi CON nascita %d, eventi mitosi %d, Schwinger %d "
           "(nodi %d / %d)" % (passi, seme, diario.passi_con_nascita, ev[0], ev[1], ev[2], ev[3]))
    return diario, ev


def principale():
    righe = []

    def stampa(*x):
        s = " ".join(str(y) for y in x)
        righe.append(s)
        print(s)

    if not os.path.isdir(FUORI):
        os.makedirs(FUORI)
    src = io.open(SIM, encoding="utf-8").read()
    albero = ast.parse(src)
    nomi = derivate_dal_sorgente(albero)
    stampa("=" * 104)
    stampa("LE DERIVATE ALLA NASCITA: le letture SPORCHE e LA COPERTURA")
    stampa("=" * 104)
    stampa("  simulatore .. %s (sha1 byte grezzi)" % blob(SIM)[:8])
    stampa("  ### le derivate sono DERIVATE dal sorgente (`REGISTRO_DERIVATE`): %d" % len(nomi))
    stampa("      %s" % ", ".join(nomi))
    stampa("")

    # ---------- pezzo 2: le letture dall'AST ---------------------------------------------------
    ast_let, per_nome_variabile = letture_dall_ast(albero, nomi)
    stampa("-" * 104)
    stampa("PEZZO 2 -- LE LETTURE DALL'AST, in TUTTO il simulatore (anche i rami spenti)")
    tot_ast = sum(len(v) for v in ast_let.values())
    stampa("  ### righe che leggono una derivata: %d in tutto" % tot_ast)
    for k in nomi:
        stampa("      %-18s %3d righe" % (k, len(ast_let[k])))
    stampa("")

    # ---------- pezzo 1 e 4: le tre scene ------------------------------------------------------
    stampa("-" * 104)
    stampa("PEZZI 1 e 4 -- LA COPERTURA DAL RUNTIME, su TRE scene")
    diari, eventi = {}, {}
    for etichetta, seme, passi in SCENE:
        stampa("  scena `%s`:" % etichetta)
        diari[etichetta], eventi[etichetta] = una_scena(etichetta, seme, passi, nomi, stampa)
    stampa("")

    # l'unione delle coperture nella FINESTRA della nascita
    coperte = {k: set() for k in nomi}
    for d in diari.values():
        for k in nomi:
            coperte[k] |= d.coperte_finestra[k]
    stampa("  ### E LE LETTURE DEL PRESIDIO sono CONTATE A PARTE, non fra le sporche:")
    stampa("      i lettori di presidio DICHIARATI: %s" % ", ".join(LETTORI_DI_PRESIDIO))
    for k in nomi:
        pres = set().union(*[d.coperte_presidio[k] for d in diari.values()])
        if pres:
            stampa("      %-18s %d righe di presidio: %s"
                   % (k, len(pres), ", ".join("`%s`:%d" % x for x in sorted(pres))[:90]))
    stampa("      *(col veleno quelle sono ESATTAMENTE le letture che DEVONO vedere il `NaN`:")
    stampa("        contarle fra le sporche direbbe che il controllo unico e' un difetto.)*")
    stampa("")
    stampa("  ### E LE LETTURE PER NOME VARIABILE NON RISOLTE: %d" % len(per_nome_variabile))
    stampa("      l'AST non sa SU CHI cadono (il nome e' calcolato a run); il runtime le vede.")
    stampa("      ### E' un LIMITE DICHIARATO del pezzo 2, non un'omissione.")
    stampa("")
    stampa("  ### righe che leggono una derivata NELLA FINESTRA DELLA NASCITA, unione delle tre:")
    for k in nomi:
        stampa("      %-18s %3d righe provate" % (k, len(coperte[k])))
    stampa("")

    # ---------- le letture SPORCHE ------------------------------------------------------------
    stampa("-" * 104)
    stampa("LE LETTURE SPORCHE: una derivata LETTA nella finestra PRIMA di essere riscritta")
    sporche = []
    for et, d in diari.items():
        for s in d.sporche:
            sporche.append(dict(s, scena=et))
    stampa("  ### letture sporche trovate: %d" % len(sporche))
    viste = set()
    for s in sporche:
        k = (s["grandezza"], s["funzione"], s["riga"])
        if k in viste:
            continue
        viste.add(k)
        stampa("      ### %-18s letta da `%s` :%d   (scena `%s`)"
               % (s["grandezza"], s["funzione"], s["riga"], s["scena"]))
    stampa("")

    # ---------- pezzo 3: la differenza, riga per riga, col MOTIVO ------------------------------
    stampa("-" * 104)
    stampa("PEZZO 3 -- LA DIFFERENZA: le letture MAI PROVATE, ciascuna col suo MOTIVO")
    # i flag al runtime: si leggono dal modulo di una scena gia' caricata
    import importlib.util
    spec = importlib.util.spec_from_file_location("_sim_flag_cop", SIM)
    simf = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(simf)
    carica("flag", 11, simf)

    def motivo(nome, voce):
        if voce["funzione"] in FUORI_DAL_PASSO:
            return ("fuori dallo schedulatore (`%s`)" % voce["funzione"],
                    "la funzione non sta sotto `esegui_passo`: un veleno applicato dentro "
                    "il passo non la raggiunge mai")
        spenti = []
        for g in voce["gate"]:
            for n in sorted({x.id for x in ast.walk(ast.parse(g, mode="eval"))
                             if isinstance(x, ast.Name)}):
                if n.isupper() and hasattr(simf, n):
                    v = getattr(simf, n)
                    if not v:
                        spenti.append("%s = %r" % (n, v))
        if spenti:
            return ("flag spento", "il gate richiede %s" % "; ".join(sorted(set(spenti))))
        if voce["gate"]:
            return ("condizione mai scattata",
                    "il gate e' `%s`, e nessuna delle tre scene l'ha reso vero nella "
                    "finestra" % " and ".join(voce["gate"])[:160])
        return ("non raggiunta, SENZA GATE",
                "nessuna condizione la protegge: se non e' stata letta e' perche' la "
                "funzione non e' stata chiamata nella finestra")
    non_provate = []
    for k in nomi:
        prov_righe = {r for (_f, r) in coperte[k]}
        for voce in ast_let[k]:
            if voce["riga"] in prov_righe:
                continue
            cl, perche = motivo(k, voce)
            non_provate.append({"grandezza": k, "funzione": voce["funzione"],
                                "riga": voce["riga"], "gate": voce["gate"],
                                "classe": cl, "perche": perche})
    per_classe = {}
    for x in non_provate:
        per_classe.setdefault(x["classe"], []).append(x)
    stampa("  ### letture dall'AST %d   PROVATE nella finestra %d   ### NON PROVATE %d"
           % (tot_ast, tot_ast - len(non_provate), len(non_provate)))
    for cl in sorted(per_classe):
        stampa("  --- %s: %d" % (cl, len(per_classe[cl])))
        for x in per_classe[cl]:
            stampa("      %-18s `%s` :%d" % (x["grandezza"], x["funzione"], x["riga"]))
            stampa("          %s" % x["perche"][:150])
    stampa("")
    stampa("=" * 104)
    stampa("### IL VERDETTO, scritto nella forma che il mandato impone:")
    stampa("###   ZERO letture sporche su %d PROVATE, %d NON PROVATE (elencate sopra)."
           % (tot_ast - len(non_provate), len(non_provate))
           if not sporche else
           "###   %d LETTURE SPORCHE su %d provate, %d non provate (elencate sopra)."
           % (len(sporche), tot_ast - len(non_provate), len(non_provate)))
    stampa("### ⛔ E NON SI SCRIVE <<nessuna derivata sporca>>: quella frase affermerebbe")
    stampa("###   qualcosa sulle %d righe che NON sono state guardate." % len(non_provate))
    stampa("=" * 104)

    esito = {
        "blob_sim_sha1_byte": blob(SIM),
        "derivate": nomi,
        "scene": [{"etichetta": e, "seme": s, "passi": p,
                   "passi_con_nascita": diari[e].passi_con_nascita,
                   "eventi_mitosi": eventi[e][0], "eventi_schwinger": eventi[e][1],
                   "nodi_mitosi": eventi[e][2], "nodi_schwinger": eventi[e][3]}
                  for e, s, p in SCENE],
        "letture_dall_ast": {k: ast_let[k] for k in nomi},
        "totale_letture_ast": tot_ast,
        "coperte_nella_finestra": {k: sorted(coperte[k]) for k in nomi},
        "coperte_dal_PRESIDIO": {k: sorted(set().union(
            *[d.coperte_presidio[k] for d in diari.values()])) for k in nomi},
        "lettori_di_presidio_DICHIARATI": list(LETTORI_DI_PRESIDIO),
        "letture_per_nome_variabile_NON_risolte": per_nome_variabile,
        "totale_provate": tot_ast - len(non_provate),
        "letture_sporche": sporche,
        "non_provate": non_provate,
        "verdetto": ("zero letture sporche su %d provate, %d non provate"
                     % (tot_ast - len(non_provate), len(non_provate))) if not sporche else
                    ("%d letture sporche su %d provate, %d non provate"
                     % (len(sporche), tot_ast - len(non_provate), len(non_provate))),
    }
    io.open(os.path.join(FUORI, "_copertura_derivate.json"), "w", encoding="utf-8",
            newline=NL).write(json.dumps(esito, indent=1, ensure_ascii=False, default=str))
    io.open(os.path.join(FUORI, "_corsa.txt"), "w", encoding="utf-8",
            newline=NL).write(NL.join(righe) + NL)
    print("  referto .. %s" % FUORI)


if __name__ == "__main__":
    principale()
