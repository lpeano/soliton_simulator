# -*- coding: utf-8 -*-
r"""**[M1446-K] LA CODA DELLE CORSE DI [M1446]: UN DISPATCHER SENZA POLLING** *(il mandato di Luca [M1446], S6; la carta `doc/CARTA_E_mc2.md`, sez. `K`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/coda_m1446.py        (legge doc/referti_l2/coda_m1446.json a ogni lancio; lo stato in E:\soliton_simulator\controllo\M1446\coda_stato.json)

**Lancia la prossima corsa** *(la priorita' piu' bassa, a parita' l'ordine della lista; saltate quelle gia' fatte o in corso)* **solo se:** i processi `python.exe` totali *(contati dalla riga di comando, il dispatcher compreso)* `< 10`; la memoria libera `> 4 GB`; **la CPU stimata dal conto dei processi** *(la lettura del carico e' negata; `< 10` processi da un filo su `12` logici = `< 83%`)* **e, dal [M1944-03] (Luca 19:44, «un solo lanciatore»), la CPU LETTA** *(`GetSystemTimes`, due campioni a `1 s`, solo al lancio)* **sotto il `90%`**. **Poi ASPETTA in modo bloccante la fine di un figlio** *(un thread per figlio che chiama `wait()`, una coda: nessun `sleep`, nessun polling: CLAUDE.md par. 5)*. **Ogni corsa** ha la voce APERTA/CHIUSO nel registro *(`_registro_corse.py apri/chiudi`: usato, non modificato)*. **Se non puo' lanciare e nessun figlio gira, si ferma e lo scrive.**
"""
import ctypes
import json
import os
import queue
import subprocess
import sys
import threading
import time

_QUI = os.path.dirname(os.path.abspath(__file__))
_RADICE = os.path.dirname(os.path.dirname(_QUI))
LISTA = os.path.join(_QUI, "coda_m1446.json")
DIR = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "M1446")
STATO = os.path.join(DIR, "coda_stato.json")
PY = r"E:\python\py3132\python.exe"
MAX_PROC, MIN_GB = 10, 4.0               # ### Luca: il tetto e il freno
MAX_CPU = 90.0                           # ### Luca: la CPU sotto il 90% ai lanci, LETTA (GetSystemTimes) e non stimata ([M1944-03])
FORZA = "Luca 2026-11-22: [M1446] la coda, nel tetto dei 10 con il freno a 4 GB"


def memoria_gb():
    class M(ctypes.Structure):
        _fields_ = [("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong), ("ullTotalPhys", ctypes.c_ulonglong), ("ullAvailPhys", ctypes.c_ulonglong),
                    ("ullTotalPageFile", ctypes.c_ulonglong), ("ullAvailPageFile", ctypes.c_ulonglong), ("ullTotalVirtual", ctypes.c_ulonglong),
                    ("ullAvailVirtual", ctypes.c_ulonglong), ("ullAvailExtendedVirtual", ctypes.c_ulonglong)]
    m = M()
    m.dwLength = ctypes.sizeof(M)
    ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))
    return m.ullAvailPhys / 1024.0 ** 3


def processi():
    out = subprocess.run(["powershell", "-NoProfile", "-c", "(Get-CimInstance Win32_Process -Filter \"name='python.exe'\" | Measure-Object).Count"], capture_output=True, text=True)
    return int(out.stdout.strip() or "0")


def cpu_ora():
    """### la CPU totale ORA: `GetSystemTimes` *(kernel32)* due volte a `1 s` di distanza, `1 - idle/(kernel + user)` *(il kernel comprende l'idle)*; solo al lancio, non e' un polling."""
    class FT(ctypes.Structure):
        _fields_ = [("lo", ctypes.c_ulong), ("hi", ctypes.c_ulong)]

    def campione():
        i_, k_, u_ = FT(), FT(), FT()
        ctypes.windll.kernel32.GetSystemTimes(ctypes.byref(i_), ctypes.byref(k_), ctypes.byref(u_))
        return [x.hi * 2 ** 32 + x.lo for x in (i_, k_, u_)]
    a = campione()
    time.sleep(1.0)
    b = campione()
    di, dk, du = (b[q] - a[q] for q in range(3))
    tot = dk + du
    return 100.0 * (1.0 - di / tot) if tot > 0 else 100.0


def registro(*args):
    return subprocess.run([PY, os.path.join(_RADICE, "csv", "solitone", "_registro_corse.py")] + list(args), cwd=_RADICE, capture_output=True, text=True)


def scrivi_stato(S):
    os.makedirs(DIR, exist_ok=True)
    tmp = STATO + ".tmp"
    open(tmp, "w", encoding="utf-8").write(json.dumps(S, indent=1, ensure_ascii=False))
    os.replace(tmp, STATO)


def ora():
    return time.strftime("%Y-%m-%dT%H:%M:%S")


def main():
    S = json.load(open(STATO, encoding="utf-8")) if os.path.exists(STATO) else {"corse": {}, "eventi": []}
    env = dict(os.environ, PYTHONNOUSERSITE="1", OMP_NUM_THREADS="1", MKL_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", NUMEXPR_NUM_THREADS="1", TMP=r"E:\python\tmp", TEMP=r"E:\python\tmp")
    for v in ("PYTHONHOME", "PYTHONPATH"):
        env.pop(v, None)
    fine = queue.Queue()
    vivi = {}

    def aspetta(nome, p, log):
        rc = p.wait()
        log.close()
        fine.put((nome, rc))

    while True:
        lista = json.load(open(LISTA, encoding="utf-8"))["corse"]
        pronte = sorted([(c["priorita"], i, c) for i, c in enumerate(lista) if c["nome"] not in S["corse"]], key=lambda x: (x[0], x[1]))
        lanciato = False
        if pronte:
            n_p, gb = processi(), memoria_gb()
            cpu = cpu_ora()
            if n_p < MAX_PROC and gb > MIN_GB and cpu < MAX_CPU:
                _pr, _i, c = pronte[0]
                voce = "m1446-" + c["nome"]
                r = registro("apri", "--nome", voce, "--tipo", "lunga", "--comando", " ".join([PY.replace("\\", "/")] + c["argv"]), "--note", c.get("note", "[M1446] " + c["nome"]), "--forza", FORZA)
                d = os.path.join(DIR, "log")
                os.makedirs(d, exist_ok=True)
                log = open(os.path.join(d, c["nome"] + ".txt"), "a", encoding="utf-8")
                p = subprocess.Popen([PY, "-u"] + c["argv"], cwd=_RADICE, env=env, stdout=log, stderr=subprocess.STDOUT)
                vivi[c["nome"]] = p
                S["corse"][c["nome"]] = {"stato": "IN CORSA", "pid": p.pid, "lanciata": ora(), "processi_prima": n_p, "gb": round(gb, 2), "registro": r.returncode}
                S["eventi"].append("%s LANCIATA %s (pid %d; i processi prima %d, la CPU letta %.1f%%; %.1f GB)" % (ora(), c["nome"], p.pid, n_p, cpu, gb))
                scrivi_stato(S)
                threading.Thread(target=aspetta, args=(c["nome"], p, log), daemon=True).start()
                lanciato = True
                continue
        if not vivi:
            S["eventi"].append("%s FERMO: %s" % (ora(), "la coda e' vuota" if not pronte else "non posso lanciare (i processi %d, %.1f GB, la CPU %.1f%%) e nessun figlio gira" % (processi(), memoria_gb(), cpu_ora())))
            scrivi_stato(S)
            return 0
        nome, rc = fine.get()                       # ### l'attesa BLOCCANTE della fine di un figlio
        del vivi[nome]
        esito = "FINITO" if rc == 0 else "FALLITO"
        registro("chiudi", "--nome", "m1446-" + nome, "--esito", esito, "--punto", "uscita %d" % rc)
        S["corse"][nome].update(stato=esito, uscita=rc, finita=ora())
        S["eventi"].append("%s %s %s (uscita %d)" % (ora(), esito, nome, rc))
        scrivi_stato(S)
        _ = lanciato


if __name__ == "__main__":
    sys.exit(main())
