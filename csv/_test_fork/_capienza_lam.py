# -*- coding: utf-8 -*-
"""`SEMINA_LAM` -- **QUANTI NODI ENTRANO DAVVERO.** Misurato con la semina RSA VERA.

> **Le stime non si estrapolano: si verificano.** La legge `r = 4*(n/352)^(1/3)` che avevo
> scritto **viene da UN solo punto**; qui si misura `n(r)` su piu' raggi e piu' semi, e si
> **guarda se l'esponente e' davvero `3`**.

**COME SI MISURA LA CAPIENZA, e usa il PERCORSO VERO:** si chiede a `_semina_lam` un `n`
enorme e si legge **il RIFIUTO**, che dichiara `collocati = il MASSIMO RAGGIUNTO`. Nessuna
formula di comodo: **il numero viene dallo stesso codice che semina.**

**⚠ E SI MISURA IN ISOLAMENTO** *(una regione vuota alla volta)*: i numeri delle masse **non
tengono conto del vuoto gia' seminato**, perche' **se il vuoto e' saturo per le masse non c'e'
posto** -- ed e' esattamente la domanda che Luca deve decidere *(strada `(i)` o `(ii)`)*.
**Dichiarato, non nascosto.**

Sola lettura sul simulatore. ASCII puro.
"""
import io
import os
import re
import subprocess
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
DEST = os.path.join(_QUI, "_revisione", "CAPIENZA_LAM.txt")

FIGLIO = r'''
import sys, re, numpy as np, math
sys.argv = ["soliton_simulator.py"]
import soliton_simulator as S
S.SEMINA_LAM = True
LAM = float(S.LAM); RC = float(S.R_CONN())

def capienza(r, seed):
    """Il MASSIMO che l'RSA colloca in una palla di raggio r, dal PERCORSO VERO."""
    net = S.Rete(seed)
    try:
        net._semina_lam(200000, r, (0.0, 0.0, 0.0))
        return 200000
    except SystemExit as ex:
        m = re.search(r"collocati\s*=\s*(\d+)", str(ex))
        return int(m.group(1)) if m else -1

RAGGI = [0.7, 1.0, 1.5, 2.0, 2.264, 3.0, 4.0, 4.5, 5.48, 7.6]
SEMI = [1, 2, 3]
print("LAM %.6f RCONN %.6f" % (LAM, RC))
dati = {}
for r in RAGGI:
    v = [capienza(r, s) for s in SEMI]
    dati[r] = v
    print("CAP r=%.4f  r/LAM=%.3f  n=%s  media=%.1f  disp=%.1f"
          % (r, r / LAM, v, float(np.mean(v)), float(np.std(v))))

# l'ESPONENTE: si misura, non si assume
rr = np.array([r for r in RAGGI if np.mean(dati[r]) >= 5.0], float)
nn = np.array([np.mean(dati[r]) for r in RAGGI if np.mean(dati[r]) >= 5.0], float)
A = np.vstack([np.log(rr), np.ones(len(rr))]).T
esp, q = np.linalg.lstsq(A, np.log(nn), rcond=None)[0]
print("ESPONENTE misurato = %.4f   (atteso 3 se n ~ r^3)  su %d raggi con n>=5"
      % (esp, len(rr)))
print("COEFF n = %.4f * r^%.4f" % (math.exp(q), esp))

def raggio_per(n, seed=1, lo=0.5, hi=40.0):
    """il RAGGIO MINIMO che contiene n, cercato con la semina VERA (bisezione)."""
    for _ in range(26):
        mid = 0.5 * (lo + hi)
        if capienza(mid, seed) >= n:
            hi = mid
        else:
            lo = mid
    return hi

for n in (497, 900, 2391):
    r = raggio_per(n)
    print("RAGGIO_PER n=%d  ->  r=%.4f  (= %.3f LAM)   verifica: capienza=%d"
          % (n, r, r / LAM, capienza(r, 1)))
'''


def main():
    try:
        os.makedirs(os.path.dirname(DEST))
    except OSError:
        pass
    f = io.open(DEST, "w", encoding="utf-8", newline="\n")

    def P(s):
        sys.stdout.write(s)
        f.write(s)

    r = subprocess.run([sys.executable, "-c", FIGLIO], cwd=RADICE, capture_output=True,
                       text=True, encoding="utf-8", errors="replace")
    P("# `SEMINA_LAM` -- QUANTI NODI ENTRANO DAVVERO. Semina RSA VERA, non estrapolazione.\n#\n")
    P("# La capienza si legge dal RIFIUTO di `_semina_lam`, che dichiara `collocati`:\n")
    P("# **il numero viene dallo stesso codice che semina.**\n")
    P("# MISURATO IN ISOLAMENTO: una regione vuota alla volta, SENZA il vuoto di fondo.\n#\n")
    if r.returncode != 0:
        P("*** MORTO (rc=%d) ***\n%s\n" % (r.returncode, (r.stdout + r.stderr)[-3000:]))
        f.close()
        return 1
    for x in (r.stdout or "").splitlines():
        if x.startswith(("LAM ", "CAP ", "ESPONENTE", "COEFF", "RAGGIO_PER")):
            P("  " + x + "\n")

    # --- le due scene, coi numeri appena misurati
    cap = {}
    for x in (r.stdout or "").splitlines():
        m = re.match(r"CAP r=([\d.]+).*media=([\d.]+)", x)
        if m:
            cap[float(m.group(1))] = float(m.group(2))
    rag = {}
    for x in (r.stdout or "").splitlines():
        m = re.match(r"RAGGIO_PER n=(\d+)\s+->\s+r=([\d.]+)", x)
        if m:
            rag[int(m.group(1))] = float(m.group(2))
    sys.path.insert(0, RADICE)
    import soliton_simulator as S
    import numpy as np
    LAM, RC = float(S.LAM), float(S.R_CONN())

    P("\n" + "=" * 100 + "\nLA SCENA DI OGGI, e il numero che la uccide\n" + "=" * 100 + "\n")
    P("  `_semina_n_masse`: %d masse su un cerchio di raggio `sep`, ognuna con\n" % 3)
    P("  `npunt = int(massa_critica_collasso() * 0.8) = %d` nodi in **raggio `0.7`**\n"
      % int(S.massa_critica_collasso() * 0.8))
    P("  (`_size_video(k, 0.7)`, e `--size` non e' passato).\n\n")
    c07 = cap.get(0.7, float("nan"))
    P("  ❗ IN RAGGIO `0.7` (= %.3f LAM) CI STANNO **%.0f** NODI. La scena ne chiede **%d**.\n"
      % (0.7 / LAM, c07, int(S.massa_critica_collasso() * 0.8)))
    P("     RAPPORTO CHIESTO / POSSIBILE = **%.0f**\n"
      % (int(S.massa_critica_collasso() * 0.8) / max(c07, 1e-9)))
    P("  -> **il raggio della massa e' PIU' PICCOLO di `LAM`**: la scena mette la materia\n")
    P("     **dentro una regione piu' piccola della scala di Planck del sistema.**\n")

    P("\n" + "=" * 100 + "\nLE DUE SCENE DEL MANDATO -- NUMERI, NON STIME\n" + "=" * 100 + "\n")
    P("  GEOMETRIA: `nm = 3` masse su un cerchio di raggio `sep`. La distanza fra i CENTRI di\n")
    P("  due masse adiacenti e' la corda a 120 gradi: **`sep * sqrt(3)`**.\n")
    P("  L'INTERVALLO fra i BORDI e' `sep*sqrt(3) - 2*r_massa`.\n")
    P("  ⚠ **`intervallo = R_CONN` E' UNA SCELTA DI LUCA, NON UNA DERIVAZIONE**, e si dichiara:\n")
    P("     e' il raggio a cui il vuoto si allaccia, quindi \"le masse si vedono appena\".\n\n")
    ra = rag.get(497)
    if ra:
        sep_a = (2.0 * ra + RC) / np.sqrt(3.0)
        P("  (a) STESSA MATERIA -- n per massa come oggi (%d)\n" % 497)
        P("      raggio della massa con `A13`:  r = %.4f  (= %.3f LAM)\n" % (ra, ra / LAM))
        P("      sep necessario:  (2*r + R_CONN)/sqrt(3) = **%.4f**\n" % sep_a)
        P("      distanza fra i centri = sep*sqrt(3) = %.4f\n" % (sep_a * np.sqrt(3.0)))
        P("      estensione totale della scena ~ sep + r = %.4f\n" % (sep_a + ra))
    sep_b = 4.0
    r_b = (sep_b * float(np.sqrt(3.0)) - RC) / 2.0
    P("\n  (b) STESSA DISTANZA -- `--sep 4.0`\n")
    P("      distanza fra i centri = 4.0*sqrt(3) = %.4f\n" % (sep_b * np.sqrt(3.0)))
    P("      raggio massimo con intervallo R_CONN:  r = (%.4f - %.4f)/2 = **%.4f** (= %.3f LAM)\n"
      % (sep_b * np.sqrt(3.0), RC, r_b, r_b / LAM))
    cb = cap.get(2.264)
    P("      n per massa = capienza a quel raggio: **%s**  (misurato a r=2.264, il piu' vicino)\n"
      % ("%.0f" % cb if cb else "da misurare"))
    P("\n  ⚠ **TUTTI QUESTI NUMERI IGNORANO IL VUOTO DI FONDO**, e non e' una svista: **se il\n")
    P("     vuoto e' seminato al massimo non c'e' posto per nessuna massa.** E' la decisione\n")
    P("     `(i)` / `(ii)` che aspetta Luca. **Le scene si PREPARANO, non si girano.**\n")
    f.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
