# -*- coding: utf-8 -*-
"""PUNTO `12(a)` — **ANCHE I CONTROLLI STANNO NELL'INDICE, e la macchina lo verifica.**

### ⛔ **LA BIIEZIONE, nei due versi, E CON DUE SEVERITA' DIVERSE** *(lo dice il
mandato, e la differenza non e' arbitraria)*:

| | il caso | che succede | perche' |
|---|---|---|---|
| `1` | il **codice dichiara un ID** che ### **non e' nell'indice** | ### ⛔ **RIFIUTATO** | un presidio che cita un ID inesistente ### **ha un riferimento rotto**, e il campo serviva a non averne |
| `2` | una **voce `classe: PRESIDIO`** che ### **nessun codice dichiara** | ### ⚠ **SEGNALE** | potrebbe essere un presidio ### **vero ma scritto in shell** *(i `H-*` vivono in `.githooks/`)*, o ### **proposto e non cablato** *(`H-ETC-1`, `H-ETC-2`)*. ### **Rifiutarlo vorrebbe dire rifiutare un fatto vero** |

### ⭐ **E LA DICHIARAZIONE SI LEGGE VIA AST, non per regex**, per la ragione di
sempre in questo repo: ### **una regex troverebbe `PRESIDIO` anche dentro un commento o
una stringa**, e ### **un presidio che si lascia ingannare da un commento non e' un
presidio.**

### ⚠ **DUE FORME DI DICHIARAZIONE, e il perche':**

- **`PRESIDIO = "<id>"`** — un file, ### **un** presidio;
- **`PRESIDI = {"<id>": "<nome di funzione o percorso>"}`** — un file che ne tiene
  ### **molti** *(`csv/indice.py` ne ha dodici: un solo `PRESIDIO` non potrebbe
  nominarli)*.

### ⛔ **E IL VALORE SI VERIFICA:** se e' un percorso, ### **il file deve esistere**;
se e' un nome, ### **la funzione deve esistere nel modulo** — letta via AST.
### **Altrimenti la dichiarazione sarebbe una promessa senza niente dietro.**
"""
import ast
import io
import json
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
sys.path.insert(0, _QUI)

NL = chr(10)
VOCI = os.path.join(RADICE, "doc", "indice", "voci.jsonl")

PRESIDIO = "P-C1"

# ### ⛔ **I FILE CHE POSSONO DICHIARARE UN PRESIDIO.** Elenco ### **chiuso**: un
# ### presidio che vivesse in un file non elencato ### **sarebbe invisibile**, e lo dico
# ### invece di scandire tutto il repo -- una scansione cieca ### **troverebbe anche i
# ### collaudi**, che dichiarano gli ID per provarli.
SORGENTI = (
    "csv/_presidi_era2.py",
    "csv/_metodi_era2.py",
    "csv/_controlli_nell_indice.py",
    "csv/_testo_e_metadati.py",
    "csv/_rami_era2.py",
    "csv/_replay_registri.py",
    "csv/_citazioni_strutturate.py",
    "csv/_rif_nel_codice.py",
    "csv/_un_solo_esecutore.py",
    "csv/_modularita_era2.py",
    "csv/_confronti_e_dati.py",
    "csv/_id_nuovo.py",
    "csv/_albero_era2.py",
    "csv/_barriera.py",
    # ### ⚠ **E UN PRESIDIO PUO- VIVERE SOTTO `primo_ordine/`:** `P-GRAFO` gira
    # ### ### **dentro il passo**, non in un `pre-commit` -- e se le `SORGENTI` guardassero
    # ### ### **solo `csv/`**, la sua voce risulterebbe ### **una tenda** mentre e- cablata.
    "primo_ordine/grafo.py",
    "primo_ordine/determinismo.py",
    "primo_ordine/leggi/schema.py",
    "primo_ordine/simmetrie.py",
    "primo_ordine/collauda.py",
    "csv/indice.py",
    "csv/_hook_presidi.py",
    "csv/_hook_id_obbligatorio.py",
    "csv/_file_fisica.py",
    "csv/_struttura_regole.py",
)


def voci():
    return [json.loads(r) for r in io.open(VOCI, encoding="utf-8").read().split(NL)
            if r.strip()]


def _costanti(p):
    """Le costanti di modulo di un file, ### **via AST.**"""
    arb = ast.parse(io.open(p, encoding="utf-8").read(), filename=p)
    d, funzioni = {}, set()
    for n in arb.body:
        if isinstance(n, ast.Assign) and len(n.targets) == 1 \
                and isinstance(n.targets[0], ast.Name):
            try:
                d[n.targets[0].id] = ast.literal_eval(n.value)
            except Exception:
                pass
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
            funzioni.add(n.name)
    return d, funzioni


def dichiarati():
    """### `{id: (file, bersaglio)}` — cio' che ### **il codice dichiara.**"""
    fuori = {}
    for rel in SORGENTI:
        p = os.path.join(RADICE, rel)
        if not os.path.exists(p):
            continue
        d, funzioni = _costanti(p)
        if isinstance(d.get("PRESIDIO"), str):
            fuori[d["PRESIDIO"]] = (rel, None, funzioni)
        for idv, bers in (d.get("PRESIDI") or {}).items():
            fuori[idv] = (rel, bers, funzioni)
    return fuori


def controlla(v=None):
    """### Gli errori *(che RIFIUTANO)*. ### **I segnali stanno in `segnali()`.**"""
    v = voci() if v is None else v
    per = {x["id"]: x for x in v}
    err = []
    for idv, (rel, bers, funzioni) in sorted(dichiarati().items()):
        if idv not in per:
            err.append("`P-C1` `%s`: `%s` DICHIARA questo ID e NON E- NELL-INDICE. "
                       "### Un presidio che cita un ID inesistente ha un riferimento "
                       "ROTTO: la voce si crea con `crea-lotto`" % (idv, rel))
            continue
        if per[idv]["classe"] != "PRESIDIO":
            err.append("`P-C1` `%s`: `%s` lo dichiara come presidio, e la sua voce ha "
                       "`classe: %s`. ### La classe e- un CAMPO: o la voce e- un "
                       "`PRESIDIO`, o quel codice non e- un presidio"
                       % (idv, rel, per[idv]["classe"]))
        if bers is None:
            continue
        # ### ⛔ **IL BERSAGLIO SI VERIFICA**: una dichiarazione senza niente dietro
        # ### ### **e- una promessa**, e questo repo ne ha gia- avute.
        if "/" in str(bers) or str(bers).endswith((".yml", ".yaml")):
            if not os.path.exists(os.path.join(RADICE, str(bers))):
                err.append("`P-C1` `%s`: `%s` lo dichiara su `%s`, e QUEL FILE NON "
                           "ESISTE" % (idv, rel, bers))
        elif str(bers) not in funzioni:
            err.append("`P-C1` `%s`: `%s` lo dichiara sulla funzione `%s`, e QUELLA "
                       "FUNZIONE NON ESISTE nel modulo (letto via AST)"
                       % (idv, rel, bers))
    return err


def segnali(v=None):
    """### I SEGNALI: una voce `PRESIDIO` che ### **nessun codice dichiara.**

    ### ⚠ **NON RIFIUTANO**, e il mandato lo dice *(`A9`)*: un presidio puo- essere
    ### **vero e scritto in shell** *(i `H-*` vivono in `.githooks/`)*, oppure
    ### **proposto e non cablato.** ### **Rifiutare un fatto vero non e- un presidio: e-
    un impedimento.**
    """
    v = voci() if v is None else v
    dich = set(dichiarati())
    fuori = []
    for x in sorted(v, key=lambda y: y["id"]):
        if x["classe"] == "PRESIDIO" and x["id"] not in dich:
            fuori.append("`P-C1` segnale `%s`: voce `PRESIDIO` che NESSUN CODICE "
                         "DICHIARA. ### O vive in shell (`.githooks/`), o e- PROPOSTO e "
                         "non cablato, o e- una tenda (`A9`). `fonte`: %s"
                         % (x["id"], x.get("fonte") or "(vuota)"))
    return fuori


# =====================================================================================
#   IL COLLAUDO -- NEI DUE VERSI
# =====================================================================================

def collaudo():
    ok = [0, 0]

    def esito(che, passa, nota=""):
        ok[1] += 1
        ok[0] += 1 if passa else 0
        print("  %-64s %s   %s" % (che, "PASSA" if passa else "### FALLISCE", nota))

    v = voci()
    dich = dichiarati()
    print("=" * 100)
    print("IL COLLAUDO DI `P-C1` -- nei DUE VERSI")
    print("=" * 100)
    esito("sul disco: `P-C1` TACE", controlla(v) == [],
          "%d presidi dichiarati dal codice" % len(dich))
    esito("### il braccio sopra HA MATERIA (il codice dichiara qualcosa)", len(dich) >= 9,
          "%d: se fosse 0 il braccio sarebbe un FALSO-UNO" % len(dich))
    esito("### e i bersagli ESISTONO TUTTI (funzione o file, via AST)",
          not any("NON ESISTE" in e for e in controlla(v)),
          "una dichiarazione senza niente dietro e- UNA PROMESSA")
    # --- il verso che DEVE scattare: un ID dichiarato e NON nell'indice
    v2 = [x for x in v if x["id"] != "P-M1"]
    esito("### DEVE scattare: il codice dichiara un ID che NON e- nell-indice",
          any("NON E- NELL-INDICE" in e for e in controlla(v2)),
          "`P-M1` tolto dall-indice per il collaudo")
    # --- una voce con la classe SBAGLIATA
    v3 = [dict(x, classe="CURA") if x["id"] == "P-M1" else x for x in v]
    esito("### DEVE scattare: la voce esiste ma NON ha `classe: PRESIDIO`",
          any("quel codice non e- un presidio" in e for e in controlla(v3)),
          "### la classe e- un CAMPO, e il campo decide")
    # --- i SEGNALI hanno materia, e NON rifiutano
    sg = segnali(v)
    esito("i SEGNALI hanno materia (voci `PRESIDIO` che il codice non dichiara)",
          len(sg) > 0, "%d segnali: sono i `H-*` (shell) e i proposti" % len(sg))
    esito("### e i segnali NON stanno fra gli errori: SEGNALANO, non impediscono",
          not any("segnale" in e for e in controlla(v)),
          "`A9`: rifiutare un fatto VERO non e- un presidio")
    esito("NON deve scattare: sul disco vero, `P-C1` TACE di nuovo", controlla() == [],
          "### i bracci di sopra scattavano per i loro casi finti")
    print("=" * 100)
    print("IL COLLAUDO DI `P-C1`: %d su %d   %s"
          % (ok[0], ok[1], "### TUTTI PASSATI" if ok[0] == ok[1] else "### CI SONO BUCHI"))
    print("=" * 100)
    return 0 if ok[0] == ok[1] else 1


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    if "--collaudo" in argv:
        return collaudo()
    err = controlla()
    sg = segnali()
    dich = dichiarati()
    print("  `P-C1`: %d presidi DICHIARATI dal codice, %d sorgenti guardate"
          % (len(dich), len(SORGENTI)))
    for e in err[:14]:
        print("  ### %s" % e)
    if "--segnali" in argv or not err:
        for s in sg:
            print("  ~ %s" % s)
    print("  ### %d errori, %d segnali%s"
          % (len(err), len(sg), "" if err else "   (gli errori RIFIUTANO, i segnali NO)"))
    return 1 if err else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
