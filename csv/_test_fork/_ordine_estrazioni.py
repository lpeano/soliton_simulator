# -*- coding: utf-8 -*-
"""**L'ORDINE DELLE ESTRAZIONI CASUALI E DELLE SOMME NELLA NASCITA.**

**Passo 1 del `COMMIT 3` del riordino** *(`doc/PIANO_riordino_mitosi.md`, parte (c))*, e si gira
### **PRIMA di una riga di codice.** Il piano dichiara il rischio:

> ### **spostare le scritture della nascita in un punto solo puo' cambiare l'ORDINE DELLE
> ### ESTRAZIONI CASUALI e l'ordine delle SOMME in virgola mobile. E il generatore e' UNO
> ### (`net.rng`): chi pesca prima cambia cio' che pescano tutti gli altri.**

### ➜ **Quindi l'ordine diventa parte del CONTRATTO**, scritto in `doc/REGOLE_nascita.tsv`.

---

## LE DUE MISURE, e sono di natura DIVERSA

| | che cosa misura | **con quale strumento, e perche' quello** |
|---|---|---|
| ### **(A) le ESTRAZIONI** | chi pesca da `net.rng`, **in che ordine**, **quante volte**, e **in quale VOCE** | ### **IL RUNTIME.** `net.rng` si avvolge con un oggetto che **inoltra e registra**. ### ⛔ **NON l'AST:** l'AST vede `rng.random(...)` in **nove** posti e ### **non sa quali rami girano** -- `ANTIFASE_ADD` e `COPPIA_DENSITA` sono flag, e un conteggio statico direbbe nove dove il runtime dice uno o due |
| ### **(B) l'ordine degli ADDENDI** | quali scritture della nascita sono **somme** o **concatenazioni di piu' pezzi**, e **in che ordine** stanno gli addendi | ### **L'AST, E QUI E' LO STRUMENTO GIUSTO.** L'ordine degli addendi di `a + b` ### **E' un fatto della sintassi**: non c'e' un runtime che lo possa dire meglio. ### **Dichiarare quale strumento vale per quale domanda e' il punto** -- la forma dell'errore che in questa sessione si e' ripetuta sei volte e' proprio **usare la sintassi per rispondere a una domanda di runtime** |

## ✅ IL CONTROLLO CHE RENDE LA MISURA (A) VALIDA

### **Lo stesso passo CON e SENZA la spia deve essere byte-identico.** Se non lo e', la spia
**consuma il generatore** o ne cambia lo stato, e ### **la misura misura la spia.**
*(E' lo stesso controllo di `_ordine_letture.py`, che il 2026-09-29 ha dato byte-identico su
**1 887 282** eventi intercettati. Qui la spia e' molto piu' leggera: avvolge **un** oggetto.)*

### ⚠ **E LA SPIA INOLTRA, NON REIMPLEMENTA:** ogni chiamata arriva al `Generator` vero, con gli
stessi argomenti e nello stesso ordine. ### **Lo stream non si tocca** -- si annota.

## ⚠ CHE COSA QUESTO STRUMENTO **NON** FA

* ### **non decide se il byte-identico del commit 3 passera'.** Dice ### **qual e' l'ordine da
  RISPETTARE**: e' il contratto, non la verifica;
* ### **non copre i rami spenti.** Se un flag cambia, l'ordine cambia -- e per questo il referto
  porta ### **la configurazione INTERA** (`H-P5`) e non solo i numeri;
* ### **non misura le estrazioni fuori dal passo** *(la `semina`, che gira alla costruzione della
  scena)*: la (A) le riporta **a parte**, da un conteggio sul passo zero.

## ⛔ **DUE DIFETTI DELLA PRIMA STESURA (`99bc86dc`), trovati dal GIRO CORTO** *(`STANDARD 7`)*

| | il difetto | la cura |
|---|---|---|
| ### **① un FALSO ZERO sulla semina** | la prima stesura metteva la spia **sottoclassando `S.Rete`** *(dopo `carica_dal_cli`)*, e riportava ### **«estrazioni della semina: 0»** -- un numero **falso**, non un errore. ### **La causa, verificata e non supposta:** `_applica_flag` crea la `Rete` *(`:9830`)* e chiama `net.semina(...)` *(`:9847`)* ### **DENTRO `carica_dal_cli`**, cioe' **prima** che una sottoclasse possa esistere | si avvolge ### **`np.random.default_rng`** *(l'**unico** punto in cui il file costruisce un generatore: `:2564`)* **prima** del caricamento, e si ripristina dopo. ### **Cosi' la spia c'e' dal primo numero pescato** |
| ### **② l'ordine degli addendi NON conta sui CONTATORI** | la (B) elencava **82** scritture, e fra loro ### **`getattr(self, '_g_nati_mitosi', 0) + int(len(a))`**: una somma di **INTERI**, dove ### **l'ordine degli addendi NON cambia il risultato.** Metterle nel contratto lo ### **diluisce**: il contratto deve dire dove l'ordine **conta** | ogni riga porta ### **se la grandezza e' nel REGISTRO** e ### **se la somma e' in VIRGOLA MOBILE.** ### **Il CONTRATTO e' il sottoinsieme in virgola mobile**; gli interi si riportano **separati e dichiarati inerti** |

## ⛔ **E UN TERZO DIFETTO, trovato GUARDANDO IL REFERTO DEL GIRO VERO**

> ### **La cura ② confondeva DUE cose, e ha prodotto una riga FALSA: `i` e `j` finivano sotto
> ### «l'ordine NON conta».**

### **Per `np.concatenate([self.i[keep], a, m])` l'ordine decide LA TOPOLOGIA.** Non e' una
questione di ultimo bit: e' ### **quale valore va a quale indice**, cioe' **il significato.**
### ➜ **Le due cose, separate:**

| forma | quando l'ordine conta | perche' |
|---|---|---|
| ### **CONCATENAZIONE** | ### **SEMPRE, per qualunque tipo** | decide ### **quale valore va a quale INDICE.** Una permutazione qui ### **non sposta un bit: cambia il sistema** |
| ### **SOMMA aritmetica** | ### **solo in VIRGOLA MOBILE** | cambia ### **l'ULTIMO BIT.** Sugli interi *(i contatori)* e' **inerte** |

### 📌 **E l'ho visto nel mio stesso output, non da un presidio.** La riga diceva
*«`i` [None] `self.i[keep] | a | m` -- l'ordine NON conta»*, ### **ed e' la topologia del grafo.**
### **Il tipo `None` veniva dal fatto che `i` e' un METRO, e `REGISTRO_METRI` non dichiara un
tipo**: il mio codice leggeva *«tipo assente»* e concludeva *«non in virgola mobile»*, quindi
*«inerte»*. ### **Due passaggi leciti, una conclusione falsa.**

### 📌 **E il ① e' il difetto peggiore dei due, perche' non fallisce: RISPONDE.**
Uno zero falso in un referto ### **si legge come un fatto** -- *«la semina non pesca»* -- e
avrebbe mandato il contratto a dire il contrario di cio' che succede. ### **E' la stessa famiglia
dello `0` del primo run sul `--regime`** *(2026-10-01: «zero differenze» perche' lo strumento non
aveva creato il secondo sistema)*. ### **Un numero che non torna si guarda; uno che torna si
crede.**

COMANDO:  python csv/_test_fork/_ordine_estrazioni.py [--da=40] [--fino=72] [--seme=11]
USCITA:   `csv/_test_fork/_ordine_estrazioni/_ordine_estrazioni.json` + `_corsa.txt` + stdout.
ASCII puro nel codice; il docstring e' utf-8 e `_presidio` riconfigura lo stdout.
"""
import ast
import contextlib
import copy
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
import numpy as np  # noqa: E402
import _cli_flag  # noqa: E402
import _passo  # noqa: E402

FUORI = os.path.join(RADICE, "csv", "_test_fork", "_ordine_estrazioni")
SIM = os.path.join(RADICE, "soliton_simulator.py")
NL = chr(10)

# I METODI DI ESTRAZIONE che si registrano. ### Si parte da cio' che il file USA (misurato col
#   conteggio delle occorrenze di `rng.<metodo>`), e si aggiunge tutto cio' che un `Generator`
#   offre e che CONSUMA lo stream: un metodo non elencato passerebbe INOSSERVATO, ed e' il buco
#   che questa riga chiude. `bit_generator` NON e' un'estrazione: e' lo stato, e si inoltra.
PESCA = ("random", "normal", "choice", "integers", "uniform", "standard_normal", "poisson",
         "exponential", "permutation", "shuffle", "binomial", "gamma", "beta", "bytes",
         "multivariate_normal", "standard_exponential", "random_sample", "randint", "rand",
         "randn", "spawn")


class RngSpiato(object):
    """Avvolge un `Generator` e REGISTRA le estrazioni. Inoltra tutto il resto.

    Non reimplementa niente: ogni chiamata va al generatore vero con gli stessi argomenti.
    `bit_generator` si inoltra, perche' `salva_stato`/`ripristina_stato` ne leggono lo stato e
    una copia romperebbe la ripresa.
    """

    def __init__(self, vero, registro, dove):
        object.__setattr__(self, "_vero", vero)
        object.__setattr__(self, "_registro", registro)
        object.__setattr__(self, "_dove", dove)

    def __getattr__(self, nome):
        v = getattr(object.__getattribute__(self, "_vero"), nome)
        if nome not in PESCA:
            return v
        reg = object.__getattribute__(self, "_registro")
        dove = object.__getattribute__(self, "_dove")

        def avvolto(*a, **k):
            r = v(*a, **k)
            reg.append({"ordine": len(reg) + 1,
                        "passo": int(dove.get("passo", -1)),
                        "voce": dove.get("voce"),
                        "metodo": nome,
                        "args": [_breve(x) for x in a],
                        "size": _breve(k.get("size")) if "size" in k else None,
                        "quanti": int(np.size(r)) if hasattr(r, "__len__")
                                  or isinstance(r, np.ndarray) else 1})
            return r
        return avvolto

    def __setattr__(self, nome, valore):
        setattr(object.__getattribute__(self, "_vero"), nome, valore)


def _breve(x):
    """Un argomento in forma leggibile e SERIALIZZABILE: mai l'array, solo la sua taglia."""
    if x is None:
        return None
    if isinstance(x, (int, float, bool, str)):
        return x
    if isinstance(x, tuple):
        return list(x)
    try:
        return "<%s len=%d>" % (type(x).__name__, len(x))
    except Exception:
        return "<%s>" % type(x).__name__


def blob(percorso):
    return hashlib.sha1(io.open(percorso, "rb").read()).hexdigest()


def carica(nome, seme, passi):
    with contextlib.redirect_stdout(io.StringIO()):
        _S0, argv = _cli_flag.argv_del_driver(extra=["--seme=%d" % seme],
                                              dest=os.path.join(FUORI, "_scarto_cli"))
        S, a = _cli_flag.carica_dal_cli(list(argv), nome=nome)
        S._applica_regime(a)
        S._NMASSE_VIDEO["n"] = max(2, int(getattr(a, "nmasse", 2)))
        S._NMASSE_VIDEO["sep"] = float(getattr(a, "sep", 3.0))
        S._NMASSE_VIDEO["size"] = None
        S.avvia_test("MASSE-COERENTI")()
        net = S.net
        for _ in range(passi):
            _passo.passo_pieno(S, net)
    return S, net


def foto(S, net):
    """La fotografia delle grandezze DICHIARATE: nomi dal registro, non scelti a mano."""
    q = {}
    for k in sorted(getattr(S, "REGISTRO_NOMI", ())):
        v = getattr(net, k, None)
        if v is None:
            continue
        try:
            q[k] = np.array(v, copy=True)
        except Exception:
            pass
    # i CONTATORI: ogni attributo intero che comincia con `_`. Un contatore che cambia di uno
    #   e' un difetto che le grandezze non vedrebbero (decisione di Luca, 2026-09-29).
    for k, v in vars(net).items():
        if k.startswith("_") and isinstance(v, (int, np.integer)) and not isinstance(v, bool):
            q["CONT:" + k] = int(v)
    return q


def identiche(a, b):
    """`(uguali, elenco_differenze)`. I non finiti si confrontano come ELEMENTI (par. 2026-10-01)."""
    diff = []
    for k in sorted(set(a) | set(b)):
        if k not in a or k not in b:
            diff.append("%s: presente in UNO solo" % k)
            continue
        x, y = a[k], b[k]
        if isinstance(x, int) and isinstance(y, int):
            if x != y:
                diff.append("%s: %d contro %d" % (k, x, y))
            continue
        x, y = np.asarray(x), np.asarray(y)
        if x.shape != y.shape:
            diff.append("%s: forma %s contro %s" % (k, x.shape, y.shape))
            continue
        with np.errstate(all="ignore"):
            try:
                ok = bool(np.array_equal(x, y, equal_nan=True))
            except TypeError:
                ok = bool(np.array_equal(x, y))
        if not ok:
            diff.append("%s: DIVERSA" % k)
    return (not diff), diff


# ------------------------------------------------------------------- (B) l'ordine degli addendi
def somme_della_nascita(percorso, funzioni, nomi_registro, tipi_registro):
    """Le scritture della nascita che DIPENDONO DALL'ORDINE DEGLI ADDENDI, dall'AST.

    Due forme contano, e per la stessa ragione (la virgola mobile non e' associativa):
      * una SOMMA di due o piu' addendi -- `0.5 * (x[a] + x[b])`;
      * una CONCATENAZIONE di due o piu' pezzi -- `np.concatenate([q[keep], dh, dh])`.
    Si riporta il nome scritto, la riga di OGGI, la forma e gli addendi NELL'ORDINE DEL SORGENTE.
    """
    src = io.open(percorso, encoding="utf-8").read()
    t = ast.parse(src)
    righe = src.split(NL)
    fuori = []

    def nome_mira(m):
        if isinstance(m, ast.Attribute) and isinstance(m.value, ast.Name) and m.value.id == "self":
            return m.attr
        if isinstance(m, ast.Subscript):
            return nome_mira(m.value)
        return None

    def addendi(e):
        """Gli addendi di una somma, in ordine, appiattendo gli `+` annidati a sinistra."""
        if isinstance(e, ast.BinOp) and isinstance(e.op, ast.Add):
            return addendi(e.left) + addendi(e.right)
        return [e]

    def somme_annidate(e):
        """TUTTE le somme aritmetiche dentro `e`, anche dentro i pezzi di una concatenazione.

        ⚠ LA PRIMA STESURA GUARDAVA SOLO LA FORMA PIU' ESTERNA, e ha prodotto il quarto falso
        zero: *<<0 somme in virgola mobile>>* mentre `psi` del nato e'
        `concatenate([cur[:n0], 0.5 * (cur[a] + cur[b])])` -- la somma c'e', ANNIDATA.
        """
        fuori = []

        def scendi(x):
            if isinstance(x, ast.BinOp) and isinstance(x.op, ast.Add):
                ad = addendi(x)
                fuori.append({"quanti": len(ad), "addendi": [ast.unparse(p) for p in ad],
                              "testo": ast.unparse(x)[:120]})
                # NON si scende dentro gli addendi di questa catena: li conterei due volte.
                # Si scende solo dentro cio' che NON e' parte della catena (gli argomenti).
                for p in ad:
                    for f in ast.iter_child_nodes(p):
                        scendi(f)
                return
            for f in ast.iter_child_nodes(x):
                scendi(f)
        scendi(e)
        return fuori

    def pezzi_concat(e):
        if (isinstance(e, ast.Call) and isinstance(e.func, ast.Attribute)
                and e.func.attr in ("concatenate", "vstack", "hstack", "stack")
                and e.args and isinstance(e.args[0], (ast.List, ast.Tuple))):
            return e.func.attr, list(e.args[0].elts)
        return None, None

    for nodo in ast.walk(t):
        if not (isinstance(nodo, ast.FunctionDef) and nodo.name in funzioni):
            continue
        for x in ast.walk(nodo):
            if not isinstance(x, (ast.Assign, ast.AugAssign)):
                continue
            mire = x.targets if isinstance(x, ast.Assign) else [x.target]
            nomi = [nome_mira(m) for m in mire]
            nomi = [q for q in nomi if q]
            if not nomi:
                continue
            e = x.value
            # si scende dentro i moltiplicatori: `0.5 * (a + b)`
            cand = [e]
            if isinstance(e, ast.BinOp) and isinstance(e.op, ast.Mult):
                cand += [e.left, e.right]
            vista = None
            for c in cand:
                k, pz = pezzi_concat(c)
                if pz is not None and len(pz) >= 2:
                    vista = (k, [ast.unparse(p) for p in pz])
                    break
                ad = addendi(c)
                if len(ad) >= 2:
                    vista = ("somma", [ast.unparse(p) for p in ad])
                    break
            if vista is None:
                continue
            g = nomi[0]
            tp = tipi_registro.get(g)
            # ⚠ ⚠ DUE COSE DIVERSE, E LA PRIMA STESURA LE CONFONDEVA (difetto trovato
            #   GUARDANDO IL PROPRIO OUTPUT: `i` e `j` finivano sotto <<l'ordine NON conta>>,
            #   ed e' FALSO -- l'ordine di `concatenate([i[keep], a, m])` decide LA TOPOLOGIA).
            #     * CONCATENAZIONE: l'ordine decide QUALE VALORE VA A QUALE INDICE. Conta
            #       SEMPRE, per QUALUNQUE tipo: non e' una questione di ultimo bit, e' il
            #       significato. Una permutazione qui non sposta un bit: cambia il sistema.
            #     * SOMMA ARITMETICA: l'ordine degli addendi cambia l'ULTIMO BIT, e solo in
            #       VIRGOLA MOBILE. `getattr(self, '_g_x', 0) + 1` e' intera: inerte.
            #   Il tipo viene dal REGISTRO, non da un'euristica sul nome. I METRI (`phi`, `i`,
            #   `j`) nel registro NON hanno un tipo dichiarato: si marca `None` e NON si assume.
            if vista[0] == "somma":
                mobile = None
                if g in nomi_registro:
                    mobile = bool(tp is not None
                                  and ("float" in str(tp) or "complex" in str(tp)))
                perche = ("somma in VIRGOLA MOBILE: l'ultimo bit dipende dall'ordine"
                          if mobile else
                          ("somma di INTERI: l'ordine e' inerte" if mobile is False
                           else "somma, tipo NON DICHIARATO nel registro: non lo assumo"))
            else:
                mobile = True
                perche = ("CONCATENAZIONE: l'ordine decide quale valore va a quale INDICE. "
                          "Conta per qualunque tipo, e non e' una questione di ultimo bit")
            # ⚠ LE SOMME ANNIDATE: anche dentro i pezzi di una concatenazione. La prima
            #   stesura guardava solo la forma ESTERNA, e il referto diceva <<0 somme in
            #   virgola mobile>> mentre `psi` del nato contiene `0.5 * (cur[a] + cur[b])`.
            ann = somme_annidate(x.value)
            mx = max([s["quanti"] for s in ann], default=0)
            fuori.append({"funzione": nodo.name, "riga_oggi": x.lineno,
                          "grandezza": g, "forma": vista[0],
                          "nel_registro": g in nomi_registro,
                          "tipo_dichiarato": tp,
                          "ordine_conta": mobile,
                          "perche": perche,
                          "addendi_in_ordine": vista[1],
                          "somme_annidate": ann,
                          "max_addendi_in_una_somma": mx,
                          "testo": righe[x.lineno - 1].strip()[:150]})
    return fuori


def controllo_ieee(stampa):
    """MISURA, non assume, le due proprieta' su cui poggia la lettura del contratto.

    * DUE addendi: `a + b` e `b + a` sono **byte-identici** (IEEE-754: l'addizione e'
      COMMUTATIVA). ### Quindi su una somma di due addendi l'ordine NON conta.
    * TRE addendi: `(a+b)+c` e `a+(b+c)` **differiscono** (l'addizione NON e' ASSOCIATIVA).
      ### Quindi da tre addendi in su l'ordine conta.
    I valori sono scelti perche' la METTANO in crisi (scale `1e8` e `1e-8`), non a caso.
    """
    r = np.random.default_rng(0)
    a = r.normal(0, 1e8, 200000)
    b = r.normal(0, 1e-8, 200000)
    c = r.normal(0, 1e-8, 200000)
    comm = bool(np.array_equal((a + b).view(np.uint64), (b + a).view(np.uint64)))
    ass = bool(np.array_equal(((a + b) + c).view(np.uint64), (a + (b + c)).view(np.uint64)))
    quante = int(np.sum(((a + b) + c) != (a + (b + c))))
    stampa("  DUE addendi   `a+b` contro `b+a`      byte-identici: %s" % comm)
    stampa("  TRE addendi   `(a+b)+c` contro `a+(b+c)`  identici: %s   (differenze: %d su 200000)"
           % (ass, quante))
    stampa("  ### ➜ L'ORDINE DEGLI ADDENDI CONTA DA **TRE** IN SU, non da due. MISURATO.")
    return {"due_addendi_commutativi": comm, "tre_addendi_associativi": ass,
            "differenze_su_200000": quante}


def tutte_le_somme_del_perimetro(percorso, funzioni):
    """TUTTE le somme `+` delle funzioni, **QUALUNQUE sia il bersaglio** -- locali comprese.

    ### ⚠ PERCHE' SERVE, ed e' il modo in cui chiudo un BUCO DICHIARATO del mio stesso strumento:
    la misura (2) parte dalle **scritture di `self.<nome>`**, quindi ### **perde le somme che
    passano da una VARIABILE LOCALE** -- per esempio `pos_figlio = 0.5 * (pos[a] + pos[b])`, che
    il figlio della mitosi usa. ### **E' il punto cieco degli ALIAS LOCALI**, che in questa
    sessione ha gia' nascosto cose quattro volte.
    ### ➜ **Invece di inseguirlo, si misura la cosa che INVALIDEREBBE la conclusione:** esiste,
    nel perimetro, **una somma di TRE addendi o piu'?** Se no, ### **il buco non puo' cambiare il
    verdetto**, perche' a due addendi l'ordine e' commutativo (misurato).
    """
    src = io.open(percorso, encoding="utf-8").read()
    t = ast.parse(src)

    def addendi(e):
        if isinstance(e, ast.BinOp) and isinstance(e.op, ast.Add):
            return addendi(e.left) + addendi(e.right)
        return [e]

    per_n, tre = {}, []
    tot = 0
    for n in ast.walk(t):
        if not (isinstance(n, ast.FunctionDef) and n.name in funzioni):
            continue
        visti = set()
        for x in ast.walk(n):
            if isinstance(x, ast.BinOp) and isinstance(x.op, ast.Add):
                if id(x) in visti:
                    continue
                ad = addendi(x)
                for y in ad:
                    for z in ast.walk(y):
                        visti.add(id(z))
                tot += 1
                per_n[len(ad)] = per_n.get(len(ad), 0) + 1
                if len(ad) >= 3:
                    tre.append({"funzione": n.name, "riga_oggi": x.lineno,
                                "quanti": len(ad), "testo": ast.unparse(x)[:120]})
    return {"totale": tot, "per_numero_di_addendi": per_n, "con_tre_o_piu": tre}


def riduzioni_ordine_dipendenti(percorso, funzioni):
    """`np.add.at` e `np.bincount`: riduzioni il cui risultato dipende dall'ORDINE degli addendi.

    Non sono somme scritte: sono **accumulazioni** su molti termini, e li' l'associativita' morde
    davvero. Si elencano col loro RAMO, cosi' si vede se girano.
    """
    src = io.open(percorso, encoding="utf-8").read()
    t = ast.parse(src)
    fuori = []
    for n in ast.walk(t):
        if isinstance(n, ast.FunctionDef) and n.name in funzioni:
            for x in ast.walk(n):
                if isinstance(x, ast.Call):
                    s = ast.unparse(x.func)
                    if "add.at" in s or "bincount" in s:
                        fuori.append({"funzione": n.name, "riga_oggi": x.lineno,
                                      "testo": ast.unparse(x)[:120]})
    return fuori


def principale():
    seme, da, fino = 11, 40, 72
    for x in sys.argv[1:]:
        if x.startswith("--seme="):
            seme = int(x.split("=", 1)[1])
        elif x.startswith("--da="):
            da = int(x.split("=", 1)[1])
        elif x.startswith("--fino="):
            fino = int(x.split("=", 1)[1])
    if not os.path.isdir(FUORI):
        os.makedirs(FUORI)
    P = []

    def stampa(*x):
        r = " ".join(str(y) for y in x)
        P.append(r)
        print(r)

    stampa("=" * 104)
    stampa("L'ORDINE DELLE ESTRAZIONI E DELLE SOMME NELLA NASCITA  (passo 1 del COMMIT 3)")
    stampa("=" * 104)
    stampa("simulatore ..... %s" % blob(SIM)[:8])
    stampa("questo strumento %s" % blob(os.path.abspath(__file__))[:8])
    stampa("seme %d   dal passo %d al %d" % (seme, da, fino))
    stampa("")

    S, net = carica("ordest", seme, da)
    _cli_flag.dichiara_configurazione(S, stampa)
    stampa("")
    stampa("scena: n = %d, archi = %d   (dopo %d passi)" % (net.n, len(net.i), da))
    stampa("")

    # ---------- il CONTROLLO: con e senza spia, byte-identico? --------------------------------
    stampa("=" * 104)
    stampa("CONTROLLO -- lo stesso passo CON e SENZA la spia su `net.rng`: byte-identico?")
    stampa("=" * 104)
    A, B = copy.deepcopy(net), copy.deepcopy(net)
    S.net = A
    with contextlib.redirect_stdout(io.StringIO()):
        _passo.passo_pieno(S, A)
    fa = foto(S, A)
    reg_prova, dove_prova = [], {"passo": da + 1, "voce": None}
    B.rng = RngSpiato(B.rng, reg_prova, dove_prova)
    S.net = B
    with contextlib.redirect_stdout(io.StringIO()):
        _passo.passo_pieno(S, B)
    fb = foto(S, B)
    S.net = net
    sano, differenze = identiche(fa, fb)
    stampa("  estrazioni intercettate nel passo di prova: %d" % len(reg_prova))
    stampa("  grandezze e contatori confrontati ........: %d" % len(fa))
    if sano:
        stampa("  ### CONTROLLO OK: la spia NON cambia un bit.")
    else:
        stampa("  ### CONTROLLO FALLITO: la spia PERTURBA. LA MISURA NON VALE.")
        for d in differenze[:20]:
            stampa("      %s" % d)
        io.open(os.path.join(FUORI, "_ordine_estrazioni.json"), "w", encoding="utf-8",
                newline=NL).write(json.dumps(
                    {"vale": False, "motivo": "la spia su net.rng perturba lo stato",
                     "differenze": differenze[:50]}, indent=1))
        io.open(os.path.join(FUORI, "_corsa.txt"), "w", encoding="utf-8",
                newline=NL).write(NL.join(P) + NL)
        return 1
    stampa("")

    # ---------- la MISURA (A): le estrazioni, per VOCE e in ORDINE ----------------------------
    stampa("=" * 104)
    stampa("(A) LE ESTRAZIONI, per VOCE e in ORDINE -- dal passo %d al %d" % (da + 1, fino))
    stampa("=" * 104)
    registro, dove = [], {"passo": da, "voce": None}
    net.rng = RngSpiato(net.rng, registro, dove)
    vero_controllo = S._ferma_se_registro_incoerente
    ordine_voci = {"ultima": None}

    def spia(nt, dv, voce=None, comp=None):
        # il controllo gira DOPO ogni voce: cio' che si e' pescato da qui in avanti appartiene
        # alla voce SEGUENTE. Si tiene l'indice nella composizione IN USO, mai il nome cablato.
        c = list(comp) if comp else list(getattr(S, "PASSO_COMPOSIZIONE", ()))
        if voce is None:
            dove["voce"] = c[0] if c else None
        else:
            k = c.index(voce) if voce in c else -1
            dove["voce"] = c[k + 1] if 0 <= k < len(c) - 1 else "(fine del passo)"
        ordine_voci["ultima"] = voce
        return vero_controllo(nt, dv, voce=voce, comp=comp)

    S._ferma_se_registro_incoerente = spia
    nascite = []
    passo = da
    while passo < fino:
        passo += 1
        dove["passo"] = passo
        n0, m0 = int(net.n), len(net.i)
        with contextlib.redirect_stdout(io.StringIO()):
            _passo.passo_pieno(S, net)
        if int(net.n) != n0:
            nascite.append({"passo": passo, "d_n": int(net.n) - n0, "d_m": len(net.i) - m0})
    S._ferma_se_registro_incoerente = vero_controllo

    stampa("  passi misurati .......: %d" % (fino - da))
    stampa("  estrazioni registrate : %d" % len(registro))
    stampa("  passi CON nascite ....: %d  %s"
           % (len(nascite), ", ".join("p%d(+%dn,+%dm)" % (x["passo"], x["d_n"], x["d_m"])
                                      for x in nascite)))
    stampa("")
    per_voce = {}
    for e in registro:
        k = (e["voce"], e["metodo"])
        per_voce.setdefault(k, {"chiamate": 0, "elementi": 0})
        per_voce[k]["chiamate"] += 1
        per_voce[k]["elementi"] += e["quanti"]
    stampa("  %-26s %-18s %10s %14s" % ("VOCE", "metodo", "chiamate", "elementi"))
    stampa("  " + "-" * 72)
    for (v, mt), q in sorted(per_voce.items(), key=lambda z: (-z[1]["chiamate"], str(z[0]))):
        stampa("  %-26s %-18s %10d %14d" % (v, mt, q["chiamate"], q["elementi"]))
    stampa("")

    # L'ORDINE DENTRO UN PASSO: si riporta la sequenza di UN passo con nascita e di uno senza,
    #   perche' il contratto e' <<quale sequenza>>, non <<quante volte in totale>>.
    def sequenza(p):
        return [(e["voce"], e["metodo"], e["quanti"]) for e in registro if e["passo"] == p]

    p_nasc = nascite[0]["passo"] if nascite else None
    p_senza = None
    for p in range(da + 1, fino + 1):
        if p not in [x["passo"] for x in nascite]:
            p_senza = p
            break
    stampa("  LA SEQUENZA DI UN PASSO -- e questa E' il contratto:")
    for eti, p in (("SENZA nascite", p_senza), ("CON nascite", p_nasc)):
        if p is None:
            stampa("    %-16s (nessun passo di questo tipo nella finestra)" % eti)
            continue
        sq = sequenza(p)
        stampa("    %-16s passo %d:  %d estrazioni" % (eti, p, len(sq)))
        for k, (v, mt, q) in enumerate(sq, 1):
            stampa("        %2d. voce `%s`  ->  rng.%s  (%d elementi)" % (k, v, mt, q))
    stampa("")

    # LE ESTRAZIONI FUORI DAL PASSO: si contano a parte.
    #   ⚠ LA SPIA SI INSTALLA AVVOLGENDO `np.random.default_rng`, PRIMA del caricamento. La prima
    #     stesura sottoclassava `S.Rete` DOPO `carica_dal_cli` e riportava ZERO: un numero FALSO,
    #     perche' `_applica_flag` crea la `Rete` (`:9830`) e chiama `net.semina(...)` (`:9847`)
    #     DENTRO `carica_dal_cli`. Verificato sul sorgente, non supposto.
    stampa("  LE ESTRAZIONI FUORI DAL PASSO (il vuoto di `_applica_flag`, poi la scena):")
    reg_semina = []
    dove_semina = {"passo": 0, "voce": "vuoto (_applica_flag, dentro carica_dal_cli)"}
    _vero_default_rng = np.random.default_rng

    def _rng_spiato(*aa, **kk):
        return RngSpiato(_vero_default_rng(*aa, **kk), reg_semina, dove_semina)

    try:
        np.random.default_rng = _rng_spiato
        with contextlib.redirect_stdout(io.StringIO()):
            _S0, argv2 = _cli_flag.argv_del_driver(extra=["--seme=%d" % seme],
                                                   dest=os.path.join(FUORI, "_scarto_cli2"))
            S2, a2 = _cli_flag.carica_dal_cli(list(argv2), nome="ordest_semina")
            S2._applica_regime(a2)
            S2._NMASSE_VIDEO["n"] = max(2, int(getattr(a2, "nmasse", 2)))
            S2._NMASSE_VIDEO["sep"] = float(getattr(a2, "sep", 3.0))
            S2._NMASSE_VIDEO["size"] = None
            dove_semina["voce"] = "scena MASSE-COERENTI (avvia_test)"
            S2.avvia_test("MASSE-COERENTI")()
    finally:
        np.random.default_rng = _vero_default_rng
    sem = {}
    for e in reg_semina:
        k = (e["voce"], e["metodo"])
        sem.setdefault(k, {"chiamate": 0, "elementi": 0})
        sem[k]["chiamate"] += 1
        sem[k]["elementi"] += e["quanti"]
    stampa("    n = %d, archi = %d   estrazioni: %d"
           % (S2.net.n, len(S2.net.i), len(reg_semina)))
    if not reg_semina:
        stampa("    ### ⛔ ZERO ESTRAZIONI: NON si legge come un fatto. La semina PESCA")
        stampa("        (`rng.random`, `rng.normal`, `rng.choice` nel suo corpo), quindi uno")
        stampa("        zero qui vuol dire CHE LA SPIA NON C'ERA. Si dichiara NON MISURATO.")
    for (v, mt), q in sorted(sem.items()):
        stampa("    %-44s rng.%-10s chiamate %4d   elementi %12d"
               % (v, mt, q["chiamate"], q["elementi"]))
    stampa("")

    # ---------- la MISURA (B): l'ordine degli addendi -----------------------------------------
    FUNZ = ("mitosi", "_eredita_psi_figli", "_eredita_spinore_figli", "semina", "_allaccia")
    stampa("=" * 104)
    stampa("(B) LE SCRITTURE CHE DIPENDONO DALL'ORDINE DEGLI ADDENDI  (dall'AST, e qui l'AST")
    stampa("    E' lo strumento giusto: l'ordine di `a + b` E' un fatto della SINTASSI)")
    stampa("=" * 104)
    nomi_reg = set(getattr(S, "REGISTRO_NOMI", ()))
    tipi_reg = {}
    for x in getattr(S, "REGISTRO_STATO", ()):
        tipi_reg[x[0]] = x[2]
    for x in getattr(S, "REGISTRO_FINESTRA", ()):
        tipi_reg[x[0]] = x[2]
    somme = somme_della_nascita(SIM, FUNZ, nomi_reg, tipi_reg)
    conc = [s for s in somme if s["forma"] != "somma"]
    # `s_mob` non serve piu`: la classificazione per TIPO della forma esterna e` stata
    #   sostituita dal conteggio degli ADDENDI (vedi la (2)).  Resta `s_int`/`s_nd` per i
    #   contatori, che si riportano separati e dichiarati inerti.
    s_int = [s for s in somme if s["forma"] == "somma" and s["ordine_conta"] is False]
    s_nd = [s for s in somme if s["forma"] == "somma" and s["ordine_conta"] is None]
    nel_reg = [s for s in somme if s["nel_registro"]]
    stampa("  funzioni esaminate: %s" % ", ".join(FUNZ))
    stampa("  scritture trovate : %d   di cui nel REGISTRO %d" % (len(somme), len(nel_reg)))
    stampa("")
    stampa("  ### IL CONTRATTO, E SONO TRE COSE DIVERSE:")
    stampa("  ###   (1) %3d CONCATENAZIONI -- l'ordine decide QUALE VALORE VA A QUALE INDICE."
           % len(conc))
    stampa("  ###       Conta per QUALUNQUE tipo: non e' l'ultimo bit, e' il SIGNIFICATO.")
    stampa("  ###   (2) le SOMME ARITMETICHE, comprese le ANNIDATE: contano da TRE addendi in su")
    stampa("  ###       (ASSOCIATIVITA'); a DUE sono commutative, e lo si MISURA qui sotto.")
    stampa("  ###   (3) le RIDUZIONI `np.add.at` / `np.bincount`: li' l'ordine morde davvero.")
    stampa("")
    stampa("  (1) LE CONCATENAZIONI, nell'ordine del sorgente:")
    stampa("  " + "-" * 100)
    for s in conc:
        stampa("  :%-6d %-22s %-10s %-16s [%s]%s"
               % (s["riga_oggi"], s["funzione"], s["forma"], s["grandezza"],
                  s["tipo_dichiarato"], "" if s["nel_registro"] else "  (NON nel registro)"))
        stampa("          pezzi in ordine: %s" % " | ".join(s["addendi_in_ordine"]))
    stampa("")
    # ---------- (2) LE SOMME ARITMETICHE, comprese le ANNIDATE -------------------------------
    stampa("  (2) LE SOMME ARITMETICHE, comprese quelle ANNIDATE dentro una concatenazione")
    stampa("  " + "-" * 100)
    stampa("  E prima di contarle, le DUE proprieta' su cui poggia la lettura -- MISURATE:")
    ieee = controllo_ieee(stampa)
    stampa("")
    tutte_somme = []
    for s in somme:
        for q in s["somme_annidate"]:
            tutte_somme.append(dict(q, grandezza=s["grandezza"], funzione=s["funzione"],
                                    riga_oggi=s["riga_oggi"],
                                    tipo_dichiarato=s["tipo_dichiarato"],
                                    nel_registro=s["nel_registro"]))
    tre_piu = [q for q in tutte_somme if q["quanti"] >= 3]
    due = [q for q in tutte_somme if q["quanti"] == 2]
    stampa("  somme aritmetiche trovate (annidate comprese): %d" % len(tutte_somme))
    stampa("    con DUE addendi  -> l'ordine e' INERTE (commutativita' misurata): %d" % len(due))
    stampa("    con TRE o piu'   -> ### L'ORDINE CONTA, ED ENTRA NEL CONTRATTO : %d" % len(tre_piu))
    if tre_piu:
        for q in tre_piu:
            stampa("      :%-6d %-16s %d addendi: %s" % (q["riga_oggi"], q["grandezza"],
                                                         q["quanti"], " | ".join(q["addendi"])))
    else:
        stampa("      ### NESSUNA. Nel perimetro della nascita non esiste una somma scritta di")
        stampa("          TRE o piu' addendi, quindi l'ASSOCIATIVITA' non ha casi. Le somme a")
        stampa("          DUE addendi -- `0.5*(x[a] + x[b])` -- sono COMMUTATIVE per IEEE-754,")
        stampa("          misurato qui sopra: il loro ordine NON va nel contratto.")
    stampa("")
    # ⚠ IL BUCO DEGLI ALIAS LOCALI, e si CHIUDE misurando cio' che invaliderebbe la conclusione.
    tutte = tutte_le_somme_del_perimetro(SIM, FUNZ)
    stampa("  ### E IL BUCO DEGLI ALIAS LOCALI, CHIUSO CON UNA MISURA invece che inseguito:")
    stampa("      la (2) parte dalle scritture di `self.<nome>`, quindi PERDE le somme che")
    stampa("      passano da una LOCALE (`pos_figlio = 0.5 * (pos[a] + pos[b])`).")
    stampa("      ➜ Allora si contano TUTTE le somme del perimetro, QUALUNQUE bersaglio:")
    stampa("        totale %d   %s" % (tutte["totale"],
                                       "  ".join("con %d addendi: %d" % (k, tutte[
                                           "per_numero_di_addendi"][k])
                                                 for k in sorted(
                                                     tutte["per_numero_di_addendi"]))))
    if tutte["con_tre_o_piu"]:
        stampa("        ### ⛔ CON TRE O PIU' ADDENDI: %d -- L'ORDINE CONTA, e vanno nel contratto"
               % len(tutte["con_tre_o_piu"]))
        for q in tutte["con_tre_o_piu"]:
            stampa("          :%-6d %-22s %d addendi  %s" % (q["riga_oggi"], q["funzione"],
                                                             q["quanti"], q["testo"]))
    else:
        stampa("        ### ✅ ZERO con tre o piu' addendi ➜ IL BUCO NON PUO' CAMBIARE IL")
        stampa("            VERDETTO: a due addendi l'ordine e' commutativo, misurato sopra.")
    stampa("")
    stampa("  LE SOMME a due addendi, elencate perche' chi legge le cerca:")
    for q in due[:40]:
        stampa("    :%-6d %-16s %s" % (q["riga_oggi"], q["grandezza"], q["testo"][:80]))
    if len(due) > 40:
        stampa("    ... e altre %d (tutte nel `json`)" % (len(due) - 40))
    stampa("")
    # ---------- (3) le RIDUZIONI, dove l'associativita' morde davvero -------------------------
    rid = riduzioni_ordine_dipendenti(SIM, FUNZ)
    stampa("  (3) LE RIDUZIONI ordine-dipendenti (`np.add.at`, `np.bincount`): %d" % len(rid))
    stampa("      Non sono somme SCRITTE: sono ACCUMULAZIONI su molti termini, e li'")
    stampa("      l'associativita' morde davvero.")
    for q in rid:
        stampa("      :%-6d %-22s %s" % (q["riga_oggi"], q["funzione"], q["testo"]))
    stampa("      E IL RAMO IN CUI VIVONO, dal RUNTIME: MITOSI_DIR = %r" % getattr(S, "MITOSI_DIR",
                                                                                  "<assente>"))
    if float(getattr(S, "MITOSI_DIR", 0.0)) == 0.0 and rid:
        stampa("      ### ➜ `MITOSI_DIR = 0.0`, quindi quel ramo NON GIRA e queste riduzioni")
        stampa("          NON avvengono nella configurazione di riferimento. Resta DICHIARATO:")
        stampa("          se un giorno `MITOSI_DIR != 0`, l'ordine di `add.at` entra nel")
        stampa("          contratto -- e il contratto di OGGI non lo copre.")
    stampa("")
    stampa("  I CONTATORI, somme di INTERI fuori dal registro: %d  (ordine INERTE)" % len(s_nd))
    stampa("    %s" % ", ".join(sorted({s["grandezza"] for s in s_nd})))
    if s_int:
        stampa("  E %d somme di grandezze del registro, intere: %s"
               % (len(s_int), ", ".join(sorted({s["grandezza"] for s in s_int}))))
    stampa("")

    ref = {"vale": True,
           "blob_sim_sha1_byte": blob(SIM),
           "blob_strumento": blob(os.path.abspath(__file__)),
           "seme": seme, "da": da, "fino": fino,
           "controllo_con_senza_spia": {"byte_identico": bool(sano),
                                        "grandezze_e_contatori": len(fa),
                                        "estrazioni_nel_passo_di_prova": len(reg_prova)},
           "nascite": nascite,
           "estrazioni_totali": len(registro),
           "per_voce_e_metodo": [{"voce": v, "metodo": mt, "chiamate": q["chiamate"],
                                  "elementi": q["elementi"]}
                                 for (v, mt), q in sorted(per_voce.items(), key=lambda z: str(z[0]))],
           "sequenza_passo_senza_nascite": sequenza(p_senza) if p_senza else None,
           "sequenza_passo_con_nascite": sequenza(p_nasc) if p_nasc else None,
           "passo_senza_nascite": p_senza, "passo_con_nascite": p_nasc,
           "fuori_dal_passo": {"estrazioni": len(reg_semina),
                               "misurato": bool(reg_semina),
                               "per_voce_e_metodo": [{"voce": v, "metodo": mt,
                                                      "chiamate": q["chiamate"],
                                                      "elementi": q["elementi"]}
                                                     for (v, mt), q in sorted(sem.items())],
                               "n": int(S2.net.n), "archi": len(S2.net.i)},
           "scritture_ordine": somme,
           "contratto_concatenazioni": conc,
           "controllo_ieee754": ieee,
           "somme_aritmetiche_tutte": tutte_somme,
           "somme_tre_o_piu_addendi_ORDINE_CONTA": tre_piu,
           "somme_due_addendi_ordine_inerte": due,
           "riduzioni_ordine_dipendenti": rid,
           "tutte_le_somme_del_perimetro": tutte,
           "MITOSI_DIR_dal_runtime": float(getattr(S, "MITOSI_DIR", 0.0)),
           "somme_interi_nel_registro": s_int,
           "somme_tipo_non_dichiarato": s_nd,
           "registro_completo": registro}
    io.open(os.path.join(FUORI, "_ordine_estrazioni.json"), "w", encoding="utf-8",
            newline=NL).write(json.dumps(ref, indent=1, default=str))
    io.open(os.path.join(FUORI, "_corsa.txt"), "w", encoding="utf-8",
            newline=NL).write(NL.join(P) + NL)
    stampa("referto: csv/_test_fork/_ordine_estrazioni/_ordine_estrazioni.json")
    return 0


if __name__ == "__main__":
    sys.exit(principale())
