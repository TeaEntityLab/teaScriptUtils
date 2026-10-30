#!/bin/bash
# check.sh — teaScriptUtils 最小驗證 harness
#
# 只做靜態檢查，不執行任何腳本:
#   1. shell 腳本語法 (shebang 指定的 shell -n)
#   2. python3 腳本語法 (py_compile; python2 腳本標 SKIP)
#   3. 預期可執行的檔案有沒有 +x
#   4. 外部依賴是否存在於 PATH
#
# 用法: ./check.sh
# 結束碼: 0 = 全部通過, 1 = 有 FAIL

set -uo pipefail
cd "$(dirname "$0")"

PASS=0; FAIL=0; SKIP=0; WARN=0

pass() { PASS=$((PASS+1)); }
fail() { FAIL=$((FAIL+1)); echo "FAIL  $1"; }
skip() { SKIP=$((SKIP+1)); echo "SKIP  $1 ($2)"; }
warn() { WARN=$((WARN+1)); echo "WARN  $1"; }

# 不檢查可執行位、不做語法檢查的檔案
is_doc_or_data() {
  case "$1" in
    *.bat|*.md|LICENSE|*.yml|*.yaml|*.json|*.csv) return 0 ;;
    *) return 1 ;;
  esac
}

echo "== 語法檢查 =="
for f in *; do
  [ -f "$f" ] || continue
  case "$f" in check.sh|GOVERNANCE.md|README.md|LICENSE) continue ;; esac

  first_line=$(head -n1 "$f" 2>/dev/null)
  case "$first_line" in '#!'*) shebang="$first_line" ;; *) shebang="" ;; esac

  if [ -z "$shebang" ]; then
    # 無 shebang: 依副檔名或文件類型分類
    case "$f" in
      *.py) skip "$f" "python2 時代腳本, 本機無 python2 可驗" ;;
      *)
        if is_doc_or_data "$f"; then skip "$f" "文件/資料檔"
        elif sh -n "$f" 2>/dev/null; then pass
        else fail "$f (sh syntax, no shebang)"; fi ;;
    esac
    continue
  fi

  case "$shebang" in
    *python3*|*python\ 3*)
      if python3 -m py_compile "$f" 2>/dev/null; then pass; else fail "$f (python3 syntax)"; fi ;;
    *python*)
      skip "$f" "python2 時代腳本, 本機無 python2 可驗" ;;
    *bash*)
      if bash -n "$f" 2>/dev/null; then pass; else fail "$f (bash syntax)"; fi ;;
    *bin/sh*|*env\ sh*)
      if sh -n "$f" 2>/dev/null; then pass; else fail "$f (sh syntax)"; fi ;;
    *awk*)
      skip "$f" "awk 無語法檢查模式" ;;
    *perl*)
      if ! command -v perl >/dev/null; then skip "$f" "無 perl"
      elif perl -c "$f" >/dev/null 2>&1; then pass
      else
        perl_err=$(perl -c "$f" 2>&1 || true)
        case "$perl_err" in
          *"Can't locate"*) warn "$f (缺 perl module)" ;;
          *) fail "$f (perl syntax)" ;;
        esac
      fi ;;
    *)
      skip "$f" "其他直譯器" ;;
  esac
done

echo
echo "== 可執行位 =="
for f in *; do
  [ -f "$f" ] || continue
  is_doc_or_data "$f" && continue
  if [ -x "$f" ]; then pass; else warn "$f 沒有 +x"; fi
done

echo
echo "== 外部依賴 =="
deps="ffmpeg mogrify optipng adb git svn repo mysql mysqldump sqlite3 go perl python3 pv bsdtar mitmproxy tmux byobu wget docker gradle nano less tree lsof curl"
for d in $deps; do
  if command -v "$d" >/dev/null 2>&1; then pass; else warn "dep 不存在: $d"; fi
done

echo
echo "==================================="
echo "PASS: $PASS  FAIL: $FAIL  WARN: $WARN  SKIP: $SKIP"
[ "$FAIL" -eq 0 ]
