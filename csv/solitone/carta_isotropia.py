# -*- coding: utf-8 -*-
r"""**L'ISOTROPIA DELLA DISPERSIONE: A QUALE LUNGHEZZA D'ONDA IL RETICOLO SI VEDE** *(Luca `2026-11-04` `20:18`-`22:26`; il task history `doc/TASK_HISTORY/2026-11-05_forma_isotropia_corona.md`, 1.2)*
    python csv/solitone/carta_isotropia.py > doc/referti_l2/isotropia_dispersione.txt
### **Nessuna corsa:** `A(k)` sul vuoto `F3` col tick CONGELATO di `DV.un_tick` *(la forma `S1`, come `carta_bordo`)*, dalla risposta a un impulso in un nodo; **per un `k` qualsiasi**
`A(k) = somma_r R(r) e^{-i k . r}` *(lo spostamento `r` per immagine minima: la risposta di un tick ha supporto corto)*. La banda `B` *(`DV.GRUPPI`, indici `10`, `11` delle fasi ordinate per
`-arg`)*, `omega = fase per tick / s`; su cerchi di `|k|` *(`N_K` raggi in scala logaritmica da `K_MIN` a `k_M = 2 pi / sqrt 3`, `N_TH` direzioni)*: l'anisotropia `(max - min) / |media|` di `omega` e di
`|v_g|` *(differenze centrali in `k`)*, la componente a sei lobi, la lunghezza d'onda `2 pi / |k|` in nodi.
### **I DEVE:** `DI-G` *(mio)* `A(k)` per `k` qualsiasi = `fft2` di `DV.matrice` sui `k` della griglia entro `TOLL_A`; `DI-T` *(mio)* la risposta a un impulso in un altro nodo, riportata indietro, = quella
dal nodo `0` entro `TOLL_A` *(il tick congelato invariante per traslazione)*; `DI0` la simmetria `D6`: `omega(theta + 60) = omega(theta)` su ogni cerchio con l'escursione sopra `ESC_MIN`, entro `TOLL_D6`
dell'escursione; `DI1` la pendenza di `ln` anisotropia di `omega` contro `ln |k|` fra `FIT` = `6` entro `TOLL_P` *(la derivazione nel task history; se `10` e `11` sono un doppietto a `Gamma` non si legge)*;
`DI1-P` *(mio)* il triangolare di prova da' `6`; `DI1-F` *(deve fallire)* il quadrato di prova da' `6`.
"""
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))
import solitone  # noqa: E402,F401  (i percorsi)

N_K = 60                       # ### task history 1.2: i raggi dei cerchi
N_TH = 144                     # ### task history 1.2: le direzioni (il mandato: almeno 72); 60 gradi = 24 passi esatti
K_MIN = 0.005                  # ### task history 1.2: il raggio piu' piccolo, in unita' di k_M
FIT = (0.02, 0.2)              # ### task history 1.2: l'intervallo del fit, in unita' di k_M
TOLL_A = 1e-12                 # ### task history 1.2: DI-G, DI-T
TOLL_D6 = 1e-9                 # ### task history 1.2: DI0, relativo all'escursione ...
ESC_MIN = 1e-6                 # ### ... sui cerchi con l'escursione sopra questa (la precisione delle fasi ~1e-15: 1e-9 relativo vuole un'escursione >= 1e-6)
TOLL_P = 0.5                   # ### task history 1.2: DI1, DI1-P, DI1-F
GAP_DOPPIETTO = 1e-8           # ### task history 1.2: sotto, 10 e 11 sono un doppietto a Gamma
SOGLIE = (1e-2, 1e-3)          # ### Luca: la lunghezza d'onda sotto cui l'anisotropia supera l'1% e lo 0.1%
PROVA = (3.0, 0.5)             # ### task history 1.2: omega0, t dei reticoli di prova (numeri di PROTOCOLLO, fuori dalla fisica)
DK = 1e-4                      # ### task history 1.2: il passo relativo delle differenze centrali per v_g

OK = [0, 0]
FALLITE = []


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    if not passa:
        FALLITE.append(che)
    print("  %-120s %s   %s" % (che[:120], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return passa


def risposte(z, F3, nodo):
    """### **Le risposte a un impulso nel `nodo`, componente per componente:** `(12, n, 12)`, `R[c]` lo stato dopo un tick diviso per l'ampiezza; lo stato della scena rimesso al suo posto."""
    import _dove_va_la_materia as DV
    n = z["inc"].n
    salvato = {k: v.copy() for k, v in z["st"].items() if isinstance(v, np.ndarray)}
    R = np.empty((12, n, 12), dtype=complex)
    try:
        for c in range(12):
            p = np.zeros((n, 12), dtype=complex)
            p[nodo, c] = DV.AMP
            R[c] = DV.un_tick(z, F3, p) / DV.AMP
    finally:
        for k, v in salvato.items():
            z["st"][k][...] = v
    return R


def supporto(R, L, A1, A2):
    """### **I nodi dove la risposta non e' zero, con lo spostamento per immagine minima dal nodo `0`:** `(indici, r cartesiano (m, 2), d1, d2)`."""
    nz = np.flatnonzero(np.any(np.abs(R) > 0.0, axis=(0, 2)))
    m1, m2 = nz // L, nz % L
    d1 = (m1 + L // 2) % L - L // 2
    d2 = (m2 + L // 2) % L - L // 2
    return nz, d1[:, None] * A1 + d2[:, None] * A2, d1, d2


def matrice_k(Rs, rs, k):
    """### **`A(k)` `(12, 12)` per un `k` cartesiano qualsiasi:** `A[a, c] = somma_r R[c][r, a] e^{-i k . r}`."""
    f = np.exp(-1j * (rs @ k))
    return np.einsum("cra,r->ac", Rs, f)


def fasi_B(Rs, rs, k, idx):
    ev = np.linalg.eigvals(matrice_k(Rs, rs, k))
    f = np.sort(-np.angle(ev))
    return f[list(idx)]


def anisotropie(om, vv, th):
    """### **Per un cerchio:** l'anisotropia di `omega` e di `|v_g|`, la componente a sei lobi, la fase dei sei lobi, l'escursione, e lo scarto della rotazione di `60` gradi."""
    me = abs(float(np.mean(om)))
    esc = float(om.max() - om.min())
    s6 = len(th) // 6
    rot = float(np.max(np.abs(np.roll(om, -s6) - om)))
    c = np.fft.fft(om) / len(om)
    non6 = float(np.max(np.abs(np.delete(c, np.arange(0, len(om), 6)))))
    c6 = np.mean(om * np.exp(-6j * th))
    return {"media": float(np.mean(om)), "a_om": esc / me, "a_v": float(vv.max() - vv.min()) / float(np.mean(vv)), "lobi6": abs(c6) / me, "fase6": math.degrees(np.angle(c6)) / 6.0,
            "esc": esc, "rot": rot, "non6": non6}


def pendenza(kk, aa):
    sel = (kk >= FIT[0]) & (kk <= FIT[1]) & (aa > 0)
    return float(np.polyfit(np.log(kk[sel]), np.log(aa[sel]), 1)[0]), int(sel.sum())


def cerchi(omega_di, kM, nome, s_om=1.0):
    """### **I cerchi per una dispersione `omega_di(k)`:** per ogni raggio le anisotropie; `v_g` per differenze centrali."""
    kk = kM * np.logspace(math.log10(K_MIN), 0.0, N_K)
    th = 2 * np.pi * np.arange(N_TH) / N_TH
    out = []
    for kr in kk:
        om, vv = [], []
        for t in th:
            k = kr * np.array([math.cos(t), math.sin(t)])
            h = DK * kr
            gx = (omega_di(k + [h, 0.0]) - omega_di(k - [h, 0.0])) / (2 * h)
            gy = (omega_di(k + [0.0, h]) - omega_di(k - [0.0, h])) / (2 * h)
            om.append(omega_di(k))
            vv.append(math.hypot(gx, gy))
        out.append(anisotropie(np.array(om) * s_om, np.array(vv) * s_om, th))
    return kk / kM, out


def main(argv):
    del argv
    import _dove_va_la_materia as DV
    import _presidio
    import _solitone_dal_fondo as SD
    import _vuoto_vivo_B as V
    from solitone import corsa_accensione as CA
    from solitone import toro as TO
    for m in ("__init__", "corsa_accensione", "toro"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(__file__)
    _sol, vuoto, s = V.CORSE[CA.NOME]
    kM = 2 * math.pi / math.sqrt(3.0)
    print("=" * 130)
    print("L'ISOTROPIA DELLA DISPERSIONE (Luca 2026-11-04 20:18-22:26): la banda B sul vuoto F3, il tick CONGELATO (DV.un_tick, forma S1); %s (s %g, eps %g); N_K %d N_TH %d K_MIN %g FIT %s"
          % (CA.NOME, s, V.EPS, N_K, N_TH, K_MIN, FIT))
    print("  k_M = 2 pi / sqrt 3 = %.6f (il raggio inscritto della zona di Brillouin); TOLL_A %g TOLL_D6 %g ESC_MIN %g TOLL_P %g GAP_DOPPIETTO %g; i reticoli di prova omega0 %g t %g (protocollo)"
          % (kM, TOLL_A, TOLL_D6, ESC_MIN, TOLL_P, GAP_DOPPIETTO, PROVA[0], PROVA[1]))
    print("=" * 130)
    idx = tuple(dict(DV.GRUPPI)["B"])
    A1, A2 = TO.vettori()
    with V.scena(s, vuoto, V.EPS) as (_rec, z, _phi0, _pK):
        inc, L = z["inc"], z["L"]
        F3 = SD.fondo_con_fasi(inc, L, tuple(dict(SD.FASI)["F3"]))
        R0 = risposte(z, F3, 0)
        j0 = 5 * L + 7
        Rj = risposte(z, F3, j0)
        Ag = DV.matrice(z, F3, DV.AMP)
    n = inc.n
    # ------------------------------------------------------------------ DI-T: la traslazione
    m1, m2 = np.arange(n) // L, np.arange(n) % L
    da = ((m1 - j0 // L) % L) * L + (m2 - j0 % L) % L          # il nodo m visto da j0: la risposta da j0 in m = quella da 0 in m - j0
    eT = float(np.max(np.abs(Rj - R0[:, da, :])))
    esito("DEVE PASSARE: DI-T la risposta a un impulso nel nodo %d, riportata indietro, = quella dal nodo 0 entro %g (il tick congelato su F3 invariante per traslazione)" % (j0, TOLL_A), eT <= TOLL_A, "%.3e" % eT)
    nz, rs, d1, d2 = supporto(R0, L, A1, A2)
    Rs = R0[:, nz, :]
    print("  il supporto della risposta di un tick: %d nodi; |d1|, |d2| fino a %d, %d (contro L / 2 = %d: l'immagine minima e' unica)" % (len(nz), int(np.abs(d1).max()), int(np.abs(d2).max()), L // 2))
    # ------------------------------------------------------------------ DI-G: la griglia
    rng = np.random.default_rng(0)
    eG = 0.0
    Bm = 2.0 * np.pi * np.linalg.inv(np.array([A1, A2])).T
    for _ in range(20):
        i1, i2 = int(rng.integers(L)), int(rng.integers(L))
        k = (i1 * Bm[0] + i2 * Bm[1]) / L
        eG = max(eG, float(np.max(np.abs(matrice_k(Rs, rs, k) - Ag[i1, i2]))))
    esito("DEVE PASSARE: DI-G A(k) per k qualsiasi = fft2 di DV.matrice su 20 k della griglia (seme 0), entro %g" % TOLL_A, eG <= TOLL_A, "%.3e" % eG)
    # ------------------------------------------------------------------ Gamma: il doppietto?
    fG = np.sort(-np.angle(np.linalg.eigvals(matrice_k(Rs, rs, np.zeros(2)))))
    gap = float(fG[idx[1]] - fG[idx[0]])
    print("  a Gamma le fasi per tick delle 12 bande: %s" % " ".join("%+.6f" % x for x in fG))
    print("  ### la banda B (indici %s) a Gamma: %+.12f, %+.12f; lo scarto %.3e (%s)" % (idx, fG[idx[0]], fG[idx[1]], gap, "### UN DOPPIETTO: DI1 non si legge" if gap < GAP_DOPPIETTO else "non degeneri"))
    print("-" * 130)
    risultati = {}
    for b in (0, 1):
        def om_b(k, b=b):
            return float(fasi_B(Rs, rs, k, idx)[b]) / s
        kk, out = cerchi(om_b, kM, "B%d" % idx[b])
        risultati[idx[b]] = (kk, out)
        print("### LA BANDA %d (omega = fase per tick / s; per unita' di tempo)" % idx[b])
        print("  %9s %9s %12s %12s %12s %10s %12s %12s %12s" % ("|k|/k_M", "lambda", "omega medio", "an. omega", "an. |v_g|", "6 lobi", "fase6 (gr)", "rot 60", "non-6"))
        for kr, o in zip(kk, out):
            print("  %9.4f %9.2f %+12.6f %12.3e %12.3e %10.3e %+12.2f %12.3e %12.3e" % (kr, 2 * math.pi / (kr * kM), o["media"], o["a_om"], o["a_v"], o["lobi6"], o["fase6"], o["rot"], o["non6"]))
    print("-" * 130)
    # ------------------------------------------------------------------ DI0
    peggio = 0.0
    usati = 0
    for b, (kk, out) in risultati.items():
        for o in out:
            if o["esc"] >= ESC_MIN:
                usati += 1
                peggio = max(peggio, o["rot"] / o["esc"], o["non6"] / o["esc"])
    esito("DEVE PASSARE: DI0 la simmetria D6: omega(theta + 60) = omega(theta) e le armoniche non multiple di 6 nulle, entro %g dell'escursione (i cerchi con l'escursione >= %g)" % (TOLL_D6, ESC_MIN),
          usati > 0 and peggio <= TOLL_D6, "%d cerchi; il peggiore %.3e" % (usati, peggio))
    d6 = usati > 0 and peggio <= TOLL_D6
    # ------------------------------------------------------------------ DI1, DI1-P, DI1-F
    for b, (kk, out) in risultati.items():
        p_om, nn = pendenza(kk, np.array([o["a_om"] for o in out]))
        p_v, _nn = pendenza(kk, np.array([o["a_v"] for o in out]))
        print("  la banda %d: la pendenza dell'anisotropia di omega %.3f, di |v_g| %.3f (%d raggi fra %s k_M); attese 6 e 4 (task history 1.2)" % (b, p_om, p_v, nn, FIT))
        if gap >= GAP_DOPPIETTO and d6:
            esito("DEVE PASSARE: DI1 la banda %d: la pendenza dell'anisotropia di omega = 6 entro %g" % (b, TOLL_P), abs(p_om - 6.0) <= TOLL_P, "%.3f" % p_om)
        else:
            print("  ### DI1 la banda %d: NON SI LEGGE (%s)" % (b, "il doppietto a Gamma" if gap < GAP_DOPPIETTO else "DI0 fallito: la premessa D6 cade"))
    w0, t = PROVA
    vic_tri = (A1, A2, A1 + A2)

    def om_tri(k):
        return w0 - 2 * t * sum(math.cos(float(k @ a)) for a in vic_tri)

    def om_qua(k):
        return w0 - 2 * t * (math.cos(float(k[0])) + math.cos(float(k[1])))
    kt, ot = cerchi(om_tri, kM, "tri")
    kq, oq = cerchi(om_qua, kM, "qua")
    pt, _n1 = pendenza(kt, np.array([o["a_om"] for o in ot]))
    pq, _n2 = pendenza(kq, np.array([o["a_om"] for o in oq]))
    pvt, _n3 = pendenza(kt, np.array([o["a_v"] for o in ot]))
    pvq, _n4 = pendenza(kq, np.array([o["a_v"] for o in oq]))
    print("  i reticoli di prova: il triangolare, la pendenza di omega %.3f, di |v_g| %.3f (attese 6, 4); il quadrato %.3f, %.3f (attese 4, 2)" % (pt, pvt, pq, pvq))
    esito("DEVE PASSARE: DI1-P il triangolare di prova: la pendenza dell'anisotropia di omega = 6 entro %g" % TOLL_P, abs(pt - 6.0) <= TOLL_P, "%.3f" % pt)
    esito("DEVE FALLIRE: DI1-F il quadrato di prova: la pendenza dell'anisotropia di omega = 6 entro %g" % TOLL_P, not abs(pq - 6.0) <= TOLL_P, "%.3f" % pq)
    # ------------------------------------------------------------------ il risultato principale
    print("-" * 130)
    print("### LA LUNGHEZZA D'ONDA SOTTO CUI L'ANISOTROPIA SUPERA LA SOGLIA (il primo raggio, salendo in |k|, con l'anisotropia sopra; lambda = 2 pi / |k| in nodi)")
    for b, (kk, out) in risultati.items():
        for chi in ("a_om", "a_v"):
            aa = np.array([o[chi] for o in out])
            pezzi = []
            for sg in SOGLIE:
                sopra = np.flatnonzero(aa > sg)
                pezzi.append("%g: %s" % (sg, ("lambda %.2f nodi (|k|/k_M %.4f)" % (2 * math.pi / (kk[sopra[0]] * kM), kk[sopra[0]])) if len(sopra) else "mai entro k_M"))
            print("  la banda %d, %s: %s" % (b, "omega" if chi == "a_om" else "|v_g|", "; ".join(pezzi)))
    print("  ### lo spessore del bordo del solitone, per il confronto: dalla carta della forma (doc/referti_l2/forma_solitone.txt), dopo questa")
    print("=" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
