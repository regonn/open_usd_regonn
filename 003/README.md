# 第3章 属性・プロパティ・リレーションシップ

Cube の属性に時刻ごとの値を設定し、Sphere を指すリレーションシップを読み戻します。

## 必要な環境

Windows の PowerShell と [共通環境](../README.md#共通環境)（uv、Python 3.13 系、`usd-core` 26.11）を使います。

## 事前準備

`work/hierarchy.usda` に `/Root/Group/Cube` と `/Root/Group/Sphere` が必要です。[第2章の手順](../002/README.md)で `hierarchy.py` を実行すると両方がそろいます。

## 実行手順

クローンしたリポジトリのルートか `003` フォルダで PowerShell を開きます。以下のブロックは同じウィンドウで順に実行してください。

```powershell
$repo = (git rev-parse --show-toplevel)
Set-Location $repo
uv sync --locked
$python = Join-Path $repo '.venv/Scripts/python.exe'
function Invoke-Sample($file) { & $python (Join-Path $repo $file) @args }
Set-Location work
```

```powershell
Invoke-Sample 003/properties.py
```

## 期待される結果

`work/properties.usda` ができます。温度の既定値は `20.0`、時刻 13 の補間値は `40.0` です。`targets` は `/Root/Group/Sphere` を指し、`target exists: True` と表示されます。

## ファイル一覧

- [properties.py](properties.py) — 階層のコピーにサイズ・ラベル・温度・参照相手を設定して読み戻す。
