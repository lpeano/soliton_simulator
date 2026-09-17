# REFERTO — **`TAU_A = 2.0` nel deterministico: NON diverge. Ma «non esplode» non è «sta bene».**

**Blob:** `7dfd3e3` (flag `--tau-a`, OFF di default; **S3 byte-identico** verificato **prima** del
run). **ESPERIMENTO, non correzione.** **Nessuna promozione, nessun cambio di default**, `G_PH` e
`_CALORE_INIT` **non toccati**.

---

## 1. S1 — **STABILITÀ: 5/5 PASS. Non diverge.**

```
run TAU_A=50 : rc=0      run TAU_A=2.0 : rc=0
[PASS] S1a nessun NaN/inf                 NaN/inf totali: 0
[PASS] S1b |nb| = 1                       max| |nb|-1 | = 2.220e-16
[PASS] S1c d0 > 0 e d > 0                 min d0 0.05, min d 0.05
[PASS] S1d tau_p stabile                  _taup_cfl_max = 0.5627  (con TAU_A=50: 0.5644)
[PASS] S1e nessun runaway di omega_s      rapporto 2.686
```

> **La testimonianza NON è confermata nella sua forma letterale: con `TAU_A = 2.0` il sistema
> NON esplode.**

---

## 2. ⚠ MA I SEGNI DI STRESS SONO GROSSI, e il mandato chiede di non minimizzarli

| campo (max \|·\|) | `TAU_A = 50` | `TAU_A = 2.0` | rapporto |
|---|---|---|---|
| `psi` | 0.06412 | **5.834** | **× 91** |
| `d0` | 2.878 | **50.22** | **× 17.4** |
| `phivel` | 2.787 | **63.35** | **× 22.7** |
| `d` | 6.019 | **35.37** | × 5.9 |
| **nodi finali** | **2577** | **1754** | **−32 %** |

> **Il sistema non diverge, ma non è lo stesso sistema.** `psi` novantuno volte più grande, `d0`
> diciassette, `phivel` ventitré, **e un terzo dei nodi in meno.**
> **«Regge» qui significa soltanto «l'aritmetica non produce NaN».**

**E va detto con la qualifica giusta:** `TAU_A = 2.0` **con** `G_PH = 3e-3` **non è né il canonico**
(che vuole `G_PH = 0.15`) **né il deterministico originale**. **È una terza combinazione, che
nessuno ha validato** — ed è esattamente ciò che il mandato chiedeva di dichiarare.

---

## 3. S2 — **`Z9` sarebbe risolta, e non di poco**

```
TAU_A=50   ramp med 0.014754   p05 0.00024   p95 0.0282   ramp=1 al passo ~8133
TAU_A=2.0  ramp med 0.47044    p05 0.16568   p95 0.6433   ramp=1 al passo ~255
```

> **Il kernel arriverebbe a maturità DENTRO la durata dei run** (~255 passi contro 300-500), invece
> che a **~6000-8000**. **`ramp` mediano passa da 1.5 % a 47 %.**

**⚠ Nota sul confronto, per non fare quello scorretto:** il `~8133` qui è calcolato da
`eta_finale / 120`, mentre il **`~5960`** della rimisura (`e24840d`) usava `(eta₁₂₀ − eta₁)/119`.
**Due metodi diversi sullo stesso blob**, e la differenza è tutta lì. **Il numero confrontabile con
`Z9` resta `~5960`; il `~8133` va usato solo contro il `~255` della stessa tabella.**

---

## 4. IL VERDETTO — **la TERZA lettura, fissata prima**

> *«REGGE ma con segni di stress → riportali senza minimizzarli. "Non esplode" non è "sta bene".»*

**È questa.** E le conseguenze sono due, opposte, e vanno tenute insieme:

1. **La compensazione sembra scaduta nel senso stretto:** il sistema non diverge più con
   `TAU_A = 2.0`. *(Plausibile che dipenda dalle correzioni di questo giro — in particolare
   l'inerzia, che non è più il pavimento `1e-6` — ma **non l'ho misurato**, e non lo affermo.)*
2. **Ma il prezzo non è un dettaglio:** `psi` × 91, `d0` × 17, `phivel` × 23, **un terzo dei nodi in
   meno**. **Adottare `TAU_A = 2.0` non sarebbe togliere una compensazione: sarebbe cambiare
   sistema.**

**Quindi: `Z9` ha una via tecnicamente percorribile, e NON la propongo come cura.** Il mandato lo
vieta esplicitamente (*«NON promuovere in questo giro»*), e la misura dà la ragione per cui il
divieto è giusto.

---

## 5. COSA RESTA, E COSA NON HO GUARDATO

- **`chi`, `|<n>|`, `theta`, `L_tot`, MISURA U: non misurati e non riportati**, come ordinato.
  **Senza quelli non si può dire se la «terza combinazione» sia fisicamente sensata** — si sa solo
  che non produce NaN.
- **Un solo seme.** I rapporti (× 91, −32 %) **non hanno barra**, e su questo sistema la dispersione
  fra semi è grande. **Sono ordini di grandezza, non misure.**
- **Il default non è cambiato**, il flag è **OFF**, e **S3** garantisce che senza flag il
  comportamento è **byte-identico**.
- **`Z10` resta aperta:** `TAU_A` governa **due leggi**, e questo esperimento le ha mosse
  **entrambe** — la maturazione del kernel **e** la memoria spinoriale. **Parte dello stress
  osservato può venire dalla seconda, non dalla prima**, e **distinguerle richiede la separazione
  che `Z10` chiede.**
