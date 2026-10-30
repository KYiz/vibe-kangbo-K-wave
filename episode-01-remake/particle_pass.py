"""Add deterministic, content-anchored particles to the selected v3 film."""
from pathlib import Path
import random

path = Path(__file__).parent / 'compositions' / 'film.html'
source = path.read_text(encoding='utf-8')
if 'id="particle-layer"' in source:
    raise SystemExit('Particle pass already present; restore v3 before reapplying.')

# Each burst is attached to an on-screen cause. Screen coordinates use the
# existing 1080x1920 composition, and the labels remain outside their travel.
bursts = [
    ('letter-a-dust', 1.25, (300, 920), 26, '#e9d7b2', 200, 150, 'dust'),
    ('letter-b-dust', 1.70, (760, 940), 26, '#cda277', 180, 150, 'dust'),
    ('machine-fault', 12.45, (380, 695), 38, '#d88977', 230, 190, 'spark'),
    ('ruler-split', 38.25, (540, 1010), 52, '#edcf92', 320, 235, 'spark'),
    ('formula-fracture', 93.84, (540, 960), 104, '#e7cc98', 440, 325, 'shard'),
    ('final-path', 130.85, (540, 1250), 34, '#b7c9be', 300, 145, 'dust'),
]

rng = random.Random(20261030)
groups = []
timings = []
for name,t,(cx,cy),count,color,spread_x,spread_y,kind in bursts:
    nodes = []
    for i in range(count):
        angle = rng.random() * 6.283185307
        radius = .25 + rng.random() * .75
        dx = int(__import__('math').cos(angle) * spread_x * radius)
        dy = int(__import__('math').sin(angle) * spread_y * radius)
        size = rng.randint(4,10) if kind == 'dust' else rng.randint(7,16)
        if kind == 'shard': size = rng.randint(11,29)
        delay = round(rng.random() * .095,3)
        rotation = rng.randint(-180,180)
        particle_color = rng.choice(['#fff0cf','#bf8857','#6e4738']) if kind == 'shard' else color
        nodes.append(f'<i class="particle {kind}" style="left:{cx}px;top:{cy}px;width:{size}px;height:{max(3,size//3) if kind != "dust" else size}px;background:{particle_color}" data-dx="{dx}" data-dy="{dy}" data-delay="{delay}" data-rotation="{rotation}"></i>')
    groups.append(f'<div class="particle-group" id="{name}">{"".join(nodes)}</div>')
    timings.append((name,t))

css = '''
#particle-layer{position:absolute;inset:0;z-index:8;pointer-events:none;overflow:hidden}
.particle-group{position:absolute;inset:0}
.particle{position:absolute;display:block;opacity:0;transform-origin:center center;will-change:transform,opacity}
.particle.dust{border-radius:50%;box-shadow:0 0 14px #e4c89799}
.particle.spark{border-radius:3px;box-shadow:0 0 18px #e4b675aa}
.particle.shard{border-radius:2px;box-shadow:0 0 12px #e7cc98aa}
'''
markup = '<div id="particle-layer" data-layout-ignore>' + ''.join(groups) + '</div>'
script = '''
function particleBurst(id,t){
 document.querySelectorAll('#'+id+' .particle').forEach(p=>{
  const dx=+p.dataset.dx,dy=+p.dataset.dy,d=+p.dataset.delay,r=+p.dataset.rotation;
  const large=p.classList.contains('shard');
  tl.fromTo(p,{opacity:0,x:0,y:0,scale:.35,rotation:0},{opacity:large?.95:.82,x:dx*.54,y:dy*.54,scale:1,rotation:r*.3,duration:.19,ease:'power3.out'},t+d)
    .to(p,{opacity:0,x:dx,y:dy+(large?72:42),scale:large?.7:.18,rotation:r,duration:large?.57:.46,ease:'power2.in'},t+d+.19);
 });
}
'''
for name,t in timings:
    script += f"particleBurst('{name}',{t});\n"

assert source.count('</style>') == 1
assert source.count('<div id="transition-flash"') == 1
assert source.count('window.__timelines.film=tl;') == 1
source = source.replace('</style>',css+'</style>',1)
source = source.replace('<div id="transition-flash"',markup+'<div id="transition-flash"',1)
source = source.replace('window.__timelines.film=tl;',script+'window.__timelines.film=tl;',1)
path.write_text(source,encoding='utf-8')
print(f'Added {sum(x[3] for x in bursts)} particles in {len(bursts)} timed bursts to {path}')
