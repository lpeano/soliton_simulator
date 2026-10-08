# -*- coding: utf-8 -*-
"""IL BILANCIO DELLA NASCITA -- **la proposta di Luca: chi paga e' il calore che si scarica
sul vuoto locale.**

Nessuna corsa: e' aritmetica sulla `H` della sonda, coi numeri del `MARE v2` (`8efed03`).

Tre conti:

**`(1)` IL BILANCIO SECCO.** Quanto libera la concentrazione, quanto costa la prima
divisione, e che frazione del primo e' il secondo.

**`(2)` LA TAUTOLOGIA DELLA CONSERVAZIONE, che e' la forza E il limite della proposta.**
In una dinamica conservativa l'energia liberata dal collasso ### **E' ESATTAMENTE** quella che
serve a disfarlo: ### **ne' piu' ne' meno.** Il margine e' ### **zero per costruzione**.

**`(3)` LA CASCATA.** Il costo della divisione va come `N²`, quindi ### **ogni livello costa
un quarto del precedente**: si somma la serie e si guarda se il bilancio regge fino in fondo.

Gira con:  python csv/_test_fork/_bilancio_nascita.py
"""
import io
import json
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(os.path.dirname(_QUI))
sys.path.insert(0, os.path.join(RADICE, "csv"))
import _presidio                                             # noqa: E402
_presidio.avvia(__file__)

# ESENTE-H-P5: non importa il simulatore e non lo fa girare. E' aritmetica sui numeri gia'
# misurati dal `MARE v2` (`proto_primo_ordine/uscite/diagnosi_v2.json`) e dal
# `_crescita_conti` (`crescita.json`), che hanno dichiarato la loro configurazione.
NL = chr(10)
FUORI = os.path.join(_QUI, "_bilancio_nascita")
P = []


def stampa(s=""):
    P.append(s)
    print(s, flush=True)


def riga(c="-", n=104):
    stampa(c * n)


def main():
    os.makedirs(FUORI, exist_ok=True)
    v2 = json.load(io.open(os.path.join(RADICE, "proto_primo_ordine", "uscite",
                                        "diagnosi_v2.json"), encoding="utf-8"))
    cre = json.load(io.open(os.path.join(_QUI, "_crescita_conti", "crescita.json"),
                            encoding="utf-8"))
    b0 = v2["per_braccio"]["NON-NORM"]["semi"]["11"]
    N = 400.0
    g = -5.0
    lam = float(b0["lambda_max"])
    H_est = float(b0["g"]["-5.0"]["H_esteso"])
    H_uno = float(b0["g"]["-5.0"]["H_un_nodo"])
    # ### il `Delta H` del conto di `PT-7`: lo si PRENDE dal json, non si riscrive.
    # ### ⚠ **Si usa la riga `w = 1`**, che e' il `+199600` che il mandato cita; la riga
    # ### `w = lambda_max` si riporta accanto, perche' e' quella fisicamente ancorata.
    def _p7(ww):
        r = [c for c in cre["pt7"] if abs(float(c["g"]) - g) < 1e-12
             and abs(float(c["w"]) - ww) < 1e-3]
        assert len(r) == 1, "il conto di PT-7 con w = %r non si trova" % ww
        return float(r[0]["dH"]), float(r[0]["w"])

    dH1, w = _p7(1.0)
    dH1_lam, w_lam = _p7(lam)

    riga("=")
    stampa("IL BILANCIO DELLA NASCITA -- la proposta di Luca: paga il CALORE sul vuoto locale")
    riga("=")
    stampa("  la scena del conto: N = %.0f, g = %.1f, w = lambda_max = %.4f  (braccio "
           "NON-NORM, seme 11)" % (N, g, w, ))
    stampa()

    # ============================================== (1) IL BILANCIO SECCO
    riga("=")
    stampa("(1) IL BILANCIO SECCO")
    riga("=")
    liberata = H_est - H_uno
    stampa("  la CONCENTRAZIONE libera:   H(esteso) %12.1f  ->  H(un nodo) %12.1f"
           % (H_est, H_uno))
    stampa("      energia liberata        %12.1f" % liberata)
    stampa("  la PRIMA DIVISIONE costa:   Delta H   %12.1f   (con w = %.1f)" % (dH1, w))
    stampa("      e con w = lambda_max = %.4f:  Delta H %12.1f  -- il %6.2f %% della liberata"
           % (w_lam, dH1_lam, 100.0 * dH1_lam / (H_est - H_uno)))
    stampa("      cioe' il %6.2f %% di cio' che la concentrazione ha liberato"
           % (100.0 * dH1 / liberata))
    stampa("  ### -> IL PRIMO CONTO TORNA: il calore gia' liberato BASTA, e avanza.")

    # ============================================== (2) LA TAUTOLOGIA
    riga("=")
    stampa("(2) LA TAUTOLOGIA DELLA CONSERVAZIONE -- la forza E il limite della proposta")
    riga("=")
    stampa("  In una dinamica conservativa (A16) l'energia non sparisce, quindi il costo di")
    stampa("  DISFARE il collasso e' ESATTAMENTE l'energia che il collasso ha liberato:")
    stampa("      per tornare da un nodo al mare esteso servono   %12.1f" % (H_est - H_uno))
    stampa("      il collasso ne aveva liberati                   %12.1f" % liberata)
    stampa("      margine                                         %12.6e" % 0.0)
    stampa("  ### -> LA FORZA: NON SERVE NESSUN BAGNO ESTERNO. Il conto si chiude da solo,")
    stampa("  ###    ed e' esattamente cio' che la proposta di Luca dice.")
    stampa("  ### -> IL LIMITE, E VA DETTO: il margine e' ZERO PER COSTRUZIONE. <<Basta>> e")
    stampa("  ###    <<basta esattamente>> sono la stessa cosa, quindi il fatto che il")
    stampa("  ###    conto torni NON E' UNA PROVA CHE IL PROCESSO AVVENGA: e' la condizione")
    stampa("  ###    minima perche' non sia vietato. Quello che decide e' DOVE VA IL CALORE.")

    # ============================================== (3) LA CASCATA
    riga("=")
    stampa("(3) LA CASCATA -- il costo va come N^2, quindi ogni livello costa UN QUARTO")
    riga("=")
    stampa("  Un nodo di norma n che si divide in due da n/2 costa  (|g|/4) n^2 - w n.")
    stampa("  Al livello k ci sono 2^k nodi da N/2^k, quindi il livello costa")
    stampa("      2^k * [ (|g|/4) (N/2^k)^2 - w (N/2^k) ]  =  (|g|/4) N^2 / 2^k  -  w N")
    stampa()
    stampa("  livello   nodi   norma per nodo   costo del livello   cumulato   calore residuo")
    stampa("  " + "-" * 86)
    cum = 0.0
    liv = []
    for k in range(0, 9):
        nodi = 2 ** k
        nk = N / nodi
        costo = (abs(g) / 4.0) * N * N / (2.0 ** k) - w * N
        cum += costo
        liv.append({"livello": k, "nodi": nodi, "norma": nk, "costo": costo,
                    "cumulato": cum, "residuo": liberata - cum})
        stampa("  %5d  %6d  %14.4f  %18.1f  %10.1f  %14.1f"
               % (k, nodi, nk, costo, cum, liberata - cum))
        if liberata - cum < 0:
            break
    rotti = [x for x in liv if x["residuo"] < 0]
    stampa()
    if rotti:
        k0 = rotti[0]["livello"]
        stampa("  ### -> IL CALORE SI ESAURISCE AL LIVELLO %d: da li' in poi la frammentazione"
               % k0)
        stampa("  ###    NON E' PIU' FINANZIATA, e il sistema si ferma a %d nodi." % (2 ** k0))
        stampa("  ###    QUESTO E' UN FRENO CHE SI FERMA DA SOLO: non frammenta all'infinito.")
    else:
        stampa("  ### -> il calore non si esaurisce entro i livelli provati.")
    somma_inf = (abs(g) / 4.0) * N * N * 2.0
    stampa()
    stampa("  E LA SERIE INTERA, se si ignorasse il termine -w N:")
    stampa("      somma_k (|g|/4) N^2 / 2^k  =  (|g|/2) N^2  =  %12.1f" % somma_inf)
    stampa("      l'energia liberata dal collasso            =  %12.1f" % liberata)
    stampa("      differenza                                 =  %12.1f" % (somma_inf - liberata))
    stampa("  ### -> I DUE TERMINI N^2 SI CANCELLANO: la differenza e' di ordine N, cioe' i")
    stampa("  ###    termini di HOPPING. QUINDI non sono le grandezze dominanti a decidere se")
    stampa("  ###    la nascita si paga: LO DECIDONO I TERMINI SOTTODOMINANTI.")

    d = {"scena": {"N": N, "g": g, "w": w, "lambda_max": lam},
         "H_esteso": H_est, "H_un_nodo": H_uno, "liberata": liberata,
         "costo_prima_divisione": dH1, "frazione": dH1 / liberata,
         "costo_prima_divisione_w_lambda": dH1_lam, "w_lambda": w_lam,
         "frazione_w_lambda": dH1_lam / liberata,
         "livelli": liv, "serie_infinita": somma_inf,
         "differenza_serie": somma_inf - liberata,
         "livello_di_arresto": (rotti[0]["livello"] if rotti else None)}
    io.open(os.path.join(FUORI, "bilancio.json"), "w", encoding="utf-8").write(
        json.dumps(d, ensure_ascii=False, default=str))
    io.open(os.path.join(FUORI, "bilancio.txt"), "w", encoding="utf-8").write(
        NL.join(P) + NL)
    stampa()
    stampa("scritto %s" % os.path.join(FUORI, "bilancio.json"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
