# -*- coding: utf-8 -*-
"""FASE A — CONTARE il fallimento della guardia di `_psi_spin_prec`. **Nessuna cura, nessuna misura
della fisica: solo quante volte quel ramo e' davvero quello che gira.**

IL SOSPETTO (letto dal codice, riga 1829 sul blob b298677a):

    _ps = getattr(self, "psi_spin", None); _psp = getattr(self, "_psi_spin_prec", None)
    if CAMPO_SPINORIALE and _ps is not None and _psp is not None \\
       and len(_ps) == self.n and len(_psp) == self.n:
        signed = ... / DT        # <- il RITMO SPINORIALE a 4pi, da cui esce r e quindi dt_n = DT*r

`_psi_spin_prec` e' scritta a fine passo (riga 2647) con l'`n` di QUEL passo, e **non e' estesa alla
mitosi** (verificato: zero occorrenze di `_psi_spin_prec[src]` / `vstack(..._psi_spin_prec)`).
L'uguaglianza e' **ESATTA** (`==`), non `>=` come nella cache `cs`: piu' stretta, piu' facile da far
fallire. **Ma un ramo LETTO non e' un ramo MISURATO** (`CLAUDE.md` par.9), e il caso sarebbe
INNOCENTE se la riscrittura chiudesse il buco prima della lettura successiva.

C'E' UN TERZO ESITO, che il mandato non nomina e che va contato a parte: **prima** di quella guardia
`ritmo()` ne ha un'altra, su `_psi_prec`, con **RETURN ANTICIPATO** (`return np.ones(self.n)`). Se
scatta quella, il ramo 4pi **non viene nemmeno raggiunto** e `r` vale **1 ovunque**. Contarli
insieme direbbe "la guardia fallisce" in due casi fisicamente diversi.

PUREZZA: questo script **non modifica `soliton_simulator.py`**. Avvolge `Rete.ritmo` in un wrapper
che valuta le STESSE condizioni in sola lettura e poi delega all'originale: non cambia un byte del
risultato, non consuma RNG, non tocca lo stato.

LETTURA FISSATA PRIMA (dal mandato):
  * la guardia 4pi fallisce in **> 10 %** delle chiamate -> stesso bug della cache cs, la cura si
    giustifica;
  * fallisce in **< 10 %** -> **caso INNOCENTE**, si registra e NON si tocca nulla.
"""
import contextlib, importlib.util, io, os, sys
import numpy as np

RAD = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(RAD); sys.path.insert(0, RAD)
ARGS = ["--batch", "--nmasse", "3", "--sep", "8", "--passi", "1", "--ogni", "100000",
        "--db-ogni", "100000", "--campo-spinoriale", "--spinore-vivo", "--spinore-corretto",
        "--chi-core", "--calore-scal", "--deparam-orologio", "--verlet", "--cs-dinamico",
        "--fork-su2", "--fork-su2-mem", "--csv", os.path.join(os.environ.get("TMP", "."), "_cnt.csv")]
PASSI = 150
SEED = 1


def carica():
    spec = importlib.util.spec_from_file_location("sim_cnt", "soliton_simulator.py")
    M = importlib.util.module_from_spec(spec); sys.modules["sim_cnt"] = M
    sys.argv = ["soliton_simulator.py"] + ARGS
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(M)
        a = M._cli(); M._applica_regime(a); M._applica_flag(a)
    return M


def main():
    M = carica()
    print("=" * 104)
    print("FASE A - contatore della guardia di `_psi_spin_prec`  (CAMPO_SPINORIALE = %s)" % M.CAMPO_SPINORIALE)
    print("=" * 104)

    orig = M.Rete.ritmo
    log = []            # una riga per CHIAMATA di ritmo()
    passo_corr = {"k": 0}

    def wrap(self):
        n = self.n
        _pp = getattr(self, "_psi_prec", None)
        _ps = getattr(self, "psi_spin", None)
        _psp = getattr(self, "_psi_spin_prec", None)
        l_pp = -1 if _pp is None else len(_pp)
        l_ps = -1 if _ps is None else len(_ps)
        l_psp = -1 if _psp is None else len(_psp)
        anticipato = (_pp is None or l_pp != n)                       # return np.ones(n): 4pi mai raggiunto
        ok4pi = (M.CAMPO_SPINORIALE and _ps is not None and _psp is not None
                 and l_ps == n and l_psp == n)
        log.append((passo_corr["k"], n, l_pp, l_ps, l_psp, anticipato, ok4pi))
        return orig(self)

    M.Rete.ritmo = wrap

    net = M.Rete(SEED); net.semina(80)

    def passo():
        M.scuoti_vuoto(net); net.step(); net.mitosi(); net.rilassa_disegno(); net.memoria_hebbiana_moto()

    for _ in range(6):
        passo()
    Nc = M.massa_critica_collasso()
    for k in range(3):
        ang = 2 * np.pi * k / 3
        net.nuova_massa(int(Nc * 0.6), raggio=0.8,
                        centro=(8.0 * np.cos(ang), 8.0 * np.sin(ang), 0.0), fase=0.0)
    n_prima = net.n
    log.clear()                                    # si conta il REGIME, non il transitorio di scena
    for k in range(PASSI):
        passo_corr["k"] = k + 1
        passo()

    tot = len(log)
    ant = sum(1 for r in log if r[5])
    ok = sum(1 for r in log if (not r[5]) and r[6])
    ko = sum(1 for r in log if (not r[5]) and not r[6])
    # quale condizione fa fallire, fra quelle che ARRIVANO alla guardia 4pi
    solo_ps = sum(1 for r in log if (not r[5]) and not r[6] and r[3] != r[1] and r[4] == r[1])
    solo_psp = sum(1 for r in log if (not r[5]) and not r[6] and r[3] == r[1] and r[4] != r[1])
    entrambe = sum(1 for r in log if (not r[5]) and not r[6] and r[3] != r[1] and r[4] != r[1])
    assente = sum(1 for r in log if (not r[5]) and not r[6] and (r[3] < 0 or r[4] < 0))

    print("  scena: %d nodi prima dei %d passi contati, %d alla fine" % (n_prima, PASSI, net.n))
    print("  chiamate a ritmo() nei %d passi contati: %d  (%.2f per passo)"
          % (PASSI, tot, tot / max(PASSI, 1)))
    print()
    print("  ESITO DI OGNI CHIAMATA")
    print("    return ANTICIPATO su _psi_prec (r = 1 ovunque, il 4pi non e' raggiunto): %5d  = %6.2f %%"
          % (ant, 100.0 * ant / max(tot, 1)))
    print("    guardia 4pi PASSA  (ritmo spinoriale attivo)                           : %5d  = %6.2f %%"
          % (ok, 100.0 * ok / max(tot, 1)))
    print("    guardia 4pi FALLISCE (ricade sul ritmo SCALARE a 2pi)                  : %5d  = %6.2f %%"
          % (ko, 100.0 * ko / max(tot, 1)))
    print()
    print("  QUALE CONDIZIONE FALLISCE (fra le chiamate che arrivano alla guardia 4pi)")
    print("    solo len(psi_spin) != n        : %d" % solo_ps)
    print("    solo len(_psi_spin_prec) != n  : %d" % solo_psp)
    print("    entrambe                       : %d" % entrambe)
    print("    uno dei due ASSENTE (None)     : %d" % assente)
    print()
    print("  CAMPIONE - n, len(_psi_prec), len(psi_spin), len(_psi_spin_prec) a piu' passi")
    print("    passo |     n | len _psi_prec | len psi_spin | len _psi_spin_prec | esito")
    visti = set()
    for r in log:
        if r[0] in (1, 2, 3, 10, 30, 60, 100, PASSI) and r[0] not in visti:
            visti.add(r[0])
            es = "ANTICIPATO" if r[5] else ("4pi" if r[6] else "SCALARE 2pi")
            print("    %5d | %5d | %13d | %12d | %18d | %s" % (r[0], r[1], r[2], r[3], r[4], es))
    print()
    print("  ORDINE REALE: _psi_spin_prec e' riscritto PRIMA di essere riletto?")
    lp = getattr(net, "_psi_spin_prec", None)
    print("    a fine run: n = %d, len(_psi_spin_prec) = %s  -> %s"
          % (net.n, "None" if lp is None else len(lp),
             "allineato" if (lp is not None and len(lp) == net.n) else "DISALLINEATO"))
    print("    NB: la scrittura (riga ~2647) sta DENTRO step(), subito dopo la lettura (riga ~1829);")
    print("        la mitosi gira DOPO step(). Il contatore dice se questo basta a chiudere il buco.")
    print()
    print("=" * 104)
    pct = 100.0 * ko / max(tot, 1)
    print("  IL NUMERO CHE DECIDE: la guardia 4pi FALLISCE nel %.2f %% delle chiamate." % pct)
    if pct > 10.0:
        print("  LETTURA (fissata prima): > 10 %  ->  STESSO BUG DELLA CACHE cs. La cura e' giustificata.")
    else:
        print("  LETTURA (fissata prima): < 10 %  ->  CASO INNOCENTE. Si registra e NON si tocca nulla.")
    print("=" * 104)
    return 0


if __name__ == "__main__":
    sys.exit(main())
