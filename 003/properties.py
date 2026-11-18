from pxr import Gf, Sdf, Usd, UsdGeom


def main() -> None:
    # 前章のシーンを別名で保存し、コピーを編集する
    source = Usd.Stage.Open("./hierarchy.usda")
    source.GetRootLayer().Export("./properties.usda")
    stage = Usd.Stage.Open("./properties.usda")

    cube = UsdGeom.Cube(stage.GetPrimAtPath("/Root/Group/Cube"))
    sphere = UsdGeom.Sphere(stage.GetPrimAtPath("/Root/Group/Sphere"))
    if not cube or not sphere:
        raise RuntimeError("Run the chapter 2 example first.")
    cube_prim = cube.GetPrim()

    # 再生範囲と、数値のタイムサンプルを読むときの補間方法
    stage.SetStartTimeCode(1)
    stage.SetEndTimeCode(25)
    stage.SetTimeCodesPerSecond(24)
    stage.SetInterpolationType(Usd.InterpolationTypeLinear)

    # スキーマで定義された属性の値を設定する
    size_attr = cube.GetSizeAttr()
    size_attr.Set(1.5)
    cube.GetDisplayColorAttr().Set([Gf.Vec3f(0.25, 0.5, 1.0)])

    # 独自のラベルと数値を、型を指定して作成する
    label = cube_prim.CreateAttribute(
        "study:label",
        Sdf.ValueTypeNames.String,
        custom=True,
        variability=Sdf.VariabilityUniform,
    )
    label.Set("Main cube")
    temperature = cube_prim.CreateAttribute(
        "study:temperature",
        Sdf.ValueTypeNames.Float,
        custom=True,
        variability=Sdf.VariabilityVarying,
    )
    temperature.Set(20.0)
    temperature.Set(30.0, Usd.TimeCode(1))
    temperature.Set(50.0, Usd.TimeCode(25))

    # Cube から Sphere を対象とする関係を記録する
    partner = cube_prim.CreateRelationship("study:partner", custom=True)
    partner.SetTargets([sphere.GetPath()])

    stage.GetRootLayer().Save()

    # 属性を名前でも取得し、デフォルトと数値の時刻を読み分ける
    read_temperature = cube_prim.GetAttribute("study:temperature")
    print("size:", size_attr.GetTypeName(), size_attr.Get())
    print("label:", cube_prim.GetAttribute("study:label").Get())
    print("default:", read_temperature.Get())
    print("samples:", read_temperature.GetTimeSamples())
    print("time 13:", read_temperature.Get(Usd.TimeCode(13)))
    targets = cube_prim.GetRelationship("study:partner").GetTargets()
    print("targets:", [str(path) for path in targets])
    print("target exists:", bool(stage.GetPrimAtPath(targets[0])))


if __name__ == "__main__":
    main()
