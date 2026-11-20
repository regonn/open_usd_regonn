# 第24章 総合演習 ― ひとつのシーンを完成させる

通りに道路を配置し、点検スキーマを添えた USDZ を作ります。受け手のフォルダで完成条件を検査します。

## 必要な環境

Windows の PowerShell と [共通環境](../README.md#共通環境)（uv、Python 3.13 系、`usd-core` 26.11）を使います。

本文の `usdchecker --strict` で梱包前後を検査し、`usdzip` で依存ファイルをまとめる場合は、別の PowerShell で conda-forge の `openusd` 26.08 環境を有効にします。環境の作り方は[第10章の必要な環境](../010/README.md#必要な環境)を参照してください。

## 事前準備

[第23章の手順](../023/README.md)で `work/path-lab/receiver/batch-20` に `street_inspection.usda` と `streetInspection/resources` の `plugInfo.json`、`generatedSchema.usda` を用意します。`street_delivery.usda` 以下、`street-v2.usdz` までの依存ファイルも必要です。

## 実行手順

クローンしたリポジトリのルートか `024` フォルダで PowerShell を開きます。以下のブロックは同じウィンドウで順に実行してください。

```powershell
$repo = (git rev-parse --show-toplevel)
Set-Location $repo
uv sync --locked
$python = Join-Path $repo '.venv/Scripts/python.exe'
function Invoke-Sample($file) { & $python (Join-Path $repo $file) @args }
Set-Location work/path-lab/receiver/batch-20
```

以下では Python API で梱包し、`receiver-24` に USDZ を置き、その下の `streetInspection/resources` にプラグイン用の2ファイルを添えます。本文の CLI 検証も行う場合は `build_final.py` の後にソースを、梱包後に USDZ を `usdchecker --strict` で検査してください。

```powershell
function New-UsdPackage($source, $destination) {
    & $python -c "import sys; from pxr import UsdUtils; sys.exit(0 if UsdUtils.CreateNewUsdzPackage(sys.argv[1], sys.argv[2]) else 1)" $source $destination
    if ($LASTEXITCODE -ne 0) { throw "USDZ の作成に失敗しました: $destination" }
}

Invoke-Sample 024/build_final.py
New-Item -ItemType Directory receiver-24/streetInspection/resources
New-UsdPackage street_final.usda receiver-24/street-final.usdz
Copy-Item streetInspection/resources/plugInfo.json,streetInspection/resources/generatedSchema.usda receiver-24/streetInspection/resources
Set-Location receiver-24
Invoke-Sample 024/check_final.py
```

## 期待される結果

`road.usda` と `street_final.usda` ができ、`receiver-24` に `street-final.usdz` と点検プラグインがそろいます。受け手側の検査は西 `passed`、東 `pending`、カメラ `/Shot/StreetCam` を表示し、最後に `All file-backed layers resolve in the delivered USDZ.` と出力します。

## ファイル一覧

- [build_final.py](build_final.py) — 道路を別のアセットとして作り、通りに配置して最終ステージを保存する。
- [check_final.py](check_final.py) — 受け手側でプラグインを登録し、ロード、屋根・点検値、道路、カメラ、依存先を検査する。
