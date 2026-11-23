# IL PREZZO DELLO SPAZIO: L'ENERGIA PERSA ALLE 538 NASCITE *(Luca, 2026-11-23, [M1739-E]; scritta PRIMA del codice e dei numeri, `18:00` da `date`; SOLA LETTURA, il ramo `mitosi`, file nuovi)* [[PROGETTO-MITOSI]]

## 1. COSA C'E' NEI DATI, E COSA NO

- **Per nascita** *(`nascite_36250.json`, `nascite_45976.json`)*: `DH = H1 - H0` *(l'energia del motore, `mitosi_regola.energia_corsa` = `somma conti_nodo["tot"] + K + V` del campo, prima e dopo la nascita, AL BIT, nello stesso tick)*, **e la sua scomposizione dalla regola:** `DH_nascita` *(il passo della nascita)* + `DH_flip` *(il giro dell'arco)*; `E_persa = -somma DH`.
- **Gli stati ogni `250`** *(con lo sha1)*: `Lambda` per nodo, `psi_h`, `phi_h`, `theta_a`, il grafo. **Le serie ogni `50`:** `E` *(la stessa `energia_corsa`)*, `D_n`, `D_epersa`.
- ### **COSA NON C'E': l'energia PER PEZZI** *(materia, vuoto, U, legame)* **un tick prima e un tick dopo la nascita.** Gli stati sono ogni `250` tick *(in una finestra cadono molte nascite e i tick in mezzo)*: **«per pezzi, prima/dopo, al bit» vuole una RIPRESA** dallo stato precedente fino al tick della nascita, **cioe' una corsa: il mandato dice sola lettura.** **NON MISURATO, la domanda a Luca** *([M1751] S1 autorizza la ripresa per `10` nascite: con quella si avrebbero i pezzi di quelle `10`)*.
- **Theta «al momento della nascita»:** l'arco che scatta ha `|Theta| >= 2 pi` per costruzione *(il contatore)*: non e' una misura. **Leggo Theta sui genitori** `Theta_v = somma |theta_a|` sugli archi di `i` e `j`, **nello stato salvato prima** *(come [M1623-L])*; **`rho` e `|phi - phi0|^2`** sui genitori nello stesso stato *(`phi0` come la carta delle nascite: la media sui mezzi archi coi due capi a `r > 60`)*; **`Lambda`** = la media di `Lambda` su `i` e `j` *(«l'energia del vuoto per nodo» del mandato: la leggo cosi', e lo dico)*.

## 2. IL CASO NOTO, DETTO PRIMA

- `E_persa = -somma DH` **e' vero per costruzione** *(il codice lo somma)*: non e' un caso noto. **Il confronto vero** e' con la deriva di `E` nella serie: `E(fine) - E(prima della prima nascita)` contiene **le nascite E i tick**. **E i tick NON conservano `E`:** nel tronco senza nascite `E` va da `8268610.17` *(k `3050`)* a `8267817.23` *(k `35750`)*. **Quindi «entro `1e-9`» fallira' quasi certamente per la deriva dei tick: lo giudico come scritto,** e in piu' tolgo la deriva dei tick stimata dal tronco *(la pendenza di `E(k)` su `k 30000-35750`, senza nascite)*, **dichiarato.**

## 3. LE LETTURE E I CRITERI *(dal mandato)*

- **(1)** `DH` per nascita: la media, la dispersione; contro `Lambda` e contro `rho` locale *(la correlazione e la pendenza)*. **(2)** il fit `DH = a + b Theta_v` *(minimi quadrati, `sigma_b` dai residui)*. **(3)** la frazione con `DH > 0`. **Per nodo:** `DH` e' gia' per un nodo nato *(una nascita = un nodo)*; «entro `+-30%` di una costante» = la frazione delle nascite con `|DH/media - 1| <= 0.3`.
- **LE PREVISIONI DEL GUARDIANO** *(copiate)*: `DH` sempre negativa `70%`; `|DH|` per nodo entro `+-30%` di una costante `45%`; `b` a `3 sigma` `40%`; `DH` proporzionale a `Lambda` entro il `30%` `35%`. **Le mie** *(ho visto in [M1623-L] media `-21.29`, da `-57.8` a `-2.5`: non sono cieche)*: sempre negativa `95%`; entro `+-30%` `30%`.
