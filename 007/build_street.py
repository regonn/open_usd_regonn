from pxr import Gf, Sdf, Usd, UsdGeom

stage = Usd.Stage.CreateNew("street.usda")
street = UsdGeom.Xform.Define(stage, "/Street")
stage.SetDefaultPrim(street.GetPrim())
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)

west = UsdGeom.Xform.Define(stage, "/Street/West")
west.AddTranslateOp().Set(Gf.Vec3d(-1.5, 0, 0))
west_house = stage.DefinePrim("/Street/West/House")
west_house.GetReferences().AddReference("./assembly.usda", Sdf.Path("/House"))

east = UsdGeom.Xform.Define(stage, "/Street/East")
east.AddTranslateOp().Set(Gf.Vec3d(1.5, 0, 0))
east_house = stage.DefinePrim("/Street/East/House")
east_house.GetPayloads().AddPayload("./assembly.usda")

stage.GetRootLayer().Save()
