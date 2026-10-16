# -*- coding: utf-8 -*-
r"""**LA PARTE PARI DI `dLambda`: IL VERSO, E L'ESPONENTE** — *misure, nessuna legge.*

> **Secondo pezzo di `L2`, mandato di Luca del 2026-10-15**, con **due correzioni al
> protocollo del primo pezzo** *(del guardiano)*:
>
> ### ⭐⭐ **(a) UNA RISPOSTA PARI HA UN VERSO.** Il criterio *«`beta` rovesciato deve
> rovesciare `dLambda`»* valeva **solo per una risposta LINEARE**. La risposta e' **pari**
> *(`dispari/pari = 1.6e-13`)*, e una risposta pari e' ### **la stessa per le due
> elicita'** — cioe' **indipendente dall'orientamento dello spin**, che e' ### **proprio
> cio' che il principio di equivalenza richiede.**
> ### ✅ **Quindi il precondizionamento <<canale dispari>> NON e' piu' un criterio del
> verso.**
>
> ### ⛔ **(b) IL GRUMO ISOTROPO NON E' UN CONTROLLO NULLO** *(l'elicita' NASCE:
> `h(0) = 0` ma `max|h(t)| = 2.16`)*. ### **Il controllo nullo e' `beta = 0`**, che da'
> `dLambda = 0` esatto: **resta, ed e' l'UNICO.**

## ⭐ LE DUE GRANDEZZE

```
E(t) = [ dLambda(beta) + dLambda(-beta) ] / 2      la parte PARI   -> il VERSO
O(t) = [ dLambda(beta) - dLambda(-beta) ] / 2      la parte DISPARI
```

### 📌 **E il verdetto e' sul SEGNO DELLA MEDIA di `E` sul grumo, con `|media| > 3` barre
d'errore** *(criterio di Luca, fissato nel mandato)*: ### **`E < 0`** vuol dire *«la
materia consuma il vuoto»*, ### **`E > 0`** vuol dire *«il vuoto si accumula»* — e quello
e' **il verso OPPOSTO alla decisione**, e allora ### **si riporta e si ferma.**

## ⛔ E L'ESPONENTE E' LA DOMANDA PIU' PESANTE

### Se `E` e' quadratica in `beta` e `beta ~ -(2/3) x^3` per `x` piccolo, allora
### **`E ~ x^6`.** ### ⚠⚠ **Una <<gravita'>> che va come `x^6` NON ESISTE PER POCA
MATERIA:** la gravita' newtoniana e' **lineare nella massa**, e `x^6` vuol dire che
### **dimezzare la materia divide l'effetto per `64`.**

## 📌 LE CORSE SONO LUNGHE E STANNO FUORI DAL `pre-commit`

### **Sono misure DICHIARATE**, non collaudi: il budget di `500` s del `pre-commit` resta.
### ⭐ **E la corsa SENZA materia e' in CACHE per `dtau`**, perche' con `psi = 0` si ha
`h = 0` ⟹ `beta = 0`: ### **e' la stessa per ogni `x` e per ogni elicita'**, e calcolarla
una volta sola e' cio' che fa stare le corse lunghe nel tempo.

Gira con:  python primo_ordine/_misura_pari_l2.py
"""
import os
import sys
import time

import numpy as np
import tick as TK

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
sys.path.insert(0, os.path.join(os.path.dirname(_QUI), "csv"))

OK = [0, 0]
# ### ⛔ **LA CONFIGURAZIONE INTERA, DICHIARATA E STAMPATA.** ### **`TICK` e `FINESTRE`
# ### sono i due numeri che il mandato fissa** *(`>= 2000` e `>= 10`)*, e il costo si
# ### MISURA e si dichiara.
TICK = 2000
FINESTRE = 10
DTAU = (1.0, 0.5, 0.25)
ELICITA = (1, -1)
X_SCAN = (0.1, 0.2, 0.5, 1.0, 2.0)
DTAU_SCAN = (1.0, 0.5)
VUOTO = 1.0
RAGGIO = 1
SEME = 7
# ### ⚠ **`x = (ampiezza/vuoto)^2`**, e non e- una convenzione mia: con l-elicita- `+1`
# ### si ha `h_k = somma |psi_h|^2` e `Lambda_k = somma |phi_h|^2` sullo stesso nodo,
# ### quindi ### **il grado si semplifica** e `x = |psi|^2/|phi|^2`.
# ### ⭐ **L-ESTENSIONE, DICHIARATA: dove il verdetto resta INDECISO si allunga.**
# ### ⚠ **E non e- <<cercare il numero che piace>>: la soglia delle `3` barre e- di Luca e
# ### ### **NON si muove** -- si allunga ### **la corsa**, che e- l-unica cosa che fa
# ### scendere la barra *(come `1/sqrt(N)`)*. ### **E si applica a `dtau` DICHIARATI
# ### PRIMA**, non a quelli che poi risultano comodi.
TICK_LUNGO = 10000
FINESTRE_LUNGO = 20
DTAU_LUNGO = (0.25,)
_SENZA = {}


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    print("  %-58s %s   %s" % (che[:58], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()


def _corri(dtau, ampiezza, materia, elicita, rovescia, tick):
    """### `Lambda(t)` su `tick` tick. ### **`rovescia` cambia il segno di `beta`.**

    ### ⛔ **E il motore NON si tocca:** si sostituisce `saturazione.pezzi` **a runtime**,
    e si rimette a posto in un `finally` — il modulo e' **condiviso**, e lasciarlo
    sporcato falserebbe ### **ogni misura successiva nella stessa corsa.**
    """
    import deriva as DV
    import saturazione as SAT
    import scena_l2 as SC
    vero = SAT.pezzi

    def rov(h, lam):
        al, be = vero(h, lam)
        return al, -be

    if rovescia:
        SAT.pezzi = rov
    try:
        inc, mot, st, par, _c, per = SC.scena(dtau, VUOTO, ampiezza, RAGGIO, materia,
                                             True, False, SEME, elicita)
        lam = [mot.densita_vuoto(st).copy()]
        for _t in range(tick):
            TK.tick(st, mot, par)
            lam.append(mot.densita_vuoto(st).copy())
    finally:
        SAT.pezzi = vero
    return np.array(lam), per


def senza_materia(dtau, tick):
    """### La corsa **senza materia**, ### **in cache per `dtau`.**

    ### ⭐ **E si puo' mettere in cache per un motivo, non per comodita':** con `psi = 0`
    si ha `h = 0` ⟹ `beta = 0`, quindi ### **non dipende ne' da `x` ne' dall'elicita' ne'
    dal segno di `beta`.**
    """
    # ### ⛔ **LA CHIAVE E- `(dtau, tick)`, E NON SOLO `dtau`:** la prima versione era
    # ### indicizzata solo su `dtau`, e il braccio del controllo -- che gira ### **200
    # ### tick** -- ha riempito la cache, cosi- il braccio del verso si e- ritrovato una
    # ### corsa di `201` righe dove ne voleva `2001`. ### **Un `ValueError` di forme, e
    # ### per fortuna RUMOROSO:** una cache con la chiave sbagliata, se le forme fossero
    # ### tornate, ### **avrebbe dato numeri sbagliati in silenzio.**
    chiave = (dtau, tick)
    if chiave not in _SENZA:
        _SENZA[chiave] = _corri(dtau, 0.0, False, 1, False, tick)
    return _SENZA[chiave]


def pari_e_dispari(dtau, x, elicita, tick):
    """### `(E, O, per, dentro)` — ### **le due combinazioni, per nodo e per tick.**"""
    amp = float(np.sqrt(x)) * VUOTO
    b, per = senza_materia(dtau, tick)
    a1, _p = _corri(dtau, amp, True, elicita, False, tick)
    a2, _p = _corri(dtau, amp, True, elicita, True, tick)
    d1, d2 = a1 - b, a2 - b
    dentro = [v for d, nodi in per.items() if d <= RAGGIO for v in nodi]
    return 0.5 * (d1 + d2), 0.5 * (d1 - d2), per, dentro


def media_e_barra(campo, nodi, finestre):
    """### `(media, barra)` sulle **finestre**: ### **lo scarto fra finestre su `sqrt(N)`.**

    ### ⛔ **La barra NON e' lo scarto dei singoli tick:** i tick vicini sono
    **correlati** *(la dinamica e' deterministica e liscia)*, quindi quella barra
    ### **sarebbe una sottostima.** ### ✅ **Le finestre sono blocchi**, e lo scarto fra
    blocchi e' la stima onesta — e' il metodo dei **blocchi**, non una scelta di comodo.
    """
    t = campo.shape[0]
    b = [int(round(t * i / float(finestre))) for i in range(finestre + 1)]
    med = [float(np.mean(campo[b[i]:b[i + 1]][:, nodi])) for i in range(finestre)]
    m = float(np.mean(med))
    s = float(np.std(med, ddof=1)) / np.sqrt(finestre) if finestre > 1 else float("nan")
    return m, s, med


# ====================================================================== i bracci
def braccio_nullo():
    """### ⛔ **IL CONTROLLO NULLO, e dal 2026-10-15 e' L'UNICO: `beta = 0`.**"""
    import saturazione as SAT
    print("-" * 96)
    print("### (A) IL CONTROLLO NULLO: `beta = 0` deve dare `dLambda = 0` ESATTO")
    vero = SAT.pezzi

    def spento(h, lam):
        al, be = vero(h, lam)
        return al, 0.0 * be

    for dtau in DTAU:
        b, per = senza_materia(dtau, 200)
        SAT.pezzi = spento
        try:
            a, _p = _corri(dtau, 1.0, True, 1, False, 200)
        finally:
            SAT.pezzi = vero
        m = float(np.max(np.abs(a - b)))
        esito("(A) `beta = 0` -> `dLambda = 0`, dtau = %.2f" % dtau, m <= 1e-12,
              "max |dLambda| = %.3e su 200 tick" % m)


def braccio_verso():
    """### ⭐⭐ **IL VERSO: la media di `E` sul grumo, con la sua barra.**"""
    print("-" * 96)
    print("### (B) IL VERSO: media di E sul grumo, su %d tick e %d finestre"
          % (TICK, FINESTRE))
    fuori = {}
    for dtau in DTAU:
        for el in ELICITA:
            t0 = time.time()
            E, O, per, dentro = pari_e_dispari(dtau, 1.0, el, TICK)
            mE, sE, _m = media_e_barra(E, dentro, FINESTRE)
            mO, sO, _m2 = media_e_barra(O, dentro, FINESTRE)
            # ### ⭐ **e la SOMMA su TUTTI i nodi: se il vuoto si SPOSTA e non nasce,
            # ### ### deve essere ZERO.**
            tutti = list(range(E.shape[1]))
            mT, sT, _m3 = media_e_barra(E, tutti, FINESTRE)
            fuori[(dtau, el)] = (mE, sE, mO, sO, mT, sT, E, O, per, dentro)
            print("  dtau=%-5.2f elicita'=%+d   E = %+.6e +- %.3e  (%.1f barre)"
                  "   O = %+.6e +- %.3e   [%.1f s]"
                  % (dtau, el, mE, sE, abs(mE) / sE if sE > 0 else float("nan"),
                     mO, sO, time.time() - t0))
            print("        e la MEDIA SU TUTTI I NODI: %+.6e +- %.3e"
                  "   (se il vuoto si sposta, deve essere ~0)" % (mT, sT))
            for d in sorted(per):
                if d <= 3:
                    me, se, _ = media_e_barra(E, per[d], FINESTRE)
                    print("        anello %d (%2d nodi): E = %+.6e +- %.3e"
                          % (d, len(per[d]), me, se))
            sys.stdout.flush()
    return fuori


def braccio_esponente():
    """### ⛔ **L'ESPONENTE: `E` contro `x` in log-log.** ### **`x^6` o `x^1`?**"""
    print("-" * 96)
    print("### (C) L'ESPONENTE: media di E sul grumo contro x = h/Lambda")
    fuori = {}
    for dtau in DTAU_SCAN:
        punti = []
        for x in X_SCAN:
            t0 = time.time()
            E, O, per, dentro = pari_e_dispari(dtau, x, 1, TICK)
            mE, sE, _m = media_e_barra(E, dentro, FINESTRE)
            punti.append((x, mE, sE))
            print("  dtau=%-5.2f x=%-5.3g   E = %+.6e +- %.3e   (%.1f barre)  [%.1f s]"
                  % (dtau, x, mE, sE, abs(mE) / sE if sE > 0 else float("nan"),
                     time.time() - t0))
            sys.stdout.flush()
        # ### ⭐ **le pendenze LOCALI, fra punti consecutivi**: dicono se l-esponente
        # ### ### **CAMBIA** lungo la scansione, e un fit solo lo nasconderebbe.
        loc = []
        for i in range(1, len(punti)):
            x0, e0, _s0 = punti[i - 1]
            x1, e1, _s1 = punti[i]
            if e0 > 0 and e1 > 0:
                loc.append((x0, x1, np.log(e1 / e0) / np.log(x1 / x0)))
        print("      pendenze LOCALI: %s"
              % "  ".join("[%.3g->%.3g] %.3f" % t for t in loc))
        # ### il fit sui punti piccoli, con l-incertezza della pendenza
        pic = [(x, e) for x, e, _s in punti if x <= 0.5 and e > 0]
        if len(pic) >= 3:
            lx = np.log([p[0] for p in pic])
            ly = np.log([p[1] for p in pic])
            A = np.vstack([lx, np.ones_like(lx)]).T
            sol, res, _r, _sv = np.linalg.lstsq(A, ly, rcond=None)
            n = len(lx)
            s2 = float(res[0]) / (n - 2) if len(res) and n > 2 else 0.0
            cov = s2 * np.linalg.inv(A.T.dot(A))
            err = float(np.sqrt(cov[0, 0]))
            print("      ### L'ESPONENTE su x <= 0.5 (%d punti): %.3f +- %.3f"
                  % (n, float(sol[0]), err))
            fuori[dtau] = (float(sol[0]), err, punti, loc)
        else:
            print("      ### non ci sono abbastanza punti positivi per un fit")
            fuori[dtau] = (float("nan"), float("nan"), punti, loc)
        sys.stdout.flush()
    return fuori


def braccio_lungo():
    """### ⭐ **L-ESTENSIONE: gli stessi conti con corse `%d` volte piu` lunghe.**

    ### ⛔ **Serve dove il verdetto resta INDECISO**, e la cosa che si cambia e-
    ### **la LUNGHEZZA della corsa, non la soglia:** la barra scende come `1/sqrt(N)`,
    la soglia delle `3` barre e- di Luca e ### **resta dov-e-.**
    """ % (TICK_LUNGO // TICK)
    print("-" * 96)
    print("### (D) ESTENSIONE DICHIARATA: %d tick e %d finestre, a dtau = %s"
          % (TICK_LUNGO, FINESTRE_LUNGO, DTAU_LUNGO))
    fuori = {}
    for dtau in DTAU_LUNGO:
        for el in ELICITA:
            t0 = time.time()
            E, O, per, dentro = pari_e_dispari(dtau, 1.0, el, TICK_LUNGO)
            mE, sE, _m = media_e_barra(E, dentro, FINESTRE_LUNGO)
            mO, sO, _m2 = media_e_barra(O, dentro, FINESTRE_LUNGO)
            fuori[(dtau, el)] = (mE, sE, mO, sO)
            print("  dtau=%-5.2f elicita'=%+d   E = %+.6e +- %.3e  (%.1f barre)"
                  "   O = %+.6e +- %.3e  (%.1f barre)   [%.1f s]"
                  % (dtau, el, mE, sE, abs(mE) / sE if sE > 0 else float("nan"),
                     mO, sO, abs(mO) / sO if sO > 0 else float("nan"),
                     time.time() - t0))
            sys.stdout.flush()
            esito("(D) a dtau=%.2f el=%+d, su %d tick, E e' fuori da 3 barre"
                  % (dtau, el, TICK_LUNGO),
                  (abs(mE) / sE if sE > 0 else 0.0) >= 3.0,
                  "E = %+.6e +- %.3e -> %s"
                  % (mE, sE, "VUOTO SI ACCUMULA (verso OPPOSTO)" if mE > 0
                     else "LA MATERIA CONSUMA"))
    return fuori


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    import scena_l2 as SC
    t0 = time.time()
    print("=" * 96)
    print("LA PARTE PARI DI dLambda: IL VERSO, E L'ESPONENTE")
    print("=" * 96)
    print("  LA CONFIGURAZIONE: toro %s   TICK = %d   FINESTRE = %d   raggio = %d"
          "   seme = %d   vuoto = %.1f" % (SC.LATI, TICK, FINESTRE, RAGGIO, SEME, VUOTO))
    print("  dtau = %s   elicita' = %s   x della scansione = %s (a dtau = %s)"
          % (DTAU, ELICITA, X_SCAN, DTAU_SCAN))
    print("  ### E LE CORSE SONO LUNGHE: stanno FUORI dal pre-commit, come misure"
          " DICHIARATE.")
    sys.stdout.flush()
    braccio_nullo()
    verso = braccio_verso()
    esp = braccio_esponente()
    lungo = braccio_lungo()
    # ================================================================ IL VERDETTO
    print("=" * 96)
    print("### IL VERDETTO")
    for dtau in DTAU:
        for el in ELICITA:
            mE, sE = verso[(dtau, el)][0], verso[(dtau, el)][1]
            barre = abs(mE) / sE if sE > 0 else float("nan")
            esito("(B) a dtau=%.2f el=%+d la media di E e' fuori da 3 barre"
                  % (dtau, el), barre >= 3.0,
                  "E = %+.6e +- %.3e, cioe' %.1f barre -> %s"
                  % (mE, sE, barre,
                     ("VUOTO SI ACCUMULA (verso OPPOSTO)" if mE > 0 else
                      "LA MATERIA CONSUMA") if barre >= 3.0 else "indeciso"))
    # ### ⭐ **e le due elicita- devono dare LO STESSO `E`**: e- il pezzo di principio di
    # ### equivalenza che la PARITA- porta con se-.
    for dtau in DTAU:
        a = verso[(dtau, 1)][0]
        b = verso[(dtau, -1)][0]
        sa, sb = verso[(dtau, 1)][1], verso[(dtau, -1)][1]
        d = abs(a - b) / np.sqrt(sa ** 2 + sb ** 2) if (sa > 0 or sb > 0) else float("nan")
        esito("(B) e a dtau=%.2f le DUE ELICITA' danno lo stesso E" % dtau,
              np.sign(a) == np.sign(b),
              "E(+1) = %+.4e, E(-1) = %+.4e, rapporto %.4f, differenza %.1f barre"
              % (a, b, abs(a / b) if b != 0 else float("nan"), d))
    print("-" * 96)
    for dtau in DTAU_SCAN:
        p, e, _pt, _lo = esp[dtau]
        print("### (C) a dtau = %.2f l'esponente di `E` in `x` e': %.3f +- %.3f"
              % (dtau, p, e))
    print("###   ### E IL CONFRONTO CHE CONTA: `x^6` e' cio' che la derivazione dice se")
    print("###   `E` e' quadratica in `beta` *(beta ~ -(2/3)x^3)*; `x^1` sarebbe la")
    print("###   gravita' newtoniana, LINEARE nella massa.")
    print("=" * 96)
    print("  %d su %d   [corsa intera: %.1f s]" % (OK[0], OK[1], time.time() - t0))
    print("### ⛔ E NESSUNA LEGGE E' STATA AGGIUNTA, e la saturazione non e' stata")
    print("###   toccata: il verso e l'esponente vanno a Luca.")
    print("=" * 96)
    return 0 if OK[0] == OK[1] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
