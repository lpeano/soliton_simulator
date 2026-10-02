# -*- coding: utf-8 -*-
"""**IL SIGILLO DELLA REGOLA DI CONFRONTO ESTESA** *(decisione di Luca, 2026-10-02, via (b) passo 1)*.

> ### **Il PRIMO lavoro e' estendere il sigillo, non cambiare il codice:** senza, il cambiamento
> che poi si fa ### **non si vede**, e la via (a) e la via (b) sono ### **indistinguibili dai
> numeri.**

## CHE COSA PROVA, in tre bracci

| braccio | che cosa dimostra | come puo' FALLIRE |
|---|---|---|
| ### **A -- LA REGOLA** | ### **elenca che cosa confronta, e PERCHE'** *(classe per classe)*, e nomina ### **le grandezze che la regola di OGGI si perde** | se l'insieme nuovo **non contiene** `_g_peqn_mediana`, `ultima_prob_coppia` o `ultima_frac_antifase`, ### **la regola non ha fatto il suo lavoro** |
| ### **B -- IL CASO CHE DEVE FALLIRE** | su una COPIA del simulatore con ### **`_g_peqn_mediana` cambiata di UN ULP**: ### **la regola NUOVA deve CADERE, quella di OGGI NO** | se la nuova **non vede** la differenza, non serve a niente; ### **se la VECCHIA la vede, il caso non prova nulla** *(vorrebbe dire che era gia' coperta)* |
| ### **C -- L'INVOLUCRO** | due bracci sul simulatore ### **NON modificato** danno ### **ZERO differenze con ENTRAMBE le regole** | ### **senza questo, lo `0` del braccio `B` potrebbe voler dire «il banco e' rotto»** invece di «la regola vecchia non vede» |

### ⭐ **PERCHE' IL BRACCIO `C` NON E' FACOLTATIVO**
`STANDARD 1` lo dice: ### **un criterio di IDENTITA' fallisce rumorosamente col banco rotto; uno
di DIFFERENZA passa piu' facilmente PROPRIO col banco rotto.** Il braccio `B` chiede *«i due DEVONO
differire»*, quindi ### **prima vanno confrontati due bracci IDENTICI.**

## ✅ **PERCHE' `_g_peqn_mediana` E' IL CASO GIUSTO, e non una scelta comoda**

### **E' solo ASSEGNATA, mai LETTA da nessun codice** *(verificato su tutto il repo: le occorrenze
sono il simulatore, le sue copie, e i referti)*. ### ➜ **Quindi un ulp su di lei e' INERTE su
tutto il resto**: la differenza che il sigillo deve vedere e' ### **esattamente una, e nient'altro
si muove.** ### **Se il braccio `B` ne trovasse due, la copia non e' chirurgica e si dice.**

## ⚠ **E IL NOME DI QUESTO FILE E' UNA SCELTA, non un caso**

### **`_sigillo_*` e non `_sig_*`**, perche' `_presidio.avvia` ### **rifiuta di girare SOLO se il
nome comincia con `_sigillo_`** *(`csv/_presidio.py:121`)*. ### ⛔ **E i sei sigilli chiamati
`_sig_*` -- fra cui quelli dei COMMIT 1 e 2 del riordino -- NON sono coperti da quel rifiuto.**
E' `PRESIDIO-RIFIUTO-SOLO-SIGILLI`, e qui ### **invece di aggiungere un settimo scoperto, uso il
nome che il presidio protegge.**

COMANDO:  python csv/_seal_fork/_sigillo_confronto_esteso.py [--passi=72] [--seme=11]
USCITA:   `csv/_seal_fork/_sigillo_confronto_esteso/_sigillo_confronto_esteso.json` + `_corsa.txt`.
ASCII puro nel codice.
"""
import contextlib
import hashlib
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
import _confronto_nascita as CN  # noqa: E402

NL = chr(10)
SIM = os.path.join(RADICE, "soliton_simulator.py")
FUORI = os.path.join(RADICE, "csv", "_seal_fork", "_sigillo_confronto_esteso")
# L'ANCORA della copia guasta: si cerca per TESTO e si asserisce UNICA (`P1-quater`).
ANCORA = "self._g_peqn_mediana = float(np.median(self.peq))"
GUASTA = "self._g_peqn_mediana = float(np.nextafter(np.median(self.peq), np.inf))"


def blob(p):
    return hashlib.sha1(io.open(p, "rb").read()).hexdigest()


def copia_un_ulp(dest):
    """La COPIA con `_g_peqn_mediana` cambiata di UN ULP. Sostituzione ASSERITA, scritta in BINARIO.

    ### `np.nextafter(x, inf)` e' il float IMMEDIATAMENTE successivo: **un ulp esatto**, e non un
    numero scelto. ### **Non e' una perturbazione tarata: e' la PIU' PICCOLA possibile.**
    """
    t = io.open(SIM, encoding="utf-8", newline="").read()
    n = t.count(ANCORA)
    if n != 1:
        raise SystemExit("** l'ancora della copia guasta e' presente %d volte (attesa 1). "
                         "NON scrivo la copia. **" % n)
    io.open(dest, "wb").write(t.replace(ANCORA, GUASTA).encode("utf-8"))
    # ### E SI VERIFICA CHE LA COPIA DIFFERISCA SOLO LI': una copia non chirurgica renderebbe il
    #   braccio `B` privo di significato (misurerebbe DUE cose).
    a = t.split(NL)
    b = io.open(dest, encoding="utf-8", newline="").read().split(NL)
    if len(a) != len(b):
        raise SystemExit("** la copia ha %d righe invece di %d **" % (len(b), len(a)))
    diverse = [k + 1 for k, (x, y) in enumerate(zip(a, b)) if x != y]
    return diverse


def carica(nome, seme, sim=None):
    with contextlib.redirect_stdout(io.StringIO()):
        _S0, argv = _cli_flag.argv_del_driver(extra=["--seme=%d" % seme],
                                              dest=os.path.join(FUORI, "_scarto_" + nome))
        S, a = _cli_flag.carica_dal_cli(list(argv), nome=nome, sim=sim)
        S._applica_regime(a)
        S._NMASSE_VIDEO["n"] = max(2, int(getattr(a, "nmasse", 2)))
        S._NMASSE_VIDEO["sep"] = float(getattr(a, "sep", 3.0))
        S._NMASSE_VIDEO["size"] = None
        S.avvia_test("MASSE-COERENTI")()
    return S, S.net


def avanza(S, net, passi):
    with contextlib.redirect_stdout(io.StringIO()):
        for _ in range(passi):
            _passo.passo_pieno(S, net)
    return net


def principale():
    seme, passi = 11, 72
    for x in sys.argv[1:]:
        if x.startswith("--seme="):
            seme = int(x.split("=", 1)[1])
        elif x.startswith("--passi="):
            passi = int(x.split("=", 1)[1])
    if not os.path.isdir(FUORI):
        os.makedirs(FUORI)
    P = []

    def stampa(*x):
        r = " ".join(str(y) for y in x)
        P.append(r)
        print(r)

    stampa("=" * 104)
    stampa("SIGILLO DELLA REGOLA DI CONFRONTO ESTESA  (via (b) passo 1, decisione di Luca)")
    stampa("=" * 104)
    stampa("simulatore ..... %s" % blob(SIM)[:8])
    stampa("questo sigillo . %s" % blob(os.path.abspath(__file__))[:8])
    stampa("regola in ...... csv/_confronto_nascita.py  %s"
           % blob(os.path.join(RADICE, "csv", "_confronto_nascita.py"))[:8])
    stampa("seme %d   passi %d" % (seme, passi))
    stampa("")

    # ---------- la COPIA GUASTA, prima di tutto -----------------------------------------------
    dest = os.path.join(FUORI, "_sim_ulp.py")
    diverse = copia_un_ulp(dest)
    stampa("=" * 104)
    stampa("LA COPIA GUASTA: `_g_peqn_mediana` cambiata di UN ULP (`np.nextafter(..., inf)`)")
    stampa("=" * 104)
    stampa("  file ........... %s" % os.path.relpath(dest, RADICE).replace(chr(92), "/"))
    stampa("  blob ........... %s" % blob(dest)[:8])
    stampa("  righe DIVERSE .. %d   %s" % (len(diverse), diverse))
    chirurgica = (len(diverse) == 1)
    stampa("  ### CHIRURGICA: %s" % ("SI" if chirurgica else "NO -- il braccio B non prova nulla"))
    stampa("")

    # ---------- i tre bracci ------------------------------------------------------------------
    SA, nA = carica("cfr_A", seme)
    stampa("  braccio A: scena n = %d, archi = %d" % (nA.n, len(nA.i)))
    _cli_flag.dichiara_configurazione(SA, stampa)
    stampa("")
    avanza(SA, nA, passi)
    fa, quali = CN.foto(SA, nA)
    oggi = CN.regola_di_oggi(SA, nA)

    SC, nC = carica("cfr_C", seme)
    avanza(SC, nC, passi)
    fc, _ = CN.foto(SC, nC)

    SB, nB = carica("cfr_B", seme, sim=dest)
    avanza(SB, nB, passi)
    fb, _ = CN.foto(SB, nB, sorgente=dest)

    # BRACCIO A -------------------------------------------------------------------------------
    stampa("=" * 104)
    stampa("BRACCIO A -- LA REGOLA: che cosa confronta, e PERCHE'")
    stampa("=" * 104)
    per_classe = {}
    for k, q in quali.items():
        per_classe.setdefault(q["classe"], []).append(k)
    for cl in ("registro", "contatore", "scritta-nella-nascita"):
        stampa("  %-24s %d" % (cl, len(per_classe.get(cl, []))))
    stampa("  " + "-" * 94)
    stampa("  ### TOTALE nell'insieme ........... %d" % len(quali))
    stampa("  ### scattate nella foto ........... %d" % len(fa))
    nuove = sorted(k for k in quali if k not in oggi)
    stampa("  ### che la regola di OGGI SI PERDE . %d" % len(nuove))
    for k in nuove:
        stampa("      ### %-26s %s" % (k, quali[k]["perche"][:62]))
    mai = sorted(k for k in quali if k not in fa)
    stampa("  grandezze dell'insieme MAI apparse: %d   %s" % (len(mai), ", ".join(mai)))
    stampa("      (non e' un difetto: una grandezza di un ramo spento non esiste. Si DICE.)")
    tre = ("_g_peqn_mediana", "ultima_prob_coppia", "ultima_frac_antifase")
    presenti = [k for k in tre if k in quali]
    stampa("")
    stampa("  ### LE TRE SCOPERTE DAL CONTRATTO, sono nell'insieme? %s"
           % ("  ".join("%s=%s" % (k, "SI" if k in quali else "NO") for k in tre)))
    A_ok = len(presenti) == 3
    stampa("  ### BRACCIO A: %s" % ("PASSA" if A_ok else "FALLISCE -- la regola non le prende"))
    stampa("")

    # BRACCIO C -------------------------------------------------------------------------------
    stampa("=" * 104)
    stampa("BRACCIO C -- L'INVOLUCRO: due bracci sul simulatore NON modificato")
    stampa("=" * 104)
    dC_n = CN.confronta(fa, fc)
    dC_o = CN.confronta({k: v for k, v in fa.items() if k in oggi},
                        {k: v for k, v in fc.items() if k in oggi})
    stampa("  con la regola NUOVA ... differenze: %d" % len(dC_n))
    stampa("  con la regola di OGGI  differenze: %d" % len(dC_o))
    for d in dC_n[:8]:
        stampa("      %s" % d)
    C_ok = (not dC_n) and (not dC_o)
    stampa("  ### BRACCIO C: %s" % ("PASSA -- il banco e' inerte" if C_ok else
                                    "FALLISCE -- il banco NON e' inerte, e il braccio B non si legge"))
    stampa("")

    # BRACCIO B -------------------------------------------------------------------------------
    stampa("=" * 104)
    stampa("BRACCIO B -- IL CASO CHE DEVE FALLIRE: un ULP su `_g_peqn_mediana`")
    stampa("=" * 104)
    dB_n = CN.confronta(fa, fb)
    dB_o = CN.confronta({k: v for k, v in fa.items() if k in oggi},
                        {k: v for k, v in fb.items() if k in oggi})
    stampa("  con la regola NUOVA ... differenze: %d" % len(dB_n))
    for d in dB_n:
        stampa("      ### %s" % d)
    stampa("  con la regola di OGGI  differenze: %d" % len(dB_o))
    for d in dB_o:
        stampa("      %s" % d)
    solo_quella = (len(dB_n) == 1 and dB_n[0]["nome"] == "_g_peqn_mediana")
    B_ok = solo_quella and (not dB_o)
    stampa("")
    stampa("  la regola NUOVA vede ESATTAMENTE `_g_peqn_mediana` e nient'altro? %s"
           % ("SI" if solo_quella else "NO"))
    stampa("  la regola di OGGI NON la vede? ................................. %s"
           % ("SI" if not dB_o else "NO"))
    stampa("  ### BRACCIO B: %s" % ("PASSA" if B_ok else "FALLISCE"))
    stampa("")

    # VERDETTO --------------------------------------------------------------------------------
    stampa("=" * 104)
    passa = A_ok and B_ok and C_ok and chirurgica
    stampa("### IL SIGILLO %s   (A %s · B %s · C %s · copia chirurgica %s)"
           % ("PASSA" if passa else "FALLISCE",
              "OK" if A_ok else "NO", "OK" if B_ok else "NO", "OK" if C_ok else "NO",
              "OK" if chirurgica else "NO"))
    stampa("=" * 104)

    ref = {"passa": bool(passa),
           "blob_sim_sha1_byte": blob(SIM),
           "blob_sigillo": blob(os.path.abspath(__file__)),
           "blob_regola": blob(os.path.join(RADICE, "csv", "_confronto_nascita.py")),
           "blob_copia_ulp": blob(dest),
           "seme": seme, "passi": passi,
           "copia_chirurgica": bool(chirurgica), "righe_diverse_nella_copia": diverse,
           "braccio_A": {"passa": bool(A_ok), "totale_insieme": len(quali),
                         "scattate": len(fa),
                         "per_classe": {k: sorted(v) for k, v in per_classe.items()},
                         "che_la_regola_di_oggi_si_perde": nuove,
                         "mai_apparse": mai,
                         "le_tre_scoperte_sono_nell_insieme": {k: (k in quali) for k in tre},
                         "perche": {k: quali[k]["perche"] for k in quali}},
           "braccio_C": {"passa": bool(C_ok), "diff_nuova": dC_n, "diff_oggi": dC_o},
           "braccio_B": {"passa": bool(B_ok), "diff_nuova": dB_n, "diff_oggi": dB_o,
                         "solo_g_peqn_mediana": bool(solo_quella)}}
    io.open(os.path.join(FUORI, "_sigillo_confronto_esteso.json"), "w", encoding="utf-8",
            newline=NL).write(json.dumps(ref, indent=1, default=str))
    io.open(os.path.join(FUORI, "_corsa.txt"), "w", encoding="utf-8",
            newline=NL).write(NL.join(P) + NL)
    return 0 if passa else 1


if __name__ == "__main__":
    sys.exit(principale())
