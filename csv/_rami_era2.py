# -*- coding: utf-8 -*-
"""PUNTO `2`, seconda parte — **OGNI RAMO DELLA FISICA DELL'ERA `2` E' DICHIARATO.**

> ### ⛔ **`A8`: UN RAMO SILENZIOSO NON E' UN RAMO.** E `P5`: *«ogni ramo `else` /
> fallback / `getattr(..., default)` su un percorso fisico ### **va CONTATO**»*.

### ⭐ **E LA PARTE CHE CONTA NON E' CONTARLI: E' DIRE A CHE SERVONO.** Un `if` non
e' un difetto — ### **un `if` NON DICHIARATO lo e'**, perche' nessuno sa se smista,
valida, o ### **sceglie in silenzio un pezzo di fisica.**

| il ruolo | che cosa significa | e' un difetto? |
|---|---|---|
| **`smistamento`** | sceglie ### **quale** operazione fare, da ### **un campo dichiarato** *(`TIPO`, il nome nella composizione)* | ### ✅ **no:** la decisione viene da un campo, non da un indovinello |
| **`validazione`** | costruisce ### **un messaggio di errore** e non cambia nessun valore | ### ✅ **no:** e' il presidio stesso |
| **`iterazione`** | ### **ferma un ciclo** *(convergenza, fine lista)* | ### ✅ **no**, ma ### **la soglia va DICHIARATA** |
| **`default`** | sceglie un valore ### **quando il chiamante non lo passa** | ### ⚠ **SI', ed e' il punto `15(b)`:** *«un parametro non presente e' un ERRORE»* |
| **`guardia`** | protegge da uno stato ### **che non dovrebbe esistere** | ### ⛔ **SI':** `A11` dice ### **cerca l'errore**, e `P5` che ### **va CONTATA** |

### ⚠ **IL LIMITE, dichiarato:** la classificazione ### **la scrivo io**, il
### **conteggio** no — quello lo misura l'AST. ### **Quindi il presidio garantisce
che un ramo NUOVO non passi inosservato, NON che la mia etichetta sia giusta.**
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
PRESIDIO = "P-R1"

RUOLI = ("smistamento", "validazione", "iterazione", "default", "guardia")

# ### I file di FISICA dell'era `2`: gli stessi di `P-E4`, piu' i generati.
def file_fisica():
    f = [os.path.join("primo_ordine", x) for x in
         ("stato.py", "hamiltoniana.py", "passo.py", "crescita.py", "vuoto.py")]
    f += sorted(glob.glob(os.path.join("primo_ordine", "termini", "*.py")))
    # ### ⚠ **I PERCORSI CON `/`, SEMPRE:** `os.path.join` su Windows da- `\\`,
    # ### e la tabella usa `/`. ### **Una chiave che cambia col sistema operativo non e-
    # ### una chiave** -- e me l-ha detto il presidio, con 24 errori al primo giro.
    return [x.replace(os.sep, "/") for x in f
            if os.path.exists(os.path.join(RADICE, x))
            and not x.endswith("__init__.py")]


# =====================================================================================
#   LA TABELLA -- (file, funzione) -> (quanti, ruolo, perche')
# -------------------------------------------------------------------------------------
#   ### ⛔ **MISURATA il 2026-10-09: `27` rami in `12` funzioni.** Il conteggio lo
#   ### fa l'AST; ### **il ruolo e il perche- li ho scritti io, leggendoli.**
# =====================================================================================
RAMI = {
    ("primo_ordine/stato.py", "nuovo"): (
        2, "validazione",
        "solleva `NotImplementedError` per i tipi d-arco e per `coppia_coniugata`: "
        "### NON sceglie un valore, DICHIARA CHE NON SA FARLO -- ed e- il segnaposto "
        "ONESTO della decisione 13"),
    ("primo_ordine/hamiltoniana.py", "carica_termini"): (
        3, "smistamento",
        "salta i file che non sono `.py` e quelli senza `LEGGE`: ### la decisione viene "
        "da UN CAMPO (`LEGGE` esiste o no), non da un indovinello"),
    ("primo_ordine/passo.py", "strati"): (
        1, "iterazione",
        "cerca ### il primo strato libero per un arco: ferma il ciclo quando lo trova. "
        "### Nessuna soglia: e- una ricerca ESATTA"),
    ("primo_ordine/passo.py", "valida_composizione"): (
        6, "validazione",
        "### SONO IL PRESIDIO STESSO: i quattro controlli della composizione "
        "(vocabolario, palindromo di nomi e pesi, doppioni, pesi a 1). Non cambiano "
        "nessun valore: ### costruiscono messaggi"),
    ("primo_ordine/passo.py", "mezzo_implicito"): (
        2, "iterazione",
        "ferma il punto fisso quando lo scarto scende sotto `toll`. ### LA SOGLIA "
        "VIENE DALLA CONFIGURAZIONE (punto 15(a)), e ### IL CONO DEL GLOBALE DIPENDE "
        "DA LEI -- misurato, e il referto lo dice"),
    ("primo_ordine/passo.py", "passo_locale"): (
        2, "smistamento",
        "smista sul nome dell-operazione, che viene ### DALLA COMPOSIZIONE DICHIARATA, "
        "e sceglie lo strato per indice. ### Nessun default: `gli_strati` SI PASSA"),
    ("primo_ordine/passo.py", "_costanti_di_modulo"): (
        2, "smistamento",
        "salta i nomi `__dunder__` e i callable: ### smista su un TIPO, non su un valore"),
    ("primo_ordine/passo.py", "senza_cache"): (
        1, "smistamento",
        "confronta i nomi prima e dopo: ### e- un confronto, non una scelta"),
}

# ### ⛔ **E QUATTRO FUNZIONI HANNO PERSO TUTTI I LORO RAMI** *(punto `15(b)`)*:
# ### `energia`, `gradiente`, `gradiente_grezzo` e `passo_globale`. Avevano
# ### ### **un default** *(`termini=None`)* e ### **uno smistamento su `TIPO`**;
# ### togliere il default ha portato via il primo, e ### **rendere UNIFORME la firma
# ### dei generati** *(`energia(st, ii, jj)` per tutti)* ha portato via il secondo.
# ### ⭐ **UNA FIRMA UNIFORME E- UN RAMO IN MENO** *(`A8`)*, e non l-avevo
# ### previsto: ### **cercavo di pagare un debito, e ne ho pagati due.**

def _conta(p):
    """### I rami per funzione, ### **contati dall-AST.**"""
    arb = ast.parse(io.open(os.path.join(RADICE, p), encoding="utf-8").read(), filename=p)
    fuori = {}
    for fn in [n for n in ast.walk(arb) if isinstance(n, ast.FunctionDef)]:
        c = 0
        for n in ast.walk(fn):
            if isinstance(n, (ast.If, ast.IfExp, ast.Try)):
                c += 1
            elif isinstance(n, ast.BoolOp) and isinstance(n.op, ast.Or):
                c += 1
        if c:
            fuori[fn.name] = c
    return fuori


def default_nelle_firme(p):
    """### I parametri con ### **un valore di default** in un file di fisica.

    ### \u26d4 **IL PUNTO `15(b)`:** *<<un parametro non presente e- un ERRORE, e un
    controllo sull-AST RIFIUTA i valori di default nei moduli di fisica>>*.
    ### \u2b50 **E la ragione e- `CONFIG-1`:** un default e- ### **un valore che gira
    senza che nessuno l-abbia scelto**, e `CONFIG-1` ha misurato dove porta --
    ### **`28` leggi su `31` che giravano SPENTE** senza che nessuno lo sapesse.
    """
    arb = ast.parse(io.open(os.path.join(RADICE, p), encoding="utf-8").read(), filename=p)
    fuori = []
    for fn in [n for n in ast.walk(arb) if isinstance(n, ast.FunctionDef)]:
        a = fn.args
        nomi = [x.arg for x in a.args][len(a.args) - len(a.defaults):]
        nomi += [x.arg for x, v in zip(a.kwonlyargs, a.kw_defaults) if v is not None]
        for x in nomi:
            fuori.append((fn.name, x))
    return fuori


def controlla():
    err = []
    visti = set()
    # ### \u26d4 **IL `15(b)`, PRIMA DI TUTTO:** nessun default nelle firme.
    for p in file_fisica():
        for fn, arg in default_nelle_firme(p):
            err.append("`P-R1` `%s::%s`: il parametro `%s` HA UN VALORE DI DEFAULT. "
                       "### Il punto 15(b): un parametro NON PRESENTE e- un ERRORE, non "
                       "un comportamento a sorpresa -- e viene DALLA CONFIGURAZIONE. "
                       "### `CONFIG-1` ha misurato dove porta un valore che gira senza "
                       "che nessuno l-abbia scelto: 28 leggi su 31 SPENTE"
                       % (p, fn, arg))
    for p in file_fisica():
        for fn, c in sorted(_conta(p).items()):
            visti.add((p, fn))
            riga = RAMI.get((p, fn))
            if riga is None:
                err.append("`P-R1` `%s::%s`: ha %d rami e NON E- DICHIARATO. "
                           "### `A8`: un ramo silenzioso non e- un ramo -- si dice "
                           "QUANTI e A CHE SERVONO, con un ruolo di %s"
                           % (p, fn, c, list(RUOLI)))
                continue
            quanti, ruolo, perche = riga
            if ruolo not in RUOLI:
                err.append("`P-R1` `%s::%s`: ruolo %r fuori vocabolario: %s"
                           % (p, fn, ruolo, list(RUOLI)))
            if quanti != c:
                err.append("`P-R1` `%s::%s`: dichiara %d rami e l-AST ne conta %d. "
                           "### Un ramo e- NATO o MORTO senza che nessuno lo dicesse"
                           % (p, fn, quanti, c))
            if len(str(perche or "")) < 30:
                err.append("`P-R1` `%s::%s`: il `perche-` e- di %d caratteri. "
                           "### Dire QUANTI senza dire A CHE SERVONO non e- dichiararli"
                           % (p, fn, len(str(perche or ""))))
    for k in sorted(set(RAMI) - visti):
        err.append("`P-R1` `%s::%s`: DICHIARATO e l-AST non lo trova. ### O la funzione "
                   "e- sparita, o non ha piu- rami: la riga va tolta" % k)
    return err


def rapporto():
    per_ruolo = {}
    for (p, fn), (q, r, _x) in RAMI.items():
        per_ruolo.setdefault(r, [0, 0])
        per_ruolo[r][0] += 1
        per_ruolo[r][1] += q
    return per_ruolo


def _finto_default():
    """Il caso che DEVE fallire: un default, su una ### **COPIA** del sorgente."""
    import tempfile
    t = io.open(os.path.join(RADICE, "primo_ordine", "passo.py"),
                encoding="utf-8").read()
    t2 = t.replace("def senza_cache(moduli, azione):",
                   "def senza_cache(moduli, azione=None):", 1)
    assert t2 != t
    d = tempfile.mkdtemp()
    p = os.path.join(d, "finto.py")
    io.open(p, "w", encoding="utf-8", newline=NL).write(t2)
    arb = ast.parse(io.open(p, encoding="utf-8").read())
    trovati = []
    for fn in [n for n in ast.walk(arb) if isinstance(n, ast.FunctionDef)]:
        a = fn.args
        if a.defaults:
            trovati.append(fn.name)
    os.remove(p)
    os.rmdir(d)
    return "senza_cache" in trovati


def collaudo():
    ok = [0, 0]

    def esito(che, passa, nota=""):
        ok[1] += 1
        ok[0] += 1 if passa else 0
        print("  %-64s %s   %s" % (che, "PASSA" if passa else "### FALLISCE", nota))

    print("=" * 100)
    print("IL COLLAUDO DI `P-R1` -- nei DUE VERSI")
    print("=" * 100)
    tot = sum(q for q, _r, _p in RAMI.values())
    esito("sul disco: `P-R1` TACE", controlla() == [],
          "%d rami in %d funzioni" % (tot, len(RAMI)))
    esito("### il braccio sopra HA MATERIA (ci sono rami da dichiarare)", tot >= 15,
          "%d rami: se fosse 0 il braccio sarebbe un FALSO-UNO. ### Erano 27, e il "
          "punto 15(b) ne ha tolti 8" % tot)
    # --- un ramo NUOVO non dichiarato
    salva = dict(RAMI)
    try:
        del RAMI[("primo_ordine/passo.py", "valida_composizione")]
        esito("### DEVE scattare: una funzione con rami e NON dichiarata",
              any("NON E- DICHIARATO" in e for e in controlla()),
              "`A8`: un ramo silenzioso non e- un ramo")
    finally:
        RAMI.clear()
        RAMI.update(salva)
    # --- un conteggio SBAGLIATO
    salva2 = RAMI[("primo_ordine/passo.py", "valida_composizione")]
    try:
        RAMI[("primo_ordine/passo.py", "valida_composizione")] = (99, "validazione",
                                                                  salva2[2])
        esito("### DEVE scattare: un CONTEGGIO che non coincide con l-AST",
              any("l-AST ne conta" in e for e in controlla()),
              "### un ramo NATO o MORTO senza che nessuno lo dicesse")
    finally:
        RAMI[("primo_ordine/passo.py", "valida_composizione")] = salva2
    # --- un ruolo fuori vocabolario, e un `perche'` troppo corto
    try:
        RAMI[("primo_ordine/passo.py", "valida_composizione")] = (6, "quasi-validazione",
                                                                  salva2[2])
        esito("### DEVE scattare: un RUOLO fuori vocabolario",
              any("fuori vocabolario" in e for e in controlla()))
        RAMI[("primo_ordine/passo.py", "valida_composizione")] = (6, "validazione", "x")
        esito("### DEVE scattare: un `perche-` troppo corto",
              any("non e- dichiararli" in e for e in controlla()),
              "### dire QUANTI senza dire A CHE SERVONO non e- dichiararli")
    finally:
        RAMI[("primo_ordine/passo.py", "valida_composizione")] = salva2
    # --- una riga ORFANA
    try:
        RAMI[("primo_ordine/passo.py", "funzione_che_non_esiste")] = (1, "guardia",
                                                                      "x" * 40)
        esito("### DEVE scattare: una riga DICHIARATA che l-AST non trova",
              any("l-AST non lo trova" in e for e in controlla()))
    finally:
        RAMI.pop(("primo_ordine/passo.py", "funzione_che_non_esiste"), None)
    esito("NON deve scattare: rimesso tutto a posto, `P-R1` TACE", controlla() == [],
          "### i bracci di sopra scattavano per i loro casi finti")
    # --- E IL RAPPORTO: i `default` erano NOVE, e il punto `15(b)` li ha TOLTI
    r = rapporto()
    ng = r.get("guardia", [0, 0])
    # ### \u26d4 **IL `15(b)`: i default sono ZERO, e il braccio che DEVE scattare.**
    esito("`15(b)` i DEFAULT nelle firme della fisica sono ZERO",
          not any("VALORE DI DEFAULT" in e for e in controlla()),
          "### erano NOVE il 2026-10-09, e il punto 15(b) li ha TOLTI")
    esito("### DEVE scattare: un default in una firma di fisica",
          _finto_default(),
          "### misurato su una COPIA del sorgente, non sul file vero")
    esito("### e i `default` NON sono piu- nella tabella dei ruoli",
          "default" not in rapporto(),
          "### il debito e- PAGATO: 27 rami -> 19, e 9 default -> 0")
    esito("### e le `guardia` sono ZERO oggi, e lo dico invece di lasciarlo credere",
          ng[0] == 0,
          "### `A11`: se ce ne fosse una, andrebbe cercato l-ERRORE da cui protegge")
    print("=" * 100)
    print("IL COLLAUDO DI `P-R1`: %d su %d   %s"
          % (ok[0], ok[1], "### TUTTI PASSATI" if ok[0] == ok[1] else "### CI SONO BUCHI"))
    print("=" * 100)
    return 0 if ok[0] == ok[1] else 1


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    if "--collaudo" in argv:
        return collaudo()
    err = controlla()
    tot = sum(q for q, _r, _p in RAMI.values())
    print("  `P-R1`: %d rami dichiarati in %d funzioni, su %d file di fisica"
          % (tot, len(RAMI), len(file_fisica())))
    for r, (nf, nr) in sorted(rapporto().items()):
        print("     %-14s %2d funzioni, %2d rami%s"
              % (r, nf, nr,
                 "   ### un DEBITO: il punto 15(b) lo vietera-" if r == "default"
                 else ("   ### `A11`: cercare l-errore" if r == "guardia" else "")))
    for e in err[:14]:
        print("  ### %s" % e)
    print("  ### %d errori" % len(err))
    return 1 if err else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
