#!/usr/bin/env python3
"""
BASES 索引自动更新脚本
当新概念卡/摘要/主题页创建后，自动更新相关索引

功能：
- 根据新文件的 type 字段识别类型（concept/summary/topic）
- 自动追加到对应 MOC 文件的链接列表
- 自动更新 knowledge/index.md

使用方法：
    python update-index.py <新文件路径>
    python update-index.py --auto  # 自动检测并更新
"""

import os
import sys
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# ============== 配置 ==============
BASES_ROOT = Path(__file__).parent.parent.parent
WORKSPACE_ROOT = BASES_ROOT / "workspace"
KNOWLEDGE_DIR = WORKSPACE_ROOT / "knowledge"
INDEX_FILE = KNOWLEDGE_DIR / "index.md"

# MOC 目录
MOC_DIR = KNOWLEDGE_DIR / "areas" / "moc"


def parse_frontmatter(file_path: Path) -> Optional[Dict]:
    """解析 Markdown 文件的 frontmatter"""
    if not file_path.exists():
        return None

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    if not content.startswith("---"):
        return None

    # 提取 frontmatter
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return None

    fm_text = match.group(1)
    result = {}

    for line in fm_text.split("\n"):
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        result[key.strip()] = value.strip()

    return result


def extract_links(content: str) -> List[str]:
    """提取 Markdown 内容中的 wiki 链接 [[...]]"""
    return re.findall(r"\[\[([^\]]+)\]\]", content)


def update_moc_file(moc_path: Path, new_link: str) -> bool:
    """在 MOC 文件末尾追加新链接"""
    if not moc_path.exists():
        return False

    with open(moc_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 检查是否已存在
    if f"[[{new_link}]]" in content:
        print(f"  链接已存在: {new_link}")
        return False

    # 在 Related 或合适的位置追加
    # 简单策略：在文件末尾追加
    with open(moc_path, "a", encoding="utf-8") as f:
        f.write(f"\n- [[{new_link}]]\n")

    return True


def update_index_file(file_path: Path, fm: Dict) -> bool:
    """更新知识总索引"""
    if not INDEX_FILE.exists():
        # 创建索引文件
        INDEX_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(INDEX_FILE, "w", encoding="utf-8") as f:
            f.write("# 知识索引\n\n")
            f.write(f"> 自动生成于 {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
            f.write("---\n\n")

    file_id = file_path.stem
    file_type = fm.get("type", "unknown")
    file_title = fm.get("title", file_id)

    # 读取现有索引
    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # 检查是否已存在
    if f"- [[{file_id}]]" in content:
        print(f"  索引已存在: {file_id}")
        return False

    # 按类型追加到对应 section
    section_header = {
        "concept": "## 概念卡\n",
        "summary": "## 摘要\n",
        "topic": "## 主题页\n",
    }.get(file_type, "## 其他\n")

    # 如果 section 不存在，创建它
    if section_header not in content:
        with open(INDEX_FILE, "a", encoding="utf-8") as f:
            f.write(f"\n{section_header}\n")

    # 在对应 section 追加
    # 简单策略：在文件末尾追加
    with open(INDEX_FILE, "a", encoding="utf-8") as f:
        f.write(f"- [[{file_id}]] — {file_title}\n")

    return True


def detect_topic_from_content(file_path: Path) -> Optional[str]:
    """根据文件内容推断所属主题"""
    if not file_path.exists():
        return None

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 读取 MOC 文件，尝试匹配
    if not MOC_DIR.exists():
        return None

    # 简单匹配：根据文件名中的关键词
    file_stem = file_path.stem.lower()

    for moc_file in MOC_DIR.glob("*.md"):
        moc_stem = moc_file.stem.lower()
        # 如果文件名包含 MOC 名
        if moc_stem in file_stem or file_stem in moc_stem:
            return moc_file.stem

    return None


def run_update(file_path: Path, verbose: bool = False) -> bool:
    """执行索引更新"""
    file_path = Path(file_path).resolve()

    if not file_path.exists():
        print(f"文件不存在: {file_path}")
        return False

    # 解析 frontmatter
    fm = parse_frontmatter(file_path)
    if not fm:
        print(f"无法解析 frontmatter: {file_path}")
        return False

    file_id = file_path.stem
    file_type = fm.get("type", "unknown")

    print(f"处理文件: {file_id}")
    print(f"  类型: {file_type}")
    print(f"  标题: {fm.get('title', 'N/A')}")

    updated = False

    # 更新总索引
    if update_index_file(file_path, fm):
        print(f"  ✅ 已更新总索引")
        updated = True

    # 更新 MOC（仅对 concept 和 summary 类型）
    if file_type in ("concept", "summary"):
        # 尝试从 frontmatter 的 topics 字段获取
        topics = fm.get("topics", "")
        if isinstance(topics, str):
            topics = [t.strip() for t in topics.split(",")]

        # 也尝试从内容中推断
        inferred_topic = detect_topic_from_content(file_path)
        if inferred_topic:
            topics.append(inferred_topic)

        for topic in topics:
            if not topic:
                continue
            # 查找对应的 MOC 文件
            moc_patterns = [
                MOC_DIR / f"moc-{topic.lower().replace(' ', '-')}.md",
                MOC_DIR / f"topic-{topic.lower().replace(' ', '-')}.md",
                MOC_DIR / f"{topic.lower().replace(' ', '-')}.md",
            ]
            for moc_path in moc_patterns:
                if moc_path.exists():
                    if update_moc_file(moc_path, file_id):
                        print(f"  ✅ 已更新 MOC: {moc_path.name}")
                        updated = True
                    break

    if not updated:
        print(f"  ℹ️ 无需更新（已存在或无对应 MOC）")

    return updated


def main():
    import argparse

    parser = argparse.ArgumentParser(description="BASES 索引自动更新脚本")
    parser.add_argument("file_path", nargs="?", help="新文件的路径")
    parser.add_argument("--auto", action="store_true", help="自动检测 workspace/knowledge/ 下所有文件")
    parser.add_argument("-v", "--verbose", action="store_true", help="详细输出")

    args = parser.parse_args()

    if args.auto:
        # 自动检测所有知识文件
        print("自动检测模式...")
        for file_path in KNOWLEDGE_DIR.rglob("*.md"):
            # 排除 inspections 和 index.md 自身
            if "inspections" in file_path.parts:
                continue
            if file_path.name == "index.md":
                continue
            run_update(file_path, args.verbose)
    elif args.file_path:
        run_update(args.file_path, args.verbose)
    else:
        print("请指定文件路径或使用 --auto")
        sys.exit(1)


if __name__ == "__main__":
    main()
