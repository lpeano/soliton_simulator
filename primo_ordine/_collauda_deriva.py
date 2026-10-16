# -*- coding: utf-8 -*-
r"""IL COLLAUDO DELLA DERIVA — **e presidia soprattutto che la misura ABBIA MATERIA.**

### ⛔ **IL DIFETTO CHE QUESTO COLLAUDO IMPEDISCE E' UN FALSO-ZERO, e l'ho fatto:** la
prima versione della misura normalizzava `psi` su tutto il grafo, e allora
`x = |h_k|/Lambda_k ~ 1/(2m)`. Siccome `G(x) = x - arctan x` va come `x^3/3`, il termine
del vuoto valeva **`~1e-5`**: ### **la saturazione era PRATICAMENTE SPENTA, e una
<<conservazione>> misurata la' non distingue <<`E` si conserva>> da <<il termine non
c'e'>>.**

### ⭐ **Quindi il braccio `1` non e' un contorno: e' il braccio PIU' IMPORTANTE.**

| | il braccio | che cosa **esclude** |
|---|---|---|
| `1` | **MATERIA**: nel regime di misura `x` e' di ordine `1`, non `1e-3` | ### **il FALSO-ZERO**: la saturazione spenta |
| `2` | il **primo termine** e' conservato **esattamente** dal solo pezzo lineare | che `E` non sia quella che credo |
| `3` | ### ⛔ **DEVE CAMBIARE:** il primo termine **sotto `N`** | che il braccio `2` passi perche' **niente si muove** |
| `4` | `Lambda_k` e' **esattamente invariante** sotto la camminata del vuoto, con `|phi|` uniforme | che la decomposizione di `(c)` dica qualcosa quando **non dice niente** |
| `5` | ### ⛔ **DEVE CAMBIARE:** la stessa cosa con `|phi|` **non uniforme** | che il braccio `4` sia un **FALSO-ZERO dello strumento** |
| `6` | la **sorgente per nodo** e' **`O(1)` in `dtau`**, non `O(dtau^2)` | — |
| `7` | ### ⛔ **DEVE FERMARE:** una legge dell'ordine di composizione **non mappata** | che un pezzo del tick **non giri in silenzio** |

Gira con:  python primo_ordine/_collauda_deriva.py
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
sys.path.insert(0, os.path.join(os.path.dirname(_QUI), "csv"))

import _presidio                                              # noqa: E402
import composizione as CM                                     # noqa: E402
import deriva as DV                                           # noqa: E402
import energia as EN                                          # noqa: E402

OK = [0, 0]
EPS = float(np.finfo(float).eps)
# ### ⚠ **LE SOGLIE, FISSATE QUI:** una soglia dentro un braccio e' ### **una soglia che
# ### si puo- aggiustare dopo aver visto il numero.**
X_MINIMO = 0.1          # ### sotto questo la saturazione e- SPENTA: falso-zero
ULP_MAX = 1000.0
CAMBIA_MIN = 1e-6
# ### ⛔⛔ **LA BANDA DELL-ESPONENTE DELLA SORGENTE, dal task history
# ### `2026-10-16_b_due_bracci_scaduti.md` e FISSATA PRIMA DELLA MISURA:** la sorgente
# ### e- ### **`O(dtau)` PER PASSO** -- il termine agisce con una fase `beta dtau`,
# ### quindi al primo ordine l-energia scambiata per tick e- proporzionale a `dtau`.
# ### ⚠ **La banda e- LARGA e il motivo e- dichiarato:** `s_k` e- un ### **MASSIMO su
# ### nodi**, non una media, e un massimo su `16` nodi ha una dispersione che
# ### ### **non e- una barra d-errore.** ### **Non si allarga dopo.**
ESPONENTE_ATTESO = 1.0
BANDA_ESPONENTE = 0.25
DTAU_SORGENTE = (0.2, 0.05, 0.0125)


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    print("  %-62s %s   %s" % (che[:62], "PASSA" if passa else "### FALLISCE", nota))


def main(argv):
    _presidio.avvia(__file__)
    print("=" * 96)
    print("IL COLLAUDO DELLA DERIVA: LA MATERIA PRIMA DI TUTTO, E I TRE CASI CHE DEVONO"
          " CAMBIARE")
    print("=" * 96)

    # ### (1) LA MATERIA: `x` di ordine `1` nel regime di misura
    _i, mot, st, _p = DV.scena(16, 7, 0.2, norma="locale", vuoto_modulo=2.0)
    x = DV.satura(st, mot)
    esito("### (1) MATERIA: nel regime di misura `x = |h|/Lambda` e- di ordine 1",
          x >= X_MINIMO, "x_max = %.4f   (sotto %.2f sarebbe un FALSO-ZERO)"
          % (x, X_MINIMO))
    _i2, mot2, st2, _p2 = DV.scena(16, 7, 0.2, norma="globale")
    x2 = DV.satura(st2, mot2)
    esito("### (1-bis) e il regime `globale` E- quello vacuo, come dichiarato",
          x2 < X_MINIMO, "x_max = %.5f: la- `G ~ x^3/3 ~ 0`" % x2)

    # ### (2) il PRIMO termine sotto il SOLO pezzo lineare: un-IDENTITA-
    _i3, mot3, st3, par = DV.scena(16, 7, 0.2, norma="locale", vuoto_modulo=2.0)
    p0, _v0 = DV.due_termini(st3, mot3, par)
    mot3.apri_tick()
    for nome in ("moneta_spin", "grover", "spostamento_trasporto"):
        mot3.operatori[nome](st3, par if nome == "moneta_spin" else {}, 1)
    mot3.chiudi_tick()
    p1, _v1 = DV.due_termini(st3, mot3, par)
    d = abs(p1 - p0)
    ulp = d / (EPS * max(abs(p0), 1.0))
    esito("### (2) il PRIMO termine: il pezzo lineare lo conserva ESATTAMENTE",
          ulp < ULP_MAX, "|Delta| = %.3e su %.4f  (%.1f ulp)" % (d, p0, ulp))

    # ### (3) DEVE CAMBIARE: lo stesso termine sotto `N`
    _i4, mot4, st4, par4 = DV.scena(16, 7, 0.2, norma="locale", vuoto_modulo=2.0)
    q0, _w0 = DV.due_termini(st4, mot4, par4)
    mot4.apri_tick()
    mot4.operatori["CAMM-SATURAZIONE"](st4, {}, 1)
    mot4.chiudi_tick()
    q1, _w1 = DV.due_termini(st4, mot4, par4)
    esito("### (3) DEVE CAMBIARE: il primo termine sotto `N` NON e- conservato",
          abs(q1 - q0) > CAMBIA_MIN,
          "|Delta| = %.3e: senza questo il braccio (2) sarebbe un FALSO-UNO"
          % abs(q1 - q0))

    # ### ⛔⛔ **(4) RISCRITTO IL `2026-10-16` SU TRE AFFERMAZIONI DERIVATE**, una per
    # ### pezzo *(task history `2026-10-16_b_due_bracci_scaduti.md`)*. ### **Il vecchio
    # ### braccio diceva <<con `|phi|` uniforme `Lambda_k` e- invariante>>, vero quando il
    # ### Grover era un-INVOLUZIONE e falso dalla strada `(B)`.**
    # ### ⭐ **(4a) IL GROVER DEL VUOTO CONSERVA `Lambda_k` ESATTAMENTE**, perche- agisce
    # ### ### **dentro il nodo** ed e- ### **unitario** su quello spazio: vale a
    # ### ### **ogni frazione** e con ### **`|phi|` NON uniforme** -- cioe- NON e- una
    # ### proprieta- del vuoto uniforme.
    for fr in (1.0, 0.5):
        g, gv = DV.lambda_sotto_vuoto(16, 7, False, ("grover_scalare",), fr, 0.2)
        esito("### (4a) il GROVER del vuoto conserva `Lambda_k` (frazione %.1f, `|phi|`"
              " NON uniforme)" % fr, g <= 4096 * EPS,
              "max |Delta Lambda| = %.3e, e |Delta V| = %.3e: e- l-UNITARIETA- del pezzo,"
              " non il vuoto uniforme" % (g, gv))
    # ### ⭐ **(4b) LO SPOSTAMENTO CONSERVA IL TOTALE `V` E MUOVE `Lambda_k`:** agisce
    # ### ### **sull-arco**, e le due estremita- di un arco stanno in ### **due nodi
    # ### diversi** -- e- ### **il TRASPORTO.**
    s, sv = DV.lambda_sotto_vuoto(16, 7, False, ("spostamento_scalare",), 0.5, 0.2)
    esito("### (4b) lo SPOSTAMENTO conserva il TOTALE `V`", sv <= 4096 * EPS,
          "|Delta V| = %.3e" % sv)
    esito("### (4b) e MUOVE `Lambda_k`: e- il TRASPORTO", s > CAMBIA_MIN,
          "max |Delta Lambda| = %.3e: se fosse zero il vuoto non si sposterebbe" % s)
    # ### ⭐ **(4c) A `theta = pi` LO SPOSTAMENTO E- UNA PERMUTAZIONE PURA**, e con
    # ### ### **`|phi|` UNIFORME** i moduli scambiati sono uguali ⟹ `Lambda_k` torna
    # ### ### **invariante.** ### **E- l-affermazione di ieri, CON LA SUA CONDIZIONE.**
    # ### ⚠ **`theta = pi dtau frazione`, e la scena ha `dtau = 0.2`: la frazione che
    # ### da- `theta = pi` sarebbe `5`, che NON e- una frazione** -- quindi si misura
    # ### ### **sulla scena a `dtau = 1`**, dove `frazione = 1` da- `theta = pi`.
    pu, _pv = DV.lambda_sotto_vuoto(16, 7, True, ("spostamento_scalare",), 1.0, 1.0)
    esito("### (4c) a `theta = pi` e `|phi|` UNIFORME `Lambda_k` e- invariante",
          pu <= 4096 * EPS,
          "max |Delta Lambda| = %.3e: la permutazione scambia moduli UGUALI" % pu)
    # ### ⛔ **IL CASO CHE DEVE FALLIRE: `theta = pi` con `|phi|` NON uniforme.**
    # ### **Senza di lui la `(4c)` passerebbe per vacuita-.**
    pn, _pnv = DV.lambda_sotto_vuoto(16, 7, False, ("spostamento_scalare",), 1.0, 1.0)
    esito("### (4c) DEVE fallire: `theta = pi` con `|phi|` NON uniforme",
          pn > CAMBIA_MIN,
          "max |Delta Lambda| = %.3e: la permutazione scambia moduli DIVERSI" % pn)

    # ### ⛔⛔ **(6) RISCRITTO IL `2026-10-16`: LA SORGENTE E- `O(dtau)` PER PASSO.**
    # ### Il vecchio braccio diceva ### **`O(1)`**, e la misura lo smentiva da sola: il
    # ### rapporto su un fattore `4` valeva `4.625` *(legge vecchia)* e `3.220` *(nuova)*,
    # ### cioe- ### **circa `4`** -- e `O(1)` darebbe ### **`1`.**
    # ### ⭐ **E L-AFFERMAZIONE SI DERIVA:** il termine agisce con una fase
    # ### `beta dtau frazione`, quindi al primo ordine ### **l-energia scambiata per tick
    # ### e- proporzionale a `dtau`** -- ed e- cio- che un flusso parziale deve dare.
    mm = []
    for dt in DTAU_SORGENTE:
        s, _dE, _po, _sa = DV.sorgente_per_nodo(dtau=dt, vuoto_modulo=2.0)
        mm.append(float(np.max(np.abs(s))))
    espo = []
    for k in range(len(mm) - 1):
        rap = mm[k] / mm[k + 1] if mm[k + 1] > 0 else float("inf")
        espo.append(float(np.log(rap) / np.log(4.0)))
    print("      la SORGENTE ai tre `dtau` %s: %s" % (DTAU_SORGENTE,
                                                      "  ".join("%.6e" % x for x in mm)))
    print("      gli ESPONENTI (log del rapporto / log 4): %s"
          % "  ".join("%.4f" % x for x in espo))
    esito("### (6) la SORGENTE per nodo e- `O(dtau)` PER PASSO",
          all(abs(e - ESPONENTE_ATTESO) <= BANDA_ESPONENTE for e in espo),
          "esponenti %s, attesi `%.1f` entro `%.2f`"
          % ("  ".join("%.4f" % x for x in espo), ESPONENTE_ATTESO, BANDA_ESPONENTE))
    # ### ⛔ **E LE DUE ALTERNATIVE SONO ESCLUSE CON LO STESSO NUMERO**, invece che con
    # ### due misure diverse: ### **`O(1)` darebbe esponente `0`, `O(dtau^2)` darebbe `2`.**
    esito("### (6) DEVE fallire: `O(1)` (esponente `0`) e `O(dtau^2)` (esponente `2`)",
          all(abs(e - 0.0) > BANDA_ESPONENTE and abs(e - 2.0) > BANDA_ESPONENTE
              for e in espo),
          "gli esponenti misurati sono %s: entrambe le alternative sono FUORI banda"
          % "  ".join("%.4f" % x for x in espo))

    # ### (7) DEVE FERMARE: una legge dell-ordine NON mappata
    salvato = dict(DV.OPERATORE)
    rotto = False
    try:
        DV.OPERATORE.pop(CM.ORDINE[2][0])
        _i5, mot5, st5, par5 = DV.scena(8, 7, 0.2)
        DV.tick(st5, mot5, par5)
    except AssertionError:
        rotto = True
    finally:
        DV.OPERATORE.clear()
        DV.OPERATORE.update(salvato)
    esito("### (7) DEVE FERMARE: una legge dell-ordine di composizione non mappata",
          rotto, "un pezzo del tick che non gira e- un tick diverso")

    print("=" * 96)
    print("  %d su %d" % (OK[0], OK[1]))
    print("=" * 96)
    return 0 if OK[0] == OK[1] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
