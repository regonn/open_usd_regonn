# 第8章 バリアントとバリアントセット

瓦の仕上げを2種類用意し、家に保存した選択とセッション中だけの選択を比較します。

## 必要な環境

Windows の PowerShell と [共通環境](../README.md#共通環境)（uv、Python 3.13 系、`usd-core` 26.11）を使います。

## 事前準備

[第7章の手順](../007/README.md)で作った `work/street.usda` と、参照・ペイロードの依存先 `assembly.usda`、`paint.usda`、`look.usda`、`house.usda` を一緒に使います。

## 実行手順

クローンしたリポジトリのルートか `008` フォルダで PowerShell を開きます。以下のブロックは同じウィンドウで順に実行してください。

```powershell
$repo = (git rev-parse --show-toplevel)
Set-Location $repo
uv sync --locked
$python = Join-Path $repo '.venv/Scripts/python.exe'
function Invoke-Sample($file) { & $python (Join-Path $repo $file) @args }
Set-Location work
```

```powershell
Invoke-Sample 008/house_choices.py
Invoke-Sample 008/street_choices.py
Invoke-Sample 008/read_choices.py
```

## 期待される結果

`work` に `house_choices.usda` と `street_choices.usda` ができます。東の家は `saved` で `ocean`、`preview` で `terracotta`、`restored` で `ocean` に戻ります。

## ファイル一覧

- [house_choices.py](house_choices.py) — 家に屋根のバリアントセットを定義する。
- [street_choices.py](street_choices.py) — 東西の家にバリアント付きの部品を使い、東の屋根を青にする。
- [read_choices.py](read_choices.py) — セッションレイヤーで選択を一時変更し、保存値との違いを表示する。
