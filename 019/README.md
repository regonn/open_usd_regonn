# 第19章 合成エラーとパフォーマンスの調べ方

循環する内部参照を修復し、通りを256区画に配置した場合のインスタンス化の効果を測ります。

## 必要な環境

Windows の PowerShell と [共通環境](../README.md#共通環境)（uv、Python 3.13 系、`usd-core` 26.11）を使います。

本文の `usdchecker --skipVariants street_cycle.usda` で循環の修復前後を比較する場合は、別の PowerShell で conda-forge の `openusd` 26.08 環境を有効にします。環境の作り方は[第10章の必要な環境](../010/README.md#必要な環境)を参照してください。

## 事前準備

[第18章の手順](../018/README.md)で `street_check.usda` の参照と色を両方修復します。`work/path-lab/receiver` に `street_render.usda` 以下のレイヤーと `street-v2.usdz` を残します。

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

循環を作った直後の警告が診断対象です。本文の CLI でも確かめるには、`create` と `repair` の直後にそれぞれ `usdchecker --skipVariants street_cycle.usda` を実行してください。

```powershell
Invoke-Sample 019/cycle.py create
Invoke-Sample 019/cycle.py repair
Invoke-Sample 019/build_blocks.py
Invoke-Sample 019/measure_stage.py blocks_plain.usda
Invoke-Sample 019/measure_stage.py blocks_shared.usda
```

## 期待される結果

`street_cycle.usda` の修復後は `composition errors: 0` で `/PlanA/House` が Mesh になります。`blocks_plain.usda` と `blocks_shared.usda` の `primary prims`、`instances`、`open_ms` を比較できます。所要時間は環境によって変わります。

## ファイル一覧

- [cycle.py](cycle.py) — `create` で循環を作り、`repair` で戻り先を変更して再診断する。
- [build_blocks.py](build_blocks.py) — 通常参照とインスタンス化を使い、2種類の256区画を生成する。
- [measure_stage.py](measure_stage.py) — 指定したステージの起動時間、Prim・インスタンス・レイヤーの数を表示する。
