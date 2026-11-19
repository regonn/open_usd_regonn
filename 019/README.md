# 第19章 Python によるバッチ処理と自動化

4つのステージに同じ検査を適用し、不合格を CSV で特定してから、合格した一式を USDC に変換します。

## 必要な環境

Windows の PowerShell と [共通環境](../README.md#共通環境)（uv、Python 3.13 系、`usd-core` 26.11）を使います。

## 事前準備

[第18章の手順](../018/README.md)を終え、`work/path-lab/receiver` に `street_check.usda`（修復済み）、`street_cycle.usda`、`blocks_plain.usda`、`blocks_shared.usda` と依存レイヤー、`street-v2.usdz` をそろえます。新しい `batch-19` のコピーにだけ循環を再現します。

## 実行手順

クローンしたリポジトリのルートか `019` フォルダで PowerShell を開きます。以下のブロックは同じウィンドウで順に実行してください。

```powershell
$repo = (git rev-parse --show-toplevel)
Set-Location $repo
uv sync --locked
$python = Join-Path $repo '.venv/Scripts/python.exe'
function Invoke-Sample($file) { & $python (Join-Path $repo $file) @args }
Set-Location work/path-lab/receiver
```

```powershell
New-Item -ItemType Directory batch-19
Copy-Item *.usda,street-v2.usdz -Destination batch-19
Set-Location batch-19
$roots = 'street_check.usda','street_cycle.usda','blocks_plain.usda','blocks_shared.usda'
Invoke-Sample 018/cycle.py create
Invoke-Sample 019/batch_street.py --export @roots
# 1回目は循環参照で1件が FAIL になる。結果を残してから修復する。
Copy-Item report.csv report-before.csv
Invoke-Sample 018/cycle.py repair
Invoke-Sample 019/batch_street.py --export @roots
```

## 期待される結果

1回目は `PASS=3 FAIL=1`（終了コード 1）で、修復前の記録を `report-before.csv` に残します。修復後は `PASS=4 FAIL=0` となり、`batch-19` に `report.csv` と4つの `*.review.usdc` ができます。

## ファイル一覧

- [batch_street.py](batch_street.py) — 指定された全ステージを検査し、CSV に集計する。`--export` は全件合格したときにルートレイヤーを変換する。
