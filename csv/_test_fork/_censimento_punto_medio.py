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
import hashlib
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
    stampa("  ### e sono TUTTE di classe ALTRO: %s"
           % all(([y for y in v.trovate if y["riga"] == r][0]["classe"] == "ALTRO")
                 for r in solo_mie))
    stampa("  ###   cioe' la mia lista e' un SOVRAINSIEME, e la differenza non tocca")
    stampa("  ###   ne' la FRAZIONE ne' l'EREDITA-MEDIA.")
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
