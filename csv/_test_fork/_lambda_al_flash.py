# -*- coding: utf-8 -*-
"""**LA CAUSA DEL FLASH: la SCHERMATURA si spegne in silenzio al passo di nascita.**

**Non e' una mia scoperta:** l'ha trovata il guardiano *(Luca, 2026-09-28)* con una sonda che
traccia `psi` **legge per legge** nel passo della prima nascita. ### **Questa sonda la VERIFICA, che
e' cio' che il mandato chiede** -- e la verifica con i miei occhi, non ricopiando i suoi numeri.

**Il meccanismo, letto dal codice:**

```
lambda_nodi :3256   if not hasattr(self, "psi") or len(self.psi) < self.n:
                        return np.full(self.n, LAM)          <- RIPIEGO SILENZIOSO 1
lambda_nodi :3261   if getattr(self, "_calcolo_schermatura", False):
                        return np.full(self.n, LAM)          <- RIPIEGO SILENZIOSO 2
_lam_archi  :3281   li = self.lambda_nodi()
                    return maximum(0.5 * (li[i] + li[j]), 1e-6)
_pesi               base = np.exp(-self.d / self._lam_archi()) * ramp[i] * ramp[j]
```

### **Al passo di nascita `mitosi` fa crescere `n`, quindi `len(psi) < n`, quindi `lambda_nodi`
restituisce `LAM` PER TUTTA LA RETE: la schermatura SI SPEGNE.** E `lam` piu' grande vuol dire
`exp(-d/lam)` piu' grande, cioe' **pesi piu' grandi**, cioe' ### **`|psi|` piu' grande per TUTTI** --
non per il nato.

**CHE COSA MISURA, e sono tre cose per ogni chiamata di `_lam_archi`:** il valore *(min, media,
max)*, **quale dei due ripieghi ha scattato**, e **dentro quale legge** la chiamata avviene.

COMANDO:  python csv/_test_fork/_lambda_al_flash.py [--passi=46] [--sim=<percorso>]
USCITA:   0 se al passo di nascita si vede `lam = LAM` su tutti gli archi *(la causa CONFERMATA)*,
          1 se non si vede *(e allora la spiegazione del guardiano non regge, e va detto)*.
"""
import io
import json
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, os.path.join(RADICE, "csv"))
import _presidio  # noqa: E402

_presidio.avvia(__file__)
import numpy as np  # noqa: E402
import _cli_flag  # noqa: E402
import _passo  # noqa: E402

FUORI = os.path.join(RADICE, "csv", "_seal_fork", "_sig_nascita_atomica")


def principale():
    passi, sim = 46, None
    for x in sys.argv[1:]:
        if x.startswith("--passi="):
            passi = int(x.split("=", 1)[1])
        elif x.startswith("--sim="):
            sim = x.split("=", 1)[1]
    if not os.path.isdir(FUORI):
        os.makedirs(FUORI)
    import contextlib
    with contextlib.redirect_stdout(io.StringIO()):
        S0, argv = _cli_flag.argv_del_driver(extra=["--seme=11"],
                                            dest=os.path.join(FUORI, "_scarto_cli"))
        S, a = _cli_flag.carica_dal_cli(list(argv), nome="sim_lam", sim=sim)
        # `nmasse` e `sep` SI LEGGONO DA `a`: la scena GRANDE, quella dei fotogrammi
        S._NMASSE_VIDEO["n"] = max(2, int(getattr(a, "nmasse", 2)))
        S._NMASSE_VIDEO["sep"] = float(getattr(a, "sep", 3.0))
        S._NMASSE_VIDEO["size"] = None
        S.avvia_test("MASSE-COERENTI")()
        net = S.net
    LAM = float(getattr(S, "LAM"))
    print("simulatore ... %s" % (os.path.basename(sim) if sim else "soliton_simulator.py"))
    print("scena ........ nmasse %d, sep %.4f  ->  n = %d, archi = %d"
          % (S._NMASSE_VIDEO["n"], S._NMASSE_VIDEO["sep"], net.n, len(net.i)))
    print("LAM .......... %.6f   SCHERMATURA = %r" % (LAM, getattr(S, "SCHERMATURA", None)))
    print("")

    # ---- la SPIA su `_lam_archi`: nessun file del simulatore viene toccato ------------------
    stato = {"passo": 0}
    reg = {}
    _lam = net._lam_archi

    def lam_spiato():
        v = _lam()
        arr = np.atleast_1d(np.asarray(v, float))
        # QUALE ripiego ha scattato? Si guarda lo STESSO stato che il codice guarda.
        r1 = (not hasattr(net, "psi")) or len(net.psi) < net.n
        r2 = bool(getattr(net, "_calcolo_schermatura", False))
        reg.setdefault(stato["passo"], []).append(
            {"min": float(arr.min()), "media": float(arr.mean()), "max": float(arr.max()),
             "tutti_LAM": bool(np.all(np.abs(arr - LAM) < 1e-12)),
             "ripiego_len_psi": bool(r1), "ripiego_ricorsione": bool(r2),
             "len_psi": int(len(net.psi)) if hasattr(net, "psi") else -1, "n": int(net.n)})
        return v
    net._lam_archi = lam_spiato

    nascita = None
    for k in range(1, passi + 1):
        stato["passo"] = k
        with contextlib.redirect_stdout(io.StringIO()):
            n_prima = int(net.n)
            _passo.passo_pieno(S, net)
            _I = (np.abs(net.psi[:net.n]) ** 2 if hasattr(net, "psi")
                  and len(net.psi) >= net.n else np.zeros(int(net.n)))
            _g = net.pozzo_grafo(_I)[0]
        for v in reg.get(k, []):
            v["mean_phi_g_fine_passo"] = float(np.mean(np.abs(_g)))
        if nascita is None and int(net.n) > n_prima:
            nascita = k
        if k >= (nascita or 0) + 2 and nascita:
            break
    net._lam_archi = _lam

    if nascita is None:
        print("### NESSUNA NASCITA in %d passi: la verifica non si fa." % passi)
        return 1
    print("### PRIMA NASCITA al passo %d" % nascita)
    print("")
    print("  %-7s %-8s %-11s %-11s %-11s %-9s %-9s %s"
          % ("passo", "chiam.", "lam min", "lam media", "lam max", "= LAM?", "ripiego", "phi_g"))
    fuori = {}
    for k in sorted(reg):
        for q, v in enumerate(reg[k], 1):
            rip = ("len(psi)<n" if v["ripiego_len_psi"] else
                   ("ricorsione" if v["ripiego_ricorsione"] else "-"))
            print("  %-7d %-8d %-11.6f %-11.6f %-11.6f %-9s %-9s %.2f"
                  % (k, q, v["min"], v["media"], v["max"],
                     "### SI" if v["tutti_LAM"] else "no", rip,
                     v.get("mean_phi_g_fine_passo", float("nan"))))
        fuori[k] = reg[k]
    # il verdetto: al passo di nascita ESISTE una chiamata con `lam = LAM` su TUTTI gli archi,
    # e il ripiego che l'ha causata e' `len(psi) < n`?
    q_n = [v for v in reg.get(nascita, []) if v["tutti_LAM"] and v["ripiego_len_psi"]]
    normali = [v["media"] for k in reg for v in reg[k]
               if k != nascita and not v["tutti_LAM"]]
    print("")
    print("=" * 96)
    print("  al passo di nascita, chiamate con lam = LAM su TUTTI gli archi e ripiego "
          "`len(psi) < n`: %d" % len(q_n))
    if normali:
        print("  lam medio nei passi NORMALI: da %.6f a %.6f   (LAM = %.6f)"
              % (min(normali), max(normali), LAM))
    if q_n:
        print("  ### CONFERMATO: al passo di nascita la SCHERMATURA SI SPEGNE per TUTTA LA RETE.")
        print("  ### E il ripiego che la spegne e' `len(self.psi) < self.n` (:3256), cioe'")
        print("  ### ESATTAMENTE l'effetto che la mitosi produce facendo crescere `n`.")
    else:
        print("  ### NON CONFERMATO: al passo di nascita non si vede `lam = LAM` su tutti gli")
        print("  ### archi col ripiego di `len(psi) < n`. La spiegazione non regge, e va detto.")
    print("=" * 96)
    OUT = os.path.join(FUORI, "_lambda_al_flash%s.json" % ("_vecchio" if sim else "_oggi"))
    io.open(OUT, "w", encoding="utf-8", newline=chr(10)).write(json.dumps(
        {"simulatore": os.path.basename(sim) if sim else "soliton_simulator.py",
         "LAM": LAM, "passo_nascita": nascita, "per_passo": fuori,
         "lam_medio_normali_min": min(normali) if normali else None,
         "lam_medio_normali_max": max(normali) if normali else None,
         "confermato": bool(q_n), "nmasse": S._NMASSE_VIDEO["n"], "sep": S._NMASSE_VIDEO["sep"]},
        indent=1, ensure_ascii=False, sort_keys=True, default=float))
    print("")
    print("scritto: " + OUT)
    return 0 if q_n else 1


if __name__ == "__main__":
    sys.exit(principale())
