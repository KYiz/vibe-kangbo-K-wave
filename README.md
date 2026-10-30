# Vibe 知识大赏 · 康波周期

围绕《人生财富靠康波》制作知识类短视频的工作区。仓库保存资料、整理后的章节文本、选题与分镜，以及第一集的可编辑工程和成片。第一集以“康波、毕业招聘与个人选择”为主题：经济波动会影响机会分布，但不能用出生年份推算个人命运。

**当前成片：**[第一集信息增强版 MP4](episode-01-remake/renders/episode-01-v5-more-information-134s.mp4)，9:16 竖屏，1080 × 1920，30 fps，时长 134.3 秒（约 2 分 14 秒），H.264 视频与 AAC 音频。详细制作记录见 [第一集工程说明](episode-01-remake/README.md)。

## 技术方案

视频使用 HyperFrames 将网页画面渲染为 MP4。画面由代码生成，而非预先导出成逐帧图片。主入口 `episode-01-remake/index.html` 声明画面尺寸、帧率、总时长和两条轨道：`compositions/film.html` 提供画面，`assets/film-mix.mp3` 提供音频。`hyperframes.json` 配置画面与素材目录。

| 环节 | 实现 | 主要文件 |
| --- | --- | --- |
| 画面 | HTML、CSS 和内联 SVG 绘制文字、图表、插图及纹理；随工程打包 Noto Sans SC、Noto Serif SC 字体 | `compositions/film.html`、`assets/fonts/`、`assets/grain.png` |
| 动画 | GSAP 时间轴控制 17 个场景的切换及场景内元素运动；暂停的时间轴注册到 `window.__timelines`，供 HyperFrames 跳转到指定时间 | `compositions/film.html`、`assets/gsap.min.js` |
| 声音 | Python 脚本按秒叠加配乐与音效，按撞击点短暂降低配乐音量；FFmpeg 解码为 48 kHz 双声道 PCM，再编码最终 MP3 | `audio/mix.py`、`assets/film-mix.mp3` |
| 输出 | HyperFrames CLI 检查工程并渲染竖屏 MP4 | `package.json`、`hyperframes.json`、`renders/` |

当前画面采用深色背景、纸张与金属质感、中文宋体标题。图形主要由 SVG 路径和 HTML 排版组成；少量颗粒纹理来自 `assets/grain.png`。六处粒子效果由带固定随机种子的脚本生成，因此同一份源文件可重复得到相同的粒子位置。

## 从资料到成片

1. **整理资料：**根目录保存原始 PDF；`output/text/` 与 `output/markdown/` 保存提取后的文本、章节和插图。仓库目前没有把 PDF 一键转成这些目录的脚本。
2. **确定论点与分镜：**[内容结构](episode-01-remake/CONTENT-STRUCTURE.md)记录五段论述、事实边界和虚构示例；[分镜](episode-01-remake/STORYBOARD.md)及续段文件记录镜头、文案和时间点。
3. **制作画面：**HTML/CSS/SVG 定义每段场景；GSAP 根据时间轴控制文字、图形、转场和粒子。当前构图可从初始画面按下文的三个 Python 脚本重建。
4. **制作音频：**`audio/mix.py` 将配乐和音效混为一条音轨，再由 `index.html` 与画面同步挂载。
5. **检查与导出：**运行 `npm run check` 检查工程，预览后运行 `npm run render` 导出。当前成片的尺寸、帧率、时长及音频检查记录在 [REVIEW.md](episode-01-remake/REVIEW.md)。

## 本地运行

需要 Node.js 与 npm；重新生成画面处理结果需要 Python 3，重新生成混音还需要 FFmpeg。HyperFrames CLI 在 `package.json` 中固定为 `0.8.210`，通过 `npx` 调用；首次运行可能需要下载该版本。

```bash
cd episode-01-remake
npm run check   # 检查工程
npm run dev     # 启动预览
npm run render  # 渲染视频
```

工程已包含当前画面与混音，直接检查、预览或渲染即可。需要从 `compositions/film.pre-visual.html.bak` 重建当前画面时，在 `episode-01-remake/` 中依次运行以下命令；这些脚本会写入 `compositions/film.html`，建议先保存自己的修改。

```bash
python visual_refine.py
python particle_pass.py
python content_pass.py
```

若修改配乐或音效时点，运行 `python audio/mix.py` 重建 `assets/film-mix.mp3`。脚本优先使用 PATH 中的 `ffmpeg`；在其他机器上运行时应将 FFmpeg 加入 PATH。声音素材的具体来源见 [ASSETS.md](episode-01-remake/ASSETS.md)。

## 仓库结构

| 路径 | 内容 |
| --- | --- |
| `episode-01-remake/` | 当前第一集工程、素材、成片及制作记录 |
| `hyperframes-style-samples/` | HyperFrames 风格试验工程 |
| `output/text/`、`output/markdown/` | 从原始资料提取的文本、章节和插图 |
| `weread-omni-main/` | 微信读书工具的独立源码副本；不是视频渲染依赖，使用方式见其[项目 README](weread-omni-main/weread-omni-main/README.md) |
| 根目录 PDF 与 Markdown 文件 | 原始资料、选题及风格策划 |

## 素材与复现边界

此仓库公开可见，但仓库可见不代表原书、配乐等第三方素材已获得再分发或商用授权。素材来源与待确认事项记录在 [ASSETS.md](episode-01-remake/ASSETS.md)。仓库保留当前成片及其工程；旧版导出、抽帧、依赖安装目录和渲染缓存未纳入版本控制。`output/` 是已整理的数据，不提供从原始资料到成片的单命令自动流水线。
