#!/usr/bin/env bash
set -euo pipefail
# Publish 3 FR10 issue drafts. Yêu cầu: gh auth login và đã push nhánh ncuong (để raw screenshot URL hoạt động).
cd "$(dirname "$0")"
command -v gh >/dev/null || { echo "gh CLI chưa cài; brew install gh rồi chạy lại."; exit 1; }
gh auth status >/dev/null || { echo "Chưa đăng nhập gh; chạy 'gh auth login'."; exit 1; }

gh issue create --title "[BUG-FR10-01] Chuyển canceled sang delivered được cho phép (phá trạng thái kết thúc)" --body-file ../bugs/BUG-FR10-01-cancelled-to-delivered.md --label bug --label major
gh issue create --title "[BUG-FR10-02] User hủy được đơn đang shipping" --body-file ../bugs/BUG-FR10-02-user-cancel-shipping.md --label bug --label major
gh issue create --title "[BUG-FR10-03] API admin không kiểm tra role, user thường đổi được trạng thái đơn (blocker)" --body-file ../bugs/BUG-FR10-03-no-role-check.md --label bug --label blocker
