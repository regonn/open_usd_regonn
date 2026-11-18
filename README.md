# 『OpenUSD実践入門』のサンプルコード

本書の「その1」から「その22」までの Python 実習を章番号順に収録しています。家を作る実習から、通りを USDZ として配布し、受け手の環境で点検する実習まで進められます。

## uv を用意する

この実習には、Python のパッケージと仮想環境を管理するツール「uv」が必要です。Windows では PowerShell から次のコマンドでインストールできます。[uv 公式のインストール手順](https://docs.astral.sh/uv/getting-started/installation/)

```powershell
winget install --id=astral-sh.uv -e
```

新しい PowerShell を開き、`uv --version` でバージョンが表示されることを確認してください。

## 最初のステージを作る

Windows の PowerShell で、クローンしたリポジトリのルートから始めます。uv は `.python-version` の Python 3.13 系と、`uv.lock` の `usd-core` 26.11 を使います。

```powershell
uv sync --locked
$repo = (Get-Location).Path
$python = Join-Path $repo '.venv/Scripts/python.exe'
function Invoke-Sample($file) { & $python (Join-Path $repo $file) @args }

New-Item -ItemType Directory work
Set-Location work
Invoke-Sample 001/stage.py
```

`Stage created with Default Prim: Root` が表示され、`work/stage.usda` ができます。以下の例は同じ PowerShell で続けて実行してください。スクリプトは現在のフォルダを基準にファイルを読み書きします。はじめからやり直すときは新しい空の作業フォルダを使ってください。

## 章とフォルダの対応

| 章 | フォルダ | 収録内容・実行環境 |
| --- | --- | --- |
| その0　Omniverse で表示環境構築 | 未収録 | Script Editor から Kit が開いているステージを編集する実習。Kit で本文のコードを実行する |
| その1　ファイルフォーマットと Python API | [001](001/) | ステージを作り、球を USDA に保存 |
| その2　Prim の親子階層と座標変換 | [002](002/) | ローカル座標とワールド座標を比較 |
| その3　属性・プロパティ・リレーションシップ | [003](003/) | その2のステージに属性・ターゲットを追加 |
| その4　Mesh の基礎 | [004](004/) | 壁と屋根を作り、面の頂点番号を読み戻す |
| その5　マテリアルとシェーディング | [005](005/) | 壁・屋根の材質を割り当てて確認 |
| その6　レイヤーとレイヤースタック | [006](006/) | 家の形・材質・配色を分け、ミュートを試す |
| その7　参照とペイロード | [007](007/) | 東西に家を配置し、ロード状態を確認 |
| その8　バリアントとバリアントセット | [008](008/) | 家の屋根の仕上げを切り替える |
| その9　継承・スペシャライズと LIVRPS | [009](009/) | 合成後の屋根の色と耐用年数を読む |
| その10　ファイル変換とツール群 | [010](010/) | 配布用のレイヤーを準備し、USDZ を読み戻す |
| その11　アセット解決とパス管理 | [011](011/) | 家を移動し、参照先を調べて修復 |
| その12　USDZ パッケージと配布 | [012](012/) | 配布物の構造・形状の出典を調べ、屋根を更新 |
| その13　モデル階層と Kind | [013](013/) | 配布された通りにモデル境界を設定 |
| その14　コレクションとシーンの整理 | [014](014/) | 家と屋根のコレクションの成員を確認 |
| その15　カメラとライト | [015](015/) | カメラ・ライトの設定と読み戻し。Viewport での見え方は Kit で確認 |
| その16　レンダリングと Hydra | [016](016/) | 描画条件をステージに保存。撮影コードは Kit の Viewport とイベントループを使うため未収録 |
| その17　診断ツールでステージを読む | [017](017/) | 壊れた参照と意図しない色を特定・修復 |
| その18　合成エラーとパフォーマンス | [018](018/) | 循環参照の修復、256区画のステージの計測 |
| その19　Python によるバッチ処理 | [019](019/) | 複数のステージを検査し、CSV と USDC を出力 |
| その20　バリデーションとアセット検証 | [020](020/) | 単位と点検用の球に関する不備を作成・修復 |
| その21　カスタムスキーマとプラグイン | [021](021/) | スキーマの定義、登録、点検属性の読み書き |
| その22　総合演習 | [022](022/) | 道路・カメラを仕上げ、配布先で完成条件を検査 |

Kit の画面操作や、本文の `usdcat`、`usdzip`、`usdchecker` などの CLI 実習は各章を参照してください。CLI の検証環境は conda-forge の `openusd` 26.08 です。以下ではサンプルの入力をそろえるため、USDC 変換と USDZ 作成にも単体の Python API を使います。

## その2〜その9　家と通りのレイヤーを作る

その2の `hierarchy.usda` がその3の入力です。家を題材にする場合は、空の作業フォルダでその4から始められます。

```powershell
Invoke-Sample 002/hierarchy.py
Invoke-Sample 003/properties.py
Invoke-Sample 004/mesh.py
Invoke-Sample 004/read_mesh.py
Invoke-Sample 005/materials.py
Invoke-Sample 005/read_materials.py
Invoke-Sample 006/build_layers.py
Invoke-Sample 006/inspect_layers.py
Invoke-Sample 007/build_street.py
Invoke-Sample 007/inspect_street.py
Invoke-Sample 008/house_choices.py
Invoke-Sample 008/street_choices.py
Invoke-Sample 008/read_choices.py
Invoke-Sample 009/build_rules.py
Invoke-Sample 009/read_rules.py
```

## その10〜その12　配布用の通りを作る

その9までのレイヤーをコピーして作業します。ルートレイヤーを USDC に変換し、依存ファイルを収集して USDZ を作ります。

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

その11では、コピー側で家を移します。移動直後は `resolved: (missing)` となり、修復後に `scene/geometry/house.usda` が表示されます。

```powershell
Set-Location ..
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

その12では修復した通りを配布します。2回目は瓦の色を更新し、受け手のフォルダで更新後の USDZ を開きます。

```powershell
Copy-Item scene release-src -Recurse
New-Item -ItemType Directory receiver
New-UsdPackage release-src/street_rules.usdc receiver/street-v1.usdz
Invoke-Sample 012/inspect_delivery.py receiver/street-v1.usdz
Invoke-Sample 012/update_tile.py
New-UsdPackage release-src/street_rules.usdc receiver/street-v2.usdz
Set-Location receiver
Invoke-Sample 012/inspect_delivery.py street-v2.usdz
```

## その13〜その18　受領した通りを組み立て、診断する

`street-v2.usdz` と同じフォルダから続けます。その17の参照切れとその18の循環は意図的に作る診断対象です。修復の前後で同じステージを開き直してください。

```powershell
Invoke-Sample 013/build_models.py
Invoke-Sample 013/inspect_models.py
Invoke-Sample 014/build_collections.py
Invoke-Sample 014/inspect_collections.py
Invoke-Sample 015/build_lighting.py
Invoke-Sample 015/inspect_lighting.py
Invoke-Sample 016/build_render.py
Invoke-Sample 017/inspect_street.py street_render.usda
Invoke-Sample 017/make_faults.py
Invoke-Sample 017/inspect_street.py street_check.usda
Invoke-Sample 017/repair_street.py reference
Invoke-Sample 017/repair_street.py tint
Invoke-Sample 017/inspect_street.py street_check.usda
Invoke-Sample 018/cycle.py create
Invoke-Sample 018/cycle.py repair
Invoke-Sample 018/build_blocks.py
Invoke-Sample 018/measure_stage.py blocks_plain.usda
Invoke-Sample 018/measure_stage.py blocks_shared.usda
```

## その19〜その22　検査、修復、納品

通り一式を新しいフォルダにコピーします。最初のバッチ検査は循環参照のため1件が不合格になります。修復してもう一度実行すると、4件とも合格して USDC が書き出されます。

```powershell
New-Item -ItemType Directory batch-19
Copy-Item *.usda,street-v2.usdz -Destination batch-19
Set-Location batch-19
$roots = 'street_check.usda','street_cycle.usda','blocks_plain.usda','blocks_shared.usda'
Invoke-Sample 018/cycle.py create
Invoke-Sample 019/batch_street.py --export @roots
Copy-Item report.csv report-before.csv
Invoke-Sample 018/cycle.py repair
Invoke-Sample 019/batch_street.py --export @roots
Invoke-Sample 020/create_delivery.py
Invoke-Sample 020/repair_delivery.py units
Invoke-Sample 020/repair_delivery.py marker
```

その20のルール別の診断を試す場合は、各修復の前後で本文の `usdchecker` を実行します。その21ではスキーマの元ファイルを作業フォルダにコピーします。生成時だけ Jinja2 を追加し、同じ `usd-core` のジェネレーターでコードレスプラグインの定義を作ります。登録の有無は別々の Python プロセスで比較します。

```powershell
Copy-Item (Join-Path $repo '021/streetInspection') . -Recurse
uv run --locked --project $repo --with jinja2 python -m pxr.Usd.usdGenSchema streetInspection/schema.usda streetInspection/resources
Invoke-Sample 021/apply_inspection.py
Invoke-Sample 021/read_inspection.py --register
Invoke-Sample 021/read_inspection.py
```

その22では、USDZ と点検スキーマを一緒に渡します。受け手のフォルダで検査を実行し、東西の屋根、点検状態、カメラ、依存レイヤーの解決先を確認します。

```powershell
Invoke-Sample 022/build_final.py
New-Item -ItemType Directory receiver-22/streetInspection/resources
New-UsdPackage street_final.usda receiver-22/street-final.usdz
Copy-Item streetInspection/resources/plugInfo.json,streetInspection/resources/generatedSchema.usda receiver-22/streetInspection/resources
Set-Location receiver-22
Invoke-Sample 022/check_final.py
```
