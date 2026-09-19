# -*- coding: utf-8 -*-
"""PROVA DEL DIFETTO D2 -- il criterio di CONTIGUITA' rifiuta il caso d'uso di --db-rigioca.

NON E' UN SIGILLO: e' la PROVA DI UN FALLIMENTO, scritta e committata PRIMA della correzione
(CLAUDE.md par.5). Serve a dimostrare che il difetto e' REALE, perche' finora veniva dalla
LETTURA del codice e non da una misura -- ed e' esattamente cio' che il par.9 vieta di fare
("un pattern che spiega tutto va verificato contro la fonte prima di scriverlo").

IL DIFETTO, in una riga:
  infittire un archivio SIGNIFICA rigirare con --db-ogni PIU' PICCOLO; una serie 250/500/750 non
  e' CONTIGUA a cadenza 50; `_db_serie_verifica` pretende la contiguita'; quindi il SystemExit
  scatta PRIMA che --db-rigioca possa infittire. Il criterio rifiuta il caso d'uso per cui la
  funzione esiste.

IL VALORE SOTTO IPOTESI NULLA (par.9), ed e' il punto che rende la prova conclusiva:
  il mandato chiedeva di rifiutare "una serie di un ALTRO RUN", e il commit 2c92b9d dichiarava
  due criteri: (a) un blob qualsiasi differisce, (b) un _db_step non e' multiplo di --db-ogni.
  CON db_ogni = 50 I PASSI 250/500/750 SONO TUTTI MULTIPLI DI 50: il criterio (b) NON scatta.
  Quindi se il rifiuto avviene, viene ESCLUSIVAMENTE dalla CONTIGUITA' -- il criterio AGGIUNTO,
  mai chiesto. Non c'e' altra spiegazione possibile, e P2b lo verifica invece di asserirlo.

COSA MISURA
  P1  serie 250/500/750 a cadenza 250 -> DEVE passare (e' la serie legittima di quel run).
  P2  la STESSA serie a cadenza  50   -> il rifiuto. E' il difetto.
  P2b i passi sono tutti multipli di 50 -> il criterio (b) del mandato NON c'entra.
  P2c il motivo dichiarato dal codice e' la CONTIGUITA', non altro.
  P3  END-TO-END: il simulatore vero, invocato con --db-rigioca 250 500 --db-ogni 50, esce con
      SystemExit senza girare un passo. P1/P2 provano la FUNZIONE, P3 prova il PROGRAMMA.
  P4  gli snapshot della serie sono file VUOTI (0 byte): non sono nemmeno pickle, non hanno un
      blob. La verifica a cadenza 250 LI ACCETTA lo stesso.
      E' il rovesciamento esatto del mandato: RIFIUTA una cadenza legittima, ACCETTA file che non
      hanno alcun blob da controllare. Il discriminante doveva essere IL BLOB.

DOPO LA CORREZIONE questo stesso script va rigirato: P2 e P3 devono ROVESCIARSI (nessun rifiuto),
P1 deve restare verde, e P4 deve rovesciarsi anch'esso (un file senza blob va RIFIUTATO).
Finche' non e' corretto, il verdetto atteso e' "D2 PRESENTE".

NESSUNA FISICA VIENE TOCCATA: la serie e' fatta di file vuoti in una cartella TEMPORANEA, che
viene rimossa alla fine. Il repo non viene sporcato.
ASCII PURO.
"""
import os
import shutil
import subprocess
import sys
import tempfile
import time

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, RADICE)
import soliton_simulator as S

SIM = os.path.join(RADICE, "soliton_simulator.py")
CADENZA_SERIE = 250          # la cadenza con cui l'archivio e' stato scritto
CADENZA_INFITTISCI = 50      # la cadenza con cui lo si vuole INFITTIRE
PASSI = [250, 500, 750]

esiti = []


def segna(nome, ok, dettaglio):
    esiti.append((nome, ok, dettaglio))
    print("%-5s %-6s %s" % (nome, "PASS" if ok else "FAIL", dettaglio), flush=True)


def main():
    tmp = tempfile.mkdtemp(prefix="provaD2_")
    try:
        base = os.path.join(tmp, "stato.pkl")
        # LA SERIE FINTA: solo i NOMI. `_db_serie_esistenti` fa glob+regex e NON apre i file,
        # quindi per provare il RIFIUTO non serve un run vero -- e il fatto che non serva e'
        # gia' meta' del rilievo (P4).
        for p in PASSI:
            with open(S._db_serie_path(base, p), "wb"):
                pass
        vuoti = [os.path.getsize(S._db_serie_path(base, p)) for p in PASSI]
        print("serie costruita: %s"
              % [os.path.basename(S._db_serie_path(base, p)) for p in PASSI])
        print("dimensioni (byte): %s" % vuoti)
        print("")

        # --- P1: la serie legittima, alla SUA cadenza -------------------------------------
        ser, guaio = S._db_serie_verifica(base, CADENZA_SERIE)
        segna("P1", guaio is None and len(ser) == 3,
              "cadenza %d: %d snapshot, guaio=%r" % (CADENZA_SERIE, len(ser), guaio))

        # --- P2b: il criterio (b) del mandato NON puo' spiegare il rifiuto -----------------
        fuori = [p for p in PASSI if p % CADENZA_INFITTISCI != 0]
        segna("P2b", not fuori,
              "passi %s tutti multipli di %d -> il criterio (b) del mandato NON scatta; "
              "se P2 rifiuta, e' SOLO la contiguita'" % (PASSI, CADENZA_INFITTISCI))

        # --- P2: IL DIFETTO ---------------------------------------------------------------
        ser2, guaio2 = S._db_serie_verifica(base, CADENZA_INFITTISCI)
        rifiuta = guaio2 is not None
        segna("P2", rifiuta,
              "cadenza %d (infittimento): guaio=%r" % (CADENZA_INFITTISCI, guaio2))
        contig = bool(rifiuta and "CONTIGUA" in guaio2)
        segna("P2c", contig,
              "il motivo del rifiuto e' la CONTIGUITA' (non il blob, non la cadenza)")

        # --- P4: accetta file senza blob ---------------------------------------------------
        segna("P4", all(v == 0 for v in vuoti) and guaio is None,
              "gli snapshot sono 0 byte -- nessun pickle, nessun blob -- e P1 LI ACCETTA: "
              "il criterio implementato non guarda cio' che il mandato chiedeva")

        # --- P3: END-TO-END sul programma vero ---------------------------------------------
        cmd = [sys.executable, SIM, "--batch", "--nmasse", "1", "--sep", "8",
               "--passi", "300", "--ogni", "50", "--seed", "900",
               "--sync-db", base, "--db-ogni", str(CADENZA_INFITTISCI),
               "--db-serie", "--db-rigioca", "250", "500"]
        print("")
        print("P3 comando: %s" % " ".join(cmd))
        t0 = time.time()
        pr = subprocess.run(cmd, cwd=RADICE, capture_output=True, text=True,
                            encoding="utf-8", errors="replace", timeout=900)
        dt = time.time() - t0
        out = (pr.stdout or "") + (pr.stderr or "")
        rifiuto_e2e = ("RIFIUTO DI PARTIRE" in out) and pr.returncode != 0
        segna("P3", rifiuto_e2e,
              "returncode=%s in %.1f s -- il programma RIFIUTA di infittire" % (pr.returncode, dt))
        # il rifiuto deve avvenire PRIMA della fisica: nessuno snapshot nuovo, nessuno toccato
        dopo = sorted(os.path.basename(p) for _, p in S._db_serie_esistenti(base))
        atteso = sorted(os.path.basename(S._db_serie_path(base, p)) for p in PASSI)
        segna("P3b", dopo == atteso,
              "nessuno snapshot creato ne' toccato: %s" % dopo)
        print("")
        print("--- ultime righe dell'output di P3 ---")
        for r in [r for r in out.splitlines() if r.strip()][-8:]:
            print("   " + r)

        # --- VERDETTO ----------------------------------------------------------------------
        print("")
        n_ok = sum(1 for _, ok, _ in esiti if ok)
        print("ESITO: %d/%d" % (n_ok, len(esiti)))
        presente = rifiuta and contig and rifiuto_e2e
        print("")
        if presente:
            print("VERDETTO: D2 E' PRESENTE E DIMOSTRATO.")
            print("  Una serie scritta a cadenza %d NON puo' essere infittita a cadenza %d:"
                  % (CADENZA_SERIE, CADENZA_INFITTISCI))
            print("  il rifiuto scatta per CONTIGUITA', che e' un criterio AGGIUNTO rispetto al")
            print("  mandato, e scatta PRIMA che --db-rigioca faccia qualunque cosa.")
            print("  Il difetto NON e' un errore di programmazione: e' una DIVERGENZA DAL MANDATO.")
        else:
            print("VERDETTO: D2 NON riprodotto in questa forma. NON correggere nulla finche'")
            print("  non si capisce perche': una prova che non fallisce dove ci si aspetta")
            print("  significa che la diagnosi e' sbagliata, non che il difetto non c'e'.")
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
