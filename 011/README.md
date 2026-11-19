# 第11章 アセット解決とパス管理（Ar リゾルバ）

通りを別の場所に移し、家が見つからなくなる条件と、パスを書き換える位置を確認します。

## 必要な環境

Windows の PowerShell と [共通環境](../README.md#共通環境)（uv、Python 3.13 系、`usd-core` 26.11）を使います。

## 事前準備

[第10章の手順](../010/README.md)で `work/exchange-work` の `street_rules.usdc` と7枚の依存 USDA を準備します。以下の `$files` がコピーする8枚の一覧です。`work/path-lab` は新しい作業場所として使います。

## 実行手順

クローンしたリポジトリのルートか `011` フォルダで PowerShell を開きます。以下のブロックは同じウィンドウで順に実行してください。

```powershell
$repo = (git rev-parse --show-toplevel)
Set-Location $repo
uv sync --locked
$python = Join-Path $repo '.venv/Scripts/python.exe'
function Invoke-Sample($file) { & $python (Join-Path $repo $file) @args }
Set-Location work
```

`house.usda` は `path-lab/scene` のコピーだけを移動します。移動直後の読み込み警告を確認してから、検索パスの比較と修復に進んでください。

```powershell
New-Item -ItemType Directory path-lab/scene
$files = 'street_rules.usdc','street_choices.usda','street.usda','house_choices.usda','assembly.usda','house.usda','look.usda','paint.usda'
foreach ($file in $files) { Copy-Item (Join-Path exchange-work $file) path-lab/scene }
Set-Location path-lab
Invoke-Sample 011/inspect_paths.py
New-Item -ItemType Directory scene/geometry
Move-Item scene/house.usda scene/geometry/house.usda
Invoke-Sample 011/inspect_paths.py
Invoke-Sample 011/search_paths.py
Invoke-Sample 011/fix_path.py
Invoke-Sample 011/inspect_paths.py
```

## 期待される結果

移動直後は `resolved: (missing)` となり、面が読めません。修復後は `resolved: scene/geometry/house.usda` と表示され、東西とも `[4, 3]` に戻ります。第12章の入力は、この修復済みの `scene` 一式です。

## ファイル一覧

- [inspect_paths.py](inspect_paths.py) — 記録されたパスと解決先、通りから読める面を表示する。
- [search_paths.py](search_paths.py) — 検索パスを指定し、`./house.usda` と `house.usda` の解決結果を比較する。
- [fix_path.py](fix_path.py) — `scene/assembly.usda` の形状レイヤーのパスを修復する。
