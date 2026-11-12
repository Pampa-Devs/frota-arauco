import json, math
LON0,LON1,LAT0,LAT1=-52.62,-51.55,-20.42,-19.42
C=math.cos(math.radians((LAT0+LAT1)/2)); K=1000/((LON1-LON0)*C)
W=1000; H=round((LAT1-LAT0)*K)
X=lambda lon:(lon-LON0)*C*K; Y=lambda lat:(LAT1-lat)*K
def path(coords, close=False):
    return "M"+" L".join(f"{X(a):.1f},{Y(b):.1f}" for a,b in coords)+("Z" if close else "")
def inb(c,pad=0.3): return LON0-pad<=c[0]<=LON1+pad and LAT0-pad<=c[1]<=LAT1+pad
m=json.load(open("geojs-50-mun.json"))
mun=[]
for f in m["features"]:
    g=f["geometry"]; rs=[g["coordinates"][0]] if g["type"]=="Polygon" else [p[0] for p in g["coordinates"]]
    for r in rs:
        if any(inb(c,0) for c in r): mun.append(path(r,True))
def lines(g): return [g["coordinates"]] if g["type"]=="LineString" else g["coordinates"]
roads=[path(l) for f in json.load(open("ne_10m_roads.geojson"))["features"] for l in lines(f["geometry"]) if any(inb(c,0.05) for c in l)]
rivers=[{"n":f["properties"].get("name"),"d":path(l)} for f in json.load(open("ne_10m_rivers_lake_centerlines.geojson"))["features"] for l in lines(f["geometry"]) if any(inb(c,0.05) for c in l)]
P={f["properties"]["name"]:f["geometry"] for f in m["features"]}
def rings(n):
    g=P[n]; return [g["coordinates"][0]] if g["type"]=="Polygon" else [p[0] for p in g["coordinates"]]
def shared(a,b):
    S=set(tuple(c) for r in rings(b) for c in r); return [c for r in rings(a) for c in r if tuple(c) in S]
suc=list(reversed(shared("Inocência","Três Lagoas")))+list(reversed(shared("Selvíria","Três Lagoas")))
json.dump({"W":W,"H":H,"LON0":LON0,"LAT1":LAT1,"C":C,"K":K,"kmPerUnit":110.6/K,"mun":mun,"roads":roads,"rivers":rivers,"sucuriu":path(suc)},open("geo.json","w"))
print(W,H,len(roads),[r["n"] for r in rivers])
