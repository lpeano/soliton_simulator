# -*- coding: utf-8 -*-
r"""IL COLLAUDO DI `M-B1` -- ### **la prova che il criterio PUO- FALLIRE.**

> ### ⛔⛔ **PERCHE- QUESTO FILE ESISTE** *(`2026-10-18`, su rifiuto di `P-MOD`)*:
> questo collaudo viveva ### **dentro `_misura_mb1.py`**, che il mandato della strada `(d)`
> ha portato a ### **`712` righe su un tetto di `700`** -- e la regola e- chiara: ### **oltre
> SI DIVIDE, NON SI ALLUNGA.**
> ### ✅ **E uscire e- la cosa giusta comunque:** `_misura_mb1.py` ### **MISURA**, questo
> ### **PROVA CHE LA MISURA PUO- DIRE NO** -- due cose, due moduli.
> ### ⚠⚠ **E UNA COSA CHE AVEVO SCRITTO QUI ED ERA FALSA, corretta subito dopo:**
> avevo detto che questo file va nella lista `CONFRONTANO_ESEGUENDO`. ### **NON ci va**,
> e il censimento ha ragione a non vederlo: ### **questo file non materializza niente** --
> ### **DELEGA** a `_misura_mb1._byte_dell_albero`, che e- ### **lo strumento dichiarato.**
> ### ✅ **E la lista dice la verita-: <<chi materializza un albero ED ESEGUE python>>**,
> non <<chi lo fa fare a qualcun altro>>.

Gira con:  python primo_ordine/_collauda_mb1.py
"""
import io
import os
import shutil
import subprocess
import sys
import tempfile

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
sys.path.insert(0, os.path.join(_QUI, "leggi"))
sys.path.insert(0, os.path.join(os.path.dirname(_QUI), "csv"))

import _misura_mb1 as MB1                                      # noqa: E402
import composizione as CM                                      # noqa: E402

# ### ✅ **I NOMI DELLA MISURA SI PRENDONO DA LEI**, non si ricopiano: un secondo
# ### elenco ### **sarebbe il prossimo a restare indietro.**
RADICE = MB1.RADICE
SCENE = MB1.SCENE
TICK = MB1.TICK
VIAGGIANO = MB1.VIAGGIANO
PEZZI_NUOVI = MB1.PEZZI_NUOVI


def collaudo():
    import tempfile
    # ### ⛔ **L-IMPORT STA QUI, NON IN TESTA:** questo file ### **viaggia nell-albero
    # ### vecchio** *(`VIAGGIANO`)*, e la' ### **`_censimento_strumenti.py` NON ESISTE**:
    # ### in testa farebbe fallire la corsa del commit vecchio con un
    # ### `ModuleNotFoundError`.
    # ### ✅ **E i censimenti servono SOLO al collaudo**, che nell-albero vecchio
    # ### ### **non gira mai.** ### ⚠ **L-alternativa era far viaggiare un file in piu-,
    # ### e un file in piu- nell-albero vecchio e- ### **la famiglia del difetto n.6.**
    import _censimento_strumenti as CENS
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
        MB1._esito("### la perturbazione dell-ORDINE cambia DAVVERO la sequenza",
               [x[0] for x in _o] != seq and seq[::-1] == seq,
               "### e l-ordine e- un PALINDROMO (invertirlo NON cambia niente): per questo"
               " si SCAMBIANO due posizioni")
        # ### ⛔⛔ **IL CASO CHE DEVE FALLIRE: il passo di oggi MODIFICATO.**
        n1, i1, b_pert, ids_pert = MB1._byte_dell_albero("8c7b9288", os.path.join(base, "pert"),
                                           MB1._perturba_operatore(oggi))
        n2, i2, b_puro, ids_puro = MB1._byte_dell_albero("8c7b9288", os.path.join(base, "puro"), None)
        rotti = MB1._pezzi_diversi(b_pert, b_puro)
        MB1._esito("### ⛔ DEVE FALLIRE: col passo di oggi MODIFICATO il confronto DIVERGE",
               rotti > 0, "### %d pezzi su %d NON coincidono: il criterio VEDE il"
               " cambiamento" % (rotti, len(SCENE) * len(MB1.PEZZI)))
        # ### ⛔⛔ **E COL DIFETTO DI IERI PASSEREBBE**, ed e' il punto dell-integrazione:
        # ### copiando il passo modificato ### **ANCHE nell-albero vecchio**, i due lati
        # ### usano ### **lo stesso passo** e il confronto ### **non vede niente.**
        n3, i3, b_infetto, ids_infetto = MB1._byte_dell_albero("8c7b9288", os.path.join(base, "infetto"),
                                              MB1._perturba_operatore(oggi))
        MB1._esito("### ⛔ e COL DIFETTO DI IERI il confronto PASSEREBBE (falso-uno)",
               MB1._pezzi_diversi(b_pert, b_infetto) == 0,
               "### 0 pezzi diversi: copiando il passo di oggi nell-albero vecchio, i due"
               " lati girano LO STESSO passo")
        # ### ⚠⚠ **E LA META' CHE `M-B1` NON VEDE, per disegno:** una perturbazione del
        # ### SOLO ORDINE ### **non cambia i pezzi** -- li cambia l-IMPRONTA, che e'
        # ### ### **riportata e non e' un criterio.**
        n4, i4, b_ordine, ids_ordine = MB1._byte_dell_albero("8c7b9288", os.path.join(base, "ordine"),
                                             MB1._perturba_ordine(oggi))
        MB1._esito("### ⚠ e una perturbazione del SOLO CAMMINO NON tocca i pezzi (per disegno)",
               MB1._pezzi_diversi(b_ordine, b_puro) == 0,
               "### 0 pezzi diversi: il criterio di `M-B1` sono I MB1.PEZZI")
        # ### ⛔⛔ **E NEMMENO L-IMPRONTA LA VEDE, ed e' la cosa che questo braccio ha
        # ### fatto uscire:** l-impronta viene da ### **`composizione.py`**, cioe' dalla
        # ### TABELLA, e ### **non da come `tick.py` percorre l-ordine.**
        # ### ✅ **CIO- CHE SI MUOVE E- IL PASSO INTERO**, che `MB1.contro()` riporta come
        # ### ### **informazione e NON come criterio.**
        # ### 📌 **Quindi per il punto `D`: se cambia IL CAMMINO e non la tabella, `M-B1`
        # ### dice <<12 su 12 AL BIT>> e l-impronta e- IDENTICA** -- e la sola cosa che lo
        # ### dice e' ### **la distanza del passo intero, che va LETTA.**
        MB1._esito("### ⛔ e NEMMENO l-impronta la vede: viene dalla TABELLA, non dal cammino",
               i4 == i2,
               "### le due impronte sono UGUALI (%s): l-impronta segue `composizione.py`,"
               " non `tick.py`" % i4)
        MB1._esito("### ✅ ma il PASSO INTERO si muove, e `MB1.contro()` lo RIPORTA",
               MB1._passo_intero_diversi(b_ordine, b_puro) == len(SCENE),
               "### %d scene su %d col passo intero DIVERSO: e- l-unico numero che vede un"
               " cammino cambiato, ed e- <<informazione, non criterio>>"
               % (MB1._passo_intero_diversi(b_ordine, b_puro), len(SCENE)))
        # ### ⛔⛔ **IL `2-SEXIES`, braccio che DEVE fallire: un id nell-ORDINE che la
        # ### misura NON SA applicare.** ### **Si perturba `CM.ORDINE` IN MEMORIA**, come
        # ### fa il collaudo della deriva: nessun file del repo si tocca.
        import composizione as CM
        vecchio_ordine = CM.ORDINE
        alzato = ""
        try:
            CM.ORDINE = (("CAMM-INVENTATA", 0.5, "flusso"),) + tuple(vecchio_ordine)
            # ### ⛔⛔ **IL REBIND VA SUL MODULO, non su `globals()` di qui**
            # ### *(`2026-10-18`)*: `pezzi_applicabili` legge ### **`PEZZI` del SUO
            # ### modulo**, e scrivere in `globals()` di questo file ### **non lo
            # ### toccava** -- il braccio alzava, ma ### **per un altro motivo.**
            vecchi_pezzi = MB1.PEZZI
            MB1.PEZZI = MB1.pezzi_dell_ordine()
            try:
                MB1.pezzi_applicabili()
            except AssertionError as e:
                alzato = str(e)[:60]
            MB1.PEZZI = vecchi_pezzi
        finally:
            CM.ORDINE = vecchio_ordine
        MB1._esito("### ⛔ DEVE fallire: un id NELL-ORDINE che la misura non sa applicare",
               bool(alzato), "### ha alzato: %s" % alzato)
        # ### ⭐⭐ **IL CONTROLLO POSITIVO DEL `2-SEXIES`: la legge CHE GIRA e- fra i
        # ### pezzi confrontati, e COINCIDE AL BIT.** ### ⚠ **Fino al `2026-10-16` NON
        # ### c-era:** `MB1.PEZZI` era una lista a mano che conteneva la ### **saturazione**
        # ### *(fuori dall-ordine)* e ### **non la legge che gira.**
        import tempfile as _tf
        _oggi_bin = os.path.join(base, "oggi.bin")
        MB1.scrivi(_oggi_bin)
        _n5, _i5, ids5, b_oggi = MB1._leggi(_oggi_bin)
        # ### ⛔⛔ **LO STRIDE E- DI CIASCUN LATO, e l-indice si cerca NEI SUOI
        # ### `id`** *(`2026-10-18`)*: da quando l-ordine di oggi ha ### **un pezzo in
        # ### piu-**, usare lo stride di oggi su un albero vecchio
        # ### ### **legge i blocchi sbagliati** -- e il braccio diceva <<diversi>> di
        # ### byte che non aveva nemmeno guardato.
        _q = "CAMM-MATERIA-VUOTO"
        _ka = list(ids5).index(_q) if _q in ids5 else -1
        _kb = list(ids_puro).index(_q) if _q in ids_puro else -1
        _sa, _sb = len(ids5) + 1, len(ids_puro) + 1
        ugua = _ka >= 0 and _kb >= 0 and all(
            b_oggi[j * _sa + _ka] == b_puro[j * _sb + _kb]
            for j in range(len(SCENE)))
        MB1._esito("### ⭐ la legge CHE GIRA e- fra i pezzi, e coincide AL BIT contro 8c7b928",
               ugua, "### `CAMM-MATERIA-VUOTO` e- il pezzo n.%d di %d (n.%d di %d nell-albero"
               " vecchio), e i suoi byte coincidono su %d scene su %d"
               % (_ka + 1, len(ids5), _kb + 1, len(ids_puro), len(SCENE),
                  len(SCENE)))
        # ### ⭐ **E l-assert che la misura non PORTA il passo: si chiama, non si descrive.**
        MB1._la_misura_non_porta_il_passo()
        MB1._esito("### la misura NON definisce nessuna funzione del passo", True,
               "### l-assert gira a OGNI confronto, non solo qui")
        # ### ⭐ **IL CENSIMENTO, e la lista DICHIARATA.**
        visti = CENS._censimento()
        MB1._esito("### e SOLO gli strumenti DICHIARATI materializzano un albero ed eseguono",
               tuple(visti) == CENS.CONFRONTANO_ESEGUENDO,
               "### visti %s, dichiarati %s" % (visti, list(CENS.CONFRONTANO_ESEGUENDO)))
        # ### ⛔ **E NESSUNO SCRIVE NEL REPO:** chi legge `TEMP` dall'ambiente ha
        # ### ### **un ripiego**, e su Linux quel ripiego e' ### **la radice del repo.**
        tempi = CENS._censimento_temporanei()
        MB1._esito("### e NESSUNO strumento legge `TEMP` dall'ambiente (il ripiego e' il repo)",
               tuple(tempi) == CENS.TEMPORANEI_AMMESSI,
               "### visti %s, ammessi %s -- la cura e' `tempfile`, che non ha ripieghi"
               % (tempi, list(CENS.TEMPORANEI_AMMESSI)))
    finally:
        # ### ⛔ **E SI SGOMBERA COME IN `contro`:** `git worktree remove` piu'
        # ### ### **`prune`**, perche' una cartella cancellata a mano lascia
        # ### ### **la registrazione in `.git/worktrees`** -- e `git worktree list` la
        # ### mostrerebbe per sempre. ### **Misurato il `2026-10-17`: ce n'erano `4` di
        # ### corse vecchie.**
        for q in ("pert", "puro", "infetto", "ordine"):
            MB1._sgombera(RADICE, os.path.join(base, q))
        shutil.rmtree(base, ignore_errors=True)
    print("=" * 100)
    print("IL COLLAUDO DI `M-B1`: %d su %d   %s"
          % (sum(MB1._OK), len(MB1._OK),
             "### TUTTI PASSATI" if all(MB1._OK) else "### CI SONO ROSSI"))
    print("=" * 100)
    return 0 if all(MB1._OK) else 1


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    return collaudo()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
