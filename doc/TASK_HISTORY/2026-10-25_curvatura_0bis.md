# LA CURVATURA, PARTE 0-BIS: LE DUE MISURE CHE MANCANO PRIMA DI LEGGERE IL RAPPORTO DELLE DUE c (la strada A1, in memoria)

> **Il mandato:** di Luca, `2026-10-25` *(«facciamo le misure», `16:58`; [[PROGETTO-CURVATURA]], [[LORENTZ-MATERIA-INTERFERENZA]])*. ### **NESSUN file del nucleo; `B-4` e l'impronta `2e7f795d2a52fbe7` intatte.** ### **Lo script `csv/_curvatura_0bis.py`** *(importa `csv/_curvatura_prototipo.py`, `_u1_terzo`, `_u1_prototipo`)*, ### **il referto `doc/referti_l2/curvatura_0bis.{txt,jsonl}`.**
> ### ⚠ **L'ORDINE, riportato:** ### **il mandato chiede queste misure PRIMA della parte `1`, ma quando e' arrivato la parte `1` era gia' corsa e committata** *(`31ee70cc`, FERMO sulla chiave di `(c)`)*: ### **la parte `1` NON si tocca; questo mandato si esegue ORA, PRIMA del mandato «colmare le mancanze del censimento» arrivato prima di lui** *(perche' e' il completamento della parte `0`; l'ordine si registra: [[PRECEDENZA-IN-CODA]])*.
> ### **LA CORREZIONE CHIESTA:** ### **la frase «a `r 0.5` il rapporto e' `1.11`: oltre la luce» di `b0edae62` NON E' MISURATA** *(la luce in `A1` viene dalla carta; `v_b` non e' una velocita' che un pacchetto raggiunge)*: ### **si annota nel task history della curvatura e nella relazione.**

**LIVELLO:** misure in memoria.

## 0. LA STELLA POLARE

1. **`A14`:** ### **non si applica** *(nessuna legge cambia)*. 2. **Il gradino:** ### **`(c)` limiti noti:** ### **`c = 1` e `v_max/s = 0.598467` a `r = 1`.** 3. **Aggiunge un numero o una legge?** ### **No.** 4. **Tocca `rho`, `c_s` o il segno?** ### **Misura come `c_s` entra nelle velocita'.** 5. **Emergente o imposto?** ### **Non si applica.**

## 1. LE SCELTE DI METODO *(fissate qui, prima dei numeri)*

- ### **`M1`, LA LUCE IN `A1`:** ### **una regione a `cs` uniforme:** ### **`s = 0.05` per tick ovunque, `s_rif = s/r`** *(quindi `l = 1/r` per arco, `A_p = (sqrt3/4)/r^2`)*, ### **`CampoA1` col tempo del campo `F1` dalla `s_arco` VERA.** ### **ENTRAMBI i metodi:** ### **`(i)` la DISPERSIONE: i blocchi del tick del campo** *(`_u1_prototipo.blocchi_campo` con `CampoA1`)*, ### **`v_g` a `|k| = 1e-3` in `12` direzioni;** ### **`(ii)` un PACCHETTO** *(`_u1_prototipo.corsa_pacchetto`)* ### **contro la sua velocita' prevista dallo spettro.**
- ### **LE UNITA':** ### **«archi per tempo proprio»** *(la velocita' per tick divisa per `s`)* ### **e «lunghezza propria per tempo proprio»** *(per `l = 1/r`)*; ### **IL RAPPORTO con la materia si fa nella STESSA unita'** *(archi per tempo proprio per tutte e due: il fattore `l` si semplifica)*.
- ### **COURANT IN `A1`:** ### **`omega^2 = s^2 (l/l*)/A_p lambda ~ s^2 r^2 lambda`, quindi `s r sqrt24 <= 2`: `s <= 0.40825/r`;** ### **al `r` massimo `2`: `s <= 0.2041`;** ### **`s 0.05` vale a ogni `r`.** ### **E si MISURA:** ### **`max|lambda|` fuori dalla gauge sulla griglia `48 x 48` a ogni `r`.**
- ### **`M2`, LA VELOCITA' MASSIMA VERA DELLA MATERIA:** ### **il generatore `H_r`, la banda della coppia a `K` seguita per CONTINUITA' su tutta la zona** *(dal `K`, per sovrapposizione col vicino gia' assegnato: NON l'ordinamento)*; ### **`|grad mu|` da Hellmann-Feynman** *(`dH_r = r dH_gen`)*; ### **le griglie `48`, `96`, `192`** *(la convergenza, la regola della parte `B` del censimento)*. ### **E accanto il massimo su TUTTE le bande** *(il `v_max` di `_triangoli_forza`, la griglia `48`)*. ### **La conferma con gli spettri completi** *(`A1`, `s 0.01`, `r` `0.5`, `1`, `2`: `_triangoli_forza.v_max`, tutte le bande)*. ### **Il pacchetto in dinamica a `r 0.5`: NON si fa** *(dichiarato: costoso e opzionale)*.
- ### **`M3`, IL RAPPORTO:** ### **`v_max/c_luce` e `v_b/c_luce`** *(`v_b/s = pi sqrt(r)/4`, `b0edae62`)* ### **nella stessa unita'.**

## 2. I CRITERI *(del mandato, le previsioni del guardiano)*

| | il criterio | il tipo |
|---|---|---|
| `1` | a `r = 1`: `c_luce = 1` arco per tempo proprio entro `1e-3`; `v_max/s = 0.598467` entro `1e-4` *(la banda di `K` seguita, griglia `48`)*; `x(1) = 1/4` | DEVE |
| `2` | `c_luce(r) = r` archi per tempo proprio entro `1e-3` a ogni `r` | PUO' FALLIRE |
| `3` | `v_max/s` contro le stime del guardiano *(`0.3821`, `0.5298`, `0.6623`, `0.7642` a `r` `0.5`, `0.8`, `1.25`, `2`)* entro `3e-3` | PUO' FALLIRE |
| `4` | `v_max/c_luce < 1` a ogni `r` | PUO' FALLIRE |
| `5` | `v_max/c_luce` costante in `r` | ### **DEVE FALLIRE, per la chiave giusta:** ### **la variazione fra `r 0.5` e `r 2` `> 1.5` volte** |
| servizio | Courant a ogni `r`: stabile a `s 0.05` | servizio |

### **Mi FERMO se** ### **una DEVE fallisce.**

## 3. TODO

1. questo task history, da solo; 2. lo script, prima dei numeri; 3. la corsa; 4. il referto, la relazione, le annotazioni della frase «oltre la luce».
