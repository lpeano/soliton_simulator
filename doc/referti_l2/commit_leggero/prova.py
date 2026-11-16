# -*- coding: utf-8 -*-
r"""**LA PROVA A3 DEL COMMIT PIU' LEGGERO** *(Luca `2026-11-16` `08:57`; la carta `doc/TASK_HISTORY/2026-11-16_commit_leggero_e_riunione.md`)*.

    python doc/referti_l2/commit_leggero/prova.py <cartella dei log di committa2> > doc/referti_l2/commit_leggero/prova.txt
    python doc/referti_l2/commit_leggero/prova.py <cartella dei log di committa2> --solo-casi > doc/referti_l2/commit_leggero/prova_casi.txt   (il secondo giro: solo F1-F5)

**I due modi, sullo STESSO commit `C` del `2026-11-15`** *(i commit dei log `commit_log_*.txt` di quel giorno che hanno un hash nei `c2_*.txt`)*,
in un `git worktree` del repo principale:
  - **VECCHIO:** `HEAD` = il padre `P`, lo stage = l'albero di `C`, il disco = lo stage *(i due file come erano: fermi da ottobre)*;
  - **NUOVO:** `HEAD` = `P'` *(un commit locale, mai spinto: `P` + `indice_nuovo.py.txt` e `_hook_presidi_nuovo.py.txt` al loro posto, con gli stessi byte)*,
    lo stage = `C` + i due file nuovi, il disco = lo stage. **Cosi' l'insieme dei file in stage e' lo STESSO dei due modi.**
**Su ogni commit, nei due modi:** `c1` `_hook_presidi.py --pre-commit`; `c2` `_stage.py --rapido`; `c3` `indice.py valida` *(il disco)*;
`c4` l'impronta di `_storico_da_git()` *(`_per_riga.py`)*. **Su `3` commit anche `c5` il `pre-commit` INTERO.**
**L'esito:** **il codice d'uscita e l'uscita** *(stdout + stderr)* **normalizzata** *(via i timbri, i numeri coi secondi, i percorsi temporanei)*.
**I casi che DEVONO fallire F1-F5** *(la carta)*. **Un solo esito diverso: la strada cade.**
"""
import glob
import hashlib
import io
import os
import re
import shutil
import subprocess
import sys
import time

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(os.path.dirname(os.path.dirname(_QUI)))
sys.path.insert(0, os.path.join(RADICE, "csv"))
NUOVI = {"csv/indice.py": os.path.join(_QUI, "indice_nuovo.py.txt"), "csv/_hook_presidi.py": os.path.join(_QUI, "_hook_presidi_nuovo.py.txt")}
BASE = "16346123"   # ### il commit del principale da cui partono i file NUOVI (la carta): i file VECCHI si leggono da li', mai da HEAD (H-P8)
GIORNO = "2026-11-15"
INTERI = 3
MEMORIA = None


def git(*a, cwd=None, inp=None, ok=True):
    r = subprocess.run(["git"] + list(a), cwd=cwd or RADICE, input=inp, capture_output=True)
    if ok and r.returncode:
        raise RuntimeError("git %s: %s" % (" ".join(a), r.stderr.decode("utf-8", "replace")))
    return r.stdout.decode("utf-8", "replace").strip()


def sha8(f):
    return hashlib.sha1(open(f, "rb").read()).hexdigest()[:8]


def commit_del_giorno(d):
    import datetime as dt
    logs = sorted(f for f in glob.glob(os.path.join(d, "commit_log_*.txt")) if dt.date.fromtimestamp(os.path.getmtime(f)).isoformat() == GIORNO)
    m = {}
    for f in glob.glob(os.path.join(d, "c2_*.txt")):
        t = io.open(f, encoding="utf-8", errors="replace").read()
        a = re.search(r"commit_log_(\d{6})\.txt", t)
        b = re.search(r"R5 COMMIT OK: (\w+)", t)
        if a and b:
            m[a.group(1)] = b.group(1)
    out = []
    for f in logs:
        hh = re.search(r"commit_log_(\d{6})", f).group(1)
        out.append((hh, m.get(hh)))
    return out


_NORM = [
    (re.compile(r"^\[TIMBRO\].*$", re.M), "[TIMBRO]"),
    (re.compile(r"\d+(\.\d+)?\s*s\b"), "<T> s"),
    (re.compile(r"\(\d+(\.\d+)? ?s\)"), "(<T>)"),
    (re.compile(r"[A-Za-z]:[\\/][^\s'\"]*?(tmp|Temp|TEMP)[^\s'\"]*", re.I), "<TMP>"),
    (re.compile(r"/tmp/[^\s'\"]*"), "<TMP>"),
    (re.compile(r"wt_prova_commit_leggero"), "<WT>"),
]


def norm(s):
    for r, x in _NORM:
        s = r.sub(x, s)
    return s


def gira(nome, argv, wt, timbri):
    t = time.time()
    r = subprocess.run(argv, cwd=wt, capture_output=True)
    uscita = (r.stdout + r.stderr).decode("utf-8", "replace")
    timbri.extend(re.findall(r"^\[TIMBRO\].*$", uscita, re.M))
    return {"nome": nome, "codice": r.returncode, "uscita": norm(uscita), "grezza": uscita, "s": time.time() - t}


def prepara(wt, c, p, modo):
    """### Il worktree nel modo chiesto: `HEAD`, lo stage e il disco come scritto nel docstring del modulo."""
    git("checkout", "-q", "-f", "--detach", c, cwd=wt)
    git("clean", "-q", "-fdx", cwd=wt)
    if modo == "VECCHIO":
        git("reset", "-q", "--soft", p, cwd=wt)
        return p
    idx = os.path.join(wt, ".git_indice_tmp")
    env = dict(os.environ)
    env["GIT_INDEX_FILE"] = idx
    blob = {}
    for rel, src in NUOVI.items():
        blob[rel] = git("hash-object", "-w", src, cwd=wt)
    subprocess.run(["git", "read-tree", p], cwd=wt, env=env, check=True)
    for rel, b in blob.items():
        subprocess.run(["git", "update-index", "--add", "--cacheinfo", "100644,%s,%s" % (b, rel)], cwd=wt, env=env, check=True)
    albero = subprocess.run(["git", "write-tree"], cwd=wt, env=env, capture_output=True, check=True).stdout.decode().strip()
    os.remove(idx)
    p2 = git("commit-tree", albero, "-p", p, "-m", "P' locale della prova S1+S2 (mai spinto)", cwd=wt)
    for rel, src in NUOVI.items():
        shutil.copyfile(src, os.path.join(wt, rel.replace("/", os.sep)))
        git("add", "--", rel, cwd=wt)
    git("reset", "-q", "--soft", p2, cwd=wt)
    return p2


def comandi(wt, intero):
    py = sys.executable
    cc = [("c1 _hook_presidi --pre-commit", [py, "csv/_hook_presidi.py", "--pre-commit"]),
          ("c2 _stage --rapido", [py, "csv/_stage.py", "--rapido"]),
          ("c3 indice.py valida (il disco)", [py, "csv/indice.py", "valida"]),
          ("c4 _storico_da_git", [py, os.path.join(_QUI, "_per_riga.py"), os.path.join(wt, "csv", "indice.py")])]
    if intero:
        cc.append(("c5 il pre-commit INTERO", ["sh", ".githooks/pre-commit"]))
    return cc


def stato_file(wt):
    """### I file del worktree diversi dallo stage, e lo stage diverso da HEAD: per vedere chi ha scritto."""
    return (git("diff", "--name-only", cwd=wt), git("diff", "--cached", "--name-only", cwd=wt))


def confronta(a, b):
    diversi = []
    for x, y in zip(a, b):
        if x["codice"] != y["codice"] or x["uscita"] != y["uscita"]:
            diversi.append((x["nome"], x["codice"], y["codice"], x["uscita"], y["uscita"]))
    return diversi


def stampa_diversi(diversi):
    import difflib
    for nome, cv, cn, uv, un in diversi:
        print("    ### DIVERSO: %s: il codice %d contro %d" % (nome, cv, cn))
        for r in list(difflib.unified_diff(uv.splitlines(), un.splitlines(), "VECCHIO", "NUOVO", lineterm="", n=1))[:40]:
            print("        " + r[:200])


def caso(wt, c, p, nome, ritocco, deve_fallire_in, intero=False):
    """### Un caso che DEVE fallire: `ritocco(wt)` dopo la preparazione, nei due modi."""
    res = {}
    for modo in ("VECCHIO", "NUOVO"):
        prepara(wt, c, p, modo)
        ritocco(wt)
        prima = stato_file(wt)
        timbri = []
        res[modo] = [gira(n, a, wt, timbri) for n, a in comandi(wt, intero)]
        res[modo + "_file"] = (prima, stato_file(wt))
    print("  %s:" % nome)
    for modo in ("VECCHIO", "NUOVO"):
        print("    %-7s %s; i file (disco, stage) prima %s, dopo %s" % (modo, ", ".join("%s -> %d" % (r["nome"].split()[0], r["codice"]) for r in res[modo]),
                                                                       res[modo + "_file"][0], res[modo + "_file"][1]))
    return res


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    global MEMORIA
    d = argv[0]
    solo = "--solo-casi" in argv[1:]                  # ### il secondo giro (ce9e7b63): SOLO i casi F1-F5, dopo il crash di F4b
    print("=" * 130)
    print("LA PROVA A3 DEL COMMIT PIU' LEGGERO (S1 + S2; Luca 2026-11-16 08:57); sys.executable %s" % sys.executable)
    print("  i file nuovi: %s" % ", ".join("%s <- %s (%s)" % (r, os.path.basename(f), sha8(f)) for r, f in NUOVI.items()))
    print("  i file vecchi al commit %s: %s" % (BASE, ", ".join("%s %s" % (r, hashlib.sha1(subprocess.run(["git", "show", BASE + ":" + r], cwd=RADICE, capture_output=True).stdout).hexdigest()[:8]) for r in NUOVI)))
    print("=" * 130)
    lista = commit_del_giorno(d)
    print("### i log del %s: %d; con un hash: %d (la carta c0c3b78d contava 40 log coi tempi)" % (GIORNO, len(lista), sum(1 for _h, c in lista if c)))
    commit = [c for _h, c in lista if c]
    for c in commit:
        for rel in NUOVI:
            assert git("rev-parse", "%s:%s" % (c, rel)) == git("rev-parse", "%s:%s" % (BASE, rel)), "il file %s di %s non e' quello di %s: la sovrapposizione non vale" % (rel, c, BASE)
    print("### i due file sono gli stessi di %s in tutti i %d commit: la sovrapposizione vale" % (BASE, len(commit)))
    MEMORIA = os.path.join(git("rev-parse", "--path-format=absolute", "--git-common-dir"), "indice_storico_righe.json")
    print("### la memoria: %s (c'e': %s; la si toglie prima, cosi' il primo NUOVO la costruisce)" % (MEMORIA, os.path.exists(MEMORIA)))
    if os.path.exists(MEMORIA):
        os.remove(MEMORIA)
    wt = os.path.join(os.environ.get("TEMP", RADICE), "wt_prova_commit_leggero")
    if os.path.exists(wt):
        git("worktree", "remove", "--force", wt, ok=False)
        shutil.rmtree(wt, ignore_errors=True)
    git("worktree", "add", "-q", "--detach", wt, BASE)
    interi = {commit[0], commit[len(commit) // 2], commit[-1]}
    tot = {"VECCHIO": 0.0, "NUOVO": 0.0}
    cadute = []
    tempi_c = {}
    try:
        print("-" * 130)
        if solo:
            print("### --solo-casi: i %d commit NON si rigirano (il primo giro: doc/referti_l2/commit_leggero/prova.txt, ce9e7b63)" % len(commit))
        for i, c in enumerate([] if solo else commit):
            p = git("rev-parse", c + "^")
            ramo = git("name-rev", "--name-only", "--refs=refs/remotes/origin/*", c, ok=False)
            res = {}
            for modo in ("VECCHIO", "NUOVO"):
                prepara(wt, c, p, modo)
                timbri = []
                res[modo] = [gira(n, a, wt, timbri) for n, a in comandi(wt, c in interi)]
                tot[modo] += sum(r["s"] for r in res[modo])
                for r in res[modo]:
                    tempi_c.setdefault((modo, r["nome"]), []).append(r["s"])
            dv = confronta(res["VECCHIO"], res["NUOVO"])
            print("  %2d %s (%s) %s; i codici V %s N %s; i secondi V %s N %s; %s"
                  % (i + 1, c, ramo, "INTERO" if c in interi else "", [r["codice"] for r in res["VECCHIO"]], [r["codice"] for r in res["NUOVO"]],
                     ["%.0f" % r["s"] for r in res["VECCHIO"]], ["%.0f" % r["s"] for r in res["NUOVO"]], "UGUALE" if not dv else "### %d DIVERSI" % len(dv)))
            for r in res["NUOVO"]:
                if r["nome"].startswith("c4"):
                    print("       %s" % r["grezza"].strip().splitlines()[-1])
            stampa_diversi(dv)
            if dv:
                cadute.append(c)
            sys.stdout.flush()
        print("-" * 130)
        print("### I TEMPI MEDI PER COMANDO (secondi):")
        for (modo, nome), v in sorted(tempi_c.items(), key=lambda x: (x[0][1], x[0][0])):
            print("    %-36s %-7s %7.1f  (su %d)" % (nome, modo, sum(v) / len(v), len(v)))
        print("### IL CONFRONTO SUI %d COMMIT: %s" % (len(commit), "TUTTI UGUALI" if not cadute else "### DIVERSI: %s" % cadute))
        # ---------------------------------------------------------------- i casi che DEVONO fallire
        print("=" * 130)
        c = commit[-1]
        p = git("rev-parse", c + "^")
        print("### I CASI CHE DEVONO FALLIRE, sul commit %s" % c)

        def f1(wt):
            f = os.path.join(wt, "doc", "indice", "storico.jsonl")
            r = io.open(f, encoding="utf-8", newline="").read().split("\n")
            k = len(r) // 2
            assert r[k].strip(), "la riga di mezzo e' vuota"
            del r[k]
            io.open(f, "w", encoding="utf-8", newline="").write("\n".join(r))
            git("add", "--", "doc/indice/storico.jsonl", cwd=wt)

        def f2(wt):
            f = os.path.join(wt, "doc", "indice", "voci.jsonl")
            r = io.open(f, encoding="utf-8", newline="").read().split("\n")
            assert '"stato": "' in r[0], "la prima voce non ha il campo stato nella forma attesa"
            r[0] = r[0].replace('"stato": "', '"stato": "X', 1)
            io.open(f, "w", encoding="utf-8", newline="").write("\n".join(r))
            git("add", "--", "doc/indice/voci.jsonl", cwd=wt)

        def f3(wt):
            f = os.path.join(wt, "doc", "indice", "voci.jsonl")
            io.open(f, "a", encoding="utf-8", newline="").write("{rotta\n")

        r1 = caso(wt, c, p, "F1 una riga di storico TOLTA in mezzo, in stage (c2 e c3 devono uscire 1)", f1, ("c2", "c3"))
        r2 = caso(wt, c, p, "F2 voci.jsonl cambiato in stage SENZA la riga di storico (c2 e c3 devono uscire 1)", f2, ("c2", "c3"))
        r3 = caso(wt, c, p, "F3 un indice rotto SOLO sul disco (c3 deve uscire 1; il pre-commit INTERO deve uscire 1, e i file dopo come prima)", f3, ("c3", "c5"), intero=True)
        esiti = []
        for nome, r, devono in (("F1", r1, ("c2", "c3")), ("F2", r2, ("c2", "c3")), ("F3", r3, ("c3", "c5"))):
            for modo in ("VECCHIO", "NUOVO"):
                for x in r[modo]:
                    k = x["nome"].split()[0]
                    if k in devono:
                        esiti.append(("%s %s %s esce 1" % (nome, modo, k), x["codice"] != 0))
        v5, n5 = r3["VECCHIO"][-1], r3["NUOVO"][-1]
        print("    F3: il pre-commit INTERO, VECCHIO: %d; NUOVO: %d; l'ultima riga di rifiuto VECCHIO %r; NUOVO %r"
              % (v5["codice"], n5["codice"], (v5["grezza"].strip().splitlines() or [""])[-1][:150], (n5["grezza"].strip().splitlines() or [""])[-1][:150]))
        for modo, x5 in (("VECCHIO", v5), ("NUOVO", n5)):
            tb = [r for r in x5["grezza"].splitlines() if r.startswith("[TIMBRO]") or "Traceback" in r or 'File "' in r or "RIFIUTATO" in r]
            print("    F3 %s, chi rifiuta (gli ultimi timbri, i traceback, le righe RIFIUTATO): %s" % (modo, " | ".join(x[:120] for x in tb[-6:])))
        esiti.append(("F3 NUOVO: i file (disco, stage) dopo il rifiuto come prima", r3["NUOVO_file"][0] == r3["NUOVO_file"][1]))
        for nome, r in (("F1", r1), ("F2", r2), ("F3", r3)):
            for x, y in zip(r["VECCHIO"], r["NUOVO"]):
                k = x["nome"].split()[0]
                if k == "c1":
                    # ### la carta, sez. 2: per S1 le righe di _hook_presidi sul disco spariscono PER COSTRUZIONE; il confronto vale sul pre-commit e sulle righe di valida
                    print("    %s c1: VECCHIO %d, NUOVO %d (per costruzione: S1 toglie da c1 il valida sul disco)" % (nome, x["codice"], y["codice"]))
                    continue
                esiti.append(("%s %s: lo stesso codice d'uscita nei due modi (%d, %d)" % (nome, k, x["codice"], y["codice"]), x["codice"] == y["codice"]))
                if k in ("c2", "c3"):
                    esiti.append(("%s %s: le stesse righe di valida nei due modi (l'uscita normalizzata)" % (nome, k), x["uscita"] == y["uscita"]))
                    if x["uscita"] != y["uscita"]:
                        stampa_diversi([(x["nome"], x["codice"], y["codice"], x["uscita"], y["uscita"])])
        # ---------------------------------------------------------------- F4, F5: la memoria
        prepara(wt, c, p, "NUOVO")
        rif = gira("c4", comandi(wt, False)[3][1], wt, [])["grezza"].strip().splitlines()[-1].split()[1]
        import json
        m = json.load(io.open(MEMORIA, encoding="utf-8"))
        k0 = sorted(m["righe"])[0]
        m["righe"][k0] += 1
        io.open(MEMORIA, "w", encoding="utf-8").write(json.dumps(m))
        x = gira("c4", comandi(wt, False)[3][1], wt, [])
        esiti.append(("F4a un conto sbagliato SENZA rifare l'impronta: riconosciuta ROTTA, lo stesso per_riga", "ROTTA" in x["grezza"] and x["grezza"].strip().splitlines()[-1].split()[1] == rif))
        print("    F4a: %s" % x["grezza"].strip().replace("\n", " | ")[:250])
        sys.path.insert(0, _QUI)
        import importlib.machinery
        import importlib.util
        # ### il crash del primo giro: per un `.txt` spec_from_file_location non da' un loader; il loader si dichiara
        spec = importlib.util.spec_from_loader("indice_nuovo_prova", importlib.machinery.SourceFileLoader("indice_nuovo_prova", NUOVI["csv/indice.py"]))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        m = json.load(io.open(MEMORIA, encoding="utf-8"))
        bl = git("rev-parse", "%s:doc/indice/storico.jsonl" % p)
        assert bl in m["righe"], "il blob piu' recente non e' in memoria"
        m["righe"][bl] += 1
        m["impronta"] = mod._impronta_memoria(m["righe"])
        io.open(MEMORIA, "w", encoding="utf-8").write(json.dumps(m))
        x = gira("c4", comandi(wt, False)[3][1], wt, [])
        esiti.append(("F4b il conto del blob PIU' RECENTE falsato CON l'impronta rifatta: riconosciuto da git, lo stesso per_riga", "NON torna" in x["grezza"] and x["grezza"].strip().splitlines()[-1].split()[1] == rif))
        print("    F4b: %s" % x["grezza"].strip().replace("\n", " | ")[:250])
        os.remove(MEMORIA)
        x = gira("c4", comandi(wt, False)[3][1], wt, [])
        esiti.append(("F5 la memoria assente: ricostruita, lo stesso per_riga", os.path.exists(MEMORIA) and x["grezza"].strip().splitlines()[-1].split()[1] == rif))
        print("    F5: %s" % x["grezza"].strip()[:200])
        print("    IL LIMITE, dichiarato: un conto falsato su un blob VECCHIO con l'impronta rifatta NON e' riconosciuto (si rilegge solo il piu' recente)")
        print("-" * 130)
        for n, ok in esiti:
            print("  DEVE: %-110s %s" % (n, "PASSA" if ok else "### FALLISCE"))
        tutti = not cadute and all(ok for _n, ok in esiti)
        print("=" * 130)
        print("### I TEMPI DELLA PROVA: VECCHIO %.0f s, NUOVO %.0f s" % (tot["VECCHIO"], tot["NUOVO"]))
        print("ESITO: %s" % ("LA STRADA S1 + S2 RESTA: ogni esito uguale, ogni caso come deve" if tutti else "### LA STRADA CADE"))
        return 0 if tutti else 1
    finally:
        git("worktree", "remove", "--force", wt, ok=False)
        shutil.rmtree(wt, ignore_errors=True)
        git("worktree", "prune", ok=False)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
