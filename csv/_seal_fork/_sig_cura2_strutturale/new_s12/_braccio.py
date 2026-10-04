# -*- coding: utf-8 -*-
import hashlib, json, os, sys
import numpy as np
sys.path.insert(0, os.path.join('C:\\Users\\lpeano\\soliton_simulator', "csv"))
import _cli_flag, _passo
_S0, argv = _cli_flag.argv_del_driver(extra=['--seme=12'],
                                     dest=os.path.join('C:\\Users\\lpeano\\soliton_simulator', "csv", "_test_fork",
                                                       "_scarto_cli"))
argv = [x for x in argv if x != '']
S, a = _cli_flag.carica_dal_cli(argv, nome="sim_c2", sim='C:\\Users\\lpeano\\soliton_simulator\\soliton_simulator.py')
S._NMASSE_VIDEO["n"] = max(2, int(getattr(a, "nmasse", 2)))
S._NMASSE_VIDEO["sep"] = float(getattr(a, "sep", 3.0))
S._NMASSE_VIDEO["size"] = None
S.avvia_test("MASSE-COERENTI")()
# ⚠ `passo_pieno`, NON `net.step()`: legge l'ordine DAL CODICE e rifiuta se sim e driver divergono
if hasattr(S, "passo_test"):
    S.passo_test()
for _ in range(12):
    _passo.passo_pieno(S, S.net)
o = {"n": int(S.net.n), "archi": int(len(S.net.d)),
     "taupp_tot": int(getattr(S.net, "_rep_taupp_tot", 0)),
     "flag": bool(getattr(S, "TEMPO_UNICO_MITOSI", None)), "firme": {}}
for k, v in sorted(vars(S.net).items()):
    if isinstance(v, np.ndarray):
        o["firme"][k] = "%s|%s|%s" % (v.shape, v.dtype,
                                       hashlib.sha1(v.tobytes()).hexdigest()[:16])
    elif isinstance(v, (int, float, bool)):
        o["firme"][k] = repr(v)
open('C:\\Users\\lpeano\\soliton_simulator\\csv\\_seal_fork\\_sig_cura2_strutturale\\new_s12\\firme.json', "w").write(json.dumps(o, sort_keys=True))
print("OK", o["n"], o["archi"], o["taupp_tot"], o["flag"])
