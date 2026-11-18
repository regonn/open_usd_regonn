import argparse

from pxr import Sdf, Usd, UsdGeom

parser = argparse.ArgumentParser()
parser.add_argument("action", choices=["create", "repair"])
action = parser.parse_args().action
path = "street_cycle.usda"

if action == "create":
    stage = Usd.Stage.CreateNew(path)
    stage.GetRootLayer().subLayerPaths.append("./street_check.usda")
    stage.SetDefaultPrim(stage.GetPrimAtPath("/Street"))
    UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)
    UsdGeom.SetStageMetersPerUnit(stage, 0.01)
    a = UsdGeom.Xform.Define(stage, "/PlanA").GetPrim()
    b = UsdGeom.Xform.Define(stage, "/PlanB").GetPrim()
    a.GetReferences().AddInternalReference("/PlanB")
    b.GetReferences().AddInternalReference("/PlanA")
else:
    stage = Usd.Stage.Open(path)
    b = stage.GetPrimAtPath("/PlanB")
    b.GetReferences().SetReferences([Sdf.Reference("", "/Street/West")])

stage.GetRootLayer().Save()
stage = Usd.Stage.Open(path)
errors = stage.GetCompositionErrors()
print("composition errors:", len(errors))
for error in errors:
    print(error)
house = stage.GetPrimAtPath("/PlanA/House")
print("PlanA has a house mesh:", bool(house) and house.IsA(UsdGeom.Mesh))
