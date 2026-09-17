# -*- coding: utf-8 -*-
"""VERDETTO su S, R, la DISPERSIONE di `r` e il conto FDT — 4 SEMI PER BRACCIO.

PERCHE' QUESTO SCRIPT ESISTE
----------------------------
Quattro domande aperte del registro si chiudono (o no) sugli STESSI dati, e nessuna di esse e'
decidibile con due semi:

  S  `chi` materia e' SOTTO 90 nel braccio OFF (89.778 / 89.876) e SOPRA 90 nell'ON
     (90.048 / 90.084): segno concorde su entrambi i semi. **Ma con 2 semi la dev.std ha UN
     grado di liberta' e `t(0.025, 1) = 12.706`: l'IC95 e' largo 1.2 gradi e contiene lo zero.**
     Criterio di chiusura gia' scritto nel registro: **>= 4 semi per braccio** (`t(3) = 3.182`).

  R  L'attesa `-0.69` del divario T3 usa il `sigma` del braccio VECCHIO (-1.078), ma l'anello
     `tau -> omega -> phi -> psi -> inerzia -> sigma` mette `sigma` A VALLE di `tau`. Si
     RICALCOLA l'attesa `sigma + tau/2` col `sigma` DI QUEL BRACCIO (colonne `t3_*`, MISURA F).

  r  La DISPERSIONE di `r` (mai la mediana: `median(r) = 1.0` per costruzione, C12) era
     ~10 % piu' alta nel braccio ON su 2 semi. Effetto o rumore?

  FDT Il conto che ha refutato Gilbert e' stato fatto con la FASE 5 INERTE (C11) e senza
     `--cs-dinamico`. Si rifa' sugli ingredienti misurati sul sistema pulito (colonne `fdt_*`).

LA BARRA (P3 / C10)
-------------------
Per confrontare due BRACCI si usa la **dispersione FRA SEMI**, mai la `SE` interna a un run: su
questo sistema caotico la pendenza cambia di **0.03 a codice INVARIATO**, contro una `SE` interna
di ~**0.010**. Qui ogni media fra semi porta `sd` (n-1 gradi di liberta') e IC95 con il `t` GIUSTO
per quel numero di gradi di liberta', stampato accanto.

USO
---
python csv/_test_fork/_verdetto_S_R.py
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
import glob
import math
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
NULL_MEDIA, NULL_STD = 90.000, 39.171     # direzioni di Bloch casuali (CLAUDE.md par.9)
BLOB_ATTESO = "08784685eeb17835389d248a2d1d07db4f0d1305"
SEMI = (1, 2, 3, 4)
BRACCI = (("OFF", "csOFF", 0), ("ON", "csON", 1))
# t di Student a due code, 95 %, per gradi di liberta' 1..7. NON si usa 1.96: con pochi semi
# sarebbe una barra falsa, ed e' l'errore che questo script esiste per non ripetere.
T95 = {1: 12.706, 2: 4.303, 3: 3.182, 4: 2.776, 5: 2.571, 6: 2.447, 7: 2.365}


def leggi_ultima(percorso):
    with open(percorso) as f:
        righe = list(csv.DictReader(f))
    return (righe[-1], len(righe)) if righe else (None, 0)


def num(riga, chiave, gradi=False):
    v = riga.get(chiave)
    if v is None or v == "":
        return float("nan")
    try:
        x = float(v)
    except ValueError:
        return float("nan")
    return math.degrees(x) if gradi else x


def media_ic(valori, etichetta=""):
    """media, sd (n-1), SE, IC95 col `t` GIUSTO per i gradi di liberta' effettivi."""
    v = np.asarray([x for x in valori if np.isfinite(x)], float)
    n = v.size
    if n == 0:
        return dict(n=0, media=float("nan"), sd=float("nan"), se=float("nan"),
                    lo=float("nan"), hi=float("nan"), t=float("nan"), eti=etichetta)
    if n == 1:
        return dict(n=1, media=float(v[0]), sd=float("nan"), se=float("nan"),
                    lo=float("nan"), hi=float("nan"), t=float("nan"), eti=etichetta)
    m = float(v.mean()); sd = float(v.std(ddof=1)); se = sd / math.sqrt(n)
    t = T95.get(n - 1, 1.96)
    return dict(n=n, media=m, sd=sd, se=se, lo=m - t * se, hi=m + t * se, t=t, eti=etichetta)


def riga_ic(d, fmt="%+9.4f"):
    if d["n"] == 0:
        return "   (nessun dato)"
    if d["n"] == 1:
        return ("   n=1  media " + fmt + "   (un solo seme: NESSUNA barra possibile)") % d["media"]
    return ("   n=%d  media " + fmt + "   sd " + fmt + "   SE " + fmt +
            "   IC95 [" + fmt + ", " + fmt + "]  (t(%d)=%.3f)") % (
        d["n"], d["media"], d["sd"], d["se"], d["lo"], d["hi"], d["n"] - 1, d["t"])


# ---------------------------------------------------------------------------------------------
# 0. RACCOLTA + CONFORMITA' P6
# ---------------------------------------------------------------------------------------------
print("=" * 112)
print("VERDETTO S / R / dispersione di r / FDT — 4 semi per braccio")
print("=" * 112)
print()
print("CONFORMITA' P6 — ogni run deve portare nei DATI blob, seme e TUTTI i flag che lo")
print("distinguono. Un file che si distingue dagli altri solo per il NOME non e' un dato.")
print("-" * 112)

dati = {}
conformi = {}
for eti, tag, tau_atteso in BRACCI:
    for s in SEMI:
        perc = os.path.join(HERE, "_vuoto_%s_s%d.vuoto.csv" % (tag, s))
        if not os.path.exists(perc):
            print("  %-6s s%d   ASSENTE: %s" % (eti, s, os.path.basename(perc)))
            continue
        u, ncamp = leggi_ultima(perc)
        if u is None:
            print("  %-6s s%d   VUOTO" % (eti, s))
            continue
        chk = []
        chk.append(("blob", u.get("blob", "") == BLOB_ATTESO, u.get("blob", "(assente)")[:8]))
        chk.append(("seme", num(u, "seed") == s, u.get("seed", "(assente)")))
        chk.append(("TAU_LUCE", num(u, "TAU_LUCE") == tau_atteso, u.get("TAU_LUCE", "(assente)")))
        chk.append(("CS_DINAMICO", num(u, "CS_DINAMICO") == 1, u.get("CS_DINAMICO", "(assente)")))
        chk.append(("KURAMOTO", num(u, "KURAMOTO_SU2") == 0, u.get("KURAMOTO_SU2", "(assente)")))
        chk.append(("STEP2", num(u, "STEP2") == 0, u.get("STEP2", "(assente)")))
        chk.append(("GAMMA_TURBO", num(u, "GAMMA_TURBO") == 1.0, u.get("GAMMA_TURBO", "(assente)")))
        chk.append(("cs_std vivo", np.isfinite(num(u, "cs_std")), u.get("cs_std", "(assente)")))
        # SPIN_LARMOR / TW_SPINORE: NON e' pignoleria. La ricostruzione della MISURA F non contiene
        # ne' `Bg` ne' `_otw`: se fossero accesi, le pendenze t3 sarebbero SBAGLIATE e non lo si
        # vedrebbe da nessun'altra parte (doc/MAPPA_accoppiamenti_spin.md par.4).
        for k in ("SPIN_LARMOR", "TW_SPINORE"):
            if k in u:
                chk.append((k, num(u, k) == 0, u.get(k)))
            else:
                chk.append((k + " (assente)", None, "n/d"))
        ok = all(c[1] for c in chk if c[1] is not None)
        manca = [c[0] for c in chk if c[1] is None]
        fail = [c[0] for c in chk if c[1] is False]
        conformi[(eti, s)] = ok and not manca
        stato = "PASS" if (ok and not manca) else ("PASS*" if ok else "FAIL")
        print("  %-6s s%d  [%-5s] campioni %3d  passo %5d  n %5d  blob %s  %s%s"
              % (eti, s, stato, ncamp, int(num(u, "passo")), int(num(u, "n")),
                 u.get("blob", "?")[:8],
                 "" if not fail else "  VIOLA: " + ",".join(fail),
                 "" if not manca else "  COLONNE ASSENTI: " + ",".join(manca)))
        dati[(eti, s)] = u

print()
print("  PASS* = tutti i campi presenti sono corretti, ma MANCA una colonna di certificazione:")
print("          il run non e' sbagliato, e' NON CERTIFICABILE DAI DATI per quel campo.")
print()

# ---------------------------------------------------------------------------------------------
# 1. VOCE S — `chi` materia: segnale o rumore?
# ---------------------------------------------------------------------------------------------
print("=" * 112)
print("1. VOCE S — `chi` MATERIA contro il null 90.000. LA POSSIBILE PRIMA FIRMA NON NULLA.")
print("=" * 112)
print("   Criterio scritto PRIMA (doc/RAMIFICAZIONI.md D.2/S): segno concorde su 4 semi per")
print("   braccio E IC95 (con t(3)) che ESCLUDE 90  ->  prima firma non nulla. IC95 contiene 90")
print("   ->  S si chiude come RUMORE, come si e' chiusa |<n>| (C15).")
print("-" * 112)

chi_br = {}
for eti, tag, _ in BRACCI:
    vals = []
    for s in SEMI:
        u = dati.get((eti, s))
        if u is None:
            continue
        m = num(u, "chi_mat_media", gradi=True)
        sd = num(u, "chi_mat_std", gradi=True)
        nn = num(u, "chi_mat_n")
        se_int = sd / math.sqrt(nn) if nn > 1 else float("nan")
        print("   %-4s s%d   chi_mat %9.4f   scarto %+7.4f   (SE INTERNA %.4f, z_interno %+6.2f "
              "- NON e' la barra giusta)" % (eti, s, m, m - NULL_MEDIA, se_int,
                                             (m - NULL_MEDIA) / se_int if se_int > 0 else float("nan")))
        vals.append(m)
    chi_br[eti] = media_ic(vals, eti)
    d = chi_br[eti]
    print("   %-4s FRA SEMI:%s" % (eti, riga_ic(d)))
    if d["n"] >= 2:
        esclude = (d["lo"] > NULL_MEDIA) or (d["hi"] < NULL_MEDIA)
        print("        IC95 %s 90.000  ->  %s" %
              ("ESCLUDE" if esclude else "CONTIENE", "FIRMA" if esclude else "compatibile col null"))
    print()

if chi_br.get("OFF", {}).get("n", 0) >= 2 and chi_br.get("ON", {}).get("n", 0) >= 2:
    a, b = chi_br["OFF"], chi_br["ON"]
    diff = b["media"] - a["media"]
    se_d = math.hypot(a["se"], b["se"])
    gl = min(a["n"], b["n"]) - 1
    tcrit = T95.get(gl, 1.96)
    print("   CONTRASTO ON - OFF  = %+8.4f  +- %.4f   IC95 [%+.4f, %+.4f]  (t(%d)=%.3f)"
          % (diff, se_d, diff - tcrit * se_d, diff + tcrit * se_d, gl, tcrit))
    print("   -> il contrasto %s lo zero" %
          ("ESCLUDE" if abs(diff) > tcrit * se_d else "CONTIENE"))
print()

# ---------------------------------------------------------------------------------------------
# 1-bis. L'INDETERMINATO DI OFF_s2 — chi_p90
# ---------------------------------------------------------------------------------------------
print("=" * 112)
print("1-bis. L'INDETERMINATO — `chi_p90`. Era un SEME ANOMALO o un segnale nel braccio OFF?")
print("=" * 112)
print("   Contesto: OFF_s2 dava z_interno = -4.17 su chi_p90 mentre chi_materia nello stesso")
print("   seme dava -1.45 e i due ON davano -0.01 e +1.23. Se OFF_s3/s4 ripetono lo STESSO")
print("   SEGNO con la stessa forza, non era un seme: e' un segnale nel braccio OFF.")
print("-" * 112)
for eti, tag, _ in BRACCI:
    vals = []
    for s in SEMI:
        u = dati.get((eti, s))
        if u is None:
            continue
        m = num(u, "chi_p90_media", gradi=True)
        sd = num(u, "chi_p90_std", gradi=True)
        nn = num(u, "chi_p90_n")
        se_int = sd / math.sqrt(nn) if nn > 1 else float("nan")
        print("   %-4s s%d   chi_p90 %9.4f   scarto %+7.4f   n %6d   z_interno %+6.2f"
              % (eti, s, m, m - NULL_MEDIA, int(nn) if nn == nn else -1,
                 (m - NULL_MEDIA) / se_int if se_int > 0 else float("nan")))
        vals.append(m)
    print("   %-4s FRA SEMI:%s" % (eti, riga_ic(media_ic(vals))))
    print()

# ---------------------------------------------------------------------------------------------
# 2. VOCE R — l'attesa RICALCOLATA col `sigma` di quel braccio
# ---------------------------------------------------------------------------------------------
print("=" * 112)
print("2. VOCE R — l'attesa `sigma + tau/2` RICALCOLATA col `sigma` DI QUEL BRACCIO")
print("=" * 112)
print("   Se il divario si annulla entro la barra FRA SEMI (~0.03, C10), il divario T3 era un")
print("   ARTEFATTO DELLA PREDIZIONE (l'anello mette `sigma` a valle di `tau`); se no, l'anello")
print("   non era la causa — e in quel caso NON si cerca un colpevole nuovo (P1).")
print("-" * 112)
r_br = {}
for eti, tag, _ in BRACCI:
    col = {k: [] for k in ("t3_b_sigma", "t3_b_tau", "t3_b_theta", "t3_attesa", "t3_divario",
                           "t3_b_r", "t3_b_theta_coord", "t3_b_theta_prop",
                           "t3_attesa_coord", "t3_divario_coord",
                           "t3_attesa_prop", "t3_divario_prop", "t3_identita")}
    visti = 0
    for s in SEMI:
        u = dati.get((eti, s))
        if u is None or "t3_b_sigma" not in u:
            continue
        v = {k: num(u, k) for k in col}
        if not np.isfinite(v["t3_b_theta"]):
            continue
        visti += 1
        print("   %-4s s%d   sigma %+8.4f (SE %.4f, r2 %.3f, n %5d)   tau %+8.4f (SE %.4f)   "
              "theta %+8.4f (SE %.4f)   attesa %+8.4f   divario %+8.4f   nodi liberi %5d"
              % (eti, s, v["t3_b_sigma"], num(u, "t3_se_sigma"), num(u, "t3_r2_sigma"),
                 int(num(u, "t3_n_sigma")), v["t3_b_tau"], num(u, "t3_se_tau"),
                 v["t3_b_theta"], num(u, "t3_se_theta"), v["t3_attesa"], v["t3_divario"],
                 int(num(u, "t3_n_liberi"))))
        for k in col:
            col[k].append(v[k])
    if not visti:
        print("   %-4s   NESSUN dato t3: le colonne MISURA F non ci sono in questi CSV." % eti)
        print("        (i run del 2026-09-15 sono precedenti al cablaggio della MISURA F)")
        print()
        continue
    r_br[eti] = {k: media_ic(col[k]) for k in col}
    for k, nome in (("t3_b_sigma", "sigma            "), ("t3_b_tau", "tau              "),
                    ("t3_b_r", "r  (NUOVO)       "),
                    ("t3_b_theta_coord", "theta_COORD      "),
                    ("t3_b_theta_prop", "theta_PROP       "),
                    ("t3_attesa_coord", "ATTESA_coord     "),
                    ("t3_divario_coord", "DIVARIO_coord    "),
                    ("t3_attesa_prop", "ATTESA_prop      "),
                    ("t3_divario_prop", "DIVARIO_prop     "),
                    ("t3_attesa", "ATTESA  (legacy) "), ("t3_divario", "DIVARIO (legacy) ")):
        print("   %-4s %s fra semi:%s" % (eti, nome, riga_ic(r_br[eti][k])))
    d = r_br[eti]["t3_divario"]
    if d["n"] >= 2:
        print("        IC95 del divario %s lo ZERO  ->  %s"
              % ("ESCLUDE" if (d["lo"] > 0 or d["hi"] < 0) else "CONTIENE",
                 "l'anello NON spiega il divario" if (d["lo"] > 0 or d["hi"] < 0)
                 else "il divario e' compatibile con un ARTEFATTO DELLA PREDIZIONE"))
        print("        confronto con la barra di sistema (C10, 0.03): |divario| = %.4f  ->  %s"
              % (abs(d["media"]), "SOPRA" if abs(d["media"]) > 0.03 else "SOTTO"))
    if "t3_b_theta" in r_br[eti] and r_br[eti]["t3_b_theta"]["n"]:
        print("        per riferimento, l'attesa STORICA usata finora era -0.69 (sigma del "
              "braccio VECCHIO, -1.078): scarto di theta da -0.69 = %+.4f"
              % (r_br[eti]["t3_b_theta"]["media"] + 0.69))
    print()

# ---------------------------------------------------------------------------------------------
# 3. LA DISPERSIONE DI `r` (MAI la mediana: C12)
# ---------------------------------------------------------------------------------------------
print("=" * 112)
print("3. LA DISPERSIONE DI `r` — l'unico numero di `ritmo()` che sia LIBERO di cambiare (C12)")
print("=" * 112)
print("   `median(r) = 1.0` per costruzione, con qualunque orologio: misurarla e' un test VUOTO.")
print("   Su 2 semi la dispersione era ~10 %% piu' ALTA nel braccio ON. E' un effetto?")
print("-" * 112)
disp = {}
for eti, tag, _ in BRACCI:
    vals, med = [], []
    for s in SEMI:
        u = dati.get((eti, s))
        if u is None:
            continue
        print("   %-4s s%d   r_std %.4f   r_iqr %.4f   r_mediana %.6f  (controllo: deve valere 1)"
              % (eti, s, num(u, "r_std"), num(u, "r_iqr"), num(u, "r_mediana")))
        vals.append(num(u, "r_std")); med.append(num(u, "r_mediana"))
    disp[eti] = media_ic(vals)
    print("   %-4s r_std FRA SEMI:%s" % (eti, riga_ic(disp[eti], "%9.4f")))
    print()
if disp.get("OFF", {}).get("n", 0) >= 2 and disp.get("ON", {}).get("n", 0) >= 2:
    a, b = disp["OFF"], disp["ON"]
    diff = b["media"] - a["media"]
    se_d = math.hypot(a["se"], b["se"])
    gl = min(a["n"], b["n"]) - 1
    tcrit = T95.get(gl, 1.96)
    print("   ON - OFF = %+.4f +- %.4f   IC95 [%+.4f, %+.4f]  (t(%d)=%.3f)   ->  %s"
          % (diff, se_d, diff - tcrit * se_d, diff + tcrit * se_d, gl, tcrit,
             "EFFETTO" if abs(diff) > tcrit * se_d else "compatibile con RUMORE"))
    if a["media"]:
        print("   in relativo: %+.1f %%" % (100.0 * diff / a["media"]))
print()

# ---------------------------------------------------------------------------------------------
# 4. IL CONTO FDT, RIFATTO SUL SISTEMA PULITO
# ---------------------------------------------------------------------------------------------
print("=" * 112)
print("4. FDT — rifatto sugli ingredienti MISURATI (FASE 5 attiva, --cs-dinamico acceso)")
print("=" * 112)
print("   DERIVAZIONE (nessun parametro nuovo, e' quella di doc/ANALISI_gilbert_fdt.md):")
print("     rumore sul Bloch: D = 2*amp^2/dt")
print("     Langevin:  <th^2> = D/(2*lambda)        Boltzmann: <th^2> = 2*kT/|B|")
print("     =>  lambda = amp^2 * |B| / (2 * dt * kT)      con kT = Lam (l'unica temperatura")
print("         parameter-free: e' la scala da cui il rumore STESSO e' costruito).")
print("   CONTROLLO DI CONSISTENZA: kT_equipartizione = I*<omega^2>/3. Se kT_eq/Lam >> 1 il")
print("   sistema NON e' in equilibrio termico: e' equilibrio DINAMICO PILOTATO, e il FDT non")
print("   puo' fissare il coefficiente per una ragione STRUTTURALE, non di ampiezza.")
print("-" * 112)
print("   %-8s %-4s %10s %10s %11s %12s %12s %12s %10s"
      % ("braccio", "seme", "|B|", "amp", "Lam", "lambda", "tau_smorz", "tau_disord", "kT/Lam"))
print("   %-8s %-4s %10s %10s %11s %12s %12s %12s %10s"
      % ("", "", "mediana", "mediana", "", "[1/tempo]", "[passi]", "[passi]", ""))
fdt = {}
for eti, tag, _ in BRACCI:
    rap, tsm, tds, lam_l = [], [], [], []
    for s in SEMI:
        u = dati.get((eti, s))
        if u is None or "fdt_B_mediana" not in u:
            continue
        B = num(u, "fdt_B_mediana"); amp = num(u, "fdt_amp_mediana")
        Lam = num(u, "Lam"); DT = num(u, "fdt_DT")
        dtn = num(u, "fdt_dtn_mediana"); om2 = num(u, "fdt_om2_media")
        I = num(u, "fdt_inerzia_mediana"); om = num(u, "fdt_om_mediana")
        if not np.isfinite(B):
            continue
        lam = amp * amp * B / (2.0 * dtn * Lam) if (dtn > 0 and Lam > 0) else float("nan")
        # tempo di smorzamento in PASSI: 1/lambda e' un tempo, DT lo converte in passi
        t_sm = 1.0 / (lam * DT) if lam > 0 else float("nan")
        # tempo di DISORDINE in PASSI: passi per ruotare di 1 radiante, theta = |omega|*dt_n
        t_ds = 1.0 / (om * dtn) if (om > 0 and dtn > 0) else float("nan")
        kT_eq = I * om2 / 3.0
        rr = kT_eq / Lam if Lam > 0 else float("nan")
        print("   %-8s %-4d %10.4g %10.4g %11.4g %12.4g %12.4g %12.4g %10.3g"
              % (eti, s, B, amp, Lam, lam, t_sm, t_ds, rr))
        rap.append(rr); tsm.append(t_sm); tds.append(t_ds); lam_l.append(lam)
    if rap:
        fdt[eti] = dict(kT=media_ic(rap), tsm=media_ic(tsm), tds=media_ic(tds),
                        lam=media_ic(lam_l))
if not fdt:
    print("   NESSUN dato fdt_*: le colonne MISURA G non ci sono in questi CSV.")
else:
    print()
    for eti in fdt:
        print("   %-4s lambda   fra semi:%s" % (eti, riga_ic(fdt[eti]["lam"], "%12.4g")))
        print("   %-4s tau_smorzamento [passi]:%s" % (eti, riga_ic(fdt[eti]["tsm"], "%12.4g")))
        print("   %-4s tau_disordine   [passi]:%s" % (eti, riga_ic(fdt[eti]["tds"], "%12.4g")))
        print("   %-4s kT_equip/Lam:%s" % (eti, riga_ic(fdt[eti]["kT"], "%12.4g")))
        k = fdt[eti]["kT"]["media"]
        t1, t2 = fdt[eti]["tsm"]["media"], fdt[eti]["tds"]["media"]
        print("   %-4s  rapporto tau_smorzamento / tau_disordine = %.4g" % (eti, t1 / t2 if t2 else float("nan")))
        if k >= 1e6:
            print("   %-4s  LETTURA (fissata PRIMA): kT/Lam ~1e7 o piu'  ->  il FDT resta" % eti)
            print("         INAPPLICABILE per ragione STRUTTURALE. Un lambda ricavato li' sarebbe")
            print("         SCELTO, non derivato.  ->  NON SI CABLA.")
        elif k <= 100:
            print("   %-4s  LETTURA (fissata PRIMA): kT/Lam e' sceso a ordine 1-100  ->  il FDT" % eti)
            print("         torna applicabile. Se anche tau_smorzamento e' comparabile a")
            print("         tau_disordine, LLG e' DERIVATO: riportare e CHIEDERE IL VIA A LUCA.")
        else:
            print("   %-4s  LETTURA (fissata PRIMA): intermedio  ->  si riporta senza forzare." % eti)
        print()

print("=" * 112)
print("PROMEMORIA, perche' un verdetto si legge insieme ai suoi limiti:")
print("  - tutte le barre qui sono FRA SEMI (P3/C10). Le `SE` interne sono stampate solo dove")
print("    servono a dire quanto e' determinata la pendenza DI QUEL RUN, e sono ~3 volte troppo")
print("    piccole per confrontare due bracci.")
print("  - `theta` va letto SEMPRE: finche' resta oltre il giro per passo, ogni esito negativo")
print("    sul settore di spin e' quello che l'ALIASING produrrebbe da solo (C14).")
print("=" * 112)
for eti, tag, _ in BRACCI:
    for s in SEMI:
        u = dati.get((eti, s))
        if u is None:
            continue
        _tc = num(u, "theta_coord_giri_mediana")
        _tp = num(u, "theta_prop_giri_mediana")
        if np.isfinite(_tc):
            print("   %-4s s%d   theta_COORD %9.4g   theta_PROP %9.4g giri/passo   rapporto %.4f"
                  "   fr>360g(prop) %.4f   n %5d"
                  % (eti, s, _tc, _tp, _tp / _tc if _tc else float("nan"),
                     num(u, "theta_prop_fr_gt360g"), int(num(u, "n"))))
        else:
            print("   %-4s s%d   theta (LEGACY = prop) %10.4g giri/passo   fr>360g %.4f   n %5d"
                  "   [CSV precedente alle due convenzioni]"
                  % (eti, s, num(u, "theta_giri_mediana"), num(u, "theta_fr_gt360g"),
                     int(num(u, "n"))))
print("=" * 112)
