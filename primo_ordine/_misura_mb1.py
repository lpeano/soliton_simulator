# -*- coding: utf-8 -*-
r"""`M-B1` — **IL RACCORDO AL BIT, PEZZO PER PEZZO, contro `717bb60`.**

> **Criterio RIFORMULATO da Luca il 2026-10-15** *(12:43)*: *«a `theta = pi` **OGNI PEZZO**
> coincide **AL BIT** con l'operatore di `717bb60` (involuzioni). Il passo intero palindromo
> **NON** si confronta al bit col passo di `717bb60`: riporta la loro distanza su 250 tick
> **come informazione, non come criterio**.»*

## ⛔ PERCHE' E' STATO RIFORMULATO — **un mio errore, e vale scriverlo qui**

### **La prima versione pretendeva il PASSO INTERO al bit.** ### ⚠ **E quella, insieme a
`M-B2`, era impossibile:** `M-B2` chiede una composizione **di secondo ordine**, cioe'
**palindroma**, e un passo palindromo **non e'** il passo di `717bb60` *(i pezzi non
commutano)*.
### ⛔ **I due criteri si escludevano, e io li avevo riportati dalla mappa SENZA
CONTROLLARLI** — me ne sono accorto **solo dopo averli misurati entrambi.**
### ✅ **La riformulazione e' di Luca:** il raccordo si misura **dove ha senso**, cioe'
### **sui PEZZI**, che sono le involuzioni di prima.

## ⭐ COME

### **Per ogni pezzo, UNA applicazione sola** su una scena a `dtau = 1` *(cioe'
`theta = pi`)*, e si confrontano **i BYTE GREZZI** di `psi_h` e `phi_h`.
### 📌 **E i pezzi sono TUTTI SEI**, non i quattro cambiati: ### **la moneta e la
saturazione sono il CONTROLLO** — non sono stati toccati, quindi **devono** coincidere, e se
non coincidessero vorrebbe dire che ho cambiato qualcosa che non volevo cambiare.

## ⛔⛔ IL CONFINE DI QUESTA MISURA, **misurato il `2026-10-17`**

### **IL CRITERIO SONO I PEZZI**: `un_pezzo` applica ### **UN pezzo da solo** a
`theta = pi`. ### ⚠ **Quindi un cambiamento del CAMMINO del tick** *(non dei pezzi, non
della tabella)* ### **lascia questa misura a <<12 su 12 AL BIT>> con l'IMPRONTA
IDENTICA** — l'impronta viene da `composizione.py`, cioe' ### **dalla TABELLA**, non da
come il modulo del passo percorre l'ordine.
### 📌 **Lo vede SOLO la distanza del passo intero**, che qui sotto e' riportata come
### **<<informazione, NON criterio>>**.

> ### ⛔ **E DA QUI IN POI, per decisione del guardiano del `2026-10-17`:**
> ### **per `D0` e per OGNI misura che tocca il CAMMINO, la distanza del passo intero
> ### `= 0` esatto su entrambe le scene E' UN CRITERIO** — e ### **i `12` pezzi al bit
> restano richiesti IN PIU', non al posto.**
> ### ⚠⚠ **E questo NON cambia il significato della misura per i referti VECCHI:** quelli
> sono stati letti col criterio dei ### **pezzi**, e la' il passo intero era
> ### **informazione.** ### **Il criterio nuovo vale da `D0` in avanti.**

### ⛔ **E il <<prima>> si prende da un `git worktree`** del commit, non da una copia nel
file: in un albero nudo `_presidio` ### **rifiuta di girare**, e ha ragione.

## 📌 LA CONFIGURAZIONE INTERA E' NELLE COSTANTI DEL MODULO

### `DTAU`, `TICK`, `SCENE`, `NORMA`, `VUOTO_MODULO`, `SU2`: **tutte in cima e tutte
stampate**, che e' cio' che il presidio dei referti pretende.
### ⚠ **E `dtau = 1.0` NON e' un numero scelto: e' `dtau_rif`**, l'unita' del raccordo.

Gira con:  python primo_ordine/_misura_mb1.py --contro 717bb60
"""
import hashlib
import io
import os
import shutil
import subprocess
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
# ### la radice del repo, DERIVATA: la misura gira anche in un ALBERO VECCHIO, e la-
# ### ### **la radice e- quella dell-albero**, non quella di oggi.
RADICE = os.path.dirname(_QUI)
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
sys.path.insert(0, os.path.join(RADICE, "csv"))

DTAU = 1.0
TICK = 250
SCENE = ((16, 7), (12, 11))
NORMA = "locale"
VUOTO_MODULO = 2.0
SU2 = True
# ### ⛔⛔ **I PEZZI SI LEGGONO DALL-ORDINE, dal `2026-10-17`** *(punto `2` del
# ### mandato unico; la regola e- nominata nel docstring qui sotto)*. ### **Erano una
# ### LISTA A MANO di `6` id**, che ### **conteneva `CAMM-SATURAZIONE`** *(fuori
# ### dall-ordine dal `2026-10-15`)* e ### **NON conteneva `CAMM-MATERIA-VUOTO`**, cioe-
# ### ### **la legge che GIRA.**
# ### ⚠ **E il `2026-10-16` l-ho USATA COME PROVA:** <<tutti i `12` pezzi coincidono
# ### AL BIT>> per giustificare lo spostamento del passo -- e ### **quei `12` pezzi non
# ### contenevano il flusso che gira.**
# ### ✅ **E LA SATURAZIONE ESCE DA SOLA**, perche- non e- nell-ordine: ### **non la
# ### togliamo noi.** Se Luca la rimettesse nell-ordine, ### **rientrerebbe da sola.**
def pezzi_dell_ordine():
    """Gli `id` ### **DISTINTI** dell-ordine, in ordine di ### **prima apparizione.**

    ### ⛔ **E' la regola `STRUMENTO-LEGGE-DALLA-TABELLA`** *(decisione di Luca del
    `2026-10-16`)*: uno strumento ### **non contiene** l-`id` di una legge scritto a mano.

    ### ⚠ **Distinti perche- l-ordine e- PALINDROMO:** `12` voci, `6` `id`, e un pezzo
    misurato due volte ### **darebbe due volte lo stesso byte.**
    """
    import composizione as CM
    fuori = []
    for idl, _frazione, _tipo in CM.ORDINE:
        if idl not in fuori:
            fuori.append(idl)
    return tuple(fuori)


PEZZI = pezzi_dell_ordine()


def pezzi_applicabili():
    """### ⛔ **ALZA se un pezzo dell-ordine NON e- misurabile al bit.**

    ### ⭐ **Il mandato lo chiede cosi-:** *<<la misura ALZA se un pezzo dell-ordine non
    e- misurabile al bit>>*. ### **Un pezzo che non si sa applicare non si salta: FERMA**,
    perche- ### **un confronto su un sottoinsieme SILENZIOSO e- un falso-uno.**
    """
    PASSO, dove = il_passo_dell_albero()
    manca = [i for i in PEZZI if i not in PASSO.OPERATORE]
    assert not manca, (
        "`M-B1`: i pezzi %r sono NELL-ORDINE e NON sono in `OPERATORE` (letto da `%s`):"
        " la misura NON SA applicarli da soli, quindi NON PUO- confrontarli al bit."
        " ### Si aggiunge la riga, oppure la misura ALZA -- un confronto su un"
        " sottoinsieme silenzioso e- un falso-uno" % (manca, dove))
    return PEZZI

# ### ⛔ **I FILE DELLA MISURA che viaggiano nell-albero vecchio**, e nient-altro: il
# ### ### **SIMULATORE la- dentro resta QUELLO DI PRIMA.**
VIAGGIANO = ("_misura_mb1.py",)


def il_passo_dell_albero():
    """### IL PASSO SI PRENDE ### **DALL-ALBERO IN CUI LA MISURA GIRA**, non da oggi.

    ### ⛔⛔ **PERCHE- ESISTE QUESTA FUNZIONE** *(cura del `2026-10-17`, difetto
    mio del `2026-10-16`)*: `VIAGGIANO` conteneva ### **`tick.py`**, e `contro()` lo
    copiava nell-albero vecchio ### **SEMPRE** -- quindi il <<prima>> girava
    ### **col ciclo del passo di OGGI.** ### ⚠ **Era innocuo finche- lo spostamento
    era VERBATIM**, ### **ma il punto `D` cambiera- il passo**, e da allora `M-B1`
    avrebbe confrontato ### **il passo nuovo col passo nuovo: un FALSO-UNO.**

    ### ✅ **ADESSO: `import tick` trova il `tick.py` DI QUELL-ALBERO**, perche-
    `python primo_ordine/_misura_mb1.py` mette ### **`primo_ordine/` per primo** in
    `sys.path`. ### **E dove `tick.py` non c-e- ancora** *(gli alberi prima del
    `2026-10-16`)* ### **si cade su `deriva`**, che la- dentro ha `tick` e `OPERATORE`.

    ### ⚠ **IL RAMO E- DICHIARATO**, e si vede ### **in entrambi i versi**: contro
    `8c7b928` passa da `tick.py`, contro `b150003` da `deriva.py`.
    """
    try:
        import tick as TK
        return TK, "tick.py"
    except ImportError:
        # ### ⭐ **L-ALBERO DI PRIMA DELLO SPOSTAMENTO:** `percorri_tick`, `tick` e
        # ### `OPERATORE` vivevano in `deriva.py`, e la misura li prende ### **da la-.**
        import deriva as DV
        return DV, "deriva.py"


def _la_misura_non_porta_il_passo():
    """### ⛔ **LA MISURA NON DEFINISCE NESSUNA FUNZIONE DEL PASSO**, e lo si ASSERISCE.

    ### ⚠ **Serve perche- `_misura_mb1.py` VIAGGIA nell-albero vecchio:** se un giorno
    qualcuno ci scrivesse dentro un `tick` o un `percorri_tick`, ### **il passo di oggi
    tornerebbe a viaggiare** -- per un-altra porta, e in silenzio.
    """
    import ast
    DEL_PASSO = ("tick", "percorri_tick", "OPERATORE")
    src = io.open(os.path.abspath(__file__), encoding="utf-8").read()
    arb = ast.parse(src)
    dentro = []
    for n in arb.body:
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name in DEL_PASSO:
            dentro.append(n.name)
        if isinstance(n, ast.Assign):
            for t in n.targets:
                if isinstance(t, ast.Name) and t.id in DEL_PASSO:
                    dentro.append(t.id)
    assert not dentro, (
        "`M-B1` definisce %r, che sono nomi DEL PASSO: questo file VIAGGIA nell-albero"
        " vecchio, quindi il passo di oggi tornerebbe a girare la- dentro -- per un-altra"
        " porta e in silenzio. ### Il passo si PRENDE dall-albero, non si porta" % dentro)


def timbra(b):
    return hashlib.sha1(b).hexdigest()[:12]


def _byte(st):
    return (np.ascontiguousarray(st["psi_h"]).tobytes()
            + np.ascontiguousarray(st["phi_h"]).tobytes())


def un_pezzo(idl, nn, seme):
    """### I byte dopo **UNA** applicazione del pezzo `idl`, a `theta = pi`."""
    import deriva as DV
    PASSO, _dove = il_passo_dell_albero()
    nome, vuole_par = PASSO.OPERATORE[idl]
    _i, mot, st, par = DV.scena(nn, seme, DTAU, norma=NORMA,
                                vuoto_modulo=VUOTO_MODULO, su2=SU2)
    mot.apri_tick()
    mot.operatori[nome](st, par if vuole_par else {}, 1)
    mot.chiudi_tick()
    return _byte(st)


def il_passo(nn, seme):
    """### I byte dopo `TICK` tick del passo **intero**, qualunque sia l'ordine."""
    import deriva as DV
    _i, mot, st, par = DV.scena(nn, seme, DTAU, norma=NORMA,
                                vuoto_modulo=VUOTO_MODULO, su2=SU2)
    PASSO, _dove = il_passo_dell_albero()
    for _t in range(TICK):
        PASSO.tick(st, mot, par)
    return _byte(st), (st["psi_h"].copy(), st["phi_h"].copy())


def scrivi(dove):
    """### Scrive i byte di **ogni pezzo** e del **passo intero**, durante la corsa."""
    import composizione as CM
    with open(dove, "wb") as f:
        f.write(len(CM.ORDINE).to_bytes(4, "little"))
        f.write(CM.IMPRONTA.encode("ascii"))
        # ### ⛔⛔ **GLI ID VANNO NEL FILE, dal `2026-10-17`**, e il motivo e- un
        # ### secondo falso-uno che la cura di oggi ### **avrebbe APERTO:** `contro()`
        # ### confronta i blocchi ### **per POSIZIONE** e asserisce solo che i due file
        # ### hanno ### **lo stesso NUMERO di blocchi.**
        # ### ⚠ **Finche- `PEZZI` era una lista FISSA le due liste erano uguali per
        # ### costruzione; leggendole DALLA TABELLA possono differire fra i due alberi** --
        # ### e il confronto metterebbe ### **pezzi diversi credendoli uguali.**
        # ### ✅ **Percio- il primo blocco sono GLI ID**, e `contro()` li CONFRONTA.
        _ids = " ".join(PEZZI).encode("utf-8")
        f.write(len(_ids).to_bytes(8, "little"))
        f.write(_ids)
        pezzi_applicabili()
        _p, _dove = il_passo_dell_albero()
        # ### ⭐ **IL RAMO DICHIARATO SI VEDE, e non si deduce:** stampare DA DOVE
        # ### viene il passo e' l'unica prova che ### **il ramo e' esercitato in entrambi
        # ### i versi** -- `tick.py` negli alberi dopo il `2026-10-16`, `deriva.py` in
        # ### quelli di prima.
        print("  l'ordine di questo albero: %d pezzi, impronta %s;"
              " il passo viene da `%s`" % (len(CM.ORDINE), CM.IMPRONTA, _dove))
        for nn, seme in SCENE:
            for idl in PEZZI:
                b = un_pezzo(idl, nn, seme)
                f.write(len(b).to_bytes(8, "little"))
                f.write(b)
                f.flush()
                print("    nn=%-4d seme=%-4d %-24s sha1-BYTE %s"
                      % (nn, seme, idl, timbra(b)))
            b, dati = il_passo(nn, seme)
            f.write(len(b).to_bytes(8, "little"))
            f.write(b)
            np.save(dove + ".psi.%d.%d.npy" % (nn, seme), dati[0])
            np.save(dove + ".phi.%d.%d.npy" % (nn, seme), dati[1])
            f.flush()
            print("    nn=%-4d seme=%-4d %-24s sha1-BYTE %s"
                  % (nn, seme, "(il passo intero)", timbra(b)))
    return 0


def _albero_vecchio(commit, dove):
    """### Un **`git worktree`** di `commit`, ### **e NON un albero nudo.**

    ### ⛔ **UN ALBERO NUDO NON BASTA, e l-ho misurato:** `git archive` da' i file ma
    **non un repo**, e li' `_presidio` ### **RIFIUTA DI GIRARE** -- la barriera vede
    `core.hooksPath` non impostato e si ferma. ### ✅ **E ha ragione:** un misuratore che
    gira dove i presidi non esistono ### **misurerebbe senza sorveglianza.**
    """
    radice = os.path.dirname(_QUI)
    if os.path.isdir(dove):
        subprocess.run(["git", "worktree", "remove", "--force", dove], cwd=radice,
                       capture_output=True)
        if os.path.isdir(dove):
            shutil.rmtree(dove, ignore_errors=True)
    r = subprocess.run(["git", "worktree", "add", "--detach", dove, commit], cwd=radice,
                       capture_output=True)
    assert os.path.isdir(os.path.join(dove, "primo_ordine")), (
        "il worktree di %s non e' nato: %s"
        % (commit, (r.stdout + r.stderr).decode("utf-8", "replace")[-500:]))
    return dove


def _leggi(dove):
    """### `(n_pezzi, impronta, ids, [blocchi])` dal file scritto da `scrivi`.

    ### ⚠ **Il PRIMO blocco sono GLI ID** *(dal `2026-10-17`)*, e non e- un blocco di
    byte da confrontare: e- ### **la lista dei pezzi di QUELL-albero.**
    """
    b = open(dove, "rb").read()
    n = int.from_bytes(b[:4], "little")
    imp = b[4:20].decode("ascii")
    k = 20
    fuori = []
    while k < len(b):
        L = int.from_bytes(b[k:k + 8], "little")
        k += 8
        fuori.append(b[k:k + L])
        k += L
    assert fuori, "il file dei byte e- VUOTO: %s" % dove
    ids = tuple(fuori[0].decode("utf-8").split())
    return n, imp, ids, fuori[1:]


def contro(commit):
    """### Il confronto **pezzo per pezzo**, piu' la distanza del passo intero."""
    radice = os.path.dirname(_QUI)
    fuori = os.path.join(os.environ.get("TEMP", radice), "mb1")
    if not os.path.isdir(fuori):
        os.makedirs(fuori)
    vecchio = _albero_vecchio(commit, os.path.join(fuori, "albero"))
    qui, la = os.path.join(fuori, "ora.bin"), os.path.join(fuori, "prima.bin")
    print("### (1) QUESTO ALBERO:")
    scrivi(qui)
    # ### ⛔⛔ **NELL-ALBERO VECCHIO NON SI COPIA MAI CODICE DEL PASSO**
    # ### *(cura del `2026-10-17`)*. ### **Viaggia SOLO la misura**, e il passo
    # ### ### **si PRENDE dall-albero in cui la misura gira**
    # ### *(`il_passo_dell_albero`)*.
    # ### ⚠ **E prima di copiarla si ASSERISCE che la misura non PORTI il passo**: se
    # ### un giorno ci finisse dentro un `tick`, il passo di oggi tornerebbe a viaggiare
    # ### ### **per un-altra porta.**
    _la_misura_non_porta_il_passo()
    for q in VIAGGIANO:
        shutil.copyfile(os.path.join(radice, "primo_ordine", q),
                        os.path.join(vecchio, "primo_ordine", q))
    print("### (2) %s, dal worktree:" % commit[:7])
    r = subprocess.run([sys.executable, os.path.join("primo_ordine", "_misura_mb1.py"),
                        "--scrivi", la], cwd=vecchio, capture_output=True)
    sys.stdout.write(r.stdout.decode("utf-8", "replace"))
    if r.returncode:
        sys.stdout.write(r.stderr.decode("utf-8", "replace")[-3000:])
        print("### ⛔ la corsa su %s e' FALLITA" % commit[:7])
        return 1
    na, ia, ids_a, ba = _leggi(qui)
    nb, ib, ids_b, bb = _leggi(la)
    # ### ⛔⛔ **IL CONFRONTO NON PARTE SE LE DUE LISTE DI PEZZI DIFFERISCONO**
    # ### *(dal `2026-10-17`)*. ### **Confrontare pezzi diversi credendoli uguali e' PEGGIO
    # ### di non confrontare**, e i blocchi si mettono a confronto ### **per POSIZIONE.**
    assert ids_a == ids_b, (
        "`M-B1`: i PEZZI dei due alberi NON COINCIDONO, e il confronto NON PARTE."
        " ### adesso %s;  %s %s. ### I pezzi si leggono dall-ORDINE di ciascun albero:"
        " se l-ordine e- cambiato, i due lati misurerebbero COSE DIVERSE, e il confronto"
        " per posizione le crederebbe uguali" % (list(ids_a), commit[:7], list(ids_b)))
    print("-" * 96)
    print("  l'ORDINE: adesso %d pezzi (impronta %s) -- %s %d pezzi (impronta %s)"
          % (na, ia, commit[:7], nb, ib))
    assert len(ba) == len(bb), (len(ba), len(bb))
    # ### ⭐ **IL CRITERIO: i PEZZI.** L-ultimo blocco di ogni scena e- il passo intero,
    # ### ### **e NON e- un criterio**: e- un numero da riportare.
    quanti, rotti = 0, []
    k = 0
    for nn, seme in SCENE:
        for idl in PEZZI:
            quanti += 1
            if ba[k] != bb[k]:
                rotti.append((nn, seme, idl))
            k += 1
        k += 1  # ### il passo intero, che NON e- un criterio
    print("-" * 96)
    if rotti:
        print("### ⛔ `M-B1` FALLISCE: %d pezzi su %d NON coincidono al bit: %s"
              % (len(rotti), quanti, rotti))
    else:
        print("### ✅ `M-B1` PASSA: TUTTI i %d pezzi coincidono AL BIT (6 pezzi x %d scene)"
              % (quanti, len(SCENE)))
    # ------------------------------------------------- l-INFORMAZIONE, non il criterio
    print("-" * 96)
    print("### 📌 INFORMAZIONE (NON un criterio): la distanza fra il passo PALINDROMO di")
    print("###   adesso e il passo di %s, su %d tick." % (commit[:7], TICK))
    for nn, seme in SCENE:
        pa = np.load(qui + ".psi.%d.%d.npy" % (nn, seme))
        pb = np.load(la + ".psi.%d.%d.npy" % (nn, seme))
        fa = np.load(qui + ".phi.%d.%d.npy" % (nn, seme))
        fb = np.load(la + ".phi.%d.%d.npy" % (nn, seme))
        dp = float(np.max(np.abs(pa - pb)))
        df = float(np.max(np.abs(fa - fb)))
        sc = max(float(np.max(np.abs(pb))), float(np.max(np.abs(fb))))
        print("###   nn=%-4d seme=%-4d  max|d psi| = %.6e   max|d phi| = %.6e"
              "   su scala %.3e" % (nn, seme, dp, df, sc))
    print("###   E NON E' UN DIFETTO: i pezzi NON COMMUTANO, quindi una composizione")
    print("###   palindroma NON PUO' dare il passo di una composizione che non lo era.")
    return 1 if rotti else 0


# =====================================================================================
#   IL COLLAUDO -- **la prova che `M-B1` PUO' FALLIRE**
# -------------------------------------------------------------------------------------
# ### ⛔⛔ **PERCHE' QUESTO COLLAUDO ESISTE** *(integrazione del guardiano del
# ### `2026-10-16`)*: `M-B1` e' ### **il criterio** con cui ogni cura dimostra di
# ### **non aver mosso un bit** -- e ### **finora nessuno aveva mostrato che PUO'
# ### fallire.** ### **Un criterio di cui non si e' visto il fallimento e' una promessa.**
#
# ### ⚠⚠ **E IL COLLAUDO DICE ANCHE CHE COSA `M-B1` NON VEDE, per disegno:** il criterio
# ### sono ### **I PEZZI** *(`un_pezzo` applica UN pezzo a `theta = pi`)*. ### **L'ORDINE
# ### di composizione e' RIPORTATO** *(l'impronta, riga per riga)* ### **e NON e' un
# ### criterio** -- cosi' c'e' scritto nel codice dal primo giorno.
# ### 📌 **Quindi per il punto `D`: `M-B1` da solo NON prova che il passo e' lo stesso.**
# ### **Prova che i PEZZI sono gli stessi**, e ### **l'impronta dell'ordine va LETTA.**
# ### **I due bracci qui sotto provano le DUE META' di questo confine.**
_LA_MISURA = os.path.abspath(__file__)


def _perturba_operatore(src):
    """Il `tick.py` di oggi con ### **DUE OPERATORI SCAMBIATI** in `OPERATORE`.

    ### ⭐ **Tocca cio' che IL CRITERIO GUARDA:** `un_pezzo` prende il nome
    dell-operatore da `OPERATORE`, quindi scambiarne due ### **cambia i byte DI DUE
    PEZZI** -- ed e' esattamente il genere di cambiamento che `M-B1` deve vedere.
    """
    a = '    "CAMM-GROVER": ("grover", False),\n'
    b = '    "CAMM-GROVER": ("grover_scalare", False),\n'
    assert src.count(a) == 1, "l-ancora di `CAMM-GROVER` non e- unica in `tick.py`"
    return src.replace(a, b)


def _perturba_ordine(src):
    """Il `tick.py` di oggi che percorre l-ordine ### **con DUE PEZZI SCAMBIATI.**

    ### ⛔⛔ **E NON SI PUO' INVERTIRE L-ORDINE: E- UN PALINDROMO** *(misurato: la
    sequenza invertita e- ### **IDENTICA**)*. ### **Una perturbazione che non cambia
    niente darebbe un braccio VACUO**, quindi si SCAMBIANO le posizioni `1` e `2`, e
    ### **un braccio verifica che la sequenza sia DAVVERO cambiata.**
    """
    a = "    for k, (idl, frazione, _tipo) in enumerate(CM.ORDINE):\n"
    b = ("    _o = list(CM.ORDINE)\n"
         "    _o[1], _o[2] = _o[2], _o[1]\n"
         "    for k, (idl, frazione, _tipo) in enumerate(tuple(_o)):\n")
    assert src.count(a) == 1, "l-ancora del ciclo non e- unica in `tick.py`"
    return src.replace(a, b)


def _byte_dell_albero(commit, dove, tick_src):
    """I byte dei pezzi, facendo girare ### **la misura di oggi** in un albero di `commit`.

    `tick_src` e' ### **il sorgente del passo da METTERE nell-albero**, oppure `None` per
    ### **non toccarlo** -- che e' la via giusta, e l-altra serve solo ### **a mostrare il
    difetto.**
    """
    alb = _albero_vecchio(commit, dove)
    shutil.copyfile(_LA_MISURA, os.path.join(alb, "primo_ordine", "_misura_mb1.py"))
    if tick_src is not None:
        io.open(os.path.join(alb, "primo_ordine", "tick.py"), "wb").write(
            tick_src.encode("utf-8"))
    fuori = dove + ".bin"
    r = subprocess.run([sys.executable, os.path.join("primo_ordine", "_misura_mb1.py"),
                        "--scrivi", fuori], cwd=alb, capture_output=True)
    assert not r.returncode, ("la corsa in %s e- FALLITA: %s"
                              % (commit[:7],
                                 (r.stdout + r.stderr).decode("utf-8", "replace")[-700:]))
    _n, _i, _ids, blocchi = _leggi(fuori)
    return _n, _i, blocchi


def _passo_intero_diversi(ba, bb):
    """Quante volte il ### **PASSO INTERO** non coincide: e' l-ultimo blocco di ogni scena.

    ### ⚠ **Non e' il criterio di `contro()`** -- la' e' <<informazione>>. ### **Serve
    a dire CHE COSA si muove quando si muove solo il CAMMINO**, e il numero sta nel
    collaudo.
    """
    diversi, k = 0, 0
    for _nn, _seme in SCENE:
        k += len(PEZZI)
        if ba[k] != bb[k]:
            diversi += 1
        k += 1
    return diversi


def _pezzi_diversi(ba, bb):
    """Quanti PEZZI non coincidono, col criterio di `contro()`."""
    rotti, k = 0, 0
    for _nn, _seme in SCENE:
        for _idl in PEZZI:
            if ba[k] != bb[k]:
                rotti += 1
            k += 1
        k += 1
    return rotti


_OK = []


def _esito(che, passa, nota=""):
    _OK.append(bool(passa))
    print("  %-66s %s   %s" % (che[:66], "PASSA" if passa else "### FALLISCE", nota))


# ### ⛔ **GLI STRUMENTI CHE MATERIALIZZANO UN ALBERO DEL PASSATO E VI ESEGUONO PYTHON.**
# ### ⚠ **La lista e' DICHIARATA, e uno nuovo FA FALLIRE** invece di passare: la stessa
# ### regola vale per lui, cioe' ### **nell-albero vecchio non si copia codice del passo.**
# ### 📌 **E <<materializzare un ALBERO>> non e' <<leggere un file da un commit>>:**
# ### `12` strumenti leggono TESTO da un commit *(documenti, indice)* e fanno girare
# ### ### **i comandi di OGGI** -- e quelli non hanno questo problema.
CONFRONTANO_ESEGUENDO = ("primo_ordine/_misura_mb1.py",)


def _censimento():
    """Chi materializza un albero del passato ### **e vi esegue python.**

    ### ⛔⛔ **CON L-AST, E NON CON UNA PAROLA** *(e la prima stesura cercava la
    parola: ha pescato ### **il commento che avevo appena scritto in `collauda.py`**)*.
    ### ✅ **Si cerca la FORMA VERA: una lista di argomenti che contiene `"worktree"`
    o `"archive"`** -- cioe' ### **una chiamata a `git`**, non una frase in prosa.
    ### ⭐ **E i commenti sono INVISIBILI all-AST**, che qui e' esattamente cio- che
    serve: e- la stessa lezione di `P-TAB`.
    """
    import ast
    import glob
    fuori_perimetro = ("_archivio", "_seal_", "_test_")
    tro = []
    for q in sorted(glob.glob(os.path.join(RADICE, "csv", "**", "*.py"), recursive=True)
                    + glob.glob(os.path.join(RADICE, "primo_ordine", "**", "*.py"),
                                recursive=True)):
        rel = os.path.relpath(q, RADICE).replace(os.sep, "/")
        if any(k in rel for k in fuori_perimetro):
            continue
        try:
            arb = ast.parse(io.open(q, encoding="utf-8").read())
        except SyntaxError:
            continue
        albero, esegue = False, False
        for n in ast.walk(arb):
            if isinstance(n, (ast.List, ast.Tuple)):
                for x in n.elts:
                    if (isinstance(x, ast.Constant)
                            and x.value in ("worktree", "archive")):
                        albero = True
            if isinstance(n, ast.Attribute) and n.attr == "executable":
                esegue = True
        if albero and esegue:
            tro.append(rel)
    return tro


def collaudo():
    import tempfile
    print("=" * 100)
    print("IL COLLAUDO DI `M-B1`: LA PROVA CHE PUO' FALLIRE")
    print("=" * 100)
    base = tempfile.mkdtemp(prefix="mb1c_")
    oggi = io.open(os.path.join(_QUI, "tick.py"), encoding="utf-8").read()
    try:
        # ### ⭐ **LA GUARDIA CONTRO IL BRACCIO VACUO: la perturbazione CAMBIA la sequenza.**
        import composizione as CM
        _o = list(CM.ORDINE)
        _o[1], _o[2] = _o[2], _o[1]
        seq = [x[0] for x in CM.ORDINE]
        _esito("### la perturbazione dell-ORDINE cambia DAVVERO la sequenza",
               [x[0] for x in _o] != seq and seq[::-1] == seq,
               "### e l-ordine e- un PALINDROMO (invertirlo NON cambia niente): per questo"
               " si SCAMBIANO due posizioni")
        # ### ⛔⛔ **IL CASO CHE DEVE FALLIRE: il passo di oggi MODIFICATO.**
        n1, i1, b_pert = _byte_dell_albero("8c7b9288", os.path.join(base, "pert"),
                                           _perturba_operatore(oggi))
        n2, i2, b_puro = _byte_dell_albero("8c7b9288", os.path.join(base, "puro"), None)
        rotti = _pezzi_diversi(b_pert, b_puro)
        _esito("### ⛔ DEVE FALLIRE: col passo di oggi MODIFICATO il confronto DIVERGE",
               rotti > 0, "### %d pezzi su %d NON coincidono: il criterio VEDE il"
               " cambiamento" % (rotti, len(SCENE) * len(PEZZI)))
        # ### ⛔⛔ **E COL DIFETTO DI IERI PASSEREBBE**, ed e' il punto dell-integrazione:
        # ### copiando il passo modificato ### **ANCHE nell-albero vecchio**, i due lati
        # ### usano ### **lo stesso passo** e il confronto ### **non vede niente.**
        n3, i3, b_infetto = _byte_dell_albero("8c7b9288", os.path.join(base, "infetto"),
                                              _perturba_operatore(oggi))
        _esito("### ⛔ e COL DIFETTO DI IERI il confronto PASSEREBBE (falso-uno)",
               _pezzi_diversi(b_pert, b_infetto) == 0,
               "### 0 pezzi diversi: copiando il passo di oggi nell-albero vecchio, i due"
               " lati girano LO STESSO passo")
        # ### ⚠⚠ **E LA META' CHE `M-B1` NON VEDE, per disegno:** una perturbazione del
        # ### SOLO ORDINE ### **non cambia i pezzi** -- li cambia l-IMPRONTA, che e'
        # ### ### **riportata e non e' un criterio.**
        n4, i4, b_ordine = _byte_dell_albero("8c7b9288", os.path.join(base, "ordine"),
                                             _perturba_ordine(oggi))
        _esito("### ⚠ e una perturbazione del SOLO CAMMINO NON tocca i pezzi (per disegno)",
               _pezzi_diversi(b_ordine, b_puro) == 0,
               "### 0 pezzi diversi: il criterio di `M-B1` sono I PEZZI")
        # ### ⛔⛔ **E NEMMENO L-IMPRONTA LA VEDE, ed e' la cosa che questo braccio ha
        # ### fatto uscire:** l-impronta viene da ### **`composizione.py`**, cioe' dalla
        # ### TABELLA, e ### **non da come `tick.py` percorre l-ordine.**
        # ### ✅ **CIO- CHE SI MUOVE E- IL PASSO INTERO**, che `contro()` riporta come
        # ### ### **informazione e NON come criterio.**
        # ### 📌 **Quindi per il punto `D`: se cambia IL CAMMINO e non la tabella, `M-B1`
        # ### dice <<12 su 12 AL BIT>> e l-impronta e- IDENTICA** -- e la sola cosa che lo
        # ### dice e' ### **la distanza del passo intero, che va LETTA.**
        _esito("### ⛔ e NEMMENO l-impronta la vede: viene dalla TABELLA, non dal cammino",
               i4 == i2,
               "### le due impronte sono UGUALI (%s): l-impronta segue `composizione.py`,"
               " non `tick.py`" % i4)
        _esito("### ✅ ma il PASSO INTERO si muove, e `contro()` lo RIPORTA",
               _passo_intero_diversi(b_ordine, b_puro) == len(SCENE),
               "### %d scene su %d col passo intero DIVERSO: e- l-unico numero che vede un"
               " cammino cambiato, ed e- <<informazione, non criterio>>"
               % (_passo_intero_diversi(b_ordine, b_puro), len(SCENE)))
        # ### ⛔⛔ **IL `2-SEXIES`, braccio che DEVE fallire: un id nell-ORDINE che la
        # ### misura NON SA applicare.** ### **Si perturba `CM.ORDINE` IN MEMORIA**, come
        # ### fa il collaudo della deriva: nessun file del repo si tocca.
        import composizione as CM
        vecchio_ordine = CM.ORDINE
        alzato = ""
        try:
            CM.ORDINE = (("CAMM-INVENTATA", 0.5, "flusso"),) + tuple(vecchio_ordine)
            vecchi_pezzi = PEZZI
            globals()["PEZZI"] = pezzi_dell_ordine()
            try:
                pezzi_applicabili()
            except AssertionError as e:
                alzato = str(e)[:60]
            globals()["PEZZI"] = vecchi_pezzi
        finally:
            CM.ORDINE = vecchio_ordine
        _esito("### ⛔ DEVE fallire: un id NELL-ORDINE che la misura non sa applicare",
               bool(alzato), "### ha alzato: %s" % alzato)
        # ### ⭐⭐ **IL CONTROLLO POSITIVO DEL `2-SEXIES`: la legge CHE GIRA e- fra i
        # ### pezzi confrontati, e COINCIDE AL BIT.** ### ⚠ **Fino al `2026-10-16` NON
        # ### c-era:** `PEZZI` era una lista a mano che conteneva la ### **saturazione**
        # ### *(fuori dall-ordine)* e ### **non la legge che gira.**
        import tempfile as _tf
        _oggi_bin = os.path.join(base, "oggi.bin")
        scrivi(_oggi_bin)
        _n5, _i5, ids5, b_oggi = _leggi(_oggi_bin)
        _k = PEZZI.index("CAMM-MATERIA-VUOTO") if "CAMM-MATERIA-VUOTO" in PEZZI else -1
        ugua = _k >= 0 and all(
            b_oggi[j * (len(PEZZI) + 1) + _k] == b_puro[j * (len(PEZZI) + 1) + _k]
            for j in range(len(SCENE)))
        _esito("### ⭐ la legge CHE GIRA e- fra i pezzi, e coincide AL BIT contro 8c7b928",
               ugua, "### `CAMM-MATERIA-VUOTO` e- il pezzo n.%d di %d, e i suoi byte"
               " coincidono su %d scene su %d" % (_k + 1, len(PEZZI), len(SCENE),
                                                  len(SCENE)))
        # ### ⭐ **E l-assert che la misura non PORTA il passo: si chiama, non si descrive.**
        _la_misura_non_porta_il_passo()
        _esito("### la misura NON definisce nessuna funzione del passo", True,
               "### l-assert gira a OGNI confronto, non solo qui")
        # ### ⭐ **IL CENSIMENTO, e la lista DICHIARATA.**
        visti = _censimento()
        _esito("### e SOLO gli strumenti DICHIARATI materializzano un albero ed eseguono",
               tuple(visti) == CONFRONTANO_ESEGUENDO,
               "### visti %s, dichiarati %s" % (visti, list(CONFRONTANO_ESEGUENDO)))
    finally:
        for q in ("pert", "puro", "infetto", "ordine"):
            d = os.path.join(base, q)
            if os.path.isdir(d):
                subprocess.run(["git", "worktree", "remove", "--force", d], cwd=RADICE,
                               capture_output=True)
        shutil.rmtree(base, ignore_errors=True)
    print("=" * 100)
    print("IL COLLAUDO DI `M-B1`: %d su %d   %s"
          % (sum(_OK), len(_OK),
             "### TUTTI PASSATI" if all(_OK) else "### CI SONO ROSSI"))
    print("=" * 100)
    return 0 if all(_OK) else 1


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    if argv and argv[0] == "--scrivi":
        return scrivi(argv[1])
    if "--collaudo" in argv:
        return collaudo()
    print("=" * 96)
    print("M-B1: IL RACCORDO AL BIT, PEZZO PER PEZZO -- dtau = dtau_rif = %.1f" % DTAU)
    print("=" * 96)
    print("  LA CONFIGURAZIONE: dtau = %.1f   tick = %d   scene = %s   norma = %s"
          "   vuoto_modulo = %.1f   su2 = %s" % (DTAU, TICK, SCENE, NORMA,
                                                 VUOTO_MODULO, SU2))
    if argv and argv[0] == "--contro":
        return contro(argv[1])
    scrivi(os.path.join(os.environ.get("TEMP", "."), "mb1_solo.bin"))
    print("### ⚠ senza `--contro <commit>` questa e' UNA SOLA corsa: nessun confronto")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
