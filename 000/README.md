# 序章　Omniverse で表示環境構築

[regonn.usd_editor.kit](regonn.usd_editor.kit) は、Kit Base Editor「OpenUSD Study Editor」を実際にビルドしたときの設定です。[create_cube.py](create_cube.py) は、そのエディターで開いているステージに Cube を作り、Cube だけを USDA に書き出します。実習には NVIDIA RTX GPU を搭載した Windows と PowerShell を使います。

## 1. テンプレートを取得する

作業用の親フォルダから実行します。すでにサンプルリポジトリを取得している場合は、その隣に `kit-app-template` を配置してください。

```powershell
git clone https://github.com/regonn/open_usd_regonn.git
git clone https://github.com/NVIDIA-Omniverse/kit-app-template.git
cd kit-app-template
```

使う版を次のどちらかに決めます。

- **書籍の手順を再現する場合**は、次のコマンドで Kit 110.0.0 のテンプレートを選びます。手順2で生成した設定をそのままビルドしてください。

```powershell
git switch --detach cf21b4ca6682946e5ff0a1c8b0105386629bf7c1
```

- **このフォルダの実ファイルを使う場合**は、代わりに次のコミットを選びます。収録した設定の末尾には、ビルド時の Kit SDK 110.4.1 と拡張機能の版が記録されています。

```powershell
git switch --detach b8e9f2e4f2930d19e87e3702d4eeaf00d9846676
```

## 2. Kit Base Editor を作る

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

これで `source/apps/regonn.usd_editor.kit` ができます。**手順1で 110.4.1 を選んだ場合のみ**、生成直後のファイルに実習済みの設定をコピーします。

```powershell
Copy-Item ..\open_usd_regonn\000\regonn.usd_editor.kit .\source\apps\regonn.usd_editor.kit
```

### 設定ファイルの読みどころ

| セクション | この実習で見る項目 |
| --- | --- |
| `[package]` | `title` は表示名、`version` はアプリ自身の版（`0.1.0`） |
| `[dependencies]` | `omni.kit.window.stage` は階層パネル、`omni.kit.viewport.window` は 3D 表示。Script Editor は `omni.kit.developer.bundle` の依存関係から読み込まれる |
| `[settings.app]` | `content.emptyStageOnStart = true` で起動時に空のステージを開く。`window.title` はウィンドウのタイトル |
| `BEGIN GENERATED PART` 以降 | ビルドで解決した拡張機能のバージョン。同じ設定を別の SDK で試す場合は、その SDK のテンプレートから生成する |

## 3. ビルドして起動する

`kit-app-template` のルートで順に実行します。ビルドが成功してから起動し、アプリの選択を求められたら `regonn.usd_editor` を選んでください。

```powershell
.\repo.bat build
.\repo.bat launch
```

## 4. Kit でスクリプトを開き、Cube を保存する

新しいステージで **Developer → Script Editor** を開きます。Script Editor のファイルを開く操作で、サンプルの `000/create_cube.py` を読み込んで実行してください。このスクリプトが使う `omni.usd` は Kit から提供されます。

Stage パネルには `/World/Cube` が現れます。Cube の一辺は 300、移動量は `(0, 0, 0)` です。実行するたびに一時フォルダを新しく作り、そこに `cube.usda` を保存します。出力の `Saved:` に続くフルパスからファイルを開くと、既定の Prim は `/Root`、その子は `/Root/Cube` です。作例を残す場合は、その USDA を自分の作業フォルダへコピーしてください。

## ライセンス

`regonn.usd_editor.kit` には NVIDIA のテンプレートを使っています。元の著作権表示とライセンス識別子はファイルの先頭にあります。[kit-app-template のライセンス](https://github.com/NVIDIA-Omniverse/kit-app-template/blob/b8e9f2e4f2930d19e87e3702d4eeaf00d9846676/LICENSE)
