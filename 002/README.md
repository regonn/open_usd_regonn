# 第2章 Prim の親子階層と座標変換

親を回転・移動したとき、Cube と Sphere の原点がワールド空間のどこに来るかを調べます。

## 必要な環境

Windows の PowerShell と [共通環境](../README.md#共通環境)（uv、Python 3.13 系、`usd-core` 26.11）を使います。

## 事前準備

入力ファイルは不要です。この章は空の `work` から始められます。

## 実行手順

クローンしたリポジトリのルートか `002` フォルダで PowerShell を開きます。以下のブロックは同じウィンドウで順に実行してください。

```powershell
$repo = (git rev-parse --show-toplevel)
Set-Location $repo
uv sync --locked
$python = Join-Path $repo '.venv/Scripts/python.exe'
function Invoke-Sample($file) { & $python (Join-Path $repo $file) @args }
New-Item -ItemType Directory -Force work | Out-Null
Set-Location work
```

```powershell
Invoke-Sample 002/hierarchy.py
```

## 期待される結果

`work/hierarchy.usda` ができます。Cube の原点はローカルで `(2, 0, 0)`、ワールドで `(10, 2, 0)` です。Sphere のワールド座標は `(7, 0, 0)` です。

## ファイル一覧

- [hierarchy.py](hierarchy.py) — 親の Xform と2つの子を保存し、各原点の座標を表示する。
