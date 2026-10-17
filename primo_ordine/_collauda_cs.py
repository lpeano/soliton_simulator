# -*- coding: utf-8 -*-
"""IL COLLAUDO DI `cs(Lambda)` — **`D0`: la forma SPENTA e' il passo di oggi AL BIT.**

> ### ⛔ **`D0` del mandato del `2026-10-16`, coi criteri dell'integrazione del
> `2026-10-17`:** la forma nasce ### **SPENTA**, e con la forma spenta il passo e'
> ### **quello di oggi AL BIT** — misurato da `M-B1 --contro` *(i `12` pezzi
> ### **piu'** la distanza del passo intero `= 0` ESATTO su ### **entrambe** le scene,
> che da `D0` in avanti e' ### **un CRITERIO**)*.
> ### ⭐ **E qui dentro sta cio' che `M-B1` non puo' dire:** che la forma
> ### **ACCESA cambia il passo**, che la forma ### **spenta non e' <<`Lambda_c = 0`>>**, e
> che ### **`Lambda = 0` l'assert del cono LO RIFIUTA.**

### ⛔ **E IL VALORE DI `Lambda_c` NON SI SCEGLIE QUI:** `LC_DI_PROVA` serve ### **solo**
al caso che deve fallire. ### **La scelta e' di Luca**, e la voce che la tiene aperta e'
`[[DOMANDA-IL-VALORE-DI-LAMBDA-C]]`.
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _QUI)
sys.path.insert(0, os.path.join(_QUI, "leggi"))
sys.path.insert(0, os.path.join(os.path.dirname(_QUI), "csv"))
import _presidio                                              # noqa: E402
import deriva as DV                                           # noqa: E402
import flussi_parziali as FP                                  # noqa: E402
import tick as TK                                             # noqa: E402

NL = chr(10)
EPS = float(np.finfo(float).eps)
SCENE = ((16, 7), (12, 11))
TICK = 250
DTAU = 1.0
VUOTO_MODULO = 2.0
# ### ⛔ **IL VALORE DI PROVA NON E' UNA SCELTA DI `Lambda_c`:** serve ### **solo** al caso
# ### che DEVE fallire, e vale ### **il `Lambda` iniziale** *(cioe' `Lambda_c/Lambda = 1`)*.
# ### ⚠ **La scelta di `Lambda_c` e' di Luca**, e la voce che la tiene aperta e' nominata
# ### nel docstring in testa a questo file.
LC_DI_PROVA = 8.0
OK = [0, 0]


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    print("  %-60s %s   %s" % (che[:60], "PASSA" if passa else "### FALLISCE", nota))


def scena(nn, seme):
    return DV.scena(nn, seme, DTAU, norma="locale", vuoto_modulo=VUOTO_MODULO, su2=True)


def corri(nn, seme, lambda_c):
    """`TICK` tick, con la forma ### **spenta** *(`None`)* o ### **accesa.**"""
    _i, mot, st, par = scena(nn, seme)
    for _t in range(TICK):
        if lambda_c is not None:
            FP.accendi_cs(mot, lambda_c, st)
        TK.tick(st, mot, par)
    return st["psi_h"].copy(), st["phi_h"].copy()


def braccio_forma():
    """### La forma ### **PURA**: dove sta, che valore prende, e quando ALZA."""
    lam = np.array([0.0, 1e-8, 1.0, 8.0, 1e8])
    fuori = np.empty_like(lam)
    c = FP.cs(lam, 2.0, fuori).copy()
    esito("### (f1) la forma sta in `[0, 1)`, e `cs < 1` viene DALLA FORMA",
          bool(np.all(c >= 0.0)) and bool(np.all(c < 1.0)),
          "min %.3e  max %.17g   (nessun pavimento, nessun tetto: `A11`)"
          % (c.min(), c.max()))
    esito("### (f2) `Lambda = 0` da' `cs = 0` ESATTO, ed e' IL VALORE della forma",
          c[0] == 0.0, "`cs(0) = %.17g`: non e' un pavimento, e' la forma" % c[0])
    esito("### (f3) la forma CRESCE con `Lambda`: piu' vuoto, luce piu' veloce",
          bool(np.all(np.diff(c) > 0.0)), "monotona su %d valori" % c.size)
    # ### ⛔ **IL CASO CHE DEVE FALLIRE della forma pura:** `lambda_c = 0` ### **non e' la
    # ### forma spenta.** ### **Spegnere si fa NON ACCENDENDO**, e la funzione lo dice.
    alzato = ""
    try:
        FP.cs(lam, 0.0, fuori)
    except AssertionError as e:                               # noqa: BLE001
        alzato = str(e)[:54]
    esito("### (f4) DEVE fallire: `lambda_c = 0` NON e' la forma spenta",
          bool(alzato), "### ha alzato: %s" % alzato)


def braccio_spenta():
    """### ⭐ **LA FORMA NASCE SPENTA, e <<spenta>> e' `mot.dtau` AL BIT.**"""
    _i, mot, st, _p = scena(16, 7)
    esito("### (s1) il motore nasce con la forma SPENTA", mot.cs is None,
          "`mot.cs is None`: `Lambda_c` NON ha un valore predefinito")
    d = FP.dtau_nodo(mot)
    esito("### (s2) con la forma spenta `dtau_nodo` e' `mot.dtau` AL BIT",
          bool(np.array_equal(d, mot.dtau)) and d is mot.dtau,
          "e' lo STESSO oggetto, non una copia uguale: nessuna moltiplicazione, nessun ulp")
    # ### ⭐ **E ACCENDERE E SPEGNERE RIPORTA AL BIT**, che non e' ovvio: un buffer
    # ### riusato potrebbe restare.
    FP.accendi_cs(mot, LC_DI_PROVA, st)
    acceso = FP.dtau_nodo(mot).copy()
    FP.spegni_cs(mot)
    esito("### (s3) e dopo accendi/spegni `dtau_nodo` torna `mot.dtau` AL BIT",
          bool(np.array_equal(FP.dtau_nodo(mot), mot.dtau))
          and not bool(np.array_equal(acceso, mot.dtau)),
          "acceso max |differenza| = %.3e, spento = 0"
          % float(np.max(np.abs(acceso - mot.dtau))))


def braccio_accesa():
    """### ⛔ **IL CASO CHE DEVE FALLIRE DI `D0`** *(integrazione del `2026-10-17`)*.

    ### **Con la forma ACCESA la distanza del passo intero deve essere `> 0` su
    ENTRAMBE le scene** — altrimenti il criterio di `D0` *(distanza `= 0` con la forma
    spenta)* ### **sarebbe verde per costruzione.**
    """
    righe = []
    for nn, seme in SCENE:
        a = corri(nn, seme, None)
        b = corri(nn, seme, LC_DI_PROVA)
        dp = float(np.max(np.abs(a[0] - b[0])))
        df = float(np.max(np.abs(a[1] - b[1])))
        righe.append((nn, seme, dp, df))
        print("      nn=%-4d seme=%-4d  max|d psi| = %.6e   max|d phi| = %.6e"
              % (nn, seme, dp, df))
    esito("### (a1) DEVE fallire: con la forma ACCESA la distanza e' `> 0` su ENTRAMBE",
          all(dp > 0.0 and df > 0.0 for _n, _s, dp, df in righe),
          "la piu' piccola delle quattro distanze e' %.6e"
          % min(min(dp, df) for _n, _s, dp, df in righe))


def braccio_lambda_zero():
    """### ⛔⛔ **`Lambda = 0` DA' `cs = 0`, E L'ASSERT DEL CONO LO RIFIUTA.**

    ### ⚠ **Il mandato `D0` chiede di VERIFICARLO e, se un assert lo rifiuta, di
    RELAZIONARE invece di cambiarlo.** ### **L'assert lo rifiuta**, e questo braccio
    ### **lo fissa nel codice** cosi' che ### **non possa cambiare in silenzio.**
    ### 📌 **E nelle scene di oggi NON si presenta:** il minimo di `Lambda` su `250` tick
    e' ### **`5.6e-02`**, misurato — quindi la forma e' usabile, ### **e il caso resta
    una domanda per Luca.**
    """
    _i, mot, st, _p = scena(16, 7)
    # ### il vuoto si azzera SU UN NODO SOLO, in memoria
    st["phi_h"].fill(0)
    FP.accendi_cs(mot, LC_DI_PROVA, st)
    esito("### (z1) con `Lambda = 0` la forma da' `cs = 0` su tutti i nodi",
          bool(np.all(mot.cs == 0.0)), "max `cs` = %.17g" % float(np.max(mot.cs)))
    alzato = ""
    try:
        FP.s_nodo(mot)
    except AssertionError as e:                               # noqa: BLE001
        alzato = str(e)[:70]
    esito("### (z2) e L'ASSERT DEL CONO LO RIFIUTA: non l'ho cambiato",
          bool(alzato), "### ha alzato: %s" % alzato)


def braccio_locale():
    """### ⛔⛔ **NESSUNA COSTANTE GLOBALE NELLA DINAMICA** *(osservazione di Luca
    del `2026-10-17`)*.

    `cs_k` usa ### **SOLO grandezze del nodo `k`** e ### **un NUMERO FISSO** `Lambda_c`.
    ### **`Lambda_c` non si calcola MAI dallo stato durante la corsa** -- niente
    `Lambda_medio`, niente `V/N`, nessuna media, nessun massimo, nessuna somma sul grafo
    ### **dentro il passo.**

    ### ✅ **E QUESTO BRACCIO LO MISURA, invece di affermarlo:** si cambia `Lambda` in
    ### **UN SOLO nodo**, e `cs` deve cambiare ### **SOLO la'** -- gli altri
    ### **AL BIT.**
    ### ⛔ **E il caso che DEVE fallire e' la <<strada 3>>:** con `Lambda_c` ricalcolato
    come `V/N` a ogni tick, la stessa prova mostra `cs` cambiato ### **in TUTTI i nodi** --
    ### **ed e' esattamente la NON LOCALITA- per cui quella strada e' scartata.**
    """
    _i, mot, st, _p = scena(16, 7)
    FP.accendi_cs(mot, LC_DI_PROVA, st)
    prima = mot.cs.copy()
    # ### il vuoto si cambia su UN SOLO nodo: le estremita- di quel nodo, in memoria
    k0 = 0
    quali = np.flatnonzero(mot.inc.nodo == k0)
    assert quali.size > 0, "il nodo 0 non ha estremita-: la scena non e- quella attesa"
    st["phi_h"][quali] *= 0.5
    FP.accendi_cs(mot, LC_DI_PROVA, st)
    dopo = mot.cs.copy()
    cambiati = np.flatnonzero(dopo != prima)
    esito("### (l1) `Lambda` cambiata in UN nodo: `cs` cambia SOLO la'",
          cambiati.size == 1 and int(cambiati[0]) == k0,
          "cambiati %d nodi su %d: %s   (gli altri AL BIT)"
          % (cambiati.size, prima.size, list(cambiati[:4])))
    # ### ⛔ **IL CASO CHE DEVE FALLIRE: la <<strada 3>>, `Lambda_c = V/N` DINAMICO.**
    _i2, mot2, st2, _p2 = scena(16, 7)

    def accendi_non_locale(mot_, st_):
        """### ⚠ **La strada SCARTATA**, qui solo per mostrare che NON e' locale."""
        lam_ = mot_.densita_vuoto(st_)
        lc_ = float(np.sum(lam_) / lam_.size)        # ### V/N: UNA MEDIA SUL GRAFO
        return FP.cs(lam_, lc_, mot_._b("fp_cs_ng", (mot_.inc.n,), float)).copy()

    pr2 = accendi_non_locale(mot2, st2)
    quali2 = np.flatnonzero(mot2.inc.nodo == k0)
    st2["phi_h"][quali2] *= 0.5
    do2 = accendi_non_locale(mot2, st2)
    cam2 = np.flatnonzero(do2 != pr2)
    esito("### (l2) DEVE fallire: con `Lambda_c = V/N` dinamico cambiano TUTTI",
          cam2.size == pr2.size,
          "cambiati %d nodi su %d: e- LA NON LOCALITA- per cui la <<strada 3>> e-"
          " SCARTATA" % (cam2.size, pr2.size))


def braccio_vuoto_vietato():
    """### ⛔⛔ **IL VUOTO NULLO NON E' UNO STATO FISICO** *(decisione di Luca del
    `2026-10-17` alle `16:25`)*, e i ### **due casi che DEVONO fallire** sono quelli che il
    mandato chiede: ### **alla COSTRUZIONE** e ### **al CARICAMENTO.**

    ### ✅ **E PASSANO DALLO STESSO POSTO:** `checkpoint.riprendi` ### **ricostruisce un
    `Motore`**, quindi il divieto e' ### **uno** e non due.
    """
    import incidenza as IN
    import motore as MO
    import stato as ST
    # ### ① **ALLA COSTRUZIONE.**
    nn = 8
    ii = np.arange(nn - 1, dtype=int)
    jj = np.arange(1, nn, dtype=int)
    inc = IN.Incidenza(ii, jj, nn, capacita=nn)
    nv = np.zeros((2 * inc.m, 3), dtype=float)
    nv[:, 2] = 1.0
    U = np.zeros((inc.m, 2, 2), dtype=complex)
    U[:, 0, 0] = 1.0
    U[:, 1, 1] = 1.0
    st = ST.nuovo(nn, inc.m)
    st["psi_h"][0, 0] = 1.0
    alzato = ""
    try:
        MO.Motore(inc, MO.Geometria(nv, U), st, np.full(nn, 0.1), "numpy")
    except AssertionError as e:                               # noqa: BLE001
        alzato = str(e)[:58]
    esito("### (v1) DEVE fallire: una scena con `Lambda = 0` ALZA alla COSTRUZIONE",
          bool(alzato), "### ha alzato: %s" % alzato)
    # ### ✅ **E il controllo positivo: con `phi` non nullo la stessa scena PASSA.**
    st["phi_h"][:] = 1.0
    mot = MO.Motore(inc, MO.Geometria(nv, U), st, np.full(nn, 0.1), "numpy")
    esito("### (v2) e con `phi` NON nullo la stessa scena passa",
          mot is not None and float(np.min(mot.densita_vuoto(st))) > 0.0,
          "min `Lambda` = %.3f: si rifiuta LO STATO, non si corregge un valore"
          % float(np.min(mot.densita_vuoto(st))))
    # ### ② **AL CARICAMENTO**, e il file si guasta ### **dopo** il salvataggio: e' il
    # ### caso vero *(un file di una versione vecchia, o modificato)*.
    import checkpoint as CK
    import schema_config as SC
    import tempfile
    base = tempfile.mkdtemp(prefix="vuoto_")
    alzato2 = ""
    try:
        cfg = SC.carica(os.path.join(_QUI, "config", "prova.yaml"))
        imp = "0" * 16
        q = os.path.join(base, "chk.npz")
        CK.salva(q, mot, 7, cfg, imp)
        # ### il guasto: `phi` a zero NEL FILE, lasciando tutto il resto
        d = dict(np.load(q, allow_pickle=False))
        assert "phi_h" in d, "la chiave `phi_h` non e- nel checkpoint: %s" % sorted(d)[:6]
        d["phi_h"] = np.zeros_like(d["phi_h"])
        np.savez(q, **d)
        try:
            CK.riprendi(q, cfg, imp)
        except AssertionError as e:                           # noqa: BLE001
            alzato2 = str(e)[:58]
    finally:
        import shutil
        shutil.rmtree(base, ignore_errors=True)
    esito("### (v3) DEVE fallire: uno stato salvato con `Lambda = 0` ALZA al CARICAMENTO",
          bool(alzato2), "### ha alzato: %s" % alzato2)


def main(argv):
    del argv
    _presidio.avvia(__file__)
    print("=" * 100)
    print("IL COLLAUDO DI `cs(Lambda)` -- `D0`: LA FORMA SPENTA E' IL PASSO DI OGGI")
    print("=" * 100)
    braccio_forma()
    braccio_spenta()
    braccio_accesa()
    braccio_lambda_zero()
    braccio_locale()
    braccio_vuoto_vietato()
    print("=" * 100)
    print("IL COLLAUDO DI `cs`: %d su %d   %s"
          % (OK[0], OK[1], "### TUTTI PASSATI" if OK[0] == OK[1] else "### CI SONO BUCHI"))
    print("=" * 100)
    return 0 if OK[0] == OK[1] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
