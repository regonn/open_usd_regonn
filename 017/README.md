# 第17章 診断ツールでステージを読む

西の参照切れと東の意図しない屋根色を作り、合成エラーと属性の出典を手掛かりに順番に直します。

## 必要な環境

Windows の PowerShell と [共通環境](../README.md#共通環境)（uv、Python 3.13 系、`usd-core` 26.11）を使います。

本文の `usdchecker --skipVariants` と `usdcat` で修復前後の状態を調べる場合は、別の PowerShell で conda-forge の `openusd` 26.08 環境を有効にします。環境の作り方は[第10章の必要な環境](../010/README.md#必要な環境)を参照してください。

## 事前準備

[第16章の手順](../016/README.md)で `work/path-lab/receiver/street_render.usda` を作ります。`street_lighting.usda` 以下のサブレイヤーと `street-v2.usdz` が読み込める状態で使います。撮影画像は不要です。

## 実行手順

クローンしたリポジトリのルートか `017` フォルダで PowerShell を開きます。以下のブロックは同じウィンドウで順に実行してください。

```powershell
$repo = (git rev-parse --show-toplevel)
Set-Location $repo
uv sync --locked
$python = Join-Path $repo '.venv/Scripts/python.exe'
function Invoke-Sample($file) { & $python (Join-Path $repo $file) @args }
Set-Location work/path-lab/receiver
```

本文の CLI 診断も行う場合は、各 `inspect_street.py` の直後に、同じファイルに対して `usdchecker --skipVariants` を実行してください。参照の修復直後には、東の屋根色の上書きがまだ残っています。

```powershell
Invoke-Sample 017/inspect_street.py street_render.usda
Invoke-Sample 017/make_faults.py
Invoke-Sample 017/inspect_street.py street_check.usda
Invoke-Sample 017/repair_street.py reference
Invoke-Sample 017/inspect_street.py street_check.usda
Invoke-Sample 017/repair_street.py tint
Invoke-Sample 017/inspect_street.py street_check.usda
```

## 期待される結果

`street_check.usda` ができます。故障時は西の家を Mesh として取得できず、東の色は緑になります。両方を修復すると `composition errors: 0`、西は Mesh、東の色は第12章の紫に戻ります。

## ファイル一覧

- [inspect_street.py](inspect_street.py) — 引数のステージの統計、合成エラー数、屋根色と属性の出典を表示する。
- [make_faults.py](make_faults.py) — 新しいレイヤーで西の参照先と東の屋根色を上書きする。
- [repair_street.py](repair_street.py) — `reference` または `tint` を指定して対応する上書きを取り除く。
