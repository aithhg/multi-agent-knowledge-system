#!/usr/bin/env python3
"""
BASES 系统增量同步脚本
将 workspace/ 中的知识文件同步到 D&H&R/ 作为只读 Obsidian 视图

功能：
- 增量同步：基于文件 modification time
- workspace/ 版本优先（冲突时覆盖 D&H&R/）
- 不删除目标目录中源目录没有的文件
- 同步健康度报告（Markdown 格式）
- 增量同步日志（详细记录每次同步的文件状态）

使用方法：
    python sync_to_DHR.py [--dry-run] [--verbose]
"""

import os
import sys
import shutil
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# ============== 配置 ==============
# BASES 根目录
BASES_ROOT = Path(__file__).parent.parent.parent
WORKSPACE_ROOT = BASES_ROOT / "workspace"
DHR_ROOT = BASES_ROOT / "D&H&R"

# 同步映射表
SYNC_MAP: Dict[str, str] = {
    "knowledge/resources/permanent": "Knowledge",
    "knowledge/resources/literature": "Knowledge",
    "knowledge/areas/moc": "Knowledge",
}

# 同步 outputs 目录（所有子目录）
OUTPUTS_SUBDIRS = [
    "article", "memo", "social", "ppt", "infographic",
    "pdf", "artifacts", "drafts", "published", "feedback"
]

# 索引文件
INDEX_FILE = "knowledge/index.md"

# 日志配置
LOG_DIR = WORKSPACE_ROOT / "logs"
LOG_FILE = LOG_DIR / "sync.log"
SYNC_REPORT_DIR = LOG_DIR / "sync"

# 排除模式
EXCLUDE_PATTERNS = {".obsidian", ".git", ".DS_Store", "Thumbs.db"}

# 同步详情记录（用于健康报告）
_sync_details: Dict[str, Dict] = {
    "synced_files": [],
    "skipped_files": [],
    "failed_files": [],
}


def setup_logging(verbose: bool = False) -> None:
    """配置日志"""
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    level = logging.DEBUG if verbose else logging.INFO

    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE, encoding="utf-8"),
            logging.StreamHandler(sys.stdout)
        ]
    )


def should_sync(src_path: Path, dst_path: Path) -> bool:
    """
    基于 modification time 判断是否需要同步
    Returns True if source is newer than destination
    """
    if not dst_path.exists():
        return True

    src_mtime = src_path.stat().st_mtime
    dst_mtime = dst_path.stat().st_mtime

    return src_mtime > dst_mtime


def sync_file(src: Path, dst: Path, dry_run: bool = False) -> Tuple[bool, str]:
    """
    同步单个文件
    Returns: (success, reason)
    """
    global _sync_details

    if not src.exists():
        logging.warning(f"Source file not found: {src}")
        _sync_details["failed_files"].append({
            "file": str(src.relative_to(WORKSPACE_ROOT)),
            "reason": "源文件不存在"
        })
        return False, "源文件不存在"

    dst.parent.mkdir(parents=True, exist_ok=True)

    if should_sync(src, dst):
        if dry_run:
            logging.info(f"[DRY-RUN] Would sync: {src} -> {dst}")
            _sync_details["synced_files"].append(str(src.relative_to(WORKSPACE_ROOT)))
            return True, "dry-run"
        else:
            try:
                shutil.copy2(src, dst)
                logging.info(f"Synced: {src} -> {dst}")
                _sync_details["synced_files"].append(str(src.relative_to(WORKSPACE_ROOT)))
                return True, "success"
            except Exception as e:
                logging.error(f"Error syncing {src}: {e}")
                _sync_details["failed_files"].append({
                    "file": str(src.relative_to(WORKSPACE_ROOT)),
                    "reason": str(e)
                })
                return False, str(e)
    else:
        logging.debug(f"Skipped (not newer): {src}")
        _sync_details["skipped_files"].append(str(src.relative_to(WORKSPACE_ROOT)))
        return False, "not newer"


def sync_directory(src_dir: Path, dst_dir: Path, dry_run: bool = False) -> Dict:
    """
    同步目录（递归）
    Returns sync statistics
    """
    stats = {"synced": 0, "skipped": 0, "errors": 0}

    if not src_dir.exists():
        logging.warning(f"Source directory not found: {src_dir}")
        return stats

    # 确保目标目录存在
    dst_dir.mkdir(parents=True, exist_ok=True)

    for root, dirs, files in os.walk(src_dir):
        # 过滤排除目录
        dirs[:] = [d for d in dirs if d not in EXCLUDE_PATTERNS]

        src_root = Path(root)
        rel_path = src_root.relative_to(src_dir)

        for filename in files:
            if filename in EXCLUDE_PATTERNS:
                continue

            src_file = src_root / filename
            dst_file = dst_dir / rel_path / filename

            try:
                success, reason = sync_file(src_file, dst_file, dry_run)
                if success:
                    stats["synced"] += 1
                elif reason == "not newer":
                    stats["skipped"] += 1
                else:
                    stats["errors"] += 1
            except Exception as e:
                logging.error(f"Error syncing {src_file}: {e}")
                stats["errors"] += 1

    return stats


def sync_index(dry_run: bool = False) -> bool:
    """同步索引文件"""
    src_index = WORKSPACE_ROOT / INDEX_FILE
    dst_index = DHR_ROOT / "Knowledge" / "index.md"

    if not src_index.exists():
        logging.warning(f"Index file not found: {src_index}")
        return False

    try:
        return sync_file(src_index, dst_index, dry_run)
    except Exception as e:
        logging.error(f"Error syncing index: {e}")
        return False


def sync_outputs(dry_run: bool = False) -> Dict:
    """同步 outputs 目录"""
    stats = {"synced": 0, "skipped": 0, "errors": 0}

    for subdir in OUTPUTS_SUBDIRS:
        src_dir = WORKSPACE_ROOT / "outputs" / subdir
        dst_dir = DHR_ROOT / "Outputs" / subdir

        if src_dir.exists():
            result = sync_directory(src_dir, dst_dir, dry_run)
            stats["synced"] += result["synced"]
            stats["skipped"] += result["skipped"]
            stats["errors"] += result["errors"]

    # 同步 outputs/ 根目录下的 .md 文件（如情报日报等非子目录文件）
    src_root = WORKSPACE_ROOT / "outputs"
    dst_root = DHR_ROOT / "Outputs"
    if src_root.exists():
        dst_root.mkdir(parents=True, exist_ok=True)
        for item in src_root.iterdir():
            if item.is_file() and item.suffix == ".md":
                try:
                    success, reason = sync_file(item, dst_root / item.name, dry_run)
                    if success:
                        stats["synced"] += 1
                    elif reason == "not newer":
                        stats["skipped"] += 1
                    else:
                        stats["errors"] += 1
                except Exception as e:
                    logging.error(f"Error syncing root output {item}: {e}")
                    stats["errors"] += 1

    return stats


def generate_sync_report(stats: Dict, timestamp: str, dry_run: bool = False) -> str:
    """生成同步健康度报告（Markdown 格式）"""
    global _sync_details

    # 执行状态判断
    if stats["knowledge_errors"] == 0 and stats["outputs_errors"] == 0:
        if stats["knowledge_synced"] == 0 and stats["outputs_synced"] == 0:
            status = "✅ 无需同步（所有文件已是最新）"
        else:
            status = "✅ 同步成功"
    elif stats["knowledge_errors"] > 0 or stats["outputs_errors"] > 0:
        status = "❌ 同步失败（有文件同步错误）"
    else:
        status = "⚠️ 部分成功"

    # 计算总数
    total_synced = stats["knowledge_synced"] + stats["outputs_synced"]
    total_skipped = stats["knowledge_skipped"] + stats["outputs_skipped"]
    total_errors = stats["knowledge_errors"] + stats["outputs_errors"]

    report = f"""## BASES 同步报告

**执行时间**：{timestamp}
**执行模式**：{"模拟执行（dry-run）" if dry_run else "正式执行"}
**状态**：{status}

---

### 同步统计

| 类别 | 同步 | 跳过 | 错误 |
|------|------|------|------|
| 知识目录 | {stats['knowledge_synced']} | {stats['knowledge_skipped']} | {stats['knowledge_errors']} |
| Outputs | {stats['outputs_synced']} | {stats['outputs_skipped']} | {stats['outputs_errors']} |
| **总计** | **{total_synced}** | **{total_skipped}** | **{total_errors}** |

"""

    # 失败文件列表
    if _sync_details["failed_files"]:
        report += "### 失败文件\n\n"
        report += "| 文件 | 原因 |\n"
        report += "|------|------|\n"
        for item in _sync_details["failed_files"]:
            report += f"| {item['file']} | {item['reason']} |\n"
        report += "\n"

    # 同步的文件（dry-run 模式下显示）
    if _sync_details["synced_files"] and dry_run:
        report += "### 将要同步的文件\n\n"
        for f in _sync_details["synced_files"][:20]:  # 最多显示20个
            report += f"- {f}\n"
        if len(_sync_details["synced_files"]) > 20:
            report += f"- ... 还有 {len(_sync_details['synced_files']) - 20} 个文件\n"
        report += "\n"

    report += f"""---

**提示**：查看详细日志 `logs/sync.log`
"""
    return report


def save_sync_report(report: str, timestamp: str) -> Path:
    """保存同步报告到文件"""
    SYNC_REPORT_DIR.mkdir(parents=True, exist_ok=True)

    report_file = SYNC_REPORT_DIR / f"sync-{timestamp}.md"
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report)

    return report_file


def run_sync(dry_run: bool = False, verbose: bool = False) -> Dict:
    """
    执行完整同步流程
    Returns sync statistics
    """
    global _sync_details

    # 重置同步详情
    _sync_details = {
        "synced_files": [],
        "skipped_files": [],
        "failed_files": [],
    }

    setup_logging(verbose)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

    logging.info(f"{'='*50}")
    logging.info(f"BASES 同步开始 (dry_run={dry_run})")
    logging.info(f"Workspace: {WORKSPACE_ROOT}")
    logging.info(f"D&H&R: {DHR_ROOT}")
    logging.info(f"{'='*50}")

    total_stats = {
        "knowledge_synced": 0,
        "knowledge_skipped": 0,
        "knowledge_errors": 0,
        "outputs_synced": 0,
        "outputs_skipped": 0,
        "outputs_errors": 0,
        "index_synced": False,
    }

    # 同步知识目录
    logging.info("同步知识目录...")
    for src_rel, dst_rel in SYNC_MAP.items():
        src_dir = WORKSPACE_ROOT / src_rel
        dst_dir = DHR_ROOT / dst_rel

        logging.info(f"  {src_rel} -> {dst_rel}")
        result = sync_directory(src_dir, dst_dir, dry_run)
        total_stats["knowledge_synced"] += result["synced"]
        total_stats["knowledge_skipped"] += result["skipped"]
        total_stats["knowledge_errors"] += result["errors"]

    # 同步 outputs
    logging.info("同步 outputs...")
    outputs_stats = sync_outputs(dry_run)
    total_stats["outputs_synced"] = outputs_stats["synced"]
    total_stats["outputs_skipped"] = outputs_stats["skipped"]
    total_stats["outputs_errors"] = outputs_stats["errors"]

    # 同步索引
    logging.info("同步索引...")
    total_stats["index_synced"] = sync_index(dry_run)

    # 汇总
    logging.info(f"{'='*50}")
    logging.info("同步完成:")
    logging.info(f"  知识目录: {total_stats['knowledge_synced']} synced, {total_stats['knowledge_skipped']} skipped, {total_stats['knowledge_errors']} errors")
    logging.info(f"  Outputs:  {total_stats['outputs_synced']} synced, {total_stats['outputs_skipped']} skipped, {total_stats['outputs_errors']} errors")
    logging.info(f"  索引:     {'已同步' if total_stats['index_synced'] else '未变化'}")
    logging.info(f"{'='*50}")

    # 生成并保存健康报告
    report = generate_sync_report(total_stats, timestamp, dry_run)
    report_file = save_sync_report(report, timestamp)

    # 打印报告到控制台
    print("\n" + "="*50)
    print(report)
    print(f"报告已保存: {report_file}")
    print("="*50)

    return total_stats


def main():
    import argparse

    parser = argparse.ArgumentParser(description="BASES 系统增量同步脚本")
    parser.add_argument("--dry-run", action="store_true", help="仅显示将要进行的同步，不实际执行")
    parser.add_argument("--verbose", "-v", action="store_true", help="显示详细日志")

    args = parser.parse_args()

    try:
        run_sync(dry_run=args.dry_run, verbose=args.verbose)
    except KeyboardInterrupt:
        logging.info("同步被用户中断")
        sys.exit(1)
    except Exception as e:
        logging.error(f"同步失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
