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

    def __init__(self, base):
        self.base = np.int64(base)
        self.chiavi = np.zeros(0, dtype=np.int64)
        self.acc = np.zeros(0, dtype=float)
        self.visto = np.zeros(0, dtype=np.int64)
        self.doppioni = 0
        self.risurrezioni = 0

    def chiave(self, ii, jj):
        return np.asarray(ii, dtype=np.int64) * self.base + np.asarray(jj, dtype=np.int64)

    def aggiungi(self, ii, jj, dx, passo):
        k = self.chiave(ii, jj)
        if len(np.unique(k)) != len(k):
            self.doppioni += int(len(k) - len(np.unique(k)))
        p = np.searchsorted(self.chiavi, k)
        pc = np.minimum(p, max(len(self.chiavi) - 1, 0))
        col = (len(self.chiavi) > 0) & (p < len(self.chiavi))
        col = col & (self.chiavi[pc] == k) if len(self.chiavi) else np.zeros(len(k), bool)
        if np.any(col):
            np.add.at(self.acc, p[col], dx[col])
            _salto = passo - self.visto[p[col]]
            self.risurrezioni += int(np.sum(_salto > 1))
            self.visto[p[col]] = passo
        nuovi = ~col
        if np.any(nuovi):
            ku, inv = np.unique(k[nuovi], return_inverse=True)
            su = np.bincount(inv, dx[nuovi], minlength=len(ku))
            self.chiavi = np.concatenate([self.chiavi, ku])
            self.acc = np.concatenate([self.acc, su])
            self.visto = np.concatenate([self.visto,
                                         np.full(len(ku), passo, dtype=np.int64)])
            o = np.argsort(self.chiavi, kind="stable")
            self.chiavi = self.chiavi[o]; self.acc = self.acc[o]; self.visto = self.visto[o]

    def leggi(self, ii, jj):
        """Il cumulato riallineato agli archi VIVI ORA. -1 = chiave non presente."""
        k = self.chiave(ii, jj)
        p = np.searchsorted(self.chiavi, k)
        pc = np.minimum(p, max(len(self.chiavi) - 1, 0))
        ok = (p < len(self.chiavi)) & (self.chiavi[pc] == k) if len(self.chiavi) \
            else np.zeros(len(k), bool)
        v = np.zeros(len(k)); v[ok] = self.acc[p[ok]]
        return v, ok


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
    # e il CONFRONTO: l'accumulatore POSIZIONALE, sugli stessi dati, cosa avrebbe dato?
    posiz = np.array([1.0, 2.0, 3.0, 4.0]) + np.array([10.0, 30.0, 40.0, 7.0])
    W("D  cumulato PER CHIAVE, con un arco MORTO e gli altri SLITTATI in mezzo\n")
    W("     atteso   %s\n" % ["%.0f" % x for x in attesi])
    W("     ottenuto %s   -> %s\n"
      % (["%.0f" % x for x in v], "OK" if okD else "*** SOMMA SULL'ARCO SBAGLIATO ***"))
    W("     (per contrasto, l'accumulatore POSIZIONALE avrebbe dato %s: sbagliato su 3 archi\n"
      % ["%.0f" % x for x in posiz])
    W("      su 4 -- ed e' esattamente il difetto che la guardia del prefisso ha trovato)\n")
    esiti.append(okD)

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
            ACCK.aggiungi(ii, jj, dx, PASSO["k"])
            TOP_PASSO["v"] = (ii.copy(), jj.copy(), dx.copy(), PASSO["k"])

    S.Rete._traccia_d0 = traccia

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

    W("\nI 20 ARCHI PIU' SPINTI VERSO L'ALTO (cumulato su %d passi, chiave = coppia di nodi)\n"
      % fatti)
    W("%6s %8s %8s %-20s | %13s | %10s %10s %8s\n"
      % ("rango", "nodo i", "nodo j", "regione", "spinta cumul.", "d", "d0", "L/d"))
    W("-" * 108 + "\n")
    for r, a_ in enumerate(np.argsort(vv)[::-1][:20], 1):
        W("%6d %8d %8d %-20s | %13.6e | %10.5f %10.5f %8.3f\n"
          % (r, int(ii[a_]), int(jj[a_]), ETICHETTE[cls[a_]], vv[a_], d[a_], d0[a_], Ld[a_]))
    W("\nI 20 ARCHI PIU' TIRATI GIU' -- e sono questi che portano il saldo, perche' il saldo\n")
    W("  totale e' NEGATIVO e vive sul confine:\n")
    W("%6s %8s %8s %-20s | %13s | %10s %10s %8s\n"
      % ("rango", "nodo i", "nodo j", "regione", "spinta cumul.", "d", "d0", "L/d"))
    W("-" * 108 + "\n")
    for r, a_ in enumerate(np.argsort(vv)[:20], 1):
        W("%6d %8d %8d %-20s | %13.6e | %10.5f %10.5f %8.3f\n"
          % (r, int(ii[a_]), int(jj[a_]), ETICHETTE[cls[a_]], vv[a_], d[a_], d0[a_], Ld[a_]))

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
