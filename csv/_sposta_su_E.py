# -*- coding: utf-8 -*-
"""SPOSTA su `E:` degli archivi gia' serviti: COPIA, VERIFICA `sha1`, e SOLO POI rimuove.

⚠ L'ORDINE E' IL PUNTO, e non e' negoziabile: **copia -> `sha1` dei byte -> confronto -> rimozione**.
  Se il confronto non torna, **NON si rimuove niente** e si dichiara. **Il par.0-ter di
  `CLAUDE.md` lo dice gia': NON cancellare in locale senza checksum.**

⚠ `sha1` DEI BYTE COMPRESSI, cioe' del file `.pkl.gz` cosi' com'e' sul disco. NON del contenuto
  decompresso: quello richiederebbe di aprire il pickle, e **un confronto che deve provare che la
  COPIA e' riuscita deve guardare i BYTE COPIATI**, non cio' che rappresentano.

⚠ SOLA LETTURA sul simulatore e sui run: non importa niente, non esegue fisica. Puo' girare
  mentre un run e' in corso -- **ma NON sposta cartelle di run ATTIVI**, e la lista e' esplicita.

COSA SPOSTA, e perche' ognuna e' gia' servita:
  `_g4_corto`      cartella **scratch** dichiarata, si ripulisce da sola al giro dopo;
  `_g4_inerzia`    ha servito `T7` del sigillo di `MEM_MOTO`, **il cui esito e' committato**;
  `_g4_controllo`  il controllo dell'involucro e' **passato e committato** (`206/0`).
ASCII PURO.
"""
import hashlib
import io
import os
import shutil
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _QUI)
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, ".."))
DEST_E = r"E:\soliton_archivio\spostati_2026-09-22"
OUT = os.path.join(RADICE, "doc", "SPOSTATI_SU_E.md")
# ⚠ ESPLICITA: nessun glob, nessuna euristica. Si sposta CIO' CHE E' SCRITTO QUI.
DA_SPOSTARE = ["csv/_test_fork/_g4_corto",
               "csv/_test_fork/_g4_inerzia",
               "csv/_test_fork/_g4_controllo"]
# ⚠ I RUN ATTIVI: se una di queste compare in DA_SPOSTARE lo script SI FERMA.
MAI = ["csv/_test_fork/_g4_riferimento", "csv/_test_fork/_g4_senza_memmoto",
       "csv/_test_fork/_val600", "csv/_test_fork/_g3_senza_bifase"]


def sha1(p):
    h = hashlib.sha1()
    with open(p, "rb") as f:
        for blocco in iter(lambda: f.read(1 << 20), b""):
            h.update(blocco)
    return h.hexdigest()


def collaudo(W):
    """`P1-sexies`: il confronto su casi a risposta NOTA, e il caso che DEVE fallire."""
    W("COLLAUDO (`P1-sexies`), PRIMA di spostare\n" + "-" * 90 + "\n")
    import tempfile
    e = []
    d = tempfile.mkdtemp()
    a = os.path.join(d, "a.bin"); b = os.path.join(d, "b.bin"); c = os.path.join(d, "c.bin")
    io.open(a, "wb").write(b"x" * 5000)
    shutil.copy2(a, b)
    io.open(c, "wb").write(b"x" * 4999 + b"y")      # UN SOLO byte diverso, in fondo
    ok1 = (sha1(a) == sha1(b))
    W("K1 copia fedele -> stesso sha1 -> %s\n" % ("OK" if ok1 else "*** NO ***"))
    ok2 = (sha1(a) != sha1(c))
    W("K2 IL CASO CHE DEVE FALLIRE: UN SOLO byte diverso, IN FONDO al file -> %s\n"
      % ("OK: il confronto lo vede" if ok2 else "*** una copia TRONCA passerebbe ***"))
    e += [ok1, ok2]
    ok3 = not set(DA_SPOSTARE) & set(MAI)
    W("K3 nessuna cartella di RUN ATTIVO nella lista da spostare -> %s\n"
      % ("OK" if ok3 else "*** STO PER SPOSTARE UN RUN VIVO ***"))
    e.append(ok3)
    shutil.rmtree(d, ignore_errors=True)
    ok = all(e)
    W("-" * 90 + "\n  -> %s\n\n" % ("si sposta" if ok else "*** NON sposto ***"))
    return ok


def main():
    W = sys.stdout.write
    if not collaudo(W):
        return 1
    if not os.path.isdir(os.path.splitdrive(DEST_E)[0] + os.sep):
        W("*** `E:` non e' raggiungibile: NON sposto niente. ***\n")
        return 1
    righe = []
    tot = 0
    for rel in DA_SPOSTARE:
        src = os.path.join(RADICE, rel.replace("/", os.sep))
        if not os.path.isdir(src):
            righe.append((rel, "\u2014", 0, "ASSENTE: niente da spostare"))
            continue
        dst = os.path.join(DEST_E, os.path.basename(src))
        try:
            os.makedirs(dst)
        except OSError:
            pass
        for nome in sorted(os.listdir(src)):
            f_src = os.path.join(src, nome)
            if not os.path.isfile(f_src):
                continue
            f_dst = os.path.join(dst, nome)
            n = os.path.getsize(f_src)
            h1 = sha1(f_src)
            shutil.copy2(f_src, f_dst)
            h2 = sha1(f_dst)
            if h1 != h2:
                righe.append(("%s/%s" % (rel, nome), h1, n,
                              "*** SHA1 DIVERSO DOPO LA COPIA: NON RIMOSSO ***"))
                continue
            os.remove(f_src)                      # solo DOPO il confronto
            tot += n
            righe.append(("%s/%s" % (rel, nome), h1, n, "copiato, verificato, RIMOSSO da `C:`"))
    with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write("# SPOSTATI SU `E:` \u2014 **copia, `sha1`, e SOLO POI rimozione**\n\n")
        f.write("> Generato da `csv/_sposta_su_E.py`. **Destinazione:** `%s`\n>\n" % DEST_E)
        f.write("> **L'ordine e' il punto:** copia \u2192 `sha1` dei **byte compressi** \u2192\n")
        f.write("> confronto \u2192 **rimozione solo se il confronto torna**. Se non torna, il\n")
        f.write("> file **resta su `C:`** e la riga lo dice.\n\n")
        f.write("| file | `sha1` dei byte | byte | esito |\n|---|---|--:|---|\n")
        for a_, b_, c_, d_ in righe:
            f.write("| `%s` | `%s` | %d | %s |\n" % (a_, b_[:16], c_, d_))
        f.write("\n**Liberati da `C:`: %.1f MB** su %d file.\n" % (tot / 1e6, len(righe)))
        f.write("\n**\u26a0 Cosa NON e' stato toccato:** le cartelle dei run *(`_val600`, "
                "`_g3_senza_bifase`, `_g4_riferimento`, `_g4_senza_memmoto`)*. La lista dei "
                "divieti e' nel sorgente, e il collaudo `K3` verifica che non si incrocino.\n")
    W("spostati %d file, liberati %.1f MB. -> %s\n"
      % (len(righe), tot / 1e6, os.path.relpath(OUT, RADICE).replace("\\", "/")))
    print(io.open(OUT, encoding="utf-8").read())
    return 0


if __name__ == "__main__":
    sys.exit(main())
