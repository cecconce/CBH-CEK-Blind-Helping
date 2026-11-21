"""Copertura v2: intervalli di visibilita', rumore camera, ottimizzazione puntamento ToF."""
import numpy as np
from cbh_sim import *

NEED = 1.29
fB = 320 / np.tan(np.radians(36.5)) * 0.075

class Cam2(Cam):
    def sees(s, lo, hi):
        if not Cam.sees(s, lo, hi): return False
        if lo[2] == 0 and hi[2] < 0.5:      # ostacolo basso: deve staccarsi dal pavimento di 3 sigma
            r = np.hypot(lo[0], H)
            return r * hi[2] / H >= 3 * r * r * 0.5 / fB
        return True

OB = OBST + [("persona", 0.25, 0.45, 0.0, 1.7), ("muro", 0.2, 4.0, 0.0, 2.5)]
D = np.round(np.arange(2.5, 0.149, -0.05), 2)
YB = np.round(np.arange(-0.3, 0.31, 0.1), 2)

def vis(sensors):
    V = np.zeros((len(OB), len(YB), len(D)), bool)
    for i, (_, dx, wy, z0, z1) in enumerate(OB):
        for j, y in enumerate(YB):
            for k, d in enumerate(D):
                lo = np.array([d, y - wy/2, z0]); hi = np.array([d + dx, y + wy/2, z1])
                V[i, j, k] = any(s.sees(lo, hi) for s in sensors)
    return V

def table(name, V):
    print(f"\n=== {name} ===")
    print(f"{'ostacolo':28s} primo allarme | visto fino a | % zona 0,15-1,25 m coperta")
    near = D <= 1.25
    for i, ob in enumerate(OB):
        v = V[i].all(0)                       # visto su tutta la traiettoria del corpo
        first = D[v].max() if v.any() else 0
        k = np.argmax(v) if v.any() else 0
        last = first
        while v.any() and k < len(D) and v[k]: last = D[k]; k += 1
        flag = "" if first >= NEED else "  <-- TARDI"
        print(f"{ob[0]:28s} {first:4.2f} m | {last:4.2f} m | {100*V[i][:, near].mean():3.0f}%{flag}")
    print(f"zona vicina coperta in totale: {100*V[:, :, near].mean():.0f}%")

mix = [ToF(-12, 0, 0.1), ToF(12, 0, -0.1), ToF(0, 30), ToF(0, -35)]
fan = [ToF(-27, 0), ToF(-9, 0), ToF(9, 0), ToF(27, 0)]
Vc = {p: vis([Cam2(p)]) for p in (0, -10, -15, -20)}
for p in Vc: table(f"solo camera, inclinazione {p} gradi", Vc[p])
Vfan = vis(fan + [Luna(0)]); table("PIANO SENZA CAMERA: 4 ToF a ventaglio + Luna dritto", Vfan)
Vmix = vis(mix + [Luna(0)]); table("PIANO SENZA CAMERA: 4 ToF misti + Luna dritto", Vmix)

# ottimizzazione puntamento dei 4 ToF per chiudere la zona vicina
near = D <= 1.25
def tofvis(params):
    return vis([ToF(y, p, yy) for (y, p, yy) in params])
best = {}
for campitch in (0, -15):
    bs, bp = -1, None
    for it in range(250):
        if it == 0: params = [(-12, 0, .1), (12, 0, -.1), (0, 30, 0), (0, -35, 0)]
        elif it < 120 or bp is None:
            params = [(rng.uniform(-25, 25), rng.uniform(-65, 55), rng.uniform(-.15, .15)) for _ in range(4)]
        else:
            params = [(y + rng.normal(0, 5), p + rng.normal(0, 7), yy) for (y, p, yy) in bp]
        V = tofvis(params) | Vc[campitch]
        s = V[:, :, near].mean() + 0.5 * V[:8, :, near].all(1).any(1).mean()
        if s > bs: bs, bp, bV = s, params, V
    best[campitch] = (bp, bV)
    print(f"\n*** camera {campitch} gradi: miglior puntamento ToF (yaw, pitch): " +
          ", ".join(f"({y:+.0f}, {p:+.0f})" for y, p, _ in bp))
    table(f"COMPLETO ottimizzato, camera {campitch}", bV)
    Vt = tofvis(bp) | vis([Luna(0)])
    table(f"  stessi ToF + Luna SENZA camera (se la OAK non va)", Vt)

print("\n##### pavimento e testa in funzione dell'inclinazione camera #####")
for p in (0, -10, -15, -20):
    fl = H / np.tan(np.radians(29 - p)); top = H + NEED * np.tan(np.radians(29 + p))
    print(f"camera {p:+d}: vede il pavimento da {fl:.2f} m in poi; a {NEED} m vede fino a {top:.2f} m di altezza")
print("\n##### gradino in discesa: camera contro Luna #####")
for drop in (0.10, 0.15, 0.20):
    rmax = drop / H * fB / 1.5; dmax = np.sqrt(max(rmax**2 - H**2, 0))
    print(f"gradino {drop*100:.0f} cm: la camera lo distingue (3 sigma) fino a {dmax:.2f} m" + ("  <-- TARDI" if dmax < NEED else ""))
aim = 1.5; p = np.degrees(np.arctan(H/aim)); r = np.hypot(H, aim)
for res in (4, 1, 0.5):
    e = abs(np.hypot(H, H/np.tan(np.radians(p-res))) - np.hypot(H, H/np.tan(np.radians(p+res))))/2
    print(f"Luna a 1,5 m: errore angolo busto +-{res} gradi -> {e*100:.0f} cm di falso salto (segnale gradino 10 cm = {r*0.10/H*100:.0f} cm)")
