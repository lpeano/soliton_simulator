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
