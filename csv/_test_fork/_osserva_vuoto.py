# -*- coding: utf-8 -*-
"""OSSERVATORE DEL VUOTO — misura PURE-READ di chi (angoli fra Bloch vicini) e <n> (isotropia).

PERCHE' ESISTE
--------------
Due cose erano date per scontate e mai misurate:
  1. lo scuotimento del vuoto e' MEDIATO (colpisce self._nb a :1803, che a :2034 viene sovrascritto
     dalla proiezione del primario; raggiunge _psi_spinor solo via il torque cross(B,nb), quindi
     O(amp*|B|*dt) e non O(amp)). SCUOTE ABBASTANZA da rompere la degenerazione dei Bloch?
  2. l'ISOTROPIA e' ASSERITA, non dimostrata (doc/ROADMAP_fork_SU2.md:46 cita una riga marcata
     "# APERTO:" che e' un condizionale). <n> resta ~0, o la dinamica rettifica il rumore isotropo?

COME NON CONTAMINA LA FISICA (par.2.3)
--------------------------------------
Non e' una modifica a soliton_simulator.py: e' un OSSERVATORE ESTERNO che avvolge `Rete.step` e,
DOPO che il passo e' finito, LEGGE gli array committati. Non scrive nulla, non chiama nulla che
muti stato (in particolare MAI `calcola_psi()`, che riscriverebbe `self.psi`), non consuma `net.rng`.
La purezza non e' affermata: e' sigillata da `_sigillo_osservatore.py` (run con/senza -> stato
byte-identico), che va girato PRIMA dei run lunghi.

SEPARAZIONE MATERIA / VUOTO — zero parametri nuovi (par.3)
----------------------------------------------------------
La soglia e' `Lam = <|Psi|^2>` = `lambda_vuoto(net)`, cioe' la scala di energia del vuoto CHE IL
SISTEMA USA GIA' per modulare l'ampiezza dello scuotimento (`amp = sqrt(Lam)/(1+I2/Lam)`). Non e'
un numero scelto: e' una grandezza di stato. Per robustezza si riportano ANCHE i percentili p10/p90,
cosi' la lettura non dipende dalla soglia.
NB: `Lam` e' una media globale, ma qui e' una CLASSIFICAZIONE DIAGNOSTICA, non una correzione
applicata allo stato: il divieto del par.4 ("niente sottrazione della media globale") riguarda la
DINAMICA, e nulla di quanto segue rientra nella dinamica.

USO
---
python csv/_test_fork/_osserva_vuoto.py --seed 1 --passi 2000 --ogni 100 \\
       --tag on   [--regime-det]  [--no-osserva]
"""
import argparse
import csv as _csv
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))

# [2026-09-16] RIUSO della ricostruzione GIA' SIGILLATA della catena di omega (MISURA F piu' sotto).
# Import per path: il file inizia con un underscore e non e' un pacchetto. L'import e' SICURO —
# `_tracing_omega.py` a livello di modulo definisce soltanto, non esegue nulla (verificato).
import importlib.util as _ilu
_spec = _ilu.spec_from_file_location("_trac_omega", os.path.join(HERE, "_tracing_omega.py"))
_TRAC = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(_TRAC)


def _pend_se(x, y):
    """Pendenza d(log y)/d(log x) fra NODI, con la sua SE. Stessa formula di `_rimisura_t3.py`.

    NB (CLAUDE.md par.9): questa `SE` e' INTERNA AL RUN. Per confrontare due BRACCI si usa la
    dispersione FRA SEMI (~0.03), non questa (~0.01). Si scrive comunque perche' dice quanto e'
    determinata la pendenza DI QUESTO run, che e' un'informazione diversa e serve lo stesso."""
    x = np.asarray(x, float); y = np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y) & (x > 0) & (y > 0)
    if int(ok.sum()) < 50:
        return float("nan"), float("nan"), float("nan"), int(ok.sum())
    lx, ly = np.log(x[ok]), np.log(y[ok])
    b = float(np.polyfit(lx, ly, 1)[0])
    rr = float(np.corrcoef(lx, ly)[0, 1])
    n = int(ok.sum())
    se = abs(b / rr) * np.sqrt((1 - rr * rr) / (n - 2)) if abs(rr) > 1e-12 else float("nan")
    return b, float(se), rr * rr, n



def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--passi", type=int, default=2000)
    ap.add_argument("--ogni", type=int, default=100)
    ap.add_argument("--tag", default="on")
    ap.add_argument("--step2", action="store_true", dest="step2",
                    help="accende --step2-orologio (omega_clk *= (cs/CS_M)^2, orologio di Compton).")
    ap.add_argument("--cs-dinamico", action="store_true", dest="cs_dinamico",
                    help="accende --cs-dinamico: senza, cs = CS_M costante e il turbo e' ignorato.")
    ap.add_argument("--gamma-turbo", type=float, default=1.0, dest="gamma_turbo", metavar="K",
                    help="amplificatore DIAGNOSTICO della sensibilita' di cs a rho (solo _cs_nodo).")
    ap.add_argument("--tau-luce", action="store_true", dest="tau_luce",
                    help="accende --tau-luce: il rilassamento di omega_s usa il TEMPO-LUCE d/cs "
                         "invece di TAU_A*max(dens/dens_rif, 0.05). NON e' un forzante come il "
                         "turbo: e' una correzione di LEGGE, ed e' l'unica cosa che abbassa theta "
                         "(da ~96 a ~43 giri/passo). Serve al braccio ON del gradiente di "
                         "risoluzione. NB: i sigilli della FASE 2 NON sono passati, quindi il "
                         "braccio OFF resta la baseline certificata.")
    ap.add_argument("--kuramoto", action="store_true", dest="kuramoto",
                    help="accende --kuramoto-su2 (allineamento locale alla media SU(2) dei vicini).")
    ap.add_argument("--regime-det", action="store_true", dest="regime_det",
                    help="braccio OFF: --regime deterministico, che cambia SOLO SCUOTIMENTO "
                         "(True->False). Verificato confrontando TUTTI i globali del modulo.")
    ap.add_argument("--no-osserva", action="store_true", dest="no_osserva",
                    help="gira senza osservatore: serve al sigillo di byte-identita'.")
    ap.add_argument("--riprendi-da", default=None, dest="riprendi_da",
                    help="RESUME: copia questo .pkl come DB del run e NON passa --db-cleanup, cosi' "
                         "il simulatore riparte dallo stato salvato. La guardia del DB confronta solo "
                         "il git blob dei byte del codice, non i flag: stesso .py con flag diversi e' "
                         "accettato (verificato dal sorgente).")
    ap.add_argument("--outdir", default=HERE)
    a = ap.parse_args()

    base = os.path.join(a.outdir, "_vuoto_%s_s%d" % (a.tag, a.seed))
    argv = ["soliton_simulator.py",
            "--batch", "--nmasse", "3", "--sep", "8",
            "--seed", str(a.seed), "--passi", str(a.passi),
            "--ogni", str(a.ogni), "--db-ogni", str(a.passi),
            "--campo-spinoriale", "--spinore-vivo", "--spinore-corretto", "--chi-core",
            "--calore-scal", "--deparam-orologio", "--verlet",
            "--fork-su2", "--fork-su2-mem",
            "--csv", base + ".cond.csv", "--sync-db", base + ".pkl"]
    if a.riprendi_da:
        import shutil
        shutil.copyfile(a.riprendi_da, base + ".pkl")   # il DB da cui ripartire
        print("[osserva] RESUME da %s" % a.riprendi_da, flush=True)
    else:
        argv += ["--db-cleanup"]
    if a.step2:
        argv += ["--step2-orologio"]
    if a.cs_dinamico:
        argv += ["--cs-dinamico"]
    if a.gamma_turbo != 1.0:
        argv += ["--gamma-turbo", str(a.gamma_turbo)]
    if a.tau_luce:
        argv += ["--tau-luce"]
    if a.kuramoto:
        argv += ["--kuramoto-su2"]
    if a.regime_det:
        argv += ["--regime", "deterministico"]

    os.chdir(ROOT)
    sys.path.insert(0, ROOT)
    sys.argv = argv
    import soliton_simulator as S

    # [2026-09-15] IL BLOB DEL CODICE CHE STA GIRANDO, calcolato come lo calcola git
    # (sha1 di "blob <len>\0" + byte del file). Senza subprocess: deterministico e puro.
    # PERCHE': un CSV senza blob non e' ri-eseguibile, e un file che si distingue dagli altri solo
    # per il NOME non e' un dato ma un ricordo (CLAUDE.md par.9). Il blob e' l'unica identita' del
    # codice che non puo' mentire: un commit puo', un blob no (par.2.6).
    import hashlib
    with open(os.path.join(ROOT, "soliton_simulator.py"), "rb") as _f:
        _by = _f.read()
    BLOB = hashlib.sha1(b"blob %d\0" % len(_by) + _by).hexdigest()
    print("[osserva] blob soliton_simulator.py = %s   seed = %d   tag = %s"
          % (BLOB, a.seed, a.tag), flush=True)

    # [REGOLA DI LUCA, 2026-09-16 -- CLAUDE.md par.5-quinquies] IL CODICE DI UNA MISURA DEV'ESSERE
    # RECUPERABILE, SEMPRE E PER COSTRUZIONE: o il blob sul disco e' QUELLO COMMITTATO nel branch
    # (caso normale), oppure accanto ai dati resta una COPIA ESATTA del file che ha girato.
    # NON e' una cosa da ricordarsi: e' cablata qui, perche' oggi (2026-09-16) e' successo il
    # contrario -- MISURA G e' rimasta non committata mentre quattro run la stavano gia' usando,
    # e la riproducibilita' e' stata salvata solo dal fatto che nessuno ha toccato il file nel
    # frattempo. Un fatto che dovevo ASSERIRE io, mentre il par.5 esiste apposta perche' non debba
    # asserirlo nessuno.
    # NB: si confronta col blob a HEAD, NON con `git status`: un file puo' essere "modificato" per
    # sole newline e restare lo stesso blob, e un file puo' essere identico a un commit VECCHIO
    # senza esserlo a HEAD. Il blob e' l'unica identita' che non mente (par.2.6).
    # [CORREZIONE 2026-09-16, dopo un FALSO POSITIVO] Il primo scatto vero di questa guardia,
    # durante il sigillo dell'osservatore, ha scritto TRE copie il cui blob era `08784685`, cioe'
    # ESATTAMENTE quello a HEAD: la guardia non aveva rilevato una differenza, aveva fallito a
    # LEGGERE git. Causa probabile: `timeout=30` con sei processi pesanti sulla macchina.
    # Tre correzioni, e la piu' importante e' la terza:
    #   1. timeout 120s invece di 30, e UN RITENTATIVO;
    #   2. si distingue «blob DIVERSO» da «git non interrogabile», perche' sono due cose diverse;
    #   3. il MOTIVO viene scritto in un file accanto alla copia. Il `print` non basta: quando lo
    #      script gira dentro un sigillo, lo stdout e' CATTURATO e il motivo si perde — che e'
    #      esattamente come un falso positivo diventa indistinguibile da un allarme vero.
    NL = chr(10)                             # a capo, per le note scritte su file
    _atteso, _perche = None, None
    for _tent in (1, 2):
        try:
            import subprocess as _sp
            _r = _sp.run(["git", "rev-parse", "HEAD:soliton_simulator.py"], cwd=ROOT,
                         capture_output=True, text=True, timeout=120)
            if _r.returncode == 0:
                _atteso = _r.stdout.strip()
                break
            _perche = "git rc=%d: %s" % (_r.returncode, _r.stderr.strip()[:200])
        except Exception as _e:                 # niente git, o repo assente: NON si blocca il run
            _perche = "%s: %s (tentativo %d)" % (type(_e).__name__, _e, _tent)
    # TERZO CASO, scoperto il 2026-09-16 e da NON confondere con gli altri due: il file puo' avere
    # lo STESSO CONTENUTO ma NON gli stessi BYTE, perche' `core.autocrlf = true` riscrive le
    # newline a ogni `git checkout`. `git hash-object` applica il filtro `clean` e quindi VEDE
    # uguale cio' che sul disco e' diverso; `BLOB` qui sopra e' lo sha1 dei BYTE GREZZI e non lo
    # vede uguale. NON e' un dettaglio: un `git checkout -- soliton_simulator.py` e' bastato a
    # portare il file da 435730 byte (LF) a 442240 (CRLF), cambiando lo sha1 grezzo da
    # `08784685` a `37c31630` — e i CSV gia' scritti portano `08784685`.
    _pulito = None
    try:
        import subprocess as _sp2
        _r2 = _sp2.run(["git", "hash-object", "--", "soliton_simulator.py"], cwd=ROOT,
                       capture_output=True, text=True, timeout=120)
        if _r2.returncode == 0:
            _pulito = _r2.stdout.strip()
    except Exception:
        pass
    if _atteso is not None and _atteso == BLOB:
        print("[osserva] codice COMMITTATO e BYTE-IDENTICO all'oggetto a HEAD. "
              "Nessuna copia necessaria.", flush=True)
    else:
        _copia = base + "._sim.py"
        with open(_copia, "wb") as _f:          # BINARIO: una riscrittura testuale cambierebbe il
            _f.write(_by)                       # blob, e la copia non sarebbe piu' quel file
        if _atteso is not None and _pulito == _atteso:
            _tit = ("*** STESSO CONTENUTO, BYTE DIVERSI: le newline sono state normalizzate "
                    "(core.autocrlf) ***")
            _nota = ("MOTIVO: contenuto IDENTICO all'oggetto a HEAD, byte DIVERSI." + NL +
                     "  sha1 dei BYTE GREZZI sul disco : %s" + NL +
                     "  git hash-object (filtro clean) : %s" + NL +
                     "  oggetto a HEAD                 : %s" + NL +
                     "Le due ultime coincidono, la prima no: il file sul disco ha newline diverse" + NL +
                     " da quelle dell'oggetto (core.autocrlf le riscrive a ogni checkout)." + NL +
                     "LA FISICA E' LA STESSA - Python ignora le newline - MA IL FILE NON E'" + NL +
                     " BYTE-IDENTICO a quello che i CSV citano col loro `blob`." + NL +
                     "NON cancellare questa copia credendola ridondante: `git hash-object` NON" + NL +
                     " puo' mostrare la differenza, perche' applica proprio il filtro che la crea." + NL
                     ) % (BLOB, _pulito, _atteso)
        elif _atteso is None:
            _tit = "*** GIT NON INTERROGABILE: copia scritta per PRUDENZA, non per una differenza ***"
            _nota = ("MOTIVO: git non interrogabile (%s).\n"
                     "Il blob sul disco e' %s. NON e' stato possibile confrontarlo con HEAD," + NL +
                     " quindi questa copia NON dimostra che il codice fosse diverso:" + NL +
                     " dimostra solo che non si e' potuto verificare." + NL +
                     "Se `git rev-parse HEAD:soliton_simulator.py` da' %s, questa copia e'" + NL +
                     " RIDONDANTE e si puo' cancellare." + NL) % (_perche, BLOB, BLOB)
        else:
            _tit = "*** IL CODICE CHE STA GIRANDO NON E' QUELLO COMMITTATO ***"
            _nota = ("MOTIVO: blob DIVERSO da HEAD." + NL + "  disco %s" + NL +
                     "  HEAD  %s" + NL +
                     "COMMITTA QUESTA COPIA INSIEME AI DATI: senza, la misura non e'" + NL +
                     " rifacibile." + NL) % (BLOB, _atteso)
        with open(_copia[:-3] + ".motivo.txt", "w") as _f:
            _f.write(_nota)                     # il motivo sopravvive anche se lo stdout e' catturato
        print("[osserva] %s" % _tit, flush=True)
        print("[osserva]     disco %s   HEAD %s" % (BLOB[:12], (_atteso or "(ignoto)")[:12]),
              flush=True)
        print("[osserva]     copia: %s   motivo: %s" % (_copia, _copia[:-3] + ".motivo.txt"),
              flush=True)

    arg = S._cli()
    S._applica_regime(arg)
    # I FLAG NON SI LEGGONO QUI. `_applica_regime` fissa solo SCUOTIMENTO; FORK_SU2 e FORK_SU2_MEM
    # sono assegnati da `_applica_flag`, che `batch_condensazione` chiama al suo interno (:5172),
    # cioe' DOPO questo punto. Leggerli adesso darebbe False su entrambi anche quando il run li usa
    # (sbaglio preso davvero: sigillo O3c FAIL, commit 279c3b7). L'unica lettura onesta di "con
    # cosa ha girato la fisica" e' quella presa DENTRO il ciclo, al momento della misura: vedi
    # `flag_visti` piu' sotto e la riga [osserva-flag] stampata a fine run.
    flag_visti = set()

    righe = []
    stato = {"k": 0, "hdr": False}

    def _scrivi_incrementale(r):
        """Scrive OGNI campione SUBITO, invece di tenerlo in memoria fino a fine run.

        PERCHE': senza, un run lungo non e' TRONCABILE SULL'EVIDENZA. Il 2026-09-14 lo scan del
        turbo e' stato ordinato partendo dal forcing piu' forte proprio per poterlo fermare presto
        se le firme restano piatte — ma l'osservatore scriveva il CSV solo alla fine, quindi al
        passo 500 non c'era nulla da guardare: o si aspettavano tutti i 2000 passi (2.8 ore), o si
        uccideva il run perdendo tutto. Difetto di progetto, corretto qui.
        Costo: una riga di CSV per campione (cioe' ogni `--ogni` passi). Irrilevante."""
        # [DIFETTO CURATO 2026-09-16] LE COLONNE SI DISALLINEAVANO IN SILENZIO.
        # `DictWriter` veniva costruito A OGNI CHIAMATA con `fieldnames = list(r.keys())`, cioe'
        # con l'ordine della RIGA CORRENTE, mentre l'intestazione era stata scritta UNA VOLTA con
        # l'ordine della PRIMA riga. Se un blocco di misura inserisce le sue chiavi in un ORDINE
        # DIVERSO fra il ramo `if` e il ramo `else` — e la prima riga prende quasi sempre il ramo
        # `else`, perche' a passo 1 il sistema e' immaturo — tutte le righe successive finiscono
        # SFASATE rispetto all'intestazione.
        # MISURATO: `L_n_passi_con_mitosi` (un CONTEGGIO) valeva `0.513`, e
        # `L_dL_senza_mitosi_mediana` (una FRAZIONE) valeva `18`. Due valori scambiati di posto.
        # CURA: le `fieldnames` si fissano UNA VOLTA, dalla prima riga, e si riusano; e ogni riga
        # successiva deve avere ESATTAMENTE lo stesso insieme di chiavi, altrimenti si ALZA un
        # errore invece di scrivere un CSV che sembra a posto.
        out = base + ".vuoto.csv"
        modo = "a" if stato["hdr"] else "w"
        if not stato["hdr"]:
            stato["campi"] = list(r.keys())
        else:
            _manca = set(stato["campi"]) - set(r.keys())
            _extra = set(r.keys()) - set(stato["campi"])
            if _manca or _extra:
                raise RuntimeError(
                    "CSV: l'insieme delle colonne e' cambiato fra i campioni. "
                    "MANCANTI: %s   IN PIU': %s" % (sorted(_manca)[:8], sorted(_extra)[:8]))
        with open(out, modo, newline="") as f:
            wcsv = _csv.DictWriter(f, fieldnames=stato["campi"])
            if not stato["hdr"]:
                wcsv.writeheader()
                stato["hdr"] = True
            wcsv.writerow(r)
    orig_step = S.Rete.step
    # [2026-09-15] SPIA SU `ritmo()`: registra `r` COSI' COM'E' restituito dal passo VERO, senza
    # chiamarlo una seconda volta. Richiamarlo dal diagnostico NON sarebbe puro: sul ramo di return
    # anticipato `ritmo()` riscrive `self._psi_prec`. Qui si legge soltanto il valore di ritorno.
    orig_ritmo = S.Rete.ritmo
    ultimo_r = {"v": None}

    def spia_ritmo(self):
        r = orig_ritmo(self)
        ultimo_r["v"] = None if r is None else np.asarray(r, float).copy()
        return r
    S.Rete.ritmo = spia_ritmo
    # RNG LOCALE del diagnostico: il campionamento delle coppie per l'autocorrelazione NON deve
    # consumare `net.rng` (par.2.3). Seme fisso -> stesse coppie a ogni campione, confrontabili.
    rng_diag = np.random.default_rng(20260915)

    def in_applica_flag():
        """_applica_flag gira 300 step di riscaldamento su un'ALTRA rete (quella interattiva
        globale): vanno ESCLUSI, altrimenti le misure mescolano due sistemi."""
        f = sys._getframe(2)
        for _ in range(7):
            if f is None:
                return False
            if f.f_code.co_name == "_applica_flag":
                return True
            f = f.f_back
        return False

    def misura(net, passo):
        """SOLO LETTURA degli array gia' committati. Nessuna scrittura, nessun rng, nessuna
        chiamata che ricalcoli campi (mai calcola_psi())."""
        n = int(net.n)
        nb = getattr(net, "_nb", None)
        psi = getattr(net, "psi", None)
        if nb is None or psi is None or len(nb) < n or len(psi) < n or n < 2 or not len(net.i):
            return
        nb = np.asarray(nb, float)[:n]
        I2 = np.abs(np.asarray(psi)[:n]) ** 2
        Lam = float(np.mean(I2))                      # = lambda_vuoto(net), scala di stato

        # ---- MISURA A: chi_ij = angolo fra i Bloch dei due estremi di ogni arco --------------
        ii, jj = net.i, net.j
        m = (ii < n) & (jj < n)
        ii, jj = ii[m], jj[m]
        cos_chi = np.clip(np.sum(nb[ii] * nb[jj], axis=1), -1.0, 1.0)
        chi = np.arccos(cos_chi)
        I2a = 0.5 * (I2[ii] + I2[jj])                 # densita' dell'ARCO (media dei due nodi)

        # ---- MISURA B: <n> = media vettoriale dei Bloch --------------------------------------
        r = {"passo": passo, "n": n, "n_archi": int(len(chi)), "Lam": Lam}
        p10, p90 = float(np.percentile(I2, 10)), float(np.percentile(I2, 90))

        regioni = (("tot", np.ones(n, bool), np.ones(len(chi), bool)),
                   ("mat", I2 > Lam, I2a > Lam),      # soglia = scala del vuoto (zero parametri)
                   ("vuo", I2 <= Lam, I2a <= Lam),
                   ("p90", I2 >= p90, I2a >= p90),    # robustezza: la lettura non deve dipendere
                   ("p10", I2 <= p10, I2a <= p10))    # dalla soglia scelta
        for nome, sel_n, sel_a in regioni:
            c = chi[sel_a]
            r["chi_%s_n" % nome] = int(c.size)
            if c.size:
                r["chi_%s_media" % nome] = float(np.mean(c))
                r["chi_%s_std" % nome] = float(np.std(c))
                r["chi_%s_mediana" % nome] = float(np.median(c))
                # frazioni vicino ai due poli degeneri (0 = allineati, pi = antipodali)
                r["chi_%s_fr_lt10g" % nome] = float(np.mean(c < np.radians(10.0)))
                r["chi_%s_fr_gt170g" % nome] = float(np.mean(c > np.radians(170.0)))
            else:
                for k in ("media", "std", "mediana", "fr_lt10g", "fr_gt170g"):
                    r["chi_%s_%s" % (nome, k)] = float("nan")
            v = nb[sel_n]
            r["nmed_%s_N" % nome] = int(v.shape[0])
            if v.shape[0]:
                mv = v.mean(axis=0)
                r["nmed_%s_x" % nome] = float(mv[0])
                r["nmed_%s_y" % nome] = float(mv[1])
                r["nmed_%s_z" % nome] = float(mv[2])
                r["nmed_%s_mod" % nome] = float(np.linalg.norm(mv))
                # riferimento statistico: per direzioni casuali |<n>| ~ 1/sqrt(N)
                r["nmed_%s_atteso" % nome] = float(1.0 / np.sqrt(max(v.shape[0], 1)))
                r["nmed_%s_sigma" % nome] = (float(np.linalg.norm(mv) * np.sqrt(v.shape[0])))
            else:
                for k in ("x", "y", "z", "mod", "atteso", "sigma"):
                    r["nmed_%s_%s" % (nome, k)] = float("nan")

        # ---- STABILITA' (gratis) -------------------------------------------------------------
        psp = getattr(net, "_psi_spinor", None)
        nbr = getattr(net, "_nb_ret", None)
        r["norma_psi_err"] = (float(np.max(np.abs(np.linalg.norm(np.asarray(psp)[:n], axis=1) - 1.0)))
                              if psp is not None and len(psp) >= n else float("nan"))
        r["norma_nret_err"] = (float(np.max(np.abs(np.linalg.norm(np.asarray(nbr)[:n], axis=1) - 1.0)))
                               if nbr is not None and len(nbr) >= n else float("nan"))
        r["nan_psi"] = int(not np.all(np.isfinite(np.asarray(psi)[:n])))
        r["max_pos"] = (float(np.max(np.abs(np.asarray(net.pos)[:n])))
                        if getattr(net, "pos", None) is not None and len(net.pos) >= n else float("nan"))
        # CON COSA HA GIRATO DAVVERO QUESTO PASSO (letto dai globali vivi, non da prima del run)
        r["FORK_SU2"] = int(S.FORK_SU2)
        r["FORK_SU2_MEM"] = int(S.FORK_SU2_MEM)
        r["SCUOTIMENTO"] = int(S.SCUOTIMENTO)
        r["SYNC_UPDATE"] = int(S.SYNC_UPDATE)
        r["KURAMOTO_SU2"] = int(S.KURAMOTO_SU2)
        r["STEP2"] = int(S.STEP2_OROLOGIO)
        r["GAMMA_TURBO"] = float(S.GAMMA_TURBO)
        r["TAU_LUCE"] = int(getattr(S, "TAU_LUCE", False))
        r["CS_DINAMICO"] = int(S.CS_DINAMICO)
        # IDENTITA' DEL RUN: senza queste, due bracci si distinguono solo dal nome del file.
        r["blob"] = BLOB
        r["seed"] = int(a.seed)
        r["tag"] = a.tag
        # cs VIVO? se std ~ 0 il turbo non morde e il run e' nullo (verifica-scala in-run)
        _csp = getattr(net, "_cs_nodo_prev", None)
        if _csp is not None and len(_csp) >= n:
            _c = np.asarray(_csp, float)[:n]
            r["cs_std"] = float(np.std(_c)); r["cs_min"] = float(np.min(_c)); r["cs_max"] = float(np.max(_c))
        else:
            r["cs_std"] = r["cs_min"] = r["cs_max"] = float("nan")
        # ---- MISURA C: `theta = |omega_s| * dt_n` in GRADI/passo ----------------------------
        # NON la sola mediana: anche la CODA (frazione sopra 30 gradi/passo), che e' cio' che decide
        # se il settore e' campionato o aliasato. dt_n = DT*r con l'`r` del passo appena finito.
        om = getattr(net, "omega_s", None)
        rv = ultimo_r["v"]
        if om is not None and len(om) >= n:
            omn = np.linalg.norm(np.asarray(om, float)[:n], axis=1)
            rr = rv[:n] if (rv is not None and len(rv) >= n) else np.ones(n)
            # [2026-09-16, C19] DUE CONVENZIONI, SCRITTE FIANCO A FIANCO. Non sono la stessa
            # osservabile, e finche' ne gira una sola un numero che si muove puo' essere fisica
            # oppure l'unita' di misura che cambia (e' gia' successo: theta_ON sembrava centrare
            # l'attesa -0.69, ma anche il braccio OFF si muoveva, senza ragione).
            #   theta_coord = |omega| * DT     tempo di COORDINATA  (la convenzione di C8 e del -0.69)
            #   theta_prop  = |omega| * dt_n   tempo PROPRIO        (quella fisicamente giusta, par.9)
            # NESSUNA DELLE DUE SI DISMETTE: la giusta e' `prop`, ma tutto lo storico e'in `coord`.
            th_coord = np.degrees(omn * S.DT)
            th_prop = np.degrees(omn * S.DT * rr)
            for _et, _v in (("coord", th_coord), ("prop", th_prop)):
                r["theta_%s_mediana" % _et] = float(np.median(_v))
                r["theta_%s_media" % _et] = float(np.mean(_v))
                r["theta_%s_p90" % _et] = float(np.percentile(_v, 90))
                r["theta_%s_giri_mediana" % _et] = float(np.median(_v) / 360.0)
                r["theta_%s_fr_gt30g" % _et] = float(np.mean(_v > 30.0))
                r["theta_%s_fr_gt360g" % _et] = float(np.mean(_v > 360.0))
            # IL RAPPORTO FRA LE DUE **E'** `r`, il tempo proprio locale: theta_prop/theta_coord = r.
            # Si scrive perche' e' utile di per se' — la FASE 5 agisce proprio li' — e perche' e' un
            # CONTROLLO: deve coincidere con `r_mediana` della MISURA D.
            r["r_ratio_mediana"] = float(np.median(th_prop / np.maximum(th_coord, 1e-300)))
            r["r_ratio_media"] = float(np.mean(th_prop / np.maximum(th_coord, 1e-300)))
            # LEGACY, da non usare nei lavori nuovi: e' `theta_prop`, e sta qui solo perche' gli 8
            # CSV gia' committati e `_verdetto_4pi.py` / `_verdetto_S_R.py` la leggono con questo
            # nome. Rinominarla avrebbe reso illeggibili i dati gia' presi (par.5).
            th = th_prop
            r["theta_mediana"] = float(np.median(th))
            r["theta_media"] = float(np.mean(th))
            r["theta_p90"] = float(np.percentile(th, 90))
            r["theta_giri_mediana"] = float(np.median(th) / 360.0)
            r["theta_fr_gt30g"] = float(np.mean(th > 30.0))
            r["theta_fr_gt360g"] = float(np.mean(th > 360.0))
        else:
            for _et in ("coord", "prop"):
                for k in ("mediana", "media", "p90", "giri_mediana", "fr_gt30g", "fr_gt360g"):
                    r["theta_%s_%s" % (_et, k)] = float("nan")
            r["r_ratio_mediana"] = r["r_ratio_media"] = float("nan")
            for k in ("theta_mediana", "theta_media", "theta_p90", "theta_giri_mediana",
                      "theta_fr_gt30g", "theta_fr_gt360g"):
                r[k] = float("nan")

        # ---- MISURA D: DISPERSIONE di `r` (MAI la mediana) -----------------------------------
        # `ritmo()` fa `x = f/median(|f|)` e normalizza su `r_unit` = il valore a x=1: il nodo
        # mediano ha x=1 per definizione e la mappa e' monotona, quindi `median(r) = 1.0` ESATTA,
        # con qualunque orologio. Misurarla per vedere se cambia e' un test VUOTO (errore commesso
        # dal sigillo S4 il 2026-09-15). Si riporta la DISPERSIONE e i quantili.
        if rv is not None and len(rv) >= n:
            rr = rv[:n]
            r["r_std"] = float(np.std(rr))
            r["r_iqr"] = float(np.percentile(rr, 75) - np.percentile(rr, 25))
            r["r_p05"] = float(np.percentile(rr, 5)); r["r_p95"] = float(np.percentile(rr, 95))
            r["r_min"] = float(np.min(rr)); r["r_max"] = float(np.max(rr))
            r["r_mediana"] = float(np.median(rr))   # solo come CONTROLLO che valga 1: non e' una misura
        else:
            for k in ("r_std", "r_iqr", "r_p05", "r_p95", "r_min", "r_max", "r_mediana"):
                r[k] = float("nan")

        # ---- MISURA H: CONSERVAZIONE, `r` PER ETA', e il FATTORE `cs^-2` --------------------
        # (1) `L_tot = somma(inerzia*|omega|)`: LA QUANTITA' CHE DOVREBBE CONSERVARSI, e il suo
        #     SALTO attraverso le mitosi. Misurato per la prima volta il 2026-09-16 (voce C20):
        #     cresce del ~3.4 % a ogni passo con crescita. Qui entra nella campagna, non solo nel
        #     sigillo, cosi' il numero ha una barra FRA SEMI e non una sola scena.
        if len(serie_L) >= 2:
            _pa = np.array([x[0] for x in serie_L], float)
            _nn = np.array([x[1] for x in serie_L], float)
            _LL = np.array([x[2] for x in serie_L], float)
            r["L_tot"] = float(_LL[-1])
            r["L_fatt_cs_mediana"] = float(serie_L[-1][3])
            r["L_fatt_cs_scarto_max"] = float(serie_L[-1][4])
            _d = np.diff(_LL) / np.maximum(_LL[:-1], 1e-300)
            _cresce = np.diff(_nn) > 0
            _ok = np.isfinite(_d)
            r["L_dL_su_L_mediana"] = float(np.median(_d[_ok])) if _ok.any() else float("nan")
            _m = _ok & _cresce
            r["L_dL_con_mitosi_mediana"] = float(np.median(_d[_m])) if _m.any() else float("nan")
            r["L_dL_con_mitosi_media"] = float(np.mean(_d[_m])) if _m.any() else float("nan")
            r["L_n_passi_con_mitosi"] = int(_m.sum())
            _s = _ok & (~_cresce)
            r["L_dL_senza_mitosi_mediana"] = float(np.median(_d[_s])) if _s.any() else float("nan")
            r["L_n_passi_senza_mitosi"] = int(_s.sum())
            r["L_nodi_nati"] = int(np.sum(np.maximum(np.diff(_nn), 0)))
        else:
            for k in ("L_tot", "L_fatt_cs_mediana", "L_fatt_cs_scarto_max", "L_dL_su_L_mediana",
                      "L_dL_con_mitosi_mediana", "L_dL_con_mitosi_media", "L_dL_senza_mitosi_mediana"):
                r[k] = float("nan")
            r["L_n_passi_con_mitosi"] = r["L_n_passi_senza_mitosi"] = r["L_nodi_nati"] = 0

        # (2) IL FATTORE `(CS_M/cs)^2` in questo istante: distribuzione, e QUANTO SI DISCOSTA DA 1.
        #     E' il numero che dice se la correzione `cs^-2` ha un effetto in questo regime, e in
        #     particolare se un run col TURBO ha davvero svegliato `cs` (se resta ~1, il test e' NULLO).
        _csn = getattr(net, "_cs_nodo_prev", None)
        if _csn is not None and len(_csn) >= n:
            _c = np.maximum(np.asarray(_csn, float)[:n], 1e-12)
            _f = (S.CS_M / _c) ** 2
            r["fatt_cs_mediana"] = float(np.median(_f))
            r["fatt_cs_media"] = float(np.mean(_f))
            r["fatt_cs_min"] = float(np.min(_f)); r["fatt_cs_max"] = float(np.max(_f))
            r["fatt_cs_p90"] = float(np.percentile(_f, 90))
            r["fatt_cs_scarto_max"] = float(np.max(np.abs(_f - 1.0)))
            r["fatt_cs_frac_oltre_1pc"] = float(np.mean(np.abs(_f - 1.0) > 0.01))
        else:
            for k in ("fatt_cs_mediana", "fatt_cs_media", "fatt_cs_min", "fatt_cs_max",
                      "fatt_cs_p90", "fatt_cs_scarto_max", "fatt_cs_frac_oltre_1pc"):
                r[k] = float("nan")

        # (3) `r` STRATIFICATO PER ETA'. Oggi c'e' solo la dispersione sulla popolazione INTERA.
        #     Serve alla domanda aperta: il figlio eredita `_psi_prec` dal padre, quindi il suo
        #     PRIMO `r` confronta la propria fase con quella del PADRE. `eta` parte da zero ma
        #     l'orologio no: il figlio e' «nato ora» per l'eta' e «in corsa da sempre» per la fase.
        _eta = getattr(net, "eta", None)
        if rv is not None and len(rv) >= n and _eta is not None and len(_eta) >= n:
            _e = np.asarray(_eta, float)[:n]
            _rr = np.asarray(rv, float)[:n]
            _q = np.percentile(_e, [25, 50, 75])
            for _et, _sel in (("q1", _e <= _q[0]), ("q2", (_e > _q[0]) & (_e <= _q[1])),
                              ("q3", (_e > _q[1]) & (_e <= _q[2])), ("q4", _e > _q[2])):
                if _sel.any():
                    r["r_eta_%s_mediana" % _et] = float(np.median(_rr[_sel]))
                    r["r_eta_%s_std" % _et] = float(np.std(_rr[_sel]))
                    r["r_eta_%s_n" % _et] = int(_sel.sum())
                else:
                    r["r_eta_%s_mediana" % _et] = r["r_eta_%s_std" % _et] = float("nan")
                    r["r_eta_%s_n" % _et] = 0
            _giov = _e <= (2.0 * S.DT)          # «appena nati»: meno di due tic di coordinata
            r["r_eta_neonati_mediana"] = float(np.median(_rr[_giov])) if _giov.any() else float("nan")
            r["r_eta_neonati_n"] = int(_giov.sum())
            r["eta_mediana"] = float(np.median(_e))
        else:
            for _et in ("q1", "q2", "q3", "q4"):
                r["r_eta_%s_mediana" % _et] = r["r_eta_%s_std" % _et] = float("nan")
                r["r_eta_%s_n" % _et] = 0
            r["r_eta_neonati_mediana"] = r["eta_mediana"] = float("nan")
            r["r_eta_neonati_n"] = 0

        # (4) `omega/sqrt(n)`: LA FIRMA che dice se il sistema e' ancora in regime di RANDOM WALK.
        #     Oggi e' costante entro il 4.6 % (CLAUDE.md par.9) — ed e' cio' che prova il regime
        #     diffusivo. Se smettesse di esserlo, la forzante e' diventata COERENTE.
        if om is not None and len(om) >= n and n > 0:
            _omn = np.linalg.norm(np.asarray(om, float)[:n], axis=1)
            r["omega_mediana"] = float(np.median(_omn))
            r["omega_su_sqrtn"] = float(np.median(_omn) / np.sqrt(n))
            r["omega_media_su_sqrtn"] = float(np.mean(_omn) / np.sqrt(n))
        else:
            r["omega_mediana"] = r["omega_su_sqrtn"] = r["omega_media_su_sqrtn"] = float("nan")

        # ---- MISURA E: AUTOCORRELAZIONE SPAZIALE <n_i . n_j> per bin di distanza -------------
        # E' la firma che DISCRIMINA (B) da (A) e da (C): ~0 ovunque = nessuna struttura;
        # decadimento a scala FINITA = struttura; ~1 ovunque = collasso globale.
        # Coppie campionate con l'RNG LOCALE del diagnostico, mai `net.rng`.
        pos = getattr(net, "pos", None)
        if pos is not None and len(pos) >= n and n >= 100:
            P = np.asarray(pos, float)[:n]
            K = 200000
            ia = rng_diag.integers(0, n, K); ib = rng_diag.integers(0, n, K)
            keep = ia != ib
            ia, ib = ia[keep], ib[keep]
            dist = np.linalg.norm(P[ia] - P[ib], axis=1)
            dot = np.sum(nb[ia] * nb[ib], axis=1)
            bordi = np.percentile(dist, [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
            idx = np.clip(np.digitize(dist, bordi[1:-1]), 0, 9)
            for b in range(10):
                m_b = idx == b
                cnt = int(m_b.sum())
                r["ac%d_n" % b] = cnt
                if cnt > 1:
                    v_b = dot[m_b]
                    r["ac%d_d" % b] = float(np.mean(dist[m_b]))
                    r["ac%d" % b] = float(np.mean(v_b))
                    r["ac%d_se" % b] = float(np.std(v_b) / np.sqrt(cnt))
                else:
                    r["ac%d_d" % b] = r["ac%d" % b] = r["ac%d_se" % b] = float("nan")
        else:
            for b in range(10):
                r["ac%d_n" % b] = 0
                r["ac%d_d" % b] = r["ac%d" % b] = r["ac%d_se" % b] = float("nan")

        # ---- MISURA F: LE TRE PENDENZE TRASVERSALI, NELLO STESSO RUN (voce R del registro) ----
        # PERCHE': l'attesa `-0.69` del divario T3 e' calcolata con il `sigma` del braccio VECCHIO
        # (-1.078), ma l'anello `tau -> omega -> phi -> psi -> inerzia -> sigma` mette `sigma` A
        # VALLE di `tau`: se cambiando `tau` cambia anche `sigma`, l'attesa va RICALCOLATA col
        # `sigma` DI QUEL BRACCIO. Non propone un colpevole nuovo: mette in dubbio il BERSAGLIO.
        # (`doc/RAMIFICAZIONI.md` D.2/R, marcata «va provata PER PRIMA».)
        #
        # NON si ricostruisce la catena qui: si RIUSA `_tracing_omega.ingredienti`, che e' gia'
        # sigillato pure-read (copia profonda + restore dell'RNG) e che gia' contiene il termine
        # `cross(_nb_grav(), nb)` la cui OMISSIONE fu l'errore del 2026-09-15. Duplicare la
        # ricostruzione qui significherebbe riesporsi allo stesso errore.
        # VALIDO SOLO SE `SPIN_LARMOR` e `TW_SPINORE` sono spenti (la ricostruzione non contiene
        # `Bg` ne' `_otw`): per questo entrambi finiscono nel CSV, e l'analisi li deve leggere.
        r["SPIN_LARMOR"] = int(getattr(S, "SPIN_LARMOR", False))
        r["TW_SPINORE"] = int(getattr(S, "TW_SPINORE", False))
        try:
            g = _TRAC.ingredienti(S, net)
            inz = np.asarray(g["inerzia"], float)
            sig = np.asarray(g["coppia_su_in"], float)          # |correzione| / inerzia
            # il `tau` CHE IL RUN USA DAVVERO, non quello di default:
            tau_eff = np.asarray(g["tau_luce"] if int(r["TAU_LUCE"]) else g["tau"], float)
            om_src = np.asarray(g["om_src"], float)
            dtn_g = np.asarray(g["dtn"], float)
            # [2026-09-16, C19] LE DUE CONVENZIONI, ANCHE QUI. `dtn_g = DT*r`, quindi
            # `theta_prop = theta_coord * r` e le due pendenze differiscono ESATTAMENTE di quella
            # di `r` (il logaritmo di un prodotto e' la somma, e il campione e' lo stesso):
            # e' un'IDENTITA', non un'approssimazione, e viene verificata sotto come controllo.
            th_coord = np.degrees(om_src * S.DT)
            th_prop = np.degrees(om_src * dtn_g)
            r_loc = np.asarray(dtn_g, float) / S.DT          # il tempo proprio locale, per nodo
            th_g = th_prop                                   # LEGACY: `t3_b_theta` E' la `prop`
            # si esclude il PAVIMENTO dell'inerzia: li' l'ascissa e' COSTANTE per costruzione
            # (una regressione su un'ascissa costante non e' una pendenza). STESSA soglia di
            # `_rimisura_t3.py` — `rho > 1.0000001e-6` — e non `~pavimento`: un nodo con
            # `rho == 1e-6` esatto non e' marcato pavimento ma ha comunque `inerzia` al floor.
            liberi = inz > 1.0000001e-6
            for nome, y in (("sigma", sig), ("tau", tau_eff), ("theta", th_g),
                            ("theta_coord", th_coord), ("theta_prop", th_prop), ("r", r_loc)):
                b, se, r2, nn = _pend_se(inz[liberi], y[liberi])
                r["t3_b_%s" % nome] = b
                r["t3_se_%s" % nome] = se
                r["t3_r2_%s" % nome] = r2
                r["t3_n_%s" % nome] = nn
            # ---- LA CATENA, RIDERIVATA. E il termine in `r` NON c'era. -----------------------
            # `|omega|_eq = |F| * sqrt(dt_n * tau / 2)` (random walk smorzato, CLAUDE.md par.9),
            # e `dt_n = DT * r`. Passando ai logaritmi e derivando rispetto a log(inerzia):
            #     pend(omega)       = sigma + tau/2 + r/2
            #     pend(theta_coord) = pend(omega)        = sigma + tau/2 +   r/2     [theta = omega*DT]
            #     pend(theta_prop)  = pend(omega) + r    = sigma + tau/2 + 3*r/2     [theta = omega*dt_n]
            # LA FORMULA USATA FINORA, `sigma + tau/2`, ASSUME `pend(r) = 0` — in ENTRAMBE le
            # convenzioni. Non e' stato verificato: ora `t3_b_r` lo misura. Se e' ~0 la vecchia
            # attesa resta valida e questa e' solo una conferma; se non lo e', l'attesa `-0.69`
            # e tutto C8 vanno riletti. NON si dismette la vecchia: si scrivono tutte e tre.
            r["t3_attesa"] = r["t3_b_sigma"] + 0.5 * r["t3_b_tau"]          # LEGACY (assume r=0)
            r["t3_divario"] = r["t3_b_theta"] - r["t3_attesa"]              # LEGACY
            r["t3_attesa_coord"] = r["t3_b_sigma"] + 0.5 * r["t3_b_tau"] + 0.5 * r["t3_b_r"]
            r["t3_divario_coord"] = r["t3_b_theta_coord"] - r["t3_attesa_coord"]
            r["t3_attesa_prop"] = r["t3_b_sigma"] + 0.5 * r["t3_b_tau"] + 1.5 * r["t3_b_r"]
            r["t3_divario_prop"] = r["t3_b_theta_prop"] - r["t3_attesa_prop"]
            # CONTROLLO DI IDENTITA' (non un test fisico): pend(prop) - pend(coord) - pend(r) = 0
            # ESATTAMENTE. Se non e' ~1e-12 c'e' un errore nel codice, non nella fisica.
            r["t3_identita"] = (r["t3_b_theta_prop"] - r["t3_b_theta_coord"] - r["t3_b_r"])
            r["t3_n_liberi"] = int(liberi.sum())
            r["t3_ok"] = 1
            # ---- MISURA G: GLI INGREDIENTI DEL CONTO FDT, sul sistema PULITO -----------------
            # Il conto che ha refutato Gilbert/FDT (`doc/ANALISI_gilbert_fdt.md`) e' stato fatto
            # con la FASE 5 INERTE (C11) e senza `--cs-dinamico`: era una misura su un sistema
            # DIVERSO da quello dichiarato, e va rifatto. Qui NON si rifa' il conto: si scrivono
            # gli INGREDIENTI misurati, e il conto si fa nell'analisi, dove e' leggibile.
            #   lambda = amp^2 * |B| / (2 * dt * kT)   con kT = Lam  (l'unica temperatura
            #   parameter-free del sistema, quella da cui il rumore stesso e' costruito)
            #   kT_equipartizione = I * <omega^2> / 3
            # `Lam` e' gia' nella riga (colonna `Lam`), `DT` e' una costante del modulo.
            _bm = np.asarray(g["Bm"], float); _amp = np.asarray(g["amp"], float)
            for _nome, _v in (("B", _bm), ("amp", _amp), ("om", om_src),
                              ("inerzia", inz), ("dtn", dtn_g)):
                _f = _v[np.isfinite(_v)]
                if _f.size:
                    r["fdt_%s_mediana" % _nome] = float(np.median(_f))
                    r["fdt_%s_p25" % _nome] = float(np.percentile(_f, 25))
                    r["fdt_%s_p75" % _nome] = float(np.percentile(_f, 75))
                else:
                    r["fdt_%s_mediana" % _nome] = r["fdt_%s_p25" % _nome] =                         r["fdt_%s_p75" % _nome] = float("nan")
            # <omega^2> serve alla equipartizione e NON e' il quadrato della mediana
            r["fdt_om2_media"] = float(np.mean(om_src[np.isfinite(om_src)] ** 2))                 if np.any(np.isfinite(om_src)) else float("nan")
            r["fdt_DT"] = float(S.DT)
            # ---- MISURA U: IL SETTORE U(1) / SEGNO -------------------------------------------
            # PERCHE' ESISTE: nell'osservatore non c'era NESSUNA colonna di questo settore. Zero.
            # E lo Step 2 e' il ponte METRICA -> OROLOGIO, e l'orologio pilota la FASE, che E' il
            # settore U(1). Accendere il ponte senza misurarne l'uscita e' accendere AL BUIO.
            # LE FORMULE SONO QUELLE DEL SIMULATORE (`diagnostica`, :5765-5792), non riscritte:
            # stessi pesi d'arco, stessa canonizzazione, stessa selezione materia-materia.
            # SI USANO GLI INGREDIENTI DELLA COPIA PROFONDA di MISURA F, perche' `_pesi()` MUTA
            # cache lette dalla dinamica: chiamarlo sulla rete VERA contaminerebbe la fisica.
            # OGNI OSSERVABILE PORTA IL SUO VALORE SOTTO IPOTESI NULLA (par.9):
            #   segno_ov_absmedia   frustrato -> 2/pi = 0.6366   (media di |cos| uniforme)
            #   segno_arco_coer     frustrato -> 0    (+1 concorde, -1 alternato)
            #   segno_arco_coer_mat idem, ma SOLO archi materia-materia: distingue ORDINE VERO da
            #                       SEPARAZIONE illusoria (il totale puo' salire solo escludendo
            #                       gli archi materia-antimateria discordi)
            #   spin_overlap_arco   casuale -> 0.5
            #   verso_arco_coer     casuale -> 0
            # NB: `berry_segno*` / `berry_spin*` NON si usano: la BUSSOLA le marca MORTE
            # (telescopano, quindi sono cieche al segno-orologio).
            _w = np.asarray(g["w"], float); _ii = np.asarray(g["ii"]); _jj = np.asarray(g["jj"])
            _psp = np.asarray(g["psi_spinor"]); _canon = np.asarray(g["canon"])
            _nbg = np.asarray(g["nb_grav"], float); _pcm = np.sign(np.asarray(g["perc_chi"], float))
            _seg = np.real(np.sum(np.conj(_canon) * _psp, axis=1))     # Re<canon|psi> in [-1,1]
            _sgn = np.sign(_seg)
            _uu = _nbg / np.maximum(np.linalg.norm(_nbg, axis=1, keepdims=True), 1e-12)
            r["u1_segno_ov_absmedia"] = float(np.mean(np.abs(_seg)))
            r["u1_segno_ov_nullo"] = 2.0 / np.pi
            _mk = (_ii < n) & (_jj < n)
            if _mk.any():
                _i2 = _ii[_mk]; _j2 = _jj[_mk]
                _wa = _w[_mk] if len(_w) == len(_ii) else np.ones(int(_mk.sum()))
                _ds = max(float(np.sum(_wa)), 1e-12)
                r["u1_segno_arco_coer"] = float(np.sum(_wa * _sgn[_i2] * _sgn[_j2]) / _ds)
                r["u1_verso_arco_coer"] = float(np.sum(_wa * np.sum(_uu[_i2] * _uu[_j2], axis=1)) / _ds)
                _ovl = np.abs(np.sum(np.conj(_psp[_i2]) * _psp[_j2], axis=1)) ** 2
                r["u1_spin_overlap_arco"] = float(np.sum(_wa * _ovl) / _ds)
                # PRESIDIO: il settore materia si seleziona con l'etichetta STABILE `perc_chi > 0`,
                # NON con `_sgn` stesso, che darebbe la tautologia `_sgn*_sgn = +1`.
                _mm = (_pcm[_i2] > 0) & (_pcm[_j2] > 0)
                r["u1_n_arco_materia"] = int(_mm.sum())
                if _mm.any():
                    _wm = _wa[_mm]; _dm = max(float(np.sum(_wm)), 1e-12)
                    r["u1_segno_arco_coer_materia"] = float(
                        np.sum(_wm * _sgn[_i2][_mm] * _sgn[_j2][_mm]) / _dm)
                else:
                    r["u1_segno_arco_coer_materia"] = float("nan")
                # stratificazione materia / vuoto / p90, come per `chi`
                _I2n = np.abs(np.asarray(psi)[:n]) ** 2
                _Lam = float(np.mean(_I2n)); _p90 = float(np.percentile(_I2n, 90))
                _I2a = 0.5 * (_I2n[_i2] + _I2n[_j2])
                for _et, _sa in (("mat", _I2a > _Lam), ("vuo", _I2a <= _Lam), ("p90", _I2a >= _p90)):
                    if _sa.any():
                        _ws = _wa[_sa]; _dd = max(float(np.sum(_ws)), 1e-12)
                        r["u1_segno_arco_coer_%s" % _et] = float(
                            np.sum(_ws * _sgn[_i2][_sa] * _sgn[_j2][_sa]) / _dd)
                        r["u1_spin_overlap_%s" % _et] = float(
                            np.sum(_ws * _ovl[_sa]) / _dd)
                    else:
                        r["u1_segno_arco_coer_%s" % _et] = float("nan")
                        r["u1_spin_overlap_%s" % _et] = float("nan")
            else:
                for k in ("u1_segno_arco_coer", "u1_verso_arco_coer", "u1_spin_overlap_arco",
                          "u1_segno_arco_coer_materia"):
                    r[k] = float("nan")
                r["u1_n_arco_materia"] = 0
                for _et in ("mat", "vuo", "p90"):
                    r["u1_segno_arco_coer_%s" % _et] = r["u1_spin_overlap_%s" % _et] = float("nan")
            r["STEP2_letto"] = int(S.STEP2_OROLOGIO)
        except Exception as _e:                      # P5: un fallback si CONTA, non si subisce
            stato["t3_fail"] = stato.get("t3_fail", 0) + 1
            stato["t3_perche"] = "%s: %s" % (type(_e).__name__, _e)
            for nome in ("sigma", "tau", "theta", "theta_coord", "theta_prop", "r"):
                r["t3_b_%s" % nome] = r["t3_se_%s" % nome] = r["t3_r2_%s" % nome] = float("nan")
                r["t3_n_%s" % nome] = 0
            r["t3_attesa"] = r["t3_divario"] = float("nan")
            r["t3_attesa_coord"] = r["t3_divario_coord"] = float("nan")
            r["t3_attesa_prop"] = r["t3_divario_prop"] = r["t3_identita"] = float("nan")
            r["t3_n_liberi"] = 0
            r["t3_ok"] = 0
            for _nome in ("B", "amp", "om", "inerzia", "dtn"):
                r["fdt_%s_mediana" % _nome] = r["fdt_%s_p25" % _nome] =                     r["fdt_%s_p75" % _nome] = float("nan")
            r["fdt_om2_media"] = float("nan")
            r["fdt_DT"] = float(S.DT)
            for k in ("u1_segno_ov_absmedia", "u1_segno_arco_coer", "u1_verso_arco_coer",
                      "u1_spin_overlap_arco", "u1_segno_arco_coer_materia"):
                r[k] = float("nan")
            r["u1_segno_ov_nullo"] = 2.0 / np.pi
            r["u1_n_arco_materia"] = 0
            for _et in ("mat", "vuo", "p90"):
                r["u1_segno_arco_coer_%s" % _et] = r["u1_spin_overlap_%s" % _et] = float("nan")
            r["STEP2_letto"] = int(S.STEP2_OROLOGIO)

        # La riga e' COMPLETA solo qui: flag e cs_* sono appena stati aggiunti. Scrivere prima
        # troncherebbe il CSV proprio sulle colonne di verifica (errore fatto e corretto il
        # 2026-09-14: il primo tentativo scriveva dopo `nan_psi`, e STEP2/cs_* sparivano).
        _scrivi_incrementale(r)
        righe.append(r)

    def _L_tot(net):
        """L = somma(inerzia * |omega|), con l'inerzia COME LA CALCOLA IL SIMULATORE (fattore
        `cs^-2` incluso). E' la quantita' che DOVREBBE conservarsi: `omega` e' intensiva, quindi
        alla mitosi e' l'INERZIA che dovrebbe ripartirsi.
        Costa poco: legge array gia' committati, niente copia profonda, niente RNG."""
        n = int(net.n)
        om = getattr(net, "omega_s", None)
        if om is None or len(om) < n or n == 0:
            return float("nan"), float("nan"), float("nan")
        rs = getattr(net, "rho_spin", None)
        rho = (np.asarray(rs, float)[:n] if (rs is not None and len(rs) >= n)
               else np.abs(np.asarray(net.psi, complex)[:n]) ** 2)
        csp = getattr(net, "_cs_nodo_prev", None)
        if csp is not None and len(csp) >= n:
            f = (S.CS_M / np.maximum(np.asarray(csp, float)[:n], 1e-12)) ** 2
        else:
            f = np.ones(n)
        inz = np.maximum(rho * f, 1e-6)
        omn = np.linalg.norm(np.asarray(om, float)[:n], axis=1)
        return float(np.sum(inz * omn)), float(np.median(f)), float(np.max(np.abs(f - 1.0)))

    serie_L = []          # (passo, n, L_tot) a OGNI passo: serve al salto attraverso le mitosi

    def spia(self):
        mio = not in_applica_flag()
        orig_step(self)
        if mio:
            stato["k"] += 1
            _L, _fm, _fd = _L_tot(self)
            serie_L.append((stato["k"], int(self.n), _L, _fm, _fd))
            # i globali VIVI, campionati a ogni passo del batch: se cambiassero a meta' run lo si
            # vedrebbe qui (l'insieme avrebbe piu' di un elemento).
            flag_visti.add((bool(S.FORK_SU2), bool(S.FORK_SU2_MEM),
                            bool(S.SCUOTIMENTO), bool(S.SYNC_UPDATE), bool(S.KURAMOTO_SU2),
                            bool(S.STEP2_OROLOGIO), bool(S.CS_DINAMICO), float(S.GAMMA_TURBO),
                            bool(getattr(S, "TAU_LUCE", False))))
            if not a.no_osserva and (stato["k"] == 1 or stato["k"] % a.ogni == 0):
                misura(self, stato["k"])

    S.Rete.step = spia          # sempre: la spia dei flag e' pure-read e serve anche al braccio
    S.batch_condensazione(arg)  # --no-osserva (dove `misura` non gira mai: vedi `campiona`)

    for f in sorted(flag_visti):
        print("[osserva-flag] tag=%s seed=%d  FORK_SU2=%s FORK_SU2_MEM=%s SCUOTIMENTO=%s "
              "SYNC_UPDATE=%s KURAMOTO_SU2=%s STEP2=%s CS_DIN=%s GAMMA_TURBO=%.4g TAU_LUCE=%s"
              "   (letti DURANTE il run)" % ((a.tag, a.seed) + f), flush=True)
    if len(flag_visti) > 1:
        print("[osserva-flag] ATTENZIONE: i flag sono CAMBIATI durante il run.", flush=True)

    if not a.no_osserva and righe:
        # NON si riscrive il file: ogni campione e' gia' stato scritto da `_scrivi_incrementale`
        # mano a mano. Riscriverlo qui vanificherebbe la troncabilita' (un run ucciso perderebbe
        # tutto, che e' esattamente il difetto corretto).
        print("[osserva] MISURA F (pendenze t3): %d campioni FALLITI su %d   %s"
              % (stato.get("t3_fail", 0), len(righe),
                 stato.get("t3_perche", "")), flush=True)
        print("[osserva] %d campioni -> %s (scritti incrementalmente)"
              % (len(righe), base + ".vuoto.csv"), flush=True)


if __name__ == "__main__":
    main()
