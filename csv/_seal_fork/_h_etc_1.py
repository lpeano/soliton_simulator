# -*- coding: utf-8 -*-
"""**`H-ETC-1` — NESSUNA `calcola_psi` SENZA `w` DENTRO `passo_pieno`.**

**Che cosa certifica:** che i pesi `w` si calcolino **una volta** dalla fotografia di inizio passo
e si **passino**, invece di essere **ricalcolati** dentro `calcola_psi` in punti diversi del passo.
E' la meta' `CENS-A7` della cura `ETC-PASSO`, e la radice di `PSI-FLASH`: `memoria_hebbiana_moto`
chiama `calcola_psi()` **senza `w`** dopo la mitosi, e quella `psi` entra in `pozzo_grafo`, quindi
nella spinta `S09` **dello stesso passo**.

**L'intento era GIA' SCRITTO nel codice** *(commento di `calcola_psi`: «Non ricalcolare psi in
punti diversi del passo: quello introdurrebbe letture miste t/t+1»)* **e non era fatto
rispettare**: e' `A8`, ed e' la ragione per cui questo presidio esiste.

> ### 🛑 **IL CASO CHE DEVE FALLIRE, e sono DUE (`P1-sexies`, `A9`):**
> **①** girato sul codice **di oggi** *(blob `e203f9a8`)* **deve contare 8, non 0**. Se contasse 0
>    **non guarderebbe niente**, e ci si ferma.
> **②** rimettere **una** chiamata senza `w` dentro una delle cinque leggi **deve far fallire** il
>    presidio. Si prova su **due sorgenti sintetici**, uno che deve passare e uno che deve
>    fallire: il **collaudo a due facce**, la stessa cosa che su `H-ETC-2` ha impedito di
>    consegnare una macchina che dice sempre NO.

**COME GUARDA:** l'AST. Dalle cinque leggi *(l'ordine si legge da `csv/_passo.py`)* calcola le
funzioni **raggiungibili**, e conta le chiamate a `calcola_psi` **prive di argomenti**.
**⚠ IL LIMITE (`A9`):** analisi **statica e per nome**. Una chiamata dietro un alias o un
`getattr` **non si vede**, e una in un ramo mai eseguito **conta**. **Quindi il conto e' un LIMITE
INFERIORE**, e il presidio **non** certifica l'assenza: certifica che **i siti visibili** sono a
posto. Chi certifica il comportamento e' `H-ETC-2`.

COMANDO:  python csv/_seal_fork/_h_etc_1.py
USCITA:   0 se zero chiamate senza `w` dentro il passo, 1 altrimenti, 2 se il COLLAUDO fallisce.
          **Sul blob di oggi ci si ASPETTA 1, con conto 8.**
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
ATTESO_OGGI = 7          # 2026-09-28: era 8, e l'ottavo era :6529 in _togli_rotazione_rigida,
#   cioe' L'UNICO in un RAMO MORTO (L_CONSERVA). Archiviato quel ramo, le 7 che restano sono
#   TUTTE VIVE, e il conto dice UNA cosa sola invece di due.


def analizza(sorgente, leggi):
    """(siti_senza_w, siti_con_w, funzioni_raggiungibili) dalle `leggi` date."""
    arb = ast.parse(sorgente)
    metodi, funzioni = {}, {}
    for n in ast.walk(arb):
        if isinstance(n, ast.ClassDef) and n.name == "Rete":
            for k in n.body:
                if isinstance(k, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    metodi[k.name] = k
    for n in arb.body:
        if isinstance(n, ast.FunctionDef):
            funzioni[n.name] = n

    def chiamate(corpo):
        out = set()
        for n in ast.walk(corpo):
            if isinstance(n, ast.Call):
                f = n.func
                nm = f.attr if isinstance(f, ast.Attribute) else (
                    f.id if isinstance(f, ast.Name) else None)
                if nm and (nm in metodi or nm in funzioni):
                    out.add(nm)
        return out

    vive, coda = set(), [x for x in leggi if x in metodi or x in funzioni]
    while coda:
        x = coda.pop()
        if x in vive:
            continue
        vive.add(x)
        c = metodi.get(x) or funzioni.get(x)
        if c is None:
            continue
        coda += [y for y in chiamate(c) if y not in vive]

    righe = sorgente.split(chr(10))
    cop = {}
    for n in ast.walk(arb):
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for l in range(n.lineno, (n.end_lineno or n.lineno) + 1):
                p = cop.get(l)
                if p is None or n.lineno > p[0]:
                    cop[l] = (n.lineno, n.name)

    senza, con = [], []
    for n in ast.walk(arb):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) \
                and n.func.attr == "calcola_psi":
            dentro = cop.get(n.lineno, (0, "<modulo>"))[1]
            if dentro not in vive:
                continue
            voce = {"riga": n.lineno, "dentro": dentro,
                    "sorgente": righe[n.lineno - 1].strip()[:120]}
            (con if (n.args or n.keywords) else senza).append(voce)
    return senza, con, vive


# ====================================================================== il COLLAUDO
# Due sorgenti SINTETICI, con la risposta NOTA. **Il caso che deve FALLIRE e' il piu'
# importante**: senza di lui il presidio potrebbe essere una macchina che dice sempre SI.
_COLLAUDO_BUONO = '''
def scuoti_vuoto(net):
    net.calcola_psi(net._pesi())
class Rete:
    def calcola_psi(self, w=None): pass
    def _pesi(self): return 1
    def step(self):
        w = self._pesi()
        self.calcola_psi(w)
        self._aiuto(w)
    def _aiuto(self, w): self.calcola_psi(w)
    def mitosi(self): pass
    def rilassa_disegno(self): pass
    def memoria_hebbiana_moto(self): self.calcola_psi(self._pesi())
    def fuori_dal_passo(self): self.calcola_psi()
'''

_COLLAUDO_CATTIVO = '''
def scuoti_vuoto(net):
    net.calcola_psi(net._pesi())
class Rete:
    def calcola_psi(self, w=None): pass
    def _pesi(self): return 1
    def step(self):
        w = self._pesi()
        self.calcola_psi(w)
        self._aiuto(w)
    def _aiuto(self, w): self.calcola_psi()
    def mitosi(self): pass
    def rilassa_disegno(self): pass
    def memoria_hebbiana_moto(self): self.calcola_psi(self._pesi())
    def fuori_dal_passo(self): self.calcola_psi()
'''

LEGGI_FINTE = ["scuoti_vuoto", "step", "mitosi", "rilassa_disegno", "memoria_hebbiana_moto"]


def collaudo():
    """Ritorna (ok, righe). Il caso BUONO deve dare 0, il CATTIVO deve dare 1."""
    righe = []
    sb, cb, vb = analizza(_COLLAUDO_BUONO, LEGGI_FINTE)
    ok1 = (len(sb) == 0 and len(cb) == 4)
    righe.append({"caso": "BUONO (deve dare 0 senza-w)", "senza_w": len(sb),
                  "con_w": len(cb), "passa": ok1})
    sc, cc, vc = analizza(_COLLAUDO_CATTIVO, LEGGI_FINTE)
    ok2 = (len(sc) == 1 and sc[0]["dentro"] == "_aiuto")
    righe.append({"caso": "CATTIVO (deve dare 1, in `_aiuto`)", "senza_w": len(sc),
                  "con_w": len(cc), "passa": ok2,
                  "dove": sc[0]["dentro"] if sc else None})
    # e la terza cosa che il collaudo deve provare: `fuori_dal_passo` NON si conta
    ok3 = all(v["dentro"] != "fuori_dal_passo" for v in sb + sc)
    righe.append({"caso": "`fuori_dal_passo` NON deve essere contata", "passa": ok3})
    return (ok1 and ok2 and ok3), righe


def principale():
    print("=" * 78)
    print("COLLAUDO A DUE FACCE (P1-sexies): il presidio sa dire SI e sa dire NO?")
    print("=" * 78)
    ok, righe = collaudo()
    for r in righe:
        print("  %-42s %s" % (r["caso"], "PASSA" if r["passa"] else "### FALLISCE"))
        if "senza_w" in r:
            print("      senza w: %d   con w: %d%s"
                  % (r["senza_w"], r["con_w"],
                     ("   dove: " + str(r.get("dove"))) if r.get("dove") else ""))
    if not ok:
        print("")
        print("### IL COLLAUDO FALLISCE: IL PRESIDIO NON E' CONSEGNABILE.")
        return 2
    print("")
    print("  -> il presidio distingue: 0 sul caso buono, 1 sul cattivo, e non conta")
    print("     le chiamate FUORI dal passo.")
    print("")

    sorgente = io.open(SIM, encoding="utf-8").read()
    blob = hashlib.sha1(io.open(SIM, "rb").read()).hexdigest()
    leggi = [n for _t, n in _passo.ordine()]
    senza, con, vive = analizza(sorgente, leggi)

    print("=" * 78)
    print("IL CODICE VERO: %s   blob sha1-BYTE %s" % (os.path.basename(SIM), blob[:8]))
    print("=" * 78)
    print("")
    print("  le cinque leggi: " + " -> ".join(leggi))
    print("  funzioni RAGGIUNGIBILI dalle cinque leggi: %d" % len(vive))
    print("")
    print("  CHIAMATE A `calcola_psi` DENTRO IL PASSO: %d   (con `w`: %d, SENZA: %d)"
          % (len(senza) + len(con), len(con), len(senza)))
    print("")
    print("  %-7s %-26s %s" % ("riga", "dentro", "sorgente"))
    for v in sorted(con, key=lambda x: x["riga"]):
        print("  :%-6d %-26s %s   [w]" % (v["riga"], v["dentro"], v["sorgente"][:60]))
    for v in sorted(senza, key=lambda x: x["riga"]):
        print("  :%-6d %-26s %s   ### SENZA w" % (v["riga"], v["dentro"], v["sorgente"][:60]))
    print("")
    print("=" * 78)
    print("### H-ETC-1 : %d chiamate SENZA `w` dentro `passo_pieno`   (atteso oggi: %d)"
          % (len(senza), ATTESO_OGGI))
    if len(senza) == 0:
        print("    NESSUNA: il presidio PASSA.")
    else:
        print("    IL PRESIDIO FALLISCE. Sul blob di oggi e' il risultato ATTESO:")
        print("    l'intento era scritto nel commento di `calcola_psi` e non era fatto")
        print("    rispettare (`A8`), e la cura ETC-PASSO non e' ancora fatta.")
        if len(senza) != ATTESO_OGGI:
            print("    ⚠ MA IL CONTO NON E' %d: e' %d. Il codice e' cambiato rispetto alla"
                  % (ATTESO_OGGI, len(senza)))
            print("      FASE 0, oppure l'analisi e' cambiata. VA GUARDATO prima di procedere.")
    print("=" * 78)

    OUT = os.path.join(_QUI, "_h_etc_1.json")
    io.open(OUT, "w", encoding="utf-8", newline=chr(10)).write(json.dumps(
        {"blob_sim": blob, "leggi": leggi, "raggiungibili": len(vive),
         "atteso_oggi": ATTESO_OGGI, "senza_w": sorted(senza, key=lambda x: x["riga"]),
         "con_w": sorted(con, key=lambda x: x["riga"]), "collaudo": righe},
        indent=1, ensure_ascii=False, sort_keys=True))
    print("")
    print("scritto: " + OUT)
    return 1 if senza else 0


if __name__ == "__main__":
    sys.exit(principale())
