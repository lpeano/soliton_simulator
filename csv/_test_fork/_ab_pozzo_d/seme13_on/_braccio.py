# -*- coding: utf-8 -*-
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.join('C:\\Users\\lpeano\\soliton_simulator', "csv"))
import _cli_flag, _passo, _osservabile_p1 as OP
_S0, argv = _cli_flag.argv_del_driver(extra=["--seme=13"],
                                     dest=os.path.join('C:\\Users\\lpeano\\soliton_simulator', "csv", "_test_fork",
                                                       "_scarto_cli"))
argv = list(argv) + (["--pozzo-d"] if True else [])
S, a = _cli_flag.carica_dal_cli(argv, nome="sim_ab")
S._NMASSE_VIDEO["n"] = max(2, int(getattr(a, "nmasse", 2)))
S._NMASSE_VIDEO["sep"] = float(getattr(a, "sep", 3.0))
S._NMASSE_VIDEO["size"] = None
S.avvia_test("MASSE-COERENTI")()
coorti = S.test["dati"]["coorti"]
rr = float(S.test["dati"]["scena_ii"]["r_regione"])
o0 = OP.misura(S.net, coorti)                       # la distanza al PASSO 0
if hasattr(S, "passo_test"):
    S.passo_test()
for _ in range(120):
    _passo.passo_pieno(S, S.net)                    # `H-P9`: mai `net.step()` da solo
o1 = OP.misura(S.net, coorti)                       # e dopo i passi
fuori = {"seme": 13, "flag": bool(S.POZZO_D), "n0": int(o0["n"]), "n1": int(o1["n"]),
         "sep": float(S._NMASSE_VIDEO["sep"]), "r_regione": rr,
         "nonpos": int(getattr(S.net, "_pozzo_d_nonpos", -1)),
         "passo0": dict((k, float(v["centro_centro"])) for k, v in o0["coppie"].items()),
         "dopo": dict((k, float(v["centro_centro"])) for k, v in o1["coppie"].items())}
open('C:\\Users\\lpeano\\soliton_simulator\\csv\\_test_fork\\_ab_pozzo_d\\seme13_on\\misura.json', "w").write(json.dumps(fuori, sort_keys=True))
print("OK", 13, True, fuori["n0"], fuori["n1"])
