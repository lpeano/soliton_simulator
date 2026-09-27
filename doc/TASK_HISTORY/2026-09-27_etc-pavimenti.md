# `ETC-PASSO` — **gli 8 pavimenti sono MORTI col driver. Verifica a runtime** *(2026-09-27)*

> **Mandato di Luca su `533f54f`:** *«PRIMA di tutto, VERIFICA A RUNTIME con l'argv del driver
> quali degli 8 siti girano davvero. […] Se sono TUTTI MORTI col driver: si archiviano con la
> cura, nessuna decisione di teoria ora. Se anche UNO è vivo: FERMATI e dimmi quale.»*
>
> ### ✅ **VERDETTO: TUTTI E 8 MORTI.** Nessuna decisione di teoria serve ora.
> ### 🛑 **Blob del simulatore `e203f9a8` PRIMA e DOPO.** Nessun codice del simulatore è cambiato.

**Lo strumento:** `csv/_test_fork/_etc_pavimenti.py` *(blob sha1-BYTE `04a6ec32`)*, referto
`_etc_pavimenti.json` *(`7c464c26`)*.

---

# 1. COME LO PROVA — e non si fida di un'inferenza sui flag

| | |
|---|---|
| **① COPERTURA DI RIGA** | `sys.settrace` ristretto a `soliton_simulator.py`: si registra **quali righe hanno ESEGUITO**. **Una riga che non compare non è girata.** È la prova **diretta** |
| **② I CONTATORI già cablati** | `_g_sm_pav_saltati`, `_g_smp_passanti`, `_g_smp_aperture`, `_g_smp_chiusure`, …: corroborazione **indipendente** dalla copertura |
| **③ L'ARGV DEL DRIVER, non ricostruito** | `_cli_flag.argv_del_driver` **esegue il testo del driver** fino all'ancora e restituisce la `sys.argv` che **il driver** ha costruito |

**Condizioni:** scena `(ii)(a)`, seme `11`, **`n = 2107` nodi, `m = 70199` archi**, **3 passi
pieni**. I flag letti **dal modulo configurato dal driver**:

| flag | |
|---|---|
| `SCALA_MIN_PASSO` | ### **ACCESO** |
| `VERLET` | ### **ACCESO** → **l'integratore vivo è VERLET**, il sottociclo a salto della rana |
| `SEMINA_LAM` · `MITOSI_2LAM` · `POZZO_D` | ACCESI |
| `SCALA_MIN` · `PAV_COM` | spenti |

---

# 2. LA COPERTURA, riga per riga

| riga | **girata?** | esec. | che cos'è |
|---|---|---|---|
| `:4453` | **SÌ** | **15** | `_pav_d0`: il ramo **INERTE** — `if SCALA_MIN or SCALA_MIN_PASSO: return v` |
| ### `:4456` | ### **NO** | ### **0** | ### `_pav_d0`: **IL PAVIMENTO** `np.maximum(v, self._floor_d0())` |
| `:5733` | **SÌ** | **12** | Verlet: `d_new = self.d + dts*vd_half` — **senza pavimento** |
| ### `:5737` | ### **NO** | ### **0** | ### Verlet: **IL PAVIMENTO** `np.maximum(…, 0.05)` |
| `:5778` | **NO** | 0 | Eulero: il ramo `SCALA_MIN_PASSO` — **l'integratore Eulero non gira affatto** |
| ### `:5782` | ### **NO** | ### **0** | ### Eulero: **IL PAVIMENTO** `np.maximum(…, 0.05)` |
| `:5789` | **SÌ** | **3** | **il FRENO di scala minima**, una volta sola dopo i sotto-passi |

## ⚠ **E la prova è più forte della copertura: `:4456` è un COLLO DI BOTTIGLIA UNICO**

I 7 siti che chiamano `_pav_d0` *(`:5899` `:6157` `:6664` `:6817` `:6840` `:6994` `:7042`)* sono
stati tracciati uno per uno: **5 sono stati chiamati** *(3 volte ciascuno = 15)*, **2 no**
*(`:6157` in `mitosi` e `:6840`, che in 3 passi non sono entrati nel loro ramo)*.

> ### **Ma questo NON indebolisce il verdetto, lo rafforza:** tutte e sette le chiamate passano
> **per la stessa funzione**, e **l'unica riga che applica il pavimento è `:4456`**, che ha
> eseguito **zero volte**. **Quindi anche i due siti non raggiunti non potrebbero applicare il
> pavimento**, perché l'unica strada per farlo non è mai stata percorsa.
>
> **E i contatori lo confermano da fuori:** `_g_sm_pav_saltati = 15` **coincide esattamente** con
> le 15 chiamate tracciate — **ogni** chiamata a `_pav_d0` è uscita dal ramo inerte.

## E `:5782` è **doppiamente** morto

**Due ragioni indipendenti**, e basta una sola: ① è il ramo `else` di `SCALA_MIN_PASSO`, che è
**acceso**; ② sta nell'**integratore Eulero**, e il driver passa `--verlet` — infatti anche
`:5778`, che è il ramo *vivo* di Eulero, ha eseguito **0** volte.

---

# 3. IL PUNTO 2 DEL MANDATO: **il freno è GIÀ «una volta per passo pieno»**

> **Luca chiedeva:** *«Verifica che il freno oggi sia già "una volta per passo pieno"
> (`_smp_apri` / `C3`) e dichiara come si compone con la fotografia.»*

### ✅ **Sì, ed è già letteralmente il meccanismo della cura.**

| contatore | misurato su 3 passi | |
|---|---|---|
| `_g_smp_aperture` *(`_smp_apri`)* | ### **3** | **una apertura per passo pieno** |
| `_g_smp_chiusure` *(il freno su `d0`)* | ### **3** | **una chiusura per passo pieno** |
| `_g_smp_d_chiusure` *(il freno su `d`)* | ### **3** | idem |
| `_g_smp_disallineati` | ### **0** | nessun confronto fra lunghezze diverse |
| `_g_smp_d_nsub` | **4** | i sotto-passi metrici nel passo peggiore: **prima il freno girava 4 volte, ora 1** |

## 3.1 — **Come si compone con la fotografia: coincide, e su `d`/`d0` è GIÀ FATTA**

| | il meccanismo di oggi | la cura |
|---|---|---|
| **apertura** | `_smp_apri()` fotografa **`d` E `d0`** a inizio `step` | la fotografia **unica**, a inizio `passo_pieno` |
| **durante** | le leggi scrivono; `_sd0` **lascia passare** la variazione senza frenarla *(`_g_smp_passanti = 15`)* | le leggi producono **variazioni** sulla fotografia |
| **chirurgia** | `_smp_chirurgia` fa subire allo snapshot **le stesse operazioni della mitosi** — `[keep]`, code nuove | è **esattamente** l'estensione della fotografia ai nati |
| **chiusura** | `d0 ← inizio + _smorza(inizio, fine − inizio)`, dentro `memoria_hebbiana_moto` *(l'ULTIMA legge)* | ### **il freno UNA VOLTA sulla variazione TOTALE, al commit** |

> ### 📌 **Quindi per `d` e `d0` la cura non inventa niente: ESTENDE `C3` alle altre 19 grandezze.**
> Il docstring di `_smp_chiudi` dice già la cosa che conta: *«Con spinte opposte di somma nulla
> `dx = 0`, che NON è una discesa: il valore resta intatto, e il bias è zero esatto. **Non
> contiene l'ordine delle leggi.**»* — **è la definizione di Jacobi**, scritta due settimane fa
> per due array su ventuno.

## 3.2 — ⚠ **Due scostamenti da correggere nella FASE 1, e li dichiaro ORA**

1. ### **L'apertura è in ritardo di una legge.** `_smp_apri()` è chiamata a `:5106`, cioè
   **all'inizio di `step`**, non di `passo_pieno`. **`scuoti_vuoto` gira PRIMA** — oggi è
   innocuo *(tocca `phivel`, non `d`/`d0`)*, **ma la fotografia della cura deve aprirsi prima
   della prima legge**, non della seconda.
2. ### **La chiusura è DENTRO l'ultima legge**, non dopo di essa *(`:6604`, `:7046` in
   `memoria_hebbiana_moto`)*. Funziona perché quella legge è l'ultima, **ma è una coincidenza
   d'ordine**: se l'ordine cambiasse, il freno chiuderebbe troppo presto. **`H-ETC-2` permuta
   l'ordine: questo va spostato, o il presidio fallirebbe per il motivo sbagliato.**

---

# 4. ⚠ **IL LIMITE DI QUESTA VERIFICA, dichiarato** (`A9`)

| | |
|---|---|
| **la copertura prova ciò che è girato IN QUESTA esecuzione** | 3 passi, `n = 2107`, seme 11. Un ramo che scattasse solo in un regime raro **non si vedrebbe** |
| ### **`_g_smp_chirurgie = 0`** | **in 3 passi nessuna mitosi ha diviso un arco**, quindi **il percorso della chirurgia sullo snapshot NON è stato esercitato**. È il percorso più delicato di `C3`, e **questa verifica non lo copre** |
| il collo di bottiglia | l'argomento di `:4456` **non** dipende dall'esecuzione: è strutturale, e tiene comunque |

---

# 5. LE DECISIONI REGISTRATE, e che cosa cambia nel progetto

| | decisione di Luca | effetto |
|---|---|---|
| **gruppo ① — 8 pavimenti** | *«se tutti morti: si archiviano con la cura»* | ### **si ARCHIVIANO**, restano censiti in `CLIP-INVENTARIO`. **Il bivio di teoria del par.1.3 della FASE 0-bis è SCIOLTO senza deciderlo** |
| **gruppo ② — `phi` ×4, `_nb` ×1** | ### **APPROVATA** la raccomandazione: **una volta sola a fine passo** | e *«l'avvolgimento è il DOMINIO della doppia copertura (4π), non un clip»* — **quindi non è un vincolo, è lo spazio di stato** |
| **scala minima** | il freno di `SCALA_MIN_PASSO` **una volta sola sulla variazione totale**, al commit | **già così per `d`/`d0`**; si estende alle altre 19 |
| **flussi casuali per legge** | ### **APPROVATI**, *«sapendo che cambiano i numeri anche a parità di fisica»* | **va dichiarato nel sigillo** |
| **`D31`** *(il freno è solo in discesa)* | **resta aperta**, è della cura **(d)** | **qui non si tocca** |

---

# TODO DEL NEXT STEP — **FASE 1, passo (a): I PRESIDI**

> ### 🛑 **Un commit per passo, STOP dopo ognuno.** Questo commit è la verifica che il mandato
> chiedeva *«PRIMA di tutto»*. Il prossimo è **(a) i presidi**, e nient'altro.

1. **`H-ETC-2` per primo e da solo**, coi flussi casuali per legge. ### **Deve FALLIRE sul blob
   `e203f9a8`. Se passa, mi fermo e non lo consegno.**
   ⚠ **E va cablato tenendo conto del par.3.2 ②:** la chiusura del freno è **dentro** l'ultima
   legge, quindi una permutazione la sposta. **O si sposta la chiusura, o il presidio misura la
   cosa sbagliata.**
2. **`H-ETC-1`**, con l'attesa **`= 8`** sul blob di oggi.
3. **Poi (b) archiviazione, (c) la cura, (d) il sigillo.**

## LE VOCI D'INDICE CHE QUESTO DOCUMENTO TOCCA

`ETC-PASSO` · `CLIP-INVENTARIO` · `H-ETC-1` · `H-ETC-2` · `D31` · `A9`
