from pxr import Gf, Sdf, Usd, UsdGeom, UsdShade

road = Usd.Stage.CreateNew("road.usda")
road.SetDefaultPrim(UsdGeom.Xform.Define(road, "/Road").GetPrim())
UsdGeom.SetStageUpAxis(road, UsdGeom.Tokens.y)
UsdGeom.SetStageMetersPerUnit(road, 0.01)


def paint(name, color):
    material = UsdShade.Material.Define(road, "/Road/Looks/" + name)
    shader = UsdShade.Shader.Define(road, material.GetPath().AppendChild("Surface"))
    shader.CreateIdAttr("UsdPreviewSurface")
    shader.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).Set(color)
    surface = shader.CreateOutput("surface", Sdf.ValueTypeNames.Token)
    material.CreateSurfaceOutput().ConnectToSource(surface)
    return material


def slab(name, center, size, material):
    cube = UsdGeom.Cube.Define(road, "/Road/" + name)
    cube.CreateSizeAttr(1)
    cube.AddTranslateOp().Set(Gf.Vec3d(*center))
    cube.AddScaleOp().Set(Gf.Vec3f(*size))
    UsdShade.MaterialBindingAPI.Apply(cube.GetPrim()).Bind(material)


UsdGeom.Scope.Define(road, "/Road/Looks")
asphalt = paint("Asphalt", Gf.Vec3f(0.065, 0.075, 0.09))
ivory = paint("Ivory", Gf.Vec3f(0.8, 0.76, 0.55))
slab("Pavement", (0, -0.05, 0), (9, 0.1, 1.8), asphalt)
for i in range(5):
    slab(f"Dash_{i}", ((i - 2) * 1.6, 0.01, 0), (0.85, 0.02, 0.08), ivory)
road.GetRootLayer().Save()

stage = Usd.Stage.CreateNew("street_final.usda")
stage.GetRootLayer().subLayerPaths.append("./street_inspection.usda")
street = stage.GetPrimAtPath("/Street")
stage.SetDefaultPrim(street)
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)
UsdGeom.SetStageMetersPerUnit(stage, 0.01)

placement = UsdGeom.Xform.Define(stage, "/Street/Road")
placement.GetPrim().GetReferences().AddReference("./road.usda")
placement.AddTranslateOp().Set(Gf.Vec3d(0, 0, 1))
street.GetVariantSets().GetVariantSet("reviewMode").SetVariantSelection("inspection")

camera = UsdGeom.Camera.Get(stage, "/Shot/StreetCam")
camera.GetPrim().GetAttribute("xformOp:translate").Set(Gf.Vec3d(0, 4, 15))
camera.AddRotateXOp().Set(-10)
stage.GetRootLayer().Save()
