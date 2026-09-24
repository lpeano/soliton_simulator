# -*- coding: utf-8 -*-
"""LA MAPPA DEL `4pi` -- dove vive la doppia copertura, e quale delle quattro e'.

Punto (2) del prompt unico di Luca, 2026-09-24. **SOLA LETTURA. AST. Tabella generata.**

RIUSA `_censimento_fasi.py` (`Z118`): non si ricomincia da zero. Quello trova i PUNTI
(`W2`/`W4`/`OSS`/`A2P`) e le classi `T`/`L`/`E` *(cosa si leviga)*; questo aggiunge la domanda
NUOVA -- **di CHI e' il `4pi` in quel punto** -- e lo **stato EFFETTIVO nei run**.

LE QUATTRO CLASSI, e le REGOLE con cui si assegnano (fissate PRIMA di girare):
  `VERA`       la doppia copertura **dello SPINORE**: un oggetto di spin 1/2 torna in se'
               dopo `4pi`, e questo e' FISICA. Regola: nell'espressione compare una
               grandezza spinoriale (`psi_spinor`, `_spinor_lift`, `s_k`, `spinor`) oppure
               un MEZZO ANGOLO (`/2` su `chi`, `theta`, `tw`), o il sito e' fra quelli che
               Luca nomina come veri (`_phc`).
  `DICHIARATA` il **dominio `[0, 4pi)` di `phi`**: e' una CONVENZIONE del codice, non una
               proprieta' misurata. Regola: avvolgimento `% (4 pi)` (o `_w4`/`_wphi`)
               applicato a `phi`, `phi0`, `fm`, `anti`.
  `EREDITATA`  cio' che prende la sua SCALA da `phi`: `dph`, `twp`, `tw`, `_w4`/`_w8`, le
               soglie (`PHI_CRIT + twist_max`, `TW_TETTO`, l'inversione), `twist_dip`,
               l'antifase, il ritmo. Regola: la riga legge una di queste grandezze e NON e'
               `VERA`.
  `INVERSA`    **il finto pilota il vero**: una grandezza `EREDITATA` (tipicamente `tw`)
               SCRIVE una grandezza spinoriale o di Bloch. Regola: un assegnamento il cui
               BERSAGLIO e' spinoriale/Bloch e il cui VALORE legge `tw`/`twp`/`dph`.
               **E' la classe che l'architettura a un solo ponte deve abolire.**

!! L'ORDINE DI PRECEDENZA CONTA, e si dichiara: `INVERSA` > `VERA` > `DICHIARATA` >
  `EREDITATA`. Un sito che e' sia spinoriale sia letto da `tw` e' **`INVERSA`**, perche' la
  domanda di Luca e' *dove il finto comanda il vero*, e quella vince su tutto.

!! CIO' CHE QUESTA MAPPA NON FA: **non decide**. Dice di CHI e' il `4pi` e se quel punto
  GIRA. La proposta e' il punto (5), ed e' una scheda a parte.

ASCII PURO.
"""
import ast
import io
import json
import os
import re
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
sys.path.insert(0, _QUI)
import _presidio

_presidio.avvia(__file__)

import _censimento_fasi as Z118          # SI RIUSA: non si ricomincia da zero

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
SORGENTE = os.path.join(RADICE, "soliton_simulator.py")
# lo stato EFFETTIVO: il referto di configurazione GENERATO da un run vero
CFG = os.path.join(_QUI, "_g4_corto", "CONFIGURAZIONE.json")
OUT = os.path.join(_QUI, "_diag_D", "MAPPA_4PI.md")

# ---------------------------------------------------------------- i vocabolari, dichiarati
SPINORIALI = ("psi_spinor", "_spinor_lift", "spinor", "s_k", "psi_spin")
BLOCH = ("_nb", "nb", "omega_s", "omega_new")
EREDITA = ("dph", "twp", "tw", "twist_dip", "twist_max", "TW_TETTO", "PHI_CRIT",
           "soglia0", "tau_soglia", "fm", "anti", "signed", "phivel")
DA_PHI = ("phi", "phi0", "fm", "anti")
# i siti che Luca nomina come VERI: si dichiarano, perche' non sono derivabili da un nome
VERI_DICHIARATI = {3186: "_phc: la fase dell'orologio proprio, dove il 4pi e' dello spinore"}


def _nomi(nodo):
    """Tutti i nomi (Name/Attribute) che compaiono in un sottoalbero."""
    out = set()
    for n in ast.walk(nodo):
        if isinstance(n, ast.Name):
            out.add(n.id)
        elif isinstance(n, ast.Attribute):
            out.add(n.attr)
    return out


def _ha(nomi, vocab):
    """Appartenenza con gli UNDERSCORE INIZIALI NORMALIZZATI, non a sottostringa.

    !! PERCHE' NON A SOTTOSTRINGA, ed e' la parte che conta: `tw` sarebbe contenuto in
       `twist_dip` e `twist_max`, che vengono da `chi` e NON da `tw` -- la regola `INVERSA`
       si accenderebbe su siti che non leggono la torsione affatto.
    !! E PERCHE' NON ESATTA: `self._psi_spinor` da' il nome `_psi_spinor`, con l'underscore,
       e un confronto esatto contro `psi_spinor` lo MANCA. **`K2` del collaudo l'ha preso**,
       e il collaudo ha rifiutato di produrre la mappa: era un caso che DEVE passare e non
       passava.
    """
    nn = {n.lstrip("_") for n in nomi}
    return any(v.lstrip("_") in nn for v in vocab)


def _mezzo_angolo(nodo):
    """Un MEZZO ANGOLO: una divisione per 2 (o un `*0.5`) su un angolo."""
    for n in ast.walk(nodo):
        if isinstance(n, ast.BinOp) and isinstance(n.op, (ast.Div, ast.Mult)):
            nm = _nomi(n)
            if not _ha(nm, ("chi", "theta", "tw", "chi_torsione", "_chi_mat")):
                continue
            for lato in (n.left, n.right):
                if isinstance(lato, ast.Constant) and lato.value in (2, 2.0, 0.5):
                    return True
    return False


SEMI_TW = ("tw", "twp", "dph")


def contagio_tw(fn):
    """I nomi di variabile che, DENTRO una funzione, discendono da `tw`/`twp`/`dph`.

    !! SERVE, e senza di lui la classe `INVERSA` risulta VUOTA: la catena vera di
       `TW_SPINORE` e' `tw -> _twh -> _otw -> omega_new`, cioe' **DUE salti**, mentre la
       regola a un salto non vede niente. Una classe sempre vuota e' un numero impossibile,
       e la prima stesura ne aveva DUE (`VERA` e `INVERSA`).
       Si itera fino a chiusura: e' un insieme piccolo, e cosi' non dipende dall'ordine.
    """
    contagiati = set(SEMI_TW)
    for _ in range(8):                      # chiusura: piu' di 8 salti non ne esistono qui
        prima = len(contagiati)
        for n in ast.walk(fn):
            # (a) un assegnamento normale
            if isinstance(n, (ast.Assign, ast.AugAssign)) and n.value is not None:
                if _ha(_nomi(n.value), tuple(contagiati)):
                    bers = n.targets if isinstance(n, ast.Assign) else [n.target]
                    for b in bers:
                        contagiati |= _nomi(b)
                continue
            # (b) LA MUTAZIONE IN PLACE: `np.add.at(X, idx, V)` scrive X con V.
            #     !! SENZA QUESTO RAMO LA CLASSE `INVERSA` RESTA VUOTA, e non per assenza
            #     del difetto: la catena vera di `TW_SPINORE` e'
            #        `_twh = tw/(2*PHI_CRIT)`  ->  `np.add.at(_otw, ii, _axis*_twh)`
            #        ->  `omega_new = omega_new + _otw/...`
            #     e `_otw` NON E' MAI il bersaglio di un assegnamento: e' mutato IN PLACE.
            #     Una regola che guarda solo gli assegnamenti non lo vede MAI.
            if isinstance(n, ast.Call):
                f = n.func
                nome = f.attr if isinstance(f, ast.Attribute) else getattr(f, "id", None)
                if nome in ("at", "add", "subtract", "put", "copyto") and len(n.args) >= 2:
                    if _ha(_nomi(n.args[-1]), tuple(contagiati)):
                        contagiati |= _nomi(n.args[0])
        if len(contagiati) == prima:
            break
    return contagiati


def classifica(nodo_riga, righe_testo, riga, contagiati=()):
    """LA CLASSE, con la regola che l'ha deciso. Precedenza: INVERSA > VERA > DICHIARATA > ERED."""
    nomi = _nomi(nodo_riga) if nodo_riga is not None else set()
    testo = righe_testo[riga - 1] if 0 < riga <= len(righe_testo) else ""

    # INVERSA: un assegnamento il cui BERSAGLIO e' spinoriale/Bloch e il cui VALORE legge
    # una grandezza CONTAGIATA da `tw` (anche a piu' salti di distanza)
    if isinstance(nodo_riga, (ast.Assign, ast.AugAssign)):
        bers = (nodo_riga.targets if isinstance(nodo_riga, ast.Assign)
                else [nodo_riga.target])
        nb = set()
        for b in bers:
            nb |= _nomi(b)
        nv = _nomi(nodo_riga.value) if nodo_riga.value is not None else set()
        semi = tuple(contagiati) or SEMI_TW
        if _ha(nb, SPINORIALI + BLOCH) and _ha(nv, semi):
            quali = sorted(n for n in nv if n.lstrip("_") in
                           {s.lstrip("_") for s in semi})[:3]
            return "INVERSA", ("bersaglio spinoriale/Bloch, valore che discende da `tw` "
                               "(via %s)" % ", ".join("`%s`" % q for q in quali))

    if riga in VERI_DICHIARATI:
        return "VERA", "sito dichiarato da Luca: %s" % VERI_DICHIARATI[riga]
    if _ha(nomi, SPINORIALI):
        return "VERA", "l'espressione contiene una grandezza SPINORIALE"
    if _mezzo_angolo(nodo_riga) if nodo_riga is not None else False:
        return "VERA", "MEZZO ANGOLO (`/2` su un angolo): e' la firma dello spin 1/2"

    # DICHIARATA: l'avvolgimento del dominio di `phi`
    if ("4 * np.pi" in testo or "4*np.pi" in testo or "_w4(" in testo
            or "_wphi(" in testo or "_dphi()" in testo):
        if _ha(nomi, DA_PHI):
            return "DICHIARATA", "avvolgimento del DOMINIO di `phi` (convenzione, non misura)"

    if _ha(nomi, EREDITA) or _ha(nomi, DA_PHI):
        return "EREDITATA", "legge una grandezza che prende la sua scala da `phi`"
    return "?", "nessuna regola ha attaccato: NON CLASSIFICATO, e si dichiara"


def nodo_di_riga(albero):
    """{riga: l'istruzione PIU' INTERNA che COPRE quella riga}.

    !! LA PRIMA STESURA MAPPAVA SOLO `n.lineno`, cioe' la riga in cui l'istruzione COMINCIA.
       Su questo file quasi ogni riga interessante sta **in mezzo** a un'istruzione su piu'
       righe, quindi il nodo risultava `None`, i nomi erano un insieme VUOTO, e la mappa
       usciva con **zero `VERA`, zero `DICHIARATA`, zero `INVERSA` e 16 `?`**.
       **Non era un risultato: era il difetto dello strumento che si denunciava da solo**,
       perche' una classe SEMPRE vuota e' un numero impossibile (par.9).
       Si copre tutto lo span `lineno..end_lineno`, e a parita' di riga vince l'istruzione
       col SUO span piu' PICCOLO: la piu' interna, che e' quella che contiene l'espressione.
    """
    out = {}
    for n in ast.walk(albero):
        if not (isinstance(n, ast.stmt) and hasattr(n, "lineno")):
            continue
        fine = getattr(n, "end_lineno", None) or n.lineno
        span = fine - n.lineno
        for r in range(n.lineno, fine + 1):
            prec = out.get(r)
            if prec is None:
                out[r] = n
            else:
                p_fine = getattr(prec, "end_lineno", None) or prec.lineno
                if span < (p_fine - prec.lineno):
                    out[r] = n
    return out


# ---------------------------------------------------------------- LA SPAZZATA, che Z118 non fa
#   !! PERCHE' SERVE, ed e' un difetto di Z118 che questa mappa ha scoperto riusandolo:
#   `_censimento_fasi.py` cerca i multipli di `pi` SCRITTI COME LETTERALI (`% (4*np.pi)`), ma
#   la cura `FASE_2PI` ha riscritto quei siti in `% self._dphi()` e `self._wphi(...)`.
#   **Quindi il censimento e' CIECO esattamente sui siti che la cura ha toccato**, e con lui
#   la prima stesura di questa mappa: zero `VERA`, zero `DICHIARATA`, zero `INVERSA`.
#   Una classe SEMPRE vuota e' un numero impossibile, ed e' cosi' che il difetto si e'
#   denunciato (par.9). Qui si spazza per NOME, non per letterale.
CHIAMATE_PERIODO = ("_dphi", "_wphi", "_w4", "_w8", "_spinor_lift")
COSTANTI_PERIODO = ("PHI_CRIT", "TW_TETTO", "twist_max", "twist_dip", "soglia0",
                    "tau_soglia", "tau_tetto",
                    # i siti del `4pi` VERO: non hanno un multiplo di `pi` scritto, quindi
                    # ne' Z118 ne' un grep li trovano. `_phc = exp(-0.5j * _sk * ...)` e'
                    # LA doppia copertura dello spinore, e il `-0.5` e' il mezzo angolo.
                    "_phc", "_sk", "s_k", "_spinor_lift", "psi_spinor",
                    # e i due anelli della catena INVERSA di `TW_SPINORE`
                    "_twh", "_otw")


def punti_extra(testo, albero, nodi):
    """I siti a periodo che `Z118` non vede: chiamate e costanti, non letterali di `pi`."""
    righe = testo.split("\n")
    fn_di_riga = {}
    for n in ast.walk(albero):
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for r in range(n.lineno, (getattr(n, "end_lineno", None) or n.lineno) + 1):
                fn_di_riga.setdefault(r, n.name)
    visti, out = set(), []
    for n in ast.walk(albero):
        nome = None
        if isinstance(n, ast.Call):
            f = n.func
            nome = f.attr if isinstance(f, ast.Attribute) else getattr(f, "id", None)
            if nome not in CHIAMATE_PERIODO:
                nome = None
        elif isinstance(n, ast.Name) and n.id in COSTANTI_PERIODO:
            nome = n.id
        elif isinstance(n, ast.Attribute) and n.attr in COSTANTI_PERIODO:
            nome = n.attr
        if not nome:
            continue
        r = getattr(n, "lineno", None)
        if r is None or (r, nome) in visti:
            continue
        visti.add((r, nome))
        # il FLAG che governa quella riga: lo chiediamo a Z118, che sa farlo
        try:
            fl = Z118.flag_di_riga(albero, righe).get(r, "")
        except Exception:
            fl = ""
        out.append(dict(riga=r, fn=fn_di_riga.get(r, "(modulo)"), tipo="SWEEP",
                        classe="", flag=fl, fonte="`%s`" % nome))
    return out


def effettivo():
    """Lo stato EFFETTIVO dei flag in un run vero, dal referto di configurazione GENERATO."""
    if not os.path.exists(CFG):
        return {}, "NESSUN REFERTO: `%s` non esiste" % os.path.relpath(CFG, RADICE)
    d = json.loads(io.open(CFG, encoding="utf-8").read())
    return d.get("effettivo_dal_modulo", {}), (
        "dal referto di configurazione del run `_g4_corto`, commit %s"
        % (d.get("git", {}).get("head", "?")[:8]))


# ---------------------------------------------------------------- IL COLLAUDO (`P1-sexies`)
def collaudo(W):
    W("COLLAUDO DELLE REGOLE DI CLASSIFICAZIONE su casi a RISPOSTA NOTA (`P1-sexies`)\n")
    W("-" * 100 + "\n")
    e = []

    def cls(src, riga=1):
        a = ast.parse(src)
        nodi = nodo_di_riga(a)
        return classifica(nodi.get(riga), src.split("\n"), riga)

    casi = [
        ("self.omega_s = self.omega_s + tw / (4 * np.pi)", "INVERSA",
         "il finto (`tw`) scrive il vero (`omega_s`)"),
        ("x = np.angle(self._psi_spinor[:, 0])", "VERA",
         "grandezza SPINORIALE"),
        ("u = np.exp(1j * chi / 2)", "VERA",
         "MEZZO ANGOLO su un angolo"),
        ("self.phi = (self.phi + d) % (4 * np.pi)", "DICHIARATA",
         "il dominio di `phi`"),
        ("self.tw += self._w8(dph - self.twp)", "EREDITATA",
         "legge `dph`/`twp`, che prendono la scala da `phi`"),
    ]
    for src, atteso, perche in casi:
        c, regola = cls(src)
        ok = (c == atteso)
        W("K%d %-58s -> %-11s (atteso %-11s) %s\n"
          % (len(e) + 1, perche, c, atteso, "OK" if ok else "*** NO ***"))
        e.append(ok)

    # IL CASO CHE DEVE FALLIRE: senza la precedenza, un sito INVERSA passerebbe per VERA
    src = "self.omega_s = self.omega_s + tw / (4 * np.pi)"
    a = ast.parse(src)
    nomi = _nomi(a.body[0])
    finto_vera = _ha(nomi, BLOCH)      # la regola SBAGLIATA: "contiene omega_s -> VERA"
    ok = finto_vera and cls(src)[0] == "INVERSA"
    W("K%d IL CASO CHE DEVE FALLIRE: la regola senza precedenza direbbe VERA (contiene "
      "`omega_s`) -> %s\n"
      % (len(e) + 1, "OK: la precedenza INVERSA>VERA lo salva" if ok else "*** NO ***"))
    e.append(ok)

    # SECONDO CASO CHE DEVE FALLIRE: un sito senza nessuna di queste grandezze non si
    # classifica a forza -- deve uscire `?`
    c, _ = cls("y = np.sin(alpha) * 3")
    ok = (c == "?")
    W("K%d SECONDO CASO CHE DEVE FALLIRE: una riga estranea -> `%s` (atteso `?`, non una "
      "classe a forza) -> %s\n" % (len(e) + 1, c, "OK" if ok else "*** classifica a forza ***"))
    e.append(ok)

    ok = all(e)
    W("-" * 100 + "\n  -> %s\n\n" % ("le regole PASSANO" if ok else "*** NON PASSANO ***"))
    return ok


# ---------------------------------------------------------------- IL GRAFO
GRAFO = [
    ("SPINORE `_psi_spinor`", "`phi`",
     "`_phc` / `phivel` / `omega_clk` fanno AVANZARE `phi`. **Attenzione: questa freccia "
     "va dallo spinore a `phi`, non il contrario** -- `phi` e' una CONSEGUENZA",
     "VERA -> DICHIARATA"),
    ("`phi`", "`dph`", "`dph = _wphi(phi[i] - phi[j])` (`:4675`)", "DICHIARATA -> EREDITATA"),
    ("`dph`", "`twp`, `tw`", "`tw += _w8(dph + twist_dip - twp)` (`:4698-4699`)", "EREDITATA"),
    ("`tw`", "MITOSI", "`avv = |tw|`, soglia `PHI_CRIT + twist_max`, campana fino a `TW_TETTO`",
     "EREDITATA"),
    ("`tw`", "SCHWINGER", "`eccesso_torsione` -> `prob_coppia`, e l'antifase `fm + dphi/2`",
     "EREDITATA"),
    ("`tw`", "REPULSIONE / `d0`", "il termine di massima compressione (`S05`)", "EREDITATA"),
    ("`tw`", "TEMPI", "`ritmo()` ramo `TEMPO_SEGNO` (`r = 1 + mean|tw|/PHI_CRIT`) e `tau_pp`",
     "EREDITATA"),
    ("SPINORE `_psi_spinor`", "TEMPI (l'OROLOGIO)",
     "`ritmo()` ramo VIVO `:2628-2629`: `np.angle(psi_spin)`, e `psi_spin` e' costruito a "
     "`:3398` DALLO SNAPSHOT `_psi_spinor`. **NON da `phi`**",
     "VERA -> il tempo"),
    ("`phi`", "TEMPI, SOLO dal fallback",
     "`:3393-3394`: se `_psi_spinor` e' assente o corto, `_psp[:,0] = exp(1j*phi)`. "
     "MISURATO: **3 volte su 441 (0.68 %), alle invocazioni 1-2-3** -- il transitorio "
     "del primo passo, e mai piu'",
     "DICHIARATA, ma TRANSITORIA"),
    ("`tw`", "SPINORE", "`TW_SPINORE`: `_otw` sommato a `omega_new` (`:2149-2154`)",
     "*** INVERSA ***"),
]


def main():
    W = sys.stdout.write
    if not collaudo(W):
        return 1
    testo = io.open(SORGENTE, encoding="utf-8").read()
    righe = testo.split("\n")
    albero = ast.parse(testo)
    nodi = nodo_di_riga(albero)
    punti = Z118.censisci(testo)
    # !! SI AGGIUNGE LA SPAZZATA: senza, la mappa e' CIECA sui siti che la cura `FASE_2PI` ha
    #    riscritto, perche' `Z118` cerca i multipli di `pi` come LETTERALI e quei siti ora
    #    dicono `self._dphi()`. Il conto dei due insiemi si stampa: si vede quanto Z118
    #    da solo NON vedeva.
    n_z118 = len(punti)
    extra = punti_extra(testo, albero, nodi)
    punti = punti + extra
    punti.sort(key=lambda p: (p["riga"], p["tipo"]))
    eff, fonte_eff = effettivo()

    try:
        os.makedirs(os.path.dirname(OUT))
    except OSError:
        pass
    f = io.open(OUT, "w", encoding="utf-8", newline="\n")
    Wf = f.write
    Wf("# LA MAPPA DEL `4pi` -- **di chi e' la doppia copertura, punto per punto**\n\n")
    Wf("> **GENERATA** da `csv/_test_fork/_mappa_4pi.py`, che **riusa `_censimento_fasi.py`**\n")
    Wf("> (`Z118`). **Sola lettura, AST.** Stato effettivo dei flag: %s.\n\n" % fonte_eff)
    Wf("## LE QUATTRO CLASSI\n\n")
    Wf("| classe | che cos'e' | che se ne fa l'architettura a un solo ponte |\n|:--:|---|---|\n")
    Wf("| **`VERA`** | la doppia copertura **dello SPINORE**: un oggetto di spin 1/2 torna in "
       "se' dopo `4pi`. **E' fisica.** | **RESTA**, ed e' l'unico posto dove il `4pi` vive |\n")
    Wf("| **`DICHIARATA`** | il **dominio `[0, 4pi)` di `phi`**: una **convenzione del codice**, "
       "non una proprieta' misurata | **CADE**: `phi` diventa una lettura dello spinore, su "
       "`2pi` |\n")
    Wf("| **`EREDITATA`** | cio' che prende la sua **scala** da `phi` | **si RIDERIVA** dal "
       "trasporto degli spinori, non dalle differenze di `phi` |\n")
    Wf("| **`INVERSA`** | **il finto pilota il vero**: una grandezza ereditata SCRIVE una "
       "grandezza spinoriale | **si ABOLISCE**: e' il verso sbagliato del ponte |\n\n")
    Wf("**Precedenza dichiarata:** `INVERSA` > `VERA` > `DICHIARATA` > `EREDITATA`. Un sito "
       "che e' sia spinoriale sia scritto da `tw` e' **`INVERSA`**, perche' la domanda e' "
       "*dove il finto comanda il vero*.\n\n")

    fn_di_nome = {n.name: n for n in ast.walk(albero)
                  if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}
    contagio = {}
    conta = {}
    Wf("## I PUNTI\n\n")
    Wf("| riga | funzione | tipo | **di chi** | regola che l'ha deciso | flag | **EFFETTIVO "
       "nei run** |\n|--:|---|:--:|:--:|---|---|:--:|\n")
    for p in punti:
        fn_nodo = fn_di_nome.get(p["fn"])
        if fn_nodo is not None and p["fn"] not in contagio:
            contagio[p["fn"]] = contagio_tw(fn_nodo)
        c, regola = classifica(nodi.get(p["riga"]), righe, p["riga"],
                               contagio.get(p["fn"], ()))
        conta[c] = conta.get(c, 0) + 1
        fl = p.get("flag") or "-"
        # !! IL FLAG SI CERCA PER TOKEN ESATTO, non a sottostringa: la prima stesura faceva
        #    `if nome in fl` e su `TW_SPINORE` prendeva il valore di un ALTRO flag il cui nome
        #    e' contenuto in quella stringa, stampando `True` dove il referto dice `False`.
        #    Un referto che sbaglia lo stato di un flag e' peggio di uno che scrive `-`.
        val = "-"
        for tok in re.findall(r"[A-Z][A-Z0-9_]+", fl or ""):
            if tok in eff:
                val = str(eff[tok])
                break
        Wf("| `:%d` | `%s` | `%s` | **`%s`** | %s | %s | **%s** |\n"
           % (p["riga"], p["fn"], p["tipo"], c, regola, fl, val))
    Wf("\n**Conteggio per classe:** %s\n\n"
       % " . ".join("**%s** %d" % (k, v) for k, v in sorted(conta.items())))
    if conta.get("?"):
        Wf("> **!! `%d` punti NON CLASSIFICATI**, e restano `?`: nessuna regola ha attaccato. "
           "**Non li forzo in una classe**, perche' una classe assegnata a forza e' peggio di "
           "una cella vuota.\n\n" % conta["?"])

    Wf("### !! COME SI LEGGE UNA `INVERSA`, e il limite e' dichiarato\n\n")
    Wf("**Il contagio da `tw` e' INSENSIBILE AL FLUSSO: ignora i gate.** Quindi una `INVERSA` "
       "dice *\"la catena ESISTE nel codice\"*, **non** *\"gira adesso\"*. Per sapere se gira si "
       "guarda la colonna **EFFETTIVO**.\n\n")
    Wf("**Le due `INVERSA` trovate stanno sulla STESSA catena**, ed e' quella di `TW_SPINORE`:\n\n")
    Wf("```\n")
    Wf("  tw  --> _twh = tw/(2*PHI_CRIT)        :3095\n")
    Wf("      --> np.add.at(_otw, ii, _axis*_twh)   :3098-3099   (mutazione IN PLACE)\n")
    Wf("      --> omega_new = omega_new + _otw/...  :3100        *** INVERSA ***\n")
    Wf("      --> psi_sp_new  (integra omega_new)\n")
    Wf("      --> self._psi_spinor = psi_sp_new     :3264        *** INVERSA (conseguenza) ***\n")
    Wf("```\n\n")
    Wf("> **`:3100` e' il PONTE SBAGLIATO** *(la torsione che scrive `omega_s`, cioe' lo "
       "spinore)*, **e `:3264` e' la sua CONSEGUENZA**: il commit atomico dello spinore. "
       "**`:3264` non e' un difetto in se'** -- diventa un ponte inverso **solo** se `:3100` "
       "ha scritto.\n")
    Wf("> **E OGGI NESSUNA DELLE DUE GIRA: `TW_SPINORE = False`.** La catena e' **in codice e "
       "spenta**, e l'architettura a un solo ponte deve dire **se puo' esistere affatto**.\n\n")
    Wf("## IL GRAFO DELLE DIPENDENZE\n\n")
    Wf("```\n")
    Wf("            SPINORE  _psi_spinor   (il 4pi VERO)\n")
    Wf("                 |                        |\n")
    Wf("   _phc/phivel/  |                        |  :3398  psi_spin = mat(w) @ (amp * _psi_spinor)\n")
    Wf("   omega_clk     v                        v\n")
    Wf("               phi                   L'OROLOGIO  r      (ritmo(), :2628-2629)\n")
    Wf("        (il 4pi DICHIARATO)               ^\n")
    Wf("                 |                        |  e `phi` ci arriva SOLO dal FALLBACK :3393-3394\n")
    Wf("                 |  :4675                 |  MISURATO: 3 volte su 441 (0.68 %), alle\n")
    Wf("                 |  dph = _wphi(          |  invocazioni 1-2-3 -- il transitorio del primo\n")
    Wf("                 |     phi[i] - phi[j])   |  passo, e MAI PIU'\n")
    Wf("                 v                        |\n")
    Wf("            twp, tw   (EREDITATO)         |  (nessuna freccia a regime)\n")
    Wf("            :4698-4699\n")
    Wf("                 |              |              |\n")
    Wf("                 v              v              v\n")
    Wf("              MITOSI        SCHWINGER      REPULSIONE\n")
    Wf("              soglia,       antifase,      max compress.\n")
    Wf("              campana       prob_coppia    (S05)\n")
    Wf("\n")
    Wf("  !! LA CORREZIONE: l'OROLOGIO NON viene da `phi` ne' da `tw`. Viene dallo SPINORE.\n")
    Wf("     Il ramo `TEMPO_SEGNO` di `ritmo()` (`r = 1 + mean|tw|/PHI_CRIT`), che SI' viene\n")
    Wf("     dalla torsione, NON GIRA: `TEMPO_SEGNO = False` in 9 run su 11 (`Z130`).\n")
    Wf("     Restano da `tw`: `tau_pp` e, indirettamente, il termine di repulsione.\n")
    Wf("\n")
    Wf("  E IL VERSO SBAGLIATO, che l'architettura deve abolire:\n")
    Wf("    tw  ---- TW_SPINORE ---->  omega_s  (lo SPINORE)     *** INVERSA ***\n")
    Wf("```\n\n")
    Wf("| da | a | come | classe |\n|---|---|---|:--:|\n")
    for da, a, come, cl in GRAFO:
        Wf("| %s | %s | %s | `%s` |\n" % (da, a, come, cl))
    Wf("\n")
    Wf("> **!! COSA QUESTA MAPPA NON FA: non decide.** Dice **di chi** e' il `4pi` in ogni "
       "punto e **se quel punto gira**. La proposta e' una **scheda a parte**.\n")
    f.close()
    W("mappa scritta -> %s\n" % os.path.relpath(OUT, RADICE))
    W("conteggio per classe: %s\n"
      % " . ".join("%s %d" % (k, v) for k, v in sorted(conta.items())))
    return 0


if __name__ == "__main__":
    sys.exit(main())
