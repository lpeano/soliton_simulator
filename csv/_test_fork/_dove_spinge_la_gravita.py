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
    ACC = {"v": np.zeros(0)}     # cumulato per arco di S09 (cresce in coda)
    GIRI = {}
    CRESCITA = {"pad": 0, "salta": 0}

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
    v = ACC["v"]
    if viol:
        W("\n*** IL PREFISSO NON REGGE (prime violazioni ai passi %s). LA TABELLA NON SI STAMPA:\n"
          % viol[:8])
        W("    sarebbero numeri VERI sommati sull'ARCO SBAGLIATO. Dichiarato, non nascosto. ***\n")
    elif v.size == 0:
        W("\n*** nessun cumulato: `S09` non ha scritto. ***\n")
    else:
        ii = np.asarray(net.i); jj = np.asarray(net.j)
        L = min(len(v), len(ii))
        vv = v[:L]
        cls = classe_arco(ii[:L], jj[:L])
        d = np.asarray(net.d, dtype=float)[:L]
        d0 = np.asarray(net.d0, dtype=float)[:L]
        pos = np.asarray(net.pos, dtype=float)
        Ld = np.linalg.norm(pos[jj[:L]] - pos[ii[:L]], axis=1) / np.maximum(d, 1e-300)
        W("\nCONCENTRAZIONE: la frazione della spinta POSITIVA totale che sta nell'1 %% di archi\n")
        W("  piu' spinti. Il valore sotto IPOTESI NULLA (spinta uniforme) e' 0.01.\n")
        cpos = concentrazione(vv)
        W("  misurata = %.5f    nullo = 0.01    rapporto = %.1fx\n"
          % (cpos, cpos / 0.01 if np.isfinite(cpos) else float("nan")))
        W("\n%6s %8s %8s %-20s | %13s | %10s %10s %8s\n"
          % ("rango", "nodo i", "nodo j", "regione", "spinta cumulata", "d", "d0", "L/d"))
        W("-" * 108 + "\n")
        ordine = np.argsort(vv)[::-1][:20]
        for r, a_ in enumerate(ordine, 1):
            W("%6d %8d %8d %-20s | %13.6e | %10.5f %10.5f %8.3f\n"
              % (r, int(ii[a_]), int(jj[a_]), ETICHETTE[cls[a_]], vv[a_],
                 d[a_], d0[a_], Ld[a_]))
        W("\ne i 5 archi piu' TIRATI GIU', per contrasto:\n")
        for r, a_ in enumerate(np.argsort(vv)[:5], 1):
            W("%6d %8d %8d %-20s | %13.6e | %10.5f %10.5f %8.3f\n"
              % (r, int(ii[a_]), int(jj[a_]), ETICHETTE[cls[a_]], vv[a_],
                 d[a_], d0[a_], Ld[a_]))

    W("\nLIMITI: UN seme, UNA scena, %d passi dalla semina. E questa misura dice DOVE la spinta\n"
      % fatti)
    W("  arriva, NON se spegnerla cambi il sistema: per quello servono `G3` e `G4`.\n")
    o.close()
    print(io.open(OUT, encoding="utf-8").read())
    return 0


if __name__ == "__main__":
    sys.exit(main())
