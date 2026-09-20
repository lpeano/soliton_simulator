# TASK HISTORY — `scala_p`: il quarto punto fisso della stessa famiglia. Prima la misura

**Data** 2026-09-20 · **branch** `fork-su2` · **HEAD** `5d19737` · **blob** `0a488348`
(**sha1 dei BYTE GREZZI**, convenzione `_presidio` — il blob git dello stesso file e' `775ceab7`,
e **sono due numeri diversi per lo stesso file**: `CLAUDE.md` §5-quinquies) · albero **pulito** ·
**nessun processo in esecuzione**.

> **Nessun run finche' la cura non e' sigillata. NIENTE NUMERI SCELTI: la scala si DERIVA.**
> **Una correzione, un sigillo.** **In questo giro si tocca SOLO `scala_p`:** le altre tre anomalie
> (②③④) hanno il loro ordine, e `L_CONSERVA`, `median(|f|)` in `ritmo()` e `_dens_rif` **non si
> toccano**.

---

## 1. IL DIFETTO, e cos'e' esattamente

```python
:4396   phi_g, _, dpozzo = self.pozzo_grafo(I)
:4399   scala_p  = max(float(np.median(np.abs(dpozzo))), 1e-9)
:4401   ampiezza = np.tanh(np.abs(dpozzo) / scala_p)
:4425   r_rad = ampiezza
```

**`scala_p` e' la MEDIANA DI `|dpozzo|` STESSO** → **`median(ampiezza) = tanh(1) = 0.761594` PER
COSTRUZIONE**, qualunque cosa faccia il sistema. **E' `A3`**, ed e' **il quarto caso della stessa
famiglia** su questo repo: `median(|f|)` in `ritmo()` *(curato con `Z42`)*, `_dens_rif` in `_tau`,
`u_nodo`, **e questo, mai curato.**

**L'asimmetria e' il punto:** `r_rad` e' normalizzato sulla **propria mediana**, `t_tan` e' il
`tanh` di una grandezza **assoluta** *(`|tw|/PHI_CRIT`, con `PHI_CRIT = 2*pi` dichiarato)*. **Si
confronta una grandezza autonormalizzata con una che non lo e'.**

## 2. ⚠ LE MISURE CHE VENGONO PRIMA, e cosa decide ciascuna

**Tutte dagli snapshot gia' in archivio: `dpozzo` e `phi_g` si ricalcolano da `pozzo_grafo`, che e'
una lettura pura, e `tw` e' salvato. NESSUN RUN.**

| # | misura | cosa decide |
|---|---|---|
| **M1** | **`\|dpozzo\|`**: percentili e **traiettoria nel tempo** | l'ordine di grandezza della grandezza da normalizzare |
| **M2** | **`phi_g`**: percentili, e **quanto spesso e' VICINO A ZERO** | **E' IL CANDIDATO DENOMINATORE.** Se si annulla, servirebbe un pavimento — **cioe' un NUMERO, e `A1` lo vieta.** **Questa misura puo' far CADERE la via del §3** |
| **M3** | **`median(ampiezza)`**: vale davvero `0.761594`? | **si VERIFICA il punto fisso invece di dedurlo.** Se non vale `tanh(1)`, la mia algebra e' sbagliata e la cura cade |
| **M4** | **`sin2`**: percentili — **e' incollato?** | **e' la firma che il punto fisso MORDE.** Se `sin2` e' gia' largo, il difetto e' formale e va detto |

**⚠ `M3` e' un CONTROLLO SU ME STESSO:** ho dedotto `median(ampiezza) = tanh(1)` dall'algebra, **e
l'algebra letta e non misurata mi ha gia' ingannato oggi** *(l'anomalia ① del mandato precedente)*.
**Se `M3` non da' `0.761594`, mi fermo e riporto invece di curare.**

## 3. LA CURA PROPOSTA, e perche' le alternative sono peggiori

**`|dpozzo| / phi_g` LOCALE.** La ragione e' fisica: *quanto e' RIPIDO il pozzo dove sei, rispetto
a quanto e' PROFONDO*. **Gradiente relativo: adimensionale per costruzione, e LOCALE.**
**E' la stessa forma di `u_nodo = I / media_dei_vicini`, che `Z5` ha mostrato soddisfare `A2`.**

**⚠ UN DETTAGLIO CHE VA DECISO E DICHIARATO, non lasciato implicito:** `dpozzo` e' **per ARCO**
*(`phi_g[jj] - phi_g[ii]`)*, `phi_g` e' **per NODO**. Il denominatore d'arco sara'
**`0.5*(phi_g[ii] + phi_g[jj])`** — la stessa media d'arco che il codice usa gia' per `circ_arc`
(`:4424`). **Non e' una scelta libera: e' la convenzione gia' presente nella stessa funzione.**

**Le alternative, e perche' no:**
- **`mean` invece di `median`** *(la via di `cs_floor`)*: **resta una statistica GLOBALE — `A2`.**
  Li' la tensione e' dichiarata aperta; **qui si puo' fare meglio;**
- **normalizzare anche `t_tan` allo stesso modo:** toglie l'asimmetria **ma lascia `A3` su
  ENTRAMBI**. **Cura il sintomo.**

**⚠ E LA VIA PUO' CADERE:** se `M2` mostra che `phi_g` si annulla spesso, **un pavimento sarebbe un
numero scelto (`A1`)**. **In quel caso NON lo prendo: propongo un'altra scala derivata, oppure
dichiaro che la via cade.** **«Nessuna scala derivabile» e' un esito valido.**

## 4. I SIGILLI, quando si arrivera' alla cura
- **Y0** riferimento **`0a488348`** *(byte grezzi)*;
- **Y1 — riduzione al limite, BLOCCANTE:** forzando la scala nuova a `median(|dpozzo|)`,
  **BYTE-IDENTICO**. **Forma algebrica binariamente esatta** *(lezione `R1`: vinse
  `sqrt(I)*sqrt(1.0/scala)`, non `sqrt(I/scala)`)*;
- **Y2 — controllo positivo:** coi valori veri **DEVE** differire;
- **Y3 — IL PUNTO FISSO E' SCIOLTO:** **`median(ampiezza)` non deve piu' valere `0.761594`.**
  **Se vale ancora quello, ho solo cambiato la formula del punto fisso;**
- **Y4 — LA RIPARTIZIONE SI MUOVE:** `sin2` ai percentili prima e dopo;
- **Y5 — L'EFFETTO SU `L`:** il momento angolare netto. **Se la selezione veniva dal punto fisso,
  deve cambiare;**
- **Y6 — `ZETA_VIR` EREDITA:** usa lo stesso `sin2` → **effetto anche su `beta`;**
- **Y7 — stabilita':** no NaN/runaway, CFL < 1, `|nb| = 1`;
- **Y8 — si RIGIRANO tutti i sigilli del giro. Se uno si muove, e' un reperto.**

## 5. COSA MI FA FERMARE
- **`M3` che non da' `tanh(1)`** → **la mia algebra e' sbagliata: riporto, non curo;**
- **`M2` che mostra `phi_g` vicino a zero su una frazione non trascurabile** → **la via cade**, e
  lo dico invece di mettere un pavimento;
- **`Y1` non byte-identico** → **la forma algebrica non e' esatta: si riscrive, non si allenta la
  soglia;**
- **`Y3` che resta a `0.761594`** → **ho cambiato la formula, non sciolto il punto fisso.**

## 6. TODO DEL NEXT STEP
1. [fatto] blob/branch dal disco; righe verificate;
2. **lo strumento delle misure `M1`-`M4`**, committato **prima** di girarlo;
3. **le misure** → **riporto, e in particolare se `phi_g` si annulla** → **STOP.**
