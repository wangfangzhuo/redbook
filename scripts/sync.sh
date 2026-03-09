#!/bin/bash
# 开始工作前：从 Git 同步最新内容
# 用法：bash scripts/sync.sh

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_DIR"

echo "正在同步最新内容..."

# 检查是否有未提交的本地修改
if ! git diff --quiet || ! git diff --cached --quiet; then
    echo "警告：检测到本地有未提交的修改，先保存到暂存区..."
    git stash push -m "auto-stash before sync $(date '+%Y-%m-%d %H:%M')"
    STASHED=true
fi

# 拉取远程最新内容
git pull origin main --rebase

if [ "$STASHED" = true ]; then
    echo "正在恢复本地修改..."
    git stash pop
fi

echo "同步完成！当前内容已是最新版本。"
echo "---"
git log --oneline -5
