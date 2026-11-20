from pathlib import Path

from pxr import Plug, Usd, UsdGeom

resources = Path("streetInspection/resources").resolve()
Plug.Registry().RegisterPlugins(str(resources / "plugInfo.json"))
schema = "StreetInspectionAPI"
if not Usd.SchemaRegistry().FindAppliedAPIPrimDefinition(schema):
    raise RuntimeError(f"Schema not found: {schema}")

stage = Usd.Stage.CreateNew("street_inspection.usda")
root = stage.GetRootLayer()
root.subLayerPaths.append("./street_delivery.usda")
stage.SetDefaultPrim(stage.GetPrimAtPath("/Street"))
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)
UsdGeom.SetStageMetersPerUnit(stage, 0.01)

for side in ("West", "East"):
    house = stage.GetPrimAtPath(f"/Street/{side}/House")
    if not house.ApplyAPI(schema):
        raise RuntimeError(f"Could not apply {schema} to {house.GetPath()}")

west = stage.GetPrimAtPath("/Street/West/House")
west.GetAttribute("inspection:status").Set("passed")
root.Save()
