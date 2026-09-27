# -*- coding: utf-8 -*-
"""**FASE 0-bis di `ETC-PASSO`: LE SCRITTURE CONCORRENTI, e quali NON sono variazioni.**

**Che cosa misura**, per le cinque leggi del passo *(ordine letto da `csv/_passo.py`)*:

1. **Chi scrive che cosa**: per ogni attributo di stato, **quali leggi** lo scrivono, **in quale
   forma** e **a quale riga**, seguendo ricorsivamente le chiamate a metodi di `Rete`.
2. **Le scritture CONCORRENTI**: gli attributi scritti da **piu' di una legge** -- gli unici per cui
   *«come si compongono»* e' una domanda.
3. **La COMPONIBILITA' di ciascuna scrittura**, in tre classi decise **dall'AST**:
   - **`A` incremento** *(`+=`, `[]+=`)*: **si compone per somma**. E' la regola di Luca.
   - **`B` assegnazione che DIPENDE DAL VALORE CORRENTE** *(la parte destra rilegge lo stesso
     attributo: `clip`, pavimento, saturazione, modulo, normalizzazione)*: **NON e' esprimibile
     come variazione** senza una decisione. **Vanno elencate, e si FERMA.**
   - **`C` assegnazione che NON dipende dal valore corrente**: e' una variazione implicita
     `nuovo - fotografia`, **ma se due leggi la fanno sullo stesso attributo e' un CONFLITTO**.
4. **I flussi casuali**: quante volte ciascuna legge tocca `rng`. *(Punto 5 del mandato: senza un
   flusso per legge, `H-ETC-2` fallirebbe per il motivo sbagliato.)*
5. **Il costo della fotografia**: byte **misurati** da uno stato reale del pilota, se c'e'.

**⚠ IL LIMITE, prima dei numeri (`A9`), ed e' lo stesso di `_etc_letture.py`:** analisi **STATICA e
per NOME**. Gli alias, `getattr` e i rami mai eseguiti non si vedono; una scrittura in un ramo
spento conta comunque. **Quindi le classi `B` sono un LIMITE INFERIORE dei casi da decidere**, mai
un elenco chiuso. Chi certifica e' `H-ETC-2`, non questo script.

COMANDO:  python csv/_test_fork/_etc_progetto.py
"""
import ast
import io
import json
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, os.path.join(RADICE, "csv"))
import _presidio  # noqa: E402

_presidio.avvia(__file__)
import _passo  # noqa: E402

SIM = os.path.join(RADICE, "soliton_simulator.py")
SRC = io.open(SIM, encoding="utf-8").read()
ARB = ast.parse(SRC)
LINEE = SRC.split(chr(10))

# le 21 grandezze della classe "stato fisico" fissate dalla FASE 0
STATO = ["d", "d0", "phi", "phi_s", "phivel", "psi", "psi_spin", "_psi_spinor", "_psi_prec",
         "_spinor_lift", "omega_s", "_nb", "_nb_prec", "eta", "tw", "twp", "vd", "peq",
         "mem_mot", "perc_chi", "perc_geom"]
STRUTTURA = ["i", "j", "n"]
CACHE = ["_S", "_perm", "_deg"]

METODI, FUNZIONI = {}, {}
for _n in ast.walk(ARB):
    if isinstance(_n, ast.ClassDef) and _n.name == "Rete":
        for _k in _n.body:
            if isinstance(_k, (ast.FunctionDef, ast.AsyncFunctionDef)):
                METODI[_k.name] = _k
for _n in ARB.body:
    if isinstance(_n, ast.FunctionDef):
        FUNZIONI[_n.name] = _n


def _radice(nodo):
    while isinstance(nodo, (ast.Attribute, ast.Subscript)):
        nodo = nodo.value
    return nodo.id if isinstance(nodo, ast.Name) else None


def _attr(nodo):
    while isinstance(nodo, ast.Subscript):
        nodo = nodo.value
    return nodo.attr if isinstance(nodo, ast.Attribute) else None


_NON_VALORE = ("dtype", "shape", "size", "ndim", "nbytes", "flags", "T")
_ESTENDE = ("concatenate", "vstack", "hstack", "stack", "append", "resize", "tile", "pad")


def _rilegge(nodo, rice, attr):
    """La parte destra rilegge il VALORE di `rice.attr`?

    ⚠ **NON conta come dipendenza dal valore** una lettura di `dtype`/`shape`/`size`/... :
    `self.perc_chi[:n] = np.where(...).astype(self.perc_chi.dtype)` **non dipende dal valore
    corrente**, dipende dal suo TIPO. La prima stesura le contava, e produceva **falsi `B`**.

    ⚠ **E SI POTA IL SOTTOALBERO, non si salta il nodo:** `ast.walk` visita `self.perc_chi`
    **dentro** `self.perc_chi.dtype`, quindi saltare il solo nodo `.dtype` non basta -- la prima
    stesura lo faceva, e i tre `perc_chi`/`perc_geom` restavano falsi `B`.
    """
    coda = [nodo]
    while coda:
        s = coda.pop()
        if isinstance(s, ast.Attribute) and s.attr in _NON_VALORE:
            continue                                    # POTATO: non si scende sotto `.dtype`
        if isinstance(s, ast.Attribute) and s.attr == attr and _radice(s) == rice:
            return True
        coda.extend(ast.iter_child_nodes(s))
    return False


def _stessa_cosa(a, b):
    """Due espressioni sono lo STESSO bersaglio? (`self.d` vs `self.d`, `self.phi[a]` vs idem)"""
    try:
        return ast.unparse(a) == ast.unparse(b)
    except Exception:
        return False


def _forma_rhs(bersaglio, valore, rice, attr):
    """La FORMA della parte destra, che decide la classe.

    - `"estensione"`  : `np.concatenate([self.X, ...])`, `np.vstack(...)`, o `self.X[:k]`
                        -- **non e' una variazione**: e' STRUTTURA, e il mandato la mette DOPO.
    - `"incremento"`  : `self.X = self.X + <expr>` -- un `+=` scritto come assegnazione.
    - `"mescola"`     : `(1-p)*self.X + p*<expr>` -- esprimibile come variazione `p*(expr-X)`.
    - `"vincolo"`     : `clip` / `maximum` / `minimum` / `%` / normalizzazione / pavimento
                        -- **dipende dal corrente e NON e' una variazione**.
    - `"altro-corrente"` : dipende dal corrente in un modo che non ho classificato.
    - `None`          : non dipende dal valore corrente.
    """
    if valore is None:
        return "in-place"
    # ⚠ un'ESPRESSIONE CONDIZIONALE va guardata nei DUE rami: `vstack(...) if len(X) else zeros(...)`
    #   e' un'estensione, e la prima stesura la contava come `B` perche' guardava solo la cima.
    if isinstance(valore, ast.IfExp):
        r = [_forma_rhs(bersaglio, valore.body, rice, attr),
             _forma_rhs(bersaglio, valore.orelse, rice, attr)]
        if "estensione" in r:
            return "estensione"
        for k in ("vincolo", "altro-corrente", "mescola", "incremento"):
            if k in r:
                return k
        return None
    # estensione / troncamento
    if isinstance(valore, ast.Call) and isinstance(valore.func, ast.Attribute) \
            and valore.func.attr in _ESTENDE:
        return "estensione"
    if isinstance(valore, ast.Subscript) and _radice(valore) == rice and _attr(valore) == attr:
        return "estensione"
    if not _rilegge(valore, rice, attr):
        return None
    # incremento: self.X = self.X + qualcosa   (oppure  qualcosa + self.X)
    if isinstance(valore, ast.BinOp) and isinstance(valore.op, ast.Add):
        for lato in (valore.left, valore.right):
            if _stessa_cosa(lato, bersaglio):
                return "incremento"
        return "mescola"
    # vincoli: clip, maximum/minimum, modulo, divisione per una norma, pavimento dichiarato
    testo = ""
    try:
        testo = ast.unparse(valore)
    except Exception:
        pass
    if isinstance(valore, ast.BinOp) and isinstance(valore.op, ast.Mod):
        return "vincolo"
    if isinstance(valore, ast.BinOp) and isinstance(valore.op, ast.Div):
        return "vincolo"
    for k in ("np.clip", "np.maximum", "np.minimum", "np.nan_to_num", "_pav_d0",
              "_floor_d0", "satura", "np.where"):
        if testo.startswith(k + "(") or ("." + k.split(".")[-1] + "(") in testo[:40]:
            return "vincolo"
    return "altro-corrente"


class Scansione(ast.NodeVisitor):
    """Le SCRITTURE di un corpo, con forma, riga e dipendenza dal valore corrente."""

    def __init__(self, rice, dove):
        self.rice, self.dove = rice, dove
        self.scritture, self.chiamate, self.rng = [], set(), 0

    def _reg(self, bersaglio, valore, forma):
        if _radice(bersaglio) != self.rice:
            return
        a = _attr(bersaglio)
        if not a or a.startswith("__"):
            return
        rhs = "incremento" if forma.endswith("+=") else _forma_rhs(bersaglio, valore,
                                                                   self.rice, a)
        self.scritture.append({"attributo": a, "forma": forma, "riga": bersaglio.lineno,
                               "dentro": self.dove, "rhs": rhs,
                               "sorgente": LINEE[bersaglio.lineno - 1].strip()[:150]})

    def visit_Assign(self, n):
        for t in n.targets:
            self._reg(t, n.value, "[]=" if isinstance(t, ast.Subscript) else "=")
        self.generic_visit(n)

    def visit_AugAssign(self, n):
        self._reg(n.target, n.value, "[]+=" if isinstance(n.target, ast.Subscript) else "+=")
        self.generic_visit(n)

    def visit_Attribute(self, n):
        if n.attr == "rng" and _radice(n) == self.rice:
            self.rng += 1
        self.generic_visit(n)

    def visit_Call(self, n):
        f = n.func
        if isinstance(f, ast.Attribute) and isinstance(f.value, ast.Name) \
                and f.value.id == self.rice and f.attr in METODI:
            self.chiamate.add((f.attr, self.rice))
        elif isinstance(f, ast.Name) and f.id in FUNZIONI:
            self.chiamate.add((f.id, "net"))
        elif isinstance(f, ast.Attribute) and isinstance(f.value, ast.Attribute) \
                and _radice(f.value) == self.rice \
                and f.attr in ("fill", "sort", "resize", "put", "itemset"):
            self._reg(f.value, None, ".%s()" % f.attr)
        self.generic_visit(n)


def raccogli(nome, rice, visti=None):
    """Scritture e usi di `rng` di `nome`, seguendo le chiamate."""
    visti = visti or set()
    if nome in visti:
        return [], 0
    visti = visti | {nome}
    corpo = METODI.get(nome) if rice == "self" else None
    corpo = corpo or FUNZIONI.get(nome) or METODI.get(nome)
    if corpo is None:
        return [], 0
    s = Scansione(rice, nome)
    for st in corpo.body:
        s.visit(st)
    W, r = list(s.scritture), s.rng
    for c, rc in s.chiamate:
        w2, r2 = raccogli(c, rc, visti)
        W += w2
        r += r2
    return W, r


ORDINE = [n for _t, n in _passo.ordine()]
print("ORDINE DEL PASSO: " + " -> ".join(ORDINE))
print("")

PER_LEGGE, RNG = {}, {}
for nome in ORDINE:
    rice = "self" if nome in METODI else "net"
    W, r = raccogli(nome, rice)
    PER_LEGGE[nome] = W
    RNG[nome] = r

# ------------------------------------------------------------------ 1. concorrenti
print("=" * 78)
print("1. SCRITTURE CONCORRENTI: attributi di STATO scritti da PIU' DI UNA legge")
print("=" * 78)
scrittori = {}
for legge, W in PER_LEGGE.items():
    for w in W:
        if w["attributo"] in STATO:
            scrittori.setdefault(w["attributo"], {}).setdefault(legge, []).append(w)
conc = {a: d for a, d in scrittori.items() if len(d) > 1}
solo = {a: d for a, d in scrittori.items() if len(d) == 1}
print("")
print("  attributi di stato scritti nel passo: %d su %d" % (len(scrittori), len(STATO)))
print("  CONCORRENTI (>1 legge): %d   -   da una sola legge: %d" % (len(conc), len(solo)))
print("")
print("  %-14s %-4s %s" % ("attributo", "n.l.", "leggi che lo scrivono (siti per legge)"))
for a in sorted(conc):
    print("  %-14s %-4d %s" % (a, len(conc[a]),
                               ", ".join("%s(%d)" % (l, len(v)) for l, v in conc[a].items())))
print("")
print("  da UNA sola legge: " + ", ".join("%s[%s]" % (a, list(d)[0]) for a, d in sorted(solo.items())))

# ------------------------------------------------------------------ 3. componibilita'
print("")
print("=" * 78)
print("3. COMPONIBILITA' delle scritture di STATO, in tre classi")
print("=" * 78)
ETICHETTA = {
    "incremento": ("A", "INCREMENTO: si compone per SOMMA (e' la regola di Luca)"),
    "mescola": ("A-bis", "MESCOLA `(1-p)X + p*E`: esprimibile come variazione `p*(E-X)`"),
    "estensione": ("S", "ESTENSIONE/TRONCAMENTO strutturale: NON e' una variazione (va DOPO)"),
    None: ("C", "assegnazione INDIPENDENTE dal valore corrente"),
    "vincolo": ("B", "VINCOLO sul corrente (clip/pavimento/modulo/norma): NON e' una variazione"),
    "altro-corrente": ("B", "dipende dal corrente in un modo NON classificato"),
    "in-place": ("B", "mutazione in place (`.fill`, `.sort`, ...)"),
}
CL = {}
for a, d in scrittori.items():
    for legge, siti in d.items():
        for w in siti:
            k, _t = ETICHETTA[w["rhs"]]
            w["classe"] = k
            w["legge"] = legge
            CL.setdefault(k, []).append(w)
print("")
for k in ("A", "A-bis", "S", "C", "B"):
    v = CL.get(k, [])
    testo = [t for _e, t in ETICHETTA.values() if _e == k][0]
    print("  %-6s %3d siti   %s" % (k, len(v), testo))
print("")
print("  ### LE `B` SONO LE SOLE SU CUI MI FERMO: %d siti. Raggruppate per attributo:"
      % len(CL.get("B", [])))
perattr = {}
for w in CL.get("B", []):
    perattr.setdefault(w["attributo"], []).append(w)
for a in sorted(perattr, key=lambda x: -len(perattr[x])):
    L = perattr[a]
    print("")
    print("    %s  -- %d siti, leggi: %s"
          % (a, len(L), ", ".join(sorted(set(w["legge"] for w in L)))))
    for w in sorted(L, key=lambda x: x["riga"])[:8]:
        print("       :%-6d %-24s %s" % (w["riga"], w["dentro"], w["sorgente"][:96]))
    if len(L) > 8:
        print("       ... e altri %d siti (tutti nel json)" % (len(L) - 8))

# ------------------------------------------------------------------ 1-bis. inventario dei clip
print("")
print("=" * 78)
print("1-bis. INVENTARIO DEI CLIP nel percorso vivo del passo pieno (`CLIP-INVENTARIO`)")
print("       SOLO INVENTARIO: la cura (a) NON ne tocca nessuno e non ne aggiunge (Luca).")
print("=" * 78)

_GUARDIE = ("clip", "maximum", "minimum", "nan_to_num", "clip_", "fmax", "fmin")


def _numero(nodo):
    """Il valore numerico di una costante, altrimenti None (anche per `-x`)."""
    if isinstance(nodo, ast.Constant) and isinstance(nodo.value, (int, float)):
        return float(nodo.value)
    if isinstance(nodo, ast.UnaryOp) and isinstance(nodo.op, ast.USub):
        v = _numero(nodo.operand)
        return None if v is None else -v
    return None


_DOMINIO = ("arccos", "arcsin", "arccosh", "arctanh", "sqrt", "log", "log1p", "log2", "log10")


def _in_dominio(padre, chi):
    """`chi` e' l'argomento di una funzione con DOMINIO limitato (`arccos`, `sqrt`, `log`, ...)?

    **A che serve la distinzione** *(criterio confermato da Luca il 2026-09-27)*: un
    `np.clip(nb[:,2], -1, 1)` dentro `arccos` **non limita una grandezza fisica** -- tiene
    l'argomento nel dominio della funzione, dove l'errore di arrotondamento lo porterebbe fuori.
    **Non e' un tetto: e' una condizione di esistenza.**
    """
    for s in ast.walk(padre):
        if isinstance(s, ast.Call) and isinstance(s.func, ast.Attribute) \
                and s.func.attr in _DOMINIO:
            for a in list(s.args) + [k.value for k in s.keywords]:
                for t in ast.walk(a):
                    if t is chi:
                        return True
    return False


def _in_denominatore(padre, chi):
    """`chi` sta al DENOMINATORE di una divisione dentro `padre`?"""
    def _dentro(ramo):
        return any(t is chi for t in ast.walk(ramo))

    for s in ast.walk(padre):
        if isinstance(s, ast.BinOp) and isinstance(s.op, (ast.Div, ast.FloorDiv)) \
                and _dentro(s.right):
            return True
        if isinstance(s, ast.Call) and isinstance(s.func, ast.Attribute) \
                and s.func.attr in ("divide", "true_divide") and len(s.args) > 1 \
                and _dentro(s.args[1]):
            return True
    return False


# le funzioni del percorso VIVO: raggiungibili dalle cinque leggi
def _raggiungibili():
    visti, coda = set(), list(ORDINE)
    while coda:
        x = coda.pop()
        if x in visti:
            continue
        visti.add(x)
        c = METODI.get(x) or FUNZIONI.get(x)
        if c is None:
            continue
        for s in ast.walk(c):
            if isinstance(s, ast.Call):
                f = s.func
                nm = f.attr if isinstance(f, ast.Attribute) else (
                    f.id if isinstance(f, ast.Name) else None)
                if nm and (nm in METODI or nm in FUNZIONI) and nm not in visti:
                    coda.append(nm)
    return visti


VIVE = _raggiungibili()
clip = []
for nome in sorted(VIVE):
    corpo = METODI.get(nome) or FUNZIONI.get(nome)
    if corpo is None:
        continue
    for s in ast.walk(corpo):
        if not (isinstance(s, ast.Call) and isinstance(s.func, ast.Attribute)
                and s.func.attr in _GUARDIE):
            continue
        cost = [c for c in (_numero(a) for a in s.args) if c is not None]
        # ⚠ LA NATURA SI DECIDE DAL POSTO, NON DALLA GRANDEZZA DELLA COSTANTE.
        #   La prima stesura chiamava "anti-zero" solo le costanti <= 1e-6, e cosi'
        #   `np.maximum(self._deg, 1)` -- che e' una guardia anti-divisione-per-zero con la
        #   costante `1` -- finiva fra i TETTI FISICI. Il posto e' quello che dice a che serve:
        #     - al DENOMINATORE di una divisione        -> anti-zero
        #     - dentro `arccos`/`arcsin`/`sqrt`/`log`   -> DOMINIO della funzione
        #     - altrove                                 -> TETTO FISICO, limita un valore
        #   - `maximum(x, 0.0)` esatto                -> PARTE POSITIVA (rettificazione):
        #       e' la FORMA di una legge (<<conta solo la parte positiva>>), non una guardia
        #   - costante <= 1e-6                        -> pavimento EPSILON, guardia numerica
        #       (spesso la grandezza finisce a denominatore piu' tardi, e il sito non lo mostra)
        eps = bool(cost) and 0.0 < min(abs(c) for c in cost) <= 1e-6
        zero = (s.func.attr in ("maximum", "fmax") and len(s.args) == 2
                and any(c == 0.0 for c in cost))
        if _in_denominatore(corpo, s):
            natura = "anti-zero"
        elif _in_dominio(corpo, s):
            natura = "dominio"
        elif zero:
            natura = "parte-positiva"
        elif eps:
            natura = "epsilon"
        elif not cost and s.func.attr in ("maximum", "minimum", "fmax", "fmin") \
                and len(s.args) == 2:
            #   `maximum(t_luce, t_visco)` non ha alcuna costante: NON limita a un valore,
            #   SCEGLIE fra due grandezze. E' un'operazione, non un tetto.
            natura = "selezione"
        else:
            natura = "TETTO-FISICO"
        clip.append({"funzione": nome, "riga": s.lineno, "chiamata": s.func.attr,
                     "costanti": cost, "natura": natura,
                     "sorgente": LINEE[s.lineno - 1].strip()[:140]})
CONTA = {}
for c in clip:
    CONTA[c["natura"]] = CONTA.get(c["natura"], 0) + 1
SPIEGA = {
    "TETTO-FISICO": "limita il VALORE che una legge produce  <-- SOLO QUESTI sono tetti",
    "anti-zero": "sta al DENOMINATORE di una divisione: guardia",
    "dominio": "argomento di arccos/arcsin/sqrt/log: condizione di ESISTENZA",
    "parte-positiva": "`maximum(x, 0.0)` esatto: e' la FORMA di una legge, non una guardia",
    "epsilon": "pavimento <= 1e-6: guardia numerica (il denominatore e' spesso altrove)",
    "selezione": "`maximum(A, B)` senza costanti: SCEGLIE fra due grandezze, non limita",
}
print("")
print("  funzioni del percorso vivo: %d   -   guardie trovate: %d" % (len(VIVE), len(clip)))
print("")
for k in ("TETTO-FISICO", "anti-zero", "epsilon", "dominio", "parte-positiva", "selezione"):
    print("  %-15s %3d   %s" % (k, CONTA.get(k, 0), SPIEGA[k]))
print("")
print("  ### I TETTI FISICI, uno per uno (%d):" % CONTA.get("TETTO-FISICO", 0))
print("  %-6s %-24s %-14s %s" % ("riga", "dentro", "costanti", "sorgente"))
for c in sorted((c for c in clip if c["natura"] == "TETTO-FISICO"), key=lambda x: x["riga"]):
    print("  :%-5d %-24s %-14s %s"
          % (c["riga"], c["funzione"], str(c["costanti"])[:14], c["sorgente"][:74]))
print("")
print("  (le altre %d sono nel json, ciascuna con la sua natura)"
      % (len(clip) - CONTA.get("TETTO-FISICO", 0)))

# ------------------------------------------------------------------ 2. per NODO o per ARCO
print("")
print("=" * 78)
print("2. PER NODO o PER ARCO: la mitosi divide ARCHI, quindi le due nature si applicano")
print("   in modo diverso. La classificazione esce dalle FORME di uno stato REALE.")
print("=" * 78)
# ⚠ LO SNAPSHOT `.npz` DEL PILOTA NON BASTA: contiene solo `d`, `phi`, `i`, `j`, `n`, `pos`
#   -- 2 delle 21. Quindi la natura NON si misura dalle forme, si LEGGE DAL CODICE, con un
#   criterio del codice stesso: **la mitosi estende gli array PER ARCO con la maschera `keep`**
#   (`concatenate([self.d[keep], dh, dh])`: gli archi sopravvissuti piu' le due meta'), e quelli
#   PER NODO senza (`concatenate([self.phi, fm])`). La presenza di `keep` E' il discriminante.
NAT = {}
for a in STATO:
    siti = [w for w in PER_LEGGE["mitosi"]
            if w["attributo"] == a and w["rhs"] == "estensione"]
    con_keep = [w for w in siti if "keep" in w["sorgente"]]
    if con_keep:
        NAT[a] = "per-ARCO"
    elif siti:
        NAT[a] = "per-NODO"
    else:
        NAT[a] = "non-esteso-da-mitosi"
print("")
print("  criterio: la mitosi estende con `keep` cio' che e' PER ARCO. Letto dal codice.")
print("")
print("  %-14s %-22s %s" % ("attributo", "natura", "il sito che lo dice"))
for a in STATO:
    siti = [w for w in PER_LEGGE["mitosi"]
            if w["attributo"] == a and w["rhs"] == "estensione"]
    print("  %-14s %-22s %s" % (a, NAT[a], (":%d" % siti[0]["riga"]) if siti else "-"))
nodo = [a for a, v in NAT.items() if v == "per-NODO"]
arco = [a for a, v in NAT.items() if v == "per-ARCO"]
altro = [a for a, v in NAT.items() if v not in ("per-NODO", "per-ARCO")]
print("")
print("  per NODO (%d): %s" % (len(nodo), ", ".join(sorted(nodo))))
print("  per ARCO (%d): %s" % (len(arco), ", ".join(sorted(arco))))
print("  NON esteso dalla mitosi (%d): %s" % (len(altro), ", ".join(sorted(altro)) or "-"))
print("")
print("  ### -> LE VARIAZIONI PER ARCO degli archi che la mitosi DIVIDE non hanno un")
print("     destinatario dopo la divisione: e' la domanda del punto 2, e riguarda i %d"
      % len(arco))
print("     attributi per arco.")

# ------------------------------------------------------------------ 6. le letture
print("")
print("=" * 78)
print("6. LE LETTURE SPORCHE: dopo la cura, quale legge le serve")
print("=" * 78)
_lett = os.path.join(_QUI, "_etc_letture.json")
righe6 = []
if os.path.exists(_lett):
    L = json.load(io.open(_lett, encoding="utf-8"))
    for s in L["sporche"]:
        a = s["attributo"]
        if a in STATO:
            dest, perche = "FOTOGRAFIA", "classe stato: la fotografia la contiene"
        elif a in STRUTTURA:
            dest, perche = "STRUTTURA VIVA", "una nascita non si nasconde (9-ter)"
        elif a in CACHE:
            dest, perche = "CACHE RICOSTRUITA", "derivata: si ricostruisce, non si fotografa"
        elif a.startswith("_g_"):
            dest, perche = "CONTATORE VIVO", "l'accumulo E' il suo scopo (A8)"
        elif a == "pos":
            dest, perche = "FOTOGRAFIA (ma resta A3-DISEGNO)", "il disegno non deve entrare: cura (c)"
        else:
            dest, perche = "**NON CLASSIFICATO**", "da decidere"
        righe6.append({"legge": s["legge"], "attributo": a, "scritto_da": s["scritto_da"],
                       "destinazione": dest, "perche": perche})
    C6 = {}
    for r in righe6:
        C6[r["destinazione"]] = C6.get(r["destinazione"], 0) + 1
    print("")
    print("  letture sporche esaminate: %d" % len(righe6))
    for k, v in sorted(C6.items(), key=lambda x: -x[1]):
        print("    %-34s %3d" % (k, v))
    manca = [r for r in righe6 if "NON CLASSIFICATO" in r["destinazione"]]
    print("")
    print("  NON CLASSIFICATE: %d %s" % (len(manca),
                                         ("-> " + ", ".join(sorted(set(r["attributo"] for r in manca))))
                                         if manca else "(tutte coperte)"))
else:
    print("")
    print("  MANCA %s: rigira prima _etc_letture.py." % _lett)

# ------------------------------------------------------------------ 5. flussi casuali
print("")
print("=" * 78)
print("5. FLUSSI CASUALI: quante volte ciascuna legge tocca `rng`")
print("=" * 78)
print("")
for nome in ORDINE:
    print("  %-26s %d" % (nome, RNG[nome]))
print("")
print("  -> %d leggi su %d consumano `rng`: senza un flusso PER LEGGE, permutare l'ordine"
      % (sum(1 for n in ORDINE if RNG[n]), len(ORDINE)))
print("     cambia le ESTRAZIONI, e H-ETC-2 fallirebbe per il motivo sbagliato.")

# ------------------------------------------------------------------ 8. costo
print("")
print("=" * 78)
print("8. COSTO DELLA FOTOGRAFIA: n e m REALI dallo stato del pilota, dtype e componenti")
print("   LETTI DAL COSTRUTTORE (`__init__`, :1673-1745). L'aritmetica e' di questo script.")
print("=" * 78)

# (componenti, byte per elemento, la riga del costruttore che lo dice)
FORMA = {
    "phi": (1, 8, 1673), "phivel": (1, 8, 1674), "eta": (1, 8, 1674), "phi_s": (1, 8, 1675),
    "omega_s": (3, 8, 1677), "_spinor_lift": (2, 16, 1682), "_psi_spinor": (2, 16, 1686),
    "perc_chi": (1, 8, 1715), "perc_geom": (1, 8, 1721), "mem_mot": (3, 8, 1738),
    "psi": (1, 16, 1742), "_psi_prec": (1, 16, 1743), "_nb": (3, 8, 3157),
    "_nb_prec": (3, 8, 1993), "psi_spin": (2, 16, 4021),
    "d": (1, 8, 1724), "d0": (1, 8, 1724), "vd": (1, 8, 1724),
    "peq": (1, 8, 1725), "tw": (1, 8, 1725), "twp": (1, 8, 1725),
}
_st = os.path.join(_QUI, "_pilota_prova1", "stati")
_f = [x for x in sorted(os.listdir(_st)) if x.endswith(".npz")] if os.path.isdir(_st) else []
costo = {"stato": None}
if _f:
    import numpy as np
    z = np.load(os.path.join(_st, _f[-1]), allow_pickle=True)
    N = int(z["n"]) if "n" in z.files else len(z["phi"])
    M = len(z["i"])
    print("")
    print("  stato REALE: %s   n = %d nodi   m = %d archi" % (_f[-1], N, M))
    print("")
    print("  %-14s %-9s %-4s %-6s %s" % ("attributo", "natura", "comp", "byte/e", "byte"))
    tot, mancanti = 0, []
    for a in STATO:
        if a not in FORMA:
            mancanti.append(a)
            continue
        c, b, rg = FORMA[a]
        L = M if NAT.get(a) == "per-ARCO" else N
        by = L * c * b
        tot += by
        print("  %-14s %-9s %-4d %-6d %d" % (a, NAT.get(a, "?"), c, b, by))
    print("")
    print("  ### TOTALE DELLA FOTOGRAFIA: %d byte = %.2f MB" % (tot, tot / 1048576.0))
    print("  non coperti (il costo NON e' stimato): %s" % (", ".join(mancanti) or "nessuno"))
    print("")
    print("  E IL CONFRONTO CHE SERVE A GIUDICARE:")
    print("    m/n = %.1f  ->  i 6 array PER ARCO dominano: %d byte su %d (%.0f%%)"
          % (M / float(N),
             sum((M * FORMA[a][0] * FORMA[a][1]) for a in STATO if NAT.get(a) == "per-ARCO"),
             tot,
             100.0 * sum((M * FORMA[a][0] * FORMA[a][1]) for a in STATO
                         if NAT.get(a) == "per-ARCO") / max(tot, 1)))
    print("    UNA COPIA PER PASSO. Il tempo NON lo stimo: dipende dalla banda di memoria")
    print("    della macchina, e una stima inventata sarebbe peggio di nessuna stima.")
    costo = {"stato": _f[-1], "n": N, "m": M, "byte": tot, "non_coperti": mancanti}
else:
    print("")
    print("  NESSUNO stato .npz: il costo NON e' stimato.")

OUT = os.path.join(_QUI, "_etc_progetto.json")
io.open(OUT, "w", encoding="utf-8", newline=chr(10)).write(json.dumps(
    {"ordine": ORDINE, "rng": RNG, "costo": costo,
     "concorrenti": {a: {l: [w["riga"] for w in v] for l, v in d.items()} for a, d in conc.items()},
     "clip": clip, "natura_nodo_arco": NAT, "letture_dopo": righe6, "classi": {k: sorted(v, key=lambda x: (x["attributo"], x["riga"])) for k, v in CL.items()}},
    indent=1, ensure_ascii=False, sort_keys=True))
print("")
print("scritto: " + OUT)
