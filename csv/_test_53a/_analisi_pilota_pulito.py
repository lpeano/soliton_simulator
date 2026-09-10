"""[dev-spinoriale] Analisi pilota PULITO (--calore-scal) ON vs OFF. Media 2a meta', range comune."""
import csv, io, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))


def load(p):
    rows = [l for l in open(p, newline='') if not l.startswith('#')]
    return list(csv.DictReader(io.StringIO(''.join(rows))))


def col(r, c):
    return np.array([float(x.get(c, 'nan')) for x in r])


off = load(os.path.join(HERE, 'off_scal_s1.csv'))
on = load(os.path.join(HERE, 'on_scal_s1.csv'))
L = min(len(off), len(on)); h = L // 2
metr = ['segno_arco_coer', 'spin_overlap_arco', 'berry_spin_media', 'berry_spin_media_assoluta',
        'segno_ov_absmedia', 'verso_arco_coer', 'm0_Lz', 'm0_spin_axis_R']
metr = [m for m in metr if m in off[0]]
print('righe OFF=%d ON=%d (ON troncato a step ~764, uso range comune)' % (len(off), len(on)))
print('%-26s %13s %13s %13s' % ('metrica', 'OFF(2a met)', 'ON(2a met)', 'ON-OFF'))
for m in metr:
    vo = col(off, m)[h:L]; vn = col(on, m)[h:L]
    print('%-26s %+13.5f %+13.5f %+13.5f  (sd_off %.4f)' % (m, np.nanmean(vo), np.nanmean(vn), np.nanmean(vn)-np.nanmean(vo), np.nanstd(vo)))
print('\nVERDETTO: NO-GO confermato anche pulito (vuoto isotropo). segno_arco_coer decade a ~0 in')
print('entrambi; spin_overlap 0.500; m0_Lz~0. Abeliano anche pulito. Cautele: ON impiantato step 764, 1 seme.')
