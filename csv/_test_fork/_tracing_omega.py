# -*- coding: utf-8 -*-
"""TRACING della catena di `omega` — stanare il termine che domina.

IL FATTO DA SPIEGARE (doc/CRITERIO_omega_rho.md)
-------------------------------------------------
d(log theta)/d(log inerzia) = -0.106, contro il -1 richiesto da `omega = coppia/inerzia`, misurato
TRASVERSALMENTE (un solo istante, leva x10.080): nessun ritardo puo' spiegarlo.
DOVE, nella catena, l'esponente -1 si perde?

IL CRITERIO E' SCRITTO PRIMA in doc/PREDIZIONE_tracing_omega.md (commit 075a09f):
  (I)    |correzione|/inerzia ~ -1 ma theta ~ -0.106   -> colpevole A VALLE (rilassamento / dtn / commit)
  (II-a) |correzione|/inerzia gia' ~ -0.106 e |B| cresce -> il campo scala con l'inerzia
  (II-b) ... e |B| piatto ma l'ANGOLO (B,nb) si chiude   -> geometria, non ampiezza
  (III)  nessuna delle due                               -> reperto nuovo, si riporta e si ferma

COSA E' ESATTO E COSA NO (dichiarato nel criterio, par.5)
----------------------------------------------------------
  esatti:       inerzia, omega_src, eta, tau, psi, e **B**
                (il codice costruisce B da `nb_vic = self._nb_prec`, riga 1854: il Bloch COMMITTATO)
  approssimato: `correzione = cross(B, nb)`, perche' il codice usa `nb` DOPO il rumore di riga 1847,
                che consuma `net.rng` e non e' riproducibile senza perturbare il run.
                L'errore relativo e' ~ |delta_nb|/sin(angolo), con |delta_nb| ~ amp*sqrt(2):
                si riporta `amp` accanto all'angolo, perche' il lettore possa giudicarlo.

PUREZZA
-------
Le funzioni del simulatore che servono a ricostruire i pesi (`_pesi`, e a cascata `_lam_archi`,
`lambda_nodi`, `massa_critica_adattiva`, `stato_crossover`, `_mat`) **MUTANO** cache lette dalla
dinamica (`psi`, `_S.data`, `_chi_core_nodi`). Percio' si lavora su una **COPIA PROFONDA** della
rete: ogni mutazione resta li'. Il sigillo (`--sigillo`) lo DIMOSTRA invece di assumerlo.
"""
import sys as _sys_enc  # PRESIDIO ENCODING (CLAUDE.md): lo stdout di Windows e' cp1252 e
# uccide qualunque print con un carattere non-ASCII. E' successo SETTE volte, l'ultima allo
# script che stava CONTANDO le occorrenze. Il `# -*- coding: utf-8 -*-` NON basta: riguarda il
# SORGENTE, non lo STDOUT. Questa riga lo risolve alla radice.
try:
    _sys_enc.stdout.reconfigure(encoding="utf-8")
    _sys_enc.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass
import argparse
import contextlib
import copy
import io
import os
import sys

import numpy as np

RADICE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def prepara(mostra=True):
    os.chdir(RADICE); sys.path.insert(0, RADICE)
    sys.argv = ["soliton_simulator.py", "--batch", "--nmasse", "3", "--sep", "8",
                "--passi", "1", "--ogni", "100000", "--db-ogni", "100000",
                "--campo-spinoriale", "--spinore-vivo", "--spinore-corretto", "--chi-core",
                "--calore-scal", "--deparam-orologio", "--verlet", "--cs-dinamico",
                "--fork-su2", "--fork-su2-mem",
                "--csv", os.path.join(os.environ.get("TMP", "."), "_trac.csv")]
    import soliton_simulator as S
    a = S._cli(); S._applica_regime(a)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        S._applica_flag(a)
    if mostra:
        print("CONFERMA FLAG IN-RUN: GAMMA_TURBO=%.4g  STEP2=%s  FORK_SU2=%s  MEM=%s  CS_DIN=%s  TAU_A=%.4g  DT=%.4g"
              % (S.GAMMA_TURBO, S.STEP2_OROLOGIO, S.FORK_SU2, S.FORK_SU2_MEM, S.CS_DINAMICO, S.TAU_A, S.DT))
    return S


def passo(S, net):
    S.scuoti_vuoto(net); net.step(); net.mitosi()
    net.rilassa_disegno(); net.memoria_hebbiana_moto()


def scena(S, seed):
    net = S.Rete(seed); net.semina(80)
    for _ in range(6):
        passo(S, net)
    Nc = S.massa_critica_collasso()
    for k in range(3):
        ang = 2 * np.pi * k / 3
        net.nuova_massa(int(Nc * 0.6), raggio=0.8,
                        centro=(8.0 * np.cos(ang), 8.0 * np.sin(ang), 0.0), fase=0.0)
    return net


def ingredienti(S, net):
    """Ricostruisce la catena della riga 1918 su una COPIA PROFONDA. Ritorna array per-nodo.

    PRESIDIO par.2.3: snapshot/restore COMPLETO dello stato RNG della rete VERA attorno alla misura.
    La copia ha un suo `rng`, quindi l'originale sarebbe intatto per costruzione; il ripristino
    esplicito e' cintura-e-bretelle, e il sigillo lo verifica comunque."""
    _rng0 = net.rng.bit_generator.state
    try:
        return _ingredienti(S, net)
    finally:
        net.rng.bit_generator.state = _rng0


def _ingredienti(S, net):
    lav = copy.deepcopy(net)                 # tutte le mutazioni restano QUI
    n = lav.n
    # ADEGUAMENTO DI LUNGHEZZA, come lo fa il simulatore a righe 1813-1820: dopo `semina()` gli
    # array spinoriali sono piu' corti di `n` (la semina non li estende; lo fa `_passo_spinoriale`).
    # Si riproduce la STESSA regola (nuovi nodi al polo [0,0,1], omega a zero), sulla COPIA.
    for nome, riemp in (("_nb", np.array([0.0, 0.0, 1.0])), ("_nb_prec", np.array([0.0, 0.0, 1.0]))):
        cur = getattr(lav, nome, None)
        if cur is None or len(cur) == 0:
            setattr(lav, nome, np.tile(riemp, (n, 1)))
        elif len(cur) < n:
            setattr(lav, nome, np.vstack([np.asarray(cur, float), np.tile(riemp, (n - len(cur), 1))]))
    if len(lav.omega_s) < n:
        lav.omega_s = np.vstack([np.asarray(lav.omega_s, float),
                                 np.zeros((n - len(lav.omega_s), 3))])
    # dt_n = DT*r. `ritmo()` MUTA `_psi_prec`, quindi si chiama SULLA COPIA e PRIMA di
    # `calcola_psi`, che sovrascriverebbe `psi` cambiando proprio cio' che `ritmo()` legge.
    # E' lo stesso ordine del simulatore: in `step()` `ritmo()` e' la prima cosa del passo.
    r = lav.ritmo()
    r = np.ones(n) if r is None else np.asarray(r, float)[:n]
    dtn = S.DT * r
    w = lav._pesi()
    lav.calcola_psi(w)
    i, j = lav.i, lav.j

    # --- B: ESATTO. Il codice usa nb_vic = _nb_prec (Bloch committato), non quello rumoroso.
    nbp = getattr(lav, "_nb_prec", None)
    nb_vic = np.asarray(nbp[:n], float) if (nbp is not None and len(nbp) >= n) else np.asarray(lav._nb[:n], float)
    nb = np.asarray(lav._nb[:n], float)      # per la coppia: il codice lo usa DOPO il rumore (approssimazione)
    chi_nodi = (lav.chiralita_core_locale() if S.CHI_CORE and len(lav.perc_chi) >= n
                else lav.perc_chi[:n].astype(float))
    cl_all = (chi_nodi[i] * chi_nodi[j]).astype(float)
    m = (i < n) & (j < n)
    ii, jj, wl, cl = i[m], j[m], w[m], cl_all[m]
    refl = np.where(cl[:, None] > 0, np.array([1.0, 1.0, -1.0]), np.array([1.0, 1.0, 1.0]))
    B = np.zeros((n, 3)); deg = np.zeros(n); kvic = np.zeros(n)
    np.add.at(B, ii, nb_vic[jj] * wl[:, None] * refl); np.add.at(deg, ii, wl); np.add.at(kvic, ii, 1.0)
    np.add.at(B, jj, nb_vic[ii] * wl[:, None] * refl); np.add.at(deg, jj, wl); np.add.at(kvic, jj, 1.0)
    B = B / np.maximum(deg[:, None], 1e-9)

    rs = getattr(lav, "rho_spin", None)
    rho = np.asarray(rs)[:n] if (rs is not None and len(rs) >= n) else np.abs(np.asarray(lav.psi[:n])) ** 2
    # [AGGIORNATO 2026-09-16] IL FATTORE `cs^-2`. Dalla correzione di difetto di oggi il simulatore
    # calcola `inerzia = max(rho * (CS_M/cs_nodo)^2, 1e-6)`: la derivazione `inerzia = (d/cs)^2`
    # lo impone. SENZA QUESTA RIGA la ricostruzione userebbe l'inerzia VECCHIA, e `sigma =
    # |correzione|/inerzia` sarebbe la pendenza di un sistema che non esiste piu'.
    # E' ESATTAMENTE il rischio che avevo dichiarato scegliendo di scrivere la lettura di `cs`
    # INLINE invece che in un metodo condiviso: due punti da tenere allineati a mano, e questo
    # e' il secondo. Se un giorno la legge di `cs` cambia, cambiano ENTRAMBI.
    _csp_in = getattr(lav, "_cs_nodo_prev", None)
    if _csp_in is not None and len(_csp_in) >= n:
        _cs_in = np.maximum(np.asarray(_csp_in, float)[:n], 1e-12)
    else:
        _cs_in = np.full(n, S.CS_M)
    fatt_cs = (S.CS_M / _cs_in) ** 2
    inerzia = np.maximum(rho * fatt_cs, 1e-6)
    pavimento = (rho * fatt_cs) < 1e-6

    # ATTENZIONE — `correzione` ha DUE termini, non uno (righe 1895-1901):
    #     correzione = cross(B, nb)
    #     if CAMPO_SPINORIALE:  correzione += cross(_nb_grav(), nb)
    # Il secondo e' il torque verso il Bloch del CAMPO EMESSO spinoriale, ed e' ATTIVO nei run del
    # fork (`--campo-spinoriale`). NELLA PRIMA VERSIONE DI QUESTO TRACER L'AVEVO OMESSO: il controllo
    # di direzione (`cos(stoc, det) = +0.643`, sopra la soglia 0.5) lo ha stanato, perche' un termine
    # mancante lascia un residuo ALLINEATO al deterministico, mentre il rumore lo lascia isotropo.
    cor = np.cross(B, nb)
    if S.CAMPO_SPINORIALE:
        cor = cor + np.cross(lav._nb_grav(), nb)
    Bm = np.linalg.norm(B, axis=1)
    corm = np.linalg.norm(cor, axis=1)
    sin_ang = np.clip(corm / np.maximum(Bm, 1e-30), 0.0, 1.0)
    ang = np.degrees(np.arcsin(sin_ang))

    dens = np.abs(np.asarray(lav.psi[:n])) ** 2
    rif = max(float(np.median(dens[dens > 1e-6])), 1e-6) if np.any(dens > 1e-6) else 1.0
    tau = S.TAU_A * np.maximum(dens / rif, 0.05)
    Lam = float(np.mean(dens))
    amp = np.sqrt(Lam) / (1.0 + dens / max(Lam, 1e-300))     # l'ampiezza del rumore su nb

    # --- tau_LUCE = d/cs, costruito con la STESSA formula gia' nel file (`_bloch_ritardato`,
    # Strato 1): d_nodo = media degli archi incidenti, cs_nodo dalla cache `_cs_nodo_prev`.
    # Non e' una formula nuova: e' quella che il fork usa gia', per la stessa ragione causale.
    ii_a, jj_a, dd = lav.i, lav.j, lav.d
    if len(ii_a) and len(dd) == len(ii_a):
        grado_a = (np.bincount(ii_a, minlength=n) + np.bincount(jj_a, minlength=n)).astype(float)
        somma_a = (np.bincount(ii_a, weights=dd, minlength=n) +
                   np.bincount(jj_a, weights=dd, minlength=n))
        d_nodo = somma_a / np.maximum(grado_a, 1.0)
        d_nodo[grado_a <= 0] = S.LAM
    else:
        d_nodo = np.full(n, S.LAM)
    d_nodo = np.maximum(d_nodo, 1e-12)
    csp = getattr(lav, "_cs_nodo_prev", None)
    if csp is not None and len(csp) >= n:
        cs_nodo = np.maximum(np.asarray(csp, float)[:n], 1e-12)
    else:
        cs_nodo = np.full(n, S.CS_M)
    tau_luce = np.maximum(d_nodo / cs_nodo, 1e-30)

    om_vec = np.asarray(lav.omega_s[:n], float)
    om_src = np.linalg.norm(om_vec, axis=1)
    coppia_su_in = corm / inerzia
    diss = om_src / tau
    # (IV) la parte DETERMINISTICA dell'incremento, come la prescrive la riga 1918, in VETTORE
    det_vec = dtn[:, None] * (cor / inerzia[:, None] - om_vec / tau[:, None])
    # errore atteso della ricostruzione: l'unica approssimazione nota e' `nb` rumoroso nel prodotto
    # vettore (criterio par.5). Errore relativo ~ amp*sqrt(2)/sin(angolo).
    err_att = amp * np.sqrt(2.0) / np.maximum(sin_ang, 1e-12)
    return dict(n=n, inerzia=inerzia, pavimento=pavimento, Bm=Bm, kvic=kvic, ang=ang,
                corm=corm, coppia_su_in=coppia_su_in, tau=tau, om_src=om_src, diss=diss,
                amp=amp, eta=np.asarray(lav.eta[:n], float), fatt_cs=fatt_cs,
                cs_nodo_in=_cs_in, rho=rho,
                # [2026-09-16] INGREDIENTI DEL SETTORE U(1)/SEGNO. Si restituiscono da QUI e non
                # si ricalcolano nell'osservatore, perche' `_pesi()` MUTA cache lette dalla
                # dinamica (`psi`, `_S.data`, `_chi_core_nodi`): l'unico posto dove e' lecito
                # chiamarlo e' questa COPIA PROFONDA, che il sigillo gia' certifica.
                w=w, ii=np.asarray(i), jj=np.asarray(j),
                psi_spinor=np.asarray(lav._psi_spinor[:n]).copy(),
                nb_grav=np.asarray(lav._nb_grav()[:n], float).copy(),
                perc_chi=(np.asarray(lav.perc_chi[:n], float).copy()
                          if len(lav.perc_chi) >= n else np.ones(n)),
                canon=np.asarray(lav._bloch_a_spinore(
                    np.asarray(lav._nb_grav()[:n], float))).copy(),
                om_vec=om_vec, det_vec=det_vec, dtn=dtn, err_att=err_att,
                d_nodo=d_nodo, cs_nodo=cs_nodo, tau_luce=tau_luce)


def pend(x, y):
    """Pendenza d(log y)/d(log x) fra NODI (non una media). Esclude non-finiti e non-positivi."""
    ok = np.isfinite(x) & np.isfinite(y) & (x > 0) & (y > 0)
    if ok.sum() < 50:
        return float("nan"), 0, float("nan")
    lx, ly = np.log(x[ok]), np.log(y[ok])
    return float(np.polyfit(lx, ly, 1)[0]), int(ok.sum()), float(np.corrcoef(lx, ly)[0, 1])


CAMPI = ("pos", "phi", "phi0", "phivel", "eta", "d", "d0", "vd", "peq", "tw", "twp",
         "i", "j", "perc_chi", "perc_tw", "_nb", "_nb_prec", "_nb_ret", "_psi_spinor", "omega_s", "psi")


def sigillo(S, seed, passi):
    def corri(osserva):
        net = scena(S, seed)
        for _ in range(passi):
            if osserva:
                ingredienti(S, net)
            passo(S, net)
        return net
    a = corri(False); b = corri(True)
    print("=" * 104)
    print("SIGILLO - il tracer e' PURE-READ?  (%d passi, seme %d)" % (passi, seed))
    print("=" * 104)
    print("PRESIDIO: uno zero con N DIVERSO e' MANCANZA DI CONFRONTO, non identita'.")
    print("  n senza tracer = %d   n con tracer = %d   ->  %s"
          % (a.n, b.n, "CONFRONTABILI" if a.n == b.n else "NON CONFRONTABILI: sigillo NULLO"))
    if a.n != b.n:
        return False
    ok = True
    for c in CAMPI:
        va, vb = getattr(a, c, None), getattr(b, c, None)
        if va is None or vb is None:
            print("  %-14s assente -> SALTATO" % c); continue
        va, vb = np.asarray(va), np.asarray(vb)
        if va.shape != vb.shape:
            print("  %-14s SHAPE diversa -> FAIL" % c); ok = False; continue
        d = float(np.max(np.abs(va.astype(complex) - vb.astype(complex)))) if va.size else 0.0
        if d != 0.0:
            ok = False
        print("  %-14s shape %-14s max|A-B| = %.3e   %s" % (c, str(va.shape), d, "PASS" if d == 0 else "FAIL"))
    rng_ok = (a.rng.bit_generator.state == b.rng.bit_generator.state)
    print("  %-14s %s   %s" % ("stato RNG", "identico" if rng_ok else "DIVERSO", "PASS" if rng_ok else "FAIL"))
    ok = ok and rng_ok
    print("")
    print("SIGILLO: %s" % ("PASS - il tracer non tocca nulla" if ok else "FAIL - NON USARLO"))
    return ok


def scegli_nodi(g, per_quartile=5):
    """20 nodi FISSI: 5 per quartile di inerzia, esclusi quelli col pavimento attivo (li' l'inerzia
    non varia). Scelti UNA VOLTA e poi seguiti: i nodi non vengono mai rimossi dal simulatore."""
    idx = np.where(~g["pavimento"])[0]
    if len(idx) < 4 * per_quartile:
        idx = np.arange(g["n"])
    ordinati = idx[np.argsort(g["inerzia"][idx])]
    scelti = []
    for q in range(4):
        blocco = ordinati[q * len(ordinati) // 4:(q + 1) * len(ordinati) // 4]
        if len(blocco):
            scelti.extend(blocco[np.linspace(0, len(blocco) - 1, per_quartile).astype(int)].tolist())
    return sorted(set(int(x) for x in scelti))


ETICHETTE = ("|B|", "angolo", "|correzione|", "coppia/inerzia", "|om_src|/tau", "theta")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--passi", type=int, default=400)
    ap.add_argument("--ogni", type=int, default=50)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--sigillo", action="store_true")
    ap.add_argument("--passi-sigillo", type=int, default=20)
    ap.add_argument("--csv", default=os.path.join("csv", "_test_fork", "_tracing_omega.csv"))
    o = ap.parse_args()
    S = prepara()
    if o.sigillo:
        sys.exit(0 if sigillo(S, o.seed, o.passi_sigillo) else 1)

    net = scena(S, o.seed)
    for _ in range(50):
        passo(S, net)
    g = ingredienti(S, net)
    nodi = scegli_nodi(g)
    print("scena: n=%d archi=%d   nodi tracciati FISSI: %d (5 per quartile di inerzia)"
          % (net.n, len(net.i), len(nodi)))
    print("")
    righe = ["passo,nodo,eta,inerzia,pavimento,B,k_vicini,angolo_gradi,correzione,"
             "coppia_su_inerzia,tau,omega_src,dissipativo,rapporto_coppia_diss,amp,omega_new,theta_gradi,"
             "det,stoc,R_stoc,cos_stoc_det,err_atteso"]
    storia = []
    for t in range(1, o.passi + 1):
        campiona = (t % o.ogni == 0) or t == 1
        if campiona:
            g = ingredienti(S, net)
        passo(S, net)
        if not campiona:
            continue
        om_new_vec = np.asarray(net.omega_s[:g["n"]], float)
        om_new = np.linalg.norm(om_new_vec, axis=1)
        th = np.degrees(om_new * S.DT)
        # --- (IV) scomposizione dell'incremento: deterministico (riga 1918) vs resto ---
        delta_vec = om_new_vec - g["om_vec"]
        stoc_vec = delta_vec - g["det_vec"]
        det_m = np.linalg.norm(g["det_vec"], axis=1)
        stoc_m = np.linalg.norm(stoc_vec, axis=1)
        R_stoc = stoc_m / np.maximum(det_m, 1e-300)
        cosang = (np.sum(stoc_vec * g["det_vec"], axis=1) /
                  np.maximum(stoc_m * det_m, 1e-300))
        for k in nodi:
            if k >= g["n"]:
                continue
            rap = g["coppia_su_in"][k] / max(g["diss"][k], 1e-300)
            righe.append("%d,%d,%.6g,%.6g,%d,%.6g,%d,%.4f,%.6g,%.6g,%.6g,%.6g,%.6g,%.6g,%.6g,%.6g,%.6g,%.6g,%.6g,%.6g,%.4f,%.6g"
                         % (t, k, g["eta"][k], g["inerzia"][k], int(g["pavimento"][k]), g["Bm"][k],
                            int(g["kvic"][k]), g["ang"][k], g["corm"][k], g["coppia_su_in"][k],
                            g["tau"][k], g["om_src"][k], g["diss"][k], rap, g["amp"][k],
                            om_new[k], th[k], det_m[k], stoc_m[k], R_stoc[k], cosang[k],
                            g["err_att"][k]))
        v = ~g["pavimento"]
        x = g["inerzia"][v]
        p = {}
        for eti, y in zip(ETICHETTE, (g["Bm"][v], g["ang"][v], g["corm"][v],
                                      g["coppia_su_in"][v], g["diss"][v], th[:g["n"]][v])):
            p[eti] = pend(x, y)
        p["_passo"] = t
        p["_nodi"] = int(v.sum())
        p["_rap"] = float(np.median(g["coppia_su_in"][v] / np.maximum(g["diss"][v], 1e-300)))
        p["_ang"] = float(np.median(g["ang"][v]))
        p["_amp"] = float(np.median(g["amp"][v]))
        p["_R"] = float(np.median(R_stoc[v]))
        p["_cos"] = float(np.median(cosang[v]))
        p["_err"] = float(np.median(g["err_att"][v]))
        storia.append(p)
        print("  passo %4d  nodi %5d | %s | R_stoc %8.3g  cos %+.3f" % (t, p["_nodi"],
              "  ".join("%s %+.3f" % (e, p[e][0]) for e in ETICHETTE), p["_R"], p["_cos"]))
    open(o.csv, "w").write("\n".join(righe) + "\n")
    print("")
    print("tracce per-nodo -> %s  (%d righe)" % (o.csv, len(righe) - 1))
    print("")
    u = storia[-1]
    print("=" * 104)
    print("PENDENZE TRASVERSALI FINALI  d(log X)/d(log inerzia)   (passo %d, %d nodi)"
          % (u["_passo"], u["_nodi"]))
    print("=" * 104)
    for e in ETICHETTE:
        s, nn, r = u[e]
        print("  %-16s pendenza %+.3f   (r = %+.3f, %d nodi)" % (e, s, r, nn))
    print("")
    print("  rapporto mediano (coppia/inerzia) / (|om_src|/tau) = %.4g" % u["_rap"])
    print("  angolo (B,nb) mediano = %.2f gradi     amp (rumore su nb) mediana = %.4g"
          % (u["_ang"], u["_amp"]))
    print("")
    print("=" * 104)
    print("ESITO (IV) — l'incremento e' DETERMINISTICO o STOCASTICO?  (criterio par. IV.3)")
    print("=" * 104)
    print("  R_stoc = |stoc|/|det|  mediana = %.4g" % u["_R"])
    print("  cos(stoc, det) mediana = %+.3f      [~0 = rumore isotropo ; ~+-1 = errore sistematico MIO]"
          % u["_cos"])
    print("  errore ATTESO della ricostruzione (amp*sqrt2/sin ang) mediano = %.4g" % u["_err"])
    if u["_R"] >= 3:
        print("  -> R_stoc >= 3 : ESITO (IV) INDICATO, e' il RUMORE a guidare omega.")
        if abs(u["_cos"]) > 0.5:
            print("     MA cos = %+.3f e' lontano da 0: la parte non spiegata e' ALLINEATA al" % u["_cos"])
            print("     deterministico -> ERRORE SISTEMATICO della ricostruzione. (IV) NON si dichiara.")
        elif u["_R"] <= 3 * u["_err"]:
            print("     MA R_stoc non supera di molto l'errore atteso (%.4g): NON concludere." % u["_err"])
        else:
            print("     cos ~ 0 e R_stoc >> errore atteso: coerente con RUMORE GENUINO.")
    elif u["_R"] > 0.3:
        print("  -> 0.3 < R_stoc < 3 : regime MISTO. Si riporta e NON si sceglie (criterio par. IV.3).")
    else:
        print("  -> R_stoc <= 0.3 : il rumore e' marginale. (IV) ESCLUSO.")
    print("")
    print("=" * 104)
    print("FASE 1 — `tau` DEVE essere il TEMPO-LUCE d/cs?  (test analitico, nessun cablaggio)")
    print("=" * 104)
    v2 = ~g["pavimento"]
    x2 = g["inerzia"][v2]
    p_tl, n_tl, r_tl = pend(x2, g["tau_luce"][v2])
    p_ta, n_ta, r_ta = pend(x2, g["tau"][v2])
    p_si = u["coppia/inerzia"][0]
    print("  pendenza di tau_ATTUALE (TAU_A*dens/dens_rif)  = %+.3f   (r = %+.3f, %d nodi)"
          % (p_ta, r_ta, n_ta))
    print("  pendenza di tau_LUCE    (d/cs)                 = %+.3f   (r = %+.3f, %d nodi)"
          % (p_tl, r_tl, n_tl))
    print("")
    print("  pendenza(theta) = pendenza(sigma) + pendenza(tau)/2,  con sigma = coppia/inerzia = %+.3f"
          % p_si)
    print("     con tau ATTUALE : attesa %+.3f    MISURATA ORA %+.3f" % (p_si + p_ta / 2.0, u["theta"][0]))
    print("     con tau_LUCE    : attesa %+.3f    <- e' questo il numero che decide" % (p_si + p_tl / 2.0))
    print("")
    ta_dt = float(np.median(g["tau"][v2])) / S.DT
    tl_dt = float(np.median(g["tau_luce"][v2])) / S.DT
    print("  VALORI ASSOLUTI:  tau_attuale/DT = %.4g passi     tau_luce/DT = %.4g passi   (rapporto %.4g)"
          % (ta_dt, tl_dt, tl_dt / max(ta_dt, 1e-30)))
    fatt = np.sqrt(tl_dt / max(ta_dt, 1e-30))
    th_ora = float(np.median(np.degrees(np.linalg.norm(np.asarray(net.omega_s[:g["n"]]), axis=1) * S.DT)))
    print("  |omega|_eq va come sqrt(tau)  ->  fattore %.4g  ->  theta da %.4g a %.4g gradi/passo"
          % (fatt, th_ora, th_ora * fatt))
    print("  cioe' da %.1f a %.1f GIRI per passo.  ATTENZIONE: e' un ordine di grandezza nella"
          % (th_ora / 360.0, th_ora * fatt / 360.0))
    print("  direzione giusta, NON la soluzione dell'aliasing.")
    print("")
    print("  LETTURA (fissata PRIMA):")
    if abs(p_tl) <= 0.3:
        print("  -> |pendenza(d/cs)| <= 0.3 : theta tornerebbe a %+.3f. LA CANCELLAZIONE SI ROMPE."
              % (p_si + p_tl / 2.0))
    elif abs(p_tl - p_ta) <= 0.4:
        print("  -> pendenza(d/cs) ~ pendenza attuale: NON CAMBIA NULLA. La sostituzione e' piu'")
        print("     coerente, ma NON risolve. Non va venduta come cura.")
    else:
        print("  -> valore INTERMEDIO (%+.3f): si riporta il numero e la pendenza attesa (%+.3f),"
              % (p_tl, p_si + p_tl / 2.0))
        print("     senza forzare.")
    print("")
    print("=" * 104)
    print("VERDETTO secondo doc/PREDIZIONE_tracing_omega.md (criterio scritto PRIMA)")
    print("=" * 104)
    pc = u["coppia/inerzia"][0]; pb = u["|B|"][0]; pa = u["angolo"][0]; pt = u["theta"][0]
    if pc <= -0.6 and -0.35 <= pt <= 0.15:
        print("  (I)  coppia/inerzia %+.3f (~ -1) MA theta %+.3f (~ -0.106)" % (pc, pt))
        print("  -> IL COLPEVOLE E' A VALLE del rapporto: rilassamento, dtn_c o commit.")
    elif -0.35 <= pc <= 0.15:
        print("  (II) coppia/inerzia ha GIA' pendenza %+.3f: il colpevole e' A MONTE." % pc)
        if pb >= 0.5:
            print("  -> (II-a) |B| pendenza %+.3f (>= +0.5): IL CAMPO SCALA COME L'INERZIA," % pb)
            print("            e il rapporto e' quasi costante PER COSTRUZIONE.")
        elif abs(pb) <= 0.25 and pa <= -0.15:
            print("  -> (II-b) |B| piatto (%+.3f) ma l'ANGOLO si chiude (%+.3f): E' GEOMETRIA." % (pb, pa))
            print("            NB: se l'angolo mediano e' piccolo la ricostruzione di `correzione`")
            print("            e' FRAGILE (criterio par.5) -> verdetto da dichiarare INCERTO.")
        else:
            print("  -> ne' (II-a) ne' (II-b): |B| %+.3f, angolo %+.3f. RIPORTARE SENZA CONCLUDERE."
                  % (pb, pa))
    else:
        print("  (III) coppia/inerzia %+.3f, theta %+.3f: FUORI da entrambe le bande." % (pc, pt))
        print("  -> REPERTO NUOVO. Si riportano i numeri e si FERMA.")


if __name__ == "__main__":
    main()
