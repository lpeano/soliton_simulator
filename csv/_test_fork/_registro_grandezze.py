# -*- coding: utf-8 -*-
"""**IL REGISTRO DELLE GRANDEZZE: chi e' per NODO, chi e' per ARCO, e la REGOLA DI NASCITA.**

Serve al **piano** del `CONTROLLO UNICO DELLO SCHEDULATORE` *(decisione di Luca, 2026-09-29)*.

## Due passaggi, e nessuno dei due mi chiede di indovinare

| | |
|---|---|
| **① a RUNTIME** | l'elenco si trova **in automatico** allo stato BASE: `len == n` → **per nodo**, `len == m` → **per arco** *(`m = len(i)`)*. ### **Come nella prova a guasto: la stessa scena, lo stesso passo, cosi' i due elenchi si confrontano** |
| **② dall'AST** | per ogni grandezza **TUTTE** le scritture `self.X = ...`, con la **funzione** che le contiene e l'**espressione**. Quelle dentro **`semina` / `mitosi` / `_allaccia`** sono i **candidati a regola di nascita** |

## La regola di nascita si PROPONE dal codice, non si sceglie

| proposta | da che cosa |
|---|---|
| **estrazione nuova** | l'espressione usa il generatore *(`rng`, `normal`, `uniform`, `standard_`)* |
| **zero / costante** | `zeros(...)` oppure `full(...)` |
| **media** | `mean(`, oppure una semisomma dei due genitori |
| **eredita** | indicizzazione con un indice di genitore *(`[src]`, `[a]`, `[aa]`, `[sel]`, …)* |
| ### **DA DECIDERE** | ### **tutto il resto: lo strumento RIFIUTA di assegnarla** |

> ### 📌 **La classe grave non si assegna a macchina.** E' la lezione di `_classi_ripieghi.py`:
> **quattro** volte una regola automatica ha **nascosto** cio' che cercava. Qui l'espressione e'
> **sempre riportata**, cosi' la proposta e' **verificabile** invece che creduta.
> ### **E una grandezza senza NESSUNA scrittura a un sito di nascita e' un BUCO, non una regola.**

COMANDO:  python csv/_test_fork/_registro_grandezze.py [--passi=30]
USCITA:   0 sempre: e' una SONDA, non un sigillo. Il verdetto lo da' il piano.
"""
import ast
import io
import os
import re
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
FUORI = os.path.join(RADICE, "doc", "REGISTRO_grandezze.md")
SCARTO = os.path.join(RADICE, "csv", "_seal_fork", "_guasto_ripieghi", "_scarto_cli")
# i siti di NASCITA: le funzioni che fanno crescere `n` o `m`. **Verificato dall'AST il
# 2026-09-29:** le tre scritture di `phi` che allungano stanno in `semina` (:3139) e in `mitosi`
# (:6641 la mitosi vera, :6803 il canale di Schwinger, che sta DENTRO `mitosi`).
RADICI_NASCITA = ("semina", "mitosi", "_allaccia")
RIF_NODI, RIF_ARCHI = ("phi",), ("i", "j")


def _t(x):
    return x if isinstance(x, str) else str(x)


# ---------------------------------------------------------------------------------------------
# ① L'ELENCO, A RUNTIME
# ---------------------------------------------------------------------------------------------
def carica(passi):
    import contextlib
    with contextlib.redirect_stdout(io.StringIO()):
        _S0, argv = _cli_flag.argv_del_driver(extra=["--seme=11"], dest=SCARTO)
        S, a = _cli_flag.carica_dal_cli(list(argv), nome="sim_registro")
        S._NMASSE_VIDEO["n"] = max(2, int(getattr(a, "nmasse", 2)))
        S._NMASSE_VIDEO["sep"] = float(getattr(a, "sep", 3.0))
        S._NMASSE_VIDEO["size"] = None
        S.avvia_test("MASSE-COERENTI")()
        net = S.net
        for _ in range(passi):
            _passo.passo_pieno(S, net)
    return S, net


def elenca(net):
    """`(per_nodo, per_arco, ambigue, forme)` allo stato BASE. **Misurato, non elencato a mano.**"""
    n, m = int(net.n), int(len(net.i))
    nodo, arco, ambigue, forme = [], [], [], {}
    for k, v in sorted(vars(net).items()):
        if not isinstance(v, (np.ndarray, list)):
            continue
        try:
            L = len(v)
        except Exception:
            continue
        arr = np.asarray(v) if not isinstance(v, np.ndarray) else v
        forme[k] = (tuple(arr.shape) if arr.ndim else (L,), str(arr.dtype))
        if n == m and L == n:
            ambigue.append(k)
        elif L == n:
            nodo.append(k)
        elif L == m:
            arco.append(k)
    return nodo, arco, ambigue, forme


# ---------------------------------------------------------------------------------------------
# ② LE SCRITTURE, DALL'AST
# ---------------------------------------------------------------------------------------------
def scritture():
    """`{nome: [(riga, funzione, espressione)]}` per ogni `self.X = ...`. **Dal sorgente.**"""
    src = io.open(SIM, encoding="utf-8").read()
    albero = ast.parse(src)
    dentro = {}
    for nodo in ast.walk(albero):
        if isinstance(nodo, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for l in range(nodo.lineno, (nodo.end_lineno or nodo.lineno) + 1):
                # la funzione PIU' INTERNA vince
                if l not in dentro or nodo.lineno > dentro[l][1]:
                    dentro[l] = (nodo.name, nodo.lineno)
    q = {}
    for nodo in ast.walk(albero):
        if not isinstance(nodo, (ast.Assign, ast.AugAssign)):
            continue
        bersagli = nodo.targets if isinstance(nodo, ast.Assign) else [nodo.target]
        for b in bersagli:
            if not (isinstance(b, ast.Attribute) and isinstance(b.value, ast.Name)
                    and b.value.id == "self"):
                continue
            try:
                espr = ast.unparse(nodo.value)
            except Exception:
                espr = "(non stampabile)"
            aug = "" if isinstance(nodo, ast.Assign) else " (AUG +=)"
            q.setdefault(b.attr, []).append(
                (nodo.lineno, dentro.get(nodo.lineno, ("(modulo)", 0))[0], espr + aug))
    return {k: sorted(v) for k, v in q.items()}


def raggiungibili(radici):
    """`{funzione: catena}` delle funzioni **raggiungibili** dalle radici di nascita.

    ### Perche' esiste, ed e' una correzione MISURATA il 2026-09-29
    La prima stesura usava una **lista di nomi** *(`semina`/`mitosi`/`_allaccia`)*, e diceva
    ### **BUCO** per `_cs_nodo_prev`, `psi_spin`, `_psi_spinor`, `_psi_spin_prec`.
    ### **Era FALSO:** l'estensione e' **delegata** a `_eredita_psi_figli` e
    `_eredita_spinore_figli`, che `mitosi` chiama a `:6660` e `:6822`.
    ### ⚠ **Sarebbe stata la SESTA volta che una mia regola basata sul NOME nasconde cio' che
    cerca** -- e qui avrebbe prodotto **falsi BUCHI** nel registro.

    ### ⚠ **IL LIMITE, dichiarato:** il grafo si costruisce **sui NOMI dei metodi chiamati**,
    non sui tipi: due classi con un metodo omonimo verrebbero confuse. Per questo la tabella
    ### **stampa la CATENA**, cosi' ogni voce e' **verificabile** invece che creduta.
    """
    src = io.open(SIM, encoding="utf-8").read()
    albero = ast.parse(src)
    fine, chiama = {}, {}
    for nodo in ast.walk(albero):
        if isinstance(nodo, (ast.FunctionDef, ast.AsyncFunctionDef)):
            fine[nodo.name] = nodo
    for nome, nodo in fine.items():
        s = set()
        for x in ast.walk(nodo):
            if isinstance(x, ast.Call):
                nc = getattr(x.func, "attr", None) or getattr(x.func, "id", None)
                if nc in fine and nc != nome:
                    s.add(nc)
        chiama[nome] = s
    fuori, coda = {}, []
    for r in radici:
        if r in fine:
            fuori[r] = r
            coda.append(r)
    while coda:
        cur = coda.pop(0)
        for succ in sorted(chiama.get(cur, ())):
            if succ not in fuori:
                fuori[succ] = fuori[cur] + " -> " + succ
                coda.append(succ)
    return fuori


def allunga(espr):
    """L'espressione **allunga** la grandezza? `concatenate` / `vstack` / `append` / `tile`."""
    return bool(re.search(r"\b(concatenate|vstack|hstack|append|r_\[)", espr))


def proponi(espr):
    """La **proposta** di regola di nascita. ### **Rifiuta di decidere** quando non e' evidente."""
    if re.search(r"\b(rng|normal|uniform|standard_|random)\b", espr):
        return "estrazione nuova"
    if re.search(r"\b(mean|median)\s*\(", espr) or re.search(r"0\.5\s*\*\s*\(", espr):
        return "media"
    if re.search(r"\b(zeros|full|ones)\s*\(", espr):
        return "zero / costante"
    if re.search(r"\[\s*(src|sel|a|aa|b|bb|ii|jj|par|genitor\w*)\s*\]", espr):
        return "eredita"
    return "### **DA DECIDERE**"


def evento(catena):
    """La **radice** della catena, cioe' **QUALE EVENTO** di nascita.

    ### Perche' serve: <<INCOERENTE>> confondeva DUE EVENTI DIVERSI
    La prima stesura metteva in una sola colonna le regole di `semina` e di `mitosi`, e chiamava
    ### **INCOERENTE** la differenza. ### **Ma la semina crea dal VUOTO e la mitosi divide un
    GENITORE: due regole diverse non sono un'incoerenza, sono DUE EVENTI.**
    ### **Un'incoerenza vera e' due regole diverse per lo STESSO evento**, e solo quella si segnala.
    """
    return catena.split(" -> ")[0]


def principale():
    passi = 30
    for x in sys.argv[1:]:
        if x.startswith("--passi="):
            passi = int(x.split("=", 1)[1])
    S, net = carica(passi)
    n, m = int(net.n), int(len(net.i))
    nodo, arco, ambigue, forme = elenca(net)
    scr = scritture()
    RAGG = raggiungibili(RADICI_NASCITA)
    R = []
    P = R.append

    P("# 📒 **IL REGISTRO DELLE GRANDEZZE: per nodo, per arco, e la regola di nascita**")
    P("")
    P("> ### **Generato da** `csv/_test_fork/_registro_grandezze.py`. **Non si modifica a mano:**")
    P("> si rigira lo strumento. *(`L-NUMERI`.)* ### **Le regole di nascita qui sono PROPOSTE dal")
    P("> codice, non decise:** l'espressione e' sempre riportata, e cio' che non e' evidente resta")
    P("> **DA DECIDERE**.")
    P("")
    P("| | |")
    P("|---|---|")
    P("| scena | `nmasse %d`, `sep %.4f` → **`n = %d`**, **archi `m = %d`**, dopo **%d** passi |"
      % (S._NMASSE_VIDEO["n"], S._NMASSE_VIDEO["sep"], n, m, passi))
    P("| riferimento di `n` | `%s` — ### **`n` E' `len(phi)`** *(property `:2063`)*: non e' un membro"
      " del registro, e' il **metro** |" % ", ".join("`%s`" % x for x in RIF_NODI))
    P("| riferimento di `m` | %s — `len(i) = %d`, `len(j) = %d`%s |"
      % (", ".join("`%s`" % x for x in RIF_ARCHI), len(net.i), len(net.j),
         ", ### **e coincidono**" if len(net.i) == len(net.j) else
         ", ### ⚠ **E NON COINCIDONO**"))
    P("| ### **per NODO** | ### **%d** |" % len(nodo))
    P("| ### **per ARCO** | ### **%d** |" % len(arco))
    P("| ambigue *(`n == m`, indistinguibili)* | %s |"
      % ("### **NESSUNA** — `n = %d` e `m = %d`" % (n, m) if not ambigue
         else "### ⚠ **%d: %s**" % (len(ambigue), ", ".join(ambigue))))
    P("")

    CONTO = {}

    for titolo, elenco, rif in (("PER NODO", nodo, "n"), ("PER ARCO", arco, "m")):
        P("## Le grandezze **%s** (`len == %s`)" % (titolo, rif))
        P("")
        P("| grandezza | forma | tipo | scr. | ### **SEMINA** | ### **MITOSI** *(+Schwinger)* |"
          " ### **`_allaccia`** | senza regola di nascita |")
        P("|---|---|---|---|---|---|---|---|")
        for k in elenco:
            s = scr.get(k, [])
            cresce = [(l, f, e) for (l, f, e) in s if f in RAGG and allunga(e)]
            per_ev = {}
            for l, f, e in cresce:
                per_ev.setdefault(evento(RAGG[f]), []).append((l, f, e))
            col = []
            for ev in RADICI_NASCITA:
                q2 = per_ev.get(ev, [])
                if not q2:
                    col.append("—")
                    continue
                v = sorted({proponi(e) for _l, _f, e in q2})
                testo = (v[0] if len(v) == 1 else
                         "### ⚠ **INCOERENTE NELLO STESSO EVENTO: %s**" % " / ".join(v))
                col.append("%s <br> *%s*" % (testo, ", ".join("`:%d`" % l for l, _f, _e in q2)))
            C = CONTO.setdefault(titolo, {"con_regola": [], "senza_regola": [],
                                          "da_decidere": [], "incoerenti": []})
            C["con_regola" if cresce else "senza_regola"].append(k)
            if any("DA DECIDERE" in x for x in col[:3]):
                C["da_decidere"].append(k)
            if any("INCOERENTE" in x for x in col[:3]):
                C["incoerenti"].append(k)
            if cresce:
                col.append("")
            else:
                col.append("### ⚠ **NESSUNA REGOLA DI NASCITA**: o e' **DERIVATA**"
                           " *(ricalcolata a piena lunghezza ogni passo)*, o e' un **BUCO**."
                           " ### **DA DECIDERE, e si legge A MANO**"
                           + (" *(scritture: %s)*"
                              % ", ".join("`:%d` `%s`" % (l, f) for l, f, _e in s[:4])
                              if s else " *(nessuna scrittura `self.%s =`)*" % k))
            P("| `%s` | `%s` | `%s` | %d | %s |"
              % (k, "×".join(str(x) for x in forme[k][0]), forme[k][1], len(s),
                 " | ".join(col)))
        P("")

    P("## ⚖ Il riepilogo, CONTATO dallo strumento")
    P("")
    P("| | con una REGOLA DI NASCITA | ### **senza** | di cui **DA DECIDERE** |"
      " di cui ### **INCOERENTI** |")
    P("|---|---|---|---|---|")
    for titolo in ("PER NODO", "PER ARCO"):
        C = CONTO.get(titolo, {})
        P("| **%s** | **%d** | ### **%d** | **%d** | %s |"
          % (titolo, len(C.get("con_regola", [])), len(C.get("senza_regola", [])),
             len(C.get("da_decidere", [])),
             ("### **%d**" % len(C.get("incoerenti", [])) if C.get("incoerenti") else "0")))
    P("")
    for titolo in ("PER NODO", "PER ARCO"):
        C = CONTO.get(titolo, {})
        P("**%s — senza regola di nascita (%d):** %s"
          % (titolo, len(C.get("senza_regola", [])),
             ", ".join("`%s`" % x for x in C.get("senza_regola", [])) or "nessuna"))
        P("")
        P("**%s — DA DECIDERE (%d):** %s"
          % (titolo, len(C.get("da_decidere", [])),
             ", ".join("`%s`" % x for x in C.get("da_decidere", [])) or "nessuna"))
        P("")
        P("**%s — INCOERENTI nello stesso evento (%d):** %s"
          % (titolo, len(C.get("incoerenti", [])),
             ", ".join("`%s`" % x for x in C.get("incoerenti", [])) or "nessuna"))
        P("")

    P("## Le espressioni, per chi verifica")
    P("")
    P("**Ogni scrittura in un sito di nascita, con l'espressione INTERA.**")
    P("### **Senza questa tabella la colonna «regola PROPOSTA» sarebbe una cosa da CREDERE.**")
    P("")
    P("| grandezza | riga | funzione | catena dalla nascita | allunga? | espressione |")
    P("|---|---|---|---|---|---|")
    for k in nodo + arco:
        for l, f, e in scr.get(k, []):
            if f not in RAGG:
                continue
            P("| `%s` | `:%d` | `%s` | %s | %s | `%s` |"
              % (k, l, f, RAGG[f] if RAGG[f] != f else "*(radice)*",
                 "### **SI**" if allunga(e) else "no",
                 e.replace("|", "\\|")[:150]))
    P("")
    P("## ⚠ Che cosa questo registro NON dice")
    P("")
    P("| | |")
    P("|---|---|")
    P("| **la proposta non e' la regola** | ### **dove c'e' «DA DECIDERE» decide Luca**, e dove")
    P("  c'e' «INCOERENTE» ce ne sono **due** per la stessa grandezza: per `9-ter` **una delle due")
    P("  e' un difetto, non una seconda legge** |")
    P("| **le scritture FUORI dai siti di nascita** non sono guardate qui | una grandezza puo'")
    P("  essere allungata da una funzione **di servizio** *(e' il caso di `_estendi_psi_spinor`)*:")
    P("  ### **quello e' proprio l'estensore che DISARMA le guardie a valle**, misurato in")
    P("  `f173050` |")
    P("| **il secondo asse** | il controllo `len == n` guarda **il primo asse**. Le forme a due")
    P("  assi sono in tabella, ### **e un presidio su un solo asse va dichiarato** |")
    P("")
    io.open(FUORI, "w", encoding="utf-8", newline=chr(10)).write("\n".join(R) + "\n")
    print("per nodo %d · per arco %d · ambigue %d   (n = %d, m = %d)"
          % (len(nodo), len(arco), len(ambigue), n, m))
    print("funzioni raggiungibili dai siti di nascita: %d" % len(RAGG))
    print("scritto: " + FUORI)
    return 0


if __name__ == "__main__":
    sys.exit(principale())
