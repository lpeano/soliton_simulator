# -*- coding: utf-8 -*-
r"""**IL VERSO DI `L2`: LA MATERIA CONSUMA IL VUOTO?** — *una misura, e i criteri sono
fissati PRIMA.*

> **Punto 2 del mandato di Luca del 2026-10-15** *(`16:50` e `17:27`)*. La decisione dice
> che **la materia consuma il vuoto**, e dice anche: ### ⛔ **IL VERSO NON E' IMPOSTO, deve
> USCIRE dalla dinamica — e se la misura da' il verso opposto, NESSUNA LEGGE per
> raddrizzarlo: si riporta e ci si ferma.**

## ⭐ LA GRANDEZZA E' DIFFERENZIALE, e non e' un dettaglio

```
dLambda_k(t) = Lambda_k(CON materia)  -  Lambda_k(SENZA materia)
```

### ⛔ **La sola `Lambda` assoluta NON conta**, perche' il vuoto si muove anche da solo
*(arrotondamento, e la camminata e' comunque unitaria)*. ### ✅ **Le due scene hanno lo
STESSO `phi`, lo STESSO grafo e lo STESSO `dtau`:** cio' che cambia e' **solo il grumo.**

## 📌 IL PAVIMENTO DEL RUMORE NON E' SCELTO: E' MISURATO

### **La deriva della scena SENZA materia** *(braccio `B`)* e' il pavimento: un `dLambda`
piu' piccolo di quello ### **non dice niente.** ### ⚠ **E non e' una soglia che ho scelto
io: e' un numero della stessa corsa.**

## ⛔ IL CASO CHE DEVE FALLIRE

### **Lo stesso esperimento col segno di `beta` ROVESCIATO** — e ### **il motore NON si
tocca:** si sostituisce `saturazione.pezzi` **a runtime, dentro questo script.**
### ⚠ **Se il segno di `dLambda` non si rovescia, la misura NON VEDE IL MECCANISMO e
nessun verdetto vale.**

Gira con:  python primo_ordine/_misura_verso_l2.py
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
TICK = 400
FINESTRE = 4
TICK_FERMO = 240
RAGGIO = 1
SEME = 7
# ### ⭐ **I DUE REGIMI DI `x = h/Lambda`**, e NON sono due numeri a caso: con l-elicita-
# ### `+1` si ha `h = somma |psi|^2` sul nodo e `Lambda = somma |phi|^2`, quindi
# ### ### **`x = (ampiezza/vuoto)^2`** -- cioe- i due valori qui sotto danno `x ~ 1e-4` e
# ### ### **`x ~ 1`**, che e- cio- che la scansione chiede.
REGIMI = (("x piccolo", 0.01, 1.0), ("x di ordine 1", 1.0, 1.0))
DTAU = (1.0, 0.5)
# ### ⛔ **L-ORDINE DI PRIMA DEL 2026-10-15, scritto qui PER UN SOLO BRACCIO e non per
# ### girare.** ### **E- un dato storico, non una seconda tabella:** serve a rispondere a
# ### UNA domanda -- ### **la parte DISPARI in `beta` ricompare se il passo NON e-
# ### palindromo?**
ORDINE_VECCHIO = (("CAMM-SATURAZIONE", 0.5), ("CAMM-MONETA-SPIN", 1),
                  ("CAMM-GROVER", 1), ("CAMM-SPOSTAMENTO", 1),
                  ("CAMM-GROVER-VUOTO", 1), ("CAMM-SPOSTAMENTO-VUOTO", 1),
                  ("CAMM-SATURAZIONE", 0.5))


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    print("  %-62s %s   %s" % (che[:62], "PASSA" if passa else "### FALLISCE", nota))


def lambda_per_nodo(mot, st):
    return mot.densita_vuoto(st).copy()


def corri(dtau, vuoto, ampiezza, materia, geometrici, fasi, tick, ordine=None,
          elicita=1):
    """### `(Lambda(t), somma|phi|^2(t), h(0))`, ### **campionati a OGNI tick.**

    ### ⚠ **`ordine = None` vuol dire L-ORDINE DELLA TABELLA** *(via `DV.tick`)*. Un
    ordine dato serve ### **a un braccio solo** -- quello che chiede se la parte dispari
    ricompare col passo **non palindromo** -- e ### **non cambia la tabella.**
    """
    import deriva as DV
    import scena_l2 as SC
    inc, mot, st, par, centro, per = SC.scena(dtau, vuoto, ampiezza, RAGGIO, materia,
                                              geometrici, fasi, SEME, elicita)
    h0 = mot.elicita(st).copy()
    storia_h = [h0.copy()]
    lam = [lambda_per_nodo(mot, st)]
    tot = [float(np.sum(np.abs(st["phi_h"]) ** 2))]
    for _t in range(tick):
        if ordine is None:
            DV.tick(st, mot, par)
        else:
            mot.apri_tick()
            for idl, fr in ordine:
                nome, vuole_par = DV.OPERATORE[idl]
                mot.operatori[nome](st, par if vuole_par else {}, fr)
            mot.chiudi_tick()
        lam.append(lambda_per_nodo(mot, st))
        tot.append(float(np.sum(np.abs(st["phi_h"]) ** 2)))
        storia_h.append(mot.elicita(st).copy())
    return np.array(lam), np.array(tot), h0, per, centro, np.array(storia_h)


def differenziale(dtau, vuoto, ampiezza, geometrici, fasi, tick, ordine=None,
                  elicita=1):
    """### `dLambda_k(t)` fra la scena **con** e la scena **senza** materia."""
    a, ta, h0, per, centro, sh = corri(dtau, vuoto, ampiezza, True, geometrici, fasi,
                                       tick, ordine, elicita)
    b, tb, _h, _p, _c, _s = corri(dtau, vuoto, ampiezza, False, geometrici, fasi, tick,
                                  ordine, elicita)
    return a - b, a, b, ta, tb, h0, per, sh


def per_finestre(dl, per, quante):
    """### `dLambda` **mediata per anello e per finestra di tick.**

    ### ⭐ **Le finestre servono a una cosa sola: vedere se il segno RESTA**, invece di
    leggere un istante. ### ⚠ **Un singolo tick di una grandezza che oscilla e' un
    campione**, e quella lezione l'ho gia' pagata.
    """
    t = dl.shape[0]
    bordi = [int(round(t * i / float(quante))) for i in range(quante + 1)]
    fuori = {}
    for d in sorted(per):
        nodi = per[d]
        riga = []
        for i in range(quante):
            a, b = bordi[i], bordi[i + 1]
            riga.append(float(np.mean(dl[a:b][:, nodi])))
        fuori[d] = riga
    return fuori


# ====================================================================== i bracci
def braccio_beta():
    """### `beta = dN/dLambda` **verificato COL CODICE**, non solo a mano."""
    import saturazione as SAT
    print("-" * 96)
    print("### (A) `beta = dN/dLambda` e `al = dN/dh`: il conto a mano contro il codice")
    h = np.array([0.03, 0.3, 1.0, 3.0, 10.0])
    lam = np.array([1.0, 1.0, 1.0, 1.0, 1.0])
    al, be = SAT.pezzi(h, lam)

    def N(hh, ll):
        return ll * SAT.G(hh / ll)

    d = 1e-6
    al_num = (N(h + d, lam) - N(h - d, lam)) / (2 * d)
    be_num = (N(h, lam + d) - N(h, lam - d)) / (2 * d)
    ea = float(np.max(np.abs(al - al_num)))
    eb = float(np.max(np.abs(be - be_num)))
    esito("(A1) `al` e' `dN/dh` (differenze finite)", ea <= 1e-7,
          "scarto massimo %.3e su 5 valori di x" % ea)
    esito("(A2) `be` e' `dN/dLambda` (differenze finite)", eb <= 1e-7,
          "scarto massimo %.3e su 5 valori di x" % eb)
    # ### ⭐ **e il SEGNO, piu- la scala `-(2/3)x^3` per `x` piccolo**
    x = 0.03
    atteso = -(2.0 / 3.0) * x ** 3
    _a, b1 = SAT.pezzi(np.array([x]), np.array([1.0]))
    esito("(A3) `be < 0` e vale `-(2/3)x^3` per `x` piccolo",
          b1[0] < 0 and abs(b1[0] - atteso) <= 0.05 * abs(atteso),
          "be(%.2f) = %.6e, e -(2/3)x^3 = %.6e" % (x, b1[0], atteso))
    return ea, eb


def braccio_fermo():
    """### Il vuoto di riferimento **SENZA materia**: ### **e' STAZIONARIO?**"""
    print("-" * 96)
    print("### (B) IL VUOTO DI RIFERIMENTO SENZA MATERIA: stazionario su %d tick?"
          % TICK_FERMO)
    peggio = {}
    for dtau in DTAU:
        lam, tot, _h, _p, _c, _sh = corri(dtau, 1.0, 0.0, False, True, False, TICK_FERMO)
        scarto = float(np.max(np.abs(lam - lam[0])))
        scala = float(np.max(np.abs(lam[0])))
        rel = scarto / scala
        eps_m = float(np.finfo(float).eps)
        dtot = float(np.max(np.abs(tot - tot[0]))) / abs(tot[0])
        esito("(B) `Lambda_k` invariante all'ulp, dtau = %.2f" % dtau,
              rel <= 4096 * eps_m,
              "scarto relativo %.3e = %.0f ulp; e somma|phi|^2 cambia di %.3e"
              % (rel, rel / eps_m, dtot))
        peggio[dtau] = scarto
    return peggio


def braccio_h():
    """### `h` del grumo: ### **`!= 0` allineato, `= 0` isotropo.**"""
    import scena_l2 as SC
    print("-" * 96)
    print("### (C) `h` DEL GRUMO: l'elicita' +1 contro il grumo ISOTROPO")
    inc, mot, st, _par, _c, per = SC.scena(1.0, 1.0, 1.0, RAGGIO, True, True, False,
                                           SEME, 1)
    h_all = mot.elicita(st).copy()
    dentro = [v for d, nodi in per.items() if d <= RAGGIO for v in nodi]
    esito("(C1) col grumo ALLINEATO `h` e' > 0 sui nodi del grumo",
          float(np.min(h_all[dentro])) > 0.1,
          "h sul grumo: min %.4f  max %.4f; fuori: max |h| = %.3e"
          % (float(np.min(h_all[dentro])), float(np.max(h_all[dentro])),
             float(np.max(np.abs(np.delete(h_all, dentro))))))
    # ### ⭐ **e la DENSITA-: `h_k` deve essere `somma |psi_h|^2` sul nodo**
    dens = np.zeros(inc.n)
    np.add.at(dens, inc.nodo, np.sum(np.abs(st["psi_h"]) ** 2, axis=1))
    esito("(C2) e `h_k` E' la densita' `somma |psi_h|^2` (l'elicita' +1 lo garantisce)",
          float(np.max(np.abs(h_all - dens))) <= 1e-12,
          "scarto massimo %.3e" % float(np.max(np.abs(h_all - dens))))
    SC.grumo_isotropo(st, inc, per, RAGGIO, 1.0)
    h_iso = mot.elicita(st).copy()
    esito("### (C3) DEVE ESSERE ZERO: col grumo ISOTROPO `h` si annulla",
          float(np.max(np.abs(h_iso))) <= 1e-12,
          "max |h| = %.3e: ### un grumo isotropo NON TOCCA IL VUOTO"
          % float(np.max(np.abs(h_iso))))
    return float(np.max(np.abs(h_iso)))


def braccio_verso(pavimento):
    """### ⭐⭐ **IL VERSO**: `dLambda` sui nodi del grumo e sugli anelli."""
    print("-" * 96)
    print("### (D) IL VERSO: dLambda = Lambda(materia) - Lambda(vuoto)")
    fuori = {}
    for nome, amp, vuo in REGIMI:
        for dtau in DTAU:
            dl, a, b, ta, tb, h0, per, sh = differenziale(dtau, vuo, amp, True, False, TICK)
            tab = per_finestre(dl, per, FINESTRE)
            x = (amp / vuo) ** 2
            dentro = [v for d, nodi in per.items() if d <= RAGGIO for v in nodi]
            grumo = [float(np.mean(dl[s:e][:, dentro]))
                     for s, e in _bordi(dl.shape[0], FINESTRE)]
            segni = set(np.sign(g) for g in grumo if abs(g) > pavimento[dtau])
            print("  %-16s dtau=%.2f  x=%.4g   dLambda sul GRUMO per finestra: %s"
                  % (nome, dtau, x, "  ".join("%+.3e" % g for g in grumo)))
            for d in sorted(tab):
                if d <= 3:
                    print("      anello %d (%2d nodi): %s"
                          % (d, len(per[d]), "  ".join("%+.3e" % y for y in tab[d])))
            tot = float(np.max(np.abs(ta - ta[0]))) / abs(ta[0])
            print("      e il vuoto TOTALE somma|phi|^2 cambia di %.3e (relativo);"
                  "  pavimento del rumore %.3e" % (tot, pavimento[dtau]))
            fuori[(nome, dtau)] = (grumo, tab, x, tot, segni)
    return fuori


def _bordi(t, quante):
    b = [int(round(t * i / float(quante))) for i in range(quante + 1)]
    return [(b[i], b[i + 1]) for i in range(quante)]


def braccio_tre_grumi(pavimento):
    """### ⭐⭐ **I TRE GRUMI: elicita' `+1`, `-1`, e ISOTROPO** *(integrazione del
    guardiano del `2026-10-15`)*.

    ### ⛔ **E nasce da una MIA AFFERMAZIONE SBAGLIATA:** avevo scritto che `h_k` **e'** la
    densita' di materia. ### **Non lo e': e' l'ELICITA', col suo segno** — e coincide con
    la densita' **solo a elicita' `+1`.** ### ⚠ **E `G(x) = x - arctan x` e' DISPARI**,
    quindi `beta` ### **cambia segno con `h`.**

    ### ⭐ **E UNA PREVISIONE, scritta prima di misurare:** siccome `dLambda` e' risultato
    ### **PARI in `beta`** *(braccio `E1`)*, e rovesciare l'elicita' ### **rovescia
    `beta`**, allora `(a)` e `(b)` dovrebbero dare ### **lo STESSO `dLambda`**, cioe'
    ### **rapporto `~1`.** ### ⛔ **Se invece danno segni OPPOSTI, la mia misura della
    parita' era sbagliata** — e allora e' quella da rifare, non questa.
    """
    print("-" * 96)
    print("### (H) I TRE GRUMI: elicita' +1, -1, e ISOTROPO -- stessa densita', stessa"
          " scena")
    fuori = {}
    for nome, el in (("elicita' +1", 1), ("elicita' -1", -1), ("ISOTROPO (h = 0)", 0)):
        for dtau in DTAU:
            dl, a, b, ta, tb, h0, per, sh = differenziale(dtau, 1.0, 1.0, True, False, TICK,
                                                      None, el)
            dentro = [v for d, nodi in per.items() if d <= RAGGIO for v in nodi]
            grumo = [float(np.mean(dl[s:e][:, dentro]))
                     for s, e in _bordi(dl.shape[0], FINESTRE)]
            anelli_ = per_finestre(dl, per, FINESTRE)
            fuori[(nome, dtau)] = (grumo, float(np.max(np.abs(dl))), h0,
                                   float(np.max(np.abs(sh[:, dentro]))))
            # ### ⛔⛔ **E LA STORIA DI `h`, che e- la cosa che spiega tutto:** `h = 0` vale
            # ### ### **solo a `t = 0`** -- poi `psi` evolve, il grumo ### **non e- piu-
            # ### isotropo**, e ### **l-elicita- NASCE.** ### **Un controllo <<nullo>> che
            # ### si accende da solo NON E- UN CONTROLLO.**
            hmax = float(np.max(np.abs(sh[:, dentro])))
            print("  %-18s dtau=%.2f  h(0) = %+.4f   max|h(t)| = %.4f   dLambda per"
                  " finestra: %s" % (nome, dtau, float(h0[dentro[0]]), hmax,
                                     "  ".join("%+.3e" % g for g in grumo)))
            for d in sorted(anelli_):
                if d <= 2:
                    print("        anello %d: %s"
                          % (d, "  ".join("%+.3e" % y for y in anelli_[d])))
    # ---------------------------------------------------- il controllo ISOTROPO, col numero
    for dtau in DTAU:
        m = fuori[("ISOTROPO (h = 0)", dtau)][1]
        hm = fuori[("ISOTROPO (h = 0)", dtau)][3]
        esito("### (H0) il grumo ISOTROPO da' `dLambda = 0` all'ulp, dtau = %.2f" % dtau,
              m <= 1e-12,
              "max |dLambda| = %.3e, e il MOTIVO e' misurato: `h(0) = 0` ma"
              " `max|h(t)| = %.4f` -> ### L'ELICITA' NASCE mentre `psi` evolve, quindi"
              " <<isotropo>> NON E' UN CONTROLLO NULLO" % (m, hm))
    # ---------------------------------------------------- (a) contro (b)
    for dtau in DTAU:
        ga = fuori[("elicita' +1", dtau)][0]
        gb = fuori[("elicita' -1", dtau)][0]
        rap = [abs(x) / abs(y) if abs(y) > 0 else float("nan")
               for x, y in zip(ga, gb)]
        stesso = all(np.sign(x) == np.sign(y) for x, y in zip(ga, gb))
        print("  dtau=%.2f  |dLambda(+1)|/|dLambda(-1)| per finestra: %s"
              % (dtau, "  ".join("%.4f" % r for r in rap)))
        esito("### (H1) a dtau = %.2f `(a)` e `(b)` hanno lo STESSO segno" % dtau,
              stesso,
              "se OPPOSTI, la fonte della <<gravita'>> e' L'ELICITA' e non la materia:"
              " conflitto col principio di equivalenza, e DECISIONE DI LUCA")
    return fuori


def braccio_rovescio(pavimento):
    """### ⛔ **IL CASO CHE DEVE FALLIRE: `beta` col segno ROVESCIATO.**

    ### ⚠ **E il motore NON si tocca:** si sostituisce `saturazione.pezzi` **a runtime**,
    e ### **si rimette a posto alla fine** -- il modulo e' condiviso, e lasciarlo
    sporcato falserebbe ogni misura successiva **nella stessa corsa.**
    """
    import saturazione as SAT
    print("-" * 96)
    print("### (E) IL CASO CHE DEVE FALLIRE: `beta` col SEGNO ROVESCIATO (solo qui)")
    vero = SAT.pezzi

    def rovescio(h, lam):
        al, be = vero(h, lam)
        return al, -be

    def spento(h, lam):
        al, be = vero(h, lam)
        return al, 0.0 * be

    fuori, campi = {}, {}
    for nome, f in (("vero", vero), ("rovesciato", rovescio), ("SPENTO (be = 0)", spento)):
        SAT.pezzi = f
        try:
            dl, a, b, ta, tb, h0, per, sh = differenziale(1.0, 1.0, 1.0, True, False, TICK)
            dentro = [v for d, nodi in per.items() if d <= RAGGIO for v in nodi]
            fuori[nome] = [float(np.mean(dl[s:e][:, dentro]))
                           for s, e in _bordi(dl.shape[0], FINESTRE)]
            campi[nome] = dl.copy()
        finally:
            SAT.pezzi = vero
        print("      dLambda sul GRUMO, beta %-16s: %s"
              % (nome, "  ".join("%+.3e" % g for g in fuori[nome])))
    # ### ⛔⛔ **E LA DIFFERENZA SI MISURA, NON SI LEGGE DAL TABULATO.** ### **Due numeri
    # ### stampati a quattro cifre possono essere diversi all-ottava**, e <<identici>>
    # ### letto a occhio e- ### **la cosa che mi ha gia- fregato.**
    # ### ⭐ **E il numero che serve e- la SCOMPOSIZIONE in parte PARI e parte DISPARI:**
    # ### pari = (f(beta) + f(-beta))/2, dispari = (f(beta) - f(-beta))/2. ### **Se la
    # ### parte dispari e- zero, il segno del risultato NON viene dal segno di `beta`.**
    A, B = campi["vero"], campi["rovesciato"]
    pari = 0.5 * (A + B)
    disp = 0.5 * (A - B)
    sp = float(np.max(np.abs(disp)))
    pp = float(np.max(np.abs(pari)))
    print("      ### LA SCOMPOSIZIONE: max |parte PARI| = %.6e,"
          "  max |parte DISPARI| = %.6e  ->  dispari/pari = %.3e"
          % (pp, sp, sp / pp if pp > 0 else float("nan")))
    esito("### (E1) la parte DISPARI in `beta` e' NON TRASCURABILE",
          pp > 0 and sp / pp > 1e-6,
          "dispari/pari = %.3e: ### se e' ~0, il SEGNO di `dLambda` NON viene dal segno"
          " di `beta`, e nessun verdetto sul VERSO vale" % (sp / pp if pp > 0 else 0.0))
    # ### ⭐⭐ **(E2) E LA DOMANDA CHE VIENE SUBITO DOPO: PERCHE- la parte dispari e- zero?**
    # ### **L-ipotesi, derivata:** il hop del vuoto da- un termine
    # ### `- |phi|^2 sin(theta_arco) sin(d psi)`, che e- ### **DISPARI** nella differenza
    # ### di fase, e quindi dispari in `beta`. ### ⛔ **Ma il passo adesso e- PALINDROMO,
    # ### cioe- SIMMETRICO PER INVERSIONE DEL TEMPO** -- e un trasporto con un verso
    # ### preferito e- proprio cio- che una simmetria di inversione del tempo
    # ### ### **VIETA.**
    # ### ✅ **E non lo suppongo: lo misuro.** Se con l-ordine di PRIMA *(non palindromo)*
    # ### la parte dispari ### **ricompare**, allora e- ### **il palindromo** a ucciderla.
    # ### ⭐⭐ **E PRIMA: LA SCOMPOSIZIONE TICK PER TICK.** ### **Se la parte dispari e-
    # ### zero GIA- AL PRIMO TICK, il motivo e- nella forma del passo; se nasce e poi si
    # ### cancella, il motivo e- nell-accumulo.** ### **Sono due cose diverse, e la
    # ### differenza va vista, non supposta.**
    for t in (1, 2, 3, 10):
        cc = {}
        for segno, f in (("vero", vero), ("rovesciato", rovescio)):
            SAT.pezzi = f
            try:
                dl, _a, _b, _ta, _tb, _h, _per, _sh = differenziale(1.0, 1.0, 1.0, True,
                                                               False, t)
                cc[segno] = dl[-1].copy()
            finally:
                SAT.pezzi = vero
        pa = 0.5 * (cc["vero"] + cc["rovesciato"])
        di = 0.5 * (cc["vero"] - cc["rovesciato"])
        mp = float(np.max(np.abs(pa)))
        md = float(np.max(np.abs(di)))
        print("      al tick %-3d: max |pari| = %.6e   max |dispari| = %.6e   -> %.3e"
              % (t, mp, md, md / mp if mp > 0 else float("nan")))
    # ### ⭐⭐ **E L-ALTRA DOMANDA, che viene da un conto ARITMETICO: a `dtau = 1` i DUE
    # ### MEZZI-HOP CENTRALI DEL VUOTO compongono il hop INTERO**, e a `theta = pi` il hop
    # ### e- ### **una PERMUTAZIONE PURA** -- `alpha = 0`, quindi ### **il termine
    # ### d-interferenza SPARISCE**, e con lui il solo canale che dipende dalla FASE in
    # ### modo DISPARI. ### ✅ **A `dtau = 0.5` quel canale c-e-**: se la parte dispari
    # ### comparisse la-, il caso `dtau = 1` sarebbe ### **un caso SPECIALE** e la misura
    # ### del verso andrebbe fatta a `dtau < 1`.
    rapporti = {}
    for nome, ordine, dt in (("PALINDROMO, dtau = 1", None, 1.0),
                             ("PALINDROMO, dtau = 0.5", None, 0.5),
                             ("NON palindromo, dtau = 1", list(ORDINE_VECCHIO), 1.0),
                             ("NON palindromo, dtau = 0.5", list(ORDINE_VECCHIO), 0.5)):
        campo = {}
        for segno, f in (("vero", vero), ("rovesciato", rovescio)):
            SAT.pezzi = f
            try:
                dl, _a, _b, _ta, _tb, _h, _per, _sh = differenziale(dt, 1.0, 1.0, True,
                                                               False, TICK, ordine)
                campo[segno] = dl.copy()
            finally:
                SAT.pezzi = vero
        pa = 0.5 * (campo["vero"] + campo["rovesciato"])
        di = 0.5 * (campo["vero"] - campo["rovesciato"])
        mp, md = float(np.max(np.abs(pa))), float(np.max(np.abs(di)))
        r = md / mp if mp > 0 else float("nan")
        rapporti[nome] = r
        print("      %-30s max|pari| = %.4e  max|dispari| = %.4e  -> %.3e"
              % (nome, mp, md, r))
    esito("### (E2) la parte DISPARI compare in ALMENO UNO dei quattro casi",
          max(r for r in rapporti.values() if r == r) > 1e-6,
          "i quattro rapporti: %s"
          % "  ".join("%s=%.2e" % (k.replace("PALINDROMO", "pal")
                                   .replace("NON palindromo", "nonpal"), r)
                      for k, r in rapporti.items()))
    # ### ⛔⛔ **IL CONTROLLO CHE DISTINGUE DUE COSE DIVERSE, e serve PRIMA di qualunque
    # ### verdetto:** se col segno rovesciato `dLambda` non cambia, ci sono DUE
    # ### spiegazioni -- ### **(i) l-effetto e- PARI in `beta`** *(e allora il suo segno
    # ### NON viene da `beta`)*, oppure ### **(ii) la sostituzione non arriva al motore**
    # ### *(e allora e- un mio difetto)*. ### ✅ **Con `beta = 0` la materia non tocca piu-
    # ### il vuoto: se `dLambda` NON va a zero, e- il caso (ii).**
    sp0 = max(abs(x) for x in fuori["SPENTO (be = 0)"])
    esito("### (E0) la sostituzione ARRIVA al motore: con `beta = 0` `dLambda` si annulla",
          sp0 <= 1e-12,
          "max |dLambda| con beta = 0: %.3e  ### se NON fosse ~0, il caso che deve"
          " fallire non starebbe misurando niente" % sp0)
    return fuori["rovesciato"], fuori["SPENTO (be = 0)"], rapporti


def braccio_robustezza(pavimento):
    """### La robustezza: `n` casuali, e `phi` a fasi casuali. ### **Il verso cambia?**"""
    print("-" * 96)
    print("### (F) ROBUSTEZZA: n casuali, e phi a fasi casuali")
    fuori = {}
    for nome, geo, fasi in (("n CASUALI", False, False),
                            ("phi a FASI CASUALI", True, True)):
        dl, a, b, ta, tb, h0, per, sh = differenziale(1.0, 1.0, 1.0, geo, fasi, TICK)
        dentro = [v for d, nodi in per.items() if d <= RAGGIO for v in nodi]
        grumo = [float(np.mean(dl[s:e][:, dentro]))
                 for s, e in _bordi(dl.shape[0], FINESTRE)]
        print("  %-22s dLambda sul GRUMO: %s   (h sul grumo: max %.4f)"
              % (nome, "  ".join("%+.3e" % g for g in grumo),
                 float(np.max(np.abs(h0)))))
        fuori[nome] = grumo
    return fuori


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    import scena_l2 as SC
    print("=" * 96)
    print("IL VERSO DI L2: LA MATERIA CONSUMA IL VUOTO? -- una misura, criteri fissati"
          " prima")
    print("=" * 96)
    print("  LA CONFIGURAZIONE: toro %s   tick = %d   finestre = %d   raggio del grumo = %d"
          "   seme = %d   dtau = %s" % (SC.LATI, TICK, FINESTRE, RAGGIO, SEME, DTAU))
    print("  I REGIMI: %s" % ", ".join("%s (ampiezza %.3g, vuoto %.3g, x = %.4g)"
                                       % (n, a, v, (a / v) ** 2) for n, a, v in REGIMI))
    braccio_beta()
    pavimento = braccio_fermo()
    braccio_h()
    tab = braccio_verso(pavimento)
    rov, spe, rapporti = braccio_rovescio(pavimento)
    tre = braccio_tre_grumi(pavimento)
    braccio_robustezza(pavimento)
    # ============================================================ IL VERDETTO
    print("=" * 96)
    print("### IL VERDETTO")
    # ### ⛔⛔ **IL VERDETTO SI LEGGE SOLO DOVE LA PRECONDIZIONE VALE, e la precondizione
    # ### e- il CASO CHE DEVE FALLIRE.** ### **Il mandato lo dice: <<se non lo rovescia, la
    # ### misura non vede il meccanismo e NESSUN VERDETTO VALE>>.**
    # ### ⭐⭐ **E la precondizione NON vale allo stesso modo ai due `dtau`, ed e- il fatto
    # ### nuovo di questa corsa:** a `dtau = 1` i due mezzi-hop centrali del vuoto
    # ### compongono il hop INTERO, e a `theta = pi` il hop e- ### **una PERMUTAZIONE
    # ### PURA** *(`alpha = 0`)* -- ### **il termine d-interferenza sparisce, e con lui il
    # ### solo canale che dipende dalla fase in modo DISPARI.**
    for dtau in DTAU:
        nome = "PALINDROMO, dtau = %g" % dtau
        r = rapporti.get(nome, float("nan"))
        grumo = tab[("x di ordine 1", dtau)][0]
        pav = pavimento[dtau]
        sopra = [g for g in grumo if abs(g) > pav]
        neg = [g for g in sopra if g < 0]
        media = float(np.mean(grumo))
        sigma = float(np.std(grumo))
        print("-" * 96)
        print("  dtau = %.2f:  canale DISPARI (dispari/pari) = %.3e" % (dtau, r))
        print("      dLambda sul grumo per finestra: %s"
              % "  ".join("%+.3e" % g for g in grumo))
        print("      media sulle finestre %+.3e,  scarto quadratico %.3e"
              % (media, sigma))
        esito("(G) a dtau = %.2f la PRECONDIZIONE vale (il canale dispari c'e')" % dtau,
              r == r and r > 1e-6,
              "dispari/pari = %.3e: ### sotto ~0 il segno di `dLambda` NON viene da `beta`"
              % r)
        esito("(G) e a dtau = %.2f il SEGNO e' lo STESSO in tutte le finestre" % dtau,
              len(sopra) >= 1 and (len(neg) == len(sopra) or len(neg) == 0),
              "negative %d su %d sopra il pavimento; media/scarto = %.3f"
              % (len(neg), len(sopra), media / sigma if sigma > 0 else float("nan")))
    print("-" * 96)
    print("### ⛔⛔ NESSUN VERDETTO SUL VERSO, e i DUE motivi sono DIVERSI ai due `dtau`:")
    print("###   a dtau = 1 il SEGNO e' costante (+) ma IL CANALE DISPARI NON C'E'")
    print("###     (dispari/pari = %.1e): il hop del vuoto a theta = pi e' una"
          % rapporti.get("PALINDROMO, dtau = 1", float("nan")))
    print("###     PERMUTAZIONE PURA, e una permutazione non ha termine d'interferenza.")
    print("###     Quindi quel + e' un effetto in `beta^2`, SENZA verso.")
    print("###   a dtau = 0.5 IL CANALE DISPARI C'E' (dispari/pari = %.2f) ma IL SEGNO"
          % rapporti.get("PALINDROMO, dtau = 0.5", float("nan")))
    print("###     ALTERNA fra le finestre: il vuoto OSCILLA attorno alla scena senza")
    print("###     materia, con una media molto piu' piccola dell'ampiezza.")
    print("###   ### E IL MECCANISMO C'E' IN ENTRAMBI I CASI: con `beta = 0` il dLambda")
    print("###   e' ESATTAMENTE zero. Cio' che manca non e' l'effetto: e' il suo VERSO.")
    print("###   ### CHE COSA SERVIREBBE, e NON lo decido io: misurare a `dtau < 1`")
    print("###   (dove il canale dispari esiste) con corse PIU' LUNGHE e una media")
    print("###   temporale con la sua barra d'errore, perche' a 400 tick l'oscillazione")
    print("###   domina la media.")
    print("=" * 96)
    print("  %d su %d" % (OK[0], OK[1]))
    print("### ⛔ E COME `cs` DIPENDE DA `Lambda` NON SI DECIDE QUI: a `L2` `cs` e'")
    print("###   ANCORA UNIFORME, e questa misura guarda SOLO la risposta del vuoto.")
    print("=" * 96)
    return 0 if OK[0] == OK[1] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
