# -*- coding: utf-8 -*-
r"""**I TEST DELLA PARTENZA E DELL'ARRESTO** *(`partenza.py`; Luca `2026-11-05` `14:14`; il task history `2026-11-05_TL120_densita_o_rientro`, 5)*: ### **le corse gia' scritte, rilette dai jsonl.**
### `PA0` *(Luca)* su `TF3 + TF3C` la partenza cade nel blocco `16000 .. 17000` *(il referto di `TF3`: `15000 .. 16000` `3.786`, `16000 .. 17000` `14.007`)*; `PA1` *(mio)* le velocita' per blocco del
modulo = quelle di `carta_deriva.finestre` su `carta_tf3_lunga.traiettoria`, AL BIT; `PA0-F` *(deve fallire, mio)* su `TB3` *(ferma: la velocita' massima `0.802`)* c'e' una partenza.
"""
from . import carta_deriva as CD
from . import carta_tf3_lunga as T3
from . import partenza as PA
from . import toro as TO

ATTESO = 16000.0               # ### il referto di TF3 (tb3_corsa.txt, tf3_lunga.txt): il primo blocco sopra 5 per 1000


def gira(esito):
    import _vuoto_vivo_B as V
    from . import corsa_accensione as CA
    print("### LA PARTENZA E L'ARRESTO (csv/solitone/partenza.py): SOGLIA %g PASSO %g DOPO %g; ATTESO %g" % (PA.SOGLIA, PA.PASSO, PA.DOPO, ATTESO))
    s = V.CORSE[CA.NOME][2]
    A1, A2 = TO.vettori()
    c3 = CA.serie("TF3")[1] + CA.serie("TF3C")[1]
    rb, cb, _d, _a = CA.serie("TB3")
    L = rb[0]["L"]
    st, ferma = PA.rileggi(c3, s, L, A1, A2, CD.pendenza)
    esito("DEVE PASSARE: PA0 su TF3 + TF3C (dai jsonl) la partenza cade nel blocco %g .. %g (il referto di TF3)" % (ATTESO, ATTESO + PA.PASSO), st["t_p"] == ATTESO,
          "la partenza %s; la corsa si sarebbe fermata a %s" % (st["t_p"], ferma))
    tq, X, ww, fl, _al = T3.traiettoria(c3, L, s)
    righe = CD.finestre("TF3", tq, X, ww, fl, 0.0, float(tq[-1]), PA.PASSO, False)
    tab = {r[0]: r[2] for r in righe}
    mod = {b[0]: b[2] for b in st["blocchi"]}
    comuni = sorted(set(tab) & set(mod))
    esito("DEVE PASSARE: PA1 le velocita' per blocco del modulo = quelle di carta_deriva.finestre, AL BIT", len(comuni) >= len(tab) - 1 and all(tab[a] == mod[a] for a in comuni),
          "%d blocchi in comune (la tabella %d, il modulo %d); diversi: %d" % (len(comuni), len(tab), len(mod), sum(1 for a in comuni if tab[a] != mod[a])))
    st3, _f3 = PA.rileggi(cb, s, L, A1, A2, CD.pendenza)
    vmax = max(b[2] for b in st3["blocchi"])
    esito("DEVE FALLIRE: PA0-F su TB3 (ferma) c'e' una partenza", st3["t_p"] is None, "la velocita' massima per blocco %.3f" % vmax)
