# -*- coding: utf-8 -*-
"""**T3, primo pezzo: OGNI SCRITTURA DI STATO nelle CINQUE FORME della SOVRAPPOSIZIONE.**

**Il principio, come l'ha dato Luca** *(2026-09-28)*: **ogni legge contribuisce una VARIAZIONE, e le
variazioni si SOMMANO.** Le cinque forme ammesse:

| forma | come si compone |
|---|---|
| **1 · variazione** | `x += d` oppure `x = x + d` -> **si somma** |
| **2 · rilassamento** | verso un bersaglio: contribuisce `alpha * (bersaglio - x)` -> **e' una variazione** |
| **3 · derivata** | `psi`, `w`, il pozzo: **si calcolano UNA volta dalla fotografia** |
| **4 · vincolo** | pavimento, avvolgimento, normalizzazione: **si applica UNA volta DOPO la somma** |
| **5 · struttura** | estensioni e troncamenti: **fase a parte, dopo la dinamica** |

### **Tutto cio' che non rientra in nessuna delle cinque e' un'ECCEZIONE, e va portata a Luca.**

**COME CLASSIFICA, e il criterio e' dichiarato:**
  - `+=` / `x = x + d` / `x = d + x`                      -> **variazione**
  - `x = (1-a)*x + a*E`  oppure  `x = x + a*(E - x)`       -> **rilassamento**
  - `x = <espressione senza x>` **e** `x` e' una derivata  -> **derivata**
  - `x = f(x)` con `f` in {pavimento, `maximum`, `minimum`, `clip`, `%`, divisione per una norma}
                                                          -> **vincolo**
  - `x = concatenate/vstack/...([x, ...])`  oppure `x = x[:k]`  -> **struttura**
  - `x = <espressione senza x>` e `x` **non** e' una derivata -> ### **ECCEZIONE**: e' una
    ASSEGNAZIONE PIENA, e <<sommare le variazioni>> non e' definito se due leggi la fanno.

**⚠ IL LIMITE (`A9`), lo stesso della FASE 0:** analisi **statica e per nome**. Alias e `getattr`
non si vedono; un ramo mai eseguito conta. **Quindi l'elenco delle eccezioni e' un LIMITE
INFERIORE**, e serve a decidere, non a certificare.

COMANDO:  python csv/_test_fork/_etc_sovrapposizione.py
"""
import ast
import hashlib
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
RIG = SRC.split(chr(10))
ARB = ast.parse(SRC)
BLOB = hashlib.sha1(io.open(SIM, "rb").read()).hexdigest()

STATO = ["d", "d0", "phi", "phi_s", "phivel", "psi", "psi_spin", "_psi_spinor", "_psi_prec",
         "_spinor_lift", "omega_s", "_nb", "_nb_prec", "eta", "tw", "twp", "vd", "peq",
         "mem_mot", "perc_chi", "perc_geom"]
# le grandezze DERIVATE: si ricalcolano dallo stato, non evolvono per conto proprio
DERIVATE = {"psi", "psi_spin", "_psi_spinor", "_psi_prec", "_spinor_lift", "_nb_prec"}
ESTENDE = ("concatenate", "vstack", "hstack", "stack", "append", "tile", "pad")
VINCOLO = ("_pav_d0", "_floor_d0", "_smorza", "_sd0", "_nasce", "satura", "clip",
           "maximum", "minimum", "nan_to_num")

METODI, FUNZIONI = {}, {}
for _n in ast.walk(ARB):
    if isinstance(_n, ast.ClassDef) and _n.name == "Rete":
        for _k in _n.body:
            if isinstance(_k, (ast.FunctionDef, ast.AsyncFunctionDef)):
                METODI[_k.name] = _k
for _n in ARB.body:
    if isinstance(_n, ast.FunctionDef):
        FUNZIONI[_n.name] = _n


def _radice(n):
    while isinstance(n, (ast.Attribute, ast.Subscript)):
        n = n.value
    return n.id if isinstance(n, ast.Name) else None


def _attr(n):
    while isinstance(n, ast.Subscript):
        n = n.value
    return n.attr if isinstance(n, ast.Attribute) else None


def _uguale(a, b):
    try:
        return ast.unparse(a) == ast.unparse(b)
    except Exception:
        return False


def _legge(nodo, rice, attr):
    """La parte destra rilegge il VALORE di `rice.attr`? (`.dtype` & co. non contano)"""
    NONVAL = ("dtype", "shape", "size", "ndim", "nbytes", "T", "flags")
    coda = [nodo]
    while coda:
        s = coda.pop()
        if isinstance(s, ast.Attribute) and s.attr in NONVAL:
            continue
        if isinstance(s, ast.Attribute) and s.attr == attr and _radice(s) == rice:
            return True
        coda.extend(ast.iter_child_nodes(s))
    return False


def alias_di(corpo, rice):
    """Le variabili LOCALI che sono un ALIAS di `rice.<attr>`: `x = self.attr` o `.copy()`.

    ### **Senza questo il classificatore sbaglia la maggior parte delle scritture**, e l'ho
    visto: `self.phivel = _phivel_t + delta_phivel` **E'** una variazione -- `_phivel_t` e' la
    **FOTOGRAFIA** di `phivel` presa a inizio `step` -- ma sintatticamente la parte destra non
    nomina `self.phivel`, quindi finiva fra le ECCEZIONI.
    **E' la scoperta che conta per `T3`:** il codice scrive **GIA'** in forma `foto + delta`,
    solo che la fotografia vive in una **variabile locale** invece che in un oggetto dichiarato.
    """
    mappa = {}
    for n in ast.walk(corpo):
        if not isinstance(n, ast.Assign) or len(n.targets) != 1:
            continue
        b = n.targets[0]
        if not isinstance(b, ast.Name):
            continue
        v = n.value
        # `x = self.attr`  oppure  `x = self.attr.copy()`  oppure  `x = np.array(self.attr, ...)`
        cand = v
        if isinstance(cand, ast.Call):
            if isinstance(cand.func, ast.Attribute) and cand.func.attr in ("copy", "array",
                                                                           "asarray"):
                cand = cand.func.value if cand.func.attr == "copy" else (
                    cand.args[0] if cand.args else cand)
        if isinstance(cand, ast.Attribute) and _radice(cand) == rice:
            mappa.setdefault(b.id, cand.attr)
    return mappa


def forma(bersaglio, valore, forma_op, rice, attr, alias=None):
    """La FORMA della scrittura, fra le cinque, oppure `ECCEZIONE`."""
    if forma_op.endswith("+="):
        return "1-variazione", "incremento `+=`"
    if valore is None:
        return "ECCEZIONE", "mutazione in place (`.fill`, `.sort`, ...)"
    # ---- espressione condizionale: si guardano i due rami
    alias = alias or {}
    if isinstance(valore, ast.IfExp):
        f1 = forma(bersaglio, valore.body, forma_op, rice, attr, alias)
        f2 = forma(bersaglio, valore.orelse, forma_op, rice, attr, alias)
        for pref in ("5-struttura", "ECCEZIONE", "4-vincolo", "2-rilassamento",
                     "1-variazione", "3-derivata"):
            if f1[0] == pref or f2[0] == pref:
                return pref, "ramo di un'espressione condizionale: " + (
                    f1[1] if f1[0] == pref else f2[1])
    testo = ""
    try:
        testo = ast.unparse(valore)
    except Exception:
        pass
    # ---- 5 struttura
    if isinstance(valore, ast.Call) and isinstance(valore.func, ast.Attribute) \
            and valore.func.attr in ESTENDE:
        return "5-struttura", "estensione `%s`" % valore.func.attr
    if isinstance(valore, ast.Subscript) and _radice(valore) == rice and _attr(valore) == attr:
        return "5-struttura", "troncamento `x[:k]`"
    def _rilegge_con_alias(v):
        if _legge(v, rice, attr):
            return True
        for n in ast.walk(v):
            if isinstance(n, ast.Name) and alias.get(n.id) == attr:
                return True
        return False
    rilegge = _rilegge_con_alias(valore)
    # ---- 1 variazione, 2 rilassamento
    if isinstance(valore, ast.BinOp) and isinstance(valore.op, ast.Add):
        for lato, altro in ((valore.left, valore.right), (valore.right, valore.left)):
            _e_x = _uguale(lato, bersaglio) or (isinstance(lato, ast.Name)
                                               and alias.get(lato.id) == attr)
            if _e_x:
                # `x + a*(bersaglio - x)` e' un RILASSAMENTO, non una variazione qualunque
                if _rilegge_con_alias(altro):
                    return "2-rilassamento", "`x + a*(bersaglio - x)`"
                _via = ("" if _uguale(lato, bersaglio)
                        else " (la fotografia vive in una LOCALE: `%s`)" % ast.unparse(lato)[:24])
                return "1-variazione", "`x = x + d`" + _via
        if rilegge:
            return "2-rilassamento", "`(1-a)*x + a*E` o forma equivalente"
    # ---- 4 vincolo
    if rilegge:
        if isinstance(valore, ast.BinOp) and isinstance(valore.op, ast.Mod):
            return "4-vincolo", "avvolgimento `%`"
        if isinstance(valore, ast.BinOp) and isinstance(valore.op, ast.Div):
            return "4-vincolo", "normalizzazione (divisione per una norma)"
        for v in VINCOLO:
            if v in testo:
                return "4-vincolo", "limite `%s`" % v
        return "ECCEZIONE", "rilegge il valore corrente in un modo NON classificato"
    # ---- 3 derivata
    if attr in DERIVATE:
        return "3-derivata", "assegnazione piena di una grandezza DERIVATA"
    # ---- resta l'assegnazione piena di una grandezza che NON e' derivata
    return "ECCEZIONE", ("ASSEGNAZIONE PIENA di una grandezza non derivata: <<sommare le "
                         "variazioni>> non e' definito se due leggi la fanno")


def raggiungibili(leggi):
    visti, coda = set(), list(leggi)
    while coda:
        x = coda.pop()
        if x in visti:
            continue
        visti.add(x)
        c = METODI.get(x) or FUNZIONI.get(x)
        if c is None:
            continue
        for n in ast.walk(c):
            if isinstance(n, ast.Call):
                f = n.func
                nm = f.attr if isinstance(f, ast.Attribute) else (
                    f.id if isinstance(f, ast.Name) else None)
                if nm and (nm in METODI or nm in FUNZIONI) and nm not in visti:
                    coda.append(nm)
    return visti


LEGGI = [n for _t, n in _passo.ordine()]
VIVE = sorted(raggiungibili(LEGGI))
print("simulatore blob sha1-BYTE %s" % BLOB[:8])
print("funzioni nel perimetro: %d" % len(VIVE))
print("")

TUTTE = []
ALIAS = {}
for nome in VIVE:
    c = METODI.get(nome) or FUNZIONI.get(nome)
    if c is None:
        continue
    rice = "self" if nome in METODI else "net"
    ALIAS[nome] = alias_di(c, rice)
    for n in ast.walk(c):
        bers = []
        if isinstance(n, ast.Assign):
            bers = [(x, n.value, "[]=" if isinstance(x, ast.Subscript) else "=")
                    for x in n.targets]
        elif isinstance(n, ast.AugAssign):
            bers = [(n.target, n.value, "[]+=" if isinstance(n.target, ast.Subscript) else "+=")]
        for b, val, op in bers:
            if _radice(b) != rice:
                continue
            a = _attr(b)
            if a not in STATO:
                continue
            f, perche = forma(b, val, op, rice, a, ALIAS.get(nome, {}))
            TUTTE.append({"dentro": nome, "riga": b.lineno, "attributo": a, "op": op,
                          "forma": f, "perche": perche,
                          "sorgente": RIG[b.lineno - 1].strip()[:120]})

CONTA = {}
for w in TUTTE:
    CONTA[w["forma"]] = CONTA.get(w["forma"], 0) + 1
print("=" * 96)
print("LE %d SCRITTURE DI STATO, nelle CINQUE FORME" % len(TUTTE))
print("=" * 96)
print("")
for k in ("1-variazione", "2-rilassamento", "3-derivata", "4-vincolo", "5-struttura", "ECCEZIONE"):
    print("  %-16s %3d" % (k, CONTA.get(k, 0)))
print("")

ECC = [w for w in TUTTE if w["forma"] == "ECCEZIONE"]
print("=" * 96)
print("LE ECCEZIONI: %d scritture che NON rientrano in nessuna delle cinque" % len(ECC))
print("=" * 96)
per = {}
for w in ECC:
    per.setdefault(w["attributo"], []).append(w)
print("")
print("  attributi coinvolti: %d   ->   %s" % (len(per), ", ".join(sorted(per))))
print("")
for a in sorted(per, key=lambda x: -len(per[x])):
    L = per[a]
    leggi = sorted({w["dentro"] for w in L})
    print("  --- %-14s %2d scritture, in %s" % (a, len(L), ", ".join(leggi)[:56]))
    for w in sorted(L, key=lambda x: x["riga"])[:6]:
        print("      :%-6d %-22s %s" % (w["riga"], w["dentro"], w["sorgente"][:74]))
    if len(L) > 6:
        print("      ... e altre %d (tutte nel json)" % (len(L) - 6))

# --- per ATTRIBUTO: chi assegna, chi incrementa
print("")
print("=" * 96)
print("PER ATTRIBUTO: chi lo INCREMENTA, chi lo ASSEGNA, e in quante forme")
print("=" * 96)
print("")
print("  %-14s %-28s %-28s %s" % ("attributo", "incrementa (1,2)", "assegna pieno (3,ECC)", "forme"))
RIGHE_ATTR = {}
for a in STATO:
    W = [w for w in TUTTE if w["attributo"] == a]
    inc = sorted({w["dentro"] for w in W if w["forma"] in ("1-variazione", "2-rilassamento")})
    ass = sorted({w["dentro"] for w in W if w["forma"] in ("3-derivata", "ECCEZIONE")})
    forme = sorted({w["forma"] for w in W})
    RIGHE_ATTR[a] = {"incrementano": inc, "assegnano": ass, "forme": forme, "n": len(W)}
    print("  %-14s %-28s %-28s %s" % (a, ", ".join(x[:12] for x in inc)[:28],
                                      ", ".join(x[:12] for x in ass)[:28],
                                      " ".join(f.split("-")[0] for f in forme)))

OUT = os.path.join(_QUI, "_etc_sovrapposizione.json")
io.open(OUT, "w", encoding="utf-8", newline=chr(10)).write(json.dumps(
    {"blob_sim": BLOB, "leggi": LEGGI, "funzioni": len(VIVE), "conta": CONTA,
     "per_attributo": RIGHE_ATTR, "eccezioni": sorted(ECC, key=lambda x: x["riga"]),
     "tutte": sorted(TUTTE, key=lambda x: x["riga"])},
    indent=1, ensure_ascii=False, sort_keys=True))
print("")
print("scritto: " + OUT)
