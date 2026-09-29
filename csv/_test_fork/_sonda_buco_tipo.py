# -*- coding: utf-8 -*-
"""IL BUCO del controllo del tipo, MISURATO PRIMA della correzione (rilievo del guardiano)."""
import contextlib, copy, hashlib, io, os, sys
sys.path.insert(0, os.path.join(os.getcwd(), "csv"))
import _presidio
_presidio.avvia(__file__)
import numpy as np, _cli_flag, _passo

print("blob del simulatore PRIMA della correzione: %s"
      % hashlib.sha1(io.open("soliton_simulator.py", "rb").read()).hexdigest()[:8])
with contextlib.redirect_stdout(io.StringIO()):
    _S0, argv = _cli_flag.argv_del_driver(
        extra=["--seme=11"], dest="csv/_seal_fork/_sig_tipo_buco/_scarto")
    S, a = _cli_flag.carica_dal_cli(list(argv), nome="sim_buco")
    S._NMASSE_VIDEO["n"] = 2; S._NMASSE_VIDEO["sep"] = 3.0; S._NMASSE_VIDEO["size"] = None
    S.avvia_test("MASSE-COERENTI")()
    net = S.net
    for _ in range(10):
        _passo.passo_pieno(S, net)
print("10 passi sani: OK, controlli %d" % net._g_registro_controlli)
print("")
print("IL BUCO: `suo is not None` e' una SECONDA ESENZIONE IMPLICITA, e il registro ne dichiara UNA.")
print("Una grandezza TIPATA che diventa una LISTA non ha `dtype`, quindi il controllo del tipo")
print("la SALTA. Ecco che cosa succede OGGI, con la forma giusta:")
print("")
esiti = {}
for nome in ("psi", "phi0", "perc_chi", "pos", "_psi_spinor", "eta"):
    C = copy.deepcopy(net)
    S.net = C
    v = getattr(C, nome)
    setattr(C, nome, list(v))
    esito = None
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            _passo.passo_pieno(S, C)
        esito = "*** SALTATO IN SILENZIO ***"
    except (S.TipoSbagliato, S.FormaSbagliata, S.CacheCorta, S.CacheLunga) as e:
        esito = "PROTETTO da %s" % type(e).__name__
    except Exception as e:
        esito = "ROTTO RUMOROSO: %s -- %s" % (type(e).__name__,
                                              str(e).split(chr(10))[0][:52])
    print("  %-13s -> list  %s" % (nome, esito))
    esiti[nome] = esito
    S.net = net
print("")
# ### LA CONCLUSIONE SI DERIVA DAI RISULTATI, non si asserisce: la prima stesura stampava una
#   lettura FISSA (<<il tipo non viene guardato>>) che dopo la cura sarebbe stata FALSA.
silenziosi = sorted(k for k, v in esiti.items() if "SILENZIO" in v)
rumorosi = sorted(k for k, v in esiti.items() if "RUMOROSO" in v)
protetti = sorted(k for k, v in esiti.items() if "PROTETTO" in v)
print("IL CONTO, derivato: SALTATI IN SILENZIO %d %s | ROTTI RUMOROSI %d %s | PROTETTI %d %s"
      % (len(silenziosi), silenziosi, len(rumorosi), rumorosi, len(protetti), protetti))
print("")
print("LA LETTURA: una lista PERDE IL SECONDO ASSE, quindi le grandezze a DUE assi sono prese da")
print("`FormaSbagliata` in ogni caso. Per quelle a UN SOLO asse la forma resta GIUSTA, quindi")
print("tutto dipende dal controllo del TIPO: e' li' che viveva il buco, e `psi` e' fra loro.")
