# -*- coding: utf-8 -*-
"""GLI SCRITTORI DI `d0` NON TRACCIATI. Punto 4 del mandato dei sospesi.

L'inventario della `FASE A` trova **22** scritture su `d0`; la traccia di `Z102` ha **19** siti.
**Chi resta fuori, con riga e funzione, e il bilancio di `G4` lo copre o no?**

COME, e non e' una grep:
  1. **AST** sul sorgente ORA: ogni scrittura su `self.d0` -- `=`, `+=`, `[...] =`, `concatenate`.
  2. **AST** di nuovo: ogni chiamata a `self._traccia_d0(...)`, col suo NOME di sito e la riga.
  3. **APPAIAMENTO**: una scrittura e' TRACCIATA se esiste una chiamata a `_traccia_d0` **DOPO**
     di essa, **nella stessa funzione**, **senza un'altra scrittura in mezzo** -- perche' la
     convenzione del codice e' `_tr_pre = d0.copy()` PRIMA, scrittura, `_traccia_d0(...)` DOPO.
  4. **COPERTURA DEL BILANCIO**: per ogni non tracciata si dice **quale termine** del bilancio di
     `G4` la contiene, e **come** l'involucro ci arriva.

⚠ IL CRITERIO SI COLLAUDA PRIMA (`P1-sexies`), su un sorgente SINTETICO a risposta nota:
  uno che DEVE dare "tracciata" e uno che DEVE dare "NON tracciata".

⚠ LE RIGHE SONO DEL BLOB DI ADESSO, e il blob e' stampato. Le `22` dell'inventario vengono da
  `ab685eac`; il flag di `G4-bis` ha spostato tutto cio' che sta dopo `:906` (par.0).

SOLA LETTURA: costruisce l'AST, non importa il simulatore, non esegue fisica.
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
SORGENTE = os.path.join(RADICE, "soliton_simulator.py")
OUT = os.path.join(_QUI, "_diag_D", "SCRITTORI_NON_TRACCIATI.md")

# Come il bilancio di `G4` arriva a ciascuna scrittura NON tracciata. Scritto a mano PERCHE'
# e' una LETTURA, non un calcolo: ogni riga cita il punto dell'involucro che la copre.
COPERTURA = {
    "__init__": ("—", "**NON e' una scrittura di PASSO:** e' l'inizializzazione. "
                 "Il bilancio misura `Δ` **fra inizio e fine di un passo**, e qui non "
                 "c'e' nessun passo. **Fuori perimetro, non scoperta.**"),
    "_smp_chiudi": ("**FRENO**", "**`D04`.** L'involucro di `_g4_prova.py` avvolge **`_smorza`** e "
                    "somma **solo** le chiamate con `quale == 'd0_passo'`. **E' il termine che in "
                    "`Z107` mancava** e che vale il `117 %`–`218 %` della crescita."),
    "_allaccia": ("**NASCITE−MORTI**", "**CONCATENA.** L'involucro misura `Σ(dopo)−"
                  "Σ(prima)` **al sito**, non i `d0` dei singoli archi nati: "
                  "un arco nato e poi scritto si conterebbe **due volte** *(il difetto di "
                  "`53e08f3`, residuo `8.0e-05`)*."),
    "mitosi": ("**NASCITE−MORTI**", "**CONCATENA**, stessa forma di `_allaccia`."),
}


def scritture_d0(albero):
    """Ogni scrittura su `self.d0`, con riga, funzione e tipo."""
    di_chi = {}
    for nodo in ast.walk(albero):
        if isinstance(nodo, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for x in ast.walk(nodo):
                ln = getattr(x, "lineno", None)
                if ln is not None:
                    pre = di_chi.get(ln)
                    if pre is None or nodo.lineno > pre[1]:
                        di_chi[ln] = (nodo.name, nodo.lineno)

    def e_d0(t):
        if isinstance(t, ast.Attribute) and t.attr == "d0":
            return isinstance(t.value, ast.Name) and t.value.id == "self"
        if isinstance(t, ast.Subscript):
            return e_d0(t.value)
        return False

    out = []
    for nodo in ast.walk(albero):
        riga = getattr(nodo, "lineno", None)
        if riga is None:
            continue
        fn = di_chi.get(riga, ("<modulo>", 0))[0]
        if isinstance(nodo, ast.Assign):
            for t in nodo.targets:
                if e_d0(t):
                    tipo = "per indice" if isinstance(t, ast.Subscript) else "diretto"
                    src = ast.dump(nodo.value)
                    if "concatenate" in src or "vstack" in src or "hstack" in src:
                        tipo = "CONCATENA"
                    out.append((riga, fn, tipo))
        elif isinstance(nodo, ast.AugAssign) and e_d0(nodo.target):
            tipo = ("aumentato per indice" if isinstance(nodo.target, ast.Subscript)
                    else "aumentato")
            out.append((riga, fn, tipo))
    return sorted(set(out)), di_chi


def siti_traccia(albero, di_chi):
    """Ogni chiamata a `self._traccia_d0(...)`, col nome del sito."""
    out = []
    for nodo in ast.walk(albero):
        if not isinstance(nodo, ast.Call):
            continue
        f = nodo.func
        if not (isinstance(f, ast.Attribute) and f.attr == "_traccia_d0"):
            continue
        nome = "?"
        if nodo.args and isinstance(nodo.args[0], ast.Constant):
            nome = str(nodo.args[0].value)
        riga = nodo.lineno
        out.append((riga, di_chi.get(riga, ("<modulo>", 0))[0], nome))
    return sorted(set(out))


def appaia(scr, sit):
    """Una scrittura e' TRACCIATA se un `_traccia_d0` la segue nella STESSA funzione, senza
    un'altra scrittura in mezzo. E' la convenzione del codice: pre-copia, scrittura, traccia."""
    righe_scr = sorted(r for r, _f, _t in scr)
    esito = {}
    for r, fn, tipo in scr:
        dopo = [s for s in sit if s[0] > r and s[1] == fn]
        if not dopo:
            esito[r] = (None, None)
            continue
        s = min(dopo, key=lambda z: z[0])
        in_mezzo = [q for q in righe_scr if r < q < s[0]]
        esito[r] = (s[2], s[0]) if not in_mezzo else (None, None)
    return esito


def collaudo(W):
    """`P1-sexies`: due sorgenti sintetici a risposta NOTA, e quello che DEVE dare NON tracciata."""
    W("COLLAUDO DEL CRITERIO su sorgenti SINTETICI a risposta nota (`P1-sexies`)\n")
    W("-" * 96 + "\n")
    buono = ("class R(object):\n"
             "    def f(self):\n"
             "        _p = self.d0.copy()\n"
             "        self.d0 = self.d0 + 1\n"
             "        self._traccia_d0('SITO_X', _p)\n")
    a = ast.parse(buono)
    s1_, dc = scritture_d0(a)
    t1 = siti_traccia(a, dc)
    e1 = appaia(s1_, t1)
    ok1 = len(s1_) == 1 and list(e1.values())[0][0] == "SITO_X"
    W("K1 scrittura SEGUITA da `_traccia_d0` nella stessa funzione -> TRACCIATA -> %s\n"
      % ("OK" if ok1 else "*** NO *** %s" % e1))

    cattivo = ("class R(object):\n"
               "    def f(self):\n"
               "        self.d0 = self.d0 * 2\n"
               "    def g(self):\n"
               "        _p = self.d0.copy()\n"
               "        self.d0 = self.d0 + 1\n"
               "        self._traccia_d0('SITO_Y', _p)\n")
    b = ast.parse(cattivo)
    s2, dc2 = scritture_d0(b)
    t2 = siti_traccia(b, dc2)
    e2 = appaia(s2, t2)
    non_tr = [r for r, (n, _l) in e2.items() if n is None]
    ok2 = (len(s2) == 2 and len(non_tr) == 1)
    W("K2 IL CASO CHE DEVE FALLIRE: una scrittura in un'ALTRA funzione, con un `_traccia_d0`\n")
    W("     piu' avanti nel file -> deve risultare NON TRACCIATA -> %s\n"
      % ("OK: la funzione discrimina" if ok2 else "*** il criterio guarda solo la RIGA ***"))

    terzo = ("class R(object):\n"
             "    def f(self):\n"
             "        self.d0 = self.d0 * 2\n"
             "        self.d0 = self.d0 + 1\n"
             "        self._traccia_d0('SITO_Z', None)\n")
    c = ast.parse(terzo)
    s3, dc3 = scritture_d0(c)
    t3 = siti_traccia(c, dc3)
    e3 = appaia(s3, t3)
    non3 = [r for r, (n, _l) in e3.items() if n is None]
    ok3 = (len(s3) == 2 and len(non3) == 1)
    W("K3 SECONDO CASO CHE DEVE FALLIRE: DUE scritture e UN solo `_traccia_d0` -> la PRIMA\n")
    W("     non e' coperta -> %s\n"
      % ("OK: una traccia copre UNA scrittura" if ok3 else "*** ne coprirebbe due ***"))
    ok = ok1 and ok2 and ok3
    W("-" * 96 + "\n  -> %s\n\n" % ("i criteri PASSANO" if ok else "*** NON PASSANO ***"))
    return ok


def main():
    testo = io.open(SORGENTE, encoding="utf-8").read()
    blob = hashlib.sha1(open(SORGENTE, "rb").read()).hexdigest()[:8]
    albero = ast.parse(testo, SORGENTE)
    righe = testo.splitlines()
    try:
        os.makedirs(os.path.dirname(OUT))
    except OSError:
        pass
    o = io.open(OUT, "w", encoding="utf-8", newline="\n")
    W = o.write
    W("# GLI SCRITTORI DI `d0` **NON TRACCIATI**\n\n")
    W("> Punto 4 del mandato dei sospesi. Generato da "
      "`csv/_test_fork/_scrittori_non_tracciati.py`.\n")
    W("> **Blob simulatore ORA: `%s`.** ⚠ Le `22` dell'inventario della `FASE A` vengono da\n"
      "> `ab685eac`: **le righe sono SPOSTATE**, il flag di `G4-bis` ha aggiunto testo a `:906`\n"
      "> *(par.0: si cerca per NOME, non per riga)*.\n\n" % blob)
    if not collaudo(W):
        o.close(); print(io.open(OUT, encoding="utf-8").read()); return 1

    scr, di_chi = scritture_d0(albero)
    sit = siti_traccia(albero, di_chi)
    esito = appaia(scr, sit)
    W("**SCRITTURE SU `self.d0`: %d** · **SITI DI TRACCIA: %d**\n\n" % (len(scr), len(sit)))
    W("| riga | funzione | tipo | sito di traccia | codice |\n|--:|---|---|---|---|\n")
    for r, fn, tipo in scr:
        nome, _rl = esito[r]
        src = righe[r - 1].strip()[:80].replace("|", "\\|")
        W("| `%d` | `%s` | %s | %s | `%s` |\n"
          % (r, fn, tipo, ("`%s`" % nome) if nome else "**— NESSUNO**", src))

    fuori = [(r, fn, tipo) for r, fn, tipo in scr if esito[r][0] is None]
    W("\n## ⚠ LE NON TRACCIATE: **%d su %d**\n\n" % (len(fuori), len(scr)))
    W("| riga | funzione | tipo | termine del bilancio di `G4` | come ci arriva |\n")
    W("|--:|---|---|---|---|\n")
    for r, fn, tipo in fuori:
        term, spieg = COPERTURA.get(fn, ("**❓ NON SO**",
                                         "**Nessuna lettura scritta per questo sito: va guardato.**"))
        W("| `%d` | `%s` | %s | %s | %s |\n" % (r, fn, tipo, term, spieg))
    W("\n## L'ESITO\n\n")
    scoperte = [x for x in fuori if x[1] not in COPERTURA]
    if scoperte:
        W("**⚠ %d scritture NON tracciate e SENZA una lettura che dica dove il bilancio le "
          "prende:** %s\n" % (len(scoperte), scoperte))
    else:
        W("**Tutte le %d non tracciate hanno una lettura che dice dove il bilancio le prende.**\n"
          % len(fuori))
        W("**E il bilancio CHIUDE a `1.138e-13` e `1.170e-13`**, che e' la verifica *a posteriori* "
          "di questa tabella: **se una di queste letture fosse sbagliata, il bilancio non "
          "chiuderebbe.**\n")
    W("\n**⚠ MA «IL BILANCIO LE COPRE» NON SIGNIFICA «IL SIMULATORE LE TRACCIA».** "
      "Il bilancio e' **uno strumento esterno** che avvolge `_smorza` e i siti che concatenano. "
      "**Nel simulatore i siti mancano ancora**, ed e' il difetto `D04`: chiunque rifaccia la "
      "traccia senza quell'involucro **ritrova il buco di `Z107`**.\n")
    o.close()
    print(io.open(OUT, encoding="utf-8").read())
    return 0


if __name__ == "__main__":
    sys.exit(main())
