"""Make the README figures. Runs the part-1 notebook's code first, then draws each figure into figures/.
Usage, from the repository root:  python scripts/readme_figures.py"""
import os, json, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.join(ROOT, 'notebooks'))
nb = json.load(open('01_core_reconstruction.ipynb'))
exec('\n'.join(''.join(c['source']) for c in nb['cells'] if c['cell_type'] == 'code'))   # the notebook's code
plt.close('all')
OUT = os.path.join(ROOT, 'figures')
os.makedirs(OUT, exist_ok=True)

INK, INK2, MUTED, GRID = '#0b0b0b', '#52514e', '#8a8984', '#e4e3df'
BLUE, ORANGE, RED = '#2a78d6', '#eb6834', '#e34948'
SEQ = LinearSegmentedColormap.from_list('seq', ['#cde2fb', '#86b6ef', '#3987e5', '#1c5cab', '#0d366b'])
DIV = LinearSegmentedColormap.from_list('div', ['#1c5cab', '#86b6ef', '#f0efec', '#f0a3a2', '#c03332'])
plt.rcParams.update({'font.size': 8, 'axes.edgecolor': '#c3c2b7', 'axes.linewidth': 0.6,
                     'xtick.color': INK2, 'ytick.color': INK2, 'axes.labelcolor': INK, 'text.color': INK,
                     'font.family': 'DejaVu Sans'})

def wafer(ax, values, cmap, vmin, vmax, ring=True, title=None, outline_sites=None, size=None):
    """Draw one wafer map: each site as a square coloured by its value."""
    ax.add_patch(Circle((0, 0), 100, fill=False, ec=MUTED, lw=0.8))
    s = size or 13.5
    for (x, y), v in zip(xy, values):
        ax.add_patch(Rectangle((x - s / 2, y - s / 2), s, s, color=cmap((v - vmin) / (vmax - vmin)), lw=0))
    if outline_sites is not None:
        for j in outline_sites:
            ax.add_patch(Rectangle((xy[j, 0] - s / 2 - 1.5, xy[j, 1] - s / 2 - 1.5), s + 3, s + 3, fill=False, ec=INK, lw=1.1))
    if ring:
        ax.add_patch(Circle((0, 0), 76.5, fill=False, ec=MUTED, lw=0.6, ls='--'))
    ax.set_xlim(-104, 104); ax.set_ylim(-104, 104); ax.set_aspect('equal'); ax.axis('off')
    if title: ax.set_title(title, fontsize=8)

def cbar(fig, ax, cmap, vmin, vmax, label):
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin, vmax))
    cb = fig.colorbar(sm, ax=ax, fraction=0.046, pad=0.02)
    cb.set_label(label, fontsize=7); cb.ax.tick_params(labelsize=6.5); cb.outline.set_linewidth(0.4)
    return cb

def save(fig, name):
    fig.savefig(f'{OUT}/{name}.png', dpi=170, bbox_inches='tight')
    plt.close(fig)

# ---------- F1: the question ----------
fig, axes = plt.subplots(1, 2, figsize=(6.6, 3.0))
ax = axes[0]
ax.add_patch(Circle((0, 0), 100, fill=False, ec=MUTED, lw=0.8))
ax.add_patch(Circle((0, 0), 76.5, fill=False, ec=MUTED, lw=0.6, ls='--'))
for j, (x, y) in enumerate(xy):
    on = j in routine
    ax.add_patch(Rectangle((x - 5, y - 5), 10, 10, color=INK if on else ('#9ec5f4' if inner[j] else '#f0a3a2'), lw=0))
for yy, txt, col in [(80, 'black: routine 9', INK), (62, 'blue: inner 49', '#1c5cab'), (44, 'red: outer 40', '#c03332'), (26, 'dashed: 76.5 mm', INK2)]:
    ax.text(108, yy, txt, fontsize=6.8, color=col, ha='left', va='center')
ax.set_xlim(-104, 150); ax.set_ylim(-104, 104); ax.set_aspect('equal'); ax.axis('off')
ax.set_title('The 89-site grid (19 mm spacing)', fontsize=8)
wafer(axes[1], Y[0], SEQ, 40.5, 53.5, outline_sites=routine, title='Wafer 1 (lot 1): depth in µm, routine 9 boxed')
cbar(fig, axes[1], SEQ, 40.5, 53.5, 'step height (µm)')
axes[1].text(0, -122, 'routine 9 read 41.1–44.5 µm;  the full map spans 40.9–53.2 µm', ha='center', fontsize=7, color=INK2)
save(fig, 'question')

# ---------- F2: pipeline ----------
fig, ax = plt.subplots(figsize=(6.8, 2.2))
ax.set_xlim(0, 100); ax.set_ylim(0, 30); ax.axis('off')
steps = [('1  Check data', 'grid, lots, dates;\n180° turn and\noffset'),
         ('2  Screen', 'find bad readings;\nfix them in\ntraining only'),
         ('3  Learn shapes', 'PCA on training\nlots: average map\n+ 4 shapes'),
         ('4  Fit a wafer', 'k readings → level\n+ 4 dials → map\n+ 90% range'),
         ('5  Test', 'hold out a lot;\nhide sites; score\ninner and outer')]
for i, (head, body) in enumerate(steps):
    x0 = 1 + i * 20
    ax.add_patch(FancyBboxPatch((x0, 8), 17, 18, boxstyle='round,pad=0.4,rounding_size=1.5', fc='#f4f8fe', ec='#86b6ef', lw=0.8))
    ax.text(x0 + 8.5, 22.8, head, ha='center', va='center', fontsize=7.2, fontweight='bold')
    ax.text(x0 + 8.5, 14.2, body, ha='center', va='center', fontsize=6.2, color=INK2, linespacing=1.25)
    if i < 4:
        ax.annotate('', xy=(x0 + 19.6, 17), xytext=(x0 + 17.6, 17), arrowprops=dict(arrowstyle='->', color=MUTED, lw=0.9))
ax.text(70, 3.2, 'Rival A = step 4 with no shapes: the average map, shifted up or down to match the readings',
        ha='center', fontsize=6.6, color=ORANGE)
save(fig, 'pipeline')

# ---------- F3: the 180° turn ----------
fig, axes = plt.subplots(1, 2, figsize=(6.2, 2.7), sharey=True)
row = {k: i for i, k in enumerate(wafers.experiment_key)}
sub_r = rout[rout.experiment_key.isin(both)]
for ax, turn in zip(axes, [False, True]):
    sg = -1 if turn else 1
    a = [Y[row[m.experiment_key], sites.index((sg * m.X // 1000, sg * m.Y // 1000))] for _, m in sub_r.iterrows()]
    b = sub_r[TARGET].to_numpy()
    ax.scatter(a, b, s=5, color=BLUE, alpha=0.6, lw=0)
    lo, hi = 39, 46
    ax.plot([lo, hi], [lo - 1.06, hi - 1.06], color=MUTED, lw=0.8, ls='--')
    d = b - np.array(a)
    ax.set_title(['same (x, y): scatter %.2f µm' , 'site turned 180°: scatter %.3f µm'][turn] % np.sqrt(np.mean((d - d.mean()) ** 2)), fontsize=8)
    ax.set_xlabel('full map at the paired site (µm)')
    ax.set_xlim(lo, hi); ax.set_ylim(lo - 1.5, hi - 0.5)
    ax.spines[['top', 'right']].set_visible(False); ax.grid(color=GRID, lw=0.5)
axes[0].set_ylabel('second instrument, etch day (µm)')
axes[1].text(39.3, 44.2, 'dashed: same depth\nminus 1.06 µm', fontsize=6.5, color=INK2)
fig.tight_layout(); save(fig, 'instrument_turn')

# ---------- F4: the screen ----------
w6 = [w for w, s in suspect if lot[w] == 6][0]; s6 = [s for w, s in suspect if lot[w] == 6][0]
typ = np.median(Y - np.median(Y, axis=1, keepdims=True), axis=0)
fig, axes = plt.subplots(1, 3, figsize=(7.0, 2.4), gridspec_kw=dict(width_ratios=[1, 1, 1.05]))
for ax, (vals, ttl, yl) in zip(axes[:2], [(Y[w6], 'raw depth vs radius', 'depth (µm)'),
                                         (Y[w6] - np.median(Y[w6]) - typ, 'after removing level + typical map', 'deviation (µm)')]):
    ax.scatter(r, vals, s=6, color='#c3c2b7', lw=0)
    ax.scatter(r[nbrs[s6]], vals[nbrs[s6]], s=14, color=BLUE, lw=0, label='its 8 touching sites')
    ax.scatter(r[s6], vals[s6], s=22, color=RED, lw=0, label='the bad reading')
    ax.set_xlabel('radius (mm)'); ax.set_ylabel(yl); ax.set_title(ttl, fontsize=8)
    ax.spines[['top', 'right']].set_visible(False)
axes[1].set_ylim(-1, 1); axes[1].scatter([r[s6]], [-0.95], marker='v', s=30, color=RED, lw=0); axes[1].text(r[s6] - 4, -0.9, 'bad reading: −15.9 µm\n(off the bottom)', fontsize=6.3, color=RED, ha='right')
axes[0].legend(fontsize=6.3, frameon=False, loc='upper left')
z_sorted = np.sort(np.abs(z_all).ravel())[::-1][:30]
axes[2].bar(range(30), z_sorted, color=[RED if v > THRESHOLD else '#9ec5f4' for v in z_sorted], width=0.8)
axes[2].axhline(THRESHOLD, color=INK2, lw=0.8, ls='--'); axes[2].text(29, THRESHOLD * 1.12, 'threshold 30', ha='right', fontsize=6.5, color=INK2)
axes[2].set_yscale('log'); axes[2].set_title('30 most unusual of 7,832 readings', fontsize=8)
axes[2].set_ylabel('score (MAD units, log)'); axes[2].set_xlabel('rank'); axes[2].spines[['top', 'right']].set_visible(False)
fig.tight_layout(); save(fig, 'bad_reading_screen')

# ---------- F5: shapes ----------
def shapes_of(M, K=4):
    lv = M.mean(axis=1); d = M - lv[:, None]; avg = d.mean(axis=0); D = d - avg
    U, S, Vt = np.linalg.svd(D, full_matrices=False)
    return avg, Vt[:K], S ** 2 / np.sum(S ** 2)
avg, V4, fr = shapes_of(Yclean)
_, Vraw, frr = shapes_of(Y)
names_s = ['edge ring', 'left–right tilt', 'top–bottom tilt', 'small edge feature']
fig, axes = plt.subplots(2, 5, figsize=(7.2, 3.3))
wafer(axes[0, 0], avg, SEQ, avg.min(), avg.max(), title='average map\n(minus level)')
for k in range(4):
    v = V4[k] * np.sign(V4[k][np.argmax(np.abs(V4[k]))]); m = np.abs(v).max()
    wafer(axes[0, k + 1], v, DIV, -m, m, title='shape %d: %.0f%%' % (k + 1, 100 * fr[k]))
for k in range(2):
    v = Vraw[k] * np.sign(Vraw[k][np.argmax(np.abs(Vraw[k]))]); m = np.abs(v).max()
    wafer(axes[1, k + 1], v, DIV, -m, m, title='shape %d: %.0f%%' % (k + 1, 100 * frr[k]))
for ax in [axes[1, 0], axes[1, 3], axes[1, 4]]:
    ax.axis('off')
fig.text(0.035, 0.72, 'after\nthe\nscreen', fontsize=7.5, ha='center', va='center', fontweight='bold')
axes[1, 0].text(0.75, 0.5, 'bad\nreadings\nleft in', fontsize=7.5, ha='center', va='center', fontweight='bold', transform=axes[1, 0].transAxes)
axes[1, 3].text(0.0, 0.5, '← each is a single site:\n   the two bad readings', fontsize=7, va='center', color=RED, transform=axes[1, 3].transAxes)
fig.text(0.5, 0.005, 'Red = deeper than average for that shape, blue = shallower. Percent = share of the shape variation each explains.',
         ha='center', fontsize=6.5, color=INK2)
save(fig, 'pca_shapes')
SHAPE_TILT = np.corrcoef(V4[1], xy[:, 0])[0, 1]

# ---------- F6: why a prior (1-D cartoon) ----------
xs = np.linspace(-1, 1, 200)
basis = np.stack([np.ones_like(xs), 2 * xs ** 2 - 1, xs, xs ** 3 - 0.6 * xs, xs ** 4 - xs ** 2])  # level + 4 "shapes"
typical = 0.8 * basis[1]
meas_x = np.array([-0.55, 0.05, 0.6]); idxm = [np.argmin(np.abs(xs - v)) for v in meas_x]
truth = typical + 0.15 + 0.25 * basis[2] + 0.1 * basis[3]
y_m = truth[idxm]
fig, ax = plt.subplots(figsize=(5.6, 2.5))
B = basis[:, idxm].T
rng2 = np.random.default_rng(3)
for t in range(14):                                     # maps that pass exactly through the 3 readings
    free = rng2.normal(0, 3, 2)
    c34 = np.r_[free]
    rhs = y_m - typical[idxm] - B[:, 3:] @ c34
    c012 = np.linalg.solve(B[:, :3], rhs)
    ax.plot(xs, typical + np.r_[c012, c34] @ basis, color='#c3c2b7', lw=0.6, zorder=1)
P0 = np.array([1.0, 0.3, 0.3, 0.15, 0.15]) ** 2; nv = 0.02 ** 2
cov = np.linalg.inv(np.diag(1 / P0) + B.T @ B / nv); coef = cov @ (B.T @ (y_m - typical[idxm]) / nv)
ax.plot(xs, typical, color=MUTED, lw=1.2, ls='--', label='typical map', zorder=2)
ax.plot(xs, typical + coef @ basis, color=BLUE, lw=2, label='with the prior: fits the readings, stays typical', zorder=3)
ax.scatter(meas_x, y_m, color=INK, s=26, zorder=4, label='3 readings')
ax.plot([], [], color='#c3c2b7', lw=0.6, label='other maps that also pass through all 3')
ax.set_ylim(-2.2, 2.2); ax.set_xlabel('position across the wafer'); ax.set_ylabel('depth (arbitrary)')
ax.set_yticks([]); ax.set_xticks([]); ax.spines[['top', 'right']].set_visible(False)
ax.legend(fontsize=6.5, frameon=False, loc='lower center', ncol=2)
save(fig, 'prior_cartoon')

# ---------- F7: leave-one-lot-out ----------
fig, ax = plt.subplots(figsize=(6.8, 1.9))
ax.set_xlim(0, 100); ax.set_ylim(0, 24); ax.axis('off')
for i in range(10):
    test = (i == 3)
    ax.add_patch(FancyBboxPatch((1 + i * 5.3, 9), 4.4, 9, boxstyle='round,pad=0.2,rounding_size=0.8',
                                fc=('#fde3d9' if test else '#e7f0fc'), ec=(ORANGE if test else '#86b6ef'), lw=0.8))
    ax.text(3.2 + i * 5.3, 13.5, 'lot\n%d' % (i + 1), ha='center', va='center', fontsize=6.5)
ax.text(27, 4.5, 'learn screen, average map, shapes, priors from the 9 blue lots', ha='center', fontsize=6.8, color='#1c5cab')
ax.text(19.1, 21, 'test lot', ha='center', fontsize=6.8, color=ORANGE)
ax.annotate('', xy=(62, 13.5), xytext=(55, 13.5), arrowprops=dict(arrowstyle='->', color=MUTED, lw=0.9))
# a mini wafer with measured / hidden sites
cx, cy, sc = 75, 12, 0.095
ax.add_patch(Circle((cx, cy), 100 * sc, fill=False, ec=MUTED, lw=0.7))
lay = layouts[5][0]
for j, (x, y) in enumerate(xy):
    ax.add_patch(Rectangle((cx + x * sc - 0.55, cy + y * sc - 0.55), 1.1, 1.1, color=(INK if j in lay else '#c3c2b7'), lw=0))
ax.text(87, 16.5, 'each test wafer: measure k sites\n(black), predict the hidden ones', fontsize=6.5, va='center')
ax.text(87, 8, 'score: RMS error at hidden\nsites, inner and outer apart', fontsize=6.5, va='center')
ax.text(75, 0.5, '200 random layouts per k, same for both methods; repeat for all 10 lots', ha='center', fontsize=6.3, color=INK2)
save(fig, 'leave_one_lot_out')

# F8, error vs number of sites, is drawn by the notebook itself (figures/error_vs_sites.png)

# ---------- F9: per-lot at 5 sites ----------
po, pa = rmse('ours', 5, 'B', per_lot=True), rmse('rival A', 5, 'B', per_lot=True)
fig, ax = plt.subplots(figsize=(5.6, 2.3))
for i in range(10):
    ax.plot([i + 1, i + 1], [po[i], pa[i]], color='#c3c2b7', lw=1.5, zorder=1)
ax.scatter(lots, pa, color=ORANGE, s=26, zorder=2, label='rival A')
ax.scatter(lots, po, color=BLUE, s=26, zorder=3, label='ours')
ax.set_xticks(lots); ax.set_xlabel('held-out lot'); ax.set_ylabel('error at hidden sites (µm)')
ax.set_ylim(0, None); ax.grid(axis='y', color=GRID, lw=0.5); ax.spines[['top', 'right']].set_visible(False)
ax.legend(fontsize=7, frameon=False, ncol=2, loc='upper right'); ax.set_title('5 measured sites, every lot', fontsize=8)
save(fig, 'per_lot')

# ---------- F10: one wafer from its routine 9 ----------
preds = {}
errs_r9 = []
for L in lots:
    Ytr, _ = screen(Y[lot != L], Y[lot != L], THRESHOLD)
    mo, ma = learn(Ytr, K), learn(Ytr, 0)
    te = np.where(lot == L)[0]
    po_, _ = fit(mo, np.array(routine), Y[te][:, routine]); pa_, _ = fit(ma, np.array(routine), Y[te][:, routine])
    for i, w in enumerate(te):
        preds[w] = (po_[i], pa_[i])
        if valid[w].all():
            errs_r9.append((np.sqrt(np.mean((po_[i] - Y[w])[~inner] ** 2)), w))
errs_r9.sort(); w_ex = errs_r9[len(errs_r9) // 2][1]
p_o, p_a = preds[w_ex]
fig, axes = plt.subplots(2, 3, figsize=(6.6, 4.4))
lo, hi = Y[w_ex].min(), Y[w_ex].max()
wafer(axes[0, 0], Y[w_ex], SEQ, lo, hi, outline_sites=routine, title='true map (lot %d wafer %d)' % (lot[w_ex], wafers.wafer_number[w_ex]))
wafer(axes[0, 1], p_o, SEQ, lo, hi, outline_sites=routine, title='ours, from the routine 9')
wafer(axes[0, 2], p_a, SEQ, lo, hi, outline_sites=routine, title='rival A, from the routine 9')
cbar(fig, axes[0, 2], SEQ, lo, hi, 'depth (µm)')
axes[1, 0].axis('off')
axes[1, 0].text(0.5, 0.5, 'error = prediction − truth\n(same colour scale)\n\nboxed = the 9 measured sites', ha='center', va='center',
                fontsize=7, color=INK2, transform=axes[1, 0].transAxes)
em = 0.35
wafer(axes[1, 1], p_o - Y[w_ex], DIV, -em, em, outline_sites=routine,
      title='ours: outer RMS %.2f µm' % np.sqrt(np.mean((p_o - Y[w_ex])[~inner] ** 2)))
wafer(axes[1, 2], p_a - Y[w_ex], DIV, -em, em, outline_sites=routine,
      title='rival A: outer RMS %.2f µm' % np.sqrt(np.mean((p_a - Y[w_ex])[~inner] ** 2)))
cbar(fig, axes[1, 2], DIV, -em, em, 'error (µm)')
save(fig, 'routine9_example')
EXAMPLE = (lot[w_ex], wafers.wafer_number[w_ex])

# ---------- F11: one bad input reading ----------
L = lot[w6]; Ytr, _ = screen(Y[lot != L], Y[lot != L], THRESHOLD)
mo, ma = learn(Ytr, K), learn(Ytr, 0)
cands = []
for idx in [idx for idx in layouts[5] if s6 in idx]:
    p1, _ = fit(mo, idx, Y[[w6]][:, idx]); mk = np.ones(89, bool); mk[idx] = False; mk[s6] = False
    cands.append((np.sqrt(np.mean((p1[0] - Y[w6])[mk] ** 2)), list(idx)))
cands.sort(key=lambda t: t[0]); lay_bad = np.array(cands[len(cands) // 2][1])   # the median layout
po_, _ = fit(mo, lay_bad, Y[[w6]][:, lay_bad]); pa_, _ = fit(ma, lay_bad, Y[[w6]][:, lay_bad])
fig, axes = plt.subplots(1, 2, figsize=(5.4, 2.6))
em = 8
for ax, p, nm in [(axes[0], po_[0], 'ours'), (axes[1], pa_[0], 'rival A')]:
    e = p - Y[w6]; mask = np.ones(89, bool); mask[lay_bad] = False; mask[s6] = False
    wafer(ax, np.clip(e, -em, em), DIV, -em, em, outline_sites=lay_bad,
          title='%s\nother hidden sites off by %.1f µm' % (nm, np.sqrt(np.mean(e[mask] ** 2))))
    ax.add_patch(Circle(tuple(xy[s6]), 13, fill=False, ec=RED, lw=1.2))
cbar(fig, axes[1], DIV, -em, em, 'error (µm)')
fig.text(0.45, -0.02, 'Lot 6 wafer 7, 5 measured sites (boxed), one of them the bad reading (circled); the median of its 9 such layouts.', ha='center', fontsize=6.8, color=INK2)
save(fig, 'bad_input_reading')

# ---------- F12: lot 1's tilt ----------
fig, ax = plt.subplots(figsize=(5.6, 2.2))
rng3 = np.random.default_rng(1)
for L in lots:
    v = amount[lot == L]
    ax.scatter(L + rng3.uniform(-0.15, 0.15, len(v)), v, s=14, color=(RED if L == 1 else BLUE), lw=0)
ax.axhspan(-np.abs(amount[lot != 1]).max(), np.abs(amount[lot != 1]).max(), color='#e7f0fc', zorder=0)
ax.text(10.4, 0.9, 'range of all\nother lots', fontsize=6.3, color='#1c5cab', va='bottom', ha='right')
ax.set_xticks(lots); ax.set_xlabel('lot'); ax.set_ylabel('amount of shape 2\n(left–right tilt)')
ax.spines[['top', 'right']].set_visible(False); ax.axhline(0, color=GRID, lw=0.6)
save(fig, 'lot1_tilt')

# numbers quoted in the README
print('EXAMPLE wafer', EXAMPLE, '| shape2 vs x r=%.2f' % SHAPE_TILT, '| fr screened', np.round(100 * fr[:5], 1), '| fr raw', np.round(100 * frr[:4], 1))
print('shape corr with x,y,r2:', [(round(np.corrcoef(V4[k], xy[:, 0])[0, 1], 2), round(np.corrcoef(V4[k], xy[:, 1])[0, 1], 2), round(np.corrcoef(V4[k], r ** 2)[0, 1], 2)) for k in range(4)])
print('routine-9 median outer error ours/A:', np.round(np.sqrt(np.mean((p_o - Y[w_ex])[~inner] ** 2)), 3), np.round(np.sqrt(np.mean((p_a - Y[w_ex])[~inner] ** 2)), 3))
