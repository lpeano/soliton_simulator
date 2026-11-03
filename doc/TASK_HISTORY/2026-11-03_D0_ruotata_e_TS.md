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
