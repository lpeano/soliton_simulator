# -*- coding: utf-8 -*-
"""LA BYTE-INERZIA DEGLI OSSERVATORI DI `A1`: `50` passi CON e SENZA, stato IDENTICO AL BIT.

*(Mandato di Luca del 2026-10-07, punto `2(c)`. ### **Se non lo danno, la corsa NON PARTE e
lo dico.**)*

### ⛔ **PERCHE' QUESTO CONTROLLO SERVE, e non e' cerimonia**

Il presidio `sola_lettura` di `_misura_verso.py` guarda ### **`net`**, e lo ripristina. Ma
gli ### **INVOLUCRI DELL'ORIGINE** toccano ### **DUE cose che NON sono `net`**:

| | |
|---|---|
| `REGOLE_NASCITA[(evento, "i")]["regola"]` | un dizionario ### **DI MODULO** |
| `net._allaccia` | un ### **metodo** sostituito sull'istanza |

> ### ⛔ **IL PRESIDIO DI `net` NON LI COPRE.** ### **Questo sigillo e' l'unico controllo
> che dice se hanno cambiato la dinamica** — e lo dice ### **al bit**, su tutto lo stato.

### LA FORMA DEL CONFRONTO

Due corse ### **nello stesso processo**, ciascuna con la sua `carica` *(quindi il suo
`rng`)*: la prima ### **NUDA** *(solo `_passo.passo_pieno`)*, la seconda ### **con i due
osservatori.** Poi si confronta ### **l'impronta di TUTTO `net.__dict__`**, con la stessa
funzione `_firma` del presidio.

### ⚠ **E SI DICHIARA CHE COSA SI ESCLUDE, perche' un'esclusione taciuta e' un insabbiamento**

I ### **contatori diagnostici** che gli osservatori fanno crescere ### **fuori** dal
presidio non esistono: ogni chiamata che scrive passa da `sola_lettura`. ### **Quindi
l'esclusione e' VUOTA**, e il confronto e' su ### **tutti** gli attributi.
### ✔ **Se un giorno servisse un'esclusione, questo file e' il posto dove dichiararla.**
"""
import contextlib
import io
import json
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, os.path.join(RADICE, "csv"))
sys.path.insert(0, os.path.join(RADICE, "csv", "_test_fork"))
import _presidio   # noqa: E402

_presidio.avvia(__file__)

import _passo                                    # noqa: E402
import _misura_verso as MV                       # noqa: E402
import _misura_plaquette as MP                   # noqa: E402
import _mitosi_soglia_grad as _MSG               # noqa: E402

stampa, riga, blob = _MSG.stampa, _MSG.riga, _MSG.blob
NL = chr(10)
PASSI = 50
FUORI = os.path.join(_QUI, "_inerzia_osservatori")
SIM = os.path.join(RADICE, "soliton_simulator.py")
BLOB_ATTESO = "b8c21049"
# ### L'ESCLUSIONE E' VUOTA, e si dichiara VUOTA.
ESCLUSI = ()


def _impronta(net):
    return {k: MV._firma(v) for k, v in net.__dict__.items() if k not in ESCLUSI}


def _gira(nome, con_osservatori):
    """Una corsa da `PASSI` passi. ### **La scena e il seme sono gli stessi.**"""
    with contextlib.redirect_stdout(io.StringIO()):
        S, N, _a = _MSG.carica(nome, SIM)
        oss = []
        if con_osservatori:
            oss = [MV.Verso(), MP.Plaquette()]
            for o in oss:
                o.prepara(S, N)
            for o in oss:
                o.osserva(S, N, 0, True)
        for k in range(1, PASSI + 1):
            _passo.passo_pieno(S, N)
            for o in oss:
                o.osserva(S, N, k, k in MV.PASSI_MISURA
                          or (k + 1) in MV.PASSI_MISURA)
        for o in oss:
            if hasattr(o, "ripristina_involucri"):
                o.ripristina_involucri(N)
    return S, N, oss


def main(argv):
    if not os.path.isdir(FUORI):
        os.makedirs(FUORI)
    riga("=")
    stampa("LA BYTE-INERZIA DEGLI OSSERVATORI: %d passi CON e SENZA" % PASSI)
    riga("=")
    b = blob(SIM)[:8]
    stampa("  simulatore %s   atteso %s" % (b, BLOB_ATTESO))
    if b != BLOB_ATTESO:
        stampa("  ### IL BLOB NON E' QUELLO ATTESO. MI FERMO.")
        return 1
    stampa("  strumenti: %s (verso)  %s (plaquette)"
           % (blob(MV.__file__)[:8], blob(MP.__file__)[:8]))
    stampa()
    stampa("  --- il braccio NUDO")
    _S1, N1, _o1 = _gira("inerzia_nuda", False)
    f1 = _impronta(N1)
    stampa("      n = %d, archi = %d, attributi = %d" % (N1.n, len(N1.i), len(f1)))
    stampa("  --- il braccio CON GLI OSSERVATORI")
    _S2, N2, o2 = _gira("inerzia_oss", True)
    f2 = _impronta(N2)
    stampa("      n = %d, archi = %d, attributi = %d" % (N2.n, len(N2.i), len(f2)))
    stampa()
    # ### IL CONFRONTO: chiavi E valori, e ### **si NOMINANO le differenze**, non si contano.
    solo1 = sorted(set(f1) - set(f2))
    solo2 = sorted(set(f2) - set(f1))
    diff = sorted(k for k in set(f1) & set(f2) if f1[k] != f2[k])
    riga("-")
    stampa("  attributi solo nel NUDO: %d  %s" % (len(solo1), solo1[:8]))
    stampa("  attributi solo CON gli osservatori: %d  %s" % (len(solo2), solo2[:8]))
    stampa("  attributi DIVERSI: %d" % len(diff))
    for k in diff[:20]:
        stampa("      %-26s nudo %s" % (k, str(f1[k])[:46]))
        stampa("      %-26s  oss %s" % ("", str(f2[k])[:46]))
    ok = not (solo1 or solo2 or diff)
    stampa()
    riga("=")
    if ok:
        stampa("  ### ✔ LA BYTE-INERZIA PASSA: lo stato e' IDENTICO AL BIT su %d "
               "attributi." % len(f1))
        stampa("  ### Gli osservatori NON cambiano la dinamica, involucri compresi.")
    else:
        stampa("  ### ⛔ LA BYTE-INERZIA FALLISCE. LA CORSA NON PARTE.")
        stampa("  ### Le differenze sono NOMINATE qui sopra.")
    riga("=")
    # ### ✔ **E UN CONTROLLO IN PIU', CHE PUO' FALLIRE:** gli involucri devono essere stati
    #   RIMOSSI, e la registrazione delle origini deve aver prodotto QUALCOSA -- altrimenti
    #   il braccio <<con osservatori>> non ha osservato niente e il confronto e' un
    #   ### **FALSO-UNO.**
    v = next((x for x in o2 if x.nome == "verso"), None)
    orig = len(v.origine) if v is not None else 0
    tolti = (v._involucri is None) if v is not None else False
    stampa("  controllo: origini registrate %d   involucri rimossi %s"
           % (orig, "SI" if tolti else "NO"))
    if orig == 0 or not tolti:
        stampa("  ### ⛔ IL BRACCIO <<CON OSSERVATORI>> NON HA OSSERVATO, o gli "
               "involucri sono rimasti: il confronto sarebbe un FALSO-UNO.")
        ok = False
    d = {"blob_sim": blob(SIM), "blob_verso": blob(MV.__file__),
         "blob_plaquette": blob(MP.__file__), "passi": PASSI,
         "esclusi": list(ESCLUSI), "attributi": len(f1),
         "solo_nudo": solo1, "solo_osservatori": solo2, "diversi": diff,
         "origini_registrate": orig, "involucri_rimossi": bool(tolti),
         "esito": "PASSA" if ok else "FALLISCE",
         "a_valle": {"nudo": [int(N1.n), int(len(N1.i))],
                     "oss": [int(N2.n), int(len(N2.i))]}}
    io.open(os.path.join(FUORI, "inerzia.json"), "w", encoding="utf-8").write(
        json.dumps(d, indent=1, default=str))
    io.open(os.path.join(FUORI, "inerzia.txt"), "w", encoding="utf-8").write(
        NL.join(_MSG.P) + NL)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
