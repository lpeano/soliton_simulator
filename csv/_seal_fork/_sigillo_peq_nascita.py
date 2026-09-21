# -*- coding: utf-8 -*-
"""SIGILLO DELLA CURA `C2 -- PEQ_NASCITA_LOCALE`. [BLOCCANTE]

SEI PROVE:
  `Q1`  flag SPENTO -> **byte-identico** al simulatore di prima della cura;
  `Q2`  **CONTROLLO POSITIVO**: flag ACCESO e SPENTO **devono differire**. Senza, `Q1` passerebbe
        anche su codice morto;
  `Q3`  a flag ACCESO, subito dopo una `mitosi()` che ha creato archi di Schwinger, **esattamente
        `2*nc` valori `nan`** compaiono in `peq` -- e a flag SPENTO **ZERO**;
  `Q4`  **dopo il passo successivo NON resta NESSUN `nan`**: la calibrazione di `:4189` ha girato.
        **E' la prova che il `nan` non e' una perdita ma una CONSEGNA;**
  `Q5`  **NESSUN `nan` ALTROVE**: `d`, `d0`, `vd`, `psi`, `tw` restano puliti. Il `nan` non si
        propaga fuori da `peq`;
  `Q6`  **LA NASCITA E' LOCALE, e si misura**: a flag ACCESO il valore calibrato **DIFFERISCE
        dalla mediana globale**; a flag SPENTO **coincide con essa a zero cifre di scarto**.
        **E' la prova che la cura ha cambiato la LEGGE, non solo un numero.**

⚠ `Q6` E' IL CRITERIO CHE CONTA, e gli altri cinque non lo sostituiscono: `Q1`-`Q5` dicono che il
  meccanismo funziona, **`Q6` dice che fa la cosa GIUSTA** -- prendere la `rho` del PROPRIO arco
  invece di una statistica della rete (`A2`).
ASCII PURO.
"""
import hashlib
import os
import subprocess
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
SIM_ORA = os.path.join(RADICE, "soliton_simulator.py")
COMMIT_PRIMA = "8227917"
BLOB_PRIMA = "d972a517"          # sha1 dei BYTE GREZZI
PASSI = 36
CAMPI = ("d0", "d", "vd", "psi", "phi", "eta", "peq", "perc_chi", "perc_geom",
         "tw", "omega_s", "pos")
PULITI = ("d", "d0", "vd", "psi", "tw", "phi")

ARGV_D = ["soliton_simulator.py", "--test", "N-MASSE", "--nmasse", "3", "--sep", "4.0",
          "--giri", "0", "--campo-spinoriale", "--spinore-vivo", "--spinore-corretto",
          "--chi-core", "--calore-scal", "--deparam-orologio", "--verlet", "--fork-su2",
          "--fork-su2-mem", "--cs-dinamico", "--tau-luce", "--rumore-colorato",
          "--pav-com", "--guscio-morbido", "--zeta-vir", "--chi-basc", "--chi-coop",
          "--scala-min", "--coes-adim", "--plast-din", "--viriale", "--olon-part"]


if "--lavoro" in sys.argv:
    simp = [x.split("=", 1)[1] for x in sys.argv if x.startswith("--sim=")][0]
    outp = [x.split("=", 1)[1] for x in sys.argv if x.startswith("--out=")][0]
    cura = "--cura" in sys.argv
    os.chdir(RADICE)
    sys.argv = list(ARGV_D) + (["--peq-nascita-locale"] if cura else [])
    import importlib.util as _iu
    _sp = _iu.spec_from_file_location("_sim_c2", simp)
    S = _iu.module_from_spec(_sp)
    sys.modules["_sim_c2"] = S
    _sp.loader.exec_module(S)
    a = S._cli(); S._applica_regime(a); S._applica_flag(a)
    if cura != bool(getattr(S, "PEQ_NASCITA_LOCALE", False)):
        raise SystemExit("[sigillo] il flag non corrisponde alla richiesta")
    S._NMASSE_VIDEO["n"] = 3; S._NMASSE_VIDEO["sep"] = 4.0; S._NMASSE_VIDEO["size"] = None
    S.avvia_test("N-MASSE")()
    net = S.net
    S.stato["nframe"] = 0

    nan_dopo_mitosi = 0      # Q3: quanti `nan` sono comparsi, in tutto
    attesi = 0               # Q3: quanti ne erano attesi (2*nc)
    nan_residui = 0          # Q4: quanti ne restano dopo il passo dopo
    nan_altrove = 0          # Q5
    scarti = []              # Q6: dispersione DOPO la calibrazione, un valore per evento
    disp_nascita = []        # Q6: dispersione ALLA NASCITA, un valore per evento
    uguali_med = 0           # Q6 ramo SPENTO: quanti valori sono ESATTAMENTE la mediana
    tot_nati = 0             # Q6: su quanti archi di Schwinger
    ident_male = 0           # controprova: eventi in cui gli archi non sono 2 per antinodo
    pend = None
    prec_nc = 0
    for _f in range(PASSI // int(S.PASSI_PER_FRAME)):
        S.passo_test()
        for _ in range(int(S.PASSI_PER_FRAME)):
            S.scuoti_vuoto(net)
            net.step()
            # --- la verifica del passo PRECEDENTE, dopo la calibrazione di `:4189`
            if pend is not None:
                idx, med = pend
                idx = idx[idx < len(net.peq)]
                v = np.asarray(net.peq)[idx]
                nan_residui += int(np.sum(~np.isfinite(v)))
                # ⚠ LA DISPERSIONE FRA GLI ARCHI DELLO STESSO EVENTO, dopo la calibrazione.
                #   E' QUESTO il contrasto fra legge GLOBALE e legge LOCALE:
                #     globale -> UN SOLO numero per tutti  -> dispersione ZERO alla nascita
                #     locale  -> UN numero CIASCUNO        -> dispersione PIENA
                if len(v) > 1 and med > 0 and np.all(np.isfinite(v)):
                    scarti.append(float(np.std(v)) / med)
                pend = None
            net.mitosi()
            nc = getattr(net, "_g_nati_schwinger", 0) - prec_nc
            prec_nc = getattr(net, "_g_nati_schwinger", 0)
            if nc > 0:
                p = np.asarray(net.peq)
                # ⚠ GLI ARCHI DI SCHWINGER SI IDENTIFICANO DAGLI ANTINODI, NON DALLA POSIZIONE.
                #   La prima versione prendeva «gli ultimi `2*nc`» e sbagliava in 1 evento su 17
                #   (`nasc_zero = 0.9412` invece di `1.0`): un'assunzione sull'ORDINE degli
                #   append, non un fatto. Gli antinodi sono gli ULTIMI `nc` NODI (`k = self.n +
                #   arange(nc)` nel blocco Schwinger) e ciascuno ha ESATTAMENTE due archi.
                anti = np.arange(net.n - nc, net.n)
                ii_, jj_ = np.asarray(net.i), np.asarray(net.j)
                msk = np.isin(ii_, anti) | np.isin(jj_, anti)
                k = np.where(msk)[0]
                nan_dopo_mitosi += int(np.sum(~np.isfinite(p[k])))
                attesi += int(2 * nc)
                # la controprova dell'identificazione: due archi per antinodo, ne' uno di piu'
                if len(k) != 2 * nc:
                    ident_male += 1
                # ⚠ LA DISPERSIONE ALLA NASCITA, misurata NELL'ISTANTE GIUSTO: subito dopo la
                #   `mitosi()`, PRIMA che il rilassamento di `:4206` muova qualunque cosa.
                #   A legge GLOBALE vale ZERO ESATTO (un solo numero per tutti); a legge LOCALE
                #   i valori sono `nan` e la dispersione si misura DOPO la calibrazione.
                if len(k) > 1 and np.all(np.isfinite(p[k])):
                    _m = float(np.nanmedian(p))
                    if _m > 0:
                        disp_nascita.append(float(np.std(p[k])) / _m)
                    # e il criterio DIRETTO del ramo SPENTO: il valore E' la mediana, per tutti
                    uguali_med += int(np.sum(p[k] == _m))
                    tot_nati += int(len(k))
                for nome in PULITI:
                    x = np.asarray(getattr(net, nome, np.zeros(0)), dtype=float)
                    nan_altrove += int(np.sum(~np.isfinite(x)))
                pend = (k, float(np.nanmedian(p)))
            net.rilassa_disegno(); net.memoria_hebbiana_moto()
    np.savez(outp, **{k: np.asarray(getattr(net, k)) for k in CAMPI if hasattr(net, k)})
    sc = np.asarray(scarti) if scarti else np.zeros(0)
    dn = np.asarray(disp_nascita) if disp_nascita else np.zeros(0)
    print("C2 eventi=%d attesi=%d nan_mitosi=%d nan_residui=%d nan_altrove=%d "
          "n_ev=%d disp_dopo=%.6e n_nasc=%d disp_nascita=%.6e nasc_zero=%.4f "
          "uguali_med=%d tot_nati=%d ident_male=%d cal=%d uguali_rho=%d vs_med=%d "
          "scarto_max=%.6e nan_fine=%d"
          % (getattr(net, "_g_nati_schwinger_ev", 0), attesi, nan_dopo_mitosi, nan_residui,
             nan_altrove, len(sc), float(np.median(sc)) if len(sc) else -1.0,
             len(dn), float(np.median(dn)) if len(dn) else -1.0,
             float(np.mean(dn == 0.0)) if len(dn) else -1.0,
             uguali_med, tot_nati, ident_male,
             getattr(net, "_g_peqn_cal", 0), getattr(net, "_g_peqn_uguali_rho", 0),
             getattr(net, "_g_peqn_vs_med", 0), getattr(net, "_g_peqn_scarto_max", -1.0),
             int(np.sum(~np.isfinite(np.asarray(net.peq, dtype=float))))))
    raise SystemExit(0)


def gira(*extra):
    pr = subprocess.run([sys.executable, os.path.abspath(__file__)] + list(extra),
                        cwd=RADICE, capture_output=True, text=True,
                        encoding="utf-8", errors="replace")
    if pr.returncode != 0:
        print(pr.stdout[-1500:]); print(pr.stderr[-2500:])
        raise SystemExit("lavoratore uscito con %d" % pr.returncode)
    return pr.stdout


def leggi(out):
    import re
    m = re.search(r"C2 eventi=(\d+) attesi=(\d+) nan_mitosi=(\d+) nan_residui=(\d+) "
                  r"nan_altrove=(\d+) n_ev=(\d+) disp_dopo=(\S+) n_nasc=(\d+) "
                  r"disp_nascita=(\S+) nasc_zero=(\S+) uguali_med=(\d+) tot_nati=(\d+) "
                  r"ident_male=(\d+) cal=(\d+) uguali_rho=(\d+) vs_med=(\d+) "
                  r"scarto_max=(\S+) nan_fine=(\d+)", out)
    if not m:
        raise SystemExit("output del lavoratore non riconosciuto:\n%s" % out[-800:])
    return dict(eventi=int(m.group(1)), attesi=int(m.group(2)), nan_mit=int(m.group(3)),
                nan_res=int(m.group(4)), nan_alt=int(m.group(5)), n_sc=int(m.group(6)),
                disp_dopo=float(m.group(7)), n_nasc=int(m.group(8)),
                disp_nasc=float(m.group(9)), nasc_zero=float(m.group(10)),
                ug_med=int(m.group(11)), tot_nati=int(m.group(12)),
                ident_male=int(m.group(13)), cal=int(m.group(14)),
                ug_rho=int(m.group(15)), vs_med=int(m.group(16)),
                scarto_max=float(m.group(17)), nan_fine=int(m.group(18)))


def main():
    base = os.path.join(RADICE, "csv", "_seal_fork", "_sig_peq_nascita")
    os.makedirs(base, exist_ok=True)
    esiti = []

    q = subprocess.run(["git", "cat-file", "-p", "%s:soliton_simulator.py" % COMMIT_PRIMA],
                       cwd=RADICE, capture_output=True)
    if q.returncode != 0:
        raise SystemExit("non riesco a estrarre il simulatore di %s" % COMMIT_PRIMA)
    bp = hashlib.sha1(q.stdout).hexdigest()[:8]
    if bp != BLOB_PRIMA:
        raise SystemExit("[Q1] blob di %s = %s, atteso %s: termine di paragone SBAGLIATO"
                         % (COMMIT_PRIMA, bp, BLOB_PRIMA))
    prima = os.path.join(base, "_sim_prima.py")
    with open(prima, "wb") as fh:
        fh.write(q.stdout)
    print("sim PRIMA (%s): sha1 GREZZO %s" % (COMMIT_PRIMA, bp))
    print("sim SUL DISCO      : sha1 GREZZO %s\n"
          % hashlib.sha1(open(SIM_ORA, "rb").read()).hexdigest()[:8])

    pA = os.path.join(base, "A_prima.npz")
    pB = os.path.join(base, "B_spento.npz")
    pC = os.path.join(base, "C_acceso.npz")
    print("braccio A (prima della cura)...")
    gira("--lavoro", "--sim=%s" % prima, "--out=%s" % pA)
    print("braccio B (disco, flag SPENTO)...")
    oB = gira("--lavoro", "--sim=%s" % SIM_ORA, "--out=%s" % pB)
    print("braccio C (disco, flag ACCESO)...")
    oC = gira("--lavoro", "--sim=%s" % SIM_ORA, "--out=%s" % pC, "--cura")
    print("")
    B_, C_ = leggi(oB), leggi(oC)

    A, B, C = np.load(pA), np.load(pB), np.load(pC)
    f1 = [k for k in CAMPI if k in A and k in B
          and (A[k].shape != B[k].shape or not np.array_equal(A[k], B[k]))]
    com = sum(1 for k in CAMPI if k in A and k in B)
    esiti.append(("Q1", (not f1) and com >= 10,
                  "flag SPENTO = prima della cura: %d campi -> %s"
                  % (com, "BYTE-IDENTICI" if not f1 else "DIVERSI: %s" % f1[:5])))

    dif = [k for k in CAMPI if k in B and k in C
           and (B[k].shape != C[k].shape or not np.array_equal(B[k], C[k]))]
    esiti.append(("Q2", len(dif) > 0,
                  "CONTROLLO POSITIVO: ACCESO vs SPENTO differiscono su %d campi%s"
                  % (len(dif), "" if dif else "   *** IL FLAG E' INERTE: codice morto ***")))

    ok3 = (C_["nan_mit"] == C_["attesi"] and C_["attesi"] > 0 and B_["nan_mit"] == 0)
    esiti.append(("Q3", ok3,
                  "`nan` dopo mitosi: ACCESO %d su %d attesi, SPENTO %d (deve essere 0). "
                  "Eventi Schwinger: %d" % (C_["nan_mit"], C_["attesi"], B_["nan_mit"],
                                            C_["eventi"])))

    esiti.append(("Q4", C_["nan_res"] == 0 and C_["n_sc"] > 0,
                  "dopo il passo dopo restano %d `nan` (deve essere 0) su %d archi verificati: "
                  "la CALIBRAZIONE di `:4189` HA GIRATO" % (C_["nan_res"], C_["n_sc"])))

    esiti.append(("Q5", C_["nan_alt"] == 0,
                  "`nan` altrove (d, d0, vd, psi, tw, phi): %d (deve essere 0)" % C_["nan_alt"]))

    # Q6: la LEGGE e' cambiata. A flag SPENTO il valore E' la mediana (scarto ~0 su tutti);
    #     a flag ACCESO se ne discosta.
    # ⚠ IL CRITERIO E' STATO CORRETTO, ED ERA MIO L'ERRORE, non della cura. La prima versione
    #   confrontava i valori DOPO il passo successivo, quando il rilassamento di `:4206` li ha
    #   gia' mossi in ENTRAMBI i rami: dava `1.0000` contro `1.0000`, cioe' ASSENZA DI CONTRASTO
    #   letta come assenza di effetto. E' il presidio del par.9: **un criterio si scrive DA UNA
    #   MISURA, non dal proprio modello mentale del codice** -- ed e' la quarta volta in questo
    #   repo.
    #   LA DIFFERENZA VERA fra legge GLOBALE e legge LOCALE e':
    #     globale -> UN SOLO numero per TUTTI gli archi dell'evento -> dispersione ZERO ESATTO
    #     locale  -> UN numero CIASCUNO                             -> dispersione PIENA
    #   e si misura ALLA NASCITA per il ramo spento, DOPO LA CALIBRAZIONE per quello acceso.
    # ⚠⚠ E LA SECONDA VERSIONE ERA **VUOTA** -- rilievo di Luca, ed e' esatto.
    #   Diceva *«a flag acceso la dispersione dev'essere >= 100 volte quella a flag spento»*, ma a
    #   flag spento quella dispersione **e' ZERO ESATTO alla nascita**: `100 * 0 = 0`, quindi
    #   **sarebbe passata con QUALUNQUE valore, anche nullo.** Un criterio che non puo' fallire
    #   non e' un criterio.
    #   ⚠ E nel giro in cui e' stata provata NON ha fallito per quel motivo: il confronto usava la
    #     dispersione DOPO UN PASSO (`2.434e-01`), non quella alla nascita. **Era vuota in linea di
    #     principio e fuorviante in pratica: due difetti, non uno.**
    #
    # LA TERZA VERSIONE E' DIRETTA, e misura quello che la cura DICHIARA:
    #   ACCESO  -> ogni arco di Schwinger passa dalla legge LOCALE (`cal == attesi`), il valore
    #              assegnato E' la `rho` del PROPRIO arco (`uguali_rho == cal`, uguaglianza
    #              ESATTA, misurata NEL punto di calibrazione), e DIFFERISCE dalla mediana
    #              globale (`vs_med == cal`);
    #   SPENTO  -> il valore E' la mediana globale, su TUTTI gli archi (`ug_med == tot_nati`).
    # Nessun fattore scelto, nessuna soglia: sono uguaglianze e conteggi.
    # ⚠ L'EFFETTO DI BORDO, misurato invece che ignorato: gli archi dell'ULTIMO evento
    #   nascono dopo l'ultimo `step()` e **non sono ancora stati calibrati**. Restano `nan` a
    #   fine finestra, e il criterio li CONTA: `cal + nan_fine == attesi`. Senza, il sigillo
    #   avrebbe detto `86 su 88` e sarei andato a cercare un difetto che non c'e'.
    ok6 = (C_["cal"] + C_["nan_fine"] == C_["attesi"] and C_["attesi"] > 0
           and C_["ug_rho"] == C_["cal"] and C_["vs_med"] == C_["cal"]
           and B_["tot_nati"] > 0 and B_["ug_med"] == B_["tot_nati"]
           and B_["cal"] == 0 and C_["ident_male"] == 0 and B_["ident_male"] == 0)
    esiti.append(("Q6", ok6,
                  "DIRETTO -- ACCESO: calibrati LOCALMENTE %d + %d ancora in attesa a fine "
                  "finestra = %d attesi; di cui %d uguali alla `rho` del PROPRIO arco e %d "
                  "DIVERSI dalla mediana globale (scarto max %.3e). SPENTO: %d su %d valori "
                  "uguali alla MEDIANA. Identificazione sbagliata in %d+%d eventi (deve essere 0)."
                  % (C_["cal"], C_["nan_fine"], C_["attesi"], C_["ug_rho"], C_["vs_med"],
                     C_["scarto_max"], B_["ug_med"], B_["tot_nati"], C_["ident_male"],
                     B_["ident_male"])))

    print("-" * 94)
    for nome, ok, testo in esiti:
        print("%-4s %-4s %s" % (nome, "PASS" if ok else "FAIL", testo))
    print("-" * 94)
    n_ok = sum(1 for _, ok, _ in esiti if ok)
    print("SIGILLO PEQ_NASCITA_LOCALE: %d/%d" % (n_ok, len(esiti)))
    print("")
    if n_ok == len(esiti):
        print("VERDETTO: la cura C2 e' INERTE a flag spento, NON e' codice morto, il `nan` e' una")
        print("  CONSEGNA e non una perdita, e la nascita di `peq` e' diventata LOCALE.")
    else:
        print("VERDETTO: *** BLOCCANTE: la cura C2 non si accende. ***")
    print("")
    print("LIMITI: UN seme, UNA scena, %d passi. Prova che la LEGGE e' cambiata e che il" % PASSI)
    print("  meccanismo e' pulito, NON che la fisica risultante sia migliore.")
    return 0 if n_ok == len(esiti) else 1


if __name__ == "__main__":
    sys.exit(main())
