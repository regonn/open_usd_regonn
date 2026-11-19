# 第6章 レイヤーとレイヤースタック

家の形、材質、上塗りの色を別のレイヤーに置き、合成の順序とミュートの効果を調べます。

## 必要な環境

Windows の PowerShell と [共通環境](../README.md#共通環境)（uv、Python 3.13 系、`usd-core` 26.11）を使います。

## 事前準備

`work` に第4章の `house.usda` と第5章の `house_materials.usda` をそろえます。[第5章の手順](../005/README.md)で形状のコピーに材質を割り当て、元の家も残してください。

## 実行手順

クローンしたリポジトリのルートか `006` フォルダで PowerShell を開きます。以下のブロックは同じウィンドウで順に実行してください。

```powershell
$repo = (git rev-parse --show-toplevel)
Set-Location $repo
uv sync --locked
$python = Join-Path $repo '.venv/Scripts/python.exe'
function Invoke-Sample($file) { & $python (Join-Path $repo $file) @args }
Set-Location work
```

```powershell
Invoke-Sample 006/build_layers.py
Invoke-Sample 006/inspect_layers.py
```

## 期待される結果

`work` に `assembly.usda`、`look.usda`、`paint.usda` ができます。`muted` と `reordered` では屋根の色が変わり、面の頂点数は常に `[4, 3]` です。

## ファイル一覧

- [build_layers.py](build_layers.py) — 材質と上塗りのレイヤーを作り、形状と重ねる。
- [inspect_layers.py](inspect_layers.py) — ミュート前後とサブレイヤーの並べ替え後の色を比較する。
