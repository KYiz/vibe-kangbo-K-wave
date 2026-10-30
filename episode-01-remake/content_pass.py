"""Deepen the existing EP01 argument without changing its visual direction."""
from pathlib import Path
import html
import re

film = Path(__file__).parent / 'compositions' / 'film.html'
source = film.read_text(encoding='utf-8')
if 'class="sub-line"' in source:
    raise SystemExit('Content pass already applied; regenerate the selected v3 source first.')

# Two short steps per scene: a concrete observation, then its implication.
# The opening scene and the first theory setup stay shorter for reading time.
copy = {
  1: ['同届两封回信：一封录用，一封缩招。差别从哪里开始？'],
  2: ['康波是一种长期波动假说，不是按年份预言人生。'],
  3: ['把出生年份直接接到财富，', '中间跳过了行业、岗位和个人选择。'],
  4: ['订单收缩，企业先控制招聘名额；', '岗位变少，录用与议价空间再受影响。'],
  5: ['同一届投向不同领域，需求未必同步；', '同一行业里，岗位冷热也会分开。'],
  6: ['历史转折能标出，不等于未来能定时；', '间隔和幅度都不能用一把尺外推。'],
  7: ['先看眼前需求，再算自己能承受多久；', '给不确定的未来留一条可调整的路。'],
  8: ['核对岗位是否持续开放、面试能否转录用；', '发布招聘信息，不等于真的有人入职。'],
  9: ['暂时无收入：可用现金÷必要月支出，', '估出缓冲月数，再决定等还是转。'],
 10: ['把现有技能映射到相邻岗位；', '主路收窄时，仍有可申请的第二条路。'],
 11: ['赢家是被挑出来讲的样本；', '被忽略的人，也可能走出完全不同的路。'],
 12: ['知道了结果，容易倒着挑选证据；', '当时看不见的变量，会在故事里消失。'],
 13: ['同年的人结果不同，已反驳单一公式；', '个案只能提出问题，不能证明年份定命。'],
 14: ['先看客户与订单，再看岗位是否持续开放；', '真正拿到录用，比日历年份更有信息。'],
 15: ['列出可转岗位、要补的技能和现金期限；', '把下一步写成行动表，而不是周期预测。'],
 16: ['经济变化先进入行业需求，再碰到个人处境；', '行动路径是几层条件共同作用的结果。'],
 17: ['同一届，有人录用，也有人遭遇缩招；', '周期改变机会分布，写不出个人命运。'],
}

for n,lines in copy.items():
    section_pattern = re.compile(r'(<section class="scene" id="s'+str(n)+r'".*?<div class="sub">)(.*?)(</div>)', re.S)
    new = ''.join('<span class="sub-line">'+html.escape(line)+'</span>' for line in lines)
    source,count = section_pattern.subn(lambda m:m.group(1)+new+m.group(3),source,count=1)
    if count != 1:
        raise RuntimeError(f'Could not update scene {n}')

css = '''
/* A second reading beat gives the example and its implication room to land. */
.sub{font-size:35px;line-height:1.36;padding-top:17px}
.sub-line{display:block}
.sub-line + .sub-line{margin-top:5px;color:#e0d1b6}
#s17 .sub{font-size:37px;line-height:1.32}
'''
source = source.replace('</style>',css+'</style>',1)

# Keep the red impact curve below the small ledger annotation in scene 9.
source = source.replace(
    'M-20 865C135 710 210 960 375 790S650 960 830 800S1000 760 1120 870',
    'M-20 925C135 840 210 965 375 870S650 965 830 845S1000 860 1120 945',
    1,
)

# The original one-line conclusions often entered in the final second of a
# scene. Bring the first explanatory line forward, then reveal the implication
# after the diagram has advanced. The exceptional scene 14 keeps its late
# headline reveal, so its lines enter after that headline.
first_line_times = {
  3:12.0,4:19.8,5:28.2,6:36.5,7:45.0,8:53.3,9:62.2,
 10:70.0,11:78.5,12:87.0,13:97.2,14:106.9,15:113.0,
 16:121.8,17:130.1,
}
second_line_times = {
  3:14.0,4:21.4,5:29.8,6:38.7,7:47.2,8:55.5,9:64.4,
 10:72.0,11:80.5,12:89.0,13:99.0,14:108.0,15:115.3,
 16:124.0,17:131.8,
}
for n,t in first_line_times.items():
    pattern = re.compile(r"(tl\.fromTo\('#s"+str(n)+r" \.sub'[^;]*),[0-9.]+\);")
    source,count = pattern.subn(lambda m:m.group(1)+','+str(t)+');',source,count=1)
    if count != 1:
        raise RuntimeError(f'Could not retime subtitle in scene {n}')

# The second line enters after the first has been read. This nested tween is
# seek-safe and leaves the earlier scene animations intact.
js = '''
const secondLineTimes=SECOND_TIMES;
for(const [scene,time] of Object.entries(secondLineTimes)){
 const second=document.querySelector('#s'+scene+' .sub-line + .sub-line');
 if(second)tl.fromTo(second,{opacity:0,y:18},{opacity:1,y:0,duration:.46,ease:'power2.out'},time);
}
'''
js = js.replace('SECOND_TIMES',str(second_line_times).replace("'",'"'))
source = source.replace('window.__timelines.film=tl;',js+'window.__timelines.film=tl;',1)
film.write_text(source,encoding='utf-8')
print(f'Expanded the argument across {len(copy)} scenes in {film}')
