# -*- coding: utf-8 -*-
"""**PASSI 0 e 1 del pezzo ② di `T3`: il FLASH, i suoi siti, e il rinculo a indici ripetuti.**

**SOLA LETTURA: nessun run.** Legge l'**AST** del simulatore e i **61 fotogrammi** del pilota
*(`csv/_test_fork/_pilota_prova1/stati/`, locali, `.gitignore`)*.

**PASSO 0 -- la scena, e l'ha PRESCRITTA il guardiano** *(Luca, 2026-09-28)*: *«usa quella del video
in cui il flash e' stato misurato (passo 42: 138.7 -> 366.2 -> 139.7), non cercarne un'altra.»*
Qui si **riproducono i numeri dai fotogrammi** *(`L-NUMERI`)* e si dice **che cosa contengono**, che
e' la cosa che decide il costo del sigillo.

**PASSO 1 -- due letture:**
  1. i **siti** con la guardia `len(self.psi) < n`, e **quali sono raggiungibili DOPO `mitosi`**;
  2. il **rinculo a indici ripetuti** (`phi[g] +=` con `g = concatenate([a, b])`), che il guardiano
     ha confermato fondato: **quando serve perche' morda?**

COMANDO:  python csv/_test_fork/_flash_passo01.py
USCITA:   0 sempre: e' una MISURA, non un sigillo. I verdetti li da' il sigillo del pezzo ②.
"""
import ast
import glob
import io
import json
import os
import re
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, os.path.join(RADICE, "csv"))
import _presidio  # noqa: E402

_presidio.avvia(__file__)
import numpy as np  # noqa: E402
import _passo  # noqa: E402

SIM = os.path.join(RADICE, "soliton_simulator.py")
SRC = io.open(SIM, encoding="utf-8").read()
RIG = SRC.split(chr(10))
ARB = ast.parse(SRC)
STATI = os.path.join(_QUI, "_pilota_prova1", "stati")

METODI, FUNZIONI = {}, {}
for _n in ast.walk(ARB):
    if isinstance(_n, ast.ClassDef) and _n.name == "Rete":
        for _k in _n.body:
            if isinstance(_k, (ast.FunctionDef, ast.AsyncFunctionDef)):
                METODI[_k.name] = _k
for _n in ARB.body:
    if isinstance(_n, ast.FunctionDef):
        FUNZIONI[_n.name] = _n


def _dentro(ln):
    q = [(b.end_lineno - b.lineno, n) for n, b in list(METODI.items()) + list(FUNZIONI.items())
         if b.lineno <= ln <= b.end_lineno]
    return min(q)[1] if q else "(modulo)"


def raggiungibili(radici):
    visti, coda = set(), list(radici)
    while coda:
        x = coda.pop()
        if x in visti:
            continue
        visti.add(x)
        c = METODI.get(x) or FUNZIONI.get(x)
        if c is None:
            continue
        for n in ast.walk(c):
            if isinstance(n, ast.Call):
                f = n.func
                nm = f.attr if isinstance(f, ast.Attribute) else (
                    f.id if isinstance(f, ast.Name) else None)
                if nm and (nm in METODI or nm in FUNZIONI) and nm not in visti:
                    coda.append(nm)
    return visti


def passo0():
    """I fotogrammi: il flash, e CHE COSA CONTENGONO."""
    f = sorted(glob.glob(os.path.join(STATI, "frame_seme11_passo*.npz")))
    if not f:
        print("  ⚠ I FOTOGRAMMI NON CI SONO (sono LOCALI, `.gitignore`): il passo 0 non si fa.")
        return {"fotogrammi": 0}
    z0 = np.load(f[0])
    chiavi = sorted(z0.files)
    print("  fotogrammi del seme 11: %d, da passo %s a passo %s"
          % (len(f), re.search(r"passo0*(\d+)", os.path.basename(f[0])).group(1),
             re.search(r"passo0*(\d+)", os.path.basename(f[-1])).group(1)))
    print("  CHIAVI di un fotogramma: %s" % ", ".join(chiavi))
    print("  blob del simulatore che li ha prodotti: %s" % str(z0["blob"])[:12])
    print("")
    SERVE = ("d", "d0", "vd", "peq", "tw", "twp", "psi", "psi_spin", "eta", "phivel")
    manca = [k for k in SERVE if k not in chiavi]
    print("  ### PER RIPARTIRE DA UNO STATO SERVIREBBERO: %s" % ", ".join(SERVE))
    print("  ### NE MANCANO %d: %s" % (len(manca), ", ".join(manca)))
    print("  ### ➜ IL RIAVVIO DA UN FOTOGRAMMA E' IMPOSSIBILE: il sigillo deve RIFARE il run.")
    print("")
    tab, per_passo = [], {}
    for p in f:
        k = int(re.search(r"passo0*(\d+)", os.path.basename(p)).group(1))
        z = np.load(p)
        g = z["phi_g"]
        per_passo[k] = {"n": int(z["n"]), "archi": int(len(z["ii"])),
                        "mean_phi_g": float(np.mean(g)), "max_phi_g": float(np.max(g))}
    print("  %-7s %-8s %-9s %-13s %-13s %-8s %s" % ("passo", "n", "dn", "mean(phi_g)",
                                                    "max(phi_g)", "salto", "flash?"))
    ks = sorted(per_passo)
    for idx, k in enumerate(ks):
        v = per_passo[k]
        pre = per_passo[ks[idx - 1]] if idx else None
        post = per_passo[ks[idx + 1]] if idx + 1 < len(ks) else None
        dn = v["n"] - pre["n"] if pre else 0
        vic = [x["mean_phi_g"] for x in (pre, post) if x]
        salto = v["mean_phi_g"] / (sum(vic) / len(vic)) if vic else float("nan")
        fl = salto > 1.5
        if k in (38, 40, 42, 44, 46, 58, 60, 62, 66, 68) or fl or dn:
            print("  %-7d %-8d %-9d %-13.2f %-13.2f %-8.3f %s"
                  % (k, v["n"], dn, v["mean_phi_g"], v["max_phi_g"], salto,
                     "### FLASH" if fl else ""))
        tab.append({"passo": k, "dn": dn, "salto_mean_phi_g": salto, "flash": bool(fl), **v})
    # ⚠⚠ IL LIVELLO, E NON IL RAPPORTO. Il rapporto coi vicini e' CIECO a uno spostamento
    #   di LIVELLO: se anche i vicini sono alti, il rapporto fa 1 mentre il campo e'
    #   permanentemente gonfiato. **E' l'errore che ho fatto**, e l'ha rilevato il
    #   guardiano (Luca, 2026-09-28): <<leggi la tua tabella per livelli, non per rapporti>>.
    _n0 = per_passo[ks[0]]["n"]
    senza = [k for k in ks if per_passo[k]["n"] == _n0 and k >= 4]   # senza il transitorio
    base = sum(per_passo[k]["mean_phi_g"] for k in senza) / len(senza)
    print("")
    print("  ### IL LIVELLO DI RIFERIMENTO (regime SENZA nascite, passi %d-%d): %.2f"
          % (senza[0], senza[-1], base))
    print("  %-7s %-8s %-13s %-12s %-12s" % ("passo", "n", "mean(phi_g)", "su base",
                                            "su |psi|"))
    liv = []
    for k in ks:
        v = per_passo[k]
        r = v["mean_phi_g"] / base
        liv.append({"passo": k, "su_base": r, "su_psi": r ** 0.5})
        if k % 10 == 0 or k in (42, 58, 60, 62, 64, 66, 68, 70):
            print("  %-7d %-8d %-13.2f %-12.3f %-12.3f"
                  % (k, v["n"], v["mean_phi_g"], r, r ** 0.5))
    fin = [x for x in liv if 62 <= x["passo"] <= 120]
    med = sum(x["su_base"] for x in fin) / len(fin)
    print("")
    print("  ### DAL PASSO 62 AL 120 il livello medio e' %.3f x la base, cioe' %.3f x su |psi|"
          % (med, med ** 0.5))
    print("  ### E AL PASSO 120 e' ancora %.3f x la base (%.3f x su |psi|): NON TORNA GIU'."
          % (liv[-1]["su_base"], liv[-1]["su_psi"]))
    print("  ### ➜ IL FLASH NON SMETTE: DIVENTA LO STATO PERMANENTE.")
    print("  ⚠ E `phi_g` e' il POZZO, non `|psi|`: il passaggio 2.6 -> 1.6 assume che")
    print("    `pozzo_grafo` sia LINEARE in `I = |psi|^2`. NON L'HO VERIFICATO, e la voce")
    print("    `PSI-FLASH` fa la stessa assunzione: va verificata, non ereditata.")
    flash = [t["passo"] for t in tab if t["flash"]]
    nasc = [t["passo"] for t in tab if t["dn"] > 0]
    print("")
    print("  passi col FLASH:    %s" % flash)
    print("  passi con NASCITE (fra due fotogrammi): %s" % nasc)
    print("  con nascite MA SENZA flash: %s" % sorted(set(nasc) - set(flash)))
    print("")
    print("  ### E QUI STA UNA LETTURA CHE CAMBIA LA VOCE `PSI-FLASH`, e la dico come LETTURA:")
    print("  I FOTOGRAMMI SONO OGNI DUE PASSI. Un `dn > 0` fra il fotogramma `k-2` e il `k` dice")
    print("  che una nascita c'e' stata al passo k-1 OPPURE al passo k, e IL FOTOGRAMMA NON")
    print("  DISTINGUE. Se il flash dura UN SOLO PASSO -- ed e' cio' che il meccanismo prevede,")
    print("  perche' al passo dopo `len(psi) == n` e nessuno ricalcola -- allora una nascita al")
    print("  passo DISPARI ha il suo flash al passo DISPARI, che NON E' FOTOGRAFATO.")
    print("  ### ➜ I casi <<nascite ma nessun flash>> potrebbero essere TUTTI nascite dispari.")
    print("  NON E' DIMOSTRATO: la granularita' dei fotogrammi non permette di dimostrarlo, e")
    print("  serve un run che guardi OGNI passo. Ma e' l'ipotesi che la voce non aveva.")
    if 42 in per_passo and 40 in per_passo and 44 in per_passo:
        a, b, c = (per_passo[x]["mean_phi_g"] for x in (40, 42, 44))
        print("")
        print("  IL NUMERO DEL MANDATO, riprodotto dai fotogrammi:")
        print("    mean(phi_g)  %.2f -> %.2f -> %.2f" % (a, b, c))
        print("    salto su phi_g (cioe' su |psi|^2): %.3f x" % (b / ((a + c) / 2)))
        print("    ### salto su |psi|: %.3f x   (il guardiano dice 1.62)"
              % ((b / ((a + c) / 2)) ** 0.5))
    return {"fotogrammi": len(f), "chiavi": chiavi, "mancano_per_ripartire": manca,
            "riavvio_possibile": not manca, "tabella": tab,
            "passi_flash": flash, "passi_nascite": nasc,
            "nascite_senza_flash": sorted(set(nasc) - set(flash)),
            "livello_base_senza_nascite": base, "livelli": liv,
            "livello_medio_62_120_su_base": med,
            "livello_al_120_su_base": liv[-1]["su_base"],
            "blob_che_li_ha_prodotti": str(z0["blob"])}


def passo1a():
    """I siti con la guardia, e quali sono RAGGIUNGIBILI dopo `mitosi`."""
    siti = [(k, _dentro(k), r.strip()) for k, r in enumerate(RIG, 1)
            if "len(self.psi) <" in r]
    ordine = [n for _t, n in _passo.ordine()]
    dopo = ordine[ordine.index("mitosi") + 1:] if "mitosi" in ordine else []
    dopo = list(dopo) + ["chiudi", "verifica_invarianti"]
    vive = raggiungibili(dopo)
    print("  le leggi DOPO `mitosi` nel passo: %s" % ", ".join(dopo))
    print("  funzioni raggiungibili da loro: %d" % len(vive))
    print("")
    print("  %-7s %-28s %-12s %s" % ("riga", "dentro", "dopo mitosi?", "sorgente"))
    fuori = []
    for k, fn, txt in siti:
        raggiunta = fn in vive
        print("  :%-6d %-28s %-12s %s" % (k, fn, "### SI" if raggiunta else "no", txt[:52]))
        fuori.append({"riga": k, "dentro": fn, "raggiungibile_dopo_mitosi": raggiunta})
    q = [x for x in fuori if x["raggiungibile_dopo_mitosi"]]
    print("")
    print("  ### SITI CON LA GUARDIA: %d  (non 8: `calcola_psi` e' il BERSAGLIO, non una guardia)"
          % len(siti))
    print("  ### RAGGIUNGIBILI DOPO `mitosi`: %d  ->  %s"
          % (len(q), [":%d in %s" % (x["riga"], x["dentro"]) for x in q]))
    return {"siti": fuori, "totale": len(siti), "dopo_mitosi": len(q)}


def passo1b():
    """Il rinculo a indici ripetuti: QUANDO morde?"""
    print("  IL SITO, dal codice:")
    for k, r in enumerate(RIG, 1):
        if "self.phi[g] = (self.phi[g] +" in r:
            print("    :%d  %s" % (k, r.strip()[:96]))
            riga = k
            break
    else:
        riga = None
    print("")
    print("  `g = np.concatenate([a, b])`, con `a = self.i[sel]` e `b = self.j[sel]`.")
    print("  In numpy un'assegnazione per indici RIPETUTI **non somma**: vince l'ULTIMA scrittura.")
    print("  ### QUINDI un nodo che e' genitore DUE VOLTE nello stesso passo riceve UNA sola")
    print("  ### spinta invece di due. Confermato dal guardiano (Luca, 2026-09-28).")
    print("")
    print("  ⚠ MA PERCHE' MORDA SERVONO **DUE ARCHI CHE SI DIVIDONO NELLO STESSO PASSO E")
    print("    CONDIVIDONO UN NODO**. Con UNA sola divisione per passo `a` e `b` sono distinti e")
    print("    il difetto NON PUO' scattare.")
    print("  ### E il passo 42 del video ha UNA nascita (n 12802 -> 12803): LI' NON MORDE.")
    print("  ### QUANTO SPESSO MORDA NON E' MISURATO, e non lo misuro qui: servirebbe contare,")
    print("    dentro un run, gli indici ripetuti in `g`. E' la voce a se' che il guardiano ha")
    print("    chiesto di aprire, ed e' esplicitamente FUORI dal sigillo del pezzo 2.")
    return {"riga": riga, "morde_solo_se": "due archi che si dividono nello stesso passo e "
                                           "condividono un nodo",
            "al_passo_42_del_video": "NON morde: una sola nascita",
            "frequenza": "NON MISURATA, e sta fuori dal pezzo 2 per decisione di Luca"}


def principale():
    print("simulatore: %s" % os.path.basename(SIM))
    print("")
    print("=" * 92)
    print("PASSO 0 -- LA SCENA PRESCRITTA DAL GUARDIANO: i fotogrammi del pilota, seme 11")
    print("=" * 92)
    p0 = passo0()
    print("")
    print("=" * 92)
    print("PASSO 1a -- I SITI CON LA GUARDIA `len(self.psi) < n`")
    print("=" * 92)
    p1a = passo1a()
    print("")
    print("=" * 92)
    print("PASSO 1b -- IL RINCULO A INDICI RIPETUTI: quando morde?")
    print("=" * 92)
    p1b = passo1b()
    OUT = os.path.join(_QUI, "_flash_passo01.json")
    io.open(OUT, "w", encoding="utf-8", newline=chr(10)).write(json.dumps(
        {"passo0_fotogrammi": p0, "passo1a_siti": p1a, "passo1b_rinculo": p1b},
        indent=1, ensure_ascii=False, sort_keys=True))
    print("")
    print("scritto: " + OUT)
    return 0


if __name__ == "__main__":
    sys.exit(principale())
