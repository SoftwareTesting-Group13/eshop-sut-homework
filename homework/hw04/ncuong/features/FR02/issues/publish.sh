#!/usr/bin/env bash
set -euo pipefail
# Publish 3 FR02 issue drafts. Yêu cầu: gh auth login và đã push nhánh ncuong (để raw screenshot URL hoạt động).
cd "$(dirname "$0")"
command -v gh >/dev/null || { echo "gh CLI chưa cài; brew install gh rồi chạy lại."; exit 1; }
gh auth status >/dev/null || { echo "Chưa đăng nhập gh; chạy 'gh auth login'."; exit 1; }

gh issue create --title "[BUG-FR02-01] Sai mật khẩu tăng login_attempts lên 2, khóa sớm từ lần sai thứ 2" --body-file ../bugs/BUG-FR02-01-counter-plus2.md --label bug --label major
gh issue create --title "[BUG-FR02-02] Ô email và mật khẩu dùng type=text, không validate HTML5 và lộ mật khẩu" --body-file ../bugs/BUG-FR02-02-input-types.md --label bug --label major
gh issue create --title "[BUG-FR02-03] Đăng nhập với password null được cấp JWT (blocker)" --body-file ../bugs/BUG-FR02-03-null-password-bypass.md --label bug --label blocker
