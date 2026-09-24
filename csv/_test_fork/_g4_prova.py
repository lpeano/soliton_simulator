# -*- coding: utf-8 -*-
"""G4 — LA PROVA DI SPEGNIMENTO DELLA MEMORIA DEL MOTO, col BILANCIO COMPLETO di `d0`.

⚠ NON MODIFICA NE' IL SIMULATORE NE' IL DRIVER. E' un INVOLUCRO: avvolge `_applica_flag` per
  impostare `MEM_MOTO` SUL MODULO, e poi esegue il driver com'e' con `runpy`.

⚠ SCRITTO SUI CINQUE PATTERN STANDARD di `doc/PATTERN_DI_PROVA.md`.

PERCHE' IL BILANCIO, e non basta la traccia degli scrittori: in `G3` (`Z107`) **il saldo di tutti
  gli scrittori vale `-1.6e+03`** -- mille volte meno dei singoli termini -- **e `med d0`
  RADDOPPIA lo stesso**. **La crescita NON viene da cio' che la traccia conta.**

IL TERMINE MANCANTE, TROVATO DAL SORGENTE E NON SUPPOSTO: `_smp_chiudi()` (`:3677`) fa
      self.d0 = v + self._smorza(v, dx, 'd0_passo')
  cioe' **RISCRIVE TUTTO `d0` a fine passo**, e **NON ha nessuna chiamata a `_traccia_d0`
  attorno**. **E' una scrittura completamente non tracciata.** Qui si misura avvolgendo
  `_smorza` e contando **solo** le chiamate con `quale == 'd0_passo'` *(le altre, se ci fossero,
  starebbero DENTRO un sito gia' tracciato e si conterebbero due volte)*.

E GLI ALTRI DUE TERMINI CHE LA TRACCIA NON PUO' VEDERE:
  * **le NASCITE** -- mitosi e Schwinger **concatenano**: gli archi nuovi entrano **con un loro
    valore di `d0`**, non come variazione di un arco esistente;
  * **le MORTI** -- gli archi spezzati **spariscono** col loro `d0`. *(Se muoiono i corti e
    nascono i lunghi, la mediana sale **senza che nessun arco cresca**.)*

IL CRITERIO DI CHIUSURA, SCRITTO PRIMA:
      Delta(somma di `d0`) nel passo = scritture + freno + (nascite - morti)    entro 1e-9 relativo
  **Se non chiude, manca un termine: si DICHIARA, e la prova non si legge finche' non si trova.**

  ⚠ E `nascite - morti` si misura **AL SITO CHE CONCATENA**, come `Σ(dopo) - Σ(prima)`,
    **non** come somma dei `d0` degli archi nati/morti letta a inizio e fine passo. La prima
    versione faceva cosi' e **NON CHIUDEVA** *(residuo relativo `8.0e-05`)*: un arco nato viene
    poi **modificato dalle scritture**, che il bilancio conta gia' a parte, e leggerlo a fine
    passo lo conta **due volte**. **Il giro corto lo ha preso in 43 s invece che in mezz'ora.**

  ⚠ E C'E' UNA SECONDA GUARDIA: **il SALTO fra la fine di un passo e l'inizio del successivo.**
    Fra i due, il driver chiama `diagnostica`/`campo_spaziale`/`pozzo_grafo`. Se una di quelle
    toccasse `d0`, **il bilancio PER PASSO chiuderebbe lo stesso** e il difetto sarebbe
    **invisibile**. Si misura, invece di darlo per scontato.

I MODI:
  --controllo    120 passi a flag INVARIATO: snapshot contro snapshot con `_val600` **e** il
                 bilancio che chiude. Se non passa, LA PROVA NON SI FA.
  --riferimento  600 passi, `MEM_MOTO` ACCESO, con la traccia completa. **Serve: senza il freno e
                 le nascite misurate NEL BRACCIO ACCESO, il confronto non regge.**
  --spegni       600 passi, `MEM_MOTO = False` (la sola scrittura su `d0`).
  --fase-2pi     600 passi, `FASE_2PI = True`: `phi` su [0, 2pi). La CURA di `D35`.
  --fase-2pi-corto  120 passi, lo STESSO braccio: **STANDARD 7**, il giro corto prima
                 del giro vero, per misurare il COSTO prima di spenderlo.
  --spegni-tutto 600 passi, `MEM_MOTO_TUTTO = False`: **L'INTERO BLOCCO**, spostamento di
                 fase compreso. E' `G4-bis`, e la condizione che lo ha attivato e' `Z109`:
                 spento `MEM_MOTO`, `d0` cresce lo stesso (rapporto 1.1607).
  --corto        aggiunge `--passi` ridotti: il giro CORTO prima del giro vero (proposta IN PROVA).
ASCII PURO.
"""
import gzip
import hashlib
import io
import os
import pickle
import runpy
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, RADICE)
DRIVER = os.path.join(RADICE, "csv", "_test_fork", "_scena_video.py")
RIF120 = os.path.join(RADICE, "csv", "_test_fork", "_val600", "scena_000120.pkl.gz")
BASE = np.int64(1) << np.int64(32)

COMUNE = ["--sep=4.0", "--serie=20", "--chi-basc=on", "--chi-coop=on", "--scala-min=off",
          "--coes-adim=on", "--peq-esatto=on", "--peq-nascita-locale=on",
          "--scala-min-passo=on", "--coes-causale=on", "--anom-simm=on", "--invarianti=on"]
CONCATENANO = ("S01_archi_nuovi", "S06_mitosi", "S07_schwinger")


# ------------------------------------------------------------------ IL BILANCIO, isolato
def bilancio(inizio, fine, scritture, freno, concat):
    """Il residuo del bilancio e il suo valore RELATIVO.

    ⚠ IL TERZO TERMINE E' `concat`, NON «nascite meno morti» misurate a inizio/fine
      passo. La prima versione usava quelle, e **NON CHIUDEVA**: residuo relativo `8.0e-05`.
      **Il giro corto lo ha preso in 43 s invece che in mezz'ora** *(proposta `IN PROVA`)*.
      **LA CAUSA, e il dato che la indica: il passo 2, con ZERO nascite e ZERO morti, chiudeva a
      `1.8e-14`; solo i passi con nascite o morti avevano residuo.** Un arco che NASCE viene poi
      **modificato dalle scritture**, che il bilancio conta gia' a parte: usare il suo `d0` a
      FINE passo lo conta **due volte**. Lo stesso, col segno opposto, per chi muore.
      **La forma esatta e' `Σ(dopo) - Σ(prima)` AL SITO CHE CONCATENA**: e' nascite meno
      morti **nell'istante giusto**, e non interferisce con nessuna scrittura.

    ⚠ Il denominatore NON e' `Delta` (che puo' essere ~0 per cancellazione e farebbe esplodere
      il relativo): e' la **scala dei termini**, cioe' la somma dei loro moduli. Un residuo si
      giudica contro **quanto materiale e' passato**, non contro quanto e' rimasto.
    """
    delta = fine - inizio
    previsto = scritture + freno + concat
    res = delta - previsto
    scala = (abs(scritture) + abs(freno) + abs(concat) + abs(delta))
    return delta, previsto, res, (abs(res) / scala if scala > 0 else 0.0)


def collaudo(W):
    """`P1-sexies`: il bilancio su un caso a risposta NOTA, e il caso che DEVE fallire."""
    W("COLLAUDO DEL BILANCIO su casi a RISPOSTA NOTA (`P1-sexies`), PRIMA di misurare\n")
    W("-" * 100 + "\n")
    e = []
    # un passo costruito a mano: tre archi esistenti, uno nasce, uno muore
    d0_in = np.array([1.0, 2.0, 3.0])                 # somma 6.0
    scritt = +0.5 - 0.2 + 0.1                         # scritture element-wise = +0.4
    fren = +0.3                                       # il freno aggiunge 0.3
    nasce = 5.0                                       # un arco nasce con d0 = 5.0
    muore = 2.0                                       # uno muore, portandosi via 2.0
    concat = nasce - muore                            # cio' che il sito che CONCATENA sposta
    fine = float(np.sum(d0_in)) + scritt + fren + concat
    delta, previsto, res, rel = bilancio(float(np.sum(d0_in)), fine, scritt, fren, concat)
    ok1 = (abs(res) < 1e-12)
    W("K1 bilancio COMPLETO su un caso noto -> residuo %.3e, atteso 0 -> %s\n"
      % (res, "OK" if ok1 else "*** NON CHIUDE su un caso costruito a mano ***"))
    e.append(ok1)

    # IL CASO CHE DEVE FALLIRE: lo stesso bilancio SENZA le nascite.
    _d, _p, res2, rel2 = bilancio(float(np.sum(d0_in)), fine, scritt, fren, -muore)
    ok2 = (abs(res2) > 1e-9) and (rel2 > 1e-9)
    W("K2 IL CASO CHE DEVE FALLIRE: lo stesso bilancio SENZA le nascite\n")
    W("     residuo %.3e (relativo %.3e), atteso NON nullo -> %s\n"
      % (res2, rel2, "OK: il criterio VEDE il termine mancante"
         if ok2 else "*** CIECO: un termine mancante passerebbe ***"))
    e.append(ok2)

    # e il caso che deve fallire per le MORTI
    _d, _p, res3, rel3 = bilancio(float(np.sum(d0_in)), fine, scritt, fren, nasce)
    ok3 = (abs(res3) > 1e-9)
    W("K3 IL CASO CHE DEVE FALLIRE: senza le MORTI -> residuo %.3e -> %s\n"
      % (res3, "OK" if ok3 else "*** CIECO ***"))
    e.append(ok3)

    # e il caso che deve fallire per il FRENO -- e' il termine che in G3 mancava davvero
    _d, _p, res4, rel4 = bilancio(float(np.sum(d0_in)), fine, scritt, 0.0, concat)
    ok4 = (abs(res4) > 1e-9)
    W("K4 IL CASO CHE DEVE FALLIRE: senza il FRENO -> residuo %.3e -> %s\n"
      % (res4, "OK" if ok4 else "*** CIECO ***"))
    e.append(ok4)

    # il denominatore NON deve esplodere quando Delta ~ 0 per cancellazione
    _d, _p, res5, rel5 = bilancio(10.0, 10.0, +1000.0, -1000.0, 0.0)
    ok5 = (rel5 < 1e-12)
    W("K5 cancellazione (`Delta = 0` con termini enormi) -> relativo %.3e, NON esplode -> %s\n"
      % (rel5, "OK" if ok5 else "*** il denominatore e' sbagliato ***"))
    e.append(ok5)

    ok = all(e)
    W("-" * 100 + "\n")
    W("  -> il bilancio %s\n\n" % ("PASSA i collaudi: si misura" if ok else "*** NON PASSA ***"))
    return ok


def chiavi(net):
    return (np.asarray(net.i, dtype=np.int64) * BASE + np.asarray(net.j, dtype=np.int64))


def confronta_snap(p_a, p_b, W):
    """Pattern 4: SNAPSHOT contro SNAPSHOT, senza cast dei complessi."""
    def leggi(p):
        with gzip.open(p, "rb") as f:
            return pickle.load(f)["attrs"]
    a, b = leggi(p_a), leggi(p_b)
    ug = dv = ass = 0
    nomi = []
    for k in sorted(set(a) | set(b)):
        if k not in a or k not in b:
            ass += 1; nomi.append("%s(in uno solo)" % k); continue
        aa = np.asarray(a[k]); bb = np.asarray(b[k])
        if aa.shape != bb.shape:
            dv += 1; nomi.append("%s(shape %s!=%s)" % (k, aa.shape, bb.shape)); continue
        if aa.dtype.kind in "fc" or bb.dtype.kind in "fc":
            d = float(np.max(np.abs(aa - bb))) if aa.size else 0.0
            if d == 0.0:
                ug += 1
            else:
                dv += 1; nomi.append("%s(max|d|=%.3e)" % (k, d))
        else:
            if np.array_equal(aa, bb):
                ug += 1
            else:
                dv += 1; nomi.append(k)
    W("  campi UGUALI %d   DIVERSI %d   non confrontati %d\n" % (ug, dv, ass))
    if nomi:
        W("  i diversi: %s\n" % ", ".join(nomi[:10]))
    return ug, dv


def installa(S, spegni_mem, spegni_tutto=False, wrap2pi=False, fase2pi=False,
             cura2=False):
    """Avvolge tutto cio' che serve. PURE-READ tranne l'unico flag che il mandato ammette."""
    stato = {"passi": [], "conti": {}, "freno": {}, "aperto": None, "n_passo": 0,
             "fine_prec": None}

    # --- 1. il FLAG, sul modulo, DOPO che il driver ha applicato i suoi
    orig_flag = S._applica_flag
    visto = {"chiamate": 0, "dopo": None, "dopo_tutto": None}

    def _wrap_flag(a):
        r = orig_flag(a)
        visto["chiamate"] += 1
        if spegni_mem:
            S.MEM_MOTO = False
        if wrap2pi:
            # [D34, 2026-09-22] LA CURA DEL RITMO. Sigillo 4/4: byte-inerte spenta,
            # e accesa CAMBIA (104 campi). Il default nel sorgente resta False.
            S.RITMO_WRAP_2PI = True
        if cura2:
            # [CURA 2] la cura IN PROVA si accende sul modulo, DOPO che il driver ha
            # applicato i suoi flag. `RITMO_WRAP_2PI` resta acceso dall'argv del driver:
            # il confronto e' con `_cura1_corto`, che ha la STESSA configurazione e questo
            # flag SPENTO -- un interruttore solo di differenza.
            S.TEMPO_UNICO_MITOSI = True
        if fase2pi:
            # [FASE_2PI, 2026-09-22] `phi` come fase ORDINARIA su [0, 2pi). Sigillo
            # `_sigillo_fase_2pi.py` **6/6** sul blob `445e2896`: byte-inerte spenta
            # (206 campi identici), e accesa `max(phi)` passa da 12.565546 a 6.282066.
            S.FASE_2PI = True
        if spegni_tutto:
            # [G4-bis, 2026-09-22] L'INTERO blocco, spostamento di fase compreso. Sigillo
            # `_sigillo_mem_moto_tutto.py` **10/10** sul blob `21e3a3dc`.
            S.MEM_MOTO_TUTTO = False
        visto["dopo"] = bool(S.MEM_MOTO)
        visto["dopo_tutto"] = bool(getattr(S, "MEM_MOTO_TUTTO", True))
        return r
    S._applica_flag = _wrap_flag

    # --- 2. gli SCRITTORI (la traccia di `Z102`/`Z107`)
    S.TRACCIA_D0 = True

    def traccia(self, sito, prima, pavimento=None):
        c = stato["conti"].setdefault(
            sito, dict(su=0.0, giu=0.0, n_su=0, n_giu=0, giri=0, salta=0))
        c["giri"] += 1
        dopo = np.asarray(self.d0, dtype=float)
        pri = np.asarray(prima, dtype=float)
        if len(pri) != len(dopo):
            # ⚠ NON si salta: `Σ(dopo) - Σ(prima)` e' ESATTAMENTE cio' che il sito
            #   sposta -- nascite meno morti NELL'ISTANTE GIUSTO. Saltare qui era il difetto che
            #   faceva non chiudere il bilancio (residuo `8.0e-05`).
            c["salta"] += 1
            stato["concat"] = stato.get("concat", 0.0) + float(np.sum(dopo) - np.sum(pri))
            return
        dx = dopo - pri
        c["su"] += float(np.sum(dx[dx > 0.0]))
        c["giu"] += float(np.sum(dx[dx < 0.0]))
        c["n_su"] += int(np.sum(dx > 0.0)); c["n_giu"] += int(np.sum(dx < 0.0))
        stato["scritture"] = stato.get("scritture", 0.0) + float(np.sum(dx))
    S.Rete._traccia_d0 = traccia

    # --- 3. IL FRENO. `_smp_chiudi` riscrive `d0` SENZA traccia: si prende da `_smorza`.
    orig_sm = S.Rete._smorza

    def _wrap_smorza(self, prima, dx, quale):
        eff = orig_sm(self, prima, dx, quale)
        c = stato["freno"].setdefault(quale, dict(agg=0.0, dx=0.0, giri=0))
        _e = np.atleast_1d(np.asarray(eff, dtype=float))
        _d = np.atleast_1d(np.asarray(dx, dtype=float))
        if _e.shape == _d.shape:
            agg = float(np.sum(_e - _d))
            c["agg"] += agg; c["dx"] += float(np.sum(_d))
            # ⚠ SOLO `d0_passo` entra nel BILANCIO: le altre chiamate, se ci fossero, starebbero
            #   DENTRO un sito gia' tracciato e si conterebbero DUE VOLTE.
            if quale == "d0_passo":
                stato["freno_passo"] = stato.get("freno_passo", 0.0) + agg
        # [V8/V9, richiesta di Luca 2026-09-24] LA DISTRIBUZIONE DI |dx|/d, SENZA UN RUN IN PIU'.
        #   L'involucro vede GIA' ogni coppia `(dx, prima)`: e' il numero che decide fra la forma
        #   PIANA `exp(x)` e la forma `1 + tanh(x)` della cura di `D31` (scheda 11, par.4-quater).
        #     |dx|/d << 1  -> le due forme sono indistinguibili, e `tanh` e' migliore su tutto
        #     |dx|/d ~ 1   -> il tetto di `tanh` (RADDOPPIA) comincia a mordere
        #     |dx|/d > 2   -> con la forma di Ito una SALITA FAREBBE SCENDERE (per questo e' uscita)
        #   SI SEPARANO SALITE E DISCESE: oggi il freno tocca SOLO le discese, quindi una
        #   distribuzione unica mescolerebbe cio' che e' frenato con cio' che non lo e'.
        _p = np.atleast_1d(np.asarray(prima, dtype=float))
        if _d.shape == _p.shape and _d.size:
            _x = np.abs(_d) / np.maximum(_p, 1e-300)
            for _et, _m in (("salite", _d > 0.0), ("discese", _d < 0.0)):
                if not _m.any():
                    continue
                v = stato.setdefault("ratio", {}).setdefault(
                    _et, {"campioni": [], "n": 0, "gt05": 0, "gt1": 0, "gt2": 0, "max": 0.0})
                xs = _x[_m]
                v["n"] += int(xs.size)
                v["gt05"] += int(np.sum(xs > 0.5))
                v["gt1"] += int(np.sum(xs > 1.0))
                v["gt2"] += int(np.sum(xs > 2.0))
                v["max"] = max(v["max"], float(xs.max()))
                # CAMPIONE per i quantili: tenerli TUTTI sarebbe centinaia di milioni di valori.
                # Si prende un sottocampione REGOLARE (non casuale: niente RNG da consumare, e
                # nessuna dipendenza dal seme), dichiarato nel referto.
                if len(v["campioni"]) < 400:
                    v["campioni"].append(xs[::max(1, xs.size // 2000)].astype(float))
        c["giri"] += 1
        return eff
    S.Rete._smorza = _wrap_smorza

    # --- 4. NASCITE e MORTI: fotografia delle CHIAVI a inizio e fine passo
    orig_scuoti = S.scuoti_vuoto
    orig_mem = S.Rete.memoria_hebbiana_moto

    def _wrap_scuoti(net, *a, **k):
        stato["aperto"] = (chiavi(net).copy(), np.asarray(net.d0, dtype=float).copy())
        stato["scritture"] = 0.0
        stato["freno_passo"] = 0.0
        stato["concat"] = 0.0
        return orig_scuoti(net, *a, **k)
    S.scuoti_vuoto = _wrap_scuoti

    def _wrap_mem(self, *a, **k):
        r = orig_mem(self, *a, **k)
        ap = stato["aperto"]
        if ap is not None:
            k0, v0 = ap
            k1 = chiavi(self); v1 = np.asarray(self.d0, dtype=float)
            vivi0 = np.isin(k0, k1, assume_unique=False)
            vivi1 = np.isin(k1, k0, assume_unique=False)
            morti = float(np.sum(v0[~vivi0])); nati = float(np.sum(v1[~vivi1]))
            inizio = float(np.sum(v0)); fine = float(np.sum(v1))
            sc = stato.get("scritture", 0.0); fr = stato.get("freno_passo", 0.0)
            cc = stato.get("concat", 0.0)
            d, p, res, rel = bilancio(inizio, fine, sc, fr, cc)
            # ⚠ LA GUARDIA DEL SALTO: fra la FINE di un passo e l'INIZIO del successivo il
            #   driver chiama `diagnostica`/`campo_spaziale`/`pozzo_grafo`. Se una di quelle
            #   toccasse `d0`, il bilancio PER PASSO chiuderebbe lo stesso e il difetto sarebbe
            #   INVISIBILE. Qui si misura, invece di darlo per scontato.
            salto = (inizio - stato["fine_prec"]) if stato["fine_prec"] is not None else 0.0
            stato["fine_prec"] = fine
            stato["salto_tot"] = stato.get("salto_tot", 0.0) + salto
            stato["n_passo"] += 1
            stato["passi"].append(
                dict(passo=stato["n_passo"], inizio=inizio, fine=fine, delta=d,
                     scritture=sc, freno=fr, nati=nati, morti=morti,
                     concat=cc, salto=salto,
                     n_nati=int(np.sum(~vivi1)), n_morti=int(np.sum(~vivi0)),
                     med_nati=float(np.median(v1[~vivi1])) if np.any(~vivi1) else float("nan"),
                     med_morti=float(np.median(v0[~vivi0])) if np.any(~vivi0) else float("nan"),
                     med_vivi=float(np.median(v1)), residuo=res, rel=rel))
            stato["aperto"] = None
        return r
    S.Rete.memoria_hebbiana_moto = _wrap_mem
    return stato, visto


def scrivi(stato, visto, dest, W, blob, seme, mem):
    """Le tabelle, GENERATE DA CODICE (`P1-ter`), in `txt` e `csv`, con blob e seme (`P6`)."""
    p_txt = os.path.join(dest, "BILANCIO_d0.txt")
    p_csv = os.path.join(dest, "BILANCIO_d0.csv")
    P = stato["passi"]
    with io.open(p_csv, "w", encoding="utf-8", newline="\n") as f:
        f.write("# blob=%s seme=%s MEM_MOTO=%s\n" % (blob, seme, mem))
        f.write("passo,inizio,fine,delta,scritture,freno,concat,salto,nati,morti,"
                "n_nati,n_morti,med_nati,med_morti,med_vivi,residuo,residuo_rel\n")
        for r in P:
            f.write("%d,%.9e,%.9e,%.9e,%.9e,%.9e,%.9e,%.9e,%.9e,%.9e,%d,%d,"
                    "%.9e,%.9e,%.9e,%.9e,%.9e\n"
                    % (r["passo"], r["inizio"], r["fine"], r["delta"], r["scritture"],
                       r["freno"], r["concat"], r["salto"], r["nati"], r["morti"],
                       r["n_nati"], r["n_morti"], r["med_nati"], r["med_morti"],
                       r["med_vivi"], r["residuo"], r["rel"]))
    with io.open(p_txt, "w", encoding="utf-8", newline="\n") as f:
        f.write("# G4 -- IL BILANCIO DI `d0`, con MEM_MOTO=%s\n" % mem)
        f.write("# blob simulatore (sha1 byte grezzi)=%s  seme=%s  passi=%d\n"
                % (blob, seme, len(P)))
        f.write("# CRITERIO, scritto PRIMA: Delta(somma d0) = scritture + freno + nati - morti,\n")
        f.write("#   entro 1e-9 RELATIVO alla scala dei termini.\n\n")
        if not P:
            f.write("*** nessun passo registrato ***\n")
            return 0.0, False
        rel = np.array([r["rel"] for r in P])
        chiude = bool(np.max(rel) < 1e-9)
        f.write("IL BILANCIO CHIUDE? residuo relativo: max %.3e, mediano %.3e su %d passi\n"
                % (float(np.max(rel)), float(np.median(rel)), len(P)))
        f.write("  -> %s\n\n" % ("CHIUDE" if chiude else
                                 "*** NON CHIUDE: MANCA UN TERMINE. La prova non si legge. ***"))
        tot = dict((k, float(np.sum([r[k] for r in P])))
                   for k in ("delta", "scritture", "freno", "concat", "nati", "morti",
                             "salto"))
        f.write("I TOTALI SU %d PASSI:\n" % len(P))
        f.write("  Delta(somma d0)  %+.6e\n" % tot["delta"])
        f.write("  scritture        %+.6e   (%6.2f %% del Delta)\n"
                % (tot["scritture"], 100.0 * tot["scritture"] / tot["delta"]
                   if tot["delta"] else float("nan")))
        f.write("  FRENO            %+.6e   (%6.2f %%)\n"
                % (tot["freno"], 100.0 * tot["freno"] / tot["delta"]
                   if tot["delta"] else float("nan")))
        f.write("  NASCITE-MORTI    %+.6e   (%6.2f %%)   <- misurato AL SITO che concatena\n"
                % (tot["concat"], 100.0 * tot["concat"] / tot["delta"]
                   if tot["delta"] else float("nan")))
        f.write("\n  (descrittivi, a granularita' di PASSO e non del sito -- NON entrano nel\n")
        f.write("   bilancio: un arco nato e poi scritto mostrerebbe il valore di fine passo)\n")
        f.write("  nascite (fine passo)  %+.6e\n" % tot["nati"])
        f.write("  morti (inizio passo)  %+.6e\n" % tot["morti"])
        f.write("\n  LA GUARDIA DEL SALTO fra la fine di un passo e l'inizio del successivo:\n")
        f.write("  somma dei salti  %+.6e  -> %s\n"
                % (tot["salto"], "nessuna scrittura fuori dal ciclo"
                   if abs(tot["salto"]) < 1e-9 * max(abs(tot["delta"]), 1.0)
                   else "*** QUALCOSA SCRIVE `d0` FUORI DAL CICLO DEL PASSO ***"))
        f.write("\nCHI FA CRESCERE `d0`: il termine col contributo POSITIVO maggiore.\n")
        cand = [("scritture", tot["scritture"]), ("freno", tot["freno"]),
                ("nascite-morti", tot["concat"])]
        cand.sort(key=lambda x: -x[1])
        for n, v in cand:
            f.write("  %-18s %+.6e\n" % (n, v))
        f.write("  -> IL PRIMO E' `%s`\n" % cand[0][0])
        f.write("\nNASCITE e MORTI, e la MEDIANA che conta:\n")
        f.write("%6s %8s %8s | %12s %12s %12s\n"
                % ("passo", "n nati", "n morti", "med nati", "med morti", "med vivi"))
        for r in P:
            if r["passo"] % max(1, len(P) // 15) and r["passo"] != len(P):
                continue
            f.write("%6d %8d %8d | %12.6f %12.6f %12.6f\n"
                    % (r["passo"], r["n_nati"], r["n_morti"], r["med_nati"],
                       r["med_morti"], r["med_vivi"]))
        f.write("\n  -> se `med nati` > `med vivi` e `med morti` < `med vivi`, la mediana sale\n")
        f.write("     SENZA CHE NESSUN ARCO CRESCA: e' NUCLEAZIONE, non stiramento.\n")
        f.write("\nGLI SCRITTORI (la traccia di `Z102`):\n")
        f.write("%-20s %14s %14s %14s | %6s %6s\n"
                % ("scrittore", "SALITE", "DISCESE", "SALDO", "giri", "salta"))
        for s in sorted(stato["conti"]):
            c = stato["conti"][s]
            if c["giri"] == c["salta"]:
                f.write("%-20s %14s %14s %14s | %6d %6d\n"
                        % (s, "n/d", "n/d", "n/d", c["giri"], c["salta"]))
                continue
            f.write("%-20s %14.6e %14.6e %14.6e | %6d %6d\n"
                    % (s, c["su"], c["giu"], c["su"] + c["giu"], c["giri"], c["salta"]))
        f.write("\nIL FRENO, per chiamante di `_smorza`:\n")
        for q in sorted(stato["freno"]):
            c = stato["freno"][q]
            f.write("  %-14s aggiunge %+.6e su dx %+.6e in %d giri%s\n"
                    % (q, c["agg"], c["dx"], c["giri"],
                       "   <- NEL BILANCIO" if q == "d0_passo" else "   (dentro un sito tracciato)"))
        f.write("\n⚠ `_smp_chiudi()` RISCRIVE `d0` a fine passo SENZA nessun `_traccia_d0`\n")
        f.write("  attorno (`:3677`): e' la scrittura che in `Z107` mancava al bilancio.\n")
        # [V8/V9] LA DISTRIBUZIONE DI |dx|/d -- il numero che decide fra `exp(x)` e `1+tanh(x)`
        f.write("\n" + "=" * 92 + "\n")
        f.write("V8/V9 -- LA DISTRIBUZIONE DI |dx|/d, SEPARATA PER SALITE E DISCESE\n")
        f.write("=" * 92 + "\n")
        f.write("  E' il numero che decide la forma del freno-legge (scheda 11, par.4-quater):\n")
        f.write("    |dx|/d << 1  -> `exp(x)` e `1+tanh(x)` sono indistinguibili\n")
        f.write("    |dx|/d ~ 1   -> il tetto di `1+tanh(x)` (RADDOPPIA) comincia a mordere\n")
        f.write("    |dx|/d > 2   -> con la forma di Ito una SALITA FAREBBE SCENDERE\n\n")
        rr = stato.get("ratio", {})
        if not rr:
            f.write("  *** NESSUN CAMPIONE: `_smorza` non e' stato chiamato, oppure le forme\n")
            f.write("      di `dx` e `prima` non coincidevano mai. E' un REPERTO, non un vuoto.\n")
        else:
            f.write("  %-9s %12s %10s %10s %10s %10s %10s %10s %10s\n"
                    % ("verso", "n", "p50", "p90", "p99", "p99.9", "max",
                       ">1 (quota)", ">2 (quota)"))
            f.write("  " + "-" * 90 + "\n")
            for et in ("discese", "salite"):
                v = rr.get(et)
                if not v:
                    f.write("  %-9s   (nessuna)\n" % et)
                    continue
                camp = np.concatenate(v["campioni"]) if v["campioni"] else np.zeros(0)
                q = (np.percentile(camp, [50, 90, 99, 99.9]) if camp.size
                     else [float("nan")] * 4)
                f.write("  %-9s %12d %10.4f %10.4f %10.4f %10.4f %10.4f %10.3e %10.3e\n"
                        % (et, v["n"], q[0], q[1], q[2], q[3], v["max"],
                           v["gt1"] / max(v["n"], 1), v["gt2"] / max(v["n"], 1)))
            f.write("\n  quota con |dx|/d > 0.5:  %s\n"
                    % "  ".join("%s %.3e" % (et, rr[et]["gt05"] / max(rr[et]["n"], 1))
                                for et in sorted(rr)))
            f.write("  ⚠ I QUANTILI vengono da un SOTTOCAMPIONE REGOLARE (non casuale: nessun\n")
            f.write("    RNG consumato, nessuna dipendenza dal seme); `n`, `max` e le QUOTE\n")
            f.write("    sono invece su TUTTI i campioni. Dichiarato perche' sono due basi.\n")
    W("  bilancio -> %s\n  e %s\n" % (p_txt, p_csv))
    rel = np.array([r["rel"] for r in P])
    return float(np.max(rel)), bool(np.max(rel) < 1e-9)


def main():
    modo = None
    passi = None
    for a in sys.argv[1:]:
        if a in ("--controllo", "--riferimento", "--spegni", "--spegni-tutto",
                 "--ritmo-wrap", "--fase-2pi", "--fase-2pi-corto",
                 "--cura1-corto", "--cura2-corto"):
            modo = a
        if a.startswith("--frame="):
            passi = int(a.split("=", 1)[1])
    if modo is None:
        print(__doc__)
        print("*** serve --controllo, --riferimento, --spegni o --spegni-tutto ***")
        return 2
    W = sys.stdout.write
    if not collaudo(W):
        return 1

    os.chdir(RADICE)
    if modo == "--controllo":
        # Un giro CORTO va in una cartella SUA: il driver RIFIUTA (giustamente) una cartella che
        # contiene gia' snapshot di questa fisica senza `--riprendi`, e il giro corto non deve
        # sporcare la cartella del controllo vero. `_g4_corto` e' scratch, e si ripulisce.
        if passi is not None:
            dest = os.path.join(RADICE, "csv", "_test_fork", "_g4_corto")
            if os.path.isdir(dest):
                for _f in os.listdir(dest):
                    if _f.endswith(".pkl.gz"):
                        os.remove(os.path.join(dest, _f))
        else:
            dest = os.path.join(RADICE, "csv", "_test_fork", "_g4_controllo")
        nfr, spegni = (passi or 20), False
    elif modo == "--riferimento":
        dest = os.path.join(RADICE, "csv", "_test_fork", "_g4_riferimento")
        nfr, spegni = (passi or 100), False
    elif modo == "--spegni":
        dest = os.path.join(RADICE, "csv", "_test_fork", "_g4_senza_memmoto")
        nfr, spegni = (passi or 100), True
    elif modo == "--cura2-corto":
        # [CURA 2] IL GIRO CORTO. `TEMPO_UNICO_MITOSI` si accende SUL MODULO, come
        # `MEM_MOTO`/`FASE_2PI`: non ha bisogno di stare nell'argv del driver perche'
        # NON e' una cura approvata -- e' una cura IN PROVA, e il suo posto e' qui
        # finche' Luca non legge il referto.
        dest = os.path.join(RADICE, "csv", "_test_fork", "_cura2_corto")
        if os.path.isdir(dest):
            for _f in os.listdir(dest):
                if _f.endswith(".pkl.gz"):
                    os.remove(os.path.join(dest, _f))
        nfr, spegni = (passi or 20), False
    elif modo == "--cura1-corto":
        # [CURA 1, 2026-09-24] IL GIRO CORTO DELLA CURA 1. NON forza NIENTE sul modulo:
        # la cura e' nell'ARGV del driver (`--ritmo-wrap-2pi`), che e' il punto della
        # cura stessa. Se l'involucro forzasse il flag, il giro proverebbe l'involucro
        # invece del driver -- ed e' esattamente cio' che `T1` del sigillo esclude.
        dest = os.path.join(RADICE, "csv", "_test_fork", "_cura1_corto")
        if os.path.isdir(dest):
            for _f in os.listdir(dest):
                if _f.endswith(".pkl.gz"):
                    os.remove(os.path.join(dest, _f))
        nfr, spegni = (passi or 20), False
    elif modo in ("--fase-2pi", "--fase-2pi-corto"):
        # [FASE_2PI] LA PROVA DELLA CURA DELLA FASE. Nient'altro e' spento: il
        # confronto e' con `_g4_riferimento`, STESSI flag e STESSO seme.
        # `--fase-2pi-corto` e' lo STANDARD 7: un giro CORTO prima del giro vero,
        # perche' la soglia della mitosi scende da 3pi a 2pi e la finestra della
        # campana e' 49.5 volte piu' popolata (17113 archi contro 346, passo 600):
        # se la mitosi accelera di quel fattore, gli ARCHI e il TEMPO esplodono, e
        # va saputo su 120 passi invece che su 600.
        corto = (modo == "--fase-2pi-corto")
        dest = os.path.join(RADICE, "csv", "_test_fork",
                            "_f2p_corto" if corto else "_f2p_prova")
        if corto and os.path.isdir(dest):
            for _f in os.listdir(dest):
                if _f.endswith(".pkl.gz"):
                    os.remove(os.path.join(dest, _f))
        nfr, spegni = (passi or (20 if corto else 100)), False
    elif modo == "--ritmo-wrap":
        # [D34] LA PROVA DELLA CURA DEL RITMO. Nient'altro e' spento: il confronto e'
        # con `_g4_riferimento`, che gira con gli STESSI flag e lo STESSO seme.
        dest = os.path.join(RADICE, "csv", "_test_fork", "_d34_ritmo_wrap")
        nfr, spegni = (passi or 100), False
    else:
        # [G4-bis] L'INTERO blocco. `MEM_MOTO` resta al suo default: e'
        # `MEM_MOTO_TUTTO` DA SOLO a dover spegnere tutti e quattro i punti
        # (sigillo `_sigillo_mem_moto_tutto.py` 10/10, blob 21e3a3dc).
        dest = os.path.join(RADICE, "csv", "_test_fork", "_g4bis_senza_blocco")
        nfr, spegni = (passi or 100), False
    try:
        os.makedirs(dest)
    except OSError:
        pass

    import soliton_simulator as S
    blob = hashlib.sha1(
        open(os.path.join(RADICE, "soliton_simulator.py"), "rb").read()).hexdigest()[:8]
    import inspect as _insp
    seme = _insp.signature(S.Rete.__init__).parameters["seed"].default
    stato, visto = installa(S, spegni, spegni_tutto=(modo == "--spegni-tutto"),
                            wrap2pi=(modo == "--ritmo-wrap"),
                            fase2pi=modo.startswith("--fase-2pi"),
                            cura2=(modo == "--cura2-corto"))
    argv = ["_scena_video.py", str(nfr), dest] + COMUNE + \
        ["--csv-progresso=%s" % os.path.join(dest, "prog.csv")]
    sys.argv = list(argv)
    W("[G4] modo %s   MEM_MOTO spento: %s   MEM_MOTO_TUTTO spento: %s   frame %d\n"
      % (modo, spegni, modo == "--spegni-tutto", nfr))
    W("[G4] blob simulatore %s   seme %s\n" % (blob, seme))
    t0 = time.time()
    runpy.run_path(DRIVER, run_name="__main__")
    W("\n[G4] %.1f s\n" % (time.time() - t0))

    W("\nL'INVOLUCRO: `_applica_flag` avvolto %d volte, MEM_MOTO ORA = %s, MEM_MOTO_TUTTO ORA = %s\n"
      % (visto["chiamate"], bool(S.MEM_MOTO), bool(S.MEM_MOTO_TUTTO)))
    if (visto["chiamate"] == 0 or (spegni and S.MEM_MOTO)
            or (modo == "--spegni-tutto" and S.MEM_MOTO_TUTTO)
            or (modo == "--ritmo-wrap" and not S.RITMO_WRAP_2PI)
            or (modo.startswith("--fase-2pi") and not S.FASE_2PI)
            or (modo == "--cura1-corto" and not S.RITMO_WRAP_2PI)
            or (modo == "--cura2-corto" and not (S.TEMPO_UNICO_MITOSI
                                                 and S.RITMO_WRAP_2PI))):
        W("*** L'INVOLUCRO NON HA AGITO. FERMO. ***\n")
        return 1

    W("\nIL BILANCIO:\n")
    relmax, chiude = scrivi(stato, visto, dest, W, blob, seme, bool(S.MEM_MOTO))
    W("  residuo relativo MASSIMO = %.3e  -> %s\n"
      % (relmax, "CHIUDE" if chiude else "*** NON CHIUDE ***"))

    if modo == "--controllo":
        W("\nIL CONTROLLO DELL'INVOLUCRO: snapshot contro snapshot col riferimento\n")
        p = os.path.join(dest, "scena_000120.pkl.gz")
        if not (os.path.exists(p) and os.path.exists(RIF120)):
            W("*** manca uno dei due snapshot ***\n"); return 1
        ug, dv = confronta_snap(RIF120, p, W)
        ok = (dv == 0 and ug > 0 and chiude)
        W("\n*** CONTROLLO: %d campi identici, %d diversi; bilancio %s -> %s ***\n"
          % (ug, dv, "CHIUDE" if chiude else "NON CHIUDE",
             "PASSA: la prova puo' partire" if ok else "NON PASSA: LA PROVA NON SI FA"))
        return 0 if ok else 1
    if not chiude:
        W("\n*** IL BILANCIO NON CHIUDE: la prova NON si legge finche' non si trova il "
          "termine mancante. ***\n")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
