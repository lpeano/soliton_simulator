# -*- coding: utf-8 -*-
"""SIGILLO DELLA RIPRESA -- **un run interrotto e ripreso e' IDENTICO a uno continuo?**

LA DOMANDA, ed e' l'unica che conta: se il run a 6000 passi si rompe e riparte dall'ultimo
snapshot, la traiettoria che ne esce e' la STESSA che si sarebbe avuta senza interruzione?
**Se non lo e', la ripresa NON si usa**: un run che SEMBRA continuo e non lo e' e' peggio di un
run interrotto, perche' nessuno se ne accorge.

"Ma abbiamo salvato tutto, anche l'RNG" e' il ragionamento giusto e NON basta -- e' esattamente
quello che ci eravamo detti prima di `V6`, che poi e' FALLITO (su `conc_nodi`, e per capirlo sono
servite tre versioni dello strumento). Il fatto che una cosa debba funzionare non e' una misura.

COME
  braccio A: NF frame DI FILA.
  braccio B: NF/2 frame, STOP, poi `--riprendi` fino a NF.
  Si confronta lo stato FINALE, e anche gli intermedi comuni.

  R0  i due bracci producono gli stessi passi
  R1  [DECISIVO] lo stato finale di A e di B e' IDENTICO
  R2  anche gli snapshot INTERMEDI comuni sono identici
  R3  la ripresa NON ha sovrascritto gli snapshot preesistenti (mtime + dimensione)
  R4  CONTROPROVA: il criterio PUO' ancora dire "diverso" -- due passi diversi DEVONO differire.
      Senza R4, un R1 verde non distingue "identici" da "criterio rotto".

IL CRITERIO DI CONFRONTO NON SI RISCRIVE: si IMPORTA da `_sigillo_archivio`.
  Quello e' stato corretto una volta (il QUATTORDICESIMO criterio riscritto del programma: i byte
  di `pickle` dipendono dal MEMO e catturavano l'ALIASING, che non e' stato del sistema). Riscriverlo
  qui significherebbe avere DUE criteri che possono divergere -- e l'importazione stampa anche il
  timbro di quel file, che e' informazione, non rumore.
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
from _sigillo_archivio import uguale_contenuto      # IL criterio, non una sua copia

# IL DRIVER VERO, non una copia: la ripresa e' stata portata in `_scena_video.py` il
# 2026-09-19 e la copia e' stata rimossa. Si puo' passare un altro percorso da argv, cosi'
# questo sigillo resta rigirabile su un driver diverso invece di essere legato a un nome
# (Z31: quattro sigilli non erano piu' rigirabili perche' il loro termine di paragone era
# sparito).
DRIVER = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    RADICE, "csv", "_test_fork", "_scena_video.py")
NF = 12            # frame totali per braccio
OGNI = 3           # snapshot ogni 3 frame = 18 passi
META = NF // 2     # dove si "rompe" il braccio B

esiti = []


def segna(nome, ok, det):
    esiti.append((nome, ok, det))
    print("%-4s %-6s %s" % (nome, "PASS" if ok else "FAIL", det), flush=True)


def carica(p):
    ap = gzip.open if p.endswith(".gz") else open
    with ap(p, "rb") as f:
        return pickle.load(f)


def gira(dest, nframe, riprendi=False):
    cmd = [sys.executable, DRIVER, str(nframe), dest, "--serie=%d" % OGNI]
    if riprendi:
        cmd.append("--riprendi")
    t0 = time.time()
    pr = subprocess.run(cmd, cwd=RADICE, capture_output=True, text=True,
                        encoding="utf-8", errors="replace", timeout=7200)
    return pr, time.time() - t0


def serie(dest):
    out = {}
    for p in sorted(glob.glob(os.path.join(dest, "scena_??????.pkl*"))):
        out[int(os.path.basename(p).split("_")[1].split(".")[0])] = p
    return out


def main():
    base = os.path.join(RADICE, "csv", "_seal_fork", "_ripresa_tmp")
    A, B = os.path.join(base, "A"), os.path.join(base, "B")
    shutil.rmtree(base, ignore_errors=True)
    os.makedirs(A); os.makedirs(B)
    try:
        print("braccio A: %d frame di fila" % NF)
        prA, tA = gira(A, NF)
        print("braccio B: %d frame, poi STOP" % META)
        prB1, tB1 = gira(B, META)
        # cio' che B ha gia' scritto, PRIMA della ripresa: serve a R3
        prima = {k: (os.path.getmtime(v), os.path.getsize(v)) for k, v in serie(B).items()}
        print("braccio B: RIPRESA fino a %d frame" % NF)
        prB2, tB2 = gira(B, NF, riprendi=True)
        for nome, pr in (("A", prA), ("B1", prB1), ("B2", prB2)):
            if pr.returncode != 0:
                print("  *** braccio %s rc=%s ***" % (nome, pr.returncode))
                for r in (pr.stdout + pr.stderr).splitlines()[-12:]:
                    print("     | " + r)
        sA, sB = serie(A), serie(B)
        print("")
        print("  A: passi %s" % sorted(sA))
        print("  B: passi %s" % sorted(sB))
        rip = [r for r in (prB2.stdout or "").splitlines() if "RIPRESA" in r]
        print("  %s" % (rip[0].strip() if rip else "*** nessuna riga RIPRESA nell'output di B2 ***"))
        print("  tempi: A %.0f s | B %.0f + %.0f s" % (tA, tB1, tB2))
        print("")

        segna("R0", sorted(sA) == sorted(sB) and len(sA) >= 2,
              "i due bracci hanno gli STESSI passi: %s" % sorted(sA))
        if not sA or not sB:
            segna("R1", False, "NON ESEGUITO: manca un braccio")
            return 1

        # --- R1 [DECISIVO] -------------------------------------------------------------
        pfin = max(sA)
        a, b = carica(sA[pfin])["attrs"], carica(sB[pfin])["attrs"]
        kc = sorted(set(a) & set(b))
        soli = sorted(set(a) ^ set(b))
        guai = [k for k in kc if not uguale_contenuto(a[k], b[k])]
        segna("R1", not guai and not soli and len(kc) > 50,
              "stato finale al passo %d: %d campi confrontati, %d diversi%s"
              % (pfin, len(kc), len(guai),
                 ("  -> " + str(guai[:6])) if guai else "  -> IDENTICO"))
        if soli:
            print("     chiavi presenti in uno solo: %s" % soli[:8])

        # --- R2: anche gli intermedi ----------------------------------------------------
        inter = [p for p in sorted(set(sA) & set(sB)) if p != pfin]
        g2 = []
        for p in inter:
            aa, bb = carica(sA[p])["attrs"], carica(sB[p])["attrs"]
            d = [k for k in sorted(set(aa) & set(bb)) if not uguale_contenuto(aa[k], bb[k])]
            if d:
                g2.append("passo %d: %s" % (p, d[:4]))
        segna("R2", not g2 and bool(inter),
              "%d snapshot intermedi confrontati, %d con differenze%s"
              % (len(inter), len(g2), ("  -> " + str(g2[:3])) if g2 else ""))

        # --- R3: la ripresa NON distrugge -----------------------------------------------
        dopo = {k: (os.path.getmtime(v), os.path.getsize(v)) for k, v in serie(B).items()}
        intatti = [k for k in prima if dopo.get(k) == prima[k]]
        segna("R3", sorted(intatti) == sorted(prima) and bool(prima),
              "gli snapshot scritti PRIMA dell'interruzione sono INTATTI: %d su %d"
              % (len(intatti), len(prima)))

        # --- R4: CONTROPROVA, il criterio deve poter dire "diverso" ----------------------
        if len(sA) >= 2:
            p1, p2 = sorted(sA)[0], sorted(sA)[-1]
            x, y = carica(sA[p1])["attrs"], carica(sA[p2])["attrs"]
            kk = sorted(set(x) & set(y))
            div = [k for k in kk if not uguale_contenuto(x[k], y[k])]
            segna("R4", len(div) > 0,
                  "due passi DIVERSI (%d contro %d) danno %d campi diversi: il criterio NON e' "
                  "cieco" % (p1, p2, len(div)))
        print("")
        ok = sum(1 for _, o, _ in esiti if o)
        print("ESITO: %d/%d" % (ok, len(esiti)))
        print("")
        dec = [n for n, o, _ in esiti if not o and n in ("R1", "R4")]
        if dec:
            print("VERDETTO: LA RIPRESA NON E' CONSISTENTE (%s). NON SI USA." % ", ".join(dec))
            print("  Un run ripreso che diverge da uno continuo produce una traiettoria che sembra")
            print("  continua e non lo e'. Meglio ripartire da zero SAPENDOLO.")
        elif ok == len(esiti):
            print("VERDETTO: LA RIPRESA E' CONSISTENTE. Un run interrotto e ripreso da uno snapshot")
            print("  da' lo STESSO stato di un run continuo, e non distrugge l'archivio esistente.")
            print("  NB: provato su UNA scena, UN seme, %d frame. Dimostra che il MECCANISMO non" % NF)
            print("  perde stato, NON che ogni ripresa possibile combaci.")
        else:
            print("VERDETTO: i decisivi passano, ma qualche voce no. Le righe FAIL dicono quali.")
        return 0
    finally:
        shutil.rmtree(base, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
