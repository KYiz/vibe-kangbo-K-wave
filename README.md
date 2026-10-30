# Vibe 知识大赏 · 康波周期

围绕《人生财富靠康波》制作知识类短视频的工作区。仓库保存原始资料、按章节整理的文本，以及第一集的可编辑视频工程和成片。第一集以“康波、毕业招聘与个人选择”为主题，当前成片为 [2 分 14 秒竖屏视频](episode-01-remake/renders/episode-01-v5-more-information-134s.mp4)（1080 × 1920，30 fps）。

## 技术方案

视频使用 HyperFrames 将网页画面渲染为 MP4。画面不是逐帧存储的图片：`episode-01-remake/index.html` 定义 134.3 秒主时间轴，引用 `compositions/film.html` 作为画面轨道，并在另一条轨道挂载最终混音。CLI 可以预览、检查和渲染这个工程。

| 环节 | 实现 | 主要文件 |
| --- | --- | --- |
| 画面 | HTML、CSS 和内联 SVG 绘制文字、图表、插图及纹理；随工程打包 Noto Sans SC、Noto Serif SC 字体 | `compositions/film.html`、`assets/fonts/`、`assets/grain.png` |
| 动画 | GSAP 时间轴控制 17 个场景的切换及场景内元素运动；时间轴注册到 `window.__timelines`，供 HyperFrames 按时间定位画面 | `compositions/film.html`、`assets/gsap.min.js` |
| 声音 | Python 脚本按秒安排配乐和音效，做音量控制与淡入淡出；FFmpeg 解码、重采样并编码最终 MP3 | `audio/mix.py`、`assets/film-mix.mp3` |
| 输出 | HyperFrames CLI 检查工程并渲染竖屏 MP4 | `package.json`、`hyperframes.json`、`renders/` |

内容制作与画面实现分开记录：分镜见 [STORYBOARD.md](episode-01-remake/STORYBOARD.md)，论述结构与事实边界见 [CONTENT-STRUCTURE.md](episode-01-remake/CONTENT-STRUCTURE.md)，素材来源见 [ASSETS.md](episode-01-remake/ASSETS.md)，成片核验见 [REVIEW.md](episode-01-remake/REVIEW.md)。

## 本地运行

需要 Node.js 与 npm；重新生成混音还需要 Python 3 和 FFmpeg。HyperFrames CLI 在 `package.json` 中固定为 `0.8.210`，通过 `npx` 调用。

```bash
cd episode-01-remake
npm run check   # 检查工程
npm run dev     # 启动预览
npm run render  # 渲染视频
```

当前工程已包含 `assets/film-mix.mp3`，因此预览和渲染不需要先运行混音脚本。若修改了音效时点或配乐，在该目录执行 `python audio/mix.py` 重建混音；脚本优先调用 PATH 中的 `ffmpeg`。工程还保留 `visual_refine.py`、`particle_pass.py` 和 `content_pass.py`，用于从初始画面依次重建当前构图，具体步骤见 [第一集工程说明](episode-01-remake/README.md)。

## 仓库结构

| 路径 | 内容 |
| --- | --- |
| `episode-01-remake/` | 当前第一集工程、素材、成片及制作记录 |
| `hyperframes-style-samples/` | HyperFrames 风格试验工程 |
| `output/markdown/` | 原始 PDF 转出的章节文本和插图 |
| `weread-omni-main/` | 微信读书工具的独立源码副本；使用方式见其[项目 README](weread-omni-main/weread-omni-main/README.md) |
| 根目录 PDF 与 Markdown 文件 | 原始资料、选题及风格策划 |

仓库为私有工作区备份。配乐的公开发布使用权需另行确认，其他素材说明见第一集的 [ASSETS.md](episode-01-remake/ASSETS.md)。依赖安装目录、临时文件和渲染缓存不纳入版本控制。
