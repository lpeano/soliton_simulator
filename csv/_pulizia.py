r"""**CANCELLARE UNA CARTELLA TEMPORANEA DAVVERO — e DIRLO se non ci si riesce.**

**Decisione di Luca, 2026-10-10:** *«ogni clone o cartella temporanea si cancella SEMPRE
(`try`/`finally`), e su Windows la cancellazione toglie prima la sola-lettura (`onerror` che fa
`chmod` e riprova); **un fallimento della pulizia e' un ERRORE visibile, non silenziato da
`ignore_errors`**»*.

> ## ⛔ **`shutil.rmtree(dove, ignore_errors=True)` E' LA FORMA DEL DIFETTO, non una
> ## precauzione.**
> `git` scrive i suoi oggetti **in sola lettura** (`-r--r--r--`), su Windows `rmtree` **non li
> tocca**, e ### **`ignore_errors=True` SILENZIA il fallimento**: la cartella resta, e
> ### **nessuno lo dice.**

**MISURATO, non dedotto** *(2026-10-10)*: nel `%TEMP%` c'erano **`24` cartelle `repo_*`** con
**`120` file e tutti e `120` in sola lettura**, lasciate da `csv/_stage.py --collaudo`. **Il
numero di cartelle era il numero di volte che il collaudo era girato.**

### ⚠ **E LA CURA NON E' <<RICORDARSI DI PULIRE>>:** e' **togliere la sola lettura e
RIPROVARE**, e poi **CONTROLLARE CHE LA CARTELLA NON CI SIA PIU'** -- perche' un `rmtree` che
non alza **non e' la prova che abbia cancellato.**

**NESSUN RUN, nessun simulatore.**
"""
# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Cancella cartelle temporanee.
import io
import os
import shutil
import stat
import subprocess
import sys
import tempfile

_QUI = os.path.dirname(os.path.abspath(__file__))

NL = chr(10)
PRESIDIO = "P-PULIZIA"

# ### ⛔ **LA PIATTAFORMA, e NON e- un dettaglio di portabilita-: cambia QUALI
# ### BRACCI POSSONO AVERE MATERIA** *(trovato il 2026-10-10, e sulla CI di GitHub)*.
# ### ⚠ **Su Linux un file in SOLA LETTURA, o APERTO, SI CANCELLA**: il permesso che
# ### conta e- quello della ### **CARTELLA**, non del file. ### ⛔ **Quindi i due
# ### bracci che provano <<`rmtree` non ce la fa>> la- NON POSSONO SCATTARE**, e un braccio
# ### che non puo- avere materia ### **non deve PASSARE ne- FALLIRE in silenzio: deve
# ### DICHIARARSI non applicabile.**
NT = (os.name == "nt")

# ### ⭐ **DOVE STO GIRANDO**, in assoluto: serve a `residui()` per non contare
# ### ### **la cartella che contiene questo file stesso.**
_CASA = os.path.abspath(__file__)

# ### ⛔ **I PREFISSI CHE QUESTO REPO SI LASCIA DIETRO, DICHIARATI UNO A UNO** -- e non
# ### <<tutto cio- che sta nel `%TEMP%`>>: ### **una cartella che non sappiamo chi ha fatto
# ### NON SI CANCELLA.** ### ⚠ **Le `tmp*` senza prefisso NON sono qui, per decisione di
# ### Luca: <<non le tocchi>>.**
NOSTRI = ("stage_", "repo_", "st_", "sol_", "clone_verifica_")


def _riprova(func, percorso, _exc):
    """### Toglie la ### **sola lettura** e RIPROVA. ### **Se non va, ALZA.**"""
    os.chmod(percorso, stat.S_IWRITE)
    func(percorso)


def via(dove):
    """### Cancella l-albero ### **davvero**. ### `[]` se non c-era niente da fare.

    ### ⛔ **ALZA `RuntimeError` se la cartella RESTA**, e questa e- la differenza con
    `ignore_errors=True`: ### **l-assenza di un-eccezione non e- la prova di una
    cancellazione.** ### ✅ **La prova e- che il percorso NON ESISTA PIU-.**
    """
    if not os.path.exists(dove):
        return False
    try:
        shutil.rmtree(dove, onexc=_riprova)
    except TypeError:
        # ### ⚠ **Prima di Python `3.12` il parametro si chiamava `onerror`**, e la
        # ### firma e- la stessa a tre argomenti: ### **si prova l-uno e si ricade
        # ### sull-altro**, invece di leggere la versione e scommetterci.
        shutil.rmtree(dove, onerror=_riprova)
    if os.path.exists(dove):
        raise RuntimeError("### `%s`: la cartella `%s` E- ANCORA LA- dopo `rmtree`"
                           % (PRESIDIO, dove))
    return True


def via_finale(dove):
    """### Per un `finally`: cancella, e ### **se non ci riesce LO DICE sempre.**

    ### \u26d4 **La differenza con `via()` sta in UN CASO SOLO:** se si sta gia-
    propagando un-eccezione, ### **questa non la SOSTITUISCE** -- la stampa e lascia
    passare l-originale. ### \u26a0 **Perche- un `raise` dentro un `finally` CANCELLA
    l-errore vero**, e ### **l-errore vero e- quello che spiega il fallimento.**
    ### \u2705 **Se invece non c-era nessuna eccezione in volo, ALZA** -- cioe-
    ### **la pulizia fallita non passa MAI in silenzio.**
    """
    try:
        return via(dove)
    except Exception as e:
        sys.stderr.write("### \u26d4 `%s`: PULIZIA FALLITA su `%s`: %s%s"
                         % (PRESIDIO, dove, e, NL))
        if sys.exc_info()[0] is None:
            raise
        return False


def residui(prefissi=NOSTRI, radice=None, casa=None):
    """### Le cartelle ### **NOSTRE** rimaste nel `%TEMP%`: `[(percorso, file, byte)]`.

    ### ⭐ **`casa` SI PUO- INIETTARE, e non e- un lusso:** e- cio- che permette al
    collaudo di ### **PROVARE** che la cartella viva non si conta, invece di
    ### **asserirlo** -- e senza iniezione il braccio potrebbe provarlo
    ### **solo stando davvero dentro un clone.**
    """
    T = radice or tempfile.gettempdir()
    _casa = os.path.abspath(casa or _CASA)
    fuori = []
    try:
        voci = sorted(os.listdir(T))
    except OSError:
        return fuori
    for v in voci:
        if not v.startswith(tuple(prefissi)):
            continue
        p = os.path.join(T, v)
        if not os.path.isdir(p):
            continue
        # ### ⛔ **LA CARTELLA IN CUI STO GIRANDO NON E- UN RESIDUO: E- LA CASA.**
        # ### ⚠ **Trovato dalla verifica su clone pulito del 2026-10-10**, e il
        # ### braccio ha fatto esattamente il suo mestiere: `csv/_verifica_clone.py`
        # ### clona in `clone_verifica_*` e ### **ci fa girare la suite**, quindi il
        # ### collaudo della pulizia ### **vedeva il clone VIVO e lo chiamava residuo.**
        # ### ✅ **Un residuo e- cio- che NESSUNO sta usando**, e <<nessuno>> si
        # ### misura: ### **la cartella che CONTIENE questo file non si conta.**
        if _casa == p or _casa.startswith(p + os.sep):
            continue
        n = b = 0
        for qui, _s, nomi in os.walk(p):
            for x in nomi:
                try:
                    b += os.path.getsize(os.path.join(qui, x))
                except OSError:
                    continue
                n += 1
        fuori.append((p, n, b))
    return fuori


def via_residui(prefissi=NOSTRI, radice=None, casa=None):
    """### Cancella i residui NOSTRI. ### `(quante, byte)`, e ### **ALZA al primo che resta.**"""
    r = residui(prefissi, radice, casa)
    byte = sum(b for _p, _n, b in r)
    for p, _n, _b in r:
        via(p)
    return len(r), byte


# =====================================================================================
#   IL COLLAUDO -- nei DUE versi
# -------------------------------------------------------------------------------------
#   ### ⛔ **Il verso che DEVE fallire e- il cuore:** senza di lui <<la pulizia e-
#   ### andata>> potrebbe voler dire ### **<<non c-era niente da cancellare>>**, che e-
#   ### ### **la stessa cosa che diceva `ignore_errors=True`.**
# =====================================================================================
def _albero(con_sola_lettura=True):
    """Una cartella finta ### **come quelle di `git`**: file in SOLA LETTURA dentro."""
    d = tempfile.mkdtemp(prefix="st_pulizia_")
    sotto = os.path.join(d, "objects", "ab")
    os.makedirs(sotto)
    for nome in ("uno", "due"):
        p = os.path.join(sotto, nome)
        io.open(p, "wb").write(b"x" * 16)
        if con_sola_lettura:
            os.chmod(p, stat.S_IREAD)
    return d


def collaudo(finge=None):
    """### `finge` serve ### **SOLO al braccio che prova la logica di piattaforma**, e il
    comando normale ### **non lo passa**: `"posix"` fa come se non fossimo su Windows."""
    nt = NT if finge is None else (finge == "nt")
    ok = [0, 0, 0]

    def esito(che, passa, nota="", solo_nt=False):
        # ### ⛔ **TRE ESITI, non due:** ### **PASSA**, ### **FALLISCE**, e
        # ### ### **NON APPLICABILE col motivo** -- che e- l-unico modo onesto di dire
        # ### ### **<<qui questo braccio non puo- avere materia>>.**
        if solo_nt and not nt:
            ok[2] += 1
            print("  %-62s %s   %s" % (che[:62], "### NON APPLICABILE",
                                       "### su questa piattaforma un file in sola lettura "
                                       "o aperto SI CANCELLA: il braccio non avrebbe "
                                       "MATERIA"))
            return
        ok[1] += 1
        ok[0] += 1 if passa else 0
        print("  %-62s %s   %s" % (che, "PASSA" if passa else "### FALLISCE", nota))

    print("=" * 100)
    print("IL COLLAUDO DELLA PULIZIA -- nei DUE VERSI")
    print("=" * 100)

    # ------------------------------------------------- materia
    d = _albero()
    sola = []
    for qui, _s, nomi in os.walk(d):
        for x in nomi:
            p = os.path.join(qui, x)
            if not os.access(p, os.W_OK):
                sola.append(p)
    esito("### il collaudo ha MATERIA: ci sono file in SOLA LETTURA", len(sola) >= 2,
          "### %d file: senza di questi il caso sano non proverebbe niente" % len(sola))

    # ------------------------------------------------- il controllo che SPIEGA il difetto
    shutil.rmtree(d, ignore_errors=True)
    resta = os.path.exists(d)
    esito("### il CONTROLLO: `ignore_errors=True` NON cancella e NON LO DICE", resta,
          "### e- il difetto del 2026-10-10: 24 cartelle lasciate, e nessun errore",
          solo_nt=True)

    # ------------------------------------------------- il caso sano
    buono = False
    try:
        via(d)
        buono = not os.path.exists(d)
    except Exception as e:
        print("     %s" % e)
    esito("il caso SANO: `via()` cancella ANCHE la sola lettura", buono,
          "### toglie il flag e riprova, e poi CONTROLLA che non ci sia piu-")

    # ------------------------------------------------- il verso che DEVE fallire
    d2 = _albero(con_sola_lettura=False)
    tenuto = os.path.join(d2, "objects", "ab", "uno")
    f = io.open(tenuto, "rb")
    alzata = ""
    try:
        via(d2)
    except Exception as e:
        alzata = type(e).__name__
    f.close()
    esito("### DEVE ALZARE: un file APERTO non si puo- cancellare", bool(alzata),
          "### ha alzato `%s`: un fallimento della pulizia e- un ERRORE VISIBILE"
          % (alzata or "NIENTE"), solo_nt=True)
    # ### ✅ **E dopo aver chiuso il file la stessa chiamata riesce**, cosi- il braccio
    # ### di sopra ### **non ha fallito per un altro motivo.**
    rifatto = False
    try:
        via(d2)
        rifatto = not os.path.exists(d2)
    except Exception as e:
        print("     %s" % e)
    esito("### e CHIUSO il file la STESSA chiamata riesce", rifatto,
          "### quindi il braccio di sopra e- fallito per il FILE APERTO, non per altro",
          solo_nt=True)

    # ------------------------------------------------- la CASA non e- un residuo
    # ### ⛔ **IL BRACCIO CHE LA VERIFICA SU CLONE PULITO HA FATTO NASCERE**
    # ### *(2026-10-10)*: `csv/_verifica_clone.py` clona in `clone_verifica_*` e ### **ci
    # ### fa girare la suite**, quindi questo collaudo ### **vedeva il clone VIVO e lo
    # ### chiamava residuo.** ### ✅ **Si prova nei DUE VERSI, con due cartelle
    # ### SORELLE**: una e- la casa, l-altra no.
    _t = tempfile.mkdtemp(prefix="st_casa_")
    _viva = os.path.join(_t, "clone_verifica_viva")
    _morta = os.path.join(_t, "clone_verifica_morta")
    for _d in (_viva, _morta):
        os.makedirs(os.path.join(_d, "csv"))
        io.open(os.path.join(_d, "csv", "_pulizia.py"), "wb").write(b"x")
    _finta = os.path.join(_viva, "csv", "_pulizia.py")
    _vedo = [x[0] for x in residui(prefissi=("clone_verifica_",), radice=_t,
                                   casa=_finta)]
    esito("### la cartella in cui STO GIRANDO non e- un residuo", _viva not in _vedo,
          "### la casa non si conta: e- VIVA, e un residuo e- cio- che nessuno usa")
    esito("### ma la SORELLA, che nessuno usa, SI- CHE E- un residuo", _morta in _vedo,
          "### altrimenti la cura avrebbe spento il controllo invece di correggerlo")
    via(_t)

    # ------------------------------------------------- la LOGICA DI PIATTAFORMA
    # ### ⛔ **E LA LOGICA DI PIATTAFORMA SI PROVA, non si promette** *(punto 6 del
    # ### mandato del `v2`)*: si rigira QUESTO collaudo ### **fingendo posix**, in un
    # ### processo a parte, e si controlla che ### **dichiari esattamente 3 non
    # ### applicabili** e che ### **esca comunque a ZERO.**
    # ### ⚠ **Solo su Windows**, perche- su posix sarebbe ### **lo stesso giro due
    # ### volte** -- e un braccio che si confronta con se stesso non prova niente.
    _cod, _nonapp = -1, -1
    if nt and finge is None:
        _r = subprocess.run([sys.executable, os.path.abspath(__file__), "--collaudo",
                             "--finge-posix"], capture_output=True, text=True,
                            encoding="utf-8", errors="replace")
        _cod = _r.returncode
        for _riga in (_r.stdout or "").split(NL):
            if _riga.startswith("NON APPLICABILI:"):
                _nonapp = int(_riga.split(":")[1].split()[0])
    esito("### la LOGICA DI PIATTAFORMA, provata FINGENDO posix",
          _cod == 0 and _nonapp == 4,
          "### fingendo posix: codice %d e %d non applicabili (attesi 0 e 4: i TRE bracci "
          "che vogliono Windows, piu- QUESTO braccio, che la- non puo- girare)"
          % (_cod, _nonapp), solo_nt=True)

    # ------------------------------------------------- niente residui nostri
    r = residui()
    esito("### e il collaudo NON LASCIA RESIDUI dei nostri prefissi", not r,
          "### %d residui: %s" % (len(r), [x[0] for x in r[:3]]))

    print("=" * 100)
    print("IL COLLAUDO DELLA PULIZIA: %d su %d   ### %s"
          % (ok[0], ok[1], "TUTTI PASSATI" if ok[0] == ok[1] else "CI SONO BUCHI"))
    # ### ⛔ **E I NON APPLICABILI SI STAMPANO SEMPRE, anche quando sono ZERO:** cosi-
    # ### ### **non si scopre su un-altra piattaforma che mezzo collaudo non girava.**
    print("NON APPLICABILI: %d   ### piattaforma `%s`%s"
          % (ok[2], (os.name if finge is None else "%s (FINTA: la vera e- %s)"
                     % (finge, os.name)),
             "   (su Windows girano tutti)" if nt else
             "   ### su questa piattaforma un file in sola lettura o aperto SI CANCELLA, "
             "quindi i bracci che provano il contrario NON AVREBBERO MATERIA"))
    print("=" * 100)
    return 0 if ok[0] == ok[1] else 1


if __name__ == "__main__":
    sys.path.insert(0, _QUI)
    import _presidio
    _presidio.avvia(__file__)
    if "--collaudo" in sys.argv:
        sys.exit(collaudo(finge="posix" if "--finge-posix" in sys.argv else None))
    if "--residui" in sys.argv:
        for p, n, b in residui():
            print("  %s   %d file   %d byte" % (p, n, b))
        print("  ### %d residui dei nostri prefissi" % len(residui()))
        sys.exit(0)
    if "--pulisci" in sys.argv:
        q, b = via_residui()
        print("  ### cancellate %d cartelle, %d byte" % (q, b))
        sys.exit(0)
    print("  python csv/_pulizia.py --collaudo | --residui | --pulisci")
    sys.exit(1)
