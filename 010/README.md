# 第10章 ファイル変換とツール群（usdcat / usdzip）

通りのルートを USDC に変換し、パスと長さの単位を整えてから依存ファイルごと USDZ にまとめます。

## 必要な環境

Windows の PowerShell と [共通環境](../README.md#共通環境)（uv、Python 3.13 系、`usd-core` 26.11）を使います。

本文の `usdcat`（表示・変換）、`usdzip`（梱包・一覧）、`usdchecker` と `usdtree`（配布物の検査）を試す場合は、別の PowerShell で conda-forge の `openusd` 26.08 環境を有効にします。conda が使える端末で初回に `conda create -n usd-cli -c conda-forge python=3.13 openusd=26.08`、利用時に `conda activate usd-cli` を実行してください。

## 事前準備

[第9章の手順](../009/README.md)で `work/street_rules.usda` を作ります。`street_choices.usda`、`street.usda`、`house_choices.usda`、`assembly.usda`、`house.usda`、`look.usda`、`paint.usda` も必要です。`work/exchange-work` を新しく作り、その中のコピーを編集します。

## 実行手順

クローンしたリポジトリのルートか `010` フォルダで PowerShell を開きます。以下のブロックは同じウィンドウで順に実行してください。

```powershell
$repo = (git rev-parse --show-toplevel)
Set-Location $repo
uv sync --locked
$python = Join-Path $repo '.venv/Scripts/python.exe'
function Invoke-Sample($file) { & $python (Join-Path $repo $file) @args }
Set-Location work
```

本文の CLI 実習を並行して試すときは、別の作業コピーを用意してください。以下は同じ配布用ファイルを Python API で作る手順です。`prepare_delivery.py` はコピー側の `assembly.usda` に相対パスの接頭辞 `./` を付けるので、変換直後のコピーに1回だけ実行します。

```powershell
New-Item -ItemType Directory exchange-work
Copy-Item *.usda exchange-work
Set-Location exchange-work
& $python -c "from pxr import Sdf; assert Sdf.Layer.FindOrOpen('street_rules.usda').Export('street_rules.usdc')"
Invoke-Sample 010/prepare_delivery.py

function New-UsdPackage($source, $destination) {
    & $python -c "import sys; from pxr import UsdUtils; sys.exit(0 if UsdUtils.CreateNewUsdzPackage(sys.argv[1], sys.argv[2]) else 1)" $source $destination
    if ($LASTEXITCODE -ne 0) { throw "USDZ の作成に失敗しました: $destination" }
}
New-UsdPackage street_rules.usdc street.usdz
Invoke-Sample 010/check_street.py
```

## 期待される結果

`work/exchange-work` に `street_rules.usdc` と `street.usdz` ができます。USDZ のルートは `/Street`、西の屋根は黄、東は緑で、どちらも `years=30` です。第12章には USDZ と別に、変換した USDC と依存レイヤーを渡します。

## ファイル一覧

- [prepare_delivery.py](prepare_delivery.py) — コピー側のサブレイヤーパスを明示し、USDC に単位を記録する。
- [check_street.py](check_street.py) — 配布用 USDZ を開いて既定の Prim、瓦の材質・色・耐用年数を読む。
