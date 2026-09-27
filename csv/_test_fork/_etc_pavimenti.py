# -*- coding: utf-8 -*-
"""**GLI 8 PAVIMENTI DEL GRUPPO 1: GIRANO DAVVERO COL DRIVER? Verifica A RUNTIME.**

**Che cosa decide** *(mandato di Luca del 2026-09-27 su `533f54f`)*: la FASE 0-bis aveva elencato
**8 scritture non esprimibili come variazione**, tutte pavimenti -- `_pav_d0` **7 volte** su `d0`
e `np.maximum(self.d + dts*self.vd, 0.05)` **una volta** su `d`. **Ma l'analisi era STATICA**, e un
sito che non gira non e' un bivio di teoria: e' codice morto.
**Se sono TUTTI MORTI col driver, si archiviano con la cura. Se anche UNO e' vivo, SI FERMA.**

**COME LO PROVA, e non si fida dei contatori soli:**
1. **COPERTURA DI RIGA** con `sys.settrace` ristretto a `soliton_simulator.py`: si registra
   **quali righe hanno ESEGUITO**. Una riga che non compare **non e' girata**. E' la prova
   diretta, perche' guarda l'esecuzione e non un'inferenza sui flag.
2. **I CONTATORI gia' cablati** (`_g_sm_pav_saltati`, `_g_smp_d_chiusure`, `_g_smp_passanti`),
   che sono la corroborazione indipendente: dicono **quante volte** il ramo vivo e' passato.
3. **L'ARGV DEL DRIVER, non ricostruito**: `_cli_flag.argv_del_driver` esegue il testo del driver
   fino all'ancora e restituisce la `sys.argv` che **il driver** ha costruito.

**⚠ IL LIMITE (`A9`):** la copertura prova **cio' che e' girato in QUESTA esecuzione**. Un ramo
che scatta solo in un regime raro (un `nsub` diverso, una scena diversa) **non si vedrebbe**.
Per questo si gira la **scena del pilota** con lo **stesso argv**, e si dichiara il numero di passi.

COMANDO:  python csv/_test_fork/_etc_pavimenti.py [--passi N]
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
import _cli_flag  # noqa: E402
import _passo  # noqa: E402

SIM = os.path.join(RADICE, "soliton_simulator.py")

# ------------------------------------------------------------------ i siti, per NOME e per RIGA
# (riga, che cos'e', "MORTO se ..." )
SITI = [
    (4453, "_pav_d0: il ramo INERTE `if SCALA_MIN or SCALA_MIN_PASSO: return v`", "ramo vivo"),
    (4456, "_pav_d0: IL PAVIMENTO `np.maximum(v, self._floor_d0())`", "IL PAVIMENTO SU d0"),
    (5733, "Verlet: `d_new = self.d + dts * vd_half`  (SCALA_MIN_PASSO, senza pavimento)", "ramo vivo"),
    (5737, "Verlet: IL PAVIMENTO `np.maximum(self.d + dts*vd_half, 0.05)`", "IL PAVIMENTO SU d (Verlet)"),
    (5778, "Eulero: `self.d = self.d + dts * self.vd`  (SCALA_MIN_PASSO, senza pavimento)", "ramo vivo"),
    (5782, "Eulero: IL PAVIMENTO `np.maximum(self.d + dts*self.vd, 0.05)`", "IL PAVIMENTO SU d (Eulero)"),
    (5789, "IL FRENO DI SCALA MINIMA, UNA VOLTA SOLA dopo i sotto-passi (C3)", "il freno"),
]
CHIAMATE_PAV = [5899, 6157, 6664, 6817, 6840, 6994, 7042]   # i 7 siti che CHIAMANO `_pav_d0`
BERSAGLI = set(r for r, _a, _b in SITI) | set(CHIAMATE_PAV)

VISTE = {}


def _traccia(frame, evento, _arg):
    if frame.f_code.co_filename != SIM:
        return None
    if evento == "line":
        n = frame.f_lineno
        if n in BERSAGLI:
            VISTE[n] = VISTE.get(n, 0) + 1
    return _traccia


def principale():
    passi = 3
    for a in sys.argv[1:]:
        if a.startswith("--passi="):
            passi = int(a.split("=", 1)[1])

    S0, argv = _cli_flag.argv_del_driver(
        extra=["--seme=11"], dest=os.path.join(_QUI, "_scarto_cli"))
    print("ARGV COSTRUITO DAL DRIVER (non ricostruito), %d voci:" % len(argv))
    print("  " + " ".join(argv[1:]))
    print("")

    S, a = _cli_flag.carica_dal_cli(list(argv), nome="sim_pav")
    FLAG = {k: bool(getattr(S, k, False))
            for k in ("SCALA_MIN", "SCALA_MIN_PASSO", "VERLET", "PAV_COM", "SEMINA_LAM",
                      "MITOSI_2LAM", "POZZO_D")}
    print("I FLAG CHE DECIDONO, letti dal MODULO CONFIGURATO DAL DRIVER:")
    for k, v in FLAG.items():
        print("  %-18s %s" % (k, "ACCESO" if v else "spento"))
    print("")
    print("  -> INTEGRATORE VIVO: %s" % ("VERLET (sottociclo a salto della rana)"
                                         if FLAG["VERLET"] else "EULERO ESPLICITO"))
    print("")

    S._NMASSE_VIDEO["n"] = 2
    S._NMASSE_VIDEO["sep"] = 3.0
    S._NMASSE_VIDEO["size"] = None
    S.avvia_test("MASSE-COERENTI")()
    net = S.net
    print("scena (ii)(a) avviata: n = %d nodi, m = %d archi" % (net.n, len(net.i)))
    print("GIRO %d PASSI PIENI con la copertura di riga attiva..." % passi)

    sys.settrace(_traccia)
    try:
        for _ in range(passi):
            _passo.passo_pieno(S, net)
    finally:
        sys.settrace(None)
    print("")

    # ------------------------------------------------------------------ il verdetto
    print("=" * 78)
    print("COPERTURA DI RIGA: quali siti hanno ESEGUITO in %d passi pieni" % passi)
    print("=" * 78)
    print("")
    print("  %-6s %-9s %-10s %s" % ("riga", "VIVO?", "esecuzioni", "che cos'e'"))
    vivi_pav = []
    for r, che, _et in SITI:
        n = VISTE.get(r, 0)
        print("  :%-5d %-9s %-10d %s" % (r, "SI" if n else "-- NO --", n, che))
        if n and ("PAVIMENTO" in che):
            vivi_pav.append((r, che))
    print("")
    print("  I 7 SITI CHE CHIAMANO `_pav_d0` (la chiamata avviene, il pavimento no):")
    for r in CHIAMATE_PAV:
        print("    :%-6d chiamate: %d" % (r, VISTE.get(r, 0)))
    chiamate_tot = sum(VISTE.get(r, 0) for r in CHIAMATE_PAV)

    print("")
    print("=" * 78)
    print("I CONTATORI GIA' CABLATI (corroborazione indipendente dalla copertura)")
    print("=" * 78)
    print("")
    CONT = {}
    for k in ("_g_sm_pav_saltati", "_g_smp_passanti",
              "_g_smp_aperture", "_g_smp_chiusure", "_g_smp_d_chiusure",
              "_g_smp_chirurgie", "_g_smp_disallineati", "_g_smp_d_nsub",
              "_g_sm_nascite", "_g_sm_patol"):
        CONT[k] = int(getattr(net, k, 0))
        print("  %-22s %d" % (k, CONT[k]))
    print("")
    print("  _g_sm_pav_saltati = %d  <->  chiamate a `_pav_d0` tracciate = %d"
          % (CONT["_g_sm_pav_saltati"], chiamate_tot))
    if CONT["_g_sm_pav_saltati"] == chiamate_tot and chiamate_tot > 0:
        print("  ### COINCIDONO: OGNI chiamata a `_pav_d0` e' uscita dal ramo INERTE.")
    elif chiamate_tot:
        print("  ⚠ NON coincidono: ci sono chiamate a `_pav_d0` che NON hanno saltato.")

    print("")
    print("  ### IL FRENO DI SCALA MINIMA E' GIA' >>UNA VOLTA PER PASSO PIENO<<?")
    print("    aperture  della fotografia (`_smp_apri`, a inizio `step`) : %d"
          % CONT["_g_smp_aperture"])
    print("    chiusure  del freno su d0 (`_smp_chiudi`, in `memoria_hebbiana_moto`): %d"
          % CONT["_g_smp_chiusure"])
    print("    chiusure  del freno su d  (dopo i sotto-passi metrici)    : %d"
          % CONT["_g_smp_d_chiusure"])
    print("    chirurgie sullo snapshot  (la mitosi lo riallinea)        : %d"
          % CONT["_g_smp_chirurgie"])
    print("    sotto-passi metrici nel passo peggiore (`nsub`)           : %d"
          % CONT["_g_smp_d_nsub"])
    _ok = (CONT["_g_smp_aperture"] == passi and CONT["_g_smp_chiusure"] == passi
           and CONT["_g_smp_d_chiusure"] == passi and CONT["_g_smp_disallineati"] == 0)
    print("    -> %s" % ("SI: una apertura e una chiusura per passo pieno, zero disallineati."
                         if _ok else
                         "NO: i conti non fanno %d. Guardare i disallineati." % passi))
    print("")
    print("=" * 78)
    if vivi_pav:
        print("### VERDETTO: ALMENO UN PAVIMENTO E' VIVO. MI FERMO.")
        for r, che in vivi_pav:
            print("    :%d  %s" % (r, che))
    else:
        print("### VERDETTO: TUTTI E 8 I PAVIMENTI SONO MORTI con l'argv del driver.")
        print("    Nessuna decisione di teoria serve ORA: si archiviano con la cura, e")
        print("    restano censiti in CLIP-INVENTARIO.")
    print("=" * 78)

    OUT = os.path.join(_QUI, "_etc_pavimenti.json")
    io.open(OUT, "w", encoding="utf-8", newline=chr(10)).write(json.dumps(
        {"argv": argv[1:], "flag": FLAG, "passi": passi, "n": int(net.n), "m": int(len(net.i)),
         "copertura": {str(k): v for k, v in sorted(VISTE.items())},
         "contatori": CONT, "pavimenti_vivi": [r for r, _c in vivi_pav],
         "blob_sim": _presidio.blob_file(SIM) if hasattr(_presidio, "blob_file") else None},
        indent=1, ensure_ascii=False, sort_keys=True))
    print("")
    print("scritto: " + OUT)
    return 1 if vivi_pav else 0


if __name__ == "__main__":
    sys.exit(principale())
