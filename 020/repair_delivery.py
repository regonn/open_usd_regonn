import argparse

from pxr import Gf, Usd, UsdGeom

parser = argparse.ArgumentParser()
parser.add_argument("target", choices=["units", "marker"])
target = parser.parse_args().target
stage = Usd.Stage.Open("street_delivery.usda")

if target == "units":
    UsdGeom.SetStageMetersPerUnit(stage, 0.01)
else:
    street = stage.GetDefaultPrim()
    view = street.GetVariantSets().GetVariantSet("reviewMode")
    view.SetVariantSelection("inspection")
    with view.GetVariantEditContext():
        stage.RemovePrim("/Street/West/House/Marker")
        marker = UsdGeom.Sphere.Define(stage, "/Street/West/Marker")
        marker.CreateRadiusAttr(0.25)
        marker.AddTranslateOp().Set(Gf.Vec3d(0, 3.5, 0))
    view.SetVariantSelection("beauty")
stage.GetRootLayer().Save()
