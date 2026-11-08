# -*- coding: utf-8 -*-
r"""**I3: L'INVENTARIO DEGLI STATI GIA' ESISTENTI, IN SOLA LETTURA** *(il task history `doc/TASK_HISTORY/2026-11-07_stato_completo.md`, sez. `2` e `5.2`)*.

    python csv/solitone/inventario_stati.py > doc/referti_l2/inventario_stati.txt

### **Per ogni corsa di `corsa_accensione.CORSE` coi suoi jsonl:** **gli stati completi su `E:`** *(`stati[]` delle righe: il file, il tick, lo `sha` per chiave)* **e il file di
ripresa** *(`db/accensione_lenta/<nome>.npz`, contro `sha_fine` dell'ultima riga)*: **il tick, `t`, il bordo si'/no, il vuoto, la dimensione, e lo `sha` di OGNI chiave riletto dal
disco contro quello registrato.** ### **I file di stato su `E:` che nessuna riga registra si elencano** *(una corsa in volo li ha scritti dopo l'ultima riga)*. **`I3-F`** *(DEVE
FALLIRE)*: uno stato confrontato con lo `sha` di un altro tick. **Nessun file si scrive.**
"""
import glob
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))
import solitone  # noqa: E402,F401  (i percorsi)

OK = [0, 0]
FALLITE = []


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    if not passa:
        FALLITE.append(che)
    print("  %-118s %s   %s" % (che[:118], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return passa


def shas_file(f, chiavi=None):
    """`(t, {chiave: sha})` di un `.npz` di stato *(lo `sha` di `_stato_fermo`: i byte)*."""
    import _stato_fermo as SFM
    with np.load(f) as d:
        ks = sorted(k for k in d.files if k != "t") if chiavi is None else chiavi
        return int(d["t"]), {k: SFM.sha(d[k]) for k in ks if k in d.files}


def main():
    import _presidio
    import _vuoto_vivo_B as V
    from solitone import corsa_accensione as CA
    _presidio.avvia(os.path.join(_QUI, "corsa_accensione.py"))
    _presidio.avvia(__file__)
    _sol, _v, s = V.CORSE[CA.NOME]
    print("=" * 130)
    print("I3, L'INVENTARIO DEGLI STATI (sola lettura): le corse di corsa_accensione.CORSE coi loro jsonl; gli stati su E: e i file di ripresa in %s" % CA.DIR_NPZ)
    print("=" * 130)
    print("  %-8s %-9s %9s %9s %-6s %-5s %10s  %s" % ("corsa", "che", "tick", "t", "bordo", "vuoto", "byte", "lo sha di ogni chiave contro il registrato"))
    tutti, ok_tutti, uno = 0, 0, None
    # ### ⛔ LE CORSE IN VOLO: il loro file di ripresa NON si apre (su Windows un file aperto fa fallire l'os.replace della corsa a fine pezzo)
    import psutil
    volo = set()
    for p_ in psutil.process_iter(["cmdline"]):
        c_ = p_.info["cmdline"] or []
        if "--corsa" in c_ and c_.index("--corsa") + 1 < len(c_) and any("corsa_accensione" in x for x in c_):
            volo.add(c_[c_.index("--corsa") + 1])
        for i_, x_ in enumerate(c_):
            if x_.endswith("driver_corsa.sh") and i_ + 1 < len(c_):
                volo.add(c_[i_ + 1])   # ### il driver dei pezzi: fra due pezzi il python non c'e', il driver si'
    print("  le corse IN VOLO (dai processi): %s -- il loro file di ripresa non si apre" % (sorted(volo) or "nessuna"))
    non_reg = []
    for nome in sorted(CA.CORSE):
        ff = CA.nomi(nome)
        if not ff:
            continue
        rr = [V.LP.leggi(os.path.join(CA.dir_json(nome), n)) for n in ff]
        bordo = "si" if nome in CA.BORDO else "no"
        vuoto = CA.VUOTI.get(nome, "F0")
        reg = [x for r in rr for x in (r.get("stati") or [])]
        for x in reg:
            if not os.path.exists(x["file"]):
                print("  %-8s %-9s %9d %9.1f %-6s %-5s %10s  ### IL FILE NON C'E': %s" % (nome, "stato", x["t"], x["t"] * s, bordo, vuoto, "-", x["file"]))
                tutti += 1
                continue
            t_, sh = shas_file(x["file"], sorted(x["sha"]))
            buono = t_ == x["t"] and sh == x["sha"]
            tutti += 1
            ok_tutti += int(buono)
            if uno is None and buono:
                uno = (nome, x)
            print("  %-8s %-9s %9d %9.1f %-6s %-5s %10d  %s" % (nome, "stato", x["t"], x["t"] * s, bordo, vuoto, os.path.getsize(x["file"]), "al bit (%d chiavi)" % len(sh) if buono else "### NON TORNA"))
        noti = {os.path.normcase(os.path.abspath(x["file"])) for x in reg}
        for f in sorted(glob.glob(os.path.join(CA.base_e(nome), "stati", nome, "%s_stato_*.npz" % nome))):
            if os.path.normcase(os.path.abspath(f)) not in noti:
                non_reg.append((nome, f))
        f_rip = os.path.join(CA.DIR_NPZ, nome + ".npz")
        if nome in volo:
            print("  %-8s %-9s %9s %9s %-6s %-5s %10s  ### NON APERTO: la corsa e' IN VOLO (l'ultima riga t1 %d)" % (nome, "ripresa", "-", "-", bordo, vuoto, "-", rr[-1]["t1"]))
        elif os.path.exists(f_rip):
            ult = rr[-1]
            t_, sh = shas_file(f_rip)
            buono = t_ == ult["t1"] and sh == ult["sha_fine"]
            tutti += 1
            ok_tutti += int(buono)
            fin = ult["t1"] >= ult["t_fine"] or ult.get("fermata") or (ult.get("t_dis") is not None and ult["t_dis"] <= ult["K"])
            print("  %-8s %-9s %9d %9.1f %-6s %-5s %10d  %s%s" % (nome, "ripresa", t_, t_ * s, bordo, vuoto, os.path.getsize(f_rip), "al bit (%d chiavi)" % len(sh) if buono else "### NON TORNA (t %d contro t1 %d)" % (t_, ult["t1"]),
                                                              "" if fin else "  -- la corsa NON e' finita (t1 %d, t_fine %d): in volo o da riprendere" % (ult["t1"], ult["t_fine"])))
    print("  ### i file di stato su E: che nessuna riga registra (%d): %s" % (len(non_reg), "; ".join("%s %s" % (n, os.path.basename(f)) for n, f in non_reg) if non_reg else "nessuno"))
    esito("DEVE PASSARE: I3 ogni stato e ogni file di ripresa riletto dal disco ha lo sha di ogni chiave = il registrato (%d file)" % tutti, ok_tutti == tutti and tutti > 0, "%d su %d" % (ok_tutti, tutti))
    if uno is not None:
        nome, x = uno
        altri = [y for r in CA.serie(nome)[0] for y in (r.get("stati") or []) if y["t"] != x["t"]]
        _t, sh = shas_file(x["file"], sorted(x["sha"]))
        esito("DEVE FALLIRE: I3-F lo stato di %s a %d confrontato con lo sha registrato a %d" % (nome, x["t"], altri[0]["t"]), not sh == altri[0]["sha"], "")
    print("=" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main())
