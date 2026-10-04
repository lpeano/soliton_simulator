# -*- coding: utf-8 -*-
import hashlib, json, os, sys
import numpy as np
sys.path.insert(0, os.path.join('C:\\Users\\lpeano\\soliton_simulator', "csv"))
import _cli_flag, _passo
_S0, argv = _cli_flag.argv_del_driver(dest=os.path.join('C:\\Users\\lpeano\\soliton_simulator', "csv", "_test_fork",
                                                        "_scarto_cli"))
argv = [x for x in argv] + []
S, a = _cli_flag.carica_dal_cli(argv, nome="sim_pd", sim='C:\\Users\\lpeano\\soliton_simulator\\soliton_simulator.py')
S._NMASSE_VIDEO["n"] = max(2, int(getattr(a, "nmasse", 2)))
S._NMASSE_VIDEO["sep"] = float(getattr(a, "sep", 3.0))
S._NMASSE_VIDEO["size"] = None
S.avvia_test("MASSE-COERENTI")()
if hasattr(S, "passo_test"):
    S.passo_test()
for _ in range(4):
    _passo.passo_pieno(S, S.net)          # `H-P9`: mai `net.step()` da solo
o = {"n": int(S.net.n), "archi": int(len(S.net.d)),
     "flag": bool(getattr(S, "POZZO_D", None)),
     "nonpos": int(getattr(S.net, "_pozzo_d_nonpos", -1)),
     "nonpos_tot": int(getattr(S.net, "_pozzo_d_tot", -1)), "firme": {}}
for k, v in sorted(vars(S.net).items()):
    if isinstance(v, np.ndarray):
        o["firme"][k] = "%s|%s|%s" % (v.shape, v.dtype,
                                       hashlib.sha1(v.tobytes()).hexdigest()[:16])
    elif isinstance(v, (int, float, bool)):
        o["firme"][k] = repr(v)
open('C:\\Users\\lpeano\\soliton_simulator\\csv\\_seal_fork\\_sig_pozzo_d\\dopo_off\\firme.json', "w").write(json.dumps(o, sort_keys=True))
print("OK", o["n"], o["archi"], o["flag"], o["nonpos"])
