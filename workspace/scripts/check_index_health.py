#!/usr/bin/env python3
"""
BASES 索引健康度检查脚本

功能：
- 检查 index.md 中标记的文件是否存在于 workspace/
- 检查 workspace/ 中是否有 index.md 未收录的文件
- 检查 index.md 与 D&H&R/Knowledge/ 同步状态
- 生成健康度报告

使用方法：
    python check_index_health.py [--fix] [--verbose]
"""

import os
import re
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Set, Optional

# ============== 配置 ==============
BASES_ROOT = Path(__file__).parent.parent.parent
WORKSPACE_ROOT = BASES_ROOT / "workspace"
DHR_ROOT = BASES_ROOT / "D&H&R"
INDEX_FILE = WORKSPACE_ROOT / "knowledge" / "index.md"
DHR_KNOWLEDGE = DHR_ROOT / "Knowledge"

# 知识目录路径
KNOWLEDGE_DIRS = [
    WORKSPACE_ROOT / "knowledge" / "resources" / "permanent",
    WORKSPACE_ROOT / "knowledge" / "resources" / "literature",
    WORKSPACE_ROOT / "knowledge" / "areas" / "moc",
]


class IndexHealthChecker:
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.issues: List[Dict] = []
        self.stats: Dict = {
            "total_indexed": 0,
            "files_exist": 0,
            "files_missing": 0,
            "files_orphan": 0,
            "dhr_extra": 0,
        }

    def log(self, message: str, level: str = "INFO"):
        if self.verbose or level in ("ERROR", "WARNING"):
            print(f"[{level}] {message}")

    def parse_index_file(self) -> Tuple[Set[str], Set[str]]:
        """
        解析 index.md，提取其中引用的文件列表
        Returns: (indexed_files, topics)
        """
        indexed_files = set()
        topics = set()

        if not INDEX_FILE.exists():
            self.log(f"Index file not found: {INDEX_FILE}", "ERROR")
            return indexed_files, topics

        content = INDEX_FILE.read_text(encoding="utf-8")

        # 匹配来源路径模式：workspace/knowledge/...
        source_pattern = re.compile(r'workspace/(knowledge/[^\s\]]+\.md)', re.MULTILINE)
        matches = source_pattern.findall(content)
        indexed_files.update(matches)

        # 统计 topics
        topic_pattern = re.compile(r'^- \[\[([^\]]+)\]\]', re.MULTILINE)
        topics.update(topic_pattern.findall(content))

        self.stats["total_indexed"] = len(indexed_files)

        return indexed_files, topics

    def get_actual_files(self) -> Set[str]:
        """获取实际存在的文件列表（相对于 workspace/）"""
        actual_files = set()

        for dir_path in KNOWLEDGE_DIRS:
            if not dir_path.exists():
                continue

            for file_path in dir_path.rglob("*.md"):
                rel_path = file_path.relative_to(WORKSPACE_ROOT)
                actual_files.add(str(rel_path).replace("\\", "/"))

        return actual_files

    def get_dhr_files(self) -> Set[str]:
        """获取 D&H&R/Knowledge/ 中实际存在的文件"""
        dhr_files = set()

        if not DHR_KNOWLEDGE.exists():
            return dhr_files

        for file_path in DHR_KNOWLEDGE.rglob("*.md"):
            rel_path = file_path.relative_to(DHR_KNOWLEDGE)
            dhr_files.add(str(rel_path).replace("\\", "/"))

        return dhr_files

    def check_index_integrity(self) -> Dict:
        """检查索引完整性"""
        indexed_files, topics = self.parse_index_file()
        actual_files = self.get_actual_files()

        # 检查 index 中引用的文件是否存在
        for file_path in sorted(indexed_files):
            full_path = WORKSPACE_ROOT / file_path
            if full_path.exists():
                self.stats["files_exist"] += 1
            else:
                self.stats["files_missing"] += 1
                self.issues.append({
                    "type": "MISSING_FROM_WORKSPACE",
                    "severity": "HIGH",
                    "message": f"Index references but file not found: {file_path}",
                    "evidence": f"Index references: {file_path}",
                    "suggestion": f"Remove from index or create the file"
                })
                self.log(f"Missing file: {file_path}", "WARNING")

        # 检查实际文件是否都被 index 收录
        for file_path in sorted(actual_files):
            if file_path not in indexed_files:
                self.stats["files_orphan"] += 1
                self.issues.append({
                    "type": "ORPHAN_FILE",
                    "severity": "MEDIUM",
                    "message": f"File exists but not in index: {file_path}",
                    "evidence": f"Found file: {file_path}",
                    "suggestion": f"Add to index or delete if unnecessary"
                })
                self.log(f"Orphan file (not in index): {file_path}", "WARNING")

        return {
            "indexed": indexed_files,
            "actual": actual_files,
            "topics": topics
        }

    def check_dhr_sync(self) -> Dict:
        """检查 D&H&R 同步状态"""
        dhr_files = self.get_dhr_files()
        indexed_files, _ = self.parse_index_file()

        # D&H&R 中有但 index 没有引用的
        dhr_extra = dhr_files - indexed_files

        # 检查 D&H&R 中是否有 index.md
        dhr_index = DHR_KNOWLEDGE / "index.md"
        index_synced = dhr_index.exists()

        self.stats["dhr_extra"] = len(dhr_extra)

        if dhr_extra:
            for file_path in sorted(dhr_extra):
                self.issues.append({
                    "type": "DHR_EXTRA_FILE",
                    "severity": "LOW",
                    "message": f"D&H&R has file not in index: {file_path}",
                    "evidence": f"D&H&R file: {file_path}",
                    "suggestion": f"Add to index if it should be tracked"
                })

        return {
            "dhr_files": dhr_files,
            "dhr_extra": dhr_extra,
            "index_synced": index_synced
        }

    def calculate_health_score(self) -> float:
        """计算健康度评分"""
        total = self.stats["total_indexed"]
        if total == 0:
            return 0.0

        # 缺失文件扣分最重
        missing_penalty = self.stats["files_missing"] * 2
        orphan_penalty = self.stats["files_orphan"]

        healthy = total - missing_penalty - orphan_penalty
        score = max(0, (healthy / total) * 100)

        return round(score, 1)

    def generate_report(self) -> str:
        """生成巡检报告"""
        # 执行检查
        self.check_index_integrity()
        self.check_dhr_sync()

        score = self.calculate_health_score()

        # 按严重程度分组
        high_priority = [i for i in self.issues if i["severity"] == "HIGH"]
        medium_priority = [i for i in self.issues if i["severity"] == "MEDIUM"]
        low_priority = [i for i in self.issues if i["severity"] == "LOW"]

        report = []
        report.append("# 索引健康度巡检报告")
        report.append("")
        report.append(f"**检查时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"**健康度评分**: {score}%")
        report.append("")
        report.append("## 统计摘要")
        report.append("")
        report.append("| 指标 | 数值 |")
        report.append("|------|------|")
        report.append(f"| 总索引条目 | {self.stats['total_indexed']} |")
        report.append(f"| 正常文件 | {self.stats['files_exist']} |")
        report.append(f"| 缺失文件 | {self.stats['files_missing']} |")
        report.append(f"| 孤立文件 | {self.stats['files_orphan']} |")
        report.append(f"| D&H&R 额外文件 | {self.stats['dhr_extra']} |")
        report.append("")
        report.append("## 问题列表")
        report.append("")

        if high_priority:
            report.append("### High Priority")
            report.append("")
            for issue in high_priority:
                report.append(f"1. **{issue['type']}**: {issue['message']}")
                report.append(f"   - Evidence: {issue['evidence']}")
                report.append(f"   - Suggestion: {issue['suggestion']}")
                report.append("")

        if medium_priority:
            report.append("### Medium Priority")
            report.append("")
            for issue in medium_priority:
                report.append(f"1. **{issue['type']}**: {issue['message']}")
                report.append(f"   - Evidence: {issue['evidence']}")
                report.append(f"   - Suggestion: {issue['suggestion']}")
                report.append("")

        if low_priority:
            report.append("### Low Priority")
            report.append("")
            for issue in low_priority:
                report.append(f"1. **{issue['type']}**: {issue['message']}")
                report.append(f"   - Evidence: {issue['evidence']}")
                report.append(f"   - Suggestion: {issue['suggestion']}")
                report.append("")

        if not self.issues:
            report.append("*未发现问题*")
            report.append("")

        report.append("---")
        report.append("*此报告由 BASES 系统自动生成*")

        return "\n".join(report)

    def run(self) -> str:
        """运行完整检查"""
        self.log("开始索引健康度检查...")
        report = self.generate_report()
        return report


def main():
    import argparse

    parser = argparse.ArgumentParser(description="BASES 索引健康度检查")
    parser.add_argument("--fix", action="store_true", help="自动修复可修复的问题")
    parser.add_argument("--verbose", "-v", action="store_true", help="显示详细日志")
    parser.add_argument("--output", "-o", help="输出报告到指定文件")

    args = parser.parse_args()

    checker = IndexHealthChecker(verbose=args.verbose)
    report = checker.run()

    # 输出报告
    print(report)

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(report, encoding="utf-8")
        print(f"\n报告已保存到: {output_path}")

    # 返回状态码
    if checker.stats["files_missing"] > 0:
        sys.exit(2)  # 有严重问题


if __name__ == "__main__":
    main()
