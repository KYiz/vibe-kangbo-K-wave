"""Resumeable read-only collection of WeRead underline discussions for this book."""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
import time
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
from pathlib import Path

BOOK_ID = "3300128305"
NODE = Path(r"D:\Node.js\node.exe")
CLI = Path(r"F:\Codex\Vibe 知识大赏\weread-omni-main\weread-omni-main\bin\weread-omni.js")
ROOT = Path(__file__).resolve().parent
BOOK_ROOT = ROOT.parent
CACHE = ROOT / ".cache"
CHAPTERS = [
    (1, 6, "人生财富靠康波 康波中的价格波动", "第一部分 涛动周期论"),
    (2, 7, "繁荣的起点 工业化转型期的投资全景", "第一部分 涛动周期论"),
    (3, 8, "“色即是空” 世界经济的共生模式与国际资源品价格调节新机制", "第一部分 涛动周期论"),
    (4, 9, "长波衰退中的增长与通胀", "第一部分 涛动周期论"),
    (5, 10, "走向成熟 中国经济即将 V 形反转", "第一部分 涛动周期论"),
    (6, 11, "结构主义的薪火 周期波动、结构演进与制度变革", "第一部分 涛动周期论"),
    (7, 12, "三周期嵌套 从熊彼特到罗斯托", "第一部分 涛动周期论"),
    (8, 13, "康波衰退二次冲击正在靠近", "第一部分 涛动周期论"),
    (9, 14, "改造“美林投资时钟” 全球大类资产配置框架研究", "第二部分 大类资产配置"),
    (10, 15, "美元破百的全球影响", "第二部分 大类资产配置"),
    (11, 16, "世界大宗商品周期研究", "第二部分 大类资产配置"),
    (12, 17, "康波中的房地产周期研究", "第二部分 大类资产配置"),
    (13, 18, "康波体系下的黄金价格", "第二部分 大类资产配置"),
    (14, 19, "全球变局：如何进行大类资产投资", "第三部分 先生言谈"),
    (15, 20, "演讲实录：宿命与反抗", "第三部分 先生言谈"),
    (16, 21, "一波三折 周期反弹节奏研究", "第三部分 先生言谈"),
    (17, 22, "采访合集", "第三部分 先生言谈"),
    (18, 23, "演讲实录：人生就是一场康波", "第三部分 先生言谈"),
]


def atomic_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    temp.replace(path)


def api(args: list[str]) -> dict:
    key = hashlib.sha256(json.dumps(args, ensure_ascii=False).encode()).hexdigest()[:20]
    path = CACHE / f"{key}.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    env = dict(os.environ)
    env["PATH"] = str(NODE.parent) + os.pathsep + env.get("PATH", "")
    cmd = [str(NODE), str(CLI), "--no-library", *args, "--json"]
    for attempt in range(4):
        result = subprocess.run(cmd, cwd=CLI.parent, env=env, capture_output=True, text=True, encoding="utf-8", errors="replace")
        try:
            data = json.loads(result.stdout)
        except json.JSONDecodeError:
            data = None
        if result.returncode == 0 and isinstance(data, dict) and "error" not in data:
            atomic_json(path, data)
            time.sleep(0.8)
            return data
        message = (result.stdout + "\n" + result.stderr).strip()[:600]
        if args[:2] == ["review", "single"] and re.search(r'"errCode"\s*:\s*-2031', message):
            unavailable = {"unavailable": "微信读书接口返回 -2031，该评论回复不可读取"}
            atomic_json(path, unavailable)
            return unavailable
        if re.search(r"auth|login|credential|captcha|风控|频繁|限制|封禁", message, re.I):
            raise RuntimeError(f"Authentication or rate-limit response; stopped: {message}")
        if attempt == 3:
            raise RuntimeError(f"API failed after retries: {args[:4]}: {message}")
        print(f"Retry {attempt + 1}: {message[:160]}", flush=True)
        time.sleep(3 * 2**attempt)
    raise AssertionError("unreachable")


def chunks(items: list, size: int):
    for start in range(0, len(items), size):
        yield items[start : start + size]


def fetch_ranges(uid: int) -> list[dict]:
    data = api(["notes", "underlines", BOOK_ID, str(uid)])
    by_range: dict[str, dict] = {}
    for underline in data.get("underlines", []):
        range_ = underline.get("range")
        if not range_:
            continue
        current = by_range.get(range_)
        if current is None or underline.get("count", 0) > current.get("count", 0):
            by_range[range_] = underline
    return sorted(by_range.values(), key=lambda u: int(u["range"].split("-")[0]))


def fetch_discussions(uid: int, underlines: list[dict]) -> dict[str, dict]:
    records = {u["range"]: {"underline": u, "reviews": [], "totalCount": None} for u in underlines}
    pending = [{"range": u["range"], "count": 20} for u in underlines]
    round_no = 0
    while pending:
        round_no += 1
        next_pending: list[dict] = []
        for batch_no, batch in enumerate(chunks(pending, 12), 1):
            data = api(["notes", "read-reviews", BOOK_ID, str(uid), "--reviews", json.dumps(batch, ensure_ascii=False, separators=(",", ":"))])
            found = {entry.get("range"): entry for entry in data.get("reviews", [])}
            for query in batch:
                range_ = query["range"]
                if range_ not in found:
                    raise RuntimeError(f"ChapterUid {uid}: API omitted range {range_}")
                page = found[range_]
                record = records[range_]
                if record["totalCount"] is None:
                    record["totalCount"] = page.get("totalCount", 0)
                record["reviews"].extend(page.get("pageReviews") or [])
                if page.get("hasMore"):
                    cursor = page.get("maxIdx")
                    if not isinstance(cursor, int) or cursor <= query.get("maxIdx", 0):
                        raise RuntimeError(f"ChapterUid {uid}: pagination stalled for {range_}")
                    next_pending.append({"range": range_, "count": 20, "maxIdx": cursor})
            if batch_no % 5 == 0:
                print(f"  uid {uid}: round {round_no}, batches {batch_no}, current reviews {sum(len(v['reviews']) for v in records.values())}", flush=True)
        pending = next_pending
    for range_, record in records.items():
        seen: set[str] = set()
        unique = []
        for item in record["reviews"]:
            review_id = item.get("reviewId") or item.get("review", {}).get("reviewId")
            if review_id not in seen:
                unique.append(item)
                if review_id:
                    seen.add(review_id)
        record["reviews"] = unique
        total = record["totalCount"] or 0
        if len(unique) < total:
            raise RuntimeError(f"ChapterUid {uid}: {range_} returned {len(unique)} of {total} comments")
    return records


def fetch_replies(records: dict[str, dict]) -> None:
    with_replies = [item for record in records.values() for item in record["reviews"] if (item.get("commentsCount") or 0) > 0]
    def one(item: dict) -> tuple[dict, dict]:
        review_id = item.get("reviewId") or item.get("review", {}).get("reviewId")
        count = item.get("commentsCount", 0)
        response = api(["review", "single", review_id, "--comments-count", str(max(20, count)), "--likes-count", "1"])
        return item, response

    pending = iter(with_replies)
    completed = 0
    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = {pool.submit(one, item) for item in (next(pending, None) for _ in range(3)) if item is not None}
        while futures:
            finished, futures = wait(futures, return_when=FIRST_COMPLETED)
            for future in finished:
                item, response = future.result()
                comments = response.get("comments") or []
                item["replies"] = comments
                if response.get("unavailable"):
                    item["repliesUnavailable"] = response["unavailable"]
                if len(comments) < item.get("commentsCount", 0):
                    item["repliesIncomplete"] = True
                completed += 1
                if completed % 50 == 0:
                    print(f"  Replies: {completed}/{len(with_replies)}", flush=True)
                next_item = next(pending, None)
                if next_item is not None:
                    futures.add(pool.submit(one, next_item))


def clean(value: object) -> str:
    return re.sub(r"\n{3,}", "\n\n", str(value or "").replace("\r\n", "\n").strip())


def quote(text: str) -> str:
    lines = clean(text).split("\n")
    return "\n".join("> " + line for line in lines) if any(lines) else "> （接口未提供划线原文）"


def write_chapter(number: int, uid: int, title: str, part: str, records: dict[str, dict]) -> dict:
    original = next(BOOK_ROOT.glob(f"{number:02d}-*.md"), None)
    filename = f"{original.stem if original else f'{number:02d}-{title}'}-读者评论.md"
    path = ROOT / filename
    review_count = sum(len(r["reviews"]) for r in records.values())
    reply_count = sum(len(i.get("replies", [])) for r in records.values() for i in r["reviews"])
    expected_replies = sum(i.get("commentsCount", 0) for r in records.values() for i in r["reviews"])
    no_comments = sum(not r["reviews"] for r in records.values())
    lines = [f"# {number:02d} {title}｜读者评论", "", f"所属部分：{part}", f"微信读书 bookId：`{BOOK_ID}`；chapterUid：`{uid}`。", f"划线范围：{len(records)}；读者评论：{review_count}；已读取回复：{reply_count}/{expected_replies}。", "数据为抓取时可见的公开评论；评论可能随时间增删。", ""]
    if original:
        lines += [f"对应正文：[《{original.stem}》](../{original.name})", ""]
    for number_in_chapter, (range_, record) in enumerate(records.items(), 1):
        items = record["reviews"]
        abstract = next((i.get("review", {}).get("abstract") for i in items if i.get("review", {}).get("abstract")), "")
        lines += [f"## {number_in_chapter}. 划线范围 {range_}", "", f"划线人数：{record['underline'].get('count', 0)}；评论：{len(items)}。", "", quote(abstract), ""]
        if not items:
            lines += ["暂无可见读者评论。", ""]
            continue
        for pos, item in enumerate(items, 1):
            review = item.get("review") or {}
            author = (review.get("author") or {}).get("name") or f"用户 {review.get('userVid', '未知')}"
            text = clean(review.get("content") or review.get("htmlContent"))
            lines += [f"### {pos}. {author}", "", text or "（评论正文为空）", "", f"点赞：{item.get('likesCount', 0)}；回复：{item.get('commentsCount', 0)}；reviewId：`{item.get('reviewId', '')}`。", ""]
            for reply in item.get("replies", []):
                reply_author = (reply.get("author") or {}).get("name") or f"用户 {reply.get('userVid', '未知')}"
                lines += [f"- **{reply_author}**：{clean(reply.get('content'))}（点赞 {reply.get('likesCount', 0)}）"]
            if item.get("replies"):
                lines += [""]
            if item.get("repliesIncomplete"):
                lines += [f"*此评论的部分回复未由接口返回。{item.get('repliesUnavailable', '')}*", ""]
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return {"number": number, "title": title, "part": part, "file": filename, "ranges": len(records), "reviews": review_count, "replies": reply_count, "expected_replies": expected_replies, "no_comments": no_comments, "incomplete_replies": sum(bool(i.get("repliesIncomplete")) for r in records.values() for i in r["reviews"])}


def write_index(summaries: list[dict]) -> None:
    lines = ["# 《人生财富靠康波》读者评论目录", "", "按现有 01–18 章目录整理微信读书划线旁的公开评论和回复。正文以各章节 Markdown 为准。", ""]
    current_part = None
    for s in summaries:
        if s["part"] != current_part:
            current_part = s["part"]
            lines += [f"## {current_part}", ""]
        lines += [f"- [{s['number']:02d} {s['title']}](./{s['file']})：{s['ranges']} 处划线、{s['reviews']} 条评论、{s['replies']}/{s['expected_replies']} 条回复"]
    lines += ["", f"合计：{sum(s['ranges'] for s in summaries)} 处划线、{sum(s['reviews'] for s in summaries)} 条评论、已读取 {sum(s['replies'] for s in summaries)}/{sum(s['expected_replies'] for s in summaries)} 条回复。", ""]
    if any(s["incomplete_replies"] for s in summaries):
        lines += [f"有 {sum(s['incomplete_replies'] for s in summaries)} 条评论的回复未取全；原因已标在对应章节和评论下。", ""]
    (ROOT / "评论目录.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    summaries = []
    for number, uid, title, part in CHAPTERS:
        print(f"Chapter {number:02d}, uid {uid}: underlines", flush=True)
        underlines = fetch_ranges(uid)
        print(f"  {len(underlines)} ranges; {sum(bool(u.get('count')) for u in underlines)} with positive count", flush=True)
        records = fetch_discussions(uid, underlines)
        print(f"  {sum(len(r['reviews']) for r in records.values())} top-level comments", flush=True)
        if "--with-replies" in sys.argv:
            print("  Fetching replies", flush=True)
            fetch_replies(records)
        summary = write_chapter(number, uid, title, part, records)
        summaries.append(summary)
        atomic_json(CACHE / f"summary-{number:02d}.json", summary)
        write_index(summaries)
        print(f"  Done {number:02d}: {summary['reviews']} comments, {summary['replies']} replies", flush=True)
    print("COMPLETE " + json.dumps({"chapters": len(summaries), "ranges": sum(s['ranges'] for s in summaries), "reviews": sum(s['reviews'] for s in summaries), "replies": sum(s['replies'] for s in summaries), "incomplete_replies": sum(s['incomplete_replies'] for s in summaries)}, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"STOPPED: {exc}", file=sys.stderr, flush=True)
        raise
