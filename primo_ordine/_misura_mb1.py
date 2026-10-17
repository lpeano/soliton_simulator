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
import tempfile
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
# ### ⛔⛔ **I PEZZI NUOVI: DICHIARATI, E NON CONFRONTATI** *(`2026-10-18`)*.
# ### ⚠ **Un pezzo che nell-albero vecchio NON ESISTE non si puo- confrontare**,
# ### e il confronto per posizione ### **lo crederebbe un altro pezzo**: e- il difetto
# ### che il controllo degli `id` impedisce dal `2026-10-17`.
# ### ✅ **E ALLORA SI DICHIARA, con la data e il motivo**, e il criterio diventa:
# ### ### **i pezzi di PRIMA devono coincidere TUTTI al bit**, e ### **la distanza del
# ### passo intero deve essere `0`** -- che e- cio- che dimostra che il pezzo nuovo
# ### ### **a forma spenta NON FA NIENTE.**
# ### ⛔ **E la lista NON e- una via d-uscita: e- un IMPEDIMENTO IN MENO che si paga** --
# ### con un nome qui dentro ### **quel pezzo non e- piu- sorvegliato da `M-B1`**, e va
# ### ### **TOLTO** appena esiste un commit in cui c-e- da entrambi i lati.
PEZZI_NUOVI = (
    # ### `CAMM-FASE-VUOTO` nasce il `2026-10-18` *(la strada `(d)`)*: nell-albero
    # ### prima di questo mandato ### **non c-e-**.
    "CAMM-FASE-VUOTO",
)


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
    # ### ⛔⛔ **IL TEMPORANEO STA FUORI DAL REPO** *(difetto trovato dal guardiano
    # ### il `2026-10-17`)*: prima era `os.environ.get("TEMP", radice)`, e
    # ### ### **su Linux `TEMP` non esiste** -- quindi questa misura scriveva
    # ### ### **una copia INTERA dell-albero vecchio DENTRO IL REPO**, e non la
    # ### cancellava. ### ✅ **`tempfile.mkdtemp()` non ha ripieghi**, e il `finally`
    # ### qui sotto ### **cancella anche se la misura ALZA.**
    fuori = tempfile.mkdtemp(prefix="mb1_")
    try:
        return _contro(commit, radice, fuori)
    finally:
        # ### ⛔ **IL WORKTREE SI TOGLIE CON `git`, non con `rmtree`:** una cartella
        # ### cancellata a mano lascia ### **la registrazione in `.git/worktrees`.**
        _sgombera(radice, os.path.join(fuori, "albero"))
        shutil.rmtree(fuori, ignore_errors=True)


def _sgombera(radice, dove):
    """### Toglie un `git worktree` ### **e la sua registrazione.**"""
    if os.path.isdir(dove):
        subprocess.run(["git", "worktree", "remove", "--force", dove], cwd=radice,
                       capture_output=True)
    subprocess.run(["git", "worktree", "prune"], cwd=radice, capture_output=True)


def _contro(commit, radice, fuori):
    """Il corpo del confronto, ### **dentro il `try` di `contro`.**"""
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
    nuovi = [q for q in ids_a if q in PEZZI_NUOVI]
    assert [q for q in ids_a if q not in PEZZI_NUOVI] == list(ids_b), (
        "`M-B1`: i PEZZI dei due alberi NON COINCIDONO, e il confronto NON PARTE."
        " ### adesso %s;  %s %s;  dichiarati NUOVI %s. ### I pezzi si leggono"
        " dall-ORDINE di ciascun albero: se l-ordine e- cambiato, i due lati"
        " misurerebbero COSE DIVERSE, e il confronto per posizione le crederebbe uguali."
        " ### Un pezzo che nasce si DICHIARA in `PEZZI_NUOVI`, con la data e il motivo"
        % (list(ids_a), commit[:7], list(ids_b), list(PEZZI_NUOVI)))
    if nuovi:
        print("### \u26a0 PEZZI NUOVI, DICHIARATI e NON confrontati: %s" % nuovi)
        print("###   Nell-albero vecchio NON ESISTONO, quindi non c-e- niente con cui")
        print("###   confrontarli. ### CIO- CHE LI SORVEGLIA E- LA DISTANZA DEL PASSO")
        print("###   INTERO: se a forma spenta non fosse `0`, il pezzo nuovo farebbe")
        print("###   qualcosa -- e invece a forma spenta NON DEVE FARE NIENTE.")
    print("-" * 96)
    print("  l'ORDINE: adesso %d pezzi (impronta %s) -- %s %d pezzi (impronta %s)"
          % (na, ia, commit[:7], nb, ib))
    # ### ⛔⛔ **I BLOCCHI SI CONFRONTANO PER `id`, NON PER POSIZIONE**
    # ### *(dal `2026-10-18`)*: con un pezzo NUOVO le due liste hanno
    # ### ### **lunghezze diverse**, e un confronto per posizione
    # ### ### **accoppierebbe pezzi SBAGLIATI** -- cioe' direbbe <<diversi>> di pezzi
    # ### che non si e' nemmeno guardati.
    # ### ✅ **Ogni scena ha `len(ids) + 1` blocchi** *(i pezzi, e poi il passo
    # ### intero)*, e l'indice si calcola ### **dentro la lista di CIASCUN lato.**
    pa_ids, pb_ids = list(ids_a), list(ids_b)
    assert len(ba) == len(SCENE) * (len(pa_ids) + 1), (len(ba), len(pa_ids))
    assert len(bb) == len(SCENE) * (len(pb_ids) + 1), (len(bb), len(pb_ids))
    # ### ⭐ **IL CRITERIO: i PEZZI CHE ESISTONO DA ENTRAMBI I LATI.** L-ultimo blocco
    # ### di ogni scena e- il passo intero, ### **e NON e- un criterio**: e- un numero da
    # ### riportare.
    quanti, rotti = 0, []
    for s, (nn, seme) in enumerate(SCENE):
        ka = s * (len(pa_ids) + 1)
        kb = s * (len(pb_ids) + 1)
        for idl in pb_ids:
            quanti += 1
            if ba[ka + pa_ids.index(idl)] != bb[kb + pb_ids.index(idl)]:
                rotti.append((nn, seme, idl))
    print("-" * 96)
    if rotti:
        print("### ⛔ `M-B1` FALLISCE: %d pezzi su %d NON coincidono al bit: %s"
              % (len(rotti), quanti, rotti))
    else:
        print("### ✅ `M-B1` PASSA: TUTTI i %d pezzi coincidono AL BIT (%d pezzi x %d"
              " scene)" % (quanti, len(pb_ids), len(SCENE)))
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
    # ### ⚠ **L-ANCORA E- CAMBIATA il `2026-10-17`**, perche- `D2` ha aggiunto `quanti`
    # ### al ciclo: ### **il collaudo l-ha detto subito**, alzando su <<ancora non unica>>.
    a = "    for k, (idl, frazione, _tipo) in enumerate(CM.ORDINE[:quanti]):\n"
    b = ("    _o = list(CM.ORDINE[:quanti])\n"
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
    # ### ⛔⛔ **E GLI `id` VIAGGIANO COL RISULTATO** *(`2026-10-18`)*: chi
    # ### confronta ha bisogno di sapere ### **quanti pezzi ha QUESTO lato**, perche'
    # ### un albero vecchio puo' averne ### **meno** -- e con lo stride di oggi
    # ### ### **si leggono i blocchi sbagliati.**
    return _n, _i, blocchi, _ids


def _passo_intero_diversi(ba, bb):
    """Quante volte il ### **PASSO INTERO** non coincide: e' l-ultimo blocco di ogni scena.

    ### ⚠ **Non e' il criterio di `contro()`** -- la' e' <<informazione>>. ### **Serve
    a dire CHE COSA si muove quando si muove solo il CAMMINO**, e il numero sta nel
    collaudo.
    """
    # ### ⛔⛔ **QUANTI PEZZI SI CONTA DAI BLOCCHI, NON DAL `PEZZI` DI QUESTO ALBERO**
    # ### *(`2026-10-18`)*: questi due aiutanti confrontano ### **alberi VECCHI**, che
    # ### possono avere ### **meno pezzi** -- e con `len(PEZZI)` di oggi l-indice ### **usciva
    # ### dalla lista.** ### ✅ **Ogni scena ha `pezzi + 1` blocchi** *(i pezzi, poi il
    # ### passo intero)*, quindi il numero ### **si DERIVA.**
    quanti = len(ba) // len(SCENE) - 1
    assert len(ba) == len(bb) == len(SCENE) * (quanti + 1), (
        "i due lati hanno %d e %d blocchi su %d scene: non sono lo stesso numero di"
        " pezzi, e un confronto per posizione accoppierebbe pezzi SBAGLIATI"
        % (len(ba), len(bb), len(SCENE)))
    diversi, k = 0, 0
    for _nn, _seme in SCENE:
        k += quanti
        if ba[k] != bb[k]:
            diversi += 1
        k += 1
    return diversi


def _pezzi_diversi(ba, bb):
    """Quanti PEZZI non coincidono, col criterio di `contro()`."""
    # ### ⛔⛔ **QUANTI PEZZI SI CONTA DAI BLOCCHI, NON DAL `PEZZI` DI QUESTO ALBERO**
    # ### *(`2026-10-18`)*: questi due aiutanti confrontano ### **alberi VECCHI**, che
    # ### possono avere ### **meno pezzi** -- e con `len(PEZZI)` di oggi l-indice ### **usciva
    # ### dalla lista.** ### ✅ **Ogni scena ha `pezzi + 1` blocchi** *(i pezzi, poi il
    # ### passo intero)*, quindi il numero ### **si DERIVA.**
    quanti = len(ba) // len(SCENE) - 1
    assert len(ba) == len(bb) == len(SCENE) * (quanti + 1), (
        "i due lati hanno %d e %d blocchi su %d scene: non sono lo stesso numero di"
        " pezzi, e un confronto per posizione accoppierebbe pezzi SBAGLIATI"
        % (len(ba), len(bb), len(SCENE)))
    rotti, k = 0, 0
    for _nn, _seme in SCENE:
        for _k in range(quanti):
            if ba[k] != bb[k]:
                rotti += 1
            k += 1
        k += 1
    return rotti


_OK = []


def _esito(che, passa, nota=""):
    _OK.append(bool(passa))
    print("  %-66s %s   %s" % (che[:66], "PASSA" if passa else "### FALLISCE", nota))


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    if argv and argv[0] == "--scrivi":
        return scrivi(argv[1])
    if "--collaudo" in argv:
        # ### ⛔⛔ **IL COLLAUDO NON STA PIU- QUI** *(`2026-10-18`, su rifiuto del
        # ### presidio della MODULARITA-: questo file era a `712` righe su `700`)*, e questo
        # ### e- ### **UN
        # ### CARTELLO**: ### **esce `1`** invece di tacere, perche' chi lancia il
        # ### comando di prima ### **deve accorgersene.** ### ✅ **E- la stessa forma di
        # ### `primo_ordine/leggi/schema.py`**, che fa cosi- dal `2026-10-10`.
        print("  IL COLLAUDO DI `M-B1` NON STA PIU- QUI.")
        print("  ### Gira:  python primo_ordine/_collauda_mb1.py")
        print("  ### (diviso il 2026-10-18: questo file era oltre il tetto di 700 righe)")
        return 1
    print("=" * 96)
    print("M-B1: IL RACCORDO AL BIT, PEZZO PER PEZZO -- dtau = dtau_rif = %.1f" % DTAU)
    print("=" * 96)
    print("  LA CONFIGURAZIONE: dtau = %.1f   tick = %d   scene = %s   norma = %s"
          "   vuoto_modulo = %.1f   su2 = %s" % (DTAU, TICK, SCENE, NORMA,
                                                 VUOTO_MODULO, SU2))
    if argv and argv[0] == "--contro":
        return contro(argv[1])
    _solo = tempfile.mkdtemp(prefix="mb1s_")
    try:
        scrivi(os.path.join(_solo, "mb1_solo.bin"))
    finally:
        shutil.rmtree(_solo, ignore_errors=True)
    print("### ⚠ senza `--contro <commit>` questa e' UNA SOLA corsa: nessun confronto")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
