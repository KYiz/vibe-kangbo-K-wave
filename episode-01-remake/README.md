# 第一集：康波、毕业招聘与个人选择

当前成片：[信息增强版 2 分 14 秒](renders/episode-01-v5-more-information-134s.mp4)，9:16 竖屏、1080×1920、30 fps。

## 工程

- `index.html`、`compositions/film.html`：当前 HyperFrames 时间轴与画面。
- `assets/film-mix.mp3`：当前混音；配乐来源及其他素材说明见 [ASSETS.md](ASSETS.md)。仓库已公开，素材的再分发与公开发布使用权仍需分别确认。
- `CONTENT-STRUCTURE.md`：内容结构与事实边界。
- `REVIEW.md`：画面、音频与成片核验记录。

需要 Node.js 与 npm；从初始画面重建构图需要 Python 3，重新制作混音还需要 FFmpeg。在本目录运行 `npm run check` 检查工程、`npm run dev` 预览、`npm run render` 导出。`package.json` 通过 `npx` 固定调用 HyperFrames `0.8.210`。

`index.html` 声明 1080×1920、30 fps、134.3 秒的主时间轴，同时挂载 `compositions/film.html` 画面和 `assets/film-mix.mp3` 音轨。画面由 HTML/CSS/SVG 绘制，GSAP 控制 17 段场景的切换与运动。`audio/mix.py` 按时间安排音效，并在关键撞击点降低配乐音量。

若要从初始画面重建当前构图，依次运行 `python visual_refine.py`、`python particle_pass.py`、`python content_pass.py`；初始画面保存在 `compositions/film.pre-visual.html.bak`。这三个脚本会改写 `compositions/film.html`。修改音效或配乐后，运行 `python audio/mix.py` 重建混音；确保 `ffmpeg` 在 PATH 中。

仓库只保留当前成片。旧版导出、抽帧和检查日志留在本地，没有纳入版本控制。
