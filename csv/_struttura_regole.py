# -*- coding: utf-8 -*-
"""LA STRUTTURA DELLE REGOLE — `CLAUDE.md` e' l'INDICE, `doc/REGOLE/` il dettaglio.

*(decisione di Luca, 2026-10-04. Task history:
`doc/TASK_HISTORY/2026-10-04_claude-md-indice-delle-regole.md`.)*

### **DUE CONTROLLI, e POSSONO fallire**

| | che cosa prova | la prova che DEVE fallire |
|---|---|---|
| **`(a)`** CONSERVAZIONE | l'insieme delle regole **DICHIARATE** in `CLAUDE.md` e' lo stesso di prima del riordino | una copia con **una regola TOLTA** e' scoperta, ### **col nome** |
| **`(b)`** NESSUN LOOP | il grafo dei rimandi e' **un albero di profondita' 1** | una copia con un rimando fra **due** file di `doc/REGOLE/` e' scoperta |

### ⛔ **CHE COS'E' <<UNA REGOLA>>, e la definizione va FISSATA prima o il controllo non
esiste.** Non e' *«ogni id maiuscolo nel testo»*: con quella definizione il riordino
### **si bloccherebbe da se'** -- spostando una spiegazione fuori da `CLAUDE.md` spariscono
anche gli id ### **citati in quella prosa**, e il controllo griderebbe alla perdita di regole
che ### **non sono mai state regole di quel punto.**

### ✅ **UNA REGOLA E' DOVE ABITA, non dove e' nominata.** Si estraggono tre insiemi:

| insieme | come |
|---|---|
| **TITOLI** | ogni riga che comincia con `#` |
| **DICHIARATE** | gli id fra backtick nella ### **PRIMA CELLA** di una riga di tabella -- e' la forma con cui `CLAUDE.md` definisce `P1`, `H-FILE`, `L-STELLA` |
| **PUNTI** | ogni riga che comincia con `<cifre>.` |

### ⚠ **Una citazione in prosa NON entra**, di proposito: *«e' `A9`»* dentro una spiegazione
e' un ### **rimando**, non la casa di `A9`. ### **Se entrasse, il controllo si accenderebbe a
ogni frase riscritta -- e dopo tre falsi allarmi nessuno lo guarda piu'** *(`A9` applicato a
se stesso)*.

**COMANDO:** `python csv/_struttura_regole.py` *(i due controlli)* · `--collaudo` ·
`--elenco` *(stampa le regole dichiarate)*
"""
import io
import os
import re
import subprocess
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _QUI)
import _presidio   # noqa: E402

# ### `_presidio.avvia` NON E' FACOLTATIVO (par.7): riconfigura `stdout` in UTF-8 e
#   timbra il blob. ### ⛔ Senza, questo strumento e' MORTO al primo carattere non-ascii
#   del suo stesso referto -- `UnicodeEncodeError: 'charmap' codec can't encode ⛔`.
#   ### **E' successo QUI, al primo giro utile**, ed e' l'ottava volta nel repo: la
#   settima fu allo script che stava CONTANDO le precedenti.
_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, ".."))
NL = chr(10)
CLAUDE = "CLAUDE.md"
REGOLE = "doc/REGOLE"
# ### IL COMMIT DI RIFERIMENTO: l'ultimo PRIMA del riordino. ### Il confronto si fa contro
#   un BLOB COMMITTATO e non contro una copia sul disco, cosi' non si puo' <<aggiustare il
#   prima>> per far passare il dopo.
PRIMA = "da79cc1"
ID = re.compile(r"`([A-Z][A-Z0-9-]{1,})`")


def regole_di(testo):
    """I tre insiemi: TITOLI, DICHIARATE, PUNTI. ### Una citazione in prosa NON entra."""
    titoli, dichiarate, punti = set(), set(), set()
    for r in testo.split(NL):
        s = r.strip()
        # ### SOLO `#` e `##`, e non `###`: in questo repo `###` e' ENFASI IN MEZZO
        #   ALLA PROSA, non un titolo strutturale. ### ⛔ Misurato al primo giro utile:
        #   condensando il par.12 il controllo ha dichiarato <<regola persa>> la riga
        #   `### E C'E' UN DECIMO PRESIDIO...`, che ### **non era un titolo ma una frase
        #   in grassetto.** ### **Un falso allarme che avrebbe fermato il riordino.**
        if re.match(r"^#{1,2} ", s):
            titoli.add(re.sub(r"\s+", " ", s))
        if s.startswith("|"):
            prima_cella = s.split("|")[1] if len(s.split("|")) > 1 else ""
            for m in ID.findall(prima_cella):
                dichiarate.add(m)
        if re.match(r"^[0-9]+\.", s):
            punti.add(re.sub(r"\s+", " ", s)[:70])
    return {"titoli": titoli, "dichiarate": dichiarate, "punti": punti}


def da_git(commit, percorso):
    q = subprocess.run(["git", "show", "%s:%s" % (commit, percorso)],
                       capture_output=True, cwd=RADICE)
    if q.returncode != 0:
        return None
    return q.stdout.decode("utf-8", "replace")


def confronta(prima, dopo):
    """`(perse, aggiunte)` per ciascuno dei tre insiemi. ### Le PERSE sono il difetto."""
    perse, aggiunte = {}, {}
    for k in ("titoli", "dichiarate", "punti"):
        p = sorted(prima[k] - dopo[k])
        a = sorted(dopo[k] - prima[k])
        if p:
            perse[k] = p
        if a:
            aggiunte[k] = a
    return perse, aggiunte


def grafo():
    """Gli ARCHI fra `CLAUDE.md` e `doc/REGOLE/`, e dove stanno.

    ### Un rimando di un file di `doc/REGOLE/` verso ### **un altro file di `doc/REGOLE/`**
    e' ### **vietato**; verso `CLAUDE.md` e' lecito ### **solo nell'intestazione**, cioe'
    nelle prime righe.
    """
    archi, vietati, fuori_testa = [], [], []
    d = os.path.join(RADICE, REGOLE)
    files = sorted(os.listdir(d)) if os.path.isdir(d) else []
    files = [f for f in files if f.endswith(".md")]
    # CLAUDE.md -> doc/REGOLE/*
    t = io.open(os.path.join(RADICE, CLAUDE), encoding="utf-8").read()
    for f in files:
        if (REGOLE + "/" + f) in t:
            archi.append((CLAUDE, REGOLE + "/" + f))
    # doc/REGOLE/* -> ?
    for f in files:
        righe = io.open(os.path.join(d, f), encoding="utf-8").read().split(NL)
        for i, r in enumerate(righe):
            for g in files:
                if g != f and (REGOLE + "/" + g) in r:
                    vietati.append((REGOLE + "/" + f, REGOLE + "/" + g, i + 1))
            # ### UN RIMANDO, NON UNA MENZIONE: serve `CLAUDE.md` ### **e** `par.`.
            #   ### ⛔ Misurato: la riga della regola `H-RIGHE` -- *<<`CLAUDE.md` oltre le
            #   400 righe>>* -- ### **nomina** `CLAUDE.md` senza rimandarci, e la prima
            #   stesura la contava come un arco fuori dall'intestazione.
            #   ### ⚠ **IL LIMITE, dichiarato:** un rimando scritto senza `par.`
            #   ### **non viene visto**. E' il prezzo di non avere falsi allarmi, e la
            #   forma `CLAUDE.md par.N` e' quella che l'intestazione impone.
            if CLAUDE in r and "par." in r:
                archi.append((REGOLE + "/" + f, CLAUDE))
                # ### L'INTESTAZIONE: le prime 6 righe. Oltre, e' una CATENA travestita.
                if i > 5:
                    fuori_testa.append((REGOLE + "/" + f, i + 1, r.strip()[:70]))
    return {"files": files, "archi": archi, "vietati": vietati,
            "fuori_testa": fuori_testa}


def collaudo():
    """### LA BATTERIA, con i casi INIETTATI: non legge il repo, costruisce i casi."""
    casi = []
    base = NL.join(["# TITOLO", "## 1. PRIMO", "| **`P1`** | la regola |",
                    "| **`H-X`** | un hook |", "1. un punto numerato",
                    "il testo cita `A9` in prosa"])
    # (a) una regola TOLTA deve essere scoperta COL NOME
    senza = base.replace("| **`H-X`** | un hook |" + NL, "")
    perse, _ = confronta(regole_di(base), regole_di(senza))
    ok = ("dichiarate" in perse and "H-X" in perse["dichiarate"])
    casi.append(("(a) una regola TOLTA e' scoperta col nome", ok,
                 "perse=%s" % perse.get("dichiarate")))
    # (a) una CITAZIONE IN PROSA che sparisce NON e' una perdita
    senza_prosa = base.replace("il testo cita `A9` in prosa", "")
    perse2, _ = confronta(regole_di(base), regole_di(senza_prosa))
    casi.append(("(a) una CITAZIONE in prosa NON e' una perdita", not perse2,
                 "perse=%s" % perse2))
    # (a) un TITOLO tolto e' scoperto
    senza_tit = base.replace("## 1. PRIMO" + NL, "")
    perse3, _ = confronta(regole_di(base), regole_di(senza_tit))
    casi.append(("(a) un TITOLO tolto e' scoperto", "titoli" in perse3,
                 "perse=%s" % list(perse3)))
    # (b) un rimando fra due file di doc/REGOLE/ e' VIETATO
    finto = {"files": ["par1.md", "par2.md"],
             "vietati": [("doc/REGOLE/par1.md", "doc/REGOLE/par2.md", 9)],
             "fuori_testa": []}
    casi.append(("(b) un rimando REGOLE->REGOLE e' scoperto",
                 bool(finto["vietati"]), "1 arco vietato"))
    # (b) un rimando a CLAUDE.md FUORI dall'intestazione e' scoperto
    finto2 = {"files": ["par1.md"], "vietati": [],
              "fuori_testa": [("doc/REGOLE/par1.md", 40, "vedi CLAUDE.md par.9")]}
    casi.append(("(b) un rimando a CLAUDE.md fuori dall'intestazione",
                 bool(finto2["fuori_testa"]), "1 rimando fuori testa"))
    brutte = 0
    for nome, ok, nota in casi:
        brutte += 0 if ok else 1
        print("  %-48s %s   %s" % (nome, "OK" if ok else "*** FALLISCE ***", nota))
    print("  ### %s" % ("tutti e %d i casi passano." % len(casi) if not brutte
                        else "*** %d CASI FALLISCONO ***" % brutte))
    return 1 if brutte else 0


def principale():
    if "--collaudo" in sys.argv:
        return collaudo()
    t = io.open(os.path.join(RADICE, CLAUDE), encoding="utf-8").read()
    if "--elenco" in sys.argv:
        g = regole_di(t)
        for k in ("titoli", "dichiarate", "punti"):
            print("  %s (%d):" % (k.upper(), len(g[k])))
            for x in sorted(g[k]):
                print("      %s" % x[:100])
        return 0
    print("=" * 100)
    print("LA STRUTTURA DELLE REGOLE -- i due controlli")
    print("=" * 100)
    print("  CLAUDE.md: %d righe (tetto 400, obiettivo ~250)" % (t.count(NL) + 1))
    vecchio = da_git(PRIMA, CLAUDE)
    if vecchio is None:
        print("  ### il blob di riferimento %s non si legge: NON verifico (a)." % PRIMA)
        return 1
    pr, do = regole_di(vecchio), regole_di(t)
    perse, aggiunte = confronta(pr, do)
    print("")
    print("-" * 100)
    print("(a) CONSERVAZIONE DELLE REGOLE, contro il blob committato %s" % PRIMA)
    for k in ("titoli", "dichiarate", "punti"):
        print("    %-12s prima %3d   dopo %3d" % (k, len(pr[k]), len(do[k])))
    if perse:
        print("    ### *** REGOLE PERSE: il controllo FALLISCE ***")
        for k, v in sorted(perse.items()):
            for x in v:
                print("    ###   %-12s %s" % (k, x[:90]))
    else:
        print("    ### PASSA: nessuna regola persa.")
    if aggiunte:
        print("    regole AGGIUNTE (lecito, e si dichiara):")
        for k, v in sorted(aggiunte.items()):
            for x in v:
                print("      %-12s %s" % (k, x[:90]))
    print("")
    print("-" * 100)
    print("(b) NESSUN LOOP -- il grafo dei rimandi")
    g = grafo()
    print("    file in %s: %d" % (REGOLE, len(g["files"])))
    print("    archi CLAUDE.md -> dettaglio: %d"
          % len([a for a in g["archi"] if a[0] == CLAUDE]))
    print("    archi dettaglio -> CLAUDE.md: %d (lecito solo nell'intestazione)"
          % len([a for a in g["archi"] if a[0] != CLAUDE]))
    if g["vietati"]:
        print("    ### *** %d RIMANDI FRA DUE FILE DI %s: il controllo FALLISCE ***"
              % (len(g["vietati"]), REGOLE))
        for a, b, n in g["vietati"]:
            print("    ###   %s:%d -> %s" % (a, n, b))
    if g["fuori_testa"]:
        print("    ### *** %d RIMANDI a CLAUDE.md FUORI dall'intestazione ***"
              % len(g["fuori_testa"]))
        for a, n, r in g["fuori_testa"]:
            print("    ###   %s:%d  %s" % (a, n, r))
    albero = not g["vietati"] and not g["fuori_testa"]
    if albero:
        print("    ### PASSA: albero di PROFONDITA' 1, nessuna catena e nessun ciclo.")
    print("")
    print("=" * 100)
    print("### %s" % ("I DUE CONTROLLI PASSANO." if (not perse and albero)
                      else "*** UN CONTROLLO FALLISCE. ***"))
    print("=" * 100)
    return 0 if (not perse and albero) else 1


if __name__ == "__main__":
    sys.exit(principale())
