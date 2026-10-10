# -*- coding: utf-8 -*-
"""PUNTO `1` DELLA TERZA PARTE — **IL DETERMINISMO: RNG, THREAD, VERSIONI.**

> ### ⛔ **Il mandato, alla lettera:** *«**DETERMINISMO:** nessun RNG globale *(solo
> `Generator` con seme esplicito, e **l'AST lo verifica**)*; calcolo numerico **a UN
> thread** nei collaudi e nei sigilli *(variabili BLAS fissate **e timbrate**)*; versioni
> **bloccate in un file di blocco**, verificato all'avvio. Collaudo: stessa configurazione
> in **due processi** → uscite **byte-identiche**»*.

### ⭐ **E IL CRITERIO DEL MANDATO SI PUO' PRENDERE ALLA LETTERA, cosa che NON DAVO PER
SCONTATA.** Nel task history avevo scritto che due processi ### **non avrebbero dato file
byte-identici**, perché un `.npz` è ### **uno ZIP e un'intestazione ZIP porta la data.**
### ⛔ **ERA SBAGLIATO, e il perché è misurato: `numpy.savez` scrive `date_time =
(1980, 1, 1, 0, 0, 0)`** — ### **azzera l'ora.** ### ✅ **Quindi l'identità al byte è
STRUTTURALE, non fortuna**, e il criterio del mandato ### **vale come è scritto.**

| | che cosa | come si verifica |
|---|---|---|
| `a` | ### **nessun RNG globale** | ### **l'AST**: ogni `*.random.*` sotto `primo_ordine/` deve essere ### **`default_rng`**. ### **Misurato: `6` usi, `6` `default_rng`, `0` globali** |
| `b` | ### **un thread** | le ### **cinque variabili** si fissano a `1` e ### **vanno nel TIMBRO** |
| `c` | ### **versioni bloccate** | `primo_ordine/versioni.lock`, confrontato all'avvio |
| `d` | ### **due processi, byte-identici** | il collaudo fa girare il driver ### **due volte in due processi** e confronta ### **i byte** |

### ⛔ **E DUE COSE CHE QUESTO MODULO NON FA, dette qui e non nascoste.**

### ⚠ **`(1)` NON VERIFICA CHE LE VARIABILI BLAS ABBIANO EFFETTO.** Le librerie BLAS
leggono quelle variabili ### **quando vengono caricate**, cioè all'`import numpy`: se
`avvia()` gira ### **dopo**, le variabili sono scritte ### **e non servono a niente.**
### ✅ **`avvia()` RESTITUISCE se era in tempo** *(`"numpy" not in sys.modules`)*, e il
timbro ### **lo registra** — ma ### ⛔ **il numero di thread effettivo NON si misura,
perché `threadpoolctl` non è installato.** ### ⭐ **E la cosa che conta si misura
ALTRIMENTI: se due processi danno byte identici, i thread NON stanno rompendo il
determinismo — qualunque sia il loro numero.** ### **Quello è il controllo vero, e c'è.**

### ⚠ **`(2)` NON FERMA PER UNA VERSIONE DIVERSA, ma solo per una PIU' VECCHIA — ed è una
MIA INFERENZA, dichiarata.** Il mandato dice *«verificato all'avvio»* e ### **non dice che
cosa fare se non coincide.** ### ⛔ **Fermare su qualunque differenza romperebbe la CI**,
che installa con `>=` e gira su Linux; e ### **il repo ha GIA' MISURATO che la piattaforma
cambia i numeri assoluti** *(Linux/numpy `2.5.3` contro Windows/numpy `2.3.0`)*.
### ✅ **Quindi: FERMA se una versione è PIU' VECCHIA del blocco** *(il blocco registra ciò
che è stato verificato)*, e ### **mette la differenza NEL TIMBRO** negli altri casi —
perché ### **una corsa con versioni diverse dal blocco non è confrontabile AL BIT con una
che coincide**, e quello è il contenuto vero.
"""
import ast
import glob
import io
import json
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)

NL = chr(10)
PRESIDIO = "P-DET"

BLOCCO = os.path.join(_QUI, "versioni.lock")

# ### ⛔ **LE CINQUE VARIABILI, e sono cinque e non una**: ogni libreria numerica legge
# ### ### **la sua**, e fissarne una sola lascia le altre ### **libere di multithreadare.**
UN_THREAD = ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
             "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS")

# ### i pacchetti del blocco: ### **quelli che toccano i NUMERI**, non tutti quelli
# ### installati -- un blocco che elenca tutto ### **non si puo- tenere aggiornato.**
PACCHETTI = ("numpy", "sympy", "yaml")


# ### ⛔ **IL VERDETTO DELLA PRIMA CHIAMATA, e serve a non MENTIRE NEL TIMBRO.**
# ### `avvia()` si puo- chiamare piu- volte in un processo, e ### **la seconda volta
# ### `numpy` c-e- sempre** -- quindi <<in tempo>> calcolato la- direbbe ### **sempre
# ### FALSO**, anche quando la prima chiamata era giusta.
# ### ⚠ **L-HO VISTO SUBITO, e stava per finire nel timbro:** il driver chiama
# ### `avvia()` ### **prima di `import numpy`** e il timbro diceva
# ### ### **`in_tempo: false`.** ### **Il valore che conta e- quello della PRIMA
# ### chiamata del processo**, ed e- questo.
_PRIMO = {}


def avvia():
    """### Fissa le cinque variabili e ### **dice se era in tempo.**

    ### ⛔ **<<In tempo>> vuol dire PRIMA DELL-`import numpy`:** le BLAS leggono
    quelle variabili ### **al caricamento**, e scriverle dopo ### **non serve a niente.**
    ### ✅ **Il valore torna, e il TIMBRO lo registra: dichiarato, non nascosto.**
    ### ⚠ **E il verdetto e- quello della PRIMA chiamata del processo**, non di
    questa: vedi `_PRIMO`.
    """
    if "in_tempo" not in _PRIMO:
        _PRIMO["in_tempo"] = "numpy" not in sys.modules
        _PRIMO["erano"] = {v: os.environ.get(v) for v in UN_THREAD
                           if os.environ.get(v) is not None}
    for v in UN_THREAD:
        os.environ[v] = "1"
    return {"un_thread": {v: "1" for v in UN_THREAD},
            "in_tempo": _PRIMO["in_tempo"],
            "erano": dict(_PRIMO["erano"])}


def versioni():
    """Le versioni ### **che girano adesso**, piu- la piattaforma."""
    import platform
    fuori = {"python": sys.version.split()[0],
             "piattaforma": platform.system().lower()}
    for nome in PACCHETTI:
        try:
            m = __import__(nome)
            fuori[nome] = getattr(m, "__version__", "?")
        except Exception:                                   # noqa: BLE001
            fuori[nome] = "### NON INSTALLATO"
    return fuori


def _tupla(s):
    """`"2.3.0"` → `(2, 3, 0)`; i pezzi non numerici ### **valgono `-1`.**"""
    fuori = []
    for pezzo in str(s).split("."):
        try:
            fuori.append(int(pezzo))
        except ValueError:
            fuori.append(-1)
    return tuple(fuori)


def blocco():
    """Il contenuto di `versioni.lock`, o `{}` ### **se non c-e-.**"""
    if not os.path.exists(BLOCCO):
        return {}
    return json.loads(io.open(BLOCCO, encoding="utf-8").read())


def scarti(ora=None, bl=None):
    """### `(ferma, differenze)`: cosa non coincide col blocco.

    ### ⛔ **`ferma` e- vero SOLO per una versione PIU- VECCHIA del blocco**, e il
    perche- sta nel docstring del modulo: e- ### **una mia inferenza, dichiarata.**
    """
    ora = versioni() if ora is None else ora
    bl = blocco() if bl is None else bl
    atteso = (bl.get("versioni") or {})
    diff, ferma = [], []
    for k in sorted(atteso):
        a, b = str(atteso[k]), str(ora.get(k, "### MANCA"))
        if a == b:
            continue
        diff.append("%s: blocco `%s`, ora `%s`" % (k, a, b))
        if k in PACCHETTI and _tupla(b) < _tupla(a):
            ferma.append("`P-DET` `%s` e- PIU- VECCHIO del blocco (`%s` contro `%s`). "
                         "### Il blocco registra CIO- CHE E- STATO VERIFICATO: una "
                         "versione piu- vecchia NON lo e-" % (k, b, a))
    return ferma, diff


def verifica_versioni():
    """### **FERMA** se una versione e- piu- vecchia del blocco; restituisce il resto."""
    ferma, diff = scarti()
    assert not ferma, "### LE VERSIONI NON PASSANO:" + "".join(
        NL + "  " + x for x in ferma)
    return {"blocco": (blocco() or {}).get("versioni", {}), "ora": versioni(),
            "differenze": diff}


def usi_di_random(radice=None):
    """### `[(file, riga, attributo)]`: ### **ogni uso di `random` sotto `primo_ordine/`.**

    ### ⛔ **VIA AST, non con una regex:** `np.random.normal` in un commento
    ### **non e- un uso**, e una regex ### **non sa la differenza.**
    """
    radice = _QUI if radice is None else radice
    fuori = []
    for p in sorted(glob.glob(os.path.join(radice, "**", "*.py"), recursive=True)):
        rel = os.path.relpath(p, os.path.dirname(radice)).replace(os.sep, "/")
        try:
            a = ast.parse(io.open(p, encoding="utf-8").read())
        except SyntaxError:
            continue
        for n in ast.walk(a):
            if not isinstance(n, ast.Attribute):
                continue
            v = n.value
            if isinstance(v, ast.Attribute) and v.attr == "random":
                fuori.append((rel, n.lineno, n.attr))
            elif isinstance(v, ast.Name) and v.id == "random":
                fuori.append((rel, n.lineno, "random." + n.attr))
    return fuori


def rng_globale(radice=None):
    """### Gli errori: ### **ogni uso di `random` che NON sia `default_rng`.**"""
    err = []
    for rel, riga, attr in usi_di_random(radice):
        if attr == "default_rng":
            continue
        err.append("`P-DET` `%s:%d`: usa `%s`, che e- L-RNG GLOBALE. ### Un RNG globale "
                   "NON HA UN SEME ESPLICITO, quindi la corsa non si puo- ripetere -- e "
                   "una misura che non si ripete non e- una misura. ### Solo "
                   "`default_rng(seme)`" % (rel, riga, attr))
    return err


def controlla(radice=None):
    """Gli errori del determinismo, o `[]`."""
    err = list(rng_globale(radice))
    ferma, _diff = scarti()
    err += ferma
    if not os.path.exists(BLOCCO):
        err.append("`P-DET`: il file di blocco `primo_ordine/versioni.lock` NON ESISTE. "
                   "### Senza blocco <<verificato all-avvio>> non verifica niente")
    return err


def per_il_timbro():
    """Il pezzo di timbro del determinismo — ### **tutto cio- che si DICHIARA.**"""
    a = avvia()
    ferma, diff = scarti()
    return {"un_thread": sorted(UN_THREAD),
            "un_thread_in_tempo": a["in_tempo"],
            "versioni": versioni(),
            "versioni_blocco": (blocco() or {}).get("versioni", {}),
            "versioni_differenze": diff,
            "rng_globali": len(rng_globale())}


def scrivi_blocco():
    """### Scrive `versioni.lock` con ### **cio- che gira ADESSO.**

    ### ⚠ **Si lancia A MANO, e non da un collaudo:** un blocco che si riscrive da
    se- ### **non blocca niente** -- ### **coinciderebbe sempre.**
    """
    d = {"versioni": versioni(),
         "perche": ("le versioni VERIFICATE. Si FERMA solo per una PIU- VECCHIA: fermare "
                    "su qualunque differenza romperebbe la CI (installa con >= e gira su "
                    "Linux), e il repo ha GIA- MISURATO che la piattaforma cambia i "
                    "numeri assoluti. Le differenze vanno NEL TIMBRO."),
         "come_si_riscrive": "python primo_ordine/determinismo.py --scrivi-blocco"}
    io.open(BLOCCO, "w", encoding="utf-8", newline=NL).write(
        json.dumps(d, indent=1, sort_keys=True, ensure_ascii=False) + NL)
    return d


def main(argv):
    if "--scrivi-blocco" in argv:
        d = scrivi_blocco()
        print("  scritto %s" % BLOCCO)
        for k in sorted(d["versioni"]):
            print("     %-14s %s" % (k, d["versioni"][k]))
        return 0
    err = controlla()
    u = usi_di_random()
    print("  `P-DET`: %d usi di `random` sotto `primo_ordine/`, %d NON `default_rng`"
          % (len(u), len(rng_globale())))
    t = per_il_timbro()
    print("     un thread: %d variabili fissate, in tempo: %s"
          % (len(UN_THREAD), t["un_thread_in_tempo"]))
    print("     versioni:  %s" % ("  ".join("%s=%s" % (k, v)
                                            for k, v in sorted(t["versioni"].items()))))
    print("     differenze dal blocco: %s" % (t["versioni_differenze"] or "nessuna"))
    for x in err:
        print("  " + x)
    if err:
        print("  ### `P-DET` FALLISCE: %d errori" % len(err))
        return 1
    print("  ### `P-DET`: TUTTO A POSTO")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
