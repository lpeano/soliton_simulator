# -*- coding: utf-8 -*-
"""IL SIGILLO DI **<<VIA IL `0.3`>>** — `S0`, `S1`, `S2`.

*(Decisione di Luca del 2026-10-06. I tre bracci e il criterio sono fissati in
`doc/TASK_HISTORY/2026-10-06_via-il-03-mitosi-soglia-grad.md`, committato **prima** in
`e693993`.)*

| | che cosa pretende |
|---|---|
| **`S0`** | il blob di **PRIMA** piu' la patch e' **byte-identico** al blob di oggi, e i due girano `150` passi con **tutti gli attributi di `net` identici** *(`_calcpsi_origini` **aggregato per nome**)* |
| **`S1`** | ### ⛔ **IL CONTROLLO FORTE:** il blob nuovo riproduce **AL BIT** i conteggi per passo di `amp0.json` *(il braccio `_AMP = 0` di `6cfcc4e`)* sui primi `150` passi |
| **`S2`** | il blob nuovo **DEVE differire** da `amp0_3.json`, e si riporta **il primo passo diverso** |

### ⛔ **SE `S1` NON COINCIDE, LA PATCH FA ALTRO: il sigillo FALLISCE e lo dice.** E' l'unico
### braccio che puo' smentire il ragionamento algebrico *(`soglia0·(1 − 0·tanh x) = soglia0`
### esattamente, e la riga non tocca il generatore casuale)*, e quel ragionamento e' l'unica
### ragione per cui mi aspetto l'identita'.

# ESENTE-H-P8: il codice di prima si prende dal PADRE del commit della patch, con
#   `_cli_flag.sim_prima_del_flag`, e NON da `HEAD`. La stringa qui sotto lo documenta.

USO:  python csv/_seal_fork/_sigillo_mitosi_soglia_grad_via.py  [--passi=N]
"""
import contextlib
import io
import json
import os
import pickle
import subprocess
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
sys.path.insert(0, os.path.join(RADICE, "csv"))
sys.path.insert(0, os.path.join(RADICE, "csv", "_test_fork"))
import _presidio   # noqa: E402

_presidio.avvia(__file__)

import _passo                                    # noqa: E402
import _cli_flag                                 # noqa: E402
import _tors_w8_lunga as LUNGA                   # noqa: E402

blob, carica, q = LUNGA.blob, LUNGA.carica, LUNGA.q
stampa, riga = LUNGA.stampa, LUNGA.riga

NL = chr(10)
FUORI = os.path.join(RADICE, "csv", "_seal_fork", "_sigillo_mitosi_soglia_grad_via")
SIM = os.path.join(RADICE, "soliton_simulator.py")
PATCH = os.path.join(_QUI, "_mitosi_soglia_grad_via_patch.py")
D_MZD = os.path.join(RADICE, "csv", "_test_fork", "_mitosi_zero_dove")
# ### ⛔ **`230` E NON `150`, e la ragione e' un NUMERO DEL MANDATO STESSO:** `S2`
#   pretende che il blob nuovo ### **DIFFERISCA** da `amp0_3.json`, e il primo passo
#   diverso -- misurato in `27c10bd` -- e' il ### **`212`**. ### **A `150` passi `S2`
#   NON PUO' PASSARE PER COSTRUZIONE**, perche' fino al `211` i due bracci sono
#   ### **identici.** ### **Il collaudo a `2` passi me l'ha mostrato subito:** `S2`
#   falliva, e ### **falliva giustamente.** ### **`S0` e `S1` restano piu' forti**
#   su `230` che su `150`, quindi allungare non indebolisce niente.
PASSI = 230

# ### ⛔ **GLI ATTRIBUTI CHE LA PATCH TOGLIE DI PROPOSITO**, ed e' l'unica esclusione di `S0`.
#   ### **Si dichiara, non si tace:** un'esclusione taciuta e' un insabbiamento, e il
#   `C-letture` di `1b5b651` e' fallito proprio per non averla dichiarata.
TOLTI = ("_tum_r_tot", "_tum_r_salti", "_tum_r_forma", "_tum_r_quando")
# ### I CAMPI DI `S1`, dal mandato: *«`n`, archi, divisioni, Schwinger, quantili di `|tw|`»*.
CAMPI_S1 = ("n", "archi", "nati_tot", "schwinger_tot")


def _byte(p):
    return io.open(p, "rb").read()


def dal_padre(dst):
    """Il simulatore del PADRE del commit della patch, ### **in BINARIO.**

    ### ⛔ **NON `git checkout`:** la trappola `CRLF` dei tre stati *(`par.7`)*.
    """
    # ### ⛔ **IL PADRE SI TROVA DAL COMMIT CHE HA INTRODOTTO LA PATCH, col log.**
    #   ### **NON con `_cli_flag.sim_prima_del_flag`:** quella funzione cerca un
    #   ### **FLAG introdotto nel simulatore**, e qui non c'e' nessun flag nuovo -- la
    #   cura e' una ### **RIMOZIONE.** ### **Il collaudo a `2` passi me l'ha mostrato
    #   subito**, e una chiamata sbagliata sarebbe stata un'ancora che si crede solida
    #   e non lo e'.
    r = subprocess.run(["git", "log", "--format=%H", "-1", "--",
                        "csv/_seal_fork/_mitosi_soglia_grad_via_patch.py"],
                       capture_output=True, text=True, cwd=RADICE)
    c = r.stdout.strip()
    if not c:
        raise SystemExit("[FERMO] non trovo il commit che ha introdotto la patch.")
    pad = c + "~1"
    g = subprocess.run(["git", "cat-file", "-p", "%s:soliton_simulator.py" % pad],
                       capture_output=True, cwd=RADICE)
    if g.returncode or not g.stdout:
        raise SystemExit("[FERMO] non riesco a leggere il simulatore dal padre `%s`." % pad)
    io.open(dst, "wb").write(g.stdout)
    return pad


def _foto(net):
    """TUTTI gli attributi di `net`. Array per `sha1` dei byte, il resto per `pickle`.

    `_calcpsi_origini` si ### **AGGREGA PER NOME**, perche' le sue chiavi contengono
    ### **numeri di riga** -- e la patch ne ha tolte `22`, quindi le righe ### **si sono
    spostate per costruzione.**
    """
    import hashlib
    out = {}
    for k in sorted(dir(net)):
        if k.startswith("__"):
            continue
        try:
            v = getattr(net, k)
        except Exception:
            continue
        if callable(v):
            continue
        if k == "_calcpsi_origini":
            try:
                agg = {}
                for kk, vv in dict(v).items():
                    nome = str(kk).split(":")[0].split("(")[0]
                    agg[nome] = agg.get(nome, 0) + (vv if isinstance(vv, int) else 1)
                out[k] = repr(sorted(agg.items()))
            except Exception as e:
                out[k] = "### non aggregabile: %r" % (e,)
            continue
        try:
            if isinstance(v, np.ndarray):
                out[k] = hashlib.sha1(np.ascontiguousarray(v).tobytes()).hexdigest()
            else:
                out[k] = hashlib.sha1(pickle.dumps(v, 4)).hexdigest()
        except Exception:
            try:
                out[k] = "repr:" + hashlib.sha1(repr(v).encode()).hexdigest()
            except Exception as e:
                out[k] = "### illeggibile: %r" % (e,)
    return out


def gira(nome, sorgente, passi, con_ganci=True):
    """Gira `passi` passi e torna `(per_passo, foto_finale, foto_per_passo)`."""
    dst = os.path.join(FUORI, "_sim_%s.py" % nome)
    if con_ganci:
        LUNGA.copia_patchata(sorgente, dst)
    else:
        io.open(dst, "wb").write(_byte(sorgente))
    S, N, _a = carica("sig_%s" % nome, dst)
    m = LUNGA.Misura(S.DT) if con_ganci else None
    if m is not None:
        S._MIS = m
    foto = []
    for k in range(1, passi + 1):
        if m is not None:
            m.passo = k
        with contextlib.redirect_stdout(io.StringIO()):
            _passo.passo_pieno(S, N)
        if m is not None:
            m.chiudi(N)
        foto.append(_foto(N))
    return (m.passi if m is not None else []), _foto(N), foto, blob(dst)


def s0(passi):
    """`S0`: ### **la copia di prima PIU' la patch e' il blob di oggi**, e i due girano
    identici."""
    if not os.path.isdir(FUORI):
        os.makedirs(FUORI)
    prima = os.path.join(FUORI, "_prima.py")
    pad = dal_padre(prima)
    ricostruito = os.path.join(FUORI, "_ricostruito.py")
    r = subprocess.run([sys.executable, PATCH, prima, ricostruito],
                       capture_output=True, text=True, cwd=RADICE)
    if r.returncode:
        return {"passa": False, "perche": "la patch non gira sul padre", "uscita": r.stdout}
    uguale = _byte(ricostruito) == _byte(SIM)
    return {"padre": pad, "blob_prima": blob(prima)[:8],
            "blob_ricostruito": blob(ricostruito)[:8], "blob_oggi": blob(SIM)[:8],
            "byte_identico": uguale, "passa": uguale, "prima": prima}


def s0b(prima, passi):
    """`S0` braccio dinamico: `prima` e `oggi` girano `passi` passi ### **identici.**"""
    _p1, _f1, F1, b1 = gira("prima", prima, passi, con_ganci=False)
    _p2, _f2, F2, b2 = gira("oggi", SIM, passi, con_ganci=False)
    diff, esclusi, tot = [], set(), 0
    for k in range(passi):
        a, b = F1[k], F2[k]
        for nome in sorted(set(a) | set(b)):
            if nome in TOLTI:
                esclusi.add(nome)
                continue
            tot += 1
            if a.get(nome) != b.get(nome):
                diff.append((k + 1, nome))
    return {"passi": passi, "attributi_confrontati": tot, "differenze": diff[:30],
            "n_differenze": len(diff), "esclusi": sorted(esclusi),
            "blob_prima": b1[:8], "blob_oggi": b2[:8],
            "passa": bool(tot) and not diff}


def _confronta(PP, rif, campi):
    """Confronta i conteggi per passo ### **AL BIT.**"""
    A = {int(x["passo"]): x for x in PP}
    B = {int(x["passo"]): x for x in (rif.get("passi_dati") or [])}
    com = sorted(set(A) & set(B))
    diff, nq = [], 0
    for p in com:
        for c in campi:
            if A[p].get(c) != B[p].get(c):
                diff.append((p, c, A[p].get(c), B[p].get(c)))
        qa, qb = A[p].get("q_tw") or {}, B[p].get("q_tw") or {}
        for z in sorted(set(qa) | set(qb)):
            nq += 1
            if qa.get(z) != qb.get(z):
                diff.append((p, "q_tw." + z, qa.get(z), qb.get(z)))
    return com, diff, nq


def main(argv):
    passi = PASSI
    for a in argv[1:]:
        if a.startswith("--passi="):
            passi = int(a.split("=", 1)[1])
    if not os.path.isdir(FUORI):
        os.makedirs(FUORI)
    riga("=")
    stampa("IL SIGILLO DI <<VIA IL 0.3>> -- %d passi" % passi)
    riga("=")
    stampa("  simulatore di oggi: %s" % blob(SIM)[:8])
    stampa()

    riga("-")
    stampa("S0 (a): la copia di PRIMA piu' la patch e' il blob di OGGI")
    riga("-")
    A = s0(passi)
    for k in sorted(A):
        if k != "prima":
            stampa("   %-20s %s" % (k, A[k]))
    stampa("   ### %s" % ("✔ PASSA" if A["passa"] else "⛔ FALLISCE"))
    if not A["passa"]:
        _scrivi({"S0a": A, "esito": 1})
        stampa()
        stampa("### S0 (a) FALLISCE: mi fermo. La patch non ricostruisce il blob di oggi.")
        return 1
    stampa()

    riga("-")
    stampa("S0 (b): PRIMA e OGGI girano %d passi con TUTTI gli attributi di net identici"
           % passi)
    riga("-")
    B = s0b(A["prima"], passi)
    for k in ("passi", "attributi_confrontati", "n_differenze", "esclusi",
              "blob_prima", "blob_oggi"):
        stampa("   %-24s %s" % (k, B[k]))
    if B["differenze"]:
        stampa("   le prime differenze (passo, attributo):")
        for z in B["differenze"][:10]:
            stampa("      %s" % (z,))
    stampa("   ### E GLI ESCLUSI SONO QUELLI CHE LA PATCH TOGLIE DI PROPOSITO, e si")
    stampa("       DICHIARANO: %s" % (B["esclusi"] or "nessuno"))
    stampa("   ### %s" % ("✔ PASSA" if B["passa"] else "⛔ FALLISCE"))
    stampa()

    riga("-")
    stampa("S1: il blob NUOVO riproduce AL BIT i conteggi di amp0.json (il braccio _AMP = 0)")
    riga("-")
    PP, _f, _F, bn = gira("nuovo", SIM, passi, con_ganci=True)
    rif0 = json.loads(io.open(os.path.join(D_MZD, "amp0.json"), encoding="utf-8").read())
    com, diff, nq = _confronta(PP, rif0, CAMPI_S1)
    C = {"passi_confrontati": len(com), "campi": list(CAMPI_S1),
         "quantili_confrontati": nq, "n_differenze": len(diff),
         "differenze": diff[:30], "materia": len(com) * len(CAMPI_S1) + nq,
         "passa": bool(com) and not diff, "blob_copia": bn[:8]}
    for k in ("passi_confrontati", "quantili_confrontati", "materia", "n_differenze"):
        stampa("   %-24s %s" % (k, C[k]))
    if diff:
        stampa("   le prime differenze (passo, campo, nuovo, amp0.json):")
        for z in diff[:10]:
            stampa("      %s" % (z,))
    stampa("   ### %s" % ("✔ PASSA" if C["passa"] else "⛔ FALLISCE"))
    if not C["passa"]:
        stampa()
        stampa("### ⛔ S1 FALLISCE: LA PATCH FA ALTRO. Mi fermo e lo scrivo.")
    stampa()

    riga("-")
    stampa("S2: il blob NUOVO DEVE differire da amp0_3.json (la legge CON il 0.3)")
    riga("-")
    rif3 = json.loads(io.open(os.path.join(D_MZD, "amp0_3.json"), encoding="utf-8").read())
    com3, diff3, nq3 = _confronta(PP, rif3, CAMPI_S1)
    primo = min((z[0] for z in diff3), default=None)
    quale = next((z for z in diff3 if z[0] == primo), None)
    D = {"passi_confrontati": len(com3), "n_differenze": len(diff3),
         "primo_passo_diverso": primo, "quale": quale,
         "materia": len(com3) * len(CAMPI_S1) + nq3, "passa": primo is not None}
    for k in ("passi_confrontati", "materia", "n_differenze", "primo_passo_diverso"):
        stampa("   %-24s %s" % (k, D[k]))
    stampa("   quale                    %s" % (quale,))
    stampa("   ### %s" % ("✔ PASSA" if D["passa"] else "⛔ FALLISCE"))
    stampa()

    riga("=")
    stampa("GLI ESITI")
    riga("=")
    for k, v in (("S0 (a) byte", A["passa"]), ("S0 (b) attributi", B["passa"]),
                 ("S1 (al bit)", C["passa"]), ("S2 (deve differire)", D["passa"])):
        stampa("  %-22s %s" % (k, "✔ PASSA" if v else "⛔ FALLISCE"))
    riga("=")
    ok = A["passa"] and B["passa"] and C["passa"] and D["passa"]
    _scrivi({"S0a": A, "S0b": B, "S1": C, "S2": D, "passi": passi,
             "blob_oggi": blob(SIM), "esito": 0 if ok else 1})
    return 0 if ok else 1


def _scrivi(d):
    if not os.path.isdir(FUORI):
        os.makedirs(FUORI)
    d = dict(d)
    d.pop("prima", None)
    for k in ("S0a",):
        if k in d and isinstance(d[k], dict):
            d[k] = {x: y for x, y in d[k].items() if x != "prima"}
    io.open(os.path.join(FUORI, "sigillo.json"), "w", encoding="utf-8").write(
        json.dumps(d, indent=1, default=str))


if __name__ == "__main__":
    sys.exit(main(sys.argv))
