# -*- coding: utf-8 -*-
"""CERCA **TUTTE** LE DEFINIZIONI DI UN ID, **in tutto il repo.**

> ### ⛔ **Serve perche' `F4` SI FERMA AL PRIMO FILE** *(un `break`)*, e il punto `5` chiede
> *«cerca ### **TUTTE** le sue definizioni nel repo»*. ### **Un presidio che si ferma al primo
> non puo' dire se un ID e' un OMONIMO**, e l'omonimia e' esattamente uno dei tre esiti.

**Che cosa conta come definizione** — la stessa regola di `F4`, importata da `csv/indice.py`
*(non ricopiata: ### **una regola in due copie diventa due regole**)*:

| | |
|---|---|
| ### **riga di tabella** | `\|` + backtick + `ID` + backtick + `\|` …, l'ID ad **apertura di riga** |
| ### **intestazione** | l'ID e' il **SOGGETTO** *(dopo i `#`, i simboli, la numerazione e una parola di stato)* **e c'e' CONTENUTO** |

### ⚠ **I file si distinguono per TIPO**, perche' non pesano uguale: un `.md` in `doc/` e' un
**documento**, un `.py` in `csv/_seal_fork/` e' **un sigillo**. ### **Le VISTE GENERATE sono
escluse**, perche' una riga in `doc/LISTA_CHIUSA.md` **elenca** un ID, non lo definisce.

Gira con:  python csv/_cerca_definizioni.py <ID> [<ID> ...]
           python csv/_cerca_definizioni.py --f4        # tutte quelle che `F4` segnala
"""
import io
import json
import os
import re
import subprocess
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
sys.path.insert(0, _QUI)
import _presidio                                             # noqa: E402
_presidio.avvia(__file__)
import indice as IX                                          # noqa: E402

# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Cerca definizioni nei documenti.
NL = chr(10)
BT = chr(96)


def tracciati():
    q = subprocess.run(["git", "ls-files"], cwd=RADICE, capture_output=True, text=True,
                       encoding="utf-8")
    out = []
    for f in (q.stdout or "").split(NL):
        f = f.strip()
        if not f or not f.lower().endswith((".md", ".py", ".txt")):
            continue
        if any(f == g or f.startswith(g) for g in IX.VISTE_GENERATE):
            continue
        if sull_indice(f):
            continue
        out.append(f)
    return out


# ### ⛔ **IL FALSO-UNO, PER LA TERZA VOLTA, e stavolta i file erano MIEI.** La prima fu
# ### il controllo `C4`, che leggeva `doc/INDICE.md` -- ### **un file che genera lui**. La
# ### seconda `doc/LISTA_CHIUSA.md`, ### **la lista degli ID**. La terza sono
# ### ### **I MIEI REFERTI**: `doc/REFERTO_indice_v3_presidi.md` contiene `| ID | ... |` per
# ### ogni segnale, e il cercatore le leggeva come ### **definizioni.**
# ### ⭐ **IL PRINCIPIO, scritto una volta per tutte:** ### **un file che PARLA DELL-INDICE
# ### ELENCA gli ID; non li DEFINISCE.** Quindi i referti dell-indice, i suoi task history,
# ### i suoi attrezzi e la sua scheda di regole ### **non sono fonti di definizione.**
SULL_INDICE = ("doc/REFERTO_indice_", "doc/INDICE", "doc/REGOLE/par9.md",
               "doc/LISTA_CHIUSA.md", "csv/indice.py", "csv/_indice_id.py",
               "csv/_cerca_definizioni.py", "csv/_segnali_chiusura.py",
               "csv/_collaudo_presidi_indice.py", "csv/_controlli_indice_v2.py",
               "csv/migra_indice_v2.py", "csv/_registri_indice.py",
               "csv/_presidio_indice.py", "csv/_analisi_lettori_indice.py",
               "csv/_doc_referto_", "csv/_fase2_", "csv/_fase3_")


def sull_indice(f):
    p = f.replace(chr(92), "/")
    if any(p.startswith(g) for g in SULL_INDICE):
        return True
    # ### i task history DEL LAVORO SULL-INDICE: elencano gli ID, non li definiscono
    return p.startswith("doc/TASK_HISTORY/") and "indice" in p


def tipo(f):
    if f.startswith("doc/TASK_HISTORY/"):
        return "task-history"
    if f.startswith("doc/relazioni/") or f == "RELAZIONE_PER_CLAUDE.md":
        return "relazione"
    if f.startswith("csv/_seal_fork/"):
        return "sigillo"
    if f.startswith("csv/"):
        return "attrezzo"
    if f.endswith(".md"):
        return "documento"
    return "altro"


def cerca(idv, files):
    q = re.escape(idv)
    rt = re.compile(r"^\s*\|\s*\**\s*`?" + q + r"`?\s*\**\s*\|")
    it = re.compile(r"^#{1,6}\s.*(?<![A-Za-z0-9_:-])" + q + r"(?![A-Za-z0-9_:-])")
    fuori = []
    for f in files:
        p = os.path.join(RADICE, f)
        if not os.path.exists(p):
            continue
        testo = io.open(p, encoding="utf-8", errors="replace").read()
        if idv not in testo:
            continue                      # ### il taglio che rende la ricerca praticabile
        righe = testo.split(NL)
        for n, r in enumerate(righe, 1):
            if rt.match(r):
                fuori.append((f, tipo(f), n, "riga di tabella", " ".join(r.split())[:150]))
            elif it.match(r) and IX._intestazione_definisce(righe, n - 1, idv):
                fuori.append((f, tipo(f), n, "intestazione", " ".join(r.split())[:150]))
    return fuori


def main(argv):
    files = tracciati()
    if argv and argv[0] == "--f4":
        et = [json.loads(r) for r in
              io.open(os.path.join(RADICE, "doc/indice/etichette_rimosse.jsonl"),
                      encoding="utf-8").read().split(NL) if r.strip()]
        ids = sorted({i for i, _m in IX._f4_etichette(et)} | set(argv[1:]))
    else:
        ids = list(argv)
    assert ids, __doc__
    print("=" * 108)
    print("TUTTE LE DEFINIZIONI, in %d file tracciati (viste generate ESCLUSE)" % len(files))
    print("=" * 108)
    out = {}
    for idv in ids:
        d = cerca(idv, files)
        out[idv] = [{"file": f, "tipo": t, "riga": n, "come": c, "testo": s}
                    for f, t, n, c, s in d]
        posti = len({f for f, _t, _n, _c, _s in d})
        print()
        print("### `%s`: %d definizioni in %d file" % (idv, len(d), posti))
        for f, t, n, c, s in d:
            print("    %-13s %-52s:%-6s %-15s %s" % (t, f[-52:], n, c, s[:70]))
        if not d:
            print("    ### NESSUNA definizione trovata in tutto il repo.")
    p = os.path.join(RADICE, "doc", "indice", "_definizioni.json")
    io.open(p, "w", encoding="utf-8", newline=NL).write(
        json.dumps(out, ensure_ascii=False, indent=1))
    print()
    print("scritto doc/indice/_definizioni.json")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
