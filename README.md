# 小红书自媒体运营管理

## 目录说明

| 目录 | 用途 |
|------|------|
| `content/drafts/` | 草稿（未发布） |
| `content/published/` | 已发布内容存档 |
| `content/templates/` | 内容模板 |
| `assets/images/` | 图片素材 |
| `assets/videos/` | 视频素材 |
| `assets/cover-templates/` | 封面模板 |
| `data/analytics/` | 数据分析记录 |
| `planning/ideas/` | 选题灵感 |
| `planning/campaigns/` | 活动策划 |
| `scripts/` | 自动化脚本 |

## 日常工作流

```bash
# 开始工作前：同步最新内容
bash scripts/sync.sh

# 结束工作后：提交所有更新
bash scripts/push.sh "今日更新说明"
```
