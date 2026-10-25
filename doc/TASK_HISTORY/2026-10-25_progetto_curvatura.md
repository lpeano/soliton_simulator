# IL PROGETTO DELLA CURVATURA DELLO SPAZIO, SULLA CARTA

> **Il mandato:** di Luca, «il piano di lavoro dopo il terzo passo del `U(1)`, e il progetto della curvatura dello spazio, sulla carta», parte `2` *([[PROGETTO-U1]], [[U1-PROTOTIPO-TRIANGOLI]], [[SPAZIOTEMPO-3PIU1]], [[DOMANDA-D9-GEOMETRIA]], [[LORENTZ-MATERIA-INTERFERENZA]])*.
> ### **NESSUN CODICE, NESSUNA DECISIONE DI LUCA PRESA.** ### **Il documento sara' `doc/PROGETTO_CURVATURA.md`.** ### **Il piano e' in `83f6a8bd`.**

**LIVELLO:** un progetto sulla carta.

## 0. LA STELLA POLARE

1. **`A14`:** ### **non si applica** *(nessuna legge entra: e' un progetto)*; ### **il progetto chiede a ogni strada di dire se conserva carica ed energia localmente.**
2. **Il gradino:** ### **il progetto di una legge** *(le lunghezze proprie degli archi)*; ### **il criterio sara' un limite noto: `gamma = 1`.**
3. **Aggiunge un numero o una legge?** ### **Una legge** *(come `cs` entra nelle lunghezze)* ### **e forse un RIFERIMENTO** *(il `cs` della regione imperturbata, come `Phi = 0` all'infinito)*: ### **il riferimento e' la scelta piu' delicata, ed e' di Luca** *(`A1`)*.
4. **Tocca `rho`, `c_s` o il segno?** ### **`c_s`: e' il punto.** ### **Il verso curvatura -> materia e luce; il verso materia -> curvatura e' il canale di `cs`** *(il passo `4` del piano)*.
5. **Emergente o imposto?** ### **La strada `(A)` IMPONE `cs` nelle lunghezze; la `(C)` lo farebbe EMERGERE** *(la geometria dinamica, `D9`)*: ### **il progetto lo dice per ognuna.**

## 1. IL RAGIONAMENTO PRELIMINARE *(prima di leggere il codice in dettaglio)*

- ### **IN RELATIVITA' GENERALE, campo debole, coordinate isotrope:** ### **`ds^2 = cs^2 dt^2 - cs^-2 dx^2`** *(`cs ~ 1 + Phi`)*: ### **la velocita' coordinata della luce `cs^2`, la deflessione di Einstein, Shapiro col fattore `1 + gamma`, `gamma = 1`.** ### **La particella lenta: `H ~ cs m + cs^3 p^2/(2m)`, cioe' la caduta dipende SOLO da `g_00`.**
- ### **NEL MODELLO OGGI:** ### **`cs` entra solo come tempo proprio** *(`dtau_nodo`, `s_arco`)*; ### **nessuna lunghezza entra nel passo della camminata** *(e' topologica: `ii`, `jj`, gli angoli)*; ### **il campo `U(1)` ha i pesi `l`, `l*`, `A_p` del triangolo equilatero, fissi.** ### **Quindi `gamma = 0`** *(misurato: `fa7ee993`)*.
- ### **LA STRADA PIU' DIRETTA, sulla carta:** ### **una lunghezza propria per arco `l_a = cs_rif/cs_a`;** ### **nella camminata, l'angolo dello spostamento e' (tempo proprio)/(lunghezza propria): `pi s_a (s_a/s_rif)`;** ### **nel campo, `A_p` dalle tre lunghezze** *(Erone)*. ### **Il Grover e la moneta** *(i pezzi del nodo: l'orologio)* ### **restano a `pi s_n`.**
- ### ⚠ **LA DOMANDA CHE NON SO:** ### **la caduta della particella lenta resta quella di oggi** *(come vuole `g_00`)*? ### **Dipende da quanta parte della massa della coppia a `K` viene dallo spostamento e quanta dal Grover:** ### **se la massa viene ANCHE dall'arco, la strada `(A)` cambia la caduta** *(un rischio per il principio di equivalenza)*. ### **E il rapporto fra le due `c` in una regione uniforme lontana dal riferimento** *(l'obiezione di Luca)* ### **dipende da come `v_b` dipende dal rapporto fra il peso dello spostamento e quello del Grover: e' la misura `(e)`.**

## 2. LA PROGETTAZIONE

- ### **Dal codice, con file e riga:** ### **dove entra `cs`, dove entrerebbero le lunghezze, la geometria dei versori, il campo; dall'era `1`: `d`, `d0`, `vd`, la metrica come onda della deformazione, `PLAST_DIN`.**
- ### **Le strade `(A)`, `(B)`, `(C)`:** ### **per ognuna `gamma`, il rapporto delle due `c`, l'universalita', Gauss e la gauge, la reversibilita', `A1`, il ritorno al passo di oggi a `cs` uniforme.**
- ### **Le misure del prototipo** *(`a`-`f`)* ### **con DEVE, DEVE FALLIRE, PUO' FALLIRE fissati sulla carta; le scelte di Luca; il costo e l'ordine.**
- ### **Mi FERMO se:** ### **il codice dice che una lunghezza non puo' entrare nella camminata senza cambiare un assioma** *(lo scrivo come contrasto)*.

## 3. TODO DEL NEXT STEP

1. questo task history, da solo; 2. `doc/PROGETTO_CURVATURA.md`, la voce `FRONTE` nell'indice, la relazione.
