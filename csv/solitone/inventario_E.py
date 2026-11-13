# -*- coding: utf-8 -*-
r"""**L'INVENTARIO DEI DATI DEL REPO SU E:** *(Luca `2026-11-13` `15:35`; SOLO LETTURA; il task history `doc/TASK_HISTORY/2026-11-13_inventario_E.md`)*.

    python csv/solitone/inventario_E.py > doc/referti_l2/inventario_E.txt

**1.** il volume E: *(`Get-Volume`: il file system, la dimensione, lo spazio libero; nient'altro del disco)*. **2.** le cartelle di E: che il CODICE apre *(i percorsi `E:` nelle stringhe di `csv/` e
`primo_ordine/`)*: per cartella *(fino al secondo livello, col totale ricorsivo)* la dimensione e il numero di file; i file oltre `50` e oltre `100` MB. **3.** gli stati di PARTENZA delle prove
*(`PARTENZE`, dagli script, dichiarati)*: il percorso, la dimensione, lo sha1 dei byte *(cercato nei referti)*, gli sha per chiave contro il jsonl; e tutti gli stati registrati delle corse, dove
stanno e quanto pesano. **4.** la proposta *(stampata, NON eseguita)*. ### **Nessuna scrittura: `os.walk`, `os.stat`, la lettura dei byte.**
"""
import hashlib
import json
import os
import re
import subprocess
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
_CSV = os.path.dirname(_QUI)
for _p in (_QUI, _CSV):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import solitone  # noqa: E402,F401  (i percorsi)

RADICE = os.path.dirname(_CSV)
MB = 1e6
SOGLIE_MB = (50.0, 100.0)            # ### i limiti di GitHub (Luca 15:35): 50 MB un avviso, 100 MB un rifiuto
PARTENZE = (("C35-pi", 60000, "G2, P6 (s5_coppia_lapse, p6_u_breve, p6_bracci)"),
            ("TBS", 10000, "le G1, il video triplo (s5_caduta_solitone, s5_g1_lunga, s5_g1_tre_partenze)"),
            ("TM1000", 13333, "carta_d0, test_simmetrica"),
            ("S162", 10000, "carta_coppia"))
FONTI_CODICE = ("csv", "primo_ordine")
RE_E = re.compile(r"""[rbuRBU]?["']((?:E|e):[\\/][^"']*)["']""")


def percorsi_E_nel_codice():
    """### **Le cartelle di E: nominate nel codice** *(le stringhe `E:\\...` o `E:/...`)*: `{la cartella di primo livello: [i file che la nominano]}`."""
    trovate = {}
    for fonte in FONTI_CODICE:
        for d, _sub, files in os.walk(os.path.join(RADICE, fonte)):
            if "__pycache__" in d:
                continue
            for f in files:
                if not f.endswith((".py", ".yaml", ".json")):
                    continue
                p = os.path.join(d, f)
                try:
                    testo = open(p, encoding="utf-8", errors="replace").read()
                except OSError:
                    continue
                for m in RE_E.finditer(testo):
                    parti = re.split(r"[\\/]+", m.group(1))
                    if len(parti) >= 2 and parti[1]:
                        cima = "E:\\" + parti[1]
                        trovate.setdefault(cima, set()).add(os.path.relpath(p, RADICE).replace("\\", "/"))
    return {k: sorted(v) for k, v in sorted(trovate.items())}


def volume():
    cmd = ["powershell", "-NoProfile", "-Command", "Get-Volume -DriveLetter E | Select-Object FileSystemType, Size, SizeRemaining | ConvertTo-Json"]
    try:
        return json.loads(subprocess.check_output(cmd).decode("utf-8", "replace"))
    except (subprocess.CalledProcessError, OSError, ValueError) as x:
        return {"errore": str(x)}


def cammina(cima):
    """### `(per_cartella {percorso: [byte, file]} ricorsivo, i file grandi [(percorso, byte)])`."""
    tot, grandi = {}, []
    for d, _sub, files in os.walk(cima):
        b, n = 0, 0
        for f in files:
            p = os.path.join(d, f)
            try:
                s = os.stat(p).st_size
            except OSError:
                continue
            b += s
            n += 1
            if s > SOGLIE_MB[0] * MB:
                grandi.append((p, s))
        x = d
        while True:
            tot.setdefault(x, [0, 0])
            tot[x][0] += b
            tot[x][1] += n
            if os.path.normcase(x) == os.path.normcase(cima):
                break
            x = os.path.dirname(x)
    return tot, sorted(grandi, key=lambda z: -z[1])


def sha1_file(p):
    h = hashlib.sha1()
    with open(p, "rb") as f:
        for blocco in iter(lambda: f.read(1 << 22), b""):
            h.update(blocco)
    return h.hexdigest()


def testi_referti():
    out = []
    for d, _sub, files in os.walk(os.path.join(RADICE, "doc")):
        for f in files:
            if f.endswith((".txt", ".md", ".json", ".jsonl", ".tsv")):
                try:
                    out.append((os.path.relpath(os.path.join(d, f), RADICE), open(os.path.join(d, f), encoding="utf-8", errors="replace").read()))
                except OSError:
                    pass
    return out


def main():
    import numpy as np
    import _presidio
    import _stato_fermo as SFM
    from solitone import corsa_accensione as CA
    _presidio.avvia(__file__)
    print("=" * 130)
    print("L'INVENTARIO DEI DATI DEL REPO SU E: (Luca 2026-11-13 15:35; SOLO LETTURA)")
    print("=" * 130)
    # ---------------------------------------------------------------- 1. il volume
    v = volume()
    if "errore" in v:
        print("### 1. IL VOLUME E: Get-Volume NON risponde: %s" % v["errore"])
    else:
        print("### 1. IL VOLUME E: il file system %s; la dimensione %.1f GB; lo spazio libero %.1f GB" % (v.get("FileSystemType"), v["Size"] / 1e9, v["SizeRemaining"] / 1e9))
    # ---------------------------------------------------------------- 2. le cartelle
    cime = percorsi_E_nel_codice()
    print("-" * 130)
    print("### 2. LE CARTELLE DI E: NOMINATE NEL CODICE (le stringhe E:\\... in %s): %d" % (", ".join(FONTI_CODICE), len(cime)))
    for c, ff in cime.items():
        print("    %-30s esiste %-5s  nominata da %d file: %s" % (c, os.path.isdir(c), len(ff), ", ".join(ff[:6]) + (" ..." if len(ff) > 6 else "")))
    totali, tutti_grandi = {}, []
    for c in cime:
        if not os.path.isdir(c):
            continue
        tot, grandi = cammina(c)
        totali[c] = tot[c]
        tutti_grandi += grandi
        print("  %s: %.3f GB in %d file" % (c, tot[c][0] / 1e9, tot[c][1]))
        livello = {k: w for k, w in tot.items() if 0 < os.path.relpath(k, c).count(os.sep) + 1 <= 2 and k != c}
        for k in sorted(livello):
            print("    %-70s %10.1f MB %8d file" % (os.path.relpath(k, c), livello[k][0] / MB, livello[k][1]))
    print("  I FILE OLTRE %g MB: %d (oltre %g MB: %d), %.3f GB in tutto" % (SOGLIE_MB[0], len(tutti_grandi), SOGLIE_MB[1], sum(1 for _p, s in tutti_grandi if s > SOGLIE_MB[1] * MB),
                                                                            sum(s for _p, s in tutti_grandi) / 1e9))
    for p, s in tutti_grandi:
        print("    %s %9.1f MB  %s" % ("###" if s > SOGLIE_MB[1] * MB else "   ", s / MB, p))
    # ---------------------------------------------------------------- 3. gli stati
    print("-" * 130)
    print("### 3. GLI STATI DELLE CORSE (gli `stati` dei jsonl di corsa_accensione)")
    tutti, per_disco = [], {}
    for nome in sorted(CA.CORSE):
        try:
            rr = CA.serie(nome)[0]
        except Exception as x:          # noqa: BLE001  (una corsa senza jsonl: si dice, non si ferma)
            print("    %-10s il jsonl non si legge: %s" % (nome, x))
            continue
        for r in rr:
            for xs in (r.get("stati") or []):
                p = xs["file"]
                s = os.stat(p).st_size if os.path.exists(p) else None
                tutti.append((nome, xs["t"], p, s, xs.get("sha")))
                disco = os.path.splitdrive(os.path.abspath(p))[0].upper()
                per_disco.setdefault(disco, [0, 0, 0])
                per_disco[disco][0] += 1
                per_disco[disco][1] += s or 0
                per_disco[disco][2] += 0 if s is not None else 1
    print("    %d stati registrati; per disco: %s" % (len(tutti), "; ".join("%s %d stati, %.3f GB, %d MANCANTI" % (k, w[0], w[1] / 1e9, w[2]) for k, w in sorted(per_disco.items()))))
    cartelle = {}
    for _n, _t, p, s, _sh in tutti:
        cartelle.setdefault(os.path.dirname(p), [0, 0])
        cartelle[os.path.dirname(p)][0] += 1
        cartelle[os.path.dirname(p)][1] += s or 0
    for k in sorted(cartelle):
        print("    %-80s %5d stati %10.1f MB%s" % (k, cartelle[k][0], cartelle[k][1] / MB, "   ### IGNORATA da git, sul disco del repo" if os.path.normcase(k).startswith(os.path.normcase(RADICE)) else ""))
    print("  GLI STATI DI PARTENZA DELLE PROVE (dichiarati in PARTENZE, dagli script):")
    referti = testi_referti()
    problemi = []
    for nome, t, chi in PARTENZE:
        xx = [z for z in tutti if z[0] == nome and z[1] == t]
        if len(xx) != 1:
            print("    %-8s a %6d (%s): %d stati nel jsonl -- NON si controlla" % (nome, t, chi, len(xx)))
            problemi.append("%s a %d: %d stati nel jsonl" % (nome, t, len(xx)))
            continue
        _n, _t, p, s, sh = xx[0]
        if s is None:
            print("    %-8s a %6d: %s ### MANCA" % (nome, t, p))
            problemi.append("%s a %d: il file manca" % (nome, t))
            continue
        h = sha1_file(p)
        citato = sorted({f for f, testo in referti if h[:12] in testo})
        with np.load(p) as d:
            chiavi = sorted(sh) if sh else []
            diverse = [k for k in chiavi if k not in d.files or SFM.sha(d[k]) != sh[k]]
        print("    %-8s a %6d (%s)" % (nome, t, chi))
        print("        %s  %.1f MB  sha1-BYTE %s" % (p, s / MB, h))
        print("        lo sha1 dei byte nei referti (i primi 12 caratteri): %s" % (", ".join(citato) if citato else "NON citato"))
        print("        gli sha per chiave contro il jsonl: %d chiavi, %s" % (len(chiavi), "TUTTE uguali" if not diverse and chiavi else "### DIVERSE: %s" % diverse if diverse else "### il jsonl non ha sha"))
        if diverse or not chiavi:
            problemi.append("%s a %d: gli sha per chiave %s" % (nome, t, diverse or "assenti"))
    # ---------------------------------------------------------------- 4. la proposta
    print("-" * 130)
    tot_E = sum(w[0] for w in totali.values())
    part = [z for z in tutti if any(z[0] == n and z[1] == t for n, t, _c in PARTENZE) and z[3]]
    b_part = sum(z[3] for z in part)
    b_stati = sum(z[3] or 0 for z in tutti)
    sotto50 = [z for z in part if z[3] <= SOGLIE_MB[0] * MB]
    print("### 4. LA PROPOSTA (NON eseguita: la decisione e' di Luca)")
    print("  (a) NEL REPO: gli stati di PARTENZA delle prove (%d file, %.1f MB; %d sotto %g MB, %d sopra):" % (len(part), b_part / MB, len(sotto50), SOGLIE_MB[0], len(part) - len(sotto50)))
    print("      - sotto %g MB DIRETTI nel repo (git li tiene in ogni clone, per sempre: %.1f MB);" % (SOGLIE_MB[0], sum(z[3] for z in sotto50) / MB))
    print("      - sopra %g MB con Git LFS (%.1f MB; il piano gratuito di GitHub ha una quota di spazio e di banda per LFS: da verificare prima)." % (SOGLIE_MB[0], (b_part - sum(z[3] for z in sotto50)) / MB))
    print("      Il dato di una prova si rifa' dal suo comando SOLO se esiste lo stato di partenza: sono questi i file senza i quali i referti non si rigirano.")
    print("  (b) FUORI DAL REPO, una COPIA INTERA di E:\\soliton_simulator e di E:\\soliton_archivio (%.3f GB) su un secondo disco o un servizio esterno; e gli stati sul disco del repo IGNORATI da git (%s)."
          % (tot_E / 1e9, ", ".join("%s %.3f GB" % (k, w[1] / 1e9) for k, w in sorted(per_disco.items()) if os.path.splitdrive(RADICE)[0].upper() == k) or "nessuno"))
    print("  (c) LO SPAZIO: (a) %.1f MB nel repo o in LFS; (b) %.3f GB per la copia di E: (+ gli stati sul disco del repo); tutti gli stati registrati delle corse insieme %.3f GB." % (b_part / MB, tot_E / 1e9, b_stati / 1e9))
    print("=" * 130)
    print("ESITO: %s" % ("NESSUN problema negli stati di partenza" if not problemi else "### PROBLEMI: %s" % problemi))
    return 0 if not problemi else 1


if __name__ == "__main__":
    sys.exit(main())
