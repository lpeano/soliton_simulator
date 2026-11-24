# [M0528] IL REFERTO FINALE DEL TORNEO (G1) E LA CARTA DEL LAPSE COME MOLTIPLICATORE *(Luca, 2026-11-23 dopo le `05:20`)* [[PROGETTO-MITOSI]]

## 1. LE PREMESSE DAL CODICE *(cosa credo prima di guardare, e cosa NON so)*

- `git log --all --grep M0528`: **nessun pezzo fatto** *(05:31)*.
- **La Parte 1 e' SOLA LETTURA** dai referti di `doc/referti_l2/` del ramo `lapse-u`: `torneo_tenuta.txt`, `torneo_tenuta_v2.txt`, `torneo_kt_v2.txt`, `torneo_kt_v2_Z.txt`, `torneo_giudizio_5a.md`, `fondo_giudizio_5b.md`, `torneo_FH_FT.txt`, `torneo_FH_FT_giudizio.md`, `inerzie_giudizio.md`, `FH_giudizio.md`, `spettro_gap_v2.txt`; nessuna corsa.
- **Cosa NON so / non c'e':** `omega` di `L+0.5`, `L+0.25`, `L0` alla cima **non e' mai stato misurato** *(le tenute v1 non registravano `omega`)*: nella tabella va NON MISURATO, non lo ricavo. **Gli orologi V2/V3 e la caduta V3 esistono solo per F0.** **La carta del torneo ha P1-P6, non P1-P8:** il mandato dice P1-P8 di [M1631]; scrivo P1-P6 e, come P7 e P8, le previsioni della portante *(sez. 11)* e del fondo *(sez. 13)*, **dichiarando che la numerazione e' mia.**
- **MITOSI-v2:** il registro del ramo `mitosi` dice FINITO a `k 45976` *(`--fino 45976`)* alle `21:28:50` del 22/11, uscita 0, `538` nascite all'ultima tappa; **la chiusura e' sul disco di `wt_mitosi` e NON committata** *(121 righe aggiunte, tutte di quella voce)*: la committo sul ramo `mitosi`, solo il registro.
- **La Parte 2** *(la carta del lapse risolto)*: **devo leggere `conti.py` e il collegamento di `chi`** *(il coefficiente della tensione, `c^2`, `kappa`)* prima di scrivere il vincolo: **non so ancora se il libro dei conti ha un'energia per nodo `eps_i` o solo totali.**

## 2. PROGETTAZIONE DEL RAGIONAMENTO

- **1a** la tabella del torneo riga per forma, ogni cella col referto da cui viene; le celle vuote = NON MISURATO. **Le previsioni** una per una: PASSA / MANCATA / NON GIUDICABILE *(se la grandezza non e' misurata, o la prova e' caduta per decisione)*.
- **1b** la sagoma: S4, S5, S16, S17, S18, e MITOSI-v2; **1c** la MAPPA e il progetto *(ramo `vincoli`, sez. 6)*.
- **2a** la carta: **cosa mi fa FERMARE:** se dal libro dei conti NON esce un'energia locale `eps_i N_i` *(cioe' se il vincolo andrebbe POSTULATO e non derivato)*, lo scrivo nella carta come premessa che cade e FERMO.

## 3. TODO DEL NEXT STEP

1. il commit di questo task history; 2. il registro del ramo `mitosi`; 3. `TORNEO_FINALE.md` (1a); 4. la sagoma (1b); 5. la MAPPA (1c) e PROGETTO_VINCOLI sez. 6; 6. la lettura di `conti.py` e di `chi`; 7. `doc/CARTA_lapse_moltiplicatore.md` (2a); FERMO.
