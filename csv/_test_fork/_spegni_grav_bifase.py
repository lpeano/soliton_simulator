# -*- coding: utf-8 -*-
"""PROVA DI SPEGNIMENTO: la GRAVITA' BIFASE. `GRAV_BIFASE = False` imposto SUL MODULO. [G3]

⚠ NON MODIFICA NE' IL SIMULATORE NE' IL DRIVER. Nemmeno di un byte.
  Questo file e' un INVOLUCRO: importa `soliton_simulator`, **avvolge `_applica_flag`** in modo
  che subito DOPO che il driver ha applicato i suoi flag la costante `GRAV_BIFASE` venga rimessa
  a `False` sul modulo, e poi **esegue il driver com'e'** con `runpy`.

  **Perche' avvolgere `_applica_flag` invece di assegnare e basta:** il driver chiama
  `_applica_flag(a)` DOPO l'import, e quella funzione scrive i globali del modulo. Assegnare
  prima verrebbe **sovrascritto in silenzio** -- ed e' esattamente la classe di difetto che
  `CLAUDE.md` chiama *«un default ribaltato converte i rami di controllo in duplicati del ramo di
  prova»*. Si **verifica** che dopo l'avvolgimento il valore sia davvero `False`, e se non lo e'
  **ci si ferma**.

DUE MODI, e il primo NON e' facoltativo:

  --controllo   IL CONTROLLO POSITIVO. Gira **20 frame (120 passi)** LASCIANDO `GRAV_BIFASE`
                COM'E', e confronta lo stato con `csv/_test_fork/_val600/scena_000120.pkl.gz`.
                **Se non coincide, l'involucro NON riproduce la validazione**, e allora qualunque
                differenza misurata in `--prova` sarebbe attribuibile all'involucro invece che
                allo spegnimento. **E' il termine di paragone: senza, la prova non vale.**
                *(`P1-sexies`: il caso che DEVE riuscire. Il caso che DEVE fallire e' il suo
                gemello: con `GRAV_BIFASE` SPENTO lo stesso confronto DEVE differire -- se
                coincidesse, il flag sarebbe inerte e la prova di spegnimento sarebbe vuota.)*

  --prova       LA PROVA. 100 frame (600 passi) con `GRAV_BIFASE = False`, serie ogni 20 frame,
                invarianti accesi, **stessa scena e stessi flag della validazione**. Esce in
                `csv/_test_fork/_g3_senza_bifase/`, e si legge con
                `_letture_validazione.py --dir=...`, cioe' **con gli STESSI criteri assoluti**.

⚠ NON si confronta con le epoche precedenti (par.9-bis): si legge contro i criteri ASSOLUTI.
ASCII PURO.
"""
import gzip
import io
import os
import pickle
import runpy
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, RADICE)
DRIVER = os.path.join(RADICE, "csv", "_test_fork", "_scena_video.py")
RIF120 = os.path.join(RADICE, "csv", "_test_fork", "_val600", "scena_000120.pkl.gz")

# ⚠ LA RIGA DELLA VALIDAZIONE, VERBATIM da `doc/STATO_RUN.md`. Cambia SOLO il numero di frame e
#   la cartella di destinazione: tutto il resto e' identico, ed e' il punto.
COMUNE = ["--sep=4.0", "--serie=20", "--chi-basc=on", "--chi-coop=on", "--scala-min=off",
          "--coes-adim=on", "--peq-esatto=on", "--peq-nascita-locale=on",
          "--scala-min-passo=on", "--coes-causale=on", "--anom-simm=on", "--invarianti=on"]


def avvolgi(spegni):
    """Avvolge `_applica_flag` sul MODULO. Ritorna una funzione che dice cosa e' successo."""
    import soliton_simulator as S
    orig = S._applica_flag
    visto = {"chiamate": 0, "prima": None, "dopo": None}

    def _wrap(a):
        r = orig(a)
        visto["chiamate"] += 1
        visto["prima"] = bool(S.GRAV_BIFASE)
        if spegni:
            S.GRAV_BIFASE = False
        visto["dopo"] = bool(S.GRAV_BIFASE)
        return r

    S._applica_flag = _wrap
    return visto


def traccia_per_scrittore(S):
    """La traccia SALITE/DISCESE per scrittore di `d0`, LA STESSA DI `Z102`.

    ⚠ PURE-READ: sostituisce `_traccia_d0` con una funzione che legge `prima` e `self.d0` e
      somma, **senza scrivere stato**. E' lo stesso impianto gia' girato in
      `_somma_per_scrittore_d0.py` e in `_dove_spinge_la_gravita.py`.

    ⚠ PERCHE' SALITE E DISCESE SEPARATE, e non il saldo: **un saldo piccolo puo' nascere da due
      termini enormi che quasi si cancellano** -- sistema fragile -- **oppure da due termini
      piccoli** -- sistema quieto. **Il saldo da solo non distingue i due casi.**

    ⚠ I SITI CHE CONCATENANO (`S01`, `S06`, `S07`) cambiano la LUNGHEZZA di `d0`: li' il delta
      elemento-per-elemento NON ESISTE, e la riga porta `n/d`. Dichiarato, non nascosto.
    """
    conti = {}
    S.TRACCIA_D0 = True

    def traccia(self, sito, prima, pavimento=None):
        c = conti.setdefault(sito, dict(su=0.0, giu=0.0, n_su=0, n_giu=0, giri=0, salta=0))
        c["giri"] += 1
        dopo = np.asarray(self.d0, dtype=float)
        pri = np.asarray(prima, dtype=float)
        if len(pri) != len(dopo):
            c["salta"] += 1
            return
        dx = dopo - pri
        c["su"] += float(np.sum(dx[dx > 0.0]))
        c["giu"] += float(np.sum(dx[dx < 0.0]))
        c["n_su"] += int(np.sum(dx > 0.0))
        c["n_giu"] += int(np.sum(dx < 0.0))
    S.Rete._traccia_d0 = traccia
    return conti


def scrivi_scrittori(conti, dest, W, blob, seme, grav):
    """La tabella per scrittore, GENERATA DA CODICE (`P1-ter`), in `csv` e in testo."""
    p_txt = os.path.join(dest, "SOMMA_PER_SCRITTORE_d0.txt")
    p_csv = os.path.join(dest, "SOMMA_PER_SCRITTORE_d0.csv")
    tot = 0.0
    with io.open(p_txt, "w", encoding="utf-8", newline="\n") as f:
        f.write("# G3 -- SALITE e DISCESE di `d0` per SCRITTORE, con `GRAV_BIFASE=%s`\n" % grav)
        f.write("# blob simulatore (sha1 byte grezzi)=%s  seme=%s\n" % (blob, seme))
        f.write("# la stessa traccia di `Z102`, cosi' i due si confrontano riga per riga.\n")
        f.write("# ⚠ i siti che CONCATENANO portano `n/d`: li' il delta non esiste.\n\n")
        f.write("%-20s %14s %14s %14s | %10s | %6s %6s\n"
                % ("scrittore", "SALITE", "DISCESE", "SALDO", "|saldo|/tot", "giri", "salta"))
        f.write("-" * 100 + "\n")
        for s in sorted(conti):
            c = conti[s]
            if c["giri"] == c["salta"]:
                f.write("%-20s %14s %14s %14s | %10s | %6d %6d\n"
                        % (s, "n/d", "n/d", "n/d", "n/d", c["giri"], c["salta"]))
                continue
            sal = c["su"] + c["giu"]; lordo = c["su"] - c["giu"]
            tot += sal
            f.write("%-20s %14.6e %14.6e %14.6e | %10.4f | %6d %6d\n"
                    % (s, c["su"], c["giu"], sal, abs(sal) / max(lordo, 1e-300),
                       c["giri"], c["salta"]))
        f.write("-" * 100 + "\n")
        f.write("%-20s %14s %14s %14.6e\n" % ("SALDO TOTALE", "", "", tot))
    with io.open(p_csv, "w", encoding="utf-8", newline="\n") as f:
        f.write("# blob=%s seme=%s GRAV_BIFASE=%s\n" % (blob, seme, grav))
        f.write("scrittore,salite,discese,saldo,giri,salta,n_su,n_giu\n")
        for s in sorted(conti):
            c = conti[s]
            f.write("%s,%.9e,%.9e,%.9e,%d,%d,%d,%d\n"
                    % (s, c["su"], c["giu"], c["su"] + c["giu"], c["giri"], c["salta"],
                       c["n_su"], c["n_giu"]))
    W("  tabella per scrittore -> %s\n  e %s\n" % (p_txt, p_csv))
    return tot


def confronta(net, p_rif, W):
    """Confronto campo per campo con uno snapshot. Zero differenze = riproduce."""
    with gzip.open(p_rif, "rb") as f:
        rif = pickle.load(f)["attrs"]
    uguali = diversi = assenti = 0
    nomi_div = []
    for k in sorted(rif):
        if not hasattr(net, k):
            assenti += 1
            continue
        a = getattr(net, k)
        b = rif[k]
        try:
            aa = np.asarray(a)
            bb = np.asarray(b)
            if aa.shape != bb.shape:
                diversi += 1; nomi_div.append("%s(shape %s!=%s)" % (k, aa.shape, bb.shape))
                continue
            if aa.dtype.kind in "fc" or bb.dtype.kind in "fc":
                d = np.max(np.abs(aa.astype(float) - bb.astype(float))) if aa.size else 0.0
                if d == 0.0:
                    uguali += 1
                else:
                    diversi += 1; nomi_div.append("%s(max|d|=%.3e)" % (k, d))
            else:
                if np.array_equal(aa, bb):
                    uguali += 1
                else:
                    diversi += 1; nomi_div.append(k)
        except Exception as e:
            assenti += 1
            nomi_div.append("%s(non confrontabile: %s)" % (k, e))
    W("  campi UGUALI %d   DIVERSI %d   non confrontati %d\n" % (uguali, diversi, assenti))
    if nomi_div:
        W("  i primi diversi: %s\n" % ", ".join(nomi_div[:10]))
    return uguali, diversi


def main():
    modo = None
    for a in sys.argv[1:]:
        if a in ("--controllo", "--prova"):
            modo = a
    if modo is None:
        print(__doc__)
        print("*** serve --controllo oppure --prova. Il CONTROLLO va fatto PRIMA. ***")
        return 2

    os.chdir(RADICE)
    if modo == "--controllo":
        if not os.path.exists(RIF120):
            print("*** manca il riferimento %s: il controllo non e' possibile ***" % RIF120)
            return 1
        dest = os.path.join(RADICE, "csv", "_test_fork", "_g3_controllo")
        # ⚠ NESSUNA opzione in piu': il driver mette cio' che non riconosce nei POSIZIONALI, e
        #   `_ARGV[3]` e' la lista degli snapshot -> `int('--senza-db')` farebbe morire il run.
        #   E' il difetto che ha gia' ucciso il lancio della validazione (`:100` del driver).
        #   Quindi la riga del controllo e' quella della validazione, con SOLO i frame cambiati.
        argv = ["_scena_video.py", "20", dest] + COMUNE
        spegni = False
    else:
        dest = os.path.join(RADICE, "csv", "_test_fork", "_g3_senza_bifase")
        argv = ["_scena_video.py", "100", dest] + COMUNE + \
            ["--csv-progresso=%s" % os.path.join(dest, "prog.csv")]
        spegni = True

    try:
        os.makedirs(dest)
    except OSError:
        pass

    import soliton_simulator as S
    visto = avvolgi(spegni)
    conti = traccia_per_scrittore(S)      # ⚠ PURE-READ: legge e somma, non scrive stato
    sys.argv = list(argv)
    print("[G3] modo %s   GRAV_BIFASE spento dall'involucro: %s" % (modo, spegni), flush=True)
    print("[G3] argv: %s" % " ".join(argv), flush=True)

    runpy.run_path(DRIVER, run_name="__main__")

    W = sys.stdout.write
    W("\n" + "=" * 92 + "\n")
    W("L'INVOLUCRO: cosa ha fatto davvero\n")
    W("=" * 92 + "\n")
    W("  `_applica_flag` avvolto, chiamate: %d\n" % visto["chiamate"])
    W("  `GRAV_BIFASE` PRIMA dell'involucro: %s   DOPO: %s\n" % (visto["prima"], visto["dopo"]))
    W("  valore ORA sul modulo: %s\n" % bool(S.GRAV_BIFASE))
    if visto["chiamate"] == 0:
        W("  *** `_applica_flag` NON E' STATO CHIAMATO: l'involucro non ha agito. FERMO. ***\n")
        return 1
    if spegni and (visto["dopo"] or S.GRAV_BIFASE):
        W("  *** LO SPEGNIMENTO NON HA TENUTO: qualcuno lo ha riacceso dopo. FERMO. ***\n")
        return 1

    if modo == "--controllo":
        W("\n" + "=" * 92 + "\n")
        W("IL CONTROLLO POSITIVO: l'involucro riproduce la validazione?\n")
        W("  confronto dello stato al passo 120 con `_val600/scena_000120.pkl.gz`\n")
        W("=" * 92 + "\n")
        ug, dv = confronta(S.net, RIF120, W)
        if dv == 0 and ug > 0:
            W("\n  *** L'INVOLUCRO RIPRODUCE LA VALIDAZIONE: %d campi identici, 0 diversi.\n" % ug)
            W("      Qualunque differenza in `--prova` e' attribuibile allo SPEGNIMENTO. ***\n")
            return 0
        W("\n  *** L'INVOLUCRO NON RIPRODUCE LA VALIDAZIONE (%d campi diversi).\n" % dv)
        W("      LA PROVA DI SPEGNIMENTO NON SI FA finche' questo non e' risolto: una\n")
        W("      differenza misurata sarebbe attribuibile all'involucro invece che al flag. ***\n")
        return 1

    import hashlib
    _blob = hashlib.sha1(
        open(os.path.join(RADICE, "soliton_simulator.py"), "rb").read()).hexdigest()[:8]
    import inspect as _insp
    _seme = _insp.signature(S.Rete.__init__).parameters["seed"].default
    W("\nLA TRACCIA PER SCRITTORE (la stessa di `Z102`):\n")
    _tot = scrivi_scrittori(conti, dest, W, _blob, _seme, bool(S.GRAV_BIFASE))
    W("  saldo totale degli scrittori di `d0`: %+.6e\n" % _tot)

    W("\n  la lettura si fa con gli STESSI criteri assoluti della validazione:\n")
    W("    python csv/_test_fork/_letture_validazione.py --dir=%s\n"
      % os.path.relpath(dest, RADICE).replace("\\", "/"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
