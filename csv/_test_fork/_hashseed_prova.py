# -*- coding: utf-8 -*-
"""**PROVA DECISIVA su `HASHSEED-RIPROD`: il SIMULATORE dipende da `PYTHONHASHSEED`?**

**Perche' esiste (obiezione di Luca a `c7f1573`, e ha ragione su tre punti):**
1. `V1` di stamattina (`4f2b224`) ha rigirato il pilota **in un altro processo**, 4 semi, 120
   passi, e ha trovato **0 campi diversi**. **Nel repo nessun `PYTHONHASHSEED` e' impostato.**
2. Le differenze fra invocazioni sono emerse nel presidio **quando usava ancora `hash()`** per i
   semi -- **il suo difetto 2**. **E' la causa piu' probabile.**
3. La riga *«senza fissare nulla»* della mia tabella **passava dal rilancio automatico con 0**:
   ### **non provava niente.** E' un errore mio, e questo strumento esiste per correggerlo.

**CHE COSA FA, e come evita di rifare lo stesso errore:**
  - gira **IL SIMULATORE E BASTA**: argv del driver, scena `(ii)(a)`, seme `11`, `3` passi pieni
    **nell'ordine canonico**, **nessuna iniezione di `rng`**, **nessun presidio**;
  - **NON contiene `hash()`** in nessuna forma, e non fissa `PYTHONHASHSEED` da se';
  - scarica le **21 grandezze di stato** in un `.npz` **grezzo**, piu' `i`, `j`, `n`;
  - `--confronta A.npz B.npz` li confronta **byte per byte**.

**IL VALORE DI `PYTHONHASHSEED` SI LEGGE E SI STAMPA**: se non e' impostato, lo dice e
**non lo imposta**. Chi lancia deve fissarlo, ed e' il punto della prova.

COMANDO (i due giri e il confronto):
  PYTHONHASHSEED=1 python csv/_test_fork/_hashseed_prova.py --out=hs1.npz
  PYTHONHASHSEED=2 python csv/_test_fork/_hashseed_prova.py --out=hs2.npz
  python csv/_test_fork/_hashseed_prova.py --confronta hs1.npz hs2.npz
"""
import io
import json
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, os.path.join(RADICE, "csv"))
import _presidio  # noqa: E402

_presidio.avvia(__file__)

STATO = ["d", "d0", "phi", "phi_s", "phivel", "psi", "psi_spin", "_psi_spinor", "_psi_prec",
         "_spinor_lift", "omega_s", "_nb", "_nb_prec", "eta", "tw", "twp", "vd", "peq",
         "mem_mot", "perc_chi", "perc_geom"]


def confronta(pa, pb):
    """Le 21 grandezze, byte per byte. `nan` allineati contano UGUALI."""
    A, B = np.load(pa, allow_pickle=True), np.load(pb, allow_pickle=True)
    def _bl(z):
        return str(z["_blob_sim"])[:8] if "_blob_sim" in z.files else "(non registrato)"
    print("HASHSEED di A: %s   di B: %s" % (str(A["_hashseed"]), str(B["_hashseed"])))
    print("BLOB del simulatore, A: %s   B: %s" % (_bl(A), _bl(B)))
    def _av(z):
        return str(z["_argv"]) if "_argv" in z.files else "(non registrato)"
    print("ARGV di A: %s" % _av(A))
    print("ARGV di B: %s" % _av(B))
    print("  -> configurazioni %s" % ("UGUALI" if _av(A) == _av(B) else "### DIVERSE"))
    print("n di A: %s   n di B: %s" % (str(A["n"]), str(B["n"])))
    print("")
    print("  %-14s %-10s %-12s %s" % ("grandezza", "forma", "identico?", "elementi diversi"))
    diversi, righe = [], []
    for k in STATO + ["i", "j"]:
        if k not in A.files or k not in B.files:
            print("  %-14s %s" % (k, "ASSENTE in uno dei due"))
            righe.append({"grandezza": k, "esito": "assente"})
            continue
        va, vb = A[k], B[k]
        if va.shape != vb.shape:
            print("  %-14s %-10s %-12s %s" % (k, va.shape, "NO", "FORMA DIVERSA %s vs %s"
                                              % (va.shape, vb.shape)))
            diversi.append(k)
            righe.append({"grandezza": k, "esito": "forma diversa"})
            continue
        ident = bool(np.array_equal(va, vb, equal_nan=True)) if va.dtype.kind == "f" \
            else bool(np.array_equal(va, vb))
        nd = 0
        if not ident:
            with np.errstate(all="ignore"):
                if va.dtype.kind == "f":
                    na, nb = np.isnan(va), np.isnan(vb)
                    nd = int(np.sum((va != vb) & ~(na & nb)))
                else:
                    nd = int(np.sum(va != vb))
            diversi.append(k)
        print("  %-14s %-10s %-12s %d" % (k, str(va.shape), "si" if ident else "### NO", nd))
        righe.append({"grandezza": k, "identico": ident, "diversi": nd, "n": int(va.size)})
    print("")
    print("=" * 78)
    # ⚠ IL VERDETTO E' NEUTRO, E NON E' UN DETTAGLIO: questo confronto serve a DUE sigilli
    #   diversi -- la prova su PYTHONHASHSEED e il sigillo byte-identico dell'archiviazione --
    #   e la prima stesura stampava <<PYTHONHASHSEED non cambia niente>> anche quando i due
    #   stati venivano da DUE BLOB DI SIMULATORE diversi. **Una conclusione cablata nello
    #   strumento diventa vera per qualunque cosa gli si dia da confrontare**: lo strumento dice
    #   se sono uguali, l'interpretazione sta nel referto di chi lo chiama.
    if diversi:
        print("### DIVERSE: %d grandezze -> %s" % (len(diversi), ", ".join(diversi)))
    else:
        print("### IDENTICHE: tutte e %d le grandezze confrontate, byte per byte." % len(righe))
    print("=" * 78)
    OUT = os.path.join(_QUI, "_hashseed_prova.json")
    io.open(OUT, "w", encoding="utf-8", newline=chr(10)).write(json.dumps(
        {"a": os.path.basename(pa), "b": os.path.basename(pb),
         "hashseed_a": str(A["_hashseed"]), "hashseed_b": str(B["_hashseed"]),
         "blob_sim_a": _bl(A), "blob_sim_b": _bl(B),
         "diverse": diversi, "righe": righe}, indent=1, ensure_ascii=False, sort_keys=True))
    print("")
    print("scritto: " + OUT)
    return 1 if diversi else 0


def gira(out, seme, passi, extra=None):
    import _cli_flag
    import _passo
    hs = os.environ.get("PYTHONHASHSEED")
    print("PYTHONHASHSEED nell'ambiente: %s" % (hs if hs is not None else "NON IMPOSTATO"))
    print("  (questo strumento NON lo imposta, e NON usa hash(): lo legge e lo dichiara)")
    print("")
    S0, argv = _cli_flag.argv_del_driver(extra=["--seme=%d" % seme],
                                         dest=os.path.join(_QUI, "_scarto_cli"))
    # `--extra`: flag AGGIUNTI a quelli del driver. Serve a misurare una configurazione che il
    # driver non usa (per esempio `--scala-min` INSIEME a `--scala-min-passo`), e finisce nel
    # referto perche' `P5` vuole la configurazione INTERA, non la differenza.
    if extra:
        argv = list(argv) + list(extra)
        print("FLAG EXTRA, aggiunti a quelli del driver: %s" % " ".join(extra))
    S, a = _cli_flag.carica_dal_cli(list(argv), nome="sim_hs")
    print("CONFIGURAZIONE INTERA (%d voci): %s" % (len(argv), " ".join(argv[1:])))
    S._NMASSE_VIDEO["n"] = 2
    S._NMASSE_VIDEO["sep"] = 3.0
    S._NMASSE_VIDEO["size"] = None
    S.avvia_test("MASSE-COERENTI")()
    net = S.net
    print("")
    print("scena (ii)(a): n = %d, m = %d. Giro %d passi pieni, ordine CANONICO, nessuna"
          % (net.n, len(net.i), passi))
    print("iniezione di rng, nessun presidio.")
    for _ in range(passi):
        _passo.passo_pieno(S, net)
    # ⚠ IL BLOB DEL SIMULATORE VA DENTRO IL DUMP: senza, un confronto fra due stati non puo'
    #   dire QUALI due versioni ha confrontato, e il referto asserisce invece di provare.
    #   `PRIMA.npz` del sigillo (b)1 e' nato prima di questa riga e NON lo porta: per quello
    #   la provenienza e' il tag `pre-archivio-pavimenti`, dichiarata nel task history.
    import hashlib as _hl
    _bl = _hl.sha1(io.open(os.path.join(RADICE, "soliton_simulator.py"), "rb").read()).hexdigest()
    print("blob del simulatore (sha1 dei byte): %s" % _bl[:8])
    dati = {"n": np.asarray(net.n), "_hashseed": np.asarray(str(hs)),
            "_blob_sim": np.asarray(_bl), "_passi": np.asarray(passi),
            "_seme": np.asarray(seme), "_argv": np.asarray(" ".join(argv[1:]))}
    # I CONTATORI DEL CONFINE DEL PASSO, nel dump: dalla cura `(c)1` il confine e' idempotente e
    # <<quante leggi hanno trovato la fotografia gia' aperta>> e' un numero che il sigillo deve
    # poter LEGGERE, non supporre (`A8`).
    CONT = ("_g_smp_aperture", "_g_smp_gia_aperta", "_g_smp_chiusure", "_g_smp_d_chiusure",
            "_g_smp_chirurgie", "_g_smp_disallineati", "_g_sm_patol", "_g_sm_nascite")
    for _k in CONT:
        dati["cnt_" + _k] = np.asarray(int(getattr(net, _k, 0)))
    print("contatori del confine: " + "  ".join("%s=%d" % (_k, int(getattr(net, _k, 0)))
                                                for _k in CONT))
    for k in STATO + ["i", "j"]:
        v = getattr(net, k, None)
        if v is not None:
            dati[k] = np.asarray(v)
    np.savez(out, **dati)
    print("")
    print("scritto: %s   (n finale = %d, grandezze salvate = %d)"
          % (out, net.n, len(dati) - 4))
    return 0


if __name__ == "__main__":
    A = sys.argv[1:]
    if "--confronta" in A:
        k = A.index("--confronta")
        sys.exit(confronta(A[k + 1], A[k + 2]))
    out, seme, passi, extra = os.path.join(_QUI, "_hs.npz"), 11, 3, []
    for x in A:
        if x.startswith("--out="):
            out = x.split("=", 1)[1]
        elif x.startswith("--seme="):
            seme = int(x.split("=", 1)[1])
        elif x.startswith("--passi="):
            passi = int(x.split("=", 1)[1])
        elif x.startswith("--extra="):
            extra += x.split("=", 1)[1].split(",")
    sys.exit(gira(out, seme, passi, extra))
