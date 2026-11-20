# 第22章 アセットの版管理と依存の整理

通りの西の家だけを初版から第2版へ切り替えます。看板の形状と画像を使い、フラット化の前後で残る依存を比べます。

## 必要な環境

Windows の PowerShell と [共通環境](../README.md#共通環境)（uv、Python 3.13 系、`usd-core` 26.11）を使います。

## 事前準備

この章の入力はすべて同梱しています。ここで使う `street_delivery.usda` は、[第21章の納品用レイヤー](../021/README.md)と同名の、この実習専用のファイルです。下のコマンドで素材を `work/versions-22` にコピーします。初期状態では `street_layout.usda` の `/Street/West/House` が `house-v1.usda` の既定の Prim を参照します。

## 実行手順

リポジトリのルートか `022` フォルダで PowerShell を開きます。

```powershell
$repo = (git rev-parse --show-toplevel)
Set-Location $repo
uv sync --locked
$python = Join-Path $repo '.venv/Scripts/python.exe'
function Invoke-Sample($file) { & $python (Join-Path $repo $file) @args }
New-Item -ItemType Directory -Force work/versions-22/textures | Out-Null
Copy-Item 022/*.usda work/versions-22/
Copy-Item 022/textures/sign.png work/versions-22/textures/
Set-Location work/versions-22
```

同じウィンドウで、版の切り替え、依存の確認、納品用コピーの作成を順に試します。

```powershell
Invoke-Sample 022/list_used.py
Invoke-Sample 022/switch_version.py
Invoke-Sample 022/list_used.py
Invoke-Sample 022/count_deps.py
Invoke-Sample 022/count_deps.py street_layout.usda
Invoke-Sample 022/flatten_delivery.py
Invoke-Sample 022/count_deps.py street_flat.usda
Invoke-Sample 022/remove_billboard.py
Invoke-Sample 022/count_deps.py street_no_billboard.usda
```

初版に戻すには `Invoke-Sample 022/switch_version.py v1` を実行し、`Invoke-Sample 022/list_used.py` で読み込み元を確認します。

## 期待される結果

| 確認するもの | 結果 |
| --- | --- |
| 西の家の版 | 使用レイヤーが `house-v1.usda` から `house-v2.usda` に切り替わる。屋根の高さは 3.0 から 3.5、色は緑から紫に変わる |
| 納品ルートの直接の依存 | サブレイヤーは `./street_layout.usda`、ペイロードは `./billboard.usda`。アセット属性も含めて調べると `./textures/sign.png` が現れる |
| フラット化後 | `street_flat.usda` の外部レイヤー依存は空。看板の形状が残り、画像は引き続き `./textures/sign.png` から読む |
| 看板の面の有無 | アンロード直後は `False`、元のステージを開き直すと `True`。ペイロードを消した `street_no_billboard.usda` では `False` |

## ファイル一覧

- [street_delivery.usda](street_delivery.usda) — レイアウトを重ね、看板のペイロードと材質を記録した納品ルート。
- [street_layout.usda](street_layout.usda) — 西の家の参照先を記録する組み立て用レイヤー。
- [house-v1.usda](house-v1.usda)・[house-v2.usda](house-v2.usda) — 緑の低い屋根と紫の高い屋根を持つ、同じ家の2つの版。
- [billboard.usda](billboard.usda)・[textures/sign.png](textures/sign.png) — 看板の面と、その材質が読む画像。
- [list_used.py](list_used.py) — 使用レイヤー、読み込み元、屋根の高さと色を表示する。
- [switch_version.py](switch_version.py) — レイアウトが参照する版を選ぶ。引数を省くと第2版になる。
- [count_deps.py](count_deps.py) — 指定ファイルに直接書かれた依存を2つの API で比較する。
- [flatten_delivery.py](flatten_delivery.py) — 合成結果を焼き込み、画像のパスを相対化して保存する。
- [remove_billboard.py](remove_billboard.py) — アンロードと、納品レイヤーのコピーからのペイロード削除を比較する。
