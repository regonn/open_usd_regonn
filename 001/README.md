# 第1章 ファイルフォーマットと Python API 環境構築

既定の Prim を持つステージを作り、球をテキスト形式の USDA に保存します。

## 必要な環境

Windows の PowerShell と [共通環境](../README.md#共通環境)（uv、Python 3.13 系、`usd-core` 26.11）を使います。

## 事前準備

入力ファイルは不要です。序章で作った Cube とは別のステージを作ります。

## 実行手順

クローンしたリポジトリのルートか `001` フォルダで PowerShell を開きます。以下のブロックは同じウィンドウで順に実行してください。

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
Invoke-Sample 001/stage.py
```

## 期待される結果

`work/stage.usda` ができ、`Stage created with Default Prim: Root` と表示されます。ファイルを開くと `/Root` の下に半径 1 の `Sphere` があります。

## ファイル一覧

- [stage.py](stage.py) — 既定の Prim `/Root` と球を作り、保存する。
