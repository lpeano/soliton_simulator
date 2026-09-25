# `POTENZE-1` — LA SCOMPOSIZIONE ESATTA DEL DIVARIO DEI FIGLI

*(criteri committati **PRIMA** della raccolta, par.5-septies. Mandato di Luca del 2026-09-26.)*

## L'IDENTITÀ CHE SI MISURA

`_contrasto = rho / peq_nodo`, quindi per un figlio `f` contro i maturi `m` **allo stesso passo**:

```
log(c_f/c_m) = log[(rho/W^2)_f / (rho/W^2)_m]  +  2 log(W_f/W_m)  -  log(peq_f/peq_m)
                \_________ T1 _________/         \____ T2 ____/      \____ T3 ____/
```

**È un'identità ESATTA**, non un'approssimazione: `T1 + T2 + T3 = log(c_f/c_m)` per algebra.
**E il suo valore sta nel significato dei tre pezzi:**

| | cosa è | chi lo toglierebbe |
|---|---|---|
| **`T2`** | `2 log(W_f/W_m)` — il figlio ha meno peso di vicinato | **`rho_s/W²`**: è **esattamente** il termine che quella cura rimuove |
| **`T3`** | `− log(peq_f/peq_m)` — il `peq` **ereditato** dall'arco del genitore | **`peq` alla nascita** |
| **`T1`** | ciò che resta in `rho/W²` **a parità di peso** | **nessuna delle due**: è la differenza *intrinseca* |

> ### **Se `rho_s/W²` fosse la cura giusta, `T2` dovrebbe essere la quota dominante.**
> ### **Se lo fosse `peq` alla nascita, `T3`.** **Le frazioni lo dicono, non il ragionamento.**

## COSA SI RACCOGLIE, e perché **queste** definizioni e non altre

| grandezza | come | perché così |
|---|---|---|
| **`W`** | la **STESSA `_wn` della cura**: `bincount(i, w) + bincount(j, w)` | **non ricalcolata a parte**: se la misura usasse una `W` diversa da quella che la cura userebbe, la scomposizione descriverebbe **un'altra cura** |
| **COPPIA** | la **STESSA `correzione`** che entra in `omega_new`, in **modulo** | `correzione` ha già dentro *tutti* i termini (`cross(B, nb)`, `_tq`…): ricostruirla da fuori è l'errore già fatto una volta, che dava **metà coppia** |
| `rho` | `_rho_sorgente()` | è l'ingresso vero di `_contrasto` |
| `peq_nodo` | `_diag_peq_nodo` | la **media per nodo**, non il `peq` d'arco |
| `contrasto`, `ramp`, `|omega|`, `grado` | come nel sigillo esteso | continuità col dato già preso |

**Le righe diagnostiche passano dalla POSTCONDIZIONE della copia** (`P9`): la copia si genera al run
e **deve differire SOLO** per le righe `self._diag_*` dichiarate, altrimenti **STOP**.

**⚠ E IL CONFRONTO È CON I MATURI DELLO STESSO PASSO**, non con una media del run: i maturi
**derivano** *(il loro contrasto va da `30` a `8.4` nei 120 passi)*, quindi un riferimento fisso
darebbe un divario che cambia **perché cambia il riferimento**.

## I CRITERI, fissati **ORA**

| | criterio | **cosa decide** |
|---|---|---|
| **`K1`** | l'identità **chiude**: `|T1+T2+T3 − log(c_f/c_m)| < 1e-9`, a **ogni** età e su **entrambi** i semi | che la raccolta sia **coerente**: se non chiude, `rho`, `peq` o `W` sono stati letti **in momenti diversi**, e **niente si legge** |
| **`K2`** | le tre frazioni hanno **lo stesso segno e lo stesso ordine** sui due semi, a ogni età | che la scomposizione sia **del sistema** e non di un seme |
| **`K3`** | `coppia ~ ramp^c` sui figli, con `R2` — **`R3bis`** | `c ≈ 1` *(entro `±0.3`)* → **l'asimmetria di esponenti è confermata**; `c ≈ 0` → **la coppia non porta `ramp`** e `R3bis` **cade**; altrimenti **si riporta il numero e resta aperto** |
| **`K4`** | il nullo: i **maturi allo stesso passo**, e la loro deriva dichiarata | senza, il divario si confonde con il movimento del riferimento |

**COSA MI FAREBBE FERMARE:**
- **`K1` che non chiude → STOP**, e il referto dice *«la raccolta è incoerente»*: **nessuna
  frazione si pubblica**. *(È il presidio contro me stesso: le tre frazioni sono numeri belli e
  convincenti, e pubblicarli da una raccolta sfasata sarebbe il peggio che posso fare qui.)*
- **`W_m = 0` o `peq_m = 0` su qualche passo** → quel passo **si esclude e si conta**, non si
  aggira con un `max(…, 1e-9)` *(`A11`)*.
- **meno di 3 età utilizzabili** → `K3` **non misurato**, non «fallito».

## COSA QUESTA LETTURA **NON** POTRÀ DIRE

- **quale cura scegliere.** Dà le **frazioni**; la scelta è di Luca, e il mandato dice **STOP**.
- **se `rho_s/W²` sia SICURA.** Toglie `T2` per costruzione, ma **non è misurato** che non rompa
  altro: `rho_s` entra in `lambda_nodi`, nella soglia della mitosi, nella coppia Schwinger.
- **niente sul taglio.** Questa è la famiglia dei **figli**; `C1'`/`C1''` restano dove sono.

---

# ❌❌ **DUE DIFETTI NELLO STRUMENTO, TROVATI DA LUCA SUL FILE COMMITTATO — PRIMA DEI DATI**

*(La raccolta era partita: **fermata**. I criteri qui sopra restano, con questa modifica.)*

## ① **IL RIFERIMENTO DEI MATURI ERA INCOERENTE: `K1` AVREBBE FALLITO PER COSTRUZIONE**

`c_m`, `rho_m`, `peq_m`, `W_m` erano **MEDIANE prese separatamente**. Ma l'identita' richiede
**`c_m = rho_m/peq_m`**, e **la mediana di un rapporto NON e' il rapporto delle mediane.**

> ### **`K1` avrebbe fallito ANCHE SU DATI PERFETTI, e io avrei cercato il difetto nella
> ### RACCOLTA.** Il criterio scritto come presidio contro me stesso **sarebbe diventato la
> ### trappola**: `STOP, la raccolta e' incoerente` su una raccolta sana.

## ② **L'AGGREGAZIONE PER ETA' NASCONDEVA LA NON-ADDITIVITA'**

Prendevo la **mediana** di `T1`, `T2`, `T3` **separatamente** e normalizzavo sulla loro somma:
**le frazioni sommavano al 100 % per COSTRUZIONE**, qualunque cosa facessero i dati.

## ✅ **LA CURA: MEDIA DEI LOGARITMI (media geometrica)**

`log` di una media geometrica e' **ADDITIVO**, quindi
`mean(log c) = mean(log rho) - mean(log peq)` **esattamente, nodo per nodo**.
**Si applica sia ai maturi sia ai figli di ogni eta'.** Le **mediane si riportano A PARTE**, come
descrizione dell'ordine di grandezza.

> ### **E `K1` DIVENTA UN CONTROLLO VERO:** non piu' *«ho aggregato in modo coerente?»* ma
> ### ***«il contrasto e' DAVVERO `rho/peq` nodo per nodo?»*** — che e' una domanda sul CODICE.

**⚠ E UN NUMERO CHE VA NEL REFERTO:** si tengono solo i nodi con **tutte e quattro** le grandezze
positive, perche' dove `_ok_n` e' falso `_contrasto` vale `1` per **convenzione** e li' l'identita'
**non deve** chiudere. **Quanti se ne scartano si conta e si stampa.**

## IL COLLAUDO (`P1-sexies`), FATTO **PRIMA** DEL RUN

Dati sintetici con `contrasto == rho/peq` **nodo per nodo**, `rho` e `peq` log-normali
**INDIPENDENTI** *(se fossero proporzionali il difetto non si vedrebbe: **il caso sintetico deve
CONTENERE il difetto**, non spiegarlo)*:

```
media GEOMETRICA   scarto massimo dell'identita'   1.776e-15      (atteso ~0)
MEDIANE separate   scarto massimo dell'identita'   4.748e-02      (atteso >> 0)
```

> ### ✅ **COLLAUDO 2/2:** la geometrica **chiude**, le mediane separate **non chiudono**.
> **Quindi `K1` non e' una tautologia:** se fallisce sul dato, il difetto e' nella **raccolta**.
> *(E il referto lo dichiara: se il collaudo fosse VUOTO — mediane che non fanno fallire
> l'identita' — lo stampa e dice che `K1` non prova niente.)*

**`K1` resta invariato come SOGLIA** (`< 1e-9`), **e ora ha senso.**