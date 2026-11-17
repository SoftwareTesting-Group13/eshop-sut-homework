#!/usr/bin/env bash
set -euo pipefail
# Publish 3 FR17 issue drafts. Yêu cầu: gh auth login và đã push nhánh ncuong (để raw screenshot URL hoạt động).
cd "$(dirname "$0")"
command -v gh >/dev/null || { echo "gh CLI chưa cài; brew install gh rồi chạy lại."; exit 1; }
gh auth status >/dev/null || { echo "Chưa đăng nhập gh; chạy 'gh auth login'."; exit 1; }

gh issue create --title "[BUG-FR17-01] Biên số không được validate: discount 0/-1/150 và min -1 đều tạo được" --body-file ../bugs/BUG-FR17-01-numeric-bounds.md --label bug --label major
gh issue create --title "[BUG-FR17-02] Code không được validate: trắng, trùng khác hoa/thường, thiếu key đều tạo được" --body-file ../bugs/BUG-FR17-02-code-validation.md --label bug --label major
gh issue create --title "[BUG-FR17-03] Các trường còn lại không được validate: type lạ, discount chữ, date rác, max 0" --body-file ../bugs/BUG-FR17-03-other-fields.md --label bug --label major
