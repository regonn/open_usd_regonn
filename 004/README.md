# 第4章 ジオメトリを作る ― Mesh の基礎

5つの頂点を壁と屋根の2面に分け、家の Mesh のトポロジーを確認します。

## 必要な環境

Windows の PowerShell と [共通環境](../README.md#共通環境)（uv、Python 3.13 系、`usd-core` 26.11）を使います。

## 事前準備

入力ファイルは不要です。家と通りの実習を始める読者は、この章から進められます。

## 実行手順

クローンしたリポジトリのルートか `004` フォルダで PowerShell を開きます。以下のブロックは同じウィンドウで順に実行してください。

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
Invoke-Sample 004/mesh.py
Invoke-Sample 004/read_mesh.py
```

## 期待される結果

`work/house.usda` ができます。`5 points, 2 faces` に続き、壁は `[0, 1, 2, 3]`、屋根は `[3, 2, 4]` と表示されます。

## ファイル一覧

- [mesh.py](mesh.py) — 壁と屋根のトポロジーを検査し、面ごとに色を付けて保存する。
- [read_mesh.py](read_mesh.py) — 頂点数・面数・面ごとの頂点番号を表示する。
