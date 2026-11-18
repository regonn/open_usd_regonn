from pxr import Gf, Usd, UsdGeom

stage = Usd.Stage.CreateNew("street_delivery.usda")
root = stage.GetRootLayer()
root.subLayerPaths.append("./street_check.review.usdc")
street = stage.GetPrimAtPath("/Street")
stage.SetDefaultPrim(street)
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)

view = street.GetVariantSets().AddVariantSet("reviewMode")
for name in ("beauty", "inspection"):
    view.AddVariant(name)
view.SetVariantSelection("inspection")
with view.GetVariantEditContext():
    marker = UsdGeom.Sphere.Define(stage, "/Street/West/House/Marker")
    marker.CreateRadiusAttr(0.25)
    marker.AddTranslateOp().Set(Gf.Vec3d(0, 3.5, 0))
view.SetVariantSelection("beauty")
root.Save()
