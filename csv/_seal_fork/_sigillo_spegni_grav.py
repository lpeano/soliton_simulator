# -*- coding: utf-8 -*-
"""SIGILLO — `GRAV_BIFASE = False` SPEGNE SOLO `S09`, e nient'altro. [G3, prima della prova]

⚠ NON MODIFICA IL SIMULATORE NE' IL DRIVER. Imposta la costante SUL MODULO dalla rigiocata, che
  e' esattamente il modo in cui la prova di spegnimento la impostera'.

COSA DEVE DIMOSTRARE, e sono tre cose diverse che NON si sostituiscono:
  1. che lo spegnimento **SPEGNE** (`S09` sparisce);
  2. che spegne **SOLO** quello (tutti gli altri scrittori di `d0` conservano le stesse
     invocazioni, e cio' che sta A MONTE resta BYTE-IDENTICO);
  3. che **la memoria del moto non e' toccata** (`mem_mot` identico bit per bit).

⚠ E UNA DISTINZIONE CHE VA FATTA E NON NASCOSTA, sulla COESIONE.
  L'ordine dei diciannove siti di scrittura di `d0`, VERIFICATO dal sorgente, e':
      S01 S02 S03 S04 P1 S05 P2 S06 S07 S08 P3 | S09 S10 P4 | S11 P5 S12 P6 P7
                                    a monte       GRAVITA'      a valle
  **`S12_coesione` sta A VALLE del blocco della gravita'.** Quindi, spenta la gravita', la
  coesione **vede un `d0` diverso** e i suoi incrementi **cambiano**. **Questo non significa che
  l'interruttore tocchi la LEGGE della coesione**, e il sigillo non lo afferma: afferma che
  **il numero di invocazioni e' lo stesso** e che **la legge non e' gated su `GRAV_BIFASE`**, e
  quest'ultima la dimostra **strutturalmente** (`T5`), non per campione.
  **Dire «la coesione non e' toccata» senza questa distinzione sarebbe FALSO.**

⚠ `P1-sexies`: i criteri sono collaudati PRIMA su casi a risposta nota, **e il piu' importante e'
  quello che DEVE fallire** -- uno spegnimento che tocca ANCHE un altro scrittore. Se `T2` non lo
  vedesse, `T2` sarebbe cieco e il sigillo direbbe «spegne solo `S09`» senza poterlo sapere.
  Il caso che deve fallire e' girato **sul codice vero**, non simulato: `MEM_HEBB = False`, cioe'
  proprio lo spegnimento che il mandato VIETA di usare.
ASCII PURO.
"""
import ast
import io
import os
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, RADICE)
OUT = os.path.join(_QUI, "_sig_spegni_grav", "REFERTO.txt")

PASSI = 3
for _a in sys.argv[1:]:
    if _a.startswith("--passi="):
        PASSI = int(_a.split("=", 1)[1])

# LA CONFIGURAZIONE DELLA VALIDAZIONE, identica a quella di `G2`
ARGV = ["soliton_simulator.py", "--test", "N-MASSE", "--nmasse", "3", "--sep", "4.0",
        "--giri", "0", "--campo-spinoriale", "--spinore-vivo", "--spinore-corretto",
        "--chi-core", "--calore-scal", "--deparam-orologio", "--verlet", "--fork-su2",
        "--fork-su2-mem", "--cs-dinamico", "--tau-luce", "--rumore-colorato",
        "--pav-com", "--guscio-morbido", "--zeta-vir", "--chi-basc", "--chi-coop",
        "--coes-adim", "--plast-din", "--viriale", "--olon-part",
        "--peq-esatto", "--peq-nascita-locale", "--scala-min-passo", "--coes-causale",
        "--anom-simm", "--invarianti=on"]

# L'ordine dei siti, VERIFICATO dal sorgente il 2026-09-22 (righe 2464..6030).
A_MONTE = ("S01_archi_nuovi", "S02_rilass_visco", "S03_diff_guscio", "S04_rilass_TAU_P",
           "P1_dopo_rilass", "S05_spinta_locale", "P2_dopo_spinta", "S06_mitosi",
           "S07_schwinger", "S08_proj", "P3_dopo_proj")
GRAVITA = ("S09_spinta_med", "S10_grav_med", "P4_dopo_grav")
A_VALLE = ("S11_flusso", "P5_dopo_flusso", "S12_coesione", "P6_dopo_coesione", "P7_dopo_4917")


# ------------------------------------------------------------------ I CRITERI, isolati
def solo_quello(cnt_a, cnt_b, esenti):
    """I siti NON esenti hanno le stesse invocazioni nei due bracci? Ritorna la lista dei
    colpevoli. E' il criterio di `T2`, ed e' quello che il collaudo deve saper far fallire."""
    fuori = []
    for s in sorted(set(cnt_a) | set(cnt_b)):
        if s in esenti:
            continue
        if cnt_a.get(s, 0) != cnt_b.get(s, 0):
            fuori.append((s, cnt_a.get(s, 0), cnt_b.get(s, 0)))
    return fuori


def scarto(a, b):
    """max|a-b| fra due array. ⚠ Se le forme differiscono NON ritorna 0: ritorna `nan` e la
    coppia di forme. Lo zero per MANCANZA DI CONFRONTO e' una trappola gia' catalogata."""
    if a is None or b is None:
        return float("nan"), ("assente", "assente")
    a = np.asarray(a, dtype=float); b = np.asarray(b, dtype=float)
    if a.shape != b.shape:
        return float("nan"), (a.shape, b.shape)
    if a.size == 0:
        return float("nan"), ("vuoto", "vuoto")
    return float(np.max(np.abs(a - b))), (a.shape, b.shape)


def gate_unico(percorso):
    """`T5`, LA PROVA STRUTTURALE: quante RAMIFICAZIONI dipendono da `GRAV_BIFASE`?

    Non e' un campione: e' il sorgente. Si costruisce l'AST e si cercano TUTTI i nodi `If`
    (e `IfExp`, e le comprehension con `if`) il cui TEST nomina `GRAV_BIFASE`.
    Se ce n'e' ESATTAMENTE UNO, allora **nessun'altra legge puo' essere gated su quel nome**, e
    l'affermazione «spegne solo la gravita'» non dipende piu' da quanti passi si sono girati.
    """
    with io.open(percorso, encoding="utf-8") as f:
        albero = ast.parse(f.read(), percorso)
    rami, assegn, altri = [], [], []
    for nodo in ast.walk(albero):
        if isinstance(nodo, (ast.If, ast.IfExp)):
            if any(isinstance(x, ast.Name) and x.id == "GRAV_BIFASE"
                   for x in ast.walk(nodo.test)):
                rami.append(nodo.lineno)
        elif isinstance(nodo, ast.Assign):
            for t in nodo.targets:
                if isinstance(t, ast.Name) and t.id == "GRAV_BIFASE":
                    assegn.append(nodo.lineno)
    for nodo in ast.walk(albero):
        if isinstance(nodo, ast.Name) and nodo.id == "GRAV_BIFASE":
            altri.append(nodo.lineno)
    return sorted(rami), sorted(assegn), sorted(set(altri))


def collaudo(W):
    """`P1-sexies`. Il criterio di `T2` si collauda su casi a risposta NOTA, PRIMA di usarlo."""
    W("COLLAUDO DEI CRITERI su casi a RISPOSTA NOTA (`P1-sexies`), PRIMA di sigillare\n")
    W("-" * 96 + "\n")
    e = []
    base = {"S08_proj": 3, "S09_spinta_med": 3, "S11_flusso": 3, "S12_coesione": 3}
    esenti = set(GRAVITA)

    spento_bene = dict(base); spento_bene["S09_spinta_med"] = 0
    f1 = solo_quello(base, spento_bene, esenti)
    ok1 = (len(f1) == 0)
    W("K1 spegnimento CHIRURGICO (solo `S09` sparisce) -> atteso NESSUN colpevole\n")
    W("     colpevoli: %s  -> %s\n" % (f1 if f1 else "nessuno",
                                       "OK" if ok1 else "*** FALSO ALLARME ***"))
    e.append(ok1)

    # IL CASO CHE DEVE FALLIRE, e non e' quello catastrofico: e' quello CHIRURGICO SBAGLIATO.
    spento_male = dict(base); spento_male["S09_spinta_med"] = 0
    spento_male["S11_flusso"] = 0
    f2 = solo_quello(base, spento_male, esenti)
    ok2 = any(s == "S11_flusso" for s, _a, _b in f2)
    W("K2 IL CASO CHE DEVE FALLIRE: lo spegnimento tocca ANCHE `S11_flusso`\n")
    W("     colpevoli: %s\n" % f2)
    W("     atteso: `S11_flusso` fra i colpevoli -> %s\n"
      % ("OK: il criterio VEDE uno spegnimento troppo largo"
         if ok2 else "*** IL CRITERIO E' CIECO: direbbe `spegne solo S09` senza saperlo ***"))
    e.append(ok2)

    # e il caso PIU' SUBDOLO: un sito che COMPARE invece di sparire.
    spento_extra = dict(base); spento_extra["S09_spinta_med"] = 0
    spento_extra["S05_spinta_locale"] = 7
    f3 = solo_quello(base, spento_extra, esenti)
    ok3 = any(s == "S05_spinta_locale" for s, _a, _b in f3)
    W("K3 un sito che COMPARE invece di sparire -> atteso segnalato\n")
    W("     colpevoli: %s  -> %s\n" % (f3, "OK" if ok3 else "*** NON LO VEDE ***"))
    e.append(ok3)

    # `scarto` NON deve restituire 0 per mancanza di confronto (trappola gia' catalogata)
    s_ok, _ = scarto(np.ones(5), np.ones(5))
    s_sh, forme = scarto(np.ones(5), np.ones(7))
    ok4 = (s_ok == 0.0) and (not np.isfinite(s_sh))
    W("K4 `scarto`: identici -> 0.0 ; FORME DIVERSE -> `nan`, MAI 0 per mancanza di confronto\n")
    W("     identici %.3e ; forme diverse %s (shape %s) -> %s\n"
      % (s_ok, s_sh, forme, "OK" if ok4 else "*** LO ZERO SAREBBE AMBIGUO ***"))
    e.append(ok4)

    ok = all(e)
    W("-" * 96 + "\n")
    W("  -> i criteri %s\n\n" % ("PASSANO: si sigilla" if ok else "*** NON PASSANO: NON sigillo ***"))
    return ok


# ------------------------------------------------------------------ un BRACCIO
def gira(S, nome, spegni_grav, spegni_hebb, W):
    """Una rigiocata dalla semina. Ritorna invocazioni, i `dx` del PRIMO passo, e `mem_mot`."""
    sys.argv = list(ARGV)
    S.TRACCIA_D0 = False                    # ⚠ spenta DURANTE la semina: senno' i contatori
    a = S._cli(); S._applica_regime(a); S._applica_flag(a)   # conterebbero le calibrazioni
    S.GRAV_BIFASE = (not spegni_grav)       # <- IMPOSTATA SUL MODULO, come fara' la prova
    S.MEM_HEBB = (not spegni_hebb)
    # ⚠ il generatore e' PER-RETE (`self.rng = np.random.default_rng(seed)`, `:1430`), ma se
    #   qualche percorso usasse quello GLOBALE i bracci non sarebbero confrontabili. Lo si rimette
    #   identico a ogni braccio: se e' inutile non fa nulla, se serve rende il confronto lecito.
    np.random.seed(20260922)
    S._NMASSE_VIDEO["n"] = 3; S._NMASSE_VIDEO["sep"] = 4.0; S._NMASSE_VIDEO["size"] = None
    S.avvia_test("N-MASSE")()
    net = S.net
    S.stato["nframe"] = 0

    cnt, primo = {}, {}
    stato = {"passo": 0}

    def traccia(self, sito, prima, pavimento=None):
        cnt[sito] = cnt.get(sito, 0) + 1
        if stato["passo"] == 1 and sito not in primo:
            dopo = np.asarray(self.d0, dtype=float)
            pri = np.asarray(prima, dtype=float)
            primo[sito] = (dopo - pri).copy() if len(pri) == len(dopo) else None
    S.Rete._traccia_d0 = traccia
    S.TRACCIA_D0 = True

    PPF = int(S.PASSI_PER_FRAME)
    mm1 = d01 = None
    for k in range(1, PASSI + 1):
        stato["passo"] = k
        if (k - 1) % PPF == 0:
            S.passo_test()
        S.scuoti_vuoto(net); net.step(); net.mitosi()
        net.rilassa_disegno(); net.memoria_hebbiana_moto()
        if k == 1:
            mm1 = np.array(net.mem_mot, dtype=float, copy=True)
            d01 = np.array(net.d0, dtype=float, copy=True)
    W("  braccio %-8s GRAV_BIFASE=%-5s MEM_HEBB=%-5s  n=%-6d archi=%-7d siti=%d\n"
      % (nome, S.GRAV_BIFASE, S.MEM_HEBB, net.n, len(net.i), len(cnt)))
    return {"cnt": cnt, "primo": primo, "mem_mot": mm1, "d0": d01, "n": net.n}


def main():
    try:
        os.makedirs(os.path.dirname(OUT))
    except OSError:
        pass
    o = io.open(OUT, "w", encoding="utf-8", newline="\n")
    W = o.write
    W("# SIGILLO -- `GRAV_BIFASE = False` SPEGNE SOLO `S09`\n")
    W("# prima della prova di spegnimento `G3`. Nessuna modifica a simulatore ne' driver.\n")
    W("# %d passi dalla semina per braccio, configurazione della validazione.\n#\n" % PASSI)
    if not collaudo(W):
        o.close(); print(io.open(OUT, encoding="utf-8").read()); return 1

    os.chdir(RADICE)
    import soliton_simulator as S
    import hashlib
    blob = hashlib.sha1(
        open(os.path.join(RADICE, "soliton_simulator.py"), "rb").read()).hexdigest()[:8]
    seme = S.Rete.__init__.__defaults__[0]
    W("blob simulatore (sha1 byte grezzi) %s   seme %s\n\n" % (blob, seme))

    t0 = time.time()
    W("I QUATTRO BRACCI:\n")
    ON = gira(S, "ON", False, False, W)
    ONB = gira(S, "ON-bis", False, False, W)
    OFF = gira(S, "OFF", True, False, W)
    HEBB = gira(S, "HEBB", False, True, W)
    W("  (%.1f s)\n\n" % (time.time() - t0))

    esiti = []

    def esito(nome, ok, riga):
        esiti.append((nome, ok))
        W("%-5s %-4s %s\n" % (nome, "PASS" if ok else "FAIL", riga))

    W("=" * 96 + "\n")
    W("I CRITERI\n")
    W("=" * 96 + "\n")

    # ---- T0: senza questo, uno zero non significa niente
    f0 = solo_quello(ON["cnt"], ONB["cnt"], set())
    pe = 0.0
    for s in ON["primo"]:
        d, _f = scarto(ON["primo"][s], ONB["primo"].get(s))
        if np.isfinite(d):
            pe = max(pe, d)
    d_mm, _ = scarto(ON["mem_mot"], ONB["mem_mot"])
    ok0 = (len(f0) == 0) and (pe == 0.0) and (d_mm == 0.0)
    esito("T0", ok0, "RIPRODUCIBILITA': due bracci ON identici? invocazioni diverse=%d, "
                     "max|dx| al passo 1 = %.3e, max|mem_mot| = %.3e" % (len(f0), pe, d_mm))
    if not ok0:
        W("\n*** T0 FALLISCE: i due bracci ON NON coincidono, quindi QUALUNQUE differenza\n")
        W("    misurata sotto sarebbe indistinguibile dalla deriva. IL SIGILLO SI FERMA. ***\n")
        o.close(); print(io.open(OUT, encoding="utf-8").read()); return 1

    # ---- T1: lo spegnimento SPEGNE
    on9 = ON["cnt"].get("S09_spinta_med", 0)
    off9 = OFF["cnt"].get("S09_spinta_med", 0)
    off10 = OFF["cnt"].get("S10_grav_med", 0)
    off4 = OFF["cnt"].get("P4_dopo_grav", 0)
    ok1 = (on9 > 0) and (off9 == 0) and (off10 == 0) and (off4 == 0)
    esito("T1", ok1, "LO SPEGNIMENTO SPEGNE: S09 ON=%d -> OFF=%d ; S10 OFF=%d ; P4 OFF=%d"
                     % (on9, off9, off10, off4))

    # ---- T2: spegne SOLO quello
    f2 = solo_quello(ON["cnt"], OFF["cnt"], set(GRAVITA))
    ok2 = (len(f2) == 0)
    esito("T2", ok2, "SPEGNE SOLO QUELLO: siti (non gravita') con invocazioni diverse = %d %s"
                     % (len(f2), f2 if f2 else ""))

    # ---- T3: byte-identita' A MONTE, al primo passo
    peg, chi = 0.0, None
    for s in A_MONTE:
        if s not in ON["primo"]:
            continue
        d, _f = scarto(ON["primo"][s], OFF["primo"].get(s))
        if not np.isfinite(d):
            peg, chi = float("nan"), s
            break
        if d > peg:
            peg, chi = d, s
    ok3 = (peg == 0.0)
    esito("T3", ok3, "BYTE-IDENTITA' A MONTE al passo 1: max|dx_ON - dx_OFF| = %.3e%s"
                     % (peg, "" if chi is None else "  (peggiore: %s)" % chi))

    # ---- T4: la MEMORIA DEL MOTO non e' toccata
    d_mm2, forme = scarto(ON["mem_mot"], OFF["mem_mot"])
    ok4 = (d_mm2 == 0.0)
    esito("T4", ok4, "MEMORIA DEL MOTO intatta: max|mem_mot_ON - mem_mot_OFF| = %.3e  shape %s"
                     % (d_mm2, forme))

    # ---- T5: la prova STRUTTURALE
    rami, assegn, tutti = gate_unico(os.path.join(RADICE, "soliton_simulator.py"))
    ok5 = (len(rami) == 1)
    esito("T5", ok5, "GATE UNICO (AST): ramificazioni che dipendono da GRAV_BIFASE = %d, righe %s"
                     % (len(rami), rami))
    W("      assegnamenti: righe %s ; tutte le occorrenze del nome: righe %s\n"
      % (assegn, tutti))
    W("      -> se la ramificazione e' UNA SOLA, nessun'altra legge PUO' essere gated su quel\n")
    W("         nome, e l'affermazione non dipende piu' da quanti passi si sono girati.\n")

    # ---- T6: IL CASO CHE DEVE FALLIRE, sul codice VERO
    f6 = solo_quello(ON["cnt"], HEBB["cnt"], set(GRAVITA))
    ok6 = (len(f6) > 0)
    esito("T6", ok6, "IL CASO CHE DEVE FALLIRE -- `MEM_HEBB=False`: siti toccati OLTRE la "
                     "gravita' = %d" % len(f6))
    for s, a_, b_ in f6:
        W("      %-20s ON=%-4d HEBB=%-4d\n" % (s, a_, b_))
    W("      -> `T2` su questo braccio FALLISCE, come deve. Se `T2` lo avesse dato per buono,\n")
    W("         direbbe \"spegne solo S09\" SENZA POTERLO SAPERE. Ed e' anche la prova, sul\n")
    W("         codice vero, di perche' il mandato VIETA `MEM_HEBB=False` come spegnimento.\n")

    # ---- la DISTINZIONE sulla coesione, dichiarata e non nascosta
    W("\n" + "-" * 96 + "\n")
    W("LA COESIONE: cosa il sigillo AFFERMA e cosa NO\n")
    W("-" * 96 + "\n")
    d12, f12 = scarto(ON["primo"].get("S12_coesione"), OFF["primo"].get("S12_coesione"))
    W("  `S12_coesione` sta A VALLE del blocco della gravita' (ordine verificato dal sorgente).\n")
    W("  invocazioni ON=%d OFF=%d  -> %s\n"
      % (ON["cnt"].get("S12_coesione", 0), OFF["cnt"].get("S12_coesione", 0),
         "UGUALI" if ON["cnt"].get("S12_coesione", 0) == OFF["cnt"].get("S12_coesione", 0)
         else "DIVERSE"))
    W("  max|dx_ON - dx_OFF| al passo 1 = %.6e   shape %s\n" % (d12, f12))
    W("  -> IL SIGILLO AFFERMA: la coesione gira lo STESSO NUMERO DI VOLTE, e la sua legge NON e'\n")
    W("     gated su `GRAV_BIFASE` (`T5`: la ramificazione e' una sola).\n")
    W("  -> IL SIGILLO NON AFFERMA che i suoi incrementi siano identici: NON LO SONO, e non\n")
    W("     devono esserlo. La coesione vede un `d0` diverso perche' la gravita' non lo ha\n")
    W("     spostato. E' FISICA CHE PROPAGA, non l'interruttore che la tocca.\n")
    W("     Dire \"la coesione non e' toccata\" senza questa distinzione sarebbe FALSO.\n")

    n_ok = sum(1 for _n, k in esiti if k)
    W("\n" + "=" * 96 + "\n")
    W("ESITO: %d/%d\n" % (n_ok, len(esiti)))
    W("=" * 96 + "\n")
    if n_ok == len(esiti):
        W("*** SIGILLO PASSATO: `GRAV_BIFASE = False` spegne SOLO la gravita' bifase.\n")
        W("    La prova di spegnimento `G3` puo' partire. ***\n")
    else:
        W("*** SIGILLO FALLITO: la prova di spegnimento NON parte. ***\n")
    W("\nLIMITI: %d passi per braccio, UN seme, UNA scena. `T2` e' un confronto di CONTEGGI su\n"
      % PASSI)
    W("  pochi passi; cio' che lo rende conclusivo NON e' il numero di passi ma `T5`, che e'\n")
    W("  strutturale e non campionario.\n")
    o.close()
    print(io.open(OUT, encoding="utf-8").read())
    return 0 if n_ok == len(esiti) else 1


if __name__ == "__main__":
    sys.exit(main())
