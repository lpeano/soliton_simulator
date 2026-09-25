# -*- coding: utf-8 -*-
"""**IL PERCORSO VERO DI UN FLAG: `argv` -> `_cli()` -> `_applica_flag()` -> MODULO.**

> ### **Un sigillo che imposta il modulo a mano prova LA LEGGE, non IL FLAG.**

E' il difetto misurato il 2026-09-25: `--semina-matura` e `--mitosi-2lam` erano **MORTI da riga
di comando** *(assegnazione in `esegui_headless`, `global` dichiarato in `_applica_flag`, quindi
una **locale silenziosamente inerte**)* e i loro sigilli **passavano ugualmente** `7/7` e `8/8`,
perche' accendevano il flag **sul modulo**. L'ha trovato il sigillo del driver, non i due sigilli.

**COSA OFFRE, e perche' sta in UN SOLO POSTO:**

* `argv_del_driver(extra)` -- **CATTURA** la `sys.argv` che il driver costruisce per il
  simulatore, eseguendo il **testo del driver** fino all'ancora `S._applica_flag(a)`.
  **Non la ricostruisce:** ricostruirla sarebbe **una SECONDA FORMULA per la stessa cosa**, ed e'
  l'errore che questo repo inseguue da giorni. *(Era il codice inline di
  `_sigillo_driver_accende.py`: qui e' fattorizzato, e quel sigillo ora lo usa.)*
* `senza(argv, opzione)` -- la stessa argv **MENO** un'opzione, con l'asserzione che ci fosse.
* `carica_dal_cli(argv, nome)` -- importa il simulatore in un modulo **privato** e lo configura
  **passando dal suo `_cli()`**, non assegnando attributi.

**PERCHE' IL BRACCIO OFF SI FA TOGLIENDO L'OPZIONE:** i flag delle cure sono `store_true`.
**`--semina-matura=off` NON ESISTE.** L'unico OFF che il CLI ammette e' *«un comando che
DIMENTICA il flag»* -- che e' anche, esattamente, il difetto contro cui il sigillo del driver
monta la guardia.

**⚠ E IL DRIVER NON PUO' DARE IL BRACCIO OFF DELLE CURE OBBLIGATORIE:** le accende
**incondizionatamente**, senza `if`. **E' `NUDA = CAMPAGNA`, di proposito.**

ASCII puro.
"""
import io
import os
import sys

NL = chr(10)
_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, ".."))
DRIVER = os.path.join(RADICE, "csv", "_test_fork", "_scena_video.py")
SIM = os.path.join(RADICE, "soliton_simulator.py")

# L'ANCORA: il punto del driver in cui i flag sono stati applicati e non un passo di fisica e'
# ancora partito. Si cerca nel TESTO INTERO e si pretende UNICA (`STANDARD 9`).
ANCORA = "S._applica_flag(a)"

# Gli argomenti che il driver prende PRIMA delle opzioni. `1` e' il numero di frame: il taglio
# all'ancora avviene molto prima che serva.
def posizionali(dest):
    return ["_scena_video.py", "1", dest]


def argv_del_driver(extra=None, dest=None):
    """Esegue il TESTO del driver fino all'ancora e restituisce `(S, argv_sim)`.

    `argv_sim` e' la `sys.argv` **che il driver ha costruito per il simulatore**, catturata
    aggiungendo UNA riga al testo eseguito -- non ricostruita.
    `S` e' il modulo del simulatore **gia' configurato dal driver**: utile per chi vuole
    leggere lo stato effettivo (e' cio' che fa `_sigillo_driver_accende.py`).
    """
    t = io.open(DRIVER, encoding="utf-8").read()
    assert t.count(ANCORA) == 1, "ancora non unica nel driver: %d" % t.count(ANCORA)
    testa = t[:t.index(ANCORA) + len(ANCORA)] + NL + "_ARGV_SIM = list(sys.argv)" + NL
    g = {"__name__": "__main__", "__file__": DRIVER}
    vecchia = list(sys.argv)
    cwd = os.getcwd()
    os.chdir(RADICE)
    sys.argv = posizionali(dest or os.path.join(_QUI, "_scarto_cli")) + list(extra or [])
    try:
        exec(compile(testa, DRIVER, "exec"), g)
    finally:
        sys.argv = vecchia
        os.chdir(cwd)
    S = g.get("S") or sys.modules["soliton_simulator"]
    return S, list(g.get("_ARGV_SIM") or [])


def senza(argv, opzione):
    """La stessa argv MENO `opzione`, con l'asserzione che ci FOSSE.

    **L'asserzione e' il punto:** se un giorno il driver smettesse di passare quel flag, il
    braccio OFF diventerebbe **identico** al braccio ON e il sigillo passerebbe misurando
    NIENTE -- il falso PASS per mancanza di contrasto, gia' catalogato in `CLAUDE.md` par.9.
    """
    argv = list(argv)
    assert opzione in argv, ("l'argv del driver NON contiene %r: il braccio OFF sarebbe "
                            "IDENTICO all'ON, e il sigillo misurerebbe niente" % opzione)
    return [x for x in argv if x != opzione]


def carica_dal_cli(argv, nome="sim_cli", sim=None):
    """Importa il simulatore e lo configura **passando dal suo `_cli()`**.

    **Nessun attributo assegnato a mano:** si mette l'argv e si chiamano `_cli()` e
    `_applica_flag(a)`, cioe' **le due funzioni che il driver chiama**.
    Restituisce `(S, a)`.

    ⚠ **`_applica_flag` SEMINA ANCHE IL VUOTO** dal 2026-09-25 (`SCENA-1`:
    `net.semina(-1 if SEMINA_LAM else a.nodi)`). Non e' piu' una funzione di soli flag, e chi
    la chiama si ritrova un `S.net` gia' seminato: chi vuole un'altra scena si fa il proprio
    `S.Rete(...)`, come fa il driver stesso per le scene che non sono il vuoto.
    """
    import importlib.util as _iu
    sp = _iu.spec_from_file_location(nome, sim or SIM)
    S = _iu.module_from_spec(sp)
    sp.loader.exec_module(S)
    vecchia = list(sys.argv)
    sys.argv = list(argv)
    try:
        a = S._cli()
        S._applica_flag(a)
    finally:
        sys.argv = vecchia
    return S, a


def dichiara(S, nomi):
    """Le righe `STATO <nome> <valore>` per i flag richiesti, lette DAL MODULO."""
    return [(n, getattr(S, n, "ASSENTE")) for n in nomi]
