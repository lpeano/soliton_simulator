# -*- coding: utf-8 -*-
"""**IL PUNTO UNICO DI NASCITA SI PUO' SCRIVERE SENZA RIORDINARE? LA MISURA CHE DECIDE.**

**Passo 3 del `COMMIT 3`**, e si gira ### **prima di una riga di codice.** Il mio task history
*(`doc/TASK_HISTORY/2026-10-02_commit3-nascita-evento-unico.md`)* fissa come ### **punto di STOP
numero ④**:

> ### **il punto unico richiede di RIORDINARE le scritture** *(non solo di spostarle)* **⇒ STOP:
> riordinare CAMBIA LA FISICA**, ed e' cio' che `doc/MITOSI_non_si_spezza_per_tipo.md` ha gia'
> misurato una volta *(per il TIPO, nel 2026-09-28)*.

### ➜ **Questa misura dice se quel punto di STOP scatta, e lo dice con un NUMERO.**

---

## LA DOMANDA, scomposta in tre -- e la terza e' quella che decide

| # | la domanda | come si risponde |
|--:|---|---|
| **1** | **dove** stanno le scritture delle grandezze del registro, in **ordine di sorgente**? | AST di `mitosi`, piu' i due `_eredita_*` *(che scrivono anche loro, e dal punto di vista di `mitosi` ### **la CHIAMATA e' la scrittura**)* |
| **2** | quali istruzioni **NON di scrittura** stanno **FRA** la prima e l'ultima? | idem |
| ### **3** | ### **quante di quelle DEVONO restare dov'e' sono?** | ### **una DIPENDENZA**: l'istruzione **legge** qualcosa che una scrittura precedente produce, **oppure** produce qualcosa che una scrittura successiva **consuma** |

### ⭐ **IL CRITERIO, fissato PRIMA dei numeri**

> ### **Se esiste ANCHE UNA SOLA istruzione non-di-scrittura che DEVE stare fra due scritture,
> allora un blocco CONTIGUO richiede di RIORDINARE ⇒ STOP.**

### ⚠ **E il verso opposto vale pure, e va detto:** se le dipendenze sono **ZERO**, la misura
### **NON dice che il punto unico sia facile** -- dice che ### **non e' impedito da un riordino.**
Restano i contatori, i rami condizionali sulle lunghezze delle cache, e `conc_nodi` che cresce per
mutazione. ### **Questa misura risponde a UNA domanda, non a tutte.**

## ⛔ CIO' CHE QUESTA MISURA **NON** FA

* ### **non e' un sigillo:** non gira il simulatore, non confronta byte. E' un'**analisi
  strutturale**, e l'AST e' lo strumento giusto perche' la domanda e' ### **sull'ORDINE DEL
  SORGENTE**, che e' un fatto sintattico;
* ### **non vede i rami che non girano:** il blocco `MITOSI_DIR` e il ramo stocastico ### **sono
  nel sorgente** e quindi nell'analisi. Si riportano **separati**, col loro gate;
* ### **non sostituisce la lettura:** dice **quante** dipendenze e **quali**, e ### **la decisione
  su che cosa farne resta di Luca.**

COMANDO:  python csv/_test_fork/_punto_unico_fattibile.py
USCITA:   `csv/_test_fork/_punto_unico_fattibile/_punto_unico_fattibile.json` + `_corsa.txt`.
ASCII puro nel codice.
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

NL = chr(10)
SIM = os.path.join(RADICE, "soliton_simulator.py")
FUORI = os.path.join(RADICE, "csv", "_test_fork", "_punto_unico_fattibile")
# le funzioni che scrivono grandezze della nascita DA DENTRO `mitosi`: la loro CHIAMATA, dal punto
#   di vista di `mitosi`, E' una scrittura -- e quali grandezze si ricava dal loro AST, non da un
#   elenco scritto a mano.
SERVIZIO = ("_eredita_psi_figli", "_eredita_spinore_figli", "_grado", "_smp_chirurgia", "_nasce")


def blob(p):
    return hashlib.sha1(io.open(p, "rb").read()).hexdigest()


def registro_dal_sorgente(albero):
    """I nomi del registro, letti DALLE TABELLE del simulatore e non scritti a mano."""
    nomi = set()
    for n in ast.walk(albero):
        if isinstance(n, ast.Assign):
            for m in n.targets:
                if isinstance(m, ast.Name) and m.id in ("REGISTRO_STATO", "REGISTRO_DERIVATE",
                                                        "REGISTRO_METRI", "REGISTRO_FINESTRA"):
                    for e in ast.walk(n.value):
                        if isinstance(e, ast.Constant) and isinstance(e.value, str):
                            nomi.add(e.value)
    return nomi


def scritti_da(albero, nome, registro):
    """Le grandezze del registro che la funzione `nome` SCRIVE (su `self`)."""
    fuori = set()
    for n in ast.walk(albero):
        if isinstance(n, ast.FunctionDef) and n.name == nome:
            for x in ast.walk(n):
                if isinstance(x, (ast.Assign, ast.AugAssign)):
                    mire = x.targets if isinstance(x, ast.Assign) else [x.target]
                    for m in mire:
                        mm = m
                        while isinstance(mm, ast.Subscript):
                            mm = mm.value
                        if (isinstance(mm, ast.Attribute) and isinstance(mm.value, ast.Name)
                                and mm.value.id == "self" and mm.attr in registro):
                            fuori.add(mm.attr)
    return fuori


def nomi_letti(nodo):
    """`(self_attr_lette, locali_lette)` -- da tutti i `Load` dentro `nodo`."""
    sa, lo = set(), set()
    for x in ast.walk(nodo):
        if isinstance(x, ast.Attribute) and isinstance(x.value, ast.Name) and x.value.id == "self":
            if isinstance(x.ctx, ast.Load):
                sa.add(x.attr)
        elif isinstance(x, ast.Name) and isinstance(x.ctx, ast.Load) and x.id != "self":
            lo.add(x.id)
    return sa, lo


def nomi_scritti(nodo):
    """`(self_attr_scritte, locali_scritte)`."""
    sa, lo = set(), set()
    for x in ast.walk(nodo):
        if isinstance(x, (ast.Assign, ast.AugAssign, ast.AnnAssign)):
            mire = x.targets if isinstance(x, ast.Assign) else [x.target]
            for m in mire:
                mm = m
                while isinstance(mm, ast.Subscript):
                    mm = mm.value
                if (isinstance(mm, ast.Attribute) and isinstance(mm.value, ast.Name)
                        and mm.value.id == "self"):
                    sa.add(mm.attr)
                elif isinstance(mm, ast.Name):
                    lo.add(mm.id)
                elif isinstance(mm, (ast.Tuple, ast.List)):
                    for e in mm.elts:
                        if isinstance(e, ast.Name):
                            lo.add(e.id)
                        elif (isinstance(e, ast.Attribute) and isinstance(e.value, ast.Name)
                              and e.value.id == "self"):
                            sa.add(e.attr)
        elif isinstance(x, ast.For):
            for e in ast.walk(x.target):
                if isinstance(e, ast.Name):
                    lo.add(e.id)
    return sa, lo


def chiamate_di_servizio(nodo):
    return sorted({x.func.attr for x in ast.walk(nodo)
                   if isinstance(x, ast.Call) and isinstance(x.func, ast.Attribute)
                   and x.func.attr in SERVIZIO})


def gate_di(corpo, bersaglio):
    fuori = []

    def scendi(lista, cond):
        for x in lista:
            if x is bersaglio:
                fuori.append(list(cond))
                return True
            if isinstance(x, ast.If):
                if scendi(x.body, cond + [ast.unparse(x.test)]):
                    return True
                if scendi(x.orelse, cond + ["NOT (%s)" % ast.unparse(x.test)]):
                    return True
            elif isinstance(x, (ast.For, ast.While)):
                if scendi(x.body, cond + ["<ciclo> " + ast.unparse(x).split(NL)[0][:40]]):
                    return True
        return False
    scendi(corpo, [])
    return fuori[0] if fuori else []


def principale():
    if not os.path.isdir(FUORI):
        os.makedirs(FUORI)
    P = []

    def stampa(*x):
        r = " ".join(str(y) for y in x)
        P.append(r)
        print(r)

    src = io.open(SIM, encoding="utf-8").read()
    t = ast.parse(src)
    registro = registro_dal_sorgente(t)
    serv_scrive = {k: scritti_da(t, k, registro) for k in SERVIZIO}
    mit = next(n for n in ast.walk(t)
               if isinstance(n, ast.FunctionDef) and n.name == "mitosi")

    stampa("=" * 104)
    stampa("IL PUNTO UNICO DI NASCITA SI PUO' SCRIVERE SENZA RIORDINARE?  (passo 3 del COMMIT 3)")
    stampa("=" * 104)
    stampa("simulatore ..... %s" % blob(SIM)[:8])
    stampa("questo strumento %s" % blob(os.path.abspath(__file__))[:8])
    stampa("`mitosi` :%d -> :%d  (%d righe)" % (mit.lineno, mit.end_lineno,
                                                mit.end_lineno - mit.lineno + 1))
    stampa("grandezze del registro, DALLE TABELLE del simulatore: %d" % len(registro))
    for k in SERVIZIO:
        stampa("  `%s` scrive %d grandezze del registro: %s"
               % (k, len(serv_scrive[k]), ", ".join(sorted(serv_scrive[k])) or "(nessuna)"))
    stampa("")

    # --- le istruzioni di PRIMO LIVELLO, in ordine, con cio' che leggono e scrivono -----------
    def appiattisci(lista):
        """Le istruzioni, in ordine di sorgente, SCENDENDO dentro gli `if` e i cicli.

        ### Si scende di proposito: una scrittura dentro `if COPPIA_MIT > 0.0` E' una scrittura
        della nascita, e trattare quel blocco come UNA istruzione nasconderebbe la domanda.
        """
        fuori = []
        for x in lista:
            if isinstance(x, ast.If):
                fuori += appiattisci(x.body) + appiattisci(x.orelse)
            elif isinstance(x, (ast.For, ast.While)):
                fuori += appiattisci(x.body)
            else:
                fuori.append(x)
        return fuori

    istr = sorted(appiattisci(mit.body), key=lambda z: z.lineno)
    passi = []
    for x in istr:
        sa_w, lo_w = nomi_scritti(x)
        sa_r, lo_r = nomi_letti(x)
        serv = chiamate_di_servizio(x)
        reg_w = set(a for a in sa_w if a in registro)
        for s in serv:
            reg_w |= serv_scrive.get(s, set())
        passi.append({"riga": x.lineno, "testo": ast.unparse(x).split(NL)[0][:96],
                      "scrive_registro": sorted(reg_w), "servizio": serv,
                      "self_scritte": sorted(sa_w), "self_lette": sorted(sa_r),
                      "locali_scritte": sorted(lo_w), "locali_lette": sorted(lo_r),
                      "gate": gate_di(mit.body, x)})
    w = [k for k, q in enumerate(passi) if q["scrive_registro"]]
    if not w:
        stampa("** NESSUNA scrittura del registro trovata in `mitosi`: la misura NON vale. **")
        return 1
    primo, ultimo = w[0], w[-1]
    stampa("=" * 104)
    stampa("(1) LE SCRITTURE DEL REGISTRO, in ordine di sorgente")
    stampa("=" * 104)
    stampa("  istruzioni di `mitosi` (scendendo dentro `if` e cicli) ... %d" % len(passi))
    stampa("  di cui SCRIVONO una grandezza del registro .............. %d" % len(w))
    stampa("  la PRIMA e' a :%d, l'ULTIMA a :%d" % (passi[primo]["riga"], passi[ultimo]["riga"]))
    stampa("  istruzioni FRA la prima e l'ultima ..................... %d"
           % (ultimo - primo + 1))
    fra = [k for k in range(primo, ultimo + 1) if not passi[k]["scrive_registro"]]
    stampa("  ### di queste, NON di scrittura ........................ %d" % len(fra))
    stampa("")

    # --- (3) LE DIPENDENZE: quali di quelle DEVONO stare dov'e' sono --------------------------
    stampa("=" * 104)
    stampa("(3) QUANTE DEVONO RESTARE DOV'E' SONO -- e questo e' il numero che decide")
    stampa("=" * 104)
    legate = []
    for k in fra:
        q = passi[k]
        prima_w = [j for j in w if j < k]
        dopo_w = [j for j in w if j > k]
        # LEGGE qualcosa che una scrittura PRECEDENTE produce?
        dip_prima = []
        for j in prima_w:
            p = passi[j]
            com_self = set(p["self_scritte"]) & set(q["self_lette"])
            com_loc = set(p["locali_scritte"]) & set(q["locali_lette"])
            if com_self or com_loc:
                dip_prima.append({"riga": p["riga"], "self": sorted(com_self),
                                  "locali": sorted(com_loc)})
        # PRODUCE qualcosa che una scrittura SUCCESSIVA consuma?
        dip_dopo = []
        for j in dopo_w:
            p = passi[j]
            com_self = set(q["self_scritte"]) & set(p["self_lette"])
            com_loc = set(q["locali_scritte"]) & set(p["locali_lette"])
            if com_self or com_loc:
                dip_dopo.append({"riga": p["riga"], "self": sorted(com_self),
                                 "locali": sorted(com_loc)})
        if dip_prima and dip_dopo:
            legate.append({"riga": q["riga"], "testo": q["testo"], "gate": q["gate"],
                           "legata_a_prima": dip_prima[-3:], "legata_a_dopo": dip_dopo[:3]})
    stampa("  ### ISTRUZIONI NON-DI-SCRITTURA CHE DEVONO STARE FRA DUE SCRITTURE: %d"
           % len(legate))
    stampa("      (leggono qualcosa che una scrittura PRECEDENTE produce **E** producono")
    stampa("       qualcosa che una scrittura SUCCESSIVA consuma: non si possono spostare")
    stampa("       ne' prima ne' dopo il blocco)")
    stampa("")
    for q in legate:
        stampa("  :%-6d %s" % (q["riga"], q["testo"]))
        if q["gate"]:
            stampa("          gate: %s" % "  AND  ".join(q["gate"])[:92])
        for d in q["legata_a_prima"]:
            stampa("          <- legge da :%d  %s"
                   % (d["riga"], ", ".join(d["self"] + d["locali"])[:70]))
        for d in q["legata_a_dopo"]:
            stampa("          -> serve a :%d  %s"
                   % (d["riga"], ", ".join(d["self"] + d["locali"])[:70]))
    stampa("")
    stampa("=" * 104)
    if legate:
        stampa("### IL VERDETTO: UN BLOCCO CONTIGUO RICHIEDE DI RIORDINARE.  ### STOP.")
        stampa("    %d istruzioni non-di-scrittura sono LEGATE in mezzo. Spostare le scritture in"
               % len(legate))
        stampa("    un punto solo le scavalcherebbe, e scavalcarle CAMBIA LA FISICA.")
        stampa("    E' il punto di STOP numero 4 del task history, e scatta.")
    else:
        stampa("### IL VERDETTO: NESSUNA istruzione e' LEGATA in mezzo.")
        stampa("    Un blocco contiguo NON e' impedito da un riordino. ### MA questo NON dice")
        stampa("    che il punto unico sia facile: restano i contatori, i rami condizionali sulle")
        stampa("    lunghezze delle cache, e `conc_nodi` che cresce per MUTAZIONE.")
    stampa("=" * 104)

    ref = {"blob_sim_sha1_byte": blob(SIM), "blob_strumento": blob(os.path.abspath(__file__)),
           "mitosi": {"riga_da": mit.lineno, "riga_a": mit.end_lineno},
           "grandezze_registro": sorted(registro),
           "servizio_scrive": {k: sorted(v) for k, v in serv_scrive.items()},
           "istruzioni": len(passi), "scritture_registro": len(w),
           "prima_scrittura_riga": passi[primo]["riga"],
           "ultima_scrittura_riga": passi[ultimo]["riga"],
           "istruzioni_fra": ultimo - primo + 1,
           "non_scritture_fra": len(fra),
           "legate_in_mezzo": legate,
           "verdetto": ("STOP: un blocco contiguo richiede di RIORDINARE" if legate
                        else "nessuna istruzione legata in mezzo"),
           "passi": passi}
    io.open(os.path.join(FUORI, "_punto_unico_fattibile.json"), "w", encoding="utf-8",
            newline=NL).write(json.dumps(ref, indent=1, default=str))
    io.open(os.path.join(FUORI, "_corsa.txt"), "w", encoding="utf-8",
            newline=NL).write(NL.join(P) + NL)
    return 0


if __name__ == "__main__":
    sys.exit(principale())
