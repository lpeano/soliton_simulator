# -*- coding: utf-8 -*-
"""**IL PASSO COMPLETO, LETTO DAL CODICE CHE GIRA** -- non ricopiato.

> **Decisione di Luca, 2026-09-25:** *«`passo_pieno(S, net)` diventa l'UNICO modo di avanzare
> nelle sonde: mettilo in un modulo condiviso e leggi l'ordine delle `5` chiamate DAL DRIVER,
> non ricopiato.»*

**PERCHÉ ESISTE, ed è un difetto misurato:** le sonde chiamavano **solo `net.step()`**, e così
mancavano **la MITOSI**, il **FRENO su `d0`** *(dentro `memoria_hebbiana_moto`)*, la **GRAVITÀ di
oggi** *(idem)* e lo **SCUOTIMENTO del vuoto**. **Con il solo `step()` il freno non si chiude mai**,
e la rimisura di `|dx|/d` non raccoglieva **nessun campione**.

**COME LO LEGGE, e non lo ricopia:** si fa il **parsing AST** del sorgente e si cerca la riga
che contiene `net.step()` **dentro una sequenza di chiamate**; l'ordine restituito è quello che
sta **nel file**. Se il file cambia, **questo modulo cambia con lui**.

**⚠ E SI LEGGE DA DUE POSTI, perché uno è UNA COPIA:** il driver
*(`csv/_test_fork/_scena_video.py`)* dichiara nel proprio docstring *«Il ciclo per frame e'
COPIATO da `update()`»*. **Quindi si legge l'ORIGINALE** *(`update()` nel simulatore)* **e IL
DRIVER, e si VERIFICA che coincidano.** Se divergono, `passo_pieno` **RIFIUTA DI GIRARE**: due
sequenze diverse significano che le sonde e la campagna avanzano in modo diverso, ed è esattamente
il difetto che questo modulo deve impedire.

**⚠ E C'È UNA SESTA CHIAMATA CHE NON STA NEL PASSO:** `passo_test()`, **una volta per FRAME**
*(`PASSI_PER_FRAME = 6` passi per frame)*. **NON è parte del passo** e `passo_pieno` non la fa;
chi vuole i frame usa `frame_pieno`. **Va detto**, perché un passo di sonda e un frame di driver
**non sono la stessa cosa**.

**Nessun fallback silenzioso:** se la sequenza non si trova, si solleva. Un `passo_pieno` che
ricadesse su `step()` da solo **rifarebbe il difetto in silenzio** *(`A9`)*.
"""
import ast
import io
import os

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, ".."))
SIM = os.path.join(RADICE, "soliton_simulator.py")
DRIVER = os.path.join(RADICE, "csv", "_test_fork", "_scena_video.py")

_CACHE = {}


def _metodi_rete():
    """I nomi dei metodi della classe `Rete`, letti dal sorgente."""
    if "metodi" in _CACHE:
        return _CACHE["metodi"]
    m = set()
    for n in ast.walk(ast.parse(io.open(SIM, encoding="utf-8").read())):
        if isinstance(n, ast.ClassDef) and n.name == "Rete":
            for k in n.body:
                if isinstance(k, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    m.add(k.name)
    _CACHE["metodi"] = m
    return m


def _sequenze(percorso):
    """Le sequenze di chiamate che contengono `.step()`, come liste di (tipo, nome).

    ⚠ SI VA SUI **BLOCCHI CONTIGUI DI STATEMENT**, non sulle righe: la prima stesura
    raggruppava per numero di riga e produceva **sequenze PARZIALI** *(cinque «sequenze diverse»
    nel simulatore, tutte sottoinsiemi della stessa)*. **Un raggruppamento sbagliato non dà un
    errore: dà un ordine sbagliato**, ed è il difetto che questo modulo deve impedire.

    Un blocco è una **successione MASSIMALE** di statement che sono **soltanto chiamate**
    *(`Expr(Call)`)*, dentro lo stesso corpo. Così `scuoti_vuoto(net); net.step(); ...` scritto
    su una riga o su due dà **lo stesso blocco**, e nulla di più corto.

    `tipo` è `"metodo"` se il nome è un metodo della classe `Rete`, `"modulo"` altrimenti. Il
    RICEVITORE non conta *(`S.net` nel driver, `net` in `update()`)*: contano **nome e ordine**.
    """
    src = io.open(percorso, encoding="utf-8").read()
    arb = ast.parse(src)
    metodi = _metodi_rete()
    trovate = []

    def _nome(st):
        if not isinstance(st, ast.Expr) or not isinstance(st.value, ast.Call):
            return None
        f = st.value.func
        if isinstance(f, ast.Attribute):
            return f.attr
        if isinstance(f, ast.Name):
            return f.id
        return None

    def _scorri(corpo):
        k = 0
        while k < len(corpo):
            nm = _nome(corpo[k])
            if nm is None:
                k += 1
                continue
            blocco = []
            riga = corpo[k].lineno
            while k < len(corpo):
                nm = _nome(corpo[k])
                if nm is None:
                    break
                blocco.append(nm)
                k += 1
            if any(x == "step" for x in blocco):
                trovate.append((riga, [("metodo" if x in metodi else "modulo", x)
                                       for x in blocco]))

    for n in ast.walk(arb):
        for campo in ("body", "orelse", "finalbody"):
            c = getattr(n, campo, None)
            if isinstance(c, list) and c and isinstance(c[0], ast.stmt):
                _scorri(c)
    return trovate


def ordine():
    """L'ORDINE DEL PASSO, letto dall'ORIGINALE (`update()`) e VERIFICATO contro il driver."""
    if "ordine" in _CACHE:
        return _CACHE["ordine"]
    # ⚠ UNA CHIAMATA SOLA NON E' UNA SEQUENZA: non porta nessuna informazione di ORDINE.
    #   Si tengono i blocchi con >= 2 chiamate. **Non e' una scelta fra sequenze diverse**: e'
    #   il criterio che dice che cosa sia una sequenza.
    #   E I BLOCCHI DA UNA SOLA CHIAMATA SI RESTITUISCONO COMUNQUE, come RISCONTRO (vedi
    #   `soli()`): nel simulatore sono DUE, e uno dei due e' un difetto vero.
    s_sim = [x for x in _sequenze(SIM) if len(x[1]) >= 2]
    s_drv = [x for x in _sequenze(DRIVER) if len(x[1]) >= 2]
    if not s_sim:
        raise SystemExit("[passo] la sequenza del passo NON si trova in %s. Non invento un "
                         "fallback: un `passo_pieno` che ricadesse su `step()` da solo "
                         "rifarebbe il difetto in silenzio (`A9`)." % SIM)
    # nel simulatore la sequenza compare piu' volte (interattivo e headless): devono coincidere
    uniche = {tuple(x[1]) for x in s_sim}
    if len(uniche) != 1:
        raise SystemExit("[passo] il SIMULATORE ha %d sequenze DIVERSE del passo:\n  %s\n"
                         "  Non scelgo io quale sia il passo." % (len(uniche), uniche))
    seq = list(next(iter(uniche)))
    if s_drv:
        uniche_d = {tuple(x[1]) for x in s_drv}
        if uniche_d != uniche:
            raise SystemExit(
                "[passo] IL DRIVER E L'ORIGINALE HANNO SEQUENZE DIVERSE.\n"
                "  originale (`update()`): %s\n"
                "  driver:                 %s\n"
                "  Il docstring del driver dice che il ciclo e' COPIATO da `update()`: se non\n"
                "  coincidono, le sonde e la campagna avanzano in modo DIVERSO, ed e'\n"
                "  esattamente il difetto che questo modulo deve impedire." % (uniche, uniche_d))
    _CACHE["ordine"] = seq
    return seq


def soli(percorso=None):
    """I siti che avanzano con `step()` **da solo**, cioè senza le altre chiamate del passo.

    **Nel SIMULATORE sono due, e vanno letti diversamente:**

    * **`:6846`** — è **la sequenza COMPLETA**, interrotta dalle assegnazioni del cronometro
      *(`t0 = _t.time(); net.step(); acc[...] += ...`)*. **È un limite del mio parser, non un
      difetto del codice**, e il commento di quella riga lo dice: *«CICLO COMPLETO identico al
      runtime (update): stessa fisica, stesse leggi, stesso ordine»*.
    * **`:8404`** — **È UN DIFETTO VERO, E STA NEL SIMULATORE:**
      `for _ in range(300): net.step()` nel percorso di ricostruzione con `--seed`/`--nodi`,
      seguito da `net.rilassa_disegno(30)`. **Trecento passi senza mitosi, senza scuotimento e
      senza memoria del moto**, per «invecchiare» la rete. **È lo stesso difetto delle sonde,
      dentro il codice che le sonde imitano.** → va in coda.

    **Il criterio per distinguerli è dichiarato: si guarda se nello STESSO corpo, entro poche
    righe, compaiono anche gli altri nomi del passo.** Se sì, è una sequenza spezzata; se no,
    è un avanzamento incompleto.
    """
    perc = percorso or SIM
    seq = _sequenze(perc)
    nomi_passo = {n for _, n in ordine()}
    src = io.open(perc, encoding="utf-8").read().split(chr(10))
    out = []
    for riga, blocco in seq:
        if len(blocco) >= 2:
            continue
        # finestra di 8 righe attorno: se ci sono gli altri nomi, e' una sequenza SPEZZATA
        a0, b0 = max(0, riga - 5), min(len(src), riga + 4)
        vicino = chr(10).join(src[a0:b0])
        altri = {n for n in nomi_passo if n != "step" and (n + "(") in vicino}
        out.append(dict(riga=riga, altri_vicini=sorted(altri),
                        spezzata=bool(len(altri) >= len(nomi_passo) - 2),
                        testo=src[riga - 1].strip()[:100]))
    return out


def passo_pieno(S, net):
    """UN PASSO, nell'ordine letto dal codice. **L'UNICO modo di avanzare in una sonda.**"""
    for tipo, nome in ordine():
        if tipo == "metodo":
            getattr(net, nome)()
        else:
            getattr(S, nome)(net)


def frame_pieno(S, net, passi=None):
    """UN FRAME: `passo_test()` UNA VOLTA, poi `PASSI_PER_FRAME` passi pieni.

    **Va usato solo da chi vuole riprodurre il driver frame per frame.** Una sonda che misura
    per PASSO usa `passo_pieno`, e **la differenza va dichiarata**: `passo_test` gira una volta
    ogni `PASSI_PER_FRAME` passi, non a ogni passo.
    """
    if hasattr(S, "passo_test"):
        S.passo_test()
    n = int(passi if passi is not None else getattr(S, "PASSI_PER_FRAME", 6))
    for _ in range(max(1, n)):
        passo_pieno(S, net)


def descrivi():
    """La riga da stampare in un referto: l'ordine, e da dove viene."""
    seq = ordine()
    return ("passo = " + " -> ".join("%s()" % nome for _, nome in seq)
            + "   (letto per AST da `update()` e verificato contro il driver)")
