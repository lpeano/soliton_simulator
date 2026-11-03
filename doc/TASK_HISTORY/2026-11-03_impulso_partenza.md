# L'IMPULSO DELLA PARTENZA: UN ARTEFATTO NOSTRO? *(Luca `2026-11-03` `14:06`)*

> **La domanda di Luca:** che cosa crea il movimento? qualcosa che abbiamo messo noi? **Il sospetto del guardiano:** la partenza di BG-F-0.15 e' un inviluppo costruito a mano
> *(`protetto.inviluppo`: la norma per nodo dello stato di `A` a `K` per lo spinore `q` della coppia di `B` a `Gamma`, `theta`, `phi` da `griglia.json`)*; se porta una corrente
> netta, il solitone parte con una spinta data da noi.
> **Il controllo, sulla carta, sullo stato di partenza** *(lo stesso di `TP1000` e `TF3`)*, col vuoto `F0` e con `F3`: **(p1)** la corrente di materia totale e la sua direzione,
> e l'impulso medio rispetto a `Gamma`; **(p2)** le stesse per lo stato ruotato di `180` gradi *(deve cambiare segno)*; **(p3)** il centro dopo `1`, `10`, `100` tick a vuoto
> CONGELATO; **(p4)** lo stato e' uguale, a meno di una fase, al suo ruotato di `180` gradi, spin compreso?
> **Le letture, di Luca, scritte prima:** (q1) nulli entro l'arrotondamento, simmetrico: la partenza e' innocente; (q2) non nulli, verso `-A1` circa: la spinta la diamo noi, si
> propone una partenza simmetrizzata; (q3) non nulli in un'altra direzione: si scrive.
> **La coda** *(`[[PRECEDENZA-IN-CODA]]`, Luca: «prima di tutto»)*: **questo, poi la continuazione di `TF3`** *(`TF3C`, il task history `2026-11-03_TF3_lunga.md`)*, poi il resto.

## 1. LE PREMESSE DAL CODICE *(cosa credo, e cosa NON so)*

- ### **`psi` vive sulle ESTREMITA' degli archi, non sui nodi:** `psi_h` e' `(2m, 2)`, e il nodo di un'estremita' e' `inc.nodo[e]` *(`_energia_del_legame.densita`)*.
  **L'arco `k` appartiene al nodo `k // 3`** *(`scena_l2`, i `3` assi)*, con le estremita' `2k` sul nodo e `2k + 1` sul vicino.
- ### **QUINDI `protetto.inviluppo` NON prende «la norma per nodo»:** `pK.reshape(n, 12)` raggruppa le `6` estremita' dei **tre archi IN AVANTI** del nodo `v`
  *(verso `A2`, `A1`, `A1 + A2`)*: **tre estremita' su `v`, tre sui suoi vicini in avanti.** **E' una CELLA ORIENTATA** *(le tre direzioni stanno tutte nel semipiano a `60` gradi)*,
  e lo stesso `q` *(`12` componenti)* si mette su ogni cella. **Il docstring dice «per nodo»: il codice fa «per cella».** ### **Non so se questo conta per il moto:** un inviluppo
  reale per uno spinore costante ha l'impulso CANONICO nullo per costruzione *(sotto)*, ma la cella orientata e' un'**asimmetria** fra le direzioni `d` e `-d`, e **(p4) la vede**.
- ### **UN FALSO-ZERO, dichiarato prima:** l'impulso medio **canonico** di uno stato `inv(cella) x q` con `inv` reale e `q` uguale su ogni cella e' **nullo per costruzione**
  *(la correlazione con lo stato traslato e' reale e positiva)*. **Lo misuro lo stesso, ma non e' una prova d'innocenza.** **Il controllo che PUO' fallire** e' quello positivo:
  lo stesso stato moltiplicato per `e^{i k0 . r}` *(`k0 . A1 = 2 pi / L`)* deve ridare `k0`, e il suo ruotato `-k0`.
- **L'impulso, la definizione MIA:** per ogni direzione `d` del reticolo, `C_d = sum_e conj(psi[e]) . psi[T_d e]` *(`T_d` la traslazione di un passo lungo `d`, estremita' per
  estremita')*; per un'onda piana `C_d = |psi|^2 e^{i k . d}`, quindi `k . d = arg C_d` *(e' la media circolare di `e^{i k . d}` pesata con `|psi_hat(k)|^2`, cioe' la trasformata
  di Fourier)*; `k` dalle tre direzioni coi minimi quadrati. **Rispetto a `Gamma`:** `k = 0` e' `Gamma`.
- **La corrente:** `primo_ordine/corrente.py` **c'e', ma e' la corrente dell'ENERGIA, e costa `O(D^2)` con `D = 8 m`** *(il suo docstring: «su una scena grande non si fa»;
  qui `m = 19683`)*. **La corrente di materia totale la definisco io** *(dichiarata)*: **`J = M dX/dt`**, la derivata del centro della densita' su UN tick congelato
  *(Ehrenfest: la somma sugli archi del flusso e' la derivata del primo momento)*. **Quindi (p1) e' (p3) al primo tick**, ed e' la grandezza che decide.
- **Il centro:** il centro periodico *(`toro.centro`, come le corse)* della densita' per nodo *(`densita`)*. **Il tick congelato:** `_modo_al_variare_di_s.tick` *(lo stesso di
  `V.partenza` per `mu`: `_congelato_lungo.avanza`, i pezzi del vuoto saltati e `phi` rimesso a fine tick)*, `LP.FORMA`.
- **La rotazione di `180` gradi** *(attorno al nodo del centro, `m -> 2 m0 - m`)*: sulle estremita' come `freccia_F0.ruota` *(l'estremita' `(i, j)` va in `(R i, R j)`)*.
  **Sul vuoto:** `R F0 = -F0` *(la coda e la testa si scambiano)*, e lo stesso per `F3`: **il tick del ruotato si fa sul vuoto RUOTATO.** ### **Lo spin: NON so** come le due
  componenti si trasformano. **Non scelgo:** misuro la commutazione `|tick(R psi; R phi) - R tick(psi; phi)|` per `U` in `{1, sigma_x, sigma_y, sigma_z}` sulle due componenti, e
  **la simmetria del tick dice quale `U`** *(se nessuna commuta, la rotazione di `180` gradi non e' una simmetria del tick congelato, e (p2), (p4) sullo spin non si decidono:
  lo scrivo)*.
- **Il nodo del centro:** se il centro di partenza non cade su un nodo, la rotazione attorno al nodo piu' vicino sposta lo stato; **lo scrivo** *(lo scarto del centro)*.

## 2. PROGETTAZIONE DEL RAGIONAMENTO

1. Questo task history *(con quello di `TF3C`, gia' scritto, e il pezzo di `TFI` fermato)*: un commit.
2. **La carta** `csv/solitone/carta_impulso.py`, committata prima di girarla. **Nessuna modifica al nucleo, nessuna corsa lunga.** `D6`, la cassetta.
3. Il referto `doc/referti_l2/impulso_partenza.txt`, la relazione, l'esito, la MAPPA. **Le letture (q1)-(q3) sono di Luca.**

**I DEVE:**

| | che cosa | il tipo |
|---|---|---|
| `P0` | lo stato di partenza e' quello di `TP1000` *(`mu` uguale al bit a quello registrato nel primo pezzo)* | DEVE PASSARE |
| `P0-C` | l'arco `k` e' del nodo `k // 3`, l'estremita' `2k` sul nodo e `2k + 1` sul vicino lungo un asse fisso per `k % 3` *(la premessa della cella orientata; puo' fallire)* | DEVE PASSARE |
| `K+` | lo stato per `e^{i k0 . r}` ridà `k0` entro `1e-9` | DEVE PASSARE |
| `K-` | il suo ruotato di `180` gradi ridà `-k0` entro `1e-9` | DEVE PASSARE |
| `K-F` | lo stato senza la spinta ridà `k0` | DEVE FALLIRE |
| `R2` | la rotazione applicata due volte e' l'identita' *(al bit)* | DEVE PASSARE |

**Le misure:** (p1) `k` e `J` *(il modulo, l'angolo, i coseni con `A1`, `A2`, `A1+A2`)*, su `F0` e su `F3`; (p2) le stesse per il ruotato; (p3) lo spostamento del centro dopo
`1`, `10`, `100` tick, e la velocita' per `1000` accanto a quella del primo blocco di `TP1000` *(`0.590`)* e di `TF3` *(`0.063`)*; (p4) lo scarto `|R psi - c psi|` per i quattro `U`,
e quello della sola densita'; la commutazione per i quattro `U`, su `F0` e `F3`.

### Che cosa mi farebbe FERMARE
Un DEVE fallito; una commutazione che nessun `U` soddisfa *(lo scrivo, e le letture sullo spin restano aperte)*.

## 3. TODO DEL NEXT STEP
- [ ] commit di questo file; la carta; commit; `D6`; la cassetta; il referto; poi `TF3C`.

## 4. ESITO *(2026-11-03; il referto `doc/referti_l2/impulso_partenza.txt`, `7/7`)*

- **Tutti i DEVE passano.** **L'impulso canonico e' nullo** *(`2.0e-19`, il falso-zero dichiarato)*; **il centro a vuoto congelato si muove** *(`1.13e-3` nodi in `100` tick, lungo `-(A1+A2)`)*; **F0 e F3 a vuoto congelato uguali al bit**; **`R180` con `sigma_z` e' una simmetria esatta** *(`1.0e-16`)* **e lo stato non e' simmetrico** *(`0.995`)*; **la densita' spostata di `0.368` nodi lungo `A1+A2`** dalla cella orientata.
- **Le premesse, annotate:** la rotazione attorno al centro d'inversione piu' vicino, non al nodo; `U` dalla commutazione: **`sigma_z`**, l'unica.
- **Le letture (q1)-(q3) sono di Luca.** **TODO:** `TF3C` *(il task history `2026-11-03_TF3_lunga.md`)*.
