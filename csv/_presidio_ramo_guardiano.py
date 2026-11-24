# -*- coding: utf-8 -*-
"""**`H-GUARDIANO` -- CC NON COMMITTA E NON PUSHA MAI SUL RAMO `guardiano`.** *(DECISIONE DI LUCA, 2026-11-24 23:53, [M2345]: «il guardiano scrive sul SOLO ramo `guardiano`; CC non committa mai su quel ramo (presidio)»)*

**STA IN DUE HOOK:**
- in `pre-commit`, `--commit` RIFIUTA se il ramo corrente e' esattamente `guardiano`;
- in `pre-push`, `--push` legge da stdin le righe `<ref locale> <sha locale> <ref remoto> <sha remoto>` e RIFIUTA se un ref remoto e' esattamente `refs/heads/guardiano`.

**NESSUNA VIA D'USCITA:** quel ramo e' del guardiano.

    python csv/_presidio_ramo_guardiano.py --commit      # dal hook pre-commit
    python csv/_presidio_ramo_guardiano.py --push        # dal hook pre-push (stdin)
    python csv/_presidio_ramo_guardiano.py --collaudo    # i casi noti, commit e push veri in un repo di prova

ASCII puro nel codice.
"""
import os
import shutil
import subprocess
import sys
import tempfile

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Legge il ramo corrente e le righe del push.

RAMO = "guardiano"
REF = "refs/heads/" + RAMO


def ramo_corrente():
    q = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True)
    return q.stdout.decode("utf-8", "replace").strip()


def decidi_commit(ramo):
    if ramo == RAMO:
        return 1, "[H-GUARDIANO] RIFIUTATO: il ramo corrente e' `%s`. Quel ramo e' del guardiano: CC non committa mai li' ([M2345]).\n" % RAMO
    return 0, ""


def decidi_push(righe):
    for r in righe:
        p = r.split()
        if len(p) >= 4 and p[2] == REF:
            return 1, "[H-GUARDIANO] RIFIUTATO: il push scrive `%s` (da `%s`). Quel ramo e' del guardiano: CC non pusha mai li' ([M2345]).\n" % (REF, p[0])
    return 0, ""


def collaudo():
    """### i casi noti con COMMIT E PUSH VERI in un repo di prova *(i hook FUORI dal repo, come `H-LANCIATORI`)*:
    (1) un commit sul ramo `guardiano`: RIFIUTATO; (2) su `lavoro`: ENTRA; (3) DEVE ENTRARE: il ramo `guardiano-x` (il nome non e' quello);
    (4) `git push origin lavoro`: ENTRA; (5) `git push origin lavoro:guardiano`: RIFIUTATO; (6) `git push origin guardiano` (creato fuori dal hook): RIFIUTATO;
    (7) `git push origin guardiano-x`: ENTRA."""
    d = tempfile.mkdtemp(prefix="h_guardiano_")
    nudo = d + "_remoto.git"
    ganci = d + "_ganci"
    ok = []
    try:
        def g(*a, controlla_=True, cwd=None):
            return subprocess.run(["git"] + list(a), cwd=cwd or d, capture_output=True, check=controlla_)
        subprocess.run(["git", "init", "-q", "--bare", nudo], check=True, capture_output=True)
        g("init", "-q")
        g("config", "user.email", "prova@prova")
        g("config", "user.name", "prova")
        g("checkout", "-q", "-b", "lavoro")
        open(os.path.join(d, "a.txt"), "w").write("x\n")
        g("add", "-A")
        g("commit", "-q", "-m", "base")
        g("remote", "add", "origin", nudo.replace("\\", "/"))
        # ### il ramo guardiano nasce PRIMA dei hook (come nella realta': lo crea il guardiano)
        g("branch", "guardiano")
        os.makedirs(ganci)
        py = sys.executable.replace("\\", "/")
        me = os.path.abspath(__file__).replace("\\", "/")
        open(os.path.join(ganci, "pre-commit"), "w", newline="\n").write('#!/bin/sh\n"%s" "%s" --commit || exit 1\n' % (py, me))
        open(os.path.join(ganci, "pre-push"), "w", newline="\n").write('#!/bin/sh\n"%s" "%s" --push || exit 1\n' % (py, me))
        g("config", "core.hooksPath", ganci.replace("\\", "/"))

        def caso_commit(che, ramo, entra):
            g("checkout", "-q", ramo)
            prima = g("rev-parse", "HEAD").stdout.strip()
            open(os.path.join(d, "a.txt"), "a").write("%s\n" % che)
            g("add", "-A")
            q = g("commit", "-q", "-m", che, controlla_=False)
            dopo = g("rev-parse", "HEAD").stdout.strip()
            e = dopo != prima
            if not e:
                g("reset", "-q", "--hard")
            ok.append(e == entra)
            print("  DEVE: %-70s %s (il commit %s; atteso %s)" % (che, "PASSA" if e == entra else "### FALLISCE", "ENTRATO" if e else "RIFIUTATO", "ENTRA" if entra else "RIFIUTATO"))
            if not e and q.stderr:
                print("        il hook: %s" % q.stderr.decode("utf-8", "replace").strip()[:160])

        def caso_push(che, spec, entra):
            q = g("push", "-q", "origin", spec, controlla_=False)
            e = q.returncode == 0
            ok.append(e == entra)
            print("  DEVE: %-70s %s (il push %s; atteso %s)" % (che, "PASSA" if e == entra else "### FALLISCE", "ENTRATO" if e else "RIFIUTATO", "ENTRA" if entra else "RIFIUTATO"))
            if not e and q.stderr:
                print("        il hook: %s" % q.stderr.decode("utf-8", "replace").strip()[:160])
        caso_commit("(1) un commit sul ramo guardiano", "guardiano", False)
        caso_commit("(2) un commit sul ramo lavoro", "lavoro", True)
        g("checkout", "-q", "-b", "guardiano-x")
        caso_commit("(3) DEVE ENTRARE: un commit sul ramo guardiano-x", "guardiano-x", True)
        g("checkout", "-q", "lavoro")
        caso_push("(4) git push origin lavoro", "lavoro", True)
        caso_push("(5) git push origin lavoro:guardiano", "lavoro:guardiano", False)
        caso_push("(6) git push origin guardiano", "guardiano", False)
        caso_push("(7) git push origin guardiano-x", "guardiano-x", True)
    finally:
        for x in (d, nudo, ganci):
            shutil.rmtree(x, ignore_errors=True)
    print("### %d casi: %d PASSANO, %d FALLISCONO" % (len(ok), sum(ok), len(ok) - sum(ok)))
    return 0 if all(ok) else 1


def main(argv):
    if argv[:1] == ["--commit"]:
        cod, t = decidi_commit(ramo_corrente())
    elif argv[:1] == ["--push"]:
        cod, t = decidi_push(sys.stdin.read().splitlines())
    elif argv[:1] == ["--collaudo"]:
        return collaudo()
    else:
        print(__doc__)
        return 2
    if cod:
        sys.stderr.write(t)
    return cod


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
