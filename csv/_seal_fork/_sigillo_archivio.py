# -*- coding: utf-8 -*-
"""SIGILLO V0-V9 dell'ARCHIVIO (serie numerata + gzip + rigiocata).

Progettazione fissata PRIMA: doc/TASK_HISTORY/2026-09-19_archivio-serie.md par.2.4 (commit 2c92b9d,
corretto in 0ed3386). I tre DECISIVI sono V1, V2 (byte-identita', BLOCCANTI) e V6 (la rigiocata
combacia).

IL CONFRONTO E' SUI BYTE, E SI CONTA QUANTI ARRAY SONO STATI CONFRONTATI.
  "max|A-B| = 0.000e+00 puo' significare NESSUN CONFRONTO" (par.9, successo davvero: 3209 nodi
  contro 3073, 32 shape su 32 divergenti, e lo zero era il massimo di un insieme VUOTO).
  Quindi ogni voce stampa N_CONFRONTATI e FALLISCE se sono zero, e le chiavi mancanti da una parte
  o dall'altra sono un FAIL esplicito, non un'omissione silenziosa.

IL BLOB VECCHIO SI ESTRAE IN BINARIO, ANCORATO AL SUO SHA
  `git cat-file -p b9e07c73`, mai `git checkout` e mai `HEAD:` -- HEAD si sposta col lavoro, e
  `git checkout` riscrive le newline LF->CRLF (par.5-quinquies, la trappola CRLF di C18).

COSA MISURA
  V0  il blob dei byte grezzi del simulatore che sta girando: si DICHIARA, non si assume.
  V1  [BLOCCANTE] flag OFF == codice PRE-ARCHIVIO (b9e07c73). Se cade, ho toccato la fisica.
  V2  [BLOCCANTE] flag ON  == flag OFF. Il salvataggio non deve PERTURBARE (precedente:
      lambda_vuoto). Si confronta la fisica, non il formato dei file.
  V3  un run di k*N passi con --db-ogni N produce ESATTAMENTE k file, ai passi giusti.
  V4  il passo nel NOME == `_db_step` nei DATI, su OGNI file della serie.
  V5  round-trip: salva -> ricarica -> le tre strutture di Z53 (conc_nodi, conc_archi, masse_info)
      tornano IDENTICHE. E' il pezzo che il filtro di salva_stato scartava in silenzio fino al
      2026-09-18: se si rompe, si rompe di nuovo in silenzio.
  V6  [DECISIVO] LA RIGIOCATA COMBACIA: ripartendo dallo snapshot 50 si riottengono snapshot
      BYTE-IDENTICI a quelli del run originale. E' il sigillo della RIPRODUCIBILITA', ed e' il
      test empirico della riserva dichiarata nel task history par.1.1 ("un solo generatore
      garantisce la casualita', non ogni sorgente di non-determinismo").
  V7  retrocompatibilita': .pkl e .pkl.gz si leggono ENTRAMBI, e danno lo stesso stato.
  V8  IL COSTO, misurato DENTRO un run: quanto rallenta la simulazione, con e senza gzip.
      (csv/_seal_fork/_costo_archivio_2026-09-19.txt ha gia' misurato il costo di UNA scrittura
      fuori dal run: 0.156 s non compresso, 4.42 s a gzip livello 9. Qui si misura l'OVERHEAD.)
  V9  i sigilli del giro rigirano: _sigillo_coorti.py e' quello che esercita salva_stato.

COSA NON MISURA, e va detto invece di lasciarlo credere
  - NON misura che la fisica sia GIUSTA: misura che NON SIA CAMBIATA. Sono due cose diverse.
  - V6 gira su UNA scena e UN seme. Una rigiocata che combacia su un seme non dimostra che
    combaci su tutti, dimostra che il meccanismo non perde stato.
  - V8 misura UNA scena breve: l'overhead relativo su un run lungo puo' differire, perche' il
    costo per snapshot cresce col numero di nodi mentre il costo per passo pure.
ASCII PURO.
"""
import os
import pickle
import shutil
import subprocess
import sys
import tempfile
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, RADICE)
import soliton_simulator as S

SIM = os.path.join(RADICE, "soliton_simulator.py")
BLOB_PRE_ARCHIVIO = "b9e07c73"     # l'ultimo blob PRIMA che l'archivio esistesse (HEAD 2c92b9d)
SEED = 900
PASSI_AB = 60                      # V1/V2: corto, serve la byte-identita', non la maturazione
PASSI_SERIE, OGNI_SERIE = 100, 25  # V3/V4/V6
# I metadati di VERSIONE devono differire fra due codici diversi: non sono fisica.
META = ("code_hash", "content_hash", "blob", "committed_blob", "commit", "branch", "dirty")

esiti = []

# GIRO PARZIALE: `python _sigillo_archivio.py V6` rigira una voce sola invece di tutte.
# ATTENZIONE: UN GIRO PARZIALE NON E' UN SIGILLO, ed e' dichiarato come tale nell'intestazione e nel
# verdetto: serve a far parlare una voce che ha gia' fallito, non a timbrare.
SOLO = set(x.upper() for x in sys.argv[1:] if not x.startswith("-"))


def attivo(v):
    return (not SOLO) or (v in SOLO)


def segna(nome, ok, dettaglio):
    esiti.append((nome, ok, dettaglio))
    print("%-4s %-6s %s" % (nome, "PASS" if ok else "FAIL", dettaglio), flush=True)


def carica(path):
    import gzip
    _apri = gzip.open if str(path).endswith(".gz") else open
    with _apri(path, "rb") as fh:
        return pickle.load(fh)


def dettaglio_diff(k, va, vb, max_elem=3):
    """CHE due strutture differiscono NON BASTA: serve COME.

    Il primo giro di questo sigillo (2026-09-19) ha dato `V6 FAIL su conc_nodi` con il `repr`
    TRONCATO a 60 caratteri: diceva CHE differivano e non COME -- lunghezza, contenuto o ordine.
    **Un sigillo che non dice cosa ha visto costringe a indovinare**, ed e' il modo in cui una
    diagnosi sbagliata entra in un referto. Quindi qui si riporta: le due LUNGHEZZE, QUANTI
    elementi differiscono, e il CONTENUTO INTEGRALE dei primi che differiscono -- NON troncato.
    (Rilievo di Luca: "non e' ancora il momento di indagare, e' il momento di far parlare lo
    strumento".)"""
    righe = []
    la = len(va) if hasattr(va, "__len__") else None
    lb = len(vb) if hasattr(vb, "__len__") else None
    righe.append("%s: len A=%s  len B=%s%s"
                 % (k, la, lb, "   <<< LUNGHEZZE DIVERSE" if la != lb else ""))
    if isinstance(va, dict) and isinstance(vb, dict):
        ka, kb = set(va), set(vb)
        righe.append("   chiavi solo in A: %s" % sorted(ka - kb)[:20])
        righe.append("   chiavi solo in B: %s" % sorted(kb - ka)[:20])
        div = [x for x in sorted(ka & kb, key=repr)
               if pickle.dumps(va[x], 5) != pickle.dumps(vb[x], 5)]
        righe.append("   chiavi comuni %d, con VALORE diverso %d: %s" % (len(ka & kb), len(div), div[:20]))
        for x in div[:max_elem]:
            righe.append("   [%r] A = %r" % (x, va[x]))
            righe.append("   [%r] B = %r" % (x, vb[x]))
    elif la is not None and lb is not None:
        n = min(la, lb)
        div = [i for i in range(n) if pickle.dumps(va[i], 5) != pickle.dumps(vb[i], 5)]
        righe.append("   elementi confrontabili %d, DIVERSI %d  (primi indici: %s)"
                     % (n, len(div), div[:20]))
        for i in div[:max_elem]:
            righe.append("   [%d] A = %r" % (i, va[i]))
            righe.append("   [%d] B = %r" % (i, vb[i]))
        if la != lb:
            piu, chi = (va, "A") if la > lb else (vb, "B")
            righe.append("   la piu' LUNGA e' %s; sua coda oltre %d: %r"
                         % (chi, n, list(piu[n:n + max_elem])))
            righe.append("   coda NON VUOTA?  %s"
                         % any(bool(x) for x in list(piu[n:])))
    else:
        righe.append("   A = %r" % (va,))
        righe.append("   B = %r" % (vb,))
    return righe


def confronta_attrs(a, b, etichetta):
    """Confronto BYTE fra due `attrs`. Ritorna (n_confrontati, guai)."""
    ka, kb = set(a["attrs"]), set(b["attrs"])
    guai = []
    for k in sorted(ka ^ kb):
        guai.append("chiave %s presente solo in %s" % (k, "A" if k in ka else "B"))
    n = 0
    for k in sorted(ka & kb):
        va, vb = a["attrs"][k], b["attrs"][k]
        if isinstance(va, np.ndarray) or isinstance(vb, np.ndarray):
            if not isinstance(va, np.ndarray) or not isinstance(vb, np.ndarray):
                guai.append("%s: tipo diverso (%s vs %s)" % (k, type(va).__name__, type(vb).__name__))
                continue
            if va.shape != vb.shape:
                guai.append("%s: SHAPE diversa %s vs %s" % (k, va.shape, vb.shape))
                continue
            if va.dtype != vb.dtype:
                guai.append("%s: dtype diverso %s vs %s" % (k, va.dtype, vb.dtype))
                continue
            n += 1
            if va.tobytes() != vb.tobytes():
                d = float(np.max(np.abs(va.astype(float) - vb.astype(float)))) if va.size else 0.0
                guai.append("%s: BYTE DIVERSI (max|A-B| = %.3e)" % (k, d))
        else:
            # NON si usa `!=`: `conc_nodi`/`conc_archi`/`masse_info` sono liste e dict che possono
            # contenere ndarray, e li' `!=` SOLLEVA ValueError ("truth value is ambiguous") invece
            # di dare un verdetto -- cioe' il sigillo SI SCHIANTEREBBE anziche' fallire, che e' la
            # modalita' piu' facile da non notare (par.9, FintaRete). Si confrontano i BYTE della
            # serializzazione: e' esatto per strutture prodotte dallo stesso codice deterministico,
            # e un eventuale falso FAIL e' preferibile a un crash.
            n += 1
            try:
                diverso = pickle.dumps(va, 5) != pickle.dumps(vb, 5)
            except Exception as e:
                guai.append("%s: NON CONFRONTABILE (%s)" % (k, type(e).__name__))
                continue
            if diverso:
                guai.append("%s: DIVERSO (dettaglio sotto)" % k)
                for r in dettaglio_diff(k, va, vb):
                    print("       > " + r, flush=True)
    if a.get("rng_state") != b.get("rng_state"):
        guai.append("rng_state DIVERSO")
    else:
        n += 1
    print("     [%s] confrontati %d campi, %d guai" % (etichetta, n, len(guai)))
    return n, guai


def run(exe_sim, tmp, nome, extra, passi=PASSI_AB, ogni_db=None, ext=".pkl"):
    """Un run di batch che lascia il proprio stato finale in <nome><ext>."""
    db = os.path.join(tmp, nome + ext)
    cmd = [sys.executable, exe_sim, "--batch", "--sep", "8", "--seed", str(SEED),
           "--passi", str(passi), "--ogni", "50",
           "--csv", os.path.join(tmp, nome + ".csv"),
           "--sync-db", db, "--db-ogni", str(ogni_db or passi)] + list(extra)
    t0 = time.time()
    pr = subprocess.run(cmd, cwd=RADICE, capture_output=True, text=True,
                        encoding="utf-8", errors="replace", timeout=3600)
    return db, time.time() - t0, pr


def estrai_vecchio(tmp):
    """Il simulatore PRE-ARCHIVIO, estratto IN BINARIO e ancorato al suo sha."""
    pr = subprocess.run(["git", "cat-file", "-p", BLOB_PRE_ARCHIVIO],
                        cwd=RADICE, capture_output=True)
    if pr.returncode != 0:
        return None
    dst = os.path.join(tmp, "sim_pre_archivio.py")
    with open(dst, "wb") as fh:          # BINARIO: nessun filtro newline (trappola CRLF, C18)
        fh.write(pr.stdout)
    return dst


def main():
    tmp = tempfile.mkdtemp(prefix="sigArch_")
    try:
        # ---- V0: si DICHIARA il blob, non si assume ----------------------------------
        import hashlib
        grezzo = hashlib.sha1(open(SIM, "rb").read()).hexdigest()[:8]
        gito = subprocess.run(["git", "hash-object", SIM], cwd=RADICE,
                              capture_output=True, text=True).stdout.strip()[:8]
        segna("V0", True, "simulatore: byte grezzi %s, git-blob %s (pre-archivio %s)"
              % (grezzo, gito, BLOB_PRE_ARCHIVIO))

        # ---- V1 [BLOCCANTE]: flag OFF == codice PRE-ARCHIVIO --------------------------
        vecchio = estrai_vecchio(tmp) if attivo("V1") else None
        if not attivo("V1"):
            pass
        elif vecchio is None:
            segna("V1", False, "NON ESEGUITO: git cat-file %s fallito" % BLOB_PRE_ARCHIVIO)
        else:
            db_old, t_old, pr_old = run(vecchio, tmp, "v1_old", [])
            db_new, t_new, pr_new = run(SIM, tmp, "v1_new", [])
            if not (os.path.exists(db_old) and os.path.exists(db_new)):
                segna("V1", False, "uno dei due run non ha prodotto il DB (old=%s new=%s)"
                      % (os.path.exists(db_old), os.path.exists(db_new)))
                for r in (pr_old.stdout + pr_old.stderr).splitlines()[-6:]:
                    print("     old| " + r)
            else:
                A, B = carica(db_old), carica(db_new)
                n, guai = confronta_attrs(A, B, "V1")
                segna("V1", n > 0 and not guai,
                      "PRE-ARCHIVIO vs flag OFF, %d passi: %d campi confrontati, %s "
                      "(%.0f s vs %.0f s)"
                      % (PASSI_AB, n, "IDENTICI" if not guai else guai[:3], t_old, t_new))
                # i metadati di versione DEVONO differire: se no, non ho confrontato due codici
                diversi = [k for k in META if A.get(k) != B.get(k)]
                segna("V1b", bool(diversi),
                      "i due DB vengono da codici DIVERSI (metadati che differiscono: %s) -- "
                      "senza questo, V1 potrebbe aver confrontato un codice con se stesso"
                      % (diversi or "NESSUNO"))

        # ---- V2 [BLOCCANTE]: flag ON == flag OFF --------------------------------------
        if attivo("V2"):
            db_off = os.path.join(tmp, "v1_new.pkl")
            if not os.path.exists(db_off):
                db_off, _, _ = run(SIM, tmp, "v2_off", [])
            db_on_base = os.path.join(tmp, "v2_on.pkl")
            _, t_on, pr_on = run(SIM, tmp, "v2_on", ["--db-serie"], ogni_db=PASSI_AB)
            ser_on = S._db_serie_esistenti(db_on_base)
            if not ser_on:
                segna("V2", False, "il run con --db-serie non ha prodotto snapshot")
            else:
                A, B = carica(db_off), carica(ser_on[-1][1])
                n, guai = confronta_attrs(A, B, "V2")
                segna("V2", n > 0 and not guai,
                      "flag OFF vs flag ON, %d passi: %d campi confrontati, %s"
                      % (PASSI_AB, n, "IDENTICI" if not guai else guai[:3]))

        # ---- V3/V4: la serie esiste, e il nome dice il vero ---------------------------
        # LA SERIE SERVE ANCHE A V5, V6 e V8: si produce se una qualunque di loro e' attiva.
        ser, t_serie, base = [], None, os.path.join(tmp, "serie.pkl")
        if any(attivo(v) for v in ("V3", "V4", "V5", "V6", "V8")):
            _, t_serie, pr_s = run(SIM, tmp, "serie", ["--db-serie"],
                                   passi=PASSI_SERIE, ogni_db=OGNI_SERIE)
            ser = S._db_serie_esistenti(base)
        attesi = list(range(OGNI_SERIE, PASSI_SERIE + 1, OGNI_SERIE))
        if attivo("V3"):
            segna("V3", [s for s, _ in ser] == attesi,
                  "%d passi @ %d -> %d file ai passi %s (attesi %s)"
                  % (PASSI_SERIE, OGNI_SERIE, len(ser), [s for s, _ in ser], attesi))
        if attivo("V4"):
            guai4 = []
            for passo, p in ser:
                dentro = (carica(p).get("attrs") or {}).get("_db_step")
                if dentro is None or int(dentro) != passo:
                    guai4.append("%s: nel file %r" % (os.path.basename(p), dentro))
            segna("V4", bool(ser) and not guai4,
                  "passo nel NOME == _db_step nei DATI su %d file: %s"
                  % (len(ser), "OK" if not guai4 else guai4))

        # ---- V5: round-trip delle tre strutture di Z53 --------------------------------
        if attivo("V5") and ser:
            st = carica(ser[-1][1])
            presenti = [k for k in ("conc_nodi", "conc_archi", "masse_info") if k in st["attrs"]]
            net = S.Rete(seed=SEED)
            p5 = os.path.join(tmp, "v5.pkl.gz")
            for k in presenti:
                setattr(net, k, st["attrs"][k])
            net._db_step = 12345
            net.salva_stato(p5)
            rt = carica(p5)
            # stessa ragione di `confronta_attrs`: si confrontano i BYTE, non con `==`
            uguali = [k for k in presenti
                      if pickle.dumps(rt["attrs"].get(k), 5) == pickle.dumps(st["attrs"][k], 5)]
            segna("V5", bool(presenti) and len(uguali) == len(presenti),
                  "round-trip GZIP delle strutture di Z53: %d su %d identiche %s"
                  % (len(uguali), len(presenti), presenti or "NESSUNA PRESENTE -> nulla da provare"))
        elif attivo("V5"):
            segna("V5", False, "NON ESEGUITO: nessuna serie da cui prendere lo stato")

        # ---- V6 [DECISIVO]: la rigiocata COMBACIA -------------------------------------
        if attivo("V6") and len(ser) >= 3:
            tmp6 = os.path.join(tmp, "rig")
            os.makedirs(tmp6)
            base6 = os.path.join(tmp6, "serie.pkl")
            meta_da = PASSI_SERIE // 2
            for passo, p in ser:
                if passo <= meta_da:
                    shutil.copy2(p, S._db_serie_path(base6, passo))
            cmd6 = [sys.executable, SIM, "--batch", "--sep", "8", "--seed", str(SEED),
                    "--passi", str(PASSI_SERIE), "--ogni", "50",
                    "--csv", os.path.join(tmp6, "o.csv"), "--sync-db", base6,
                    "--db-ogni", str(OGNI_SERIE), "--db-serie",
                    "--db-rigioca", str(meta_da), str(PASSI_SERIE)]
            t0 = time.time()
            pr6 = subprocess.run(cmd6, cwd=RADICE, capture_output=True, text=True,
                                 encoding="utf-8", errors="replace", timeout=3600)
            dt6 = time.time() - t0
            orig = dict(ser)
            rig = dict(S._db_serie_esistenti(base6))
            rigenerati = sorted(s for s in rig if s > meta_da)
            guai6, n6 = [], 0
            for s in rigenerati:
                n, g = confronta_attrs(carica(orig[s]), carica(rig[s]), "V6@%d" % s)
                n6 += n
                guai6 += ["passo %d: %s" % (s, x) for x in g]
            segna("V6", bool(rigenerati) and n6 > 0 and not guai6,
                  "rigiocata da %d: rigenerati i passi %s in %.0f s, %d campi confrontati, %s"
                  % (meta_da, rigenerati, dt6, n6,
                     "BYTE-IDENTICI" if not guai6 else guai6[:3]))
        elif attivo("V6"):
            segna("V6", False, "NON ESEGUITO: serie troppo corta (%d snapshot)" % len(ser))

        # ---- V7: retrocompatibilita' dei due formati ----------------------------------
        if attivo("V7"):
            net7 = S.Rete(seed=SEED)
            net7._db_step = 777
            pa, pb = os.path.join(tmp, "v7.pkl"), os.path.join(tmp, "v7.pkl.gz")
            net7.salva_stato(pa)
            net7.salva_stato(pb)
            A7, B7 = carica(pa), carica(pb)
            n7, guai7 = confronta_attrs(A7, B7, "V7")
            letti = S.Rete(seed=SEED).carica_stato(pa) and S.Rete(seed=SEED).carica_stato(pb)
            segna("V7", n7 > 0 and not guai7 and letti,
                  ".pkl (%d B) e .pkl.gz (%d B): stesso contenuto su %d campi, entrambi RICARICABILI"
                  % (os.path.getsize(pa), os.path.getsize(pb), n7))

        # ---- V8: il COSTO dentro un run ------------------------------------------------
        if attivo("V8") and t_serie is not None:
            _, t_gz, _ = run(SIM, tmp, "v8gz", ["--db-serie"],
                             passi=PASSI_SERIE, ogni_db=OGNI_SERIE, ext=".pkl.gz")
            n_snap = max(1, PASSI_SERIE // OGNI_SERIE)
            over = (t_gz - t_serie) / n_snap
            segna("V8", True,
                  "run %d passi @%d: %.1f s senza gzip, %.1f s con gzip -> %+.2f s per snapshot "
                  "(%+.1f %% sul run). MISURATO, non stimato."
                  % (PASSI_SERIE, OGNI_SERIE, t_serie, t_gz, over,
                     100.0 * (t_gz - t_serie) / t_serie if t_serie else float("nan")))

        # ---- V9: i sigilli del giro rigirano -------------------------------------------
        if attivo("V9"):
            altro = os.path.join(_QUI, "_sigillo_coorti.py")
            if os.path.exists(altro):
                t0 = time.time()
                pr9 = subprocess.run([sys.executable, altro], cwd=RADICE, capture_output=True,
                                     text=True, encoding="utf-8", errors="replace", timeout=3600)
                dt9 = time.time() - t0
                coda = [r for r in (pr9.stdout or "").splitlines() if r.strip()][-3:]
                segna("V9", pr9.returncode == 0,
                      "_sigillo_coorti.py rc=%s in %.0f s | %s"
                      % (pr9.returncode, dt9, " / ".join(coda)))
            else:
                segna("V9", False, "NON ESEGUITO: _sigillo_coorti.py assente")

        # ---- VERDETTO -------------------------------------------------------------------
        print("")
        ok = sum(1 for _, o, _ in esiti if o)
        print("ESITO: %d/%d%s" % (ok, len(esiti),
                                  "   *** GIRO PARZIALE (%s): NON E' UN SIGILLO ***"
                                  % ",".join(sorted(SOLO)) if SOLO else ""))
        bloccanti = [n for n, o, _ in esiti if not o and n in ("V1", "V2", "V6")]
        print("")
        if SOLO:
            print("ATTENZIONE: GIRO PARZIALE su %s: le voci non girate NON sono state verificate, e"
                  % ",".join(sorted(SOLO)))
            print("  l'assenza di un FAIL non e' un PASS. Per timbrare serve il giro COMPLETO.")
            print("")
        if bloccanti:
            print("VERDETTO: SIGILLO FALLITO sui DECISIVI: %s" % ", ".join(bloccanti))
            print("  V1/V2 che cadono significano CHE HO TOCCATO LA FISICA: si torna indietro.")
            print("  V6 che cade significa che la riproduzione NON funziona, e il par.1 del task")
            print("  history ha gia' escluso la causa piu' ovvia (un secondo generatore): si")
            print("  RIPORTA, senza inventare la spiegazione.")
        elif ok == len(esiti):
            print("VERDETTO: SIGILLO COMPLETO. L'archivio e' byte-inerte sulla fisica (V1, V2) e")
            print("  la rigiocata e' BYTE-IDENTICA (V6).")
            print("  NB: questo NON dice che la fisica sia GIUSTA, dice che NON E' CAMBIATA.")
        else:
            print("VERDETTO: i DECISIVI passano, ma qualche voce no. Le righe FAIL dicono quali.")
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
