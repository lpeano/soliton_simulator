# -*- coding: utf-8 -*-
"""SIGILLO DI `CHI_COOP` -- geometria e carica COOPERANO invece di escludersi.

Criteri fissati PRIMA in `doc/TASK_HISTORY/2026-09-21_ramo_C_cooperazione.md` (`e384057`),
committato PRIMA del codice (`0f4fc1e`): l'ordine e' verificabile da git, non asserito qui.

  Z0  i due blob, in BYTE GREZZI (`sha1`), mai `git hash-object` (C18: due numeri diversi).
  Z1  [BLOCCANTE] `CHI_COOP = False` -> stato BYTE-IDENTICO al simulatore PRIMA della patch.
      Una sola divergenza = STOP.
  Z1b [BLOCCANTE, ed e' la CLAUSOLA STRUTTURALE] a flag spento il ramo della geometria non e'
      soltanto inerte: e' IRRAGGIUNGIBILE. Il contatore `_g_ccl_geom` deve valere ESATTAMENTE 0.
  Z2  [BLOCCANTE] LA TORSIONE RICEVE LA GEOMETRIA. Con `CHI_COOP` acceso, le chiamate di
      `chiralita_core_locale` si dividono: quelle della torsione su `perc_geom` (`_g_ccl_geom`),
      quella del campo `B` su `perc_chi` (`_g_ccl_chi`). ENTRAMBE devono essere > 0: se una fosse
      zero, un padrone starebbe leggendo l'array dell'altro.
  Z2b [CONTROLLO POSITIVO OBBLIGATORIO -- senza, `Z2` e' VUOTO] i due array DEVONO aver
      differito, e le due cache con loro. Se `perc_geom == perc_chi` sempre, il test "la torsione
      legge la geometria" non ha distinto NIENTE: due array uguali passano qualunque assegnazione.
      Se non differiscono, l'esito e' FAIL, non PASS. (Stessa famiglia del `max|A-B| = 0.000e+00`
      per mancanza di confronto.)
  Z2c ⚠ DEBOLE, E LO DICHIARO: al PRIMO passo `perc_geom` del ramo C deve valere `perc_chi` del
      ramo A. Ma al passo 1 i due array sono ancora identici PER COSTRUZIONE, quindi un lettore
      assegnato male passerebbe comunque. LA FORZA DEL SIGILLO STA IN `Z2`/`Z2b`, NON QUI.
  Z3  [BLOCCANTE] `perc_chi` == segno di doppia copertura di `_psi_spinor`, su TUTTI i nodi, a
      ogni passo; e `chi_basc` NON scrive `perc_chi` nemmeno una volta (`_g_chibasc_su_chi == 0`).
  Z4  [BLOCCANTE] `len(perc_geom) == n` a OGNI passo -- le tre vie di crescita. Se ne mancasse
      una, la lunghezza divergerebbe IN SILENZIO.
  Z5  nessun `NaN`, nessun `inf`.

⚠ IL SIMULATORE PRIMA si estrae con `git cat-file -p` IN BINARIO, mai con `git checkout`
  (par.5-quinquies, la trappola CRLF).
⚠ Z6 NON E' QUI: e' il sigillo interno della rigiocata, e si gira a parte.
ASCII PURO.
"""
import hashlib
import os
import re
import subprocess
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
SIM_ORA = os.path.join(RADICE, "soliton_simulator.py")
COMMIT_PRIMA = "79be011"        # l ultimo commit PRIMA della patch CHI_COOP
for _x in sys.argv[1:]:
    if _x.startswith("--commit-prima="):
        COMMIT_PRIMA = _x.split("=", 1)[1]
PASSI = 30
CAMPI = ("d0", "d", "vd", "psi", "phi", "eta", "perc_chi", "tw", "omega_s", "pos")

esiti = []


def segna(nome, ok, det):
    esiti.append((nome, ok))
    print("%-5s %-6s %s" % (nome, "PASS" if ok else "FAIL", det))


# ----------------------------------------------------------------- il lavoratore
if "--lavoro" in sys.argv:
    simp = [x.split("=", 1)[1] for x in sys.argv if x.startswith("--sim=")][0]
    outp = [x.split("=", 1)[1] for x in sys.argv if x.startswith("--out=")][0]
    coop = "--coop" in sys.argv
    os.chdir(RADICE)
    sys.argv = ["soliton_simulator.py", "--test", "N-MASSE", "--nmasse", "3", "--sep", "4.0",
                "--giri", "0", "--campo-spinoriale", "--spinore-vivo", "--spinore-corretto",
                "--chi-core", "--calore-scal", "--deparam-orologio", "--verlet", "--fork-su2",
                "--fork-su2-mem", "--cs-dinamico", "--tau-luce", "--rumore-colorato",
                "--pav-com", "--guscio-morbido", "--zeta-vir", "--chi-basc", "--plast-din",
                "--viriale", "--olon-part",
                # ⚠⚠ [2026-09-24] **QUESTO SIGILLO NON E' PIU' RIGIRABILE, E NON PER L'ARGV.**
                # Avevo aggiunto qui le otto cure del driver, credendo che bastasse: **era
                # SBAGLIATO, e la prova e' il rigiro** --
                #   `soliton_simulator.py: error: unrecognized arguments: --scala-min-passo
                #    --peq-esatto ... --tempo-unico-mitosi`
                # perche' **il braccio A e' un simulatore VECCHIO** (`79be011`, sha1 grezzo
                # `b46835bd`) **che quelle opzioni non le ha**. L'argv e' UNA SOLA per i due
                # bracci, e non puo' essere valida per entrambi.
                #
                # **IL PROBLEMA E' STRUTTURALE, non di argv:**
                #   * SENZA le cure, il braccio B (simulatore di OGGI) **si schianta**
                #     sull'invariante `d >= LAM`, che `E4-LAM` ha reso incondizionato
                #     (**`Z148`**: `223 380` archi nascono sotto `LAM`);
                #   * CON le cure, il braccio A **non parte**.
                #   * e darle a UNO SOLO dei due farebbe differire i bracci **per le cure**
                #     invece che per `CHI_COOP`: **il confronto non direbbe piu' niente.**
                #
                # **Quindi si dichiara NON RIGIRABILE** invece di truccarlo, e **NON si
                # spegne l'invariante**: spegnerlo nasconderebbe proprio la misura di `Z148`.
                # **E' un `Z31` NUOVO**, non un'omissione di inventario.
                ] + (["--chi-coop"] if coop else [])
    import importlib.util as _iu
    _sp = _iu.spec_from_file_location("_sim_x", simp)
    S = _iu.module_from_spec(_sp)
    sys.modules["_sim_x"] = S
    _sp.loader.exec_module(S)
    if coop and not hasattr(S, "CHI_COOP"):
        raise SystemExit("questo simulatore non ha CHI_COOP")
    a = S._cli(); S._applica_regime(a); S._applica_flag(a)
    S._NMASSE_VIDEO["n"] = 3; S._NMASSE_VIDEO["sep"] = 4.0; S._NMASSE_VIDEO["size"] = None
    S.avvia_test("N-MASSE")()
    net = S.net
    S.stato["nframe"] = 0

    len_bad = 0            # Z4
    car_bad = 0            # Z3
    car_tot = 0
    passi_diff = 0         # Z2b: quante volte perc_geom != perc_chi
    max_diff = 0
    cache_diverse = 0      # Z2b: quante volte le DUE cache portano contenuti diversi
    p1_geom = p1_chi = None
    n_passi = 0

    for _f in range(PASSI // int(S.PASSI_PER_FRAME)):
        S.passo_test()
        for _ in range(int(S.PASSI_PER_FRAME)):
            S.scuoti_vuoto(net); net.step()
            n_passi += 1
            nn = net.n
            # ---- Z4: la lunghezza di perc_geom, a OGNI passo
            if len(getattr(net, "perc_geom", [])) != len(net.perc_chi):
                len_bad += 1
            # ---- Z3: perc_chi e' il segno di doppia copertura?
            if coop and len(getattr(net, "_psi_spinor", [])) >= nn and len(net._nb) >= nn:
                _canon = net._bloch_a_spinore(net._nb[:nn])
                _ov = np.sum(np.conj(_canon) * net._psi_spinor[:nn], axis=1)
                atteso = np.where(np.real(_ov) >= 0.0, 1, -1)
                car_tot += 1
                if not np.array_equal(np.asarray(net.perc_chi[:nn]), atteso):
                    car_bad += 1
            # ---- Z2b: i due array hanno DAVVERO differito?
            if coop:
                pg = np.asarray(net.perc_geom[:nn]); pc = np.asarray(net.perc_chi[:nn])
                nd = int(np.sum(pg != pc))
                if nd:
                    passi_diff += 1
                    max_diff = max(max_diff, nd)
                cg = np.asarray(getattr(net, "_chi_geom_nodi", []))
                cc = np.asarray(getattr(net, "_chi_core_nodi", []))
                if len(cg) == len(cc) == nn and not np.array_equal(cg, cc):
                    cache_diverse += 1
            if n_passi == 1:
                p1_geom = np.asarray(getattr(net, "perc_geom", []), int).copy()
                p1_chi = np.asarray(net.perc_chi, int).copy()
            net.mitosi()
            net.rilassa_disegno(); net.memoria_hebbiana_moto()

    d = {k: np.asarray(getattr(net, k)) for k in CAMPI if hasattr(net, k)}
    if p1_geom is not None:
        d["p1_geom"] = p1_geom
        d["p1_chi"] = p1_chi
    np.savez(outp, **d)
    print("CONT ccl_geom=%d ccl_chi=%d bas_geom=%d bas_chi=%d"
          % (getattr(net, "_g_ccl_geom", 0), getattr(net, "_g_ccl_chi", 0),
             getattr(net, "_g_chibasc_su_geom", 0), getattr(net, "_g_chibasc_su_chi", 0)))
    print("LEN bad=%d passi=%d n=%d len_geom=%d"
          % (len_bad, n_passi, net.n, len(getattr(net, "perc_geom", []))))
    print("CARICA bad=%d controllati=%d" % (car_bad, car_tot))
    print("DIFF passi=%d maxnodi=%d cache_diverse=%d" % (passi_diff, max_diff, cache_diverse))
    nan = [k for k, v in d.items()
           if v.dtype.kind == "f" and not np.all(np.isfinite(v))]
    print("NAN campi=%s" % (",".join(nan) if nan else "nessuno"))
    raise SystemExit(0)


def gira(sim, out, coop=False):
    cmd = [sys.executable, os.path.abspath(__file__), "--lavoro", "--sim=%s" % sim, "--out=%s" % out]
    if coop:
        cmd.append("--coop")
    pr = subprocess.run(cmd, cwd=RADICE, capture_output=True, text=True,
                        encoding="utf-8", errors="replace")
    if pr.returncode != 0:
        print(pr.stdout[-1500:]); print(pr.stderr[-2500:])
        raise SystemExit("lavoratore uscito con %d" % pr.returncode)
    return pr.stdout


def num(out, chiave, campo):
    m = re.search(r"^%s .*\b%s=(-?\d+)" % (chiave, campo), out, re.M)
    return int(m.group(1)) if m else None


def main():
    base = os.path.join(RADICE, "csv", "_seal_fork", "_sig_chicoop")
    os.makedirs(base, exist_ok=True)
    vecchio = os.path.join(base, "_sim_prima.py")
    q = subprocess.run(["git", "cat-file", "-p", "%s:soliton_simulator.py" % COMMIT_PRIMA],
                       cwd=RADICE, capture_output=True)
    if q.returncode != 0:
        raise SystemExit("non riesco a estrarre il simulatore di %s" % COMMIT_PRIMA)
    with open(vecchio, "wb") as f:      # BINARIO: niente riscrittura delle newline
        f.write(q.stdout)
    with open(SIM_ORA, "rb") as f:
        dn = f.read()
    print("Z0  simulatore PRIMA (%s): sha1 GREZZO %s"
          % (COMMIT_PRIMA, hashlib.sha1(q.stdout).hexdigest()[:8]))
    print("Z0  simulatore ORA            : sha1 GREZZO %s" % hashlib.sha1(dn).hexdigest()[:8])
    print("Z0  (NB: NON e' `git hash-object`. Sono due numeri diversi per lo stesso file, C18.)")
    print("")

    oA = os.path.join(base, "A_prima.npz")
    oB = os.path.join(base, "B_ora_off.npz")
    oC = os.path.join(base, "C_ora_coop.npz")
    print("braccio A: simulatore PRIMA della patch        (chi_basc -> perc_chi)")
    outA = gira(vecchio, oA)
    print("braccio B: simulatore ORA, CHI_COOP = False    (atteso: identico ad A)")
    outB = gira(SIM_ORA, oB)
    print("braccio C: simulatore ORA, CHI_COOP = True     (atteso: DIVERSO, e per la cosa giusta)")
    outC = gira(SIM_ORA, oC, coop=True)
    print("")

    A, B, C = np.load(oA), np.load(oB), np.load(oC)

    def diff(x, y):
        f = []
        for k in CAMPI:
            if k not in x or k not in y:
                f.append("%s(assente)" % k); continue
            a, b = x[k], y[k]
            if a.shape != b.shape:
                f.append("%s(shape %s vs %s)" % (k, a.shape, b.shape))
            elif not np.array_equal(a, b):
                f.append("%s(max|d|=%.3e)" % (k, float(np.nanmax(np.abs(a - b)))))
        return f

    f1 = diff(A, B)
    segna("Z1", not f1, "a CHI_COOP spento: %d campi -> %s"
          % (len(CAMPI), "BYTE-IDENTICI" if not f1 else "DIVERSI: %s" % f1[:6]))
    if f1:
        print("  *** Z1 e' BLOCCANTE: la cooperazione TOCCA il ramo spento. FERMO. ***")
        return 1

    gB = num(outB, "CONT", "ccl_geom")
    segna("Z1b", gB == 0,
          "a flag spento il ramo geometria e' IRRAGGIUNGIBILE, non solo inerte: _g_ccl_geom = %s"
          % gB)

    gC = num(outC, "CONT", "ccl_geom")
    cC = num(outC, "CONT", "ccl_chi")
    segna("Z2", (gC or 0) > 0 and (cC or 0) > 0,
          "le chiamate si DIVIDONO: torsione su perc_geom = %s, campo B su perc_chi = %s"
          % (gC, cC))

    pd = num(outC, "DIFF", "passi")
    md = num(outC, "DIFF", "maxnodi")
    cd = num(outC, "DIFF", "cache_diverse")
    segna("Z2b", (pd or 0) > 0 and (cd or 0) > 0,
          "CONTROLLO POSITIVO: i due array differiscono in %s passi (max %s nodi) e le due CACHE "
          "portano contenuti diversi in %s passi %s"
          % (pd, md, cd, "" if (pd or 0) > 0 and (cd or 0) > 0
             else "-> il test NON HA DISTINTO NIENTE: e' VUOTO, quindi FAIL"))

    if "p1_geom" in C and "p1_chi" in A:
        z2c = np.array_equal(C["p1_geom"], A["p1_chi"])
        segna("Z2c", z2c,
              "al PRIMO passo perc_geom(C) == perc_chi(A): %s  [DEBOLE: al passo 1 i due array "
              "sono identici per costruzione, la forza sta in Z2/Z2b]" % ("si'" if z2c else "NO"))

    cb = num(outC, "CARICA", "bad")
    ct = num(outC, "CARICA", "controllati")
    bc = num(outC, "CONT", "bas_chi")
    bg = num(outC, "CONT", "bas_geom")
    segna("Z3", cb == 0 and ct and ct > 0 and bc == 0 and (bg or 0) > 0,
          "perc_chi == segno di doppia copertura in %s passi su %s; chi_basc ha scritto perc_geom "
          "%s volte e perc_chi %s volte" % ((ct or 0) - (cb or 0), ct, bg, bc))

    lb = num(outC, "LEN", "bad")
    npas = num(outC, "LEN", "passi")
    nn = num(outC, "LEN", "n")
    lg = num(outC, "LEN", "len_geom")
    segna("Z4", lb == 0 and nn == lg,
          "len(perc_geom) == len(perc_chi) in %s passi su %s; a fine run n = %s, len = %s"
          % ((npas or 0) - (lb or 0), npas, nn, lg))

    nanC = re.search(r"NAN campi=(\S+)", outC)
    segna("Z5", bool(nanC) and nanC.group(1) == "nessuno",
          "NaN/inf nei campi del ramo C: %s" % (nanC.group(1) if nanC else "?"))

    f2 = diff(A, C)
    print("")
    print("  (non e' un criterio, e' un'informazione) il ramo C differisce da A su %d campi su %d:"
          % (len(f2), len(CAMPI)))
    for x in f2[:10]:
        print("    %s" % x)
    print("  ATTESO: lo spinore sente la carica vera dal passo 2, e `:4493` cambia la NASCITA dei")
    print("  nodi. La divergenza NON e' un fallimento.")

    print("")
    n_pass = sum(1 for _, o in esiti if o)
    print("ESITO: %d/%d" % (n_pass, len(esiti)))
    print("")
    if n_pass == len(esiti):
        print("VERDETTO: CHI_COOP e' INERTE a flag spento (e il ramo geometria IRRAGGIUNGIBILE),")
        print("  la torsione riceve la GEOMETRIA e il campo B la CARICA, chi_basc non tocca mai")
        print("  perc_chi, e perc_geom resta lungo n. Il ramo C si puo' lanciare.")
    else:
        print("VERDETTO: IL SIGILLO NON PASSA. Il ramo C NON si lancia.")
    print("")
    print("⚠ LIMITI, dichiarati: UN seme, UNA scena, %d passi. In %d passi la coppia di SCHWINGER" % (PASSI, PASSI))
    print("  puo' non essere MAI scattata, quindi la terza via di crescita di `perc_geom` puo'")
    print("  essere NON ESERCITATA: Z4 la copre solo se e' scattata. Si legge nel conteggio dei")
    print("  nati (`_g_nati_schwinger`), non si assume.")
    print("⚠ E Z6 NON E' QUI: e' il sigillo interno della rigiocata, e si gira a parte.")
    return 0 if n_pass == len(esiti) else 1


if __name__ == "__main__":
    sys.exit(main())
