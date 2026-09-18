# -*- coding: utf-8 -*-
"""Z9 PER COORTE ANAGRAFICA -- la maturazione, il tasso, e il kernel acerbo.

Task history con la DERIVAZIONE, committato PRIMA: doc/TASK_HISTORY/2026-09-18_Z9-per-coorte.md
Previsioni qualitative committate PRIMA: doc/PREVISIONI_qualitative.md (f3895aa)

IN TESTA, NON IN FONDO:
  * `--tau-luce` HA IL SIGILLO FALLITO (CLAUDE.md par.0): ramo NON CERTIFICATO, ogni numero lo eredita;
  * `--chi-basc` attivo; UN SEME per scena; sei istanti;
  * LA COORTE E' ANAGRAFICA, NON PER MASSA. conc_nodi/conc_archi/masse_info NON sono nei .pkl
    (vengono dal blob a1ae5090, che le scartava in silenzio: Z53). La domanda "i nodi di QUESTA
    MASSA maturano?" RESTA SENZA RISPOSTA, e non la sostituisco con un'altra fingendo che sia uguale.
  * NESSUN VERDETTO DI FISICA, NESSUNA IDENTIFICAZIONE.

LA DERIVAZIONE CHE REGGE TUTTO (dal codice, non da una regressione):
  :3236  self.eta += dt_n        :3038  dt_n = DT * r        :2649  ramp = min(1, eta/TAU_A)
  ->  d(eta)/d(passo) = DT * r          passi(ramp = 1) = TAU_A / (DT * r) = 5000 / r
Il par.2 la VERIFICA: se la misura non la conferma, la derivazione e' sbagliata e ci si FERMA.

E `base`: l'ASSOLUTO non si ricostruisce (lambda_nodi -> massa_critica_adattiva -> i pesi: catena
RICORSIVA; ricostruirla fuori e' l'errore gia' fatto su `correzione`). Il RAPPORTO si', ed e' ESATTO:
  base = exp(-d/lam) * ramp[i] * ramp[j] * exp(alpha*tau/(1+beta*tau))
  -> base / base_maturo = ramp[i] * ramp[j]     (gli altri due fattori si CANCELLANO)
ASCII PURO.
"""
import glob
import os
import pickle
import subprocess
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")))
import _presidio
_presidio.avvia(__file__)

import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
os.chdir(ROOT)
PPF = 6
DT = 0.01                       # dal simulatore :189 -- VERIFICATO dal sorgente
R_FLOOR = 1e-6 / (1.0 / np.sqrt(2.0) + 1e-6)
FERMO = 2.0                     # r/r_floor < 2 -> FERMO. Soglia DICHIARATA: Z46 misura 1.0000 esatto
                                # sui fermi, quindi 2 e' gia' un ordine di tolleranza, non una scelta fine.
SCENE = [("TRE  (Z49)", os.path.join("csv", "_test_fork", "_gvideo")),
         ("DUE  (Z52)", os.path.join("csv", "_test_fork", "_g2m"))]

print("=" * 124)
print("Z9 PER COORTE ANAGRAFICA -- la maturazione, il tasso, il kernel acerbo. NESSUN VERDETTO.")
print("=" * 124)
print("  PRESIDI, IN TESTA:")
print("    * --tau-luce HA IL SIGILLO FALLITO (par.0): ramo NON CERTIFICATO, ogni numero lo eredita;")
print("    * --chi-basc attivo; UN SEME per scena; sei istanti; nessuna identificazione;")
print("    * COORTE ANAGRAFICA, NON PER MASSA: il tracking non e' nei .pkl (Z53). La domanda")
print("      'i nodi di QUESTA MASSA maturano?' RESTA SENZA RISPOSTA.")


def pct(v):
    if v.size == 0:
        return (np.nan,) * 5
    return (float(v.min()), float(np.percentile(v, 5)), float(np.median(v)),
            float(np.percentile(v, 95)), float(v.max()))


def leggi(D):
    S = {}
    for p in sorted(glob.glob(os.path.join(D, "frame_*.pkl"))):
        s = pickle.load(open(p, "rb"))
        S[int(s["attrs"].get("_db_step", -1))] = s
    return S, sorted(S)


# ================================================================== IL REGIME, LETTO DAL BLOB DEL .pkl
print("")
print("--- IL REGIME: TAU_A NON E' NEI DATI, ma il .pkl REGISTRA IL BLOB -> si risale AL SORGENTE ---")
print("  (e' il corollario di par.9: 'deducibile, non scritto'. Qui la deduzione parte dal BLOB che")
print("   il .pkl porta con se', non dalla mia memoria di quale regime girava.)")
TAU_A = {}
for eti, D in SCENE:
    S, F = leggi(D)
    b = S[F[-1]].get("blob")
    src = subprocess.check_output(["git", "cat-file", "-p", b]).decode("utf-8", "replace").splitlines()
    reg = [l for l in src if l.startswith("REGIME =")]
    ta = [l for l in src if l.strip().startswith("_TAU_A_REGIME =")]
    nome = reg[0].split("#")[0].strip() if reg else "?"
    print("  %-12s blob nel .pkl = %s" % (eti, str(b)[:8]))
    print("               %s" % nome)
    for l in ta:
        print("               %s" % l.strip())
    # il ramo attivo e' il PRIMO se REGIME == "deterministico"
    det = 'REGIME = "deterministico"' in nome
    TAU_A[eti] = 50.0 if det else 2.0
    print("               -> RAMO ATTIVO: %s   TAU_A = %.1f   passi(ramp=1) = TAU_A/(DT*r) = %.0f / r"
          % ("deterministico" if det else "stocastico", TAU_A[eti], TAU_A[eti] / DT))
print("  ATTENZIONE: DIFETTO P6, VERIFICATO DAL DISCO: `RUN_PARAMS` (:6274-6296) scrive `leggi_attive` con")
print("    REGIME e `costanti_effettive` con LAM/GAMMA/SCALA_B/CS_M/K_C/PHI_CRIT -- ma NON TAU_A,")
print("    NON G_PH, NON CALORE_INIT. I TRE NUMERI CHE DEFINISCONO IL REGIME SONO GLI UNICI CHE")
print("    MANCANO. Sono DEDUCIBILI da REGIME, non SCRITTI: e una deduzione dichiarata vale, una")
print("    ricostruzione a memoria no.")

for eti, D in SCENE:
    S, F = leggi(D)
    TA = TAU_A[eti]
    A = {f: S[f]["attrs"] for f in F}
    N = {f: len(A[f]["pos"]) for f in F}

    print("")
    print("=" * 124)
    print("SCENA %s   (%s)" % (eti, D))
    print("=" * 124)
    print("  istanti (FRAME; il passo di motore e' frame*%d):" % PPF)
    for f in F:
        print("    frame %-5d = passo %-6d  n = %d" % (f, f * PPF, N[f]))

    # ---------------------------------------------------------- le coorti ANAGRAFICHE
    bordi = [0] + [N[f] for f in F]
    CO = []
    for k in range(len(F)):
        lo, hi = bordi[k], bordi[k + 1]
        if hi > lo:
            nome = ("presenti al f%d" % F[0]) if k == 0 else ("nati f%d -> f%d" % (F[k - 1], F[k]))
            CO.append((nome, lo, hi))
    print("")
    print("  LE COORTI ANAGRAFICHE (l'indice E' l'ordine di nascita: i nodi si appendono in coda,")
    print("  :3958, e nascono con eta = 0, :3961/:4082/:1849). Finestre ESATTE, non stimate:")
    for nome, lo, hi in CO:
        print("    %-22s indici [%6d, %6d)   %6d nodi" % (nome, lo, hi, hi - lo))

    # ---------------------------------------------------------- (1) maturazione per coorte
    print("")
    print("--- (1) LA MATURAZIONE PER COORTE -- eta e ramp = min(1, eta/%.0f) ---" % TA)
    for f in F:
        et = np.asarray(A[f]["eta"], float)[:N[f]]
        print("")
        print("  frame %-5d (passo %-6d, n = %d)" % (f, f * PPF, N[f]))
        print("    %-22s %-7s | %-9s %-9s %-9s %-9s %-9s | %-9s %-9s %-9s %-9s"
              % ("coorte", "nodi", "eta min", "eta p05", "eta MED", "eta p95", "eta max",
                 "ramp MED", "ramp p95", "fr>0.5", "fr>0.9"))
        for nome, lo, hi in CO:
            if lo >= N[f]:
                continue
            v = et[lo:min(hi, N[f])]
            if v.size < 5:
                continue
            mn, p5, md, p95, mx = pct(v)
            rp = np.minimum(1.0, v / TA)
            print("    %-22s %-7d | %-9.4g %-9.4g %-9.4g %-9.4g %-9.4g | %-9.4g %-9.4g %-9.4f %-9.4f"
                  % (nome, v.size, mn, p5, md, p95, mx,
                     float(np.median(rp)), float(np.percentile(rp, 95)),
                     float(np.mean(rp > 0.5)), float(np.mean(rp > 0.9))))
        rp_tot = np.minimum(1.0, et / TA)
        print("    %-22s %-7d | %-9.4g %-9.4g %-9.4g %-9.4g %-9.4g | %-9.4g %-9.4g %-9.4f %-9.4f"
              % ("TUTTA LA POPOLAZIONE", et.size, *pct(et),
                 float(np.median(rp_tot)), float(np.percentile(rp_tot, 95)),
                 float(np.mean(rp_tot > 0.5)), float(np.mean(rp_tot > 0.9))))

    # ---------------------------------------------------------- (2) il tasso, per regime di moto
    print("")
    print("--- (2) IL TASSO -- `r` LETTO da `_r_corrente`, FERMI contro MOBILI (mai una mediana comune, A3c) ---")
    print("    %-7s %-8s %-9s %-9s | %-12s %-12s | %-12s %-12s"
          % ("frame", "len(r)", "FERMI", "MOBILI", "r MED fermi", "r MED mobili",
             "DT*r fermi", "DT*r mobili"))
    RR = {}
    for f in F:
        rc = A[f].get("_r_corrente", None)
        if rc is None:
            print("    frame %-5d  `_r_corrente` ASSENTE -> il par.2 non si fa qui, e NON stimo r da eta"
                  % f)
            continue
        r = np.asarray(rc, float)
        RR[f] = r
        fer = r / R_FLOOR < FERMO
        mob = ~fer
        print("    %-7d %-8d %-9d %-9d | %-12.6e %-12.6e | %-12.4e %-12.4e"
              % (f, r.size, int(fer.sum()), int(mob.sum()),
                 float(np.median(r[fer])) if fer.any() else np.nan,
                 float(np.median(r[mob])) if mob.any() else np.nan,
                 DT * float(np.median(r[fer])) if fer.any() else np.nan,
                 DT * float(np.median(r[mob])) if mob.any() else np.nan))
    print("    (`_r_corrente` e' scritta PRIMA dell'ultima mitosi: len(r) < n. I nodi in eccesso sono")
    print("     ESCLUSI, non riempiti.)")

    print("")
    print("  ATTENZIONE: IL FALSIFICATORE DELLA DERIVAZIONE: d(eta)/d(passo) MISURATO contro DT*r LETTO")
    print("    %-16s %-10s | %-13s %-13s | %-13s %-13s | %-10s"
          % ("intervallo", "gruppo", "deta/dpasso", "DT*r letto", "rapporto MED", "rapporto p95", "nodi"))
    for k in range(len(F) - 1):
        f0, f1 = F[k], F[k + 1]
        if f0 not in RR or f1 not in RR:
            continue
        m = min(N[f0], N[f1], RR[f0].size, RR[f1].size)
        de = (np.asarray(A[f1]["eta"], float)[:m] - np.asarray(A[f0]["eta"], float)[:m]) \
            / float((f1 - f0) * PPF)
        rme = 0.5 * (RR[f0][:m] + RR[f1][:m])          # r medio sull'intervallo, dai DUE estremi
        fer = rme / R_FLOOR < FERMO
        for nome, sel in (("FERMI", fer), ("MOBILI", ~fer)):
            if sel.sum() < 5:
                continue
            att = DT * rme[sel]
            rap = de[sel] / np.maximum(att, 1e-300)
            print("    %-16s %-10s | %-13.6e %-13.6e | %-13.4f %-13.4f | %-10d"
                  % ("%d->%d" % (f0, f1), nome, float(np.median(de[sel])), float(np.median(att)),
                     float(np.median(rap)), float(np.percentile(rap, 95)), int(sel.sum())))
    print("    (il rapporto deve valere ~1: `r` e' campionato ai due ESTREMI e mediato, quindi uno")
    print("     scarto MODERATO e' la curvatura di r nell'intervallo. Uno scarto di ORDINI romperebbe")
    print("     la derivazione, ed e' il falsificatore fissato nel task history.)")

    print("")
    print("  L'ESTRAPOLAZIONE A `ramp = 1`, per gruppo: passi = TAU_A/(DT*r) = %.0f / r" % (TA / DT))
    f = F[-1]
    if f in RR:
        r = RR[f]
        fer = r / R_FLOOR < FERMO
        for nome, sel in (("FERMI ", fer), ("MOBILI", ~fer)):
            if sel.sum() < 5:
                continue
            rm = float(np.median(r[sel]))
            print("    %-8s r MED = %-13.6e -> %-14.4g passi   (la scena ne ha %d)"
                  % (nome, rm, (TA / DT) / rm, F[-1] * PPF))

    # ---------------------------------------------------------- (3) il kernel
    print("")
    print("--- (3) IL KERNEL ACERBO -- `base/base_maturo = ramp[i]*ramp[j]`, ESATTO (gli altri fattori si cancellano) ---")
    print("    %-7s %-10s | %-11s %-11s %-11s %-11s %-11s | %-9s %-9s %-9s"
          % ("frame", "archi", "min", "p05", "MEDIANA", "p95", "max", "fr>0.01", "fr>0.5", "fr>0.9"))
    for f in F:
        a = A[f]
        et = np.asarray(a["eta"], float)
        ii = np.asarray(a["i"], int)
        jj = np.asarray(a["j"], int)
        n = N[f]
        msk = (ii < n) & (jj < n) & (ii < et.size) & (jj < et.size)
        rp = np.minimum(1.0, et / TA)
        b = rp[ii[msk]] * rp[jj[msk]]
        print("    %-7d %-10d | %-11.4e %-11.4e %-11.4e %-11.4e %-11.4e | %-9.4f %-9.4f %-9.4f"
              % (f, b.size, *pct(b), float(np.mean(b > 0.01)),
                 float(np.mean(b > 0.5)), float(np.mean(b > 0.9))))
    print("    (il prodotto pesa IL MINORE dei due: un arco fra un nodo maturo e un neonato e' ACERBO.)")

    # confronto col quadrato del ramp tipico: era la previsione 6
    f = F[-1]
    et = np.asarray(A[f]["eta"], float)[:N[f]]
    rp = np.minimum(1.0, et / TA)
    a = A[f]
    ii = np.asarray(a["i"], int); jj = np.asarray(a["j"], int)
    msk = (ii < N[f]) & (jj < N[f])
    b = np.minimum(1.0, np.asarray(a["eta"], float) / TA)[ii[msk]] * \
        np.minimum(1.0, np.asarray(a["eta"], float) / TA)[jj[msk]]
    print("    PREVISIONE 6, all'ultimo istante: ramp MED nodi = %.4e -> il suo QUADRATO = %.4e"
          % (float(np.median(rp)), float(np.median(rp)) ** 2))
    print("                                      base/base_maturo MEDIANO misurato = %.4e  (rapporto %.4f)"
          % (float(np.median(b)), float(np.median(b)) / max(float(np.median(rp)) ** 2, 1e-300)))

    # ---------------------------------------------------------- A8: i contatori
    print("")
    print("--- A8 -- i contatori GIA' CABLATI, letti e riportati (non commentati) ---")
    a = A[F[-1]]
    for k in sorted(a):
        if k.startswith("_ritmo_") or k in ("_inerzia_al_pavimento", "_inerzia_tot",
                                            "_cs_fallback", "_cs_chiamate", "nati", "coppie_nate"):
            print("    %-30s %s" % (k, a[k]))

print("")
print("=" * 124)

# ============================================================== (4) IL CRITERIO -- aggiunto DOPO il
# primo giro, e lo dichiaro: il primo giro ha mostrato che `base/base_maturo` MEDIANO e' PIU' GRANDE
# del QUADRATO del `ramp` mediano (rapporto 1.58 e 1.13). Avevo una SPIEGAZIONE in testa -- "gli archi
# connettono nodi coetanei" -- e una spiegazione in testa non e' una misura. Qui si MISURA.
print("")
print("=" * 124)
print("(4) IL CRITERIO -- e la correlazione che il par.3 aveva lasciato come IPOTESI")
print("=" * 124)
for eti, D in SCENE:
    S, F = leggi(D)
    TA = TAU_A[eti]
    A = {f: S[f]["attrs"] for f in F}
    N = {f: len(A[f]["pos"]) for f in F}
    f = F[-1]
    a = A[f]
    n = N[f]
    n0 = N[F[0]]
    et = np.asarray(a["eta"], float)
    rp = np.minimum(1.0, et / TA)
    ii = np.asarray(a["i"], int)
    jj = np.asarray(a["j"], int)
    msk = (ii < n) & (jj < n) & (ii < et.size) & (jj < et.size)
    I2, J2 = ii[msk], jj[msk]
    x, y = rp[I2], rp[J2]

    print("")
    print("  SCENA %s -- ultimo istante (frame %d = passo %d, n = %d, n0 = %d)"
          % (eti, f, f * PPF, n, n0))

    # (4a) ASSORTATIVITA' PER ETA': misurata, col NULLO accanto
    c = float(np.corrcoef(x, y)[0, 1])
    rng = np.random.default_rng(0)
    nulli = [float(np.corrcoef(x, rp[rng.permutation(J2)])[0, 1]) for _ in range(5)]
    print("    (4a) ASSORTATIVITA': corr(ramp[i], ramp[j]) sugli archi = %+.4f" % c)
    print("         NULLO (estremo j rimescolato, 5 ripetizioni)      = %s"
          % " ".join("%+.4f" % v for v in nulli))
    print("         -> se la corr e' ALTA e il nullo e' ~0, gli archi sono ASSORTATIVI PER ETA',")
    print("            ed E' QUELLO che rende il prodotto mediano piu' grande del quadrato della")
    print("            mediana. Se la corr fosse ~0, la mia spiegazione e' SBAGLIATA e si scrive.")

    # (4b) IL CRITERIO NECESSARIO: gli archi INTERNI alla coorte ORIGINALE
    ori = (I2 < n0) & (J2 < n0)
    b_ori = x[ori] * y[ori]
    b_tot = x * y
    mat_ori = float(np.mean((et[I2[ori]] >= TA) & (et[J2[ori]] >= TA))) if ori.sum() else np.nan
    mat_tot = float(np.mean((et[I2] >= TA) & (et[J2] >= TA)))
    print("    (4b) IL CRITERIO NECESSARIO -- archi INTERNI alla coorte ORIGINALE (nessuna diluizione")
    print("         da neonati, e nessuna soglia scelta: `ramp` SATURA ESATTAMENTE a eta = TAU_A)")
    print("         archi interni alla coorte originale : %d su %d (%.2f %%)"
          % (int(ori.sum()), int(b_tot.size), 100.0 * ori.sum() / max(b_tot.size, 1)))
    print("         median(base/base_maturo) SU QUELLI  : %.6f      <- DEVE valere 1 per chiudere Z9"
          % float(np.median(b_ori)) if ori.sum() else "         (nessun arco interno)")
    print("         median(base/base_maturo) su TUTTI   : %.6f" % float(np.median(b_tot)))
    print("         frazione di archi MATURI (entrambi gli estremi con eta >= TAU_A):")
    print("            interni alla coorte originale    : %.6f" % mat_ori)
    print("            su tutti gli archi               : %.6f" % mat_tot)

    # (4c) LA CONDIZIONE DI REGIME, da dichiarare: quanti passi mancano
    rc = a.get("_r_corrente", None)
    if rc is not None:
        r = np.asarray(rc, float)
        mob = r / R_FLOOR >= FERMO
        rm = float(np.median(r[mob]))
        att = TA / (DT * rm)
        print("    (4c) LA CONDIZIONE DI REGIME (da dichiarare in OGNI referto che usi questa scena):")
        print("         r MED dei MOBILI = %.6e   -> passi(ramp=1) = TAU_A/(DT*r) = %.0f" % (rm, att))
        print("         passi FATTI = %d   -> PASSI MANCANTI = %.0f   (il %.1f %% del cammino e' fatto)"
              % (f * PPF, att - f * PPF, 100.0 * f * PPF / att))
print("")
print("=" * 124)
