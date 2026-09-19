# -*- coding: utf-8 -*-
"""LA SCENA DEL VIDEO CON LA RIPRESA -- copia di `_scena_video.py` piu' `--riprendi`.

*** PERCHE' E' UNA COPIA E NON UNA MODIFICA (decisione di Luca, 2026-09-19) ***
  `_scena_video.py` e' IN USO da un run a 6000 passi che sta girando adesso. Modificarlo non
  fermerebbe quel processo -- Python ha gia' caricato il modulo in memoria -- ma cambierebbe il
  FILE SU DISCO: il run ha gia' timbrato il blob vecchio, e se poi si volesse riprendere si
  userebbe un file DIVERSO da quello che ha prodotto i dati. Separare i due file toglie
  l'ambiguita' invece di doverla spiegare dopo.

*** COSA AGGIUNGE, E COSA NON CAMBIA ***
  `--riprendi`: se la cartella contiene gia' una serie DI QUESTA FISICA, carica il piu' recente e
  continua da li'. SENZA il flag il comportamento e' IDENTICO all'originale: cartella sporca ->
  RIFIUTO. La ripresa e' una scelta ESPLICITA, mai un ripiego automatico.
  Il blob di OGNI snapshot e' gia' verificato da `_db_serie_verifica` PRIMA del carico: riprendere
  da una fisica diversa e' impossibile, non sconsigliato.

*** LA CONSISTENZA NON E' DICHIARATA QUI: E' SIGILLATA ALTROVE ***
  `csv/_seal_fork/_sigillo_ripresa_scena.py` confronta un run CONTINUO con uno INTERROTTO E
  RIPRESO. Se lo stato finale non e' identico, LA RIPRESA NON SI USA: un run che SEMBRA continuo
  e non lo e' e' peggio di un run interrotto, perche' non te ne accorgi.

---
LA SCENA DEL VIDEO, SENZA IL RENDERING -- riproduce `--test N-MASSE` e SALVA lo stato.

⚠ PERCHE' ESISTE, e NON e' una scorciatoia:
  nel ramo headless `--sync-db` **CARICA soltanto** (`:5836-5844`; il commento lo dice:
  *«se --sync-db e il file esiste, CARICA lo stato»*) e **NON CHIAMA MAI `salva_stato`**.
  Quindi il comando del mandato NON produrrebbe nessun `.pkl` e le misure non si potrebbero fare.

NON APPLICO I FLAG A MANO: uso il PERCORSO UFFICIALE del programma, lo stesso di `:7328-7336`
    a = _cli(); _applica_regime(a); _applica_flag(a)
e la scena si avvia col SUO costruttore, `avvia_test("N-MASSE")` -> `_semina_n_masse()`.
Il ciclo per frame e' COPIATO da `update()` (`:5091-5100`), non reinventato:
    passo_test()                                   # una volta per frame: fa avanzare le fasi
    for _ in range(PASSI_PER_FRAME):               # = 6
        scuoti_vuoto(net); net.step(); net.mitosi(); net.rilassa_disegno(); net.memoria_hebbiana_moto()

USO:  python _scena_video.py <n_frame> <destinazione> [frame,di,snapshot]
ASCII PURO.
"""
import os
import sys
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")))
import _presidio
_presidio.avvia(__file__)

import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
os.chdir(ROOT)

_ARGV = list(sys.argv)
# [ARCHIVIO, 2026-09-19] OPZIONI DEL DRIVER, tolte da argv PRIMA che il parser del simulatore lo
# veda. Sono NOMINALI e non posizionali di proposito: aggiungere un 6o argomento posizionale
# avrebbe costretto a passare anche i precedenti, e il comando di `Z49` deve restare riproducibile
# VERBATIM.
#   --serie=K            salva uno snapshot ogni K frame, come SERIE numerata col PASSO DI MOTORE
#   --csv-progresso=P    scrive il progresso in un CSV, con blob/seme/flag (P6)
# ⚠ SENZA QUESTE DUE, IL DRIVER FA ESATTAMENTE QUELLO CHE FACEVA. Lo prova il rigiro del sigillo.
# ⚠ E `--db-serie`/`--db-ogni` del simulatore NON servono qui: quella logica vive in
#   `batch_condensazione`, dove questo percorso non passa. Verificato dal sorgente, non dedotto.
SERIE = None
CSVPROG = None
RIPRENDI = False
_resti = []
for _x in _ARGV[1:]:
    if _x.startswith("--serie="):
        SERIE = int(_x.split("=", 1)[1])
    elif _x.startswith("--csv-progresso="):
        CSVPROG = _x.split("=", 1)[1]
    elif _x == "--riprendi":
        # LA RIPRESA E' UNA SCELTA ESPLICITA, MAI UN RIPIEGO AUTOMATICO: senza questo flag il
        # comportamento resta quello dell'originale (cartella sporca -> RIFIUTO).
        RIPRENDI = True
    else:
        _resti.append(_x)
_ARGV = [_ARGV[0]] + _resti
NFRAME = int(_ARGV[1]) if len(_ARGV) > 1 else 20
DEST = _ARGV[2] if len(_ARGV) > 2 else os.path.join("csv", "_test_fork", "_gvideo")
SNAP = set(int(x) for x in _ARGV[3].split(",")) if len(_ARGV) > 3 else set()
# [SIGILLO 2026-09-18] `fedele` chiama ANCHE le quattro funzioni che `update()` usa per
# DISEGNARE, nello STESSO ordine (:5104, :5136, :5218, :5267). Serve a PROVARE che il
# rendering non tocca la fisica, invece di dedurlo. Default: solo fisica.
MODO = _ARGV[4] if len(_ARGV) > 4 else "fisica"
os.makedirs(DEST, exist_ok=True)

# gli STESSI flag del comando del mandato. `--test` fa scegliere Agg a `:132`: nessuna finestra.
# [A/B a variabile singola, 2026-09-18] `--nmasse` e' l'UNICA cosa che cambia fra il run a tre
# masse (`Z49`) e quello di controllo a due. Si passa da riga di comando come 5o argomento; il
# default resta 3, cosi' il comando di `Z49` resta riproducibile VERBATIM.
NMASSE = _ARGV[5] if len(_ARGV) > 5 else "3"
sys.argv = ["soliton_simulator.py", "--test", "N-MASSE", "--nmasse", NMASSE, "--sep", "8",
            "--giri", "0", "--campo-spinoriale", "--spinore-vivo", "--spinore-corretto",
            "--chi-core", "--calore-scal", "--deparam-orologio", "--verlet", "--fork-su2",
            "--fork-su2-mem", "--cs-dinamico", "--tau-luce", "--rumore-colorato",
            "--pav-com", "--guscio-morbido", "--zeta-vir", "--chi-basc", "--plast-din",
            "--viriale", "--olon-part"]
import soliton_simulator as S

print("=" * 112)
print("SCENA DEL VIDEO senza rendering -- %d frame x %d passi = %d passi di motore"
      % (NFRAME, S.PASSI_PER_FRAME, NFRAME * S.PASSI_PER_FRAME))
print("=" * 112)

a = S._cli()                 # IL PERCORSO UFFICIALE: stesso parser del programma
S._applica_regime(a)
S._applica_flag(a)
S._NMASSE_VIDEO["n"] = max(2, int(getattr(a, "nmasse", 2)))
S._NMASSE_VIDEO["sep"] = float(getattr(a, "sep", 3.0))
S._NMASSE_VIDEO["size"] = None

print("\n  FLAG ATTIVI, letti dal MODULO dopo `_applica_flag` (P6: dai dati, non dal comando):")
for f in ("CAMPO_SPINORIALE", "SPINORE_VIVO", "SPINORE_CORRETTO", "CHI_CORE", "CS_DINAMICO",
          "TAU_LUCE", "CHI_BASC", "FORK_SU2", "FORK_SU2_MEM", "STEP2_OROLOGIO", "SPIN_FEEDBACK",
          "CALORE_VETTORIALE", "PLAST_DIN", "VERLET", "TAU_LOC"):
    print("    %-20s %s" % (f, getattr(S, f, "ASSENTE")))
print("  PASSI_PER_FRAME = %s   DT = %s   TAU_A = %s   N_c(collasso) = %d"
      % (S.PASSI_PER_FRAME, S.DT, S.TAU_A, int(S.massa_critica_collasso())))
print("  ⚠ `--tau-luce` ha il SIGILLO FALLITO (CLAUDE.md par.0): ramo NON CERTIFICATO.")
print("  ⚠ `--chi-basc` RISCRIVE `perc_chi` a ogni passo: non e' un'etichetta di lignaggio.")

S.avvia_test("N-MASSE")()    # il costruttore UFFICIALE della scena -> _semina_n_masse()
print("\n  scena avviata: n = %d nodi alla semina (N_c*0.8 per massa, %s masse)"
      % (S.net.n, NMASSE))   # il NUMERO DI MASSE si STAMPA, non si assume: era cablato a "3"

# [ARCHIVIO] IL SEME SI LEGGE, NON SI ASSUME. `net = Rete()` (:4531) usa il DEFAULT della classe;
# `SEME_INIZIALE = 900` e' il NUMERO DI NODI seminati (:4532), non il seme -- e nel batch lo stesso
# 900 viene riusato COME seme (:6407). Scrivere "seed 900" qui sarebbe FALSO.
import inspect as _insp
SEME_EFFETTIVO = _insp.signature(S.Rete.__init__).parameters["seed"].default
BLOB_RUN = (S.net._versione_codice() or {}).get("blob")
BASE_SERIE = os.path.join(DEST, "scena.pkl.gz")     # `.gz` -> compressione a livello 1
_n_scritti = _n_saltati = _n_falliti = 0
_peso_tot = 0
print("\n  SEME EFFETTIVO (letto da Rete.__init__): %s    BLOB: %s" % (SEME_EFFETTIVO, BLOB_RUN))
FRAME0 = 0          # da quale frame si parte: 0 = da zero, >0 = RIPRESA
if SERIE:
    print("  SERIE ATTIVA: uno snapshot ogni %d frame = %d passi di motore -> %s"
          % (SERIE, SERIE * int(S.PASSI_PER_FRAME), BASE_SERIE))
    _pre, _guaio = S._db_serie_verifica(BASE_SERIE, S.net._versione_codice())
    if _guaio:
        raise SystemExit("[serie] RIFIUTO DI PARTIRE: %s" % _guaio)
    if _pre and not RIPRENDI:
        raise SystemExit("[serie] RIFIUTO: la cartella contiene gia' %d snapshot di QUESTA fisica, "
                         "e --riprendi NON e' stato chiesto. O usi una cartella pulita, o dichiari "
                         "di voler RIPRENDERE." % len(_pre))
    if _pre and RIPRENDI:
        # LA RIPRESA. `_db_serie_verifica` ha GIA' controllato il BLOB di OGNI snapshot: se il
        # codice fosse cambiato saremmo usciti sopra. Qui si carica il piu' RECENTE.
        _passo0, _path0 = _pre[-1]
        S.net.carica_stato(_path0)
        _dentro = int(getattr(S.net, "_db_step", -1))
        if _dentro != _passo0:
            raise SystemExit("[serie] RIFIUTO: il passo NEL FILE (%d) non e' quello NEL NOME (%d). "
                             "Non riprendo da uno snapshot che non sa dire dove si trova."
                             % (_dentro, _passo0))
        if _passo0 % int(S.PASSI_PER_FRAME):
            raise SystemExit("[serie] RIFIUTO: il passo %d non e' un multiplo di PASSI_PER_FRAME=%d, "
                             "quindi cadrebbe DENTRO un frame e la ripresa non sarebbe allineata."
                             % (_passo0, int(S.PASSI_PER_FRAME)))
        FRAME0 = _passo0 // int(S.PASSI_PER_FRAME)
        if FRAME0 >= NFRAME:
            raise SystemExit("[serie] NIENTE DA FARE: l'archivio arriva gia' al frame %d di %d."
                             % (FRAME0, NFRAME))
        print("  RIPRESA: caricato %s (passo %d = frame %d). Si riparte dal frame %d, "
              "n=%d, archi=%d." % (os.path.basename(_path0), _passo0, FRAME0, FRAME0 + 1,
                                   S.net.n, len(S.net.i)))
        print("  ATTENZIONE: il COPIONE della scena riparte dalla fase 0. NON tocca la fisica -- la")
        print("  sua unica azione, _semina_n_masse, e' gia' avvenuta all'avvio ed e' stata")
        print("  SOVRASCRITTA dal carica_stato. Lo dimostra il sigillo della ripresa, non questo commento.")
    elif RIPRENDI:
        print("  --riprendi chiesto ma la cartella e' VUOTA: si parte da zero (non e' un errore).")

csv_f = None
if CSVPROG:
    os.makedirs(os.path.dirname(os.path.abspath(CSVPROG)) or ".", exist_ok=True)
    csv_f = open(CSVPROG, "w", encoding="utf-8")
    # P6: BLOB, SEME e TUTTI i flag che distinguono questo run. Nel CSV, non solo nel log.
    _flag = ("CAMPO_SPINORIALE", "SPINORE_VIVO", "SPINORE_CORRETTO", "CHI_CORE", "CS_DINAMICO",
             "TAU_LUCE", "CHI_BASC", "FORK_SU2", "FORK_SU2_MEM", "STEP2_OROLOGIO", "SPIN_FEEDBACK",
             "PLAST_DIN", "VERLET", "RUMORE_COLORATO", "PAV_COM", "GUSCIO_MORBIDO", "ZETA_VIR",
             "VIRIALE", "OLON_PART", "CALORE_VETTORIALE")
    csv_f.write("# blob=%s seme_effettivo=%s nmasse=%s sep=%s PASSI_PER_FRAME=%s DT=%s TAU_A=%s\n"
                % (BLOB_RUN, SEME_EFFETTIVO, NMASSE, S._sep_video(), S.PASSI_PER_FRAME, S.DT, S.TAU_A))
    csv_f.write("# " + " ".join("%s=%s" % (f, int(bool(getattr(S, f, False)))) for f in _flag) + "\n")
    csv_f.write("frame,passo,n,archi,coer_l,dil,elapsed_s,s_per_frame\n")
    csv_f.flush()

t0 = time.time()
S.stato["nframe"] = 0
prog = []
for k in range(FRAME0, NFRAME):
    S.passo_test()
    for _ in range(int(S.PASSI_PER_FRAME)):
        S.scuoti_vuoto(S.net); S.net.step(); S.net.mitosi()
        S.net.rilassa_disegno(); S.net.memoria_hebbiana_moto()
    S.stato["nframe"] += 1
    fr = k + 1
    if MODO == "fedele":
        # l'ORDINE e' quello di `update()`: diagnostica -> campo_spaziale -> pozzo_grafo -> intensita
        S.net.diagnostica()
        try:
            S.net.campo_spaziale()
        except Exception:
            pass
        try:
            _Iv = S.net.intensita()[:S.net.n]
            S.net.pozzo_grafo(_Iv)
        except Exception:
            pass
    if SERIE and (fr % SERIE == 0 or fr == NFRAME):
        # ⚠ QUI `_db_step` E' IL PASSO DI MOTORE, non il frame: la serie numera per PASSO, e `V4`
        # del sigillo dell'archivio verifica "il passo nel NOME == `_db_step` nei DATI".
        _pm = fr * int(S.PASSI_PER_FRAME)
        S.net._db_step = _pm
        _p = S._db_serie_path(BASE_SERIE, _pm)
        if os.path.exists(_p):
            _n_saltati += 1
        else:
            try:
                _ts = time.time()
                S.net.salva_stato(_p)
                _dts = time.time() - _ts
                _n_scritti += 1
                _mb = os.path.getsize(_p) / 1e6
                _peso_tot += os.path.getsize(_p)
                print("  SNAPSHOT passo %-7d n=%-8d %7.2f MB in %5.1f s -> %s"
                      % (_pm, S.net.n, _mb, _dts, os.path.basename(_p)), flush=True)
            except Exception as _e:
                # A8: UN SALVATAGGIO CHE FALLISCE IN SILENZIO E' IL DIFETTO PEGGIORE QUI,
                # e col disco al 96 % non e' un'ipotesi teorica.
                _n_falliti += 1
                print("  *** SALVATAGGIO FALLITO al passo %d: %s ***" % (_pm, _e), flush=True)
    if fr in SNAP or (fr == NFRAME and not SERIE):
        S.net._db_step = fr          # ⚠ e' il FRAME, non il passo di motore. DICHIARATO.
        p = os.path.join(DEST, "frame_%d.pkl" % fr)
        S.net.salva_stato(p)
        print("  SNAPSHOT frame %-5d (passi %-6d) n=%-7d -> %s"
              % (fr, fr * S.PASSI_PER_FRAME, S.net.n, p), flush=True)
    if fr % 5 == 0 or fr == 1:
        dg = S.net.diagnostica()
        el = time.time() - t0
        prog.append((fr, S.net.n, el))
        print("  frame %-5d n=%-7d archi=%-8d coer_l=%-8.4g dil=%+7.3f%%   [%.1f s, %.3f s/frame]"
              % (fr, S.net.n, len(S.net.i), dg.get("coer_l", float("nan")),
                 100 * dg.get("dil", float("nan")), el, el / max(fr - FRAME0, 1)), flush=True)
        if csv_f is not None:
            csv_f.write("%d,%d,%d,%d,%.6g,%.6g,%.1f,%.3f\n"
                        % (fr, fr * int(S.PASSI_PER_FRAME), S.net.n, len(S.net.i),
                           dg.get("coer_l", float("nan")), dg.get("dil", float("nan")),
                           el, el / max(fr - FRAME0, 1)))
            csv_f.flush()

el = time.time() - t0
print("\n  TOTALE %.1f s per %d frame (dal %d al %d) -> %.3f s/frame medio"
      % (el, NFRAME - FRAME0, FRAME0 + 1, NFRAME, el / max(NFRAME - FRAME0, 1)))
if len(prog) >= 2:
    (f1, n1, t1), (f2, n2, t2) = prog[0], prog[-1]
    c1 = t1 / f1; c2 = (t2 - t1) / max(f2 - f1, 1)
    print("  n da %d a %d;  costo per frame da %.3f a %.3f s  (x%.2f)" % (n1, n2, c1, c2, c2 / max(c1, 1e-9)))
    print("  ⚠ IL COSTO CRESCE COL NUMERO DI NODI: un'estrapolazione LINEARE SOTTOSTIMA.")
if csv_f is not None:
    csv_f.close()
    print("  progresso CSV -> %s" % CSVPROG)
if SERIE:
    # A8: il conteggio SI DICHIARA. Un contatore che non si stampa non e' un contatore.
    print("  ARCHIVIO: %d snapshot scritti, %d saltati, %d FALLITI   (%.2f GB in totale)"
          % (_n_scritti, _n_saltati, _n_falliti, _peso_tot / 1e9))
    if _n_falliti:
        print("  *** ATTENZIONE: %d SALVATAGGI SONO FALLITI. L'ARCHIVIO E' INCOMPLETO: i passi "
              "mancanti NON sono recuperabili senza rigirare. ***" % _n_falliti)
print("=" * 112)
