from pxr import Kind, Usd, UsdGeom

stage = Usd.Stage.CreateNew("street_models.usda")
root = stage.GetRootLayer()
root.subLayerPaths.append("./street-v2.usdz")

street = stage.GetPrimAtPath("/Street")
stage.SetDefaultPrim(street)
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)
UsdGeom.SetStageMetersPerUnit(stage, 0.01)
Usd.ModelAPI(street).SetKind(Kind.Tokens.assembly)

for side in ("West", "East"):
    district = street.GetChild(side)
    house = district.GetChild("House")
    roof = house.GetChild("RoofFaces")
    Usd.ModelAPI(district).SetKind(Kind.Tokens.group)
    Usd.ModelAPI(house).SetKind(Kind.Tokens.component)
    Usd.ModelAPI(roof).SetKind(Kind.Tokens.subcomponent)

root.Save()
