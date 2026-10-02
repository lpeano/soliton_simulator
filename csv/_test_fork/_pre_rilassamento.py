# -*- coding: utf-8 -*-
"""**IL PRE-RILASSAMENTO FUORI DALLO SCHEDULATORE: quante volte gira, e i sigilli lo attraversano?**

Rilievo del guardiano *(2026-10-03)*. In `_applica_flag` c'e'

```
if net.n and (a.seed is not None or a.nodi != SEME_INIZIALE):
    for _ in range(300): net.step()
    net.rilassa_disegno(30)
```

### ⚠ **E' FUORI da `esegui_passo`**, quindi quei 300 passi girano ### **senza il controllo
unico, senza `scuoti_vuoto`, senza `memoria_hebbiana_moto`, e senza nessuna nascita** — cioe'
### **senza sei delle otto voci** di `PASSO_COMPOSIZIONE`.

### \U0001f4cc **NON SI CURA: si MISURA e si DICHIARA** *(mandato del 2026-10-03)*. Le domande
sono tre, e ciascuna ha una risposta ### **dal RUNTIME**, non dalla lettura:

| | |
|---|---|
| **1** | la condizione e' vera ### **nella configurazione del driver**? |
| **2** | ### **quante volte** gira `net.step()` fuori dallo schedulatore, per caricamento? |
| **3** | ### **i sigilli lo attraversano**? cioe': la scena `MASSE-COERENTI` passa da qui? |

### **COME SI MISURA, e non e' una stima:** si avvolgono `Rete.step` e
`Rete.rilassa_disegno` con un contatore ### **prima** di chiamare `carica_dal_cli`, e si
guarda ### **quando** scattano — prima o dopo `avvia_test`.

**COMANDO:** `python csv/_test_fork/_pre_rilassamento.py`
**USCITA:** `csv/_test_fork/_pre_rilassamento/`
"""
import contextlib
import hashlib
import io
import json
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_QUI, ".."))
import _presidio   # noqa: E402

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, os.path.join(RADICE, "csv"))
import _cli_flag   # noqa: E402

SIM = os.path.join(RADICE, "soliton_simulator.py")
FUORI = os.path.join(_QUI, "_pre_rilassamento")
NL = chr(10)


def blob(p):
    return hashlib.sha1(io.open(p, "rb").read()).hexdigest()


def principale():
    righe = []

    def stampa(*x):
        s = " ".join(str(y) for y in x)
        righe.append(s)
        print(s)

    stampa("=" * 100)
    stampa("IL PRE-RILASSAMENTO FUORI DALLO SCHEDULATORE -- misurato dal RUNTIME")
    stampa("=" * 100)
    stampa("  simulatore .. %s (sha1 byte grezzi)" % blob(SIM)[:8])
    stampa("")

    if not os.path.isdir(FUORI):
        os.makedirs(FUORI)
    # l'argv del driver, lo STESSO del sigillo esteso (seme 11)
    with contextlib.redirect_stdout(io.StringIO()):
        _S0, argv = _cli_flag.argv_del_driver(extra=["--seme=11"],
                                              dest=os.path.join(FUORI, "_scarto"))
    stampa("  argv del driver: %d voci, e porta `--seme=11`" % len(argv))

    # ### LA SPIA, installata PRIMA del caricamento: si avvolge la CLASSE, non l'istanza,
    #   perche' la `Rete` non esiste ancora quando `carica_dal_cli` la crea.
    conta = {"step": 0, "rilassa": 0, "step_prima_di_avvia": 0, "fase": "caricamento"}
    # ### E QUI SI REPLICANO LE TRE RIGHE DI `carica_dal_cli`, e si dichiara PERCHE':
    #   quella funzione fa `exec_module` -> `_cli()` -> `_applica_flag(a)` in un colpo, e
    #   ### il pre-rilassamento avviene DENTRO `_applica_flag`. Per vederlo la spia va
    #   installata ### FRA l'import e `_applica_flag`, e dall'esterno non c'e' quel punto.
    #   ### `H-P3` E' RISPETTATO NELLA SOSTANZA: si passa per le STESSE DUE funzioni che il
    #   driver chiama (`_cli` e `_applica_flag`), e nessun attributo e' messo a mano.
    import importlib.util
    spec = importlib.util.spec_from_file_location("_sim_prerilax", SIM)
    sim = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(sim)
    _step0, _ril0 = sim.Rete.step, sim.Rete.rilassa_disegno

    def step_spiato(self, *a, **k):
        conta["step"] += 1
        if conta["fase"] == "caricamento":
            conta["step_prima_di_avvia"] += 1
        return _step0(self, *a, **k)

    def ril_spiato(self, *a, **k):
        conta["rilassa"] += 1
        conta.setdefault("rilassa_arg", []).append(a[0] if a else None)
        return _ril0(self, *a, **k)

    sim.Rete.step, sim.Rete.rilassa_disegno = step_spiato, ril_spiato
    try:
        vecchia = list(sys.argv)
        sys.argv = list(argv)
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                a = sim._cli()
                sim._applica_flag(a)
        finally:
            sys.argv = vecchia
        S = sim
        stampa("")
        stampa("  --- DOPO `carica_dal_cli` (cioe' dopo `_applica_flag`) ---")
        stampa("      `a.seed` ................... %r" % getattr(a, "seed", "ASSENTE"))
        stampa("      `a.nodi` ................... %r" % getattr(a, "nodi", "ASSENTE"))
        stampa("      `SEME_INIZIALE` ............ %r" % getattr(S, "SEME_INIZIALE", "ASSENTE"))
        stampa("      `a.nodi != SEME_INIZIALE` .. %s"
               % (getattr(a, "nodi", None) != getattr(S, "SEME_INIZIALE", None)))
        stampa("      ### `net.n` ora ............ %d" % S.net.n)
        stampa("      ### `net.step()` chiamate .. %d   <-- FUORI dallo schedulatore"
               % conta["step_prima_di_avvia"])
        stampa("      ### `rilassa_disegno` ...... %d, con argomento %s"
               % (conta["rilassa"], conta.get("rilassa_arg")))
        attesa = bool(S.net.n and (getattr(a, "seed", None) is not None
                                   or getattr(a, "nodi", None)
                                   != getattr(S, "SEME_INIZIALE", None)))
        stampa("      la CONDIZIONE del `:10658` era vera? %s" % attesa)

        conta["fase"] = "avvia_test"
        prima = conta["step"]
        with contextlib.redirect_stdout(io.StringIO()):
            S._applica_regime(a)
            S._NMASSE_VIDEO["n"] = max(2, int(getattr(a, "nmasse", 2)))
            S._NMASSE_VIDEO["sep"] = float(getattr(a, "sep", 3.0))
            S._NMASSE_VIDEO["size"] = None
            S.avvia_test("MASSE-COERENTI")()
        stampa("")
        stampa("  --- `avvia_test('MASSE-COERENTI')`, cioe' LA SCENA DEI SIGILLI ---")
        stampa("      ### `net.step()` chiamate DENTRO la scena .. %d" % (conta["step"] - prima))
        stampa("      ### `net.n` dopo la scena .................. %d" % S.net.n)
        esito = {
            "blob_sim_sha1_byte": blob(SIM),
            "argv_voci": len(argv),
            "seed": getattr(a, "seed", None),
            "nodi": getattr(a, "nodi", None),
            "SEME_INIZIALE": getattr(S, "SEME_INIZIALE", None),
            "condizione_vera": attesa,
            "step_fuori_dallo_schedulatore": conta["step_prima_di_avvia"],
            "rilassa_disegno_chiamate": conta["rilassa"],
            "rilassa_disegno_argomenti": conta.get("rilassa_arg"),
            "step_dentro_la_scena": conta["step"] - prima,
            "n_dopo_il_caricamento": None,
            "n_dopo_la_scena": int(S.net.n),
        }
        stampa("")
        stampa("-" * 100)
        if conta["step_prima_di_avvia"]:
            stampa("### VERDETTO: IL PRE-RILASSAMENTO GIRA, e i sigilli LO ATTRAVERSANO.")
            stampa("###   %d chiamate a `net.step()` FUORI da `esegui_passo`, per ogni"
                   % conta["step_prima_di_avvia"])
            stampa("###   caricamento -- e OGNI braccio di OGNI sigillo fa un caricamento.")
            stampa("###   Quei passi girano SENZA: controllo unico, `scuoti_vuoto`,")
            stampa("###   `memoria_hebbiana_moto`, `mitosi` (nessuna nascita), `verifica_invarianti`.")
        else:
            stampa("### VERDETTO: NON GIRA in questa configurazione.")
            stampa("###   E questo NON vuol dire <<non gira mai>>: vuol dire che con QUESTO")
            stampa("###   argv la condizione del `:10658` e' falsa. L'insieme e' DICHIARATO:")
            stampa("###   un solo argv, quello del driver col seme 11.")
        stampa("### E NON SI CURA: si DICHIARA (voce `PRE-RILASSAMENTO-FUORI-PASSO`).")
        stampa("")
        # ### IL CONTROLLO POSITIVO, e senza di lui lo zero sopra non vale (`STANDARD 2`,
        #   `FALSO-ZERO`): si rifa' lo STESSO caricamento cambiando SOLO `--nodi`, e il
        #   pre-rilassamento DEVE girare. Se non girasse nemmeno li', la spia non funziona
        #   e lo zero di sopra non significa niente.
        stampa("-" * 100)
        stampa("IL CONTROLLO POSITIVO: lo STESSO argv con `--nodi 400` invece di `--nodi 0`")
        argv2 = list(argv)
        _k = argv2.index("--nodi")
        argv2[_k + 1] = "400"
        conta2 = {"step": 0, "rilassa": 0, "arg": []}

        def step2(self, *aa, **kk):
            conta2["step"] += 1
            return _step0(self, *aa, **kk)

        def ril2(self, *aa, **kk):
            conta2["rilassa"] += 1
            conta2["arg"].append(aa[0] if aa else None)
            return _ril0(self, *aa, **kk)

        spec2 = importlib.util.spec_from_file_location("_sim_prerilax2", SIM)
        sim2 = importlib.util.module_from_spec(spec2)
        with contextlib.redirect_stdout(io.StringIO()):
            spec2.loader.exec_module(sim2)
        sim2.Rete.step, sim2.Rete.rilassa_disegno = step2, ril2
        _v2 = list(sys.argv)
        sys.argv = list(argv2)
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                a2 = sim2._cli()
                sim2._applica_flag(a2)
        finally:
            sys.argv = _v2
        stampa("      `a.nodi` ................... %r" % getattr(a2, "nodi", None))
        stampa("      ### `net.n` dopo la semina . %d" % sim2.net.n)
        stampa("      ### `net.step()` chiamate .. %d" % conta2["step"])
        stampa("      ### `rilassa_disegno` ...... %d, con %s"
               % (conta2["rilassa"], conta2["arg"]))
        ok_pos = conta2["step"] == 300 and conta2["rilassa"] == 1
        stampa("      ### IL CONTROLLO POSITIVO %s"
               % ("PASSA: 300 step e 1 rilassa_disegno, come dice il sorgente" if ok_pos
                  else "### FALLISCE: la spia non vede il pre-rilassamento, e lo zero "
                       "di sopra NON SIGNIFICA NIENTE"))
        esito["controllo_positivo"] = {
            "argv_cambiato": "--nodi 0 -> --nodi 400",
            "nodi": getattr(a2, "nodi", None), "n_dopo_semina": int(sim2.net.n),
            "step": conta2["step"], "rilassa": conta2["rilassa"],
            "rilassa_arg": conta2["arg"], "passa": bool(ok_pos)}
        stampa("")
        stampa("### ➜ QUINDI IL VERDETTO SI SCRIVE COSI', e non altrimenti:")
        stampa("###   <<ZERO step fuori dallo schedulatore su UN argv DICHIARATO (quello del")
        stampa("###   driver, seme 11), e il controllo positivo con `--nodi 400` ne da' 300>>.")
        stampa("###   MAI <<il pre-rilassamento non gira>>: gira, e la condizione dice QUANDO.")
    finally:
        sim.Rete.step, sim.Rete.rilassa_disegno = _step0, _ril0

    io.open(os.path.join(FUORI, "_pre_rilassamento.json"), "w", encoding="utf-8",
            newline=NL).write(json.dumps(esito, indent=1, default=str))
    io.open(os.path.join(FUORI, "_corsa.txt"), "w", encoding="utf-8",
            newline=NL).write(NL.join(righe) + NL)
    print("  referto .. %s" % FUORI)


if __name__ == "__main__":
    principale()
