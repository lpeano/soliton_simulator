# `D0'` E `TS`: LA PARTENZA RUOTATA E LA PARTENZA SIMMETRIZZATA *(Luca, le decisioni dopo `ae60cfb6`)*

**Il mandato** *(dopo `ae60cfb6`, punto `2`; in coda dopo `TF3C`, prima di `TFI` e `TL120`)*: due corse come `TP1000` *(fino a `16000`, il centro periodico, su `F0`)*.
**(a) `D0'`:** la partenza di `TP1000` ruotata di `180` gradi con `U = sigma_z`, e il vuoto ruotato *(`-F0`)*. **La previsione di Luca:** l'immagine ruotata di `TP1000` *(lo
spostamento a `+6.9` gradi da `+A1`)*; **scrivere da quando smettono di essere l'una l'immagine dell'altra.** **(b) `TS`:** una partenza SIMMETRIZZATA, uguale alla sua ruotata
*(`R180` con `sigma_z`)* a meno di una fase; l'inviluppo sul NODO, non sulla cella in avanti; la costruzione nella libreria col suo test `|R psi - c psi| / |psi| < 1e-12`. Le
letture (s1)-(s3) sono di Luca.

## 1. LE PREMESSE DAL CODICE *(cosa credo prima di guardare, e cosa NON so)*

- **La corsa `TP1000`** *(`corsa_accensione.corsa`)*: la partenza `p0 = V.partenza(sol, z, phi0, pK, s)` sul vuoto `F0` *(`phi0`)*; lo stato `z["st"]` ha **sei chiavi**:
  `psi` *(per nodo, `(n, 2)`)*, `psi_h` *(per estremita', `(2m, 2)`)*, `phi_h` *(per estremita')*, `Lambda`, `rho`, `h_int` *(per nodo)*. **Il tick vivo** e' `AC.tick(z, t, K)`:
  nella rampa *(`t < K`)* `tick_acceso` *(i pezzi del vuoto scalati di `lam`)*, dopo `TK.percorri_tick` *(il tick intero del nucleo)*. **Il motore** ha uno stato suo
  *(`apri_tick`, `chiudi_tick`, il contatore delle crescite)*: **non so** se tiene altro che conti per lo stato della scena.
- **La rotazione** *(`carta_impulso.rotazione`)*: `m -> m2 - m` attorno al centro d'inversione `m2 / 2 = (40.5, 40.5)`; l'arco `(v, a)` va nell'arco `(R(v + d_a), a)`
  ROVESCIATO. **Le chiavi per estremita'** `psi_h` con `sigma_z` e `phi_h` senza; **le chiavi per nodo** con la mappa dei nodi; **`psi` per nodo: non so** se e' derivata da
  `psi_h` *(allora si ricalcola)* o una variabile del tick *(allora va ruotata, e con quale `U` lo dice il tick)*. **Nel referto dell'impulso** il tick CONGELATO della materia
  commuta con `R180` e `sigma_z` a `1.0e-16`, su `F0` e su `F3`; il vuoto ruotato di `F0` e' `-F0`. **Il tick del vuoto a `psi = 0`** commuta con le rotazioni *((f5), `freccia_F0.txt`)*.
  ### **NON e' misurato: il tick VIVO intero** *(materia + vuoto, la rampa, `eps`, la moneta)* **contro `R180` x `sigma_z`.**
- ### **Se il tick vivo commuta, la previsione di Luca e' VERA PER COSTRUZIONE fino all'arrotondamento:** `D0'` diventa la misura di QUANTO in fretta l'arrotondamento
  separa le due corse *(il caos deterministico)*, non una prova della fisica. **Se non commuta, la previsione cade gia' sulle leggi**, e la corsa non serve a saperlo.
  **Quindi un controllo di minuti PRIMA della corsa di ~`2` ore.**
- **La domanda della fase globale di `phi`** *(`-F0` contro `F0`)*: se il tick vivo commuta con la rotazione **su tutto lo stato**, il vuoto giusto e' `R F0 = -F0` e la domanda
  non serve a `D0'`. **Resta una domanda a se'** *(il tick legge la fase globale di `phi`?)*: **non la misuro qui** se non serve.
- **`TS`, l'inviluppo sul nodo** *(dalla bozza)*: `psi[e] = inv(nodo(e)) q_e`; con `inv(R v) = inv(v)` il ruotato vale `R psi = c psi` **SOLO SE `sigma_z q_{a,coda} = c q_{a,testa}`
  e `sigma_z q_{a,testa} = c q_{a,coda}` per ogni asse `a`** *(lo spinore `q` della coppia di `B` a `Gamma`)*. **Non so se vale: si misura.** **Se non vale, l'inviluppo sul nodo
  NON basta**, e l'unica costruzione esatta che vedo e' la proiezione `(1 + R) psi` *(o `(1 - R) psi`)*: **una scelta di settore, che non faccio io.** **E l'inviluppo:** anche `pK`
  e' per estremita'; la norma per nodo si fa con `densita`, non con `reshape(n, 12)` *(la riga e' una cella orientata)*.

## 2. PROGETTAZIONE DEL RAGIONAMENTO

1. **La carta di `D0'`** *(`csv/solitone/carta_d0.py`, minuti, nessuna corsa; committata prima di girarla, `D6`, la cassetta)*:

| | che cosa | il tipo |
|---|---|---|
| `D-R2` | la rotazione di tutto lo stato due volte e' l'identita' *(al bit, ogni chiave)* | DEVE PASSARE |
| `D-V` | il vuoto ruotato di `F0` e' `-F0` *(lo scarto relativo, entro `1e-12`)* | DEVE PASSARE |
| `D-T` | **il tick VIVO** *(`AC.tick`, `10` tick dalla partenza nella rampa, e `10` tick dopo la rampa da uno stato di `TP1000` dopo `K`)*: `|T^10(R x) - R T^10(x)| / |x|` sotto `1e-12`, ogni chiave | DEVE PASSARE |
| `D-T-F` | lo stesso con `U = 1` sulle due componenti | DEVE FALLIRE |
| `D-P` | `psi` per nodo: derivata da `psi_h`, o ruotata con quale `U` *(si legge dal codice e si misura: il tick che parte da `psi` ruotato in due modi)* | registrata |

   **La soglia `1e-12`** e' la stessa di `carta_impulso` *(`TOLL_UGUALE`)*: non tarata qui. **Lo stato dopo la rampa:** il primo stato completo di `TP1000` oltre `K = 6667`
   che c'e' *(`TM1000` a `13333`, su `E:`, al bit di `TP1000`)*.
2. **Se `D-T` passa:** la corsa `D0'` *(un nome in `CORSE`, `(1000, 16000)`)*, la partenza `R p0` e il vuoto `R F0`, gli stati completi agli stessi tick di `TM1000`
   *(`13333`, `40000`, `66667`)*; **la carta del confronto**: per ogni campione `|X_D0' - X_im|` *(`X_im` l'immagine del centro di `TP1000`)*, e agli stati
   `|st_D0' - R st_TM1000| / |st|` per chiave. **Nessuna soglia di «separazione»:** la tabella in scala logaritmica, e la lettura «da quando» e' di Luca.
   **Se `D-T` fallisce:** il referto, la relazione, **FERMO**: la previsione cade sulle leggi, e cosa fare e' di Luca.
3. **`TS`, dopo `D0'`:** una carta di minuti misura `sigma_z q_coda = c q_testa` per ogni asse. **Se vale:** la costruzione nella libreria *(`protetto`, una funzione nuova)* col
   test `|R psi - c psi| / |psi| < 1e-12` e un caso che deve fallire *(l'inviluppo di oggi, `0.995`)*; poi la corsa. **Se non vale: FERMO**, e la domanda del settore a Luca.

### Che cosa mi farebbe FERMARE
`D-T` che fallisce *(la previsione cade sulle leggi)*; `D-R2` o `D-V` che falliscono *(la rotazione e' sbagliata: prima si corregge, un commit a se')*; un `D-T-F` che PASSA *(il
controllo non legge `U`)*; per `TS` la condizione su `q` che non vale.

## 3. TODO DEL NEXT STEP
- [ ] questo file, la relazione; commit;
- [ ] `carta_d0.py`, l'inventario; commit; `D6`; la cassetta; la carta; il referto;
- [ ] se `D-T` passa: la corsa `D0'` *(~`2` ore)*, la carta del confronto; se no: FERMO;
- [ ] `TS`: la carta della condizione su `q`; poi la costruzione o FERMO.
- [ ] **`TFI`:** Luca decide ora che `TF3C` e' finita *(non e' in questa coda finche' non decide)*.

## 4. ESITO DEL PASSO 1 *(`d0_simmetria_vivo.txt`, `7/7`)*

- **`D-T` passa:** il tick vivo commuta con `R180` x `sigma_z` *(`5.194e-15` dopo la rampa, `7.631e-16` nella rampa; U = 1 `2.929e-01`)*. **Il vuoto ruotato e' `-F0` esattamente.** **`psi` per nodo e `h_int` sono nulli e non scritti:** il loro zero e' un falso-zero *(dichiarato)*. **Nella rampa `lam` e' `5.6e-06`:** il vuoto lo prova il controllo dopo la rampa.
- **Quindi il passo 2: la corsa `D0'`**, come progettato. **Niente mi ha fatto fermare.**

## 5. LA CODA DOPO LE DECISIONI DI LUCA *(dopo `eaa5e3ec`)*

- **La lettura (f1)**; **`TFI` in lista d'attesa**; **`F3` il vuoto predefinito delle prove nuove**.
- **La coda:** `D0R` *(il referto coi tempi delle decadi `1e-12`, `1e-6`, `1e-2`)*, poi `TS` *(su `F0` e, se il costo lo permette, su `F3`: dichiararlo)*, poi `TL120` su `F3`, poi il resto.

## 6. ESITO DEL PASSO 2 *(`d0_confronto.txt`, `4/4`)*

- **I tempi:** `1e-12` a `631.5`, `1e-6` a `957`, `1e-2` a `1179`; una decade ogni `~50`-`70` unita' di tempo dalla rampa; gli stati d'ordine `1` gia' a `2000`.
- **La direzione:** `D0R` `-137.43` gradi contro l'immagine di `TP1000` a `+6.94`: **la previsione di Luca vale fino a `~1000` e poi no.** Le grandezze grandi *(cuore, `w`, alone)* restano vicine.
- **Niente mi ha fatto fermare.** La lettura e' di Luca.

## 7. ESITO DEL PASSO 3 *(`ts_condizione.txt`, `6/6`)*: **FERMO**

- **`P` sulla coppia: `+1` e `-1`** *(degeneri al bit)*: **la `q` simmetrica e' una SCELTA DI SETTORE** *(`q+` o `q-`)*: di Luca.
- **L'inviluppo di `pK` per nodo non e' simmetrico** *(`4.63e-02`; il centro a `(40.333, 40.333)`, un centro di triangolo)*: serve un inviluppo simmetrico; **la proposta** *(la densita' simmetrizzata)* **e' da approvare.**
- **Il codice di `TS` non si scrive prima delle due risposte.**

## 8. LE DUE SCELTE DI LUCA *(dopo `aad1435a`)* E LA PROGETTAZIONE DI `TS`

- **Il settore: `q+`** *(`P = +1`)*, una corsa sola; `q-` solo se `q+` da' un risultato da capire *(decide Luca)*. **L'inviluppo:** la densita' di `pK` per nodo simmetrizzata attorno al centro d'inversione piu' vicino, `inv(v) = sqrt((rho_K(v) + rho_K(R v)) / 2)`, `psi[e] = inv(nodo(e)) q+[a, s]`; `N` come `TP1000`. **La corsa su `F0` fino a `16000`**; nel referto quando la simmetria si rompe *(`1e-12`, `1e-6`, `1e-2`)* e la direzione.
- ### **UNA PREMESSA NUOVA, scritta prima del codice:** **il vuoto `F0` ruotato e' `-F0`** *(`D-V`)*, non `F0`. **Quindi lo stato `(psi_TS, F0)` e' simmetrico solo per `S` = `R180` x `sigma_z` su `psi` e `R180` seguito da `phi -> -phi` su `phi`**: `S psi = psi` *(`q+`, l'inviluppo simmetrico)* e `S phi = -R F0 = F0`. **`S` commuta col tick vivo SE il tick commuta con `R180` x `sigma_z`** *(`D-T`, misurato: `5.2e-15`)* **E con il segno globale `phi -> -phi`** *(NON misurato)*. ### **Un DEVE nuovo, nel test:** il tick vivo *(10 tick nella rampa e 10 dopo)* commuta con `phi -> -phi` *(`|T(psi, -phi) - (psi', -phi')|` entro `1e-12`)*. **Se non commuta, `TS` su `F0` non puo' essere esattamente simmetrica: FERMO.**
- **Una convenzione mia, dichiarata:** la fase globale di `q+` *(l'autovettore e' definito a meno di una fase)*: **la componente di modulo massimo reale positiva.** Con `P q+ = +q+` e l'inviluppo simmetrico `c = +1` esattamente.
- **Il codice:**
  1. `protetto.q_simmetrica(z, phi0, s, segno)` *(l'autovettore di `P` nella coppia, la convenzione di fase)* e `protetto.partenza_simmetrica(z, phi0, pK, s, N)` *(l'inviluppo simmetrizzato, `m2` il centro d'inversione piu' vicino al centro di `pK`)*.
  2. `test_simmetrica.py` nella cassetta: `S1` `|S psi - c psi| / |psi|` sotto `1e-12` e `c = 1`; `S1-F` *(deve fallire)* la partenza di oggi; `S2` la norma `N`; `S3` `q+` nella coppia *(il residuo di Bloch)*; **`S4` il tick vivo commuta con `phi -> -phi`**; `S4-F` *(deve fallire)* con `phi -> 1.1 phi`.
  3. `corsa_accensione`: `CORSE["TS"]`, la partenza simmetrica; **in ogni campione la distanza dello stato dal suo `S`** *(`psi_h` e `phi_h`, con `c` stimato)*; `info` della scena invariato *(il controllo della scena)*, `mu` di `TS` registrato a parte.
  4. La carta del referto: i tempi `1e-12`, `1e-6`, `1e-2`; lo spostamento e la direzione contro `TP1000` e `D0R`; cuore, `w`, alone.

## 9. LA CORREZIONE DI LUCA *(21:14)*: `TS` SU `F3`, FINO A `30000`

- **Il vuoto `F3`** *(il predefinito delle prove nuove)*, **fino a `30000`** *(su `F3` la corsa e' partita a `~16000`)*; **il confronto con `TF3` + `TF3C`**. `TS` su `F0` non era partita: niente da interrompere. Il resto *(`q+`, l'inviluppo, l'ordine)* com'era.
- ### **La premessa cambia col vuoto:** **non so quanto vale `R F3`.** **`S0`** *(registrata e DEVE)*: `c_v = <F3, R F3> / |F3|^2` e `|R F3 - c_v F3| / |F3|` entro `1e-12`. **Se `c_v = +1`**, `S` su `phi` e' la sola `R` e il segno globale non entra *(`S4` resta un controllo in piu')*; **se `c_v = -1`**, `S4` e' necessario come prima; **se `R F3` non e' `+-F3`, `TS` su `F3` non puo' essere simmetrica: FERMO.**
- **La costruzione:** la partenza simmetrica sulla scena *(`F0`, come `TF3`)*, poi il vuoto sostituito con `F3` *(`VUOTI`, come `TF3`)*. **La coppia di `B` a `Gamma` e' la stessa su `F0` e `F3`** *(`ts_condizione.txt`)*.

## 10. ESITO DI `TS` *(`doc/referti_l2/ts_corsa.txt`, `5/5`; `carta_ts_corsa.py` `de1d29b5`, `corsa_accensione.py` `7a401775`)*

- **I DEVE:** `T0` *(la partenza registrata = `partenza_ts` ricalcolata, `20` pezzi; autovalore `+1`)*, `T0-F`, `T1` *(a `t 0`: `psi` `8.3e-16`, `phi` `1.1e-16`)*, `A3` *(`M` `+3.9e-12`, `V` `+2.7e-12` per `1000`)*, `A4`: **passano tutti.**
- **Quando la simmetria si rompe** *(`psi_h`)*: **`1e-12` a `565.5`**, **`1e-6` a `1092.0`**, **`1e-2` a `1381.5`**, `1e-1` a `1792.5`; `phi_h` circa `80` unita' prima *(`486.0`, `1005.0`, `1290.0`)*. **Il seme si vede gia' a `1.5`** *(`psi` `1e-15`)*: **l'arrotondamento** *(`R180` commuta col tick a `5.2e-15`, non al bit)*. Circa un ordine ogni `~80` unita' di tempo *(fra `1e-12` e `1e-2`)*; **`D0R`** dava `631.5`, `957`, `1179`.
- ### **IL MOTO PARTE, E PARTE PRIMA:** **`TS` corre da `~4000`** *(`1.96` per `1000` a `4000-5000`, il massimo **`12.04` a `7000-8000`**, `+35.7` gradi)*; **`TF3 + TF3C` da `~16000`** *(il massimo `22.35` a `17000-18000`)*. **`TS` ha un secondo picco** *(`12.02` a `15000-16000`)* **e poi rallenta** *(`0.93` a `29000-30000`)*.
- **La direzione:** `TS` **`117.9` nodi a `+7.9` gradi**; `TF3 + TF3C` **`87.8` nodi a `-158.2` gradi**. **Il moto di `TS` persiste:** `C(k)` non scende sotto `0.5` entro `k = 10` *(`TF3`: `k = 1`)*.
- **Le letture (s1)-(s3) sono di Luca.** ### **Un fatto che il mandato non prevedeva:** con la partenza simmetrica il moto **non sparisce e non tarda: anticipa di `~12000`**. **Non so dire perche'** da questa corsa sola: la partenza simmetrizzata **e' un'altra partenza** *(l'inviluppo simmetrizzato, `q+`, `mu` `4.1679`)*, non solo la stessa senza seme.
