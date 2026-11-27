# TODO per la sessione successiva *(dal 2026-11-27)*

[[PROGETTO-MITOSI]]

Questo documento traduce in lista il piano di **[M0951]** *(DECISIONE DI LUCA, 2026-11-27 `09:51`, posta `30d9cd91`)*. Per ogni pezzo dice da dove si parte *(percorsi e sha1 dei byte)*, cosa e' gia' deciso e cosa e' in ATTESA DI LUCA.

> **TUTTO IL PIANO E' IN ATTESA DI LUCA:** un pezzo si esegue solo dopo un suo «leggi la posta» che porti la decisione. La parte di lettura di A e' una DELEGA, ma anche quella parte solo su mandato.

**I rami e i worktree:**

| ramo | worktree |
|---|---|
| `lapse-u` | `C:\Users\lpeano\wt_lapse_u` |
| `primo-ordine` | `C:\Users\lpeano\soliton_simulator` |
| `mitosi` | `C:\Users\lpeano\wt_mitosi` |

Le corse passano dal lanciatore `coda_m1446.py` *(su lapse-u)*.

## Lo stato alla chiusura *(2026-11-27, circa `10:15`)*

- **La coppia d1'** *(la scena: `M2034/coppia`, i dati in `E:/soliton_simulator/controllo/M2034/coppia/{d1,d2,d3}`)*:
  - le letture v3, v4 e v5 e il video `doc/referti_l2/anima_coppia.mp4` *(v2, `838d378e`)*;
  - D2'' dice VERSO `8`, VIA `4`, ND `0` *(`due_corpi_fondo_v6_C.txt`, `41ccae13`)*.
- **### IL VIDEO HA MOSTRATO** *(a occhio, non misurato; la relazione, pezzo 1d)*: a `k 3250` e a `k 6000` la materia e' **una nube sola**. Il «rimbalzo» fino a `d 27.87` puo' essere la distanza fra le due meta' di una nube che si allarga, e non fra due corpi.
- **La mitosi:**
  - la soglia e' chiusa *(S, `c09d2906`)*;
  - K4'' passa;
  - il vuoto puro con le nascite accese ha dato **`0` nascite in `6000` tick** *(`mitosi_vuoto_v3.txt`, ramo mitosi `82739c06`)*;
  - la norma deriva di `2.26e-12`, crescente in `24` passi su `24` *(domanda aperta)*.

## A. La coppia, la lettura seria *(DELEGA per la lettura; la corsa lunga e' ATTESA)*

- **A0 *(NUOVO, proposto da me dopo il video; ATTESA DI LUCA)*: due corpi o una nube?** Per ognuno dei `25` stati di d1' si contano i massimi locali di `rho_psi` sopra una frazione del massimo *(la soglia si fissa nella carta PRIMA)*.
  - Due picchi = due corpi; uno = fusione.
  - E' a costo zero, sugli stessi stati.
  - **Va fatto PRIMA di A1-A4:** tutti e quattro presuppongono due corpi distinti.
  - **Lo stato di partenza:** `M2034/coppia/d1/stato_*.npz`, `25` stati da `0` a `6000` ogni `250`. `serie.json` ha sha1 `512149ee`.
- **A1 — la corsa lunga d1''** da `k 6000` per altri `12000` tick, stati ogni `250`: il secondo e il terzo minimo di `d(k)`.
  - **Lo stato di partenza:** `M2034/coppia/d1/stato_006000.npz`, sha1 `aca74f48`.
  - **ATTESA DI LUCA, e subordinata ad A0:** se i corpi si sono fusi, non ci sono minimi da cercare.
- **A2 — il periodo radiale T contro la massa M e la profondita' del pozzo**, cioe' la «terza legge» in 2D.
  - **La forma attesa va scritta PRIMA:** il potenziale e' di Yukawa, con portata `100`, non `1/r`.
  - Dipende da A1 *(un periodo intero)*.
- **A3 — l'energia della coppia:** H totale, H_chi e l'energia cinetica dei baricentri lungo la corsa. Si conserva? Dove va?
  - Si parte dagli stessi `25` stati.
  - **Lo strumento per H** e' `mitosi_regola.energia_corsa` *(ramo mitosi)*, da adattare alla scena della coppia: **va deciso**.
- **A4 — le masse 1 e 4:** il corpo B prende la norma `x4`.
  - **Esiste gia' la tenuta a norma `x4`** *(a2, [M1631])*.
  - **Attenzione:** «massa 4» li' e' la NORMA `x4`, non la massa inerziale. `m*` di a2 vale `18.6350` contro `18.9162` di 1c *(la relazione, [M1631])*. **Il rapporto atteso delle accelerazioni non e' `4`:** va riscritto nella carta prima della corsa.
  - **ATTESA DI LUCA.**

## B. Il vento con due corpi *(a costo zero)*

- `J_phi` radiale attorno a ciascun corpo e lungo l'asse, da d1'.
- Si parte da `M2034/coppia/d1/stato_*.npz`; lo strumento di riferimento e' `vento_vuoto_v2.py`.
- **Lega con la deriva lungo x del baricentro della coppia** *(`-2.56` a `k 4250`, pezzo 1b)*: e' una domanda aperta. Il confronto con d2' *(chi spento)* dice se la causa e' il pozzo.

## C. La mitosi

- **C1 — il ritmo a `2 pi` contro il tempo:** le nascite per finestra di `500` lungo la fiammata. Esponenziale, lineare o a gradini? *(a costo zero)*
  - Si parte da `E:/soliton_simulator/controllo/mitosi_rami/{MITOSI,MITOSI_V2}/nascite_*.json`.
  - La fiammata va dalla nascita `12` *(`k 36294`)* a `k 45950`. Le prime due finestre contano gia' `26` e `45` nascite *(`doc/CARTA_mitosi.md`)*.
  - Lo strumento di riferimento e' `mitosi_energia_fiammata.py` *(referto `478703c8`)*.
- **C2 — la nascita nel vuoto CON il lapse:** chi acceso, nessuna materia, il vuoto che cade in un pozzo dipinto. **ATTESA:** e' una scena nuova.
  - Il vuoto puro senza lapse ha gia' dato `0` nascite in `6000` tick, da `M0237/vuoto_v2`.
- **C3 — `a(k) = sqrt(n(k))` dalla fiammata:** `H = a'/a` e `q = -a'' a / a'^2` per finestra. C'e' una fase decelerata prima di quella accelerata? *(a costo zero; si legge senza l'ipotesi Lambda)*
  - Si parte dagli stessi registri di C1 e da `n(k)` di `mitosi_energia_fiammata.py`.

## D. Le semine e il passo *(ATTESA)*

- Tre semine del vuoto per K della cima e del fondo.
- Il passo dimezzato per E(p): la piega si sposta?

## E. N come vincolo di Poisson *(ATTESA: scena nuova)*

- La stessa coppia con N dal solutore istantaneo `(c2 L + m2)^{-1}`, invece del chi dinamico. La differenza misurabile e' il ritardo.

## F. Gestione *(ATTESA, DECISIONE DI LUCA con l'ora: [M2145])*

- Gli stati `.npz` e i video fuori da git *(gitignore e un presidio)*.
- La RELAZIONE spezzata per mese.
- Il repo pesa `1.07 GB` *(il numero e' del guardiano: non l'ho rimisurato)*.
- **Nota:** `*.mp4` e' gia' nel `.gitignore`. I tre video tracciati *(`anima_tenuta_fondo.mp4`, `anima_vento.mp4`, `anima_coppia.mp4`)* sono stati aggiunti con `git add -f`.

## Le previsioni del guardiano *(scritte il 2026-11-27, prima della sessione)*

| pezzo | probabilita' | previsione |
|---|---|---|
| A1 | `55%` | il secondo minimo e' piu' basso del primo di oltre il `10%` |
| A3 | `60%` | H totale conservata entro `1e-3` relativo; l'energia dei baricentri si scambia con H_chi |
| C1 | `60%` | il ritmo e' a gradini |
| C3 | `70%` | `a(k)` accelera dall'inizio, senza fase decelerata |

**La mia, su A0, scritta ora:** **una nube sola dopo `k 3250`, al `75%`.**

## Le domande aperte per Luca

- **A0** prima di A1, cioe' la fusione.
- La deriva della norma nel vuoto puro.
- La deriva lungo x del baricentro della coppia.
- Le domande gia' in coda: M2210-r4; M0105-02; il segno di E(p); C1, D e M0140.
