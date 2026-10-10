# -*- coding: utf-8 -*-
"""PUNTO `9` — **UN SOLO ESECUTORE: chi avanza lo stato passa dallo schedulatore.**

> ### ⛔ *«uno script che avanza lo stato **senza** l'esecutore dello schedulatore
> → **rifiutato** *(generalizza `H-P9`)*»*.

### ⭐ **E `H-P9` DICEVA LA STESSA COSA PER L'ERA `1`:** *«uno strumento che fa
avanzare una rete con `net.step()` invece di `passo_pieno`»*. ### **La ragione e'
identica:** se due posti avanzano lo stato, ### **due misure della stessa scena possono
divergere**, e ### **il confronto non prova niente.**

### ⚠ **MA UN COLLAUDO DEVE POTER CHIAMARE UN SOTTO-PASSO, e questa non e' una
scappatoia: e' il suo MESTIERE.** Il cono ### **per STRATO** si misura
### **esattamente** facendo ### **un sotto-passo d'arco** — e un presidio che lo
vietasse ### **renderebbe la misura impossibile**, non il codice migliore.

### ✅ **QUINDI LE ECCEZIONI SONO DICHIARATE, UNA PER UNA, CON IL LORO PERCHE'**, e
il presidio ### **rifiuta tutto il resto.** ### ⛔ **Un'eccezione senza un perche' di
almeno `40` caratteri e' rifiutata anche lei:** *«una via di fuga a costo zero non e'
un'eccezione, e' un buco.»*

### ⚠ **E L'AVEVO PREVISTO, nel task history:** *«sospetto che il caso da rifiutare
sia `_collauda_passo.py`, che chiama `mezzo_implicito` direttamente»*.
### ✅ **Era vero**, e la cura e' ### **dichiararlo**, non nasconderlo.
"""
import ast
import glob
import io
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
sys.path.insert(0, _QUI)

NL = chr(10)
PRESIDIO = "P-ES1"

# ### ⛔ **LE FUNZIONI CHE AVANZANO LO STATO.** Chiamarne una vuol dire
# ### ### **far evolvere la fisica**, e il punto `9` dice che lo fa ### **un solo
# ### posto.**
# ### ⚠ **E `gradiente` NON E- QUI, benche- al primo giro lo avessi messo:**
# ### calcolare `dH/dpsi*` ### **NON E- avanzare lo stato** -- e il presidio aveva
# ### accusato `hamiltoniana.py`, che ### **lo DEFINISCE.** ### **Avanza chi integra**,
# ### cioe- chi mette insieme il gradiente e il `dt`.
AVANZANO = ("mezzo_implicito", "passo_globale", "passo_locale")

# ### ⭐ **L-ESECUTORE: il file che PUO- chiamarle tutte.**
ESECUTORE = "primo_ordine/passo.py"

# =====================================================================================
#   LE ECCEZIONI, DICHIARATE UNA PER UNA
# -------------------------------------------------------------------------------------
#   `file -> {funzione chiamata: perche-}`
# =====================================================================================
ECCEZIONI = {
    "primo_ordine/_collauda_passo.py": {
        "mezzo_implicito":
            "il cono PER STRATO si misura facendo UN SOTTO-PASSO d-arco, e un presidio "
            "che lo vietasse renderebbe la misura impossibile invece del codice migliore. "
            "### E- il MESTIERE di un collaudo, non una scappatoia",
        "passo_globale":
            "il collaudo DEVE far girare entrambi i candidati per confrontarli: cono, "
            "deriva, reversibilita-. ### Chiamarli e- cio- che il mandato gli chiede",
        "passo_locale":
            "idem: i due candidati si misurano NELLO STESSO MODO, e la tavola del referto "
            "esiste perche- il collaudo li ha fatti girare entrambi",
    },
    "primo_ordine/_collauda_simmetrie.py": {
        "passo_locale":
            "una CONSERVAZIONE si misura SU UNA CORSA: non c-e- un altro modo di sapere "
            "se la norma si conserva in 200 passi. ### E la corsa deve essere QUELLA DEL "
            "DRIVER -- stesso integratore, stessa scena, stesso seme -- altrimenti la "
            "deriva misurata e- quella di un ALTRO sistema, e la soglia derivata non le "
            "si applica. ### Chiamare l-esecutore e- cio- che rende la misura VERA; "
            "scriverne uno qui la renderebbe FINTA",
    },
    "primo_ordine/_collauda_grafo.py": {
        "passo_globale":
            "il secondo significato di <<archi simmetrici>> e- che LA FISICA tratti "
            "`(i,j)` e `(j,i)` allo stesso modo, e si misura SCAMBIANDO `ii` e `jj` su "
            "tutti gli archi e PRETENDENDO LO STESSO STATO AL BIT. ### Senza far "
            "avanzare lo stato DUE VOLTE quella misura non esiste -- e il controllo per "
            "passo, che e- quello cablato, NON PUO- vederla. ### E lo stesso passo serve "
            "a MISURARE IL COSTO del controllo in rapporto a un passo vero: un budget "
            "stimato invece che misurato e- un numero senza provenienza (`L-NUMERI`)",
    },
    "primo_ordine/sigilli/_modello.py": {
        "passo_locale":
            "un SIGILLO fa girare i suoi bracci, ed e- il suo mestiere: chiama l-esecutore "
            "come il driver, e NON ne scrive uno suo. ### Il braccio `zero` e il braccio "
            "`g != 0` DEVONO girare NELLO STESSO MODO, altrimenti il confronto al byte "
            "non misura la legge: misura due esecutori diversi",
    },
    "primo_ordine/driver.py": {
        "passo_globale":
            "il driver AVANZA LA CORSA, ed e- il suo mestiere: chiama l-esecutore che la "
            "configurazione DICHIARA, e non ne scrive uno suo",
        "passo_locale":
            "idem: la configurazione dichiara QUALE dei due, e il driver chiama quello -- "
            "### non c-e- nessun ramo che sceglie da solo",
    },
}

# ### ⛔ **E UN SECONDO ESECUTORE SCRITTO A MANO SI RICONOSCE DALLA FORMA:**
# ### `st[k] + dt * (-1j) * g[k]`. ### **Chi la scrive sta integrando**, e deve
# ### ### **essere l-esecutore** o ### **essere dichiarato.**
FORMA_PASSO = "-1j"

SCRITTI_A_MANO = {
    "primo_ordine/_collauda_passo.py::eulero_esplicito":
        "e- l-EULERO ESPLICITO, scritto SOLO per il caso che DEVE fallire del punto 8: "
        "senza di lui il braccio della reversibilita- non distinguerebbe un metodo "
        "SIMMETRICO da uno qualunque, e sarebbe un FALSO-UNO. ### NON e- un candidato e "
        "non lo diventera-",
    "primo_ordine/passo.py::mezzo_implicito":
        "E- L-ESECUTORE: e- il posto dove lo stato avanza, e l-unico",
}


def file_era2():
    f = sorted(glob.glob(os.path.join(RADICE, "primo_ordine", "**", "*.py"),
                         recursive=True))
    base = RADICE.replace(os.sep, "/")
    return [x.replace(os.sep, "/")[len(base) + 1:] for x in f
            if "__pycache__" not in x]


def chiamate(rel):
    """### Le funzioni di `AVANZANO` che un file ### **chiama O NOMINA**, via AST.

    ### ⛔ **E <<O NOMINA>> E- LA PARTE CHE CONTA, e me l-ha insegnata il driver:**
    scrive ### **`avanza = PA.passo_locale if ... else PA.passo_globale`** e poi chiama
    ### **`avanza(...)`**. ### ⚠ **Un presidio che guardasse solo le CHIAMATE non
    vedrebbe niente** -- e ### **assegnare la funzione a una variabile sarebbe la via di
    fuga piu- facile del mondo.**
    """
    p = os.path.join(RADICE, rel)
    try:
        arb = ast.parse(io.open(p, encoding="utf-8").read(), filename=p)
    except Exception:
        return set()
    fuori = set()
    for n in ast.walk(arb):
        # ### la CHIAMATA diretta
        if isinstance(n, ast.Call):
            nome = getattr(n.func, "id", None) or getattr(n.func, "attr", None)
            if nome in AVANZANO:
                fuori.add(nome)
        # ### e il NOME, dovunque sia: assegnato, passato, messo in una tupla
        if isinstance(n, ast.Attribute) and n.attr in AVANZANO:
            fuori.add(n.attr)
        if isinstance(n, ast.Name) and n.id in AVANZANO:
            fuori.add(n.id)
    return fuori


def passi_a_mano(rel):
    """### Le funzioni che ### **scrivono un passo a mano** *(la forma `-1j`)*."""
    p = os.path.join(RADICE, rel)
    try:
        src = io.open(p, encoding="utf-8").read()
        arb = ast.parse(src, filename=p)
    except Exception:
        return []
    fuori = []
    for n in ast.walk(arb):
        if not isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        seg = ast.get_source_segment(src, n) or ""
        # ### ⚠ **Si guarda il SEGMENTO della funzione, non il file:** cosi- il
        # ### nome che si riporta e- ### **quello della funzione che integra**, non
        # ### del file -- e ### **un-eccezione per un file intero sarebbe troppo larga.**
        if FORMA_PASSO in seg and "dt" in seg:
            fuori.append(n.name)
    return fuori


def controlla():
    err = []
    for rel in file_era2():
        if rel == ESECUTORE:
            continue
        amm = ECCEZIONI.get(rel, {})
        for fn in sorted(chiamate(rel)):
            if fn not in amm:
                err.append("`P-ES1` `%s`: chiama `%s`, che AVANZA LO STATO, e NON E- "
                           "DICHIARATO. ### Il punto 9: un solo esecutore. Se serve "
                           "davvero, va in `ECCEZIONI` ### con il suo perche-"
                           % (rel, fn))
                continue
            if len(str(amm[fn])) < 40:
                err.append("`P-ES1` `%s::%s`: l-eccezione ha un perche- di %d caratteri. "
                           "### Una via di fuga a costo zero non e- un-eccezione: e- un "
                           "buco" % (rel, fn, len(str(amm[fn]))))
        for fn in passi_a_mano(rel):
            k = "%s::%s" % (rel, fn)
            if k not in SCRITTI_A_MANO:
                err.append("`P-ES1` `%s`: SCRIVE UN PASSO A MANO (la forma `%s`) e NON E- "
                           "DICHIARATO. ### Chi integra deve essere l-esecutore, o "
                           "dichiararsi" % (k, FORMA_PASSO))
            elif len(str(SCRITTI_A_MANO[k])) < 40:
                err.append("`P-ES1` `%s`: dichiarato con un perche- troppo corto" % k)
    # --- e le eccezioni ORFANE
    for rel, d in sorted(ECCEZIONI.items()):
        if rel not in file_era2():
            err.append("`P-ES1` `%s`: ha delle eccezioni e IL FILE NON C-E-" % rel)
            continue
        for fn in sorted(set(d) - chiamate(rel)):
            err.append("`P-ES1` `%s::%s`: l-eccezione e- DICHIARATA e la chiamata NON "
                       "C-E- PIU-. ### Un-eccezione che non serve va TOLTA: resta come "
                       "un permesso che nessuno ha chiesto" % (rel, fn))
    for k in sorted(SCRITTI_A_MANO):
        rel, _, fn = k.partition("::")
        if rel in file_era2() and fn not in passi_a_mano(rel):
            err.append("`P-ES1` `%s`: dichiarato come passo a mano e NON LO E- PIU-" % k)
    return err


def collaudo():
    ok = [0, 0]

    def esito(che, passa, nota=""):
        ok[1] += 1
        ok[0] += 1 if passa else 0
        print("  %-64s %s   %s" % (che, "PASSA" if passa else "### FALLISCE", nota))

    print("=" * 100)
    print("IL COLLAUDO DI `P-ES1` -- nei DUE VERSI")
    print("=" * 100)
    n_ecc = sum(len(d) for d in ECCEZIONI.values())
    esito("sul disco: `P-ES1` TACE", controlla() == [],
          "%d file, %d eccezioni dichiarate, %d passi a mano"
          % (len(file_era2()), n_ecc, len(SCRITTI_A_MANO)))
    esito("### il braccio sopra HA MATERIA (ci sono eccezioni da verificare)",
          n_ecc >= 5, "%d: se fosse 0 il braccio sarebbe un FALSO-UNO" % n_ecc)
    esito("### e L-AVEVO PREVISTO: `_collauda_passo.py` chiama `mezzo_implicito`",
          "mezzo_implicito" in chiamate("primo_ordine/_collauda_passo.py"),
          "### scritto nel task history PRIMA di guardare, e la cura e- DICHIARARLO")
    # --- un'eccezione TOLTA
    # ### ⚠ **E QUI AVEVO UN DIFETTO DI ALIASING, e il collaudo me l-ha detto:**
    # ### `salva` era ### **lo stesso dizionario** che il ripristino rimetteva in
    # ### `ECCEZIONI`, quindi il caso successivo ### **mutava la copia di salvataggio.**
    # ### ✅ **Si ricopia a ogni giro**, e il braccio finale ### **lo verifica.**
    import copy as _copy
    salva = _copy.deepcopy(ECCEZIONI["primo_ordine/_collauda_passo.py"])
    try:
        del ECCEZIONI["primo_ordine/_collauda_passo.py"]["mezzo_implicito"]
        esito("### DEVE scattare: una chiamata NON dichiarata",
              any("NON E- DICHIARATO" in e for e in controlla()),
              "### il punto 9: un solo esecutore")
    finally:
        ECCEZIONI["primo_ordine/_collauda_passo.py"] = _copy.deepcopy(salva)
    # --- un perche' troppo corto
    try:
        ECCEZIONI["primo_ordine/_collauda_passo.py"]["mezzo_implicito"] = "serve"
        esito("### DEVE scattare: un `perche-` troppo corto",
              any("e- un buco" in e for e in controlla()),
              "### una via di fuga a costo zero non e- un-eccezione")
    finally:
        ECCEZIONI["primo_ordine/_collauda_passo.py"] = _copy.deepcopy(salva)
    # --- un'eccezione ORFANA
    try:
        ECCEZIONI["primo_ordine/_collauda_passo.py"] = dict(
            salva, passo_inventato="x" * 50)
        esito("### DEVE scattare: un-eccezione ORFANA (la chiamata non c-e- piu-)",
              any("NON C-E- PIU-" in e for e in controlla()),
              "### un permesso che nessuno ha chiesto")
    finally:
        ECCEZIONI["primo_ordine/_collauda_passo.py"] = _copy.deepcopy(salva)
    # --- un passo scritto a mano, non dichiarato
    salva2 = dict(SCRITTI_A_MANO)
    try:
        del SCRITTI_A_MANO["primo_ordine/_collauda_passo.py::eulero_esplicito"]
        esito("### DEVE scattare: un PASSO SCRITTO A MANO non dichiarato",
              any("SCRIVE UN PASSO A MANO" in e for e in controlla()),
              "### l-Eulero esplicito del punto 8: ### esiste, e va DICHIARATO")
    finally:
        SCRITTI_A_MANO.clear()
        SCRITTI_A_MANO.update(salva2)
    esito("NON deve scattare: rimesso tutto a posto, `P-ES1` TACE", controlla() == [],
          "### i bracci di sopra scattavano per i loro casi finti")
    print("=" * 100)
    print("IL COLLAUDO DI `P-ES1`: %d su %d   %s"
          % (ok[0], ok[1], "### TUTTI PASSATI" if ok[0] == ok[1] else "### CI SONO BUCHI"))
    print("=" * 100)
    return 0 if ok[0] == ok[1] else 1


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    if "--collaudo" in argv:
        return collaudo()
    err = controlla()
    print("  `P-ES1`: l-esecutore e- `%s`; %d eccezioni dichiarate su %d file, %d passi "
          "a mano" % (ESECUTORE, sum(len(d) for d in ECCEZIONI.values()),
                      len(ECCEZIONI), len(SCRITTI_A_MANO)))
    for e in err[:14]:
        print("  ### %s" % e)
    print("  ### %d errori" % len(err))
    return 1 if err else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
