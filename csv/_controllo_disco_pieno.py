# -*- coding: utf-8 -*-
r"""**I CONTROLLI DOPO IL DISCO PIENO** *(il mandato di Luca delle `13:40` del `2026-10-30`; il task history `doc/TASK_HISTORY/2026-10-30_livelli_piatti.md`, sezione `5-bis`)*:
### **ogni file della prova dei livelli piatti scritto dalle `11:19` in poi si apre, ha la forma attesa, e lo sha1 coincide con quello registrato dove esiste;**
### **la corsa lunga di `R_1e6` si rifa' IN MEMORIA dai tick `1` a `4000` e si confronta AL BIT col pezzo `00000` committato (`6c385aa2`, il controllo positivo) e col pezzo `02000` sul disco;**
### **NON SCRIVE NIENTE su disco** *(solo `stdout`)*.

    python csv/_controllo_disco_pieno.py > doc/referti_l2/livelli_piatti/controllo_disco_pieno.txt
"""
import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
import time

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
_PO = os.path.join(RADICE, "primo_ordine")
for _p in (_QUI, _PO, os.path.join(_PO, "leggi")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import numpy as np                                             # noqa: E402

import _livelli_piatti as LP                                   # noqa: E402

REL = "doc/referti_l2/livelli_piatti/"
COMMIT_POSITIVO = "6c385aa2"   # ### il pezzo 00000, committato prima del disco pieno
COMMITTATI = (REL + "lunga_R_1e6_00000.jsonl", REL + "breve_R_3e6.json", REL + "breve_R_3e6.txt", REL + "cerca_X1.json", REL + "cerca_R_3e6.json", REL + "cerca_R_1e6.json")
STATI = ("R_1e6", "R_3e6", "X1", "R_3e5", "X2")
BREVI = ("R_1e6", "R_3e6", "X1")
TXT_SCRATCH = ("breve_X1", "cerca_R_3e5", "cerca_X2")
DA_FARE = {"pezzi": 8, "brevi": 2, "stati": 2}   # ### quel che manca al mandato delle 09:31: i pezzi 04000..18000, le brevi R_3e5 e X2, gli stati R_3e6 e X1 rifatti


def sha1(dati):
    return hashlib.sha1(dati).hexdigest()


def blob(commit, path):
    return subprocess.check_output(["git", "cat-file", "-p", "%s:%s" % (commit, path)], cwd=RADICE)


def disco(path):
    with open(os.path.join(RADICE, path), "rb") as fh:
        return fh.read()


def json_pieno(path):
    dati = disco(path)
    return dati, json.loads(dati.decode("utf-8")), dati.endswith(b"\n")


def file_committati():
    print("\n(a1) I FILE COMMITTATI: lo sha1 dei byte sul disco = il blob a HEAD")
    for p in COMMITTATI:
        d, h = disco(p), blob("HEAD", p)
        if p.endswith(".txt"):
            # ### la trappola CRLF (CLAUDE.md par.7): l'output di python su Windows ha CRLF, il blob LF: stesso CONTENUTO, byte diversi
            dl = d.replace(b"\r\n", b"\n")
            LP.esito("%s: %d byte, sha1 %s; senza i CR %d byte, sha1 %s" % (p, len(d), sha1(d)[:8], len(dl), sha1(dl)[:8]), dl == h,
                     "HEAD %s; %s" % (sha1(h)[:8], "byte uguali" if d == h else "byte diversi solo per i CR"))
            continue
        LP.esito("%s: %d byte, sha1 %s" % (p, len(d), sha1(d)[:8]), sha1(d) == sha1(h), "HEAD %s" % sha1(h)[:8])


def stati():
    import _stato_fermo as SFM
    print("\n(a2) GLI STATI: l'.npz si apre, sha(psi) = il campo sha del cerca_*.json")
    for nome in STATI:
        fn = os.path.join(LP.DIR_NPZ, "fermo_%s.npz" % nome)
        try:
            with np.load(fn) as fe:
                psi, mu = fe["psi_h"].copy(), float(fe["mu"])
            _d, cj, nl = json_pieno(REL + "cerca_%s.json" % nome)
        except Exception as e:                                   # noqa: BLE001
            LP.esito("%s: si apre" % nome, False, repr(e)[:120])
            continue
        LP.esito("%s: %d byte, psi %s %s, sha %s; il json chiuso da a-capo, mu %+.9f" % (nome, os.path.getsize(fn), psi.shape, psi.dtype, SFM.sha(psi)[:8], cj["mu"]),
                 SFM.sha(psi) == cj["sha"] and mu == cj["mu"] and nl and bool(np.all(np.isfinite(psi))), "json %s, residuo %.3e" % (cj["sha"][:8], cj["residuo_finale"]))


def brevi():
    print("\n(a3) LE CORSE BREVI: il json si legge, ha le chiavi di una committata (R_1e6 se la forma si giudica, R_3e6 se no), il suo sha = quello dello stato")
    chiavi = [set(json.loads(blob("HEAD", REL + "breve_%s.json" % n).decode("utf-8"))) for n in ("R_1e6", "R_3e6")]
    for nome in BREVI:
        p = REL + "breve_%s.json" % nome
        d, b, nl = json_pieno(p)
        cj = json.loads(disco(REL + "cerca_%s.json" % nome).decode("utf-8"))
        n = int(round(LP.T_BREVE / LP.S))
        LP.esito("%s: %d byte, sha1 %s, %d chiavi, %d campioni ogni 5 tick" % (p, len(d), sha1(d)[:8], len(b), len(b["t5"])),
                 set(b) in chiavi and b["sha"] == cj["sha"] and nl and len(b["t5"]) == n // LP.OGNI_D and b["t5"][-1] == n, "")


def testi():
    print("\n(a4) I .txt: la copia nel repo = l'output nello scratchpad, al byte")
    sp = os.environ.get("SCRATCH_LP")
    for nome in TXT_SCRATCH:
        s = open(os.path.join(sp, "%s.txt" % nome), "rb").read()
        p = os.path.join(RADICE, REL + "%s.txt" % nome)
        if os.path.exists(p):
            d = open(p, "rb").read()
            LP.esito("%s.txt: %d byte, sha1 %s" % (nome, len(d), sha1(d)[:8]), d == s, "scratchpad %s" % sha1(s)[:8])
        else:
            ultima = s.decode("utf-8").rstrip("\n").split("\n")[-1].strip()
            LP.esito("%s.txt solo nello scratchpad: %d byte, sha1 %s; l'ultima riga" % (nome, len(s), sha1(s)[:8]), "residuo finale" in ultima, ultima[:100])


def lunga():
    import _congelato_lungo as CL
    import _deriva_congelato as DC
    import _dove_va_la_materia as DV
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _stato_fermo as SFM
    import _triangoli_bassa_energia as BE
    print("\n(b) LA CORSA LUNGA DI R_1e6 RIFATTA IN MEMORIA, tick 1 -> 4000")
    nome = "R_1e6"
    p00 = json.loads(blob(COMMIT_POSITIVO, REL + "lunga_R_1e6_00000.jsonl").decode("utf-8"))
    d02, p02, nl02 = json_pieno(REL + "lunga_R_1e6_02000.jsonl")
    with np.load(os.path.join(LP.DIR_NPZ, "lunga_%s.npz" % nome)) as dati:
        t_rip, sha_rip = int(dati["t"]), SFM.sha(dati["psi_h"])
    r, g, N = LP.CONFIG[nome]
    psi0, mu, _cj = LP.stato(nome)
    righe = {}
    s0 = time.time()
    with LP.scena(N) as (rec, z, phi0, _p), LP.configurazione(r, g):
        w0 = rec["larghezza"]
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            w_in = DC.forma(z, w0)[0]
        Z = DV.autovettori(DV.matrice(z, phi0, DV.AMP))[1]
        bande = LP.ML.Bande(Z, z["L"])
        n0 = float(np.linalg.norm(psi0))
        z["st"]["psi_h"][...] = psi0
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            p = CL.punto(z, 0, w_in, w0)
        p["tau"] = 0.0
        for t0 in (0, LP.PEZZO):
            punti, dd = ([p] if t0 == 0 else []), []
            with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
                for t in range(t0 + 1, t0 + LP.PEZZO + 1):
                    CL.avanza(z, phi0, 1)
                    if t % LP.OGNI == 0:
                        q = CL.punto(z, t, w_in, w0)
                        q["tau"] = t * LP.S
                        punti.append(q)
                    if t % LP.OGNI_LUNGA_D == 0:
                        D = np.exp(1j * mu * LP.S * t) * z["st"]["psi_h"] - psi0
                        c = bande.coeff(D)
                        pk = np.abs(c) ** 2
                        tot = float(pk.sum())
                        dd.append({"t": t, "nD": float(np.linalg.norm(D)) / n0, "bande": {gn: float(pk[..., list(idx)].sum()) / tot for gn, idx in bande.gruppi.items()}})
            righe[t0] = json.loads(json.dumps({"punti": punti, "D": dd, "sha_fine": SFM.sha(z["st"]["psi_h"]), "w0": w0, "w_in": w_in}, sort_keys=True))
    print("  %d tick in %.0f s" % (2 * LP.PEZZO, time.time() - s0))
    for t0, rif, chi in ((0, p00, "il pezzo 00000 committato in %s (IL CONTROLLO POSITIVO)" % COMMIT_POSITIVO), (LP.PEZZO, p02, "il pezzo 02000 sul disco (%d byte, sha1 %s)" % (len(d02), sha1(d02)[:8]))):
        ri = righe[t0]
        for k in ("sha_fine", "w0", "w_in", "punti", "D"):
            LP.esito("%s: %s uguale AL BIT" % (chi, k), ri[k] == rif[k], ("%s" % ri[k])[:16] if k == "sha_fine" else "%d voci" % len(ri[k]) if isinstance(ri[k], list) else "")
        LP.esito("%s: t0 %d, t1 %d" % (chi, rif["t0"], rif["t1"]), rif["t0"] == t0 and rif["t1"] == t0 + LP.PEZZO, "")
    LP.esito("il pezzo 02000: chiuso da a-capo", nl02, "")
    LP.esito("lo stato di ripresa lunga_R_1e6.npz: t %d, sha %s = la fine rifatta in memoria" % (t_rip, sha_rip[:8]), t_rip == 2 * LP.PEZZO and sha_rip == righe[LP.PEZZO]["sha_fine"], "")
    return len(d02)


def spazio(byte_pezzo):
    print("\n(c) LO SPAZIO")
    libero = shutil.disk_usage(RADICE).free
    breve = max(os.path.getsize(os.path.join(RADICE, REL + "breve_%s.json" % n)) for n in BREVI)
    npz = os.path.getsize(os.path.join(LP.DIR_NPZ, "fermo_R_1e6.npz"))
    # ### ogni file conta DUE volte: sul disco e nell'oggetto di git (senza compressione, per eccesso); lo stato ne conta un altro per il _tmp
    serve = 2 * (DA_FARE["pezzi"] * byte_pezzo + DA_FARE["brevi"] * 2 * breve) + DA_FARE["stati"] * 2 * npz + 2 * npz
    print("  serve (per eccesso): %d pezzi da %d byte, %d brevi da %d byte (json + txt), %d stati da %d byte: %.2f MB" % (DA_FARE["pezzi"], byte_pezzo, DA_FARE["brevi"], breve, DA_FARE["stati"], npz, serve / 1e6))
    LP.esito("lo spazio libero su C basta: %.2f GB liberi" % (libero / 1e9), libero > serve, "il rapporto %.0f" % (libero / serve))


def main():
    import _presidio
    _presidio.avvia(__file__)
    import _deriva_congelato as DC
    import _solitone_vuoto_congelato as VC
    vero = (VC.FORMA, VC.S, DC.N)
    try:
        file_committati()
        stati()
        brevi()
        testi()
        b = lunga()
        spazio(b)
    finally:
        VC.FORMA, VC.S, DC.N = vero
    print("\n%d/%d PASSANO" % tuple(LP.OK))
    for f in LP.FALLITE:
        print("  ### FALLISCE: %s" % f)
    return 0 if LP.OK[0] == LP.OK[1] else 1


if __name__ == "__main__":
    sys.exit(main())
