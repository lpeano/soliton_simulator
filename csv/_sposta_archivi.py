# -*- coding: utf-8 -*-
"""SPOSTA GLI ARCHIVI `.pkl` GROSSI SU `E:` -- copia, verifica, e solo allora cancella.

Decisione di Luca (2026-09-21): si spostano **solo le cartelle di `.pkl` sopra i 300 MB**, su
`E:\\soliton_archivio\\` con la STESSA struttura di cartelle del repository.

⚠ LA VERIFICA E' IL `sha1` DEI BYTE DEL FILE **COMPRESSO**, originale contro copia. **NIENTE
  decompressione, NIENTE `pickle.load`.** E' la scelta giusta e va detto perche': **se i byte del
  `.gz` coincidono, il contenuto dentro coincide per forza** -- decomprimere non aggiunge
  informazione, aggiunge solo CPU. E quella CPU la pagherebbe **il ramo D che sta girando**
  *(il 20/9 un carico del genere porto' il ramo B da 25 a 84 s/frame)*.

IL RITO, per OGNI file e mai in parallelo:
  1. COPIA su `E:`
  2. VERIFICA `sha1` dei byte, originale == copia
  3. **solo se passa**: CANCELLA l'originale
  4. se fallisce: **NON cancella**, segna il file, prosegue col successivo

⚠ NON SI TOCCA la cartella del ramo D in corsa, e nessun file TRACCIATO da git.
⚠ IL REGISTRO si scrive MAN MANO (`doc/SPOSTAMENTO_archivi.tsv`): se il lavoro si interrompe a
  meta', il registro dice **esattamente** dove si e' arrivati.
⚠ SORVEGLIANZA DEL RAMO D: si leggono i `s/frame` dal suo log e **ci si ferma se salgono oltre il
  25 % della base**. La soglia e' OPERATIVA, non fisica, ed e' dichiarata qui invece che scelta in
  silenzio.
ASCII PURO.
"""
import hashlib
import io
import os
import re
import shutil
import subprocess
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _QUI)
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, ".."))
DEST = r"E:\soliton_archivio"
RAMO_D = os.path.normpath("csv/_test_fork/_ab_D")
LOG_D = os.path.join(RADICE, "csv", "_test_fork", "_ab_D_log.txt")
REG = os.path.join(RADICE, "doc", "SPOSTAMENTO_archivi.tsv")
SOGLIA_MB = 300
MARGINE = 1.25          # soglia OPERATIVA: ci si ferma se D rallenta di oltre il 25 %
RADICI = ("csv/_test_fork", "csv/_seal_fork", "csv", "db")


def sha1f(p, buf=1 << 20):
    h = hashlib.sha1()
    with open(p, "rb") as f:
        while True:
            b = f.read(buf)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def sframe():
    """I secondi per frame del ramo D, dall'ultima riga utile del suo log. None se non gira."""
    try:
        t = io.open(LOG_D, encoding="utf-8", errors="replace").read()
    except OSError:
        return None
    m = re.findall(r"([\d.]+)\s*s/frame", t)
    return float(m[-1]) if m else None


def gruppo(rel):
    d = os.path.dirname(rel)
    for r in RADICI:
        if d == r:
            return r + "  (sciolti)"
        if d.startswith(r + "/"):
            return r + "/" + d[len(r) + 1:].split("/")[0]
    return d


def elenco():
    trk = set(subprocess.check_output(["git", "ls-files"], text=True, cwd=RADICE).splitlines())
    g = {}
    for r, ds, fs in os.walk(RADICE):
        rn = os.path.relpath(r, RADICE)
        if ".git" in rn.split(os.sep):
            ds[:] = []
            continue
        if rn == RAMO_D or rn.startswith(RAMO_D + os.sep):
            ds[:] = []                      # il ramo D non si tocca, nemmeno in lettura
            continue
        for f in fs:
            if not f.endswith((".pkl", ".pkl.gz")):
                continue
            rel = os.path.relpath(os.path.join(r, f), RADICE).replace("\\", "/")
            if rel in trk:
                continue                    # un `.pkl` tracciato NON si sposta
            k = gruppo(rel)
            g.setdefault(k, [0, []])
            g[k][0] += os.path.getsize(os.path.join(RADICE, rel))
            g[k][1].append(rel)
    return {k: v[1] for k, v in g.items() if v[0] > SOGLIA_MB * 2 ** 20}


def main():
    grp = elenco()
    file = sorted(p for v in grp.values() for p in v)
    print("gruppi sopra i %d MB: %d   file: %d" % (SOGLIA_MB, len(grp), len(file)))
    base = sframe()
    print("ramo D, s/frame di base: %s   (stop se supera %.2f)"
          % (base, base * MARGINE if base else float("nan")))
    print("destinazione: %s" % DEST)
    os.makedirs(DEST, exist_ok=True)
    nuovo = not os.path.exists(REG)
    reg = io.open(REG, "a", encoding="utf-8", newline="\n")
    if nuovo:
        reg.write("# registro dello spostamento -- scritto MAN MANO\n")
        reg.write("vecchio\tnuovo\tsha1_byte\tbyte\tesito\n")
    ok = falliti = 0
    liberati = 0
    for k, p in enumerate(file):
        src = os.path.join(RADICE, p)
        if not os.path.exists(src):
            continue
        dst = os.path.join(DEST, p.replace("/", os.sep))
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        n = os.path.getsize(src)
        h1 = sha1f(src)
        try:
            shutil.copyfile(src, dst)
            h2 = sha1f(dst)
        except Exception as e:
            reg.write("%s\t%s\t%s\t%d\tERRORE_COPIA: %s\n" % (p, dst, h1, n, e))
            reg.flush()
            falliti += 1
            print("  ⚠ ERRORE COPIA  %s  (%s)" % (p, e))
            continue
        if h1 == h2:
            os.remove(src)                  # SOLO ORA
            reg.write("%s\t%s\t%s\t%d\tOK\n" % (p, dst, h1, n))
            ok += 1
            liberati += n
        else:
            reg.write("%s\t%s\t%s != %s\t%d\tSHA1_DIVERSO\n" % (p, dst, h1, h2, n))
            falliti += 1
            print("  ⚠ SHA1 DIVERSO, originale NON cancellato: %s" % p)
        reg.flush()
        if (k + 1) % 10 == 0 or k + 1 == len(file):
            sf = sframe()
            print("  %3d/%d  ok=%d falliti=%d  liberati %.2f GB   D: %s s/frame"
                  % (k + 1, len(file), ok, falliti, liberati / 2 ** 30, sf))
            if base and sf and sf > base * MARGINE:
                print("  *** IL RAMO D RALLENTA (%.2f > %.2f): MI FERMO QUI. ***" % (sf, base * MARGINE))
                break
    reg.close()
    print("")
    print("SPOSTATI %d file, FALLITI %d, liberati %.2f GB" % (ok, falliti, liberati / 2 ** 30))
    print("registro: %s" % os.path.relpath(REG, RADICE))
    return 0 if falliti == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
