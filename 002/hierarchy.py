from pxr import Gf, Usd, UsdGeom


def main() -> None:
    stage: Usd.Stage = Usd.Stage.CreateNew("./hierarchy.usda")
    UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)

    # Root の下に、2つの形状をまとめる Group を作る
    root: UsdGeom.Xform = UsdGeom.Xform.Define(stage, "/Root")
    stage.SetDefaultPrim(root.GetPrim())
    group: UsdGeom.Xform = UsdGeom.Xform.Define(stage, "/Root/Group")

    # 親の変換：Z 軸まわりに90度回転し、X 方向へ10移動
    group.AddTranslateOp().Set(Gf.Vec3d(10, 0, 0))
    group.AddRotateXYZOp().Set(Gf.Vec3f(0, 0, 90))

    # 子1：X 方向へ2移動、Z 軸まわりに45度回転、X 方向に2倍
    cube: UsdGeom.Cube = UsdGeom.Cube.Define(stage, "/Root/Group/Cube")
    cube.GetSizeAttr().Set(1.0)
    cube.AddTranslateOp().Set(Gf.Vec3d(2, 0, 0))
    cube.AddRotateXYZOp().Set(Gf.Vec3f(0, 0, 45))
    cube.AddScaleOp().Set(Gf.Vec3f(2, 1, 1))

    # 子2：Y 方向へ3移動、全方向に0.5倍
    sphere: UsdGeom.Sphere = UsdGeom.Sphere.Define(stage, "/Root/Group/Sphere")
    sphere.GetRadiusAttr().Set(1.0)
    sphere.AddTranslateOp().Set(Gf.Vec3d(0, 3, 0))
    sphere.AddScaleOp().Set(Gf.Vec3f(0.5, 0.5, 0.5))

    stage.GetRootLayer().Save()

    # 子の原点を、親の空間とワールド空間でそれぞれ確認
    time = Usd.TimeCode.Default()
    for shape in (cube, sphere):
        xformable = UsdGeom.Xformable(shape.GetPrim())
        local_matrix = xformable.GetLocalTransformation(time)
        world_matrix = xformable.ComputeLocalToWorldTransform(time)
        local_origin = local_matrix.Transform(Gf.Vec3d(0, 0, 0))
        world_origin = world_matrix.Transform(Gf.Vec3d(0, 0, 0))
        # 回転計算の浮動小数点誤差を丸めて表示
        local = tuple(round(value, 6) for value in local_origin)
        world = tuple(round(value, 6) for value in world_origin)
        print(f"{shape.GetPath()}: local={local}, world={world}")


if __name__ == "__main__":
    main()
