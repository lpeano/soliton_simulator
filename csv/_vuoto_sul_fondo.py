# -*- coding: utf-8 -*-
r"""**IL VUOTO SUL FONDO, SULLA CARTA: LO SPETTRO, IL SEGNO, L'ENERGIA** *(la parte 2 `a`-`b`-`c-i` del mandato dopo `15df5c63`; [[PROGETTO-MASSA-COLLETTIVA]];
il task history `doc/TASK_HISTORY/2026-10-27_vuoto_sul_fondo.md`)*: ### **la matrice del generatore del vuoto DAL CODICE** *(per polarizzazione di
`energia_pesata.termini_di_h`, la materia a zero)*, ### **il suo spettro, dove stanno il vuoto uniforme e il fondo; il fondo UNIFORME IN MODULO
costruito** *(il flusso costante per direzione del reticolo)*; ### **il tick sui due stati; il segno** *(i due termini separati, la materia)*; ### **l'energia a `L 48`.**

> ### **In memoria; nessun file del nucleo.** ### **Importati, non copiati:** `_scomposizione_solitone` *(`scena`, `stato_uniforme`, `PAR`)*, `_triangoli_forza.coppia_K`,
> `_solitone_vuoto_congelato.S`, `_triangoli_bassa_energia.conv`, `energia_pesata.termini_di_h`, `tick.percorri_tick`, `scena_l2.VUOTO_PER_ESTREMITA`.

Gira con:  python csv/_vuoto_sul_fondo.py > doc/referti_l2/vuoto_sul_fondo.txt
"""
import io
import json
import math
import os
import sys
import time

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
_PO = os.path.join(RADICE, "primo_ordine")
for _p in (_QUI, _PO, os.path.join(_PO, "leggi")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import numpy as np                                             # noqa: E402

JSONL = os.path.join(RADICE, "doc", "referti_l2", "vuoto_sul_fondo.jsonl")
LATI = (6, 12)
L_ENERGIA = 48
ZERI = (("oggi", 0.0), ("simm", 0.5))
N_CASUALI = 5
SEME = 20261027
TOLL_T = 1e-12
TOLL_A = 1e-12
TOLL_M = 1e-9
TOLL_F = 1e-12
TOLL_MOLT = 1e-9
OK = [0, 0]
FALLITE = []


def esito(che, passa, nota="", deve=True):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    if deve and not passa:
        FALLITE.append(che)
    print("  %-110s %s   %s" % (che[:110], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return passa


def scrivi(r):
    with io.open(JSONL, "a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n")


def energia(mot, st, campo, quale):
    """### **L'energia del codice** *(`termini_di_h`)* ### **del campo `campo` con l'ALTRO a zero:** ### `quale` = `"tutto"`, `"nodo"`, `"arco"`."""
    import energia_pesata as EP
    import _scomposizione_solitone as SC
    s = dict(st)
    altro = "psi_h" if campo == "phi_h" else "phi_h"
    s[altro] = np.zeros_like(st[altro])
    pn, pa = EP.termini_di_h(mot, s, SC.PAR)
    if quale == "nodo":
        return math.fsum(np.asarray(pn, float).tolist())
    if quale == "arco":
        return math.fsum(np.asarray(pa, float).tolist())
    return math.fsum(np.asarray(pn, float).tolist()) + math.fsum(np.asarray(pa, float).tolist())


def matrice(inc, mot, st, campo, quale):
    """### **`H` per polarizzazione, sulle coppie di componenti dello stesso nodo o dello stesso arco** *(il supporto della forma)*."""
    forma = st[campo].shape
    D = int(np.prod(forma))
    comp = 1 if len(forma) == 1 else forma[1]
    st = dict(st)
    salvo = st[campo]
    st[campo] = np.zeros(forma, dtype=complex)
    v = st[campo].reshape(-1)

    def E(idx, val):
        v[...] = 0.0
        for i, x in zip(idx, val):
            v[i] += x
        return energia(mot, st, campo, quale)
    H = np.zeros((D, D), dtype=complex)
    for i in range(D):
        H[i, i] = E([i], [1.0])
    gruppi = []
    per_nodo = {}
    for e, k in enumerate(inc.nodo):
        per_nodo.setdefault(int(k), []).append(e)
    for es in per_nodo.values():
        gruppi.append([e * comp + c for e in es for c in range(comp)])
    for a in range(inc.m):
        gruppi.append([e * comp + c for e in (2 * a, 2 * a + 1) for c in range(comp)])
    fatte = set()
    for g in gruppi:
        for x in range(len(g)):
            for y in range(x + 1, len(g)):
                i, j = g[x], g[y]
                if (i, j) in fatte:
                    continue
                fatte.add((i, j))
                re = (E([i, j], [1.0, 1.0]) - H[i, i].real - H[j, j].real) / 2.0
                im = -(E([i, j], [1.0, 1j]) - H[i, i].real - H[j, j].real) / 2.0
                H[i, j] = re + 1j * im
                H[j, i] = re - 1j * im
    st[campo] = salvo
    return H


def fondo_uniforme(inc, L, valore):
    """### **Il flusso COSTANTE per direzione del reticolo:** ### **l'estremita' alla CODA dell'arco `+valore`, alla TESTA `-valore`** *(ogni nodo: una coda e una testa per direzione)*."""
    n = inc.n
    v = np.arange(n)
    m1, m2 = v // L, v % L
    phi = np.zeros(2 * inc.m, dtype=complex)
    direzioni = set()
    for a in range(inc.m):
        i, j = int(inc.nodo[2 * a]), int(inc.nodo[2 * a + 1])
        d = ((int(m1[j] - m1[i]) + L // 2) % L - L // 2, (int(m2[j] - m2[i]) + L // 2) % L - L // 2)
        pos = d if (d[0] > 0 or (d[0] == 0 and d[1] > 0)) else (-d[0], -d[1])
        direzioni.add(pos)
        segno = 1.0 if pos == d else -1.0      # ### `+1`: il nodo `i` e' la CODA
        phi[2 * a] = segno * valore
        phi[2 * a + 1] = -segno * valore
    return phi, sorted(direzioni)


def main(argv):
    del argv
    import _presidio
    import _universalita_massa as UM
    import _scomposizione_solitone as SC
    import _solitone_vuoto_congelato as VC
    import _triangoli_bassa_energia as BE
    import _triangoli_forza as TF
    import composizione as CM
    import scena_l2 as SL
    import tick as TK
    _presidio.avvia(__file__)
    print("=" * 130)
    print("IL VUOTO SUL FONDO, SULLA CARTA: la matrice del generatore del vuoto dal codice, lo spettro, il fondo uniforme in modulo, il tick, il segno, l'energia a L %d" % L_ENERGIA)
    print("=" * 130)
    blobs = {p: UM.blob(p) for p in ("soliton_simulator.py", "csv/_vuoto_sul_fondo.py", "csv/_scomposizione_solitone.py", "primo_ordine/energia_pesata.py", "primo_ordine/tick.py",
                                     "primo_ordine/flussi_parziali.py")}
    print("  il passo: %d pezzi, impronta %s (intatto); i blob nel repo: %s" % (len(CM.ORDINE), CM.IMPRONTA, "; ".join("%s %s" % (k, v["sha1-BYTE"]) for k, v in blobs.items())))
    print("  la configurazione: LATI %s L_ENERGIA %d ZERI %s N_CASUALI %d SEME %d TOLL_T %g TOLL_A %g TOLL_M %g TOLL_F %g TOLL_MOLT %g; S %g; VUOTO_PER_ESTREMITA %g; eps 0"
          % (LATI, L_ENERGIA, ZERI, N_CASUALI, SEME, TOLL_T, TOLL_A, TOLL_M, TOLL_F, TOLL_MOLT, VC.S, SL.VUOTO_PER_ESTREMITA))
    print("  la forma letta dal codice: per nodo -pi (nrm_phi - pu_phi), per arco -pi (|f0|^2 + |f1|^2 - 2 Re f0* f1)/2; lo zero simmetrico sposta di + 2 pi lambda = + pi per unita' di norma")
    print("-" * 130)
    if os.path.exists(JSONL):
        os.remove(JSONL)
    scrivi({"tipo": "testata", "blobs": blobs, "impronta": CM.IMPRONTA})
    rng = np.random.default_rng(SEME)
    ok_t, ok_a, ok_m, ok_f = True, True, True, True
    note_t, note_a, note_m, note_f = [], [], [], []
    for L in LATI:
        t0 = time.time()
        inc, mot, st, par = SC.scena(L)
        st["psi_h"][...] = 0.0
        H = matrice(inc, mot, st, "phi_h", "tutto")
        D = H.shape[0]
        peg = 0.0
        for _k in range(N_CASUALI):
            x = rng.standard_normal(D) + 1j * rng.standard_normal(D)
            s = dict(st)
            s["phi_h"] = x.copy()
            ec = energia(mot, s, "phi_h", "tutto")
            em = float(np.real(np.vdot(x, H @ x)))
            peg = max(peg, abs(ec - em) / abs(ec))
        ok_t &= peg <= TOLL_T
        note_t.append("L %d %.1e" % (L, peg))
        w = np.linalg.eigvalsh(H)
        vu = np.full(D, SL.VUOTO_PER_ESTREMITA, dtype=complex)
        eu = float(np.real(np.vdot(vu, H @ vu)) / np.real(np.vdot(vu, vu)))
        ru = float(np.linalg.norm(H @ vu - eu * vu) / np.linalg.norm(vu))
        ok_a &= ru <= TOLL_A
        note_a.append("L %d %.1e" % (L, ru))
        ok_m &= abs(eu - w.max()) <= TOLL_M
        note_m.append("L %d E_u %.12f max %.12f" % (L, eu, w.max()))
        vf, dirs = fondo_uniforme(inc, L, SL.VUOTO_PER_ESTREMITA)
        ef = float(np.real(np.vdot(vf, H @ vf)) / np.real(np.vdot(vf, vf)))
        rf = float(np.linalg.norm(H @ vf - ef * vf) / np.linalg.norm(vf))
        fondo = abs(ef - w.min()) <= TOLL_M and rf <= TOLL_F
        ok_f &= fondo
        note_f.append("L %d E_f %.12f min %.12f res %.1e" % (L, ef, w.min(), rf))
        m_max = int(np.sum(w >= w.max() - TOLL_MOLT))
        m_min = int(np.sum(w <= w.min() + TOLL_MOLT))
        nodo_s = np.zeros(inc.n, dtype=complex)
        np.add.at(nodo_s, inc.nodo, vf)
        tors = np.angle(np.conj(vf[1::2]) * vf[0::2])
        print("### L %d: %d nodi, %d archi, %d estremita' (%.0f s); le direzioni del reticolo %s" % (L, inc.n, inc.m, D, time.time() - t0, dirs))
        print("  il controllo: E del codice contro phi^+ H phi su %d stati casuali, il peggiore %.2e relativo" % (N_CASUALI, peg))
        print("  lo spettro per unita' di norma (lo zero di oggi): da %.12f (molteplicita' %d) a %.12f (molteplicita' %d); allo zero simmetrico + pi: da %.12f a %.12f"
              % (w.min(), m_min, w.max(), m_max, w.min() + math.pi, w.max() + math.pi))
        print("  il vuoto UNIFORME: il quoziente %.12f, il residuo %.2e" % (eu, ru))
        print("  il FONDO UNIFORME IN MODULO (il flusso costante per direzione): il quoziente %.12f, il residuo %.2e; |phi| da %.6f a %.6f; la somma per nodo al massimo %.1e; la torsione sugli archi da %.6f a %.6f (in valore assoluto)"
              % (ef, rf, float(np.abs(vf).min()), float(np.abs(vf).max()), float(np.abs(nodo_s).max()), float(np.abs(tors).min()), float(np.abs(tors).max())))
        istog = np.unique(np.round(w, 9), return_counts=True)
        print("  i livelli distinti (arrotondati a 1e-9): %d; i piu' bassi %s; i piu' alti %s"
              % (len(istog[0]), ["%.6f x%d" % (a, b) for a, b in zip(istog[0][:4], istog[1][:4])], ["%.6f x%d" % (a, b) for a, b in zip(istog[0][-4:], istog[1][-4:])]))
        Hn = matrice(inc, mot, st, "phi_h", "nodo")
        Ha = matrice(inc, mot, st, "phi_h", "arco")
        wn, wa = np.linalg.eigvalsh(Hn), np.linalg.eigvalsh(Ha)
        print("  (b) i due termini SEPARATI: il nodo da %.12f a %.12f, l'arco da %.12f a %.12f; la somma ricostruisce H: %.1e"
              % (wn.min(), wn.max(), wa.min(), wa.max(), float(np.abs(Hn + Ha - H).max())))
        scrivi({"tipo": "spettro", "L": L, "D": D, "controllo": peg, "min": float(w.min()), "max": float(w.max()), "molt_min": m_min, "molt_max": m_max, "E_uniforme": eu, "res_uniforme": ru,
                "E_fondo": ef, "res_fondo": rf, "nodo": [float(wn.min()), float(wn.max())], "arco": [float(wa.min()), float(wa.max())]})
        # ------------------------------------------------------------------ il tick sui due stati
        for nome, lam in ZERI:
            for etich, stato in (("uniforme", vu), ("fondo", vf)):
                s = {k: (x.copy() if hasattr(x, "copy") else x) for k, x in st.items()}
                s["psi_h"][...] = 0.0
                s["phi_h"][...] = stato
                with BE.conv(nome):
                    TK.percorri_tick(s, mot, par, (), None, len(CM.ORDINE))
                ov = np.vdot(stato, s["phi_h"])
                th = float(np.angle(ov))
                res = float(np.linalg.norm(s["phi_h"] - np.exp(1j * th) * stato) / np.linalg.norm(stato))
                e = eu if etich == "uniforme" else ef
                atteso = -VC.S * (e + 2 * math.pi * lam)
                scarto = float(np.angle(np.exp(1j * (th - atteso))))
                print("  il tick (%s) sul %-8s: il residuo da autostato %.2e; la fase %+.12f contro -s (E + 2 pi lambda) %+.12f (lo scarto mod 2 pi %.1e)" % (nome, etich, res, th, atteso, scarto))
                scrivi({"tipo": "tick", "L": L, "zero": nome, "stato": etich, "residuo": res, "fase": th, "attesa": atteso, "scarto": scarto})
        # ------------------------------------------------------------------ la materia (b)
        if L == LATI[0]:
            sm = dict(st)
            sm["phi_h"] = np.zeros_like(st["phi_h"])
            Hm = matrice(inc, mot, sm, "psi_h", "tutto")
            wm = np.linalg.eigvalsh(Hm)
            Q = TF.coppia_K(0.0, VC.S)[0]["Q"][:, 0]
            v = np.arange(inc.n)
            _i, _m, stu = SC.stato_uniforme(L, Q, v // L, v % L)
            xu = stu["psi_h"].reshape(-1)
            ek = float(np.real(np.vdot(xu, Hm @ xu)) / np.real(np.vdot(xu, xu)))
            sotto = int(np.sum(wm < ek - TOLL_MOLT))
            sopra = int(np.sum(wm > ek + TOLL_MOLT))
            print("  (b) LA MATERIA a L %d (il vuoto a zero, eps 0): lo spettro da %.6f a %.6f; lo stato uniforme della materia (K) %.6f: %d livelli sotto e %d sopra (su %d)"
                  % (L, wm.min(), wm.max(), ek, sotto, sopra, len(wm)))
            print("      col segno capovolto (-H) lo stesso stato sarebbe a %.6f, con %d livelli sotto e %d sopra" % (-ek, sopra, sotto))
            scrivi({"tipo": "materia", "L": L, "min": float(wm.min()), "max": float(wm.max()), "e_K": ek, "sotto": sotto, "sopra": sopra})
    print("-" * 130)
    print("### (c-i) L'ENERGIA A L %d (dal codice, i due stati costruiti)" % L_ENERGIA)
    inc, mot, st, par = SC.scena(L_ENERGIA)
    st["psi_h"][...] = 0.0
    vu = np.full(2 * inc.m, SL.VUOTO_PER_ESTREMITA, dtype=complex)
    vf, _d = fondo_uniforme(inc, L_ENERGIA, SL.VUOTO_PER_ESTREMITA)
    V = float(np.sum(np.abs(vu) ** 2))
    out = {}
    for etich, stato in (("uniforme", vu), ("fondo", vf)):
        s = dict(st)
        s["phi_h"] = stato.copy()
        E = energia(mot, s, "phi_h", "tutto")
        out[etich] = E
        print("  il %-8s: V %.1f; E (zero di oggi) %.6f = %.12f per unita' di norma; allo zero simmetrico %.6f" % (etich, float(np.sum(np.abs(stato) ** 2)), E, E / V, E + math.pi * V))
    print("  la differenza fondo - uniforme: %.6f = %.12f per unita' di norma (non dipende dallo zero)" % (out["fondo"] - out["uniforme"], (out["fondo"] - out["uniforme"]) / V))
    scrivi({"tipo": "energia", "L": L_ENERGIA, "V": V, "E_uniforme": out["uniforme"], "E_fondo": out["fondo"]})
    print("-" * 130)
    print("### I CRITERI")
    esito("DEVE PASSARE (t): la matrice ridà l'energia del codice su %d stati casuali entro %g relativo" % (N_CASUALI, TOLL_T), ok_t, "; ".join(note_t))
    esito("DEVE PASSARE (a): il vuoto uniforme e' un autostato del generatore (residuo <= %g)" % TOLL_A, ok_a, "; ".join(note_a))
    esito("PUO' FALLIRE (m): il vuoto uniforme e' l'autovalore MASSIMO (entro %g)" % TOLL_M, ok_m, "; ".join(note_m), deve=False)
    esito("PUO' FALLIRE (f): esiste un fondo uniforme in modulo: il flusso costante per direzione e' sul minimo (entro %g) con residuo <= %g" % (TOLL_M, TOLL_F), ok_f, "; ".join(note_f), deve=False)
    print("-" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    scrivi({"tipo": "esito", "passano": OK[0], "totale": OK[1], "deve_fallite": FALLITE, "fondo_uniforme": ok_f})
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
