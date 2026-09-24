# -*- coding: utf-8 -*-
"""REPERTO -- **`d >= LAM` SENZA IL FRENO: la legge regge PERCHE' UNA CURA E' ACCESA.**

Il sigillo `_sigillo_chicoop.py` **SI SCHIANTA** sul blob di oggi: `DominioViolato` su `d`,
**`223 396` archi su `526 047` -- il `42.5 %` -- sotto `LAM` gia' al passo 1**.

**La sua argv e' ferma a prima che le cure esistessero:** non ha `--scala-min-passo`, ne'
`--peq-esatto`, ne' le altre. E' **la stessa famiglia** del difetto gia' catalogato in
`CLAUDE.md` -- *l'argv di `_sigillo_strato1.py` non conteneva `--cs-dinamico`, quindi il
`23/23` non aveva mai esercitato la dipendenza da `cs`*.

**QUI NON SI SUPPONE: SI MISURA.** Due bracci, **stessa scena, stesso seme, stesso blob**:
  * `SENZA` -- l'argv del sigillo di `CHI_COOP`, come sta scritta oggi;
  * `CON`   -- la stessa argv **piu' le cure che il driver accende** *(decisione di Luca,
              2026-09-24: `NUDA = CAMPAGNA`)*.

**Un passo di motore. Nessuna scena lunga.**
ASCII puro.
"""
import io
import os
import subprocess
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
DEST = os.path.join(_QUI, "_sig_cura2", "REPERTO_lam_senza_freno.txt")

BASE = ["soliton_simulator.py", "--test", "N-MASSE", "--nmasse", "3", "--sep", "4.0",
        "--giri", "0", "--campo-spinoriale", "--spinore-vivo", "--spinore-corretto",
        "--chi-core", "--calore-scal", "--deparam-orologio", "--verlet", "--fork-su2",
        "--fork-su2-mem", "--cs-dinamico", "--tau-luce", "--rumore-colorato",
        "--pav-com", "--guscio-morbido", "--zeta-vir", "--chi-basc", "--plast-din",
        "--viriale", "--olon-part"]
# le cure che il driver accende, e che l'argv del sigillo NON ha
CURE = ["--scala-min-passo", "--peq-esatto", "--peq-nascita-locale", "--coes-causale",
        "--anom-simm", "--coes-adim", "--ritmo-wrap-2pi", "--tempo-unico-mitosi"]

FIGLIO = r'''
import sys, numpy as np
sys.argv = ARGV
import soliton_simulator as S
a = S._cli(); S._applica_regime(a); S._applica_flag(a)
S._NMASSE_VIDEO["n"] = 3; S._NMASSE_VIDEO["sep"] = 4.0; S._NMASSE_VIDEO["size"] = None
S.avvia_test("N-MASSE")
net = S.rete
np.random.seed(42)
try:
    net.step(); net.mitosi(); net.rilassa_disegno(); net.memoria_hebbiana_moto()
    esito = "NESSUNA VIOLAZIONE"
except Exception as ex:
    esito = "VIOLATO: %s" % (str(ex).splitlines()[0],)
d = np.asarray(net.d, dtype=float)
sotto = int(np.sum(d < S.LAM))
print("RIS %s | LAM %.6f | archi %d | sotto LAM %d (%.2f %%) | min(d)/LAM %.6f"
      % (esito, S.LAM, d.size, sotto, 100.0 * sotto / max(d.size, 1),
         float(d.min()) / S.LAM))
'''


def gira(nome, argv, P):
    src = "ARGV = %r\n" % (argv,) + FIGLIO
    r = subprocess.run([sys.executable, "-c", src], cwd=RADICE, capture_output=True,
                       text=True, encoding="utf-8", errors="replace")
    riga = ""
    for x in (r.stdout or "").splitlines():
        if x.startswith("RIS "):
            riga = x[4:]
    if not riga:
        riga = "*** il braccio e' morto (rc=%d): %s" % (
            r.returncode, ((r.stdout or "") + (r.stderr or "")).strip().splitlines()[-1:])
    P("  %-7s %s\n" % (nome, riga))
    return riga


def main():
    f = io.open(DEST, "w", encoding="utf-8", newline="\n")

    def P(s):
        sys.stdout.write(s)
        f.write(s)

    P("# REPERTO -- `d >= LAM` SENZA IL FRENO\n#\n")
    P("# Due bracci, STESSA SCENA, STESSO SEME, STESSO BLOB. Un passo di motore.\n")
    P("# SENZA = l'argv del sigillo di `CHI_COOP` come sta scritta oggi\n")
    P("# CON   = la stessa piu' le cure che il driver accende\n#\n")
    a = gira("SENZA", BASE, P)
    b = gira("CON", BASE + CURE, P)
    P("\n  cure aggiunte nel braccio CON: %s\n" % " ".join(CURE))
    P("\n" + "=" * 92 + "\nCOME SI LEGGE\n" + "=" * 92 + "\n")
    if "NESSUNA" in b and "VIOLATO" in a:
        P("  ❗ **LA LEGGE `d >= LAM` REGGE PERCHE' UNA CURA E' ACCESA.**\n")
        P("     Senza le cure la legge e' violata **su quasi meta' degli archi al passo 1**;\n")
        P("     con le cure non e' violata affatto. **Non e' una proprieta' del sistema: e'\n")
        P("     una CONSEGUENZA DI UN FLAG.**\n")
        P("\n  -> ed e' esattamente cio' che la decisione di Luca su `LAM` STRUTTURALE dice:\n")
        P("     *«nessuna lunghezza sotto `LAM` deve diventare STRUTTURALE, non un freno che\n")
        P("     ci arriva»*. **Qui si vede il costo della realizzazione di oggi.**\n")
        P("\n  -> E IL SIGILLO DI `CHI_COOP` NON E' ROTTO: e' la sua ARGV a essere ferma a\n")
        P("     prima che le cure esistessero. **Stessa famiglia del `23/23` dello Strato 1\n")
        P("     che non aveva mai esercitato `cs`.** Si aggiorna l'argv, non si spegne\n")
        P("     l'invariante: spegnerlo sarebbe nascondere la misura.\n")
    else:
        P("  ⚠ L'ESITO NON E' QUELLO ATTESO, e va letto prima di concludere.\n")
        P("     SENZA: %s\n     CON:   %s\n" % (a, b))
    P("\n!! LIMITE: UN passo, UN seme, UNA scena. Dice CHE la legge dipende dal flag,\n")
    P("   non di quanto il difetto cresca nel tempo.\n")
    f.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
