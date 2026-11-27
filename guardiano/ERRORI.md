# Il registro degli errori del guardiano

**Ultimo numero: 252** (2026-11-24, 17:48). Il conto è cumulativo e non torna indietro. Una sessione nuova riparte dall'ultimo numero di questo file (la copia nel progetto Claude, `claude/ERRORI_del_guardiano.md`, è la stessa).

Regola: ogni errore del guardiano si dichiara a Luca con il suo numero, nel momento in cui lo si scopre; qui si registra con data, numero e una riga. Le previsioni mancate non sono errori (hanno la loro percentuale); lo sono le affermazioni false, i criteri sbagliati, le convenzioni scambiate, le cose dette senza averle lette.

## Dal 223 (22–24 novembre 2026)

| n. | data | errore |
|---|---|---|
| 223 | 22/11 | detto che chi-mattone-v2 era finita (era la corsa vecchia) |
| 224 | 22/11 | proposta una prova (coniugare lo stato) che non provava niente |
| 225 | 22/11 | criterio K3 col segno dato per scontato |
| 226 | 22/11 | zero della V3 sbagliato (corretto da CC: 1,103) |
| 227 | 22/11 | doppia copertura descritta come raddoppio dello spettro (è il mezzo angolo) |
| 228 | 22/11 | «lo zero simmetrico non l'abbiamo mai cercato» (è nel nucleo dall'8/11) |
| 229 | 22/11 | non previsto che v_max del solitone > banda fosse reale |
| 230 | 22/11 | θ dei pezzi liberi e dτ della non linearità creduti manopole separate |
| 231 | 22/11 | criterio K-T ±30% attorno a w(500) nel transitorio |
| 232 | 22/11 | controllo negativo del fondo dimenticato |
| 233 | 22/11 | «esiste un mattone sotto il fondo» scritto prima del controllo negativo |
| 234 | 22/11 | carica di U detta σ_z (è ρ) |
| 235 | 22/11 | riferimento della coppia preso da uno stato diverso |
| 236 | 22/11 | K3 della tenuta lunga misurava il respiro, non lo scioglimento |
| 237 | 22/11 | soglia di stazionarietà 1e-6 fuori scala |
| 238 | 23/11 | ω contata in assoluto invece che dal vuoto (lo specchio) |
| 239 | 23/11 | Pound–Rebka della luce mal posto; [M1633] ritirato |
| 240 | 23/11 | «il fondo della banda» letto come minimo dello spettro invece del fondo a K |
| 241 | 23/11 | nascite credute da k 0 (sono tutte dopo k 35976) |
| 242 | 23/11 | 6 gradi di libertà per nascita invece di 12 |
| 243 | 23/11 | la ripresa P8 fino alla nascita è una corsa, non «solo lettura» |
| 244 | 23/11 | sospettato CC di iniziativa su [M1658] 1b/1c/(iii): il mandato era mio, dimenticato dopo il taglio del contesto |
| 245 | 23/11 | `git ls-tree -l` su un clone senza blob (fetch dell'intero albero) |
| 246 | 23/11 | previsione «orologio come N in V3 e non in V2» copiata dalla cima senza specchiarla |
| 247 | 23/11 | tenuta a L 162 chiesta come robustezza: la scena era già L 162 |
| 248 | 24/11 | lo slogan della cima («va dove l'orologio accelera») riusato per il fondo, dove è falso |
| 249 | 24/11 | la convenzione dell'orologio di CC (Δ dal vuoto) detta ragionevole senza accorgersi che non era quella della cima: un fattore 6 scambiato per fisica |
| 250 | 24/11 | criterio «solo 5 file» applicato al ramo mitosi (che ne ha 9 propri) |
| 251 | 24/11 | criterio del periodo del respiro (minimi su w ogni 100) ingenuo: prende le increspature |
| 252 | 24/11 | criterio v3 (due minimi lisciati) non verificato sulla serie: un solo minimo, ripiego fuori dal giro |

## Prima del 223
I numeri 1–222 sono nelle sessioni di settembre–novembre; il dettaglio non è stato riportato qui. Si ricostruisce da RELAZIONE_PER_CLAUDE.md e dai documenti `claude/*` del progetto.

## Errori ricorrenti (per non rifarli)
- Misurare con precisione la cosa sbagliata: convenzioni (238, 249), finestre (236), scene (247).
- Scrivere il verdetto prima del controllo negativo (232, 233).
- Scrivere un criterio senza guardare la serie su cui si applica (231, 237, 251, 252).
- Credere al riassunto del contesto invece che al log (244).
- n.253 (2026-11-25 04:14) — [M0137] criterio B: «chi NON si media, si riparte da (psi medio, chi, pi) di fine giro». Il respiro è un modo accoppiato psi-chi (periodo ~2500): lasciare chi con il suo impulso rimette in moto l'oscillazione a ogni giro. Corretto in [M0414] (chi medio, pi = 0).
- n.254 (2026-11-25 04:14) — [M0137] criterio B: il periodo da w lisciata 500 con P = 2(k_min - k_max), già errore n.251, riusato: nel giro 2 ha dato P 200 con il massimo al bordo, e la media di psi è stata fatta su 200 tick. Corretto in [M0414] (P dai picchi di max|chi|(k)).
- n.256 (2026-11-27 00:24) — [M2034] criterio C: w entro il 5% per finestra di 500, dodici ore dopo aver dichiarato (D di [M0414]) che il respiro di w è un modo normale a ±20% con periodo 2500. Il riferimento fallisce il proprio criterio (0 su 12). Corretto in [M0024] (w sul periodo).
- n.257 (2026-11-27 01:06) — [M0024] D2': «nello stesso verso» al posto di «nello stesso intervallo»: una caduta 80 volte la deriva, nel verso opposto alla deriva, è finita «non distinguibile». CC ha applicato alla lettera e segnalato. Corretto in [M0106].
- n.258 (2026-11-27 01:06) — [M0024] K4': soglia |Delta H| < 1e-12 con H del vuoto puro 1,2e-10: sotto il pavimento dell'arrotondamento; CC l'aveva previsto. Corretto in [M0106] (la norma come criterio).
- n.259 (2026-11-27 14:33) — Il video didattico dell'esagono fatto sul nido d'ape (3 vicini) invece che sul reticolo triangolare (6 vicini, la moneta a sei vie, A2 = (-1/2, sqrt3/2)). Corretto da Luca, rifatto.
- n.260 (2026-11-27 15:22) — git ls-tree -l sul clone senza blob: l'errore n.245 rifatto identico. Fermato dopo 120 s.
