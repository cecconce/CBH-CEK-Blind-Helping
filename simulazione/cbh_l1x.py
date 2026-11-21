"""Piano senza camera con 2 VL53L1X (cono 27 gradi, portata nominale 3,6 m al chiuso)."""
import numpy as np
from cbh_sim import ToF, Luna, OBST, H

NEED = 1.29
OB = OBST + [("persona", 0.25, 0.45, 0.0, 1.7), ("muro", 0.2, 4.0, 0.0, 2.5)]
D = np.round(np.arange(2.5, 0.149, -0.05), 2)
YB = np.round(np.arange(-0.3, 0.31, 0.1), 2)

def L1X(yaw, pitch, y=0.0, rmax=3.6):
    return ToF(yaw, pitch, y, half=13.5, rmax=rmax, n=300)

def first(sensors):
    out = []
    for _, dx, wy, z0, z1 in OB:
        v = np.array([[any(s.sees(np.array([d, y - wy/2, z0]), np.array([d + dx, y + wy/2, z1])) for s in sensors)
                       for d in D] for y in YB]).all(0)
        out.append(D[v].max() if v.any() else 0.0)
    return np.array(out)

if __name__ == "__main__":
    mod = [ToF(-9, 54), ToF(9, 47), ToF(-4, -41), ToF(-9, -62)]
    base = mod + [Luna(-41)]
    cfgs = {
        "senza L1X": [],
        "2 L1X dritti affiancati (yaw +-10)": [L1X(-10, 0, .1), L1X(10, 0, -.1)],
        "1 dritto + 1 a 25 gradi in basso": [L1X(0, 0), L1X(0, -25)],
        "1 a 12 in alto + 1 a 20 in basso": [L1X(0, 12), L1X(0, -20)],
        "1 a 12 in alto + 1 a 20 in basso, luce forte (1,3 m)": [L1X(0, 12, rmax=1.3), L1X(0, -20, rmax=1.3)],
    }
    res = {k: first(base + v) for k, v in cfgs.items()}
    print(f"{'primo allarme [m]':28s} " + " | ".join(f"{i}" for i in range(len(cfgs))))
    for i, ob in enumerate(OB):
        print(f"{ob[0]:28s} " + " | ".join(f"{res[k][i]:4.2f}{'*' if res[k][i] < NEED else ' '}" for k in cfgs))
    for i, k in enumerate(cfgs):
        print(f"{i} = {k}: in tempo {int((res[k] >= NEED).sum())}/{len(OB)}")
    print("* = allarme sotto 1,29 m (tardi a 1,0 m/s)")
