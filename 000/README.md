# 序章　Omniverse で表示環境構築

[regonn.usd_editor.kit](regonn.usd_editor.kit) は、Kit Base Editor「OpenUSD Study Editor」を実際にビルドしたときの設定です。[create_cube.py](create_cube.py) は、そのエディターで開いているステージに Cube を作り、Cube だけを USDA に書き出します。

## 必要な環境

NVIDIA RTX GPU を搭載した Windows、PowerShell、Git を使います。初回ビルドには、SDK と拡張機能をダウンロードするためのインターネット接続が必要です。実習は Kit SDK 110.4.1 の Kit Base Editor と、その Script Editor に組み込まれた Python で実行します。uv の環境は第1章から使います。

## 事前準備

入力となる USD ファイルは不要です。ビルド用の `kit-app-template` とサンプルのクローンを、次のように並べて用意します。

作業用の親フォルダから実行します。サンプルリポジトリを取得済みなら、1行目を飛ばしてください。

```powershell
git clone https://github.com/regonn/open_usd_regonn.git
git clone https://github.com/NVIDIA-Omniverse/kit-app-template.git
cd kit-app-template
```

序章の実習で使った Kit SDK 110.4.1 に対応するコミットに切り替えます。

```powershell
git switch --detach b8e9f2e4f2930d19e87e3702d4eeaf00d9846676
```

## 実行手順

### 1. Kit Base Editor を作る

以下を実行し、選択式の質問には矢印キーと Enter、入力欄には表の値で回答します。初回にライセンス条項が表示された場合は内容を確認してください。

```powershell
.\repo.bat template new
```

| 質問 | 回答例 |
| --- | --- |
| Select what you want to create | `Application` |
| Select desired template | `Kit Base Editor` |
| Enter name of application .kit file | `regonn.usd_editor` |
| Enter application_display_name | `OpenUSD Study Editor` |
| Enter version | `0.1.0` |
| Do you want to add application layers? | `No` |

テンプレートの生成が終わったら、`kit-app-template` のルートで次のコマンドを実行します。生成直後の設定ファイルを、序章でビルドと起動を確認した [regonn.usd_editor.kit](regonn.usd_editor.kit) で上書きしてから、ビルドに進みます。

```powershell
Copy-Item ..\open_usd_regonn\000\regonn.usd_editor.kit .\source\apps\regonn.usd_editor.kit
```

#### 設定ファイルの読みどころ

| セクション | この実習で見る項目 |
| --- | --- |
| `[package]` | `title` は表示名、`version` はアプリ自身の版（`0.1.0`） |
| `[dependencies]` | `omni.kit.window.stage` は階層パネル、`omni.kit.viewport.window` は 3D 表示。Script Editor は `omni.kit.developer.bundle` の依存関係から読み込まれる |
| `[settings.app]` | `content.emptyStageOnStart = true` で起動時に空のステージを開く。`window.title` はウィンドウのタイトル |
| `BEGIN GENERATED PART` 以降 | ビルドで解決した拡張機能のバージョン。同じ設定を別の SDK で試す場合は、その SDK のテンプレートから生成する |

### 2. ビルドして起動する

`kit-app-template` のルートで順に実行します。ビルドが成功してから起動し、アプリの選択を求められたら `regonn.usd_editor` を選んでください。

```powershell
.\repo.bat build
.\repo.bat launch
```

### 3. Kit でスクリプトを開き、Cube を保存する

新しいステージで **Developer → Script Editor** を開きます。Script Editor のファイルを開く操作で、サンプルの `000/create_cube.py` を読み込んで実行してください。このスクリプトが使う `omni.usd` は Kit から提供されます。

## 期待される結果

Stage パネルには `/World/Cube` が現れます。Cube の一辺は 300、移動量は `(0, 0, 0)` です。実行するたびに一時フォルダを新しく作り、そこに `cube.usda` を保存します。出力の `Saved:` に続くフルパスからファイルを開くと、既定の Prim は `/Root`、その子は `/Root/Cube` です。作例を残す場合は、その USDA を自分の作業フォルダへコピーしてください。

## ファイル一覧

- [regonn.usd_editor.kit](regonn.usd_editor.kit) — テンプレート生成後にコピーするアプリ設定。
- [create_cube.py](create_cube.py) — Kit で Cube を作り、USDA に書き出すスクリプト。

## ライセンス

`regonn.usd_editor.kit` には NVIDIA のテンプレートを使っています。元の著作権表示とライセンス識別子はファイルの先頭にあります。[kit-app-template のライセンス](https://github.com/NVIDIA-Omniverse/kit-app-template/blob/b8e9f2e4f2930d19e87e3702d4eeaf00d9846676/LICENSE)
