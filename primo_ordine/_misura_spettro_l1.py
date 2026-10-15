# -*- coding: utf-8 -*-
r"""**LO SPETTRO DEL PASSO LINEARE PALINDROMO — una MISURA, nessuna decisione.**

> **Punto 3 del mandato di Luca del 2026-10-15** *(12:44)*: *«Su un toro piccolo, col passo
> palindromo, a `theta = pi`, `0.5 pi`, `0.25 pi` (`dtau` uniforme): le fasi proprie `eps`
> del passo lineare sono appaiate `eps <-> -eps`? ci sono degeneranze doppie (alla Kramers,
> perche' `C^2 = -1` su `psi`)? `C W C^-1 = W^-1` vale al bit o all'ulp?»*
>
> ### ⛔ **NESSUNA CONCLUSIONE DI FISICA: la decide Luca.** Qui ci sono **solo numeri**.

## ⭐ CHE COS'E' `W` QUI, E CHE COSA NON E'

### **`W` e' la PARTE LINEARE del passo**: *moneta di spin, Grover, spostamento* — e
### ⛔ **SENZA LA SATURAZIONE**, che e' il solo pezzo non lineare *(dipende da `h` e da
`Lambda`, cioe' **dallo stato**)*.
### 📌 **E si costruisce APPLICANDO il passo ai vettori di base**, non scrivendo una
matrice a mano: ### **cosi' `W` e' per costruzione l'operatore che il motore applica
davvero**, e non la mia idea di che cosa applichi.

### ⛔ **E `bande.py` RESTA CONGELATO:** questo e' uno script **nuovo di `L1`**, e **non
importa** `bande.py`, `segno.py` ne' le loro misure.

## ⭐⭐ UNA DERIVAZIONE SCRITTA PRIMA DI MISURARE — **e dice che cosa aspettarsi**

### Se `C W C^-1 = W^-1` e `W v = e^{i eps} v`, allora *(e `C` e' **antiunitaria**, quindi
coniuga gli scalari)*:

```
W^-1 (C v) = C W C^-1 C v = C (W v) = C (e^{i eps} v) = e^{-i eps} (C v)
      ==>   W (C v) = e^{+i eps} (C v)
```

### ⭐ **Quindi `C v` e' autovettore con LO STESSO autovalore**, e siccome `C^2 = -1` su
`psi` ### **`C v` e' indipendente da `v`**: ### ✅ **ogni autovalore e' ALMENO DOPPIO.**
### **E' la degenerazione di Kramers, e qui e' una CONSEGUENZA, non un'ipotesi.**

### ⚠⚠ **E LA STESSA DERIVAZIONE DICE CHE `eps <-> -eps` NON SEGUE.** Un'antiunitaria da'
**la degenerazione**; un appaiamento `eps <-> -eps` vorrebbe un'**antisimmetria UNITARIA**
*(del tipo `X W X^-1 = W^-1` con `X` lineare)*, che ### **nessuno ha mostrato esistere.**
### 📌 **Quindi la risposta attesa e': degeneranze DOPPIE SI', appaiamento `eps <-> -eps`
NON NECESSARIAMENTE.** ### ⛔ **E lo scrivo PRIMA per non poter chiamare <<previsto>> cio'
che la misura dira'.**

## ⛔ IL CASO CHE DEVE FALLIRE

### **L'ordine NON palindromo** *(quello di prima del `2026-10-15`)*: la' `C W C^-1 = W^-1`
### **deve ROMPERSI**, perche' `C W C^-1` e' il prodotto degli `Op^-1` **nello stesso
ordine** mentre `W^-1` lo e' **in ordine rovescio.**
### ⚠ **Senza questo braccio il verdetto sarebbe un FALSO-UNO:** una `C` che passa non
proverebbe che e' **il palindromo** a farla passare.

Gira con:  python primo_ordine/_misura_spettro_l1.py
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
sys.path.insert(0, os.path.join(os.path.dirname(_QUI), "csv"))

OK = [0, 0]
# ### ⛔ **LA CONFIGURAZIONE INTERA, DICHIARATA E STAMPATA**
LATI = (3, 3)
SEME = 7
DTAU = (1.0, 0.5, 0.25)
EPS = 0.5
VUOTO_MODULO = 2.0
SY = np.array([[0.0, -1.0j], [1.0j, 0.0]], dtype=complex)
# ### ⛔ **L-ORDINE DI PRIMA, per il CASO CHE DEVE FALLIRE.** ### **Non e- una seconda
# ### tabella:** e- un dato storico, e serve solo a questo braccio.
ORDINE_VECCHIO = (("CAMM-SATURAZIONE", 0.5), ("CAMM-MONETA-SPIN", 1),
                  ("CAMM-GROVER", 1), ("CAMM-SPOSTAMENTO", 1),
                  ("CAMM-GROVER-VUOTO", 1), ("CAMM-SPOSTAMENTO-VUOTO", 1),
                  ("CAMM-SATURAZIONE", 0.5))


def accoppia(a, b):
    """### `max` distanza di un accoppiamento GOLOSO fra due multinsiemi complessi.

    ### ⛔ **E SI FA SUL PIANO COMPLESSO, NON SUGLI ANGOLI, ed e' la correzione di un mio
    difetto di misura:** confrontare angoli ordinati ### **spezza una coppia vicina a
    `+-pi`** — la' `-(-pi) = +pi` e' **lo stesso autovalore**, ma due angoli lontani `2pi`.
    ### ⚠ **Con gli angoli avevo misurato <<molteplicita' 1>> a `dtau = 1`, che
    CONTRADDICEVA la derivazione di Kramers: era l'avvolgimento, non la fisica.**
    """
    b = list(b)
    peggio = 0.0
    for x in a:
        k = min(range(len(b)), key=lambda j: abs(b[j] - x))
        d = abs(b[k] - x)
        if d > peggio:
            peggio = d
        b.pop(k)
    return peggio


def gruppi_di(lam, toll):
    """### Le molteplicita', raggruppando ### **per AUTOVALORE** e non per angolo."""
    n = len(lam)
    usato = np.zeros(n, dtype=bool)
    fuori = []
    for i in range(n):
        if usato[i]:
            continue
        vv = [j for j in range(n) if not usato[j] and abs(lam[j] - lam[i]) <= toll]
        for j in vv:
            usato[j] = True
        fuori.append(len(vv))
    return fuori


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    print("  %-58s %s   %s" % (che[:58], "PASSA" if passa else "### FALLISCE", nota))


def scena(dtau):
    """### Il **TORO** `LATI`, ### **grado `2 d` e NON `2`.**

    ### ⛔ **Il toro, e non l'anello:** un anello ha grado `2`, e li' il Grover e' quasi
    una permutazione — ### **una proprieta' dello spettro misurata a grado `2` non dice
    niente del grado `4`.** ### ✅ **E non ha bordi**, che e' cio' che <<toro>> compra.
    ### 📌 **Il costruttore e' `corrente.toro`, usato IN SOLA LETTURA.**
    """
    import corrente as CO
    import incidenza as IN
    import motore as MO
    import stato as ST
    ii, jj, nn = CO.toro(LATI)
    inc = IN.Incidenza(np.asarray(ii, dtype=IN.INDICE),
                       np.asarray(jj, dtype=IN.INDICE), nn, capacita=len(ii))
    r = np.random.default_rng(SEME)
    nv = r.normal(size=(2 * inc.m, 3))
    nv /= np.linalg.norm(nv, axis=1).reshape(-1, 1)
    U = np.zeros((inc.m, 2, 2), dtype=complex)
    for a in range(inc.m):
        X = r.normal(size=(2, 2)) + 1j * r.normal(size=(2, 2))
        Qm, _ = np.linalg.qr(X)
        # ### ⛔ **`SU(2)`, e NON e- un abbellimento:** la `C` antilineare chiede
        # ### `sigma_y U^* sigma_y^-1 = U`, che vale ### **se e solo se `det U = 1`.**
        U[a] = Qm / np.sqrt(np.linalg.det(Qm))
    st = ST.nuovo(nn, inc.m)
    st["psi_h"][...] = (r.normal(size=st["psi_h"].shape)
                        + 1j * r.normal(size=st["psi_h"].shape))
    st["phi_h"][...] = (float(VUOTO_MODULO)
                        * np.exp(1j * r.random(st["phi_h"].shape) * 2.0 * np.pi))
    mot = MO.Motore(inc, MO.Geometria(nv, U), st, np.full(nn, dtau), "numpy")
    return inc, mot, st


def ordine_lineare(ordine):
    """### L'ordine dato **senza la saturazione**: ### **e' la PARTE LINEARE.**"""
    return [(idl, fr) for idl, fr in ordine if idl != "CAMM-SATURAZIONE"]


def ordine_tabella():
    """### L'ordine della **TABELLA**, letto da `composizione.py`."""
    import composizione as CM
    return [(idl, fr) for idl, fr, _t in CM.ORDINE]


def passo(mot, st, ordine):
    """### Applica `ordine` **una volta**, ### **in posto.**"""
    import deriva as DV
    mot.apri_tick()
    for idl, fr in ordine:
        nome, vuole_par = DV.OPERATORE[idl]
        mot.operatori[nome](st, {"eps": EPS} if vuole_par else {}, fr)
    mot.chiudi_tick()


def matrice(mot, st, ordine):
    """### `W` **sulla parte `psi`**, costruita applicando il passo ai vettori di base.

    ### ⚠ **`phi` si azzera**, e si puo': i pezzi del vuoto ### **non toccano `psi`**,
    e la saturazione — l'unico pezzo che li lega — ### **non e' in `ordine`.**
    """
    forma = st["psi_h"].shape
    d = forma[0] * forma[1]
    W = np.zeros((d, d), dtype=complex)
    for k in range(d):
        st["psi_h"].fill(0)
        st["phi_h"].fill(0)
        st["psi_h"].reshape(-1)[k] = 1.0
        passo(mot, st, ordine)
        W[:, k] = st["psi_h"].reshape(-1)
    return W


def c_su_psi(v, forma):
    """### `C psi = i sigma_y psi^*` ### **per estremita'.**"""
    p = np.conj(v.reshape(forma))
    return np.einsum("ij,aj->ai", 1.0j * SY, p).reshape(-1)


def c_su_U(U):
    """### `C U = sigma_y U^* sigma_y^-1` — ### **la correzione di Luca del 2026-10-13.**"""
    return np.einsum("ij,ajk,kl->ail", SY, np.conj(U), SY)


def prove(dtau):
    """### Le tre domande, ### **a un `dtau` dato.**"""
    eps_m = float(np.finfo(float).eps)
    inc, mot, st = scena(dtau)
    forma = st["psi_h"].shape
    ordine = ordine_lineare(ordine_tabella())
    W = matrice(mot, st, ordine)
    d = W.shape[0]
    print("-" * 96)
    print("  dtau = %.4f -> theta = %.4f pi   |   W e' %dx%d, %d pezzi lineari"
          % (dtau, dtau, d, d, len(ordine)))
    # ------------------------------------------------- (0) W e' UNITARIA?
    sb = float(np.max(np.abs(np.conj(W.T).dot(W) - np.eye(d))))
    esito("(0) `W` e' UNITARIA (senza questo, le fasi non sono fasi)",
          sb <= 1024 * eps_m, "scarto %.3e, cioe' %.0f ulp" % (sb, sb / eps_m))
    # ------------------------------------------------- le fasi proprie
    autov = np.linalg.eigvals(W)
    e = np.sort(np.angle(autov))
    toll = 1e-8
    # ------------------------------------------------- (1) eps <-> -eps?
    # ### ⭐ **`eps -> -eps` e- `lambda -> coniugato(lambda)`**, e il confronto si fa
    # ### ### **sul piano complesso** per non spezzare le coppie vicine a `+-pi`.
    dist = accoppia(autov, np.conj(autov))
    print("    le fasi: min %.6f  max %.6f  (su pi: %.4f .. %.4f)"
          % (e[0], e[-1], e[0] / np.pi, e[-1] / np.pi))
    print("    ### (1) APPAIAMENTO `eps <-> -eps`: max distanza fra lo spettro e il suo"
          " opposto = %.6e" % dist)
    # ------------------------------------------------- (2) degeneranze doppie?
    gruppi = gruppi_di(autov, toll)
    molt = {}
    for g in gruppi:
        molt[g] = molt.get(g, 0) + 1
    esito("(2) ogni autovalore e' ALMENO DOPPIO (Kramers, `C^2 = -1`)",
          min(gruppi) >= 2,
          "molteplicita': %s su %d gruppi (tolleranza %.0e)"
          % (molt, len(gruppi), toll))
    # ------------------------------------------------- (3) C W C^-1 = W^-1?
    scarto = _prova_c(mot, st, forma, ordine)
    sc = 1.0
    esito("(3) `C W C^-1 = W^-1` (inversione del tempo del PASSO INTERO)",
          scarto <= 1024 * eps_m * sc,
          "scarto %.3e, cioe' %.0f ulp" % (scarto, scarto / eps_m))
    # ------------------------------------------------- il caso che DEVE fallire
    vecchio = ordine_lineare(ORDINE_VECCHIO)
    inc2, mot2, st2 = scena(dtau)
    rotto = _prova_c(mot2, st2, forma, vecchio)
    esito("### DEVE ROMPERSI: lo stesso con l'ordine NON palindromo",
          rotto > 1024 * eps_m,
          "scarto %.3e: ### senza questo il braccio (3) sarebbe un FALSO-UNO" % rotto)
    # ============================================= LA DIAGNOSI: CHI ROMPE LA (3)?
    # ### ⛔ **Il braccio `(3)` FALLISCE anche col palindromo**, e la derivazione dice
    # ### ### **chi**: ### la MONETA DI SPIN. ### ⭐ **Il conto, in due righe:**
    # ### `C exp(-i a sigma.n) C^-1 = (i sigma_y) exp(+i a (sigma.n)^*) (i sigma_y)^-1`,
    # ### e siccome `sigma_y (sigma.n)^* sigma_y^-1 = -(sigma.n)` *(con `n` reale)*, il
    # ### risultato e- ### **`exp(-i a sigma.n)`, cioe- LA STESSA COSA** -- ### **non la
    # ### sua inversa.** ### ⚠ **E la moneta NON c-era nel test dei quattro pezzi del
    # ### 2026-10-15**: ### **non l-avevo mai misurata.**
    print("    ### LA DIAGNOSI DEL BRACCIO (3): chi non si rovescia?")
    inc3, mot3, st3 = scena(dtau)
    m_inv = _prova_c(mot3, st3, forma, [("CAMM-MONETA-SPIN", 0.5)])
    inc4, mot4, st4 = scena(dtau)
    m_ug = _prova_c_uguale(mot4, st4, forma, [("CAMM-MONETA-SPIN", 0.5)])
    esito("(4) la MONETA sotto `C` resta SE STESSA, non la sua inversa",
          m_ug <= 1024 * eps_m and m_inv > 1024 * eps_m,
          "`C M C^-1 = M` da' %.3e, `= M^-1` da' %.3e" % (m_ug, m_inv))
    senza = [x for x in ordine if x[0] != "CAMM-MONETA-SPIN"]
    inc5, mot5, st5 = scena(dtau)
    s_senza = _prova_c(mot5, st5, forma, senza)
    esito("(5) e SENZA la moneta `C W C^-1 = W^-1` TORNA ESATTA",
          s_senza <= 1024 * eps_m,
          "scarto %.3e su %d pezzi, cioe' %.0f ulp"
          % (s_senza, len(senza), s_senza / eps_m))
    W2 = matrice(mot5, st5, senza)
    l2 = np.linalg.eigvals(W2)
    g2 = gruppi_di(l2, toll)
    esito("(6) e SENZA la moneta la degenerazione di Kramers C'E'",
          min(g2) >= 2, "molteplicita' minima %d su %d gruppi" % (min(g2), len(g2)))
    d2 = accoppia(l2, np.conj(l2))
    print("    ### (7) e SENZA la moneta l'appaiamento `eps <-> -eps` vale %.6e" % d2)
    return dist, min(gruppi), scarto, rotto, m_ug, s_senza, min(g2), d2


def _prova_c_uguale(mot, st, forma, ordine):
    """### `max |C W C psi - psi|`: ### **vale se `C W C^-1 = W`**, non `W^-1`.

    ### ⭐ **La differenza col test di sopra e' SOLO il verso del confronto:** qui si
    applica `C`, il passo, `C`, e **l'INVERSO non si applica** — si confronta col passo
    fatto una volta sola. ### **E il segno di `C^2 = -1` resta.**
    """
    r = np.random.default_rng(SEME + 1)
    v = (r.normal(size=forma) + 1j * r.normal(size=forma))
    # ### il passo UNA volta, su `v`
    st["psi_h"][...] = v
    st["phi_h"].fill(0)
    passo(mot, st, ordine)
    diretto = st["psi_h"].copy()
    # ### e `C`, il passo, `C` -- che e- `C W C^-1` a meno del segno di `C^2`
    st["psi_h"][...] = v
    st["phi_h"].fill(0)
    st["psi_h"][...] = c_su_psi(st["psi_h"].reshape(-1), forma).reshape(forma)
    mot.geo.U[...] = c_su_U(mot.geo.U.copy())
    passo(mot, st, ordine)
    st["psi_h"][...] = c_su_psi(st["psi_h"].reshape(-1), forma).reshape(forma)
    mot.geo.U[...] = c_su_U(mot.geo.U.copy())
    sc = float(np.max(np.abs(diretto)))
    return float(np.max(np.abs(st["psi_h"] + diretto))) / sc


def _prova_c(mot, st, forma, ordine):
    """### `max |W C W C psi + psi|`, ### **e il `+` e' `C^2 = -1`.**

    ### ⭐ **La prova non costruisce `C` come matrice:** applica `C`, il passo, `C`, il
    passo, e confronta con ### **`-psi`** — perche' `C^2 = -1` su `psi`, che e' un fatto
    derivato *(`sigma_y^* = -sigma_y`)* e **non una convenzione.**
    ### ⚠ **E `C` tocca ANCHE `U`**, che e' la parte che avevo dimenticato una volta.
    """
    r = np.random.default_rng(SEME + 1)
    v = (r.normal(size=forma) + 1j * r.normal(size=forma))
    st["psi_h"][...] = v
    st["phi_h"].fill(0)
    for _ in range(2):
        st["psi_h"][...] = c_su_psi(st["psi_h"].reshape(-1), forma).reshape(forma)
        mot.geo.U[...] = c_su_U(mot.geo.U.copy())
        passo(mot, st, ordine)
    sc = float(np.max(np.abs(v)))
    return float(np.max(np.abs(st["psi_h"] + v))) / sc


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    print("=" * 96)
    print("LO SPETTRO DEL PASSO LINEARE PALINDROMO -- una MISURA, nessuna decisione")
    print("=" * 96)
    print("  LA CONFIGURAZIONE: toro %s   seme = %d   dtau = %s   eps = %.1f"
          "   vuoto_modulo = %.1f   U in SU(2)"
          % (LATI, SEME, DTAU, EPS, VUOTO_MODULO))
    tab = []
    for dtau in DTAU:
        tab.append((dtau,) + prove(dtau))
    print("=" * 96)
    print("  LA TABELLA, in una riga per `dtau`. ### ATTENZIONE AL FATTORE 2: con l'ordine")
    print("  palindromo OGNI PEZZO sta a frazione 0.5, quindi un pezzo agisce a")
    print("  `theta = pi*dtau/2`, non a `pi*dtau`.")
    print("  %-8s %-14s %-7s %-12s %-12s %-12s %-12s %s"
          % ("dtau", "dist(e,-e)", "molt.", "C W C-1=W-1", "NON palind.",
             "moneta=se", "senza mon.", "molt./dist senza"))
    for dtau, dist, mm, sc, rotto, m_ug, s_senza, mm2, d2 in tab:
        print("  %-8.4f %-14.6e %-7d %-12.3e %-12.3e %-12.3e %-12.3e %d / %.3e"
              % (dtau, dist, mm, sc, rotto, m_ug, s_senza, mm2, d2))
    print("=" * 96)
    print("  %d su %d" % (OK[0], OK[1]))
    print("### ⛔ E NESSUNA CONCLUSIONE DI FISICA: i numeri sono questi, e la lettura")
    print("###   la decide Luca. Cio' che questo file NON dice e' se il modello DEVE")
    print("###   avere la C, la CT, o un'altra simmetria.")
    print("=" * 96)
    return 0 if OK[0] == OK[1] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
