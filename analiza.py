#!/usr/bin/env python3
"""Precalculador de catalogo: lee STL binarios/ASCII y emite la ficha de cada
producto (material, tiempo, caja, encaje en bandeja) con las mismas formulas
que usaba el presupuestador original."""
import struct, math, json, sys, os

PERIMS, LINEW, INFILL, LAYERH = 2, 0.42, 0.18, 0.2
DENSITY, FLOW = 1.24, 5.0
THR, SUPDENS = 45, 0.12
BED = (180, 180, 180)

def leer(path):
    b = open(path, 'rb').read()
    tris = []
    if len(b) >= 84:
        n = struct.unpack('<I', b[80:84])[0]
        if 84 + n*50 == len(b):
            uf = struct.Struct('<12fH').unpack_from
            for i in range(n):
                d = uf(b, 84 + i*50)
                tris.append(d[3:12])
            return tris
    import re
    txt = b.decode('utf-8', 'replace')
    vs = re.findall(r'vertex\s+(-?[\d.eE+-]+)\s+(-?[\d.eE+-]+)\s+(-?[\d.eE+-]+)', txt)
    for i in range(0, len(vs)-2, 3):
        tris.append(tuple(float(c) for p in vs[i:i+3] for c in p))
    return tris

def medir(tris, sinthr):
    vol = area = ohA = ohM = 0.0
    mn = [1e30]*3; mx = [-1e30]*3
    for (ax,ay,az,bx,by,bz,cx,cy,cz) in tris:
        vol += (ax*(by*cz-bz*cy) - ay*(bx*cz-bz*cx) + az*(bx*cy-by*cx))/6
        ux,uy,uz = bx-ax, by-ay, bz-az
        vx,vy,vz = cx-ax, cy-ay, cz-az
        nx,ny,nz = uy*vz-uz*vy, uz*vx-ux*vz, ux*vy-uy*vx
        mag = math.sqrt(nx*nx+ny*ny+nz*nz); a = mag/2; area += a
        if mag > 1e-12:
            nzu = nz/mag
            if nzu < -sinthr:
                proj = abs(nzu)*a; ohA += proj; ohM += proj*(az+bz+cz)/3
        for (X,Y,Z) in ((ax,ay,az),(bx,by,bz),(cx,cy,cz)):
            mn[0]=min(mn[0],X); mx[0]=max(mx[0],X)
            mn[1]=min(mn[1],Y); mx[1]=max(mx[1],Y)
            mn[2]=min(mn[2],Z); mx[2]=max(mx[2],Z)
    return dict(vol=abs(vol), area=area, ohA=ohA,
                sup=max(0, ohM - mn[2]*ohA),
                size=[mx[i]-mn[i] for i in range(3)], tris=len(tris))

def componentes(tris):
    par = {}
    def find(x):
        r = x
        while par[r] != r: r = par[r]
        while par[x] != r: par[x], x = r, par[x]
        return r
    def uni(a, b):
        ra, rb = find(a), find(b)
        if ra != rb: par[ra] = rb
    Q = lambda v: round(v*100)
    keys = []
    for t in tris:
        vs = [(Q(t[0]),Q(t[1]),Q(t[2])),(Q(t[3]),Q(t[4]),Q(t[5])),(Q(t[6]),Q(t[7]),Q(t[8]))]
        for v in vs: par.setdefault(v, v)
        uni(vs[0], vs[1]); uni(vs[1], vs[2])
        keys.append(vs[0])
    g = {}
    for i, k in enumerate(keys): g.setdefault(find(k), []).append(i)
    return list(g.values())

def encaje(size, bed):
    import itertools
    for p in itertools.permutations(range(3)):
        if all(size[p[i]] <= bed[i] for i in range(3)):
            return "ok" if p == (0,1,2) else "girado"
    return "no"

def ficha(path):
    tris = leer(path)
    m = medir(tris, math.sin(math.radians(THR)))
    wall = PERIMS*LINEW
    shell = min(m['area']*wall, m['vol'])
    core = max(0, m['vol'] - shell)
    body = shell + core*INFILL
    sup = m['sup']*SUPDENS
    total = body + sup
    comps = componentes(tris)
    return dict(
        archivo=os.path.basename(path), tris=m['tris'], piezas=len(comps),
        caja_mm=[round(x,2) for x in m['size']],
        encaje=encaje(m['size'], BED),
        volumen_cm3=round(m['vol']/1000, 2),
        area_cm2=round(m['area']/100, 1),
        solido=round(shell/m['vol']*100, 1),
        voladizo_cm2=round(m['ohA']/100, 1),
        soporte_g=round(sup/1000*DENSITY, 2),
        gramos=round(total/1000*DENSITY, 1),
        horas=round(total/FLOW/3600, 2),
        capas=math.ceil(m['size'][2]/LAYERH),
    )

if __name__ == '__main__':
    out = [ficha(p) for p in sys.argv[1:]]
    print(json.dumps(out, indent=2, ensure_ascii=False))
