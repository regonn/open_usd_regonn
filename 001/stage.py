from pxr import Gf, Usd, UsdGeom


def main() -> None:
    # 1. 新しいUSDステージを作成（.usda形式を指定して可読性を確保）
    stage: Usd.Stage = Usd.Stage.CreateNew("./stage.usda")

    # 2. 最初のPrim（プリミティブ）を定義
    # デジタルツイン等の構築では、Xformをルートに置くのが作法です。
    root_xform: UsdGeom.Xform = UsdGeom.Xform.Define(stage, "/Root")

    # 3. デフォルトPrimの設定
    # 他のUSDファイルから参照（Reference）される際、どのPrimを主軸にするかを明示します。
    # これを忘れると、コンポジション時に意図したデータが読み込まれません。
    stage.SetDefaultPrim(root_xform.GetPrim())

    # 4. 球体（ルート配下に定義。ジオメトリは既定Prim設定の後に追加する）
    sphere: UsdGeom.Sphere = UsdGeom.Sphere.Define(stage, "/Root/Sphere")
    sphere.GetRadiusAttr().Set(1.0)
    sphere.GetDisplayColorAttr().Set([Gf.Vec3f(0.35, 0.55, 0.95)])

    # 5. メモリ上の変更をファイルシステムへ書き出し（保存）
    stage.GetRootLayer().Save()

    default_prim: Usd.Prim = stage.GetDefaultPrim()
    print(f"Stage created with Default Prim: {default_prim.GetName()}")


if __name__ == "__main__":
    main()
