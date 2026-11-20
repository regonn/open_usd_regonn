# 第22章 カスタムスキーマとプラグイン

街区の点検情報を持つコードレス API スキーマを生成し、プラグインを登録した場合としない場合の値を比較します。

## 必要な環境

Windows の PowerShell と [共通環境](../README.md#共通環境)（uv、Python 3.13 系、`usd-core` 26.11）を使います。 スキーマ生成時だけ `uv run --with jinja2` で Jinja2 を追加します。

本文の CLI 版 `usdGenSchema` と `usdcat` を使う場合は、別の PowerShell で conda-forge の `openusd` 26.08 環境を有効にします。環境の作り方は[第10章の必要な環境](../010/README.md#必要な環境)を参照してください。

## 事前準備

[第21章の手順](../021/README.md)で `street_delivery.usda` の単位と点検球を修復します。`work/path-lab/receiver/batch-20` に `street_check.review.usdc` 以下の依存ファイルを残し、その中にスキーマの作業用コピーを作ります。

## 実行手順

クローンしたリポジトリのルートか `022` フォルダで PowerShell を開きます。以下のブロックは同じウィンドウで順に実行してください。

```powershell
$repo = (git rev-parse --show-toplevel)
Set-Location $repo
uv sync --locked
$python = Join-Path $repo '.venv/Scripts/python.exe'
function Invoke-Sample($file) { & $python (Join-Path $repo $file) @args }
Set-Location work/path-lab/receiver/batch-20
```

生成・登録は `batch-20` 内のコピーで行います。`read_inspection.py` は2回とも新しい Python プロセスで起動し、登録の影響を比較します。

```powershell
Copy-Item (Join-Path $repo '022/streetInspection') . -Recurse
uv run --locked --project $repo --with jinja2 python -m pxr.Usd.usdGenSchema streetInspection/schema.usda streetInspection/resources
Invoke-Sample 022/apply_inspection.py
Invoke-Sample 022/read_inspection.py --register
Invoke-Sample 022/read_inspection.py
```

## 期待される結果

`streetInspection/resources/generatedSchema.usda` と `street_inspection.usda` ができます。生成時に `CMakeLists.txt` や `module.cpp` がないという警告が表示されることがあります。この章のコードレススキーマは、続く読み戻しで確認できます。登録ありは `schema known: True` で西が `passed`、東が `pending`、間隔は両方 `30` です。登録なしでは明示した西の値だけが読め、スキーマの既定値は `None` になります。

## ファイル一覧

- [streetInspection/schema.usda](streetInspection/schema.usda) — 点検状態と間隔を定義するスキーマの元ファイル。
- [streetInspection/resources/plugInfo.json](streetInspection/resources/plugInfo.json) — コードレスプラグインの登録情報。生成時には作業用コピーを使う。
- [apply_inspection.py](apply_inspection.py) — プラグインを登録し、東西の家にスキーマを適用して西の点検結果を保存する。
- [read_inspection.py](read_inspection.py) — 別プロセスで `--register` の有無を切り替えて値を読む。
