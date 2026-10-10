r"""**LA VERIFICA SU UN CLONE PULITO — UNO SOLO, E SEMPRE CANCELLATO.**

**Decisione di Luca, 2026-10-10:** *«al massimo UN clone di verifica alla volta; dove basta, un
clone leggero (es. `--local` sullo stesso volume, o senza la storia se la verifica non la usa) --
**dichiara quale e perche'**»*, e *«ogni clone o cartella temporanea si cancella SEMPRE
(`try`/`finally`)»*.

> ## ⛔ **IL DISCO PIENO L'HANNO CAUSATO `11` CLONI LASCIATI NEL `%TEMP%`: `6.8` GB.**
> Li facevo **a mano**, uno per corsa, e **nessuno li cancellava**. ### **Questo file esiste
> perche' quella verifica diventi UNO STRUMENTO con un `finally`**, invece di tre righe di
> shell che ogni volta riscrivo.

### ⭐ **QUALE CLONE, E PERCHE' — la dichiarazione che il mandato chiede:**
**`git clone --local`**, cioe' **gli oggetti si HARDLINKANO** invece di essere copiati: sullo
stesso volume il clone costa **quasi zero byte** e **la storia resta INTERA**.
### ⛔ **E la storia SERVE, quindi `--depth 1` NON si puo':** `H-P8` pretende che un confronto
prenda il codice di prima **dal PADRE**, `_replay_registri` legge **lo storico dei commit**, e
`indice.py storico-commit` **ricava il commit di una riga dai log**. ### ⚠ **Un clone
superficiale farebbe passare quei presidi PER VACUITA'** — che e' peggio di non girarli.

**NESSUN RUN del simulatore.**
"""
# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Clona e fa girare i collaudi.
import io
import os
import subprocess
import sys
import tempfile
import time

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _QUI)
import _presidio                                             # noqa: E402
import _pulizia                                              # noqa: E402

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, ".."))
NL = chr(10)
PRESIDIO = "P-CLONE-PULITO"
RAMO = "primo-ordine"

# ### ⛔ **I SEI COMANDI, DICHIARATI, e ognuno nei DUE AMBIENTI** -- perche- `CI=true`
# ### ### **accende i passi che rigenerano**, e il 2026-10-10 ### **i cinque referti che
# ### la CI rigenerava erano esattamente i cinque che si rompevano.**
COMANDI = (
    ("valida", "csv/indice.py valida"),
    ("la suite dei collaudi", "primo_ordine/collauda.py"),
    ("la prossima domanda", "csv/indice.py prossima"),
)


def _gira(dove, cmd, ci):
    e = dict(os.environ)
    if ci:
        e["CI"] = "true"
    else:
        e.pop("CI", None)
    t0 = time.perf_counter()
    r = subprocess.run([sys.executable] + cmd.split(), cwd=dove, capture_output=True,
                       env=e)
    out = ((r.stdout or b"") + (r.stderr or b"")).decode("utf-8", "replace")
    return time.perf_counter() - t0, r.returncode, out


def _git(dove, *a):
    r = subprocess.run(["git"] + list(a), cwd=dove, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    return r.returncode, (r.stdout or "").strip(), (r.stderr or "").strip()


def verifica():
    rotti = []
    dove = tempfile.mkdtemp(prefix="clone_verifica_")
    # ### ⛔ **`mkdtemp` crea la cartella, e `git clone` la vuole VUOTA o inesistente:**
    # ### quindi si clona ### **dentro**, in una sottocartella.
    clone = os.path.join(dove, "repo")
    try:
        print("=" * 100)
        print("LA VERIFICA SU UN CLONE PULITO -- uno solo, e cancellato nel `finally`")
        print("=" * 100)
        c, _o, err = _git(RADICE, "clone", "--local", "--quiet", "--branch", RAMO,
                          RADICE, clone)
        if c != 0:
            print("  ### ⛔ il clone NON si e- fatto: %s" % err[:300])
            return 1
        _git(clone, "config", "core.hooksPath", ".githooks")
        c, head, _e = _git(clone, "rev-parse", "--short", "HEAD")
        sim = ""
        try:
            import hashlib
            sim = hashlib.sha1(io.open(os.path.join(clone, "soliton_simulator.py"),
                                       "rb").read()).hexdigest()[:8]
        except Exception as e:
            sim = "NON LEGGIBILE: %s" % e
        print("  il clone: %s" % clone)
        print("  HEAD: %s     simulatore: %s" % (head, sim))
        print("  ### e il simulatore DEVE essere `b8c21049`: %s"
              % ("SI" if sim == "b8c21049" else "### NO, e- `%s`" % sim))
        if sim != "b8c21049":
            rotti.append(("il simulatore", "sha1", 1, "atteso b8c21049, trovato %s" % sim))
        print("-" * 100)
        print("  %-28s %-10s %9s  %s" % ("il comando", "ambiente", "secondi", "esito"))
        print("  " + "-" * 94)
        for nome, cmd in COMANDI:
            for ci in (False, True):
                s, rc, out = _gira(clone, cmd, ci)
                print("  %-28s %-10s %9.2f  %s"
                      % (nome, "CI=true" if ci else "senza CI", s,
                         "ok" if rc == 0 else "### FALLISCE (codice %d)" % rc))
                if rc != 0:
                    rotti.append((nome, cmd + (" [CI]" if ci else ""), rc, out))

        # ------------------------------------------------- `git status` VUOTO
        _c, fuori, _e = _git(clone, "status", "--porcelain")
        righe = [x for x in fuori.split(NL) if x.strip()]
        print("  " + "-" * 94)
        print("  `git status` dopo tutto: %s"
              % ("VUOTO" if not righe else "### %d FILE SPORCHI" % len(righe)))
        for x in righe[:8]:
            print("      | %s" % x)
        if righe:
            rotti.append(("`git status` dopo la suite", "git status --porcelain", 1,
                          NL.join(righe)))

        # ------------------------------------------------- nessun residuo
        res = _pulizia.residui(prefissi=("stage_", "repo_", "st_", "sol_"))
        print("  residui nel `%%TEMP%%` dei nostri prefissi: %s"
              % ("NESSUNO" if not res else "### %d" % len(res)))
        for p, n, b in res[:6]:
            print("      | %s   %d file   %d byte" % (p, n, b))
        if res:
            rotti.append(("i residui nel `%TEMP%`", "csv/_pulizia.py --residui", 1,
                          NL.join("%s (%d file)" % (p, n) for p, n, _b in res)))
    finally:
        # ### ⛔ **IL `finally` E- IL PUNTO DI QUESTO FILE:** il clone se ne va
        # ### ### **anche se tutto e- andato storto**, e se non ci riesce ### **LO DICE.**
        _pulizia.via_finale(dove)
        print("  il clone e- stato cancellato: %s" % (not os.path.exists(dove)))

    print("=" * 100)
    if rotti:
        print("  ### %d COSE NON TORNANO:" % len(rotti))
        for nome, cmd, rc, out in rotti:
            print("     %-30s `%s` -> codice %d" % (nome, cmd, rc))
            coda = [x for x in str(out).split(NL) if x.strip()][-20:]
            for riga in coda:
                print("        | %s" % riga[:160])
    else:
        print("  ### TUTTO VERDE: %d comandi nei due ambienti, `git status` vuoto, "
              "nessun residuo" % (2 * len(COMANDI)))
    print("=" * 100)
    return 1 if rotti else 0


if __name__ == "__main__":
    sys.exit(verifica())
