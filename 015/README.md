# 第15章 コレクションとシーンの整理

家、屋根、西区画の調査対象をコレクションにし、含まれる Prim を名前から取得します。

## 必要な環境

Windows の PowerShell と [共通環境](../README.md#共通環境)（uv、Python 3.13 系、`usd-core` 26.11）を使います。

## 事前準備

`work/path-lab/receiver` に `street_models.usda` と `street-v2.usdz` が必要です。[第14章の手順](../014/README.md)で第2版の通りに Kind を設定してください。

## 実行手順

クローンしたリポジトリのルートか `015` フォルダで PowerShell を開きます。以下のブロックは同じウィンドウで順に実行してください。

```powershell
$repo = (git rev-parse --show-toplevel)
Set-Location $repo
uv sync --locked
$python = Join-Path $repo '.venv/Scripts/python.exe'
function Invoke-Sample($file) { & $python (Join-Path $repo $file) @args }
Set-Location work/path-lab/receiver
```

```powershell
Invoke-Sample 015/build_collections.py
Invoke-Sample 015/inspect_collections.py
```

## 期待される結果

`street_collections.usda` ができます。`houses` は東西の家、`roofs` は両方の `RoofFaces` を列挙します。`westSurvey` は西区画を展開し、`Looks` の枝を除外します。

## ファイル一覧

- [build_collections.py](build_collections.py) — 3つのコレクションに対象・除外・展開規則を設定する。
- [inspect_collections.py](inspect_collections.py) — 各コレクションの成員と調査対象の includes を表示する。
