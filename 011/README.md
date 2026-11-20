# 第11章 インポーター／エクスポーターとツール連携

同じ Alembic ファイルを使い、環境に登録されたファイル形式と、実際に開ける形式を照合します。

## 必要な環境

Windows の PowerShell と [共通環境](../README.md#共通環境)（uv、Python 3.13 系、`usd-core` 26.11）を使います。読み込みに成功する例は、[序章の Kit Base Editor](../000/README.md)（Kit 110.4.1）で確認できます。

## 事前準備

2軒の家を収めた `houses.abc` を同梱しています。この章から始める場合も、そのファイルだけで形式判定を試せます。本文の追加例で通り全体を Alembic に書き出す場合は、[第7章の手順](../007/README.md)で `street.usda` と依存レイヤーをそろえ、usdAbc を利用できる `usdcat` を使ってください。

## 実行手順

クローンしたリポジトリのルートか `011` フォルダで PowerShell を開きます。

```powershell
$repo = (git rev-parse --show-toplevel)
Set-Location $repo
uv sync --locked
$python = Join-Path $repo '.venv/Scripts/python.exe'
function Invoke-Sample($file) { & $python (Join-Path $repo $file) @args }
New-Item -ItemType Directory -Force work/formats | Out-Null
Copy-Item 011/houses.abc work/formats/
Set-Location work/formats
Invoke-Sample 011/formats.py
Invoke-Sample 011/open_cache.py
```

Kit でも試す場合は、Script Editor で次を実行します。パスは手元の `houses.abc` の絶対パスに置き換えてください。

```python
from pxr import Usd, UsdGeom

stage = Usd.Stage.Open(r"C:\path\to\open_usd_regonn\011\houses.abc")
for prim in stage.Traverse():
    if prim.IsA(UsdGeom.Mesh):
        print(prim.GetPath())
```

## 期待される結果

- 単体 Python では `['usd', 'usda', 'usdc', 'usdz']` が表示され、`abc` と `gltf` の検索結果は `None` です。レイヤーと Stage の読み込みはどちらも例外になり、スクリプトが `Cannot determine file format` を表示します。
- Kit では同じファイルから `/Street/West` と `/Street/East` が読めます。各 Mesh は四角い壁と三角の屋根を持ちます。

## ファイル一覧

- [formats.py](formats.py) — 登録された拡張子と形式ごとの検索結果を表示する。
- [open_cache.py](open_cache.py) — 作業フォルダの Alembic をレイヤーと Stage として開き、両方の結果を表示する。
- [houses.abc](houses.abc) — 本書用に作成した2軒の家の形状。Kit 同梱 USD で書き出した Ogawa 形式の Alembic。
