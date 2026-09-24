# -*- coding: utf-8 -*-
"""QUANTE VOLTE SCATTA IL FALLBACK `:3394`, quello che fa entrare `phi` nell'orologio.

Mandato di Luca, 2026-09-24. **NON MODIFICA IL SIMULATORE**: avvolge `calcola_psi` e valuta
la condizione del fallback PRIMA di ogni chiamata, poi esegue il metodo originale.

PERCHE' CONTA: il ramo VIVO di `ritmo()` (`:2628-2629`) legge `psi_spin`, e `psi_spin` e'
costruito a `:3398` dallo SNAPSHOT `_psi_spinor`. **L'orologio viene dallo SPINORE, non da
`phi`** -- con UNA eccezione: il fallback di `:3393-3394`,

    if _psp is None or len(_psp) < _n:
        _psp = np.zeros((_n, 2), complex); _psp[:, 0] = np.exp(1j * self.phi[:_n])

che e' **l'unico punto in cui `phi` entra nella catena dell'orologio**. Se scattasse spesso,
l'orologio verrebbe da `phi` **quasi sempre**, e il grafo della mappa andrebbe letto al
contrario. **E' `P5`: un fallback mai misurato e' un comportamento SCONOSCIUTO.**

⚠ E IL PRECEDENTE E' GROSSO: `_cs_nodo_prev` scattava nel **71.88 %** delle chiamate e
  `_psi_spin_prec` nel **95.33 %**, per mesi, in silenzio. La domanda non e' retorica.

SOLA LETTURA sul simulatore (il file non si tocca). Gira un giro CORTO in-process.
ASCII PURO.
"""
import io
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, RADICE)

PASSI = int(os.environ.get("SONDA_PASSI", "30"))

# l'ARGV del driver, VERBATIM da `csv/_test_fork/_scena_video.py:185-199` piu' il `COMUNE`
# di `_g4_prova.py`: si riproduce la configurazione dei run, non una inventata.
ARGV = ["soliton_simulator.py", "--test", "N-MASSE", "--nmasse", "3", "--sep", "4.0",
        "--giri", "0", "--campo-spinoriale", "--spinore-vivo", "--spinore-corretto",
        "--chi-core", "--calore-scal", "--deparam-orologio", "--verlet", "--fork-su2",
        "--fork-su2-mem", "--cs-dinamico", "--tau-luce", "--rumore-colorato",
        "--pav-com", "--guscio-morbido", "--zeta-vir", "--chi-basc", "--chi-coop",
        "--coes-adim", "--peq-esatto", "--peq-nascita-locale", "--scala-min-passo",
        "--coes-causale", "--anom-simm", "--invarianti=on", "--plast-din", "--viriale",
        "--olon-part"]


def main():
    W = sys.stdout.write
    W("# QUANTE VOLTE SCATTA IL FALLBACK `:3394` (`phi` nell'orologio)\n#\n")
    W("# passi: %d   (SONDA_PASSI per cambiarlo)\n#\n" % PASSI)

    import soliton_simulator as S
    vecchio = list(sys.argv)
    sys.argv = list(ARGV)
    try:
        a = S._cli()
        S._applica_regime(a)
        S._applica_flag(a)
    finally:
        sys.argv = vecchio
    S._NMASSE_VIDEO["n"] = 3
    S._NMASSE_VIDEO["sep"] = 4.0
    S._NMASSE_VIDEO["size"] = None
    S.avvia_test("N-MASSE")()
    net = S.net
    W("scena avviata: n = %d\n\n" % net.n)

    conta = {"chiamate": 0, "fallback": 0, "assente": 0, "corto": 0,
             "quando": [], "forma": []}
    orig = type(net).calcola_psi

    def _wrap(self, *args, **kw):
        # LA STESSA CONDIZIONE DI `:3393`, valutata PRIMA della chiamata. Pure-read.
        if S.CAMPO_SPINORIALE:
            conta["chiamate"] += 1
            _psp = getattr(self, "_psi_spinor", None)
            if _psp is None:
                conta["fallback"] += 1
                conta["assente"] += 1
                conta["quando"].append(conta["chiamate"])
                conta["forma"].append((-1, self.n))
            elif len(_psp) < self.n:
                conta["fallback"] += 1
                conta["corto"] += 1
                conta["quando"].append(conta["chiamate"])
                conta["forma"].append((len(_psp), self.n))
        return orig(self, *args, **kw)

    type(net).calcola_psi = _wrap
    try:
        for _ in range(PASSI):
            S.passo_test()
            for _k in range(int(S.PASSI_PER_FRAME)):
                S.scuoti_vuoto(net)
                net.step()
                net.mitosi()
                net.rilassa_disegno()
                net.memoria_hebbiana_moto()
    finally:
        type(net).calcola_psi = orig

    c, fb = conta["chiamate"], conta["fallback"]
    W("=" * 96 + "\n")
    W("IL FALLBACK `:3394` -- `_psi_spinor` assente o piu' corto di `n`\n")
    W("=" * 96 + "\n")
    W("  invocazioni di `calcola_psi` con `CAMPO_SPINORIALE` acceso   %8d\n" % c)
    W("  di cui il FALLBACK e' scattato                               %8d   (%.4f %%)\n"
      % (fb, (100.0 * fb / c) if c else float("nan")))
    W("     perche' `_psi_spinor` era ASSENTE (`None`)                %8d\n" % conta["assente"])
    W("     perche' era piu' CORTO di `n`                             %8d\n" % conta["corto"])
    if conta["quando"]:
        W("  QUANDO (indici delle prime 12 invocazioni saltate): %s\n"
          % ", ".join(str(x) for x in conta["quando"][:12]))
        W("  FORMA al fallimento (len(_psi_spinor), n), prime 6: %s\n"
          % ", ".join("(%d, %d)" % f for f in conta["forma"][:6]))
        W("  ULTIMA invocazione saltata: %d su %d\n" % (conta["quando"][-1], c))
    W("  n finale: %d\n" % net.n)
    W("\n")
    W("COME SI LEGGE, e il criterio e' scritto qui perche' non ci sono soglie da scegliere:\n")
    if fb == 0:
        W("  *** ZERO: `phi` NON entra MAI nella catena dell'orologio. Il grafo va corretto:\n")
        W("      l'orologio viene dallo SPINORE, e la freccia `phi -> TEMPI` sparisce. ***\n")
    elif conta["quando"] and conta["quando"][-1] <= 3:
        W("  *** SOLO ALL'AVVIO (ultima invocazione saltata: %d): e' il transitorio del primo\n"
          % conta["quando"][-1])
        W("      passo, quando `_psi_spinor` non esiste ancora. Legittimo, e NON cambia il\n")
        W("      grafo: a regime l'orologio viene dallo SPINORE. ***\n")
    else:
        W("  *** SPARSO SU TUTTO IL RUN: `phi` entra nell'orologio in modo NON transitorio,\n")
        W("      e il grafo NON si corregge come previsto. E' un reperto, non una nota. ***\n")
    W("\n!! LIMITE: UN seme, UNA scena, %d passi, e la sonda gira IN-PROCESS -- non e' un run\n"
      % PASSI)
    W("   del driver. Il conteggio e' del PERCORSO, non di una campagna.\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
