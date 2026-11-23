#!/usr/bin/env python
"""按扩展名归档一个目录。默认只打印计划，加 --apply 才真移动。"""
import argparse
from pathlib import Path

RULES = {
    "图片": {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".bmp", ".ico"},
    "文档": {".pdf", ".docx", ".doc", ".xlsx", ".xls", ".pptx", ".ppt", ".txt", ".md", ".csv"},
    "压缩包": {".zip", ".7z", ".rar", ".tar", ".gz", ".bz2"},
    "音视频": {".mp4", ".mkv", ".avi", ".mov", ".mp3", ".wav", ".flac"},
    "安装包": {".exe", ".msi", ".apk", ".deb", ".dmg"},
}


def bucket(suffix: str) -> str:
    """把一个后缀归到某个分类名。认不出的后缀进「其他」。"""
    s = suffix.lower()
    for name, exts in RULES.items():
        if s in exts:
            return name
    return "其他"


def main() -> None:
    ap = argparse.ArgumentParser(
        description="按扩展名归档目录里的文件。默认只打印计划，加 --apply 才真移动。"
    )
    ap.add_argument("target", type=Path, help="要整理的目录")
    ap.add_argument("--apply", action="store_true", help="真的移动文件（默认只打印计划）")
    args = ap.parse_args()

    if not args.target.is_dir():
        raise SystemExit(f"目录不存在: {args.target}")

    planned = 0
    moved = 0
    for f in sorted(args.target.iterdir()):
        if not f.is_file():
            continue

        dest_dir = args.target / bucket(f.suffix)
        dest = dest_dir / f.name
        planned += 1

        print(f"{'MOVE' if args.apply else 'PLAN'} {f.name} -> {dest_dir.name}/")

        if not args.apply:
            continue

        dest_dir.mkdir(exist_ok=True)
        if dest.exists():
            print(f"  跳过，目标已存在: {dest.name}")
            continue
        f.rename(dest)
        moved += 1

    if args.apply:
        print(f"\n共 {planned} 个文件，已移动 {moved} 个")
    else:
        print(f"\n共 {planned} 个文件，仅计划（加 --apply 执行）")


if __name__ == "__main__":
    main()