# -*- coding: utf-8 -*-
"""REVISIONE (1) -- **L'AVVIO: quale tempo usa ogni legge nei primi passi.**

Tre domande di Luca, e si misurano, non si deducono:
  a) `ritmo()` torna `r = 1` per tutti al primo passo -- **quante volte e fino a quando**;
  b) il **fallback `exp(i phi)` di `psi_spin`** -- quando scatta, e **cosa legge `phi`** li';
  c) la **SEMINA al passo zero** -- quanti archi con `d < LAM`, `min(d)/LAM`, e **quanti
     portati a `LAM` dal troncone alla nascita** (`_nasce`).

⚠ **PURE-READ (par.2.3):** l'involucro su `calcola_psi` **CONTA e basta** -- non tocca stato ne'
RNG. Chiama la funzione vera e ne restituisce il risultato.

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
DEST = os.path.join(_QUI, "_revisione", "AVVIO.txt")
PASSI = 4

FIGLIO = r'''
import sys, numpy as np
sys.argv = ARGV
import soliton_simulator as S
a = S._cli(); S._applica_regime(a); S._applica_flag(a)
S._NMASSE_VIDEO["n"] = 3; S._NMASSE_VIDEO["sep"] = 4.0; S._NMASSE_VIDEO["size"] = None
S.avvia_test("N-MASSE")()
net = S.net
S.stato["nframe"] = 0

# --- (c) LA SEMINA AL PASSO ZERO, prima di qualunque passo
d = np.asarray(net.d, dtype=float)
eq = int(np.sum(d == S.LAM))
print("SEM archi=%d  sotto_LAM=%d  min/LAM=%.6f  esattamente_LAM=%d  nascite=%s  SCALA_MIN=%s  SCALA_MIN_PASSO=%s"
      % (d.size, int(np.sum(d < S.LAM)), float(d.min())/S.LAM, eq,
         getattr(net, "_g_sm_nascite", 0), S.SCALA_MIN, S.SCALA_MIN_PASSO))

# --- (b) INVOLUCRO PURE-READ su calcola_psi: conta il fallback dello SPINORE
_vero = S.Rete.calcola_psi
_reg = []
def _wrap(self, w=None):
    _psp = getattr(self, "_psi_spinor", None)
    corto = (_psp is None) or (len(_psp) < self.n)
    ph = np.asarray(getattr(self, "phi", []), dtype=float)
    _reg.append((len(_reg) + 1, bool(corto),
                 -1 if _psp is None else len(_psp), self.n,
                 float(np.max(np.abs(ph))) if ph.size else float("nan"),
                 int(np.sum(ph != 0.0)) if ph.size else -1, ph.size))
    return _vero(self, w)
S.Rete.calcola_psi = _wrap

# --- (a) e (b): i primi passi
for p in range(1, PASSI + 1):
    S.scuoti_vuoto(net); net.step(); net.mitosi()
    net.rilassa_disegno(); net.memoria_hebbiana_moto()
    d = np.asarray(net.d, dtype=float)
    print("PASSO %d  ritmo_chiamate=%s  ritmo_r1=%s  forma_r1=%s  calcpsi=%s  w_none=%s  "
          "n=%d  archi=%d  sotto_LAM=%d  min/LAM=%.6f"
          % (p, getattr(net, "_ritmo_chiamate", 0), getattr(net, "_ritmo_sicurezza", 0),
             getattr(net, "_ritmo_sicurezza_shape", "-"),
             getattr(net, "_calcpsi_chiamate", 0), getattr(net, "_calcpsi_w_none", 0),
             net.n, d.size, int(np.sum(d < S.LAM)), float(d.min())/S.LAM))

for k, corto, lp, nn, mx, nz, sz in _reg[:14]:
    print("PSI %d  fallback=%s  len(_psi_spinor)=%d  n=%d  max|phi|=%.6f  phi_non_zero=%d/%d"
          % (k, corto, lp, nn, mx, nz, sz))
print("PSI TOT invocazioni=%d  con fallback=%d" % (len(_reg), sum(1 for r in _reg if r[1])))
'''

ARGV = ["soliton_simulator.py", "--test", "N-MASSE", "--nmasse", "3", "--sep", "4.0",
        "--giri", "0", "--campo-spinoriale", "--spinore-vivo", "--spinore-corretto",
        "--chi-core", "--calore-scal", "--deparam-orologio", "--verlet", "--fork-su2",
        "--fork-su2-mem", "--cs-dinamico", "--tau-luce", "--rumore-colorato",
        "--pav-com", "--guscio-morbido", "--zeta-vir", "--chi-basc", "--chi-coop",
        "--plast-din", "--viriale", "--olon-part",
        "--scala-min-passo", "--peq-esatto", "--peq-nascita-locale", "--coes-causale",
        "--anom-simm", "--coes-adim", "--ritmo-wrap-2pi", "--tempo-unico-mitosi",
        "--invarianti=on"]


def main():
    try:
        os.makedirs(os.path.dirname(DEST))
    except OSError:
        pass
    f = io.open(DEST, "w", encoding="utf-8", newline="\n")

    def P(s):
        sys.stdout.write(s)
        f.write(s)

    src = "ARGV = %r\nPASSI = %d\n" % (ARGV, PASSI) + FIGLIO
    r = subprocess.run([sys.executable, "-c", src], cwd=RADICE, capture_output=True,
                       text=True, encoding="utf-8", errors="replace")
    P("# REVISIONE (1) -- L'AVVIO: quale tempo usa ogni legge nei primi passi\n#\n")
    P("# ARGV: quella del driver DOPO la decisione `NUDA = CAMPAGNA` (tutte le cure accese)\n")
    P("# PURE-READ: l'involucro su `calcola_psi` CONTA e basta.\n#\n")
    if r.returncode != 0:
        P("*** IL FIGLIO E' MORTO (rc=%d) ***\n%s\n"
          % (r.returncode, ((r.stdout or "") + (r.stderr or ""))[-3000:]))
        f.close()
        return 1
    sem = [x for x in r.stdout.splitlines() if x.startswith("SEM ")]
    pas = [x for x in r.stdout.splitlines() if x.startswith("PASSO ")]
    psi = [x for x in r.stdout.splitlines() if x.startswith("PSI ")]

    P("=" * 104 + "\n(1c) LA SEMINA AL PASSO ZERO -- prima di qualunque passo\n" + "=" * 104 + "\n")
    for x in sem:
        P("  " + x[4:] + "\n")
    P("\n  `_nasce` porta il troncone a `LAM` ALLA NASCITA, ed e' gated su\n")
    P("  `SCALA_MIN or SCALA_MIN_PASSO`. **`esattamente_LAM` sono gli archi TRONCATI**:\n")
    P("  una distribuzione continua non colpisce `LAM` esatto per caso.\n")

    P("\n" + "=" * 104 + "\n(1a) `ritmo()` -- il ramo `r = 1` per tutti\n" + "=" * 104 + "\n")
    for x in pas:
        P("  " + x + "\n")
    P("\n  `ritmo_r1` e' `_ritmo_sicurezza`: quante volte `ritmo()` ha restituito\n")
    P("  `np.ones(n)` perche' `_psi_prec` mancava o era della lunghezza sbagliata.\n")

    P("\n" + "=" * 104 + "\n(1b) IL FALLBACK `exp(i phi)` DELLO SPINORE\n" + "=" * 104 + "\n")
    for x in psi:
        P("  " + x[4:] + "\n")
    P("\n  Quando scatta, `psi_spin` e' costruito **DA `phi`**:\n")
    P("      `_psp[:, 0] = np.exp(1j * self.phi[:_n])`   (in `calcola_psi`)\n")
    P("  ⚠ **E' UN PONTE `INVERSA`**: `phi` -- il cui `4pi` e' **DICHIARATO**, cioe' una\n")
    P("  convenzione -- **scrive lo SPINORE**, il cui `4pi` e' **VERO**. E' la stessa forma\n")
    P("  per cui `TW_SPINORE` e' bloccato PER SEMPRE. **Qui pero' e' un FALLBACK DI AVVIO,\n")
    P("  non una legge**, e la differenza va detta invece di confonderle.\n")
    f.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
