# 第9章 継承・スペシャライズと合成の優先順位（LIVRPS）

地区と瓦のクラスを作り、ローカル値・継承・バリアント・スペシャライズが競合したときの屋根色を読みます。

## 必要な環境

Windows の PowerShell と [共通環境](../README.md#共通環境)（uv、Python 3.13 系、`usd-core` 26.11）を使います。

## 事前準備

`work/street_choices.usda` と、依存する `street.usda`、`house_choices.usda`、`assembly.usda`、`paint.usda`、`look.usda`、`house.usda` を同じ場所に置きます。[第8章の手順](../008/README.md)で家と通りの両方のバリアント用ファイルを生成してください。

## 実行手順

クローンしたリポジトリのルートか `009` フォルダで PowerShell を開きます。以下のブロックは同じウィンドウで順に実行してください。

```powershell
$repo = (git rev-parse --show-toplevel)
Set-Location $repo
uv sync --locked
$python = Join-Path $repo '.venv/Scripts/python.exe'
function Invoke-Sample($file) { & $python (Join-Path $repo $file) @args }
Set-Location work
```

```powershell
Invoke-Sample 009/build_rules.py
Invoke-Sample 009/read_rules.py
```

## 期待される結果

`work/street_rules.usda` ができます。`saved` では西はローカルの黄、東は地区の緑、耐用年数は両方とも `30` です。東の継承を一時的に外すとバリアントの青が現れます。

## ファイル一覧

- [build_rules.py](build_rules.py) — 地区色と瓦の基礎値を定義し、各家の瓦に合成アークを加える。
- [read_rules.py](read_rules.py) — 保存値・継承を外した値・復元後の値を比較する。
