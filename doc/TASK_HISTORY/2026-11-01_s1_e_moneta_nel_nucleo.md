# 2026-11-01 — `S1` E LA MONETA NEL NUCLEO *(la decisione di Luca delle `16:52` del `2026-11-01`; le decisioni (1) e (7) delle `01:27`; [[STRUMENTO-LEGGE-DALLA-TABELLA]], [[PIANO-2D-3D]], [[SUITE-NEL-COMMIT]])*

> **La decisione di Luca:** il nucleo usa `S1` e la moneta accesa *(eps `0.5`)*, **tutte e due lette dalla tabella**; `S3` resta come **opzione esplicita**, solo per riprodurre il vecchio; gli script vecchi di `csv/` restano come sono, **storici**; il lavoro nuovo passa da `csv/solitone/`.

## 1. LE PREMESSE DAL CODICE

### Dove vive oggi la forma *(i blob sha1-BYTE di oggi)*
- **`primo_ordine/materia_vuoto.py`** *(`68ff3ffd`)*: `N` *(riga `63`)*, `alpha` *(`80`)*, `beta` *(`94`)*, `pezzi` *(`111`, «quello che il motore chiede»)*, `applica` *(`116`: chiama `pezzi(rho, lam)` **per nome di modulo**, e dunque una sostituzione di `MV.pezzi` la vede)*. **`S3`:** `N = rho ln(rho/(rho+Lambda))`, `alpha = ln(rho/(rho+Lambda)) + Lambda/(rho+Lambda)`, `beta = -rho/(rho+Lambda)`.
- **La tabella** `primo_ordine/leggi/leggi.yaml`, `CAMM-MATERIA-VUOTO` *(blob `2593860b`)*: `generatore: rho*log(rho/(rho + Lambda))`, **`parametri: {}`**. Il modulo generato `primo_ordine/termini/camm_materia_vuoto.py` porta `GENERATORE` e `PARAMETRI = {}`.
- **`S1` entra solo da `csv/`:** `csv/_screening_forme_s3.py` *(`80ffe96c`)*, `_ab("S1", x)` = `(x^2/(1+x^2), x - arctan x - x^3/(1+x^2))` con **`x = rho/Lambda`**, `pezzi_di("S1")` *(il vettore su `rho > 0`)*, `forma(nome)` *(sostituisce `MV.pezzi` in un contesto)*. **`pezzi_di("S3")` restituisce `MV.pezzi`, la funzione del CODICE.** L'energia di `S1`: `csv/_scomposizione_solitone.F1(x) = x - arctan x`, `E_leg = sum(Lambda F1(rho/Lambda))`.
- **`energia.py`** usa `MV.N` *(riga `118`)*: **l'energia del nucleo segue la forma del nucleo.**

### I parametri di `S1` come li usa `csv/` *(dal codice, nessuno nuovo)*
- **Nessuna costante:** la scala e' `x = rho/Lambda`, un rapporto, come per `S3`. **`g = 1`**: il fattore `g` esiste solo in `_livelli_piatti.configurazione(r, g)` *(`g alpha`, `g beta`, per la regola dei livelli piatti)*, e a `g 1` vale `1.0`. **Nel nucleo `S1` entra senza `g`.**
- **La coerenza** *(acbdfb88)*: `alpha = F1'(x)`, `beta = F1(x) - x F1'(x)`, cioe' `alpha = dN/drho` e `beta = dN/dLambda` con `N = Lambda F1(rho/Lambda)`. **Il vuoto riceve la rotazione gemella** per `S1` e per `S3`.
- ### ⚠ **`Lambda = 0` con `rho > 0`:** in `csv/` `x = rho/Lambda` e' infinito, e `alpha` e' `nan` *(in nessuna scena di `csv/` succede: il vuoto e' positivo ovunque)*. **Nel nucleo si scrive il LIMITE, non un pavimento** *(`A11`, come `rho = 0` per `S3`)*: `alpha -> 1`, `beta -> -pi/2`, `N -> rho`. **Dove `Lambda > 0` le espressioni sono QUELLE di `csv/`, operazione per operazione** *(il confronto al bit)*.

### Ogni punto che chiama `alpha`, `beta`, `N`, `pezzi`, `EPS_MONETA` o scrive `"eps": 0.5`
- **nel nucleo:** `motore._materia_vuoto` -> `MV.applica`; `energia.py:118` `MV.N`; `scena_l2.py:81` `EPS_MONETA = 0.5`, `:115` il suo uso, `:283` `{"eps": 0.5}`; `bande.py:65`, `bande_floquet.py:69`, `corrente.py:326`, `deriva.py:156`: `{"eps": 0.5}` scritto a mano.
- **nei collaudi del nucleo:** `_collauda_materia_vuoto.py` *(`MV.pezzi` `97`, `110`, `285`; `MV.N` `126`, `133`, `135`)*; `_collauda_deriva.py:148` *(`MV.beta`, chiamato «`b_s3`»)*; `{"eps": 0.5}` in `_collauda_checkpoint.py:73`, `_collauda_energia.py:40`, `_collauda_memoria.py:198`, `283`, `365`, `_collauda_motore.py:98`, `170`, `256`, `264`, `269`, `270`, `_misura_costo_motore.py:53`, `58`.
- **in `csv/`** *(non si toccano)*: `_screening_forme_s3.py`, `_s3_diluita.py`, `_solitone_con_la_buca.py` chiamano `MV.*`; **`11` script che fanno girare il passo senza nominare la forma** *(un censimento per parola: `_conto_del_vuoto`, `_controllo_passo`, `_instabilita_dtau_piccolo`, `_sigillo_scena_triangoli`, `_tolleranza_omega`, `_triangoli`, `_triangoli_bassa_energia`, `_triangoli_forza`, `_u1_prototipo`, `_u1_secondo`, `_vuoto_sul_fondo`)*: **girano con la forma del nucleo, cioe' `S3` fino a oggi.**

### Che cosa ne segue, PRIMA del codice
- **Gli script vecchi che girano `S3` per omissione** *(i `11` sopra, e `_screening_forme_s3.pezzi_di("S3")`, che restituisce `MV.pezzi`)* **cambiano risultato a `HEAD`** quando il predefinito diventa `S1`. **Restano riproducibili al LORO commit** *(la regola: un sigillo si rigira con `git checkout` del commit che ha sigillato)*. **La riga «storico» lo dice per tutti**; e la frase di Luca «forma `S1` da `csv/`» **non e' vera per questi `11`**: lo scrivo, non lo nascondo.
- **`csv/solitone/` non cambia numeri:** le sue corse girano dentro `SF.forma("S1")`, che sostituisce `MV.pezzi` con quello di `csv/`. **Il predefinito del nucleo non entra.** Lo verifica il collaudo `38/38`.
- **L'energia del nucleo con `S1`** e' `N_S1`: cambia per chi la usa senza scegliere.

### Cosa NON so
- **quanti collaudi del nucleo cambiano con `S1`** *(la lettura (n2))*: lo misuro, girandoli col predefinito;
- se qualche collaudo **lancia altri processi** che non vedrebbero una scelta di `S3` fatta nel processo padre *(il caso del FERMO del mandato)*.

## 2. LA PROGETTAZIONE

1. **La tabella:** in `CAMM-MATERIA-VUOTO`, `parametri.forma` con `valore: S1`, `ammessi` *(`S1` e `S3`, ciascuno col suo generatore: `rho - Lambda*atan(rho/Lambda)` e `rho*log(rho/(rho + Lambda))`)*, `dimensione: E^0`, `origine` *(la decisione di Luca e le espressioni di `csv/`)*; `generatore` **diventa quello di `S1`**. Si rigenera: `PARAMETRI = {'forma': 'S1'}` nel modulo generato, l'impronta, la scheda.
2. **`materia_vuoto`:** `N_s3`, `alpha_s3`, `beta_s3` *(le funzioni di oggi, i corpi intatti)*; `N_s1`, `alpha_s1`, `beta_s1` *(le espressioni di `csv/`, piu' il limite a `Lambda = 0`)*; `FORME = {"S1": ..., "S3": ...}`. **`FORMA` si legge dal modulo generato** *(`termini.camm_materia_vuoto.PARAMETRI["forma"]`)*, e `N`, `alpha`, `beta` sono quelli di `FORME[FORMA]`. **`pezzi` e `applica` restano come sono**, cosi' `SF.forma` di `csv/` continua a funzionare. **L'opzione esplicita:** `scegli(nome)` per un processo intero e `forma_esplicita(nome)`, un contesto. Un nome fuori da `FORME`, o fuori dagli `ammessi` della tabella, **alza**.
3. **eps:** `scena_l2.par_della_tabella()` restituisce `{"eps": termini.camm_moneta_spin.PARAMETRI["eps"]}`, e ogni `{"eps": 0.5}` del nucleo e dei suoi collaudi lo usa. **Il valore resta `0.5`:** i numeri non cambiano.
4. **`csv/solitone/protetto.forma_predefinita()`** legge la forma dalla tabella *(il modulo generato)*, non piu' da `_solitone_vuoto_congelato.FORMA`.
5. **La suite al bit:** lo strumento `csv/_suite_al_bit.py` gira ogni collaudo di `COLLAUDI`, uno alla volta, e salva lo `sha1` della sua uscita **senza le righe dei tempi**. Con `--forma S3` lo lancia dopo `MV.scegli("S3")` *(con `runpy`, nello stesso processo)*. **Si gira PRIMA del cambio** *(il riferimento)*; **DOPO, con `S3` esplicita** *(DEVE coincidere, collaudo per collaudo)*; e **DOPO, col predefinito** *(la lettura (n2): quali cambiano)*.

## 3. I CRITERI *(del mandato, scritti prima)*

| | il criterio |
|---|---|
| `K1` | **DEVE:** con `S3` esplicita ogni collaudo della suite ridà **la stessa uscita di prima** *(lo `sha1` senza i tempi)*, e lo stesso codice d'uscita. |
| `K2` | **DEVE:** col predefinito *(`S1`, eps `0.5`)* i `38` test di `csv/solitone/` passano **al bit**. |
| `K3` | **DEVE:** nel nucleo *(`primo_ordine/`, codice e collaudi)* `EPS_MONETA` e `"eps": 0.5` scritti a mano: **zero righe** fuori dalla tabella e dai moduli generati. |
| `K4` | **DEVE:** nessuna scelta di forma scritta a mano nel nucleo: `FORMA` si legge **solo** dal modulo generato, e le sole altre occorrenze sono l'opzione esplicita `S3` dei collaudi. |
| `K5` | **DEVE:** `beta` coerente con `alpha` per `S1` e per `S3`: `alpha = dN/drho` e `beta = dN/dLambda` a differenze finite *(come `_collauda_materia_vuoto`, righe `133`-`135`)*, e il limite a `Lambda = 0` di `S1`. |
| `K6` | **DEVE:** nessuno script vecchio di `csv/` cambiato *(i blob uguali dal commit di questo task history)*. |
| `K7` | Nessun peso tarato, **nessun parametro nuovo di `S1`**. **Un collaudo del nucleo che dipende da `S3` in un modo che `scegli("S3")` non risolve: FERMO.** |

## 4. LE LETTURE *(di Luca)*

- **(n1)** tutto al bit nei due casi: le decisioni (1) e (7) sono nel codice;
- **(n2)** qualche collaudo del nucleo cambia con `S1`: si elencano, coi numeri prima e dopo, e decide Luca;
- **(n3)** altro.

## 5. LA STELLA POLARE

1. **`A14`** *(`CONSERVAZIONE-LOCALE`)*: `S1` e' un flusso di sole fasi come `S3`. `rho` e `Lambda` non cambiano nel pezzo, quindi conserva la norma e `N_k` nodo per nodo. **`H_tot` col legame `S1` non e' la quantita' conservata** *(`ENERGIA-NON-CONSERVATA-S1`, acbdfb88)*: e' una violazione **gia' dichiarata**, e qui non cambia.
2. **Il gradino** *(`ROBUSTEZZA-FISICA`)*: non si afferma un risultato fisico nuovo. Si sposta un predefinito, e la prova e' l'identita' *(gradino (a), al bit)*.
3. **Numeri e leggi** *(`A1-COSTANTI`)*: **nessun numero nuovo.** `S1` non ha costanti. Le leggi che girano restano le stesse: `CAMM-MATERIA-VUOTO` cambia **forma**, non posto. `forma` e' un parametro **di scelta, non un numero tarato**. Non compensa un difetto: e' la decisione (1).
4. **Il verso** *(`EM-CURVATURA-BIDIREZIONALE`)*: tocca il legame `rho`-`Lambda` in tutti e due i versi, come prima *(`alpha` sulla materia, `beta` sul vuoto)*. Non tocca `cs` ne' il segno.
5. **Emergente o imposto:** non si applica, perche' non si osserva un fenomeno. Si allinea il nucleo a una decisione presa sulle misure di `csv/` *(a8e0e43b, 751bca7f)*.

## 6. TODO

1. Questo file, committato **DA SOLO**.
2. `csv/_suite_al_bit.py` e la riga d'inventario: committati; **il riferimento** girato sul nucleo di prima, committato *(`doc/referti_l2/s1_e_moneta_nel_nucleo/prima.json`)*.
3. Il nucleo: la tabella, la rigenerazione, `materia_vuoto`, `scena_l2` e gli altri `{"eps": 0.5}`, i collaudi del nucleo *(solo la riga di eps: il valore dalla tabella)*, il collaudo `K5`, `REGISTRO_FISICA`, `csv/solitone/protetto.forma_predefinita`. La SUITE nel messaggio. **Un commit.**
4. Le due corse della suite *(`S3` esplicita, poi il predefinito)* e il collaudo di `csv/solitone/`, uno alla volta.
5. Il referto `doc/referti_l2/s1_e_moneta_nel_nucleo.txt`; le righe «storico» nell'inventario; la MAPPA *(«nel codice:» di (1) e (7))*; `doc/DECISIONI_NEL_CODICE.md`; la relazione.
