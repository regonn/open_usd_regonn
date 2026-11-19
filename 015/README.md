# 第15章 カメラとライト（UsdLux）

同じ構図で照明を比較するため、通りにカメラと3種類のライトを置きます。

## 必要な環境

Windows の PowerShell と [共通環境](../README.md#共通環境)（uv、Python 3.13 系、`usd-core` 26.11）を使います。 ステージの作成は共通環境で実行できます。Viewport の実習には RTX GPU と [序章で構築する Kit 110.4.1](../000/README.md) を使います。

## 事前準備

[第14章の手順](../014/README.md)で `street_collections.usda` を作り、`street_models.usda` と `street-v2.usdz` と一緒に `work/path-lab/receiver` に残します。

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

見え方を比べるには、Kit で `street_lighting.usda` を開き、カメラに `/Shot/StreetCam`、照明に **Stage Lights** を選びます。本文「Kit で同じ構図の3枚を見比べる」に沿って `Sun`、`WestLamp`、`EastPanel` を1灯ずつ点けてください。

```powershell
Invoke-Sample 015/build_lighting.py
Invoke-Sample 015/inspect_lighting.py
```

## 期待される結果

`street_lighting.usda` ができます。読み戻すと水平画角は約 36.87 度で、家のパスと3灯の設定が表示されます。初期状態では `/Shot/Sun` が見え、残り2灯は非表示です。

## ファイル一覧

- [build_lighting.py](build_lighting.py) — 通りに `StreetCam`、日光、西の球形ライト、東の面光源を追加する。
- [inspect_lighting.py](inspect_lighting.py) — 水平画角、撮影対象の家、各ライトの値を読み戻す。
