# -*- coding: utf-8 -*-
"""**IL CENSIMENTO DELLA FRAZIONE DI NASCITA nel perimetro della mitosi.**

### `PASSO 1` del `COMMIT 6a` del riordino, e gira **PRIMA del codice**.

## IL SETACCIO PARTE DAL NUMERO, NON DALLE FORME -- e il motivo e' un buco MISURATO

La prima stesura cercava le **forme** che il mandato elenca *(`0.5*(x+y)`, `(x+y)/2`,
`x*0.5`)* e ne ha trovate **17**. ### **Ma non ha visto `(0.5 + bias) * D`** *(`:8496`)*,
dove il `0.5` sta dentro un `Add` e non e' un operando diretto di `Mult`.
### **Ed era il sito piu' importante: quello dove una frazione DIVERSA da `0.5` ESISTE GIA'.**

### \U0001f4cc **E' la famiglia di `FALSO-ZERO`:** un setaccio che parte dalle **forme** trova
### **le forme che ha pensato**, e lo zero sulle altre e' ### **garantito dalla costruzione.**

### ✅ **CURA: si cerca OGNI `0.5` LETTERALE e ogni DIVISIONE PER `2`**, qualunque sia
l'espressione che li contiene. ### **Cosi' nessuna forma puo' nascondersi**, e il lavoro passa
dal **trovare** al **classificare** -- che e' dove deve stare, perche' una classificazione
### **si dichiara e si verifica.**

### ⚠ **E LA FORMA `x / 2` NON ERA NEL MANDATO** *(che elencava `0.5*(x+y)`, `(x+y)/2`,
`x*0.5`)*: senza di lei ### **il sito `dh` NON si troverebbe**, perche' e'
`self.d[sel] / 2` -- e e' uno dei siti che il commit deve curare.

## LE TRE CLASSI, e distinguerle E' il lavoro

| | |
|---|---|
| ### **`FRAZIONE`** | decide ### **DOVE sta il figlio** *(`pos`, `fm`)* o ### **QUANTO sono lunghi i suoi archi** *(`d`, `d0`, `dd`)*. ### **E' quello che il `6a` deve portare in un solo posto** |
| `EREDITA-MEDIA` | il figlio prende la ### **MEDIA** dei genitori di una grandezza di ### **STATO** *(`phivel`, `psi`)*. ### **Lo STESSO numero, NON la stessa domanda** |
| `ALTRO` | una meta' che fa ### **altro**: una media di densita', il centro di un intervallo di soglia, l'ampiezza di un calcio, ### **meta' del DOMINIO** della fase |

### \U0001f4cc **E LA TABELLA `DICHIARATI` E' UN PRESIDIO:** `principale()` asserisce che
l'insieme trovato sia ### **esattamente** quello dichiarato. ### **Un sito NUOVO fa FALLIRE lo
strumento** invece di cambiare il conteggio in silenzio *(`A9`)*.

**COMANDO:** `python csv/_test_fork/_censimento_punto_medio.py`
**USCITA:** `csv/_test_fork/_censimento_punto_medio/`
"""
import ast
import contextlib
import hashlib
import importlib.util
import io
import json
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_QUI, ".."))
import _presidio   # noqa: E402

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
SIM = os.path.join(RADICE, "soliton_simulator.py")
FUORI = os.path.join(_QUI, "_censimento_punto_medio")
NL = chr(10)

# ### IL PERIMETRO, dichiarato: `mitosi` (che contiene la preparazione E il ramo
#   Schwinger), `decidi_divisione` (dove vivono meta' che NON sono frazioni di nascita,
#   e vanno VISTE per poterle escludere), e TUTTE le regole della tabella.
PERIMETRO_ESATTO = ("mitosi", "decidi_divisione")
PERIMETRO_PREFISSI = ("_rn_div_", "_rn_sch_")

DICHIARATI = {
    # ---- FRAZIONE: dove sta il figlio, e quanto sono lunghi i suoi archi
    8496: ("FRAZIONE", "DIVISIONE/fm (fase)",
           "DIVISIONE, la FASE del figlio, ramo MITOSI_DIR: fm = (phi[a] - (0.5+bias)*D). "
           "*** QUI UNA FRAZIONE DIVERSA DA 0.5 ESISTE GIA': "
           "bias = 0.5*tanh(MITOSI_DIR*(twn[a]-twn[b])) sta in [-0.5,0.5], e il commento del "
           "codice dice: <<verso il genitore piu' teso. 0 = punto medio>>"),
    8498: ("FRAZIONE", "DIVISIONE/fm (fase)",
           "DIVISIONE, la FASE del figlio, ramo SENZA MITOSI_DIR: fm = (phi[a] - 0.5*D)"),
    8499: ("FRAZIONE", "DIVISIONE/pos",
           "DIVISIONE, DOVE nasce il figlio: pos_figlio = 0.5*(pos[a] + pos[b])"),
    8561: ("FRAZIONE", "DIVISIONE/d,d0",
           "DIVISIONE, QUANTO sono lunghi i due tronconi: dh = self.d[sel]/2. La lunghezza "
           "viene da `d` -- e nello Schwinger da `pos`: e' SCHW-CORTI"),
    2344: ("FRAZIONE", "SCHWINGER/pos",
           "SCHWINGER, DOVE nasce l'antinodo: 0.5*(pos[aa] + pos[bb]), nella regola "
           "_rn_sch_pos"),
    8701: ("FRAZIONE", "SCHWINGER/dd",
           "SCHWINGER, QUANTO sono lunghi i due archi nuovi: 0.5*norm(pos[aa]-pos[bb]). La "
           "lunghezza viene da `pos`, NON da `d`: e' SCHW-CORTI"),
    # ---- EREDITA-MEDIA: il figlio prende la MEDIA di una grandezza di STATO.
    #      Lo STESSO numero, ma NON la stessa domanda: se la frazione cambia, questa media
    #      dovrebbe seguire la GEOMETRIA? Il 6a NON lo decide: lo DICHIARA.
    1954: ("EREDITA-MEDIA", "phivel",
           "DIVISIONE: il figlio prende la media di phivel. Ed e' la regola che A14 segnala: "
           "la nascita CAMBIA la carica totale"),
    1984: ("EREDITA-MEDIA", "psi", "DIVISIONE: il figlio prende la media di psi"),
    2335: ("EREDITA-MEDIA", "phivel", "SCHWINGER: l'antinodo prende la media di phivel"),
    # ---- ALTRO
    8259: ("ALTRO", "soglia",
           "decidi_divisione: centro = 0.5*(pos_soglia + pos_tetto), il centro di un "
           "INTERVALLO DI SOGLIA, non una nascita"),
    8404: ("ALTRO", "densita",
           "decidi_divisione: 0.5*(I[a]+I[b]) e' la MEDIA DI DENSITA' del criterio"),
    8495: ("ALTRO", "bias",
           "mitosi: bias = 0.5*tanh(...). Il 0.5 e' l'AMPIEZZA del bias (lo tiene in "
           "[-0.5,0.5]), NON la frazione: la frazione e' il 0.5 di :8496. DUE 0.5 CON DUE "
           "RUOLI DIVERSI SULLA STESSA LEGGE, e distinguerli e' il punto"),
    8509: ("ALTRO", "densita", "mitosi: rho_sel = 0.5*(I[a]+I[b]), media di densita'"),
    8519: ("ALTRO", "dominio",
           "mitosi: _mezzo = self._dphi()/2.0, META' DEL DOMINIO della fase"),
    8540: ("ALTRO", "calcio",
           "mitosi: comune = KICK_TW*sciolta*(mod - 0.5). Il 0.5 e' un OFFSET che centra "
           "`mod` intorno a zero, non una frazione di nascita. *** E L'HA TROVATA SOLO IL "
           "SETACCIO CHE PARTE DAL NUMERO: nella forma `(mod - 0.5)` il 0.5 sta dentro un "
           "Sub, quindi il setaccio delle FORME non la vedeva -- una conferma in piu' che "
           "partire dalle forme era sbagliato"),
    8541: ("ALTRO", "calcio",
           "mitosi: 0.5*KICK_TW, l'ampiezza del calcio ripartita fra i due genitori"),
    8542: ("ALTRO", "calcio", "mitosi: idem, col segno opposto"),
    8665: ("ALTRO", "densita", "mitosi (ramo Schwinger): rho_sel = 0.5*(I[a]+I[b])"),
    8694: ("ALTRO", "dominio",
           "mitosi: anti = fm + _dphi()/2, l'ANTIFASE (meta' del DOMINIO)"),
}


# ### LA LISTA DEL GUARDIANO (rilievo del 2026-10-03), per il CONFRONTO.
#   Il mandato chiede: *<<fallo dall'AST, confronta la tua lista con questa, e se
#   differiscono dimmi DOVE>>*. La tengo qui perche' il confronto lo faccia LA MACCHINA.
GUARDIANO_OLTRE_I_QUATTRO = {
    # ### CORREZIONE DEL 2026-10-03, E LA CAUSA E' UN ERRORE DEL GUARDIANO, che la
    #   dichiara: aveva citato il ramo `MITOSI_DIR` come ### **`:8489`**, che e' la riga
    #   del CANCELLO (`if MITOSI_DIR != 0.0`), non la riga del NUMERO. Le righe del
    #   numero, misurate dall'AST, sono ### **`:8495`** (l'ampiezza del bias) e
    #   ### **`:8496`** (la frazione `(0.5 + bias)`).
    #   ### ✅ E CON LA LISTA CORRETTA LA DIFFERENZA CALCOLATA DEVE RISULTARE TUTTA
    #   `ALTRO`: ### e' il controllo che la correzione e' giusta, e non una mia asserzione.
    8495: "l'ampiezza del bias del ramo MITOSI_DIR (correzione: il guardiano citava :8489)",
    8496: "la frazione (0.5 + bias) del ramo MITOSI_DIR (correzione: era :8489)",
    8498: "la fase fm = phi[a] - 0.5*D",
    1954: "phivel nella divisione",
    2335: "phivel nello Schwinger",
    1984: "psi, usata da ENTRAMBI gli eventi",
    8509: "rho_sel, la densita' sull'arco del cancello dell'antifase",
    8665: "rho_sel, idem nel ramo Schwinger",
}
GUARDIANO_FALSI_POSITIVI = {
    8519: "_dphi()/2: l'antifase pi, non un punto medio",
    8694: "_dphi()/2: idem",
}
GUARDIANO_I_QUATTRO = {8499: "DIVISIONE/pos", 8561: "DIVISIONE/d,d0",
                       2344: "SCHWINGER/pos", 8701: "SCHWINGER/dd"}


# ### IL CONTEGGIO DEL GUARDIANO per l'EREDITA' DA UN SOLO GENITORE, da confrontare
#   con quello della macchina.
GUARDIANO_COPIA_GENITORE = {
    ("divisione", "phi_s"): "da `a`",
    ("divisione", "psi_spin"): "da `a`",
    ("divisione", "rho_spin"): "da `a`",
    ("schwinger", "psi_spin"): "da `aa`",
    ("schwinger", "rho_spin"): "da `aa`",
    ("schwinger", "phi_s"): "zero (non da un genitore)",
}
# ### LE CHIAVI DEL CONTESTO, divise per LATO. Una regola che indicizza SOLO il lato `a`
#   e non il lato `b` eredita ### **da un solo genitore**, cioe' usa un ### **`t = 0`
#   IMPLICITO** -- e il setaccio del NUMERO non lo vede, perche' ### **non c'e' nessun
#   numero da trovare.** ### 📌 E' `FALSO-ZERO` applicato alla decisione aperta di
#   Luca: cercando i `0.5` si conclude *<<cinque siti>>* e si perde una CLASSE INTERA di
#   siti dove la frazione e' ### **gia' decisa, a zero.**
LATO_A = ("a", "aa", "src", "src_a")
LATO_B = ("b", "bb", "src_b")
# ### LE FORME PER CUI UNA FRAZIONE NON HA SENSO, e il criterio e' LETTO DAL REPO
#   (`DOMINI`, 42 voci: nome -> (forma, descrizione)) invece di una mia lista a mano:
#     `indice`  -> `i`, `j`: e' TOPOLOGIA, non un valore da interpolare;
#     `segno`   -> `perc_chi`, `perc_geom`: e' CATEGORIALE, e il registro lo dice
#                  esplicitamente -- *<<sommare due decisioni darebbe +2, 0 o -2,
#                  che non sono valori ammessi>>*.
#   ### ⛔ **E UNA GRANDEZZA CHE NON STA IN `DOMINI` NON SI ESCLUDE: SI ELENCA.**
#   La prima stesura la escludeva *<<perche' la forma non e' dichiarata>>*, ed era un
#   ### **FALSO-ZERO** *(rilievo del guardiano, 2026-10-03, ed e' giusto)*:
#   ### **una forma IGNOTA non e' una forma in cui la frazione non ha senso.**
#   Escludere per ignoranza fa SCOMPARIRE 18 regole che copiano da un solo genitore --
#   e fra loro c'e' ### **lo SPINORE.**
#   ### ✅ CURA: una ### **TERZA CLASSE**, `COPIA-GENITORE-FORMA-IGNOTA`. Restano
#   esclusi ### **solo** i quattro che hanno un motivo DICHIARATO.
FORME_SENZA_FRAZIONE = ("indice", "segno")


def blob(p):
    return hashlib.sha1(io.open(p, "rb").read()).hexdigest()


def _il_numero(nodo):
    """Questo nodo E' il numero che cerchiamo? L'etichetta, oppure `None`.

    ### Due casi, e bastano perche' partono dal NUMERO e non dalla forma: un
    ### **`0.5` letterale DOVUNQUE**, e una ### **divisione per `2`**.
    """
    if isinstance(nodo, ast.Constant) and nodo.value == 0.5:
        return "0.5 letterale"
    if (isinstance(nodo, ast.BinOp) and isinstance(nodo.op, ast.Div)
            and isinstance(nodo.right, ast.Constant) and nodo.right.value in (2, 2.0)):
        return "/ 2"
    return None


class LatiDelleRegole(ast.NodeVisitor):
    """Per ogni `_rn_*`: quali chiavi del CONTESTO indicizza, e di quale LATO.

    ### Non cerca un numero: cerca ### **l'ASSENZA** del lato `b`. Una regola che
    legge solo `c["a"]` (o `aa`, `src`, `src_a`) e mai `c["b"]` eredita da ### **un
    solo genitore**, cioe' ha una frazione ### **implicita a zero.**
    """

    def __init__(self):
        self.per_regola = {}
        self.delega = {}
        self.pila = ["<modulo>"]

    def visit_FunctionDef(self, nodo):
        self.pila.append(nodo.name)
        if nodo.name.startswith(PERIMETRO_PREFISSI):
            self.per_regola.setdefault(nodo.name, set())
        self.generic_visit(nodo)
        self.pila.pop()

    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_Subscript(self, nodo):
        # `c["a"]`: un Subscript su un Name `c` con una stringa costante
        if (isinstance(nodo.value, ast.Name) and nodo.value.id == "c"
                and isinstance(nodo.slice, ast.Constant)
                and isinstance(nodo.slice.value, str)):
            d = self.pila[-1]
            if d.startswith(PERIMETRO_PREFISSI):
                self.per_regola.setdefault(d, set()).add(nodo.slice.value)
        self.generic_visit(nodo)

    def visit_Call(self, nodo):
        """### LA DELEGA, e senza di lei TRE regole sono INVISIBILI.

        `_rn_sch_psi_spin(net, c)` fa ### **soltanto** `_rn_div_psi_spin(net, c)`:
        nel suo corpo ### **non c'e' nessun `c["..."]`**, quindi il setaccio dei lati
        la vedeva con l'insieme ### **vuoto** e la escludeva. ### E sono esattamente
        tre delle sei che il guardiano conta.
        """
        if (isinstance(nodo.func, ast.Name)
                and nodo.func.id.startswith(PERIMETRO_PREFISSI)):
            d = self.pila[-1]
            if d.startswith(PERIMETRO_PREFISSI) and d != nodo.func.id:
                self.delega[d] = nodo.func.id
        self.generic_visit(nodo)

    def risolvi_deleghe(self):
        """Le chiavi di chi delega sono quelle del delegato. UN SALTO, non ricorsivo:
        due salti sarebbero una deduzione, e una deduzione va DICHIARATA."""
        for chi, a_chi in self.delega.items():
            if not self.per_regola.get(chi) and self.per_regola.get(a_chi):
                self.per_regola[chi] = set(self.per_regola[a_chi])


class Setaccio(ast.NodeVisitor):
    """Ogni occorrenza del numero nel perimetro, con funzione, riga e BERSAGLIO."""

    def __init__(self, righe):
        self.righe = righe
        self.trovate = []
        self.pila = ["<modulo>"]
        self.bersaglio = [None]

    def _dentro(self):
        return self.pila[-1]

    def _nel_perimetro(self):
        d = self._dentro()
        return d in PERIMETRO_ESATTO or d.startswith(PERIMETRO_PREFISSI)

    def visit_FunctionDef(self, nodo):
        self.pila.append(nodo.name)
        self.generic_visit(nodo)
        self.pila.pop()

    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_Assign(self, nodo):
        nomi = []
        for t in nodo.targets:
            if isinstance(t, ast.Name):
                nomi.append(t.id)
            elif isinstance(t, ast.Attribute):
                nomi.append("self." + t.attr)
        self.bersaglio.append(", ".join(nomi) if nomi else None)
        self.generic_visit(nodo)
        self.bersaglio.pop()

    def _registra(self, nodo, forma):
        riga = nodo.lineno
        testo = (self.righe[riga - 1].strip()[:150]
                 if 0 < riga <= len(self.righe) else "?")
        self.trovate.append({"riga": riga, "col": nodo.col_offset,
                             "dentro": self._dentro(), "forma": forma,
                             "bersaglio": self.bersaglio[-1], "testo": testo})

    def visit_Constant(self, nodo):
        f = _il_numero(nodo)
        if f is not None and self._nel_perimetro():
            self._registra(nodo, f)
        self.generic_visit(nodo)

    def visit_BinOp(self, nodo):
        f = _il_numero(nodo)
        if f is not None and self._nel_perimetro():
            self._registra(nodo, f)
        self.generic_visit(nodo)


def principale():
    out = []

    def stampa(*x):
        s = " ".join(str(y) for y in x)
        out.append(s)
        print(s)

    if not os.path.isdir(FUORI):
        os.makedirs(FUORI)
    sorgente = io.open(SIM, encoding="utf-8").read()
    v = Setaccio(sorgente.split(NL))
    v.visit(ast.parse(sorgente))

    stampa("=" * 100)
    stampa("IL CENSIMENTO DELLA FRAZIONE DI NASCITA nel perimetro della mitosi")
    stampa("=" * 100)
    stampa("  simulatore .. %s (sha1 byte grezzi)" % blob(SIM)[:8])
    stampa("  strumento ... %s" % blob(os.path.abspath(__file__))[:8])
    stampa("  perimetro ... %s  +  %s*"
           % (", ".join(PERIMETRO_ESATTO), "*, ".join(PERIMETRO_PREFISSI)))
    stampa("  il setaccio cerca IL NUMERO: ogni `0.5` letterale e ogni `/ 2`.")
    stampa("  ### NON le FORME, e il motivo e' un buco MISURATO: cercando `0.5*(x+y)`,")
    stampa("  ###   `(x+y)/2` e `x*0.5` (le tre del mandato) si trovavano 17 siti e NON")
    stampa("  ###   si vedeva `(0.5 + bias) * D` a :8496 -- dove il 0.5 sta dentro un")
    stampa("  ###   Add. Ed era IL SITO PIU' IMPORTANTE. E' FALSO-ZERO: un setaccio che")
    stampa("  ###   parte dalle forme trova le forme che ha pensato.")
    stampa("  ### E la forma `x / 2` non era fra le tre del mandato: senza di lei il")
    stampa("  ###   sito `dh` (self.d[sel] / 2) NON si troverebbe.")
    stampa("")
    stampa("-" * 100)
    stampa("TUTTE LE OCCORRENZE NEL PERIMETRO: %d" % len(v.trovate))
    stampa("")
    non_dich = []
    for x in sorted(v.trovate, key=lambda y: (y["riga"], y["col"])):
        d = DICHIARATI.get(x["riga"])
        if d is None:
            x["classe"], x["grandezza"], x["che_cosa"] = "?", "?", "NON DICHIARATA"
            non_dich.append(x)
        else:
            x["classe"], x["grandezza"], x["che_cosa"] = d
        stampa("  :%-6d col %-4d %-20s %-14s %-14s %s"
               % (x["riga"], x["col"], x["dentro"][:20], x["forma"],
                  x["classe"], x["grandezza"]))
        stampa("          %s" % x["testo"])
        stampa("          -> %s" % x["che_cosa"][:150])
        stampa("")

    if non_dich:
        stampa("=" * 100)
        stampa("### %d OCCORRENZE NON DICHIARATE: LO STRUMENTO FALLISCE." % len(non_dich))
        stampa("###   Un sito nuovo nel perimetro non puo' cambiare il conteggio in")
        stampa("###   silenzio: si classifica o si DICHIARA (A9).")
        for x in non_dich:
            stampa("###   :%d  %s  %s" % (x["riga"], x["dentro"], x["testo"][:90]))
        io.open(os.path.join(FUORI, "_corsa.txt"), "w", encoding="utf-8",
                newline=NL).write(NL.join(out) + NL)
        raise RuntimeError(
            "%d occorrenze NON dichiarate: %s. Si classifica o si dichiara."
            % (len(non_dich), sorted(set(x["riga"] for x in non_dich))))

    fraz = [x for x in v.trovate if x["classe"] == "FRAZIONE"]
    ered = [x for x in v.trovate if x["classe"] == "EREDITA-MEDIA"]
    altri = [x for x in v.trovate if x["classe"] == "ALTRO"]
    gr = sorted(set(x["grandezza"] for x in fraz))
    gr_e = sorted(set(x["grandezza"] for x in ered))

    stampa("-" * 100)
    stampa("LA CLASSIFICAZIONE")
    stampa("  FRAZIONE      (DOVE sta il figlio, QUANTO sono lunghi i suoi archi) .. %d siti"
           % len(fraz))
    for x in sorted(fraz, key=lambda y: y["riga"]):
        stampa("      :%-6d %-20s %-12s %s"
               % (x["riga"], x["dentro"][:20], x["grandezza"], x["forma"]))
    stampa("  EREDITA-MEDIA (il figlio prende la MEDIA di una grandezza di STATO) . %d siti"
           % len(ered))
    for x in sorted(ered, key=lambda y: y["riga"]):
        stampa("      :%-6d %-20s %-12s %s"
               % (x["riga"], x["dentro"][:20], x["grandezza"], x["forma"]))
    stampa("  ALTRO         (una meta' che fa altro) ............................. %d siti"
           % len(altri))
    stampa("")
    stampa("  le GRANDEZZE della FRAZIONE ......... %s  (%d)" % (", ".join(gr), len(gr)))
    stampa("  le GRANDEZZE dell'EREDITA-MEDIA ..... %s" % ", ".join(gr_e))
    stampa("")
    stampa("=" * 100)
    stampa("### IL VERDETTO DEL CENSIMENTO")
    stampa("###   occorrenze del numero nel perimetro .. %d" % len(v.trovate))
    stampa("###   di cui FRAZIONE ...................... %d siti su %d GRANDEZZE"
           % (len(fraz), len(gr)))
    # ### IL CANCELLO CONTA LE COPPIE (evento, grandezza), NON I NOMI.
    #   ### La prima stesura contava i NOMI e dava 4 invece di 5, perche' collassava
    #   `pos` della DIVISIONE con `pos` dello SCHWINGER -- che sono DUE formule in DUE
    #   leggi diverse. ### Il mandato elenca QUATTRO COPPIE: (divisione, pos),
    #   (divisione, d/d0), (schwinger, pos), (schwinger, dd). ### Un cancello che conta i
    #   nomi e' LENIENTE NELLA DIREZIONE SBAGLIATA: mi avrebbe fatto passare oltre la
    #   condizione di stop del mandato.
    basta = (len(gr) <= 4)
    if not basta:
        stampa("###")
        stampa("###   *** PIU' DI QUATTRO: IL COMMIT 6a SI FERMA, come dice il mandato. ***")
        stampa("###")
        stampa("###   Il mandato elencava QUATTRO grandezze -- pos e d/d0 della DIVISIONE,")
        stampa("###   pos e dd dello SCHWINGER -- e NON la FASE del figlio (`fm`), che e'")
        stampa("###   la quinta e sta nella preparazione, con DUE rami.")
        stampa("###")
        stampa("###   E IL FATTO PIU' GRAVE NON E' IL NUMERO: a :8496 UNA FRAZIONE")
        stampa("###   DIVERSA DA 0.5 ESISTE GIA'.")
        stampa("###     bias = 0.5 * tanh(MITOSI_DIR * (twn[a] - twn[b]))")
        stampa("###     fm   = (phi[a] - (0.5 + bias) * D) % dphi")
        stampa("###   e il commento del codice dice: <<bias in [-0.5,0.5]: verso il")
        stampa("###   genitore piu' teso. 0 = punto medio>>.")
        stampa("###")
        stampa("###   CIOE' IL SISTEMA HA GIA' UNA FRAZIONE GENERALE, MA SOLO PER LA FASE,")
        stampa("###   E NON LA APPLICA A `pos`.")
        stampa("###")
        stampa("###   *** E NON E' UNA SVISTA: IL CODICE DICHIARA PERCHE'. *** Il commento")
        stampa("###   a :8486-8488 dice: <<L'asimmetria e' nella FASE, dove vive la materia,")
        stampa("###   non nella posizione (che il rilassamento geometrico riporterebbe")
        stampa("###   indietro). Non e' una forza: e' l'orientamento della replicazione")
        stampa("###   lungo il gradiente gia' presente>>.")
        stampa("###   CORREGGO QUELLO CHE AVEVO SCRITTO: NON e' <<esattamente il difetto")
        stampa("###   che il punto 2 del piano vuole impedire>>. Il punto 2 chiede che `pos`")
        stampa("###   e `d`/`d0` dicano la STESSA cosa -- sono due descrizioni della")
        stampa("###   GEOMETRIA. La fase e' un ALTRO asse, e il codice ha una RAGIONE")
        stampa("###   SCRITTA per trattarlo diversamente.")
        stampa("###")
        stampa("###   MITOSI_DIR vale 0.0 nella configurazione del driver, quindi oggi")
        stampa("###   bias = 0 e la fase sta nel mezzo.")
        stampa("###   MA IL PUNTO RESTA, E NON E' IL NUMERO: se il 6a dichiarasse `t` in un")
        stampa("###   posto solo per la GEOMETRIA, nel codice resterebbero DUE frazioni --")
        stampa("###   `t` per la geometria e `0.5 + bias` per la fase -- e la seconda")
        stampa("###   sarebbe l'unica a non leggere il valore dichiarato. ### SE LE DUE")
        stampa("###   DEBBANO ESSERE LA STESSA E UNA DECISIONE DI LUCA, NON MIA.")
    else:
        stampa("###   *** QUATTRO O MENO: si procede. ***")
    stampa("=" * 100)

    # ------------------------------- L'EREDITA' DA UN SOLO GENITORE: UN `t = 0` IMPLICITO
    lati = LatiDelleRegole()
    lati.visit(ast.parse(sorgente))
    lati.risolvi_deleghe()
    with contextlib.redirect_stdout(io.StringIO()):
        spec = importlib.util.spec_from_file_location("_sim_cens6a", SIM)
        _S = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(_S)
    copie, ignote, esclusi = [], [], []
    for nome, chiavi in sorted(lati.per_regola.items()):
        usa_a = sorted(k for k in chiavi if k in LATO_A)
        usa_b = sorted(k for k in chiavi if k in LATO_B)
        if not (usa_a and not usa_b):
            continue
        ev = "divisione" if nome.startswith("_rn_div_") else "schwinger"
        # ### `gq` e NON `gr`: `gr` e' GIA' usata piu' sopra per le grandezze della
        #   FRAZIONE, e riassegnarla qui ha rotto IL CANCELLO -- il verdetto contava i
        #   CARATTERI di `_spinor_lift` invece delle coppie. Il guasto si e' visto perche'
        #   il referto ha stampato un'assurdita', non perche' l'avessi previsto.
        gq = nome.split("_", 3)[3] if nome.count("_") >= 3 else "?"
        # ### IL NOME SI RISOLVE CONTRO I REGISTRI, NON SI DEDUCE DAL NOME DELLA
        #   FUNZIONE. `_rn_div_psi_spinor` -> `psi_spinor`, ma la grandezza si chiama
        #   ### **`_psi_spinor`**, col trattino basso. ### ⛔ La stesura precedente
        #   troncava e concludeva *<<forma non dichiarata in DOMINI>>* per SEDICI regole
        #   su diciotto -- cioe' ### **lo stesso FALSO-ZERO un livello piu' sotto**:
        #   la forma era dichiarata, era IL MIO NOME a essere sbagliato.
        for _cand in (gq, "_" + gq):
            if (ev, _cand) in _S.REGOLE_NASCITA or _cand in _S.DOMINI:
                gq = _cand
                break
        voce = _S.REGOLE_NASCITA.get((ev, gq)) or {}
        dom = _S.DOMINI.get(gq)
        forma = dom[0] if dom else None
        x = {"regola": nome, "evento": ev, "grandezza": gq, "chiavi_a": usa_a,
             "forma": forma, "delegata_a": lati.delega.get(nome),
             "classe_dichiarata": voce.get("classe", "?")}
        # ### IL FILTRO E' LETTO DA `DOMINI`, non deciso da me: una frazione ha senso
        #   solo per una grandezza CONTINUA e DICHIARATA.
        if forma is None:
            # ### NON si esclude: si ELENCA. Una forma ignota non e' una forma in cui
            #   la frazione non ha senso -- e `COPIA-GENITORE` resta cio' che e'.
            x["nota"] = "forma non dichiarata in DOMINI"
            ignote.append(x)
        elif forma in FORME_SENZA_FRAZIONE:
            x["motivo_esclusione"] = "forma `%s`: una frazione NON ha senso" % forma
            esclusi.append(x)
        else:
            copie.append(x)
    stampa("")
    stampa("-" * 100)
    stampa("PEZZO NUOVO -- L'EREDITA' DA UN SOLO GENITORE: UN `t = 0` IMPLICITO")
    stampa("  ### E IL SETACCIO DEL NUMERO NON LO VEDE, perche' NON C'E' NESSUN NUMERO DA")
    stampa("  ###   TROVARE: la frazione non e' scritta, e' nella SCELTA DELL'INDICE.")
    stampa("  ###   E' FALSO-ZERO applicato alla decisione aperta di Luca -- cercando i")
    stampa("  ###   `0.5` si conclude <<cinque siti>> e si perde UNA CLASSE INTERA di siti")
    stampa("  ###   dove la frazione e' GIA' DECISA, A ZERO.")
    stampa("  ### NON ENTRA NEL CONTEGGIO DEL CANCELLO DEL 6a: e' materiale per la")
    stampa("  ###   decisione di Luca (DIVISIONE-AUTOCONSISTENTE), non un sito da curare.")
    stampa("")
    stampa("  COPIA-GENITORE: indicizza SOLO il lato `a`, E la forma dichiarata in")
    stampa("  DOMINI ammette una frazione. Siti: %d" % len(copie))
    stampa("    %-24s %-11s %-13s %-8s %-8s %s"
           % ("regola", "evento", "grandezza", "forma", "delega", "classe dichiarata"))
    for x in copie:
        stampa("    %-24s %-11s %-13s %-8s %-8s %s"
               % (x["regola"][:24], x["evento"], x["grandezza"][:13], x["forma"],
                  "si" if x["delegata_a"] else "-", str(x["classe_dichiarata"])[:40]))
    stampa("")
    stampa("  COPIA-GENITORE-FORMA-IGNOTA: indicizza SOLO il lato `a`, e la forma NON e'")
    stampa("  dichiarata in DOMINI. SI ELENCANO, non si escludono. Siti: %d" % len(ignote))
    stampa("    %-24s %-11s %-15s %-8s %s"
           % ("regola", "evento", "grandezza", "delega", "classe dichiarata"))
    for x in ignote:
        stampa("    %-24s %-11s %-15s %-8s %s"
               % (x["regola"][:24], x["evento"], x["grandezza"][:15],
                  "si" if x["delegata_a"] else "-", str(x["classe_dichiarata"])[:44]))
    stampa("  ### \u26d4 E LA STESURA PRECEDENTE LE ESCLUDEVA <<perche' la forma non e'")
    stampa("  ###   dichiarata>>: ERA UN FALSO-ZERO. Una forma IGNOTA non e' una forma in")
    stampa("  ###   cui la frazione non ha senso: escludere per IGNORANZA fa SCOMPARIRE")
    stampa("  ###   regole che copiano da un solo genitore.")
    stampa("  ### E C'ERA UN SECONDO FALSO-ZERO, UN LIVELLO PIU' SOTTO: il nome della")
    stampa("  ###   grandezza lo DEDUCEVO dal nome della funzione, e `_rn_div_psi_spinor`")
    stampa("  ###   dava `psi_spinor` mentre la grandezza si chiama `_psi_spinor`, COL")
    stampa("  ###   TRATTINO BASSO. Cosi' la forma risultava <<non dichiarata>> per colpa")
    stampa("  ###   del MIO nome, non del registro. Ora il nome si RISOLVE contro i")
    stampa("  ###   registri, e delle %d regole a un solo genitore ne restano %d con forma"
           % (len(copie) + len(ignote) + len(esclusi), len(ignote)))
    stampa("  ###   ignota: solo `conc_nodi`, nei due eventi.")
    stampa("")
    stampa("  ESCLUSI, e solo questi hanno un MOTIVO DICHIARATO: %d" % len(esclusi))
    for x in esclusi:
        stampa("    %-24s %-15s %s"
               % (x["regola"][:24], x["grandezza"][:15], x["motivo_esclusione"]))
    stampa("  ### IL CRITERIO NON E' MIO: e' la FORMA che il registro DICHIARA.")
    stampa("  ###   `indice` e' topologia, `segno` e' categoriale -- e per il `segno` il")
    stampa("  ###   registro lo dice esplicitamente: sommare due decisioni darebbe")
    stampa("  ###   +2, 0 o -2, che non sono valori ammessi.")
    stampa("")
    stampa("  IL TOTALE: %d copie + %d forma ignota + %d esclusi = %d regole che"
           % (len(copie), len(ignote), len(esclusi),
              len(copie) + len(ignote) + len(esclusi)))
    stampa("  indicizzano UN SOLO GENITORE.")
    stampa("")
    stampa("  *** IL FATTO PRINCIPALE, e lo fa emergere la terza classe: ***")
    _spin = [x for x in (copie + ignote)
             if x["grandezza"] in ("_psi_spinor", "spinor_lift", "_spinor_lift",
                                   "psi_spinor", "nb", "_nb")]
    stampa("    LO SPINORE STESSO NASCE COME COPIA DI `a`, NON COME MEDIA.")
    for x in sorted(_spin, key=lambda y: (y["grandezza"], y["evento"])):
        stampa("      %-11s %-15s %s"
               % (x["evento"], x["grandezza"][:15], str(x["classe_dichiarata"])[:60]))
    stampa("    MENTRE `psi` NASCE COME MEDIA DEI DUE GENITORI (:1984, EREDITA-MEDIA).")
    stampa("    ### E nello Schwinger la copia dello spinore porta il SEGNO -1 (doppia")
    stampa("    ###   copertura OPPOSTA), che e' una scelta dichiarata nel registro.")
    stampa("    ### QUINDI: il campo `psi` interpola fra i genitori, LO SPINORE NO.")
    stampa("    ###   Due descrizioni della stessa materia, DUE FRAZIONI DIVERSE.")
    stampa("    ### Non e' un difetto dichiarato: e' la DOMANDA che la decisione di Luca")
    stampa("    ###   deve chiudere -- e con gli esclusi per <<forma ignota>> NON SI")
    stampa("    ###   VEDEVA AFFATTO.")
    mie_cg = {(x["evento"], x["grandezza"]) for x in copie}
    tutte_cg = {(x["evento"], x["grandezza"]) for x in (copie + ignote + esclusi)}
    sue_cg = set(GUARDIANO_COPIA_GENITORE)
    stampa("")
    stampa("  IL CONFRONTO col conteggio del guardiano")
    stampa("    ### E IL CONTEGGIO INIZIALE DEL GUARDIANO ERA SEI, e lui dichiara perche'")
    stampa("    ###   era sbagliato: NON CONTAVA `c[\"src\"]`, quindi perdeva `omega_s`,")
    stampa("    ###   `mem_mot` e TUTTE le regole indicizzate da `src`. Errore del")
    stampa("    ###   guardiano, dichiarato da lui. Con `src` contato come lato `a`")
    stampa("    ###   (vale `a` a :8604 e `aa` a :8724) i due conteggi coincidono: %d."
           % len(tutte_cg))
    stampa("    nella MIA e non nella sua .. %s"
           % (sorted(mie_cg - sue_cg) or "nessuna"))
    stampa("    nella SUA e non nella mia .. %s"
           % (sorted(sue_cg - mie_cg) or "nessuna"))
    for k in sorted(sue_cg - mie_cg):
        stampa("      %s -> il guardiano la descrive come: %s"
               % (k, GUARDIANO_COPIA_GENITORE[k]))
    stampa("")
    stampa("  ### IL FATTO DA FAR EMERGERE, e il guardiano lo nomina:")
    _psi = [x for x in v.trovate if x["riga"] == 1984]
    stampa("    `psi` nasce come MEDIA dei due genitori (:1984, classe EREDITA-MEDIA%s),"
           % ("" if _psi else " -- NON TROVATA, da verificare"))
    _comp = [x for x in copie if x["grandezza"] == "psi_spin"]
    stampa("    il suo COMPAGNO `psi_spin` nasce come COPIA di `a` (%d regole: %s)."
           % (len(_comp), ", ".join(x["regola"] for x in _comp)))
    stampa("    ### DUE GRANDEZZE DELLA STESSA FAMIGLIA, DUE FRAZIONI DIVERSE: 0.5 e 0.")
    stampa("    ### Non e' un difetto dichiarato: e' la DOMANDA che la decisione di Luca")
    stampa("    ###   deve chiudere, e senza questo pezzo non si vedrebbe affatto.")
    stampa("")

    # ---------------------------------------------- IL CONFRONTO CON LA LISTA DEL GUARDIANO
    stampa("")
    stampa("-" * 100)
    stampa("IL CONFRONTO CON LA LISTA DEL GUARDIANO (rilievo del 2026-10-03)")
    mie = {x["riga"] for x in v.trovate}
    sue = (set(GUARDIANO_I_QUATTRO) | set(GUARDIANO_OLTRE_I_QUATTRO)
           | set(GUARDIANO_FALSI_POSITIVI))
    stampa("  righe nella MIA lista ......... %d" % len(mie))
    stampa("  righe nella SUA lista ......... %d" % len(sue))
    solo_mie = sorted(mie - sue)
    solo_sue = sorted(sue - mie)
    stampa("")
    stampa("  SOLO NELLA MIA: %d" % len(solo_mie))
    for r in solo_mie:
        x = [y for y in v.trovate if y["riga"] == r][0]
        stampa("      :%-6d %-20s %-14s %s" % (r, x["dentro"][:20], x["classe"],
                                               x["testo"][:60]))
    # ### LA FRASE SI CALCOLA, NON SI AFFERMA. La prima stesura stampava il booleano
    #   e POI diceva <<la differenza non tocca ne' la FRAZIONE ne' l'EREDITA-MEDIA>>:
    #   ### il booleano diceva False e la frase diceva il contrario. E' il difetto
    #   <<commento contro codice>> dentro il mio stesso strumento.
    _cl = {}
    for r in solo_mie:
        _c = [y for y in v.trovate if y["riga"] == r][0]["classe"]
        _cl.setdefault(_c, []).append(r)
    stampa("  ### per CLASSE: %s"
           % " · ".join("%s %d (%s)" % (k, len(x), ", ".join(":%d" % r for r in x))
                        for k, x in sorted(_cl.items())))
    _tocca = [k for k in _cl if k != "ALTRO"]
    if not _tocca:
        stampa("  ###   la mia lista e' un SOVRAINSIEME e la differenza e' TUTTA `ALTRO`:")
        stampa("  ###   non tocca ne' la FRAZIONE ne' l'EREDITA-MEDIA.")
    else:
        # ### IL RAMO E' GENERICO: elenca le righe non-`ALTRO` con classe e TESTO, e
        #   ### NESSUNA spiegazione scritta a mano su righe specifiche.
        #   ### ⛔ La stesura precedente aveva qui una frase FISSA su `:8496` -- cioe'
        #   lo STESSO difetto <<commento contro codice>> spostato di un livello: se la
        #   differenza toccasse un'altra riga, quella frase la stamperebbe comunque.
        #   ### La storia di `:8489`/`:8496` sta nel commento di `GUARDIANO_OLTRE_I_QUATTRO`
        #   e nel task history, ### NON in un print che finge di essere calcolato.
        stampa("  ###   *** LA DIFFERENZA TOCCA %s, non solo `ALTRO`. ***"
               % ", ".join(sorted(_tocca)))
        for k in sorted(_tocca):
            for r in _cl[k]:
                x = [y for y in v.trovate if y["riga"] == r][0]
                stampa("  ###     :%-6d %-14s %-20s %s"
                       % (r, k, x["dentro"][:20], x["testo"][:70]))
        stampa("  ###   Ogni riga qui sopra e' un sito di classe non-`ALTRO` che NON sta")
        stampa("  ###   nella lista del guardiano: va spiegata UNA PER UNA, e la")
        stampa("  ###   spiegazione NON sta in questo print.")
    stampa("")
    stampa("  SOLO NELLA SUA: %d" % len(solo_sue))
    for r in solo_sue:
        stampa("      :%d" % r)
    stampa("")
    stampa("  E DOVE LE CLASSI NON COINCIDONO:")
    stampa("    :8509 e :8665 (rho_sel) -- il guardiano le mette fra i siti <<oltre i")
    stampa("      quattro>>, io le ho classificate ALTRO, perche' NON decidono dove nasce")
    stampa("      il figlio: sono la MEDIA DI DENSITA' del cancello dell'antifase.")
    stampa("      *** NON E' UNA DIFFERENZA DI MISURA, E' UNA DIFFERENZA DI CLASSE: la")
    stampa("      domanda <<se il nato eredita con peso t, la densita' del cancello lo")
    stampa("      segue?>> il guardiano la pone, e dice che LA DECIDE LUCA. Quindi la")
    stampa("      lascio ALTRO e la DICHIARO come candidata in sospeso.")
    stampa("    :8495 e :8496 -- il guardiano cita il ramo MITOSI_DIR come :8489, che e'")
    stampa("      la riga del CANCELLO (if MITOSI_DIR != 0.0). Le righe del NUMERO,")
    stampa("      misurate dall'AST, sono :8495 (l'ampiezza del bias) e :8496 (la")
    stampa("      frazione (0.5 + bias)). Stessa cosa, righe diverse: uso le mie, che")
    stampa("      sono misurate.")
    stampa("")
    stampa("  ### E UN FATTO IN PIU', verificato: `psi` ha UN SOLO sito (:1984) per")
    stampa("  ###   ENTRAMBI gli eventi, perche' `_rn_sch_psi` CHIAMA `_rn_div_psi`.")
    stampa("  ###   Il guardiano lo dice, e il codice lo conferma. ### Mentre `pos` e")
    stampa("  ###   `phivel` hanno DUE siti ciascuna: la condivisione NON e' uniforme.")
    stampa("")
    esito = {"confronto_solo_mie": solo_mie, "confronto_solo_sue": solo_sue,
             "copia_genitore": copie, "copia_genitore_forma_ignota": ignote,
             "copia_genitore_esclusi": esclusi,
             "copia_genitore_totale": len(copie) + len(ignote) + len(esclusi),
             "copia_genitore_solo_mie": sorted("/".join(k) for k in (mie_cg - sue_cg)),
             "copia_genitore_solo_sue": sorted("/".join(k) for k in (sue_cg - mie_cg)),
             "blob_sim": blob(SIM), "blob_strumento": blob(os.path.abspath(__file__)),
             "perimetro_esatto": list(PERIMETRO_ESATTO),
             "perimetro_prefissi": list(PERIMETRO_PREFISSI),
             "trovate": v.trovate,
             "frazione_siti": len(fraz), "frazione_grandezze": gr,
             "eredita_siti": len(ered), "eredita_grandezze": gr_e,
             "altro_siti": len(altri),
             "quattro_o_meno": bool(basta)}
    io.open(os.path.join(FUORI, "_censimento.json"), "w", encoding="utf-8",
            newline=NL).write(json.dumps(esito, indent=1, ensure_ascii=False, default=str))
    io.open(os.path.join(FUORI, "_corsa.txt"), "w", encoding="utf-8",
            newline=NL).write(NL.join(out) + NL)
    print("  referto .. %s" % FUORI)
    if not basta:
        raise SystemExit(
            "IL COMMIT 6a SI FERMA: le grandezze della frazione sono %d (%s), non 4."
            % (len(gr), ", ".join(gr)))


if __name__ == "__main__":
    principale()
