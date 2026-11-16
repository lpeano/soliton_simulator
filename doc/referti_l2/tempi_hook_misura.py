# -*- coding: utf-8 -*-
r"""**PERCHE' I HOOK COSTANO TANTO: LE MISURE** *(Luca `2026-11-16` `00:23`; SOLO LETTURA: nessun hook, collaudo o strumento cambiato)*.

    python doc/referti_l2/tempi_hook_misura.py <cartella dei log di committa2> <una cartella temporanea su E:> > doc/referti_l2/tempi_hook_misure.txt

**A. I GRUPPI DEL `pre-commit`, dai log** *(`commit_log_*.txt` del `2026-11-15`)*: **l'ordine dei comandi si legge da `.githooks/pre-commit`; uno script che chiama `_presidio.avvia` stampa
`[TIMBRO] <nome>` SUBITO, con `flush`: quello e' il suo INIZIO.** **Un GRUPPO = uno script col timbro + quelli dopo di lui SENZA timbro** *(o con l'uscita in `/dev/null`)*, **fino al timbro dopo**;
**il primo gruppo va da `0` al primo timbro.** *(Corregge l'attribuzione del referto `bb14987b`, dove il tempo di un «passo» andava da un'etichetta qualunque alla successiva.)*
**B. LE MISURE DIRETTE, una volta ciascuna, dei comandi che NON scrivono file tracciati** *(il tempo da fuori, `perf_counter` attorno a `subprocess.run`)*: **`_nucleo_congelato --pre-commit`,
`_hook_presidi --pre-commit` e i suoi tre figli, `_stage.py --rapido`, `git checkout-index` di tutto l'indice su C: e su E:; il PROFILO** *(`cProfile`)* **di `indice.py valida`.**
**NON girati, perche' scrivono per un momento file tracciati:** `_albero_era2.py --collaudo` *(il yaml)*, `_collauda_regole.py` *(`CLAUDE.md`)*, `_collauda_guida.py` *(la tabella)*,
`_controlli_indice_v2.py --scrivi`, `_presidio_indice.py --collaudo --scrivi`, `_barriera.py --collaudo`: **per loro valgono i gruppi di A.**
"""
import cProfile
import datetime as dt
import glob
import io
import os
import pstats
import re
import shutil
import stat
import statistics
import subprocess
import sys
import tempfile
import time

RADICE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
GIORNO = "2026-11-15"


def ordine_precommit():
    out = []
    for r in io.open(os.path.join(RADICE, ".githooks", "pre-commit"), encoding="utf-8"):
        m = re.match(r'^python "[^"]*/(csv|primo_ordine)/([A-Za-z0-9_]+\.py)"(.*)$', r.strip())
        if m:
            out.append((m.group(2), m.group(3).split("||")[0].strip()))
    return out


def gruppi(f, ordine):
    tim = {}
    fine = 0.0
    for r in io.open(f, encoding="utf-8", errors="replace"):
        m = re.match(r"\[\s*([0-9.]+) s\] (.*)$", r.rstrip("\n"))
        if not m:
            continue
        fine = float(m.group(1))
        m2 = re.match(r"\[TIMBRO\] (\S+)", m.group(2))
        if m2 and m2.group(1) not in tim:
            tim[m2.group(1)] = fine
    # ### gli inizi in ordine: solo gli script del pre-commit col timbro, e crescenti
    inizi, ult = [], -1.0
    for nome, _arg in ordine:
        if nome in tim and tim[nome] >= ult:
            inizi.append((nome, tim[nome]))
            ult = tim[nome]
    out = []
    # ### il gruppo d'apertura: da 0 al primo timbro
    nomi_ord = [n for n, _a in ordine]
    primo = inizi[0][0] if inizi else None
    testa = nomi_ord[:nomi_ord.index(primo)] if primo else nomi_ord
    out.append((" + ".join(testa), inizi[0][1] if inizi else fine))
    for i, (nome, t0) in enumerate(inizi):
        t1 = inizi[i + 1][1] if i + 1 < len(inizi) else fine
        a = nomi_ord.index(nome)
        b = nomi_ord.index(inizi[i + 1][0]) if i + 1 < len(inizi) else len(nomi_ord)
        out.append((" + ".join(nomi_ord[a:b]), t1 - t0))
    return out, fine


def cronometra(argv, cwd=RADICE, env=None):
    t = time.perf_counter()
    r = subprocess.run(argv, cwd=cwd, capture_output=True, env=env)
    return time.perf_counter() - t, r.returncode


def _togli(d):
    def sblocca(fn, p, _e):
        os.chmod(p, stat.S_IWRITE)
        fn(p)
    shutil.rmtree(d, onerror=sblocca)
    return not os.path.exists(d)


def main(argv):
    d, tmp_e = argv[0], argv[1]
    print("=" * 130)
    print("PERCHE' I HOOK COSTANO TANTO, LE MISURE (Luca 2026-11-16 00:23): SOLO LETTURA; sys.executable %s; il carico: le corse aperte del registro, dichiarate nella carta" % sys.executable)
    print("=" * 130)
    ordine = ordine_precommit()
    print("### A. IL PRE-COMMIT: %d comandi python, in ordine: %s" % (len(ordine), ", ".join(n for n, _a in ordine)))
    logs = sorted(f for f in glob.glob(os.path.join(d, "commit_log_*.txt")) if dt.date.fromtimestamp(os.path.getmtime(f)).isoformat() == GIORNO)
    tutti, totali = {}, []
    for f in logs:
        g, fine = gruppi(f, ordine)
        if fine <= 0.0:
            continue
        totali.append(fine)
        for nome, s in g:
            tutti.setdefault(nome, []).append(s)
    tm = statistics.median(totali)
    print("### i log con i tempi: %d; il totale mediano dei hook %.1f s" % (len(totali), tm))
    print("  %-110s %4s %8s %8s %6s" % ("il gruppo (lo script col timbro + quelli dopo senza timbro)", "n", "mediana", "max", "quota"))
    for nome in sorted(tutti, key=lambda n: -statistics.median(tutti[n])):
        v = tutti[nome]
        print("  %-110s %4d %8.1f %8.1f %5.1f%%" % (nome[:110], len(v), statistics.median(v), max(v), 100.0 * statistics.median(v) / tm))
    print("=" * 130)
    print("### B. LE MISURE DIRETTE (una volta ciascuna; la macchina carica)")
    py = sys.executable
    for nome, argvv in (("_nucleo_congelato.py --pre-commit", [py, "csv/_nucleo_congelato.py", "--pre-commit"]),
                        ("_hook_presidi.py --pre-commit (lo stage vuoto)", [py, "csv/_hook_presidi.py", "--pre-commit"]),
                        ("  il figlio _presidio_commenti_flag.py --pre-commit", [py, "csv/_presidio_commenti_flag.py", "--pre-commit"]),
                        ("  il figlio _indice_id.py", [py, "csv/_indice_id.py"]),
                        ("  il figlio indice.py valida", [py, "csv/indice.py", "valida"]),
                        ("_stage.py --rapido (TMP del processo)", [py, "csv/_stage.py", "--rapido"])):
        s, rc = cronometra(argvv)
        print("  %-60s %7.1f s  (uscita %d)" % (nome, s, rc))
        sys.stdout.flush()
    n_file = len(subprocess.run(["git", "ls-files"], cwd=RADICE, capture_output=True, text=True).stdout.splitlines())
    for disco, base in (("C: (%TEMP%)", tempfile.gettempdir()), ("E:", tmp_e)):
        dd = tempfile.mkdtemp(prefix="misura_stage_", dir=base)
        s, rc = cronometra(["git", "checkout-index", "-a", "--prefix=" + dd + os.sep])
        n = sum(len(ff) for _b, _d, ff in os.walk(dd))
        tolta = _togli(dd)
        print("  git checkout-index di tutto l'indice su %-12s %7.1f s  (uscita %d; %d file su %d tracciati; la cartella tolta: %s)" % (disco, s, rc, n, n_file, tolta))
        sys.stdout.flush()
    print("-" * 130)
    # ### C. che cosa legge _storico_da_git (indice.py): git log del percorso, poi cat-file --batch di OGNI versione
    rel = "doc/indice/storico.jsonl"
    n_commit = subprocess.run(["git", "rev-list", "--count", "HEAD"], cwd=RADICE, capture_output=True, text=True).stdout.strip()
    t = time.perf_counter()
    q = subprocess.run(["git", "log", "--reverse", "--format=%h", "--", rel], cwd=RADICE, capture_output=True, text=True)
    t_log = time.perf_counter() - t
    sha = q.stdout.split()
    t = time.perf_counter()
    b = subprocess.run(["git", "cat-file", "--batch"], cwd=RADICE, input=("\n".join("%s:%s" % (c, rel) for c in sha) + "\n").encode("utf-8"), capture_output=True)
    t_cat = time.perf_counter() - t
    print("### C. CHE COSA LEGGE _storico_da_git: %s commit a HEAD; %s oggi %.2f MB; le sue versioni nella storia %d; git log del percorso %.1f s; cat-file --batch di tutte le versioni %.1f s, %.0f MB letti"
          % (n_commit, rel, os.path.getsize(os.path.join(RADICE, rel)) / 1e6, len(sha), t_log, t_cat, len(b.stdout) / 1e6))
    print("-" * 130)
    print("### IL PROFILO DI indice.py valida (cProfile, in questo processo; il tempo CUMULATIVO, le prime 25 righe)")
    sys.stdout.flush()
    sys.path.insert(0, os.path.join(RADICE, "csv"))
    vecchio = sys.argv
    sys.argv = ["indice.py", "valida"]
    pr = cProfile.Profile()
    cwd = os.getcwd()
    os.chdir(RADICE)
    try:
        import contextlib
        import runpy
        muto = io.StringIO()                                        # ### l'uscita di valida non entra nel referto
        with contextlib.redirect_stdout(muto):
            pr.enable()
            try:
                runpy.run_path(os.path.join(RADICE, "csv", "indice.py"), run_name="__main__")
            except SystemExit:
                pass
            pr.disable()
    finally:
        os.chdir(cwd)
        sys.argv = vecchio
    sys.stdout.flush()
    buf = io.StringIO()
    pstats.Stats(pr, stream=buf).sort_stats("cumulative").print_stats(25)
    print("-" * 130)
    print(buf.getvalue())
    print("=" * 130)
    return 0


if __name__ == "__main__":
    sys.path.insert(0, os.path.join(RADICE, "csv"))
    import _presidio
    _presidio.avvia(__file__)
    sys.exit(main(sys.argv[1:]))
