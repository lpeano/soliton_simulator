# -*- coding: utf-8 -*-
"""MARE v2 — LA DIAGNOSI: lo stato di partenza che il mandato chiede NON ESISTE come stato
piu' basso, e il conto che lo decide.

Gira con:  python proto_primo_ordine/diagnosi_v2.py
Scrive:    proto_primo_ordine/uscite/diagnosi_v2.json  e  .txt
           doc/REFERTO_proto_mare_v2_2026-10-08.md
"""
import io
import json
import os
import sys

import numpy as np

for _f in (sys.stdout, sys.stderr):
    try:
        _f.reconfigure(encoding="utf-8", errors="replace")
    except Exception:                                          # noqa: BLE001
        pass

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _QUI)
import proto as PR                                             # noqa: E402

RAD = os.path.dirname(_QUI)
FUORI = os.path.join(_QUI, "uscite")
REFERTO = os.path.join(RAD, "doc", "REFERTO_proto_mare_v2_2026-10-08.md")
NL = chr(10)
P = []
R = []


def stampa(s=""):
    P.append(s)
    print(s, flush=True)


def A(s=""):
    R.append(s)


def main():
    PR._niente_simulatore()
    os.makedirs(FUORI, exist_ok=True)
    d = {"domanda": "esiste uno stato di partenza FERMO ed ESTESO a g < 0?",
         "bracci": list(PR.BRACCI_V2), "semi": list(PR.SEMI), "g": list(PR.G_V2),
         "per_braccio": {}}
    stampa("=" * 104)
    stampa("MARE v2 -- LA DIAGNOSI: lo stato di partenza del mandato NON ESISTE come stato "
           "piu' basso")
    stampa("=" * 104)
    for br in PR.BRACCI_V2:
        d["per_braccio"][br] = {"semi": {}}
        for s in PR.SEMI:
            G = PR.grafo(s, u_identita=True)
            n = int(G["n"])
            wv, sk0 = PR.pesi_v2(G, br)
            # ### **`pesi_v2` restituisce `s_k` DI PRIMA in entrambi i bracci: il `s_k`
            # ### del braccio si ricalcola DAI PESI VERI**, altrimenti la riga <<dopo la
            # ### normalizzazione>> ripete il numero di prima -- un FALSO-UNO.
            sk = np.zeros(n)
            np.add.at(sk, G["i"], wv)
            np.add.at(sk, G["j"], wv)
            u, W, lam = PR.perron(G, wv)
            psi2 = np.stack([u, np.zeros(n)], axis=1).astype(complex)
            pr0 = PR.partecipazione(psi2)
            mm0 = float(np.max(u ** 2) / np.mean(u ** 2))
            neff = float(np.sum(u ** 2)) ** 2 / float(np.sum(u ** 4))
            H0 = PR.energia_v2(W, u.astype(complex), 0.0)
            q = float(np.sum(u ** 4))
            voci = {"lambda_max": lam, "PR_perron": pr0, "max_su_media_perron": mm0,
                    "n_eff_perron": neff, "H_esteso_g0": H0, "somma_rho2_esteso": q,
                    "s_k_dev_rel": float(sk.std() / sk.mean()),
                    "s_k_max_su_min": float(sk.max() / sk.min()),
                    "s_k_media": float(sk.mean()),
                    "s_k_dev_rel_prima": float(sk0.std() / sk0.mean()),
                    "s_k_max_su_min_prima": float(sk0.max() / sk0.min()), "g": {}}
            for g in PR.G_V2:
                if g == 0.0:
                    continue
                H_uno = 0.5 * g * n * n
                H_est = H0 + 0.5 * g * q
                Nso = 2.0 * lam / (abs(g) * (1.0 - 1.0 / neff))
                voci["g"]["%.1f" % g] = {
                    "H_un_nodo": H_uno, "H_esteso": H_est,
                    "vince": "UN NODO" if H_uno < H_est else "ESTESO",
                    "rapporto": H_uno / H_est,
                    "norma_di_soglia": Nso, "rho_0_di_soglia": Nso / n,
                    "non_linearita_a_quella_soglia": abs(g) * Nso / n}
            # ### la continuazione VERA, per confronto: dove finisce davvero
            ps, mu, W2, s2, tappe, fine = PR.continua(G, br, -5.0, dg=-0.25)
            voci["continuazione"] = {
                "tappe": len(tappe), "PR_finale": tappe[-1]["PR"],
                "max_su_media_finale": tappe[-1]["max_su_media"],
                "residuo_finale": tappe[-1]["residuo"],
                "fine_ramo": (fine or {}).get("g_fine_ramo"),
                "PR_lungo_il_ramo": [t["PR"] for t in tappe[:6]]}
            d["per_braccio"][br]["semi"][str(s)] = voci
            stampa("  %-9s seme %d: lambda_max %.4f  PR(Perron) %7.2f  max/media %7.2f  "
                   "n_eff %6.1f   s_k dev %.4f max/min %6.2f"
                   % (br, s, lam, pr0, mm0, neff, voci["s_k_dev_rel"],
                      voci["s_k_max_su_min"]))
            for g in PR.G_V2:
                if g == 0.0:
                    continue
                v = voci["g"]["%.1f" % g]
                stampa("      g = %6.1f: H(un nodo) %12.1f  H(esteso) %12.1f  -> %s   "
                       "rho_0 di soglia %.6f  (|g| rho_0 = %.5f)"
                       % (g, v["H_un_nodo"], v["H_esteso"], v["vince"],
                          v["rho_0_di_soglia"], v["non_linearita_a_quella_soglia"]))
            stampa("      continuazione a dg = -0.25: PR lungo il ramo %s   fine %s"
                   % (" ".join("%.1f" % x for x in voci["continuazione"]
                               ["PR_lungo_il_ramo"]),
                      voci["continuazione"]["fine_ramo"]))
    io.open(os.path.join(FUORI, "diagnosi_v2.json"), "w",
            encoding="utf-8").write(json.dumps(d, ensure_ascii=False))
    io.open(os.path.join(FUORI, "diagnosi_v2.txt"), "w",
            encoding="utf-8").write(NL.join(P) + NL)

    # ====================================================== il referto
    b0 = d["per_braccio"]["NON-NORM"]["semi"][str(PR.SEMI[0])]
    b1 = d["per_braccio"]["NORM"]["semi"][str(PR.SEMI[0])]
    A("# MARE `v2` — **LO STATO DI PARTENZA CHE IL MANDATO CHIEDE NON ESISTE COME STATO PIÙ "
      "BASSO, E IL CONTO LO DICE**")
    A("")
    A("*Referto generato da `proto_primo_ordine/diagnosi_v2.py`. Criteri e previsioni: "
      "`doc/TASK_HISTORY/2026-10-08_proto-mare-v2.md`, committato ### **prima** in "
      "`9baf4a1`.*")
    A("")
    A("> ### ⛔ **Simulatore `b8c21049`, `ASSIOMI.md` non toccato, e il prototipo NON importa "
      "il simulatore.** ### **Solo `U = I`**, come il mandato chiede.")
    A("")
    A("---")
    A("")
    A("# ⛔ `①` **L'ESITO: `LO STATO PIÙ BASSO È GIÀ UNA MASSA`, E SCATTA SUBITO SOTTO "
      "`g = 0`**")
    A("")
    A("Il mandato prevede questo esito *(«se il ramo esteso finisce prima di `g = -10`: "
      "riportalo come esito a sé, con il `g` in cui finisce»)*. ### ➜ **Finisce prima di "
      "quanto l'esito previsto lasciasse immaginare: NON c'è nessun `g < 0` in cui lo stato "
      "più basso sia esteso.**")
    A("")
    A("| | |")
    A("|---|---|")
    A("| il conto | a norma totale fissa `Σψ² = N`, lo stato su ### **un solo nodo** ha "
      "`ρ = N` e quindi `H = (g/2)·N²`; lo stato ### **esteso** ha "
      "`H ≈ −λ_max·N + (g/2)·N²/n_eff` |")
    A("| ### ➜ **perché vince sempre** | ### **`(g/2)N²` va come `N²`, l'esteso come `N`.** "
      "Con `N = n = 400` il primo è più basso del secondo di ### **ordini di grandezza**, per "
      "### **ogni** `g < 0` |")
    A("")
    A("| braccio | `g` | `H` su ### **un nodo** | `H` ### **esteso** | ### **vince** |")
    A("|---|--:|--:|--:|---|")
    for br in PR.BRACCI_V2:
        v = d["per_braccio"][br]["semi"][str(PR.SEMI[0])]
        for g in PR.G_V2:
            if g == 0.0:
                continue
            x = v["g"]["%.1f" % g]
            A("| `%s` | `%.1f` | ### **%.1f** | %.1f | ### **%s** |"
              % (br, g, x["H_un_nodo"], x["H_esteso"], x["vince"]))
    A("")
    A("> ### ✔ **E LA MISURA LO CONFERMA, non solo il conto:** la continuazione dal Perron, "
      "con la discesa a tempo immaginario, collassa a ### **`PR = 1.00`** *(tutta la norma su "
      "`UN` nodo, `max/media = 400`)* già al ### **primo** passo sotto `g = 0`, in "
      "### **entrambi** i bracci e per ### **entrambi** i passi di continuazione provati.")
    A("")
    A("| braccio | seme | `PR` lungo il ramo, dal Perron in giu' | ### **dove Newton si ferma** |")
    A("|---|--:|---|--:|")
    for br in PR.BRACCI_V2:
        for s in PR.SEMI:
            c = d["per_braccio"][br]["semi"][str(s)]["continuazione"]
            A("| `%s` | `%d` | %s | %s |"
              % (br, s, " → ".join("### **%.1f**" % x if k == 0 else "%.1f" % x
                                   for k, x in enumerate(c["PR_lungo_il_ramo"])),
                 ("### **`g = %.2f`**" % c["fine_ramo"]) if c["fine_ramo"] is not None
                 else "non si ferma *(ma e' gia' su UN nodo)*"))
    A("")
    A("> ### ⚠ **E NEL BRACCIO `NORM` NEWTON SI FERMA ANCHE LUI**, fra `g = -1.75` e "
      "`g = -2.50` ### **dopo** essere gia' collassato: non e' «il ramo esteso che finisce», "
      "e' ### **il ramo di UN NODO che smette di convergere.** ### ⛔ **Leggere quel `g` come "
      "«il ramo esteso finisce qui» sarebbe un FALSO-UNO**, e lo dico perche' il criterio del "
      "mandato chiede proprio quel numero.")
    A("")
    A("# ⛔ `②` **E NON ESISTE UN `ρ_0` CHE SALVI IL MARE: LE DUE CONDIZIONI SI ESCLUDONO**")
    A("")
    A("Lo stato su un nodo vince se `N > 2·λ_max / (|g|·(1 − 1/n_eff))`. ### ➜ **Sotto quella "
      "soglia il mare sopravvive come stato più basso — ma a quella densità la non linearità "
      "è TRASCURABILE:**")
    A("")
    A("| braccio | `g` | ### **`ρ_0` di soglia** | la non linearità lì: `\\|g\\|·ρ_0` | contro "
      "`λ_max` |")
    A("|---|--:|--:|--:|--:|")
    for br in PR.BRACCI_V2:
        v = d["per_braccio"][br]["semi"][str(PR.SEMI[0])]
        for g in PR.G_V2:
            if g == 0.0:
                continue
            x = v["g"]["%.1f" % g]
            A("| `%s` | `%.1f` | ### **%.6f** | ### **%.5f** | `%.4f` |"
              % (br, g, x["rho_0_di_soglia"], x["non_linearita_a_quella_soglia"],
                 v["lambda_max"]))
    A("")
    A("> ### ⛔ **QUINDI: «il mare è lo stato più basso» e «la non linearità conta» NON "
      "possono valere insieme in QUESTA `H`.** ### **Non è un difetto del metodo né una "
      "scelta sbagliata di `ρ_0`: è una proprietà della forma di `H`**, e vale per ### **ogni** "
      "`ρ_0`.")
    A("")
    A("> ### ⚠ **E IL RAMO ESTESO ESISTE ANCORA — come SELLA, non come minimo.** Seguirlo "
      "serve un metodo che ### **non scenda**; una discesa ci cade fuori ### **per "
      "costruzione**, e infatti ci cade. ### ➜ **Un esperimento sul ramo esteso misurerebbe "
      "«una sella instabile decade», che NON è «l'interferenza fa nascere le masse».**")
    A("")
    A("# ⭐ `③` **CHE COSA SI È MISURATO LUNGO LA STRADA**")
    A("")
    A("| | `NON-NORM` | `NORM` |")
    A("|---|--:|--:|")
    A("| `λ_max` | %s | %s |" % (("%.4f" % b0["lambda_max"]), ("%.4f" % b1["lambda_max"])))
    A("| ### **`PR` dell'autovettore di Perron** *(a `g = 0`)* | ### **%s** | ### **%s** |"
      % (("%.2f" % b0["PR_perron"]), ("%.2f" % b1["PR_perron"])))
    A("| ### **`max/media` del Perron** | ### **%s** | ### **%s** |"
      % (("%.2f" % b0["max_su_media_perron"]), ("%.2f" % b1["max_su_media_perron"])))
    A("| `s_k` ### **del braccio**: media | %s | ### **%s** |"
      % (("%.4f" % b0["s_k_media"]), ("%.4f" % b1["s_k_media"])))
    A("| `s_k` ### **del braccio**: deviazione relativa | %s | ### **%s** |"
      % (("%.4f" % b0["s_k_dev_rel"]), ("%.4f" % b1["s_k_dev_rel"])))
    A("| `s_k`: `max/min` | %s | ### **%s** |"
      % (("%.2f" % b0["s_k_max_su_min"]), ("%.2f" % b1["s_k_max_su_min"])))
    A("")
    A("> ### ⭐ **IL NUMERO CHE VALE È IL `PR` DEL PERRON A `g = 0`:** nel braccio "
      "### **`NON-NORM`** lo stato più basso ### **LINEARE** è già concentrato su "
      "### **%s** nodi su `400` *(`max/media` = %s)*. ### ➜ **La geometria da sola, senza "
      "nessuna non linearità, concentra quasi tutto.** Nel braccio ### **`NORM`** il `PR` è "
      "### **%s**: la normalizzazione ### **toglie quasi tutta** quella concentrazione."
      % (("%.1f" % b0["PR_perron"]), ("%.2f" % b0["max_su_media_perron"]),
         ("%.1f" % b1["PR_perron"])))
    A("")
    A("> ### ⚠ **E LA NORMALIZZAZIONE TOCCA `A3`, con la precisione che serve:** `s_k` è una "
      "### **SOMMA** sul proprio intorno, non una mediana né una media, quindi il meccanismo "
      "che `A3` nomina — *«il centro diventa `1` per identità»* — ### **non scatta**: dopo la "
      "normalizzazione `s̃_k` ha deviazione relativa ### **%s** contro `%s` di prima, e "
      "`max/min` ### **%s** contro `%s` -- ### **CALA, ma NON va a `1` per identita'**, e la "
      "media resta ### **%s**, non `1`. "
      "### ⛔ **La scelta fra le due forme resta una DECISIONE DI LUCA.**"
      % (("%.4f" % b1["s_k_dev_rel"]), ("%.4f" % b1["s_k_dev_rel_prima"]),
         ("%.2f" % b1["s_k_max_su_min"]), ("%.2f" % b1["s_k_max_su_min_prima"]),
         ("%.4f" % b1["s_k_media"])))
    A("")
    A("# ⛔ `④` **TRE METODI PROVATI, E I PRIMI DUE ERANO SBAGLIATI — MISURATO, NON "
      "ARGOMENTATO**")
    A("")
    A("| metodo | che cosa ha fatto | come l'ho saputo |")
    A("|---|---|---|")
    A("| Newton ### **pieno** | ### ⛔ **SALTAVA**: `PR = 2.0` con `Δg = -0.25`, `1.0` con "
      "`-0.05` | ### **rifacendo la continuazione con un `Δg` più fine**: un risultato che "
      "dipende dal passo ### **non sta sul ramo** |")
    A("| Newton ### **smorzato** | non saltava più, ma ### **non convergeva** *(si fermava al "
      "primo `g`)* | il residuo restava sopra la soglia |")
    A("| ### **discesa a tempo immaginario + Newton** | ### **coerente fra i passi**, e "
      "collassa a `PR = 1` | i due `Δg` danno ### **lo stesso** risultato |")
    A("")
    A("> ### ⚠ **E UN DIFETTO MIO NEL CRITERIO, che era `A3c`:** misuravo il residuo del "
      "vincolo `\\|Σψ² − n\\|` in ### **assoluto** contro `1e-12`, ma quella somma vale `400` e "
      "la precisione macchina su `400` termini è già `~1e-12`. ### **Un `1.82e-12` assoluto è "
      "`4.5e-15` relativo, cioè ZERO** — e il ramo «finiva» per un confronto fra grandezze "
      "### **non commensurabili**. ### **Ora il residuo è relativo.**")
    A("")
    A("---")
    A("")
    A("# ⛔ **CHE COSA QUESTO REFERTO NON DICE**")
    A("")
    A("| | |")
    A("|---|---|")
    A("| che l'interferenza ### **non** faccia nascere le masse | ### ⛔ **NO.** Dice che "
      "### **in questa `H`, a norma fissa, non esiste un mare da cui farle nascere**: lo "
      "stato più basso è già una massa |")
    A("| i ### **criteri** del mandato | ### **non sono stati valutati**: l'esperimento "
      "richiede uno stato di partenza ### **fermo ed esteso**, e quello ### **non esiste** |")
    A("| che la colpa sia di ### **`ρ_0`** | ### ⛔ **no, ed è misurato:** per ogni `ρ_0` che "
      "salva il mare la non linearità scende a `~1e-2`, cioè ### **sparisce** |")
    A("| che cosa fare | ### ⛔ **è una DECISIONE DI LUCA.** Le strade che il conto lascia "
      "aperte: una `H` con un termine che ### **penalizzi** la concentrazione *(un `ρ²` "
      "repulsivo, o un vincolo locale)*; oppure studiare il ramo esteso ### **come sella**, "
      "dichiarando che si misura un decadimento; oppure un `g` ### **positivo** |")
    A("| l'esperimento del ### **pacchetto** | ### ⛔ **non girato**, come nel `v1` |")
    A("")
    io.open(REFERTO, "w", encoding="utf-8", newline=NL).write(NL.join(R) + NL)
    stampa()
    stampa("scritto %s (%d righe)" % (REFERTO, len(R)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
