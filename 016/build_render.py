from pxr import Gf, Usd, UsdGeom, UsdRender

stage = Usd.Stage.CreateNew("street_render.usda")
root = stage.GetRootLayer()
root.subLayerPaths.append("./street_lighting.usda")
stage.SetDefaultPrim(stage.GetPrimAtPath("/Street"))
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)
UsdGeom.SetStageMetersPerUnit(stage, 0.01)

camera = UsdGeom.Camera.Get(stage, "/Shot/StreetCam")
UsdGeom.Scope.Define(stage, "/Render")
for name, size in (("Draft", (160, 90)), ("Review", (960, 540))):
    settings = UsdRender.Settings.Define(stage, f"/Render/{name}")
    settings.CreateCameraRel().SetTargets([camera.GetPath()])
    settings.CreateResolutionAttr(Gf.Vec2i(*size))

root.Save()
