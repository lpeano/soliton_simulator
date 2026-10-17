# -*- coding: utf-8 -*-
"""`P-TAB` — **UNO STRUMENTO NON CONTIENE UNA LEGGE: LA LEGGE SI LEGGE DALLA TABELLA.**

> ### ⛔ **LA REGOLA, decisa da Luca il `2026-10-16` alle `13:25`** *(il testo integrale
> sta in `doc/CODA_2026-10-16.md`)*: uno strumento *(misura, collaudo, presidio, referto)*
> ### **NON CONTIENE una legge** -- ne' la sua formula, ne' il suo ### **`id` scritto a
> mano**, ne' il ### **nome del suo operatore**, ne' un ### **conto di leggi o di
> legami.** La legge ### **si LEGGE dalla tabella** o ### **si IMPORTA dal modulo della
> legge.** ### **Se lo strumento trova una legge che non sa misurare, ALZA.**

### ⭐⭐ **DA DOVE NASCE: UN CONTO.** In un giorno sono emersi ### **SETTE** strumenti con
la legge vecchia scritta dentro -- `h_tot` di `M-B2`, `ordine_lineare` di
`_misura_theta_n`, la sostituzione per nome di `_misura_statica_l2`, il `7` delle guardie
di `P-R1`, `deriva.satura`, `deriva.sorgente_per_nodo` e il braccio `(3)` di
`_collauda_deriva`. ### **Il motore si e' aggiornato perche' LEGGE DALLA TABELLA; le
copie no, e nessuno le obbligava.**

## ⛔ I TRE LIMITI, DICHIARATI E NON NASCOSTI

### ① **I COMMENTI SONO INVISIBILI ALL'AST, e i `docstring` SONO ESCLUSI.** Un `id` in un
commento ### **passa**: e' il perimetro di `P-RIF`, non di questo presidio. ### **E
escludere i `docstring` non e' una comodita':** la prosa che ### **spiega** perche' una
legge e' stata sostituita ### **deve poterla nominare.**

### ② **<<UN INTERO LETTERALE CONFRONTATO CON UN CONTO>> NON E' DECIDIBILE IN GENERALE.**
Quello che questo presidio fa e' ### **una regola NOMINATA**: un confronto con un
letterale `>= 2` dove ### **l'altro lato nomina la tabella** *(`ORDINE`, `LEGGI`,
`FLUSSI`, `OPERATORI`, `legami`, `guardie`, `termini`)*. ### **Un conto scritto in
un'altra forma lo evade**, e lo dico qui invece di far credere che il presidio capisca.

### ③ **LA MAPPA LEGGE -> MODULO NON E' DERIVABILE DALLA TABELLA**, perche'
`leggi.yaml` ### **non ha un campo `modulo`** *(verificato il `2026-10-16`: lo schema
dichiara `id`, `tipo`, `prova`, `scheda`, `assiomi`, `espressione`, `ambito`,
`parametri`, e per una regola `ingressi`/`uscite`/`bilancio` -- ### **nessun modulo**)*.
### ✅ **Quindi la mappa e' DICHIARATA qui sotto, e il presidio ALZA se una legge fuori
dall'ordine non ce l'ha:** ### **una legge superata nuova non puo' entrare in silenzio.**
### 📌 **La cura pulita e' un campo nella TABELLA, ed e' una proposta per Luca** -- perche'
cambia lo schema che `_genera.py` valida.
"""
import ast
import io
import os
import re
import sys
import warnings

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
sys.path.insert(0, _QUI)
import _presidio                                              # noqa: E402

NL = chr(10)
PRESIDIO = "P-TAB"

# ### ⛔ **IL PERIMETRO ATTIVO**, e le tre cartelle che ne escono: sono ### **REPERTI**
# ### *(`_archivio`, `_seal_*`, `_test_fork`)*, e un reperto ### **non si riscrive.**
# ### ⚠ **E `_test_*` ci sta:** sono le ### **infornate di prova dell-era `1`**
# ### *(`_test_53a`, `_test_fork`)*, cioe- reperti -- e una di quelle non si fa nemmeno
# ### ### **leggere da `ast`** *(`csv/_test_53a/_analisi_pilota.py`, uno `\|` in una
# ### stringa)*. ### **Riscriverla sarebbe riscrivere un reperto.**
FUORI = ("_archivio", "_seal_", "_test_")
# ### ⚠ **E QUESTO FILE ESCE, dichiarato:** nomina gli `id` nella mappa e nelle eccezioni,
# ### quindi ### **troverebbe se stesso.**
IO_STESSO = os.path.basename(__file__)

# ### ⛔ **LE PAROLE CHE DICONO <<QUESTO E' UN CONTO DELLA TABELLA>>.** ### ⚠ **Sono
# ### parole della TABELLA, non di una legge:** nessuna di queste e' un `id`.
PAROLE_TABELLA = ("ORDINE", "LEGGI", "FLUSSI", "OPERATORI", "operatori", "legami",
                  "guardie", "termini", "leggi")

# ### ⛔ **LA MAPPA LEGGE -> MODULO, DICHIARATA** *(limite `③` del titolo)*. ### **Il
# ### presidio ALZA se una legge fuori dall'ordine non e' qui**, quindi la mappa
# ### ### **non puo' restare indietro.**
MODULO_DELLA_LEGGE = {"CAMM-SATURAZIONE": "saturazione", "CAMM-FORMA-D": ""}

# ### ⛔ **LE ECCEZIONI DICHIARATE: una riga per FILE e SIMBOLO, col MOTIVO.**
# ### ⚠ **Un'eccezione ORFANA fa fallire anche lei**, cosi' una cura ### **non lascia la
# ### sua eccezione dietro.**
ECCEZIONI = {
 ("primo_ordine/motore.py", "CAMM-SATURAZIONE"):
    "IL MOTORE REGISTRA TUTTI GLI OPERATORI, anche quelli fuori dall-ordine: una riga"
    " TOLTA da `operatori` farebbe ALZARE il tick se la tabella la rimettesse"
    " nell-ordine, invece di girare",
 ("primo_ordine/motore.py", "saturazione"):
    "serve all-operatore `_saturazione`, che resta registrato",
 ("primo_ordine/tick.py", "CAMM-SATURAZIONE"):
    "`OPERATORE` registra ENTRAMBE le leggi, per lo stesso motivo del motore."
    " ### ⚠ L-ECCEZIONE SI E- SPOSTATA CON `OPERATORE` il 2026-10-16, da"
    " `deriva.py` a `tick.py`: `P-TAB` l-ha chiamata ORFANA nello stesso istante in cui"
    " il dizionario ha cambiato casa",
 ("primo_ordine/_collauda_saturazione.py", "CAMM-SATURAZIONE"):
    "e- il collaudo DELLA saturazione: la legge resta in tabella, e il suo collaudo"
    " dev-essere ancora ri-girabile",
 ("primo_ordine/_collauda_saturazione.py", "saturazione"):
    "e- il collaudo DELLA saturazione",
 ("primo_ordine/_collauda_deriva.py", "saturazione"):
    "il braccio `(1-bis)` CONFRONTA le due leggi: senza il numero della saturazione il"
    " confronto non esiste",
 ("primo_ordine/termini/camm_saturazione.py", "CAMM-SATURAZIONE"):
    "e- il LEGAME GENERATO della legge: si rigenera dalla tabella, e scriverlo a mano"
    " e- vietato",
 ("primo_ordine/_misura_mb2.py", "CAMM-SATURAZIONE"):
    "`ORDINE_VECCHIO`: un confronto STORICO dichiarato, che DEVE nominare l-ordine di"
    " allora",
 ("primo_ordine/_misura_mb2.py", "saturazione"):
    "IMPORT MORTO -- ### SCADUTO, e la cura e- il pezzo `2-septies` della coda",
 ("primo_ordine/_misura_verso_l2.py", "CAMM-SATURAZIONE"):
    "`ORDINE_VECCHIO`: un confronto STORICO dichiarato",
 ("primo_ordine/_misura_verso_l2.py", "saturazione"):
    "misura le forme della saturazione, col referto gia- committato",
 ("primo_ordine/_misura_pari_l2.py", "saturazione"):
    "misura le forme della saturazione, col referto gia- committato",
 ("primo_ordine/_misura_spettro_l1.py", "CAMM-SATURAZIONE"):
    "`ORDINE_VECCHIO` e- storico, ma `ordine_lineare` FILTRA PER NOME -- ### SCADUTO, e"
    " la cura e- il pezzo `2-quinquies` della coda",
 ("primo_ordine/bande.py", "CAMM-SATURAZIONE"):
    "`salta` spegne `N` PER NOME, e oggi non spegne niente -- ### SCADUTO, e la cura e-"
    " il pezzo `2-quinquies` della coda",
 ("primo_ordine/_collauda_tempo_proprio.py", "CAMM-SATURAZIONE"):
    "il braccio `(2)` chiede che la saturazione dipenda da `dtau` -- ### SCADUTO, e la"
    " cura e- il pezzo `2-septies` della coda",
 ("primo_ordine/_misura_forme_l2.py", "CAMM-SATURAZIONE"):
    "SOSTITUISCE l-operatore PER NOME -- ### SCADUTO, misura storica col referto gia-"
    " committato",
 ("primo_ordine/energia.py", "saturazione"):
    "IMPORT MORTO -- ### SCADUTO, e la cura e- il pezzo `2-septies` della coda",
 ("primo_ordine/termini/camm_forma_d.py", "CAMM-FORMA-D"):
    "e- il LEGAME GENERATO della legge: si rigenera dalla tabella",
 ("csv/_censimento_legge_vecchia.py", "CAMM-SATURAZIONE"):
    "e- IL CENSIMENTO DI QUELL-ID: cerca chi ne parla ancora, quindi deve nominarlo --"
    " e il suo elenco di verdetti ALZA su una coppia che non ha un verdetto",
}


# =====================================================================================
#   LA TABELLA -- e cio' che NE STA FUORI si DERIVA, non si scrive
# -------------------------------------------------------------------------------------
def fuori_dall_ordine():
    """### Gli `id` delle leggi ### **VERE** che NON stanno nell'ordine di composizione.

    ### ⭐ **SI DERIVA:** gli `id` escono da `leggi.yaml`, l'ordine da `composizione.py`, e
    le leggi ### **`prova: true`** *(finte)* ### **non contano** -- sono fuori dall'ordine
    ### **per costruzione**, e segnalarle sarebbe un falso-uno.
    """
    sys.path.insert(0, os.path.join(RADICE, "primo_ordine"))
    import composizione as CM
    dentro = set(i for i, _f, _t in CM.ORDINE)
    testo = io.open(os.path.join(RADICE, "primo_ordine", "leggi", "leggi.yaml"),
                    encoding="utf-8").read()
    fuori = []
    for blocco in re.split(r"^  - id: ", testo, flags=re.M)[1:]:
        idl = blocco.split(NL, 1)[0].strip()
        finta = re.search(r"^    prova: true", blocco, flags=re.M) is not None
        if idl not in dentro and not finta:
            fuori.append(idl)
    return fuori


# =====================================================================================
#   L'ANALIZZATORE -- **PURO, e prende le RADICI come argomento**
# -------------------------------------------------------------------------------------
# ### ⛔⛔ **PERCHE' LE RADICI SONO UN ARGOMENTO:** il collaudo dei casi che devono fallire
# ### scrive i file finti in una cartella ### **TEMPORANEA, FUORI dal repo.** ### **Due
# ### collaudi di presidio che scrivono nel repo e poi ripristinano i byte hanno lasciato
# ### l'albero sporco DUE VOLTE** *(`OSError: [Errno 22]` sul ripristino)*: cosi' quella
# ### fragilita' ### **qui non si puo' presentare.**
def _docstring(albero):
    """Gli `id` degli oggetti `Constant` che sono ### **docstring**: si escludono."""
    fuori = set()
    for n in ast.walk(albero):
        if isinstance(n, (ast.Module, ast.ClassDef, ast.FunctionDef,
                          ast.AsyncFunctionDef)):
            c = n.body[0] if n.body else None
            if (isinstance(c, ast.Expr) and isinstance(c.value, ast.Constant)
                    and isinstance(c.value.value, str)):
                fuori.add(id(c.value))
    return fuori


def _piega(n):
    """La stringa di `n` se si puo' ### **RIPIEGARE**, altrimenti `None`.

    ### ⛔ **Serve perche' una FORMA EQUIVALENTE non deve evadere:** `"CAMM-" +
    "SATURAZIONE"` e' lo stesso `id`, ed e' esattamente il buco di `P-ES1` *(che cerca la
    stringa letterale `-1j` e si fa evadere da `- 1j` con lo spazio)*.
    """
    if isinstance(n, ast.Constant):
        return n.value if isinstance(n.value, str) else None
    if isinstance(n, ast.BinOp) and isinstance(n.op, ast.Add):
        a, b = _piega(n.left), _piega(n.right)
        return None if a is None or b is None else a + b
    if isinstance(n, ast.JoinedStr):
        pezzi = [_piega(p) for p in n.values]
        return None if any(p is None for p in pezzi) else "".join(pezzi)
    if (isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
            and n.func.attr == "join" and len(n.args) == 1
            and isinstance(n.args[0], (ast.List, ast.Tuple))):
        sep = _piega(n.func.value)
        pezzi = [_piega(p) for p in n.args[0].elts]
        if sep is not None and not any(p is None for p in pezzi):
            return sep.join(pezzi)
    return None


def _nomi(n):
    """I ### **nomi** che un'espressione tocca: `Name.id` e `Attribute.attr`."""
    fuori = set()
    for x in ast.walk(n):
        if isinstance(x, ast.Name):
            fuori.add(x.id)
        elif isinstance(x, ast.Attribute):
            fuori.add(x.attr)
    return fuori


def _alza_o_raise(n):
    """`True` se nel corpo di `n` c'e' ### **almeno un `assert` o un `raise`.**"""
    return any(isinstance(x, (ast.Assert, ast.Raise)) for x in ast.walk(n))


def _file_del_perimetro(radici):
    for radice in radici:
        for cartella, _sub, file in os.walk(radice):
            rel = cartella.replace(os.sep, "/")
            if any(x in rel for x in FUORI):
                continue
            for f in sorted(file):
                if f.endswith(".py") and f != IO_STESSO:
                    yield os.path.join(cartella, f)


def analizza(radici, fuori_ordine, moduli_vecchi, base=None):
    """### I REPERTI: `(file, simbolo, specie, riga, nota)`.

    ### ⭐ **Le QUATTRO specie:** `id-fuori-ordine` · `import-legge-vecchia` ·
    `conto-letterale` · `seconda-fonte-senza-confronto`.
    """
    base = base or RADICE
    rep = []
    for percorso in _file_del_perimetro(radici):
        rel = os.path.relpath(percorso, base).replace(os.sep, "/")
        testo = io.open(percorso, encoding="utf-8").read()
        try:
            # ### ⚠ **GLI AVVISI DI `ast.parse` SI ZITTISCONO QUI, dichiarato:** un
            # ### `"\|"` in una stringa non grezza da- `SyntaxWarning`, e ce n-e- uno nel
            # ### repo *(`csv/_cerca_definizioni.py`)*. ### **Non e- il perimetro di questo
            # ### presidio**, e stamparlo a ogni corsa sarebbe rumore su cio- che conta.
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                albero = ast.parse(testo)
        except SyntaxError as e:                                  # noqa: PERF203
            rep.append((rel, "", "sorgente-illeggibile", e.lineno or 0, str(e)[:60]))
            continue
        salta = _docstring(albero)
        seconda = {}
        for n in ast.walk(albero):
            # ### ① un `id` di legge FUORI dall'ordine, in QUALUNQUE forma ripiegabile
            if isinstance(n, (ast.Constant, ast.BinOp, ast.JoinedStr, ast.Call)):
                if id(n) in salta:
                    continue
                v = _piega(n)
                if v in fuori_ordine:
                    rep.append((rel, v, "id-fuori-ordine", getattr(n, "lineno", 0),
                                "un `id` di legge fuori dall-ordine, scritto nel codice"))
            # ### ② l'import del modulo di una legge fuori dall'ordine
            if isinstance(n, ast.Import):
                for a in n.names:
                    if a.name in moduli_vecchi:
                        rep.append((rel, a.name, "import-legge-vecchia", n.lineno,
                                    "importa il modulo di una legge fuori dall-ordine"))
            if isinstance(n, ast.ImportFrom) and n.module in moduli_vecchi:
                rep.append((rel, n.module, "import-legge-vecchia", n.lineno,
                            "importa il modulo di una legge fuori dall-ordine"))
            # ### ③ un intero letterale confrontato con un conto DELLA TABELLA
            if isinstance(n, ast.Compare) and len(n.comparators) == 1:
                lati = (n.left, n.comparators[0])
                for a, b in (lati, lati[::-1]):
                    if (isinstance(a, ast.Constant) and isinstance(a.value, int)
                            and not isinstance(a.value, bool) and a.value >= 2
                            and _nomi(b) & set(PAROLE_TABELLA)):
                        rep.append((rel, "conto:%d" % a.value, "conto-letterale",
                                    n.lineno, "un conto della tabella scritto a mano"))
                        break
            # ### ④ la SECONDA FONTE dichiarata
            if isinstance(n, ast.Assign):
                for t in n.targets:
                    if isinstance(t, ast.Name) and t.id == "SECONDA_FONTE":
                        v = n.value
                        if isinstance(v, ast.Dict):
                            for k in v.keys:
                                k = _piega(k)
                                if k:
                                    seconda[k] = n.lineno
        for n in ast.walk(albero):
            if (isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
                    and n.name in seconda and not _alza_o_raise(n)):
                rep.append((rel, n.name, "seconda-fonte-senza-confronto", n.lineno,
                            "dichiarata SECONDA FONTE e NON confronta: e- una COPIA"))
    return rep


def orfane(rep, eccezioni):
    """Le eccezioni ### **che non corrispondono a nessun reperto.**"""
    visti = set((f, s) for f, s, _sp, _r, _n in rep)
    return sorted(k for k in eccezioni if k not in visti)


# =====================================================================================
#   IL PRESIDIO -- e il COLLAUDO, che scrive **FUORI DAL REPO**
# -------------------------------------------------------------------------------------
def radici_del_repo():
    return [os.path.join(RADICE, "primo_ordine"), os.path.join(RADICE, "csv")]


def moduli_vecchi(fuori):
    """I moduli delle leggi fuori dall'ordine, dalla mappa ### **DICHIARATA**.

    ### ⛔ **E ALZA se una legge fuori dall'ordine non e' nella mappa:** e' il presidio
    della mappa stessa, e senza di lui ### **una legge superata nuova entrerebbe in
    silenzio** -- che e' esattamente la malattia che questo file cura.
    """
    manca = [i for i in fuori if i not in MODULO_DELLA_LEGGE]
    assert not manca, (
        "`%s`: le leggi %r sono FUORI dall-ordine e NON stanno in `MODULO_DELLA_LEGGE`."
        " ### Si dichiara il loro modulo (stringa vuota se non ne hanno uno), oppure"
        " questo presidio ALZA: una legge superata non entra in silenzio"
        % (PRESIDIO, manca))
    return set(m for i, m in MODULO_DELLA_LEGGE.items() if m and i in fuori)


def referto(rep, orf, fuori):
    T = []
    per_coppia = {}
    for f, s, sp, r, _n in rep:
        per_coppia.setdefault((f, s), [sp, []])[1].append(r)
    T.append("`%s` -- LO STRUMENTO LEGGE LA LEGGE DALLA TABELLA" % PRESIDIO)
    T.append("")
    T.append("  le leggi FUORI dall-ordine, DERIVATE dalla tabella: %s"
             % ("  ".join(sorted(fuori)) or "nessuna"))
    T.append("  i moduli di quelle leggi, DICHIARATI: %s"
             % ("  ".join(sorted(moduli_vecchi(fuori))) or "nessuno"))
    T.append("")
    T.append("  %-44s %-22s %-30s %s" % ("file", "simbolo", "specie", "righe"))
    T.append("  " + "-" * 112)
    for (f, s), (sp, righe) in sorted(per_coppia.items()):
        T.append("  %-44s %-22s %-30s %s"
                 % (f, s, sp, " ".join(str(x) for x in sorted(righe))))
    T.append("")
    T.append("  reperti %d, coppie file/simbolo %d, eccezioni dichiarate %d, ORFANE %d"
             % (len(rep), len(per_coppia), len(ECCEZIONI), len(orf)))
    nudi = [k for k in per_coppia if k not in ECCEZIONI]
    T.append("  coppie NON coperte da un-eccezione: %d%s"
             % (len(nudi), ("   " + "  ".join("%s/%s" % k for k in sorted(nudi)))
                if nudi else ""))
    return NL.join(T)


def main(argv):
    _presidio.avvia(__file__)
    fuori = set(fuori_dall_ordine())
    vecchi = moduli_vecchi(fuori)
    rep = analizza(radici_del_repo(), fuori, vecchi)
    orf = orfane(rep, ECCEZIONI)
    coppie = set((f, s) for f, s, _a, _b, _c in rep)
    nudi = sorted(k for k in coppie if k not in ECCEZIONI)
    if "--referto" in argv:
        print(referto(rep, orf, fuori))
    err = []
    for f, s in nudi:
        err.append("`%s` `%s` / `%s`: un riferimento a una legge FUORI DALL-ORDINE, e"
                   " NESSUNA eccezione dichiarata. ### La legge si LEGGE dalla tabella,"
                   " oppure il riferimento si DICHIARA col suo motivo"
                   % (PRESIDIO, f, s))
    for f, s in orf:
        err.append("`%s` `%s` / `%s`: ECCEZIONE ORFANA -- non corrisponde a nessun"
                   " reperto. ### Una cura non lascia dietro la sua eccezione"
                   % (PRESIDIO, f, s))
    print("  `%s`: %d reperti su %d coppie, %d eccezioni dichiarate"
          % (PRESIDIO, len(rep), len(coppie), len(ECCEZIONI)))
    if "--collaudo" in argv:
        return collaudo(err)
    for e in err:
        print("  " + e)
    print("  ### %d errori" % len(err))
    return 1 if err else 0


# =====================================================================================
#   IL COLLAUDO -- **i cinque casi che DEVONO fallire, in una cartella TEMPORANEA**
# -------------------------------------------------------------------------------------
# ### ⛔⛔ **PERCHE' FUORI DAL REPO:** due collaudi di presidio scrivono nel repo e poi
# ### ripristinano i byte, e ### **due volte il ripristino e' fallito**
# ### (`OSError: [Errno 22]`), lasciando l'albero sporco -- una volta con una regola di
# ### `CLAUDE.md` ### **rinominata**, una volta con ### **una legge finta in tabella.**
# ### ✅ **Qui non c'e' niente da ripristinare**, e il controllo e' `git status`.
_OK = []


def esito(che, passa, nota=""):
    _OK.append(bool(passa))
    print("  %-62s %s   %s" % (che[:62], "PASSA" if passa else "### FALLISCE", nota))


def collaudo(err_veri):
    import shutil
    import tempfile
    print("=" * 100)
    print("IL COLLAUDO DI `%s`: I CINQUE CASI CHE DEVONO FALLIRE, FUORI DAL REPO"
          % PRESIDIO)
    print("=" * 100)
    fuori_vero = set(fuori_dall_ordine())
    vecchi_vero = moduli_vecchi(fuori_vero)
    idl = sorted(fuori_vero)[0]
    meta = len(idl) // 2
    finti = {
        "a_id.py": 'X = "%s"' % idl,
        "b_concat.py": 'X = "%s" + "%s"' % (idl[:meta], idl[meta:]),
        "c_conto.py": ("import composizione as CM" + NL + "def f():" + NL
                       + "    assert len(CM.ORDINE) == 12"),
        "d_fonte.py": ('SECONDA_FONTE = {"mia": "riscrive N per controllare il motore"}'
                       + NL + "def mia(rho, lam):" + NL + "    return rho / lam"),
        "e_pulito.py": '"""Un file che non nomina niente."""' + NL + "X = 1",
    }
    base = tempfile.mkdtemp(prefix="ptab_")
    try:
        for f, testo in finti.items():
            io.open(os.path.join(base, f), "wb").write((testo + NL).encode("utf-8"))
        rep = analizza([base], fuori_vero, vecchi_vero, base=base)
        per = {}
        for f, s, sp, _r, _n in rep:
            per.setdefault(f, set()).add(sp)
        esito("### (1) DEVE fallire: un `id` fuori dall-ordine SCRITTO A MANO",
              "id-fuori-ordine" in per.get("a_id.py", ()),
              "`%s` visto in `a_id.py`" % idl)
        esito("### (2) DEVE fallire: lo stesso `id` PER CONCATENAZIONE",
              "id-fuori-ordine" in per.get("b_concat.py", ()),
              "`%s` + `%s` RIPIEGATO: una forma equivalente non evade"
              % (idl[:meta], idl[meta:]))
        esito("### (3) DEVE fallire: un CONTO LETTERALE della tabella",
              "conto-letterale" in per.get("c_conto.py", ()),
              "`len(CM.ORDINE) == 12`: il `12` e- scritto a mano")
        esito("### (4) DEVE fallire: una SECONDA FONTE che non confronta",
              "seconda-fonte-senza-confronto" in per.get("d_fonte.py", ()),
              "dichiarata e senza `assert` ne- `raise`: e- una COPIA")
        esito("### (5) DEVE fallire: un-ECCEZIONE ORFANA",
              orfane(rep, {("e_pulito.py", idl): "un motivo qualunque"})
              == [("e_pulito.py", idl)],
              "l-eccezione non corrisponde a nessun reperto")
        # ### ⭐ **IL CONTROLLO CHE POTREBBE FALLIRE: il file PULITO non da- niente.**
        esito("### (c) e il file PULITO non da- NESSUN reperto",
              "e_pulito.py" not in per,
              "altrimenti l-analizzatore vede FANTASMI, e i cinque sopra sarebbero vacui")
        for f in finti:
            if f != "e_pulito.py":
                os.remove(os.path.join(base, f))
        esito("### (c) e la cartella RIPULITA non da- nessun reperto",
              not analizza([base], fuori_vero, vecchi_vero, base=base),
              "il presidio non trova cio- che non c-e-")
    finally:
        shutil.rmtree(base, ignore_errors=True)
    # ### ⭐ **E IL REPO DI OGGI: ogni coppia o CURATA o DICHIARATA, zero orfane.**
    esito("### (r) sul repo di oggi: ogni coppia e- DICHIARATA, e zero ORFANE",
          not err_veri, "%d errori" % len(err_veri))
    for e in err_veri:
        print("    " + e)
    print("=" * 100)
    print("IL COLLAUDO DI `%s`: %d su %d   %s"
          % (PRESIDIO, sum(_OK), len(_OK),
             "### TUTTI PASSATI" if all(_OK) else "### CI SONO ROSSI"))
    print("=" * 100)
    return 0 if all(_OK) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
