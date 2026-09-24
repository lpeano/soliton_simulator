# -*- coding: utf-8 -*-
"""`massa_critica_collasso` -- **CHI LA USA.** Elenco GENERATO dall'AST. **Non si tocca.**

`A13`: *«`LAM` e' la scala di Planck del sistema»*, e la conseguenza 4 dice che **qualunque
costante tarata su un numero di nodi entro un raggio `< LAM` e' tarata SOTTO la scala di
Planck**.

`massa_critica_collasso()` chiede **~`621` nodi in una sfera di raggio `LAM`**. Con distanza
minima `LAM` **ne entra circa una dozzina**: il conto e' geometrico e sta nel referto.

> **DECISIONE DI LUCA: si MARCA e NON SI TOCCA.** Questa sonda **elenca chi la usa**, cosi' la
> marcatura ha un perimetro invece di essere un'avvertenza generica.

Sola lettura, nessun run. `P1-ter`.
ASCII puro.
"""
import ast
import io
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
SORGENTE = os.path.join(RADICE, "soliton_simulator.py")
DEST = os.path.join(_QUI, "_revisione", "USI_massa_critica.txt")
NOMI = ("massa_critica_collasso", "massa_critica_adattiva")


def main():
    try:
        os.makedirs(os.path.dirname(DEST))
    except OSError:
        pass
    f = io.open(DEST, "w", encoding="utf-8", newline="\n")

    def P(s):
        sys.stdout.write(s)
        f.write(s)

    src = io.open(SORGENTE, encoding="utf-8").read()
    alb = ast.parse(src)
    righe = {}
    for n in ast.walk(alb):
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for r in range(n.lineno, (n.end_lineno or n.lineno) + 1):
                righe.setdefault(r, n.name)
    usi = []
    for n in ast.walk(alb):
        if isinstance(n, ast.Name) and n.id in NOMI:
            usi.append((n.lineno, n.id, righe.get(n.lineno, "(modulo: SCENE)")))
    usi.sort()

    P("# `massa_critica_collasso` -- CHI LA USA. Elenco GENERATO dall'AST.\n#\n")
    P("# `A13` conseguenza 4: una costante tarata entro un raggio < LAM e' tarata SOTTO la\n")
    P("# scala di Planck. **DECISIONE DI LUCA: SI MARCA E NON SI TOCCA.**\n#\n")

    # il conto geometrico, DERIVATO e non ricopiato
    sys.path.insert(0, RADICE)
    import soliton_simulator as S
    import numpy as np
    Nc = float(S.massa_critica_collasso())
    LAM = float(S.LAM)
    # IL MIO PRIMO CONTO ERA SBAGLIATO, e il numero di Luca era giusto.
    #   Avevo usato l'impacchettamento di KEPLER: palline di raggio LAM/2 dentro una sfera di
    #   raggio LAM -> `8 * 0.740480 = 5.92`. **Kepler pretende le palline INTERAMENTE DENTRO**,
    #   che e' una condizione PIU' STRETTA di quella vera: qui il vincolo e' solo sui CENTRI.
    #   IL PROBLEMA VERO: quanti PUNTI stanno in una palla di raggio `LAM` con distanze mutue
    #   `>= LAM`? Se uno sta al centro, gli altri devono stare a distanza `>= LAM` da lui e
    #   `<= LAM` dal centro: quindi **esattamente sulla sfera di raggio `LAM`**, con
    #   separazione angolare `>= 60 gradi`. Il massimo su una sfera con separazione
    #   `>= 60 gradi` e' il **NUMERO DI BACIO** in 3D, `K(3) = 12`.
    #   **Quindi al piu' `12 + 1 = 13`** -- ed e' la "circa una dozzina" di Luca, ESATTA.
    n_max = 13.0
    dens_kepler = np.pi / (3.0 * np.sqrt(2.0))     # resta, per mostrare il conto SBAGLIATO
    n_kepler = dens_kepler * 8.0
    P("IL CONTO, derivato e non ricopiato:\n")
    P("  massa_critica_collasso() = %.4f  nodi, chiesti in una sfera di raggio LAM = %.6f\n"
      % (Nc, LAM))
    P("  IL PROBLEMA: quanti PUNTI stanno in una palla di raggio LAM con distanze mutue >= LAM?\n")
    P("  Se uno sta al centro, gli altri devono stare a distanza >= LAM da lui e <= LAM dal\n")
    P("  centro: quindi ESATTAMENTE sulla sfera di raggio LAM, con separazione angolare >= 60\n")
    P("  gradi. Il massimo su una sfera con separazione >= 60 gradi e' il NUMERO DI BACIO in\n")
    P("  3D, K(3) = 12. Quindi al piu' 12 + 1 = %d.\n" % int(n_max))
    P("  RAPPORTO CHIESTO / POSSIBILE = %.2f\n" % (Nc / n_max))
    P("\n  -> **la costante chiede ~%.0f volte piu' nodi di quanti ne stiano.**\n" % (Nc / n_max))
    P("\n  !! IL MIO PRIMO CONTO ERA SBAGLIATO, E IL NUMERO DI LUCA ERA GIUSTO.\n")
    P("     Avevo usato l'impacchettamento di KEPLER -- palline di raggio LAM/2 dentro una\n")
    P("     sfera di raggio LAM -> 8 * %.6f = %.4f. **Kepler pretende le palline INTERAMENTE\n"
      % (dens_kepler, n_kepler))
    P("     DENTRO, che e' una condizione PIU' STRETTA di quella vera**: qui il vincolo e' solo\n")
    P("     sui CENTRI. Il mio numero (%.2f) era TROPPO PICCOLO di ~%.1f volte, e la \"circa\n"
      % (n_kepler, n_max / n_kepler))
    P("     una dozzina\" di Luca e' ESATTA.\n")
    P("     **Il conto sbagliato resta stampato, col perche': un errore cancellato non insegna\n")
    P("     niente, e chi rifara' il conto rischia di rifare il mio.**\n")

    P("\n" + "=" * 100 + "\nCHI LA USA -- %d usi\n" % len(usi) + "=" * 100 + "\n")
    scene = [u for u in usi if u[2].startswith("(modulo")]
    codice = [u for u in usi if not u[2].startswith("(modulo")]
    P("\n-- NEL CODICE DELLA FISICA (%d) --\n" % len(codice))
    for l, nm, fu in codice:
        P("  :%-6d %-26s in  %s\n" % (l, nm, fu))
    P("\n-- NELLE SCENE / TAVOLA DEI TEST (%d), a livello di modulo --\n" % len(scene))
    for l, nm, fu in scene:
        P("  :%-6d %-26s\n" % (l, nm))

    P("\n" + "=" * 100 + "\nCOME SI LEGGE\n" + "=" * 100 + "\n")
    P("  **Gli usi NELLE SCENE decidono QUANTI nodi seminare**: sono la taglia delle masse.\n")
    P("  **Gli usi NELLA FISICA la usano come SOGLIA o come SCALA** -- ed e' li' che il fatto\n")
    P("  di essere tarata sotto la scala di Planck **entra nelle leggi**.\n")
    P("\n  ⚠ **NON SI TOCCA NIENTE** (decisione di Luca). Questo elenco e' il PERIMETRO della\n")
    P("  marcatura: una costante marcata senza l'elenco di chi la usa e' un'avvertenza\n")
    P("  generica, e un'avvertenza generica non impedisce nulla (`A9`).\n")
    f.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
