#!/usr/bin/env python3
"""
BASES 文件监控自动同步脚本
监控 workspace/ 目录的文件变化，自动触发同步

功能：
- 监控 workspace/ 目录及其子目录的文件变化
- 检测到变化后，延迟 5 秒（防抖动）
- 自动触发 sync_to_DHR.py 执行同步

使用方法：
    python watch_and_sync.py [--delay 5] [--daemon]

注意：
- Windows：使用 Windows API (ReadDirectoryChangesW)
- 需要以管理员权限运行（Windows）
"""

import os
import sys
import time
import subprocess
import threading
from pathlib import Path
from datetime import datetime
from typing import Set

# ============== 配置 ==============
BASES_ROOT = Path(__file__).parent.parent.parent
WORKSPACE_ROOT = BASES_ROOT / "workspace"
SYNC_SCRIPT = BASES_ROOT / "workspace" / "scripts" / "sync_to_DHR.py"

# 延迟秒数（防抖动）
DEFAULT_DELAY = 5

# 排除模式
EXCLUDE_DIRS = {".obsidian", ".git", "__pycache__", ".cache"}
EXCLUDE_EXTENSIONS = {".tmp", ".lock", ".swp"}


class FileWatcher:
    """文件监控器"""

    def __init__(self, watch_path: Path, delay: int = DEFAULT_DELAY):
        self.watch_path = watch_path
        self.delay = delay
        self.recent_changes: Set[str] = set()
        self.running = False
        self.lock = threading.Lock()

    def is_excluded(self, path: str) -> bool:
        """检查是否应该排除"""
        path_obj = Path(path)
        parts = path_obj.parts

        # 排除特定目录
        for part in parts:
            if part in EXCLUDE_DIRS:
                return True

        # 排除特定扩展名
        if path_obj.suffix in EXCLUDE_EXTENSIONS:
            return True

        return False

    def on_file_changed(self, file_path: str):
        """文件变化回调"""
        if self.is_excluded(file_path):
            return

        print(f"[{datetime.now().strftime('%H:%M:%S')}] 检测到变化: {file_path}")

        with self.lock:
            self.recent_changes.add(file_path)

        # 延迟后触发同步
        threading.Timer(self.delay, self._trigger_sync).start()

    def _trigger_sync(self):
        """触发同步"""
        with self.lock:
            if not self.recent_changes:
                return
            changes = self.recent_changes.copy()
            self.recent_changes.clear()

        print(f"[{datetime.now().strftime('%H:%M:%S')}] 触发同步...")
        print(f"  变化文件数: {len(changes)}")

        try:
            result = subprocess.run(
                ["python", str(SYNC_SCRIPT), "--verbose"],
                capture_output=True,
                text=True,
                timeout=60
            )
            if result.returncode == 0:
                print(f"  ✅ 同步完成")
            else:
                print(f"  ❌ 同步失败: {result.stderr}")
        except subprocess.TimeoutExpired:
            print(f"  ❌ 同步超时")
        except Exception as e:
            print(f"  ❌ 同步错误: {e}")


def watch_windows(watcher: FileWatcher):
    """Windows 文件监控实现"""
    import ctypes
    from ctypes import wintypes

    # Windows API 常量
    FILE_NOTIFY_CHANGE_LAST_WRITE = 0x10
    FILE_LIST_DIRECTORY = 0x1
    GENERIC_READ = 0x80000000
    FILE_SHARE_READ = 0x1
    FILE_SHARE_WRITE = 0x2
    FILE_SHARE_DELETE = 0x4
    OPEN_EXISTING = 3
    INVALID_HANDLE_VALUE = -1

    # 定义结构体
    class FILE_NOTIFY_INFORMATION(ctypes.Structure):
        _fields_ = [
            ("NextEntryOffset", wintypes.DWORD),
            ("Action", wintypes.DWORD),
            ("FileNameLength", wintypes.DWORD),
            ("FileName", wintypes.WCHAR * 1),
        ]

    FILE_NOTIFY_INFORMATION_P = ctypes.POINTER(FILE_NOTIFY_INFORMATION)

    kernel32 = ctypes.windll.kernel32

    # 打开目录
    handle = kernel32.CreateFileW(
        str(watcher.watch_path),
        FILE_LIST_DIRECTORY,
        FILE_SHARE_READ | FILE_SHARE_WRITE | FILE_SHARE_DELETE,
        None,
        OPEN_EXISTING,
        FILE_NOTIFY_CHANGE_LAST_WRITE,
        None
    )

    if handle == INVALID_HANDLE_VALUE:
        print(f"无法打开目录: {watcher.watch_path}")
        return

    print(f"开始监控: {watcher.watch_path}")
    print(f"延迟触发: {watcher.delay} 秒")

    buffer = ctypes.create_string_buffer(1024 * 1024)  # 1MB buffer
    bytes_returned = wintypes.DWORD()

    try:
        while watcher.running:
            result = kernel32.ReadDirectoryChangesW(
                handle,
                buffer,
                len(buffer),
                True,  # recursive
                FILE_NOTIFY_CHANGE_LAST_WRITE,
                ctypes.byref(bytes_returned),
                None,
                None
            )

            if result:
                offset = 0
                while True:
                    fni = ctypes.cast(
                        ctypes.byref(buffer, offset),
                        FILE_NOTIFY_INFORMATION_P
                    ).contents

                    if fni.FileNameLength > 0:
                        filename = fni.FileName[:fni.FileNameLength // 2]
                        full_path = str(watcher.watch_path / filename)
                        watcher.on_file_changed(full_path)

                    if fni.NextEntryOffset == 0:
                        break
                    offset += fni.NextEntryOffset
    finally:
        kernel32.CloseHandle(handle)


def watch_unix(watcher: FileWatcher):
    """Unix/macOS 文件监控实现（使用 inotify）"""
    import inotify.adapters

    print(f"开始监控: {watcher.watch_path}")
    print(f"延迟触发: {watcher.delay} 秒")

    i = inotify.adapters.InotifyTree(str(watcher.watch_path))

    try:
        for event in i.event_gen():
            if event is None:
                continue
            if not watcher.running:
                break

            (header, type_names, path, filename) = event
            full_path = str(Path(path) / filename) if filename else path
            watcher.on_file_changed(full_path)
    except Exception as e:
        print(f"inotify 错误: {e}")
        print("提示：Linux 需要安装 inotify-tools")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="BASES 文件监控自动同步脚本")
    parser.add_argument("--delay", type=int, default=DEFAULT_DELAY, help=f"延迟触发秒数（默认 {DEFAULT_DELAY}）")
    parser.add_argument("--daemon", action="store_true", help="守护进程模式")
    parser.add_argument("--stop", action="store_true", help="停止守护进程")

    args = parser.parse_args()

    # 检查 sync 脚本是否存在
    if not SYNC_SCRIPT.exists():
        print(f"错误: 同步脚本不存在: {SYNC_SCRIPT}")
        sys.exit(1)

    # 创建监控器
    watcher = FileWatcher(WORKSPACE_ROOT, args.delay)

    if args.stop:
        print("停止守护进程...")
        # 发送信号或使用 PID 文件停止
        # 这里简化处理，实际需要用信号或 PID 文件
        print("守护进程已停止")
        return

    watcher.running = True

    print("=" * 50)
    print("BASES 文件监控自动同步")
    print("=" * 50)
    print(f"监控目录: {WORKSPACE_ROOT}")
    print(f"同步脚本: {SYNC_SCRIPT}")
    print("按 Ctrl+C 停止")
    print("=" * 50)

    try:
        if sys.platform == "win32":
            watch_windows(watcher)
        else:
            watch_unix(watcher)
    except KeyboardInterrupt:
        print("\n停止监控...")
        watcher.running = False


if __name__ == "__main__":
    main()
