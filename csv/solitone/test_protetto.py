# -*- coding: utf-8 -*-
r"""**I TEST DEL SOLITONE PROTETTO** *(il task history `2026-11-01_cassetta_solitone`, `P1`-`P3`)*: ### **le partenze gia' committate, AL BIT.**"""
import json
import os

from . import RADICE
from . import protetto as P


def primo(percorso):
    with open(percorso, encoding="utf-8") as f:
        return json.loads(f.readline())


def gira(esito):
    import _consolida_B as CO
    import _coppia_di_B as CB
    import _deriva_congelato as DC
    import _livelli_piatti as LP
    import _salti_nel_cuore as SN
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _stato_fermo as SFM
    import _triangoli_bassa_energia as BE
    import _vuoto_vivo_B as V
    import materia_vuoto as MV
    print("### IL SOLITONE PROTETTO (csv/solitone/protetto.py)")
    S, FORMA, N, L, EPS = LP.S, LP.FORMA, CB.N, CB.L, CB.EPS_LUNGA
    esito("DEVE PASSARE: GRIGLIA e' il griglia.json di _coppia_di_B", os.path.samefile(P.GRIGLIA, os.path.join(CB.DIR_JSON, "griglia.json")), "")
    # ### P1: A a K, la partenza della corsa di a8e0e43b
    ref = primo(os.path.join(CB.DIR_JSON, "lunga_AK_00000.jsonl"))
    with P.scena_riferimento(N, L, EPS, S, FORMA) as (_rec, z, phi0, pK):
        p = P.stato_AK(pK)
        mu, _r = P.mu_rayleigh(z, phi0, p, S, FORMA)
    esito("DEVE PASSARE: P1 A a K (N %.0e, L %d, eps %g): lo sha e mu = lunga_AK_00000.jsonl (a8e0e43b) AL BIT" % (N, L, EPS), SFM.sha(p) == ref["sha_partenza"] and mu == ref["mu"], "mu %+.12f" % mu)
    # ### P2: B a Gamma dall'inviluppo; la scelta sulla scena di riferimento (come _consolida_B.q_migliore), l'inviluppo a N 3e5
    th, fi = P.griglia(CO.NOME_EPS)
    with P.scena_riferimento(N, L, EPS, S, FORMA) as (_rec, z, phi0, _p):
        q1, q2, _E0, _G = P.coppia(z, phi0, S)
    q, qp = P.scelta(q1, q2, th, fi)
    ref = primo(os.path.join(CO.DIR_JSON, "robusta_N3e5_000000.jsonl"))
    N_ = CO.ROBUSTE["N3e5"][0]
    assert ref["info"]["L"] == L
    with P.scena_riferimento(N_, L, EPS, S, FORMA) as (_rec, z, phi0, pK):
        p = P.inviluppo(z, pK, q, N_)
        z["st"]["psi_h"][...] = p          # ### come _massimo_di_B.misure, PRIMA della coppia
        _a, _b, E0, G = P.coppia(z, phi0, S)
        b = P.bloch(G, q, E0, S)
        mu, r = P.mu_rayleigh(z, phi0, p, S, FORMA)
        p_sb = P.inviluppo(z, pK, qp, N_)
    inf = ref["info"]
    esito("DEVE PASSARE: P2 B a Gamma, l'inviluppo a N 3e5: lo sha, E0, bloch, mu, il residuo = robusta_N3e5_000000.jsonl AL BIT",
          SFM.sha(p) == ref["sha_partenza"] and E0 == inf["E0"] and b == inf["bloch"] and mu == inf["mu"] and r == inf["residuo"] and (th, fi) == (inf["theta"], inf["phi"]),
          "E0 %+.9f mu %+.9f residuo %.6e" % (E0, mu, r))
    esito("DEVE FALLIRE: P2 col partner della scelta al posto della scelta: lo sha = robusta_N3e5_000000.jsonl", SFM.sha(p_sb) != ref["sha_partenza"], "")
    # ### P3: B a Gamma con s come argomento: la partenza di BG-F-0.15 (_vuoto_vivo_B, la scena col vuoto del fondo)
    sol, vuoto, s = V.CORSE["BG-F-0.15"]
    ref = primo(os.path.join(V.DIR_JSON, "BG-F-0.15_000000.jsonl"))
    with P.scena_vuoto(N, L, V.EPS, s, FORMA, vuoto) as (rec, z, phi0, pK):
        w0 = rec["larghezza"]
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            w_in = DC.forma(z, w0)[0]
        h = SN.lunghezza_arco(z)
        q1, q2, E0, G = P.coppia(z, phi0, s)
        q, _qp = P.scelta(q1, q2, th, fi)
        p = P.inviluppo(z, pK, q, N)
        mu, r = P.mu_rayleigh(z, phi0, p, s, FORMA)
        e_K = P.e_K(z)
        # ### il controllo positivo (Luca, l'unita' e_K): col legame ACCESO (S1 esplicita) e_K DEVE differire, o lo spegnimento non legge N
        with MV.forma_esplicita("S1"):
            e_K_acceso = V.e_K_di(z)
    inf = ref["info"]
    esito("DEVE PASSARE: P3 BG-F-0.15 (s %g, il vuoto %s): mu, il residuo, w_in, h, e_K (legame spento) = il primo pezzo di _vuoto_vivo_B AL BIT;"
          " e_K col legame acceso (S1) diverso" % (s, vuoto),
          mu == inf["mu"] and r == inf["residuo"] and w_in == ref["w_in"] and h == ref["h"] and e_K == ref["e_K"] and e_K_acceso != ref["e_K"],
          "mu %+.9f e_K %+.17g, acceso %+.17g" % (mu, e_K, e_K_acceso))
    print("    P3, E0: qui %+.17g (fase/s); _vuoto_vivo_B %+.17g (E0 * CB.S / s); la differenza %.1e (la conversione fatta una volta)" % (E0, inf["E0"], E0 - inf["E0"]))
    # ### D5: le decisioni di Luca (01:27) per le prove nuove (01:28, punto 6)
    print("### D5: LE DECISIONI PER LE PROVE NUOVE (eps dalla tabella, ridotto=True dichiarato; la forma S1; il costruttore su B a Gamma)")
    e, dich = P.eps_della_prova()
    e0, dich0 = P.eps_della_prova(ridotto=True)
    esito("DEVE PASSARE: D5 eps della prova = 0.5 della tabella (la decisione (7)); ridotto=True = 0, dichiarato", e == 0.5 and e0 == 0.0 and "CASO RIDOTTO" in dich0, "%s | %s" % (dich, dich0))
    esito("DEVE PASSARE: D5 la forma predefinita = S1 (la decisione (1), da _solitone_vuoto_congelato.FORMA)", P.forma_predefinita() == "S1" == FORMA, P.forma_predefinita())
    with P.scena_prova(N, L, s, vuoto=vuoto) as (_rec, z, phi0, pK, dich):
        ok_eps = z["par"]["eps"] == 0.5
        pd = P.partenza(z, phi0, pK, s, N)
        pa = P.partenza(z, phi0, pK, s, N, quale="AK")
    esito("DEVE PASSARE: D5 la scena della prova (BG-F-0.15) ha eps 0.5, e il costruttore predefinito = la partenza di P3 AL BIT (B a Gamma)", ok_eps and SFM.sha(pd) == SFM.sha(p), dich)
    esito("DEVE FALLIRE: D5 il costruttore predefinito = A a K", SFM.sha(pd) != SFM.sha(pa), "")
    return {"psi0_BG_F": p, "mu_BG_F": mu}
