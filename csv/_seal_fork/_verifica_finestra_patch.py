# -*- coding: utf-8 -*-
"""LA TRAIETTORIA DEL RUN E' INTATTA ATTRAVERSO LA FINESTRA IN CUI HO TOCCATO I FILE?

IL FATTO: il 2026-09-19, mentre il run a 6000 passi girava, ho patchato `_scena_video.py` (la
ripresa) e poi l'ho RIPRISTINATO -- tutto fra le ~15:55 e le 15:57:52. In quella finestra il run
ha scritto lo snapshot del passo 1860 (15:57:06), e quello del 1800 e' di PRIMA (15:54:16).

LA DOMANDA DI LUCA: come fai a essere sicuro che toccare i file mentre i processi girano non abbia
mescolato le cose? Il ragionamento dice di no -- Python compila il sorgente UNA VOLTA all'avvio e
non lo rilegge; il `.pyc` del driver e' del giorno prima e nessuno lo importa; gli snapshot sono
scritti dall'immagine IN MEMORIA. **Ma un ragionamento non e' una misura**, e questo repo ha gia'
pagato per la differenza.

LA PROVA: si riparte dallo snapshot del passo 1800 -- scritto PRIMA che toccassi qualunque cosa --
e si rigioca fino al 1860, cioe' ATTRAVERSO la finestra. Se lo snapshot rigenerato e' identico a
quello che il run ha scritto DURANTE la finestra, la traiettoria non e' stata contaminata.

  W1  la rigiocata produce lo snapshot atteso
  W2  [DECISIVO] e' IDENTICO a quello scritto dal run durante la finestra
  W3  CONTROPROVA: il confronto sa ancora dire "diverso" (contro un altro passo)

*** NON TOCCA `_g6000` ***
Gli snapshot del run si leggono in SOLA LETTURA e si COPIANO in una cartella temporanea. La
rigiocata scrive solo li'. Il run continua a girare e non se ne accorge -- ed e' esattamente la
proprieta' che questa prova sta verificando.

Il criterio di confronto si IMPORTA da `_sigillo_archivio`, non si riscrive.
ASCII PURO.
"""
import glob
import gzip
import os
import pickle
import shutil
import subprocess
import sys
import time

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, RADICE)
sys.path.insert(0, _QUI)
from _sigillo_archivio import uguale_contenuto

DRIVER = os.path.join(RADICE, "csv", "_test_fork", "_scena_video_ripresa.py")
ARCH = os.path.join(RADICE, "csv", "_test_fork", "_g6000")
DA = int(sys.argv[1]) if len(sys.argv) > 1 else 1800      # scritto PRIMA della finestra
A = int(sys.argv[2]) if len(sys.argv) > 2 else 1860       # scritto DURANTE la finestra
PPF = 6

esiti = []


def segna(n, ok, d):
    esiti.append((n, ok, d))
    print("%-4s %-6s %s" % (n, "PASS" if ok else "FAIL", d), flush=True)


def carica(p):
    ap = gzip.open if p.endswith(".gz") else open
    with ap(p, "rb") as f:
        return pickle.load(f)


def main():
    src_da = os.path.join(ARCH, "scena_%06d.pkl.gz" % DA)
    src_a = os.path.join(ARCH, "scena_%06d.pkl.gz" % A)
    for p in (src_da, src_a):
        if not os.path.exists(p):
            print("ASSENTE: %s" % p)
            return 2
    print("partenza : %s   (%s)" % (os.path.basename(src_da),
                                    time.strftime("%H:%M:%S", time.localtime(os.path.getmtime(src_da)))))
    print("bersaglio: %s   (%s)  <- scritto DURANTE la finestra"
          % (os.path.basename(src_a),
             time.strftime("%H:%M:%S", time.localtime(os.path.getmtime(src_a)))))
    tmp = os.path.join(RADICE, "csv", "_seal_fork", "_finestra_tmp")
    shutil.rmtree(tmp, ignore_errors=True)
    os.makedirs(tmp)
    try:
        shutil.copy2(src_da, os.path.join(tmp, "scena_%06d.pkl.gz" % DA))
        nframe = A // PPF
        cmd = [sys.executable, DRIVER, str(nframe), tmp, "--serie=%d" % ((A - DA) // PPF),
               "--riprendi"]
        print("comando  : %s" % " ".join(cmd[1:]))
        t0 = time.time()
        pr = subprocess.run(cmd, cwd=RADICE, capture_output=True, text=True,
                            encoding="utf-8", errors="replace", timeout=3600)
        dt = time.time() - t0
        rip = [r for r in (pr.stdout or "").splitlines() if "RIPRESA" in r]
        print("  %s" % (rip[0].strip() if rip else "*** nessuna riga RIPRESA ***"))
        rig = os.path.join(tmp, "scena_%06d.pkl.gz" % A)
        segna("W1", os.path.exists(rig) and pr.returncode == 0,
              "rigiocata %d -> %d in %.0f s, rc=%s" % (DA, A, dt, pr.returncode))
        if not os.path.exists(rig):
            for r in (pr.stdout + pr.stderr).splitlines()[-12:]:
                print("     | " + r)
            return 1

        a, b = carica(src_a)["attrs"], carica(rig)["attrs"]
        kc = sorted(set(a) & set(b))
        soli = sorted(set(a) ^ set(b))
        guai = [k for k in kc if not uguale_contenuto(a[k], b[k])]
        segna("W2", not guai and not soli and len(kc) > 50,
              "%d campi confrontati, %d diversi%s"
              % (len(kc), len(guai), ("  -> " + str(guai[:6])) if guai else "  -> IDENTICO"))
        if soli:
            print("     chiavi in uno solo: %s" % soli[:8])

        altro = sorted(glob.glob(os.path.join(ARCH, "scena_??????.pkl.gz")))[0]
        c = carica(altro)["attrs"]
        kk = sorted(set(c) & set(b))
        div = [k for k in kk if not uguale_contenuto(c[k], b[k])]
        segna("W3", len(div) > 0,
              "contro %s: %d campi diversi -- il confronto NON e' cieco"
              % (os.path.basename(altro), len(div)))

        print("")
        ok = sum(1 for _, o, _ in esiti if o)
        print("ESITO: %d/%d" % (ok, len(esiti)))
        print("")
        if ok == len(esiti):
            print("VERDETTO: LA TRAIETTORIA E' INTATTA. Ripartendo da uno snapshot scritto PRIMA")
            print("  che toccassi i file, si riottiene ESATTAMENTE lo snapshot che il run ha")
            print("  scritto DURANTE la finestra. Toccare il sorgente non ha contaminato il run.")
            print("  NB: prova UNA finestra, quella misurata. Non e' un teorema su ogni caso.")
        else:
            print("VERDETTO: NON CONFERMATO. Le righe FAIL dicono dove, e va riportato COSI'")
            print("  invece di cercarne una spiegazione comoda.")
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
