# -*- coding: utf-8 -*-
"""DOVE SPINGE LA GRAVITA': il saldo di `S09` PER REGIONE, e i 20 archi piu' spinti. [G2]

⚠ SOLA MISURA. Nessuna cura, nessuna modifica al simulatore ne' al driver.

PERCHE' ESISTE: `Z102` ha dato UN SOLO numero per `S09` -- il saldo globale, `-1.268e+05`.
  **Un saldo globale non dice DOVE.** Due sistemi con lo stesso saldo -- uno che spinge in modo
  uniforme, uno che concentra tutto su mille archi -- sono **due fisiche diverse**, e il saldo da
  solo non li distingue.

COME: si **sostituisce** `_traccia_d0` con una funzione **pure-read** allo stesso punto di
  chiamata (lo stesso impianto di `_somma_per_scrittore_d0.py`, gia' girato). Legge `prima` e
  `self.d0`, e non scrive stato.

LE LETTURE, FISSATE PRIMA (task history `2026-09-22_dove-spinge-la-gravita.md`, commit `8823ecc`):
  * saldo **per arco** simile in tutte le regioni -> la spinta e' **GLOBALE**, non segue la massa;
  * saldo per arco maggiore in `massa-massa`/`CONFINE` -> la spinta **SEGUE la massa**;
  * saldo per arco maggiore in `vuoto-vuoto` -> **spinge dove non c'e' niente: e' un difetto**;
  * frazione nell'`1 %` piu' spinto **~ 0.01** -> distribuzione **liscia**;
  * frazione nell'`1 %` **molto sopra `0.01`** -> **pochi archi portano quasi tutto**.
  ⚠ Il `0.01` NON e' una soglia scelta: e' il **valore sotto ipotesi nulla** (spinta uniforme).

⚠ COSA MI FA FERMARE, ed e' la ragione della guardia del prefisso: il cumulato **per arco**
  assume che la mitosi **APPENDA** archi senza riordinare i precedenti. **Non lo suppongo: lo
  VERIFICO a ogni passo** sul prefisso di `(i, j)`. **Se anche una sola volta non regge, la
  tabella dei 20 archi NON si stampa**, perche' sarebbero numeri veri sommati sull'arco sbagliato.

⚠ `P1-sexies` -- IL CRITERIO SI COLLAUDA PRIMA, SU CASI A RISPOSTA NOTA. Tre casi, e **il piu'
  importante e' `C`, quello che DEVE fallire**: se la guardia non vede una permutazione, lo
  strumento **si ferma e non misura**.
ASCII PURO.
"""
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

PASSI = 120
LIMITE_S = 2100          # ⚠ se sfora, si ferma PULITA e scrive cio' che ha
for _a in sys.argv[1:]:
    if _a.startswith("--passi="):
        PASSI = int(_a.split("=", 1)[1])
    if _a.startswith("--limite="):
        LIMITE_S = int(_a.split("=", 1)[1])
OUT = os.path.join(RADICE, "csv", "_test_fork", "_diag_D", "DOVE_SPINGE_LA_GRAVITA.txt")
# ⚠ `P1-ter`: la tabella dei 20 archi si GENERA in `csv` e in `markdown`, e non si ricopia MAI a
#   mano. `P6`: entrambi portano BLOB, SEME e i flag che distinguono questo run.
OUT_CSV = os.path.join(RADICE, "csv", "_test_fork", "_diag_D", "G2_20_ARCHI.csv")
OUT_MD = os.path.join(RADICE, "csv", "_test_fork", "_diag_D", "G2_20_ARCHI.md")

# LA CONFIGURAZIONE DELLA VALIDAZIONE, identica a `_somma_per_scrittore_d0.py`
ARGV = ["soliton_simulator.py", "--test", "N-MASSE", "--nmasse", "3", "--sep", "4.0",
        "--giri", "0", "--campo-spinoriale", "--spinore-vivo", "--spinore-corretto",
        "--chi-core", "--calore-scal", "--deparam-orologio", "--verlet", "--fork-su2",
        "--fork-su2-mem", "--cs-dinamico", "--tau-luce", "--rumore-colorato",
        "--pav-com", "--guscio-morbido", "--zeta-vir", "--chi-basc", "--chi-coop",
        "--coes-adim", "--plast-din", "--viriale", "--olon-part",
        "--peq-esatto", "--peq-nascita-locale", "--scala-min-passo", "--coes-causale",
        "--anom-simm", "--invarianti=on"]

N_VUOTO, N0_SEMINA = 900, 2391
ETICHETTE = ("vuoto-vuoto", "massa-massa", "nato-nato",
             "CONFINE vuoto-massa", "CONFINE con nato", "altro")


def regione_nodo(k):
    return np.where(k < N_VUOTO, 0, np.where(k < N0_SEMINA, 1, 2))


def classe_arco(ii, jj):
    """0 vv, 1 mm, 2 nn, 3 confine vuoto-massa, 4 confine con nato, 5 altro."""
    ri, rj = regione_nodo(ii), regione_nodo(jj)
    c = np.full(len(ii), 5, dtype=np.int64)
    c[(ri == 0) & (rj == 0)] = 0
    c[(ri == 1) & (rj == 1)] = 1
    c[(ri == 2) & (rj == 2)] = 2
    c[((ri == 0) & (rj == 1)) | ((ri == 1) & (rj == 0))] = 3
    c[((ri == 2) & (rj != 2)) | ((rj == 2) & (ri != 2))] = 4
    return c


def somma_per_classe(cls, dx):
    """Salite, discese e conteggi per classe. E' la funzione che il collaudo A verifica."""
    nc = len(ETICHETTE)
    su = np.zeros(nc); giu = np.zeros(nc)
    n_su = np.zeros(nc, dtype=np.int64); n_giu = np.zeros(nc, dtype=np.int64)
    n_tot = np.bincount(cls, minlength=nc).astype(np.int64)
    p = dx > 0.0; m = dx < 0.0
    su += np.bincount(cls[p], dx[p], minlength=nc)
    giu += np.bincount(cls[m], dx[m], minlength=nc)
    n_su += np.bincount(cls[p], minlength=nc).astype(np.int64)
    n_giu += np.bincount(cls[m], minlength=nc).astype(np.int64)
    return su, giu, n_su, n_giu, n_tot


def concentrazione(v):
    """Frazione del totale POSITIVO che sta nell'1 % di archi piu' spinti.
    ⚠ Il valore sotto IPOTESI NULLA (spinta uniforme) e' 0.01: non e' una soglia scelta."""
    pos = v[v > 0.0]
    if pos.size < 100:
        return float("nan")
    k = max(1, int(round(0.01 * pos.size)))
    s = np.sort(pos)[::-1]
    return float(np.sum(s[:k]) / np.sum(pos))


class AccChiave(object):
    """Il cumulato per arco IDENTIFICATO DALLA COPPIA DI NODI, non dalla posizione.

    ⚠ PERCHE' NON BASTA LA POSIZIONE, e non e' una precauzione: e' MISURATO. La mitosi fa
      `self.i = concatenate([self.i[keep], a, m])` (`:5325`), cioe' **TOGLIE** gli archi spezzati
      con `[keep]` e appende i nuovi: tutto cio' che segue un arco rimosso **SLITTA**. La guardia
      del prefisso lo ha visto in **61 passi su 120**.

    ⚠ PERCHE' LA COPPIA DI NODI E' UN'IDENTITA' VALIDA, verificato dal sorgente: le uniche
      assegnazioni di `self.pos` sono `vstack` (`:2299`, `:5258`, `:5402`), l'inizializzazione
      (`:1431`) e un `nan_to_num` che non cambia la forma (`:5535`). **I nodi si APPENDONO e basta:
      nessuna rimozione, nessuna rinumerazione.**

    ⚠ E I DUE MODI IN CUI QUESTA IDENTITA' POTREBBE ROMPERSI SONO CONTATI, NON ESCLUSI:
      * **doppioni** -- due archi con la stessa coppia di nodi nello stesso passo;
      * **risurrezioni** -- una coppia che sparisce e poi ricompare, cioe' un arco DIVERSO che
        eredita la chiave di uno morto. Si rileva dal SALTO nell'ultimo passo in cui si e' vista.
      Se sono molti, il cumulato non vale e lo si dice.
    """

    CAMPI = ("acc", "su", "giu", "npassi", "nsat", "visto")

    def __init__(self, base):
        self.base = np.int64(base)
        self.chiavi = np.zeros(0, dtype=np.int64)
        self.acc = np.zeros(0, dtype=float)      # saldo netto
        self.su = np.zeros(0, dtype=float)       # somma delle SALITE
        self.giu = np.zeros(0, dtype=float)      # somma delle DISCESE
        self.npassi = np.zeros(0, dtype=np.int64)   # in quanti passi l'arco ESISTE
        self.nsat = np.zeros(0, dtype=np.int64)     # in quanti passi e' INCOLLATO AL TETTO
        self.visto = np.zeros(0, dtype=np.int64)    # l'ULTIMO passo in cui si e' visto
        self.doppioni = 0
        self.risurrezioni = 0

    def chiave(self, ii, jj):
        return np.asarray(ii, dtype=np.int64) * self.base + np.asarray(jj, dtype=np.int64)

    def nodi(self, k):
        k = np.asarray(k, dtype=np.int64)
        return k // self.base, k % self.base

    def _trova(self, k):
        if len(self.chiavi) == 0:
            return np.zeros(len(k), dtype=np.int64), np.zeros(len(k), bool)
        p = np.searchsorted(self.chiavi, k)
        pc = np.minimum(p, len(self.chiavi) - 1)
        ok = (p < len(self.chiavi)) & (self.chiavi[pc] == k)
        return p, ok

    def aggiungi(self, ii, jj, dx, passo, sat=None):
        k = self.chiave(ii, jj)
        nu = len(np.unique(k))
        if nu != len(k):
            self.doppioni += int(len(k) - nu)
        p, col = self._trova(k)
        if np.any(col):
            pc = p[col]; dc = dx[col]
            np.add.at(self.acc, pc, dc)
            np.add.at(self.su, pc, np.where(dc > 0.0, dc, 0.0))
            np.add.at(self.giu, pc, np.where(dc < 0.0, dc, 0.0))
            np.add.at(self.npassi, pc, 1)
            if sat is not None:
                np.add.at(self.nsat, pc, sat[col].astype(np.int64))
            self.risurrezioni += int(np.sum((passo - self.visto[pc]) > 1))
            self.visto[pc] = passo
        nuovi = ~col
        if np.any(nuovi):
            kn = k[nuovi]; dn = dx[nuovi]
            sn = (sat[nuovi].astype(np.int64) if sat is not None
                  else np.zeros(int(np.sum(nuovi)), dtype=np.int64))
            ku, inv = np.unique(kn, return_inverse=True)
            m = len(ku)
            self.chiavi = np.concatenate([self.chiavi, ku])
            self.acc = np.concatenate([self.acc, np.bincount(inv, dn, minlength=m)])
            self.su = np.concatenate(
                [self.su, np.bincount(inv, np.where(dn > 0.0, dn, 0.0), minlength=m)])
            self.giu = np.concatenate(
                [self.giu, np.bincount(inv, np.where(dn < 0.0, dn, 0.0), minlength=m)])
            self.npassi = np.concatenate(
                [self.npassi, np.bincount(inv, minlength=m).astype(np.int64)])
            self.nsat = np.concatenate(
                [self.nsat, np.bincount(inv, sn, minlength=m).astype(np.int64)])
            self.visto = np.concatenate([self.visto, np.full(m, passo, dtype=np.int64)])
            o = np.argsort(self.chiavi, kind="stable")
            self.chiavi = self.chiavi[o]
            for _c in self.CAMPI:
                setattr(self, _c, getattr(self, _c)[o])

    def leggi(self, ii, jj):
        """Il cumulato riallineato agli archi VIVI ORA."""
        k = self.chiave(ii, jj)
        p, ok = self._trova(k)
        v = np.zeros(len(k)); v[ok] = self.acc[p[ok]]
        return v, ok


def satura(dx):
    """Quanti archi sono INCOLLATI AL TETTO in questo passo, e quanti sono stati scritti.

    ⚠ PERCHE' SI MISURA, e non e' una curiosita': `S09` fa
        `spinta = np.clip(spinta, -passo_causale, passo_causale)`
        `d0[mask] += _sd0(spinta * float(np.median(self.d0[mask])), mask)`
      cioe' quando il clip MORDE l'incremento vale `passo_causale * median(d0[mask])`, che e'
      **UGUALE PER TUTTI GLI ARCHI SATURI**: un tetto globale per una statistica globale (`A2`).
      **Su un arco saturo la spinta non dipende piu' dall'arco: solo il SEGNO lo fa.**
      **`A11` corollario 6: se un limite satura, e' un allarme, non una protezione.**

    ⚠ COME SI RICONOSCE SENZA LEGGERE IL TETTO: se il clip NON morde, il massimo di `|dx|` e'
      raggiunto da UNO o DUE archi; se morde, da MOLTI. Il conteggio distingue i due casi da se',
      e il collaudo `F` lo verifica su entrambi.
    """
    a = np.abs(dx)
    scritti = int(np.count_nonzero(dx))
    if scritti == 0:
        return 0, 0, np.zeros(len(dx), bool)
    tetto = float(np.max(a))
    sel = a >= tetto * (1.0 - 1e-12)
    return int(np.sum(sel)), scritti, sel


def prefisso_regge(ii, jj, pii, pjj):
    """La guardia: il prefisso di (i, j) e' rimasto identico? E' il caso C del collaudo."""
    if pii is None:
        return True
    L = min(len(pii), len(ii))
    return bool(np.array_equal(ii[:L], pii[:L]) and np.array_equal(jj[:L], pjj[:L]))


def collaudo(W):
    """P1-sexies: tre casi a RISPOSTA NOTA. Il piu' importante e' `C`, che DEVE fallire."""
    W("COLLAUDO DEI CRITERI su casi a RISPOSTA NOTA (`P1-sexies`), PRIMA di misurare\n")
    W("-" * 92 + "\n")
    esiti = []

    # --- A: aggregazione per regione con somme NOTE
    ii = np.array([0, 1, 1000, 1001, 3000, 3001, 10, 1500])          # vv vv mm mm nn nn v-m
    jj = np.array([2, 3, 1002, 1003, 3002, 3003, 1600, 3500])
    dx = np.array([+2.0, -1.0, +10.0, -4.0, +100.0, -40.0, +7.0, +0.5])
    cls = classe_arco(ii, jj)
    su, giu, n_su, n_giu, n_tot = somma_per_classe(cls, dx)
    attesi_su = {0: 2.0, 1: 10.0, 2: 100.0, 3: 7.0, 4: 0.5}
    attesi_giu = {0: -1.0, 1: -4.0, 2: -40.0, 3: 0.0, 4: 0.0}
    okA = all(abs(su[k] - v) < 1e-12 for k, v in attesi_su.items()) and \
        all(abs(giu[k] - v) < 1e-12 for k, v in attesi_giu.items())
    W("A  aggregazione per regione, somme NOTE costruite a mano\n")
    W("     atteso  su = %s\n" % ["%.1f" % attesi_su[k] for k in sorted(attesi_su)])
    W("     ottenuto su = %s   -> %s\n"
      % (["%.1f" % su[k] for k in sorted(attesi_su)],
         "OK" if okA else "*** SBAGLIA L'AGGREGAZIONE ***"))
    esiti.append(okA)

    # --- B: concentrazione su UNIFORME -> deve dare ~0.01, il nullo
    rng = np.random.default_rng(11)
    unif = rng.random(200000) * 0.1 + 1.0           # tutti positivi, QUASI UGUALI
    cu = concentrazione(unif)
    okB = abs(cu - 0.01) < 0.005
    W("B  concentrazione su una spinta UNIFORME  -> atteso ~0.01 (il valore sotto ipotesi nulla)\n")
    W("     ottenuto %.5f  -> %s\n" % (cu, "OK" if okB else "*** IL NULLO NON E' 0.01 ***"))
    esiti.append(okB)
    # e il controllo POSITIVO: se pochi archi portano tutto, DEVE staccarsi dal nullo
    conc = np.full(200000, 1e-6); conc[:200] = 1.0
    cc = concentrazione(conc)
    okB2 = cc > 0.5
    W("B+ controllo POSITIVO: 200 archi su 200000 portano tutto -> atteso MOLTO sopra 0.01\n")
    W("     ottenuto %.5f  -> %s\n" % (cc, "OK" if okB2 else "*** NON DISTINGUE ***"))
    esiti.append(okB2)

    # --- C: IL CASO CHE DEVE FALLIRE. Una permutazione: la guardia DEVE vederla.
    a_i = np.arange(1000); a_j = np.arange(1000) + 1
    cresciuto_i = np.concatenate([a_i, np.arange(50)])          # APPESO: deve reggere
    cresciuto_j = np.concatenate([a_j, np.arange(50) + 7])
    perm = rng.permutation(1000)
    perm_i = a_i[perm]; perm_j = a_j[perm]                      # PERMUTATO: NON deve reggere
    okC1 = prefisso_regge(cresciuto_i, cresciuto_j, a_i, a_j)
    okC2 = not prefisso_regge(perm_i, perm_j, a_i, a_j)
    W("C  LA GUARDIA DEL PREFISSO -- il caso che DEVE fallire\n")
    W("     archi APPESI in coda      -> la guardia dice %s, atteso REGGE      -> %s\n"
      % ("REGGE" if okC1 else "NON REGGE", "OK" if okC1 else "*** FALSO ALLARME ***"))
    W("     archi PERMUTATI           -> la guardia dice %s, atteso NON REGGE  -> %s\n"
      % ("REGGE" if not okC2 else "NON REGGE",
         "OK" if okC2 else "*** NON VEDE IL RIORDINO: IL CUMULATO SAREBBE FALSO ***"))
    esiti += [okC1, okC2]

    # --- D: IL CUMULATO PER CHIAVE su un caso a somme NOTE, CON RIORDINO E RIMOZIONE in mezzo.
    #     E' il caso che DEVE riuscire dove quello posizionale sbaglia.
    A = AccChiave(1 << 32)
    p1_i = np.array([10, 11, 12, 13]); p1_j = np.array([20, 21, 22, 23])
    A.aggiungi(p1_i, p1_j, np.array([1.0, 2.0, 3.0, 4.0]), 1)
    # passo 2: l'arco (11,21) MUORE, i restanti SLITTANO, e ne nasce uno nuovo in coda
    p2_i = np.array([10, 12, 13, 99]); p2_j = np.array([20, 22, 23, 98])
    A.aggiungi(p2_i, p2_j, np.array([10.0, 30.0, 40.0, 7.0]), 2)
    fin_i = np.array([10, 12, 13, 99]); fin_j = np.array([20, 22, 23, 98])
    v, _ok = A.leggi(fin_i, fin_j)
    attesi = np.array([11.0, 33.0, 44.0, 7.0])       # noti a mano
    okD = bool(np.allclose(v, attesi, rtol=0, atol=1e-12))
    W("D  cumulato PER CHIAVE, con una MITOSI in mezzo: l'arco (11,21) MUORE e gli altri SLITTANO\n")
    W("     atteso   %s\n" % ["%.0f" % x for x in attesi])
    W("     ottenuto %s   -> %s\n"
      % (["%.0f" % x for x in v], "OK" if okD else "*** SOMMA SULL'ARCO SBAGLIATO ***"))
    esiti.append(okD)

    # --- D-bis: IL CASO CHE DEVE FALLIRE, e NON e' un commento: e' un'asserzione.
    #     L'accumulatore POSIZIONALE, sugli stessi identici dati, DEVE dare il risultato
    #     SBAGLIATO. Se desse quello giusto, il collaudo D non proverebbe niente -- passerebbe
    #     anche un accumulatore rotto, perche' il caso non distinguerebbe i due.
    posiz = np.array([1.0, 2.0, 3.0, 4.0]) + np.array([10.0, 30.0, 40.0, 7.0])
    sbagliati = int(np.sum(~np.isclose(posiz, attesi, rtol=0, atol=1e-12)))
    okDb = sbagliati >= 3
    W("D- IL CASO CHE DEVE FALLIRE: lo stesso caso con l'accumulatore PER POSIZIONE\n")
    W("     ottenuto %s   contro l'atteso %s\n"
      % (["%.0f" % x for x in posiz], ["%.0f" % x for x in attesi]))
    W("     archi sbagliati: %d su 4, atteso >= 3  -> %s\n"
      % (sbagliati, "OK: il caso DISTINGUE i due accumulatori" if okDb
         else "*** IL CASO NON DISTINGUE: il collaudo D non proverebbe nulla ***"))
    esiti.append(okDb)

    # --- F: LA SATURAZIONE, su due casi a risposta nota.
    #     F1 DEVE trovarne esattamente il numero noto; F2 e' IL CASO CHE DEVE FALLIRE -- una
    #     distribuzione SENZA clip, dove il massimo e' raggiunto da UNO solo: se il criterio
    #     dicesse "molti saturi" anche li', misurerebbe il massimo invece del TETTO, e la
    #     "saturazione diffusa" sarebbe un artefatto del criterio invece che un fatto del codice.
    rng2 = np.random.default_rng(3)
    base = rng2.random(10000) * 0.5                      # tutti sotto il tetto
    tetto = 0.9
    base[:137] = tetto                                   # 137 INCOLLATI in su
    base[137:137 + 61] = -tetto                          # 61 INCOLLATI in giu'
    ns, scr, sel = satura(base)
    okF1 = (ns == 198) and (scr == 10000)
    W("F  LA SATURAZIONE, su un caso a numero NOTO di archi incollati al tetto\n")
    W("     atteso 198 saturi (137 in su + 61 in giu') su 10000 scritti\n")
    W("     ottenuto %d saturi su %d scritti  -> %s\n"
      % (ns, scr, "OK" if okF1 else "*** CONTEGGIO SBAGLIATO ***"))
    esiti.append(okF1)

    liscio = np.linspace(0.01, 0.99, 10000)              # NESSUN clip: tutti valori diversi
    ns2, _s2, _l2 = satura(liscio)
    okF2 = ns2 <= 2
    W("F- IL CASO CHE DEVE FALLIRE: una distribuzione LISCIA, senza nessun tetto\n")
    W("     ottenuti %d saturi, atteso <= 2 (solo il massimo)  -> %s\n"
      % (ns2, "OK: il criterio vede il TETTO, non il massimo"
         if okF2 else "*** MISURA IL MASSIMO: la saturazione sarebbe un artefatto ***"))
    esiti.append(okF2)

    # --- G: le TRE COLONNE NUOVE -- salite, discese e PASSI IN CUI L'ARCO ESISTE -- a somme note.
    G = AccChiave(1 << 32)
    G.aggiungi(np.array([3, 4]), np.array([7, 8]), np.array([+5.0, -2.0]), 1)
    G.aggiungi(np.array([3]), np.array([7]), np.array([-1.0]), 2)          # (4,8) MUORE
    G.aggiungi(np.array([3]), np.array([7]), np.array([+0.5]), 3)
    kk = G.chiave(np.array([3, 4]), np.array([7, 8]))
    p, _o = G._trova(kk)
    att_su = np.array([5.5, 0.0]); att_giu = np.array([-1.0, -2.0])
    att_np = np.array([3, 1]); att_sal = np.array([4.5, -2.0])
    okG = (np.allclose(G.su[p], att_su, rtol=0, atol=1e-12)
           and np.allclose(G.giu[p], att_giu, rtol=0, atol=1e-12)
           and np.array_equal(G.npassi[p], att_np)
           and np.allclose(G.acc[p], att_sal, rtol=0, atol=1e-12))
    W("G  le TRE COLONNE NUOVE a somme NOTE: salite, discese, passi in cui l'arco ESISTE\n")
    def _l(v):
        return "[" + ", ".join("%g" % float(x) for x in v) + "]"
    W("     atteso   salite %s  discese %s  passi %s  saldo %s\n"
      % (_l(att_su), _l(att_giu), _l(att_np), _l(att_sal)))
    W("     ottenuto salite %s  discese %s  passi %s  saldo %s  -> %s\n"
      % (_l(G.su[p]), _l(G.giu[p]), _l(G.npassi[p]), _l(G.acc[p]),
         "OK" if okG else "*** COLONNE SBAGLIATE ***"))
    esiti.append(okG)

    # --- E: IL CASO CHE DEVE FALLIRE. Una RISURREZIONE: una chiave che sparisce e ricompare.
    #     Se l'accumulatore non se ne accorge, sta sommando DUE archi diversi nello stesso posto.
    B = AccChiave(1 << 32)
    B.aggiungi(np.array([5]), np.array([6]), np.array([1.0]), 1)
    B.aggiungi(np.array([7]), np.array([8]), np.array([1.0]), 2)     # (5,6) ASSENTE al passo 2
    B.aggiungi(np.array([5]), np.array([6]), np.array([1.0]), 3)     # e RICOMPARE al passo 3
    okE = B.risurrezioni >= 1
    C = AccChiave(1 << 32)
    for _p in (1, 2, 3):
        C.aggiungi(np.array([5]), np.array([6]), np.array([1.0]), _p)  # sempre viva: 0 allarmi
    okE2 = C.risurrezioni == 0
    W("E  LA GUARDIA DELLA RISURREZIONE -- il caso che DEVE fallire\n")
    W("     chiave che SPARISCE e RICOMPARE -> risurrezioni contate %d, atteso >= 1  -> %s\n"
      % (B.risurrezioni, "OK" if okE else "*** NON LA VEDE: sommerebbe DUE archi diversi ***"))
    W("     chiave sempre VIVA               -> risurrezioni contate %d, atteso 0     -> %s\n"
      % (C.risurrezioni, "OK" if okE2 else "*** FALSO ALLARME ***"))
    esiti += [okE, okE2]

    ok = all(esiti)
    W("-" * 92 + "\n")
    W("  -> i criteri %s\n\n" % ("PASSANO tutti: si misura" if ok
                                 else "*** NON PASSANO: NON MISURO ***"))
    return ok


def main():
    o = io.open(OUT, "w", encoding="utf-8", newline="\n")
    W = o.write
    W("# DOVE SPINGE LA GRAVITA' -- il saldo di `S09` PER REGIONE, e i 20 archi piu' spinti\n")
    W("# SOLA MISURA. Nessuna cura, nessuna modifica al simulatore.\n")
    W("# ATTENZIONE A COSA E' `dx`: `S09` scrive `d0[mask] += _sd0(...)`, e sotto\n")
    W("#   `SCALA_MIN_PASSO` -- acceso qui -- `_sd0` e' PASS-THROUGH: il freno agisce UNA volta\n")
    W("#   a fine passo, FUORI da questo punto. Quindi `dx` e' la spinta GREZZA, la stessa che\n")
    W("#   in `Z102` somma a `-1.268e+05`, NON quella dopo il freno.\n#\n")
    if not collaudo(W):
        o.close(); print(io.open(OUT, encoding="utf-8").read()); return 1

    os.chdir(RADICE)
    sys.argv = list(ARGV)
    import soliton_simulator as S
    S.TRACCIA_D0 = True
    a = S._cli(); S._applica_regime(a); S._applica_flag(a)
    for f in ("PEQ_ESATTO", "PEQ_NASCITA_LOCALE", "SCALA_MIN_PASSO", "COES_CAUSALE",
              "ANOM_SIMM", "INVARIANTI"):
        if not getattr(S, f):
            raise SystemExit("[G2] %s e' SPENTO: non e' la configurazione della validazione" % f)

    # accumulatori per REGIONE, per sito; e il cumulato PER ARCO del solo `S09`
    PER_REG = {}                 # sito -> [su, giu, n_su, n_giu] per classe
    ACC = {"v": np.zeros(0)}     # cumulato POSIZIONALE di S09 -- tenuto per CONTRASTO
    ACCK = AccChiave(1 << 32)    # cumulato PER CHIAVE (coppia di nodi): quello buono
    GIRI = {}
    CRESCITA = {"pad": 0, "salta": 0}
    PASSO = {"k": 0}
    TOP_PASSO = {"v": None}      # il top-20 di UN SOLO passo: immune al riordino per costruzione
    SAT_PASSO = []               # (passo, n_saturi, n_scritti, n_vivi)
    SAT_REG = np.zeros(len(ETICHETTE), dtype=np.int64)   # archi-passo saturi per regione
    SAT_REG_TOT = np.zeros(len(ETICHETTE), dtype=np.int64)  # archi-passo scritti per regione
    SAT_SALDO = {"sat": 0.0, "tot": 0.0, "sat_su": 0.0, "sat_giu": 0.0}

    def traccia(self, sito, prima, pavimento=None):
        """SOSTITUISCE `_traccia_d0`. PURE-READ: legge e somma, non scrive stato."""
        GIRI[sito] = GIRI.get(sito, 0) + 1
        dopo = np.asarray(self.d0, dtype=float)
        pri = np.asarray(prima, dtype=float)
        if len(pri) != len(dopo):
            CRESCITA["salta"] += 1
            return
        dx = dopo - pri
        ii = np.asarray(self.i); jj = np.asarray(self.j)
        if len(ii) != len(dx):
            CRESCITA["salta"] += 1
            return
        cls = classe_arco(ii, jj)
        su, giu, n_su, n_giu, n_tot = somma_per_classe(cls, dx)
        c = PER_REG.setdefault(sito, [np.zeros(len(ETICHETTE)), np.zeros(len(ETICHETTE)),
                                      np.zeros(len(ETICHETTE), dtype=np.int64),
                                      np.zeros(len(ETICHETTE), dtype=np.int64)])
        c[0] += su; c[1] += giu; c[2] += n_su; c[3] += n_giu
        if sito.startswith("S09"):
            v = ACC["v"]
            if len(v) < len(dx):
                ACC["v"] = np.concatenate([v, np.zeros(len(dx) - len(v))])
                CRESCITA["pad"] += 1
            ACC["v"][:len(dx)] += dx
            n_sat, scritti, sel = satura(dx)
            SAT_PASSO.append((PASSO["k"], n_sat, scritti, len(dx)))
            # ⚠ `SAT_REG += ...` qui NON si puo' usare: un assegnamento aumentato dentro una
            #   funzione annidata LEGA il nome come LOCALE e alza `UnboundLocalError`.
            #   `np.add(..., out=...)` scrive IN PLACE senza legare nulla. Difetto preso il
            #   2026-09-22, al passo 1, e il collaudo NON lo aveva visto perche' collauda i
            #   CRITERI, non l'impianto che li alimenta.
            np.add(SAT_REG, np.bincount(cls[sel], minlength=len(ETICHETTE)).astype(np.int64),
                   out=SAT_REG)
            _scr = dx != 0.0
            np.add(SAT_REG_TOT,
                   np.bincount(cls[_scr], minlength=len(ETICHETTE)).astype(np.int64),
                   out=SAT_REG_TOT)
            SAT_SALDO["sat"] += float(np.sum(dx[sel]))
            SAT_SALDO["tot"] += float(np.sum(dx))
            _ds = dx[sel]
            SAT_SALDO["sat_su"] += float(np.sum(_ds[_ds > 0.0]))
            SAT_SALDO["sat_giu"] += float(np.sum(_ds[_ds < 0.0]))
            ACCK.aggiungi(ii, jj, dx, PASSO["k"], sat=sel)
            TOP_PASSO["v"] = (ii.copy(), jj.copy(), dx.copy(), PASSO["k"])

    S.Rete._traccia_d0 = traccia

    # ⚠ `P6`: il BLOB (sha1 dei byte GREZZI, non `git hash-object`) e il SEME EFFETTIVO, letto
    #   dalla firma di `Rete.__init__` come fa il driver -- non da una costante ricordata.
    import hashlib
    import inspect as _insp
    _BLOB_SIM = hashlib.sha1(
        open(os.path.join(RADICE, "soliton_simulator.py"), "rb").read()).hexdigest()[:8]
    _SEME = _insp.signature(S.Rete.__init__).parameters["seed"].default

    S._NMASSE_VIDEO["n"] = 3; S._NMASSE_VIDEO["sep"] = 4.0; S._NMASSE_VIDEO["size"] = None
    S.avvia_test("N-MASSE")()
    net = S.net
    S.stato["nframe"] = 0
    PPF = int(S.PASSI_PER_FRAME)
    t0 = time.time()
    fatti = 0
    fermato = None
    pii = pjj = None
    viol = []                     # i passi in cui il prefisso NON regge
    for k in range(1, PASSI + 1):
        if (k - 1) % PPF == 0:
            S.passo_test()
        PASSO["k"] = k
        S.scuoti_vuoto(net); net.step(); net.mitosi()
        net.rilassa_disegno(); net.memoria_hebbiana_moto()
        fatti = k
        ii = np.asarray(net.i).copy(); jj = np.asarray(net.j).copy()
        if not prefisso_regge(ii, jj, pii, pjj):
            viol.append(k)
        pii, pjj = ii, jj
        if time.time() - t0 > LIMITE_S:
            fermato = "LIMITE DI TEMPO (%d s): fermata PULITA al passo %d" % (LIMITE_S, k)
            break

    W("configurazione: quella della VALIDAZIONE (sei cure accese). Passi: %d su %d. %.1f s%s\n\n"
      % (fatti, PASSI, time.time() - t0, "" if fermato is None else "   *** %s" % fermato))

    # ------------------------------------------------------------------ S09 per regione
    for sito in ("S09_spinta_med", "S10_grav_med"):
        W("=" * 108 + "\n")
        W("`%s` -- IL SALDO PER REGIONE\n" % sito)
        W("=" * 108 + "\n")
        if sito not in PER_REG:
            W("*** NON HA MAI GIRATO in questa configurazione: non e' misurabile qui, e lo dico\n")
            W("    invece di dedurlo. (giri registrati: %d) ***\n\n" % GIRI.get(sito, 0))
            continue
        su, giu, n_su, n_giu = PER_REG[sito]
        cls_fin = classe_arco(np.asarray(net.i), np.asarray(net.j))
        n_arc = np.bincount(cls_fin, minlength=len(ETICHETTE))
        W("%-20s %9s | %13s %13s %13s | %13s %11s\n"
          % ("regione", "archi", "SALITE", "DISCESE", "SALDO", "SALDO/ARCO", "|saldo|/tot"))
        W("-" * 108 + "\n")
        for c in range(len(ETICHETTE)):
            if n_arc[c] == 0 and n_su[c] == 0 and n_giu[c] == 0:
                continue
            saldo = su[c] + giu[c]
            tot = su[c] - giu[c]
            W("%-20s %9d | %13.6e %13.6e %13.6e | %13.6e %11.4f\n"
              % (ETICHETTE[c], int(n_arc[c]), su[c], giu[c], saldo,
                 saldo / max(int(n_arc[c]), 1), abs(saldo) / max(tot, 1e-300)))
        W("-" * 108 + "\n")
        W("%-20s %9d | %13.6e %13.6e %13.6e |\n"
          % ("TOTALE", int(np.sum(n_arc)), float(np.sum(su)), float(np.sum(giu)),
             float(np.sum(su) + np.sum(giu))))
        W("  giri: %d   conteggi: salite %d, discese %d\n\n"
          % (GIRI.get(sito, 0), int(np.sum(n_su)), int(np.sum(n_giu))))

    # ------------------------------------------------------------------ i 20 archi
    W("=" * 108 + "\n")
    W("I 20 ARCHI CHE RICEVONO LA SPINTA PIU' GRANDE (cumulato di `S09` sui %d passi)\n" % fatti)
    W("=" * 108 + "\n")
    W("la guardia del PREFISSO: %d passi su %d in cui `(i, j)` NON e' rimasto un prefisso\n"
      % (len(viol), fatti))
    W("  (allungamenti dell'accumulatore: %d; chiamate saltate per lunghezza: %d)\n"
      % (CRESCITA["pad"], CRESCITA["salta"]))
    W("  -> IL CUMULATO POSIZIONALE E' INUTILIZZABILE, e per questo non si usa.\n")
    W("     LA MITOSI TOGLIE archi (`self.i = concatenate([self.i[keep], a, m])`, `:5325`):\n")
    W("     tutto cio' che segue un arco rimosso SLITTA. Si usa l'accumulatore PER CHIAVE.\n")
    W("\nla guardia dell'accumulatore PER CHIAVE (coppia di nodi):\n")
    W("  doppioni (due archi con la stessa coppia nello stesso passo): %d\n" % ACCK.doppioni)
    W("  RISURREZIONI (una coppia sparisce e ricompare -> un arco DIVERSO eredita la chiave): %d\n"
      % ACCK.risurrezioni)
    W("  chiavi distinte viste in tutto il run: %d\n" % len(ACCK.chiavi))

    ii = np.asarray(net.i); jj = np.asarray(net.j)
    d = np.asarray(net.d, dtype=float)
    d0 = np.asarray(net.d0, dtype=float)
    pos = np.asarray(net.pos, dtype=float)
    cls = classe_arco(ii, jj)
    Ld = np.linalg.norm(pos[jj] - pos[ii], axis=1) / np.maximum(d, 1e-300)
    vv, trovati = ACCK.leggi(ii, jj)
    W("  archi VIVI ora con un cumulato: %d su %d\n" % (int(np.sum(trovati)), len(ii)))
    _sporco = (ACCK.doppioni + ACCK.risurrezioni)
    if _sporco:
        W("\n  *** %d chiavi AMBIGUE: il cumulato per chiave e' SPORCO su quelle. Il numero e'\n"
          % _sporco)
        W("      dichiarato qui invece di essere nascosto; se e' grande davanti a %d, la\n"
          % len(ACCK.chiavi))
        W("      tabella cumulata NON si legge. ***\n")

    W("\nCONCENTRAZIONE, sul cumulato PER CHIAVE: la frazione della spinta POSITIVA totale che\n")
    W("  sta nell'1 %% di archi piu' spinti. Il valore sotto IPOTESI NULLA (uniforme) e' 0.01.\n")
    cpos = concentrazione(vv)
    W("  misurata = %.5f    nullo = 0.01    rapporto = %.1fx\n"
      % (cpos, cpos / 0.01 if np.isfinite(cpos) else float("nan")))
    cneg = concentrazione(-vv)
    W("  e sulle SPINTE NEGATIVE (la compressione): %.5f    rapporto = %.1fx\n"
      % (cneg, cneg / 0.01 if np.isfinite(cneg) else float("nan")))

    # ---------------- I 20 ARCHI col |saldo| piu' grande, SU TUTTE LE CHIAVI (anche morte)
    kt = ACCK.chiavi
    ki, kj = ACCK.nodi(kt)
    kcls = classe_arco(ki, kj)
    ordine = np.argsort(np.abs(ACCK.acc))[::-1][:20]

    intest = ["rango", "nodo_i", "nodo_j", "regione", "saldo_netto", "somma_salite",
              "somma_discese", "passi_in_cui_esiste", "vivo_ora", "d", "d0", "L_disegno_su_d"]
    vivi = {}
    for _a in range(len(ii)):
        vivi[int(ii[_a]) * (1 << 32) + int(jj[_a])] = _a
    righe_csv = []
    for r, a_ in enumerate(ordine, 1):
        _k = int(kt[a_])
        _iv = vivi.get(_k)
        righe_csv.append([r, int(ki[a_]), int(kj[a_]), ETICHETTE[kcls[a_]],
                          ACCK.acc[a_], ACCK.su[a_], ACCK.giu[a_], int(ACCK.npassi[a_]),
                          1 if _iv is not None else 0,
                          d[_iv] if _iv is not None else float("nan"),
                          d0[_iv] if _iv is not None else float("nan"),
                          Ld[_iv] if _iv is not None else float("nan")])

    with io.open(OUT_CSV, "w", encoding="utf-8", newline="\n") as fc:
        fc.write("# G2 -- i 20 archi col |saldo S09| piu' grande, identificati per CHIAVE (i,j)\n")
        fc.write("# blob simulatore (sha1 byte grezzi)=%s  seme=%s  passi=%d  scena=N-MASSE sep=4.0\n"
                 % (_BLOB_SIM, _SEME, fatti))
        fc.write("# doppioni=%d risurrezioni=%d chiavi_distinte=%d\n"
                 % (ACCK.doppioni, ACCK.risurrezioni, len(kt)))
        fc.write(",".join(intest) + "\n")
        for rr in righe_csv:
            fc.write(",".join(("%d" % x) if isinstance(x, int) else
                              (x if isinstance(x, str) else "%.9e" % x) for x in rr) + "\n")

    with io.open(OUT_MD, "w", encoding="utf-8", newline="\n") as fm:
        fm.write("# `G2` -- i **20 archi** col `|saldo S09|` piu' grande\n\n")
        fm.write("> **GENERATA DA CODICE** (`P1-ter`), mai ricopiata a mano.\n")
        fm.write("> `csv/_test_fork/_dove_spinge_la_gravita.py`, blob simulatore `%s`, seme `%s`,\n"
                 % (_BLOB_SIM, _SEME))
        fm.write("> **%d passi dalla semina**, configurazione della validazione.\n" % fatti)
        fm.write("> Archi identificati per **chiave `(i, j)`**, non per posizione.\n\n")
        fm.write("| # | `i` | `j` | regione | saldo netto | salite | discese | passi | vivo |\n")
        fm.write("|--:|--:|--:|---|--:|--:|--:|--:|:-:|\n")
        for rr in righe_csv:
            fm.write("| %d | %d | %d | %s | `%+.6e` | `%.6e` | `%.6e` | %d | %s |\n"
                     % (rr[0], rr[1], rr[2], rr[3], rr[4], rr[5], rr[6], rr[7],
                        "si" if rr[8] else "**no**"))
        fm.write("\n**doppioni** *(stessa chiave due volte nello stesso passo)*: **%d** · "
                 "**risurrezioni** *(chiave che sparisce e ricompare)*: **%d** · "
                 "chiavi distinte: **%d**\n" % (ACCK.doppioni, ACCK.risurrezioni, len(kt)))

    W("\nI 20 ARCHI COL |SALDO| PIU' GRANDE -- per CHIAVE (i,j), su tutte le chiavi viste\n")
    W("  tabella GENERATA DA CODICE anche in:\n    %s\n    %s\n"
      % (os.path.relpath(OUT_CSV, RADICE).replace("\\", "/"),
         os.path.relpath(OUT_MD, RADICE).replace("\\", "/")))
    W("%5s %7s %7s %-20s | %13s %13s %13s | %6s %5s\n"
      % ("#", "i", "j", "regione", "SALDO", "salite", "discese", "passi", "vivo"))
    W("-" * 108 + "\n")
    for rr in righe_csv:
        W("%5d %7d %7d %-20s | %+13.6e %13.6e %13.6e | %6d %5s\n"
          % (rr[0], rr[1], rr[2], rr[3], rr[4], rr[5], rr[6], rr[7],
             "si" if rr[8] else "NO"))

    # ---------------- LA SATURAZIONE, MISURATA
    W("\n" + "=" * 108 + "\n")
    W("LA SATURAZIONE DI `S09`: QUANTO SPESSO LA SPINTA E' INCOLLATA AL TETTO CAUSALE\n")
    W("  `spinta = np.clip(spinta, -passo_causale, passo_causale)` e poi\n")
    W("  `d0[mask] += _sd0(spinta * median(d0[mask]), mask)`: su un arco SATURO l'incremento vale\n")
    W("  `passo_causale * median(d0[mask])`, UGUALE PER TUTTI. Non dipende piu' dall'arco.\n")
    W("=" * 108 + "\n")
    if SAT_PASSO:
        _ns = np.array([r[1] for r in SAT_PASSO], dtype=float)
        _nw = np.array([r[2] for r in SAT_PASSO], dtype=float)
        _nv = np.array([r[3] for r in SAT_PASSO], dtype=float)
        fr_scr = _ns / np.maximum(_nw, 1.0)
        fr_viv = _ns / np.maximum(_nv, 1.0)
        W("\nPER PASSO (%d passi):\n" % len(SAT_PASSO))
        W("%-28s %12s %12s %12s %12s\n" % ("", "min", "mediana", "max", "totale"))
        W("  %-26s %12d %12d %12d %12d\n"
          % ("archi SATURI", int(_ns.min()), int(np.median(_ns)), int(_ns.max()), int(_ns.sum())))
        W("  %-26s %12d %12d %12d %12d\n"
          % ("archi SCRITTI (dx != 0)", int(_nw.min()), int(np.median(_nw)), int(_nw.max()),
             int(_nw.sum())))
        W("  %-26s %12.6f %12.6f %12.6f %12.6f\n"
          % ("frazione sugli SCRITTI", fr_scr.min(), float(np.median(fr_scr)), fr_scr.max(),
             float(_ns.sum() / max(_nw.sum(), 1.0))))
        W("  %-26s %12.6f %12.6f %12.6f %12.6f\n"
          % ("frazione sugli archi VIVI", fr_viv.min(), float(np.median(fr_viv)), fr_viv.max(),
             float(_ns.sum() / max(_nv.sum(), 1.0))))

        W("\nPER ARCO -- in quanti passi ciascuno e' SATURO (istogramma, su %d chiavi):\n"
          % len(ACCK.chiavi))
        _bins = [(0, 0, "0 (mai saturo)"), (1, 10, "1-10"), (11, 60, "11-60"),
                 (61, 119, "61-119"), (120, 10 ** 9, "120 (SEMPRE)")]
        for lo, hi, et in _bins:
            _sel = (ACCK.nsat >= lo) & (ACCK.nsat <= hi)
            _c = int(np.sum(_sel))
            W("  %-16s %10d archi   %7.4f della popolazione\n"
              % (et, _c, _c / max(len(ACCK.chiavi), 1)))

        W("\nPER REGIONE -- archi-passo saturi su archi-passo scritti:\n")
        W("%-22s %14s %14s %12s\n" % ("regione", "saturi", "scritti", "frazione"))
        W("-" * 66 + "\n")
        for c in range(len(ETICHETTE)):
            if SAT_REG_TOT[c] == 0:
                continue
            W("%-22s %14d %14d %12.6f\n"
              % (ETICHETTE[c], int(SAT_REG[c]), int(SAT_REG_TOT[c]),
                 SAT_REG[c] / max(float(SAT_REG_TOT[c]), 1.0)))

        W("\nQUANTA PARTE DEL SALDO VIENE DA INCREMENTI SATURI:\n")
        _st = SAT_SALDO["sat"]; _tt = SAT_SALDO["tot"]
        W("  saldo da incrementi SATURI   %+.6e   (salite %+.6e, discese %+.6e)\n"
          % (_st, SAT_SALDO["sat_su"], SAT_SALDO["sat_giu"]))
        W("  saldo NETTO totale di `S09`  %+.6e\n" % _tt)
        W("  rapporto saturo/totale       %.6f\n" % (_st / _tt if _tt else float("nan")))

        # ---- LA LETTURA, FISSATA PRIMA (mandato del 2026-09-22 par.1)
        _fr = float(_ns.sum() / max(_nw.sum(), 1.0))
        W("\n" + "-" * 108 + "\n")
        W("LA LETTURA, FISSATA PRIMA DI GUARDARE I NUMERI:\n")
        W("  saturazione RARA   (< 1 %%)  -> il clip e' un difetto LOCALE, il plateau e' una coda\n")
        W("  saturazione DIFFUSA (> 10 %%) -> la spinta e' in gran parte `tetto x mediana globale`:\n")
        W("                                 un numero GLOBALE con un segno. `A11` corollario 6.\n")
        W("  in mezzo                    -> si scrive il numero, SENZA etichetta.\n")
        W("  MISURATO: frazione di archi-passo saturi sugli scritti = %.6f = %.4f %%\n"
          % (_fr, 100.0 * _fr))
        if _fr < 0.01:
            W("  -> *** SATURAZIONE RARA: difetto LOCALE. ***\n")
        elif _fr > 0.10:
            W("  -> *** SATURAZIONE DIFFUSA: la spinta di oggi e' in gran parte UN NUMERO\n")
            W("         GLOBALE CON UN SEGNO. E' `A11` corollario 6. ***\n")
        else:
            W("  -> IN MEZZO: il numero e' %.4f %%, e resta SENZA ETICHETTA.\n" % (100.0 * _fr))
    else:
        W("\n*** `S09` non ha scritto: la saturazione non e' misurabile qui. ***\n")

    # ---------------- LE TRE RIGHE DI RISCONTRO
    # il saldo per regione COME LO HA CALCOLATO `Z105`: sommando PER PASSO, con la classe
    # ricalcolata a ogni passo. Serve al riscontro 3, che lo confronta col saldo PER CHIAVE.
    PER_REG_C = {}
    if "S09_spinta_med" in PER_REG:
        _su0, _giu0, _n1, _n2 = PER_REG["S09_spinta_med"]
        for c in range(len(ETICHETTE)):
            PER_REG_C[c] = float(_su0[c] + _giu0[c])
    W("\n" + "=" * 108 + "\n")
    W("LE TRE RIGHE DI RISCONTRO\n")
    W("=" * 108 + "\n")
    _sul_conf = int(np.sum([1 for rr in righe_csv if rr[3].startswith("CONFINE")]))
    W("1. I 20 ARCHI STANNO SUL CONFINE?  %d su 20\n" % _sul_conf)

    saldo_reg = np.zeros(len(ETICHETTE))
    su_reg = np.zeros(len(ETICHETTE)); giu_reg = np.zeros(len(ETICHETTE))
    for c in range(len(ETICHETTE)):
        s = kcls == c
        saldo_reg[c] = float(np.sum(ACCK.acc[s]))
        su_reg[c] = float(np.sum(ACCK.su[s])); giu_reg[c] = float(np.sum(ACCK.giu[s]))
    _conf = saldo_reg[3]
    _venti = float(np.sum([rr[4] for rr in righe_csv if rr[3].startswith("CONFINE")]))
    W("2. QUANTA PARTE DEL SALDO DI CONFINE FANNO I 20?\n")
    W("   saldo dei 20 sul confine = %+.6e   saldo TOTALE del confine = %+.6e\n"
      % (_venti, _conf))
    W("   frazione = %.8f   -- il nullo, se il saldo fosse diffuso su tutti i %d archi di\n"
      % (_venti / _conf if _conf else float("nan"), int(np.sum(kcls == 3))))
    W("   confine, sarebbe 20/%d = %.8f\n"
      % (int(np.sum(kcls == 3)), 20.0 / max(int(np.sum(kcls == 3)), 1)))
    W("   -> %s\n" % ("CONCENTRATO su pochi archi"
                      if _conf and abs(_venti / _conf) > 10 * (20.0 / max(int(np.sum(kcls == 3)), 1))
                      else "DIFFUSO: i 20 non fanno una parte speciale del saldo"))

    W("3. IL SALDO PER REGIONE RIFATTO PER CHIAVE COINCIDE CON QUELLO DI `Z105`?\n")
    W("   `Z105` ha sommato PER PASSO (classe calcolata a ogni passo); qui si somma PER CHIAVE.\n")
    W("   Se coincidono, la tabella per regione di `Z105` NON era toccata dal riordino.\n")
    W("%-20s | %15s %15s | %15s\n"
      % ("regione", "saldo PER PASSO", "saldo PER CHIAVE", "differenza"))
    W("-" * 74 + "\n")
    _peggio = 0.0
    for c in range(len(ETICHETTE)):
        if c not in PER_REG_C:
            continue
        a = PER_REG_C[c]; b = saldo_reg[c]
        dd = abs(a - b)
        _peggio = max(_peggio, dd / max(abs(a), 1e-300))
        W("%-20s | %+15.6e %+15.6e | %15.3e\n" % (ETICHETTE[c], a, b, dd))
    W("-" * 74 + "\n")
    W("   scarto relativo PEGGIORE = %.3e\n" % _peggio)
    W("   -> %s\n" % ("COINCIDONO: `Z105` NON va corretto."
                      if _peggio < 1e-9 else
                      "*** NON COINCIDONO: `Z105` VA CORRETTO, e con esso "
                      "`doc/IPOTESI_gravita_a_spinta.md`. ***"))

    # ---------------- il top di UN SOLO passo: immune al riordino PER COSTRUZIONE
    if TOP_PASSO["v"] is not None:
        tii, tjj, tdx, tk = TOP_PASSO["v"]
        W("\n" + "-" * 108 + "\n")
        W("CONTROPROVA -- il top di UN SOLO PASSO (il %d), che NON cumula nulla e quindi e'\n" % tk)
        W("  immune al riordino PER COSTRUZIONE. Se i nodi qui somigliano a quelli di sopra,\n")
        W("  le due strade concordano; se no, il cumulato va guardato con sospetto.\n")
        tcl = classe_arco(tii, tjj)
        W("%6s %8s %8s %-20s | %13s\n"
          % ("rango", "nodo i", "nodo j", "regione", "spinta nel passo"))
        for r, a_ in enumerate(np.argsort(tdx)[:10], 1):
            W("%6d %8d %8d %-20s | %13.6e\n"
              % (r, int(tii[a_]), int(tjj[a_]), ETICHETTE[tcl[a_]], tdx[a_]))
        W("  concentrazione delle DISCESE in questo singolo passo: %.5f  (nullo 0.01)\n"
          % concentrazione(-tdx))

    W("\nLIMITI: UN seme, UNA scena, %d passi dalla semina. E questa misura dice DOVE la spinta\n"
      % fatti)
    W("  arriva, NON se spegnerla cambi il sistema: per quello servono `G3` e `G4`.\n")
    o.close()
    print(io.open(OUT, encoding="utf-8").read())
    return 0


if __name__ == "__main__":
    sys.exit(main())
