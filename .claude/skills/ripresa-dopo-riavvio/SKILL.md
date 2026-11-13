---
name: ripresa-dopo-riavvio
description: Usare all'inizio di ogni sessione dopo un riavvio o una caduta: controllare lo stato del repo, del registro delle corse e dei file a meta' prima di fare qualunque altra cosa
---

# La ripresa dopo un riavvio

*(Luca, 2026-11-13 10:20. Il primo controllo fatto cosi': `9ad7489a`; il task history `doc/TASK_HISTORY/2026-11-13_registro_corse.md`, sez. 0.)*

**Prima di qualunque altra cosa, SOLO LETTURA.** Nessun rilancio, nessuna riparazione, nessun commit di lavoro finche' i passi qui sotto non sono fatti e scritti.

## I passi

1. **git** sul ramo `primo-ordine`:
   - `git status`, `git log -1`, `git fetch`, poi `git rev-parse HEAD origin/primo-ordine`: **l'atteso e' pulito e allineato a origin, sull'ultimo commit noto.**
   - **Un avviso del commit-graph** *(`unable to find all commit-graph files`)* **e' atteso dopo un riavvio forzato** *(Luca, 2026-11-13 11:50)*: **prima `git fsck --no-dangling`** *(solo lettura)*; **se e' pulito, `git commit-graph write --reachable`** *(non tocca i commit)* **e si verifica che l'avviso sparisca.** **Se `git fsck` trova errori: FERMO, nessuna riparazione da soli.**
2. **I file a meta'**, nella cartella del repo **e** in `E:\soliton_simulator`: npz parziali, temporanei *(`*.tmp`, `.registro_*.tmp`)*, lock.
   - `csv/_barriera.lock` e `primo_ordine/versioni.lock` sono **file TRACCIATI**, non lucchetti rimasti.
   - File con l'ora recente ma `git status` pulito: **gli hook li riscrivono identici**, non sono a meta'.
3. **Il registro delle corse:**
   ```
   python csv/solitone/_registro_corse.py aperte
   ```
   Per ogni voce APERTA: **il nome, il tipo, da quando, l'ultima tappa, il comando.**
4. **Gli orari dello scratchpad** *(`orari_prove.txt` e i file di orari accanto)*: l'ultima riga e la sua ora; **una corsa iniziata e non finita?**
5. **I processi del repo ancora vivi** *(`tasklist`, i `python`)*. ### **Mai uccidere processi che non sono miei.**
6. **La coda:** `doc/ROTTA.md`, la sezione **«La coda»**: **che cosa e' pronto, che cosa aspetta Luca.**

## La regola

### ⛔ **Se c'e' una voce APERTA nel registro o un file a meta': FERMO, e si chiede a Luca. Niente si rilancia da soli.**

- Una voce aperta dopo un riavvio **si chiude solo dopo che Luca l'ha vista** *(la skill `registro-corse`, regola 7)*.
- **I fatti si scrivono nella RELAZIONE** *(`RELAZIONE_PER_CLAUDE.md`)* **nello stesso giro**, e il messaggio a Luca finisce con `FERMO: <motivo>` o, se tutto e' pulito, si prosegue la coda.
