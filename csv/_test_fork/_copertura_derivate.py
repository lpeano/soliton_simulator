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
#   ### E `verifica_invarianti` L'HA AGGIUNTO IL GIRO VERO, non io: ha prodotto
#   ### TUTTE le 808 <<letture sporche>> del primo giro, e TUTTE dalla STESSA riga
#   (`:6112`), che e' `v = getattr(self, quale, None)` dentro il ciclo su `DOMINI`.
#   ### E' IL CONTROLLO DEGLI INVARIANTI che scorre le grandezze dichiarate -- cioe'
#   l'ULTIMA voce del passo, e ### col veleno e' PROPRIO la voce che lo prende.
#   ### 808 letture da UNA riga di presidio non sono 808 difetti: sono UN lettore
#   che non avevo dichiarato -- e il referto lo diceva a chi lo leggeva, perche'
#   stampava la funzione e la riga di ciascuna.
LETTORI_DI_PRESIDIO = ("_ferma_se_registro_incoerente", "verifica_invarianti",
                       "rapporto_guardie", "_forma_di",
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


def modifiche_in_posto(albero, nomi):
    """I siti che modificano una derivata IN POSTO: `x[i] = ...`, `x[:] = ...`, `copyto`.

    ### LA SEMANTICA DELLA SPIA, e va DICHIARATA perche' taglia in due direzioni
    (rilievo del guardiano, 2026-10-03). In `self.x[i] = v` Python valuta ### PRIMA
    `self.x` -- cioe' chiama `__get__` -- e poi `__setitem__` sull'array. ### Quindi la
    spia vede ### **una LETTURA, non una scrittura**:

    | | |
    |---|---|
    | un ricalcolo ### **PARZIALE** in posto *(`x[i] = ...`)* | ### **non pulisce**, ed e' ### **GIUSTO**: gli altri elementi restano quelli di prima, cioe' quelli che la nascita ha invalidato |
    | un ricalcolo ### **COMPLETO** in posto *(`x[:] = ...`, `np.copyto(x, ...)`)* | ### **non pulisce NEMMENO**, e questo e' ### **SBAGLIATO**: darebbe letture sporche ### **spurie** |

    ### \u279c **L'errore cade dalla parte PRUDENTE** *(una lettura sporca in piu' da
    spiegare, non una in meno)*, ### **ma solo se i siti del secondo tipo si ELENCANO** --
    altrimenti un allarme spurio si legge come un difetto del simulatore.
    """
    parziali, completi = [], []

    def dentro(nodo, funzione):
        for figlio in ast.iter_child_nodes(nodo):
            f2 = figlio.name if isinstance(figlio, ast.FunctionDef) else funzione
            if isinstance(figlio, (ast.Assign, ast.AugAssign)):
                mire = (figlio.targets if isinstance(figlio, ast.Assign)
                        else [figlio.target])
                for m in mire:
                    if not isinstance(m, ast.Subscript):
                        continue
                    b = m.value
                    if not (isinstance(b, ast.Attribute) and isinstance(b.value, ast.Name)
                            and b.value.id in ("self", "net") and b.attr in nomi):
                        continue
                    s = ast.unparse(m.slice)
                    voce = {"grandezza": b.attr, "funzione": f2, "riga": figlio.lineno,
                            "codice": ast.unparse(figlio)[:120], "indice": s}
                    completo = s in (":", "...", "slice(None, None, None)")
                    (completi if completo else parziali).append(voce)
            if (isinstance(figlio, ast.Call) and isinstance(figlio.func, ast.Attribute)
                    and figlio.func.attr == "copyto" and figlio.args):
                a0 = figlio.args[0]
                if (isinstance(a0, ast.Attribute) and isinstance(a0.value, ast.Name)
                        and a0.value.id in ("self", "net") and a0.attr in nomi):
                    completi.append({"grandezza": a0.attr, "funzione": f2,
                                     "riga": figlio.lineno,
                                     "codice": ast.unparse(figlio)[:120],
                                     "indice": "np.copyto"})
            dentro(figlio, f2)

    dentro(albero, "<modulo>")
    return parziali, completi


def collaudo_in_posto():
    """### IL CONTROLLO POSITIVO del rilevatore delle modifiche in posto (`STANDARD 2`).

    Senza di lui lo *<<zero modifiche in posto>>* sul simulatore vero sarebbe
    ### **indistinguibile da un rilevatore rotto** -- ed e' la forma `FALSO-ZERO`, che in
    due giorni ha morso ### **undici volte.** Gira su un frammento ### **sintetico**, in
    memoria, e costa microsecondi: ### **non c'e' nessuna ragione per non cablarlo.**

    Il frammento contiene ### **cinque** righe, e il rilevatore deve prenderne
    ### **esattamente tre**, con la classificazione giusta:

    | la riga | atteso |
    |---|---|
    | `self._sin2_vir[idx] = 1.0` | ### **PARZIALE** |
    | `self._r_corrente[:] = 3.0` | ### **COMPLETA** |
    | `np.copyto(self._xi_rumore, nuovo)` | ### **COMPLETA** |
    | `self._dt_e_ultimo = 7.0` | ### **ignorata**: non e' in posto |
    | `self.peq[:] = 1.0` | ### **ignorata**: `peq` non e' una derivata |

    ### \u279c **Le due righe ignorate contano quanto le tre trovate:** un rilevatore
    troppo largo gonfierebbe l'elenco degli allarmi spuri e renderebbe illeggibile
    l'unica cosa che conta.
    """
    finto = NL.join([
        "class Rete:",
        "    def legge(self):",
        "        self._r_corrente[:] = 3.0",
        "        self._sin2_vir[idx] = 1.0",
        "        np.copyto(self._xi_rumore, nuovo)",
        "        self._dt_e_ultimo = 7.0",
        "        self.peq[:] = 1.0",
    ])
    nomi = ("_r_corrente", "_sin2_vir", "_xi_rumore", "_dt_e_ultimo")
    pz, cp = modifiche_in_posto(ast.parse(finto), nomi)
    atteso_pz = [("_sin2_vir", "idx")]
    atteso_cp = [("_r_corrente", ":"), ("_xi_rumore", "np.copyto")]
    ott_pz = sorted((x["grandezza"], x["indice"]) for x in pz)
    ott_cp = sorted((x["grandezza"], x["indice"]) for x in cp)
    return {"passa": ott_pz == sorted(atteso_pz) and ott_cp == sorted(atteso_cp),
            "parziali_attese": atteso_pz, "parziali_ottenute": ott_pz,
            "complete_attese": sorted(atteso_cp), "complete_ottenute": ott_cp}


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
        self.sporche_ora = set()   # le derivate SPORCHE in questo istante
        self.dentro_nascita = False
        self.scritte_nella_nascita = set()
        self.nascite = 0
        self.coperte = {k: set() for k in nomi}        # (funzione, riga) che LEGGONO
        self.coperte_finestra = {k: set() for k in nomi}
        self.coperte_presidio = {k: set() for k in nomi}   # il CONTROLLO che guarda
        self.scritte = {k: set() for k in nomi}
        self.sporche = []                              # letture PRIMA della scrittura

    def inizia_nascita(self):
        """Comincia a registrare le scritture fatte DENTRO una chiamata a `nascita`."""
        self.dentro_nascita = True
        self.scritte_nella_nascita = set()

    def apri_finestra(self):
        """Una nascita: TUTTE le derivate diventano SPORCHE, e restano tali FINO ALLA
        RISCRITTURA -- anche attraverso il confine del passo.

        ### IL GIRO VERO HA TROVATO QUI UN DIFETTO STRUTTURALE DELLA MISURA, e quel
        difetto GARANTIVA UNO ZERO. La prima stesura chiudeva la finestra ### all'inizio
        di ogni passo. Ma `PASSO_COMPOSIZIONE` e'

            `apri, scuoti_vuoto, ### step, ### mitosi, rilassa_disegno, ...`

        cioe' ### **`step` viene PRIMA di `mitosi`.** Una derivata avvelenata alla
        nascita viene riletta da `step` ### **AL PASSO DOPO** -- e una finestra che si
        chiude all'inizio del passo si chiude ### **esattamente prima di quella
        lettura.** ### Il primo giro ha dato <<0 PROVATE su 31>>, e quello zero era
        ### GARANTITO DALLA COSTRUZIONE, non misurato.

        ### LA CURA: la finestra e' PER GRANDEZZA e dura fino alla sua SCRITTURA -- che
        e' letteralmente cio' che la domanda chiede, *<<letta fra la nascita e la
        riscrittura>>*. Se una derivata non viene mai riscritta resta sporca, ed ### e'
        giusto: leggerla e' leggere un valore che la nascita ha invalidato.
        """
        # ### SPORCHE TUTTE, TRANNE QUELLE CHE LA NASCITA HA SCRITTO LEI STESSA.
        #   Senza questa sottrazione una grandezza appena riscritta DENTRO la nascita
        #   (da una regola o da una chiamata collocata) tornerebbe sporca ### subito
        #   dopo essere stata scritta bene, e le sue letture successive risulterebbero
        #   sporche ### PER ERRORE. Rilievo del guardiano, 2026-10-03.
        #   ### ⚠ E OGGI QUESTA SOTTRAZIONE HA ZERO CASI, e lo dico invece di
        #   lasciarlo credere: le tre grandezze scritte dalle CHIAMATE COLLOCATE sono
        #   `_deg` (in `REGISTRO_STATO`) e `_smp_d`/`_smp_d0` (in `REGISTRO_FINESTRA`),
        #   ### e NESSUNA delle tre e' in `REGISTRO_DERIVATE`. Il rilievo e' giusto
        #   nella FORMA, e la cura resta cablata perche' ### un domani il registro puo'
        #   cambiare -- e allora morderebbe senza avvisare.
        self.sporche_ora = set(self.nomi) - set(self.scritte_nella_nascita)
        self.dentro_nascita = False
        self.nascite += 1

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
        if nome in self.sporche_ora:
            self.coperte_finestra[nome].add((funzione, riga))
            self.sporche.append({"grandezza": nome, "funzione": funzione, "riga": riga})

    def scrivi(self, nome, funzione, riga):
        self.scritte[nome].add((funzione, riga))
        # ### LA RISCRITTURA PULISCE, ed e' la SOLA cosa che pulisce: non il confine del
        #   passo, non un'altra grandezza. E' la semantica del par.(d): <<tornano pulite
        #   quando LA LORO LEGGE le riscrive>>.
        self.sporche_ora.discard(nome)
        if self.dentro_nascita:
            self.scritte_nella_nascita.add(nome)


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
    # ### SI AVVOLGE `nascita`, NON `mitosi`, E QUESTO E' IL TERZO DIFETTO DELLA
    #   FINESTRA (rilievo del guardiano, 2026-10-03). Avvolgendo `mitosi` la finestra
    #   si apriva ### QUANDO MITOSI RITORNAVA -- ma la nascita avviene DENTRO, alla
    #   chiamata `nascita(self, "divisione", c)`, e dopo di lei ### mitosi CONTINUA
    #   (il ramo Schwinger, con la sua `nascita(self, "schwinger", c2)`).
    #   ### ➜ DUE ERRORI OPPOSTI, e il primo e' quello grave:
    #     ① LETTURE PERSE: tutto cio' che `mitosi` legge DOPO la nascita della
    #       divisione -- cioe' ### tutta la preparazione dello Schwinger, 64 eventi
    #       nella scena lunga -- avveniva PRIMA che la finestra si aprisse, quindi
    #       ### non era mai contato come sporco;
    #     ② FALSI ALLARMI: le grandezze riscritte DENTRO la nascita tornavano
    #       sporche al ritorno di `mitosi`, dopo essere state scritte bene.
    #   ### ✅ ORA: la finestra si apre alla FINE DI OGNI chiamata a `nascita`, PER
    #   EVENTO, e sottrae cio' che quella chiamata ha scritto.
    # ### E UNA COLLOCATA CHE GIRA *DOPO* `nascita()`: COME LA TRATTO, E PERCHE'
    #   (la domanda e' del guardiano, 2026-10-03). Il caso concreto e' `_grado()`, che
    #   `mitosi` chiama ### DOPO il blocco della nascita perche' legge `i`, `j` e
    #   `len(phi)` -- cioe' e' una DERIVATA della topologia.
    #   ### LA RISPOSTA E' CHE NON HA BISOGNO DI UN TRATTAMENTO SPECIALE, e per due
    #   ragioni distinte:
    #     \u2460 ### `_grado()` NON SCRIVE NESSUNA DELLE DIECI DERIVATE SORVEGLIATE.
    #       Scrive `_deg` (che sta in `REGISTRO_STATO`) e `_cicli_topologici`; nessuna
    #       delle due e' in `REGISTRO_DERIVATE`. ### Misurato sul registro, non assunto.
    #       Lo stesso vale per `_smp_chirurgia` (`_smp_d`/`_smp_d0`, in
    #       `REGISTRO_FINESTRA`) e per `_traccia_d0`.
    #     \u2461 ### E SE DOMANI NE SCRIVESSE UNA, LA SEMANTICA E' GIA' GIUSTA: la
    #       finestra e' PER GRANDEZZA e la chiude ### LA SCRITTURA, dovunque avvenga --
    #       dentro `nascita`, dopo di lei, o in un passo successivo. Una collocata che
    #       riscrive una derivata la PULISCE alla sua riga, ### che e' esattamente cio'
    #       che deve fare. La sottrazione in `apri_finestra` serve al caso OPPOSTO: una
    #       grandezza scritta DENTRO la nascita che altrimenti verrebbe RIMARCATA sporca
    #       subito dopo.
    #   ### \u279c Quindi: nessuna eccezione per `_grado`, e il motivo e' che non ne
    #   serve una. Dichiararlo e' il punto -- un'eccezione non necessaria sarebbe una
    #   legge in piu' (`9-ter`).
    _nascita0 = sim.nascita

    def nascita_spiata(net, evento, c):
        diario.inizia_nascita()
        r = _nascita0(net, evento, c)
        diario.apri_finestra()
        return r

    sim.nascita = nascita_spiata
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            for _ in range(passi):
                # ### NESSUNA CHIUSURA QUI: la finestra e' PER GRANDEZZA e la chiude la
                #   SUA riscrittura, anche in un passo successivo. Chiuderla qui era il
                #   difetto che garantiva lo zero.
                _passo.passo_pieno(S, net)
        ev = (int(getattr(net, "_g_nati_mitosi_ev", 0)),
              int(getattr(net, "_g_nati_schwinger_ev", 0)),
              int(getattr(net, "_g_nati_mitosi", 0)),
              int(getattr(net, "_g_nati_schwinger", 0)))
    finally:
        sim.nascita = _nascita0
        for k in nomi:
            try:
                delattr(sim.Rete, k)
            except AttributeError:
                pass
    stampa("    passi %d, seme %d .. chiamate a `nascita` %d, eventi mitosi %d, "
           "Schwinger %d (nodi %d / %d)"
           % (passi, seme, diario.nascite, ev[0], ev[1], ev[2], ev[3]))
    return diario, ev


ANCORA_INIEZIONE = '        nascita(self, "divisione", c)'
LETTURA_INIETTATA = ('_ = getattr(self, "_r_corrente", None)   '
                     '# LETTURA INIETTATA (controllo positivo della finestra)')


def controllo_iniettato(nomi, stampa):
    """### IL CONTROLLO POSITIVO DELLA FINESTRA, e la prima versione era MAL POSTA.

    Il guardiano l'aveva chiesto cosi': *<<almeno una lettura che avviene dentro
    `mitosi` dopo la nascita della divisione deve comparire fra le letture nella
    finestra>>*. ### \u26d4 E dava ZERO in tutte e tre le scene -- ma NON perche' la cura
    non avesse attaccato:

    ### \u2705 **`mitosi` NON LEGGE NESSUNA DELLE DIECI DERIVATE**, ne' direttamente ne'
    via `getattr`. ### **Misurato sull'AST**, non supposto: le funzioni che le leggono
    sono `step` (20), `_diag_completa` (4), `decidi_divisione` (2), `_bloch_ritardato`,
    `_fattore_tempo_arco`, `_passo_spinoriale`, `_pesi`, `_r_nodo_mitosi` -- ### e
    `mitosi` non e' fra loro.

    ### \u26a0 **QUINDI QUEL CONTROLLO NON ERA SATISFACIBILE, e il suo zero non
    discriminava niente** -- ne' il successo ne' il fallimento della cura. ### **Un
    controllo che non puo' passare non e' un controllo: e' un allarme fisso.**

    ### \u2705 **LA VERSIONE CHE DISCRIMINA: si INIETTA la lettura.** In una COPIA del
    simulatore si mette `_ = self._r_corrente` ### subito dopo `nascita(self,
    "divisione", c)`, dentro `mitosi`. Allora:

    | | |
    |---|---|
    | con la finestra che si apre al ### **RITORNO di `mitosi`** *(il difetto)* | la lettura iniettata ### **NON compare** |
    | con la finestra che si apre alla ### **FINE di `nascita`** *(la cura)* | la lettura iniettata ### **COMPARE**, attribuita a `mitosi` |

    ### \u279c **E' la stessa tecnica dell'ulp iniettato del sigillo esteso:** non si
    chiede al sistema di avere per caso il caso che serve, ### **lo si costruisce.**
    """
    import importlib.util
    dest = os.path.join(FUORI, "_sim_lettura_iniettata.py")
    testo = io.open(SIM, encoding="utf-8", newline="").read()
    n = testo.count(ANCORA_INIEZIONE)
    if n != 1:
        raise SystemExit("** l'ancora dell'iniezione e' presente %d volte (attesa 1). NON "
                         "scrivo la copia. **" % n)
    io.open(dest, "wb").write(testo.replace(
        ANCORA_INIEZIONE,
        ANCORA_INIEZIONE + NL + "        " + LETTURA_INIETTATA).encode("utf-8"))
    a = testo.split(NL)
    b = io.open(dest, encoding="utf-8", newline="").read().split(NL)
    riga_iniettata = next((i + 1 for i, (x, y) in enumerate(zip(a, b)) if x != y), None)
    stampa("  la copia: una riga AGGIUNTA alla `:%s` (%d righe -> %d)"
           % (riga_iniettata, len(a), len(b)))
    spec = importlib.util.spec_from_file_location("_sim_cop_iniettata", dest)
    sim = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(sim)
    S, net = carica("iniettata", 11, sim)
    diario = Diario(nomi)
    for k in nomi:
        setattr(sim.Rete, k, Spia(k, diario))
    _n0 = sim.nascita

    def nascita_spiata(net2, evento, c):
        diario.inizia_nascita()
        r = _n0(net2, evento, c)
        diario.apri_finestra()
        return r

    sim.nascita = nascita_spiata
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            for _ in range(72):
                _passo.passo_pieno(S, net)
    finally:
        sim.nascita = _n0
        for k in nomi:
            try:
                delattr(sim.Rete, k)
            except AttributeError:
                pass
    trovate = sorted({(k, f, r) for k in nomi for (f, r) in diario.coperte_finestra[k]
                      if f == "mitosi"})
    ev = int(getattr(net, "_g_nati_mitosi_ev", 0))
    stampa("  eventi di mitosi nel run iniettato: %d" % ev)
    stampa("  ### letture nella finestra da DENTRO `mitosi`: %d" % len(trovate))
    for k, f, r in trovate:
        stampa("      ### %-18s `%s` :%d" % (k, f, r))
    ok = bool(trovate) and bool(ev)
    stampa("  ### IL CONTROLLO POSITIVO INIETTATO %s"
           % ("PASSA: la finestra E' APERTA dentro `mitosi` dopo la nascita." if ok
              else "### FALLISCE: la finestra NON e' aperta dentro `mitosi`, quindi la cura "
                   "NON ha attaccato e il verdetto NON VALE."))
    return {"passa": bool(ok), "riga_iniettata": riga_iniettata,
            "lettura": LETTURA_INIETTATA, "eventi_mitosi": ev,
            "trovate": [list(x) for x in trovate],
            "blob_copia": blob(dest)}


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

    # ---------- LA SEMANTICA DELLE MODIFICHE IN POSTO, dichiarata -----------------------------
    parz, compl = modifiche_in_posto(albero, nomi)
    stampa("-" * 104)
    stampa("LA SEMANTICA DELLA SPIA SULLE MODIFICHE IN POSTO, e si DICHIARA")
    stampa("  In `self.x[i] = v` Python valuta PRIMA `self.x` (cioe' `__get__`) e poi")
    stampa("  `__setitem__`: ### la spia vede UNA LETTURA, NON UNA SCRITTURA.")
    stampa("    un ricalcolo PARZIALE in posto (`x[i] = ...`) .. NON pulisce, ed e' GIUSTO")
    stampa("      (gli altri elementi restano quelli che la nascita ha invalidato)")
    stampa("    un ricalcolo COMPLETO in posto (`x[:] = ...`, `np.copyto`) NON pulisce")
    stampa("      NEMMENO, e questo e' ### SBAGLIATO: darebbe letture sporche SPURIE")
    stampa("  ### L'errore cade dalla parte PRUDENTE, ma solo se i siti si ELENCANO:")
    stampa("      modifiche in posto PARZIALI: %d" % len(parz))
    for x in parz:
        stampa("          %-18s `%s` :%d  [%s]  %s"
               % (x["grandezza"], x["funzione"], x["riga"], x["indice"], x["codice"][:70]))
    stampa("      ### modifiche in posto COMPLETE (quelle che darebbero allarmi SPURI): %d"
           % len(compl))
    for x in compl:
        stampa("          ### %-18s `%s` :%d  [%s]  %s"
               % (x["grandezza"], x["funzione"], x["riga"], x["indice"], x["codice"][:70]))
    if not compl:
        stampa("          ### NESSUNA: quindi oggi nessun allarme puo' essere spurio per")
        stampa("          ### questa ragione.")
    # ### E LO ZERO VALE SOLO SE IL RILEVATORE FUNZIONA (`STANDARD 2`, `FALSO-ZERO`):
    cip = collaudo_in_posto()
    stampa("      ### IL CONTROLLO POSITIVO DEL RILEVATORE, su un frammento sintetico:")
    stampa("          parziali: attese %s   ottenute %s"
           % (cip["parziali_attese"], cip["parziali_ottenute"]))
    stampa("          complete: attese %s   ottenute %s"
           % (cip["complete_attese"], cip["complete_ottenute"]))
    stampa("          *(e DUE righe devono essere IGNORATE: `self._dt_e_ultimo = 7.0`, che")
    stampa("            non e' in posto, e `self.peq[:]`, che non e' una derivata. Un")
    stampa("            rilevatore troppo largo renderebbe illeggibile l'unica cosa che conta.)*")
    stampa("          ### %s"
           % ("IL RILEVATORE FUNZIONA, quindi lo zero di sopra E' VERO." if cip["passa"]
              else "### IL RILEVATORE NON FUNZIONA: lo zero di sopra NON VALE."))
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

    # ---------- IL CONTROLLO POSITIVO DELLA FINESTRA, con una lettura INIETTATA ---------------
    stampa("-" * 104)
    stampa("IL CONTROLLO POSITIVO DELLA FINESTRA: una lettura INIETTATA dentro `mitosi`")
    stampa("  ### E LA PRIMA VERSIONE DI QUESTO CONTROLLO ERA MAL POSTA, e lo dico perche'")
    stampa("      il suo zero poteva essere letto come un fallimento della cura.")
    stampa("      Chiedeva: <<una lettura DENTRO `mitosi` dopo la nascita deve comparire>>.")
    stampa("      ### Ma `mitosi` NON LEGGE NESSUNA DELLE DIECI DERIVATE -- misurato")
    stampa("      sull'AST: le leggono `step` (20), `_diag_completa` (4),")
    stampa("      `decidi_divisione` (2), `_bloch_ritardato`, `_fattore_tempo_arco`,")
    stampa("      `_passo_spinoriale`, `_pesi`, `_r_nodo_mitosi` -- e `mitosi` NON c'e'.")
    stampa("      ### Un controllo che non PUO' passare non e' un controllo: e' un")
    stampa("      ### allarme fisso, e non discrimina ne' il successo ne' il fallimento.")
    stampa("  ### LA VERSIONE CHE DISCRIMINA: si INIETTA `_ = self._r_corrente` subito")
    stampa("      dopo `nascita(self, \"divisione\", c)`, in una COPIA del simulatore.")
    stampa("      Con la finestra al RITORNO di `mitosi` (il difetto) NON comparirebbe;")
    stampa("      con la finestra alla FINE di `nascita` (la cura) DEVE comparire.")
    stampa("      ### E' la stessa tecnica dell'ulp iniettato: il caso non si spera, SI COSTRUISCE.")
    iniettato = controllo_iniettato(nomi, stampa)
    pos_ok = iniettato["passa"]
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
                   "chiamate_a_nascita": diari[e].nascite,
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
        "collaudo_del_rilevatore_in_posto": cip,
        "modifiche_in_posto_PARZIALI": parz,
        "modifiche_in_posto_COMPLETE_allarmi_spuri": compl,
        "controllo_positivo_finestra_INIETTATO": iniettato,
        "mitosi_legge_derivate": False,
        "perche_il_primo_controllo_era_mal_posto": (
            "chiedeva una lettura dentro `mitosi` dopo la nascita, ma `mitosi` non legge "
            "nessuna delle dieci derivate (misurato sull'AST): il suo zero non "
            "discriminava ne' il successo ne' il fallimento della cura"),
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
