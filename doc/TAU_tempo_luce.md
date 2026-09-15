# `tau` deve essere il **TEMPO-LUCE `d/cs`**? — FASE 1, criterio scritto **PRIMA**

> **Scritto per Claude web** (regola §5-ter). Branch `fork-su2`, 2026-09-15. Blob **`f5887254`**.
> **Nessuna modifica alla fisica, nessun cablaggio.**
> **Stato: misura IN VOLO.** Questo documento contiene **solo** il criterio e il setup, committati
> **prima** dei dati. I numeri arriveranno in un commit dedicato.

---

## 1. DA DOVE VIENE LA DOMANDA

Il tracing (`doc/TRACING_omega.md`) si è chiuso con **ESITO (I), nessun bug**: la formula d'ingresso
è giusta, ma l'esponente si perde a valle.

```
|omega|_eq = sigma * sqrt(tau/(2 dt))
sigma = coppia/inerzia   pendenza  -1.056   (2781 nodi, r = -0.981)
tau                      pendenza  +1.812
attesa per theta: -1.056 + 1.812/2 = -0.150      misurato -0.113
```

> **Il `−1` della coppia è cancellato dal `+0.91` di `√tau`.** L'aliasing nasce dall'**interazione di
> DUE leggi**, ciascuna ragionevole da sola: `omega = coppia/inerzia` (riga **1918**) e
> `tau = TAU_A·max(dens/dens_rif, 0.05)` (riga **1913**).

## 2. LE DUE RIGHE NON SONO PARI — e la seconda ha già un precedente misurato

**Riga 1918 — non si tocca.** È la meccanica rotazionale standard (`dω/dt = τ/I`), ed è
**dimensionalmente coerente** con la lettura già confermata `inerzia = T²`
(`doc/INERZIA_tempo_quadro.md`).

**Riga 1913 — sospetta, e non per gusto.** Due fatti **misurati**, non opinioni:
1. **non fa quello che dichiara.** È scritta come `tau ∝ dens`, ma misurata dà **`rho^1.81`**
   (e per via indiretta `+1.867`): due strade indipendenti, stesso scarto dall'unità;
2. **il perché è strutturale:** `dens_rif` è la **MEDIANA**, quindi per il nodo mediano
   `dens/dens_rif ≈ 1` **sempre**, a qualunque maturazione — `tau` del nodo tipico è **ancorato a
   `TAU_A` per costruzione** (`CLAUDE.md` §9, rilievo di Luca). È un **punto fisso
   auto-normalizzante**, non un transitorio.

> Una riga che **non fa quello che dichiara** è esattamente la categoria che questo repo ha già
> pagato tre volte in due giorni (riga 2196; «`omega_s` conservativo»; «il calcio alimenta ogni
> passo»).

## 3. L'INCOERENZA DA SANARE, e il candidato **imposto**

> Se `inerzia = T² = (d/cs)²`, allora **il tempo che COSTRUISCE l'inerzia e il tempo che la RILASSA
> devono essere lo stesso.** Oggi ce ne sono **due diversi nella stessa equazione**: `(d/cs)²` al
> numeratore e la **densità** nel rilassamento.

Il candidato è `tau = d/cs`, e non è scelto:

| perché | |
|---|---|
| **causalità** | è il tempo perché l'informazione attraversi la regione: un sistema **non può ricordare più a lungo di quanto impieghi a sapere di sé** |
| **è già cablato** | è il `tau` dello **Strato 1** (`_bloch_ritardato`, `_nb_ret`), messo lì **per la stessa ragione** |
| **zero manopole** | `d` e `cs` esistono già (§3) |

**E il tracer usa la STESSA formula già nel file**, non una nuova: `d_nodo` = media degli archi
incidenti con fallback a `LAM` per i nodi isolati, `cs_nodo` dalla cache `_cs_nodo_prev`. Misurare
la proposta con una formula **diversa** da quella cablata sarebbe stato incoerente col suo stesso
argomento.

---

## 4. IL CRITERIO DI LETTURA — fissato PRIMA

La pendenza di `theta` è **prevedibile senza cablare nulla**:

> **pendenza(theta) = pendenza(sigma) + pendenza(tau)/2 = −1.056 + pendenza(d/cs)/2**

| misura | lettura |
|---|---|
| **\|pendenza(d/cs)\| ≤ 0.3** | `theta` tornerebbe a **≈ −1.0**: **la cancellazione si rompe**, la sostituzione risolve il problema di scala — **e lo si sa senza cablare** |
| **pendenza(d/cs) ≈ +1.8** (come l'attuale) | **non cambia nulla**: la sostituzione resta più coerente ma **NON risolve**. Va detto così, e **non venduto come cura** |
| valori intermedi | si riporta il numero e la pendenza attesa, **senza forzare** |

## 5. IL CAVEAT DI AMPIEZZA — da riportare **comunque**, anche se il criterio è favorevole

`tau` passa da `~44` unità di tempo (≈ 4425·`DT`) a `~d/cs` (≈ 0.25). Poiché
**`|omega|_eq ∝ √tau`**, il fattore è ~`√(0.25/44)` ≈ **1/13**.

> Da **112 giri/passo** si scenderebbe a **~9**. **Un ordine di grandezza nella direzione giusta,
> NON la soluzione dell'aliasing.** Questo va scritto **nella stessa riga** in cui si dà il numero,
> non in una nota a piè di pagina.

## 6. COSA QUESTA FASE NON FA

Non cabla niente. Non tocca la riga 1918, né `inerzia`, né la **forma** del termine dissipativo — e
in particolare **non** apre la questione se `−omega/tau` debba invece essere un termine di
allineamento LLG `−lambda·n×(n×B)`: è **separata e aperta**, e mescolarla renderebbe inattribuibile
qualunque risultato (§1, un interruttore alla volta).

Il cablaggio (flag `TAU_LUCE`, OFF di default, sigilli T1-T4) parte **solo** dopo il via libera di
Luca e **solo** se la FASE 1 è coerente.
