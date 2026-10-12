# -*- coding: utf-8 -*-
"""IL COLLAUDO DEL SOTTO-PEZZO `5b` — **il contenitore, e i cinque pezzi unitari.**

### ⭐ **LE TRE DOMANDE A CUI RISPONDE:**

1. **ZERO allocazioni** nei tick dopo il primo? *(e' la promessa del doppio contenitore)*
2. `cresci()` **al piu' una volta per tick** — e **due volte ALZA**? *(la regola che la
   verifica esterna ha chiesto, dopo aver mostrato che il raddoppio **non** toglie la
   ricostruzione)*
3. i cinque pezzi sono **UNITARI**, e il Grover e' **un'involuzione al bit**?

### ⛔ **E OGNI BRACCIO CHE <<DEVE FALLIRE>> SI VERIFICA SULLA CHIAVE GIUSTA.**
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
sys.path.insert(0, os.path.join(os.path.dirname(_QUI), "csv"))

import _presidio                                              # noqa: E402
import incidenza as IN                                        # noqa: E402
import motore as MO                                           # noqa: E402
import stato as ST                                            # noqa: E402

OK = [0, 0]


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    print("  %-64s %s   %s" % (che[:64], "PASSA" if passa else "### FALLISCE", nota))


def _banco(nn, sommatoria, seme):
    """### Un anello con la geometria **banale** *(`n = z`, `U = I`)* e uno stato casuale.

    ### ⚠ **La geometria banale NON e' una semplificazione della fisica:** e' **il caso
    di controllo** in cui le risposte si sanno a mano, e serve a provare **il
    contenitore**, non la geometria. ### **La geometria vera entra da fuori, ed e' una
    decisione aperta.**
    """
    ii = np.arange(nn, dtype=IN.INDICE)
    jj = (ii + 1) % nn
    inc = IN.Incidenza(ii, jj, nn, capacita=2 * nn)
    nv = np.zeros((2 * inc.m, 3), dtype=float)
    nv[:, 2] = 1.0
    U = np.zeros((inc.m, 2, 2), dtype=complex)
    U[:, 0, 0] = 1.0
    U[:, 1, 1] = 1.0
    st = ST.nuovo(nn, inc.m)
    r = np.random.default_rng(seme)
    st["psi_h"][...] = (r.normal(size=st["psi_h"].shape)
                        + 1j * r.normal(size=st["psi_h"].shape))
    st["phi_h"][...] = r.normal(size=st["phi_h"].shape)
    mot = MO.Motore(inc, MO.Geometria(nv, U), st, np.full(nn, 0.37), sommatoria)
    return inc, st, mot


def _norma(v):
    return float(np.sum(np.abs(v) ** 2))


def main(argv):
    _presidio.avvia(__file__)
    print("=" * 100)
    print("IL SOTTO-PEZZO `5b`: IL DOPPIO CONTENITORE E I CINQUE PEZZI UNITARI")
    print("=" * 100)

    # =============================================== (1) ZERO ALLOCAZIONI DOPO IL PRIMO
    inc, st, mot = _banco(64, "numpy", 11)
    esito("### il collaudo ha MATERIA: lo stato NON e' nullo",
          _norma(st["psi_h"]) > 1.0 and _norma(st["phi_h"]) > 1.0,
          "### |psi|^2=%.3f |phi|^2=%.3f: su zero ogni operatore sarebbe l'identita'"
          % (_norma(st["psi_h"]), _norma(st["phi_h"])))

    def passo():
        mot.apri_tick()
        mot.operatori["grover"](st, {}, 1)
        mot.operatori["moneta_spin"](st, {"eps": 0.5}, 1)
        mot.operatori["spostamento_trasporto"](st, {}, 1)
        mot.operatori["grover_scalare"](st, {}, 1)
        mot.operatori["spostamento_scalare"](st, {}, 1)
        mot.chiudi_tick()

    passo()
    primi = mot.ripieghi
    for _ in range(25):
        passo()
    esito("### (1) ZERO allocazioni nei 25 tick dopo il primo",
          mot.ripieghi == primi and primi > 0,
          "### %d buffer al primo tick, %d dopo: e' la promessa del doppio contenitore"
          % (primi, mot.ripieghi - primi))
    esito("### e il contatore delle applicazioni le ha contate TUTTE",
          all(mot.applicazioni[o] == 26 for o in MO.OPERATORI),
          "### %r" % sorted(set(mot.applicazioni.values())))

    # ============================================ (2) LA REGOLA DEL TICK, NEI DUE VERSI
    print()
    tieni = np.ones(inc.m, dtype=bool)
    mot.apri_tick()
    mot.cresci(tieni, [], [], 0)
    quante = mot.chiudi_tick()
    esito("### (2) UNA `cresci()` in un tick: passa, e il tick la conta",
          quante == 1 and mot.cresciute == 1,
          "### se questo fallisse, il braccio sotto non direbbe niente")
    # ### ⛔ **E DUE VOLTE DEVE ALZARE**, ed e- la regola che la verifica esterna ha
    # ### chiesto: il raddoppio ### **non toglie la ricostruzione**, che costa
    # ### `O(m log m)` ### **a chiamata.**
    mot.apri_tick()
    mot.cresci(tieni, [], [], 0)
    mot.cresci(tieni, [], [], 0)
    try:
        mot.chiudi_tick()
        passa, nota = False, "### NON ha alzato: la regola NON e' un impedimento"
    except AssertionError as e:
        passa = "il tetto e' 1" in str(e)
        nota = ("### e per la chiave giusta" if passa
                else "### ha alzato per un'altra ragione: %r" % str(e)[:50])
    esito("### (2) DEVE fallire: DUE `cresci()` nello stesso tick", passa, nota)
    # ### ⚠ **e il tick si e- CHIUSO comunque**, altrimenti il motore resterebbe
    # ### ### **bloccato dentro un tick che non si puo- chiudere.**
    esito("### e il tick si e' chiuso COMUNQUE, nonostante l'errore",
          mot.cresciute_nel_tick < 0,
          "### altrimenti il motore resterebbe bloccato in un tick senza uscita")
    for che, fai, chiave in (
            ("`cresci()` FUORI da un tick",
             lambda: mot.cresci(tieni, [], [], 0), "fuori da un tick"),
            ("`chiudi_tick` senza `apri_tick`", mot.chiudi_tick, "nessun tick aperto")):
        try:
            fai()
            passa, nota = False, "### NON ha alzato"
        except AssertionError as e:
            passa = chiave in str(e)
            nota = ("### e per la chiave giusta" if passa
                    else "### altra ragione: %r" % str(e)[:50])
        esito("### DEVE fallire: %s" % che, passa, nota)
    mot.apri_tick()
    try:
        mot.apri_tick()
        passa, nota = False, "### NON ha alzato"
    except AssertionError as e:
        passa, nota = "GIA' aperto" in str(e), "### e per la chiave giusta"
    esito("### DEVE fallire: aprire un tick quando uno e' GIA' aperto", passa, nota)
    mot.chiudi_tick()

    # ================================================ (3) L'UNITARIETA', e l'involuzione
    print()
    inc, st, mot = _banco(32, "numpy", 7)
    n0 = _norma(st["psi_h"])
    eps_m = float(np.finfo(float).eps)
    for nome, par in (("grover", {}), ("moneta_spin", {"eps": 0.5}),
                      ("spostamento_trasporto", {})):
        mot.apri_tick()
        mot.operatori[nome](st, par, 1)
        mot.ne = mot.chiudi_tick()
        n1 = _norma(st["psi_h"])
        rel = abs(n1 - n0) / n0
        esito("### (3) `%s` CONSERVA la norma" % nome, rel <= 4096 * eps_m,
              "### scarto relativo %.3e su %d estremita'" % (rel, 2 * inc.m))
        n0 = n1
    # ### ⭐ **IL GROVER E- UN-INVOLUZIONE: `G^2 = I` AL BIT.** ### ⚠ **E <<al bit>> non
    # ### e- un modo di dire:** `(2/d)S - psi` con `d` intero e `S` somma di `d` termini
    # ### ### **non e- esatto in virgola mobile**, quindi la lettura giusta e- ### **entro
    # ### pochi ulp**, e il numero si STAMPA.
    prima = st["psi_h"].copy()
    mot.apri_tick()
    mot.operatori["grover"](st, {}, 1)
    mot.operatori["grover"](st, {}, 1)
    mot.chiudi_tick()
    scarto = float(np.max(np.abs(st["psi_h"] - prima)))
    scala = float(np.max(np.abs(prima)))
    esito("### (3) il Grover e' un'INVOLUZIONE: `G^2 = I` entro pochi ulp",
          scarto <= 64 * eps_m * scala,
          "### scarto %.3e su scala %.3e, cioe' %.1f ulp"
          % (scarto, scala, scarto / (eps_m * scala)))
    # ### ⛔ **E UNA FRAZIONE DIVERSA DA `1` DEVE ALZARE:** la radice di una riflessione
    # ### ### **non e- una riflessione**, quindi mezzo Grover ### **non significa niente.**
    for nome in ("grover", "spostamento_trasporto", "grover_scalare",
                 "spostamento_scalare"):
        mot.apri_tick()
        try:
            mot.operatori[nome](st, {}, 0.5)
            passa, nota = False, "### NON ha alzato: mezzo pezzo unitario passerebbe"
        except AssertionError as e:
            passa = "non ha significato" in str(e)
            nota = ("### e per la chiave giusta" if passa
                    else "### altra ragione: %r" % str(e)[:50])
        mot.chiudi_tick()
        esito("### DEVE fallire: `%s` a frazione 0.5" % nome, passa, nota)
    # ### ⚠ **E la moneta di spin INVECE la prende**, perche- ### **e- un flusso in
    # ### `eps dtau`**: `exp(-i a) exp(-i b) = exp(-i(a+b))`. ### **Senza questo braccio,
    # ### il braccio di sopra proverebbe solo che tutto alza.**
    mot.apri_tick()
    mot.operatori["moneta_spin"](st, {"eps": 0.5}, 0.5)
    mot.chiudi_tick()
    esito("### e la moneta di spin INVECE accetta 0.5: e' un FLUSSO in `eps dtau`",
          True, "### altrimenti il braccio di sopra proverebbe solo che tutto alza")
    # ### ⭐ **E LE DUE META- FANNO L-INTERO: `exp(-ia/2) exp(-ia/2) = exp(-ia)`.**
    _i2, s2, m2 = _banco(16, "numpy", 3)
    pr = s2["psi_h"].copy()
    m2.apri_tick()
    m2.operatori["moneta_spin"](s2, {"eps": 0.5}, 1)
    m2.chiudi_tick()
    intero = s2["psi_h"].copy()
    s2["psi_h"][...] = pr
    m2.apri_tick()
    m2.operatori["moneta_spin"](s2, {"eps": 0.5}, 0.5)
    m2.operatori["moneta_spin"](s2, {"eps": 0.5}, 0.5)
    m2.chiudi_tick()
    d = float(np.max(np.abs(s2["psi_h"] - intero)))
    esito("### e DUE META' fanno l'INTERO: la moneta e' un flusso, non un'involuzione",
          d <= 64 * eps_m * float(np.max(np.abs(intero))),
          "### scarto %.3e: se non tornasse, <<frazione>> non vorrebbe dire niente" % d)

    # ====================================== (4) LE DUE SOMMATORIE DANNO LO STESSO NUMERO
    print()
    _a, sa, ma = _banco(24, "numpy", 5)
    _b, sb, mb = _banco(24, "esatta", 5)
    ma.apri_tick(); ma.operatori["grover"](sa, {}, 1); ma.chiudi_tick()
    mb.apri_tick(); mb.operatori["grover"](sb, {}, 1); mb.chiudi_tick()
    d = float(np.max(np.abs(sa["psi_h"] - sb["psi_h"])))
    sc = float(np.max(np.abs(sa["psi_h"])))
    esito("### (4) le DUE sommatorie danno lo stesso numero entro pochi ulp",
          d <= 64 * eps_m * sc,
          "### scarto %.3e su scala %.3e: in aritmetica esatta sono LO STESSO numero"
          % (d, sc))

    # ========================================== (5) LO STATO SEGUE LA PERMUTAZIONE
    print()
    inc, st, mot = _banco(10, "numpy", 2)
    prima = st["psi_h"].copy()
    tieni = np.ones(inc.m, dtype=bool)
    tieni[0] = False
    mot.apri_tick()
    dove = mot.cresci(tieni, [0, 10], [10, 1], 1)
    mot.chiudi_tick()
    vive = dove >= 0
    buono = bool(np.allclose(st["psi_h"][dove[vive]], prima[:2 * 10][vive], atol=0))
    esito("### (5) lo stato SEGUE la permutazione, al bit",
          buono, "### %d estremita' vive su %d" % (int(vive.sum()), 2 * 10))
    esito("### e le estremita' NUOVE nascono a ZERO",
          abs(_norma(st["psi_h"]) - _norma(prima[:2 * 10][vive])) <= 1e-12,
          "### altrimenti un'estremita' nuova porterebbe un dato che nessuno ha messo")

    # ============================================= (6) I CASI CHE DEVONO FALLIRE
    print()
    nv = np.zeros((4, 3), dtype=float)
    nv[:, 2] = 1.0
    Ub = np.zeros((2, 2, 2), dtype=complex)
    Ub[:, 0, 0] = 1.0
    Ub[:, 1, 1] = 1.0
    i2 = IN.Incidenza([0, 1], [1, 2], 3, capacita=2)
    for che, fai, chiave in (
            ("un versore NON unitario",
             lambda: MO.Geometria(np.full((4, 3), 0.9), Ub), "NON unitario"),
            ("una `U` NON unitaria",
             lambda: MO.Geometria(nv, Ub * 2.0), "NON unitaria"),
            ("`n` della forma sbagliata",
             lambda: MO.Geometria(np.zeros((4, 2)), Ub), "versore per ESTREMITA'"),
            ("`n` e `U` di taglie INCOERENTI",
             lambda: MO.Geometria(nv, Ub[:1]), "il doppio degli archi"),
            ("una `sommatoria` fuori vocabolario",
             lambda: MO.Motore(i2, MO.Geometria(nv, Ub), ST.nuovo(3, 2),
                               np.zeros(3), "veloce"), "sommatoria"),
            ("un `dtau` della forma sbagliata",
             lambda: MO.Motore(i2, MO.Geometria(nv, Ub), ST.nuovo(3, 2),
                               np.zeros(7), "numpy"), "PER NODO"),
            ("una geometria di un'ALTRA taglia",
             lambda: MO.Motore(IN.Incidenza([0], [1], 2, capacita=1),
                               MO.Geometria(nv, Ub), ST.nuovo(2, 1),
                               np.zeros(2), "numpy"), "un'altra taglia")):
        try:
            fai()
            passa, nota = False, "### NON ha alzato: il caso NON e' impedito"
        except AssertionError as e:
            passa = chiave.lower() in str(e).lower()
            nota = ("### e per la chiave GIUSTA (%r)" % chiave if passa
                    else "### altra ragione: %r" % str(e)[:55])
        except Exception as e:                                # noqa: BLE001
            passa, nota = False, "### eccezione SBAGLIATA: %r" % str(e)[:55]
        esito("### DEVE fallire: %s" % che, passa, nota)
    # ### ⛔ **E LA MONETA SENZA `eps` DEVE ALZARE:** un `eps` scelto dal motore
    # ### ### **non ha origine**, e l-origine di un numero e- il punto della tabella.
    _i3, s3, m3 = _banco(8, "numpy", 1)
    m3.apri_tick()
    try:
        m3.operatori["moneta_spin"](s3, {}, 1)
        passa, nota = False, "### NON ha alzato: il motore avrebbe scelto un numero"
    except AssertionError as e:
        passa = "dalla TABELLA" in str(e)
        nota = "### e per la chiave giusta" if passa else "### %r" % str(e)[:50]
    m3.chiudi_tick()
    esito("### DEVE fallire: la moneta di spin SENZA `eps` in tabella", passa, nota)

    print("=" * 100)
    print("IL SOTTO-PEZZO `5b`: %d su %d   ### %s"
          % (OK[0], OK[1], "TUTTI PASSATI" if OK[0] == OK[1] else "CI SONO BUCHI"))
    print("=" * 100)
    return 0 if OK[0] == OK[1] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
