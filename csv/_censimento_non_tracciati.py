# -*- coding: utf-8 -*-
"""IL CENSIMENTO DEI FILE NON TRACCIATI — **e' tutto persistito come deve?**

*(domanda di Luca, 2026-10-04, dalla foto di VS Code: `480` file non tracciati.)*

### ⛔ **QUESTO STRUMENTO NON CANCELLA E NON IGNORA NIENTE.** Legge, classifica, conta e
scrive un referto. ### **Le decisioni le prende Luca leggendo i numeri** — e la ragione e'
scritta nel mandato: *niente `git clean`, niente `rm`*.

## LE QUATTRO CLASSI, e distinguerle E' il lavoro

| | come si riconosce | che cos'e' |
|---|---|---|
| **`(a)` COPIA-SIMULATORE** | il suo **sha1 dei byte grezzi** coincide con quello di un blob STORICO di `soliton_simulator.py` | ### **RIGENERABILE**: si riporta il blob e il commit |
| `(b)` STUB | sta sotto una cartella `_tmp/` | scarto |
| `(c)` STATO BINARIO | `.pkl`, `.pkl.gz`, `.npy`, `.npz` e simili | ### **non si committano** *(decisione di Luca)* |
| ### **`(d)` TUTTO IL RESTO** | — | ### **CANDIDATO OMISSIONE**, e per ciascuno si chiede: ### **chi lo cita?** |

### ⚠ **L'ORDINE DELLE CLASSI NON E' NEUTRO:** `(a)` si prova **prima** di `(b)`, cosi' una
copia del simulatore salvata sotto `_tmp/` risulta ### **rigenerabile** e non ### **scarto**.
Nell'ordine inverso una copia finirebbe fra gli stub e ### **si perderebbe l'informazione
che si puo' ricostruire.**

### ⚠ **IL LIMITE, DICHIARATO:** la classe `(a)` riconosce ### **solo** le copie di
`soliton_simulator.py`. Una copia di un ALTRO file tracciato ### **non e' riconosciuta come
copia** e finisce in `(d)` — dove la domanda *<<chi lo cita?>>* puo' ancora identificarla.
### **E' il difetto che ha morso nel censimento di `MITOSI_2LAM`**, dove
`_sig_scena_ii/_driver_prima.py` *(una copia del **driver**)* non era riconosciuta.

**COMANDO:** `python csv/_censimento_non_tracciati.py`
**USCITA:** `csv/_censimento_non_tracciati/`
"""
import hashlib
import io
import json
import os
import subprocess
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _QUI)
import _presidio   # noqa: E402

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, ".."))
FUORI = os.path.join(_QUI, "_censimento_non_tracciati")
NL = chr(10)
SIM = "soliton_simulator.py"
# ### LE ESTENSIONI DELLO STATO BINARIO. `.pkl.gz` sta qui e NON in `.gitignore`: e'
#   l'incoerenza che il mandato chiede di dichiarare.
BINARI = (".pkl", ".pkl.gz", ".npy", ".npz", ".pt", ".h5", ".bin", ".gz", ".pickle")


def git(*a):
    q = subprocess.run(["git"] + list(a), capture_output=True, cwd=RADICE)
    return q.stdout, q.returncode


def gits(*a):
    o, r = git(*a)
    return o.decode("utf-8", "replace") if r == 0 else ""


def sha_byte(percorso):
    try:
        return hashlib.sha1(io.open(percorso, "rb").read()).hexdigest()
    except OSError:
        return None


def blob_storici_del_simulatore():
    """### `{sha1 dei byte : (oid, [commit])}` per OGNI versione storica del simulatore.

    ### ⛔ **I DUE HASH NON SONO LO STESSO NUMERO** *(par.2)*: l'`oid` di git e' lo sha1 di
    `blob <len>\\0` + contenuto, l'identita' usata dai presidi di questo repo e' lo
    ### **sha1 dei byte GREZZI**. ### **Quindi l'oid NON si puo' confrontare con lo sha1 di un
    file sul disco**, e il contenuto va tirato fuori e ri-hashato.
    """
    fuori = {}
    oid_di = {}
    for c in gits("log", "--format=%H", "--", SIM).split(NL):
        c = c.strip()
        if not c:
            continue
        oid = gits("rev-parse", "%s:%s" % (c, SIM)).strip()
        if oid:
            oid_di.setdefault(oid, []).append(c)
    for oid, commits in oid_di.items():
        dati, r = git("cat-file", "blob", oid)
        if r != 0:
            continue
        fuori[hashlib.sha1(dati).hexdigest()] = (oid, commits)
    return fuori


def non_tracciati():
    """### Dallo stesso comando che il mandato nomina, e con `--untracked-files=all`:
    senza quel flag git ### **riassume una cartella in una riga** e il conto sarebbe
    sbagliato per difetto."""
    fuori = []
    for r in gits("status", "--porcelain", "--untracked-files=all").split(NL):
        if r.startswith("?? "):
            fuori.append(r[3:].strip().strip(chr(34)))
    return sorted(fuori)


def e_binario(rel):
    b = rel.lower()
    return any(b.endswith(x) for x in BINARI)


def chi_lo_cita(rel, corpora):
    """### CHI NOMINA QUESTO FILE, e si cerca il PERCORSO e il NOME BASE separatamente.

    ### Il percorso completo e' la citazione ### **forte**; il solo nome base e' ### **debole**
    *(due file possono chiamarsi `CONFIGURAZIONE.json`)*, e il referto li tiene distinti
    invece di sommarli.
    """
    base = os.path.basename(rel)
    fuori = {}
    for nome, testo in corpora.items():
        forte = rel in testo or rel.replace("/", chr(92)) in testo
        debole = (base in testo) and not forte
        if forte:
            fuori[nome] = "percorso"
        elif debole:
            fuori[nome] = "solo il nome"
    return fuori


def strumento_del_padre(rel):
    """### C'E' UNO STRUMENTO COMMITTATO CHE PORTA IL NOME DELLA SUA CARTELLA?

    ### E' un INDIZIO di *<<output di uno strumento committato>>*, non una prova: la
    convenzione di questo repo mette il referto di `X.py` dentro `X/`. ### **Si dichiara come
    indizio**, perche' una cartella puo' avere il nome di uno strumento senza esserne
    l'uscita.
    """
    d = os.path.dirname(rel)
    while d and d != ".":
        base = os.path.basename(d)
        for cand in (d + ".py", os.path.join(os.path.dirname(d), base + ".py"),
                     os.path.join(os.path.dirname(d), "_sigillo" + base + ".py")):
            cand = cand.replace(chr(92), "/")
            if gits("ls-files", "--error-unmatch", cand).strip():
                return cand
        d = os.path.dirname(d)
    return None


def principale():
    out = []

    def stampa(*x):
        s = " ".join(str(y) for y in x)
        out.append(s)
        print(s)

    if not os.path.isdir(FUORI):
        os.makedirs(FUORI)
    stampa("=" * 100)
    stampa("IL CENSIMENTO DEI FILE NON TRACCIATI -- e' tutto persistito come deve?")
    stampa("=" * 100)
    stampa("  strumento ... %s" % sha_byte(os.path.abspath(__file__))[:8])
    stampa("  ### QUESTO STRUMENTO NON CANCELLA E NON IGNORA NIENTE: legge e conta.")
    stampa("  ###   Le decisioni su (c) e (d) le prende Luca leggendo i numeri.")
    stampa("")

    nt = non_tracciati()
    stampa("  file non tracciati (`git status --porcelain --untracked-files=all`): %d"
           % len(nt))
    stampa("  ### con `--untracked-files=all`, perche' senza quel flag git RIASSUME una")
    stampa("  ###   cartella in UNA riga e il conto sarebbe sbagliato PER DIFETTO.")
    stampa("")
    stampa("  i blob STORICI di %s ..." % SIM)
    storici = blob_storici_del_simulatore()
    stampa("    %d versioni distinte, ri-hashate dai BYTE GREZZI" % len(storici))
    stampa("    ### I DUE HASH NON SONO LO STESSO NUMERO (par.2): l'`oid` di git e' lo")
    stampa("    ###   sha1 di `blob <len>\\0` + contenuto, l'identita' dei presidi e' lo")
    stampa("    ###   sha1 dei byte GREZZI. ### L'oid NON si confronta con un file su disco.")
    stampa("")

    # ---- i corpora in cui cercare le citazioni
    # ### ⛔ IL REFERTO DI QUESTO CENSIMENTO ESCE DAL CORPUS, e la ragione e' un difetto
    #   MISURATO il 2026-10-04: il referto `_corsa_2026-10-04_PRIMO.txt` ### **elenca TUTTI
    #   i candidati PER PERCORSO**, e una volta committato il giro successivo
    #   ### **TROVA SE STESSO** e dichiara ### **citati** anche i file che nessun altro
    #   nomina. ### **I <<non citati>> passarono da 57 a ZERO senza che niente cambiasse
    #   nel repo.**
    #   ### ⚠ **E' UN AUTORIFERIMENTO: il corpus in cui cerco le citazioni conteneva IL
    #   DOCUMENTO CHE ENUMERA LE COSE CERCATE.** ### **Un segnale che si autoalimenta non
    #   e' una misura.**
    #   ### ✅ Esce SOLO la cartella di questo strumento: che un ALTRO documento citi un
    #   file per percorso e' ### **una citazione legittima**, ed e' precisamente cio' che
    #   la misura vuole vedere.
    MIO = os.path.relpath(FUORI, RADICE).replace(chr(92), "/")
    corpora = {}
    saltati = 0
    for rel in gits("ls-files").split(NL):
        rel = rel.strip()
        if not rel:
            continue
        if rel.startswith(MIO + "/"):
            saltati += 1
            continue
        if rel.endswith((".md", ".tsv", ".txt", ".py", ".json")):
            try:
                corpora_testo = io.open(os.path.join(RADICE, rel), encoding="utf-8",
                                        errors="replace").read()
            except OSError:
                continue
            if rel == "doc/INVENTARIO_strumenti.md":
                corpora["INVENTARIO"] = corpora_testo
            elif rel.startswith("doc/TASK_HISTORY/"):
                corpora["TASK_HISTORY"] = corpora.get("TASK_HISTORY", "") + corpora_testo
            elif rel.startswith("doc/") or rel == "RELAZIONE_PER_CLAUDE.md":
                corpora["DOC"] = corpora.get("DOC", "") + corpora_testo
            elif rel.endswith(".py"):
                corpora["STRUMENTI"] = corpora.get("STRUMENTI", "") + corpora_testo
            elif rel.endswith(".txt"):
                corpora["REFERTI"] = corpora.get("REFERTI", "") + corpora_testo
    stampa("  ### dal corpus esclusi %d file di `%s`: il referto di questo censimento"
           % (saltati, MIO))
    stampa("  ###   elenca i candidati PER PERCORSO, e senza escluderlo il censimento")
    stampa("  ###   TROVEREBBE SE STESSO. ### Misurato: i non citati passarono da 57 a")
    stampa("  ###   ZERO senza che niente cambiasse nel repo. ### Un segnale che si")
    stampa("  ###   autoalimenta non e' una misura.")
    stampa("  i corpora in cui si cerca la citazione: %s"
           % ", ".join("%s (%d KB)" % (k, len(v) // 1024) for k, v in sorted(corpora.items())))
    stampa("")

    classi = {"(a) COPIA-SIMULATORE": [], "(b) STUB": [], "(c) STATO BINARIO": [],
              "(d) CANDIDATO OMISSIONE": []}
    dettaglio = []
    for rel in nt:
        full = os.path.join(RADICE, rel)
        if os.path.isdir(full):
            continue
        s = sha_byte(full)
        voce = {"file": rel, "sha1": s,
                "byte": (os.path.getsize(full) if os.path.exists(full) else None)}
        if s in storici:
            oid, commits = storici[s]
            voce["classe"] = "(a) COPIA-SIMULATORE"
            voce["oid_git"] = oid
            voce["commit"] = commits[0]
            voce["commit_quanti"] = len(commits)
        elif "/_tmp/" in ("/" + rel.replace(chr(92), "/")):
            voce["classe"] = "(b) STUB"
        elif e_binario(rel):
            voce["classe"] = "(c) STATO BINARIO"
        else:
            voce["classe"] = "(d) CANDIDATO OMISSIONE"
            voce["citato_da"] = chi_lo_cita(rel, corpora)
            voce["e_uno_strumento"] = rel.endswith(".py")
            voce["strumento_del_padre"] = strumento_del_padre(rel)
        classi[voce["classe"]].append(rel)
        dettaglio.append(voce)

    stampa("-" * 100)
    stampa("I CONTEGGI PER CLASSE")
    for k in ("(a) COPIA-SIMULATORE", "(b) STUB", "(c) STATO BINARIO",
              "(d) CANDIDATO OMISSIONE"):
        stampa("  %-26s %4d" % (k, len(classi[k])))
    stampa("  %-26s %4d" % ("TOTALE", sum(len(v) for v in classi.values())))
    stampa("")

    # ---- (c): l'incoerenza del .gitignore, e i binari GIA' TRACCIATI
    stampa("-" * 100)
    stampa("LA CLASSE `(c)`: l'incoerenza del `.gitignore`, e i binari GIA' TRACCIATI")
    gi = io.open(os.path.join(RADICE, ".gitignore"), encoding="utf-8").read()
    for pat in ("*.pkl", "*.pkl.gz", "*.npy", "*.npz", "*.gz"):
        stampa("  `.gitignore` contiene `%-9s`? %s" % (pat, pat in gi.split()))
    stampa("  ### ⛔ L'INCOERENZA, e il mandato chiede di dichiararla: `*.pkl` NON copre")
    stampa("  ###   `x.pkl.gz`. Un pattern di `.gitignore` combacia col NOME INTERO, e")
    stampa("  ###   `x.pkl.gz` finisce in `.gz`, non in `.pkl`. ### Quindi i `.pkl` sono")
    stampa("  ###   ignorati e i `.pkl.gz` NO, pur essendo la stessa cosa compressa.")
    trac = []
    for rel in gits("ls-files").split(NL):
        rel = rel.strip()
        if rel and e_binario(rel):
            c = gits("log", "--format=%h", "-1", "--", rel).strip()
            trac.append({"file": rel, "commit": c})
    stampa("  binari GIA' TRACCIATI: %d" % len(trac))
    for x in trac[:40]:
        stampa("    %-70s %s" % (x["file"][:70], x["commit"]))
    if len(trac) > 40:
        stampa("    ... e altri %d" % (len(trac) - 40))
    stampa("")

    # ---- (d): la lista INTERA
    stampa("-" * 100)
    stampa("LA CLASSE `(d)` -- CANDIDATI OMISSIONE: la lista INTERA, %d file"
           % len(classi["(d) CANDIDATO OMISSIONE"]))
    stampa("  ### Per ciascuno: chi lo cita, se e' uno strumento, e se la sua cartella")
    stampa("  ###   porta il nome di uno strumento committato (INDIZIO di <<e' l'uscita")
    stampa("  ###   di quello strumento>>, NON una prova).")
    stampa("")
    for v in dettaglio:
        if v["classe"] != "(d) CANDIDATO OMISSIONE":
            continue
        cit = v.get("citato_da") or {}
        stampa("  %s" % v["file"])
        stampa("      %d byte   %s%s"
               % (v["byte"] or 0,
                  "E' UNO STRUMENTO (.py)" if v["e_uno_strumento"] else "non e' un .py",
                  ("   cartella di `%s`" % v["strumento_del_padre"])
                  if v.get("strumento_del_padre") else ""))
        stampa("      citato da: %s"
               % (", ".join("%s (%s)" % (k, w) for k, w in sorted(cit.items()))
                  if cit else "### NESSUNO -- e' il caso che il mandato chiama OMISSIONE"))
    stampa("")

    # ---- la proposta, DA NON APPLICARE
    stampa("-" * 100)
    stampa("LA PROPOSTA, DA NON APPLICARE -- la decide Luca")
    stampa("  ### L'OBIETTIVO: che `non tracciato` significhi `DIMENTICATO`. Oggi non lo")
    stampa("  ###   significa, perche' fra i non tracciati ci sono %d copie rigenerabili e"
           % len(classi["(a) COPIA-SIMULATORE"]))
    stampa("  ###   %d stub -- rumore che NASCONDE i %d candidati veri."
           % (len(classi["(b) STUB"]), len(classi["(d) CANDIDATO OMISSIONE"])))
    stampa("")
    stampa("  LE REGOLE che renderebbero non tracciata SOLO la classe (d):")
    for r in ("csv/**/_tmp/", "csv/**/_sim_*.py", "csv/**/_br_*.py", "csv/**/_driver_*.py",
              "*.pkl.gz", "*.pickle"):
        stampa("      %s" % r)
    stampa("  ### ⚠ E DUE AVVERTENZE, perche' una regola di `.gitignore` e' una LEGGE che")
    stampa("  ###   agisce in silenzio:")
    stampa("  ###   ① `csv/**/_sim_*.py` ignorerebbe anche una copia che qualcuno vuole")
    stampa("  ###     committare ACCANTO AI DATI (par.7, stato 2): servirebbe un `!` per")
    stampa("  ###     le copie che stanno accanto a un referto committato.")
    stampa("  ###   ② `*.gz` NON va aggiunto in generale: ignorerebbe anche un referto")
    stampa("  ###     compresso. Si aggiunge `*.pkl.gz`, che e' la cosa che manca.")
    stampa("")
    stampa("  IL PRESIDIO che impedirebbe il caso `_sonda_scherm` (uno strumento girato")
    stampa("    fuori dal repo, col referto committato e lo strumento no):")
    stampa("      un hook `pre-commit` che AVVISA se esistono file non tracciati e NON")
    stampa("      ignorati sotto `csv/` o `doc/`, elencandoli.")
    stampa("  ### ⚠ AVVISA, non blocca: un blocco fermerebbe ogni commit fatto mentre un")
    stampa("  ###   run sta scrivendo i suoi output, che e' la norma qui. ### E un avviso")
    stampa("  ###   che nessuno legge e' `A9` -- quindi la forma la decide Luca.")

    esito = {"strumento": sha_byte(os.path.abspath(__file__)),
             "non_tracciati": len(nt),
             "blob_storici_simulatore": len(storici),
             "conteggi": {k: len(v) for k, v in classi.items()},
             "classi": classi, "dettaglio": dettaglio,
             "binari_tracciati": trac,
             "gitignore_pkl": "*.pkl" in gi.split(),
             "gitignore_pkl_gz": "*.pkl.gz" in gi.split()}
    stampa("")
    stampa("=" * 100)
    stampa("### IL RIEPILOGO")
    stampa("###   %d non tracciati: %d copie del simulatore (RIGENERABILI), %d stub,"
           % (len(nt), len(classi["(a) COPIA-SIMULATORE"]), len(classi["(b) STUB"])))
    stampa("###   %d binari di stato, %d CANDIDATI OMISSIONE."
           % (len(classi["(c) STATO BINARIO"]), len(classi["(d) CANDIDATO OMISSIONE"])))
    stampa("###   NIENTE E' STATO CANCELLATO, NIENTE E' STATO IGNORATO.")
    stampa("=" * 100)

    io.open(os.path.join(FUORI, "_censimento.json"), "w", encoding="utf-8",
            newline=NL).write(json.dumps(esito, indent=1, ensure_ascii=False, default=str))
    io.open(os.path.join(FUORI, "_corsa.txt"), "w", encoding="utf-8",
            newline=NL).write(NL.join(out) + NL)
    print("  referto .. %s" % FUORI)


if __name__ == "__main__":
    principale()
