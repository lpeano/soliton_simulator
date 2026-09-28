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


def composizione():
    """**LA COMPOSIZIONE DEL PASSO, letta da `PASSO_COMPOSIZIONE` nel simulatore.**

    ### IL CONTRATTO E' CAMBIATO CON `T1` (2026-09-28), e va detto in chiaro
    **Prima** questa funzione leggeva **la SEQUENZA DELLE CINQUE CHIAMATE** dall'AST di
    `update()` e **verificava che il driver coincidesse**. Serviva perche' l'ordine viveva
    **cablato in sei posti**, e una divergenza fra due di loro era invisibile.
    **Da `T1` l'ordine vive in UN POSTO SOLO** -- `PASSO_COMPOSIZIONE` -- e c'e' **un solo
    esecutore**, `esegui_passo`. ### **Quindi non c'e' piu' niente da confrontare fra due
    copie: si legge la lista, e si verifica che il driver PASSI DALL'ESECUTORE.**

    ⚠ **Il vecchio contratto NON e' cancellato:** `_sequenze` e `_metodi_rete` restano qui
    sotto *(decisione 3: cio' che esce si archivia)*, e `soli()` continua a usarli per
    trovare chi avanza con `step()` da solo -- che **resta un difetto** e che `H-P9` cerca.

    **Si legge dal SORGENTE per AST, non importando il modulo:** importare
    `soliton_simulator` lo farebbe girare.
    """
    if "composizione" in _CACHE:
        return _CACHE["composizione"]
    arb = ast.parse(io.open(SIM, encoding="utf-8").read())
    trovata = None
    for n in arb.body:
        if isinstance(n, ast.Assign):
            for b in n.targets:
                if isinstance(b, ast.Name) and b.id == "PASSO_COMPOSIZIONE":
                    trovata = ast.literal_eval(n.value)
    if not trovata:
        raise SystemExit("[passo] `PASSO_COMPOSIZIONE` NON si trova in %s. Non invento un "
                         "fallback: una composizione inventata girerebbe una fisica che "
                         "nessuno ha dichiarato (`A9`)." % SIM)
    # ⚠ IL DRIVER DEVE PASSARE DALL'ESECUTORE. E' cio' che resta del vecchio confronto: non
    #   piu' <<le due sequenze coincidono>>, ma <<il driver non ha una sequenza propria>>.
    td = io.open(DRIVER, encoding="utf-8").read()
    if "esegui_passo" not in td:
        raise SystemExit(
            "[passo] IL DRIVER NON USA `esegui_passo`: %s -- con T1 l'ordine del passo "
            "vive in PASSO_COMPOSIZIONE e c'e' UN SOLO esecutore. Un driver che avanza "
            "per conto suo fa girare una fisica DIVERSA da quella delle sonde, ed e' "
            "il difetto che questo modulo esiste per impedire." % DRIVER)
    _CACHE["composizione"] = list(trovata)
    return _CACHE["composizione"]


def ordine():
    """**COMPATIBILITA'**: le sole LEGGI della composizione, come `(tipo, nome)`.

    Serve agli strumenti scritti prima di `T1`, che chiedevano `ordine()` e si aspettavano
    coppie `(tipo, nome)`. **Le fasi dello schedulatore (`apri`, `chiudi`,
    `verifica_invarianti`) NON sono leggi e non compaiono**: chi vuole la composizione
    INTERA usa `composizione()`.
    """
    if "ordine" in _CACHE:
        return _CACHE["ordine"]
    metodi = _metodi_rete()
    fasi = {"apri", "chiudi", "verifica_invarianti"}
    seq = [("metodo" if n in metodi else "modulo", n)
           for n in composizione() if n not in fasi]
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
    """UN PASSO. **L'UNICO modo di avanzare in una sonda**, e da `T1` e' un INVOLUCRO.

    ### Non ricopia piu' niente: chiama `S.esegui_passo(net)`.
    Prima ricostruiva il passo iterando la sequenza letta dall'AST -- il che era giusto
    quando l'ordine viveva in sei posti, **ma era il settimo posto in cui viveva**.
    `composizione()` si chiama comunque, perche' **verifica che il driver passi
    dall'esecutore**: se non lo fa, si solleva qui invece di far girare due fisiche.
    """
    composizione()          # il controllo del contratto: solleva se il driver va per conto suo
    _ese = getattr(S, "esegui_passo", None)
    if _ese is not None:
        return _ese(net)
    # ------------------------------------------------------------------ FALLBACK PRE-`T1`
    # ⚠ SERVE A UNA COSA SOLA, e va detta: far avanzare un BLOB STORICO ESTRATTO che
    #   `esegui_passo` NON CE L'HA, perche' precede `T1`. Senza questo, **nessun sigillo puo'
    #   piu' confrontarsi con un blob pre-`T1`** -- e il confronto col codice di prima e' la
    #   cosa che `H-P8` esiste per proteggere.
    # ### NON INDEBOLISCE `H-P9`: scatta SOLO quando l'esecutore NON ESISTE, cosa che per il
    #   simulatore sul disco non puo' succedere. Per il codice di oggi il ramo e' MORTO, e chi
    #   volesse saltare l'esecutore lo troverebbe comunque li'.
    # ### E NON REINVENTA L'ORDINE: usa `ordine()`, che legge `PASSO_COMPOSIZIONE`. Le cinque
    #   LEGGI sono le stesse prima e dopo `T1` -- `T1` ha aggiunto le FASI (`apri`, `chiudi`,
    #   `verifica_invarianti`), che un blob pre-`T1` non ha e che `ordine()` non restituisce.
    _pre = getattr(S, "_g_passo_pieno_pre_t1", 0)
    S._g_passo_pieno_pre_t1 = _pre + 1
    for _tipo, _nome in ordine():
        if _tipo == "modulo":
            getattr(S, _nome)(net)
        else:
            getattr(net, _nome)()
    return None


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
