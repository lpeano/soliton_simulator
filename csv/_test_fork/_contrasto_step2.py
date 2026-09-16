# -*- coding: utf-8 -*-
"""CONTRASTO STEP 2 -- ON contro OFF, 4 semi APPAIATI, 500 passi.

IL CRITERIO E' SCRITTO PRIMA, in doc/PREDIZIONE_step2_U1.md (commit b7cb537), e NON si proroga:
  "un contrasto ON-OFF conta SOLO se il suo IC95 fra semi (4 semi, t(3) = 3.182) ESCLUDE lo zero.
   Mai la SE interna al run."

APPAIAMENTO: i due bracci girano sugli STESSI quattro semi, quindi la differenza si prende
SEME PER SEME (Delta_k = ON_k - OFF_k) e l'IC95 si costruisce sui QUATTRO Delta. E' piu' potente
del confronto fra medie indipendenti, perche' il seme fissa la condizione iniziale, ed e' il
disegno che la campagna ha realmente eseguito.

LA PREDIZIONE CHE QUESTO TEST PUO' FAR PERDERE:
  "NESSUNA firma di SPIN si muove oltre la dispersione fra semi", perche' `_phc` e' una fase
  globale (:2212-2213, uniche occorrenze) e il Bloch e' invariante a 3.3e-16.
  SE una firma di SPIN si muovesse, scatterebbe il CRITERIO DI RETROCESSIONE dello Step 2 scritto
  al momento della promozione, e la promozione si rivelerebbe SBAGLIATA.

ASCII PURO.
"""
import csv
import glob
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
T3 = 3.182


def carica(tag):
    out = {}
    for f in sorted(glob.glob(os.path.join(HERE, "_vuoto_%s_s?.vuoto.csv" % tag))):
        r = list(csv.DictReader(open(f, newline="")))
        if r:
            out[int(r[-1]["seed"])] = r[-1]
    return out


ON, OFF = carica("s2ON"), carica("s2OFF")
SEMI = sorted(set(ON) & set(OFF))

GRADI = ("chi_tot_media", "chi_tot_std", "chi_mat_media", "chi_mat_std",
         "chi_p90_media", "chi_p90_std", "chi_vuo_media")


def num(riga, col):
    try:
        v = float(riga.get(col, "nan"))
    except (TypeError, ValueError):
        return float("nan")
    return math.degrees(v) if col in GRADI and v == v else v


def delta(col):
    d = [num(ON[k], col) - num(OFF[k], col) for k in SEMI]
    d = [x for x in d if x == x]
    if len(d) < 2:
        return None
    m = sum(d) / len(d)
    sd = math.sqrt(sum((x - m) ** 2 for x in d) / (len(d) - 1))
    ic = T3 * sd / math.sqrt(len(d))
    return m, ic, d


def riga(col, nome=None, fmt="%.4g", settore=""):
    r = delta(col)
    if r is None:
        print("  %-36s (assente)" % (nome or col))
        return None
    m, ic, d = r
    esclude = abs(m) > ic
    marca = "*** ESCLUDE LO ZERO ***" if esclude else "contiene lo zero"
    print(("  %-36s Delta = " + fmt + "  IC95 +- " + fmt + "   %s") % (nome or col, m, ic, marca))
    if esclude:
        print(("      per seme: " + ", ".join([fmt] * len(d))) % tuple(d))
    return (nome or col, m, ic, esclude, settore)


print("=" * 104)
print("CONTRASTO STEP 2 -- ON (default) contro OFF (--senza-step2), %d semi APPAIATI" % len(SEMI))
print("  criterio SCRITTO PRIMA: IC95 fra semi con t(3) = %.3f che ESCLUDA lo zero. Non si proroga."
      % T3)
r0 = ON[SEMI[0]]
print("  blob %s   ON: STEP2=%s   OFF: STEP2=%s   TAU_LUCE=%s  TW=%s  CS_DIN=%s  passo %s"
      % (str(r0["blob"])[:8], r0["STEP2"], OFF[SEMI[0]]["STEP2"], r0["TAU_LUCE"],
         r0["TW_SPINORE"], r0["CS_DINAMICO"], r0["passo"]))
print("=" * 104)

esiti = []
print("\n### A. FIRME DI SPIN -- e' QUI che si gioca la RETROCESSIONE")
print("-" * 104)
for c, nm in (("chi_tot_media", "chi medio TUTTI (gradi)"),
              ("chi_mat_media", "chi medio MATERIA (gradi)"),
              ("chi_p90_media", "chi medio p90 (gradi)"),
              ("chi_tot_std", "chi std TUTTI (gradi)"),
              ("chi_tot_fr_lt10g", "frazione chi < 10 gradi"),
              ("nmed_tot_mod", "|<n>| TUTTI"),
              ("nmed_mat_mod", "|<n>| MATERIA"),
              ("nmed_p90_mod", "|<n>| p90"),
              ("u1_spin_overlap_arco", "spin overlap d'arco"),
              ("omega_mediana", "|omega_s| mediana"),
              ("theta_prop_giri_mediana", "theta giri/passo")):
    e = riga(c, nm, settore="SPIN")
    if e:
        esiti.append(e)

print("\n### B. SETTORE U(1) / EM -- quello che lo Step 2 TOCCA")
print("-" * 104)
for c, nm in (("u1_segno_ov_absmedia", "|Re<canon|psi>|"),
              ("u1_segno_arco_coer", "coerenza SEGNO d'arco"),
              ("u1_segno_arco_coer_materia", "  ... materia-materia"),
              ("u1_segno_arco_coer_p90", "  ... p90"),
              ("u1_verso_arco_coer", "coerenza VERSO [nullo IGNOTO]")):
    e = riga(c, nm, settore="U(1)")
    if e:
        esiti.append(e)

print("\n### C. CONTROLLI -- il fattore dello Step 2 e' DAVVERO diverso fra i bracci?")
print("-" * 104)
for c, nm in (("fatt_cs_scarto_max", "max|fatt_cs - 1|"),
              ("fatt_cs_frac_oltre_1pc", "frazione nodi |fatt_cs-1| > 1%"),
              ("cs_std", "cs dispersione"),
              ("n", "n nodi"),
              ("Lam", "Lam"),
              ("L_tot", "L_tot")):
    e = riga(c, nm, settore="controllo")
    if e:
        esiti.append(e)

print("\n" + "=" * 104)
spin = [e for e in esiti if e[4] == "SPIN" and e[3]]
u1 = [e for e in esiti if e[4] == "U(1)" and e[3]]
print("VERDETTO col criterio scritto prima:")
print("  firme di SPIN che ESCLUDONO lo zero : %d su %d" % (
    len(spin), len([e for e in esiti if e[4] == "SPIN"])))
for e in spin:
    print("     -> %s   Delta = %.4g +- %.4g" % (e[0], e[1], e[2]))
print("  osservabili U(1) che ESCLUDONO lo zero : %d su %d" % (
    len(u1), len([e for e in esiti if e[4] == "U(1)"])))
for e in u1:
    print("     -> %s   Delta = %.4g +- %.4g" % (e[0], e[1], e[2]))
print()
if spin:
    print("  *** ATTENZIONE: una firma di SPIN si e' mossa oltre la barra. E' la condizione del")
    print("      CRITERIO DI RETROCESSIONE scritto al momento della promozione. Va ESAMINATA, non")
    print("      archiviata: la promozione dello Step 2 e' in discussione.")
else:
    print("  NESSUNA firma di SPIN si muove oltre la barra: la predizione REGGE.")
    print("  NB: 'regge' non vuol dire 'lo Step 2 non fa nulla'. Vuol dire che NON organizza lo")
    print("      spin, che e' esattamente cio' che il suo stesso messaggio dichiara.")
print("=" * 104)
