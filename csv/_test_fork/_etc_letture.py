# -*- coding: utf-8 -*-
"""**FASE 0 della cura (a) `ETC-PASSO`: CHI LEGGE STATO GIA' MODIFICATO DENTRO LO STESSO PASSO.**

**Che cosa misura:** per ciascuna delle **cinque leggi** del passo *(l'ordine si legge da
`csv/_passo.py`, non si ricopia)*, gli **attributi di stato** che **legge** e quelli che
**scrive** -- ricorsivamente, seguendo le chiamate a metodi della classe `Rete`.
Poi incrocia: **una lettura della legge `k` e' SPORCA se una legge `j < k` dello stesso passo ha
gia' scritto quell'attributo.** L'insieme delle letture sporche **e' la cura (a)**: sono
esattamente i punti che una fotografia di inizio passo renderebbe sincroni.

**PERCHE' DALL'AST E NON A OCCHIO:** e' `L-NUMERI`. Un elenco di letture compilato leggendo il
file **non ha provenienza**, e su cinque leggi che chiamano decine di metodi **non e' nemmeno
affidabile**. Qui il conto esce da uno script che si rigira.

**⚠ IL LIMITE, e va detto prima dei numeri (`A9`):** questa e' un'analisi **STATICA e per NOME**.
  - un attributo passato a una funzione e mutato **la' dentro** *(alias)* **non si vede**;
  - `getattr` / attributi costruiti dinamicamente **non si vedono**;
  - la ricorsione segue **solo `self.<metodo>()`** e, per `scuoti_vuoto(net)`, **solo `net.<...>`**;
  - una lettura **dentro un ramo mai eseguito** conta come lettura: **e' statica, non dinamica**.
**Quindi il risultato e' un LIMITE INFERIORE delle letture sporche, mai un elenco completo.**
Serve a **progettare** la cura, e **non** a certificarla: chi certifica e' il presidio `H-ETC-2`,
che confronta lo STATO dopo una PERMUTAZIONE dell'ordine.

COMANDO:  python csv/_test_fork/_etc_letture.py
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

# ------------------------------------------------------------------ indice dei corpi
METODI = {}
for _n in ast.walk(ARB):
    if isinstance(_n, ast.ClassDef) and _n.name == "Rete":
        for _k in _n.body:
            if isinstance(_k, (ast.FunctionDef, ast.AsyncFunctionDef)):
                METODI[_k.name] = _k
FUNZIONI = {n.name: n for n in ARB.body if isinstance(n, ast.FunctionDef)}


def _radice(nodo):
    """Il nome del ricevitore di una catena di attributi: `self.a.b` -> `self`, `net.x` -> `net`."""
    while isinstance(nodo, (ast.Attribute, ast.Subscript)):
        nodo = nodo.value
    return nodo.id if isinstance(nodo, ast.Name) else None


def _attr(nodo):
    """`self.d` -> `d`; `self.d[m]` -> `d`; altrimenti None."""
    while isinstance(nodo, ast.Subscript):
        nodo = nodo.value
    if isinstance(nodo, ast.Attribute):
        return nodo.attr
    return None


class Scansione(ast.NodeVisitor):
    """Letture, scritture e chiamate a metodi, per UN corpo, sul ricevitore `rice`."""

    def __init__(self, rice):
        self.rice = rice
        self.letture, self.scritture, self.chiamate = set(), set(), set()

    def _registra(self, nodo, dove):
        if _radice(nodo) != self.rice:
            return
        a = _attr(nodo)
        if a and not a.startswith("__"):
            dove.add(a)

    def visit_Assign(self, n):
        for t in n.targets:
            self._registra(t, self.scritture)
            # `self.d[m] = x` legge anche l'indice e il contenitore: e' una scrittura PARZIALE
            if isinstance(t, ast.Subscript):
                self._registra(t, self.letture)
        self.visit(n.value)
        for t in n.targets:
            for s in ast.walk(t):
                if isinstance(s, ast.Subscript):
                    self.visit(s.slice)

    def visit_AugAssign(self, n):
        self._registra(n.target, self.scritture)
        self._registra(n.target, self.letture)   # `+=` LEGGE e scrive
        self.visit(n.value)

    def visit_Attribute(self, n):
        self._registra(n, self.letture)
        self.generic_visit(n)

    def visit_Call(self, n):
        f = n.func
        if isinstance(f, ast.Attribute) and _radice(f) == self.rice and isinstance(f.value, ast.Name):
            if f.attr in METODI:
                self.chiamate.add(f.attr)
            else:
                # metodo numpy in place: `self.d.fill(...)`, `.sort()`, `.clip(out=...)`
                pass
        elif isinstance(f, ast.Attribute) and isinstance(f.value, ast.Attribute):
            if _radice(f.value) == self.rice and f.attr in ("fill", "sort", "resize", "put",
                                                            "itemset", "setfield"):
                self._registra(f.value, self.scritture)
        elif isinstance(f, ast.Name) and f.id in FUNZIONI:
            self.chiamate.add("@" + f.id)
        self.generic_visit(n)


_MEMO = {}


def analizza(nome, rice, visti=None):
    """Letture e scritture di `nome`, seguendo le chiamate. `visti` spezza la ricorsione."""
    visti = visti or set()
    if nome in visti:
        return set(), set()
    visti = visti | {nome}
    corpo = FUNZIONI[nome[1:]] if nome.startswith("@") else METODI.get(nome) or FUNZIONI.get(nome)
    if corpo is None:
        return set(), set()
    s = Scansione(rice)
    for st in corpo.body:
        s.visit(st)
    L, W = set(s.letture), set(s.scritture)
    for c in s.chiamate:
        r = "net" if c.startswith("@") else rice
        l2, w2 = analizza(c, r, visti)
        L |= l2
        W |= w2
    return L, W


# ------------------------------------------------------------------ le cinque leggi
ORDINE = [nome for _t, nome in _passo.ordine()]
print("ORDINE DEL PASSO, letto da csv/_passo.py: " + " -> ".join(ORDINE))
print("")

RIS = {}
for nome in ORDINE:
    rice = "net" if nome not in METODI else "self"
    chiave = ("@" + nome) if nome not in METODI else nome
    L, W = analizza(chiave, rice)
    RIS[nome] = {"legge": sorted(L), "scrive": sorted(W)}

# ------------------------------------------------------------------ le letture SPORCHE
print("=" * 78)
print("LETTURE SPORCHE: la legge k legge X, e una legge j<k dello STESSO passo ha gia' scritto X")
print("=" * 78)
sporche = []
for i, nome in enumerate(ORDINE):
    prima = {}
    for j in range(i):
        for x in RIS[ORDINE[j]]["scrive"]:
            prima.setdefault(x, []).append(ORDINE[j])
    mie = [x for x in RIS[nome]["legge"] if x in prima]
    RIS[nome]["sporche"] = {x: prima[x] for x in mie}
    print("")
    print("  %d. %s   legge %d, scrive %d,  SPORCHE %d"
          % (i + 1, nome, len(RIS[nome]["legge"]), len(RIS[nome]["scrive"]), len(mie)))
    for x in sorted(mie):
        print("       %-22s gia' scritto da: %s" % (x, ", ".join(prima[x])))
        sporche.append((nome, x, prima[x]))

print("")
print("=" * 78)
print("TOTALE letture sporche: %d   su %d leggi"
      % (len(sporche), sum(1 for k in ORDINE if RIS[k]["sporche"])))
print("ATTRIBUTI coinvolti: %d  ->  %s"
      % (len(set(x for _a, x, _b in sporche)), ", ".join(sorted(set(x for _a, x, _b in sporche)))))
print("=" * 78)

OUT = os.path.join(_QUI, "_etc_letture.json")
io.open(OUT, "w", encoding="utf-8", newline=chr(10)).write(
    json.dumps({"ordine": ORDINE, "leggi": RIS,
                "sporche": [{"legge": a, "attributo": b, "scritto_da": c} for a, b, c in sporche]},
               indent=1, ensure_ascii=False, sort_keys=True))
print("scritto: " + OUT)
