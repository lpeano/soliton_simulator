# -*- coding: utf-8 -*-
r"""`M-B2` — **L'ERRORE DI CONSERVAZIONE DI `H_tot` CALA COME `dtau^2`?**

> **Criterio di uscita di `L1`, nelle parole di Luca:** *«con `dtau` uniforme
> `= dtau_rif/2^k` (`k = 1..4`), l'errore di conservazione dell'energia totale (strada
> `B`) cala di un **fattore 4** a ogni dimezzamento. Riporta la tabella dei rapporti.»*

## ⭐ CHE COS'E' `H_tot` DI STRADA `(B)`, E PERCHE' NON E' LA `E` DI PRIMA

### **Ogni strato del passo e' il flusso di un generatore LOCALE**, e `H_tot` e' la somma
dei valori medi di quei generatori — ### **uno per arco, uno per nodo, uno per
estremita'**:

```
H_tot = - pi  SOMMA_nodi ( <psi|psi>_k - |SOMMA_k psi|^2/d_k )      il Grover di psi
        - pi  SOMMA_archi ( <psi|psi>_a - 2 Re[psi_0^dagger U^dagger psi_1] )/2   il hop
        - pi  SOMMA_nodi ( ... )   - pi SOMMA_archi ( ... )         gli stessi su phi
        + eps SOMMA_estremita <psi_h| sigma.n_h |psi_h>             la moneta di spin
        + SOMMA_nodi Lambda_k G(h_k/Lambda_k)                       la saturazione
```

### ⛔ **E NON E' LA `E` DELLA DERIVA:** quella ha **raggio 1** *(usa `W`, cioe' guarda il
vicino)*, questa ha ### **raggio ZERO** — un arco, un nodo, un'estremita'.
### ⭐ **`omega = pi` NON E' UNA COSTANTE NUOVA:** e' il raccordo `B-4` con `dtau_rif = 1`.

## ⚠ IL PROTOCOLLO: **TEMPO TOTALE FISSO**, e il perche' decide la previsione

### ⛔ **A numero di tick FISSO l'errore globale andrebbe come `N dtau^3`**, cioe'
**fattore 8**; ### ✅ **a TEMPO TOTALE fisso** *(`N = T/dtau`, quindi `N` RADDOPPIA a ogni
dimezzamento)* **va come `T dtau^2`**, cioe' ### **fattore 4** — ed e' il fattore che il
criterio nomina. ### **Quindi il protocollo e' a tempo totale fisso**, e lo dico prima di
misurare.

### 📌 **E L'ERRORE E' L'ESCURSIONE, non `fine - inizio`:** `max_t |H(t) - H(0)|`.
### ⛔ **E' una lezione gia' pagata:** con una quantita' che oscilla, `fine - inizio` e'
**un campione casuale** e aveva fatto sembrare falsa una previsione vera.

## ⛔ IL PERIMETRO

### Usa `deriva.py` **IN SOLA LETTURA** *(`DV.scena`, `TK.tick`)*, che la scelta di
perimetro di Luca del `2026-10-15` ammette per i criteri di uscita di questo livello.

## 📌 E IL LIMITE A `Lambda == 0` NON E' UN PAVIMENTO

### `Lambda G(h/Lambda)` ### **tende a `h`** quando `Lambda -> 0`, perche' `Lambda arctan` va
a zero. ### ✅ **E' il VALORE CHE LA FUNZIONE PRENDE la'**, quindi `A11` e' rispettato:
### **un pavimento curerebbe dove non c'e' un errore, un limite E' la funzione.**

Gira con:  python primo_ordine/_misura_mb2.py
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
sys.path.insert(0, os.path.join(os.path.dirname(_QUI), "csv"))

import tick as TK                                             # noqa: E402

# ### ⛔ **LA CONFIGURAZIONE INTERA, DICHIARATA E STAMPATA**
TEMPO = 8.0
KAPPA = (1, 2, 3, 4)
# ### ⛔ **DUE PUNTI PIU- FINI, E SONO UN-ESTENSIONE, NON IL CRITERIO.** Il criterio
# ### di Luca e- `KAPPA`, ### **e resta intatto**: questi servono a rispondere a una
# ### domanda che i primi quattro ### **non possono** chiudere -- ### **la pendenza
# ### CONVERGE a `2`?** ### ⚠ **A `dtau = 0.5` i pezzi stanno a `theta = pi/2`, cioe-
# ### ### **lontano dal regime asintotico**: la- i termini di ordine superiore pesano,
# ### e un rapporto diverso da `4` ### **non dice che il metodo non e- di secondo
# ### ordine** -- dice che quel passo e- troppo grosso.
KAPPA_FINE = (4, 5, 6)
NN = 16
SEME = 7
NORMA = "locale"
VUOTO_MODULO = 2.0
SU2 = True
OMEGA = float(np.pi)


def _per_nodo(inc, v):
    """### Somma per nodo di un reale per estremita', ### **senza cicli Python.**"""
    fuori = np.zeros(inc.n, dtype=float)
    np.add.at(fuori, inc.nodo, v)
    return fuori


def h_tot(inc, mot, st, par):
    """### `H_tot`, ### **la somma dei generatori locali.**"""
    psi, phi = st["psi_h"], st["phi_h"]
    m = inc.m
    U = mot.geo.U
    # ------------------------------------------------- i due pezzi di NODO
    nrm_psi = _per_nodo(inc, np.abs(psi[:, 0]) ** 2 + np.abs(psi[:, 1]) ** 2)
    nrm_phi = _per_nodo(inc, np.abs(phi) ** 2)
    S_psi = np.zeros((inc.n, 2), dtype=complex)
    np.add.at(S_psi, inc.nodo, psi)
    S_phi = np.zeros(inc.n, dtype=complex)
    np.add.at(S_phi, inc.nodo, phi)
    d = inc.grado.astype(float)
    pu_psi = (np.abs(S_psi[:, 0]) ** 2 + np.abs(S_psi[:, 1]) ** 2) / d
    pu_phi = np.abs(S_phi) ** 2 / d
    nodo = -OMEGA * float(np.sum((nrm_psi - pu_psi) + (nrm_phi - pu_phi)))
    # ------------------------------------------------- i due pezzi di ARCO
    v = psi.reshape(m, 2, 2)
    p0, p1 = v[:, 0, :], v[:, 1, :]
    incro = np.einsum("ai,aji,aj->a", np.conj(p0), np.conj(U), p1)
    nrm_a = (np.abs(p0) ** 2).sum(axis=1) + (np.abs(p1) ** 2).sum(axis=1)
    arco_psi = float(np.sum(nrm_a - 2.0 * np.real(incro))) / 2.0
    w = phi.reshape(m, 2)
    f0, f1 = w[:, 0], w[:, 1]
    arco_phi = float(np.sum(np.abs(f0) ** 2 + np.abs(f1) ** 2
                            - 2.0 * np.real(np.conj(f0) * f1))) / 2.0
    arco = -OMEGA * (arco_psi + arco_phi)
    # ------------------------------------------------- la moneta di spin
    h = mot.elicita(st).copy()
    moneta = float(par["eps"]) * float(np.sum(h))
    # ------------------------------------------------- l-accoppiamento materia-vuoto
    # ### ⛔⛔ **DAL `2026-10-15` IL TERMINE E- `CAMM-MATERIA-VUOTO`**, e il motivo per
    # ### cui questa riga e- CAMBIATA e- un numero: con la `N` della saturazione qui
    # ### dentro, ### **`M-B2` dava pendenza `0.078`** invece di `~2` -- cioe-
    # ### ### **misurava un `H` CHE NON E- QUELLO DEL PASSO.**
    # ### ⚠ **Non e- un parametro aggiustato: e- la misura che deve guardare LA LEGGE
    # ### CHE GIRA.** La saturazione e- ### **fuori dall-ordine di composizione**, quindi
    # ### ### **il suo generatore non e- piu- in `H`.**
    # ### ⭐ **E resta UNA SECONDA FONTE, come tutto il resto di questa funzione:** la
    # ### `N` si scrive ### **qui**, con `rho` e `Lambda` ### **che questa funzione ha
    # ### gia- calcolato da se-** (`nrm_psi` e `nrm_phi`), e ### **non si importa da
    # ### `materia_vuoto.py`** -- se le due divergessero, il confronto lo direbbe.
    rho = nrm_psi
    lam = nrm_phi
    N = np.zeros(inc.n, dtype=float)
    vivi = rho > 0.0
    if np.any(vivi):
        N[vivi] = rho[vivi] * np.log(rho[vivi] / (rho[vivi] + lam[vivi]))
    # ### ⛔ **E dove `rho == 0` il termine fa `0`**, perche- `x ln x -> 0`: ### **e- il
    # ### valore che la funzione PRENDE**, non un pavimento.
    accoppia = float(np.sum(N))
    return nodo + arco + moneta + accoppia


def pezzi_di_h(inc, mot, st, par):
    """### `(per_nodo, per_arco)`: ### **i termini di `h_tot`, NON sommati.**

    ### ⛔⛔ **PERCHE' ESISTE** *(mandato del guardiano del `2026-10-17` alle
    `22:08`)*: l'energia ### **PESATA** `H_w` ha bisogno dei termini ### **separati**, e
    `h_tot` ne restituisce ### **UNO SOMMATO.**
    ### ⛔ **E `h_tot` NON SI TOCCA:** il suo valore e' ### **il criterio di `M-B2`**,
    e una somma fatta in un ordine diverso ### **cambia i bit.**

    ### ⚠⚠ **QUESTA E' UNA SECONDA FONTE, E LO DICO:** ripete i quattro termini
    di `h_tot` ### **senza sommarli.** ### ✅ **E si CONFRONTA, a ogni corsa:** a
    `cs = 1` uniforme ### **`sum(per_nodo) + sum(per_arco)` deve dare `h_tot`**, a meno
    dell'ORDINE DELLA SOMMA -- ed e' il braccio `0` di `_misura_hw.py`.
    ### ⛔ **Senza quel confronto sarebbe una copia che puo' divergere in silenzio**,
    ed e' cio' che `STRUMENTO-LEGGE-DALLA-TABELLA` vieta.

    ### ⭐ **E LA DIVISIONE IN DUE GRUPPI NON E' UNA SCELTA: E' LA MAPPA PEZZO ->
    PESO**, letta da `flussi_parziali`:
    ### **NODO** *(i due Grover via `z_nodo`, la moneta via `dtau_nodo`,
    l'accoppiamento `N` via `dtau_nodo`)* ·
    ### **ARCO** *(i due spostamenti via `z_arco`, la media ARMONICA di `B-3`)*.
    """
    psi, phi = st["psi_h"], st["phi_h"]
    m = inc.m
    U = mot.geo.U
    # ------------------------------------------------- i termini di NODO
    nrm_psi = _per_nodo(inc, np.abs(psi[:, 0]) ** 2 + np.abs(psi[:, 1]) ** 2)
    nrm_phi = _per_nodo(inc, np.abs(phi) ** 2)
    S_psi = np.zeros((inc.n, 2), dtype=complex)
    np.add.at(S_psi, inc.nodo, psi)
    S_phi = np.zeros(inc.n, dtype=complex)
    np.add.at(S_phi, inc.nodo, phi)
    d = inc.grado.astype(float)
    pu_psi = (np.abs(S_psi[:, 0]) ** 2 + np.abs(S_psi[:, 1]) ** 2) / d
    pu_phi = np.abs(S_phi) ** 2 / d
    per_nodo = -OMEGA * ((nrm_psi - pu_psi) + (nrm_phi - pu_phi))
    # ### la MONETA: `elicita` e' ### **GIA' SOMMATA PER NODO** *(letto dal sorgente:
    # ### `motore.elicita` fa `np.add.at(h, inc.nodo, sn)` e torna `(n,)`)*, quindi
    # ### ### **non si raccoglie una seconda volta** -- e il peso che la moneta
    # ### legge e' `dtau_nodo`, cioe' ### **il peso del NODO.**
    h = mot.elicita(st).copy()
    assert h.shape == (inc.n,), (
        "`elicita` ha forma %r invece di `(n,)`: se tornasse per ESTREMITA' andrebbe"
        " raccolta sui nodi, e questo termine starebbe pesato SBAGLIATO" % (h.shape,))
    per_nodo = per_nodo + float(par["eps"]) * h
    # ### l'ACCOPPIAMENTO `N`, ### **per nodo**: la stessa riga di `h_tot`
    rho = nrm_psi
    lam = nrm_phi
    N = np.zeros(inc.n, dtype=float)
    vivi = rho > 0.0
    if np.any(vivi):
        N[vivi] = rho[vivi] * np.log(rho[vivi] / (rho[vivi] + lam[vivi]))
    per_nodo = per_nodo + N
    # ------------------------------------------------- i termini di ARCO
    v = psi.reshape(m, 2, 2)
    p0, p1 = v[:, 0, :], v[:, 1, :]
    incro = np.einsum("ai,aji,aj->a", np.conj(p0), np.conj(U), p1)
    nrm_a = (np.abs(p0) ** 2).sum(axis=1) + (np.abs(p1) ** 2).sum(axis=1)
    arco_psi = (nrm_a - 2.0 * np.real(incro)) / 2.0
    w = phi.reshape(m, 2)
    f0, f1 = w[:, 0], w[:, 1]
    arco_phi = (np.abs(f0) ** 2 + np.abs(f1) ** 2
                - 2.0 * np.real(np.conj(f0) * f1)) / 2.0
    per_arco = -OMEGA * (arco_psi + arco_phi)
    return per_nodo, per_arco


def _tick_ordine(st, mot, par, ordine):
    """### ⛔ **UN TICK CON UN ORDINE DATO — SOLO PER LA CONTROPROVA.**

    ### ⚠ **NON cambia la tabella e NON cambia il passo del simulatore:** vive qui
    dentro, e serve a far girare ### **l-ordine di PRIMA** per far vedere che cosa si
    perde.
    """
    import deriva as DV
    mot.apri_tick()
    for idl, frazione in ordine:
        nome, vuole_par = TK.OPERATORE[idl]
        mot.operatori[nome](st, par if vuole_par else {}, frazione)
    mot.chiudi_tick()


# ### ⛔ **L-ORDINE DI PRIMA DEL `2026-10-15`, scritto qui PER LA CONTROPROVA e NON per
# ### girare.** ### ⚠ **E- un dato storico, non una seconda tabella:** la tabella e- UNA, e
# ### questo elenco ### **non la tocca** -- serve a far vedere ### **che cosa si perde**
# ### quando la sequenza non e- palindroma. ### ✅ **E con la composizione di adesso in
# ### tabella, questo e- IL CASO CHE DEVE DARE UN NUMERO DIVERSO.**
ORDINE_VECCHIO = (("CAMM-SATURAZIONE", 0.5), ("CAMM-MONETA-SPIN", 1),
                  ("CAMM-GROVER", 1), ("CAMM-SPOSTAMENTO", 1),
                  ("CAMM-GROVER-VUOTO", 1), ("CAMM-SPOSTAMENTO-VUOTO", 1),
                  ("CAMM-SATURAZIONE", 0.5))


def controprova():
    """### Gli stessi `dtau`, ### **con l-ordine VECCHIO**: la pendenza cade a `1`?

    ### ⛔ **E- IL CASO CHE DEVE DARE UN NUMERO DIVERSO**, e senza di lui il verdetto di
    sopra sarebbe ### **un FALSO-UNO**: una pendenza `2` non proverebbe che e- ### **il
    PALINDROMO** a comprarla -- potrebbe venire da qualunque altra cosa.
    """
    import deriva as DV
    ordine = list(ORDINE_VECCHIO)
    print("-" * 96)
    print("### ⛔ CONTROPROVA (il caso che DEVE dare un numero diverso):")
    print("###   lo STESSO H_tot e gli STESSI dtau, con l'ORDINE DI PRIMA del 2026-10-15")
    print("###   (%d pezzi, NON palindromo). Se la pendenza restasse 2, il verdetto di"
          % len(ordine))
    print("###   sopra sarebbe un FALSO-UNO.")
    righe = []
    for k in KAPPA:
        dtau = 1.0 / (2 ** k)
        tick = int(round(TEMPO / dtau))
        inc, mot, st, par = DV.scena(NN, SEME, dtau, norma=NORMA,
                                     vuoto_modulo=VUOTO_MODULO, su2=SU2)
        h0 = h_tot(inc, mot, st, par)
        peggio = 0.0
        for _t in range(tick):
            _tick_ordine(st, mot, par, ordine)
            d = abs(h_tot(inc, mot, st, par) - h0)
            if d > peggio:
                peggio = d
        rap = (righe[-1] / peggio) if righe and peggio > 0 else float("nan")
        righe.append(peggio)
        print("###   k=%d  dtau=%.6f  tick=%-5d escursione=%.6e  rapporto %s"
              % (k, dtau, tick, peggio,
                 "--" if np.isnan(rap) else "%.3f" % rap))
        sys.stdout.flush()
    rap = [righe[i - 1] / righe[i] for i in range(1, len(righe)) if righe[i] > 0]
    print("###   I RAPPORTI DELL'ORDINE VECCHIO: %s"
          % ("  ".join("%.3f" % r for r in rap),))
    ee = [x for x in righe if x > 0]
    kk = [-np.log2(1.0 / (2 ** k)) for k in KAPPA[:len(ee)]]
    pend = -float(np.polyfit(kk, np.log2(ee), 1)[0])
    print("###   E LA PENDENZA DELL'ORDINE VECCHIO: %.3f   (il palindromo da' ~2)" % pend)
    if pend < 1.5:
        print("###   ✅ IL CASO CHE DEVE FALLIRE FALLISCE: pendenza %.3f, cioe' PRIMO"
              " ordine." % pend)
        print("###   Quindi il secondo ordine viene DAL PALINDROMO, e non da altro.")
    else:
        print("###   ⛔ IL CASO CHE DEVE FALLIRE NON FALLISCE (pendenza %.3f): allora il"
              % pend)
        print("###   verdetto di sopra NON e' attribuibile al palindromo -- E' UN"
              " FALSO-UNO.")
    return pend


def una_corsa(dtau, tick):
    """### `(escursione, H0)` su `tick` tick, ### **guardando H A OGNI TICK.**"""
    import deriva as DV
    inc, mot, st, par = DV.scena(NN, SEME, dtau, norma=NORMA,
                                 vuoto_modulo=VUOTO_MODULO, su2=SU2)
    h0 = h_tot(inc, mot, st, par)
    peggio = 0.0
    for _t in range(tick):
        TK.tick(st, mot, par)
        d = abs(h_tot(inc, mot, st, par) - h0)
        if d > peggio:
            peggio = d
    return peggio, h0


def estendi_righe():
    """### Gli stessi conti su `KAPPA_FINE`: ### **la pendenza CONVERGE a `2`?**

    ### ⛔ **NON E- IL CRITERIO, ed e- dichiarato**: il criterio e- `KAPPA`, con la scena e
    lo script che il mandato fissa. ### **Questo blocco AGGIUNGE punti, non cambia la
    soglia** -- e la differenza conta: allargare una soglia per far passare una misura e-
    vietato, ### **misurare piu- a fondo no.**
    """
    print("-" * 96)
    print("### 📌 ESTENSIONE (NON il criterio): due dimezzamenti in piu', per vedere se la")
    print("###   PENDENZA CONVERGE a 2. A dtau = 0.5 i pezzi stanno a theta = pi/2, cioe'")
    print("###   LONTANO dal regime asintotico.")
    righe = []
    for k in KAPPA_FINE:
        dtau = 1.0 / (2 ** k)
        tick = int(round(TEMPO / dtau))
        err, _h0 = una_corsa(dtau, tick)
        rap = (righe[-1][1] / err) if righe and err > 0 else float("nan")
        righe.append((dtau, err))
        print("###   k=%d  dtau=%.6f  tick=%-5d escursione=%.6e  rapporto %s"
              % (k, dtau, tick, err, "--" if np.isnan(rap) else "%.3f" % rap))
        sys.stdout.flush()
    rr = [righe[i - 1][1] / righe[i][1] for i in range(1, len(righe))
          if righe[i][1] > 0]
    if rr:
        print("###   I RAPPORTI FINI: %s   (pendenza log2: %s)"
              % ("  ".join("%.3f" % r for r in rr),
                 "  ".join("%.3f" % np.log2(r) for r in rr)))
    # ### ⚠ **il primo punto e- lo STESSO `k = 4` del criterio**: si torna senza, per
    # ### ### **non contarlo due volte** nella pendenza complessiva.
    return righe[1:]


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    print("=" * 96)
    print("M-B2: L'ERRORE DI CONSERVAZIONE DI H_tot CONTRO dtau -- tempo totale FISSO")
    print("=" * 96)
    print("  LA CONFIGURAZIONE: T = %.1f   nn = %d   seme = %d   norma = %s"
          "   vuoto_modulo = %.1f   su2 = %s   omega = pi"
          % (TEMPO, NN, SEME, NORMA, VUOTO_MODULO, SU2))
    print("-" * 96)
    print("  %-4s %-10s %-7s %-14s %-14s %s"
          % ("k", "dtau", "tick", "H(0)", "escursione", "rapporto col k-1"))
    righe = []
    for k in KAPPA:
        dtau = 1.0 / (2 ** k)
        tick = int(round(TEMPO / dtau))
        err, h0 = una_corsa(dtau, tick)
        rap = (righe[-1][2] / err) if righe and err > 0 else float("nan")
        righe.append((dtau, tick, err))
        print("  %-4d %-10.6f %-7d %-14.6f %-14.6e %s"
              % (k, dtau, tick, h0, err,
                 "--" if np.isnan(rap) else "%.3f" % rap))
        sys.stdout.flush()
    print("-" * 96)
    rap = [righe[i - 1][2] / righe[i][2] for i in range(1, len(righe))
           if righe[i][2] > 0]
    if not rap:
        print("### ⛔ escursione NULLA: niente da misurare, e un rapporto non esiste")
        return 1
    print("  I RAPPORTI: %s" % ("  ".join("%.3f" % r for r in rap),))
    print("  LA PENDENZA in log2: %s"
          % ("  ".join("%.3f" % np.log2(r) for r in rap),))
    # ### ⭐ **L-ESTENSIONE, PRIMA DEL VERDETTO**: serve a dire se la pendenza converge
    tutti = righe + [(d, 0, e) for d, e in estendi_righe()]
    # ### ⭐⭐ **LA PENDENZA COMPLESSIVA, e perche- e- LEI il verdetto e non i rapporti
    # ### uno per uno:** l-errore e- un ### **MASSIMO su una finestra**, e un massimo
    # ### ### **NON e- una funzione liscia di `dtau`** -- al dimezzare, il massimo puo-
    # ### spostarsi su un altro istante, e il rapporto ### **oscilla.** ### ✅ **La
    # ### PENDENZA su tutto l-intervallo e- la stima che non oscilla**, ed e- la
    # ### statistica che si usa per un ordine di convergenza.
    ee = [x[2] for x in tutti]
    kk = [-np.log2(x[0]) for x in tutti]
    pend = float(np.polyfit(kk, np.log2(ee), 1)[0])
    glob = ee[0] / ee[-1]
    print("-" * 96)
    print("  I RAPPORTI, uno per uno: %s" % ("  ".join("%.3f" % r for r in rap),))
    print("  E LA PENDENZA COMPLESSIVA su %d dimezzamenti: %.3f   (globale: %.6e -> %.6e,"
          " cioe' un fattore %.1f dove 2^(2*%d) = %d)"
          % (len(tutti) - 1, -pend, ee[0], ee[-1], glob, len(tutti) - 1,
             2 ** (2 * (len(tutti) - 1))))
    # ### ⛔ **E LA BANDA E- MIA, non di Luca, e lo dico:** `0.25` attorno a `2`. Il
    # ### ### **criterio di Luca e- <<rapporto ~ 4>>**, e un rapporto per volta qui
    # ### ### **oscilla fra `2.97` e `5.19`** per il motivo di sopra. ### **Chi legge
    # ### decide se questa e- la lettura giusta: i numeri sono tutti stampati.**
    if abs(-pend - 2.0) <= 0.25:
        print("### ✅ L'ERRORE E' DI SECONDO ORDINE: pendenza %.3f, entro `0.25` da `2`."
              % (-pend,))
        print("###   ⚠ MA I RAPPORTI UNO PER UNO NON sono tutti `~4`: il piu' grossolano")
        print("###   e' %.3f. La banda `0.25` sulla PENDENZA e' MIA, non di Luca: il suo"
              % (rap[0],))
        print("###   criterio dice <<rapporto ~ 4>>, e la lettura la decide lui.")
        controprova()
        return 0
    print("### ⛔ `M-B2` NON DA' IL SECONDO ORDINE: pendenza %.3f" % (-pend,))
    print("###   NESSUN PARAMETRO SI TOCCA per far tornare il 4.")
    controprova()
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
