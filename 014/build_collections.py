from pxr import Usd, UsdGeom

stage = Usd.Stage.CreateNew("street_collections.usda")
root = stage.GetRootLayer()
root.subLayerPaths.append("./street_models.usda")
street = stage.GetPrimAtPath("/Street")
stage.SetDefaultPrim(street)
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)
UsdGeom.SetStageMetersPerUnit(stage, 0.01)

houses = Usd.CollectionAPI.Apply(street, "houses")
roofs = Usd.CollectionAPI.Apply(street, "roofs")
for collection in (houses, roofs):
    collection.CreateExpansionRuleAttr().Set(Usd.Tokens.explicitOnly)

for side in ("West", "East"):
    house = street.GetChild(side).GetChild("House")
    houses.CreateIncludesRel().AddTarget(house.GetPath())
    roofs.CreateIncludesRel().AddTarget(house.GetChild("RoofFaces").GetPath())

west = street.GetChild("West")
survey = Usd.CollectionAPI.Apply(street, "westSurvey")
survey.CreateExpansionRuleAttr().Set(Usd.Tokens.expandPrims)
survey.CreateIncludesRel().AddTarget(west.GetPath())
survey.CreateExcludesRel().AddTarget(west.GetChild("House").GetChild("Looks").GetPath())
root.Save()
