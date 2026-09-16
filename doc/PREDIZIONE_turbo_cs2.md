# PREDIZIONE — il TURBO come diagnostico del fattore `cs^-2`

> **Scritta e committata PRIMA dei run col turbo**, e **prima di aver letto la baseline**.
> 2026-09-16, blob **`c57800c1`** (verificato sui **byte grezzi**, non con `git hash-object`).
> Branch `fork-su2`. **Nessuna riga di `soliton_simulator.py` toccata da questo documento.**

---

## 0. LA DOMANDA — una sola, e non e' quella che il turbo ha gia' chiuso

Il 2026-09-16 e' stato cablato **`inerzia = max(rho * (CS_M/cs_nodo)^2, 1e-6)`**: il fattore
`cs^-2` che la derivazione `inerzia = (d/cs)^2` impone e che **mancava** (sigillo **M2** PASS,
byte-identico dove `cs = CS_M`; **M2b** PASS, col `cs` vivo morde).
**Ma il fattore e' quasi 1 ovunque**, perche' `cs_std/cs_medio` vale **0.033 %** a 150 passi.

> ### La domanda: **«il fattore `cs^-2` cambia qualcosa quando `cs` varia DAVVERO?»**
> **NON**: «cosa fa lo spin ad alta densita'». Quella e' un'altra domanda, e **non si risponde col
> turbo**.

**⚠ E QUESTO MANDATO NON RIAPRE B6.** Il turbo ha gia' un verdetto — **ESITO B**: *«con `cs` al
5 % di `CS_M` lo Step 2 non muove lo spin»* (`chi` ON **89.9865** / OFF **89.9941** contro il null
90.000; autocorrelazione piatta su 14 bin). **La sua condizione di riapertura e' `theta < ~1
giro/passo`, e NON e' soddisfatta** — nella baseline migliore `theta` sta a ~12-16 giri/passo.
**B6 resta chiusa.**

---

## 1. CATEGORIA — e cosa si puo' dire, e cosa no

Il turbo sta in **ESPERIMENTI, OFF per sempre** (`doc/COMPONENTI_PROMOSSE.md`): **amplifica un
parametro per rendere visibile un effetto**. Si usa **per VEDERE, non per CONCLUDERE**.

| | |
|---|---|
| **legittimo** | *«con `cs` amplificato il fattore morde e produce X»* |
| **NON legittimo** | *«quindi nel regime reale succede X»* |

**Questa riga va nel referto, non solo qui.**

---

## 2. LA STIMA, dai numeri sul disco

`cs_eff(rho) = CS_M / (1 + GAMMA*GAMMA_TURBO*sqrt(I))`, e il turbo moltiplica **solo** la
sensibilita' di `cs` a `rho` dentro `_cs_nodo` — **altrove `GAMMA` resta originale**.
Nel regime attuale `cs` sta in **`[1.9949, 2.0000]`** con `CS_M = 2`, cioe' lo scostamento
relativo massimo e' **`2.6e-3`** e `cs_std/cs = 0.033 %`.

Poiche' `1 - cs/CS_M ~ GAMMA*GAMMA_TURBO*sqrt(I)` per scostamenti piccoli, **lo scostamento scala
~linearmente con `GAMMA_TURBO`** finche' resta piccolo. Quindi, con `K = GAMMA_TURBO`:

| `K` | scostamento max atteso `1 - cs/CS_M` | fattore `(CS_M/cs)^2` atteso, max |
|---|---|---|
| 1 (baseline) | `2.6e-3` | **1.0051** |
| 10 | `~2.6e-2` | **~1.053** |
| 100 | `~0.26` **(non piu' lineare)** | **~1.8** |

> **Si useranno `K = 100`**, e la ragione e' che a `K = 10` il fattore arriva a ~1.05: uno scarto
> del 5 % e' ancora dentro il rumore delle traiettorie caotiche, e **l'esperimento sarebbe nullo
> per costruzione**. A `K = 100` la relazione **non e' piu' lineare** e la stima sopra **e' un
> ordine di grandezza, non una previsione**: va **misurata**, ed e' per questo che
> `fatt_cs_scarto_max` e `fatt_cs_frac_oltre_1pc` sono colonne del CSV.

---

## 3. IL NUMERO CHE DECIDE SE L'ESPERIMENTO E' INFORMATIVO

> ### **`fatt_cs_frac_oltre_1pc`** — la frazione di nodi in cui `(CS_M/cs)^2` si discosta da 1 di
> piu' dell'1 %.
> **Nella baseline vale `0.000`.** Se col turbo **resta ~0**, **il turbo non ha svegliato `cs`
> abbastanza e IL TEST E' NULLO.** Si dice, non si forza.

Accanto vanno letti `fatt_cs_mediana`, `fatt_cs_max` e `fatt_cs_scarto_max`.

---

## 4. ⚠ COSA NON DEVE SUCCEDERE — il controllo che distingue l'effetto dall'artefatto

> **Se `chi`, `|<n>|` o l'autocorrelazione si muovono MENTRE il fattore resta ~1, l'effetto NON e'
> del fattore: e' un artefatto del turbo.**
> **Il turbo amplifica anche gli artefatti** — cambia `cs`, e `cs` entra nel CFL
> (`beta = 2*zeta*cs/d`, `n2 = ceil(max(beta)*DT/0.2)`), nella metrica e nel tempo-luce dello
> Strato 1. **Non e' un interruttore che tocca solo l'inerzia.**

**E' il controllo piu' importante di tutto il documento**, perche' e' l'unico modo di non
attribuire al pezzo nuovo un effetto che viene da tutto il resto.

---

## 5. LE TRE LETTURE, fissate ORA

1. **Il fattore si discosta da 1 in modo netto** (`frac_oltre_1pc` sensibilmente > 0) **E `L_tot`
   cambia comportamento alle mitosi** (`L_dL_con_mitosi_mediana` si muove rispetto alla baseline,
   contro la dispersione FRA SEMI) -> **il fattore `cs^-2` fa il lavoro di conservazione per cui e'
   stato messo.** Risultato utile, e **da dire solo del regime col turbo**.
2. **Il fattore si discosta ma `L_tot` non cambia** -> il fattore e' **cablato correttamente ma
   senza conseguenze dinamiche**. **E' un'informazione, non una delusione**: significa che la
   violazione del ~3.4 % per passo (**C20**) ha un'altra causa.
3. **Il fattore resta ~1** -> **il turbo non basta a svegliare `cs`**: **esperimento NULLO**, e la
   domanda resta aperta per un regime a **densita' vera**.

**In tutti e tre i casi la barra e' la dispersione FRA SEMI** (P3/C10: su questo sistema la
pendenza cambia di **0.03** a codice invariato), **mai la `SE` interna a un run**. Con 2 semi
`t(0.025,1) = 12.706`, quindi **un IC95 a 2 semi non decide**: si potra' dire il **segno** e
l'**ordine di grandezza**, non stabilire un effetto.

---

## 6. CONFIG — identica alla baseline tranne un interruttore

```
--batch --nmasse 3 --sep 8 --passi 500 --ogni 50
--campo-spinoriale --spinore-vivo --spinore-corretto --chi-core
--calore-scal --deparam-orologio --verlet
--fork-su2 --fork-su2-mem
--cs-dinamico                    <- OBBLIGATORIO: senza, il turbo e' IGNORATO (:5081, verificato)
--tau-luce                       <- il braccio a risoluzione migliore
--gamma-turbo 100                <- L'UNICO interruttore che cambia
```
**Due run, semi 1 e 2.** **SPENTI:** `--kuramoto-su2`, `--step2-orologio`, `--sync`, `--regime`.

**Checklist P6 dai DATI:** `BLOB = c57800c1`, `CS_DINAMICO = 1`, `cs_std != nan`, `TAU_LUCE = 1`,
`KURAMOTO_SU2 = 0`, `STEP2 = 0`, **`GAMMA_TURBO = 100.0`**, `SEME = 1, 2`.
**Un campo che non combacia: quel run non conta.**

---

## 7. E COSA QUESTO ESPERIMENTO NON POTRA' DIRE, in nessun caso

- **nulla sul regime reale** (categoria ESPERIMENTI);
- **nulla su B6**, che resta chiusa con la sua condizione di riapertura non soddisfatta;
- **nulla su «lo spin si organizza»**: `theta` restera' ben oltre il giro per passo, e ogni esito
  negativo li' e' quello che l'**aliasing** produrrebbe da solo (**C14**);
- e **nulla sulla violazione di `L_tot`** nel regime vero: se il fattore la muovesse col turbo,
  direbbe che **il canale esiste**, non che sia **aperto** a densita' simulabili.
