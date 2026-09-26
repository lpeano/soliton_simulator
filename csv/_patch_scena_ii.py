# -*- coding: utf-8 -*-
"""**LA CURA DI `DRIVER-SCENA-II`** *(mandato di Luca, 2026-09-26)* -- **quattro sostituzioni**.

**OGNUNA E' ASSERITA PER SE' (`P1-quater`):** l'ancora si conta e, se non e' unica o non c'e',
lo script **si ferma**. **Nessun escape** nelle stringhe: `chr()` dove serve (`L-PATCH`).

| | file | che cosa cambia | perche' |
|--:|---|---|---|
| **1** | `soliton_simulator.py` | `--nodi 0` = **nessun vuoto qui**, anche con `SEMINA_LAM` | `M0a`: `--nodi 0` chiedeva zero nodi e ne arrivavano **455** |
| **2** | `soliton_simulator.py` | il pre-rilassamento non gira **su una rete vuota** | 300 `step()` su `n = 0` non sono un rilassamento: sono un giro a vuoto |
| **3** | `csv/_test_fork/_scena_video.py` | opzione **`--scena=`** *(default `N-MASSE`, invariato)* + **`--nodi=`** | il driver FISSAVA `N-MASSE` in **due** punti |
| **4** | `csv/_test_fork/_scena_video.py` | opzione **`--seme=`**, e `SEME_EFFETTIVO` **letto da `a.seed`** | `--seed` non era mai passato: ogni run girava col seme **42** |

**LA SOSTITUZIONE 1 TOGLIE UN'ECCEZIONE, NON AGGIUNGE UNA LEGGE** (`STANDARD 10`): `--nodi 0`
significava *«niente»* a flag spento e *«saturazione»* a flag acceso — **due significati per un
valore**. Ora e' **uno solo**, in entrambi i rami.

    python csv/_patch_scena_ii.py --prova
    python csv/_patch_scena_ii.py

ASCII puro.
"""
import io
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Sostituisce testo in due sorgenti.

NL = chr(10)
_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, ".."))
SIM = "soliton_simulator.py"
DRV = "csv/_test_fork/_scena_video.py"

# ------------------------------------------------------------------- 1 e 2: il simulatore
S1_V = """    net.semina(-1 if SEMINA_LAM else a.nodi)
    if a.seed is not None or a.nodi != SEME_INIZIALE:
        for _ in range(300): net.step()
        net.rilassa_disegno(30)"""

S1_N = """    # [DRIVER-SCENA-II, 2026-09-26] `--nodi 0` = **NESSUN VUOTO QUI: lo costruisce la SCENA.**
    #   Prima `a.nodi` era guardato SOLO a flag spento: con `SEMINA_LAM` il ternario andava in
    #   saturazione e `--nodi 0` chiedeva ZERO nodi ottenendone **455** (misura 0, `M0a`). La
    #   scena `(ii)` vuole UN SOLO VUOTO e rifiutava -- correttamente: il difetto era QUI.
    #   ⚠ E' UN'ECCEZIONE IN MENO, NON UNA LEGGE IN PIU' (`STANDARD 10`): `--nodi 0` significava
    #   «niente» a flag spento e «saturazione» a flag acceso, DUE significati per un valore.
    #   Ora e' UNO SOLO in entrambi i rami. *(A flag spento il comportamento non cambia di un
    #   bit: `semina(0)` ritornava subito da se'.)*
    if a.nodi:
        net.semina(-1 if SEMINA_LAM else a.nodi)
    # ⚠ E IL PRE-RILASSAMENTO NON GIRA SU UNA RETE VUOTA: 300 `step()` con `n = 0` non sono un
    #   rilassamento, sono un giro a vuoto -- e su una rete vuota non c'e' niente da rilassare.
    #   Il ramo con `net.n > 0` e' INVARIATO.
    if net.n and (a.seed is not None or a.nodi != SEME_INIZIALE):
        for _ in range(300): net.step()
        net.rilassa_disegno(30)"""

# ------------------------------------------------------------------- 3 e 4: il driver
S2_V = 'CHIBASC = "on"'
S2_N = '''CHIBASC = "on"
# [DRIVER-SCENA-II, 2026-09-26] LA SCENA E' UN'OPZIONE, NON UNA COSTANTE.
#   Il driver FISSAVA `N-MASSE` in DUE punti (l'argv del simulatore e `avvia_test`), e la scena
#   `(ii)` -- quella del RUN BASE -- non era raggiungibile da nessun comando.
#   ⚠ IL DEFAULT RESTA `N-MASSE`, E LO DICHIARO: e' l'unico valore che riproduce VERBATIM il
#   comportamento di prima, e senza quello la byte-identita' del criterio 1 non avrebbe niente
#   da dimostrare. **Nessun comando gia' scritto cambia di un bit.**
SCENA = "N-MASSE"
# `--nodi=` NON si passa per default: `None` significa «non inoltrare l'opzione», cioe' il
#   default del simulatore (`SEME_INIZIALE`). La scena `(ii)` vuole `0`, e il driver lo passa
#   DICENDOLO (vedi sotto): non lo aggiunge in silenzio (`A9`).
NODI = None
# [DRIVER-SCENA-II] IL SEME E' UN'OPZIONE, NON UNA COSTANTE NASCOSTA. `--seed` non era mai
#   passato: OGNI run del driver girava col seme **42** (`_applica_flag`: `Rete(a.seed if
#   a.seed is not None else 42)`). Senza un seme variabile non esiste una barra fra semi, e
#   `P3` ne chiede **almeno quattro**. `None` = non inoltrare, cioe' 42 come prima.
SEME = None'''

S3_V = '''    elif _x == "--riprendi":'''
S3_N = '''    elif _x.startswith("--scena="):
        SCENA = _x.split("=", 1)[1].strip()
    elif _x.startswith("--nodi="):
        NODI = int(_x.split("=", 1)[1])
    elif _x.startswith("--seme="):
        SEME = int(_x.split("=", 1)[1])
    elif _x == "--riprendi":'''

S4_V = '''sys.argv = ["soliton_simulator.py", "--test", "N-MASSE", "--nmasse", NMASSE, "--sep", SEP,'''
S4_N = '''# [DRIVER-SCENA-II] la scena `(ii)` COSTRUISCE IL SUO VUOTO, e ne vuole UNO SOLO: qui il
#   driver passa `--nodi 0` e **LO STAMPA** (poco sotto), invece di aggiungerlo in silenzio.
#   Un `--nodi=` esplicito vince, perche' chi lo scrive sa cosa sta chiedendo.
if NODI is None and SCENA == "MASSE-COERENTI":
    NODI = 0
sys.argv = ["soliton_simulator.py", "--test", SCENA, "--nmasse", NMASSE, "--sep", SEP,'''

S5_V = '''    + (["--chi-basc"] if CHIBASC == "on" else []) \\'''
S5_N = '''    + ([] if NODI is None else ["--nodi", str(NODI)]) \\
    + ([] if SEME is None else ["--seed", str(SEME)]) \\
    + (["--chi-basc"] if CHIBASC == "on" else []) \\'''

S6_V = '''S.avvia_test("N-MASSE")()    # il costruttore UFFICIALE della scena -> _semina_n_masse()'''
S6_N = '''if SCENA not in S.TESTS:      # il vocabolario si LEGGE dal modulo, non si ricopia
    raise SystemExit("--scena=%s non esiste. Le scene del simulatore sono: %s"
                     % (SCENA, ", ".join(sorted(S.TESTS))))
print("\\n  SCENA: %s%s" % (SCENA, "" if NODI is None else
                            ("   `--nodi %d` PASSATO AL SIMULATORE (la scena costruisce il suo "
                             "vuoto: non lo aggiungo in silenzio)" % NODI)))
S.avvia_test(SCENA)()        # il costruttore UFFICIALE della scena'''

S7_V = '''SEME_EFFETTIVO = _insp.signature(S.Rete.__init__).parameters["seed"].default'''
S7_N = '''# [DRIVER-SCENA-II, 2026-09-26] IL SEME SI LEGGE DA `a.seed`, NON DALLA FIRMA DELLA CLASSE.
#   La firma dice il DEFAULT (42); `a.seed` dice quello che il run USA. Finche' `--seed` non era
#   passato i due coincidevano -- quindi il driver non mentiva -- ma con `--seme` NON coincidono
#   piu', e leggere la firma scriverebbe `42` in un run con un altro seme (`P6`).
SEME_EFFETTIVO = (a.seed if a.seed is not None
                  else _insp.signature(S.Rete.__init__).parameters["seed"].default)'''

#   ⚠ `NN` E' LA COPPIA DI CARATTERI barra-n, COMPOSTA CON `chr()` E NON SCRITTA COME ESCAPE.
#   Scritta come escape dentro un heredoc e' MORTA: diventa un fine-riga vero, e l'ancora non
#   si trova piu' (`0 volte`). **E' successo qui, il 2026-09-26** -- ed e' la ragione per cui
#   `L-PATCH` vieta gli escape nei patch script.
NN = chr(92) + "n"

S8_V = ('print("' + NN + '  scena avviata: n = %d nodi alla semina (N_c*0.8 per massa, %s masse)"'
        + NL + '      % (S.net.n, NMASSE))   # il NUMERO DI MASSE si STAMPA, non si assume: '
        + 'era cablato a "3"')
S8_N = NL.join([
    "# [DRIVER-SCENA-II, 2026-09-26] la didascalia NON puo' essere quella di `N-MASSE` per ogni",
    "#   scena: `N_c*0.8 per massa` e' vero per `N-MASSE` e FALSO per la scena `(ii)`, dove le",
    "#   masse sono REGIONI di un vuoto solo e non aggiungono nodi. Una didascalia sbagliata",
    "#   accanto a un numero giusto e' peggio di nessuna didascalia.",
    'print("' + NN + '  scena avviata: n = %d nodi%s"',
    '      % (S.net.n, ("   (N_c*0.8 per massa, %s masse)" % NMASSE) if SCENA == "N-MASSE"',
    '         else "   (la scena ha costruito il suo vuoto: le masse sono REGIONI, '
    'non nodi in piu\')"))'])

S9_V = ('print("' + NN + '  SEME EFFETTIVO (letto da Rete.__init__): %s    BLOB: %s"'
        + ' % (SEME_EFFETTIVO, BLOB_RUN))')
S9_N = NL.join([
    'print("' + NN + '  SEME EFFETTIVO (%s): %s    BLOB: %s"',
    '      % ("da --seme" if SEME is not None else "default di Rete.__init__",',
    '         SEME_EFFETTIVO, BLOB_RUN))'])

LAVORO = [(SIM, [(S1_V, S1_N)]),
          (DRV, [(S2_V, S2_N), (S3_V, S3_N), (S4_V, S4_N),
                 (S5_V, S5_N), (S6_V, S6_N), (S7_V, S7_N),
                 (S8_V, S8_N), (S9_V, S9_N)])]


if __name__ == "__main__":
    scrivi = "--prova" not in sys.argv[1:]
    print("=" * 92)
    print("CURA DI `DRIVER-SCENA-II`%s" % ("" if scrivi else "   (PROVA: non scrivo)"))
    print("=" * 92)
    for rel, coppie in LAVORO:
        p = os.path.join(RADICE, rel)
        t = io.open(p, encoding="utf-8", newline="").read()
        fatte = 0
        for vecchio, nuovo in coppie:
            if nuovo in t:
                print("  %-34s gia' applicata: %s" % (rel, vecchio.strip()[:40]))
                continue
            n = t.count(vecchio)
            if n != 1:
                raise SystemExit("%s: ancora attesa 1 volta, trovata %d:%s%s"
                                 % (rel, n, NL, vecchio[:160]))
            t = t.replace(vecchio, nuovo)
            fatte += 1
        if scrivi and fatte:
            io.open(p, "w", encoding="utf-8", newline=NL).write(t)
        print("  %-34s %d sostituzioni asserite" % (rel, fatte))
    sys.exit(0)
