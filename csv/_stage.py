# -*- coding: utf-8 -*-
"""I CONTROLLI SI FANNO SULLO **STAGE**, non sul **DISCO** — *cioè su ciò che il commit
contiene davvero.*

> ### ⛔ **IL DIFETTO, misurato dal guardiano su un clone pulito di `c68b635`:** `valida`
> FALLISCE — `PI-REPLAY` su `Z47` e `Z103`, perché quel commit porta ### **`4` righe di
> storico SENZA `voci.jsonl`.** ### **E il `pre-commit` NON l'ha fermato**, perché i
> controlli ### **leggono i file SUL DISCO** — dove `voci.jsonl` era già modificata — e
> ### **non il contenuto IN STAGE.**

### ⭐ **E L'ESPOSIZIONE L'HO CREATA IO, poche ore prima:** curando la ricorrenza dello
storico ho messo `_stage_storico()` nel percorso di scrittura, che mette `storico.jsonl`
### **in stage appena ci scrive** — e `git commit` committa ### **l'INDICE**, quindi un
commit che non fa `git add` di `voci.jsonl` ### **si porta via le righe da sole.**

### 📌 **COME:** si esporta l'indice in una cartella temporanea *(`git checkout-index`)* e
i controlli girano ### **là**, con `GIT_DIR` che punta al repo vero — così `git show` e
`git diff --cached` continuano a vedere ### **lo stesso indice**, e gli strumenti vedono
### **i byte che il commit conterrà.**

### ⚠ **E IL LIMITE E' DICHIARATO, non taciuto** *(`A9`)*: **non** tutti i controlli del
`pre-commit` possono girare sullo stage, e la tabella `SULLO_STAGE` dice ### **quali
sì e quali no, col motivo.** ### ⛔ **Un controllo che guarda lo STATO DELL'ALBERO**
*(i file non tracciati, l'impronta dei hook, la lista `FILE CAMBIATI`)* ### **sullo stage
non vedrebbe niente, e tacerebbe per vacuità** — che è peggio di leggere il disco.

Gira con:  python csv/_stage.py  ·  --collaudo
"""
import io
import os
import shutil
import subprocess
import sys
import tempfile

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
sys.path.insert(0, _QUI)
import _presidio                                             # noqa: E402

# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Esporta l'indice di git e fa
# girare i controlli del contenuto su quei byte.

PRESIDIO = "PRESIDI-SUL-DISCO-NON-SULLO-STAGE"

NL = chr(10)

# ### ⛔ **I CONTROLLI DEL CONTENUTO: girano SULLO STAGE.** Sono quelli che leggono
# ### ### **i file del repo** e dicono se ciò che c'è scritto è coerente.
SULLO_STAGE = (
    ("il validatore dell-indice", "csv/indice.py valida"),
    ("`P-T2` il replay dei registri", "csv/_replay_registri.py --collaudo"),
    ("`P-ALB` l-albero delle scelte", "csv/_albero_era2.py --collaudo"),
    ("i presidi dell-indice", "csv/_presidio_indice.py --collaudo"),
    ("i controlli della migrazione", "csv/_controlli_indice_v2.py"),
)

# ### ⚠ **E QUESTI NO, e il motivo e- scritto uno per uno.** ### **Non e- una
# ### scorciatoia:** un controllo che guarda ### **lo STATO DELL-ALBERO** sullo stage
# ### ### **non vedrebbe niente**, e ### **tacerebbe per vacuita-.**
SUL_DISCO = (
    ("`H-NON-TRACCIATI`", "guarda i file NON TRACCIATI: nello stage, per definizione, "
                          "NON CE NE SONO -- la- tacerebbe sempre"),
    ("`H-FILE`", "confronta la lista del messaggio con `git diff --cached`: guarda "
                 "L-INDICE, quindi e- GIA- sullo stage per costruzione"),
    ("`P-BARRIERA`", "guarda l-impronta dei hook ATTIVI e `core.hooksPath`: e- lo stato "
                     "della macchina, non un contenuto del commit"),
    ("`P-TEMPI` e i collaudi della fisica",
     "misurano il COMPORTAMENTO del codice, e il codice che gira e- quello sul disco: "
     "farli sullo stage raddoppierebbe il tempo del `pre-commit`, che e- la ragione "
     "numero uno per dare `--no-verify` (`A9` dal lato del tempo)"),
)


def esporta(dove):
    """### Esporta ### **l-INDICE** in `dove`. ### `[]` se e- andata, gli errori se no."""
    r = subprocess.run(["git", "checkout-index", "-a", "--prefix=" + dove + os.sep],
                       cwd=RADICE, capture_output=True, text=True, encoding="utf-8",
                       errors="replace")
    if r.returncode != 0:
        return ["### `%s`: `git checkout-index` e- fallito: %s"
                % (PRESIDIO, ((r.stderr or "") + (r.stdout or "")).strip()[:200])]
    return []


def _ambiente(dove):
    """### `GIT_DIR` al repo VERO, `GIT_WORK_TREE` alla copia dello stage.

    ### ⭐ **Cosi- `git show :<file>` e `git diff --cached` vedono LO STESSO INDICE**, e
    gli strumenti leggono ### **i byte che il commit conterra-.**
    """
    e = dict(os.environ)
    # ### ⛔ **E SI TOLGONO LE VARIABILI CHE GIT INIETTA NEL HOOK**, e questo l-ho
    # ### ### **misurato dentro un commit**: fuori dal hook i controlli passavano, dentro
    # ### il hook ### **`_presidio` diceva <<NON TRACCIATO>>** sulla copia. ### **`GIT_PREFIX`
    # ### e- la cartella relativa da cui git e- stato invocato**, e nella copia
    # ### ### **non vuol dire niente**: fa risolvere i percorsi nel posto sbagliato.
    # ### ⚠ **`GIT_INDEX_FILE` INVECE RESTA**, ed e- giusto: e- l-indice del commit
    # ### in corso, cioe- ### **esattamente cio- che si vuole validare.**
    for _v in ("GIT_PREFIX", "GIT_WORK_TREE", "GIT_COMMON_DIR"):
        e.pop(_v, None)
    # ### ⛔ **E I PERCORSI DI GIT SI RENDONO ASSOLUTI, e questo l-ho MISURATO dentro
    # ### un commit:** nel hook git mette `GIT_INDEX_FILE` ### **RELATIVO**
    # ### *(`.git/index`)*, e il figlio gira ### **in un-altra cartella** — quindi
    # ### quel percorso puntava a ### **un indice che non esiste**, `git ls-files` diceva
    # ### ### **<<NON TRACCIATO>>** e `git show :<file>` falliva.
    # ### ⚠ **Fuori dal hook non si vedeva**, perche- fuori dal hook quelle variabili
    # ### ### **non ci sono**: e- la TERZA volta oggi che un presidio si comporta
    # ### ### **diversamente DENTRO un commit.**
    for _v in ("GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY",
               "GIT_ALTERNATE_OBJECT_DIRECTORIES"):
        _x = e.get(_v)
        if _x and not os.path.isabs(_x):
            e[_v] = os.path.abspath(os.path.join(RADICE, _x))
    e["GIT_DIR"] = os.path.join(RADICE, ".git")
    e["GIT_WORK_TREE"] = dove
    # ### ⚠ **E si dichiara di essere sullo stage**, perche- uno strumento che volesse
    # ### ### **saperlo** non debba indovinarlo.
    e["PRESIDI_SULLO_STAGE"] = "1"
    return e


# ### ⛔ **IL PRIMO DELLA LISTA E- IL <<RAPIDO>>, e la divisione e- MISURATA:**
# ### i cinque controlli sullo stage costano ### **`46.5` s**, e il `pre-commit` ne costa
# ### gia- ### **`80`** -- insieme fanno ### **`126` s, OLTRE il budget di `120`**, e un
# ### `pre-commit` troppo lento e- ### **la ragione numero uno per dare `--no-verify`**
# ### *(`A9` dal lato del tempo)*.
# ### ✅ **Quindi nel hook gira SOLO il primo** *(il validatore dell-indice, `~13` s)*,
# ### che e- ### **quello che prende il difetto vero** -- l-incoerenza fra `voci.jsonl` e
# ### `storico.jsonl`. ### **La serie INTERA gira in CI e nel comando unico**, dove il
# ### tempo non spinge nessuno a spegnere niente.
RAPIDI = 1


def controlla(dove=None, rapido=False):
    """### `[]` se ogni controllo del contenuto passa ### **sui byte dello STAGE.**"""
    proprio = dove is None
    dove = dove or tempfile.mkdtemp(prefix="stage_")
    try:
        err = esporta(dove)
        if err:
            return err
        env = _ambiente(dove)
        for nome, cmd in (SULLO_STAGE[:RAPIDI] if rapido else SULLO_STAGE):
            pezzi = cmd.split()
            via = os.path.join(dove, pezzi[0].replace("/", os.sep))
            if not os.path.exists(via):
                err.append("### `%s` %s: `%s` NON E- NELLO STAGE -- e un controllo che "
                           "non c-e- non controlla niente" % (PRESIDIO, nome, pezzi[0]))
                continue
            r = subprocess.run([sys.executable, via] + pezzi[1:], cwd=dove,
                               capture_output=True, text=True, encoding="utf-8",
                               errors="replace", env=env)
            if r.returncode != 0:
                coda = [x for x in ((r.stdout or "") + (r.stderr or "")).split(NL)
                        if x.strip()][-3:]
                err.append("### `%s` %s: FALLISCE SULLO STAGE (codice %d). ### Il disco "
                           "puo- essere a posto e il COMMIT no: e- esattamente il difetto "
                           "del `2026-10-10`.%s"
                           % (PRESIDIO, nome, r.returncode,
                              (NL + NL.join("        " + x for x in coda))
                              if coda else ""))
        return err
    finally:
        if proprio:
            shutil.rmtree(dove, ignore_errors=True)


# =====================================================================================
#   IL COLLAUDO -- nei DUE versi, su un REPO USA-E-GETTA
# -------------------------------------------------------------------------------------
#   ### ⛔ **Non sul repo vero:** un collaudo che per provarsi deve scrivere nell-indice
#   ### ### **e- lo stesso difetto che nel giro scorso ha cancellato `867`
#   ### classificazioni.** ### ✅ **Qui si costruisce un repo intero da zero**, con un
#   ### `git` vero, e si prova ### **la proprieta-**: cio- che si legge e- lo STAGE.
# =====================================================================================
_VALIDATORE = '''# -*- coding: utf-8 -*-
"""Un validatore finto: la REGOLA e- che se cambia `b` deve cambiare anche `a`."""
import io, sys
a = io.open("a.txt", encoding="utf-8").read().strip()
b = io.open("b.txt", encoding="utf-8").read().strip()
if a != b:
    print("INCOERENTE: a=%s b=%s" % (a, b))
    sys.exit(1)
print("coerente: %s" % a)
sys.exit(0)
'''


def collaudo():
    ok = [0, 0]

    def esito(che, passa, nota=""):
        ok[1] += 1
        ok[0] += 1 if passa else 0
        print("  %-64s %s   %s" % (che, "PASSA" if passa else "### FALLISCE", nota))

    print("=" * 100)
    print("IL COLLAUDO DEI CONTROLLI SULLO STAGE -- nei DUE VERSI")
    print("=" * 100)
    esito("### e il modo RAPIDO passa (e- quello del `pre-commit`)",
          controlla(rapido=True) == [],
          "### %d controllo su %d: il validatore dell-indice, che e- quello che prende "
          "l-incoerenza fra `voci.jsonl` e `storico.jsonl`"
          % (RAPIDI, len(SULLO_STAGE)))
    esito("sul disco: i controlli del contenuto passano SULLO STAGE",
          controlla() == [],
          "%d controlli sullo stage, %d dichiarati sul disco col motivo"
          % (len(SULLO_STAGE), len(SUL_DISCO)))
    esito("### il collaudo ha MATERIA: le due liste non sono vuote",
          len(SULLO_STAGE) >= 3 and len(SUL_DISCO) >= 3,
          "### se una fosse vuota, o non si controllerebbe niente o non si "
          "dichiarerebbe niente")
    # ------------------------------------------------- il repo usa-e-getta
    t = tempfile.mkdtemp(prefix="repo_")
    try:
        def g(*a):
            return subprocess.run(["git"] + list(a), cwd=t, capture_output=True,
                                  text=True, encoding="utf-8", errors="replace")

        def scrivi(nome, testo):
            io.open(os.path.join(t, nome), "w", encoding="utf-8",
                    newline=NL).write(testo + NL)

        g("init", "-q")
        g("config", "user.email", "x@y.z")
        g("config", "user.name", "x")
        scrivi("a.txt", "1")
        scrivi("b.txt", "1")
        scrivi("v.py", _VALIDATORE)
        g("add", "-A")
        g("commit", "-q", "-m", "uno")

        def prova():
            """Esporta l-indice di `t` e fa girare il validatore LA- DENTRO."""
            d = tempfile.mkdtemp(prefix="st_")
            try:
                q = subprocess.run(["git", "checkout-index", "-a",
                                    "--prefix=" + d + os.sep], cwd=t,
                                   capture_output=True)
                if q.returncode != 0:
                    return None
                r = subprocess.run([sys.executable, os.path.join(d, "v.py")], cwd=d,
                                   capture_output=True, text=True, encoding="utf-8",
                                   errors="replace")
                return r.returncode
            finally:
                shutil.rmtree(d, ignore_errors=True)

        esito("### il caso SANO: tutto committato, il controllo PASSA", prova() == 0,
              "### se questo fallisse, i due casi sotto non direbbero niente")
        # ### (a) `b` in stage e `a` SOLO SUL DISCO -> DEVE essere RIFIUTATO
        scrivi("b.txt", "2")
        g("add", "b.txt")
        scrivi("a.txt", "2")            # ### sul DISCO, e NON in stage
        rc_a = prova()
        esito("### (a) DEVE scattare: `b` in stage e `a` SOLO SUL DISCO",
              rc_a == 1,
              "### e- IL DIFETTO: sul disco e- coerente, nel COMMIT no -- e il presidio "
              "vecchio avrebbe detto <<a posto>>")
        # ### e il verso che dimostra che il difetto ERA REALE: sul DISCO passa
        rd = subprocess.run([sys.executable, os.path.join(t, "v.py")], cwd=t,
                            capture_output=True)
        esito("### e SUL DISCO lo stesso caso PASSA: ecco perche- nessuno lo vedeva",
              rd.returncode == 0,
              "### il disco diceva <<coerente>>, e il commit NON lo era")
        # ### (b) entrambi in stage -> PASSA
        g("add", "a.txt")
        esito("### (b) entrambi in stage: il controllo PASSA", prova() == 0,
              "### la cura non deve rifiutare il caso GIUSTO")
    finally:
        shutil.rmtree(t, ignore_errors=True)
    print("=" * 100)
    print("IL COLLAUDO DELLO STAGE: %d su %d   %s"
          % (ok[0], ok[1], "### TUTTI PASSATI" if ok[0] == ok[1] else "### CI SONO BUCHI"))
    print("=" * 100)
    return 0 if ok[0] == ok[1] else 1


def main(argv):
    _presidio.avvia(__file__)
    if "--collaudo" in argv:
        return collaudo()
    rapido = "--rapido" in argv
    err = controlla(rapido=rapido)
    print("  `%s`: %d controlli del contenuto SULLO STAGE%s, %d dichiarati sul disco "
          "col motivo" % (PRESIDIO, RAPIDI if rapido else len(SULLO_STAGE),
                          " (modo RAPIDO, per il `pre-commit`)" if rapido else "",
                          len(SUL_DISCO)))
    for e in err[:8]:
        print("  %s" % e)
    print("  ### %d errori" % len(err))
    return 1 if err else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
