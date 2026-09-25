# -*- coding: utf-8 -*-
"""LA SCENA DEL VIDEO, SENZA IL RENDERING -- riproduce `--test N-MASSE` e SALVA lo stato.

*** LA RIPRESA E' STATA PORTATA QUI IL 2026-09-19, MENTRE IL RUN A 6000 PASSI GIRAVA ***
  Era stata sviluppata su una COPIA (`_scena_video_ripresa.py`) per non toccare il file in uso, e
  li' e' stata SIGILLATA 5/5 (`csv/_seal_fork/_sigillo_ripresa_scena.txt`: un run interrotto e
  ripreso da' lo STESSO stato di uno continuo, 113 campi confrontati, 0 diversi).
  **Poi e' stata portata QUI, e la copia e' stata rimossa**, per una ragione precisa: se il run
  fosse caduto, riprenderlo con un FILE DIVERSO da quello che ha prodotto gli snapshot avrebbe
  reso il run non certificabile come una cosa sola. Un run, un driver.

  ⚠ IL BLOB DI QUESTO FILE E' CAMBIATO A META' DEL RUN: da `f14ea4bd` a quello attuale. Il
  processo in corso NON se ne e' accorto (Python aveva gia' caricato il modulo in memoria), e il
  ramo nuovo e' INERTE senza `--riprendi`. Ma e' un fatto, e sta scritto in `doc/STATO_RUN.md`.

*** COSA AGGIUNGE, E COSA NON CAMBIA ***
  `--riprendi`: se la cartella contiene gia' una serie DI QUESTA FISICA, carica il piu' recente e
  continua da li'. SENZA il flag il comportamento e' IDENTICO a prima: cartella sporca -> RIFIUTO.
  La ripresa e' una scelta ESPLICITA, mai un ripiego automatico.
  Il blob di OGNI snapshot e' verificato da `_db_serie_verifica` PRIMA del carico: riprendere da
  una fisica diversa e' IMPOSSIBILE, non sconsigliato.

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
# [REFERTO DI CONFIGURAZIONE, 2026-09-24] LA COPIA VERBATIM, presa PRIMA di qualunque
# filtro: `_ARGV` viene RISCRITTO piu' sotto (le opzioni del driver vengono tolte prima
# che il parser del simulatore le veda), quindi da quel punto in poi NON e' piu' verbatim.
# Il referto deve riportare il comando COME E' STATO DATO, non come e' stato ripulito.
_ARGV_VERBATIM = list(sys.argv)
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
# [2026-09-20] --sep=X NOMINALE, DEFAULT 8. Stessa ragione delle altre due opzioni qui sopra: se
# fosse posizionale, passarlo costringerebbe a passare anche i precedenti e il comando di `Z49`
# non resterebbe riproducibile VERBATIM. A default il driver fa ESATTAMENTE quello che faceva:
# lo prova `csv/_seal_fork/_sigillo_sep_driver.py`, non questo commento.
SEP = "4.0"             # [DECISIONE DI LUCA, 2026-09-24] IL DEFAULT SEGUE LA CAMPAGNA.
                        # Era `"8"`, e OGNI comando di campagna passava `--sep=4.0`: il
                        # default non riproduceva piu' il comportamento attuale -- **la
                        # stessa scadenza di `CHICOOP`**. Con questo `NUDA = CAMPAGNA` non
                        # ha piu' NESSUNA differenza, e il sigillo del driver puo' passare.
                        # ⚠ CAMBIA LA SCENA DI DEFAULT: chi lancia nudo ottiene ora le
                        #   masse a `4.0` invece che a `8`. **Non e' byte-inerte, ed e' il
                        #   punto.** I run gia' fatti passavano `--sep=4.0` esplicitamente
                        #   e il loro `CONFIGURAZIONE.txt` lo documenta.
# [A/B chi_basc, 2026-09-20] --chi-basc=on|off NOMINALE, DEFAULT `on`.
# ⚠ IL DEFAULT E' `on` E NON `off`, ED E' UNA SCELTA: il driver ha SEMPRE passato `--chi-basc`
#   (era cablato poche righe sotto), quindi `on` e' l'unico default che riproduce il comportamento
#   attuale VERBATIM -- e senza quello la byte-identita' del sigillo non avrebbe niente da
#   dimostrare. Il default seguira' la decisione su `chi_basc`, NON la anticipa: la decisione e'
#   proprio cio' che il run A/B di oggi serve a prendere (`Z73`).
# ⚠ E NON E' UNA MODIFICA AL SIMULATORE: `CHI_BASC = False` e' gia' il default di MODULO (`:746`).
#   Era il DRIVER ad accenderlo. Qui si rende esplicito un interruttore che c'era gia'.
CHIBASC = "on"
# [RAMO C a cooperazione, 2026-09-21] --chi-coop=on|off NOMINALE.
# ⚠ IL DEFAULT ERA `off`, ED E' PASSATO A `on` IL 2026-09-24. La ragione del `off` era
#   valida QUANDO il flag nasceva: *il default e' quello che riproduce il comportamento
#   ATTUALE VERBATIM*, e il driver non aveva mai passato `--chi-coop`.
#   ⚠⚠ MA DA `G3` IN POI OGNI COMANDO DI CAMPAGNA HA PASSATO `--chi-coop=on`, e il default
#   e' rimasto `off`: **il comportamento attuale non era piu' quello che il default
#   riproduceva.** La ragione era scaduta e il default no.
CHICOOP = "on"          # [2026-09-24] ACCESA DAL DRIVER. E' una delle TRE leggi che
                        # DEFINISCONO L'EPOCA 2 (`CLAUDE.md` par.9-bis) ed era passata
                        # `=on` da OGNI comando di campagna mentre il default diceva
                        # `"off"`: **il sigillo non la vedeva perche' non e' in
                        # `_cure_verificate.py` -- ORFANO FUORI DALLA LISTA.**
# [RAMO D, 2026-09-21] --scala-min=on|off e --coes-adim=on|off, DEFAULT `off` entrambi, per la
# stessa ragione di `--chi-coop`: il default e' quello che lascia l'argv IDENTICO elemento per
# elemento a quello di prima. Lo prova il sigillo, non questo commento.
SCALAMIN = "off"
# ⚠⚠ [DECISIONE DI LUCA, 2026-09-24] **IL DRIVER ACCENDE TUTTE LE CURE APPROVATE IN MODO
#   INCONDIZIONATO. UN SOLO MODO DI LANCIARE: NUDA = CAMPAGNA.**
#   PERCHE': il sigillo `csv/_seal_fork/_sigillo_driver_accende.py` ha MISURATO che con
#   l'invocazione NUDA **SEI cure su dieci erano SPENTE** -- `PEQ_ESATTO`,
#   `PEQ_NASCITA_LOCALE`, `SCALA_MIN_PASSO`, `COES_CAUSALE`, `COES_ADIM`, `ANOM_SIMM`.
#   Erano accese **solo** perche' OGNI comando di campagna passava `=on`: non erano nel
#   codice, erano **nell'argv di chi lancia**, e un comando che ne dimenticava una girava su
#   un sistema che si sa difettoso (`P2`) **senza che nessun sigillo se ne accorgesse**.
#   COME, e conserva cio' che il par.10 impone: **si cambia il DEFAULT DELL'OPZIONE DEL
#   DRIVER**, non si toglie l'opzione. `=off` continua a funzionare ed e' il ramo
#   **DIAGNOSTICO** per gli A/B -- *«resta un `--senza-<nome>` marcato DIAGNOSTICO, non
#   fisica alternativa»*.
#   ⚠ E NON E' L'EPOCA 3: i `default` NEL SORGENTE del simulatore restano `False`. Qui
#   cambia il default **del driver**, che e' cio' che decide che cosa GIRA.
#   ⚠ `SCALAMIN` RESTA `off`: **non e' una cura approvata** (e' il freno vecchio, quello che
#   `D31` accusa). Non entra in questa decisione.
COESADIM = "on"
# [LE CINQUE CURE, 2026-09-21] stesso schema NOMINALE `=on|off`. **DEFAULT `on` dal
# 2026-09-24**: sono cure APPROVATE, e il driver le accende da se'.
# ⚠⚠ `--invarianti=on|off` SI PARSA QUI, E LA PRIMA VERSIONE NON LO FACEVA -- ERRORE MIO.
#   Il ragionamento era: *e' un'opzione VALORIZZATA del simulatore, quindi cade in `_resti` e ci
#   arriva tale e quale*. **FALSO:** `_resti` diventa il NUOVO `_ARGV`, e il driver legge
#   `_ARGV[3]` come **la lista degli snapshot**. Il lancio della validazione e' morto con
#     ValueError: invalid literal for int() with base 10: '--invarianti=on'
#   **Un'opzione che «passa dritta» passa dritta anche nei POSIZIONALI.**
#   Si parsa e si inoltra **VERBATIM**, senza tradurla in booleano: cosi' non esiste nessuna
#   traduzione che possa divergere -- che era la ragione vera della scelta iniziale.
INVARIANTI_OPT = "on"   # [2026-09-24] ESPLICITO, non piu' `None`. Il default del sorgente
                        # e' gia' `True`, quindi NON cambia cio' che gira -- cambia che
                        # **l'argv lo DICE**, e `NUDA` e `CAMPAGNA` coincidono anche qui.
PEQESATTO = "on"
PEQNASCITA = "on"
SCALAMINPASSO = "on"
COESCAUSALE = "on"
ANOMSIMM = "on"

_resti = []
for _x in _ARGV[1:]:
    if _x.startswith("--serie="):
        SERIE = int(_x.split("=", 1)[1])
    elif _x.startswith("--csv-progresso="):
        CSVPROG = _x.split("=", 1)[1]
    elif _x.startswith("--sep="):
        SEP = _x.split("=", 1)[1]
    elif _x.startswith("--chi-basc="):
        # NOMINALE con `=`, quindi NON collide col `--chi-basc` nudo del simulatore: quello, se
        # qualcuno lo passasse a mano, finirebbe in `_resti` e resterebbe un flag del simulatore.
        CHIBASC = _x.split("=", 1)[1].strip().lower()
        if CHIBASC not in ("on", "off"):
            raise SystemExit("--chi-basc vuole `on` o `off`, non %r" % CHIBASC)
    elif _x.startswith("--chi-coop="):
        # NOMINALE con `=`, come `--chi-basc=`: non collide col `--chi-coop` nudo del
        # simulatore, che finirebbe in `_resti` e resterebbe un flag del simulatore.
        CHICOOP = _x.split("=", 1)[1].strip().lower()
        if CHICOOP not in ("on", "off"):
            raise SystemExit("--chi-coop vuole `on` o `off`, non %r" % CHICOOP)
    elif _x.startswith("--scala-min="):
        SCALAMIN = _x.split("=", 1)[1].strip().lower()
        if SCALAMIN not in ("on", "off"):
            raise SystemExit("--scala-min vuole `on` o `off`, non %r" % SCALAMIN)
    elif _x.startswith("--coes-adim="):
        COESADIM = _x.split("=", 1)[1].strip().lower()
        if COESADIM not in ("on", "off"):
            raise SystemExit("--coes-adim vuole `on` o `off`, non %r" % COESADIM)
    elif _x.startswith("--peq-esatto="):
        PEQESATTO = _x.split("=", 1)[1].strip().lower()
        if PEQESATTO not in ("on", "off"):
            raise SystemExit("--peq-esatto vuole `on` o `off`, non %r" % PEQESATTO)
    elif _x.startswith("--peq-nascita-locale="):
        PEQNASCITA = _x.split("=", 1)[1].strip().lower()
        if PEQNASCITA not in ("on", "off"):
            raise SystemExit("--peq-nascita-locale vuole `on` o `off`, non %r" % PEQNASCITA)
    elif _x.startswith("--scala-min-passo="):
        SCALAMINPASSO = _x.split("=", 1)[1].strip().lower()
        if SCALAMINPASSO not in ("on", "off"):
            raise SystemExit("--scala-min-passo vuole `on` o `off`, non %r" % SCALAMINPASSO)
    elif _x.startswith("--coes-causale="):
        COESCAUSALE = _x.split("=", 1)[1].strip().lower()
        if COESCAUSALE not in ("on", "off"):
            raise SystemExit("--coes-causale vuole `on` o `off`, non %r" % COESCAUSALE)
    elif _x.startswith("--anom-simm="):
        ANOMSIMM = _x.split("=", 1)[1].strip().lower()
        if ANOMSIMM not in ("on", "off"):
            raise SystemExit("--anom-simm vuole `on` o `off`, non %r" % ANOMSIMM)
    elif _x.startswith("--invarianti="):
        _v = _x.split("=", 1)[1].strip().lower()
        if _v not in ("on", "off"):
            raise SystemExit("--invarianti vuole `on` o `off`, non %r" % _v)
        INVARIANTI_OPT = _v      # si INOLTRA verbatim, non si traduce in booleano
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
sys.argv = ["soliton_simulator.py", "--test", "N-MASSE", "--nmasse", NMASSE, "--sep", SEP,
            "--giri", "0", "--campo-spinoriale", "--spinore-vivo", "--spinore-corretto",
            "--chi-core", "--calore-scal", "--deparam-orologio", "--verlet", "--fork-su2",
            "--fork-su2-mem", "--cs-dinamico", "--tau-luce", "--rumore-colorato",
            "--pav-com", "--guscio-morbido", "--zeta-vir",
            # [CURA 1a, 2026-09-24] LA CURA DI `D34`, APPROVATA DA LUCA: il driver la
            # ACCENDE IN OGNI RUN. Da qui in avanti ogni run del fork gira col wrap del
            # ritmo sul periodo GIUSTO. **NON e' byte-inerte, ed e' il punto**: e' una
            # cura, non un'opzione, e i numeri di prima non si confrontano con questi
            # senza dirlo (par.9-bis). Lo stato effettivo sta in CONFIGURAZIONE.txt.
            "--ritmo-wrap-2pi",
            # [CURA 2, 2026-09-24] IL TEMPO UNICO NELLA MITOSI, APPROVATA DA LUCA: il driver
            # la ACCENDE IN OGNI RUN. Gli usi di `tau_pp` come TEMPO passano all'orologio
            # `dt_e` che il sistema gia' definisce; i quattro usi come POSIZIONE sull'asse
            # della torsione restano INTOCCATI (verificato dall'AST: `T3` del sigillo).
            # Sigillo 5/5 con UN PROCESSO PER BRACCIO (`Z145`); giro corto di 120 passi
            # contro `_cura1_corto`: la mitosi vive (eventi 67 -> 76), il bilancio chiude
            # (5.304e-14), e la saturazione di `tanh(grad)` passa da 0.0034 % a ZERO.
            # **NON e' byte-inerte, ed e' il punto**: e' una cura, non un'opzione.
            # IL DEFAULT NEL SORGENTE RESTA `False`: i default si cambiano all'EPOCA 3
            # (decisione di Luca, 2026-09-24). Lo stato effettivo sta in CONFIGURAZIONE.txt.
            "--tempo-unico-mitosi",
            # [CURA 4, 2026-09-25] L'ACCENSIONE DEL CAMPO, APPROVATA DA LUCA: il driver la
            # ACCENDE IN OGNI RUN. Senza, l'universo parte SENZA CAMPO (somma dei pesi
            # `0.000000e+00` al passo zero) e ci mette `TAU_A/DT = 5000` passi ad accendersi:
            # al passo 120 il peso d'arco vale `5.76e-04` del maturo. E SEPARA I DUE RUOLI DI
            # `TAU_A`, che restava insieme vita media della memoria spinoriale E tempo di
            # accensione di una sorgente. Sigillo 7/7, un processo per braccio.
            "--semina-matura",
            # [CURA 5, 2026-09-25] `A13` ALLA NASCITA, APPROVATA DA LUCA: un arco si divide
            # SOLO se `d >= 2 LAM`. `_sm_lund_mitosi` passa da `3.5`-`4.0` a `0.0` ESATTO: la
            # mitosi non fabbrica piu' lunghezza. E TOGLIE una legge invece di aggiungerla
            # (`STANDARD 10`): `_nasce` non ha piu' niente da fare su quel sito. Lo SCHWINGER
            # non e' toccato (resta `A3`). Sigillo 8/8.
            "--mitosi-2lam"] \
    + (["--chi-basc"] if CHIBASC == "on" else []) \
    + (["--chi-coop"] if CHICOOP == "on" else []) \
    + (["--scala-min"] if SCALAMIN == "on" else []) \
    + (["--coes-adim"] if COESADIM == "on" else []) \
    + (["--peq-esatto"] if PEQESATTO == "on" else []) \
    + (["--peq-nascita-locale"] if PEQNASCITA == "on" else []) \
    + (["--scala-min-passo"] if SCALAMINPASSO == "on" else []) \
    + (["--coes-causale"] if COESCAUSALE == "on" else []) \
    + (["--anom-simm"] if ANOMSIMM == "on" else []) \
    + ([] if INVARIANTI_OPT is None else ["--invarianti=%s" % INVARIANTI_OPT]) \
    + ["--plast-din", "--viriale", "--olon-part"]
# ⚠⚠ QUESTE DUE RIGHE MANCAVANO, e il ramo D e' girato per 1200 passi con SCALA_MIN e COES_ADIM
#   SPENTI mentre il comando li chiedeva ACCESI. Le opzioni erano PARSATE (`--scala-min=on` non
#   finiva in `_resti` e non dava errore) ma non arrivavano MAI al simulatore: un'opzione che si
#   accetta e si ignora e' peggio di un'opzione che non esiste, perche' non si lamenta.
#   CAUSA: la patch che doveva aggiungerle usava `str.replace()` con un solo `assert t != o`
#   GLOBALE, soddisfatto dalle ALTRE sostituzioni. L'ancora di QUESTA non ha attaccato, in
#   silenzio. Ogni sostituzione va asserita PER SE', non in blocco.
#   PRESIDIO: `csv/_seal_fork/_sigillo_flag_driver.py` verifica che OGNI opzione `=on` del driver
#   arrivi davvero al MODULO -- e' l'unico test che attraversa il percorso del driver.
# ⚠ IL FLAG SI INSERISCE NELLA STESSA POSIZIONE IN CUI ERA CABLATO. A default la lista e' IDENTICA
#   ELEMENTO PER ELEMENTO a quella di prima: non "equivalente", identica. Lo prova
#   `csv/_seal_fork/_sigillo_chibasc_driver.py`, non questo commento.
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
          "TAU_LUCE", "CHI_BASC", "CHI_COOP", "SCALA_MIN", "COES_ADIM",
          "PEQ_ESATTO", "PEQ_NASCITA_LOCALE", "SCALA_MIN_PASSO", "COES_CAUSALE", "ANOM_SIMM",
          "INVARIANTI", "FORK_SU2", "FORK_SU2_MEM", "STEP2_OROLOGIO",
          "SPIN_FEEDBACK", "CALORE_VETTORIALE", "PLAST_DIN", "VERLET", "TAU_LOC"):
    print("    %-20s %s" % (f, getattr(S, f, "ASSENTE")))
print("  PASSI_PER_FRAME = %s   DT = %s   TAU_A = %s   N_c(collasso) = %d"
      % (S.PASSI_PER_FRAME, S.DT, S.TAU_A, int(S.massa_critica_collasso())))
print("  ⚠ `--tau-luce` ha il SIGILLO FALLITO (CLAUDE.md par.0): ramo NON CERTIFICATO.")
if CHIBASC == "on":
    print("  ⚠ `--chi-basc` RISCRIVE `perc_chi` a ogni passo: non e' un'etichetta di lignaggio.")
else:
    print("  ⚠ `--chi-basc` e' SPENTO (--chi-basc=off): `perc_chi` e' scritta SOLO dalle nascite,")
    print("    `:4294` (eredita UGUALE) e `:4415` (antinodo OPPOSTO). E' il braccio B dell'A/B.")

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

# ---------------------------------------------------------------------------------------
# [REFERTO DI CONFIGURAZIONE, decisione di Luca 2026-09-24] NESSUN RUN PARTE SENZA.
#   Si scrive QUI e non prima: deve stare DOPO `_applica_flag` (`:223`) e dopo eventuali
#   involucri che impostano flag sul modulo (`_g4_prova.py` lo fa DENTRO l'involucro di
#   `_applica_flag`, quindi e' gia' incluso). Letto prima, mostrerebbe i DEFAULT -- cioe'
#   esattamente la bugia che il referto esiste per impedire, e `collaudo()` verifica
#   QUEST'ORDINE dall'AST.
#   PERCHE' RIFIUTA DI PARTIRE invece di avvisare: un run senza referto e' un run le cui
#   conclusioni si dedurranno dal sorgente -- ed e' cosi' che sono nati `S10` e la lettura
#   sbagliata su `SPINORE_CORRETTO`, nello stesso giorno.
import _configurazione as _CFG                                              # noqa: E402
try:
    _p_cfg, _p_cfgj = _CFG.scrivi(DEST, S, os.path.join(ROOT, "soliton_simulator.py"),
                                  sys.argv, argv_esterno=_ARGV_VERBATIM,
                                  driver=os.path.abspath(__file__),
                                  seme=SEME_EFFETTIVO)
except Exception as _e_cfg:
    raise SystemExit("[configurazione] RIFIUTO DI PARTIRE: non riesco a scrivere "
                     "CONFIGURAZIONE.txt in %s -- %s: %s"
                     % (DEST, type(_e_cfg).__name__, _e_cfg))
print("  CONFIGURAZIONE -> %s  (+ .json)" % _p_cfg)

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
