# -*- coding: utf-8 -*-
"""INVENTARIO — ogni punto del simulatore che SCRIVE lo stato. Generato dall'AST, non a mano.

⚠ FASE A del registro della fisica: **viene PRIMA delle schede**. Ogni scrittore trovato qui
  dovra' finire in una scheda di `doc/REGISTRO_FISICA.md`. **Nessuno escluso.**

⚠ SOLA LETTURA. Non importa il simulatore, non esegue nulla: **costruisce l'AST del sorgente**.
  Puo' girare mentre un run e' in corso.

COSA CERCA, e perche' NON basta una `grep`:
  * `self.x = ...`            assegnamento diretto
  * `self.x[...] = ...`       scrittura per INDICE
  * `self.x += ...`           assegnamento AUMENTATO *(che una `grep` di `=` non vede)*
  * `self.x[...] += ...`      aumentato per indice
  * `np.add.at(self.x, ...)`  scrittura IN PLACE con una chiamata *(nessun `=` nella riga)*
  * `self.x = np.concatenate([...])`  **CONCATENAZIONE**: cambia la LUNGHEZZA, cioe' fa nascere
                              o morire archi/nodi. Va marcata a parte: li' il delta
                              elemento-per-elemento **non esiste** *(e' cio' che ha fatto non
                              chiudere il bilancio di `G4`)*.

E PER OGNUNO: **la funzione**, **la riga**, e **il FLAG che lo governa** -- cioe' la costante di
  modulo in maiuscolo che compare nel test di un `if` che lo racchiude. Se non c'e', **`sempre`**.

⚠ NON si decide da soli cosa e' "stato fisico": si dichiara. `FISICHE` qui sotto e' la lista, e
  **tutto cio' che NON e' in lista compare lo stesso**, marcato `non-fisico (dichiarato)`.
  **Cosi' l'esclusione e' VISIBILE invece che silenziosa.**

⚠ `P1-sexies`: il collaudo gira su un **modulo sintetico** con scrittori NOTI, **compresi tre
  nascosti** -- un aumentato dentro una funzione ANNIDATA, un `concatenate`, un `np.add.at`.
  **E il caso che DEVE fallire: un cercatore MENOMATO** *(che guarda solo gli `Assign`)* **deve
  PERDERE quegli scrittori**, e il collaudo deve accorgersene. Senza, il collaudo direbbe
  "trovati tutti" senza poterlo sapere.
ASCII PURO.
"""
import ast
import hashlib
import io
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
SIM = os.path.join(RADICE, "soliton_simulator.py")
DEST = os.path.join(_QUI, "_inventario")
OUT_MD = os.path.join(DEST, "INVENTARIO_SCRITTORI.md")
OUT_CSV = os.path.join(DEST, "INVENTARIO_SCRITTORI.csv")

# LE GRANDEZZE DI STATO FISICO, DICHIARATE. Tutto il resto compare lo stesso, marcato.
FISICHE = {
    "d", "d0", "vd", "peq", "tw", "twp", "phi", "phi0", "phivel", "pos",
    "psi", "_psi_spinor", "_psi_prec", "_psi_spin_prec", "_spinor_lift",
    "_nb", "_nb_prec", "_nb_ret", "omega_s", "mem_mot", "g", "i", "j",
    "perc_chi", "perc_geom", "_rep", "_deg", "rho", "xi", "_cs_nodo_prev",
}


class Cercatore(ast.NodeVisitor):
    """Percorre l'AST tenendo la PILA delle funzioni e degli `if`, cosi' ogni scrittura sa
    **dove** sta e **quale flag** la governa."""

    def __init__(self, menomato=False):
        self.menomato = menomato      # ⚠ la versione che DEVE perdere gli scrittori: collaudo
        self.fn = []
        self.flag = []
        self.trovati = []

    # --- contesto
    def visit_FunctionDef(self, nodo):
        self.fn.append(nodo.name)
        self.generic_visit(nodo)
        self.fn.pop()

    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_If(self, nodo):
        nomi = [x.id for x in ast.walk(nodo.test)
                if isinstance(x, ast.Name) and x.id.isupper() and len(x.id) > 2]
        self.flag.append(nomi[0] if nomi else None)
        self.generic_visit(nodo)
        self.flag.pop()

    # --- le scritture
    def _registra(self, bersaglio, nodo, tipo, valore=None):
        a = bersaglio
        while isinstance(a, (ast.Subscript, ast.Attribute)):
            if isinstance(a, ast.Attribute):
                if isinstance(a.value, ast.Name) and a.value.id == "self":
                    concat = False
                    if valore is not None:
                        concat = any(
                            isinstance(c, ast.Attribute) and c.attr in
                            ("concatenate", "vstack", "hstack", "append", "delete")
                            for c in ast.walk(valore))
                    self.trovati.append({
                        "attributo": a.attr, "riga": nodo.lineno,
                        "funzione": self.fn[-1] if self.fn else "(modulo)",
                        "tipo": ("CONCATENA" if concat else tipo),
                        "flag": next((f for f in reversed(self.flag) if f), "sempre"),
                    })
                    return
                a = a.value
            else:
                a = a.value

    def visit_Assign(self, nodo):
        for t in nodo.targets:
            self._registra(t, nodo, "diretto" if isinstance(t, ast.Attribute) else "per indice",
                           nodo.value)
        self.generic_visit(nodo)

    def visit_AugAssign(self, nodo):
        if not self.menomato:      # ⚠ il cercatore MENOMATO ignora gli aumentati: collaudo `K3`
            self._registra(nodo.target, nodo, "aumentato", nodo.value)
        self.generic_visit(nodo)

    def visit_Call(self, nodo):
        # `np.add.at(self.x, ...)` -- scrittura IN PLACE, e nella riga non c'e' nessun `=`
        if not self.menomato and isinstance(nodo.func, ast.Attribute) and nodo.func.attr == "at":
            if nodo.args:
                self._registra(nodo.args[0], nodo, "in place (add.at)", None)
        self.generic_visit(nodo)


def cerca(sorgente, nome="<sorgente>", menomato=False):
    c = Cercatore(menomato=menomato)
    c.visit(ast.parse(sorgente, nome))
    return c.trovati


# ------------------------------------------------------------------ IL COLLAUDO
SINTETICO = '''
FLAG_UNO = True

class Finta(object):
    def semplice(self):
        self.d0 = 1.0                      # 1 diretto
        self.d[3] = 2.0                    # 2 per indice

    def aumenta(self):
        self.peq += 1.0                    # 3 AUMENTATO (una grep di "=" non lo vede)

    def annidata(self):
        def dentro():
            self.tw[0] += 1.0              # 4 AUMENTATO, per indice, DENTRO UNA ANNIDATA
        dentro()

    def concatena(self):
        self.i = np.concatenate([self.i, a])   # 5 CONCATENA: cambia la LUNGHEZZA

    def inplace(self):
        np.add.at(self.rho, ii, x)         # 6 IN PLACE: nessun "=" nella riga

    def sotto_flag(self):
        if FLAG_UNO:
            self.mem_mot = 0.0             # 7 diretto, GOVERNATO da FLAG_UNO
'''
ATTESI = {"d0", "d", "peq", "tw", "i", "rho", "mem_mot"}


def collaudo(W):
    W("COLLAUDO (`P1-sexies`) su un modulo SINTETICO a scrittori NOTI, PRIMA di inventariare\n")
    W("-" * 100 + "\n")
    e = []
    t = cerca(SINTETICO, "sintetico")
    att = set(x["attributo"] for x in t)
    ok1 = (att == ATTESI)
    W("K1 i SETTE scrittori noti -> attesi %s\n" % sorted(ATTESI))
    W("     trovati %s -> %s\n"
      % (sorted(att), "OK" if ok1 else "*** NE MANCA QUALCUNO: %s ***" % sorted(ATTESI - att)))
    e.append(ok1)

    # i tre NASCOSTI, uno per uno
    per_tipo = dict((x["attributo"], x["tipo"]) for x in t)
    ok2 = per_tipo.get("tw") == "aumentato"
    ok3 = per_tipo.get("i") == "CONCATENA"
    ok4 = per_tipo.get("rho") == "in place (add.at)"
    W("K2 il NASCOSTO 1: aumentato dentro una funzione ANNIDATA -> `tw` = %s -> %s\n"
      % (per_tipo.get("tw"), "OK" if ok2 else "*** PERSO ***"))
    W("K3 il NASCOSTO 2: `concatenate` (cambia la LUNGHEZZA) -> `i` = %s -> %s\n"
      % (per_tipo.get("i"), "OK" if ok3 else "*** PERSO ***"))
    W("K4 il NASCOSTO 3: `np.add.at` (nessun `=` nella riga) -> `rho` = %s -> %s\n"
      % (per_tipo.get("rho"), "OK" if ok4 else "*** PERSO ***"))
    e += [ok2, ok3, ok4]

    # il FLAG
    fl = dict((x["attributo"], x["flag"]) for x in t)
    ok5 = (fl.get("mem_mot") == "FLAG_UNO") and (fl.get("d0") == "sempre")
    W("K5 il FLAG che governa: `mem_mot` -> %s (atteso FLAG_UNO) ; `d0` -> %s (atteso sempre)\n"
      % (fl.get("mem_mot"), fl.get("d0")))
    W("     -> %s\n" % ("OK" if ok5 else "*** il flag non e' attribuito bene ***"))
    e.append(ok5)

    # --- IL CASO CHE DEVE FALLIRE: un cercatore MENOMATO deve PERDERE degli scrittori
    tm = cerca(SINTETICO, "sintetico", menomato=True)
    attm = set(x["attributo"] for x in tm)
    persi = ATTESI - attm
    ok6 = len(persi) >= 2
    W("K6 IL CASO CHE DEVE FALLIRE: un cercatore MENOMATO (solo `Assign`)\n")
    W("     perde %s -> %s\n"
      % (sorted(persi),
         "OK: il collaudo SA distinguere un cercatore che perde pezzi"
         if ok6 else "*** NON DISTINGUE: `K1` direbbe `trovati tutti` senza poterlo sapere ***"))
    e.append(ok6)

    ok = all(e)
    W("-" * 100 + "\n")
    W("  -> il cercatore %s\n\n"
      % ("PASSA: si inventaria" if ok else "*** NON PASSA: NON inventario ***"))
    return ok


def main():
    W = sys.stdout.write
    if not collaudo(W):
        return 1
    try:
        os.makedirs(DEST)
    except OSError:
        pass
    src = io.open(SIM, encoding="utf-8", errors="replace").read()
    blob = hashlib.sha1(open(SIM, "rb").read()).hexdigest()[:8]
    t = cerca(src, SIM)
    t.sort(key=lambda x: (x["attributo"], x["riga"]))

    fis = [x for x in t if x["attributo"] in FISICHE]
    non = [x for x in t if x["attributo"] not in FISICHE]
    conc = [x for x in fis if x["tipo"] == "CONCATENA"]
    attr = sorted(set(x["attributo"] for x in fis))

    with io.open(OUT_CSV, "w", encoding="utf-8", newline="\n") as f:
        f.write("# blob simulatore (sha1 byte grezzi)=%s\n" % blob)
        f.write("attributo,fisico,riga,funzione,tipo,flag\n")
        for x in t:
            f.write("%s,%d,%d,%s,%s,%s\n"
                    % (x["attributo"], 1 if x["attributo"] in FISICHE else 0,
                       x["riga"], x["funzione"], x["tipo"], x["flag"]))

    with io.open(OUT_MD, "w", encoding="utf-8", newline="\n") as f:
        f.write("# INVENTARIO DEGLI SCRITTORI DI STATO — **generato dall'AST**\n\n")
        f.write("> **FASE A del registro della fisica.** Ogni scrittore qui dentro **dovra' "
                "finire in una scheda** di `doc/REGISTRO_FISICA.md`. **Nessuno escluso.**\n>\n")
        f.write("> Generato da `csv/_seal_fork/_inventario_scrittori.py` · simulatore blob "
                "`%s` · **sola lettura**, nessuna esecuzione.\n>\n" % blob)
        f.write("> **⚠ L'esclusione e' VISIBILE, non silenziosa:** cio' che non e' nella "
                "lista dichiarata delle grandezze fisiche compare lo stesso, in fondo, marcato "
                "`non-fisico (dichiarato)`.\n\n")
        f.write("**%d scritture su grandezze FISICHE**, su **%d** attributi distinti · "
                "**%d** sono CONCATENAZIONI *(cambiano la lunghezza: nascite e morti)* · "
                "**%d** scritture su attributi non dichiarati fisici.\n\n"
                % (len(fis), len(attr), len(conc), len(non)))
        f.write("## Le grandezze fisiche, una riga per scrittura\n\n")
        f.write("| grandezza | riga | funzione | tipo | flag |\n|---|--:|---|---|---|\n")
        for x in fis:
            f.write("| `%s` | %d | `%s` | %s | `%s` |\n"
                    % (x["attributo"], x["riga"], x["funzione"],
                       ("**CONCATENA**" if x["tipo"] == "CONCATENA" else x["tipo"]), x["flag"]))
        f.write("\n## Quante scritture per grandezza\n\n| grandezza | scritture | di cui "
                "CONCATENA | funzioni |\n|---|--:|--:|---|\n")
        for a in attr:
            xs = [x for x in fis if x["attributo"] == a]
            fn = sorted(set(x["funzione"] for x in xs))
            f.write("| `%s` | %d | %d | %s |\n"
                    % (a, len(xs), sum(1 for x in xs if x["tipo"] == "CONCATENA"),
                       ", ".join("`%s`" % y for y in fn[:6])))
        f.write("\n## Non dichiarati fisici — **elencati, non nascosti**\n\n")
        f.write("| attributo | scritture | funzioni |\n|---|--:|---|\n")
        for a in sorted(set(x["attributo"] for x in non)):
            xs = [x for x in non if x["attributo"] == a]
            fn = sorted(set(x["funzione"] for x in xs))
            f.write("| `%s` | %d | %s |\n"
                    % (a, len(xs), ", ".join("`%s`" % y for y in fn[:4])))
    W("inventario: %d scritture fisiche su %d attributi (%d concatenazioni), "
      "%d non dichiarate fisiche\n" % (len(fis), len(attr), len(conc), len(non)))
    W("  -> %s\n  -> %s\n" % (os.path.relpath(OUT_MD, RADICE).replace("\\", "/"),
                              os.path.relpath(OUT_CSV, RADICE).replace("\\", "/")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
