from pxr import Gf, Sdf, Usd, UsdGeom, UsdShade

stage = Usd.Stage.CreateNew("street_rules.usda")
root = stage.GetRootLayer()
root.subLayerPaths.append("./street_choices.usda")
stage.SetDefaultPrim(stage.GetPrimAtPath("/Street"))
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)

base = stage.CreateClassPrim("/TileBase")
base.CreateAttribute("inputs:tint", Sdf.ValueTypeNames.Color3f, custom=False).Set(
    Gf.Vec3f(0.35, 0.35, 0.35)
)
base.CreateAttribute("study:serviceYears", Sdf.ValueTypeNames.Int).Set(30)

district = stage.CreateClassPrim("/DistrictTile")
district.CreateAttribute("inputs:tint", Sdf.ValueTypeNames.Color3f, custom=False).Set(
    Gf.Vec3f(0.04, 0.36, 0.12)
)

for side in ("West", "East"):
    tile = stage.GetPrimAtPath(f"/Street/{side}/House/Looks/GlazedTile")
    tile.GetInherits().AddInherit(district.GetPath())
    tile.GetSpecializes().AddSpecialize(base.GetPath())

west_tile = UsdShade.Material.Get(stage, "/Street/West/House/Looks/GlazedTile")
west_tile.GetInput("tint").Set(Gf.Vec3f(0.85, 0.52, 0.08))
root.Save()
