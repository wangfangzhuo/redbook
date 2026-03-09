#!/bin/bash
# 结束工作后：提交并推送所有更新
# 用法：bash scripts/push.sh "提交说明"
#       bash scripts/push.sh          （不填则自动生成）

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_DIR"

# 提交信息：优先使用参数，否则自动生成
if [ -n "$1" ]; then
    MSG="$1"
else
    MSG="$(date '+%Y-%m-%d %H:%M') 更新内容"
fi

# 检查是否有变更
if git diff --quiet && git diff --cached --quiet && [ -z "$(git ls-files --others --exclude-standard)" ]; then
    echo "没有需要提交的变更。"
    exit 0
fi

echo "正在提交更新..."
git add -A
git commit -m "$MSG"

echo "正在推送到远程仓库..."
git push origin main

echo "完成！已推送到 GitHub。"
echo "---"
git log --oneline -5
