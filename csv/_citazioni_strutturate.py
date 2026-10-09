# -*- coding: utf-8 -*-
"""PUNTO `13(d)` — **LE CITAZIONI DIVENTANO STRUTTURATE, e si verificano su `git show`.**

> ### ⛔ *«le CITAZIONI diventano STRUTTURATE `{file, riga, commit, impronta}` e si
> verificano su `git show` — le citazioni libere gia' scritte **restano come
> reperti**»*.

### ⭐ **PERCHE' IL `commit` E' LA PARTE CHE CONTA, e non il `file:riga`.** Il par.`2`
di `CLAUDE.md` dice: *«CERCA PER NOME DI FUNZIONE O DI FLAG, MAI PER RIGA: i numeri di
riga nei documenti sono di blob vecchi e ### **SONO SHIFTATI**»*.
### ⛔ **Una citazione `file:riga` SENZA un commit e' percio' destinata a diventare
falsa** — non per malizia, ### **per il tempo che passa.**

### ✅ **Con il `commit`, invece, la citazione e' VERA PER SEMPRE:** `git show
<commit>:<file>` ### **da' sempre gli stessi byte**, quindi la riga `N` e' ### **quella**
e la sua impronta ### **non cambia mai.** E chi legge sa ### **dove guardare adesso**
*(cerca la frase)* e ### **dov'era allora** *(l'indirizzo)*.

### ⚠ **E LE `10` CITAZIONI DA CUI PARTE QUESTO REGISTRO NON LE HO INVENTATE:**
sono quelle di `csv/_righe_indirizzate.py`, ### **date dal guardiano** e gia' verificate
una volta. Qui ### **guadagnano il commit e l'impronta**, e diventano
### **ri-verificabili.**
"""
import hashlib
import io
import json
import os
import subprocess
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
sys.path.insert(0, _QUI)

NL = chr(10)
D = os.path.join(RADICE, "doc", "indice")
CIT = os.path.join(D, "citazioni.jsonl")

PRESIDIO = "P-T3"

CAMPI = ("id", "file", "riga", "commit", "impronta", "frase")


def _jsonl(p):
    if not os.path.exists(p):
        return []
    return [json.loads(r) for r in io.open(p, encoding="utf-8").read().split(NL)
            if r.strip()]


def righe_a(commit, percorso):
    """### Le righe di un file ### **a un commit**, da `git show`.

    ### ⛔ **IN BINARIO, e poi `utf-8`:** `git show` in modo testo
    ### **tradurrebbe i fine-riga**, e ### **la trappola CRLF di questo repo e' scritta
    nel par.`7`.**
    """
    r = subprocess.run(["git", "show", "%s:%s" % (commit, percorso)],
                       cwd=RADICE, capture_output=True)
    if r.returncode != 0:
        return None
    return r.stdout.decode("utf-8", "replace").split(NL)


def impronta_riga(testo):
    """### L-impronta di una riga: ### **gli spazi normalizzati, il resto NO.**

    ### ⚠ **Si normalizzano SOLO gli spazi** *(`" ".join(split())`)*, e il perche-
    e- stretto: un file puo- essere ri-indentato, e ### **l-indentazione non e- la
    citazione.** ### ⛔ **Il TESTO invece non si tocca:** niente accenti piegati,
    niente markdown tolto — ### **se cambia una parola, l-impronta DEVE cambiare.**
    """
    return hashlib.sha1(" ".join(str(testo).split()).encode("utf-8")).hexdigest()[:16]


def controlla(righe=None):
    """### Gli errori, o `[]`. ### **Ogni citazione si ri-verifica su `git show`.**"""
    err = []
    righe = _jsonl(CIT) if righe is None else righe
    voci = {x["id"] for x in _jsonl(os.path.join(D, "voci.jsonl"))}
    etich = {x["id"] for x in _jsonl(os.path.join(D, "etichette_rimosse.jsonl"))}
    visti = set()
    for k, c in enumerate(righe, 1):
        manca = sorted(set(CAMPI) - set(c))
        if manca:
            err.append("`P-T3` riga %d: mancano i campi %s" % (k, manca))
            continue
        extra = sorted(set(c) - set(CAMPI))
        if extra:
            err.append("`P-T3` riga %d: campi NON previsti %s: il vocabolario e- CHIUSO"
                       % (k, extra))
        chiave = (c["id"], c["file"], c["riga"], c["commit"])
        if chiave in visti:
            err.append("`P-T3` riga %d: citazione DOPPIA %s" % (k, chiave))
        visti.add(chiave)
        # ### ⛔ **L-ID DEVE ESISTERE**: una citazione verso il nulla non e- una
        # ### citazione.
        if c["id"] not in voci and c["id"] not in etich:
            err.append("`P-T3` `%s`: l-ID della citazione NON E- NELL-INDICE (ne- fra le "
                       "etichette rimosse)" % c["id"])
        if not isinstance(c["riga"], int) or c["riga"] < 1:
            err.append("`P-T3` `%s`: `riga` %r: serve un intero >= 1"
                       % (c["id"], c["riga"]))
            continue
        rr = righe_a(c["commit"], c["file"])
        if rr is None:
            err.append("`P-T3` `%s`: `git show %s:%s` NON DA- NIENTE. ### Il commit non "
                       "c-e-, o il file non c-era a quel commit: ### una citazione che "
                       "non si puo- ri-leggere NON E- UNA CITAZIONE"
                       % (c["id"], c["commit"][:10], c["file"]))
            continue
        if c["riga"] > len(rr):
            err.append("`P-T3` `%s`: a `%s` il file `%s` ha %d righe, e la %d non esiste"
                       % (c["id"], c["commit"][:10], c["file"], len(rr), c["riga"]))
            continue
        riga = rr[c["riga"] - 1]
        att = impronta_riga(riga)
        if att != c["impronta"]:
            err.append("`P-T3` `%s`: l-IMPRONTA della riga %d di `%s` a `%s` e- `%s`, e "
                       "la citazione dichiara `%s`. ### Una citazione STRUTTURATA si "
                       "ri-verifica: se non torna, O il commit e- sbagliato O l-impronta "
                       "e- stata scritta a mano"
                       % (c["id"], c["riga"], c["file"], c["commit"][:10], att,
                          c["impronta"]))
            continue
        # ### ✅ **E LA FRASE DEVE STARCI DENTRO:** l-impronta prova che la riga e-
        # ### ### **quella**, la frase prova che la citazione ### **parla di quello.**
        if " ".join(str(c["frase"]).split()).upper() \
                not in " ".join(riga.split()).upper():
            err.append("`P-T3` `%s`: l-impronta torna, ma LA FRASE NON STA NELLA RIGA. "
                       "### L-impronta dice che la riga e- QUELLA; la frase dice che la "
                       "citazione PARLA DI QUELLO: servono entrambe" % c["id"])
    return err


# =====================================================================================
#   LA VIA UNICA DI SCRITTURA: si CALCOLA l'impronta, non si scrive
# =====================================================================================

def aggiungi(id_, percorso, n, commit, frase):
    """### Costruisce la riga, ### **calcolando l-impronta da `git show`.**

    ### ⛔ **L-IMPRONTA NON SI SCRIVE A MANO**, e il perche- e- quello di sempre in
    questo repo: ### **un numero ricopiato non ha provenienza** *(`L-NUMERI`)*.
    """
    rr = righe_a(commit, percorso)
    assert rr is not None, "`git show %s:%s` non da- niente" % (commit, percorso)
    assert 1 <= n <= len(rr), "la riga %d non esiste (%d righe)" % (n, len(rr))
    riga = rr[n - 1]
    assert " ".join(str(frase).split()).upper() in " ".join(riga.split()).upper(), (
        "### LA FRASE NON STA NELLA RIGA %d: <<%s>>" % (n, " ".join(riga.split())[:140]))
    return {"id": id_, "file": percorso, "riga": n, "commit": commit,
            "impronta": impronta_riga(riga), "frase": frase}


def scrivi(righe):
    io.open(CIT, "w", encoding="utf-8", newline=NL).write(
        NL.join(json.dumps(r, ensure_ascii=False) for r in
                sorted(righe, key=lambda x: (x["id"], x["file"], x["riga"]))) + NL)


# =====================================================================================
#   IL COLLAUDO -- NEI DUE VERSI
# =====================================================================================

def collaudo():
    ok = [0, 0]

    def esito(che, passa, nota=""):
        ok[1] += 1
        ok[0] += 1 if passa else 0
        print("  %-64s %s   %s" % (che, "PASSA" if passa else "### FALLISCE", nota))

    righe = _jsonl(CIT)
    print("=" * 100)
    print("IL COLLAUDO DI `P-T3` -- nei DUE VERSI")
    print("=" * 100)
    esito("sul disco: `P-T3` TACE", controlla() == [], "%d citazioni" % len(righe))
    esito("### il braccio sopra HA MATERIA (ci sono citazioni da ri-verificare)",
          len(righe) >= 5, "%d: se fosse 0 il braccio sarebbe un FALSO-UNO" % len(righe))
    esito("### e ogni citazione porta un COMMIT diverso da `HEAD` o uguale, ma SEMPRE un "
          "commit", all(len(str(c.get("commit") or "")) >= 7 for c in righe),
          "### senza il commit una citazione `file:riga` e- destinata a diventare falsa")
    base = righe[0] if righe else None
    assert base is not None
    # --- l'IMPRONTA sbagliata
    esito("### DEVE scattare: un-IMPRONTA sbagliata",
          any("l-IMPRONTA della riga" in e
              for e in controlla([dict(base, impronta="0" * 16)])),
          "### una citazione STRUTTURATA si RI-VERIFICA")
    # --- la RIGA sbagliata
    esito("### DEVE scattare: la RIGA spostata di uno",
          controlla([dict(base, riga=base["riga"] + 1)]) != [],
          "### il par.`2`: i numeri di riga SONO SHIFTATI, e per questo c-e- il commit")
    # --- il COMMIT inesistente
    esito("### DEVE scattare: un COMMIT che non esiste",
          any("NON DA- NIENTE" in e
              for e in controlla([dict(base, commit="0" * 40)])),
          "### una citazione che non si puo- ri-leggere NON E- UNA CITAZIONE")
    # --- la FRASE che non c'e'
    esito("### DEVE scattare: la FRASE che non sta nella riga",
          any("LA FRASE NON STA NELLA RIGA" in e
              for e in controlla([dict(base, frase="una frase che non c-e- mai stata")])),
          "### l-impronta dice che la riga e- QUELLA, la frase che PARLA DI QUELLO")
    # --- un ID che non esiste
    esito("### DEVE scattare: un ID che NON e- nell-indice",
          any("NON E- NELL-INDICE" in e
              for e in controlla([dict(base, id="ID-CHE-NON-ESISTE")])),
          "### una citazione verso il nulla non e- una citazione")
    # --- un campo in piu', e uno in meno
    esito("### DEVE scattare: un campo IN PIU-",
          any("vocabolario e- CHIUSO" in e
              for e in controlla([dict(base, inventato=1)])))
    esito("### DEVE scattare: un campo che MANCA",
          any("mancano i campi" in e
              for e in controlla([{k: v for k, v in base.items() if k != "frase"}])))
    # --- una citazione DOPPIA
    esito("### DEVE scattare: una citazione DOPPIA",
          any("DOPPIA" in e for e in controlla([base, dict(base)])))
    # --- e l'IMPRONTA normalizza gli SPAZI e NON il testo
    esito("### l-impronta normalizza gli SPAZI *(un file si ri-indenta)*",
          impronta_riga("  a   b ") == impronta_riga("a b"),
          "### l-indentazione non e- la citazione")
    esito("### e NON normalizza il TESTO: se cambia una parola, CAMBIA",
          impronta_riga("a b") != impronta_riga("a c"),
          "### se cambiasse una parola senza cambiare l-impronta, non proverebbe niente")
    esito("NON deve scattare: sul disco vero, `P-T3` TACE di nuovo", controlla() == [],
          "### i bracci di sopra scattavano per i loro casi finti")
    print("=" * 100)
    print("IL COLLAUDO DI `P-T3`: %d su %d   %s"
          % (ok[0], ok[1], "### TUTTI PASSATI" if ok[0] == ok[1] else "### CI SONO BUCHI"))
    print("=" * 100)
    return 0 if ok[0] == ok[1] else 1


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    if "--collaudo" in argv:
        return collaudo()
    err = controlla()
    righe = _jsonl(CIT)
    print("  `P-T3`: %d citazioni STRUTTURATE, ri-verificate su `git show`" % len(righe))
    for e in err[:14]:
        print("  ### %s" % e)
    print("  ### %d errori" % len(err))
    return 1 if err else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
