# TASK HISTORY — **il ragionamento si scrive PRIMA, e si committa PRIMA**

> **Regola di Luca, 2026-09-18** (`CLAUDE.md` par.5-septies). **Non è documentazione: è un
> prerequisito del lavoro.**

## Perché esiste

In questo repo il ragionamento è già stato la parte più preziosa più di una volta — **e più volte
quella che stava per andare persa**:

- la strada **scartata** era più informativa di quella presa (le quattro varianti del denominatore,
  le **due** rotture del punto 1 di `Z24`, i tre nulli letti con risoluzioni diverse);
- un riavvio del PC ha cancellato lo scratchpad e con esso il termine di paragone di **quattro
  sigilli** (`Z31`);
- e quattro **errori di popolazione in due giorni** sono stati trovati **rileggendo il proprio
  ragionamento**, non i risultati.

**Un ragionamento scritto DOPO è una ricostruzione.** Scritto **prima**, è un impegno: si può
confrontare con ciò che è successo, e **può risultare sbagliato** — che è l'unica cosa che lo rende
utile. *(È la stessa ragione per cui le previsioni sono ex ante e i criteri dei sigilli si scrivono
prima di girarli: dodici criteri scaduti in questo repo lo hanno insegnato a caro prezzo.)*

## La struttura — tre sezioni, in quest'ordine

```
doc/TASK_HISTORY/<AAAA-MM-GG>_<slug>.md
```

1. **RAGIONAMENTO PRELIMINARE** — *cosa credo prima di guardare.* Le premesse, cosa mi aspetto, e
   **cosa NON so**. Va scritto **prima di misurare**, e resta anche quando si rivela sbagliato:
   **non si riscrive, si annota** con ciò che l'ha smentito.
2. **PROGETTAZIONE DEL RAGIONAMENTO** — *come intendo arrivarci.* I passi, **cosa deciderebbe
   ciascuno**, e **cosa mi farebbe fermare**. È qui che si fissano le letture **prima** di vedere i
   numeri.
3. **TODO DEL NEXT STEP** — *cosa resta da fare, esplicito.* Non un riassunto: **la lista operativa
   del passo successivo**, con lo stato di ciascuna voce.

## Il rito

**Il task history si committa e si pusha PRIMA di fare il lavoro**, non insieme e non dopo.
**Così l'ordine è verificabile da git**, non asserito: il commit del task history dev'essere
**antenato** dei commit del lavoro che descrive. È la stessa logica di par.5 (*«il codice che genera
un output dev'essere già committato quando l'output nasce»*) applicata al **pensiero** invece che al
codice.

**E la sezione 3 si aggiorna a ogni passo**, nello stesso commit del riscontro che la cambia
(par.5-bis): un TODO aggiornato «dopo» è un TODO falso.

## Come si verifica che la regola sia stata seguita

```bash
# il task history deve precedere il lavoro che descrive
git log --oneline --reverse -- doc/TASK_HISTORY/<file>.md | head -1     # il commit del PRIMA
git merge-base --is-ancestor <quel commit> HEAD && echo "ordine rispettato"
```

**Dichiarazione onesta:** questo è un **controllo**, non un **impedimento**. Non impedisce di
scrivere il task history dopo e antidatarlo nel testo — **impedisce di farlo senza che git lo
mostri**. Per Regola 9 è meno di un meccanismo e più di una nota, e **va detto così** invece di
chiamarlo presidio.
