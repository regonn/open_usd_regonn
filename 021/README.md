# 第21章 バリデーションとアセット検証（UsdChecker）

単位の欠落と点検用の球の配置を順に修復し、検証するルールやバリアントによって検出結果が変わることを確かめます。

## 必要な環境

Windows の PowerShell と [共通環境](../README.md#共通環境)（uv、Python 3.13 系、`usd-core` 26.11）を使います。

本文の `usdchecker` でルールを選び、修復の各段階で合否を調べる場合は、別の PowerShell で conda-forge の `openusd` 26.08 環境を有効にします。環境の作り方は[第10章の必要な環境](../010/README.md#必要な環境)を参照してください。

## 事前準備

[第20章の手順](../020/README.md)で4件すべてを合格させ、`work/path-lab/receiver/batch-20` に `street_check.review.usdc` を作ります。`street_render.usda` 以下の依存レイヤーと `street-v2.usdz` も同じ場所に必要です。

## 実行手順

クローンしたリポジトリのルートか `021` フォルダで PowerShell を開きます。以下のブロックは同じウィンドウで順に実行してください。

```powershell
$repo = (git rev-parse --show-toplevel)
Set-Location $repo
uv sync --locked
$python = Join-Path $repo '.venv/Scripts/python.exe'
function Invoke-Sample($file) { & $python (Join-Path $repo $file) @args }
Set-Location work/path-lab/receiver/batch-20
```

CLI も試す場合は、以下を1行ずつ進めます。作成直後に `usdchecker --skipVariants street_delivery.usda`、単位の修復直後に `usdchecker street_delivery.usda --variants reviewMode:inspection`、点検球の修復後に `usdchecker --strict street_delivery.usda` を同じ作業フォルダで実行してください。ルールの一覧と検証ログの保存方法は本文の第21章にあります。

```powershell
Invoke-Sample 021/create_delivery.py
# 本文の CLI で検証する場合は、ここで単位の欠落を確認する。
Invoke-Sample 021/repair_delivery.py units
# 次に inspection を検証し、点検球の配置を確認する。
Invoke-Sample 021/repair_delivery.py marker
```

## 期待される結果

`street_delivery.usda` ができます。修復後は `metersPerUnit` が `0.01` で、`inspection` の点検球は `/Street/West/Marker` にあります。本文の全バリアントの厳格検査もこの状態で行います。

## ファイル一覧

- [create_delivery.py](create_delivery.py) — 単位の記述を省き、点検バリアント内で家の下に球を置く。
- [repair_delivery.py](repair_delivery.py) — `units` で長さの単位を記録し、`marker` で点検球を区画の直下へ移す。
