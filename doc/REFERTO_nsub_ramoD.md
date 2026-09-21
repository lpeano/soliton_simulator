# REFERTO — **il ramo D diverge: `nsub = 22591`, e il vincolo vincente e' `n1` (la SORGENTE)**

> **EPOCA 2.** Ramo D, secondo lancio, tutte e tre le modifiche attive *(`CHI_COOP`, `SCALA_MIN`,
> `COES_ADIM`)* piu' la cura del mondo-dopo-i-flag. Simulatore **`4954fe5b`** *(sha1 byte grezzi)*.
> **Processo NON ucciso.** Cattura con `py-spy dump --locals` sul `PID 19912`.
> **⚠ NESSUN CONFRONTO CON A, B o C come metro:** i numeri di B compaiono solo per dire che **la
> FIRMA e' la stessa**, non per misurare D contro di lui.

---

## 1. IL NUMERO

```
nsub = 22591        n1 = 22591        n2 = 1        n3 = 3
```
**Contro il pavimento `nsub = 4`** che il codice impone come minimo (`:4267`,
`nsub = int(max(4, n1, n2, n3))`).

**Dove si trovava:** `_smorza` (`:3290`) chiamato da `step` (`:4288`), `quale = "d"` — cioe' dentro
il **sotto-passo del Verlet**, che gira `nsub` volte per ogni passo.

**Il processo NON e' piantato: sta calcolando.** Misurato: **`8.4 s` di CPU in `12 s` reali**.
**E' lento, non morto** — e la distinzione conta, perche' un processo fermo si diagnostica
diversamente da uno che macina.

---

## 2. ⚠ IL VINCOLO VINCENTE E' `n1`, LA SORGENTE — non `n3`

| vincolo | da cosa nasce | valore |
|---|---|---|
| **`n1`** | **`|src|`, il termine SORGENTE** | **22591** |
| `n2` | `beta` | 1 |
| `n3` | `|vd|` | 3 |

> **Non e' la velocita' dei legami a esplodere: `n3` vale TRE.** **E' la SORGENTE.**
> `src` e' il termine con **`peq` al denominatore** (`anom = (rho - peq)/max(peq, 1e-9)`), ed e'
> esattamente il difetto che il mandato dell'epoca elencava fra quelli **«NON toccati: ATTIVI»**.

---

## 3. LA FIRMA E' LA STESSA DEL RAMO B, E QUESTO E' IL PUNTO

```
ramo B (20/9, EPOCA 1)   nsub 206 -> 15594    n3 fermo a 205, n1 esploso
ramo D (oggi, EPOCA 2)   nsub = 22591         n3 = 3,         n1 = 22591
```

**⚠ E NON E' UNA RIPETIZIONE:** nel ramo B `chi_basc` era **SPENTO**; qui e' **ACCESO**, con in
piu' le tre modifiche e la cura del mondo. **Lo stesso canale esplode in entrambe le
configurazioni.**

> **CONCLUSIONE, e si ferma dove finisce la prova: le tre modifiche NON toccano questo canale.**
> `SCALA_MIN` governa le lunghezze, `COES_ADIM` la coesione, `CHI_COOP` la carica. **Nessuna delle
> tre tocca `src`, ne' `peq`.** **Il difetto era gia' catalogato come ATTIVO, ed era previsto che
> lo restasse.**

---

## 4. COSA NON SO, e non lo invento

- **QUANDO e' esploso.** L'ultimo dato pulito e' **frame 185 a `20.537 s/frame`**; poi **18 minuti
  senza una riga di log**. Lo snapshot che daterebbe il salto e' quello a **passo 1200**, **che non
  e' ancora stato scritto**: l'ultimo su disco e' **passo 1080** *(9 snapshot, `12:34`)*;
- **se si stabilizza o continua a salire:** **un solo campione non e' una traiettoria;**
- **se `peq` sia degenere.** E' il sospetto naturale — `src ∝ 1/peq` — **ma NON l'ho misurato**, e
  scriverlo come causa sarebbe una congettura travestita da riscontro.

---

## 5. COSA SIGNIFICA PER IL RUN

**A `nsub = 22591` un frame costa circa `5000` volte il normale.** I **315 frame restanti** sono
**giorni**, non ore. **Il run non arrivera' ai 3000 passi**, e il criterio assoluto
*«arrivo ai 3000 passi: si' o no, e se no dove e perche'»* ha gia' la sua risposta: **NO, e il
dove e' fra il passo 1110 e ora.**

**I 9 snapshot gia' scritti (fino al passo 1080) sono la finestra in cui il sistema era sano**, ed
e' li' che si misura **quando** e **perche'** e' cambiato regime.

---

## 6. LE DUE STRADE, e la decisione e' di Luca

- **A — lasciarlo andare:** di fatto e' fermo. Non produce piu' snapshot in tempo utile;
- **B — fermarlo catturando tutto** *(`py-spy` gia' fatto, piu' i contatori)*, **e aprire il fronte
  su `n1`/`src`/`peq`.**

**Raccomandazione: B.** **Non perche' D abbia fallito** — le tre modifiche fanno cio' che
dichiarano, e i loro sigilli tengono — **ma perche' il run non puo' piu' rispondere alla domanda
per cui e' stato lanciato, e il canale che lo blocca e' un difetto NOTO e MAI CURATO.**

**⚠ IL PROCESSO NON E' STATO UCCISO.**
