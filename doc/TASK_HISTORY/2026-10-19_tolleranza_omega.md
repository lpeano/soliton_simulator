# LA TOLLERANZA DEL PUNTO FISSO DI `Omega`: LA SCALA DEI DATI, NON `|Omega|`

> **Il mandato:** decisione di Luca del `2026-10-19` alle `16:29` sullo STOP di `D4`
> *(`7d061581`)*, strada `(1)`: ### **i `10` bracci «non converge» di `Omega` sono un
> FALSO** -- lo scarto e' fermo al rumore d'arrotondamento, e la soglia chiede una precisione
> piu' fine dello zero macchina dei dati.
> **Il fatto del guardiano** *(rapporto `1`, `dtau 0.5`, `x 0.01`)*: scarto FERMO a
> `1.7e-16`, `max|Omega| = 1.8e-2`, soglia `8 eps * 1.8e-2 = 3.2e-17`; i due termini di
> `Omega` valgono `1.4e-2` *(nodo)* e `3.9e-3` *(arco)*, ### **dello stesso ordine del
> risultato** -- ### **la mia lettura di `a59994b9` («differenza di termini di ordine 1») NON
> regge, e la ritiro qui.** ### **Il rumore viene dalle energie di `H`**, che sono costruite
> da `phi` e `psi` con norme di ordine `Lambda ~ 4`. ### **I numeri li riproduco io, con uno
> script.**

**LIVELLO CORRENTE:** `L2`, la cura del criterio d'arresto di un punto fisso del passo, prima
di rifare `D4`.

## 0. LA STELLA POLARE

1. **`A14`:** ### **la fase resta PURA** *(`|phi|` di ogni estremita' e' conservato al bit
   qualunque `Omega` si usi)*, quindi le norme `M` e `V` non cambiano; l'energia resta
   conservata al **secondo ordine** come prima: cambia solo ### **dove si ferma il punto
   fisso**, entro `8` ulp della scala dei dati.
2. **Il gradino:** `(a)` il controllo positivo sui bracci di `D4`, i due casi sintetici e il
   braccio reale che deve alzare, il braccio `0` al bit; `(b)` e `(c)`: ### **non si
   applicano** -- non si afferma un fenomeno, si cura un criterio d'arresto.
3. **Aggiunge un numero o una legge?** ### **Nessuno dei due:** `EPS_OMEGA` resta `8 eps`, e
   la scala ### **si deriva dai dati** *(`A1`)*. ### **E' la cura di un FALSO non-converge**,
   non una toppa: la soglia di prima chiedeva **meno dello zero macchina** dei dati.
4. **Tocca `rho`, `c_s` o il segno?** ### **Li LEGGE per la scala** *(`cs'`, `Lambda`,
   `rho`)*; ### **nessun verso dell'accoppiamento cambia.**
5. **Emergente o imposto?** ### **Non si applica**: nessun fenomeno.

## 1. LA SCALA, DICHIARATA PRIMA

### **Che cosa entra in `H`, letto in `energia_pesata.termini_di_h`:** il termine di NODO
`-pi [(rho - pu_psi) + (Lambda - pu_phi)] + eps h + N`, cioe' ### **differenze fra grandezze
dell'ordine di `rho` e di `Lambda`** *(con `|h| <= rho` e `|N| <= Lambda`)*; il termine
d'ARCO `-pi (arco_psi + arco_phi)`, costruito dalle norme di `psi` e `phi` sull'arco.
### **La materia entra con la STESSA forma del vuoto**, quindi -- come il mandato prevede --
### **la scala si prende sui termini che entrano davvero:**

```
scala = max_k  |cs'_k| * OMEGA_H * (Lambda_k + rho_k)        OMEGA_H = pi
converge  <=>  scarto <= EPS_OMEGA * scala                   EPS_OMEGA = 8 eps, INVARIATO
```

### ⚠ **Il fattore `OMEGA_H = pi` c'e' perche' i termini lo portano** *(sono `pi` volte le
norme)*: e' ### **la grandezza di cio' che si cancella**, non un margine. ### ⚠ **E la
scala e' COSTANTE dentro `applica`**: la fase non cambia ne' `Lambda` ne' `rho`, quindi si
calcola ### **una volta**, ### **dai buffer del pezzo e non da `st`** *(cosi' non si scrive
niente nello stato)*. ### **Il criterio diventa UNA FUNZIONE** *(`entro_tolleranza`)*, per
poterlo collaudare.
### 📌 **La tolleranza di `cs_al_centro` NON si tocca:** `cs` sta in `(0, 1)`, e' di ordine
`1`, e si calcola ### **direttamente da `Lambda` senza cancellazioni** -- quindi il rumore e'
di qualche ulp di `max|cs|`, e la soglia relativa a `max|cs|` ### **e' gia' sulla scala dei
dati.** ### **Il ciclo di periodo `2` di stamattina** *(`|x_n - x_{n-1}| = 6.2e-2`)* ### **e'
una non convergenza VERA, non rumore.**

## 2. LE PROVE, E COSA FERMA CIASCUNA

| | la prova | il criterio | cosa mi FERMA |
|---|---|---|---|
| `P1` | ### **il fatto del guardiano, riprodotto** *(rapporto `1`, `dtau 0.5`, `x 0.01`)* | i MIEI numeri: lo scarto di stagnazione, `max|Omega|`, i termini di nodo e d'arco, la scala vecchia e la nuova | -- |
| `P2` | ### **IL CONTROLLO POSITIVO, che puo' fallire:** `6` bracci di `D4` *(`x 0.01` e `x 1`, ai tre rapporti, `dtau 0.5`, i primi `20` tick)*: per ogni applicazione il punto fisso si itera ### **fino a `GIRI_MAX_OMEGA`** *(una copia DICHIARATA del corpo del ciclo, che non si ferma)*, e lo scarto di STAGNAZIONE e' ### **la mediana degli ultimi `10`** | ### **`stagnazione / scala <= 8` ulp in TUTTE le applicazioni dei `6` bracci** | ### **un braccio oltre `8` ulp: la scala e' sbagliata -- STOP** |
| `P3` | ### **IL CASO CHE DEVE FALLIRE, sintetico** | `(i)` uno scarto che si ferma al rumore della scala ### **converge**; `(ii)` un ciclo di periodo `2` di ampiezza `1e-6` sulla stessa scala ### **ALZA** | uno dei due sbagliato: STOP |
| `P4` | ### **IL CASO CHE DEVE FALLIRE, reale:** `applica` con una frazione `16` *(`tau = 8` a `dtau 0.5`)*, dichiarata qui, sullo stato del grumo a `x = 1` | ### **ALZA** | se converge: STOP |
| `P5` | ### **il braccio `0`, `cs` SPENTO:** `M-B1 --contro` il commit prima del codice, due scene | ### **AL BIT**, distanza del passo intero `0` | un bit: STOP |
| `P6` | ### **il braccio `0`, `cs` ACCESO:** sulla scena di `C1` *(strada `(d)`, `dtau 0.25`)*, per `32` tick, ### **un tick dal MEDESIMO stato** col codice di prima e con quello nuovo | ### **`max|delta phi|` per tick `<= n_app * tau * max|phi| * EPS_OMEGA * scala`** *(`n_app` le applicazioni di `applica` nel tick, contate)* | oltre: STOP |
| `P7` | ### **`C1` rifatto** | ### **`2.091`** con le sue cifre, e `0.044`, `0.012` | un numero diverso: STOP |

## 3. TODO

1. il codice *(`energia_pesata`: `scala_omega`, `entro_tolleranza`, `applica`)*, un commit.
2. `csv/_tolleranza_omega.py` *(`P1`-`P4`, `P6`)*, un commit; la corsa e il referto.
3. `M-B1` *(`P5`)* e `C1` *(`P7`)*, dal blob committato.
4. `D4` rifatto intero *(`LINEARE` riportato e SOSPESO)*; l'errore `n.16` nella relazione, e
   ### **la verifica con uno script degli `R` contro l'algebra esatta della forma.**
