> ### ⛔ **GRIGLIA QUADRATA -- risultato da rifare sui triangoli (DECISIONE-SOLO-TRIANGOLI)**

# LA PROVA DEL PRINCIPIO DI EQUIVALENZA: L'UNIVERSALITA' DELLA MASSA AL VARIARE DI `cs`

> **Il mandato:** di Luca, dopo `51f45268`. ### **Una MISURA, non sceglie niente.** ### **`dtau`, `eps` e `cs` SOLO nella scena, in memoria**; `leggi.yaml`, l'impronta
> `2e7f795d2a52fbe7` e il nucleo intatti; ### **`soliton_simulator.py` al blob `b8c21049`** *(verificato: e' lo sha1-BYTE dei byte grezzi; il blob di git e' `e96ca41a`;
> il file e' pulito)*. ### **`matrice()` e `rami_seguiti()` di `csv/_massa_vicino_al_cono.py` IMPORTATI, non copiati.**

**LIVELLO:** `L2`, una misura.

## 0. LA STELLA POLARE *(e' una misura: lo dichiaro, e rispondo lo stesso)*

1. **`A14`:** ### **non si applica** *(nessuna legge cambia)*.
2. **Il gradino:** `(a)` ### **il positivo** *(la stessa specie contro se stessa, `R = 1` al bit)* ### **e il caso che deve fallire** *(sintetico)*; `(b)` ### **`eps = 0`, il solo
   generatore**, come riferimento; `(c)` ### **il principio di equivalenza** *(una sola massa per tutte le specie)*.
3. **Aggiunge un numero o una legge?** ### **No.** La soglia di lettura `1e-3` e' ### **una soglia di LETTURA**, non di fisica.
4. **Tocca `rho`, `c_s` o il segno?** ### **`cs` SI'** *(uniforme a mano, come la misura `2` di `51f45268`)*: ### **e' la variabile della prova.**
5. **Emergente o imposto?** ### **E' la domanda:** ### **le masse scalano insieme con `s`** *(un osservatore locale non vede `cs`)*, ### **o no** *(il principio di
   equivalenza e' violato fra specie)*.

## 1. IL CENSIMENTO, FATTO PRIMA *(lato `32`, in memoria, nessun file scritto)*

### **Un ramo e' MASSIVO** se e' dispersivo *(`|v_g|` per tempo proprio `> 0.1`, la definizione di `51f45268`)*, ### **il fit converge** *(scarto `<= 5%`)*, ### **il salto
per tick `Dt` e' `> 0` e `<= pi` *(IL TETTO)***; ### **due rami sono la stessa specie se i loro `Dt` coincidono entro `1e-6` relativo** *(le coppie degeneri)*. ### **Il numero
di rami massivi DISTINTI** *(e i loro `Dt`)*:

| `eps` | `s 0.5` | `0.6` | `0.7` | `0.8` | `0.9` | `0.95` | `0.99` | `1` |
|---|---|---|---|---|---|---|---|---|
| `0` | `1` | `1` | `1` | `1` | `1` | `1` | `1` | `0` *(il gap e' nullo)* |
| `0.25` | `1` | `1` | `1` | `1` | `2` | `2` | `2` | `2` |
| `0.5` | `1` | `1` | `1` | `1` | `1` | `3` | `3` | `3` |
| `0.75` | `1` | `1` | `2` | `2` | `2` | `2` | `3` | `3` |
| `1.0` | `1` | `1` | `2` | `2` | `2` | `2` | `2` | `2` |

- ### ⭐ **IL NUMERO CAMBIA CON `s`:** ### **vicino al cono nascono rami massivi nuovi** *(a `eps 0.75` un ramo leggero, `Dt` `0.027`, compare a `s 0.7`)*. ### **Quindi una specie
  NON si definisce per rango** *(il primo, il secondo)*: ### **il rango salterebbe.**
- ### **E IL «BUCO» DI `51f45268` NON E' UN BUCO DEI RAMI:** con il TETTO applicato ramo per ramo, ### **a `eps 0.5` e `s 0.5` il salto valido e' `0.670` per tick**; ### **i `131`
  radianti di `51f45268` venivano dalla MEDIANA presa anche sui rami NON validi.**

## 2. IL METODO

- ### **LE SPECIE:** ### **`(a)` i rami massivi distinti dello stesso spettro**, ### **seguiti in `s` come CATENE PER CONTINUITA'** *(a ogni `s` ogni catena prende il `Dt` piu'
  vicino in senso relativo fra quelli validi, entro un fattore `2`; un `Dt` non preso apre una catena nuova)*; ### **`(b)` le camminate con moneta diversa** *(`eps` `0.25`,
  `0.5`, `0.75`, `1.0`, e `eps 0` come riferimento del solo generatore)*: ### **le catene di `eps` diversi sono specie diverse.**
- ### **LA MISURA:** `s` in `(0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.99, 1.0)`, lati `32` e `64`, ### **`cs` uniforme a mano** *(`matrice(L, s, eps, cs=1.0)`: `s = dtau`; la misura `2`
  di `51f45268` ha gia' mostrato che conta solo `s`)*; ### **per ogni specie e ogni `s`: `Dt` e `Delta = Dt/dtau`.**
- ### **IL TETTO:** `Dt > pi` o il fit che non converge ### **-> INVALIDO, escluso, tenuto in tabella.**
- ### **I RAPPORTI:** ### **`R_ij(s) = Delta_i(s)/Delta_j(s)`** sugli `s` dove tutte e due sono valide; ### **`V_ij = (max - min)/media`** *(almeno `2` punti, altrimenti «non
  leggibile»)*. ### **I rapporti per tick e per tempo proprio sono gli stessi** *(lo stesso `s` al numeratore e al denominatore)*.
- ### **L'OROLOGIO LOCALE** *(punto `5`)*: ### **il ramo di LUCE** = il ramo del settore del VUOTO ### **con la variazione massima fra `k = 0` e `k = pi/4`**, seguito per continuita'
  ### **con `rami_seguiti()` stesso** *(il blocco del vuoto messo in un `8 x 8` diagonale a blocchi con l'identita': i rami dell'identita' sono piatti e non si scelgono)*; ### **la sua
  frequenza per tick `|phi(pi/4) - phi(0)|`.** ### **`Delta_i(s)` per tick diviso quella frequenza, e la sua `V`.**
- ### **LE TAGLIE:** ### **le catene di lato `64` accoppiate a quelle di lato `32` per `Dt` piu' vicino al primo `s` comune**; ### **`|Delta(32) - Delta(64)|/Delta < 0.01` per ogni valore
  valido** *(`TOLL_TAGLIE`)*.

## 3. I CRITERI, FISSATI ORA *(copiati dal mandato)*

- ### **POSITIVO, DEVE PASSARE:** ### **ogni specie contro se stessa: `R = 1` AL BIT, a ogni `s`.**
- ### **DEVE FALLIRE:** ### **i dati sintetici `Delta_1 = (1 - s)`, `Delta_2 = 0.339`**, ### **lo STESSO stimatore di `V`**: ### **`V` oltre la soglia `1e-3`**, ### **e per `V`, non per
  altro** *(nessun `NaN`, nessuna eccezione: il valore di `V` stampato)*.
- ### **PUO' FALLIRE:** ### **`Delta_1 = 2 (1 - s)`, `Delta_2 = 3 (1 - s)`: `V < 1e-12`.**
- ### **LE TAGLIE:** `< 0.01` per ogni valore valido.
- ### **IL VERDETTO DI FISICA NON E' UN PASSA/FALLISCE: e' la TABELLA dei `V_ij`**, ### **con la soglia di lettura `1e-3`** *(sotto: universale entro la misura; sopra: dipendente
  dalla specie)*, ### **senza conclusioni oltre la tabella.**

## 4. IL PROSSIMO PASSO, NON IN QUESTO MANDATO

### **L'accoppiamento al GRADIENTE di `cs`** *(la marea)*: ### **resta una voce aperta.**

## 5. I RISULTATI *(scritti dopo la corsa, sotto)*

### **LA CORSA:** `csv/_universalita_massa.py`, blob sha1-BYTE `94ebb415` *(git `c26bff01`)*, committato e pulito; ### **`4` controlli su `5`.** ### **Positivo: PASSA**
*(`R = 1` al bit)*; ### **deve fallire: FALLISCE per `V`** *(`V = 2.564`)*; ### **puo' fallire: `V = 0.0`**; ### ⚠ **LE TAGLIE: FALLISCONO** *(il peggiore `0.377` su `65`
valori)*. ### **Il criterio NON si cambia.** ### **La diagnosi** *(dal confronto catena per catena, lato `32` contro `64`)*: ### **le catene principali** *(`catena 0`)*
### **concordano entro lo `0.1`-`0.5%`**; ### **il peggiore viene dai gap quasi nulli a `s = 1`, `eps 0`** *(`Delta ~ 0` su tutti e due: la differenza relativa non ha
senso)*; ### **e dalle catene SECONDARIE leggere** *(`eps 0.5 catena 1` al `7`-`8%`, `eps 0.75 catena 1` al `2.6`-`5.9%`)* ### **e da catene NON accoppiate** *(il lato `64` ha
piu' catene del `32`)*. ### **Le secondarie si leggono con la loro taglia come incertezza.**

### 5.1 `Delta_i(s)` per tempo proprio, lato `32` *(lato `64` nel `jsonl`)*

| specie | `s 0.5` | `s 0.6` | `s 0.7` | `s 0.8` | `s 0.9` | `s 0.95` | `s 0.99` | `s 1.0` |
|---|---|---|---|---|---|---|---|---|
| `eps 0 catena 0` | `1.36804` | `1.17996` | `0.93497` | `0.63866` | `0.31387` | `0.15237` | -- | -- |
| `eps 0 catena 1` | -- | -- | -- | -- | -- | -- | `0.02757` | -- |
| `eps 0 catena 2` | -- | -- | -- | -- | -- | -- | -- | `0.00000` |
| `eps 0 catena 3` | -- | -- | -- | -- | -- | -- | -- | `0.00000` |
| `eps 0.25 catena 0` | `1.36106` | `1.17632` | `0.93743` | `0.65467` | `0.64588` | -- | -- | -- |
| `eps 0.25 catena 1` | -- | -- | -- | -- | `0.36837` | `0.35964` | `0.20657` | `0.20116` |
| `eps 0.25 catena 2` | -- | -- | -- | -- | -- | `0.25629` | `0.27225` | `0.26455` |
| `eps 0.5 catena 0` | `1.34022` | `1.16511` | `0.94341` | `0.69452` | `0.47121` | `0.39207` | `0.34761` | `0.33864` |
| `eps 0.5 catena 1` | -- | -- | -- | -- | -- | `0.01588` | `0.01782` | `0.01829` |
| `eps 0.5 catena 2` | -- | -- | -- | -- | -- | `1.06075` | `0.71524` | `0.67324` |
| `eps 0.75 catena 0` | `1.30586` | `1.14553` | `0.94923` | `0.74188` | `0.56624` | `0.49949` | `0.45542` | `0.44549` |
| `eps 0.75 catena 1` | -- | -- | `0.03888` | `0.05819` | `0.07416` | `0.07990` | `0.08346` | `0.08422` |
| `eps 0.75 catena 2` | -- | -- | -- | -- | -- | -- | `1.54740` | `1.32983` |
| `eps 1 catena 0` | `1.25852` | `1.11635` | `0.95020` | `0.78416` | `0.64525` | `0.58952` | `0.55115` | `0.54235` |
| `eps 1 catena 1` | -- | -- | `0.11097` | `0.15763` | `0.18924` | `0.19830` | `0.20298` | `0.20386` |

### 5.2 I `V_ij` LEGGIBILI *(almeno `2` `s` comuni)*: **125** su 258 coppie; **sotto `1e-3`: 1**

| lato | `i` | `j` | `s` comuni | `V_ij` |
|---|---|---|---|---|
| `32` | `eps 0 catena 0` | `eps 0.25 catena 0` | `5` | `5.8112e-01` |
| `32` | `eps 0 catena 0` | `eps 0.25 catena 1` | `2` | `6.7158e-01` |
| `32` | `eps 0 catena 0` | `eps 0.5 catena 0` | `6` | `7.5872e-01` |
| `32` | `eps 0 catena 0` | `eps 0.75 catena 0` | `6` | `9.3152e-01` |
| `32` | `eps 0 catena 0` | `eps 0.75 catena 1` | `4` | `2.1516e+00` |
| `32` | `eps 0 catena 0` | `eps 1 catena 0` | `6` | `1.0606e+00` |
| `32` | `eps 0 catena 0` | `eps 1 catena 1` | `4` | `2.0550e+00` |
| `32` | `eps 0.25 catena 0` | `eps 0.5 catena 0` | `5` | `4.0140e-01` |
| `32` | `eps 0.25 catena 0` | `eps 0.75 catena 0` | `5` | `2.5414e-01` |
| `32` | `eps 0.25 catena 0` | `eps 0.75 catena 1` | `3` | `1.0485e+00` |
| `32` | `eps 0.25 catena 0` | `eps 1 catena 0` | `5` | `2.4872e-01` |
| `32` | `eps 0.25 catena 0` | `eps 1 catena 1` | `3` | `9.4312e-01` |
| `32` | `eps 0.25 catena 1` | `eps 0.25 catena 2` | `3` | `6.6165e-01` |
| `32` | `eps 0.25 catena 1` | `eps 0.5 catena 0` | `4` | `4.4787e-01` |
| `32` | `eps 0.25 catena 1` | `eps 0.5 catena 1` | `3` | `7.7220e-01` |
| `32` | `eps 0.25 catena 1` | `eps 0.5 catena 2` | `3` | `1.6264e-01` |
| `32` | `eps 0.25 catena 1` | `eps 0.75 catena 0` | `4` | `4.7191e-01` |
| `32` | `eps 0.25 catena 1` | `eps 0.75 catena 1` | `4` | `7.1965e-01` |
| `32` | `eps 0.25 catena 1` | `eps 0.75 catena 2` | `2` | `1.2483e-01` |
| `32` | `eps 0.25 catena 1` | `eps 1 catena 0` | `4` | `4.9654e-01` |
| `32` | `eps 0.25 catena 1` | `eps 1 catena 1` | `4` | `6.6601e-01` |
| `32` | `eps 0.25 catena 2` | `eps 0.5 catena 0` | `3` | `1.7516e-01` |
| `32` | `eps 0.25 catena 2` | `eps 0.5 catena 1` | `3` | `1.0921e-01` |
| `32` | `eps 0.25 catena 2` | `eps 0.5 catena 2` | `3` | `4.4725e-01` |
| `32` | `eps 0.25 catena 2` | `eps 0.75 catena 0` | `3` | `1.4904e-01` |
| `32` | `eps 0.25 catena 2` | `eps 0.75 catena 1` | `3` | `3.7737e-02` |
| `32` | `eps 0.25 catena 2` | `eps 0.75 catena 2` | `2` | `1.2272e-01` |
| `32` | `eps 0.25 catena 2` | `eps 1 catena 0` | `3` | `1.2542e-01` |
| `32` | `eps 0.25 catena 2` | `eps 1 catena 1` | `3` | `3.7257e-02` |
| `32` | `eps 0.5 catena 0` | `eps 0.5 catena 1` | `3` | `2.9507e-01` |
| `32` | `eps 0.5 catena 0` | `eps 0.5 catena 2` | `3` | `2.9454e-01` |
| `32` | `eps 0.5 catena 0` | `eps 0.75 catena 0` | `8` | `2.9930e-01` |
| `32` | `eps 0.5 catena 0` | `eps 0.75 catena 1` | `6` | `2.1828e+00` |
| `32` | `eps 0.5 catena 0` | `eps 0.75 catena 2` | `2` | `1.2521e-01` |
| `32` | `eps 0.5 catena 0` | `eps 1 catena 0` | `8` | `5.3095e-01` |
| `32` | `eps 0.5 catena 0` | `eps 1 catena 1` | `6` | `1.9780e+00` |
| `32` | `eps 0.5 catena 1` | `eps 0.5 catena 2` | `3` | `5.4553e-01` |
| `32` | `eps 0.5 catena 1` | `eps 0.75 catena 0` | `3` | `2.4795e-01` |
| `32` | `eps 0.5 catena 1` | `eps 0.75 catena 1` | `3` | `8.7501e-02` |
| `32` | `eps 0.5 catena 1` | `eps 0.75 catena 2` | `2` | `1.7731e-01` |
| `32` | `eps 0.5 catena 1` | `eps 1 catena 0` | `3` | `2.1869e-01` |
| `32` | `eps 0.5 catena 1` | `eps 1 catena 1` | `3` | `1.1201e-01` |
| `32` | `eps 0.5 catena 2` | `eps 0.75 catena 0` | `3` | `3.5297e-01` |
| `32` | `eps 0.5 catena 2` | `eps 0.75 catena 1` | `3` | `5.3110e-01` |
| `32` | `eps 0.5 catena 2` | `eps 0.75 catena 2` | `2` | `9.0951e-02` |
| `32` | `eps 0.5 catena 2` | `eps 1 catena 0` | `3` | `3.8588e-01` |
| `32` | `eps 0.5 catena 2` | `eps 1 catena 1` | `3` | `5.0431e-01` |
| `32` | `eps 0.75 catena 0` | `eps 0.75 catena 1` | `6` | `1.8570e+00` |
| `32` | `eps 0.75 catena 0` | `eps 0.75 catena 2` | `2` | `1.2930e-01` |
| `32` | `eps 0.75 catena 0` | `eps 1 catena 0` | `8` | `2.3435e-01` |
| `32` | `eps 0.75 catena 0` | `eps 1 catena 1` | `6` | `1.6470e+00` |
| `32` | `eps 0.75 catena 1` | `eps 0.75 catena 2` | `2` | `1.6029e-01` |
| `32` | `eps 0.75 catena 1` | `eps 1 catena 0` | `6` | `1.0207e+00` |
| `32` | `eps 0.75 catena 1` | `eps 1 catena 1` | `6` | `1.6114e-01` |
| `32` | `eps 0.75 catena 2` | `eps 1 catena 0` | `2` | `1.3523e-01` |
| `32` | `eps 0.75 catena 2` | `eps 1 catena 1` | `2` | `1.5553e-01` |
| `32` | `eps 1 catena 0` | `eps 1 catena 1` | `6` | `1.3999e+00` |
| `64` | `eps 0 catena 0` | `eps 0.25 catena 0` | `5` | `5.9979e-01` |
| `64` | `eps 0 catena 0` | `eps 0.25 catena 1` | `2` | `6.8063e-01` |
| `64` | `eps 0 catena 0` | `eps 0.5 catena 0` | `6` | `7.5751e-01` |
| `64` | `eps 0 catena 0` | `eps 0.5 catena 1` | `2` | `8.2686e-01` |
| `64` | `eps 0 catena 0` | `eps 0.75 catena 0` | `6` | `9.3003e-01` |
| `64` | `eps 0 catena 0` | `eps 0.75 catena 1` | `4` | `2.1299e+00` |
| `64` | `eps 0 catena 0` | `eps 1 catena 0` | `6` | `1.0589e+00` |
| `64` | `eps 0 catena 0` | `eps 1 catena 1` | `5` | `2.6059e+00` |
| `64` | `eps 0.25 catena 0` | `eps 0.5 catena 0` | `5` | `4.3962e-01` |
| `64` | `eps 0.25 catena 0` | `eps 0.75 catena 0` | `5` | `2.8903e-01` |
| `64` | `eps 0.25 catena 0` | `eps 0.75 catena 1` | `3` | `9.9951e-01` |
| `64` | `eps 0.25 catena 0` | `eps 1 catena 0` | `5` | `2.4636e-01` |
| `64` | `eps 0.25 catena 0` | `eps 1 catena 1` | `4` | `1.6790e+00` |
| `64` | `eps 0.25 catena 1` | `eps 0.25 catena 2` | `3` | `6.7865e-01` |
| `64` | `eps 0.25 catena 1` | `eps 0.5 catena 0` | `4` | `4.5996e-01` |
| `64` | `eps 0.25 catena 1` | `eps 0.5 catena 1` | `4` | `8.8171e-01` |
| `64` | `eps 0.25 catena 1` | `eps 0.5 catena 2` | `3` | `1.6086e-01` |
| `64` | `eps 0.25 catena 1` | `eps 0.75 catena 0` | `4` | `4.8426e-01` |
| `64` | `eps 0.25 catena 1` | `eps 0.75 catena 1` | `4` | `7.0927e-01` |
| `64` | `eps 0.25 catena 1` | `eps 0.75 catena 2` | `2` | `1.2716e-01` |
| `64` | `eps 0.25 catena 1` | `eps 0.75 catena 3` | `2` | `1.2716e-01` |
| `64` | `eps 0.25 catena 1` | `eps 1 catena 0` | `4` | `5.0895e-01` |
| `64` | `eps 0.25 catena 1` | `eps 1 catena 1` | `4` | `6.6091e-01` |
| `64` | `eps 0.25 catena 2` | `eps 0.5 catena 0` | `3` | `1.7958e-01` |
| `64` | `eps 0.25 catena 2` | `eps 0.5 catena 1` | `3` | `9.6324e-02` |
| `64` | `eps 0.25 catena 2` | `eps 0.5 catena 2` | `3` | `4.6170e-01` |
| `64` | `eps 0.25 catena 2` | `eps 0.75 catena 0` | `3` | `1.5327e-01` |
| `64` | `eps 0.25 catena 2` | `eps 0.75 catena 1` | `3` | `3.7980e-02` |
| `64` | `eps 0.25 catena 2` | `eps 0.75 catena 2` | `2` | `1.2455e-01` |
| `64` | `eps 0.25 catena 2` | `eps 0.75 catena 3` | `2` | `1.2455e-01` |
| `64` | `eps 0.25 catena 2` | `eps 1 catena 0` | `3` | `1.2960e-01` |
| `64` | `eps 0.25 catena 2` | `eps 1 catena 1` | `3` | `4.2508e-02` |
| `64` | `eps 0.5 catena 0` | `eps 0.5 catena 1` | `4` | `6.5715e-01` |
| `64` | `eps 0.5 catena 0` | `eps 0.5 catena 2` | `3` | `3.0673e-01` |
| `64` | `eps 0.5 catena 0` | `eps 0.75 catena 0` | `8` | `2.9899e-01` |
| `64` | `eps 0.5 catena 0` | `eps 0.75 catena 1` | `6` | `2.1419e+00` |
| `64` | `eps 0.5 catena 0` | `eps 0.75 catena 2` | `2` | `1.2766e-01` |
| `64` | `eps 0.5 catena 0` | `eps 0.75 catena 3` | `2` | `1.2767e-01` |
| `64` | `eps 0.5 catena 0` | `eps 1 catena 0` | `8` | `5.3026e-01` |
| `64` | `eps 0.5 catena 0` | `eps 1 catena 1` | `7` | `2.9050e+00` |
| `64` | `eps 0.5 catena 1` | `eps 0.5 catena 2` | `3` | `5.4928e-01` |
| `64` | `eps 0.5 catena 1` | `eps 0.75 catena 0` | `4` | `4.9465e-01` |
| `64` | `eps 0.5 catena 1` | `eps 0.75 catena 1` | `4` | `1.6694e-01` |
| `64` | `eps 0.5 catena 1` | `eps 0.75 catena 2` | `2` | `1.7820e-01` |
| `64` | `eps 0.5 catena 1` | `eps 0.75 catena 3` | `2` | `1.7820e-01` |
| `64` | `eps 0.5 catena 1` | `eps 1 catena 0` | `4` | `4.3680e-01` |
| `64` | `eps 0.5 catena 1` | `eps 1 catena 1` | `4` | `2.1255e-01` |
| `64` | `eps 0.5 catena 2` | `eps 0.75 catena 0` | `3` | `3.6781e-01` |
| `64` | `eps 0.5 catena 2` | `eps 0.75 catena 1` | `3` | `5.4257e-01` |
| `64` | `eps 0.5 catena 2` | `eps 0.75 catena 2` | `2` | `9.2110e-02` |
| `64` | `eps 0.5 catena 2` | `eps 0.75 catena 3` | `2` | `9.2112e-02` |
| `64` | `eps 0.5 catena 2` | `eps 1 catena 0` | `3` | `4.0092e-01` |
| `64` | `eps 0.5 catena 2` | `eps 1 catena 1` | `3` | `5.1827e-01` |
| `64` | `eps 0.75 catena 0` | `eps 0.75 catena 1` | `6` | `1.8157e+00` |
| `64` | `eps 0.75 catena 0` | `eps 0.75 catena 2` | `2` | `1.3188e-01` |
| `64` | `eps 0.75 catena 0` | `eps 0.75 catena 3` | `2` | `1.3188e-01` |
| `64` | `eps 0.75 catena 0` | `eps 1 catena 0` | `8` | `2.3400e-01` |
| `64` | `eps 0.75 catena 0` | `eps 1 catena 1` | `7` | `2.6074e+00` |
| `64` | `eps 0.75 catena 1` | `eps 0.75 catena 2` | `2` | `1.6227e-01` |
| `64` | `eps 0.75 catena 1` | `eps 0.75 catena 3` | `2` | `1.6227e-01` |
| `64` | `eps 0.75 catena 1` | `eps 1 catena 0` | `6` | `1.0032e+00` |
| `64` | `eps 0.75 catena 1` | `eps 1 catena 1` | `6` | `1.4507e-01` |
| `64` | `eps 0.75 catena 2` | `eps 0.75 catena 3` | `2` | `2.7572e-06` |
| `64` | `eps 0.75 catena 2` | `eps 1 catena 0` | `2` | `1.3785e-01` |
| `64` | `eps 0.75 catena 2` | `eps 1 catena 1` | `2` | `1.5795e-01` |
| `64` | `eps 0.75 catena 3` | `eps 1 catena 0` | `2` | `1.3786e-01` |
| `64` | `eps 0.75 catena 3` | `eps 1 catena 1` | `2` | `1.5795e-01` |
| `64` | `eps 1 catena 0` | `eps 1 catena 1` | `7` | `2.3523e+00` |

### 5.3 L'OROLOGIO LOCALE: `V` di `Delta_i / orologio di luce a k = pi/4`

| lato | specie | `V` |
|---|---|---|
| `32` | `eps 0 catena 0` | `2.1527e+00` |
| `32` | `eps 0 catena 1` | non leggibile |
| `32` | `eps 0 catena 2` | non leggibile |
| `32` | `eps 0 catena 3` | non leggibile |
| `32` | `eps 0.25 catena 0` | `1.4516e+00` |
| `32` | `eps 0.25 catena 1` | `1.0352e+00` |
| `32` | `eps 0.25 catena 2` | `2.0241e-01` |
| `32` | `eps 0.5 catena 0` | `2.4977e+00` |
| `32` | `eps 0.5 catena 1` | `9.2565e-02` |
| `32` | `eps 0.5 catena 2` | `7.2301e-01` |
| `32` | `eps 0.75 catena 0` | `2.3055e+00` |
| `32` | `eps 0.75 catena 1` | `4.1966e-01` |
| `32` | `eps 0.75 catena 2` | `1.9816e-01` |
| `32` | `eps 1 catena 0` | `2.1278e+00` |
| `32` | `eps 1 catena 1` | `5.2881e-01` |
| `64` | `eps 0 catena 0` | `2.1522e+00` |
| `64` | `eps 0 catena 1` | non leggibile |
| `64` | `eps 0 catena 2` | non leggibile |
| `64` | `eps 0 catena 3` | non leggibile |
| `64` | `eps 0.25 catena 0` | `1.4362e+00` |
| `64` | `eps 0.25 catena 1` | `1.0322e+00` |
| `64` | `eps 0.25 catena 2` | `1.9910e-01` |
| `64` | `eps 0.5 catena 0` | `2.4978e+00` |
| `64` | `eps 0.5 catena 1` | `1.5888e-01` |
| `64` | `eps 0.5 catena 2` | `7.3861e-01` |
| `64` | `eps 0.75 catena 0` | `2.3060e+00` |
| `64` | `eps 0.75 catena 1` | `4.3851e-01` |
| `64` | `eps 0.75 catena 2` | `2.0085e-01` |
| `64` | `eps 0.75 catena 3` | `2.0085e-01` |
| `64` | `eps 1 catena 0` | `2.1287e+00` |
| `64` | `eps 1 catena 1` | `5.5112e-01` |
| `64` | `eps 1 catena 2` | non leggibile |
| `64` | `eps 1 catena 3` | non leggibile |

### 5.4 GLI INVALIDI *(118 in tutto; esclusi, tenuti nel referto)*

| lato | `eps` | perche' | quanti | a quali `s` |
|---|---|---|---|---|
| `32` | `0.25` | Dt > pi | `8` | `0.5`, `0.6`, `0.7`, `0.8` |
| `32` | `0.5` | Dt > pi | `10` | `0.5`, `0.6`, `0.7`, `0.8`, `0.9` |
| `32` | `0.75` | Dt > pi | `18` | `0.5`, `0.6`, `0.7`, `0.8`, `0.9`, `0.95`, `0.99`, `1` |
| `32` | `1` | Dt > pi | `22` | `0.5`, `0.6`, `0.7`, `0.8`, `0.9`, `0.95`, `0.99`, `1` |
| `64` | `0.25` | Dt > pi | `8` | `0.5`, `0.6`, `0.7`, `0.8` |
| `64` | `0.5` | Dt > pi | `10` | `0.5`, `0.6`, `0.7`, `0.8`, `0.9` |
| `64` | `0.75` | Dt > pi | `20` | `0.5`, `0.6`, `0.7`, `0.8`, `0.9`, `0.95`, `0.99`, `1` |
| `64` | `1` | Dt > pi | `22` | `0.5`, `0.6`, `0.7`, `0.8`, `0.9`, `0.95`, `0.99`, `1` |

### 5.5 LA LETTURA, IN TRE RIGHE

1. ### **IL PRINCIPIO DI EQUIVALENZA, FRA SPECIE, NON TIENE nella camminata a `cs` uniforme:** ### **`124` dei `125` `V_ij` leggibili sono SOPRA `1e-3`** *(tipicamente
   `0.04`-`2.5`)*: ### **le masse delle specie NON scalano insieme con `s`** *(la principale di `eps 0` si spegne al cono, quella di `eps 0.5` resta `0.339`)*.
2. ### ⚠ **L'UNICO `V` sotto `1e-3`** *(`2.8e-6`, lato `64`, `eps 0.75 catena 2` contro `catena 3`)* ### **NON E' UNIVERSALITA': e' la STESSA specie contata due volte**
   *(gli stessi `Delta` `3.0056` e `2.4570`: una coppia degenere che la soglia `1e-6` ha separato)*.
3. ### **E l'orologio locale non salva:** ### **anche diviso la luce a `k = pi/4`, le principali hanno `V` `2.1`-`2.5`**: ### **un osservatore locale VEDE `cs`**
   *(attraverso `s`)*. ### **Nessuna conclusione oltre la tabella; la marea resta il passo dopo.**
