# 第16章 レンダリングと Hydra の基礎

同じカメラに下見用と確認用の描画設定を作ります。本文の Kit 実習では、その2つの解像度で画像を撮影します。

## 必要な環境

Windows の PowerShell と [共通環境](../README.md#共通環境)（uv、Python 3.13 系、`usd-core` 26.11）を使います。 ステージの作成は共通環境で実行できます。Viewport の実習には RTX GPU と [序章で構築する Kit 110.4.1](../000/README.md) を使います。

## 事前準備

[第15章の手順](../015/README.md)で `/Shot/StreetCam` とライトを持つ `street_lighting.usda` を生成します。`work/path-lab/receiver` の `street_collections.usda`、`street_models.usda`、`street-v2.usdz` も同じ場所に残してください。

## 実行手順

クローンしたリポジトリのルートか `016` フォルダで PowerShell を開きます。以下のブロックは同じウィンドウで順に実行してください。

```powershell
$repo = (git rev-parse --show-toplevel)
Set-Location $repo
uv sync --locked
$python = Join-Path $repo '.venv/Scripts/python.exe'
function Invoke-Sample($file) { & $python (Join-Path $repo $file) @args }
Set-Location work/path-lab/receiver
```

撮影コードは Kit の Viewport とイベントループを使うため未収録です。PNG を作る場合は、Kit で生成した `street_render.usda` を開いて **Stage Lights** を選び、本文「Kit で設定を読み、2枚の PNG を描く」のコードを Script Editor で実行してください。

```powershell
Invoke-Sample 016/build_render.py
```

## 期待される結果

`street_render.usda` ができます。`/Render/Draft` は 160 × 90、`/Render/Review` は 960 × 540 で、どちらも `/Shot/StreetCam` を指します。本文の撮影まで行うと `street-draft.png` と `street-review.png` が USDA の隣にできます。

## ファイル一覧

- [build_render.py](build_render.py) — 2つの `UsdRender.Settings` に解像度とカメラを記録する。
