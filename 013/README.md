# 第13章 アセットを組み立てる ― モデル階層と Kind

通り・区画・家・屋根に Kind を付け、モデルの境界と親の Kind が判定に与える影響を確認します。

## 必要な環境

Windows の PowerShell と [共通環境](../README.md#共通環境)（uv、Python 3.13 系、`usd-core` 26.11）を使います。

## 事前準備

[第12章の手順](../012/README.md)で地区色を更新し、`work/path-lab/receiver/street-v2.usdz` を作ります。ここからは、その USDZ と同じフォルダにレイヤーを重ねます。

## 実行手順

クローンしたリポジトリのルートか `013` フォルダで PowerShell を開きます。以下のブロックは同じウィンドウで順に実行してください。

```powershell
$repo = (git rev-parse --show-toplevel)
Set-Location $repo
uv sync --locked
$python = Join-Path $repo '.venv/Scripts/python.exe'
function Invoke-Sample($file) { & $python (Join-Path $repo $file) @args }
Set-Location work/path-lab/receiver
```

```powershell
Invoke-Sample 013/build_models.py
Invoke-Sample 013/inspect_models.py
```

## 期待される結果

`street_models.usda` が USDZ の隣にできます。通りは `assembly`、区画は `group`、家は `component`、屋根は `subcomponent` です。`models` の一覧と個々の Prim の `model` 判定を比較できます。

## ファイル一覧

- [build_models.py](build_models.py) — 受領した通りに Kind を設定したレイヤーを重ねる。
- [inspect_models.py](inspect_models.py) — Kind の派生関係と階層内でのモデル判定を表示する。
