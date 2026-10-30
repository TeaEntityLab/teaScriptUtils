# Governance & Flows

teaScriptUtils 是個人日常腳本庫。全部腳本平鋪在 repo 根目錄（不放子資料夾），
透過把此目錄加進 `PATH` 直接呼叫。本文件整理目前用法、慣例與安全分級。

## 結構慣例

- **平鋪**：新腳本直接放根目錄。`avc/`、`docker/` 是早期遺留的例外。
- **可執行**：`chmod +x`，無副檔名（`download_to_mp3`、`mergeav`）或 `.sh` 皆可。
- **Python**：`.py` 結尾加 shebang，直接用檔名呼叫。
- **`.bat`**：Windows 專用，macOS/Linux 不會用到。
- **source 型腳本**：`cd*`、`prepareAOSP` 這類改變當前 shell 狀態的腳本，
  必須用 `. cdapp` / `source cdapp` 執行才有效，直接執行無作用。

## 驗證（Harness）

`./check.sh` 是本 repo 的最小驗證 harness，只做靜態檢查、不執行任何腳本：

- shell 腳本：用 shebang 指定的 shell 做 `-n` 語法檢查
- python3：`py_compile`；python2 時代腳本標 `SKIP`（本機無 py2）
- 預期可執行的檔案檢查 `+x`
- 掃描 GOVERNANCE 列出的外部依賴是否都在 `PATH`（缺的列 `WARN`，不算 FAIL）

結束碼 0 = 無 FAIL。改動或新增腳本後跑一次即可；`WARN`/`SKIP` 為資訊性，
多半是 legacy 腳本或本機沒裝的選用工具。

## 新增腳本規範

- 一個腳本只做一件事；檔頭註明用途與用法，或參數不足時印 usage。
- 含空白檔名一律 `"$var"`、`for f in "$@"` 處理。
- 新 bash 腳本建議 `set -euo pipefail`（舊腳本沒有，不強求回補）。
- 寫死個人機器路徑的（`cd*`、`repoinitsync.sh`、`go133`）屬 env-specific，
  換機器即失效，可接受但要在檔頭或本文件標示。
- 破壞性操作（rm、reset --hard、revert）要先檢查參數並印出將做的事。

## 安全分級

### 破壞性 — 執行前看清楚

| 腳本 | 行為 |
| --- | --- |
| `rr` | `rm -rf $1` |
| `gitresetclean.sh` | `git reset --hard` + `git clean -di` |
| `svnreverthead` | 刪除 untracked + revert 全部 + 退回指定 revision |
| `repoclean` | repo forall git clean -f -d |
| `clearUp.sh` | 清空系統 log 與 bash history（需 root） |
| `pk.sh` | `kill -9` 所有 grep 到的 process |
| `flattenfiles.sh` | 搬動目錄下所有檔案，改變目錄結構 |

### 需 sudo / 特殊權限

`aptin`、`aptrm`、`mitm.sh`（iptables 轉發）、`installMitmproxy`、`pupriv`/`pusys`（adb remount）

### env-specific（寫死路徑或內網，換環境即失效）

`cd85` `cd86` `cdandroid` `cdaosp` `cdapp` `cdios`、`cpimg89`、`mkbeango` `mkcocos2dx` `mkinhon_89_shevdo_mm`、
`prepareAOSP`、`repoinitsync.sh`（192.168.10.120）、`go133`、`runmydoku`、`monitorMysql.sh`

### 唯讀 / 安全

`scanip.sh`、`seekps.sh`、`psport`、`du.sh`、`bitcoinrate`、`hexall`、`ptandroid`、
`findgrep`、`gitlogcolor`、`imagemagick_list_fonts.sh`

## 外部依賴

`ffmpeg`、`imagemagick (mogrify/convert)`、`optipng`、`adb`、`git`、`svn`、`repo`、
`mysql`/`mysqldump`/`sqlite3`、`go`、`perl HTML::WikiConverter`、`python3`、
`pv`+`bsdtar`（fastcp）、`mitmproxy`、`tmux`/`byobu`、`wget`、`docker`、`gradle`

## Flows — 目前的主要用法

### 影音處理（ffmpeg）

```
下載素材 (yt-dlp 等) → mergeav 合併影音軌 → 視需要後續處理
```

| 腳本 | 用途 |
| --- | --- |
| `mergeav` | 影片 + 音軌合併成單一檔，stream copy 不轉檔 |
| `download_to_mp3` | 批次把影片轉 mp3：`<集數> <檔案...>` → `集數-N.mp3` |
| `compress_mp4` | 壓縮成 360p x264 |
| `mp42mkv.sh` | 目錄下所有 mp4 批次轉 mkv（copy） |
| `tsconvert.sh` | 目錄下所有 ts 批次轉 mp4（copy） |

典型流程：yt-dlp 下載 YouTube 分離的影像與音訊檔 → `mergeav a.mp4 a.m4a` → 完成。
要再壓縮才接 `compress_mp4`，要抽聲音才接 `download_to_mp3`。

### 圖片批次

`mogrifyjpgall.sh`（縮到 1000px + 70% quality）、`mogrifypngall.sh`、
`optipngall.sh`、`imagemagick_list_fonts.sh`、`imagemagick_test_fonts.sh`

### Git / repo 管理

`cloneAllGithub.sh`、`cloneAllBitbucket.sh`（整批 clone）、`repoinitsync.sh`、`reposync`、
`repoclean`、`gitresetclean.sh`、`svnreverthead`、`gitlogcolor`、`gitcobyreporthead.py`

### Android 開發 / 測試（多為前工作環境遺留）

adb：`coloradb`、`kadb`、`startActivity`、`pupriv`、`pusys`、`scanip.sh`
建置：`android-sdkmanager-bootstrap.sh`、`mk*`、`prepareAOSP`
CTS/XTS：`ctsAutoSetup.*`、`ctsparsinglib.py`、`mobiletestlib.py`、
`launchCTS/XTSwithErrorDetection.*`、`runEachTestWithDelay.py`、`runPkgChild.py`、
`*-tradefed.bat` — Python 2 時代、依賴舊測試框架，視為 legacy。

### 檔案 / 傳輸 / 備份

`fastcp`（tar+pv 高速複製）、`cpfromserver.sh`、`cptoserver.sh`（ssh+tar 管道）、
`flattenfiles.sh`、`wgetmirror.sh`、`mergetxt.py`（vtt 字幕合併成純文字）、
`backupMe`、`backupmysql2sqlite`+`mysql2sqlite`、`gitblitbackup.bat`、`wikibackup.bat`

### Shell 環境 / 系統雜項

`bashrcAdd.sh`、`bashrcEdit.sh`、`tmux-session`（save/restore）、`du.sh`、
`scanip.sh`、`seekps.sh`、`psport`、`pk.sh`、`clearUp.sh`、`go133`、
`bitcoinrate`、`hexall`、`ptandroid`、`pinyinToZhuyinDialnumCodegen.py`、
`html2doku.pl`、`runmydoku`、`mitm.sh`、`gotestcov.sh`、`docker/`（mysql、mongoredis 啟停）
