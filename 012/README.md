# 第12章 USDZ パッケージと配布

修復済みの通りを梱包し、配布先で形状の読み込み元と屋根色を確認してから、第2版を届けます。

## 必要な環境

Windows の PowerShell と [共通環境](../README.md#共通環境)（uv、Python 3.13 系、`usd-core` 26.11）を使います。

本文の `usdzip -a`・`usdzip -l` で梱包・一覧を確認し、`usdchecker` で受け取り後の USDZ を検査する場合は、別の PowerShell で conda-forge の `openusd` 26.08 環境を有効にします。環境の作り方は[第10章の必要な環境](../010/README.md#必要な環境)を参照してください。

## 事前準備

[第11章の手順](../011/README.md)の最後まで進め、`work/path-lab/scene/street_rules.usdc` が `geometry/house.usda` を解決できる状態にします。`scene` 全体を新しい `release-src` にコピーし、配布物は隣の `receiver` に置きます。

## 実行手順

クローンしたリポジトリのルートか `012` フォルダで PowerShell を開きます。以下のブロックは同じウィンドウで順に実行してください。

```powershell
$repo = (git rev-parse --show-toplevel)
Set-Location $repo
uv sync --locked
$python = Join-Path $repo '.venv/Scripts/python.exe'
function Invoke-Sample($file) { & $python (Join-Path $repo $file) @args }
Set-Location work/path-lab
```

以下では Python API で USDZ を受け手の `receiver` に直接書き出します。`update_tile.py` は `release-src` 側の色を変えるので、初版を作った後に実行します。

```powershell
function New-UsdPackage($source, $destination) {
    & $python -c "import sys; from pxr import UsdUtils; sys.exit(0 if UsdUtils.CreateNewUsdzPackage(sys.argv[1], sys.argv[2]) else 1)" $source $destination
    if ($LASTEXITCODE -ne 0) { throw "USDZ の作成に失敗しました: $destination" }
}

Copy-Item scene release-src -Recurse
New-Item -ItemType Directory receiver
New-UsdPackage release-src/street_rules.usdc receiver/street-v1.usdz
Invoke-Sample 012/inspect_delivery.py receiver/street-v1.usdz
Invoke-Sample 012/update_tile.py
New-UsdPackage release-src/street_rules.usdc receiver/street-v2.usdz
Set-Location receiver
Invoke-Sample 012/inspect_delivery.py street-v2.usdz
```

## 期待される結果

`work/path-lab/receiver` に `street-v1.usdz` と `street-v2.usdz` ができます。`stored`、`unencrypted`、`aligned` はすべて `True`。形状の出典はどちらもパッケージ内の `geometry/house.usda` で、第2版の東の屋根色は `(0.42, 0.08, 0.56)` です。

## ファイル一覧

- [inspect_delivery.py](inspect_delivery.py) — 指定した USDZ の格納条件、形状の出典、屋根色を調べる。
- [update_tile.py](update_tile.py) — 配布元コピーの地区色を第2版の紫に変更する。
