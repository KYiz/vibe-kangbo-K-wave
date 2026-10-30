"""Apply the 2026-10-30 visual pass to the original EP01 composition.

The source copy is kept beside this file so the pass is reproducible.
"""

from pathlib import Path
import re

project = Path(__file__).resolve().parent
source = project / "compositions" / "film.pre-visual.html.bak"
target = project / "compositions" / "film.html"
html = source.read_text(encoding="utf-8")

def replace_once(old: str, new: str) -> None:
    global html
    count = html.count(old)
    if count != 1:
        raise RuntimeError(f"Expected one match, found {count}: {old[:90]}")
    html = html.replace(old, new, 1)


# The four observed crossings are solved in the composition, not covered by a mask.
replace_once(
    '<circle cx="690" cy="203" r="35" fill="#d1ab72"/></g><g id="letter-a">',
    '<circle cx="690" cy="203" r="35" fill="#d1ab72"/><path d="M390 223H610" stroke="#b3a487" stroke-width="3"/></g><g id="letter-a">',
)
replace_once(
    '<text x="225" y="585" fill="#3d6e68" font-size="53" font-weight="700" font-family="Hive">录用</text></g><g id="letter-b">',
    '<text x="225" y="585" fill="#3d6e68" font-size="53" font-weight="700" font-family="Hive">录用</text><path d="M158 650H435M158 668H322" stroke="#9d9b8f" stroke-width="4"/></g><g id="letter-b">',
)
replace_once(
    '<text x="700" y="585" fill="#8f4b43" font-size="53" font-weight="700" font-family="Hive">缩招</text></g><g id="s1-question">',
    '<text x="700" y="585" fill="#8f4b43" font-size="53" font-weight="700" font-family="Hive">缩招</text><path d="M633 650H910M633 668H800" stroke="#a59a8c" stroke-width="4"/></g><g id="s1-question">',
)
replace_once(
    '<text x="235" y="900" fill="#c97565" font-size="48" font-family="Hive" font-weight="700">行业 A</text><text x="752" y="900" fill="#9bbab6" font-size="48" font-family="Hive" font-weight="700">行业 B</text>',
    '<text x="235" y="900" fill="#c97565" font-size="48" font-family="Hive" font-weight="700" id="s5-label-a">行业 A</text><text x="752" y="900" fill="#9bbab6" font-size="48" font-family="Hive" font-weight="700" id="s5-label-b">行业 B</text>',
)
# Keep the labels hidden until the shop fronts have reached their final position.
replace_once(
    "tl.fromTo('#s5-drops',{opacity:0,y:-200}",
    "tl.fromTo('#s5-label-a,#s5-label-b',{opacity:0},{opacity:1,duration:.28},27.05);tl.fromTo('#s5-drops',{opacity:0,y:-200}",
)
replace_once(
    "tl.fromTo('#s6-ruler',{y:260,rotation:7,transformOrigin:'50% 50%'},{y:0,rotation:0,duration:.65,ease:'power3.out'},36.6)",
    "tl.fromTo('#s6-ruler',{y:-180,rotation:7,opacity:0,transformOrigin:'50% 50%'},{y:0,rotation:0,opacity:1,duration:.65,ease:'power3.out'},36.6)",
)
replace_once(
    '<g id="s12-stamp"><rect x="380" y="578" width="350" height="150" fill="none" stroke="#b35f54" stroke-width="15" transform="rotate(-8 555 653)"/><text x="440" y="670" fill="#b35f54" font-family="Hive" font-size="70" font-weight="700" transform="rotate(-8 555 653)">必然？</text></g>',
    '<g id="s12-stamp"><rect x="626" y="172" width="300" height="128" fill="none" stroke="#b35f54" stroke-width="11" transform="rotate(-8 776 236)"/><text x="661" y="263" fill="#b35f54" font-family="Hive" font-size="60" font-weight="700" transform="rotate(-8 776 236)">必然？</text></g>',
)
for card, angle, moment in (("a", "-10", "110.8"), ("b", "8", "112.55"), ("c", "-7", "114.25")):
    replace_once(
        f"tl.fromTo('#s15-card-{card}',{{y:-340,rotation:{angle},opacity:0,transformOrigin:'50% 50%'}},{{y:0,rotation:0,opacity:1,duration:.6,ease:'power4.out'}},{moment})",
        f"tl.fromTo('#s15-card-{card}',{{y:80,scale:.92,opacity:0,transformOrigin:'center bottom'}},{{y:0,scale:1,opacity:1,duration:.6,ease:'power4.out'}},{moment})",
    )

# Paper, pale inserts, metal, and dark boards receive distinct directional light.
paper = {"#e8decb", "#e7ddca", "#e6dac4", "#e5dccb", "#e3d9c6", "#d8d0bd", "#ddc79f", "#e7ddca"}
pale = {"#f1eadc", "#eee7d9", "#e7ddca", "#e3d9c6"}
metal = {"#c8a16b", "#b69568", "#d1ab72"}
dark = {"#2c3032", "#191d20"}

def materialize(match: re.Match[str]) -> str:
    segment = match.group(0)
    scene_id = re.search(r'id="(s\d+)"', segment).group(1)
    defs = (
        f'<defs>'
        f'<linearGradient id="paper-{scene_id}" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0" stop-color="#fff8e8"/><stop offset=".42" stop-color="#eadcc5"/>'
        '<stop offset="1" stop-color="#c9baa1"/></linearGradient>'
        f'<linearGradient id="pale-{scene_id}" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0" stop-color="#fffdf3"/><stop offset=".52" stop-color="#eee5d3"/>'
        '<stop offset="1" stop-color="#d8cab2"/></linearGradient>'
        f'<linearGradient id="metal-{scene_id}" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0" stop-color="#f2daa8"/><stop offset=".48" stop-color="#c69d65"/>'
        '<stop offset="1" stop-color="#85643d"/></linearGradient>'
        f'<linearGradient id="dark-{scene_id}" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0" stop-color="#40505a"/><stop offset=".52" stop-color="#253139"/>'
        '<stop offset="1" stop-color="#151e23"/></linearGradient>'
        '</defs>'
    )
    segment = re.sub(r'(<svg\b[^>]*>)', lambda m: m.group(1) + defs, segment, count=1)
    def refine_rect(m: re.Match[str]) -> str:
        rect = m.group(0)
        weights = {"7": "5", "8": "5", "9": "6", "10": "6", "13": "8", "15": "10"}
        return re.sub(r'stroke-width="(7|8|9|10|13|15)"', lambda s: f'stroke-width="{weights[s.group(1)]}"', rect)
    segment = re.sub(r'<rect\b[^>]*>', refine_rect, segment)
    def fill_repl(m: re.Match[str]) -> str:
        color = m.group(1).lower()
        if color in pale:
            material = "pale"
        elif color in paper:
            material = "paper"
        elif color in metal:
            material = "metal"
        elif color in dark:
            material = "dark"
        else:
            return m.group(0)
        return f'fill="url(#{material}-{scene_id})"'
    return re.sub(r'fill="(#[0-9A-Fa-f]{6})"', fill_repl, segment)

html, scene_count = re.subn(r'<section class="scene" id="s\d+"[\s\S]*?</section>', materialize, html)
if scene_count != 17:
    raise RuntimeError(f"Expected 17 scenes, got {scene_count}")

# A shared, restrained gallery light replaces the nearly flat charcoal stage.
style = r'''
/* Visual pass: tactile documentary objects inside a controlled pool of light. */
#root .scene{
  --lamp: 194 145 87;
  background:
    radial-gradient(ellipse 730px 810px at 63% 49%,rgb(var(--lamp) / .19),transparent 70%),
    radial-gradient(ellipse 610px 1000px at 10% 72%,rgb(94 142 151 / .13),transparent 74%),
    linear-gradient(153deg,#111c22 0%,#0d1419 40%,#0a1015 72%,#14191a 100%);
  box-shadow:inset 0 0 165px #02070aaa;
}
#root #s2,#root #s6,#root #s12,#root #s13,#root #s16{--lamp:211 154 88}
#root #s5,#root #s7,#root #s10,#root #s15{--lamp:114 162 153}
#root #s3,#root #s8,#root #s11,#root #s14{--lamp:168 130 117}
#root .scene:before{
  opacity:.46;
  background:
    linear-gradient(111deg,transparent 21%,rgb(240 222 181 / .045) 37%,transparent 53%),
    radial-gradient(ellipse 470px 850px at 80% 39%,rgb(255 226 167 / .09),transparent 76%),
    url('assets/grain.png') repeat;
  background-size:auto,auto,256px 256px;
  mix-blend-mode:screen;
  pointer-events:none;
}
#root .scene:after{
  height:2px;top:112px;
  background:linear-gradient(90deg,transparent,#d8b47caa 9%,#d8b47c44 55%,transparent);
}
#root .eyebrow{
  color:#c4d0c6;border-left:2px solid #d7b67d;
  text-shadow:0 2px 18px #071014;
}
#root .title{
  color:#f3ede0;font-weight:630;letter-spacing:0;
  text-shadow:0 3px 2px #0007,0 13px 35px #0009;
}
#root .title .gold{color:#edc990}
#root .title .red{color:#e19884}
#root .title .cyan{color:#b6d9ce}
#root .sub{
  color:#ddd7c9;border-top-color:#c5a57588;
  text-shadow:0 2px 20px #0009;
}
#root .scene svg{filter:drop-shadow(0 30px 22px #02070999)}
#root svg rect[fill^="url(#paper-"],#root svg rect[fill^="url(#pale-"]{
  filter:drop-shadow(0 13px 10px #06080755);
}
#root svg rect[stroke]{stroke-linejoin:round}
#root #s6-ruler{opacity:0}
#root #s5-label-a,#root #s5-label-b{opacity:0}
'''
replace_once('</style><div id="root"', style + '</style><div id="root"')

target.write_text(html, encoding="utf-8")
print(f"Wrote {target} with {scene_count} materialized scenes")
