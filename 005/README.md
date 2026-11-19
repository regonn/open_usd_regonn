# 第5章 マテリアルとシェーディング（UsdShade）

家に漆喰と釉薬瓦のマテリアルを作り、屋根の面だけに瓦を割り当てます。

## 必要な環境

Windows の PowerShell と [共通環境](../README.md#共通環境)（uv、Python 3.13 系、`usd-core` 26.11）を使います。

## 事前準備

`work/house.usda` の `/House` が、面 0 に壁、面 1 に屋根を持つ Mesh であることが前提です。[第4章の手順](../004/README.md)で `mesh.py` を実行してください。

## 実行手順

クローンしたリポジトリのルートか `005` フォルダで PowerShell を開きます。以下のブロックは同じウィンドウで順に実行してください。

```powershell
$repo = (git rev-parse --show-toplevel)
Set-Location $repo
uv sync --locked
$python = Join-Path $repo '.venv/Scripts/python.exe'
function Invoke-Sample($file) { & $python (Join-Path $repo $file) @args }
Set-Location work
```

```powershell
Invoke-Sample 005/materials.py
Invoke-Sample 005/read_materials.py
```

## 期待される結果

`work/house_materials.usda` ができます。`/House` には `Plaster`（粗さ `0.85`）、`/House/RoofFaces` には `GlazedTile`（粗さ `0.20`）が割り当てられます。

## ファイル一覧

- [materials.py](materials.py) — 家をコピーし、シェーダーを接続して壁と屋根に割り当てる。
- [read_materials.py](read_materials.py) — 各 Prim に効いている材質と粗さを表示する。
