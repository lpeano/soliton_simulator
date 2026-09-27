# -*- coding: utf-8 -*-
"""**`H-ETC-2` — PERMUTARE L'ORDINE DELLE CINQUE LEGGI DEVE DARE LO STESSO STATO (Jacobi).**

**Che cosa certifica:** che il passo pieno sia **indipendente dall'ordine** in cui le sue cinque
leggi girano. E' la definizione operativa di *«tutto simultaneo»*: se permutare l'ordine cambia
lo stato, il passo e' **Gauss-Seidel**, non Jacobi, e la cura `ETC-PASSO` non e' fatta.

> ### 🛑 **IL CASO CHE DEVE FALLIRE, ed e' il piu' importante (`P1-sexies`, `A9`):**
> girato sul codice **di oggi** -- cura **spenta** -- **DEVE FALLIRE**. Con **56 letture sporche**
> misurate dalla FASE 0, un passo che risultasse gia' indipendente dall'ordine significherebbe che
> **il presidio non sta guardando lo stato**. **Se passa sul codice di oggi, ci si FERMA e il
> presidio non si consegna.**

**COME, e le tre scelte che lo rendono una misura invece di un rumore:**

**① LE PERMUTAZIONI AMMESSE NON SPOSTANO `mitosi`.** La mitosi **cambia la struttura**: spostarla
   cambia **quali** nodi esistono, e il confronto misurerebbe **la nascita**, non la sincronia.
   Con `mitosi` ferma al posto 3, restano **tre** permutazioni: scambiare le due leggi **prima**
   di lei, le due **dopo**, o entrambe.

**② I FLUSSI CASUALI SONO PER LEGGE**, derivati da `(seme, passo, legge)`. **Senza questo il
   presidio fallirebbe per il motivo sbagliato:** `scuoti_vuoto`, `step` e `mitosi` consumano
   `rng` *(1, 7, 4 siti)*, e con un flusso unico permutarle cambia **le estrazioni**, non la
   fisica. Il presidio **inietta** il flusso prima di ogni legge -- **e non tocca il simulatore**:
   e' `net.rng` che viene sostituito, dall'esterno, per la durata della chiamata.

**③ LA TOLLERANZA E' DERIVATA, NON SCELTA** (`A1`, zero manopole). Sotto Jacobi l'unica
   differenza legittima fra due ordini e' la **non associativita' della somma in virgola mobile**:
   sommare le stesse variazioni in ordine diverso. L'errore e' limitato da
   `n_addendi * 2^-52 * |valore|`, e gli addendi sono **le cinque leggi**. Quindi:

       TOLLERANZA RELATIVA = 5 * 2^-52   (~1.11e-15)

   Nessun numero e' stato tarato: viene dal formato `float64` e dal numero di leggi.

COMANDO:  python csv/_seal_fork/_h_etc_2.py [--passi=1] [--seme=11]
USCITA:   0 se il passo e' INDIPENDENTE dall'ordine, 1 se NON lo e'.
          **Sul blob di oggi ci si ASPETTA 1.**
"""
import copy
import io
import json
import os
import sys
import zlib

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))

# ====================================================================== `HASHSEED-RIPROD`
# ⚠ **IL SIMULATORE NON E' RIPRODUCIBILE FRA PROCESSI SE `PYTHONHASHSEED` NON E' FISSATO.**
#   **Misurato qui, il 2026-09-27:** tre invocazioni dello STESSO comando davano differenze
#   peggiori `1.999884`, `1.999889`, `1.999890` e `phi` diversa su `2053`/`2054`/`2060`
#   elementi. Con `PYTHONHASHSEED=0` **due giri danno il referto BYTE-IDENTICO**
#   (`sha1 1da33034cbe3` entrambi).
#   **Non e' un difetto di questo presidio** -- che non usa piu' `hash()` -- ma della catena
#   scena + simulatore, dove l'ordine di iterazione di qualche insieme dipende dall'hash.
#   **Quindi il presidio NON SPERA: rimette in moto se stesso col seme fissato.** Un presidio
#   che chiedesse all'utente di ricordarsi una variabile d'ambiente non impedirebbe nulla (`A9`).
#   ⚠⚠ **E NON SI USA `os.execve`: SU WINDOWS NON SOSTITUISCE IL PROCESSO.** La `exec` del CRT
#   di Windows **avvia un processo nuovo e TERMINA quello corrente con codice `0`**. Il risultato
#   e' che il presidio **usciva sempre `0`** -- cioe' **PASSAVA SEMPRE** -- anche con 3 permutazioni
#   su 3 fallite. **L'ho visto:** il referto diceva `falliti: 3` e `echo $?` diceva `0`.
#   **Un presidio che esce 0 qualunque cosa accada non e' un presidio** (`A9`), ed e' il difetto
#   piu' insidioso possibile qui: non sbaglia la misura, sbaglia il VERDETTO.
#   Si usa `subprocess` e **si propaga il codice d'uscita**.
if os.environ.get("PYTHONHASHSEED") != "0":
    import subprocess
    _amb = dict(os.environ)
    _amb["PYTHONHASHSEED"] = "0"
    sys.stderr.write("[H-ETC-2] PYTHONHASHSEED non era 0: mi rilancio con 0 "
                     "(vedi HASHSEED-RIPROD).\n")
    sys.stderr.flush()
    sys.exit(subprocess.run([sys.executable] + sys.argv, env=_amb).returncode)
sys.path.insert(0, os.path.join(RADICE, "csv"))
import _presidio  # noqa: E402

_presidio.avvia(__file__)
import _cli_flag  # noqa: E402
import _passo  # noqa: E402

# le 21 grandezze di STATO FISICO fissate dalla FASE 0 di `ETC-PASSO`
STATO = ["d", "d0", "phi", "phi_s", "phivel", "psi", "psi_spin", "_psi_spinor", "_psi_prec",
         "_spinor_lift", "omega_s", "_nb", "_nb_prec", "eta", "tw", "twp", "vd", "peq",
         "mem_mot", "perc_chi", "perc_geom"]

TOLL = 5 * 2.0 ** -52          # derivata: 5 leggi, float64. NON tarata.


def _semina_per_legge(net, seme, passo, legge):
    """Il flusso casuale di UNA legge: `(seme, passo, legge)` -> uno `rng` suo.

    **Non tocca il simulatore:** sostituisce `net.rng` dall'esterno, prima della chiamata.
    La chiave e' un intero costruito dai tre pezzi, cosi' due ordini diversi dello stesso
    passo danno alla stessa legge **lo stesso flusso**.

    ⚠ **NON si usa `hash()`:** l'hash delle stringhe in Python e' **randomizzato per processo**
    (`PYTHONHASHSEED`), quindi due invocazioni dello stesso comando darebbero **semi diversi**.
    **L'ho visto accadere:** fra due giri identici la differenza peggiore passava da `1.999884` a
    `1.999889` e gli elementi diversi di `phi` da `2053` a `2060`. **Un presidio non riproducibile
    non e' un presidio** (`A9`). Si usa `crc32`, che e' **stabile per definizione**.
    """
    chiave = (int(seme) * 1_000_003 + int(passo) * 10_007
              + zlib.crc32(legge.encode("utf-8")) % 100_003)
    net.rng = np.random.default_rng(chiave)


def _gira(S, net, ordine, seme, passi):
    """`passi` passi pieni nell'ORDINE dato, con un flusso casuale PER LEGGE."""
    for p in range(passi):
        for tipo, nome in ordine:
            _semina_per_legge(net, seme, p, nome)
            if tipo == "metodo":
                getattr(net, nome)()
            else:
                getattr(S, nome)(net)


def _confronta(A, B):
    """Le differenze fra due reti, sulle 21 grandezze di stato. Ritorna (righe, peggiore)."""
    righe = []
    for a in STATO:
        va, vb = getattr(A, a, None), getattr(B, a, None)
        if va is None or vb is None:
            righe.append({"attributo": a, "esito": "assente", "delta": None})
            continue
        va, vb = np.asarray(va), np.asarray(vb)
        if va.shape != vb.shape:
            righe.append({"attributo": a, "esito": "FORMA DIVERSA",
                          "forma_a": list(va.shape), "forma_b": list(vb.shape), "delta": None})
            continue
        if va.size == 0:
            righe.append({"attributo": a, "esito": "vuoto", "delta": 0.0})
            continue
        # ⚠ I `NaN` CI SONO DI PROPOSITO: `peq` NASCE `nan` e viene CALIBRATO da `step()`
        #   sulla `rho` del proprio arco. Quindi non si puo' sottrarre alla cieca -- e il
        #   simulatore gira con `np.errstate` in modalita' `raise`, che lo trasforma in
        #   un'eccezione. Si confrontano TRE cose, separate:
        #     - le posizioni dove ENTRAMBI sono `nan`: UGUALI (e' lo stesso segnaposto);
        #     - le posizioni dove UNO SOLO e' `nan`: DIVERSE, e si contano;
        #     - le altre: la differenza relativa.
        with np.errstate(all="ignore"):
            na, nb = np.isnan(va), np.isnan(vb)
            ia, ib = np.isinf(va), np.isinf(vb)
            # ### PRIMA L'IDENTITA' ESATTA, e questo ordine NON e' un dettaglio.
            #   `eta` contiene INFINITI, e `inf - inf` fa `nan`: calcolare la differenza
            #   PRIMA di aver verificato l'uguaglianza fa apparire DIVERSO un array
            #   IDENTICO. La prima stesura lo faceva, e segnalava `eta` come diversa con
            #   `elementi diversi 0/2107` -- cioe' si contraddiceva da sola.
            #   Un presidio che da' un falso allarme e' peggio di uno assente (`A9`):
            #   dopo la cura NON PASSEREBBE MAI.
            identico = bool(np.array_equal(va, vb, equal_nan=True))
            solo_uno_nan = int(np.sum(na != nb))
            inf_disallineati = int(np.sum(ia != ib))
            if identico:
                rel, mx, diversi = 0.0, 0.0, 0
            else:
                buoni = ~(na | nb | ia | ib)
                if np.any(buoni):
                    xa, xb = va[buoni], vb[buoni]
                    dd = np.abs(xa - xb)
                    scala = np.maximum(np.abs(xa), np.abs(xb))
                    rel = float(np.max(np.where(scala > 0, dd / np.maximum(scala, 1e-300), 0.0)))
                    mx = float(np.max(dd))
                    diversi = int(np.sum(xa != xb))
                else:
                    rel, mx, diversi = 0.0, 0.0, 0
        rotto = (solo_uno_nan > 0 or inf_disallineati > 0)
        ok = identico or (not rotto and rel <= TOLL)
        righe.append({"attributo": a, "identico": identico,
                      "diversi": diversi + solo_uno_nan + inf_disallineati, "n": int(va.size),
                      "nan_disallineati": solo_uno_nan, "nan_entrambi": int(np.sum(na & nb)),
                      "inf_disallineati": inf_disallineati, "inf_totali": int(np.sum(ia | ib)),
                      "max_assoluto": mx, "max_relativo": rel,
                      "esito": "uguale" if ok else "DIVERSO",
                      "delta": 0.0 if ok else (float("inf") if rotto else rel)})
    peggiore = max((r for r in righe if r.get("delta") is not None),
                   key=lambda r: r["delta"], default=None)
    return righe, peggiore


def principale():
    passi, seme = 1, 11
    for x in sys.argv[1:]:
        if x.startswith("--passi="):
            passi = int(x.split("=", 1)[1])
        if x.startswith("--seme="):
            seme = int(x.split("=", 1)[1])

    S0, argv = _cli_flag.argv_del_driver(extra=["--seme=%d" % seme],
                                         dest=os.path.join(_QUI, "_scarto_cli"))
    S, a = _cli_flag.carica_dal_cli(list(argv), nome="sim_hetc2")
    print("CONFIGURAZIONE INTERA, dall'argv COSTRUITO DAL DRIVER (%d voci):" % len(argv))
    print("  " + " ".join(argv[1:]))
    print("")
    import hashlib
    _bl = hashlib.sha1(io.open(os.path.join(RADICE, "soliton_simulator.py"), "rb").read()).hexdigest()
    print("BLOB DEL SIMULATORE (sha1 dei byte): %s" % _bl[:8])

    CANON = _passo.ordine()
    nomi = [n for _t, n in CANON]
    k = nomi.index("mitosi")
    assert k == 2, "mitosi non e' al posto 3: le permutazioni ammesse vanno ripensate"

    def scambia(seq, x, y):
        s = list(seq)
        s[x], s[y] = s[y], s[x]
        return s

    PERMUTAZIONI = [
        # ### IL CONTROLLO POSITIVO, e viene PRIMO: l'ordine IDENTICO deve dare lo STESSO stato.
        #   Senza questo, `H-ETC-2` potrebbe essere una macchina che dice sempre NO -- e un
        #   presidio che fallisce comunque non distingue niente. Se questo FALLISCE il presidio
        #   e' rotto (tipicamente: il flusso casuale per legge non e' deterministico), e ci si
        #   ferma PRIMA di guardare le permutazioni vere.
        ("CONTROLLO POSITIVO: ordine IDENTICO (deve PASSARE)", list(CANON)),
        ("scambio le due leggi PRIMA di mitosi", scambia(CANON, 0, 1)),
        ("scambio le due leggi DOPO mitosi", scambia(CANON, 3, 4)),
        ("scambio entrambe le coppie", scambia(scambia(CANON, 0, 1), 3, 4)),
    ]
    print("ordine CANONICO : " + " -> ".join(nomi))
    print("permutazioni ammesse: %d (nessuna sposta `mitosi`)" % len(PERMUTAZIONI))
    print("tolleranza RELATIVA derivata: 5 * 2^-52 = %.3e  (5 leggi, float64)" % TOLL)
    print("")

    S._NMASSE_VIDEO["n"] = 2
    S._NMASSE_VIDEO["sep"] = 3.0
    S._NMASSE_VIDEO["size"] = None
    S.avvia_test("MASSE-COERENTI")()
    base = S.net
    print("scena (ii)(a): n = %d nodi, m = %d archi, %d passi per braccio"
          % (base.n, len(base.i), passi))
    print("")

    A = copy.deepcopy(base)
    S.net = A
    _gira(S, A, CANON, seme, passi)

    esiti, falliti = [], 0
    rotto_presidio = [False]
    for eti, perm in PERMUTAZIONI:
        B = copy.deepcopy(base)
        S.net = B
        _gira(S, B, perm, seme, passi)
        righe, peg = _confronta(A, B)
        diversi = [r for r in righe if r["esito"] in ("DIVERSO", "FORMA DIVERSA")]
        stessa_n = (A.n == B.n)
        print("=" * 78)
        print("PERMUTAZIONE: %s" % eti)
        print("  " + " -> ".join(n for _t, n in perm))
        print("  n finale: A = %d, B = %d   %s"
              % (A.n, B.n, "uguale" if stessa_n else "### DIVERSO"))
        print("  grandezze di stato DIVERSE: %d su %d" % (len(diversi), len(righe)))
        if peg:
            print("  differenza relativa PEGGIORE: %.6e   su `%s`" % (peg["delta"], peg["attributo"]))
        for r in sorted(diversi, key=lambda x: -(x.get("delta") or 0))[:8]:
            if r["esito"] == "FORMA DIVERSA":
                print("    %-14s FORMA DIVERSA %s vs %s" % (r["attributo"], r["forma_a"], r["forma_b"]))
            else:
                print("    %-14s rel %.3e   assoluta %.3e   elementi diversi %d/%d"
                      % (r["attributo"], r["max_relativo"], r["max_assoluto"],
                         r["diversi"], r["n"]))
        ok = (not diversi) and stessa_n
        print("  -> %s" % ("INDIPENDENTE dall'ordine" if ok else "### DIPENDE DALL'ORDINE"))
        print("")
        controllo = eti.startswith("CONTROLLO POSITIVO")
        if controllo and not ok:
            print("  ### IL CONTROLLO POSITIVO FALLISCE: IL PRESIDIO E' ROTTO.")
            print("      L'ordine identico DEVE dare lo stesso stato. Se non lo da', il flusso")
            print("      casuale per legge non e' deterministico. CI SI FERMA QUI.")
            print("")
        if controllo and ok:
            print("  ### il controllo positivo PASSA: il presidio non e' una macchina che dice")
            print("      sempre NO, e il flusso casuale per legge e' deterministico.")
            print("")
        if not ok and not controllo:
            falliti += 1
        if controllo and not ok:
            rotto_presidio[0] = True
        esiti.append({"permutazione": eti, "ordine": [n for _t, n in perm], "passa": bool(ok),
                      "controllo_positivo": bool(controllo),
                      "n_A": int(A.n), "n_B": int(B.n), "righe": righe})

    print("=" * 78)
    if rotto_presidio[0]:
        print("### H-ETC-2 NON E' CONSEGNABILE: il controllo positivo e' fallito.")
        print("=" * 78)
        return 2
    print("### H-ETC-2 : %d permutazioni VERE su %d FALLISCONO"
          % (falliti, len(PERMUTAZIONI) - 1))
    if falliti:
        print("    IL PASSO DIPENDE DALL'ORDINE. E' il risultato ATTESO sul codice di oggi:")
        print("    il presidio GUARDA lo stato, e la cura ETC-PASSO non e' ancora fatta.")
    else:
        print("    IL PASSO E' GIA' INDIPENDENTE DALL'ORDINE.")
        print("    ⚠ SUL CODICE DI OGGI QUESTO SIGNIFICA CHE IL PRESIDIO NON GUARDA LO STATO:")
        print("      con 56 letture sporche misurate, non puo' essere vero. CI SI FERMA.")
    print("=" * 78)

    OUT = os.path.join(_QUI, "_h_etc_2.json")
    io.open(OUT, "w", encoding="utf-8", newline=chr(10)).write(json.dumps(
        {"argv": argv[1:], "ordine_canonico": nomi, "tolleranza_relativa": TOLL, "blob_sim": _bl,
         "passi": passi, "seme": seme, "n": int(base.n), "m": int(len(base.i)),
         "falliti": falliti, "esiti": esiti}, indent=1, ensure_ascii=False, sort_keys=True))
    print("")
    print("scritto: " + OUT)
    return 1 if falliti else 0


if __name__ == "__main__":
    sys.exit(principale())
