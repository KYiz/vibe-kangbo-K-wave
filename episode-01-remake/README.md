# 第一集：康波、毕业招聘与个人选择

当前成片：[信息增强版 2 分 14 秒](renders/episode-01-v5-more-information-134s.mp4)，9:16 竖屏、1080×1920、30 fps。

## 工程

- `index.html`、`compositions/film.html`：当前 HyperFrames 时间轴与画面。
- `assets/film-mix.mp3`：当前混音；配乐来源及其他素材说明见 [ASSETS.md](ASSETS.md)。仓库为私有，用于工作区备份；公开发布前需另行确认配乐使用权。
- `CONTENT-STRUCTURE.md`：内容结构与事实边界。
- `REVIEW.md`：画面、音频与成片核验记录。

在本目录运行 `npm run check` 可检查工程。若要从初始画面重建当前构图，依次运行 `python visual_refine.py`、`python particle_pass.py`、`python content_pass.py`；初始画面保存在 `compositions/film.pre-visual.html.bak`。重新制作混音可参考 `audio/mix.py`。

仓库只保留当前成片。旧版导出、抽帧和检查日志留在本地，没有纳入版本控制。
