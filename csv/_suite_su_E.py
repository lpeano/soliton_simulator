# -*- coding: utf-8 -*-
r"""**LA SUITE LANCIATA SU E:** *(DECISIONE DI LUCA, 2026-11-27 `23:21`, [M2245-27] B2)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe csv/_suite_su_E.py            # = primo_ordine/collauda.py, con l'ambiente qui sotto
    E:\python\py3132\python.exe csv/_suite_su_E.py <argomenti di collauda.py>

**Perche'.** E: e' un file system che **non registra il proprietario**: ogni repository git creato nel temp
*(`E:\soliton_lavoro\tmp`, perche' C: MAI -- decisione di Luca delle `18:59`)* e' «dubious ownership», e i due
collaudi che ne creano uno *(`M-B1`, che crea un worktree al commit `8c7b9288` e ci lancia un figlio, e
lo STAGE, `csv/_stage.py --collaudo`)* falliscono **per l'ambiente, non per il codice** *(provato: un
`git init` vuoto nel temp di E: da' `detected dubious ownership`)*.

**Che cosa fa.** Imposta **nel PROPRIO ambiente** `GIT_CONFIG_COUNT=1`, `GIT_CONFIG_KEY_0=safe.directory`,
`GIT_CONFIG_VALUE_0=*`, poi esegue `primo_ordine/collauda.py` con gli stessi argomenti e ne rende il codice
d'uscita: **i figli lo ereditano** *(M-B1 compreso)*. ### **Niente in `git config --global`, niente su C:,
niente sotto `primo_ordine/`** *(il nucleo di mitosi resta a 9 file contro `42638304`)*.

**Il limite, dichiarato.** Il jolly vale per OGNI git lanciato dalla suite, non solo per i due collaudi:
e' la via scelta da Luca alle `23:21` *(«i figli la ereditano»)*. `TMP` e `TEMP`, se non sono gia' su E:,
si mettono su `E:\soliton_lavoro\tmp`.
"""
# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Lancia la suite (collauda.py) con safe.directory=* nel solo ambiente del processo: E: non registra il proprietario (Luca 23:21).
import os
import subprocess
import sys

_RADICE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TMP_E = r"E:\soliton_lavoro\tmp"
AMBIENTE = {"GIT_CONFIG_COUNT": "1", "GIT_CONFIG_KEY_0": "safe.directory", "GIT_CONFIG_VALUE_0": "*"}


def ambiente():
    env = dict(os.environ)
    gia = [k for k in env if k.startswith("GIT_CONFIG_")]
    assert not gia, ("### GIT_CONFIG_* gia' nell'ambiente (%s): non le sovrascrivo in silenzio" % gia)
    env.update(AMBIENTE)
    for k in ("TMP", "TEMP"):
        if not env.get(k, "").upper().startswith("E:"):
            env[k] = TMP_E
    assert not env["TMP"].upper().startswith("C:") and not env["TEMP"].upper().startswith("C:")
    return env


def main(argv):
    env = ambiente()
    print("[_suite_su_E] %s; TMP=%s TEMP=%s; la suite: primo_ordine/collauda.py %s" % (
        ", ".join("%s=%s" % kv for kv in AMBIENTE.items()), env["TMP"], env["TEMP"], " ".join(argv)))
    sys.stdout.flush()
    r = subprocess.run([sys.executable, os.path.join(_RADICE, "primo_ordine", "collauda.py")] + list(argv),
                       cwd=_RADICE, env=env)
    return r.returncode


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
