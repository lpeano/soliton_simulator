# -*- coding: utf-8 -*-
r"""**T1: I TRE SIGILLI DI GAUGE COL CRITERIO DELLA DECISIONE `(1)`** *(il task history `doc/TASK_HISTORY/2026-11-07_u1_prototipo_verificato.md`, sez. `12`)*. [[U1-PROTOTIPO-TRIANGOLI]]

    python csv/solitone/u1_t1.py > doc/referti_l2/u1_t1.txt

### **Rigirati AL LORO COMMIT in un `git worktree` staccato ACCANTO al repo** *(`C:\Users\lpeano\wt_t1`; su `E:` git lo rifiuta, `1c246469`; la cartella della corsa non cambia)*: `_u1_prototipo.py` a `0b6bfde8` *(il sigillo `(b)`)*,
`_u1_secondo.py` a `64bb2328` *(`(b1)`, `(b2)`)*. ### **`T1-R`:** le righe rifatte = le righe dei referti committati. ### **`T1-b`, `T1-b1`, `T1-b2`** *(la decisione `(1)`)*:
in ogni riga `|dE| / stima <= 1`, `rho <= 1e-12`, `eB <= 1e-12`. **`T1-F`** *(DEVE FALLIRE)*: lo stesso con la stima divisa per `10`. **I referti vecchi non si riscrivono.**
"""
import os
import re
import shutil
import subprocess
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))
import solitone  # noqa: E402,F401  (i percorsi)

DIR_WT = os.path.join(os.path.dirname(solitone.RADICE), "wt_t1")   # ### accanto al repo, su C: (come st_main): su E: git rifiuta il worktree, E: non registra il proprietario (1c246469)
TOLL_REL = 1e-12               # ### la decisione (1) di Luca: rho ed e B a 1e-12 relativo
SIGILLI = (("u1_prototipo", "0b6bfde8", "csv/_u1_prototipo.py", "doc/referti_l2/u1_prototipo.txt",
            re.compile(r"^\s*(\S+) s ([\d.]+) (\S+)\s+e ([\d.]+) \| \(b\) rho (\S+) E (\S+) eB (\S+) \[fase globale: E (\S+); \|dE\| / stima (\S+)\]")),
           ("u1_secondo", "64bb2328", "csv/_u1_secondo.py", "doc/referti_l2/u1_secondo.txt",
            re.compile(r"^\s*(\S+) s ([\d.]+) e ([\d.]+) \| \(b1\) rho (\S+) eB (\S+) E (\S+) \(max\|A'\| (\S+), \|dE\|/stima (\S+)\) \| \(b2\) rho (\S+) eB (\S+) E (\S+) \(max\|A'\| (\S+), \|dE\|/stima (\S+)\)")))

OK = [0, 0]
FALLITE = []


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    if not passa:
        FALLITE.append(che)
    print("  %-118s %s   %s" % (che[:118], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return passa


def righe(testo, rx):
    return [m.groups() for m in (rx.match(r) for r in testo.splitlines()) if m]


def giudica(rr, nome, fatt):
    """### la decisione `(1)` su ogni riga; `fatt` divide la stima *(1: il criterio; 10: `T1-F`)*. `(passa, il rapporto massimo, rho max, eB max)`."""
    if nome == "u1_prototipo":
        terne = [(float(g[4]), float(g[6]), float(g[8])) for g in rr]          # rho, eB, |dE|/stima
    else:
        terne = [(float(g[3]), float(g[4]), float(g[7])) for g in rr] + [(float(g[8]), float(g[9]), float(g[12])) for g in rr]
    q = max(t[2] for t in terne) * fatt
    r_ = max(t[0] for t in terne)
    b_ = max(t[1] for t in terne)
    return q <= 1.0 and r_ <= TOLL_REL and b_ <= TOLL_REL, q, r_, b_


def main():
    import _presidio
    _presidio.avvia(__file__)
    R = solitone.RADICE
    os.makedirs(DIR_WT, exist_ok=True)
    print("=" * 130)
    print("T1, I SIGILLI DI GAUGE COL CRITERIO DELLA DECISIONE (1): |dE| / stima <= 1, rho ed eB <= %g, in ogni riga; rigirati al loro commit in un git worktree su %s" % (TOLL_REL, DIR_WT))
    print("=" * 130)
    for nome, comm, script, ref, rx in SIGILLI:
        wt = os.path.join(DIR_WT, comm)
        assert not os.path.exists(wt), "il worktree %s esiste gia': non lo sovrascrivo" % wt
        subprocess.check_call(["git", "-C", R, "worktree", "add", "--detach", wt, comm])
        out = os.path.join(DIR_WT, "%s_%s.txt" % (nome, comm))
        try:
            with open(out, "wb") as f:
                rc = subprocess.run([sys.executable, script], cwd=wt, stdout=f, stderr=subprocess.STDOUT).returncode
        finally:
            subprocess.call(["git", "-C", R, "worktree", "remove", "--force", wt])
        nuovo = open(out, encoding="utf-8", errors="replace").read()
        vecchio = subprocess.check_output(["git", "-C", R, "show", "%s:%s" % (comm, ref)]).decode("utf-8", errors="replace")
        rn, rv = righe(nuovo, rx), righe(vecchio, rx)
        tim = [r for r in nuovo.splitlines() if "[TIMBRO]" in r][:3]
        print("### %s a %s (%s): exit %d; righe del sigillo rifatte %d, committate %d; %s" % (nome, comm, script, rc, len(rn), len(rv), " | ".join(t.strip() for t in tim)))
        esito("DEVE PASSARE: T1-R %s: le righe del sigillo rifatte al commit %s = quelle del referto committato (il testo dei campi)" % (nome, comm), bool(rv) and rn == rv,
              "%d righe" % len(rv) if rn == rv else "### diverse: %s" % [i for i, (a, b) in enumerate(zip(rn, rv)) if a != b][:5])
        passa, q, r_, b_ = giudica(rv, nome, 1.0)
        che = "(b)" if nome == "u1_prototipo" else "(b1) e (b2)"
        esito("DEVE PASSARE: T1-%s %s: in ogni riga |dE| / stima <= 1, rho e eB <= %g (la decisione (1))" % (che.replace(" e ", "-").replace("(", "").replace(")", ""), che, TOLL_REL), passa,
              "|dE|/stima max %.3f, rho max %.1e, eB max %.1e" % (q, r_, b_))
        pf, qf, _r, _b = giudica(rv, nome, 10.0)
        esito("DEVE FALLIRE: T1-F %s %s con la stima divisa per 10" % (nome, che), not pf, "|dE|/(stima/10) max %.3f" % qf)
    print("=" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main())
