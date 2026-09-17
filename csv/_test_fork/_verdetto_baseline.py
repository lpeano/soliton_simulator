# -*- coding: utf-8 -*-
"""VERDETTO della BASELINE del sistema CORRETTO (blob c57800c1) — e, se ci sono, dei run col TURBO.

PERCHE' ESISTE
--------------
Il sistema e' cambiato TRE volte dall'ultima tornata di misure: taglio spettrale del rumore (flag,
OFF di default), `_xi_rumore` NON piu' ereditato, e il fattore `cs^-2` nell'inerzia.
**Ogni numero precedente viene da un sistema DIVERSO da quello sul disco.** Senza una baseline del
sistema corretto, il turbo non ha un confronto.

LA BARRA, e va detta prima dei numeri (P3 / C10)
------------------------------------------------
Su questo sistema caotico una pendenza trasversale cambia di **0.03 a codice INVARIATO**, mentre la
`SE` interna a un run vale ~0.010. Per confrontare due BRACCI si usa la **dispersione FRA SEMI**.
**E con 2 semi per braccio la dev.std ha UN grado di liberta': `t(0.025,1) = 12.706`.**
**Nessun IC95 a due semi decide alcunche'**: si potra' dire il **segno** e l'**ordine di
grandezza**, non stabilire un effetto (presidio di `CLAUDE.md` par.9).

USO
---
python csv/_test_fork/_verdetto_baseline.py
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
import csv
import math
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
BLOB = "c57800c1051c6884fbfadd70c2c2f2930a284aee"
NULL_CHI_M, NULL_CHI_S = 90.000, 39.171     # direzioni di Bloch casuali (CLAUDE.md par.9)
NULL_N_M, NULL_N_S = 0.9213, 0.3888         # nullo EMPIRICO di |<n>|/(1/sqrt(N)) (C15)
SEMI = (1, 2)
BRACCI = (("OFF", "base_OFF", 0, 1.0), ("ON", "base_ON", 1, 1.0),
          ("TURBO", "turbo_ON", 1, 100.0))
T95 = {1: 12.706, 2: 4.303, 3: 3.182, 4: 2.776, 5: 2.571}


def num(u, k, gradi=False):
    v = u.get(k)
    if v is None or v == "":
        return float("nan")
    try:
        x = float(v)
    except ValueError:
        return float("nan")
    return math.degrees(x) if gradi else x


def ic(vals, eti=""):
    v = np.asarray([x for x in vals if np.isfinite(x)], float)
    n = v.size
    if n == 0:
        return dict(n=0)
    if n == 1:
        return dict(n=1, m=float(v[0]))
    m = float(v.mean()); sd = float(v.std(ddof=1)); se = sd / math.sqrt(n)
    t = T95.get(n - 1, 1.96)
    return dict(n=n, m=m, sd=sd, se=se, lo=m - t * se, hi=m + t * se, t=t)


def riga(d, f="%+10.4f"):
    if d.get("n", 0) == 0:
        return "   (nessun dato)"
    if d["n"] == 1:
        return ("   n=1  " + f + "   (UN SOLO SEME: nessuna barra possibile)") % d["m"]
    return ("   n=%d  media " + f + "   sd " + f + "   IC95 [" + f + ", " + f + "]  (t(%d)=%.3f)") % (
        d["n"], d["m"], d["sd"], d["lo"], d["hi"], d["n"] - 1, d["t"])


print("=" * 116)
print("BASELINE DEL SISTEMA CORRETTO — blob c57800c1 (taglio spettrale + xi fresco + fattore cs^-2)")
print("=" * 116)
print()
print("CONFORMITA' P6 — letta dai DATI, non dal nome del file")
print("-" * 116)
dati = {}
for eti, tag, tl, gt in BRACCI:
    for s in SEMI:
        p = os.path.join(HERE, "_vuoto_%s_s%d.vuoto.csv" % (tag, s))
        if not os.path.exists(p):
            continue
        with open(p) as f:
            rr = list(csv.DictReader(f))
        if not rr:
            continue
        u = rr[-1]
        chk = [("blob", u.get("blob", "") == BLOB),
               ("seme", num(u, "seed") == s),
               ("TAU_LUCE", num(u, "TAU_LUCE") == tl),
               ("CS_DINAMICO", num(u, "CS_DINAMICO") == 1),
               ("cs_std vivo", np.isfinite(num(u, "cs_std"))),
               ("KURAMOTO", num(u, "KURAMOTO_SU2") == 0),
               ("STEP2", num(u, "STEP2") == 0),
               ("GAMMA_TURBO", num(u, "GAMMA_TURBO") == gt),
               ("SPIN_LARMOR", num(u, "SPIN_LARMOR") == 0),
               ("TW_SPINORE", num(u, "TW_SPINORE") == 0)]
        viola = [c[0] for c in chk if not c[1]]
        print("  %-6s s%d  [%s]  campioni %3d  passo %5d  n %5d  blob %s%s"
              % (eti, s, "PASS" if not viola else "FAIL", len(rr), int(num(u, "passo")),
                 int(num(u, "n")), u.get("blob", "?")[:8],
                 "" if not viola else "   VIOLA: " + ",".join(viola)))
        if not viola:
            dati[(eti, s)] = u
        else:
            print("       ^ QUESTO RUN NON CONTA (par.6 del mandato: un campo che non combacia)")
print()
if not dati:
    raise SystemExit("nessun run conforme: niente da leggere.")


def sezione(titolo, righe, nota=None):
    print("=" * 116)
    print(titolo)
    print("=" * 116)
    if nota:
        print(nota)
    print("-" * 116)
    presenti = [e for e, _, _, _ in BRACCI if any((e, s) in dati for s in SEMI)]
    for eti in presenti:
        vals = {}
        for etichetta, chiave, gradi, fmt in righe:
            v = [num(dati[(eti, s)], chiave, gradi) for s in SEMI if (eti, s) in dati]
            for s, x in zip([s for s in SEMI if (eti, s) in dati], v):
                print("   %-6s s%d  %-26s %s" % (eti, s, etichetta, fmt % x))
            vals[etichetta] = ic(v)
        for etichetta, *_ in righe:
            print("   %-6s FRA SEMI  %-24s %s" % (eti, etichetta, riga(vals[etichetta])))
        print()


sezione("1. chi — l'angolo fra Bloch vicini.  NULLO: 90.000 +- 39.171 (direzioni casuali)",
        [("chi materia", "chi_mat_media", True, "%10.4f"),
         ("chi vuoto", "chi_vuo_media", True, "%10.4f"),
         ("chi p90", "chi_p90_media", True, "%10.4f"),
         ("frazione < 10 gradi", "chi_mat_fr_lt10g", False, "%10.6f"),
         ("frazione > 170 gradi", "chi_mat_fr_gt170g", False, "%10.6f")],
        "   Scarto da 90 = il segnale. Con 2 semi NON si decide: si legge il SEGNO.")

sezione("2. |<n>| — isotropia.  NULLO EMPIRICO: 0.9213 +- 0.3888 in unita' di 1/sqrt(N) (C15)",
        [("|<n>| / (1/sqrt N)", "nmed_tot_sigma", False, "%10.4f"),
         ("|<n>| materia / atteso", "nmed_mat_sigma", False, "%10.4f")])

sezione("3. theta — LE DUE CONVENZIONI (C19). MAI citare theta senza dire quale.",
        [("theta_COORD giri/passo", "theta_coord_giri_mediana", False, "%10.4f"),
         ("theta_PROP  giri/passo", "theta_prop_giri_mediana", False, "%10.4f"),
         ("frazione oltre il giro", "theta_prop_fr_gt360g", False, "%10.4f"),
         ("omega/sqrt(n)", "omega_su_sqrtn", False, "%10.4g")],
        "   theta_coord = |omega|*DT (coordinata)   theta_prop = |omega|*dt_n (proprio, giusto).\n"
        "   omega/sqrt(n): se smette di essere costante, la forzante e' diventata COERENTE.")

sezione("4. r — la DISPERSIONE (mai la mediana: median(r) = 1 per costruzione, C12), e per ETA'",
        [("r_std (popolazione)", "r_std", False, "%10.4f"),
         ("r mediana (controllo=1)", "r_mediana", False, "%10.6f"),
         ("r mediana eta q1 (giovani)", "r_eta_q1_mediana", False, "%10.4f"),
         ("r mediana eta q4 (maturi)", "r_eta_q4_mediana", False, "%10.4f"),
         ("r mediana NEONATI", "r_eta_neonati_mediana", False, "%10.4f")],
        "   Il figlio eredita `_psi_prec` dal padre: il suo PRIMO `r` confronta la propria fase\n"
        "   con quella del PADRE. `eta` parte da zero ma l'orologio no.")

sezione("5. L_tot = somma(inerzia*|omega|) — LA CONSERVAZIONE (C20: ~+3.4 %/passo nel sigillo)",
        [("L_tot finale", "L_tot", False, "%10.4g"),
         ("dL/L con mitosi (mediana)", "L_dL_con_mitosi_mediana", False, "%10.5f"),
         ("dL/L senza mitosi (mediana)", "L_dL_senza_mitosi_mediana", False, "%10.5f"),
         ("nodi nati", "L_nodi_nati", False, "%10.0f")],
        "   `omega` e' intensiva: alla mitosi dovrebbe ripartirsi l'INERZIA, e non lo fa.\n"
        "   Il confronto FRA BRACCI e' fra traiettorie caotiche diverse: si legge l'ORDINE, non lo scarto.")

sezione("6. IL FATTORE (CS_M/cs)^2 — quanto si discosta da 1?  E' il numero che dice se il TURBO\n"
        "   ha svegliato `cs` o se il test e' NULLO",
        [("fattore mediano", "fatt_cs_mediana", False, "%12.8f"),
         ("fattore max", "fatt_cs_max", False, "%12.8f"),
         ("scarto max da 1", "fatt_cs_scarto_max", False, "%12.3e"),
         ("frazione oltre l'1 %", "fatt_cs_frac_oltre_1pc", False, "%12.4f"),
         ("cs_std / cs", "cs_std", False, "%12.3e")],
        "   SE `frazione oltre l'1 %` RESTA ~0 COL TURBO, IL TEST E' NULLO: si dice, non si forza.")

print("=" * 116)
print("7. AUTOCORRELAZIONE <n_i . n_j> per bin di distanza (10 bin, ultimo campione)")
print("=" * 116)
for eti, _, _, _ in BRACCI:
    for s in SEMI:
        if (eti, s) not in dati:
            continue
        u = dati[(eti, s)]
        vv = [(num(u, "ac%d_d" % b), num(u, "ac%d" % b), num(u, "ac%d_se" % b)) for b in range(10)]
        zmax = max((abs(a / se) for _, a, se in vv if np.isfinite(se) and se > 0), default=float("nan"))
        print("   %-6s s%d   max |ac|/SE sui 10 bin = %6.2f   (il nullo empirico su 40 bin dava 2.2-2.5)"
              % (eti, s, zmax))
        print("        " + "  ".join("%5.3f" % a for _, a, _ in vv))
print()
print("=" * 116)
print("PROMEMORIA — come si legge tutto questo")
print("  * la barra fra BRACCI e' la dispersione FRA SEMI (0.03), MAI la SE interna a un run;")
print("  * con 2 semi t(0.025,1) = 12.706: NESSUN IC95 decide. Si legge SEGNO e ORDINE DI GRANDEZZA;")
print("  * `theta` non si cita senza dire quale convenzione (C19);")
print("  * finche' `theta` resta oltre il giro per passo, ogni esito negativo sullo spin e' quello")
print("    che l'ALIASING produrrebbe da solo (C14).")
print("=" * 116)
