"""Simulazione di fattibilita' CBH: copertura geometrica, tempi, gradino, autonomia.
Assi: x = avanti, y = sinistra, z = alto. Persona in x=0, sensori sul petto."""
import numpy as np

rng = np.random.default_rng(42)
H = 1.30  # altezza sensori (petto) [m]


# ---------- geometria ----------
def dirs_cone(yaw, pitch, half_deg, n):
    """n raggi uniformi in un cono (semi-apertura half_deg) puntato a yaw/pitch [gradi]."""
    k = np.arange(n) + 0.5
    r = np.sqrt(k / n) * np.tan(np.radians(half_deg))
    t = k * 2.399963
    local = np.stack([np.ones(n), r * np.cos(t), r * np.sin(t)], 1)
    return rot(local, yaw, pitch)


def dirs_rect(yaw, pitch, hfov, vfov, step=0.5):
    a = np.radians(np.arange(-hfov / 2, hfov / 2 + 1e-9, step))
    b = np.radians(np.arange(-vfov / 2, vfov / 2 + 1e-9, step))
    A, B = np.meshgrid(a, b)
    local = np.stack([np.ones(A.size), np.tan(A).ravel(), np.tan(B).ravel()], 1)
    return rot(local, yaw, pitch)


def rot(v, yaw, pitch):
    v = v / np.linalg.norm(v, axis=1, keepdims=True)
    p, y = np.radians(pitch), np.radians(yaw)
    Rp = np.array([[np.cos(p), 0, -np.sin(p)], [0, 1, 0], [np.sin(p), 0, np.cos(p)]])
    Ry = np.array([[np.cos(y), -np.sin(y), 0], [np.sin(y), np.cos(y), 0], [0, 0, 1]])
    return v @ (Ry @ Rp).T


def ray_box(o, d, lo, hi):
    """distanza lungo il raggio fino al box (inf se mancato)."""
    with np.errstate(divide="ignore", invalid="ignore"):
        t1 = (lo - o) / d
        t2 = (hi - o) / d
    tn = np.nanmax(np.minimum(t1, t2), axis=1)
    tf = np.nanmin(np.maximum(t1, t2), axis=1)
    hit = (tf >= tn) & (tf > 0)
    return np.where(hit, np.maximum(tn, 0), np.inf)


def floor_t(o, d):
    with np.errstate(divide="ignore"):
        t = -o[2] / d[:, 2]
    return np.where(d[:, 2] < 0, t, np.inf)


# ---------- sensori ----------
class Cam:  # OAK-D Lite, stereo passivo
    def __init__(s, pitch, minz=0.35):
        s.o = np.array([0, 0, H]); s.pitch = pitch; s.minz = minz
        s.d = dirs_rect(0, pitch, 73, 58)
        s.axis = rot(np.array([[1.0, 0, 0]]), 0, pitch)[0]

    def sees(s, lo, hi):
        t = ray_box(s.o, s.d, lo, hi)
        ok = (t < floor_t(s.o, s.d)) & np.isfinite(t)
        depth = t * (s.d @ s.axis)
        ok &= (depth >= s.minz) & (depth <= 8)
        return ok.sum() >= 6  # almeno ~6 campioni da 0,5 gradi


class ToF:  # cono con modello di segnale: riempimento/d^2
    def __init__(s, yaw, pitch, y=0.0, half=9.0, rmax=1.2, rmin=0.0, n=150):
        s.o = np.array([0, y, H]); s.d = dirs_cone(yaw, pitch, half, n)
        s.rmax, s.rmin = rmax, rmin

    def sees(s, lo, hi):
        t = ray_box(s.o, s.d, lo, hi)
        ok = (t < floor_t(s.o, s.d)) & np.isfinite(t) & (t >= s.rmin)
        if not ok.any():
            return False
        fill = ok.mean(); dist = t[ok].mean()
        return fill * (s.rmax / dist) ** 2 >= 1.0


def Luna(pitch):
    return ToF(0, pitch, half=1.0, rmax=8.0, rmin=0.2, n=30)


# ---------- ostacoli: (nome, dx, larghezza y, z0, z1, largo?) ----------
OBST = [
    ("palo 5 cm", 0.05, 0.05, 0.0, 2.0),
    ("paletto 60 cm", 0.15, 0.15, 0.0, 0.6),
    ("cordolo 15 cm (in salita)", 0.5, 2.0, 0.0, 0.15),
    ("sedia/panchina 45 cm", 0.4, 0.5, 0.0, 0.45),
    ("bordo tavolo 72 cm", 0.6, 1.0, 0.70, 0.74),
    ("transenna 1,0 m", 0.05, 1.5, 1.00, 1.05),
    ("cartello a 1,7-2,0 m", 0.03, 0.4, 1.70, 2.00),
    ("ramo 3 cm a 1,75 m", 0.03, 1.0, 1.735, 1.765),
]
DS = np.round(np.arange(2.5, 0.049, -0.05), 2)
YS = np.round(np.arange(-0.7, 0.71, 0.1), 2)


def first_detection(sensors, ob, y0):
    """distanza del primo allarme mentre ci si avvicina (0 = mai visto)."""
    _, dx, wy, z0, z1 = ob
    for d in DS:
        lo = np.array([d, y0 - wy / 2, z0]); hi = np.array([d + dx, y0 + wy / 2, z1])
        if any(s.sees(lo, hi) for s in sensors):
            return d
    return 0.0


def evaluate(sensors, ys=YS):
    return np.array([[first_detection(sensors, ob, y) for y in ys] for ob in OBST])


def report(name, sensors, need):
    M = evaluate(sensors)
    body = np.abs(YS) <= 0.31
    print(f"\n=== {name} ===")
    print(f"{'ostacolo':28s} primo allarme [m]: min corridoio | min traiettoria corpo | % corridoio in tempo")
    for ob, row in zip(OBST, M):
        print(f"{ob[0]:28s} {row.min():4.2f} | {row[body].min():4.2f} | {100*(row>=need).mean():3.0f}%")
    print(f"TOTALE in tempo (>= {need} m): corridoio {100*(M>=need).mean():.0f}%  corpo {100*(M[:,body]>=need).mean():.0f}%")
    return M


# ---------- 2) tempi di reazione ----------
def stopping(v, path, n=200_000):
    if path == "cam":   # frame 30 fps + stereo/IA + USB + Linux + bridge
        tsys = rng.uniform(0, 0.033, n) + rng.normal(0.14, 0.03, n)
    else:               # ToF: budget 50 ms + giro I2C + MCU
        tsys = rng.uniform(0, 0.05, n) + rng.normal(0.02, 0.005, n)
    tsys += rng.normal(0.06, 0.015, n)                       # avvio motorino vibro
    thum = rng.lognormal(np.log(0.45), 0.35, n)              # reazione umana al tatto
    a = np.clip(rng.normal(2.0, 0.4, n), 1.0, None)          # decelerazione [m/s2]
    return v * (tsys + thum) + v**2 / (2 * a)


if __name__ == "__main__":
    print("##### 2) SPAZIO D'ARRESTO (mediana / 95 percentile) #####")
    for v in (0.6, 0.8, 1.0, 1.2, 1.4):
        c, t = stopping(v, "cam"), stopping(v, "tof")
        print(f"v={v:.1f} m/s  camera: {np.median(c):.2f}/{np.percentile(c,95):.2f} m   ToF: {np.median(t):.2f}/{np.percentile(t,95):.2f} m")
    for lim, path in ((2.0, "cam"), (1.2, "tof"), (0.66, "tof")):
        vs = np.arange(0.3, 2.01, 0.01)
        ok = [v for v in vs if np.percentile(stopping(v, path, 40_000), 95) <= lim]
        print(f"allarme a {lim} m ({path}): velocita' max sicura (95%) = {max(ok):.2f} m/s")
    NEED = round(float(np.percentile(stopping(1.0, "cam"), 95)), 2)
    print("soglia 'in tempo' usata nella copertura (1,0 m/s, 95%):", NEED)

    print("\n##### 1) COPERTURA #####")
    fan = [ToF(-27, 0), ToF(-9, 0), ToF(9, 0), ToF(27, 0)]
    mix = [ToF(-12, 0, 0.1), ToF(12, 0, -0.1), ToF(0, 30), ToF(0, -35)]
    report("A) solo camera, orizzontale", [Cam(0)], NEED)
    report("A2) solo camera, inclinata 15 gradi in basso", [Cam(-15)], NEED)
    report("B) senza camera: 4 ToF a ventaglio + Luna dritto", fan + [Luna(0)], NEED)
    report("B2) senza camera: 4 ToF misti + Luna dritto", mix + [Luna(0)], NEED)
    report("C) completo: camera 0 + ToF misti + Luna 40 gradi in basso", [Cam(0)] + mix + [Luna(-40)], NEED)
    report("C2) completo: camera -10 + ToF misti + Luna 40 in basso", [Cam(-10)] + mix + [Luna(-40)], NEED)

    print("\n##### zona vicina: cosa resta visibile a 0,5 m (ostacolo gia' vicino, es. dopo una svolta) #####")
    for name, S in (("solo camera 0", [Cam(0)]), ("camera 0 + ToF misti", [Cam(0)] + mix)):
        seen = []
        for ob in OBST:
            _, dx, wy, z0, z1 = ob
            r = [any(s.sees(np.array([0.5, y - wy/2, z0]), np.array([0.5+dx, y + wy/2, z1])) for s in S) for y in YS[np.abs(YS) <= 0.31]]
            seen.append(f"{ob[0]}: {100*np.mean(r):.0f}%")
        print(name, "->", "; ".join(seen))

    print("\n##### 3) GRADINO IN DISCESA col TF-Luna #####")
    for aim in (1.2, 1.5, 1.8):
        p = np.degrees(np.arctan(H / aim)); r = np.hypot(H, aim)
        for drop in (0.10, 0.15):
            sig = r * drop / H
            sway = [np.hypot(H, H / np.tan(np.radians(p + e))) for e in (-4, 4)]
            print(f"mira a {aim} m (inclinazione {p:.0f} gradi): gradino {drop*100:.0f} cm -> salto di {sig*100:.0f} cm "
                  f"(rumore sensore 6 cm); oscillazione busto +-4 gradi -> {abs(sway[0]-sway[1])/2*100:.0f} cm di falso segnale")
    f, B = 320 / np.tan(np.radians(36.5)), 0.075
    for z in (1.0, 2.0, 2.4):
        print(f"camera: errore di profondita' a {z} m = {z*z*0.5/(f*B)*100:.1f} cm (0,5 px), minima distanza = {f*B/95:.2f} m")

    print("\n##### 4) AUTONOMIA (power bank 72 Wh, resa 80-88%) #####")
    n = 100_000
    uno = rng.uniform(2.0, 5.0, n); cam = rng.uniform(2.5, 4.5, n)
    mod = rng.uniform(0.4, 1.0, n); hub = rng.uniform(0.5, 1.5, n)
    for lab, P in (("con camera", uno + cam + mod + hub), ("senza camera (piano B)", uno + mod + hub)):
        h = 72 * rng.uniform(0.80, 0.88, n) / P
        print(f"{lab}: potenza {np.percentile(P,5):.1f}-{np.percentile(P,95):.1f} W, autonomia {np.percentile(h,5):.1f}-{np.percentile(h,95):.1f} h (mediana {np.median(h):.1f})")
    print("giro I2C 4 ToF via hub @100 kHz: ~", round(4 * (2 + 3 + 4) * 9 * 10e-6 * 1000 * 3, 1), "ms -> limite reale = budget di misura (50 ms = 20 Hz)")
