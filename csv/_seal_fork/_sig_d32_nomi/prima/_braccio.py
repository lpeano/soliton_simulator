# -*- coding: utf-8 -*-
import hashlib, json, os, sys
import numpy as np
sys.path.insert(0, os.path.join('C:\\Users\\lpeano\\soliton_simulator', "csv"))
import _cli_flag, _passo
_S0, argv = _cli_flag.argv_del_driver(dest=os.path.join('C:\\Users\\lpeano\\soliton_simulator', "csv", "_test_fork",
                                                        "_scarto_cli"))
S, a = _cli_flag.carica_dal_cli(argv, nome="sim_n1", sim='C:\\Users\\lpeano\\soliton_simulator\\csv\\_seal_fork\\_sig_d32_nomi\\_sim_prima.py')
S._NMASSE_VIDEO["n"] = max(2, int(getattr(a, "nmasse", 2)))
S._NMASSE_VIDEO["sep"] = float(getattr(a, "sep", 3.0))
S._NMASSE_VIDEO["size"] = None
S.avvia_test("MASSE-COERENTI")()
# ⚠ `passo_pieno`, NON le cinque chiamate A MANO: la prima correzione le ricopiava, cioe'
#   aggiungeva il ventiseiesimo posto in cui quell'ordine vive CABLATO. `_passo.passo_pieno`
#   LEGGE l'ordine dal codice e RIFIUTA di girare se simulatore e driver divergono.
#   (`net.step()` da solo chiamava `mitosi()` ZERO volte: misurato, 0 in 14 giri.)
S.passo_test()
for _ in range(12):
    _passo.passo_pieno(S, S.net)
o = {"n": int(S.net.n), "archi": int(len(S.net.d)), "firme": {},
     "taupp_tot": int(getattr(S.net, "_rep_taupp_tot", 0)),
     "mitosi_eventi": int(getattr(S.net, "_mit_eventi", -1))}
for k, v in sorted(vars(S.net).items()):
    if isinstance(v, np.ndarray):
        o["firme"][k] = "%s|%s|%s" % (v.shape, v.dtype,
                                       hashlib.sha1(v.tobytes()).hexdigest()[:16])
    elif isinstance(v, (int, float, bool)):
        o["firme"][k] = repr(v)
open('C:\\Users\\lpeano\\soliton_simulator\\csv\\_seal_fork\\_sig_d32_nomi\\prima\\firme.json', "w").write(json.dumps(o, sort_keys=True))
print("OK", o["n"], o["archi"], len(o["firme"]))
