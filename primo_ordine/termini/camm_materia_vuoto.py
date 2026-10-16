# -*- coding: utf-8 -*-
"""GENERATO da `primo_ordine/leggi/leggi.yaml` - NON si modifica a mano.

### **CAMM-MATERIA-VUOTO** -- `flusso`

L'accoppiamento fra la MATERIA e il VUOTO: `N_k = rho_k ln(rho_k / (rho_k + Lambda_k))`, con `rho_k = somma_h |psi_h|^2` e `Lambda_k = somma_h |phi_h|^2` (punto `F5`). ### DECISIONE DI LUCA del 2026-10-15 (23:30 e 23:38): SOSTITUISCE `CAMM-SATURAZIONE`. ### IL CONTO GIUSTO (errore n.1 del guardiano, corretto il 2026-10-16): LE LEGGI CHE GIRANO ERANO 6 E RESTANO 6 -- nell'ordine entra questa ed esce la saturazione, che RESTA in tabella come scheda SUPERATA. Le righe non di prova sono 8, e non c'e' niente da decidere. ### LE DUE DERIVATE, che sono il flusso: `alpha = dN/drho = ln(rho/(rho+Lambda)) + Lambda/(rho+Lambda)` su `psi`, e `beta = dN/dLambda = -rho/(rho+Lambda) = -x/(1+x)` su `phi`, con `x = rho/Lambda`. ### SENZA NESSUNA COSTANTE: `parametri: {}`, e la scala e' IL VUOTO LOCALE -- `x` e' un rapporto, cioe' RELAZIONALE e non tarato. ### ⭐ `esatto: true` SI DIMOSTRA, e non e' una promessa: `N` dipende SOLO da `rho` e `Lambda`, il flusso mette UNA FASE su `psi` e UNA FASE su `phi`, e una fase NON CAMBIA ne' `rho` ne' `Lambda`. ### Quindi `alpha` e `beta` sono COSTANTI durante il pezzo, e `exp(-i a dtau/2)` due volte fa `exp(-i a dtau)` IN ARITMETICA ESATTA. ### Cioe' IL FLUSSO CONSERVA LE PROPRIE SORGENTI, e percio' conserva `N_k` stesso -- e un collaudo ne misura GLI ULP. ### ⛔ `rho_k = 0`: `alpha` NON E' DEFINITA (`ln 0`), ma la' `psi = 0` e LA FASE DI UN VETTORE NULLO NON VUOL DIRE NIENTE -- `exp(-i a dtau) * 0 = 0` per qualunque `a`. ### Quindi la' `alpha = 0`, ed e' UNA SINGOLARITA' ELIMINABILE, non un pavimento: e' il valore che l'espressione PRENDE dove e' definita. ### E NESSUN PAVIMENTO SU `rho > 0`: dove `rho` e' piccolo ma non nullo, `alpha` e' grande e SI USA COM'E'. ### I CINQUE MOTIVI DELLA FORMA, tutti MISURATI: (a) LINEARE per poca materia (pendenza statica `1.11`), che e' il regime della materia reale se il vuoto e' planckiano; (b) SATURA per molta materia (`beta -> -1`); (c) rispetta il CONO nel senso del cambio di stato (`0.80` del passo libero, mentre `S2` lo VIOLA con `1.89`); (d) il VERSO statico e' quello deciso -- la materia CONSUMA il vuoto, `24` casi su `24`, da `85` a `1560` barre; (e) la SOVRAPPOSIZIONE vale fuori dalla saturazione (scarto `~2%` a `x = 0.01`). ### ⚠ E LA FORMA E' UNA SCELTA DI LUCA FRA QUATTRO CANDIDATE MISURATE, non una derivazione da un principio: il posto dove si derivera' e' il nodo `DEC-D6F-FORME-VUOTO` dell'albero, che NON e' ancora `presa`. ### ⚠ E IL VERSO E' BIDIREZIONALE NELLA LEGGE, al contrario della misura che l'ha scelta: `beta` da' al vuoto una fase che dipende dalla materia, e `alpha` da' alla materia una fase che dipende dal vuoto -- e quella fase CONTA, perche' il Grover e lo spostamento che seguono INTERFERISCONO.

### ⛔ **QUESTO MODULO E- UN LEGAME, non uno stub:** `applica()` chiede
l-operatore ### **al motore**, e se il motore non ce l-ha ### **ALZA** -- non
torna un risultato finto.
"""

IMPRONTA = '4d6c0486f4731348'
LEGGE = 'CAMM-MATERIA-VUOTO'
TIPO = 'flusso'
AMBITO = ('psi_h', 'phi_h', 'Lambda', 'rho')
PARAMETRI = {}
POSTO = None
VOCE_DECISIONE = None

GENERATORE = 'rho*log(rho/(rho + Lambda))'
ESATTO = True


def applica(st, motore, frazione):
    """### Applica questo pezzo allo stato, ### **tramite il MOTORE.**

    ### ⛔ **NON fa la fisica qui dentro:** la fisica e- ### **un
    operatore del motore**, e questo modulo e- ### **il legame fra la tabella
    e lui.**
    """
    quale = LEGGE
    fai = getattr(motore, 'operatori', {}).get(quale)
    if fai is None:
        raise NotImplementedError(
            'il motore non ha l-operatore ' + repr(quale)
            + ': questo modulo e- un LEGAME, e un legame senza il suo'
            + ' operatore ALZA invece di tornare un risultato finto')
    return fai(st, PARAMETRI, frazione)

