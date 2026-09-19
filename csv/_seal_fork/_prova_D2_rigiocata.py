# -*- coding: utf-8 -*-
"""PROVA DEL DIFETTO D2 -- il criterio di CONTIGUITA' rifiutava il caso d'uso di --db-rigioca.
E LA PROVA CHE LA CURA FUNZIONA, sulla stessa scena.

NON E' UN SIGILLO: e' la PROVA DI UN FALLIMENTO, scritta e committata PRIMA della correzione
(CLAUDE.md par.5), e poi RIGIRATA dopo. Serviva perche' D2 veniva dalla LETTURA del codice e non
da una misura -- cio' che il par.9 vieta di fare.

IL DIFETTO, in una riga:
  infittire un archivio SIGNIFICA rigirare con --db-ogni PIU' PICCOLO; una serie 250/500/750 non
  e' CONTIGUA a cadenza 50; `_db_serie_verifica` pretendeva la contiguita'; quindi il SystemExit
  scattava PRIMA che --db-rigioca potesse infittire. Il criterio rifiutava il caso d'uso per cui
  la funzione esiste.

ESITO PRIMA DELLA CURA: 7/7, `_prova_D2_rigiocata_2026-09-19.txt` (commit edab9d4). QUEL FILE
RESTA, ed e' l'evidenza del "prima": questo script e' stato AGGIORNATO dopo averlo visto, e il
perche' va detto -- LA FIRMA DI `_db_serie_verifica` E' CAMBIATA (da `db_ogni` a `ver`), quindi lo
script vecchio si SCHIANTEREBBE invece di fallire. E' la stessa classe di difetto di `FintaRete`
(par.9: "non falliva: SI SCHIANTAVA"), e si evita aggiornando lo script NELLO STESSO COMMIT della
correzione, non dopo.

COSA MISURA, in due blocchi
  [P] IL CRITERIO, su una serie di soli NOMI (file vuoti). Si adatta alla firma che trova, e le
      attese si ROVESCIANO fra prima e dopo:
        P1  serie 250/500/750 alla sua cadenza     PRIMA: accettata      DOPO: RIFIUTATA
            (sono file VUOTI: 0 byte, nessun blob) -- il DOPO e' il rovesciamento di P4
        P2  la STESSA serie a cadenza 50           PRIMA: RIFIUTATA per CONTIGUITA'
                                                   DOPO: rifiutata, ma MAI per contiguita'
        P2b i passi sono tutti multipli di 50 -> il criterio di cadenza non c'entra
  [R] LA CURA, END-TO-END, su snapshot VERI prodotti da un run vero. E' il blocco che conta,
      perche' [P] prova il CRITERIO e [R] prova il PROGRAMMA:
        R1  un run da 100 passi con --db-ogni 25 --db-serie -> 4 snapshot (25/50/75/100)
        R2  quella serie verificata a cadenza 10 NON viene piu' rifiutata  <- IL DIFETTO CURATO
        R3  --db-rigioca 50 100 --db-ogni 10 GIRA e scrive 60/70/80/90
        R4  lo snapshot 000100, che gia' esisteva, NON e' stato SOVRASCRITTO (mtime e dimensione
            invariati): "salta e conta". L'archivio non e' distruggibile da una rigiocata.
        R5  il riepilogo "[db] ARCHIVIO: N scritti, N saltati, N FALLITI" COMPARE nell'output.
            E' il difetto D1: i contatori erano incrementati e MAI stampati.

⚠ COSA QUESTO SCRIPT NON PROVA, e non va fatto dire di piu': [R] usa UNA sola scena, UN seme e
150 passi. Non e' V6 (la rigiocata BYTE-IDENTICA): qui si prova che la rigiocata GIRA e non
distrugge, non che riproduca la stessa traiettoria. V6 e' un altro sigillo.

Il repo non viene sporcato: tutto in cartelle TEMPORANEE, rimosse alla fine.
ASCII PURO.
"""
import inspect
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
CADENZA_SERIE = 250
CADENZA_INFITTISCI = 50
PASSI = [250, 500, 750]

# [R]: la scena vera. Piccola di proposito -- deve provare il MECCANISMO, non la fisica.
R_PASSI, R_OGNI, R_INFITTISCI, R_DA = 100, 25, 10, 50

esiti = []

# Il criterio ha DUE firme nella storia del file: (base, db_ogni) prima, (base, ver) dopo.
# Si RILEVA invece di assumerla, cosi' lo script dice cosa ha trovato invece di schiantarsi.
_ARGS = list(inspect.signature(S._db_serie_verifica).parameters)
CURATO = _ARGS[-1] != "db_ogni"


def verifica(base, cadenza, net=None):
    if CURATO:
        return S._db_serie_verifica(base, net._versione_codice())
    return S._db_serie_verifica(base, cadenza)


def segna(nome, ok, dettaglio):
    esiti.append((nome, ok, dettaglio))
    print("%-5s %-6s %s" % (nome, "PASS" if ok else "FAIL", dettaglio), flush=True)


def _rete():
    """Una rete minima: serve SOLO per `_versione_codice()`, che e' un metodo di istanza."""
    return S.Rete(seed=1)


def blocco_P(net):
    tmp = tempfile.mkdtemp(prefix="provaD2_")
    try:
        base = os.path.join(tmp, "stato.pkl")
        for p in PASSI:
            with open(S._db_serie_path(base, p), "wb"):
                pass
        vuoti = [os.path.getsize(S._db_serie_path(base, p)) for p in PASSI]
        print("serie di soli NOMI: %s  dimensioni %s"
              % ([os.path.basename(S._db_serie_path(base, p)) for p in PASSI], vuoti))

        ser, guaio = verifica(base, CADENZA_SERIE, net)
        if CURATO:
            segna("P1", guaio is not None and "ILLEGGIBILE" in guaio,
                  "ROVESCIATO: i file da 0 byte sono RIFIUTATI -> %r" % (guaio or "")[:90])
        else:
            segna("P1", guaio is None and len(ser) == 3,
                  "cadenza %d: %d snapshot, guaio=%r" % (CADENZA_SERIE, len(ser), guaio))

        fuori = [p for p in PASSI if p % CADENZA_INFITTISCI != 0]
        segna("P2b", not fuori,
              "passi %s tutti multipli di %d -> un rifiuto per CADENZA sarebbe ingiustificato"
              % (PASSI, CADENZA_INFITTISCI))

        ser2, guaio2 = verifica(base, CADENZA_INFITTISCI, net)
        contig = bool(guaio2 and "CONTIGUA" in guaio2)
        if CURATO:
            segna("P2", not contig,
                  "ROVESCIATO: nessun rifiuto per CONTIGUITA' -> %r" % (guaio2 or "")[:90])
        else:
            segna("P2", contig,
                  "cadenza %d: guaio=%r" % (CADENZA_INFITTISCI, guaio2))
        return contig
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def blocco_R(net):
    """END-TO-END su snapshot VERI. E' il blocco che decide."""
    tmp = tempfile.mkdtemp(prefix="provaD2R_")
    try:
        base = os.path.join(tmp, "stato.pkl")
        csv = os.path.join(tmp, "out.csv")
        comune = [sys.executable, SIM, "--batch", "--sep", "8", "--seed", "900",
                  "--csv", csv, "--sync-db", base, "--db-serie"]

        # --- R1: il run che COSTRUISCE l'archivio ---------------------------------------
        cmd1 = comune + ["--passi", str(R_PASSI), "--ogni", "50", "--db-ogni", str(R_OGNI)]
        print("")
        print("R1 comando: %s" % " ".join(cmd1[2:]))
        t0 = time.time()
        p1 = subprocess.run(cmd1, cwd=RADICE, capture_output=True, text=True,
                            encoding="utf-8", errors="replace", timeout=1800)
        dt1 = time.time() - t0
        ser1 = S._db_serie_esistenti(base)
        attesi = list(range(R_OGNI, R_PASSI + 1, R_OGNI))
        segna("R1", [s for s, _ in ser1] == attesi,
              "run %d passi @%d in %.0f s -> snapshot %s (attesi %s)"
              % (R_PASSI, R_OGNI, dt1, [s for s, _ in ser1], attesi))
        if not ser1:
            print("--- output R1 ---")
            for r in [r for r in (p1.stdout + p1.stderr).splitlines() if r.strip()][-12:]:
                print("   " + r)
            return False

        # --- R2: la verifica alla cadenza FITTA, che PRIMA rifiutava ---------------------
        _s, guaio = verifica(base, R_INFITTISCI, net)
        segna("R2", guaio is None,
              "serie %s verificata a cadenza %d -> guaio=%r  (PRIMA: 'serie NON CONTIGUA')"
              % ([s for s, _ in ser1], R_INFITTISCI, guaio))

        # --- R3/R4/R5: la rigiocata vera -------------------------------------------------
        prima = {os.path.basename(p): (os.path.getmtime(p), os.path.getsize(p)) for _, p in ser1}
        cmd2 = comune + ["--passi", str(R_PASSI), "--ogni", "50",
                         "--db-ogni", str(R_INFITTISCI),
                         "--db-rigioca", str(R_DA), str(R_PASSI)]
        print("")
        print("R3 comando: %s" % " ".join(cmd2[2:]))
        t0 = time.time()
        p2 = subprocess.run(cmd2, cwd=RADICE, capture_output=True, text=True,
                            encoding="utf-8", errors="replace", timeout=1800)
        dt2 = time.time() - t0
        out2 = (p2.stdout or "") + (p2.stderr or "")
        ser2 = S._db_serie_esistenti(base)
        nuovi = sorted(set(s for s, _ in ser2) - set(s for s, _ in ser1))
        att_nuovi = [s for s in range(R_DA + R_INFITTISCI, R_PASSI, R_INFITTISCI)]
        segna("R3", p2.returncode == 0 and nuovi == att_nuovi,
              "rigiocata %d->%d @%d in %.0f s, rc=%s -> NUOVI %s (attesi %s)"
              % (R_DA, R_PASSI, R_INFITTISCI, dt2, p2.returncode, nuovi, att_nuovi))

        dopo = {os.path.basename(p): (os.path.getmtime(p), os.path.getsize(p)) for _, p in ser2}
        intatti = [k for k in prima if dopo.get(k) == prima[k]]
        segna("R4", sorted(intatti) == sorted(prima),
              "gli snapshot preesistenti sono INTATTI (mtime+dimensione): %d su %d"
              % (len(intatti), len(prima)))

        riga = [r for r in out2.splitlines() if "ARCHIVIO:" in r]
        segna("R5", bool(riga), "il riepilogo dei contatori COMPARE: %s"
              % (riga[0].strip() if riga else "ASSENTE -- D1 NON e' curato"))
        print("")
        print("--- righe [db] della rigiocata ---")
        for r in [r for r in out2.splitlines() if "[db]" in r][-8:]:
            print("   " + r)
        return True
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    print("criterio rilevato: firma %s -> codice %s"
          % (tuple(_ARGS), "CURATO" if CURATO else "PRE-CURA"))
    print("")
    net = _rete()
    contig = blocco_P(net)
    if CURATO:
        blocco_R(net)

    print("")
    n_ok = sum(1 for _, ok, _ in esiti if ok)
    print("ESITO: %d/%d" % (n_ok, len(esiti)))
    print("")
    if not CURATO:
        print("VERDETTO: D2 E' PRESENTE E DIMOSTRATO." if contig else
              "VERDETTO: D2 NON riprodotto -- NON correggere nulla finche' non si capisce perche'.")
    elif n_ok == len(esiti):
        print("VERDETTO: D2 E' CURATO, e la cura e' provata END-TO-END su snapshot VERI.")
        print("  Una serie a cadenza %d si infittisce a cadenza %d, gli snapshot preesistenti"
              % (R_OGNI, R_INFITTISCI))
        print("  NON vengono sovrascritti, e il conteggio si DICHIARA (D1).")
        print("  NON e' V6: qui si prova che la rigiocata GIRA e non distrugge, NON che riproduca")
        print("  la stessa traiettoria. Quello e' un altro sigillo.")
    else:
        print("VERDETTO: LA CURA NON E' COMPLETA. Le righe FAIL qui sopra dicono dove.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
