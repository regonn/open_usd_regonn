# 第7章 参照とペイロード

西の家を参照、東の家をペイロードで配置し、ロード状態と屋根の有無を比較します。

## 必要な環境

Windows の PowerShell と [共通環境](../README.md#共通環境)（uv、Python 3.13 系、`usd-core` 26.11）を使います。

## 事前準備

`work` に `assembly.usda` と、そのサブレイヤー `paint.usda`、`look.usda`、`house.usda` が必要です。[第6章の手順](../006/README.md)でレイヤーを組み、4枚を同じ場所に置きます。

## 実行手順

クローンしたリポジトリのルートか `007` フォルダで PowerShell を開きます。以下のブロックは同じウィンドウで順に実行してください。

```powershell
$repo = (git rev-parse --show-toplevel)
Set-Location $repo
uv sync --locked
$python = Join-Path $repo '.venv/Scripts/python.exe'
function Invoke-Sample($file) { & $python (Join-Path $repo $file) @args }
Set-Location work
```

```powershell
Invoke-Sample 007/build_street.py
Invoke-Sample 007/inspect_street.py
```

## 期待される結果

`work/street.usda` ができます。`westRoof` は常に `True` で、`eastRoof` は `open`、`load`、`unload` の順に `False`、`True`、`False` と変わります。

## ファイル一覧

- [build_street.py](build_street.py) — 東西に家を配置して通りを保存する。
- [inspect_street.py](inspect_street.py) — 東の家をロード・アンロードして Prim の有無を表示する。
