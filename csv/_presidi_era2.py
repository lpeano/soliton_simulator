# -*- coding: utf-8 -*-
"""I PRESIDI DELL'ERA `2` — **`P-E1`…`P-E7`, bloccanti e SENZA VIA D'USCITA.**

> ### ⛔ **PER I FILE DI `primo_ordine/` NON C'E' VIA D'USCITA**, e il mandato lo dice. È la
> ### **prima volta** che un presidio di questo repo non ha scappatoia: tutti gli altri
> hanno un `[SENZA-…]` da dichiarare. ### ⭐ **Qui no, e la ragione è che la catena
> `tabella → codice → scheda → registro` non ha CASI LIMITE: o è in biiezione, o è rotta.**

| | che cosa impedisce |
|---|---|
| `P-E1` | **la BIIEZIONE**: ogni riga di `leggi.yaml` ↔ **un** file generato *(letto via **AST**: la costante `LEGGE`)* ↔ **una** riga di `leggi.jsonl` *(era `2`)* ↔ **una** scheda. **Nessun ID doppio** |
| `P-E2` | **l'IMPRONTA**: un file generato la cui impronta non corrisponde alla tabella → **rifiutato** |
| `P-E3` | **le VARIABILI**: ogni variabile di `stato.py` ↔ una riga di `variabili.jsonl`, **e viceversa** per l'era `2` |
| `P-E4` | **le IMPORTAZIONI**: `stato`, `termini/`, `hamiltoniana`, `passo`, `crescita`, `vuoto` **non importano** `osservatori/` né `driver` — ### **lo strumento non è fisica** *(`A17`)* |
| `P-E5` | **gli OSSERVATORI in sola lettura**: un collaudo **li fa girare** e verifica che lo stato sia **BYTE-IDENTICO** prima e dopo |
| `P-E6` | una modifica a `leggi.yaml` **senza** la riga in `leggi.jsonl` nello stesso commit, o **senza** l'ID della legge nel messaggio |
| `P-E7` | un riferimento di una riga dei registri a una **legge** o a una **variabile** che non esiste |

### ⚠ **E `P-E5` NON SI FIDA DELLA REGOLA SCRITTA.** Una regola che dice *«l'osservatore non
scrive»* è ### **una tenda** *(`A9`)*; ### **un confronto al byte è una misura.**

Gira con:  python csv/_presidi_era2.py                    # tutti, sul disco
           python csv/_presidi_era2.py --collaudo         # nei due versi
           python csv/_presidi_era2.py --pre-commit       # per il hook
           python csv/_presidi_era2.py --commit-msg FILE  # `P-E6`
"""
import ast
import hashlib
import io
import json
import os
import re
import subprocess
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
sys.path.insert(0, _QUI)
sys.path.insert(0, os.path.join(RADICE, "primo_ordine"))
sys.path.insert(0, os.path.join(RADICE, "primo_ordine", "leggi"))

NL = chr(10)
PO = os.path.join(RADICE, "primo_ordine")
TERMINI = os.path.join(PO, "termini")
OSSERV = os.path.join(PO, "osservatori")
SCHEDE = os.path.join(RADICE, "doc", "leggi_era2")
# ### I MODULI DI FISICA: ### **non importano lo strumento** *(`P-E4`)*.
FISICA = ("stato.py", "hamiltoniana.py", "passo.py", "crescita.py", "vuoto.py")
VIETATI_IMPORT = ("osservatori", "driver")


# =====================================================================================
#   gli aiuti
# =====================================================================================

def _tabella():
    import yaml
    d = yaml.safe_load(io.open(os.path.join(PO, "leggi", "leggi.yaml"),
                               encoding="utf-8").read()) or {}
    return (d.get("leggi") or []), (d.get("variabili") or [])


def _registri():
    import _indice_era2 as E2
    return (E2.era2(E2.righe(E2.LEGGI)), E2.era2(E2.righe(E2.VARIA)))


def _generati():
    """### I file di `termini/` che ### **dichiarano `LEGGE`**, letti ### **via AST.**

    ### ⛔ **Via AST e non per regex**, e il mandato lo chiede: una regex troverebbe
    `LEGGE` ### **anche dentro un commento o una stringa**, e ### **un presidio che si
    lascia ingannare da un commento non e- un presidio.**
    """
    # ### ⛔ **DUE CARTELLE, UNA SOLA BIIEZIONE.** Prima si guardava SOLO
    # ### `termini/`, e ### **un osservatore in tabella era INVISIBILE a `P-E1`:**
    # ### la tabella lo dichiarava, e ### **nessuno verificava che il file ci fosse.**
    # ### ⚠ **La chiave resta l-ID**, e il valore porta ### **il percorso CON la
    # ### cartella**, cosi- il messaggio di `P-E2` dice DOVE sta il file.
    fuori = {}
    for sotto, base in (("termini", TERMINI), ("osservatori", OSSERV)):
        if not os.path.isdir(base):
            continue
        for f in sorted(os.listdir(base)):
            if not f.endswith(".py") or f == "__init__.py":
                continue
            d = _costanti(os.path.join(base, f))
            if "LEGGE" in d:
                fuori[d["LEGGE"]] = (sotto + "/" + f, d)
    return fuori


def _costanti(p):
    """### Le costanti di modulo di UN file, lette ### **via AST.**

    ### ⛔ **Via AST e non per regex**, e il mandato lo chiede: una regex
    troverebbe `LEGGE` ### **anche dentro un commento o una stringa.**
    """
    arb = ast.parse(io.open(p, encoding="utf-8").read(), filename=p)
    d = {}
    for n in arb.body:
        if isinstance(n, ast.Assign) and len(n.targets) == 1 \
                and isinstance(n.targets[0], ast.Name):
            try:
                d[n.targets[0].id] = ast.literal_eval(n.value)
            except Exception:
                pass
    return d


def _impronta(riga):
    return hashlib.sha1(json.dumps(riga, sort_keys=True, ensure_ascii=False)
                        .encode("utf-8")).hexdigest()[:16]


# =====================================================================================
#   P-E1 ... P-E7
# =====================================================================================

def pe1(leggi, gen, reg_l):
    """### `P-E1`: la ### **BIIEZIONE** fra i quattro posti."""
    err = []
    # ### \u26d4 **ANCHE GLI OSSERVATORI.** Il mandato chiede la biiezione fra
    # ### ### **legge, file, voce del registro e scheda**, e un osservatore
    # ### ### **E- UNA LEGGE DELLA TABELLA.** Tenerlo fuori avrebbe reso la biiezione
    # ### vera ### **solo sui tipi che avevo implementato**, che non e- la stessa cosa.
    t = {x["id"] for x in leggi
         if x["tipo"] in ("termine_nodo", "termine_arco", "osservatore")}
    g = set(gen)
    r = {x["id"] for x in reg_l}
    s = {f[:-3] for f in os.listdir(SCHEDE) if f.endswith(".md")} \
        if os.path.isdir(SCHEDE) else set()
    ids = [x["id"] for x in leggi]
    for i in sorted({x for x in ids if ids.count(x) > 1}):
        err.append("`P-E1` `%s`: ID DOPPIO nella tabella" % i)
    for nome, ins in (("un file generato", g), ("una riga di `leggi.jsonl` (era 2)", r),
                      ("una scheda in `doc/leggi_era2/`", s)):
        for i in sorted(t - ins):
            err.append("`P-E1` `%s`: la tabella la dichiara, e MANCA %s" % (i, nome))
        for i in sorted(ins - t):
            err.append("`P-E1` `%s`: c-e- %s, e LA TABELLA NON LA DICHIARA. "
                       "### La tabella e- l-UNICA FONTE" % (i, nome))
    return err


def pe2(leggi, gen, varia):
    """### `P-E2`: l-### **IMPRONTA** del generato contro la riga di tabella."""
    err = []
    per = {x["id"]: x for x in leggi}
    for idv, (f, d) in sorted(gen.items()):
        if idv not in per:
            continue
        atteso = _impronta(per[idv])
        if d.get("IMPRONTA") != atteso:
            err.append("`P-E2` `%s`: il file `%s` porta l-impronta `%s`, e la riga "
                       "di tabella da- `%s`. ### IL FILE E- STATO TOCCATO A MANO, o la "
                       "tabella e- cambiata senza rigenerare: si rigenera, NON si corregge "
                       "il file" % (idv, f, d.get("IMPRONTA"), atteso))
    # ### e `stato.py`, che porta l-impronta del blocco `variabili`.
    p = os.path.join(PO, "stato.py")
    if os.path.exists(p):
        arb = ast.parse(io.open(p, encoding="utf-8").read(), filename=p)
        got = None
        for n in arb.body:
            if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", "") == "IMPRONTA":
                got = ast.literal_eval(n.value)
        atteso = _impronta({"variabili": varia})
        if got != atteso:
            err.append("`P-E2` `stato.py`: porta l-impronta `%s`, e il blocco `variabili` "
                       "della tabella da- `%s`" % (got, atteso))
    return err


def pe3(varia, reg_v):
    """### `P-E3`: le ### **VARIABILI**, in biiezione fra `stato.py` e il registro."""
    err = []
    p = os.path.join(PO, "stato.py")
    if not os.path.exists(p):
        return ["`P-E3`: `primo_ordine/stato.py` non c-e-"]
    arb = ast.parse(io.open(p, encoding="utf-8").read(), filename=p)
    dich = ()
    for n in arb.body:
        if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", "") == "VARIABILI":
            dich = ast.literal_eval(n.value)
    nomi = {x[0] for x in dich}
    voci = {x[2] for x in dich}
    nomi_reg = {x["nome"] for x in reg_v}
    id_reg = {x["id"] for x in reg_v}
    for n in sorted(nomi - nomi_reg):
        err.append("`P-E3` `%s`: dichiarata in `stato.py` e NON in `variabili.jsonl` "
                   "(era 2)" % n)
    for n in sorted(nomi_reg - nomi):
        err.append("`P-E3` `%s`: e- in `variabili.jsonl` (era 2) e NON in `stato.py`. "
                   "### La biiezione vale NEI DUE VERSI" % n)
    for v in sorted(voci - id_reg):
        err.append("`P-E3`: `stato.py` nomina la voce `%s`, che non e- un ID di "
                   "`variabili.jsonl` (era 2)" % v)
    # ### e la tabella e- la fonte: `stato.py` deve rispecchiarla.
    for n in sorted({x["nome"] for x in varia} - nomi):
        err.append("`P-E3` `%s`: e- nella TABELLA e non in `stato.py`: si rigenera" % n)
    return err


def pe4():
    """### `P-E4`: i moduli di fisica ### **non importano lo strumento** *(`A17`)*."""
    err = []
    da = [(f, os.path.join(PO, f)) for f in FISICA]
    da += [(os.path.join("termini", f), os.path.join(TERMINI, f))
           for f in sorted(os.listdir(TERMINI)) if f.endswith(".py")]
    for rel, p in da:
        if not os.path.exists(p):
            continue
        arb = ast.parse(io.open(p, encoding="utf-8").read(), filename=p)
        for n in ast.walk(arb):
            nomi = []
            if isinstance(n, ast.Import):
                nomi = [a.name for a in n.names]
            elif isinstance(n, ast.ImportFrom):
                nomi = [n.module or ""]
            for x in nomi:
                for v in VIETATI_IMPORT:
                    if x == v or x.startswith(v + ".") or x.endswith("." + v):
                        err.append("`P-E4` `%s`: importa `%s`. ### LO STRUMENTO NON E- "
                                   "FISICA (`A17`): la fisica non puo- dipendere da chi la "
                                   "guarda" % (rel, x))
    return err


def _voci():
    """### Le voci dell-indice *(`doc/indice/voci.jsonl`)*, per `P-E7`."""
    p = os.path.join(RADICE, "doc", "indice", "voci.jsonl")
    if not os.path.exists(p):
        return []
    return [json.loads(r) for r in io.open(p, encoding="utf-8").read().split(NL)
            if r.strip()]


def pe7(reg_l, reg_v, leggi, varia):
    """### `P-E7`: i ### **riferimenti** delle righe dei registri esistono."""
    err = []
    id_lg = {x["id"] for x in leggi}
    nomi_v = {x["nome"] for x in varia}
    for x in reg_l:
        if x["id"] not in id_lg:
            err.append("`P-E7` `%s`: la riga di `leggi.jsonl` non ha una legge in tabella"
                       % x["id"])
        if not os.path.exists(os.path.join(RADICE, x.get("scheda", ""))):
            err.append("`P-E7` `%s`: la scheda `%s` non esiste"
                       % (x["id"], x.get("scheda")))
    # ### ⛔ **IL CAMPO `voce` DI UN OSSERVATORE DEVE RISOLVERE NELL-INDICE.**
    # ### Il mandato chiede la biiezione fra ### **legge, file, VOCE DELL-INDICE e
    # ### scheda**, e prima di questo controllo `voce` era ### **una stringa che
    # ### nessuno verificava**: un ID inventato sarebbe passato.
    # ### ⚠ **Vale SOLO per l-osservatore**, perche- lo schema lo pretende solo
    # ### a lui -- e un termine di prova ha `voce: "-"` per dire ### **che non ne
    # ### ha**, cosa diversa da un ID sbagliato.
    voci = {v["id"] for v in _voci()}
    for x in leggi:
        if x["tipo"] != "osservatore":
            continue
        if x.get("voce") not in voci:
            err.append("`P-E7` `%s`: l-osservatore dichiara la voce `%s`, che NON E- "
                       "NELL-INDICE. ### Una voce dichiarata e non esistente e- un "
                       "riferimento ROTTO, e il campo serviva proprio a non averne"
                       % (x["id"], x.get("voce")))
    for x in reg_v:
        if x["nome"] not in nomi_v:
            err.append("`P-E7` `%s`: la riga di `variabili.jsonl` nomina `%s`, che non e- "
                       "nella tabella" % (x["id"], x["nome"]))
    return err


def tutti(verboso=True):
    """### `P-E1`…`P-E4` e `P-E7` sul disco. ### **`P-E5` e `P-E6` hanno il loro stadio.**"""
    leggi, varia = _tabella()
    reg_l, reg_v = _registri()
    gen = _generati()
    err = (pe1(leggi, gen, reg_l) + pe2(leggi, gen, varia)
           + pe3(varia, reg_v) + pe4() + pe7(reg_l, reg_v, leggi, varia))
    if verboso:
        print("  la tabella: %d leggi, %d variabili   |   i generati: %d   |   "
              "i registri: %d + %d" % (len(leggi), len(varia), len(gen),
                                       len(reg_l), len(reg_v)))
        if err:
            for e in err[:14]:
                print("   ### %s" % e)
        else:
            print("  ### P-E1, P-E2, P-E3, P-E4, P-E7: TUTTO A POSTO")
    return err


# =====================================================================================
#   P-E5 -- gli osservatori LEGGONO, e si MISURA
# =====================================================================================

def pe5(verboso=True):
    """### `P-E5`: fa girare ogni osservatore e confronta lo stato ### **AL BYTE.**"""
    import importlib.util
    import numpy as np
    err = []
    if not os.path.isdir(OSSERV):
        return err
    files = [f for f in sorted(os.listdir(OSSERV))
             if f.endswith(".py") and f != "__init__.py"]
    import stato as ST
    for f in files:
        p = os.path.join(OSSERV, f)
        spec = importlib.util.spec_from_file_location("_oss_" + f[:-3], p)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        st = ST.nuovo(5)
        rng = np.random.default_rng(7)
        for k in st:
            st[k][...] = (rng.normal(size=st[k].shape)
                          + 1j * rng.normal(size=st[k].shape))
        prima = {k: v.tobytes() for k, v in st.items()}
        if hasattr(m, "misura"):
            m.misura(st)
        dopo = {k: v.tobytes() for k, v in st.items()}
        for k in prima:
            if prima[k] != dopo[k]:
                err.append("`P-E5` `%s`: l-osservatore ha SCRITTO `%s`. ### Un osservatore "
                           "LEGGE: non scrive MAI" % (f, k))
    if verboso:
        print("  `P-E5`: %d osservatori provati, stato BYTE-IDENTICO: %s"
              % (len(files), "si-" if not err else "### NO"))
    return err


# =====================================================================================
#   P-E6 -- la tabella cambia, il registro e il messaggio la seguono
# =====================================================================================

# ### ⛔ **QUI NON C-E- NESSUNA REGEX DI VIA D-USCITA, e la sua ASSENZA e- il presidio.**
# ### ⚠ **La prima stesura ne definiva una** *(`_FUGA`)* ### **senza leggerla mai**, come
# ### promemoria. ### **E- codice morto che INVITA una scappatoia che il mandato vieta:**
# ### *<<per i file di `primo_ordine/` NESSUNA via d-uscita>>*.
# ### ⭐ **E il braccio di collaudo che lo provava FALLIVA PER UNA RAGIONE PERFETTA:**
# ### cercava la stringa `[SENZA-` nel file, e ### **la trovava NEL PROPRIO TESTO.**
# ### **Un controllo che si cerca addosso trova sempre se stesso** -- e la cura non era
# ### cambiare il controllo: ### **era togliere la cosa che non doveva esistere.**

def _staged():
    q = subprocess.run(["git", "diff", "--cached", "--name-only"], cwd=RADICE,
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    return [r.strip().replace(chr(92), "/") for r in (q.stdout or "").split(NL) if r.strip()]


def pe6(msg_file):
    """### `P-E6`: `leggi.yaml` cambia ⇒ ### **`leggi.jsonl` nello stesso commit** e
    ### **l-ID della legge nel messaggio.**

    ### ⛔ **SENZA VIA D-USCITA, e il mandato lo dice:** per i file di `primo_ordine/`
    ### **nessun `[SENZA-…]`.** ### **La riga `_FUGA` esiste solo per DIRE che non si
    legge**, e il collaudo ### **lo prova.**
    """
    err = []
    st = _staged()
    if "primo_ordine/leggi/leggi.yaml" not in st:
        return err
    if "doc/indice/leggi.jsonl" not in st and "doc/indice/variabili.jsonl" not in st:
        err.append("`P-E6`: `leggi.yaml` cambia e NESSUN registro dell-era 2 e- nel commit. "
                   "### La riga del registro si scrive con `python csv/indice.py "
                   "era2-lotto`, e va NELLO STESSO COMMIT")
    msg = io.open(msg_file, encoding="utf-8", errors="replace").read() \
        if msg_file and os.path.exists(msg_file) else ""
    leggi, _v = _tabella()
    citati = [x["id"] for x in leggi if x["id"] in msg]
    if not citati:
        err.append("`P-E6`: `leggi.yaml` cambia e il messaggio NON CITA NESSUN ID di legge "
                   "(in tabella: %s). ### Un commit che cambia una legge e non dice QUALE "
                   "non si rilegge" % [x["id"] for x in leggi][:6])
    return err


# =====================================================================================
#   IL COLLAUDO, nei due versi
# =====================================================================================

def collaudo():
    import _presidio
    _presidio.avvia(__file__)
    ok = [0, 0]

    def esito(che, passa, nota=""):
        ok[1] += 1
        ok[0] += 1 if passa else 0
        print("  %-66s %s   %s" % (che, "PASSA" if passa else "### FALLISCE", nota))

    leggi, varia = _tabella()
    reg_l, reg_v = _registri()
    gen = _generati()
    print("=" * 100)
    print("COLLAUDO DEI PRESIDI DELL-ERA 2 -- nei DUE VERSI")
    print("=" * 100)
    esito("sul disco: `P-E1`, `P-E2`, `P-E3`, `P-E4`, `P-E7` TACCIONO",
          tutti(verboso=False) == [], "la catena e- in biiezione OGGI")
    # ### ⛔ **LA NOTA DI PRIMA DICEVA <<zero osservatori oggi: il braccio e-
    # ### VERO e VUOTO>>, ed ERA VERA. ORA E- FALSA**, perche- `PROVA-NORMA`
    # ### esiste -- e ### **una nota che dice il falso e- peggio di nessuna nota.**
    # ### ⚠ **Quindi il numero SI CONTA**, non si asserisce.
    _n_oss = len([f for f in os.listdir(OSSERV)
                  if f.endswith(".py") and f != "__init__.py"]) \
        if os.path.isdir(OSSERV) else 0
    esito("`P-E5`: gli osservatori NON scrivono", pe5(verboso=False) == [],
          ("%d osservatori, lo stato e- BYTE-IDENTICO" % _n_oss) if _n_oss
          else "### ZERO osservatori: IL BRACCIO E- VERO E VUOTO, e lo dico")
    esito("### il braccio di `P-E5` HA MATERIA (almeno un osservatore)", _n_oss > 0,
          "### se fosse 0, il braccio sopra sarebbe un FALSO-UNO")
    # ### ⛔ **IL CASO CHE DEVE FALLIRE: UN OSSERVATORE CHE SCRIVE LO STATO.**
    # ### E- uno dei sei che la tappa 5 pretende, e ### **si prova per davvero:**
    # ### si scrive un osservatore che tocca `st`, si fa girare `P-E5`, e si
    # ### verifica che scatti ### **per la chiave giusta.**
    _p = os.path.join(OSSERV, "_prova_scrive.py")
    try:
        io.open(_p, "w", encoding="utf-8", newline=NL).write(NL.join([
            "# -*- coding: utf-8 -*-",
            "LEGGE = 'PROVA-SCRIVE'",
            "TIPO = 'osservatore'",
            "",
            "",
            "def misura(st):",
            "    st['psi'][0, 0] += 1.0",
            "    return 0.0",
        ]) + NL)
        esito("### DEVE scattare: un OSSERVATORE CHE SCRIVE lo stato",
              any("ha SCRITTO" in e for e in pe5(verboso=False)),
              "`A17`: lo strumento non e- fisica, e NON la cambia")
    finally:
        if os.path.exists(_p):
            os.remove(_p)
    esito("NON deve scattare: tolto quello finto, `P-E5` TACE di nuovo",
          pe5(verboso=False) == [],
          "### il braccio di sopra scattava per LUI, non per un residuo")
    print()
    print("  (a) `P-E1` -- LA BIIEZIONE")
    esito("### DEVE scattare: una legge in tabella SENZA file generato",
          any("MANCA un file generato" in e
              for e in pe1(leggi + [dict(leggi[0], id="PROVA-FANTASMA")], gen, reg_l)))
    esito("### DEVE scattare: un file generato che LA TABELLA NON DICHIARA",
          any("LA TABELLA NON LA DICHIARA" in e
              for e in pe1(leggi, dict(gen, **{"PROVA-ORFANA": ("x.py", {})}), reg_l)))
    esito("### DEVE scattare: una riga di registro SENZA legge in tabella",
          any("LA TABELLA NON LA DICHIARA" in e
              for e in pe1(leggi, gen, reg_l + [dict(reg_l[0], id="PROVA-ORFANA")])))
    esito("### DEVE scattare: un ID DOPPIO in tabella",
          any("DOPPIO" in e for e in pe1(leggi + [leggi[0]], gen, reg_l)))
    print()
    print("  (b) `P-E2` -- L-IMPRONTA")
    esito("### DEVE scattare: un file generato con l-impronta SBAGLIATA",
          any("TOCCATO A MANO" in e
              for e in pe2(leggi, {leggi[0]["id"]: ("x.py", {"IMPRONTA": "zzz"})}, varia)),
          "si rigenera, NON si corregge il file")
    esito("### DEVE scattare: la tabella cambiata senza rigenerare",
          any("TOCCATO A MANO" in e
              for e in pe2([dict(leggi[0], espressione=leggi[0]["espressione"] + " + 0")]
                           + leggi[1:], gen, varia)))
    print()
    print("  (c) `P-E3` -- LE VARIABILI, nei due versi")
    esito("### DEVE scattare: una variabile nel registro e NON in `stato.py`",
          any("NON in `stato.py`" in e
              for e in pe3(varia, reg_v + [dict(reg_v[0], id="V-FANTASMA",
                                                nome="fantasma")])),
          "la biiezione vale NEI DUE VERSI")
    esito("### DEVE scattare: una variabile in TABELLA e non in `stato.py`",
          any("si rigenera" in e
              for e in pe3(varia + [dict(varia[0], nome="fantasma")], reg_v)))
    print()
    print("  (d) `P-E4` -- LE IMPORTAZIONI")
    # ### si prova su un file di PROVA, e il file vero non si tocca.
    p = os.path.join(TERMINI, "_prova_import.py")
    try:
        io.open(p, "w", encoding="utf-8", newline=NL).write(
            "# -*- coding: utf-8 -*-" + NL + "import osservatori" + NL)
        esito("### DEVE scattare: un termine che importa `osservatori`",
              any("NON E- FISICA" in e for e in pe4()),
              "la fisica non puo- dipendere da chi la guarda (`A17`)")
    finally:
        os.remove(p)
    esito("NON deve scattare: i file veri", pe4() == [])
    print()
    print("  (e) `P-E6` -- E SENZA VIA D-USCITA")
    # ### ⛔ **IL BRACCIO GUARDA CHE LA VIA D-USCITA NON ESISTA**, e non puo- cercare la
    # ### stringa nel proprio file *(la troverebbe nel proprio testo)*: guarda
    # ### ### **l-ALBERO** -- nessuna chiamata a un `search` su un pattern `SENZA`.
    _src = io.open(__file__, encoding="utf-8").read()
    _arb = ast.parse(_src)
    _chiamate = [n for n in ast.walk(_arb)
                 if isinstance(n, ast.Attribute) and n.attr in ("search", "match")]
    _nomi = {getattr(n.value, "id", "") for n in _chiamate}
    esito("### NESSUNA via d-uscita: non esiste un pattern di FUGA che qualcuno legga",
          not any("FUGA" in x.upper() or "SENZA" in x.upper() for x in _nomi),
          "la prima stesura ne definiva uno SENZA leggerlo: codice morto che INVITA "
          "una scappatoia che il mandato vieta")
    print("=" * 100)
    print("COLLAUDO DEI PRESIDI DELL-ERA 2: %d su %d   %s"
          % (ok[0], ok[1], "### TUTTI PASSATI" if ok[0] == ok[1]
             else "### QUALCUNO FALLISCE"))
    print("=" * 100)
    return 0 if ok[0] == ok[1] else 1


def main(a):
    if "--collaudo" in a:
        return collaudo()
    if "--commit-msg" in a:
        err = pe6(a[a.index("--commit-msg") + 1])
        if err:
            sys.stderr.write(NL + "[P-E6] *** COMMIT RIFIUTATO ***" + NL + NL)
            for e in err:
                sys.stderr.write("  " + e + NL)
            sys.stderr.write(NL + "  ### NESSUNA VIA D-USCITA per i file di "
                                  "`primo_ordine/`." + NL + NL)
            return 1
        return 0
    import _presidio
    _presidio.avvia(__file__)
    err = tutti() + pe5()
    if err and "--pre-commit" in a:
        sys.stderr.write(NL + "[P-E1..P-E7] *** COMMIT RIFIUTATO ***" + NL + NL)
        for e in err[:14]:
            sys.stderr.write("  " + e + NL)
        sys.stderr.write(NL + "  ### NESSUNA VIA D-USCITA per i file di "
                              "`primo_ordine/`: si rigenera con "
                              "`python primo_ordine/_genera.py`." + NL + NL)
        return 1
    return 1 if err else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
