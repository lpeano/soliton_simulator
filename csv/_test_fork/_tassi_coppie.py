# -*- coding: utf-8 -*-
"""FASE B — I DUE TASSI: quanto in fretta nasce l'ordine, e quanto in fretta muore?

LA DOMANDA
----------
La FASE A ha stabilito che alla mitosi il figlio eredita il Bloch del padre per COPIA ESATTA
(chi = 0.0000), che nasce ADIACENTE, e che la PARENTELA e' ricostruibile. Quindi l'ordine di spin
non manca: NASCE a ogni nascita e viene DISTRUTTO. Qui si misurano i due tassi.

  tau_dec  tempo perche' una coppia padre-figlio, nata a chi = 0, arrivi a 1-1/e del percorso
           verso chi = 90 (il valore di direzioni CASUALI).
  tau_mit  tempo medio fra due mitosi NELLO STESSO VICINATO (locale: e' il tasso che compete col
           disordine locale, non quello globale).

IL CONFONDENTE, e come si separa
--------------------------------
La coppia nasce ADIACENTE, quindi la sua decorrelazione mescola DUE effetti:
  (a) il disordine vero (rumore + precessione mutua);
  (b) il fatto che i due si ALLONTANANO - l'espansione li separa e il kernel e^{-d/lambda} li
      disaccoppia, cosi' smettono di interagire.
Senza separarli, tau_dec e' AMBIGUO. Per questo si misura, alla stessa eta':
  - chi(eta')                        la decorrelazione;
  - la distanza padre-figlio;
  - se l'ARCO DIRETTO fra i due e' ancora vivo (la mitosi successiva lo suddivide).
Se chi arriva a 90 mentre i due sono ancora vicini e connessi, e' DISORDINE. Se ci arriva solo
dopo che si sono separati, e' DISACCOPPIAMENTO.

PUREZZA (sigillo prima dell'uso, par.2.3)
-----------------------------------------
L'osservatore legge SOLO array di stato: `net.i`, `net.j`, `net._nb`, `net.pos`, `net.d`, `net.n`.
NON chiama `calcola_psi()`, `ritmo()`, `_pesi()`, `_lam_archi()`, `lambda_nodi()` - tutte mutano
cache di continuita' lette dalla dinamica (`psi`, `_psi_prec`, `_chi_core_nodi`) o innescano
`massa_critica_adattiva`. Non consuma `net.rng`. Il sigillo (`--sigillo`) lo DIMOSTRA invece di
assumerlo, confrontando due run identici con e senza osservatore, stato dell'RNG incluso.

VALORE-NULL, sempre accanto (CLAUDE.md par.9)
---------------------------------------------
direzioni di Bloch CASUALI -> chi = 90.000 +- 39.171 gradi. Il bersaglio 1-1/e vale 56.870 gradi.

USO
---
python csv/_test_fork/_tassi_coppie.py --sigillo          # sigillo di byte-identita'
python csv/_test_fork/_tassi_coppie.py --passi 400        # la misura
"""
import argparse
import contextlib
import io
import os
import sys

import numpy as np

RADICE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

CHI_NULL_MEDIA = 90.000
CHI_NULL_STD = 39.171
CHI_BERSAGLIO = CHI_NULL_MEDIA * (1.0 - 1.0 / np.e)     # 56.870 gradi: 1-1/e del percorso
ETA_MAX = 80                                            # oltre, la coppia non si segue piu'


def _prepara(seed, passi_dummy=1):
    """Imposta i globali dai flag del fork SENZA far ricostruire la rete a `_applica_flag`
    (niente --seed, niente --nodi: cosi' non parte il riscaldamento da 300 passi che poi
    `batch_condensazione` butterebbe via comunque). Poi costruisce la scena REALE come la
    costruisce il batch: 80 nodi + 6 passi + le masse in cerchio."""
    os.chdir(RADICE)
    sys.path.insert(0, RADICE)
    sys.argv = ["soliton_simulator.py", "--batch", "--nmasse", "3", "--sep", "8",
                "--passi", str(passi_dummy), "--ogni", "100000", "--db-ogni", "100000",
                "--campo-spinoriale", "--spinore-vivo", "--spinore-corretto", "--chi-core",
                "--calore-scal", "--deparam-orologio", "--verlet", "--cs-dinamico",
                "--csv", os.path.join(os.environ.get("TMP", "."), "_tassi.csv")]
    import soliton_simulator as S
    a = S._cli()
    S._applica_regime(a)
    with contextlib.redirect_stdout(io.StringIO()):
        S._applica_flag(a)
    return S, a


def _scena(S, seed, nmasse=3, sep=8.0):
    """La scena del batch, riprodotta: 80 nodi, 6 passi, poi `nmasse` masse in cerchio."""
    net = S.Rete(seed)
    net.semina(80)
    for _ in range(6):
        _passo(S, net)
    Nc = S.massa_critica_collasso()
    for k in range(nmasse):
        ang = np.pi * k if nmasse == 2 else 2 * np.pi * k / nmasse
        net.nuova_massa(int(Nc * 0.6), raggio=0.8,
                        centro=(sep * np.cos(ang), sep * np.sin(ang), 0.0), fase=0.0)
    return net


def _passo(S, net):
    S.scuoti_vuoto(net); net.step(); net.mitosi()
    net.rilassa_disegno(); net.memoria_hebbiana_moto()


def _angoli(U, V):
    """Angoli in gradi fra righe corrispondenti di U e V. Vettorizzato, nessuna mutazione."""
    nu = np.maximum(np.linalg.norm(U, axis=1), 1e-30)
    nv = np.maximum(np.linalg.norm(V, axis=1), 1e-30)
    c = np.clip(np.sum(U * V, axis=1) / (nu * nv), -1.0, 1.0)
    return np.degrees(np.arccos(c))


class Osservatore:
    """PURE-READ. Registra le coppie padre-figlio alla nascita e le campiona a ogni eta'."""

    def __init__(self):
        self.figli = []          # indice del figlio
        self.padri = []          # indice del padre `a` (quello da cui eredita)
        self.nascite = []        # passo di nascita
        self.arco0 = []          # (padre, figlio) per ritrovare l'arco diretto
        # accumulatori per eta': somma, conteggio
        self.chi_somma = np.zeros(ETA_MAX + 1)
        self.chi_n = np.zeros(ETA_MAX + 1)
        self.dist_somma = np.zeros(ETA_MAX + 1)
        self.arco_vivo = np.zeros(ETA_MAX + 1)
        self.nati_per_passo = []

    def registra(self, net, n_prima, passo):
        if net.n == n_prima:
            self.nati_per_passo.append(0)
            return
        ii, jj = net.i, net.j
        nuovi = 0
        for m in range(n_prima, net.n):
            genitori_i = ii[jj == m]
            gen = [int(x) for x in genitori_i if x < n_prima]
            if len(gen) != 1:
                continue                      # padre non identificabile: si scarta, non si indovina
            self.figli.append(m); self.padri.append(gen[0]); self.nascite.append(passo)
            nuovi += 1
        self.nati_per_passo.append(net.n - n_prima)

    def campiona(self, net, passo):
        if not self.figli:
            return
        f = np.asarray(self.figli); p = np.asarray(self.padri); nb = np.asarray(self.nascite)
        eta = passo - nb
        vivi = (eta >= 0) & (eta <= ETA_MAX)
        if not vivi.any():
            return
        f = f[vivi]; p = p[vivi]; eta = eta[vivi]
        chi = _angoli(net._nb[p], net._nb[f])
        dist = np.linalg.norm(net.pos[p] - net.pos[f], axis=1)
        # arco diretto padre-figlio ancora presente? (la mitosi successiva lo suddivide)
        coppie = set(zip(net.i.tolist(), net.j.tolist()))
        vivo = np.array([1.0 if ((int(a), int(b)) in coppie or (int(b), int(a)) in coppie) else 0.0
                         for a, b in zip(p, f)])
        np.add.at(self.chi_somma, eta, chi)
        np.add.at(self.chi_n, eta, 1.0)
        np.add.at(self.dist_somma, eta, dist)
        np.add.at(self.arco_vivo, eta, vivo)


# ---------------------------------------------------------------------------------------------
# SIGILLO DI BYTE-IDENTITA' (par.2.3): l'osservatore non deve mutare stato ne' RNG.
# ---------------------------------------------------------------------------------------------
CAMPI = ("pos", "phi", "phi0", "phivel", "eta", "d", "d0", "vd", "peq", "tw", "twp",
         "i", "j", "perc_chi", "perc_tw", "_nb", "_psi_spinor", "omega_s", "psi")


def sigillo(S, seed, passi):
    def corri(con_osservatore):
        net = _scena(S, seed)
        oss = Osservatore() if con_osservatore else None
        for t in range(passi):
            n_prima = net.n
            _passo(S, net)
            if oss is not None:
                oss.registra(net, n_prima, t)
                oss.campiona(net, t)
        return net

    a = corri(False)
    b = corri(True)
    print("=" * 96)
    print("SIGILLO — l'osservatore e' PURE-READ?  (%d passi, seme %d)" % (passi, seed))
    print("=" * 96)
    print("PRESIDIO: uno zero con N DIVERSO e' MANCANZA DI CONFRONTO, non identita'.")
    print("  n senza osservatore = %d   n con osservatore = %d   ->  %s"
          % (a.n, b.n, "CONFRONTABILI" if a.n == b.n else "NON CONFRONTABILI: sigillo NULLO"))
    if a.n != b.n:
        return False
    ok = True
    for c in CAMPI:
        va = getattr(a, c, None); vb = getattr(b, c, None)
        if va is None or vb is None:
            print("  %-14s assente in uno dei due -> SALTATO" % c); continue
        va = np.asarray(va); vb = np.asarray(vb)
        if va.shape != vb.shape:
            print("  %-14s SHAPE DIVERSA %s vs %s -> FAIL" % (c, va.shape, vb.shape)); ok = False; continue
        d = float(np.max(np.abs(va.astype(complex) - vb.astype(complex)))) if va.size else 0.0
        stato = "PASS" if d == 0.0 else "FAIL"
        if d != 0.0:
            ok = False
        print("  %-14s shape %-14s max|A-B| = %.3e   %s" % (c, str(va.shape), d, stato))
    sa = a.rng.bit_generator.state; sb = b.rng.bit_generator.state
    rng_ok = (sa == sb)
    print("  %-14s %s   %s" % ("stato RNG", "identico" if rng_ok else "DIVERSO",
                               "PASS" if rng_ok else "FAIL"))
    ok = ok and rng_ok
    print()
    print("SIGILLO: %s" % ("PASS — l'osservatore non tocca nulla" if ok else "FAIL — NON USARLO"))
    return ok


# ---------------------------------------------------------------------------------------------
# LA MISURA
# ---------------------------------------------------------------------------------------------
def _tau_dec(chi_media, chi_n):
    """Prima eta' in cui <chi> raggiunge 1-1/e del percorso verso 90 gradi, con interpolazione
    lineare fra i due campioni che la racchiudono. None se non ci arriva."""
    for e in range(1, len(chi_media)):
        if chi_n[e] < 3:
            continue
        if chi_media[e] >= CHI_BERSAGLIO:
            e0 = e - 1
            if chi_n[e0] < 1 or chi_media[e] == chi_media[e0]:
                return float(e)
            frazione = (CHI_BERSAGLIO - chi_media[e0]) / (chi_media[e] - chi_media[e0])
            return float(e0 + frazione)
    return None


def misura(S, seed, passi):
    net = _scena(S, seed)
    oss = Osservatore()
    print("scena: n=%d archi=%d dopo la semina delle masse (seme %d)" % (net.n, len(net.i), seed))
    for t in range(passi):
        n_prima = net.n
        _passo(S, net)
        oss.registra(net, n_prima, t)
        oss.campiona(net, t)

    chi_n = oss.chi_n
    chi_m = np.where(chi_n > 0, oss.chi_somma / np.maximum(chi_n, 1), np.nan)
    dist_m = np.where(chi_n > 0, oss.dist_somma / np.maximum(chi_n, 1), np.nan)
    arco_f = np.where(chi_n > 0, oss.arco_vivo / np.maximum(chi_n, 1), np.nan)
    nati = np.asarray(oss.nati_per_passo, float)

    print()
    print("=" * 96)
    print("B1 — TASSO DI CREAZIONE")
    print("=" * 96)
    print("coppie padre-figlio registrate : %d in %d passi" % (len(oss.figli), passi))
    print("nascite per passo              : media %.3f   mediana %.1f   max %d"
          % (nati.mean(), np.median(nati), int(nati.max()) if len(nati) else 0))
    n_fin = net.n; archi = len(net.i)
    grado_medio = 2.0 * archi / max(n_fin, 1)
    tasso_arco = nati.mean() / max(archi, 1)
    tau_mit_loc = 1.0 / max(grado_medio * tasso_arco, 1e-30)
    tau_mit_glob = n_fin / max(nati.mean(), 1e-30)
    print("N finale %d, archi %d, grado medio %.1f" % (n_fin, archi, grado_medio))
    print("tau_mit LOCALE  (una mitosi nel vicinato di un nodo) : %.1f passi" % tau_mit_loc)
    print("tau_mit globale (raddoppio del sistema)              : %.1f passi" % tau_mit_glob)

    print()
    print("=" * 96)
    print("B2 — TASSO DI DISTRUZIONE, e la separazione del confondente")
    print("=" * 96)
    print("VALORE-NULL: chi casuale = %.3f +- %.3f   |   bersaglio 1-1/e = %.3f gradi"
          % (CHI_NULL_MEDIA, CHI_NULL_STD, CHI_BERSAGLIO))
    print()
    print("  eta'   <chi> gradi     n      distanza   d/LAM   arco diretto vivo")
    for e in list(range(0, 11)) + [12, 15, 20, 30, 40, 60, 80]:
        if e >= len(chi_m) or not np.isfinite(chi_m[e]) or chi_n[e] < 1:
            continue
        print("  %4d   %10.3f  %6d   %9.3f  %6.2f   %7.1f%%"
              % (e, chi_m[e], int(chi_n[e]), dist_m[e], dist_m[e] / S.LAM, 100 * arco_f[e]))
    td = _tau_dec(chi_m, chi_n)
    print()
    print("tau_dec (eta' a cui <chi> tocca %.3f gradi) : %s"
          % (CHI_BERSAGLIO, ("%.2f passi" % td) if td is not None else "MAI raggiunto entro ETA_MAX"))

    print()
    print("=" * 96)
    print("B3 — IL VERDETTO DEL BILANCIO")
    print("=" * 96)
    if td is None:
        print("tau_dec non raggiunto: la correlazione NON muore entro %d passi -> vedi il testo." % ETA_MAX)
    else:
        r = tau_mit_loc / td
        print("tau_dec = %.2f passi   tau_mit(locale) = %.1f passi   rapporto tau_mit/tau_dec = %.1f"
              % (td, tau_mit_loc, r))
        if r > 3:
            print("-> tau_dec << tau_mit : DOMINIO DELLA DISTRUZIONE. Coerente con chi = 90 ovunque.")
        elif r > 1.0 / 3:
            print("-> tau_dec ~ tau_mit : BILANCIO IN BILICO. Il caso interessante.")
        else:
            print("-> tau_dec >> tau_mit : l'ordine DOVREBBE accumularsi e non lo fa. REPERTO.")
    return dict(chi_m=chi_m, chi_n=chi_n, dist_m=dist_m, arco_f=arco_f,
                tau_dec=td, tau_mit_loc=tau_mit_loc, tau_mit_glob=tau_mit_glob)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--passi", type=int, default=400)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--sigillo", action="store_true")
    ap.add_argument("--passi-sigillo", type=int, default=25)
    o = ap.parse_args()
    S, _ = _prepara(o.seed)
    if o.sigillo:
        ok = sigillo(S, o.seed, o.passi_sigillo)
        sys.exit(0 if ok else 1)
    misura(S, o.seed, o.passi)


if __name__ == "__main__":
    main()
