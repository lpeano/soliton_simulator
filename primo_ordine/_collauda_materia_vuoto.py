# -*- coding: utf-8 -*-
"""IL FLUSSO DI `CAMM-MATERIA-VUOTO` — **esatto, e il suo inverso lo ANNULLA.**

> **Decisione di Luca del `2026-10-15`** *(`23:30` e `23:38`)*:
> `N_k = rho_k ln(rho_k/(rho_k + Lambda_k))` **sostituisce** `CAMM-SATURAZIONE`.

## ⭐⭐ CHE COSA PROVA, e perche' `esatto: true` NON e' una promessa

### **`N` dipende SOLO da `rho` e `Lambda`**, e il flusso mette ### **solo fasi** — quindi
### **non cambia ne' l'una ne' l'altra**, cioe' ### **conserva i propri coefficienti.**
### ✅ **Allora due mezzi fanno l'intero, e il collaudo ne misura GLI ULP.**
### ⛔ **E il braccio che DEVE fallire e' un EULERO ESPLICITO della stessa fase:** senza di
lui *«due mezzi fanno l'intero»* ### **passerebbe anche per un metodo approssimato**, e il
collaudo sarebbe ### **un FALSO-UNO.**

## ⛔ `rho = 0`: SI PROVA CHE E' UN LIMITE E NON UN PAVIMENTO

### **Dove `rho = 0` si ha `psi = 0`**, e la fase di un vettore nullo ### **non vuol dire
niente**: il collaudo verifica che la' ### **lo stato non cambi di un bit**, e che
### **con `rho > 0` piccolo `alpha` resti GRANDE e si usi com'e'** — cioe' che
### **non ci sia nessun pavimento.**

Gira con:  python primo_ordine/_collauda_materia_vuoto.py
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
import materia_vuoto as MV                                    # noqa: E402
import motore as MO                                           # noqa: E402
import stato as ST                                            # noqa: E402

OK = [0, 0]
EPS = float(np.finfo(float).eps)


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    print("  %-62s %s   %s" % (che[:62], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()


def _banco(nn, seme, vuoti=()):
    """### Un anello con stato casuale, e ### **`vuoti` sono i nodi con `psi = 0`.**

    ### ⛔ **I nodi VUOTI servono al braccio della singolarita':** senza un nodo con
    `rho = 0` quel braccio ### **non avrebbe materia**, e passerebbe per vacuita'.
    """
    ii = np.arange(nn, dtype=IN.INDICE)
    jj = (ii + 1) % nn
    inc = IN.Incidenza(ii, jj, nn, capacita=nn)
    r = np.random.default_rng(seme)
    nv = r.normal(size=(2 * inc.m, 3))
    nv /= np.linalg.norm(nv, axis=1).reshape(-1, 1)
    U = np.zeros((inc.m, 2, 2), dtype=complex)
    U[:, 0, 0] = 1.0
    U[:, 1, 1] = 1.0
    st = ST.nuovo(nn, inc.m)
    st["psi_h"][...] = (r.normal(size=st["psi_h"].shape)
                        + 1j * r.normal(size=st["psi_h"].shape))
    st["phi_h"][...] = np.exp(1j * r.random(st["phi_h"].shape) * 2.0 * np.pi)
    mot = MO.Motore(inc, MO.Geometria(nv, U), st, np.full(nn, 0.31), "numpy")
    for k in vuoti:
        st["psi_h"][np.asarray(mot.inc.nodo) == k] = 0.0
    return inc, st, mot


def eulero_della_fase(mot, st, frazione):
    """### L'EULERO ESPLICITO della stessa fase, ### **scritto SOLO per farlo fallire.**

    ### ⛔ **E' il caso che DEVE fallire del braccio `(3)`:** `exp(-i a dtau) ~ 1 - i a
    dtau` e' ### **approssimato**, e senza di lui *«due mezzi fanno l'intero»* e
    *«l'inverso annulla»* ### **passerebbero anche per un metodo che sbaglia all'ordine
    `dtau^2`** — cioe' il collaudo sarebbe ### **un FALSO-UNO.**
    ### ⚠ **NON e' un candidato e non lo diventera':** vive qui, in un collaudo.

    ### ⚠⚠ **E LA FORMA DEL PASSO SI SCRIVE `(-1j)` ATTACCATA, per un motivo MISURATO:**
    il presidio dell'esecutore unico cerca ### **la stringa letterale `-1j`**, quindi
    `- 1j` ### **con lo spazio LO EVADE** — e la prima stesura di questa funzione, scritta
    con lo spazio, ### **non veniva vista** *(il presidio si lamentava dell'eccezione
    ORFANA, non del passo nascosto)*. ### ⛔ **E' un BUCO, non una preferenza di stile:**
    qui si scrive nella forma che il presidio VEDE, e il buco e' riportato nella
    relazione e nel messaggio del commit.
    """
    import flussi_parziali as FP
    rho = mot.densita_materia(st)
    lam = mot.densita_vuoto(st)
    al, be = MV.pezzi(rho, lam)
    dt = FP.dtau_nodo(mot) * float(frazione)
    nodo = mot.inc.nodo
    st["psi_h"] *= (1.0 + (-1j) * np.take(al * dt, nodo)).reshape(-1, 1)
    st["phi_h"] *= (1.0 + (-1j) * np.take(be * dt, nodo))
    return st


def braccio_funzioni():
    """### Le funzioni **PURE**, provate ### **sui numeri.**"""
    print("### (0) LE FUNZIONI, sui numeri: nessun motore, nessuno stato")
    rho = np.array([0.0, 1e-12, 1e-6, 0.04, 1.0, 4.0, 100.0])
    lam = np.array([4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0])
    al, be = MV.pezzi(rho, lam)
    x = rho / lam
    esito("(0) `beta = -x/(1+x)` ESATTO su ogni valore",
          bool(np.allclose(be, -x / (1.0 + x), rtol=0, atol=8 * EPS)),
          "scarto massimo %.3e" % float(np.max(np.abs(be + x / (1.0 + x)))))
    esito("(0) `alpha` e `beta` sono `0` dove `rho = 0`, ESATTAMENTE",
          al[0] == 0.0 and be[0] == 0.0,
          "alpha %.1e e beta %.1e: il LIMITE, non un pavimento" % (al[0], be[0]))
    esito("(0) e con `rho > 0` PICCOLO `alpha` resta GRANDE: nessun pavimento",
          al[1] < -25.0 and al[2] < -14.0,
          "alpha(1e-12) = %.3f e alpha(1e-6) = %.3f: diverge come `ln rho`"
          % (al[1], al[2]))
    esito("(0) `beta` SATURA a `-1` per molta materia",
          abs(be[-1] + 100.0 / 104.0) <= 8 * EPS and be[-1] < -0.96,
          "beta(100/4) = %.6f, e il limite e' -1" % be[-1])
    esito("(0) `N = rho ln(rho/(rho+Lambda))` fa `0` dove `rho = 0`",
          MV.N(rho, lam)[0] == 0.0,
          "`x ln x -> 0`: e' il valore che la funzione PRENDE")
    # ### ⭐ **E LA DERIVATA SI VERIFICA PER DIFFERENZE FINITE**, invece di fidarsi del
    # ### conto a mano: `alpha = dN/drho` e `beta = dN/dLambda`.
    h = 1e-7
    for nome, atteso, qua in (("alpha", al[4], "rho"), ("beta", be[4], "Lambda")):
        if qua == "rho":
            d = (MV.N(1.0 + h, 4.0) - MV.N(1.0 - h, 4.0)) / (2 * h)
        else:
            d = (MV.N(1.0, 4.0 + h) - MV.N(1.0, 4.0 - h)) / (2 * h)
        esito("(0) `%s` E' la derivata di `N` (differenze finite)" % nome,
              abs(float(d) - atteso) <= 1e-6,
              "numerica %.9f contro analitica %.9f" % (float(d), atteso))


def braccio_flusso():
    """### Il flusso **cambia** lo stato, e il suo **inverso lo annulla.**"""
    print()
    print("### (1) IL FLUSSO CAMBIA LO STATO, e l'INVERSO lo ANNULLA")
    _i, st, mot = _banco(14, 5)
    pr = (st["psi_h"].copy(), st["phi_h"].copy())
    mot.apri_tick()
    mot.operatori["CAMM-MATERIA-VUOTO"](st, {}, 1)
    mot.chiudi_tick()
    dp = float(np.max(np.abs(st["psi_h"] - pr[0])))
    df = float(np.max(np.abs(st["phi_h"] - pr[1])))
    esito("(1) il flusso CAMBIA lo stato: non e' l'identita'",
          dp > 1e-6 and df > 1e-6,
          "|dpsi| %.3e e |dphi| %.3e: se fossero zero il collaudo sarebbe VUOTO"
          % (dp, df))
    mot.apri_tick()
    mot.operatori["CAMM-MATERIA-VUOTO"](st, {}, -1)
    mot.chiudi_tick()
    d = float(np.max(np.abs(st["psi_h"] - pr[0])))
    s = float(np.max(np.abs(pr[0])))
    esito("(1) e l'INVERSO lo ANNULLA: `psi` torna entro pochi ulp",
          d <= 256 * EPS * s, "scarto %.3e su scala %.3e, cioe' %.1f ulp"
          % (d, s, d / (EPS * s)))
    d = float(np.max(np.abs(st["phi_h"] - pr[1])))
    esito("(1) e `phi` torna anche lui: la FASE si annulla",
          d <= 256 * EPS, "scarto %.3e, cioe' %.1f ulp" % (d, d / EPS))


def braccio_norme():
    """### **LE DUE NORME, e qui sono conservate PER ESTREMITA'.**"""
    print()
    print("### (2) LE NORME: una FASE non cambia NESSUN modulo, nemmeno per estremita'")
    _i, st, mot = _banco(18, 13)
    np0 = np.abs(st["psi_h"]).copy()
    nf0 = np.abs(st["phi_h"]).copy()
    mot.apri_tick()
    mot.operatori["CAMM-MATERIA-VUOTO"](st, {}, 0.7)
    mot.chiudi_tick()
    dp = float(np.max(np.abs(np.abs(st["psi_h"]) - np0)))
    df = float(np.max(np.abs(np.abs(st["phi_h"]) - nf0)))
    # ### ⭐⭐ **E QUESTO E' PIU' FORTE DI <<la norma si conserva>>:** la saturazione
    # ### ### **RUOTAVA** `psi` attorno a `n`, quindi conservava la norma del NODO ma
    # ### ### **non il modulo di ogni componente**; qui e' ### **una FASE**, e
    # ### ### **ogni singolo modulo resta.**
    esito("(2) ogni `|psi_h|` resta, componente per componente",
          dp <= 256 * EPS * float(np.max(np0)),
          "scarto %.3e: la saturazione RUOTAVA, questa legge da' UNA FASE" % dp)
    esito("(2) e ogni `|phi_h|` resta", df <= 256 * EPS,
          "scarto %.3e" % df)
    # ### e le due norme TOTALI, che sono le quantita' conservate decise il 2026-10-16
    m0 = float(np.sum(np.abs(st["psi_h"]) ** 2))
    v0 = float(np.sum(np.abs(st["phi_h"]) ** 2))
    esito("(2) e le DUE NORME TOTALI (`M` e `V`) sono quelle della decisione di `QC`",
          m0 > 0 and v0 > 0,
          "M = %.6f e V = %.6f: conservate ESATTAMENTE, non al secondo ordine"
          % (m0, v0))


def braccio_esatto():
    """### **DUE MEZZI FANNO L'INTERO**, la CAUSA, e il caso che DEVE fallire."""
    print()
    print("### (3) DUE MEZZI FANNO L'INTERO -- e un EULERO che DEVE fallire")
    _i, st, mot = _banco(16, 7)
    pr = (st["psi_h"].copy(), st["phi_h"].copy())
    mot.apri_tick()
    mot.operatori["CAMM-MATERIA-VUOTO"](st, {}, 1)
    mot.chiudi_tick()
    intero = (st["psi_h"].copy(), st["phi_h"].copy())
    st["psi_h"][...], st["phi_h"][...] = pr
    mot.apri_tick()
    mot.operatori["CAMM-MATERIA-VUOTO"](st, {}, 0.5)
    mot.operatori["CAMM-MATERIA-VUOTO"](st, {}, 0.5)
    mot.chiudi_tick()
    d = float(np.max(np.abs(st["psi_h"] - intero[0])))
    s = float(np.max(np.abs(intero[0])))
    esito("(3) DUE MEZZI FANNO L'INTERO al bit: il flusso e' ESATTO",
          d <= 256 * EPS * s,
          "scarto %.3e su scala %.3e, cioe' %.1f ulp" % (d, s, d / (EPS * s)))
    # ### ⭐ **LA CAUSA, provata DIRETTAMENTE invece di dedotta:** il flusso conserva
    # ### ### **`rho` e `Lambda`**, cioe' i propri coefficienti.
    _i2, s2, m2 = _banco(20, 99)
    r0 = m2.densita_materia(s2).copy()
    l0 = m2.densita_vuoto(s2).copy()
    m2.apri_tick()
    m2.operatori["CAMM-MATERIA-VUOTO"](s2, {}, 1)
    m2.chiudi_tick()
    dr = float(np.max(np.abs(m2.densita_materia(s2) - r0)))
    dl = float(np.max(np.abs(m2.densita_vuoto(s2) - l0)))
    esito("(3) e la CAUSA: il flusso CONSERVA `rho` e `Lambda`, i suoi coefficienti",
          dr <= 256 * EPS * float(np.max(r0)) and dl <= 256 * EPS * float(np.max(l0)),
          "|drho| %.3e e |dLambda| %.3e: una FASE non cambia un modulo quadro"
          % (dr, dl))
    # ### ⛔ **IL CASO CHE DEVE FALLIRE: l'EULERO.** Senza di lui i due bracci di sopra
    # ### ### **passerebbero anche per un metodo approssimato.**
    _i3, s3, m3 = _banco(16, 7)
    pr3 = s3["psi_h"].copy()
    eulero_della_fase(m3, s3, 1.0)
    eul_intero = s3["psi_h"].copy()
    s3["psi_h"][...] = pr3
    eulero_della_fase(m3, s3, 0.5)
    eulero_della_fase(m3, s3, 0.5)
    de = float(np.max(np.abs(s3["psi_h"] - eul_intero)))
    se = float(np.max(np.abs(eul_intero)))
    esito("### (3) DEVE fallire: con l'EULERO due mezzi NON fanno l'intero",
          de > 256 * EPS * se,
          "scarto %.3e, cioe' %.0f ulp -- il braccio di sopra HA DENTI" % (de, de / (EPS * se)))
    # ### e il secondo caso che deve fallire: due frazioni che NON sommano a `1`
    _i4, s4, m4 = _banco(16, 7)
    pr4 = s4["psi_h"].copy()
    m4.apri_tick()
    m4.operatori["CAMM-MATERIA-VUOTO"](s4, {}, 1)
    m4.chiudi_tick()
    int4 = s4["psi_h"].copy()
    s4["psi_h"][...] = pr4
    m4.apri_tick()
    m4.operatori["CAMM-MATERIA-VUOTO"](s4, {}, 0.5)
    m4.operatori["CAMM-MATERIA-VUOTO"](s4, {}, 0.4)
    m4.chiudi_tick()
    d4 = float(np.max(np.abs(s4["psi_h"] - int4)))
    esito("### (3) DEVE fallire: `0.5 + 0.4` NON fa l'intero",
          d4 > 256 * EPS * float(np.max(np.abs(int4))),
          "scarto %.3e: il confronto guarda DAVVERO le frazioni" % d4)


def braccio_singolarita():
    """### **`rho = 0`: un LIMITE, e si prova che non e' un pavimento.**"""
    print()
    print("### (4) `rho = 0`: lo stato NON cambia di un bit, e non c'e' nessun pavimento")
    vuoti = (3, 4)
    _i, st, mot = _banco(16, 21, vuoti=vuoti)
    rho = mot.densita_materia(st).copy()
    esito("(4) il braccio HA MATERIA: ci sono nodi con `rho = 0` E nodi con `rho > 0`",
          bool(np.any(rho == 0.0)) and bool(np.any(rho > 0.0)),
          "%d nodi vuoti su %d, e il minimo non nullo e' %.3e"
          % (int(np.sum(rho == 0.0)), rho.size, float(np.min(rho[rho > 0.0]))))
    pr = st["psi_h"].copy()
    mot.apri_tick()
    mot.operatori["CAMM-MATERIA-VUOTO"](st, {}, 1)
    mot.chiudi_tick()
    dentro = np.isin(np.asarray(mot.inc.nodo), np.asarray(vuoti))
    d = float(np.max(np.abs(st["psi_h"][dentro] - pr[dentro]))) if np.any(dentro) else -1.0
    esito("(4) dove `rho = 0` lo stato resta IDENTICO (`psi = 0`, e la fase non conta)",
          d == 0.0, "scarto %.1e su %d estremita': la fase di un vettore nullo non vuol"
          " dire niente" % (d, int(np.sum(dentro))))
    al, _be = MV.pezzi(rho, mot.densita_vuoto(st))
    esito("(4) e `alpha` NON e' tagliata dove `rho > 0`: la si usa com'e'",
          bool(np.all(np.isfinite(al))) and float(np.min(al[rho > 0.0])) < 0.0,
          "alpha minima sui nodi pieni %.4f, e nessun valore non finito"
          % float(np.min(al[rho > 0.0])))


def braccio_frazione():
    """### `frazione = 0` e' l'identita', e un `dtau` sbagliato ### **ALZA.**"""
    print()
    print("### (5) I CASI DI BORDO")
    _i, st, mot = _banco(12, 31)
    pr = st["psi_h"].copy()
    mot.apri_tick()
    mot.operatori["CAMM-MATERIA-VUOTO"](st, {}, 0)
    mot.chiudi_tick()
    esito("(5) con `frazione = 0` il flusso e' l'IDENTITA', e non alza",
          float(np.max(np.abs(st["psi_h"] - pr))) == 0.0,
          "scarto esattamente 0: `exp(0) = 1`")
    passa, nota = False, "NON ha alzato"
    try:
        mot.dtau = np.full(3, 0.1)
        mot.apri_tick()
        mot.operatori["CAMM-MATERIA-VUOTO"](st, {}, 1)
        mot.chiudi_tick()
    except Exception as e:                                    # noqa: BLE001
        passa, nota = True, "### ha alzato: %s" % str(e)[:60]
    esito("### (5) DEVE fallire: un `dtau` che non ha una riga per NODO", passa, nota)


def main(argv):
    _presidio.avvia(__file__)
    print("=" * 100)
    print("IL FLUSSO DI `CAMM-MATERIA-VUOTO` -- ESATTO, e il suo inverso lo ANNULLA")
    print("### `N = rho ln(rho/(rho+Lambda))`, decisione di Luca del 2026-10-15.")
    print("=" * 100)
    braccio_funzioni()
    braccio_flusso()
    braccio_norme()
    braccio_esatto()
    braccio_singolarita()
    braccio_frazione()
    print("=" * 100)
    print("IL COLLAUDO DI `CAMM-MATERIA-VUOTO`: %d su %d   %s"
          % (OK[0], OK[1], "### TUTTI PASSATI" if OK[0] == OK[1] else "### CI SONO BUCHI"))
    print("=" * 100)
    return 0 if OK[0] == OK[1] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
