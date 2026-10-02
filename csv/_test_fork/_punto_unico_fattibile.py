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


def e_pura_estensione(nodo, attr):
    """`True` se l'istruzione ESTENDE `self.attr` senza filtrarlo ne' riordinarlo.

    ### PERCHE' SERVE, ed e' la differenza fra una dipendenza VERA e una SPURIA.
    `self.pos = np.vstack([self.pos, pos_figlio])` e' una ### **pura estensione**: gli indici
    PREESISTENTI valgono lo stesso prima e dopo, quindi ### **una lettura a `pos[aa]` con `aa`
    genitore NON dipende da quella scrittura.**
    `self.peq = np.concatenate([self.peq[keep], self.peq[sel], self.peq[sel]])` invece ### **FILTRA
    con `keep`**: dopo, lo stesso indice punta a un'ALTRA voce. ### **Quella dipendenza e' VERA.**
    ### ⚠ **E l'analisi del resto dello strumento e' alla granularita' dell'ATTRIBUTO**, quindi
    sovra-segnala: questa funzione e' cio' che rende la distinzione MISURATA invece che argomentata.
    """
    for x in ast.walk(nodo):
        if (isinstance(x, ast.Call) and isinstance(x.func, ast.Attribute)
                and x.func.attr in ("concatenate", "vstack", "hstack")
                and x.args and isinstance(x.args[0], (ast.List, ast.Tuple))
                and x.args[0].elts):
            pezzi = x.args[0].elts
            primo = pezzi[0]
            # il PRIMO pezzo deve essere `self.attr` NUDO (non `self.attr[...]`)
            if not (isinstance(primo, ast.Attribute) and isinstance(primo.value, ast.Name)
                    and primo.value.id == "self" and primo.attr == attr):
                continue
            # e NESSUN pezzo deve essere un'indicizzazione di `self.attr`
            sporco = False
            for p in pezzi[1:]:
                for y in ast.walk(p):
                    if (isinstance(y, ast.Subscript) and isinstance(y.value, ast.Attribute)
                            and isinstance(y.value.value, ast.Name)
                            and y.value.value.id == "self" and y.value.attr == attr):
                        # `self.attr[a]` come pezzo NUOVO e' lecito (il figlio eredita): non
                        # cambia gli indici preesistenti.
                        pass
            return not sporco
    return False


def indici_stantii(albero, funzioni):
    """**LETTURE A INDICE STANTIO: un `x[idx]` DOPO che `x` e' stato RIFILTRATO.**

    ### ⛔ **NON e' una domanda sulla MOVIBILITA': e' un DIFETTO GIA' PRESENTE.**
    Una riscrittura come `self.peq = np.concatenate([self.peq[keep], self.peq[sel], self.peq[sel]])`
    ### **FILTRA con `keep`**: dopo quella riga ### **lo stesso indice punta a UN'ALTRA VOCE.**
    Una lettura `self.peq[sel]` che venga **dopo** legge ### **gli archi sbagliati, in silenzio** --
    e in silenzio perche' l'array e' **piu' lungo**, quindi ### **l'indice resta VALIDO** e nessuna
    eccezione scatta.

    ### ⭐ **LA REGOLA, dichiarata perche' il verdetto dipende da lei**

    | | |
    |---|---|
    | una **riscrittura con FILTRO** | `self.x = <concat>([... ])` in cui il pezzo che porta il
      vecchio contenuto e' ### **`self.x[M]` INDICIZZATO** e non `self.x` nudo. ### **Una PURA
      ESTENSIONE non conta**, perche' non sposta gli indici preesistenti |
    | un **indice STANTIO** | un `Name` ### **assegnato PRIMA** della riscrittura e ### **NON
      riassegnato** fra la riscrittura e la lettura |
    | ### **il reperto** | una lettura o scrittura ### **`self.x[idx]` DOPO** la riscrittura, con
      `idx` stantio |

    ### ⚠ **E IL LIMITE, dichiarato:** un indice **ricalcolato** fra le due righe non e'
    stantio, e la regola lo vede *(si guarda la RIASSEGNAZIONE)*. Ma ### **un indice passato a una
    FUNZIONE che lo rimappa non si vede**: l'analisi e' locale alla funzione.
    """
    fuori = []
    for n in ast.walk(albero):
        if not (isinstance(n, ast.FunctionDef) and n.name in funzioni):
            continue
        # tutte le assegnazioni di Name, con la riga
        assegnati = {}
        for x in ast.walk(n):
            if isinstance(x, (ast.Assign, ast.AugAssign)):
                mire = x.targets if isinstance(x, ast.Assign) else [x.target]
                for m in mire:
                    for y in ([m] if not isinstance(m, (ast.Tuple, ast.List)) else m.elts):
                        if isinstance(y, ast.Name):
                            assegnati.setdefault(y.id, []).append(x.lineno)
            elif isinstance(x, ast.For):
                for y in ast.walk(x.target):
                    if isinstance(y, ast.Name):
                        assegnati.setdefault(y.id, []).append(x.lineno)
        # le riscritture CON FILTRO, per attributo
        filtri = []
        for x in ast.walk(n):
            if not isinstance(x, ast.Assign) or len(x.targets) != 1:
                continue
            m = x.targets[0]
            if not (isinstance(m, ast.Attribute) and isinstance(m.value, ast.Name)
                    and m.value.id == "self"):
                continue
            attr = m.attr
            if e_pura_estensione(x, attr):
                continue
            # il pezzo vecchio e' `self.attr[M]` indicizzato?
            maschera = None
            for y in ast.walk(x.value):
                if (isinstance(y, ast.Subscript) and isinstance(y.value, ast.Attribute)
                        and isinstance(y.value.value, ast.Name)
                        and y.value.value.id == "self" and y.value.attr == attr
                        and isinstance(y.slice, ast.Name)):
                    maschera = y.slice.id
                    break
            if maschera is not None:
                filtri.append({"attr": attr, "riga": x.lineno, "maschera": maschera,
                               "testo": ast.unparse(x)[:110]})
        # le letture/scritture `self.attr[idx]` DOPO una riscrittura con filtro
        for f in filtri:
            for y in ast.walk(n):
                if not (isinstance(y, ast.Subscript) and isinstance(y.value, ast.Attribute)
                        and isinstance(y.value.value, ast.Name)
                        and y.value.value.id == "self" and y.value.attr == f["attr"]):
                    continue
                if y.lineno <= f["riga"]:
                    continue
                if not isinstance(y.slice, ast.Name):
                    continue
                idx = y.slice.id
                righe_idx = assegnati.get(idx, [])
                if not righe_idx:
                    continue
                prima = [r for r in righe_idx if r < f["riga"]]
                fra = [r for r in righe_idx if f["riga"] < r <= y.lineno]
                if prima and not fra:
                    istr = next((z for z in ast.walk(n)
                                 if isinstance(z, (ast.Assign, ast.AugAssign, ast.Expr))
                                 and z.lineno == y.lineno), None)
                    fuori.append({"funzione": n.name, "attr": f["attr"],
                                  "riscrittura_riga": f["riga"], "maschera": f["maschera"],
                                  "riscrittura": f["testo"],
                                  "lettura_riga": y.lineno,
                                  "indice": idx, "indice_assegnato_a": prima,
                                  "lettura": (ast.unparse(istr)[:110] if istr
                                              else ast.unparse(y)[:110]),
                                  "gate": gate_di(n.body, istr) if istr else []})
    # si deduplica per (riga di lettura, attributo, indice)
    visti, puliti = set(), []
    for q in fuori:
        k = (q["lettura_riga"], q["attr"], q["indice"])
        if k not in visti:
            visti.add(k)
            puliti.append(q)
    return sorted(puliti, key=lambda z: z["lettura_riga"])


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
        # ⚠ IL TERZO TIPO DI DIPENDENZA, e la prima stesura NON lo controllava: l'ANTI-DIPENDENZA.
        #   Un'istruzione che LEGGE un attributo che una scrittura SUCCESSIVA modifica NON si puo'
        #   spostare DOPO quella scrittura -- e per raccogliere le scritture in un blocco bisogna
        #   spostare la lettura di la'. E' la dipendenza che DECIDE, perche' `sel` indicizza gli
        #   array PRE-mitosi: dopo `concatenate([tw[keep], zz, zz])` lo stesso `sel` punta ad
        #   ARCHI DIVERSI.
        anti = []
        for j in dopo_w:
            p = passi[j]
            com = set(p["self_scritte"]) & set(q["self_lette"])
            if com:
                anti.append({"riga": p["riga"], "self": sorted(com)})
        # ⚠ E IL QUARTO: un'istruzione che PESCA da `net.rng`. Spostarla cambia L'ORDINE DELLE
        #   ESTRAZIONI, che dal 2026-10-02 e' un CONTRATTO SCRITTO (doc/CONTRATTO_nascita.md).
        pesca = ("rng" in " ".join(q["self_lette"]) or ".rng." in q["testo"]
                 or "rng." in q["testo"])
        if (dip_prima and (dip_dopo or anti)) or (pesca and (dip_prima or anti)):
            # ### SPURIA O GENUINA: una dipendenza su un attributo che la scrittura ESTENDE senza
            #   filtrare NON vincola una lettura a indici PREESISTENTI. Si misura dall'AST.
            def classifica(elenco):
                fuori = []
                for d in elenco:
                    nodo_w = next((y for y in istr if y.lineno == d["riga"]), None)
                    sp = []
                    for attr in d.get("self", []):
                        sp.append(bool(nodo_w is not None and e_pura_estensione(nodo_w, attr)))
                    fuori.append(dict(d, pura_estensione=(bool(sp) and all(sp))))
                return fuori
            dp = classifica(dip_prima[-3:])
            an = classifica(anti[:4])
            # GENUINA se almeno una dipendenza NON e' una pura estensione, oppure se la catena
            #   passa per una LOCALE (li' l'indice non c'entra: e' un valore).
            genuina = (any(not d["pura_estensione"] for d in dp)
                       or any(not d["pura_estensione"] for d in an)
                       or any(d.get("locali") for d in dip_prima)
                       or any(d.get("locali") for d in dip_dopo))
            legate.append({"riga": q["riga"], "testo": q["testo"], "gate": q["gate"],
                           "pesca_dal_generatore": bool(pesca),
                           "legata_a_prima": dp, "legata_a_dopo": dip_dopo[:3],
                           "anti_dipendenze": an,
                           "genuina_a_granularita_indice": bool(genuina)})
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
        if q["pesca_dal_generatore"]:
            stampa("          ### PESCA DA `net.rng`: spostarla cambia l'ORDINE DELLE ESTRAZIONI,")
            stampa("              che e' un CONTRATTO SCRITTO (doc/CONTRATTO_nascita.md).")
        for d in q["legata_a_prima"]:
            stampa("          <- legge da :%d  %s"
                   % (d["riga"], ", ".join(d["self"] + d["locali"])[:70]))
        for d in q["legata_a_dopo"]:
            stampa("          -> serve a :%d  %s"
                   % (d["riga"], ", ".join(d["self"] + d["locali"])[:70]))
        for d in q["anti_dipendenze"]:
            stampa("          !! ANTI-DIP: :%d RISCRIVE %s, quindi questa lettura NON puo'"
                   % (d["riga"], ", ".join(d["self"])[:52]))
            stampa("             andare DOPO quella scrittura (`sel` indicizza il PRE-mitosi)")
    stampa("")
    stampa("  RIEPILOGO PER TIPO DI DIPENDENZA:")
    stampa("    con flusso PRIMA e flusso DOPO ..: %d"
           % sum(1 for q in legate if q["legata_a_prima"] and q["legata_a_dopo"]))
    stampa("    ### con ANTI-DIP (lettura invalidata da una scrittura successiva): %d"
           % sum(1 for q in legate if q["anti_dipendenze"]))
    stampa("    che PESCANO dal generatore ......: %d"
           % sum(1 for q in legate if q["pesca_dal_generatore"]))
    stampa("")
    # --- IL GATE, dal RUNTIME: una dipendenza in un ramo che non gira NON vincola il run di oggi
    stampa("=" * 104)
    stampa("(4) QUALI DI QUELLE GIRANO, e quali sono SPURIE a granularita' di INDICE")
    stampa("=" * 104)
    import contextlib  # noqa: E402  (solo qui: serve il runtime dei flag)
    sys.path.insert(0, os.path.join(RADICE, "csv"))
    import _cli_flag  # noqa: E402
    with contextlib.redirect_stdout(io.StringIO()):
        _S0, argv = _cli_flag.argv_del_driver(extra=["--seme=11"],
                                              dest=os.path.join(FUORI, "_scarto_cli"))
        S, a = _cli_flag.carica_dal_cli(list(argv), nome="pu_flag")
        S._applica_regime(a)

    def gira(gate):
        """`(gira, perche')` -- si valuta ogni condizione del gate coi flag DAL RUNTIME.
        Cio' che non si sa valutare si dichiara `None`, non si assume."""
        for c in gate:
            for nome in ("COPPIA_DENSITA", "PEQ_NASCITA_LOCALE", "TRACCIA_D0", "MITOSI_DIR",
                         "ANTIFASE_ADD", "COPPIA_MIT", "REGIME", "MITOSI_2LAM"):
                if nome in c:
                    v = getattr(S, nome, None)
                    neg = c.startswith("NOT (")
                    if nome == "COPPIA_MIT":
                        ok = float(v) > 0.0
                    elif nome == "MITOSI_DIR":
                        ok = float(v) != 0.0
                    elif nome == "REGIME":
                        ok = (str(v) == "deterministico") == ("deterministico" in c)
                    else:
                        ok = bool(v)
                    if neg:
                        ok = not ok
                    if not ok:
                        return False, "%s = %r" % (nome, v)
        return True, "tutte le condizioni del gate sono vere coi flag di oggi"

    tabella = []
    for q in legate:
        g, perche = gira(q["gate"])
        q["gira_col_driver"] = g
        q["perche_gate"] = perche
        tabella.append(q)
    girano = [q for q in tabella if q["gira_col_driver"]]
    gen = [q for q in girano if q["genuina_a_granularita_indice"]]
    stampa("  %-7s %-6s %-9s %s" % ("riga", "gira?", "genuina?", "perche'"))
    stampa("  " + "-" * 96)
    for q in tabella:
        stampa("  :%-6d %-6s %-9s %s"
               % (q["riga"], "SI" if q["gira_col_driver"] else "NO",
                  "SI" if q["genuina_a_granularita_indice"] else "spuria", q["perche_gate"][:56]))
    stampa("")
    stampa("  ### segnalate %d  ->  girano col driver %d  ->  ### GENUINE a granularita'"
           % (len(tabella), len(girano)))
    stampa("      di INDICE: %d" % len(gen))
    for q in gen:
        stampa("      ### :%-6d %s" % (q["riga"], q["testo"][:84]))
    stampa("")
    # --- (5) LE LETTURE A INDICE STANTIO: un DIFETTO, non una domanda sulla movibilita' ---------
    stampa("=" * 104)
    stampa("(5) LETTURE A INDICE STANTIO -- `x[idx]` DOPO che `x` e' stato RIFILTRATO")
    stampa("=" * 104)
    stampa("    Non e' una domanda sulla MOVIBILITA': e' un DIFETTO GIA' PRESENTE. Dopo una")
    stampa("    riscrittura con filtro, lo stesso indice punta a UN'ALTRA VOCE -- e in silenzio,")
    stampa("    perche' l'array e' PIU' LUNGO e l'indice resta VALIDO.")
    stantii = indici_stantii(t, ("mitosi", "semina", "_allaccia", "_eredita_psi_figli",
                                 "_eredita_spinore_figli"))
    for q in stantii:
        g, perche = gira(q["gate"])
        q["gira_col_driver"] = g
        q["perche_gate"] = perche
    stampa("")
    stampa("  ### TROVATE: %d" % len(stantii))
    for q in stantii:
        stampa("")
        stampa("  ### :%d  `%s`  <- legge `%s[%s]` con l'indice STANTIO"
               % (q["lettura_riga"], q["lettura"][:80], q["attr"], q["indice"]))
        stampa("          la riscrittura CON FILTRO e' a :%d, maschera `%s`:"
               % (q["riscrittura_riga"], q["maschera"]))
        stampa("            %s" % q["riscrittura"])
        stampa("          l'indice `%s` e' assegnato a :%s e NON riassegnato in mezzo"
               % (q["indice"], ",".join(str(x) for x in q["indice_assegnato_a"])))
        if q["gate"]:
            stampa("          gate: %s" % "  AND  ".join(q["gate"])[:88])
        stampa("          ### GIRA col driver: %s   (%s)"
               % ("SI" if q["gira_col_driver"] else "NO", q["perche_gate"][:50]))
    vivi = [q for q in stantii if q["gira_col_driver"]]
    if stantii:
        stampa("")
        stampa("  ### di cui GIRANO col driver: %d   -> %s" % (len(vivi),
               "DIFETTO ATTIVO" if vivi else "difetti LATENTI, in rami spenti"))
    stampa("")
    stampa("=" * 104)
    if gen:
        stampa("### IL VERDETTO: UN BLOCCO CONTIGUO RICHIEDE DI RIORDINARE.  ### STOP.")
        stampa("    %d istruzione/i non-di-scrittura e' LEGATA in mezzo, GIRA col driver e la sua"
               % len(gen))
        stampa("    dipendenza e' GENUINA anche a granularita' di INDICE. Spostare le scritture in")
        stampa("    un punto solo la scavalcherebbe, e scavalcarla CAMBIA LA FISICA.")
        stampa("    E' il punto di STOP numero 4 del task history, e scatta.")
        stampa("    ### E le altre %d NON sono la prova: %d non girano col driver, le restanti"
               % (len(tabella) - len(gen), len(tabella) - len(girano)))
        stampa("    sono SPURIE a granularita' di indice (una PURA ESTENSIONE non vincola una")
        stampa("    lettura a indici PREESISTENTI). ### Lo dico invece di contarle tutte.")
    elif legate:
        stampa("### IL VERDETTO: nessuna dipendenza GENUINA che giri col driver.")
        stampa("    Le %d segnalate sono o in rami che NON girano, o SPURIE a granularita' di"
               % len(legate))
        stampa("    indice. ### Un blocco contiguo NON e' impedito da un riordino -- ma restano")
        stampa("    i contatori, i rami sulle cache e `conc_nodi` per mutazione.")
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
           "legate_che_girano": [q["riga"] for q in girano],
           "letture_a_indice_stantio": stantii,
           "indici_stantii_che_girano": [q["lettura_riga"] for q in vivi],
           "legate_GENUINE_che_girano": [{"riga": q["riga"], "testo": q["testo"]} for q in gen],
           "verdetto": ("STOP: un blocco contiguo richiede di RIORDINARE" if gen
                        else ("nessuna dipendenza GENUINA che giri col driver" if legate
                              else "nessuna istruzione legata in mezzo")),
           "passi": passi}
    io.open(os.path.join(FUORI, "_punto_unico_fattibile.json"), "w", encoding="utf-8",
            newline=NL).write(json.dumps(ref, indent=1, default=str))
    io.open(os.path.join(FUORI, "_corsa.txt"), "w", encoding="utf-8",
            newline=NL).write(NL.join(P) + NL)
    return 0


if __name__ == "__main__":
    sys.exit(principale())
