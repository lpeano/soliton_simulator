# -*- coding: utf-8 -*-
"""**MISURA 0 di `DRIVER-SCENA-II`: che cosa fa il driver OGGI con la scena `(ii)`.**

*(Primo punto del TODO di `doc/TASK_HISTORY/2026-09-26_driver-scena-ii.md`, **committato prima**.
E' il **termine di paragone del criterio 2**: senza di esso, dopo la cura non si saprebbe **da
che cosa** si e' guariti -- `STANDARD 5` applicato al proprio punto di partenza.)*

**NON CURA NIENTE. MISURA.** Tre cose, e ognuna con la sua risposta attesa scritta **prima**:

| | che cosa misura | atteso, scritto PRIMA |
|---|---|---|
| **`M0a`** | `net.n` dopo `_applica_flag` con l'argv del driver **e `--nodi 0`** | **> 0**: il ternario `-1 if SEMINA_LAM else a.nodi` **ignora `a.nodi`** |
| **`M0b`** | che cosa fa la scena `(ii)` su quella rete | **`SystemExit`** di `_semina_masse_coerenti`: *«LA RETE HA GIA' ... NODI»* |
| **`M0c`** | che cosa fa la scena `N-MASSE` con `SEMINA_LAM` *(il presidio da non rompere)* | **`SystemExit`** di `_massa`: *«SCENA DI EPOCA PRE-`A13`»* |

**Passa dal CLI** (`csv/_cli_flag.py`): l'argv e' **quella del driver**, catturata eseguendone il
testo fino all'ancora, **non ricostruita a mano** (`H-P3`).

    python csv/_test_fork/_misura0_scena_ii.py

ASCII puro.
"""
import io
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, os.path.join(RADICE, "csv"))

import _presidio                                                       # noqa: E402
import _cli_flag                                                       # noqa: E402

_presidio.avvia(__file__)

NL = chr(10)
DEST = os.path.join(_QUI, "_misura0_scena_ii.txt")
R = []


def P(s=""):
    print(s)
    R.append(s)


def _swap(argv, scena, nodi):
    """L'argv del driver con la SCENA cambiata e `--nodi` aggiunto. Asserita per se'."""
    fuori = list(argv)
    if "--test" not in fuori:
        raise SystemExit("l'argv del driver non contiene `--test`: e' cambiato il driver")
    fuori[fuori.index("--test") + 1] = scena
    if "--nodi" in fuori:
        fuori[fuori.index("--nodi") + 1] = str(nodi)
    else:
        fuori += ["--nodi", str(nodi)]
    return fuori


def prova(argv, scena, nodi):
    """`(n_dopo_flag, esito, messaggio)` per una scena. `esito` e' 'PARTE' o 'SystemExit'."""
    a2 = _swap(argv, scena, nodi)
    S2, _a = _cli_flag.carica_dal_cli(a2, nome="sim_m0_%s" % scena.replace("-", "_").lower())
    n_dopo = int(S2.net.n)
    try:
        S2.avvia_test(scena)()
        return n_dopo, "PARTE", "(nessun rifiuto)"
    except SystemExit as e:
        return n_dopo, "SystemExit", str(e)


if __name__ == "__main__":
    P("=" * 104)
    P("MISURA 0 -- `DRIVER-SCENA-II`: che cosa fa il driver OGGI con la scena (ii)")
    P("=" * 104)
    S, argv = _cli_flag.argv_del_driver()
    P("  argv del driver: %d elementi, catturata dal TESTO del driver (non ricostruita)"
      % len(argv))
    _cli_flag.dichiara_configurazione(S, P)

    esiti = []

    n_a, es_a, msg_a = prova(argv, "MASSE-COERENTI", 0)
    P("")
    P("  M0a  net.n dopo `_applica_flag` con `--nodi 0` ..... %d" % n_a)
    P("       atteso > 0 (il ternario ignora `a.nodi` con SEMINA_LAM) -> %s"
      % ("COME ATTESO" if n_a > 0 else "*** NON come atteso ***"))
    esiti.append(("M0a  `--nodi 0` NON e' rispettato", n_a > 0))
    P("")
    P("  M0b  la scena (ii) su quella rete ................. %s" % es_a)
    for r in msg_a.strip().split(NL)[:4]:
        P("         %s" % r)
    ok_b = (es_a == "SystemExit" and "HA GIA'" in msg_a)
    P("       atteso: SystemExit «LA RETE HA GIA' ... NODI» -> %s"
      % ("COME ATTESO" if ok_b else "*** NON come atteso ***"))
    esiti.append(("M0b  la scena (ii) RIFIUTA la rete non vuota", ok_b))

    n_c, es_c, msg_c = prova(argv, "N-MASSE", 0)
    P("")
    P("  M0c  la scena N-MASSE con SEMINA_LAM ............... %s" % es_c)
    for r in msg_c.strip().split(NL)[:3]:
        P("         %s" % r)
    ok_c = (es_c == "SystemExit" and "PRE-" in msg_c)
    P("       atteso: SystemExit «SCENA DI EPOCA PRE-`A13`» -> %s"
      % ("COME ATTESO" if ok_c else "*** NON come atteso ***"))
    esiti.append(("M0c  N-MASSE rifiuta (presidio da NON rompere)", ok_c))

    P("")
    P("=" * 104)
    for nome, ok in esiti:
        P("  %-46s %s" % (nome, "COME ATTESO" if ok else "** DIVERSO DALL'ATTESO **"))
    buoni = len([1 for _n, o in esiti if o])
    P("MISURA 0: %d/%d come atteso" % (buoni, len(esiti)))
    P("=" * 104)
    P()
    P("COSA QUESTA MISURA *NON* DICE:")
    P("  - **non dice che la cura sia quella riga**: dice che il vuoto c'e' PRIMA della scena e")
    P("    che la scena lo rifiuta. Che il punto sia `net.semina(-1 if SEMINA_LAM else a.nodi)`")
    P("    e' una LETTURA del codice, e la prova sara' il criterio 2 del sigillo.")
    P("  - **non misura quanti nodi** faccia la saturazione in generale: quel numero dipende dal")
    P("    seme, e il seme qui e' quello che il driver non puo' cambiare (42).")
    io.open(DEST, "w", encoding="utf-8", newline=NL).write(NL.join(R) + NL)
    print(NL + "scritto %s" % os.path.relpath(DEST, RADICE).replace(chr(92), "/"))
    sys.exit(0 if buoni == len(esiti) else 1)
