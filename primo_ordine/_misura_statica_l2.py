# -*- coding: utf-8 -*-
r"""**LA RISPOSTA DEL VUOTO A UNA SORGENTE FERMA** — *`L2`, quarto pezzo.*

> **Mandato di Luca del 2026-10-15.** Il task history sta in
> `doc/TASK_HISTORY/2026-10-15_l2_risposta_statica.md`, ### **committato PRIMA di questo
> file.** ### ⛔ **Il motore NON si tocca, la tabella NON si tocca: tutto qui dentro.**

## ⛔ PERCHE' QUESTA MISURA ESISTE

### **La sorgente NON ERA FERMA** nei tre pezzi precedenti, e si disperde: ### **la
risposta di primo ordine di una sorgente che si muove si media a zero, e resta `beta^2`.**
### ⭐ **E la gravita' di una massa e' il suo campo STATICO.**

## ⛔⛔ LA SORGENTE CONGELATA E' UNO STRUMENTO DI MISURA, NON UNA LEGGE

### **E' la <<massa di prova>> della fisica:** un corpo che ### **genera il campo e non lo
subisce.** ### ⚠ **Viola la conservazione PER COSTRUZIONE** — la `rho` che il vuoto vede
### **non cambia mai** — e per questo ### **non puo' stare in nessuna tabella: vive in
questo file.**

### ⛔ **E IL MODO DI CONGELARE E' QUELLO DELL'INTEGRAZIONE DEL GUARDIANO** *(dopo
`e01e46f`)*: ### **il termine legge una FOTOGRAFIA FISSA di `rho`**, presa al tick `0`, in
### **entrambe le meta'** della saturazione — e `psi` ### **si ripristina a ogni tick.**
### 📌 **Il perche' sta in `_termine_statico`, e NON e' un'assunzione: e' misurato** dai
bracci `(3)` e `(3-bis)`. ### ⭐ **E il mio metodo di `e01e46f`** *(`rho` ricalcolata dalla
`psi` corrente)* ### **resta come CONTROLLO**: il braccio `(e)` riporta ### **la differenza
fra i due profili**, che e' cio' che il punto `2` dell'integrazione chiede.

## 📌 IL VERSO E' UNO SOLO, PER COSTRUZIONE

### **`materia -> vuoto`.** La retroazione ### **`vuoto -> materia` e' ESCLUSA dal
congelamento**, quindi ### ⛔ **questa misura non dice NIENTE sul verso opposto**, e un suo
risultato ### **non si puo' usare per affermare la bidirezionalita'.**

## ⚠ LE FORME E LA DENSITA' NON SI RIDEFINISCONO QUI

### **`_alpha_beta` e `densita_materia` si IMPORTANO da `_misura_forme_l2.py`:** le quattro
forme hanno ### **una sola definizione in tutto il repo**, e due copie divergerebbero
*(par.`9-ter`: a parita' di effetto si preferisce togliere, non aggiungere)*.

Gira con:  python primo_ordine/_misura_statica_l2.py
"""
import os
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
sys.path.insert(0, os.path.join(os.path.dirname(_QUI), "csv"))

OK = [0, 0]
# ### ⛔⛔ **LA CONFIGURAZIONE E LO STRUMENTO STANNO IN `statica_protocollo.py`**, e il
# ### motivo e- il tetto delle `700` righe: ### **oltre, SI DIVIDE.** ### **Qui restano LE
# ### MISURE**, cioe- i bracci e i loro verdetti.
import statica_protocollo as PR                               # noqa: E402
from statica_protocollo import (DTAU, FINESTRE, FORME, LATI, RAGGIO, SEME, SEP,
                                SOSTITUISCI, TICK, TICK_SCAN, TRANSITORIO,
                                T_ACCENSIONE, T_SCAN, ULTIMA, VUOTO, X_RIF, X_SCAN,
                                X_SOVR, barra, base, blocchi, corri, inizio_finestra,
                                metti_grumi, nodo_di, pezzo_del_passo, su_nodi)

def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    print("  %-58s %s   %s" % (che[:58], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()


# ============================================================== l'accensione e la scena
def braccio_base():
    print("-" * 96)
    print("### (1) IL VUOTO DI RIFERIMENTO su %s: senza sorgente, dev'essere STAZIONARIO"
          % (LATI,))
    for dtau in DTAU:
        lam, _dr, dtot, _per = base(dtau, TICK)
        d = float(np.max(np.abs(lam - lam[0])))
        esito("(1) vuoto libero fermo a dtau = %.2f" % dtau, d <= 1e-12,
              "max |Lambda(t) - Lambda(0)| = %.3e su %d tick, e la somma |phi|^2 deriva di"
              " %.3e" % (d, TICK, dtot))


def braccio_congelamento():
    print("-" * 96)
    print("### (2) IL CONGELAMENTO FA QUALCOSA? rho con e SENZA il ripristino")
    print("###     (senza questo braccio <<rho costante>> sarebbe un FALSO-ZERO:")
    print("###      e' costante perche' LO IMPONGO, e devo mostrare che altrimenti cambia)")
    import scena_l2 as SC
    per = SC.anelli(LATI, 0)
    d2 = np.zeros(LATI[0] * LATI[1], dtype=float)
    for d, nodi in per.items():
        d2[nodi] = float(d) ** 2
    for congela in ("tick", "no"):
        lam, drho, dtot, _p = corri(0.5, X_RIF, "S1", 400, 0, (0,), congela=congela)
        esito("(2) ripristino %s: max |rho(t) - rho(0)|"
              % ("a ogni TICK" if congela == "tick" else "SPENTO"),
              (drho == 0.0) if congela == "tick" else (drho > 1e-3),
              "%.3e su 400 tick  (atteso: %s)"
              % (drho, "ESATTAMENTE 0" if congela == "tick" else
                 "> 1e-3, cioe' la sorgente SI MUOVE"))
        # ### la larghezza, dal canale laterale `ULTIMA`, letta SUBITO dopo la corsa
        r0, r1 = ULTIMA["rho0"], ULTIMA["rho_fine"]
        print("      larghezza di rho (raggio quadratico medio): t=0 %.4f   t=400 %.4f"
              % (float(np.sqrt(np.sum(d2 * r0) / np.sum(r0))),
                 float(np.sqrt(np.sum(d2 * r1) / np.sum(r1)))))
        sys.stdout.flush()


def braccio_alpha():
    """### **(3) `alpha` conta?** — *la previsione, il controllo, e DOVE nasce.*"""
    print("-" * 96)
    print("### (3) alpha NON PUO' CONTARE: col metodo della FOTOGRAFIA deve valere AL BIT")
    print("###     e col MIO metodo (rho corrente) il mandato non lo garantiva: si misura")
    print("###     la differenza, e si dice A QUALE delle due applicazioni per tick nasce.")
    for forma in ("S1", "S2"):
        for sorgente in ("foto", "corrente"):
            a, _d1, _t1, _p = corri(0.5, X_RIF, forma, 200, 0, (0,), sorgente=sorgente)
            b, _d2, _t2, _p2 = corri(0.5, X_RIF, forma, 200, 0, (0,), senza_alpha=True,
                                     sorgente=sorgente)
            d = float(np.max(np.abs(a - b)))
            if sorgente == "foto":
                esito("(3) %s FOTO: alpha = 0 da' lo STESSO Lambda(t)" % forma, d == 0.0,
                      "max |differenza| = %.3e su 200 tick  (0 = identico AL BIT)" % d)
            else:
                print("      %s rho CORRENTE: max |differenza| = %.3e   <- il mio metodo"
                      " di e01e46f" % (forma, d))
                sys.stdout.flush()
    # ### ⭐ **(3-bis) E DOVE NASCE: la saturazione agisce DUE volte per tick** *(ordine
    # ### PALINDROMO)*, e fra le due girano ### **Grover e spostamento su `psi`.** Quindi
    # ### con `rho` corrente la ### **SECONDA** meta- legge una `rho` spostata.
    # ### ✅ **Si misura `rho` COME IL TERMINE LA VEDE, chiamata per chiamata.**
    import composizione as CM
    quante = sum(1 for idl, _f, _t in CM.ORDINE if idl == pezzo_del_passo())
    esito("(3-bis) la saturazione agisce DUE volte per tick", quante == 2,
          "%d applicazioni in composizione.ORDINE su %d pezzi: e' il PALINDROMO"
          % (quante, len(CM.ORDINE)))
    for sorgente in ("corrente", "foto"):
        vA, vB = [], []
        corri(0.5, X_RIF, "S2", 3, 0, (0,), visto=vA, sorgente=sorgente)
        corri(0.5, X_RIF, "S2", 3, 0, (0,), senza_alpha=True, visto=vB, sorgente=sorgente)
        sc = [float(np.max(np.abs(x - y))) for x, y in zip(vA, vB)]
        print("      %-9s rho vista dal termine, chiamata per chiamata (3 tick):"
              " %s" % (sorgente, "  ".join("#%d %.1e" % (i + 1, s)
                                           for i, s in enumerate(sc))))
        sys.stdout.flush()
        if sorgente == "corrente":
            esito("(3-bis) con rho CORRENTE la differenza nasce alla SECONDA"
                  " applicazione", len(sc) >= 2 and sc[0] == 0.0 and sc[1] > 0.0,
                  "chiamata 1: %.1e (identica)   chiamata 2: %.1e (diversa)"
                  % (sc[0], sc[1]) if len(sc) >= 2 else "meno di 2 chiamate")
        else:
            esito("(3-bis) con la FOTOGRAFIA ogni chiamata vede la STESSA rho",
                  all(s == 0.0 for s in sc),
                  "massimo su %d chiamate: %.1e" % (len(sc), max(sc) if sc else 0.0))
    # ### ✅ **(3-ter) E con la fotografia il RIPRISTINO di `psi` non conta per il vuoto:**
    # ### se la saturazione e- ### **l-unico canale `materia -> vuoto`**, allora
    # ### ### **`psi` LIBERA deve dare lo stesso `Lambda(t)` AL BIT.**
    a, _d1, _t1, _p = corri(0.5, X_RIF, "S1", 200, 0, (0,))
    b, _d2, _t2, _p2 = corri(0.5, X_RIF, "S1", 200, 0, (0,), congela="no")
    d = float(np.max(np.abs(a - b)))
    esito("(3-ter) FOTO: psi LIBERA da' lo stesso Lambda(t) AL BIT", d == 0.0,
          "max |differenza| = %.3e -> la saturazione E' l'unico canale materia->vuoto" % d)


def braccio_nullo():
    print("-" * 96)
    print("### (4) IL CONTROLLO NULLO: beta = 0 -> dLambda = 0 esatto")
    for dtau in DTAU:
        b, _d, _t, _p = base(dtau, 200)
        a, _d2, _t2, _p2 = corri(dtau, X_RIF, "S1", 200, 0, (0,), beta_zero=True)
        d = float(np.max(np.abs(a - b)))
        esito("(4) beta = 0 a dtau = %.2f" % dtau, d <= 1e-14,
              "max |dLambda| = %.3e su 200 tick" % d)


# ====================================================================== le quattro domande
def braccio_segno():
    """### **(a) IL SEGNO** di `dLambda` sulla sorgente, e ### **(d) il PROFILO.**"""
    print("-" * 96)
    print("### (a) IL SEGNO di dLambda sulla sorgente, e per TRE accensioni")
    print("###     x = %.2f   %d tick   finestra da T+%d   %d blocchi"
          % (X_RIF, TICK, TRANSITORIO, FINESTRE))
    fuori = {}
    conservazione = 0.0
    for forma in FORME:
        for dtau in DTAU:
            for acceso in T_ACCENSIONE:
                t0 = time.time()
                b, _dr, _dt, per = base(dtau, TICK)
                a, drho, dtot, _p = corri(dtau, X_RIF, forma, TICK, acceso, (0,))
                conservazione = max(conservazione, dtot)
                prof = blocchi(a - b, inizio_finestra(acceso), FINESTRE)
                dentro = [v for d, nodi in per.items() if d <= RAGGIO for v in nodi]
                m, s = su_nodi(prof, dentro)
                tutti = list(range(prof.shape[1]))
                mt, _st = su_nodi(prof, tutti)
                fuori[(forma, dtau, acceso)] = (m, s, prof, per, dentro)
                print("  %s dtau=%.2f T=%-4d  dLambda = %+.6e +- %.3e (%.1f barre)"
                      "   somma-nodi %+.2e   rho fermo %.1e   [%.1f s]"
                      % (forma, dtau, acceso, m, s, abs(m) / s if s > 0 else float("nan"),
                         mt, drho, time.time() - t0))
                sys.stdout.flush()
    esito("(9) la somma di |phi|^2 e' CONSERVATA in ogni corsa",
          conservazione <= 1e-9,
          "deriva massima %.3e su tutte le corse del braccio (a)" % conservazione)
    return fuori


def braccio_profilo(segno):
    """### **(d) IL PROFILO in distanza** — *senza adattarlo a una legge.*"""
    print("-" * 96)
    print("### (d) IL PROFILO in distanza: dLambda(r) per anelli, e DOVE cambia segno")
    print("###     ⛔ NON lo adatto a log r: il mandato lo vieta, e un profilo si guarda")
    print("###        PRIMA di sceglierne la legge.")
    for forma in FORME:
        for dtau in DTAU:
            ch = (forma, dtau, T_SCAN)
            if ch not in segno:
                continue
            _m, _s, prof, per, _d = segno[ch]
            righe = []
            cambio = None
            primo = None
            for d in sorted(per):
                mm, ss = su_nodi(prof, per[d])
                if primo is None:
                    primo = mm
                if cambio is None and primo is not None and mm * primo < 0:
                    cambio = d
                if d <= 8 or d % 4 == 0:
                    righe.append("r=%-2d %+.3e+-%.1e" % (d, mm, ss))
            print("  %s dtau=%.2f  %s" % (forma, dtau, "  ".join(righe[:7])))
            print("      %s   cambio di segno a r = %s"
                  % ("  ".join(righe[7:]), cambio if cambio is not None else "MAI"))
            sys.stdout.flush()


def braccio_due_metodi():
    """### **Il punto `2` dell'integrazione: i DUE metodi, e la differenza dei profili.**"""
    print("-" * 96)
    print("### (e) I DUE METODI A CONFRONTO: fotografia FISSA di rho contro rho CORRENTE")
    print("###     (il secondo e' il mio metodo di e01e46f: la sorgente ferma SOLO ai")
    print("###      confini dei tick. Se la differenza e' piccola, il prezzo che avevo")
    print("###      dichiarato era trascurabile; se no, conta la FOTOGRAFIA.)")
    for forma in FORME:
        dtau = DTAU[0]
        b, _dr, _dt, per = base(dtau, TICK_SCAN)
        ini = inizio_finestra(T_SCAN)
        pr = {}
        for sorgente in ("foto", "corrente"):
            a, _d2, _t2, _p = corri(dtau, X_RIF, forma, TICK_SCAN, T_SCAN, (0,),
                                    sorgente=sorgente)
            pr[sorgente] = blocchi(a - b, ini, FINESTRE)
        dentro = [vv for d, nodi in per.items() if d <= RAGGIO for vv in nodi]
        mf, sf = su_nodi(pr["foto"], dentro)
        mc, sc = su_nodi(pr["corrente"], dentro)
        # ### il profilo per anelli, e lo scarto FRA I DUE PROFILI
        rf = np.array([np.mean(np.mean(pr["foto"], axis=0)[per[d]]) for d in sorted(per)])
        rc = np.array([np.mean(np.mean(pr["corrente"], axis=0)[per[d]])
                       for d in sorted(per)])
        rel = (np.linalg.norm(rf - rc) / np.linalg.norm(rf)) if np.any(rf) else float("nan")
        print("  %s dtau=%.2f  sorgente: FOTO %+.4e +- %.1e   CORRENTE %+.4e +- %.1e"
              % (forma, dtau, mf, sf, mc, sc))
        print("      e lo scarto FRA I DUE PROFILI dLambda(r): %.4f relativo"
              " (su %d anelli)   stesso segno: %s"
              % (rel, rf.size, "SI'" if mf * mc > 0 else "### NO"))
        sys.stdout.flush()


def braccio_linearita():
    """### **(b) LA LINEARITA'**: pendenza `log`-`log` di `|dLambda|` in `x`."""
    print("-" * 96)
    print("### (b) LA LINEARITA' in x: pendenza log-log di |dLambda| sulla sorgente")
    print("###     x = %s   %d tick   T = %d   finestra da %d"
          % (X_SCAN, TICK_SCAN, T_SCAN, inizio_finestra(T_SCAN)))
    print("###     ATTESO se la risposta statica e' LINEARE in beta:")
    print("###       S1 ~ 3   S2 ~ 1   S3 ~ 1   S4 ~ 1.64   (l'esponente di beta)")
    print("###     e il DOPPIO se la risposta e' quadratica, come nei tre pezzi precedenti.")
    fuori = {}
    for forma in FORME:
        for dtau in DTAU:
            vals, barre = [], []
            b, _dr, _dt, per = base(dtau, TICK_SCAN)
            dentro = [v for d, nodi in per.items() if d <= RAGGIO for v in nodi]
            for x in X_SCAN:
                a, _d2, _t2, _p = corri(dtau, x, forma, TICK_SCAN, T_SCAN, (0,))
                prof = blocchi(a - b, inizio_finestra(T_SCAN), FINESTRE)
                m, s = su_nodi(prof, dentro)
                vals.append(m)
                barre.append(s)
            pend = []
            for i in range(len(X_SCAN) - 1):
                v1, v2 = vals[i], vals[i + 1]
                # ### ⛔ **la pendenza si legge solo se il SEGNO non cambia e i due valori
                # ### sono FUORI dalla loro barra:** altrimenti e- rumore, e un esponente
                # ### letto sul rumore ### **e- un numero senza provenienza.**
                if (v1 * v2 > 0 and abs(v1) > barre[i] and abs(v2) > barre[i + 1]):
                    pend.append("[%g->%g] %.3f"
                                % (X_SCAN[i], X_SCAN[i + 1],
                                   np.log(abs(v2) / abs(v1))
                                   / np.log(X_SCAN[i + 1] / X_SCAN[i])))
            fuori[(forma, dtau)] = (vals, barre, pend)
            print("  %s dtau=%.2f  dLambda: %s"
                  % (forma, dtau,
                     "  ".join("%g:%+.2e" % (x, v) for x, v in zip(X_SCAN, vals))))
            print("      pendenze LOCALI: %s"
                  % ("  ".join(pend) if pend else "### NON LEGGIBILE (segno che cambia o"
                     " valori dentro la barra)"))
            sys.stdout.flush()
    return fuori


def braccio_sovrapposizione():
    """### **(c) LA SOVRAPPOSIZIONE**: `dL(A+B)` contro `dL(A) + dL(B)`, nodo per nodo."""
    print("-" * 96)
    nb = nodo_di(LATI, (SEP, 0))
    print("### (c) LA SOVRAPPOSIZIONE: due sorgenti a distanza %d (nodi 0 e %d)"
          % (SEP, nb))
    print("###     dLambda(A+B) contro dLambda(A) + dLambda(B), NODO PER NODO")
    for forma in FORME:
        for dtau in DTAU:
          for xs in X_SOVR:
            b, _dr, _dt, per = base(dtau, TICK_SCAN)
            ini = inizio_finestra(T_SCAN)
            pr = {}
            for nome, centri in (("A", (0,)), ("B", (nb,)), ("AB", (0, nb))):
                a, _d2, _t2, _p = corri(dtau, xs, forma, TICK_SCAN, T_SCAN, centri)
                pr[nome] = blocchi(a - b, ini, FINESTRE)
            somma = pr["A"] + pr["B"]
            resto = pr["AB"] - somma
            # ### la norma per blocco, cosi- la barra viene dai BLOCCHI
            nr = np.sqrt(np.sum(resto ** 2, axis=1))
            ns = np.sqrt(np.sum(somma ** 2, axis=1))
            rel = nr / np.where(ns > 0, ns, np.nan)
            mr, sr = barra(rel)
            pmax = float(np.max(np.abs(np.mean(resto, axis=0)))
                         / max(float(np.max(np.abs(np.mean(somma, axis=0)))), 1e-300))
            print("  %s dtau=%.2f x=%.2f  scarto relativo = %.4f +- %.4f"
                  "   (nodo peggiore %.4f)" % (forma, dtau, xs, mr, sr, pmax))
            sys.stdout.flush()


# ====================================================================== il giro
def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    t0 = time.time()
    print("=" * 96)
    print("LA RISPOSTA DEL VUOTO A UNA SORGENTE FERMA -- L2, quarto pezzo.")
    print("### LA SORGENTE CONGELATA E' UNO STRUMENTO (la <<massa di prova>>), NON UNA")
    print("### LEGGE: viola la conservazione PER COSTRUZIONE, e non entra in nessuna")
    print("### tabella. IL MOTORE NON SI TOCCA.")
    print("=" * 96)
    print("  LA CONFIGURAZIONE: toro %s = %d nodi   TICK = %d (%d nella scansione)"
          % (LATI, LATI[0] * LATI[1], TICK, TICK_SCAN))
    print("  accensioni T = %s (0 = DI COLPO)   transitorio = %d   finestre = %d"
          % (T_ACCENSIONE, TRANSITORIO, FINESTRE))
    print("  dtau = %s   x = %s   x del verso = %.2f   separazione = %d"
          % (DTAU, X_SCAN, X_RIF, SEP))
    print("  raggio = %d   seme = %d   vuoto = %.1f   forme = %s"
          % (RAGGIO, SEME, VUOTO, FORME))
    print("  ### IL CONGELAMENTO: psi si RIPRISTINA a ogni tick (scelta DICHIARATA).")
    print("  ### CORSA LUNGA: sta FUORI dal pre-commit, come misura DICHIARATA.")
    sys.stdout.flush()
    braccio_base()
    braccio_congelamento()
    braccio_alpha()
    braccio_nullo()
    segno = braccio_segno()
    braccio_profilo(segno)
    braccio_due_metodi()
    braccio_linearita()
    braccio_sovrapposizione()
    print("=" * 96)
    print("### IL VERDETTO SUL SEGNO, forma per forma (accensione T = %d)" % T_SCAN)
    for forma in FORME:
        for dtau in DTAU:
            ch = (forma, dtau, T_SCAN)
            if ch not in segno:
                continue
            m, s = segno[ch][0], segno[ch][1]
            barre = abs(m) / s if s > 0 else float("nan")
            esito("(a) %s a dtau=%.2f: dLambda fuori da 3 barre" % (forma, dtau),
                  barre >= 3.0,
                  "dLambda = %+.4e +- %.3e (%.1f barre) -> %s"
                  % (m, s, barre,
                     ("il vuoto si ACCUMULA" if m > 0 else "il vuoto SI RITIRA")
                     if barre >= 3 else "indeciso"))
    print("=" * 96)
    print("  %d su %d   [corsa intera: %.1f s]" % (OK[0], OK[1], time.time() - t0))
    print("### ⛔ E LA FORMA NON SI DECIDE QUI: la tabella NON e' toccata, e la scelta")
    print("###   fra S1-S4 (o altro) e' di Luca, coi numeri di questa misura.")
    print("### ⛔ E IL VERSO E' UNO SOLO (materia -> vuoto): il congelamento ESCLUDE la")
    print("###   retroazione, quindi questa misura non dice niente sul verso opposto.")
    print("=" * 96)
    return 0 if OK[0] == OK[1] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
