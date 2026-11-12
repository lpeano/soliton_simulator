# -*- coding: utf-8 -*-
r"""**IL LATERALE HA v2? -- F-B E F-K, PER LA FUSIONE DEL PRINCIPALE COL REVERT DEL REVERT** *(Luca `2026-11-09` `01:31`, la regola `3`; il task history `doc/TASK_HISTORY/2026-11-09_laterale_mb.md`, sez. `6`)*. [[PIANO-2D-3D]]

    python csv/solitone/fusione_v2.py --atteso senza > doc/referti_l2/fusione_v2_X.txt      (lo stato X: dopo la sola fusione)
    python csv/solitone/fusione_v2.py --atteso con   > doc/referti_l2/fusione_v2_Y.txt      (lo stato Y: dopo il revert del revert)

**F-B:** i file di v2 *(quelli che il revert `de46816d` tocca, `.py` e `.yaml` sotto `primo_ordine/` e `csv/`)* **nel lavoro = quelli di `16d2ebdb`** *(il principale con v2)*, **ogni byte.**
**F-K:** `e_K` della scena di `C35-pi` *(le righe di `corsa_accensione.corsa`)*: **con v2 `-1.5706823467648499`, senza `-4.7122750003546425`** *(`de46816d`)*.
**`--atteso con`:** F-B e F-K DEVONO dire «con v2»; **`--atteso senza`:** DEVONO dire «senza» *(il DEVE FALLIRE di Luca: «con v2» deve fallire)*.
"""
import os
import subprocess
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))
import solitone  # noqa: E402,F401  (i percorsi)

RADICE = os.path.dirname(os.path.dirname(_QUI))
COMMIT_V2 = "16d2ebdb"
REVERT = "de46816d"
EK_CON = -1.5706823467648499
EK_SENZA = -4.7122750003546425
OK = [0, 0]
FALLITE = []


def esito(che, passa, nota="", deve=True):
    OK[1] += 1
    buono = passa if deve else not passa
    OK[0] += 1 if buono else 0
    if not buono:
        FALLITE.append(che)
    print("  %s: %-100s %s   %s" % ("DEVE PASSARE" if deve else "DEVE FALLIRE", che[:100], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()


def git(*a):
    return subprocess.run(["git"] + list(a), cwd=RADICE, capture_output=True).stdout


def main():
    import _presidio
    _presidio.avvia(__file__)
    atteso = sys.argv[sys.argv.index("--atteso") + 1]
    assert atteso in ("con", "senza")
    con = atteso == "con"
    file_v2 = [f for f in git("show", "--name-only", "--format=", REVERT).decode().split()
               if (f.startswith("primo_ordine/") or f.startswith("csv/")) and f.endswith((".py", ".yaml"))]
    print("=" * 130)
    print("IL LATERALE HA v2? (Luca 01:31, la regola 3): atteso %s; HEAD %s; %d file di v2 (dal revert %s)" % (atteso, git("rev-parse", "--short", "HEAD").decode().strip(), len(file_v2), REVERT))
    print("=" * 130)
    uguali, diversi = [], []
    for f in file_v2:
        r_ = subprocess.run(["git", "show", "%s:%s" % (COMMIT_V2, f)], cwd=RADICE, capture_output=True)
        rif = r_.stdout if r_.returncode == 0 else None        # ### la cura: un file CANCELLATO da v2 (in 16d2ebdb non c'e') e' None, come sul disco quando manca
        p = os.path.join(RADICE, f)
        disco = open(p, "rb").read() if os.path.exists(p) else None
        (uguali if disco == rif else diversi).append(f)
    print("  F-B: uguali a %s %d, diversi %d %s" % (COMMIT_V2, len(uguali), len(diversi), diversi))
    esito("F-B i file di v2 nel lavoro = quelli di %s (il principale con v2), ogni byte" % COMMIT_V2, not diversi, "%d su %d" % (len(uguali), len(file_v2)), deve=con)
    import _deriva_congelato as DC
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _triangoli_bassa_energia as BE
    import _vuoto_vivo_B as V
    from solitone import corsa_accensione as CA
    from solitone import protetto as P
    sol, vuoto, s = V.CORSE[CA.NOME]
    with CA.con_L(CA.LCORSA.get("C35-pi")), V.scena(s, vuoto, V.EPS) as (rec, z, phi0, pK):
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            DC.forma(z, rec["larghezza"])
        e_K = P.e_K(z)
    print("  F-K: e_K della scena di C35-pi %r (con v2 %r, senza %r)" % (e_K, EK_CON, EK_SENZA))
    esito("F-K e_K = quello CON v2", e_K == EK_CON, "%r" % e_K, deve=con)
    print("=" * 130)
    print("ESITO: %d/%d controlli come devono; fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main())
