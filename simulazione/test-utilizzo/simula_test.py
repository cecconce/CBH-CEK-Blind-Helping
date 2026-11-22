#!/usr/bin/env python3
"""
CBH - CEK Blind Helping
Simulazione realistica di un test di utilizzo del giubbino (prototipo anno 1).

Sensori: OAK-D Lite (orizzontale), 4 Modulino Distance, 3 VL53L1X, TF-Luna,
Modulino Movement (IMU). Feedback: 2 Modulino Vibro, Buzzer, cuffie BT.

Percorso di prova: corridoio largo 2,5 m, 10 prove (un ostacolo per prova,
partenza a 5 m dall'ostacolo) + un tratto di corridoio vuoto per i falsi allarmi.

Uso:  python3 simula_test.py  [--n 100]
Dati dei sensori: valori di targa o stimati, NON misurati. Vedi resoconto.
"""
import argparse, math, os
import numpy as np

H_SENS = 1.30          # altezza dei sensori sul petto (m)
Z_CEIL = 2.70          # soffitto
Y_WALL = 1.25          # pareti a +/- 1,25 m
BAND_Y = 0.75          # fascia di passaggio considerata (larghezza 1,5 m)
BAND_Z = (0.08, 2.10)  # fascia d'altezza considerata
OBST_START = 5.0       # distanza iniziale dall'ostacolo
STEP_DROP = 0.15       # gradino in discesa

ID_NONE, ID_FLOOR, ID_CEIL, ID_WALL = 0, 1, 2, 3
ID_OBS, ID_GLASS, ID_LOWFLOOR = 10, 11, 12

# --------------------------------------------------------------------------
# Scena e ray casting
# --------------------------------------------------------------------------
def box(x0, x1, y0, y1, z0, z1, ident=ID_OBS):
    return ("box", np.array([x0, y0, z0]), np.array([x1, y1, z1]), ident)

def cyl(cx, cy, r, z0, z1, ident=ID_OBS):
    return ("cyl", (cx, cy, r, z0, z1), None, ident)

def make_obstacle(name, yo, x0=OBST_START):
    """Restituisce (primitive, riflettanza, etichetta IA, offset di contatto)."""
    if name == "persona":
        return [box(x0, x0 + .30, yo - .23, yo + .23, 0, 1.75)], .35, "persona", .35
    if name == "sedia":
        p = [box(x0, x0 + .45, yo - .22, yo + .22, .42, .46),
             box(x0 + .40, x0 + .45, yo - .22, yo + .22, .46, .90)]
        for dx in (.03, .42):
            for dy in (-.19, .19):
                p.append(cyl(x0 + dx, yo + dy, .015, 0, .42))
        return p, .20, "sedia", .35
    if name == "cartello testa":
        return [box(x0, x0 + .02, yo - .30, yo + .30, 1.70, 2.00)], .80, None, 0.0
    if name == "bordo tavolo":
        p = [box(x0, x0 + .80, yo - .60, yo + .60, .72, .76)]
        for dx in (.05, .75):
            for dy in (-.55, .55):
                p.append(cyl(x0 + dx, yo + dy, .02, 0, .72))
        return p, .50, "tavolo", .35
    if name == "palo sottile":
        return [cyl(x0 + .03, yo, .03, 0, 2.5)], .50, None, .35
    if name == "paletto basso":
        return [cyl(x0 + .05, yo, .05, 0, .70)], .60, None, .35
    if name == "zaino a terra":
        return [box(x0, x0 + .25, yo - .16, yo + .16, 0, .40)], .25, "zaino", .35
    if name == "vetrata":
        return [box(x0, x0 + .01, -1.0, 1.0, .05, 2.2, ID_GLASS),
                box(x0, x0 + .05, -1.0, 1.0, 0, .05)], .50, None, .35
    if name == "muro":
        return [box(x0, x0 + .30, -Y_WALL, Y_WALL, 0, Z_CEIL)], .70, None, .35
    if name == "gradino discesa":
        return [], .30, None, .35
    if name == "vuoto":
        return [], .30, None, 0
    raise ValueError(name)

def cast(o, D, prims, step_x=None, glass=False):
    """Primo impatto dei raggi D (N,3) dall'origine o. Ritorna t, id."""
    n = D.shape[0]
    t = np.full(n, np.inf); ids = np.zeros(n, int)
    dx, dy, dz = D[:, 0], D[:, 1], D[:, 2]
    with np.errstate(divide="ignore", invalid="ignore"):
        # pavimento (eventuale gradino in discesa)
        tf = np.where(dz < 0, (0 - o[2]) / dz, np.inf)
        if step_x is not None:
            xf = o[0] + tf * dx
            low = xf >= step_x
            tf = np.where(low, (-STEP_DROP - o[2]) / dz, tf)
            idf = np.where(low, ID_LOWFLOOR, ID_FLOOR)
        else:
            idf = np.full(n, ID_FLOOR)
        m = tf < t; t[m] = tf[m]; ids[m] = idf[m]
        tc = np.where(dz > 0, (Z_CEIL - o[2]) / dz, np.inf)
        m = tc < t; t[m] = tc[m]; ids[m] = ID_CEIL
        for s in (Y_WALL, -Y_WALL):
            tw = (s - o[1]) / dy
            tw = np.where(tw > 0, tw, np.inf)
            m = tw < t; t[m] = tw[m]; ids[m] = ID_WALL
        for kind, a, b, ident in prims:
            if (ident == ID_GLASS) != glass:
                continue
            if kind == "box":
                t1 = (a[None, :] - o[None, :]) / D
                t2 = (b[None, :] - o[None, :]) / D
                tmin = np.nanmax(np.minimum(t1, t2), axis=1)
                tmax = np.nanmin(np.maximum(t1, t2), axis=1)
                hit = (tmax >= tmin) & (tmax > 0)
                th = np.where(hit, np.maximum(tmin, 0), np.inf)
            else:
                cx, cy, r, z0, z1 = a
                ox, oy = o[0] - cx, o[1] - cy
                A = dx * dx + dy * dy
                B = 2 * (dx * ox + dy * oy)
                C = ox * ox + oy * oy - r * r
                disc = B * B - 4 * A * C
                ts = (-B - np.sqrt(np.maximum(disc, 0))) / (2 * A)
                zz = o[2] + ts * dz
                th = np.where((disc >= 0) & (ts > 0) & (zz >= z0) & (zz <= z1), ts, np.inf)
                # tappo superiore
                ttop = (z1 - o[2]) / dz
                xt, yt = ox + ttop * dx, oy + ttop * dy
                okt = (ttop > 0) & (xt * xt + yt * yt <= r * r)
                th = np.minimum(th, np.where(okt, ttop, np.inf))
            m = th < t; t[m] = th[m]; ids[m] = ident
    return t, ids

def rot(D, el_deg, az_deg):
    e, a = math.radians(el_deg), math.radians(az_deg)
    x, y, z = D[:, 0], D[:, 1], D[:, 2]
    x1 = x * math.cos(e) - z * math.sin(e); z1 = x * math.sin(e) + z * math.cos(e)
    x2 = x1 * math.cos(a) - y * math.sin(a); y2 = x1 * math.sin(a) + y * math.cos(a)
    return np.stack([x2, y2, z1], 1)

def cone_rays(half_deg, n):
    i = np.arange(n) + .5
    ct = 1 - (1 - math.cos(math.radians(half_deg))) * i / n
    st = np.sqrt(1 - ct * ct); ph = i * math.pi * (3 - math.sqrt(5))
    return np.stack([ct, st * np.cos(ph), st * np.sin(ph)], 1)

FLOOR_FIT = True       # stima del pavimento nella nuvola di punti della camera
CAM_H, CAM_V, CAM_STEP = 73.0, 58.0, 0.75
_h = np.radians(np.arange(-CAM_H / 2, CAM_H / 2 + 1e-6, CAM_STEP))
_v = np.radians(np.arange(-CAM_V / 2, CAM_V / 2 + 1e-6, CAM_STEP))
HH, VV = np.meshgrid(_h, _v)
CAM_RAYS = np.stack([np.ones(HH.size), np.tan(HH).ravel(), np.tan(VV).ravel()], 1)
CAM_RAYS /= np.linalg.norm(CAM_RAYS, axis=1)[:, None]

# --------------------------------------------------------------------------
# Sensori
# --------------------------------------------------------------------------
class ToF:
    def __init__(s, name, el, az, half, n, rmax, rsun, rate, lat, kind):
        s.name, s.el, s.az, s.half = name, el, az, half
        s.rays = cone_rays(half, n); s.rmax, s.rsun = rmax, rsun
        s.rate, s.lat, s.kind = rate, lat, kind
        s.baseline = None

    def measure(s, o, pitch, sc, rng):
        D = rot(s.rays, s.el - pitch, s.az)
        t, ids = cast(o, D, sc["prims"], sc["step_x"])
        tg, _ = cast(o, D, sc["prims"], sc["step_x"], glass=True)
        gl = tg < t
        rmax = s.rsun if sc["sun"] else s.rmax
        thr = .88 / rmax ** 2
        groups = []
        n = len(t)
        for g in np.unique(ids[np.isfinite(t)]):
            m = (ids == g) & np.isfinite(t)
            d = np.percentile(t[m], 20); fill = m.sum() / n
            groups.append((d, fill, sc["refl"].get(int(g), .3), int(g)))
        if gl.any() and rng.random() < .40:          # vetro: riflesso intermittente
            groups.append((np.percentile(tg[gl], 20), gl.sum() / n, .10, ID_GLASS))
        best = None
        for d, fill, refl, g in groups:
            if refl * fill / d ** 2 >= thr and (best is None or d < best[0]):
                best = (d, g, refl)
        if best is None:
            return None
        d, g, refl = best
        sig = (.005 + .01 * d) * (2 if sc["sun"] else 1) * (1.5 if refl < .2 else 1)
        return (max(d + rng.normal(0, sig), .01), g)

class Luna(ToF):
    def measure(s, o, pitch, sc, rng):
        D = rot(np.array([[1.0, 0, 0]]), s.el - pitch, 0)
        t, ids = cast(o, D, sc["prims"], sc["step_x"])
        g = int(ids[0]); refl = sc["refl"].get(g, .3)
        sig = .05 if refl < .1 else .03
        return (t[0] + rng.normal(0, sig), g)

def camera_measure(o, pitch_true, pitch_est, sc, rng):
    """Profondità OAK-D Lite: cluster di punti nella fascia di passaggio."""
    if rng.random() < .02:                          # frame perso
        return None
    D = rot(CAM_RAYS, -pitch_true, 0)
    t, ids = cast(o, D, sc["prims"], sc["step_x"])  # il vetro non dà profondità
    axis = rot(np.array([[1.0, 0, 0]]), -pitch_true, 0)[0]
    depth = t * (D @ axis)
    ok = np.isfinite(depth) & (depth >= .40) & (depth <= 3.0)
    if not ok.any():
        return None
    dn = depth[ok] + rng.normal(0, .01 * depth[ok] ** 2 + .003)
    Dc = rot(CAM_RAYS[ok], -pitch_est, 0)            # ricostruzione con IMU
    tr = dn / (Dc @ rot(np.array([[1.0, 0, 0]]), -pitch_est, 0)[0])
    P = Dc * tr[:, None]
    z = H_SENS + P[:, 2]; y = P[:, 1]; xh = P[:, 0]
    zmin = BAND_Z[0]
    if FLOOR_FIT:
        # stima del piano del pavimento a ogni frame (minimi quadrati sui punti bassi):
        # toglie l'errore di beccheggio dell'IMU e il rimbalzo del passo
        fl = (np.abs(z) < .15) & (xh < 3.0)
        if fl.sum() > 50:
            A = np.stack([xh[fl], y[fl], np.ones(fl.sum())], 1)
            coef, *_ = np.linalg.lstsq(A, z[fl], rcond=None)
            z = z - (coef[0] * xh + coef[1] * y + coef[2])
        zmin = .10 + .02 * xh                         # soglia che cresce col rumore
    sel = (z > zmin) & (z < BAND_Z[1]) & (np.abs(y) < BAND_Y)
    if sel.sum() < 6:
        return None
    xb = np.floor(xh[sel] / .2).astype(int)
    yb = np.floor(y[sel] / .2).astype(int)
    idsel = ids[ok][sel]; zs = z[sel]; xs = xh[sel]
    keys = xb * 100 + yb
    best = None
    for k in np.unique(keys):
        m = keys == k
        if m.sum() >= 6:
            d = xs[m].min()
            if best is None or d < best[0]:
                vals, cnt = np.unique(idsel[m], return_counts=True)
                best = (d, int(vals[cnt.argmax()]), float(np.median(zs[m])))
    if best is None:
        return None
    n_obs = int(((ids == ID_OBS) & ok).sum())
    return best + (n_obs,)

def build_sensors(with_camera=True):
    S = [ToF("MD alto sx", 45, 15, 9, 120, 1.2, .8, 30, .035, "md"),
         ToF("MD alto dx", 45, -15, 9, 120, 1.2, .8, 30, .035, "md"),
         ToF("MD basso sx", -45, 15, 9, 120, 1.2, .8, 30, .035, "md"),
         ToF("MD basso dx", -45, -15, 9, 120, 1.2, .8, 30, .035, "md"),
         ToF("VL alto +22", 22, 0, 13.5, 200, 3.6, 1.3, 20, .05, "vl"),
         ToF("VL dritto", 0, 0, 13.5, 200, 3.6, 1.3, 20, .05, "vl"),
         ToF("VL basso -30", -30, 0, 13.5, 200, 3.6, 1.3, 20, .05, "vlb"),
         Luna("TF-Luna", -41, 0, 1, 1, 8, 8, 100, .01, "luna")]
    # taratura a pavimento del VL puntato in basso (tabella in funzione del beccheggio)
    vb = S[6]; tab = {}
    rng = np.random.default_rng(0)
    sc = scene("vuoto", 0)
    for p in np.arange(-10, 10.01, .5):
        vals = [vb.measure(np.array([0, 0, H_SENS]), p, sc, rng) for _ in range(5)]
        vals = [v[0] for v in vals if v]
        tab[round(p * 2) / 2] = np.median(vals) if vals else None
    vb.baseline = tab
    return S, with_camera

def scene(name, yo, sun=False, dark=False):
    prims, refl, label, offs = make_obstacle(name, yo)
    return {"prims": prims, "sun": sun, "dark": dark, "label": label,
            "offset": offs, "name": name,
            "step_x": OBST_START if name == "gradino discesa" else None,
            "obs_x": OBST_START,
            "refl": {ID_FLOOR: .06 if dark else .30, ID_LOWFLOOR: .06 if dark else .30,
                     ID_CEIL: .80, ID_WALL: .70, ID_OBS: refl, ID_GLASS: .10}}

# --------------------------------------------------------------------------
# Decisione (lato Linux della UNO Q)
# --------------------------------------------------------------------------
def d_stop(v):
    """Distanza a cui serve l'allarme STOP: latenza+reazione (95%), frenata, margine."""
    return v * (0.10 + 0.95) + v * v / (2 * 1.5) + 0.35 + 0.15

def classify(cands, v_est, step):
    """Livello d'allarme: 2 = STOP (vibrazione continua), 1 = attenzione, 0 = nulla."""
    if step:
        return 2
    if not cands:
        return 0
    dmin = min(c["dh"] for c in cands)
    if dmin <= d_stop(v_est):
        return 2
    if dmin <= max(2.5, 3.0 * v_est):
        return 1
    return 0

def phrase(c):
    if c.get("step"):
        return "Gradino in discesa"
    d = max(.5, round(c["dh"] * 2) / 2)
    ds = f"{d:.1f}".replace(".", ",").replace(",0", "")
    ds += " metro" if d == 1 else " metri"
    if c.get("label"):
        return f"{c['label'].capitalize()} a {ds}"
    if c["z"] > 1.6:
        return f"Ostacolo in alto a {ds}"
    if c["z"] < .6:
        return f"Ostacolo in basso a {ds}"
    return f"Ostacolo davanti a {ds}"

# --------------------------------------------------------------------------
# Una prova
# --------------------------------------------------------------------------
def run_trial(sensors, with_cam, sc, v, rng, log=None, length=None):
    dt = .02
    yo_bias = rng.normal(0, .5); dr = rng.normal(0, .04)          # bias IMU, deriva passi
    f_step = 1.8 * math.sqrt(v); ph = rng.uniform(0, 2 * math.pi)
    v_est = v * (1 + rng.normal(0, .08))
    x = 0.0; t = 0.0
    nxt = {s.name: rng.uniform(0, 1 / s.rate) for s in sensors}
    nxt["cam"] = rng.uniform(0, 1 / 15)
    queue = []; latest = {}; consec = {}; memory = []
    first_det = {}; l1_done = False; suppressed = set(); n_fa = 0
    events = []
    obs_x = sc["obs_x"]; contact = obs_x - sc["offset"]
    end_x = length if length else contact + .01
    is_empty = sc["name"] == "vuoto"
    def L(msg):
        if log is not None:
            events.append((t, x, msg))
    while x < end_x:
        pitch = 4 * math.sin(2 * math.pi * f_step * t + ph)
        pitch_est = pitch + yo_bias + rng.normal(0, .5)
        h = H_SENS + .02 * math.sin(4 * math.pi * f_step * t + ph)
        o = np.array([x, 0, h])
        if is_empty and length:                      # zone di disturbo nel corridoio vuoto
            sc["sun"] = 5 <= x < 10; sc["dark"] = 12 <= x < 18
            sc["refl"][ID_FLOOR] = .06 if sc["dark"] else .30
        for s in sensors:
            if t >= nxt[s.name]:
                nxt[s.name] += 1 / s.rate
                queue.append((t + s.lat, s.name, s.measure(o, pitch, sc, rng), pitch_est))
        if with_cam and t >= nxt["cam"]:
            nxt["cam"] += 1 / 15
            queue.append((t + .09, "cam", camera_measure(o, pitch, pitch_est, sc, rng), pitch_est))
        fresh = {}
        for q in [q for q in queue if q[0] <= t]:
            fresh[q[1]] = (q[2], q[3]); queue.remove(q)
        x_est = x * (1 + dr)
        cands = []; step = None
        for s in sensors + ([None] if with_cam else []):
            name = s.name if s else "cam"
            if name in fresh:
                r, pe = fresh[name]; c = None
                if r is not None:
                    if name == "cam":
                        d, tag, z, n_obs = r
                        lab = sc["label"] if tag >= ID_OBS and n_obs >= 40 else None
                        c = {"dh": d, "z": z, "tag": tag, "label": lab}
                    elif s.kind == "luna":
                        d, tag = r
                        ang = math.radians(s.el - pe)
                        z = H_SENS + d * math.sin(ang); dh = d * math.cos(ang)
                        if z < -.08:
                            c = {"dh": dh, "z": z, "tag": tag, "step": True}
                        elif z > BAND_Z[0]:
                            c = {"dh": dh, "z": z, "tag": tag}
                    elif s.kind == "vlb":
                        d, tag = r
                        base = s.baseline.get(round(pe * 2) / 2)
                        if base and d < base - .30:
                            c = {"dh": d * math.cos(math.radians(30 - pe)), "z": .3, "tag": tag}
                    else:
                        d, tag = r
                        ang = math.radians(s.el - pe)
                        z = H_SENS + d * math.sin(ang)
                        dh = d * math.cos(ang) * math.cos(math.radians(s.az))
                        y = d * math.cos(ang) * math.sin(math.radians(s.az))
                        if BAND_Z[0] < z < BAND_Z[1] and abs(y) < BAND_Y:
                            c = {"dh": dh, "z": z, "tag": tag}
                need = 3 if (s and s.kind == "luna") else 2
                if c and c["tag"] not in suppressed:
                    consec[name] = consec.get(name, 0) + 1
                    if consec[name] >= need:
                        c["src"] = name; latest[name] = c
                        if c["tag"] >= ID_OBS and name not in first_det:
                            first_det[name] = obs_x - x
                            L(f"rileva: {name:<13} distanza reale {obs_x - x:4.2f} m")
                        if not c.get("step"):
                            memory.append({**c, "xw": x_est + c["dh"], "t": t})
                    else:
                        latest.pop(name, None)
                else:
                    consec[name] = 0; latest.pop(name, None)
        for c in latest.values():
            if c.get("step"):
                step = c
            else:
                cands.append(c)
        memory = [m for m in memory if t - m["t"] < 10 and m["tag"] not in suppressed]
        for m in memory:
            dh = m["xw"] - x_est
            if dh > 0:
                cands.append({**m, "dh": dh, "src": m["src"] + " (memoria)"})
        lvl = classify(cands, v_est, step)
        if lvl >= 1:
            top = step if step else min(cands, key=lambda c: c["dh"])
            if lvl == 1 and not l1_done:
                l1_done = True
                L(f"ALLARME 1 - impulso breve Vibro + voce in cuffia "
                  f"(arriva tra {rng.uniform(.25, .40):.2f} s): «{phrase(top)}» [fonte {top['src']}]")
            if lvl == 2:
                truth = top["tag"] >= ID_OBS
                if not truth:
                    n_fa += 1; suppressed.add(top["tag"])
                    L(f"FALSO ALLARME STOP da {top['src']} (lettura di {['', 'pavimento', 'soffitto', 'parete'][top['tag']] if top['tag'] < 4 else '?'}): "
                      "la persona si ferma e riparte")
                    latest.clear(); consec.clear(); memory = []
                    if is_empty:
                        suppressed.discard(top["tag"])
                else:
                    rt = float(np.clip(rng.normal(.65, .18), .35, 1.5))
                    a = float(np.clip(rng.normal(1.6, .3), .9, 2.5))
                    x_stop = x + v * (.03 + rt) + v * v / (2 * a)
                    clear = contact - x_stop
                    L(f"ALLARME 2 - STOP: vibrazione continua sx+dx, buzzer; "
                      f"«{phrase(top)}» [fonte {top['src']}]")
                    L(f"reazione {rt:.2f} s, frenata {a:.1f} m/s² → si ferma a "
                      f"{obs_x - x_stop:4.2f} m dall'ostacolo, margine {clear:+.2f} m "
                      f"→ {'OK' if clear >= 0 else 'CONTATTO'}")
                    return {"ok": clear >= 0, "clear": clear, "first": first_det,
                            "trig": obs_x - x, "src": top["src"], "fa": n_fa,
                            "events": events, "time": t}
        x += v * dt; t += dt
    if is_empty:
        return {"fa": n_fa, "time": t, "events": events}
    L("NESSUN ALLARME STOP in tempo → CONTATTO con l'ostacolo")
    return {"ok": False, "clear": None, "first": first_det, "trig": None,
            "src": None, "fa": n_fa, "events": events, "time": t}

TRIALS = [("persona", {}), ("sedia", {"sun": True}), ("cartello testa", {}),
          ("bordo tavolo", {}), ("palo sottile", {"sun": True}),
          ("paletto basso", {"dark": True}), ("zaino a terra", {}),
          ("vetrata", {}), ("gradino discesa", {"dark": True}), ("muro", {})]

POWER = {"UNO Q (Linux + App Lab)": 3.0, "OAK-D Lite (profondità + IA)": 3.5,
         "4 Modulino Distance": 4 * .06, "3 VL53L1X": 3 * .06, "TF-Luna": .35,
         "Movement, Buttons, Buzzer, Hub": .08, "Bluetooth audio": .15,
         "2 Vibro (media in uso)": .05}

def mc_job(job):
    cam, v, i, n = job
    name, fl = TRIALS[i]
    rng = np.random.default_rng(1000 + 100 * i + int(v * 10) + (0 if cam else 5000))
    SA, _ = build_sensors()
    R = [run_trial(SA, cam, scene(name, rng.uniform(-.25, .25), **fl), v, rng) for _ in range(n)]
    ok = float(np.mean([r["ok"] for r in R]))
    cl = [r["clear"] for r in R if r["clear"] is not None]
    tr = [r["trig"] for r in R if r["trig"] is not None]
    srcs = {}
    for r in R:
        if r["src"]:
            k = r["src"].replace(" (memoria)", "*")
            srcs[k] = srcs.get(k, 0) + 1
    src = max(srcs, key=srcs.get) if srcs else "-"
    fa = float(np.mean([r["fa"] for r in R]))
    return (cam, v, name, ok, float(np.median(cl)) if cl else None,
            float(np.median(tr)) if tr else None, src, fa)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--n", type=int, default=100)
    ap.add_argument("--out", default="out"); a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    rng = np.random.default_rng(2026)
    SA, _ = build_sensors()

    # --- 1. registro dettagliato: percorso completo a 1,0 m/s, con e senza camera
    for cam, tag in ((True, "A_con_camera"), (False, "B_senza_camera")):
        lines = [f"CBH - registro del test simulato - configurazione {tag} - 1,0 m/s", ""]
        tt = 0.0; rr = np.random.default_rng(7)
        for i, (name, fl) in enumerate(TRIALS, 1):
            yo = rr.uniform(-.25, .25)
            sc = scene(name, yo, **fl)
            dist = ", ".join(k for k, v in fl.items() if v) or "nessuno"
            lines.append(f"=== Prova {i}: {name}  (spostato {yo:+.2f} m dal centro; disturbi: "
                         f"{'sole' if fl.get('sun') else 'pavimento scuro' if fl.get('dark') else 'nessuno'})")
            r = run_trial(SA, cam, sc, 1.0, rr, log=True)
            for t, x, msg in r["events"]:
                lines.append(f"  t={tt + t:6.2f} s  pos {x:4.2f} m  {msg}")
            tt += r["time"] + 4.0
            lines.append("")
        open(f"{a.out}/registro_{tag}.txt", "w").write("\n".join(lines))
        print("\n".join(lines))

    # --- 2. Monte Carlo (in parallelo)
    from multiprocessing import Pool
    jobs = [(cam, v, i, a.n) for cam in (True, False) for v in (0.6, 1.0, 1.4)
            for i in range(len(TRIALS))]
    with Pool() as pool:
        rows = pool.map(mc_job, jobs)
    for cam, v, name, ok, cl, tr, src, fa in rows:
        print(f"{'A' if cam else 'B'} v={v} {name:<16} ok={ok:4.0%} "
              f"margine={cl if cl is not None else float('nan'):+.2f} "
              f"allarme a={tr if tr is not None else float('nan'):.2f} fonte={src} fa={fa:.2f}")
    # --- 3. corridoio vuoto (20 m, sole 5-10 m, pavimento scuro 12-18 m)
    fa_rows = []
    for cam in (True, False):
        for v in (0.6, 1.0, 1.4):
            tot_fa = 0; tot_t = 0
            for _ in range(max(10, a.n // 5)):
                r = run_trial(SA, cam, scene("vuoto", 0), v, rng, length=20.0)
                tot_fa += r["fa"]; tot_t += r["time"]
            fa_rows.append((cam, v, tot_fa / (tot_t / 60)))
            print(f"vuoto {'A' if cam else 'B'} v={v}: {tot_fa / (tot_t / 60):.2f} falsi STOP/min")
    # --- 4. energia
    pA = sum(POWER.values()) / .90
    pB = (sum(POWER.values()) - POWER["OAK-D Lite (profondità + IA)"]) / .90
    wh = 20 * 3.6 * .85
    # salva CSV
    with open(f"{a.out}/risultati_montecarlo.csv", "w") as f:
        f.write("config,velocita,ostacolo,successo,margine_mediano_m,allarme_stop_a_m,fonte_principale,falsi_allarmi_per_prova\n")
        for cam, v, name, ok, cl, tr, src, fa in rows:
            f.write(f"{'A' if cam else 'B'},{v},{name},{ok:.3f},{'' if cl is None else f'{cl:.2f}'},"
                    f"{'' if tr is None else f'{tr:.2f}'},{src},{fa:.3f}\n")
    with open(f"{a.out}/falsi_allarmi_corridoio_vuoto.csv", "w") as f:
        f.write("config,velocita,falsi_stop_al_minuto\n")
        for cam, v, x in fa_rows:
            f.write(f"{'A' if cam else 'B'},{v},{x:.2f}\n")
    print(f"Potenza A {pA:.1f} W → {wh / pA:.1f} h; B {pB:.1f} W → {wh / pB:.1f} h")

if __name__ == "__main__":
    main()
