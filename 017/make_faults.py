from pxr import Gf, Sdf, Usd, UsdGeom

stage = Usd.Stage.CreateNew("street_check.usda")
root = stage.GetRootLayer()
root.subLayerPaths.append("./street_render.usda")
stage.SetDefaultPrim(stage.GetPrimAtPath("/Street"))
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)
UsdGeom.SetStageMetersPerUnit(stage, 0.01)

west = stage.GetPrimAtPath("/Street/West/House")
west.GetReferences().SetReferences([Sdf.Reference("./missing_house.usda", "/House")])

tile = stage.GetPrimAtPath("/Street/East/House/Looks/GlazedTile")
tile.GetAttribute("inputs:tint").Set(Gf.Vec3f(0.05, 0.65, 0.1))
root.Save()
