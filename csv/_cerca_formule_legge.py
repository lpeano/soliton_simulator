# -*- coding: utf-8 -*-
r"""**LA RICERCA PER FORMULE, NON PER NOMI** *(il mandato di Luca «`S1` nel nucleo, la chiusura»; il task history `doc/TASK_HISTORY/2026-11-01_s1_nucleo_chiusura.md`, passo `2`)*.

### **Perche' esiste:** il criterio `K4` di `3fe2f12d` cercava i NOMI delle forme, e non ha visto `rho*log(rho/(rho+lam))` scritta a mano in `energia_pesata.py`.
### **Che cosa fa:** in `primo_ordine/` e `csv/solitone/` *(esclusi `materia_vuoto.py` e i moduli generati `termini/`)* cerca le formule della legge nel CODICE
*(commenti e stringhe a parte, col modulo `tokenize`)*. **Ogni occorrenza nel codice ha un giudizio scritto qui** *(per file e testo della riga)*; una senza giudizio **fa fallire**.
**Il criterio:** zero `legge a mano`. **Il caso che deve fallire:** una riga sintetica con la formula di `S3`, in un file finto, si trova e si giudica `legge a mano`.

    python csv/_cerca_formule_legge.py
"""
import io
import os
import re
import sys
import tokenize

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)

DOVE = ("primo_ordine", os.path.join("csv", "solitone"))
ESCLUSI = ("primo_ordine/materia_vuoto.py",)
ESCLUSE_CARTELLE = ("primo_ordine/termini/",)
# ### i pattern del mandato *(`log(rho`, `log(r/`, `atan`, `arctan`, `x^2/(1+x^2)`)*, piu' `log(x/` e `rho + lam` *(le copie di `S3` scritte in `x` o in `rho`)*
PATTERN = (("log(rho", re.compile(r"log\s*\(\s*rho")),
           ("log(r/", re.compile(r"log\s*\(\s*r\s*/")),
           ("log(x/", re.compile(r"log\s*\(\s*x\s*/")),
           ("atan/arctan", re.compile(r"arctan|atan")),   # ### `arctan` NON contiene `atan` (a-r-c-t-a-n): servono tutti e due
           ("x^2/(1+x^2)", re.compile(r"x\s*\*\*\s*2\s*/\s*\(\s*1(\.0)?\s*\+\s*x\s*\*\*\s*2|1(\.0)?\s*\+\s*x\s*\*\s*x")),
           ("rho + lam", re.compile(r"rho\w*\s*(\[[^\]]*\])?\s*\+\s*lam")))
CATEGORIE = ("legge a mano", "screening dichiarato", "oracolo di collaudo", "modulo di un'altra legge", "non e' la legge")
# ### I GIUDIZI: (file, riga di codice senza spazi) -> (categoria, il perche'). ### Una riga che sparisce col giudizio `legge a mano` e' una correzione
# ### (si riporta); una che sparisce con un altro giudizio e' un giudizio ORFANO, e fa fallire.
GIUDIZI = {
    ('primo_ordine/_collauda_forme.py',
     'np.array_equal(MV.alpha_s1(rho,lam)[1:],x**2/(1.0+x**2))andnp.array_equal(MV.beta_s1(rho,lam)[1:],x-np.arctan(x)-x**3/(1.0+x**2))'):
        ('oracolo di collaudo', "l'oracolo di `S1`: le espressioni di `csv/` scritte apposta FUORI dal nucleo, per il confronto al bit"),
    ('primo_ordine/_collauda_forme.py',
     'andnp.array_equal(MV.N_s1(rho,lam)[1:],lam[1:]*(x-np.arctan(x)))andMV.alpha_s1(rho,lam)[0]==MV.beta_s1(rho,lam)[0]==MV.N_s1(rho,lam)[0]==0.0,"")'):
        ('oracolo di collaudo', "l'oracolo di `S1` (`N`): idem"),
    ('primo_ordine/_collauda_materia_vuoto.py',
     'n_gira=-rho*np.log(rho/(rho+lam))'):
        ('oracolo di collaudo', 'braccio `(s3)`, il caso che DEVE fallire: la forma float di `S3` contro `log1p`; non chiama il nucleo'),
    ('primo_ordine/_deriva_forme_l2.py',
     'forme["S1"]=("N=LambdaG(x),G=x-arctanx",x-sp.atan(x))'):
        ('screening dichiarato', 'la derivazione `sympy` delle forme candidate `S1`-`S4` (screening)'),
    ('primo_ordine/_deriva_forme_l2.py',
     'forme["S3"]=("N=rholn(rho/(rho+Lambda))",x*sp.log(x/(1+x)))'):
        ('screening dichiarato', 'idem, `S3`'),
    ('primo_ordine/_misura_forme_l2.py',
     'returnx**2/(1.0+x**2),x/(1.0+x**2)-np.arctan(x)'):
        ('screening dichiarato', 'le quattro forme candidate per il confronto (`_alpha_beta`), usate da `statica_protocollo`'),
    ('primo_ordine/_misura_forme_l2.py',
     'al=np.log(x/(1.0+x))+1.0/(1.0+x)'):
        ('screening dichiarato', 'idem, `S3`'),
    ('primo_ordine/_misura_mb2.py',
     'N[vivi]=rho[vivi]*np.log(rho[vivi]/(rho[vivi]+lam[vivi]))'):
        ('legge a mano', 'la `N` di `S3` in `h_tot`: la seconda fonte non segue la forma della tabella'),
    ('primo_ordine/_misura_mb2.py',
     'N[vivi]=rho[vivi]*np.log(rho[vivi]/(rho[vivi]+lam[vivi]))'):
        ('legge a mano', 'la `N` di `S3` in `pezzi_di_h` (i bracci `(a)` e `(b)` di `H_w`)'),
    ('primo_ordine/energia_pesata.py',
     'N[vivi]=rho[vivi]*np.log(rho[vivi]/(rho[vivi]+lam[vivi]))'):
        ('legge a mano', 'la `N` di `S3` in `termini_di_h` (`Omega` e `g_dello_stato`)'),
    ('primo_ordine/saturazione.py',
     'returnx-np.arctan(x)'):
        ("modulo di un'altra legge", "`CAMM-SATURAZIONE` (`G(x) = x - arctan x` di `h_int`), il modulo della sua legge; fuori dall'ordine di composizione"),
    ('primo_ordine/saturazione.py',
     'return(x*x)/(1.0+x*x)'):
        ("modulo di un'altra legge", 'idem, `a(x)`'),
    ('primo_ordine/saturazione.py',
     'returnx/(1.0+x*x)-np.arctan(x)'):
        ("modulo di un'altra legge", 'idem, `b(x)`'),
    ('csv/solitone/misure.py',
     'return-math.atan2(v.imag,v.real)/dtau'):
        ("non e' la legge", '`atan2`: la fase di un numero complesso (una frequenza misurata)'),
    ('csv/solitone/protetto.py',
     'return-math.atan2(lam.imag,lam.real)/s,float(np.linalg.norm(T-lam*p)/np.linalg.norm(p))'):
        ("non e' la legge", "`atan2`: la fase dell'autovalore (una frequenza misurata)"),
}

STRINGA = {tokenize.STRING, tokenize.COMMENT}
for _n in ("FSTRING_START", "FSTRING_MIDDLE", "FSTRING_END"):
    if hasattr(tokenize, _n):
        STRINGA.add(getattr(tokenize, _n))


def righe_di_codice(testo):
    """### `{riga: codice}`: i token che NON sono commenti ne' stringhe, uniti da spazi; e `{riga: testo}` per commenti e stringhe."""
    codice, parole = {}, {}
    for t in tokenize.generate_tokens(io.StringIO(testo).readline):
        if t.type in (tokenize.NL, tokenize.NEWLINE, tokenize.INDENT, tokenize.DEDENT, tokenize.ENDMARKER):
            continue
        dest = parole if t.type in STRINGA else codice
        dest[t.start[0]] = dest.get(t.start[0], "") + " " + t.string
    return codice, parole


def chiave(riga):
    return re.sub(r"\s+", "", riga)


def cerca(rel, testo):
    """### `(nel codice, nel testo)`: liste di `(riga, pattern, testo della riga)`."""
    codice, parole = righe_di_codice(testo)
    sorgente = testo.splitlines()
    nel_codice, nel_testo = [], []
    for dest, mappa in ((nel_codice, codice), (nel_testo, parole)):
        for n in sorted(mappa):
            for nome, p in PATTERN:
                if p.search(mappa[n]):
                    dest.append((n, nome, sorgente[n - 1].strip() if n - 1 < len(sorgente) else mappa[n].strip()))
                    break
    return nel_codice, nel_testo


def file_in_esame():
    for d in DOVE:
        for cart, _s, ff in os.walk(os.path.join(RADICE, d)):
            if "__pycache__" in cart:
                continue
            for f in sorted(ff):
                if not f.endswith(".py"):
                    continue
                rel = os.path.relpath(os.path.join(cart, f), RADICE).replace(os.sep, "/")
                if rel in ESCLUSI or any(rel.startswith(c) for c in ESCLUSE_CARTELLE):
                    continue
                yield rel


def giudica(rel, nel_codice):
    """### `[(riga, pattern, testo, categoria, perche')]`; categoria `None` = senza giudizio."""
    fuori = []
    for n, nome, t in nel_codice:
        g = GIUDIZI.get((rel, chiave(t)))
        fuori.append((n, nome, t, g[0] if g else None, g[1] if g else ""))
    return fuori


def caso_che_deve_fallire():
    """### Una riga sintetica con la formula di `S3`, in un file finto giudicato come `energia_pesata.py`: **deve** risultare `legge a mano` o senza giudizio."""
    finto = "import numpy as np\n# rho*log(rho/(rho+lam)) in un commento non conta\nN = rho * np.log(rho / (rho + lam))\nb = x - np.arctan(x)\n"
    nc, nt = cerca("finto.py", finto)
    return [r[0] for r in nc] == [3, 4] and len(nt) == 1


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    print("=" * 140)
    print("LA RICERCA PER FORMULE (non per nomi): %s, esclusi %s e %s" % (", ".join(DOVE), ", ".join(ESCLUSI), ", ".join(ESCLUSE_CARTELLE)))
    print("  i pattern: %s" % "; ".join(n for n, _p in PATTERN))
    print("=" * 140)
    tutte, testo_per_file, visti = [], {}, set()
    nfile = 0
    for rel in file_in_esame():
        nfile += 1
        with open(os.path.join(RADICE, rel), encoding="utf-8") as fh:
            testo = fh.read()
        nc, nt = cerca(rel, testo)
        if nt:
            testo_per_file[rel] = len(nt)
        for r in giudica(rel, nc):
            tutte.append((rel,) + r)
            visti.add((rel, chiave(r[2])))
    print("NEL CODICE: %d occorrenze in %d file (su %d esaminati)" % (len(tutte), len({t[0] for t in tutte}), nfile))
    for rel, n, nome, t, cat, perche in tutte:
        print("  %-45s %5d  %-12s %-26s %s" % (rel, n, nome, cat or "### SENZA GIUDIZIO", t[:110]))
        if perche:
            print("  %-45s %5s  %-12s %-26s   -> %s" % ("", "", "", "", perche))
    print("NEL TESTO (commenti e stringhe, non si giudicano): %d occorrenze in %d file" % (sum(testo_per_file.values()), len(testo_per_file)))
    for rel in sorted(testo_per_file):
        print("  %-45s %d" % (rel, testo_per_file[rel]))
    orfani = [(k, v) for k, v in GIUDIZI.items() if k not in visti]
    corretti = [(k, v) for k, v in orfani if v[0] == "legge a mano"]
    orfani = [(k, v) for k, v in orfani if v[0] != "legge a mano"]
    for (rel, t), (cat, _p) in corretti:
        print("  ### SPARITA (era `legge a mano`, cioe' CORRETTA): %s  %s" % (rel, t[:100]))
    for (rel, t), (cat, _p) in orfani:
        print("  ### GIUDIZIO ORFANO (%s): %s  %s" % (cat, rel, t[:100]))
    a_mano = [t for t in tutte if t[4] == "legge a mano"]
    senza = [t for t in tutte if t[4] is None]
    cattive = [k for k, v in GIUDIZI.items() if v[0] not in CATEGORIE]
    per_cat = {c: sum(1 for t in tutte if t[4] == c) for c in CATEGORIE}
    print("=" * 140)
    print("PER CATEGORIA: %s" % "; ".join("%s %d" % (c, per_cat[c]) for c in CATEGORIE))
    esiti = [("il caso che DEVE fallire: la formula di `S3` in una riga sintetica si trova nel codice, e quella nel commento si separa", caso_che_deve_fallire()),
             ("ogni occorrenza nel codice ha un giudizio (%d senza)" % len(senza), not senza),
             ("nessun giudizio orfano e nessuna categoria fuori elenco (%d, %d)" % (len(orfani), len(cattive)), not orfani and not cattive),
             ("DEVE PASSARE: zero `legge a mano` fuori da materia_vuoto.py (%d)" % len(a_mano), not a_mano)]
    for che, passa in esiti:
        print("  %-120s %s" % (che, "PASSA" if passa else "### FALLISCE"))
    ok = all(p for _c, p in esiti)
    print("LA RICERCA PER FORMULE: %s" % ("### TUTTO PASSA" if ok else "### CI SONO ROSSI"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
