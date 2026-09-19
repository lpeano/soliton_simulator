# REFERTO — **il run a 6000 passi si è FERMATO al passo 2700, e il processo è VIVO**

> **Per Claude web.** Dati grezzi: **`csv/_test_fork/_dump_2700.txt`** (238 righe, tutte le 113
> chiavi dello snapshot). Script: `csv/_test_fork/_dump_snapshot.py` (`043922cc`).
> **Nulla è stato toccato:** il processo gira ancora, gli snapshot sono in sola lettura, il driver
> resta `f14ea4bd` e il simulatore `7c4dec1d`.

---

## 1. IL FATTO

```
ultimo progresso scritto : frame 450, passo 2700, ore 16:35:05
ora                      : 18:43        -> FERMO DA 2h08
ritmo precedente         : 5 frame in 78 s  (15.6 s/frame, stabile per 450 frame)
processo                 : VIVO. 12015 s di CPU su 12060 di orologio = 99.6 %, SU UN SOLO CORE
```

**Non è morto e non è in attesa: sta calcolando.** E sta calcolando **da solo**, su un core, senza
scrivere nulla — né log, né CSV, né snapshot.

## 2. COSA HO ESCLUSO, MISURANDOLO

| ipotesi | misura | esito |
|---|---|---|
| memoria esaurita / swap | working set **287 MB**, RAM libera **11.5 GB** su 32 | **escluso** |
| disco pieno | **17 GB** liberi | **escluso** |
| esplosione del CFL | `_taup_cfl_max` = **0.5657** su sei snapshot, `_taup_cs_clamp = 0` | **escluso** |
| limite `MAX_NODI` | `MAX_NODI = 4000000`, siamo a **9511** = **0.24 %** | **escluso** |
| `NaN` / `inf` nello stato | **zero** su tutti gli array dello snapshot 2700 | **escluso** |
| degenerazione progressiva dei contatori | crescono **regolarmente** fino al 2700 | **escluso** |

> **Quindi qualcosa è cambiato DOPO il passo 2700**, dentro i frame 451-460, e lo stato salvato al
> 2700 **non è rotto**.

## 3. COSA STAVA DEGENERANDO — il trend negli ultimi 420 passi

```
passo   d0 MAX    d MAX    phivel MAX   r MIN       fr(r<1e-4)   eta MAX
2280     43.2      7.10       81.9      1.0e-05      0.0004       30.3
2400     53.2      7.07      101.6      1.8e-05      0.0016       32.7
2520    339.1     10.28      154.8      4.6e-06      0.0012       34.1
2640    129.8     17.02      224.5      1.3e-05      0.0022       35.7
2700    394.7     16.79      213.7      2.1e-06      0.0026       36.4
```

**Tre cose crescono insieme:** la lunghezza **a riposo** massima di un arco (`d0`) da `43` a `395`,
la lunghezza **effettiva** massima (`d`) che raddoppia, la velocità di fase massima (`phivel`) che
quasi triplica.

**E la degenerazione di `d0` non è un singolo outlier:**

```
p50 = 1.305      MAX = 394.7      MAX/p50 = 302
archi con d0 > 10 : 1227      > 50 : 108      > 100 : 30      > 200 : 6
arco peggiore: d0 = 394.65   d = 0.0899   ->   d/d0 = 2.3e-04
```

**Una molla che "vorrebbe" essere lunga 394 e si trova lunga 0.09.** Il rapporto `d/d0` è
`2.3 × 10⁻⁴` su quell'arco, e **1227 archi** stanno sopra dieci volte la mediana.

**Altre code lunghe nello stesso snapshot** *(colonna `MAX/p50`, e quanti superano `10 × p50`)*:

```
vd          MAX/p50 = 67        20019 archi sopra 10*p50
omega_s     MAX/p50 = 5.3e4      8720 nodi
psi_spin    MAX/p50 = 542        3848 nodi
rho_spin    MAX/p50 = 3.6e4      3100 nodi
```

## 4. UN DATO CHE RIGUARDA `Z9`, e non il blocco

```
_r_corrente   p50 = 1.003    p90 = p99 = p99.9 = MAX = 1.414213   ( = sqrt(2), IL TETTO di ritmo() )
eta           p50 = 10.66    p99 = 34.64    MAX = 36.37           ( TAU_A = 50 )
```

**Oltre il 10 % dei nodi è ESATTAMENTE al tetto del ritmo.** E il nodo più vecchio ha
`eta = 36.37` su `TAU_A = 50`, cioè **`ramp = 0.727`: al 73 % della maturazione**, a metà run.

> **Nessun nodo è ancora maturo** (`ramp = 1` richiede `eta = 50`), quindi **`fr(ramp > 0.9)` è
> ancora zero** — coerente con `Z49`. Ma il nodo più avanti è più vicino di quanto fosse mai stato.

**E il rischio scritto in `P3` si sta manifestando:** la frazione di nodi con `r < 1e-4` — quelli
che scendono verso il pavimento — è passata da `0.0004` a `0.0026`, **sei volte in 420 passi**.
Sono ancora lo `0.26 %`, ma è **il meccanismo che farebbe smettere di crescere `Z9-b`**.

## 5. LE MIE IPOTESI — **dichiarate come ipotesi, perché non le ho misurate**

**① Un ciclo che non converge.** Il consumo è **single-core al 100 %** con memoria **stabile**:
non è numpy vettoriale (userebbe più core), è **un loop Python**. Un rilassamento iterativo, o un
ciclo di sottopassi il cui numero dipende da una grandezza che è esplosa.
**Contro questa ipotesi:** il contatore del CFL è **fermo**, e quello sarebbe il candidato ovvio.

**② La degenerazione di `d0`.** Con `d0 = 394` e `d = 0.09`, una forza elastica proporzionale a
`(d − d0)` vale **centinaia**. Se qualche passo adattivo si accorcia in risposta, il numero di
sottopassi cresce. **Ma questo è esattamente ciò che il CFL dovrebbe registrare, e non lo
registra** — quindi o il meccanismo è un altro, o esiste un ciclo che il CFL non conta.

**③ Non lo so.** Ed è la risposta onesta: **nessuno dei numeri che ho misurato spiega un blocco di
due ore**. Tutti mostrano un sistema che **degenera progressivamente**, non che si ferma di colpo.

> **Quello che servirebbe è banale e non ce l'ho:** `py-spy dump --pid 28764` legge lo stack di un
> processo vivo **dall'esterno, senza toccarlo**, e direbbe **su quale riga** è fermo. Non è
> installato. Installarlo non tocca né il run né il repo.

## 6. COSA C'È DA SALVARE, E COSA SI PUÒ FARE

**L'archivio è intatto e completo fino al passo 2700:** **45 snapshot, 1.3 GB**, cadenza 60 passi,
nessun buco, nessun duplicato, blob `7c4dec1d` in tutti.

**Le misure del §3 del mandato si possono fare su quei 45 snapshot** — `Z9-b`, `ramp` per coorte,
`p95/p05`, le conseguenze, il ciclo — **senza rigirare niente**. È metà run, non zero.

**E la ripresa è sigillata `5/5`:** si può ripartire dal passo 2700 *(la ripresa sta sulla COPIA
del driver, `_scena_video_ripresa.py`; quella sul file in uso è stata ripristinata per non
cambiare il blob a metà run — e la scelta è dichiarata in `doc/STATO_RUN.md`)*.

## 7. LA DOMANDA CHE GIRO A CLAUDE WEB

**Il sistema stava degenerando o stava facendo qualcosa?** La dilatazione a `−13.25 %` in caduta
libera, la coerenza locale al **massimo del run** e ancora in salita, `d0` che esplode su oltre
mille archi: **non so se sia una patologia numerica o una transizione**.

**E la domanda operativa:** conviene riprendere da 2700, o le code lunghe di `d0` e `omega_s`
dicono che da lì in poi il run non è più interpretabile?

---

**LIMITI:** un seme, una scena, `--tau-luce` con sigillo **6/7**, `--chi-basc` che riscrive
`perc_chi`. Il run **non è finito** e queste sono misure **a metà**.
