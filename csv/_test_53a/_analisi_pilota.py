"""[dev-spinoriale] Analisi pilota covariante MOD 5.3a+5.3b (--tempo-segno) — ON vs OFF, 800p seed 1.
DOMANDA: la materia/antimateria coerente che controlla il verso del tempo -> ordine del segno
ATTRATTORE (segno_arco_coer sale e RESTA) o resta 0.5 (abeliano)? Media 2a meta', N-appaiato.
"""
import csv, io, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))


def load(p):
    rows = [l for l in open(p, newline='') if not l.startswith('#')]
    return list(csv.DictReader(io.StringIO(''.join(rows))))


def col(r, c):
    return np.array([float(x.get(c, 'nan')) for x in r])


off = load(os.path.join(HERE, 'off_s1.csv'))
on = load(os.path.join(HERE, 'on_s1.csv'))
metr = ['segno_arco_coer', 'spin_overlap_arco', 'berry_spin_media', 'berry_spin_media_assoluta']
print('righe OFF=%d ON=%d' % (len(off), len(on)))
print('%-26s %12s %12s %12s' % ('metrica', 'OFF(2a meta)', 'ON(2a meta)', 'ON-OFF'))
for m in metr:
    vo = col(off, m); vn = col(on, m)
    mo = np.nanmean(vo[len(vo)//2:]); so = np.nanstd(vo[len(vo)//2:]); mn = np.nanmean(vn[len(vn)//2:])
    print('%-26s %+12.5f %+12.5f %+12.5f  (sd_off %.4f)' % (m, mo, mn, mn-mo, so))
so = col(off, 'segno_arco_coer'); sn = col(on, 'segno_arco_coer')
print('\nsegno_arco_coer OFF primi3=%s ultimi3=%s' % (np.round(so[:3], 3), np.round(so[-3:], 3)))
print('segno_arco_coer ON  primi3=%s ultimi3=%s' % (np.round(sn[:3], 3), np.round(sn[-3:], 3)))
print('\nVERDETTO PILOTA: NO-GO. segno_arco_coer decade a ~0 in ENTRAMBI (ON-OFF nel rumore);')
print('spin_overlap_arco 0.500=0.500. L\\'ordine del segno NON diventa attrattore col verso del')
print('tempo dalla materia/antimateria (Feynman-Stuckelberg). Cautele: 800p=formazione, 1 seme.')
