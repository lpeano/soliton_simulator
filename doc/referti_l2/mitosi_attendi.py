# -*- coding: utf-8 -*-
r"""**L'ATTESA E LA DECISIONE DELLA PROROGA DEL TRONCO** *(la nota di Luca `2026-11-21` `13:57`; la carta `doc/TASK_HISTORY/2026-11-20_covariante_di_stella.md` del ramo `primo-ordine`, sez. `16`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/mitosi_attendi.py attendi <WINPID>     aspetta che quel processo Windows esca (WaitForSingleObject: un'attesa del sistema, NON un sondaggio)
    E:\python\py3132\python.exe doc/referti_l2/mitosi_attendi.py decidi <cartella TRONCO> <k limite>
    E:\python\py3132\python.exe doc/referti_l2/mitosi_attendi.py prova                 le prove a secco (la carta sez. 16.5)

**`decidi`** stampa UNA parola e la rende come codice d'uscita: **`SCATTO`** *(`scatto.json` c'e': `0`)*; **`PROROGA`** *(nessuno scatto, l'ultimo stato INTEGRO e' al `k limite`: `20`)*; **`CADUTO`** *(nessuno scatto, l'ultimo stato integro e' prima del limite: `21`)*; **`VUOTO`** *(nessuno stato integro: `22`)*.
**Solo dai FILE** *(lo sha1 di ogni stato controllato, come `mitosi_rami.ultimo`)*: il registro non entra nella decisione.
"""
import ctypes
import glob
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
import time

CODICI = {"SCATTO": 0, "PROROGA": 20, "CADUTO": 21, "VUOTO": 22}
SYNCHRONIZE, INFINITE = 0x00100000, 0xFFFFFFFF


def sha1(f):
    h = hashlib.sha1()
    with open(f, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def ultimo(d):
    """### l'ultimo stato INTEGRO *(lo sha1 dei byte uguale al file `.sha1`)*: `(k, file)` o `None`."""
    for f in sorted(glob.glob(os.path.join(d, "stato_*.npz")), reverse=True):
        try:
            if open(f + ".sha1", encoding="utf-8").read().split()[0] == sha1(f):
                return int(os.path.basename(f)[6:11]), f
        except (OSError, IndexError):
            pass
        print("### lo stato %s NON e' integro: si prende quello prima" % os.path.basename(f))
    return None


def decidi(d, k_limite):
    if os.path.exists(os.path.join(d, "scatto.json")):
        return "SCATTO", None
    u = ultimo(d)
    if u is None:
        return "VUOTO", None
    return ("PROROGA" if u[0] == k_limite else "CADUTO"), u


def attendi(winpid):
    """### aspetta l'uscita del processo Windows `winpid`. Se non si apre (gia' uscito, o non c'e'), torna SUBITO e lo dice."""
    k32 = ctypes.WinDLL("kernel32", use_last_error=True)
    k32.OpenProcess.restype = ctypes.c_void_p
    h = k32.OpenProcess(SYNCHRONIZE, False, int(winpid))
    if not h:
        print("### il processo %s non si apre (errore %d): gia' uscito, o non c'e'" % (winpid, ctypes.get_last_error()))
        return 1
    print("### aspetto il processo %s dalle %s" % (winpid, time.strftime("%Y-%m-%d %H:%M:%S")))
    sys.stdout.flush()
    r = k32.WaitForSingleObject(ctypes.c_void_p(h), INFINITE)
    k32.CloseHandle(ctypes.c_void_p(h))
    print("### il processo %s e' uscito alle %s (WaitForSingleObject %d)" % (winpid, time.strftime("%Y-%m-%d %H:%M:%S"), r))
    return 0


def prova():
    """### LE PROVE A SECCO (la carta sez. 16.5): l'attesa su un processo breve; la decisione su tre cartelle finte."""
    ok = True
    # ### l'attesa: un processo di 3 s; attendi deve tornare DOPO che esce, non prima
    p = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(3)"])
    t = time.time()
    attendi(p.pid)
    dt = time.time() - t
    fine = p.poll()
    print("### ATTESA: tornata dopo %.2f s; il processo uscito: %s" % (dt, fine is not None))
    ok &= fine is not None and dt >= 2.5
    # ### DEVE TORNARE SUBITO: un pid che non c'e' piu'
    t = time.time()
    rc = attendi(p.pid)
    print("### ATTESA su un processo uscito: codice %d dopo %.2f s" % (rc, time.time() - t))
    tmp = tempfile.mkdtemp()
    try:
        def stato(d, k, buono=True):
            f = os.path.join(d, "stato_%05d.npz" % k)
            with open(f, "wb") as fh:
                fh.write(b"stato %d" % k)
            with open(f + ".sha1", "w", encoding="utf-8") as fh:
                fh.write((sha1(f) if buono else "0" * 40) + "  " + os.path.basename(f) + "\n")
        casi = []
        a = os.path.join(tmp, "scatto"); os.makedirs(a); stato(a, 39750); stato(a, 40000)
        open(os.path.join(a, "scatto.json"), "w").write("{}")
        casi.append((a, "SCATTO"))
        b = os.path.join(tmp, "limite"); os.makedirs(b); stato(b, 39750); stato(b, 40000)
        casi.append((b, "PROROGA"))
        c = os.path.join(tmp, "caduto"); os.makedirs(c); stato(c, 39500); stato(c, 39750)
        casi.append((c, "CADUTO"))
        e = os.path.join(tmp, "rotto"); os.makedirs(e); stato(e, 39750); stato(e, 40000, buono=False)
        casi.append((e, "CADUTO"))                                      # ### lo stato 40000 non integro: NON e' una proroga
        v = os.path.join(tmp, "vuoto"); os.makedirs(v)
        casi.append((v, "VUOTO"))
        for d, atteso in casi:
            got = decidi(d, 40000)[0]
            print("### DECISIONE %-7s: %s (attesa %s) %s" % (os.path.basename(d), got, atteso, "OK" if got == atteso else "SBAGLIATA"))
            ok &= got == atteso
        # ### DEVE FALLIRE: la stessa cartella del limite con un limite diverso non e' una proroga
        got = decidi(b, 50000)[0]
        print("### DEVE FALLIRE (il limite 50000 sulla cartella del 40000): %s %s" % (got, "OK, non e' PROROGA" if got != "PROROGA" else "SBAGLIATA"))
        ok &= got != "PROROGA"
    finally:
        shutil.rmtree(tmp)
    print("### LE PROVE A SECCO: %s" % ("PASSANO" if ok else "NON PASSANO"))
    return 0 if ok else 1


def main(argv):
    if argv[0] == "attendi":
        return attendi(argv[1])
    if argv[0] == "decidi":
        w, u = decidi(argv[1], int(argv[2]))
        print(w if u is None else "%s %d %s" % (w, u[0], u[1]))
        return CODICI[w]
    if argv[0] == "prova":
        return prova()
    print("uso: attendi WINPID | decidi CARTELLA K | prova")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
