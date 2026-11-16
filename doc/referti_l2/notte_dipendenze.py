# -*- coding: utf-8 -*-
r"""**LE DIPENDENZE DI `notte.py` E DI `verifica_coppie.py` DAI FILE** *(Luca `2026-11-16` `21:35`: «l'elenco di TUTTI i file che leggono»)*.

    E:\python\py3132\python.exe doc/referti_l2/notte_dipendenze.py caso --caso coppia|triangolo|verifica --out <scratchpad>/dip_<caso>.json
    E:\python\py3132\python.exe doc/referti_l2/notte_dipendenze.py elenco --dentro <scratchpad>/dip_coppia.json <scratchpad>/dip_triangolo.json <scratchpad>/dip_verifica.json > doc/referti_l2/notte_dipendenze.txt

### **MISURATE, non lette dal codice:** **un audit hook di Python** *(`sys.addaudithook`, l'evento `open`)* **registra OGNI file che il processo apre**, in tre casi: **(coppia)** `notte.py avvio` della coppia su `L 297` + `corsa` di `2` tick; **(triangolo)** `avvio` del triangolo su `L 339` + `2` tick; **(verifica)** `verifica_coppie.main` fino al primo tick *(`mattone_coppia_L162.N_TICK = 1` in memoria; le SCRITTURE nel repo sono BLOCCATE dall'hook: il caso finisce li', dopo le letture)*.
### **`elenco`:** per ogni file letto *(fuori dalla libreria di Python)*: **il percorso, se e' nel repo di C: e se e' TRACCIATO** *(`git ls-files`)*, **lo sha1 dei byte grezzi, se esiste nel worktree del mattone e con che sha1**; **e accanto i file NOMINATI nei sorgenti** *(`DIR_REF`, `DIR_E`, `DIR_NPZ`)* **che i casi non hanno aperto.**
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys

QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(os.path.dirname(QUI))
MATTONE = r"C:\Users\lpeano\soliton_simulator_mattone"
SOL = os.path.join(RADICE, "csv", "solitone")
for _p in (SOL, os.path.join(RADICE, "csv")):
    if _p not in sys.path:
        sys.path.insert(0, _p)
APERTI = []


class Bloccata(Exception):
    pass


def norm(p):
    return os.path.normcase(os.path.abspath(p))


def hook(ev, args):
    if ev != "open":
        return
    p = args[0]
    if not isinstance(p, (str, bytes, os.PathLike)):
        return
    p = os.path.abspath(os.fsdecode(p))
    mode = args[1] if len(args) > 1 else None
    flags = args[2] if len(args) > 2 else 0
    scrive = (isinstance(mode, str) and any(c in mode for c in "wax+")) or (mode is None and isinstance(flags, int) and flags & (os.O_WRONLY | os.O_RDWR))
    APERTI.append([p, str(mode), bool(scrive)])
    if scrive and BLOCCA[0] and norm(p).startswith(norm(RADICE)):
        raise Bloccata("la scrittura di %s e' bloccata (il caso verifica finisce qui)" % p)


BLOCCA = [False]


def caso(nome, out):
    sys.addaudithook(hook)
    import notte as N
    try:
        if nome == "coppia":
            N.main(["avvio", "--nome", "DIP-coppia", "--tipo", "coppia", "--L", "297", "--d", "35", "--fase", "0", "--R_A", "85.06"])
            N.main(["corsa", "--nome", "DIP-coppia", "--da", "0", "--fino", "2", "--ogni", "2"])
        elif nome == "triangolo":
            N.main(["avvio", "--nome", "DIP-t120", "--tipo", "triangolo", "--L", "339", "--R_A", "97.16"])
            N.main(["corsa", "--nome", "DIP-t120", "--da", "0", "--fino", "2", "--ogni", "2"])
        else:
            import mattone_coppia_L162 as MCL
            import verifica_coppie as VC
            MCL.N_TICK = 1
            BLOCCA[0] = True
            VC.main(["--d", "35", "--L", "297", "--fase", "0"])
    except Bloccata as z:
        print("### %s" % z)
    except Exception as z:  # noqa: BLE001
        print("### il caso %s finisce con %r (le letture fin qui sono registrate)" % (nome, z))
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(APERTI, fh)
    print("### %d aperture registrate in %s" % (len(APERTI), out))
    return 0


def sha1(f):
    h = hashlib.sha1()
    with open(f, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()[:8]


def tracciato(rel):
    r = subprocess.run(["git", "ls-files", "--error-unmatch", rel], cwd=RADICE, capture_output=True, text=True)
    return r.returncode == 0


def elenco(dentro):
    lib = norm(os.path.dirname(os.path.dirname(os.__file__)))
    letti, pyc = {}, set()
    for f in dentro:
        c = os.path.basename(f)[4:-5]
        for p, mode, scrive in json.load(open(f, encoding="utf-8")):
            if scrive or norm(p).startswith(lib) or "\\notte\\DIP-" in p or os.path.isdir(p):
                continue
            if "__pycache__" in p:
                pyc.add(p)
                continue
            letti.setdefault(p, set()).add(c)
    print("=" * 130)
    print("LE DIPENDENZE DI notte.py E verifica_coppie.py DAI FILE (Luca 2026-11-16 21:35): MISURATE con un audit hook (l'evento open), fuori dalla libreria di Python (%s)" % lib)
    print("=" * 130)
    print("    %-86s %-10s %-9s %-9s %-26s %s" % ("il file", "dove", "tracciato", "sha1", "nel worktree del mattone", "i casi"))
    print("    (i .pyc di __pycache__ letti: %d, DERIVATI dai sorgenti da Python, non dipendenze: fuori dalla tabella)" % len(pyc))
    non_tr = []
    for p in sorted(letti, key=lambda q: (not norm(q).startswith(norm(RADICE)), q.endswith(".py"), q)):
        dentro_repo = norm(p).startswith(norm(RADICE))
        rel = os.path.relpath(p, RADICE).replace("\\", "/") if dentro_repo else None
        tr = tracciato(rel) if dentro_repo else False
        ex = os.path.exists(p)
        s = sha1(p) if ex else "MANCA"
        pm = os.path.join(MATTONE, os.path.relpath(p, RADICE)) if dentro_repo else None
        mt = (sha1(pm) if os.path.exists(pm) else "no") if pm else "-"
        print("    %-86s %-10s %-9s %-9s %-26s %s" % (rel or p, "repo C:" if dentro_repo else "fuori", "SI" if tr else "### NO", s, mt, ",".join(sorted(letti[p]))))
        if not tr:
            non_tr.append((rel or p, s, mt))
    print("-" * 130)
    print("### I FILE LETTI NON TRACCIATI: %d" % len(non_tr))
    for p, s, mt in non_tr:
        print("    %s  sha1 %s  (il worktree del mattone: %s)" % (p, s, mt))
    # ---------------------------------------------------------------- i nomi nei sorgenti che i casi non hanno aperto
    import mattone as MT
    dirs = {"DIR_REF": MT.DIR_REF, "DIR_E": MT.DIR_E}
    nomi = set()
    for m in ("notte", "verifica_coppie", "mattone_coppia_L162", "legati", "triangolo_120", "mattone_triangolo", "triangolo_video", "convergenza", "prova_scatola5", "mattone", "mattone_cottura", "mattone_cottura_U", "porto", "porto_alone"):
        f = os.path.join(SOL, m + ".py")
        if not os.path.exists(f):
            continue
        t = open(f, encoding="utf-8").read()
        for d, nome in re.findall(r"(DIR_REF|DIR_E)\s*,\s*\"([^\"%{}]+)\"", t):
            nomi.add((m, d, nome))
    aperti = {norm(p) for p in letti}
    print("-" * 130)
    print("### I FILE NOMINATI NEI SORGENTI (os.path.join(DIR_REF|DIR_E, \"nome\"), nomi fissi) CHE I TRE CASI NON HANNO APERTO (rami non toccati, o file che si SCRIVONO):")
    for m, d, nome in sorted(nomi):
        p = os.path.join(dirs[d], nome)
        if norm(p) in aperti:
            continue
        dentro_repo = norm(p).startswith(norm(RADICE))
        rel = os.path.relpath(p, RADICE).replace("\\", "/") if dentro_repo else p
        if os.path.isdir(p):
            continue
        ex = os.path.isfile(p)
        print("    %-24s %-8s %-70s %s%s" % (m, d, rel, ("esiste sha1 %s" % sha1(p)) if ex else "### NON esiste", ("; tracciato %s" % ("SI" if tracciato(rel) else "NO")) if dentro_repo and ex else ""))
    print("=" * 130)
    return 0


def main(argv):
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("caso")
    a.add_argument("--caso", required=True, choices=("coppia", "triangolo", "verifica"))
    a.add_argument("--out", required=True)
    b = sub.add_parser("elenco")
    b.add_argument("--dentro", nargs="+", required=True)
    x = ap.parse_args(argv)
    if x.cmd == "caso":
        return caso(x.caso, x.out)
    return elenco(x.dentro)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
