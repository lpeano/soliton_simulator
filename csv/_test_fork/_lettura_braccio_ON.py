# -*- coding: utf-8 -*-
"""LETTURA DEL BRACCIO ON — spin, U(1)/EM, Bloch. 4 semi, 500 passi, Step 2 di DEFAULT.

COSA E' E COSA NON E':
  E' una DESCRIZIONE della dinamica del braccio ON, con la barra FRA SEMI (P3) e il valore sotto
  IPOTESI NULLA accanto a ogni riga (par.9).
  NON E' un contrasto ON-OFF: il braccio OFF sta ancora girando. **Nulla di cio' che si legge qui
  puo' essere ATTRIBUITO allo Step 2**, perche' non c'e' niente con cui confrontarlo. Chi legge
  questo file e ne trae "lo Step 2 fa X" sta commettendo l'errore che il par.9 chiama
  "mancanza di confronto".

BARRA: 4 semi -> t(0.025, 3) = 3.182. IC95 = media +- 3.182 * sd/sqrt(4).
ASCII PURO (tre script gia' morti su cp1252).
"""
import csv
import glob
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
T3 = 3.182            # t(0.025, 3), 4 semi
TAG = sys.argv[1] if len(sys.argv) > 1 else "s2ON"


def carica(tag):
    out = {}
    for f in sorted(glob.glob(os.path.join(HERE, "_vuoto_%s_s?.vuoto.csv" % tag))):
        r = list(csv.DictReader(open(f, newline="")))
        if r:
            out[int(r[-1].get("seed", 0))] = r
    return out


def val(righe, col, passo=None):
    """valore della colonna all'ultimo campione, o al passo chiesto."""
    if passo is None:
        cand = righe[-1]
    else:
        c = [x for x in righe if x.get("passo") == str(passo)]
        if not c:
            return float("nan")
        cand = c[0]
    try:
        return float(cand.get(col, "nan"))
    except (TypeError, ValueError):
        return float("nan")


def stat(dati, col, passo=None):
    v = [val(r, col, passo) for r in dati.values()]
    v = [x for x in v if x == x]
    if not v:
        return float("nan"), float("nan"), 0
    m = sum(v) / len(v)
    if len(v) < 2:
        return m, float("nan"), len(v)
    sd = math.sqrt(sum((x - m) ** 2 for x in v) / (len(v) - 1))
    return m, T3 * sd / math.sqrt(len(v)), len(v)


# ERRORE MIO, CORRETTO: `chi` esce da `np.arccos` in RADIANTI (`_osserva_vuoto.py:347`) e NON
# viene mai convertito, mentre i valori-null del par.9 (90.000 +- 39.171) sono in GRADI. La prima
# lettura confrontava 1.5716 con 90 e stampava "FUORI dall'IC95" su TUTTE le righe di chi: un
# FALSO REPERTO da disallineamento di UNITA', non un fatto. Convertito qui, in un posto solo.
GRADI = ("chi_tot_media", "chi_tot_std", "chi_tot_mediana", "chi_mat_media", "chi_mat_std",
         "chi_mat_mediana", "chi_vuo_media", "chi_vuo_std", "chi_vuo_mediana", "chi_p90_media",
         "chi_p90_std", "chi_p90_mediana", "chi_p10_media", "chi_p10_std", "chi_p10_mediana")


def riga(dati, col, nullo=None, nome=None, fmt="%.4f", passo=None):
    m, ic, k = stat(dati, col, passo)
    if col in GRADI and m == m:
        m, ic = math.degrees(m), (math.degrees(ic) if ic == ic else ic)
    nm = nome or col
    if m != m:
        print("  %-34s  (assente)" % nm)
        return
    s = ("  %-34s  " + fmt + "  +- " + fmt) % (nm, m, ic if ic == ic else 0.0)
    if nullo is not None:
        d = abs(m - nullo)
        fuori = (ic == ic) and d > ic
        s += ("   | nullo " + fmt + "   %s") % (nullo, "FUORI dall'IC95" if fuori else "compatibile")
    print(s)


def traiettoria(dati, col, nome=None, fmt="%.4g"):
    ps = [50, 150, 300, 500]
    vv = []
    for p in ps:
        m, _, _ = stat(dati, col, p)
        if col in GRADI and m == m:
            m = math.degrees(m)
        vv.append(fmt % m if m == m else "-")
    print("  %-34s  " % (nome or col) + "  ".join("%-12s" % x for x in vv))


D = carica(TAG)
print("=" * 104)
print("LETTURA DEL BRACCIO '%s' -- %d semi, barra FRA SEMI con t(3) = %.3f" % (TAG, len(D), T3))
if D:
    r0 = list(D.values())[0][-1]
    print("  blob %s   STEP2=%s  TW_SPINORE=%s  TAU_LUCE=%s  CS_DIN=%s  FORK_SU2=%s/%s  passo %s"
          % (str(r0.get("blob"))[:8], r0.get("STEP2"), r0.get("TW_SPINORE"), r0.get("TAU_LUCE"),
             r0.get("CS_DINAMICO"), r0.get("FORK_SU2"), r0.get("FORK_SU2_MEM"), r0.get("passo")))
    print("  semi: %s   nodi a fine run: %s"
          % (sorted(D), [int(val(r, "n")) for _, r in sorted(D.items())]))
print("=" * 104)

# ---------------------------------------------------------------- 1. SPIN
print("\n### 1. SPIN -- quanto ruota lo spinore in un passo (il settore e' RISOLTO o ALIASATO?)")
print("-" * 104)
riga(D, "theta_coord_giri_mediana", nome="theta COORD, giri/passo (mediana)", fmt="%.4g")
riga(D, "theta_prop_giri_mediana", nome="theta PROPRIO, giri/passo (mediana)", fmt="%.4g")
riga(D, "theta_prop_fr_gt360g", nullo=None, nome="frazione nodi OLTRE il giro intero")
riga(D, "theta_prop_fr_gt30g", nome="frazione nodi oltre 30 gradi")
print("  > Il criterio di risoluzione NON e' statistico: >1 giro/passo = ALIASING (par.4).")
print()
riga(D, "omega_mediana", nome="|omega_s| mediana", fmt="%.4g")
riga(D, "omega_su_sqrtn", nome="omega / sqrt(n_passi)  [random walk]", fmt="%.4g")
riga(D, "fdt_inerzia_mediana", nome="inerzia mediana (floor = 1e-6)", fmt="%.4g")
riga(D, "Lam", nome="Lam (energia del vuoto)", fmt="%.4g")
riga(D, "L_tot", nome="L_tot = somma(I*|omega|)", fmt="%.4g")

print("\n  -- LE PENDENZE TRASVERSALI (l'ESITO (I) del tracing: attesa -1.056) --")
riga(D, "t3_b_theta", nullo=-1.056, nome="pendenza(theta) vs inerzia", fmt="%.4f")
riga(D, "t3_b_sigma", nome="pendenza(sigma = coppia/inerzia)", fmt="%.4f")
riga(D, "t3_b_tau", nome="pendenza(tau)", fmt="%.4f")
riga(D, "t3_b_r", nullo=0.0, nome="pendenza(r)  [assunta ZERO finora]", fmt="%.4f")
riga(D, "t3_divario", nullo=0.0, nome="divario attesa - misurata", fmt="%.4f")
riga(D, "t3_identita", nullo=0.0, nome="identita' prop - coord - r (deve essere 0)", fmt="%.3e")

print("\n  -- DINAMICA nel tempo (passo 50 / 150 / 300 / 500) --")
print("  %-34s  %-12s  %-12s  %-12s  %-12s" % ("", "p50", "p150", "p300", "p500"))
for c, nm in (("theta_prop_giri_mediana", "theta giri/passo"),
              ("omega_mediana", "|omega_s| mediana"),
              ("fdt_inerzia_mediana", "inerzia mediana"),
              ("Lam", "Lam"),
              ("L_tot", "L_tot"),
              ("t3_b_theta", "pendenza(theta)"),
              ("n", "n nodi")):
    traiettoria(D, c, nome=nm)

# ---------------------------------------------------------------- 2. U(1) / EM
print("\n\n### 2. U(1) / EM -- il settore che lo Step 2 TOCCA (la FASE, non il Bloch)")
print("-" * 104)
# ERRORE MIO, NEL CODICE DI MISURA U: il nullo 2/pi vale per |cos(fase)| con MODULO UNITARIO,
# cioe' se `canon` fosse il rappresentante canonico del Bloch DEL NODO. Non lo e': `canon` e'
# costruito da `_nb_grav()` (`_tracing_omega.py:214`), una direzione DIVERSA. Per due direzioni
# INDIPENDENTI |<canon|psi>| = sqrt((1+cos chi)/2) ha media 2/3, quindi il nullo e'
#     E[|Re|] = (2/3) * (2/pi) = 0.42441   (verificato Monte Carlo su 4e6 campioni: 0.424474)
# Col nullo sbagliato la riga risultava "FUORI dall'IC95" ed era un FALSO REPERTO.
# La colonna `u1_segno_ov_nullo` nei CSV porta ancora 2/pi: va corretta nell'osservatore DOPO la
# campagna (non durante: i run del braccio OFF stanno usando quel file).
riga(D, "u1_segno_ov_absmedia", nullo=(2.0 / 3.0) * (2.0 / math.pi),
     nome="|Re<canon|psi>| media")
riga(D, "u1_segno_arco_coer", nullo=0.0, nome="coerenza di SEGNO d'arco (tutti)")
riga(D, "u1_segno_arco_coer_materia", nullo=0.0, nome="  ... solo archi MATERIA-MATERIA")
riga(D, "u1_segno_arco_coer_mat", nullo=0.0, nome="  ... strato materia (I2 > Lam)")
riga(D, "u1_segno_arco_coer_vuo", nullo=0.0, nome="  ... strato vuoto (I2 <= Lam)")
riga(D, "u1_segno_arco_coer_p90", nullo=0.0, nome="  ... strato p90 (il piu' denso)")
# ATTENZIONE: qui il nullo 0 NON E' VERIFICATO, e con ogni probabilita' e' SBAGLIATO. `_uu` e'
# `nb_grav` normalizzato, cioe' un campo costruito per MEDIA DI VICINATO: due nodi adiacenti
# CONDIVIDONO i contributori, quindi sono correlati PER COSTRUZIONE, non per fisica. Il nullo
# giusto e' la coerenza fra coppie CASUALI di nodi dello stesso run, e non e' stata misurata.
# Finche' non lo e', questa riga NON dice nulla. (P4: prima di misurare se una grandezza cambia,
# verificare che sia libera di valere il suo nullo.)
riga(D, "u1_verso_arco_coer", nullo=0.0,
     nome="coerenza VERSO d'arco [nullo NON verificato]")
riga(D, "u1_n_arco_materia", nome="n archi materia-materia", fmt="%.1f")
print()
riga(D, "u1_spin_overlap_arco", nullo=0.5, nome="spin overlap d'arco (tutti)")
riga(D, "u1_spin_overlap_mat", nullo=0.5, nome="  ... strato materia")
riga(D, "u1_spin_overlap_vuo", nullo=0.5, nome="  ... strato vuoto")
riga(D, "u1_spin_overlap_p90", nullo=0.5, nome="  ... strato p90")

print("\n  -- DINAMICA nel tempo --")
print("  %-34s  %-12s  %-12s  %-12s  %-12s" % ("", "p50", "p150", "p300", "p500"))
for c, nm in (("u1_segno_ov_absmedia", "|Re<canon|psi>| (nullo 0.4244)"),
              ("u1_segno_arco_coer", "coerenza segno (nullo 0)"),
              ("u1_segno_arco_coer_p90", "  ... p90 (nullo 0)"),
              ("u1_spin_overlap_arco", "spin overlap (nullo 0.5)"),
              ("u1_verso_arco_coer", "coerenza verso (nullo IGNOTO)")):
    traiettoria(D, c, nome=nm)

# ---------------------------------------------------------------- 3. nb / BLOCH
print("\n\n### 3. nb / BLOCH -- la direzione di spin. Nullo: chi = 90.000 +- 39.171 gradi")
print("-" * 104)
for pre, nm in (("chi_tot", "TUTTI"), ("chi_mat", "MATERIA"), ("chi_vuo", "VUOTO"),
                ("chi_p90", "p90 (denso)"), ("chi_p10", "p10 (rarefatto)")):
    riga(D, pre + "_media", nullo=90.0, nome="chi medio [%s]" % nm)
print()
for pre, nm in (("chi_tot", "TUTTI"), ("chi_mat", "MATERIA"), ("chi_p90", "p90")):
    riga(D, pre + "_std", nullo=39.171, nome="chi std [%s]" % nm)
print()
for pre, nm in (("chi_tot", "TUTTI"), ("chi_mat", "MATERIA"), ("chi_p90", "p90")):
    riga(D, pre + "_fr_lt10g", nullo=(1 - math.cos(math.radians(10))) / 2.0,
         nome="frazione chi < 10 gradi [%s]" % nm, fmt="%.5f")

print("\n  -- |<n>| : il Bloch MEDIO. Il nullo NON e' zero: e' il valore di N versori CASUALI --")
for pre, nm in (("nmed_tot", "TUTTI"), ("nmed_mat", "MATERIA"), ("nmed_vuo", "VUOTO"),
                ("nmed_p90", "p90"), ("nmed_p10", "p10")):
    m, ic, _ = stat(D, pre + "_mod")
    a, _, _ = stat(D, pre + "_atteso")
    sg, _, _ = stat(D, pre + "_sigma")
    nn, _, _ = stat(D, pre + "_N")
    if m != m:
        continue
    z = (m - a) / sg if sg == sg and sg > 0 else float("nan")
    print("  %-34s  %.4f +- %.4f   | atteso(casuale) %.4f  sigma %.4f  ->  z = %+.2f   (N=%d)"
          % ("|<n>| [%s]" % nm, m, ic if ic == ic else 0.0, a, sg, z, int(nn) if nn == nn else 0))
print("  > z e' in unita' della sigma ATTESA per N versori casuali, non della barra fra semi.")

print("\n  -- DINAMICA nel tempo --")
print("  %-34s  %-12s  %-12s  %-12s  %-12s" % ("", "p50", "p150", "p300", "p500"))
for c, nm in (("chi_tot_media", "chi medio TUTTI (nullo 90)"),
              ("chi_mat_media", "chi medio MATERIA (nullo 90)"),
              ("chi_p90_media", "chi medio p90 (nullo 90)"),
              ("chi_tot_std", "chi std (nullo 39.171)"),
              ("nmed_tot_mod", "|<n>| TUTTI"),
              ("nmed_tot_atteso", "  atteso casuale")):
    traiettoria(D, c, nome=nm)

# ---------------------------------------------------------------- 4. controlli
print("\n\n### 4. CONTROLLI DI SANITA' e P4 (una grandezza ANCORATA non puo' muoversi)")
print("-" * 104)
riga(D, "r_mediana", nullo=1.0, nome="r mediana [ANCORATA a 1 per costruzione]", fmt="%.6f")
riga(D, "r_std", nome="r dispersione [questa SI muove]", fmt="%.4f")
riga(D, "cs_std", nome="cs dispersione", fmt="%.3e")
riga(D, "fatt_cs_scarto_max", nome="max|fatt_cs - 1| (il fattore dello Step 2)", fmt="%.3e")
riga(D, "fatt_cs_frac_oltre_1pc", nome="frazione nodi con |fatt_cs-1| > 1%", fmt="%.5f")
# il nullo di un errore di norma NON e' 0: e' l'epsilon di macchina (2.22e-16). Confrontarlo
# con lo zero esatto produce un "FUORI dall'IC95" che non significa nulla.
riga(D, "norma_psi_err", nullo=2.22e-16, nome="err norma |psi| (nullo = eps macchina)", fmt="%.3e")
riga(D, "nan_psi", nullo=0.0, nome="NaN in psi", fmt="%.1f")
print("=" * 104)
