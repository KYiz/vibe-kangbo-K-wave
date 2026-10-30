# 第一集成片核验

## v5 信息增强版（2026-10-30）

- 可复现的 `content_pass.py` 在用户认可的 v3 画风、短音效和粒子动画上，扩展了 17 段字幕，保留原有 134.3 秒节奏。内容按“同届两封回信→订单与招聘传导→可观察信号和现金缓冲→样本与事后叙事偏差→行动和结论”推进；详情与事实边界见 `CONTENT-STRUCTURE.md`。
- 两行字幕错时进入，第一行交代现象或判断，第二行给解释或行动。同步把多数字幕的进入时间提前，避免结论只在镜头尾部一闪而过。
- 原尺寸抽帧检查 3、22.5、65、108.5、132.5 秒的阅读与遮挡；65 秒现金账本的红色冲击曲线已移到注释下方，修正图文重叠。修正抽帧见 `visual-audit/content-ledger-fix/`；17 段总览见 `.hyperframes/artifacts/snapshots/49bc0500-5471-4f3e-a290-cce54d1bf814/`。
- 修正后 `npm run check` 通过：lint、runtime、layout、motion、audio 均为 0 错误；craft 的 18 条场景级 `dead_stretch` 提示与前版一致。
- 新成片：`renders/episode-01-v5-more-information-134s.mp4`。`ffprobe` 核验为 1080×1920、30 fps、134.300 秒、H.264 + AAC、71,605,575 字节；从实际 MP4 抽看 65 秒及 132.5 秒，图文层级与修正后的账本曲线正常，见 `renders/v5-65.png`、`renders/v5-132.5.png`。

## v3 粒子与音效收尾（2026-10-30）

- 在用户认可的 v3 视觉源上叠加 `particle_pass.py`，六处因果卡点共 280 枚可寻址、确定性粒子：两封回信的纸屑、机器报错、尺子分岔、公式破碎和结尾分路。粒子限制在画面图解区域，关键文字保留净空。
- `audio/mix.py` 将低频撞击控制在约 0.9–1 秒；将原长 5.54 秒的 cinematic whoosh 裁为 1.18 秒、10 秒 riser 裁为 1.38 秒并移到重拍之前。音乐压低后的恢复也由约 1.12 秒收紧到 0.70 秒。原音轨备份为 `assets/film-mix-v3.mp3`。
- 新混音时长 134.300 秒，整体峰值 -1.6 dBFS，无削波。HyperFrames 完整检查通过：lint、runtime、layout、motion、audio 为 0 错误；craft 仍报告此前场景级 `data-layout-ignore` 相关的 18 条静止提示。最终粒子几何已抽帧检查，见 `.hyperframes/artifacts/snapshots/15e2c856-3163-4e8f-8a55-0dd460f5210e/`。
- 新成片：`renders/episode-01-v3-particles-tight-sfx-134s.mp4`。`ffprobe` 核验为 1080×1920、30 fps、134.300 秒、H.264 + AAC、70,438,972 字节；从实际 MP4 抽看 1.45、38.5、94.36、131.1 秒，未见黑帧，粒子位置与文字层级正常，见 `renders/v4-*.png`。

> **当前选用版本（2026-10-30）：** 主工程以 `visual_refine.py` 的 v3 画面为基础，叠加粒子与信息增强字幕；当前成片为 `renders/episode-01-v5-more-information-134s.mp4`。被否决的参考画风实验稿保留在 `compositions/film.reference-style.html.bak` 和 `renders/episode-01-reference-style-134s.mp4`，仅供对照。

## 《运气的形状》参考画风重制（2026-10-30）

- 参考视频：https://www.douyin.com/video/7690344836800913785 。直接查看原片画面后，提取暗色舞台、暖金索引、宋体叙事、史料式小标注和“一幕一个可观察物件”的设计语法，转译为 9:16 竖屏；没有套用原片的历史日期、骰子画面或具体镜头。
- 17 段内容和 134.3 秒切点保持原结构，音乐与音效继续沿用 `assets/film-mix.mp3`。视觉物件改为毕业回信、长波曲线、传导链、行业分岔、预测仪、需求档案、现金账本、样本剪影、放大镜等。
- 可复现的生成脚本：`reference_style_remake.py`；生成 `compositions/film.html`。旧版仍在 `compositions/film.pre-visual.html.bak`，上一版成片仍在 `renders/episode-01-visual-v3-134s.mp4`。
- 全片逐段抽帧检查：`.hyperframes/artifacts/snapshots/4d562f1d-beaa-4e93-8b53-b3cba626324d/`（18 个时点和三张总览）。标题、实验物件、结论分别占据上、中、下区域，抽帧未见文字互挡。
- 完整 `npm run check` 通过：lint、runtime、motion、craft、audio 为 0 错误；layout 仅在 0 秒报告 `sweep_static`，全片抽帧可见物件入场、曲线描绘与场景变换。
- 新成片：`renders/episode-01-reference-style-134s.mp4`。`ffprobe` 核验为 1080×1920、30 fps、134.300 秒、H.264 + AAC、29,964,639 字节；从实际 MP4 抽出 0.8、47、132 秒画面复查，见 `renders/reference-intro.png`、`reference-middle.png`、`reference-end.png`。

## 视觉升级版（2026-10-30）

- 新成片：`renders/episode-01-visual-v3-134s.mp4`。保留原版 `renders/episode-01-editorial-full-134s.mp4`、原有内容、音乐和卡点。
- 视觉改动：为 17 段统一建立深色局部照明，并给纸张、金属和深色看板设置不同的方向渐变；收紧卡片描边与阴影，补充开场信件细节。
- 动态排版：行业标签延后到店铺就位后出现；34 秒尺子在入场前隐藏且从标题之外运动；90 秒印章避开因果箭头；110 秒卡片从地图内部空白区进入，不再穿过标题栏。
- `check --json` 结果 `ok=true`，lint、runtime、layout、motion、contrast、audio 错误均为 0。craft 18 条提示仍与场景 `data-layout-ignore` 有关，不能代替成片目视检查。
- 对实际导出的 MP4 抽看 2.5、26.3、34.4、90.2、110.9、132.5 秒，见 `visual-audit/v3-final/`。容器探测：1080×1920、30 fps、134.300 秒、H.264 + AAC、70,745,369 字节。

> **2026-10-30 视觉复审：** 现版内容与音乐暂定保留。技术检查通过不代表画面质感或动态排版通过；成片可见的遮挡和美术升级方向见 [VISUAL-QUALITY-AUDIT.md](VISUAL-QUALITY-AUDIT.md)。

## 全曲完成版（2026-10-30）

- 0–134.3 秒完整成片：`renders/episode-01-editorial-full-134s.mp4`；本次新增的 101–134.3 秒试看：`renders/episode-01-final-33s-101-134.mp4`。
- 终段以“机会从哪来→自己能转向哪里→周期如何影响机会→回答开头问题”四步收束。分镜、拍点与事实边界见 `STORYBOARD-101-END.md`。
- `snapshots-101-end/` 抽看 17 个关键时刻；`snapshots-101-end-fixes/` 复核 102.06 秒转场与结尾布局。最终 MP4 的 132.8 秒画面抽出为 `snapshots-101-end/render-132.8.png`，字幕与回信没有重叠。
- 完整 HyperFrames 检查 `ok=true`；lint、runtime、layout、motion、contrast、audio 均无错误或警告。craft 的 18 条静止警告源于时间轴场景的 `data-layout-ignore`，场景内动画已通过逐段抽帧复查。
- 成片 1080×1920、30 fps、134.300 秒，H.264 + AAC；新增试看 33.300 秒。四个主要新拍点（102.06、110.56、119.06、127.56 秒）的 1.5 秒音段峰值约为 -3.4、-2.7、-3.3、-2.4 dBFS，均无削波。

## 76–101 秒续段（2026-10-29）

- 25 秒单独试看：`renders/episode-01-new-25s-76-101.mp4`；0–101 秒连贯版：`renders/episode-01-editorial-101s.mp4`。目标总长按歌曲约 2:14 规划，后续还剩约 33 秒。
- 继续深墨、纸张、哑金的编辑视觉系统。第 11 段将成功案例档案与侧页并置；第 12 段用案卷和逆向箭头解释事后归因；第 13 段在 93.56 秒重拍击碎“年份＝财富”，揭示同一年中的多条路径。分镜与事实边界见 `STORYBOARD-76-101.md`。
- 新增段落已在 `snapshots-76-101/` 和 `snapshots-76-101-fixes/` 抽帧复查；另从最终 MP4 抽取 `snapshots-76-101/render-96.5.png` 复核实际成片画面。
- 完整 HyperFrames 检查 `ok=true`，lint、runtime、layout、motion、contrast、audio 均无错误或警告。craft 的 14 条静止警告来自时间轴场景的 `data-layout-ignore`，已通过逐段抽帧检查场景内动画。
- 最终连贯版为 1080×1920、30 fps、101.000 秒，H.264 + AAC；新增片段为精确 25.000 秒。
- 93.56–95.06 秒撞击段平均音量约 -9.3 dBFS、峰值约 -1.4 dBFS；88–92 秒铺垫段平均约 -15.6 dBFS，两处均无削波。

## 51–76 秒续段（2026-10-29）

- 25 秒单独试看：`renders/episode-01-new-25s.mp4`；0–76 秒连贯版：`renders/episode-01-editorial-76s.mp4`。
- 延续深墨、旧纸、哑金、灰绿与宋体标题。新增三件解释物：企业需求看板、家庭账本、备用路线图。分镜见 `STORYBOARD-51-76.md`。
- 51 秒接缝和新增段落已在 `snapshots-51-76/`、`snapshots-51-76-fixes/` 抽帧复查；最终 MP4 的 65.7 秒画面也抽帧复核。
- 完整 HyperFrames 检查 `ok=true`，lint、runtime、layout、motion、contrast、audio 均无错误或警告。craft 的 11 条静止警告来自时间轴场景的 `data-layout-ignore`，已通过逐段抽帧检查场景内动画。
- 最终连贯版为 1080×1920、30 fps、76.000 秒，H.264 + AAC；新增片段为精确 25.000 秒。
- 64–65.5 秒音效段平均音量约 -12.3 dBFS、峰值约 -3.2 dBFS，无削波。

## 编辑风格版（2026-10-29）

- 新成片：`renders/episode-01-editorial-51s.mp4`，保留上一版文件供对比。
- 改为深墨色、纸张与哑金色的统一视觉系统；宋体大标题、细分隔线和轻颗粒替换了原先偏扁平的教学卡片感。
- 第 3、6 段改为物件在上、论点在下的版式，以打破每段都“标题上、图形中”的重复节奏。内容、时点和混音保持一致。
- 抽帧复查：`snapshots-premium/contact-sheet.jpg` 与 `snapshots-premium-layout/contact-sheet.jpg`；另从最终 MP4 抽出 `renders/editorial-frame-40s.png` 验证了成片画面。
- 完整 HyperFrames 检查 `ok=true`，lint、runtime、layout、motion、contrast、audio 均无错误或警告；craft 的 8 条静止警告仍是时间轴场景 `data-layout-ignore` 引起的检查局限，已用逐段抽帧复查。
- 最终成片为 1080×1920、30 fps、51 秒，H.264 + AAC。

## 第一版

- 成片：`renders/episode-01-remake-51s-final.mp4`
- 格式：1080×1920，30 fps，51.000 秒，H.264 视频 + AAC 立体声音频。
- 使用 `hyperframes check --json` 完整检查：`ok=true`；lint、runtime、layout、motion、contrast、audio 均无错误或警告。`craft` 的 8 条静止警告来自给整段时间轴场景添加 `data-layout-ignore` 后，检查器不再检测场景内动画；已通过逐段抽帧独立复查。
- 画面复查：`snapshots-review/contact-sheet.jpg` 观察 2.8、8.5、14.2、20.5、29.5、40、49 秒；`snapshots-beats/contact-sheet.jpg` 观察 0.08、4.35、9.7、17.13、25.6、34.1、38.35、42.6、50.3 秒。
- 音频复核：第一版撞击混音发生削波，已调整音效叠加与软限幅，并将修正版音轨复用到最终 MP4。最终文件的 17.03–18.53 秒峰值约 -2.1 dBFS，38.25–39.75 秒峰值约 -1.3 dBFS；两处均无 0 dBFS 削波。
- 音效来源与授权见 `ASSETS.md`；事实边界与分镜见 `STORYBOARD.md`。
