# -*- coding: utf-8 -*-
r"""**LA TABELLA DELLA NOTTE (F3 del mandato di Luca `2026-11-16` `20:35`)**: che cosa e' finito, che cosa e' sospeso, da quale k e da quale file si riprende, quanti tick mancano.

    E:\python\py3132\python.exe doc/referti_l2/notte_tabella.py > doc/referti_l2/notte_tabella.txt

**Legge SOLO le uscite delle corse copiate nel repo** *(`doc/referti_l2/notte_<nome>.txt`, `notte_<nome>_avvio.txt`; per V-T120 `notte_V-T120_fermata.txt`)*, **e RICALCOLA dal disco lo sha1 dell'ultimo stato** *(confrontato con quello che la corsa ha scritto e col file `.sha1` accanto)*.
**Accanto:** **R-SCATOLA al `5%` a ogni tappa** *(R_ogg)*, **il residuo di Gauss massimo contro la soglia** *(`10` volte il residuo a `k 0`)*, **la deriva relativa della massa** *(coppie: la massa totale; triangolo: la somma delle tre)*, **il tempo per tick.**
"""
import hashlib
import json
import os
import re
import sys

QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(os.path.dirname(QUI))
CORSE = (("V-B2", "notte_V-B2.txt"), ("V-B2pi", "notte_V-B2pi.txt"), ("V-T120", "notte_V-T120_fermata.txt"),
         ("F-66", "notte_F-66.txt"), ("A-66", "notte_A-66.txt"), ("F-51", "notte_F-51.txt"))
NON_PARTITE = ("A-51", "A-45", "F-35", "A-35")


def sha1(f):
    h = hashlib.sha1()
    with open(f, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def leggi(nome, file):
    t = open(os.path.join(QUI, file), encoding="utf-8").read()
    av = open(os.path.join(QUI, "notte_%s_avvio.txt" % nome), encoding="utf-8").read()
    fatto = json.loads(re.search(r"### L'AVVIO FATTO: (\{.*\})", av).group(1))
    fino = int(re.search(r"a k (\d+); lo stato ogni", t).group(1))
    m = re.search(r"### (\d+) tick in (\d+) s \(([\d.]+) s per tick\); (.*)", t)
    come = m.group(4)
    ult = re.search(r"### L'ULTIMO STATO: k (\d+), (\S+), sha1 ([0-9a-f]{40})", t)
    k, path, h = int(ult.group(1)), ult.group(2).rstrip(","), ult.group(3)
    rogg = [(int(a), float(b)) for a, b in re.findall(r"### R-SCATOLA AL 5% \(\S+ a k (\d+)\): R_ogg ([\d.]+)", t)]
    gauss = [float(g) for g in re.findall(r"  Gauss ([\d.e+-]+)  \(", t)]  # SOLO le righe dei tick: l'intestazione scrive anche "la soglia di Gauss" (l'errore della prima versione, 58d1045b)
    if fatto["tipo"] == "coppia":
        masse = [float(x) for x in re.findall(r"la massa ([\d.e+-]+)", t)]
    else:
        masse = [sum(float(y) for y in x) for x in re.findall(r"masse ([\d.e+-]+) ([\d.e+-]+) ([\d.e+-]+)", t)]
    return dict(nome=nome, fatto=fatto, fino=fino, tick=int(m.group(1)), s_tick=float(m.group(3)), come=come,
                k=k, path=path, sha=h, rogg=rogg, gauss=gauss, masse=masse)


def main():
    sys.path.insert(0, os.path.join(RADICE, "csv"))
    import _presidio
    _presidio.avvia(__file__)
    print("=" * 130)
    print("LA NOTTE 2026-11-16/17 (il mandato di Luca 20:35, F3): che cosa e' finito, che cosa e' sospeso, da dove si riprende")
    print("=" * 130)
    print("    %-7s %-9s %-5s %-7s %-6s %-7s %-10s %-60s %s" % ("corsa", "tipo", "L", "R_A", "fino", "k", "mancano", "l'ultimo stato (lo sha1 RICALCOLATO dal disco)", "lo stato"))
    righe = []
    for nome, file in CORSE:
        r = leggi(nome, file)
        righe.append(r)
        su_disco = sha1(r["path"]) if os.path.exists(r["path"]) else "MANCA"
        side = r["path"] + ".sha1"
        side_h = open(side).read().split()[0] if os.path.exists(side) else "MANCA"
        ok = (su_disco == r["sha"]) and side_h.startswith(r["sha"][:8])
        if "SOSPESA" in r["come"]:
            stato = "SOSPESA alle 08:00 (da riprendere)"
        elif "rifiuta la tappa" in r["come"]:
            stato = "FERMATA per decisione di Luca (00:20)"
        else:
            stato = r["come"]
        f = r["fatto"]
        print("    %-7s %-9s %-5d %-7.2f %-6d %-7d %-10d %-60s %s" % (nome, f["tipo"] + ("" if f["tipo"] != "coppia" else (" " + f["fase"])), f["L"], f["R_A"], r["fino"], r["k"], r["fino"] - r["k"],
                                                         "%s sha1 %s %s" % (os.path.basename(r["path"]), r["sha"][:8], "(disco e .sha1 CONCORDI)" if ok else "### DISCORDE: disco %s, .sha1 %s" % (su_disco[:8], side_h[:8])), stato))
    for n in NON_PARTITE:
        print("    %-7s %-9s %-5s %-7s %-6s %-7s %-10s %-60s %s" % (n, "coppia", "-", "-", "2000", "-", "2000", "-", "NON PARTITA (il posto di V-T120 e' andato a F-51; dalle 07:30 nessuna corsa nuova)"))
    print("-" * 130)
    print("### I CONTROLLI E R-SCATOLA AL 5% (R_ogg a ogni tappa; la regola: la distanza al lato >= 3 R_ogg, R_A >= 2 R_ogg)")
    for r in righe:
        f = r["fatto"]
        gm = max(r["gauss"])
        dm = (max(r["masse"]) - min(r["masse"])) / r["masse"][0]
        print("    %-7s %d tick in %.3f s per tick; Gauss massimo %.3e contro la soglia %.3e (%s); la massa: la deriva massima %.2e relativa (%d letture)" % (
            r["nome"], r["tick"], r["s_tick"], gm, f["soglia_gauss"], "sotto" if gm < f["soglia_gauss"] else "### SOPRA", dm, len(r["masse"])))
        print("            R_ogg al 5%%: k 0 %.1f; %s" % (f["R_ogg5_k0"], ", ".join("k %d %.1f" % kr for kr in r["rogg"])))
        print("            il massimo %.1f (%.2f volte quello di k 0); R_A / R_ogg al massimo %.2f" % (max(x for _, x in r["rogg"]), max(x for _, x in r["rogg"]) / f["R_ogg5_k0"], f["R_A"] / max(x for _, x in r["rogg"])))
    print("=" * 130)
    return 0


if __name__ == "__main__":
    sys.exit(main())
