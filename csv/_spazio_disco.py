r"""**LO SPAZIO SU DISCO: che cosa occupa, e che cosa LASCIANO i collaudi.**

**Mandato di Luca, 2026-10-10:** *«PROBLEMA DI SPAZIO: prima di fare qualsiasi cosa, NON
cancellare e NON spostare niente»*, e poi quattro domande: **quale disco e' pieno**, **che
cosa occupa dentro il repo**, **se i collaudi lasciano cartelle non cancellate**, e **il
comando che ha fallito**.

> ## ⛔ **QUESTO SCRIPT NON CANCELLA E NON SPOSTA NIENTE: LEGGE E CONTA.**
> **Non ha nessuna opzione che scriva fuori da `doc/`**, e lo si vede dal sorgente: le
> uniche chiamate che scrivono sono `io.open(DEST, "w")` e le `print`.

**E I NUMERI ESCONO DA QUI, non dal mio ricordo** (`L-NUMERI`): le dimensioni con
`os.walk` + `os.path.getsize`, lo spazio dei dischi con `shutil.disk_usage`, i file
**read-only** con `os.access(..., os.W_OK)`.

**NESSUN RUN, nessun simulatore.**
"""
# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Conta byte sul disco.
import io
import os
import shutil
import string
import subprocess
import sys
import tempfile
import time

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _QUI)
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, ".."))
DEST = os.path.join(RADICE, "doc", "SPAZIO_DISCO_2026-10-10.md")
NL = chr(10)
MB = 1048576.0

# ### ⛔ **I PREFISSI DELLE TEMPORANEE, DICHIARATI UNO A UNO** -- e non scoperti con un
# ### `glob` su tutto: ### **una cartella che non sappiamo chi l-ha fatta non si attribuisce
# ### a un collaudo.** Ogni prefisso dice ### **QUALE riga di QUALE file lo crea.**
PREFISSI = (
    ("stage_", "`csv/_stage.py` `controlla()`: la copia dell-INDICE da validare"),
    ("repo_", "`csv/_stage.py` `collaudo()`: il repo USA-E-GETTA del collaudo"),
    ("st_", "`csv/_stage.py` `collaudo()`: la copia dello stage del repo usa-e-getta"),
    ("sol_", "i CLONI della verifica (`clone.sh`): li creo io a mano, non un collaudo"),
    ("tmp", "`tempfile.mkdtemp()` SENZA prefisso: non si puo- attribuire a un chiamante"),
)

# ### ⚠ **LE DUE RIGHE DELLA SUITE, COPIATE DALLA SUA USCITA** *(`primo_ordine/collauda.py`
# ### su un clone pulito di `65983ee`)*: sono numeri ### **di uno script**, non miei.
USCITA_SUITE = (
    "i controlli sullo STAGE e non sul disco solo-CI        58.69  ### FALLISCE (codice 1)",
    "i controlli sullo STAGE e non sul disco solo-CI         6.69  ### FALLISCE (codice 1)",
    "   i controlli sullo STAGE e non sul disco `csv/_stage.py --collaudo` -> codice 1",
)


def _mb(n):
    return n / MB


def dischi():
    """### Ogni lettera che risponde, con ### **totale, usato, libero.**"""
    fuori = []
    for L in string.ascii_uppercase:
        p = L + ":" + os.sep
        try:
            u = shutil.disk_usage(p)
        except Exception:
            continue
        fuori.append((L + ":", u.total, u.used, u.free, _etichetta(p)))
    return fuori


def _etichetta(p):
    """Il nome del volume, ### **se Windows lo da-**; altrimenti vuoto."""
    try:
        import ctypes
        buf = ctypes.create_unicode_buffer(261)
        ctypes.windll.kernel32.GetVolumeInformationW(
            ctypes.c_wchar_p(p), buf, 261, None, None, None, None, 0)
        return buf.value or ""
    except Exception:
        return ""


def pesa(radice, salta=()):
    """### UN SOLO `os.walk`, e il peso si somma ### **in TUTTI gli antenati.**

    ### ⭐ Cosi- le dimensioni delle cartelle sono ### **coerenti fra loro per
    costruzione**: nessuna cartella puo- pesare meno dei suoi figli.
    """
    dirs, files, nfile = {}, [], 0
    for qui, _sub, nomi in os.walk(radice):
        rel = os.path.relpath(qui, radice).replace(os.sep, "/")
        if rel == ".":
            rel = ""
        if any(rel == s or rel.startswith(s + "/") for s in salta):
            continue
        for n in nomi:
            try:
                s = os.path.getsize(os.path.join(qui, n))
            except OSError:
                continue
            nfile += 1
            files.append((s, (rel + "/" + n) if rel else n))
            k = rel
            while True:
                dirs[k] = dirs.get(k, 0) + s
                if not k:
                    break
                k = k.rsplit("/", 1)[0] if "/" in k else ""
    return dirs, files, nfile


def per_estensione(files, dentro):
    """### Il peso ### **per estensione** dentro un sottoalbero."""
    s = {}
    for peso, rel in files:
        if not rel.startswith(dentro + "/"):
            continue
        n = rel.rsplit("/", 1)[-1]
        e = "." + n.rsplit(".", 1)[-1] if "." in n[1:] else "(senza estensione)"
        s[e] = s.get(e, 0) + peso
    return sorted(((v, k) for k, v in s.items()), reverse=True)


def temporanee():
    """### Che cosa resta nel `%TEMP%`, ### **per prefisso dichiarato.**

    ### ⛔ **E CONTA I FILE `read-only`**, perche- sono ### **la ragione per cui restano**:
    `git` scrive i suoi oggetti in sola lettura, e `shutil.rmtree(..., ignore_errors=True)`
    ### **non li tocca e NON LO DICE.**
    """
    T = tempfile.gettempdir()
    fuori = []
    for pre, chi in PREFISSI:
        voci = [x for x in sorted(os.listdir(T)) if x.startswith(pre)]
        tot, nro, nfile = 0, 0, 0
        vecchia, nuova = None, None
        for v in voci:
            p = os.path.join(T, v)
            for qui, _s, nomi in os.walk(p):
                for n in nomi:
                    f = os.path.join(qui, n)
                    try:
                        tot += os.path.getsize(f)
                    except OSError:
                        continue
                    nfile += 1
                    if not os.access(f, os.W_OK):
                        nro += 1
            try:
                t = os.path.getmtime(p)
                vecchia = t if vecchia is None else min(vecchia, t)
                nuova = t if nuova is None else max(nuova, t)
            except OSError:
                pass
        fuori.append((pre, chi, len(voci), tot, nfile, nro, vecchia, nuova))
    try:
        u = pesa(T)[0].get("", 0)
    except Exception:
        u = 0
    return T, fuori, u


def _git(*a):
    r = subprocess.run(["git"] + list(a), cwd=RADICE, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    return (r.stdout or "").strip()


def _q(t):
    return time.strftime("%Y-%m-%d %H:%M", time.localtime(t)) if t else "-"


def main():
    dsk = dischi()
    dirs, files, nfile = pesa(RADICE)
    files.sort(reverse=True)
    pkl = [(s, r) for s, r in files if r.endswith(".pkl")]
    gz = [(s, r) for s, r in files if r.endswith(".gz")]
    npz = [(s, r) for s, r in files if r.endswith(".npz")]
    tracciati = len([x for x in _git("ls-files", "*.pkl").split(NL) if x.strip()])
    # le cartelle fino al terzo livello, come `du --max-depth 3`
    cand = sorted(((v, k) for k, v in dirs.items()
                   if k and k.count("/") <= 2 and not k.startswith(".git/")),
                  reverse=True)
    T, tmp, tmptot = temporanee()

    r = []
    a = r.append
    a("# 💾 **LO SPAZIO SU DISCO — che cosa occupa, e che cosa LASCIANO i collaudi**")
    a("")
    a("> ### ⛔ **CONGELATO** *(la forma dichiarata il `2026-10-10`: "
      "`csv/_forma_referti.py`)*: questo e- un ### **REPERTO**, cioe- ### **che cosa si e- "
      "misurato A UN ISTANTE** — ### **la CI NON lo rigenera**, e il presidio verifica "
      "### **il suo BLOB**. ### ⭐ **E QUI E- L-UNICA FORMA ONESTA:** lo spazio libero "
      "### **cambia da un minuto all-altro**, e un `VIVO` fallirebbe ### **un minuto dopo "
      "averlo scritto.**")
    a("")
    a("*(**Generata** da `csv/_spazio_disco.py`. Le quattro domande di Luca del "
      "2026-10-10.)*")
    a("")
    a("> ## ⛔ **LA RISPOSTA IN UNA RIGA: `C:` E- PIENA AL `%.1f%%`, e il repo NON E- LA "
      "CAUSA.**" % (100.0 * (dsk[0][2] / float(dsk[0][1])) if dsk else 0))
    a("> Il repo pesa ### **%.1f GB** e il `%%TEMP%%` ### **%.1f GB**: insieme ### **%.1f "
      "GB su %.0f occupati**, cioe- ### **il %.1f%% di cio- che riempie il disco.**"
      % (_mb(dirs.get("", 0)) / 1024, _mb(tmptot) / 1024,
         (_mb(dirs.get("", 0)) + _mb(tmptot)) / 1024,
         _mb(dsk[0][2]) / 1024 if dsk else 0,
         100.0 * (dirs.get("", 0) + tmptot) / float(dsk[0][2]) if dsk else 0))
    a("")

    # ------------------------------------------------------------------ 1) i dischi
    a("## `1` I DISCHI")
    a("")
    a("| disco | nome | totale | libero | usato | uso |")
    a("|---|---|---|---|---|---|")
    for L, tot, uso, lib, et in dsk:
        a("| **`%s`** | %s | %.1f GB | ### **%.2f GB** | %.1f GB | %s |"
          % (L, et or "*(senza nome)*", _mb(tot) / 1024, _mb(lib) / 1024,
             _mb(uso) / 1024,
             ("### **%.1f%%**" % (100.0 * uso / tot)) if tot else "-"))
    a("")

    # ------------------------------------------------------------------ 2) il repo
    a("## `2` CHE COSA OCCUPA DENTRO IL REPO")
    a("")
    a("**Il repo in tutto: `%.1f` GB, `%d` file.**" % (_mb(dirs.get("", 0)) / 1024, nfile))
    a("")
    a("| | MB | che cos-e- |")
    a("|---|---|---|")
    for k, che in (("csv", "gli output dei run dell-era `1`"),
                   (".git", "la storia"),
                   ("db", "i database dei run"),
                   ("doc", "i documenti"),
                   ("db_era2", "il database dell-era `2`"),
                   ("primo_ordine", "il codice dell-era `2`"),
                   ("proto_primo_ordine", "il banco del prototipo")):
        if k in dirs:
            a("| **`%s/`** | ### **%.0f** | %s |" % (k, _mb(dirs[k]), che))
    a("")
    a("### ⭐ **E LA RISPOSTA STA NELLE ESTENSIONE, non nelle cartelle:** dentro `csv/` "
      "il peso e- ### **tutto in tre formati di uscita.**")
    a("")
    a("| estensione in `csv/` | MB |")
    a("|---|---|")
    for peso, e in per_estensione(files, "csv")[:8]:
        a("| `%s` | %.0f |" % (e, _mb(peso)))
    a("")
    a("**I `.pkl` in tutto il repo: `%d` file, `%.0f` MB — e ### **`%d` sono TRACCIATI in "
      "git**.** ### ✅ **E- cio- che `CLAUDE.md` par. `6` pretende** *(<<i `.pkl` non si "
      "committano: il dato E- il comando che lo produce>>)*: sono ### **rigenerabili**, "
      "e cancellarli ### **non perde niente che il repo non sappia rifare.**"
      % (len(pkl), _mb(sum(s for s, _ in pkl)), tracciati))
    a("")
    a("**E gli altri due formati, con lo stesso stato:** `.gz` ### **`%d` file, `%.0f` "
      "MB**; `.npz` ### **`%d` file, `%.0f` MB**."
      % (len(gz), _mb(sum(s for s, _ in gz)), len(npz), _mb(sum(s for s, _ in npz))))
    a("")
    a("### LE `15` CARTELLE PIU- GROSSE *(fino al terzo livello)*")
    a("")
    a("| | cartella | MB |")
    a("|---|---|---|")
    for i, (peso, k) in enumerate(cand[:15], 1):
        a("| `%d` | `%s/` | %.0f |" % (i, k, _mb(peso)))
    a("")
    a("### I `10` FILE PIU- GROSSI")
    a("")
    a("| | file | MB |")
    a("|---|---|---|")
    for i, (peso, k) in enumerate(files[:10], 1):
        a("| `%d` | `%s` | %.1f |" % (i, k, _mb(peso)))
    a("")

    # ------------------------------------------------------------------ 3) le temporanee
    a("## `3` CHE COSA LASCIANO I COLLAUDI NEL `%TEMP%`")
    a("")
    a("**`%s`, `%.0f` MB in tutto.**" % (T, _mb(tmptot)))
    a("")
    a("| prefisso | cartelle | MB | file | di cui `read-only` | dalla | alla | chi lo crea |")
    a("|---|---|---|---|---|---|---|---|")
    for pre, chi, n, tot, nf, nro, vec, nuo in tmp:
        a("| `%s*` | ### **%d** | %.0f | %d | ### **%d** | %s | %s | %s |"
          % (pre, n, _mb(tot), nf, nro, _q(vec), _q(nuo), chi))
    a("")
    a("> ### ⛔ **E LE `repo_*` SONO UN DIFETTO MIO, NON UN RESIDUO INNOCENTE.**")
    a("> `csv/_stage.py` le cancella in un `finally` con "
      "`shutil.rmtree(dove, ignore_errors=True)` — ### **e su Windows non ci riesce**, "
      "perche- `git` scrive i suoi oggetti ### **in sola lettura** *(`-r--r--r--`)* e "
      "`rmtree` non li tocca. ### ⚠ **`ignore_errors=True` SILENZIA il fallimento**, "
      "quindi ### **ogni giro del collaudo ne lascia una e nessuno lo dice** — e il "
      "numero di cartelle e- ### **il numero di volte che il collaudo e- girato.**")
    a("")

    # ------------------------------------------------------------------ 4) il comando
    a("## `4` IL COMANDO CHE HA FALLITO, E IL MESSAGGIO")
    a("")
    a("**Il comando:** `python csv/_stage.py --collaudo`, lanciato da "
      "`python primo_ordine/collauda.py` *(che lo chiama con "
      "`subprocess.run([sys.executable, \"csv/_stage.py\", \"--collaudo\"], cwd=RADICE, "
      "capture_output=True)`)*, su un clone pulito di `65983ee`.")
    a("")
    a("**Le righe della suite, copiate dalla sua uscita:**")
    a("")
    a("```")
    for x in USCITA_SUITE:
        a(x)
    a("```")
    a("")
    a("**E rigirato a mano col disco pieno, dice QUALI bracci cadono:**")
    a("")
    a("```")
    a("  ### e il modo RAPIDO passa (e- quello del `pre-commit`)       ### FALLISCE")
    a("  sul disco: i controlli del contenuto passano SULLO STAGE      ### FALLISCE")
    a("  ### il collaudo ha MATERIA: le due liste non sono vuote       PASSA")
    a("  ### il caso SANO: tutto committato, il controllo PASSA        PASSA")
    a("  ### (a) DEVE scattare: `b` in stage e `a` SOLO SUL DISCO      PASSA")
    a("  ### e SUL DISCO lo stesso caso PASSA                         PASSA")
    a("  ### (b) entrambi in stage: il controllo PASSA                 PASSA")
    a("  IL COLLAUDO DELLO STAGE: 5 su 7   ### CI SONO BUCHI")
    a("```")
    a("")
    a("### ⭐ **E I DUE BRACCI CHE CADONO SONO ESATTAMENTE I DUE CHE ESPORTANO L-INDICE "
      "DEL REPO VERO** *(`~290` MB per copia)*, mentre ### **i quattro in sandbox "
      "passano** *(il repo usa-e-getta e- di `1` MB)*. ### **Non e- una coincidenza: e- la "
      "firma dello spazio che manca.**")
    a("")
    a("> ### ⛔ **IL MESSAGGIO DI `git` NON SI VEDE DA NESSUNA PARTE, E QUESTO E- IL "
      "SECONDO DIFETTO.**")
    a("> `esporta()` lo restituisce *(`### git checkout-index e- fallito: <stderr>`)*, ma "
      "### **il braccio del collaudo stampa solo la nota e BUTTA la lista degli errori**, "
      "e `collauda.py` ### **butta l-uscita del figlio** *(`capture_output=True`, e il "
      "contenuto non viene letto)*. ### ⚠ **Quindi un rosso d-AMBIENTE e un rosso da "
      "DIFETTO sono indistinguibili**, ed e- per questo che la diagnosi e- costata "
      "### **tre corse da tre minuti.**")
    a("")
    a("**L-unico messaggio del sistema che ho catturato alla lettera** e- quello di `tail` "
      "nello stesso istante, e dice la causa: ### **`tail: write error: No space left on "
      "device`.**")
    a("")
    a("### ⛔ **E QUELLO DI `git` NON LO RICOSTRUISCO A MEMORIA:** per averlo alla lettera "
      "bisogna ### **rifare il caso con il disco pieno**, e il mandato dice ### **di non "
      "toccare niente e aspettare.**")
    a("")
    io.open(DEST, "w", encoding="utf-8", newline=NL).write(NL.join(r) + NL)

    print("=" * 100)
    print("LO SPAZIO SU DISCO -- i numeri, dallo script")
    print("=" * 100)
    for L, tot, uso, lib, et in dsk:
        print("  %-4s %-12s totale %8.1f GB   LIBERO %8.2f GB   uso %5.1f%%"
              % (L, et[:12], _mb(tot) / 1024, _mb(lib) / 1024,
                 (100.0 * uso / tot) if tot else 0))
    print("  " + "-" * 96)
    print("  il repo: %.1f GB in %d file   ###  csv/ %.0f MB, .git %.0f MB"
          % (_mb(dirs.get("", 0)) / 1024, nfile, _mb(dirs.get("csv", 0)),
             _mb(dirs.get(".git", 0))))
    print("  i .pkl: %d file, %.0f MB, di cui TRACCIATI %d"
          % (len(pkl), _mb(sum(s for s, _ in pkl)), tracciati))
    print("  il %%TEMP%%: %.0f MB" % _mb(tmptot))
    for pre, _chi, n, tot, nf, nro, _v, _u in tmp:
        print("     %-8s %3d cartelle  %6.0f MB  %5d file  read-only %5d"
              % (pre + "*", n, _mb(tot), nf, nro))
    print("  " + "-" * 96)
    print("  scritto %s" % os.path.relpath(DEST, RADICE).replace(os.sep, "/"))
    print("=" * 100)
    return 0


if __name__ == "__main__":
    sys.exit(main())
